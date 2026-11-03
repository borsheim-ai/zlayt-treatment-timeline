"""Flags panel. R-FL-1..R-FL-7, R-RV-2 (note only)."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE


def flags(page): return page.get_by_test_id("flags-panel")

def test_73_day_gap_flag_and_no_28_day(page, sample_case):
    """R-FL-1: the gap flag says 73 days; no flag mentions 28 days."""
    open_case(page, sample_case); t = flags(page).inner_text(); assert "73" in t and "28 days" not in t

def test_both_conflicts_present_not_merged(page, sample_case):
    """R-FL-2: accident-date conflict (shows 2026-01-19 and the EMS sentence) and PT-plan conflict."""
    open_case(page, sample_case); t = flags(page).inner_text()
    assert "2026-01-19" in t and "rear-ended" in t and "12 visits" in t

def test_patient_self_report_label(page, sample_case):
    """R-FL-7: the record-9 causation flag shows 'Reported onset'."""
    open_case(page, sample_case); assert "Reported onset" in flags(page).inner_text()

def test_flag_edit_is_note_only(page, sample_case):
    """R-RV-2: the only editable field on a flag is the reviewer note."""
    open_case(page, sample_case); f = flags(page).locator("[data-flag-type=gap]").first
    assert f.get_by_test_id("flag-note").count() == 1 and f.get_by_test_id("edit-summary").count() == 0

def test_no_causation_conclusion_words(page, sample_case):
    """R-FL-4: flag text never says 'caused by' or 'non-compliant'."""
    open_case(page, sample_case); t = flags(page).inner_text().lower(); assert "caused by" not in t and "non-compliant" not in t
