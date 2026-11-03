"""T-097 round 3 (D-051, T-098 r2): Accept (single and batch) can be refused with 422 CODE_CHECK_FAILED. The UI shows the server's plain reason next to the item's Accept button
with an Edit action, and for a batch lists the items it refused; nothing is accepted. Each test runs twice: against the REAL backend (needs ZLAYT_DB, the SQLite file of the server
under test, to put a failing summary into the store the way a stale or imported state would) and against a route stub that answers exactly as memory/contracts/api.md says."""
import json
import os
import re
import sys
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, reveal

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REASON = "The summary has a number that is not in the quote: 5. Edit the summary to match the quote."
NEXT = {"code": "EDIT_SUMMARY", "text": "Edit the summary to match the quote"}


def _entry(tok, eid):
    c = api("GET", f"/api/cases/{tok}")[1]
    return next(e for e in c["entries"] + c["undated_entries"] if e["id"] == eid)


def _break(tok, eid):
    """Real backend: put 'Pain 5/10' (a figure the quote does not carry) into the stored summary, like a stale or imported state."""
    path = os.environ.get("ZLAYT_DB")
    if not path:
        pytest.skip("the real-backend variant needs ZLAYT_DB (the SQLite file of the server under test)")
    sys.path.insert(0, ROOT)
    from app.db import db as DB
    conn = DB.connect(path)
    try:
        assert "5/10" not in (_entry(tok, eid)["excerpt"] or "")
        DB.update_item(conn, eid, now=9e9, case=tok, summary="Pain 5/10")
    finally:
        conn.close()


class Refuse:
    """Stub: POST .../review (accept) and POST .../review/batch (accept) answer 422 CODE_CHECK_FAILED while the item's summary is unchanged (an edit through the real route lifts it)."""
    def __init__(self, tok, eid):
        self.tok, self.eid = tok, eid
        self.base = _entry(tok, eid)["summary"]
        self.posts = 0

    def attach(self, page):
        page.route(re.compile(r"/api/cases/[^/]+/items/[^/]+/review$"), self._single)
        page.route(re.compile(r"/api/cases/[^/]+/review/batch$"), self._batch)

    def active(self):
        return _entry(self.tok, self.eid)["summary"] == self.base

    def _single(self, route):
        body = route.request.post_data_json or {}
        if body.get("action") != "accept" or not route.request.url.endswith(f"/items/{self.eid}/review") or not self.active():
            return route.fallback()
        self.posts += 1
        route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CODE_CHECK_FAILED", "message": REASON, "detail": {
            "item_id": self.eid, "reason_code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "step_id": "summary_tokens", "failed_steps": ["summary_tokens"], "tokens": ["5"],
            "next_action": dict(NEXT, target={"item_id": self.eid})}}}))

    def _batch(self, route):
        body = route.request.post_data_json or {}
        if body.get("action") != "accept" or self.eid not in (body.get("item_ids") or []) or not self.active():
            return route.fallback()
        self.posts += 1
        route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CODE_CHECK_FAILED", "message": REASON + " Nothing was changed.", "detail": {"rejected": [
            {"id": self.eid, "reason": "code_check_failed", "reason_code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "why": REASON, "next_action": dict(NEXT, target={"item_id": self.eid})}]}}}))


@pytest.fixture(params=["real", "stub"])
def broken(request, sample_case):
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    orig = e["summary"]
    if request.param == "real":
        _break(sample_case, e["id"])
        assert _entry(sample_case, e["id"])["summary"] == "Pain 5/10"
        stub = None
    else:
        stub = Refuse(sample_case, e["id"])
    return {"tok": sample_case, "id": e["id"], "orig": orig, "mode": request.param, "stub": stub}


def arm(t, page):
    if t["stub"]:
        t["stub"].attach(page)
    return t


def row_of(page, i):
    return page.get_by_test_id("timeline").locator(f'[data-item-id="{i}"]').first


def vis(page, loc, frames=120):
    """True once the box is fully inside the viewport. Polls frame by frame (no sleeps): the row can still be scrolling after a click,
    so a single bounding_box() read can land mid-scroll."""
    vh = page.viewport_size["height"]
    for _ in range(frames):
        bb = loc.bounding_box()
        if bb is not None and bb["y"] >= 0 and bb["y"] + bb["height"] <= vh:
            return True
        page.evaluate("() => new Promise(r => requestAnimationFrame(() => r(true)))")
    return False


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action(pw, broken, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        t = arm(broken, pg)
        open_case(pg, t["tok"]); row = row_of(pg, t["id"])
        row.scroll_into_view_if_needed()
        btn = row.get_by_test_id("btn-accept"); btn.click()
        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
        msg = box.get_by_test_id("accept-refused-msg").inner_text()
        assert msg.startswith("Not accepted. ") and msg.endswith("Edit the summary to match the quote."), msg
        assert "not in the quote" in msg or t["mode"] == "real"
        assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
        assert abs(box.bounding_box()["y"] - btn.bounding_box()["y"]) < 140, "next to the Accept button"
        assert box.get_attribute("role") == "alert"
        assert api("GET", f"/api/cases/{t['tok']}")[1]["review"]["counts"]["accepted"] == 0 and _entry(t["tok"], t["id"])["review_status"] == "pending", "nothing was changed"
        # Edit opens the item's edit box; a passing edit clears the refusal and the item is accepted by the edit
        box.get_by_test_id("btn-accept-refused-edit").click()
        ta = row.get_by_test_id("edit-summary"); expect(ta).to_be_visible()
        assert pg.evaluate("document.activeElement === document.querySelector('[data-item-id=\"%s\"] textarea')" % t["id"]) or ta.is_visible()
        ta.fill(t["orig"]); row.get_by_test_id("btn-save-edit").click()
        expect(row_of(pg, t["id"])).to_have_attribute("data-review", "edited")
        expect(row_of(pg, t["id"]).get_by_test_id("accept-refused")).to_be_hidden()
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


def test_refused_accept_by_keyboard_keeps_focus_and_says_it(page, broken):
    t = arm(broken, page)
    open_case(page, t["tok"]); row = row_of(page, t["id"]); row.focus()
    page.keyboard.press("a")
    expect(row.get_by_test_id("accept-refused")).to_be_visible()
    assert page.evaluate("document.activeElement.getAttribute('data-item-id')") == t["id"], "focus stays on the refused item"
    assert row.get_by_test_id("btn-accept").get_attribute("aria-pressed") == "false"
    page.keyboard.press("d")                                   # deciding the item another way clears the refusal
    expect(row_of(page, t["id"]).get_by_test_id("accept-refused")).to_be_hidden()


def test_refused_batch_lists_the_items_it_refused_and_nothing_is_accepted(page, broken):
    t = arm(broken, page)
    open_case(page, t["tok"])
    page.get_by_test_id("btn-accept-verified").click()
    box = page.get_by_test_id("batch-refused"); expect(box).to_be_visible()
    assert box.get_attribute("role") == "alert" and box.get_by_test_id("batch-refused-msg").inner_text().startswith("Nothing was accepted.")
    items = box.get_by_test_id("batch-refused-item"); assert items.count() == 1
    assert items.first.get_attribute("data-refused-id") == t["id"]
    txt = items.first.inner_text()
    assert "Edit the summary to match the quote" in txt or "Edit the summary" in txt
    c = api("GET", f"/api/cases/{t['tok']}")[1]
    assert c["review"]["counts"]["accepted"] == 0, "all or nothing: the batch accepted none"
    items.first.get_by_test_id("btn-batch-refused-edit").click()
    ta = row_of(page, t["id"]).get_by_test_id("edit-summary"); expect(ta).to_be_visible()
    ta.fill(t["orig"]); row_of(page, t["id"]).get_by_test_id("btn-save-edit").click()
    expect(page.get_by_test_id("batch-refused")).to_have_count(0)      # the edited item is no longer waiting, so it leaves the list
    page.get_by_test_id("btn-accept-verified").click()
    expect(page.get_by_test_id("btn-undo-batch")).to_be_visible()      # the next batch goes through


def test_case_verdict_reads_the_backend_label_in_rail_and_panel(page, sample_case):
    """Real backend: an accepted AI draft whose summary then fails a code check is a gate blocker; the case verdict is the backend's words, in the rail and in the panel."""
    from tests.e2e.test_stepper import open_rail, open_judges
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    assert api("POST", f"/api/cases/{sample_case}/items/{e['id']}/review", {"action": "accept"})[0] == 200
    _break(sample_case, e["id"])
    open_case(page, sample_case); cs = open_rail(page)
    assert cs.get_by_test_id("case-verdict").text_content() == "1 summary fails a check"
    jp = open_judges(page)
    assert jp.get_by_test_id("judge-case-verdict").text_content() == "1 summary fails a check"
    assert "1 summary fails a check, blocks export: 1" in jp.get_by_test_id("judge-summary-counts").inner_text()
    blocker = cs.locator(f'[data-testid="gate-blocker"][data-jump-item="{e["id"]}"]')
    assert "This summary doesn't match the quote:" in blocker.inner_text() and "Your wording" not in blocker.inner_text(), "the paralegal did not write an AI draft"
    assert blocker.get_by_test_id("btn-gate-edit").inner_text() == "Edit the summary"


# ---- T-104: a first failing check on the QUOTE (next_action EDIT_QUOTE) offers "Change the quote" and opens the quote picker; CODE_CHECK_FAILED returned by an EDIT is shown
# inline under the edit box (typed text kept); the Why dialog follows the backend verdict string as sent. Real backend (ZLAYT_DB) and a route stub per case.
QUOTE_REASON = "The quote does not start and end on whole sentences. Change the quote to whole sentences of the record that keep the hedge sentence."
QUOTE_NEXT = {"code": "EDIT_QUOTE", "text": "Change the quote to whole sentences of the record that keep the hedge sentence"}


def _break_quote(tok, eid):
    """Real backend: store a quote that starts mid-sentence (first word cut off), like a stale or imported state. The record offsets stay, so the quote picker still preselects the whole sentences."""
    path = os.environ.get("ZLAYT_DB")
    if not path:
        pytest.skip("the real-backend variant needs ZLAYT_DB (the SQLite file of the server under test)")
    sys.path.insert(0, ROOT)
    from app.db import db as DB
    conn = DB.connect(path)
    try:
        words = _entry(tok, eid)["excerpt"].split(" ")
        DB.update_item(conn, eid, now=9e9, case=tok, excerpt=" ".join(words[1:]))
    finally:
        conn.close()


class RefuseQuote(Refuse):
    """Stub: accept (single and batch) and a summary-only edit answer 422 CODE_CHECK_FAILED / EDIT_QUOTE while the item's quote is unchanged; a quote edit goes to the real route and lifts it."""
    def __init__(self, tok, eid, edit_code="EDIT_QUOTE"):
        super().__init__(tok, eid)
        self.base_q = _entry(tok, eid)["excerpt"]
        self.edit_code = edit_code

    def active(self):
        return _entry(self.tok, self.eid)["excerpt"] == self.base_q and _entry(self.tok, self.eid)["review_status"] == "pending"

    def _detail(self, code):
        return {"item_id": self.eid, "reason_code": "EXCERPT_NOT_WHOLE_SENTENCE", "step_id": "excerpt_whole_sentence", "failed_steps": ["excerpt_whole_sentence"], "tokens": [],
                "next_action": dict(QUOTE_NEXT if code == "EDIT_QUOTE" else NEXT, code=code, target={"item_id": self.eid})}

    def _single(self, route):
        body = route.request.post_data_json or {}
        if not route.request.url.endswith(f"/items/{self.eid}/review") or not self.active():
            return route.fallback()
        if body.get("action") == "accept":
            self.posts += 1
            return route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CODE_CHECK_FAILED", "message": QUOTE_REASON, "detail": self._detail("EDIT_QUOTE")}}))
        if body.get("action") == "edit" and "summary" in (body.get("edits") or {}):
            self.posts += 1
            msg = QUOTE_REASON if self.edit_code == "EDIT_QUOTE" else REASON
            return route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CODE_CHECK_FAILED", "message": msg, "detail": self._detail(self.edit_code)}}))
        return route.fallback()

    def _batch(self, route):
        body = route.request.post_data_json or {}
        if body.get("action") != "accept" or self.eid not in (body.get("item_ids") or []) or not self.active():
            return route.fallback()
        self.posts += 1
        route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CODE_CHECK_FAILED", "message": QUOTE_REASON + " Nothing was changed.", "detail": {"rejected": [
            {"id": self.eid, "reason": "code_check_failed", "reason_code": "EXCERPT_NOT_WHOLE_SENTENCE", "why": QUOTE_REASON, "next_action": dict(QUOTE_NEXT, target={"item_id": self.eid})}]}}}))


@pytest.fixture(params=["real", "stub"])
def broken_quote(request, sample_case):
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    if request.param == "real":
        _break_quote(sample_case, e["id"]); stub = None
    else:
        stub = RefuseQuote(sample_case, e["id"])
    return {"tok": sample_case, "id": e["id"], "orig": e["summary"], "excerpt": e["excerpt"], "mode": request.param, "stub": stub}


def _picker_open(page, t):
    """The item's own quote picker is open (its sentences listed, focus on one of them, on screen). Saving a choice is the picker's own job (excerpt.js); the sample record prints
    'Excerpt: "..."' around the quote, so its sentence units cannot rebuild the original quote and this spec stops at opening it."""
    row = row_of(page, t["id"]); ed = row.get_by_test_id("excerpt-editor")
    expect(ed).to_be_visible(); assert ed.get_by_test_id("excerpt-unit").count() >= 2
    assert page.evaluate("document.activeElement.getAttribute('data-testid')") == "excerpt-unit", "focus moves into the picker"
    assert vis(page, ed.get_by_test_id("btn-save-excerpt")) or vis(page, ed.get_by_test_id("excerpt-unit").first), "the picker is on screen"


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_refused_accept_on_a_quote_check_offers_change_the_quote_and_opens_the_picker(pw, broken_quote, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        t = arm(broken_quote, pg)
        open_case(pg, t["tok"]); row = row_of(pg, t["id"]); row.scroll_into_view_if_needed()
        row.get_by_test_id("btn-accept").click()
        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
        msg = box.get_by_test_id("accept-refused-msg").inner_text()
        assert msg.startswith("Not accepted. ") and "whole sentences" in msg, msg
        q = box.get_by_test_id("btn-accept-refused-quote")
        assert q.inner_text() == "Change the quote" and box.get_by_test_id("btn-accept-refused-edit").count() == 0, "a quote check does not offer 'Edit the summary'"
        assert "Change the quote for" in q.get_attribute("aria-label")
        q.click()
        _picker_open(pg, t)
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


def test_refused_batch_on_a_quote_check_offers_change_the_quote_per_item(page, broken_quote):
    t = arm(broken_quote, page)
    open_case(page, t["tok"])
    page.get_by_test_id("btn-accept-verified").click()
    box = page.get_by_test_id("batch-refused"); expect(box).to_be_visible()
    item = box.get_by_test_id("batch-refused-item"); assert item.count() == 1 and item.first.get_attribute("data-refused-id") == t["id"]
    assert item.first.get_by_test_id("btn-batch-refused-edit").count() == 0 and "summary" not in box.get_by_test_id("batch-refused-msg").inner_text()
    assert item.first.get_by_test_id("btn-batch-refused-quote").inner_text() == "Change the quote"
    item.first.get_by_test_id("btn-batch-refused-quote").click()
    _picker_open(page, t)


def test_a_refused_summary_check_still_offers_edit_the_summary(page, broken):
    """EDIT_SUMMARY keeps 'Edit the summary' (and no quote button)."""
    t = arm(broken, page)
    open_case(page, t["tok"]); row = row_of(page, t["id"])
    row.get_by_test_id("btn-accept").click()
    box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
    assert box.get_by_test_id("btn-accept-refused-edit").inner_text() == "Edit the summary" and box.get_by_test_id("btn-accept-refused-quote").count() == 0


def test_code_check_failed_returned_by_an_edit_shows_inline_under_the_edit_box_and_keeps_the_text(page, broken_quote):
    """A summary-only edit on an item whose quote fails: 422 CODE_CHECK_FAILED / EDIT_QUOTE. The sentence sits under the edit box, the box stays open with the typed text,
    nothing is saved, and 'Change the quote' opens the picker."""
    t = arm(broken_quote, page)
    open_case(page, t["tok"]); row = row_of(page, t["id"])
    row.get_by_test_id("btn-edit").click()
    ta = row.get_by_test_id("edit-summary"); expect(ta).to_be_visible()
    typed = t["orig"].rstrip(".") + " as the record says."
    ta.fill(typed); row.get_by_test_id("btn-save-edit").click()
    ref = row.get_by_test_id("edit-refused-msg"); expect(ref).to_be_visible()
    assert "whole sentences" in ref.inner_text() and "Not accepted" not in ref.inner_text()
    form = row.locator("form.rv-edit"); assert form.is_visible() and ta.input_value() == typed, "the box stays open with the typed text"
    ya, yb = ref.bounding_box()["y"], form.bounding_box()["y"] + form.bounding_box()["height"]
    assert ya >= yb - 2, "under the edit box"
    assert ref.evaluate("e => e.closest('.rv-error').getAttribute('role')") == "alert"
    assert _entry(t["tok"], t["id"])["review_status"] == "pending", "nothing was saved"
    assert page.evaluate("document.activeElement.tagName") == "TEXTAREA", "focus stays in the box"
    row.get_by_test_id("btn-edit-refused-quote").click()
    _picker_open(page, t)


def test_code_check_failed_on_an_edit_with_edit_the_summary_has_no_quote_button(page, sample_case):
    """Stub: the edit route answers CODE_CHECK_FAILED / EDIT_SUMMARY. Same inline place, text kept, no 'Change the quote'."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    st = RefuseQuote(sample_case, e["id"], edit_code="EDIT_SUMMARY"); st.attach(page)
    open_case(page, sample_case); row = row_of(page, e["id"])
    row.get_by_test_id("btn-edit").click(); ta = row.get_by_test_id("edit-summary"); typed = e["summary"] + " Pain 5/10."
    ta.fill(typed); row.get_by_test_id("btn-save-edit").click()
    ref = row.get_by_test_id("edit-refused-msg"); expect(ref).to_be_visible()
    assert ref.inner_text() == REASON and ta.input_value() == typed and row.get_by_test_id("btn-edit-refused-quote").count() == 0


def _why_dialog(page, t, rewrite_label=None):
    """Accept the item (AI draft), break its quote in the store, open the Why dialog. rewrite_label rewrites the item trace's verdict label (a stub of what the backend sends)."""
    assert api("POST", f"/api/cases/{t['tok']}/items/{t['id']}/review", {"action": "accept"})[0] == 200
    _break_quote(t["tok"], t["id"])
    if rewrite_label:
        def fn(route):
            d = route.fetch().json(); d["verdict"] = dict(d.get("verdict") or {}, label=rewrite_label); route.fulfill(json=d)
        page.route(re.compile(r"/api/cases/[^/]+/items/[^/]+/trace$"), fn)
    open_case(page, t["tok"])
    reveal(page.locator(f'[data-testid="queue"] [data-item-id="{t["id"]}"], [data-testid="timeline"] [data-item-id="{t["id"]}"]').first.get_by_test_id("entry-why")).click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    return st


def test_why_dialog_uses_the_backend_verdict_string_for_an_ai_draft_and_offers_change_the_quote(page, sample_case):
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    st = _why_dialog(page, {"tok": sample_case, "id": e["id"]})
    assert st.get_by_test_id("item-verdict").inner_text() == "Needs your attention: a check on this summary fails", "the backend's verdict string as sent"
    w = st.get_by_test_id("item-wording-fail"); txt = w.inner_text()
    assert txt.startswith("This summary doesn't match the quote:") and "Your wording" not in txt
    b = w.get_by_test_id("btn-wording-edit"); assert b.inner_text() == "Change the quote"
    b.click()
    expect(page.locator("#why-modal")).not_to_be_visible()
    expect(row_of(page, e["id"]).get_by_test_id("excerpt-editor")).to_be_visible()


@pytest.mark.parametrize("label,lead", [("Needs your attention: a check on your wording fails", "Your wording doesn't match the quote:"),
                                         ("Needs your attention: a check on this summary fails", "This summary doesn't match the quote:")])
def test_why_dialog_lead_follows_the_verdict_string_not_a_frontend_guess(page, sample_case, label, lead):
    """An AI draft whose trace the backend labels 'your wording' reads 'Your wording...'; the same item labelled 'this summary' reads 'This summary...'."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
    st = _why_dialog(page, {"tok": sample_case, "id": e["id"]}, rewrite_label=label)
    assert st.get_by_test_id("item-verdict").inner_text() == label
    assert st.get_by_test_id("item-wording-fail").inner_text().startswith(lead)
