"""Runtime configuration, read-only. One place that says which mode the process is in and why; never returns or prints a secret.

`python -m app.config` prints the resolved settings (a key is reported only as set / not set). The Dockerfile, run.sh and the Makefile
use it as a startup self-check. The rules themselves live where they are enforced (app.llm.provider.backend_name, app.backend.store.live_enabled);
this module calls those so there is one definition of "live".
"""
import importlib.util
import json
import os
import socket

DEFAULTS = {"HOST": "127.0.0.1", "PORT": "7860", "LLM_BACKEND": "fixture", "FIXTURE_SET": "curated"}


def resolved() -> dict:
    from app.backend import store
    from app.llm import provider
    live = store.live_enabled()
    key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))
    backend = provider.backend_name()
    warnings = []
    if os.environ.get("ENABLE_LIVE") == "1" and not live:
        warnings.append("ENABLE_LIVE=1 but there is nothing to call (no ANTHROPIC_API_KEY, backend is not claude-cli): serving demo mode.")
    if os.environ.get("LLM_BACKEND") not in (None, "", "fixture") and os.environ.get("ENABLE_LIVE") != "1":
        warnings.append("LLM_BACKEND is set but ENABLE_LIVE is not 1: the fixture backend is used (no model call is possible).")
    if live and backend == "anthropic-api" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        warnings.append("Live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a spend limit at the provider first); the server will refuse to start.")
    return {
        "mode": "live" if live else "demo",
        "backend": backend,
        "fixture_set": os.environ.get("FIXTURE_SET", DEFAULTS["FIXTURE_SET"]) if backend == "fixture" else None,
        "host": os.environ.get("HOST", DEFAULTS["HOST"]),
        "port": int(os.environ.get("PORT", DEFAULTS["PORT"])),
        "anthropic_api_key": "set" if key_set else "not set",
        "local_mode": os.environ.get("ZLAYT_MODE") == "local",
        "warnings": warnings,
    }


def preflight() -> str | None:
    """One-line reason the server cannot start in the configured mode, or None. Called by app.main before create_app so a misconfigured
    live opt-in prints one line naming the variable instead of a traceback. The cap/host rules themselves stay in create_app (it still raises)."""
    from app.llm import provider
    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        return "live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)"
    if provider.backend_name() == "claude-cli" and importlib.util.find_spec("app.llm.backends.claude_cli") is None:
        return ("LLM_BACKEND=claude-cli is not available in this build (the Docker image does not ship the CLI backend, CONTRACT section 10): "
                "use LLM_BACKEND=anthropic-api, or unset ENABLE_LIVE for demo mode.")
    return None


def port_in_use(host: str, port: int) -> bool:
    """True when something is already listening on host:port (same SO_REUSEADDR setting uvicorn binds with)."""
    with socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
        except OSError:
            return True
    return False


if __name__ == "__main__":
    import sys
    why = preflight()
    if why:                                           # same refusal app.main makes: print only the error line, not a config dump with a contradicting warning
        print(f"error: {why}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(resolved(), indent=2))
