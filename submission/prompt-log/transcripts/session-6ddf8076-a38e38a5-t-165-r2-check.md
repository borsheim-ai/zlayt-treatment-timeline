# Subagent: T-165 r2 check (T-165 r2 check)

Source: `agent-a38e38a5b441fe8d9.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T16:26:34.370Z

Run the round-2 check of board card T-165 (commit 56d746c) in /Users/arsis/zlayt-pm-project. Read reviews/T-165-staff-engineer.md (the blocker at pipeline.py:368-376).

On a `git archive HEAD` copy, verify:
- a re-run that recovers a record keeps the paralegal's hand entry, with a note that the AI now also has an entry, and never deletes it;
- the round-1 checks still hold;
- the T-165 and T-146 test files pass.

The unrelated e2e-contract unit failure comes from frontend commit f7a8f2a and is being fixed elsewhere.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-165-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:26:36.807Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:26:36.810Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-165-staff-engineer.md"
}
````

### User / tool · 2026-11-02T16:26:36.819Z

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

### User / tool · 2026-11-02T16:26:36.820Z

**tool result**
````
1	# T-165 staff-engineer review (commit 312efe6)
2	
3	Verdict: **fail**. One blocker: a re-run that extracts a hand-entered record again deletes the paralegal's pending entry with no note. The contract says a re-run never erases earlier work. The T-165 hand-entry protection covers only the branch where the record stays down.
4	
5	Scope: commit 312efe6 (HEAD at review time), read on a `git archive 312efe6` copy. The working tree is dirty with other agents' files and was not used. Golden sample and synthetic two-record notes only.
6	
7	What holds (checked by running the code):
8	- A first run with the extract step down on one record (1 of 9), eight of nine, or all nine reads `failed` / `run_partial`, names the records, and the export gate lists `RUN_FAILED`. Probe A, B.
9	- A run where every record extracted reads `ready`, `error: null`, no warnings. Probe C.
10	- A record entered by hand before the run, or after a failed run, gives an `ENTERED_BY_HAND` warning and no failure. Probe D, E.
11	- A re-run where the record is still down keeps the pending hand-entered entry `e1_m`. Probe F. On the parent `ea988f8` the same probe deletes `e1_m`, so the fix is real for this branch.
12	
13	Blocker, detail: scenario G. A hand-entered record (`e1_m`, pending) is entered, then the re-run extracts record 1 successfully. The final entries are `e1` (AI, pending) only; `e1_m` is gone, the case reads `ready`, and no warning is shown. The sweep at `app/backend/pipeline.py:368-376` skips the delete only when `live_rids` does not cover the record; once the AI writes a live `e1`, the `DELETE` at line 376 removes the paralegal's row. `memory/contracts/api.md:129` says "a re-run never erases earlier work", and the T-165 text in the same line protects a hand-entered entry only "whose extract fails again". The same G probe on `ea988f8` also loses `e1_m`, so this was already present and T-165 did not close it. No test covers it: `tests/unit/test_t165_partial_extract.py:154` (`test_a_rerun_that_extracts_the_record_clears_the_failure`) has no hand entry.
14	
15	Minor, detail: scenario H. After the paralegal dismisses `e1_m`, the case reads `ready`, the tray is empty, the failure does not come back, and the `ENTERED_BY_HAND` warning still says "you entered it by hand". No test covers dismissal.
16	
17	Minor, detail: the four pins named in the brief are justified (see the JSON). A fifth changed assertion, `tests/unit/test_t139_charge_text.py` `counts.entries` 3 to 4, counts the hand entry as an entry; it is a workaround for the T-168 fixture gap and should be reverted with T-168.
18	
19	Pin justification (each one checked against the api.md T-165 text):
20	1. `test_t161_first_run_stage_down.py::test_first_run_with_extract_down_and_no_entries...`: exact error now carries `records` and `extract_only` and names records 1 to 9. Justified by the AC.
21	2. `test_t161_first_run_stage_down.py::test_first_run_with_extract_down_for_some_records...`: `ready` flipped to `failed`, `records == [1]`. Justified by "any record whose extract step failed makes the case run_partial".
22	3. `test_t146_r3_decided_items_never_lowered.py::test_rerun_with_nothing_to_keep...`: exact error gains `records` and `extract_only` and the names. Justified by the AC.
23	4. `test_t146_r3_decided_items_never_lowered.py::test_nothing_to_keep_and_something_kept...`: message gains "No entry was made for record 4." Justified by the AC.
24	
25	Mutation spot-checks on scratch copies of the archive (mutant text is in the commands below):
26	- m1: remove the hand-entry skip at pipeline.py:372. Targeted tests: 2 fail (`test_a_rerun_with_the_record_still_down_keeps_the_hand_entry...`, `test_a_record_entered_by_hand_before_the_run...`). Killed.
27	- m2: drop `PL.refresh_extract_error` at review.py:678. Targeted tests: 2 fail. Killed.
28	- m3: `hand_entered_warnings` returns `[]`. Targeted tests: 4 fail. Killed.
29	
30	Commands and outputs are saved in `artifacts/review-evidence/T-165/` (`probe_t165.py`, `probe_out.txt`, `mut.py`).
31	
32	```json
33	{"card": "T-165", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
34	 "scope": "commit 312efe6 (HEAD at review time) via git archive copy at artifacts-free scratch dir; files: app/backend/pipeline.py, generator.py, present.py, review.py; tests/unit/test_t165_partial_extract.py, _hand_entry.py, test_t161_first_run_stage_down.py, test_t146_r3_decided_items_never_lowered.py, test_t139_charge_text.py, test_api_routes.py, test_case_list.py, test_t114_rates_and_demo_judges.py; contract memory/contracts/api.md:129; synthetic golden sample and two-record synthetic note; no app URL exercised (in-process only)",
35	 "exercised": [
36	  "python3 tools/board.py show T-165 (card read: status in_review, ac 1 done, handoff)",
37	  "reviews/T-161-staff-engineer-r2.md read in full",
38	  "git show 312efe6 --stat and git diff 312efe6^ 312efe6 for all app and test files in the commit",
39	  "git archive 312efe6 | tar -x into scratchpad t165-review/head; file list diffed against git ls-tree -r 312efe6 (identical, 1213 fixture files included)",
40	  "cd head && .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -> 5058 passed, 8 skipped, exit 0 (276 s). Worker handoff quoted 4961 on archive plus hunks; not reconciled, does not change the verdict",
41	  "artifacts/review-evidence/T-165/probe_t165.py run on HEAD archive, scenarios A-H -> artifacts/review-evidence/T-165/probe_out.txt (status, error, export_blockers via trace.export_blockers, warnings, tray, entries)",
42	  "same probe scenario F and G on git archive ea988f8 (parent): G deletes e1_m on the parent too (pre-existing); F deletes e1_m on the parent (fixed by T-165)",
43	  "mutant m1 (pipeline.py:372 continue -> pass) on scratch copy: t165 + t161 + t146_r3 files -> 2 failed, 85 passed",
44	  "mutant m2 (review.py:678 PL.refresh_extract_error -> pass): 2 failed, 85 passed",
45	  "mutant m3 (generator.py hand_entered_warnings return [] ): 4 failed, 83 passed",
46	  "grep of the T-165 diff for except, float(, sleep(, network or key strings: none added (only the word 'retry' in a message string)",
47	  "grep -rn dismiss on the T-165 test file: no test covers a dismissed hand entry",
48	  "grep allow_failed and export_blockers call sites in head/app/backend (export gate is trace.export_blockers, per api.md:663 and export.py:836)"
49	 ],
50	 "verdict": "fail",
51	 "scores": {"first_run_partial_names_records": 4, "all_extracted_stays_ready": 5, "hand_entry_warning_not_failure": 4, "rerun_keeps_pending_hand_entry": 2, "dismiss_and_recover_states": 2, "pins_justified": 4, "test_strength_mutants": 4},
52	 "findings": [
53	  {"severity": "blocker",
54	   "title": "A re-run that extracts a hand-entered record again silently deletes the paralegal's pending entry",
55	   "evidence": "Probe G (artifacts/review-evidence/T-165/probe_out.txt, block '== G'): after hand entry on record 1 and a re-run with record 1 extracting, entries are e1 (AI, pending, verified) only; e1_m is gone; status ready, warnings []. Code: app/backend/pipeline.py:368 live_rids; :372 continue applies only when the record has no live row; :376 DELETE FROM entries ... review_status='pending' removes e1_m. Contract: memory/contracts/api.md:129 'a re-run never erases earlier work'; T-165 text in the same line protects the hand entry only 'whose extract fails again'. Pre-existing: the same probe on git archive ea988f8 also loses e1_m. Repro: git archive 312efe6 | tar -x -C D; cd D && PYTHONPATH=$PWD <repo>/.venv/bin/python <repo>/artifacts/review-evidence/T-165/probe_t165.py G",
56	   "why_it_matters": "The paralegal's typed summary and quote are removed by a re-run with no note and no warning, while the case reads ready. The contract states that a re-run never erases earlier work. The card that claims to protect hand-entered entries leaves this path open, and the brief's check 'a re-run keeps a pending hand-entered entry' fails for this case.",
57	   "fix": "Keep a pending hand-entered entry on every re-run, not only while its record has no live AI row. When the AI also now has an entry for that record, keep both and set a rerun_note on the hand entry (for example 'the AI step now has an entry for record 1; your entry was kept, it is pending'). Remove the live_rids condition at pipeline.py:372 for entered_by=reviewer rows.",
58	   "acceptance_test": "tests/unit/test_t165_partial_extract.py: run with record 1 down, hand-enter record 1, re-run with record 1 extracting. Assert e1_m is still in DB.list_items(conn, cid, 'entry') with review_status 'pending', its ladder.rerun_note is set, and the case status is ready. On HEAD this test fails (e1_m is absent)."},
59	  {"severity": "minor",
60	   "title": "Dismissing a hand-entered entry leaves a stale ENTERED_BY_HAND warning and the failure never returns",
61	   "evidence": "Probe H (probe_out.txt, block '== H'): after RV.apply_review(conn, cid, 'e1_m', {'action': 'dismiss'}), e1_m has review_status 'dismissed', case status ready, error null, tray [], warnings [('ENTERED_BY_HAND', 1, 'e1')]. generator.py:205-207 entered_by_hand counts any non-rejected entry, dismissed included. No test in tests/unit/test_t165_partial_extract.py mentions dismiss.",
62	   "why_it_matters": "The warning tells the paralegal 'you entered it by hand' about an entry they dismissed. Record 1 has no usable entry, and the case no longer shows the extract failure. The dismissed entry is still visible in the entry list, so this is not silent, but the case-level message is wrong.",
63	   "fix": "Exclude dismissed hand entries from entered_by_hand, or word the warning by state. Decide with Chris whether dismissing the hand entry re-opens the extract failure (see questions_for_chris).",
64	   "acceptance_test": "Hand-enter record 1 after a failed run, then dismiss e1_m. Assert the chosen state: either RUN_FAILED and record 1 named again, or no ENTERED_BY_HAND warning. Pin the chosen one."},
65	  {"severity": "minor",
66	   "title": "Fifth changed assertion outside the named pins: test_t139 counts.entries 3 to 4 counts a hand entry as an entry",
67	   "evidence": "tests/unit/test_t139_charge_text.py diff: '-    assert j[\"counts\"][\"entries\"] == 3' / '+    assert j[\"counts\"][\"entries\"] == 4                      # e1, e5, e6 and the hand-entered record 3 (wait_ready)'. Caused by the lib01 fixture gap (T-168) worked around with enter_failed_records_by_hand (tests/unit/_hand_entry.py).",
68	   "why_it_matters": "An assertion about the AI-made timeline now counts a paralegal entry. It is documented in the comment and is a test-data workaround, but it will need reverting when T-168 lands, and it can hide a real AI regression on lib01.",
69	   "fix": "Keep the workaround, but assert the AI-made count separately from the hand entry (for example count entries whose ladder.entered_by is not 'reviewer' equals 3, and the hand entry id is present). Revert with T-168.",
70	   "acceptance_test": "test_t139 lib01 assertion: AI-made entries == 3 and the hand entry e3_m present; mutant that drops one AI entry fails the test."}
71	 ],
72	 "whats_right": [
73	  "A first run with the extract step down on one, eight or all nine records reads failed / run_partial, names the records, and the export gate lists RUN_FAILED; all-extracted stays ready with error null (probe A, B, C)",
74	  "A hand entry before the run or after a failed run gives an ENTERED_BY_HAND warning, not a failure; a still-down re-run keeps the pending hand entry, where the parent ea988f8 deleted it (probe D, E, F vs parent)",
75	  "The four pins in tests/unit/test_t161_first_run_stage_down.py and tests/unit/test_t146_r3_decided_items_never_lowered.py each change one assertion to the behaviour the api.md T-165 text names; mutants m1, m2, m3 are killed by the T-165 file"
76	 ],
77	 "questions_for_chris": [
78	  "When a record's extract failed and the paralegal hand-enters it, then dismisses that entry: should the extract failure (RUN_FAILED and the tray placeholder) come back, or stay cleared?",
79	  "On a re-run that extracts a record the paralegal had entered by hand and that entry is still pending: keep both (with a note), or is the sweep a deliberate decision? Reading of api.md:129 is keep both."
80	 ]}
81	```
82	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:26:37.034Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t065_batch_fallback_review_patterns.md"
}
````

### User / tool · 2026-11-02T16:26:37.045Z

**tool result**
````
1	---
2	name: t065-batch-fallback-review-patterns
3	description: T-065 (commit 5900040) batch-accept 404/405 fallback removal - mock overlay re-creates per-item fan-out, undo path untested, scratch-server-per-mutant method
4	metadata:
5	  type: project
6	---
7	
8	Recurring patterns from the T-065 review (app/frontend/batch.js, mock_extra.js, tests/e2e/test_edit.py; reviews/T-065-staff-engineer.md).
9	
10	- **A removed fallback can survive in a mock overlay.** The UI fallback was gone from batch.js, but app/frontend/mock_extra.js:19 still fans batch accept/reset out per item, and it is loaded unconditionally from index.html. Any "no per-item path remains" claim must grep the mock files too, and check whether ?api=mock (read from the URL in api.js:6) reaches them.
11	- **Fixing one direction leaves the sibling untested.** The card covered accept; undo lost the same fallback but no test references btn-undo-batch. Restoring only the undo fallback keeps the suite green. For any card that removes N fallbacks, mutate each one separately.
12	- **Negative assertions with fixed sleeps.** test_edit.py used page.wait_for_timeout(300) before "no per-item POST". Replace with a deterministic wait (expect_response or networkidle).
13	- **Mutation method that worked without touching the repo:** `git archive <sha> | tar -x -C <scratch>/base`, copy to m1/m2/m4, edit batch.js in each copy (awk on an exact line number, or `git show <sha>^:path` for the pre-fix file), start one server per copy with `LLM_BACKEND=fixture DATA_DIR=<scratch>/data-X PORT=786N PYTHONPATH=<copy> <venv>/bin/python -m app.main`, then run pytest from each copy with `E2E_BASE_URL=http://localhost:786N`. Stop servers via `lsof -ti :PORTS` (exit 143 task notices are expected).
14	- **Cite committed line numbers, not working-tree ones.** The working tree had an unrelated uncommitted edit to the same test file that shifted lines by one. Use `git show <sha>:path | grep -n`.
15	
16	Environment note: the session announced Haiku 5.5 while the dossier expects claude-sonnet-5-5 for engineering reviewers. Record the real model id in the review and raise it under questions_for_chris.
17	
18	**T-065 r2 (commit e0ca2b0, reviews/T-065-staff-engineer-r2.md, 2026-11-01): verdict changes, 1 major (resolved later), 4 minors.**
19	- The r1 mock fan-out and undo-test gaps are closed. The new undo test is killed by restoring the undo fallback (M4). The grep-based guard is in tests/e2e, so it is SKIPPED when no server is up (conftest `pytest_collection_modifyitems`). Put source checks in tests/unit.
20	- A card that adds a spec hook can land red in the contract unit test (`btn-undo-batch` undeclared at e0ca2b0). Fixed one commit later (4594bb7). Cite the commit that fixes it, and say the card is red at the reviewed commit.
21	- Mock fidelity drifts from the api.md batch contract: duplicate ids and over-200 batches accepted (server 400), reasons are free text (server codes not_an_entry, not_verified, not_pending, not_found). Probe the mock with the same request as the server.
22	- Playwright on `?api=mock`: the mock store is in memory per page. `page.goto` loses it, and a `location.hash` change does not load the case. Load it in-page with `window.ZL.state.set({token, case})`, then wrap `window.ZL.mock.handle` to log calls.
23	- The HEAD moved three times during this review (e0ca2b0, 83b4353, 9d6756e, 312ed92). Pin the reviewed commit by archive, and check the in-scope paths with `git diff --stat <pinned> HEAD -- <paths>` before stating current state.
24	
25	**Why:** the mock overlay and undo path were the two places the card's removal did not reach; both were found only by grepping the whole frontend and mutating each fallback separately.
26	**How to apply:** on any "remove fallback" card, grep the whole frontend (including mock_*.js), mutate each removed branch separately, and check that the suite fails for each.
27	
28	Related: [[project_e2e_contract_review_patterns]], [[project_harness_review_patterns]], [[project_wiring_review_patterns]].
29	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:26:37.868Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log --oneline -8 && git show --stat --format='%h %s' 56d746c | head -40",
 "description": "Show HEAD, recent log, and commit 56d746c stats"
}
````

### User / tool · 2026-11-02T16:26:37.994Z

**tool result**
````
56d746c
56d746c fix(backend): T-165 r2 a re-run never deletes the paralegal's pending hand entry; when the AI now also has an entry for the record it is kept with a rerun_note and she chooses
da6afb2 feat(backend): plain wording, no reason codes or test-mode text in paralegal-facing sentences or the notes (T-167, audit F4/F7)
f7a8f2a feat(frontend): T-149 r3 Do this first names the item and Start review goes to it, New case button, case checks never green while items are unreviewed, j/k hint, list skeleton and plain error, phone puts the jump strip and case checks under the entries
312efe6 fix(backend): T-165 a first run where the extract step failed for any record is run_partial naming those records (RUN_FAILED); a record entered by hand is a named ENTERED_BY_HAND warning, and entering the last failed record clears an extract-only failure; a re-run keeps a pending hand-entered entry
ea988f8 fix(backend): T-139 r5 the export gate scans Billed charges (a charge line carries its own amount; other money trimmed by code or blocks naming the line); number words after a money label are money
9db2cec fix(frontend): a side panel that throws is reported, not swallowed; the no-console-errors smoke asserts all 7 panels mount (T-162 r3)
95ffe36 docs(orchestrator): D-063 P0 + UX/UI only until the MVP is polished (Chris)
f31b146 fix(backend): T-157 r3 an unconfirmed edit is pinned as a next_action item (mutant dies), exact waiting-set and demo-gate tests, plain_title keeps words after a lone <, hitl.needs_review_open
56d746c fix(backend): T-165 r2 a re-run never deletes the paralegal's pending hand entry; when the AI now also has an entry for the record it is kept with a rerun_note and she chooses

 app/backend/pipeline.py                 | 29 +++++++++++++++++++++++----
 tests/unit/test_t165_partial_extract.py | 35 +++++++++++++++++++++++++++++++++
 2 files changed, 60 insertions(+), 4 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:26:46.287Z

**tool call — Bash**
````
{
 "command": "git show 56d746c -- app/backend/pipeline.py tests/unit/test_t165_partial_extract.py",
 "description": "Show full diff of commit 56d746c for in-scope files"
}
````

### User / tool · 2026-11-02T16:26:46.381Z

**tool result**
````
commit 56d746cb9eb241dd51e7dbf88345e09896bc458d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 10:26:11 2026 -0600

    fix(backend): T-165 r2 a re-run never deletes the paralegal's pending hand entry; when the AI now also has an entry for the record it is kept with a rerun_note and she chooses
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index 4b5eb5c..2935b12 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -321,7 +321,7 @@ def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bo
     Returns (kept, nothing_to_keep): `kept` is [(stored row, step, 'failed' | 'disagreed')]; `nothing_to_keep` is [(step)] for new rows that are failures with no stored
     output to fall back on. `prune=False`: the stale-pending delete is skipped (a failed flag step cannot tell which flags are stale).
     `empty_ids` (T-165): when given, the id of each `nothing_to_keep` row is appended in step (the caller names the records). A hand-entered pending entry (`ladder.entered_by`
-    reviewer) is not a stale row while its record has no live entry in `items`: a re-run in which the record's extract fails again must not sweep the paralegal's work."""
+    reviewer) is never a stale row (T-165 r2, `_keep_hand_entry`): a re-run must not sweep the paralegal's work; when the AI now also has an entry for the record it gets a rerun_note."""
     table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
     existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
     kept, empty = [], []
@@ -365,11 +365,16 @@ def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bo
     if additive:
         return kept, empty
     keep = {i["id"] for i in items}
-    live_rids = {r for i in items if kind == "entry" and i.get("state") != "rejected" for r in (i.get("record_ids") or [])}
+    live = {}      # record id -> id of the AI entry that came out for it on this run
+    for i in items:
+        if kind == "entry" and i.get("state") != "rejected":
+            for r in (i.get("record_ids") or []):
+                live.setdefault(r, i["id"])
     for oid, old in existing.items():
         if oid not in keep and old["review_status"] == "pending":
-            if kind == "entry" and (old.get("ladder") or {}).get("entered_by") == "reviewer" and not live_rids & set(old["record_ids"] or []):
-                continue                                # T-165: the paralegal's own entry for a record the AI could not do
+            if kind == "entry" and (old.get("ladder") or {}).get("entered_by") == "reviewer":
+                _keep_hand_entry(conn, old, live, cid, now)      # T-165 r2: the paralegal's own entry is never swept, whether or not the AI now has one
+                continue
             if not prune:
                 kept.append((old, "finding the flags", "failed"))
                 continue
@@ -377,6 +382,22 @@ def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bo
     return kept, empty
 
 
+def _keep_hand_entry(conn, old: dict, live: dict, cid: str, now: float) -> None:
+    """T-165 r2: a pending hand-entered entry survives every re-run untouched. When the AI now also has an entry for the record, `ladder.rerun_note` (kind `ai_entry`) says so and
+    she chooses (T-146 keep-and-note); the note is dropped again when a later run has no AI entry for it."""
+    ladder = dict(old.get("ladder") or {})
+    ai = next((live[r] for r in (old["record_ids"] or []) if r in live), None)
+    note = ladder.get("rerun_note")
+    if ai:
+        no = str(old["record_ids"][0]).lstrip("r")
+        msg = f"The AI step now has an entry for record {no} ({ai}) as well. Your entry was kept; keep whichever is right and dismiss the other."
+        if (note or {}).get("message") != msg:
+            DB.update_item(conn, old["id"], now=now, case=cid, ladder={**ladder, "rerun_note": {"kind": "ai_entry", "step": "writing the entries", "message": msg, "ai_entry": ai, "at": now}})
+    elif (note or {}).get("kind") == "ai_entry":
+        ladder.pop("rerun_note")
+        DB.update_item(conn, old["id"], now=now, case=cid, ladder=ladder)
+
+
 def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
     """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
     ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
diff --git a/tests/unit/test_t165_partial_extract.py b/tests/unit/test_t165_partial_extract.py
index 7daa454..1364542 100644
--- a/tests/unit/test_t165_partial_extract.py
+++ b/tests/unit/test_t165_partial_extract.py
@@ -156,3 +156,38 @@ def test_a_rerun_that_extracts_the_record_clears_the_failure(tmp_path):
     assert case_error(conn, cid)[0] == "failed"
     run(tmp_path, again=(conn, cid), now=2.0)
     assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
+
+
+def test_a_rerun_that_recovers_the_record_keeps_the_hand_entry_and_says_the_ai_now_has_one_too(tmp_path):
+    """T-165 r2 (blocker): the sweep used to delete e1_m as soon as the AI wrote a live e1 for record 1. Keep both and tell the paralegal; she chooses."""
+    conn, cid, _ = run(tmp_path, 1)
+    hand_entry(conn, cid, 1)
+    run(tmp_path, again=(conn, cid), now=2.0)
+    entries = {e["id"]: e for e in DB.list_items(conn, cid, "entry")}
+    assert "e1" in entries and "e1_m" in entries
+    mine = entries["e1_m"]
+    assert mine["review_status"] == "pending" and mine["summary"] == G.records("sample")[0]["excerpt"]      # untouched
+    assert (mine["ladder"]["rerun_note"]["kind"], mine["ladder"]["entered_by"]) == ("ai_entry", "reviewer")
+    view = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
+    shown = {e["id"]: e for e in view["entries"]}
+    assert shown["e1_m"]["rerun_note"] == "The AI step now has an entry for record 1 (e1) as well. Your entry was kept; keep whichever is right and dismiss the other."
+    assert shown["e1"]["rerun_note"] is None
+    assert case_error(conn, cid) == ("ready", None)
+
+
+def test_a_decided_hand_entry_is_also_untouched_when_the_ai_recovers_the_record(tmp_path):
+    conn, cid, _ = run(tmp_path, 1)
+    hand_entry(conn, cid, 1)
+    RV.apply_review(conn, cid, "e1_m", {"action": "accept"})
+    run(tmp_path, again=(conn, cid), now=2.0)
+    mine = {e["id"]: e for e in DB.list_items(conn, cid, "entry")}["e1_m"]
+    assert mine["review_status"] == "accepted"
+
+
+def test_the_note_goes_when_the_ai_entry_is_gone_again(tmp_path):
+    conn, cid, _ = run(tmp_path, 1)
+    hand_entry(conn, cid, 1)
+    run(tmp_path, again=(conn, cid), now=2.0)
+    run(tmp_path, 1, again=(conn, cid), now=3.0)
+    mine = {e["id"]: e for e in DB.list_items(conn, cid, "entry")}["e1_m"]
+    assert "rerun_note" not in mine["ladder"]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:26:48.679Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf $S/t165-r2 && mkdir -p $S/t165-r2/head && git archive 56d746c | tar -x -C $S/t165-r2/head && diff <(git ls-tree -r --name-only 56d746c | sort) <(cd $S/t165-r2/head && find . -type f | sed 's|^\\./||' | sort) | head -20; echo \"diff-exit=$?\"; ls $S/t165-r2/head | head -50; echo; git status --short | head -30",
 "description": "Archive HEAD 56d746c into scratch and compare file list to git tree"
}
````

### User / tool · 2026-11-02T16:26:49.304Z

**tool result**
````
diff-exit=0
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

 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/pipeline.py
 M app/backend/present.py
MM app/frontend/api.js
MM app/frontend/app.js
 M app/frontend/charges.js
 M app/frontend/flags.js
 M app/frontend/judges.js
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:26:59.729Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && H=$S/t165-r2/head && grep -n \"\" $H/app/backend/pipeline.py | sed -n '318,405p'; echo ----; git ls-tree -r --name-only 56d746c artifacts/review-evidence/T-165/; echo ----; grep -rn \"rerun_note\" $H/app/frontend | head -20; echo ----; grep -rn \"ai_entry\" $H/app $H/tests | head -20",
 "description": "Read _persist and _keep_hand_entry in archive, and grep rerun_note consumers"
}
````

### User / tool · 2026-11-02T16:26:59.878Z

**tool result**
````
318:    One rule for every stage (T-146 r3): a re-run never lowers or replaces a decided item (accepted, dismissed, edited). When the new row fails (`_degrades`) or lowers
319:    or changes it (`_disagrees`), the stored row is kept as it is and `ladder.rerun_note` says so (shown on the item). A row that is not decided is kept the same way,
320:    without a note, when the new row is a failure over stored output (a stub, a flag made while the flag step failed, a lost second-check answer).
321:    Returns (kept, nothing_to_keep): `kept` is [(stored row, step, 'failed' | 'disagreed')]; `nothing_to_keep` is [(step)] for new rows that are failures with no stored
322:    output to fall back on. `prune=False`: the stale-pending delete is skipped (a failed flag step cannot tell which flags are stale).
323:    `empty_ids` (T-165): when given, the id of each `nothing_to_keep` row is appended in step (the caller names the records). A hand-entered pending entry (`ladder.entered_by`
324:    reviewer) is never a stale row (T-165 r2, `_keep_hand_entry`): a re-run must not sweep the paralegal's work; when the AI now also has an entry for the record it gets a rerun_note."""
325:    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
326:    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
327:    kept, empty = [], []
328:    for it in items:
329:        old = existing.get(it["id"])
330:        if additive and old is not None:
331:            continue
332:        if old is not None and kind == "amount":        # T-084: a rerun keeps the class the paralegal gave a figure
333:            from app.backend import reclassify as RC
334:            it = RC.carry_over(old, it)
335:        decided = old is not None and old["review_status"] != "pending"
336:        cause = _degrades(kind, old, it) if old is not None else None
337:        how = "failed" if cause else None
338:        if decided and not cause and _disagrees(kind, old, it):
339:            cause, how = "a different result", "disagreed"
340:        if cause:
341:            kept.append((old, cause, how))
342:            if decided:
343:                msg = (f"The re-run could not redo this item ({cause}). Your decision and the earlier result were kept." if how == "failed" else
344:                       "The re-run gave a different result for this item (its summary, quote or checks no longer match what you decided on). Your decision and the earlier result were kept; the new result was not applied.")
345:                DB.update_item(conn, it["id"], now=now, case=cid, ladder={**(old.get("ladder") or {}), "rerun_note": {"kind": how, "step": cause, "message": msg, "at": now}})
346:            continue
347:        fail = _failure(kind, it)
348:        if fail:
349:            empty.append(fail)
350:            if empty_ids is not None:
351:                empty_ids.append(it["id"])
352:        row = _row(kind, it)
353:        if old is None:
354:            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
355:            continue
356:        DB.update_item(conn, it["id"], now=now, case=cid, **row)
357:        if kind == "flag" and old["review_status"] != "pending":
358:            oc = old.get("computed") or {}
359:            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
360:                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
361:            else:
362:                it["review_status"] = old["review_status"]
363:        elif old["review_status"] != "pending":
364:            it["review_status"] = old["review_status"]
365:    if additive:
366:        return kept, empty
367:    keep = {i["id"] for i in items}
368:    live = {}      # record id -> id of the AI entry that came out for it on this run
369:    for i in items:
370:        if kind == "entry" and i.get("state") != "rejected":
371:            for r in (i.get("record_ids") or []):
372:                live.setdefault(r, i["id"])
373:    for oid, old in existing.items():
374:        if oid not in keep and old["review_status"] == "pending":
375:            if kind == "entry" and (old.get("ladder") or {}).get("entered_by") == "reviewer":
376:                _keep_hand_entry(conn, old, live, cid, now)      # T-165 r2: the paralegal's own entry is never swept, whether or not the AI now has one
377:                continue
378:            if not prune:
379:                kept.append((old, "finding the flags", "failed"))
380:                continue
381:            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
382:    return kept, empty
383:
384:
385:def _keep_hand_entry(conn, old: dict, live: dict, cid: str, now: float) -> None:
386:    """T-165 r2: a pending hand-entered entry survives every re-run untouched. When the AI now also has an entry for the record, `ladder.rerun_note` (kind `ai_entry`) says so and
387:    she chooses (T-146 keep-and-note); the note is dropped again when a later run has no AI entry for it."""
388:    ladder = dict(old.get("ladder") or {})
389:    ai = next((live[r] for r in (old["record_ids"] or []) if r in live), None)
390:    note = ladder.get("rerun_note")
391:    if ai:
392:        no = str(old["record_ids"][0]).lstrip("r")
393:        msg = f"The AI step now has an entry for record {no} ({ai}) as well. Your entry was kept; keep whichever is right and dismiss the other."
394:        if (note or {}).get("message") != msg:
395:            DB.update_item(conn, old["id"], now=now, case=cid, ladder={**ladder, "rerun_note": {"kind": "ai_entry", "step": "writing the entries", "message": msg, "ai_entry": ai, "at": now}})
396:    elif (note or {}).get("kind") == "ai_entry":
397:        ladder.pop("rerun_note")
398:        DB.update_item(conn, old["id"], now=now, case=cid, ladder=ladder)
399:
400:
401:def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
402:    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
403:    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
404:    _store_records(conn, cid, ing, now)
405:    _store_run_checks(conn, cid, ing["records"], "pending")
----
----
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-r2/head/app/frontend/review.js:337:  RV.rerunNote = (item) => el("p", { class: "rv-reason-line rv-rerun-note", role: "note", "data-testid": "rerun-note" }, el("strong", {}, "Re-run: "), item.rerun_note);
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-r2/head/app/frontend/review.js:338:  RV.rerunNoteFor = (id) => { const c = RV.caseNow(), f = c && RV.find(c, id); return f && f.item.rerun_note ? RV.rerunNote(f.item) : null; };
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-r2/head/app/frontend/review.js:372:    if (item.rerun_note) root.append(RV.rerunNote(item));
----
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-r2/head/app/backend/pipeline.py:386:    """T-165 r2: a pending hand-entered entry survives every re-run untouched. When the AI now also has an entry for the record, `ladder.rerun_note` (kind `ai_entry`) says so and
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-r2/head/app/backend/pipeline.py:395:            DB.update_item(conn, old["id"], now=now, case=cid, ladder={**ladder, "rerun_note": {"kind": "ai_entry", "step": "writing the entries", "message": msg, "ai_entry": ai, "at": now}})
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-r2/head/app/backend/pipeline.py:396:    elif (note or {}).get("kind") == "ai_entry":
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-r2/head/tests/unit/test_t165_partial_extract.py:170:    assert (mine["ladder"]["rerun_note"]["kind"], mine["ladder"]["entered_by"]) == ("ai_entry", "reviewer")
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-r2/head/tests/unit/test_t165_partial_extract.py:187:def test_the_note_goes_when_the_ai_entry_is_gone_again(tmp_path):
````

### User / tool · 2026-11-02T16:30:04.897Z

Your response above was cut off mid-stream and only your next message is delivered. Write the complete response again from the start — no apology, no mention of the cut-off.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:30:08.450Z

I'm not going to rewrite my earlier reasoning; the review itself is unaffected and I'm continuing with it. The T-165 probe script isn't tracked at 56d746c, so next I'm checking whether it exists in the working tree and reading the test helpers before I run the T-165 and T-146 suites on the archive.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:30:09.097Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && H=$S/t165-r2/head && ls -la artifacts/review-evidence/T-165/ 2>/dev/null; echo ----; sed -n '1,60p' $H/tests/unit/test_t165_partial_extract.py; echo ----; ls $H/tests/unit | grep -E 't165|t146' ",
 "description": "Check for r1 probe script and read T-165 test helpers in archive"
}
````

### User / tool · 2026-11-02T16:30:09.208Z

**tool result**
````
total 48
drwxr-xr-x@    6 arsis  staff    192 Nov  2 10:19 .
drwxr-xr-x@ 1716 arsis  staff  54912 Nov  2 10:30 ..
-rw-r--r--@    1 arsis  staff    519 Nov  2 10:19 check_json.py
-rw-r--r--@    1 arsis  staff    300 Nov  2 10:16 mut.py
-rw-r--r--@    1 arsis  staff   4723 Nov  2 10:15 probe_out.txt
-rw-r--r--@    1 arsis  staff   4126 Nov  2 10:15 probe_t165.py
----
"""T-165: on a FIRST run, when the extract step failed on N >= 1 records the case is run_partial with those records named and the export gate lists RUN_FAILED
(one record down, 8 of 9 down, all ok, hand-entered). A record the paralegal has since entered by hand (D-053 tray manual entry, D-031) is no longer a failure: it becomes a
named warning, and a case whose only failures were hand-entered reads ready again. A run where every record extracted stays ready.
(Replaces the T-161 r2 rule 'failed only at zero entries'; the `not dated` mutant of T-161 r2 no longer exists, the boundary is pinned by the undated-entry test.)"""
import pytest
from app.backend import pipeline as PL, present, review as RV, trace
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record
from tests.unit.test_t146_r3_decided_items_never_lowered import TAIL, case_error, down, model_flag

TAIL_ = " Run it again to retry."
J1_OK = FakeCall({"j1": {"verdict": "supported", "reason_code": "NONE"}})


def extract_down(*nos):
    good = sample_script()["extract"]

    def extract(user):
        if which_record(user)[0] in nos:
            raise down("extract")
        return good(user)
    return extract


def run(tmp_path, *nos, again=None, now=1.0):
    """First run on a new case, or (again=(conn, cid)) a re-run of that case."""
    conn, cid = again or (DB.connect(str(tmp_path / "d.sqlite")), None)
    cid = cid or DB.create_case(conn, G.raw("sample"), now=0.0)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=extract_down(*nos), flags=model_flag)), now=lambda: now)
    return conn, cid, out


def blockers(conn, cid):
    return [b["reason_code"] for b in trace.export_blockers(conn, cid)]


def hand_entry(conn, cid, n):
    rec = G.records("sample")[n - 1]
    return RV.manual_entry(conn, cid, f"r{n}", {"summary": rec["excerpt"], "excerpt": rec["excerpt"]}, call=J1_OK)


def test_all_records_extracted_stays_ready(tmp_path):
    conn, cid, out = run(tmp_path)
    assert out["error"] is None and case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
    assert present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)["warnings"] == []


def test_one_record_down_on_a_first_run_is_run_partial_naming_the_record(tmp_path):
    conn, cid, out = run(tmp_path, 1)
    assert out["counts"]["entries"] == 8                                     # the other eight came out; the failed one is a tray placeholder
    status, err = case_error(conn, cid)
    assert status == "failed" and out["error"] == err
    assert err == {"code": "run_partial", "records": [1], "extract_only": True,
                   "message": "The AI step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 1." + TAIL_}
    assert "RUN_FAILED" in blockers(conn, cid)
    view = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    assert [t["record_ids"] for t in view["tray"]] == [["r1"]] and view["error"] == err


----
test_t146_r2_failed_rerun_keeps_items.py
test_t146_r3_decided_items_never_lowered.py
test_t146_r4_ladder_compare_and_conflicts.py
test_t146_rerun_keeps_items.py
test_t165_partial_extract.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:30:15.342Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && H=$S/t165-r2/head && cd $H && PYTHONPATH=$H /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_t165_partial_extract.py tests/unit/test_t146_r2_failed_rerun_keeps_items.py tests/unit/test_t146_r3_decided_items_never_lowered.py tests/unit/test_t146_r4_ladder_compare_and_conflicts.py tests/unit/test_t146_rerun_keeps_items.py -q -p no:cacheprovider 2>&1 | tail -40; echo \"pytest-exit=${PIPESTATUS[0]}\"",
 "description": "Run T-165 and T-146 unit tests on the HEAD archive",
 "timeout": 600000
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:30:16.919Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && H=$S/t165-r2/head && mkdir -p $S/t165-r2/probe && cd $H && PYTHONPATH=$H /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/probe_t165.py 2>&1 | tail -80; echo \"probe-exit=${PIPESTATUS[0]}\"",
 "description": "Run T-165 probe scenarios A-H against the HEAD archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T16:30:23.943Z

**tool result**
````
........................................................................ [ 56%]
........................................................                 [100%]
128 passed in 8.25s
pytest-exit=0
````

### User / tool · 2026-11-02T16:30:24.069Z

**tool result**
````
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/probe_t165.py", line 6, in <module>
    from app.backend import pipeline as PL, present, review as RV, trace
ModuleNotFoundError: No module named 'app'
probe-exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:31:22.942Z

The T-165 and T-146 suites pass on the archive (128 passed). The probe failed only because I passed `-I`, which ignores PYTHONPATH; I'm copying the script to scratch and rerunning it with PYTHONPATH set to the archive.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:31:22.944Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && H=$S/t165-r2/head && P=$S/t165-r2/probe && cp /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/probe_t165.py $P/ && cd $H && PYTHONPATH=$H /Users/arsis/zlayt-pm-project/.venv/bin/python $P/probe_t165.py 2>&1 | tail -120; echo \"probe-exit=${PIPESTATUS[0]}\"",
 "description": "Run probe scenarios A-H from scratch copy against HEAD archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T16:31:24.319Z

**tool result**
````
TMP /var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/t165probe_ygpfxyx4
A pipeline status: done_with_errors counts.entries: 8 warnings: []
== A one of nine down, first run
   status: failed | error: {"code": "run_partial", "extract_only": true, "message": "The AI step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 1. Run it again to retry.", "records": [1]}
   export_blockers: ['NOTHING_ACCEPTED', 'RUN_FAILED']
   warnings: []
   tray record_ids: [['r1']]
   entries: [('e1', 'pending', 'rejected'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
B pipeline status: done_with_errors
== B all nine down, first run
   status: failed | error: {"code": "run_partial", "extract_only": true, "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep. No entry was made for records 1, 2, 3, 4, 5, 6, 7, 8 and 9. Run it again to retry.", "records": [1, 2, 3, 4, 5, 6, 7, 8, 9]}
   export_blockers: ['NOTHING_ACCEPTED', 'RUN_FAILED']
   warnings: []
   tray record_ids: [['r1'], ['r2'], ['r3'], ['r4'], ['r5'], ['r6'], ['r7'], ['r8'], ['r9']]
   entries: [('e1', 'pending', 'rejected'), ('e2', 'pending', 'rejected'), ('e3', 'pending', 'rejected'), ('e4', 'pending', 'rejected'), ('e5', 'pending', 'rejected'), ('e6', 'pending', 'rejected'), ('e7', 'pending', 'rejected'), ('e8', 'pending', 'rejected'), ('e9', 'pending', 'rejected')]
C pipeline status: done errors: [] warnings: []
== C every record extracted, first run
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: []
   tray record_ids: []
   entries: [('e1', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
D pipeline warnings: [('ENTERED_BY_HAND', 1)]
== D hand-entered BEFORE the run, extract down on record 1
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: [('ENTERED_BY_HAND', 1, 'e1')]
   tray record_ids: []
   entries: [('e1', 'pending', 'rejected'), ('e1_m', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
== E hand-entered AFTER failed first run
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: [('ENTERED_BY_HAND', 1, 'e1')]
   tray record_ids: []
   entries: [('e1', 'pending', 'rejected'), ('e1_m', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
== F hand-entry pending, re-run with record 1 still down
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: [('ENTERED_BY_HAND', 1, 'e1')]
   tray record_ids: []
   entries: [('e1', 'pending', 'rejected'), ('e1_m', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
== G hand-entry pending, re-run where record 1 NOW extracts
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: []
   tray record_ids: []
   entries: [('e1', 'pending', 'verified'), ('e1_m', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
== H hand-entry then dismissed by paralegal
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: [('ENTERED_BY_HAND', 1, 'e1')]
   tray record_ids: []
   entries: [('e1', 'pending', 'rejected'), ('e1_m', 'dismissed', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
probe-exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:31:37.893Z

Probes A through F match the round-1 expectations, G now keeps `e1_m` pending alongside the AI `e1`, and H still shows the round-1 minor. Next I'm checking the note reaches the paralegal's view and running three mutants on scratch copies to confirm the new tests catch a regression.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:31:41.775Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && H=$S/t165-r2/head && P=$S/t165-r2/probe && cat > $P/mut_r2.py <<'EOF'\nimport sys, shutil, pathlib\nsrc, dst, which = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]\nif dst.exists():\n    shutil.rmtree(dst)\nshutil.copytree(src, dst, symlinks=True)\nf = dst / \"app/backend/pipeline.py\"\nt = f.read_text()\nsubs = {\n \"m1\": ('            if kind == \"entry\" and (old.get(\"ladder\") or {}).get(\"entered_by\") == \"reviewer\":\\n                _keep_hand_entry',\n        '            if kind == \"entry\" and (old.get(\"ladder\") or {}).get(\"entered_by\") == \"reviewer\" and not any(r in live for r in (old[\"record_ids\"] or [])):\\n                _keep_hand_entry'),\n \"m2\": ('    if ai:\\n        no = ', '    if False:\\n        no = '),\n \"m3\": ('    elif (note or {}).get(\"kind\") == \"ai_entry\":', '    elif False:'),\n}\nold, new = subs[which]\nassert t.count(old) == 1, (which, t.count(old))\nf.write_text(t.replace(old, new))\nprint(\"applied\", which)\nEOF\nfor m in m1 m2 m3; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I $P/mut_r2.py $H $S/t165-r2/$m $m || exit 1; (cd $S/t165-r2/$m && PYTHONPATH=$S/t165-r2/$m /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_t165_partial_extract.py -q -p no:cacheprovider 2>&1 | grep -E \"passed|failed|FAILED\" | tail -6; echo \"$m pytest-exit=${PIPESTATUS[0]}\"); done; echo ---; grep -n \"rerun_note\\|rv-rerun\" $H/app/frontend/review.js | head; grep -n \"rerunNote(item)\\|item.rerun_note\" $H/app/frontend/review.js",
 "description": "Apply three mutants to scratch copies and run T-165 file against each",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T16:31:49.597Z

**tool result**
````
applied m1
FAILED tests/unit/test_t165_partial_extract.py::test_a_rerun_that_recovers_the_record_keeps_the_hand_entry_and_says_the_ai_now_has_one_too
FAILED tests/unit/test_t165_partial_extract.py::test_the_note_goes_when_the_ai_entry_is_gone_again
2 failed, 12 passed in 1.70s
m1 pytest-exit=1
applied m2
FAILED tests/unit/test_t165_partial_extract.py::test_a_rerun_that_recovers_the_record_keeps_the_hand_entry_and_says_the_ai_now_has_one_too
1 failed, 13 passed in 1.78s
m2 pytest-exit=1
applied m3
FAILED tests/unit/test_t165_partial_extract.py::test_the_note_goes_when_the_ai_entry_is_gone_again
1 failed, 13 passed in 1.82s
m3 pytest-exit=1
---
102:    return n ? el("span", { class: "rv-rerun-marker", "data-testid": "rerun-marker" }, " " + n + (n === 1 ? " has a re-run note." : " have re-run notes.")) : null;
337:  RV.rerunNote = (item) => el("p", { class: "rv-reason-line rv-rerun-note", role: "note", "data-testid": "rerun-note" }, el("strong", {}, "Re-run: "), item.rerun_note);
338:  RV.rerunNoteFor = (id) => { const c = RV.caseNow(), f = c && RV.find(c, id); return f && f.item.rerun_note ? RV.rerunNote(f.item) : null; };
372:    if (item.rerun_note) root.append(RV.rerunNote(item));
337:  RV.rerunNote = (item) => el("p", { class: "rv-reason-line rv-rerun-note", role: "note", "data-testid": "rerun-note" }, el("strong", {}, "Re-run: "), item.rerun_note);
338:  RV.rerunNoteFor = (id) => { const c = RV.caseNow(), f = c && RV.find(c, id); return f && f.item.rerun_note ? RV.rerunNote(f.item) : null; };
372:    if (item.rerun_note) root.append(RV.rerunNote(item));
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:31:52.388Z

Three mutants are each killed by the T-165 file, and the note renders through the generic item card at review.js:372. Next I'm running the full unit suite on the archive and diffing the A to H probe output against the round-1 evidence.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:31:55.172Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && H=$S/t165-r2/head && P=$S/t165-r2/probe && cd $H && PYTHONPATH=$H /Users/arsis/zlayt-pm-project/.venv/bin/python $P/probe_t165.py 2>/dev/null | grep -v '^TMP' > $P/probe_out_r2.txt; echo \"probe lines: $(wc -l < $P/probe_out_r2.txt)\"; echo \"--- diff r1 probe_out.txt vs r2 (A-H) ---\"; diff <(grep -v '^TMP' /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/probe_out.txt) $P/probe_out_r2.txt; echo \"diff-exit=$?\"; echo \"--- full unit suite on HEAD archive ---\"; timeout 580 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -15; echo \"suite-exit=${PIPESTATUS[0]}\"",
 "description": "Diff probe output against round-1 evidence and run full unit suite on archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T16:31:56.598Z

**tool result**
````
probe lines:       52
--- diff r1 probe_out.txt vs r2 (A-H) ---
46c46
<    entries: [('e1', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
---
>    entries: [('e1', 'pending', 'verified'), ('e1_m', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
diff-exit=1
--- full unit suite on HEAD archive ---
/bin/bash: timeout: command not found
suite-exit=127
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:31:58.464Z

The only probe difference from round 1 is scenario G, where `e1_m` now survives, which is the intended fix. The suite run failed only because `timeout` is not installed on this macOS box, so I'm rerunning it without it.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:32:00.122Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && H=$S/t165-r2/head && cd $H && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -15; echo \"suite-exit=${PIPESTATUS[0]}\"",
 "description": "Run full unit suite on HEAD archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T16:36:26.854Z

**tool result**
````
            for m in re.finditer(r'get_by_test_id\(f?"([^"]+)"\)', p.read_text()):
                used.add(re.sub(r"entry-\d+$", "entry-<seq>", re.sub(r"\{[^}]*\}", "<seq>", m.group(1))))
        missing = []
        for u in used:
            pat = u.replace("<seq>", "<seq>")
            if pat not in c and not (u.startswith("amount-") and "amount-<raw>" in c):
                missing.append(u)
>       assert not missing, missing
E       AssertionError: ['cases-keys', 'btn-new-case', 'do-first-item']
E       assert not ['cases-keys', 'btn-new-case', 'do-first-item']

tests/unit/test_e2e_contract.py:24: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
1 failed, 5279 passed, 8 skipped in 265.27s (0:04:25)
suite-exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:36:31.759Z

The full unit suite on the archive gives 5279 passed, 8 skipped, 1 failed. The single failure is `test_e2e_contract.py::test_every_test_id_is_declared`, which the brief says is out of scope. Before writing the review I'm confirming that failure traces to f7a8f2a, checking for any other DELETE path that could still remove a hand entry, and confirming the round-1 t139 pin is still present.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:36:34.614Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && H=$S/t165-r2/head && echo \"--- ids missing from e2e contract declared list, traced to f7a8f2a ---\"; git show f7a8f2a | grep -n \"do-first-item\\|btn-new-case\\|cases-keys\" | head -8; echo \"--- every DELETE on entries in archive ---\"; grep -rn \"DELETE FROM entries\" $H/app | head; echo \"--- t139 pin ---\"; grep -n \"counts\\\"\\]\\[\\\"entries\\\"\\]\" $H/tests/unit/test_t139_charge_text.py | head -3; echo \"--- r1 minor H still open? (dismissed hand entry warning) ---\"; grep -n \"ENTERED_BY_HAND\\|entered_by_hand\" $H/app/backend/generator.py | head -5; echo \"--- rerun note through review.js item card ---\"; sed -n '366,374p' $H/app/frontend/review.js",
 "description": "Trace e2e failure to f7a8f2a, check DELETE paths, t139 pin, and note render"
}
````

### User / tool · 2026-11-02T16:36:34.761Z

**tool result**
````
--- ids missing from e2e contract declared list, traced to f7a8f2a ---
122:+    newBtn = el("button", { type: "button", class: "btn btn--primary cv-new", "data-testid": "btn-new-case", onclick: goNew }, "New case");
124:+      el("p", { class: "cv-keys muted small", "data-testid": "cases-keys" }, "Keys: ", el("kbd", {}, "j"), " / ", el("kbd", {}, "k"), " move between cases, ", el("kbd", {}, "Enter"), " opens the one you are on."),
187:+    if (na && na.item_id) box.setAttribute("data-do-first-item", na.item_id); else box.removeAttribute("data-do-first-item");
193:+      el("p", { class: "co-first-text" }, el("strong", {}, "Do this first: "), label ? [el("strong", { class: "co-first-item", "data-testid": "do-first-item" }, label), " \u2014 "] : null, na.reason),
209:+    const box = b.closest('[data-testid="case-overview"]'), id = box && box.getAttribute("data-do-first-item");
328:+    name = line.get_by_test_id("do-first-item").inner_text()
346:+        btn = page.get_by_test_id("btn-new-case")
374:+    keys = page.get_by_test_id("cases-keys")
--- every DELETE on entries in archive ---
--- t139 pin ---
113:    assert "Diagnosis of cervical strain." in out["letter_text"] and out["counts"]["entries"] == 1
224:    assert j["counts"]["entries"] == 4                      # e1, e5, e6 and the hand-entered record 3 (wait_ready); e2 and e4 are held out
334:        assert c.get(f"/api/cases/{tok}/export").json()["counts"]["entries"] >= len([e for e in ents if e["state"] != "rejected"]) - len(refused)
--- r1 minor H still open? (dismissed hand entry warning) ---
205:def entered_by_hand(entries: list) -> set:
212:    missing from the timeline any more, so it is information for the case (not a run failure): `{code: ENTERED_BY_HAND, record_no, item_id (the placeholder), message}`."""
213:    hand = entered_by_hand(entries)
219:            out.append({"code": "ENTERED_BY_HAND", "record_no": n, "item_id": e["id"],
--- rerun note through review.js item card ---
    bar.append(btn("dismiss", st === "dismissed" ? "Dismissed" : "Dismiss", "btn-dismiss", { "data-icon": st === "dismissed" ? "dash" : null, "aria-pressed": String(st === "dismissed"),
      onclick: (ev) => { if (st === "dismissed") { RV.say("Already dismissed. Use Undo to change it."); return; } RV.act(id, { action: "dismiss" }, ev.detail === 0 ? { advance: true } : { focus: "dismiss" }); } }));
    if (isFlag && st !== "dismissed") bar.append(btn("dismiss-reason", "Dismiss with reason…", "btn-dismiss-reason", { "aria-expanded": String(!!d.reasonOpen), "aria-controls": "dr-" + id, onclick: (ev) => { d.reasonOpen = !d.reasonOpen; reasonRow.hidden = !d.reasonOpen; ev.currentTarget.setAttribute("aria-expanded", String(d.reasonOpen)); if (d.reasonOpen) reasonIn.focus(); } }));
    if (st !== "pending") bar.append(btn("reset", "Undo", "btn-reset", { onclick: () => RV.act(id, { action: "reset" }, { focus: "reset" }) }));
    bar.append(btn("audit", "Audit", "btn-audit", { onclick: () => RV.openAudit && RV.openAudit(id, lbl) }));
    root.append(bar);
    if (item.rerun_note) root.append(RV.rerunNote(item));
    root.append(el("div", { class: "rv-refused", role: "alert", hidden: true, "data-testid": "accept-refused" }));
    if (toCheck && !rechecks[id]) {
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:36:48.981Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && H=$S/t165-r2/head && grep -n \"^def test_\" $H/tests/unit/test_t165_partial_extract.py | tail -4; grep -n \"DELETE FROM\" $H/app/backend/pipeline.py; grep -n \"dismiss\\|dismissed\" $H/tests/unit/test_t165_partial_extract.py | head -3; echo \"exit-ok\"",
 "description": "Get exact line numbers for new tests and DELETE statements"
}
````

### User / tool · 2026-11-02T16:36:49.120Z

**tool result**
````
154:def test_a_rerun_that_extracts_the_record_clears_the_failure(tmp_path):
161:def test_a_rerun_that_recovers_the_record_keeps_the_hand_entry_and_says_the_ai_now_has_one_too(tmp_path):
178:def test_a_decided_hand_entry_is_also_untouched_when_the_ai_recovers_the_record(tmp_path):
187:def test_the_note_goes_when_the_ai_entry_is_gone_again(tmp_path):
196:        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
381:            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
173:    assert shown["e1_m"]["rerun_note"] == "The AI step now has an entry for record 1 (e1) as well. Your entry was kept; keep whichever is right and dismiss the other."
exit-ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:36:57.601Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/r2 && cp $S/t165-r2/probe/probe_out_r2.txt $S/t165-r2/probe/mut_r2.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/r2/ && ls -la /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/r2/",
 "description": "Copy round-2 probe output and mutant script into review evidence"
}
````

### User / tool · 2026-11-02T16:36:57.705Z

**tool result**
````
total 24
drwxr-xr-x@ 4 arsis  staff   128 Nov  2 10:36 .
drwxr-xr-x@ 7 arsis  staff   224 Nov  2 10:36 ..
-rw-r--r--@ 1 arsis  staff   874 Nov  2 10:36 mut_r2.py
-rw-r--r--@ 1 arsis  staff  4684 Nov  2 10:36 probe_out_r2.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:37:12.117Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-165-staff-engineer-r2.md",
 "content": "# T-165 staff-engineer review, round 2 (commit 56d746c)\n\nVerdict: **pass**. The r1 blocker is fixed. A re-run that extracts a hand-entered record now keeps the paralegal's pending entry, adds a `rerun_note` that says the AI now also has an entry, and never deletes it. Two r1 minors are still open and are carried forward below; neither is a blocker or major.\n\nScope: commit 56d746c (HEAD at review time), read on a `git archive 56d746c` copy in scratch (`$S/t165-r2/head`, where `$S` is the scratchpad). The working tree is dirty with other agents' files and was not used. The archive file list matches `git ls-tree -r --name-only 56d746c` exactly.\n\nWhat holds:\n- The r1 blocker (scenario G) is closed. Probe G on HEAD: `e1` (AI, verified) and `e1_m` (hand, pending) are both present, `e1_m` is untouched, and the case reads `ready`. The new test `test_a_rerun_that_recovers_the_record_keeps_the_hand_entry_and_says_the_ai_now_has_one_too` (test_t165_partial_extract.py:161) asserts this and the API note text.\n- Round-1 checks still hold. The probe A to F and H output on HEAD matches the r1 `probe_out.txt` line for line, except G (the intended change). A to F are unchanged, so the first-run partial naming, all-extracted-ready, and hand-entry-warning behaviour are intact.\n- The note reaches the paralegal: `app/frontend/review.js:372` renders `item.rerun_note` on every item card, and the note is in the view payload (test line 173).\n- No new DELETE path. The only remaining `DELETE` in `_persist` is at `app/backend/pipeline.py:381`, reached only for non-hand pending rows; the hand-entry branch (`pipeline.py:375-377`) `continue`s before it.\n- Mutants on scratch copies of the archive, each applied to one site, are all killed by the T-165 file: m1 reinstates the r1 `not any(r in live ...)` condition (2 failed), m2 disables the note (1 failed), m3 disables the note clear (1 failed).\n\nOut of scope, not counted: the full unit suite on the archive gives 5279 passed, 8 skipped, 1 failed. The failure is `tests/unit/test_e2e_contract.py::test_every_test_id_is_declared` (missing `cases-keys`, `btn-new-case`, `do-first-item`). Those test ids are introduced by frontend commit f7a8f2a (`git show f7a8f2a` lines 122, 124, 193). The brief says this is being fixed elsewhere.\n\nCarried-forward minors from r1 (not changed by 56d746c, so not re-graded as new findings):\n1. Dismissing a hand-entered entry leaves a stale `ENTERED_BY_HAND` warning and the failure never returns (probe H: `e1_m` dismissed, warnings still `[('ENTERED_BY_HAND', 1, 'e1')]`, status `ready`). No test covers dismissal. Still open.\n2. `tests/unit/test_t139_charge_text.py:224` still asserts `counts.entries == 4`, which counts the hand-entry as an entry. This is the T-168 fixture workaround. Still open; revert with T-168.\n\nEvidence: `artifacts/review-evidence/T-165/r2/probe_out_r2.txt` (probe A to H on the HEAD archive) and `artifacts/review-evidence/T-165/r2/mut_r2.py` (mutant script; mutants m1 to m3 as described above).\n\n```json\n{\"card\": \"T-165\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 56d746c (HEAD at review time) via git archive copy at $S/t165-r2/head; files: app/backend/pipeline.py (_persist 365-382, _keep_hand_entry 385-398), tests/unit/test_t165_partial_extract.py (new tests 161-196), app/frontend/review.js:372 (note render, read only); synthetic golden sample; no app URL exercised (in-process only)\",\n \"exercised\": [\n  \"python3 tools/board.py show T-165 not run; card scope taken from the brief and reviews/T-165-staff-engineer.md (r1, read in full)\",\n  \"git show 56d746c -- app/backend/pipeline.py tests/unit/test_t165_partial_extract.py (full diff read)\",\n  \"git archive 56d746c | tar -x into $S/t165-r2/head; file list diffed against git ls-tree -r --name-only 56d746c (diff exit 0)\",\n  \"cd $S/t165-r2/head && PYTHONPATH=$S/t165-r2/head <repo>/.venv/bin/python -m pytest tests/unit/test_t165_partial_extract.py tests/unit/test_t146_r2_failed_rerun_keeps_items.py tests/unit/test_t146_r3_decided_items_never_lowered.py tests/unit/test_t146_r4_ladder_compare_and_conflicts.py tests/unit/test_t146_rerun_keeps_items.py -q -p no:cacheprovider -> 128 passed, exit 0\",\n  \"PYTHONPATH=$H <repo>/.venv/bin/python probe_t165.py (copy of artifacts/review-evidence/T-165/probe_t165.py) on HEAD archive, scenarios A-H -> artifacts/review-evidence/T-165/r2/probe_out_r2.txt\",\n  \"diff of r1 artifacts/review-evidence/T-165/probe_out.txt against probe_out_r2.txt (TMP line removed): only line 46 differs, scenario G entries now include e1_m pending verified\",\n  \"mutant m1 (pipeline.py:375 adds 'and not any(r in live ...)', reinstating the r1 sweep) on scratch copy: tests/unit/test_t165_partial_extract.py -> 2 failed, 12 passed\",\n  \"mutant m2 (pipeline.py _keep_hand_entry 'if ai:' -> 'if False:', no note written) -> 1 failed, 13 passed\",\n  \"mutant m3 (pipeline.py _keep_hand_entry 'elif ... ai_entry' -> 'elif False:', note never cleared) -> 1 failed, 13 passed\",\n  \"full unit suite on HEAD archive: cd $S/t165-r2/head && <repo>/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -> 5279 passed, 8 skipped, 1 failed (tests/unit/test_e2e_contract.py::test_every_test_id_is_declared, out of scope; ids from f7a8f2a)\",\n  \"grep -n 'DELETE FROM' app/backend/pipeline.py on archive -> line 381 (f-string table delete, reached only for non-hand pending rows)\",\n  \"read app/frontend/review.js:337 and :372 on archive (rerun_note rendered on item cards; not exercised in a browser)\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"first_run_partial_names_records\": 5, \"all_extracted_stays_ready\": 5, \"hand_entry_warning_not_failure\": 4, \"rerun_keeps_pending_hand_entry\": 5, \"dismiss_and_recover_states\": 2, \"pins_justified\": 4, \"test_strength_mutants\": 5},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from r1: dismissing a hand-entered entry leaves a stale ENTERED_BY_HAND warning and the failure never returns\",\n   \"evidence\": \"probe_out_r2.txt block '== H': e1_m review_status 'dismissed', case status ready, error null, warnings [('ENTERED_BY_HAND', 1, 'e1')]; app/backend/generator.py:205-219 counts any non-rejected hand entry; no test in tests/unit/test_t165_partial_extract.py covers dismissal\",\n   \"why_it_matters\": \"The case-level message tells the paralegal she entered record 1 by hand after she has dismissed that entry. The state of record 1 (no usable entry) is not reported. Unchanged by 56d746c, so not a new defect.\",\n   \"fix\": \"Exclude dismissed hand entries from entered_by_hand, or word the warning by state; decide with Chris whether dismissing a hand entry re-opens RUN_FAILED (r1 questions_for_chris).\",\n   \"acceptance_test\": \"Hand-enter record 1 after a failed run, dismiss e1_m; assert the chosen state (RUN_FAILED with record 1 named, or no ENTERED_BY_HAND warning). Pin it.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from r1: test_t139 counts.entries == 4 counts a hand entry as an AI entry\",\n   \"evidence\": \"tests/unit/test_t139_charge_text.py:224 'assert j[\\\"counts\\\"][\\\"entries\\\"] == 4  # e1, e5, e6 and the hand-entered record 3 (wait_ready)'\",\n   \"why_it_matters\": \"An AI-timeline assertion now counts a paralegal entry. It is a documented workaround for the T-168 lib01 fixture gap and can hide an AI regression on lib01. Unchanged by 56d746c.\",\n   \"fix\": \"Keep the workaround; assert AI-made entries (ladder.entered_by != 'reviewer') == 3 and the hand entry id present. Revert with T-168.\",\n   \"acceptance_test\": \"test_t139 lib01: AI-made entries == 3, e3_m present; mutant dropping one AI entry fails.\"}\n ],\n \"whats_right\": [\n  \"A re-run that extracts a hand-entered record keeps the pending entry, adds rerun_note (kind ai_entry) naming the AI entry, and never deletes it (probe G, test line 161; m1 killed)\",\n  \"The round-1 probe scenarios A to F are unchanged on HEAD; only G differs, as intended (probe_out_r2.txt vs r1 probe_out.txt)\",\n  \"The note is cleared when a later run has no AI entry for the record (test line 187; m3 killed)\"\n ],\n \"questions_for_chris\": [\n  \"Dismissing a hand entry after a failed extract: should RUN_FAILED and the tray placeholder come back, or stay cleared? (carried from r1)\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T16:37:12.296Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-165-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:37:19.086Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t165_r2_patterns.md",
 "content": "---\nname: t165-r2-patterns\ndescription: T-165 r2 56d746c pass: hand-entry kept on re-run with rerun_note, mutants m1-m3 killed, r1 minors carried, f7a8f2a e2e-contract failure out of scope\nmetadata:\n  type: project\n---\n\nT-165 round 2 (commit 56d746c, reviews/T-165-staff-engineer-r2.md): verdict pass. Blocker from r1 (re-run deletes pending hand entry when the AI now also has a live entry) fixed in `_persist` / `_keep_hand_entry` (app/backend/pipeline.py:373-398).\n\n- The r1 scenario G probe (`artifacts/review-evidence/T-165/probe_t165.py`) must be re-run on each round; diff its output against the earlier `probe_out.txt`. Only the intended scenario should change.\n- Pytest on the scratch archive needs `PYTHONPATH=<archive>`; `python -I` ignores PYTHONPATH, so copy the probe into scratch and run it without -I.\n- The unit suite has one known red at HEAD from f7a8f2a (`test_e2e_contract.py::test_every_test_id_is_declared`, undeclared ids `cases-keys`, `btn-new-case`, `do-first-item`). It is out of scope for T-165; cite the commit that introduced it.\n- macOS has no `timeout` binary; do not wrap pytest in it.\n- Carried minors that persist across rounds: dismissed hand entry keeps ENTERED_BY_HAND warning (no dismissal test); test_t139 `counts.entries == 4` counts a hand entry (T-168 workaround).\n\n**Why:** a blocker fixed in code can be pinned only by tests that assert both the entry survives and the note text; a single sibling branch (note clear) needed its own mutant.\n**How to apply:** for any \"keep on re-run\" fix, mutate the keep condition, the note write, and the note clear separately, and check each dies.\n\nRelated: [[project_t165_partial_extract]], [[project_t146_r3_decided_items_never_lowered]].\n"
}
````

### User / tool · 2026-11-02T16:37:19.209Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t165_r2_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:37:24.889Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 150
}
````

### User / tool · 2026-11-02T16:37:24.902Z

**tool result**
````
<system-reminder>Warning: the file exists but is shorter than the provided offset (150). The file has 96 lines.</system-reminder>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:37:26.245Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 90
}
````

### User / tool · 2026-11-02T16:37:26.254Z

**tool result**
````
90	- [T-159/T-161 r2 patterns](project_t159_t161_r2_patterns.md) — both pass: compensation fails under double fault (export 200), always-reset mutant, undated-boundary mutant, FakeCall skips validate_schema
91	- [T-158 settle patterns](project_t158_settle_patterns.md) — r1/r2 (pinned f31b146, changes): splice in mountSection silently killed panels (cured by 2de5ba9), fixed-timer settle unproven, sha-less AC artifact
92	- [T-160 budget/placement patterns](project_t160_budget_placement_patterns.md) — 94a31a4 pass: budget test sample-only, reverted placement passes density tests, "never own line" false at 320 px
93	- [T-155 r2 / T-164 patterns](project_t155_r2_t164_patterns.md) — 95ffe36 pass: totals match but skip sets differ (order-dependent count-zero skip), [hidden] !important makes CSS mutant a no-op, parent-of-fix control
94	- [T-167 plain-wording patterns](project_t167_plain_wording_patterns.md) — r1 da6afb2 changes: AC universal grep overclaimed (qa calibration sentences), sibling commit reds e2e id contract, fallback doubles phrase
95	- [Reviewer scratch writes](feedback_reviewer_scratch_writes.md) — Write blocked in scratchpad; put helpers and evidence under artifacts/review-evidence; no backticks in shell lines
96	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:37:29.075Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [Reviewer scratch writes](feedback_reviewer_scratch_writes.md) — Write blocked in scratchpad; put helpers and evidence under artifacts/review-evidence; no backticks in shell lines\n",
 "new_string": "- [Reviewer scratch writes](feedback_reviewer_scratch_writes.md) — Write blocked in scratchpad; put helpers and evidence under artifacts/review-evidence; no backticks in shell lines\n- [T-165 r2 patterns](project_t165_r2_patterns.md) — 56d746c pass: hand entry kept with rerun_note, m1-m3 killed, r1 minors carried, f7a8f2a e2e red out of scope\n"
}
````

### User / tool · 2026-11-02T16:37:29.178Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:37:31.465Z

T-165 r2 (56d746c): pass, no blockers or majors. The r1 hand-entry blocker is fixed, and two r1 minors are carried; review at /Users/arsis/zlayt-pm-project/reviews/T-165-staff-engineer-r2.md.
