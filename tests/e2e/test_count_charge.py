"""T-172 (D-064 UI): every not-counted amount shows its plain reason in the charges section; one that is held back only for a missing detail (countable) offers "Count this charge" with a named
confirm ("I checked this is a separate charge for a service"); a rule-excluded one (balance, payment, adjustment, total) shows why and offers no counting. Real server on lib11 (the ledger case:
$3,260 accepted + $250 + $180 + $2,310 counted = $6,000.00). Library cases need ZLAYT_MODE=local. Contract: memory/contracts/api.md ('Why an amount is not counted, and counting it').
Test ids (declared in conftest): not-counted-reason (the code's sentence, in the Status cell), btn-count-charge (the action, countable rows only), count-confirm (the confirm <dialog>), count-confirm-amount,
count-confirm-reason, btn-count-confirm (named: 'I checked this is a separate charge for a service'), btn-count-cancel, count-error (a refusal in the server's words, under the Count button)."""
import json
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case

LIB = "case_lib11_priors_and_ledger"
NAMED = "I checked this is a separate charge for a service"
COUNTABLE = ["$250.00", "$180.00", "$2,310.00"]
EXCLUDED = {"$2,740.00": "repeats the charges", "$300.00": "Payment", "$274.00": "Adjustment", "$2,166.00": "Balance or amount due"}


@pytest.fixture
def lib11():
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


def _by_text(tok):
    return {a["text"]: a for a in api("GET", f"/api/cases/{tok}")[1]["amounts"]}


def _row(page, a):
    return page.get_by_test_id("charges-panel").locator(f'[data-item-id="{a["id"]}"]').first


def _norm(s):
    return re.sub(r"\s+", " ", s).strip()


def _accept_the_listed_charge(page, tok):
    a = _by_text(tok)["$3,260"]
    row = _row(page, a); row.scroll_into_view_if_needed()
    row.get_by_test_id("btn-accept").click()
    expect(row).to_have_attribute("data-review", "accepted")
    expect(page.get_by_test_id("accepted-total")).to_contain_text("$3,260.00")


def _count_with_mouse(page, a):
    row = _row(page, a); row.scroll_into_view_if_needed()
    row.get_by_test_id("btn-count-charge").click()
    dlg = page.get_by_test_id("count-confirm"); expect(dlg).to_be_visible()
    dlg.get_by_test_id("btn-count-confirm").click()
    expect(dlg).to_be_hidden()
    expect(_row(page, a)).to_have_attribute("data-amount-kind", "charge")
    expect(_row(page, a)).to_have_attribute("data-review", "accepted")


def test_every_not_counted_amount_says_why_and_only_the_countable_ones_offer_to_count(page, lib11):
    amounts = _by_text(lib11)
    open_case(page, lib11)
    for text in COUNTABLE + list(EXCLUDED):
        a = amounts[text]; assert a["not_counted_reason"], text
        row = _row(page, a); row.scroll_into_view_if_needed()
        reason = row.get_by_test_id("not-counted-reason")
        expect(reason).to_have_count(1)
        assert _norm(reason.inner_text()).startswith("Not counted"), text
        assert a["not_counted_reason"] in _norm(reason.inner_text()), text           # the server's sentence, unedited
    for text in COUNTABLE:
        row = _row(page, amounts[text])
        expect(row.get_by_test_id("not-counted-reason")).to_contain_text("no date of service")
        expect(row.get_by_test_id("btn-count-charge")).to_have_count(1)
        expect(row.get_by_test_id("btn-count-charge")).to_have_text("Count this charge")
    for text, word in EXCLUDED.items():
        row = _row(page, amounts[text])
        expect(row.get_by_test_id("not-counted-reason")).to_contain_text(word)
        expect(row.get_by_test_id("btn-count-charge")).to_have_count(0)               # a balance, payment, adjustment or total line offers nothing to count
    assert page.get_by_test_id("unclear-tray").get_by_test_id("btn-count-charge").count() == 3
    # the listed charge (a1) is not a not-counted amount: no reason line, no Count action
    a1 = _row(page, amounts["$3,260"])
    expect(a1.get_by_test_id("not-counted-reason")).to_have_count(0); expect(a1.get_by_test_id("btn-count-charge")).to_have_count(0)


def test_counting_the_three_ledger_lines_makes_the_total_six_thousand(page, lib11):
    amounts = _by_text(lib11)
    posts = []
    page.on("request", lambda r: posts.append(json.loads(r.post_data or "{}")) if r.method == "POST" and r.url.endswith("/review") else None)
    open_case(page, lib11)
    _accept_the_listed_charge(page, lib11)
    # Cancel sends nothing and counts nothing
    row = _row(page, amounts["$250.00"]); row.scroll_into_view_if_needed()
    row.get_by_test_id("btn-count-charge").click()
    dlg = page.get_by_test_id("count-confirm"); expect(dlg).to_be_visible()
    expect(dlg.get_by_test_id("count-confirm-amount")).to_contain_text("$250.00")
    expect(dlg.get_by_test_id("count-confirm-reason")).to_contain_text("no date of service")
    expect(dlg.get_by_test_id("btn-count-confirm")).to_have_text(NAMED)
    dlg.get_by_test_id("btn-count-cancel").click(); expect(dlg).to_be_hidden()
    assert not [p for p in posts if p.get("action") == "count"]
    expect(page.get_by_test_id("accepted-total")).to_contain_text("$3,260.00")
    for text in COUNTABLE:
        _count_with_mouse(page, amounts[text])
    expect(page.get_by_test_id("accepted-total")).to_contain_text("$6,000.00")
    assert [p for p in posts if p.get("action") == "count"] == [{"action": "count", "confirm": "separate_charge"}] * 3
    # a counted line is now one of the detected charges, in the charges table, and no longer in the not-counted list
    for text in COUNTABLE:
        r = _row(page, amounts[text])
        assert r.locator("xpath=ancestor::table[1]").get_attribute("data-group") == "charges"
        expect(r.get_by_test_id("btn-count-charge")).to_have_count(0); expect(r.get_by_test_id("not-counted-reason")).to_have_count(0)
    assert page.get_by_test_id("unclear-tray").get_by_test_id("btn-count-charge").count() == 0
    # the balance and the other rule-excluded lines are unchanged, and the server agrees
    for text in EXCLUDED:
        expect(_row(page, amounts[text]).get_by_test_id("not-counted-reason")).to_have_count(1)
    st = api("GET", f"/api/cases/{lib11}")[1]
    assert st["totals"]["accepted"]["cents"] == 600000
    open_case(page, lib11)                                                              # and it survives a reload
    expect(page.get_by_test_id("accepted-total")).to_contain_text("$6,000.00")


def test_counting_works_by_keyboard_alone(page, lib11):
    amounts = _by_text(lib11); a = amounts["$250.00"]
    open_case(page, lib11)
    row = _row(page, a); row.scroll_into_view_if_needed()
    btn = row.get_by_test_id("btn-count-charge")
    btn.focus(); expect(btn).to_be_focused()
    expect(btn).to_have_attribute("aria-label", re.compile(r"Count this charge.*\$250\.00"))
    page.keyboard.press("Enter")
    dlg = page.get_by_test_id("count-confirm"); expect(dlg).to_be_visible()
    expect(dlg.get_by_test_id("btn-count-cancel")).to_be_focused()                      # the safe answer has focus: Enter alone counts nothing
    page.keyboard.press("Escape"); expect(dlg).to_be_hidden()
    expect(btn).to_be_focused()                                                         # focus returns to the action she used
    assert _by_text(lib11)["$250.00"]["kind"] != "charge"
    page.keyboard.press("Enter"); expect(dlg).to_be_visible()
    page.keyboard.press("Tab"); expect(dlg.get_by_test_id("btn-count-confirm")).to_be_focused()
    page.keyboard.press("Enter"); expect(dlg).to_be_hidden()
    expect(_row(page, a)).to_have_attribute("data-review", "accepted")
    expect(_row(page, a)).to_be_focused()                                               # focus follows the line to its new place in the charges table
    assert _by_text(lib11)["$250.00"]["kind"] == "charge"


def test_a_rule_excluded_line_cannot_be_counted_even_from_the_keyboard(page, lib11):
    """No count control exists on a balance line, so nothing is tabbable that counts it; and the page never sends `count` for it."""
    amounts = _by_text(lib11); bal = amounts["$2,166.00"]
    posts = []
    page.on("request", lambda r: posts.append(json.loads(r.post_data or "{}")) if r.method == "POST" and r.url.endswith("/review") else None)
    open_case(page, lib11)
    row = _row(page, bal); row.scroll_into_view_if_needed()
    expect(row.get_by_test_id("not-counted-reason")).to_contain_text("Balance or amount due")
    assert row.locator("button").filter(has_text=re.compile(r"count", re.I)).count() == 0
    row.focus()
    for key in ("a", "c", "Enter"):
        page.keyboard.press(key)
    assert not [p for p in posts if p.get("action") == "count"]
    assert api("GET", f"/api/cases/{lib11}")[1]["totals"]["accepted"]["cents"] != 600000


def test_reasons_and_counting_fit_a_390px_screen(pw, lib11):
    amounts = _by_text(lib11); a = amounts["$180.00"]
    b = pw.chromium.launch()
    try:
        pg = b.new_context(viewport={"width": 390, "height": 844}).new_page()
        open_case(pg, lib11)
        row = _row(pg, a); row.scroll_into_view_if_needed()
        expect(row.get_by_test_id("not-counted-reason")).to_be_visible()
        btn = row.get_by_test_id("btn-count-charge"); expect(btn).to_be_visible()
        bb = btn.bounding_box(); assert bb["x"] >= 0 and bb["x"] + bb["width"] <= 390 and bb["height"] >= 36, bb
        for text in EXCLUDED:
            r = _row(pg, amounts[text]); r.scroll_into_view_if_needed()
            rb = r.get_by_test_id("not-counted-reason").bounding_box(); assert rb["x"] >= 0 and rb["x"] + rb["width"] <= 390, text
        assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        row.scroll_into_view_if_needed(); btn.click()
        dlg = pg.get_by_test_id("count-confirm"); expect(dlg).to_be_visible()
        for t in ("btn-count-confirm", "btn-count-cancel"):
            x = dlg.get_by_test_id(t).bounding_box(); assert x["x"] >= 0 and x["x"] + x["width"] <= 390 and x["height"] >= 36 and x["y"] + x["height"] <= 844, (t, x)
        assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        dlg.get_by_test_id("btn-count-confirm").click(); expect(dlg).to_be_hidden()
        expect(_row(pg, a)).to_have_attribute("data-amount-kind", "charge")
        assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    finally:
        b.close()


def test_a_server_refusal_is_shown_in_its_own_words_and_nothing_changes(page, lib11):
    a = _by_text(lib11)["$250.00"]
    msg = "This amount cannot be counted. Payment: money received, not a charge."
    page.route(re.compile(r"/items/[^/]+/review$"), lambda route: route.fulfill(status=422, content_type="application/json", body=json.dumps(
        {"error": {"code": "NOT_COUNTABLE", "message": msg, "detail": {"item_id": a["id"], "reason_code": "NOT_COUNTABLE", "not_counted_reason": "Payment: money received, not a charge."}}}))
        if json.loads(route.request.post_data or "{}").get("action") == "count" else route.continue_())
    open_case(page, lib11)
    row = _row(page, a); row.scroll_into_view_if_needed()
    row.get_by_test_id("btn-count-charge").click()
    page.get_by_test_id("btn-count-confirm").click()
    expect(row.get_by_test_id("count-error")).to_contain_text("money received, not a charge")
    expect(_row(page, a)).to_have_attribute("data-amount-kind", "unclear")


def test_a_line_that_would_double_another_charge_asks_for_the_flag_by_name(page, lib11):
    """CONFIRM_REQUIRED naming likely_duplicate: the same flag confirm as a flagged charge opens, and the retry carries confirm_flag."""
    a = _by_text(lib11)["$180.00"]
    posts = []
    flag_msg = "Same date, service and amount as another charge. Counting both would count it twice."

    def handler(route):
        body = json.loads(route.request.post_data or "{}")
        if body.get("action") != "count":
            return route.continue_()
        posts.append(body)
        if "confirm_flag" not in body:
            return route.fulfill(status=422, content_type="application/json", body=json.dumps({"error": {"code": "CONFIRM_REQUIRED", "message": "Likely duplicate: " + flag_msg,
                "detail": {"item_id": a["id"], "reason_code": "CONFIRM_REQUIRED", "flag": "likely_duplicate", "name": "Likely duplicate", "confirm_with": "likely_duplicate", "of": "a1", "message": flag_msg}}}))
        route.continue_()
    page.route(re.compile(r"/items/[^/]+/review$"), handler)
    open_case(page, lib11)
    row = _row(page, a); row.scroll_into_view_if_needed()
    row.get_by_test_id("btn-count-charge").click()
    page.get_by_test_id("btn-count-confirm").click()
    dlg = page.get_by_test_id("charge-confirm"); expect(dlg).to_be_visible()
    expect(dlg.get_by_test_id("charge-confirm-flag")).to_have_text("Likely duplicate")
    expect(dlg.get_by_test_id("charge-confirm-msg")).to_contain_text("Counting both")
    assert len(posts) == 1                                                              # nothing counted yet
    dlg.get_by_test_id("btn-charge-confirm").click()
    expect(_row(page, a)).to_have_attribute("data-amount-kind", "charge")
    assert posts[-1] == {"action": "count", "confirm": "separate_charge", "confirm_flag": "likely_duplicate"}


def test_the_reason_line_is_on_the_rows_of_the_other_not_counted_kinds_too(page):
    """Rates, estimates and damages figures carry the code's sentence as well (no count action: they are rule-excluded)."""
    st, c = api("POST", "/api/cases", {"sample": True})
    if st not in (200, 201):
        pytest.skip("sample case unavailable")
    tok = c["token"]
    try:
        assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
        for _ in range(300):
            s = api("GET", f"/api/cases/{tok}/status")[1]
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(.5)
        assert s["status"] == "ready"
        amts = [a for a in api("GET", f"/api/cases/{tok}")[1]["amounts"] if a["kind"] != "charge" and a.get("not_counted_reason")]
        assert amts
        open_case(page, tok)
        for a in amts:
            row = _row(page, a); row.scroll_into_view_if_needed()
            expect(row.get_by_test_id("not-counted-reason")).to_contain_text(a["not_counted_reason"][:40])
            if not a["countable"]:
                expect(row.get_by_test_id("btn-count-charge")).to_have_count(0)
    finally:
        api("DELETE", f"/api/cases/{tok}")

