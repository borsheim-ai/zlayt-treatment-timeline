"""T-141 r7 (F1, staff-engineer blocker): a labelled plural history list that names a date on or after the stated accident date in a two-digit-year form
('1/3/26', '1-3-26', 'Jan 3, 26', '1/26') is the accident, not history: conflict. Years before the stated year, and four-digit variants, behave as before.
Case: stated accident date 2026-01-03 (so '1/3/26' is the accident date itself)."""
import pytest

from app.backend import conflicts as C

LABEL = "History per patient: car accidents in 2019 and 2022, "


def classify(ex):
    r = [dict(n=1, date_iso="2026-01-02", source="PCP", excerpt=ex, kind="encounter"),
         dict(n=2, date_iso="2026-01-12", source="PT", excerpt="Exam: ok.", kind="encounter"),
         dict(n=3, date_iso="2026-01-20", source="Intake", excerpt="Date of accident per intake form: 2026-01-03.", kind="encounter")]
    if C.accident_date_conflicts(r):
        return "conflict"
    return "info" if C.accident_date_note(r) else "none"


ON_OR_AFTER = [   # the reviewer's Q19 and its date-form class, plus 4-digit variants
    "one on 1/3/26.", "one on 01/03/26.", "one on 1-3-26.", "one on 03-01-26.", "one on 3/1/26.", "one on 01.03.26.", "one on Jan 3, 26.", "one on 3rd Jan 26.",
    "one on 1/26.", "one on 3/27/26.", "one on 1/3/2026.", "one on 01/03/2026.", "one on 03-01-2026.", "one on Jan 3, 2026.", "one in 2026.",
]
BEFORE = ["one in 2015.", "one on 1/3/15.", "one on 01-03-15.", "one on 1/3/25.", "one on Jan 3, 25.", "one on 3rd Jan 25.", "one on 12/25.", "one on 1/3/2015."]


@pytest.mark.parametrize("tail", ON_OR_AFTER)
def test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict(tail):
    assert classify(LABEL + tail) == "conflict", tail


@pytest.mark.parametrize("tail", BEFORE)
def test_dates_before_the_accident_year_stay_history(tail):
    assert classify(LABEL + tail) == "info", tail


def test_reviewer_blocker_case_q19():
    assert classify("History per patient: car accidents in 2019 and 2022, one on 1/3/26.") == "conflict"


def test_blood_pressure_is_not_a_date():
    assert classify("History per patient: car accidents in 2019 and 2022, BP 120/80.") == "info"
