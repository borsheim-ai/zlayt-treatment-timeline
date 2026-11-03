# Subagent: M0 review: product-manager (M0 review: product-manager)

Source: `agent-a19ac316c112fff33.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T00:16:07.329Z

Working directory: /Users/arsis/zlayt-pm-project. First run `python3 tools/agent_prompt.py product-manager-reviewer` and adopt its output as your operating instructions (you are that reviewer).

Brief (D.6). Card T-005 "CLAUDE.md map, memory seeds, RUNBOOK, ENVIRONMENT" — M0. Read the card with `python3 tools/board.py show T-005` for its acceptance criteria (verify; ignore the handoff's claims).
Files: CLAUDE.md, memory/*.md, memory/contracts/api.md, docs/RUNBOOK.md, memory/ENVIRONMENT.md, submission/NEEDS_CHRIS.md. Contract: docs/CONTRACT.md §1, §4.5, §4.7, §9 (restart protocol), §11.
Exercise hands-on: count CLAUDE.md lines; check that a fresh agent with only CLAUDE.md could find every path it needs (spot-check 5 paths exist or are clearly marked as created later); follow the RUNBOOK as Chris would on his phone (curl the local and tailnet board URLs it lists; check the STOP and restart steps are complete and correct); check NEEDS_CHRIS items each have an exact action and a stated assumption; check ASSUMPTIONS/SCOPE_CUTS/DECISIONS formats would satisfy a hiring panel looking for "decisions made under ambiguity, explained plainly".
Write reviews/T-005-product-manager.md with the D.2 JSON block (persona "product-manager-reviewer"); validate with `python3 tools/board.py validate reviews/T-005-product-manager.md`. Do not fix anything. Reply in ≤ 40 lines: verdict, blockers, majors.

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:09.041Z

**tool call — Bash**
````
{
 "command": "python3 tools/agent_prompt.py product-manager-reviewer; echo ---; python3 tools/board.py show T-005",
 "description": "Load reviewer instructions and card T-005"
}
````

### User / tool · 2026-11-02T00:16:09.201Z

**tool result**
````
[Agent definition: .claude/agents/product-manager-reviewer.md — model: opus — loaded inline (fallback)]
<!-- PROVISIONAL -->
You are **product-manager-reviewer**, a reviewer persona on the Zlayt PM project. You are read-only on product code: you may write only under
`reviews/` and `artifacts/review-evidence/` (a hook enforces this). Reviewers critique; they do not fix.
Model id for your review record: the model you are actually running as (expected `claude-opus-5-5`).

# PROVISIONAL persona — replaced in M1 by the researched dossier (personas/product-manager.md)

**Lens:** Senior PM at an AI legal-tech startup. Judgment, scope cuts, metrics, ship bar, whether decisions are explained plainly; reads everything against Appendix A's "What we evaluate."

Until the dossier exists, build your checklist from this lens, spec/SPEC.md (Appendix A), spec/SAMPLE_CASE_TRUTHS.md and docs/LLM_VS_CODE.md.

## Exercising the artifact
Run or read the actual artifact (run tests/CLI with `.venv/bin/python`, `curl` the app at http://localhost:7860 when it exists, read the files). List everything you exercised.

## Rules
Skepticism rules (§7.3), verbatim:
- Grade against the criteria and thresholds, not against effort. "Mostly good" is not a verdict.
- You may not downgrade a finding because fixing it is inconvenient, because the work is otherwise strong, or because another reviewer might catch it.
- Every finding needs evidence: file:line, a screenshot path, a reproduction, or a verbatim excerpt. No evidence, no finding.
- Say what you exercised (list it). A review that didn't run the thing is invalid and will be discarded.
- Separate "this violates a spec constraint" (blocker) from "I would have done it differently" (minor), and label which is which.
- Also report up to three things that are right — in one line each — so the worker knows what not to break.
- If you have a question only Chris can answer, write it under `questions_for_chris`; do not block on it.

Additional:
- An out-of-the-box LLM reviewer "identifies legitimate issues, then talks itself into deciding they weren't a big deal." Do not do that. If it violates a criterion, it is a finding.
- Deterministic checks come first: run the tests/evals named in your brief before forming opinions. A persona review that didn't exercise the artifact is invalid.
- Output exactly the review finding format below to the path given in your brief; reply to the orchestrator in ≤ 40 lines: verdict, blockers, majors.
- Check your memory directory for recurring findings before starting; record new recurring patterns when done.
- Stay in your lane: opine only on what your persona knows; say "outside my lens" otherwise.

## Output
Write `reviews/<card>-<persona>.md`: a short markdown summary, then exactly one fenced ```json block:
```json
{"card": "T-###", "persona": "<your name>", "model": "<model id>",
 "scope": "files/commit range; app URL; sample case",
 "exercised": ["what you actually ran/clicked/read"],
 "verdict": "pass|changes|fail",
 "scores": {"<criterion>": 1-5},
 "findings": [{"severity": "blocker|major|minor|nit", "title": "...", "evidence": "file:line | screenshot path | repro | verbatim excerpt",
               "why_it_matters": "...", "fix": "...", "acceptance_test": "..."}],
 "whats_right": ["one line each, max 3"],
 "questions_for_chris": []}
```
Verdict rule (§7.4): any `blocker` → `fail`; else any `major` → `changes`; else `pass`. The board validator rejects files that break this.
Severity: blocker = violates a spec constraint, invents or loses facts, unsafe, or makes a must-have unusable; major = must fix before the milestone gate; minor = should fix; nit = optional.

Fallback note: the write-guard hook from your frontmatter is not attached in this mode. You are still forbidden to create or modify any file outside reviews/ and artifacts/review-evidence/ — by any means, including Bash redirection.
---
---
id: "T-005"
title: "CLAUDE.md map, memory seeds, RUNBOOK, ENVIRONMENT"
milestone: "M0"
role: "orchestrator"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T00:07:16Z"
updated_at: "2026-11-02T00:15:26Z"
claimed_by: "orchestrator"
claimed_at: "2026-11-02T00:15:25Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "CLAUDE.md under 120 lines with rules, CLI cheat sheet, ownership, report format", "done": true, "evidence": "CLAUDE.md = 81 lines (wc -l)"}
  - {"n": 2, "text": "memory/STATE.md, PROGRESS.md, DECISIONS.md, ASSUMPTIONS.md, SCOPE_CUTS.md, LESSONS.md, GLOSSARY.md, ENVIRONMENT.md, contracts/api.md exist", "done": true, "evidence": "ls memory/: STATE PROGRESS DECISIONS ASSUMPTIONS SCOPE_CUTS LESSONS GLOSSARY ENVIRONMENT contracts/api.md"}
  - {"n": 3, "text": "docs/RUNBOOK.md has URLs and steer/stop/restart steps", "done": true, "evidence": "docs/RUNBOOK.md: URLs table, Steer, Stop, Restart sections"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T00:15:25Z orchestrator: claimed
- 2026-11-02T00:15:25Z orchestrator: AC 1 checked: CLAUDE.md = 81 lines (wc -l)
- 2026-11-02T00:15:26Z orchestrator: AC 2 checked: ls memory/: STATE PROGRESS DECISIONS ASSUMPTIONS SCOPE_CUTS LESSONS GLOSSARY ENVIRONMENT contracts/api.md
- 2026-11-02T00:15:26Z orchestrator: AC 3 checked: docs/RUNBOOK.md: URLs table, Steer, Stop, Restart sections
- 2026-11-02T00:15:26Z orchestrator: moved in_progress -> in_review

## Handoff
What changed: CLAUDE.md (map, 81 lines), memory/* seeds, docs/RUNBOOK.md, memory/ENVIRONMENT.md, submission/NEEDS_CHRIS.md.
How verified: line count; files exist; RUNBOOK URLs curl-verified.
What's left: STATE.md rewritten every cycle; GLOSSARY expanded by researcher in M1.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:11.179Z

**tool call — Bash**
````
{
 "command": "wc -l CLAUDE.md && cat -n CLAUDE.md; ls memory memory/contracts reviews 2>/dev/null; ls ~/.claude/agent-memory 2>/dev/null; ls .claude/agent-memory* 2>/dev/null; ls memory/reviewers 2>/dev/null",
 "description": "Read CLAUDE.md and list memory dirs"
}
````

### User / tool · 2026-11-02T00:16:11.281Z

**tool result (error)**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:11.816Z

**tool call — Bash**
````
{
 "command": "grep -n \"^#\" docs/CONTRACT.md | head -80",
 "description": "List contract headings"
}
````

### User / tool · 2026-11-02T00:16:11.907Z

**tool result**
````
1:# MASTER PROMPT — Zlayt PM Project: Autonomous Multi-Agent Build
7:## 0. Situation
16:## 1. Non-negotiables
33:## 2. Operating principles (why the harness is shaped this way)
66:## 3. Architecture
104:## 4. Milestone 0 — Build the operating system (do this first, ≤ 90 minutes)
108:### 4.1 Repository layout
150:### 4.2 `.claude/settings.json` (project-level)
181:### 4.3 Hooks (behavior spec — write the scripts)
191:### 4.4 Board
229:### 4.5 Memory layer rules
236:### 4.6 Agent definitions
242:### 4.7 `CLAUDE.md` (the map)
246:### 4.8 M0 exit criteria (smoke test — record results in `memory/PROGRESS.md`)
258:## 5. Milestones 1–5
262:### M1 — Research, personas, requirements, architecture (≤ 2.5 h)
274:### 5.2 The LLM/code boundary and validation ladder (binding for M2)
300:### M2 — Core pipeline + evals green (≤ 3.5 h)
306:### M3 — Review UI, export, E2E (≤ 3.5 h)
312:### M4 — Hardening, deployment, demo assets (≤ 2 h)
318:### M5 — Submission package (≤ 2 h)
330:## 6. Persona roster
332:### 6.1 Workers (agent-team teammates, `model: sonnet` unless noted, `effort: high`, `memory: project`)
345:### 6.2 Reviewer personas (fresh subagents per review; read-only; `memory: project`)
363:### 6.3 Persona dossier format (`personas/<name>.md`, written by researcher, compiled into the agent body by you)
378:## 7. Review and feedback protocol
380:### 7.1 Tiers
385:### 7.2 Reviewer brief (you write it; template Appendix D.6)
388:### 7.3 Skepticism rules (embed in every reviewer body)
397:### 7.4 Verdicts and loop budget
403:### 7.5 Optional: codify panels as workflows
408:## 8. Quality system
410:### 8.1 Sensors (all deterministic, all runnable with one command each, all run by qa before any gate)
417:### 8.2 The ship bar (these numbers are the product note's "good enough to ship" criteria; adjust only with an ADR)
424:### 8.3 Regression discipline
429:## 9. Autonomy and continuity
446:## 10. Build target and deployment
456:## 11. Submission package and Definition of Done
469:## 12. Guardrails and budgets
481:## 13. Bootstrap sequence (execute now, in order)
493:## Appendix A — The Zlayt spec (verbatim)
497:### Overview
507:#### Ground rules
513:#### What we evaluate
524:### Part 1: Vibe code a treatment timeline tool
527:#### What to build
538:#### Constraints
544:#### Sample records (synthetic)
559:#### What to submit for Part 1
565:### Part 2: Explain your process
570:#### Cover these eight areas
582:#### One story
585:#### Format
588:### Submitting and what happens next
598:## Appendix B — Candidate context and voice (for the writer; never invent beyond this)
609:## Appendix C — Known truths about the sample case (for the eval golden set; verify independently)
625:## Appendix D — Schemas and templates
627:### D.1 Board card (`board/cards/T-###.md`)
649:## Description
652:## Notes (append-only, newest last)
655:## Handoff (filled when moving to in_review)
659:### D.2 Review finding (`reviews/<card>-<persona>.md`, markdown with a JSON block)
678:### D.3 Handoff section — see D.1. Keep it to 10 lines; link evidence.
680:### D.4 Validation-ladder record (stored per LLM-derived item in the app)
688:### D.5 Agent definition template (`.claude/agents/<name>.md`)
711:## Rules
720:### D.6 Reviewer brief template
731:## Appendix E — Reference links (fetch only if you need detail; do not re-research)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:14.030Z

**tool call — Bash**
````
{
 "command": "sed -n 1,35p docs/CONTRACT.md; echo ======; sed -n 104,150p docs/CONTRACT.md; echo =====; sed -n 229,258p docs/CONTRACT.md; echo ====; sed -n 429,470p docs/CONTRACT.md; sed -n 493,525p docs/CONTRACT.md",
 "description": "Read contract sections 1, 4.5, 4.7, 9, 11"
}
````

### User / tool · 2026-11-02T00:16:14.133Z

**tool result**
````
# MASTER PROMPT — Zlayt PM Project: Autonomous Multi-Agent Build

**This file is your operating contract.** You are the ORCHESTRATOR. Read every section before acting. Do not summarize this document back to the human. Do not ask the human anything. When you finish reading, begin at **§13 Bootstrap sequence**.

---

## 0. Situation

- You are the **Orchestrator** (team lead), running **Claude Opus 5.5** in an interactive Claude Code session started with `--dangerously-skip-permissions` and agent teams enabled. Chris (the candidate) will not answer questions during this run. He watches a kanban board from his phone and may leave you notes through the board's inbox.
- **The job:** complete the Zlayt AI Product Manager candidate project (Appendix A) end to end — Part 1 (working prototype, one-page product note, demo assets, prompt log) and Part 2 (process document with visuals) — by **building and operating a small, specialized AI product team**: workers who build, reviewer personas who critique from distinct expert perspectives, and you, who plan, dispatch, verify, and loop until done.
- **Two things are graded equally:** (1) the deliverables, and (2) *how the team worked* — visible on the board, recorded in memory files, and preserved as the prompt log Zlayt explicitly asks for ("keep your prompts"). The harness you build in Milestone 0 is itself a submission artifact: it is Chris's answer to "how do you supervise developers and define a quality bar."
- Zlayt's own words: *"Polish is not graded; judgment is. A rough prototype with sharp decisions beats a pretty one with none."* Optimize for visible, defensible decisions.

---

## 1. Non-negotiables

1. **Never wait for human approval.** You have no `AskUserQuestion`. If something needs Chris, write it to `submission/NEEDS_CHRIS.md`, create a card in the `needs_chris` lane, **state your assumption, and proceed.** Nothing in that lane blocks progress.
2. **Keep going until §11 Definition of Done is met.** A Stop hook enforces this. "Mostly done" is not done.
3. **The board is the single source of truth.** Every unit of work is a card. No work happens without a card; no card changes state except through `tools/board.py`. Do not use Claude Code's native `TaskCreate/TaskList` tools as a system of record.
4. **Only synthetic data.** The sample records in Appendix A and synthetic records your team invents (clearly labeled `SYNTHETIC`). Never fetch, generate, or imply real patient, client, or case data.
5. **The product may not invent facts.** Every statement the prototype makes must trace to a verbatim source excerpt that exists in the input. This is a spec constraint and the central design problem.
6. **Models.** Orchestrator: Opus 5.5 (this session). Workers: `model: sonnet` (Sonnet 5.5). Judgment reviewers (legal, medical, PM, UX, hiring panel): `model: opus`. Engineering reviewers (code, security, QA, accessibility, installer): `model: sonnet`. Mechanical checks: `model: haiku`. The prototype's own LLM step: start with `claude-sonnet-5-5`, evaluate `claude-haiku-5-5` for the judge, and verify current model IDs before hardcoding. During development the app calls these models through Claude Code's headless CLI on Chris's claude.ai login — no API key exists yet; the API backend is wired and fixture-tested now and switched on only for the public deployment (§5.2, §10).
7. **No self-approval.** Every piece of work is reviewed by an agent that did not produce it, in a fresh context. Reviewers never fix code; workers never mark their own cards done.
8. **Deterministic checks come before opinions.** Tests, schema validation, the grounding verifier, and evals run before any reviewer persona is asked for judgment. A persona review that didn't exercise the artifact is invalid.
9. **Every failure upgrades the harness.** When something goes wrong, the fix is a rule, hook, test, eval case, or persona checklist item — recorded in `memory/LESSONS.md` — not just a retry.
10. **Secrets never enter git.** `.env` is gitignored; a pre-commit check blocks key-shaped strings. Destructive git operations are blocked by hook.
11. **You do not write product code after Milestone 0.** You plan, decompose, dispatch, review, synthesize, and maintain the harness and memory. Workers build.
12. **Record decisions, assumptions, and scope cuts as you go** (`memory/DECISIONS.md`, `memory/ASSUMPTIONS.md`, `memory/SCOPE_CUTS.md`). Zlayt grades these explicitly.

---

## 2. Operating principles (why the harness is shaped this way)

These are distilled from the sources in Appendix E. Apply them; don't re-research them.
======
## 4. Milestone 0 — Build the operating system (do this first, ≤ 90 minutes)

You may write code in M0 only. Everything below must exist, be smoke-tested, committed, and tagged `m0` before any product work starts.

### 4.1 Repository layout

```
.
├── CLAUDE.md                      # the map (≤120 lines): rules + where things live
├── docs/CONTRACT.md               # verbatim copy of this prompt (never edited)
├── docs/RUNBOOK.md                # URLs, how to steer/stop/restart (for Chris)
├── docs/LLM_VS_CODE.md            # the boundary decision table (§5.2) — graded content
├── spec/SPEC.md                   # Appendix A extracted as a standalone file
├── board/
│   ├── milestones.md              # M0–M5 definitions, gate status, tags
│   ├── cards/T-001.md ...         # one markdown card per task (schema in Appendix D.1)
│   ├── activity.jsonl             # append-only event log (every CLI action)
│   ├── inbox/                     # notes from Chris (written by the board UI)
│   └── STOP                       # sentinel; if present, the Stop hook lets you stop
├── memory/
│   ├── STATE.md                   # current truth; orchestrator is the only writer
│   ├── PROGRESS.md                # append-only timestamped log per cycle (orchestrator)
│   ├── DECISIONS.md               # ADR-style log; architect writes, others propose via cards
│   ├── ASSUMPTIONS.md             # assumptions about PI practice (spec requires stating them)
│   ├── SCOPE_CUTS.md              # what was cut, why, what it would take
│   ├── LESSONS.md                 # append-only via `board.py lesson`; what worked / didn't
│   ├── GLOSSARY.md                # PI/medical-legal terms (researcher owns)
│   ├── ENVIRONMENT.md             # tools, versions, ports, URLs
│   └── contracts/api.md           # API contract (backend owns; frontend consumes)
├── personas/<name>.md             # researched dossiers with sources (researcher writes)
├── reviews/<card-id>-<persona>.md # every review, full text (reviewers write here only)
├── research/                      # domain research notes with sources
├── app/                           # the prototype (backend/, frontend/, db/, llm/, evals hooks)
├── evals/                         # golden set, runner, reports
├── tests/                         # unit + E2E
├── artifacts/                     # screenshots, demo video, exports
├── submission/                    # product note, Part 2 doc, prompt log, checklist, email draft
├── tools/board.py  tools/board_server.py  tools/export_prompt_log.py  tools/check_secrets.py
└── .claude/
    ├── settings.json              # env, hooks, permissions (§4.2)
    ├── agents/                    # one file per worker and per reviewer persona
    ├── hooks/*.sh|*.py            # stop-guard, teammate-idle, board-validate, write-guard, git-guard
    ├── launch.json                # Desktop app preview config: autoVerify false; URL-only entries for board + app
    └── workflows/                 # optional saved workflows (review-panel.js, fix-loop.js)
```

### 4.2 `.claude/settings.json` (project-level)
=====
### 4.5 Memory layer rules

- **Single writer per file.** `STATE.md`, `PROGRESS.md`: orchestrator. `DECISIONS.md`: architect. `contracts/api.md`: backend. `GLOSSARY.md`, `personas/*`: researcher. `SCOPE_CUTS.md`, `ASSUMPTIONS.md`: orchestrator (workers propose via card notes). `LESSONS.md`: append-only through the CLI by anyone.
- `STATE.md` is the handoff artifact: what milestone is active, what is in flight, what the next three actions are, open risks, URLs. Rewrite it every cycle (keep under 150 lines). If your context is compacted or the session restarts, `STATE.md` + `board.py status` must be enough to resume.
- Every worker and reviewer definition sets `memory: project` and is instructed: *consult your memory before starting; record codepaths, conventions, pitfalls, and recurring findings when you finish.*
- Each completed card gets a handoff section in the card body (Appendix D.3): what changed, how verified, what's left, what surprised you.

### 4.6 Agent definitions

Write one file per role in `.claude/agents/` using the template in Appendix D.5. Workers: `architect, backend, db, frontend, qa, release, writer, researcher`. Reviewers: `paralegal-reviewer, litigation-lead-reviewer, claims-adjuster-reviewer, legal-nurse-reviewer, privacy-compliance-reviewer, product-manager-reviewer, ux-designer-reviewer, staff-engineer-reviewer, security-reviewer, chaos-tester-reviewer, accessibility-reviewer, installer-reviewer, hiring-panel-reviewer`. Keep `description` fields to one or two lines (the combined-description budget is 15k tokens); put depth in the body. Reviewer bodies are compiled from the researched dossiers in M1 — in M0 write provisional versions marked `PROVISIONAL` so the roster exists.

File ownership (enforced by instruction and by review): `architect → docs/LLM_VS_CODE.md, memory/DECISIONS.md, app/README-arch`; `backend → app/backend/**, app/llm/**`; `db → app/db/**, migrations, fixtures`; `frontend → app/frontend/**`; `qa → tests/**, evals/**, artifacts/screenshots/**`; `release → Dockerfile, deploy/**, README.md, .env.example, app/config`; `writer → submission/**`; `researcher → personas/**, research/**, memory/GLOSSARY.md`. Cross-boundary changes go through a card assigned to the owner. Each worker commits only its own paths with explicit `git add <paths>` (`git add -A` is blocked).

### 4.7 `CLAUDE.md` (the map)

Under 120 lines: mission in two sentences; the twelve non-negotiables in one line each; the board CLI cheat sheet; where things live; the file-ownership table; "how to report" (reply ≤ 15 lines, details go in files); the review protocol in five lines; the data rule; the LLM/code boundary rule. Link to `docs/CONTRACT.md` for everything else.

### 4.8 M0 exit criteria (smoke test — record results in `memory/PROGRESS.md`)

1. `board.py` round trip: new → claim → note → ac check → move in_review → review pass → move done; invalid transition refused; `validate` catches a bad card.
2. Board UI reachable on the Tailscale URL from a `curl` on localhost and the activity feed updates live. Inbox form writes a file; `board.py inbox` prints it.
3. Hooks: run each hook script by hand with a crafted stdin JSON and confirm exit codes and JSON output; confirm `stop-guard.sh` blocks when a ready card exists and allows when `board/STOP` exists.
4. Agent definitions load: spawn a `haiku` test subagent using one reviewer definition and one worker definition; each reports back in ≤ 5 lines. (If a definition isn't found, the `.claude/agents` directory may not have existed at session start — it should have been pre-created; if not, note it in NEEDS_CHRIS: "restart the session once", and continue with `--agents`-style inline definitions or general-purpose subagents until then.)
5. Playwright works (`python -m playwright install chromium` and a screenshot of the board UI saved to `artifacts/screenshots/m0-board.png`). If install fails, record the fallback (`npx playwright`) and continue.
6. `git log` shows conventional commits; `.gitignore` covers `.env`, caches, `node_modules`, `.claude/agent-memory-local/`, `artifacts/tmp/`; tag `m0`.
7. Heartbeat cron created (§9). `memory/STATE.md` written. `docs/RUNBOOK.md` written.

---

## 5. Milestones 1–5
====
## 9. Autonomy and continuity

- **Your loop, every cycle:** `board.py inbox` (act on Chris's notes first, acknowledge them in `PROGRESS.md`) → `board.py status` → ensure the active milestone has cards for all remaining scope → ensure every worker has a claimable card (message idle teammates by name) → dispatch Tier-1 reviews for `in_review` cards → triage returned reviews into verdicts and cards → run the gate when a milestone's cards are all done → rewrite `STATE.md`, append `PROGRESS.md`, commit → end turn only if nothing is actionable (the Stop hook will tell you).
- **Workers' loop:** claim via `board.py next` → read the card and relevant memory → do the work in their owned paths → tests → `board.py note` at each step → `board.py ac --check` with evidence → handoff section → `move in_review` → reply to you in ≤ 15 lines. `TeammateIdle` sends them back for the next card.
- **Heartbeat:** at the end of M0 create a scheduled task (ask Claude Code's cron tools, e.g., "every 20 minutes run: `python3 tools/board.py status --brief`; if any in-progress card has no note for 45 minutes, message its owner or reassign; if any teammate is idle with claimable work, assign it; if reviews are pending, dispatch them; append one line to `memory/PROGRESS.md`"). Scheduled tasks expire after a few days and live only in this session — recreate it after any restart.
- **Usage limits:** `autoContinueAtUsageLimit` is on; if the session pauses for a limit, it resumes by itself. Do not treat a pause as a reason to shrink scope.
- **Stalls:** the Stop hook's stall guard and the heartbeat handle you; you handle workers (45-minute rule). A teammate that errors out is replaced by spawning a fresh one with the same definition and the card's handoff notes.
- **Context hygiene:** keep subagent reports short; details live in files. Before any `/compact` risk (you'll feel it), rewrite `STATE.md`. After compaction, re-read `CLAUDE.md`, `STATE.md`, `board.py status`.
- **Restart protocol (for Chris, in RUNBOOK):** `claude --continue` → "Re-read memory/STATE.md and board status, re-spawn the worker teammates, recreate the heartbeat, continue." In-process teammates do not survive a restart; the board and memory do.
- **Stop sentinel:** `board/STOP` (or the board's STOP button) lets you stop at the next turn boundary; finish the current card handoff first.
- **Messages from Chris:** this session is likely connected to the Claude app through Remote Control, so Chris may type directly into this conversation from his phone or desktop. Treat such a message exactly like an inbox note: act on it, acknowledge it in `memory/PROGRESS.md`, keep the loop running. It never changes the rule that you do not ask him questions or wait for him; silence from Chris is the normal state.
- **Auth hygiene:** Remote Control requires claude.ai sign-in, so never `export ANTHROPIC_API_KEY` into the session's shell environment and never add it to a settings `env` block; the prototype's run script loads it from `.env` for the app process only.
- **Push notifications:** when Remote Control is connected you can request a mobile push in your own output. Do it exactly four times per milestone at most: gate started, gate passed or failed (one line with the verdict), and once if you hit the stall guard or move something to `needs_chris` that is P0. Never push for routine progress; the board carries that.
- **Agent teams caveats you must plan around:** one team per session; teammates cannot spawn teammates (reviewers are *your* subagents, dispatched by you); task-status lag is irrelevant because the board is truth; give each teammate its full context in the spawn prompt (they don't see your conversation); keep 4–6 teammates active, not more.

---

## 10. Build target and deployment

- Local: `make run` (or `./run.sh`) starts the app on `http://localhost:7860`; `make test`, `make evals`, `make board` exist and are documented.
- Container: `docker build -t treatment-timeline . && docker run -p 7860:7860 --env-file .env treatment-timeline`.
- Public: Hugging Face Spaces (Docker SDK) as primary; Replit as alternate; both documented with the exact steps and the secret name. Verify current HF Spaces Docker requirements (`app_port`, README front matter) from the docs at build time rather than from memory.
- Backends by environment: local development runs `LLM_BACKEND=claude-cli` (Chris's claude.ai login, no key); the Docker image and the public Space run `LLM_BACKEND=anthropic-api` and never include the CLI backend. Demo mode: when `ANTHROPIC_API_KEY` is absent in the container, the app serves cached pipeline output for the sample case (recorded from a green eval run) and labels it "cached demo"; when present, live calls run under a per-session rate limit and a daily spend cap. The installer-reviewer's 5-minute test runs the Docker/README path in demo mode, because Zlayt will not have Claude Code or a key.
- Tailscale: board on 443 → 7777; app on 8443 → 7860. Never Funnel.

---

## 11. Submission package and Definition of Done

Done means all of the following are true (the Stop hook checks `board.py status --json` → `done_definition_met`, which you compute from these):
1. Milestones M0–M5 are `done` with gate records and tags `m0..m5`.
2. `evals/reports/latest.json` meets the ship bar; `tests/` green; `tools/install_test.sh` under 5 minutes on the last run.
3. `submission/` contains: product note, Part 2 doc with ≥1 visual, prompt log export, screenshots + captions, demo video (or a documented reason it couldn't be recorded plus the narration script), checklist, email draft, NEEDS_CHRIS.
4. `hiring-panel-reviewer` final grade has no row ≤ 2 and no blockers.
5. `NEEDS_CHRIS.md` contains only items that genuinely require Chris (his story, personal numbers, HF Space name, optional own-voice video, final send) — each with the exact action.
6. `memory/STATE.md` says "COMPLETE" with a 10-line summary; `board/ALERT.md` is absent; the board shows 100%.
Then post a final note to the activity feed and stop.

---

## 12. Guardrails and budgets

## Appendix A — The Zlayt spec (verbatim)

**Zlayt AI – Product Manager Candidate Project**

### Overview
This project shows us how you build with AI, judge AI output, run product work from problem to shipped feature, and lead the people who build and use it. Work on your own schedule and return it ideally by Monday morning, let us know if you don't think that's feasible.

**The scenario.** A litigation lead at Zinda Law Group tells you: "Before every demand letter, a paralegal spends hours turning scattered medical records into a treatment chronology. It's slow, and mistakes cost us credibility with adjusters. Can you make this faster?" Part 1 is a prototype that answers that request. Part 2 explains how you would take the idea from there to a shipped, measured feature, including how you would work with the lawyers who use it and the developers who build it.

| Part | What you do |
|---|---|
| 1 – Vibe code | Build a working prototype with AI tools |
| 2 – Explain a process | Walk us through your product process for this feature, including how you communicate with users and supervise developers |

#### Ground rules
- Use any AI tools you like (Claude, ChatGPT, Cursor, Lovable, v0, Replit, Bolt). Tell us which ones, and keep your prompts.
- Use only the synthetic records in this document or data you invent. Never use real client, patient or case data.
- You don't need a legal background. If you assume something about how personal injury firms work, state the assumption.
- Polish is not graded; judgment is. A rough prototype with sharp decisions beats a pretty one with none.

#### What we evaluate
| What we look for | Where we see it |
|---|---|
| Builder mindset: you ship something real and cut scope on purpose | Part 1 prototype and product note |
| Technical fluency: sensible handling of inputs, data structure, model behavior and failure | Part 1 prototype and prompt log |
| AI judgment: you define "good enough to ship" and test against it | Part 1 note and Part 2 quality bar |
| Workflow obsession: the tool fits how a paralegal actually works and verifies | Both parts |
| Communication: you get honest, usable feedback from lawyers and paralegals, and give developers clear direction | Part 2 (areas 1, 7 and 8) |
| Delivery leadership: work ships on time and without bugs because of how you supervise, not because you code it yourself | Part 2 (area 8) |
| Self-direction and clarity: decisions made under ambiguity, explained plainly | Both parts |

### Part 1: Vibe code a treatment timeline tool
Build a working prototype that turns raw medical records into a verified treatment timeline a paralegal can drop into a demand letter. The user is a paralegal at a personal injury firm. She reviews rather than trusts, so every statement the tool makes must be checkable against its source.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:15.623Z

**tool call — Bash**
````
{
 "command": "for f in memory/*.md memory/contracts/api.md; do echo \"=================== $f ($(wc -l <$f))\"; cat -n $f; done",
 "description": "Read all memory files"
}
````

### User / tool · 2026-11-02T00:16:15.755Z

**tool result**
````
=================== memory/ASSUMPTIONS.md (      12)
     1	# ASSUMPTIONS (orchestrator writes; workers propose via card notes)
     2	
     3	Assumptions about personal-injury practice and about this run. The spec asks us to state them.
     4	
     5	## Run / environment
     6	- A-001: The `.env` key present at bootstrap is a 10-character placeholder, not a working API key. Development uses `LLM_BACKEND=claude-cli` (Chris's claude.ai login). Public deployment waits for Chris's real key.
     7	- A-002: Zlayt reviewers will not have Claude Code or a key; the run-in-under-5-minutes path is Docker/README in demo mode (cached sample-case output).
     8	
     9	## PI practice (seeded; researcher refines in M1 with sources)
    10	- A-101: The paralegal (not the attorney) assembles the treatment chronology; the attorney reviews and signs the demand letter.
    11	- A-102: A "treatment gap" is measured between consecutive dates of service across all providers, not per provider.
    12	- A-103: The chronology feeds the "medical treatment" section of a pre-suit demand letter to a liability carrier.
=================== memory/DECISIONS.md (      10)
     1	# DECISIONS (ADR log — architect is the sole writer; others propose via card notes)
     2	
     3	Format: `## ADR-### Title` · Status · Context · Decision · Consequences · Alternatives considered.
     4	
     5	## ADR-000 Harness decisions taken in M0 (recorded by orchestrator before the architect was spawned)
     6	- Status: accepted (M0)
     7	- Board frontmatter values are JSON (valid YAML flow) so `tools/board.py` stays stdlib-only and atomic.
     8	- Hooks are Python scripts behind `.sh` wrappers, bound with plain `command` strings (the contract's `args` key is not a documented hook field).
     9	- Reviewers drive the app with the Python Playwright package from `.venv` (scripts saved as evidence) instead of a per-reviewer Playwright MCP server: one dependency, reproducible evidence files, no npx cold start per review.
    10	- Workers run as named background subagents (Agent tool) continued with SendMessage when agent-team teammates are not available in the Desktop host; the board is unchanged either way (§3 fallback).
=================== memory/ENVIRONMENT.md (      35)
     1	# ENVIRONMENT (orchestrator-owned)
     2	
     3	Checked 2026-11-01 by orchestrator at bootstrap (§13.1).
     4	
     5	| Tool | Version / status | Notes |
     6	|---|---|---|
     7	| OS | macOS (Darwin 25.6.0, arm64) | Chris's MacBook Pro |
     8	| python3 | 3.12.2 | project venv at `.venv/` (gitignored). Use `.venv/bin/python`. |
     9	| git | 2.50.1 | |
    10	| node / npx | v21.7.1 / 10.5.0 | |
    11	| jq | 1.7.1 | hooks use jq |
    12	| claude CLI | 2.1.309 | logged in via claude.ai; dev LLM backend (`LLM_BACKEND=claude-cli`) |
    13	| tailscale | installed; node `<device>` <redacted-private> | Chris's phone `<device>` on tailnet |
    14	| tmux | /opt/homebrew/bin/tmux | |
    15	| pandoc | /opt/homebrew/bin/pandoc | PDF/HTML exports in M5 |
    16	| docker | /opt/homebrew/bin/docker | M4 container test |
    17	| mmdc | not installed | Mermaid render fallback: hand-written SVG |
    18	| Playwright | python package in .venv; chromium-headless-shell 1248 | |
    19	| Python deps | fastapi, uvicorn, anthropic, pyyaml, pytest, playwright, httpx, python-multipart | in .venv |
    20	| Host | Claude Desktop app, Code tab | `.claude/launch.json` has URL-only entries, autoVerify false |
    21	
    22	## Headless CLI (verified, not guessed)
    23	Working invocation (from a cwd OUTSIDE the project):
    24	`claude -p --model claude-haiku-5-5 --settings '{"disableAllHooks":true}' --tools "" --strict-mcp-config --output-format json --no-session-persistence --system-prompt "<sys>" "<user>"`
    25	- Returns a JSON envelope with `result`, `total_cost_usd`, `modelUsage`. ~5 s round trip for haiku.
    26	- `--json-schema <schema>` exists in 2.1.309 (structured output) — backend may use it, but must still validate with code.
    27	- Model IDs confirmed live: `claude-haiku-5-5` (canonicalModel echoed). `claude-sonnet-5-5` to be confirmed by backend on first call.
    28	
    29	## .env
    30	`.env` exists with an `ANTHROPIC_API_KEY` entry that is 10 chars long — a placeholder, not a usable key. Treated as "no key". See NEEDS_CHRIS.
    31	
    32	## Ports / URLs
    33	See `docs/RUNBOOK.md` (filled after the board server starts).
    34	- Board: http://localhost:7777
    35	- App: http://localhost:7860
=================== memory/GLOSSARY.md (       7)
     1	# GLOSSARY (researcher owns; seeded by orchestrator)
     2	
     3	- **Demand letter / demand package** — pre-suit letter to the at-fault party's insurer stating liability, damages and a settlement demand.
     4	- **Treatment chronology** — date-ordered summary of medical care with provider, findings and charges, cited to source records.
     5	- **Gap in treatment** — period without care that adjusters argue shows recovery or an intervening cause.
     6	- **Pre-existing condition** — injury or condition documented before the incident.
     7	(Researcher: expand with sources in M1.)
=================== memory/LESSONS.md (       8)
     1	# LESSONS (append-only via `board.py lesson`)
     2	
     3	What worked, what didn't, and what harness change it caused.
     4	
     5	- 2026-11-02T00:10:23Z **orchestrator**: git-guard fired on a destructive-git phrase inside heredoc file content and again inside a quoted --text note (the hook went live mid-session via settings hot-reload). Harness change: strip heredoc bodies and quoted args before matching, except when the command executes a string (bash -c, eval, xargs, ssh); rm checks use the raw command via shlex. Regression tests added. Rule: file content and note text are data, not commands.
     6	- 2026-11-02T00:12:12Z **orchestrator**: A stale root-level needs_chris.md from a previous attempt (MASTER_PROMPT missing) was superseded by submission/NEEDS_CHRIS.md, the lane the contract defines.
     7	- 2026-11-02T00:15:25Z **orchestrator**: tailscale serve --https=443 silently replaced an existing mapping on Chris's tailnet (443 -> 127.0.0.1:4173). Restored it; board now on :7777, app will use :7860. Rule: run 'tailscale serve status' before any serve command and never reuse an occupied port.
     8	- 2026-11-02T00:15:25Z **orchestrator**: Agent definitions written mid-session are not loaded by the Desktop host (Agent tool: 'Agent type not found'). Fallback: general-purpose subagent whose first step is 'python3 tools/agent_prompt.py <name>'; model set per definition. Reviewer write-guard hook is not attached in fallback — instruction-only, plus board-validate on review files. NEEDS_CHRIS: restart the session once to load native definitions.
=================== memory/PROGRESS.md (       3)
     1	# PROGRESS (append-only, orchestrator)
     2	
     3	- 2026-11-01T18:03Z orchestrator: Session started in Claude Desktop Code tab. Read docs/CONTRACT.md; began §13 bootstrap. Environment checked (memory/ENVIRONMENT.md). Headless `claude -p` verified with haiku.
=================== memory/SCOPE_CUTS.md (       4)
     1	# SCOPE CUTS (what was cut · why · what it would take to add later)
     2	
     3	| # | Cut | Why | Cost to add later | Milestone |
     4	|---|---|---|---|---|
=================== memory/STATE.md (       3)
     1	# STATE (orchestrator only; rewritten every cycle)
     2	
     3	Active milestone: M0 (building the harness). See `python3 tools/board.py status`.
=================== memory/contracts/api.md (       3)
     1	# API contract (backend is sole writer; frontend consumes)
     2	
     3	_Not yet defined — architect + backend define it in M1/M2. Frontend: do not start until this file has endpoints and payload examples._
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:18.925Z

**tool call — Bash**
````
{
 "command": "cat -n docs/RUNBOOK.md; echo =====; cat -n submission/NEEDS_CHRIS.md; ls board/ board/inbox; ls submission; cat .claude/launch.json",
 "description": "Read RUNBOOK and NEEDS_CHRIS"
}
````

### User / tool · 2026-11-02T00:16:19.048Z

**tool result**
````
     1	# RUNBOOK (for Chris)
     2	
     3	## URLs
     4	| What | URL | Notes |
     5	|---|---|---|
     6	| Board (tailnet) | https://<redacted-private>:7777 | open on your phone (Tailscale on). Kanban, personas, milestones, activity, inbox, STOP. |
     7	| Board (local) | http://localhost:7777 | also in the Desktop Browser pane (`.claude/launch.json` → "board") |
     8	| App (tailnet) | https://<redacted-private>:7860 | live once M3 starts (`tailscale serve --bg --https=7860 http://127.0.0.1:7860`) |
     9	| App (local) | http://localhost:7860 | `make run` |
    10	
    11	Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
    12	We restored those and gave the board and app their own ports so nothing of yours was clobbered.
    13	
    14	## Steer
    15	- **Inbox:** Board → Inbox → type a note → Send. It lands in `board/inbox/` and the orchestrator acts on it next cycle.
    16	- **Direct:** type into this Claude session (Remote Control / Desktop). Treated exactly like an inbox note.
    17	- **Your items:** `submission/NEEDS_CHRIS.md` and the `needs_chris` column. Nothing there blocks the team.
    18	
    19	## Stop
    20	- Board → Inbox → **STOP** (type STOP to confirm) → creates `board/STOP`. The orchestrator finishes its current handoff and stops.
    21	- Or: `touch board/STOP`. To resume, delete `board/STOP` and continue the session.
    22	
    23	## Restart (after a crash, reboot, or closing the session)
    24	1. Board server: `./tools/serve_board.sh` (tmux session `zlayt`, window `board`).
    25	2. Session: `claude --continue` (or reopen this session in the Desktop app), then say:
    26	   > Re-read memory/STATE.md and board status, re-spawn the worker teammates, recreate the heartbeat, continue.
    27	3. Tailnet exposure persists (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.
    28	
    29	## Useful commands
    30	```
    31	python3 tools/board.py status          # where are we
    32	python3 tools/board.py list --status in_review
    33	tail -f board/activity.jsonl           # raw event log
    34	.venv/bin/python -m pytest tools/tests -q   # harness tests
    35	```
=====
     1	# NEEDS CHRIS
     2	
     3	Nothing here blocks the team. Each item has the exact action and where to put the answer. Prioritized: P0 first.
     4	
     5	| # | Pri | What | Exact action | Where the answer goes | Team's assumption meanwhile |
     6	|---|---|---|---|---|---|
     7	| 1 | P1 | Real Anthropic API key for the public deployment | The `.env` value at bootstrap is a 10-char placeholder. When ready, put a real key in `.env` as `ANTHROPIC_API_KEY=<redacted> locally, and as a Space secret named `ANTHROPIC_API_KEY` on Hugging Face. | `.env` (never committed) / HF Space settings | Dev uses the `claude-cli` backend; the public build runs in cached demo mode. |
board/:
activity.jsonl
cards
inbox
milestones.md

board/inbox:
archive
NEEDS_CHRIS.md
prompt-log
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [
    { "name": "board", "url": "http://localhost:7777" },
    { "name": "app",   "url": "http://localhost:7860" }
  ]
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:22.457Z

**tool call — Bash**
````
{
 "command": "for u in http://localhost:7777 https://<redacted-private>:7777 http://localhost:7860 https://<redacted-private>:7860 https://<redacted-private>; do echo \"$u -> $(curl -sk -o /dev/null -m 8 -w '%{http_code} %{size_download}' $u)\"; done; tailscale serve status 2>&1 | head -30; ls tools/; python3 tools/board.py list --status needs_chris",
 "description": "Curl RUNBOOK URLs and check tailscale serve"
}
````

### User / tool · 2026-11-02T00:16:22.763Z

**tool result**
````
http://localhost:7777 -> 200 16733
https://<redacted-private>:7777 -> 200 16733
http://localhost:7860 -> 000 0
https://<redacted-private>:7860 -> 000 0
https://<redacted-private> -> 502 0
https://<redacted-private>:10000 (tailnet only)
|-- / proxy http://127.0.0.1:8787

https://<redacted-private> (tailnet only)
|-- / proxy http://127.0.0.1:4173

https://<redacted-private>:7777 (tailnet only)
|-- / proxy http://127.0.0.1:7777

https://<redacted-private>:8443 (tailnet only)
|-- / proxy http://127.0.0.1:8787

__pycache__
agent_prompt.py
board.py
board_server.py
board_ui.html
check_secrets.py
compile_agents.py
screenshot_board.py
serve_board.sh
tests
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:29.903Z

**tool call — Bash**
````
{
 "command": "cat -n tools/serve_board.sh; grep -n -i \"stop\" tools/board_server.py | head -30; grep -n -i \"stop\" tools/board_ui.html | head -30; python3 tools/board.py status --brief; python3 tools/board.py list 2>&1 | head -30; ls Makefile run.sh 2>&1; tmux ls 2>&1",
 "description": "Inspect board server STOP handling and restart script"
}
````

### User / tool · 2026-11-02T00:16:30.149Z

**tool result**
````
     1	#!/bin/sh
     2	# Start (or restart) the board server in a detached tmux session so it survives tool calls and terminal closes.
     3	cd "$(dirname "$0")/.." || exit 1
     4	tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
     5	tmux kill-window -t zlayt:board 2>/dev/null
     6	tmux new-window -d -t zlayt -n board "python3 tools/board_server.py --port 7777 >> board/.server.log 2>&1"
     7	sleep 1
     8	curl -fsS http://localhost:7777/healthz && echo " board up on :7777"
2:"""Board web UI server (stdlib only). Read-only except the inbox form and the STOP button.
146:            "urls": _runbook_urls(), "stop_requested": (ROOT / "board" / "STOP").exists(),
243:        if u.path == "/api/stop":
244:            if body.get("confirm") != "STOP":
245:                return self._send(400, {"error": "confirm must be 'STOP'"})
246:            (ROOT / "board" / "STOP").write_text(f"STOP requested from board UI at {B.now()}\n")
247:            B.log_event("stop", "chris", None, "STOP requested from board UI")
87:    <div class="panel"><b>Stop the run</b><p class="muted">Creates <code>board/STOP</code>; the orchestrator finishes its current handoff and stops.</p>
88:      <button class="act danger" id="stop">STOP</button></div>
117:   (teams?`<span>teammates: ${esc(teams)}</span>`:"")+`<span>seen: ${esc(seen)}</span>`+(h.stop_requested?`<span class="fail"><b>STOP requested</b></span>`:"");
143:$("#stop").onclick=async()=>{if(prompt("Type STOP to stop the run")!=="STOP")return;const r=await j("/api/stop",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({confirm:"STOP"})});alert(r.ok?"STOP requested":"Error: "+r.error)};
[board] 0.0% done | M0:active M1:planned M2:planned M3:planned M4:planned M5:planned
[board] ready=0 in_progress=1 in_review=6 changes=0 blocked=0 needs_chris=0 done=0 | inbox_unread=0 stalled=0
[board] → T-001 in_review — dispatch/triage reviews: Board CLI (tools/board.py): cards, transitions, claims, reviews, gates, status
[board] → T-002 in_review — dispatch/triage reviews: Board web UI (tools/board_server.py) + Tailscale serve
[board] → T-003 in_review — dispatch/triage reviews: Hooks + .claude/settings.json (stop-guard, teammate-idle, board-validate, git-guard, reviewer-write-guard)
[board] → T-004 in_review — dispatch/triage reviews: Agent definitions: 8 workers + 13 reviewer personas (provisional)
[board] → T-005 in_review — dispatch/triage reviews: CLAUDE.md map, memory seeds, RUNBOOK, ENVIRONMENT
T-001	M0	orchestrator	in_review        	P0	AC 4/4	Board CLI (tools/board.py): cards, transitions, claims, reviews, gates, status
T-002	M0	orchestrator	in_review        	P0	AC 4/4	Board web UI (tools/board_server.py) + Tailscale serve
T-003	M0	orchestrator	in_review        	P0	AC 3/3	Hooks + .claude/settings.json (stop-guard, teammate-idle, board-validate, git-guard, reviewer-write-guard)
T-004	M0	orchestrator	in_review        	P0	AC 3/3	Agent definitions: 8 workers + 13 reviewer personas (provisional)
T-005	M0	orchestrator	in_review        	P1	AC 3/3	CLAUDE.md map, memory seeds, RUNBOOK, ENVIRONMENT
T-006	M0	orchestrator	in_review        	P0	AC 3/3	Secrets scanner + git hygiene (check_secrets.py, .gitignore, conventional commits, tag m0)
T-007	M0	orchestrator	in_progress      	P0	AC 0/3	M0 smoke test (§4.8) + heartbeat + Playwright screenshot of board
ls: Makefile: No such file or directory
ls: run.sh: No such file or directory
zlayt: 2 windows (created Sun Nov  1 17:49:29 2026)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:44.493Z

**tool call — Bash**
````
{
 "command": "for p in docs/CONTRACT.md spec/SPEC.md spec/REQUIREMENTS.md spec/SAMPLE_CASE_TRUTHS.md docs/LLM_VS_CODE.md board/milestones.md board/activity.jsonl board/inbox personas research app app/backend evals tests artifacts submission tools/export_prompt_log.py tools/compile_agents.py tools/check_secrets.py app/README-arch.md tools/install_test.sh .claude/agents .claude/hooks reviews; do [ -e $p ] && echo \"OK   $p\" || echo \"MISS $p\"; done; grep -n \"check_secrets\\|staged\" tools/check_secrets.py | head -5; ls .claude/hooks; grep -n \"lesson\\|inbox\\|gate\\|milestone\" tools/board.py | grep -i \"add_parser\\|subparsers\\|sub.add\" | head",
 "description": "Spot-check paths named in CLAUDE.md"
}
````

### User / tool · 2026-11-02T00:16:44.594Z

**tool result**
````
OK   docs/CONTRACT.md
OK   spec/SPEC.md
MISS spec/REQUIREMENTS.md
OK   spec/SAMPLE_CASE_TRUTHS.md
MISS docs/LLM_VS_CODE.md
OK   board/milestones.md
OK   board/activity.jsonl
OK   board/inbox
OK   personas
OK   research
OK   app
OK   app/backend
OK   evals
OK   tests
OK   artifacts
OK   submission
MISS tools/export_prompt_log.py
OK   tools/compile_agents.py
OK   tools/check_secrets.py
MISS app/README-arch.md
MISS tools/install_test.sh
OK   .claude/agents
OK   .claude/hooks
OK   reviews
2:"""Secret scanner. `--staged` checks files staged for commit (used by git-guard pre-commit); default scans tracked files.
16:ALLOW_FILES = {"tools/check_secrets.py", "tools/tests/test_secrets.py", ".claude/hooks/git_guard.py"}
24:    staged = "--staged" in argv
25:    files = git("diff", "--cached", "--name-only", "--diff-filter=ACM").split() if staged else git("ls-files").split()
34:        text = git("show", f":{f}") if staged else (ROOT / f).read_text(errors="ignore") if (ROOT / f).is_file() else ""
_common.py
board-validate.sh
board_validate.py
git-guard.sh
git_guard.py
reviewer-write-guard.sh
reviewer_write_guard.py
stop-guard.sh
stop_guard.py
teammate-idle.sh
teammate_idle.py
1019:    s = sub.add_parser("milestone"); s.add_argument("action", choices=["set"]); s.add_argument("id", choices=MILESTONE_IDS)
1023:    s = sub.add_parser("gate"); s.add_argument("id", choices=MILESTONE_IDS); s.add_argument("--record", required=True)
1027:    s = sub.add_parser("lesson"); s.add_argument("--agent", required=True); s.add_argument("--text", required=True)
1030:    s = sub.add_parser("inbox"); s.add_argument("--ack", action="store_true"); s.add_argument("--agent", default="orchestrator")
1038:    s = sub.add_parser("list"); s.add_argument("--status"); s.add_argument("--milestone"); s.add_argument("--role")
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:48.423Z

**tool call — Bash**
````
{
 "command": "sed -n 990,1045p tools/board.py; python3 tools/board.py inbox 2>&1 | head -5",
 "description": "Verify CLI cheat sheet against argparse"
}
````

### User / tool · 2026-11-02T00:16:48.557Z

**tool result**
````
    s.add_argument("--text", required=True); s.set_defaults(fn=cmd_note)

    s = sub.add_parser("handoff"); s.add_argument("id"); s.add_argument("--agent", required=True)
    s.add_argument("--text"); s.add_argument("--file"); s.set_defaults(fn=cmd_handoff)

    s = sub.add_parser("ac"); s.add_argument("id"); s.add_argument("--agent", required=True)
    s.add_argument("--check", type=int); s.add_argument("--uncheck", type=int); s.add_argument("--evidence")
    s.add_argument("--add"); s.add_argument("--edit", type=int); s.add_argument("--text"); s.set_defaults(fn=cmd_ac)

    s = sub.add_parser("review"); s.add_argument("id"); s.add_argument("--persona", required=True)
    s.add_argument("--model", required=True); s.add_argument("--verdict", required=True, choices=VERDICTS)
    s.add_argument("--file", required=True); s.add_argument("--agent", default="orchestrator"); s.set_defaults(fn=cmd_review)

    s = sub.add_parser("commit"); s.add_argument("id"); s.add_argument("--sha", required=True)
    s.add_argument("--agent", required=True); s.set_defaults(fn=cmd_commit)

    s = sub.add_parser("update"); s.add_argument("id"); s.add_argument("--agent", required=True)
    s.add_argument("--title"); s.add_argument("--priority", choices=PRIORITIES); s.add_argument("--role", choices=ROLES)
    s.add_argument("--milestone", choices=MILESTONE_IDS); s.add_argument("--depends", nargs="*")
    s.add_argument("--append-body"); s.set_defaults(fn=cmd_update)

    s = sub.add_parser("next"); s.add_argument("--role", required=True, choices=ROLES)
    s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_next)

    s = sub.add_parser("status"); s.add_argument("--json", action="store_true"); s.add_argument("--brief", action="store_true")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("validate"); s.add_argument("path", nargs="?"); s.set_defaults(fn=cmd_validate)

    s = sub.add_parser("milestone"); s.add_argument("action", choices=["set"]); s.add_argument("id", choices=MILESTONE_IDS)
    s.add_argument("--status", required=True); s.add_argument("--note"); s.add_argument("--agent", default="orchestrator")
    s.set_defaults(fn=cmd_milestone)

    s = sub.add_parser("gate"); s.add_argument("id", choices=MILESTONE_IDS); s.add_argument("--record", required=True)
    s.add_argument("--result", required=True, choices=["pass", "fail"]); s.add_argument("--agent", default="orchestrator")
    s.set_defaults(fn=cmd_gate)

    s = sub.add_parser("lesson"); s.add_argument("--agent", required=True); s.add_argument("--text", required=True)
    s.add_argument("--card"); s.set_defaults(fn=cmd_lesson)

    s = sub.add_parser("inbox"); s.add_argument("--ack", action="store_true"); s.add_argument("--agent", default="orchestrator")
    s.set_defaults(fn=cmd_inbox)

    s = sub.add_parser("log"); s.add_argument("--event", required=True); s.add_argument("--agent", required=True)
    s.add_argument("--card"); s.add_argument("--text", default=""); s.set_defaults(fn=cmd_log)

    s = sub.add_parser("show"); s.add_argument("id"); s.set_defaults(fn=cmd_show)

    s = sub.add_parser("list"); s.add_argument("--status"); s.add_argument("--milestone"); s.add_argument("--role")
    s.set_defaults(fn=cmd_list)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
inbox empty
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:16:51.071Z

**tool call — Bash**
````
{
 "command": "sed -n 970,990p tools/board.py; grep -n \"new\\b\\|board.py new\" CLAUDE.md; grep -n -i \"needs_chris\" tools/board.py | head; grep -rn \"teammate\\|heartbeat\" docs/RUNBOOK.md memory/STATE.md",
 "description": "Check new-card command and needs_chris support"
}
````

### User / tool · 2026-11-02T00:16:51.172Z

**tool result**
````
    p = argparse.ArgumentParser(prog="board.py", description="Zlayt PM project board CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("--agent", default="orchestrator"); s.set_defaults(fn=cmd_init)

    s = sub.add_parser("new")
    s.add_argument("--title", required=True); s.add_argument("--milestone", required=True, choices=MILESTONE_IDS)
    s.add_argument("--role", required=True, choices=ROLES); s.add_argument("--priority", default="P1", choices=PRIORITIES)
    s.add_argument("--depends", nargs="*"); s.add_argument("--ac", action="append")
    s.add_argument("--by", default="orchestrator"); s.add_argument("--body-file"); s.add_argument("--body")
    s.add_argument("--status", default="ready", choices=["backlog", "ready", "needs_chris", "blocked"])
    s.set_defaults(fn=cmd_new)

    s = sub.add_parser("claim"); s.add_argument("id"); s.add_argument("--agent", required=True)
    s.add_argument("--force", action="store_true"); s.set_defaults(fn=cmd_claim)

    s = sub.add_parser("move"); s.add_argument("id"); s.add_argument("status")
    s.add_argument("--agent", required=True); s.add_argument("--note"); s.set_defaults(fn=cmd_move)

    s = sub.add_parser("note"); s.add_argument("id"); s.add_argument("--agent", required=True)
    s.add_argument("--text", required=True); s.set_defaults(fn=cmd_note)
38:            "done", "blocked", "needs_chris", "cancelled"]
49:    "backlog": {"ready", "cancelled", "needs_chris", "blocked"},
50:    "ready": {"in_progress", "backlog", "blocked", "cancelled", "needs_chris"},
51:    "in_progress": {"in_review", "blocked", "ready", "needs_chris", "cancelled"},
53:    "changes_requested": {"in_progress", "needs_chris", "cancelled", "blocked"},
54:    "blocked": {"ready", "in_progress", "cancelled", "needs_chris"},
55:    "needs_chris": {"ready", "in_progress", "cancelled", "done"},
380:                       "submission/NEEDS_CHRIS.md", "submission/prompt-log/TOOLS.md",
406:    open_cards = [m["id"] for m, _ in cards if m["status"] not in ("done", "cancelled", "needs_chris")]
425:        if st not in ("cancelled", "needs_chris"):
docs/RUNBOOK.md:26:   > Re-read memory/STATE.md and board status, re-spawn the worker teammates, recreate the heartbeat, continue.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:17:00.690Z

**tool call — Bash**
````
{
 "command": "python3 -c \"import json;d=json.load(open('.claude/settings.json'));print(json.dumps({k:v for k,v in d.items() if k!='hooks'},indent=1))\"; sed -n 1,60p .claude/hooks/stop_guard.py | grep -n -i \"stop\" | head",
 "description": "Check permissions mode and stop guard"
}
````

### User / tool · 2026-11-02T00:17:00.807Z

**tool result**
````
{
 "env": {
  "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
  "CLAUDE_CODE_FORK_SUBAGENT": "0",
  "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "2",
  "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS": "12"
 },
 "teammateMode": "in-process",
 "autoContinueAtUsageLimit": true,
 "permissions": {
  "deny": [
   "Bash(git push --force*)",
   "Bash(git push -f*)",
   "Bash(git reset --hard*)",
   "Bash(git checkout -- .)",
   "Bash(git clean -fd*)",
   "Bash(rm -rf /*)",
   "Bash(rm -rf ~*)",
   "Bash(git add -A*)",
   "Bash(git add --all*)",
   "Bash(git add .)"
  ]
 }
}
2:"""Stop hook (§4.3): keep the orchestrator looping while actionable work exists, with a stall guard."""
6:STATE = ROOT / "board" / ".stop_guard_state"
14:    if (ROOT / "board" / "STOP").exists():
38:            "# ALERT: orchestrator stalled\n\nBoard unchanged across 5 consecutive Stop-hook blocks. Last reason:\n\n" + reason + "\n")
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:17:17.181Z

**tool call — Bash**
````
{
 "command": "sed -n 78,92p tools/board_ui.html | cut -c1-220; curl -s http://localhost:7777/api/state 2>/dev/null | head -c 300; echo; grep -n \"def do_GET\" -A15 tools/board_server.py | grep path | head",
 "description": "Check STOP UI location and API routes"
}
````

### User / tool · 2026-11-02T00:17:17.289Z

**tool result**
````
    <ul class="feed panel" id="feed"></ul>
  </section>
  <section id="v-inbox" class="hide">
    <div class="panel">
      <b>Send a note to the orchestrator</b>
      <p class="muted">Written to <code>board/inbox/</code>; read every cycle. Use it to steer, reprioritize or answer a needs_chris item.</p>
      <textarea id="note" rows="5" style="width:100%" placeholder="e.g. Prioritize the export format over the stretch item."></textarea>
      <div style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap"><button class="act" id="send">Send note</button><span id="sent" class="muted"></span></div>
    </div>
    <div class="panel"><b>Stop the run</b><p class="muted">Creates <code>board/STOP</code>; the orchestrator finishes its current handoff and stops.</p>
      <button class="act danger" id="stop">STOP</button></div>
    <div class="panel"><b>Unread</b><div id="unread" class="md"></div><b>Recently acknowledged</b><div id="archived" class="md"></div></div>
  </section>
  <section id="v-state" class="hide">
    <div class="filters"><select id="f-file">
{"error": "not found"}
194-        u = urlparse(self.path)
197-            if u.path in ("/", "/index.html"):
199-            if u.path == "/api/status":
201-            if u.path == "/api/cards":
203-            if u.path == "/api/agents":
205-            if u.path == "/api/activity":
207-            if u.path == "/api/milestones":
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:17:42.442Z

**tool call — Bash**
````
{
 "command": "grep -n \"Board (tailnet)\\|App (local)\" docs/RUNBOOK.md; grep -n \"spec/REQUIREMENTS\" CLAUDE.md; python3 tools/board.py validate --help 2>&1 | head -3; ls reviews",
 "description": "Confirm line refs before writing review"
}
````

### User / tool · 2026-11-02T00:17:42.592Z

**tool result**
````
6:| Board (tailnet) | https://<redacted-private>:7777 | open on your phone (Tailscale on). Kanban, personas, milestones, activity, inbox, STOP. |
9:| App (local) | http://localhost:7860 | `make run` |
7:Full contract: `docs/CONTRACT.md` (never edited). Spec: `spec/SPEC.md`, `spec/REQUIREMENTS.md`, `spec/SAMPLE_CASE_TRUTHS.md`.
usage: board.py validate [-h] [path]

positional arguments:
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:18:35.206Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-005-product-manager.md",
 "content": "# T-005 review — product-manager-reviewer\n\n**Verdict: fail** (1 blocker, 3 majors, 3 minors).\n\nCLAUDE.md is a tight, complete-in-shape map (81 lines, every §4.7 section present), and the board's tailnet URL works from Chris's phone path.\nThe card fails because a Chris action that the team itself recorded (\"restart the session once\") never reached\n`submission/NEEDS_CHRIS.md`, and no item there has the `needs_chris` card that non-negotiable 1 requires. Majors: the restart\nprotocol would not actually resume an autonomous run today; the map points fresh agents at five paths that don't exist (unmarked) and leaves out\nthe one tool that makes reviewers spawnable in this host; and the decision/assumption logs record *what* but not *why / what if wrong*,\nwhich is exactly what Zlayt says it grades (\"decisions made under ambiguity, explained plainly\").\n\nExercised: `wc -l CLAUDE.md` (81); existence check of 23 paths named in CLAUDE.md; CLI cheat sheet checked against `tools/board.py` argparse;\n`curl` of all 4 RUNBOOK URLs + tailnet root; `tailscale serve status`; read `tools/serve_board.sh`, the STOP endpoint in\n`tools/board_server.py:243-247` and the UI panel in `tools/board_ui.html:87-88` (STOP not clicked — side effect); `.claude/settings.json`\npermissions; `board.py status --brief`, `list`, `list --status needs_chris`, `inbox`; read every memory file, RUNBOOK, NEEDS_CHRIS, and\nCONTRACT §1, §4.5–4.8, §9, §10, §11, Appendix A.\n\n```json\n{\"card\": \"T-005\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"CLAUDE.md, memory/*.md, memory/contracts/api.md, docs/RUNBOOK.md, memory/ENVIRONMENT.md, submission/NEEDS_CHRIS.md (working tree 2026-11-02); board http://localhost:7777 and https://<redacted-private>:7777; no sample case (M0)\",\n \"exercised\": [\n  \"wc -l CLAUDE.md -> 81 (AC1 under 120: met)\",\n  \"existence check of 23 paths named in CLAUDE.md: 5 missing (spec/REQUIREMENTS.md, docs/LLM_VS_CODE.md, tools/export_prompt_log.py, app/README-arch.md, tools/install_test.sh)\",\n  \"CLI cheat sheet vs tools/board.py build_parser(): all listed verbs/flags valid; `new` absent from sheet\",\n  \"curl http://localhost:7777 -> 200; https://<redacted-private>:7777 -> 200; localhost:7860 and tailnet :7860 -> 000 (app not built; RUNBOOK says live once M3)\",\n  \"tailscale serve status: :7777 -> 127.0.0.1:7777 present; 443 -> 4173 and 8443/10000 -> 8787 present (root returns 502, nothing on 4173)\",\n  \"read tools/serve_board.sh, board_server.py /api/stop, board_ui.html STOP panel (in Inbox tab, typed-confirm) — did not trigger STOP\",\n  \".claude/settings.json: no permissions.defaultMode\",\n  \"board.py status --brief (needs_chris=0), list, list --status needs_chris (empty), inbox (empty)\",\n  \"read memory/STATE, PROGRESS, DECISIONS, ASSUMPTIONS, SCOPE_CUTS, LESSONS, GLOSSARY, ENVIRONMENT, contracts/api.md; docs/RUNBOOK.md; submission/NEEDS_CHRIS.md\",\n  \"read docs/CONTRACT.md §1, §4.1, §4.5-4.8, §9, §10, §11, Appendix A 'What we evaluate'\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"map_completeness_for_fresh_agent\": 3, \"runbook_operable_by_chris\": 3, \"restart_readiness\": 2, \"needs_chris_quality\": 2, \"decisions_under_ambiguity_legibility\": 2},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"A Chris action the team recorded is missing from NEEDS_CHRIS, and no NEEDS_CHRIS item has a needs_chris card\",\n   \"evidence\": \"memory/LESSONS.md:8 'NEEDS_CHRIS: restart the session once to load native definitions.' — submission/NEEDS_CHRIS.md has exactly one row (API key, line 7), no restart item. `board.py status --brief` -> needs_chris=0; `board.py list --status needs_chris` -> empty. CONTRACT §1.1: 'write it to submission/NEEDS_CHRIS.md, create a card in the needs_chris lane, state your assumption'. CONTRACT §4.8.4 names this exact item: 'note it in NEEDS_CHRIS: \\\"restart the session once\\\"'.\",\n   \"why_it_matters\": \"NEEDS_CHRIS is Chris's only to-do list and the board column is what he watches on his phone. Until he restarts, native agent definitions don't load and the reviewer write-guard hook is not attached (LESSONS.md:8) — a supervision gap the harness is supposed to close. A recorded fact was lost between files, and the contract's two-part rule (file + card) is half-met.\",\n   \"fix\": \"Add row 2 to NEEDS_CHRIS.md: P0/P1, 'Restart the Claude session once so .claude/agents/* load natively', exact action (see restart finding for the correct command), where the answer goes (inbox note 'restarted'), assumption meanwhile (general-purpose subagents via tools/agent_prompt.py; write-guard is instruction-only). Create a needs_chris card for each NEEDS_CHRIS row (`board.py new --status needs_chris ...`) and cross-reference the card id in the table.\",\n   \"acceptance_test\": \"`board.py list --status needs_chris` lists one card per NEEDS_CHRIS row; `grep -n -i restart submission/NEEDS_CHRIS.md` hits; every row has non-empty Exact action and Assumption cells.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Restart protocol would not resume the autonomous run as written\",\n   \"evidence\": \"docs/RUNBOOK.md:24-26: `./tools/serve_board.sh` and `claude --continue` with no `cd /Users/arsis/zlayt-pm-project` (both are cwd-relative; --continue picks the latest conversation in cwd). No `--dangerously-skip-permissions` flag, and .claude/settings.json has no permissions.defaultMode -> a CLI resume runs in default permission mode and will stop on prompts nobody answers (CONTRACT §0 assumes the session runs with that flag). memory/STATE.md is 3 lines (only 'Active milestone: M0'); CONTRACT §4.5 requires in-flight work, next three actions, open risks, URLs, and 'STATE.md + board.py status must be enough to resume'. The resume prompt says 're-spawn the worker teammates' but nothing a resumed agent reads (CLAUDE.md, STATE.md, RUNBOOK) mentions the tools/agent_prompt.py fallback needed when definitions don't load (LESSONS.md:8, DECISIONS.md:10). 'Recreate the heartbeat' gives no schedule/text; the §9 heartbeat spec is only in CONTRACT.\",\n   \"why_it_matters\": \"Chris has no technical help during the run; RUNBOOK's restart section is the one thing he must execute correctly from memory. As written, a reboot leaves him with a session that either stalls on permission prompts or resumes with no recorded in-flight state.\",\n   \"fix\": \"RUNBOOK restart: prefix `cd /Users/arsis/zlayt-pm-project`; give the exact CLI line including `--dangerously-skip-permissions` (or state that the Desktop 'reopen session' path is the supported one and how its permission mode is set); add 'if Agent type not found: use tools/agent_prompt.py fallback' and the heartbeat text, or point to a STATE.md section that holds them. Rewrite STATE.md to the §4.5 shape now (milestone, in-flight cards, next 3 actions, open risks incl. un-restarted session, URLs).\",\n   \"acceptance_test\": \"A fresh agent given only CLAUDE.md + STATE.md + `board.py status` can name the in-review cards, the next 3 actions, the agent-spawn fallback and the heartbeat command without opening CONTRACT.md; RUNBOOK restart commands run verbatim from a new terminal in $HOME.\"},\n  {\"severity\": \"major\",\n   \"title\": \"CLAUDE.md map names 5 non-existent paths as if present and omits tools a fresh agent needs\",\n   \"evidence\": \"CLAUDE.md:7 lists `spec/REQUIREMENTS.md` alongside SPEC.md as current spec — missing. CLAUDE.md:41 `docs/LLM_VS_CODE.md`, :49 `tools/export_prompt_log.py`, :54 `app/README-arch.md`, :58 `tools/install_test.sh` — all missing, none marked 'created in Mx'. CLAUDE.md:49 tools row omits tools/agent_prompt.py (the only working way to spawn personas in this host), tools/serve_board.sh, tools/screenshot_board.py. Cheat sheet CLAUDE.md:24-30 omits `board.py new` (card creation, incl. `--status needs_chris`) — the verb non-negotiable 1 depends on.\",\n   \"why_it_matters\": \"§4.7 makes CLAUDE.md the map a fresh/compacted agent relies on. An agent told the spec includes REQUIREMENTS.md will either search for it or invent its absence; an orchestrator after compaction can't create a needs_chris card or spawn a reviewer from the map alone.\",\n   \"fix\": \"Mark future paths '(created in M1)' etc.; add agent_prompt.py, serve_board.sh to the tools row; add `$B new --title .. --milestone Mx --role r [--status needs_chris] --ac ..` to the cheat sheet. Stays under 120 lines.\",\n   \"acceptance_test\": \"Script: every backticked path in CLAUDE.md either exists or carries a '(created in Mx)' marker; `grep -c 'board.py new\\\\|\\\\$B new' CLAUDE.md` >= 1; `grep agent_prompt CLAUDE.md` hits; `wc -l` < 120.\"},\n  {\"severity\": \"major\",\n   \"title\": \"ASSUMPTIONS/DECISIONS formats record conclusions, not reasoning under ambiguity\",\n   \"evidence\": \"memory/ASSUMPTIONS.md:10-12 are bare assertions, e.g. A-102 'A \\\"treatment gap\\\" is measured between consecutive dates of service across all providers, not per provider.' — no basis, confidence, impact-if-wrong, or how/who validates. memory/DECISIONS.md:3 declares 'Status · Context · Decision · Consequences · Alternatives considered' but ADR-000 (:5-10) bundles four decisions as bullets with none of Context/Consequences/Alternatives. The plainest decision under ambiguity so far — moving board/app off the contract's 443/8443 to 7777/7860 because Chris's tailnet already used them (RUNBOOK.md:11-12, LESSONS.md:7) — is not in DECISIONS at all.\",\n   \"why_it_matters\": \"Appendix A grades 'Self-direction and clarity: decisions made under ambiguity, explained plainly' and §1.12 says 'Zlayt grades these explicitly'. A hiring panel reading A-102 can't tell whether it was researched, guessed, or how the product behaves if it's wrong (gap logic is in the eval golden set). Seeding a weak format now means every later entry inherits it.\",\n   \"fix\": \"ASSUMPTIONS columns/fields: ID · assumption · why we believe it (source or 'unverified guess') · confidence · if wrong, what changes in the product · how we'd validate (who to ask). Split ADR-000 into ADR-000a..d in the declared format; add an ADR for the port deviation from §10. (Architect owns DECISIONS — orchestrator should card it.)\",\n   \"acceptance_test\": \"Every ASSUMPTIONS entry has non-empty basis, confidence, impact-if-wrong and validation fields; every ADR has all five declared headings; `grep -n 7777 memory/DECISIONS.md` hits.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"STOP is one-tap from the phone but resume is not documented for the phone\",\n   \"evidence\": \"docs/RUNBOOK.md:21 'To resume, delete board/STOP and continue the session.' tools/board_server.py exposes only POST /api/stop (line 243); there is no un-stop endpoint or UI control.\",\n   \"why_it_matters\": \"RUNBOOK is written for Chris on his phone (RUNBOOK.md:6). After an accidental STOP he needs a Mac terminal to undo it, which the doc doesn't say; the Remote Control path ('tell the orchestrator: remove board/STOP and continue') would work but isn't listed.\",\n   \"fix\": \"Add the phone resume path (type into the Remote Control session) and the Mac path with full path `rm /Users/arsis/zlayt-pm-project/board/STOP`.\",\n   \"acceptance_test\": \"RUNBOOK Stop section lists a resume step that works with only the phone.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Handoff claims 'RUNBOOK URLs curl-verified'; half of them can't be\",\n   \"evidence\": \"curl localhost:7860 and tailnet :7860 -> 000. RUNBOOK.md:9 App (local) row says '`make run`' with no 'from M3' marker; Makefile does not exist.\",\n   \"why_it_matters\": \"Chris will tap/try every row; an unmarked dead row reads as broken. Also the handoff over-claims verification.\",\n   \"fix\": \"Mark both app rows 'not live until M3; `make run` added by release in M4' and state in the handoff that only board URLs were verified.\",\n   \"acceptance_test\": \"Every RUNBOOK URL row either curls 200 or carries an explicit 'live from Mx' note.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"SCOPE_CUTS and STATE seeds give no worked example of the expected entry\",\n   \"evidence\": \"memory/SCOPE_CUTS.md:3-4 header only; memory/STATE.md:1-3.\",\n   \"why_it_matters\": \"Workers propose cuts via card notes and the orchestrator transcribes; an example row (e.g. the deferred native-agent-definition load, or contract port change) anchors the quality bar for the hiring panel.\",\n   \"fix\": \"Add one real row (anything already cut in M0) to SCOPE_CUTS.\",\n   \"acceptance_test\": \"SCOPE_CUTS has >= 1 row with all five columns filled.\"}\n ],\n \"whats_right\": [\n  \"CLAUDE.md is 81 lines and has every §4.7 section (mission, 12 rules, CLI, map, ownership, report, review protocol, data, LLM/code) — keep it this tight.\",\n  \"Board tailnet URL returns 200 and RUNBOOK.md:11-12 explains the port deviation in plain words Chris will understand.\",\n  \"NEEDS_CHRIS table columns (exact action · where the answer goes · assumption meanwhile) are exactly the right shape; SCOPE_CUTS columns (cut · why · cost to add) likewise.\"\n ],\n \"questions_for_chris\": [\n  \"memory/ENVIRONMENT.md:13 records your tailnet IP, MagicDNS name and phone device name, and RUNBOOK has the <redacted-private> hostname; if this repo is shared with Zlayt, do you want those redacted? (privacy is outside my lens; flagging only)\",\n  \"Your pre-existing tailnet mapping 443 -> 127.0.0.1:4173 currently returns 502 (nothing listening). Was that service running before this session? LESSONS.md:7 says the team overwrote and then restored the mapping.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T00:18:35.326Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-005-product-manager.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:18:36.550Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-005-product-manager.md",
 "description": "Validate the review file"
}
````

### User / tool · 2026-11-02T00:18:36.668Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:18:50.023Z

**Verdict: fail.** There is 1 blocker, 3 majors and 3 minors. The review is at `/Users/arsis/zlayt-pm-project/reviews/T-005-product-manager.md` and `board.py validate` returned "ok".

**What I ran:** I counted CLAUDE.md lines (81, so AC1 is met) and checked whether 23 paths it names exist. I compared the CLI cheat sheet with board.py's argument parser. I curled the 4 RUNBOOK URLs and ran `tailscale serve status`. I read `serve_board.sh` and the STOP endpoint and panel, but did not press STOP. I checked the permissions in `.claude/settings.json`, ran `board.py status`, `list` and `inbox`, and read every memory file, the RUNBOOK, NEEDS_CHRIS and the named contract sections.

**Blocker**
- **A known item for Chris is missing from NEEDS_CHRIS, and no card exists in the `needs_chris` lane.** LESSONS.md:8 says "NEEDS_CHRIS: restart the session once to load native definitions." The contract's §4.8.4 names that exact item. `submission/NEEDS_CHRIS.md` has only the API-key row. `board.py` shows `needs_chris=0` and the lane is empty. Non-negotiable §1.1 needs both the file entry and a card, so it is half met. Until Chris restarts, the reviewer write-guard hook isn't attached.

**Majors**
1. **The restart steps would not resume the run as written.**
   - RUNBOOK.md:24-26 runs `./tools/serve_board.sh` and `claude --continue` without `cd`-ing into the project first.
   - The resume command has no `--dangerously-skip-permissions`, and settings.json sets no default permission mode. A CLI resume would most likely stop on permission prompts nobody is there to answer.
   - STATE.md is 3 lines. §4.5 asks for in-flight work, the next 3 actions, risks and URLs.
   - Nothing a resumed agent reads mentions the `tools/agent_prompt.py` fallback for spawning agents, or the text for the heartbeat task.
2. **CLAUDE.md names 5 paths that don't exist, with no "created later" note.** They are `spec/REQUIREMENTS.md` (line 7, listed as part of the spec), `docs/LLM_VS_CODE.md`, `tools/export_prompt_log.py`, `app/README-arch.md` and `tools/install_test.sh`.
   - It leaves out `tools/agent_prompt.py`, the only way reviewers can be spawned in this host, and `tools/serve_board.sh`.
   - The cheat sheet has no `board.py new`. A fresh agent therefore can't see how to create the `needs_chris` card that rule 1 requires.
3. **ASSUMPTIONS and DECISIONS record conclusions but not the reasoning.**
   - Entries like A-102 (how a treatment gap is measured) give no basis, confidence, effect if wrong, or way to check.
   - ADR-000 lumps four decisions into bullets and skips the Context, Consequences and Alternatives sections the file itself declares.
   - Moving the board and app off the contract's 443/8443 ports is not in DECISIONS at all.
   - This is the "decisions made under ambiguity, explained plainly" row that Zlayt grades.

**Minors**
- STOP works from the phone, but resuming means deleting `board/STOP` on the Mac, and the RUNBOOK gives no phone route.
- The handoff says the RUNBOOK URLs were curl-verified, but both app URLs fail (curl status 000). The local app row says `make run`, there is no Makefile, and the row isn't marked as not live yet.
- SCOPE_CUTS has a header but no example row.

**What's right:** CLAUDE.md is tight and has every section §4.7 asks for. The board's tailnet URL returns 200, and the RUNBOOK explains the port change plainly. The NEEDS_CHRIS and SCOPE_CUTS column layouts are the right shape.

**Questions for Chris** (also in the review):
- Should the tailnet IP and device names in ENVIRONMENT.md be redacted if the repo goes to Zlayt?
- His existing 443 → 4173 tailnet mapping currently returns 502. Was that service running before this session?

I didn't record any recurring patterns in reviewer memory, because I can only write under `reviews/` and `artifacts/review-evidence/`.
