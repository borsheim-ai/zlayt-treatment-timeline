"""Input screen. R-IN-1, R-IN-2, R-IN-3, R-IN-5, R-ST (synthetic banner)."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_synthetic_banner_always_visible(page):
    """CLAUDE.md data rule: the persistent 'synthetic data only' banner is on the first screen."""
    page.goto(BASE); assert page.get_by_test_id("banner-synthetic").is_visible()

def test_load_sample_shows_nine_records_before_any_model_call(page):
    """R-IN-1 (row 1): 'N records found' appears right after ingest; the record count is 9."""
    page.goto(BASE); page.get_by_test_id("btn-sample").click()
    assert "9" in page.get_by_test_id("record-count").inner_text()

def test_pdf_upload_refused_with_plain_message(page, tmp_path):
    """R-IN-2: a .pdf upload is refused with a plain message, not a crash."""
    f = tmp_path / "x.pdf"; f.write_bytes(b"%PDF-1.4 fake")
    page.goto(BASE); page.get_by_test_id("file-input").set_input_files(str(f))
    assert page.get_by_role("alert").is_visible()

def test_txt_upload_equals_paste(page, tmp_path):
    """R-IN-2: uploading evals/golden/sample.txt gives the same nine records as paste."""
    f = tmp_path / "s.txt"; f.write_text(golden_text("sample.txt"))
    page.goto(BASE); page.get_by_test_id("file-input").set_input_files(str(f))
    assert "9" in page.get_by_test_id("record-count").inner_text()

def _confirm(scope, date):
    """T-096: case_01's ambiguous date has a code suggestion, so the readings are radios and one explicit Confirm click is required."""
    scope.locator(f'[data-testid="confirm-date"][data-date="{date}"]').check(); scope.get_by_test_id("btn-confirm-date").click()

def _analyze_case_01(page):
    page.goto(BASE); page.get_by_test_id("input-text").fill(golden_text("case_01_date_formats.txt")); page.get_by_test_id("btn-analyze").click()
    expect(page.get_by_test_id("dates-to-confirm")).to_contain_text("04/05/2026", timeout=120000)

def test_ambiguous_date_goes_to_dates_to_confirm(page):
    """R-IN-3/R-IN-5, undated-entry branch (T-068): case_01 record 8 (04/05/2026) has an undated entry. It is listed ONCE, in
    'Dates to confirm', with both readings and its verbatim excerpt; confirming it moves the entry onto the timeline."""
    _analyze_case_01(page)
    box = page.get_by_test_id("dates-to-confirm")
    assert page.get_by_test_id("date-to-confirm-item").count() == 0, "this case has an undated entry, so the no-entry row must not render"
    expect(box.get_by_test_id("confirm-date")).to_have_count(2)
    expect(box.get_by_test_id("entry-excerpt")).to_contain_text("Patient reports no new symptoms.")
    expect(page.locator('[data-testid="missing-entry"][data-record-id="r8"]')).to_have_count(0)   # not listed twice
    _confirm(box, "2026-04-05")
    expect(box).to_contain_text("None. Every record has a readable date.")
    expect(page.get_by_test_id("queue").locator('[data-testid=entry-date][datetime="2026-04-05"]')).to_have_count(1)

def test_confirming_a_date_with_no_entry_keeps_the_record_visible(page):
    """T-068 round 2 (orphan branch, forced: the case response is rewritten so record 8 has no entry anywhere). The row shows the
    verbatim excerpt, offers both dates and Open record; confirming does NOT make the record vanish: it moves to
    'Records without an entry' with the confirmed date and the by-hand entry control. The record is listed once at every step."""
    def strip_r8(route):
        r = route.fetch(); body = r.json()
        for k in ("entries", "undated_entries", "tray"):
            body[k] = [x for x in body.get(k, []) if "r8" not in x.get("record_ids", [])]
        route.fulfill(response=r, json=body)
    page.route(re.compile(r"/api/cases/[^/?]+$"), lambda route: strip_r8(route) if route.request.method == "GET" else route.continue_())
    _analyze_case_01(page)
    row = page.locator('[data-testid="date-to-confirm-item"][data-record-id="r8"]')
    expect(row).to_have_count(1)
    expect(row.get_by_test_id("date-to-confirm-excerpt")).to_have_text("Patient reports no new symptoms.")
    expect(row.get_by_test_id("confirm-date")).to_have_count(2)
    expect(page.locator('[data-testid="missing-entry"][data-record-id="r8"]')).to_have_count(0)   # not listed twice before confirming
    row.get_by_test_id("btn-source").click()
    expect(page.get_by_test_id("record-modal")).to_contain_text("Patient reports no new symptoms.")
    page.keyboard.press("Escape")
    _confirm(row, "2026-04-05")
    expect(page.get_by_test_id("date-to-confirm-item")).to_have_count(0)
    left = page.locator('[data-testid="missing-entry"][data-record-id="r8"]')
    expect(left).to_have_count(1)
    expect(left.get_by_test_id("missing-date-confirmed")).to_contain_text("April 5, 2026")
    expect(left.get_by_test_id("btn-manual-entry")).to_be_visible()
    expect(left.get_by_test_id("missing-entry-excerpt")).to_have_text("Patient reports no new symptoms.")   # the quote stays on the card she acts on (T-068 r3)

def test_undated_row_shows_record_number(page):
    """T-068 r3 (paralegal N2): the undated entry in Dates to confirm names its record and its Open button carries the number."""
    _analyze_case_01(page)
    row = page.get_by_test_id("dates-to-confirm").locator('[data-testid^="entry-"][data-item-id]').first
    expect(row.get_by_test_id("entry-provider")).to_contain_text("Record 8:")
    expect(row.get_by_test_id("btn-source")).to_have_text("Open record 8")

def test_undated_entry_cannot_be_accepted_until_date_confirmed(page):
    """T-068 r3 / D-041: on an undated entry Accept is disabled with the visible reason 'Confirm the date first' and a link to the date choices;
    the keyboard shortcut and 'Accept all verified' do not accept it (the batch says how many it skipped); the letter never says 'date not stated';
    after the date is confirmed Accept is enabled."""
    _analyze_case_01(page)
    box = page.get_by_test_id("dates-to-confirm")
    row = box.locator('[data-testid^="entry-"][data-item-id]').first
    expect(row.get_by_test_id("btn-accept")).to_be_disabled()
    expect(row.get_by_test_id("accept-blocked-reason")).to_contain_text("Confirm the date first")
    row.get_by_test_id("link-confirm-date").click()
    expect(row.get_by_test_id("confirm-date").first).to_be_focused()
    page.keyboard.press("a")
    expect(row).to_have_attribute("data-review", "pending")
    expect(page.get_by_test_id("batch-skipped-note")).to_contain_text("1 undated entry was skipped")
    page.get_by_test_id("btn-accept-verified").click()
    expect(row).to_have_attribute("data-review", "pending")
    expect(page.locator('#rv-live')).to_contain_text("1 undated entry was skipped")
    page.get_by_test_id("btn-export").click()
    expect(page.get_by_test_id("export-letter")).not_to_contain_text("date not stated")
    page.keyboard.press("Escape")
    _confirm(box, "2026-04-05")
    entry = page.get_by_test_id("queue").locator('[data-testid^="entry-"][data-item-id]').filter(has=page.locator('time[datetime="2026-04-05"]'))
    expect(entry.get_by_test_id("btn-accept")).to_be_enabled()

def test_server_date_unconfirmed_is_explained_in_plain_words(page):
    """T-068 r3: a 422 DATE_UNCONFIRMED from the server (T-076) is shown as a plain sentence, not a raw code."""
    page.route(re.compile(r"/api/cases/[^/]+/items/[^/]+/review$"), lambda route: route.fulfill(status=422, json={"error": {"code": "DATE_UNCONFIRMED", "message": "DATE_UNCONFIRMED"}}))
    _analyze_case_01(page)
    entry = page.get_by_test_id("queue").locator('[data-testid^="entry-"][data-item-id]').first
    entry.get_by_test_id("btn-accept").click()
    expect(entry.locator(".rv-error")).to_contain_text("Confirm the date first")
    expect(entry.locator(".rv-error")).not_to_contain_text("DATE_UNCONFIRMED")
