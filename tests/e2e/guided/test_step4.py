"""T-181 (D-068) guided UI, Step 4 Get your letter (/case/<token>/letter) and the first-time path from Home to a downloaded letter. Spec section 7. Builder A.
Steps 2 and 3 belong to the other builder: here every item is answered over the API (accept) where the path needs them. Real data everywhere except the blocker-code rows (a trace stub: the fixture
backend cannot produce RERUN_JUDGE or RUN_FAILED blockers on demand). Test ids: letter-status, letter-text, notes-text, btn-copy-letter, btn-download-letter, btn-copy-notes, btn-download-notes,
check-copy-anyway, btn-first-undecided, blockers, blocker (data-code), btn-blocker, blocker-note, btn-rejudge, cfg-exhibit, cfg-bates-prefix, cfg-bates-start, btn-save-cfg, cfg-error, prepared-badge, bar-msg, action-bar."""
import json
import re
import pytest
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided._helpers import api, make_case, decide_all, golden_letter, golden_notes, uid, browser, shot, in_view, no_h_scroll, go, jbody, err
from tests.e2e.guided.test_shell_smoke import watch


@pytest.fixture
def made():
    toks = []
    yield toks
    for t in toks:
        api("DELETE", f"/api/cases/{t}/export_config"); api("DELETE", f"/api/cases/{t}")


def slug(t):
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", t.lower()))


def box(page, tid):
    b = page.get_by_test_id(tid).bounding_box(); return [round(b[k]) for k in ("x", "y", "width", "height")]


def test_first_time_path_from_home_to_a_downloaded_letter(pw, made, tmp_path):
    """Home -> Start a new case -> Read the records -> Draft the timeline -> (steps 2 and 3 answered over the API) -> Get your letter -> Download. Only clicks, no typing but the case name."""
    br, page = browser(pw, 1440, 900)
    try:
        seen = watch(page); go(page, "/")
        page.get_by_test_id("btn-new-case").first.click()
        expect(page).to_have_url(re.compile(r"/new$"))
        name = f"First time {uid()}"; page.get_by_test_id("input-name").fill(name)
        page.get_by_test_id("btn-read").click()
        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
        tok = page.url.split("/case/")[1].split("/")[0]; made.append(tok)
        page.get_by_test_id("btn-draft").click()
        expect(page.get_by_test_id("draft-done")).to_be_visible(timeout=20000)
        page.get_by_test_id("btn-next-step").click()
        expect(page).to_have_url(re.compile(r"/timeline$"))
        decide_all(tok)                                                      # Steps 2 and 3 (another builder's pages): every item answered
        page.get_by_test_id("step-4").click()
        expect(page).to_have_url(re.compile(r"/letter$"))
        expect(page.get_by_test_id("letter-status")).to_contain_text("Your letter is ready. Every item has an answer.")
        expect(page.get_by_test_id("letter-status")).to_contain_text("9 timeline lines and 2 charges are in it.")
        assert in_view(page, page.get_by_test_id("btn-copy-letter")) and in_view(page, page.get_by_test_id("btn-download-letter"))
        with page.expect_download() as d:
            page.get_by_test_id("btn-download-letter").click()
        dl = d.value; assert dl.suggested_filename == f"{slug(name)}-letter.txt", dl.suggested_filename
        path = tmp_path / "letter.txt"; dl.save_as(str(path))
        text = path.read_text()
        assert text == golden_letter()                                       # byte for byte the golden export (evals/golden/sample.export.expected.txt)
        assert "TREATMENT SUMMARY" not in text and "narrative" not in text.lower()          # D-067: no drafted paragraph
        expect(page.get_by_test_id("step-4")).to_have_attribute("data-state", "done")
        assert seen == [], seen
    finally:
        br.close()


def test_letter_ready_copy_and_download_match_the_export_and_nothing_moves(pw, made, tmp_path):
    tok = make_case(f"Letter {uid()}", decide=True); made.append(tok)
    title = api("GET", f"/api/cases/{tok}")[1]["title"]
    ex = api("GET", f"/api/cases/{tok}/export")[1]
    for w, h in ((1440, 900), (1366, 768), (390, 844)):
        br, page = browser(pw, w, h)
        try:
            seen = watch(page); go(page, f"/case/{tok}/letter")
            expect(page.get_by_test_id("page-title")).to_have_text("Get your letter")
            copy = page.get_by_test_id("btn-copy-letter")
            assert in_view(page, copy) and in_view(page, page.get_by_test_id("btn-download-letter")), (w, h)       # the primary actions are on screen without scrolling
            assert page.get_by_test_id("letter-text").inner_text() == ex["letter_text"] and page.get_by_test_id("notes-text").inner_text() == ex["internal_notes_text"]
            expect(page.get_by_test_id("notes-text")).to_contain_text("DO NOT SEND")
            expect(page.locator("main")).to_contain_text("Notes for the attorney"); expect(page.locator("main")).to_contain_text("Do not send")
            assert no_h_scroll(page), (w, h)
            before = (box(page, "action-bar"), box(page, "btn-copy-letter"), box(page, "btn-download-letter"), box(page, "letter-text"))
            copy.click()
            expect(copy).to_have_text("Copied")
            assert page.evaluate("navigator.clipboard.readText()") == ex["letter_text"]
            assert (box(page, "action-bar"), box(page, "btn-copy-letter"), box(page, "btn-download-letter"), box(page, "letter-text")) == before      # a label change moves nothing
            expect(copy).to_have_text("Copy letter", timeout=5000)
            page.get_by_test_id("btn-copy-notes").click(); assert page.evaluate("navigator.clipboard.readText()") == ex["internal_notes_text"]
            with page.expect_download() as d:
                page.get_by_test_id("btn-download-notes").click()
            assert d.value.suggested_filename == f"{slug(title)}-notes.txt"
            p = tmp_path / f"n{w}.txt"; d.value.save_as(str(p)); assert p.read_text() == golden_notes()
            assert seen == [], seen
            shot(page, "step4-letter", w) if h in (900, 844) else None
        finally:
            br.close()


def test_the_letter_blanks_sentence_and_the_exhibit_numbers(pw, made):
    tok = make_case(f"Exhibit {uid()}", decide=True); made.append(tok)
    br, page = browser(pw, 1440, 900)
    try:
        go(page, f"/case/{tok}/letter")
        expect(page.get_by_test_id("bar-msg")).to_contain_text("The [Ex. __ / Bates __] blanks and each “date of service [____]” blank are yours to fill in.")
        page.get_by_test_id("cfg-exhibit").fill("4$$"); page.get_by_test_id("btn-save-cfg").click()
        expect(page.get_by_test_id("cfg-error")).to_contain_text("Exhibit and prefix:")             # the server's sentence, under the inputs
        assert api("GET", f"/api/cases/{tok}/export_config")[1]["exhibit"] is None
        page.get_by_test_id("cfg-exhibit").fill("4"); page.get_by_test_id("cfg-bates-prefix").fill("RIV"); page.get_by_test_id("cfg-bates-start").fill("1")
        page.get_by_test_id("btn-save-cfg").click()
        expect(page.get_by_test_id("bar-msg")).to_have_text("Saved. The numbers are in your letter.")
        assert "[Ex. 4 / Bates RIV0001]" in page.get_by_test_id("letter-text").inner_text()
        page.get_by_test_id("cfg-bates-start").fill("x"); page.get_by_test_id("btn-save-cfg").click()
        expect(page.get_by_test_id("cfg-error")).to_have_text("The first number must be a whole number, like 1.")
        page.reload(); page.locator("[data-testid=view][data-ready]").wait_for(state="attached")
        assert page.get_by_test_id("cfg-exhibit").input_value() == "4"                                 # remembered
    finally:
        br.close()


def test_blocked_letter_lists_each_problem_with_the_step_that_fixes_it(pw, made):
    tok = make_case(f"Blocked {uid()}"); made.append(tok)           # drafted, nothing answered: NOTHING_ACCEPTED
    br, page = browser(pw, 1440, 900)
    try:
        seen = watch(page); go(page, f"/case/{tok}/letter")           # no refused request: the trace says blocked, the export is not asked for
        expect(page.get_by_test_id("letter-status")).to_contain_text("The letter can't be made yet.")
        rows = page.get_by_test_id("blocker"); expect(rows).to_have_count(1)
        assert rows.first.get_attribute("data-code") == "DECIDE"
        expect(rows.first).to_contain_text("Nothing is accepted or edited yet, so the letter would be empty.")      # the server's sentence, as given
        b = page.get_by_test_id("btn-blocker"); expect(b).to_have_text("Go to step 2"); assert b.get_attribute("href") == f"/case/{tok}/timeline"
        expect(page.get_by_test_id("letter-text")).to_have_text("Your letter will appear here once the problem above is fixed.")
        expect(page.get_by_test_id("btn-copy-letter")).to_be_disabled(); expect(page.get_by_test_id("btn-download-letter")).to_be_disabled()
        assert page.get_by_test_id("step-4").locator(".st-status").inner_text() == "1 problem"
        assert in_view(page, page.get_by_test_id("btn-copy-letter"))
        shot(page, "step4-blocked", 1440)
        assert seen == [], seen
        page.set_viewport_size({"width": 390, "height": 844}); assert no_h_scroll(page); shot(page, "step4-blocked", 390)
        b.click(); expect(page).to_have_url(re.compile(r"/timeline$"))
    finally:
        br.close()


def test_every_blocker_code_gets_its_own_button_or_sentence(pw, made):
    tok = make_case(f"Codes {uid()}", decide=True); made.append(tok)
    na = lambda code, **t: {"code": code, "text": "x", "target": t}
    blockers = [
        {"item_id": "e3", "kind": "entry", "reason_code": "SUMMARY_NUMBER_NOT_IN_EXCERPT", "why": "The summary says 8 but the quote says 6.", "next_action": na("EDIT_SUMMARY", item_id="e3")},
        {"item_id": "e4", "kind": "entry", "reason_code": "EXCERPT_NOT_VERBATIM", "why": "The quote is not in the record.", "next_action": na("EDIT_QUOTE", item_id="e4")},
        {"item_id": "a2", "kind": "amount", "reason_code": "X", "why": "This amount needs a look.", "next_action": na("DISMISS_OR_ENTER_BY_HAND", item_id="a2")},
        {"item_id": "e5", "kind": "entry", "reason_code": "JUDGE_NOT_RUN", "why": "This accepted line has no second check.", "next_action": na("RERUN_JUDGE", item_id="e5", judge="j1")},
        {"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": "The last run stopped.", "next_action": na("CONFIRM_RERUN")},
        {"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": "A run is going.", "next_action": na("RUN_IN_PROGRESS")},
    ]
    gate = {"id": "export_gate", "ready": False, "blockers": blockers}
    br, page = browser(pw, 1440, 900)
    try:
        page.route(f"**/api/cases/{tok}/trace", lambda r: jbody(r, 200, {"token": tok, "status": "ready", "steps": [gate]}))
        go(page, f"/case/{tok}/letter")
        rows = page.get_by_test_id("blocker"); expect(rows).to_have_count(6)
        act = lambda i: rows.nth(i)
        assert act(0).locator("a").get_attribute("href") == f"/case/{tok}/timeline?item=e3" and act(0).locator("a").inner_text() == "Fix it"
        assert act(1).locator("a").get_attribute("href") == f"/case/{tok}/timeline?item=e4" and act(1).locator("a").inner_text() == "Fix it"
        assert act(2).locator("a").get_attribute("href") == f"/case/{tok}/bills?item=a2" and act(2).locator("a").inner_text() == "Go to it"
        expect(act(3).get_by_test_id("blocker-note")).to_have_text("The second check can't run here. Fix the wording in your own words, or leave the item out.")    # rerun_available is false in demo mode
        assert act(4).locator("a").get_attribute("href") == f"/case/{tok}/records" and act(4).locator("a").inner_text() == "Go to step 1"
        expect(act(5).get_by_test_id("blocker-note")).to_have_text("Wait for drafting to finish.")
        assert page.get_by_test_id("step-4").locator(".st-status").inner_text() == "6 problems"
    finally:
        br.close()


def test_rerun_the_second_check_when_the_item_can_be_rerun(pw, made):
    tok = make_case(f"Rejudge {uid()}", decide=True); made.append(tok)
    blockers = [{"item_id": "e5", "kind": "entry", "reason_code": "JUDGE_NOT_RUN", "why": "This accepted line has no second check.", "next_action": {"code": "RERUN_JUDGE", "text": "x", "target": {"item_id": "e5", "judge": "j1"}}}]
    state = {"posted": 0}
    br, page = browser(pw, 1440, 900)
    try:
        def trace(route):
            if state["posted"]:
                return route.continue_()
            jbody(route, 200, {"token": tok, "status": "ready", "steps": [{"id": "export_gate", "ready": False, "blockers": blockers}]})
        def case(route):
            j = route.fetch().json()
            for i in j["entries"]:
                if i["id"] == "e5":
                    i["rerun_available"] = True
            route.fulfill(json=j)
        def rejudge(route):
            state["posted"] += 1; jbody(route, 200, {"token": tok, "asked": 1, "rejudged": [], "still_unavailable": [], "export_gate": {"ready": True, "blockers": []}})
        page.route(f"**/api/cases/{tok}/trace", trace); page.route(f"**/api/cases/{tok}", case); page.route(f"**/api/cases/{tok}/rejudge", rejudge)
        go(page, f"/case/{tok}/letter")
        b = page.get_by_test_id("btn-rejudge"); expect(b).to_have_text("Run the second check again"); b.click()
        expect(page.get_by_test_id("letter-status")).to_contain_text("Your letter is ready.")      # the gate is re-read after the check
        assert state["posted"] == 1
    finally:
        br.close()


def test_undecided_items_need_one_tick_before_copying_and_the_link_goes_to_the_first(pw, made):
    tok = make_case(f"Pending {uid()}"); made.append(tok)
    c = api("GET", f"/api/cases/{tok}")[1]
    st, r = api("POST", f"/api/cases/{tok}/review/batch", {"action": "accept", "item_ids": [e["id"] for e in c["entries"]]}); assert st == 200, r
    left = api("GET", f"/api/cases/{tok}")[1]["review"]["counts"]; n = left["pending"] + left["edit_to_check"]
    br, page = browser(pw, 1440, 900)
    try:
        seen = watch(page); go(page, f"/case/{tok}/letter")
        s = page.get_by_test_id("letter-status")
        expect(s).to_contain_text(f"{n} items still need a decision.")
        expect(s).to_contain_text("If you don't decide them, they stay out of the letter.")
        first = page.get_by_test_id("btn-first-undecided"); expect(first).to_have_text("Go to the first one")
        assert first.get_attribute("href") == f"/case/{tok}/timeline"        # steps are in order: the first undecided item is in step 2
        copy, dl = page.get_by_test_id("btn-copy-letter"), page.get_by_test_id("btn-download-letter")
        expect(copy).to_be_disabled(); expect(dl).to_be_disabled()
        expect(page.get_by_test_id("bar-msg")).to_contain_text("Tick the box above")
        assert page.get_by_test_id("letter-text").inner_text().startswith("TREATMENT CHRONOLOGY")          # the preview is what would be sent now
        tick = page.get_by_test_id("check-copy-anyway"); tick.check()
        expect(copy).to_be_enabled(); expect(dl).to_be_enabled()
        copy.click(); expect(copy).to_have_text("Copied")
        assert page.evaluate("navigator.clipboard.readText()") == api("GET", f"/api/cases/{tok}/export")[1]["letter_text"]
        tick.uncheck(); expect(copy).to_be_disabled()
        assert page.get_by_test_id("step-4").locator(".st-status").inner_text() == "Not yet"
        assert seen == [], seen
        shot(page, "step4-pending", 1440)
    finally:
        br.close()


def test_provenance_badge_and_no_narrative_anywhere(pw, made):
    tok = make_case(f"Prov {uid()}", decide=True); made.append(tok)
    hl = api("GET", "/api/health")[1]
    br, page = browser(pw, 1440, 900)
    try:
        asked = []
        page.on("request", lambda r: asked.append(r.url) if "/narrative" in r.url else None)
        go(page, f"/case/{tok}/letter")
        text = page.locator("main").inner_text()
        assert "TREATMENT SUMMARY" not in text and "treatment paragraph" not in text.lower() and asked == []
        if hl["answers"] == "prepared":
            b = page.get_by_test_id("prepared-badge")
            assert b.get_attribute("title") == "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."
            expect(page.locator("main")).to_contain_text("Prepared by our team for this demo, not written by an AI model.")
        else:
            expect(page.get_by_test_id("prepared-badge")).to_have_count(0)
        for jargon in ("tray", "judge", "LLM", "excerpt", "export gate"):
            assert jargon not in text.split("DO NOT SEND")[0].split("TREATMENT CHRONOLOGY")[0], jargon      # the page chrome around the two text boxes is plain words
    finally:
        br.close()


def test_a_failed_load_says_so_in_a_sentence_and_try_again_works(pw, made):
    tok = make_case(f"Offline {uid()}", decide=True); made.append(tok)
    br, page = browser(pw, 1440, 900)
    try:
        page.route(f"**/api/cases/{tok}/trace", lambda r: r.abort())
        page.route(f"**/api/cases/{tok}/export", lambda r: r.abort())
        go(page, f"/case/{tok}/letter")
        e = page.get_by_test_id("page-error"); expect(e).to_contain_text("We couldn't make the letter")
        assert "Failed to fetch" not in e.inner_text()
        page.unroute(f"**/api/cases/{tok}/trace"); page.unroute(f"**/api/cases/{tok}/export")
        page.get_by_test_id("btn-retry").click()
        expect(page.get_by_test_id("letter-status")).to_contain_text("Your letter is ready.")
    finally:
        br.close()
