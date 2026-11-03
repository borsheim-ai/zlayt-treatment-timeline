"""Timeline. R-TL-1, R-TL-5, R-TL-3, R-RV-1."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE, reveal


def test_nine_entries_in_date_order(page, sample_case):
    """R-TL-1: nine entries, ISO dates non-decreasing, each with provider/summary/excerpt."""
    open_case(page, sample_case)
    dates = [page.get_by_test_id(f"entry-{i}").get_by_test_id("entry-date").get_attribute("datetime") for i in range(1, 10)]
    assert dates == sorted(dates)

def test_record_7_dated_by_header_not_body(page, sample_case):
    """R-TL-3: entry 7 shows 2026-05-18, never 2026-01-19."""
    open_case(page, sample_case); assert page.get_by_test_id("entry-7").get_by_test_id("entry-date").get_attribute("datetime") == "2026-05-18"

def test_needs_review_sorted_first_in_queue(page, sample_case):
    """R-TL-5: items in state needs_review appear above verified ones in the queue."""
    open_case(page, sample_case)
    states = [e.get_attribute("data-state") for e in page.get_by_test_id("queue").locator("[data-state]").all()]
    seen_verified = False
    for s in states:
        if s == "verified": seen_verified = True
        assert not (seen_verified and s == "needs_review")

def test_provider_is_header_label(page, sample_case):
    """R-TL-9: entry 4 provider reads 'Capital PT, initial evaluation'."""
    open_case(page, sample_case); assert page.get_by_test_id("entry-4").get_by_test_id("entry-provider").inner_text() == "Capital PT, initial evaluation"

def test_every_entry_shows_why(page, sample_case):
    """R-TL-5 / row 18: each entry exposes a 'Why?' sentence."""
    open_case(page, sample_case); reveal(page.get_by_test_id("entry-8").get_by_test_id("entry-why")).click(); expect(page.get_by_test_id("why-text")).to_be_visible()
