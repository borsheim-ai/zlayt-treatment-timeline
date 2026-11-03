"""T-073: the review.py judge path catches only expected judge errors, keeps the error class in the recorded ladder, and lets bugs propagate."""
import pytest
from app.backend import judge_guard, judges, review as RV
from app.db import db as DB
from app.llm import audited as AU, provider as P
from tests.unit.test_review_rules import ent, judge, seeded


def _raising(exc):
    def call(step, system, user, schema, *, item_id=None):
        raise exc
    return call


def test_judges_own_handling_of_llmfailed_is_unavailable():
    assert judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=_raising(AU.LLMFailed()))[:3] == ("unavailable", None, "NONE")


@pytest.mark.parametrize("exc", [AU.LLMFailed(), P.FixtureMissing("abc"), P.LLMError("TIMEOUT")])
def test_guard_turns_expected_errors_into_unavailable_with_class(exc):
    v, cid, code, err = judge_guard.guarded(lambda *a, **k: (_ for _ in ()).throw(exc))
    assert (v, cid, code, err) == ("unavailable", None, "NONE", type(exc).__name__)


def test_guard_passes_a_normal_answer_through():
    v, cid, code, err = judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=judge("supported"))
    assert (v, code, err) == ("supported", "NONE", None)


@pytest.mark.parametrize("exc", [RuntimeError("bug"), KeyError("x"), AttributeError("y")])
def test_guard_does_not_swallow_unexpected_errors(exc):
    with pytest.raises(type(exc)):
        judge_guard.guarded(lambda *a, **k: (_ for _ in ()).throw(exc))


def test_edit_with_expected_judge_error_saves_as_unavailable_and_keeps_class(tmp_path):
    conn, cid, out = seeded(tmp_path)
    eid = ent(out, 5)
    r = RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Pain improving.")), call=_raising(P.FixtureMissing("h")))
    assert [w["code"] for w in r["warnings"]] == ["JUDGE_UNAVAILABLE"]
    jd = DB.get_item(conn, eid, cid)["ladder"]["judge"]
    assert jd["verdict"] == "unavailable" and jd["error_class"] == "FixtureMissing"


def test_edit_with_unexpected_error_propagates_and_saves_nothing(tmp_path):
    conn, cid, out = seeded(tmp_path)
    eid = ent(out, 5)
    before = DB.get_item(conn, eid, cid)
    with pytest.raises(RuntimeError):
        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Pain improving.")), call=_raising(RuntimeError("bug")))
    after = DB.get_item(conn, eid, cid)
    assert after["review_status"] == before["review_status"] and not after.get("edited")


# ---------------------------------------------------------------- r2: the real call path (audited_call underneath), error_class for LLMFailed
def _through_audited(tmp_path, provider):
    """A review `call` that runs the real audited_call over a fake provider, as the pipeline's make_call does."""
    conn = DB.connect(str(tmp_path / "ag.sqlite"))
    cid = DB.create_case(conn, "SYNTHETIC text", now=1.0)

    def call(step, system, user, schema, *, item_id=None, validate=None):
        return AU.audited_call(conn, cid, step, "m", system, user, schema, complete_with_meta=provider, validate=validate, item_id=item_id)
    return conn, cid, call


def _provider(exc):
    n = {"calls": 0}

    def cwm(model, system, user, schema):
        n["calls"] += 1
        raise exc
    cwm.n = n
    return cwm


def test_a_bug_in_the_provider_adapter_propagates_through_the_real_audited_call_and_the_guard(tmp_path):
    conn, cid, call = _through_audited(tmp_path, p := _provider(RuntimeError("programmer bug in provider adapter")))
    with pytest.raises(RuntimeError):
        judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=call)
    assert p.n["calls"] == 1 and len(DB.list_llm_calls(conn, cid)) == 1


def test_a_bug_in_the_provider_adapter_through_apply_review_raises_and_saves_nothing(tmp_path):
    conn, cid, out = seeded(tmp_path)
    eid = ent(out, 5)
    before = DB.get_item(conn, eid, cid)
    _c, _i, call = _through_audited(tmp_path, p := _provider(RuntimeError("programmer bug in provider adapter")))
    with pytest.raises(RuntimeError):
        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Pain improving.")), call=call)
    after = DB.get_item(conn, eid, cid)
    assert p.n["calls"] == 1 and after["review_status"] == before["review_status"] and not after.get("edited")


def test_llmfailed_is_returned_with_its_class_even_though_judges_run_swallows_it():
    v, cid, code, err = judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=_raising(AU.LLMFailed("down")))
    assert (v, cid, code, err) == ("unavailable", None, "NONE", "LLMFailed")


def test_provider_failure_through_the_real_audited_call_records_llmfailed(tmp_path):
    conn, cid, call = _through_audited(tmp_path, p := _provider(P.LLMError("TIMEOUT claude-cli")))
    v, call_id, code, err = judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=call)
    assert (v, err) == ("unavailable", "LLMFailed") and p.n["calls"] == 3


@pytest.mark.parametrize("exc,cls", [(AU.LLMFailed("down"), "LLMFailed"), (AU.LLMFailedFixtureMiss("h"), "LLMFailedFixtureMiss"),
                                     (P.FixtureMissing("h"), "FixtureMissing"), (P.LLMError("TIMEOUT"), "LLMError")])
def test_edit_records_error_class_on_the_ladder_for_every_expected_failure(tmp_path, exc, cls):
    conn, cid, out = seeded(tmp_path)
    eid = ent(out, 5)
    r = RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Pain improving.")), call=_raising(exc))
    assert [w["code"] for w in r["warnings"]] == ["JUDGE_UNAVAILABLE"]
    jd = DB.get_item(conn, eid, cid)["ladder"]["judge"]
    assert jd["verdict"] == "unavailable" and jd["error_class"] == cls


def test_a_judge_that_answers_normally_has_no_error_class(tmp_path):
    conn, cid, out = seeded(tmp_path)
    eid = ent(out, 5)
    RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Pain improving.")), call=judge("supported"))
    assert not DB.get_item(conn, eid, cid)["ladder"]["judge"].get("error_class")
