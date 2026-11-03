"""T-165: on a FIRST run, when the extract step failed on N >= 1 records the case is run_partial with those records named and the export gate lists RUN_FAILED
(one record down, 8 of 9 down, all ok, hand-entered). A record the paralegal has since entered by hand (D-053 tray manual entry, D-031) is no longer a failure: it becomes a
named warning, and a case whose only failures were hand-entered reads ready again. A run where every record extracted stays ready.
(Replaces the T-161 r2 rule 'failed only at zero entries'; the `not dated` mutant of T-161 r2 no longer exists, the boundary is pinned by the undated-entry test.)"""
import pytest
from app.backend import pipeline as PL, present, review as RV, trace
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record
from tests.unit.test_t146_r3_decided_items_never_lowered import TAIL, case_error, down, model_flag

TAIL_ = " Run it again to retry."
J1_OK = FakeCall({"j1": {"verdict": "supported", "reason_code": "NONE"}})


def extract_down(*nos):
    good = sample_script()["extract"]

    def extract(user):
        if which_record(user)[0] in nos:
            raise down("extract")
        return good(user)
    return extract


def run(tmp_path, *nos, again=None, now=1.0):
    """First run on a new case, or (again=(conn, cid)) a re-run of that case."""
    conn, cid = again or (DB.connect(str(tmp_path / "d.sqlite")), None)
    cid = cid or DB.create_case(conn, G.raw("sample"), now=0.0)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=extract_down(*nos), flags=model_flag)), now=lambda: now)
    return conn, cid, out


def blockers(conn, cid):
    return [b["reason_code"] for b in trace.export_blockers(conn, cid)]


def hand_entry(conn, cid, n):
    rec = G.records("sample")[n - 1]
    return RV.manual_entry(conn, cid, f"r{n}", {"summary": rec["excerpt"], "excerpt": rec["excerpt"]}, call=J1_OK)


def test_all_records_extracted_stays_ready(tmp_path):
    conn, cid, out = run(tmp_path)
    assert out["error"] is None and case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
    assert present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)["warnings"] == []


def test_one_record_down_on_a_first_run_is_run_partial_naming_the_record(tmp_path):
    conn, cid, out = run(tmp_path, 1)
    assert out["counts"]["entries"] == 8                                     # the other eight came out; the failed one is a tray placeholder
    status, err = case_error(conn, cid)
    assert status == "failed" and out["error"] == err
    assert err == {"code": "run_partial", "records": [1], "extract_only": True,
                   "message": "The AI step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 1." + TAIL_}
    assert "RUN_FAILED" in blockers(conn, cid)
    view = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    assert [t["record_ids"] for t in view["tray"]] == [["r1"]] and view["error"] == err


def test_eight_of_nine_down_is_run_partial_naming_all_eight(tmp_path):
    conn, cid, out = run(tmp_path, *range(2, 10))
    assert out["counts"]["entries"] == 1
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial" and err["records"] == list(range(2, 10))
    assert err["message"] == ("The AI step failed for 8 items (writing the entries) on this run, and there is no earlier result to keep. "
                              "No entry was made for records 2, 3, 4, 5, 6, 7, 8 and 9." + TAIL_)
    assert "RUN_FAILED" in blockers(conn, cid)


def test_all_nine_down_names_all_nine(tmp_path):
    conn, cid, out = run(tmp_path, *range(1, 10))
    status, err = case_error(conn, cid)
    assert status == "failed" and err["records"] == list(range(1, 10)) and "records 1, 2, 3, 4, 5, 6, 7, 8 and 9." in err["message"]


NOTE = ('=== Record 1 ===\nSource: Brindlewood Physical Therapy, visit note\n'
        'Excerpt: "Patient seen for follow up of neck stiffness. Range of motion improved."\n\n'
        '=== Record 2 ===\nDate: 2026-05-10\nSource: Brindlewood Physical Therapy, visit note\n'
        'Excerpt: "Patient seen. Physical therapy continued 2x per week."\n')      # SYNTHETIC; record 1 has no date


def test_an_undated_entry_is_still_an_entry_the_failed_record_is_named(tmp_path):
    """The boundary the T-161 r2 reviewer's `not dated` mutant probed: the only entry that came out is undated, every other record failed."""
    conn = DB.connect(str(tmp_path / "n.sqlite"))
    cid = DB.create_case(conn, NOTE, now=0.0)

    def extract(u):
        if "Physical therapy continued" in u:
            raise down("extract")
        return dict(summary="Range of motion improved.", excerpt="Range of motion improved.")
    out = PL.run_pipeline(conn, cid, NOTE, call=FakeCall(sample_script(extract=extract)), now=lambda: 1.0)
    assert out["entries"] == [] and len(out["undated_entries"]) == 1          # the one entry is undated
    status, err = case_error(conn, cid)
    assert status == "failed" and err["records"] == [2] and "No entry was made for record 2." in err["message"] and "RUN_FAILED" in blockers(conn, cid)


# ---------------------------------------------------------------------------------------- hand-entered (D-053 tray manual entry)
def hand_warnings(conn, cid):
    return present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)["warnings"]


def test_a_record_entered_by_hand_before_the_run_is_a_named_warning_not_a_failure(tmp_path):
    conn = DB.connect(str(tmp_path / "h.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.ingest_case(conn, cid, G.raw("sample"))
    hand_entry(conn, cid, 1)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=extract_down(1), flags=model_flag)), now=lambda: 1.0)
    assert out["error"] is None and case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
    assert [e["id"] for e in DB.list_items(conn, cid, "entry") if e["id"] == "e1_m"] == ["e1_m"]      # the hand-entered row survived the run
    w = [x for x in out["warnings"] if x["code"] == "ENTERED_BY_HAND"]
    assert [(x["record_no"], x["item_id"]) for x in w] == [(1, "e1")] and "record 1" in w[0]["message"] and "by hand" in w[0]["message"]
    assert [x["record_no"] for x in hand_warnings(conn, cid) if x["code"] == "ENTERED_BY_HAND"] == [1]


def test_entering_the_failed_record_by_hand_after_the_run_clears_the_failure_into_a_warning(tmp_path):
    conn, cid, _ = run(tmp_path, 1)
    assert case_error(conn, cid)[0] == "failed"
    hand_entry(conn, cid, 1)
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
    assert [x["record_no"] for x in hand_warnings(conn, cid)] == [1]
    assert present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)["tray"] == []      # T-110 r2: it left the tray


def test_entering_one_of_two_failed_records_by_hand_leaves_the_other_named(tmp_path):
    conn, cid, _ = run(tmp_path, 1, 2)
    hand_entry(conn, cid, 1)
    status, err = case_error(conn, cid)
    assert status == "failed" and err["records"] == [2]
    assert err["message"] == "The AI step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 2." + TAIL_
    assert "RUN_FAILED" in blockers(conn, cid)
    assert [x["record_no"] for x in hand_warnings(conn, cid)] == [1]


def test_a_failure_with_another_cause_is_not_cleared_by_a_hand_entry(tmp_path):
    conn = DB.connect(str(tmp_path / "o.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=extract_down(1), j2=down("j2"), flags=model_flag)), now=lambda: 1.0)
    status, err = case_error(conn, cid)
    assert status == "failed" and "extract_only" not in err
    hand_entry(conn, cid, 1)
    assert case_error(conn, cid)[0] == "failed" and "RUN_FAILED" in blockers(conn, cid)


def test_a_rerun_with_the_record_still_down_keeps_the_hand_entry_and_reads_ready(tmp_path):
    conn, cid, _ = run(tmp_path, 1)
    hand_entry(conn, cid, 1)
    run(tmp_path, 1, again=(conn, cid), now=2.0)
    assert case_error(conn, cid) == ("ready", None)
    assert "e1_m" in {e["id"] for e in DB.list_items(conn, cid, "entry")}      # the pending hand-entered row is not swept as a stale row
    assert [x["record_no"] for x in hand_warnings(conn, cid)] == [1]


def test_a_rerun_that_extracts_the_record_clears_the_failure(tmp_path):
    conn, cid, _ = run(tmp_path, 1)
    assert case_error(conn, cid)[0] == "failed"
    run(tmp_path, again=(conn, cid), now=2.0)
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)


def test_a_rerun_that_recovers_the_record_keeps_the_hand_entry_and_says_the_ai_now_has_one_too(tmp_path):
    """T-165 r2 (blocker): the sweep used to delete e1_m as soon as the AI wrote a live e1 for record 1. Keep both and tell the paralegal; she chooses."""
    conn, cid, _ = run(tmp_path, 1)
    hand_entry(conn, cid, 1)
    run(tmp_path, again=(conn, cid), now=2.0)
    entries = {e["id"]: e for e in DB.list_items(conn, cid, "entry")}
    assert "e1" in entries and "e1_m" in entries
    mine = entries["e1_m"]
    assert mine["review_status"] == "pending" and mine["summary"] == G.records("sample")[0]["excerpt"]      # untouched
    assert (mine["ladder"]["rerun_note"]["kind"], mine["ladder"]["entered_by"]) == ("ai_entry", "reviewer")
    view = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    shown = {e["id"]: e for e in view["entries"]}
    assert shown["e1_m"]["rerun_note"] == "The AI step now has an entry for record 1 (e1) as well. Your entry was kept; keep whichever is right and dismiss the other."
    assert shown["e1"]["rerun_note"] is None
    assert case_error(conn, cid) == ("ready", None)


def test_a_decided_hand_entry_is_also_untouched_when_the_ai_recovers_the_record(tmp_path):
    conn, cid, _ = run(tmp_path, 1)
    hand_entry(conn, cid, 1)
    RV.apply_review(conn, cid, "e1_m", {"action": "accept"})
    run(tmp_path, again=(conn, cid), now=2.0)
    mine = {e["id"]: e for e in DB.list_items(conn, cid, "entry")}["e1_m"]
    assert mine["review_status"] == "accepted"


def test_the_note_goes_when_the_ai_entry_is_gone_again(tmp_path):
    conn, cid, _ = run(tmp_path, 1)
    hand_entry(conn, cid, 1)
    run(tmp_path, again=(conn, cid), now=2.0)
    run(tmp_path, 1, again=(conn, cid), now=3.0)
    mine = {e["id"]: e for e in DB.list_items(conn, cid, "entry")}["e1_m"]
    assert "rerun_note" not in mine["ladder"]
