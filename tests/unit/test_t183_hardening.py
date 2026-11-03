"""T-183 (M4 hardening check): the server-side key is never exposed or logged, the public build makes no model call and serves the prepared
sample answers with no key, a key cannot be supplied by a request (BYOK is cut, D-011), input size limits hold at the HTTP layer, and every
error state is plain JSON. Fixture backend; the live path uses a fake SDK client. No network, no real key (the key below is a sentinel)."""
import json
import logging
import pathlib
import re
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import ingest
from app.backend.api import MAX_BODY_BYTES, create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]
KEY = "sk-" + "ant-SENTINEL-" + "key-0123456789abcdef"      # built in two parts so the secret scan does not take a test sentinel for a key


def _client(tmp_path, monkeypatch, *, live=False, local=False, key=None):
    monkeypatch.setenv("LLM_BACKEND", "anthropic-api" if live else "fixture")
    for k, v in (("ENABLE_LIVE", "1" if live else None), ("ANTHROPIC_API_KEY", key), ("PROVIDER_CAP_CONFIRMED", "1" if live else None),
                 ("ZLAYT_MODE", "local" if local else None)):
        monkeypatch.delenv(k, raising=False) if v is None else monkeypatch.setenv(k, v)
    (tmp_path / "index.html").write_text("<p>hi</p>")
    return TestClient(create_app(str(tmp_path / "t183.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000), raise_server_exceptions=False)


def _wait(c, tok, ok=("ready", "failed", "done_with_errors")):
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ok:
            return s
        time.sleep(0.25)
    raise AssertionError(s)


# ---------------------------------------------------------------- 1. the key never reaches the browser or a log
def test_key_never_appears_in_any_response_or_log_even_when_the_sdk_error_echoes_it(tmp_path, monkeypatch, caplog, capsys):
    """Live path with every call failing and the SDK error carrying the key: nothing the browser can fetch, and nothing logged, contains it."""
    import anthropic
    from app.llm import audited as AU

    class Boom:
        def __init__(self, *a, **k):
            assert k.get("api_key") == KEY            # the key is used server-side, here and only here
            self.messages = self
        def create(self, **kw):
            raise RuntimeError(f"401 invalid x-api-key {KEY}")
    monkeypatch.setattr(anthropic, "Anthropic", Boom)
    monkeypatch.setattr(AU.time, "sleep", lambda s: None)
    caplog.set_level(logging.DEBUG)
    c = _client(tmp_path, monkeypatch, live=True, key=KEY)
    h = c.get("/api/health")
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    s = _wait(c, tok)
    seen = [h.text, json.dumps(dict(h.headers)), json.dumps(s)]
    for path in ("", "/audit", "/trace", "/status", "/export"):
        r = c.get(f"/api/cases/{tok}{path}")
        seen += [r.text, json.dumps(dict(r.headers))]
    seen += [c.get("/").text, c.get("/api/nope").text, c.get(f"/api/cases/{tok}", headers={"x-api-key": KEY}).text]
    out = capsys.readouterr()
    blob = "\n".join(seen) + caplog.text + out.out + out.err
    assert KEY not in blob and "sk-" + "ant" not in blob and "ANTHROPIC_API_KEY" not in blob
    assert s["status"] in ("failed", "done_with_errors", "ready")
    assert c.get("/api/health").json()["live_enabled"] is True      # live really was on: the absence above is not an accident of demo mode


def test_no_static_file_or_api_text_names_the_key_or_a_key_field():
    """The shipped frontend never mentions the env var, a key prefix or a key input; the health payload has no key-shaped field."""
    hits = []
    for p in (ROOT / "app" / "frontend").rglob("*"):
        if p.is_file() and p.suffix in (".js", ".html", ".css", ".json", ".svg", ".mjs") and "dev" not in p.parts:
            t = p.read_text(errors="ignore")
            if re.search(r"ANTHROPIC_API_KEY|sk-ant|x-api-key|api[_-]?key", t, re.I):
                hits.append(str(p.relative_to(ROOT)))
    assert hits == [], hits


def test_health_reports_whether_live_is_on_but_never_the_key_or_cap_setting(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, live=True, key=KEY)
    body = c.get("/api/health").text
    assert KEY not in body and "PROVIDER_CAP" not in body and "api_key" not in body.lower()


def test_env_example_and_repo_tree_carry_no_real_key():
    ex = ROOT / ".env.example"
    if ex.exists():
        for line in ex.read_text().splitlines():
            if line.startswith("ANTHROPIC_API_KEY"):
                assert line.split("=", 1)[1].strip() in ("", '""', "''"), "the example file must not carry a key"
    assert (ROOT / "tools" / "check_secrets.py").exists()           # the pre-commit scan (git-guard) that keeps keys out of git


# ---------------------------------------------------------------- 2. no model call without ENABLE_LIVE; spend control is the provider-side cap
def test_every_route_that_can_call_a_model_makes_zero_calls_in_demo_mode_even_with_a_key(tmp_path, monkeypatch):
    """The public Space may hold a key as a secret; without ENABLE_LIVE=1 no route (run, rejudge, manual entry) reaches the SDK or the CLI."""
    import anthropic
    from app.llm.backends import claude_cli as CLI
    calls = []
    monkeypatch.setattr(anthropic, "Anthropic", lambda *a, **k: calls.append("sdk"))
    monkeypatch.setattr(CLI.subprocess, "run", lambda *a, **k: calls.append("cli"))
    c = _client(tmp_path, monkeypatch, key=KEY)
    monkeypatch.setenv("LLM_BACKEND", "anthropic-api")                # as a Space would be configured: live backend named, key present, live NOT enabled
    h = c.get("/api/health").json()
    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    assert _wait(c, tok)["status"] == "ready"
    assert c.post(f"/api/cases/{tok}/rejudge", json={}).status_code in (200, 409)
    case = c.get(f"/api/cases/{tok}").json()
    rid = case["entries"][0]["record_id"] if case["entries"] and "record_id" in case["entries"][0] else None
    if rid:
        c.post(f"/api/cases/{tok}/records/{rid}/entry", json={"date": "2026-01-01", "summary": "x", "excerpt": "x"})
    assert calls == []


def test_a_live_api_build_refuses_to_start_without_the_provider_side_spend_limit_confirmed(tmp_path, monkeypatch):
    """The spend cap is a provider-side limit (D-020, ADR-006); the app will not start live on the API without the owner confirming it is set."""
    monkeypatch.setenv("LLM_BACKEND", "anthropic-api"); monkeypatch.setenv("ENABLE_LIVE", "1"); monkeypatch.setenv("ANTHROPIC_API_KEY", KEY)
    monkeypatch.delenv("PROVIDER_CAP_CONFIRMED", raising=False)
    with pytest.raises(RuntimeError, match="PROVIDER_CAP_CONFIRMED"):
        create_app(str(tmp_path / "a.sqlite"), static_dir=str(tmp_path))


def test_live_work_per_run_is_bounded_by_the_input_limits():
    """No in-app rate limiter (cut, D-020): the most one run can ask a model is bounded by MAX_CHARS and MAX_RECORDS."""
    assert ingest.MAX_CHARS == 60_000 and ingest.MAX_RECORDS == 40


# ---------------------------------------------------------------- 3. demo mode with no key serves the prepared sample answers
def test_no_key_demo_runs_the_sample_to_ready_with_prepared_answers_and_refuses_other_text(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch)
    h = c.get("/api/health").json()
    assert h["demo_mode"] is True and h["live_enabled"] is False and h["backend"] == "fixture" and h["synthetic_only"] is True and h["banner"]
    assert h["answers"] in ("prepared", "recorded") and h["sample_available"] is True
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    assert _wait(c, tok)["status"] == "ready"
    case = c.get(f"/api/cases/{tok}").json()
    assert case["entries"] and case["demo_mode"] is True
    r = c.post("/api/cases", json={"text": "=== Record 1 ===\nDate: 2026-01-01\nSource: X\nExcerpt: \"Anything new.\""})
    assert r.status_code == 409 and r.json()["error"]["code"] == "demo_mode_unsupported_input"
    assert "recorded sample cases" in r.json()["error"]["message"]


# ---------------------------------------------------------------- 4. bring-your-own-key is cut (D-011): a request cannot supply or switch a key
@pytest.mark.parametrize("hdrs,body", [({"x-api-key": KEY}, {"sample": True}), ({"authorization": f"Bearer {KEY}"}, {"sample": True}),
                                       ({}, {"sample": True, "api_key": KEY, "anthropic_api_key": KEY, "enable_live": True, "backend": "anthropic-api"})])
def test_a_key_sent_with_a_request_is_never_used_or_echoed(tmp_path, monkeypatch, hdrs, body):
    import anthropic
    calls = []
    monkeypatch.setattr(anthropic, "Anthropic", lambda *a, **k: calls.append(k))
    c = _client(tmp_path, monkeypatch)
    r = c.post("/api/cases", json=body, headers=hdrs)
    assert r.status_code == 201 and KEY not in r.text and r.json()["demo_mode"] is True
    tok = r.json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json=body, headers=hdrs).status_code == 202
    assert _wait(c, tok)["status"] == "ready"
    assert calls == [] and KEY not in c.get(f"/api/cases/{tok}", headers=hdrs).text and c.get("/api/health").json()["live_enabled"] is False


# ---------------------------------------------------------------- 5. input size limits at the HTTP layer
def test_character_and_record_limits_return_413_and_store_nothing(tmp_path, monkeypatch):
    from app.db import db as DB
    c = _client(tmp_path, monkeypatch, live=True, key=KEY)            # live (any text accepted) so the limit, not the demo gate, is what answers
    big = 'Date: 2026-01-01\nSource: A\nExcerpt: "' + "y" * 60_000 + '"'
    many = "\n".join(f'=== Record {i} ===\nDate: 2026-01-{(i % 28) + 1:02d}\nSource: S{i}\nExcerpt: "Note {i}."\n' for i in range(1, 42))
    for text in (big, many):
        r = c.post("/api/cases", json={"text": text})
        assert r.status_code == 413 and r.json()["error"]["code"] == "input_too_large" and r.json()["error"]["message"] == "Input is too large."
    r = c.post("/api/cases", content=b'{"text":"' + b"x" * (MAX_BODY_BYTES + 10) + b'"}', headers={"content-type": "application/json"})
    assert r.status_code == 413
    # chunked body with no content-length is cut off too
    r = c.post("/api/cases", content=iter([b'{"text":"' + b"x" * (MAX_BODY_BYTES // 2), b"x" * (MAX_BODY_BYTES // 2 + 10), b'"}']), headers={"content-type": "application/json"})
    assert r.status_code == 413
    assert DB.connect(str(tmp_path / "t183.sqlite")).execute("SELECT count(*) FROM cases").fetchone()[0] == 0


def test_pdf_upload_is_size_limited_and_refused_in_demo_mode(tmp_path, monkeypatch):
    from app.backend import pdf_text
    c = _client(tmp_path, monkeypatch)
    r = c.post("/api/cases/pdf", content=b"%PDF-1.4 x", headers={"content-type": "application/pdf"})
    assert r.status_code == 409 and r.json()["error"]["code"] == "demo_mode_unsupported_input"       # the public demo never parses an upload
    c = _client(tmp_path / "live" if (tmp_path / "live").mkdir() is None else tmp_path, monkeypatch, live=True, key=KEY)
    r = c.post("/api/cases/pdf", content=b"%PDF" + b"0" * (pdf_text.MAX_PDF_BYTES + 1), headers={"content-type": "application/pdf"})
    assert r.status_code == 413 and r.json()["error"]["code"] == "input_too_large"


# ---------------------------------------------------------------- 6. error states are plain
def test_every_error_is_plain_json_with_no_trace_path_or_framework_text(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch)
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    probes = [("get", "/api/cases/nope", None), ("get", "/api/nope", None), ("post", "/api/cases", b"{not json"), ("post", "/api/cases", b"[1]"),
              ("post", "/api/cases", json.dumps({"text": 5}).encode()), ("post", "/api/cases", json.dumps({"text": "   "}).encode()),
              ("post", f"/api/cases/{tok}/items/zzz/review", json.dumps({"action": "accept"}).encode()),
              ("post", f"/api/cases/{tok}/items/e1/review", json.dumps({"action": "explode"}).encode()),
              ("post", f"/api/cases/{tok}/items/e1/review", b"{}"), ("delete", "/api/health", None),
              ("post", f"/api/cases/{tok}/records/r1/confirm_date", json.dumps({"date": "not a date"}).encode()),
              ("post", "/api/cases", json.dumps({"text": "=== Record 1 ===\nDate: 2026-01-01\nSource: X\nExcerpt: \"New.\""}).encode())]
    bad = []
    for verb, path, body in probes:
        r = getattr(c, verb)(path, **({"content": body, "headers": {"content-type": "application/json"}} if body is not None else {}))
        t = r.text
        try:
            e = r.json()["error"]
        except Exception:
            bad.append((verb, path, r.status_code, "not the standard error JSON")); continue
        if r.status_code < 400 or r.status_code >= 500 and e["code"] != "internal":
            bad.append((verb, path, r.status_code, "unexpected status"))
        if re.search(r"Traceback|File \"|\.py\b|pydantic|starlette|fastapi|\"loc\"|Internal Server Error", t):
            bad.append((verb, path, r.status_code, "framework or trace text"))
        if not e.get("message") or re.fullmatch(r"[a-z_]+", e["message"]):
            bad.append((verb, path, r.status_code, "message is a bare code, not a sentence"))
    assert bad == [], bad


def test_a_run_that_fails_says_so_in_one_plain_sentence_and_keeps_finished_items(tmp_path, monkeypatch):
    class Boom:
        @staticmethod
        def run_pipeline(*a, **k): raise RuntimeError(f"SECRET {KEY} /Users/x/app.py line 3")
        @staticmethod
        def ingest_case(c, cid, text, now):
            from app.backend import pipeline as PL
            return PL.ingest_case(c, cid, text, now)
    monkeypatch.setenv("LLM_BACKEND", "fixture"); monkeypatch.delenv("ENABLE_LIVE", raising=False)
    c = TestClient(create_app(str(tmp_path / "f.sqlite"), static_dir=str(tmp_path), pipeline=Boom), client=("127.0.0.1", 50000))
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    s = _wait(c, tok)
    assert s["status"] == "failed"
    err = s.get("error") or {}
    assert err.get("message") == "The run stopped; finished items are kept." and "SECRET" not in json.dumps(s) and KEY not in json.dumps(s) and "/Users" not in json.dumps(s)
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202       # and it can be run again
