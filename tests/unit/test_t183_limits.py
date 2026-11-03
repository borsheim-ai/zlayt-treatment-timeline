"""T-183 round 2: the public demo bounds stored cases (DEMO_MAX_CASES, default 200) and runs in flight (DEMO_MAX_RUNS, default 4); both answer a plain
429 `busy`; local/dev mode is unlimited. Fixture backend, no network, no key."""
import json
import re
import threading

import pytest
from fastapi.testclient import TestClient

from app.backend import limits
from app.backend.api import create_app

KEY = "sk-" + "ant-SENTINEL-" + "key-0123456789abcdef"


class Hold:
    """A pipeline stand-in whose runs stay in flight until released."""
    def __init__(self):
        self.gate = threading.Event()
        self.started = threading.Semaphore(0)

    def ingest_case(self, c, cid, text, now):
        from app.backend import pipeline as PL
        return PL.ingest_case(c, cid, text, now)

    def run_pipeline(self, c, token, raw, **k):
        self.started.release()
        self.gate.wait(20)


def _app(tmp_path, monkeypatch, *, local=False, pipeline=None, **env):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    for k in ("ENABLE_LIVE", "DEMO_MAX_CASES", "DEMO_MAX_RUNS", "ZLAYT_MODE"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", KEY)           # present, to prove no 429 body can carry it
    if local:
        monkeypatch.setenv("ZLAYT_MODE", "local")
    for k, v in env.items():
        monkeypatch.setenv(k, str(v))
    (tmp_path / "index.html").write_text("<p>hi</p>")
    return TestClient(create_app(str(tmp_path / "l.sqlite"), static_dir=str(tmp_path), pipeline=pipeline), client=("127.0.0.1", 50000), raise_server_exceptions=False)


def _plain_429(r):
    assert r.status_code == 429
    e = r.json()["error"]
    text = r.text
    assert e["code"] == "busy" and e["message"].endswith(".") and not re.fullmatch(r"[a-z_]+", e["message"])
    for bad in ("Traceback", "File \"", "/Users", "sk-ant", KEY, "sqlite", "Exception", "limits.py", "200", "DEMO_MAX"):
        assert bad not in text, bad
    assert set(r.json()) == {"error"} and set(e) <= {"code", "message", "detail"}
    return e


def _count(c):
    import sqlite3
    return sqlite3.connect(c.app.state.db_path).execute("SELECT COUNT(*) FROM cases").fetchone()[0]


def test_defaults_are_200_cases_and_4_runs_and_a_bad_value_falls_back(monkeypatch):
    for k in ("DEMO_MAX_CASES", "DEMO_MAX_RUNS"):
        monkeypatch.delenv(k, raising=False)
    assert (limits.max_cases(), limits.max_runs()) == (200, 4)
    for bad in ("", "abc", "0", "-3", "2.5"):
        monkeypatch.setenv("DEMO_MAX_CASES", bad)
        monkeypatch.setenv("DEMO_MAX_RUNS", bad)
        assert (limits.max_cases(), limits.max_runs()) == (200, 4), bad
    monkeypatch.setenv("DEMO_MAX_CASES", "7")
    monkeypatch.setenv("DEMO_MAX_RUNS", " 2 ")
    assert (limits.max_cases(), limits.max_runs()) == (7, 2)


def test_the_case_cap_refuses_the_extra_create_with_a_plain_429_and_stores_nothing(tmp_path, monkeypatch):
    c = _app(tmp_path, monkeypatch, DEMO_MAX_CASES=3)
    for _ in range(3):
        assert c.post("/api/cases", json={"sample": True}).status_code == 201
    r = c.post("/api/cases", json={"sample": True})
    e = _plain_429(r)
    assert e["message"] == "This demo is full right now. Try again later." and e["detail"] == {"reason": "demo_full"}
    assert _count(c) == 3
    assert c.get("/api/health").status_code == 200


def test_deleting_a_case_makes_room_again(tmp_path, monkeypatch):
    c = _app(tmp_path, monkeypatch, DEMO_MAX_CASES=1)
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post("/api/cases", json={"sample": True}).status_code == 429
    assert c.delete(f"/api/cases/{tok}").status_code == 204
    assert c.post("/api/cases", json={"sample": True}).status_code == 201


def test_a_refused_text_is_still_409_not_429_and_a_full_demo_does_not_hide_a_bad_request(tmp_path, monkeypatch):
    c = _app(tmp_path, monkeypatch, DEMO_MAX_CASES=1)
    assert c.post("/api/cases", json={"sample": True}).status_code == 201
    assert c.post("/api/cases", json={"text": "x" * 60001}).status_code == 413
    assert c.post("/api/cases", json={"text": "Visit 1/2/2024 knee pain."}).status_code == 409      # unrecorded text is refused before the cap is looked at
    assert c.post("/api/cases", json={}).status_code == 400


def test_the_run_cap_refuses_the_extra_run_with_a_plain_429_and_frees_a_slot_when_a_run_ends(tmp_path, monkeypatch):
    hold = Hold()
    c = _app(tmp_path, monkeypatch, pipeline=hold, DEMO_MAX_RUNS=2)
    toks = [c.post("/api/cases", json={"sample": True}).json()["token"] for _ in range(3)]
    try:
        assert c.post(f"/api/cases/{toks[0]}/run", json={}).status_code == 202
        assert c.post(f"/api/cases/{toks[1]}/run", json={}).status_code == 202
        r = c.post(f"/api/cases/{toks[2]}/run", json={})
        e = _plain_429(r)
        assert e["message"] == "This demo is busy right now. Try again in a minute." and e["detail"] == {"reason": "demo_busy"}
        assert c.get(f"/api/cases/{toks[2]}/status").json()["status"] != "running"      # the refused case was not flipped to running
        assert c.get("/api/health").status_code == 200
    finally:
        hold.gate.set()
    for t in toks[:2]:
        for _ in range(100):
            if c.get(f"/api/cases/{t}/status").json()["status"] != "running":
                break
            threading.Event().wait(0.1)
    assert c.post(f"/api/cases/{toks[2]}/run", json={}).status_code == 202


def test_a_second_run_of_the_same_case_is_still_409_not_429(tmp_path, monkeypatch):
    hold = Hold()
    c = _app(tmp_path, monkeypatch, pipeline=hold, DEMO_MAX_RUNS=1)
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    try:
        assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
        assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 409
    finally:
        hold.gate.set()


def test_local_dev_mode_is_unlimited(tmp_path, monkeypatch):
    hold = Hold()
    c = _app(tmp_path, monkeypatch, local=True, pipeline=hold, DEMO_MAX_CASES=1, DEMO_MAX_RUNS=1)
    try:
        toks = [c.post("/api/cases", json={"sample": True}).json()["token"] for _ in range(4)]
        assert _count(c) == 4
        for t in toks:
            assert c.post(f"/api/cases/{t}/run", json={}).status_code == 202
    finally:
        hold.gate.set()


def test_the_429_body_carries_no_trace_key_or_internal_name_even_in_a_full_busy_demo(tmp_path, monkeypatch):
    hold = Hold()
    c = _app(tmp_path, monkeypatch, pipeline=hold, DEMO_MAX_CASES=1, DEMO_MAX_RUNS=1)
    try:
        tok = c.post("/api/cases", json={"sample": True}).json()["token"]
        assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
        _plain_429(c.post("/api/cases", json={"sample": True}, headers={"x-api-key": KEY}))
        other = _plain_429(c.post("/api/cases", json={"sample": True}))
        assert json.dumps(other).count(KEY) == 0
    finally:
        hold.gate.set()


def test_pure_helpers(monkeypatch):
    monkeypatch.setenv("DEMO_MAX_RUNS", "2")
    assert limits.runs_busy(1, False) is None and limits.runs_busy(2, False) == limits.BUSY_MESSAGE
    assert limits.runs_busy(99, True) is None
