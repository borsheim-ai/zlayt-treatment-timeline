# M0 smoke check 2 — live activity feed

Newest event via GET /api/activity?limit=1 before and after `board.py log`:

before: `[{"ts": "2026-11-02T00:20:16Z", "event": "note", "agent": "orchestrator", "card": "T-007", "text": "Triage of round-1 review: MAJOR rejected — evidence is wrong: memory/PROGRESS.md:10 reads 'tag m0 pending M0 gate' (not PASS) and T-006 is in_review, not READY (board.py list --milestone M0). Minors accepted: saving load-test replies and live-feed evidence to artifacts/m0-smoke/. Nit (screenshot predates claim) accepted as-is: screenshot was taken before T-007 was claimed; it evidences the UI, not T-007's state."}]`

after: `[{"ts": "2026-11-02T00:20:16Z", "event": "smoke", "agent": "orchestrator", "card": null, "text": "live feed evidence probe"}]`

The UI polls this endpoint every 5 s (tools/board_ui.html, setInterval refresh).
