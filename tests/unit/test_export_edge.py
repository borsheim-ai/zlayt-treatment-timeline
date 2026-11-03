"""T-041 review round 1: could-not-process reconciliation, non-verbatim excerpt guard, rate reason wording."""
import re
from app.backend import export as X
from tests.unit.test_export import build_case


def test_could_not_process_record_listed_in_reconciliation():
    c = build_case(lambda k, key: not (k == "entry" and key == 4))
    c["entries"] = [e for e in c["entries"] if e["record_no"] != 4]
    next(r for r in c["records"] if r["n"] == 4)["could_not_process"] = True
    out = X.build_export(c)
    sec = out["internal_notes_text"].split("RECORDS NOT IN THE TREATMENT SECTION")[1].split("EDITED ITEMS")[0]
    assert "- Record 4 (Capital PT, initial evaluation, January 23, 2026) — could not process" in sec
    assert "January 23, 2026" not in out["letter_text"]


def test_non_verbatim_excerpt_not_exported_and_listed():
    c = build_case()
    e3 = next(e for e in c["entries"] if e["record_no"] == 3)
    e3.update(review_status="edited", excerpt="Persistent neck pain 6/10, daily headaches. Patient has chronic condition.")
    out = X.build_export(c)
    assert "chronic condition" not in out["letter_text"] and "January 16, 2026" not in out["letter_text"]
    sec = out["internal_notes_text"].split("RECORDS NOT IN THE TREATMENT SECTION")[1].split("EDITED ITEMS")[0]
    assert "Record 3" in sec and "excerpt not found in record" in sec
    assert out["counts"]["records_in_letter"] == 8


def test_non_verbatim_charge_not_totaled():
    c = build_case()
    next(a for a in c["amounts"] if a["id"] == "A1")["excerpt"] = "ER charges: $9,999."
    out = X.build_export(c)
    assert "Billed charges accepted from these records: $2,150.00" in out["letter_text"].split("\n")
    assert "9,999" not in out["letter_text"] and "excerpt not found in record" in out["internal_notes_text"]


def test_rate_reason_wording_from_same_provider_records():
    n = X.build_export(build_case())["internal_notes_text"]
    assert "Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger." in n


def test_fixture_set_env_maps_to_named_dir(monkeypatch):
    from app.llm.backends import fixture as F
    monkeypatch.delenv("LLM_FIXTURE_DIR", raising=False)
    monkeypatch.setenv("FIXTURE_SET", "curated")
    assert F.fixture_dir() == F.DEFAULT_DIR / "curated"
    monkeypatch.setenv("LLM_FIXTURE_DIR", "/x")
    assert str(F.fixture_dir()) == "/x"


def test_pipeline_shaped_amounts_quote_their_own_sentence_and_labels_match_golden():
    """T-051: a pipeline amount carries the whole record excerpt and category-style subtypes; the export still quotes the amount sentence."""
    from tests.unit.test_export import build_case
    c = build_case()
    full = {r["n"]: r["excerpt"] for r in c["records"]}
    for a in c["amounts"]:
        if a["cls"] in ("charge", "rate"):
            a["excerpt"] = full[a["record_no"]]
    for f in c["flags"]:
        f["subtype"] = {"treatment_plan": "treatment_plan_vs_actual", "patient_reported_onset": "patient_report"}.get(f["subtype"], f["subtype"])
    out = X.build_export(c)
    assert 'Source [Ex. __ / Bates __]: "ER charges: $6,240."' in out["letter_text"]
    n = out["internal_notes_text"]
    assert "Conflict, PT plan:" in n and '"Charge per visit $185."' in n and "self-report" not in n


def test_patient_report_flag_title_is_neutral():
    """D-040: no label asserts who spoke."""
    from app.backend import flag_templates as T
    title, expl = T.render("causation", "patient_reported_onset", provider="Hill Country Pain Management", date="2026-06-12", quote="Patient states symptoms began after the January collision.")
    assert title == "Reported onset" and "self-report" not in (title + expl).lower() and "patient self" not in expl.lower()
