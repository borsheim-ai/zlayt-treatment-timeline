"""T-033 additions (backend): amounts extraction end to end, rate note numbers, damages mention, gap flag text/merge, flag text is template.
Golden data only."""
import pathlib
from app.backend import amounts as A, gaps as GP, conflicts as C, flag_templates as F, ingest as I, totals as T
from tests.unit import _golden as G

def case(name):
    return I.ingest(G.raw(name))["records"]

def test_sample_extract_amounts_and_totals():
    """R-CH-1..3: $6,240 and $2,150 charges, $185 rate, 'missing 3 days of work' damages with null value; accepted charges total $8,390."""
    rows = A.extract_amounts(case("sample"))
    got = [(r["record_no"], r["raw"], r["cents"], r["cls"]) for r in rows]
    assert got == [(2, "$6,240", 624000, "charge"), (4, "$185", 18500, "rate"), (5, "missing 3 days of work", None, "damages"), (8, "$2,150", 215000, "charge")]
    t = T.totals([{**r, "review_status": "accepted"} for r in rows if r["cls"] == "charge"] + [{**r, "review_status": "pending"} for r in rows if r["cls"] != "charge"])
    assert t["accepted_cents"] == 839000 and t["letter_line"] == "Billed charges accepted from these records: $8,390.00" and t["detected_pending_cents"] == 0

def test_dismiss_er_gives_2150_and_pending_is_separate():
    rows = A.extract_amounts(case("sample"))
    st = {2: "dismissed", 8: "accepted"}
    t = T.totals([{**r, "review_status": st.get(r["record_no"], "pending")} for r in rows])
    assert t["accepted_cents"] == 215000 and t["letter_line"].endswith("$2,150.00")

def test_injected_amount_is_never_a_charge_or_in_a_total():
    """R-RV-6: case_07 $50,000 is unclear with no value; accepted $420 only."""
    rows = A.extract_amounts(case("case_07_prompt_injection"))
    inj = [r for r in rows if r["raw"] == "$50,000"][0]
    assert inj["cls"] == "unclear" and inj["cents"] is None
    t = T.totals([{**r, "review_status": "accepted"} for r in rows])
    assert t["accepted_cents"] == 42000 and t["letter_line"] == "Billed charges accepted from these records: $420.00"

def test_duplicate_records_count_charge_once():
    rows = A.extract_amounts(case("case_03_rate_and_ocr"))
    assert sum(r["cents"] or 0 for r in rows if r["cls"] == "charge") == 33500

def test_no_float_in_amounts():
    assert "float(" not in pathlib.Path(A.__file__).read_text()
    assert A.to_cents("6,240") == 624000 and A.to_cents("95.5") == 9550 and A.to_cents("1,2OO") is None

def test_rate_note_numbers_sample_and_variant():
    """T-033 AC7: 12 planned and last visit 9 on the sample; plan 10 / last visit 7 on a variant; omitted when absent."""
    recs = case("sample")
    assert A.rate_note(recs, 4) == {"planned": 12, "last_visit": 9}
    v = [dict(n=1, source="Alpha PT, initial evaluation", excerpt="Plan of care: 10 visits. Charge per visit $90."),
         dict(n=2, source="Alpha PT, visit 7", excerpt="Pain 2/10."), dict(n=3, source="Other Clinic, visit 99", excerpt="Plan of care: 3 visits.")]
    assert A.rate_note(v, 1) == {"planned": 10, "last_visit": 7}
    assert A.rate_note([dict(n=1, source="Solo", excerpt="Charge per visit $90.")], 1) == {"planned": None, "last_visit": None}

def test_gap_flag_text_is_template_and_ids():
    """R-FL-8: flag title/explanation equal flag_templates output; id keyed by the record pair; evidence is the header lines."""
    recs = case("sample")
    f = GP.gap_flags(recs)
    assert [x["id"] for x in f] == ["f_gap_r6_r7"]
    assert (f[0]["title"], f[0]["explanation"]) == F.render("gap", "gap_over_30", days=73, from_date="2026-03-06", to_date="2026-05-18",
                                                            provider_a="Capital PT, visit 9", provider_b="Hill Country Pain Management, new patient")
    raw = I.normalize_text(G.raw("sample"))
    assert [raw[e["start"]:e["end"]] for e in f[0]["evidence"]][0] == "Date: 2026-03-06"

def test_accident_date_flag_evidence_offsets_and_template():
    """R-FL-2a: evidence offsets index the input; no choice between dates; no 'delay'."""
    recs = case("sample")
    raw = I.normalize_text(G.raw("sample"))
    c = C.accident_date_conflicts(recs)[0]
    assert [raw[e["start"]:e["end"]] for e in c["evidence"]] == ["Date of accident per intake form: 2026-01-19", "Date: 2026-01-09", "Date: 2026-01-09"]
    assert "delay" not in c["explanation"].lower() and "does not choose" in c["explanation"]

def test_confirm_date_recompute_keeps_unchanged_status():
    """ADR-002: an unchanged record pair keeps review status; a changed one resets."""
    recs = [dict(n=1, date_iso="2026-01-01", kind="encounter", source="A"), dict(n=2, date_iso="2026-03-01", kind="encounter", source="B")]
    old = [{**f, "review_status": "accepted"} for f in GP.gap_flags(recs)]
    assert GP.merge_flags(old, GP.gap_flags(recs))[0]["review_status"] == "accepted"
    recs[1]["date_iso"] = "2026-04-01"
    assert GP.merge_flags(old, GP.gap_flags(recs))[0]["review_status"] == "pending"

def test_ambiguous_endpoint_marks_gap_needs_review():
    """ADR-010: an undated encounter record whose candidates could fall in the span gives ENDPOINT_NOT_VERIFIED."""
    recs = [dict(n=1, date_iso="2026-01-01", kind="encounter"), dict(n=2, date_iso="2026-03-01", kind="encounter"),
            dict(n=3, date_iso=None, kind="encounter", date_candidates=["2026-02-04", "2026-04-02"])]
    assert GP.gap_flags(recs)[0]["reasons"] == ["ENDPOINT_NOT_VERIFIED"]
    recs[2]["kind"] = "phone_note"      # D-055: the ingest kind is a label guess and is not read; an undated record that could fall inside the span still needs review
    assert GP.gap_flags(recs)[0]["reasons"] == ["ENDPOINT_NOT_VERIFIED"]

def test_render_rejects_free_text_variables():
    import pytest
    with pytest.raises(KeyError):
        F.render("gap", "gap_over_30", days=40, narrative="the patient delayed care")
