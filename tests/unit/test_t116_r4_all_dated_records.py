"""T-116 round 4 (D-055, binding): every dated record reaches gap math, from ingest to gaps; nothing is dropped by guessing at a label.
A paperwork-looking record that starts, ends or splits a gap draws a visible warning that shows BOTH numbers (the counted gap and the gap if that
record is paperwork), and the paralegal decides. The accident-date baseline never states an intake form as the first treatment.
Reproduces the round 3 reviewer's probes (artifacts/review-evidence/T-116-paralegal-r3-probe.py, ...-warn-and-api.py). Fixture backend, no network."""
import pathlib

import pytest

from app.backend import conflicts as CF
from app.backend import gaps as GP
from app.backend import ingest as I

ROOT = pathlib.Path(__file__).resolve().parents[2]
HDR = "SYNTHETIC — invented for evaluation; not real patient data\n\n"
PLAIN = "Neck pain 5/10. Improved range of motion. Continue home exercise."
HEADED = "Exam: neck range of motion reduced. Plan: continue PT 2x/week."


def pk(*items):
    return HDR + "".join(f"=== Record {i} ===\nDate: {d}\nSource: {s}\nExcerpt: \"{e}\"\n\n" for i, (d, s, e) in enumerate(items, 1))


def run(*items):
    recs = I.ingest(pk(*items))["records"]
    return recs, GP.gap_flags(recs)


# the five visit labels (plus the W4 hidden-gap label) the r3 reviewer showed ingest classifying as records_admin / billing_statement
R3_VISIT_LABELS = [
    "Capital PT, initial evaluation, correspondence", "Dr. Lee, chiropractic, visit 3 - records request copy", "Office visit / records request",
    "Capital PT, visit 5 (ledger balance reviewed)", "Austin Imaging, MRI cervical spine (records request attached)"]


@pytest.mark.parametrize("excerpt", [PLAIN, HEADED])
@pytest.mark.parametrize("label", R3_VISIT_LABELS)
def test_blocker1_a_visit_whose_label_carries_a_paperwork_word_is_a_gap_endpoint_and_invents_no_gap(label, excerpt):
    recs, flags = run(("2026-03-01", "Capital PT, visit 1", excerpt), ("2026-03-20", label, excerpt), ("2026-04-10", "Capital PT, visit 3", excerpt))
    assert [g["days"] for g in GP.compute_gaps(recs)] == [19, 21]
    assert flags == []                      # no invented 40-day gap, and no paperwork warning on a real visit


@pytest.mark.parametrize("label", R3_VISIT_LABELS)
def test_blocker1_hidden_gap_w4_a_visit_that_ends_a_real_40_day_span_keeps_the_gap(label):
    recs, flags = run(("2026-03-01", "Capital PT, visit 1", PLAIN), ("2026-04-10", label, PLAIN))
    (f,) = flags
    assert (f["from_date"], f["to_date"], f["days"]) == ("2026-03-01", "2026-04-10", 40) and f["endpoint_warnings"] == []


@pytest.mark.parametrize("source", ["Clinic, billing statement", "Clinic, phone note", "Clinic, records request", "Plan, EOB", "Clinic, intake form",
                                    "Firm, correspondence", "Clinic, itemized ledger"])
def test_every_dated_record_reaches_gap_math_whatever_ingest_called_it(source):
    recs = I.ingest(pk(("2026-03-01", "Capital PT, visit 1", PLAIN), ("2026-03-20", source, PLAIN), ("2026-04-10", "Capital PT, visit 3", PLAIN)))["records"]
    assert [(g["from_date"], g["to_date"]) for g in GP.compute_gaps(recs)] == [("2026-03-01", "2026-03-20"), ("2026-03-20", "2026-04-10")]


def test_ingest_dated_records_all_have_a_date_in_gap_math_even_when_the_kind_is_not_an_encounter():
    recs = [dict(n=1, date_iso="2026-01-01", source="Clinic, visit 1", kind="encounter", excerpt="", date_candidates=[]),
            dict(n=2, date_iso="2026-01-20", source="Clinic, billing statement", kind="billing_statement", excerpt="", date_candidates=[]),
            dict(n=3, date_iso="2026-02-25", source="Clinic, visit 2", kind="phone_note", excerpt="", date_candidates=[])]
    assert [(g["days"]) for g in GP.compute_gaps(recs)] == [19, 36]


# ---- Major (mid-span): a paperwork-looking record inside a span shows both numbers
def test_midspan_split_into_two_flagged_gaps_each_carries_the_alternative_80_days():
    recs, flags = run(("2026-01-01", "Capital PT, visit 1", PLAIN), ("2026-02-20", "Capital PT, intake form", PLAIN), ("2026-03-23", "Capital PT, visit 2", PLAIN))
    assert [f["days"] for f in flags] == [50, 31]
    alt = ("If record 2: Capital PT, intake form is paperwork, not a visit, the gap would be 81 days (January 1, 2026 to March 23, 2026).")
    for f in flags:
        assert alt in f["explanation"] and any(alt == w["alternative"] for w in f["endpoint_warnings"])
        assert all(w["alternative_days"] == 81 and (w["alternative_from"], w["alternative_to"]) == ("2026-01-01", "2026-03-23") for w in f["endpoint_warnings"])


def test_midspan_paperwork_that_leaves_one_flagged_piece_still_names_the_full_span():
    recs, flags = run(("2026-01-01", "Capital PT, visit 1", PLAIN), ("2026-01-11", "Capital PT, billing statement", PLAIN), ("2026-03-23", "Capital PT, visit 2", PLAIN))
    (f,) = flags
    assert (f["from_date"], f["to_date"], f["days"]) == ("2026-01-11", "2026-03-23", 71)
    assert "If record 2: Capital PT, billing statement is paperwork, not a visit, the gap would be 81 days (January 1, 2026 to March 23, 2026)." in f["explanation"]


def test_midspan_paperwork_that_splits_a_40_day_span_into_two_short_pieces_still_shows_a_flag_with_both_numbers():
    recs, flags = run(("2026-03-01", "Capital PT, visit 1", PLAIN), ("2026-03-20", "Capital PT, intake form", PLAIN), ("2026-04-10", "Capital PT, visit 3", PLAIN))
    assert [g["days"] for g in GP.compute_gaps(recs)] == [19, 21]
    (f,) = flags
    assert (f["from_date"], f["to_date"], f["days"], f["conditional"]) == ("2026-03-01", "2026-04-10", 40, True)
    assert f["record_nos"] == [1, 2, 3] and f["id"] == "f_gap_r1_r3"
    assert f["title"] == "Possible gap of 40 days"
    assert ("No gap is counted here because record 2: Capital PT, intake form (March 20, 2026) falls inside this span and is counted as a visit "
            "(19 days, then 21 days). If record 2: Capital PT, intake form is paperwork, not a visit, the gap would be 40 days "
            "(March 1, 2026 to April 10, 2026).") in f["explanation"]
    (w,) = f["endpoint_warnings"]
    assert (w["side"], w["record_no"], w["alternative_days"]) == ("inside", 2, 40)


def test_midspan_paperwork_with_exam_text_still_draws_the_flag_r5():
    """T-116 r5: the header decides, not the text. A form-headed record whose text reads like an exam still warns (it costs a click)."""
    recs, flags = run(("2026-03-01", "Capital PT, visit 1", PLAIN), ("2026-03-20", "Capital PT, intake form", HEADED), ("2026-04-10", "Capital PT, visit 3", PLAIN))
    (f,) = flags
    assert (f["days"], f["conditional"], [w["side"] for w in f["endpoint_warnings"]]) == (40, True, ["inside"])


def test_midspan_paperwork_inside_a_span_of_30_days_or_less_draws_nothing():
    recs, flags = run(("2026-03-01", "Capital PT, visit 1", PLAIN), ("2026-03-10", "Capital PT, intake form", PLAIN), ("2026-03-31", "Capital PT, visit 3", PLAIN))
    assert flags == []


def test_paperwork_at_both_ends_names_both_records_in_one_alternative():
    recs, flags = run(("2026-01-01", "Capital PT, visit 1", PLAIN), ("2026-01-05", "Plan, EOB", PLAIN), ("2026-03-05", "Capital PT, intake form", PLAIN),
                      ("2026-04-20", "Capital PT, visit 2", PLAIN))
    f = next(x for x in flags if x["from_date"] == "2026-01-05")
    assert [w["side"] for w in f["endpoint_warnings"]] == ["start", "end"]
    assert ("If record 2: Plan, EOB and record 3: Capital PT, intake form are paperwork, not visits, the gap would be 109 days "
            "(January 1, 2026 to April 20, 2026).") in f["explanation"]


def test_when_there_is_no_visit_on_one_side_the_alternative_says_so():
    recs, flags = run(("2026-01-01", "Capital PT, intake form", PLAIN), ("2026-03-05", "Capital PT, visit 1", PLAIN))
    (f,) = flags
    assert "If record 1: Capital PT, intake form is paperwork, not a visit, there would be no visit before it and no gap to measure." in f["explanation"]
    assert f["endpoint_warnings"][0]["alternative_days"] is None


# ---- Blocker 2: the accident baseline never states an intake form as the first treatment
INTAKE = ("2026-01-12", "Capital PT, intake form", "NEW PATIENT INTAKE FORM\nDate of accident: 2026-01-15")
VISIT = ("2026-01-20", "Capital PT, visit 1", "Exam: neck ROM reduced.")


def test_blocker2_an_intake_form_is_not_stated_as_the_first_recorded_treatment():
    recs = I.ingest(pk(INTAKE, VISIT))["records"]
    (c,) = CF.accident_date_conflicts(recs)
    e = c["explanation"]
    assert "first recorded treatment" not in e
    assert "earliest recorded date, January 12, 2026 (record 1: Capital PT, intake form), which looks like paperwork, not a visit" in e
    assert ("If record 1: Capital PT, intake form is paperwork, not a visit, the first recorded visit is January 20, 2026 "
            "(record 2: Capital PT, visit 1), and the stated date is not later than it.") in e
    assert c["title"] == "Stated accident date is later than the earliest record" and c["first_treatment_date"] == "2026-01-12"


def test_blocker2_the_alternative_says_so_when_the_stated_date_is_later_than_the_first_visit_too():
    recs = I.ingest(pk(("2026-01-12", "Capital PT, intake form", "NEW PATIENT INTAKE FORM\nDate of accident: 2026-02-15"), VISIT))["records"]
    assert "and the stated date is also later than it." in CF.accident_date_conflicts(recs)[0]["explanation"]


def test_blocker2_with_no_visit_at_all_the_alternative_says_there_is_nothing_to_compare():
    recs = I.ingest(pk(INTAKE))["records"]
    assert "there is no recorded visit to compare with." in CF.accident_date_conflicts(recs)[0]["explanation"]


def test_blocker2_a_visit_on_the_earliest_date_keeps_the_plain_wording():
    recs = I.ingest(pk(("2026-01-12", "Capital PT, visit 1", "Exam: ok. Date of accident: 2026-01-15"), ("2026-01-20", "Capital PT, visit 2", "Exam: ok.")))["records"]
    (c,) = CF.accident_date_conflicts(recs)
    assert "first recorded treatment, January 12, 2026" in c["explanation"] and "paperwork" not in c["explanation"]
    assert c["title"] == "Stated accident date is later than recorded treatment"


def test_blocker2_a_billing_statement_dated_before_the_first_visit_does_not_become_the_first_treatment():
    """T-141 r2: the statement (01-05) predates the stated accident (01-09) but says nothing about a collision, so it is an info note, not a conflict; the first
    visit (01-12) is after the stated date. Expected changed from 'conflict naming the statement' (old rule: any earlier-dated record was 'treatment')."""
    recs = I.ingest(pk(("2026-01-05", "Hobbleton Clinic, billing statement", "Balance forward."), ("2026-01-12", "Capital PT, visit 1", "Exam: ok. Date of accident: 2026-01-09"),
                       ("2026-01-20", "Capital PT, visit 2", "Exam: ok.")))["records"]
    assert CF.accident_date_conflicts(recs) == []
    assert CF.accident_date_note(recs)["record_nos"] == [1]


def test_blocker2_a_billing_statement_dated_before_the_first_visit_is_never_named_as_the_first_treatment():
    """Stated 01-15, statement 01-05, visit 01-12 whose text states the accident: the conflict compares with the visit, never with the statement."""
    recs = I.ingest(pk(("2026-01-05", "Hobbleton Clinic, billing statement", "Balance forward."), ("2026-01-12", "Capital PT, visit 1", "Exam: ok. Date of accident: 2026-01-15"),
                       ("2026-01-20", "Capital PT, visit 2", "Exam: ok.")))["records"]
    (c,) = CF.accident_date_conflicts(recs)
    assert "first recorded treatment, January 12, 2026" in c["explanation"] and "paperwork" not in c["explanation"] and c["record_nos"] == [2]


# ---- through the API (fixture backend): both numbers reach the flag's explanation, why and trace
@pytest.fixture
def client(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from app.backend.api import create_app
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    return TestClient(create_app(str(tmp_path / "t116r4.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _gaps_via_api(c, library):
    import time
    tok = c.post("/api/cases", json={"library": library}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(480):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed", "done_with_errors"):
            break
        time.sleep(0.25)
    return tok, [f for f in c.get(f"/api/cases/{tok}").json()["flags"] if f["type"] == "gap"]


def test_lib06_ledger_inside_a_35_day_span_shows_the_conditional_flag_with_both_numbers_in_explanation_and_why(client):
    tok, gaps = _gaps_via_api(client, "case_lib06_lop_billed_vs_adjusted")
    f = next(g for g in gaps if (g["computed"]["from"], g["computed"]["to"]) == ("2026-05-13", "2026-06-17"))
    assert f["title"] == "Possible gap of 35 days" and f["computed"]["conditional"] is True
    assert "No gap is counted here because record 4:" in f["explanation"] and "the gap would be 35 days (May 13, 2026 to June 17, 2026)." in f["explanation"]
    assert "the gap would be 35 days" in f["why"] and "No gap is counted here" in f["why"]
    assert "the gap would be 35 days" in str(client.get(f"/api/cases/{tok}/items/{f['id']}/trace").json())


def test_lib10_claim_form_after_the_last_visit_shows_43_counted_and_49_if_paperwork(client):
    tok, gaps = _gaps_via_api(client, "case_lib10_eob_ub04_cms1500")
    (f,) = [g for g in gaps if g["computed"]["days"] in (43, 49)]
    assert f["title"] == "Gap of 43 days" and f["computed"]["endpoint_warnings"][0]["alternative_days"] == 49
    assert "the gap would be 49 days (July 8, 2026 to August 26, 2026)." in f["explanation"] and "the gap would be 49 days" in f["why"]


def test_case_09_counts_the_billing_statement_and_phone_note_and_shows_the_56_day_span_as_a_conditional_flag():
    """D-003 said they never split the 56-day gap; D-055 counts every dated record and shows the span with both numbers instead of hiding it."""
    recs = I.ingest((ROOT / "evals" / "golden" / "case_09_nonvisit_hides_gap.txt").read_text())["records"]
    assert [g["days"] for g in GP.compute_gaps(recs)] == [27, 11, 18, 14]
    (f,) = GP.gap_flags(recs)
    assert (f["from_date"], f["to_date"], f["days"], f["conditional"]) == ("2026-02-02", "2026-03-30", 56, True)
    assert "the gap would be 56 days (February 2, 2026 to March 30, 2026)." in f["explanation"]
