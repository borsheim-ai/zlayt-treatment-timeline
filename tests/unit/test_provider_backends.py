"""T-034 AC3-5,7,8: claude-cli argv/limits, anthropic-api client config, recorder, single call path. No key, no network (fakes)."""
import json, pathlib, re, subprocess, threading, time, types
import pytest
from app.llm import provider as P, audited as AU, record as R
from app.llm._types import lenient_json
from app.llm.backends import claude_cli as CLI, anthropic_api as API
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.spawn_audit import audit

SCHEMA = {"type": "object", "properties": {"summary": {"type": "string"}}, "required": ["summary"]}
ROOT = pathlib.Path(__file__).resolve().parents[2]

def _proc(out):
    return subprocess.CompletedProcess([], 0, stdout=json.dumps({"result": json.dumps(out), "total_cost_usd": 0.01,
        "modelUsage": {"claude-haiku-5-5": {"inputTokens": 5, "outputTokens": 3}}}), stderr="")

def test_claude_cli_argv_and_cwd_and_timeout(monkeypatch):
    """ADR-004: pinned model, no tools/MCP/hooks/session, json envelope, cwd outside the project, 120 s timeout, no API key in env."""
    seen = {}
    def fake_run(argv, **kw):
        seen.update(argv=argv, **kw); return _proc({"summary": "ok"})
    monkeypatch.setattr(CLI.subprocess, "run", fake_run)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x" * 10); monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "t"); monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://x")
    monkeypatch.setenv("LLM_BACKEND", "claude-cli"); monkeypatch.setenv("ENABLE_LIVE", "1")
    r = P.complete_with_meta("claude-haiku-5-5", "sys", "usr", SCHEMA)
    a = seen["argv"]
    assert r.output == {"summary": "ok"} and r.backend == "claude-cli" and r.model_resolved == "claude-haiku-5-5" and r.cost_usd == 0.01
    assert a[1] == "-p" and a[a.index("--model") + 1] == "claude-haiku-5-5"
    assert a[a.index("--settings") + 1] == '{"disableAllHooks":true}'
    assert a[a.index("--tools") + 1] == "" and "--strict-mcp-config" in a and "--no-session-persistence" in a
    assert a[a.index("--output-format") + 1] == "json" and a[-2:] == ["--", "usr"]
    assert seen["timeout"] == 120
    assert not pathlib.Path(seen["cwd"]).resolve().is_relative_to(ROOT)
    assert not [k for k in seen["env"] if k.startswith("ANTHROPIC")] and set(seen["env"]) <= set(CLI.ENV_ALLOW)

def test_claude_cli_concurrency_at_most_three(monkeypatch):
    state = dict(now=0, peak=0); lock = threading.Lock()
    def fake_run(argv, **kw):
        with lock:
            state["now"] += 1; state["peak"] = max(state["peak"], state["now"])
        time.sleep(0.05)
        with lock:
            state["now"] -= 1
        return _proc({"summary": "ok"})
    monkeypatch.setattr(CLI.subprocess, "run", fake_run)
    ts = [threading.Thread(target=CLI.call, args=("m", "s", "u", SCHEMA)) for _ in range(9)]
    [t.start() for t in ts]; [t.join() for t in ts]
    assert 1 < state["peak"] <= 3

@pytest.mark.parametrize("exc,code", [(subprocess.TimeoutExpired("claude", 120), "TIMEOUT"), (OSError("nope"), "BACKEND_UNAVAILABLE")])
def test_claude_cli_failures_are_llmerror(monkeypatch, exc, code):
    def fake_run(argv, **kw): raise exc
    monkeypatch.setattr(CLI.subprocess, "run", fake_run)
    with pytest.raises(P.LLMError, match=code):
        CLI.call("m", "s", "u", SCHEMA)

def test_claude_cli_reply_must_be_one_json_object(monkeypatch):
    monkeypatch.setattr(CLI.subprocess, "run", lambda a, **k: subprocess.CompletedProcess([], 0, stdout=json.dumps({"result": "Sure! here you go"}), stderr=""))
    with pytest.raises(P.LLMError):
        CLI.call("m", "s", "u", SCHEMA)
    fenced = "```json\n{\"summary\": \"x\"}\n```"
    monkeypatch.setattr(CLI.subprocess, "run", lambda a, **k: subprocess.CompletedProcess([], 0, stdout=json.dumps({"result": fenced}), stderr=""))
    assert CLI.call("m", "s", "u", SCHEMA).output == {"summary": "x"}

class _FakeClient:
    def __init__(self, **kw): self.kw = kw; self.messages = self; self.calls = []
    def create(self, **kw):
        self.calls.append(kw)
        return types.SimpleNamespace(content=[types.SimpleNamespace(type="tool_use", input={"summary": "ok"})], model="m-resolved",
                                     usage=types.SimpleNamespace(input_tokens=7, output_tokens=2))

def test_sdk_no_internal_retry(monkeypatch):
    """T-034 AC7: the constructed client has max_retries=0 and an explicit timeout <= 120 s."""
    import anthropic
    made = {}
    monkeypatch.setattr(anthropic, "Anthropic", lambda **kw: made.setdefault("c", _FakeClient(**kw)))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    API.make_client()
    assert made["c"].kw["max_retries"] == 0 and 0 < made["c"].kw["timeout"] <= 120

def test_anthropic_api_mocked_sdk():
    c = _FakeClient()
    r = API.call("m", "s", "u", SCHEMA, client=c)
    assert r.output == {"summary": "ok"} and r.backend == "anthropic-api" and r.tokens_in == 7
    assert c.calls[0]["temperature"] == 0 and c.calls[0]["tool_choice"] == {"type": "tool", "name": "emit"}

def test_anthropic_api_error_keeps_no_text(monkeypatch):
    class Boom(_FakeClient):
        def create(self, **kw): raise RuntimeError("SECRET RECORD TEXT")
    with pytest.raises(P.LLMError) as e:
        API.call("m", "s", "u", SCHEMA, client=Boom())
    assert "SECRET" not in str(e.value)

def test_schema_invalid_live_output_is_llmerror(monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setattr(CLI.subprocess, "run", lambda a, **k: _proc({"summary": 3}))
    with pytest.raises(P.LLMError):
        P.complete("m", "s", "u", SCHEMA)

def test_recorder_refuses_foreign_text(tmp_path, monkeypatch):
    """T-034 AC3: a file outside evals/golden (or text not in golden) is refused."""
    f = tmp_path / "x.txt"; f.write_text("Jane Doe, SSN 123-45-6789")
    monkeypatch.setenv("LLM_BACKEND", "claude-cli"); monkeypatch.setenv("RECORD_FIXTURES", "1")
    with pytest.raises(ValueError):
        R.record_file(str(f))
    for bad in ("Jane Doe, SSN 123-45-6789", "a", "2019", G.record("sample", 1)["excerpt"]):   # foreign, tiny fragments, a mere excerpt
        with pytest.raises(ValueError):
            with P.record_context(bad):
                pass
    with P.record_context(G.raw("sample")):           # a complete golden input is accepted
        pass
    with pytest.raises(ValueError):
        P.assert_recordable("a"); 
    with pytest.raises(P.LLMError):
        P.validate_schema({"s": "xxxxxx"}, {"type": "object", "properties": {"s": {"type": "string", "maxLength": 3}}})
    with pytest.raises(P.LLMError):
        P.validate_schema({"s": 1}, {"type": "object", "patternProperties": {}})   # unknown keyword fails closed
    P.validate_schema({"s": None}, {"type": "object", "properties": {"s": {"anyOf": [{"type": "string"}, {"type": "null"}]}}})
    assert R.main([str(f)]) == 1

def test_record_mode_writes_fixture_and_fixture_replays_it(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "claude-cli"); monkeypatch.setenv("RECORD_FIXTURES", "1"); monkeypatch.setenv("LLM_FIXTURE_DIR", str(tmp_path / "fx")); monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.setattr(CLI.subprocess, "run", lambda a, **k: _proc({"summary": "ok"}))
    with pytest.raises(ValueError):                       # live call outside record_context is refused in record mode
        P.complete("claude-haiku-5-5", "s", "u", SCHEMA)
    def run(conn, cid, raw, call):
        return call("extract", "s", "u", SCHEMA)
    n = R.record_file(str(ROOT / "evals" / "golden" / "sample.txt"), run=run)
    assert n == 1
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    r = P.complete_with_meta("claude-sonnet-5-5", "s", "u", SCHEMA)   # recorded under the generator model
    assert r.output == {"summary": "ok"} and r.recorded_from["backend"] == "claude-cli"

def test_fixture_miss_through_audited_is_failed_after_retries(tmp_path, monkeypatch):
    """T-034 AC8: miss -> LLM_FAILED_AFTER_RETRIES (still a FixtureMiss), one attempt, no default answer."""
    monkeypatch.setenv("LLM_BACKEND", "fixture"); monkeypatch.setenv("LLM_FIXTURE_DIR", str(tmp_path))
    conn = DB.connect(str(tmp_path / "a.sqlite")); cid = DB.create_case(conn, "SYNTHETIC", now=1.0)
    with pytest.raises(AU.LLMFailed) as e:
        AU.audited_call(conn, cid, "extract", "m", "s", "u", SCHEMA)
    assert e.value.code == "LLM_FAILED_AFTER_RETRIES" and isinstance(e.value, P.FixtureMiss)
    rows = DB.list_llm_calls(conn, cid)
    assert len(rows) == 1 and rows[0]["backend"] == "fixture" and rows[0]["attempt"] == 1 and rows[0]["prompt_sha256"] == P.prompt_hash("m", "s", "u", SCHEMA)

def test_audit_row_records_backend_and_recorded_from(tmp_path, monkeypatch):
    """T-034 AC1: backend (and the recording backend for replays) is stored on each row."""
    monkeypatch.setenv("LLM_BACKEND", "fixture"); monkeypatch.setenv("LLM_FIXTURE_DIR", str(tmp_path))
    (tmp_path / f"{P.prompt_hash('m', 's', 'u', SCHEMA)}.json").write_text(json.dumps(dict(output={"summary": "ok"}, recorded_from=dict(backend="claude-cli", model="m", recorded_at="t"))))
    conn = DB.connect(str(tmp_path / "a.sqlite")); cid = DB.create_case(conn, "SYNTHETIC", now=1.0)
    out, call_id = AU.audited_call(conn, cid, "judge_x", "m", "s", "u", SCHEMA)
    row = DB.get_llm_call(conn, call_id)
    assert out == {"summary": "ok"} and row["backend"] == "fixture" and row["role"] == "judge" and row["parsed_ok"] == 1
    assert json.loads(row["recorded_from_json"] if "recorded_from_json" in row else json.dumps(row["recorded_from"]))["backend"] == "claude-cli"

def test_single_call_path():
    """T-034 AC5: no SDK or subprocess use outside app/llm/backends."""
    for p in (ROOT / "app").rglob("*.py"):
        if "backends" in p.parts and "llm" in p.parts:
            continue
        src = p.read_text()
        if p.name in ("pdf_ocr.py", "pdf_hidden.py") and "backend" in p.parts:      # local Tesseract binary (T-086) / local scan child process (T-087), not LLM calls
            assert audit(src, p.stem) == [], p                                       # AST audit: no claude/anthropic/app.llm, argv allow-list only
            continue
        assert not re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", src, re.M), p

def test_no_text_in_logs(tmp_path, monkeypatch, caplog, capsys):
    """T-034 AC5: a failing live call logs neither prompt nor error text."""
    caplog.set_level("DEBUG")
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    def fake_run(a, **k): raise subprocess.TimeoutExpired("claude", 120)
    monkeypatch.setattr(CLI.subprocess, "run", fake_run)
    conn = DB.connect(str(tmp_path / "a.sqlite")); cid = DB.create_case(conn, "SYNTHETIC", now=1.0)
    with pytest.raises(AU.LLMFailed):
        AU.audited_call(conn, cid, "extract", "m", "s", "RECORD TEXT XYZZY", SCHEMA)
    o = capsys.readouterr()
    assert "XYZZY" not in caplog.text + o.out + o.err


def test_audit_error_column_holds_only_codes(tmp_path, monkeypatch):
    """T-034 review nit: model-controlled text (extra keys) never lands in llm_calls.error."""
    conn = DB.connect(str(tmp_path / "a.sqlite")); cid = DB.create_case(conn, "SYNTHETIC", now=1.0)
    evil = "<img src=x onerror=alert(1)>"
    def f(model, system, user, schema): return P.LLMResult(output={evil: 1})
    with pytest.raises(AU.LLMFailed):
        AU.audited_call(conn, cid, "extract", "m", "s", "u", {"type": "object", "properties": {}, "additionalProperties": False}, complete_with_meta=f, validate=lambda o: P.validate_schema(o, {"type": "object", "properties": {}, "additionalProperties": False}))
    errs = [r["error"] for r in DB.list_llm_calls(conn, cid)]
    assert errs == ["SCHEMA_INVALID"] * 3 and not any("<img" in e for e in errs)

def test_audited_sleep_seam_is_capped_and_injectable(tmp_path):
    conn = DB.connect(str(tmp_path / "a.sqlite")); cid = DB.create_case(conn, "SYNTHETIC", now=1.0)
    naps = []
    def f(model, system, user, schema): raise P.LLMError("TIMEOUT x")
    with pytest.raises(AU.LLMFailed):
        AU.audited_call(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f, sleep=naps.append)
    assert naps == list(AU.RETRY_DELAYS_S) and max(naps) <= 2


@pytest.mark.parametrize("backend", ["claude-cli", "anthropic-api"])
def test_demo_never_reaches_a_live_backend(tmp_path, monkeypatch, backend):
    """T-053 security r1 blocker: without ENABLE_LIVE=1 every call resolves to the fixture backend whatever LLM_BACKEND or a key say;
    no subprocess and no SDK client is created."""
    import anthropic
    monkeypatch.setenv("LLM_BACKEND", backend); monkeypatch.setenv("ANTHROPIC_API_KEY", "k"); monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.setenv("LLM_FIXTURE_DIR", str(tmp_path))
    def boom(*a, **k): raise AssertionError("live call from demo mode")
    monkeypatch.setattr(CLI.subprocess, "run", boom); monkeypatch.setattr(anthropic, "Anthropic", boom)
    assert P.backend_name() == "fixture"
    with pytest.raises(P.FixtureMissing):
        P.complete("m", "s", "u", SCHEMA)
    monkeypatch.setenv("ENABLE_LIVE", "1")
    assert P.backend_name() == backend


def test_claude_cli_reply_that_ends_with_its_corrected_object_is_that_object(monkeypatch):
    """T-168: lib01 record 3 -- the model drafts an object, says 'Wait', and closes with the corrected one. The closing object is the answer."""
    reply = ('{"summary": "a", "excerpt": "b"}\n\nWait, those two sentences are not adjacent. Corrected output:\n\n'
             '{"summary": "c {x}", "excerpt": "d", "n": {"k": 1}}')
    monkeypatch.setattr(CLI.subprocess, "run", lambda a, **k: subprocess.CompletedProcess([], 0, stdout=json.dumps({"result": reply}), stderr=""))
    with pytest.raises(P.LLMError, match="INVALID_JSON"):        # T-168 r2: strict unless the extract call opts in (boundary tests: test_t168_strict_judge_parse.py)
        CLI.call("m", "s", "u", SCHEMA)
    with lenient_json():
        assert CLI.call("m", "s", "u", SCHEMA).output == {"summary": "c {x}", "excerpt": "d", "n": {"k": 1}}


@pytest.mark.parametrize("reply", ['{"summary": "a"} and then some words', 'Sure {not json} here', '{"summary": "a"}\n\nWait, no.', '[{"summary": "a"}]', 'x {"summary": "a"} {'])
def test_claude_cli_reply_with_text_after_the_object_or_no_closing_object_is_still_invalid(monkeypatch, reply):
    monkeypatch.setattr(CLI.subprocess, "run", lambda a, **k: subprocess.CompletedProcess([], 0, stdout=json.dumps({"result": reply}), stderr=""))
    with pytest.raises(P.LLMError, match="INVALID_JSON"):
        CLI.call("m", "s", "u", SCHEMA)
