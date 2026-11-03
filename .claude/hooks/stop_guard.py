#!/usr/bin/env python3
"""Stop hook (§4.3): keep the orchestrator looping while actionable work exists, with a stall guard."""
from __future__ import annotations
import hashlib, json, sys, time
from _common import ROOT, read_input, board

STATE = ROOT / "board" / ".stop_guard_state"
STALL_LIMIT = 5


def main():
    data = read_input()
    if data.get("agent_id") or data.get("agent_type"):
        return 0  # only the main session
    if (ROOT / "board" / "STOP").exists():
        return 0
    r = board("status", "--json")
    try:
        s = json.loads(r.stdout)
    except Exception:
        return 0  # never trap the session on a broken board; the heartbeat will surface it
    if s.get("done_definition_met"):
        print(json.dumps({"systemMessage": "DONE — Definition of Done met (§11)."}))
        return 0
    triggers = (s.get("ready_unclaimed", 0) > 0 or s.get("in_review", 0) > 0 or s.get("changes_requested", 0) > 0
                or s.get("gate_failed") or s.get("inbox_unread", 0) > 0 or s.get("active_milestone_has_no_cards"))
    if not triggers:
        _reset()
        return 0  # workers busy, nothing actionable: let teammate messages / heartbeat wake us
    h = s.get("board_hash", "")
    st = _load()
    st["count"] = st.get("count", 0) + 1 if st.get("hash") == h else 1
    st["hash"], st["at"] = h, time.time()
    items = s.get("actionable", [])[:5]
    reason = "Actionable board items:\n" + "\n".join(f"- {x}" for x in items) + "\nContinue the orchestration loop (§7/§9)."
    st["last_reason"] = reason
    if st["count"] > STALL_LIMIT:
        (ROOT / "board" / "ALERT.md").write_text(
            "# ALERT: orchestrator stalled\n\nBoard unchanged across 5 consecutive Stop-hook blocks. Last reason:\n\n" + reason + "\n")
        _save({"count": 0, "hash": h})
        print(json.dumps({"systemMessage": "Stall guard tripped: board unchanged across 5 blocks; wrote board/ALERT.md"}))
        return 0
    _save(st)
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


def _load():
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {}


def _save(d):
    STATE.write_text(json.dumps(d))


def _reset():
    if STATE.exists():
        STATE.unlink()


if __name__ == "__main__":
    sys.exit(main())
