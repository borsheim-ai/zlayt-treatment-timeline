"""Batch accept of verified entries (atomic, entries only) and per-case export config (D-031; T-055, T-058)."""
import time
import pytest
from fastapi.testclient import TestClient
from app.backend import export as X
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.test_api_routes import wait_ready, run_case
from tests.unit.test_export import build_case


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "x.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def items(c, tok):
    v = c.get(f"/api/cases/{tok}").json()
    return v


def statuses(db, tok):
    conn = DB.connect(db)
    out = {k: {i["id"]: (i["review_status"], i["state"]) for i in DB.list_items(conn, tok, k)} for k in ("entry", "amount", "flag")}
    conn.close()
    return out


def test_batch_accepts_verified_entries_only_and_logs_one_event_each(env):
    db, c = env
    tok = run_case(c)
    st = statuses(db, tok)
    ver = [i for i, (rs, s) in st["entry"].items() if s == "verified" and rs == "pending"]
    assert len(ver) >= 7
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ver})
    assert r.status_code == 200 and [x["review_status"] for x in r.json()["items"]] == ["accepted"] * len(ver)
    assert {"totals", "review", "warnings"} <= set(r.json())
    conn = DB.connect(db)
    ev = [e for e in DB.list_events(conn, tok) if e["action"] == "accept"]
    assert sorted(e["item_id"] for e in ev) == sorted(ver)
    st2 = statuses(db, tok)
    assert all(rs == "pending" for rs, _ in list(st2["amount"].values()) + list(st2["flag"].values()))
    u = c.post(f"/api/cases/{tok}/review/batch", json={"action": "reset", "item_ids": ver})
    assert u.status_code == 200 and all(x["review_status"] == "pending" for x in u.json()["items"])


def test_batch_refuses_amounts_flags_and_unverified_and_applies_nothing(env):
    db, c = env
    tok = run_case(c)
    st = statuses(db, tok)
    ver = [i for i, (rs, s) in st["entry"].items() if s == "verified"]
    nonver = [i for i, (rs, s) in st["entry"].items() if s != "verified"]
    amount, flag = next(iter(st["amount"])), next(iter(st["flag"]))
    bad = [flag] + nonver[:1]
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ver + bad})
    assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_batch"
    reasons = {x["id"]: x["reason"] for x in r.json()["error"]["detail"]["rejected"]}
    assert reasons[flag] == "not_an_entry"
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ver + [amount]})        # D-059: a charge is never in a batch
    assert r.status_code == 422 and r.json()["error"]["code"] == "CHARGES_NOT_BATCHED"
    assert {x["id"]: x["reason"] for x in r.json()["error"]["detail"]["rejected"]}[amount] == "charge_in_batch"
    assert statuses(db, tok) == st                                    # nothing applied
    assert c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": []}).status_code == 400
    assert c.post(f"/api/cases/{tok}/review/batch", json={"action": "dismiss", "item_ids": ver}).status_code == 400
    assert c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ["e999"]}).json()["error"]["detail"]["rejected"][0]["reason"] == "not_found"


def test_batch_is_atomic_when_a_write_fails_midway(env, monkeypatch):
    db, c = env
    tok = run_case(c)
    st = statuses(db, tok)
    ver = [i for i, (rs, s) in st["entry"].items() if s == "verified"][:4]
    real, n = DB.apply_review, {"n": 0}

    def flaky(conn, item_id, action, **kw):
        if action == "accept":
            n["n"] += 1
            if n["n"] == 3:
                raise RuntimeError("disk")
        return real(conn, item_id, action, **kw)
    monkeypatch.setattr(DB, "apply_review", flaky)
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ver})
    assert r.status_code == 500
    assert statuses(db, tok)["entry"] == st["entry"]                  # the two applied items were put back


def test_export_config_roundtrip_validation_and_delete(env):
    db, c = env
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    url = f"/api/cases/{tok}/export_config"
    assert c.get(url).json() == {"exhibit": None, "bates_prefix": None, "bates_start": None}
    r = c.put(url, json={"exhibit": "7", "bates_prefix": "RIV-", "bates_start": 1})
    assert r.status_code == 200 and r.json() == {"exhibit": "7", "bates_prefix": "RIV-", "bates_start": 1}
    assert c.get(url).json()["exhibit"] == "7"
    for bad in ({"exhibit": "x" * 21}, {"bates_prefix": "<b>"}, {"bates_start": -1}, {"bates_start": 1e9}, {"bates_start": "1"}, {"foo": 1}, {"bates_start": True}):
        assert c.put(url, json=bad).status_code == 422, bad
    assert c.get(url).json()["exhibit"] == "7"                       # a refused PUT changes nothing
    assert c.delete(url).json() == {"exhibit": None, "bates_prefix": None, "bates_start": None}
    assert c.get(f"/api/cases/nope/export_config").status_code == 404


def test_default_export_is_byte_identical_to_golden_and_config_fills_the_citation():
    letter, notes = G.export_blocks()
    out = X.build_export(build_case())
    assert out["letter_text"] == letter.rstrip("\n") and out["internal_notes_text"] == notes.rstrip("\n")
    empty = build_case(); empty["export_config"] = {"exhibit": None, "bates_prefix": None, "bates_start": None}
    assert X.build_export(empty)["letter_text"] == letter.rstrip("\n")
    cfg = build_case(); cfg["export_config"] = {"exhibit": "7", "bates_prefix": "RIV-", "bates_start": 1}
    txt = X.build_export(cfg)["letter_text"]
    assert 'Source [Ex. 7 / Bates RIV-0001]: "41M restrained driver' in txt          # record 1
    assert 'Source [Ex. 7 / Bates RIV-0008]: "C5-C6 disc protrusion' in txt        # record 8
    assert txt.count("[Ex. 7 / Bates RIV-") == len([e for e in cfg["entries"]]) + 2     # every letter citation (entries + two charges)
    part = build_case(); part["export_config"] = {"exhibit": "A", "bates_prefix": None, "bates_start": None}
    assert 'Source [Ex. A / Bates __]: "41M' in X.build_export(part)["letter_text"]
    assert X.build_export(cfg)["internal_notes_text"] == notes.rstrip("\n")           # notes never carry the exhibit numbers


# ---- T-055 review F1/F2: the sample has no needs_review or rejected entry, so build one and assert the server rule
@pytest.mark.parametrize("state", ["needs_review", "rejected"])
def test_batch_refuses_a_non_verified_entry_with_not_verified_and_changes_nothing(env, state):
    db, c = env
    tok = run_case(c)
    ver = [i for i, (rs, s) in statuses(db, tok)["entry"].items() if s == "verified" and rs == "pending"]
    odd, rest = ver[0], ver[1:5]
    conn = DB.connect(db)
    DB.update_item(conn, odd, now=0, case=tok, state=state)
    conn.commit(); conn.close()
    st = statuses(db, tok)
    assert st["entry"][odd][1] == state                                  # the fixture really holds the state under test
    conn = DB.connect(db); ev_before = DB.list_events(conn, tok); conn.close()
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": rest + [odd]})
    assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_batch"
    assert r.json()["error"]["detail"]["rejected"] == [{"id": odd, "reason": "not_verified"}]
    assert statuses(db, tok) == st                                       # the verified ids in the same batch were not touched
    conn = DB.connect(db); assert DB.list_events(conn, tok) == ev_before; conn.close()


# ---- T-058 security review: a trailing newline must not pass the label check (re `$` matches before a final newline)
@pytest.mark.parametrize("bad", [{"exhibit": "7\n"}, {"bates_prefix": "RIV-\n"}, {"exhibit": "\n7"}, {"exhibit": "7\r\n"}, {"exhibit": "7\n\n"}])
def test_export_config_with_a_newline_is_422_and_nothing_is_stored(env, bad):
    db, c = env
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    url = f"/api/cases/{tok}/export_config"
    assert c.put(url, json={"exhibit": "7"}).status_code == 200
    r = c.put(url, json=bad)
    assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_edit", bad
    assert c.get(url).json() == {"exhibit": "7", "bates_prefix": None, "bates_start": None}


def test_no_backend_validator_accepts_a_trailing_newline():
    from app.backend import amounts, dates
    from app.llm import _types
    assert amounts.to_cents("12\n") is None and amounts.to_cents("12") == 1200
    assert dates._ISO.match("2026-01-05\n") is None and dates._NUM.match("1/5/2026\n") is None
    assert dates._MDY.match("Jan 5, 2026\n") is None and dates._DMY.match("5 Jan 2026\n") is None
    assert _types._FENCE.match("```json\n{}\n```\n") is None
