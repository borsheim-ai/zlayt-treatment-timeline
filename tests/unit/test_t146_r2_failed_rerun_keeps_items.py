"""T-146 round 2: no re-run with errors (done_with_errors, failed, deadline) overwrites a decided item, or an item with stored output, with an empty or
partial stub. Errored records keep their previous rows (full row, not a few fields) and the case shows an honest error. T-145 add: a judge that was
called and failed says 'second check is not available' (reason code unchanged), not 'did not run'. T-167: no code appears in any sentence."""
import json

import pytest
from app.backend import pipeline as PL, present, why as WHY
from app.db import db as DB
from app.llm import audited as AU
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script

VOLATILE = {"updated_at"}


def _full(conn, cid, no_ladder=()):
    """Every stored column of every item: a summary-only, excerpt-only or ladder-only change shows up here. `no_ladder`: kinds compared without the ladder (those rows
    are legitimately remade by a re-run whose call numbering differs: only their call ids change)."""
    def clean(c, v):      # T-146 r3: a decided item carries `ladder.rerun_note` after a re-run that failed on it; everything else must be unchanged
        return {a: b for a, b in v.items() if a != "rerun_note"} if c == "ladder" and isinstance(v, dict) else v
    return {k: {i["id"]: {c: clean(c, v) for c, v in i.items() if c not in VOLATILE | ({"ladder"} if k in no_ladder else set())} for i in DB.list_items(conn, cid, k)}
            for k in ("entry", "amount", "flag")}


def _completed(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    assert PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 1.0)["status"] == "done"
    DB.apply_review(conn, "e1", "accept", now=2.0, case=cid)         # decisions made between the runs
    DB.apply_review(conn, "e2", "dismiss", now=2.0, case=cid)
    DB.apply_review(conn, "a1", "accept", now=2.0, case=cid)
    return conn, cid


def _rerun(conn, cid, **script):
    return PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(**script)), now=lambda: 3.0)


def _down(step):
    return AU.LLMFailed(f"{step} down", last_error="TIMEOUT")


def _err(conn, cid):
    c = DB.get_case(conn, cid)
    return c, (json.loads(c["error"]) if c["error"] else None)


def test_extract_down_rerun_keeps_every_stored_row_whole_and_says_so(tmp_path):
    conn, cid = _completed(tmp_path)
    before = _full(conn, cid, ("amount", "flag"))
    out = _rerun(conn, cid, extract=_down("extract"))
    assert out["status"] == "done_with_errors"
    assert _full(conn, cid, ("amount", "flag")) == before                      # summary, excerpt, offsets, ladder, state, review status: all of it
    assert before["entry"]["e1"]["summary"] and before["entry"]["e1"]["review_status"] == "accepted"
    c, err = _err(conn, cid)
    assert c["status"] == "failed" and err["code"] == "run_partial"
    assert "earlier" in err["message"] and "kept" in err["message"] and "finished items" not in err["message"]
    assert "9 " in err["message"]                          # names how many items the failed step touched
    assert out["error"] == err


def test_one_record_failing_keeps_that_row_and_the_rest_are_rerun(tmp_path):
    conn, cid = _completed(tmp_path)
    before = _full(conn, cid)
    sums = sample_script()["extract"]

    def extract(user):
        if "Restrained driver" not in user and "rear-ended" in user:    # only the record that e1 was made from
            raise _down("extract")
        return sums(user)
    out = _rerun(conn, cid, extract=extract)
    after = _full(conn, cid)
    assert after["entry"]["e1"] == before["entry"]["e1"] and after["entry"]["e1"]["summary"]
    assert after["entry"]["e1"]["review_status"] == "accepted" and after["entry"]["e2"]["review_status"] == "dismissed"
    assert out["status"] == "done_with_errors"
    _, err = _err(conn, cid)
    assert err and err["code"] == "run_partial" and "1 " in err["message"]


def test_judge_down_rerun_keeps_judged_rows_instead_of_downgrading_them(tmp_path):
    conn, cid = _completed(tmp_path)
    before = _full(conn, cid)
    assert {r["state"] for r in before["entry"].values()} == {"verified"}
    out = _rerun(conn, cid, j1=_down("j1"), j2=_down("j2"), j3=_down("j3"), j4=_down("j4"))
    assert out["status"] == "done"
    assert _full(conn, cid) == before                      # verified stays verified with its stored judge answer
    c, err = _err(conn, cid)
    assert err and err["code"] == "run_partial" and "second" in err["message"].lower() and "kept" in err["message"]
    assert c["status"] == "failed"


def test_first_run_with_extract_down_still_stores_its_stubs_and_is_failed_with_the_step_named(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=_down("extract"))), now=lambda: 1.0)
    assert out["status"] == "done_with_errors"
    rows = DB.list_items(conn, cid, "entry")
    assert len(rows) == 9 and all(r["state"] == "rejected" and r["state_reasons"] == ["LLM_FAILED_AFTER_RETRIES"] for r in rows)
    c, err = _err(conn, cid)
    assert c["status"] == "failed" and err["code"] == "run_partial" and "(writing the entries)" in err["message"]      # T-161 r2: no entry at all on a first run reads failed, step named


def test_a_later_good_rerun_replaces_the_kept_rows_and_clears_the_error(tmp_path):
    conn, cid = _completed(tmp_path)
    _rerun(conn, cid, extract=_down("extract"))
    out = _rerun(conn, cid)
    assert out["status"] == "done"
    c, err = _err(conn, cid)
    assert err is None and c["status"] == "ready"
    assert DB.get_item(conn, "e1")["review_status"] == "accepted"


def test_deadline_message_says_earlier_and_kept_and_not_finished_items(tmp_path):
    conn, cid = _completed(tmp_path)
    ticks = iter([0.0] + [10_000.0] * 5000)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: next(ticks), deadline_s=480)
    assert out["status"] == "timeout"
    _, err = _err(conn, cid)
    assert err["code"] == "run_deadline"
    assert "earlier" in err["message"] and "kept" in err["message"] and "decision" in err["message"] and "finished items" not in err["message"]


@pytest.mark.parametrize("jump_at", ["verify", "judge_entries", "amounts", "conflicts", "flags"])
def test_deadline_rerun_keeps_the_whole_stored_row_not_only_its_state(tmp_path, jump_at):
    """Full rows (summary, quote, offsets, ladder, state, status): a run stopped at `jump_at` has entries in hand, so a summary-wiping persist would show here."""
    conn, cid = _completed(tmp_path)
    before = _full(conn, cid)
    t = [0.0]

    def on_stage(name):
        if name == jump_at:
            t[0] = 10_000.0
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: t[0], on_stage=on_stage, deadline_s=480)
    assert out["status"] == "timeout"
    assert _full(conn, cid) == before
    assert before["entry"]["e1"]["summary"] and DB.get_item(conn, "e1")["summary"] == before["entry"]["e1"]["summary"]


def _model_flag(user):
    from tests.unit._fakes import which_record
    return {"flags": [dict(type="pre_existing", category="pre_existing", excerpt="CT head negative.")] if which_record(user)[0] == 2 else []}


def test_flag_step_down_rerun_keeps_the_model_flag_it_cannot_rediscover(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=_model_flag)), now=lambda: 1.0)
    assert DB.get_item(conn, "f_r2_1")["origin"] == "llm"
    before = _full(conn, cid, ("amount", "flag", "entry"))["flag"]["f_r2_1"]
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=_down("flags"))), now=lambda: 3.0)
    assert _full(conn, cid, ("amount", "flag", "entry"))["flag"]["f_r2_1"] == before         # not deleted as 'stale'
    _, err = _err(conn, cid)
    assert err and err["code"] == "run_partial" and "kept" in err["message"]


# ---- T-145 minor: a judge that was called and failed is not reported as 'did not run'
def test_a_failed_second_check_says_failed_and_keeps_the_reason_code(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(j1=_down("j1"))), now=lambda: 1.0)
    e = DB.get_item(conn, "e1")
    assert e["state"] == "needs_review" and e["state_reasons"] == ["JUDGE_UNAVAILABLE"]       # the reason code is unchanged
    assert e["ladder"]["judge"]["verdict"] == "unavailable" and e["ladder"]["judge"]["reason_code"] != "JUDGE_NOT_RUN"
    text = present.item_view(conn, cid, "e1")["why"]
    assert "second check is not available" in text.lower() and "JUDGE_NOT_RUN" not in text
    assert "agreed" not in text


def test_a_second_check_that_never_ran_still_says_so_with_its_code(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    ticks = iter([0.0, 0.0, 0.0, 0.0] + [10_000.0] * 5000)       # the deadline passes before judge 1
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: next(ticks), deadline_s=480)
    rows = [r for r in DB.list_items(conn, cid, "entry") if r["state"] != "rejected"]
    if rows:
        assert all((r["ladder"].get("judge") or {}).get("reason_code") == "JUDGE_NOT_RUN" for r in rows)
        assert WHY.why("JUDGE_UNAVAILABLE").startswith("The second AI check did not run")


def test_why_helper_picks_the_sentence_from_the_judge_record():
    failed = {"verdict": "unavailable", "reason_code": "NONE", "call_id": None}
    notrun = {"verdict": "unavailable", "reason_code": "JUDGE_NOT_RUN"}
    assert "second check is not available" in WHY.why("JUDGE_UNAVAILABLE", failed).lower() and "JUDGE_NOT_RUN" not in WHY.why("JUDGE_UNAVAILABLE", failed)
    assert WHY.why("JUDGE_UNAVAILABLE", notrun).startswith("The second AI check did not run")
    assert WHY.why("JUDGE_UNAVAILABLE", None).startswith("The second AI check did not run")                  # no judge record = it did not run
    assert WHY.why("JUDGE_UNSURE", failed) == WHY.why("JUDGE_UNSURE")


def test_a_recorded_answer_miss_is_not_called_a_failed_check():
    failed = {"verdict": "unavailable", "reason_code": "NONE"}
    text = WHY.join(["JUDGE_UNAVAILABLE", "FIXTURE_MISS"], failed)
    assert text.startswith("The second AI check did not run") and "not available" not in text.lower()
