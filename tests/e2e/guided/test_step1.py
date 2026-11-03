"""T-181 (D-068) guided UI, Step 1 Add records: /new and /case/<token>/records. Spec section 4. Builder A.
Two servers: the shared test server (demo mode: the fixture backend, so Paste and Upload are not offered as working) and a private LIVE-mode server (ENABLE_LIVE=1 with the claude-cli backend name; it only
creates cases (ingest is code), it never runs one) for the paste, .txt and .pdf paths and their real 413 / pdf refusals. Errors the servers do not produce on demand (429, offline, 409) use a route stub.
Test ids: input-name, name-error, tile-paste|file|sample|library, radio-<key>, input-text, file-input, btn-choose-file, library-<id>, btn-read, btn-draft, btn-start-over, bar-msg, action-bar, btn-use-sample, btn-retry-read,
btn-ocr, btn-hidden-anyway, check-hidden, demo-note, records-list, records-notes, stage-list, draft-bar, draft-done, done-counts, ai-banner, prepared-badge, btn-next-step, draft-failed, btn-run-again, btn-run-yes, btn-run-cancel."""
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import pytest
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided._helpers import api, make_case, uid, browser, shot, in_view, no_h_scroll, go, jbody, err
from tests.e2e.guided.test_shell_smoke import watch

STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]


def health():
    return api("GET", "/api/health")[1]


@pytest.fixture
def made():
    toks = []
    yield toks
    for t in toks:
        api("DELETE", f"/api/cases/{t}")


@pytest.fixture(scope="module")
def live():
    """A private live-mode server (never runs a case). Yields its base URL."""
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    tmp = tempfile.mkdtemp(prefix="zlayt-live-")
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", ENABLE_LIVE="1", LLM_BACKEND="claude-cli", ZLAYT_DB=os.path.join(tmp, "live.sqlite3"))
    env.pop("ANTHROPIC_API_KEY", None)
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=C.ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
            except Exception:
                if proc.poll() is not None:
                    pytest.fail("the live-mode test server exited early")
                time.sleep(.5)
        else:
            pytest.fail("the live-mode test server did not answer")
        assert json.load(urllib.request.urlopen(base + "/api/health"))["demo_mode"] is False
        yield base
    finally:
        proc.terminate()
        try: proc.wait(timeout=10)
        except Exception: proc.kill()
        log.close()


def goto(page, base, path):
    page.goto(base + path)
    page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=15000)


def box(page, tid):
    b = page.get_by_test_id(tid).bounding_box(); return [round(b[k]) for k in ("x", "y", "width", "height")]


# ------------------------------------------------------------------ demo mode: no Paste/Upload as if they worked
def test_demo_mode_explains_and_disables_paste_and_upload_and_the_primary_is_above_the_fold(pw):
    if not health()["demo_mode"]:
        pytest.skip("demo-mode test")
    for w, h in ((1440, 900), (1366, 768), (390, 844)):
        br, page = browser(pw, w, h)
        try:
            seen = watch(page); go(page, "/new")
            expect(page.get_by_test_id("page-title")).to_have_text("Add records")
            note = page.get_by_test_id("demo-note"); expect(note).to_contain_text("This demo can only read the sample case and our test cases.")
            for k in ("paste", "file"):                          # shown, disabled, and the reason is visible text (not a tooltip)
                t = page.get_by_test_id(f"tile-{k}")
                assert t.get_attribute("aria-disabled") == "true"; expect(page.get_by_test_id(f"radio-{k}")).to_be_disabled()
                expect(t).to_contain_text("Not available in this demo.")
            expect(page.get_by_test_id("radio-sample")).to_be_checked()
            read = page.get_by_test_id("btn-read")
            expect(read).to_be_enabled(); assert in_view(page, read), (w, h)       # Read the records is on screen with no scrolling
            assert no_h_scroll(page), (w, h)
            assert [s for s in seen if "library" not in s and "404" not in s] == [], seen
            if h in (900, 844):
                shot(page, "new-demo", w)
        finally:
            br.close()


def test_demo_mode_offers_the_sample_and_a_test_case_and_reads_either(pw, made):
    hl = health()
    if not hl["demo_mode"]:
        pytest.skip("demo-mode test")
    lib = api("GET", "/api/library")
    br, page = browser(pw, 1440, 900)
    try:
        go(page, "/new")
        name = f"Sample {uid()}"; page.get_by_test_id("input-name").fill(name)
        page.get_by_test_id("btn-read").click()
        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
        made.append(page.url.split("/case/")[1].split("/")[0])
        expect(page.get_by_test_id("page-title")).to_have_text("We found 9 records")
        expect(page.get_by_test_id("case-title")).to_have_text(name)
        if lib[0] != 200:
            return
        go(page, "/new")                                         # a test case from the library (local mode lists it)
        page.get_by_test_id("tile-library").click()
        read = page.get_by_test_id("btn-read"); expect(read).to_be_disabled()      # nothing picked yet
        first = lib[1]["cases"][0]["id"]; page.get_by_test_id(f"library-{first}").check(); expect(read).to_be_enabled()
        read.click(); expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
        made.append(page.url.split("/case/")[1].split("/")[0])
        assert int(re.search(r"(\d+)", page.get_by_test_id("page-title").inner_text()).group(1)) >= 1
    finally:
        br.close()


# ------------------------------------------------------------------ the whole step, by clicking
def test_sample_read_found_draft_done_a_first_time_user_needs_no_instructions(pw, made):
    br, page = browser(pw, 1440, 900)
    try:
        seen = watch(page); go(page, "/new")
        page.get_by_test_id("btn-read").click()
        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
        tok = page.url.split("/case/")[1].split("/")[0]; made.append(tok)
        expect(page.get_by_test_id("page-title")).to_have_text("We found 9 records")
        assert page.get_by_test_id("records-list").locator("li").count() == 9
        assert page.get_by_test_id("records-list").locator("li").first.inner_text().split("\n")[1:] == ["January 9, 2026", "Austin EMS run report"] or "January 9, 2026" in page.get_by_test_id("records-list").inner_text()
        expect(page.get_by_test_id("records-notes")).to_contain_text("Every record has a date we could read.")
        assert page.get_by_test_id("step-1").locator(".st-status").inner_text() == "Not started"
        draft = page.get_by_test_id("btn-draft"); assert in_view(page, draft); shot(page, "step1-found", 1440)
        draft.click()
        done = page.get_by_test_id("draft-done"); expect(done).to_be_visible(timeout=20000)
        c = api("GET", f"/api/cases/{tok}")[1]
        n2 = len([i for i in c["entries"] + c["undated_entries"] + c["flags"] if i["state"] != "rejected"]); n3 = len([i for i in c["amounts"] if i["state"] != "rejected"])
        expect(page.get_by_test_id("done-counts")).to_have_text(f"{n2} timeline items and {n3} bill amounts are ready for you to check.")
        hl = health()
        expect(page.get_by_test_id("ai-banner")).to_have_text(hl["ai_banner"])      # D-065: the provenance sentence the server sends
        if hl["answers"] == "prepared":
            b = page.get_by_test_id("prepared-badge")
            assert "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." == b.get_attribute("title")
            expect(page.locator("main")).to_contain_text("Prepared by our team for this demo, not written by an AI model.")    # visible, not only a tooltip
        expect(page.get_by_test_id("step-1").locator(".st-status")).to_have_text("Done")
        go_next = page.get_by_test_id("btn-next-step"); assert in_view(page, go_next)
        assert go_next.get_attribute("href") == f"/case/{tok}/timeline" and go_next.inner_text() == "Go to step 2: Check the timeline"
        shot(page, "step1-done", 1440)
        page.reload(); page.locator("[data-testid=view][data-ready]").wait_for(state="attached")      # a reload lands on the same done screen
        expect(page.get_by_test_id("draft-done")).to_be_visible()
        assert seen == [], seen
    finally:
        br.close()


def test_drafting_shows_one_plain_checklist_then_the_done_screen(pw, made):
    tok = make_case(f"Drafting {uid()}", run=False); made.append(tok)
    prepared = health()["answers"] == "prepared"
    br, page = browser(pw, 1440, 900)
    try:
        calls = {"status": 0, "case": 0}
        def case(route):
            calls["case"] += 1; r = route.fetch(); j = r.json()
            if calls["case"] == 1:
                j["status"] = "running"          # the first open says: still drafting; after it finished the real (ingested) case would be re-read, so serve a ready one
            route.fulfill(json=j)
        def status(route):
            calls["status"] += 1
            if calls["status"] == 1:
                return jbody(route, 200, {"token": tok, "status": "running", "stage": "verify", "stages": STAGES, "progress": {"done": 2, "total": 8, "label": "Step 3 of 8: verify"}, "counts": {}, "error": None})
            jbody(route, 200, {"token": tok, "status": "ready", "stage": "finalize", "stages": STAGES, "progress": {"done": 7, "total": 8, "label": "x"}, "counts": {"entries": 9, "amounts": 4, "flags": 10}, "error": None})
        page.route(f"**/api/cases/{tok}", case); page.route(f"**/api/cases/{tok}/status", status)
        goto(page, C.SERVER, f"/case/{tok}/records")
        lis = page.get_by_test_id("stage-list").locator("li")
        expect(lis).to_have_count(8)
        assert lis.evaluate_all("els => els.map(e => e.className)") == ["done", "done", "now", "", "", "", "", ""]
        txt = lis.all_inner_texts()
        assert txt[0].strip().endswith("Reading the records")
        assert ("Getting the line our team prepared for each record" if prepared else "Writing one line for each record") in txt[1]
        joined = " ".join(txt)
        for jargon in ("verify", "judge", "extract", "LLM", "excerpt", "ingest", "finalize", "stage"):
            assert jargon not in joined, jargon                  # never a raw stage id or label with ids
        assert page.get_by_test_id("step-1").locator(".st-status").inner_text() == "Drafting 3 of 8"
        shot(page, "step1-drafting", 1440)
        expect(page.get_by_test_id("draft-done")).to_be_visible(timeout=10000)      # the next 1 s poll says ready
        assert page.get_by_test_id("step-1").locator(".st-status").inner_text() == "Done"
    finally:
        br.close()


def test_stopped_run_names_the_records_and_asks_before_a_rerun_that_has_answers(pw, made):
    tok = make_case(f"Stopped {uid()}"); made.append(tok)
    br, page = browser(pw, 1440, 900)
    try:
        def case(route):
            j = route.fetch().json(); j["status"] = "failed"
            j["error"] = {"code": "run_partial", "message": "The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry.", "interrupted": True, "records": [2, 7]}
            route.fulfill(json=j)
        page.route(f"**/api/cases/{tok}", case)
        posted = []
        def run(route):
            body = json.loads(route.request.post_data or "{}"); posted.append(body)
            if not body.get("confirm_rerun"):
                return jbody(route, 409, err("needs_confirm", "This case already has decisions."))
            jbody(route, 202, {"token": tok, "status": "running", "stage": "extract", "started_at": "2026-11-02T00:00:00Z"})
        page.route(f"**/api/cases/{tok}/run", run)
        page.route(f"**/api/cases/{tok}/status", lambda r: jbody(r, 200, {"token": tok, "status": "running", "stage": "extract", "stages": STAGES, "progress": {"done": 1, "total": 8, "label": "x"}, "counts": {}, "error": None}))
        goto(page, C.SERVER, f"/case/{tok}/records")
        expect(page.get_by_test_id("page-title")).to_have_text("Drafting stopped")
        expect(page.get_by_test_id("failed-message")).to_contain_text("every decision of yours were kept")      # the server's sentence, as given
        expect(page.get_by_test_id("draft-failed")).to_contain_text("No line was written for records 2 and 7. You can write them yourself in step 2.")
        expect(page.get_by_test_id("draft-failed")).to_contain_text("The items that did finish can be checked now in steps 2 and 3.")
        assert page.get_by_test_id("step-1").locator(".st-status").inner_text() == "Run again"
        assert in_view(page, page.get_by_test_id("btn-run-again")); shot(page, "step1-failed", 1440)
        page.get_by_test_id("btn-run-again").click()
        expect(page.get_by_test_id("bar-msg")).to_have_text("Run it again? Your answers so far are kept.")
        page.get_by_test_id("btn-run-cancel").click(); expect(page.get_by_test_id("bar-msg")).to_have_text("")
        page.get_by_test_id("btn-run-again").click(); page.get_by_test_id("btn-run-yes").click()
        expect(page.get_by_test_id("stage-list")).to_be_visible()
        assert posted == [{"confirm_rerun": False}, {"confirm_rerun": False}, {"confirm_rerun": True}], posted
    finally:
        br.close()


# ------------------------------------------------------------------ errors are plain sentences, with the action, in the bar
@pytest.mark.parametrize("status,payload,sentence,action", [
    (413, err("input_too_large", "Input is too large."), "That's more than we can read at once (60,000 characters or 40 records). Split it into two cases.", None),
    (429, err("busy", "Busy.", {"reason": "pdf_busy"}), "We're reading other files right now. Try again in a moment.", "btn-retry-read"),
    (429, err("busy", "This demo is full right now. Try again later.", {"reason": "demo_full"}), "This demo is full right now. Try again later.", "btn-retry-read"),
    (409, err("demo_mode_unsupported_input", "This demo only runs the recorded sample cases."), "This demo can only read the sample case and our test cases.", "btn-use-sample"),
    (400, err("bad_request", "Input is empty."), "There's nothing to read yet. Paste the records or choose a file.", None),
    (503, err("llm_unavailable", "x"), "We couldn't reach the server. Your text is still here.", "btn-retry-read"),
])
def test_read_errors_are_plain_sentences_with_the_action(pw, status, payload, sentence, action):
    br, page = browser(pw, 1440, 900)
    try:
        go(page, "/new")
        page.route("**/api/cases", lambda r: jbody(r, status, payload) if r.request.method == "POST" else r.continue_())
        bar0 = box(page, "action-bar"); read0 = box(page, "btn-read")
        page.get_by_test_id("btn-read").click()
        msg = page.get_by_test_id("bar-msg"); expect(msg).to_have_text(sentence)
        t = msg.inner_text()
        for raw in (str(status), "input_too_large", "demo_mode", "Failed to fetch", "HTTP"):
            assert raw not in t, raw
        if action:
            expect(page.get_by_test_id(action)).to_be_visible()
        assert box(page, "action-bar") == bar0 and box(page, "btn-read") == read0        # nothing moved: the message has its reserved slot
        expect(page.get_by_test_id("btn-read")).to_be_enabled()
        if action == "btn-use-sample":
            page.get_by_test_id(action).click(); expect(page.get_by_test_id("radio-sample")).to_be_checked(); expect(msg).not_to_have_text(sentence)
    finally:
        br.close()


def test_offline_keeps_the_input_and_try_again_works(pw, made):
    br, page = browser(pw, 1440, 900)
    try:
        go(page, "/new")
        page.route("**/api/cases", lambda r: r.abort() if r.request.method == "POST" else r.continue_())
        page.get_by_test_id("btn-read").click()
        expect(page.get_by_test_id("bar-msg")).to_have_text("We couldn't reach the server. Your text is still here.")
        page.unroute("**/api/cases")
        page.get_by_test_id("btn-retry-read").click()
        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
        made.append(page.url.split("/case/")[1].split("/")[0])
    finally:
        br.close()


def test_a_refused_case_name_shows_under_the_name_box_and_nothing_is_created(pw):
    br, page = browser(pw, 1440, 900)
    try:
        go(page, "/new")
        page.get_by_test_id("input-name").fill("Rivera <b>")
        page.get_by_test_id("btn-read").click()
        expect(page.get_by_test_id("name-error")).to_contain_text("Remove the angle brackets")      # the server's sentence, under the box
        expect(page.get_by_test_id("input-name")).to_be_focused()
        assert "/new" in page.url
        page.get_by_test_id("input-name").fill("Rivera"); expect(page.get_by_test_id("name-error")).to_have_text("")
    finally:
        br.close()


# ------------------------------------------------------------------ live mode: paste and upload
def test_paste_is_disabled_until_there_is_text_then_reads_the_records(pw, live):
    br, page = browser(pw, 1440, 900)
    try:
        goto(page, live, "/new")
        expect(page.get_by_test_id("demo-note")).to_have_count(0)
        for k in ("paste", "file"):
            assert page.get_by_test_id(f"tile-{k}").get_attribute("aria-disabled") is None
        expect(page.get_by_test_id("radio-paste")).to_be_checked()
        read = page.get_by_test_id("btn-read"); expect(read).to_be_disabled()
        page.get_by_test_id("input-text").fill("   \n  "); expect(read).to_be_disabled()       # blank is nothing
        page.get_by_test_id("input-text").fill(C.golden_text("sample.txt")); expect(read).to_be_enabled()
        page.get_by_test_id("input-name").fill("Pasted " + uid())
        read.click(); expect(read).to_have_text("Reading…")
        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=20000)
        expect(page.get_by_test_id("page-title")).to_have_text("We found 9 records")
    finally:
        br.close()


def test_choosing_another_way_never_moves_the_box_or_the_bar(pw, live):
    br, page = browser(pw, 1440, 900)
    try:
        goto(page, live, "/new")
        base = (box(page, "input-box"), box(page, "btn-read"), box(page, "action-bar"))
        for k in ("file", "sample", "library", "paste"):
            if page.get_by_test_id(f"tile-{k}").count() == 0:
                continue
            page.get_by_test_id(f"tile-{k}").click(); page.wait_for_timeout(100)
            assert (box(page, "input-box"), box(page, "btn-read"), box(page, "action-bar")) == base, k
    finally:
        br.close()


def test_too_big_a_paste_is_refused_with_the_real_413_sentence_and_the_text_stays(pw, live):
    br, page = browser(pw, 1440, 900)
    try:
        goto(page, live, "/new")
        big = "=== Record 1 ===\nDate: 2026-01-09\nSource: x\nExcerpt: \"" + ("word " * 14000) + "\"\n"
        page.get_by_test_id("input-text").fill(big)
        page.get_by_test_id("btn-read").click()
        expect(page.get_by_test_id("bar-msg")).to_have_text("That's more than we can read at once (60,000 characters or 40 records). Split it into two cases.")
        assert len(page.get_by_test_id("input-text").input_value()) > 60000          # her text is still there
    finally:
        br.close()


def test_txt_and_pdf_uploads_read_like_paste_and_bad_files_say_why(pw, live, tmp_path):
    from tests.unit._pdf import sample_pdf, make_pdf
    sample = C.golden_text("sample.txt")
    br, page = browser(pw, 1440, 900)
    try:
        goto(page, live, "/new"); page.get_by_test_id("tile-file").click()
        read = page.get_by_test_id("btn-read"); expect(read).to_be_disabled()
        t = tmp_path / "s.txt"; t.write_text(sample)
        page.get_by_test_id("file-input").set_input_files(str(t))
        expect(page.get_by_test_id("file-name")).to_have_text("s.txt"); expect(read).to_be_enabled()
        read.click(); expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=20000)
        expect(page.get_by_test_id("page-title")).to_have_text("We found 9 records")
        # a PDF with a text layer
        goto(page, live, "/new"); page.get_by_test_id("tile-file").click()
        p = tmp_path / "s.pdf"; p.write_bytes(sample_pdf(sample))
        page.get_by_test_id("file-input").set_input_files(str(p)); page.get_by_test_id("btn-read").click()
        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=30000)
        expect(page.get_by_test_id("page-title")).to_have_text("We found 9 records")
        # a scanned PDF: a plain sentence, and the OCR button only when the server can do it
        goto(page, live, "/new"); page.get_by_test_id("tile-file").click()
        sc = tmp_path / "scan.pdf"; sc.write_bytes(make_pdf([["x"]], image_only=True))
        page.get_by_test_id("file-input").set_input_files(str(sc)); page.get_by_test_id("btn-read").click()
        expect(page.get_by_test_id("bar-msg")).to_have_text("This PDF looks scanned, so it has no text we can read.", timeout=30000)
        # a file that is neither: refused in the browser before anything is sent
        goto(page, live, "/new"); page.get_by_test_id("tile-file").click()
        d = tmp_path / "x.docx"; d.write_bytes(b"PK")
        page.get_by_test_id("file-input").set_input_files(str(d))
        expect(page.get_by_test_id("bar-msg")).to_have_text("We can read .txt and .pdf files. Choose another file.")
        expect(page.get_by_test_id("btn-read")).to_be_disabled()
    finally:
        br.close()


def test_phone_layout_of_every_step_1_screen_has_nothing_clipped(pw, live, made):
    tok = make_case(f"Phone {uid()}", run=False); made.append(tok)
    br, page = browser(pw, 390, 844)
    try:
        goto(page, live, "/new")
        for k in ("paste", "file", "sample", "library"):
            if page.get_by_test_id(f"tile-{k}").count():
                page.get_by_test_id(f"tile-{k}").click()
        page.get_by_test_id("tile-paste").click()
        assert in_view(page, page.get_by_test_id("btn-read")) and no_h_scroll(page)
        shot(page, "step1-add-live", 390)
        goto(page, C.SERVER, f"/case/{tok}/records")
        assert in_view(page, page.get_by_test_id("btn-draft")) and no_h_scroll(page); shot(page, "step1-found", 390)
        for sel in ("main h1", "[data-testid=records-list]"):
            b = page.locator(sel).first.bounding_box(); assert b["x"] >= 0 and b["x"] + b["width"] <= 390, sel
    finally:
        br.close()
