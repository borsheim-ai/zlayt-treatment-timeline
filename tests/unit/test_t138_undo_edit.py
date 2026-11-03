"""T-138 (staff-engineer r2 on T-134, pre-existing): undoing an edit must put the AI wording back TOGETHER with the second-check result and the
state it had before the edit. Before this, reset restored the words but kept the edit route's judge result ('unavailable' when the re-check had no
answer), so an item that was verified before the edit hit 422 JUDGE_NOT_RUN on accept."""
import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from app.db import db as DB
from tests.unit.test_api_routes import run_case

EDIT = "Persistent neck pain 6/10 with daily headaches noted."


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "t138.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _post(c, tok, iid, body):
    return c.post(f"/api/cases/{tok}/items/{iid}/review", json=body)


def _snap(db, tok, iid):
    conn = DB.connect(db)
    r = DB.get_item(conn, iid, tok)
    conn.close()
    return {"state": r["state"], "reasons": sorted(r["state_reasons"] or []), "judge": (r["ladder"] or {}).get("judge"),
            "code_checks": (r["ladder"] or {}).get("code_checks"), "summary": r["summary"], "excerpt": r["excerpt"]}


def test_undo_of_an_edit_restores_the_ai_wording_with_its_original_judge_result_and_accept_then_works(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    assert before["judge"]["verdict"] in ("supported", "faithful") and before["judge"]["verdict"] != "unavailable"       # the AI wording had a real second-check answer
    assert _post(c, tok, "e1", {"action": "accept"}).status_code == 200
    r = _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}})
    assert r.status_code == 200
    during = _snap(db, tok, "e3")
    assert during["judge"] != before["judge"]                                           # the edit re-ran the check on her wording
    r = _post(c, tok, "e3", {"action": "reset"})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "pending"
    after = _snap(db, tok, "e3")
    assert after["judge"] == before["judge"] and after["code_checks"] == before["code_checks"]
    assert (after["state"], after["reasons"]) == (before["state"], before["reasons"])
    assert after["summary"] == before["summary"] and r.json()["item"]["summary"] == before["summary"]
    # accept works exactly as it did before the edit, and the export is not blocked by JUDGE_NOT_RUN
    assert _post(c, tok, "e3", {"action": "accept"}).status_code == 200
    ex = c.get(f"/api/cases/{tok}/export")
    blockers = [] if ex.status_code == 200 else str(ex.json())
    assert "JUDGE_NOT_RUN" not in blockers and "JUDGE_UNAVAILABLE" not in blockers


def test_two_edits_then_one_undo_restores_the_state_before_the_first_edit(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": "Persistent neck pain 6/10 and daily headaches."}}).status_code == 200
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    after = _snap(db, tok, "e3")
    assert after["judge"] == before["judge"] and (after["state"], after["reasons"]) == (before["state"], before["reasons"])


def test_a_second_edit_after_an_undo_snapshots_again(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    for _ in range(2):
        assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
        assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
        assert _snap(db, tok, "e3")["judge"] == before["judge"]


def test_undo_after_accepting_the_edit_also_restores_the_original_check(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    assert _post(c, tok, "e3", {"action": "accept"}).status_code == 200
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    after = _snap(db, tok, "e3")
    assert after["judge"] == before["judge"] and (after["state"], after["reasons"]) == (before["state"], before["reasons"])


def test_undo_of_an_item_with_no_snapshot_old_data_still_works(env):
    """Rows edited before this change have no stored snapshot; reset behaves as before (words back, nothing invented)."""
    db, c = env
    tok = run_case(c)
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    conn = DB.connect(db)
    row = DB.get_item(conn, "e3", tok)
    lad = dict(row["ladder"])
    lad.pop("pre_edit", None)
    DB.update_item(conn, "e3", case=tok, ladder=lad)
    conn.close()
    r = _post(c, tok, "e3", {"action": "reset"})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "pending"


def test_undo_of_a_flag_note_or_an_unedited_item_is_unchanged(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    assert _post(c, tok, "e3", {"action": "accept"}).status_code == 200
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    assert _snap(db, tok, "e3") == before


def test_undo_when_something_else_changed_the_state_since_the_edit_restores_the_check_but_leaves_the_state(env):
    db, c = env
    tok = run_case(c)
    before = _snap(db, tok, "e3")
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    conn = DB.connect(db)
    DB.update_item(conn, "e3", case=tok, state="needs_review", state_reasons_json=["DATE_AMBIGUOUS"])      # some other step rewrote it
    conn.close()
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    after = _snap(db, tok, "e3")
    assert after["judge"] == before["judge"]
    assert (after["state"], after["reasons"]) == ("needs_review", ["DATE_AMBIGUOUS"])


# ---- T-138 round 2 (staff-engineer r1): the snapshot must not alias the dict the edit updates in place; the snapshot goes after the undo; pre_edit is not in GET case
def _set_ladder(db, tok, iid, **kw):
    conn = DB.connect(db)
    lad = dict(DB.get_item(conn, iid, tok)["ladder"] or {})
    lad.update(kw)
    DB.update_item(conn, iid, case=tok, ladder=lad)
    conn.close()


def test_undo_restores_the_pre_edit_code_checks_not_the_edited_wordings(env):
    """r1 finding 1 (mutants T3 and the alias): an AI draft whose stored code checks differ from what the edit writes."""
    db, c = env
    tok = run_case(c)
    old = {"qualifier_carried": False, "summary_tokens_not_in_excerpt": ["5/10"], "highlight_found": True}
    _set_ladder(db, tok, "e3", code_checks=dict(old))
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    during = _snap(db, tok, "e3")["code_checks"]
    assert during != old and during["qualifier_carried"] is True and during["summary_tokens_not_in_excerpt"] == []
    conn = DB.connect(db)
    snap = DB.get_item(conn, "e3", tok)["ladder"]["pre_edit"]
    conn.close()
    assert snap["code_checks"] == old                                                  # the snapshot itself is the old record, not an alias of the edited one
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    assert _snap(db, tok, "e3")["code_checks"] == old


def test_second_undo_cycle_restores_what_the_item_had_after_the_first_undo_and_the_snapshot_is_gone(env):
    """r1 finding 3 (mutant T9): the snapshot is removed by the undo, so a later edit snapshots what the item holds THEN."""
    db, c = env
    tok = run_case(c)
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    conn = DB.connect(db)
    assert "pre_edit" not in (DB.get_item(conn, "e3", tok)["ladder"] or {})
    cur = (DB.get_item(conn, "e3", tok)["ladder"] or {}).get("judge")
    conn.close()
    changed = dict(cur, verdict="partial", reason_code="CHANGED_BETWEEN_CYCLES")
    _set_ladder(db, tok, "e3", judge=changed)                                           # something (a rejudge) changed the check between the cycles
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    assert _snap(db, tok, "e3")["judge"] == changed


def test_undo_restores_the_rerun_record_the_old_wording_had_and_an_edit_clears_it(env):
    """T-134 r3 finding 2: ladder.rejudge belongs to the wording and quote it ran on."""
    db, c = env
    tok = run_case(c)
    attempts = [{"at": 1.0, "call_id": "c1", "verdict": "unavailable"}]
    _set_ladder(db, tok, "e3", rejudge=attempts)
    assert _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}}).status_code == 200
    conn = DB.connect(db)
    assert not DB.get_item(conn, "e3", tok)["ladder"].get("rejudge")
    conn.close()
    assert _post(c, tok, "e3", {"action": "reset"}).status_code == 200
    conn = DB.connect(db)
    assert DB.get_item(conn, "e3", tok)["ladder"].get("rejudge") == attempts
    conn.close()


def test_pre_edit_snapshot_is_not_in_any_case_payload(env):
    """r1 finding 2: the snapshot is internal (api.md); it is not in GET case, the review response or the list payloads."""
    db, c = env
    tok = run_case(c)
    r = _post(c, tok, "e3", {"action": "edit", "edits": {"summary": EDIT}})
    assert r.status_code == 200 and "pre_edit" not in r.text
    assert "pre_edit" not in c.get(f"/api/cases/{tok}").text
    conn = DB.connect(db)
    assert "pre_edit" in DB.get_item(conn, "e3", tok)["ladder"]                        # still stored, only hidden
    conn.close()
