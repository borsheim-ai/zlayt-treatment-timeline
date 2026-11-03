"""Shared helpers for hook scripts. Hooks read JSON on stdin and must exit 0 silently when not applicable."""
from __future__ import annotations
import json, os, sys, subprocess
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
BOARD_PY = ROOT / "tools" / "board.py"


def read_input() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def board(*args, timeout=30):
    return subprocess.run([sys.executable, str(BOARD_PY), *args], capture_output=True, text=True,
                          timeout=timeout, cwd=str(ROOT))


def deny(reason: str):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)
