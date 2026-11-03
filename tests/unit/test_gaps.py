"""Treatment gaps (code). R-FL-1, LLM_VS_CODE row 9; golden gap_table of every case."""
import pytest
from app.backend import gaps as GP
from tests.unit import _golden as G

def recs(case):
    """The golden gap_table is the VISIT-ONLY reading (non-encounter records left out): it is the alternative number the product shows beside a counted
    gap that a paperwork-looking record changes (D-055, T-116 round 4). The counted math over every dated record is in test_t116_r4_all_dated_records.py."""
    return [dict(n=r["record_no"], date_iso=r["date"], kind=r["kind"]) for r in G.expected(case)["records"] if r["kind"] == "encounter"]

@pytest.mark.parametrize("case", G.case_names())
def test_gap_table_matches_golden(case):
    """R-FL-1: for every golden case the computed intervals (dates, record lists, days, flag) equal gap_table."""
    got = GP.compute_gaps(recs(case))
    want = G.expected(case)["gap_table"]
    assert [(g["from_date"], g["to_date"], g["days"], g["flag"]) for g in got] == [(w["from_date"], w["to_date"], w["days"], w["flag"]) for w in want]
    assert [(g["from_records"], g["to_records"]) for g in got] == [(w["from_records"], w["to_records"]) for w in want]

@pytest.mark.parametrize("days,flag", [(28, False), (29, False), (30, False), (31, True), (73, True)])
def test_threshold_is_strictly_greater_than_30(days, flag):
    """R-FL-1 (A-104): 29 and 30 do not flag, 31 does."""
    assert GP.is_gap(days) is flag

def test_sample_73_day_flag_and_28_day_near_miss():
    """R-FL-1: sample flags 2026-03-06 -> 2026-05-18 (73) and not 2026-01-23 -> 2026-02-20 (28)."""
    flagged = [(g["from_date"], g["to_date"], g["days"]) for g in GP.compute_gaps(recs("sample")) if g["flag"]]
    assert flagged == [("2026-03-06", "2026-05-18", 73)]

def test_leap_year_case_02_three_flags_four_near_misses():
    """R-FL-1: case_02 (2028 leap) -> 3 flags (31 days), 4 intervals of 29/30."""
    g = GP.compute_gaps(recs("case_02_gap_boundaries"))
    assert sum(x["flag"] for x in g) == 3 and sum(not x["flag"] for x in g) == 4

def test_non_encounter_records_never_endpoints():
    """R-FL-1 (D-003, read through D-055): over the visit-only reading case_09's billing statement + phone note do not split the 56-day gap. The product counts
    them (27, 11 and 18 days) and shows the 56-day span as a conditional flag with both numbers (test_t116_r4_all_dated_records.py)."""
    g = GP.compute_gaps(recs("case_09_nonvisit_hides_gap"))
    assert (g[0]["from_date"], g[0]["to_date"], g[0]["days"], g[0]["flag"]) == ("2026-02-02", "2026-03-30", 56, True)

def test_undated_and_ambiguous_excluded_until_confirmed():
    """R-IN-5: a record with date None is excluded; recomputing after confirm_date (date set) includes it."""
    base = [dict(n=1, date_iso="2026-01-01", kind="encounter"), dict(n=2, date_iso=None, kind="encounter"), dict(n=3, date_iso="2026-01-20", kind="encounter")]
    assert [(g["days"]) for g in GP.compute_gaps(base)] == [19]
    base[1]["date_iso"] = "2026-02-25"
    assert [(g["days"], g["flag"]) for g in GP.compute_gaps(base)] == [(19, False), (36, True)]
    assert [(g["from_date"], g["to_date"]) for g in GP.compute_gaps(base)] == [("2026-01-01", "2026-01-20"), ("2026-01-20", "2026-02-25")]

def test_dropping_an_entry_never_changes_gaps():
    """R-FL-1 / arch invariant: gap math reads record dates only, so the same input gives identical output."""
    r = recs("sample")
    assert GP.compute_gaps(r) == GP.compute_gaps(list(r))

def test_same_day_records_make_one_date():
    """R-FL-1 / A-108: records 1 and 2 (both 2026-01-09) are one date point; first interval is 7 days."""
    g = GP.compute_gaps(recs("sample"))
    assert g[0]["from_records"] == [1, 2] and g[0]["days"] == 7
