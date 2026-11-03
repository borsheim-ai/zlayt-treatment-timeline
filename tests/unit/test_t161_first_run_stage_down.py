"""T-161: a FIRST run with a stage down (flags, judge 1-4) reads like a re-run that fails: the case is failed / run_partial, the message names the step, and the export
gate lists RUN_FAILED. A clean first run stays ready.
r2: the flag step is read from the steps that were down (not from lexicon flag rows), so it fails the case on a note with no phrase-list hit too; a first run whose extract
step gave NO entries at all is failed too (writing the entries named); a first run where only some records failed extraction kept its old shape (tray items, case ready) until T-165, which fails it too and names the records."""
import pytest
from app.backend import pipeline as PL, trace
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record
from tests.unit.test_t146_r3_decided_items_never_lowered import TAIL, case_error, down, model_flag

NOTHING_KEPT = "The AI step failed for {n} (the second check) on this run, and there is no earlier result to keep." + TAIL


def first_run(tmp_path, **script):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    script.setdefault("flags", model_flag)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(**script)), now=lambda: 1.0)
    return conn, cid, out


def blockers(conn, cid):
    return [b["reason_code"] for b in trace.export_blockers(conn, cid)]


def test_a_clean_first_run_stays_ready(tmp_path):
    conn, cid, out = first_run(tmp_path)
    assert out["status"] == "done" and out["error"] is None
    assert case_error(conn, cid) == ("ready", None)
    assert "RUN_FAILED" not in blockers(conn, cid)


@pytest.mark.parametrize("step,n,what", [("j1", 9, "items"), ("j2", None, None), ("j4", None, None), ("j3", 1, "item")], ids=["j1", "j2", "j4", "j3"])
@pytest.mark.parametrize("miss", [False, True], ids=["down", "fixture_miss"])
def test_first_run_with_a_judge_down_fails_the_case_and_names_the_step(tmp_path, step, n, what, miss):
    conn, cid, out = first_run(tmp_path, **{step: PL.AU.LLMFailedFixtureMiss("x") if miss else down(step)})
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial"
    assert out["error"] == err
    assert err["message"].startswith("The AI step failed for ") and "(the second check) on this run, and there is no earlier result to keep." in err["message"]
    assert err["message"].endswith(TAIL)
    assert "RUN_FAILED" in blockers(conn, cid)
    if n:
        assert err["message"] == NOTHING_KEPT.format(n=f"{n} {what}")


def test_first_run_with_the_flag_step_down_fails_the_case_and_names_the_step(tmp_path):
    conn, cid, out = first_run(tmp_path, flags=down("flags"))
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial" and out["error"] == err
    assert "(finding the flags) on this run, and there is no earlier result to keep." in err["message"] and err["message"].endswith(TAIL)
    assert "RUN_FAILED" in blockers(conn, cid)


def test_first_run_with_the_flag_step_missing_a_fixture_fails_the_case_too(tmp_path):
    conn, cid, _ = first_run(tmp_path, flags=PL.AU.LLMFailedFixtureMiss("x"))
    assert case_error(conn, cid)[0] == "failed" and "RUN_FAILED" in blockers(conn, cid)


NOTE = ('=== Record 1 ===\nDate: 2026-05-01\nSource: Brindlewood Physical Therapy, visit note\n'
        'Excerpt: "Patient seen for follow up of neck stiffness. Range of motion improved."\n\n'
        '=== Record 2 ===\nDate: 2026-05-10\nSource: Brindlewood Physical Therapy, visit note\n'
        'Excerpt: "Patient seen. Physical therapy continued 2x per week."\n')      # SYNTHETIC; no phrase-list hit, no dollar amount
NOTE_SCRIPT = sample_script(extract=lambda u: dict(summary="Physical therapy continued.", excerpt="Physical therapy continued 2x per week.") if "Physical therapy continued" in u
                            else dict(summary="Range of motion improved.", excerpt="Range of motion improved."))


def note_run(tmp_path, text=NOTE, **script):
    conn = DB.connect(str(tmp_path / "n.sqlite"))
    cid = DB.create_case(conn, text, now=0.0)
    sc = {**NOTE_SCRIPT, **script}
    return conn, cid, PL.run_pipeline(conn, cid, text, call=FakeCall(sc), now=lambda: 1.0)


def test_a_clean_first_run_of_a_plain_note_stays_ready(tmp_path):
    conn, cid, out = note_run(tmp_path)
    assert out["counts"]["entries"] == 2 and out["flags"] == []
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)


@pytest.mark.parametrize("miss", [False, True], ids=["down", "fixture_miss"])
def test_flag_step_down_on_a_note_with_no_phrase_list_hit_still_fails_the_case(tmp_path, miss):
    conn, cid, out = note_run(tmp_path, flags=PL.AU.LLMFailedFixtureMiss("x") if miss else down("flags"))
    assert out["flags"] == []                                      # nothing was made, so no row can carry the failure
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial" and out["error"] == err
    assert "(finding the flags)" in err["message"] and err["message"].endswith(TAIL)
    assert "RUN_FAILED" in blockers(conn, cid)


def test_flag_step_down_on_a_plain_note_rerun_names_the_step_too(tmp_path):
    conn, cid, _ = note_run(tmp_path)
    out = PL.run_pipeline(conn, cid, NOTE, call=FakeCall({**NOTE_SCRIPT, "flags": down("flags")}), now=lambda: 2.0)
    status, err = case_error(conn, cid)
    assert status == "failed" and "(finding the flags)" in err["message"] and out["error"] == err and "RUN_FAILED" in blockers(conn, cid)


def test_a_good_second_run_clears_a_flag_failure_on_a_plain_note(tmp_path):
    conn, cid, _ = note_run(tmp_path, flags=down("flags"))
    assert case_error(conn, cid)[0] == "failed"
    PL.run_pipeline(conn, cid, NOTE, call=FakeCall(NOTE_SCRIPT), now=lambda: 2.0)
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)


def test_j2_down_on_a_note_with_no_amounts_has_nothing_to_judge_and_stays_ready(tmp_path):      # documented: no amount, no judge-2 call, nothing failed
    conn, cid, out = note_run(tmp_path, j2=down("j2"))
    assert case_error(conn, cid) == ("ready", None)


def test_first_run_with_extract_down_and_no_entries_fails_and_names_the_step(tmp_path):
    conn, cid, out = first_run(tmp_path, extract=down("extract"))
    assert out["status"] == "done_with_errors" and out["counts"]["entries"] == 0
    status, err = case_error(conn, cid)
    assert status == "failed" and out["error"] == err
    assert err == {"code": "run_partial", "records": list(range(1, 10)), "extract_only": True,      # T-165: the records are named
                   "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep. No entry was made for records 1, 2, 3, 4, 5, 6, 7, 8 and 9." + TAIL}
    assert "RUN_FAILED" in blockers(conn, cid)


def test_first_run_with_extract_down_for_some_records_is_failed_too_t165(tmp_path):      # T-161 r2 kept this 'ready'; T-165 supersedes it (tests/unit/test_t165_partial_extract.py)
    good = sample_script()["extract"]

    def extract(user):
        if which_record(user)[0] == 1:
            raise down("extract")
        return good(user)
    conn, cid, out = first_run(tmp_path, extract=extract)
    assert out["status"] == "done_with_errors" and out["counts"]["entries"] > 0
    status, err = case_error(conn, cid)
    assert status == "failed" and err["records"] == [1] and "RUN_FAILED" in blockers(conn, cid)


def test_a_good_second_run_clears_a_failed_first_run(tmp_path):
    conn, cid, _ = first_run(tmp_path, j1=down("j1"))
    assert case_error(conn, cid)[0] == "failed"
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: 3.0)
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
