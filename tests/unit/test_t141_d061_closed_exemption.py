"""T-141 r6 / D-061: a record dated before the stated accident date is info-only ONLY when every accident or mechanism word in it is governed by an explicit
prior / previous / earlier, or by a negation of prior accidents. Any other accident or mechanism word, noun or verb, with or without a date or 'last year', is
a date conflict. No date-distance exemption. The reviewer's r5 probes (artifacts/review-evidence/T-141-r5/r5_probe.py, r5_probe2.py) are the cases."""
import pytest

from app.backend import conflicts as C


def R(n, d, src, ex):
    return dict(n=n, date_iso=d, source=src, excerpt=ex, kind="encounter")


def recs(ex, src="ER"):
    return [R(1, "2026-01-05", src, ex), R(2, "2026-01-12", "PT", "Exam: ok."), R(3, "2026-01-20", "Intake", "Date of accident per intake form: 2026-01-09.")]


@pytest.mark.parametrize("ex", [
    "Rear-end collision in October 2025.", "MVC in October 2025.", "MVA in October 2025.", "Collision in October 2025.", "Crash in October 2025.",
    "Involved in an MVA in October 2025.", "Rear-end collision, driver restrained, October 2025.", "Airbag deployed in October 2025.", "Rear-ended last year.",
    "Rear-ended in October 2025.", "Rear-ended in November 2025.", "Rear-ended 03/14/2024, resolved.", "Rear-ended in 2021, resolved.", "Was rear-ended in March 2025, resolved.",
    "Rear-end collision 03/14/2024, resolved.", "Car accident last year, fully recovered.", "Car accident in March 2025, resolved.", "MVA in 2015, resolved.",
    "MVA on 03/04/2024, resolved.", "Reports a car accident years ago.", "Accident in October 2025.", "Struck by a car last year.", "Hit by a car as a child.",
    "Injured in October 2025.", "Injury in October 2025.", "LOC in October 2025.", "Whiplash in October 2025.", "Pedestrian struck in 2022.", "Impact to the left side last year.",
    "History: MVC.", "History of MVC 2018.", "Hx rear-end collision 2018.", "Old MVC, resolved.", "MVA remote past, resolved.", "Past accident, resolved.",
])
def test_every_date_or_relative_time_exemption_is_gone(ex):
    out = C.accident_date_conflicts(recs(f"Annual physical. {ex}"))
    assert len(out) == 1, ex
    assert C.accident_date_note(recs(f"Annual physical. {ex}")) is None


@pytest.mark.parametrize("ex", [
    "No prior accidents.", "Denies previous MVA.", "Prior accidents: No.", "Denies any accidents or injuries.", "No history of prior injury.", "Negative for whiplash.",
    "Previous accident with whiplash.", "Prior MVA with head injury.", "Previously had an MVA.", "Prior MVC in October 2025.", "Prior rear-end collision, resolved.",
    "Previous rear-ended episode.", "Earlier MVA, resolved.", "Denies MVC.", "Without trauma.", "Neg for injuries.", "Prior accident, resolved.",
])
def test_the_one_closed_exemption_explicit_prior_or_a_negation_of_prior_accidents(ex):
    r = recs(f"Annual physical. {ex}")
    assert C.accident_date_conflicts(r) == [], ex
    assert C.accident_date_note(r)["count"] == 1


@pytest.mark.parametrize("ex", [
    "Prior accidents: No. Rear-ended in October 2025.", "No prior accidents; rear-end collision in October 2025.", "Prior MVA, resolved. Collision in October 2025.",
    "Denies previous MVA. MVC last year.", "No prior accidents. Was in a crash.",
])
def test_one_ungoverned_word_anywhere_in_the_record_makes_it_a_conflict(ex):
    assert len(C.accident_date_conflicts(recs(f"Annual physical. {ex}"))) == 1, ex


def _lib11_records():
    import re
    from pathlib import Path
    txt = Path("evals/library/case_lib11_priors_and_ledger.txt").read_text(encoding="utf-8")
    out = []
    for i, blk in enumerate(re.split(r"=== Record \d+ ===", txt)[1:], 1):
        d = re.search(r"Date:\s*(.+)", blk).group(1).strip()
        out.append(dict(n=i, date_iso=d if re.fullmatch(r"\d{4}-\d\d-\d\d", d) else None, source=re.search(r"Source:\s*(.+)", blk).group(1).strip(),
                        excerpt=re.search(r'Excerpt:\s*"(.*?)"\s*$', blk, re.S | re.M).group(1), kind="encounter"))
    return out


def test_lib11_is_unchanged_no_accident_date_conflict():
    records = _lib11_records()
    assert C.stated_accident_dates(records), "the stated date must be found or the check is vacuous"
    assert C.accident_date_conflicts(records) == []


@pytest.mark.parametrize("ex,expected", [
    ("History per patient: car accidents in 2019 and 2022 with neck pain.", 0), ("History per patient: MVAs in 2019 and 2022.", 0),
    ("History per patient: car accident in 2022.", 1), ("History: MVC.", 1), ("History: rear-ended at a stoplight.", 1), ("Hx: the accident.", 1),
    ("History per patient: car accidents in 2019; rear-ended in October 2025.", 1), ("Reports car accidents in 2019 and 2022.", 1),
])
def test_a_plural_event_list_under_a_history_label_is_the_one_added_shape_lib11_needs(ex, expected):
    """The only exemption beyond D-061's wording, needed because lib11 (unchanged) lists past accidents under 'History per patient:'. A singular event stays a conflict."""
    assert len(C.accident_date_conflicts(recs(f"Annual visit. {ex}", "PCP"))) == expected, ex
