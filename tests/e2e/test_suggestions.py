"""T-096: suggestions and confidence. Date-convention suggestion pre-selected (T-088), dismissal-pattern banner (T-089), measured precision line (T-099),
possible-overlap warning (T-110), could-not-verify wording for flags and the sentences_reason line (T-094/T-108). Real backend where the fixtures give the state
(case_01, lib06, lib09, lib01); route stubs where the state depends on this machine's history (dismissal counts) or on a missing file (calibration)."""
import json, re, time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE, SAMPLE_PATH, tray_entry_for_record

LIB = SAMPLE_PATH + "/../library/"

def make_case(text):
    st, c = api("POST", "/api/cases", {"text": text}); assert st in (200, 201), c
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"): break
        time.sleep(1)
    assert s["status"] == "ready", s
    return tok

@pytest.fixture
def cases():
    made = []
    def mk(text):
        tok = make_case(text); made.append(tok); return tok
    yield mk
    for t in made: api("DELETE", f"/api/cases/{t}")

def lib(name): return open(LIB + name).read()

def rewrite_case(page, fn):
    """Rewrite GET /api/cases/<token> (the case JSON) with fn(body)."""
    def h(route):
        if route.request.method != "GET": return route.continue_()
        r = route.fetch(); body = r.json(); fn(body); route.fulfill(response=r, json=body)
    page.route(re.compile(r"/api/cases/[^/?]+$"), h)

# ---- 1. date-convention suggestion (T-088) --------------------------------------------------------------------------------------

def test_suggested_date_is_preselected_with_reason_and_still_needs_a_confirm(page, cases):
    """The suggested reading is checked, its reason is shown, and nothing is confirmed until the Confirm click."""
    tok = cases(golden_text("case_01_date_formats.txt")); open_case(page, tok)
    box = page.get_by_test_id("dates-to-confirm")
    expect(box.locator('[data-testid="confirm-date"][data-date="2026-04-05"]')).to_be_checked()
    expect(box.locator('[data-testid="confirm-date"][data-date="2026-05-04"]')).not_to_be_checked()
    expect(box.get_by_test_id("date-suggested-tag")).to_have_text(re.compile("Suggested"))
    expect(box.get_by_test_id("date-suggestion-reason")).to_contain_text("month first")
    expect(box.get_by_test_id("btn-confirm-date")).to_be_enabled()
    # nothing was confirmed on load: the undated entry is still here and cannot be accepted
    expect(box.locator('[data-testid^="entry-"][data-item-id]').first.get_by_test_id("btn-accept")).to_be_disabled()
    assert api("GET", f"/api/cases/{tok}")[1]["dates_to_confirm"], "the date must still be waiting for the paralegal"
    box.get_by_test_id("btn-confirm-date").click()
    expect(box).to_contain_text("None. Every record has a readable date.")
    expect(page.get_by_test_id("queue").locator('[data-testid=entry-date][datetime="2026-04-05"]')).to_have_count(1)

def test_the_other_reading_can_be_picked_with_the_keyboard(page, cases):
    tok = cases(golden_text("case_01_date_formats.txt")); open_case(page, tok)
    box = page.get_by_test_id("dates-to-confirm")
    box.locator('[data-testid="confirm-date"][data-date="2026-04-05"]').focus()
    page.keyboard.press("ArrowDown")                       # native radio group: moves the choice
    expect(box.locator('[data-testid="confirm-date"][data-date="2026-05-04"]')).to_be_checked()
    box.get_by_test_id("btn-confirm-date").focus(); page.keyboard.press("Enter")
    expect(page.get_by_test_id("queue").locator('[data-testid=entry-date][datetime="2026-05-04"]')).to_have_count(1)

def test_flags_panel_date_form_also_preselects(page, cases):
    tok = cases(golden_text("case_01_date_formats.txt")); open_case(page, tok)
    f = page.get_by_test_id("flags-panel").locator('[data-category="date_ambiguous"]')
    expect(f.locator('[data-testid="confirm-date"][data-date="2026-04-05"]')).to_be_checked()
    expect(f.get_by_test_id("date-suggestion-reason")).to_contain_text("month first")
    f.get_by_test_id("btn-confirm-date").click()
    expect(page.get_by_test_id("dates-to-confirm")).to_contain_text("None. Every record has a readable date.")

def test_date_form_fits_390_px(page, cases):
    tok = cases(golden_text("case_01_date_formats.txt")); page.set_viewport_size({"width": 390, "height": 844}); open_case(page, tok)
    form = page.get_by_test_id("dates-to-confirm").locator("form.sg-dateform")
    expect(form).to_be_visible()
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), "no sideways scroll at 390 px"
    box = form.get_by_test_id("btn-confirm-date").bounding_box(); assert box["height"] >= 40

def test_without_a_usable_suggestion_nothing_is_preselected(page, cases):
    """suggestion null: the old one-click buttons. suggestion with iso null: reason shown as a hint, still no pre-selection (buttons)."""
    tok = cases(golden_text("case_01_date_formats.txt"))
    def strip(b):
        for d in b["dates_to_confirm"]: d["suggestion"] = {"convention": "MDY", "label": "MM/DD", "iso": None, "reason": "Another date in this packet uses month first (Record 1: 03/14/26)", "evidence": [], "evidence_count": 1, "auto_applied": False}
    rewrite_case(page, strip); open_case(page, tok)
    box = page.get_by_test_id("dates-to-confirm")
    expect(box.get_by_test_id("confirm-date")).to_have_count(2)
    expect(box.locator('input[type="radio"]')).to_have_count(0)
    expect(box.get_by_test_id("date-suggestion-reason")).to_contain_text("does not point to one date")

# ---- 2. dismissal suggestions (T-089) ---------------------------------------------------------------------------------------------

MSG = "You dismissed this kind of flag 4 times. Hide similar ones in this case?"

class DismissalStub:
    """Stubs GET .../dismissal_suggestions and POST .../apply for one flag; the POST really dismisses the flag through the review route, like the backend."""
    def __init__(self, page, token, flag_id):
        self.token, self.flag_id, self.posts, self.hidden = token, flag_id, [], False
        page.route(re.compile(r"/api/cases/[^/]+/dismissal_suggestions$"), self._get)
        page.route(re.compile(r"/api/cases/[^/]+/dismissal_suggestions/apply$"), self._post)
    def item(self):
        return {"key": "phrase:new_onset", "kind": "phrase", "label": "new onset", "dismissed_count": 4, "scope": "all cases on this computer", "flag_ids": [self.flag_id], "auto_applied": False, "message": MSG}
    def _get(self, route):
        route.fulfill(json={"suggestions": [] if self.hidden else [self.item()], "min_phrase": 3, "min_category": 5})
    def _post(self, route):
        self.posts.append(json.loads(route.request.post_data or "{}"))
        api("POST", f"/api/cases/{self.token}/items/{self.flag_id}/review", {"action": "dismiss", "note": "Hidden by dismissal-pattern suggestion (paralegal confirmed)."}); self.hidden = True
        route.fulfill(json={"key": "phrase:new_onset", "dismissed_flag_ids": [self.flag_id], "suggestions": []})

def test_dismissal_banner_never_hides_on_load_and_hides_only_on_click(page, sample_case):
    stub = DismissalStub(page, sample_case, "f_r7_2"); open_case(page, sample_case)
    flag = page.get_by_test_id("flags-panel").locator('[data-item-id="f_r7_2"]')
    ban = page.get_by_test_id("dismissal-suggestion")
    expect(ban.get_by_test_id("dismissal-message")).to_have_text(MSG)
    expect(flag).to_have_attribute("data-review", "pending"); page.wait_for_timeout(300)
    assert stub.posts == [], "nothing may be hidden without the click"
    ban.get_by_test_id("btn-hide-similar").focus(); page.keyboard.press("Enter")
    expect(flag).to_have_attribute("data-review", "dismissed")
    expect(page.get_by_test_id("dismissal-suggestion")).to_have_count(0)
    assert stub.posts == [{"key": "phrase:new_onset"}]
    expect(page.locator("#rv-live")).to_contain_text("Hid 1 similar flag")

def test_keep_showing_changes_nothing_on_the_server(page, sample_case):
    stub = DismissalStub(page, sample_case, "f_r7_2"); open_case(page, sample_case)
    flag = page.get_by_test_id("flags-panel").locator('[data-item-id="f_r7_2"]')
    page.get_by_test_id("btn-keep-showing").click()
    expect(page.get_by_test_id("dismissal-suggestion")).to_have_count(0)
    expect(flag).to_have_attribute("data-review", "pending"); assert stub.posts == []
    page.get_by_test_id("flags-panel").locator('[data-item-id="f_r7_2"]').get_by_test_id("btn-dismiss").first.click()   # a later repaint does not bring the banner back
    page.wait_for_timeout(300); expect(page.get_by_test_id("dismissal-suggestion")).to_have_count(0)

def test_dismissal_apply_error_is_shown_and_nothing_is_claimed(page, sample_case):
    DismissalStub(page, sample_case, "f_r7_2")
    page.route(re.compile(r"/api/cases/[^/]+/dismissal_suggestions/apply$"), lambda r: r.fulfill(status=500, json={"error": {"code": "internal", "message": "Could not hide those flags."}}))
    open_case(page, sample_case)
    page.get_by_test_id("btn-hide-similar").click()
    expect(page.get_by_test_id("dismissal-error")).to_contain_text("Could not hide those flags.")
    expect(page.get_by_test_id("flags-panel").locator('[data-item-id="f_r7_2"]')).to_have_attribute("data-review", "pending")
    expect(page.get_by_test_id("btn-hide-similar")).to_be_enabled()

def test_real_backend_banner_after_three_dismissals(page, cases):
    """Real route: three dismissals of one lexicon phrase make the fourth case offer the banner (local mode counts every case on this computer)."""
    for _ in range(3):
        t = cases(golden_text("sample.txt"))
        assert api("POST", f"/api/cases/{t}/items/f_r7_2/review", {"action": "dismiss"})[0] == 200
    tok = cases(golden_text("sample.txt"))
    if not api("GET", f"/api/cases/{tok}/dismissal_suggestions")[1]["suggestions"]: pytest.skip("server is not in ZLAYT_MODE=local (one case only), so dismissals do not add up")
    open_case(page, tok)
    expect(page.get_by_test_id("dismissal-message").first).to_contain_text(re.compile(r"You dismissed this kind of flag \d+ times\. Hide similar ones in this case\?"))
    expect(page.get_by_test_id("flags-panel").locator('[data-item-id="f_r7_2"]')).to_have_attribute("data-review", "pending")
    page.get_by_test_id("btn-hide-similar").first.click()
    expect(page.get_by_test_id("flags-panel").locator('[data-item-id="f_r7_2"]')).to_have_attribute("data-review", "dismissed")

# ---- 3. measured precision (T-099) ------------------------------------------------------------------------------------------------

def test_calibration_line_shows_the_backends_sentence_with_counts_and_no_percent(page, sample_case):
    open_case(page, sample_case)
    line = page.get_by_test_id("calibration-line")
    expect(line.get_by_test_id("calibration-verified")).to_contain_text(re.compile(r"In testing on \d+ synthetic cases, \d+ of \d+ verified items matched the record"))
    txt = line.inner_text(); assert "%" not in txt and "null" not in txt
    cal = api("GET", "/api/calibration")[1]["calibration"]
    if cal["small_sample"]: expect(line.get_by_test_id("calibration-small-sample")).to_contain_text(f"{cal['case_count']} synthetic test cases")

@pytest.mark.parametrize("status,word", [("missing", "No measurement file"), ("invalid", "not valid")])
def test_calibration_missing_or_invalid_is_said_plainly(page, sample_case, status, word):
    page.route(re.compile(r"/api/calibration$"), lambda r: r.fulfill(json={"status": status, "calibration": None, "message": "Run python -m evals.run to write it."}))
    open_case(page, sample_case)
    n = page.get_by_test_id("calibration-unavailable")
    expect(n).to_contain_text("Measured precision is not available"); expect(n).to_contain_text(word); expect(n).to_contain_text("No accuracy figure is shown")
    assert "%" not in page.get_by_test_id("calibration-line").inner_text()

def test_calibration_fetch_failure_is_said_plainly(page, sample_case):
    page.route(re.compile(r"/api/calibration$"), lambda r: r.fulfill(status=500, json={"error": {"code": "internal", "message": "x"}}))
    open_case(page, sample_case)
    expect(page.get_by_test_id("calibration-unavailable")).to_contain_text("could not be loaded")

def test_stale_calibration_says_the_numbers_are_from_older_prompts(page, sample_case):
    """T-102: stale true -> the line says so next to the counts and gives the backend's reason; stale false -> no such note."""
    REASON = "Changed since the run: app/llm/prompts/judge_v2.txt."
    def h(route):
        r = route.fetch(); b = r.json(); b["calibration"]["stale"] = True; b["calibration"]["stale_reason"] = REASON; route.fulfill(response=r, json=b)
    page.route(re.compile(r"/api/calibration$"), h); open_case(page, sample_case)
    line = page.get_by_test_id("calibration-line"); st = line.get_by_test_id("calibration-stale")
    expect(st).to_contain_text("These counts were measured before the latest change to the AI checks."); expect(st).to_contain_text(REASON)
    expect(line.get_by_test_id("calibration-verified")).to_be_visible()            # the counts are still shown, next to the warning
    expect(line).to_have_attribute("data-stale", "true")

def test_current_calibration_has_no_stale_note(page, sample_case):
    def h(route):
        r = route.fetch(); b = r.json(); b["calibration"]["stale"] = False; b["calibration"]["stale_reason"] = None; route.fulfill(response=r, json=b)
    page.route(re.compile(r"/api/calibration$"), h); open_case(page, sample_case)
    expect(page.get_by_test_id("calibration-verified")).to_be_visible(); expect(page.get_by_test_id("calibration-stale")).to_have_count(0)

def test_calibration_small_sample_note_follows_the_flag(page, sample_case):
    def h(route):
        r = route.fetch(); b = r.json(); b["calibration"]["small_sample"] = False; route.fulfill(response=r, json=b)
    page.route(re.compile(r"/api/calibration$"), h); open_case(page, sample_case)
    expect(page.get_by_test_id("calibration-verified")).to_be_visible(); expect(page.get_by_test_id("calibration-small-sample")).to_have_count(0)

# ---- 4. possible overlaps (T-110) ---------------------------------------------------------------------------------------------------

def test_overlap_warning_sits_with_the_total_and_changes_no_number(page, cases):
    tok = cases(lib("case_lib09_spanish_interpreter_espalda.txt")); open_case(page, tok)
    panel = page.get_by_test_id("charges-panel"); w = panel.get_by_test_id("overlap-warning")
    expect(w).to_be_visible(); expect(w.get_by_test_id("overlap-message")).to_contain_text("Possible overlap")
    expect(w.get_by_test_id("overlap-item")).to_have_count(1)
    expect(w).to_contain_text("Statement line: $1,300.00"); expect(w).to_contain_text("Separate charge: $650.00")
    assert panel.evaluate("(p) => p.querySelector('[data-testid=accepted-total]').compareDocumentPosition(p.querySelector('[data-testid=overlap-warning]')) & Node.DOCUMENT_POSITION_FOLLOWING")
    totals = api("GET", f"/api/cases/{tok}")[1]["totals"]
    expect(page.get_by_test_id("accepted-total")).to_contain_text("$0")          # nothing accepted: the warning added or removed nothing
    assert totals["accepted"]["cents"] == 0
    w.get_by_test_id("btn-overlap-goto").first.focus(); page.keyboard.press("Enter")
    expect(panel.locator('[data-item-id="%s"]' % w.get_by_test_id("overlap-item").get_attribute("data-statement-amount"))).to_be_focused()

def test_no_overlap_no_warning(page, sample_case):
    open_case(page, sample_case); expect(page.get_by_test_id("overlap-warning")).to_have_count(0)

def test_overlap_warning_fits_390_px(page, cases):
    tok = cases(lib("case_lib09_spanish_interpreter_espalda.txt")); page.set_viewport_size({"width": 390, "height": 844}); open_case(page, tok)
    expect(page.get_by_test_id("overlap-warning")).to_be_visible()
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")

# ---- 5. could-not-verify wording for flags; sentences_reason ------------------------------------------------------------------

LEAD = "The AI suggested this flag. The checks did not support it, so it is left out of the letter."   # T-060: one sentence for both reasons

def test_tray_flag_item_says_it_is_not_in_the_letter(page, cases):
    tok = cases(lib("case_lib06_lop_billed_vs_adjusted.txt")); open_case(page, tok)
    item = page.get_by_test_id("rejected-tray").locator('[data-tray-kind="flag"]').first
    expect(item.get_by_test_id("tray-flag-lead")).to_have_text(LEAD)
    expect(item.get_by_test_id("tray-attempt")).to_contain_text("The flag the AI suggested (not used)")
    tid = item.get_attribute("data-item-id")
    expect(page.get_by_test_id("flags-panel").locator('[data-item-id="%s"]' % tid)).to_have_count(0)   # never in the flags list

def test_tray_flag_that_only_the_ai_suggested_says_so(page, cases):
    tok = cases(lib("case_lib06_lop_billed_vs_adjusted.txt"))
    def only_ai(b):
        for t in b["tray"]:
            if t.get("kind") == "flag": t["reasons"] = ["LLM_ONLY"]
    rewrite_case(page, only_ai); open_case(page, tok)
    expect(page.get_by_test_id("tray-flag-lead").first).to_have_text(LEAD)
    item = page.get_by_test_id("tray-flag-lead").first.locator("xpath=ancestor::*[@data-tray-kind='flag']")
    assert item.locator("details:not([open]) [data-testid='tray-why']").count() == 1      # tray-why sits in a closed disclosure

def test_entry_tray_item_keeps_its_own_wording(page, cases):
    """Entry tray item keeps its own reason wording. T-173 (T-168): lib01 record 3 is put in the tray by tray_entry_for_record, because T-168 recorded its extract answer and the
    library case has no tray item of its own now. Assertions unchanged."""
    tok = cases(lib("case_lib01_er_only_then_gap.txt")); tray_entry_for_record(tok, "r3"); open_case(page, tok)
    item = page.get_by_test_id("rejected-tray").get_by_test_id("tray-item").first
    expect(item).to_have_attribute("data-tray-kind", "entry"); expect(item.get_by_test_id("tray-flag-lead")).to_have_count(0)
    expect(item.get_by_test_id("tray-reason")).to_be_visible()

def test_no_sentences_to_pick_shows_the_backends_reason(page, cases):
    """The manual-entry form for a tray entry with no sentences shows the backend's sentences_reason. T-173 (T-168): the lib01 tray entry (record 3) is put in the tray by
    tray_entry_for_record, because T-168 recorded its extract answer and the library case has no tray item of its own now. Assertions unchanged."""
    tok = cases(lib("case_lib01_er_only_then_gap.txt")); tray_entry_for_record(tok, "r3")
    REASON = "This record has no Date and Source lines, so no sentence can be cut from it."
    def strip(b):
        rid = next(t for t in b["tray"] if t.get("kind") == "entry")["record_ids"][0]
        for r in b["records"]:
            if r["id"] == rid: r["sentences"] = []; r["sentences_reason"] = REASON
    rewrite_case(page, strip); open_case(page, tok)
    page.get_by_test_id("btn-manual-entry").first.click()
    expect(page.get_by_test_id("manual-no-sentences")).to_have_text(REASON)      # T-060 r4 (T-096 r2 F6): the backend's reason alone; the generic lead plus "Why:" said the same thing twice
