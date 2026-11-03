#!/usr/bin/env python3
"""PreToolUse(Edit|Write) hook for reviewer personas: writes allowed only under reviews/ and artifacts/review-evidence/."""
from __future__ import annotations
import sys
from pathlib import Path
from _common import ROOT, read_input, deny

ALLOWED = [Path(__import__('os').path.realpath(ROOT / "reviews")), Path(__import__('os').path.realpath(ROOT / "artifacts" / "review-evidence"))]


def main():
    import json as _json
    raw = sys.stdin.read()
    try:
        data = _json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict):
            raise ValueError
    except ValueError:
        deny("reviewer-write-guard: malformed hook input; denying to fail closed")
        return 0
    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("notebook_path") or ti.get("path")
    if not path:
        return 0
    p = Path(path)
    if not p.is_absolute():
        p = Path(data.get("cwd") or ROOT) / p
    p = p.resolve()
    if any(p == a or a in p.parents for a in ALLOWED):
        if p.exists() and (ROOT / "reviews") in p.parents and p.suffix == ".md":
            deny(f"reviewer-write-guard: {p.name} already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)")
        return 0
    # own agent memory only (memory: project)
    at = data.get("agent_type") or ""
    if at and (ROOT / ".claude" / "agent-memory" / at) in [p, *p.parents]:
        return 0
    deny(f"reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted {path}). Reviewers critique; they do not fix.")


if __name__ == "__main__":
    sys.exit(main())
