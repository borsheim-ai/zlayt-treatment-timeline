#!/usr/bin/env python3
"""PostToolUse(Edit|Write) hook (§4.3): validate board cards and review files on every write."""
from __future__ import annotations
import os
import sys
from pathlib import Path
from _common import ROOT, read_input, board


def main():
    data = read_input()
    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("path") or ""
    if not path:
        return 0
    p = Path(path)
    if not p.is_absolute():
        p = Path(data.get("cwd") or ROOT) / p
    try:
        rel = Path(os.path.realpath(p)).relative_to(Path(os.path.realpath(ROOT)))
    except ValueError:
        return 0
    if not rel.parts or rel.parts[0] not in ("board", "reviews") or p.suffix != ".md":
        return 0
    r = board("validate", str(p))
    if r.returncode != 0:
        print((r.stderr or r.stdout).strip() + "\nFix the file (cards change state only via tools/board.py).", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
