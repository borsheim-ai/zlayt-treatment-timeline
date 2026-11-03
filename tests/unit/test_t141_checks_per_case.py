"""T-141 round 2: GET case `checks` is computed from what THIS case ran (language routing, skipped stage, never run), not a constant."""
import pathlib

from app.backend import pipeline as PL, present
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.test_t145_judge_not_run import Clock, _run

LIB = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"
ALL = ["plan_vs_early_end", "denial_vs_history", "accident_date", "provider_name"]


def _view(conn, cid):
    return present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)["checks"]


def _lib_checks(name, tmp_path):
    text = (LIB / f"{name}.txt").read_text()
    with PL._Backend("fixture"):
        conn, cid, call = PL._scratch_call(str(tmp_path), PL.IN.normalize_text(text))
        PL.run_pipeline(conn, cid, text, call=call)
        out = _view(conn, cid)
        conn.close()
    return out


def test_ingested_but_not_run_case_says_the_comparison_between_records_has_not_run(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.ingest_case(conn, cid, G.raw("sample"), 0.0)
    ch = _view(conn, cid)
    assert ch["conflict_types"] == ["accident_date", "provider_name"]
    assert {x["type"]: x["reason_code"] for x in ch["skipped"]} == {"plan_vs_early_end": "NOT_RUN", "denial_vs_history": "NOT_RUN"}


def test_a_finished_english_case_lists_all_four_and_skips_nothing(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    _run(conn, cid, Clock())
    ch = _view(conn, cid)
    assert ch["conflict_types"] == ALL and ch["skipped"] == []


def test_a_run_that_hit_its_deadline_before_the_conflict_stage_says_so(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    _run(conn, cid, Clock("amounts"))              # the deadline passes as the amounts stage starts: the conflicts stage is never reached
    ch = _view(conn, cid)
    assert ch["conflict_types"] == ["accident_date", "provider_name"]
    assert {x["type"]: x["reason_code"] for x in ch["skipped"]} == {"plan_vs_early_end": "STAGE_SKIPPED", "denial_vs_history": "STAGE_SKIPPED"}


def test_a_run_that_died_before_the_conflict_stage_is_run_failed(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    _run(conn, cid, Clock())
    DB.update_case(conn, cid, status="failed")
    cfg = dict(DB.get_case(conn, cid)["config"])
    cfg["run_checks"] = dict(cfg["run_checks"], conflicts_stage="pending")      # what a crash between 'run started' and 'conflict stage done' leaves behind
    DB.update_case(conn, cid, config_json=cfg)
    ch = _view(conn, cid)
    assert {x["type"]: x["reason_code"] for x in ch["skipped"]} == {"plan_vs_early_end": "RUN_FAILED", "denial_vs_history": "RUN_FAILED"}


def test_a_mixed_language_case_names_the_records_the_english_rules_could_not_read(tmp_path):
    ch = _lib_checks("case_lib09_spanish_interpreter_espalda", tmp_path)
    sk = {x["type"]: x for x in ch["skipped"]}
    assert set(sk) == {"plan_vs_early_end", "denial_vs_history", "accident_date"}
    assert all(x["reason_code"] == "LANGUAGE_PARTIAL" and x["record_nos"] == [2, 4, 7] for x in sk.values())
    assert "provider_name" in ch["conflict_types"] and "denial_vs_history" in ch["conflict_types"]


def test_lib11_no_false_accident_date_conflict_and_the_predate_note_counts_the_annual_visit(tmp_path):
    ch = _lib_checks("case_lib11_priors_and_ledger", tmp_path)
    assert ch["skipped"] == [] and ch["conflict_types"] == ALL
    assert [n["code"] for n in ch["notes"]] == ["RECORDS_PREDATE_ACCIDENT"] and ch["notes"][0]["count"] >= 1


# ---------------------------------------------------------------- T-141 round 3: notes at read time, no stored summary, mutants
_STALE = """SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-03-04
Source: Dr. A, primary care, annual visit
Excerpt: "Annual visit. Blood pressure 120/80. No complaints."

=== Record 2 ===
Date: 03/06/2026
Source: Central ER discharge summary
Excerpt: "Restrained driver in a rear-end collision. Neck pain 7/10. CT head negative."

=== Record 3 ===
Date: 2026-03-27
Source: Intake form
Excerpt: "Date of accident per intake form: 2026-03-18."
"""


def test_confirming_a_date_refreshes_the_note_and_the_flag_together(tmp_path):
    """Reviewer r2 finding 2: the ambiguous collision record made the note say 'no conflict is raised'; confirming it must raise the conflict and drop the note."""
    from app.backend import review
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, _STALE, now=0.0)
    PL.ingest_case(conn, cid, _STALE, 0.0)
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    assert [n["code"] for n in v["checks"]["notes"]] == ["RECORDS_PREDATE_ACCIDENT"] and not [f for f in v["flags"] if f["category"] == "accident_date_after_treatment"]
    rec2 = next(r for r in v["records"] if r["seq"] == 2)
    review.confirm_date(conn, cid, rec2["id"], "2026-03-06")
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    assert [f["category"] for f in v["flags"] if f["category"] == "accident_date_after_treatment"] == ["accident_date_after_treatment"]
    assert v["checks"]["notes"] == []


def test_a_case_whose_only_dated_record_was_ambiguous_lists_accident_date_after_confirming_it(tmp_path):
    from app.backend import review
    text = """SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 03/06/2026
Source: Central ER discharge summary
Excerpt: "Restrained driver in a rear-end collision. Neck pain 7/10."
"""
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, text, now=0.0)
    PL.ingest_case(conn, cid, text, 0.0)
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    assert "accident_date" not in v["checks"]["conflict_types"] and {x["type"]: x["reason_code"] for x in v["checks"]["skipped"]}["accident_date"] == "NO_DATED_RECORD"
    review.confirm_date(conn, cid, v["records"][0]["id"], "2026-03-06")
    assert "accident_date" in _view(conn, cid)["conflict_types"]


def test_a_case_with_no_stored_summary_reports_every_check_as_not_run(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    _run(conn, cid, Clock())
    cfg = dict(DB.get_case(conn, cid)["config"])
    cfg.pop("run_checks")
    DB.update_case(conn, cid, config_json=cfg)                      # a case stored before per-case checks existed
    ch = _view(conn, cid)
    assert ch["conflict_types"] == [] and sorted(x["type"] for x in ch["skipped"]) == sorted(ALL) and {x["reason_code"] for x in ch["skipped"]} == {"NOT_RUN"}
    DB.update_case(conn, cid, status="failed")
    assert _view(conn, cid)["conflict_types"] == [] and {x["reason_code"] for x in _view(conn, cid)["skipped"]} == {"NOT_RUN"}


def test_a_rerun_that_crashes_in_the_conflict_stage_is_run_failed_not_the_previous_result(tmp_path, monkeypatch):
    """The run-start 'pending' write is what stops a crashed re-run of a finished case from reporting the earlier run's result."""
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    _run(conn, cid, Clock())
    assert _view(conn, cid)["conflict_types"] == ALL
    def boom(*a, **k):
        raise RuntimeError("simulated crash inside the conflict stage")
    monkeypatch.setattr(PL.FL, "run_conflict_pass", boom)
    try:
        _run(conn, cid, Clock())
    except RuntimeError:
        pass
    DB.update_case(conn, cid, status="failed")                        # what the API does on an escaped exception
    ch = _view(conn, cid)
    assert ch["conflict_types"] == ["accident_date", "provider_name"]
    assert {x["type"]: x["reason_code"] for x in ch["skipped"]} == {"plan_vs_early_end": "RUN_FAILED", "denial_vs_history": "RUN_FAILED"}


def test_a_case_with_an_uncertain_language_record_says_the_english_rules_did_not_read_it(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    _run(conn, cid, Clock())
    cfg = dict(DB.get_case(conn, cid)["config"])
    cfg["run_checks"] = PL.CC.run_summary([dict(n=1, lang="en"), dict(n=2, lang="uncertain")], stage="ran")
    DB.update_case(conn, cid, config_json=cfg)
    sk = {x["type"]: x for x in _view(conn, cid)["skipped"]}
    assert set(sk) == {"plan_vs_early_end", "denial_vs_history", "accident_date"} and all(x["reason_code"] == "LANGUAGE_PARTIAL" and x["record_nos"] == [2] for x in sk.values())
