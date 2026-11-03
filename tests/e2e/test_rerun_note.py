"""T-162 (T-146): a decided item whose re-run disagreed or failed carries `rerun_note` (the message string; null otherwise). It is shown in the item's row and in its 'How this was checked' dialog.
GET case is rewritten to add the note to two decided items (an accepted charge, a dismissed entry) because the fixture backend's re-run never produces one; everything else is the real server.
New test ids (declared in conftest): rerun-note (in the row's controls and inside the trace dialog)."""
import json
import os
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, reveal

LIB = "case_lib06_lop_billed_vs_adjusted"
NOTE = "The re-run gave a different result for this item. Your decision and the earlier result were kept."


@pytest.fixture
def decided():
    st, c = api("POST", "/api/cases", {"library": LIB})
    if st not in (200, 201):
        if os.environ.get("E2E_REQUIRE_DB") == "1":
            pytest.fail("library cases need ZLAYT_MODE=local")
        pytest.skip("library cases need ZLAYT_MODE=local")
    tok = c["token"]
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"
    case = api("GET", f"/api/cases/{tok}")[1]
    charges = [a for a in case["amounts"] if a["kind"] == "charge" and a["review_status"] == "pending" and not a.get("flag")]
    charge, gone_amount = charges[0], charges[1]
    entry = next(e for e in case["entries"] if e["review_status"] == "pending")
    assert api("POST", f"/api/cases/{tok}/items/{charge['id']}/review", {"action": "accept"})[0] == 200
    assert api("POST", f"/api/cases/{tok}/items/{entry['id']}/review", {"action": "dismiss"})[0] == 200
    assert api("POST", f"/api/cases/{tok}/items/{gone_amount['id']}/review", {"action": "dismiss"})[0] == 200
    yield tok, charge["id"], entry["id"], gone_amount["id"]
    api("DELETE", f"/api/cases/{tok}")


def _stub(page, ids):
    def case(route):
        if route.request.method != "GET":
            return route.continue_()
        r = route.fetch(); body = r.json()
        for k in ("entries", "amounts"):
            for it in body.get(k, []):
                if it["id"] in ids:
                    it["rerun_note"] = NOTE
        route.fulfill(response=r, body=json.dumps(body), headers={**r.headers, "content-type": "application/json"})
    page.route(re.compile(r"/api/cases/[^/?]+$"), case)


def test_a_decided_item_shows_its_rerun_note_in_the_row_and_the_trace(page, decided):
    tok, charge, entry, gone_amount = decided
    _stub(page, {charge, entry, gone_amount})
    open_case(page, tok)
    crow = page.get_by_test_id("charges-panel").locator(f'[data-item-id="{charge}"]').first; crow.scroll_into_view_if_needed()
    expect(crow.get_by_test_id("rerun-note")).to_contain_text(NOTE)
    reveal(crow.get_by_test_id("btn-trace")).first.click()
    expect(page.locator("#why-modal").get_by_test_id("rerun-note")).to_contain_text(NOTE)
    page.keyboard.press("Escape")


def test_a_dismissed_items_note_is_hidden_in_the_closed_group_marked_on_it_and_visible_once_opened(page, decided):
    tok, charge, entry, gone_amount = decided
    _stub(page, {entry, gone_amount})
    open_case(page, tok)
    # entries: the closed Dismissed group says one item has a note; the note itself shows when the group is opened
    esum = page.get_by_test_id("dismissed-summary")
    erow = page.get_by_test_id("dismissed-queue").locator(f'[data-item-id="{entry}"]')
    expect(esum.get_by_test_id("rerun-marker")).to_contain_text("1 has a re-run note")
    expect(erow.get_by_test_id("rerun-note")).to_have_count(1)   # the row and its note are in the DOM; only the closed group hides them
    expect(erow.get_by_test_id("rerun-note")).to_be_hidden()
    esum.click()
    expect(erow.get_by_test_id("rerun-note")).to_be_visible()
    expect(erow.get_by_test_id("rerun-note")).to_contain_text(NOTE)
    # amounts: the same in the Charges panel
    asum = page.get_by_test_id("dismissed-summary-amounts")
    arow = page.get_by_test_id("dismissed-amounts").locator(f'[data-item-id="{gone_amount}"]')
    expect(asum.get_by_test_id("rerun-marker")).to_contain_text("1 has a re-run note")
    expect(arow.get_by_test_id("rerun-note")).to_have_count(1)   # the row and its note are in the DOM; only the closed group hides them
    expect(arow.get_by_test_id("rerun-note")).to_be_hidden()
    asum.click()
    expect(arow.get_by_test_id("rerun-note")).to_be_visible()
    expect(arow.get_by_test_id("rerun-note")).to_contain_text(NOTE)
    reveal(arow.get_by_test_id("btn-trace")).first.click()
    expect(page.locator("#why-modal").get_by_test_id("rerun-note")).to_contain_text(NOTE)


def test_an_item_without_a_note_shows_none(page, decided):
    tok, charge, _, _ = decided
    open_case(page, tok)
    crow = page.get_by_test_id("charges-panel").locator(f'[data-item-id="{charge}"]').first; crow.scroll_into_view_if_needed()
    expect(crow.get_by_test_id("rerun-note")).to_have_count(0)
    expect(page.get_by_test_id("rerun-note")).to_have_count(0)
    expect(page.get_by_test_id("rerun-marker")).to_have_count(0)
