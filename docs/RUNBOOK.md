# RUNBOOK (for Chris)

## URLs
| What | URL | Notes |
|---|---|---|
| Board (tailnet) | https://<redacted-private>:7777 | open on your phone (Tailscale on). Kanban, personas, milestones, activity, inbox, STOP. |
| Board (local) | http://localhost:7777 | also in the Desktop Browser pane (`.claude/launch.json` → "board") |
| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |

Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
We restored those and gave the board and app their own ports so nothing of yours was clobbered.

## Steer
- **Inbox:** Board → Inbox → type a note → Send. It lands in `board/inbox/` and the orchestrator acts on it next cycle.
- **Direct:** type into this Claude session (Remote Control / Desktop). Treated exactly like an inbox note.
- **Your items:** `submission/NEEDS_CHRIS.md` and the `needs_chris` column. Nothing there blocks the team.

## Stop
- Board → Inbox → **STOP** (type STOP to confirm) → creates `board/STOP`. The orchestrator finishes its current handoff and stops.
- Or on the Mac: `touch ~/zlayt-pm-project/board/STOP`.
- **Resume after STOP:** from the phone, type into this Claude session (Remote Control): "Delete board/STOP and continue the loop." On the Mac: `rm ~/zlayt-pm-project/board/STOP`, then continue the session.

## Restart (after a crash, reboot, or closing the session)
1. `cd ~/zlayt-pm-project`
2. Board server: `./tools/serve_board.sh` (also installs the native git pre-commit secret scan if missing) (tmux session `zlayt`, window `board`). Check: `curl -s localhost:7777/healthz`.
3. Session — either:
   - Desktop app: reopen this session from the sidebar (it keeps bypass-permissions mode), or
   - Terminal: `claude --continue --dangerously-skip-permissions --remote-control` (without the first flag the run stalls on permission prompts nobody answers; the second lets you steer and resume from your phone).
4. Say:
   > Re-read CLAUDE.md, memory/STATE.md and `python3 tools/board.py status`. Re-spawn the worker agents (general-purpose subagents whose first step is `python3 tools/agent_prompt.py <role>` unless native agent types are available), recreate the heartbeat cron (text in memory/STATE.md), continue the loop.
5. Tailnet exposure persists across restarts (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.

## Useful commands
```
python3 tools/board.py status          # where are we
python3 tools/board.py list --status in_review
tail -f board/activity.jsonl           # raw event log
.venv/bin/python -m pytest tools/tests -q   # harness tests
```
