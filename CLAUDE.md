# Zlayt PM Project — map

**Mission.** Build Chris's Zlayt AI-PM candidate project end to end: a treatment-timeline prototype that turns synthetic medical
records into a verified chronology a paralegal can drop into a demand letter, plus the product note, Part 2 process doc, demo
assets and prompt log. The team (orchestrator + workers + reviewer personas) works through the board; *how* we work is graded too.

Full contract: `docs/CONTRACT.md` (never edited). Spec: `spec/SPEC.md`, `spec/SAMPLE_CASE_TRUTHS.md`, `spec/REQUIREMENTS.md` (M1).
Paths marked (M1)/(M2)… are created in that milestone; if one is missing, its card is still open — check `board.py list`.

## Non-negotiables (one line each)
1. Never wait for Chris: write `submission/NEEDS_CHRIS.md` + a `needs_chris` card, state the assumption, proceed.
2. Keep going until §11 Definition of Done is met (a Stop hook enforces it).
3. The board is the single source of truth; cards change state only through `tools/board.py`.
4. Synthetic data only (Appendix A records or records labeled SYNTHETIC).
5. The product may not invent facts: every statement traces to a verbatim excerpt of the input.
6. Models: orchestrator Opus; workers Sonnet (researcher Opus); judgment reviewers Opus; engineering reviewers Sonnet; mechanical Haiku.
7. No self-approval: a different agent, in a fresh context, reviews every card; workers never mark their own cards done.
8. Deterministic checks (tests, schema, grounding verifier, evals) run before any persona opinion.
9. Every failure upgrades the harness: a rule, hook, test, eval case or checklist item, recorded via `board.py lesson`.
10. Secrets never enter git (`.env` ignored; git-guard runs `tools/check_secrets.py --staged`); destructive git is blocked.
11. The orchestrator writes no product code after M0.
12. Record decisions, assumptions and scope cuts as you go (`memory/DECISIONS.md`, `ASSUMPTIONS.md`, `SCOPE_CUTS.md`).

## Board CLI cheat sheet (`B="python3 tools/board.py"`)
```
$B new --title ".." --milestone Mx --role r --priority P1 --ac "testable" [--status needs_chris]
$B next --role <role>            $B claim T-### --agent <role>        $B note T-### --agent <who> --text "..."
$B ac T-### --check N --agent <who> --evidence "..."                  $B handoff T-### --agent <who> --text "..."
$B move T-### in_review --agent <who>                                 $B review T-### --persona p --model m --verdict pass|changes|fail --file reviews/..
$B status [--brief|--json]       $B show T-###   $B list [--role r] [--status s]   $B lesson --agent <who> --text "..."
$B assign T-### --to <agent>     $B dispatch T-### --personas "a, b"   (mark queued work so the Stop hook ignores it)
$B inbox [--ack]                 $B milestone set Mx --status ...     $B gate Mx --record reviews/GATE-Mx-summary.md --result pass|fail
```
Statuses: backlog → ready → in_progress → in_review → (changes_requested → in_progress) → done; plus blocked, needs_chris, cancelled.

## Where things live
| Path | What |
|---|---|
| `board/cards/T-###.md`, `board/activity.jsonl`, `board/milestones.md` | cards, event log, milestones |
| `board/inbox/` | notes from Chris (board UI form) — read every cycle |
| `memory/STATE.md` | current truth + next 3 actions (orchestrator only) |
| `memory/{PROGRESS,DECISIONS,ASSUMPTIONS,SCOPE_CUTS,LESSONS,GLOSSARY,ENVIRONMENT}.md` | durable memory |
| `memory/ORCHESTRATOR_DECISIONS.md` | cross-cutting product decisions D-001.. from review triage — binding on spec + ADRs |
| `memory/contracts/api.md` | API contract (backend writes, frontend consumes) |
| `docs/LLM_VS_CODE.md` (M1) | LLM/code boundary + validation ladder table (graded) |
| `docs/RUNBOOK.md` | URLs; how Chris steers/stops/restarts |
| `personas/`, `research/` | researched dossiers, domain notes (with sources) |
| `reviews/<card>-<persona>.md` | every review, full text, D.2 JSON block |
| `app/` | prototype: `backend/ llm/ db/ frontend/` |
| `evals/`, `tests/` | golden set + runner + reports; unit + E2E |
| `artifacts/` | screenshots, demo video, captions, review evidence |
| `submission/` | product note, Part 2, prompt log, checklist, email draft, NEEDS_CHRIS |
| `tools/` | board.py, board_server.py + board_ui.html, serve_board.sh, check_secrets.py, compile_agents.py, export_prompt_log.py, screenshot_board.py |
| `.claude/agents/` | native agent types (workers + `*-reviewer`); `tools/agent_prompt.py <name>` is the fallback if a host doesn't load them |

## File ownership (write only your paths; cross-boundary = card for the owner; stage with `git add <paths>`, then commit with a pathspec `git commit -m msg -- <paths>` because the index is shared)
| Role | Owns |
|---|---|
| architect | `docs/LLM_VS_CODE.md`, `memory/DECISIONS.md`, `app/README-arch.md` (M1) |
| backend | `app/backend/**`, `app/llm/**`, `memory/contracts/api.md` |
| db | `app/db/**` |
| frontend | `app/frontend/**` |
| qa | `tests/**`, `evals/**`, `artifacts/**` (not review-evidence), `tools/install_test.sh` (M4) |
| release | `Dockerfile`, `deploy/**`, `README.md`, `.env.example`, `Makefile`, `run.sh`, `app/config.py` (all M4) |
| writer | `submission/**` |
| researcher | `research/**`, `personas/**`, `memory/GLOSSARY.md`, `app/llm/lexicon.yaml` |
| reviewers | `reviews/**`, `artifacts/review-evidence/**` only (hook-enforced) |
| orchestrator | `board/`, `memory/STATE.md`, `PROGRESS.md`, `ASSUMPTIONS.md`, `SCOPE_CUTS.md`, `CLAUDE.md`, `.claude/`, `tools/` |

## How to report
Reply ≤ 15 lines (reviewers ≤ 40): what you did, evidence paths, what's left. Details go in files and card notes, not chat.

## Review protocol (five lines)
1. Worker checks AC with evidence, writes the handoff, moves the card to `in_review`.
2. Orchestrator dispatches fresh reviewer subagents (staff-engineer or PM + one domain persona) with a D.6 brief — no worker claims.
3. Reviewer exercises the artifact, writes `reviews/<card>-<persona>.md` (D.2), verdict by rule: blocker→fail, major→changes, else pass.
4. `board.py review` records it; changes/fail sends the card back with findings pasted; max 3 rounds, then decide (§7.4).
5. Milestone gates run a panel in parallel; synthesis in `reviews/GATE-Mx-summary.md`; zero blockers to pass.

## Data rule
Synthetic only. The app shows a persistent "synthetic data only" banner. Never paste, fetch or imply real records.

## LLM/code boundary rule
Deterministic tasks are code, never LLM (dates, gaps, substring checks, currency, totals, sorting, dedupe, schema, export).
Language/judgment tasks are LLM, each behind the ladder: code check → independent LLM judge (different prompt/model) → human
accept/edit/dismiss. Nothing LLM-made reaches the export without all three. Dev backend: `LLM_BACKEND=claude-cli`.
