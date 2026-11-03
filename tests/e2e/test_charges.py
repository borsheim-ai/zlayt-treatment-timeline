"""Charges panel. R-CH-1..R-CH-5, R-CH-7."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_three_amounts_listed_185_is_rate(page, sample_case):
    """R-CH-1/R-CH-2: $6,240, $2,150, $185 listed; $185 is a rate in the unclear tray."""
    open_case(page, sample_case); p = page.get_by_test_id("charges-panel").inner_text()
    assert "$6,240" in p and "$2,150" in p and "$185" in p and "$185" in page.get_by_test_id("unclear-tray").inner_text()

def test_accepting_both_charges_totals_8390(page, sample_case):
    """R-CH-3: Accepted charges: $8,390 after accepting the two charges; $185 never added."""
    open_case(page, sample_case)
    for raw in ("$6,240", "$2,150"): page.get_by_test_id(f"amount-{raw}").get_by_test_id("btn-accept").click()
    expect(page.get_by_test_id("accepted-total")).to_contain_text("$8,390")

def test_dismissing_er_drops_total(page, sample_case):
    """R-CH-3: dismiss ER charge -> $2,150."""
    open_case(page, sample_case)
    page.get_by_test_id("amount-$6,240").get_by_test_id("btn-dismiss").click(); page.get_by_test_id("amount-$2,150").get_by_test_id("btn-accept").click()
    expect(page.get_by_test_id("accepted-total")).to_contain_text("$2,150")

def test_rate_has_no_edit_path(page, sample_case):
    """R-CH-7: the rate row offers accept/dismiss only - no edit control."""
    open_case(page, sample_case); row = page.get_by_test_id("amount-$185"); assert row.is_visible() and row.get_by_test_id("btn-accept").count() == 1 and row.get_by_test_id("btn-edit").count() == 0

def test_pending_detected_is_labelled_not_a_total(page, sample_case):
    """R-CH-3: 'Detected, not yet accepted' is shown separately."""
    open_case(page, sample_case); assert "not yet accepted" in page.get_by_test_id("pending-total").inner_text().lower()
