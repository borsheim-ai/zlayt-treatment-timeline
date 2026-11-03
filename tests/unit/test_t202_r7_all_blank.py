"""T-202 D-073 FALLBACK (round 6 failed: a visit note lent its date to another visit's charge; a UB-04 period overrode a line's own date). The letter extracts NO service date:
every charge line prints the fillable blank 'date of service [__________] (record dated X)', Step 3 carries the same text, and evals/letter_check accepts that form and nothing else.
The reader is kept (service_date.read, SCOPE_CUTS row 28) and still reads; nothing calls it. Code only."""
import pytest

from app.backend import amounts as AM, export, service_date as SD, store
from evals import letter_check as LC

LEDGER = "Fennimoor Spine Clinic, itemized ledger"
NOTE = "Fennimoor Spine Clinic, progress note"
TABLE = "Itemized ledger.\nDOS\tService\tCharge\n03/27/2026\tNew patient exam\t$250.00\n04/02/2026\toffice visit\t$180.00\n"
VISIT = "Exam charge $250.00."
UB = "UB-04 itemized bill. Statement covers period FROM 06/09/2026 THROUGH 06/12/2026.\nRev 0120 room and board semi-private FL47 total charges $4,920.00\n"
SHAPES = [(LEDGER, TABLE, "$250.00"), (NOTE, VISIT, "$250.00"), ("Saltmarrow General Hospital, UB-04 itemized bill", UB, "$4,920.00")]


def _item(ex, fig):
    return {"excerpt": ex, "value_cents": AM.to_cents(fig.lstrip("$"))}


@pytest.mark.parametrize("src,ex,fig", SHAPES)
def test_nothing_is_stated_but_the_reader_still_reads(src, ex, fig):
    pos = ex.index(fig)
    assert SD.read(ex, pos, src, "2026-06-15")["state"] == "stated"          # the dormant reader: the control that the fixtures are real
    assert SD.resolve(ex, pos, src, "2026-06-15")["state"] == "not_stated"
    d = store.charge_service_date(_item(ex, fig), {"source": src, "date_iso": "2026-06-15"}, pos)
    assert d["state"] == "not_stated" and d["date_iso"] is None and d["end_iso"] is None
    assert d["text"] == f"date of service [__________] (record dated June 15, 2026)" and d["date_label"] == "record"
    assert d["confirm_note"] and "leaves a blank" in d["confirm_note"]
    assert store.charge_service_dates(_item(ex, fig), {"source": src, "date_iso": "2026-06-15"}, pos) == (None, None)


def test_a_line_the_reader_would_have_dated_gets_the_reason_not_read():
    ex = VISIT
    assert SD.resolve(ex, ex.index("$250.00"), NOTE, "2026-06-15")["reason"] == "not_read"
    assert "does not take a date of service" in SD.confirm_note("not_read", "")


def _case(**ch):
    return {"records": [{"n": 1, "source": LEDGER, "date_iso": "2026-06-15", "excerpt": "New patient exam charge $250.00."}], "entries": [], "flags": [], "pending_count": 0, "events": [],
            "amounts": [dict(id="a1", record_no=1, cents=25000, cls="charge", raw="$250.00", excerpt="New patient exam charge $250.00.", review_status="accepted", **ch)]}


@pytest.mark.parametrize("extra", [{}, {"dos_iso": None}, {"dos_iso": "2026-03-27"}, {"dos_iso": "2026-06-09", "dos_end_iso": "2026-06-12"}, {"dos_iso": "2026-03-27", "dos_text": "March 27, 2026"}])
def test_the_letter_prints_the_blank_whatever_the_case_dict_carries(extra):
    out = export.build_export(_case(**extra), None)
    assert f"{LEDGER}, date of service [__________] (record dated June 15, 2026): $250.00" in out["letter_text"].split("\n")
    assert "March 27" not in out["letter_text"] and "June 9" not in out["letter_text"]
    assert "CHARGES WITHOUT A CERTAIN DATE OF SERVICE" in out["internal_notes_text"]


def _check(head, source=LEDGER, ex="New patient exam charge $250.00.", rd="2026-06-15"):
    letter = f"BILLED CHARGES\n\n{head}: $250.00\nSource [Ex. __ / Bates __]: \"{ex}\"\n\nBilled charges accepted from these records: $250.00"
    return LC.charge_date_violations(letter, [{"n": 1, "source": source, "date_iso": rd, "excerpt": ex}])


BLANK_OK = f"{LEDGER}, date of service [__________] (record dated June 15, 2026)"


def test_letter_check_accepts_the_exact_blank_only():
    assert _check(BLANK_OK) == []
    assert _check(f"{LEDGER}, date of service [__________]", rd=None) == []
    assert _check(f"{NOTE}, date of service [__________] (record dated June 15, 2026)", NOTE, "Exam charge $250.00.") == []
    for bad in (f"{LEDGER}, June 15, 2026", f"{LEDGER}, March 27, 2026", f"{LEDGER}, June 9–12, 2026", f"{LEDGER}, date of service [__________] (record dated June 16, 2026)",
                f"{LEDGER}, date of service [__________] (statement dated June 15, 2026)", f"{LEDGER}, date of service [__________]", f"{LEDGER}, date of service [__________] (record dated June 15, 2026) x",
                f"{LEDGER}, date of service [_________] (record dated June 15, 2026)", f"Other, date of service [__________] (record dated June 15, 2026)"):
        assert _check(bad), bad
    assert _check(f"{NOTE}, date of service [__________] (statement dated June 15, 2026)", NOTE, "Exam charge $250.00.")          # D-075: the statement variant is gone for every source
    assert _check(BLANK_OK, rd=None)          # the record has no date, so no parenthesis


def test_letter_check_fails_a_dated_letter_over_the_corpus_sample():
    letters = LC.letters_for(open("evals/golden/sample.txt").read())
    got = letters["all_accepted"]
    assert LC.charge_date_violations(got["letters"]["standard"], got["records"]) == []
    dated = got["letters"]["standard"].replace("date of service [__________] (record dated January 9, 2026)", "January 9, 2026")
    assert dated != got["letters"]["standard"] and LC.charge_date_violations(dated, got["records"])
