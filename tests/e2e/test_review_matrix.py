"""Review matrix. R-RV-1, R-RV-4, R-RV-5, R-RV-6, ADR-005."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_decisions_survive_reload(page, sample_case):
    """R-RV-1: accept entry 3, reload -> still accepted."""
    open_case(page, sample_case); page.get_by_test_id("entry-3").get_by_test_id("btn-accept").click(); page.reload()
    page.get_by_test_id("timeline").wait_for(); assert page.get_by_test_id("entry-3").get_attribute("data-review") == "accepted"

def test_nothing_starts_accepted(page, sample_case):
    """R-RV-6/D-011: every item is pending on load; no bulk accept control exists."""
    open_case(page, sample_case)
    assert page.locator("[data-review=accepted]").count() == 0 and page.get_by_role("button", name=re.compile("accept all(?! verified)", re.I)).count() == 0

def test_dismiss_reset_dismiss(page, sample_case):
    """R-RV-5: dismiss, reset, dismiss again works; reset returns to pending."""
    open_case(page, sample_case); e = page.get_by_test_id("entry-5")
    e.get_by_test_id("btn-dismiss").click(); expect(e).to_have_attribute("data-review", "dismissed"); e.get_by_test_id("btn-reset").click(); expect(e).to_have_attribute("data-review", "pending")
    e.get_by_test_id("btn-dismiss").click(); expect(e).to_have_attribute("data-review", "dismissed")

def test_rejected_item_cannot_be_accepted(page, sample_case):
    """ADR-005: rejected items live in the 'could not verify' tray without an accept button."""
    open_case(page, sample_case); tray = page.get_by_test_id("rejected-tray"); assert tray.count() == 1 and page.get_by_test_id("entry-1").get_by_test_id("btn-accept").count() == 1 and tray.get_by_test_id("btn-accept").count() == 0

def test_injection_case_shows_warning_and_pending(page):
    """R-RV-6 (D-005): case_07 shows the INJECTION warning and no flag is resolved."""
    page.goto(BASE); page.get_by_test_id("input-text").fill(golden_text("case_07_prompt_injection.txt")); page.get_by_test_id("btn-analyze").click()
    page.get_by_test_id("timeline").wait_for(timeout=120000)
    assert "instruction" in page.get_by_test_id("flags-panel").inner_text().lower() and page.locator("[data-review=accepted]").count() == 0
