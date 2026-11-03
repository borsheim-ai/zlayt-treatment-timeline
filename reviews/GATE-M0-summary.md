# GATE M0 — Operating system (harness) — PASS

Date: 2026-11-02 · Orchestrator synthesis · Exit criteria: CONTRACT §4.8

## Evidence
| §4.8 check | Result | Evidence |
|---|---|---|
| 1 board.py round trip, illegal transition refused, validate catches bad card | pass | tools/tests/test_board.py (19 tests) |
| 2 board UI on localhost + tailnet, live feed, inbox → file → `board.py inbox` | pass | artifacts/m0-smoke/live-feed.md; reviews/T-002-staff-engineer-r3.md (pass) |
| 3 hooks by hand with crafted stdin | pass | tools/tests/test_hooks.py, test_git_guard.py (≈190 probes), test_board_guard.py |
| 4 agent definitions load | pass | native types loaded mid-session; artifacts/m0-smoke/agent-load-tests.md; tools/tests/test_agents.py |
| 5 Playwright screenshot | pass | artifacts/screenshots/m0-board.png, office-*.png |
| 6 conventional commits, .gitignore, tag m0 | pass | git log; tag applied with this gate |
| 7 heartbeat, STATE, RUNBOOK | pass | cron 0c86ab2d (hourly, D-024); memory/STATE.md; docs/RUNBOOK.md |

Harness test suite: 318 passing (`.venv/bin/python -m pytest tools/tests -q`).

## Card outcomes (Tier 1)
| Card | Reviewer(s) | Rounds | Outcome |
|---|---|---|---|
| T-001 board CLI | staff-engineer | 3 | accepted with documented debt (§7.4); r3 major fixed post-review with test |
| T-002 board UI | staff-engineer | 3 | pass (CSRF, XSS, DNS rebinding closed) |
| T-003 hooks | security | 3 | accepted with debt; both r2 blockers fixed; residuals per D-023 |
| T-004 agent definitions | staff-engineer | 3 | accepted with debt; r3 major fixed post-review with test |
| T-005 map/memory/runbook | product-manager | 3 | accepted with debt; r3 items fixed by orchestrator |
| T-006 secrets | security | 3 | pass |
| T-007 smoke test | staff-engineer | 2 | pass (r1 major rejected with evidence) |

## What the reviews changed (harness upgrades, see memory/LESSONS.md)
- git-guard rewritten from regex to argv parsing after security r1 found ~250 bypasses; newline separators after r2; threat model written down (D-023) to end the arms race.
- Identity-based board-guard (hook agent_id/agent_type): subagents cannot mark done, record reviews, or act as orchestrator.
- Board server: CSRF refusal, DOMPurify, Host allow-list (DNS rebinding), CSP + SRI.
- Secret scanner: NUL-safe names, renames, fail-closed, native pre-commit hook.
- §7.4 accept-with-debt path and stale-marker fixes in the stop guard.

## Blockers open: 0. Debt: memory/SCOPE_CUTS.md rows tagged "debt".
## Decision: M0 gate PASS. Tag m0.
