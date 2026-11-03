"""T-179 / D-066 (GATE-M3 product-manager major): accepting an item the second check disputed (judge verdict disagrees, unsupported or partially, or a
JUDGE_DISAGREES reason) needs the explicit `compared: true` statement ("I compared it with the quote"). Without it: 422 COMPARE_REQUIRED, nothing written.
With it: 200, and the statement is kept in the accept event. Batch accept never includes such an item. An item nobody disputed accepts as before."""
import pytest
from fastapi.testclient import TestClient

from app.backend import review as RV

from app.backend.api import create_app
from app.db import db as DB
from tests.unit.test_api_routes import run_case

CASES = [("partially", "JUDGE_PARTIAL"), ("unsupported", "JUDGE_UNSUPPORTED"), ("disagrees", "JUDGE_DISAGREES")]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "d066.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _dispute(db, tok, item_id, verdict, code, *, reasons=True):
    conn = DB.connect(db)
    try:
        it = DB.get_item(conn, item_id, tok)
        lad = {**(it.get("ladder") or {}), "judge": {"model": "m", "prompt_version": "j1", "call_id": None, "verdict": verdict, "reason_code": None}}
        DB.update_item(conn, item_id, now=9e9, case=tok, state="needs_review", state_reasons_json=[code] if reasons else [], ladder=lad)
    finally:
        conn.close()


def _events(db, tok, item_id):
    conn = DB.connect(db)
    try:
        return DB.list_events(conn, tok, item_id)
    finally:
        conn.close()


def _post(c, tok, item_id, **body):
    return c.post(f"/api/cases/{tok}/items/{item_id}/review", json={"action": "accept", **body})


@pytest.mark.parametrize("verdict,code", CASES)
def test_accept_of_a_disputed_entry_needs_the_compare(env, verdict, code):
    db, c = env
    tok = run_case(c)
    _dispute(db, tok, "e2", verdict, code)
    r = _post(c, tok, "e2")
    assert r.status_code == 422, r.text
    err = r.json()["error"] if "error" in r.json() else r.json()
    blob = r.text
    assert "COMPARE_REQUIRED" in blob and "compared" in blob and verdict in blob
    assert DB.get_item(DB.connect(db), "e2", tok)["review_status"] == "pending"      # nothing written
    assert [e for e in _events(db, tok, "e2") if e["action"] == "accept"] == []
    assert _post(c, tok, "e2", compared=False).status_code == 422
    ok = _post(c, tok, "e2", compared=True)
    assert ok.status_code == 200 and ok.json()["item"]["review_status"] == "accepted"
    acc = [e for e in _events(db, tok, "e2") if e["action"] == "accept"]
    assert len(acc) == 1 and acc[0]["after"]["compared"]["at"], acc          # kept on the review event


def test_the_verdict_alone_or_the_reason_alone_counts(env):
    db, c = env
    tok = run_case(c)
    conn = DB.connect(db)
    DB.update_item(conn, "e3", now=9e9, case=tok, state="needs_review", state_reasons_json=["JUDGE_DISAGREES"])      # reason only
    _dispute(db, tok, "e4", "unsupported", "JUDGE_UNSUPPORTED", reasons=False)                                     # verdict only
    conn.close()
    assert _post(c, tok, "e3").status_code == 422
    assert _post(c, tok, "e4").status_code == 422
    assert _post(c, tok, "e3", compared=True).status_code == 200


def test_an_undisputed_item_accepts_as_before_and_a_bad_compared_is_refused(env):
    db, c = env
    tok = run_case(c)
    assert _post(c, tok, "e1").status_code == 200
    assert not [e for e in _events(db, tok, "e1") if e["action"] == "accept" and "compared" in (e["after"] or {})]       # nothing to compare: nothing recorded
    assert _post(c, tok, "e5", compared=True).status_code == 200      # r2: she said it, but nobody disputed e5, so no stamp (the audit shows only a real compare)
    assert not [e for e in _events(db, tok, "e5") if e["action"] == "accept" and "compared" in (e["after"] or {})]
    assert _post(c, tok, "e4", compared="yes").status_code == 422
    # unsure / unavailable are not an objection
    _dispute(db, tok, "e6", "unsure", "JUDGE_UNSURE")
    assert _post(c, tok, "e6").status_code == 200


def test_dismiss_and_reset_need_no_compare(env):
    db, c = env
    tok = run_case(c)
    _dispute(db, tok, "e2", "partially", "JUDGE_PARTIAL")
    assert c.post(f"/api/cases/{tok}/items/e2/review", json={"action": "dismiss"}).status_code == 200
    assert c.post(f"/api/cases/{tok}/items/e2/review", json={"action": "reset"}).status_code == 200


def test_batch_accept_excludes_a_disputed_item(env):
    db, c = env
    tok = run_case(c)
    _dispute(db, tok, "e2", "partially", "JUDGE_PARTIAL")
    conn = DB.connect(db)
    DB.update_item(conn, "e3", now=9e9, case=tok, state="verified", state_reasons_json=[], ladder={**DB.get_item(conn, "e3", tok)["ladder"], "judge": {"verdict": "disagrees"}})      # even a "verified" row with the verdict is out
    conn.close()
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ["e1", "e2", "e3"]})
    assert r.status_code == 422 and "judge_disputed" in r.text
    rej = {x["id"]: x["reason"] for x in r.json()["error"]["detail"]["rejected"]}
    assert rej == {"e2": "judge_disputed", "e3": "judge_disputed"}, r.text
    assert DB.get_item(DB.connect(db), "e1", tok)["review_status"] == "pending"      # all or nothing
    assert c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ["e1"]}).status_code == 200


# ---------------------------------------------------------------- round 2 (staff-engineer review of f17c991)
def _status(db, tok, item_id):
    conn = DB.connect(db)
    try:
        return DB.get_item(conn, item_id, tok)["review_status"]
    finally:
        conn.close()


def test_a_failed_compared_stamp_takes_the_accept_back(env, monkeypatch):
    db, c = env
    tok = run_case(c)
    _dispute(db, tok, "e2", "disagrees", "JUDGE_DISAGREES")

    def boom(*a, **k):
        raise RuntimeError("stamp write failed")
    monkeypatch.setattr(RV, "_record_compared", boom)
    assert _post(c, tok, "e2", compared=True).status_code == 500
    assert _status(db, tok, "e2") == "pending"                  # never left accepted without the compare on record
    monkeypatch.undo()
    ok = _post(c, tok, "e2", compared=True)
    assert ok.status_code == 200 and _status(db, tok, "e2") == "accepted"
    acc = [e for e in _events(db, tok, "e2") if e["action"] == "accept"][-1]
    assert acc["after"]["compared"]["at"]


def test_the_code_checks_refuse_before_the_compare(env):
    db, c = env
    tok = run_case(c)
    conn = DB.connect(db)
    ed = dict(DB.get_item(conn, "e3", tok)["edited"] or {}, summary="Persistent neck pain 9/10 with daily headaches noted.")      # a figure the quote does not carry
    DB.apply_review(conn, "e3", "edit", edited=ed, now=1.0, case=tok)
    conn.close()
    _dispute(db, tok, "e3", "disagrees", "JUDGE_DISAGREES")
    for body in ({}, {"compared": True}):
        r = _post(c, tok, "e3", **body)
        assert r.status_code == 422 and r.json()["error"]["code"] == "CODE_CHECK_FAILED", r.text         # not COMPARE_REQUIRED
    assert _status(db, tok, "e3") == "edited"


def _amount_env(tmp_path, monkeypatch):
    from tests.unit.test_amounts_d059_api import LEDGER, make_env
    c, tok, _ = make_env(tmp_path, monkeypatch, LEDGER)
    return str(tmp_path / "d059.sqlite"), c, tok


def _amount_dispute(db, tok, item_id, *, verdict="disagree", reasons=()):
    conn = DB.connect(db)
    try:
        it = DB.get_item(conn, item_id, tok)
        lad = {**(it.get("ladder") or {}), "judge": {"model": "m", "prompt_version": "j2", "call_id": None, "verdict": verdict, "reason_code": None}}
        DB.update_item(conn, item_id, now=9e9, case=tok, state="needs_review", state_reasons_json=list(reasons), ladder=lad)
    finally:
        conn.close()


def test_a_disputed_amount_needs_the_compare_on_the_amount_judges_own_verdict(tmp_path, monkeypatch):
    db, c, tok = _amount_env(tmp_path, monkeypatch)
    am = next(a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["kind"] != "damages")
    _amount_dispute(db, tok, am["id"], verdict="disagree", reasons=())          # the amount judge says "disagree"; no JUDGE_* reason to fall back on
    r = _post(c, tok, am["id"])
    assert r.status_code == 422 and r.json()["error"]["code"] == "COMPARE_REQUIRED" and r.json()["error"]["detail"]["verdict"] == "disagrees", r.text
    assert _status(db, tok, am["id"]) == "pending"
    ok = _post(c, tok, am["id"], compared=True)
    assert ok.status_code == 200 and _status(db, tok, am["id"]) == "accepted", ok.text
    acc = [e for e in _events(db, tok, am["id"]) if e["action"] == "accept"]
    assert len(acc) == 1 and acc[0]["after"]["compared"]["at"], acc


def test_a_disputed_flagged_charge_needs_both_statements_compare_first(tmp_path, monkeypatch):
    from tests.unit.test_amounts_d059_api import NOTE, make_env, charges
    c, tok, _ = make_env(tmp_path, monkeypatch, NOTE)
    db = str(tmp_path / "d059.sqlite")
    for a in [a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["kind"] != "damages"]:
        assert c.post(f"/api/cases/{tok}/items/{a['id']}/reclassify", json={"to": "charge"}).status_code == 200
    f = next(a for a in charges(c, tok) if a["flag"])
    assert f["flag"]["flag"] == "likely_duplicate"
    _amount_dispute(db, tok, f["id"], verdict="disagree", reasons=())
    code = lambda r: r.json()["error"]["code"]
    assert code(_post(c, tok, f["id"])) == "COMPARE_REQUIRED"                                  # compare first (documented order)
    assert code(_post(c, tok, f["id"], confirm="likely_duplicate")) == "COMPARE_REQUIRED"
    assert code(_post(c, tok, f["id"], compared=True)) == "CONFIRM_REQUIRED"
    assert _status(db, tok, f["id"]) == "pending" and not [e for e in _events(db, tok, f["id"]) if e["action"] == "accept"]
    ok = _post(c, tok, f["id"], compared=True, confirm="likely_duplicate")
    assert ok.status_code == 200, ok.text
    acc = [e for e in _events(db, tok, f["id"]) if e["action"] == "accept"]
    assert len(acc) == 1 and acc[0]["after"]["compared"]["at"] and acc[0]["after"]["confirm"], acc
