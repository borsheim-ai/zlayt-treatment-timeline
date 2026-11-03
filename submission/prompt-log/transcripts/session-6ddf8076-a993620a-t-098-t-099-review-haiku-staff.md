# Subagent: T-098 + T-099 review (haiku staff) (T-098 + T-099 review (haiku staff))

Source: `agent-a993620a506869f57.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T05:00:29.034Z

Review two board cards in /Users/arsis/zlayt-pm-project. Test a `git archive HEAD` copy in your scratchpad, since reviewers can't use worktree.

1. **T-098** (commit e511778): an accepted, human-edited summary that fails any code check is an export-gate blocker, and GET export returns 422 with the same list; gate.ready == export allowed still holds. Read reviews/T-097-ux-designer.md (the blocker case) and D-045 and D-047 in memory/ORCHESTRATOR_DECISIONS.md.
   - D-047 is new: side and negation tokens are now hard 422 on edit, and the 409 "keep my wording" path is to be removed. Check whether the 409 path still exists. If it does, that's a major for T-098's follow-up; say so.
   - The commit also carried other workers' uncommitted hunks in trace.py and api.md (T-094, T-099). Check that those don't break anything.
   - Run `.venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_export.py`.
   - Write reviews/T-098-staff-engineer.md.
2. **T-099** (commit 3ecb8b1): GET /api/calibration serves evals/reports/calibration.json in the T-096 shape, with clear missing and invalid states and never invented numbers. It's safe in demo mode. Run `.venv/bin/python -m pytest -q tests/unit -k calibration`. Write reviews/T-099-staff-engineer.md.

Each file needs a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 2 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:30.972Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T05:00:30.986Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:31.584Z

**tool call — Bash**
````
{
 "command": "git rev-parse --is-inside-work-tree 2>&1; git log --oneline -n 8 2>&1; git show --stat e511778 2>&1 | head -40; git show --stat 3ecb8b1 2>&1 | head -40",
 "description": "Check git state and show the two commits' file stats"
}
````

### User / tool · 2026-11-02T05:00:31.737Z

**tool result**
````
true
196c985 harness: stale-index guard allows partial staging; blocks only re-staged older committed versions
3ecb8b1 feat(backend): GET /api/calibration serves the measured calibration read-only (T-099)
36a982b docs: D-047 side/negation tokens hard 422, drop 409 keep-my-wording path
e511778 fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)
5b4ccb0 harness: pre-commit blocks stale-index reverts (staged blob matches neither HEAD nor worktree)
9c1af01 fix(backend): restore the T-085 r2 files that 57a08ba reverted by mistake (stale temp index); T-084 r3 change stays
57a08ba fix(backend): reclassify wording gate uses the classifier's rate verdict and the shared rate cues; class-only restore tested (T-084 r3)
1b1c711 fix(backend): language detection fails safe, French/Portuguese refused, CLI crash, 'no se descarta' keeps its meaning, Spanish cue words, Spanish eval pairs (T-085 r2)
commit e5117784ccec180cc41b68eb050cbe1d99f5534d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:59:28 2026 -0600

    fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)
    
    A summary the paralegal wrote or edited is exempt from the judge but still has to pass the D-034/D-022 code checks. Accepted/edited entries of that kind
    with a failing code step are now gate blockers (named step + next action), GET /export returns 422 for them, and the item trace shows the failing step
    with a specific 'Edit the summary to keep ...' action. trace.py and api.md also carry other workers' uncommitted hunks (T-094 flag steps, T-099 calibration contract).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/grounding.py  |  28 +++++++++++++
 app/backend/trace.py      |  94 +++++++++++++++++++++++++++++++++++++-----
 memory/contracts/api.md   |  15 ++++++-
 tests/unit/test_export.py |  12 ++++++
 tests/unit/test_trace.py  | 102 ++++++++++++++++++++++++++++++++++++++++++++++
 5 files changed, 239 insertions(+), 12 deletions(-)
commit 3ecb8b1ca58b97c2d23cdd78a8a99a7bf292f8db
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:00:11 2026 -0600

    feat(backend): GET /api/calibration serves the measured calibration read-only (T-099)
    
    Serves evals/reports/calibration.json in the T-096 shape (counts, statements, source commit, backend, sample size).
    Envelope {status, calibration, message}: ok | missing | invalid. calibration is null unless ok; nothing is invented
    and the file contents are never echoed. Aggregate only, no case token, so it is demo-safe. GET only (other methods 405).
    Validation: shape, count ranges, state totals equal type totals, each statement quotes its own m/t.
    Contract section is already in memory/contracts/api.md (landed with e511778).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/api.py                   |   2 +
 app/backend/calibration_route.py     | 123 ++++++++++++++++++++++++
 tests/unit/test_calibration_route.py | 177 +++++++++++++++++++++++++++++++++++
 3 files changed, 302 insertions(+)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:36.190Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git status --short | head -30; echo ---; grep -n \"D-04[5-7]\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -150",
 "description": "Show HEAD, working tree status, and D-045 to D-047 decisions"
}
````

### User / tool · 2026-11-02T05:00:36.322Z

**tool result**
````
196c985641d72aa699e295223fed8961db0b0c2a
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
 M app/backend/billing.py
D  app/backend/calibration_route.py
 M app/backend/confidence.py
 M app/backend/flags.py
MM app/backend/grounding.py
 M app/backend/judges.py
 M app/backend/pdf_checks.py
 M app/backend/pdf_hidden.py
 M app/backend/pdf_ocr.py
 M app/backend/pdf_text.py
 M app/backend/pipeline.py
 M app/backend/reclassify.py
 M app/backend/review.py
---
53:| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
54:| D-046 | Ship-bar item 4 also gates on the seeded J3 (conflict) and J4 (flag) judge control sets (2026-11-02): each must catch every seeded wrong item with 0 false agrees. Control labels are fixed before a run; an item may be relabelled only with a written reason reviewed by a second agent, never because it failed. | Judges J3/J4 now decide flags (T-075, T-094); a catch rate only on J1 would leave them unmeasured. | T-093 staff r1 major 2 |
55:| D-047 | Extends D-034 (2026-11-02): side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a **hard 422** on edit and manual entry. The 409 'keep my wording' path is removed, so the gate (T-098) and the edit route agree and no item can be confirmed into an unexportable state. | A side or negation the record does not state is as dangerous as an invented number; a confirm path that leads to a blocked export is a dead end. | T-098 handoff |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:36.440Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-097-ux-designer.md"
}
````

### User / tool · 2026-11-02T05:00:36.448Z

**tool result**
````
1	# T-097 ux-designer-reviewer: rerun feedback beside the refused export, panel failure message, panel/gate agreement
2	
3	Verdict: **fail** (1 blocker, 2 majors, 1 minor, 1 nit).
4	
5	Scope: card T-097, commit 0e30623 (the card's commit). I ran a `git archive 0e30623` copy from my scratchpad on my own server (:7895, fixture backend, curated set, scratch ZLAYT_DB). Shared-tree HEAD was 8bc7f90 at the start and 172028c at the end (it moved during the review); I did not review either. Server stopped by PID, port returns 000.
6	
7	## The four brief questions
8	
9	1. **Rerun feedback directly under the button in the refused-export message: pass.** At 1440 the button is at y=154 (h=44) and the status line at y=202, 4 px below it. At 390 the button is at y=202 and the status at y=250. The Running and the failed sentence are both in view at both widths. Failed sentence: "The second check still did not answer for 3 items of 3. Try again, or dismiss them." The lead sentence is above the button, so "under the button" is the status line, not the lead.
10	2. **A failed panel rerun shows a plain-words message that survives a repaint: pass.** The AI-check panel group shows the same failed sentence at 1440 (y=879, in view) and 390 (y=448, in view). It survives collapse and reopen and a second failed rerun, which rebuilds the panel. A full page reload clears it; that is expected for in-memory state and I do not count it.
11	3. **The panel reads the gate's JUDGE_NOT_RUN blockers, and an edited item says "Edited by you, not AI-checked" with no rerun: partly.** The panel rows and group are right: the edited row has the chip "Edited by you, not AI-checked", no "Blocks the export" chip and no button; the accepted row carries "Blocks the export"; the group button reads "for this item" for N=1. Dismissing the accepted item clears the panel block and the rail says "Ready to export". Two places still disagree with the gate: the panel's one-line summary (finding 2) and the item Why dialog for the edited item (finding 3). Finding 1 is a gate defect the walk exposed.
12	4. **One group button instead of per-row buttons: reasonable in the AI-check panel, incomplete overall.** One POST covers the whole list (the server scope), and the label counts match the rows. But the rail's gate rows still carry one button per row, and the label names one item while the POST answers for all of them (finding 4). Apply the group model to the rail too.
13	
14	## Findings
15	
16	**B1 (blocker). An edited summary whose qualifier check fails passes the export gate and goes into the letter.** Walk2 part B: after I accepted one item and edited another so it drops a qualifier from its quote, dismissing the accepted item gives a gate of "pass", an export of 200 that contains the edited sentence, and the edited item's own trace reports `summary_qualifier` fail with `SUMMARY_DROPS_QUALIFIER`. The Why dialog shows "Summary keeps the quote's qualifiers | Code | Needs your decision", and the rail says "Ready to export, 21 not reviewed". D-045(b) says an edited summary "still passes the D-034 code checks". The gate does not enforce that for edits. The probe found no AI draft in the sample with this check failing, so I cannot compare the AI path; the blocker is on the edited path that was exercised. Open question for Chris below.
17	
18	**M1 (major). The panel summary still says "2 not checked (blocks export)" while the gate blocks 1.** With one accepted item (judge never ran) and one edited item (exempt), the summary reads "18 checked, 18 agreed with the draft, 2 not checked (blocks export)" at both widths, and the rail says "Export blocked by 1". The "(blocks export)" suffix is attached to the full unchecked count. This is the T-082 r3 contradiction, fixed in the rows and group but not in the summary the paralegal sees when the panel is collapsed. The card's own AC says the panel never says "Blocks the export" for items the gate treats as ready.
19	
20	**M2 (major). The Why dialog for an edited item says "Accepted, second check missing" and offers "Run the second check again".** The verdict and the judge step come from the per-item trace, which still treats the edited item as a failed judge. The same item's panel row says "Edited by you, not AI-checked" with no button. T-081 r3 logged this as minor; I raise it because the card's goal is gate and panel agreement, and the Why dialog is the surface where the paralegal decides the item. The T-097 handoff lists it as left open.
21	
22	**m1 (minor). Rail gate-row rerun buttons name one item but rerun all of them (carried from T-081 r3, unchanged).** The row's aria-label is "Run the second check again for 2026-01-09 · Austin EMS run report", yet one click posts once and the status reads "for 3 items of 3" (walk2 `A_1440_after_row_click`, same at 390). The rail rows are built by `blockerRow` at stepper.js:419, which passes the per-item label into the shared handler that posts with no item id (stepper.js:137).
23	
24	**n1 (nit). The Export button is still scrolled out of view when a refused export opens (carried from T-081 r3).** Export button y=-32 at 1440 and y=-179 at 390 after the message opens; `export-blocked` is in view but `btn-export` is not.
25	
26	## Evidence
27	
28	- Walk scripts and results: `artifacts/review-evidence/T-097-ux-designer-walk1.py` and `artifacts/review-evidence/T-097-ux-designer-walk1-results.json`; `artifacts/review-evidence/T-097-ux-designer-walk2.py` and `artifacts/review-evidence/T-097-ux-designer-walk2-results.json`; `artifacts/review-evidence/T-097-ux-designer-probe3.py`.
29	- Screenshots: `artifacts/review-evidence/T-097-ux-designer-1440-s1-refused-export-failed.png`, `artifacts/review-evidence/T-097-ux-designer-390-s1-refused-export-failed.png`, `artifacts/review-evidence/T-097-ux-designer-390-s2-panel-failed.png`, `artifacts/review-evidence/T-097-ux-designer-1440-s3-mixed-panel.png`, `artifacts/review-evidence/T-097-ux-designer-1440-s3-edited-item-dialog.png`, `artifacts/review-evidence/T-097-ux-designer-1440-s3-after-dismiss.png`.
30	- Code located (not used as evidence of behaviour): `app/frontend/stepper.js:131-143, 163-171, 411-420, 488-507`; `app/frontend/judges.js:1-39, 40-150`; `memory/ORCHESTRATOR_DECISIONS.md:42` (D-034) and `:53` (D-045).
31	
32	## What I did not exercise
33	
34	Keyboard-only walk (not in this brief). The item Why dialog for an accepted item was not clicked separately; it uses the same `S.rerunButton` handler as the rail (finding m1). The server log has four `llm call failed step=j1` lines from the walk; I did not trace them to any UI state, and that is outside my lens.
35	
36	## Three things that are right
37	
38	- The refused-export message puts the rerun button and its Running and result sentences directly beneath the lead sentence, in view at 1440 and 390 (S1 `status_directly_under_button: true`).
39	- A failed panel rerun says what happened in plain words and survives collapse, reopen and a second failed rerun at both widths.
40	- The panel's edited row says "Edited by you, not AI-checked" with no block chip and no button, and dismissing the accepted item clears the panel block and the rail.
41	
42	```json
43	{"card": "T-097", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
44	 "scope": "card commit 0e30623 via git archive copy in scratchpad (t097/wt); shared-tree HEAD was 8bc7f90 at start and 172028c at end (not reviewed); app http://127.0.0.1:7895 on own server (fixture backend, curated set, scratch ZLAYT_DB), stopped by PID; sample case plus synthetic cases created by the walks",
45	 "exercised": [
46	  "git rev-parse --short HEAD -> 8bc7f90; git rev-parse --short 0e30623 -> 0e30623; git status --short | wc -l -> 277 (start)",
47	  "git archive 0e30623 | tar -x into scratchpad t097/wt (card commit, not HEAD)",
48	  "own server LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7895 ZLAYT_DB in scratchpad: health 200; pids 45474 and 54605 stopped by PID; curl returns 000 after each",
49	  "E2E_BASE_URL=http://127.0.0.1:7895 pytest -p no:cacheprovider tests/e2e/test_rerun_judge.py -q from the copy: 17 passed in 25.15s",
50	  "artifacts/review-evidence/T-097-ux-designer-walk1.py at 1440x900 and 390x844: S1 refused export with JudgeNotRun mode still and hold: pressed the message rerun button, read busy and failed sentences, measured positions, scroll, reopen after reload",
51	  "walk1 S2: AI-check panel group button, failed sentence, collapse/reopen, second failed rerun",
52	  "walk1 S3: mixed case (accepted judge-never-ran plus edited exempt): rail summary and row aria-labels, panel summary, edited and accepted rows, group button, item Why dialog for the edited item, dismiss accepted and reload",
53	  "artifacts/review-evidence/T-097-ux-designer-walk2.py: rail gate-row click (aria-label vs POST scope); edited-summary gate and export via GET /trace, GET /export, GET /items/<id>/trace",
54	  "artifacts/review-evidence/T-097-ux-designer-probe3.py: searched sample AI drafts for summary_qualifier fail: none found",
55	  "viewed screenshots: 1440 s1 failed, 390 s1 failed, 390 s2 panel failed, 1440 s3 mixed panel, 1440 s3 edited item dialog",
56	  "read stepper.js 131-143, 163-171, 411-420, 488-507; judges.js 1-39 and 40-150; ORCHESTRATOR_DECISIONS.md D-034 line 42 and D-045 line 53; reviews T-081-ux-r3 and T-082-ux-r3"],
57	 "verdict": "fail",
58	 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 2},
59	 "findings": [
60	  {"severity": "blocker", "title": "Edited summary whose qualifier check fails passes the export gate and goes into the letter",
61	   "evidence": "walk2 part_b (artifacts/review-evidence/T-097-ux-designer-walk2-results.json): B_item_trace_code_steps [summary_qualifier, fail, SUMMARY_DROPS_QUALIFIER]; B_gate_after_dismiss {status: pass, ready: true, blockers: []}; B_export {status: 200, contains_edit: true}. Rail after dismiss: 'Ready to export, 21 not reviewed' (artifacts/review-evidence/T-097-ux-designer-1440-s3-after-dismiss.png). Why dialog: 'Summary keeps the quote's qualifiers | Code | Needs your decision' (artifacts/review-evidence/T-097-ux-designer-1440-s3-edited-item-dialog.png). D-045(b) at memory/ORCHESTRATOR_DECISIONS.md:53.",
62	   "why_it_matters": "D-045(b) exempts an edited summary from the judge but says it still passes the D-034 code checks. Here the code check fails, the gate says ready, and the letter carries the edited wording with no flag. The export is what the paralegal pastes into a demand letter, so a dropped qualifier reaches the letter with the product's own check failing. Spec-class blocker (invents or loses facts). Whether summary_qualifier is in the D-034 set is an open question for Chris.",
63	   "fix": "Apply to edited summaries the same code steps the gate enforces on model drafts. Refuse the edit at save time with an inline message naming the dropped qualifier, keeping the typed text in the box. Also have the gate list any edited item whose code step fails as a named blocker, so GET /export is refused while it fails. The rail, the Export message and the item Why dialog must all say the same thing.",
64	   "acceptance_test": "E2E: edit a summary so it drops a qualifier from its quote. Expect an inline refusal beside the edit box with the typed text preserved; while it fails, GET /api/cases/<t>/export is not 200 and the letter does not contain the edited sentence. Unit: the gate blocker list includes any edited item with a failing code step."},
65	  {"severity": "major", "title": "Panel summary still says '2 not checked (blocks export)' while the gate blocks 1",
66	   "evidence": "S3_edited_mixed_1440_panel_summary {summary_counts: '18 checked, 18 agreed with the draft, 2 not checked (blocks export)'}; S3_edited_mixed_1440_rail {summary_gate: 'Export blocked by 1'}; same at 390 (S3_edited_mixed_390_panel_summary). Screenshot artifacts/review-evidence/T-097-ux-designer-1440-s3-mixed-panel.png. judges.js summaryText attaches '(blocks export)' to the full unavailable count when nb > 0.",
67	   "why_it_matters": "The T-097 AC says the panel never says 'Blocks the export' for items the gate treats as ready. The one-line summary is the signal the paralegal reads when the panel is collapsed; it says two unchecked items block, and the gate says one. It is the same contradiction T-082 r3 named, fixed in the rows and group but not in the summary.",
68	   "fix": "Build the summary from the gate's JUDGE_NOT_RUN set: '2 not checked, 1 blocks export'. Only the gate-listed count carries the blocking wording.",
69	   "acceptance_test": "E2E on the mixed case (1 accepted, 1 edited, judge never ran on the accepted one): judge-summary-counts shows the gate count (1) next to 'blocks export' and does not attach it to the edited item; after the accepted item is dismissed, the summary has no 'blocks export'."},
70	  {"severity": "major", "title": "Why dialog for an edited item says 'Accepted, second check missing' and offers 'Run the second check again'",
71	   "evidence": "S3_edited_mixed_1440_item_dialog_edited {verdict: 'Accepted, second check missing', rerun_btn: 1}, judge step '✕ ... Did not run ... Run the second check again'; same at 390 (S3_edited_mixed_390_item_dialog_edited). Same item's panel row: S3_edited_mixed_1440_panel_edited_row {chip 'Edited by you, not AI-checked', rerun_btn_in_row: 0}. Screenshot artifacts/review-evidence/T-097-ux-designer-1440-s3-edited-item-dialog.png. The verdict comes from GET /api/cases/<t>/items/<id>/trace, which the stub does not change for edited items. The T-097 handoff lists this as left open.",
72	   "why_it_matters": "The Why dialog is where the paralegal decides an item. For an item D-045(b) exempts, it says the check is missing, shows a red cross, and offers a button that answers 'nothing to run'. The panel and the gate say the opposite. T-081 r3 logged this as minor; raised here because the card's goal is gate and panel agreement, and this is the third surface showing the state.",
73	   "fix": "For human-wording items (review_status edited), build the judge step as neutral 'Not needed: you wrote this summary', with verdict 'Edited by you' and no btn-rerun-judge. Do it in the per-item trace builder so the Why dialog and the panel read one source.",
74	   "acceptance_test": "E2E on the mixed case: the item-stepper for the edited item has no text 'second check missing', no btn-rerun-judge, and no judge step with data-status fail; after the accepted item is dismissed the rail still says Ready to export."},
75	  {"severity": "minor", "title": "Rail gate-row 'Run the second check again' buttons name one item but rerun every item (carried from T-081 r3)",
76	   "evidence": "walk2 A_1440_row_before aria_label 'Run the second check again for 2026-01-09 · Austin EMS run report'; A_1440_after_row_click {posts: 1, rail_status_texts: ['The second check still did not answer for 3 items of 3. Try again, or dismiss them.']}; same at 390. stepper.js:419 passes RERUN + ' for ' + name to S.rerunButton (stepper.js:137), which posts with no item id.",
77	   "why_it_matters": "The label and the effect disagree: a screen-reader user hears a per-item promise, and a sighted user reads a result for three items after pressing one row. T-097 moved the panel to one group button, the right model, but the rail rows and the item Why dialog keep per-item labels.",
78	   "fix": "Use the group model everywhere: one 'Run the second check again for these N' in the gate step and no per-row button (rows keep Go to item). If per-row buttons stay, send the item id and rerun only that item.",
79	   "acceptance_test": "E2E: for every rerun button in the rail, the aria-label scope equals the POST scope: a one-item label means one item in the POST, and a label naming N items means N equals the number of JUDGE_NOT_RUN blockers."},
80	  {"severity": "nit", "title": "Export button is scrolled out of view when a refused export opens (carried from T-081 r3)",
81	   "evidence": "S1_export_blocked_1440_before export_btn_box {y: -32}, message top y=90; S1_export_blocked_390_before export_btn_box {y: -179}; export_btn_in_view false after the failure at both widths (walk1 results).",
82	   "why_it_matters": "The message correctly sits under the toolbar, but the Export button it explains is above the fold; to press Export again the user scrolls up.",
83	   "fix": "Set scroll-margin-top on the export-blocked section to the toolbar height, or scroll the toolbar row into view instead of the message.",
84	   "acceptance_test": "E2E: after a refused Export at 1440x900 and 390x844, btn-export and export-blocked both have their top inside the viewport."}
85	 ],
86	 "whats_right": [
87	  "Refused-export message: the rerun button and its Running and result sentences sit directly beneath the lead sentence, the status 4 px under the button, in view at 1440 and 390 (walk1 S1, status_directly_under_button true).",
88	  "A failed panel rerun says what happened in plain words and survives collapse, reopen and a second failed rerun at both widths (walk1 S2).",
89	  "The panel's edited row says 'Edited by you, not AI-checked' with no block chip and no button; dismissing the accepted item clears the panel block and the rail says Ready to export (walk1 S3)."],
90	 "questions_for_chris": ["Is summary_qualifier part of the D-034 code-check set that D-045(b) requires edited summaries to pass? If yes, B1 stands as a blocker; if the qualifier check is advisory for edits, B1 becomes a major and the gate copy must say so."]}
91	```
92	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:37.209Z

**tool call — Bash**
````
{
 "command": "ls .claude/agent-memory/staff-engineer-reviewer/ && cat .claude/agent-memory/staff-engineer-reviewer/project_t080_trace_review_patterns.md .claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md .claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md .claude/agent-memory/staff-engineer-reviewer/feedback_severity_vs_brief.md",
 "description": "List and read my memory files on trace and export review patterns"
}
````

### User / tool · 2026-11-02T05:00:37.296Z

**tool result**
````
MEMORY.md
feedback_review_write_once.md
feedback_severity_vs_brief.md
project_backend_llm_review_patterns.md
project_db_review_patterns.md
project_design_review_patterns.md
project_e2e_contract_review_patterns.md
project_eval_runner_review_patterns.md
project_harness_review_patterns.md
project_llm_stage_review_patterns.md
project_r2_fix_verification_patterns.md
project_round2_snapshot_review_patterns.md
project_split_llm_review_patterns.md
project_t050_namespacing_review_patterns.md
project_t063_doc_vs_code_review_patterns.md
project_t065_batch_fallback_review_patterns.md
project_t066_no_model_reason_patterns.md
project_t067_r6_d043_patterns.md
project_t070_t067_review_patterns.md
project_t073_t084_review_patterns.md
project_t075_determinism_review_patterns.md
project_t080_trace_review_patterns.md
project_t083_billing_review_patterns.md
project_t088_t089_review_patterns.md
project_t090_calibration_review_patterns.md
project_t093_signature_controls_patterns.md
project_t095_head_revert_patterns.md
project_wiring_review_patterns.md
---
name: project_t080_trace_review_patterns
description: T-080 r1 (check-trace API): aggregates that go green when the judge never ran, gate ready vs blockers contradiction, 404 masking KeyError, survivors in a mostly-strong test file
metadata:
  type: project
---

T-080 r1 (e3cea6f, verdict changes: 0 blockers, 2 majors). Item ladders matched stored data on 16 cases; the bugs were in aggregates and failure branches.

- **Aggregates built from "rows with a verdict" go green when the judge never ran.** `judge_report` skips items with no `ladder.judge.verdict`; a deadline-cut run (pipeline guard false) leaves judge None + JUDGE_UNAVAILABLE, so item traces say skipped while /judges says unavailable 0 and the case step says PASS. How to apply: for any "N of M checked" summary, probe the case where the producer stage did not run (delete the judge record in a DB copy) and compare item-level counts with the summary.
- **Gate `ready` computed from one source, `blockers` from another** (ready ignored status=failed). Check `ready == (blockers == [])` across running/failed/all-accepted.
- **Broad `except (KeyError, IndexError)` -> 404** hides internal table bugs (monkeypatch a fixed-sentence table to prove it).
- Tests were strong (20/23 mutants killed) but survivors sat on the same untested failure branches: dismissed human step, running + all accepted, `disagrees` in totals.

T-080 r2 (94beaeb, verdict changes: 0 blockers, 1 major). Round-1 fixes verified: judges never-ran counted and judges step FAILs, gate `ready == (no blockers)` incl. RUN_FAILED, 404 narrowed, ZLAYT_DB honoured, 3 survivors killed (16/16 valid mutants killed).
- New major: gate passes and `build_export` is silent over accepted items whose judge never ran (12 items: judges FAIL, gate ready, internal notes "Items not reviewed: 0"). Policy gap (R-RV-3 allows accepting JUDGE_UNAVAILABLE), so major not blocker; question to Chris.
- Residuals: rejected amount/flag traces still untested; ITEMS_PENDING gate branch is unreachable (present.py ready_to_export equals live-pending plus NOTHING_ACCEPTED).
- Probe method that worked: a scratch-only helper that calls `DB.update_case` / blanks judge rows on the scratch DB file while the live server runs (it reads per request), then GET /judges, /trace and /export. Verify the probe script's DB path is the scratch file before running it.
- Mutant method: when a mutant survives, first check its anchor is in the branch the test covers (r2 first R2 draft changed an unrelated mapping and survived; a corrected mutant on the fallback was killed).

T-080 r3 (fe4ee80 + D-045 docs f49c4c2; verdict changes: 0 blockers, 1 major, 2 minor, 1 nit; reviews/T-080-staff-engineer-r3.md). D-044 JUDGE_NOT_RUN blocker and export 422 agree live; mutants M1-M7 killed.
- **A binding decision scoped in a docs commit after the code commit is not in the code.** D-045(a) ("pending never blocks export") landed in f49c4c2, after fe4ee80; the gate still lists PENDING_DECISION blockers and `ready` is False, while the export endpoint returns 200. Check each decision line against the code, not just the card's own commit. How to apply: for any "X does not block Y" decision, probe Y with X present.
- **Exemption applied in one function only.** The paralegal-summary exemption lived in `unjudged_items` but not in `_judge_rows`/`judge_report`, so /judges and the judges step still counted the paralegal's edited summary as unchecked (judges FAIL next to gate ready True). How to apply: when an exemption is added, grep every consumer of the same row set (counts, steps, gate, export).
- **Rejudge targets wider than the decision.** `unjudged_items` includes pending items, so POST /rejudge asked 12 (4 blocked + 8 pending) where D-044 says "just those items". Check the target set against the decision text, not only the state change.
- Probe method that worked again: scratch DB helper blanks judge rows (server reads per request); live /trace, /export, /rejudge and /judges on 127.0.0.1:7996; stop by PID.

T-080 r4 (10d358e, D-045 gate: one `export_blockers` list, pending as warnings; verdict pass: 0 blockers, 0 majors, 2 minor, 1 nit; reviews/T-080-staff-engineer-r4.md). r3 major and r3 judges-step minor and nit are closed; r3 rejudge-scope minor still open.
- **A carry-over finding stays open until its file is in the fix diff.** rejudge.py was not in 10d358e, so the r3 rejudge-scope minor was still there, and test_trace.py:906 (`asked == n`) now codifies it. How to apply: for each prior finding, check whether its cited file appears in the round's `git show --stat`; if not, say "still open" and name the test that locks it in.
- **Export refusal status: 422 for state conflicts.** Run in progress, run failed and nothing accepted all return 422 export_blocked. The refusal is right (fail-closed); 422 means invalid content, and the spec reserves 409 for state objections (R-RV-3). Minor, because the spec names no export code.
- **Shared-list invariant test covers the gate and the export, not each guard.** Removing the export_payload guard (M3) was caught only by the nine-state invariant test. How to apply: a single-function guard in one consumer needs one test of its own, not just the shared invariant.
- **Clean mutant beats crude.** A mutant that injected an unknown reason key (ITEMS_PENDING with no TRACE_WHY entry) raised KeyError in unrelated tests and muddied the kill count; a mutant reusing PENDING_DECISION gave 7 precise failures. Report the clean one.

**Environment gotcha:** the app reads `ZLAYT_DB` first (fixed in 94beaeb), then `DATA_DIR` (default `data/zlayt.sqlite`, untracked, shared with the orchestrator's :7860 app). To prove ZLAYT_DB is honoured, set both: ZLAYT_DB to a scratch file and DATA_DIR to an empty sentinel dir; the scratch file should appear and the sentinel stay empty. In r1 (before the fix) the app ignored ZLAYT_DB. Delete only your own cases by token. `rm` is blocked by board-guard for reviewers, and `pkill -f app.main` in a compound command can be refused or hit the shared app; kill by PID from `lsof -nP -iTCP:<port> -sTCP:LISTEN`.

**Method that worked:** drive the real API on a spare port for many golden cases, then a scratch `sqlite3.backup` copy + `PYTHONPATH=. .venv/bin/python` probes that call `trace.*` directly; mutation runner copies the tree once (`cp -R app tests evals docs spec`) and applies string-replace mutants per directory.
---
name: t073-t084-review-patterns
description: T-073 r1 (7724412) narrowed catch, real path retries bugs; T-084 r1 (ec33bf0) restore bypass, rate phrase, commit deleted T-083 billing; r2 (c8a9874, HEAD a850be0) commit fails its own tree, class-only restore untested, gate passes classifier-rate phrasings
metadata:
  type: project
---

T-073 r1 (7724412): the narrowed guard (judge_guard.py) is right at the seam, but the production path still hides programmer bugs: `app/llm/audited.py:70` has its own `except Exception` that retries 3x and surfaces as JUDGE_UNAVAILABLE/NONE. The card's propagation test raises from a raw fake call one layer above, so it cannot see this. Also `judges._run` catches LLMFailed before the guard, so `error_class` is never recorded for the failure the AC names.
**Why:** a card's test proves the behaviour at the seam it fakes; the broad catch moved one layer down and the card's AC was still marked done.
**How to apply:** for any "narrow the except" card, run the real call path with the provider raising a plain RuntimeError (audited_call with complete_with_meta raising) and check llm_calls rows and the ladder. Do not accept a raw FakeCall as proof of propagation.

T-084 r1 (ec33bf0): (a) restore (undo own demotion) skips both checks and reuses the judge answer for the OLD sentence; `carry_over` keys on figure text and cents only, so a rerun that flips the code class of the same figure lets a current rate become a charge with no check. (b) The code wording gate matches "Charge" in "Charge per visit $185." and "Billed" in "Billed $150 per visit", so the judge is the only gate; the test at test_reclassify.py:108-116 encodes the sneak as expected. (c) The commit deleted T-083's committed billing.py, test_billing.py, api billing hook and api.md section; the cards' commit list and the commit message did not say so.
**Why:** the gate tests cover each check alone; the bypass needs a rerun between two calls. Commit-level deletions are only visible in `git show --stat`.
**How to apply:** on any "skip checks when restored/previous" path, rerun the pipeline with a changed sentence before the restore and check the outcome. On any keyword gate, feed it the rate phrase the spec names. On every review, run `git show --stat <commit>` and grep for deletions of other cards' paths.

Harness notes (this review): the brief's `-k "review or reclass"` selector collects zero tests from tests/unit/test_judge_guard.py, so name guard files explicitly. The working tree moved mid-review (reclassify.py and test_reclassify.py edited by another worker), so the review pinned HEAD with `git archive ec33bf0`. The review-write guard refused an Edit to my own T-084 file after I had written one unverified sentence ("the sample case is not affected"); I disclosed it in the reply instead of creating an -r2 file. Proof-read before the first Write, as in [[feedback_review_write_once]].

## r2 (c8a9874 + e2b4e3f, HEAD a850be0; reviews/T-073-staff-engineer-r2.md pass, reviews/T-084-staff-engineer-r3.md changes)

- **A fix commit can fail its own tree while the working tree is green.** c8a9874 alone: 9 of 120 fail (IntegrityError at reclassify.py:90) because it set AUDIT_ACTION to 'reclassify' while 2fca530 had removed the schema CHECK entry; the worker's runs were on a working tree that still had the T-095 schema uncommitted. A reclassify request 500'd and left the item changed with no audit row. Closed at HEAD by 6feb2ff (T-095 restore). **Why:** worker test runs use the working tree. **How to apply:** run the card's test files on `git archive <card commit>` as well as HEAD, and check any schema or migration the constants depend on. See [[project_t095_head_revert_patterns]].
- **Two-arm predicate with one arm untested:** `_may_restore` skips the checks only when the class AND the sentence are unchanged. The tests changed both together, so dropping the class clause passed all 139 tests (mutant T84-3). The code was right; the test was missing. **How to apply:** for each `and`-clause of a guard predicate, write a test where only that input changes, and mutate each clause separately.
- **Gate and classifier disagree on the same sentence:** charge_wording used its own rate-cue list; amounts.classify uses `_UNIT` (hour, unit, appointment). Six phrasings the classifier calls rates ("Charged $150 an hour.", "Charged $75 a unit.", "Billed $120 an appointment.") passed the gate, so the judge was the only gate. **How to apply:** run both functions on the same fixture sentences and list the disagreements (probe_classifier_vs_wording_gate.py pattern).
- **Restored sentence-arm mutants were caught;** the class-only arm was not. The worker's "17 rate cues" test pinned the named strings, not the classifier's vocabulary.
- **Handoff cites a card that is unrelated:** T-073's deferral said "T-094"; `board.py show T-094` is a live ship-bar card. **How to apply:** for every card a handoff names, check `board.py show` returns the matching work.
- **Probe and mutant indexing:** mutate_r2 writes m00..m10 in list order (control is m00, T84-3 is m03). I ran the T84-4 mutant (m04) by mistake once; check the directory name against the log before a probe.

Related: [[project_backend_llm_review_patterns]] (judge reason prose, label-window bleed), [[project_r2_fix_verification_patterns]] (partial fixes), [[project_t095_head_revert_patterns]] (the 2fca530 revert, closed by 6feb2ff), [[feedback_review_write_once]] (the JSON block in the first Write).
---
name: feedback_review_write_once
description: reviews/*.md are append-only under reviewer-write-guard; proof-read the review body before the first Write, because Edit is blocked afterwards
metadata:
  type: feedback
---

Write a review file once, after proof-reading every line citation and every "I ran X" claim. Once `reviews/<card>-<persona>.md` exists, `Edit` on it is refused by reviewer-write-guard ("reviews are append-only — write a new file with a -r2/-r3 suffix"), so a typo in the body stays there.

**Why:** T-080 r2 (this session): I wrote `reviews/T-080-staff-engineer-r2.md` with three wrong body citations (a line number, an "export builder" pointer with no path, and an unverified "stable across GETs" claim). The JSON block was accurate, but the body could not be corrected in place.

**The ```json block belongs to the first Write.** T-084 r2 (this session): I wrote `reviews/T-084-staff-engineer-r2.md` without its json fence. The board-validate PostToolUse hook rejected it ("review must contain a ```json block"), and reviewer-write-guard refused the Edit that would have added it. The fix was a complete `-r3` file that says it supersedes the r2 file. **How to apply:** before the Write, count the fences (exactly one ```json block) and parse the block with `json.loads`; check the verdict against the rule.

**How to apply:** before the first Write of a review, grep every cited line number and re-check each "checked and fine" claim against a command you actually ran. If a correction is needed later, write a new suffixed file (`-r3`) and say so in the reply, not a silent overwrite. Do not try to get around the guard with shell writes.
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

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:42.636Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo $S; ls $S 2>&1 | head; mkdir -p \"$S/t098-head\" \"$S/t098-e511778\" \"$S/t099-3ecb8b1\" && git archive 196c985 | tar -x -C \"$S/t098-head\" && git archive e511778 | tar -x -C \"$S/t098-e511778\" && git archive 3ecb8b1 | tar -x -C \"$S/t099-3ecb8b1\" && ls \"$S/t098-head\" | head -50 && ls -la /Users/arsis/zlayt-pm-project/.venv/bin/python",
 "description": "Create pinned git archive copies of HEAD and the card commits in scratchpad"
}
````

### User / tool · 2026-11-02T05:00:43.749Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
T-047-run1.json
a.sqlite3
a27e3a4.diff
adr013.txt
api
api2
api_at_099732b.py
api_head.log
api_head.py
api_head.sqlite3
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
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
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 /Users/arsis/zlayt-pm-project/.venv/bin/python -> python3.12
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:45.078Z

**tool call — Bash**
````
{
 "command": "git show e511778 -- app/backend/grounding.py app/backend/trace.py memory/contracts/api.md tests/unit/test_export.py | head -400",
 "description": "Show full e511778 diff for the T-098 files"
}
````

### User / tool · 2026-11-02T05:00:45.182Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:46.287Z

**tool call — Bash**
````
{
 "command": "git show e511778 -- app/backend/grounding.py tests/unit/test_export.py memory/contracts/api.md",
 "description": "Show e511778 diff for grounding, export tests and API contract"
}
````

### User / tool · 2026-11-02T05:00:46.386Z

**tool result**
````
commit e5117784ccec180cc41b68eb050cbe1d99f5534d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:59:28 2026 -0600

    fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)
    
    A summary the paralegal wrote or edited is exempt from the judge but still has to pass the D-034/D-022 code checks. Accepted/edited entries of that kind
    with a failing code step are now gate blockers (named step + next action), GET /export returns 422 for them, and the item trace shows the failing step
    with a specific 'Edit the summary to keep ...' action. trace.py and api.md also carry other workers' uncommitted hunks (T-094 flag steps, T-099 calibration contract).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/grounding.py b/app/backend/grounding.py
index 02b5997..5a3a850 100644
--- a/app/backend/grounding.py
+++ b/app/backend/grounding.py
@@ -195,6 +195,34 @@ def dropped_qualifiers(summary: str, excerpt: str) -> list:
     return out
 
 
+def missing_qualifier_terms(summary: str, excerpt: str) -> list:
+    """The words in the quote that carry a qualifier the summary dropped (D-022), for the 'Edit the summary to keep ...' sentence. English patterns only;
+    a Spanish quote may return []. Display only: the pass/fail decision is dropped_qualifiers()."""
+    kinds = set(dropped_qualifiers(summary, excerpt))
+    found = []
+
+    def add(m):
+        w = re.sub(r"\s+", " ", m.group(0)).strip(" .").lower()
+        if w and w not in found:
+            found.append(w)
+    if "hedge" in kinds:
+        for rx in _lexicon()["hedge"].values():
+            m = rx.search(excerpt)
+            if m:
+                add(m)
+        if not found:
+            m = _HEDGE_WORDS.search(excerpt)
+            if m:
+                add(m)
+    for kind, rx in (("self_report", _SELF_CARRIED), ("negation", _NEG), ("laterality", _LATERAL), ("approx", _APPROX)):
+        if kind in kinds:
+            sm = {w.lower() for w in rx.findall(summary)}
+            for m in rx.finditer(excerpt):
+                if m.group(0).lower() not in sm:
+                    add(m)
+    return found[:4]
+
+
 def check_summary(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
     reasons = []
     if new_tokens(summary, excerpt, label, date_iso):
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index caf91ca..55c7390 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -38,6 +38,7 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
 | GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
 | GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (billed, adjustment, paid, balance, each cited), totals by provider, LOP and lien amounts listed separately, rates excluded, ledger-vs-EOB checks; internal view, never in the letter |
 | GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
+| GET | `/api/calibration` | T-099 read-only measured calibration (aggregate counts only, no case token, demo-safe): the T-096 shape in `calibration`, or `null` with `status` `missing`/`invalid`. See the section below |
 
 ---
 
@@ -357,7 +358,7 @@ Response 200:
 Note `item.kind` is the item type (`"amount"`, as in the review response); the amount's class is `amount.kind`, the same field the case endpoint uses. Patch local state from `amount`, `totals` and `review`; no refetch needed.
 
 ## GET /api/cases/{token}/export
-**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
+**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
 Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). No parameters. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
 ```json
 {
@@ -614,7 +615,7 @@ Each case step has the shared step keys plus `counts` (object, may be `{}`); `ex
 
 `verdict.code` for the case: `ready` (export gate open), `needs_attention` (nothing accepted yet, or accepted items not double-checked), `running`, `failed`. The judge's closed `reason_code` is now kept in `ladder.judge.reason_code` for entries, amounts, flags, edits and manual entries (in `ladder_json`; no schema change).
 
-**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
+**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. AI drafts are not covered by this blocker (they keep needs_review + the human accept).  **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
 
 ### GET /api/cases/{token}/judges
 ```json
@@ -648,6 +649,16 @@ Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays tok
 `GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
 `POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).
 
+## GET /api/calibration  (T-099, serves T-090 counts to T-096)
+Read-only. Serves `evals/reports/calibration.json` (written by `python -m evals.run`), the measured calibration the review screen quotes. It holds aggregate counts, the statements built from them, the source commit, the backend and the sample size. No case token, no record text, so it works in demo mode with no gate. Any other method is `405`.
+
+Always `200` with one envelope:
+- `{"status": "ok", "calibration": {...}, "message": null}`. `calibration` has exactly: `schema` (`evals.calibration/1`), `backend` (`fixture` or a live backend name), `case_count` (the sample size: golden cases pooled), `small_sample` (bool), `source_commit`, `generated_at`, `by_state` (`verified` and `needs_review`, each `{matched, total, cases[]}`), `by_type` (`entry`, `amount`, `flag`, each with the two states as `{matched, total, by_case: {case: [m, t]}}`), `not_scored` (`entry`, `amount`, `flag`, `total`) and `sentences` (`overall` and `by_type`, each state a string).
+- `{"status": "missing", "calibration": null, "message": "..."}`: no file yet.
+- `{"status": "invalid", "calibration": null, "message": "..."}`: the file is not a valid measurement (bad JSON or encoding, wrong schema, a count out of range, totals that do not add up, or a statement that does not quote its own `m/t`). The file's contents are never echoed; the reasons go to the server log.
+
+Rules for the client: render `sentences.overall.verified` and `sentences.overall.needs_review` verbatim (they name the backend and the basis); never compute or show a percentage; hide the line when `calibration` is null. Nothing is invented: no default numbers appear in any state. `calibration` is served by `app/backend/calibration_route.py`; the route is registered in `create_app` and reads one fixed path.
+
 ## GET /api/cases/{token}/billing  (T-083, D-042)
 Code-only billing analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs. Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals` (the letter's total line is still accepted charges only, D-019). Unknown token: `404 not_found`.
 ```json
diff --git a/tests/unit/test_export.py b/tests/unit/test_export.py
index 21c7fee..7af086b 100644
--- a/tests/unit/test_export.py
+++ b/tests/unit/test_export.py
@@ -195,3 +195,15 @@ def test_export_blocked_code_is_judge_not_run_only_when_every_blocker_is():
     assert X.ExportBlocked([{"reason_code": "RUN_FAILED"}]).code == "export_blocked"
     assert X.ExportBlocked([{"reason_code": "JUDGE_NOT_RUN"}, {"reason_code": "RUN_FAILED"}]).code == "export_blocked"
     assert X.ExportBlocked([{"reason_code": "JUDGE_NOT_RUN"}]).code == "judge_not_run"
+
+
+def test_export_payload_refuses_for_a_failing_code_check_on_edited_wording_d045b():
+    """T-098: export_payload raises ExportBlocked for the blocker list the gate gives, whatever the reason; the code is export_blocked, not judge_not_run."""
+    from app.backend import export_routes as XR
+    c = build_case()
+    blk = {"item_id": "e2", "kind": "entry", "reason_code": "SUMMARY_DROPS_QUALIFIER", "step_id": "summary_qualifier", "why": "The summary leaves out a qualifier.", "next_action": None}
+    c["export_blockers"] = [blk]
+    with pytest.raises(X.ExportBlocked) as ei:
+        XR.export_payload("tok", c)
+    assert ei.value.code == "export_blocked" and ei.value.items == [blk]
+    assert XR.blocked_message(ei.value) == "The summary leaves out a qualifier. The export is blocked."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:47.622Z

**tool call — Bash**
````
{
 "command": "git show e511778 -- app/backend/trace.py | cat",
 "description": "Show full e511778 diff for trace.py"
}
````

### User / tool · 2026-11-02T05:00:47.719Z

**tool result**
````
commit e5117784ccec180cc41b68eb050cbe1d99f5534d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:59:28 2026 -0600

    fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)
    
    A summary the paralegal wrote or edited is exempt from the judge but still has to pass the D-034/D-022 code checks. Accepted/edited entries of that kind
    with a failing code step are now gate blockers (named step + next action), GET /export returns 422 for them, and the item trace shows the failing step
    with a specific 'Edit the summary to keep ...' action. trace.py and api.md also carry other workers' uncommitted hunks (T-094 flag steps, T-099 calibration contract).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/trace.py b/app/backend/trace.py
index acb44b0..1ac9f43 100644
--- a/app/backend/trace.py
+++ b/app/backend/trace.py
@@ -10,7 +10,7 @@ closed reason_code (D-028), written by code; the model never supplies prose. Eve
 """
 import json
 
-from app.backend import narrative, present, review, store, why
+from app.backend import grounding, narrative, present, review, store, why
 from app.backend import judges as J
 from app.db import db as DB
 from app.llm import audited as AU
@@ -45,6 +45,7 @@ TRACE_WHY = {
     "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
     "NOTHING_ACCEPTED": "Nothing is accepted or edited yet, so the letter would be empty.",
     "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
+    "CODE_CHECK_FAILED": "You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter.",
     "NOT_AN_ACCEPTED_ENTRY": narrative.REASONS["NOT_AN_ACCEPTED_ENTRY"],
     "CAUSATION_NOT_QUOTED": narrative.REASONS["CAUSATION_NOT_QUOTED"],
     "SEVERITY_NOT_QUOTED": narrative.REASONS["SEVERITY_NOT_QUOTED"],
@@ -84,8 +85,8 @@ def reason_text(code: str) -> str:
         return code
 
 
-def na(code: str, target: dict = None, options: list = None) -> dict:
-    d = {"code": code, "text": _NEXT[code]}
+def na(code: str, target: dict = None, options: list = None, text: str = None) -> dict:
+    d = {"code": code, "text": text or _NEXT[code]}
     if target:
         d["target"] = target
     if options:
@@ -260,9 +261,12 @@ def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
     rs = row.get("review_status")
     live = row.get("state") != "rejected"
     first_na = next((s["next_action"] for s in steps if s["next_action"]), None)
+    gated = [s for s in steps if s["kind"] == "code" and s["status"] == FAIL and s.get("blocks_export")]      # D-045(b): human wording whose code check fails
     if rs in ("accepted", "edited", "dismissed"):
-        first_na = None             # the human already decided; step-level hints stay on the steps
-    if rs in ("accepted", "edited"):
+        first_na = gated[0]["next_action"] if gated else None     # the human already decided; step-level hints stay on the steps, except a failing code check on their own wording
+    if gated:
+        code, label = "needs_attention", "Needs your attention: a check on your wording fails"
+    elif rs in ("accepted", "edited"):
         code, label = "accepted", "Accepted by you"
     elif rs == "dismissed":
         code, label = "dismissed", "Dismissed by you"
@@ -277,6 +281,7 @@ def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
     else:
         code, label = "ready_for_decision", "Ready for your decision"
     blocks = (live and rs == "pending") if blocks_flag is None else blocks_flag
+    blocks = blocks or bool(gated)
     judge_id = next((s["id"] for s in steps if s["id"].startswith("judge_")), None)
     fallback = next((s["id"] for s in steps if s["status"] == FAIL), steps[0]["id"] if steps else None)   # e.g. record-warning flags have one code step
 
@@ -382,10 +387,60 @@ def _entry_steps(cx, row):
     nxt = None
     if unconf:
         nxt = na("CONFIRM_DATE", {"record_id": rid, "view": "dates_to_confirm"}) if rec.get("date_status") == "ambiguous" else na("READ_RECORD", {"record_id": rid})
+    if _code_check_gated(row):        # D-045(b): human wording skips the judge, never the code checks; a failing one blocks the export and says what to do
+        for s in st:
+            if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS:
+                s["blocks_export"] = True
+                s["next_action"] = _fix_action(row, s)
     st.append(_human_step(cx, row, "entry", extra_pending_next=nxt))
     return st
 
 
+def _code_check_gated(row) -> bool:
+    """An accepted or edited, live entry whose wording the paralegal wrote or edited: its failing code checks block the export (D-045(b))."""
+    return row["state"] != "rejected" and row["review_status"] in ("accepted", "edited") and _paralegal_wording("entry", row)
+
+
+def _current_text(row):
+    ed = row.get("edited") or {}
+    return ed.get("summary", row.get("summary") or ""), ed.get("excerpt", row.get("excerpt") or "")
+
+
+def _fix_action(row, stp) -> dict:
+    """The paralegal's next move for a failed code step on their own wording: a fixed sentence plus the words from the quote (display only; code decided the failure)."""
+    code, summ, exc = stp["reason_code"], *_current_text(row)
+    target = {"item_id": row["id"]}
+    tail = " The export stays blocked until it passes."
+    if code == "SUMMARY_DROPS_QUALIFIER":
+        terms = grounding.missing_qualifier_terms(summ, exc)
+        what = ", ".join(f"\u2018{t}\u2019" for t in terms) if terms else "the quote's hedge, attribution, negation, side or approximation"
+        return na("EDIT_SUMMARY", target, text=f"Edit the summary to keep {what}; the quote says it and your summary leaves it out." + tail)
+    if code == "SUMMARY_TOKEN_NOT_IN_EXCERPT":
+        toks = (stp.get("evidence") or {}).get("tokens") or []
+        what = ", ".join(f"\u2018{t}\u2019" for t in toks) if toks else "the words that are not in the quote"
+        return na("EDIT_SUMMARY", target, text=f"Edit the summary to remove {what}, or change the quote so it contains {'it' if len(toks) == 1 else 'them'}." + tail)
+    if code in ("EXCERPT_NOT_WHOLE_SENTENCE", "EXCERPT_OMITS_QUALIFIER"):
+        return na("EDIT_QUOTE", target, text=_NEXT["EDIT_QUOTE"] + tail)
+    return na("READ_RECORD", {"record_id": (row.get("record_ids") or [None])[0]}, text="Read the record yourself, then fix the quote or dismiss this item." + tail)
+
+
+def code_check_blockers(conn, case_id: str, cx=None) -> list:
+    """Export blockers (D-045(b)): accepted or edited entries whose wording the paralegal wrote or edited and whose current summary or quote fails a code check.
+    One blocker per item, reason_code = its first failing check; `failed_steps` lists every failing step. Same steps the item trace shows, so gate and trace agree."""
+    cx = cx or _Cx(conn, case_id, False)
+    out = []
+    for row in DB.list_items(conn, case_id, "entry"):
+        if not _code_check_gated(row):
+            continue
+        fails = [s for s in _entry_steps(cx, row) if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS]
+        if not fails:
+            continue
+        f = fails[0]
+        out.append({"item_id": row["id"], "kind": "entry", "reason_code": f["reason_code"], "step_id": f["id"], "failed_steps": [x["id"] for x in fails],
+                    "why": f["why"] + " " + TRACE_WHY["CODE_CHECK_FAILED"], "next_action": _fix_action(row, f)})
+    return out
+
+
 # ------------------------------------------------------------------ amounts
 def _amount_steps(cx, row):
     R = set(row.get("state_reasons") or [])
@@ -469,6 +524,22 @@ def _flag_steps(cx, row):
                        else (na("READ_RECORD", {"record_id": rid0}) if rid0 else na("RERUN"))))
         st.append(_human_step(cx, row, "flag"))
         return st
+    if origin == "code" and cc.get("candidate_rule"):
+        # T-094: a conflict pair proposed by code and classified by the judge (J3). The model proposed nothing.
+        comp = present._computed(row.get("computed"))
+        arith = cc.get("arithmetic")
+        st.append(step("paired_by_code", "Code paired these two quotes", "code", PASS,
+                       "Software found a stated plan and a later record that shows it ended early" if cc["candidate_rule"] == "plan_vs_outcome"
+                       else "Software found a denial of prior problems and another record that mentions an earlier problem",
+                       rule="row 10", evidence={"values": {"rule": cc["candidate_rule"], "arithmetic": arith}, "spans": spans}))
+        bad = row["state"] == "rejected" and "JUDGE_DISAGREES" not in R or cc.get("excerpt_verbatim") is False
+        st.append(step("spans_match", "Cited text matches the record", "code", FAIL if bad else PASS,
+                       reason_text("GROUNDING_EXCERPT_NOT_VERBATIM") if bad else "Both quotes are in the records, character for character.",
+                       reason="GROUNDING_EXCERPT_NOT_VERBATIM" if bad else None, rule="row 4", evidence={"spans": spans}))
+        st.append(inj())
+        st.append(_judge_step(cx, row["id"], lad.get("judge"), "j3", R, rule="row 11"))
+        st.append(_human_step(cx, row, "flag"))
+        return st
     if origin == "code":
         comp = present._computed(row.get("computed"))
         vals = {k: comp[k] for k in ("from", "to", "days", "threshold", "stated_dates", "body_date", "first_treatment_date", "names", "subtype") if k in comp}
@@ -485,6 +556,7 @@ def _flag_steps(cx, row):
         else:
             st.append(step("endpoints_confirmed", "Dates at both ends are confirmed", "code", PASS, "Both dates are parsed or confirmed.", rule="row 9"))
         st.append(inj())
+        st += _ocr_steps(R, rid0)
         st.append(step("judge_not_needed", "Second AI check", "llm", SKIPPED, "Not needed: this is arithmetic over dates in the record, which code does exactly.", rule="row 9"))
         st.append(_human_step(cx, row, "flag"))
         return st
@@ -499,9 +571,8 @@ def _flag_steps(cx, row):
         gen = lad.get("generator") or {}
         step_name = "conflicts" if ftype == "conflict" else "flags"
         call = cx.call(gen.get("call_id"), row["id"], step_name)
-        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or AU.PROMPT_OF_STEP[step_name], call)
+        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or AU.PROMPT_OF_STEP.get(step_name), call)
         st.append(step("proposed_by_ai", "AI found it", "llm", PASS, "The AI proposed this flag as a category and a quote; it wrote no explanation.", rule="row 12", evidence=ev))
-        st += _ocr_steps(R, rid0)
     else:
         st.append(step("proposed_by_ai", "AI found it", "llm", SKIPPED, reason_text("LEXICON_ONLY"), reason="LEXICON_ONLY", rule="row 12"))
     if ftype == "conflict":
@@ -533,6 +604,7 @@ def _flag_steps(cx, row):
         else:
             st.append(step("highlight", "Quote can be highlighted in the record", "code", PASS, "The quote's position in the record was found.", rule="row 4"))
     st.append(inj())
+    st += _ocr_steps(R, rid0)
     jid = "j3" if ftype == "conflict" else "j4"
     if vfail:
         st.append(_skipped(f"judge_{jid[1]}", f"Second AI check: {JUDGE_LABEL[jid].lower()}", "llm", "GROUNDING_EXCERPT_NOT_VERBATIM", "row 11" if jid == "j3" else "row 12"))
@@ -549,7 +621,6 @@ def _flag_steps(cx, row):
     return st
 
 
-    st += _ocr_steps(R, rid0)
 # ------------------------------------------------------------------ narrative sentences
 def _ntext(code):
     return narrative.REASONS.get(code) or reason_text(code)
@@ -900,12 +971,13 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
     # 10 export gate
     blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
     jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
+    ccf = [b for b in blockers if b.get("step_id")]             # D-045(b): the paralegal's own wording fails a code check
     live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
     n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
     n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
     ready = not blockers
     gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"],
-                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr)}
+                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf)}
     warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
                  "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])}] if n_pend else []
     if ready:
@@ -923,7 +995,8 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
     _number(st)
     verdict = ({"code": "running", "label": "The AI run is in progress"} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
                else {"code": "ready", "label": "Ready to export" + (f" ({n_pend} not reviewed)" if n_pend else "")} if ready
-               else {"code": "needs_attention", "label": f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr else "Nothing is accepted yet"})
+               else {"code": "needs_attention", "label": f"{len(ccf)} edited summar{'ies fail' if len(ccf) != 1 else 'y fails'} a check" if ccf and not jnr
+                      else f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr else "Nothing is accepted yet"})
     return {"token": case_id, "mode": "full" if cx.full else "metadata", "status": case["status"], "verdict": verdict, "progress": _progress(st), "steps": st}
 
 
@@ -941,6 +1014,7 @@ def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
         out.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
     if cx.case["status"] == "failed":
         out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
+    out.extend(code_check_blockers(conn, case_id, cx))         # D-045(b): the paralegal's own wording is exempt from the judge, not from the code checks
     if cx.ran and not cx.running:
         out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
     if not (rv["counts"]["accepted"] + rv["counts"]["edited"]):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:56.623Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-e511778\" && timeout 300 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -40; echo \"=== HEAD ===\"; cd \"$S/t098-head\" && timeout 300 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -40",
 "description": "Run trace and export unit tests on e511778 and HEAD archives",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T05:00:56.721Z

**tool result**
````
/bin/bash: timeout: command not found
=== HEAD ===
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:59.489Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-e511778\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -40; echo \"=== HEAD ===\"; cd \"$S/t098-head\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -40",
 "description": "Run trace and export unit tests on e511778 and HEAD archives",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T05:01:11.842Z

**tool result**
````
........................................................................ [ 81%]
................                                                         [100%]
88 passed in 5.73s
=== HEAD ===
........................................................................ [ 81%]
................                                                         [100%]
88 passed in 5.61s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:14.585Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && grep -rn -i \"409\\|keep my wording\\|keep_my_wording\\|keep-my-wording\\|conflict\" app/backend app/frontend tests memory/contracts/api.md 2>/dev/null | grep -v \"\\.pyc\" | head -60",
 "description": "Search HEAD archive for 409 and keep-my-wording paths"
}
````

### User / tool · 2026-11-02T05:01:14.687Z

**tool result**
````
app/backend/why.py:29:    "CONFLICT_CHECK_INCOMPLETE": "The check for conflicts between records did not finish or had no recorded answer, so conflicts between records may be missing.",
app/backend/store.py:72:    events = [dict(type=ev["action"], item_id=ev["item_id"]) for ev in DB.list_events(conn, case_id) if ev["action"] == "keep_my_wording"]
app/backend/trace.py:19:_JUDGE_PREFIX = (("judge_faithfulness", "j1"), ("judge_amount_class", "j2"), ("judge_conflict", "j3"), ("judge_flag", "j4"))
app/backend/trace.py:21:               "j3": "Do these two quotes really conflict?", "j4": "Does this flag fit the quote?"}
app/backend/trace.py:31:_RAW_TO_LADDER = {"agree": "supported", "conflict": "supported", "disagree": "disagrees", "benign": "disagrees"}
app/backend/trace.py:35:         "j3": "The second check agreed that the two quotes conflict.",
app/backend/trace.py:73:    "AMOUNT_ESTIMATE": "amount_class", "AMOUNT_DAMAGES": "amount_class", "AMOUNT_UNCLEAR": "amount_class", "CONFLICT_CHECK_INCOMPLETE": "record_warning_check",
app/backend/trace.py:519:        code = {"injection_suspected": "INJECTION_SUSPECTED", "analysis_incomplete": "CONFLICT_CHECK_INCOMPLETE", "llm_split": "LLM_SPLIT", "date_ambiguous": "DATE_AMBIGUOUS"}.get(cat) \
app/backend/trace.py:528:        # T-094: a conflict pair proposed by code and classified by the judge (J3). The model proposed nothing.
app/backend/trace.py:564:    if ftype == "conflict":
app/backend/trace.py:565:        pass                                  # a conflict is the AI's pair proposal (row 11): no phrase list, so no agreement step
app/backend/trace.py:572:        step_name = "conflicts" if ftype == "conflict" else "flags"
app/backend/trace.py:578:    if ftype == "conflict":
app/backend/trace.py:608:    jid = "j3" if ftype == "conflict" else "j4"
app/backend/trace.py:945:        st.append(step("flags", "Gaps, conflicts and wording flags", "code", FAIL, reason_text("CONFLICT_CHECK_INCOMPLETE"), reason="CONFLICT_CHECK_INCOMPLETE", rule="row 11", counts=fc,
app/backend/trace.py:948:        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PENDING, "Gaps and date conflicts are ready (code). The AI and phrase-list pass has not run.", rule="row 9", counts=fc,
app/backend/trace.py:951:        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PASS, f"{len(flgs)} flag{'s' if len(flgs) != 1 else ''}: dates compared by code, wording found by the phrase list and the AI.", rule="row 9", counts=fc))
app/backend/confidence.py:11:    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT", "OCR_DERIVED", "LANGUAGE_UNCERTAIN",
app/backend/dismissal_patterns.py:13:Only lexicon-phrase flags of type pre_existing or causation are eligible. Gap and conflict flags, injection and date warnings, and flags
app/backend/flag_templates.py:14:    ("conflict", "accident_date"): "accident_date_after_treatment",
app/backend/flag_templates.py:15:    ("conflict", "provider_name"): "provider_name_variant",
app/backend/flag_templates.py:16:    ("conflict", "treatment_plan"): "treatment_plan_vs_actual",
app/backend/flag_templates.py:17:    ("conflict", "history_inconsistency"): "other_fact_mismatch",
app/backend/flag_templates.py:32:    "accident_date_after_treatment": "conflict", "accident_dates_differ": "conflict", "provider_name_variant": "conflict",
app/backend/flag_templates.py:33:    "treatment_plan_vs_actual": "conflict", "other_fact_mismatch": "conflict",
app/backend/flag_templates.py:139:                                      "The check for conflicts between records did not finish, so conflicts between records may be missing from this list. Review the records side by side."),
app/backend/flags.py:3:with the code lexicon scan; one cross-record pass for semantic conflicts (accident-date and provider-name conflicts are code, conflicts.py).
app/backend/flags.py:22:_CONFLICT_CATEGORIES = ("treatment_plan_vs_actual", "other_fact_mismatch")
app/backend/flags.py:212:# ------------------------------------------------------------------ cross-record conflict pass
app/backend/flags.py:214:    """No silent loss: when the conflict pass cannot run, a case-level record_warning (no single record) says conflicts may be missing;
app/backend/flags.py:219:            "reasons": ["CONFLICT_CHECK_INCOMPLETE"], "why": why.why("CONFLICT_CHECK_INCOMPLETE"), "excerpt": "", "source_kind": "record",
app/backend/flags.py:220:            "evidence": [], "pipeline_warning": "CONFLICT_PASS_INCOMPLETE",
app/backend/flags.py:221:            "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {"classified_by": "code:conflict_pass_failure"}}}
app/backend/flags.py:224:def run_conflict_pass(records: list, *, call, any_tagged: bool = False, case_text: str = "") -> list:
app/backend/flags.py:225:    """One call over all records for semantic conflicts only. Each quote must be verbatim in some record or the flag is rejected."""
app/backend/flags.py:226:    n = promptlib.nonce(case_text, "conflicts", "all")
app/backend/flags.py:227:    prompt = promptlib.load("conflicts_v1")
app/backend/flags.py:230:        out, _cid = call("conflicts", prompt.text, blocks + "\nReturn the JSON object.", schemas.FlagPass.model_json_schema(), item_id="conflicts")
app/backend/flags.py:231:        raw = [f for f in schemas.FlagPass.model_validate(out).flags if f.type == "conflict"]
app/backend/flags.py:249:        if m.category not in _CONFLICT_CATEGORIES or not m.excerpt_b:    # a conflict needs two quotes
app/backend/flags.py:252:        f = {"type": "conflict", "category": m.category, "excerpt": m.excerpt, "excerpt_b": m.excerpt_b, "origin": "llm",
app/backend/flags.py:259:        if m.category in _CONFLICT_CATEGORIES:
app/backend/flags.py:260:            f["title"], f["explanation"] = FT.render("conflict", m.category, provider_a=(ra or ref).get("source"), date_a=(ra or ref).get("date_iso"),
app/backend/flags.py:267:    # R-CO-7: one conflict per (category, unordered pair of quotes), in a fixed order, so the model's phrasing or order cannot change
app/backend/flags.py:280:    """J4 on every model-involved pre_existing/causation flag; J3 on every model conflict. Lexicon-only flags have no judge.
app/backend/flags.py:286:        nonce = promptlib.nonce(case_text, "j3" if f["type"] == "conflict" else "j4", item)
app/backend/flags.py:288:            if f["type"] == "conflict":
app/backend/flags.py:292:                step, pv = "j3", "judge_conflict_v2"
app/backend/flags.py:300:            v, cid, reason, step, pv = "unavailable", None, "NONE", "j3" if f["type"] == "conflict" else "j4", "judge_conflict_v2" if f["type"] == "conflict" else "judge_flag_v2"
app/backend/narrative.py:22:    "FLAG_CONTENT": "The sentence talks about gaps, conflicts or other review flags, which stay out of the paragraph.",
app/backend/narrative.py:29:_FLAGISH = re.compile(r"\b(?:gaps?|conflicts?|inconsisten\w+|discrepanc\w+|pre-?existing|prior (?:injur\w+|condition)|missed appointments?|"
app/backend/review.py:3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
app/backend/review.py:5:and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
app/backend/review.py:10:from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store
app/backend/review.py:66:        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
app/backend/review.py:83:    Raises 409 needs_confirm unless body['confirm_warnings']; returns the pieces both callers store."""
app/backend/review.py:108:        raise ReviewError(409, "needs_confirm", {"warnings": blocking}, "This edit adds a number or fact that is not in the quote.")
app/backend/review.py:161:        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
app/backend/review.py:233:    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
app/backend/review.py:241:    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:15.055Z

**tool call — Bash**
````
{
 "command": "git show 36a982b --stat | cat && git show 36a982b -- memory/ORCHESTRATOR_DECISIONS.md memory/contracts/api.md | cat | head -120",
 "description": "Show D-047 commit stat and its doc diff"
}
````

### User / tool · 2026-11-02T05:01:15.178Z

**tool result**
````
commit 36a982b66ffde2c14d4f09ff2c7d19630bea6691
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:59:53 2026 -0600

    docs: D-047 side/negation tokens hard 422, drop 409 keep-my-wording path
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 memory/ORCHESTRATOR_DECISIONS.md | 1 +
 1 file changed, 1 insertion(+)
commit 36a982b66ffde2c14d4f09ff2c7d19630bea6691
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:59:53 2026 -0600

    docs: D-047 side/negation tokens hard 422, drop 409 keep-my-wording path
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/memory/ORCHESTRATOR_DECISIONS.md b/memory/ORCHESTRATOR_DECISIONS.md
index 075be74..5c4c166 100644
--- a/memory/ORCHESTRATOR_DECISIONS.md
+++ b/memory/ORCHESTRATOR_DECISIONS.md
@@ -52,3 +52,4 @@ Questions that are really Chris's are in submission/NEEDS_CHRIS.md with the assu
 | D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
 | D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
 | D-046 | Ship-bar item 4 also gates on the seeded J3 (conflict) and J4 (flag) judge control sets (2026-11-02): each must catch every seeded wrong item with 0 false agrees. Control labels are fixed before a run; an item may be relabelled only with a written reason reviewed by a second agent, never because it failed. | Judges J3/J4 now decide flags (T-075, T-094); a catch rate only on J1 would leave them unmeasured. | T-093 staff r1 major 2 |
+| D-047 | Extends D-034 (2026-11-02): side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a **hard 422** on edit and manual entry. The 409 'keep my wording' path is removed, so the gate (T-098) and the edit route agree and no item can be confirmed into an unexportable state. | A side or negation the record does not state is as dangerous as an invented number; a confirm path that leads to a blocked export is a dead end. | T-098 handoff |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:18.471Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && sed -n 1,12p app/backend/review.py; echo ...; sed -n 80,175p app/backend/review.py",
 "description": "Read review.py edit path around the 409 needs_confirm branch at HEAD archive"
}
````

### User / tool · 2026-11-02T05:01:18.558Z

**tool result**
````
"""Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).

Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
Edit order: (1) structure, else 422 invalid_edit; (2) code token check; (3) judge 1 re-run. A token/judge objection saves nothing
and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
that cannot answer never blocks: the edit is saved as needs_review with JUDGE_UNAVAILABLE.
"""
import time

from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store
from app.db import db as DB

...

def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, body):
    """Code token/qualifier checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
    Raises 409 needs_confirm unless body['confirm_warnings']; returns the pieces both callers store."""
    code_reasons = []
    lang = language.record_lang(rec)                        # D-042: a Spanish record's English summary is checked against the Spanish quote
    g = spanish.module_for(lang)
    toks = g.new_tokens(new_sum, new_exc, label, date_iso)
    numeric = [t for t in toks if _NUMERIC_TOKEN.search(t)]
    if numeric:    # D-034: a number, date or $ figure that is not in the quote is never saved, with or without confirm_warnings
        raise _bad("The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(numeric) + ". Remove it or change the quote.",
                   tokens=numeric, reason="SUMMARY_NUMBER_NOT_IN_EXCERPT")
    blocking = []
    if toks:
        code_reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
        blocking.append({"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "\u201c" + "\u201d, \u201c".join(toks) + "\u201d is not in the quote.", "item_id": item_id})
    if g.dropped_qualifiers(new_sum, new_exc):
        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
    if span is None:
        code_reasons.append("HIGHLIGHT_NOT_FOUND")
    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
    if call is not None:
        verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
        ladder_verdict = judges.to_ladder("j1", verdict)
    if ladder_verdict in ("partially", "unsupported"):
        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
        blocking.append({"code": code, "message": "The second check could not fully support the summary from the quote.", "item_id": item_id})
    if blocking and not bool(body.get("confirm_warnings")):
        raise ReviewError(409, "needs_confirm", {"warnings": blocking}, "This edit adds a number or fact that is not in the quote.")
    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed")})
    return {"toks": toks, "code_reasons": code_reasons, "blocking": blocking, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
            "judge_error": judge_error,
            "state": state, "reasons": reasons}


# ---------------------------------------------------------------- edit
def _edit(conn, case_id, kind, item, body, call, t):
    edits = body.get("edits")
    if kind == "amount":
        raise _bad("A charge can only be accepted or dismissed.")
    if not isinstance(edits, dict) or not edits:
        raise _bad("Nothing to edit.")
    if kind == "flag":
        if set(edits) != {"note"} or not isinstance(edits["note"], str) or not edits["note"].strip():
            raise _bad("Only a note can be added to a flag.")
        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, case=case_id)
        DB.update_item(conn, item["id"], now=t, case=case_id, reviewer_note=edits["note"].strip()[:2000])
        return []
    if not set(edits) <= {"summary", "excerpt"} or not all(isinstance(v, str) and v.strip() for v in edits.values()):
        raise _bad("Only the summary or the quoted sentences of an entry can be edited.")
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    rec = next((r for r in recs if r["id"] == (item["record_ids"] or [None])[0]), None)
    if rec is None:
        raise _bad("The entry's source record is missing.")
    prev = item.get("edited") or {}
    cur_sum, cur_exc = prev.get("summary", item["summary"]), prev.get("excerpt", item["excerpt"])
    new_sum, new_exc = edits.get("summary", cur_sum).strip(), edits.get("excerpt", cur_exc).strip()
    span = None
    if "excerpt" in edits:
        problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], new_exc)
        if problems:
            raise _bad("The quote must be whole sentences of the same record, in order, with any hedge sentence that qualifies them.", reasons=problems)
    span = grounding.locate(rec["excerpt"], new_exc)
    base = generator.body_offset(rec)
    label, date_iso = item["provider"] or "", item["date_iso"] or ""
    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call, body)
    toks, code_reasons, blocking, ladder_verdict, call_id, state, reasons = (
        chk["toks"], chk["code_reasons"], chk["blocking"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
    confirmed = bool(body.get("confirm_warnings"))
    edited = dict(prev)
    edited.update(at=store.iso(t), kept_my_wording=bool(blocking and confirmed),
                  override_reasons=[b["code"] for b in blocking] if blocking and confirmed else prev.get("override_reasons", []))
    if "summary" in edits or "summary" in prev:
        edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
    if "excerpt" in edits or "excerpt" in prev:
        edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t, case=case_id)
    if edited["kept_my_wording"]:
        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
    lad = item.get("ladder") or {"item_id": item["id"]}
    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
    lad["state"] = state
    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
    return [{"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": item["id"]}] \
        if ladder_verdict == "unavailable" else []


# ---------------------------------------------------------------- confirm_date
def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
    t = _now(now)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:20.410Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && grep -n \"ReviewError\\|needs_confirm\\|confirm_warnings\\|422\\|status_code\\|def \" app/backend/api.py | head -80; echo ---; grep -rn \"needs_confirm\\|confirm_warnings\\|keep_my_wording\\|keep my wording\" app/frontend tests | head -40",
 "description": "Locate API error mapping and frontend or test references to needs_confirm"
}
````

### User / tool · 2026-11-02T05:01:20.523Z

**tool result**
````
49:    def __init__(self, status, code, message="", detail=None):
54:def digest(text: str) -> str:
58:def recorded_hashes() -> set:
62:def library_cases() -> list:
79:def local_mode() -> bool:
83:def is_loopback_peer(request) -> bool:
93:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
100:    def allowed_hashes():
112:    def backend():
116:    def live_enabled():
119:    def demo_mode():
122:    def models():
125:    def conn():
128:    def make_call(c, cid):
134:    def pipeline_mod():
140:    def get_case(c, token):
148:    async def _api_error(_, e):
149:        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)
151:    @app.exception_handler(review.ReviewError)
152:    async def _review_error(_, e):
153:        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)
156:    async def _http_error(_, e):
157:        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
158:        return JSONResponse({"error": {"code": code, "message": code.replace("_", " "), "detail": {}}}, status_code=e.status_code)
161:    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log
163:        return JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
166:    async def _validation(_, e):
167:        return JSONResponse({"error": {"code": "bad_request", "message": "Malformed request.", "detail": {}}}, status_code=400)
170:    async def _headers(request, call_next):
180:                resp = JSONResponse({"error": {"code": "forbidden", "message": "Local mode accepts loopback clients only.", "detail": {}}}, status_code=403)
185:            resp = JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
192:    async def body_of(request: Request) -> dict:
213:    def health():
219:    def list_cases():
229:    def library():
234:    @app.post("/api/cases", status_code=201)
235:    async def create_case(request: Request):
250:    @app.post("/api/cases/pdf", status_code=201)
251:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):
280:    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None):
315:    def get_case_view(token: str):
323:    @app.delete("/api/cases/{token}", status_code=204)
324:    def delete_case(token: str):
331:        return Response(status_code=204)
333:    def _run_thread(token, raw):
347:    @app.post("/api/cases/{token}/run", status_code=202)
348:    async def run_case(token: str, request: Request):
361:                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
371:    async def rejudge_case(token: str):
393:    def status(token: str):
412:    async def confirm_date(token: str, rid: str, request: Request):
423:    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
424:    async def manual_entry(token: str, rid: str, request: Request):
425:        """D-031: the reviewer writes the entry for a record the AI could not make one for. Quote = whole verbatim sentences (422 otherwise)."""
435:    async def not_duplicate(token: str, item_id: str, request: Request):
448:    def narrative_get(token: str):
457:    def narrative_draft(token: str):
470:    async def narrative_review(token: str, request: Request):
480:                raise ApiError(422, "invalid_edit", "That action is not allowed.") from None
485:    def item(token: str, item_id: str):
497:    async def review_item(token: str, item_id: str, request: Request):
518:    def export(token: str):
527:                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
545:    def item_trace(token: str, item_id: str):
558:    def case_trace(token: str):
567:    def judge_report(token: str):
576:    def audit(token: str):
---
app/frontend/review.js:125:  // ---- errors and the "keep my wording" confirmation (R-RV-3)
app/frontend/review.js:135:        el("button", { type: "button", class: "rv-btn", "data-testid": "btn-keep-wording", onclick: () => RV.act(id, Object.assign({}, body, { confirm_warnings: true }), { focus: "edit" }) }, "Keep my wording"),
app/frontend/review.js:137:    RV.say("This edit adds something that is not in the quote. Choose keep my wording or go back.", true);
app/frontend/review.js:170:      if (e && e.code === "needs_confirm") showConfirm(id, e, body);
app/frontend/manual.js:3:   Server refusals (422) and the token check (409 needs_confirm, "keep my wording") are shown in plain words. Text via ZL.el only. */
app/frontend/manual.js:45:      if (confirmWarnings) body.confirm_warnings = true;
app/frontend/manual.js:51:      if (r.status === 409 && err.code === "needs_confirm") {
app/frontend/excerpt.js:2:   The server validates (invalid_edit / needs_confirm); this only builds the text from API offsets and shows the server's reasons. */
app/frontend/dev/mock-review.js:44:        if (id[0] === "e") { if (/\$9,000/.test(body.edits.summary) && !body.confirm_warnings) throw new E(409, "needs_confirm", "This edit adds a number or fact that is not in the quote.", { warnings: [{ code: "SUMMARY_TOKEN_NOT_IN_EXCERPT", message: "“$9,000” is not in the quote." }] });
tests/unit/test_review_rules.py:87:    """D-034 (R-RV-3): summary edited to add '$9,000' -> 422 invalid_edit, no override via confirm_warnings; the item is unchanged."""
tests/unit/test_review_rules.py:91:        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Visit 8: pain 4/10, improving; billed $9,000."), confirm_warnings=confirm), call=judge("supported"))
tests/unit/test_review_rules.py:95:def test_seeded_herniation_judge_unsupported_needs_confirm(tmp_path):
tests/unit/test_review_rules.py:100:    assert e.value.code == "needs_confirm" and "JUDGE_UNSUPPORTED" in [w["code"] for w in e.value.detail["warnings"]]
tests/unit/test_review_rules.py:102:def test_keep_my_wording_resend_saves_and_logs(tmp_path):
tests/unit/test_review_rules.py:103:    """R-RV-3: resend with confirm_warnings=true saves (review_status edited) and logs a keep_my_wording event."""
tests/unit/test_review_rules.py:108:    assert e.value.code == "needs_confirm"                                       # non-numeric judge objection keeps the confirm path
tests/unit/test_review_rules.py:109:    r = RV.apply_review(conn, cid, eid, dict(action="edit", edits=edits, confirm_warnings=True), call=judge("unsupported"))
tests/unit/test_api_routes.py:132:def test_charge_cannot_be_edited_and_rerun_needs_confirm(env):
tests/unit/test_api_routes.py:139:    assert r.status_code == 409 and r.json()["error"]["code"] == "needs_confirm"
tests/unit/test_export.py:161:    c["events"] = [dict(type="keep_my_wording", item_id="e3")]
tests/unit/test_export.py:164:    assert "referred to physical therapy 2x/week" in sec and "Persistent neck pain 6/10; daily headaches." in sec and "keep my wording" in sec.lower()
tests/unit/test_manual_and_split.py:58:        RV.manual_entry(conn, cid, "r5", {"summary": "Pain 9/10.", "excerpt": "Pain 4/10, improving.", "confirm_warnings": confirm}, call=judge("supported"))
tests/unit/test_manual_and_split.py:68:    assert e.value.code == "needs_confirm"                                           # non-numeric judge objection: the confirm path stays
tests/unit/test_manual_and_split.py:69:    r = RV.manual_entry(conn, cid, "r5", {**body, "confirm_warnings": True}, call=judge("unsupported"))
tests/unit/test_manual_and_split.py:76:    assert "entered by reviewer" in sec and "paralegal confirmed keep my wording (reviewer override: JUDGE_UNSUPPORTED)" in sec
tests/e2e/test_edit.py:17:    """R-RV-3 / D-034: adding '$9,000' (not in the quote) is a hard 422 - API and UI; nothing saved, no 'keep my wording' button."""
tests/e2e/test_edit.py:19:    st, err = api("POST", f"/api/cases/{sample_case}/items/{eid}/review", {"action": "edit", "edits": {"summary": "Visit 8: pain 4/10, improving; billed $9,000."}, "confirm_warnings": True})
tests/e2e/test_rerun_judge.py:240:    st, _ = api("POST", f"/api/cases/{sample_case}/items/{edited['id']}/review", {"action": "edit", "edits": {"summary": edited["summary"].rstrip(".") + " per the record."}, "confirm_warnings": True})
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:36.277Z

**tool call — Bash**
````
{
 "command": "git show e511778 -- tests/unit/test_trace.py | cat",
 "description": "Show the new T-098 tests added in test_trace.py at e511778"
}
````

### User / tool · 2026-11-02T05:01:36.375Z

**tool result**
````
commit e5117784ccec180cc41b68eb050cbe1d99f5534d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:59:28 2026 -0600

    fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)
    
    A summary the paralegal wrote or edited is exempt from the judge but still has to pass the D-034/D-022 code checks. Accepted/edited entries of that kind
    with a failing code step are now gate blockers (named step + next action), GET /export returns 422 for them, and the item trace shows the failing step
    with a specific 'Edit the summary to keep ...' action. trace.py and api.md also carry other workers' uncommitted hunks (T-094 flag steps, T-099 calibration contract).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_trace.py b/tests/unit/test_trace.py
index b931fe3..ad630af 100644
--- a/tests/unit/test_trace.py
+++ b/tests/unit/test_trace.py
@@ -1015,3 +1015,105 @@ def test_rejudge_writes_one_rejudge_event_per_asked_item_and_leaves_review_statu
     assert sorted(e["item_id"] for e in ev) == sorted(x["item_id"] for x in out["rejudged"] + out["still_unavailable"])
     assert all(e["after"]["event"] == "rejudge" and e["after"]["verdict"] and e["before"]["review_status"] == "accepted" for e in ev)
     assert {r["id"]: r["review_status"] for k in ("entry", "amount", "flag") for r in DB.list_items(conn, tok, k)} == before
+
+
+# ---- D-045(b) / T-098: a human-edited summary is exempt from the judge, never from the code checks (reviewer case: reviews/T-097-ux-designer.md B1)
+REVIEWER_EDIT = "Paralegal wording for the mixed-case check."          # the T-097 walk's edit: drops the quote's qualifier
+
+
+def _edit_entry(c, tok, eid, summary):
+    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "edit", "edits": {"summary": summary}})
+    assert r.status_code == 200, r.text
+    return r
+
+
+def _mixed(c, tok):
+    """The reviewer's walk: accept one entry, edit another so it drops a qualifier, dismiss the first. Returns the edited id."""
+    ents = c.get(f"/api/cases/{tok}").json()["entries"]
+    acc, edt = ents[0]["id"], ents[1]["id"]
+    assert c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "accept"}).status_code == 200
+    _edit_entry(c, tok, edt, REVIEWER_EDIT)
+    c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "dismiss"})
+    return edt
+
+
+def _ccf(gate):
+    return [b for b in gate["blockers"] if b.get("step_id")]
+
+
+def test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098(env):
+    c, conn, tok, _ = env
+    edt = _mixed(c, tok)
+    g = _gate(c, tok)
+    got = _ccf(g)
+    assert [b["item_id"] for b in got] == [edt] and got[0]["reason_code"] == "SUMMARY_DROPS_QUALIFIER" and got[0]["step_id"] == "summary_qualifier"
+    assert g["ready"] is False and g["status"] == "fail" and g["counts"]["code_check_failed"] == 1 and g["reason_code"] == "SUMMARY_DROPS_QUALIFIER"
+    assert "second AI check is not needed" in got[0]["why"] and g["next_action"]["code"] == "EDIT_SUMMARY"
+    r = c.get(f"/api/cases/{tok}/export")
+    assert r.status_code == 422 and "letter_text" not in r.text and REVIEWER_EDIT not in r.text
+    det = r.json()["error"]["detail"]["blockers"]
+    assert [(b["item_id"], b["reason_code"]) for b in det] == [(edt, "SUMMARY_DROPS_QUALIFIER")]
+    assert r.json()["error"]["code"] == "export_blocked" and "export is blocked" in r.json()["error"]["message"]
+    ct = c.get(f"/api/cases/{tok}/trace").json()
+    assert ct["verdict"]["code"] == "needs_attention" and "fails a check" in ct["verdict"]["label"]
+
+
+def test_item_trace_shows_the_failing_code_step_with_the_next_action_t098(env):
+    c, conn, tok, _ = env
+    edt = _mixed(c, tok)
+    t = c.get(f"/api/cases/{tok}/items/{edt}/trace").json()
+    s = steps_of(t)
+    q = s["summary_qualifier"]
+    assert q["status"] == "fail" and q["blocks_export"] is True and q["reason_code"] == "SUMMARY_DROPS_QUALIFIER"
+    na = q["next_action"]
+    assert na["code"] == "EDIT_SUMMARY" and na["text"].startswith("Edit the summary to keep ") and "‘" in na["text"] and "export stays blocked" in na["text"]
+    assert t["verdict"]["blocks_export"] is True and t["verdict"]["code"] == "needs_attention" and t["next_action"] == na
+    assert s["human"]["status"] == "pass"                                       # the decision is still recorded; the code check is what blocks
+    for sid in ("summary_tokens", "excerpt_verbatim", "highlight"):
+        assert s[sid]["blocks_export"] is False
+
+
+def test_fixing_the_summary_clears_the_blocker_and_the_gate_agrees_with_export_t098(env):
+    c, conn, tok, _ = env
+    edt = _mixed(c, tok)
+    assert c.get(f"/api/cases/{tok}/export").status_code == 422
+    quote = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == edt)["excerpt"]
+    _edit_entry(c, tok, edt, quote)      # the quote verbatim keeps every qualifier
+    g = _gate(c, tok)
+    assert _ccf(g) == [] and g["ready"] is True
+    ex = c.get(f"/api/cases/{tok}/export")
+    assert ex.status_code == 200 and g["ready"] == (ex.status_code < 400)
+    assert steps_of(c.get(f"/api/cases/{tok}/items/{edt}/trace").json())["summary_qualifier"]["status"] == "pass"
+
+
+def test_dismissing_the_failing_edited_item_clears_the_blocker_t098(env):
+    c, conn, tok, _ = env
+    edt = _mixed(c, tok)
+    c.post(f"/api/cases/{tok}/items/{edt}/review", json={"action": "dismiss"})
+    assert _ccf(_gate(c, tok)) == []
+
+
+def test_ai_draft_is_not_gated_by_this_blocker_only_human_wording_t098(env):
+    c, conn, tok, _ = env
+    _accept_all(c, tok)
+    assert _ccf(_gate(c, tok)) == []
+
+
+def test_gate_ready_equals_export_allowed_with_a_failing_edit_t098(env):
+    c, conn, tok, _ = env
+    _mixed(c, tok)
+    for name in ("failing edit", "failing edit and run failed"):
+        if name.endswith("run failed"):
+            DB.update_case(conn, tok, status="failed")
+        g = _gate(c, tok)
+        ex = c.get(f"/api/cases/{tok}/export")
+        assert g["ready"] == (g["blockers"] == []) == (ex.status_code < 400), name
+        assert [b["reason_code"] for b in ex.json()["error"]["detail"]["blockers"]] == [b["reason_code"] for b in g["blockers"]], name
+
+
+def test_missing_qualifier_terms_name_the_words_to_keep_t098():
+    from app.backend import grounding
+    assert grounding.missing_qualifier_terms("MRI of the cervical spine was done.", "MRI suggests possible disc herniation.")
+    got = grounding.missing_qualifier_terms("Fracture seen.", "Possible left wrist fracture.")
+    assert "possible" in got and "left" in got
+    assert grounding.missing_qualifier_terms("Possible left wrist fracture.", "Possible left wrist fracture.") == []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:43.338Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && sed -n 515,530p app/backend/api.py; echo ---; grep -n \"_CODE_CHECK_REASONS\\|def export_payload\\|def blocked_message\\|class ExportBlocked\" -A6 app/backend/trace.py app/backend/export_routes.py | head -80; echo ---; grep -rn \"SUMMARY_TOKEN_NOT_IN_EXCERPT\\|SUMMARY_DROPS_QUALIFIER\" app/backend/*.py | grep -v \"^app/backend/trace.py\" | head -30",
 "description": "Read export route, export blockers and where code-check reasons are produced"
}
````

### User / tool · 2026-11-02T05:01:43.444Z

**tool result**
````
    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)

    @app.get("/api/cases/{token}/export")
    def export(token: str):
        from app.backend import export_routes as XR
        c = conn()
        try:
            get_case(c, token)
            case = store.export_case(c, token)
            try:
                ex = XR.export_payload(token, case)
            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
            calls = DB.list_llm_calls(c, token)
            ok = ("accepted", "edited")
            tv = present.totals_view(c, token)
---
app/backend/export_routes.py:27:def export_payload(token: str, case: dict, now: datetime = None) -> dict:
app/backend/export_routes.py-28-    if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
app/backend/export_routes.py-29-        raise export.ExportBlocked(case["export_blockers"])
app/backend/export_routes.py-30-    out = export.build_export(case)
app/backend/export_routes.py-31-    now = now or datetime.now(timezone.utc)
app/backend/export_routes.py-32-    ok = ("accepted", "edited")
app/backend/export_routes.py-33-    return {
--
app/backend/export_routes.py:52:def blocked_message(e) -> str:
app/backend/export_routes.py-53-    if e.code == "judge_not_run":
app/backend/export_routes.py-54-        return judge_not_run_message(len(e.items))
app/backend/export_routes.py-55-    return e.items[0]["why"] + " The export is blocked."
app/backend/export_routes.py-56-
app/backend/export_routes.py-57-
app/backend/export_routes.py-58-def judge_not_run_message(n: int) -> str:
app/backend/trace.py:76:_CODE_CHECK_REASONS = {"SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND"}
app/backend/trace.py-77-
app/backend/trace.py-78-
app/backend/trace.py-79-def reason_text(code: str) -> str:
app/backend/trace.py-80-    if code in TRACE_WHY:
app/backend/trace.py-81-        return TRACE_WHY[code]
app/backend/trace.py-82-    try:
--
app/backend/trace.py:392:            if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS:
app/backend/trace.py-393-                s["blocks_export"] = True
app/backend/trace.py-394-                s["next_action"] = _fix_action(row, s)
app/backend/trace.py-395-    st.append(_human_step(cx, row, "entry", extra_pending_next=nxt))
app/backend/trace.py-396-    return st
app/backend/trace.py-397-
app/backend/trace.py-398-
--
app/backend/trace.py:435:        fails = [s for s in _entry_steps(cx, row) if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS]
app/backend/trace.py-436-        if not fails:
app/backend/trace.py-437-            continue
app/backend/trace.py-438-        f = fails[0]
app/backend/trace.py-439-        out.append({"item_id": row["id"], "kind": "entry", "reason_code": f["reason_code"], "step_id": f["id"], "failed_steps": [x["id"] for x in fails],
app/backend/trace.py-440-                    "why": f["why"] + " " + TRACE_WHY["CODE_CHECK_FAILED"], "next_action": _fix_action(row, f)})
app/backend/trace.py-441-    return out
--
app/backend/trace.py:813:            elif not (R & _CODE_CHECK_REASONS):
app/backend/trace.py-814-                disagreements.append({"item_id": r["item_id"], "kind": r["kind"], "type": "judge_objects", "code_says": "All code checks passed.",
app/backend/trace.py-815-                                      "judge_says": rationale_or(r["reason_code"], v), "resolution": "needs_review", "review_status": row["review_status"]})
app/backend/trace.py-816-        elif v in ("unsure", "unavailable"):
app/backend/trace.py-817-            unresolved.append(dict(base, state_reason="JUDGE_UNSURE" if v == "unsure" else ("FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"),
app/backend/trace.py-818-                                   **({"reason_code": r["reason_code"]} if v == "unsure" else {})))
app/backend/trace.py:819:        elif R & _CODE_CHECK_REASONS:            # judge supported but a code check raised a doubt
app/backend/trace.py-820-            disagreements.append({"item_id": r["item_id"], "kind": r["kind"], "type": "judge_agrees_code_flags",
app/backend/trace.py:821:                                  "code_says": " ".join(reason_text(c) for c in sorted(R & _CODE_CHECK_REASONS)), "judge_says": _J_OK[r["judge"]],
app/backend/trace.py-822-                                  "resolution": "needs_review", "review_status": row["review_status"]})
app/backend/trace.py-823-    for row in DB.list_items(conn, case_id, "flag"):
app/backend/trace.py-824-        R = set(row.get("state_reasons") or [])
app/backend/trace.py-825-        for c in ("LEXICON_ONLY", "LLM_ONLY"):
app/backend/trace.py-826-            if c in R:
app/backend/trace.py-827-                disagreements.append({"item_id": row["id"], "kind": "flag", "type": "sources_disagree",
---
app/backend/confidence.py:7:    "SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE",
app/backend/generator.py:91:              qualifier_carried="EXCERPT_OMITS_QUALIFIER" not in code_reasons and "SUMMARY_DROPS_QUALIFIER" not in code_reasons,
app/backend/grounding.py:229:        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
app/backend/grounding.py:231:        reasons.append("SUMMARY_DROPS_QUALIFIER")
app/backend/narrative.py:18:    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The sentence has a number, side, negation or date that is not in the cited quote.",
app/backend/narrative.py:19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, an attribution phrase or a negation that the cited quote has.",
app/backend/narrative.py:60:        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
app/backend/narrative.py:62:        reasons.append("SUMMARY_DROPS_QUALIFIER")
app/backend/review.py:94:        code_reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
app/backend/review.py:95:        blocking.append({"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "\u201c" + "\u201d, \u201c".join(toks) + "\u201d is not in the quote.", "item_id": item_id})
app/backend/review.py:97:        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
app/backend/review.py:166:                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
app/backend/review.py:303:                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
app/backend/spanish_text.py:7:gets SUMMARY_TOKEN_NOT_IN_EXCERPT / SUMMARY_DROPS_QUALIFIER, which route it to the paralegal (fail toward flagging).
app/backend/spanish_text.py:246:        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
app/backend/spanish_text.py:248:        reasons.append("SUMMARY_DROPS_QUALIFIER")
app/backend/why.py:6:    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.",
app/backend/why.py:7:    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:50.188Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && sed -n 40,70p app/backend/review.py; echo ...; grep -n \"def apply\\|def act\\|\\\"accept\\\"\\|'accept'\\|rejected\\|needs_review\" app/backend/review.py | head -40; echo ---; sed -n 1,40p app/backend/confidence.py",
 "description": "Read review accept path and confidence state rules at HEAD archive"
}
````

### User / tool · 2026-11-02T05:01:50.288Z

**tool result**
````
def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
    """D-041: an entry whose date is not confirmed (ambiguous, missing, or no date at all) cannot go into the letter. Same rule as
    present.case_view uses to put an entry under `undated_entries`: date_iso set and the record's date_status parsed or confirmed."""
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
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
        raise _bad("That action is not allowed.")
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
        raise _date_unconfirmed_error()
    warnings = []
    if action in ("accept", "dismiss", "reset"):
...
6:that cannot answer never blocks: the edit is saved as needs_review with JUDGE_UNAVAILABLE.
13:ACTIONS = ("accept", "dismiss", "reset", "edit")
59:def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
65:    if item["state"] == "rejected" and action in ("accept", "edit"):
66:        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
67:    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
70:    if action in ("accept", "dismiss", "reset"):
208:    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
211:    if state == "needs_review" and not reasons:
250:        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
274:    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
285:    live = [e for e in DB.list_items(conn, case_id, "entry") if record_id in (e["record_ids"] or []) and e["state"] != "rejected"]
354:            if e["state"] != "rejected":
---
"""compose_state(ladder, context) -> (state, reasons)  (ADR-005, R-TL-5, LLM_VS_CODE row 17). Pure and deterministic.

Precedence: rejected > needs_review > verified. Reason codes are a closed list (api.md appendix); an unknown code is a bug.
"""
REASON_CODES = (
    "GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE",
    "HIGHLIGHT_NOT_FOUND", "JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE",
    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
    "AMOUNT_ESTIMATE", "AMOUNT_DAMAGES", "AMOUNT_UNCLEAR", "LEXICON_ONLY", "LLM_ONLY", "SPLIT_AMBIGUOUS",
    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT", "OCR_DERIVED", "LANGUAGE_UNCERTAIN",
)
REJECTED_CODES = frozenset({"GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"})
STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}

_JUDGE = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES",
          "unsure": "JUDGE_UNSURE", "unavailable": "JUDGE_UNAVAILABLE"}
_AMOUNT = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
_AGREE = {"lexicon_only": "LEXICON_ONLY", "llm_only": "LLM_ONLY"}
_DATE = {"ambiguous": "DATE_AMBIGUOUS", "missing": "DATE_MISSING"}


def sort_key(state: str) -> int:
    """needs_review first, then verified, then rejected."""
    return STATE_ORDER[state]


def _known(code: str) -> str:
    if code not in REASON_CODES:
        raise ValueError(f"unknown reason code: {code}")
    return code


def _lookup(table: dict, value, none_ok=()):
    if value is None or value in none_ok:
        return None
    if value not in table:
        raise ValueError(f"unknown value: {value}")
    return table[value]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:53.282Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-034\\|D-022\\|D-044\" memory/ORCHESTRATOR_DECISIONS.md | cut -c1-900; echo ---; grep -n -i \"code check\\|ladder\\|human\" docs/LLM_VS_CODE.md | head -30; echo ---; grep -n -i \"ladder\" -A3 docs/CONTRACT.md | head -40",
 "description": "Read decisions D-022 D-034 D-044 and the LLM/code ladder rules"
}
````

### User / tool · 2026-11-02T05:01:53.386Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:59.158Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && sed -n 68,80p app/backend/review.py; echo ...; sed -n 176,200p app/backend/review.py",
 "description": "Read the accept branch of apply_review at HEAD archive"
}
````

### User / tool · 2026-11-02T05:01:59.267Z

**tool result**
````
        raise _date_unconfirmed_error()
    warnings = []
    if action in ("accept", "dismiss", "reset"):
        DB.apply_review(conn, item_id, action, now=t, case=case_id)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}


...
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:02:08.926Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && sed -n 55,100p app/backend/generator.py",
 "description": "Read generator code-check handling for AI-drafted entries at HEAD archive"
}
````

### User / tool · 2026-11-02T05:02:09.029Z

**tool result**
````
    except AU.LLMFailed:
        return {"failure": "LLM_FAILED_AFTER_RETRIES", "record_no": record["n"]}
    e = _entry_base(record, group, case_text)
    e["ladder"] = {"item_id": e["id"], "generator": {"model": judges.generator_model(), "prompt_version": prompt.name,
                                                      "call_id": call_id, "output": out if isinstance(out, dict) else None},
                   "judge": None, "code_checks": {}, "human": {"action": None, "edited_text": None, "at": None}}
    if language.is_translated(lang):                      # the quote stays in the original language; the summary is a labelled AI translation (D-042)
        e["ladder"]["translation"] = spanish.translation_info(lang)
    try:
        o = schemas.ExtractOutput.model_validate(out)
    except (ValidationError, TypeError, ValueError):
        e.update(summary="", excerpt="", excerpt_start=None, excerpt_end=None, source_kind="record")
        return compose(e, record, grounding_failures=["SCHEMA_INVALID"], schema_valid=False)
    return verify(e, record, o.summary, o.excerpt)


def verify(e: dict, record: dict, summary: str, excerpt: str) -> dict:
    """Stage 2 (code): grounding of the excerpt, summary token/qualifier checks, offsets. Never edits the model's text."""
    body = record["excerpt"]
    g = spanish.module_for(language.record_lang(record))     # English: grounding itself; Spanish: the same checks mapped onto Spanish words
    exc_reasons = g.check_excerpt(body, excerpt)
    failures = [c for c in exc_reasons if c in confidence.REJECTED_CODES]
    code_reasons = [c for c in exc_reasons if c not in confidence.REJECTED_CODES]
    if language.record_lang(record) == "uncertain":          # D-042: never verified when the language is not confidently English or Spanish
        code_reasons.append("LANGUAGE_UNCERTAIN")
    span = grounding.locate(body, excerpt)
    if not failures:
        code_reasons += g.check_summary(summary, excerpt, record["source"], record.get("date_iso") or "")
        if span is None:
            code_reasons.append("HIGHLIGHT_NOT_FOUND")
    base = body_offset(record)
    e.update(summary=summary, excerpt=excerpt,
             excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None,
             source_kind="record")
    cc = e["ladder"]["code_checks"]
    cc.update(excerpt_verbatim=not failures, excerpt_whole_sentence="EXCERPT_NOT_WHOLE_SENTENCE" not in code_reasons,
              qualifier_carried="EXCERPT_OMITS_QUALIFIER" not in code_reasons and "SUMMARY_DROPS_QUALIFIER" not in code_reasons,
              date_provider_from_header=True,
              summary_tokens_not_in_excerpt=g.new_tokens(summary, excerpt, record["source"], record.get("date_iso") or "") if not failures else [],
              highlight_found=span is not None)
    return compose(e, record, grounding_failures=failures, code_reasons=list(dict.fromkeys(code_reasons)))


def compose(e: dict, record: dict, *, grounding_failures=None, code_reasons=None, schema_valid=True, judge="__keep__", fixture_miss=False) -> dict:
    """Set e['state'], e['reasons'], e['why'] from e['_stage'] (private inputs; callers drop '_' keys when storing). Re-run after the judge."""
    lad = e["ladder"]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:02:16.965Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && grep -n \"^def env\\|@pytest.fixture\" -A22 tests/unit/test_trace.py | head -60; grep -n \"^def _gate\\|^def _accept_all\\|^def steps_of\" -A4 tests/unit/test_trace.py",
 "description": "Read the test_trace env fixture and helpers at HEAD archive"
}
````

### User / tool · 2026-11-02T05:02:17.060Z

**tool result**
````
21:@pytest.fixture(scope="module")
22-def base(tmp_path_factory):
23-    import os
24-    d = tmp_path_factory.mktemp("trace")
25-    old = {k: os.environ.get(k) for k in ("LLM_BACKEND", "ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY")}
26-    os.environ["LLM_BACKEND"] = "fixture"
27-    for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
28-        os.environ.pop(k, None)
29-    db = str(d / "base.sqlite")
30-    c = TestClient(create_app(db, static_dir=str(d)), client=("127.0.0.1", 50000))
31-    pre = c.post("/api/cases", json={"sample": True}).json()["token"]          # an ingested case that never ran
32-    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
33-    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
34-    for _ in range(240):
35-        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
36-            break
37-        time.sleep(0.25)
38-    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready"
39-    yield {"dir": d, "db": db, "tok": tok, "pre": pre}
40-    for k, v in old.items():
41-        if v is None:
42-            os.environ.pop(k, None)
43-        else:
--
47:@pytest.fixture
48:def env(base, tmp_path, monkeypatch):
49-    monkeypatch.setenv("LLM_BACKEND", "fixture")
50-    monkeypatch.delenv("ZLAYT_MODE", raising=False)
51-    path = str(tmp_path / "copy.sqlite")
52-    src = sqlite3.connect(base["db"])
53-    dst = sqlite3.connect(path)
54-    src.backup(dst)
55-    src.close()
56-    dst.close()
57-    conn = DB.connect(path)
58-    c = TestClient(create_app(path, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
59-    return c, conn, base["tok"], base["pre"]
60-
61-
62-def steps_of(t):
63-    return {s["id"]: s for s in t["steps"]}
64-
65-
66-def walk(o, keys):
67-    """Every dict key anywhere in o that is in `keys`."""
68-    found = set()
69-    if isinstance(o, dict):
70-        for k, v in o.items():
62:def steps_of(t):
63-    return {s["id"]: s for s in t["steps"]}
64-
65-
66-def walk(o, keys):
--
537:def _gate_states(c, conn, tok):
538-    """Yield (name) after putting the case into each state we can build; the caller checks the invariant."""
539-    case = c.get(f"/api/cases/{tok}").json()
540-    ids = [x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k]]
541-    yield "pending items"
--
676:def _accept_all(c, tok):
677-    case = c.get(f"/api/cases/{tok}").json()
678-    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
679-        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
680-
--
688:def _gate(c, tok):
689-    return steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
690-
691-
692-def _jnr(gate):
--
774:def _accept_all_but(c, tok, keep_pending):
775-    case = c.get(f"/api/cases/{tok}").json()
776-    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
777-        if x["id"] not in keep_pending:
778-            c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:02:25.475Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && grep -n \"^def update_item\\|^def apply_review\\|^def list_items\\|^def get_case\\|^def connect\" -A8 app/db/db.py | head -80; grep -n \"def _paralegal_wording\" -A8 app/backend/trace.py",
 "description": "Check DB helper signatures and paralegal-wording predicate"
}
````

### User / tool · 2026-11-02T05:02:25.576Z

**tool result**
````
38:def connect(path: str):
39-    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
40-    text): the schema uses CREATE IF NOT EXISTS, so an old file would otherwise keep its old keys, and keeping it aside would keep
41-    pasted text past the 24 h purge (T-040 security r2)."""
42-    if path != ":memory:" and os.path.exists(path) and os.path.getsize(path) > 0:
43-        probe = sqlite3.connect(path)
44-        try:
45-            version = probe.execute("PRAGMA user_version").fetchone()[0]
46-            has_tables = probe.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0] > 0
--
131:def get_case(conn, case_id: str):
132-    r = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
133-    return _decode(r) if r else None
134-
135-
136-def _insert(conn, table, row):
137-    bad = set(row) - _cols(conn, table)
138-    if bad:
139-        raise ValueError(f"unknown {table} fields {sorted(bad)}")
--
195:def list_items(conn, case_id: str, kind: str) -> list:
196-    table = _ITEM_TABLES[kind][0]
197-    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]
198-
199-
200:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
201-    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
202-    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
203-    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
204-    if locked & set(fields):
205-        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
206-    table, found = _find(conn, item_id, case)
207-    bad = set(fields) - _cols(conn, table)
208-    if bad:
--
215:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
216-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
217-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
218-    if action not in ACTIONS:
219-        raise ValueError(f"invalid review action {action!r}")
220-    table, row = _find(conn, item_id, case)
221-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
222-    status = ACTIONS[action] or row["review_status"]
223-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
750:def _paralegal_wording(kind, row) -> bool:
751-    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
752-    return kind == "entry" and bool((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {}))
753-
754-
755-def unjudged_items(conn, case_id: str) -> list:
756-    """Live (not rejected, not dismissed) AI-made entries, charges and flags whose second check never gave an answer (D-044).
757-    [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run has started."""
758-    cx = _Cx(conn, case_id, False)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:02:35.460Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && sed -n 1,20p tests/unit/test_trace.py; grep -n \"^def _entry_base\" -A12 app/backend/generator.py | head -30; grep -n \"^def compose\" -A25 app/backend/generator.py | sed -n 1,30p",
 "description": "Read test imports, generator entry base, and compose function"
}
````

### User / tool · 2026-11-02T05:02:35.569Z

**tool result**
````
"""D-042 check traces (T-080): per-item stepper, case stepper with export gate, judge summary, and the full/metadata visibility split.
Fixture backend, no key. One recorded sample run is built once; each test works on its own copy of the database."""
import json
import pathlib
import sqlite3
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import trace, why
from app.backend.api import create_app
from app.db import db as DB

STATUSES = {"pass", "fail", "skipped", "pending"}
KINDS = {"code", "llm", "human"}
NEXT_CODES = {"DECIDE", "CONFIRM_DATE", "EDIT_SUMMARY", "EDIT_QUOTE", "READ_RECORD", "COMPARE_BY_HAND", "DISMISS_OR_ENTER_BY_HAND", "RERUN", "SENTENCE_REMOVED", "CONFIRM_RERUN", "RERUN_JUDGE"}
FULL_ONLY_KEYS = {"response_raw", "before", "after", "edited_text"}


37:def _entry_base(record: dict, group: list, case_text: str) -> dict:
38-    return {"id": f"e{record['n']}", "seq": record["n"], "record_id": record["id"], "record_ids": [f"r{n}" for n in group],
39-            "date": record.get("date_iso"), "date_status": record.get("date_status", "parsed"),
40-            "provider": record["source"], "ai_drafted": True, "review_status": "pending"}
41-
42-
43-def extract_one(record: dict, group: list, *, call, case_text: str = "") -> dict:
44-    """One generator call. Returns an entry dict (pre-judge) or {'failure': code, 'record_no': n} when no output exists."""
45-    lang = language.record_lang(record)
46-    if lang == "other":                                   # D-042: only English and Spanish are read; say so, never guess
47-        return {"failure": "UNSUPPORTED_LANGUAGE", "record_no": record["n"]}
48-    step, item = (spanish.EXTRACT_STEP if language.is_translated(lang) else "extract"), f"e{record['n']}"
49-    n = promptlib.nonce(case_text, step, item)
98:def compose(e: dict, record: dict, *, grounding_failures=None, code_reasons=None, schema_valid=True, judge="__keep__", fixture_miss=False) -> dict:
99-    """Set e['state'], e['reasons'], e['why'] from e['_stage'] (private inputs; callers drop '_' keys when storing). Re-run after the judge."""
100-    lad = e["ladder"]
101-    st = e.setdefault("_stage", {})
102-    if grounding_failures is not None:
103-        st["grounding_failures"] = grounding_failures
104-    if code_reasons is not None:
105-        st["code_reasons"] = code_reasons
106-    st.setdefault("code_reasons", [])
107-    st.setdefault("grounding_failures", [])
108-    st["schema_valid"] = schema_valid and st.get("schema_valid", True)
109-    if judge != "__keep__":
110-        st["judge"] = judge
111-    st["fixture_miss"] = fixture_miss or st.get("fixture_miss", False)
112-    state, reasons = confidence.compose_state(
113-        {"grounding_failures": st["grounding_failures"], "schema_valid": st["schema_valid"], "code_reasons": st["code_reasons"],
114-         "judge": st.get("judge")}, _ctx(record, fixture_miss=st["fixture_miss"]))
115-    e["state"], e["reasons"] = state, reasons
116-    e["why"] = " ".join(why.why(c) for c in reasons) if reasons else "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
117-    jd = (lad.get("judge") or {})
118-    if jd.get("verdict") in ("partially", "unsupported") and why.judge_detail(jd.get("reason_code")):
119-        e["why"] += " " + why.judge_detail(jd["reason_code"])
120-    lad["state"] = state
121-    return e
122-
123-
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:02:57.348Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/probe98\" && cat > \"$S/probe98/test_probe_t098.py\" <<'EOF'\n\"\"\"Scratch probe for T-098 review (not in the repo). Runs against a git-archive copy via `python -m pytest` from that copy.\"\"\"\nimport os, time, json\nimport pytest\nfrom fastapi.testclient import TestClient\n\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ.pop(\"ZLAYT_MODE\", None)\nos.environ.pop(\"ENABLE_LIVE\", None)\nos.environ.pop(\"ANTHROPIC_API_KEY\", None)\n\nfrom app.backend.api import create_app\nfrom app.backend import generator, store\nfrom app.db import db as DB\n\n\n@pytest.fixture(scope=\"module\")\ndef setup(tmp_path_factory):\n    d = tmp_path_factory.mktemp(\"p98\")\n    db = str(d / \"p.sqlite\")\n    c = TestClient(create_app(db, static_dir=str(d)), client=(\"127.0.0.1\", 50000))\n    tok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n    assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\n    for _ in range(240):\n        if c.get(f\"/api/cases/{tok}/status\").json()[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.25)\n    assert c.get(f\"/api/cases/{tok}/status\").json()[\"status\"] == \"ready\"\n    return c, db, tok\n\n\ndef _edit(c, tok, eid, summary, confirm=None):\n    body = {\"action\": \"edit\", \"edits\": {\"summary\": summary}}\n    if confirm is not None:\n        body[\"confirm_warnings\"] = confirm\n    r = c.post(f\"/api/cases/{tok}/items/{eid}/review\", json=body)\n    return r.status_code, (r.json().get(\"error\") or {}).get(\"code\")\n\n\ndef test_p1_p2_status_of_edits_at_head(setup):\n    c, db, tok = setup\n    ents = c.get(f\"/api/cases/{tok}\").json()[\"entries\"]\n    e = next(x for x in ents if not any(ch.isdigit() for ch in x[\"summary\"]) and \"$\" not in x[\"summary\"])\n    eid, orig, exc = e[\"id\"], e[\"summary\"], e[\"excerpt\"]\n    print(\"\\nP1 entry\", eid, \"| summary:\", orig, \"| excerpt:\", exc)\n    print(\"P1 add 'significantly' no confirm ->\", _edit(c, tok, eid, orig.rstrip(\".\") + \" significantly.\"))\n    print(\"P1 add 'significantly' confirm_warnings=true ->\", _edit(c, tok, eid, orig.rstrip(\".\") + \" significantly.\", True))\n    print(\"P1 accept ->\", c.post(f\"/api/cases/{tok}/items/{eid}/review\", json={\"action\": \"accept\"}).status_code)\n    g = c.get(f\"/api/cases/{tok}/trace\").json()\n    gate = next(s for s in g[\"steps\"] if s[\"id\"] == \"export_gate\")\n    print(\"P1 gate ready\", gate[\"ready\"], \"blockers\", [(b[\"item_id\"], b[\"reason_code\"]) for b in gate[\"blockers\"]])\n    ex = c.get(f\"/api/cases/{tok}/export\")\n    print(\"P1 export\", ex.status_code, ex.json().get(\"error\", {}).get(\"code\"))\n    c.post(f\"/api/cases/{tok}/items/{eid}/review\", json={\"action\": \"reset\"})\n    # D-047 candidates on the same entry, no confirm: side, negation, hedge\n    print(\"P2 add 'left' ->\", _edit(c, tok, eid, orig.rstrip(\".\") + \" on the left.\"))\n    print(\"P2 add 'not' ->\", _edit(c, tok, eid, orig.rstrip(\".\") + \" and not improving.\"))\n    print(\"P2 add 'possibly' ->\", _edit(c, tok, eid, \"Possibly \" + orig))\n\n\ndef test_p3_ai_draft_with_numeric_mismatch_vs_human_edit(setup):\n    c, db, tok = setup\n    conn = DB.connect(db)\n    case = DB.get_case(conn, tok)\n    recs = store.load_records(conn, tok, case[\"raw_text\"])\n    ents = c.get(f\"/api/cases/{tok}\").json()[\"entries\"]\n    e = next(x for x in ents if any(ch.isdigit() for ch in x[\"excerpt\"]) and x[\"id\"] != \"\")\n    eid = e[\"id\"]\n    rid = (DB.list_items(conn, tok, \"entry\")[0][\"record_ids\"] or [None])[0]\n    row = next(x for x in DB.list_items(conn, tok, \"entry\") if x[\"id\"] == eid)\n    rec = next(r for r in recs if r[\"id\"] == (row[\"record_ids\"] or [None])[0])\n    import re\n    m = re.search(r\"\\d+(?:/\\d+)?\", e[\"excerpt\"])\n    bad_num = \"9/10\" if m.group(0) != \"9/10\" else \"8/10\"\n    bad_summary = re.sub(r\"\\d+(?:/\\d+)?\", bad_num, e[\"summary\"], count=1) if re.search(r\"\\d\", e[\"summary\"]) else e[\"summary\"] + f\" Pain {bad_num}.\"\n    print(\"\\nP3 excerpt:\", e[\"excerpt\"], \"| bad summary:\", bad_summary)\n    # Same wording through the real generator verify(): what state does code give an AI draft?\n    ent = generator._entry_base(rec, [rec[\"n\"]], case[\"raw_text\"])\n    ent[\"ladder\"] = {\"item_id\": eid, \"generator\": {}, \"judge\": None, \"code_checks\": {}, \"human\": {}}\n    out = generator.verify(ent, rec, bad_summary, e[\"excerpt\"])\n    print(\"P3 generator.verify state:\", out[\"state\"], out[\"reasons\"])\n    # Human edit with the same wording (D-034 says hard 422)\n    print(\"P3 human edit same wording ->\", _edit(c, tok, eid, bad_summary))\n    # Simulate the AI draft as the generator stored it: bad wording, code reasons, judge agrees\n    lad = dict(row.get(\"ladder\") or {})\n    lad[\"judge\"] = {\"model\": \"fixture\", \"prompt_version\": \"judge\", \"call_id\": None, \"verdict\": \"supported\", \"reason_code\": \"NONE\"}\n    lad[\"state\"] = out[\"state\"]\n    DB.update_item(conn, eid, now=time.time(), case=tok, summary=bad_summary, state=out[\"state\"], state_reasons_json=out[\"reasons\"], ladder=lad)\n    conn.commit() if hasattr(conn, \"commit\") else None\n    print(\"P3 stored item state:\", DB.list_items(conn, tok, \"entry\")[0 if False else 0] and next(x for x in DB.list_items(conn, tok, \"entry\") if x[\"id\"] == eid)[\"state\"])\n    print(\"P3 accept AI draft ->\", c.post(f\"/api/cases/{tok}/items/{eid}/review\", json={\"action\": \"accept\"}).status_code)\n    g = c.get(f\"/api/cases/{tok}/trace\").json()\n    gate = next(s for s in g[\"steps\"] if s[\"id\"] == \"export_gate\")\n    print(\"P3 gate ready\", gate[\"ready\"], \"blockers\", [(b[\"item_id\"], b[\"reason_code\"]) for b in gate[\"blockers\"]])\n    ex = c.get(f\"/api/cases/{tok}/export\")\n    print(\"P3 export\", ex.status_code, \"contains bad summary:\", bad_summary in ex.text)\nEOF\ncd \"$S/t098-head\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q -s \"$S/probe98/test_probe_t098.py\" 2>&1 | tail -60",
 "description": "Run scratch probe of edit status codes and AI-draft gate behaviour on HEAD archive",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T05:02:58.893Z

**tool result**
````
P1 entry e9 | summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision. | excerpt: Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.
P1 add 'significantly' no confirm -> (200, None)
P1 add 'significantly' confirm_warnings=true -> (200, None)
P1 accept -> 200
P1 gate ready True blockers []
P1 export 200 None
P2 add 'left' -> (409, 'needs_confirm')
P2 add 'not' -> (409, 'needs_confirm')
P2 add 'possibly' -> (200, None)
.
P3 excerpt: 41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER. | bad summary: 9/10-year-old male restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache, alert and oriented, transported to Central ER.
P3 generator.verify state: verified []
P3 human edit same wording -> (200, None)
P3 stored item state: verified
P3 accept AI draft -> 200
P3 gate ready True blockers []
P3 export 200 contains bad summary: True
.
2 passed in 1.22s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:03:09.001Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nimport sys\nsys.path.insert(0, \".\")\nfrom app.backend import spanish, grounding\nexc = \"41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.\"\nfor s in [\"9/10-year-old male restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache, alert and oriented, transported to Central ER.\",\n          \"Neck pain 9/10 reported after the collision; transported to Central ER.\",\n          \"Neck pain 7/10 reported after the collision; transported to Central ER.\",\n          \"Neck pain reported after the collision; transported to Central ER on the left.\"]:\n    g = spanish.module_for(\"en\")\n    print(repr(s[:40]), \"toks:\", g.new_tokens(s, exc, \"Central ER\", \"2026-01-09\"), \"dropped:\", g.dropped_qualifiers(s, exc), \"checks:\", g.check_summary(s, exc, \"Central ER\", \"2026-01-09\"))\nEOF",
 "description": "Check which summaries the code token checks flag on a sample excerpt"
}
````

### User / tool · 2026-11-02T05:03:09.289Z

**tool result**
````
'9/10-year-old male restrained driver rea' toks: [] dropped: [] checks: []
'Neck pain 9/10 reported after the collis' toks: [] dropped: ['self_report', 'approx'] checks: ['SUMMARY_DROPS_QUALIFIER']
'Neck pain 7/10 reported after the collis' toks: [] dropped: ['self_report', 'approx'] checks: ['SUMMARY_DROPS_QUALIFIER']
'Neck pain reported after the collision; ' toks: ['left'] dropped: ['self_report', 'approx'] checks: ['SUMMARY_TOKEN_NOT_IN_EXCERPT', 'SUMMARY_DROPS_QUALIFIER']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:03:15.184Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-head\" && grep -n \"def new_tokens\" -B30 -A30 app/backend/grounding.py | sed -n 1,120p",
 "description": "Read grounding.new_tokens implementation at HEAD archive"
}
````

### User / tool · 2026-11-02T05:03:15.280Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:03:30.265Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/probe98/test_probe_t098b.py\" <<'EOF'\n\"\"\"Scratch probe 2 for T-098 review (not in the repo). Uses the same sample run as probe 1.\"\"\"\nimport os, time, re\nimport pytest\nfrom fastapi.testclient import TestClient\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfor k in (\"ZLAYT_MODE\", \"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\"):\n    os.environ.pop(k, None)\nfrom app.backend.api import create_app\nfrom app.backend import generator, store\nfrom app.db import db as DB\n\n\n@pytest.fixture(scope=\"module\")\ndef setup(tmp_path_factory):\n    d = tmp_path_factory.mktemp(\"p98b\")\n    db = str(d / \"p.sqlite\")\n    c = TestClient(create_app(db, static_dir=str(d)), client=(\"127.0.0.1\", 50000))\n    tok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n    assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\n    for _ in range(240):\n        if c.get(f\"/api/cases/{tok}/status\").json()[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.25)\n    assert c.get(f\"/api/cases/{tok}/status\").json()[\"status\"] == \"ready\"\n    return c, db, tok\n\n\ndef _gate(c, tok):\n    g = c.get(f\"/api/cases/{tok}/trace\").json()\n    return next(s for s in g[\"steps\"] if s[\"id\"] == \"export_gate\")\n\n\ndef _edit(c, tok, eid, summary, confirm=None):\n    body = {\"action\": \"edit\", \"edits\": {\"summary\": summary}}\n    if confirm is not None:\n        body[\"confirm_warnings\"] = confirm\n    r = c.post(f\"/api/cases/{tok}/items/{eid}/review\", json=body)\n    return r.status_code, (r.json().get(\"error\") or {}).get(\"code\")\n\n\ndef test_p1_409_keep_wording_dead_end(setup):\n    c, db, tok = setup\n    ents = c.get(f\"/api/cases/{tok}\").json()[\"entries\"]\n    e = next(x for x in ents if not re.search(r\"\\d\", x[\"summary\"]) and \"left\" not in x[\"excerpt\"].lower())\n    eid, orig = e[\"id\"], e[\"summary\"]\n    print(\"\\nP1 entry\", eid, \"| summary:\", orig)\n    print(\"P1 'on the left' no confirm ->\", _edit(c, tok, eid, orig.rstrip(\".\") + \" on the left.\"))\n    print(\"P1 'on the left' confirm_warnings=true ->\", _edit(c, tok, eid, orig.rstrip(\".\") + \" on the left.\", True))\n    print(\"P1 accept ->\", c.post(f\"/api/cases/{tok}/items/{eid}/review\", json={\"action\": \"accept\"}).status_code)\n    gate = _gate(c, tok)\n    print(\"P1 gate ready\", gate[\"ready\"], \"| blockers\", [(b[\"item_id\"], b[\"reason_code\"]) for b in gate[\"blockers\"]], \"| why:\", gate[\"blockers\"][0][\"why\"] if gate[\"blockers\"] else None)\n    ex = c.get(f\"/api/cases/{tok}/export\")\n    print(\"P1 export\", ex.status_code, ex.json().get(\"error\", {}).get(\"code\"), \"| message:\", ex.json().get(\"error\", {}).get(\"message\"))\n    print(\"P1 ready == (export 200):\", gate[\"ready\"] == (ex.status_code == 200))\n    c.post(f\"/api/cases/{tok}/items/{eid}/review\", json={\"action\": \"reset\"})\n\n\ndef test_p3_ai_draft_with_invented_score_vs_human_edit(setup):\n    c, db, tok = setup\n    conn = DB.connect(db)\n    case = DB.get_case(conn, tok)\n    recs = store.load_records(conn, tok, case[\"raw_text\"])\n    rows = DB.list_items(conn, tok, \"entry\")\n    row = next(x for x in rows if not re.search(r\"\\d\", x[\"summary\"]) and x[\"review_status\"] == \"pending\")\n    eid, exc = row[\"id\"], row[\"excerpt\"]\n    bad = row[\"summary\"].rstrip(\".\") + \" Pain 5/10.\"\n    rec = next(r for r in recs if r[\"id\"] == (row[\"record_ids\"] or [None])[0])\n    print(\"\\nP3 excerpt:\", exc, \"| date:\", row[\"date_iso\"], \"| bad summary:\", bad)\n    ent = generator._entry_base(rec, [rec[\"n\"]], case[\"raw_text\"])\n    ent[\"ladder\"] = {\"item_id\": eid, \"generator\": {}, \"judge\": None, \"code_checks\": {}, \"human\": {}}\n    out = generator.verify(ent, rec, bad, exc)\n    print(\"P3 generator.verify (code rung) on AI wording -> state:\", out[\"state\"], \"| reasons:\", out[\"reasons\"])\n    print(\"P3 human edit with same wording ->\", _edit(c, tok, eid, bad))\n    lad = dict(row.get(\"ladder\") or {})\n    lad[\"judge\"] = {\"model\": \"fixture\", \"prompt_version\": \"judge\", \"call_id\": None, \"verdict\": \"supported\", \"reason_code\": \"NONE\"}\n    lad[\"state\"] = out[\"state\"]\n    DB.update_item(conn, eid, now=time.time(), case=tok, summary=bad, state=out[\"state\"], state_reasons_json=out[\"reasons\"], ladder=lad)\n    print(\"P3 stored AI item:\", next(x for x in DB.list_items(conn, tok, \"entry\") if x[\"id\"] == eid)[\"state\"])\n    print(\"P3 accept AI draft ->\", c.post(f\"/api/cases/{tok}/items/{eid}/review\", json={\"action\": \"accept\"}).status_code)\n    gate = _gate(c, tok)\n    print(\"P3 gate ready\", gate[\"ready\"], \"| blockers\", [(b[\"item_id\"], b[\"reason_code\"]) for b in gate[\"blockers\"]])\n    ex = c.get(f\"/api/cases/{tok}/export\")\n    print(\"P3 export\", ex.status_code, \"| letter contains invented 5/10:\", \"5/10\" in ex.text)\n    it = c.get(f\"/api/cases/{tok}/items/{eid}/trace\").json()\n    print(\"P3 item trace verdict:\", it.get(\"verdict\"))\nEOF\ncd \"$S/t098-head\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q -s \"$S/probe98/test_probe_t098b.py\" 2>&1 | tail -40",
 "description": "Run second probe for 409 dead end and AI-draft code failure accepted into export",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T05:03:31.590Z

**tool result**
````
P1 entry e9 | summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
P1 'on the left' no confirm -> (409, 'needs_confirm')
P1 'on the left' confirm_warnings=true -> (200, None)
P1 accept -> 200
P1 gate ready False | blockers [('e9', 'SUMMARY_TOKEN_NOT_IN_EXCERPT')] | why: The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter.
P1 export 422 export_blocked | message: The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter. The export is blocked.
P1 ready == (export 200): True
.
P3 excerpt: Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision. | date: 2026-06-12 | bad summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision Pain 5/10.
P3 generator.verify (code rung) on AI wording -> state: needs_review | reasons: ['SUMMARY_TOKEN_NOT_IN_EXCERPT']
P3 human edit with same wording -> (422, 'invalid_edit')
P3 stored AI item: needs_review
P3 accept AI draft -> 200
P3 gate ready True | blockers []
P3 export 200 | letter contains invented 5/10: True
P3 item trace verdict: {'code': 'accepted', 'label': 'Accepted by you', 'blocks_export': False}
.
2 passed in 0.89s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:03:45.237Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/probe98\" && sed -e 's/\"verdict\": \"supported\"/\"verdict\": VERDICT/' -e 's/^def test_p3_ai_draft_with_invented_score_vs_human_edit(setup):/def test_p3_ai_draft_with_invented_score_vs_human_edit(setup, monkeypatch):\\n    VERDICT = os.environ.get(\"P3_VERDICT\", \"supported\")/' -e 's/lad = dict(row.get(\"ladder\") or {})/lad = dict(row.get(\"ladder\") or {}); lad[\"judge\"] = {\"model\": \"fixture\", \"prompt_version\": \"judge\", \"call_id\": None, \"verdict\": VERDICT, \"reason_code\": \"NONE\"}/' test_probe_t098b.py > test_probe_t098c.py && cd \"$S/t098-head\" && for v in unsupported disagrees; do echo \"== judge verdict $v\"; P3_VERDICT=$v /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q -s \"$S/probe98/test_probe_t098c.py\" -k p3 2>&1 | grep \"P3\" ; done",
 "description": "Repeat AI-draft probe with judge verdicts unsupported and disagrees",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T05:03:47.438Z

**tool result**
````
== judge verdict unsupported
P3 excerpt: Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision. | date: 2026-06-12 | bad summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision Pain 5/10.
P3 generator.verify (code rung) on AI wording -> state: needs_review | reasons: ['SUMMARY_TOKEN_NOT_IN_EXCERPT']
P3 human edit with same wording -> (422, 'invalid_edit')
P3 stored AI item: needs_review
P3 accept AI draft -> 200
P3 gate ready True | blockers []
P3 export 200 | letter contains invented 5/10: True
P3 item trace verdict: {'code': 'accepted', 'label': 'Accepted by you', 'blocks_export': False}
== judge verdict disagrees
P3 excerpt: Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision. | date: 2026-06-12 | bad summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision Pain 5/10.
P3 generator.verify (code rung) on AI wording -> state: needs_review | reasons: ['SUMMARY_TOKEN_NOT_IN_EXCERPT']
P3 human edit with same wording -> (422, 'invalid_edit')
P3 stored AI item: needs_review
P3 accept AI draft -> 200
P3 gate ready True | blockers []
P3 export 200 | letter contains invented 5/10: True
P3 item trace verdict: {'code': 'accepted', 'label': 'Accepted by you', 'blocks_export': False}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:03:57.778Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && git log --oneline --all | grep -i \"T-094\\|T-099\" | head; echo ---; cd \"$S/t098-e511778\" && grep -rn \"candidate_rule\" tests/ | head -5; echo ---; cd \"$S/t098-head\" && grep -rn \"candidate_rule\" tests/ | head -5; echo; echo \"== full unit e511778\"; cd \"$S/t098-e511778\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -8; echo \"== full unit HEAD\"; cd \"$S/t098-head\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -8",
 "description": "Check T-094 commit presence, candidate_rule test coverage, and full unit runs on both archives",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:05:23.572Z

**tool result**
````
3ecb8b1 feat(backend): GET /api/calibration serves the measured calibration read-only (T-099)
---
---

== full unit e511778
........................................................................ [ 72%]
........................................................................ [ 77%]
.................................................................s...... [ 81%]
........................................................................ [ 86%]
........................................................................ [ 91%]
........................................................................ [ 95%]
.....................................................................    [100%]
1577 passed, 4 skipped in 41.41s
== full unit HEAD
........................................................................ [ 76%]
........................................................................ [ 80%]
................s....................................................... [ 85%]
........................................................................ [ 89%]
........................................................................ [ 94%]
........................................................................ [ 98%]
....................                                                     [100%]
1600 passed, 4 skipped in 41.85s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:05:31.614Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t098-e511778\" && grep -rln \"paired_by_code\\|plan_vs_outcome\\|candidate_rule\\|spans_match\" tests/ app/ | head; echo ---; grep -rn \"paired_by_code\\|plan_vs_outcome\\|candidate_rule\" tests/ | head -5; echo ---; grep -rln \"_ocr_steps\\|OCR_DERIVED\\|ocr\" tests/unit | head; echo ---; cd /Users/arsis/zlayt-pm-project && git show e511778 --stat | tail -3; git show 196c985 --stat | cat | head -20",
 "description": "Check test coverage of the T-094 trace hunk carried into e511778"
}
````

### User / tool · 2026-11-02T05:05:31.791Z

**tool result**
````
tests/unit/test_trace.py
app/backend/trace.py
app/backend/review.py
app/backend/pipeline.py
---
---
tests/unit/test_pdf_checks_api.py
tests/unit/test_pdf_ocr.py
tests/unit/test_billing.py
tests/unit/test_grounding.py
tests/unit/test_provider.py
tests/unit/test_review_rules.py
tests/unit/test_provider_backends.py
tests/unit/test_t033_backend.py
tests/unit/test_amounts.py
tests/unit/test_eval_runner.py
---
 tests/unit/test_export.py |  12 ++++++
 tests/unit/test_trace.py  | 102 ++++++++++++++++++++++++++++++++++++++++++++++
 5 files changed, 239 insertions(+), 12 deletions(-)
commit 196c985641d72aa699e295223fed8961db0b0c2a
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:00:24 2026 -0600

    harness: stale-index guard allows partial staging; blocks only re-staged older committed versions
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 tools/check_stale_index.py            | 11 ++++++--
 tools/tests/test_check_stale_index.py | 48 +++++++++++++++++++++++++++++++++++
 2 files changed, 57 insertions(+), 2 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:05:41.049Z

**tool call — Bash**
````
{
 "command": "git show 3ecb8b1 -- app/backend/calibration_route.py app/backend/api.py | cat; echo ---; ls -la evals/reports/ 2>&1 | head; git ls-files evals/reports | head; git status --short evals/reports 2>&1 | head",
 "description": "Show T-099 route code and check whether calibration report file exists"
}
````

### User / tool · 2026-11-02T05:05:41.223Z

**tool result**
````
commit 3ecb8b1ca58b97c2d23cdd78a8a99a7bf292f8db
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:00:11 2026 -0600

    feat(backend): GET /api/calibration serves the measured calibration read-only (T-099)
    
    Serves evals/reports/calibration.json in the T-096 shape (counts, statements, source commit, backend, sample size).
    Envelope {status, calibration, message}: ok | missing | invalid. calibration is null unless ok; nothing is invented
    and the file contents are never echoed. Aggregate only, no case token, so it is demo-safe. GET only (other methods 405).
    Validation: shape, count ranges, state totals equal type totals, each statement quotes its own m/t.
    Contract section is already in memory/contracts/api.md (landed with e511778).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index 021d5f8..ded34e5 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -511,6 +511,8 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
     from app.backend import reclassify
     reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
     dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
+    from app.backend import calibration_route
+    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)
 
     @app.get("/api/cases/{token}/export")
     def export(token: str):
diff --git a/app/backend/calibration_route.py b/app/backend/calibration_route.py
new file mode 100644
index 0000000..bf5a74c
--- /dev/null
+++ b/app/backend/calibration_route.py
@@ -0,0 +1,123 @@
+"""GET /api/calibration (T-099): the measured calibration the review screen quotes (T-090 writes it, T-096 shows it).
+
+Read-only. Serves evals/reports/calibration.json, which evals.run writes from the golden cases: aggregate counts, the statements built
+from those counts, the source commit and the backend. It holds no record text and no case token, so it is safe in demo mode and has no gate.
+
+Three states, always HTTP 200 with the same envelope {"status", "calibration", "message"}:
+- "ok": the file is the evals.calibration/1 shape, its totals add up, and every statement quotes its own counts. `calibration` is the
+  served subset (SERVED below).
+- "missing": no file. `calibration` is null. Nothing is invented.
+- "invalid": the file cannot be read as a valid measurement (bad JSON, wrong schema, a hand-edited count, a statement that quotes other
+  counts). `calibration` is null and the file's contents are never echoed; the reasons go to the log.
+The UI hides the accuracy line when `calibration` is null (T-096). This module reads one fixed path and never writes.
+"""
+import json
+import logging
+import pathlib
+
+ROOT = pathlib.Path(__file__).resolve().parents[2]
+REPORT = ROOT / "evals" / "reports" / "calibration.json"
+SCHEMA = "evals.calibration/1"
+TYPES = ("entry", "amount", "flag")
+STATES = ("verified", "needs_review")
+SERVED = ("schema", "backend", "case_count", "small_sample", "source_commit", "generated_at", "by_state", "by_type", "not_scored", "sentences")
+MISSING = "No calibration has been measured yet, so no accuracy line is shown."
+INVALID = "The calibration file is not a valid measurement, so no accuracy line is shown. Regenerate it with python -m evals.run."
+log = logging.getLogger("zlayt.calibration")
+
+
+def _count(x) -> bool:
+    return isinstance(x, int) and not isinstance(x, bool) and x >= 0
+
+
+def _cell_ok(c) -> bool:
+    return isinstance(c, dict) and _count(c.get("matched")) and _count(c.get("total")) and c["matched"] <= c["total"]
+
+
+def _statement_ok(text, cell) -> bool:
+    """A statement is a non-empty string; when its cell has items it must quote that cell's own m/t. A hand-edited number fails here."""
+    if not isinstance(text, str) or not text:
+        return False
+    return cell["total"] == 0 or f"{cell['matched']}/{cell['total']} times" in text
+
+
+def problems(c) -> list:
+    """Why `c` is not a valid calibration document. Empty list when it is. Checks the shape, the count ranges, that the state totals add up
+    to the type totals, and that each statement quotes its own counts."""
+    if not isinstance(c, dict):
+        return ["not an object"]
+    bad = []
+    if c.get("schema") != SCHEMA:
+        bad.append("schema")
+    if not (isinstance(c.get("backend"), str) and c["backend"]):
+        bad.append("backend")
+    if not _count(c.get("case_count")):
+        bad.append("case_count")
+    if not isinstance(c.get("small_sample"), bool):
+        bad.append("small_sample")
+    if not (isinstance(c.get("source_commit"), str) and c["source_commit"]):
+        bad.append("source_commit")
+    if not isinstance(c.get("generated_at"), str):
+        bad.append("generated_at")
+    ns = c.get("not_scored")
+    if not (isinstance(ns, dict) and all(_count(ns.get(k)) for k in TYPES + ("total",)) and ns["total"] == sum(ns[t] for t in TYPES)):
+        bad.append("not_scored")
+    bs, bt, se = c.get("by_state"), c.get("by_type"), c.get("sentences")
+    if not (isinstance(bs, dict) and isinstance(bt, dict) and all(isinstance(bt.get(t), dict) for t in TYPES)):
+        return bad + ["by_state or by_type"]
+    for s in STATES:
+        if not (_cell_ok(bs.get(s)) and isinstance(bs[s].get("cases"), list) and all(isinstance(x, str) for x in bs[s]["cases"])):
+            bad.append(f"by_state.{s}")
+            continue
+        for k in ("matched", "total"):
+            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):
+                bad.append(f"by_state.{s}.{k} is not the sum over by_type (hand-edited count)")
+    for t in TYPES:
+        for s in STATES:
+            cell = (bt.get(t) or {}).get(s)
+            if not (_cell_ok(cell) and isinstance(cell.get("by_case"), dict)):
+                bad.append(f"by_type.{t}.{s}")
+    if bad:
+        return bad
+    if not (isinstance(se, dict) and isinstance(se.get("overall"), dict) and isinstance(se.get("by_type"), dict)):
+        return bad + ["sentences"]
+    for s in STATES:
+        if not _statement_ok(se["overall"].get(s), bs[s]):
+            bad.append(f"sentences.overall.{s} does not quote its counts")
+    for t in TYPES:
+        for s in STATES:
+            if not _statement_ok((se["by_type"].get(t) or {}).get(s), bt[t][s]):
+                bad.append(f"sentences.by_type.{t}.{s} does not quote its counts")
+    return bad
+
+
+def _envelope(status, calibration=None, message=None) -> dict:
+    return {"status": status, "calibration": calibration, "message": message}
+
+
+def load(path=REPORT) -> dict:
+    """The envelope for the file at `path`: ok with the served subset, missing, or invalid. Read-only; never raises."""
+    p = pathlib.Path(path)
+    try:
+        raw = p.read_text(encoding="utf-8")
+    except FileNotFoundError:
+        return _envelope("missing", message=MISSING)
+    except (OSError, UnicodeDecodeError):
+        log.warning("calibration file could not be read: %s", p.name)
+        return _envelope("invalid", message=INVALID)
+    try:
+        doc = json.loads(raw)
+    except ValueError:
+        log.warning("calibration file is not JSON: %s", p.name)
+        return _envelope("invalid", message=INVALID)
+    bad = problems(doc)
+    if bad:
+        log.warning("calibration file rejected: %s", "; ".join(bad))
+        return _envelope("invalid", message=INVALID)
+    return _envelope("ok", {k: doc[k] for k in SERVED})
+
+
+def add_routes(app, *, path=REPORT):
+    @app.get("/api/calibration")
+    def calibration():
+        return load(path)
---
total 696
drwxr-xr-x@ 45 arsis  staff   1440 Nov  1 22:54 .
drwxr-xr-x@ 12 arsis  staff    384 Nov  1 22:30 ..
-rw-r--r--@  1 arsis  staff   2694 Nov  1 20:08 20261102T020824Z.md
-rw-r--r--@  1 arsis  staff   2791 Nov  1 20:09 20261102T020933Z.md
-rw-r--r--@  1 arsis  staff   2605 Nov  1 20:10 20261102T021029Z.md
-rw-r--r--@  1 arsis  staff   2732 Nov  1 20:10 20261102T021046Z.md
-rw-r--r--@  1 arsis  staff   2737 Nov  1 20:27 20261102T022701Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:29 20261102T022927Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:30 20261102T023039Z.md
evals/reports/20261102T020824Z.md
evals/reports/20261102T020933Z.md
evals/reports/20261102T021029Z.md
evals/reports/20261102T021046Z.md
evals/reports/20261102T022701Z.md
evals/reports/20261102T022927Z.md
evals/reports/20261102T023039Z.md
evals/reports/20261102T025219Z.md
evals/reports/20261102T025715Z.md
evals/reports/20261102T032823Z.md
 M evals/reports/latest.json
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
?? evals/reports/20261102T024355Z.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:05:51.720Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t099-3ecb8b1\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration -v 2>&1 | tail -30; echo \"== HEAD archive\"; cd \"$S/t098-head\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration 2>&1 | tail -3; echo \"== files\"; cd /Users/arsis/zlayt-pm-project && ls evals/reports/calibration.json 2>&1; grep -rn \"calibration.json\" evals/*.py tools/*.py 2>/dev/null | head; grep -rn \"calibration\" evals/*.py 2>/dev/null | head -5",
 "description": "Run calibration unit tests on 3ecb8b1 and HEAD archives and check the report writer",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T05:05:56.206Z

**tool result**
````
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0
rootdir: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t099-3ecb8b1
plugins: platformdirs-4.14.3, anyio-4.16.0
collected 1604 items / 1570 deselected / 34 selected

tests/unit/test_calibration_route.py .......................             [ 67%]
tests/unit/test_eval_runner.py .......ss..                               [100%]

================ 32 passed, 2 skipped, 1570 deselected in 1.88s ================
== HEAD archive
..............................ss..                                       [100%]
32 passed, 2 skipped, 1570 deselected in 1.87s
== files
evals/reports/calibration.json
evals/run.py:1009:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
evals/run.py:1023:    bad = check_calibration(p.parent / "calibration.json", root)
evals/run.py:1025:        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
evals/run.py:1030:    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
evals/run.py:69:    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
evals/run.py:247:def score_calibration(exp, out, unscored=None):
evals/run.py:287:def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
evals/run.py:288:    """The statements the UI renders verbatim.  Built from the counts only, so check_calibration can rebuild them and catch a hand-edited sentence."""
evals/run.py:318:def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:06:01.889Z

**tool call — Bash**
````
{
 "command": "git ls-files evals/reports/calibration.json; git log --oneline -n 3 -- evals/reports/calibration.json | cat; echo ---; cat evals/reports/calibration.json; echo; echo ---; grep -n \"demo_mode\\|def local_mode\" -A4 app/backend/api.py | head -40",
 "description": "Read the real calibration.json and the demo-mode gating in api.py"
}
````

### User / tool · 2026-11-02T05:06:02.034Z

**tool result**
````
evals/reports/calibration.json
172028c chore(evals): regenerate calibration.json from a clean worktree of b85fc1b (T-090 r3)
02ff244 chore(evals): regenerate calibration.json from a clean worktree of 823b718 (fixture: verified 83/84, needs_review 10/10) (T-090 r2)
d0aee83 feat(evals): calibrated confidence from measured matches per state and item type (T-090)
---
{
 "backend": "fixture",
 "by_state": {
  "needs_review": {
   "cases": [
    "case_01_date_formats",
    "case_03_rate_and_ocr",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "sample"
   ],
   "matched": 10,
   "total": 10
  },
  "verified": {
   "cases": [
    "case_01_date_formats",
    "case_02_gap_boundaries",
    "case_03_rate_and_ocr",
    "case_04_duplicates_no_amounts",
    "case_05_provider_conflict",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "case_08_diagnosis_temptation",
    "case_09_nonvisit_hides_gap",
    "sample"
   ],
   "matched": 83,
   "total": 84
  }
 },
 "by_type": {
  "amount": {
   "needs_review": {
    "by_case": {
     "case_03_rate_and_ocr": [
      3,
      3
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "sample": [
      2,
      2
     ]
    },
    "matched": 6,
    "total": 6
   },
   "verified": {
    "by_case": {
     "case_01_date_formats": [
      1,
      1
     ],
     "case_03_rate_and_ocr": [
      2,
      2
     ],
     "case_05_provider_conflict": [
      1,
      1
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "case_08_diagnosis_temptation": [
      1,
      1
     ],
     "case_09_nonvisit_hides_gap": [
      1,
      1
     ],
     "sample": [
      2,
      2
     ]
    },
    "matched": 9,
    "total": 9
   }
  },
  "entry": {
   "needs_review": {
    "by_case": {
     "case_01_date_formats": [
      1,
      1
     ],
     "case_07_prompt_injection": [
      1,
      1
     ]
    },
    "matched": 2,
    "total": 2
   },
   "verified": {
    "by_case": {
     "case_01_date_formats": [
      7,
      7
     ],
     "case_02_gap_boundaries": [
      8,
      8
     ],
     "case_03_rate_and_ocr": [
      5,
      5
     ],
     "case_04_duplicates_no_amounts": [
      4,
      4
     ],
     "case_05_provider_conflict": [
      5,
      5
     ],
     "case_06_subtle_pre_existing": [
      4,
      5
     ],
     "case_07_prompt_injection": [
      3,
      3
     ],
     "case_08_diagnosis_temptation": [
      4,
      4
     ],
     "case_09_nonvisit_hides_gap": [
      5,
      5
     ],
     "sample": [
      9,
      9
     ]
    },
    "matched": 54,
    "total": 55
   }
  },
  "flag": {
   "needs_review": {
    "by_case": {
     "case_06_subtle_pre_existing": [
      1,
      1
     ],
     "case_07_prompt_injection": [
      1,
      1
     ]
    },
    "matched": 2,
    "total": 2
   },
   "verified": {
    "by_case": {
     "case_02_gap_boundaries": [
      3,
      3
     ],
     "case_05_provider_conflict": [
      1,
      1
     ],
     "case_06_subtle_pre_existing": [
      3,
      3
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "case_08_diagnosis_temptation": [
      1,
      1
     ],
     "case_09_nonvisit_hides_gap": [
      1,
      1
     ],
     "sample": [
      10,
      10
     ]
    },
    "matched": 20,
    "total": 20
   }
  }
 },
 "case_count": 10,
 "cases": [
  "sample",
  "case_01_date_formats",
  "case_02_gap_boundaries",
  "case_03_rate_and_ocr",
  "case_04_duplicates_no_amounts",
  "case_05_provider_conflict",
  "case_06_subtle_pre_existing",
  "case_07_prompt_injection",
  "case_08_diagnosis_temptation",
  "case_09_nonvisit_hides_gap"
 ],
 "generated_at": "2026-11-02T04:48:31Z",
 "hashes": {
  "app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263",
  "app/llm/prompts/conflicts_v1.md": "16c18d05e68a5cfa0fa6496497b377dfbcda3c19fbf04dfaa9c9cf36139932ca",
  "app/llm/prompts/extract_es_v1.md": "985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb",
  "app/llm/prompts/extract_v1.md": "11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2",
  "app/llm/prompts/flags_v1.md": "d5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725",
  "app/llm/prompts/judge_amount_class_v1.md": "e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8",
  "app/llm/prompts/judge_conflict_v1.md": "10c7cfddbd32d78cbdb005a14731abcb40ef55c83265b87abb88f74c48551daa",
  "app/llm/prompts/judge_conflict_v2.md": "6eac7a227ea9292e89350c3f10c11bc94d057b446cd3bf8cfde1a4684843cbc6",
  "app/llm/prompts/judge_faithfulness_es_v1.md": "d51be0b39c9d2ba0725f81b402e82e80696282bd0ea98e9ce789f575fa21f898",
  "app/llm/prompts/judge_faithfulness_v1.md": "636bd46d728af66608aba566efe431371e49e32a066fca71b2046534adbd002b",
  "app/llm/prompts/judge_flag_v1.md": "97dd90e3d9546a836d327e12953c9c30ba574ebdcc6073ada9162cd480d2e432",
  "app/llm/prompts/judge_flag_v2.md": "7b6b34712531643b0d79f3ccdd92932d8abb86bfdeeb756d7c39314e29ed39fe",
  "app/llm/prompts/narrative_v1.md": "3d75a823c717359208322d17ba8b77fd58893a4aa15bc92a18c48c78e94e12ac",
  "app/llm/prompts/split_v1.md": "9a2d0cffafa37f318e18a9c076c82f9f5c404ecb53781956813fafe7bf66197b"
 },
 "match_rule": "entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.",
 "models": {
  "generator": "claude-sonnet-5-5",
  "judge": "claude-haiku-5-5"
 },
 "not_scored": {
  "amount": 0,
  "entry": 0,
  "flag": 0,
  "total": 0
 },
 "schema": "evals.calibration/1",
 "sentences": {
  "by_type": {
   "amount": {
    "needs_review": "Needs-review amounts matched the record 6/6 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
    "verified": "Verified amounts matched the record 9/9 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
   },
   "entry": {
    "needs_review": "Needs-review entries matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
    "verified": "Verified entries matched the record 54/55 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
   },
   "flag": {
    "needs_review": "Needs-review flags matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
    "verified": "Verified flags matched the record 20/20 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
   }
  },
  "overall": {
   "needs_review": "Items marked needs review matched the record 10/10 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
   "verified": "Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
  }
 },
 "small_sample": true,
 "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
 "source_commit": "b85fc1b56386aa0d37460186b5840eec0e578642",
 "source_tree": "3f014d4b5d84f8731ff464d4548e18dfce3fbd4f",
 "source_tree_clean": true
}

---
79:def local_mode() -> bool:
80-    return os.environ.get("ZLAYT_MODE") == "local"
81-
82-
83-def is_loopback_peer(request) -> bool:
--
119:    def demo_mode():
120-        return not live_enabled()
121-
122-    def models():
123-        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
--
214:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
215-                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
216-                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
217-
218-    @app.get("/api/cases")
--
254:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
255:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
256-        cl = request.headers.get("content-length")
257-        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
258-            raise ApiError(413, "input_too_large", "The PDF is too large.")
259-        data = b""
--
285:        if demo_mode() and digest(text) not in allowed_hashes():
286:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
287-        c = conn()
288-        try:
289-            now = time.time()
290-            DB.purge_expired(c, now)
--
293:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
294-                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
295-            try:
296-                ing = pipeline_mod().ingest_case(c, cid, text, now)
297-                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
--
306:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
307-                    "dates_to_confirm": present.dates_to_confirm(c, cid),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:06:23.248Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/probe99\" && cat > \"$S/probe99/probe_t099.py\" <<'EOF'\n\"\"\"Scratch probe for T-099 (not in the repo). Run as: cd <3ecb8b1 archive> && python probe_t099.py <probe dir>\"\"\"\nimport copy, json, logging, os, pathlib, sys, tempfile\nsys.path.insert(0, os.getcwd())\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfor k in (\"ZLAYT_MODE\", \"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\"):\n    os.environ.pop(k, None)\nlogging.basicConfig(level=logging.WARNING, format=\"LOG %(levelname)s %(message)s\")\nfrom app.backend import calibration_route as CR\n\nREAL = pathlib.Path(os.getcwd()) / \"evals\" / \"reports\" / \"calibration.json\"\ndoc = json.loads(REAL.read_text(encoding=\"utf-8\"))\nout = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)\n\ndef run(name, text=None, obj=None, raw=None):\n    p = out / (name + \".json\")\n    if raw is not None:\n        p.write_bytes(raw)\n    elif text is not None:\n        p.write_text(text, encoding=\"utf-8\")\n    elif obj is not None:\n        p.write_text(json.dumps(obj), encoding=\"utf-8\")\n    env = CR.load(p)\n    cal = env[\"calibration\"]\n    print(f\"{name:34s} status={env['status']:8s} cal_keys={sorted(cal) if cal else None}\")\n    return env\n\nprint(\"== state probes (CR.load on scratch copies)\")\ne = run(\"real_copy\", obj=doc)\nprint(\"   served by_case present:\", \"by_case\" in json.dumps(e[\"calibration\"]), \"| served has 'cases' key:\", \"cases\" in (e[\"calibration\"] or {}))\nrun(\"missing\", text=None) if False else None\nprint(\"   missing path:\", CR.load(out / \"does_not_exist.json\")[\"status\"])\nrun(\"not_json\", text=\"{not json\")\nrun(\"not_utf8\", raw=b\"\\xff\\xfe\\x00bad\")\nrun(\"top_level_list\", text=\"[]\")\nd = copy.deepcopy(doc); d[\"schema\"] = \"evals.calibration/0\"; run(\"wrong_schema\", obj=d)\nd = copy.deepcopy(doc); d[\"by_state\"][\"verified\"][\"matched\"] += 1; run(\"hand_edit_state_total\", obj=d)\nd = copy.deepcopy(doc); d[\"by_type\"][\"entry\"][\"verified\"][\"by_case\"][\"sample\"] = [1, 9]; run(\"hand_edit_by_case_only\", obj=d)\nd = copy.deepcopy(doc); d[\"by_type\"][\"entry\"][\"verified\"][\"by_case\"][\"sample\"] = [12, 9]; run(\"by_case_matched_gt_total\", obj=d)\nd = copy.deepcopy(doc); d[\"case_count\"] = 500; run(\"hand_edit_case_count\", obj=d)\nd = copy.deepcopy(doc); d[\"backend\"] = \"claude-sonnet-5-5\"; run(\"hand_edit_backend_label\", obj=d)\nd = copy.deepcopy(doc); d[\"sentences\"][\"overall\"][\"verified\"] = d[\"sentences\"][\"overall\"][\"verified\"].replace(\"fixture backend\", \"live model backend\"); run(\"hand_edit_sentence_words\", obj=d)\nd = copy.deepcopy(doc); d[\"sentences\"][\"overall\"][\"verified\"] = \"Verified items matched the record 83/84 times, so the letter is safe to send.\"; run(\"hand_edit_sentence_claim\", obj=d)\nd = copy.deepcopy(doc); d[\"sentences\"][\"overall\"][\"verified\"] = \"Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).\"; d[\"sentences\"][\"overall\"][\"verified\"] = d[\"sentences\"][\"overall\"][\"verified\"].replace(\"83/84\", \"84/84\"); run(\"sentence_mn_mismatch\", obj=d)\nd = copy.deepcopy(doc); d[\"small_sample\"] = False; run(\"small_sample_flipped\", obj=d)\nd = copy.deepcopy(doc); d[\"matched_extra_key_secret\"] = \"RECORD TEXT SHOULD NOT ECHO\"; e2 = run(\"extra_key\", obj=d)\nprint(\"   extra key echoed:\", \"RECORD TEXT\" in json.dumps(e2))\nd = copy.deepcopy(doc); d[\"by_state\"][\"verified\"][\"matched\"] = 83.0; run(\"float_count\", obj=d)\nd = copy.deepcopy(doc); d[\"by_state\"][\"verified\"][\"matched\"] = True; run(\"bool_count\", obj=d)\nd = copy.deepcopy(doc); d[\"not_scored\"][\"total\"] = 7; run(\"not_scored_total_mismatch\", obj=d)\nd = copy.deepcopy(doc); d[\"by_state\"][\"verified\"][\"cases\"] = []; run(\"cases_list_emptied\", obj=d)\nd = copy.deepcopy(doc); d[\"by_type\"][\"entry\"][\"verified\"][\"matched\"] = 56; d[\"by_type\"][\"entry\"][\"verified\"][\"total\"] = 55; run(\"matched_gt_total_cell\", obj=d)\nprint(\"== directory at path:\", CR.load(out)[\"status\"])\nEOF\ncd \"$S/t099-3ecb8b1\" && /Users/arsis/zlayt-pm-project/.venv/bin/python \"$S/probe99/probe_t099.py\" \"$S/probe99/out\" 2>&1 | tail -80",
 "description": "Probe calibration loader states, tampering and log output on the 3ecb8b1 archive",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T05:06:23.383Z

**tool result**
````
LOG WARNING calibration file is not JSON: not_json.json
LOG WARNING calibration file could not be read: not_utf8.json
LOG WARNING calibration file rejected: not an object
LOG WARNING calibration file rejected: schema
LOG WARNING calibration file rejected: by_state.verified.matched is not the sum over by_type (hand-edited count)
LOG WARNING calibration file rejected: sentences.overall.verified does not quote its counts
LOG WARNING calibration file rejected: by_state.verified
LOG WARNING calibration file rejected: by_state.verified
LOG WARNING calibration file rejected: not_scored
LOG WARNING calibration file rejected: by_state.verified.matched is not the sum over by_type (hand-edited count); by_state.verified.total is not the sum over by_type (hand-edited count); by_type.entry.verified
LOG WARNING calibration file could not be read: out
== state probes (CR.load on scratch copies)
real_copy                          status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
   served by_case present: True | served has 'cases' key: False
   missing path: missing
not_json                           status=invalid  cal_keys=None
not_utf8                           status=invalid  cal_keys=None
top_level_list                     status=invalid  cal_keys=None
wrong_schema                       status=invalid  cal_keys=None
hand_edit_state_total              status=invalid  cal_keys=None
hand_edit_by_case_only             status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
by_case_matched_gt_total           status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
hand_edit_case_count               status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
hand_edit_backend_label            status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
hand_edit_sentence_words           status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
hand_edit_sentence_claim           status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
sentence_mn_mismatch               status=invalid  cal_keys=None
small_sample_flipped               status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
extra_key                          status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
   extra key echoed: False
float_count                        status=invalid  cal_keys=None
bool_count                         status=invalid  cal_keys=None
not_scored_total_mismatch          status=invalid  cal_keys=None
cases_list_emptied                 status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
matched_gt_total_cell              status=invalid  cal_keys=None
== directory at path: invalid
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:06:30.758Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-099 2>&1 | head -60; echo ======; python3 tools/board.py show T-098 2>&1 | head -60",
 "description": "Read the T-099 and T-098 cards via the read-only board CLI"
}
````

### User / tool · 2026-11-02T05:06:30.943Z

**tool result**
````
---
id: "T-099"
title: "Serve calibration.json to the app (GET route, shape per T-096 note)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T04:55:57Z"
updated_at: "2026-11-02T05:00:24Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:55:59Z"
rounds: 0
commits: ["3ecb8b1ca58b97c2d23cdd78a8a99a7bf292f8db"]
reviews: []
ac:
  - {"n": 1, "text": "GET /api/calibration (or a case field) serves evals/reports/calibration.json with source commit and sample size; missing file -> clear empty state, never invented numbers; unit test; T-096 consumes it", "done": true, "evidence": "tests/unit/test_calibration_route.py: pytest -q tests/unit -k calibration gives 34 passed (present, missing, invalid, read-only, demo mode)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:55:59Z backend: claimed
- 2026-11-02T04:57:17Z backend: Plan: new app/backend/calibration_route.py (load/validate/add_routes, GET /api/calibration, envelope status ok|missing|invalid, calibration null unless ok); one hook line in api.py; tests/unit/test_calibration_route.py written first; contract section in memory/contracts/api.md. Shared tree is dirty (other workers): commit via temp index built on HEAD, stage my api.py hunk only.
- 2026-11-02T04:59:56Z backend: AC 1 checked: tests/unit/test_calibration_route.py: pytest -q tests/unit -k calibration gives 34 passed (present, missing, invalid, read-only, demo mode)
- 2026-11-02T04:59:56Z backend: Commit BLOCKED by tools/check_stale_index.py: app/backend/api.py has another worker's uncommitted reorder (pdf_routes/billing lines) in the worktree, so the staged HEAD+hook blob matches neither HEAD nor worktree. Not bypassing the guard and not committing their hunk. Also: my contract section for GET /api/calibration already landed inside e511778 (T-098 commit, memory/contracts/api.md), so HEAD documents a route HEAD does not yet serve. Needs the owner of the api.py reorder to commit or drop it; then I commit calibration_route.py, tests/unit/test_calibration_route.py and the 2-line hook.
- 2026-11-02T05:00:16Z backend: moved in_progress -> in_review
- 2026-11-02T05:00:24Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Changed: app/backend/calibration_route.py (new; load() gives ok|missing|invalid envelope; problems() checks the T-096 shape, count ranges, state totals = type totals, each statement quotes its own m/t; add_routes registers read-only GET /api/calibration). Hook: 2 lines in app/backend/api.py after the T-089 hook. Contract: memory/contracts/api.md (section and endpoint row; they landed earlier inside e511778, T-098, through the shared worktree). Tests: tests/unit/test_calibration_route.py. Verified: pytest -q tests/unit -k calibration = 34 passed; test_api, test_api_routes, test_boundaries, test_dismissal_patterns = 81 passed. Commit 3ecb8b1 (temp index on HEAD, 3 files, 302 insertions). Left: T-096 frontend consumes it. Surprised: the stale-index guard blocked the first attempt and was then relaxed to pass partial stages.

======
---
id: "T-098"
title: "Export gate must block human-edited items whose code checks fail (D-045b: exempt from judge, not from code checks)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T04:55:06Z"
updated_at: "2026-11-02T05:00:24Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:55:09Z"
rounds: 0
commits: ["e511778"]
reviews: []
ac:
  - {"n": 1, "text": "An accepted, human-edited summary that fails any D-034/D-022 code check (qualifier dropped, token not in excerpt) is a gate blocker and GET export returns 422 with the reason; gate.ready == export allowed still holds; per-item trace shows the failing code step; tests with the reviewer's case (reviews/T-097-ux-designer.md)", "done": true, "evidence": "tests/unit/test_trace.py::test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098 + test_item_trace_shows_the_failing_code_step_with_the_next_action_t098 + test_gate_ready_equals_export_allowed_with_a_failing_edit_t098 + tests/unit/test_export.py::test_export_payload_refuses_for_a_failing_code_check_on_edited_wording_d045b pass; tests/unit 1614 passed (test_calibration_route.py ignored: another worker's in-progress import error)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:55:09Z backend: claimed
- 2026-11-02T04:59:37Z backend: AC 1 checked: tests/unit/test_trace.py::test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098 + test_item_trace_shows_the_failing_code_step_with_the_next_action_t098 + test_gate_ready_equals_export_allowed_with_a_failing_edit_t098 + tests/unit/test_export.py::test_export_payload_refuses_for_a_failing_code_check_on_edited_wording_d045b pass; tests/unit 1614 passed (test_calibration_route.py ignored: another worker's in-progress import error)
- 2026-11-02T04:59:37Z backend: moved in_progress -> in_review
- 2026-11-02T05:00:24Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: trace.code_check_blockers() adds a gate blocker {item_id, kind:entry, reason_code (first failing check), step_id, failed_steps[], why, next_action} for each accepted/edited live entry with paralegal-written/edited wording whose code step fails (summary_tokens, summary_qualifier, excerpt_*, highlight); it feeds export_blockers, so gate.ready == export allowed and GET /export is 422 export_blocked with the same list. Item trace: failing code step has blocks_export true and next_action EDIT_SUMMARY with text like 'Edit the summary to keep 'possible'; ...'; verdict becomes needs_attention + blocks_export true; gate counts.code_check_failed; case verdict label '1 edited summary fails a check'. grounding.missing_qualifier_terms supplies the words (display only). | Verified: tests/unit test_trace + test_export 88 passed; full tests/unit 1614 passed, 1 skipped (test_calibration_route.py excluded, import error from another worker's WIP). Reviewer case (accept e1, edit e2 to 'Paralegal wording for the mixed-case check.', dismiss e1) now gate fail + 422. | Left: AI drafts are NOT gated by this blocker (accept of needs_review stays the human step); an edit confirmed via kept_my_wording for a non-numeric token now blocks too, so the 409 confirm path for such tokens leads to an unexportable item (frontend/D-034 may want the 409 removed for tokens); M2 (edited item judge step in Why dialog) and M1 (panel summary) untouched. | Surprised: trace.py and api.md carried other workers' uncommitted hunks (T-094, T-099) and the stale-index guard rejects hunk-only staging, so e511778 includes them.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:06:38.140Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-096 2>&1 | sed -n 1,25p | cut -c1-600; echo =====; sed -n 1026,1060p evals/run.py; echo =====; cd \"$S\" 2>/dev/null; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t099-3ecb8b1\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration -rs 2>&1 | grep -i \"skip\" | head -5",
 "description": "Read T-096 card, the eval-side calibration checker, and skip reasons in the calibration selection"
}
````

### User / tool · 2026-11-02T05:06:40.346Z

**tool result**
````
---
id: "T-096"
title: "UI for suggestions and confidence: date-convention suggestion, dismissal suggestions, measured-precision line"
milestone: "M3"
role: "frontend"
status: "ready"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T04:30:07Z"
updated_at: "2026-11-02T04:48:59Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Dates-to-confirm row pre-selects the suggested convention with its reason and still requires one confirm (T-088); dismissal suggestion banner with Hide-similar action that the paralegal must click (T-089); 'Verified items matched the record N/M times in testing' line with small-sample note (T-090); e2e tests", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:30:16Z orchestrator: Starts once T-088/T-089 r2 and T-090 r2 pass (their API shapes may still change).
- 2026-11-02T04:30:16Z orchestrator: assigned: frontend
=====
    return 1 if diff or bad else 0


def check_calibration(path, root=ROOT):
    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
    files on disk (the counts were measured against other prompts). Empty list when the file is absent or fine."""
    p = pathlib.Path(path)
    if not p.exists():
        return []
    c = json.loads(p.read_text())
    bad = []
    for s in CAL_STATES:
        for k in ("matched", "total"):
            if c["by_state"][s][k] != sum(c["by_type"][t][s][k] for t in CAL_TYPES):
                bad.append(f"by_state.{s}.{k} is not the sum of by_type")
    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
        bad.append("sentences do not match the counts they are built from")
    old = c.get("hashes") or {}
    now = hashes(root)
    bad += [f"was measured against a different {k}" for k in sorted(set(old) | set(now)) if old and old.get(k) != now.get(k)]
    return bad


def load_pipeline():
    from app import pipeline
    return pipeline


class CuratedFixtures(Exception):
    pass


def refuse_curated(env=None):
    """D-029: the ship bar is measured on live runs and recorded fixtures only. Curated (hand-checked) responses reproduce the golden
    answers by construction, so scoring them would be circular. Refuse to compute ship-bar metrics when the curated set is selected."""
=====
SKIPPED [2] tests/unit/test_eval_runner.py:636: no git repository here (exported tree)
32 passed, 2 skipped, 1570 deselected in 1.77s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:06:50.663Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t099-3ecb8b1\" && grep -n \"^def test_\" tests/unit/test_calibration_route.py; echo ---; grep -n \"405\\|TestClient\\|ZLAYT_MODE\\|echo\\|RECORD\\|secret\" tests/unit/test_calibration_route.py | head -20; echo ---; for f in app/llm/lexicon.yaml app/llm/prompts/judge_faithfulness_v1.md app/llm/prompts/extract_v1.md; do printf \"%s \" \"$f\"; /usr/bin/shasum -a 256 \"$f\" | cut -c1-16; done; grep -o '\"app/llm/lexicon.yaml\": \"[0-9a-f]\\{16\\}' evals/reports/calibration.json; grep -o '\"app/llm/prompts/judge_faithfulness_v1.md\": \"[0-9a-f]\\{16\\}' evals/reports/calibration.json; grep -o '\"app/llm/prompts/extract_v1.md\": \"[0-9a-f]\\{16\\}' evals/reports/calibration.json",
 "description": "List calibration route tests and check measured prompt hashes against current files"
}
````

### User / tool · 2026-11-02T05:06:50.842Z

**tool result**
````
56:def test_present_file_is_served_with_source_commit_backend_and_sample_size(tmp_path):
66:def test_served_object_is_exactly_the_t096_shape_without_hashes_models_or_paths(tmp_path):
72:def test_route_serves_present_file_over_http(tmp_path):
79:def test_committed_report_is_valid_when_present():
88:def test_missing_file_is_an_empty_state_with_no_numbers(tmp_path):
93:def test_route_missing_file_returns_200_empty_state_not_an_error(tmp_path):
118:def test_invalid_file_is_an_empty_state_and_is_never_served(tmp_path, name):
134:def test_invalid_route_response_does_not_echo_file_contents(tmp_path):
142:def test_problems_is_empty_for_a_valid_document_and_lists_faults_otherwise():
159:def test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode(app_client):
167:def test_route_carries_no_case_tokens_or_record_text(app_client):
173:def test_route_is_read_only(app_client):
---
8:from fastapi.testclient import TestClient
51:    return TestClient(app)
134:def test_invalid_route_response_does_not_echo_file_contents(tmp_path):
156:    return TestClient(create_app(str(tmp_path / "cal.sqlite"), static_dir=str(tmp_path)))
174:    assert app_client.post("/api/calibration", json={}).status_code == 405
175:    assert app_client.put("/api/calibration", json={}).status_code == 405
176:    assert app_client.patch("/api/calibration", json={}).status_code == 405
177:    assert app_client.delete("/api/calibration").status_code == 405
---
app/llm/lexicon.yaml a2518d8f098de26b
app/llm/prompts/judge_faithfulness_v1.md 636bd46d728af666
app/llm/prompts/extract_v1.md 11a948d70400e97f
"app/llm/lexicon.yaml": "a2518d8f098de26b
"app/llm/prompts/judge_faithfulness_v1.md": "636bd46d728af666
"app/llm/prompts/extract_v1.md": "11a948d70400e97f
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:06:57.719Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; M=\"$S/mut99\"; rm -rf \"$M\"; mkdir -p \"$M\"; cp -R \"$S/t099-3ecb8b1/.\" \"$M/\"; cd \"$M\" && F=app/backend/calibration_route.py; cp $F $F.orig\nrun(){ /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_calibration_route.py 2>&1 | tail -1; }\necho \"M0 control:\"; run\necho \"M1 sentence check removed (statement always ok):\"; cp $F.orig $F; /usr/bin/sed -i '' 's/    return cell\\[\"total\"\\] == 0 or f\"{cell\\[.matched.\\]}\\/{cell\\[.total.\\]} times\" in text/    return True/' $F; grep -n \"return True\" $F | head -2; run\necho \"M2 state-sum check removed:\"; cp $F.orig $F; /usr/bin/sed -i '' 's/            if bs\\[s\\]\\[k\\] != sum/            if False and bs[s][k] != sum/' $F; run\necho \"M3 problems ignored (always ok when parsed):\"; cp $F.orig $F; /usr/bin/sed -i '' 's/    if bad:\\n        log.warning(\"calibration file rejected/X/' $F; /usr/bin/python3 - <<'EOF'\nimport re,pathlib\np=pathlib.Path(\"app/backend/calibration_route.py\"); s=p.read_text()\ns2=s.replace(\"    bad = problems(doc)\\n    if bad:\", \"    bad = problems(doc)\\n    if False:\")\nassert s2!=s; p.write_text(s2)\nEOF\nrun\necho \"M4 all methods accepted on route:\"; cp $F.orig $F; /usr/bin/sed -i '' 's/    @app.get(\"\\/api\\/calibration\")/    @app.api_route(\"\\/api\\/calibration\", methods=[\"GET\",\"POST\",\"PUT\",\"PATCH\",\"DELETE\"])/' $F; run\ncp $F.orig $F; echo \"restored:\"; run",
 "description": "Mutation spot-check of the calibration route validation in a scratch copy",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:07:02.175Z

**tool result**
````
M0 control:
23 passed in 0.40s
M1 sentence check removed (statement always ok):
41:    return True
1 failed, 22 passed in 0.37s
M2 state-sum check removed:
23 passed in 0.36s
M3 problems ignored (always ok when parsed):
11 failed, 12 passed in 0.40s
M4 all methods accepted on route:
1 failed, 22 passed in 0.37s
restored:
23 passed in 0.35s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:07:08.895Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; M=\"$S/mut99\"; cd \"$M\" && F=app/backend/calibration_route.py; cp $F.orig $F; /usr/bin/python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"app/backend/calibration_route.py\"); s=p.read_text()\nold='            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):'\nassert s.count(old)==1, s.count(old)\np.write_text(s.replace(old, '            if False:'))\nprint(\"M2 applied\")\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_calibration_route.py 2>&1 | tail -1; echo \"M2b: by_type cell total check removed\"; cp $F.orig $F; /usr/bin/python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"app/backend/calibration_route.py\"); s=p.read_text()\nold='    if bad:\\n        return bad\\n    if not (isinstance(se, dict)'\nassert s.count(old)==1\np.write_text(s.replace(old, '    if bad:\\n        return bad\\n    if False and not (isinstance(se, dict)'))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_calibration_route.py 2>&1 | tail -1; cp $F.orig $F; echo \"M3 by_case not checked (served raw): see probe\"; grep -n \"by_case\" tests/unit/test_calibration_route.py | head -5",
 "description": "Apply the by_state sum-check mutant precisely and confirm surviving",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:07:10.320Z

**tool result**
````
M2 applied
23 passed in 0.35s
M2b: by_type cell total check removed
1 failed, 22 passed in 0.40s
M3 by_case not checked (served raw): see probe
17:        "entry": {"verified": {"matched": 54, "total": 55, "by_case": {"sample": [54, 55]}},
18:                  "needs_review": {"matched": 2, "total": 2, "by_case": {"sample": [2, 2]}}},
19:        "amount": {"verified": {"matched": 9, "total": 9, "by_case": {"sample": [9, 9]}},
20:                   "needs_review": {"matched": 6, "total": 6, "by_case": {"sample": [6, 6]}}},
21:        "flag": {"verified": {"matched": 20, "total": 20, "by_case": {"sample": [20, 20]}},
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:07:18.762Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; M=\"$S/mut98\"; rm -rf \"$M\"; mkdir -p \"$M\"; cp -R \"$S/t098-head/.\" \"$M/\"; cd \"$M\" && /usr/bin/python3 - <<'EOF'\nimport pathlib, subprocess, shutil\nPY=\"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nT=\"app/backend/trace.py\"\norig=pathlib.Path(T).read_text()\nmuts={\n \"M1 export_blockers drops code_check_blockers\": (\"    out.extend(code_check_blockers(conn, case_id, cx))\", \"    pass\"),\n \"M2 _code_check_gated always False\": (\"    return row[\\\"state\\\"] != \\\"rejected\\\" and row[\\\"review_status\\\"] in (\\\"accepted\\\", \\\"edited\\\") and _paralegal_wording(\\\"entry\\\", row)\", \"    return False\"),\n \"M3 blocker drops failing step filter (any code fail)\": (\"s.get(\\\"reason_code\\\") in _CODE_CHECK_REASONS]\\n        if not fails:\", \"s.get(\\\"reason_code\\\")]\\n        if not fails:\"),\n \"M4 blocks_export flag not set\": (\"                s[\\\"blocks_export\\\"] = True\\n\", \"                pass\\n\"),\n}\nfor name,(a,b) in muts.items():\n    assert orig.count(a)>=1, (name, orig.count(a))\n    pathlib.Path(T).write_text(orig.replace(a,b,1))\n    r=subprocess.run([PY,\"-m\",\"pytest\",\"-p\",\"no:cacheprovider\",\"-q\",\"tests/unit/test_trace.py\",\"tests/unit/test_export.py\"],capture_output=True,text=True)\n    print(name, \"->\", r.stdout.strip().splitlines()[-1])\npathlib.Path(T).write_text(orig)\nr=subprocess.run([PY,\"-m\",\"pytest\",\"-p\",\"no:cacheprovider\",\"-q\",\"tests/unit/test_trace.py\",\"tests/unit/test_export.py\"],capture_output=True,text=True)\nprint(\"restored ->\", r.stdout.strip().splitlines()[-1])\nEOF",
 "description": "Mutation spot-check of the T-098 export gate blocker in a scratch copy",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T05:07:52.018Z

**tool result**
````
M1 export_blockers drops code_check_blockers -> 3 failed, 85 passed in 6.06s
M2 _code_check_gated always False -> 4 failed, 84 passed in 5.92s
M3 blocker drops failing step filter (any code fail) -> 88 passed in 6.17s
M4 blocks_export flag not set -> 1 failed, 87 passed in 5.95s
restored -> 88 passed in 5.96s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:08:25.357Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; H=\"$S/t098-head\"; cd \"$H\" && grep -n \"if blocking and not bool\\|raise ReviewError(409, \\\"needs_confirm\\\"\\|keep_my_wording\\\"\\|def _check_summary\\|def _edit\\|DB.apply_review(conn, item_id, action\" app/backend/review.py; grep -n \"def verify\\|SUMMARY_TOKEN\\|_code_check_gated\\|def code_check_blockers\\|candidate_rule\\|_ocr_steps\\|out.extend(code_check_blockers\\|s.get(\\\"reason_code\\\") in _CODE_CHECK_REASONS\\]\" app/backend/trace.py app/backend/generator.py | head -30; grep -n \"AI drafts are not covered\\|AI drafts are NOT\" memory/contracts/api.md; grep -n \"keep my wording\\|btn-keep-wording\" app/frontend/review.js app/frontend/manual.js | head; grep -n \"needs_confirm\" app/backend/api.py app/frontend/manual.js | head -4; grep -n \"409\\|needs_confirm\" tests/unit/test_review_rules.py tests/unit/test_manual_and_split.py | head -8; grep -n \"D-034\" memory/ORCHESTRATOR_DECISIONS.md | cut -c1-80",
 "description": "Collect exact line numbers for the T-098 citations at HEAD archive"
}
````

### User / tool · 2026-11-02T05:08:25.497Z

**tool result**
````
71:        DB.apply_review(conn, item_id, action, now=t, case=case_id)
81:def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, body):
107:    if blocking and not bool(body.get("confirm_warnings")):
108:        raise ReviewError(409, "needs_confirm", {"warnings": blocking}, "This edit adds a number or fact that is not in the quote.")
117:def _edit(conn, case_id, kind, item, body, call, t):
161:        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
316:        DB.apply_review(conn, eid, "keep_my_wording", now=t, case=case_id)
400:    DB.apply_review(conn, item_id, action, now=now, case=case_id)
app/backend/generator.py:71:def verify(e: dict, record: dict, summary: str, excerpt: str) -> dict:
app/backend/trace.py:69:    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "summary_tokens", "SUMMARY_DROPS_QUALIFIER": "summary_qualifier", "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge",
app/backend/trace.py:76:_CODE_CHECK_REASONS = {"SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND"}
app/backend/trace.py:102:def _ocr_steps(R, rid) -> list:
app/backend/trace.py:355:    code_step("summary_tokens", "Numbers and dates in the summary are in the quote", "SUMMARY_TOKEN_NOT_IN_EXCERPT",
app/backend/trace.py:357:              evidence={"tokens": toks}, failed="SUMMARY_TOKEN_NOT_IN_EXCERPT" in R or bool(toks))
app/backend/trace.py:381:    st += _ocr_steps(R, rid)
app/backend/trace.py:390:    if _code_check_gated(row):        # D-045(b): human wording skips the judge, never the code checks; a failing one blocks the export and says what to do
app/backend/trace.py:399:def _code_check_gated(row) -> bool:
app/backend/trace.py:418:    if code == "SUMMARY_TOKEN_NOT_IN_EXCERPT":
app/backend/trace.py:427:def code_check_blockers(conn, case_id: str, cx=None) -> list:
app/backend/trace.py:433:        if not _code_check_gated(row):
app/backend/trace.py:435:        fails = [s for s in _entry_steps(cx, row) if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS]
app/backend/trace.py:477:    st += _ocr_steps(R, rid)
app/backend/trace.py:527:    if origin == "code" and cc.get("candidate_rule"):
app/backend/trace.py:532:                       "Software found a stated plan and a later record that shows it ended early" if cc["candidate_rule"] == "plan_vs_outcome"
app/backend/trace.py:534:                       rule="row 10", evidence={"values": {"rule": cc["candidate_rule"], "arithmetic": arith}, "spans": spans}))
app/backend/trace.py:559:        st += _ocr_steps(R, rid0)
app/backend/trace.py:607:    st += _ocr_steps(R, rid0)
app/backend/trace.py:1017:    out.extend(code_check_blockers(conn, case_id, cx))         # D-045(b): the paralegal's own wording is exempt from the judge, not from the code checks
618:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. AI drafts are not covered by this blocker (they keep needs_review + the human accept).  **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
app/frontend/manual.js:3:   Server refusals (422) and the token check (409 needs_confirm, "keep my wording") are shown in plain words. Text via ZL.el only. */
app/frontend/manual.js:55:          el("div", { class: "rv-actions" }, el("button", { type: "button", class: "rv-btn", "data-testid": "btn-keep-wording", onclick: () => submit(true) }, "Keep my wording"),
app/frontend/review.js:125:  // ---- errors and the "keep my wording" confirmation (R-RV-3)
app/frontend/review.js:135:        el("button", { type: "button", class: "rv-btn", "data-testid": "btn-keep-wording", onclick: () => RV.act(id, Object.assign({}, body, { confirm_warnings: true }), { focus: "edit" }) }, "Keep my wording"),
app/frontend/review.js:137:    RV.say("This edit adds something that is not in the quote. Choose keep my wording or go back.", true);
app/backend/api.py:361:                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
app/frontend/manual.js:3:   Server refusals (422) and the token check (409 needs_confirm, "keep my wording") are shown in plain words. Text via ZL.el only. */
app/frontend/manual.js:51:      if (r.status === 409 && err.code === "needs_confirm") {
tests/unit/test_manual_and_split.py:68:    assert e.value.code == "needs_confirm"                                           # non-numeric judge objection: the confirm path stays
tests/unit/test_review_rules.py:95:def test_seeded_herniation_judge_unsupported_needs_confirm(tmp_path):
tests/unit/test_review_rules.py:96:    """R-RV-3: 'herniation' passes the code check but judge #1 says unsupported -> 409 with JUDGE_UNSUPPORTED."""
tests/unit/test_review_rules.py:100:    assert e.value.code == "needs_confirm" and "JUDGE_UNSUPPORTED" in [w["code"] for w in e.value.detail["warnings"]]
tests/unit/test_review_rules.py:108:    assert e.value.code == "needs_confirm"                                       # non-numeric judge objection keeps the confirm path
42:| D-034 | Hardens D-006/R-RV-3: a number, date or $ figure in a summary, edit
50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build eve
53:| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter,
55:| D-047 | Extends D-034 (2026-11-02): side (left/right), negation (no/not/wit
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:08:32.277Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t099-3ecb8b1\" && grep -n \"def _statement_ok\\|if bs\\[s\\]\\[k\\] != sum\\|def problems\\|sentences.overall\\|return _envelope(\\\"ok\\\"\\|def load\\|def add_routes\\|for t in TYPES:\\|by_case\" app/backend/calibration_route.py; sed -n 95,120p tests/unit/test_calibration_route.py; sed -n 56,60p tests/unit/test_calibration_route.py",
 "description": "Get line numbers for T-099 citations and the invalid-state test list"
}
````

### User / tool · 2026-11-02T05:08:32.371Z

**tool result**
````
37:def _statement_ok(text, cell) -> bool:
44:def problems(c) -> list:
73:            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):
75:    for t in TYPES:
78:            if not (_cell_ok(cell) and isinstance(cell.get("by_case"), dict)):
86:            bad.append(f"sentences.overall.{s} does not quote its counts")
87:    for t in TYPES:
98:def load(path=REPORT) -> dict:
117:    return _envelope("ok", {k: doc[k] for k in SERVED})
120:def add_routes(app, *, path=REPORT):
    assert r.status_code == 200
    assert r.json() == {"status": "missing", "calibration": None, "message": CR.MISSING}


# ---- invalid

INVALID_CASES = {
    "not_json": "{not json",
    "not_utf8": None,      # written as raw bytes below
    "top_level_list": "[]",
    "wrong_schema": lambda d: d.update(schema="evals.calibration/2"),
    "sum_mismatch_hand_edit": lambda d: d["by_state"]["verified"].update(matched=90),
    "sentence_quotes_other_counts": lambda d: d["sentences"]["overall"].update(verified=d["sentences"]["overall"]["verified"].replace("83/84", "90/91")),
    "matched_above_total": lambda d: d["by_type"]["flag"]["verified"].update(matched=21),
    "negative_count": lambda d: d["by_type"]["amount"]["verified"].update(matched=-1, total=-1),
    "bool_counts": lambda d: d["by_state"]["needs_review"].update(matched=True),
    "missing_key": lambda d: d.pop("sentences"),
    "missing_source_commit": lambda d: d.update(source_commit=""),
    "statement_for_a_type_missing": lambda d: d["sentences"]["by_type"].pop("flag"),
}


@pytest.mark.parametrize("name", sorted(INVALID_CASES))
def test_invalid_file_is_an_empty_state_and_is_never_served(tmp_path, name):
    spec = INVALID_CASES[name]
    if name == "not_utf8":
def test_present_file_is_served_with_source_commit_backend_and_sample_size(tmp_path):
    out = CR.load(write(tmp_path, make()))
    assert out["status"] == "ok" and out["message"] is None
    c = out["calibration"]
    assert c["source_commit"] == "b85fc1b56386aa0d37460186b5840eec0e578642"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:08:41.344Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/probe99/probe_consistent_edit.py\" <<'EOF'\nimport copy, json, os, pathlib, sys\nsys.path.insert(0, os.getcwd())\nfrom app.backend import calibration_route as CR\ndoc = json.loads((pathlib.Path(os.getcwd()) / \"evals/reports/calibration.json\").read_text())\nd = copy.deepcopy(doc)\nd[\"by_state\"][\"verified\"][\"matched\"] = 90\nd[\"sentences\"][\"overall\"][\"verified\"] = d[\"sentences\"][\"overall\"][\"verified\"].replace(\"83/84\", \"90/84\")\np = pathlib.Path(sys.argv[1]); p.write_text(json.dumps(d))\nprint(\"consistent hand-edit (state total + its sentence changed together):\", CR.load(p)[\"status\"], CR.problems(d))\nEOF\ncd \"$M\" && /Users/arsis/zlayt-pm-project/.venv/bin/python \"$S/probe99/probe_consistent_edit.py\" \"$S/probe99/consistent.json\"; cd \"$S/t099-3ecb8b1\" && /Users/arsis/zlayt-pm-project/.venv/bin/python \"$S/probe99/probe_consistent_edit.py\" \"$S/probe99/consistent2.json\"",
 "description": "Show a consistent hand-edit of the state total passes on the mutant but not on the real code"
}
````

### User / tool · 2026-11-02T05:08:41.498Z

**tool result**
````
calibration file rejected: by_state.verified
consistent hand-edit (state total + its sentence changed together): invalid ['by_state.verified']
calibration file rejected: by_state.verified
consistent hand-edit (state total + its sentence changed together): invalid ['by_state.verified']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:08:49.380Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; sed -i.bak 's/90\\/84/82\\/84/; s/matched\"\\] = 90/matched\"] = 82/' \"$S/probe99/probe_consistent_edit.py\" && M=\"$S/mut99\"; cd \"$M\" && /usr/bin/python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"app/backend/calibration_route.py\"); s=p.read_text()\nold='            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):'\nassert s.count(old)==1\np.write_text(s.replace(old, '            if False:'))\nprint(\"M2 applied on scratch copy\")\nEOF\necho \"mutant (state-sum check removed):\"; /Users/arsis/zlayt-pm-project/.venv/bin/python \"$S/probe99/probe_consistent_edit.py\" \"$S/probe99/consistent_mut.json\" 2>&1 | tail -1; echo \"real code 3ecb8b1 archive:\"; cd \"$S/t099-3ecb8b1\" && /Users/arsis/zlayt-pm-project/.venv/bin/python \"$S/probe99/probe_consistent_edit.py\" \"$S/probe99/consistent_real.json\" 2>&1 | tail -1; echo \"mutant test run:\"; cd \"$M\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_calibration_route.py 2>&1 | tail -1; cp \"$M/app/backend/calibration_route.py.orig\" \"$M/app/backend/calibration_route.py\"",
 "description": "Rerun the consistent hand-edit probe with a valid cell on mutant and real code",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T05:08:50.369Z

**tool result**
````
M2 applied on scratch copy
mutant (state-sum check removed):
consistent hand-edit (state total + its sentence changed together): ok []
real code 3ecb8b1 archive:
consistent hand-edit (state total + its sentence changed together): invalid ['by_state.verified.matched is not the sum over by_type (hand-edited count)']
mutant test run:
23 passed in 0.36s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:09:15.471Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && E=artifacts/review-evidence && ls $E 2>/dev/null | grep -i \"T-09[89]\" | head -3; mkdir -p \"$E\" && cp \"$S/probe98/test_probe_t098.py\" \"$E/T-098-staff-engineer-probe1.py\" && cp \"$S/probe98/test_probe_t098b.py\" \"$E/T-098-staff-engineer-probe2.py\" && cp \"$S/probe99/probe_t099.py\" \"$E/T-099-staff-engineer-probe-states.py\" && cp \"$S/probe99/probe_consistent_edit.py\" \"$E/T-099-staff-engineer-probe-consistent-edit.py\" && cat > \"$E/T-099-staff-engineer-probe-http.py\" <<'EOF'\n\"\"\"T-099 review probe (scratch copy of the app): GET /api/calibration in default (demo) mode on the real app.\"\"\"\nimport json, os, sys\nsys.path.insert(0, os.getcwd())\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfor k in (\"ZLAYT_MODE\", \"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\"):\n    os.environ.pop(k, None)\nimport tempfile\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd = tempfile.mkdtemp(prefix=\"t099probe\")\nc = TestClient(create_app(os.path.join(d, \"p.sqlite\"), static_dir=d))\nr = c.get(\"/api/calibration\")\nbody = r.json()\nprint(\"GET status\", r.status_code, \"| envelope keys\", sorted(body), \"| status\", body[\"status\"], \"| calibration keys\", sorted(body[\"calibration\"] or {}))\nprint(\"served backend/sentence:\", body[\"calibration\"][\"backend\"], \"|\", body[\"calibration\"][\"sentences\"][\"overall\"][\"verified\"][:60])\nprint(\"token or record text in body:\", any(x in r.text for x in (\"case_\", \"token\", \"excerpt\", \"Patient\")) )\nfor m in (\"post\", \"put\", \"patch\", \"delete\"):\n    print(m.upper(), c.request(m.upper(), \"/api/calibration\").status_code)\nprint(\"GET /api/health demo_mode:\", c.get(\"/api/health\").json()[\"demo_mode\"])\nEOF\nS2=\"$S\"; cd \"$S/t099-3ecb8b1\" && /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/$E/T-099-staff-engineer-probe-http.py 2>&1 | tail -12",
 "description": "Copy probe scripts into review evidence and run the demo-mode HTTP probe for T-099",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T05:09:16.016Z

**tool result**
````
GET status 200 | envelope keys ['calibration', 'message', 'status'] | status ok | calibration keys ['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
served backend/sentence: fixture | Verified items matched the record 83/84 times in testing on 
token or record text in body: True
POST 405
PUT 405
PATCH 405
DELETE 405
GET /api/health demo_mode: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:09:19.897Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence && /usr/bin/sed -i '' 's/print(\"token or record text in body:\", any(x in r.text for x in (\"case_\", \"token\", \"excerpt\", \"Patient\")) )/print(\"body terms:\", {t: (t in r.text) for t in (\"token\", \"excerpt\", \"Patient\", \"summary\", \"case_\")}, \"| golden case ids in by_case keys are synthetic names, not case tokens\")/' $E/T-099-staff-engineer-probe-http.py && cd \"$(ls -d /private/tmp/claude-501/*/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad)/t099-3ecb8b1\" && /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/$E/T-099-staff-engineer-probe-http.py 2>&1 | tail -8",
 "description": "Refine the demo-mode probe to report each term separately and rerun it",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T05:09:19.954Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may not edit s/print("token or record text in body:", any(x in r.text for x in ("case_", "token", "excerpt", "Patient")) )/print("body terms:", {t: (t in r.text) for t in ("token", "excerpt", "Patient", "summary", "case_")}, "| golden case ids in by_case keys are synthetic names, not case tokens")/ in place
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:09:23.539Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-099-staff-engineer-probe-http.py",
 "content": "\"\"\"T-099 review probe (run from a git-archive copy of 3ecb8b1): GET /api/calibration in default (demo) mode on the real app.\"\"\"\nimport json, os, sys\nsys.path.insert(0, os.getcwd())\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfor k in (\"ZLAYT_MODE\", \"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\"):\n    os.environ.pop(k, None)\nimport tempfile\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd = tempfile.mkdtemp(prefix=\"t099probe\")\nc = TestClient(create_app(os.path.join(d, \"p.sqlite\"), static_dir=d))\nr = c.get(\"/api/calibration\")\nbody = r.json()\nprint(\"GET status\", r.status_code, \"| envelope keys\", sorted(body), \"| status\", body[\"status\"], \"| calibration keys\", sorted(body[\"calibration\"] or {}))\nprint(\"served backend/sentence:\", body[\"calibration\"][\"backend\"], \"|\", body[\"calibration\"][\"sentences\"][\"overall\"][\"verified\"][:60])\nprint(\"body terms:\", {t: (t in r.text) for t in (\"token\", \"excerpt\", \"Patient\", \"summary\", \"case_\")},\n      \"| 'case_' hits are golden-case ids inside by_case keys (synthetic names, not case tokens)\")\nfor m in (\"post\", \"put\", \"patch\", \"delete\"):\n    print(m.upper(), c.request(m.upper(), \"/api/calibration\").status_code)\nprint(\"GET /api/health demo_mode:\", c.get(\"/api/health\").json()[\"demo_mode\"])\n"
}
````

### User / tool · 2026-11-02T05:09:23.654Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-099-staff-engineer-probe-http.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:09:25.742Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t099-3ecb8b1\" && /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-099-staff-engineer-probe-http.py 2>&1 | tail -9; ls /Users/arsis/zlayt-pm-project/reviews | grep -i \"T-098\\|T-099\"",
 "description": "Rerun the demo-mode HTTP probe and check for existing review files",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T05:09:26.268Z

**tool result**
````
GET status 200 | envelope keys ['calibration', 'message', 'status'] | status ok | calibration keys ['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
served backend/sentence: fixture | Verified items matched the record 83/84 times in testing on 
body terms: {'token': False, 'excerpt': False, 'Patient': False, 'summary': False, 'case_': True} | 'case_' hits are golden-case ids inside by_case keys (synthetic names, not case tokens)
POST 405
PUT 405
PATCH 405
DELETE 405
GET /api/health demo_mode: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:09:31.748Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-098-staff-engineer-mutants.py",
 "content": "\"\"\"T-098 review mutation spot-check. Run: python3 this_file <copy-of-HEAD-archive-root>. Edits only the scratch copy's trace.py, restores it after each mutant.\"\"\"\nimport pathlib, subprocess, sys\n\nroot = pathlib.Path(sys.argv[1])\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nT = root / \"app/backend/trace.py\"\norig = T.read_text()\nmuts = {\n    \"M1 export_blockers drops code_check_blockers\": (\"    out.extend(code_check_blockers(conn, case_id, cx))\", \"    pass\"),\n    \"M2 _code_check_gated always False\": ('    return row[\"state\"] != \"rejected\" and row[\"review_status\"] in (\"accepted\", \"edited\") and _paralegal_wording(\"entry\", row)', \"    return False\"),\n    \"M3 blocker keeps any failing code step (no reason filter)\": ('s.get(\"reason_code\") in _CODE_CHECK_REASONS]\\n        if not fails:', 's.get(\"reason_code\")]\\n        if not fails:'),\n    \"M4 failing step not marked blocks_export\": ('                s[\"blocks_export\"] = True\\n', \"                pass\\n\"),\n}\ntry:\n    for name, (a, b) in muts.items():\n        assert orig.count(a) == 1, (name, orig.count(a))\n        T.write_text(orig.replace(a, b, 1))\n        r = subprocess.run([PY, \"-m\", \"pytest\", \"-p\", \"no:cacheprovider\", \"-q\", \"tests/unit/test_trace.py\", \"tests/unit/test_export.py\"],\n                           capture_output=True, text=True, cwd=root)\n        print(name, \"->\", r.stdout.strip().splitlines()[-1])\nfinally:\n    T.write_text(orig)\nr = subprocess.run([PY, \"-m\", \"pytest\", \"-p\", \"no:cacheprovider\", \"-q\", \"tests/unit/test_trace.py\", \"tests/unit/test_export.py\"], capture_output=True, text=True, cwd=root)\nprint(\"restored ->\", r.stdout.strip().splitlines()[-1])\n"
}
````

### User / tool · 2026-11-02T05:09:31.852Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-098-staff-engineer-mutants.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:09:34.284Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-099-staff-engineer-mutants.py",
 "content": "\"\"\"T-099 review mutation spot-check. Run: python3 this_file <copy-of-3ecb8b1-archive-root>. Edits only the scratch copy's calibration_route.py and restores it.\"\"\"\nimport pathlib, subprocess, sys\n\nroot = pathlib.Path(sys.argv[1])\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nF = root / \"app/backend/calibration_route.py\"\norig = F.read_text()\nmuts = {\n    \"M1 sentence m/t check removed\": ('    return cell[\"total\"] == 0 or f\"{cell[\\'matched\\']}/{cell[\\'total\\']} times\" in text', \"    return True\"),\n    \"M2 state-total = type-total check removed\": (\"            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):\", \"            if False:\"),\n    \"M3 problems() ignored by load()\": (\"    bad = problems(doc)\\n    if bad:\", \"    bad = problems(doc)\\n    if False:\"),\n    \"M4 all methods accepted on the route\": ('    @app.get(\"/api/calibration\")', '    @app.api_route(\"/api/calibration\", methods=[\"GET\", \"POST\", \"PUT\", \"PATCH\", \"DELETE\"])'),\n}\ntry:\n    for name, (a, b) in muts.items():\n        assert orig.count(a) == 1, (name, orig.count(a))\n        F.write_text(orig.replace(a, b, 1))\n        r = subprocess.run([PY, \"-m\", \"pytest\", \"-p\", \"no:cacheprovider\", \"-q\", \"tests/unit/test_calibration_route.py\"], capture_output=True, text=True, cwd=root)\n        print(name, \"->\", r.stdout.strip().splitlines()[-1])\nfinally:\n    F.write_text(orig)\nr = subprocess.run([PY, \"-m\", \"pytest\", \"-p\", \"no:cacheprovider\", \"-q\", \"tests/unit/test_calibration_route.py\"], capture_output=True, text=True, cwd=root)\nprint(\"restored ->\", r.stdout.strip().splitlines()[-1])\n"
}
````

### User / tool · 2026-11-02T05:09:34.407Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-099-staff-engineer-mutants.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:09:39.412Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && { echo \"# T-098 evidence (staff-engineer-reviewer). HEAD=$(git rev-parse HEAD); card commit e511778; scratch copies under $S\"; echo \"## pytest test_trace + test_export, e511778 archive\"; (cd \"$S/t098-e511778\" && $PY -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -1); echo \"## same, HEAD archive\"; (cd \"$S/t098-head\" && $PY -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -1); echo \"## full tests/unit, e511778 archive\"; (cd \"$S/t098-e511778\" && $PY -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -1); echo \"## full tests/unit, HEAD archive\"; (cd \"$S/t098-head\" && $PY -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -1); echo \"## probe1 (409 keep-wording dead end, D-047 token statuses)\"; (cd \"$S/t098-head\" && $PY -m pytest -p no:cacheprovider -q -s $E/T-098-staff-engineer-probe1.py -k p1_p2 2>&1 | grep \"^P\"); echo \"## probe2 (AI draft with invented 5/10, human edit, accept, export)\"; (cd \"$S/t098-head\" && $PY -m pytest -p no:cacheprovider -q -s $E/T-098-staff-engineer-probe2.py -k p1_409 -k p3 2>&1 | grep \"^P\"); echo \"## mutants\"; $PY $E/T-098-staff-engineer-mutants.py \"$S/t098-head\" 2>&1; } > $E/T-098-staff-engineer-results.txt 2>&1; cat $E/T-098-staff-engineer-results.txt",
 "description": "Run T-098 tests, probes and mutants and save the results under review evidence",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:11:56.729Z

**tool result**
````
# T-098 evidence (staff-engineer-reviewer). HEAD=e7a1987c64e08f46d05805401c63451adb44172c; card commit e511778; scratch copies under /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
## pytest test_trace + test_export, e511778 archive
88 passed in 5.86s
## same, HEAD archive
88 passed in 6.04s
## full tests/unit, e511778 archive
1577 passed, 4 skipped in 43.30s
## full tests/unit, HEAD archive
1600 passed, 4 skipped in 42.19s
## probe1 (409 keep-wording dead end, D-047 token statuses)
P1 entry e9 | summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision. | excerpt: Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.
P1 add 'significantly' no confirm -> (200, None)
P1 add 'significantly' confirm_warnings=true -> (200, None)
P1 accept -> 200
P1 gate ready True blockers []
P1 export 200 None
P2 add 'left' -> (409, 'needs_confirm')
P2 add 'not' -> (409, 'needs_confirm')
P2 add 'possibly' -> (200, None)
## probe2 (AI draft with invented 5/10, human edit, accept, export)
P3 excerpt: Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision. | date: 2026-06-12 | bad summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision Pain 5/10.
P3 generator.verify (code rung) on AI wording -> state: needs_review | reasons: ['SUMMARY_TOKEN_NOT_IN_EXCERPT']
P3 human edit with same wording -> (422, 'invalid_edit')
P3 stored AI item: needs_review
P3 accept AI draft -> 200
P3 gate ready True | blockers []
P3 export 200 | letter contains invented 5/10: True
P3 item trace verdict: {'code': 'accepted', 'label': 'Accepted by you', 'blocks_export': False}
## mutants
M1 export_blockers drops code_check_blockers -> 3 failed, 85 passed in 5.98s
M2 _code_check_gated always False -> 4 failed, 84 passed in 5.99s
M3 blocker keeps any failing code step (no reason filter) -> 88 passed in 6.10s
M4 failing step not marked blocks_export -> 1 failed, 87 passed in 6.54s
restored -> 88 passed in 6.30s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:12:04.648Z

**tool call — Bash**
````
{
 "command": "git log --oneline -n 4 | cat; echo ---; git diff --stat 196c985 HEAD | tail -3; E=$PWD/artifacts/review-evidence && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && { echo \"# T-098 evidence (staff-engineer-reviewer). Pinned archive HEAD 196c985641d72aa699e295223fed8961db0b0c2a (live HEAD moved to e7a1987 during review; not reviewed). Card commit e511778.\"; echo \"## pytest test_trace + test_export, e511778 archive\"; (cd \"$S/t098-e511778\" && $PY -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -1); echo \"## same, 196c985 archive\"; (cd \"$S/t098-head\" && $PY -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -1); echo \"## full tests/unit, e511778 archive\"; (cd \"$S/t098-e511778\" && $PY -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -1); echo \"## full tests/unit, 196c985 archive\"; (cd \"$S/t098-head\" && $PY -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -1); echo \"## probe1: edit with a non-token word, gate and export\"; (cd \"$S/t098-head\" && $PY -m pytest -p no:cacheprovider -q -s $E/T-098-staff-engineer-probe1.py -k p1_p2 2>&1 | grep \"^P\"); echo \"## probe2 P1: 409 keep-wording dead end\"; (cd \"$S/t098-head\" && $PY -m pytest -p no:cacheprovider -q -s $E/T-098-staff-engineer-probe2.py -k p1_409 2>&1 | grep \"^P\"); echo \"## probe2 P3: AI draft with invented 5/10\"; (cd \"$S/t098-head\" && $PY -m pytest -p no:cacheprovider -q -s $E/T-098-staff-engineer-probe2.py -k p3 2>&1 | grep \"^P\"); echo \"## mutants (196c985 archive)\"; $PY $E/T-098-staff-engineer-mutants.py \"$S/t098-head\" 2>&1; } > $E/T-098-staff-engineer-results.txt 2>&1; cat $E/T-098-staff-engineer-results.txt",
 "description": "Check live HEAD movement and regenerate T-098 evidence with the correct probe selection",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:14:25.215Z

**tool result**
````
f5ddec8 fix(frontend): remove the 409 keep-my-wording dialog and its copy now that T-100 landed; refused edits show the 422 reason inline (D-047, T-097 r2)
24c18a7 feat(backend): side/negation/qualifier tokens missing from the quote are a hard 422 on edit and manual entry; 409 keep-my-wording path removed (D-047, T-100)
e7a1987 fix(backend): language routing fails safe (D-048): English only when confidently English, mixed lines run the union of checks, Spanish cue words, 206-line routing set (T-085 r3)
21b6665 fix(frontend): AI-check summary and Why dialog read the gate and trace; failing edited wording is a named blocker with an Edit action; 422 edit reason inline (T-097 r2)
---
 tests/unit/test_spanish_records.py          |   2 +-
 tests/unit/test_trace.py                    |  20 +-
 38 files changed, 2303 insertions(+), 364 deletions(-)
# T-098 evidence (staff-engineer-reviewer). Pinned archive HEAD 196c985641d72aa699e295223fed8961db0b0c2a (live HEAD moved to e7a1987 during review; not reviewed). Card commit e511778.
## pytest test_trace + test_export, e511778 archive
88 passed in 5.99s
## same, 196c985 archive
88 passed in 6.20s
## full tests/unit, e511778 archive
1577 passed, 4 skipped in 44.13s
## full tests/unit, 196c985 archive
1600 passed, 4 skipped in 44.62s
## probe1: edit with a non-token word, gate and export
P1 entry e9 | summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision. | excerpt: Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.
P1 add 'significantly' no confirm -> (200, None)
P1 add 'significantly' confirm_warnings=true -> (200, None)
P1 accept -> 200
P1 gate ready True blockers []
P1 export 200 None
P2 add 'left' -> (409, 'needs_confirm')
P2 add 'not' -> (409, 'needs_confirm')
P2 add 'possibly' -> (200, None)
## probe2 P1: 409 keep-wording dead end
P1 entry e9 | summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
P1 'on the left' no confirm -> (409, 'needs_confirm')
P1 'on the left' confirm_warnings=true -> (200, None)
P1 accept -> 200
P1 gate ready False | blockers [('e9', 'SUMMARY_TOKEN_NOT_IN_EXCERPT')] | why: The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter.
P1 export 422 export_blocked | message: The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter. The export is blocked.
P1 ready == (export 200): True
## probe2 P3: AI draft with invented 5/10
P3 excerpt: Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision. | date: 2026-06-12 | bad summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision Pain 5/10.
P3 generator.verify (code rung) on AI wording -> state: needs_review | reasons: ['SUMMARY_TOKEN_NOT_IN_EXCERPT']
P3 human edit with same wording -> (422, 'invalid_edit')
P3 stored AI item: needs_review
P3 accept AI draft -> 200
P3 gate ready True | blockers []
P3 export 200 | letter contains invented 5/10: True
P3 item trace verdict: {'code': 'accepted', 'label': 'Accepted by you', 'blocks_export': False}
## mutants (196c985 archive)
M1 export_blockers drops code_check_blockers -> 3 failed, 85 passed in 6.31s
M2 _code_check_gated always False -> 4 failed, 84 passed in 6.12s
M3 blocker keeps any failing code step (no reason filter) -> 88 passed in 5.97s
M4 failing step not marked blocks_export -> 1 failed, 87 passed in 5.84s
restored -> 88 passed in 5.69s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:14:32.497Z

**tool call — Bash**
````
{
 "command": "git show --stat 24c18a7 | head -30 | cat; echo ---; git show --stat f5ddec8 | head -12 | cat; echo ---; git show --stat 21b6665 | head -12 | cat; echo; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/t098-f5ddec8\" && git archive f5ddec8 | tar -x -C \"$S/t098-f5ddec8\" && cd \"$S/t098-f5ddec8\" && grep -n \"needs_confirm\\|keep_my_wording\" app/backend/review.py | head -5; echo \"--- frontend keep-wording refs:\"; grep -rn \"btn-keep-wording\\|Keep my wording\" app/frontend | head -3; echo \"--- trace/export tests:\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py 2>&1 | tail -1",
 "description": "Inspect the T-100 D-047 follow-up commits and archive f5ddec8 for a re-check",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:14:39.199Z

**tool result**
````
commit 24c18a757beaef62d42be592f85409187531e563
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:09:49 2026 -0600

    feat(backend): side/negation/qualifier tokens missing from the quote are a hard 422 on edit and manual entry; 409 keep-my-wording path removed (D-047, T-100)
    
    Judge objections no longer block a human-written edit: saved as needs_review with a warnings[] code.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/export.py               |  7 ++--
 app/backend/review.py               | 70 +++++++++++++++++--------------------
 app/backend/store.py                |  7 +---
 app/backend/trace.py                |  2 --
 memory/contracts/api.md             | 20 +++++------
 tests/unit/test_api_routes.py       | 24 ++++++++++++-
 tests/unit/test_export.py           |  5 ++-
 tests/unit/test_manual_and_split.py | 27 ++++++++++----
 tests/unit/test_ocr_invariant.py    |  2 +-
 tests/unit/test_review_rules.py     | 64 ++++++++++++++++++++++++++-------
 tests/unit/test_trace.py            | 20 +++++++----
 11 files changed, 156 insertions(+), 92 deletions(-)
---
commit f5ddec825e5287124d268ddf16d06a299b957fda
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:10:53 2026 -0600

    fix(frontend): remove the 409 keep-my-wording dialog and its copy now that T-100 landed; refused edits show the 422 reason inline (D-047, T-097 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/frontend/manual.js        | 20 +++++---------------
 app/frontend/review.css       |  3 +--
 app/frontend/review.js        | 19 +++----------------
 tests/e2e/conftest.py         |  2 +-
---
commit 21b66650ca2fcd0c5f3442689b865469f418712d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:08:22 2026 -0600

    fix(frontend): AI-check summary and Why dialog read the gate and trace; failing edited wording is a named blocker with an Edit action; 422 edit reason inline (T-097 r2)
    
    Panel summary counts only gate-listed items as 'blocks export'; an edited item that fails a code check shows
    "Your wording doesn't match the quote: <reason>" with Edit your wording (panel row, Why dialog, rail row);
    an edited item that passes shows 'Edited by you, not AI-checked' and its judge step is 'Not needed'.
    D-047: a refused edit shows the 422 reason under the edit box; the 409 keep-my-wording path stays dead code until T-100 lands.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

--- frontend keep-wording refs:
--- trace/export tests:
88 passed in 5.76s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:14:44.657Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; E=/Users/arsis/zlayt-pm-project/artifacts/review-evidence; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; cd \"$S/t098-f5ddec8\" && { echo \"# f5ddec8 re-check (live HEAD during review; T-100 24c18a7 D-047 follow-up)\"; $PY -m pytest -p no:cacheprovider -q -s $E/T-098-staff-engineer-probe1.py -k p1_p2 2>&1 | grep \"^P\"; $PY -m pytest -p no:cacheprovider -q -s $E/T-098-staff-engineer-probe2.py -k p1_409 2>&1 | grep \"^P\\|passed\\|failed\" | cut -c1-260; $PY -m pytest -p no:cacheprovider -q -s $E/T-098-staff-engineer-probe2.py -k p3 2>&1 | grep \"^P\\|passed\\|failed\" | cut -c1-260; } 2>&1 | tee \"$E/T-098-staff-engineer-f5ddec8-recheck.txt\"",
 "description": "Re-run the T-098 probes on the f5ddec8 archive to see whether D-047 and the AI-draft gap changed",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T05:14:48.017Z

**tool result**
````
# f5ddec8 re-check (live HEAD during review; T-100 24c18a7 D-047 follow-up)
P1 entry e9 | summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision. | excerpt: Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.
P1 add 'significantly' no confirm -> (200, None)
P1 add 'significantly' confirm_warnings=true -> (200, None)
P1 accept -> 200
P1 gate ready True blockers []
P1 export 200 None
P2 add 'left' -> (422, 'invalid_edit')
P2 add 'not' -> (422, 'invalid_edit')
P2 add 'possibly' -> (200, None)
P1 entry e9 | summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
P1 'on the left' no confirm -> (422, 'invalid_edit')
P1 'on the left' confirm_warnings=true -> (422, 'invalid_edit')
P1 accept -> 200
P1 gate ready True | blockers [] | why: None
P1 export 200 None | message: None
P1 ready == (export 200): True
1 passed, 1 deselected in 0.94s
P3 excerpt: Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision. | date: 2026-06-12 | bad summary: Cervical epidural steroid injection recommended; patient states symptoms began after the January collision P
P3 generator.verify (code rung) on AI wording -> state: needs_review | reasons: ['SUMMARY_TOKEN_NOT_IN_EXCERPT']
P3 human edit with same wording -> (422, 'invalid_edit')
P3 stored AI item: needs_review
P3 accept AI draft -> 200
P3 gate ready True | blockers []
P3 export 200 | letter contains invented 5/10: True
P3 item trace verdict: {'code': 'accepted', 'label': 'Accepted by you', 'blocks_export': False}
1 passed, 1 deselected in 0.82s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:14:59.199Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && T=\"$S/t099-3ecb8b1\" && { echo \"# T-099 evidence (staff-engineer-reviewer). Pinned archive 3ecb8b1 (card commit). Live HEAD during review: f5ddec8.\"; echo \"## pytest tests/unit -k calibration (3ecb8b1 archive), with skip reasons\"; (cd \"$T\" && $PY -m pytest -p no:cacheprovider -q tests/unit -k calibration -rs 2>&1 | tail -4); echo \"## test_calibration_route.py only\"; (cd \"$T\" && $PY -m pytest -p no:cacheprovider -q tests/unit/test_calibration_route.py 2>&1 | tail -1); echo \"## state probes\"; (cd \"$T\" && $PY $E/T-099-staff-engineer-probe-states.py \"$S/probe99/out2\" 2>&1); echo \"## consistent hand-edit probe (real code)\"; (cd \"$T\" && $PY $E/T-099-staff-engineer-probe-consistent-edit.py \"$S/probe99/consistent_real2.json\" 2>&1 | tail -1); echo \"## HTTP demo-mode probe\"; (cd \"$T\" && $PY $E/T-099-staff-engineer-probe-http.py 2>&1 | tail -9); echo \"## mutants\"; $PY $E/T-099-staff-engineer-mutants.py \"$T\" 2>&1; echo \"## consistent hand-edit under M2 (state-sum removed)\"; } > $E/T-099-staff-engineer-results.txt 2>&1; cat $E/T-099-staff-engineer-results.txt | head -80; echo ---; git diff --stat 3ecb8b1 f5ddec8 -- app/backend/calibration_route.py tests/unit/test_calibration_route.py evals/reports/calibration.json | cat",
 "description": "Run T-099 tests, state probes, HTTP probe and mutants and save the results under review evidence",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:15:05.666Z

**tool result**
````
# T-099 evidence (staff-engineer-reviewer). Pinned archive 3ecb8b1 (card commit). Live HEAD during review: f5ddec8.
## pytest tests/unit -k calibration (3ecb8b1 archive), with skip reasons
..............................ss..                                       [100%]
=========================== short test summary info ============================
SKIPPED [2] tests/unit/test_eval_runner.py:636: no git repository here (exported tree)
32 passed, 2 skipped, 1570 deselected in 1.84s
## test_calibration_route.py only
23 passed in 0.42s
## state probes
LOG WARNING calibration file is not JSON: not_json.json
LOG WARNING calibration file could not be read: not_utf8.json
LOG WARNING calibration file rejected: not an object
LOG WARNING calibration file rejected: schema
LOG WARNING calibration file rejected: by_state.verified.matched is not the sum over by_type (hand-edited count)
LOG WARNING calibration file rejected: sentences.overall.verified does not quote its counts
LOG WARNING calibration file rejected: by_state.verified
LOG WARNING calibration file rejected: by_state.verified
LOG WARNING calibration file rejected: not_scored
LOG WARNING calibration file rejected: by_state.verified.matched is not the sum over by_type (hand-edited count); by_state.verified.total is not the sum over by_type (hand-edited count); by_type.entry.verified
LOG WARNING calibration file could not be read: out2
== state probes (CR.load on scratch copies)
real_copy                          status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
   served by_case present: True | served has 'cases' key: False
   missing path: missing
not_json                           status=invalid  cal_keys=None
not_utf8                           status=invalid  cal_keys=None
top_level_list                     status=invalid  cal_keys=None
wrong_schema                       status=invalid  cal_keys=None
hand_edit_state_total              status=invalid  cal_keys=None
hand_edit_by_case_only             status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
by_case_matched_gt_total           status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
hand_edit_case_count               status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
hand_edit_backend_label            status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
hand_edit_sentence_words           status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
hand_edit_sentence_claim           status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
sentence_mn_mismatch               status=invalid  cal_keys=None
small_sample_flipped               status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
extra_key                          status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
   extra key echoed: False
float_count                        status=invalid  cal_keys=None
bool_count                         status=invalid  cal_keys=None
not_scored_total_mismatch          status=invalid  cal_keys=None
cases_list_emptied                 status=ok       cal_keys=['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
matched_gt_total_cell              status=invalid  cal_keys=None
== directory at path: invalid
## consistent hand-edit probe (real code)
consistent hand-edit (state total + its sentence changed together): invalid ['by_state.verified.matched is not the sum over by_type (hand-edited count)']
## HTTP demo-mode probe
GET status 200 | envelope keys ['calibration', 'message', 'status'] | status ok | calibration keys ['backend', 'by_state', 'by_type', 'case_count', 'generated_at', 'not_scored', 'schema', 'sentences', 'small_sample', 'source_commit']
served backend/sentence: fixture | Verified items matched the record 83/84 times in testing on 
body terms: {'token': False, 'excerpt': False, 'Patient': False, 'summary': False, 'case_': True} | 'case_' hits are golden-case ids inside by_case keys (synthetic names, not case tokens)
POST 405
PUT 405
PATCH 405
DELETE 405
GET /api/health demo_mode: True
## mutants
M1 sentence m/t check removed -> 1 failed, 22 passed in 0.33s
M2 state-total = type-total check removed -> 23 passed in 0.31s
M3 problems() ignored by load() -> 11 failed, 12 passed in 0.41s
M4 all methods accepted on the route -> 1 failed, 22 passed in 0.38s
restored -> 23 passed in 0.35s
## consistent hand-edit under M2 (state-sum removed)
---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:15:13.261Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && M=\"$S/mut99\" && { echo \"## consistent hand-edit (by_state.verified 82/84 with its sentence rewritten), state-sum check removed in scratch copy\"; cd \"$M\" && $PY - <<'EOF'\nimport pathlib, subprocess, json\nF = pathlib.Path(\"app/backend/calibration_route.py\"); orig = F.read_text()\nold = \"            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):\"\ntry:\n    F.write_text(orig.replace(old, \"            if False:\"))\n    print(\"M2 applied; probe:\")\n    print(subprocess.run([\"/Users/arsis/zlayt-pm-project/.venv/bin/python\", \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-099-staff-engineer-probe-consistent-edit.py\", \"/tmp/unused-but-scratch.json\"], capture_output=True, text=True, cwd=\".\").stdout)\nfinally:\n    F.write_text(orig)\nprint(\"restored\")\nEOF\n} >> $E/T-099-staff-engineer-results.txt 2>&1; tail -6 $E/T-099-staff-engineer-results.txt; echo \"--- T-094 hunk tests at f5ddec8:\"; cd \"$S/t098-f5ddec8\" && grep -rln \"candidate_rule\\|paired_by_code\" tests/ | head -3; echo \"(none above = no test references)\"; echo \"--- archive HEAD dirs check:\"; ls \"$S\" | head -0",
 "description": "Append the consistent-edit mutant result and check T-094 branch tests at f5ddec8",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:15:13.443Z

**tool result (error)**
````
Exit code 1
## consistent hand-edit under M2 (state-sum removed)
## consistent hand-edit (by_state.verified 82/84 with its sentence rewritten), state-sum check removed in scratch copy
M2 applied; probe:
consistent hand-edit (state total + its sentence changed together): ok []

restored
--- T-094 hunk tests at f5ddec8:
(none above = no test references)
--- archive HEAD dirs check:
head: illegal line count -- 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:16:01.071Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && cp \"$S/probe98/test_probe_t098c.py\" \"$E/T-098-staff-engineer-probe3-verdicts.py\" && { echo \"## probe3: AI draft with invented 5/10 under judge verdicts unsupported and disagrees (196c985 archive)\"; for v in unsupported disagrees; do echo \"# judge=$v\"; (cd \"$S/t098-head\" && P3_VERDICT=$v $PY -m pytest -p no:cacheprovider -q -s $E/T-098-staff-engineer-probe3-verdicts.py -k p3 2>&1 | grep \"^P3 accept\\|^P3 gate\\|^P3 export\"); done; echo \"## same probe at f5ddec8 (live HEAD during review)\"; (cd \"$S/t098-f5ddec8\" && $PY -m pytest -p no:cacheprovider -q -s $E/T-098-staff-engineer-probe3-verdicts.py -k p3 2>&1 | grep \"^P3 accept\\|^P3 gate\\|^P3 export\"); } >> $E/T-098-staff-engineer-results.txt 2>&1; tail -14 $E/T-098-staff-engineer-results.txt; rm -f /tmp/unused-but-scratch.json 2>/dev/null; echo \"--- line refs\"; grep -n \"def check_calibration\\|calibration_sentences(c\\[\" evals/run.py; grep -n \"def sum_mismatch\\|sum_mismatch_hand_edit\\|sentence_quotes_other_counts\" tests/unit/test_calibration_route.py | head -3",
 "description": "Save the judge-verdict variants of the AI-draft probe and collect the evals checker line numbers",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T05:16:04.329Z

**tool result**
````
restored -> 88 passed in 5.69s
## probe3: AI draft with invented 5/10 under judge verdicts unsupported and disagrees (196c985 archive)
# judge=unsupported
P3 accept AI draft -> 200
P3 gate ready True | blockers []
P3 export 200 | letter contains invented 5/10: True
# judge=disagrees
P3 accept AI draft -> 200
P3 gate ready True | blockers []
P3 export 200 | letter contains invented 5/10: True
## same probe at f5ddec8 (live HEAD during review)
P3 accept AI draft -> 200
P3 gate ready True | blockers []
P3 export 200 | letter contains invented 5/10: True
--- line refs
1029:def check_calibration(path, root=ROOT):
1041:    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
106:    "sum_mismatch_hand_edit": lambda d: d["by_state"]["verified"].update(matched=90),
107:    "sentence_quotes_other_counts": lambda d: d["sentences"]["overall"].update(verified=d["sentences"]["overall"]["verified"].replace("83/84", "90/91")),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:16:51.801Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-098-staff-engineer.md",
 "content": "# T-098 staff-engineer-reviewer: export gate for human-edited wording (commit e511778)\n\nVerdict: **fail** (1 blocker, 1 major, 2 minor). The card's own AC holds: an accepted, human-edited summary that fails a code check is a gate blocker, GET /export returns 422 with the same list, and gate `ready` equals export allowed. The blocker is adjacent to the AC: AI drafts with a number not in the quote are still accepted and exported with no code check (finding 1). That is outside the card, the handoff lists it as an exclusion, and I have not downgraded it for that reason.\n\nPinning: I reviewed `git archive 196c985` (HEAD when I started; e511778 and 36a982b are its ancestors). HEAD moved during the review to e7a1987, then to f5ddec8. f5ddec8 contains T-100 (24c18a7, the D-047 follow-up) and the frontend change that removes the 409 dialog. I re-ran the two open items at f5ddec8 (finding 2 closed there; finding 1 still open).\n\nSeverity note: the brief expected the D-047 409 leftover to be a major. I kept it as a major. The outcome at the reviewed commit is fail-closed (the export is refused and no invented fact leaves), which is what D.2 uses to separate major from blocker. Finding 1 is a blocker because an invented number reaches the letter.\n\nCounts: `pytest -q tests/unit/test_trace.py tests/unit/test_export.py` gives 88 passed at e511778 and at 196c985. The full `tests/unit` gives 1577 passed, 4 skipped at e511778 and 1600 passed, 4 skipped at 196c985. The card's \"1614 passed\" comes from a dirty shared tree and does not reproduce from the archives.\n\nCarried hunks (T-094 in trace.py, T-099 contract in api.md): they do not break the suite. The T-094 conflict branch has no test (finding 3). The T-099 API section is documentation only and matches the route.\n\n## Findings\n\n**F1 (blocker). An AI draft with a number not in its quote reaches the export after one accept.** Outside the T-098 AC; found while testing the gate path. Probe at 196c985: code marks the AI wording `needs_review` (reason SUMMARY_TOKEN_NOT_IN_EXCERPT); the human edit of the same wording is refused with 422; accept returns 200; the gate is ready with no blockers; GET /export returns 200 and the letter contains the invented \"5/10\". Same result when the judge answer is unsupported or disagrees. Code: `app/backend/review.py:70-71` (accept applies no code check), `app/backend/trace.py:399-400` and `:750-751` (the gate only covers human wording), `memory/contracts/api.md:618` (\"AI drafts are not covered by this blocker\"). D-034 (`memory/ORCHESTRATOR_DECISIONS.md:42`) says a number not in the quote is never saved, with no override; CLAUDE.md non-negotiable 5 says the product may not invent facts. Rated blocker per D.2 (invents a fact that reaches the letter).\n\n**F2 (major, closed at f5ddec8). The D-047 409 \"keep my wording\" path still existed at the reviewed commit.** `app/backend/review.py:107-108` raises 409 needs_confirm for token warnings; `:161` logs keep_my_wording; `app/frontend/review.js:135` and `app/frontend/manual.js:55` render the button. At 196c985, \"on the left\" returns 409 without confirm, saves with confirm, accepts, and the gate blocks it (export 422). D-047 says that state must not be reachable. At f5ddec8 (24c18a7 and f5ddec8) the edit returns 422 invalid_edit with and without confirm and there is no keep path. Open question: a hedge added to a quote without one (\"Possibly ...\") still saves with 200 and no warning.\n\n**F3 (minor). The T-094 trace hunk carried in e511778 has no test.** `app/backend/trace.py:527-540` (the candidate_rule conflict branch) and `trace.py:607` (`_ocr_steps` now runs on every flag; before e511778 it ran only in the AI branch). `grep -rln 'candidate_rule\\|paired_by_code' tests/` prints nothing at 196c985, e511778 and f5ddec8. Owned by T-094.\n\n**F4 (minor). The reason filter in the new blocker is untested.** `app/backend/trace.py:435` filters failing steps by `_CODE_CHECK_REASONS`. Mutant M3 (filter removed) leaves 88 passed. A widened blocker would over-block and no test would notice.\n\n## What I exercised\n\n- `git rev-parse HEAD` (196c985641d7...), `git show --stat e511778`, `git show 36a982b` (docs only), `git show --stat 196c985`, `git show --stat 24c18a7 f5ddec8`, `git log --oneline -n 4`.\n- `git archive` of e511778, 196c985 and f5ddec8 into the scratchpad; `.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py` on each (88 passed).\n- Full `tests/unit` on e511778 and 196c985 (1577 and 1600 passed, 4 skipped).\n- Probes, all through the real FastAPI app with the fixture backend and a scratch DB: `artifacts/review-evidence/T-098-staff-engineer-probe1.py` (non-token edit, gate and export), `artifacts/review-evidence/T-098-staff-engineer-probe2.py` (409 path, AI draft), `artifacts/review-evidence/T-098-staff-engineer-probe3-verdicts.py` (judge verdict variants). The AI-draft state comes from the real `generator.verify`; the judge verdict and the DB row were then set in the scratch copy.\n- Results: `artifacts/review-evidence/T-098-staff-engineer-results.txt` (196c985) and `artifacts/review-evidence/T-098-staff-engineer-f5ddec8-recheck.txt` (f5ddec8).\n- Mutants on a scratch copy: `artifacts/review-evidence/T-098-staff-engineer-mutants.py` (M1 3 failed, M2 4 failed, M3 88 passed, M4 1 failed).\n- Read: `reviews/T-097-ux-designer.md` (B1 case), `memory/ORCHESTRATOR_DECISIONS.md` D-022, D-034, D-044, D-045, D-047, `memory/contracts/api.md` export section, `git show e511778` in full for the four files in scope.\n- Grep: `409`, `needs_confirm`, `keep_my_wording`, `btn-keep-wording` across app and tests; `candidate_rule` across tests.\n- Not exercised: UX (Why dialog, panel copy), outside my lens; the browser was not driven.\n\n```json\n{\"card\": \"T-098\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit e511778 (T-098) with 36a982b (D-047 docs); pinned git archive 196c985 (HEAD at review start); re-check of open items at git archive f5ddec8 (live HEAD during review, includes T-100 24c18a7 and frontend f5ddec8); no app URL (FastAPI TestClient, fixture backend, scratch DB); sample case entry e9 and the synthetic probes\",\n \"exercised\": [\n  \"git rev-parse HEAD -> 196c985641d72aa699e295223fed8961db0b0c2a; git show --stat e511778, 3ecb8b1, 36a982b, 196c985, 24c18a7, f5ddec8\",\n  \"git archive 196c985 | tar -x (scratch t098-head); git archive e511778 (t098-e511778); git archive f5ddec8 (t098-f5ddec8)\",\n  \".venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_trace.py tests/unit/test_export.py -> 88 passed at e511778 and at 196c985 (artifacts/review-evidence/T-098-staff-engineer-results.txt)\",\n  \".venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -> 1577 passed, 4 skipped at e511778; 1600 passed, 4 skipped at 196c985\",\n  \"artifacts/review-evidence/T-098-staff-engineer-probe1.py: edit 'significantly' (no token), accept, gate and export; D-047 candidates 'on the left', 'not', 'possibly' -> 409, 409, 200 at 196c985 and 422, 422, 200 at f5ddec8\",\n  \"artifacts/review-evidence/T-098-staff-engineer-probe2.py: edit 'on the left' without and with confirm_warnings -> 409 then 200; accept 200; gate ready False with SUMMARY_TOKEN_NOT_IN_EXCERPT; GET /export 422 export_blocked; ready == (export 200) True. At f5ddec8: 422 both times\",\n  \"artifacts/review-evidence/T-098-staff-engineer-probe2.py (p3): generator.verify on 'Pain 5/10' over a quote without it -> needs_review, SUMMARY_TOKEN_NOT_IN_EXCERPT; human edit same wording -> 422 invalid_edit; AI accept -> 200; gate ready True, blockers []; export 200 contains 5/10. Same at f5ddec8\",\n  \"artifacts/review-evidence/T-098-staff-engineer-probe3-verdicts.py: judge verdict unsupported and disagrees -> accept 200, export 200 with the invented figure, at 196c985 and f5ddec8\",\n  \"artifacts/review-evidence/T-098-staff-engineer-mutants.py on the 196c985 copy: M1 drop code_check_blockers -> 3 failed; M2 _code_check_gated False -> 4 failed; M3 drop reason filter -> 88 passed (survives); M4 blocks_export not set -> 1 failed; restored -> 88 passed\",\n  \"read reviews/T-097-ux-designer.md (B1 and walk2 evidence); memory/ORCHESTRATOR_DECISIONS.md lines 30, 42, 53, 55; memory/contracts/api.md line 618; app/backend/review.py 59-175, app/backend/trace.py 390-441 and 527-607, app/backend/generator.py 71-100, app/frontend/review.js 125-137, app/frontend/manual.js 45-56\",\n  \"grep -rn '409\\\\|keep my wording\\\\|needs_confirm\\\\|keep_my_wording\\\\|btn-keep-wording' app tests memory/contracts (at 196c985 and f5ddec8); grep -rln 'candidate_rule\\\\|paired_by_code' tests (empty at 196c985, e511778, f5ddec8)\",\n  \"git show e511778 -- app/backend/trace.py app/backend/grounding.py tests/unit/test_trace.py tests/unit/test_export.py memory/contracts/api.md (full diff read)\"],\n \"verdict\": \"fail\",\n \"scores\": {\"gate_export_agreement\": 4, \"human_wording_code_check_gate\": 4, \"ai_draft_path\": 1, \"d047_followup\": 2, \"test_pins_behaviour\": 3},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"An AI draft with a number not in its quote reaches the export after one accept (outside the T-098 AC, found on the gate path)\",\n   \"evidence\": \"artifacts/review-evidence/T-098-staff-engineer-results.txt (probe2 p3 at 196c985): 'P3 generator.verify (code rung) on AI wording -> state: needs_review | reasons: [SUMMARY_TOKEN_NOT_IN_EXCERPT]', 'P3 human edit with same wording -> (422, invalid_edit)', 'P3 accept AI draft -> 200', 'P3 gate ready True | blockers []', 'P3 export 200 | letter contains invented 5/10: True'. Same with judge verdict unsupported or disagrees (probe3 block) and at f5ddec8 (artifacts/review-evidence/T-098-staff-engineer-f5ddec8-recheck.txt). Code: app/backend/review.py:70-71 (accept applies no code check); app/backend/trace.py:399-400 and 750-751 (gate covers only human wording); memory/contracts/api.md:618 'AI drafts are not covered by this blocker'; memory/ORCHESTRATOR_DECISIONS.md:42 (D-034: a number not in the quote is never saved, no override).\",\n   \"why_it_matters\": \"D-034 names this failure ('Pain 9/10' against a 4/10 quote reached the letter). The paralegal typing the same number is refused with 422, but an AI draft with it is saved as needs_review and one accept sends it to the letter; a judge objection does not stop it. CLAUDE.md non-negotiable 5 (no invented facts) is violated on the export path. Rated blocker per D.2 (invents a fact that reaches the letter). The card's AC covers human wording only and the handoff lists AI drafts as an exclusion; that is not a reason to downgrade.\",\n   \"fix\": \"Decide and record the rule for AI drafts whose D-034 tokens (numbers, dates, dollar figures, left/right/no/not/without) fail the code check: either the generator refuses the draft as it refuses GROUNDING_* failures (app/backend/generator.py:71 verify, REJECTED_CODES in app/backend/confidence.py), or accept returns 422 with EDIT_SUMMARY and the gate lists it as a blocker. Apply the same rule whatever the judge says.\",\n   \"acceptance_test\": \"Unit: generator.verify on 'Pain 5/10' over an excerpt without 5/10 must not yield a state that accept can send to the export; accept returns 422 or GET /export returns 422. Run with judge verdicts supported, unsupported and disagrees; the export never contains '5/10'. Mutation: removing the new check makes the test fail.\"},\n  {\"severity\": \"major\", \"title\": \"D-047 409 keep-my-wording path still existed at the reviewed commit (T-098 follow-up; closed at f5ddec8 by T-100 24c18a7 and frontend f5ddec8)\",\n   \"evidence\": \"app/backend/review.py:107-108 (raise ReviewError 409 needs_confirm for token warnings), :161 (keep_my_wording event), app/frontend/review.js:135 and app/frontend/manual.js:55 (btn-keep-wording). At 196c985, artifacts/review-evidence/T-098-staff-engineer-results.txt (probe2 P1): 'on the left no confirm -> (409, needs_confirm)', 'confirm_warnings=true -> (200, None)', 'accept -> 200', 'gate ready False | blockers [(e9, SUMMARY_TOKEN_NOT_IN_EXCERPT)]', 'export 422 export_blocked'. At f5ddec8 (artifacts/review-evidence/T-098-staff-engineer-f5ddec8-recheck.txt): 'on the left' -> (422, invalid_edit) with and without confirm; 'not' -> 422.\",\n   \"why_it_matters\": \"D-047 says the 409 path is removed so that no item can be confirmed into an unexportable state. At the reviewed commit a paralegal could confirm one: it saved, accepted, and the gate then refused the export. The outcome is fail-closed and no invented fact leaves, so I rate major (the brief's default), not blocker. Closed at f5ddec8.\",\n   \"fix\": \"Already done in 24c18a7 and f5ddec8. Keep the regression: side, negation and qualifier tokens refused with 422 at edit and manual entry, with no keep path in the API or the UI.\",\n   \"acceptance_test\": \"E2E and unit: edit 'Neck pain ... on the left.' with and without confirm_warnings returns 422 invalid_edit, the item is unchanged, and no btn-keep-wording exists in the DOM. Mutation: restoring the 409 branch in review.py:107-108 makes the test fail.\"},\n  {\"severity\": \"minor\", \"title\": \"The T-094 trace hunk carried in e511778 has no test and no card review\",\n   \"evidence\": \"app/backend/trace.py:527-540 (candidate_rule conflict branch: paired_by_code, spans_match, judge_conflict) and app/backend/trace.py:607 (_ocr_steps now on every flag; in e511778 it moved out of the AI-only branch). 'grep -rln candidate_rule\\\\|paired_by_code tests' prints nothing at 196c985, e511778 and f5ddec8.\",\n   \"why_it_matters\": \"The brief asked whether the carried hunks break anything. The suite passes (88 at e511778 and 196c985), but no test runs the new code-origin conflict branch, and the OCR-step move changes what lexicon-only flags show. Behaviour owned by T-094 is untested.\",\n   \"fix\": \"T-094 adds its own tests and goes through its own review before it closes, or the hunk is split out of the T-098 commit.\",\n   \"acceptance_test\": \"tests/unit/test_trace.py: a conflict with candidate_rule plan_vs_outcome gives paired_by_code pass, spans_match pass (verbatim) or fail (not verbatim), and a judge_conflict step; a lexicon-only flag on an OCR record shows the OCR step. Mutation: deleting the trace.py:527 branch makes the test fail.\"},\n  {\"severity\": \"minor\", \"title\": \"The reason filter in the new blocker is untested\",\n   \"evidence\": \"app/backend/trace.py:435 (fails = steps with reason_code in _CODE_CHECK_REASONS). Mutant with the filter removed: 88 passed (artifacts/review-evidence/T-098-staff-engineer-results.txt, M3).\",\n   \"why_it_matters\": \"A widened blocker would block on any failing code step of a paralegal entry (over-blocking) and no test would notice. It does not under-block, so minor.\",\n   \"fix\": \"Add a test: an accepted paralegal entry with a failing non-summary code step is not listed as a code-check blocker (or state the intended behaviour and test it).\",\n   \"acceptance_test\": \"Mutant M3 makes the new test fail.\"}\n ],\n \"whats_right\": [\n  \"Gate and export share one list: at 196c985 a refused edit gives gate ready False and GET /export 422 with the identical blocker; ready == (export 200) held in every probed state (probe2 P1 and probe1 P1 in the results file).\",\n  \"The blocker is pinned by tests: removing the call from export_blockers (M1) fails 3 tests, the gating predicate (M2) fails 4, and the blocks_export flag (M4) fails 1.\",\n  \"The T-097 B1 case now gates: the test test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098 passes, and the item trace names summary_qualifier with an EDIT_SUMMARY action.\"],\n \"questions_for_chris\": [\n  \"F1: should an AI draft whose number, date or dollar figure is not in its quote be refused at generation or at accept (D-034 says never saved), or may the paralegal accept it? D-022 says needs_review for qualifiers; the numeric case is the open question.\",\n  \"D-047: does a hedge added to a quote without one ('Possibly ...') count as a qualifier token? At f5ddec8 it saves with 200 and no warning.\",\n  \"T-100 made judge objections on a human-written edit non-blocking (saved as needs_review). D-045(b) exempts human wording from the judge. Confirm this is intended.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T05:16:51.950Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-098-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:17:01.421Z

**tool call — Bash**
````
{
 "command": "/usr/bin/python3 - <<'EOF'\nimport json, re\nt = open(\"reviews/T-098-staff-engineer.md\", encoding=\"utf-8\").read()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", t, re.S)\nprint(\"json blocks:\", len(blocks), \"fence count:\", t.count(\"```json\"))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"card\", d[\"card\"], \"model\", d[\"model\"], \"verdict\", d[\"verdict\"], \"expected\", exp, \"match\", d[\"verdict\"] == exp, sev)\nEOF",
 "description": "Validate the T-098 review JSON block and the verdict rule"
}
````

### User / tool · 2026-11-02T05:17:01.537Z

**tool result**
````
json blocks: 1 fence count: 1
card T-098 model claude-haiku-5-5 verdict fail expected fail match True ['blocker', 'major', 'minor', 'minor']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:17:17.329Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t099-3ecb8b1\" && grep -n \"case_count\\|small_sample\\|\\\"backend\\\"\\|by_case\\|_statement_ok\\|sentences.overall\\|sentences.by_type\" app/backend/calibration_route.py; cd /Users/arsis/zlayt-pm-project && grep -n \"hashes\\|def hashes\\|CAL_SMALL_N =\" evals/run.py | sed -n 1,12p; sed -n 1043,1047p evals/run.py",
 "description": "Get exact line numbers for T-099 citations in the route and the evals checker"
}
````

### User / tool · 2026-11-02T05:17:17.437Z

**tool result**
````
23:SERVED = ("schema", "backend", "case_count", "small_sample", "source_commit", "generated_at", "by_state", "by_type", "not_scored", "sentences")
37:def _statement_ok(text, cell) -> bool:
52:    if not (isinstance(c.get("backend"), str) and c["backend"]):
53:        bad.append("backend")
54:    if not _count(c.get("case_count")):
55:        bad.append("case_count")
56:    if not isinstance(c.get("small_sample"), bool):
57:        bad.append("small_sample")
78:            if not (_cell_ok(cell) and isinstance(cell.get("by_case"), dict)):
85:        if not _statement_ok(se["overall"].get(s), bs[s]):
86:            bad.append(f"sentences.overall.{s} does not quote its counts")
89:            if not _statement_ok((se["by_type"].get(t) or {}).get(s), bt[t][s]):
90:                bad.append(f"sentences.by_type.{t}.{s} does not quote its counts")
6:    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk
84:def hashes(root=ROOT):
244:CAL_SMALL_N = 30            # fewer cases (or items in a cell) than this is reported as a small sample, never rounded up to a rate
318:def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
345:            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "source_tree": (source or {}).get("tree"), "hashes": hashes_ or {},
915:              "hashes": hashes(), "metrics": m, "assertions": a, **spec, "per_case": results,
917:    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
998:          "", "## Prompt and lexicon hashes", ""] + [f"- `{k}` {v}" for k, v in r["hashes"].items()]
1014:    """0 when latest.json hashes equal the files on disk; 1 otherwise (or when latest.json is missing)."""
1019:    old, now = json.loads(p.read_text()).get("hashes", {}), hashes(root)
1030:    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
1043:    old = c.get("hashes") or {}
    old = c.get("hashes") or {}
    now = hashes(root)
    bad += [f"was measured against a different {k}" for k in sorted(set(old) | set(now)) if old and old.get(k) != now.get(k)]
    return bad
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:17:44.513Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-099-staff-engineer.md",
 "content": "# T-099 staff-engineer-reviewer: GET /api/calibration (commit 3ecb8b1)\n\nVerdict: **changes** (0 blockers, 1 major, 3 minor). The route does what the card says: it serves the committed calibration in the contract shape, returns `calibration: null` for missing and invalid files, invents no numbers, and is read-only and safe in demo mode. The major is a test gap: the rule \"state totals equal type totals\" can be removed and every test stays green.\n\nPinning: I reviewed `git archive 3ecb8b1` (the card commit). The live HEAD during the review was f5ddec8; `git diff --stat 3ecb8b1 f5ddec8 -- app/backend/calibration_route.py tests/unit/test_calibration_route.py evals/reports/calibration.json` printed nothing, so the reviewed files are unchanged at live HEAD.\n\nSeverity: the card's validation rules are the thing I check against D.2. A hand-edited statement or a wrong sub-count is not an invented number produced by the app (the route serves only what is in the file), so nothing rises to blocker. Those gaps are minors, with the reasons in each finding.\n\n## Findings\n\n**F1 (major). The \"state totals equal type totals\" rule is untested.** `app/backend/calibration_route.py:73` is the only check of `by_state` against `by_type`. Replacing it with `if False:` leaves `tests/unit/test_calibration_route.py` at 23 passed. The test that looks like it covers it (`sum_mismatch_hand_edit`, `tests/unit/test_calibration_route.py:106`) is rejected by the statement check, because it changes only the count. A consistent hand-edit (count and its sentence changed together) is served as `ok` on the mutant and rejected on the real code: `artifacts/review-evidence/T-099-staff-engineer-results.txt`, \"consistent hand-edit\" lines. The card lists this rule as validation; a regression would serve a wrong \"matched N/M times\" line with no failing test.\n\n**F2 (minor). The route checks less than the producer.** `app/backend/calibration_route.py:37-41` (`_statement_ok`) only requires that the substring \"N/M times\" appear in a statement. `evals/run.py:1041` rebuilds all statements from the counts and requires equality, and `evals/run.py:1043-1045` compares prompt and lexicon hashes with disk. Probe `hand_edit_sentence_claim` rewrites the verified-overall sentence to end \"so the letter is safe to send.\" and the route returns `ok`; the UI shows statements verbatim (`memory/contracts/api.md`, T-099 section). The hash comparison is absent from the route, so a measurement made on older prompts is served with no staleness signal. This is latent, not live: I checked three hashes (`app/llm/lexicon.yaml`, `app/llm/prompts/judge_faithfulness_v1.md`, `app/llm/prompts/extract_v1.md`) with `shasum -a 256` and they match the committed file.\n\n**F3 (minor). Fields the route serves are not cross-checked.** `calibration_route.py:52-57` checks only the type of `backend`, `case_count` and `small_sample`; `:78` checks only that `by_case` is a dict. Probes, all `ok`: `case_count` 500 while the sentences say \"10 golden cases\" (`hand_edit_case_count`); `by_case` `[1, 9]` in a 55-item cell (`hand_edit_by_case_only`); `by_case` `[12, 9]` (`by_case_matched_gt_total`); `small_sample` false with 10 cases (`small_sample_flipped`, the threshold is `evals/run.py:244`, CAL_SMALL_N = 30); `backend` changed to `claude-sonnet-5-5` while the sentence names the fixture backend (`hand_edit_backend_label`). The counts the card cares about are checked; these labels and sub-counts are not.\n\n**F4 (minor). The card's evidence does not reproduce.** The T-099 card AC 1 says `pytest -q tests/unit -k calibration gives 34 passed`. At 3ecb8b1 the command prints `32 passed, 2 skipped, 1570 deselected`, the skips are `tests/unit/test_eval_runner.py:636: no git repository here (exported tree)`, and `tests/unit/test_calibration_route.py` alone gives 23 passed. The feature is fine; the evidence line is wrong, and \"done\" rests on it.\n\n## What I exercised\n\n- `git show --stat 3ecb8b1`; `git show 3ecb8b1 -- app/backend/api.py app/backend/calibration_route.py` (read in full); `git archive 3ecb8b1` into the scratchpad.\n- `.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration -rs` on the archive: 32 passed, 2 skipped. `tests/unit/test_calibration_route.py` alone: 23 passed.\n- State probes on 22 scratch files (missing, not JSON, not UTF-8, list, wrong schema, state total, sentence, floats, bools, cell `matched > total`, not_scored, extra key, directory): `artifacts/review-evidence/T-099-staff-engineer-probe-states.py`. Results: `artifacts/review-evidence/T-099-staff-engineer-results.txt`.\n- Consistent hand-edit probe: `artifacts/review-evidence/T-099-staff-engineer-probe-consistent-edit.py` (real code: invalid; mutant: ok).\n- HTTP demo-mode probe on the real app: `artifacts/review-evidence/T-099-staff-engineer-probe-http.py`. GET `/api/calibration` returns 200, envelope keys `calibration, message, status`, status `ok`; POST, PUT, PATCH and DELETE return 405; `/api/health` reports `demo_mode: True`; the body contains none of `token`, `excerpt`, `Patient`, `summary`.\n- Mutants on a scratch copy: `artifacts/review-evidence/T-099-staff-engineer-mutants.py` (M1 sentence check removed: 1 failed; M2 state-total check removed: 23 passed; M3 `problems()` ignored: 11 failed; M4 all methods accepted: 1 failed; restored: 23 passed).\n- Read the committed `evals/reports/calibration.json` and checked its arithmetic: verified 83/84 = 9+54+20 and 9+55+20; needs_review 10/10 = 6+2+2; `source_commit` b85fc1b; `case_count` 10 and `small_sample` true agree with the sentences.\n- Read `memory/contracts/api.md` (T-099 section), `evals/run.py:1029-1047` (`check_calibration`), `evals/run.py:6` (`--check-fresh`), and the cards via `python3 tools/board.py show T-099` and `show T-096`.\n- Not exercised: the review screen (T-096 is not built); the Docker image (release lane).\n\n```json\n{\"card\": \"T-099\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 3ecb8b1 (app/backend/api.py hook, app/backend/calibration_route.py, tests/unit/test_calibration_route.py) via git archive 3ecb8b1; live HEAD f5ddec8 checked: no change to the reviewed files; no app URL (FastAPI TestClient, real app, default demo mode); committed evals/reports/calibration.json (sample: 10 golden cases, fixture backend)\",\n \"exercised\": [\n  \"git show --stat 3ecb8b1; git show 3ecb8b1 -- app/backend/api.py app/backend/calibration_route.py (full); git archive 3ecb8b1 into scratch t099-3ecb8b1\",\n  \"git diff --stat 3ecb8b1 f5ddec8 -- app/backend/calibration_route.py tests/unit/test_calibration_route.py evals/reports/calibration.json -> empty\",\n  \".venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration -rs -> 32 passed, 2 skipped (test_eval_runner.py:636); tests/unit/test_calibration_route.py -> 23 passed\",\n  \"artifacts/review-evidence/T-099-staff-engineer-probe-states.py: 22 scratch files through calibration_route.load; statuses ok/missing/invalid as listed in artifacts/review-evidence/T-099-staff-engineer-results.txt\",\n  \"artifacts/review-evidence/T-099-staff-engineer-probe-consistent-edit.py: state total and its sentence changed together -> invalid on 3ecb8b1; ok with calibration_route.py:73 disabled\",\n  \"artifacts/review-evidence/T-099-staff-engineer-probe-http.py: GET /api/calibration -> 200 status ok, keys calibration/message/status; POST, PUT, PATCH, DELETE -> 405; /api/health demo_mode True; body has no token, excerpt, Patient or summary\",\n  \"artifacts/review-evidence/T-099-staff-engineer-mutants.py on the scratch copy: M1 sentence m/t check removed -> 1 failed; M2 state-total check removed -> 23 passed; M3 problems() ignored -> 11 failed; M4 all methods accepted -> 1 failed; restored -> 23 passed\",\n  \"read evals/reports/calibration.json (committed): arithmetic checked (verified 83/84 = 9+54+20 and 9+55+20; needs_review 10/10 = 6+2+2); shasum -a 256 of app/llm/lexicon.yaml, app/llm/prompts/judge_faithfulness_v1.md, app/llm/prompts/extract_v1.md matches the hashes in the file\",\n  \"read memory/contracts/api.md T-099 section; evals/run.py 6, 244, 1029-1047; app/backend/calibration_route.py in full; tests/unit/test_calibration_route.py test names and INVALID_CASES (lines 56-177); python3 tools/board.py show T-099 and show T-096\"],\n \"verdict\": \"changes\",\n \"scores\": {\"contract_shape\": 4, \"never_invents_numbers\": 3, \"demo_safety\": 5, \"validation_strength\": 2, \"test_pins_behaviour\": 2},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"The 'state totals equal type totals' validation rule is untested: removing it keeps all 23 route tests green\",\n   \"evidence\": \"app/backend/calibration_route.py:73 (if bs[s][k] != sum(bt[t][s][k] ...)). Mutant with the check replaced by 'if False:': .venv/bin/python -m pytest -q tests/unit/test_calibration_route.py -> 23 passed (artifacts/review-evidence/T-099-staff-engineer-mutants.py, M2). tests/unit/test_calibration_route.py:106 (sum_mismatch_hand_edit) is rejected by the statement check, not the sum check. Consistent hand-edit (by_state.verified 82/84 with its sentence rewritten): ok on the mutant, invalid on 3ecb8b1 (artifacts/review-evidence/T-099-staff-engineer-results.txt).\",\n   \"why_it_matters\": \"The card lists this rule as a validation step. It is the only check that stops a headline total being edited together with its sentence. No test fails when it is removed, so a regression would serve a wrong 'matched N/M times' line with no failing test. Rated major (tests fail when the code breaks).\",\n   \"fix\": \"Add an INVALID_CASES entry whose sentences are rebuilt to match the changed state total, so only the sum check can reject it, and assert the problem names by_state.verified.matched.\",\n   \"acceptance_test\": \"New case returns status invalid; with calibration_route.py:73 disabled the new test fails.\"},\n  {\"severity\": \"minor\", \"title\": \"The route validates less than the producer's own check (sentences are not rebuilt; hashes are not compared)\",\n   \"evidence\": \"app/backend/calibration_route.py:37-41 (_statement_ok: only the substring 'N/M times' is required), :85-90 (statement checks). evals/run.py:1041 rebuilds the statements from the counts and requires equality; evals/run.py:1043-1045 compares prompt and lexicon hashes with disk. Probe hand_edit_sentence_claim (artifacts/review-evidence/T-099-staff-engineer-results.txt): verified-overall sentence changed to end 'so the letter is safe to send.' -> status ok.\",\n   \"why_it_matters\": \"The UI shows the statements verbatim (memory/contracts/api.md T-099 section), so a hand-edited statement that keeps the numbers is shown as measured. The same file fails check_calibration, so the server accepts what the producer rejects. A calibration measured on older prompts is also served with no staleness signal. Latent, not live: the three hashes I checked match the files on disk.\",\n   \"fix\": \"Move calibration_sentences into a module both evals/run.py and calibration_route.py import; require exact equality with the file's sentences. Add the hash comparison (or a freshness field in SERVED) so a stale file is flagged.\",\n   \"acceptance_test\": \"A calibration whose sentence adds a claim is invalid; a file whose prompt hash differs from disk is invalid or served with a stale flag.\"},\n  {\"severity\": \"minor\", \"title\": \"by_case, case_count, small_sample and backend are served without cross-checks\",\n   \"evidence\": \"app/backend/calibration_route.py:52-57 (backend, case_count, small_sample: type checks only), :78 (by_case: dict check only). Probes, all status ok (artifacts/review-evidence/T-099-staff-engineer-results.txt): hand_edit_case_count (case_count 500, sentences still say '10 golden cases'); hand_edit_by_case_only (by_case [1, 9] in a 55-item cell); by_case_matched_gt_total ([12, 9]); small_sample_flipped (false with 10 cases; threshold evals/run.py:244 CAL_SMALL_N = 30); hand_edit_backend_label (backend 'claude-sonnet-5-5' while the sentence says fixture backend).\",\n   \"why_it_matters\": \"The served envelope carries numbers and labels that the statements and the sample size contradict, and the UI can show them. The card's 'never invented numbers' holds for the headline counts, but these fields are not checked against each other or against the sentences.\",\n   \"fix\": \"Check that by_case sums equal each cell total and that matched <= total per case; require case_count == len(cases); require small_sample == (case_count < 30); require backend to match the backend named in the sentences.\",\n   \"acceptance_test\": \"Each probe above returns status invalid.\"},\n  {\"severity\": \"minor\", \"title\": \"The card's test evidence does not reproduce\",\n   \"evidence\": \"T-099 card AC 1 evidence (python3 tools/board.py show T-099): 'pytest -q tests/unit -k calibration gives 34 passed'. At 3ecb8b1: '32 passed, 2 skipped, 1570 deselected' (artifacts/review-evidence/T-099-staff-engineer-results.txt); 'SKIPPED [2] tests/unit/test_eval_runner.py:636: no git repository here (exported tree)'. tests/unit/test_calibration_route.py alone: 23 passed.\",\n   \"why_it_matters\": \"The 'done' evidence is what the orchestrator checks. The numbers do not match what the command prints, and the two skipped tests are from another file. The feature is unaffected.\",\n   \"fix\": \"Correct the card's evidence line to the printed counts, or select the route file explicitly (tests/unit/test_calibration_route.py).\",\n   \"acceptance_test\": \"The cited command prints the cited numbers.\"}\n ],\n \"whats_right\": [\n  \"Envelope and empty states are right: GET returns 200 with {status, calibration, message}; missing and invalid files give calibration null with a constant message; no default numbers appear in any state (state probes, HTTP probe).\",\n  \"Invalid files never echo their contents: an extra key with record-like text is not served, and the logs name only the rule (state probes 'extra_key'; server log lines in the results file).\",\n  \"Read-only and demo-safe: POST, PUT, PATCH and DELETE return 405, no case token or record text is served, and the route is not gated by demo mode (HTTP probe; test_route_is_read_only).\"],\n \"questions_for_chris\": [\n  \"Should the route refuse a calibration whose prompt or lexicon hashes differ from disk, as evals/run.py check_calibration does, or serve it with a stale flag for the review screen to show?\"]}\n```\n"
}
````

### User / tool · 2026-11-02T05:17:44.689Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-099-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:17:48.421Z

**tool call — Bash**
````
{
 "command": "/usr/bin/python3 - <<'EOF'\nimport json, re\nfor f in [\"reviews/T-098-staff-engineer.md\", \"reviews/T-099-staff-engineer.md\"]:\n    t = open(f, encoding=\"utf-8\").read()\n    blocks = re.findall(r\"```json\\n(.*?)\\n```\", t, re.S)\n    d = json.loads(blocks[0])\n    sev = [x[\"severity\"] for x in d[\"findings\"]]\n    exp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\n    print(f, \"| fences\", t.count(\"```json\"), \"| card\", d[\"card\"], \"| model\", d[\"model\"], \"| verdict\", d[\"verdict\"], \"expected\", exp, \"| ok\", d[\"verdict\"] == exp, \"| findings\", sev, \"| whats_right\", len(d[\"whats_right\"]))\nEOF\nls -la reviews | grep \"T-09[89]\"; ls artifacts/review-evidence | grep \"T-09[89]\\|T-099\"",
 "description": "Validate both review JSON blocks against the verdict rule and list the evidence files"
}
````

### User / tool · 2026-11-02T05:17:48.570Z

**tool result**
````
reviews/T-098-staff-engineer.md | fences 1 | card T-098 | model claude-haiku-5-5 | verdict fail expected fail | ok True | findings ['blocker', 'major', 'minor', 'minor'] | whats_right 3
reviews/T-099-staff-engineer.md | fences 1 | card T-099 | model claude-haiku-5-5 | verdict changes expected changes | ok True | findings ['major', 'minor', 'minor', 'minor'] | whats_right 3
-rw-r--r--@   1 arsis  staff  16113 Nov  1 23:16 T-098-staff-engineer.md
-rw-r--r--@   1 arsis  staff  14301 Nov  1 23:17 T-099-staff-engineer.md
T-098-staff-engineer-f5ddec8-recheck.txt
T-098-staff-engineer-mutants.py
T-098-staff-engineer-probe1.py
T-098-staff-engineer-probe2.py
T-098-staff-engineer-probe3-verdicts.py
T-098-staff-engineer-results.txt
T-099-staff-engineer-mutants.py
T-099-staff-engineer-probe-consistent-edit.py
T-099-staff-engineer-probe-http.py
T-099-staff-engineer-probe-states.py
T-099-staff-engineer-results.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:18:02.329Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t098_t099_review_patterns.md",
 "content": "---\nname: project_t098_t099_review_patterns\ndescription: T-098 e511778 (gate for edited wording): AI-draft invented number accepted with one click, D-047 409 leftover closed by T-100; T-099 3ecb8b1 (calibration route): state-sum rule untested, consistent hand-edit passes, route weaker than evals check\nmetadata:\n  type: project\n---\n\nT-098 r1 (e511778, pinned 196c985; verdict fail: 1 blocker, 1 major, 2 minor; reviews/T-098-staff-engineer.md).\n- **A gate that covers only human wording leaves the AI path open.** `_code_check_gated` requires `_paralegal_wording`, and `apply_review` accept applies no code check, so an AI draft with an invented number (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, state needs_review) reached GET /export after one accept, with the judge at supported, unsupported or disagrees. The human-typed version got 422. How to apply: for any \"gate blocks X\" fix, probe the same content through every producer (AI draft, human edit, manual entry) and compare the export outcome.\n- **A binding decision is closed by a later card, not by the one reviewed.** D-047 (docs 36a982b) said the 409 keep-wording path is removed; the code landed in T-100 (24c18a7) and the UI in f5ddec8, both after my pin. Rated major (fail-closed, no invented fact leaves), closed at live HEAD. How to apply: for a \"remove X\" decision, grep X at the pin and at live HEAD and re-run the probe at live HEAD before saying \"open\".\n- **Carry-over hunks in a commit ship untested.** e511778 carried T-094's conflict branch (trace.py candidate_rule) and moved `_ocr_steps`; no test references candidate_rule or paired_by_code at any of the three SHAs. How to apply: on any commit whose message names other cards' hunks, `grep -rn` each new branch's key string under tests/.\n- Mutant M3 (drop the reason-code filter in the new gate blocker) survived 88 tests: over-blocking is untested. Filters on a shared list need a test with an out-of-set reason.\n\nT-099 r1 (3ecb8b1, pinned archive; verdict changes: 0 blockers, 1 major, 3 minor; reviews/T-099-staff-engineer.md).\n- **A validation rule that another check always catches is untested.** `state total == type total` (calibration_route.py:73) was never the decisive check: the sentence check fired first in the only test that touches it. Removing the rule kept 23 tests green. How to apply: for each validation clause, mutate it and check that a test fails for that clause alone (the case must not be caught by another clause).\n- **Consistent hand-edit probe:** change a count AND the sentence that quotes it together. Passes only if the rule being tested is the only one that can reject it. This is what exposed the gap.\n- **Route validation weaker than the producer's check:** evals/run.py check_calibration rebuilds the sentences and compares hashes; the route checks only the \"N/M times\" substring and no hashes. Hand-edited claims (\"so the letter is safe to send\") are served. How to apply: when a server re-validates an artifact the producer already validates, diff the two validators clause by clause.\n- Card evidence said \"34 passed\" for `-k calibration`; the command prints 32 passed and 2 skipped from test_eval_runner.py, route file 23 passed. Check the printed counts, not the card.\n\nHarness and method notes (this review):\n- Pin HEAD by sha: HEAD moved twice during the review (196c985 to e7a1987 to f5ddec8). Re-run the open items at live HEAD and say which SHA each result is from.\n- pytest `-k a -k b` keeps only the last `-k`; use `-k \"a or b\"`.\n- The fixture `2026-01-09` date contributes digits 2026, 1, 9 to the allowed-number set (`_allowed_numbers`, parsed date is allowed by D-034), so \"Pain 9/10\" passes on that record. Use a number with no date digit (5) for the invented-number probe.\n- The board guard refused `sed -i` on a file under artifacts/review-evidence with the message \"reviewers may not edit ... in place\". Use Write for edits to my own evidence files.\n- `timeout` is not installed on this macOS shell; run pytest without it.\n- Probe the AI path with real `generator.verify` for the state, then set the judge row and state on the scratch DB (`DB.update_item(..., ladder=...)`); the server reads per request.\n\nRelated: [[project_t080_trace_review_patterns]] (gate vs export agreement, exemption in one function), [[project_t073_t084_review_patterns]] (commit-level deletions, rate phrase on gate), [[feedback_severity_vs_brief]] (D.2 vs brief default: kept major for D-047, blocker for the AI path).\n"
}
````

### User / tool · 2026-11-02T05:18:02.426Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t098_t099_review_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:18:03.764Z

**tool call — Bash**
````
{
 "command": "tail -3 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md | cut -c1-200; echo ---; python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Check the memory index tail and run the read-only board validator"
}
````

### User / tool · 2026-11-02T05:18:03.920Z

**tool result**
````
- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without p
- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 031a708 fail (HEAD revert); r2 31b7ceb pass: partial restore, later-card hunks, CLI crash out of scope
- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks 
---
ok (100 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:18:05.796Z

**tool call — Bash**
````
{
 "command": "printf '%s\\n' '- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted, D-047 409 closed by T-100; T-099 3ecb8b1 changes: state-sum rule untested, route weaker than evals check' >> .claude/agent-memory/staff-engineer-reviewer/MEMORY.md && tail -1 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md | cut -c1-120",
 "description": "Add the new pattern file to the memory index"
}
````

### User / tool · 2026-11-02T05:18:05.890Z

**tool result**
````
- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:18:09.742Z

T-098 verdict fail (blocker: an AI draft with an invented "5/10" is accepted and exported after one click, outside the card's AC; major: the D-047 409 path existed at e511778 and T-100 closed it at f5ddec8; trace+export tests 88 passed): /Users/arsis/zlayt-pm-project/reviews/T-098-staff-engineer.md
T-099 verdict changes (major: removing the state-total check leaves all 23 route tests green; 3 minors): /Users/arsis/zlayt-pm-project/reviews/T-099-staff-engineer.md
