"""Provider interface and fixture backend. ADR-004, R-CO-2, R-ST-*; no key and no network (fixture backend only)."""
import json
import pytest
from app.llm import provider as P

MISS = getattr(P, "FixtureMissing", None) or P.FixtureMiss
SCHEMA = {"type": "object", "properties": {"summary": {"type": "string"}}, "required": ["summary"], "additionalProperties": False}

@pytest.fixture
def fx(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("LLM_FIXTURE_DIR", str(tmp_path))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return tmp_path

def put(dirp, model, system, user, output):
    h = P.prompt_hash(model, system, user, SCHEMA)
    (dirp / f"{h}.json").write_text(json.dumps(dict(output=output, recorded_from=dict(backend="claude-cli", model=model, recorded_at="2026-11-02"))))

def test_prompt_hash_is_stable_and_sensitive():
    """ADR-004: key = sha256 over model+system+user+schema - stable, and any change alters it."""
    a = P.prompt_hash("m", "s", "u", SCHEMA)
    assert a == P.prompt_hash("m", "s", "u", SCHEMA) and len(a) == 64
    assert len({a, P.prompt_hash("m2", "s", "u", SCHEMA), P.prompt_hash("m", "s2", "u", SCHEMA), P.prompt_hash("m", "s", "u2", SCHEMA), P.prompt_hash("m", "s", "u", {})}) == 5

def test_fixture_hit_returns_recorded_output(fx):
    """ADR-004: fixture replays tests/fixtures/llm/<sha256>.json."""
    put(fx, "m", "s", "u", {"summary": "ok"})
    assert P.complete("m", "s", "u", SCHEMA) == {"summary": "ok"}

def test_fixture_miss_raises_never_invents(fx):
    """ADR-004 / T-034 AC8: a miss raises FixtureMissing (an LLMError) carrying the prompt hash; no answer is invented."""
    with pytest.raises(MISS) as e:
        P.complete("m", "s", "nothing recorded", SCHEMA)
    assert isinstance(e.value, P.LLMError) and e.value.prompt_hash == P.prompt_hash("m", "s", "nothing recorded", SCHEMA)

def test_fixture_missing_name_is_exported():
    """T-034 AC8 / T-037 AC7: the exception is called FixtureMissing (one spelling across app, tests and docs)."""
    assert hasattr(P, "FixtureMissing") and issubclass(P.FixtureMissing, P.LLMError)

def test_fixture_miss_reports_hash_not_text(fx, caplog, capsys):
    """T-034 AC8 + arch invariant: the miss message carries the prompt hash (the audited row stores it) and never the prompt text; nothing is printed."""
    import logging
    caplog.set_level(logging.DEBUG)
    with pytest.raises(MISS) as e:
        P.complete("m", "s", "SECRET RECORD TEXT", SCHEMA)
    out = capsys.readouterr()
    assert P.prompt_hash("m", "s", "SECRET RECORD TEXT", SCHEMA) in str(e.value)
    assert "SECRET RECORD TEXT" not in str(e.value) + caplog.text + out.out + out.err

def test_meta_surfaces_recorded_from(fx):
    """ADR-004 / ADR-003: LLMResult carries backend='fixture' and recorded_from for the audit trail."""
    put(fx, "m", "s", "u", {"summary": "ok"})
    r = P.complete_with_meta("m", "s", "u", SCHEMA)
    assert r.backend == "fixture" and r.recorded_from["backend"] == "claude-cli" and r.output == {"summary": "ok"}

def test_schema_invalid_recording_is_llmerror(fx):
    """ADR-004: output is re-validated against the schema; invalid -> LLMError (not FixtureMiss)."""
    put(fx, "m", "s", "u", {"summary": 5, "extra": 1})
    with pytest.raises(P.LLMError) as e:
        P.complete("m", "s", "u", SCHEMA)
    assert not isinstance(e.value, MISS)

def test_no_key_needed(fx):
    """R-ST / A-001: fixture backend works with no ANTHROPIC_API_KEY."""
    put(fx, "m", "s", "u", {"summary": "ok"})
    assert P.complete("m", "s", "u", SCHEMA)

def test_recorder_refuses_foreign_text():
    """ADR-004: recording refuses any text not in evals/golden (no accidental commit of other text); golden text is accepted."""
    from tests.unit import _golden as G
    P.assert_recordable(G.record("sample", 1)["excerpt"])
    with pytest.raises(ValueError):
        P.assert_recordable("Jane Doe, SSN 123-45-6789, real patient text")


# ---- backends: retries, timeouts, argv, single call path, no text in logs (T-034 AC4, AC5, AC7) ----
import pathlib, subprocess, sys, types

def test_sdk_no_internal_retry(monkeypatch):
    """T-034 AC7 / checklist 8: the anthropic-api client is constructed with max_retries=0 and an explicit timeout <= 120 s (audited.py owns retries)."""
    seen = {}
    class FakeAnthropic:
        def __init__(self, **kw): seen.update(kw)
    monkeypatch.setitem(sys.modules, "anthropic", types.SimpleNamespace(Anthropic=FakeAnthropic))
    from app.llm.backends import anthropic_api as A
    A.make_client()
    assert seen["max_retries"] == 0 and 0 < float(seen["timeout"]) <= 120

def test_cli_argv_pins_model_and_disables_tools_hooks_mcp():
    """T-034 AC4: pinned --model, no tools, MCP strict, hooks disabled, prompt last after `--`; concurrency <= 3."""
    from app.llm.backends import claude_cli as C
    argv = C.build_argv("claude-test-model", "sys", "USER PROMPT", SCHEMA)
    assert argv[argv.index("--model") + 1] == "claude-test-model"
    assert argv[argv.index("--tools") + 1] == ""
    assert "--strict-mcp-config" in argv and "disableAllHooks" in argv[argv.index("--settings") + 1]
    assert "--dangerously-skip-permissions" not in argv and argv[-2:] == ["--", "USER PROMPT"]
    assert C.MAX_CONCURRENCY <= 3

def test_cli_runs_outside_project_with_timeout_and_no_api_key(monkeypatch):
    """T-034 AC4: cwd outside the project, timeout <= 120 s, ANTHROPIC_API_KEY stripped from the child env (uses the claude.ai login)."""
    from app.llm.backends import claude_cli as C
    root = pathlib.Path(__file__).resolve().parents[2]
    seen = {}
    def fake_run(argv, **kw):
        seen.update(kw)
        return subprocess.CompletedProcess(argv, 0, stdout='{"result": "{\\"summary\\": \\"ok\\"}", "is_error": false}', stderr="")
    monkeypatch.setattr(C.subprocess, "run", fake_run)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "not-a-real-key")
    r = C.call("m", "s", "u", SCHEMA, key="k")
    assert r.output == {"summary": "ok"} and r.backend == "claude-cli"
    assert root not in pathlib.Path(seen["cwd"]).resolve().parents and pathlib.Path(seen["cwd"]).resolve() != root
    assert 0 < seen["timeout"] <= 120 and "ANTHROPIC_API_KEY" not in seen["env"]

def test_single_call_path():
    """T-034 AC5 / arch invariant: no anthropic SDK or subprocess import outside app/llm/backends."""
    import re
    from tests.unit.spawn_audit import audit
    app = pathlib.Path(__file__).resolve().parents[2] / "app"
    # Two local-process modules may import subprocess: app/backend/pdf_ocr.py (Tesseract, T-086) and app/backend/pdf_hidden.py (its own scan
    # child plus a `ps` RSS probe, T-087). They are not allowed to call the LLM, and they are not checked with a regex: the AST audit in
    # tests/unit/spawn_audit.py rejects any claude/anthropic/app.llm name, any spawn outside its argv allow-list, and any alias or lookup trick.
    allow_subprocess = {"backend/pdf_ocr.py": "pdf_ocr", "backend/pdf_hidden.py": "pdf_hidden"}
    bad = []
    for p in app.rglob("*.py"):
        rel = str(p.relative_to(app))
        if "llm/backends" in p.as_posix():
            continue
        src = p.read_text()
        if rel in allow_subprocess:
            bad += [f"{rel}: {v}" for v in audit(src, allow_subprocess[rel])]
        elif re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", src, re.M):
            bad.append(rel)
    assert bad == []

def test_no_text_in_logs(monkeypatch, caplog, capsys):
    """T-034 AC5 / arch invariant: backend failures never put the prompt, reply or SDK message in errors or logs."""
    import logging
    caplog.set_level(logging.DEBUG)
    from app.llm.backends import claude_cli as C, anthropic_api as A
    monkeypatch.setattr(C.subprocess, "run", lambda argv, **kw: subprocess.CompletedProcess(argv, 1, stdout="SECRET REPLY", stderr="SECRET RECORD TEXT"))
    with pytest.raises(P.LLMError) as e1:
        C.call("m", "s", "SECRET RECORD TEXT", SCHEMA, key="k")
    class Boom:
        class messages:
            @staticmethod
            def create(**kw): raise RuntimeError("SECRET RECORD TEXT echoed by SDK")
    with pytest.raises(P.LLMError) as e2:
        A.call("m", "s", "SECRET RECORD TEXT", SCHEMA, key="k", client=Boom())
    out = capsys.readouterr()
    assert "SECRET" not in str(e1.value) + str(e2.value) + caplog.text + out.out + out.err
