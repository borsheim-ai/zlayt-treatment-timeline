"""T-146 (GATE-M2 staff major): a failed or timed-out re-run keeps every previous item and decision, as its error message says."""
import json

import pytest
from app.backend import case_extras, pipeline as PL, present
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script


class Clock:
    """Injected clock: jumps past the deadline when a named stage starts (on_stage), so the run stops exactly there."""
    def __init__(self, jump_at=None):
        self.t, self.jump_at = 0.0, jump_at

    def __call__(self):
        return self.t

    def on_stage(self, name):
        if name == self.jump_at:
            self.t = 10_000.0


def _case(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    return conn, DB.create_case(conn, G.raw("sample"), now=0.0)


def _run(conn, cid, clock):
    return PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=clock, on_stage=clock.on_stage, deadline_s=480)


def _snapshot(conn, cid):
    return {k: {i["id"]: (i["review_status"], i["state"], i["state_reasons"]) for i in DB.list_items(conn, cid, k)} for k in ("entry", "amount", "flag")}


@pytest.mark.parametrize("jump_at", ["extract", "verify", "judge_entries", "flags"])
def test_timed_out_rerun_keeps_every_previous_item_and_decision(tmp_path, jump_at):
    conn, cid = _case(tmp_path)
    first = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 1.0)
    assert first["status"] == "done"
    before = _snapshot(conn, cid)
    assert len(before["entry"]) == 9 and len(before["flag"]) >= 10
    DB.apply_review(conn, "e1", "accept", now=2.0, case=cid)             # a decision made between the runs
    before["entry"]["e1"] = ("accepted",) + before["entry"]["e1"][1:]
    out = _run(conn, cid, Clock(jump_at))
    assert out["status"] == "timeout"
    c = DB.get_case(conn, cid)
    assert c["status"] == "failed" and json.loads(c["error"])["code"] == "run_deadline"
    assert _snapshot(conn, cid) == before          # nothing deleted, nothing downgraded, the decision stands


def test_timed_out_rerun_between_flags_of_two_records_keeps_the_flags(tmp_path):
    conn, cid = _case(tmp_path)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 1.0)
    before = _snapshot(conn, cid)
    clock = Clock()
    calls = {"n": 0}
    real = PL.FL.run_flag_pass

    def flag_pass(r, **kw):
        calls["n"] += 1
        if calls["n"] == 4:                         # the deadline passes after the third record's flags
            clock.t = 10_000.0
        return real(r, **kw)
    PL.FL.run_flag_pass = flag_pass
    try:
        out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=clock, deadline_s=480)
    finally:
        PL.FL.run_flag_pass = real
    assert out["status"] == "timeout"
    assert _snapshot(conn, cid) == before


def test_first_run_that_times_out_still_stores_what_finished(tmp_path):
    conn, cid = _case(tmp_path)
    out = _run(conn, cid, Clock("amounts"))
    assert out["status"] == "timeout" and len(DB.list_items(conn, cid, "entry")) == 9
    assert [f for f in DB.list_items(conn, cid, "flag") if f["type"] == "gap"]
