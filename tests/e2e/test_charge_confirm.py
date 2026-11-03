"""T-154 (D-059 UI): charges are never batch-accepted, and a charge the code flagged (likely duplicate / likely total) accepts only through a confirm step that names the flag.
No library case has a flagged charge on the fixture backend, so the page's GET case is rewritten to carry `flag` + `confirm_required` on one pending charge, and the single-item review POST
answers 422 CONFIRM_REQUIRED the way the server does until the body carries `confirm` (the contract: memory/contracts/api.md, 'Flags that need a named confirm'). Everything else is the real server.
Library cases need ZLAYT_MODE=local. New test ids (declared in conftest): charge-flag (the flag word + the server's sentence in a charge row), charge-confirm (the confirm <dialog>), charge-confirm-flag
(the flag's name inside it), charge-confirm-msg (the server's sentence), btn-charge-confirm, btn-charge-cancel, batch-charges-note (batch bar: charges are accepted one at a time)."""
import json
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, reveal

LIB = "case_lib06_lop_billed_vs_adjusted"
from app.backend import amounts   # the sentence is the backend's own (T-159: amounts.promotion_flag), not a hand-written stub
_BASIS = {"dos": "2026-04-09", "codes": set(), "tokens": set()}
_REAL = amounts.promotion_flag({"id": "a9", "record_no": 1, "cents": 15000, "basis": _BASIS},
                               [{"id": "a3", "record_no": 2, "cents": 15000, "basis": _BASIS, "line": "04/09 Therapeutic exercise $150.00"}])
RAW = _REAL["message"]   # the server's sentence: it names the other line by what the record says and carries no internal id
SHOWN = RAW              # so what she reads is the same sentence
FLAG = {"flag": "likely_duplicate", "name": "Likely duplicate", "confirm_with": "likely_duplicate", "of": "a3", "message": RAW}
CONFIRMED_AT = "2026-11-02T14:40:00Z"


@pytest.fixture
def lib06():
    st, c = api("POST", "/api/cases", {"library": LIB})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    tok = c["token"]
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")


def _pending_charge(tok):
    c = api("GET", f"/api/cases/{tok}")[1]
    return next(a for a in c["amounts"] if a["kind"] == "charge" and a["review_status"] == "pending"), c


class Flagged:
    """Rewrites GET case so one pending charge is flagged, and records the review POSTs for it. `server_says` = how the stub answers an accept without `confirm`."""
    def __init__(self, page, tok, item_id, flagged_in_case=True):
        self.posts, self.item_id, self.flagged_in_case, self.confirmed = [], item_id, flagged_in_case, False
        page.route(re.compile(r"/api/cases/[^/?]+$"), self._case)
        page.route(re.compile(r"/api/cases/[^/]+/items/[^/]+/review$"), self._review)

    def _case(self, route):
        if route.request.method != "GET":
            return route.continue_()
        r = route.fetch(); body = r.json()
        if self.flagged_in_case:
            for a in body.get("amounts", []):
                if a["id"] == self.item_id and a.get("review_status") == "pending":
                    a["flag"] = dict(FLAG); a["confirm_required"] = True
                elif a["id"] == self.item_id and a.get("review_status") == "accepted" and self.confirmed:   # the server keeps the flag with confirmed_at once she confirmed it
                    a["flag"] = {**FLAG, "confirmed_at": CONFIRMED_AT}; a["confirm_required"] = False
        route.fulfill(response=r, body=json.dumps(body), headers={**r.headers, "content-type": "application/json"})

    def _review(self, route):
        req = route.request
        if self.item_id not in req.url:
            return route.continue_()
        data = json.loads(req.post_data or "{}"); self.posts.append(data)
        if data.get("action") == "accept" and "confirm" not in data:
            return route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CONFIRM_REQUIRED",
                "message": "Likely duplicate: " + RAW.replace(" Counting both", " Counting both") + " It is not counted unless you confirm that flag by name (likely_duplicate).",
                "detail": {"item_id": self.item_id, "reason_code": "CONFIRM_REQUIRED", "flag": "likely_duplicate", "name": "Likely duplicate", "confirm_with": "likely_duplicate", "of": None, "message": RAW}}}))
        if data.get("action") == "accept" and data.get("confirm") == FLAG["confirm_with"]:
            r = route.fetch(); body = r.json(); self.confirmed = True
            if isinstance(body.get("item"), dict):
                body["item"]["flag"] = {**FLAG, "confirmed_at": CONFIRMED_AT}; body["item"]["confirm_required"] = False
            return route.fulfill(response=r, body=json.dumps(body), headers={**r.headers, "content-type": "application/json"})
        route.continue_()


def _charge_row(page, item_id):
    return page.get_by_test_id("charges-panel").locator(f'[data-item-id="{item_id}"]').first


def test_flagged_charge_shows_its_flag_and_accepts_only_through_a_named_confirm(page, lib06):
    a, _ = _pending_charge(lib06)
    stub = Flagged(page, lib06, a["id"])
    open_case(page, lib06)
    row = _charge_row(page, a["id"]); row.scroll_into_view_if_needed()
    flag = row.get_by_test_id("charge-flag")
    expect(flag).to_contain_text("Likely duplicate"); expect(flag).to_contain_text(SHOWN)
    row.get_by_test_id("btn-accept").click()
    dlg = page.get_by_test_id("charge-confirm"); expect(dlg).to_be_visible()
    expect(dlg.get_by_test_id("charge-confirm-flag")).to_have_text("Likely duplicate")
    expect(dlg.get_by_test_id("charge-confirm-msg")).to_contain_text(SHOWN)
    assert stub.posts == []                                                         # nothing was sent before she confirmed
    expect(dlg.get_by_test_id("btn-charge-cancel")).to_be_focused()                 # the safe answer has focus
    dlg.get_by_test_id("btn-charge-cancel").click()
    expect(dlg).to_be_hidden(); assert stub.posts == []
    expect(row).to_have_attribute("data-review", "pending")
    row.get_by_test_id("btn-accept").click()
    page.get_by_test_id("btn-charge-confirm").click()
    expect(row).to_have_attribute("data-review", "accepted")
    assert stub.posts == [{"action": "accept", "confirm": "likely_duplicate"}]
    st = api("GET", f"/api/cases/{lib06}")[1]
    assert next(x for x in st["amounts"] if x["id"] == a["id"])["review_status"] == "accepted"


def test_the_a_key_asks_first_and_escape_cancels(page, lib06):
    a, _ = _pending_charge(lib06)
    stub = Flagged(page, lib06, a["id"])
    open_case(page, lib06)
    row = _charge_row(page, a["id"]); row.scroll_into_view_if_needed(); row.focus(); expect(row).to_be_focused()
    page.keyboard.press("a")
    dlg = page.get_by_test_id("charge-confirm"); expect(dlg).to_be_visible()
    page.keyboard.press("Escape")
    expect(dlg).to_be_hidden(); assert stub.posts == []
    expect(row).to_have_attribute("data-review", "pending")
    page.keyboard.press("a"); expect(dlg).to_be_visible()
    page.keyboard.press("Tab"); expect(page.get_by_test_id("btn-charge-confirm")).to_be_focused()
    page.keyboard.press("Enter")
    expect(row).to_have_attribute("data-review", "accepted")
    assert stub.posts[-1]["confirm"] == "likely_duplicate"


def test_a_refusal_from_the_server_opens_the_same_confirm(page, lib06):
    """The page did not know the charge was flagged (a stale case): the server's 422 CONFIRM_REQUIRED opens the confirm, naming the flag, and the retry carries `confirm`."""
    a, _ = _pending_charge(lib06)
    stub = Flagged(page, lib06, a["id"], flagged_in_case=False)
    open_case(page, lib06)
    row = _charge_row(page, a["id"]); row.scroll_into_view_if_needed()
    row.get_by_test_id("btn-accept").click()
    dlg = page.get_by_test_id("charge-confirm"); expect(dlg).to_be_visible()
    expect(dlg.get_by_test_id("charge-confirm-flag")).to_have_text("Likely duplicate")
    assert stub.posts == [{"action": "accept"}]
    page.get_by_test_id("btn-charge-confirm").click()
    expect(row).to_have_attribute("data-review", "accepted")
    assert stub.posts[-1] == {"action": "accept", "confirm": "likely_duplicate"}


def test_an_unflagged_charge_accepts_in_one_step(page, lib06):
    a, _ = _pending_charge(lib06)
    open_case(page, lib06)
    row = _charge_row(page, a["id"]); row.scroll_into_view_if_needed()
    expect(row.get_by_test_id("charge-flag")).to_have_count(0)
    row.get_by_test_id("btn-accept").click()
    expect(row).to_have_attribute("data-review", "accepted")
    expect(page.get_by_test_id("charge-confirm")).to_be_hidden()


def test_confirm_fits_a_390px_screen(pw, lib06):
    a, _ = _pending_charge(lib06)
    b = pw.chromium.launch()
    try:
        pg = b.new_context(viewport={"width": 390, "height": 844}).new_page()
        Flagged(pg, lib06, a["id"]); open_case(pg, lib06)
        row = _charge_row(pg, a["id"]); row.scroll_into_view_if_needed()
        row.get_by_test_id("btn-accept").click()
        dlg = pg.get_by_test_id("charge-confirm"); expect(dlg).to_be_visible()
        for t in ("btn-charge-confirm", "btn-charge-cancel"):
            bb = dlg.get_by_test_id(t).bounding_box(); assert bb["x"] >= 0 and bb["x"] + bb["width"] <= 390 and bb["height"] >= 36 and bb["y"] + bb["height"] <= 844
        assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    finally:
        b.close()


def test_batch_bar_says_charges_are_one_at_a_time_and_sends_no_charge(page, lib06):
    c = api("GET", f"/api/cases/{lib06}")[1]
    charge_ids = {a["id"] for a in c["amounts"]}
    sent = []
    page.route(re.compile(r"/review/batch$"), lambda route: (sent.append(json.loads(route.request.post_data)), route.continue_()))
    open_case(page, lib06)
    note = page.get_by_test_id("batch-bar").get_by_test_id("batch-charges-note")
    expect(note).to_be_visible(); expect(note).to_contain_text("one at a time")
    btn = page.get_by_test_id("btn-accept-verified")
    if btn.is_enabled():
        btn.click()
        expect(page.get_by_test_id("btn-undo-batch")).to_be_visible()
        assert sent and sent[0]["action"] == "accept" and not (set(sent[0]["item_ids"]) & charge_ids)
    # the charges are still waiting for her own decision
    assert all(a["review_status"] == "pending" for a in api("GET", f"/api/cases/{lib06}")[1]["amounts"] if a["kind"] == "charge")


def test_a_charges_not_batched_refusal_is_said_plainly(page, lib06):
    msg = "Charges are accepted one at a time, so a charge cannot be part of a batch. Take the charge out and review it by itself; nothing was changed."
    page.route(re.compile(r"/review/batch$"), lambda route: route.fulfill(status=422, content_type="application/json",
               body=json.dumps({"error": {"code": "CHARGES_NOT_BATCHED", "message": msg, "detail": {"rejected": [{"id": "a1", "reason": "charge_in_batch"}]}}})))
    open_case(page, lib06)
    btn = page.get_by_test_id("btn-accept-verified")
    if btn.is_disabled():
        pytest.skip("no verified pending entries on this case")
    btn.click()
    expect(page.locator("#rv-live")).to_contain_text("one at a time")
    expect(page.get_by_test_id("btn-undo-batch")).to_have_count(0)


def _confirm_it(page, row):
    row.get_by_test_id("btn-accept").click()
    page.get_by_test_id("btn-charge-confirm").click()
    expect(row).to_have_attribute("data-review", "accepted")


def test_the_a_key_on_an_accepted_confirmed_flagged_charge_says_so_and_sends_nothing(page, lib06):
    """Claims adjuster (T-154 r1, major): `a` on a charge she already counted reopened 'It is not counted' and wrote a second accept."""
    a, _ = _pending_charge(lib06)
    stub = Flagged(page, lib06, a["id"])
    open_case(page, lib06)
    row = _charge_row(page, a["id"]); row.scroll_into_view_if_needed()
    _confirm_it(page, row)
    assert len(stub.posts) == 1
    row.focus(); expect(row).to_be_focused(); page.keyboard.press("a")
    page.wait_for_timeout(400)
    expect(page.get_by_test_id("charge-confirm")).to_be_hidden()
    expect(page.locator("#rv-live")).to_contain_text("Accepted already")
    assert len(stub.posts) == 1                                                       # no second decision
    row.get_by_test_id("btn-accept").click(); page.wait_for_timeout(300)
    assert len(stub.posts) == 1 and not page.get_by_test_id("charge-confirm").is_visible()


def test_the_audit_drawer_and_the_trace_name_the_flag_and_the_confirm(page, lib06):
    a, _ = _pending_charge(lib06)
    Flagged(page, lib06, a["id"])
    open_case(page, lib06)
    row = _charge_row(page, a["id"]); row.scroll_into_view_if_needed()
    reveal(row.get_by_test_id("btn-trace")).first.click()                                        # before the confirm: the flag needs her named confirm
    note = page.locator("#why-modal").get_by_test_id("trace-charge-flag")
    expect(note).to_contain_text("Likely duplicate"); expect(note).to_contain_text("needs your named confirm")
    page.keyboard.press("Escape")
    _confirm_it(page, row)
    reveal(row.get_by_test_id("btn-trace")).first.click()
    note = page.locator("#why-modal").get_by_test_id("trace-charge-flag")
    expect(note).to_contain_text("Likely duplicate"); expect(note).to_contain_text("You confirmed"); expect(note).not_to_contain_text("needs your named confirm")
    page.keyboard.press("Escape")
    reveal(row.get_by_test_id("btn-audit")).click()
    drawer = page.get_by_test_id("audit-drawer")
    flag = drawer.get_by_test_id("audit-charge-flag")
    expect(flag).to_contain_text("Likely duplicate"); expect(flag).to_contain_text("confirmed")
    ev = drawer.get_by_test_id("audit-event")
    expect(ev.filter(has_text="accept").last).to_contain_text("confirmed Likely duplicate")
    assert not re.search(r"\ba\d+\b|\(likely_duplicate\)", drawer.inner_text() + page.locator("#why-modal").inner_text())


def test_the_fallback_dialog_uses_plain_words_only(page, lib06):
    """The page did not know the charge was flagged: the dialog shows the flag's sentence, not the server's whole error (no token, no repeated 'not counted', no internal id)."""
    a, _ = _pending_charge(lib06)
    Flagged(page, lib06, a["id"], flagged_in_case=False)
    open_case(page, lib06)
    row = _charge_row(page, a["id"]); row.scroll_into_view_if_needed()
    row.get_by_test_id("btn-accept").click()
    dlg = page.get_by_test_id("charge-confirm"); expect(dlg).to_be_visible()
    txt = dlg.inner_text()
    assert "(likely_duplicate)" not in txt and "likely_duplicate" not in txt
    assert txt.count("not counted") == 1, txt
    assert not re.search(r"\ba\d+\b", txt), txt
    expect(dlg.get_by_test_id("charge-confirm-msg")).to_contain_text(SHOWN)


def test_a_duplicate_sentence_names_the_other_line_not_an_internal_id(page, lib06):
    a, _ = _pending_charge(lib06)
    Flagged(page, lib06, a["id"])
    open_case(page, lib06)
    row = _charge_row(page, a["id"]); row.scroll_into_view_if_needed()
    t = row.get_by_test_id("charge-flag").inner_text()
    assert not re.search(r"\ba\d+\b", t), t
    assert "Therapeutic exercise $150.00" in t and "record 2" in t and "2026-04-09" not in t, t   # the backend's own wording: the other line's text, amount, record; no date (T-202 r6 rule 5: the message never prints a prose date)


def test_the_shortcut_sheet_says_a_flagged_charge_asks_first(page, lib06):
    open_case(page, lib06)
    page.get_by_test_id("btn-shortcuts").click()
    sheet = page.get_by_test_id("shortcuts-modal"); expect(sheet).to_be_visible()
    assert "flagged charge asks first" in sheet.inner_text().replace("\n", " ")
