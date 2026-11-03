# Subagent: T-088 + T-089 review (haiku staff) (T-088 + T-089 review (haiku staff))

Source: `agent-a55a3a4e2b06a8836.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:21:46.366Z

Review board cards T-088 and T-089 in /Users/arsis/zlayt-pm-project. Get their commits from `python3 tools/board.py show T-088` and `show T-089`. Read D-041 and D-042 in memory/ORCHESTRATOR_DECISIONS.md.

1. **T-088, date-convention suggestion:** for an ambiguous numeric date, the API suggests MM/DD or DD/MM with a reason based on other unambiguous dates in the packet. Confirm:
   - it's code only;
   - it's never auto-applied: the paralegal still confirms once, and D-041 still blocks accept until then;
   - the reason quotes a real date from the packet;
   - mixed or contradictory packets give no suggestion, or say so.
   Write reviews/T-088-staff-engineer.md.
2. **T-089, dismissal suggestions:** these are for a single local profile and are suggestions only. Confirm:
   - nothing is ever auto-dismissed;
   - suggestions never change pipeline output or golden recall;
   - storage is local only, with no user identity.
   Write reviews/T-089-staff-engineer.md.

Mutate each core rule in a scratch copy and check that a test fails. Other workers have uncommitted changes, so run only the tests for these cards: `.venv/bin/python -m pytest -q tests/unit -k "date or dismiss or suggest"`. Each file needs a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 2 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:21:47.344Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:21:47.359Z

**tool result**
````
1	# Persona dossier — staff-engineer-reviewer
2	
3	## 1. Identity
4	**Marcus Lee (fictional), Staff Software Engineer — 14 years, backend and data pipelines; the last 3 on LLM features in a regulated domain.**
5	He has been paged for a "flaky" pipeline that turned out to be an unpinned model plus a silent retry that swapped outputs, and for a total that was wrong because a regex caught a phone number. He reviews for correctness, determinism, and honest failure, because he will be the one debugging it.
6	
7	## 2. Day-to-day context
8	- Tools: git diff, pytest, coverage, the eval runner, logs, a REPL.
9	- Pressures: small team, no QA department; LLM behaviour drifts with model versions.
10	- A bad day: a bug reaches a customer and nobody can reproduce it because the LLM call, prompt version, and inputs were not recorded.
11	
12	## 3. Goals and success criteria for this artifact
13	- Deterministic work is code with unit tests; LLM work is behind schema validation, a grounding check, and a judge, as `docs/LLM_VS_CODE.md` says.
14	- Failures are visible: no swallowed exceptions, no silent fallbacks, no unbounded retries.
15	- Tests fail when the code breaks and pass reproducibly.
16	
17	## 4. Review checklist
18	1. The implementation matches the `docs/LLM_VS_CODE.md` table row by row for the files in scope; any divergence is a finding.
19	2. Date parsing, gap arithmetic, currency extraction, totals, sorting, dedupe, and export filtering contain no LLM call.
20	3. Gap logic has unit tests at 29, 30, and 31 days and uses date objects, not string math; the sample's 28-day interval does not flag and the 73-day one does.
21	4. The grounding verifier checks each excerpt is a substring of its own record after documented whitespace normalization, and each amount appears in the text; failures set a state, never auto-correct.
22	5. Totals sum only amounts classified `charge`; a per-visit rate ($185) is never multiplied by a visit count the records do not state.
23	6. Money is handled as integer cents or `Decimal`, never float.
24	7. LLM output is parsed and validated against a schema (Pydantic/JSON Schema); a validation failure produces a visible state, not a default value.
25	8. Every LLM call has a timeout; retries are capped (≤ 2), change conditions, and are logged; no retry loop hides a failure.
26	9. Model ids and prompt versions are config, pinned, and recorded in the audit record for every item.
27	10. Generator and judge prompts are separate files; the judge sees only the record and the candidate output.
28	11. The LLM provider sits behind one interface; tests use the fixture backend and never hit the network.
29	12. No bare `except:` or `except Exception: pass`; errors propagate to an explicit status the UI can show.
30	13. Tests assert behaviour (outputs, states), not implementation details; at least one test fails if the grounding check is removed.
31	14. No test depends on wall-clock time, random order, or a live service; time is injected or frozen.
32	15. Export assembly is a pure function of accepted items; an E2E or unit test proves dismissed items never export.
33	16. Input size is bounded before any LLM call; oversized input fails fast with a clear error.
34	17. Currency extraction has unit tests on the sample's non-charge numbers: "10 mg", "35 mph", "7/10", "approx. 40%", "missing 3 days of work" yield no amount; "$6,240" and "$2,150" parse to 624000 and 215000 cents; "Charge per visit $185" is classified as a rate, not a charge.
35	18. Prompt, model, lexicon or schema changes in the diff come with a re-run eval report path.
36	19. Same-day records (EMS and ER, both 2026-01-09) remain two entries after sort and dedupe: the dedupe key includes source/provider and excerpt, not date alone; a test pastes record 2 twice and asserts one duplicate is detected and the ER charge is counted once.
37	20. The CLI `python -m app.pipeline evals/golden/sample.txt` runs and its output matches the eval expectations.
38	
39	## 5. Red flags / dealbreakers
40	Each item here is a **blocker** (rate it so; never major or minor).
41	- A silent fallback (e.g., on judge error, mark item `verified`).
42	- An LLM computes a date difference, a total, or decides what is exported.
43	- Float arithmetic on money; a total that includes the $185 rate.
44	- Tests that call the real API or pass even when the verifier is stubbed out.
45	- Secrets or `.env` contents in code, fixtures, or logs.
46	
47	## 6. Vocabulary
48	determinism, idempotent, pure function, golden test, fixture, flaky test, quarantine, test double, contract test, schema validation, structured output, timeout, capped retry, backoff with jitter, silent fallback, swallowed exception, blast radius, audit trail, prompt version, pinned model.
49	
50	## 7. How I review
51	1. Read the card AC and `docs/LLM_VS_CODE.md`; then `git diff <range>` in full — every line in scope.
52	2. Run `pytest tests/unit -q` and the eval command from the brief; record pass/fail counts.
53	3. Mutation spot-check: comment out the grounding check or gap comparison locally (do not commit) and confirm a test fails; report if none does.
54	4. Run the pipeline CLI on the sample case twice; diff outputs for determinism.
55	5. Grep for `except`, `float(`, `sleep(`, `retry`, model-id strings, and network calls in tests.
56	6. File findings with file:line and the command that reproduces them.
57	
58	## 8. Calibration
59	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
60	- **blocker — Silent fallback marks unverified items verified.** Evidence: `app/backend/judge.py:88` returns `"supported"` on `TimeoutError`. Fix: return `needs_review` with reason "judge unavailable". Test: fixture backend raising timeout yields `needs_review`.
61	- **major — Gap test misses the boundary.** Evidence: `tests/unit/test_gaps.py` covers 28 and 73 days only. Fix: add 29/30/31 cases asserting flag only when > 30.
62	- **blocker — Money as float (red flag: float arithmetic on money).** Evidence: `charges.py:41 total += float(amt)`. Fix: parse to `Decimal` or integer cents.
63	
64	## 9. Sources
65	- https://google.github.io/eng-practices/review/reviewer/looking-for.html — Google eng-practices: review design, functionality, complexity, tests, naming, comments, docs; read every line in scope.
66	- https://martinfowler.com/articles/nonDeterminism.html — Fowler (2011): quarantine flaky tests, never bare sleeps, test doubles for remote services, wrap the clock.
67	- https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter — AWS Builders' Library: timeouts on every remote call, capped retries at one layer, jitter, idempotency before retrying.
68	- https://www.anthropic.com/engineering/building-effective-agents — Anthropic (Dec 2024): simplest solution first; predefined workflows for well-defined tasks; evaluator-optimizer pattern needs clear criteria.
69	- docs/CONTRACT.md §5.2 — the binding LLM/code table and validation ladder this reviewer enforces.
70	- Assumption: Decimal/integer-cents money handling is standard practice; no single source cited.
71	
72	## 10. Limits
73	Do not judge UX copy, clinical meaning, legal strategy, or the product note's prose. Security depth (injection, secrets, rate limits) belongs to security-reviewer; flag obvious issues and defer.
74	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:21:47.713Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-088 && echo ---- && python3 tools/board.py show T-089",
 "description": "Show board cards T-088 and T-089"
}
````

### User / tool · 2026-11-02T04:21:47.898Z

**tool result**
````
---
id: "T-088"
title: "Date-convention suggestion (pre-select with stated reason, still one confirm)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:21:41Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: ["f667f08"]
reviews: []
ac:
  - {"n": 1, "text": "For an ambiguous numeric date, the API suggests MM/DD or DD/MM with the reason (other dates in the packet), the UI pre-selects it, and the paralegal still confirms once; never auto-applied; eval case", "done": true, "evidence": "tests/unit/test_date_convention.py (8 tests) pass: month-first/day-first/no-evidence/mixed evidence, golden case_01 suggestion, confirm still required, nothing written. UI pre-select is frontend's (see note)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed
- 2026-11-02T04:21:36Z backend: UI needs: dates_to_confirm[].suggestion {convention, label, iso, reason, evidence, auto_applied:false} (contract in api.md). Pre-select the radio for suggestion.iso (when non-null), show reason beneath, still require an explicit confirm click (D-041); never confirm on load. Golden: evals/golden/case_01_date_formats should get a case asserting the 04/05/2026 record's suggestion is MM/DD with 4 evidence dates (qa owns golden; unit test tests/unit/test_date_convention.py covers it on that file today). No db change.
- 2026-11-02T04:21:36Z backend: AC 1 checked: tests/unit/test_date_convention.py (8 tests) pass: month-first/day-first/no-evidence/mixed evidence, golden case_01 suggestion, confirm still required, nothing written. UI pre-select is frontend's (see note)
- 2026-11-02T04:21:37Z backend: moved in_progress -> in_review
- 2026-11-02T04:21:41Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Changed: new app/backend/date_convention.py (code only); present.dates_to_confirm adds suggestion; contract section in memory/contracts/api.md. Verified: .venv/bin/python -m pytest tests/unit/test_date_convention.py (8 pass); full unit run has 14 failures all in T-094 J3/conflict, reclassify and provider tests, none from this card. Left: frontend pre-select; qa golden case. Surprised: ambiguous dates within the record text also count as evidence, but dates in ISO form do not. Commit f667f08.

----
---
id: "T-089"
title: "Dismissal-pattern suggestions for a single local profile (suggestions only)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:21:41Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: ["f667f08"]
reviews: []
ac:
  - {"n": 1, "text": "Repeated dismissals of the same flag phrase surface as a suggestion ('You dismissed this 4 times'); never auto-dismisses; per-profile local only; eval shows no recall loss on golden", "done": true, "evidence": "tests/unit/test_dismissal_patterns.py (17 pass): 3 dismissals -> suggestion, 2 -> none, apply only on click via review path, no self-reinforcement, ineligible types never offered, demo-mode isolation, pipeline output identical on all golden cases + sample with/without history (recall unchanged)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed
- 2026-11-02T04:21:37Z backend: UI needs: GET /api/cases/{token}/dismissal_suggestions -> {suggestions:[{key,kind,label,dismissed_count,scope,flag_ids,message,auto_applied:false}]}; show message as a banner on the flags list with Hide similar (POST .../dismissal_suggestions/apply {key}) and Keep showing (client-side only). Never apply on load. Hidden flags stay in the Dismissed filter and are reversible via reset. Thresholds 3 (phrase) and 5 (category); only lexicon pre_existing/causation flags are eligible. History is read from the flags table (no db change); counts span all cases only under ZLAYT_MODE=local. Golden: no case needed; unit test proves identical pipeline output on every golden case with and without dismissal history.
- 2026-11-02T04:21:37Z backend: AC 1 checked: tests/unit/test_dismissal_patterns.py (17 pass): 3 dismissals -> suggestion, 2 -> none, apply only on click via review path, no self-reinforcement, ineligible types never offered, demo-mode isolation, pipeline output identical on all golden cases + sample with/without history (recall unchanged)
- 2026-11-02T04:21:37Z backend: moved in_progress -> in_review
- 2026-11-02T04:21:41Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Changed: new app/backend/dismissal_patterns.py (suggest read-only, apply = paralegal click via review.apply_review), 2 routes registered in api.py, contract in api.md. Verified: .venv/bin/python -m pytest tests/unit/test_dismissal_patterns.py (17 pass); recall unchanged shown by pipeline-output equality on every golden case. Left: frontend banner; optional db CHECK for a dismissal_suggestion event (not needed, reviewer_note marks bulk-hidden flags). Surprised: flags do not store the lexicon phrase, so the phrase is re-derived by lexicon_scan on the flag's evidence. Commit f667f08.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:21:48.117Z

**tool call — Bash**
````
{
 "command": "grep -n -A12 -E \"D-041|D-042\" memory/ORCHESTRATOR_DECISIONS.md | head -120",
 "description": "Read D-041 and D-042 decisions"
}
````

### User / tool · 2026-11-02T04:21:48.201Z

**tool result**
````
49:| D-041 | An entry with no confirmed date cannot be accepted into the letter (2026-11-02). Accept returns 422 `DATE_UNCONFIRMED` until the paralegal confirms a date (Dates to confirm) or the entry is moved to the notes block. The UI disables Accept with the reason shown. 'Date not stated' never appears in the treatment section. | A demand letter treatment line without a date is unusable and invites an adjuster challenge. | T-068 paralegal r2 major |
50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
51-| D-043 | Credibility flags fail toward flagging (2026-11-02, after T-067 r3): any sentence containing a credibility term flags, **unless** the whole sentence is one clause matching a short allow-list of clean negations ('No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Not tested/not performed.'). Anything with a second clause, contrast word or side qualifier flags. An extra flag costs one paralegal click; a missed one costs credibility at the adjuster. | Three rounds of clause-scoped negation each regressed a different word order. | T-067 claims-adjuster r3 |
52-| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
53-| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
54-| D-046 | Ship-bar item 4 also gates on the seeded J3 (conflict) and J4 (flag) judge control sets (2026-11-02): each must catch every seeded wrong item with 0 false agrees. Control labels are fixed before a run; an item may be relabelled only with a written reason reviewed by a second agent, never because it failed. | Judges J3/J4 now decide flags (T-075, T-094); a catch rate only on J1 would leave them unmeasured. | T-093 staff r1 major 2 |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:21:50.716Z

**tool call — Bash**
````
{
 "command": "git rev-parse --is-inside-work-tree 2>&1; git show --stat f667f08 2>&1 | head -60; echo ----; git log --oneline -5 2>&1; echo ----; git status --short 2>&1 | head -40",
 "description": "Inspect commit f667f08 and working tree state"
}
````

### User / tool · 2026-11-02T04:21:50.905Z

**tool result**
````
true
commit f667f087a24b6d618e6129696a874fa61605258d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:21:22 2026 -0600

    feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)
    
    Both are suggestions only: neither changes pipeline output or applies itself.
    Contract in memory/contracts/api.md.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/api.py                    |   3 +-
 app/backend/date_convention.py        |  67 +++++++++++++++++
 app/backend/dismissal_patterns.py     | 114 +++++++++++++++++++++++++++++
 app/backend/present.py                |   9 ++-
 memory/contracts/api.md               |  29 ++++++++
 tests/unit/test_date_convention.py    | 103 ++++++++++++++++++++++++++
 tests/unit/test_dismissal_patterns.py | 134 ++++++++++++++++++++++++++++++++++
 7 files changed, 455 insertions(+), 4 deletions(-)
----
5616dc3 feat(frontend): side-by-side source viewer at >= 1024 px (R-ST-1, T-046)
f667f08 feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)
328428f feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
d0aee83 feat(evals): calibrated confidence from measured matches per state and item type (T-090)
ea259cd docs: D-046 ship-bar item 4 gates on J3/J4 seeded controls
----
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
D  app/backend/date_convention.py
D  app/backend/dismissal_patterns.py
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/pdf_text.py
 M app/backend/pipeline.py
MM app/backend/present.py
 M app/backend/review.py
 M app/backend/trace.py
 M app/frontend/api.js
 M app/frontend/export.js
 M app/frontend/judges.js
 M app/frontend/stepper.css
 M app/frontend/stepper.js
 M app/frontend/timeline.js
 M app/llm/audited.py
D  app/llm/prompts/conflicts_v1.md
 M artifacts/screenshots/judge-panel-1440.png
 M artifacts/screenshots/judge-panel-390.png
 M artifacts/screenshots/stepper-case-1440.png
 M artifacts/screenshots/stepper-case-390.png
 M artifacts/screenshots/stepper-case-collapsed-1440.png
 M artifacts/screenshots/stepper-case-collapsed-390.png
 M artifacts/screenshots/stepper-item-1440.png
 M board/activity.jsonl
 M board/cards/T-045.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:21:51.221Z

**tool call — Bash**
````
{
 "command": "ls app/backend/ | head -80; echo ----; ls tests/unit | grep -iE \"date|dismiss|suggest\"; echo ----; ls evals/golden 2>&1 | head -40",
 "description": "List backend modules and related unit tests"
}
````

### User / tool · 2026-11-02T04:21:51.322Z

**tool result**
````
__init__.py
__pycache__
amounts.py
api.py
billing.py
case_extras.py
confidence.py
conflict_candidates.py
conflicts.py
credibility.py
date_convention.py
dates.py
dismissal_patterns.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judge_guard.py
judges.py
language.py
lexicon.py
lexicon_scan.py
narrative.py
pdf_checks.py
pdf_hidden.py
pdf_ocr.py
pdf_text.py
pipeline.py
present.py
reclassify.py
rejudge.py
review.py
schemas.py
sentences.py
split_llm.py
store.py
totals.py
trace.py
why.py
----
test_conflict_candidates.py
test_date_convention.py
test_date_unconfirmed.py
test_dates.py
test_dismissal_patterns.py
----
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
case_09_nonvisit_hides_gap.expected.json
case_09_nonvisit_hides_gap.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
judge_controls.jsonl
judge_controls_heldout.jsonl
sample.expected.json
sample.export.expected.txt
sample.txt
unsplit_paste.split.json
unsplit_paste.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:21:54.330Z

**tool call — Bash**
````
{
 "command": "git show f667f08 -- app/backend/date_convention.py app/backend/present.py app/backend/api.py | cat -n | head -300",
 "description": "Show diff of date convention and present/api changes"
}
````

### User / tool · 2026-11-02T04:21:54.447Z

**tool result**
````
     1	commit f667f087a24b6d618e6129696a874fa61605258d
     2	Author: Chris Borsheim <cborsheim@gmail.com>
     3	Date:   Sun Nov 1 22:21:22 2026 -0600
     4	
     5	    feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)
     6	    
     7	    Both are suggestions only: neither changes pipeline output or applies itself.
     8	    Contract in memory/contracts/api.md.
     9	    
    10	    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
    11	
    12	diff --git a/app/backend/api.py b/app/backend/api.py
    13	index 4edd585..4cd0b39 100644
    14	--- a/app/backend/api.py
    15	+++ b/app/backend/api.py
    16	@@ -20,7 +20,7 @@ from starlette.exceptions import HTTPException as StarletteHTTPException
    17	 
    18	 from starlette.concurrency import run_in_threadpool
    19	 
    20	-from app.backend import case_extras, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
    21	+from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
    22	 from app.db import db as DB
    23	 
    24	 MAX_BODY_BYTES = 512 * 1024      # cheap rejection before the 60,000-character rule: UTF-8 worst case plus JSON overhead
    25	@@ -494,6 +494,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
    26	             c.close()
    27	 
    28	     case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
    29	+    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
    30	 
    31	     @app.get("/api/cases/{token}/export")
    32	     def export(token: str):
    33	diff --git a/app/backend/date_convention.py b/app/backend/date_convention.py
    34	new file mode 100644
    35	index 0000000..226b57d
    36	--- /dev/null
    37	+++ b/app/backend/date_convention.py
    38	@@ -0,0 +1,67 @@
    39	+"""Date-convention SUGGESTION for ambiguous numeric dates (T-088, D-042; code only, LLM_VS_CODE row 2). Never applied by itself.
    40	+
    41	+An ambiguous record date such as 04/05/2026 has two code-proposed readings (MM/DD and DD/MM). This module looks at the OTHER numeric
    42	+dates in the same packet whose order is certain (one number above 12: 03/14/2026 is month first, 14/03/2026 is day first) and, when they
    43	+all agree, suggests that order with the reason stated in plain words and the dates it rests on. Mixed evidence or none: no suggestion.
    44	+The suggestion is a hint the UI pre-selects; the paralegal still confirms once through confirm_date (D-041), and confirm_date still only
    45	+accepts one of the code candidates. Nothing here writes to the database or changes a pipeline result."""
    46	+import re
    47	+
    48	+from app.backend import dates
    49	+
    50	+_NUM_DATE = re.compile(r"(?<![\d/.\-])(\d{1,2})([/.\-])(\d{1,2})\2(\d{4}|\d{2})(?![\d/.\-]\d)(?!\d)")
    51	+MAX_EVIDENCE = 2
    52	+_LABEL = {"MDY": "MM/DD", "DMY": "DD/MM"}
    53	+
    54	+
    55	+def _order(a: int, b: int):
    56	+    """MDY / DMY when the numbers prove the order, else None (both <= 12, or neither a valid month)."""
    57	+    if a > 12 and 1 <= b <= 12:
    58	+        return "DMY"
    59	+    if b > 12 and 1 <= a <= 12:
    60	+        return "MDY"
    61	+    return None
    62	+
    63	+
    64	+def _evidence(records, raw_text):
    65	+    """Unambiguous numeric dates in the packet, in record order: [{record_id, raw, order}]. Reads each record's date label and its text."""
    66	+    out, seen = [], set()
    67	+    for r in records:
    68	+        block = raw_text[r["char_start"]:r["char_end"]]
    69	+        for m in _NUM_DATE.finditer(block):
    70	+            order = _order(int(m[1]), int(m[3]))
    71	+            key = (r["id"], m[0])
    72	+            if order and key not in seen:
    73	+                seen.add(key)
    74	+                out.append({"record_id": r["id"], "raw": m[0], "order": order})
    75	+    return out
    76	+
    77	+
    78	+def _example(ev):
    79	+    return f"({ev['raw']})"
    80	+
    81	+
    82	+def suggest(rec: dict, records: list, raw_text: str):
    83	+    """Suggestion for one ambiguous record, or None. `rec` and `records` are record rows (id, date_raw, date_status, date_candidates,
    84	+    char_start, char_end). Returns {convention, label, iso, reason, evidence[]}; `iso` is None when the year is also ambiguous."""
    85	+    if rec.get("date_status") != "ambiguous":
    86	+        return None
    87	+    m = _NUM_DATE.fullmatch(" ".join(str(rec.get("date_raw") or "").split()))
    88	+    if not m or _order(int(m[1]), int(m[3])) is not None:
    89	+        return None
    90	+    ev = _evidence(records, raw_text)
    91	+    orders = {e["order"] for e in ev}
    92	+    if len(orders) != 1:
    93	+        return None                      # no evidence, or the packet mixes both orders: say nothing rather than guess
    94	+    order = next(iter(orders))
    95	+    a, b = int(m[1]), int(m[3])
    96	+    mo, d = (a, b) if order == "MDY" else (b, a)
    97	+    cands = [c for c in rec.get("date_candidates") or [] if int(c[5:7]) == mo and int(c[8:10]) == d]
    98	+    iso = cands[0] if len(cands) == 1 else None
    99	+    shown = ev[:MAX_EVIDENCE]
   100	+    n = len(ev)
   101	+    first = "month first" if order == "MDY" else "day first"
   102	+    reason = (f"Other dates in this record use {first} {_example(shown[0])}" if n == 1 else
   103	+              f"{n} other dates in this record use {first} " + " and ".join(_example(e) for e in shown))
   104	+    return {"convention": order, "label": _LABEL[order], "iso": iso, "reason": reason,
   105	+            "evidence": [{"record_id": e["record_id"], "raw": e["raw"]} for e in shown], "evidence_count": n, "auto_applied": False}
   106	diff --git a/app/backend/present.py b/app/backend/present.py
   107	index 01344f8..f9bc01f 100644
   108	--- a/app/backend/present.py
   109	+++ b/app/backend/present.py
   110	@@ -1,7 +1,7 @@
   111	 """Read-side views in the shapes of memory/contracts/api.md, built from the DB. No writes."""
   112	 import json
   113	 
   114	-from app.backend import confidence, grounding, pdf_text, sentences, store, totals as T, why
   115	+from app.backend import confidence, date_convention, grounding, pdf_text, sentences, store, totals as T, why
   116	 from app.db import db as DB
   117	 
   118	 STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
   119	@@ -123,8 +123,11 @@ def review_view(conn, case_id):
   120	 
   121	 
   122	 def dates_to_confirm(conn, case_id):
   123	-    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"]}
   124	-            for r in _recs_by_id(conn, case_id).values() if r["date_status"] in ("ambiguous", "missing")]
   125	+    recs = list(_recs_by_id(conn, case_id).values())
   126	+    raw = DB.get_case(conn, case_id)["raw_text"]
   127	+    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"],
   128	+             "suggestion": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)
   129	+            for r in recs if r["date_status"] in ("ambiguous", "missing")]
   130	 
   131	 
   132	 def record_view(r, raw, with_sentences=True, pages=None):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:21:54.656Z

**tool call — Bash**
````
{
 "command": "git show f667f08:app/backend/date_convention.py | cat -n",
 "description": "Read committed date_convention.py with line numbers"
}
````

### User / tool · 2026-11-02T04:21:54.757Z

**tool result**
````
     1	"""Date-convention SUGGESTION for ambiguous numeric dates (T-088, D-042; code only, LLM_VS_CODE row 2). Never applied by itself.
     2	
     3	An ambiguous record date such as 04/05/2026 has two code-proposed readings (MM/DD and DD/MM). This module looks at the OTHER numeric
     4	dates in the same packet whose order is certain (one number above 12: 03/14/2026 is month first, 14/03/2026 is day first) and, when they
     5	all agree, suggests that order with the reason stated in plain words and the dates it rests on. Mixed evidence or none: no suggestion.
     6	The suggestion is a hint the UI pre-selects; the paralegal still confirms once through confirm_date (D-041), and confirm_date still only
     7	accepts one of the code candidates. Nothing here writes to the database or changes a pipeline result."""
     8	import re
     9	
    10	from app.backend import dates
    11	
    12	_NUM_DATE = re.compile(r"(?<![\d/.\-])(\d{1,2})([/.\-])(\d{1,2})\2(\d{4}|\d{2})(?![\d/.\-]\d)(?!\d)")
    13	MAX_EVIDENCE = 2
    14	_LABEL = {"MDY": "MM/DD", "DMY": "DD/MM"}
    15	
    16	
    17	def _order(a: int, b: int):
    18	    """MDY / DMY when the numbers prove the order, else None (both <= 12, or neither a valid month)."""
    19	    if a > 12 and 1 <= b <= 12:
    20	        return "DMY"
    21	    if b > 12 and 1 <= a <= 12:
    22	        return "MDY"
    23	    return None
    24	
    25	
    26	def _evidence(records, raw_text):
    27	    """Unambiguous numeric dates in the packet, in record order: [{record_id, raw, order}]. Reads each record's date label and its text."""
    28	    out, seen = [], set()
    29	    for r in records:
    30	        block = raw_text[r["char_start"]:r["char_end"]]
    31	        for m in _NUM_DATE.finditer(block):
    32	            order = _order(int(m[1]), int(m[3]))
    33	            key = (r["id"], m[0])
    34	            if order and key not in seen:
    35	                seen.add(key)
    36	                out.append({"record_id": r["id"], "raw": m[0], "order": order})
    37	    return out
    38	
    39	
    40	def _example(ev):
    41	    return f"({ev['raw']})"
    42	
    43	
    44	def suggest(rec: dict, records: list, raw_text: str):
    45	    """Suggestion for one ambiguous record, or None. `rec` and `records` are record rows (id, date_raw, date_status, date_candidates,
    46	    char_start, char_end). Returns {convention, label, iso, reason, evidence[]}; `iso` is None when the year is also ambiguous."""
    47	    if rec.get("date_status") != "ambiguous":
    48	        return None
    49	    m = _NUM_DATE.fullmatch(" ".join(str(rec.get("date_raw") or "").split()))
    50	    if not m or _order(int(m[1]), int(m[3])) is not None:
    51	        return None
    52	    ev = _evidence(records, raw_text)
    53	    orders = {e["order"] for e in ev}
    54	    if len(orders) != 1:
    55	        return None                      # no evidence, or the packet mixes both orders: say nothing rather than guess
    56	    order = next(iter(orders))
    57	    a, b = int(m[1]), int(m[3])
    58	    mo, d = (a, b) if order == "MDY" else (b, a)
    59	    cands = [c for c in rec.get("date_candidates") or [] if int(c[5:7]) == mo and int(c[8:10]) == d]
    60	    iso = cands[0] if len(cands) == 1 else None
    61	    shown = ev[:MAX_EVIDENCE]
    62	    n = len(ev)
    63	    first = "month first" if order == "MDY" else "day first"
    64	    reason = (f"Other dates in this record use {first} {_example(shown[0])}" if n == 1 else
    65	              f"{n} other dates in this record use {first} " + " and ".join(_example(e) for e in shown))
    66	    return {"convention": order, "label": _LABEL[order], "iso": iso, "reason": reason,
    67	            "evidence": [{"record_id": e["record_id"], "raw": e["raw"]} for e in shown], "evidence_count": n, "auto_applied": False}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:04.045Z

**tool call — Bash**
````
{
 "command": "git show f667f08:app/backend/dismissal_patterns.py | cat -n",
 "description": "Read committed dismissal_patterns.py with line numbers"
}
````

### User / tool · 2026-11-02T04:22:04.139Z

**tool result**
````
     1	"""Dismissal-pattern SUGGESTIONS for the single local profile (T-089, D-042; code only, LLM_VS_CODE row 12). Suggestions only.
     2	
     3	The tool has one local profile: no accounts, no users, no auth. "Profile" means this machine's database, so the history is the set of flags
     4	the paralegal has dismissed in it (read from the flags table; nothing new is stored, and deleting a case deletes its history). Outside
     5	ZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.
     6	
     7	When the same lexicon phrase (PHRASE_MIN dismissals) or the same category (CATEGORY_MIN) has been dismissed repeatedly, the review screen
     8	may offer "You dismissed this kind of flag 4 times. Hide similar ones in this case?". This module only READS: suggest() never writes and
     9	never changes a pipeline result, a flag's state or its review_status. The paralegal's click calls apply(), which dismisses the matching
    10	PENDING flags in this case one by one through the normal review path (each a logged `dismiss` event with a reviewer note). Those
    11	bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself.
    12	
    13	Only lexicon-phrase flags of type pre_existing or causation are eligible. Gap and conflict flags, injection and date warnings, and flags
    14	that code or the model found without a lexicon phrase are never suggested for hiding."""
    15	from fastapi import Request
    16	
    17	from app.backend import lexicon_scan, review
    18	from app.db import db as DB
    19	
    20	PHRASE_MIN = 3
    21	CATEGORY_MIN = 5
    22	ELIGIBLE_TYPES = ("pre_existing", "causation")
    23	APPLIED_NOTE = "Hidden by dismissal-pattern suggestion (paralegal confirmed)."
    24	_BAD = ("rejected",)
    25	
    26	
    27	def _eligible(f) -> bool:
    28	    return f["type"] in ELIGIBLE_TYPES and "lexicon" in (f.get("origin") or "")
    29	
    30	
    31	def _phrase(f):
    32	    """(lexicon entry id, matched phrase) for the flag, from its own evidence text, or (None, None). Same category only."""
    33	    for ev in f.get("evidence") or []:
    34	        hits = [h for h in lexicon_scan.scan(ev.get("text") or "") if h["category"] == f["category"]]
    35	        if hits:
    36	            h = min(hits, key=lambda x: x["start"])
    37	            return h["id"], " ".join(h["text"].lower().split())
    38	    return None, None
    39	
    40	
    41	def _history(conn, case_id: str, local: bool) -> list:
    42	    """Dismissed, eligible flags that were dismissed by the paralegal one at a time."""
    43	    rows = conn.execute("SELECT * FROM flags WHERE review_status='dismissed'" + ("" if local else " AND case_id=?"), () if local else (case_id,)).fetchall()
    44	    return [f for f in (DB._decode(r) for r in rows) if _eligible(f) and (f.get("reviewer_note") or "") != APPLIED_NOTE]
    45	
    46	
    47	def _pending(conn, case_id: str) -> list:
    48	    return [f for f in DB.list_items(conn, case_id, "flag") if f["review_status"] == "pending" and f["state"] not in _BAD and _eligible(f)]
    49	
    50	
    51	def suggest(conn, case_id: str, *, local: bool = False) -> list:
    52	    """Read-only. [{key, kind: phrase|category, label, dismissed_count, scope, flag_ids, message}], phrase suggestions first."""
    53	    hist = _history(conn, case_id, local)
    54	    phrase_n, cat_n = {}, {}
    55	    for f in hist:
    56	        pid, _ = _phrase(f)
    57	        if pid:
    58	            phrase_n[pid] = phrase_n.get(pid, 0) + 1
    59	        cat_n[f["category"]] = cat_n.get(f["category"], 0) + 1
    60	    out, covered = [], set()
    61	    pend = [(f, *_phrase(f)) for f in _pending(conn, case_id)]
    62	    scope = "all cases on this computer" if local else "this case"
    63	    for pid in sorted({p for _, p, _ in pend if p and phrase_n.get(p, 0) >= PHRASE_MIN}):
    64	        ids = [f["id"] for f, p, _ in pend if p == pid]
    65	        label = next(t for _, p, t in pend if p == pid)
    66	        out.append(_row(f"phrase:{pid}", "phrase", label, phrase_n[pid], scope, ids))
    67	        covered.update(ids)
    68	    for cat in sorted({f["category"] for f, _, _ in pend if cat_n.get(f["category"], 0) >= CATEGORY_MIN}):
    69	        ids = [f["id"] for f, _, _ in pend if f["category"] == cat and f["id"] not in covered]
    70	        if ids:
    71	            out.append(_row(f"category:{cat}", "category", cat.replace("_", " "), cat_n[cat], scope, ids))
    72	    return out
    73	
    74	
    75	def _row(key, kind, label, n, scope, ids):
    76	    return {"key": key, "kind": kind, "label": label, "dismissed_count": n, "scope": scope, "flag_ids": ids, "auto_applied": False,
    77	            "message": f"You dismissed this kind of flag {n} times. Hide similar ones in this case?"}
    78	
    79	
    80	def apply(conn, case_id: str, key: str, *, local: bool = False, now=None) -> dict:
    81	    """The paralegal accepted the suggestion: dismiss the matching pending flags in THIS case through the normal review path.
    82	    Raises KeyError when the key is not a current suggestion (nothing is written)."""
    83	    s = next((x for x in suggest(conn, case_id, local=local) if x["key"] == key), None)
    84	    if s is None:
    85	        raise KeyError(key)
    86	    for fid in s["flag_ids"]:
    87	        review.apply_review(conn, case_id, fid, {"action": "dismiss", "note": APPLIED_NOTE}, now=now)
    88	    return {"key": key, "dismissed_flag_ids": s["flag_ids"], "suggestions": suggest(conn, case_id, local=local)}
    89	
    90	
    91	def add_routes(app, *, conn, get_case, body_of, ApiError, now, local_mode):
    92	    @app.get("/api/cases/{token}/dismissal_suggestions")
    93	    def dismissal_suggestions(token: str):
    94	        c = conn()
    95	        try:
    96	            get_case(c, token)
    97	            return {"suggestions": suggest(c, token, local=local_mode()), "min_phrase": PHRASE_MIN, "min_category": CATEGORY_MIN}
    98	        finally:
    99	            c.close()
   100	
   101	    @app.post("/api/cases/{token}/dismissal_suggestions/apply")
   102	    async def dismissal_suggestions_apply(token: str, request: Request):
   103	        b = await body_of(request)
   104	        if not isinstance(b.get("key"), str):
   105	            raise ApiError(400, "bad_request", "Send the key of the suggestion to apply.")
   106	        c = conn()
   107	        try:
   108	            get_case(c, token)
   109	            try:
   110	                return apply(c, token, b["key"], local=local_mode(), now=now)
   111	            except KeyError:
   112	                raise ApiError(404, "not_found", "That suggestion no longer applies.") from None
   113	        finally:
   114	            c.close()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:04.509Z

**tool call — Bash**
````
{
 "command": "git show f667f08:memory/contracts/api.md | tail -45",
 "description": "Read the API contract additions from the commit"
}
````

### User / tool · 2026-11-02T04:22:04.610Z

**tool result**
````
Run the second check again for the AI-made items whose judge never answered (the items the export gate lists as `JUDGE_NOT_RUN`, plus any live pending ones with no answer: kept on purpose so the `judges` step's RERUN_JUDGE button always has something to do; D-045 note). No body. The same judge (J1 entry, J2 charge, J3 AI conflict, J4 AI flag) gets the same input the run or the edit gave it, so a recorded answer is found again. Same rules as `/run`: `404 not_found`; `409 run_in_progress`; `409 demo_mode_unsupported_input` (demo mode, text not a recorded case); `503 llm_unavailable`. **Demo mode (no `ENABLE_LIVE=1`) is fixture-only**: only recorded answers are replayed, a miss stays unavailable and never calls a model; live calls (`claude-cli` or `anthropic-api` with a key) need `ENABLE_LIVE=1`. Every call is audited in `llm_calls` (judge role, item id, step `j1`..`j4`) and each attempt is appended to the item's `ladder.rejudge[]` `{at, call_id, verdict}`. An answer replaces `ladder.judge` and recomposes `state`/`state_reasons` (other doubts stay; `JUDGE_UNAVAILABLE`/`FIXTURE_MISS` go; an objection adds `JUDGE_PARTIAL|UNSUPPORTED|DISAGREES|UNSURE`); `review_status` is never changed. Nothing can clear the gate except an answer.
```json
{ "token": "k3Jf9x...", "asked": 12,
  "rejudged": [ { "item_id": "e4", "kind": "entry", "judge": "j1", "review_status": "accepted", "verdict": "supported", "state": "verified", "state_reasons": [] } ],
  "still_unavailable": [ { "item_id": "a2", "kind": "amount", "judge": "j2", "review_status": "accepted", "verdict": "unavailable" } ],
  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
```
`verdict` is the ladder vocabulary (`supported|partially|unsupported|disagrees|unsure|unavailable`). Frontend: after the call, refetch `/trace` (and the case view, since `state` can change).

## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays token-only and has no case list.
`GET /api/cases` -> `{ "cases": [ { "token", "name", "status", "source", "record_count", "counts": {"pending","accepted","edited","dismissed","needs_review"}, "created_at" } ] }`, newest first, never record text.
`GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
`POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).

## DELETE /api/cases/{token}
`204`. Removes the case, records, items, calls and events. It is the same function the 24 h purge uses and deletes from every table by case id, including stored prompts (ADR-006).

---

## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
| Code | State | Meaning |
|---|---|---|
| `GROUNDING_EXCERPT_NOT_VERBATIM` | rejected | model's excerpt is not word for word in the record |
| `GROUNDING_AMOUNT_NOT_IN_TEXT` | rejected | model reported an amount the record does not contain |
| `SCHEMA_INVALID` | rejected | model output failed schema validation after retries |
| `SUMMARY_TOKEN_NOT_IN_EXCERPT` | needs_review | a number, date, dollar figure or left/right/no/not/without in the summary (or an edit) is not in the quote |
| `SUMMARY_DROPS_QUALIFIER` | needs_review | the excerpt has a hedge, self-report marker, negation, laterality or "approx." that the summary leaves out (D-022) |
| `EXCERPT_OMITS_QUALIFIER` | needs_review | the record has a hedge sentence the excerpt leaves out |
| `EXCERPT_NOT_WHOLE_SENTENCE` | needs_review | the excerpt starts or ends mid-sentence |
| `HIGHLIGHT_NOT_FOUND` | needs_review | the quote cannot be located in the raw text for highlighting |
| `JUDGE_PARTIAL` / `JUDGE_UNSUPPORTED` | needs_review | judge 1 found the summary partly or not supported |
| `JUDGE_DISAGREES` / `JUDGE_UNSURE` | needs_review | judge 2, 3 or 4 disagreed or could not decide |
| `JUDGE_UNAVAILABLE` | needs_review | the judge call failed or timed out, or (always in demo mode) an edit has no recorded judge answer |
| `FIXTURE_MISS` | needs_review | the demo has no recorded model answer for this call; never retried |
| `DATE_AMBIGUOUS` / `DATE_MISSING` | needs_review | date has two readings or is absent; excluded from gap math until confirmed |
| `ENDPOINT_NOT_VERIFIED` | needs_review | a gap's span could contain an unconfirmed date |
| `AMOUNT_RATE_NOT_TOTALED` | needs_review | a rate, not a charge |
| `AMOUNT_ESTIMATE` / `AMOUNT_DAMAGES` / `AMOUNT_UNCLEAR` | needs_review | estimate, non-bill figure, or unreadable/unlabelled value |
| `LEXICON_ONLY` / `LLM_ONLY` | needs_review | phrase list and model disagree on a flag |
| `SPLIT_AMBIGUOUS` | needs_review | record boundaries uncertain |
| `LLM_SPLIT` | needs_review | the record's boundaries were chosen by the model (code-validated), because the paste had no recognisable record markers |
| `INJECTION_SUSPECTED` | needs_review | the item's record (or a cross-record pass in this case) carries an instruction-like-text warning |
| `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
| `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded answer; conflicts between records may be missing (case-level `record_warning` `analysis_incomplete`, no single record) |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:14.049Z

**tool call — Bash**
````
{
 "command": "git diff --stat HEAD -- app/backend/date_convention.py app/backend/dismissal_patterns.py app/backend/present.py app/backend/api.py app/backend/review.py app/backend/pipeline.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py memory/contracts/api.md; echo \"exit=$?\"; echo ----; git status --short -- app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py memory/contracts/api.md; echo ----; git show f667f08 -- memory/contracts/api.md | head -80",
 "description": "Check working-tree drift on the card files and show contract diff"
}
````

### User / tool · 2026-11-02T04:22:14.220Z

**tool result**
````
 app/backend/api.py                    |   2 +
 app/backend/date_convention.py        |  67 -----------------
 app/backend/dismissal_patterns.py     | 114 -----------------------------
 app/backend/pipeline.py               |  18 ++---
 app/backend/review.py                 |  14 ++--
 tests/unit/test_date_convention.py    | 103 --------------------------
 tests/unit/test_dismissal_patterns.py | 134 ----------------------------------
 7 files changed, 15 insertions(+), 437 deletions(-)
exit=0
----
D  app/backend/date_convention.py
D  app/backend/dismissal_patterns.py
MM memory/contracts/api.md
D  tests/unit/test_date_convention.py
D  tests/unit/test_dismissal_patterns.py
?? app/backend/date_convention.py
?? app/backend/dismissal_patterns.py
?? tests/unit/test_date_convention.py
?? tests/unit/test_dismissal_patterns.py
----
commit f667f087a24b6d618e6129696a874fa61605258d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:21:22 2026 -0600

    feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)
    
    Both are suggestions only: neither changes pipeline output or applies itself.
    Contract in memory/contracts/api.md.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index e722aa1..ef44675 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -21,6 +21,8 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
 | POST | `/api/cases/{token}/run` | start the LLM stages (202) |
 | GET | `/api/cases/{token}/status` | stage and progress |
 | POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
+| GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |
+| POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |
 | POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt, confirm_warnings?}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same token check and judge 1 as an edit (`409 needs_confirm` for non-numeric judge objections only; a number, date or $ figure in the summary that is not in the quote is a hard `422 invalid_edit` with `detail.tokens`, no override, D-034); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`; an override is listed in the notes as `reviewer override: <code>`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
 | POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
 | GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
@@ -230,6 +232,33 @@ Response 200: the record with `date_status: "confirmed"`, its entry's date, the
 ```
 `422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event whose `after` records the chosen date (`date_chosen`, `date_raw`, `candidates`, `record_id`) and the ids whose `DATE_AMBIGUOUS` reason it cleared. Confirming also removes `DATE_AMBIGUOUS` from the entry's `reasons` and recomputes its `state` (it becomes `verified` unless another reason remains), so the entry reads like any other dated entry and can be reviewed normally. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
 
+## Date-convention suggestion (T-088, D-042): `dates_to_confirm[].suggestion`
+Every entry of `dates_to_confirm` (in `GET /api/cases/{token}` and in the `confirm_date` response) now has a `suggestion`: `null`, or a hint for an **ambiguous** numeric date. Code only (`app/backend/date_convention.py`). It looks at the other numeric dates in the packet whose order is certain (one number above 12: `03/14/2026` is month first, `14/03/2026` is day first), in each record's date label and text. It suggests only when all of that evidence agrees; no evidence, or evidence in both orders, gives `null`.
+```json
+{ "record_id": "r8", "raw": "04/05/2026", "candidates": ["2026-04-05", "2026-05-04"], "status": "ambiguous",
+  "suggestion": { "convention": "MDY", "label": "MM/DD", "iso": "2026-04-05",
+                  "reason": "Other dates in this record use month first (03/14/2026)",
+                  "evidence": [{"record_id": "r3", "raw": "03/14/2026"}], "evidence_count": 1, "auto_applied": false } }
+```
+`convention` is `MDY` or `DMY`. `iso` is the candidate that reading gives, always one of `candidates`, or `null` when the year is also ambiguous (two-digit year above 40). `reason` is plain words: one date reads "Other dates in this record use month first (03/14/2026)"; several read "4 other dates in this record use month first (02/17/2026) and (03-17-26)" (at most two examples in `evidence`, the total in `evidence_count`). `auto_applied` is always `false`.
+
+The suggestion changes nothing: the record stays `ambiguous`, its entry stays in `undated_entries`, and Accept stays blocked (D-041, `DATE_UNCONFIRMED`) until the paralegal confirms through `confirm_date`, which still accepts only a code candidate (`422 date_invalid` otherwise). **UI:** pre-select the radio for `suggestion.iso` (when not null), show `reason` under it, keep the confirm button enabled only on an explicit click, and let the paralegal pick the other reading freely. Do not confirm on load.
+
+## Dismissal-pattern suggestions (T-089, D-042): `GET /api/cases/{token}/dismissal_suggestions`
+Suggestions only (`app/backend/dismissal_patterns.py`). The tool has one local profile and no accounts, so "the profile" is this machine's database: the history is the set of flags the paralegal dismissed one at a time. Under `ZLAYT_MODE=local` it counts every case in the database; otherwise only this case (a public/demo token never sees another case's dismissals). Nothing new is stored. Only lexicon-phrase flags of type `pre_existing` or `causation` can be suggested; gap and conflict flags, injection and date warnings are never offered for hiding.
+Response 200:
+```json
+{ "suggestions": [
+    { "key": "phrase:new_onset", "kind": "phrase", "label": "new onset", "dismissed_count": 4, "scope": "all cases on this computer",
+      "flag_ids": ["f_r7_2"], "auto_applied": false,
+      "message": "You dismissed this kind of flag 4 times. Hide similar ones in this case?" } ],
+  "min_phrase": 3, "min_category": 5 }
+```
+`kind` is `phrase` (same lexicon phrase group dismissed at least `min_phrase` times) or `category` (same category at least `min_category` times, listing only flags a phrase suggestion does not already cover). `flag_ids` are this case's still-**pending** flags that match. The list is empty when nothing qualifies. This GET is read-only and changes no flag, state or pipeline result.
+
+### POST /api/cases/{token}/dismissal_suggestions/apply
+Request `{"key": "phrase:new_onset"}`. This is the paralegal's click on "Hide similar": the server dismisses each matching pending flag in this case through the normal review path (one logged `dismiss` event per flag, `reviewer_note` "Hidden by dismissal-pattern suggestion (paralegal confirmed)."). They stay reversible with `reset`. Response 200: `{"key", "dismissed_flag_ids": [...], "suggestions": [...]}` (the refreshed list). `404 not_found` when the key is not a current suggestion (nothing written); `400 bad_request` without a `key`. Bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself. **UI:** show the `message` as a dismissible banner/chip on the flags list with two buttons ("Hide similar", "Keep showing"); "Keep showing" is client-side only. Never call `apply` without the click; never hide flags on load. Hidden flags remain in the Dismissed filter.
+
 ## GET /api/cases/{token}/items/{item_id}  — "Why?"
 Ladder, the audited calls behind the item, and the source record text with the highlight range. Prompt text is not returned here (it is in the per-case audit).
 ```json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:14.553Z

**tool call — Bash**
````
{
 "command": "git show f667f08 -- tests/unit/test_date_convention.py | sed -n '1,120p'",
 "description": "Read the T-088 test file from the commit"
}
````

### User / tool · 2026-11-02T04:22:14.653Z

**tool result**
````
commit f667f087a24b6d618e6129696a874fa61605258d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:21:22 2026 -0600

    feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)
    
    Both are suggestions only: neither changes pipeline output or applies itself.
    Contract in memory/contracts/api.md.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_date_convention.py b/tests/unit/test_date_convention.py
new file mode 100644
index 0000000..c7e2235
--- /dev/null
+++ b/tests/unit/test_date_convention.py
@@ -0,0 +1,103 @@
+"""T-088: date-convention suggestion. Code only, never auto-applied, still one confirm (D-041/D-042)."""
+import pytest
+from fastapi.testclient import TestClient
+
+from app.backend import date_convention as DC, present
+from app.backend.api import create_app
+from app.db import db as DB
+from tests.unit import _golden as G
+from tests.unit.test_api_routes import run_case
+from tests.unit.test_date_unconfirmed import snapshot
+
+
+def packet(*dates_text):
+    """records built from (date_raw, extra text) pairs; returns (rows, raw)."""
+    raw, rows, pos = "", [], 0
+    for i, (d, extra) in enumerate(dates_text, 1):
+        block = f"Date: {d}\nNote: {extra}\n"
+        p = dates.parse_date(d)
+        rows.append({"id": f"r{i}", "date_raw": d, "date_status": p["status"], "date_candidates": p["candidates"],
+                     "char_start": pos, "char_end": pos + len(block)})
+        raw, pos = raw + block, pos + len(block)
+    return rows, raw
+
+
+from app.backend import dates   # noqa: E402
+
+
+def test_month_first_evidence_suggests_mm_dd_with_reason():
+    rows, raw = packet(("03/14/2026", "seen"), ("04/05/2026", "seen again"))
+    s = DC.suggest(rows[1], rows, raw)
+    assert s["convention"] == "MDY" and s["label"] == "MM/DD" and s["iso"] == "2026-04-05"
+    assert s["reason"] == "Other dates in this record use month first (03/14/2026)"
+    assert s["evidence"] == [{"record_id": "r1", "raw": "03/14/2026"}] and s["auto_applied"] is False
+
+
+def test_day_first_evidence_suggests_dd_mm():
+    rows, raw = packet(("14/03/2026", "x"), ("04/05/2026", "y"))
+    s = DC.suggest(rows[1], rows, raw)
+    assert s["convention"] == "DMY" and s["iso"] == "2026-05-04" and "day first (14/03/2026)" in s["reason"]
+
+
+def test_evidence_inside_record_text_counts_and_is_listed_up_to_two():
+    rows, raw = packet(("04/05/2026", "follow up on 06/25/2026 and 07/30/2026 and 08/31/2026"))
+    s = DC.suggest(rows[0], rows, raw)
+    assert s["convention"] == "MDY" and s["evidence_count"] == 3 and len(s["evidence"]) == 2
+    assert s["reason"].startswith("3 other dates in this record use month first (06/25/2026) and (07/30/2026)")
+
+
+def test_no_suggestion_without_evidence_or_with_mixed_evidence():
+    rows, raw = packet(("04/05/2026", "alone"), ("06/07/2026", "also ambiguous"))
+    assert DC.suggest(rows[0], rows, raw) is None
+    rows, raw = packet(("03/14/2026", "a"), ("25/03/2026", "b"), ("04/05/2026", "c"))
+    assert DC.suggest(rows[2], rows, raw) is None
+
+
+def test_not_ambiguous_or_iso_dates_never_get_or_give_evidence():
+    rows, raw = packet(("2026-03-14", "iso is not numeric-order evidence"), ("04/05/2026", "x"))
+    assert DC.suggest(rows[1], rows, raw) is None
+    assert DC.suggest(rows[0], rows, raw) is None        # a parsed record has no suggestion
+
+
+def test_two_digit_year_ambiguity_keeps_convention_but_no_iso():
+    rows, raw = packet(("03/14/2026", "x"), ("04/05/98", "y"))
+    s = DC.suggest(rows[1], rows, raw)
+    assert s["convention"] == "MDY" and s["iso"] is None or s["iso"] in rows[1]["date_candidates"]
+
+
+def test_suggestion_never_writes_and_is_not_a_confirmation(tmp_path, monkeypatch):
+    monkeypatch.setenv("LLM_BACKEND", "fixture")
+    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
+    db = str(tmp_path / "x.sqlite")
+    c = TestClient(create_app(db, static_dir=str(tmp_path)))
+    t = run_case(c, G.raw("case_01_date_formats"))
+    before = snapshot(db, t)
+    g = c.get(f"/api/cases/{t}").json()
+    amb = [r for r in g["records"] if r["date_status"] == "ambiguous"]
+    assert amb
+    for item in g["dates_to_confirm"]:
+        s = item.get("suggestion")
+        if s:
+            assert s["auto_applied"] is False and item["candidates"] and (s["iso"] is None or s["iso"] in item["candidates"])
+    assert all(r["date_status"] == "ambiguous" for r in amb)        # nothing was confirmed by the suggestion
+    assert snapshot(db, t) == before
+    conn = DB.connect(db)
+    assert not [e for e in DB.list_events(conn, t) if e["action"] == "confirm_date"]
+    conn.close()
+
+
+def test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required(tmp_path, monkeypatch):
+    monkeypatch.setenv("LLM_BACKEND", "fixture")
+    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
+    db = str(tmp_path / "y.sqlite")
+    c = TestClient(create_app(db, static_dir=str(tmp_path)))
+    t = run_case(c, G.raw("case_01_date_formats"))
+    g = c.get(f"/api/cases/{t}").json()
+    item = [d for d in g["dates_to_confirm"] if d["raw"] == "04/05/2026"][0]
+    s = item["suggestion"]
+    assert s["label"] == "MM/DD" and s["iso"] == "2026-04-05" and s["auto_applied"] is False
+    assert s["evidence_count"] == 4 and s["reason"] == "4 other dates in this record use month first (02/17/2026) and (03-17-26)"
+    assert item["status"] == "ambiguous"                     # still unconfirmed until the paralegal confirms
+    assert c.post(f"/api/cases/{t}/records/{item['record_id']}/confirm_date", json={"date": "2026-06-06"}).status_code == 422
+    r = c.post(f"/api/cases/{t}/records/{item['record_id']}/confirm_date", json={"date": "2026-04-05"})
+    assert r.status_code == 200 and not [d for d in r.json()["dates_to_confirm"] if d["raw"] == "04/05/2026"]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:27.563Z

**tool call — Bash**
````
{
 "command": "git show f667f08:tests/unit/test_dismissal_patterns.py | cat -n",
 "description": "Read the T-089 test file from the commit with line numbers"
}
````

### User / tool · 2026-11-02T04:22:27.665Z

**tool result**
````
     1	"""T-089: dismissal-pattern suggestions for the single local profile. Read-only suggestions; never auto-dismiss; no effect on pipeline output."""
     2	import pytest
     3	from fastapi.testclient import TestClient
     4	
     5	from app.backend import dismissal_patterns as DP, pipeline as PL
     6	from app.backend.api import create_app
     7	from app.db import db as DB
     8	from tests.unit import _golden as G
     9	from tests.unit._fakes import FakeCall, sample_script, which_record as wr
    10	from tests.unit.test_review_rules import seeded
    11	
    12	NEW_ONSET = "New onset pain radiating to right arm with numbness in fingers."
    13	
    14	
    15	def add_flag(conn, case, fid, *, category="new_onset", text=NEW_ONSET, type_="causation", origin="lexicon+llm", status=None):
    16	    DB.add_item(conn, case, "flag", {"id": fid, "type": type_, "category": category, "origin": origin, "title": "t", "explanation": "e",
    17	                "evidence_json": [{"record_no": 1, "text": text, "start": 0, "end": len(text)}], "state": "verified", "state_reasons_json": []})
    18	    if status:
    19	        DB.apply_review(conn, fid, status, now=1.0, case=case)
    20	
    21	
    22	def snapshot(conn, case):
    23	    return [(f["id"], f["review_status"], f["state"]) for f in DB.list_items(conn, case, "flag")]
    24	
    25	
    26	def test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss(tmp_path):
    27	    conn, cid, _ = seeded(tmp_path)
    28	    for i in range(3):
    29	        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    30	    before = snapshot(conn, cid)
    31	    s = DP.suggest(conn, cid)
    32	    assert len(s) == 1 and s[0]["kind"] == "phrase" and s[0]["dismissed_count"] == 3 and s[0]["auto_applied"] is False
    33	    assert s[0]["message"] == "You dismissed this kind of flag 3 times. Hide similar ones in this case?"
    34	    assert "f_r7_2" in s[0]["flag_ids"]                           # the sample's pending new_onset flag
    35	    assert snapshot(conn, cid) == before                          # suggest() wrote nothing; the flag is still pending
    36	    assert next(f for f in DB.list_items(conn, cid, "flag") if f["id"] == "f_r7_2")["review_status"] == "pending"
    37	
    38	
    39	def test_two_dismissals_are_not_enough(tmp_path):
    40	    conn, cid, _ = seeded(tmp_path)
    41	    for i in range(2):
    42	        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    43	    assert DP.suggest(conn, cid) == []
    44	
    45	
    46	def test_ineligible_flags_are_never_suggested(tmp_path):
    47	    conn, cid, _ = seeded(tmp_path)
    48	    for i in range(6):
    49	        add_flag(conn, cid, f"f_g{i}", category="gap_over_30", type_="gap", origin="code", status="dismiss")
    50	        add_flag(conn, cid, f"f_i{i}", category="injection_suspected", type_="record_warning", origin="code", status="dismiss")
    51	    assert DP.suggest(conn, cid) == []
    52	
    53	
    54	def test_category_suggestion_after_five_dismissals_of_different_phrases(tmp_path):
    55	    conn, cid, _ = seeded(tmp_path)
    56	    texts = ["Pain began after the collision.", "Symptoms began after the accident.", "Onset after the fall.", "New onset of numbness.",
    57	             "Developed pain after the accident."]
    58	    for i, t in enumerate(texts):
    59	        add_flag(conn, cid, f"f_c{i}", category="patient_report", text=t, status="dismiss")
    60	    s = DP.suggest(conn, cid)
    61	    cats = [x for x in s if x["kind"] == "category"]
    62	    assert len(cats) == 1 and cats[0]["key"] == "category:patient_report" and cats[0]["dismissed_count"] == 5
    63	    assert cats[0]["flag_ids"] == ["f_r9_1"] and cats[0]["label"] == "patient report"
    64	
    65	
    66	def test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself(tmp_path):
    67	    conn, cid, _ = seeded(tmp_path)
    68	    for i in range(3):
    69	        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    70	    key = DP.suggest(conn, cid)[0]["key"]
    71	    n_events = len(DB.list_events(conn, cid))
    72	    out = DP.apply(conn, cid, key, now=2.0)
    73	    assert out["dismissed_flag_ids"] == ["f_r7_2"] and out["suggestions"] == []
    74	    f = next(x for x in DB.list_items(conn, cid, "flag") if x["id"] == "f_r7_2")
    75	    assert f["review_status"] == "dismissed" and f["reviewer_note"] == DP.APPLIED_NOTE
    76	    assert len(DB.list_events(conn, cid)) == n_events + 1         # one logged dismiss event
    77	    # a bulk-hidden flag is not a new manual dismissal: the count stays 3, not 4
    78	    add_flag(conn, cid, "f_new")
    79	    assert DP.suggest(conn, cid)[0]["dismissed_count"] == 3
    80	    with pytest.raises(KeyError):
    81	        DP.apply(conn, cid, "phrase:nope")
    82	
    83	
    84	def test_scope_is_this_case_unless_local_profile(tmp_path):
    85	    conn, cid, _ = seeded(tmp_path)
    86	    other = DB.create_case(conn, "x", now=1.0)
    87	    for i in range(3):
    88	        add_flag(conn, other, f"f_o{i}", status="dismiss")
    89	    assert DP.suggest(conn, cid, local=False) == []
    90	    s = DP.suggest(conn, cid, local=True)
    91	    assert len(s) == 1 and s[0]["scope"] == "all cases on this computer"
    92	
    93	
    94	def test_routes_and_demo_mode_isolation(tmp_path, monkeypatch):
    95	    monkeypatch.setenv("LLM_BACKEND", "fixture")
    96	    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    97	    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    98	    from tests.unit.test_api_routes import run_case
    99	    db = str(tmp_path / "r.sqlite")
   100	    c = TestClient(create_app(db, static_dir=str(tmp_path)))
   101	    t = run_case(c)
   102	    conn = DB.connect(db)
   103	    for i in range(3):
   104	        add_flag(conn, t, f"f_old{i}", status="dismiss")
   105	    conn.close()
   106	    r = c.get(f"/api/cases/{t}/dismissal_suggestions")
   107	    assert r.status_code == 200 and r.json()["suggestions"][0]["dismissed_count"] == 3
   108	    assert c.get("/api/cases/nope/dismissal_suggestions").status_code == 404
   109	    assert c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={}).status_code == 400
   110	    assert c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={"key": "phrase:zzz"}).status_code == 404
   111	    key = r.json()["suggestions"][0]["key"]
   112	    a = c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={"key": key})
   113	    assert a.status_code == 200 and a.json()["dismissed_flag_ids"] and a.json()["suggestions"] == []
   114	
   115	
   116	@pytest.mark.parametrize("case", G.case_names())
   117	def test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged(tmp_path, case):
   118	    """Same case through the pipeline with and without a dismissal history in the database: identical flags, entries and amounts."""
   119	    def run(seed_history):
   120	        conn = DB.connect(str(tmp_path / f"{case}-{seed_history}.sqlite"))
   121	        if seed_history:
   122	            hist = DB.create_case(conn, "history", now=1.0)
   123	            for i in range(8):
   124	                add_flag(conn, hist, f"f_h{i}", status="dismiss")
   125	        cid = DB.create_case(conn, G.raw(case), now=1.0)
   126	        def extract(u):
   127	            ex = G.record(case, wr(u, case)[0])["excerpt"].split(". ")[0].rstrip(".") + "."
   128	            return dict(summary=ex, excerpt=ex)
   129	        PL.run_pipeline(conn, cid, G.raw(case), call=FakeCall(sample_script() if case == "sample" else sample_script(extract=extract)), now=lambda: 1.0)
   130	        view = {k: [(i["id"], i.get("category"), i["state"], i["review_status"]) for i in DB.list_items(conn, cid, k)] for k in ("entry", "amount", "flag")}
   131	        DP.suggest(conn, cid, local=True)                          # computing suggestions after the run must not matter either
   132	        assert {k: [(i["id"], i.get("category"), i["state"], i["review_status"]) for i in DB.list_items(conn, cid, k)] for k in view} == view
   133	        return view
   134	    assert run(False) == run(True)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:28.503Z

**tool call — Bash**
````
{
 "command": "for f in app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py; do echo \"== $f\"; git show f667f08:$f | diff - $f && echo same; done; echo ----; grep -rn \"date_convention\\|dismissal_patterns\\|dismissal_suggestions\" app tests tools evals --include=*.py --include=*.js --include=*.html | grep -v \"^app/backend/date_convention.py\\|^app/backend/dismissal_patterns.py\"",
 "description": "Compare committed vs on-disk card files and find all references"
}
````

### User / tool · 2026-11-02T04:22:28.689Z

**tool result**
````
== app/backend/date_convention.py
same
== app/backend/dismissal_patterns.py
same
== tests/unit/test_date_convention.py
same
== tests/unit/test_dismissal_patterns.py
same
----
app/backend/api.py:23:from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
app/backend/api.py:499:    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
app/backend/present.py:4:from app.backend import confidence, date_convention, grounding, pdf_text, sentences, store, totals as T, why
app/backend/present.py:129:             "suggestion": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)
tests/unit/test_dismissal_patterns.py:5:from app.backend import dismissal_patterns as DP, pipeline as PL
tests/unit/test_dismissal_patterns.py:106:    r = c.get(f"/api/cases/{t}/dismissal_suggestions")
tests/unit/test_dismissal_patterns.py:108:    assert c.get("/api/cases/nope/dismissal_suggestions").status_code == 404
tests/unit/test_dismissal_patterns.py:109:    assert c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={}).status_code == 400
tests/unit/test_dismissal_patterns.py:110:    assert c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={"key": "phrase:zzz"}).status_code == 404
tests/unit/test_dismissal_patterns.py:112:    a = c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={"key": key})
tests/unit/test_date_convention.py:5:from app.backend import date_convention as DC, present
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:37.239Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 timeout 300 .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit -k \"date or dismiss or suggest\" 2>&1 | tail -60",
 "description": "Run the brief's scoped unit tests on the working tree",
 "timeout": 320000
}
````

### User / tool · 2026-11-02T04:22:37.327Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:37.934Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 timeout 300 .venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py -v 2>&1 | tail -45",
 "description": "Run the two card test files verbosely to list each test",
 "timeout": 320000
}
````

### User / tool · 2026-11-02T04:22:38.022Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:39.284Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit -k \"date or dismiss or suggest\" 2>&1 | tail -60",
 "description": "Run the brief's scoped unit tests on the working tree",
 "timeout": 320000
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:39.877Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py -v 2>&1 | tail -45",
 "description": "Run the two card test files verbosely to list each test",
 "timeout": 320000
}
````

### User / tool · 2026-11-02T04:22:47.037Z

**tool result**
````
........................................................................ [ 47%]
........................................................................ [ 95%]
.......                                                                  [100%]
151 passed, 1106 deselected in 7.28s
````

### User / tool · 2026-11-02T04:22:49.649Z

**tool result**
````
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/arsis/zlayt-pm-project/.venv/bin/python
rootdir: /Users/arsis/zlayt-pm-project
plugins: anyio-4.16.0
collecting ... collected 25 items

tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason PASSED [  4%]
tests/unit/test_date_convention.py::test_day_first_evidence_suggests_dd_mm PASSED [  8%]
tests/unit/test_date_convention.py::test_evidence_inside_record_text_counts_and_is_listed_up_to_two PASSED [ 12%]
tests/unit/test_date_convention.py::test_no_suggestion_without_evidence_or_with_mixed_evidence PASSED [ 16%]
tests/unit/test_date_convention.py::test_not_ambiguous_or_iso_dates_never_get_or_give_evidence PASSED [ 20%]
tests/unit/test_date_convention.py::test_two_digit_year_ambiguity_keeps_convention_but_no_iso PASSED [ 24%]
tests/unit/test_date_convention.py::test_suggestion_never_writes_and_is_not_a_confirmation PASSED [ 28%]
tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required PASSED [ 32%]
tests/unit/test_dismissal_patterns.py::test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss PASSED [ 36%]
tests/unit/test_dismissal_patterns.py::test_two_dismissals_are_not_enough PASSED [ 40%]
tests/unit/test_dismissal_patterns.py::test_ineligible_flags_are_never_suggested PASSED [ 44%]
tests/unit/test_dismissal_patterns.py::test_category_suggestion_after_five_dismissals_of_different_phrases PASSED [ 48%]
tests/unit/test_dismissal_patterns.py::test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself PASSED [ 52%]
tests/unit/test_dismissal_patterns.py::test_scope_is_this_case_unless_local_profile PASSED [ 56%]
tests/unit/test_dismissal_patterns.py::test_routes_and_demo_mode_isolation PASSED [ 60%]
tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_01_date_formats] PASSED [ 64%]
tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_02_gap_boundaries] PASSED [ 68%]
tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_03_rate_and_ocr] PASSED [ 72%]
tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_04_duplicates_no_amounts] PASSED [ 76%]
tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_05_provider_conflict] PASSED [ 80%]
tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_06_subtle_pre_existing] PASSED [ 84%]
tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_07_prompt_injection] PASSED [ 88%]
tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_08_diagnosis_temptation] PASSED [ 92%]
tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_09_nonvisit_hides_gap] PASSED [ 96%]
tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[sample] PASSED [100%]

============================== 25 passed in 2.16s ==============================
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:53.665Z

**tool call — Bash**
````
{
 "command": "du -sh --exclude=.venv --exclude=.git . 2>/dev/null; echo \"SCRATCH=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\"; ls -la \"$SCRATCH\" 2>&1 | head",
 "description": "Measure repo size and check scratchpad directory"
}
````

### User / tool · 2026-11-02T04:22:53.747Z

**tool result**
````
SCRATCH=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
ls: : No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:22:58.273Z

**tool call — Bash**
````
{
 "command": "ls -a; echo ----; cat pytest.ini setup.cfg pyproject.toml 2>/dev/null | head -30; echo ----; mkdir -p \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut\" && echo made",
 "description": "List repo top-level files and create scratch mutation directory"
}
````

### User / tool · 2026-11-02T04:22:58.418Z

**tool result**
````
.
..
.claude
.env
.git
.gitignore
.pytest_cache
.venv
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
data
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
----
----
made
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:23:02.028Z

**tool call — Bash**
````
{
 "command": "SCR=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut\"; cd /Users/arsis/zlayt-pm-project && rm -rf \"$SCR/base\" && mkdir -p \"$SCR/base\" && cp -R app tests evals data \"$SCR/base/\" && cp requirements*.txt \"$SCR/base/\" && ls \"$SCR/base\" && cd \"$SCR/base\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py 2>&1 | tail -3",
 "description": "Copy app, tests, evals into scratch and run card tests there",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:23:02.120Z

**tool result (error)**
````
Permission to use Bash with command SCR="/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut"; cd /Users/arsis/zlayt-pm-project && rm -rf "$SCR/base" && mkdir -p "$SCR/base" && cp -R app tests evals data "$SCR/base/" && cp requirements*.txt "$SCR/base/" && ls "$SCR/base" && cd "$SCR/base" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py 2>&1 has been denied.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:23:05.276Z

**tool call — Bash**
````
{
 "command": "cp -R app tests evals data \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut/\" && echo copied",
 "description": "Copy app, tests, evals, data into scratch mutation directory",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:23:06.359Z

**tool result**
````
copied
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:23:27.893Z

**tool call — Bash**
````
{
 "command": "grep -n \"confirm_date\\|DATE_UNCONFIRMED\\|date_invalid\\|def local_mode\\|local_mode\\s*=\" app/backend/*.py | head -40",
 "description": "Locate confirm_date, DATE_UNCONFIRMED and local_mode logic"
}
````

### User / tool · 2026-11-02T04:23:28.001Z

**tool result**
````
app/backend/api.py:77:def local_mode() -> bool:
app/backend/api.py:401:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
app/backend/api.py:402:    async def confirm_date(token: str, rid: str, request: Request):
app/backend/api.py:409:            return review.confirm_date(c, token, rid, b["date"])
app/backend/api.py:501:    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
app/backend/date_convention.py:6:The suggestion is a hint the UI pre-selects; the paralegal still confirms once through confirm_date (D-041), and confirm_date still only
app/backend/dates.py:77:    """confirm_date hook (R-IN-5): the paralegal may only choose one of the code-proposed readings. Returns the confirmed date dict."""
app/backend/dates.py:79:        raise ValueError("date_invalid")
app/backend/gaps.py:63:    """Recompute after confirm_date: a flag whose record pair, dates and days are unchanged keeps its review status and note;
app/backend/case_extras.py:119:                    raise ApiError(422, "DATE_UNCONFIRMED", "Confirm the date of every undated entry first (Dates to confirm); nothing was changed.", {"rejected": e.rejected}) from None
app/backend/review.py:3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
app/backend/review.py:55:    return ReviewError(422, "DATE_UNCONFIRMED", message="Confirm this entry's date first (Dates to confirm). An entry with no confirmed date "
app/backend/review.py:171:# ---------------------------------------------------------------- confirm_date
app/backend/review.py:172:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
app/backend/review.py:181:        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
app/backend/review.py:197:    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t)
app/backend/review.py:217:def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t):
app/backend/review.py:222:                 (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))
app/backend/trace.py:42:    "DATE_UNCONFIRMED": "This entry's date is not confirmed, so it cannot be accepted into the letter yet.",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:23:29.543Z

**tool call — Bash**
````
{
 "command": "sed -n 45,60p app/backend/review.py; echo ----; sed -n 171,200p app/backend/review.py; echo ----; sed -n 70,90p app/backend/dates.py; echo ----; sed -n 75,82p app/backend/api.py; echo ----; sed -n 398,412p app/backend/api.py; echo ----; grep -n \"DATE_UNCONFIRMED\" -B6 app/backend/case_extras.py | head -30",
 "description": "Read confirm_date, D-041 block, and local_mode definitions"
}
````

### User / tool · 2026-11-02T04:23:29.732Z

**tool result**
````
    if kind != "entry":
        return False
    if not item.get("date_iso"):
        return True
    rid = (item.get("record_ids") or [None])[0]
    row = conn.execute("SELECT date_status FROM records WHERE id=? AND case_id=?", (rid, case_id)).fetchone()
    return bool(row) and row["date_status"] not in ("parsed", "confirmed", None)


def _date_unconfirmed_error():
    return ReviewError(422, "DATE_UNCONFIRMED", message="Confirm this entry's date first (Dates to confirm). An entry with no confirmed date "
                       "cannot be accepted into the letter.")


def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
----
# ---------------------------------------------------------------- confirm_date
def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
    t = _now(now)
    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
    if row is None:
        raise ReviewError(404, "not_found", message="No such record.")
    rec = DB._decode(row)
    if rec["date_status"] != "ambiguous":
        raise _bad("Only a record whose date can be read two ways can be confirmed.")
    if date_iso not in (rec["date_candidates"] or []):
        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
    moved, cleared = None, []
    for e in DB.list_items(conn, case_id, "entry"):
        if record_id in (e["record_ids"] or []):
            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso, **_without_date_doubt(e))
            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
                cleared.append(e["id"])
            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
    for a in DB.list_items(conn, case_id, "amount"):
        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
            DB.update_item(conn, a["id"], now=t, case=case_id, **_without_date_doubt(a))
            cleared.append(a["id"])
    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
    removed += _recompute_gaps(conn, case_id, t)
    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t)
    from app.backend import present
    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
----

def days_between(a_iso: str, b_iso: str) -> int:
    """Calendar days from a to b (real calendar, leap years included)."""
    return (_dt.date.fromisoformat(b_iso) - _dt.date.fromisoformat(a_iso)).days


def confirm(parsed: dict, chosen_iso: str) -> dict:
    """confirm_date hook (R-IN-5): the paralegal may only choose one of the code-proposed readings. Returns the confirmed date dict."""
    if parsed.get("status") != "ambiguous" or chosen_iso not in parsed.get("candidates", []):
        raise ValueError("date_invalid")
    return {**parsed, "status": "confirmed", "iso": chosen_iso}


_MONTH_RE = "|".join(sorted((k for k in MONTHS), key=len, reverse=True))
_FIND = re.compile(
    r"\b\d{4}-\d{2}-\d{2}\b"
    r"|\b\d{1,2}[/-]\d{1,2}[/-](?:\d{4}|\d{2})\b"
    rf"|\b(?:{_MONTH_RE})[a-z]*\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}\b"
    rf"|\b\d{{1,2}}(?:st|nd|rd|th)?\s+(?:of\s+)?(?:{_MONTH_RE})[a-z]*\.?,?\s+\d{{4}}\b", re.IGNORECASE)


----


def local_mode() -> bool:
    return os.environ.get("ZLAYT_MODE") == "local"


def is_loopback_peer(request) -> bool:
    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
----
        finally:
            c.close()

    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
    async def confirm_date(token: str, rid: str, request: Request):
        b = await body_of(request)
        if not isinstance(b.get("date"), str):
            raise ApiError(400, "bad_request", "Provide the chosen date.")
        c = conn()
        try:
            get_case(c, token)
            return review.confirm_date(c, token, rid, b["date"])
        finally:
            c.close()

----
113-            try:
114-                return apply_batch(c, token, b, now())
115-            except ValueError:
116-                raise ApiError(400, "bad_request", "Send an action (accept or reset) and a list of entry ids.") from None
117-            except BatchRefused as e:
118-                if any(r["reason"] == "date_unconfirmed" for r in e.rejected):     # D-041: same code as a single accept
119:                    raise ApiError(422, "DATE_UNCONFIRMED", "Confirm the date of every undated entry first (Dates to confirm); nothing was changed.", {"rejected": e.rejected}) from None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:23:33.242Z

**tool call — Bash**
````
{
 "command": "cat -n evals/golden/case_01_date_formats.txt | head -80",
 "description": "Read golden case_01 date formats input text"
}
````

### User / tool · 2026-11-02T04:23:33.337Z

**tool result**
````
     1	SYNTHETIC — invented for evaluation; not real patient data
     2	
     3	=== Record 1 ===
     4	Date: 2026-02-03
     5	Source: Quillfeather Urgent Care
     6	Excerpt: "Right ankle swelling after twisting on stairs. X-ray negative for fracture. Urgent care charge: $310.00."
     7	
     8	=== Record 2 ===
     9	Date: 02/17/2026
    10	Source: Dr. Orla Pennywhistle, primary care
    11	Excerpt: "Ankle swelling improved. Refer to physical therapy 1x/week for 4 weeks."
    12	
    13	=== Record 3 ===
    14	Date: Feb 24, 2026
    15	Source: Pemberwick Physical Therapy, visit 1
    16	Excerpt: "Gait mildly antalgic. Pain 4/10."
    17	
    18	=== Record 4 ===
    19	Date: 3 March 2026
    20	Source: Pemberwick Physical Therapy, visit 2
    21	Excerpt: "Pain 3/10. Balance exercises added."
    22	
    23	=== Record 5 ===
    24	Date: March 10th, 2026
    25	Source: Pemberwick Physical Therapy, visit 3
    26	Excerpt: "Pain 2/10. Walking without a limp."
    27	
    28	=== Record 6 ===
    29	Date: 03-17-26
    30	Source: Pemberwick Physical Therapy, visit 4
    31	Excerpt: "Pain 1/10. Discharged to home exercise program."
    32	
    33	=== Record 7 ===
    34	Date: 3/25/26
    35	Source: Dr. Orla Pennywhistle, primary care
    36	Excerpt: "Ankle exam normal. Optional recheck on 04/14/2026 if symptoms return."
    37	
    38	=== Record 8 ===
    39	Date: 04/05/2026
    40	Source: Dr. Orla Pennywhistle, phone note
    41	Excerpt: "Patient reports no new symptoms."
    42
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:23:45.097Z

**tool call — Bash**
````
{
 "command": "grep -n \"def run_pipeline\" -A6 app/backend/pipeline.py | head -20; echo ----; grep -n \"return\" app/backend/pipeline.py | tail -5; echo ----; grep -n \"CREATE TABLE IF NOT EXISTS flags\\|CREATE TABLE flags\\|flags\" app/db/*.py app/db/*.sql 2>/dev/null | head -10; echo ----; grep -n \"def list_items\\|def apply_review\\|def add_item\" -A4 app/db/db.py | head -40",
 "description": "Inspect pipeline return path, flags schema, and DB helpers"
}
````

### User / tool · 2026-11-02T04:23:45.241Z

**tool result**
````
260:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
261-    clock = now if callable(now) else (lambda: time.time() if now is None else now)
262-    t0 = clock()
263-    call = call or AU.make_call(conn, cid, now=clock)
264-    errors, stage_done = [], []
265-
266-    def set_stage(name):
----
464:    return TT.usd(c)
485:    return "\n".join(L)
499:        return 1
504:        return 1
513:    return 0 if out["status"] in ("done", "done_with_errors") else 1
----
app/db/db.py:21:_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
app/db/db.py:22:_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
app/db/db.py:24:_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
app/db/schema.sql:36:CREATE TABLE IF NOT EXISTS flags (
app/db/schema.sql:63:CREATE INDEX IF NOT EXISTS ix_flags_case ON flags(case_id);
----
114:def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
115-    """Insert an entry/amount/flag. payload keys must be column names (dicts/lists JSON-encoded). New items are pending."""
116-    if kind not in _ITEM_TABLES:
117-        raise ValueError(f"unknown item kind {kind!r}")
118-    table, prefix = _ITEM_TABLES[kind]
--
159:def list_items(conn, case_id: str, kind: str) -> list:
160-    table = _ITEM_TABLES[kind][0]
161-    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]
162-
163-
--
179:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
180-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
181-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
182-    if action not in ACTIONS:
183-        raise ValueError(f"invalid review action {action!r}")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:23:47.556Z

**tool call — Bash**
````
{
 "command": "grep -n '\"flag\"' app/backend/pipeline.py | head; echo ----; sed -n 440,460p app/backend/pipeline.py | head -5; grep -n \"^    return {\" app/backend/pipeline.py | head; echo ----; grep -n \"def main\\|__main__\" app/backend/pipeline.py | head",
 "description": "Find where pipeline writes flags and its return statement"
}
````

### User / tool · 2026-11-02T04:23:47.691Z

**tool result**
````
117:    if not any(i["review_status"] != "pending" for k in ("entry", "amount", "flag") for i in DB.list_items(conn, cid, k)):
187:    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
199:        if kind == "flag" and old["review_status"] != "pending":
217:    _persist(conn, cid, "flag", ing["flags"], now)
370:    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
----
    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
        conn, cid, call = _scratch_call(tmp, IN.normalize_text(text))
        with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
            out = run_pipeline(conn, cid, text, call=call)
        view = case_view(out)
27:    return {k: v for k, v in d.items() if not k.startswith("_")}
31:    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
96:    return {"text": text, "records": recs, "groups": ing["groups"], "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "split_detail": ing.get("split_detail"), "banner": ing["banner"],
103:    return {"id": item_id or a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
179:    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
381:    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
402:    return {"records": out["records"], "entries": out["entries"], "undated_entries": out["undated_entries"],
----
488:def main(argv=None) -> int:
516:if __name__ == "__main__":
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:24:06.518Z

**tool call — Bash**
````
{
 "command": "sed -n 360,372p app/backend/pipeline.py; echo ----; grep -n \"def _persist\" -A3 app/backend/pipeline.py | head -6; echo ----; grep -rn \"user\\|email\\|identity\\|account\" app/backend/dismissal_patterns.py app/backend/date_convention.py | head; echo ----; grep -n \"def add_routes\" -A3 app/backend/case_extras.py | head -4; echo ----; grep -n \"CATEGORY_MIN\\|PHRASE_MIN\" -r app tests | head",
 "description": "Inspect pipeline flag persistence, identity fields, and threshold usage"
}
````

### User / tool · 2026-11-02T04:24:06.696Z

**tool result**
````
    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
    flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
    final_amounts = [_clean(a) for a in final_amounts]
    damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
    from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
    now_t = clock()
    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
    _persist(conn, cid, "amount", final_amounts, now_t)
    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
    if timed_out:
        status = "timeout"
----
184:def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
185-    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
186-    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
187-    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
----
app/backend/dismissal_patterns.py:3:The tool has one local profile: no accounts, no users, no auth. "Profile" means this machine's database, so the history is the set of flags
----
106:def add_routes(app, *, conn, get_case, body_of, ApiError, now):
107-    @app.post("/api/cases/{token}/review/batch")
108-    async def review_batch(token: str, request: Request):
109-        b = await body_of(request)
----
app/backend/dismissal_patterns.py:7:When the same lexicon phrase (PHRASE_MIN dismissals) or the same category (CATEGORY_MIN) has been dismissed repeatedly, the review screen
app/backend/dismissal_patterns.py:20:PHRASE_MIN = 3
app/backend/dismissal_patterns.py:21:CATEGORY_MIN = 5
app/backend/dismissal_patterns.py:63:    for pid in sorted({p for _, p, _ in pend if p and phrase_n.get(p, 0) >= PHRASE_MIN}):
app/backend/dismissal_patterns.py:68:    for cat in sorted({f["category"] for f, _, _ in pend if cat_n.get(f["category"], 0) >= CATEGORY_MIN}):
app/backend/dismissal_patterns.py:97:            return {"suggestions": suggest(c, token, local=local_mode()), "min_phrase": PHRASE_MIN, "min_category": CATEGORY_MIN}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:24:19.176Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mutate.py",
 "content": "\"\"\"Mutation runner for T-088/T-089. Edits ONLY the scratch copy under MUT; the repo is never touched.\nEach mutant: (name, relative file, old text, new text, expectation). Runs the two card test files, restores the file, reports.\"\"\"\nimport os\nimport subprocess\nimport sys\n\nMUT = sys.argv[1]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nTESTS = [\"tests/unit/test_date_convention.py\", \"tests/unit/test_dismissal_patterns.py\"]\n\nMUTANTS = [\n    (\"88a mixed evidence not refused (first order wins by sort)\", \"app/backend/date_convention.py\",\n     \"    if len(orders) != 1:\\n        return None\", \"    if not orders:\\n        return None\",\n     \"expect fail\"),\n    (\"88a2 mixed evidence pick order by sort\", \"app/backend/date_convention.py\",\n     \"    order = next(iter(orders))\", \"    order = sorted(orders)[0]\", \"expect fail (paired with 88a)\"),\n    (\"88b ambiguous dates counted as evidence (MDY)\", \"app/backend/date_convention.py\",\n     \"            order = _order(int(m[1]), int(m[3]))\\n            key\", \"            order = _order(int(m[1]), int(m[3])) or 'MDY'\\n            key\",\n     \"expect fail\"),\n    (\"88c reason quotes a fabricated date\", \"app/backend/date_convention.py\",\n     'def _example(ev):\\n    return f\"({ev[\\'raw\\']})\"', 'def _example(ev):\\n    return \"(01/01/2026)\"',\n     \"expect fail\"),\n    (\"88d iso month/day swapped\", \"app/backend/date_convention.py\",\n     \"    mo, d = (a, b) if order == \\\"MDY\\\" else (b, a)\", \"    mo, d = (b, a) if order == \\\"MDY\\\" else (a, b)\",\n     \"expect fail\"),\n    (\"88e suggestion auto-confirmed on read (DB write in dates_to_confirm)\", \"app/backend/present.py\",\n     \"    recs = list(_recs_by_id(conn, case_id).values())\\n\",\n     \"    recs = list(_recs_by_id(conn, case_id).values())\\n\"\n     \"    from app.backend import date_convention as _DCM\\n\"\n     \"    for _r in recs:\\n\"\n     \"        _s = _DCM.suggest(_r, recs, DB.get_case(conn, case_id)['raw_text']) if _r['date_status']=='ambiguous' else None\\n\"\n     \"        if _s and _s['iso']:\\n\"\n     \"            conn.execute(\\\"UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?\\\", (_s['iso'], _r['id'], case_id))\\n\"\n     \"    recs = list(_recs_by_id(conn, case_id).values())\\n\",\n     \"expect fail (write + confirm)\"),\n    (\"89a phrase threshold 3 -> 2\", \"app/backend/dismissal_patterns.py\", \"PHRASE_MIN = 3\", \"PHRASE_MIN = 2\", \"expect fail\"),\n    (\"89b category threshold 5 -> 4 (boundary)\", \"app/backend/dismissal_patterns.py\", \"CATEGORY_MIN = 5\", \"CATEGORY_MIN = 4\",\n     \"predict: NOT caught (no 4-dismissal negative test)\"),\n    (\"89c bulk-applied flags counted as new dismissals (self-reinforcement)\", \"app/backend/dismissal_patterns.py\",\n     'if _eligible(f) and (f.get(\"reviewer_note\") or \"\") != APPLIED_NOTE]', 'if _eligible(f)]', \"expect fail\"),\n    (\"89d ineligible gap type added to eligibility\", \"app/backend/dismissal_patterns.py\",\n     'ELIGIBLE_TYPES = (\"pre_existing\", \"causation\")', 'ELIGIBLE_TYPES = (\"pre_existing\", \"causation\", \"gap\")', \"expect fail\"),\n    (\"89e suggest() writes: dismisses matching pending flags on read\", \"app/backend/dismissal_patterns.py\",\n     \"    return out\\n\\n\\ndef _row\",\n     \"    for _s in out:\\n        for _fid in _s['flag_ids']:\\n            conn.execute(\\\"UPDATE flags SET review_status='dismissed' WHERE id=?\\\", (_fid,))\\n    return out\\n\\n\\ndef _row\",\n     \"expect fail\"),\n    (\"89f GET route auto-applies suggestions (no click)\", \"app/backend/dismissal_patterns.py\",\n     '            return {\"suggestions\": suggest(c, token, local=local_mode()), \"min_phrase\"',\n     '            for _s in suggest(c, token, local=local_mode()):\\n                apply(c, token, _s[\"key\"], local=local_mode(), now=now)\\n            return {\"suggestions\": suggest(c, token, local=local_mode()), \"min_phrase\"',\n     \"expect fail\"),\n    (\"89g local scope ignored in history (cross-case counts in case scope)\", \"app/backend/dismissal_patterns.py\",\n     'rows = conn.execute(\"SELECT * FROM flags WHERE review_status=\\'dismissed\\'\" + (\"\" if local else \" AND case_id=?\"), () if local else (case_id,)).fetchall()',\n     'rows = conn.execute(\"SELECT * FROM flags WHERE review_status=\\'dismissed\\'\").fetchall()',\n     \"expect fail\"),\n    (\"89h route forces local scope (demo token would see other cases)\", \"app/backend/api.py\",\n     \"dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)\",\n     \"dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=lambda: True)\",\n     \"predict: NOT caught (no route test with another case's history in non-local mode)\"),\n    (\"89i dismissal history feeds pipeline flags (pipeline output changes)\", \"app/backend/pipeline.py\",\n     \"    _persist(conn, cid, \\\"flag\\\", flag_items + [f for f in tray if \\\"summary\\\" not in f], now_t)\",\n     \"    from app.backend import dismissal_patterns as _DPM\\n    _hc = {f[\\\"category\\\"] for f in _DPM._history(conn, cid, True)}\\n\"\n     \"    flag_items = [f for f in flag_items if f.get(\\\"category\\\") not in _hc]\\n\"\n     \"    _persist(conn, cid, \\\"flag\\\", flag_items + [f for f in tray if \\\"summary\\\" not in f], now_t)\",\n     \"expect fail (golden identity test)\"),\n]\n\n\ndef run_tests():\n    p = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\"] + TESTS, cwd=MUT,\n                       capture_output=True, text=True, env={**os.environ, \"PYTHONDONTWRITEBYTECODE\": \"1\"})\n    last = [l for l in p.stdout.strip().splitlines() if l.strip()][-1]\n    failed = [l.split(\"::\", 1)[1].split(\" \")[0] for l in p.stdout.splitlines() if l.startswith(\"FAILED\")]\n    return p.returncode, last, failed\n\n\ndef main():\n    base_rc, base_last, base_failed = run_tests()\n    print(f\"BASELINE rc={base_rc} :: {base_last}\")\n    for name, rel, old, new, expect in MUTANTS:\n        path = os.path.join(MUT, rel)\n        with open(path, encoding=\"utf-8\") as fh:\n            orig = fh.read()\n        n = orig.count(old)\n        if n != 1:\n            print(f\"MUTANT {name}: ANCHOR COUNT {n} (must be 1) -> not applied\")\n            continue\n        try:\n            with open(path, \"w\", encoding=\"utf-8\") as fh:\n                fh.write(orig.replace(old, new, 1))\n            rc, last, failed = run_tests()\n        finally:\n            with open(path, \"w\", encoding=\"utf-8\") as fh:\n                fh.write(orig)\n        verdict = \"CAUGHT\" if rc != 0 else \"NOT CAUGHT\"\n        print(f\"MUTANT {name} [{expect}] -> {verdict} :: {last}\")\n        for f in failed[:4]:\n            print(f\"    failed: {f}\")\n    # restored check\n    rc, last, _ = run_tests()\n    print(f\"RESTORED rc={rc} :: {last}\")\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T04:24:19.242Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mutate.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:24:30.333Z

The write guard blocks the script file in the scratchpad. I'll keep the mutation copy and runner under the allowed `artifacts/review-evidence/` path instead.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:24:31.151Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-088-T-089/mut && cp -R app tests evals data artifacts/review-evidence/T-088-T-089/mut/ && cp requirements.txt artifacts/review-evidence/T-088-T-089/mut/ && du -sh artifacts/review-evidence/T-088-T-089/mut && ls artifacts/review-evidence/T-088-T-089/mut",
 "description": "Create a scratch mutation copy under the allowed review-evidence path",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:24:31.795Z

**tool result**
````
 16M	artifacts/review-evidence/T-088-T-089/mut
app
data
evals
requirements.txt
tests
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:24:40.757Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089/mutate.py",
 "content": "\"\"\"Mutation runner for T-088 / T-089 (staff-engineer-reviewer). Edits ONLY the copy under MUT, never the repo.\nEach mutant: (name, relative file, old text, new text, expectation). Runs the two card test files, restores the file after each run.\"\"\"\nimport os\nimport subprocess\nimport sys\n\nMUT = sys.argv[1]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nTESTS = [\"tests/unit/test_date_convention.py\", \"tests/unit/test_dismissal_patterns.py\"]\n\nMUTANTS = [\n    (\"88a mixed evidence not refused\", \"app/backend/date_convention.py\",\n     \"    if len(orders) != 1:\\n        return None\", \"    if not orders:\\n        return None\",\n     \"expect fail\"),\n    (\"88a2 mixed evidence: order picked by sort (paired with 88a)\", \"app/backend/date_convention.py\",\n     \"    order = next(iter(orders))\", \"    order = sorted(orders)[0]\", \"expect fail\"),\n    (\"88b ambiguous dates counted as evidence (MDY)\", \"app/backend/date_convention.py\",\n     \"            order = _order(int(m[1]), int(m[3]))\\n            key\", \"            order = _order(int(m[1]), int(m[3])) or 'MDY'\\n            key\",\n     \"expect fail\"),\n    (\"88c reason quotes a fabricated date\", \"app/backend/date_convention.py\",\n     \"def _example(ev):\\n    return f\\\"({ev['raw']})\\\"\", \"def _example(ev):\\n    return \\\"(01/01/2026)\\\"\",\n     \"expect fail\"),\n    (\"88d iso month/day swapped\", \"app/backend/date_convention.py\",\n     \"    mo, d = (a, b) if order == \\\"MDY\\\" else (b, a)\", \"    mo, d = (b, a) if order == \\\"MDY\\\" else (a, b)\",\n     \"expect fail\"),\n    (\"88e suggestion auto-confirmed on read (DB write in dates_to_confirm)\", \"app/backend/present.py\",\n     \"    recs = list(_recs_by_id(conn, case_id).values())\\n\",\n     \"    recs = list(_recs_by_id(conn, case_id).values())\\n\"\n     \"    from app.backend import date_convention as _DCM\\n\"\n     \"    for _r in recs:\\n\"\n     \"        _s = _DCM.suggest(_r, recs, DB.get_case(conn, case_id)['raw_text']) if _r['date_status']=='ambiguous' else None\\n\"\n     \"        if _s and _s['iso']:\\n\"\n     \"            conn.execute(\\\"UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?\\\", (_s['iso'], _r['id'], case_id))\\n\"\n     \"    recs = list(_recs_by_id(conn, case_id).values())\\n\",\n     \"expect fail (write + confirm)\"),\n    (\"89a phrase threshold 3 -> 2\", \"app/backend/dismissal_patterns.py\", \"PHRASE_MIN = 3\", \"PHRASE_MIN = 2\", \"expect fail\"),\n    (\"89b category threshold 5 -> 4 (boundary)\", \"app/backend/dismissal_patterns.py\", \"CATEGORY_MIN = 5\", \"CATEGORY_MIN = 4\",\n     \"predict: NOT caught\"),\n    (\"89c bulk-applied flags counted as new dismissals\", \"app/backend/dismissal_patterns.py\",\n     \"if _eligible(f) and (f.get(\\\"reviewer_note\\\") or \\\"\\\") != APPLIED_NOTE]\", \"if _eligible(f)]\", \"expect fail\"),\n    (\"89d gap type made eligible\", \"app/backend/dismissal_patterns.py\",\n     'ELIGIBLE_TYPES = (\"pre_existing\", \"causation\")', 'ELIGIBLE_TYPES = (\"pre_existing\", \"causation\", \"gap\")', \"expect fail\"),\n    (\"89e suggest() writes: dismisses matching pending flags on read\", \"app/backend/dismissal_patterns.py\",\n     \"    return out\\n\\n\\ndef _row\",\n     \"    for _s in out:\\n        for _fid in _s['flag_ids']:\\n            conn.execute(\\\"UPDATE flags SET review_status='dismissed' WHERE id=?\\\", (_fid,))\\n    return out\\n\\n\\ndef _row\",\n     \"expect fail\"),\n    (\"89f GET route auto-applies suggestions (no click)\", \"app/backend/dismissal_patterns.py\",\n     \"            return {\\\"suggestions\\\": suggest(c, token, local=local_mode()), \\\"min_phrase\\\"\",\n     \"            for _s in suggest(c, token, local=local_mode()):\\n                apply(c, token, _s[\\\"key\\\"], local=local_mode(), now=now)\\n            return {\\\"suggestions\\\": suggest(c, token, local=local_mode()), \\\"min_phrase\\\"\",\n     \"expect fail\"),\n    (\"89g case scope ignored: history counts all cases\", \"app/backend/dismissal_patterns.py\",\n     \"    rows = conn.execute(\\\"SELECT * FROM flags WHERE review_status='dismissed'\\\" + (\\\"\\\" if local else \\\" AND case_id=?\\\"), () if local else (case_id,)).fetchall()\",\n     \"    rows = conn.execute(\\\"SELECT * FROM flags WHERE review_status='dismissed'\\\").fetchall()\",\n     \"expect fail\"),\n    (\"89h route forces local scope (demo token would count other cases)\", \"app/backend/api.py\",\n     \"now=time.time, local_mode=local_mode)   # T-089\", \"now=time.time, local_mode=lambda: True)   # T-089\",\n     \"predict: NOT caught\"),\n    (\"89i dismissal history feeds pipeline flags\", \"app/backend/pipeline.py\",\n     \"    _persist(conn, cid, \\\"flag\\\", flag_items + [f for f in tray if \\\"summary\\\" not in f], now_t)\",\n     \"    from app.backend import dismissal_patterns as _DPM\\n    _hc = {f[\\\"category\\\"] for f in _DPM._history(conn, cid, True)}\\n\"\n     \"    flag_items = [f for f in flag_items if f.get(\\\"category\\\") not in _hc]\\n\"\n     \"    _persist(conn, cid, \\\"flag\\\", flag_items + [f for f in tray if \\\"summary\\\" not in f], now_t)\",\n     \"expect fail (golden identity test)\"),\n]\n\n\ndef run_tests():\n    env = {**os.environ, \"PYTHONDONTWRITEBYTECODE\": \"1\"}\n    p = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\"] + TESTS, cwd=MUT,\n                       capture_output=True, text=True, env=env)\n    lines = [l for l in p.stdout.strip().splitlines() if l.strip()]\n    last = lines[-1] if lines else p.stderr.strip()[-200:]\n    failed = [l.split(\" \", 1)[0].replace(\"FAILED\", \"\").strip() for l in p.stdout.splitlines() if l.startswith(\"FAILED\")]\n    return p.returncode, last, failed\n\n\ndef main():\n    rc, last, _ = run_tests()\n    print(f\"BASELINE rc={rc} :: {last}\")\n    for name, rel, old, new, expect in MUTANTS:\n        path = os.path.join(MUT, rel)\n        with open(path, encoding=\"utf-8\") as fh:\n            orig = fh.read()\n        n = orig.count(old)\n        if n != 1:\n            print(f\"MUTANT {name}: ANCHOR COUNT {n} (need 1) -> NOT APPLIED\")\n            continue\n        try:\n            with open(path, \"w\", encoding=\"utf-8\") as fh:\n                fh.write(orig.replace(old, new, 1))\n            rc, last, failed = run_tests()\n        finally:\n            with open(path, \"w\", encoding=\"utf-8\") as fh:\n                fh.write(orig)\n        verdict = \"CAUGHT\" if rc != 0 else \"NOT CAUGHT\"\n        print(f\"MUTANT {name} [{expect}] -> {verdict} :: {last}\")\n        for f in failed[:5]:\n            print(f\"    failed: {f}\")\n    rc, last, _ = run_tests()\n    print(f\"RESTORED rc={rc} :: {last}\")\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-02T04:24:40.893Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089/mutate.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:24:42.419Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-088-T-089/mutate.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089/mut 2>&1 | tee artifacts/review-evidence/T-088-T-089/mutation_run.txt",
 "description": "Run the mutation suite in the scratch copy and record output",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:25:28.452Z

**tool result**
````
BASELINE rc=0 :: 25 passed in 2.54s
MUTANT 88a mixed evidence not refused [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.61s
    failed: 
MUTANT 88a2 mixed evidence: order picked by sort (paired with 88a) [expect fail] -> NOT CAUGHT :: 25 passed in 2.36s
MUTANT 88b ambiguous dates counted as evidence (MDY) [expect fail] -> CAUGHT :: 6 failed, 19 passed in 2.56s
    failed: 
    failed: 
    failed: 
    failed: 
    failed: 
MUTANT 88c reason quotes a fabricated date [expect fail] -> CAUGHT :: 4 failed, 21 passed in 2.64s
    failed: 
    failed: 
    failed: 
    failed: 
MUTANT 88d iso month/day swapped [expect fail] -> CAUGHT :: 3 failed, 22 passed in 2.64s
    failed: 
    failed: 
    failed: 
MUTANT 88e suggestion auto-confirmed on read (DB write in dates_to_confirm): ANCHOR COUNT 2 (need 1) -> NOT APPLIED
MUTANT 89a phrase threshold 3 -> 2 [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.12s
    failed: 
MUTANT 89b category threshold 5 -> 4 (boundary) [predict: NOT caught] -> NOT CAUGHT :: 25 passed in 2.67s
MUTANT 89c bulk-applied flags counted as new dismissals [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.48s
    failed: 
MUTANT 89d gap type made eligible [expect fail] -> NOT CAUGHT :: 25 passed in 2.51s
MUTANT 89e suggest() writes: dismisses matching pending flags on read [expect fail] -> CAUGHT :: 4 failed, 21 passed in 2.99s
    failed: 
    failed: 
    failed: 
    failed: 
MUTANT 89f GET route auto-applies suggestions (no click) [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.51s
    failed: 
MUTANT 89g case scope ignored: history counts all cases [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.61s
    failed: 
MUTANT 89h route forces local scope (demo token would count other cases) [predict: NOT caught] -> NOT CAUGHT :: 25 passed in 2.28s
MUTANT 89i dismissal history feeds pipeline flags [expect fail (golden identity test)] -> CAUGHT :: 1 failed, 24 passed in 2.47s
    failed: 
RESTORED rc=0 :: 25 passed in 2.48s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:47.079Z

Most mutants behave as expected. Two need fixing: the 88e anchor matches twice, and my failed-test name parser is wrong. I'll also add a probe that shows the real `reason` output on golden case_01.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:48.035Z

**tool call — Bash**
````
{
 "command": "grep -n \"in this record\\|two_digit\\|s\\[\\\"convention\\\"\\] == \\\"MDY\\\" and s\\[\\\"iso\\\"\\] is None\" tests/unit/test_date_convention.py; echo ----; grep -n \"in this record\" app/backend/date_convention.py; echo ----; grep -n \"def dates_to_confirm\" -A2 app/backend/present.py; echo ----; grep -n \"_s = _DCM\\|recs = list\" app/backend/present.py | head",
 "description": "Locate the reason wording and weak assertion line numbers"
}
````

### User / tool · 2026-11-02T04:25:48.145Z

**tool result**
````
32:    assert s["reason"] == "Other dates in this record use month first (03/14/2026)"
46:    assert s["reason"].startswith("3 other dates in this record use month first (06/25/2026) and (07/30/2026)")
62:def test_two_digit_year_ambiguity_keeps_convention_but_no_iso():
65:    assert s["convention"] == "MDY" and s["iso"] is None or s["iso"] in rows[1]["date_candidates"]
99:    assert s["evidence_count"] == 4 and s["reason"] == "4 other dates in this record use month first (02/17/2026) and (03-17-26)"
----
64:    reason = (f"Other dates in this record use {first} {_example(shown[0])}" if n == 1 else
65:              f"{n} other dates in this record use {first} " + " and ".join(_example(e) for e in shown))
----
131:def dates_to_confirm(conn, case_id):
132-    recs = list(_recs_by_id(conn, case_id).values())
133-    raw = DB.get_case(conn, case_id)["raw_text"]
----
132:    recs = list(_recs_by_id(conn, case_id).values())
157:    recs = list(_recs_by_id(conn, case_id).values())
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:52.167Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089 && .venv_probe_placeholder 2>/dev/null; /usr/bin/env python3 - <<'EOF'\nimport re\np = \"mutate.py\"\nsrc = open(p, encoding=\"utf-8\").read()\nsrc = src.replace('''     \"    recs = list(_recs_by_id(conn, case_id).values())\\\\n\",\n     \"    recs = list(_recs_by_id(conn, case_id).values())\\\\n\"\n     \"    from app.backend import date_convention as _DCM\\\\n\"''',\n'''     \"def dates_to_confirm(conn, case_id):\\\\n    recs = list(_recs_by_id(conn, case_id).values())\\\\n\",\n     \"def dates_to_confirm(conn, case_id):\\\\n    recs = list(_recs_by_id(conn, case_id).values())\\\\n\"\n     \"    from app.backend import date_convention as _DCM\\\\n\"''')\nsrc = src.replace('''     \"    recs = list(_recs_by_id(conn, case_id).values())\\\\n\"\n     \"    recs = list(_recs_by_id(conn, case_id).values())\\\\n\",''', '''     \"    recs = list(_recs_by_id(conn, case_id).values())\\\\n\"\n     \"    recs = list(_recs_by_id(conn, case_id).values())\\\\n\",''')\nsrc = src.replace('failed = [l.split(\" \", 1)[0].replace(\"FAILED\", \"\").strip() for l in p.stdout.splitlines() if l.startswith(\"FAILED\")]',\n                  'failed = [l.split()[1] for l in p.stdout.splitlines() if l.startswith(\"FAILED\") and len(l.split()) > 1]')\n# extra mutants: origin rule removed (type rule alone is masked), and split 88a2 as equivalent-alone control\nsrc = src.replace('    (\"89h route forces local scope', '''    (\"89d2 origin (lexicon) requirement dropped\", \"app/backend/dismissal_patterns.py\",\n     'return f[\"type\"] in ELIGIBLE_TYPES and \"lexicon\" in (f.get(\"origin\") or \"\")', 'return f[\"type\"] in ELIGIBLE_TYPES',\n     \"expect fail\"),\n    (\"89h route forces local scope''')\nopen(p, \"w\", encoding=\"utf-8\").write(src)\nprint(\"88e anchor fixed:\", \"def dates_to_confirm(conn, case_id):\\\\n    recs\" in src, \"| 89d2 added:\", \"89d2\" in src, \"| name parser fixed:\", \"l.split()[1]\" in src)\nEOF",
 "description": "Patch mutation runner anchors and name parsing in the evidence copy"
}
````

### User / tool · 2026-11-02T04:25:52.276Z

**tool result**
````
88e anchor fixed: True | 89d2 added: True | name parser fixed: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:25:55.155Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-088-T-089/mutate.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089/mut 2>&1 | tee artifacts/review-evidence/T-088-T-089/mutation_run.txt",
 "description": "Re-run the corrected mutation suite and record output",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:26:47.250Z

**tool result**
````
BASELINE rc=0 :: 25 passed in 2.36s
MUTANT 88a mixed evidence not refused [expect fail] -> CAUGHT :: 1 failed, 24 passed in 3.99s
    failed: tests/unit/test_date_convention.py::test_no_suggestion_without_evidence_or_with_mixed_evidence
MUTANT 88a2 mixed evidence: order picked by sort (paired with 88a) [expect fail] -> NOT CAUGHT :: 25 passed in 2.67s
MUTANT 88b ambiguous dates counted as evidence (MDY) [expect fail] -> CAUGHT :: 6 failed, 19 passed in 2.31s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_day_first_evidence_suggests_dd_mm
    failed: tests/unit/test_date_convention.py::test_evidence_inside_record_text_counts_and_is_listed_up_to_two
    failed: tests/unit/test_date_convention.py::test_no_suggestion_without_evidence_or_with_mixed_evidence
    failed: tests/unit/test_date_convention.py::test_not_ambiguous_or_iso_dates_never_get_or_give_evidence
MUTANT 88c reason quotes a fabricated date [expect fail] -> CAUGHT :: 4 failed, 21 passed in 2.40s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_day_first_evidence_suggests_dd_mm
    failed: tests/unit/test_date_convention.py::test_evidence_inside_record_text_counts_and_is_listed_up_to_two
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
MUTANT 88d iso month/day swapped [expect fail] -> CAUGHT :: 3 failed, 22 passed in 2.56s
    failed: tests/unit/test_date_convention.py::test_month_first_evidence_suggests_mm_dd_with_reason
    failed: tests/unit/test_date_convention.py::test_day_first_evidence_suggests_dd_mm
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
MUTANT 88e suggestion auto-confirmed on read (DB write in dates_to_confirm) [expect fail (write + confirm)] -> CAUGHT :: 2 failed, 23 passed in 2.23s
    failed: tests/unit/test_date_convention.py::test_suggestion_never_writes_and_is_not_a_confirmation
    failed: tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
MUTANT 89a phrase threshold 3 -> 2 [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.61s
    failed: tests/unit/test_dismissal_patterns.py::test_two_dismissals_are_not_enough
MUTANT 89b category threshold 5 -> 4 (boundary) [predict: NOT caught] -> NOT CAUGHT :: 25 passed in 2.58s
MUTANT 89c bulk-applied flags counted as new dismissals [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.51s
    failed: tests/unit/test_dismissal_patterns.py::test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself
MUTANT 89d gap type made eligible [expect fail] -> NOT CAUGHT :: 25 passed in 2.39s
MUTANT 89e suggest() writes: dismisses matching pending flags on read [expect fail] -> CAUGHT :: 4 failed, 21 passed in 2.96s
    failed: tests/unit/test_dismissal_patterns.py::test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss
    failed: tests/unit/test_dismissal_patterns.py::test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself
    failed: tests/unit/test_dismissal_patterns.py::test_routes_and_demo_mode_isolation
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[sample]
MUTANT 89f GET route auto-applies suggestions (no click) [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.60s
    failed: tests/unit/test_dismissal_patterns.py::test_routes_and_demo_mode_isolation
MUTANT 89g case scope ignored: history counts all cases [expect fail] -> CAUGHT :: 1 failed, 24 passed in 2.36s
    failed: tests/unit/test_dismissal_patterns.py::test_scope_is_this_case_unless_local_profile
MUTANT 89d2 origin (lexicon) requirement dropped [expect fail] -> NOT CAUGHT :: 25 passed in 2.39s
MUTANT 89h route forces local scope (demo token would count other cases) [predict: NOT caught] -> NOT CAUGHT :: 25 passed in 2.18s
MUTANT 89i dismissal history feeds pipeline flags [expect fail (golden identity test)] -> CAUGHT :: 1 failed, 24 passed in 2.38s
    failed: tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[sample]
RESTORED rc=0 :: 25 passed in 2.41s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:26:52.970Z

Mutation results are in. Next, a probe to confirm the reason wording against the real golden case and check the two-digit-year assertion.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:26:56.617Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089/probe_t088.py",
 "content": "\"\"\"Probe for T-088 (staff-engineer-reviewer). Runs in the scratch copy; prints what the API returns for golden case_01 and\nchecks the reason's scope claim against the record each evidence date actually sits in. Read-only on the repo.\"\"\"\nimport json\nimport os\nimport sys\nimport tempfile\n\nMUT = sys.argv[1]\nsys.path.insert(0, MUT)\nos.chdir(MUT)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ.pop(\"ANTHROPIC_API_KEY\", None)\nos.environ.pop(\"ZLAYT_MODE\", None)\n\nfrom fastapi.testclient import TestClient  # noqa: E402\n\nfrom app.backend import date_convention as DC  # noqa: E402\nfrom app.backend.api import create_app  # noqa: E402\nfrom tests.unit import _golden as G  # noqa: E402\nfrom tests.unit.test_api_routes import run_case  # noqa: E402\nfrom tests.unit.test_date_convention import packet  # noqa: E402\n\nout_dir = tempfile.mkdtemp(prefix=\"t088probe-\")\ndb = os.path.join(out_dir, \"probe.sqlite\")\nc = TestClient(create_app(db, static_dir=out_dir))\nt = run_case(c, G.raw(\"case_01_date_formats\"))\ng = c.get(f\"/api/cases/{t}\").json()\nrecs = {r[\"id\"]: r for r in g[\"records\"]}\nprint(\"RECORDS:\", [(r[\"id\"], r.get(\"seq\"), r[\"date_raw\"], r[\"date_status\"]) for r in g[\"records\"]])\nfor d in g[\"dates_to_confirm\"]:\n    if d[\"raw\"] == \"04/05/2026\":\n        print(\"SUGGESTION_FOR_04/05/2026:\", json.dumps(d, indent=1))\n        ev_ids = sorted({e[\"record_id\"] for e in d[\"suggestion\"][\"evidence\"]})\n        print(\"AMBIGUOUS_RECORD:\", d[\"record_id\"], \"| evidence sits in records:\", ev_ids)\n        print(\"reason says 'in this record' ->\", \"this record\" in d[\"suggestion\"][\"reason\"],\n              \"| evidence record ids other than the ambiguous record:\", [i for i in ev_ids if i != d[\"record_id\"]])\n\n# two-digit-year case: the test's assertion is `A and B or C`; check what it really pins\nrows, raw = packet((\"03/14/2026\", \"x\"), (\"04/05/98\", \"y\"))\ns = DC.suggest(rows[1], rows, raw)\nprint(\"TWO_DIGIT_YEAR suggestion:\", s)\nprint(\"test expression value with convention forced wrong:\",\n      (\"DMY\" == \"MDY\" and s[\"iso\"] is None or s[\"iso\"] in rows[1][\"date_candidates\"]))\n"
}
````

### User / tool · 2026-11-02T04:26:56.711Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089/probe_t088.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:26:58.270Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089/mut && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python ../probe_t088.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089/mut 2>&1 | tee ../probe_t088_output.txt | head -80",
 "description": "Run the T-088 probe against golden case_01 in the scratch copy",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:26:59.255Z

**tool result**
````
RECORDS: [('r1', 1, '2026-02-03', 'parsed'), ('r2', 2, '02/17/2026', 'parsed'), ('r3', 3, 'Feb 24, 2026', 'parsed'), ('r4', 4, '3 March 2026', 'parsed'), ('r5', 5, 'March 10th, 2026', 'parsed'), ('r6', 6, '03-17-26', 'parsed'), ('r7', 7, '3/25/26', 'parsed'), ('r8', 8, '04/05/2026', 'ambiguous')]
SUGGESTION_FOR_04/05/2026: {
 "record_id": "r8",
 "raw": "04/05/2026",
 "candidates": [
  "2026-04-05",
  "2026-05-04"
 ],
 "status": "ambiguous",
 "suggestion": {
  "convention": "MDY",
  "label": "MM/DD",
  "iso": "2026-04-05",
  "reason": "4 other dates in this record use month first (02/17/2026) and (03-17-26)",
  "evidence": [
   {
    "record_id": "r2",
    "raw": "02/17/2026"
   },
   {
    "record_id": "r6",
    "raw": "03-17-26"
   }
  ],
  "evidence_count": 4,
  "auto_applied": false
 }
}
AMBIGUOUS_RECORD: r8 | evidence sits in records: ['r2', 'r6']
reason says 'in this record' -> True | evidence record ids other than the ambiguous record: ['r2', 'r6']
TWO_DIGIT_YEAR suggestion: {'convention': 'MDY', 'label': 'MM/DD', 'iso': None, 'reason': 'Other dates in this record use month first (03/14/2026)', 'evidence': [{'record_id': 'r1', 'raw': '03/14/2026'}], 'evidence_count': 1, 'auto_applied': False}
test expression value with convention forced wrong: False
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:27:16.604Z

The probe confirms the reason-scope problem on golden case_01. Next I'll check the index state for the four card files, the eval-case and UI parts of AC1, and the D-041 accept block.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:27:17.909Z

**tool call — Bash**
````
{
 "command": "git cat-file -e HEAD:app/backend/date_convention.py && echo \"HEAD has date_convention.py\"; git cat-file -e HEAD:tests/unit/test_dismissal_patterns.py && echo \"HEAD has test_dismissal_patterns.py\"; echo ----; git diff --cached --stat | tail -8; echo ----; git ls-files --stage -- app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py; echo \"(empty above means not in index)\"; echo ----; grep -rln \"suggestion\\|dismissal_suggestions\" evals/ | head; echo \"evals refs above (none = no eval case)\"; echo ----; grep -n \"DATE_UNCONFIRMED\" tests/unit/*.py | head -5",
 "description": "Check index state, HEAD presence, eval coverage, and D-041 test coverage"
}
````

### User / tool · 2026-11-02T04:27:18.096Z

**tool result**
````
HEAD has date_convention.py
HEAD has test_dismissal_patterns.py
----
 app/backend/date_convention.py        |  67 -----------------
 app/backend/dismissal_patterns.py     | 114 -----------------------------
 app/backend/present.py                |   9 +--
 app/llm/prompts/conflicts_v1.md       |  14 ----
 tests/unit/test_date_convention.py    | 103 --------------------------
 tests/unit/test_dismissal_patterns.py | 134 ----------------------------------
 6 files changed, 3 insertions(+), 438 deletions(-)
----
(empty above means not in index)
----
evals/library_build_v2.py
evals/golden/case_03_rate_and_ocr.expected.json
evals/library/case_lib09_spanish_interpreter_espalda.expected.json
evals refs above (none = no eval case)
----
tests/unit/test_trace.py:193:    assert c.post(f"/api/cases/{tok}/items/e5/review", json={"action": "accept"}).json()["error"]["code"] == "DATE_UNCONFIRMED"   # the trace and the rule agree
tests/unit/test_date_unconfirmed.py:42:    assert r.status_code == 422 and r.json()["error"]["code"] == "DATE_UNCONFIRMED"
tests/unit/test_date_unconfirmed.py:44:    assert r.status_code == 422 and r.json()["error"]["code"] == "DATE_UNCONFIRMED"
tests/unit/test_date_unconfirmed.py:57:    assert r.status_code == 422 and r.json()["error"]["code"] == "DATE_UNCONFIRMED"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:27:30.998Z

**tool call — Bash**
````
{
 "command": "echo \"== backend readers of suggestion fields\"; grep -rn \"suggestion\" app/backend app/db --include=*.py | grep -v \"^app/backend/date_convention.py\\|^app/backend/dismissal_patterns.py\"; echo \"== frontend mentions\"; grep -rln \"suggestion\\|dismissal\" app/frontend | head; echo \"== frontend pre-select / confirm-on-load lines\"; grep -rn \"suggestion\" app/frontend | head -10; echo \"== LLM imports in T-088/T-089 code\"; grep -n \"llm\\|call\\|anthropic\\|claude\" app/backend/date_convention.py app/backend/dismissal_patterns.py; echo \"== bare except / float / sleep\"; grep -n \"except\\|float(\\|sleep(\" app/backend/date_convention.py app/backend/dismissal_patterns.py; echo \"(end)\"",
 "description": "Grep for suggestion readers, frontend use, LLM calls and risky patterns"
}
````

### User / tool · 2026-11-02T04:27:31.126Z

**tool result**
````
== backend readers of suggestion fields
app/backend/present.py:135:             "suggestion": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)
== frontend mentions
== frontend pre-select / confirm-on-load lines
== LLM imports in T-088/T-089 code
app/backend/date_convention.py:49:    m = _NUM_DATE.fullmatch(" ".join(str(rec.get("date_raw") or "").split()))
app/backend/dismissal_patterns.py:9:never changes a pipeline result, a flag's state or its review_status. The paralegal's click calls apply(), which dismisses the matching
== bare except / float / sleep
app/backend/dismissal_patterns.py:111:            except KeyError:
(end)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:27:44.526Z

Both cards' code is confined to backend and the frontend has no suggestion UI yet. Before writing the reviews, I'll check for existing review files (write-once) and the memory notes on write-once and the blocker calibration.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:27:45.320Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -E \"T-088|T-089\" ; echo \"(end listing)\"; cat .claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md 2>/dev/null | head -30; echo ----; cat .claude/agent-memory/staff-engineer-reviewer/feedback_severity_vs_brief.md 2>/dev/null | head -20",
 "description": "Check existing review files and relevant reviewer memory notes"
}
````

### User / tool · 2026-11-02T04:27:45.414Z

**tool result**
````
(end listing)
---
name: feedback_review_write_once
description: reviews/*.md are append-only under reviewer-write-guard; proof-read the review body before the first Write, because Edit is blocked afterwards
metadata:
  type: feedback
---

Write a review file once, after proof-reading every line citation and every "I ran X" claim. Once `reviews/<card>-<persona>.md` exists, `Edit` on it is refused by reviewer-write-guard ("reviews are append-only — write a new file with a -r2/-r3 suffix"), so a typo in the body stays there.

**Why:** T-080 r2 (this session): I wrote `reviews/T-080-staff-engineer-r2.md` with three wrong body citations (a line number, an "export builder" pointer with no path, and an unverified "stable across GETs" claim). The JSON block was accurate, but the body could not be corrected in place.

**How to apply:** before the first Write of a review, grep every cited line number and re-check each "checked and fine" claim against a command you actually ran. If a correction is needed later, write a new suffixed file (`-r3`) and say so in the reply, not a silent overwrite. Do not try to get around the guard with shell writes.
----
---
name: severity-vs-brief
description: When the dispatch brief sets a default severity that conflicts with CONTRACT D.2 (for example "list mismatches as major"), rate per D.2 and state the deviation in the review
metadata:
  type: feedback
---

When the brief says to file a class of finding as a major, but the finding violates a spec constraint, rate it a blocker per CONTRACT D.2 (persona section 8) and say so in the review summary and in why_it_matters.

**Why:** T-063 brief said "list any mismatch as a major". The D-033 mismatch labelled a family member's statement as the patient's own self-report, which D-033 explicitly forbids. D.2 defines a spec-constraint violation as a blocker. I rated it a blocker, stated the deviation at the top of the review, and left the override to the orchestrator.

**How to apply:** for each finding, check the D.2 definition first; a brief's default is a starting point, not a cap. Put any deviation in the review's first paragraph so the orchestrator sees it without reading the JSON. Do not downgrade a finding to match a brief.

See also [[project_t063_doc_vs_code_review_patterns]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:27:59.546Z

No existing review files, so the write is first. Now I'll verify every line citation against the committed files before writing.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:28:02.360Z

**tool call — Bash**
````
{
 "command": "echo \"== committed line refs\"; git show f667f08:app/backend/api.py | grep -n \"dismissal_patterns.add_routes\"; git show f667f08:app/backend/present.py | grep -n \"date_convention.suggest\\|recs = list(_recs_by_id\"; git show f667f08:app/backend/date_convention.py | grep -n \"dates\\.\\|ev = _evidence\\|Other dates in this record\\|other dates in this record\\|def suggest\\|MAX_EVIDENCE = \"; git show f667f08:app/backend/dismissal_patterns.py | grep -n \"SELECT \\* FROM flags\\|!= APPLIED_NOTE\\|def _eligible\\|return f\\[\\\"type\\\"\\]\\|CATEGORY_MIN = \\|PHRASE_MIN = \\|ELIGIBLE_TYPES = \\|def apply\\|apply_review(conn\"; echo \"== committed tests refs\"; git show f667f08:tests/unit/test_date_convention.py | grep -n \"in this record\\|is None or s\\[\\\"iso\\\"\\]\\|def test_golden\\|def test_month_first\"; git show f667f08:tests/unit/test_dismissal_patterns.py | grep -n \"def test_routes\\|def test_category\\|def test_ineligible\\|origin\\|def test_scope\\|local_mode\\|^PHRASE\\|def test_three\"; echo \"== golden record lines\"; grep -n \"Date: 02/17/2026\\|Date: 03-17-26\\|Date: 04/05/2026\\|Patient reports no new symptoms\\|Date: 3/25/26\\|04/14/2026\" evals/golden/case_01_date_formats.txt; echo \"== working-tree frontend suggestion grep\"; grep -rn \"suggestion\" app/frontend | wc -l; echo \"== golden expected mention\"; grep -c \"suggestion\\|dismissal\" evals/golden/case_01_date_formats.expected.json; echo \"== index\"; git diff --cached --name-status | head -20",
 "description": "Verify all line citations against committed files and golden text"
}
````

### User / tool · 2026-11-02T04:28:02.584Z

**tool result**
````
== committed line refs
497:    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
126:    recs = list(_recs_by_id(conn, case_id).values())
129:             "suggestion": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)
149:    recs = list(_recs_by_id(conn, case_id).values())
7:accepts one of the code candidates. Nothing here writes to the database or changes a pipeline result."""
13:MAX_EVIDENCE = 2
44:def suggest(rec: dict, records: list, raw_text: str):
52:    ev = _evidence(records, raw_text)
64:    reason = (f"Other dates in this record use {first} {_example(shown[0])}" if n == 1 else
65:              f"{n} other dates in this record use {first} " + " and ".join(_example(e) for e in shown))
20:PHRASE_MIN = 3
21:CATEGORY_MIN = 5
22:ELIGIBLE_TYPES = ("pre_existing", "causation")
27:def _eligible(f) -> bool:
28:    return f["type"] in ELIGIBLE_TYPES and "lexicon" in (f.get("origin") or "")
43:    rows = conn.execute("SELECT * FROM flags WHERE review_status='dismissed'" + ("" if local else " AND case_id=?"), () if local else (case_id,)).fetchall()
44:    return [f for f in (DB._decode(r) for r in rows) if _eligible(f) and (f.get("reviewer_note") or "") != APPLIED_NOTE]
80:def apply(conn, case_id: str, key: str, *, local: bool = False, now=None) -> dict:
87:        review.apply_review(conn, case_id, fid, {"action": "dismiss", "note": APPLIED_NOTE}, now=now)
== committed tests refs
28:def test_month_first_evidence_suggests_mm_dd_with_reason():
32:    assert s["reason"] == "Other dates in this record use month first (03/14/2026)"
46:    assert s["reason"].startswith("3 other dates in this record use month first (06/25/2026) and (07/30/2026)")
65:    assert s["convention"] == "MDY" and s["iso"] is None or s["iso"] in rows[1]["date_candidates"]
81:            assert s["auto_applied"] is False and item["candidates"] and (s["iso"] is None or s["iso"] in item["candidates"])
89:def test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required(tmp_path, monkeypatch):
99:    assert s["evidence_count"] == 4 and s["reason"] == "4 other dates in this record use month first (02/17/2026) and (03-17-26)"
15:def add_flag(conn, case, fid, *, category="new_onset", text=NEW_ONSET, type_="causation", origin="lexicon+llm", status=None):
16:    DB.add_item(conn, case, "flag", {"id": fid, "type": type_, "category": category, "origin": origin, "title": "t", "explanation": "e",
26:def test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss(tmp_path):
46:def test_ineligible_flags_are_never_suggested(tmp_path):
49:        add_flag(conn, cid, f"f_g{i}", category="gap_over_30", type_="gap", origin="code", status="dismiss")
50:        add_flag(conn, cid, f"f_i{i}", category="injection_suspected", type_="record_warning", origin="code", status="dismiss")
54:def test_category_suggestion_after_five_dismissals_of_different_phrases(tmp_path):
84:def test_scope_is_this_case_unless_local_profile(tmp_path):
94:def test_routes_and_demo_mode_isolation(tmp_path, monkeypatch):
== golden record lines
9:Date: 02/17/2026
29:Date: 03-17-26
34:Date: 3/25/26
36:Excerpt: "Ankle exam normal. Optional recheck on 04/14/2026 if symptoms return."
39:Date: 04/05/2026
41:Excerpt: "Patient reports no new symptoms."
== working-tree frontend suggestion grep
       0
== golden expected mention
0
== index
D	app/backend/date_convention.py
D	app/backend/dismissal_patterns.py
M	app/backend/present.py
D	app/llm/prompts/conflicts_v1.md
D	tests/unit/test_date_convention.py
D	tests/unit/test_dismissal_patterns.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:28:32.731Z

Line citations check out. I'll write the T-088 review first, since reviews are write-once.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:28:49.516Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-088-staff-engineer.md",
 "content": "# T-088 review: date-convention suggestion (staff-engineer-reviewer)\n\n**Verdict: fail.** One blocker: the suggestion's `reason` says the evidence dates are \"in this record\" when they sit in other records of the packet. I rated it a blocker, not a major, under CONTRACT D.2 and CLAUDE.md non-negotiable 5 (every statement traces to the input). The code-only, never-applied and D-041 parts hold.\n\nScope: commit f667f08 (`app/backend/date_convention.py`, `app/backend/present.py:122-135`, `tests/unit/test_date_convention.py`, the T-088 contract section in `memory/contracts/api.md`). Cross-checked against D-041 and D-042 in `memory/ORCHESTRATOR_DECISIONS.md` (lines 49-50) and the golden sample `evals/golden/case_01_date_formats.txt`.\n\n**Checks against your four points**\n1. Code only: holds. `date_convention.py` imports only `re` and `dates`, with no LLM or call path. Mutation 88e (a DB write that auto-confirms the ISO reading) is caught by 2 tests.\n2. Never auto-applied, one confirm still required: holds. No server path reads `suggestion` except `present.py:129`, which only builds it. `review.confirm_date` (`review.py:172-181`) still takes the client's date and checks it against the candidates. The D-041 block reads `records.date_status`, not the suggestion (`review.py:45-50`).\n3. Reason quotes a real date from the packet: the quoted dates are real (`02/17/2026`, `03-17-26`), but the scope is wrong. See F1.\n4. Mixed or contradictory packets: `date_convention.py:54-55` returns `None` when the orders disagree or there is no evidence. Mutant 88a (mixed packets allowed through) is caught.\n\n**Exercised**\n- `python3 tools/board.py show T-088` and `show T-089`; `git show f667f08 --stat` and per-file diffs; `git show f667f08:<path>` for every file in scope; D-041/D-042 lines in `memory/ORCHESTRATOR_DECISIONS.md`.\n- `.venv/bin/python -m pytest -q tests/unit -k \"date or dismiss or suggest\"`: 151 passed, 1106 deselected. `pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py -v`: 25 passed.\n- Mutation suite in a scratch copy (`artifacts/review-evidence/T-088-T-089/mut`, runner `mutate.py`, output `mutation_run.txt`). Core rules 88a/88b/88c/88d/88e are all caught.\n- Probe on golden case_01 through FastAPI `TestClient` (no live server, no network, `LLM_BACKEND=fixture`): output in `artifacts/review-evidence/T-088-T-089/probe_t088_output.txt`.\n- `git diff --cached --name-status` and `git cat-file -e HEAD:<path>` (index state, see F3).\n- `grep -rn suggestion app/frontend` returned 0 matches. `grep -c \"suggestion\\|dismissal\" evals/golden/case_01_date_formats.expected.json` returned 0.\n\n```json\n{\"card\": \"T-088\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit f667f08: app/backend/date_convention.py, app/backend/present.py (dates_to_confirm), memory/contracts/api.md (T-088 section), tests/unit/test_date_convention.py; golden evals/golden/case_01_date_formats.txt; no live app URL (TestClient in-process)\",\n \"exercised\": [\"board.py show T-088 and T-089\", \"git show f667f08 --stat and per-file diffs\", \"git show f667f08:<path> for in-scope files\", \"memory/ORCHESTRATOR_DECISIONS.md D-041, D-042\", \"pytest -q tests/unit -k 'date or dismiss or suggest' (151 passed, 1106 deselected)\", \"pytest tests/unit/test_date_convention.py -v (8 passed)\", \"mutation suite 88a-88e in scratch copy (artifacts/review-evidence/T-088-T-089/mutation_run.txt)\", \"probe on golden case_01 via TestClient (artifacts/review-evidence/T-088-T-089/probe_t088_output.txt)\", \"git diff --cached --name-status; git cat-file -e HEAD:<path>\", \"grep suggestion app/frontend (0); golden case_01 expected.json (0)\"],\n \"verdict\": \"fail\",\n \"scores\": {\"code_only_no_llm\": 5, \"never_auto_applied_d041\": 5, \"reason_grounded_in_packet\": 2, \"mixed_packet_handling\": 4, \"tests_fail_on_mutation\": 4, \"ac_integrity\": 2},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"Reason says the evidence dates are 'in this record' when they come from other records in the packet\",\n   \"evidence\": \"app/backend/date_convention.py:64-65 builds 'Other dates in this record use ...' while `_evidence(records, raw_text)` (line 52) scans every packet record. Golden repro (probe_t088_output.txt): the 04/05/2026 suggestion on record r8 returns reason '4 other dates in this record use month first (02/17/2026) and (03-17-26)', with evidence record ids r2 and r6 (the other two counted dates, 3/25/26 in r7 and 04/14/2026 in r7's excerpt, are also outside r8). evals/golden/case_01_date_formats.txt: record 8 (lines 39-41) contains only 'Patient reports no new symptoms.' and no other date. The false wording is pinned by tests/unit/test_date_convention.py:32, :46 and :99 (line 99 asserts the exact golden reason). The T-088 AC text (board show T-088) says 'the reason (other dates in the packet)'.\",\n   \"why_it_matters\": \"The paralegal reads a provenance claim about the record in front of them that is false for every golden case of this kind. The D-041 gate still stops an unconfirmed date from reaching the letter, so no wrong date is exported, but the stated reason sends the paralegal to look in the wrong record. CLAUDE.md non-negotiable 5 says every statement must trace to the input, and this one does not. Rated blocker per CONTRACT D.2 (invented fact), not major. The date strings quoted are real.\",\n   \"fix\": \"Build the reason from the evidence's own record ids, e.g. 'Other dates in this packet use month first (02/17/2026, record 2) and (03-17-26, record 6)'. Remove the phrase 'in this record' everywhere. Update the expected strings at test_date_convention.py:32, :46 and :99.\",\n   \"acceptance_test\": \"tests/unit/test_date_convention.py: (a) golden case_01 reason names the record of each quoted date and does not contain 'this record'; (b) packet r1 '03/14/2026' with ambiguous r2 '04/05/2026' yields a reason that names record 1. Mutation: restore the old wording, and tests (a) and (b) must fail.\"},\n  {\"severity\": \"major\",\n   \"title\": \"AC 1 is marked done=true while two of its required parts are not in the codebase\",\n   \"evidence\": \"board show T-088, AC 1: \\\"done\\\": true, evidence \\\"... UI pre-select is frontend's (see note)\\\". The AC text includes 'the UI pre-selects it' and 'eval case'. Handoff: 'Left: frontend pre-select; qa golden case.' grep -rn suggestion app/frontend: 0 matches. grep -c 'suggestion|dismissal' evals/golden/case_01_date_formats.expected.json: 0.\",\n   \"why_it_matters\": \"The card says the AC is done, but the paralegal-facing behaviour (radio pre-selected with the reason, confirm on click only) does not exist, and the eval case the AC names does not exist either. Only the unit-level half is shipped. A required AC item that is present but incomplete is major under the persona calibration.\",\n   \"fix\": \"Set AC 1 back to done=false until (a) the frontend pre-select ships and (b) a golden expected entry for case_01 record 8 asserts the MDY suggestion. Or split those two parts into follow-up cards and close the unit half only.\",\n   \"acceptance_test\": \"grep -n suggestion evals/golden/case_01_date_formats.expected.json shows the MDY assertion. A frontend or E2E test shows the 04/05/2026 radio pre-selected with its reason, no confirm request is sent on load, and Accept stays blocked (422 DATE_UNCONFIRMED) until a click on Confirm.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Shared git index stages deletion of this card's files (blast radius: T-088 and T-089)\",\n   \"evidence\": \"git diff --cached --name-status: 'D app/backend/date_convention.py', 'D app/backend/dismissal_patterns.py', 'D tests/unit/test_date_convention.py', 'D tests/unit/test_dismissal_patterns.py' (also 'D app/llm/prompts/conflicts_v1.md'). git cat-file -e HEAD:app/backend/date_convention.py succeeds, and the on-disk files match HEAD byte for byte (checked with git show f667f08:<path> | diff). git status shows them as '??' untracked.\",\n   \"why_it_matters\": \"The committed artifact at HEAD is intact, so this is not a defect in f667f08 itself. But the next commit made from this index deletes the T-088 and T-089 code and tests from the repository. That is a silent loss of both cards' deliverables.\",\n   \"fix\": \"Orchestrator (not this reviewer) restores the index for the card paths without touching the working tree, then commits with explicit paths. The index then matches HEAD for these four files.\",\n   \"acceptance_test\": \"git diff --cached --name-status -- app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py prints nothing, and git ls-files app/backend/date_convention.py lists the file.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Weak assertion: `and`/`or` precedence lets the two-digit-year test pass with the wrong convention\",\n   \"evidence\": \"tests/unit/test_date_convention.py:65: assert s[\\\"convention\\\"] == \\\"MDY\\\" and s[\\\"iso\\\"] is None or s[\\\"iso\\\"] in rows[1][\\\"date_candidates\\\"]. Python parses this as (A and B) or C. When iso is not None and is in the candidates, C is True whatever the convention. In this packet iso is None, so the convention is pinned today; the defect is latent.\",\n   \"why_it_matters\": \"A later change that makes iso non-null for this case could pass with the convention wrong, which is exactly the regression this test exists to catch.\",\n   \"fix\": \"assert s[\\\"convention\\\"] == \\\"MDY\\\" and (s[\\\"iso\\\"] is None or s[\\\"iso\\\"] in rows[1][\\\"date_candidates\\\"])\",\n   \"acceptance_test\": \"Mutant: swap _LABEL so MDY reports DD/MM while iso is non-null for a two-digit-year packet. The fixed assertion must fail.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Unused import\",\n   \"evidence\": \"app/backend/date_convention.py:10: from app.backend import dates (no reference to dates in the module).\",\n   \"why_it_matters\": \"Dead import; harmless.\",\n   \"fix\": \"Delete the line.\",\n   \"acceptance_test\": \"python -m pyflakes app/backend/date_convention.py (or a grep for 'dates\\\\.') reports nothing.\"}\n ],\n \"whats_right\": [\n  \"No server path reads the suggestion: present.py:129 only builds it, confirm_date (review.py:172-181) still takes the client's date and checks it against the candidates, and the D-041 block reads records.date_status (review.py:45-50).\",\n  \"Mixed-order and no-evidence packets return None (date_convention.py:54-55); mutant 88a, which lets mixed packets through, fails test_no_suggestion_without_evidence_or_with_mixed_evidence.\",\n  \"Code only with no LLM path, and the auto-confirm mutant 88e is caught by two tests (the write-check and the golden confirm test).\"\n ],\n \"questions_for_chris\": [\"For a packet whose dates disagree on order, should the paralegal see a short note that the packet is mixed, or is silence (no suggestion) the intended behaviour? The AC allows either.\"]\n}\n```\n"
}
````

### User / tool · 2026-11-02T04:28:49.668Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-088-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:01.162Z

T-088 is written. Now the T-089 review.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:18.417Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-089-staff-engineer.md",
 "content": "# T-089 review: dismissal-pattern suggestions (staff-engineer-reviewer)\n\n**Verdict: changes.** No blocker. The core rules hold: nothing is auto-dismissed, the GET is read-only, bulk-applied flags never feed back into the count, the pipeline does not read the history, and storage adds no identity. Two majors and one minor-level test gap need fixing before the gate. The majors are the demo-isolation test gap (F1) and the shared git index that stages deletion of this card's files (F3). Suggestions only, no auto-dismiss, and no change to pipeline output or golden recall are all verified, not assumed.\n\nScope: commit f667f08 (`app/backend/dismissal_patterns.py`, `app/backend/api.py:497`, `tests/unit/test_dismissal_patterns.py`, the T-089 contract section in `memory/contracts/api.md`). Checked against D-042 in `memory/ORCHESTRATOR_DECISIONS.md` line 50.\n\n**Checks against your three points**\n1. Nothing auto-dismissed: holds. `suggest()` (`dismissal_patterns.py:51-72`) only reads. The GET route (`:92-99`) does not call `apply`. The POST route (`:101-114`) is the only writer, and it needs a key. Mutants 89e (suggest writes) and 89f (GET auto-applies) are both caught.\n2. No effect on pipeline output or golden recall: holds. `pipeline.py` does not import `dismissal_patterns`. The golden identity test (`test_dismissal_patterns.py:116-134`) passes, and mutant 89i (history filters pipeline flags) is caught. Sensitivity is limited, see F4.\n3. Storage local only, no user identity: holds. The module reads the existing `flags` table with no new column, table, or identity field. `grep -n \"user|email|identity|account\"` on the module returns only the docstring that says there are no users. Scope is case-only unless `ZLAYT_MODE=local`, mutant 89g is caught.\n\n**Exercised**\n- `python3 tools/board.py show T-089`; `git show f667f08` (stat and per-file); `git show f667f08:<path>` for in-scope files; D-042 in `memory/ORCHESTRATOR_DECISIONS.md`.\n- `.venv/bin/python -m pytest -q tests/unit -k \"date or dismiss or suggest\"`: 151 passed, 1106 deselected. `pytest tests/unit/test_dismissal_patterns.py -v`: 17 passed (of 25 across both cards).\n- Mutation suite in scratch copy `artifacts/review-evidence/T-088-T-089/mut` (runner `mutate.py`, output `mutation_run.txt`): 89a, 89c, 89e, 89f, 89g, 89i caught; 89b, 89d, 89d2, 89h not caught (see findings).\n- `git diff --cached --name-status`; `git cat-file -e HEAD:<path>` (F3).\n- `grep -rn dismissal app/frontend`: 0 matches (no banner built yet).\n\n```json\n{\"card\": \"T-089\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit f667f08: app/backend/dismissal_patterns.py, app/backend/api.py:497 (route registration), tests/unit/test_dismissal_patterns.py, memory/contracts/api.md (T-089 section); golden evals/golden/*.txt via G.case_names(); no live app URL (TestClient in-process)\",\n \"exercised\": [\"board.py show T-089 and T-088\", \"git show f667f08 --stat and per-file diffs\", \"git show f667f08:<path> for in-scope files\", \"memory/ORCHESTRATOR_DECISIONS.md D-042\", \"pytest -q tests/unit -k 'date or dismiss or suggest' (151 passed, 1106 deselected)\", \"pytest tests/unit/test_dismissal_patterns.py -v (17 passed)\", \"mutation suite 89a-89i incl. 89d2 in scratch copy (artifacts/review-evidence/T-088-T-089/mutation_run.txt)\", \"git diff --cached --name-status; git cat-file -e HEAD:<path>\", \"grep -rn dismissal app/frontend (0)\", \"grep for pipeline imports of dismissal_patterns (none)\"],\n \"verdict\": \"changes\",\n \"scores\": {\"never_auto_dismiss\": 5, \"no_pipeline_or_recall_effect\": 4, \"local_only_no_identity\": 4, \"demo_isolation_tested\": 2, \"tests_fail_on_mutation\": 3, \"ac_integrity\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Demo-mode isolation at the route is not tested; forcing local scope in the route passes all 25 tests\",\n   \"evidence\": \"app/backend/api.py:497 registers the route with local_mode=local_mode. Mutant 89h replaces it with local_mode=lambda: True in the scratch copy: '25 passed' (artifacts/review-evidence/T-088-T-089/mutation_run.txt, line 'MUTANT 89h ... NOT CAUGHT'). tests/unit/test_dismissal_patterns.py:94-113 (test_routes_and_demo_mode_isolation) creates one case only and seeds history in that case, so it cannot tell local from non-local scope. The unit test at :84-91 tests the function with local=True/False, not the route. memory/contracts/api.md (T-089 section) says 'a public/demo token never sees another case's dismissals'; the test named 'demo-mode isolation' does not assert that.\",\n   \"why_it_matters\": \"The suggestion message counts dismissals in other cases ('all cases on this computer'). If the route's scope regresses, a public demo token would see phrase counts from other cases. The data is synthetic and the counts carry little content, so this is a test-coverage gap, not a live leak; the code today is correct. Depth on exposure belongs to security-reviewer. The card's AC evidence names a demo-isolation test that does not test isolation.\",\n   \"fix\": \"Add a route test: create case A with 3 dismissals of a phrase and case B with the pending match, run without ZLAYT_MODE, and assert GET /api/cases/B/dismissal_suggestions returns suggestions == []. Then run with ZLAYT_MODE=local and assert the suggestion appears. Rename the test to describe what it asserts.\",\n   \"acceptance_test\": \"Mutant 89h (local_mode forced True in api.py:497) must fail the new test. The unmodified route must pass it.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Shared git index stages deletion of this card's files (blast radius: T-088 and T-089)\",\n   \"evidence\": \"git diff --cached --name-status: 'D app/backend/dismissal_patterns.py' and 'D tests/unit/test_dismissal_patterns.py' (plus the T-088 files and app/llm/prompts/conflicts_v1.md). git cat-file -e HEAD:app/backend/dismissal_patterns.py succeeds and the on-disk file matches HEAD (git show f667f08:<path> | diff: no output).\",\n   \"why_it_matters\": \"HEAD is intact, so f667f08 itself is fine. The next commit made from this index deletes the T-089 module, its routes' code path and its tests, which is a silent loss of the deliverable.\",\n   \"fix\": \"Orchestrator restores the index for these paths without touching the working tree, then commits with explicit paths. The reviewer does not run git reset.\",\n   \"acceptance_test\": \"git diff --cached --name-status -- app/backend/dismissal_patterns.py tests/unit/test_dismissal_patterns.py prints nothing.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Eligibility rules are tested only as a conjunction; neither the type rule nor the origin rule is isolated\",\n   \"evidence\": \"app/backend/dismissal_patterns.py:22 (ELIGIBLE_TYPES) and :28 (origin must contain 'lexicon'). tests/unit/test_dismissal_patterns.py:49-50 builds the gap and record_warning flags with origin='code', so the origin check alone excludes them. Mutant 89d (gap added to ELIGIBLE_TYPES) and mutant 89d2 (origin requirement removed) both give '25 passed' (mutation_run.txt).\",\n   \"why_it_matters\": \"The AC says 'ineligible types never offered'. Today a lexicon-origin gap flag would be offered for hiding if the type list were widened, and no test would notice.\",\n   \"fix\": \"Add cases: a gap flag and a record_warning flag with origin 'lexicon+llm' (must not be suggested); a pre_existing flag with origin 'llm' only (must not be suggested).\",\n   \"acceptance_test\": \"Mutants 89d and 89d2 must each fail a test.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Category threshold boundary (CATEGORY_MIN) has no negative test; golden identity test seeds only one category\",\n   \"evidence\": \"app/backend/dismissal_patterns.py:21 CATEGORY_MIN = 5. The category test (tests/unit/test_dismissal_patterns.py:54-63) only asserts the positive case at 5. Mutant 89b (CATEGORY_MIN = 4) gives '25 passed'. Also tests/unit/test_dismissal_patterns.py:15 defaults the seeded history to category 'new_onset'. Mutant 89i fails only the [sample] parametrization of the golden identity test (mutation_run.txt), so the other nine golden cases are not sensitive to history at all.\",\n   \"why_it_matters\": \"The AC claim 'pipeline output identical on all golden cases with and without history' is true, but the test can only detect pipeline influence on flags of category new_onset. For the other nine cases it is a vacuous equality. The AC item also says 'eval shows no recall loss', and no eval report path exists; this unit equivalence test is the only evidence.\",\n   \"fix\": \"Add a 4-dismissal negative case for the category rule. In the golden identity test, seed history with each case's own flag categories and phrases (taken from its pipeline output) so the equality is sensitive per case. Name the unit test as the recall evidence in the card, or add an eval report.\",\n   \"acceptance_test\": \"Mutants 89b and 89i must each fail on at least one golden case other than sample.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"AC 'surface as a suggestion' is evidenced only by the API payload; the banner is not built\",\n   \"evidence\": \"board show T-089, AC 1 done=true. Handoff: 'Left: frontend banner'. grep -rn dismissal app/frontend: 0 matches. The AC text does not name a UI element, so the API payload is the AC's surface.\",\n   \"why_it_matters\": \"Acceptable for this AC as written, but the card's notes ask the frontend to show a banner with two buttons, and nothing in the card records that as a later AC. The surfacing will be lost unless a follow-up card tracks it.\",\n   \"fix\": \"Create a follow-up frontend card for the banner, or add the banner to this card's AC before closing it.\",\n   \"acceptance_test\": \"A UI test shows the banner after three dismissals, and flags stay unchanged until the 'Hide similar' click.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"apply() is not atomic across flags\",\n   \"evidence\": \"app/backend/dismissal_patterns.py:86-87: the loop calls review.apply_review once per flag id with no transaction. A failure partway leaves earlier flags dismissed. Not reproduced; the flag ids come from pending flags and no test exercises a mid-loop failure.\",\n   \"why_it_matters\": \"Low risk because each dismissal is individually logged and reversible with reset. Still a partial write with no explicit response.\",\n   \"fix\": \"Wrap the loop in one transaction, or document the partial-write behaviour in api.md.\",\n   \"acceptance_test\": \"A test that forces apply_review to raise on the second flag and asserts the first flag is not dismissed.\"}\n ],\n \"whats_right\": [\n  \"The GET path is read-only (mutant 89e, which writes on read, fails four tests; mutant 89f, which auto-applies on GET, fails the route test).\",\n  \"Bulk-applied flags carry APPLIED_NOTE and are excluded from the count (dismissal_patterns.py:44); mutant 89c, which counts them, fails the self-reinforcement test.\",\n  \"The pipeline does not import the module, and the history can change no pipeline output (mutant 89i is caught by the golden identity test).\"\n ],\n \"questions_for_chris\": [\"In local mode the suggestion counts dismissals across every case on the machine. Is that the intended single-profile scope, or should counts stay per case until a profile concept exists?\"]}\n```\n"
}
````

### User / tool · 2026-11-02T04:29:18.568Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-089-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:27.916Z

Both reviews are written. Next I'll validate the JSON blocks, remove the 16 MB product copy under `review-evidence` so a full-repo pytest cannot collect a second copy of the tests, and confirm the file states.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:29.546Z

**tool call — Bash**
````
{
 "command": "for f in reviews/T-088-staff-engineer.md reviews/T-089-staff-engineer.md; do python3 -c \"\nimport json,re,sys\nt=open(sys.argv[1],encoding='utf-8').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint(sys.argv[1], 'json blocks:', len(blocks))\nd=json.loads(blocks[0])\nsev=[x['severity'] for x in d['findings']]\nv='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint(' card',d['card'],'| persona',d['persona'],'| model',d['model'],'| verdict',d['verdict'],'| rule-derived',v,'| findings',sev)\n\" \"$f\"; done; rm -rf artifacts/review-evidence/T-088-T-089/mut && echo \"removed scratch product copy\"; ls artifacts/review-evidence/T-088-T-089/",
 "description": "Validate both review JSON blocks and remove the scratch product copy"
}
````

### User / tool · 2026-11-02T04:29:29.600Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:32.414Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport json, re\nfor p in [\"reviews/T-088-staff-engineer.md\", \"reviews/T-089-staff-engineer.md\"]:\n    t = open(p, encoding=\"utf-8\").read()\n    blocks = re.findall(r\"```json\\n(.*?)\\n```\", t, re.S)\n    d = json.loads(blocks[0])\n    sev = [x[\"severity\"] for x in d[\"findings\"]]\n    rule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\n    print(p, \"| json blocks:\", len(blocks), \"| card\", d[\"card\"], \"| persona\", d[\"persona\"], \"| model\", d[\"model\"],\n          \"| verdict\", d[\"verdict\"], \"| rule\", rule, \"| ok\" if rule == d[\"verdict\"] else \"| MISMATCH\", sev)\nEOF",
 "description": "Validate both review JSON blocks and verdict rule"
}
````

### User / tool · 2026-11-02T04:29:32.509Z

**tool result**
````
reviews/T-088-staff-engineer.md | json blocks: 1 | card T-088 | persona staff-engineer-reviewer | model claude-haiku-5-5 | verdict fail | rule fail | ok ['blocker', 'major', 'major', 'minor', 'nit']
reviews/T-089-staff-engineer.md | json blocks: 1 | card T-089 | persona staff-engineer-reviewer | model claude-haiku-5-5 | verdict changes | rule changes | ok ['major', 'major', 'minor', 'minor', 'minor', 'nit']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:33.826Z

**tool call — Bash**
````
{
 "command": "rm -rf artifacts/review-evidence/T-088-T-089/mut && ls artifacts/review-evidence/T-088-T-089/",
 "description": "Remove the scratch product copy and list the evidence folder"
}
````

### User / tool · 2026-11-02T04:29:34.018Z

**tool result**
````
mutate.py
mutation_run.txt
probe_t088.py
probe_t088_output.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:37.038Z

Both reviews are written and validated. I'll record the recurring patterns in my memory directory so future reviews check them.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:41.344Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t088_t089_review_patterns.md",
 "content": "---\nname: t088-t089-review-patterns\ndescription: T-088 date-convention and T-089 dismissal suggestions (f667f08) r1 patterns: packet-scope reason wording, AC marked done with UI unbuilt, shared index staging card files deleted, route isolation untested\nmetadata:\n  type: project\n---\n\nRecurring patterns from the T-088 (date-convention suggestion) and T-089 (dismissal suggestions) r1 review of commit f667f08.\n\n- **Reason text states a scope the data does not have.** T-088 reason said \"in this record\" for evidence in other packet records (golden case_01 record 8). Pinned by the test itself, so a green suite did not catch it. Check every generated sentence's scope claim against the record ids in its evidence array.\n- **AC marked done=true with a named UI or eval half unbuilt.** T-088 AC named \"the UI pre-selects\" and \"eval case\"; neither existed (frontend grep 0, golden expected 0). Check each AC noun against the file it names before accepting done.\n- **Shared index staging deletion of card files.** `git diff --cached --name-status` showed 'D' for both cards' files while HEAD had them. Any commit from that index deletes the code. Run `git diff --cached --name-status` at the start of each review.\n- **Named isolation test that asserts no isolation.** T-089 `test_routes_and_demo_mode_isolation` seeds one case only; forcing `local_mode=lambda: True` in api.py passes all tests. Mutate the route wiring, not just the function.\n- **Eligibility rules masking each other.** Type list and lexicon-origin check each excluded the same test flags, so removing either alone was not caught. Test each rule with a flag that only the other rule would exclude.\n- **Golden identity test sensitivity.** History seeded in one category; only the sample case is sensitive. Seed history per golden case's own categories.\n- **Assertion precedence.** `A and B or C` in a test assertion passes whenever C holds regardless of A. Parenthesize.\n\n**How to apply:** mutation runs in this repo must write under `artifacts/review-evidence/` (scratchpad writes are blocked by reviewer-write-guard for Write; shell copies there were allowed). Remove the copied product tree afterwards, since a stray `tests/` copy under artifacts can break full-repo pytest collection. See [[feedback_review_write_once]] and [[project_t050_namespacing_review_patterns]].\n"
}
````

### User / tool · 2026-11-02T04:29:41.442Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t088_t089_review_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:42.495Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T04:29:42.500Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E
8	- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1-r2: producer case= fix, delete-on-upgrade silent loss, guard in wrong file, pin HEAD by archive
9	- [Eval runner review patterns](project_eval_runner_review_patterns.md) — T-038 r1-r3: fake hides real keys, fix picks internal not API shape, git-archive pinning
10	- [Split LLM review patterns](project_split_llm_review_patterns.md) — T-057 r1-r4: stale-on-failed-rerun, freeze trigger untested beyond accept, orphan probe needs pre-fix control
11	- [Round-2 snapshot review patterns](project_round2_snapshot_review_patterns.md) — T-040/T-043 r2: HEAD moves mid-review, archive needs untracked fixtures, guard traps, overwrite hazard
12	- [T-063 doc-vs-code patterns](project_t063_doc_vs_code_review_patterns.md) — r1 "code only" docs that call models; r2 fixed defects still named open; r3 "no card" goes stale, None branch drops reason, HEAD moves
13	- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts (D-033 blocker, not major)
14	- [T-065 fallback-removal patterns](project_t065_batch_fallback_review_patterns.md) — r1-r2: mock fan-out, undo test, contract red at commit, mock contract drift, skipped e2e guard
15	- [T-066 NO_MODEL patterns](project_t066_no_model_reason_patterns.md) — r1-r3: elif reason wider than its message, gate survives, r3 pass: assert reason absence, not only wrong text
16	- [R2 fix-verification patterns](project_r2_fix_verification_patterns.md) — T-058/T-055/T-059 r2: fix inside another card's commit, overstated mutant counts, $-anchor sweep, diagnosis wording
17	- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-070 r2 normalizer+guard+consumer mutation (pass), T-067 r2 mixed-result drop, persona mismatch
18	- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — r1-r4: judge-never-ran summaries, gate vs export agreement, D-045(a) fixed in r4, carry-over minors need their file in the diff, 422 vs 409
19	- [Review write-once](feedback_review_write_once.md) — reviews/*.md is append-only under the guard; proof-read citations before the first Write
20	- [T-067 r6 D-043 patterns](project_t067_r6_d043_patterns.md) — r6 e3cea6f: later decision supersedes old acceptance clause, allow-list "exactly" comment drift, reviewer write guard
21	- [T-075 determinism patterns](project_t075_determinism_review_patterns.md) — r1 3104213: signature narrower than R-CO-7, vacuous order test; r2 b5b9b34: sort and J3/J4 mutants red, pass
22	- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1 e491cad: J3 relabel after failure, controls gate without ADR, keyword-separable controls, scratch-mutant guard traps
23	- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83: committed counts not reproducible from commit, AC closed with UI unbuilt, class/tolerated/threshold mutants survive
24	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:44.558Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83: committed counts not reproducible from commit, AC closed with UI unbuilt, class/tolerated/threshold mutants survive\n",
 "new_string": "- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83: committed counts not reproducible from commit, AC closed with UI unbuilt, class/tolerated/threshold mutants survive\n- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason says \"in this record\" for packet evidence, AC done with UI unbuilt, index stages card deletions, route isolation untested\n"
}
````

### User / tool · 2026-11-02T04:29:44.647Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:29:50.126Z

T-088 fails: its reason says "in this record" for dates that sit in other packet records (golden case_01 record 8), and AC1 is marked done with the UI and eval case unbuilt. T-089 needs changes, with no blocker: route-level demo isolation is untested (a forced-local mutant passes), and the shared index stages deletion of both cards' files.
Reviews: `/Users/arsis/zlayt-pm-project/reviews/T-088-staff-engineer.md` and `/Users/arsis/zlayt-pm-project/reviews/T-089-staff-engineer.md`; mutation evidence is `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-088-T-089/mutation_run.txt`.
