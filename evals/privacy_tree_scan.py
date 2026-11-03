#!/usr/bin/env python3
"""Report which files carry a private term, on the normalized view (D-070). Never prints a value; prints path, class, count.

  python3 evals/privacy_tree_scan.py --dir submission/prompt-log      # a directory on disk (every class, the outside name too)
  python3 evals/privacy_tree_scan.py --head [--exclude submission/prompt-log/]   # every tracked text file at HEAD

Terms come from the git-ignored deploy/.private_patterns via evals/finalize_prompt_log.py (no value is written here). The view removes
backslashes, quotes, backticks, '+' and whitespace and folds case, and each term of 7+ letters/digits may have up to 12 punctuation characters
between its characters, so split, escaped, spaced, tuple and regex-quantifier spellings are found; derived terms (phone name without its
number, job-folder pieces) are included. Exit 1 on any hit.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "evals"))
sys.path.insert(0, str(ROOT / "tools"))
import finalize_prompt_log as fpl  # noqa: E402


def rules() -> list:
    fpl.require_terms()
    t = fpl.TERMS
    return [("work email / tailnet host", fpl.term_rx(t["email"] + t["term"])), ("device name", fpl.term_rx(t["device"])),
            ("third-party name", fpl.term_rx(t["third"])), ("personal job-application name", fpl.term_rx(t["personal"])),
            ("outside project name", fpl.term_rx(t["outside"]))]


def hits(text: str, name: str, rs: list) -> dict:
    view = fpl._VIEW_ALL.sub("", text)
    out = {}
    if fpl.OUTSIDE_WORD_RX is not None:   # short outside values (the ticker) are whole-word matches on the raw text and the path
        n = len(fpl.OUTSIDE_WORD_RX.findall(text))
        if n:
            out["outside project name (short value, whole word)"] = n
        if fpl.OUTSIDE_WORD_RX.search(name):
            out["outside project name (short value, whole word) (in the path itself)"] = 1
    for label, rx in rs:
        n = len(rx.findall(view))
        if n:
            out[label] = n
    pv = fpl._VIEW_ALL.sub("", name)
    for label, rx in rs:
        if rx.search(pv):
            out[label + " (in the path itself)"] = 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir")
    ap.add_argument("--head", action="store_true")
    ap.add_argument("--exclude", default="submission/prompt-log/")
    a = ap.parse_args()
    rs = rules()
    found = {}
    nfiles = 0
    if a.dir:
        for p in sorted(Path(a.dir).rglob("*")):
            if p.is_file():
                data = p.read_bytes()
                if b"\0" in data[:8192]:
                    continue
                nfiles += 1
                text = data.decode("utf-8", "replace")
                h = hits(text, str(p), rs)
                n = len(fpl.chris_spans(text))   # a run of 8+ words copied verbatim from one of Chris's messages (MASTER_PROMPT.md's own wording is exempt)
                if n:
                    h["Chris's own words (8+ word run)"] = n
                if p.name in ("activity.jsonl", "board-activity.jsonl"):
                    n = sum(1 for ln in text.splitlines() if fpl.omit_inbox_text(ln)[1])
                    if n:
                        h["Chris's board-inbox note text"] = n
                if p.name.endswith("-orchestrator.md") and p.parent.name == "transcripts":
                    h["transcript of a session with Chris's own turns"] = 1
                if h:
                    found[str(p)] = h
    else:
        names = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "-z", "--name-only", "HEAD"], capture_output=True, check=True).stdout.split(b"\0")
        for raw in names:
            name = raw.decode("utf-8", "replace")
            if not name or name.startswith(a.exclude):
                continue
            data = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{name}"], capture_output=True).stdout
            if b"\0" in data[:8192]:
                h = hits("", name, rs)
            else:
                nfiles += 1
                h = hits(data.decode("utf-8", "replace"), name, rs)
            if h:
                found[name] = h
    if a.dir and (Path(a.dir) / "board" / "inbox").exists():
        found["board/inbox"] = {"Chris's board-inbox notes directory present": 1}
    for k, v in found.items():
        print(f"HIT {k}: " + ", ".join(f"{c} x{n}" for c, n in v.items()))
    print(f"privacy_tree_scan: {nfiles} text file(s) checked, {len(found)} with hits")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
