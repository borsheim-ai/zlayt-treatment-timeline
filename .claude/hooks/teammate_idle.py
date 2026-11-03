#!/usr/bin/env python3
"""TeammateIdle hook (§4.3): send an idle teammate back to the board if its role has claimable work."""
from __future__ import annotations
import json, re, sys
from _common import ROOT, read_input, board

ROLES = ["architect", "backend", "db", "frontend", "qa", "release", "writer", "researcher"]
DEBUG = ROOT / "board" / ".hook_debug.log"


def main():
    raw = read_input()
    if not DEBUG.exists():
        DEBUG.write_text("TeammateIdle input keys (values not logged): " + json.dumps(sorted(raw)) + "\n")
    cand = " ".join(str(raw.get(k, "")) for k in ("agent_type", "teammate_name", "agent_name", "name", "subagent_type"))
    role = next((r for r in ROLES if re.search(rf"\b{r}\b", cand)), None)
    if not role:
        return 0
    r = board("next", "--role", role, "--json")
    try:
        nxt = json.loads(r.stdout)
    except Exception:
        return 0
    if not nxt:
        return 0
    print(f"Claim and work card {nxt['id']}: {nxt['title']}. Use tools/board.py "
          f"(python3 tools/board.py claim {nxt['id']} --agent {role}).", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
