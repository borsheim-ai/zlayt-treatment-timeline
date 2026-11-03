"""T-145 (GATE-M2 staff blocker): an entry whose second check (judge 1) never ran is never `verified`, says JUDGE_NOT_RUN, and batch accept refuses it."""
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


@pytest.mark.parametrize("jump_at", ["extract", "verify"])      # the clock jumps as that stage starts, so the next guard (verify / judge_entries) fails
def test_deadline_before_judge1_leaves_no_verified_entry(tmp_path, jump_at):
    conn, cid = _case(tmp_path)
    out = _run(conn, cid, Clock(jump_at))
    assert out["status"] == "timeout"
    rows = DB.list_items(conn, cid, "entry")
    assert len(rows) == 9
    for r in rows:
        assert r["state"] == "needs_review" and "JUDGE_UNAVAILABLE" in r["state_reasons"], r["id"]
        jd = r["ladder"]["judge"]
        assert jd["verdict"] == "unavailable" and jd["reason_code"] == "JUDGE_NOT_RUN" and jd["call_id"] is None
        assert r["ladder"]["state"] == "needs_review"
    assert all(e["state"] == "needs_review" for e in out["entries"])
    assert out["counts"]["verified"] == 0 or all(i["state"] != "verified" for i in out["entries"])


def test_deadline_case_view_says_judge_not_run_and_never_that_the_check_agreed(tmp_path):
    conn, cid = _case(tmp_path)
    _run(conn, cid, Clock("verify"))
    for r in DB.list_items(conn, cid, "entry"):
        why = present._common(r)["why"]
        assert "did not run or did not finish" in why and "JUDGE_NOT_RUN" not in why and "agreed" not in why, r["id"]      # T-167: plain sentence, no code


def test_deadline_batch_accept_refuses_every_unjudged_entry(tmp_path):
    conn, cid = _case(tmp_path)
    _run(conn, cid, Clock("verify"))
    ids = [r["id"] for r in DB.list_items(conn, cid, "entry")]
    with pytest.raises(case_extras.BatchRefused) as ex:
        case_extras.apply_batch(conn, cid, {"action": "accept", "item_ids": ids}, 5.0)
    assert {b["reason"] for b in ex.value.rejected} == {"not_verified"} and len(ex.value.rejected) == 9
    assert all(r["review_status"] == "pending" for r in DB.list_items(conn, cid, "entry"))      # all or nothing


def test_normal_run_still_verifies_judged_entries(tmp_path):
    conn, cid = _case(tmp_path)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 1.0)
    assert out["status"] == "done" and all(e["state"] == "verified" and e["ladder"]["judge"]["verdict"] == "supported" for e in out["entries"])


