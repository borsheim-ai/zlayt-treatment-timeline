"""T-175: GET /api/cases (and every per-case route) never answers 500 while cases are created, run, reviewed and deleted at the same time.
Root cause it guards: `case_list.summaries` read the id list, then read each case in its own statements; a case deleted in between (DELETE, the 24 h purge)
made `DB.get_case` return None and the list died with a TypeError (500). Fixture backend, no network; local mode."""
import os
import threading
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import case_list
from app.backend.api import create_app
from app.db import db as DB

# The default unit run does 40 rounds (about 10 s); RACE_FULL=1 runs the full 200, RACE_ITERATIONS=n overrides both.
ITERATIONS = int(os.environ.get("RACE_ITERATIONS", "200" if os.environ.get("RACE_FULL") else "40"))
WORKERS = 4
LIB = "case_lib01_er_only_then_gap"


@pytest.fixture()
def app_env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    app = create_app(str(tmp_path / "t.sqlite"), static_dir=str(tmp_path))
    return app, str(tmp_path / "t.sqlite")


def _client(app):
    return TestClient(app, client=("127.0.0.1", 50000))


def test_list_skips_a_case_deleted_mid_list(app_env, monkeypatch):
    """A case that vanishes between the id SELECT and its read is left out; the rest of the list is returned (200), and the skip is logged."""
    app, path = app_env
    c = _client(app)
    toks = [c.post("/api/cases", json={"library": LIB}).json()["token"] for _ in range(3)]
    real = DB.get_case
    gone = toks[1]

    def flaky(conn, cid):
        if cid == gone:
            DB.delete_case(conn, cid)
        return real(conn, cid)
    monkeypatch.setattr(DB, "get_case", flaky)
    r = c.get("/api/cases")
    assert r.status_code == 200, r.text
    got = [x["token"] for x in r.json()["cases"]]
    assert gone not in got and set(got) == set(toks) - {gone}


def test_list_retries_a_case_whose_summary_fails_once_and_shows_its_full_row(app_env, monkeypatch):
    """A case that is mid-write (summary fails once, then works) is listed with its full, normal row on the same read: no marker, real counts."""
    app, path = app_env
    c = _client(app)
    tok = c.post("/api/cases", json={"library": LIB}).json()["token"]
    real = case_list.summary
    calls = {"n": 0}

    def once(conn, cid, stages):
        if cid == tok:
            calls["n"] += 1
            if calls["n"] == 1:
                raise RuntimeError("half written")
        return real(conn, cid, stages)
    monkeypatch.setattr(case_list, "summary", once)
    r = c.get("/api/cases")
    assert r.status_code == 200, r.text
    row = r.json()["cases"][0]
    assert calls["n"] == 2 and row["token"] == tok
    assert row["status_error"] is False and row["status_error_message"] is None
    assert row["record_count"] and row["counts"] is not None and row["hitl"] is not None


def test_list_marks_a_case_whose_summary_keeps_failing_and_never_shows_zeros(app_env, monkeypatch, caplog):
    """A real bug in summary for a case that exists: the list still answers 200 with the other cases, but that row says status_error with a plain message, every figure is null
    (not 0), and the log has an ERROR line with the exception class only."""
    app, path = app_env
    c = _client(app)
    tok = c.post("/api/cases", json={"library": LIB}).json()["token"]
    other = c.post("/api/cases", json={"library": LIB}).json()["token"]
    real = case_list.summary

    def boom(conn, cid, stages):
        if cid == tok:
            raise RuntimeError("SECRET-RECORD-TEXT")
        return real(conn, cid, stages)
    monkeypatch.setattr(case_list, "summary", boom)
    with caplog.at_level("WARNING", logger="zlayt.api"):
        r = c.get("/api/cases")
    assert r.status_code == 200, r.text
    rows = {x["token"]: x for x in r.json()["cases"]}
    assert set(rows) == {tok, other}
    bad, good = rows[tok], rows[other]
    assert bad["status_error"] is True and bad["status_error_message"] == "We couldn't load this case's status"
    assert bad["record_count"] is None and bad["counts"] is None and bad["progress"] is None and bad["hitl"] is None
    assert bad["export_ready"] is False and bad["next_action"] is None and bad["status"] == "ingested"
    assert set(bad) == set(good)                       # same keys as a full row
    assert good["status_error"] is False and good["record_count"]
    errors = [rec for rec in caplog.records if rec.levelname == "ERROR"]
    assert len(errors) == 1 and "RuntimeError" in errors[0].getMessage() and "SECRET" not in " ".join(x.getMessage() for x in caplog.records)


def test_routes_answer_404_for_a_case_deleted_under_them(app_env, monkeypatch):
    """Every case route that reads the case after its existence check answers 404 (never 500) when the case is deleted in that gap: the first read of the case passes,
    the case is deleted, every later read finds nothing."""
    app, path = app_env
    c = _client(app)
    real = DB.get_case
    state = {"tok": None, "n": 0}

    def vanish(conn, cid):
        if cid == state["tok"]:
            state["n"] += 1
            if state["n"] == 2:
                DB.delete_case(conn, cid)
        return real(conn, cid)
    monkeypatch.setattr(DB, "get_case", vanish)
    routes = (("get", ""), ("get", "/status"), ("get", "/trace"), ("get", "/export"), ("get", "/audit"), ("get", "/judges"), ("get", "/narrative"),
              ("post", "/run"), ("post", "/rejudge"), ("patch", ""), ("delete", ""))
    for method, suffix in routes:
        tok = c.post("/api/cases", json={"library": LIB}).json()["token"]
        state.update(tok=tok, n=0)
        kw = {"json": {"title": "x"}} if method == "patch" else ({"json": {}} if method in ("post",) else {})
        r = getattr(c, method)(f"/api/cases/{tok}{suffix}", **kw)
        assert r.status_code in (200, 202, 204, 404, 409), (method, suffix, r.status_code, r.text)
        if suffix in ("", "/status", "/trace", "/export", "/audit", "/judges", "/narrative") and method == "get":
            assert r.status_code in (200, 404), (method, suffix, r.status_code)
        DB.delete_case(DB.connect(path), tok) if real(DB.connect(path), tok) else None


def test_stress_create_run_review_delete_list(app_env):
    """ITERATIONS rounds of create -> run -> review -> delete across WORKERS threads while two threads list and read cases as fast as they can:
    no response anywhere is a 500."""
    app, path = app_env
    bad, stop, counter = [], threading.Event(), {"i": 0, "lists": 0}
    lock = threading.Lock()

    def note(where, r):
        if r.status_code >= 500:
            with lock:
                bad.append((where, r.status_code, r.text[:200]))

    def worker():
        c = _client(app)
        while True:
            with lock:
                if counter["i"] >= ITERATIONS:
                    return
                counter["i"] += 1
                n = counter["i"]
            r = c.post("/api/cases", json={"library": LIB})
            note("create", r)
            if r.status_code != 201:
                with lock:
                    bad.append(("create", r.status_code, r.text[:200]))
                continue
            tok = r.json()["token"]
            r = c.post(f"/api/cases/{tok}/run", json={})
            note("run", r)
            if n % 2:                                    # half wait for the run and review items; the rest delete a case that is still running
                for _ in range(200):
                    s = c.get(f"/api/cases/{tok}/status")
                    note("status", s)
                    if s.status_code != 200 or s.json()["status"] in ("ready", "failed"):
                        break
                    time.sleep(0.02)
                g = c.get(f"/api/cases/{tok}")
                note("get", g)
                if g.status_code == 200:
                    for it in (g.json()["entries"] + g.json()["flags"] + g.json()["amounts"])[:3]:
                        note("review", c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "accept"}))
            for url in (f"/api/cases/{tok}/trace", f"/api/cases/{tok}/export"):
                note(url.rsplit("/", 1)[1], c.get(url))
            note("delete", c.delete(f"/api/cases/{tok}"))

    def lister():
        c = _client(app)
        while not stop.is_set():
            r = c.get("/api/cases")
            note("list", r)
            with lock:
                counter["lists"] += 1

    ls = [threading.Thread(target=lister, daemon=True) for _ in range(2)]
    ws = [threading.Thread(target=worker, daemon=True) for _ in range(WORKERS)]
    for t in ls + ws:
        t.start()
    for t in ws:
        t.join(timeout=600)
    stop.set()
    for t in ls:
        t.join(timeout=30)
    assert counter["i"] >= ITERATIONS and counter["lists"] > 0
    assert not bad, bad[:5]


def test_unhandled_log_names_class_and_app_frame_but_no_text(app_env, monkeypatch, caplog):
    """The 500 log line carries the exception class and the innermost app frame (file:line) so the cause is findable, and never the message text."""
    app, path = app_env
    c = _client(app)

    def boom(conn, stages):
        raise ValueError("SECRET-RECORD-TEXT")
    monkeypatch.setattr(case_list, "summaries", boom)
    with caplog.at_level("ERROR", logger="zlayt.api"):
        r = c.get("/api/cases")
    assert r.status_code == 500 and "SECRET" not in r.text
    line = " ".join(rec.getMessage() for rec in caplog.records)
    assert "SECRET" not in line
    assert "unhandled ValueError at " in line and ".py:" in line


def test_a_real_error_on_an_existing_cases_route_stays_a_500_and_is_logged(app_env, monkeypatch, caplog):
    """The 404 mapping fires only when the case is gone. An existing case whose route hits a real bug answers 500 'internal' (never 404), the body and the log carry no
    record text, and the log names the exception class and the app frame. The same error for a case that does not exist is a 404."""
    from app.backend import present, trace
    app, path = app_env
    c = _client(app)
    tok = c.post("/api/cases", json={"library": LIB}).json()["token"]

    def boom(*a, **k):
        raise ValueError("SECRET-RECORD-TEXT")
    monkeypatch.setattr(present, "case_view", boom)
    monkeypatch.setattr(trace, "case_trace", boom)
    for suffix in ("", "/trace"):
        caplog.clear()
        with caplog.at_level("WARNING", logger="zlayt.api"):
            r = c.get(f"/api/cases/{tok}{suffix}")
        assert r.status_code == 500, (suffix, r.status_code, r.text)
        assert r.json()["error"]["code"] == "internal" and "SECRET" not in r.text
        msgs = " ".join(rec.getMessage() for rec in caplog.records)
        assert "unhandled ValueError at api.py:" in msgs and "SECRET" not in msgs
        assert any(rec.levelname == "ERROR" for rec in caplog.records)
    r = c.get("/api/cases/no_such_token")
    assert r.status_code == 404


def test_a_failing_existence_probe_is_logged_by_class_and_the_original_500_stands(app_env, monkeypatch, caplog):
    """If the probe that decides 404 vs 500 itself fails, one WARNING names its exception class (no text) and the original error is still a 500."""
    from app.backend import present
    app, path = app_env
    c = _client(app)
    tok = c.post("/api/cases", json={"library": LIB}).json()["token"]
    real = DB.get_case

    state = {"armed": False}

    def probe_fails(conn, cid):
        if state["armed"]:
            raise OSError("SECRET-DISK-TEXT")
        return real(conn, cid)

    def arm(*a, **k):
        state["armed"] = True
        raise ValueError("SECRET-RECORD-TEXT")
    monkeypatch.setattr(present, "case_view", arm)
    monkeypatch.setattr(DB, "get_case", probe_fails)
    with caplog.at_level("WARNING", logger="zlayt.api"):
        r = c.get(f"/api/cases/{tok}")
    assert r.status_code == 500
    msgs = " ".join(rec.getMessage() for rec in caplog.records)
    assert "existence probe" in msgs and "OSError" in msgs and "SECRET" not in msgs
