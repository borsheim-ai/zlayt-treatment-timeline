# Subagent: T-146 r2 staff review (T-146 r2 staff review)

Source: `agent-aba677539e62421f0.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T13:58:53.083Z

This is the round-2 review of board card T-146 (commit 2db6ad2) in /Users/arsis/zlayt-pm-project. Read reviews/T-146-staff-engineer.md and `python3 tools/board.py show T-146`, including the orchestrator's note and the handoff.

On a `git archive HEAD` copy:
- **Re-runs with errors.** No re-run that ends with errors (done_with_errors, failed, deadline, or a failed flag step) may overwrite a decided item or one with stored output, undo a second-check answer, or delete flags. The case must show an honest `failed`/`run_partial` error naming the count and the step.
- **Repro.** Reproduce your round-1 case (an extract-step failure during a re-run after accepting entries) and compare the full stored rows.
- **Judge wording.** A judge that was called and failed says "The second check failed"; a deadline or fixture miss still says JUDGE_NOT_RUN.
- **Tests.** Mutate the code to test the tests, and run the unit suite.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-146-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings, exercised. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:58:55.341Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T13:58:55.349Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:58:55.711Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-146-staff-engineer.md"
}
````

### User / tool · 2026-11-02T13:58:55.718Z

**tool result**
````
1	# T-146 staff-engineer review (7d3ca35, tested on a `git archive` of 7d3ca35)
2	
3	Verdict: **changes** (0 blockers, 1 major, 1 minor).
4	
5	The timed-out re-run is fixed as the card says. On a `git archive HEAD` copy (HEAD 7d3ca35 at archive time; `pipeline.py` unchanged since) I completed the sample (9 entries, 4 amounts, 10 flags on the fixture backend), accepted e1, dismissed e2, accepted a1, then re-ran with an injected clock that passes the 480 s deadline when a named stage starts. For `extract`, `amounts` and `conflicts` (plus the `verify`, `judge_entries`, `flags` and mid-flags cases in the card's own tests), case status is `failed`, error `run_deadline`, and entries 9/9, amounts 4/4, flags 10/10 keep identical `(review_status, state, state_reasons)`: nothing deleted, nothing downgraded, the decisions stand. A first-ever run that times out still stores what finished. The message now reads "every item from earlier runs and every decision of yours was kept unchanged", which is true for that path (and `app/frontend/input.js:75` shows it after "Your records are kept and finished items are saved").
6	
7	The AC also says "or failed re-run". A re-run where the AI step fails (not a deadline) still loses accepted work. See F1.
8	
9	What I ran, on the archive with the project `.venv/bin/python`:
10	- `pytest tests/unit -q -p no:cacheprovider`: **3668 passed, 8 skipped**, no failures. The two new files: 11 passed.
11	- Timed-out re-run probes at `extract`, `amounts`, `conflicts` (before/after compare of state and reasons for entries, amounts, flags with decisions made); timed-out run then full re-run (accept kept, gate clears); extract-down re-run; judge-down re-run.
12	- Mutants of `_persist` and its callers on a second scratch copy, each restored: entries persisted non-additive (2 fail), amounts non-additive (3 fail), flags non-additive (5 fail), drop the `continue` that skips existing ids (3 fail), drop the early `return` that skips the stale-delete (5 fail), additive branch overwrites ladder and excerpt (5 fail). **Survived:** (a) message reverted to "finished items were kept" (11 pass), (b) additive branch sets an existing entry's `summary` to NULL (11 pass). See F2.
13	- Greps for `done_with_errors` and `finished items` across `app/`, and the other places that write case `status="failed"`.
14	
15	```json
16	{
17	  "card": "T-146",
18	  "persona": "staff-engineer-reviewer",
19	  "model": "claude-sonnet-5-5",
20	  "scope": "commit 7d3ca35 (app/backend/pipeline.py _persist additive mode and the run_deadline message, tests/unit/test_t146_rerun_keeps_items.py); git archive of 7d3ca35; fixture backend; sample case evals/golden/sample.txt",
21	  "exercised": [
22	    "read GATE-M2-staff-engineer.md F2, python3 tools/board.py show T-145 and T-146, git show 7d3ca35",
23	    "git archive HEAD (7d3ca35) into a scratch dir; pytest tests/unit -q -p no:cacheprovider: 3668 passed, 8 skipped",
24	    "re-run probes: complete run, accept e1, dismiss e2, accept a1, then re-run with a deadline at extract, amounts, conflicts: item counts and (review_status, state, reasons) identical for entries, amounts, flags; case failed/run_deadline",
25	    "timed-out first run then full re-run: accept kept, state verified, gate clears",
26	    "extract-down re-run (extract raises LLMFailed) and judge-down re-run (j1/j2 raise LLMFailed): before/after compare, DB.get_item('e1'), case status and error, trace.export_blockers",
27	    "seven mutants of _persist/run_pipeline (entries, amounts, flags non-additive; continue dropped; early return dropped; ladder overwrite; message revert; summary overwrite): five killed by count, two survived (message text, summary-only overwrite)",
28	    "grep of done_with_errors, 'finished items', status=\"failed\" writers in app/backend; read of present/trace RUN_FAILED text and app/frontend/input.js:75"
29	  ],
30	  "verdict": "changes",
31	  "scores": {
32	    "timeout_rerun_keeps_items_and_decisions": 5,
33	    "failed_rerun_keeps_accepted_work": 2,
34	    "message_tells_the_truth": 3,
35	    "test_quality_mutation_sensitivity": 3,
36	    "no_silent_data_loss": 3
37	  },
38	  "findings": [
39	    {
40	      "severity": "major",
41	      "title": "A failed re-run (AI step down) still overwrites the paralegal's accepted entries with empty failure stubs, and the case reads 'ready' with no error",
42	      "evidence": "AC 1 of T-146: 'a timed-out or failed re-run keeps every previous item and decision'. Only `timed_out` is made additive (pipeline.py:425-427 `additive=timed_out`); every other status takes the replace path (`DB.update_item(conn, it['id'], **row)`, pipeline.py:244-247 at HEAD). Repro (archive of 7d3ca35, fixture backend): complete run; `DB.apply_review(conn,'e1','accept')`; `PL.run_pipeline(conn, cid, raw, call=FakeCall(sample_script(extract=AU.LLMFailed('x', last_error='TIMEOUT'))), now=lambda: 3.0)` -> status `done_with_errors`, case status `ready`, case error `None`; `DB.get_item(conn,'e1')` = `{summary: None, excerpt: None, excerpt_start: None, state: 'rejected', state_reasons: ['LLM_FAILED_AFTER_RETRIES'], review_status: 'accepted', ...}`; before the re-run e1 held the 'Restrained driver rear-ended at approx. 35 mph ...' summary and its verbatim excerpt. Every one of the 9 entries changed this way (verified/pending/dismissed -> rejected). `trace.export_blockers` then returns `[(None, 'NOTHING_ACCEPTED')]`. `done_with_errors` is never stored (grep: only pipeline.py:432 and :570), so no case-level message says the re-run failed. A judge-down re-run (j1/j2 raise) downgrades e1..e9 and a1/a4 from `verified` to `needs_review JUDGE_UNAVAILABLE` while the case is `ready` (that one is visible per item, and recoverable by the rejudge button).",
43	      "why_it_matters": "This is the same class as the gate finding the card fixes: a normal failure (backend down on the second click of Run) erases an AI summary and quote the paralegal had already accepted, keeps the 'accepted' flag on an empty row, and tells her nothing at case level. The only per-item trace is a 'rejected' state with LLM_FAILED_AFTER_RETRIES. The record text survives, so another run recovers it, which keeps this at major rather than blocker. If Chris reads 'failed' in the AC as case status `failed` only, the AC is met on its narrow reading, but the loss is the same and the card's own handoff ('Surprised: ... the whole persist is additive') shows the intent was to protect earlier results from partial runs.",
44	      "fix": "When the re-run produces a failure stub for an id that already has a stored row with a summary and excerpt (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, SCHEMA_INVALID at extract), keep the stored row and record the failure on the run (case `error` with a code such as run_partial and a message that names how many records failed), instead of replacing it. Do the same for judge-down: do not downgrade a stored judged state on a run whose judge call failed, or at least store a case-level error. Alternatively split this into a new card and change the T-146 AC to say 'timed-out'.",
45	      "acceptance_test": "Unit test: complete run, accept e1, re-run with extract raising LLMFailed; assert e1 still has its summary, excerpt, state and 'accepted', and the case has an error naming the failed re-run. Add the judge-down variant asserting no verified item is downgraded without a stored error. Mutation: replacing the keep-old rule with the current replace makes it fail."
46	    },
47	    {
48	      "severity": "minor",
49	      "title": "The tests do not pin the message the card changed, and compare only review_status/state/reasons, so a summary-only overwrite and the old message both pass",
50	      "evidence": "tests/unit/test_t146_rerun_keeps_items.py:34-35 `_snapshot` returns `(review_status, state, state_reasons)` per item; the only message assertion is `json.loads(c['error'])['code'] == 'run_deadline'` (line 47). Mutant (a): replace the new message text with the old 'finished items were kept' -> `11 passed`. Mutant (b): in `_persist`, `if additive and old is not None: if kind == 'entry': DB.update_item(conn, it['id'], now=now, case=cid, summary=None); continue` -> `11 passed`. The card's AC half 'the message tells the truth' therefore has no test that fails when the message changes, and a regression that wipes summary, excerpt, date or computed numbers while leaving state alone is invisible.",
51	      "why_it_matters": "Checklist 13: tests assert behaviour, and at least one must fail when the guarded behaviour is removed. The fix is correct today, but the safety net covers the three state fields, not the content a paralegal accepted.",
52	      "fix": "Snapshot the full stored row (summary, excerpt, date_iso, record_ids, computed, ladder judge verdict) and assert equality; assert the message text, or better, that it contains 'earlier' and 'kept' and does not contain 'finished items'.",
53	      "acceptance_test": "Both mutants above fail the strengthened tests; the existing six still pass."
54	    }
55	  ],
56	  "whats_right": [
57	    "The additive persist is the right design: a timed-out run neither deletes, downgrades nor overwrites, so pending items, judged states, flags and the paralegal's decisions are identical before and after at every stage I tried (extract, amounts, conflicts, plus the card's verify, judge_entries, flags, mid-flags).",
58	    "Five of seven mutants (three kinds non-additive, dropped continue, dropped early return, ladder overwrite) are killed by the count and state snapshots, and a first-ever timed-out run still stores what finished.",
59	    "A timed-out run followed by a full re-run recovers cleanly: the accepted e1 stays accepted and becomes verified, and the export gate clears."
60	  ],
61	  "questions_for_chris": [
62	    "Does 'failed re-run' in T-146 AC 1 mean only a case that ends status failed (deadline, unsupported language, crash), or any re-run where the AI step fails (done_with_errors)? F1 assumes the second reading; if the first, move F1 to its own card."
63	  ]
64	}
65	```
66	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:58:56.110Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-146; git log --oneline | head -5; git rev-parse HEAD"
}
````

### User / tool · 2026-11-02T13:58:56.314Z

**tool result**
````
---
id: "T-146"
title: "GATE-M2 major (staff): a timed-out re-run deletes the previous run's pending items while the error says finished items were kept"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T13:09:56Z"
updated_at: "2026-11-02T13:58:48Z"
claimed_by: "backend"
claimed_at: "2026-11-02T13:39:44Z"
rounds: 1
commits: ["7d3ca35a434914a83318255c703c375b2e443b93", "2db6ad2"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-146-staff-engineer.md", "at": "2026-11-02T13:39:36Z"}
ac:
  - {"n": 1, "text": "a timed-out or failed re-run keeps every previous item and decision (or keeps exactly what the error message says); test reproduces 9 entries/11 flags kept", "done": true, "evidence": "tests/unit/test_t146_r2_failed_rerun_keeps_items.py (11 tests: extract-down, one-record-down, judge-down, flag-step-down re-runs keep full stored rows, case failed/run_partial with message; deadline at 5 stages keeps full rows; message text asserted; mutants no-protect/summary-wipe/prune/old-message each fail)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:10:00Z orchestrator: assigned: backend
- 2026-11-02T13:10:11Z backend: claimed
- 2026-11-02T13:14:56Z backend: Fix in pipeline.py: _persist(additive=timed_out) adds only unseen ids on a timed-out run; no delete, no overwrite, so a complete earlier run and the paralegal's decisions are untouched; error message reworded to say exactly that. Reviewer saw 11 flags; this sample gives 10 on the fixture backend, tests assert equality before/after not the count.
- 2026-11-02T13:26:49Z backend: AC 1 checked: tests/unit/test_t146_rerun_keeps_items.py (6 tests: complete run then timeout at extract/verify/judge_entries/flags and between records 3 and 4 -> every item, state and the accepted e1 decision unchanged; 9 entries, 10 flags on this fixture)
- 2026-11-02T13:26:50Z backend: moved in_progress -> in_review
- 2026-11-02T13:26:56Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T13:39:36Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-146-staff-engineer.md; round 1; findings:
    - [major] A failed re-run (AI step down) still overwrites the paralegal's accepted entries with empty failure stubs, and the case reads 'ready' with no error — fix: When the re-run produces a failure stub for an id that already has a stored row with a summary and excerpt (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, SCHEMA_INVALID at extract), keep the stored row and record the failure on the run (
    - [minor] The tests do not pin the message the card changed, and compare only review_status/state/reasons, so a summary-only overwrite and the old message both pass — fix: Snapshot the full stored row (summary, excerpt, date_iso, record_ids, computed, ladder judge verdict) and assert equality; assert the message text, or better, that it contains 'earlier' and 'kept' and does not contain 'finis
- 2026-11-02T13:39:36Z orchestrator: Orchestrator answer to the reviewer's question (not for Chris): 'failed re-run' includes any re-run with errors (done_with_errors, failed, deadline). No re-run may overwrite a decided item or an item with stored output with an empty or partial stub; errored records keep their previous items and the case shows an honest error. Also: tests assert the message text; kill the summary-wipe mutant. Cheap add: T-145 minor - a judge that was called and failed says 'second check failed', not 'JUDGE_NOT_RUN:' (keep the reason code).
- 2026-11-02T13:39:36Z orchestrator: assigned: backend
- 2026-11-02T13:39:44Z backend: claimed
- 2026-11-02T13:58:43Z backend: AC 1 checked: tests/unit/test_t146_r2_failed_rerun_keeps_items.py (11 tests: extract-down, one-record-down, judge-down, flag-step-down re-runs keep full stored rows, case failed/run_partial with message; deadline at 5 stages keeps full rows; message text asserted; mutants no-protect/summary-wipe/prune/old-message each fail)
- 2026-11-02T13:58:43Z backend: moved in_progress -> in_review
- 2026-11-02T13:58:48Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed (r2): _persist keeps a stored row whole when the re-run's output is a failure stub (extract LLM_FAILED/FIXTURE_MISS/SCHEMA_INVALID) or lost its second-check answer, skips stale-pending deletes when the flag/conflict step failed, and the case reads failed with error run_partial naming how many items and which step (api.md updated). why.join: a judge asked and failed says 'The second check failed', not 'JUDGE_NOT_RUN:' (reason code JUDGE_UNAVAILABLE unchanged; FIXTURE_MISS and deadline keep JUDGE_NOT_RUN). · Verified: 11 new tests assert full-row equality and message text; mutants (no protection, summary wipe in additive branch, prune on, old message) each fail; unit suite 4006 passed, 2 flaky (pass alone: case_extras, pdf rss) , 4 others failing from another worker's uncommitted amounts.py (t140, lib10), not mine. · Left: first run with a down step still stores stubs and reads ready; SUMMARY_NOT_IN_QUOTE (model answered) still replaces. · Surprised: call ids in amount/flag ladders differ between runs, so those compare without ladder. Commit 2db6ad2

2db6ad2 fix(backend): T-146 r2 a re-run with errors keeps stored rows whole (run_partial); a judge that failed says 'second check failed'
ba82071 docs(backend): api.md T-139 excerpt narrowing contract. Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
184cbb7 feat(backend): T-139 code narrows a quote whose charge sentences sit at its start or end. Rung 1 re-runs on the narrowed quote; judge 1 runs on the narrowed pair (D-044/D-058); held-out recorded entries 51 -> 9; J1 answers for the narrowed pairs and the sample narrative recorded with claude-cli. Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
255b001 fix(backend): T-143 r3 skip a line only on a whole-line admin pattern with no clinical kind
4f416a4 fix(backend): T-134 r4 re-picked-quote texts (review step, gate headline, conditional warning), rerun claim tied to the current quote, second_check_pending item field
2db6ad2e60b5131af587ee10e99e8db97eea7697
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:58:56.759Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t145_t146_patterns.md"
}
````

### User / tool · 2026-11-02T13:58:56.767Z

**tool result**
````
1	---
2	name: t145-t146-patterns
3	description: T-145 b604ff2 pass, T-146 7d3ca35 changes - shared reason sentence labels two cases, "failed re-run" AC covers only the timeout path, snapshot tests compare state only
4	metadata:
5	  type: project
6	---
7	
8	T-145 (deadline leaves entries verified) pass: `_mark_judge_not_run` call-site patch; 6/6 mutants killed. Minor: the "JUDGE_NOT_RUN:" prefix sits on the shared JUDGE_UNAVAILABLE sentence, so a judge that ran and failed (ladder reason NONE, model set) prints it too. compose_state still treats judge None as clean.
9	T-146 (timed-out re-run) changes: `_persist(additive=timed_out)` is right for timeouts, but a done_with_errors re-run (extract LLMFailed) still replaces accepted entries with summary=None stubs and the case stays `ready`, error None (`done_with_errors` is never stored). Tests snapshot only (review_status, state, reasons) and never the message; summary-null and old-message mutants survive.
10	
11	**How to apply:** for "keeps earlier results" fixes, probe every non-happy re-run status (timeout, done_with_errors, judge-down), not just the one named; compare full rows, and mutate the message text. Files: reviews/T-145-staff-engineer.md, reviews/T-146-staff-engineer.md. Errata: the T-146 file cites pipeline.py:244-247 for the replace path; it is :250 (write-once, not edited).
12	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:00.957Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/t146r2/arc && git archive HEAD | tar -x -C $S/t146r2/arc && git status --short | head; git show --stat HEAD | head -20; ls $S/t146r2/arc/.venv 2>&1 | head -2; ls .venv/bin/python"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:01.177Z

**tool call — Bash**
````
{
 "command": "git show HEAD -- app/ memory/ | head -600"
}
````

### User / tool · 2026-11-02T13:59:01.952Z

**tool result**
````
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
commit 2db6ad2e60b5131af587ee10e99e8db97eea7697
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:58:33 2026 -0600

    fix(backend): T-146 r2 a re-run with errors keeps stored rows whole (run_partial); a judge that failed says 'second check failed'
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/flags.py                               |   2 +-
 app/backend/pipeline.py                            |  67 ++++++--
 app/backend/present.py                             |   6 +-
 app/backend/why.py                                 |  19 ++-
 memory/contracts/api.md                            |   2 +-
 .../unit/test_t146_r2_failed_rerun_keeps_items.py  | 190 +++++++++++++++++++++
 6 files changed, 270 insertions(+), 16 deletions(-)
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2/arc/.venv: No such file or directory
.venv/bin/python
````

### User / tool · 2026-11-02T13:59:02.103Z

**tool result**
````
commit 2db6ad2e60b5131af587ee10e99e8db97eea7697
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:58:33 2026 -0600

    fix(backend): T-146 r2 a re-run with errors keeps stored rows whole (run_partial); a judge that failed says 'second check failed'
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/flags.py b/app/backend/flags.py
index 5b611b7..c04146a 100644
--- a/app/backend/flags.py
+++ b/app/backend/flags.py
@@ -42,7 +42,7 @@ def _compose(f: dict) -> dict:
     ctx = {"injection": st["injection"], "agreement": st.get("agreement"), "fixture_miss": st.get("fixture_miss", False),
            "llm_failed": st.get("llm_failed", False), "translated": st.get("translated", False)}      # D-050
     f["state"], f["reasons"] = confidence.compose_state(ladder, ctx)
-    f["why"] = " ".join(why.why(c) for c in f["reasons"]) if f["reasons"] else "Found by the phrase list and the model, and the second check agreed."
+    f["why"] = why.join(f["reasons"], (f.get("ladder") or {}).get("judge")) if f["reasons"] else "Found by the phrase list and the model, and the second check agreed."
     return f
 
 
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index 9221f82..a633e16 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -237,17 +237,38 @@ def _mark_judge_not_run(entries: list, by_n: dict) -> None:
         generator.compose(e, by_n[e["seq"]], judge="unavailable")
 
 
-def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bool = False) -> None:
+_STUB_REASONS = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"}      # an entry rejected for one of these has no output at all: a stub
+
+
+def _degrades(kind: str, old: dict, it: dict):
+    """T-146 r2: would storing `it` over the stored row `old` replace output with a stub or take back a second-check answer? True when
+    (entry) the re-run made a failure stub (no summary, no quote: the AI step failed) over a row that has a summary and a quote, or
+    (any AI-made item) the re-run's second check gave no answer where the stored row had one. Failures are never allowed to erase earlier work.
+    Returns the cause, 'writing the entries' or 'the second check', or None."""
+    if kind == "entry" and it.get("state") == "rejected" and set(it.get("reasons") or []) & _STUB_REASONS and old.get("summary") and old.get("excerpt"):
+        return "writing the entries"
+    new_j, old_j = (it.get("ladder") or {}).get("judge") or {}, (old.get("ladder") or {}).get("judge") or {}
+    return "the second check" if new_j.get("verdict") == "unavailable" and old_j.get("verdict") not in (None, "unavailable") else None
+
+
+def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bool = False, prune: bool = True) -> list:
     """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
     computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed.
     `additive` (T-146, a run that stopped at its deadline): only items with no stored row are added. A stopped run is partial, so it must not delete, downgrade or
-    overwrite what an earlier complete run stored (its judged states, its flags) or what the paralegal decided."""
+    overwrite what an earlier complete run stored (its judged states, its flags) or what the paralegal decided.
+    Also (T-146 r2, any run): a row whose re-run output is a failure stub or lost its second-check answer (`_degrades`) is left exactly as stored, and the stored rows
+    returned (`kept`, as (row, cause)) so the caller can say so. `prune=False`: the stale-pending delete is skipped (a failed flag step cannot tell which flags are stale)."""
     table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
     existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
+    kept = []
     for it in items:
         old = existing.get(it["id"])
         if additive and old is not None:
             continue
+        cause = _degrades(kind, old, it) if old is not None else None
+        if cause:
+            kept.append((old, cause))
+            continue
         if kind == "amount" and old is not None:        # T-084: a rerun keeps the class the paralegal gave a figure
             from app.backend import reclassify as RC
             it = RC.carry_over(old, it)
@@ -265,11 +286,15 @@ def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bo
         elif old["review_status"] != "pending":
             it["review_status"] = old["review_status"]
     if additive:
-        return
+        return kept
     keep = {i["id"] for i in items}
     for oid, old in existing.items():
         if oid not in keep and old["review_status"] == "pending":
+            if not prune:
+                kept.append((old, "finding the flags"))
+                continue
             conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
+    return kept
 
 
 def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
@@ -295,10 +320,11 @@ def _finish_amount(a: dict, ing: dict, judged) -> dict:
          "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
         {"injection": a["injection"], "amount_class": a["cls"], "translated": any(language.translated_record(by_n.get(n)) for n in a["record_nos"])})      # D-050
     a["state"], a["reasons"] = state, reasons
-    a["why"] = " ".join(WHY.why(c) for c in reasons) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
     a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
                    "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
-                              "verdict": judged["verdict"], "reason_code": judged.get("reason_code")} if judged else None)}
+                              "verdict": judged["verdict"], "reason_code": judged.get("reason_code")} if judged else None),
+                   **({"confirm": a["confirm"]} if a.get("confirm") else {})}      # D-059: the flag the paralegal must confirm by name before accepting this charge
+    a["why"] = WHY.join(reasons, a["ladder"]["judge"]) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
     return a
 
 
@@ -320,10 +346,22 @@ def _accident_year(recs: list):
     return int(ds[0][:4]) if ds else None
 
 
+def _noting(raw_call, failed_steps: list):
+    """T-146 r2: the same `call`, remembering the steps whose call failed (the AI layer gave up, or a fixture was missing). The failure still propagates to the
+    caller's own handling; this only lets the run say which steps were down."""
+    def call(step, system, user, schema, *, item_id=None):
+        try:
+            return raw_call(step, system, user, schema, item_id=item_id)
+        except (AU.LLMFailed, P.FixtureMiss):
+            failed_steps.append(step)
+            raise
+    return call
+
+
 def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
     clock = now if callable(now) else (lambda: time.time() if now is None else now)
     t0 = clock()
-    call = call or AU.make_call(conn, cid, now=clock)
+    call = _noting(call or AU.make_call(conn, cid, now=clock), failed_steps := [])
     errors, stage_done = [], []
 
     def set_stage(name):
@@ -433,9 +471,14 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
     PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
     now_t = clock()
-    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out)
-    _persist(conn, cid, "amount", final_amounts, now_t, additive=timed_out)
-    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t, additive=timed_out)
+    kept_e = _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out)
+    for a in final_amounts:                     # an amount stays linked to the entry whose record failed this time (that entry's stored row was kept)
+        if not a.get("entry_id"):
+            a["entry_id"] = next((o["id"] for o, _ in kept_e if f"r{a['record_nos'][0]}" in (o["record_ids"] or [])), None)
+    kept_a = _persist(conn, cid, "amount", final_amounts, now_t, additive=timed_out)
+    kept_f = _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t, additive=timed_out,
+                      prune=not ({"flags", "conflicts"} & set(failed_steps)))
+    kept_n = len(kept_e) + len(kept_a) + len(kept_f)
     _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
     if timed_out:
         status = "timeout"
@@ -443,7 +486,11 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     else:
         status = "done_with_errors" if errors else "done"
         err = None
-    DB.update_case(conn, cid, status="failed" if timed_out else "ready", stage="finalize", error=json.dumps(err) if err else None,
+        if kept_n:      # T-146 r2: an AI step failed on a re-run and its earlier results were kept; the case says so instead of reading 'ready'
+            what = " and ".join(sorted({c for _, c in kept_e + kept_a + kept_f}))
+            err = {"code": "run_partial", "message": f"The AI step failed for {kept_n} item{'s' if kept_n != 1 else ''} ({what}) on this run. Their earlier results and every "
+                                                      "decision of yours were kept unchanged. Run it again to retry."}
+    DB.update_case(conn, cid, status="failed" if (timed_out or err) else "ready", stage="finalize", error=json.dumps(err) if err else None,
                    run_finished_at=now_t, injection_records_json=ing["injection_records"])
     tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
     all_items = dated + undated + final_amounts + flag_items
diff --git a/app/backend/present.py b/app/backend/present.py
index dc0d0e5..d3d14d1 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -9,11 +9,11 @@ STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss",
 OK_WHY = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
 
 
-def _why(reasons):
+def _why(reasons, judge=None):
     out = []
     for c in reasons or []:
         try:
-            out.append(why.why(c))
+            out.append(why.why(c, None if "FIXTURE_MISS" in reasons else judge))
         except KeyError:
             pass
     return " ".join(out) if out else OK_WHY
@@ -35,7 +35,7 @@ def _ladder(row):
 
 
 def _common(row):
-    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons")),
+    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
             "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row)}
 
 
diff --git a/app/backend/why.py b/app/backend/why.py
index 83273b7..a19b813 100644
--- a/app/backend/why.py
+++ b/app/backend/why.py
@@ -44,10 +44,27 @@ MODEL_CONFLICT = ("The AI suggested a conflict between two passages, but the sof
                   "and they did not pick this one. Read both passages; add it by hand if it matters.")
 
 
-def why(code: str) -> str:
+# T-146 r2 / T-145: JUDGE_UNAVAILABLE is one closed reason code with two causes. The sentence follows the judge record: a judge that was asked and gave no usable
+# answer says so; one that never ran (deadline, or no judge record yet) keeps the JUDGE_NOT_RUN sentence. The reason code itself is unchanged.
+JUDGE_FAILED = "The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked."
+
+
+def judge_failed(judge) -> bool:
+    return bool(judge) and judge.get("verdict") == "unavailable" and judge.get("reason_code") != "JUDGE_NOT_RUN"
+
+
+def why(code: str, judge=None) -> str:
+    if code == "JUDGE_UNAVAILABLE" and judge_failed(judge):
+        return JUDGE_FAILED
     return _WHY[code]
 
 
+def join(reasons, judge=None) -> str:
+    """The sentences for a reason list. A recorded-answer miss (FIXTURE_MISS, demo) is not a failed call: no model was asked, so the 'did not run' sentence stays."""
+    j = None if "FIXTURE_MISS" in (reasons or []) else judge
+    return " ".join(why(c, j) for c in reasons or [])
+
+
 def all_codes() -> list:
     return list(_WHY)
 
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index e6d15c0..cbd0506 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -125,7 +125,7 @@ Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human dec
   "counts": {"entries": 9, "amounts": 3, "flags": 1},
   "error": null, "elapsed_ms": 21540 }
 ```
-`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline", "message": "..."}`; finished items are kept. Poll every second. Partial results are readable from the case endpoint while running.
+`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: the run passed its time limit; it only adds items that had no stored row, and every earlier item, second-check answer and decision of the paralegal is kept unchanged ("every item from earlier runs and every decision of yours was kept unchanged"). `run_partial`: an AI step failed on a re-run (the extract step made a failure stub, a second check gave no answer, or the flag step was down) and the stored rows it would have overwritten, or deleted as stale, were left exactly as they were; `message` names how many items and which step ("The AI step failed for N items (writing the entries / the second check / finding the flags) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."). `run_partial` is set only when something was kept; a first run with a failing step still stores its failure stubs and stays `ready` with `error: null`. A good re-run clears the error. **Second-check wording (T-145/T-146):** the `why` of a `JUDGE_UNAVAILABLE` item reads "JUDGE_NOT_RUN: the second AI check did not run or did not finish..." when no judge ran, and "The second check failed (the AI check was asked and gave no usable answer)..." when the judge was called and gave no answer (`ladder.judge.verdict: "unavailable"`, `reason_code` other than `JUDGE_NOT_RUN`); the state reason code is `JUDGE_UNAVAILABLE` in both. Poll every second. Partial results are readable from the case endpoint while running.
 
 ## GET /api/cases/{token}
 Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **D-057 / T-126, filtered by rule:** a model proposal that a code rule filters out (today D-032 `objective_negative`: a normal finding is not a flag) is not in `tray`, `flags`, `review.queue`, the review counts, the trace gate counts or the export. It is listed in the case payload's `tray_filtered`: `{label: "Filtered by rule", collapsed: true, needs_action: false, count, rules: [{rule: "objective_negative", ref: "D-032", label, explanation, count, items: [<tray flag items, reasons[0] FILTERED_BY_RULE>]}]}` (`count: 0, rules: []` when none). The frontend shows it as a collapsed group with the count and the rule name; no action is needed. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:05.271Z

**tool call — Bash**
````
{
 "command": "cat tests/unit/test_t146_r2_failed_rerun_keeps_items.py; git status --short app tests | head"
}
````

### User / tool · 2026-11-02T13:59:05.404Z

**tool result**
````
"""T-146 round 2: no re-run with errors (done_with_errors, failed, deadline) overwrites a decided item, or an item with stored output, with an empty or
partial stub. Errored records keep their previous rows (full row, not a few fields) and the case shows an honest error. T-145 add: a judge that was
called and failed says 'second check failed' (reason code unchanged), not 'JUDGE_NOT_RUN:'."""
import json

import pytest
from app.backend import pipeline as PL, present, why as WHY
from app.db import db as DB
from app.llm import audited as AU
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script

VOLATILE = {"updated_at"}


def _full(conn, cid, no_ladder=()):
    """Every stored column of every item: a summary-only, excerpt-only or ladder-only change shows up here. `no_ladder`: kinds compared without the ladder (those rows
    are legitimately remade by a re-run whose call numbering differs: only their call ids change)."""
    return {k: {i["id"]: {c: v for c, v in i.items() if c not in VOLATILE | ({"ladder"} if k in no_ladder else set())} for i in DB.list_items(conn, cid, k)}
            for k in ("entry", "amount", "flag")}


def _completed(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    assert PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 1.0)["status"] == "done"
    DB.apply_review(conn, "e1", "accept", now=2.0, case=cid)         # decisions made between the runs
    DB.apply_review(conn, "e2", "dismiss", now=2.0, case=cid)
    DB.apply_review(conn, "a1", "accept", now=2.0, case=cid)
    return conn, cid


def _rerun(conn, cid, **script):
    return PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(**script)), now=lambda: 3.0)


def _down(step):
    return AU.LLMFailed(f"{step} down", last_error="TIMEOUT")


def _err(conn, cid):
    c = DB.get_case(conn, cid)
    return c, (json.loads(c["error"]) if c["error"] else None)


def test_extract_down_rerun_keeps_every_stored_row_whole_and_says_so(tmp_path):
    conn, cid = _completed(tmp_path)
    before = _full(conn, cid, ("amount", "flag"))
    out = _rerun(conn, cid, extract=_down("extract"))
    assert out["status"] == "done_with_errors"
    assert _full(conn, cid, ("amount", "flag")) == before                      # summary, excerpt, offsets, ladder, state, review status: all of it
    assert before["entry"]["e1"]["summary"] and before["entry"]["e1"]["review_status"] == "accepted"
    c, err = _err(conn, cid)
    assert c["status"] == "failed" and err["code"] == "run_partial"
    assert "earlier" in err["message"] and "kept" in err["message"] and "finished items" not in err["message"]
    assert "9 " in err["message"]                          # names how many items the failed step touched
    assert out["error"] == err


def test_one_record_failing_keeps_that_row_and_the_rest_are_rerun(tmp_path):
    conn, cid = _completed(tmp_path)
    before = _full(conn, cid)
    sums = sample_script()["extract"]

    def extract(user):
        if "Restrained driver" not in user and "rear-ended" in user:    # only the record that e1 was made from
            raise _down("extract")
        return sums(user)
    out = _rerun(conn, cid, extract=extract)
    after = _full(conn, cid)
    assert after["entry"]["e1"] == before["entry"]["e1"] and after["entry"]["e1"]["summary"]
    assert after["entry"]["e1"]["review_status"] == "accepted" and after["entry"]["e2"]["review_status"] == "dismissed"
    assert out["status"] == "done_with_errors"
    _, err = _err(conn, cid)
    assert err and err["code"] == "run_partial" and "1 " in err["message"]


def test_judge_down_rerun_keeps_judged_rows_instead_of_downgrading_them(tmp_path):
    conn, cid = _completed(tmp_path)
    before = _full(conn, cid)
    assert {r["state"] for r in before["entry"].values()} == {"verified"}
    out = _rerun(conn, cid, j1=_down("j1"), j2=_down("j2"), j3=_down("j3"), j4=_down("j4"))
    assert out["status"] == "done"
    assert _full(conn, cid) == before                      # verified stays verified with its stored judge answer
    c, err = _err(conn, cid)
    assert err and err["code"] == "run_partial" and "second" in err["message"].lower() and "kept" in err["message"]
    assert c["status"] == "failed"


def test_first_run_with_a_down_step_still_stores_its_stubs_and_is_not_marked_partial(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=_down("extract"))), now=lambda: 1.0)
    assert out["status"] == "done_with_errors"
    rows = DB.list_items(conn, cid, "entry")
    assert len(rows) == 9 and all(r["state"] == "rejected" and r["state_reasons"] == ["LLM_FAILED_AFTER_RETRIES"] for r in rows)
    c, err = _err(conn, cid)
    assert err is None and c["status"] == "ready"          # nothing earlier existed to keep


def test_a_later_good_rerun_replaces_the_kept_rows_and_clears_the_error(tmp_path):
    conn, cid = _completed(tmp_path)
    _rerun(conn, cid, extract=_down("extract"))
    out = _rerun(conn, cid)
    assert out["status"] == "done"
    c, err = _err(conn, cid)
    assert err is None and c["status"] == "ready"
    assert DB.get_item(conn, "e1")["review_status"] == "accepted"


def test_deadline_message_says_earlier_and_kept_and_not_finished_items(tmp_path):
    conn, cid = _completed(tmp_path)
    ticks = iter([0.0] + [10_000.0] * 5000)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: next(ticks), deadline_s=480)
    assert out["status"] == "timeout"
    _, err = _err(conn, cid)
    assert err["code"] == "run_deadline"
    assert "earlier" in err["message"] and "kept" in err["message"] and "decision" in err["message"] and "finished items" not in err["message"]


@pytest.mark.parametrize("jump_at", ["verify", "judge_entries", "amounts", "conflicts", "flags"])
def test_deadline_rerun_keeps_the_whole_stored_row_not_only_its_state(tmp_path, jump_at):
    """Full rows (summary, quote, offsets, ladder, state, status): a run stopped at `jump_at` has entries in hand, so a summary-wiping persist would show here."""
    conn, cid = _completed(tmp_path)
    before = _full(conn, cid)
    t = [0.0]

    def on_stage(name):
        if name == jump_at:
            t[0] = 10_000.0
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: t[0], on_stage=on_stage, deadline_s=480)
    assert out["status"] == "timeout"
    assert _full(conn, cid) == before
    assert before["entry"]["e1"]["summary"] and DB.get_item(conn, "e1")["summary"] == before["entry"]["e1"]["summary"]


def _model_flag(user):
    from tests.unit._fakes import which_record
    return {"flags": [dict(type="pre_existing", category="pre_existing", excerpt="CT head negative.")] if which_record(user)[0] == 2 else []}


def test_flag_step_down_rerun_keeps_the_model_flag_it_cannot_rediscover(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=_model_flag)), now=lambda: 1.0)
    assert DB.get_item(conn, "f_r2_1")["origin"] == "llm"
    before = _full(conn, cid, ("amount", "flag", "entry"))["flag"]["f_r2_1"]
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=_down("flags"))), now=lambda: 3.0)
    assert _full(conn, cid, ("amount", "flag", "entry"))["flag"]["f_r2_1"] == before         # not deleted as 'stale'
    _, err = _err(conn, cid)
    assert err and err["code"] == "run_partial" and "kept" in err["message"]


# ---- T-145 minor: a judge that was called and failed is not reported as 'did not run'
def test_a_failed_second_check_says_failed_and_keeps_the_reason_code(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(j1=_down("j1"))), now=lambda: 1.0)
    e = DB.get_item(conn, "e1")
    assert e["state"] == "needs_review" and e["state_reasons"] == ["JUDGE_UNAVAILABLE"]       # the reason code is unchanged
    assert e["ladder"]["judge"]["verdict"] == "unavailable" and e["ladder"]["judge"]["reason_code"] != "JUDGE_NOT_RUN"
    text = present.item_view(conn, cid, "e1")["why"]
    assert "second check failed" in text.lower() and "JUDGE_NOT_RUN" not in text
    assert "agreed" not in text


def test_a_second_check_that_never_ran_still_says_so_with_its_code(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    ticks = iter([0.0, 0.0, 0.0, 0.0] + [10_000.0] * 5000)       # the deadline passes before judge 1
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: next(ticks), deadline_s=480)
    rows = [r for r in DB.list_items(conn, cid, "entry") if r["state"] != "rejected"]
    if rows:
        assert all((r["ladder"].get("judge") or {}).get("reason_code") == "JUDGE_NOT_RUN" for r in rows)
        assert WHY.why("JUDGE_UNAVAILABLE").startswith("JUDGE_NOT_RUN:")


def test_why_helper_picks_the_sentence_from_the_judge_record():
    failed = {"verdict": "unavailable", "reason_code": "NONE", "call_id": None}
    notrun = {"verdict": "unavailable", "reason_code": "JUDGE_NOT_RUN"}
    assert "second check failed" in WHY.why("JUDGE_UNAVAILABLE", failed).lower() and "JUDGE_NOT_RUN" not in WHY.why("JUDGE_UNAVAILABLE", failed)
    assert WHY.why("JUDGE_UNAVAILABLE", notrun).startswith("JUDGE_NOT_RUN:")
    assert WHY.why("JUDGE_UNAVAILABLE", None).startswith("JUDGE_NOT_RUN:")                  # no judge record = it did not run
    assert WHY.why("JUDGE_UNSURE", failed) == WHY.why("JUDGE_UNSURE")


def test_a_recorded_answer_miss_is_not_called_a_failed_check():
    failed = {"verdict": "unavailable", "reason_code": "NONE"}
    text = WHY.join(["JUDGE_UNAVAILABLE", "FIXTURE_MISS"], failed)
    assert text.startswith("JUDGE_NOT_RUN:") and "second check failed" not in text.lower()
 M app/backend/amounts.py
 M app/backend/case_extras.py
MM app/backend/flags.py
MM app/backend/pipeline.py
MM app/backend/present.py
 M app/backend/reclassify.py
 M app/backend/review.py
MM app/backend/why.py
 M app/frontend/api.js
 M app/frontend/app.js
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:05.534Z

**tool call — Bash**
````
{
 "command": "sed -n 395,520p app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T13:59:05.668Z

**tool result**
````
    def guard(name):
        nonlocal timed_out
        if timed_out or expired():
            timed_out = True
            return False
        set_stage(name)
        return True

    # 1-3: entries
    if guard("extract"):
        entries, rejected, failures = generator.extract_entries(recs, ing["groups"], call=call, case_text=text)
        for f in failures:
            rejected.append(generator.failure_entry(by_n[f["record_no"]], next(g for g in ing["groups"] if g[0] == f["record_no"]), f["failure"], f.get("detail")))   # never vanishes: tray item with the reason
            if f["failure"] != "SUMMARY_NOT_IN_QUOTE":      # D-054: a tray item, not an error (the model answered; code removed what the quote does not support)
                errors.append(_err("UNSUPPORTED_LANGUAGE" if f["failure"] == "UNSUPPORTED_LANGUAGE" else "LLM_FAILED_AFTER_RETRIES", "extract", f["record_no"],
                                   "FIXTURE_MISS" if f["failure"] == "FIXTURE_MISS" else None))
    if guard("verify"):
        pass                                    # grounding, token and qualifier checks ran inside extract_entries (code, same call per record)
    if guard("judge_entries") and entries:
        generator.judge_entries(entries, by_n, call=call, case_text=text)
    _mark_judge_not_run(entries, by_n)           # T-145: judge 1 did not run (deadline) -> never 'verified'
    for e in entries + rejected:
        e["ladder"]["backend"] = P.backend_name()
        e.pop("_stage", None)
    # 4: amounts (J2 on every dollar amount)
    final_amounts = code_amounts
    if guard("amounts"):
        dollars = [a for a in ing["amounts"]]
        verdicts = judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars],
                                        call=call, case_text=text)
        final_amounts = [_finish_amount(a, ing, verdicts.get(a["id"])) for a in dollars] + [_finish_amount(a, ing, None) for a in ing["damages"]]
    for a in final_amounts:
        a["entry_id"] = _entry_for(entries, a["record_nos"][0])
    # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T-094). No model search, so the candidate set cannot vary.
    llm_flags = []
    distinct = [by_n[g[0]] for g in ing["groups"] if by_n[g[0]].get("lang") != "other"]     # unsupported-language records are skipped (warning + error)
    conflicts_ran = guard("conflicts")
    if conflicts_ran:
        llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
    # 6: per-record flags (one call per distinct record) + J4
    if guard("flags"):
        year = _accident_year(recs)

        def one(r):
            if expired():                    # the deadline also applies inside the stage, record by record
                return r, None
            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
            per = list(ex.map(one, distinct))
        for r, fs in per:
            if fs is None or expired():
                timed_out = True
                continue
            fs = [f for f in fs if f["type"] != "record_warning"]          # stage 0 already made the record_warning flag
            for k, f in enumerate(fs, 1):
                f["id"] = f"f_r{r['n']}_{k}"
            llm_flags += FL.judge_flags(fs, call=call, case_text=text)
    # 7: finalize
    set_stage("finalize")
    for f in llm_flags:
        f.setdefault("record_nos", [f["record_no"]])
        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
        f["ladder"]["item_id"], f["ladder"]["backend"], f["ladder"]["state"] = f["id"], P.backend_name(), f["state"]
        f["ladder"]["code_checks"].setdefault("classified_by", "lexicon+llm")
        f.setdefault("review_status", "pending")
        f["origin"] = _ORIGIN.get(f["origin"], f["origin"])
        f.pop("record_no", None)
    flag_items = ing["flags"] + [_clean(f) for f in llm_flags if f["state"] != "rejected"]
    tray = [_clean(e) for e in rejected] + [_clean(f) for f in llm_flags if f["state"] == "rejected"]
    entries = [_clean(e) for e in entries]
    dated = sorted((e for e in entries if dated_cut(e)), key=lambda e: (e["date"], e["seq"]))
    undated = [e for e in entries if not dated_cut(e)]
    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
    flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
    final_amounts = [_clean(a) for a in final_amounts]
    damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
    from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
    now_t = clock()
    kept_e = _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out)
    for a in final_amounts:                     # an amount stays linked to the entry whose record failed this time (that entry's stored row was kept)
        if not a.get("entry_id"):
            a["entry_id"] = next((o["id"] for o, _ in kept_e if f"r{a['record_nos'][0]}" in (o["record_ids"] or [])), None)
    kept_a = _persist(conn, cid, "amount", final_amounts, now_t, additive=timed_out)
    kept_f = _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t, additive=timed_out,
                      prune=not ({"flags", "conflicts"} & set(failed_steps)))
    kept_n = len(kept_e) + len(kept_a) + len(kept_f)
    _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
    if timed_out:
        status = "timeout"
        err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    else:
        status = "done_with_errors" if errors else "done"
        err = None
        if kept_n:      # T-146 r2: an AI step failed on a re-run and its earlier results were kept; the case says so instead of reading 'ready'
            what = " and ".join(sorted({c for _, c in kept_e + kept_a + kept_f}))
            err = {"code": "run_partial", "message": f"The AI step failed for {kept_n} item{'s' if kept_n != 1 else ''} ({what}) on this run. Their earlier results and every "
                                                      "decision of yours were kept unchanged. Run it again to retry."}
    DB.update_case(conn, cid, status="failed" if (timed_out or err) else "ready", stage="finalize", error=json.dumps(err) if err else None,
                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
    tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
    all_items = dated + undated + final_amounts + flag_items
    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
            "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
            "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
                       "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
                       "verified": sum(1 for i in all_items if i["state"] == "verified")}}


# ------------------------------------------------------------------ eval / API view
def case_view(out: dict) -> dict:
    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
    flags = []
    for f in out["flags"] + out["tray"]:
        if "summary" in f:
            continue
        g = dict(f)
        g["evidence"] = [{**e, "record_id": f"r{e['record_no']}", "excerpt": e.get("text")} for e in f.get("evidence", [])]
        if f["type"] == "gap":
            g["computed"] = {"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}
        flags.append(g)
    return {"records": out["records"], "entries": out["entries"], "undated_entries": out["undated_entries"],
            "amounts": [{**a, "value_cents": a["cents"], "kind": a["cls"]} for a in out["amounts"] + out["damages"]],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:42.848Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cd $S/arc && ls; git -C /Users/arsis/zlayt-pm-project ls-files | grep -c '' ; (/Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider -x -q 2>&1 | tail -15) ",
 "timeout": 600000
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:43.526Z

**tool call — Bash**
````
{
 "command": "grep -rn \"run_deadline\\|run_partial\\|RUN_FAILED\" app --include=*.py --include=*.js | grep -v \"^app/backend/pipeline.py\" | head -30"
}
````

### User / tool · 2026-11-02T14:05:51.382Z

**tool result**
````
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
2176
..............ss........................................................ [ 75%]
........................................................................ [ 77%]
........................................................................ [ 79%]
........................................................................ [ 81%]
........................................................................ [ 83%]
........................................................................ [ 84%]
........................................................................ [ 86%]
........................................................................ [ 88%]
...................................................................ss... [ 90%]
........................................................................ [ 92%]
........................................................................ [ 94%]
........................................................................ [ 95%]
........................................................................ [ 97%]
........................................................................ [ 99%]
.............                                                            [100%]
````

### User / tool · 2026-11-02T14:05:51.628Z

**tool result**
````
app/backend/trace.py:48:    "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
app/backend/trace.py:1133:        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
app/backend/conflict_candidates.py:280:            skip(t, "RUN_FAILED", "The run stopped before this check finished, so nothing is known about it.")
app/backend/conflict_candidates.py:285:                skip(t, "RUN_FAILED", "The run stopped before the comparison between records finished.")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:06:00.481Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cd $S/arc && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -4; sed -n 1120,1140p app/backend/trace.py; sed -n 40,52p app/backend/trace.py",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:13:24.276Z

**tool result**
````
........................................................................ [ 97%]
........................................................................ [ 99%]
.............                                                            [100%]
3893 passed, 8 skipped in 441.20s (0:07:21)
    return (f"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm {'them' if n != 1 else 'it'}), so {'they are' if n != 1 else 'it is'} "
            f"not in the letter and {'are' if n != 1 else 'is'} not counted as accepted until you compare {'them' if n != 1 else 'it'} with the quote and accept.")


def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
    cx = cx or _Cx(conn, case_id, False)
    rv = rv or present.review_view(conn, case_id)
    out = []
    if cx.running:
        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
    if cx.case["status"] == "failed":
        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
    out.extend(code_check_blockers(conn, case_id, cx))         # D-045(b): the paralegal's own wording is exempt from the judge, not from the code checks
    if cx.ran and not cx.running:
        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
    if not (rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0)):       # T-134: an edit not yet accepted is not accepted
        out.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": TRACE_WHY["NOTHING_ACCEPTED"], "next_action": na("DECIDE", {"view": "queue"})})
    return out

TRACE_WHY = {
    "PENDING_DECISION": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
    "DATE_UNCONFIRMED": "This entry's date is not confirmed, so it cannot be accepted into the letter yet.",
    "EDIT_NOT_CONFIRMED_ITEM": "You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.",
    "EDIT_NOT_CONFIRMED_ITEM_AI": "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.",
    "EDIT_NOT_CONFIRMED": "An edited entry is still marked Needs review; it stays out of the letter until you compare it with the quote and accept it.",
    "ITEMS_NOT_REVIEWED": "Some items have no decision yet; they will not be in the letter and the AI disclosure line counts them.",
    "RUN_IN_PROGRESS": "The AI run is still going.",
    "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
    "NOTHING_ACCEPTED": "Nothing is accepted or edited yet, so the letter would be empty.",
    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
    "JUDGE_NOT_RUN_RETRIED": "You accepted this item, but the second AI check ran again and still gave no answer. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it. It clears when the check answers, or when you edit the summary in your own words.",
    "CODE_CHECK_FAILED_AI": "This summary was drafted by the AI and a code check on it fails, so it cannot go into the letter until the summary matches the quote.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:13:37.799Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; mkdir -p $S/probes; cat > $S/probes/p1.py <<'EOF'\nimport sys, json, tempfile, os\nARC = sys.argv[1]; sys.path.insert(0, ARC); os.chdir(ARC)\nfrom app.backend import pipeline as PL, present, trace\nfrom app.db import db as DB\nfrom app.llm import audited as AU\nfrom tests.unit import _golden as G\nfrom tests.unit._fakes import FakeCall, sample_script\n\ndef snap(conn, cid):\n    return {k: {i[\"id\"]: {c: v for c, v in i.items() if c != \"updated_at\"} for i in DB.list_items(conn, cid, k)} for k in (\"entry\", \"amount\", \"flag\")}\ndef diff(a, b, label):\n    n = 0\n    for k in a:\n        ids = set(a[k]) | set(b[k])\n        for i in sorted(ids):\n            if i not in b[k]: print(label, k, i, \"DELETED\"); n += 1; continue\n            if i not in a[k]: print(label, k, i, \"ADDED\"); n += 1; continue\n            ch = [c for c in a[k][i] if a[k][i][c] != b[k][i].get(c)]\n            if ch: print(label, k, i, \"CHANGED\", ch); n += 1\n    print(label, \"total differing items:\", n, \"| counts\", {k: len(v) for k, v in b.items()})\ndef fresh():\n    d = tempfile.mkdtemp(); conn = DB.connect(os.path.join(d, \"d.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\n    r = PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script()), now=lambda: 1.0); assert r[\"status\"] == \"done\", r[\"status\"]\n    DB.apply_review(conn, \"e1\", \"accept\", now=2.0, case=cid); DB.apply_review(conn, \"e2\", \"dismiss\", now=2.0, case=cid); DB.apply_review(conn, \"a1\", \"accept\", now=2.0, case=cid)\n    return conn, cid\ndef rerun(conn, cid, **kw):\n    return PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(**kw)), now=lambda: 3.0)\ndef report(conn, cid, out, label):\n    c = DB.get_case(conn, cid)\n    print(label, \"run status\", out[\"status\"], \"| case\", c[\"status\"], \"| error\", c[\"error\"])\n    print(label, \"e1\", {k: (DB.get_item(conn, \"e1\")[k] if k != \"summary\" else (DB.get_item(conn,\"e1\")[k] or \"\")[:40]) for k in (\"state\",\"state_reasons\",\"review_status\")})\n    print(label, \"blockers\", [(b[\"item_id\"], b[\"reason_code\"]) for b in trace.export_blockers(conn, cid)])\n\nLF = lambda s: AU.LLMFailed(f\"{s} down\", last_error=\"TIMEOUT\")\ncases = {\n \"R1-extract-down\": dict(extract=LF(\"extract\")),\n \"judge-down(j1,j2)\": dict(j1=LF(\"j1\"), j2=LF(\"j2\")),\n \"judge-down(all4)\": dict(j1=LF(\"j1\"), j2=LF(\"j2\"), j3=LF(\"j3\"), j4=LF(\"j4\")),\n \"conflicts-down\": dict(conflicts=LF(\"conflicts\")),\n \"flags-down\": dict(flags=LF(\"flags\")),\n}\nfor name, kw in cases.items():\n    conn, cid = fresh(); before = snap(conn, cid)\n    try:\n        out = rerun(conn, cid, **kw)\n    except Exception as e:\n        print(name, \"EXC\", repr(e)); continue\n    report(conn, cid, out, name); diff(before, snap(conn, cid), name); print()\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p1.py $S/arc 2>&1 | tail -60; grep -n \"def sample_script\" -A40 $S/arc/tests/unit/_fakes.py | head -70",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:13:40.643Z

**tool result**
````
R1-extract-down run status done_with_errors | case failed | error {"code": "run_partial", "message": "The AI step failed for 9 items (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."}
R1-extract-down e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
R1-extract-down blockers [(None, 'RUN_FAILED')]
R1-extract-down amount a1 CHANGED ['ladder']
R1-extract-down amount a2 CHANGED ['ladder']
R1-extract-down amount a4 CHANGED ['ladder']
R1-extract-down flag f_cx1 CHANGED ['ladder']
R1-extract-down total differing items: 4 | counts {'entry': 9, 'amount': 4, 'flag': 10}

judge-down(j1,j2) run status done | case failed | error {"code": "run_partial", "message": "The AI step failed for 12 items (the second check) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."}
judge-down(j1,j2) e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
judge-down(j1,j2) blockers [(None, 'RUN_FAILED')]
judge-down(j1,j2) total differing items: 0 | counts {'entry': 9, 'amount': 4, 'flag': 10}

judge-down(all4) run status done | case failed | error {"code": "run_partial", "message": "The AI step failed for 13 items (the second check) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."}
judge-down(all4) e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
judge-down(all4) blockers [(None, 'RUN_FAILED')]
judge-down(all4) total differing items: 0 | counts {'entry': 9, 'amount': 4, 'flag': 10}

conflicts-down run status done | case ready | error None
conflicts-down e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
conflicts-down blockers []
conflicts-down entry e2 CHANGED ['ladder']
conflicts-down entry e4 CHANGED ['ladder']
conflicts-down entry e5 CHANGED ['ladder']
conflicts-down entry e6 CHANGED ['ladder']
conflicts-down entry e7 CHANGED ['ladder']
conflicts-down entry e8 CHANGED ['ladder']
conflicts-down total differing items: 6 | counts {'entry': 9, 'amount': 4, 'flag': 10}

flags-down run status done | case ready | error None
flags-down e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
flags-down blockers []
flags-down entry e2 CHANGED ['ladder']
flags-down entry e4 CHANGED ['ladder']
flags-down entry e6 CHANGED ['ladder']
flags-down flag f_r3_1 CHANGED ['state_reasons']
flags-down flag f_r6_1 CHANGED ['state_reasons']
flags-down flag f_r7_1 CHANGED ['state_reasons']
flags-down flag f_r7_2 CHANGED ['state_reasons']
flags-down flag f_r8_1 CHANGED ['state_reasons']
flags-down flag f_r8_2 CHANGED ['state_reasons']
flags-down flag f_r9_1 CHANGED ['state_reasons']
flags-down total differing items: 10 | counts {'entry': 9, 'amount': 4, 'flag': 10}

42:def sample_script(**over):
43-    """Happy-path script for the sample case (extract returns the golden summary and quote; judges agree; no LLM flags). `over` replaces steps."""
44-    sums = golden_summaries()
45-    def extract(user):
46-        n = which_record(user)[0]
47-        return dict(summary=sums[n][0], excerpt=sums[n][1])
48-    sc = {"extract": extract, "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"},
49-          "j3": {"verdict": "conflict", "reason_code": "NONE"}, "j4": {"verdict": "agree", "reason_code": "NONE"},
50-          "conflicts": {"flags": []}, "flags": {"flags": []}}
51-    sc.update(over)
52-    return sc
53-
54-def run_sample(tmp_path, case="sample", call=None, now=lambda: 1.0, **kw):
55-    """Run the whole pipeline on a golden case with a FakeCall; returns (output, call). Pipeline output keys used by tests:
56-    entries, amounts, flags, tray (rejected attempts), errors [{code, ...}], status, warnings."""
57-    from app.backend import pipeline as PL
58-    from app.db import db as DB
59-    conn = DB.connect(str(tmp_path / f"{case}-{next(_RUNS)}.sqlite"))
60-    cid = DB.create_case(conn, G.raw(case), now=1.0)
61-    call = call or FakeCall(sample_script())
62-    return PL.run_pipeline(conn, cid, G.raw(case), call=call, now=now, **kw), call
63-
64-def items_for(out, n):
65-    """Every entry-like item (timeline, undated, tray) that cites record number n."""
66-    rid = f"r{n}"
67-    pool = list(out.get("entries", [])) + list(out.get("undated_entries", [])) + list(out.get("tray", []))
68-    return [i for i in pool if rid in i.get("record_ids", [])]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:13:52.832Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cat > $S/probes/p2.py <<'EOF'\nimport sys; sys.argv=[sys.argv[0], sys.argv[1]]\nexec(open(sys.argv[0].replace(\"p2.py\",\"p1.py\")).read().split(\"LF = lambda\")[0])\nLF = lambda s: AU.LLMFailed(f\"{s} down\", last_error=\"TIMEOUT\")\nconn, cid = fresh(); before = snap(conn, cid)\nfor fid in (\"f_r3_1\",\"f_r7_1\"):\n    b = before[\"flag\"][fid]; print(\"BEFORE\", fid, b[\"state\"], b[\"state_reasons\"], b[\"review_status\"], b[\"origin\"], (b[\"ladder\"] or {}).get(\"judge\"))\nout = rerun(conn, cid, flags=LF(\"flags\")); after = snap(conn, cid)\nfor fid in (\"f_r3_1\",\"f_r7_1\"):\n    b = after[\"flag\"][fid]; print(\"AFTER \", fid, b[\"state\"], b[\"state_reasons\"], b[\"review_status\"], b[\"origin\"])\nprint(out[\"errors\"])\nc = DB.get_case(conn, cid); print(c[\"status\"], c[\"error\"])\nprint(present.item_view(conn, cid, \"f_r3_1\")[\"why\"])\n# decided flag: accept a flag then rerun\nconn, cid = fresh(); DB.apply_review(conn, \"f_r3_1\", \"accept\", now=2.0, case=cid); b = snap(conn, cid)\nout = rerun(conn, cid, flags=LF(\"flags\")); a = snap(conn, cid); diff(b, a, \"flags-down-after-accept-f_r3_1\")\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p2.py $S/arc 2>&1 | tail -30",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T14:13:54.561Z

**tool result**
````
BEFORE f_r3_1 needs_review ['LEXICON_ONLY'] pending lexicon None
BEFORE f_r7_1 needs_review ['LEXICON_ONLY'] pending lexicon None
AFTER  f_r3_1 needs_review ['LLM_FAILED_AFTER_RETRIES'] pending lexicon
AFTER  f_r7_1 needs_review ['LLM_FAILED_AFTER_RETRIES'] pending lexicon
[]
ready None
The AI step failed on all three attempts, so this record has no AI-made entry.
flags-down-after-accept-f_r3_1 entry e1 CHANGED ['ladder']
flags-down-after-accept-f_r3_1 entry e2 CHANGED ['ladder']
flags-down-after-accept-f_r3_1 entry e5 CHANGED ['ladder']
flags-down-after-accept-f_r3_1 entry e6 CHANGED ['ladder']
flags-down-after-accept-f_r3_1 entry e7 CHANGED ['ladder']
flags-down-after-accept-f_r3_1 entry e8 CHANGED ['ladder']
flags-down-after-accept-f_r3_1 flag f_r3_1 CHANGED ['state_reasons']
flags-down-after-accept-f_r3_1 flag f_r6_1 CHANGED ['state_reasons']
flags-down-after-accept-f_r3_1 flag f_r7_1 CHANGED ['state_reasons']
flags-down-after-accept-f_r3_1 flag f_r7_2 CHANGED ['state_reasons']
flags-down-after-accept-f_r3_1 flag f_r8_1 CHANGED ['state_reasons']
flags-down-after-accept-f_r3_1 flag f_r8_2 CHANGED ['state_reasons']
flags-down-after-accept-f_r3_1 flag f_r9_1 CHANGED ['state_reasons']
flags-down-after-accept-f_r3_1 total differing items: 13 | counts {'entry': 9, 'amount': 4, 'flag': 10}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:14:09.634Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cat > $S/probes/p3.py <<'EOF'\nimport sys\nexec(open(sys.argv[0].replace(\"p3.py\",\"p1.py\")).read().split(\"LF = lambda\")[0])\nLF = lambda s: AU.LLMFailed(f\"{s} down\", last_error=\"TIMEOUT\")\nconn, cid = fresh()\nfor f in DB.list_items(conn, cid, \"flag\"):\n    print(f[\"id\"], f[\"state\"], f[\"state_reasons\"], f[\"origin\"], f.get(\"type\") or f.get(\"flag_type\"), (f.get(\"summary\") or \"\")[:50], \"|\", [k for k in f if k in (\"category\",\"excerpt\",\"evidence\")])\nprint(DB.get_item(conn,\"f_r3_1\").keys())\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p3.py $S/arc 2>&1 | tail -30; grep -n \"def which_record\" -A12 $S/arc/tests/unit/_fakes.py",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T14:14:10.532Z

**tool result**
````
f_gap_r6_r7 verified [] code gap  | ['category', 'evidence']
f_accident_date_after_treatment_1_2_7 verified [] code conflict  | ['category', 'evidence']
f_cx1 verified [] code conflict  | ['category', 'evidence']
f_r3_1 needs_review ['LEXICON_ONLY'] lexicon pre_existing  | ['category', 'evidence']
f_r8_1 needs_review ['LEXICON_ONLY'] lexicon pre_existing  | ['category', 'evidence']
f_r6_1 needs_review ['LEXICON_ONLY'] lexicon causation  | ['category', 'evidence']
f_r7_1 needs_review ['LEXICON_ONLY'] lexicon causation  | ['category', 'evidence']
f_r7_2 needs_review ['LEXICON_ONLY'] lexicon causation  | ['category', 'evidence']
f_r8_2 needs_review ['LEXICON_ONLY'] lexicon causation  | ['category', 'evidence']
f_r9_1 needs_review ['LEXICON_ONLY'] lexicon causation  | ['category', 'evidence']
dict_keys(['id', 'case_id', 'type', 'category', 'source_kind', 'title', 'explanation', 'computed', 'evidence', 'origin', 'reviewer_note', 'state', 'state_reasons', 'review_status', 'edited', 'ladder', 'updated_at'])
37:def which_record(user, case="sample"):
38-    """Record numbers whose excerpt appears in the prompt text."""
39-    return [r["n"] for r in G.records(case) if r["excerpt"] in user or r["excerpt"][:40] in user]
40-
41-
42-def sample_script(**over):
43-    """Happy-path script for the sample case (extract returns the golden summary and quote; judges agree; no LLM flags). `over` replaces steps."""
44-    sums = golden_summaries()
45-    def extract(user):
46-        n = which_record(user)[0]
47-        return dict(summary=sums[n][0], excerpt=sums[n][1])
48-    sc = {"extract": extract, "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"},
49-          "j3": {"verdict": "conflict", "reason_code": "NONE"}, "j4": {"verdict": "agree", "reason_code": "NONE"},
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:14:19.849Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cat > $S/probes/p4.py <<'EOF'\nimport sys\nexec(open(sys.argv[0].replace(\"p4.py\",\"p1.py\")).read().split(\"LF = lambda\")[0])\nfrom tests.unit._fakes import which_record\nLF = lambda s: AU.LLMFailed(f\"{s} down\", last_error=\"TIMEOUT\")\nconn, cid = fresh()\nf = DB.get_item(conn, \"f_r3_1\"); print(f[\"evidence\"], f[\"category\"], f[\"type\"])\nev = f[\"evidence\"][0]; ex = ev.get(\"text\") or ev.get(\"excerpt\")\ndef mf(user):\n    return {\"flags\": [dict(type=\"pre_existing\", category=f[\"category\"], excerpt=ex)] if which_record(user)[0] == 3 else []}\nd = tempfile.mkdtemp(); conn = DB.connect(os.path.join(d, \"d.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\nPL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(flags=mf)), now=lambda: 1.0)\nfor x in DB.list_items(conn, cid, \"flag\"):\n    if \"r3\" in x[\"id\"]: print(\"COMPLETE\", x[\"id\"], x[\"state\"], x[\"state_reasons\"], x[\"origin\"])\nDB.apply_review(conn, \"f_r3_1\", \"accept\", now=2.0, case=cid)\nb = snap(conn, cid)\nout = rerun(conn, cid, flags=LF(\"flags\")); \nc = DB.get_case(conn, cid); print(\"case\", c[\"status\"], c[\"error\"], out[\"status\"], out[\"errors\"])\nfor x in DB.list_items(conn, cid, \"flag\"):\n    if \"r3\" in x[\"id\"]: print(\"AFTER\", x[\"id\"], x[\"state\"], x[\"state_reasons\"], x[\"origin\"], x[\"review_status\"])\ndiff(b, snap(conn, cid), \"flags-down-verified-flag\")\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p4.py $S/arc 2>&1 | grep -v \"entry e\" | tail -30",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T14:14:20.913Z

**tool result**
````
[{'end': 772, 'record_no': 3, 'start': 724, 'text': 'Patient reports low back pain in 2023, resolved.'}] pre_existing pre_existing
COMPLETE f_r3_1 verified [] lexicon+llm
case ready None done []
AFTER f_r3_1 needs_review ['LLM_FAILED_AFTER_RETRIES'] lexicon accepted
flags-down-verified-flag flag f_r3_1 CHANGED ['origin', 'state', 'state_reasons', 'ladder']
flags-down-verified-flag flag f_r6_1 CHANGED ['state_reasons']
flags-down-verified-flag flag f_r7_1 CHANGED ['state_reasons']
flags-down-verified-flag flag f_r7_2 CHANGED ['state_reasons']
flags-down-verified-flag flag f_r8_1 CHANGED ['state_reasons']
flags-down-verified-flag flag f_r8_2 CHANGED ['state_reasons']
flags-down-verified-flag flag f_r9_1 CHANGED ['state_reasons']
flags-down-verified-flag total differing items: 13 | counts {'entry': 9, 'amount': 4, 'flag': 10}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:14:39.706Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cat > $S/probes/p5.py <<'EOF'\nimport sys\nexec(open(sys.argv[0].replace(\"p5.py\",\"p1.py\")).read().split(\"LF = lambda\")[0])\nfrom tests.unit._fakes import which_record\nfrom app.llm import provider as P\nLF = lambda s: AU.LLMFailed(f\"{s} down\", last_error=\"TIMEOUT\")\nbase = sample_script()[\"extract\"]\ndef only_rec(n, fn):\n    def ex(user):\n        if which_record(user)[0] == n: return fn(user)\n        return base(user)\n    return ex\ncases = {\n \"extract-e1-summary-not-in-quote\": only_rec(1, lambda u: dict(summary=\"Patient had a skull fracture of 99 cm.\", excerpt=base(u)[\"excerpt\"])),\n \"extract-e1-schema-invalid\": only_rec(1, lambda u: {\"summary\": 5}),\n \"extract-e1-llmfailed\": only_rec(1, lambda u: (_ for _ in ()).throw(LF(\"extract\"))),\n \"extract-e1-fixturemiss\": only_rec(1, lambda u: (_ for _ in ()).throw(P.FixtureMiss(\"x\"))) ,\n}\nfor name, ex in cases.items():\n    conn, cid = fresh(); before = snap(conn, cid)\n    try: out = rerun(conn, cid, extract=ex)\n    except Exception as e: print(name, \"EXC\", repr(e)); continue\n    report(conn, cid, out, name); diff(before, snap(conn, cid), name); print()\n# partial judge: j1 fails only for record 1\nj1 = sample_script()[\"j1\"]\ndef j1f(user):\n    if which_record(user) and which_record(user)[0] == 1: raise LF(\"j1\")\n    return j1\nconn, cid = fresh(); before = snap(conn, cid)\nout = rerun(conn, cid, j1=j1f); report(conn, cid, out, \"j1-e1-only\"); diff(before, snap(conn, cid), \"j1-e1-only\")\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p5.py $S/arc 2>&1 | grep -v \" ladder\\]$\" | tail -50",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:14:41.403Z

**tool result**
````
extract-e1-schema-invalid amount a2 CHANGED ['ladder']
extract-e1-schema-invalid amount a4 CHANGED ['ladder']
extract-e1-schema-invalid flag f_cx1 CHANGED ['ladder']
extract-e1-schema-invalid total differing items: 12 | counts {'entry': 9, 'amount': 4, 'flag': 10}

extract-e1-llmfailed run status done_with_errors | case failed | error {"code": "run_partial", "message": "The AI step failed for 1 item (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."}
extract-e1-llmfailed e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
extract-e1-llmfailed blockers [(None, 'RUN_FAILED')]
extract-e1-llmfailed entry e2 CHANGED ['ladder']
extract-e1-llmfailed entry e3 CHANGED ['ladder']
extract-e1-llmfailed entry e4 CHANGED ['ladder']
extract-e1-llmfailed entry e5 CHANGED ['ladder']
extract-e1-llmfailed entry e6 CHANGED ['ladder']
extract-e1-llmfailed entry e7 CHANGED ['ladder']
extract-e1-llmfailed entry e8 CHANGED ['ladder']
extract-e1-llmfailed entry e9 CHANGED ['ladder']
extract-e1-llmfailed amount a1 CHANGED ['ladder']
extract-e1-llmfailed amount a2 CHANGED ['ladder']
extract-e1-llmfailed amount a4 CHANGED ['ladder']
extract-e1-llmfailed flag f_cx1 CHANGED ['ladder']
extract-e1-llmfailed total differing items: 12 | counts {'entry': 9, 'amount': 4, 'flag': 10}

extract-e1-fixturemiss run status done_with_errors | case failed | error {"code": "run_partial", "message": "The AI step failed for 1 item (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."}
extract-e1-fixturemiss e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
extract-e1-fixturemiss blockers [(None, 'RUN_FAILED')]
extract-e1-fixturemiss entry e2 CHANGED ['ladder']
extract-e1-fixturemiss entry e3 CHANGED ['ladder']
extract-e1-fixturemiss entry e4 CHANGED ['ladder']
extract-e1-fixturemiss entry e5 CHANGED ['ladder']
extract-e1-fixturemiss entry e6 CHANGED ['ladder']
extract-e1-fixturemiss entry e7 CHANGED ['ladder']
extract-e1-fixturemiss entry e8 CHANGED ['ladder']
extract-e1-fixturemiss entry e9 CHANGED ['ladder']
extract-e1-fixturemiss amount a1 CHANGED ['ladder']
extract-e1-fixturemiss amount a2 CHANGED ['ladder']
extract-e1-fixturemiss amount a4 CHANGED ['ladder']
extract-e1-fixturemiss flag f_cx1 CHANGED ['ladder']
extract-e1-fixturemiss total differing items: 12 | counts {'entry': 9, 'amount': 4, 'flag': 10}

j1-e1-only run status done | case failed | error {"code": "run_partial", "message": "The AI step failed for 1 item (the second check) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."}
j1-e1-only e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
j1-e1-only blockers [(None, 'RUN_FAILED')]
j1-e1-only entry e2 CHANGED ['ladder']
j1-e1-only entry e3 CHANGED ['ladder']
j1-e1-only entry e4 CHANGED ['ladder']
j1-e1-only entry e5 CHANGED ['ladder']
j1-e1-only entry e6 CHANGED ['ladder']
j1-e1-only entry e7 CHANGED ['ladder']
j1-e1-only entry e8 CHANGED ['ladder']
j1-e1-only total differing items: 7 | counts {'entry': 9, 'amount': 4, 'flag': 10}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:14:48.190Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p5.py $S/arc 2>&1 | grep -v \"CHANGED \\['ladder'\\]$\" | head -20\ncat >> $S/probes/p5.py <<'EOF'\n\n# ladder-only diffs: what differs?\nconn, cid = fresh(); b = snap(conn, cid); rerun(conn, cid, j1=j1f); a = snap(conn, cid)\ndef flat(d, p=\"\"):\n    o = {}\n    for k, v in (d.items() if isinstance(d, dict) else enumerate(d)):\n        if isinstance(v, (dict, list)): o.update(flat(v, f\"{p}.{k}\"))\n        else: o[f\"{p}.{k}\"] = v\n    return o\nfb, fa = flat(b[\"entry\"][\"e2\"][\"ladder\"]), flat(a[\"entry\"][\"e2\"][\"ladder\"])\nprint(\"e2 ladder diff keys:\", {k: (fb.get(k), fa.get(k)) for k in set(fb)|set(fa) if fb.get(k) != fa.get(k)})\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p5.py $S/arc 2>&1 | tail -1",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:14:51.504Z

**tool result**
````
extract-e1-summary-not-in-quote run status done | case ready | error None
extract-e1-summary-not-in-quote e1 {'state': 'rejected', 'state_reasons': ['SUMMARY_NOT_IN_QUOTE'], 'review_status': 'accepted'}
extract-e1-summary-not-in-quote blockers []
extract-e1-summary-not-in-quote entry e1 CHANGED ['summary', 'excerpt', 'excerpt_start', 'excerpt_end', 'state', 'state_reasons', 'ladder']
extract-e1-summary-not-in-quote total differing items: 13 | counts {'entry': 9, 'amount': 4, 'flag': 10}

extract-e1-schema-invalid run status done | case failed | error {"code": "run_partial", "message": "The AI step failed for 1 item (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."}
extract-e1-schema-invalid e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
extract-e1-schema-invalid blockers [(None, 'RUN_FAILED')]
extract-e1-schema-invalid total differing items: 12 | counts {'entry': 9, 'amount': 4, 'flag': 10}

extract-e1-llmfailed run status done_with_errors | case failed | error {"code": "run_partial", "message": "The AI step failed for 1 item (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."}
extract-e1-llmfailed e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
extract-e1-llmfailed blockers [(None, 'RUN_FAILED')]
extract-e1-llmfailed total differing items: 12 | counts {'entry': 9, 'amount': 4, 'flag': 10}

extract-e1-fixturemiss run status done_with_errors | case failed | error {"code": "run_partial", "message": "The AI step failed for 1 item (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."}
extract-e1-fixturemiss e1 {'state': 'verified', 'state_reasons': [], 'review_status': 'accepted'}
extract-e1-fixturemiss blockers [(None, 'RUN_FAILED')]
extract-e1-fixturemiss total differing items: 12 | counts {'entry': 9, 'amount': 4, 'flag': 10}
e2 ladder diff keys: {'.generator.call_id': ('call3', 'call2'), '.judge.call_id': ('call11', 'call13')}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:15:02.593Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cd $S/arc && grep -n \"def export_case\\|def build_export\" -r app/backend | head; cat > $S/probes/p6.py <<'EOF'\nimport sys\nexec(open(sys.argv[0].replace(\"p6.py\",\"p1.py\")).read().split(\"LF = lambda\")[0])\nfrom tests.unit._fakes import which_record\nbase = sample_script()[\"extract\"]\ndef ex(user):\n    if which_record(user)[0] == 1: return dict(summary=\"Patient had a skull fracture of 99 cm.\", excerpt=base(user)[\"excerpt\"])\n    return base(user)\nconn, cid = fresh()\nout = rerun(conn, cid, extract=ex)\ne = DB.get_item(conn, \"e1\"); print({k: e[k] for k in (\"summary\",\"excerpt\",\"state\",\"state_reasons\",\"review_status\")})\nrv = present.review_view(conn, cid); print(\"counts\", rv[\"counts\"])\nfrom app.backend import store\ntry:\n    ex_ = store.export_case(conn, cid) if hasattr(store, \"export_case\") else None\n    print(type(ex_), str(ex_)[:600])\nexcept Exception as err: print(\"EXPORT EXC\", repr(err))\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p6.py $S/arc 2>&1 | tail -12",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T14:15:03.562Z

**tool result**
````
app/backend/store.py:36:def export_case(conn, case_id: str) -> dict:
app/backend/export.py:691:def build_export(case: dict, style: str = None) -> dict:
{'summary': None, 'excerpt': None, 'state': 'rejected', 'state_reasons': ['SUMMARY_NOT_IN_QUOTE'], 'review_status': 'accepted'}
counts {'pending': 20, 'accepted': 1, 'edited': 0, 'dismissed': 1, 'needs_review': 9, 'verified': 13, 'rejected': 1, 'edit_to_check': 0}
<class 'dict'> {'records': [{'n': 1, 'source': 'Austin EMS run report', 'date_iso': '2026-01-09', 'excerpt': '41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.'}, {'n': 2, 'source': 'Central ER discharge summary', 'date_iso': '2026-01-09', 'excerpt': 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.'}, {'n': 3, 'source': 'Dr. Alvarez, primary care', 'date_iso': '2026-01-16', 'excerpt': 'Persistent neck pain 6/10, daily h
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:15:09.367Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cat >> $S/probes/p6.py <<'EOF'\nprint([ (k, (len(v) if hasattr(v,'__len__') else v)) for k,v in ex_.items()])\nprint(\"entries:\", [(x.get(\"id\"), x.get(\"summary\")) for x in ex_.get(\"entries\", [])])\nprint(\"excluded:\", ex_.get(\"excluded\"))\nprint(\"blockers:\", trace.export_blockers(conn, cid))\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p6.py $S/arc 2>&1 | tail -5 | cut -c1-900",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T14:15:10.287Z

**tool result**
````
<class 'dict'> {'records': [{'n': 1, 'source': 'Austin EMS run report', 'date_iso': '2026-01-09', 'excerpt': '41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.'}, {'n': 2, 'source': 'Central ER discharge summary', 'date_iso': '2026-01-09', 'excerpt': 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.'}, {'n': 3, 'source': 'Dr. Alvarez, primary care', 'date_iso': '2026-01-16', 'excerpt': 'Persistent neck pain 6/10, daily h
[('records', 9), ('entries', 8), ('amounts', 4), ('flags', 10), ('pending_count', 20), ('events', 0), ('export_blockers', 0), ('judge_not_run', 0)]
entries: [('e2', 'Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.'), ('e3', 'Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.'), ('e4', 'Cervical range of motion reduced approx. 40%; plan of care 12 visits.'), ('e5', 'Pain 4/10, improving.'), ('e6', 'Discharged from physical therapy after two missed appointments; pain 3/10.'), ('e7', 'New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.'), ('e8', 'C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.'), ('e9', 'Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.')]
excluded: None
blockers: []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:15:35.045Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cd $S/arc && ls tests/unit | grep -i \"t145\\|t146\"; grep -ln \"second check failed\\|JUDGE_NOT_RUN\" tests/unit/*.py | head -20"
}
````

### User / tool · 2026-11-02T14:15:35.238Z

**tool result**
````
test_t145_judge_not_run.py
test_t146_r2_failed_rerun_keeps_items.py
test_t146_rerun_keeps_items.py
tests/unit/test_export.py
tests/unit/test_t114_rates_and_demo_judges.py
tests/unit/test_t138_undo_edit.py
tests/unit/test_t145_judge_not_run.py
tests/unit/test_t139_narrow.py
tests/unit/test_t146_r2_failed_rerun_keeps_items.py
tests/unit/test_trace.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:15:49.621Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cat > $S/probes/mut.py <<'EOF'\nimport sys, os, shutil, subprocess\nS, ARC = sys.argv[1], sys.argv[2]\nM = os.path.join(S, \"arcm\")\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nmuts = [\n (\"M1 _degrades always None\", \"app/backend/pipeline.py\", '    if kind == \"entry\" and it.get(\"state\") == \"rejected\" and set(it.get(\"reasons\") or []) & _STUB_REASONS and old.get(\"summary\") and old.get(\"excerpt\"):\\n        return \"writing the entries\"', '    if False:\\n        return \"writing the entries\"'),\n (\"M1b judge arm off\", \"app/backend/pipeline.py\", 'return \"the second check\" if new_j.get(\"verdict\") == \"unavailable\" and old_j.get(\"verdict\") not in (None, \"unavailable\") else None', 'return None'),\n (\"M3 prune ignored\", \"app/backend/pipeline.py\", \"            if not prune:\\n\", \"            if False:\\n\"),\n (\"M5 entry_id backfill off\", \"app/backend/pipeline.py\", \"        if not a.get(\\\"entry_id\\\"):\\n            a[\\\"entry_id\\\"] = next(\", \"        if False:\\n            a[\\\"entry_id\\\"] = next(\"),\n (\"M6 case status failed only on timeout\", \"app/backend/pipeline.py\", 'status=\"failed\" if (timed_out or err) else \"ready\"', 'status=\"failed\" if timed_out else \"ready\"'),\n (\"M7 run_partial error never set\", \"app/backend/pipeline.py\", \"        if kept_n:      # T-146 r2\", \"        if False:      # T-146 r2\"),\n (\"M8 count = entries only\", \"app/backend/pipeline.py\", \"The AI step failed for {kept_n} item{'s' if kept_n != 1 else ''}\", \"The AI step failed for {len(kept_e)} item{'s' if len(kept_e) != 1 else ''}\"),\n (\"M9 flags label -> second check\", \"app/backend/pipeline.py\", '(old, \"finding the flags\")', '(old, \"the second check\")'),\n (\"M10 join drops FIXTURE_MISS exclusion\", \"app/backend/why.py\", 'j = None if \"FIXTURE_MISS\" in (reasons or []) else judge', 'j = judge'),\n (\"M11 judge_failed ignores NOT_RUN code\", \"app/backend/why.py\", ' and judge.get(\"reason_code\") != \"JUDGE_NOT_RUN\"', ''),\n (\"M12 present._why ignores judge\", \"app/backend/present.py\", 'why.why(c, None if \"FIXTURE_MISS\" in reasons else judge)', 'why.why(c)'),\n (\"M13 flags stored why old\", \"app/backend/flags.py\", 'f[\"why\"] = why.join(f[\"reasons\"], (f.get(\"ladder\") or {}).get(\"judge\")) if', 'f[\"why\"] = \" \".join(why.why(c) for c in f[\"reasons\"]) if'),\n (\"M14 _noting ignores FixtureMiss\", \"app/backend/pipeline.py\", \"except (AU.LLMFailed, P.FixtureMiss):\", \"except (AU.LLMFailed,):\"),\n (\"M15 flags/conflicts not in prune guard\", \"app/backend/pipeline.py\", 'prune=not ({\"flags\", \"conflicts\"} & set(failed_steps))', 'prune=not ({\"flags\"} & set(failed_steps))'),\n (\"M16 stub reasons drop SCHEMA_INVALID\", \"app/backend/pipeline.py\", '_STUB_REASONS = {\"LLM_FAILED_AFTER_RETRIES\", \"FIXTURE_MISS\", \"SCHEMA_INVALID\"}', '_STUB_REASONS = {\"LLM_FAILED_AFTER_RETRIES\", \"FIXTURE_MISS\"}'),\n (\"M17 stub reasons drop FIXTURE_MISS\", \"app/backend/pipeline.py\", '_STUB_REASONS = {\"LLM_FAILED_AFTER_RETRIES\", \"FIXTURE_MISS\", \"SCHEMA_INVALID\"}', '_STUB_REASONS = {\"LLM_FAILED_AFTER_RETRIES\", \"SCHEMA_INVALID\"}'),\n]\ntests = [\"tests/unit/test_t146_r2_failed_rerun_keeps_items.py\", \"tests/unit/test_t146_rerun_keeps_items.py\", \"tests/unit/test_t145_judge_not_run.py\"]\nwide = tests + [\"tests/unit/test_trace.py\", \"tests/unit/test_export.py\", \"tests/unit/test_t138_undo_edit.py\", \"tests/unit/test_t114_rates_and_demo_judges.py\", \"tests/unit/test_t139_narrow.py\"]\nfor name, f, old, new in muts:\n    if os.path.exists(M): shutil.rmtree(M)\n    shutil.copytree(ARC, M)\n    p = os.path.join(M, f); s = open(p).read()\n    if s.count(old) != 1: print(name, \"PATTERN COUNT\", s.count(old)); continue\n    open(p, \"w\").write(s.replace(old, new))\n    r = subprocess.run([PY, \"-I\", \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\", \"-x\", \"--no-header\"] + tests, cwd=M, capture_output=True, text=True)\n    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]\n    res = f\"{name}: narrow -> {last}\"\n    if r.returncode == 0:\n        r2 = subprocess.run([PY, \"-I\", \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\", \"--no-header\"] + wide, cwd=M, capture_output=True, text=True)\n        res += f\" | wide -> {r2.stdout.strip().splitlines()[-1]}\"\n    print(res, flush=True)\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/mut.py $S $S/arc 2>&1 | tail -30",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:20:16.084Z

**tool result**
````
M1 _degrades always None: narrow -> 1 failed in 0.73s
M1b judge arm off: narrow -> 1 failed, 2 passed in 0.88s
M3 prune ignored: narrow -> 1 failed, 11 passed in 1.95s
M5 entry_id backfill off: narrow -> 1 failed in 0.63s
M6 case status failed only on timeout: narrow -> 1 failed in 0.67s
M7 run_partial error never set: narrow -> 1 failed in 0.70s
M8 count = entries only: narrow -> 27 passed in 2.71s | wide -> 189 passed in 30.71s
M9 flags label -> second check: narrow -> 27 passed in 2.52s | wide -> 189 passed in 30.52s
M10 join drops FIXTURE_MISS exclusion: narrow -> 1 failed, 15 passed in 2.79s
M11 judge_failed ignores NOT_RUN code: narrow -> 1 failed, 14 passed in 2.13s
M12 present._why ignores judge: narrow -> 1 failed, 12 passed in 1.83s
M13 flags stored why old: narrow -> 27 passed in 2.63s | wide -> 189 passed in 30.05s
M14 _noting ignores FixtureMiss: narrow -> 27 passed in 2.91s | wide -> 189 passed in 29.09s
M15 flags/conflicts not in prune guard: narrow -> 27 passed in 3.11s | wide -> 189 passed in 34.16s
M16 stub reasons drop SCHEMA_INVALID: narrow -> 27 passed in 2.89s | wide -> 189 passed in 26.40s
M17 stub reasons drop FIXTURE_MISS: narrow -> 27 passed in 2.48s | wide -> 189 passed in 26.10s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:20:33.675Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cat > $S/probes/p7.py <<'EOF'\nimport sys\nexec(open(sys.argv[0].replace(\"p7.py\",\"p1.py\")).read().split(\"LF = lambda\")[0])\nfrom app.llm import provider as P\nLF = lambda s: AU.LLMFailed(f\"{s} down\", last_error=\"TIMEOUT\")\n# deadline at each stage, full-row compare\nfor stage in (\"extract\",\"verify\",\"judge_entries\",\"amounts\",\"conflicts\",\"flags\"):\n    conn, cid = fresh(); b = snap(conn, cid); t=[0.0]\n    def on_stage(n, t=t, stage=stage):\n        if n == stage: t[0] = 10_000.0\n    out = PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script()), now=lambda: t[0], on_stage=on_stage, deadline_s=480)\n    c = DB.get_case(conn, cid); print(\"deadline@\", stage, out[\"status\"], c[\"status\"], json.loads(c[\"error\"])[\"code\"]); diff(b, snap(conn, cid), \"  \")\n# wording\nd = tempfile.mkdtemp(); conn = DB.connect(os.path.join(d, \"d.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\nPL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(j1=LF(\"j1\"))), now=lambda: 1.0)\nprint(\"CALLED+FAILED:\", present.item_view(conn, cid, \"e1\")[\"why\"])\nprint(\"CALLED+FAILED amount j2:\", end=\" \")\nd = tempfile.mkdtemp(); conn = DB.connect(os.path.join(d, \"d.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\nPL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(j2=LF(\"j2\"))), now=lambda: 1.0)\nprint(present.item_view(conn, cid, \"a1\")[\"why\"])\nd = tempfile.mkdtemp(); conn = DB.connect(os.path.join(d, \"d.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\nticks = iter([0.0, 0.0, 0.0, 0.0] + [10_000.0] * 5000)\nPL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script()), now=lambda: next(ticks), deadline_s=480)\nrows = DB.list_items(conn, cid, \"entry\"); print(\"deadline rows:\", len(rows), set(r[\"state\"] for r in rows))\nfor r in rows[:1]: print(\"DEADLINE:\", present.item_view(conn, cid, r[\"id\"])[\"why\"][:120], r[\"state_reasons\"], (r[\"ladder\"] or {}).get(\"judge\"))\n# fixture miss j1\nd = tempfile.mkdtemp(); conn = DB.connect(os.path.join(d, \"d.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\nPL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(j1=P.FixtureMiss(\"m\"))), now=lambda: 1.0) if False else None\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p7.py $S/arc 2>&1 | grep -v \"ladder'\\]$\" | tail -30",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:20:35.021Z

**tool result**
````
deadline@ extract timeout failed run_deadline
   total differing items: 0 | counts {'entry': 9, 'amount': 4, 'flag': 10}
deadline@ verify timeout failed run_deadline
   total differing items: 0 | counts {'entry': 9, 'amount': 4, 'flag': 10}
deadline@ judge_entries timeout failed run_deadline
   total differing items: 0 | counts {'entry': 9, 'amount': 4, 'flag': 10}
deadline@ amounts timeout failed run_deadline
   total differing items: 0 | counts {'entry': 9, 'amount': 4, 'flag': 10}
deadline@ conflicts timeout failed run_deadline
   total differing items: 0 | counts {'entry': 9, 'amount': 4, 'flag': 10}
deadline@ flags timeout failed run_deadline
   total differing items: 0 | counts {'entry': 9, 'amount': 4, 'flag': 10}
CALLED+FAILED: The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked.
CALLED+FAILED amount j2: The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked.
deadline rows: 9 {'needs_review'}
DEADLINE: JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked. ['JUDGE_UNAVAILABLE'] {'call_id': None, 'model': None, 'prompt_version': None, 'reason_code': 'JUDGE_NOT_RUN', 'verdict': 'unavailable'}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:20:41.825Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2; cat > $S/probes/p8.py <<'EOF'\nimport sys\nexec(open(sys.argv[0].replace(\"p8.py\",\"p1.py\")).read().split(\"LF = lambda\")[0])\nfrom app.llm import provider as P\nd = tempfile.mkdtemp(); conn = DB.connect(os.path.join(d, \"d.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\nPL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(j1=P.FixtureMiss(\"m\"))), now=lambda: 1.0)\ne = DB.get_item(conn, \"e1\"); print(e[\"state\"], e[\"state_reasons\"], (e[\"ladder\"].get(\"judge\") or {}))\nprint(present.item_view(conn, cid, \"e1\")[\"why\"][:160])\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/probes/p8.py $S/arc 2>&1 | tail -5; cd /Users/arsis/zlayt-pm-project && git rev-parse HEAD && git diff HEAD --stat -- app/backend/pipeline.py app/backend/why.py | tail -2",
 "timeout": 100000
}
````

### User / tool · 2026-11-02T14:20:42.470Z

**tool result**
````
needs_review ['JUDGE_UNAVAILABLE', 'FIXTURE_MISS'] {'call_id': None, 'model': 'claude-haiku-5-5', 'prompt_version': 'judge_faithfulness_v1', 'reason_code': 'NONE', 'verdict': 'unavailable'}
JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked. The demo has no recorded AI answer for this step, so
611bdcc3f99ff48127fc9c0a647b8aa3ff2a7623
 app/backend/why.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:20:47.355Z

**tool call — Bash**
````
{
 "command": "git log --oneline 2db6ad2..HEAD; git diff 2db6ad2 HEAD --stat | tail -5; git diff 2db6ad2 HEAD -- app/backend/pipeline.py app/backend/why.py app/backend/present.py app/backend/flags.py | head -30; grep -n \"_STUB_REASONS\\|prune=\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t146r2/arc/app/backend/pipeline.py | head -3; sed -n 70,80p app/frontend/input.js | cut -c1-220"
}
````

### User / tool · 2026-11-02T14:20:47.519Z

**tool result**
````
e2bb025 test(frontend): declare data-entry-id and data-flag in the e2e hook contract (T-144, T-154)
611bdcc feat(frontend): T-154 charges are never batch-accepted (note + CHARGES_NOT_BATCHED message); a flagged charge shows its flag and accepts only through a named confirm
f262223 fix(frontend): T-144 the uncovered list opens from a short link in the entry head so compact rows keep their height
ad8b7d1 fix(backend): T-141 r3 pre-accident records are info-only only without injury/mechanism vocabulary; checks notes computed at read time; no stored summary = not run
2a6f40b docs(orchestrator): D-060 charge candidates are default-deny (amends D-059)
078c5ae fix(frontend): T-136 r3 the open quote-pick card no longer says the export stays blocked while the gate passes: conditional fallback, server human why shown as given (no regex swap)
a0e2639 feat(backend): D-059 charge rules, named confirms, no batch accept, expected totals (T-140 r2)
f5ad979 feat(frontend): T-136 r3 case-level steps and the AI-check panel read second_check_pending; a held re-picked quote offers Write the summary and a rerun only until one gave no answer (rerun_no_answer), never 'dismiss it'
94c30db feat(frontend): T-151 Conflicts group lists checks.skipped[] with the server's reason and records, shows checks.notes[] as info (not conflicts), keeps the not-checked line visible; a skipped type is not listed as checked
ded5ca4 feat(frontend): T-144 'Also in this record, not in an entry (n)' list under each entry, one click to the highlighted sentence
1394661 feat(frontend): T-149 multi-case overview (list, filter, sort, call-out chips, progress per kind) and case overview block (progress, call-outs, export-gate steps) at the top of the detail
df6afac tools: pre-commit refuses a tree that cannot import or run the sample case on its own (lessons 225e666, 2db6ad2)
 tests/unit/test_t141_checks_per_case.py            |  96 ++++++
 tests/unit/test_t141_r3_variants.py                | 115 +++++++
 tools/check_index_imports.py                       |  47 +++
 tools/install_git_hooks.sh                         |   1 +
 77 files changed, 2866 insertions(+), 198 deletions(-)
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index a633e16..b03171b 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -104,7 +104,8 @@ def amount_item(a: dict, r: dict, item_id: str = None) -> dict:
     """The pipeline's amount item from an amounts.extract_amounts row and its record."""
     return {"id": item_id or a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
             "cents": a["cents"], "value_cents": a["cents"], "cls": a["cls"], "kind": a["cls"], "start": a["start"], "end": a["end"],
-            "excerpt": r["excerpt"], "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending"}
+            "excerpt": r["excerpt"], "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending",
+            "confirm": a.get("confirm")}
 
 
 def _not_duplicates(conn, cid: str) -> list:
diff --git a/app/backend/present.py b/app/backend/present.py
index d3d14d1..038cd92 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -62,8 +62,15 @@ def accept_effect(row) -> str:
     return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")
 
 
+def amount_flag(row):
+    """D-059: the flag a charge carries (likely_duplicate | likely_total) and whether accepting it now needs the confirm step. (None, False) for any other amount."""
+    f = (row.get("ladder") or {}).get("confirm") if row["kind"] == "charge" else None
+    return (None, False) if not f else ({k: f.get(k) for k in ("flag", "name", "message", "confirm_with", "of", "confirmed_at")}, row["review_status"] == "pending")
+
+
 def amount_view(row, recs):
-    return {**_common(row), "record_ids": row["record_ids"], "entry_id": row["entry_id"], "text": row["text"], "value_cents": row["value_cents"],
240:_STUB_REASONS = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"}      # an entry rejected for one of these has no output at all: a stub
248:    if kind == "entry" and it.get("state") == "rejected" and set(it.get("reasons") or []) & _STUB_REASONS and old.get("summary") and old.get("excerpt"):
260:    returned (`kept`, as (row, cause)) so the caller can say so. `prune=False`: the stale-pending delete is skipped (a failed flag step cannot tell which flags are stale)."""
      running ? runningNode(s) : null,
      el("div", { class: "row" },
        c.status === "ingested" && !running ? el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-analyze", onclick: startRun }, "Analyze") : null,
        el("button", { type: "button", class: running ? "btn btn--ghost" : "btn", "data-testid": "start-over", onclick: startOver }, "Start over")),
      failed ? el("div", { class: "notice notice--bad", role: "alert", "data-testid": "run-error" },
        el("div", { class: "notice-body" }, el("strong", {}, "The analysis did not finish. "), "Your records are kept and finished items are saved. ", (s.status.error && s.status.error.message) || ""),
        el("button", { type: "button", class: "btn", "data-testid": "btn-retry-run", onclick: startRun }, "Try again")) : null,
      el("p", { id: "input-error", class: "error", role: "alert", "data-testid": "error", hidden: true })].filter(Boolean));
  };
  // ---- processing state: a real progress element, the stage in plain words, elapsed seconds after a while, skeleton rows. No raw stage names.
  let runStart = 0;
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:05.669Z

**tool call — Bash**
````
{
 "command": "git show 2db6ad2:app/backend/pipeline.py | grep -n \"def _degrades\\|_STUB_REASONS = \\|return \\\"the second check\\\"\\|kept_f = _persist\\|prune=not\\|if kept_n:\\|status=\\\"failed\\\" if (timed_out or err)\\|def _noting\\|confirm\\\": a\\[\\\"confirm\\\"\\]\" ; git show 2db6ad2:tests/unit/test_t146_r2_failed_rerun_keeps_items.py | grep -n \"def test_flag_step_down\\|def _model_flag\\|def test_first_run\\|\\\"9 \\\" in\\|\\\"second\\\" in\"; ls reviews | grep T-146"
}
````

### User / tool · 2026-11-02T14:21:05.792Z

**tool result**
````
240:_STUB_REASONS = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"}      # an entry rejected for one of these has no output at all: a stub
243:def _degrades(kind: str, old: dict, it: dict):
251:    return "the second check" if new_j.get("verdict") == "unavailable" and old_j.get("verdict") not in (None, "unavailable") else None
326:                   **({"confirm": a["confirm"]} if a.get("confirm") else {})}      # D-059: the flag the paralegal must confirm by name before accepting this charge
349:def _noting(raw_call, failed_steps: list):
479:    kept_f = _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t, additive=timed_out,
480:                      prune=not ({"flags", "conflicts"} & set(failed_steps)))
489:        if kept_n:      # T-146 r2: an AI step failed on a re-run and its earlier results were kept; the case says so instead of reading 'ready'
493:    DB.update_case(conn, cid, status="failed" if (timed_out or err) else "ready", stage="finalize", error=json.dumps(err) if err else None,
56:    assert "9 " in err["message"]                          # names how many items the failed step touched
86:    assert err and err["code"] == "run_partial" and "second" in err["message"].lower() and "kept" in err["message"]
90:def test_first_run_with_a_down_step_still_stores_its_stubs_and_is_not_marked_partial(tmp_path):
137:def _model_flag(user):
142:def test_flag_step_down_rerun_keeps_the_model_flag_it_cannot_rediscover(tmp_path):
T-146-staff-engineer.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:06.692Z

Now write the review.

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:48.513Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-146-staff-engineer-r2.md",
 "content": "# T-146 staff-engineer review, round 2 (2db6ad2, tested on a `git archive` of 2db6ad2)\n\nVerdict: **changes** (0 blockers, 2 majors, 2 minors, 1 nit).\n\nThe round-1 case is fixed. On the archive I completed the sample (9 entries, 4 amounts, 10 flags), accepted e1, dismissed e2, accepted a1, then re-ran with the extract step raising `LLMFailed`: case `failed`, error `run_partial` \"The AI step failed for 9 items (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged...\", e1 still `verified`/`accepted` with its summary and quote, and a full-row compare of all 23 stored items differs only in `ladder.*.call_id` on amounts/flags that were re-judged. Judge-down (j1/j2, or all four judges) keeps all 23 rows byte-identical and reads `failed/run_partial` \"...12 items (the second check)\". A deadline at extract, verify, judge_entries, amounts, conflicts and flags keeps all rows identical (`run_deadline`). The judge wording is right in all three cases: called-and-failed says \"The second check failed\", a deadline keeps `JUDGE_NOT_RUN:`, and a fixture miss keeps `JUDGE_NOT_RUN:` plus the demo sentence.\n\nTwo re-run paths still overwrite stored work without an error, and both are inside the orchestrator's rule (\"No re-run may overwrite a decided item or an item with stored output with an empty or partial stub\", \"undo a second-check answer\", \"delete flags\", \"failed flag step\"). See F1 and F2.\n\nWhat I ran (archive of 2db6ad2, project `.venv/bin/python -I`):\n- `pytest tests/unit -q -p no:cacheprovider`: **3893 passed, 8 skipped** in 441 s, no failures (the handoff's 2 flaky and 4 failing tests did not reproduce on the committed tree).\n- Probe scripts (kept outside the archive, in the scratchpad `t146r2/probes/`): complete run, accept e1, dismiss e2, accept a1, then re-run with extract down, j1+j2 down, all four judges down, flags down, conflicts down, deadline at six stages, and one record failing at extract (LLMFailed, FixtureMiss, schema-invalid, summary-not-in-quote); each compared on full stored rows (every column but `updated_at`), case status/error, and `trace.export_blockers`.\n- Wording probe: j1 down, j2 down, deadline, and j1 FixtureMiss, read through `present.item_view(...)[\"why\"]`.\n- 16 mutants of `pipeline.py`, `why.py`, `present.py`, `flags.py` on a scratch copy, run against the three T-145/T-146 test files and, for survivors, 5 more related files (189 tests).\n\nMutants killed: `_degrades` always None, judge arm off, prune ignored, entry_id backfill off, case status failed only on timeout, `run_partial` never set, FIXTURE_MISS exclusion dropped from `why.join`, `judge_failed` ignoring the NOT_RUN code, `present._why` ignoring the judge. Survived: see F3.\n\n```json\n{\n  \"card\": \"T-146\",\n  \"persona\": \"staff-engineer-reviewer\",\n  \"model\": \"claude-sonnet-5-5\",\n  \"scope\": \"commit 2db6ad2 (app/backend/pipeline.py _degrades/_persist/_noting/run_partial, why.py, present.py, flags.py, tests/unit/test_t146_r2_failed_rerun_keeps_items.py); git archive of 2db6ad2 (HEAD later moved to 611bdcc, pipeline.py _persist and run_pipeline unchanged by it); fixture backend; sample case evals/golden/sample.txt\",\n  \"exercised\": [\n    \"read reviews/T-146-staff-engineer.md, python3 tools/board.py show T-146 (orchestrator note and handoff), git show 2db6ad2\",\n    \"git archive 2db6ad2 into a scratch dir; pytest tests/unit -q -p no:cacheprovider: 3893 passed, 8 skipped\",\n    \"round-1 repro: complete run, accept e1, dismiss e2, accept a1, re-run with extract raising LLMFailed: case failed/run_partial naming 9 items and 'writing the entries', e1 verified+accepted, full-row compare of 9 entries, 4 amounts, 10 flags (only ladder call ids of re-judged amounts/flags differ)\",\n    \"re-run probes with full-row compare: j1+j2 down, all four judges down, flags step down, conflicts step down, deadline at extract/verify/judge_entries/amounts/conflicts/flags\",\n    \"per-record probes at e1: extract LLMFailed, FixtureMiss, schema-invalid summary, SUMMARY_NOT_IN_QUOTE; j1 failing for record 1 only\",\n    \"model flag that agrees with lexicon flag f_r3_1 (state lexicon+llm, verified), accept it, re-run with the flags step down\",\n    \"export gate and letter: trace.export_blockers, present.review_view counts and store.export_case after the SUMMARY_NOT_IN_QUOTE re-run\",\n    \"judge wording via present.item_view: j1 failed, j2 failed, deadline, j1 FixtureMiss\",\n    \"16 mutants on a scratch copy (killed 9: no-protect, judge arm, prune, entry_id backfill, status, run_partial error, join FIXTURE_MISS, judge_failed NOT_RUN code, present._why; survived 7: count, flags label, stored flag why, _noting FixtureMiss, conflicts prune guard, two stub-reason set members)\",\n    \"git show 2db6ad2 diff read in full; git log 2db6ad2..HEAD and git diff 2db6ad2 HEAD on pipeline.py/why.py/present.py/flags.py\"\n  ],\n  \"verdict\": \"changes\",\n  \"scores\": {\n    \"timeout_rerun_keeps_items_and_decisions\": 5,\n    \"errored_rerun_keeps_stored_rows_whole\": 3,\n    \"case_shows_honest_error_with_count_and_step\": 3,\n    \"judge_wording_matches_cause\": 5,\n    \"test_quality_mutation_sensitivity\": 3\n  },\n  \"findings\": [\n    {\n      \"severity\": \"major\",\n      \"title\": \"A re-run with the flag step down downgrades an accepted, verified flag to needs_review / LLM_FAILED_AFTER_RETRIES, drops its second-check answer and AI origin, and reports run status 'done', case 'ready', error None\",\n      \"evidence\": \"Repro on the archive (probe p4): fixture backend, model flag for record 3 with the same quote as lexicon flag f_r3_1 -> complete run stores `f_r3_1 verified [] lexicon+llm`; `DB.apply_review(conn,'f_r3_1','accept')`; `PL.run_pipeline(..., call=FakeCall(sample_script(flags=AU.LLMFailed('flags down', last_error='TIMEOUT'))), now=lambda: 3.0)` -> out status `done`, `out['errors'] == []`, case `ready`, `error None`; `f_r3_1` now `needs_review ['LLM_FAILED_AFTER_RETRIES'] lexicon accepted`; diff of stored rows: `flag f_r3_1 CHANGED ['origin','state','state_reasons','ladder']`. Without any model flag the same re-run rewrites the reasons of 7 stored flags (f_r3_1, f_r6_1, f_r7_1, f_r7_2, f_r8_1, f_r8_2, f_r9_1) from `LEXICON_ONLY` to `LLM_FAILED_AFTER_RETRIES`, including f_r3_1 after it was accepted (case still `ready`, error None). Cause: `_degrades` (pipeline.py:243-251) protects a flag only when the NEW row's judge verdict is `unavailable`; a flag made while the flag step failed has no judge record at all (lexicon fallback), so nothing is kept. `failed_steps` already contains 'flags' (pipeline.py:479-480) but is used only for `prune`. The only flag-step test (`test_flag_step_down_rerun_keeps_the_model_flag_it_cannot_rediscover`, test file line 142) uses a model-only flag, which takes the prune path.\",\n      \"why_it_matters\": \"This is the orchestrator's own list: a failed flag step must not undo a second-check answer or alter stored flags, and an errored re-run must show an honest error naming the count and the step. Here the paralegal's accepted flag loses its AI corroboration (verified -> needs_review, origin lexicon+llm -> lexicon, judge answer erased from the ladder) and nothing at case level says the flag step failed. Not a blocker: no fact is invented, the quote and the accept decision survive, and a good re-run restores it.\",\n      \"fix\": \"Treat a flag row made while the flag step failed (its reasons contain LLM_FAILED_AFTER_RETRIES and the stored row's do not, or `failed_steps` contains 'flags') as degraded when a stored row exists: keep the stored row whole and count it under 'finding the flags', so the case reads failed/run_partial with the count. Extend the flag-step test to the corroborated lexicon+llm flag, an accepted lexicon-only flag, and assert full-row equality.\",\n      \"acceptance_test\": \"Complete run with a model flag agreeing with f_r3_1, accept it, re-run with flags down: assert full stored rows of all flags equal (no_ladder allowed only for call ids), f_r3_1 still `verified`/`lexicon+llm`/`accepted`, case `failed`, error `run_partial` naming the count and 'finding the flags'. Mutation: removing the new keep rule fails it.\"\n    },\n    {\n      \"severity\": \"major\",\n      \"title\": \"A re-run whose extract answer fails the summary-in-quote check replaces an accepted entry with an empty rejected stub, with case 'ready', error None, and a passing export gate\",\n      \"evidence\": \"Repro on the archive (probe p6): complete run, accept e1, re-run with extract returning `{'summary': 'Patient had a skull fracture of 99 cm.', 'excerpt': <e1's real quote>}` for record 1 -> out status `done`, case `ready`, error None; `DB.get_item(conn,'e1')` = `{summary: None, excerpt: None, state: 'rejected', state_reasons: ['SUMMARY_NOT_IN_QUOTE'], review_status: 'accepted'}`; stored-row diff `entry e1 CHANGED ['summary','excerpt','excerpt_start','excerpt_end','state','state_reasons','ladder']`; `trace.export_blockers` = `[]`; `present.review_view` counts `accepted: 1` (the empty stub itself, so NOTHING_ACCEPTED does not fire); the exported entry list is e2..e9 with e1 absent. `_STUB_REASONS` (pipeline.py:240) lists LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS and SCHEMA_INVALID only; the handoff states this under 'Left: SUMMARY_NOT_IN_QUOTE (model answered) still replaces', and no test covers it. Control: the same re-run with LLMFailed, FixtureMiss or an invalid schema for record 1 keeps e1 whole (`failed/run_partial`, 1 item).\",\n      \"why_it_matters\": \"The orchestrator's rule has no exception for 'the model answered': the next run of a non-deterministic summarizer can erase an accepted entry, and the paralegal gets a green gate and a letter missing a paragraph she accepted, with no error anywhere. A declared gap in the handoff is still a gap against the rule. Rated major (recoverable by a re-run, the record text survives, the stub is visible in the tray) rather than blocker, consistent with round 1.\",\n      \"fix\": \"Either include SUMMARY_NOT_IN_QUOTE (and any extract-stage rejection) in the keep-whole rule for rows that have a stored summary and quote, with the same run_partial message, or keep the new row only as a tray attempt while the accepted/decided entry stays in the timeline; add the case to the tests. If Chris wants D-054 to win (the new answer replaces), record that as a decision and make the gate fail on an accepted item with no summary.\",\n      \"acceptance_test\": \"Unit test: complete run, accept e1, re-run with an unsupported summary for record 1; assert e1's full stored row is unchanged and the case is failed/run_partial naming 1 item (or, under the alternative, that an accepted empty stub blocks the export). Mutation: dropping SUMMARY_NOT_IN_QUOTE from the keep set fails it.\"\n    },\n    {\n      \"severity\": \"minor\",\n      \"title\": \"Seven mutants survive: the message count, the flag-step label, the stub-reason set, the FixtureMiss path and the conflicts guard are not pinned\",\n      \"evidence\": \"Scratch copy of the archive, narrow (3 files, 27 tests) and wide (8 files, 189 tests) both green for: (M8) message count uses `len(kept_e)` instead of `kept_n`: judge-down would read '9 items' instead of 12 (test line 86 only checks 'second'/'kept'); (M9) label 'finding the flags' changed to 'the second check'; (M13) `flags.py:45` back to the old `why.why(c)` join; (M14) `_noting` catching only `AU.LLMFailed` (no FixtureMiss); (M15) prune guard drops 'conflicts'; (M16) SCHEMA_INVALID removed from `_STUB_REASONS`; (M17) FIXTURE_MISS removed from `_STUB_REASONS` (tests only exercise LLM_FAILED_AFTER_RETRIES for the stub rule). Killed: 9 others (listed above).\",\n      \"why_it_matters\": \"Checklist 13: tests assert behaviour. The headline behaviour is covered, but the count and step the orchestrator asked the message to name, and two of the three stub causes, can regress unseen.\",\n      \"fix\": \"Assert the exact count and step in each message test (extract-down: '9 items' and 'writing the entries'; judge-down: the stored-row count and 'the second check'; flag-down: 'finding the flags'); add one parametrized test over the three stub reasons (LLMFailed, FixtureMiss, schema-invalid) and one with conflicts down.\",\n      \"acceptance_test\": \"M8, M9, M14, M15, M16 and M17 each fail the strengthened tests; M13 fails if a test reads the stored flag `why` after a judge-failed run.\"\n    },\n    {\n      \"severity\": \"minor\",\n      \"title\": \"A re-run that ends with errors but has no stored output to keep still reads 'ready' with error None; the new messages never fire\",\n      \"evidence\": \"tests/unit/test_t146_r2_failed_rerun_keeps_items.py:90 `test_first_run_with_a_down_step_still_stores_its_stubs_and_is_not_marked_partial` asserts `err is None and c['status'] == 'ready'` after `done_with_errors`; pipeline.py:489 sets `run_partial` only `if kept_n:`. Same for a second extract-down run on top of a first one (stored rows already stubs, nothing to keep) and for the flags-down run in F1 (`out['errors'] == []`). The handoff lists the first-run case under 'Left'.\",\n      \"why_it_matters\": \"The orchestrator asked for an honest error on any errored re-run naming the count and the step; today the case-level message depends on there being something to protect, so a stub-on-stub re-run says nothing. The tray shows the failed records, so this is not data loss.\",\n      \"fix\": \"When `errors` is non-empty or a step in `failed_steps` failed, set the case error (code run_partial or a sibling) with the count of items that have no output and the step name, whether or not anything was kept.\",\n      \"acceptance_test\": \"Second consecutive extract-down run on the sample: case failed, error names 9 items and 'writing the entries'; first run still stores stubs. Mutation: restoring `if kept_n:` fails it.\"\n    },\n    {\n      \"severity\": \"nit\",\n      \"title\": \"Commit 2db6ad2 carries a D-059 hunk that belongs to the T-140 card\",\n      \"evidence\": \"pipeline.py:326 in 2db6ad2: `**({\\\"confirm\\\": a[\\\"confirm\\\"]} if a.get(\\\"confirm\\\") else {})}      # D-059: the flag the paralegal must confirm by name`; `amount_item` only starts setting `confirm` in a0e2639 (git diff 2db6ad2 HEAD -- app/backend/pipeline.py), so the hunk is dead code inside this commit.\",\n      \"why_it_matters\": \"Reviewers of T-146 cannot tell this hunk from the fix, and a revert of T-146 would pull a T-140 piece with it (the shared index is a known hazard in this repo).\",\n      \"fix\": \"Stage by hunk (`git add -p` is unavailable here, so split the file edit) or note it in the card handoff.\",\n      \"acceptance_test\": \"git show --stat of the fix commit lists only T-146 hunks.\"\n    }\n  ],\n  \"whats_right\": [\n    \"run_partial keeps the full stored row (summary, quote, offsets, ladder, state, review status) for failed extract, one failed record, all-judges-down, and a single failed j1, and the case reads failed with the count and the step named in the message.\",\n    \"The judge wording follows the judge record: called-and-failed says 'The second check failed' (reason code JUDGE_UNAVAILABLE unchanged), while deadline and fixture-miss keep the JUDGE_NOT_RUN sentence, and the choice is made in one place (why.why/join) with the mutants killed.\",\n    \"The deadline path stays additive at all six stages with identical rows, and a later good re-run clears the error and the accepted decision stands.\"\n  ],\n  \"questions_for_chris\": []\n}\n```\n"
}
````

### User / tool · 2026-11-02T14:21:48.690Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-146-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:49.095Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T14:21:49.265Z

**tool result**
````
ok (155 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:50.514Z

Save a memory note.

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:54.774Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t146_r2_patterns.md",
 "content": "---\nname: t146-r2-patterns\ndescription: T-146 r2 2db6ad2 changes - keep-whole rule keyed on judge/stub only, so lexicon-fallback flags and SUMMARY_NOT_IN_QUOTE still overwrite; message count/step unpinned\nmetadata:\n  type: project\n---\n\nT-146 r2 (2db6ad2) changes, 2 majors: `_degrades` protects an entry stub (3 reasons) and a new judge verdict 'unavailable'; a flags-step-down re-run makes lexicon-fallback flags with NO judge record, so an accepted verified lexicon+llm flag becomes needs_review/LLM_FAILED, origin lexicon, case ready, error None. SUMMARY_NOT_IN_QUOTE (model answered) over accepted e1 -> empty rejected stub, gate passes, accepted count counts the stub. Declared in handoff \"Left\" - still a finding.\n\n**How to apply:** for \"keep earlier results\" fixes, probe each failing step (extract, each judge, flags, conflicts) with a corroborated + accepted item, not only the model-only case the author tested. Mutant method: copy of git archive, 16 string-replace mutants, narrow then wide test files; survivors were count/label/stub-set members. Fake-backend probes: `sample_script(flags=LLMFailed)`, model flag copying the lexicon quote makes `lexicon+llm` verified. File: reviews/T-146-staff-engineer-r2.md.\n"
}
````

### User / tool · 2026-11-02T14:21:54.914Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t146_r2_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:55.845Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && echo \"- [T-146 r2 patterns](project_t146_r2_patterns.md) — 2db6ad2 changes: keep-whole rule keyed on judge/stub only; flags-down downgrades corroborated flag, SUMMARY_NOT_IN_QUOTE overwrites\" >> MEMORY.md"
}
````

### User / tool · 2026-11-02T14:21:55.994Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:59.647Z

T-146 round 2 verdict is **changes**: 0 blockers, 2 majors, 2 minors, 1 nit. The written review is `/Users/arsis/zlayt-pm-project/reviews/T-146-staff-engineer-r2.md`, and `board.py validate` accepted it.

- **Fixed:** My round-1 repro (extract down after accepting entries) now ends `failed`/`run_partial`, names 9 items and the step, and keeps all stored rows. Judge-down and deadline re-runs also keep every row, and the judge wording matches the cause. `pytest tests/unit` gave 3893 passed, 8 skipped.
- **Major:** With the flag step down, an accepted, verified flag drops to `needs_review`/`LLM_FAILED_AFTER_RETRIES`, loses its AI origin and second-check answer, and the case reads `ready` with no error.
- **Major:** An extract answer that fails the summary-in-quote check replaces an accepted entry with an empty stub, and the export gate still passes. The handoff lists this under "Left", but your rule has no exception for it.
- **Minor:** Seven of 16 mutants survived: the message count, the flag-step label, the stub-reason set and the conflicts guard. A re-run with nothing stored to keep still shows no error.
- **Nit:** Commit 2db6ad2 carries a D-059 hunk that belongs to T-140.
