"""D-041 (T-076): an entry with no confirmed date cannot be accepted (single, edit, batch) until confirm_date; the letter never says 'date not stated'."""
import pytest
from fastapi.testclient import TestClient
from app.backend import export as X
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.test_api_routes import run_case


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "x.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def undated_case(c):
    t = run_case(c, G.raw("case_01_date_formats"))
    g = c.get(f"/api/cases/{t}").json()
    rec = [r for r in g["records"] if r["date_status"] == "ambiguous"][0]
    und = [e for e in g["undated_entries"] if rec["id"] in e["record_ids"]]
    assert und, "case_01 must have an undated entry for the ambiguous record"
    return t, g, rec, und[0]


def snapshot(db, t):
    conn = DB.connect(db)
    out = {k: [(i["id"], i["review_status"]) for i in DB.list_items(conn, t, k)] for k in ("entry", "amount", "flag")}
    n = len(DB.list_events(conn, t))
    conn.close()
    return out, n


def test_single_accept_and_edit_on_undated_entry_is_422_and_changes_nothing(env):
    db, c = env
    t, g, rec, e = undated_case(c)
    before = snapshot(db, t)
    r = c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "DATE_UNCONFIRMED"
    r = c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "edit", "edits": {"summary": e["summary"] + " "}})
    assert r.status_code == 422 and r.json()["error"]["code"] == "DATE_UNCONFIRMED"
    assert snapshot(db, t) == before
    # dismiss and reset stay available: the entry can be moved out of the letter
    assert c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "dismiss"}).status_code == 200


def test_batch_with_one_undated_entry_is_422_and_applies_nothing(env):
    db, c = env
    t, g, rec, e = undated_case(c)
    dated_ok = [x["id"] for x in g["entries"] if x["state"] == "verified" and x["review_status"] == "pending"][:2]
    assert dated_ok
    before = snapshot(db, t)
    r = c.post(f"/api/cases/{t}/review/batch", json={"action": "accept", "item_ids": dated_ok + [e["id"]]})
    assert r.status_code == 422 and r.json()["error"]["code"] == "DATE_UNCONFIRMED"
    assert {"id": e["id"], "reason": "date_unconfirmed"} in r.json()["error"]["detail"]["rejected"]
    assert snapshot(db, t) == before


def test_accept_works_after_confirm_date_and_letter_has_no_date_not_stated(env):
    db, c = env
    t, g, rec, e = undated_case(c)
    assert c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "accept"}).status_code == 422
    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]}).status_code == 200
    r = c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "accept"})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "accepted"
    letter = c.get(f"/api/cases/{t}/export").json()["letter_text"]
    assert "date not stated" not in letter.lower()


def test_export_never_puts_an_undated_accepted_entry_in_the_letter(env):
    """Defence in depth: an entry accepted before D-041 (or by a direct DB write) still stays out of the treatment section."""
    db, c = env
    t, g, rec, e = undated_case(c)
    conn = DB.connect(db)
    DB.apply_review(conn, e["id"], "accept", now=1.0, case=t)        # bypasses the HTTP rule on purpose
    conn.close()
    ex = c.get(f"/api/cases/{t}/export").json()
    assert "date not stated" not in ex["letter_text"].lower()
    assert "date not confirmed" in ex["internal_notes_text"]


def test_confirm_date_then_batch_accepts(env):
    db, c = env
    t, g, rec, e = undated_case(c)
    c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]})
    g2 = c.get(f"/api/cases/{t}").json()
    moved = [x for x in g2["entries"] if x["id"] == e["id"]][0]
    if moved["state"] == "verified":
        r = c.post(f"/api/cases/{t}/review/batch", json={"action": "accept", "item_ids": [e["id"]]})
        assert r.status_code == 200 and r.json()["items"][0]["review_status"] == "accepted"


def test_confirm_date_clears_date_ambiguous_on_entry_and_logs_chosen_date(env):
    """T-076 r2 (paralegal F1): after confirm the entry no longer says 'two ways' / needs_review, and the audit names the chosen date."""
    db, c = env
    t, g, rec, e = undated_case(c)
    assert "DATE_AMBIGUOUS" in e["reasons"] and e["state"] == "needs_review"
    chosen = rec["date_candidates"][0]
    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": chosen}).status_code == 200
    item = c.get(f"/api/cases/{t}/items/{e['id']}").json()
    grid = c.get(f"/api/cases/{t}").json()
    ent = next(x for x in grid["entries"] if x["id"] == e["id"])
    assert "DATE_AMBIGUOUS" not in ent["reasons"] and "two ways" not in ent["why"]
    assert ent["state"] != "needs_review" or ent["reasons"]          # needs_review only if another doubt remains
    assert not any(x["id"] == e["id"] for x in grid["undated_entries"])
    assert next(r for r in grid["records"] if r["id"] == rec["id"])["date_status"] == "confirmed"
    assert item is not None
    r = c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "accept"})
    assert r.status_code == 200
    ent = next(x for x in c.get(f"/api/cases/{t}").json()["entries"] if x["id"] == e["id"])
    assert ent["review_status"] == "accepted" and "DATE_AMBIGUOUS" not in ent["reasons"] and "two ways" not in ent["why"]
    conn = DB.connect(db)
    ev = [x for x in DB.list_events(conn, t) if x["action"] == "confirm_date"]
    conn.close()
    assert len(ev) == 1 and ev[0]["after"]["date_chosen"] == chosen and ev[0]["after"]["cleared_date_ambiguous"] == [e["id"]]


def test_confirm_date_keeps_other_doubts_and_rejected_state():
    from app.backend.review import _without_date_doubt as w
    assert w({"state": "needs_review", "state_reasons": ["DATE_AMBIGUOUS"]}) == {"state": "verified", "state_reasons_json": []}
    assert w({"state": "needs_review", "state_reasons": ["DATE_AMBIGUOUS", "JUDGE_UNSURE"]}) == {"state": "needs_review", "state_reasons_json": ["JUDGE_UNSURE"]}
    assert w({"state": "rejected", "state_reasons": ["SCHEMA_INVALID", "DATE_AMBIGUOUS"]}) == {"state": "rejected", "state_reasons_json": ["SCHEMA_INVALID"]}
