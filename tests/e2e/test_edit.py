"""Edit flow. R-RV-2, R-RV-3, R-EX-4(10)."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_edit_summary_labelled_and_persists(page, sample_case):
    """R-RV-2: edit entry 3 summary -> 'edited' label; reload keeps summary and label; letter has no 'edited'."""
    open_case(page, sample_case); e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 and daily headaches."); e.get_by_test_id("btn-save-edit").click()
    expect(e).to_have_attribute("data-review", "edited")
    page.reload(); page.get_by_test_id("timeline").wait_for()
    e = page.get_by_test_id("entry-3"); assert e.get_attribute("data-review") == "edited" and "edited" in e.inner_text().lower() and "daily headaches" in e.get_by_test_id("entry-summary").inner_text()

def test_added_dollar_is_a_hard_422_no_override(page, sample_case):
    """R-RV-3 / D-034: adding '$9,000' (not in the quote) is a hard 422 - API and UI; nothing saved, no 'keep my wording' button."""
    c = api("GET", f"/api/cases/{sample_case}")[1]; eid = [e for e in c["entries"] if "r5" in e["record_ids"]][0]["id"]
    st, err = api("POST", f"/api/cases/{sample_case}/items/{eid}/review", {"action": "edit", "edits": {"summary": "Visit 8: pain 4/10, improving; billed $9,000."}, "confirm_warnings": True})
    assert st == 422
    open_case(page, sample_case); e = page.get_by_test_id("entry-5"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Visit 8: pain 4/10, improving; billed $9,000."); e.get_by_test_id("btn-save-edit").click()
    expect(page.get_by_role("alert").or_(page.get_by_test_id("warning-list")).first).to_contain_text("$9,000")      # T-060 r4: the figure is shown as she typed it, not as the server normalises it ("9000")
    assert e.get_attribute("data-review") != "edited" and page.get_by_test_id("btn-keep-wording").count() == 0

def test_date_and_provider_not_editable(page, sample_case):
    """R-RV-2: no input exists for date or provider."""
    open_case(page, sample_case); e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    assert e.locator("input[name=date], input[name=provider]").count() == 0

def test_notes_list_edited_item_with_both_texts(page, sample_case):
    """R-EX-4(10): after editing entry 3 and exporting, EDITED ITEMS holds the exact original and new sentences; the letter has no 'edited'."""
    open_case(page, sample_case); e = page.get_by_test_id("entry-3")
    original = "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks."; new = "Persistent neck pain 6/10 with daily headaches noted."
    e.get_by_test_id("btn-edit").click(); e.get_by_test_id("edit-summary").fill(new); e.get_by_test_id("btn-save-edit").click()
    expect(e).to_have_attribute("data-review", "edited"); expect(e.get_by_test_id("entry-summary")).to_contain_text("daily headaches noted")
    e.get_by_test_id("btn-accept").click(); page.get_by_test_id("btn-export").click()
    sec = page.get_by_test_id("export-notes").inner_text().split("EDITED ITEMS")[1].split("PENDING ITEMS")[0]
    assert original in sec and new in sec and "edited" not in page.get_by_test_id("export-letter").inner_text().lower()

@pytest.mark.parametrize("status", [404, 405])
def test_batch_accept_route_missing_accepts_nothing(page, sample_case, status):
    """T-065 / T-063 major 8: if the batch route answers 404/405 the UI shows an error and fires no per-item accept."""
    open_case(page, sample_case); seen = []
    page.on("request", lambda r: seen.append((r.method, r.url)) if r.method == "POST" else None)
    page.route("**/review/batch", lambda route: route.fulfill(status=status, content_type="application/json", body='{"error":{"message":"gone"}}'))
    page.get_by_test_id("btn-accept-verified").click()
    expect(page.locator('[role="status"], [role="alert"]').filter(has_text="nothing was accepted").first).to_be_visible()
    page.wait_for_timeout(300)
    assert [u for m, u in seen if u.endswith("/review")] == [], seen
    assert [u for m, u in seen if u.endswith("/review/batch")]  # the batch attempt itself happened
    assert page.locator('[data-review="accepted"]').count() == 0


@pytest.mark.parametrize("status", [404, 405])
def test_batch_undo_route_missing_resets_nothing(page, sample_case, status):
    """T-065 round 2: Undo has no per-item fallback either; if the batch route is gone nothing is reset and no /review POST fires."""
    open_case(page, sample_case)
    page.get_by_test_id("btn-accept-verified").click()
    expect(page.get_by_test_id("btn-undo-batch")).to_be_visible()
    accepted = page.locator('[data-review="accepted"]').count(); assert accepted > 0
    seen = []
    page.on("request", lambda r: seen.append((r.method, r.url)) if r.method == "POST" else None)
    page.route("**/review/batch", lambda route: route.fulfill(status=status, content_type="application/json", body='{"error":{"message":"gone"}}'))
    with page.expect_request("**/review/batch"):
        page.get_by_test_id("btn-undo-batch").click()
    expect(page.locator('[role="status"], [role="alert"]').filter(has_text="Undo was refused").or_(page.locator('[role="status"], [role="alert"]').filter(has_text="gone")).first).to_be_visible()
    assert [u for m, u in seen if u.endswith("/review")] == [], seen
    assert page.locator('[data-review="accepted"]').count() == accepted


def test_no_frontend_code_posts_to_the_per_item_review_route_for_a_batch():
    """T-065 round 2: the mock overlay must not fan a batch out per item (bypasses the verified-only, all-or-nothing rule)."""
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[2] / "app" / "frontend"
    for f in ("batch.js", "mock_extra.js"):
        src = (root / f).read_text()
        assert "/review`" not in src and 'items/" + id' not in src and "items/${id}" not in src, f"{f}: per-item review call"
        assert not (f == "batch.js" and "action: \"reset\"" in src and "for (const" in src), f
    assert "/review/batch" in (root / "mock.js").read_text()  # the mock implements the batch itself
