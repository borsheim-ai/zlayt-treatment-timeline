"""T-116 rounds 3 and 4 (D-055): gap math never guesses a record out. Every dated record is a gap endpoint (round 4: whatever ingest called it). A gap that
starts or ends at a record whose header looks administrative (intake form, records request, bill or ledger, affidavit, records review) carries
a visible warning in its explanation and why, with the alternative number, and the paralegal decides. The same warn-don't-exclude rule covers the
accident-date baseline. Round 4 cases through ingest are in test_t116_r4_all_dated_records.py. Fixture backend, no network."""
import os
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import gaps as GP
from app.backend import ingest as I
from app.backend.api import create_app

ROOT = pathlib.Path(__file__).resolve().parents[2]
LIB09 = "case_lib09_spanish_interpreter_espalda"


def rec(n, date, source, kind="encounter", excerpt=""):
    return dict(n=n, date_iso=date, source=source, kind=kind, excerpt=excerpt, date_candidates=[])


@pytest.mark.parametrize("source,label", [
    ("Consultorio Médico Aguaclara, formulario de admisión (OCR)", "intake form"),
    ("Fennimoor Spine Clinic, new patient intake form (OCR text)", "intake form"),
    ("Brightwater Spine, new patient paperwork", "intake form"),
    ("Capital PT, patient information form", "intake form"),
    ("Saltmarrow General Hospital, UB-04 itemized bill", "claim form"),
    ("Quoinmere Mutual Health Plan, EOB", "explanation of benefits"),
    ("Fennimoor Spine Clinic, itemized ledger", "ledger"),
    ("Hobbleton Family Clinic, billing statement", "billing statement"),
    ("Consultorio Aguaclara, estado de cuenta", "billing statement"),
    ("Pennyroyal Records Retrieval, 18.001 affidavit", "affidavit"),
    ("Capital PT, records request", "records request"),
    ("Marlowe Assurance, records review", "records review"),
    ("Sunderland Chiropractic, narrative letter", "narrative letter"),
    ("Pellingham and Rook PLLC, correspondence (letter of protection)", "letter or correspondence"),
    ("Dr. Orla Pennywhistle, phone note", "phone or message note"),
])
def test_administrative_types_are_recognised_from_the_header_label(source, label):
    assert GP.admin_label(rec(1, "2026-01-01", source)) == label


@pytest.mark.parametrize("source", [
    "Nimblewick Hand Therapy, intake", "Quarry Hill Occupational Health, intake", "Dr. Alvarez, primary care", "Capital PT, initial evaluation",
    "Hill Country Pain Management, new patient", "Fennimoor Spine Clinic, new patient", "Dr. Lysander Quibble, telehealth visit",
    "Austin Imaging, cervical MRI", "Central ER discharge summary", "Austin EMS run report", "Okmarrow EMS run report"])
def test_treatment_encounters_get_no_warning(source):
    """A bare 'intake' is an intake evaluation or visit: a treatment encounter. Only the paperwork wording looks administrative."""
    assert GP.admin_label(rec(1, "2026-01-01", source)) is None


def test_a_form_that_titles_itself_on_its_first_line_is_excluded_but_a_note_that_mentions_one_is_not():
    assert GP.admin_label(rec(1, "2026-01-01", "Clinic, new patient", excerpt="NEW PATIENT INTAKE FORM\nName: ...")) == "intake form"
    assert GP.admin_label(rec(1, "2026-01-01", "Clinic, new patient", excerpt="Exam today. Patient completed the intake form in the lobby.")) is None



def legacy_gaps(records):
    """D-055, copied and independent of kind: every dated record is an endpoint."""
    by = {}
    for r in records:
        if r.get("date_iso"):
            by.setdefault(r["date_iso"], []).append(r["n"])
    ds = sorted(by)
    from app.backend import dates
    return [{"from_date": a, "to_date": b, "from_records": sorted(by[a]), "to_records": sorted(by[b]), "days": dates.days_between(a, b),
             "flag": dates.days_between(a, b) > 30} for a, b in zip(ds, ds[1:])]


ADMIN_SOURCES = ["Clinic, billing statement", "Clinic, itemized ledger", "Plan, EOB", "Clinic, CMS-1500", "Firm, records request", "Clinic, intake form",
                 "Custodian, business records affidavit", "Clinic, narrative letter", "Insurer, records review", "Aguaclara, formulario de admisión (OCR)"]


@pytest.mark.parametrize("source", ADMIN_SOURCES)
def test_an_administrative_looking_record_still_ends_the_gap_it_always_did(source):
    """D-055: no record is dropped from gap math. Visit 1 Jan, paperwork 20 Jan, visit 25 Feb: two gaps (19 and 36 days), identical to pre-T-116."""
    recs = [rec(1, "2026-01-01", "Clinic, visit 1"), rec(2, "2026-01-20", source), rec(3, "2026-02-25", "Clinic, visit 2")]
    assert GP.compute_gaps(recs) == legacy_gaps(recs)
    assert [(x["days"], x["flag"]) for x in GP.compute_gaps(recs)] == [(19, False), (36, True)]


def test_a_gap_that_starts_at_paperwork_carries_the_warning_in_explanation_and_computed():
    recs = [rec(1, "2026-01-01", "Clinic, visit 1"), rec(2, "2026-01-20", "Clinic, intake form"), rec(3, "2026-02-25", "Clinic, visit 2")]
    (f,) = GP.gap_flags(recs)
    w = "This gap starts at record 2: Clinic, intake form, which looks like paperwork, not a visit. Check whether treatment continued."
    assert f["days"] == 36 and f["record_nos"] == [2, 3] and f["id"] == "f_gap_r2_r3"
    alt = "If record 2: Clinic, intake form is paperwork, not a visit, the gap would be 55 days (January 1, 2026 to February 25, 2026)."
    assert [x["warning"] for x in f["endpoint_warnings"]] == [w] and f["explanation"].endswith(w + " " + alt)
    assert f["endpoint_warnings"][0]["alternative_days"] == 55
    assert (f["endpoint_warnings"][0]["side"], f["endpoint_warnings"][0]["record_type"]) == ("start", "intake form")


def test_a_gap_that_ends_at_paperwork_carries_the_ends_wording():
    recs = [rec(1, "2026-01-01", "Clinic, visit 1"), rec(2, "2026-03-05", "Aguaclara, formulario de admisión (OCR)")]
    (f,) = GP.gap_flags(recs)
    assert f["days"] == 63
    assert f["endpoint_warnings"][0]["warning"] == ("This gap ends at record 2: Aguaclara, formulario de admisión (OCR), which looks like paperwork, "
                                                    "not a visit. Check whether treatment continued.")


def test_both_ends_at_paperwork_warn_twice_and_a_visit_on_the_same_date_anchors_the_end_so_it_does_not_warn():
    recs = [rec(1, "2026-01-01", "Clinic, billing statement"), rec(2, "2026-03-05", "Clinic, records request")]
    assert [x["side"] for x in GP.gap_flags(recs)[0]["endpoint_warnings"]] == ["start", "end"]
    both = [rec(1, "2026-01-01", "Clinic, visit 1"), rec(2, "2026-03-05", "Clinic, intake form"), rec(3, "2026-03-05", "Clinic, new patient visit")]
    f = GP.gap_flags(both)[0]
    assert f["endpoint_warnings"] == [] and "paperwork" not in f["explanation"] and f["days"] == 63


def test_a_clean_gap_has_no_warning_and_a_paperwork_record_inside_a_span_is_a_real_endpoint_not_a_note():
    recs = [rec(1, "2026-01-01", "Clinic, visit 1"), rec(2, "2026-03-01", "Clinic, visit 2")]
    f = GP.gap_flags(recs)[0]
    assert f["endpoint_warnings"] == [] and f["explanation"].endswith(".") and "paperwork" not in f["explanation"]


def test_an_undated_paperwork_record_is_judged_like_any_undated_encounter():
    """Pre-T-116 behaviour: an undated encounter whose candidate date falls inside the span raises ENDPOINT_NOT_VERIFIED."""
    base = [rec(1, "2026-01-01", "Clinic, visit 1"), rec(3, "2026-03-01", "Clinic, visit 3")]
    undated = dict(rec(2, None, "Clinic, intake form"), date_candidates=["2026-01-15"])
    assert GP.gap_flags(base + [undated])[0]["reasons"] == ["ENDPOINT_NOT_VERIFIED"]


# The reviewer's round 1 and round 2 probe labels (artifacts/review-evidence/T-116-paralegal-r2-labels.py): every one yields exactly the gap it
# yielded before T-116, whatever the warning says.
R1_R2_LABELS = [
    "Capital PT, initial evaluation (intake form completed same day)", "Hill Country Pain Management, intake form visit",
    "Dr. Alvarez, primary care, visit with billing review", "Dr. Alvarez, primary care, patient statement at visit", "Dr. Reyes, orthopedics, statement of MMI",
    "Austin Imaging, MRI cervical spine (records request attached)", "Dr. Lee, chiropractic, fax copy of visit 3", "Dr. Lee, chiropractic, visit 3 (faxed)",
    "Dr. Nguyen, records review visit", "Capital PT, discharge summary letter", "Dr. Patel, telehealth visit", "Dr. Patel, telephone visit (video)",
    "Brightwater Spine, new patient, consent form for ESI on same day", "Dr. Alvarez, pre-operative consent form and examination",
    "Capital PT, daily note (copy of billing record)", "Hill Country Pain Management, new patient", "Dr. Alvarez, initial visit; intake packet reviewed",
    "Capital PT, visit 5 (ledger balance reviewed)", "Dr. Oyelaran, physician statement of disability",
    "Office visit / records request", "PT daily note (billing copy)", "Intake and evaluation", "Capital PT, daily note, fax",
    "Capital PT, re-eval visit, statement", "Hill Country Pain Management, new patient, billing", "Capital PT, initial evaluation, correspondence",
    "Dr. Lee, chiropractic, visit 3 - records request copy", "Capital PT, intake form", "Dr. Lee, chiropractic, billing statement"]
CLINICAL = "Neck pain 5/10. Improved range of motion. Continue home exercise."


@pytest.mark.parametrize("excerpt", [CLINICAL, "Exam: neck range of motion reduced. Plan: continue PT 2x/week."])
@pytest.mark.parametrize("label", R1_R2_LABELS)
def test_reviewer_probe_labels_give_the_pre_t116_gap(label, excerpt):
    recs = [rec(1, "2026-03-01", "Capital PT, visit 1", excerpt="Exam: ok."), rec(2, "2026-03-20", label, excerpt=excerpt),
            rec(3, "2026-04-10", "Capital PT, visit 3", excerpt="Exam: ok.")]
    assert GP.compute_gaps(recs) == legacy_gaps(recs)
    assert [x["days"] for x in GP.compute_gaps(recs)] == [19, 21]
    assert GP.gap_flags(recs) == [] or label in ("Capital PT, intake form", "Dr. Lee, chiropractic, billing statement")     # a real paperwork label: D-055 conditional flag
    far = recs[:2] + [rec(3, "2026-05-10", "Capital PT, visit 3", excerpt="Exam: ok.")]
    assert GP.compute_gaps(far) == legacy_gaps(far)


@pytest.mark.parametrize("label", [
    "Capital PT, initial evaluation (intake form completed same day)", "Dr. Reyes, orthopedics, statement of MMI", "Dr. Nguyen, records review visit",
    "Dr. Lee, chiropractic, visit 3 (faxed)", "Capital PT, daily note, fax", "Capital PT, re-eval visit, statement",
    "Hill Country Pain Management, new patient, billing", "Capital PT, initial evaluation, correspondence", "Dr. Lee, chiropractic, fax copy of visit 3"])
def test_a_real_visit_whose_label_has_a_paperwork_word_does_not_draw_a_warning(label):
    recs = [rec(1, "2026-03-01", "Capital PT, visit 1"), rec(2, "2026-04-20", label, excerpt=CLINICAL)]
    f = GP.gap_flags(recs)[0]
    assert f["endpoint_warnings"] == [] and "paperwork" not in f["explanation"]


GOLD_GAP_CASES = sorted(p.stem for p in list((ROOT / "evals" / "golden").glob("case_*.txt")) + list((ROOT / "evals" / "library").glob("case_lib*.txt")))


@pytest.mark.parametrize("name", GOLD_GAP_CASES)
def test_golden_and_library_flagged_gaps_are_never_silently_different(name):
    """D-055 / round 4: the golden gap_table lists the visit-only reading. Every flagged row of it must appear in the product either as a counted flag
    with the same dates or, when paperwork-looking records change the counted math, as a flag that SHOWS that row as its alternative. Any product flag
    that is not a golden row must carry a warning. Nothing differs without a visible note."""
    import json
    d = ROOT / "evals" / ("golden" if name.startswith("case_0") else "library")
    exp = json.loads((d / f"{name}.expected.json").read_text())
    recs = I.ingest((d / f"{name}.txt").read_text())["records"]
    assert GP.compute_gaps(recs) == legacy_gaps(recs)
    flags = GP.gap_flags(recs)
    want = {(g["from_date"], g["to_date"], g["days"]) for g in exp["gap_table"] if g["flag"]}
    plain = {(f["from_date"], f["to_date"], f["days"]) for f in flags if not f["endpoint_warnings"]}
    shown = {(f["from_date"], f["to_date"], f["days"]) for f in flags} | {(w["alternative_from"], w["alternative_to"], w["alternative_days"])
                                                                        for f in flags for w in f["endpoint_warnings"]}
    assert want <= shown, (want - shown)
    assert plain <= want, (plain - want)


# ---- F3: the accident-date baseline warns, it does not exclude
def test_accident_date_conflict_still_fires_but_names_the_paperwork_record_instead_of_calling_it_treatment():
    from app.backend import conflicts as CF
    recs = [rec(1, "2026-01-12", "Capital PT, intake form", excerpt="NEW PATIENT INTAKE FORM\nDate of accident: 2026-01-15"),
            rec(2, "2026-01-20", "Capital PT, visit 1", excerpt="Exam: neck ROM reduced.")]
    (c,) = CF.accident_date_conflicts(recs)
    assert c["category"] == "accident_date_after_treatment" and c["first_treatment_date"] == "2026-01-12"
    assert "first recorded treatment" not in c["explanation"]
    assert "(record 1: Capital PT, intake form), which looks like paperwork, not a visit." in c["explanation"]
    assert c["explanation"].endswith("Check when treatment actually began before relying on this comparison.")


def test_accident_date_conflict_has_no_warning_when_a_visit_holds_the_earliest_date():
    from app.backend import conflicts as CF
    recs = [rec(1, "2026-01-12", "Capital PT, visit 1", excerpt="Exam: ok. Date of accident: 2026-01-15"), rec(2, "2026-01-20", "Capital PT, visit 2", excerpt="Exam: ok.")]
    (c,) = CF.accident_date_conflicts(recs)
    assert "paperwork" not in c["explanation"]
    recs[0]["source"] = "Capital PT, intake form"
    recs.append(rec(3, "2026-01-12", "Capital PT, new patient visit", excerpt="Exam: ok."))
    # T-123 (T-116 r5 M1): a paperwork record sharing the earliest date with a visit is never named as part of the first recorded treatment
    e = CF.accident_date_conflicts(recs)[0]["explanation"]
    assert "first recorded treatment" not in e and "looks like paperwork" in e and "record 3: Capital PT, new patient visit" in e


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    return TestClient(create_app(str(tmp_path / "t116.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def test_lib09_confirming_the_intake_form_date_changes_the_gap_as_before_and_warns_in_why_and_trace(client):
    """Gap math is as before T-116: confirming record 4 as 5 March moves the gap from 42 to 40 days and gap_changes says so. The gap now starts
    at an intake form, so it also carries the warning, in explanation, why and the item trace; the paralegal decides."""
    c = client
    tok = c.post("/api/cases", json={"library": LIB09}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(480):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed", "done_with_errors"):
            break
        time.sleep(0.25)
    gap = lambda: [f for f in c.get(f"/api/cases/{tok}").json()["flags"] if f["type"] == "gap"]
    assert [f["computed"]["days"] for f in gap()] == [42] and gap()[0]["computed"].get("endpoint_warnings") == []
    out = c.post(f"/api/cases/{tok}/records/r4/confirm_date", json={"date": "2026-03-05"}).json()
    assert [(x["old_days"], x["new_days"]) for x in out["gap_changes"]] == [(42, 40)]
    (f,) = gap()
    assert f["title"] == "Gap of 40 days" and (f["computed"]["from"], f["computed"]["to"]) == ("2026-03-05", "2026-04-14")
    w = f["computed"]["endpoint_warnings"][0]["warning"]
    assert w.startswith("This gap starts at record 4: ") and w.endswith("which looks like paperwork, not a visit. Check whether treatment continued.")
    assert w in f["explanation"] and w in f["why"]
    tr = c.get(f"/api/cases/{tok}/items/{f['id']}/trace").json()
    assert w in str(tr)
