# Subagent: T-159 r2 + T-161 r2 review (T-159 r2 + T-161 r2 review)

Source: `agent-a18d0a5d6395b55da.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T15:28:47.712Z

In /Users/arsis/zlayt-pm-project, run the round-2 reviews of two cards. Read reviews/T-159-staff-engineer.md, reviews/T-161-staff-engineer.md, and both cards (`python3 tools/board.py show T-###`).

On a `git archive HEAD` copy:
- **T-161 (99438fb).** A flag step that is down on a first run reads run_partial and RUN_FAILED, even with no phrase-list hit. An extract-down first run with no entries reads failed, with the step named. Re-run your round-1 repro. The worker flipped three older test pins, including one in test_t146_r2_failed_rerun_keeps_items.py; check that each flip is justified.
- **T-159 (c0e2b86).** The confirm and its event are written in one transaction, and the accept is taken back if the confirm write fails. Judge whether that compensation is safe. The two mutants must die. AC1 has moved to T-163.

Run the unit suite.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-159-staff-engineer-r2.md and reviews/T-161-staff-engineer-r2.md. Each needs a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings, exercised. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:28:50.153Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T15:28:50.170Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:28:50.501Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-159-staff-engineer.md"
}
````

### User / tool · 2026-11-02T15:28:50.518Z

**tool result**
````
1	# T-159 staff-engineer review (D-059 audit trail for a flagged charge)
2	
3	Reviewed commit 9fc579c as contained in HEAD 83f1afd, on a `git archive 83f1afd` copy (HEAD later moved to ba21b4b; `git diff 83f1afd ba21b4b --stat` touches only conflicts.py, SCOPE_CUTS.md and a T-141 test, none of this card's files).
4	
5	Verdict: **changes**. No blocker. One major: AC1 is only partly delivered (the card says so itself: `internal_notes_text` does not list confirmed-flag charges). The rest of the audit trail works end to end through the API and is well pinned.
6	
7	What I exercised (all on the archive copy, `.venv/bin/python`):
8	- `pytest tests/unit -q` at 83f1afd: 4613 passed, 8 skipped (252 s).
9	- API probe (TestClient, live-mode env as in `test_amounts_d059_api.make_env`) for a likely_total charge (extraction-time flag, ledger text) and a promoted likely_duplicate charge:
10	  - 422 CONFIRM_REQUIRED carries `detail.message` = the flag's own sentence (no token, no `a<n>`); the top-level `message` still has the "(likely_total)" token, as the AC allows.
11	  - Accept with the named confirm gives 200; GET /audit then shows `events[].confirm = {flag, name, confirmed_at}` in public mode (no before/after). The DB row `after_json` carries the same confirm.
12	  - Item trace: `charge_flag` step "Flagged by the code: Likely total", pending with `next_action.code == CONFIRM_FLAG` and "needs your named confirm", then pass with `evidence.values {flag, name, confirmed_at}`; human step says "You accepted this item and confirmed the flag "Likely total" by name."
13	  - Three repeat accepts (no confirm) return 200, `confirmed_at` unchanged, totals unchanged, still exactly one accept event in /audit.
14	  - dismiss then accept without confirm gives 422; confirm, dismiss, accept without confirm gives 422 (the no-op does not outlive a status change).
15	  - The duplicate sentence reads: `This looks like the same charge as “04/16/2026 manual therapy invoiced $150.00.” in record 1: $150.00 on 2026-04-16. Counting both would count one service twice.` (no id).
16	- Mutation run of 13 mutants against `test_t159_flag_audit.py` + `test_amounts_d059_api.py`: 11 killed, 2 survived (findings 2 and 3). Killed: dropping the no-op, dropping the event write, dropping the review_status check, dropping the charge_flag step, pending-when-confirmed, dismissed-not-skipped, detail message dropped, plain human step, audit_view dropping confirm, id back in the sentence, wrong flag name stamped.
17	- Failure-injection probe: made the event write in `_record_confirm` raise after the accept committed (finding 3).
18	- Read `git show 9fc579c` for amounts.py, present.py, reclassify.py, review.py, trace.py, api.md in full, and `git diff HEAD` to see uncommitted state.
19	
20	Separation of labels: findings 1 is a card AC that is unmet (must fix before the gate). Findings 2 to 4 are test and robustness gaps I would want fixed (minor). Finding 5 is housekeeping (nit).
21	
22	```json
23	{"card": "T-159", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
24	 "scope": "commit 9fc579c within HEAD 83f1afd (git archive copy); app/backend/{review,trace,present,amounts,reclassify}.py, tests/unit/test_t159_flag_audit.py, memory/contracts/api.md; synthetic NOTE and ledger text; no app server",
25	 "exercised": ["python3 tools/board.py show T-159 and T-161; read memory/contracts/api.md D-059 paragraph", "git archive 83f1afd copy: pytest tests/unit -q -> 4613 passed, 8 skipped", "API probe via TestClient: likely_total (extraction-time) and promoted likely_duplicate: 422 CONFIRM_REQUIRED detail.message, accept with confirm, GET /audit events[].confirm in public mode, item trace charge_flag pending then pass, human step text, three repeat accepts (200, one event, totals unchanged), dismiss/reset then accept needs confirm again", "13 mutants of review.py, trace.py, present.py, amounts.py against test_t159_flag_audit.py + test_amounts_d059_api.py: 11 killed, 2 survived", "failure injection: json.loads raising inside _record_confirm after apply_review committed", "git show 9fc579c (all hunks) and git diff HEAD (found an uncommitted trace.py hunk)"],
26	 "verdict": "changes",
27	 "scores": {"audit_event_confirm": 4, "trace_flag_step": 5, "repeat_accept_noop": 5, "plain_sentence": 5, "ac_completeness": 2, "test_strength": 4, "atomicity": 3},
28	 "findings": [
29	  {"severity": "major", "title": "AC1 is not met: internal_notes_text does not list confirmed-flag charges",
30	   "evidence": "board T-159 AC1 text: 'internal_notes_text lists confirmed-flag charges, the letter is unchanged'; AC1 done:false; handoff note 2026-11-02T15:06:37Z 'AC1 part not done: internal_notes_text listing ... needs export.py'. `git show --stat 9fc579c` touches no export file; grep -n confirmed_at app/backend/export.py at 83f1afd finds nothing for a flag confirm.",
31	   "why_it_matters": "The audit trail of a D-059 confirm is meant to reach the one artifact the paralegal keeps: the internal notes. Today the confirm lives in /audit and the trace only. The card is in_review with a stated gap, so it cannot be done as written.",
32	   "fix": "Either add the internal-notes line (service/amount/date/record, flag name, confirmed_at) in export.py via a card for its owner or with the orchestrator's go-ahead, with the letter text byte-identical, or split AC1 into a new card with an explicit SCOPE_CUTS row and amend this card's AC.",
33	   "acceptance_test": "Accept a flagged charge with its confirm, call GET /api/cases/{tok}/export: internal_notes_text names the charge and the flag 'Likely duplicate' with the confirm date; letter_text equals the letter exported when the same charge was accepted without a flag change; dismissed flagged charges are not listed."},
34	  {"severity": "minor", "title": "Mutant survives: the confirm is stamped on the wrong accept event after reset and re-accept",
35	   "evidence": "mutate app/backend/review.py:228 query 'ORDER BY at DESC, rowid DESC LIMIT 1' to 'ORDER BY at ASC, rowid ASC LIMIT 1' -> 23 passed (test_t159_flag_audit.py + test_amounts_d059_api.py + test_t159 duplicate file). tests/unit/test_t159_flag_audit.py:92 test_accept_again_after_a_reset_needs_the_confirm_again asserts only len(accept_events) == 2.",
36	   "why_it_matters": "A flagged charge accepted, reset and accepted again has two accept events. With the mutant the second confirm overwrites the first event and the second event shows no confirm: the audit trail would be wrong exactly in the path the AC calls out.",
37	   "fix": "Assert in that test that both accept events carry a confirm and that their confirmed_at values differ or match the item at each step.",
38	   "acceptance_test": "After accept(confirm) -> reset -> accept(confirm), GET /audit shows two accept events for the item and each has its own confirm {flag, name, confirmed_at}; the ASC mutant fails."},
39	  {"severity": "minor", "title": "Mutant survives: repeat-accept no-op does not require confirmed_at",
40	   "evidence": "delete 'and bool(f.get(\"confirmed_at\"))' in review.py:212-215 confirmed_accept -> 23 passed. No test builds an accepted, flagged charge with no confirmed_at.",
41	   "why_it_matters": "The only way to get that state is a partial write (see next finding) or an older run; the intended behaviour (a charge with an unconfirmed flag asks for the confirm again) is unpinned.",
42	   "fix": "Add a unit test with an accepted flagged item whose ladder.confirm has no confirmed_at: a repeat accept without confirm is 422 CONFIRM_REQUIRED.",
43	   "acceptance_test": "That test passes at HEAD and fails with the confirmed_at clause removed."},
44	  {"severity": "minor", "title": "The confirm is written in three separate autocommit statements; a failure leaves the item confirmed and the event not, and the no-op then makes it permanent",
45	   "evidence": "app/backend/review.py:252-254 (apply_review, then _record_confirm) and :225-228 (DB.update_item, then a raw conn.execute UPDATE review_events outside any transaction; connection is isolation_level=None, app/db/db.py:54). Repro: patch app.backend.review.json with a loads that raises, POST accept with confirm=likely_duplicate -> 500; GET case shows review_status accepted, flag.confirmed_at set, totals.accepted 15000; /audit accept event has no confirm; a second POST accept without confirm -> 200 (no-op), so the event never gets its confirm.",
46	   "why_it_matters": "It is visible (a 500), not silent, but the audit event is the artifact this card exists to make reliable, and the new no-op removes the retry that would have repaired it.",
47	   "fix": "Write status, item confirm and event confirm in one transaction (give DB.apply_review an optional extra for after_json), or have the repeat-accept path repair an accepted event whose confirm is missing.",
48	   "acceptance_test": "Inject a failure into the event write: either nothing is accepted (status pending, no confirm anywhere) or a retry leaves the event with its confirm."},
49	  {"severity": "nit", "title": "Working tree holds an uncommitted trace.py hunk in this card's area",
50	   "evidence": "git diff HEAD -- app/backend/trace.py shows `_human_step` events gaining `**({\"confirm\": e[\"after\"][\"confirm\"]} ...)` at line 244; the HEAD archive trace shows human evidence.events with only action and at (probe output, TRACE-DONE).",
51	   "why_it_matters": "I reviewed committed HEAD; the committed human step names the confirm in its text, so AC1's wording holds, but the machine-readable confirm in the trace events is not in any commit or test yet.",
52	   "fix": "Commit it with a test in the T-159 file or drop it.",
53	   "acceptance_test": "GET /items/{id}/trace human evidence.events[0].confirm equals the /audit event confirm."}
54	 ],
55	 "whats_right": ["repeat accept is a true no-op: one event, same confirmed_at, same totals, and it does not survive dismiss or reset (probe and tests agree)", "charge_flag trace step is a code step with pending/pass/skipped states, CONFIRM_FLAG next_action and evidence.values; 7 of 7 trace mutants killed", "the flag sentence names the other charge by its own line (service, amount, date, record) with no internal id and no token"],
56	 "questions_for_chris": []}
57	```
58	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:28:50.850Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-161-staff-engineer.md"
}
````

### User / tool · 2026-11-02T15:28:50.864Z

**tool result**
````
1	# T-161 staff-engineer review (first run with a stage down reads failed, gate RUN_FAILED)
2	
3	Reviewed commit 83f1afd (HEAD at review start) on a `git archive 83f1afd` copy. HEAD later moved to ba21b4b; `git diff 83f1afd ba21b4b --stat` touches only conflicts.py, SCOPE_CUTS.md and a T-141 test, none in this card's path.
4	
5	Verdict: **fail**. One blocker: the flag step is detected only through failure-marked lexicon flags, so a first run whose flag step is down on records with no phrase-list hit still reads `ready`, shows zero flags, and exports with HTTP 200. The card's own AC says "no stage missed", and this is the stage it names first.
6	
7	What I exercised (archive copy, `.venv/bin/python`):
8	- `pytest tests/unit -q`: 4613 passed, 8 skipped. `tests/unit/test_t161_first_run_stage_down.py`: 13 green.
9	- Stage matrix on a first run, in-process through `PL.run_pipeline` with FakeCall, on the golden sample and on a two-record plain note (no phrase-list hit): j1, j2, j3, j4, flags, conflicts, extract, split (unsplit paste), and Spanish `extract_es` / `judge_faithfulness_es`.
10	- API run (TestClient `/run`, `/status`, `/export`) for flags down on the sample and on the plain note.
11	- 10 mutants of `pipeline.py` (reverting the T-161 line, dropping each step from the first-run list, keeping extract, failed-only-on-timeout, FIXTURE_MISS not a flag failure, flag-kind check removed, unavailable arm removed, names dropped from the message) run against the T-161 file, then against the T-145/T-146/rerun/partial tests: 10 of 10 killed.
12	
13	Results of the matrix (status | error code | gate):
14	- sample j1 (9 items), j2 (3), j3 (1), flags (7): `failed | run_partial | RUN_FAILED`, message "The AI step failed for N items (the second check|finding the flags) on this run, and there is no earlier result to keep. Run it again to retry." Spanish `judge_faithfulness_es` and `j1` on a mixed packet: same.
15	- sample j4 with the default empty-flag script: `ready`. That is by design (`flags.py` `judge_flags`: lexicon-only flags have no judge); the card's test sets `model_flag` so j4 has something to judge.
16	- plain note, flags down: `ready | none | no RUN_FAILED`; accept both verified entries, GET export returns 200 with a letter (finding 1).
17	- extract down and split down: `ready` with `done_with_errors` and the failure shown as tray items or a split error; by design and pinned by the T-146 r3 test. Not counted as a finding (question below).
18	
19	Labels: finding 1 violates the card AC and the persona's no-silent-failure rule (blocker). Finding 2 is a missing-test item (minor). The reading of j2/j3/j4 as "the second check" is wording I would have done differently, not a defect.
20	
21	```json
22	{"card": "T-161", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
23	 "scope": "commit 83f1afd (pipeline.py hunk, tests/unit/test_t161_first_run_stage_down.py) in a git archive copy; golden sample, a two-record plain synthetic note, a mixed English/Spanish synthetic packet, the unsplit paste from test_split_llm",
24	 "exercised": ["python3 tools/board.py show T-161; git show 83f1afd (full diff)", "git archive 83f1afd copy: pytest tests/unit -q -> 4613 passed, 8 skipped; T-161 file 13 passed", "in-process stage matrix on a first run: j1 j2 j3 j4 flags conflicts extract split, on the sample and on a plain note; Spanish extract_es / judge_faithfulness_es / j1 on a mixed packet", "API run of flags-down through POST /run, GET /status, GET /export on the sample (failed, run_partial, export 422 RUN_FAILED) and on the plain note (ready, export 200)", "10 pipeline.py mutants vs the T-161 file and the T-145/T-146/rerun/partial tests: 10 killed", "read flags.py run_flag_pass/merge/judge_flags and pipeline.py _noting/_failure/_partial_error/run_pipeline"],
25	 "verdict": "fail",
26	 "scores": {"stage_coverage": 2, "gate_agreement": 4, "message_names_step": 4, "test_strength": 4, "clean_run_stays_ready": 5},
27	 "findings": [
28	  {"severity": "blocker", "title": "A first run with the flag step down reads ready (and exports) when the records have no phrase-list hit",
29	   "evidence": "Repro: two-record note ('Patient seen for follow up of neck stiffness. Range of motion improved.' / 'Patient seen. Physical therapy continued 2x per week.'), every call works except step 'flags' raises AU.LLMFailed. Result: GET /status status 'ready', error null; GET case flags 0, warnings []; accept both verified entries; GET /export -> 200 with the letter. The same note with j1 down is 'failed | run_partial | RUN_FAILED'. Cause: app/backend/pipeline.py:247 _failure and :242 _FLAG_FAIL detect a failed flag step only on a flag row whose reasons carry LLM_FAILED_AFTER_RETRIES or FIXTURE_MISS, and app/backend/flags.py:164 sets that marker only on lexicon flags (merge loop over lex_flags). With no lexicon flag there is no row, so `empty` never gets 'finding the flags'. pipeline.py:443-450 _noting already records failed_steps (it holds 'flags') and pipeline.py:575 already reads it for prune; line 583 does not.",
30	   "why_it_matters": "This is a silent fallback to 'no AI flags': a paralegal gets a ready case with no pre-existing or causation warnings and an open export, though the step never ran. The card's AC and title name the flags stage; the unit test passes only because the sample's records 3 and 6 happen to carry phrase-list flags (test_first_run_with_the_flag_step_down_fails_the_case_and_names_the_step uses the sample, 7 items).",
31	   "fix": "In run_pipeline, if 'flags' is in failed_steps and no stub row carried it, add 'finding the flags' to the steps passed to _partial_error (first run and re-run); keep prune logic as is. The message may count records instead of items when there is no item.",
32	   "acceptance_test": "Unit test: first run of a two-record note with no phrase-list hit and the flags step down (both LLMFailed and FixtureMiss) -> case failed, error.code run_partial, message names 'finding the flags', trace.export_blockers has RUN_FAILED; same note with flags working stays ready; a good second run clears it. Mutant: drop the failed_steps addition and the test fails."},
33	  {"severity": "minor", "title": "Stage tests all run on the golden sample, which hides stage-detection that depends on the input",
34	   "evidence": "tests/unit/test_t161_first_run_stage_down.py:first_run uses G.raw('sample') for every parametrized case; j2 on a note with no dollar amount and flags on a note with no lexicon hit are not covered (my probe: plain note j2 and flags down both 'ready').",
35	   "why_it_matters": "It let finding 1 pass 13 tests and 10 of 10 mutants. For j2 on a case with no amounts there is nothing to judge, so ready is right; the test should say so rather than leave it open.",
36	   "fix": "Add the plain-note rows: flags down (expects failed), j2 down with no amounts (expects ready, documented).",
37	   "acceptance_test": "Parametrize first_run over the sample and a plain note; the flags-down row on the plain note fails against HEAD and passes after the fix."}
38	 ],
39	 "whats_right": ["one code path: the first run reuses the T-146 _partial_error wording, so the message and the RUN_FAILED gate cannot drift between first run and re-run", "tests pin the clean first run staying ready, a good second run clearing a failed first run, and extract-down keeping its tray shape", "all 10 mutants of the first-run line were killed, including FIXTURE_MISS and the flag-kind check"],
40	 "questions_for_chris": ["A first run with extract down or the splitter down still reads 'ready' with done_with_errors and tray/split-error items (pinned by T-146 r3 by design). Is that still the intended reading, or should those two also read failed?"]}
41	```
42	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:28:51.525Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-159; python3 tools/board.py show T-161; git log --oneline | head -8"
}
````

### User / tool · 2026-11-02T15:28:51.769Z

**tool result**
````
---
id: "T-159"
title: "D-059 audit trail for a flagged charge: the named confirm in the review event, a flag step in the item trace, a plain flag message, and a no-op for a repeat accept"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: ["T-154"]
created_by: "frontend"
created_at: "2026-11-02T14:43:39Z"
updated_at: "2026-11-02T15:28:43Z"
claimed_by: "backend"
claimed_at: "2026-11-02T15:18:26Z"
rounds: 1
commits: ["9fc579c", "c0e2b86"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-159-staff-engineer.md", "at": "2026-11-02T15:18:19Z"}
ac:
  - {"n": 1, "text": "GET /audit: the accept event of a flagged charge carries confirm {flag, name, confirmed_at} (metadata, also in public mode); the item trace for a charge with ladder.confirm has a code step id charge_flag ('Flagged by the code: Likely total', pending 'needs your named confirm' until confirmed, pass after with evidence.values {flag, name, confirmed_at}, next_action CONFIRM_FLAG) and the human step names the confirm; internal_notes_text lists confirmed-flag charges, the letter is unchanged", "done": true, "evidence": "Scope moved by orchestrator §7.4: the internal-notes line for confirmed-flag charges is T-163 (needs export.py after T-139/T-140)."}
  - {"n": 2, "text": "a repeat accept (no confirm) on a charge already accepted with its flag confirmed returns 200 unchanged, with no second review event; CONFIRM_REQUIRED detail carries message (the flag's own sentence, no token) so a client never has to strip it", "done": true, "evidence": "tests/unit/test_t159_flag_audit.py::test_a_repeat_accept_of_a_confirmed_charge_writes_nothing, ::test_confirm_required_carries_the_flags_own_sentence_without_the_token pass; full unit suite 4607 passed"}
  - {"n": 3, "text": "the likely_duplicate sentence names the other charge by its line (service, amount, date, record) and never by its internal id (no a<n> in message); memory/contracts/api.md updated", "done": true, "evidence": "tests/unit/test_t159_flag_audit.py::test_the_duplicate_sentence_names_the_other_line_not_its_id passes; api.md D-059 paragraph updated"}
---
## Description
Found by T-154 r2 (claims-adjuster, reviews/T-154-claims-adjuster.md). The frontend already shows the flag and the confirm in the Audit drawer and the 'How this was checked' dialog by reading the case item (flag.confirmed_at) via ZL.chargeFlagNote; once the trace carries a step with id charge_flag and an event carries confirm, the page uses those and skips its own note. Frontend also strips the 'It is not counted unless you confirm that flag by name (token)' tail and the 'a<n>' id from the sentence, which is a stopgap for the sentence the server should send clean.

## Notes (append-only, newest last)
- 2026-11-02T14:52:47Z orchestrator: assigned: frontend
- 2026-11-02T14:52:57Z orchestrator: assigned: backend
- 2026-11-02T14:53:12Z backend: claimed
- 2026-11-02T14:53:12Z backend: claimed with --force: T-154 dependency is the frontend card in its own review loop; orchestrator directed this claim. Backend work independent of it.
- 2026-11-02T15:06:37Z backend: AC 2 checked: tests/unit/test_t159_flag_audit.py::test_a_repeat_accept_of_a_confirmed_charge_writes_nothing, ::test_confirm_required_carries_the_flags_own_sentence_without_the_token pass; full unit suite 4607 passed
- 2026-11-02T15:06:37Z backend: AC 3 checked: tests/unit/test_t159_flag_audit.py::test_the_duplicate_sentence_names_the_other_line_not_its_id passes; api.md D-059 paragraph updated
- 2026-11-02T15:06:37Z backend: AC1 part not done: internal_notes_text listing of confirmed-flag charges needs export.py (T-139 worker's file) plus the case loader; the rest of AC1 (event confirm in /audit incl. public mode, charge_flag trace step, human step names the confirm) is done and tested. Needs a small follow-up card or a go-ahead to edit export.py. Also touched present.py (1 line, audit_view), amounts.py (charge_line, plain duplicate sentence) and reclassify.py (pass the other charge's line) because the event and the sentence live there; committed hunk-only.
- 2026-11-02T15:06:39Z backend: moved in_progress -> in_review: AC1 unchecked: the internal_notes_text line for confirmed-flag charges needs export.py (T-139's file); event confirm, charge_flag step and human step are done (commit 9fc579c)
- 2026-11-02T15:06:50Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T15:18:19Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-159-staff-engineer.md; round 1; findings:
    - [major] AC1 is not met: internal_notes_text does not list confirmed-flag charges — fix: Either add the internal-notes line (service/amount/date/record, flag name, confirmed_at) in export.py via a card for its owner or with the orchestrator's go-ahead, with the letter text byte-identical, or split AC1 into a new card with an explicit SCOPE_CUTS row and amend this card's AC.
    - [minor] Mutant survives: the confirm is stamped on the wrong accept event after reset and re-accept — fix: Assert in that test that both accept events carry a confirm and that their confirmed_at values differ or match the item at each step.
    - [minor] Mutant survives: repeat-accept no-op does not require confirmed_at — fix: Add a unit test with an accepted flagged item whose ladder.confirm has no confirmed_at: a repeat accept without confirm is 422 CONFIRM_REQUIRED.
    - [minor] The confirm is written in three separate autocommit statements; a failure leaves the item confirmed and the event not, and the no-op then makes it permanent — fix: Write status, item confirm and event confirm in one transaction (give DB.apply_review an optional extra for after_json), or have the repeat-accept path repair an accepted event whose confirm is missing.
- 2026-11-02T15:18:19Z orchestrator: AC1 (internal notes line) is moved to T-163 (needs export.py after T-139/T-140). Round 2: write the confirm and its event in one transaction; kill the 2 surviving mutants.
- 2026-11-02T15:18:19Z orchestrator: assigned: backend
- 2026-11-02T15:18:26Z backend: claimed
- 2026-11-02T15:28:25Z backend: AC 1 checked: moved to T-163 by orchestrator (internal notes line, export.py); this round covers the review findings only
- 2026-11-02T15:28:25Z backend: moved in_progress -> in_review
- 2026-11-02T15:28:34Z backend: AC 1 unchecked
- 2026-11-02T15:28:34Z backend: AC1 check by mistake was reverted; it stays with T-163 as the orchestrator directed.
- 2026-11-02T15:28:43Z orchestrator: AC 1 checked: Scope moved by orchestrator §7.4: the internal-notes line for confirmed-flag charges is T-163 (needs export.py after T-139/T-140).
- 2026-11-02T15:28:43Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed (r2): review._record_confirm writes the item confirm and the event confirm in one transaction; set_review takes the accept back (reset/dismiss to the prior status) if that write fails, so nothing counts without its confirm; trace human-step events carry confirm (committed, was left uncommitted). Tests added first: newest-event ordering (kills ASC mutant), accepted charge with no confirmed_at asks again (kills clause mutant), failure injection (item has no confirmed_at, totals unchanged, retry works), trace events confirm. Verified in git archive HEAD copy + my files: tests/unit 4788 pass; 3 mutants run (ASC, clause, no-txn) all killed. Left: AC1 -> T-163. Surprised: status+event are still DB.apply_review's own transaction (db.py is not mine), so the accept is compensated, not atomic; an optional after_json extra in apply_review would make it one write. Commit c0e2b86.

---
id: "T-161"
title: "First run with a stage down (flags, judge, conflicts) reads 'ready': it must read failed/run_partial with the step named and the gate RUN_FAILED, same as re-runs (T-146 handoff)"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T14:58:59Z"
updated_at: "2026-11-02T15:28:43Z"
claimed_by: "backend"
claimed_at: "2026-11-02T15:18:26Z"
rounds: 1
commits: ["83f1afd", "99438fb"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "fail", "file": "reviews/T-161-staff-engineer.md", "at": "2026-11-02T15:18:19Z"}
ac:
  - {"n": 1, "text": "unit tests per stage: first run with that stage failing -> case failed/run_partial, message names the step, gate RUN_FAILED; a clean first run stays ready", "done": true, "evidence": "tests/unit/test_t161_first_run_stage_down.py (plain-note flags down/fixture-miss, rerun, clears on good run, j2 no amounts ready, extract-down no entries failed, partial extract ready) pass; git archive HEAD + my files: tests/unit 4788 pass (1 pin updated after)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T14:59:05Z orchestrator: assigned: backend
- 2026-11-02T14:59:18Z backend: claimed
- 2026-11-02T15:06:46Z backend: AC 1 checked: tests/unit/test_t161_first_run_stage_down.py (13 tests: j1,j2,j3,j4,flags down and fixture-miss -> failed/run_partial, step named, RUN_FAILED; clean first run ready; extract-down first run unchanged); full unit suite 4649 pass, 6 fail only in test_amounts_d062 (T-140 amounts.py in progress, not mine)
- 2026-11-02T15:06:46Z backend: moved in_progress -> in_review
- 2026-11-02T15:06:50Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T15:07:12Z orchestrator: Reviewer: also judge the 'extract down on a first run still reads ready' case - with no entries at all it should not read ready; T-146 r3 pinned it, so decide whether that pin was right.
- 2026-11-02T15:18:19Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): fail — reviews/T-161-staff-engineer.md; round 1; findings:
    - [blocker] A first run with the flag step down reads ready (and exports) when the records have no phrase-list hit — fix: In run_pipeline, if 'flags' is in failed_steps and no stub row carried it, add 'finding the flags' to the steps passed to _partial_error (first run and re-run); keep prune logic as is. The message may count records instead of items when there is no item.
    - [minor] Stage tests all run on the golden sample, which hides stage-detection that depends on the input — fix: Add the plain-note rows: flags down (expects failed), j2 down with no amounts (expects ready, documented).
- 2026-11-02T15:18:19Z orchestrator: Round 2: drive the first-run failure from failed_steps (pipeline.py:583), not from lexicon-flag markers, so a flag step down reads run_partial even with no phrase-list hit; also an extract-down first run with no entries must not read ready (decide failed, step named).
- 2026-11-02T15:18:20Z orchestrator: assigned: backend
- 2026-11-02T15:18:26Z backend: claimed
- 2026-11-02T15:28:25Z backend: AC 1 checked: tests/unit/test_t161_first_run_stage_down.py (plain-note flags down/fixture-miss, rerun, clears on good run, j2 no amounts ready, extract-down no entries failed, partial extract ready) pass; git archive HEAD + my files: tests/unit 4788 pass (1 pin updated after)
- 2026-11-02T15:28:25Z backend: moved in_progress -> in_review
- 2026-11-02T15:28:43Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: pipeline.run_pipeline reads the flag step from failed_steps (new 'down' arg of _partial_error, named without an item count) so flags down on a note with no phrase-list hit reads failed/run_partial/RUN_FAILED; a first run with extract down and no entry at all reads failed (writing the entries named); partial extract failures keep the tray shape. Verified: tests written first (6 red), git archive HEAD copy + my files, tests/unit 4788 pass, 1 old pin (t146_r2 first-run stubs) updated to the new decision. Left: nothing. Surprised: 'ready' on extract-down-with-nothing was pinned in 3 tests (t146 r2, r3, t161); flipped. Commit 99438fb.

c0e2b86 fix(backend): T-159 r2 confirm and its event in one transaction (accept taken back on failure), trace events carry the confirm, tests kill the oldest-event and confirmed_at mutants
99438fb fix(backend): T-161 r2 first-run failure driven by failed_steps (flag step down with no phrase-list hit reads run_partial), extract-down first run with no entries reads failed
78b6a33 fix(backend): T-141 r7 plural-history date guard reads two-digit years (1/3/26, 1-3-26, Jan 3, 26, 1/26)
b576567 tools: pre-commit loads a case with no console errors when frontend files are staged (lesson 6379c0b)
2de5ba9 fix(frontend): T-154 r3 the a-key guard moves from mountSection() (ReferenceError on every case load) into the keydown handler; the duplicate sentence is the backend's own; e2e test_no_console_errors
c3a2af8 docs(orchestrator): D-062 amended - notes yield charges only without a same-provider itemized bill
2ac96cf fix(backend): T-140 D-062 total line 'Billed charges accepted from these records', charge sources by billing header, per-figure rule, CPT/HCPCS normalization
852b060 fix(backend): T-157 r2 title validation (plain text, 422 invalid_title), next_action order tests kill the mutants, one live definition for rerun_available
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:29:04.345Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git status --short | head -20; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo $S; mkdir -p $S/r2a && git archive HEAD | tar -x -C $S/r2a && ls $S/r2a | head -30; ls -d .venv; git show --stat 99438fb c0e2b86 | head -40"
}
````

### User / tool · 2026-11-02T15:29:05.183Z

**tool result**
````
c0e2b86
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
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
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
.venv
commit 99438fb194d8a81737bd0bf18b02e0cba0a1c6d8
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:27:54 2026 -0600

    fix(backend): T-161 r2 first-run failure driven by failed_steps (flag step down with no phrase-list hit reads run_partial), extract-down first run with no entries reads failed
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/pipeline.py                            | 13 +++-
 .../unit/test_t146_r2_failed_rerun_keeps_items.py  |  4 +-
 .../test_t146_r3_decided_items_never_lowered.py    |  2 +-
 tests/unit/test_t161_first_run_stage_down.py       | 76 ++++++++++++++++++++--
 4 files changed, 85 insertions(+), 10 deletions(-)

commit c0e2b86c02e9889353a9ac791e57283a3aec3607
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:28:09 2026 -0600

    fix(backend): T-159 r2 confirm and its event in one transaction (accept taken back on failure), trace events carry the confirm, tests kill the oldest-event and confirmed_at mutants
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/review.py              | 27 +++++++++++----
 app/backend/trace.py               |  3 +-
 tests/unit/test_t159_flag_audit.py | 68 ++++++++++++++++++++++++++++++++++++++
 3 files changed, 90 insertions(+), 8 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:29:08.142Z

**tool call — Bash**
````
{
 "command": "git show 99438fb -- app tests/unit/test_t146_r2_failed_rerun_keeps_items.py tests/unit/test_t146_r3_decided_items_never_lowered.py; git show c0e2b86 -- app"
}
````

### User / tool · 2026-11-02T15:29:08.269Z

**tool result**
````
commit 99438fb194d8a81737bd0bf18b02e0cba0a1c6d8
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:27:54 2026 -0600

    fix(backend): T-161 r2 first-run failure driven by failed_steps (flag step down with no phrase-list hit reads run_partial), extract-down first run with no entries reads failed
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index ce2b3eb..e9b7bed 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -423,9 +423,10 @@ def _items(n: int) -> str:
     return f"{n} item{'s' if n != 1 else ''}"
 
 
-def _partial_error(kept: list, empty: list):
+def _partial_error(kept: list, empty: list, down: tuple = ()):
     """T-146 r3: the case's honest message for a re-run that kept earlier work or had a step fail with nothing to fall back on (code `run_partial`), or None.
-    It names how many items and which steps, and says exactly what was kept."""
+    It names how many items and which steps, and says exactly what was kept. `down` (T-161 r2): steps that failed without leaving any row to count (the flag step on
+    records with no phrase-list hit makes no flag at all), named without a count."""
     failed, differed = [k for k in kept if k[2] == "failed"], [k for k in kept if k[2] == "disagreed"]
     parts = []
     if failed:
@@ -437,6 +438,8 @@ def _partial_error(kept: list, empty: list):
     if empty:
         parts.append(f"The AI step also failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) with no earlier result to keep." if kept else
                      f"The AI step failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) on this run, and there is no earlier result to keep.")
+    if down:
+        parts.append(f"The AI step ({' and '.join(sorted(down))}) failed on this run, so nothing from it could be used.")
     return {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None
 
 
@@ -580,7 +583,11 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
         err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
     else:
         status = "done_with_errors" if errors else "done"
-        err = _partial_error(kept, empty if rerun else [s for s in empty if s != _EXTRACT_STEP])      # T-161: a first run with a judge or the flag step down fails like a re-run; its extract failures stay tray items
+        # T-161: a first run with a judge or the flag step down fails like a re-run. The flag step is read from the steps that were down (a note with no phrase-list hit has no flag row to carry the failure).
+        # A first run's extract failures stay tray items while some entries came out; with no entry at all there is nothing to review, so it is failed and the step is named.
+        named = {c for _, c, _ in kept} | set(empty)
+        down = ("finding the flags",) if "flags" in failed_steps and "finding the flags" not in named else ()
+        err = _partial_error(kept, empty if (rerun or not (dated or undated)) else [s for s in empty if s != _EXTRACT_STEP], down)
     DB.update_case(conn, cid, status="failed" if (timed_out or err) else "ready", stage="finalize", error=json.dumps(err) if err else None,
                    run_finished_at=now_t, injection_records_json=ing["injection_records"])
     tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
diff --git a/tests/unit/test_t146_r2_failed_rerun_keeps_items.py b/tests/unit/test_t146_r2_failed_rerun_keeps_items.py
index 9d5c064..19415f7 100644
--- a/tests/unit/test_t146_r2_failed_rerun_keeps_items.py
+++ b/tests/unit/test_t146_r2_failed_rerun_keeps_items.py
@@ -89,7 +89,7 @@ def test_judge_down_rerun_keeps_judged_rows_instead_of_downgrading_them(tmp_path
     assert c["status"] == "failed"
 
 
-def test_first_run_with_a_down_step_still_stores_its_stubs_and_is_not_marked_partial(tmp_path):
+def test_first_run_with_extract_down_still_stores_its_stubs_and_is_failed_with_the_step_named(tmp_path):
     conn = DB.connect(str(tmp_path / "d.sqlite"))
     cid = DB.create_case(conn, G.raw("sample"), now=0.0)
     out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=_down("extract"))), now=lambda: 1.0)
@@ -97,7 +97,7 @@ def test_first_run_with_a_down_step_still_stores_its_stubs_and_is_not_marked_par
     rows = DB.list_items(conn, cid, "entry")
     assert len(rows) == 9 and all(r["state"] == "rejected" and r["state_reasons"] == ["LLM_FAILED_AFTER_RETRIES"] for r in rows)
     c, err = _err(conn, cid)
-    assert err is None and c["status"] == "ready"          # nothing earlier existed to keep
+    assert c["status"] == "failed" and err["code"] == "run_partial" and "(writing the entries)" in err["message"]      # T-161 r2: no entry at all on a first run reads failed, step named
 
 
 def test_a_later_good_rerun_replaces_the_kept_rows_and_clears_the_error(tmp_path):
diff --git a/tests/unit/test_t146_r3_decided_items_never_lowered.py b/tests/unit/test_t146_r3_decided_items_never_lowered.py
index 02e631c..ae5e6a4 100644
--- a/tests/unit/test_t146_r3_decided_items_never_lowered.py
+++ b/tests/unit/test_t146_r3_decided_items_never_lowered.py
@@ -211,7 +211,7 @@ def test_rerun_with_nothing_to_keep_still_says_the_step_failed(tmp_path):
     conn = DB.connect(str(tmp_path / "d.sqlite"))
     cid = DB.create_case(conn, G.raw("sample"), now=0.0)
     first = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=down("extract"))), now=lambda: 1.0)
-    assert first["status"] == "done_with_errors" and case_error(conn, cid) == ("ready", None)      # a first run: the tray shows the failed records, as before
+    assert first["status"] == "done_with_errors" and case_error(conn, cid)[0] == "failed"      # T-161 r2: a first run with no entries at all is failed too (steps named)
     again = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=down("extract"))), now=lambda: 2.0)
     assert again["status"] == "done_with_errors"
     status, err = case_error(conn, cid)
commit c0e2b86c02e9889353a9ac791e57283a3aec3607
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:28:09 2026 -0600

    fix(backend): T-159 r2 confirm and its event in one transaction (accept taken back on failure), trace events carry the confirm, tests kill the oldest-event and confirmed_at mutants
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/review.py b/app/backend/review.py
index 7481d74..80a65a0 100644
--- a/app/backend/review.py
+++ b/app/backend/review.py
@@ -217,15 +217,21 @@ def confirmed_accept(item: dict) -> bool:
 
 def _record_confirm(conn, case_id: str, item_id: str, item: dict, t) -> None:
     """The named confirm is kept on the item (ladder.confirm.confirmed_at) and in the accept event that carried it (after.confirm = {flag, name, confirmed_at}),
-    so GET /audit shows who confirmed which flag and when without reading the item (T-159, D-059)."""
+    so GET /audit shows who confirmed which flag and when without reading the item (T-159, D-059). Both writes are ONE transaction: a failure on either leaves neither."""
     f = (item.get("ladder") or {}).get("confirm")
     if item.get("kind") == "charge" and f:
         stamp = {"flag": f["flag"], "name": f["name"], "confirmed_at": store.iso(t)}
-        DB.update_item(conn, item_id, now=t, case=case_id, ladder={**item["ladder"], "confirm": {**f, "confirmed_at": stamp["confirmed_at"]}})
-        ev = conn.execute("SELECT id, after_json FROM review_events WHERE case_id=? AND item_id=? AND action='accept' ORDER BY at DESC, rowid DESC LIMIT 1", (case_id, item_id)).fetchone()
-        if ev:
-            after = json.loads(ev["after_json"]) if ev["after_json"] else {}
-            conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "confirm": stamp}), ev["id"]))
+        conn.execute("BEGIN")
+        try:
+            DB.update_item(conn, item_id, now=t, case=case_id, ladder={**item["ladder"], "confirm": {**f, "confirmed_at": stamp["confirmed_at"]}})
+            ev = conn.execute("SELECT id, after_json FROM review_events WHERE case_id=? AND item_id=? AND action='accept' ORDER BY at DESC, rowid DESC LIMIT 1", (case_id, item_id)).fetchone()
+            if ev:
+                after = json.loads(ev["after_json"]) if ev["after_json"] else {}
+                conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "confirm": stamp}), ev["id"]))
+            conn.execute("COMMIT")
+        except Exception:
+            conn.execute("ROLLBACK")
+            raise
 
 
 def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None) -> dict:
@@ -251,7 +257,14 @@ def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: di
             raise err
     out = DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)
     if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
-        _record_confirm(conn, case_id, item_id, item, now)
+        try:
+            _record_confirm(conn, case_id, item_id, item, now)
+        except Exception:
+            back = {"pending": "reset", "dismissed": "dismiss"}.get(item.get("review_status"))      # T-159 r2: take the accept back, so no charge counts without its confirm on record
+            if back:
+                DB.apply_review(conn, item_id, back, now=now, case=case_id)
+            raise
+        out = DB.get_item(conn, item_id, case_id)
     return out
 
 
diff --git a/app/backend/trace.py b/app/backend/trace.py
index 3792c72..3b48c2c 100644
--- a/app/backend/trace.py
+++ b/app/backend/trace.py
@@ -241,7 +241,8 @@ def _human_step(cx, row, kind, *, blocks_ok=True, extra_pending_next=None):
     rs, rejected = row["review_status"], row["state"] == "rejected"
     evs = cx.events.get(row["id"], [])
     ev = {"action": present.STATUS_ACTION.get(rs), "at": ((row.get("edited") or {}).get("at") if rs == "edited" else None),
-          "events": [{"action": e["action"], "at": store.iso(e["at"]), **({"before": e["before"], "after": e["after"]} if cx.full else {})} for e in evs]}
+          "events": [{"action": e["action"], "at": store.iso(e["at"]), **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),
+                      **({"before": e["before"], "after": e["after"]} if cx.full else {})} for e in evs]}
     if evs:
         ev["at"] = store.iso(evs[-1]["at"])
     if rs == "edited":
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:29:10.353Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -d .venv/bin/python; (cd $S/r2a && ln -s /Users/arsis/zlayt-pm-project/.venv .venv 2>/dev/null; ls -la .venv | head -2; nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider > $S/unit_r2a.txt 2>&1 &) ; echo started",
 "run_in_background": false
}
````

### User / tool · 2026-11-02T15:29:10.447Z

**tool result**
````
.venv/bin/python
lrwxr-xr-x@ 1 arsis  wheel  35 Nov  2 09:29 .venv -> /Users/arsis/zlayt-pm-project/.venv
started
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:29:22.178Z

**tool call — Bash**
````
{
 "command": "sed -n 195,275p app/backend/review.py; grep -n \"def apply_review\" -A45 app/db/db.py; grep -n \"ACTIONS\" app/db/db.py | head"
}
````

### User / tool · 2026-11-02T15:29:22.277Z

**tool result**
````
    rid = (item.get("record_ids") or [None])[0]
    return next((r for r in recs if r["id"] == rid), None)


def confirm_error(item_id: str, item: dict, confirm):
    """D-059: a charge that carries a likely_duplicate or likely_total flag is accepted only when the call names that flag (`confirm`). A 422 CONFIRM_REQUIRED
    with the flag and the exact word to send, else None. Code only: the flag was set by amounts.py, not by a model, and a judge answer does not clear it."""
    f = (item.get("ladder") or {}).get("confirm")
    if item.get("kind") != "charge" or not f or confirm == f["confirm_with"]:
        return None
    detail = {"item_id": item_id, "reason_code": "CONFIRM_REQUIRED", "flag": f["flag"], "name": f["name"], "confirm_with": f["confirm_with"], "of": f.get("of"),
              "message": f["message"],      # T-159: the flag's own sentence, without the "confirm by name" tail, so a client never strips the token out of the error message
              "next_action": {"code": "CONFIRM_FLAG", "text": "Confirm the flag by name, or dismiss the charge", "target": {"item_id": item_id}}}
    wrong = "" if confirm is None else " The confirm you sent does not name this flag."
    return ReviewError(422, "CONFIRM_REQUIRED", detail, f"{f['name']}: {f['message']} It is not counted unless you confirm that flag by name ({f['confirm_with']}).{wrong}")


def confirmed_accept(item: dict) -> bool:
    """T-159: a charge that is accepted and whose flag has been confirmed by name. A repeat accept of it changes nothing, so it writes nothing."""
    f = (item.get("ladder") or {}).get("confirm")
    return item.get("kind") == "charge" and bool(f) and bool(f.get("confirmed_at")) and item.get("review_status") == "accepted"      # item["kind"] = the amount's class


def _record_confirm(conn, case_id: str, item_id: str, item: dict, t) -> None:
    """The named confirm is kept on the item (ladder.confirm.confirmed_at) and in the accept event that carried it (after.confirm = {flag, name, confirmed_at}),
    so GET /audit shows who confirmed which flag and when without reading the item (T-159, D-059). Both writes are ONE transaction: a failure on either leaves neither."""
    f = (item.get("ladder") or {}).get("confirm")
    if item.get("kind") == "charge" and f:
        stamp = {"flag": f["flag"], "name": f["name"], "confirmed_at": store.iso(t)}
        conn.execute("BEGIN")
        try:
            DB.update_item(conn, item_id, now=t, case=case_id, ladder={**item["ladder"], "confirm": {**f, "confirmed_at": stamp["confirmed_at"]}})
            ev = conn.execute("SELECT id, after_json FROM review_events WHERE case_id=? AND item_id=? AND action='accept' ORDER BY at DESC, rowid DESC LIMIT 1", (case_id, item_id)).fetchone()
            if ev:
                after = json.loads(ev["after_json"]) if ev["after_json"] else {}
                conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "confirm": stamp}), ev["id"]))
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise


def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None) -> dict:
    """THE one place a review decision is written (DB.apply_review is called from here for accept, edit, dismiss, reset and the batch).
    D-051: whenever the decision leaves an ENTRY accepted or edited (so in the letter), the code checks are recomputed from the wording that
    decision would leave (`edited` replaces the current text; stored code reasons are dropped because the new text is what counts) and a
    failure is a 422 CODE_CHECK_FAILED before anything is written. The judge verdict, the stored state and who wrote the wording do not matter."""
    if kind is None or item is None:
        kind, item = _item(conn, case_id, item_id)
    if kind == "entry" and DB.ACTIONS.get(action) in ("accepted", "edited"):
        cand = dict(item)
        if edited is not None:
            cand["edited"] = edited
            cand["state_reasons"] = [c for c in item.get("state_reasons") or [] if c not in CODE_CHECK_REASONS]
        err = code_check_error(item_id, entry_record(cand, recs if recs is not None else store.load_records(conn, case_id)), cand) or charge_text_error(item_id, cand, lambda: bill_state_for(conn, case_id, item.get("record_ids")))
        if err:
            raise err
    if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
        if confirmed_accept(item):
            return item                                     # T-159: already accepted with its flag confirmed; a repeat accept writes no second decision
        err = confirm_error(item_id, item, confirm)         # D-059
        if err:
            raise err
    out = DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)
    if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
        try:
            _record_confirm(conn, case_id, item_id, item, now)
        except Exception:
            back = {"pending": "reset", "dismissed": "dismiss"}.get(item.get("review_status"))      # T-159 r2: take the accept back, so no charge counts without its confirm on record
            if back:
                DB.apply_review(conn, item_id, back, now=now, case=case_id)
            raise
        out = DB.get_item(conn, item_id, case_id)
    return out


def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
215:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
216-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
217-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
218-    if action not in ACTIONS:
219-        raise ValueError(f"invalid review action {action!r}")
220-    table, row = _find(conn, item_id, case)
221-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
222-    status = ACTIONS[action] or row["review_status"]
223-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
224-    if action == "edit" and not new_edited:
225-        raise ValueError("edit requires a non-empty edited payload")
226-    after = {"review_status": status, "edited": new_edited}
227-    conn.execute("BEGIN")
228-    try:
229-        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
230-                     (status, _enc(new_edited), now, item_id, row["case_id"]))
231-        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
232-                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
233-        conn.execute("COMMIT")
234-    except Exception:
235-        conn.execute("ROLLBACK")
236-        raise
237-    return get_item(conn, item_id, row["case_id"])
238-
239-
240-def log_event(conn, case_id: str, item_id: str, action: str, before=None, after=None, now: float = 0) -> str:
241-    """Append an audit-only row to review_events (reclassify, rejudge). It never touches review_status; apply_review stays the only writer of that."""
242-    if action not in AUDIT_ONLY_ACTIONS:
243-        raise ValueError(f"log_event only writes {AUDIT_ONLY_ACTIONS}, not {action!r}")
244-    eid = _tok("v")
245-    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
246-                 (eid, case_id, item_id, action, _enc(before), _enc(after), now))
247-    return eid
248-
249-
250-def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
251-    if status not in REVIEW_STATUSES:
252-        raise ValueError(f"invalid review_status {status!r}")
253-    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
254-    apply_review(conn, item_id, action, edited=edited, now=now, case=case)
255-
256-
257-def list_events(conn, case_id: str, item_id: str = None) -> list:
258-    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
259-    if item_id:
260-        q, a = q + " AND item_id=?", a + [item_id]
19:ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
34:AUDIT_ONLY_ACTIONS = ("reclassify", "rejudge")          # logged by log_event(); never change review_status, so apply_review() refuses them
218:    if action not in ACTIONS:
222:    status = ACTIONS[action] or row["review_status"]
242:    if action not in AUDIT_ONLY_ACTIONS:
243:        raise ValueError(f"log_event only writes {AUDIT_ONLY_ACTIONS}, not {action!r}")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:29:32.868Z

**tool call — Bash**
````
{
 "command": "grep -n \"def update_item\" -A25 app/db/db.py | head -50; grep -rn \"set_review(\" app | grep -v \"def set_review\"; git show c0e2b86 -- tests | head -120; cat $S 2>/dev/null; tail -3 /private/tmp/claude-501/*/*/scratchpad/unit_r2a.txt 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T15:29:34.954Z

**tool result**
````
200:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
201-    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
202-    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
203-    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
204-    if locked & set(fields):
205-        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
206-    table, found = _find(conn, item_id, case)
207-    bad = set(fields) - _cols(conn, table)
208-    if bad:
209-        raise ValueError(f"unknown {table} fields {sorted(bad)}")
210-    fields["updated_at"] = now
211-    sets = ", ".join(f"{k}=?" for k in fields)
212-    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])
213-
214-
215-def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
216-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
217-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
218-    if action not in ACTIONS:
219-        raise ValueError(f"invalid review action {action!r}")
220-    table, row = _find(conn, item_id, case)
221-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
222-    status = ACTIONS[action] or row["review_status"]
223-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
224-    if action == "edit" and not new_edited:
225-        raise ValueError("edit requires a non-empty edited payload")
app/backend/review.py:286:        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)
app/backend/review.py:394:        set_review(conn, case_id, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, kind="flag", item=item)
app/backend/review.py:437:    set_review(conn, case_id, item["id"], "edit", edited=edited, now=t, kind="entry", item=item, recs=recs)     # D-051: edit implies accept; refused before any write
app/backend/review.py:765:    set_review(conn, case_id, item_id, action, now=now, recs=recs)
commit c0e2b86c02e9889353a9ac791e57283a3aec3607
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:28:09 2026 -0600

    fix(backend): T-159 r2 confirm and its event in one transaction (accept taken back on failure), trace events carry the confirm, tests kill the oldest-event and confirmed_at mutants
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_t159_flag_audit.py b/tests/unit/test_t159_flag_audit.py
index 5b3e7bd..e13f548 100644
--- a/tests/unit/test_t159_flag_audit.py
+++ b/tests/unit/test_t159_flag_audit.py
@@ -3,6 +3,7 @@ the flag sentence is plain words (no internal id, no token), and a repeat accept
 import re
 
 import pytest
+from fastapi.testclient import TestClient
 
 from tests.unit.test_amounts_d059_api import NOTE, charges, make_env
 
@@ -99,6 +100,73 @@ def test_accept_again_after_a_reset_needs_the_confirm_again(promoted):
     assert len(accept_events(c, tok, f["id"])) == 2
 
 
+def test_each_accept_event_after_a_reset_carries_its_own_confirm(promoted):
+    """r2 mutant: the confirm must land on the NEWEST accept event, so the first accept keeps its own and the second gets the second confirm."""
+    c, tok, f = promoted
+    first = review(c, tok, f["id"], confirm="likely_duplicate").json()["item"]["flag"]["confirmed_at"]
+    assert c.post(f"/api/cases/{tok}/items/{f['id']}/review", json={"action": "reset"}).status_code == 200
+    second = review(c, tok, f["id"], confirm="likely_duplicate").json()["item"]["flag"]["confirmed_at"]
+    ev = sorted(accept_events(c, tok, f["id"]), key=lambda e: e["at"])
+    assert [e["confirm"]["confirmed_at"] for e in ev] == [first, second]
+    assert all(e["confirm"]["flag"] == "likely_duplicate" for e in ev)
+
+
+def _db(tmp_path):
+    from app.db import db as DB
+    return DB.connect(str(tmp_path / "d059.sqlite"))
+
+
+def test_an_accepted_flagged_charge_whose_confirm_has_no_timestamp_asks_for_the_confirm_again(promoted, tmp_path):
+    """r2 mutant: the no-op needs the confirm to have happened (confirmed_at), not just the flag to exist on an accepted charge."""
+    from app.db import db as DB
+    c, tok, f = promoted
+    review(c, tok, f["id"], confirm="likely_duplicate")
+    conn = _db(tmp_path)
+    cid = DB.get_case_by_token(conn, tok)["id"] if hasattr(DB, "get_case_by_token") else conn.execute("SELECT id FROM cases").fetchone()["id"]
+    item = DB.get_item(conn, f["id"], cid)
+    DB.update_item(conn, f["id"], now=9.0, case=cid, ladder={**item["ladder"], "confirm": {k: v for k, v in item["ladder"]["confirm"].items() if k != "confirmed_at"}})
+    r = review(c, tok, f["id"])
+    assert r.status_code == 422 and r.json()["error"]["code"] == "CONFIRM_REQUIRED"
+
+
+# ---------------------------------------------------------------- one transaction
+def test_a_failure_writing_the_confirm_leaves_no_half_confirmed_charge(promoted, monkeypatch):
+    """r2: the item's confirm and the event's confirm are written in ONE transaction, so a failure on the second write rolls back the first (the item never shows a
+    confirmed_at the event lacks), and the accept that preceded them is taken back: the charge is pending again and counts for nothing. A retry then works."""
+    from app.backend import review as RV
+    c, tok, f = promoted
+    real = RV.json
+
+    class Boom:
+        def __getattr__(self, name):
+            return getattr(real, name)
+
+        def loads(self, *a, **k):
+            raise RuntimeError("injected failure writing the event")
+    monkeypatch.setattr(RV, "json", Boom())
+    bad = TestClient(c.app, client=("127.0.0.1", 50000), raise_server_exceptions=False)
+    totals_before = c.get(f"/api/cases/{tok}").json()["totals"]
+    assert review(bad, tok, f["id"], confirm="likely_duplicate").status_code == 500
+    monkeypatch.setattr(RV, "json", real)
+    g = c.get(f"/api/cases/{tok}").json()
+    now = next(a for a in g["amounts"] if a["id"] == f["id"])
+    assert now["review_status"] == "pending" and not now["flag"].get("confirmed_at")
+    assert g["totals"] == totals_before                                                      # never counted without its confirm
+    assert review(c, tok, f["id"]).status_code == 422                                       # a bare accept is still refused
+    ok = review(c, tok, f["id"], confirm="likely_duplicate")
+    assert ok.status_code == 200 and ok.json()["item"]["flag"]["confirmed_at"]
+    ev = sorted(accept_events(c, tok, f["id"]), key=lambda e: e["at"])
+    assert ev[-1]["confirm"]["confirmed_at"] == ok.json()["item"]["flag"]["confirmed_at"]   # the accept that stands carries its own confirm
+    assert [e["action"] for e in c.get(f"/api/cases/{tok}/audit").json()["events"] if e["item_id"] == f["id"] and e["action"] in ("accept", "reset")].count("reset") == 1      # the taken-back accept is in the trail
+
+
+def test_the_trace_events_carry_the_confirm(promoted):
+    c, tok, f = promoted
+    at = review(c, tok, f["id"], confirm="likely_duplicate").json()["item"]["flag"]["confirmed_at"]
+    ev = [e for e in steps(c, tok, f["id"])["human"]["evidence"]["events"] if e["action"] == "accept"]
+    assert ev[0]["confirm"] == {"flag": "likely_duplicate", "name": "Likely duplicate", "confirmed_at": at}
+
+
 def test_a_wrong_confirm_is_still_refused_before_the_first_accept(promoted):
     c, tok, f = promoted
     r = review(c, tok, f["id"], confirm="likely_total")
........................................................................ [ 14%]
........................................................................ [ 16%]
................................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:29:47.276Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/unit/test_t159_flag_audit.py; sed -n 276,300p app/backend/review.py; grep -n \"edit\" app/backend/api.py | grep -i amount | head"
}
````

### User / tool · 2026-11-02T15:29:47.388Z

**tool result**
````
"""T-159 (D-059 audit trail of a flagged charge): the named confirm is in the review event (GET /audit, also in public mode), the item trace has a charge_flag step,
the flag sentence is plain words (no internal id, no token), and a repeat accept of a charge already accepted with its flag confirmed is a no-op."""
import re

import pytest
from fastapi.testclient import TestClient

from tests.unit.test_amounts_d059_api import NOTE, charges, make_env


@pytest.fixture
def promoted(tmp_path, monkeypatch):
    """NOTE: four unclear figures promoted to charges one by one; the second 04/16 manual therapy $150.00 (record 2) is a likely_duplicate of the one in record 1."""
    c, tok, _ = make_env(tmp_path, monkeypatch, NOTE)
    for a in [a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["kind"] != "damages"]:
        assert c.post(f"/api/cases/{tok}/items/{a['id']}/reclassify", json={"to": "charge"}).status_code == 200
    f = next(a for a in charges(c, tok) if a["flag"])
    return c, tok, f


def review(c, tok, item, **body):
    return c.post(f"/api/cases/{tok}/items/{item}/review", json={"action": "accept", **body})


def accept_events(c, tok, item):
    return [e for e in c.get(f"/api/cases/{tok}/audit").json()["events"] if e["item_id"] == item and e["action"] == "accept"]


def steps(c, tok, item):
    return {s["id"]: s for s in c.get(f"/api/cases/{tok}/items/{item}/trace").json()["steps"]}


# ---------------------------------------------------------------- the sentence
def test_the_duplicate_sentence_names_the_other_line_not_its_id(promoted):
    c, tok, f = promoted
    msg = f["flag"]["message"]
    assert not re.search(r"\b[aeqf]\d+\b", msg), msg
    assert "04/16/2026 manual therapy invoiced $150.00." in msg and "record 1" in msg           # service, amount, date, record: the other charge's own line
    assert "Counting both would count one service twice." in msg
    assert f["flag"]["of"] and f["flag"]["of"] != f["id"]                                      # the id is still there for a client that wants to jump to it, not in the words


def test_confirm_required_carries_the_flags_own_sentence_without_the_token(promoted):
    c, tok, f = promoted
    r = review(c, tok, f["id"])
    err = r.json()["error"]
    assert r.status_code == 422 and err["code"] == "CONFIRM_REQUIRED"
    assert err["detail"]["message"] == f["flag"]["message"]
    assert "likely_duplicate" not in err["detail"]["message"] and "confirm" not in err["detail"]["message"].lower()
    assert not re.search(r"\b[aeqf]\d+\b", err["message"])


# ---------------------------------------------------------------- the review event
def test_the_accept_event_carries_the_named_confirm_in_public_mode(promoted, monkeypatch):
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    c, tok, f = promoted
    assert accept_events(c, tok, f["id"]) == []
    ok = review(c, tok, f["id"], confirm="likely_duplicate")
    assert ok.status_code == 200
    ev = accept_events(c, tok, f["id"])
        raise _bad("That action is not allowed.")
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
        raise _date_unconfirmed_error()
    warnings = []
    if action in ("accept", "dismiss", "reset"):
        confirm = body.get("confirm")
        if confirm is not None and not isinstance(confirm, str):
            raise _bad("The confirm must be the name of the flag.")
        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)
        if action == "reset":
            restore_pre_edit(conn, case_id, item_id, kind, item, t)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}


def ocr_record_ids(conn, case_id: str) -> set:
    """Ids of the records whose text lies on an OCR-read page of this case (empty for a text case). T-086, D-042."""
    from app.backend import pdf_checks
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:30:05.949Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/probes159; cat > $S/probes159/test_probe159.py <<'EOF'\nimport pytest\nfrom fastapi.testclient import TestClient\nfrom tests.unit.test_t159_flag_audit import promoted, review, accept_events  # noqa\nfrom tests.unit.test_amounts_d059_api import charges\n\n\ndef item(c, tok, iid):\n    return next(a for a in c.get(f\"/api/cases/{tok}\").json()[\"amounts\"] if a[\"id\"] == iid)\n\n\ndef boom_json(monkeypatch):\n    from app.backend import review as RV\n    real = RV.json\n    class Boom:\n        def __getattr__(self, n): return getattr(real, n)\n        def loads(self, *a, **k): raise RuntimeError(\"inj\")\n    monkeypatch.setattr(RV, \"json\", Boom())\n    return real, RV\n\n\ndef test_prior_dismissed_failure_goes_back_to_dismissed(promoted, monkeypatch):\n    c, tok, f = promoted\n    assert c.post(f\"/api/cases/{tok}/items/{f['id']}/review\", json={\"action\": \"dismiss\"}).status_code == 200\n    real, RV = boom_json(monkeypatch)\n    bad = TestClient(c.app, client=(\"127.0.0.1\", 50000), raise_server_exceptions=False)\n    assert review(bad, tok, f[\"id\"], confirm=\"likely_duplicate\").status_code == 500\n    monkeypatch.setattr(RV, \"json\", real)\n    it = item(c, tok, f[\"id\"])\n    print(\"PRIOR_DISMISSED ->\", it[\"review_status\"], it[\"flag\"].get(\"confirmed_at\"))\n    assert it[\"review_status\"] == \"dismissed\"\n\n\ndef test_compensation_itself_fails(promoted, monkeypatch):\n    c, tok, f = promoted\n    from app.backend import review as RV\n    real_apply = RV.DB.apply_review\n    calls = {\"n\": 0}\n    def flaky(*a, **k):\n        calls[\"n\"] += 1\n        if calls[\"n\"] == 2: raise RuntimeError(\"back failed\")\n        return real_apply(*a, **k)\n    real, _ = boom_json(monkeypatch)\n    monkeypatch.setattr(RV.DB, \"apply_review\", flaky)\n    bad = TestClient(c.app, client=(\"127.0.0.1\", 50000), raise_server_exceptions=False)\n    r = bad.post(f\"/api/cases/{tok}/items/{f['id']}/review\", json={\"action\": \"accept\", \"confirm\": \"likely_duplicate\"})\n    print(\"BACKFAIL status\", r.status_code, r.text[:200])\n    monkeypatch.setattr(RV, \"json\", real)\n    monkeypatch.setattr(RV.DB, \"apply_review\", real_apply)\n    g = c.get(f\"/api/cases/{tok}\").json()\n    it = item(c, tok, f[\"id\"])\n    print(\"BACKFAIL item\", it[\"review_status\"], it[\"flag\"].get(\"confirmed_at\"), g[\"totals\"])\n    r2 = review(c, tok, f[\"id\"])\n    print(\"BACKFAIL bare accept after ->\", r2.status_code)\n\n\ndef test_item_write_failure_rolls_back(promoted, monkeypatch):\n    c, tok, f = promoted\n    from app.backend import review as RV\n    real = RV.DB.update_item\n    def bad_up(*a, **k):\n        raise RuntimeError(\"item write\")\n    monkeypatch.setattr(RV.DB, \"update_item\", bad_up)\n    bad = TestClient(c.app, client=(\"127.0.0.1\", 50000), raise_server_exceptions=False)\n    assert review(bad, tok, f[\"id\"], confirm=\"likely_duplicate\").status_code == 500\n    monkeypatch.setattr(RV.DB, \"update_item\", real)\n    it = item(c, tok, f[\"id\"])\n    print(\"ITEMFAIL ->\", it[\"review_status\"], it[\"flag\"].get(\"confirmed_at\"))\n    assert it[\"review_status\"] == \"pending\"\n    ev = [e for e in c.get(f\"/api/cases/{tok}/audit\").json()[\"events\"] if e[\"item_id\"] == f[\"id\"]]\n    print(\"ITEMFAIL events\", [(e[\"action\"], e.get(\"confirm\")) for e in ev])\n\n\ndef test_prior_accepted_no_confirmed_at_failure(promoted, monkeypatch, tmp_path):\n    \"\"\"accepted flagged charge with confirm lacking confirmed_at; accept with confirm; event write fails.\"\"\"\n    c, tok, f = promoted\n    from app.db import db as DB\n    assert review(c, tok, f[\"id\"], confirm=\"likely_duplicate\").status_code == 200\n    conn = DB.connect(str(tmp_path / \"d059.sqlite\"))\n    cid = conn.execute(\"SELECT id FROM cases\").fetchone()[\"id\"]\n    cur = DB.get_item(conn, f[\"id\"], cid)\n    DB.update_item(conn, f[\"id\"], now=9.0, case=cid, ladder={**cur[\"ladder\"], \"confirm\": {k: v for k, v in cur[\"ladder\"][\"confirm\"].items() if k != \"confirmed_at\"}})\n    real, RV = boom_json(monkeypatch)\n    bad = TestClient(c.app, client=(\"127.0.0.1\", 50000), raise_server_exceptions=False)\n    assert review(bad, tok, f[\"id\"], confirm=\"likely_duplicate\").status_code == 500\n    monkeypatch.setattr(RV, \"json\", real)\n    it = item(c, tok, f[\"id\"])\n    g = c.get(f\"/api/cases/{tok}\").json()\n    print(\"PRIOR_ACCEPTED_NOCONF ->\", it[\"review_status\"], it[\"flag\"].get(\"confirmed_at\"), g[\"totals\"])\nEOF\ncd $S/r2a && tail -2 $S/unit_r2a.txt | cut -c1-200; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest $S/probes159/test_probe159.py -p no:cacheprovider -q -s 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T15:30:08.667Z

**tool result**
````
........................................................................ [ 35%]
.................................................................PRIOR_DISMISSED -> dismissed None
.BACKFAIL status 500 {"error":{"code":"internal","message":"Something went wrong.","detail":{}}}
BACKFAIL item accepted None {'accepted': {'cents': 15000, 'count': 1, 'label': 'Accepted charges'}, 'pending': {'cents': 51000, 'count': 3, 'label': 'Pending review'}, 'detected_not_a_total': {'cents': 66000, 'count': 4, 'label': 'Detected (not a total)'}, 'flagged_charges': [], 'not_totaled': [], 'possible_overlaps': []}
BACKFAIL bare accept after -> 422
.ITEMFAIL -> pending None
ITEMFAIL events [('reclassify', None), ('accept', None), ('reset', None)]
.PRIOR_ACCEPTED_NOCONF -> accepted None {'accepted': {'cents': 15000, 'count': 1, 'label': 'Accepted charges'}, 'pending': {'cents': 51000, 'count': 3, 'label': 'Pending review'}, 'detected_not_a_total': {'cents': 66000, 'count': 4, 'label': 'Detected (not a total)'}, 'flagged_charges': [], 'not_totaled': [], 'possible_overlaps': []}
.
4 passed in 2.21s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:30:15.333Z

**tool call — Bash**
````
{
 "command": "grep -n \"confirmed_at\\|confirm_with\\|\\\"confirm\\\"\" app/backend/*.py | grep -v \"^app/backend/review.py\" | head -30; tail -c 300 /private/tmp/claude-501/*/*/scratchpad/unit_r2a.txt | tail -3"
}
````

### User / tool · 2026-11-02T15:30:15.480Z

**tool result**
````
app/backend/amounts.py:607:    """The flag a charge carries until the paralegal confirms it by name (D-059). `confirm_with` is the exact word the accept call must send. `of` is the other charge's
app/backend/amounts.py:612:    return {"flag": flag, "name": CONFIRM_NAMES[flag], "message": msg, "confirm_with": flag, "of": of}
app/backend/amounts.py:742:            a["confirm"] = confirm_info("likely_total") if i in totals else None
app/backend/amounts.py:743:        found += [{**d, "confirm": None, "basis": None} for d in damages_mentions(r["excerpt"])]
app/backend/amounts.py:747:                         "confirm": a["confirm"], "basis": a["basis"]})
app/backend/present.py:75:    f = (row.get("ladder") or {}).get("confirm") if row["kind"] == "charge" else None
app/backend/present.py:76:    return (None, False) if not f else ({k: f.get(k) for k in ("flag", "name", "message", "confirm_with", "of", "confirmed_at")}, row["review_status"] == "pending")
app/backend/present.py:392:                        **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),      # T-159: the flag she confirmed by name (metadata, also in public mode)
app/backend/pipeline.py:108:            "confirm": a.get("confirm")}
app/backend/pipeline.py:399:                   **({"confirm": a["confirm"]} if a.get("confirm") else {})}      # D-059: the flag the paralegal must confirm by name before accepting this charge
app/backend/reclassify.py:152:    lad.pop("confirm", None)
app/backend/reclassify.py:156:            lad["confirm"] = flag
app/backend/trace.py:244:          "events": [{"action": e["action"], "at": store.iso(e["at"]), **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),
app/backend/trace.py:256:        cf = (row.get("ladder") or {}).get("confirm") if kind == "amount" and rs == "accepted" else None
app/backend/trace.py:257:        said = f"You accepted this item and confirmed the flag \u201c{cf['name']}\u201d by name." if cf and cf.get("confirmed_at") else "You accepted this item."      # T-159
app/backend/trace.py:531:    if rs in ("accepted", "edited") and cf.get("confirmed_at"):
app/backend/trace.py:532:        at = cf["confirmed_at"]
app/backend/trace.py:534:                    rule="D-059", evidence={"values": {**vals, "confirmed_at": at}})
app/backend/trace.py:585:    cf = lad.get("confirm") if kind == "charge" and not gfail and row["state"] != "rejected" else None
........................................................................ [ 36%]
........................................................................ [ 38%]
..........................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:30:36.439Z

**tool call — Bash**
````
{
 "command": "grep -n \"failed_steps\\|_FLAG_FAIL\\|def _noting\\|def _failure\" app/backend/pipeline.py | head -30; sed -n 236,262p app/backend/pipeline.py; sed -n 440,470p app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T15:30:36.581Z

**tool result**
````
242:_FLAG_FAIL = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS"}      # a flag made while the flag step failed carries one of these (it is the lexicon floor, nothing the model checked)
247:def _failure(kind: str, it: dict):
252:    if kind == "flag" and set(it.get("reasons") or []) & _FLAG_FAIL:
265:        return None if set(old.get("state_reasons") or []) & _FLAG_FAIL else cause
446:def _noting(raw_call, failed_steps: list):
453:            failed_steps.append(step)
461:    call = _noting(call or AU.make_call(conn, cid, now=clock), failed_steps := [])
578:                               prune="flags" not in failed_steps)      # conflicts are code candidates + judge 3: a down judge leaves them in the run, only the flag step can lose a stored flag
589:        down = ("finding the flags",) if "flags" in failed_steps and "finding the flags" not in named else ()
            continue
        e["ladder"]["judge"] = {"model": None, "prompt_version": None, "call_id": None, "verdict": "unavailable", "reason_code": JUDGE_NOT_RUN}
        generator.compose(e, by_n[e["seq"]], judge="unavailable")


_STUB_REASONS = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"}      # an entry rejected for one of these has no output at all: a stub
_FLAG_FAIL = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS"}      # a flag made while the flag step failed carries one of these (it is the lexicon floor, nothing the model checked)
_RANK = {"verified": 0, "needs_review": 1, "rejected": 2}
_EXTRACT_STEP = "writing the entries"


def _failure(kind: str, it: dict):
    """T-146 r3: what failed in the NEW row `it` alone, as the step's name, or None: an entry that is a failure stub (the AI step gave nothing), a flag made while the flag
    step failed, or an item whose second check was asked and gave no answer."""
    if kind == "entry" and it.get("state") == "rejected" and set(it.get("reasons") or []) & _STUB_REASONS:
        return _EXTRACT_STEP
    if kind == "flag" and set(it.get("reasons") or []) & _FLAG_FAIL:
        return "finding the flags"
    return "the second check" if ((it.get("ladder") or {}).get("judge") or {}).get("verdict") == "unavailable" else None


def _degrades(kind: str, old: dict, it: dict):
    """T-146 r2/r3: would storing `it` over the stored row `old` replace output with a failure, or take back a second-check answer? Returns the step's name or None.
    (entry) the AI step gave nothing where the stored row has a summary and a quote; (flag) the flag step failed and the stored row was not made from a failure;
    (any AI-made item) the second check gave no answer where the stored row had one. A failure is never allowed to erase earlier work."""
    cause = _failure(kind, it)
    if cause == _EXTRACT_STEP:
                     f"The AI step failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) on this run, and there is no earlier result to keep.")
    if down:
        parts.append(f"The AI step ({' and '.join(sorted(down))}) failed on this run, so nothing from it could be used.")
    return {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None


def _noting(raw_call, failed_steps: list):
    """T-146 r2: the same `call`, remembering the steps whose call failed (the AI layer gave up, or a fixture was missing). The failure still propagates to the
    caller's own handling; this only lets the run say which steps were down."""
    def call(step, system, user, schema, *, item_id=None):
        try:
            return raw_call(step, system, user, schema, item_id=item_id)
        except (AU.LLMFailed, P.FixtureMiss):
            failed_steps.append(step)
            raise
    return call


def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
    clock = now if callable(now) else (lambda: time.time() if now is None else now)
    t0 = clock()
    call = _noting(call or AU.make_call(conn, cid, now=clock), failed_steps := [])
    errors, stage_done = [], []

    def set_stage(name):
        if on_stage:
            on_stage(name)
        DB.update_case(conn, cid, status="running", stage=name)

    def expired():
        return clock() - t0 > deadline_s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:30:40.643Z

**tool call — Bash**
````
{
 "command": "sed -n 1,200p tests/unit/test_t161_first_run_stage_down.py"
}
````

### User / tool · 2026-11-02T15:30:40.723Z

**tool result**
````
"""T-161: a FIRST run with a stage down (flags, judge 1-4) reads like a re-run that fails: the case is failed / run_partial, the message names the step, and the export
gate lists RUN_FAILED. A clean first run stays ready.
r2: the flag step is read from the steps that were down (not from lexicon flag rows), so it fails the case on a note with no phrase-list hit too; a first run whose extract
step gave NO entries at all is failed too (writing the entries named); a first run where only some records failed extraction keeps its old shape (tray items, case ready)."""
import pytest
from app.backend import pipeline as PL, trace
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record
from tests.unit.test_t146_r3_decided_items_never_lowered import TAIL, case_error, down, model_flag

NOTHING_KEPT = "The AI step failed for {n} (the second check) on this run, and there is no earlier result to keep." + TAIL


def first_run(tmp_path, **script):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    script.setdefault("flags", model_flag)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(**script)), now=lambda: 1.0)
    return conn, cid, out


def blockers(conn, cid):
    return [b["reason_code"] for b in trace.export_blockers(conn, cid)]


def test_a_clean_first_run_stays_ready(tmp_path):
    conn, cid, out = first_run(tmp_path)
    assert out["status"] == "done" and out["error"] is None
    assert case_error(conn, cid) == ("ready", None)
    assert "RUN_FAILED" not in blockers(conn, cid)


@pytest.mark.parametrize("step,n,what", [("j1", 9, "items"), ("j2", None, None), ("j4", None, None), ("j3", 1, "item")], ids=["j1", "j2", "j4", "j3"])
@pytest.mark.parametrize("miss", [False, True], ids=["down", "fixture_miss"])
def test_first_run_with_a_judge_down_fails_the_case_and_names_the_step(tmp_path, step, n, what, miss):
    conn, cid, out = first_run(tmp_path, **{step: PL.AU.LLMFailedFixtureMiss("x") if miss else down(step)})
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial"
    assert out["error"] == err
    assert err["message"].startswith("The AI step failed for ") and "(the second check) on this run, and there is no earlier result to keep." in err["message"]
    assert err["message"].endswith(TAIL)
    assert "RUN_FAILED" in blockers(conn, cid)
    if n:
        assert err["message"] == NOTHING_KEPT.format(n=f"{n} {what}")


def test_first_run_with_the_flag_step_down_fails_the_case_and_names_the_step(tmp_path):
    conn, cid, out = first_run(tmp_path, flags=down("flags"))
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial" and out["error"] == err
    assert "(finding the flags) on this run, and there is no earlier result to keep." in err["message"] and err["message"].endswith(TAIL)
    assert "RUN_FAILED" in blockers(conn, cid)


def test_first_run_with_the_flag_step_missing_a_fixture_fails_the_case_too(tmp_path):
    conn, cid, _ = first_run(tmp_path, flags=PL.AU.LLMFailedFixtureMiss("x"))
    assert case_error(conn, cid)[0] == "failed" and "RUN_FAILED" in blockers(conn, cid)


NOTE = ('=== Record 1 ===\nDate: 2026-05-01\nSource: Brindlewood Physical Therapy, visit note\n'
        'Excerpt: "Patient seen for follow up of neck stiffness. Range of motion improved."\n\n'
        '=== Record 2 ===\nDate: 2026-05-10\nSource: Brindlewood Physical Therapy, visit note\n'
        'Excerpt: "Patient seen. Physical therapy continued 2x per week."\n')      # SYNTHETIC; no phrase-list hit, no dollar amount
NOTE_SCRIPT = sample_script(extract=lambda u: dict(summary="Physical therapy continued.", excerpt="Physical therapy continued 2x per week.") if "Physical therapy continued" in u
                            else dict(summary="Range of motion improved.", excerpt="Range of motion improved."))


def note_run(tmp_path, text=NOTE, **script):
    conn = DB.connect(str(tmp_path / "n.sqlite"))
    cid = DB.create_case(conn, text, now=0.0)
    sc = {**NOTE_SCRIPT, **script}
    return conn, cid, PL.run_pipeline(conn, cid, text, call=FakeCall(sc), now=lambda: 1.0)


def test_a_clean_first_run_of_a_plain_note_stays_ready(tmp_path):
    conn, cid, out = note_run(tmp_path)
    assert out["counts"]["entries"] == 2 and out["flags"] == []
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)


@pytest.mark.parametrize("miss", [False, True], ids=["down", "fixture_miss"])
def test_flag_step_down_on_a_note_with_no_phrase_list_hit_still_fails_the_case(tmp_path, miss):
    conn, cid, out = note_run(tmp_path, flags=PL.AU.LLMFailedFixtureMiss("x") if miss else down("flags"))
    assert out["flags"] == []                                      # nothing was made, so no row can carry the failure
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial" and out["error"] == err
    assert "(finding the flags)" in err["message"] and err["message"].endswith(TAIL)
    assert "RUN_FAILED" in blockers(conn, cid)


def test_flag_step_down_on_a_plain_note_rerun_names_the_step_too(tmp_path):
    conn, cid, _ = note_run(tmp_path)
    out = PL.run_pipeline(conn, cid, NOTE, call=FakeCall({**NOTE_SCRIPT, "flags": down("flags")}), now=lambda: 2.0)
    status, err = case_error(conn, cid)
    assert status == "failed" and "(finding the flags)" in err["message"] and out["error"] == err and "RUN_FAILED" in blockers(conn, cid)


def test_a_good_second_run_clears_a_flag_failure_on_a_plain_note(tmp_path):
    conn, cid, _ = note_run(tmp_path, flags=down("flags"))
    assert case_error(conn, cid)[0] == "failed"
    PL.run_pipeline(conn, cid, NOTE, call=FakeCall(NOTE_SCRIPT), now=lambda: 2.0)
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)


def test_j2_down_on_a_note_with_no_amounts_has_nothing_to_judge_and_stays_ready(tmp_path):      # documented: no amount, no judge-2 call, nothing failed
    conn, cid, out = note_run(tmp_path, j2=down("j2"))
    assert case_error(conn, cid) == ("ready", None)


def test_first_run_with_extract_down_and_no_entries_fails_and_names_the_step(tmp_path):
    conn, cid, out = first_run(tmp_path, extract=down("extract"))
    assert out["status"] == "done_with_errors" and out["counts"]["entries"] == 0
    status, err = case_error(conn, cid)
    assert status == "failed" and out["error"] == err
    assert err == {"code": "run_partial", "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep." + TAIL}
    assert "RUN_FAILED" in blockers(conn, cid)


def test_first_run_with_extract_down_for_some_records_keeps_its_old_shape(tmp_path):
    good = sample_script()["extract"]

    def extract(user):
        if which_record(user)[0] == 1:
            raise down("extract")
        return good(user)
    conn, cid, out = first_run(tmp_path, extract=extract)
    assert out["status"] == "done_with_errors" and out["counts"]["entries"] > 0
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)


def test_a_good_second_run_clears_a_failed_first_run(tmp_path):
    conn, cid, _ = first_run(tmp_path, j1=down("j1"))
    assert case_error(conn, cid)[0] == "failed"
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: 3.0)
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:30:48.370Z

**tool call — Bash**
````
{
 "command": "sed -n 100,200p app/backend/flags.py; grep -n \"flags\" tests/unit/_fakes.py | head -20"
}
````

### User / tool · 2026-11-02T15:30:48.453Z

**tool result**
````
        f = _flag(record, h["flag_type"], h["category"], text[a:b], "lexicon", (a, b), False, "lexicon_only")
        f["lexicon_ids"] = [h["id"]]
        f["_span"] = (a, b)
        seen[key] = f
        out.append(f)
    return out


# ------------------------------------------------------------------ merge
def _overlap(a, b) -> bool:
    return bool(a and b and a[0] < b[1] and b[0] < a[1])


def _note_merged(f: dict, lf: dict) -> None:
    """Other categories the model proposed for the same quote (collapsed into this flag) go in the audit trail: ladder.code_checks.merged_categories."""
    extra = sorted(c for c in lf.get("_merged", []) if c and c != f["category"])
    if extra:
        f["ladder"] = dict(f["ladder"], code_checks=dict(f["ladder"].get("code_checks") or {}, merged_categories=extra))


def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False, *, llm_failed: bool = False, fixture_miss: bool = False) -> list:
    """Combine model flags and lexicon flags. Same type with overlapping spans -> origin 'both'; one side only -> LEXICON_ONLY / LLM_ONLY
    (needs_review). Grounding of model quotes is checked separately (ground()); a tagged record adds INJECTION_SUSPECTED to every flag."""
    body, out, used = record["excerpt"], [], set()
    uniq, seen, filtered, fseen = [], {}, [], set()
    for lf in llm_flags:
        if lf.get("category") in _CONTEXT_ONLY:       # D-032 + D-057: never a flag, but listed (collapsed, counted) rather than dropped
            k = (lf["type"], lf["category"], grounding.normalize(lf["excerpt"]))
            if k not in fseen:
                fseen.add(k)
                filtered.append(lf)
            continue
        k = (lf["type"], grounding.normalize(lf["excerpt"]))
        if k not in seen:
            seen[k] = lf
            uniq.append(lf)
        elif lf.get("category") != seen[k].get("category") and lf.get("category") not in seen[k].setdefault("_merged", []):
            seen[k]["_merged"].append(lf.get("category"))       # T-126 r2 / D-053: a second category on the same quote is not silently lost; the kept flag's code_checks names it
    # R-CO-7: the model's flag order must not decide ids or which model flag a lexicon flag pairs with. Sort by position in the record,
    # then type, category and text (code decides what code can decide).
    uniq.sort(key=lambda lf: ((grounding.locate(body, lf["excerpt"]) or (10 ** 9, 0))[0], lf["type"], lf["category"], grounding.normalize(lf["excerpt"])))
    llm_spans = [grounding.locate(body, lf["excerpt"]) for lf in uniq]
    for lx in lex_flags:
        lx = dict(lx)
        lx["_stage"] = dict(lx["_stage"], injection=tagged)
        match = next((i for i, lf in enumerate(uniq) if i not in used and lf["type"] == lx["type"] and _overlap(llm_spans[i], lx.get("_span"))), None)
        if match is not None:
            used.add(match)
            lx["origin"], lx["_stage"]["agreement"], lx["_stage"]["judge"] = "both", "both", "unavailable"
            lx["ladder"] = dict(lx["ladder"], judge=None)
            _note_merged(lx, uniq[match])
            # D-030: evidence is the verbatim phrase span the model returned (still grounded by ground()); the lexicon sentence is
            # only the fallback quote for phrase-list-only flags. A credibility flag is the exception (D-043, T-092): its excerpt is the whole
            # period sentence, so a model clause never replaces it (the positive half of a mixed sentence must stay in the quote).
            if lx["category"] != CREDIBILITY_CATEGORY:
                lx["excerpt"] = uniq[match]["excerpt"]
                sp = llm_spans[match]
                base = _base(record)
                lx["evidence"] = [{"record_no": record["n"], "text": lx["excerpt"],
                                   "start": base + sp[0] if sp else None, "end": base + sp[1] if sp else None}]
                lx["_span"] = sp or lx.get("_span")
            _render(lx, record)
        else:
            lx["origin"], lx["_stage"]["agreement"] = "lexicon", "lexicon_only"
            lx["_stage"]["llm_failed"], lx["_stage"]["fixture_miss"] = llm_failed, fixture_miss
            if llm_failed or fixture_miss:
                lx["_stage"]["agreement"] = None
        out.append(_compose(lx))
    for i, lf in enumerate(uniq):
        if i in used:
            continue
        f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", llm_spans[i], tagged, "llm_only")
        _note_merged(f, lf)
        if lf.get("category") in _NEEDS_LEXICON:
            f["_tray"] = "LLM_ONLY"      # D-032 + D-053: a scene_facts flag needs a phrase-list hit; the model's alone is shown in the tray, never dropped
        out.append(f)
    for lf in filtered:
        f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", grounding.locate(body, lf["excerpt"]), tagged, "llm_only")
        f["_tray"] = FILTERED
        f["_last"] = True       # after every other tray item, so no recorded judge prompt (it carries the flag id) changes
        out.append(f)
    for f in out:
        f["_stage"]["injection"] = tagged
        _compose(f)
    return out


def _model_conflicts(proposed: list, record: dict, tagged: bool) -> list:
    """A conflict the model proposed in the per-record pass (T-113, D-053; T-109 r2): only a code candidate (run_conflict_pass) can be a conflict flag, so the
    model's is a could-not-verify tray item (LLM_ONLY) with its own quotes and the fixed template title. It is not judged and never reaches the letter."""
    out, seen = [], set()
    for lf in proposed:
        k = (grounding.normalize(lf["excerpt"]), grounding.normalize(lf.get("excerpt_b") or ""), lf["category"])
        if k in seen:
            continue
        seen.add(k)
        f = _flag(record, "conflict", lf["category"], lf["excerpt"], "llm", grounding.locate(record["excerpt"], lf["excerpt"]), tagged, "llm_only")
        if lf.get("excerpt_b"):
            f["excerpt_b"] = lf["excerpt_b"]
            sb = grounding.locate(record["excerpt"], lf["excerpt_b"])
            f["evidence"].append({"record_no": record["n"], "text": lf["excerpt_b"],
43:    """Happy-path script for the sample case (extract returns the golden summary and quote; judges agree; no LLM flags). `over` replaces steps."""
50:          "conflicts": {"flags": []}, "flags": {"flags": []}}
56:    entries, amounts, flags, tray (rejected attempts), errors [{code, ...}], status, warnings."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:30:53.324Z

**tool call — Bash**
````
{
 "command": "grep -n \"def run_flag_pass\" -A40 app/backend/flags.py | head -70"
}
````

### User / tool · 2026-11-02T15:30:53.408Z

**tool result**
````
242:def run_flag_pass(record: dict, *, call, tagged: bool = False, accident_year=None, case_text: str = "") -> list:
243-    """One model call for this record only, merged with the lexicon floor. A failed or missed model call leaves the lexicon flags in place."""
244-    item = f"f_r{record['n']}"
245-    n = promptlib.nonce(case_text, "flags", item)
246-    prompt = promptlib.load("flags_v1")
247-    user = f"{injection.wrap(record['excerpt'], n)}\nReturn the JSON object."
248-    llm, conflicts, failed, miss = [], [], False, False
249-    try:
250-        out, _cid = call("flags", prompt.text, user, schemas.FlagPass.model_json_schema(), item_id=item)
251-        try:
252-            proposed = [f.model_dump() for f in schemas.FlagPass.model_validate(out).flags]
253-            llm = [f for f in proposed if f["type"] in _PER_RECORD_TYPES]
254-            conflicts = [f for f in proposed if f["type"] == "conflict"]
255-        except (ValidationError, TypeError, ValueError):
256-            failed = True
257-    except P.FixtureMiss:
258-        miss = True
259-    except AU.LLMFailed:
260-        failed = True
261-    flags = merge(llm, lexicon_flags(record, accident_year), record, tagged, llm_failed=failed, fixture_miss=miss)
262-    # tray items go LAST: a flag's id (f_r<n>_<k>) is its position in this list and is part of the judge's prompt, so inserting an item that used to be
263-    # dropped must not renumber the flags after it (recorded judge answers are keyed on that prompt)
264-    last = [f for f in flags if f.pop("_last", False)]
265-    flags = [f for f in flags if "_tray" not in f] + [f for f in flags if "_tray" in f and f not in last] + _model_conflicts(conflicts, record, tagged) + last
266-    ground(flags, record)
267-    for f in flags:
268-        code = f.pop("_tray", None)
269-        if code:
270-            _to_tray(f, code)       # after ground(), which recomposes the state; a rung-1 failure keeps its own reason after the tray code
271-    if tagged:
272-        flags.append(_record_warning(record))
273-    return flags
274-
275-
276-# ------------------------------------------------------------------ cross-record conflict pass
277-def _candidate_flag(c: dict, by_n: dict, any_tagged: bool, fid: str) -> dict:
278-    """A conflict flag built from a code candidate: both quotes are whole sentences cut from the record text, so rung 1 holds by construction
279-    (it is still checked, not assumed). Title and explanation come from the code template."""
280-    ra, rb = by_n[c["a"].record_no], by_n[c["b"].record_no]
281-    qa, qb = c["a"].text, c["b"].text
282-    sa, sb = grounding.locate(ra["excerpt"], qa), grounding.locate(rb["excerpt"], qb)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:31:04.842Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/probes161; cat > $S/probes161/test_probe161.py <<'EOF'\nimport pytest\nfrom app.backend import pipeline as PL, trace\nfrom app.db import db as DB\nfrom tests.unit._fakes import FakeCall, sample_script\nfrom tests.unit.test_t161_first_run_stage_down import NOTE, NOTE_SCRIPT, case_error, blockers, down, note_run, first_run\n\n\n@pytest.mark.parametrize(\"bad\", [{\"flags\": \"not a list\"}, {\"flags\": [{\"type\": 5}]}, None, {}], ids=[\"str\", \"badrow\", \"none\", \"empty\"])\ndef test_flags_schema_invalid_plain_note(tmp_path, bad):\n    conn, cid, out = note_run(tmp_path, flags=bad)\n    print(\"SCHEMA_INVALID\", repr(bad), case_error(conn, cid), blockers(conn, cid))\n\n\ndef test_flags_down_sample_still_failed(tmp_path):\n    conn, cid, out = first_run(tmp_path, flags=down(\"flags\"))\n    print(\"SAMPLE_FLAGS_DOWN\", case_error(conn, cid))\n\n\ndef test_plain_note_flags_down_export(tmp_path):\n    conn, cid, out = note_run(tmp_path, flags=down(\"flags\"))\n    print(\"PLAIN_FLAGS_DOWN\", case_error(conn, cid), blockers(conn, cid))\n\n\ndef test_extract_down_partial_most(tmp_path):\n    from tests.unit.test_t161_first_run_stage_down import which_record\n    good = sample_script()[\"extract\"]\n    def extract(user):\n        if which_record(user)[0] != 1:\n            raise down(\"extract\")\n        return good(user)\n    conn, cid, out = first_run(tmp_path, extract=extract)\n    print(\"EXTRACT_8_OF_9_DOWN\", out[\"status\"], out[\"counts\"][\"entries\"], case_error(conn, cid))\nEOF\ncd $S/r2a && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest $S/probes161/test_probe161.py -p no:cacheprovider -q -s 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T15:31:06.825Z

**tool result**
````
SCHEMA_INVALID {'flags': 'not a list'} ('ready', None) ['NOTHING_ACCEPTED']
.SCHEMA_INVALID {'flags': [{'type': 5}]} ('ready', None) ['NOTHING_ACCEPTED']
.SCHEMA_INVALID None ('ready', None) ['NOTHING_ACCEPTED']
.SCHEMA_INVALID {} ('ready', None) ['NOTHING_ACCEPTED']
.SAMPLE_FLAGS_DOWN ('failed', {'code': 'run_partial', 'message': 'The AI step failed for 7 items (finding the flags) on this run, and there is no earlier result to keep. Run it again to retry.'})
.PLAIN_FLAGS_DOWN ('failed', {'code': 'run_partial', 'message': 'The AI step (finding the flags) failed on this run, so nothing from it could be used. Run it again to retry.'}) ['RUN_FAILED', 'NOTHING_ACCEPTED']
.EXTRACT_8_OF_9_DOWN done_with_errors 1 ('ready', None)
.
7 passed in 1.63s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:31:11.015Z

**tool call — Bash**
````
{
 "command": "grep -n \"def make_call\" -B2 -A60 app/backend/ai_util.py 2>/dev/null | head -100; ls app/backend | head -40; grep -rn \"AU\\b\" app/backend/pipeline.py | head -3"
}
````

### User / tool · 2026-11-02T15:31:11.178Z

**tool result**
````
__init__.py
__pycache__
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
case_list.py
charge_text.py
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
money.py
narrative.py
overlap.py
pdf_checks.py
pdf_hidden.py
pdf_ocr.py
pdf_routes.py
pdf_text.py
pipeline.py
present.py
app/backend/pipeline.py:17:from app.llm import audited as AU, provider as P
app/backend/pipeline.py:452:        except (AU.LLMFailed, P.FixtureMiss):
app/backend/pipeline.py:461:    call = _noting(call or AU.make_call(conn, cid, now=clock), failed_steps := [])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:31:12.451Z

**tool call — Bash**
````
{
 "command": "grep -n \"validate\\|jsonschema\\|SCHEMA\\|raise LLMFailed\\|def audited_call\\|def make_call\\|class LLMFailed\" app/llm/audited.py | head -30"
}
````

### User / tool · 2026-11-02T15:31:12.545Z

**tool result**
````
19:# (timeout, connection). Output that fails the caller's `validate` (ValueError) is retried too, but only from the validate step. Anything else
32:class LLMFailed(Exception):
34:    (TIMEOUT, SCHEMA_INVALID, FIXTURE_MISS ...), so a caller can record why without keeping any record text."""
44:class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
54:    """Our own codes only (SCHEMA_INVALID, TIMEOUT, BACKEND_FAILED ...); anything else is reduced to the exception class."""
70:def audited_call(conn, case_id: str, step: str, model: str, system: str, user: str, json_schema: dict, *,
71:                 complete_with_meta=None, validate=None, item_id=None, now=None, prompt_version=None, sleep=None):
81:            if validate is not None:
83:                    validate(res.output)
112:            raise LLMFailedFixtureMiss(h)
115:    raise LLMFailed(f"{step}: {MAX_ATTEMPTS} attempts failed", last_error=(last_err or "LLM_ERROR").split()[0])
128:def make_call(conn, case_id: str, *, now=None, models: dict = None, schemas: dict = None):
133:    def call(step, system, user, schema, *, item_id=None, validate=None):
135:        return audited_call(conn, case_id, step, m[role_for(step)], system, user, schema, item_id=item_id, now=now, validate=validate,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:31:24.083Z

**tool call — Bash**
````
{
 "command": "sed -n 70,126p app/llm/audited.py; grep -n \"json-schema\\|json_schema\\|structured\" app/llm/provider.py | head"
}
````

### User / tool · 2026-11-02T15:31:24.232Z

**tool result**
````
def audited_call(conn, case_id: str, step: str, model: str, system: str, user: str, json_schema: dict, *,
                 complete_with_meta=None, validate=None, item_id=None, now=None, prompt_version=None, sleep=None):
    cwm = complete_with_meta or P.complete_with_meta
    last_err = "unknown"
    for attempt in range(1, MAX_ATTEMPTS + 1):
        u = user + _RETRY_NOTES[attempt - 1]
        h = P.prompt_hash(model, system, u, json_schema)
        t0 = time.monotonic()
        res, err, fixture_miss, bug = None, None, False, None
        try:
            res = cwm(model, system, u, json_schema)
            if validate is not None:
                try:
                    validate(res.output)
                except RETRYABLE_VALIDATION_ERRORS as e:
                    err = _error_code(e)               # schema-invalid output: a failed attempt, retried with a stricter note
        except P.FixtureMissing as e:
            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
        except RETRYABLE_PROVIDER_ERRORS as e:          # only our own error codes are stored, never model- or record-derived text
            err = _error_code(e)
        except Exception as e:                         # a bug in our code: keep the row (class name only), then let it propagate below
            err, bug = _error_code(e), e
        ms = int((time.monotonic() - t0) * 1000)
        fields = dict(role=role_for(step), step=step, backend=(res.backend if res else P.backend_name()), model=(res.model_resolved if res and res.model_resolved else model),
                      prompt_version=prompt_version, prompt_sha256=h, attempt=attempt, latency_ms=(res.latency_ms if res and res.latency_ms else ms),
                      parsed_ok=1 if err is None else 0, error=err)
        if item_id:
            fields["item_id"] = item_id
        if res:
            import json as _j
            fields.update(cost_usd=res.cost_usd, tokens_in=res.tokens_in, tokens_out=res.tokens_out,
                          recorded_from_json=_j.dumps(res.recorded_from) if res.recorded_from else None)
        with _DB_LOCK:
            call_id = DB.add_llm_call(conn, case_id, u, (res.raw or _dump(res.output)) if res else None, now=_t(now), system=system, **fields)
        if err is None:
            return res.output, call_id
        if bug is not None:
            log.error("llm call raised a programmer error call_id=%s step=%s class=%s", call_id, step, type(bug).__name__)
            raise bug
        last_err = err
        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
        if fixture_miss:
            raise LLMFailedFixtureMiss(h)
        if sleep is not None and attempt < MAX_ATTEMPTS:
            sleep(RETRY_DELAYS_S[attempt - 1])         # short, capped, code-controlled
    raise LLMFailed(f"{step}: {MAX_ATTEMPTS} attempts failed", last_error=(last_err or "LLM_ERROR").split()[0])


def _dump(o):
    import json
    return json.dumps(o, sort_keys=True)


PROMPT_OF_STEP = {"extract": "extract_v1", "j1": "judge_faithfulness_v1", "j2": "judge_amount_class_v1", "j3": "judge_conflict_v6",
                  "j4": "judge_flag_v3", "flags": "flags_v1", "split": "split_v1", "narrative": "narrative_v1"}
PROMPT_OF_STEP.update({"extract_es": "extract_es_v1", "judge_faithfulness_es": "judge_faithfulness_es_v1"})     # Spanish records (D-042, T-085)

1:"""Provider interface (ADR-004, R-CO-2/6): complete(model, system, user, json_schema) -> dict over three backends.
33:def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
35:    blob = json.dumps([model, system, user, json_schema], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
92:def complete_with_meta(model: str, system: str, user: str, json_schema: dict) -> LLMResult:
94:    key = prompt_hash(model, system, user, json_schema)
96:        res = _fixture.call(model, system, user, json_schema, key=key)
104:        res = be.call(model, system, user, json_schema, key=key)
107:    validate_schema(res.output, json_schema)
113:def complete(model: str, system: str, user: str, json_schema: dict) -> dict:
114:    return complete_with_meta(model, system, user, json_schema).output
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:31:30.868Z

**tool call — Bash**
````
{
 "command": "grep -n \"class FlagPass\" -B30 -A8 app/llm/schemas.py | grep -n \"validator\\|class \\|Field\\|Literal\" | head -30; sed -n 100,112p app/llm/provider.py"
}
````

### User / tool · 2026-11-02T15:31:30.966Z

**tool result**
````
ugrep: warning: app/llm/schemas.py: No such file or directory
        if name == "claude-cli":
            from app.llm.backends import claude_cli as be
        else:
            from app.llm.backends import anthropic_api as be
        res = be.call(model, system, user, json_schema, key=key)
    else:
        raise LLMError(f"UNKNOWN_BACKEND {name}")
    validate_schema(res.output, json_schema)
    if name != "fixture" and _recording():
        _fixture.write(key, res, model)
    return res
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:31:34.069Z

**tool call — Bash**
````
{
 "command": "grep -rn \"class FlagPass\" app | head; "
}
````

### User / tool · 2026-11-02T15:31:34.157Z

**tool result**
````
app/backend/schemas.py:79:class FlagPass(_Closed):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:31:36.340Z

**tool call — Bash**
````
{
 "command": "sed -n 1,30p app/backend/schemas.py; sed -n 55,100p app/backend/schemas.py; tail -c 200 /private/tmp/claude-501/*/*/scratchpad/unit_r2a.txt"
}
````

### User / tool · 2026-11-02T15:31:36.481Z

**tool result**
````
"""Pydantic models for LLM outputs (closed schemas; extra fields rejected). R-TL-9, ADR-004, ADR-013, ADR-016.
The generator returns {summary, excerpt} only: no provider, date, amount or clinical-facts field (code supplies those).
Flag/conflict outputs carry a type, a category and quoted text only: no free prose (D-007)."""
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class _Closed(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ExtractOutput(_Closed):
    summary: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)


_J1_CODES = Literal["NONE", "ADDS_DIAGNOSIS", "ADDS_SEVERITY", "ADDS_CAUSATION", "DROPS_QUALIFIER", "NUMBER_MISMATCH", "OTHER_UNSUPPORTED"]
_J2_CODES = Literal["NONE", "SHOULD_BE_CHARGE", "SHOULD_BE_RATE", "SHOULD_BE_ESTIMATE", "SHOULD_BE_DAMAGES", "SHOULD_BE_UNCLEAR", "TEXT_AMBIGUOUS"]
_J3_CODES = Literal["NONE", "PLAN_VS_ACTUAL", "FACT_MISMATCH", "DIFFERENT_VISITS", "CAN_BOTH_BE_TRUE", "TEXT_AMBIGUOUS"]
_J4_CODES = Literal["NONE", "WRONG_TYPE", "WRONG_CATEGORY", "NEGATED", "NOT_SUPPORTED_BY_QUOTE", "TEXT_AMBIGUOUS"]
JUDGE_REASON_CODES = {"j1": _J1_CODES, "j2": _J2_CODES, "j3": _J3_CODES, "j4": _J4_CODES}


class _Judge(BaseModel):
    """D-028: a verdict enum plus a reason_code from a closed list; no free-text reason. Unknown keys (an old-style `reason`) are ignored
    and never stored; the schema handed to the provider is closed and requires verdict + reason_code."""
    model_config = ConfigDict(extra="ignore", json_schema_extra={"additionalProperties": False, "required": ["verdict", "reason_code"]})


    excerpt: str
    excerpt_b: Optional[str] = None


class SplitSpan(_Closed):
    start: int = Field(ge=0)
    end: int = Field(ge=0)


class SplitOutput(_Closed):
    """LLM split fallback (D-031): character offsets only. Code validates them (ingest.validate_split)."""
    records: List[SplitSpan] = Field(min_length=1)


class NarrativeSentence(_Closed):
    entry_id: str = Field(min_length=1)
    text: str = Field(min_length=1, max_length=600)


class NarrativeOutput(_Closed):
    """Firm-voice treatment paragraph (D-031): sentences, each citing one accepted entry. Code and judge 1 check every sentence."""
    sentences: List[NarrativeSentence] = Field(min_length=1, max_length=60)


class FlagPass(_Closed):
    flags: List[FlagOutput]


def json_schema(model) -> dict:
    return model.model_json_schema()
................ [ 38%]
........................................................................ [ 39%]
........................................................................ [ 41%]
................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:31:47.726Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && mkdir -p $S/r2b && git archive HEAD | tar -x -C $S/r2b && ln -sfn /Users/arsis/zlayt-pm-project/.venv $S/r2b/.venv; cd $S/r2b; ls tests/unit | grep -i \"t146\\|t161\\|partial\\|rerun\\|first_run\" ; sed -n 583,592p app/backend/pipeline.py; grep -n \"dated\\b\\|undated\\b\" app/backend/pipeline.py | head"
}
````

### User / tool · 2026-11-02T15:31:48.494Z

**tool result**
````
test_t146_r2_failed_rerun_keeps_items.py
test_t146_r3_decided_items_never_lowered.py
test_t146_r4_ladder_compare_and_conflicts.py
test_t146_rerun_keeps_items.py
test_t161_first_run_stage_down.py
        err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    else:
        status = "done_with_errors" if errors else "done"
        # T-161: a first run with a judge or the flag step down fails like a re-run. The flag step is read from the steps that were down (a note with no phrase-list hit has no flag row to carry the failure).
        # A first run's extract failures stay tray items while some entries came out; with no entry at all there is nothing to review, so it is failed and the step is named.
        named = {c for _, c, _ in kept} | set(empty)
        down = ("finding the flags",) if "flags" in failed_steps and "finding the flags" not in named else ()
        err = _partial_error(kept, empty if (rerun or not (dated or undated)) else [s for s in empty if s != _EXTRACT_STEP], down)
    DB.update_case(conn, cid, status="failed" if (timed_out or err) else "ready", stage="finalize", error=json.dumps(err) if err else None,
                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
51:    fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
418:    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso"))      # D-055: a year hint from every dated record; the ingest kind is a label guess and is not read
561:    dated = sorted((e for e in entries if dated_cut(e)), key=lambda e: (e["date"], e["seq"]))
562:    undated = [e for e in entries if not dated_cut(e)]
569:    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
572:    kept_e, empty_e = _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out)
590:        err = _partial_error(kept, empty if (rerun or not (dated or undated)) else [s for s in empty if s != _EXTRACT_STEP], down)
594:    all_items = dated + undated + final_amounts + flag_items
595:    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
598:            "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:31:59.786Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $S/mut161.py <<'EOF'\nimport subprocess, sys, shutil\nroot = sys.argv[1]\nf = root + \"/app/backend/pipeline.py\"\nsrc = open(f).read()\nmuts = {\n \"M1 down always ()\": ('down = (\"finding the flags\",) if \"flags\" in failed_steps and \"finding the flags\" not in named else ()', 'down = ()'),\n \"M2 flags never in failed_steps\": ('if \"flags\" in failed_steps and \"finding', 'if False and \"finding'),\n \"M3 drop named dedupe\": ('and \"finding the flags\" not in named else ()', 'else ()'),\n \"M4 extract filter always (old)\": ('empty if (rerun or not (dated or undated)) else', 'empty if rerun else'),\n \"M5 extract never filtered\": ('empty if (rerun or not (dated or undated)) else [s for s in empty if s != _EXTRACT_STEP]', 'empty'),\n \"M6 only dated\": ('not (dated or undated)', 'not dated'),\n \"M7 _partial_error ignores down\": ('    if down:\\n        parts.append', '    if False:\\n        parts.append'),\n \"M8 down wording drops step name\": (\"({' and '.join(sorted(down))}) failed on this run\", \"failed on this run\"),\n \"M9 down only first run\": ('\"flags\" in failed_steps and', '\"flags\" in failed_steps and not rerun and'),\n}\ntests = [\"tests/unit/test_t161_first_run_stage_down.py\",\"tests/unit/test_t146_r2_failed_rerun_keeps_items.py\",\"tests/unit/test_t146_r3_decided_items_never_lowered.py\",\"tests/unit/test_t146_rerun_keeps_items.py\",\"tests/unit/test_t146_r4_ladder_compare_and_conflicts.py\"]\nfor name,(a,b) in muts.items():\n    if a not in src: print(name, \"PATTERN MISSING\"); continue\n    open(f,\"w\").write(src.replace(a,b,1))\n    r = subprocess.run([root+\"/.venv/bin/python\",\"-m\",\"pytest\",\"-q\",\"-x\",\"-p\",\"no:cacheprovider\"]+tests,cwd=root,capture_output=True,text=True)\n    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]\n    print(name, \"->\", \"KILLED\" if r.returncode else \"SURVIVED\", \"|\", tail)\nopen(f,\"w\").write(src)\nEOF\ncd $S/r2b && /Users/arsis/zlayt-pm-project/.venv/bin/python $S/mut161.py $S/r2b 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T15:32:26.058Z

**tool result**
````
M1 down always () -> KILLED | 1 failed, 12 passed in 1.43s
M2 flags never in failed_steps -> KILLED | 1 failed, 12 passed in 1.38s
M3 drop named dedupe -> KILLED | 1 failed, 36 passed in 3.36s
M4 extract filter always (old) -> KILLED | 1 failed, 17 passed in 1.58s
M5 extract never filtered -> KILLED | 1 failed, 18 passed in 1.61s
M6 only dated -> SURVIVED | 134 passed in 10.20s
M7 _partial_error ignores down -> KILLED | 1 failed, 12 passed in 1.38s
M8 down wording drops step name -> KILLED | 1 failed, 12 passed in 1.48s
M9 down only first run -> KILLED | 1 failed, 14 passed in 1.51s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:32:35.265Z

**tool call — Bash**
````
{
 "command": "grep -n \"def make_env\" -A30 tests/unit/test_amounts_d059_api.py | head -50; tail -c 150 /private/tmp/claude-501/*/*/scratchpad/unit_r2a.txt"
}
````

### User / tool · 2026-11-02T15:32:35.355Z

**tool result**
````
18:def make_env(tmp_path, monkeypatch, text):
19-    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
20-    monkeypatch.setenv("ENABLE_LIVE", "1")                     # leaves demo mode; the fake call factory means no model is ever started
21-    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
22-    judged = []
23-
24-    def factory(conn, cid):
25-        def call(step, system, user, schema, *, item_id=None, validate=None):
26-            judged.append(step)
27-            v = SCRIPT[step](user) if callable(SCRIPT[step]) else SCRIPT[step]
28-            return v, None
29-        return call
30-    c = TestClient(create_app(str(tmp_path / "d059.sqlite"), call_factory=factory, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
31-    tok = c.post("/api/cases", json={"text": text}).json()["token"]
32-    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
33-    for _ in range(200):
34-        s = c.get(f"/api/cases/{tok}/status").json()
35-        if s["status"] in ("ready", "failed"):
36-            break
37-        time.sleep(0.1)
38-    assert s["status"] == "ready", s
39-    return c, tok, judged
40-
41-
42-@pytest.fixture
43-def env(tmp_path, monkeypatch):
44-    return make_env(tmp_path, monkeypatch, LEDGER)
45-
46-
47-def charges(c, tok):
48-    return [a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["kind"] == "charge"]
................................. [ 63%]
........................................................................ [ 64%]
...........................ss
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:32:38.829Z

Now an API-level run of the plain note with the flag step down.

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:32:44.661Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $S/probes161/test_api161.py <<'EOF'\nimport time\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom app.backend import pipeline as PL\nfrom tests.unit._fakes import FakeCall\nfrom tests.unit.test_t161_first_run_stage_down import NOTE, NOTE_SCRIPT, down\n\n\ndef run(tmp_path, monkeypatch, script):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"claude-cli\"); monkeypatch.setenv(\"ENABLE_LIVE\", \"1\"); monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    fc = FakeCall(script)\n    c = TestClient(create_app(str(tmp_path / \"a.sqlite\"), call_factory=lambda conn, cid: fc, static_dir=str(tmp_path)), client=(\"127.0.0.1\", 50000))\n    tok = c.post(\"/api/cases\", json={\"text\": NOTE}).json()[\"token\"]\n    assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\n    for _ in range(200):\n        s = c.get(f\"/api/cases/{tok}/status\").json()\n        if s[\"status\"] in (\"ready\", \"failed\"): break\n        time.sleep(0.1)\n    return c, tok, s\n\n\ndef test_api(tmp_path, monkeypatch):\n    c, tok, s = run(tmp_path, monkeypatch, {**NOTE_SCRIPT, \"flags\": down(\"flags\")})\n    print(\"API status\", s[\"status\"], s.get(\"error\"))\n    for e in c.get(f\"/api/cases/{tok}\").json()[\"entries\"]:\n        c.post(f\"/api/cases/{tok}/items/{e['id']}/review\", json={\"action\": \"accept\"})\n    r = c.get(f\"/api/cases/{tok}/export\")\n    print(\"API export\", r.status_code, r.text[:300])\nEOF\ncd $S/r2a && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest $S/probes161/test_api161.py -p no:cacheprovider -q -s 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T15:32:45.927Z

**tool result**
````
API status failed {'code': 'run_partial', 'message': 'The AI step (finding the flags) failed on this run, so nothing from it could be used. Run it again to retry.'}
API export 422 {"error":{"code":"export_blocked","message":"The last run stopped before it finished; the items that finished are kept. The export is blocked.","detail":{"blockers":[{"item_id":null,"kind":"case","reason_code":"RUN_FAILED","why":"The last run stopped before it finished; the items that finished are k
.
1 passed in 0.93s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:32:56.990Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $S/mut159.py <<'EOF'\nimport subprocess, sys\nroot = sys.argv[1]\nf = root + \"/app/backend/review.py\"\nsrc = open(f).read()\nmuts = {\n \"A ASC order\": (\"ORDER BY at DESC, rowid DESC LIMIT 1\", \"ORDER BY at ASC, rowid ASC LIMIT 1\"),\n \"B drop confirmed_at clause\": (' and bool(f.get(\"confirmed_at\"))', ''),\n \"C no txn (BEGIN/COMMIT/ROLLBACK as no-ops)\": ('        conn.execute(\"BEGIN\")\\n        try:\\n            DB.update_item(conn, item_id, now=t, case=case_id, ladder={**item[\"ladder\"], \"confirm\"', '        if True:\\n            DB.update_item(conn, item_id, now=t, case=case_id, ladder={**item[\"ladder\"], \"confirm\"'),\n \"D no rollback on failure\": ('        except Exception:\\n            conn.execute(\"ROLLBACK\")\\n            raise\\n\\n\\ndef set_review', '        except Exception:\\n            conn.execute(\"COMMIT\")\\n            raise\\n\\n\\ndef set_review'),\n \"E no compensation\": ('            if back:\\n                DB.apply_review(conn, item_id, back', '            if False:\\n                DB.apply_review(conn, item_id, back'),\n \"F compensation always reset\": ('{\"pending\": \"reset\", \"dismissed\": \"dismiss\"}.get(item.get(\"review_status\"))', '\"reset\"'),\n \"G swallow the failure\": ('                DB.apply_review(conn, item_id, back, now=now, case=case_id)\\n            raise', '                DB.apply_review(conn, item_id, back, now=now, case=case_id)\\n            return item'),\n}\ntests = [\"tests/unit/test_t159_flag_audit.py\",\"tests/unit/test_amounts_d059_api.py\"]\nfor name,(a,b) in muts.items():\n    if a not in src: print(name, \"PATTERN MISSING\"); continue\n    open(f,\"w\").write(src.replace(a,b,1))\n    r = subprocess.run([root+\"/.venv/bin/python\",\"-m\",\"pytest\",\"-q\",\"-p\",\"no:cacheprovider\"]+tests,cwd=root,capture_output=True,text=True)\n    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]\n    print(name, \"->\", \"KILLED\" if r.returncode else \"SURVIVED\", \"|\", tail)\nopen(f,\"w\").write(src)\nEOF\ncd $S/r2b && /Users/arsis/zlayt-pm-project/.venv/bin/python $S/mut159.py $S/r2b 2>&1 | tail -12"
}
````

### User / tool · 2026-11-02T15:33:55.585Z

**tool result**
````
A ASC order -> KILLED | 2 failed, 25 passed in 8.21s
B drop confirmed_at clause -> KILLED | 1 failed, 26 passed in 7.92s
C no txn (BEGIN/COMMIT/ROLLBACK as no-ops) -> KILLED | 2 errors in 0.50s
D no rollback on failure -> KILLED | 1 failed, 26 passed in 9.13s
E no compensation -> KILLED | 1 failed, 26 passed in 9.10s
F compensation always reset -> SURVIVED | 27 passed in 9.61s
G swallow the failure -> KILLED | 1 failed, 26 passed in 11.50s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:34:02.388Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/r2b && python3 - <<'EOF'\nimport subprocess,os\nroot=os.getcwd(); f=root+\"/app/backend/review.py\"; src=open(f).read()\ni=src.index(\"def _record_confirm\"); j=src.index(\"def set_review\")\nblk=src[i:j]\nm=blk.replace('conn.execute(\"BEGIN\")','pass').replace('conn.execute(\"COMMIT\")','pass').replace('conn.execute(\"ROLLBACK\")','pass')\nopen(f,\"w\").write(src[:i]+m+src[j:])\nr=subprocess.run([root+\"/.venv/bin/python\",\"-m\",\"pytest\",\"-q\",\"-p\",\"no:cacheprovider\",\"tests/unit/test_t159_flag_audit.py\",\"tests/unit/test_amounts_d059_api.py\"],cwd=root,capture_output=True,text=True)\nprint(\"C real no-txn:\", \"KILLED\" if r.returncode else \"SURVIVED\", r.stdout.strip().splitlines()[-1])\nopen(f,\"w\").write(src)\nEOF\ntail -c 300 $S/unit_r2a.txt"
}
````

### User / tool · 2026-11-02T15:34:12.513Z

**tool result**
````
C real no-txn: KILLED 1 failed, 26 passed in 9.64s
........ [ 95%]
........................................................................ [ 97%]
........................................................................ [ 98%]
................................................................         [100%]
4880 passed, 8 skipped in 281.00s (0:04:40)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:34:27.669Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && git rev-parse --short HEAD; cat >> $S/probes159/test_probe159.py <<'EOF'\n\n\ndef test_backfail_export_and_trace(promoted, monkeypatch):\n    c, tok, f = promoted\n    from app.backend import review as RV\n    real_apply = RV.DB.apply_review\n    calls = {\"n\": 0}\n    def flaky(*a, **k):\n        calls[\"n\"] += 1\n        if calls[\"n\"] == 2: raise RuntimeError(\"back failed\")\n        return real_apply(*a, **k)\n    real, _ = boom_json(monkeypatch)\n    monkeypatch.setattr(RV.DB, \"apply_review\", flaky)\n    bad = TestClient(c.app, client=(\"127.0.0.1\", 50000), raise_server_exceptions=False)\n    bad.post(f\"/api/cases/{tok}/items/{f['id']}/review\", json={\"action\": \"accept\", \"confirm\": \"likely_duplicate\"})\n    monkeypatch.setattr(RV, \"json\", real); monkeypatch.setattr(RV.DB, \"apply_review\", real_apply)\n    for a in [a for a in c.get(f\"/api/cases/{tok}\").json()[\"entries\"]]:\n        c.post(f\"/api/cases/{tok}/items/{a['id']}/review\", json={\"action\": \"accept\"})\n    r = c.get(f\"/api/cases/{tok}/export\")\n    print(\"BACKFAIL export\", r.status_code, r.text[:400])\n    st = {s[\"id\"]: s for s in c.get(f\"/api/cases/{tok}/items/{f['id']}/trace\").json()[\"steps\"]}\n    print(\"BACKFAIL trace charge_flag\", st.get(\"charge_flag\", {}).get(\"status\"), st.get(\"charge_flag\", {}).get(\"next_action\"))\nEOF\ncd $S/r2a && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest $S/probes159/test_probe159.py -k backfail_export -p no:cacheprovider -q -s 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T15:34:28.818Z

**tool result**
````
67be38d
BACKFAIL export 200 {"token":"fP_So0DNo2uPY_qcd98CdA","generated_at":"2026-11-02T15:34:28Z","letter_text":"TREATMENT CHRONOLOGY\n\nBILLED CHARGES\n\nBrindlewood Physical Therapy, visit note, June 1, 2026: $150.00\nSource [Ex. __ / Bates __]: \"04/16/2026 manual therapy invoiced $150.00.\"\n\nBilled charges accepted from these records: $150.00","internal_notes_text":"INTERNAL REVIEW NOTES — DO NOT SEND\n\nThis chronol
BACKFAIL trace charge_flag pending {'code': 'CONFIRM_FLAG', 'text': 'Confirm the flag by name, or dismiss the charge', 'target': {'item_id': 'a3'}, 'options': ['accept', 'dismiss']}
.
1 passed, 4 deselected in 0.81s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:34:40.834Z

**tool call — Bash**
````
{
 "command": "git log --oneline c0e2b86..HEAD; git diff c0e2b86 HEAD --stat | tail -8; grep -n \"t146_r3\\|first_run\" -r tests/unit/*.py -l | head; ls reviews | grep \"T-159\\|T-161\""
}
````

### User / tool · 2026-11-02T15:34:40.979Z

**tool result**
````
985dbd2 fix(backend): T-139 r4 one money detector (money.py) for the hold, the export gate and the letter eval; the gate scans the final letter text and blocks naming the line; labelled figures and number words after a money verb are money; held-out hints state the true cause
67be38d fix(frontend): T-162 r2 a collapsed Dismissed group says how many of its items carry a re-run note; e2e opens the group and asserts the entry and amount notes visible, unconditional; note helpers at module scope
a4eeb2b docs(orchestrator): scope cut 7e charge-source detection residuals (T-140)
94a31a4 fix(frontend): T-160 the Not in an entry (n) link sits in the entry head line right after the record chip, so it never takes a line of its own; rows are back inside the T-060 compact-row budget (<=2 px)
802d5fd feat(frontend): T-149 r2 one merged case overview block (do-this-first from next_action, amber Can export, open-count chips), loading/error/retry states, j/k and search, case names (create, rename, T-157 titles), rerun only when rerun_available
 tests/e2e/test_multicase.py                        | 386 ++++++++++++++++++---
 tests/e2e/test_polish_r3.py                        |   1 -
 tests/e2e/test_rerun_note.py                       |  44 ++-
 tests/unit/test_t139_charge_text.py                |  26 +-
 tests/unit/test_t139_r3.py                         |  65 +++-
 tests/unit/test_t139_r4.py                         | 168 +++++++++
 tests/unit/test_t139_unmarked.py                   |   4 +-
 32 files changed, 1291 insertions(+), 414 deletions(-)
tests/unit/test_t146_rerun_keeps_items.py
tests/unit/test_t146_r2_failed_rerun_keeps_items.py
tests/unit/test_t161_first_run_stage_down.py
tests/unit/test_t146_r4_ladder_compare_and_conflicts.py
T-159-staff-engineer.md
T-161-staff-engineer.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:34:43.246Z

**tool call — Bash**
````
{
 "command": "git diff c0e2b86 HEAD --stat -- app/backend/pipeline.py app/backend/review.py app/backend/trace.py app/backend/flags.py app/db tests/unit/test_t159_flag_audit.py tests/unit/test_t161_first_run_stage_down.py tests/unit/test_t146_r2_failed_rerun_keeps_items.py tests/unit/test_t146_r3_decided_items_never_lowered.py; echo ---; sed -n 205,235p tests/unit/test_t146_r3_decided_items_never_lowered.py"
}
````

### User / tool · 2026-11-02T15:34:43.364Z

**tool result**
````
---
    assert err == {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    assert_notes(conn, cid, (), "failed", "")


# ---- a re-run with nothing to keep
def test_rerun_with_nothing_to_keep_still_says_the_step_failed(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    first = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=down("extract"))), now=lambda: 1.0)
    assert first["status"] == "done_with_errors" and case_error(conn, cid)[0] == "failed"      # T-161 r2: a first run with no entries at all is failed too (steps named)
    again = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=down("extract"))), now=lambda: 2.0)
    assert again["status"] == "done_with_errors"
    status, err = case_error(conn, cid)
    assert status == "failed"
    assert err == {"code": "run_partial", "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep." + TAIL}


def test_nothing_to_keep_and_something_kept_are_both_said(tmp_path):
    conn, cid = completed(tmp_path)
    good = sample_script()["extract"]
    DB.update_item(conn, "e4", now=2.0, case=cid, summary=None, excerpt=None, state="rejected", state_reasons_json=["LLM_FAILED_AFTER_RETRIES"])      # a stub left by an earlier failure

    def extract(user):
        if which_record(user)[0] in (1, 4):
            raise down("extract")
        return good(user)
    rerun(conn, cid, extract=extract)
    _, err = case_error(conn, cid)
    assert err["message"] == ("The AI step failed for 1 item (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. "
                              "The AI step also failed for 1 item (writing the entries) with no earlier result to keep." + TAIL)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:34:55.983Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/r2a && grep -n \"back = \\|_record_confirm(conn\\|def _record_confirm\\|conn.execute(\\\"BEGIN\\\")\" app/backend/review.py; grep -n \"down = (\\|err = _partial_error\\|named = \" app/backend/pipeline.py; grep -n \"failed = True\" app/backend/flags.py | head -3; grep -n \"validate_schema(res.output\" app/llm/provider.py; grep -n \"def test_\" tests/unit/test_t159_flag_audit.py | sed -n 1,30p | grep -n \"transaction\\|failure\\|each_accept\\|no_timestamp\"; git -C /Users/arsis/zlayt-pm-project diff c0e2b86 HEAD --stat -- .claude/agent-memory/staff-engineer-reviewer | tail -1"
}
````

### User / tool · 2026-11-02T15:34:56.126Z

**tool result**
````
218:def _record_confirm(conn, case_id: str, item_id: str, item: dict, t) -> None:
224:        conn.execute("BEGIN")
261:            _record_confirm(conn, case_id, item_id, item, now)
263:            back = {"pending": "reset", "dismissed": "dismiss"}.get(item.get("review_status"))      # T-159 r2: take the accept back, so no charge counts without its confirm on record
588:        named = {c for _, c, _ in kept} | set(empty)
589:        down = ("finding the flags",) if "flags" in failed_steps and "finding the flags" not in named else ()
590:        err = _partial_error(kept, empty if (rerun or not (dated or undated)) else [s for s in empty if s != _EXTRACT_STEP], down)
256:            failed = True
260:        failed = True
107:    validate_schema(res.output, json_schema)
8:103:def test_each_accept_event_after_a_reset_carries_its_own_confirm(promoted):
9:119:def test_an_accepted_flagged_charge_whose_confirm_has_no_timestamp_asks_for_the_confirm_again(promoted, tmp_path):
10:133:def test_a_failure_writing_the_confirm_leaves_no_half_confirmed_charge(promoted, monkeypatch):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:35:00.348Z

Writing both reviews.

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:35:23.627Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-159-staff-engineer-r2.md",
 "content": "# T-159 staff-engineer review, round 2 (confirm and its event in one transaction)\n\nReviewed commit c0e2b86 on a `git archive` copy taken at that commit. HEAD later moved to 67be38d; `git diff c0e2b86 HEAD --stat` for app/backend/{review,trace,pipeline,flags}.py, app/db and tests/unit/test_t159_flag_audit.py is empty, so none of this card's files changed.\n\nVerdict: **pass**. No blocker, no major. The round-1 minor (three autocommit statements) is fixed for a single fault, and both surviving mutants now die. Two minors remain: the take-back is best-effort, not atomic (a double fault leaves a flagged charge accepted, counted and exported without its confirm), and the dismissed-prior take-back is unpinned. AC1 is T-163's and is not judged here.\n\nIs the compensation safe? For a single failure, yes. `_record_confirm` (review.py:218-235) now writes the item confirm and the event confirm inside one BEGIN/COMMIT/ROLLBACK, so a failure on either leaves neither. `set_review` (review.py:259-267) then takes the accept back with a `reset` (prior pending) or `dismiss` (prior dismissed) and re-raises, so the caller sees a 500 and the trail shows accept then reset. Amounts have no edit action, so those two priors are the only ones. It is not safe against a second fault (finding 1), because the accept is committed by `DB.apply_review` before the confirm write starts and only then taken back. The worker says so in the handoff.\n\nWhat I exercised (archive copy of c0e2b86, `.venv/bin/python`):\n- `pytest tests/unit -q`: 4880 passed, 8 skipped (281 s).\n- Probes (TestClient, `make_env` and the `promoted` fixture from test_t159_flag_audit.py):\n  - prior pending, event write fails: pending again, no confirmed_at, totals unchanged, bare accept 422, retry with confirm works, one `reset` in /audit (the card's own test, re-run).\n  - prior dismissed, event write fails: item ends `dismissed`, confirmed_at None. Correct.\n  - item write (`DB.update_item`) raises inside the transaction: item pending, events show reclassify, accept, reset; no confirm anywhere.\n  - compensation itself fails (the second `DB.apply_review` call raises, after the event write failed): 500; item stays `accepted`, confirmed_at None, `totals.accepted` 15000 count 1; bare accept then 422 CONFIRM_REQUIRED; trace `charge_flag` pending with next_action CONFIRM_FLAG; after accepting the entries, GET /export returns 200 and the letter lists `$150.00` for the flagged duplicate.\n  - prior accepted with the confirm's timestamp stripped, event write fails: stays accepted, unconfirmed, counted (the state before this card, unchanged).\n- Mutants of app/backend/review.py against test_t159_flag_audit.py + test_amounts_d059_api.py (27 tests): ASC order on the newest accept event: killed. Drop the `confirmed_at` clause: killed. Real no-transaction (BEGIN, COMMIT, ROLLBACK replaced by `pass`): killed. ROLLBACK replaced by COMMIT: killed. No compensation: killed. Swallow the failure (return instead of raise): killed. Compensation always `reset` regardless of prior status: survived (finding 2).\n- Read `git show c0e2b86` for review.py, trace.py and the new tests in full.\n\nLabels: finding 1 is a robustness gap against a spec constraint (D-059) that needs two faults; I rate it minor because the single-fault path is closed and the fix is cheap, not because the fix is inconvenient. Finding 2 is a missing test.\n\n```json\n{\"card\": \"T-159\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit c0e2b86 (app/backend/review.py, trace.py, tests/unit/test_t159_flag_audit.py) in a git archive copy; HEAD later 67be38d with none of these files changed; synthetic NOTE from test_amounts_d059_api.py; no app server\",\n \"exercised\": [\"python3 tools/board.py show T-159 and T-161; read reviews/T-159-staff-engineer.md\", \"git archive c0e2b86 copy: pytest tests/unit -q -> 4880 passed, 8 skipped\", \"git show c0e2b86 (review.py, trace.py, tests) in full; git diff c0e2b86 HEAD --stat on this card's files: empty\", \"TestClient probes: prior pending, prior dismissed, item-write failure, compensation failure (export 200 and trace), prior accepted without confirmed_at\", \"7 mutants of review.py against test_t159_flag_audit.py + test_amounts_d059_api.py: 6 killed, 1 survived (always-reset compensation)\", \"grep of callers of set_review and _record_confirm; read db.apply_review and update_item for transaction handling\"],\n \"verdict\": \"pass\",\n \"scores\": {\"atomic_confirm_write\": 4, \"compensation_safety\": 3, \"mutant_kills\": 4, \"failure_visibility\": 5, \"trace_confirm\": 5},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"The take-back is best-effort: if it fails, or the process dies between the two commits, a flagged charge stays accepted, counted and exported without its confirm\",\n   \"evidence\": \"app/backend/review.py:257 DB.apply_review commits the accept; review.py:261-267 _record_confirm then the take-back, each a separate transaction. Repro (archive, promoted fixture): event write raises (json.loads patched) and the second DB.apply_review call raises -> POST accept confirm=likely_duplicate returns 500; GET case shows review_status accepted, flag.confirmed_at None, totals.accepted {'cents': 15000, 'count': 1}; trace charge_flag status pending with next_action CONFIRM_FLAG; after accepting the entries GET /export returns 200 and letter_text contains 'Brindlewood Physical Therapy, visit note, June 1, 2026: $150.00' for the likely_duplicate charge. A bare accept then returns 422 CONFIRM_REQUIRED, so a retry repairs it.\",\n   \"why_it_matters\": \"D-059 says a flagged charge is not counted unless confirmed by name. Under a double fault, or a kill between the two commits, the invariant holds only until someone retries; meanwhile totals and the letter carry the duplicate. The 500 is visible, but the state that follows is not flagged at export time.\",\n   \"fix\": \"Either give DB.apply_review an optional extra for after_json and the item ladder so status, item confirm and event are one transaction (db owner), or make the export gate and totals refuse an accepted charge whose ladder.confirm has no confirmed_at (trace.py already shows it as pending CONFIRM_FLAG, so the read side knows).\",\n   \"acceptance_test\": \"Inject the double fault as above: either the charge is pending/dismissed afterwards, or GET /export returns 422 with a CONFIRM_FLAG blocker naming the charge until it is confirmed or dismissed.\"},\n  {\"severity\": \"minor\", \"title\": \"Mutant survives: the take-back of a previously dismissed charge always resets instead of dismissing\",\n   \"evidence\": \"replace the dict at review.py:263 {\\\"pending\\\": \\\"reset\\\", \\\"dismissed\\\": \\\"dismiss\\\"}.get(item.get(\\\"review_status\\\")) with \\\"reset\\\" -> 27 passed (test_t159_flag_audit.py + test_amounts_d059_api.py). tests/unit/test_t159_flag_audit.py:133 test_a_failure_writing_the_confirm_leaves_no_half_confirmed_charge starts only from pending. My probe of the dismissed prior ends 'dismissed', so the code is right; no test pins it.\",\n   \"why_it_matters\": \"A dismissed charge whose accept fails would reappear as pending under that regression, undoing the paralegal's earlier decision without a word.\",\n   \"fix\": \"Add a variant of the failure-injection test that dismisses the charge first and asserts review_status == 'dismissed' after the 500.\",\n   \"acceptance_test\": \"The always-reset mutant fails that test; HEAD passes it.\"},\n  {\"severity\": \"nit\", \"title\": \"The take-back's own failure is not caught, so the caller sees only the second exception\",\n   \"evidence\": \"review.py:263-266: DB.apply_review(conn, item_id, back, ...) inside the except block is not guarded; if it raises, the original exception survives only as __context__ and nothing logs that the accept was left standing.\",\n   \"why_it_matters\": \"A person debugging the 500 sees the take-back error, not that a counted charge remains.\",\n   \"fix\": \"Wrap the take-back, log both errors with the item id, and re-raise the original.\",\n   \"acceptance_test\": \"Compensation-failure probe: the log line names the item and says the accept stands.\"}\n ],\n \"whats_right\": [\"the item confirm and the event confirm share one BEGIN/COMMIT with ROLLBACK on error; the real no-transaction mutant and the ROLLBACK-to-COMMIT mutant are both killed\", \"both round-1 survivors (newest-event ordering, confirmed_at required for the no-op) now die, with tests that assert behaviour (event confirm values, 422 on the stripped state)\", \"failures stay loud: every injected fault returns 500, the taken-back accept shows up as an accept then reset in /audit, and a retry with the confirm works\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T15:35:23.770Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-159-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:35:46.603Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-161-staff-engineer-r2.md",
 "content": "# T-161 staff-engineer review, round 2 (flag step read from failed_steps; extract-down first run with no entries is failed)\n\nReviewed commit 99438fb as contained in c0e2b86, on a `git archive` copy taken at c0e2b86. HEAD later moved to 67be38d; `git diff c0e2b86 HEAD --stat` for app/backend/pipeline.py, flags.py, tests/unit/test_t161_first_run_stage_down.py and the two T-146 test files is empty.\n\nVerdict: **pass**. No blocker, no major. The round-1 blocker is closed: a first run with the flag step down on a note with no phrase-list hit now reads `failed | run_partial | RUN_FAILED` with the step named, and the export is blocked. Extract down with no entry at all on a first run reads failed with the step named. Two minors (one surviving mutant, one case that still reads ready) and one nit.\n\nWhat I exercised (archive copy of c0e2b86, `.venv/bin/python`):\n- `pytest tests/unit -q`: 4880 passed, 8 skipped (281 s). The T-161 file, both T-146 pin files and the T-146 re-run files pass.\n- Round-1 repro, in-process (`PL.run_pipeline`, FakeCall) on the two-record plain note: flags down (LLMFailed) and flags fixture-miss both give `failed`, code `run_partial`, message \"The AI step (finding the flags) failed on this run, so nothing from it could be used. Run it again to retry.\", blockers `RUN_FAILED`. The golden sample with flags down still gives \"The AI step failed for 7 items (finding the flags) on this run, and there is no earlier result to keep.\" (no double naming).\n- Same repro through the API (TestClient POST /run, GET /status, accept both entries, GET /export): status `failed`, error run_partial as above, export 422 `export_blocked` with blocker `RUN_FAILED`. Round 1 had status ready and export 200.\n- Extract matrix: all 9 records down gives failed with \"9 items (writing the entries)\"; 8 of 9 down gives `done_with_errors`, 1 entry, case `ready`, no error (the tray-shape rule, see question).\n- Three flipped pins, read in full: see the section below.\n- 9 mutants of pipeline.py (down always empty, flags never in failed_steps, drop the `named` dedupe, old extract filter, extract never filtered, `not dated` instead of `not (dated or undated)`, `_partial_error` ignoring `down`, wording without the step name, down on first run only) against the T-161 file and the T-146 r2, r3, r4 and re-run files: 8 killed, 1 survived (finding 1).\n- Read `git show 99438fb` in full, and run_flag_pass, _noting, _failure and run_pipeline.\n\nThe three flipped pins (checked one by one):\n- `test_t146_r2_failed_rerun_keeps_items.py` (renamed `test_first_run_with_extract_down_still_stores_its_stubs_and_is_failed_with_the_step_named`): still asserts 9 stored stub rows, all rejected with LLM_FAILED_AFTER_RETRIES; the only flip is `err is None / ready` to `failed`, `run_partial` and \"(writing the entries)\". Justified: it is exactly the decision the orchestrator made for r2; the stub assertions are kept.\n- `test_t146_r3_decided_items_never_lowered.py` (`test_rerun_with_nothing_to_keep_still_says_the_step_failed`): `== (\"ready\", None)` became `case_error(...)[0] == \"failed\"`. Justified, but the status-only assertion is looser than the old exact tuple; the exact first-run message is pinned in test_t161 (`err == {...9 items (writing the entries)...}`) so nothing is lost. The re-run half of that test is unchanged and exact.\n- The T-161 file's own extract-down test: rewritten from \"unchanged ready\" to the failed shape, and a partial-extract test added that keeps the old ready shape. Justified.\nNone of the three flips hides a regression: each moves one assertion to the behaviour the brief named, and the surrounding assertions still bite (mutants 4 and 5 are killed by these files).\n\nLabels: both findings are test or edge gaps, not spec violations (minor). The nit is a defensive branch that the production call layer cannot reach.\n\n```json\n{\"card\": \"T-161\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit 99438fb within c0e2b86 (app/backend/pipeline.py hunk, tests/unit/test_t161_first_run_stage_down.py, test_t146_r2 and r3 pin flips) in a git archive copy; golden sample and a two-record plain synthetic note; HEAD later 67be38d with none of these files changed\",\n \"exercised\": [\"python3 tools/board.py show T-161; read reviews/T-161-staff-engineer.md\", \"git archive c0e2b86 copy: pytest tests/unit -q -> 4880 passed, 8 skipped\", \"git show 99438fb in full (pipeline.py, T-161 file, both T-146 files); git diff c0e2b86 HEAD --stat on these files: empty\", \"round-1 repro in-process: plain note with flags down (LLMFailed and fixture-miss) -> failed/run_partial/RUN_FAILED; sample with flags down -> one naming of the step\", \"API run: POST /run, GET /status, accept entries, GET /export on the plain note with flags down -> 422 export_blocked RUN_FAILED\", \"extract matrix: 9 of 9 down -> failed, 8 of 9 down -> ready with 1 entry\", \"9 pipeline.py mutants vs T-161 + T-146 r2/r3/r4/re-run files: 8 killed, 1 survived\", \"schema-invalid flag output via FakeCall on the plain note (ready), then read app/llm/provider.py:107 validate_schema\"],\n \"verdict\": \"pass\",\n \"scores\": {\"stage_coverage\": 4, \"gate_agreement\": 5, \"message_names_step\": 5, \"test_strength\": 4, \"pin_flips_justified\": 5},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"Mutant survives: the 'no entry at all' test counts dated entries only\",\n   \"evidence\": \"app/backend/pipeline.py:590 `empty if (rerun or not (dated or undated)) else ...`; change `not (dated or undated)` to `not dated` -> 134 passed (tests/unit/test_t161_first_run_stage_down.py + test_t146_r2/r3/r4/re-run files). Every extract-down test in the T-161 file produces dated entries or none.\",\n   \"why_it_matters\": \"A first run where the only entry that came out is undated, and every other record failed extraction, must keep the tray shape (some entries came out). With the mutant it would read failed. The boundary of the new rule is unpinned.\",\n   \"fix\": \"Add a first-run test with one record whose extract gives an undated entry and the rest down: case ready, failed records as tray items, no RUN_FAILED.\",\n   \"acceptance_test\": \"The `not dated` mutant fails that test; HEAD passes it.\"},\n  {\"severity\": \"minor\", \"title\": \"A first run where extract fails for 8 of 9 records still reads ready with no error\",\n   \"evidence\": \"probe on the sample, extract raises LLMFailed for every record except record 1: out['status'] done_with_errors, counts.entries 1, case status ready, error None. Pinned by tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_extract_down_for_some_records_keeps_its_old_shape (written for one record down).\",\n   \"why_it_matters\": \"The orchestrator's rule is 'no entry at all'; the stubs are visible in the tray, so this is not a silent fallback. But a case where most records produced nothing reads the same as one record down, and the message that names the step appears only at zero.\",\n   \"fix\": \"Decide whether a majority-down first run should read failed or carry a non-blocking note; if the current rule stays, say so in the test name and in api.md.\",\n   \"acceptance_test\": \"A test for a mostly-down first run asserting the chosen status and message.\"},\n  {\"severity\": \"nit\", \"title\": \"The flag step's schema-invalid branch is not recorded in failed_steps\",\n   \"evidence\": \"app/backend/flags.py:255-256 sets failed = True on a pydantic ValidationError without raising, so _noting never appends 'flags'. FakeCall returning {'flags': 'not a list'} on the plain note gives ('ready', None). In production the provider validates the JSON schema first (app/llm/provider.py:107 validate_schema), which raises and reaches _noting as LLMFailed, so I could not reach the branch outside a test double.\",\n   \"why_it_matters\": \"If the pydantic model ever gets a rule the JSON schema does not carry, the r1 blocker returns through that door.\",\n   \"fix\": \"Raise or record the step in failed_steps on that branch, or delete the branch and let validation failures propagate.\",\n   \"acceptance_test\": \"Plain note, flags returns a schema-invalid object -> case failed, run_partial, 'finding the flags'.\"}\n ],\n \"whats_right\": [\"the flag step is now read from the steps that were down, with a dedupe against rows that already carry the failure, so the sample's message names the step once and the plain note's names it without an item count\", \"the same _partial_error path serves first run and re-run, so message and RUN_FAILED gate cannot drift apart; 8 of 9 mutants die\", \"the three flipped pins each change one assertion to the decided behaviour and keep the surrounding stub and message assertions\"],\n \"questions_for_chris\": [\"An extract-down first run with some entries (even 1 of 9) reads ready with tray stubs. Is 'failed only at zero entries' the intended threshold?\"]}\n```\n"
}
````

### User / tool · 2026-11-02T15:35:46.830Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-161-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:35:49.585Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -5; python3 - <<'EOF'\nimport json,re\nfor f in [\"reviews/T-159-staff-engineer-r2.md\",\"reviews/T-161-staff-engineer-r2.md\"]:\n    t=open(f).read(); m=re.findall(r\"```json\\n(.*?)\\n```\",t,re.S); print(f,len(m),json.loads(m[0])[\"verdict\"])\nEOF"
}
````

### User / tool · 2026-11-02T15:35:49.763Z

**tool result**
````
ok (164 file(s))
reviews/T-159-staff-engineer-r2.md 1 pass
reviews/T-161-staff-engineer-r2.md 1 pass
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:35:54.128Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t159_t161_r2_patterns.md",
 "content": "---\nname: t159-t161-r2-patterns\ndescription: T-159 r2 c0e2b86 pass, T-161 r2 99438fb pass: compensation not atomic (double fault exports unconfirmed flagged charge), always-reset mutant, undated boundary mutant, FakeCall bypasses provider.validate_schema\nmetadata:\n  type: project\n---\n\nT-159 r2 / T-161 r2 both pass (minors only).\n\n- A \"take the accept back\" compensation is safe for one fault only. Probe the double fault (patch the event write AND the second DB.apply_review call): accepted flagged charge stays, totals count it, GET /export 200. Fix is a read-side guard (export blocks accepted + ladder.confirm without confirmed_at) or one transaction in db.apply_review.\n- Compensation tables keyed on prior status need a test per prior state (always-reset mutant survived; dismissed prior untested).\n- A literal `BEGIN`-to-`COMMIT` swap in a mutant script may give a syntax error (\"2 errors\"), which is not a kill. Replace the three execute calls with `pass` for a real no-transaction mutant.\n- FakeCall bypasses app/llm/provider.py:107 validate_schema, so a schema-invalid probe via FakeCall reaches branches the real call layer cannot (flags.py:255 failed=True not in failed_steps). Say so before rating.\n- Count-the-entries rules (`dated or undated`) need a test where only the second list is non-empty.\n\n**Why:** found while verifying fixes round 2. **How to apply:** when a card says \"atomic\" or \"compensated\", run the double-fault probe and read the export, not only /status.\n"
}
````

### User / tool · 2026-11-02T15:35:54.221Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t159_t161_r2_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:35:58.754Z

**tool call — Bash**
````
{
 "command": "echo \"- [T-159/T-161 r2 patterns](project_t159_t161_r2_patterns.md) — both pass: compensation fails under double fault (export 200), always-reset mutant, undated-boundary mutant, FakeCall skips validate_schema\" >> .claude/agent-memory/staff-engineer-reviewer/MEMORY.md; tail -2 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md | cut -c1-120"
}
````

### User / tool · 2026-11-02T15:35:58.836Z

**tool result**
````
- [T-162 rerun-note patterns](project_t162_rerun_note_patterns.md) — 70af4a7 fail: 6379c0b paste breaks mountSection (
- [T-159/T-161 r2 patterns](project_t159_t161_r2_patterns.md) — both pass: compensation fails under double fault (expo
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:36:03.082Z

Both cards pass with no blocker and no major; the unit suite on a `git archive` copy at c0e2b86 gave 4880 passed, 8 skipped.
- **T-161 (99438fb):** pass. Your round-1 repro (flags down, no phrase-list hit) now reads `failed | run_partial | RUN_FAILED` with "finding the flags" named, and the API export returns 422. An extract-down first run with no entries now reads failed. The three flipped pins are justified (8 of 9 mutants die). Minors: the `not dated` mutant survives, and 8 of 9 records down still reads ready.
- **T-159 (c0e2b86):** pass. The confirm and its event now share one transaction, and the take-back is safe for a single fault. A double fault leaves a flagged charge accepted, counted and exported (export 200) without its confirm, so I filed it as a minor. Both original mutants die; an always-reset compensation mutant survives (minor).

Reviews are `reviews/T-159-staff-engineer-r2.md` and `reviews/T-161-staff-engineer-r2.md` (board validate ok). One question for Chris, filed in the T-161 review: is "failed only at zero entries" the intended threshold?
