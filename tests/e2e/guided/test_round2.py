"""T-181 round 2 (D-068): the paralegal and UX-designer findings of round 1, each with its own guard.
Real browser, the fixture backend (curated set), the real API. Cases are made over the API and deleted afterwards.
What is guarded: the borrowed-sentence label and the underlined words (paralegal major 1); the Bates rule and its preview (paralegal major 2); no failed request on first paint, in a local and in a
PUBLIC server (T-182 r3); a refused edit names the dropped words (UX major 3); the step list closes when its toggle is tapped again (UX major 4); a disputed line and its tick box are on screen together
at 390 (UX major 2); Step 3's done lists fit a phone (UX major 1); no sideways scrolling on any guided screen at 390 and 320; a refused Yes never moves focus onto a button that answers; the second
check's direction on an amount; ledger lines with no date of service; the title-row provenance follows the case; every highlight of a multi-record warning is in view at 1440x900."""
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

import pytest
from playwright.sync_api import expect

import tests.e2e.conftest as C
from tests.e2e.guided._helpers import decide_all
from tests.e2e.guided.test_shell_smoke import go, watch
from tests.e2e.guided.test_step2 import LIB10, item, make, open_item, case   # noqa: F401  (make is a fixture)

LIB11 = "case_lib11_priors_and_ledger"


def no_h_scroll(page):
    return page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1")


def phone(pw, w=390, h=844):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=True, has_touch=True)
    return b, ctx.new_page()


def desktop(pw, w=1440, h=900):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, permissions=["clipboard-read", "clipboard-write"], accept_downloads=True)
    return b, ctx.new_page()


# ------------------------------------------------------------------------------------ paralegal major 1: the borrowed sentence

def test_the_grey_box_does_not_say_a_borrowed_sentence_is_in_no_line_and_the_outside_words_are_underlined(pw, make):
    tok = make(LIB11); b, page = desktop(pw)
    try:
        for iid, words in (("e1", {"Annual", "visit"}), ("e2", {"struck", "behind"})):
            open_item(page, tok, iid)
            box = page.get_by_test_id("uncovered")
            expect(box).to_contain_text("outside the highlighted words")
            assert "not in any line" not in box.inner_text()
            out = set(page.get_by_test_id("outside-word").all_inner_texts())
            assert words <= out, (iid, out)
            expect(page.get_by_test_id("outside-note")).to_contain_text("Underlined words are not in the highlighted words")
        # an item that is not disputed carries no underline
        open_item(page, tok, "e3")
        assert page.get_by_test_id("outside-word").count() == 0
    finally:
        b.close()


# ------------------------------------------------------------------------------------ paralegal major 2: Bates

def test_the_bates_panel_says_one_number_per_record_and_previews_before_save(pw, make):
    tok = make(); decide_all(tok); b, page = desktop(pw)
    try:
        go(page, f"/case/{tok}/letter")
        rule = page.get_by_test_id("cfg-rule").inner_text()
        assert "One Bates number per record" in rule and "not per page" in rule and "9 records" in rule, rule
        expect(page.get_by_test_id("cfg-panel")).to_contain_text("fill in the page numbers in Word")
        expect(page.get_by_test_id("cfg-preview")).to_contain_text("Nothing filled in")
        page.get_by_test_id("cfg-exhibit").fill("3"); page.get_by_test_id("cfg-bates-prefix").fill("RIVERA"); page.get_by_test_id("cfg-bates-start").fill("1")
        pv = page.get_by_test_id("cfg-preview")
        expect(pv).to_contain_text("record 1 reads [Ex. 3 / Bates RIVERA0001]")
        expect(pv).to_contain_text("record 9 reads [Ex. 3 / Bates RIVERA0009]")
        assert C.api("GET", f"/api/cases/{tok}/export_config")[1]["bates_prefix"] is None, "a preview saves nothing"
        page.get_by_test_id("cfg-bates-start").fill("100")
        expect(pv).to_contain_text("record 9 reads [Ex. 3 / Bates RIVERA0108]")
    finally:
        b.close()


# ------------------------------------------------------------------------------------ T-182 r3: no failed request on first paint

def test_no_failed_request_on_first_paint_in_a_local_server(pw):
    b, page = desktop(pw)
    try:
        seen = watch(page)
        for path in ("/", "/new"):
            go(page, path); page.wait_for_timeout(300)
        assert seen == [], seen
    finally:
        b.close()


@pytest.fixture(scope="module")
def public_server():
    """A second private server in PUBLIC mode (ZLAYT_MODE unset): GET /api/cases and /api/library answer 404 there by design."""
    s = __import__("socket").socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    tmp = tempfile.mkdtemp(prefix="zlayt-e2e-public-")
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "p.sqlite3"))
    env.pop("ANTHROPIC_API_KEY", None); env.pop("ZLAYT_MODE", None)
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=C.ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
            except Exception:
                if proc.poll() is not None:
                    pytest.fail("the public test server exited: " + open(os.path.join(tmp, "server.log")).read()[-1500:])
                time.sleep(0.5)
        else:
            pytest.fail("the public test server did not answer /api/health")
        yield base
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
        log.close()


def test_no_failed_request_on_first_paint_in_a_public_server(pw, public_server):
    """Home and /new in public mode: no 404 on /api/cases or /api/library. Needs `local_mode` in GET /api/health (T-197): without it the page cannot know."""
    health = __import__("json").loads(urllib.request.urlopen(public_server + "/api/health").read())
    b, page = desktop(pw)
    try:
        seen = watch(page)
        for path in ("/", "/new"):
            page.goto(public_server + path); page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=15000); page.wait_for_timeout(300)
        assert health.get("local_mode") is False, health          # T-197: health says whether the list of cases and the library exist
        assert seen == [], seen
        page.goto(public_server + "/new"); page.locator("[data-testid=view][data-ready]").wait_for(state="attached")
        assert "test cases" not in page.get_by_test_id("demo-note").inner_text()      # nothing in a public demo offers the test cases
    finally:
        b.close()


def test_when_health_says_local_mode_is_false_the_page_never_asks_for_the_list_or_the_library(pw, public_server):
    """The frontend half of the 404 fix, proven now: the public server's health gets `local_mode: false` injected (what backend adds), and / and /new make no request that fails."""
    import json as _json
    b, page = desktop(pw)
    try:
        def health(route):
            r = route.fetch(); body = r.json(); body["local_mode"] = False
            route.fulfill(response=r, body=_json.dumps(body))
        page.route("**/api/health", health)
        seen = watch(page); asked = []
        page.on("request", lambda r: asked.append(r.url) if re.search(r"/api/(cases|library)$", r.url) and r.method == "GET" else None)
        for path in ("/", "/new"):
            page.goto(public_server + path); page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=15000); page.wait_for_timeout(300)
        assert seen == [] and asked == [], (seen, asked)
        assert "test cases" not in page.get_by_test_id("demo-note").inner_text()
    finally:
        b.close()


# ------------------------------------------------------------------------------------ UX major 3: the refusal names the words

def test_a_refused_edit_names_the_words_she_dropped_in_plain_grammar(pw, make):
    tok = make(); e1 = item(tok, "e1"); b, page = desktop(pw)
    try:
        open_item(page, tok, "e1")
        page.get_by_test_id("btn-third").click()
        ta = page.get_by_test_id("edit-summary"); ta.fill(e1["summary"].replace("complained of ", ""))
        page.get_by_test_id("answer-yes").click()
        foot = page.get_by_test_id("card-foot"); expect(foot).to_contain_text("Not saved.")
        t = foot.inner_text()
        assert "complained of" in t and "leaves out" in t and "whose account" in t, t
        assert not re.search(r"highlighted words (carries|gives)", t), t
        assert item(tok, "e1")["summary"] == e1["summary"], "nothing was saved"
    finally:
        b.close()


def test_plain_words_for_every_qualifier_sentence_the_server_has(pw):
    """The server's sentence for each kind reads in the plain vocabulary with the verb agreeing; the page script is run in a browser."""
    br = pw.chromium.launch()
    try:
        pg = br.new_page(); pg.goto(C.SERVER + "/"); pg.locator("[data-testid=view][data-ready]").wait_for(state="attached")
        for what in ("a hedge (such as may, possible or appears)", "a phrase that says whose account the quote gives", "a negation (such as no, not or denies)", "a side (left or right)", "an approximation (such as approximately)"):
            out = pg.evaluate("(w) => G.review.plain(`The quote carries ${w} that the summary leaves out. Put it back in the summary.`)", what)
            assert not re.search(r"highlighted words (carries|gives)", out) and "Your line leaves out" in out, out
        out = pg.evaluate("() => G.review.droppedText(['hedge','laterality'], 'may be on the left arm', 'arm pain', 'possible pain on the left arm')")
        assert "“possible”" in out and "“left”" in out and "those words" in out, out
    finally:
        br.close()


# ------------------------------------------------------------------------------------ UX major 4: the step list closes

@pytest.mark.parametrize("w", [390, 360])
def test_tapping_the_step_toggle_again_closes_the_list_and_stays_on_the_page(pw, make, w):
    tok = make(); b, page = phone(pw, w)
    try:
        open_item(page, tok, "e3"); url = page.url; h1 = page.get_by_test_id("page-title").inner_text()
        btn = page.get_by_test_id("btn-steps")
        btn.click(); expect(btn).to_have_attribute("aria-expanded", "true")
        expect(page.get_by_test_id("step-1")).to_be_visible()
        btn.click(); expect(btn).to_have_attribute("aria-expanded", "false")
        assert page.url == url and page.get_by_test_id("page-title").inner_text() == h1
    finally:
        b.close()


# ------------------------------------------------------------------------------------ UX major 2: line and tick box together at 390

def test_a_disputed_line_and_its_tick_box_are_on_screen_together_at_390(pw, make):
    tok = make(LIB10); b, page = phone(pw)
    try:
        open_item(page, tok, "e1")
        assert page.get_by_test_id("check-compare").count() == 1
        r = page.evaluate("""() => {
          const q = (s) => document.querySelector('[data-testid=' + s + ']').getBoundingClientRect(), card = q('card-line'), head = q('line-head'), line = q('line-text'), chk = q('check-compare');
          return { card: [card.top, card.bottom], head: head.bottom, line: [line.top, line.bottom], chk: [chk.top, chk.bottom], vh: innerHeight, scrolled: document.querySelector('[data-testid=card-line]').scrollTop };
        }""")
        assert r["scrolled"] == 0, r
        assert r["line"][0] >= r["head"] - 1 and r["line"][1] <= r["card"][1], r       # the line is under the header, not behind it
        assert r["chk"][1] <= r["card"][1] + 1 and r["chk"][1] <= r["vh"], r         # the tick box is inside the card and in the viewport, with no scrolling
    finally:
        b.close()


def test_an_edited_line_and_its_tick_box_are_on_screen_together_at_390(pw, make):
    tok = make(); e1 = item(tok, "e1"); b, page = phone(pw)
    try:
        open_item(page, tok, "e1")
        page.get_by_test_id("btn-third").click()
        page.get_by_test_id("edit-summary").fill(e1["summary"].replace("alert and oriented; ", ""))
        page.get_by_test_id("answer-yes").click()
        expect(page.get_by_test_id("check-compare")).to_be_visible()
        r = page.evaluate("""() => { const q = (s) => document.querySelector('[data-testid=' + s + ']').getBoundingClientRect(), card = q('card-line'), line = q('line-text'), chk = q('check-compare');
          return { card: [card.top, card.bottom], line: [line.top, line.bottom], chk: [chk.top, chk.bottom], vh: innerHeight }; }""")
        assert r["line"][0] >= r["card"][0] and r["chk"][1] <= r["card"][1] + 1 and r["chk"][1] <= r["vh"], r
    finally:
        b.close()


# ------------------------------------------------------------------------------------ UX major 1: Step 3 done at a phone width

@pytest.mark.parametrize("w,h", [(390, 844), (320, 640)])
def test_step3_done_fits_a_phone_and_every_change_button_is_on_screen(pw, make, w, h):
    tok = make(); decide_all(tok); b, page = phone(pw, w, h)
    try:
        go(page, f"/case/{tok}/bills")
        expect(page.get_by_test_id("done-heading")).to_be_visible()
        assert no_h_scroll(page), page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        btns = page.get_by_test_id("btn-change")
        assert btns.count() >= 4
        for i in range(btns.count()):
            r = btns.nth(i).bounding_box(); assert r["x"] >= 0 and r["x"] + r["width"] <= w + 1, (i, r)
        tds = page.locator("[data-testid=list-never] td:not(.amt)")
        for i in range(tds.count()):
            assert tds.nth(i).is_visible(), i                                    # no column is hidden on a phone
    finally:
        b.close()


# ------------------------------------------------------------------------------------ no sideways scroll anywhere

@pytest.mark.parametrize("w,h", [(390, 844), (320, 640)])
def test_no_guided_screen_scrolls_sideways_on_a_phone(pw, make, w, h):
    tok = make(); tok_l = make(LIB11); b, page = phone(pw, w, h)
    try:
        seen = watch(page)
        shots = [("/", None), ("/new", None), (f"/case/{tok}/records", None), (f"/case/{tok}/timeline?item=e1", None), (f"/case/{tok}/timeline?item=f_accident_date_after_treatment_1_2_7", None),
                 (f"/case/{tok}/bills", None), (f"/case/{tok}/letter", None), (f"/case/{tok_l}/timeline?item=e1", None), (f"/case/{tok_l}/timeline?item=e9", None),
                 (f"/case/{tok_l}/bills?item=a2", None), ("/case/not-a-case/timeline", None), ("/nowhere", None)]
        for path, _ in shots:
            go(page, path); page.wait_for_timeout(200)
            assert no_h_scroll(page), (w, path, page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]"))
        # fix mode, the note box and the picker
        open_item(page, tok, "e1"); page.get_by_test_id("btn-third").click(); assert no_h_scroll(page), (w, "fix")
        decide_all(tok)
        for path in (f"/case/{tok}/timeline", f"/case/{tok}/bills", f"/case/{tok}/letter", "/"):
            go(page, path); page.wait_for_timeout(300)
            assert no_h_scroll(page), (w, path, "decided", page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]"))
        assert [s for s in seen if "404" not in s and "not-a-case" not in s and "nowhere" not in s] == [], seen
    finally:
        b.close()


# ------------------------------------------------------------------------------------ keyboard: a refused Yes never lands focus on No

def test_a_refused_yes_keeps_focus_off_the_answer_buttons_and_sends_nothing(pw, make):
    tok = make(LIB11); b, page = desktop(pw)
    try:
        posts = []
        page.on("request", lambda r: posts.append(r.url) if r.method == "POST" and "/review" in r.url else None)
        open_item(page, tok, "e9")
        expect(page.get_by_test_id("answer-yes")).to_be_disabled()
        assert page.evaluate("document.activeElement.getAttribute('data-testid')") not in ("answer-no", "answer-yes", "btn-third"), "focus is on the reason, not on a button that answers"
        page.keyboard.press("a")
        expect(page.get_by_test_id("status-text")).to_contain_text("is not available here")
        assert page.evaluate("document.activeElement.getAttribute('data-testid')") != "answer-no"
        page.keyboard.press("Space"); page.keyboard.press("Enter"); page.wait_for_timeout(300)
        assert posts == [], posts
        assert item(tok, "e9")["review_status"] == "pending"
    finally:
        b.close()


def test_the_ledger_line_reason_points_to_step_3_and_reads_in_plain_words(pw, make):
    tok = make(LIB11); b, page = desktop(pw)
    try:
        open_item(page, tok, "e9")
        t = page.get_by_test_id("refusal").inner_text()
        assert "none of them is in Billed charges" not in t and "step 3" in t and "a highlighted words" not in t, t
    finally:
        b.close()


# ------------------------------------------------------------------------------------ Step 3 words

def test_an_amount_the_second_check_disputed_says_which_way_it_disagreed(pw, make):
    tok = make(LIB11); b, page = desktop(pw)
    try:
        go(page, f"/case/{tok}/bills?item=a2"); page.get_by_test_id("card-line").wait_for()
        t = page.get_by_test_id("compare-reason").inner_text()
        assert "charge" in t and "disagreed with the first result" not in t, t
    finally:
        b.close()


def test_a_counted_ledger_line_with_no_date_of_service_shows_the_statement_date(pw, make):
    tok = make(LIB11); b, page = desktop(pw)
    try:
        decide_all(tok, "dismiss")                                               # every item answered, so the done screen opens
        r = C.api("POST", f"/api/cases/{tok}/items/a2/review", {"action": "count", "confirm": "separate_charge"}); assert r[0] == 200, r
        go(page, f"/case/{tok}/bills")
        counted = page.get_by_test_id("list-counted").inner_text()
        assert "date of service [__________] (record dated June 15, 2026)" in counted and "Date of service" in counted, counted      # T-205: the letter's own date text (service_date.text)
    finally:
        b.close()


# ------------------------------------------------------------------------------------ provenance follows the case

def test_the_title_row_does_not_say_not_written_by_an_ai_while_a_tag_says_ai_draft(pw, make):
    tok = make(LIB11); b, page = desktop(pw)
    try:
        open_item(page, tok, "e1")
        assert page.get_by_test_id("line-tag").inner_text() == "AI draft"
        assert "not written by an AI model" not in page.get_by_test_id("ai-note").inner_text()
        assert "not written by an AI model" not in page.get_by_test_id("footer-note").inner_text()
        assert "prepared by our team" not in page.get_by_test_id("demo-badge").inner_text().lower()
    finally:
        b.close()


# ------------------------------------------------------------------------------------ minors

def test_pressing_e_clears_the_previous_saved_message_and_its_undo(pw, make):
    tok = make(); b, page = desktop(pw)
    try:
        open_item(page, tok, "e1"); page.get_by_test_id("answer-yes").click()
        expect(page.get_by_test_id("btn-undo")).to_be_visible()
        page.get_by_test_id("btn-third").click()
        expect(page.get_by_test_id("btn-undo")).to_be_hidden()
    finally:
        b.close()


def test_every_highlight_of_a_multi_record_warning_is_in_view_at_1440(pw, make):
    tok = make(); b, page = desktop(pw)
    try:
        open_item(page, tok, "f_accident_date_after_treatment_1_2_7")
        pane = page.get_by_test_id("card-source").bounding_box()
        marks = page.locator("[data-testid=card-source] mark")
        assert marks.count() == 3
        for i in range(3):
            m = marks.nth(i).bounding_box()
            assert m["y"] >= pane["y"] - 1 and m["y"] + m["height"] <= pane["y"] + pane["height"] + 1, (i, m, pane)
        page.get_by_test_id("btn-whole-record").first.click()                              # the whole record is one click away
        assert page.locator("[data-testid=card-source] [data-testid=record-text]").first.inner_text().startswith("=== Record 1")
    finally:
        b.close()


def test_step_3_keys_hint_does_not_offer_a_key_for_an_action_that_is_not_there(pw, make):
    tok = make(); b, page = desktop(pw)
    try:
        go(page, f"/case/{tok}/bills"); page.get_by_test_id("card-line").wait_for()
        assert "E fixes" not in page.get_by_test_id("status-text").inner_text()
        open_item(page, tok, "e1")
        assert "E fixes" in page.get_by_test_id("status-text").inner_text()
    finally:
        b.close()
