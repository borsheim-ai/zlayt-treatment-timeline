#!/usr/bin/env python3
"""Fallback for hosts that did not load .claude/agents at session start: print an agent definition as an inline prompt.
Usage: python3 tools/agent_prompt.py <agent-name> [--brief-file path]  → stdout = definition body (+ brief)."""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
name = sys.argv[1] if len(sys.argv) > 1 else ""
if not re.fullmatch(r"[a-z][a-z0-9-]{1,40}", name) or not (ROOT / ".claude" / "agents" / f"{name}.md").is_file():
    print(f"agent_prompt.py: unknown agent {name!r}; see .claude/agents/", file=sys.stderr)
    sys.exit(2)
txt = (ROOT / ".claude" / "agents" / f"{name}.md").read_text()
m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
head, body = (m.group(1), m.group(2)) if m else ("", txt)
model = re.search(r"^model:\s*(\S+)", head, re.M)
out = [f"[Agent definition: .claude/agents/{name}.md — model: {model.group(1) if model else '?'} — loaded inline (fallback)]", body.strip()]
if "-reviewer" in name:
    out.append("\nFallback note: the write-guard hook from your frontmatter is not attached in this mode. You are still forbidden to "
               "create or modify any file outside reviews/ and artifacts/review-evidence/ — by any means, including Bash redirection.")
if "--brief-file" in sys.argv:
    i = sys.argv.index("--brief-file") + 1
    if i >= len(sys.argv) or not Path(sys.argv[i]).is_file():
        print("agent_prompt.py: --brief-file needs an existing file", file=sys.stderr)
        sys.exit(2)
    out.append("\n# Your brief\n" + Path(sys.argv[i]).read_text())
print("\n".join(out))
