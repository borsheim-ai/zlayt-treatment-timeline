"""Date parsing (code, explicit format list). R-IN-3, R-TL-3, LLM_VS_CODE row 2; golden case_01."""
import pytest
from app.backend import dates as D
from tests.unit import _golden as G

CASE1 = G.expected("case_01_date_formats")["records"]

@pytest.mark.parametrize("rec", [r for r in CASE1 if r["date"]], ids=lambda r: r["raw_date"])
def test_seven_formats_parse(rec):
    """R-IN-3: ISO, 02/17/2026, 'Feb 24, 2026', '3 March 2026', 'March 10th, 2026', '03-17-26', '3/25/26' parse to the golden ISO date."""
    out = D.parse_date(rec["raw_date"])
    assert out["status"] == "parsed" and out["iso"] == rec["date"]

def test_ambiguous_numeric_date_is_never_guessed():
    """R-IN-3: 04/05/2026 -> ambiguous with both readings; no iso."""
    out = D.parse_date("04/05/2026")
    assert out["status"] == "ambiguous" and out["iso"] is None
    assert sorted(out["candidates"]) == ["2026-04-05", "2026-05-04"]

@pytest.mark.parametrize("raw", ["05/05/2026", "3/25/26", "13/02/2026"])
def test_not_ambiguous_when_equal_or_one_number_exceeds_12(raw):
    """R-IN-3: ambiguous only when the first two numbers are both 1-12 AND differ."""
    assert D.parse_date(raw)["status"] == "parsed"

@pytest.mark.parametrize("raw", ["", "sometime in spring", "2026-13-45", "N/A"])
def test_unreadable_is_missing(raw):
    """R-IN-3 / row 2: unreadable or impossible dates are 'missing', never guessed."""
    out = D.parse_date(raw)
    assert out["status"] == "missing" and out["iso"] is None

def test_dates_inside_body_are_not_the_record_date():
    """R-TL-3: parse_date is applied to the header only; body '2026-01-19' of sample record 7 is a different string than header 2026-05-18."""
    assert D.parse_date(G.record("sample", 7)["date_raw"])["iso"] == "2026-05-18"

@pytest.mark.parametrize("a,b,n", [("2026-01-23", "2026-02-20", 28), ("2026-03-06", "2026-05-18", 73), ("2028-02-08", "2028-03-09", 30), ("2026-02-08", "2026-03-09", 29)])
def test_days_between_real_calendar(a, b, n):
    """R-FL-1 / row 9: calendar-day arithmetic incl. leap February (2028 vs 2026)."""
    assert D.days_between(a, b) == n

def test_golden_header_dates_all_cases():
    """R-TL-3: header date of every golden record parses to the golden ISO (or ambiguous when golden is null)."""
    for c in G.case_names():
        for r in G.expected(c)["records"]:
            out = D.parse_date(r["raw_date"])
            assert out["iso"] == r["date"], (c, r["record_no"])
