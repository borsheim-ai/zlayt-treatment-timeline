"""claude-cli backend (development only, never in the Docker image). ADR-004; flags verified in memory/ENVIRONMENT.md.

Runs `claude -p` from a throwaway cwd outside the project with hooks, tools and MCP disabled. One attempt, no retry.
Never logs prompts or replies.
"""
import json
import os
import shutil
import subprocess
import tempfile
import threading
import time

from app.llm._types import LLMError, LLMResult, parse_json_reply

TIMEOUT_S = 120
MAX_CONCURRENCY = 3
_SEM = threading.BoundedSemaphore(MAX_CONCURRENCY)


ENV_ALLOW = ("PATH", "HOME", "USER", "LOGNAME", "LANG", "LC_ALL", "TMPDIR", "CLAUDE_BIN", "CLAUDE_CONFIG_DIR", "XDG_CONFIG_HOME",
             "XDG_DATA_HOME", "XDG_CACHE_HOME")


def child_env() -> dict:
    """Minimal environment for the CLI child (claude.ai login via HOME): no ANTHROPIC_* variable or other secret is inherited."""
    return {k: os.environ[k] for k in ENV_ALLOW if k in os.environ}


def _system_with_schema(system: str, json_schema: dict) -> str:
    return (f"{system}\n\nReply with exactly one JSON object and nothing else (no prose, no code fence) "
            f"that satisfies this JSON Schema:\n{json.dumps(json_schema, sort_keys=True)}")


def build_argv(model: str, system: str, user: str, json_schema: dict) -> list:
    # --tools is variadic, so it is followed by another flag; the user prompt comes last after `--` (qa-pinned contract).
    return [os.environ.get("CLAUDE_BIN") or shutil.which("claude") or "claude", "-p", "--model", model,
            "--settings", '{"disableAllHooks":true}', "--tools", "", "--strict-mcp-config",
            "--no-session-persistence", "--output-format", "json",
            "--system-prompt", _system_with_schema(system, json_schema), "--", user]


def call(model: str, system: str, user: str, json_schema: dict, *, key: str = "") -> LLMResult:
    argv = build_argv(model, system, user, json_schema)
    env = child_env()
    cwd = tempfile.mkdtemp(prefix="zlayt-cli-")
    t0 = time.monotonic()
    try:
        with _SEM:
            try:
                p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=TIMEOUT_S, stdin=subprocess.DEVNULL)
            except subprocess.TimeoutExpired:
                raise LLMError("TIMEOUT claude-cli") from None
            except OSError:
                raise LLMError("BACKEND_UNAVAILABLE claude-cli not runnable") from None
    finally:
        shutil.rmtree(cwd, ignore_errors=True)
    if p.returncode != 0:
        raise LLMError(f"BACKEND_FAILED claude-cli exit {p.returncode}")
    try:
        env_json = json.loads(p.stdout)
    except ValueError:
        raise LLMError("BACKEND_FAILED claude-cli envelope not JSON") from None
    if not isinstance(env_json, dict) or env_json.get("is_error"):
        raise LLMError("BACKEND_FAILED claude-cli reported an error")
    text = env_json.get("result") or ""
    out = parse_json_reply(text)      # strict unless audited_call opened `lenient_json()` (extract steps only)
    mu = env_json.get("modelUsage") or {}
    resolved = next(iter(mu), model)
    u = mu.get(resolved, {}) if mu else {}
    return LLMResult(output=out, backend="claude-cli", model_resolved=resolved,
                     latency_ms=int((time.monotonic() - t0) * 1000), cost_usd=float(env_json.get("total_cost_usd") or 0.0),
                     tokens_in=int(u.get("inputTokens", 0) or 0), tokens_out=int(u.get("outputTokens", 0) or 0), raw=text)
