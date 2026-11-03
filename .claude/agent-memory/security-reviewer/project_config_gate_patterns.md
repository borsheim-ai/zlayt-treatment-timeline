---
name: config-gate-patterns
description: Recurring weaknesses in env-var gates of the Zlayt app (bind host read from env not the listener, record/live env toggles, label vs behaviour when ENABLE_LIVE is set without a key); where to probe first
metadata:
  type: project
---

Pattern 1: a gate that reads an env var instead of the thing it protects. T-053 r2: `create_app` refuses `ZLAYT_MODE=local` unless `HOST` is loopback (api.py:93-94), but `uvicorn app.main:create --factory --host 0.0.0.0` with HOST unset serves `/api/cases` on the LAN (verified: 200 from a non-loopback address). The `python -m app.main` path is safe because it passes the same env HOST to uvicorn. Fix shape: check the peer address per request (`request.client.host`) in local mode, not the configured host.

Pattern 2: a second env toggle that opens the same switch. `RECORD_FIXTURES=1` sets `_record_ok` through `record_context` and bypasses the ENABLE_LIVE check on the dev eval path (132 live stub calls in run_case). It is unreachable from the server today. Re-check whenever a new caller of `record_context`, `record_fragment_context` or `judge_summary` appears in app/backend/.

Pattern 3: the label disagrees with the behaviour. `ENABLE_LIVE=1` without a key makes `/api/health` report `backend: anthropic-api` while `demo_mode: true`, because `backend_name()` does not check the key that `live_enabled()` checks. No live call happens (fail closed), but the audit rows and the health label are wrong.

Pattern 4: a spec amendment that lives only in the card note. Local-mode library admission (T-053 decision 3) is not in memory/ORCHESTRATOR_DECISIONS.md; D-020 and R-CO-4 still say demo accepts only recorded hashes. Under D.2 that is a blocker if not amended before the gate.

Pattern 5 (T-053 r3): a peer-address gate is not loopback-only behind a loopback proxy. After the peer check (api.py:81-88, gate api.py:176) the uvicorn --host 0.0.0.0 bypass is closed (LAN 403, loopback 200), but a relay on 127.0.0.1 forwarding LAN clients gives 200 with no header added (out_probe Part B). The project's own tailnet exposure is `tailscale serve` in front of :7860 (RUNBOOK.md:8), and the card handoff says "works behind tailscale serve (loopback peer)". Forwarding headers are ignored from a LAN peer, and uvicorn honours X-Forwarded-For from a loopback peer, so a header-adding proxy fails closed. Fix shape: Host allowlist (localhost/127.0.0.1/[::1]) plus refusing Forwarded/X-Forwarded-*/X-Real-IP/Tailscale-* in local mode. Any "loopback only" rule must be checked behind every proxy the RUNBOOK documents.

**Why:** these are the five ways the T-053 gates were weakened or left inconsistent in rounds 1-3. The round-1 demo blocker (provider.py had no ENABLE_LIVE check) was of the same kind as pattern 1.
**How to apply:** for any card that adds an env var, a launch path, or a second caller of record or live code, check (a) what the gate reads versus what it protects, (b) every env toggle that can reach the same switch, (c) that health and audit labels match the backend that ran, and (d) that the spec text, not just the card note, carries the decision. Probe with a counting stub and a blocked socket, and launch through every documented entry point.

Related: [[demo-live-gate]], [[round2-review-workflow]]
