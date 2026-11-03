# T-161 staff-engineer review (first run with a stage down reads failed, gate RUN_FAILED)

Reviewed commit 83f1afd (HEAD at review start) on a `git archive 83f1afd` copy. HEAD later moved to ba21b4b; `git diff 83f1afd ba21b4b --stat` touches only conflicts.py, SCOPE_CUTS.md and a T-141 test, none in this card's path.

Verdict: **fail**. One blocker: the flag step is detected only through failure-marked lexicon flags, so a first run whose flag step is down on records with no phrase-list hit still reads `ready`, shows zero flags, and exports with HTTP 200. The card's own AC says "no stage missed", and this is the stage it names first.

What I exercised (archive copy, `.venv/bin/python`):
- `pytest tests/unit -q`: 4613 passed, 8 skipped. `tests/unit/test_t161_first_run_stage_down.py`: 13 green.
- Stage matrix on a first run, in-process through `PL.run_pipeline` with FakeCall, on the golden sample and on a two-record plain note (no phrase-list hit): j1, j2, j3, j4, flags, conflicts, extract, split (unsplit paste), and Spanish `extract_es` / `judge_faithfulness_es`.
- API run (TestClient `/run`, `/status`, `/export`) for flags down on the sample and on the plain note.
- 10 mutants of `pipeline.py` (reverting the T-161 line, dropping each step from the first-run list, keeping extract, failed-only-on-timeout, FIXTURE_MISS not a flag failure, flag-kind check removed, unavailable arm removed, names dropped from the message) run against the T-161 file, then against the T-145/T-146/rerun/partial tests: 10 of 10 killed.

Results of the matrix (status | error code | gate):
- sample j1 (9 items), j2 (3), j3 (1), flags (7): `failed | run_partial | RUN_FAILED`, message "The AI step failed for N items (the second check|finding the flags) on this run, and there is no earlier result to keep. Run it again to retry." Spanish `judge_faithfulness_es` and `j1` on a mixed packet: same.
- sample j4 with the default empty-flag script: `ready`. That is by design (`flags.py` `judge_flags`: lexicon-only flags have no judge); the card's test sets `model_flag` so j4 has something to judge.
- plain note, flags down: `ready | none | no RUN_FAILED`; accept both verified entries, GET export returns 200 with a letter (finding 1).
- extract down and split down: `ready` with `done_with_errors` and the failure shown as tray items or a split error; by design and pinned by the T-146 r3 test. Not counted as a finding (question below).

Labels: finding 1 violates the card AC and the persona's no-silent-failure rule (blocker). Finding 2 is a missing-test item (minor). The reading of j2/j3/j4 as "the second check" is wording I would have done differently, not a defect.

```json
{"card": "T-161", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 83f1afd (pipeline.py hunk, tests/unit/test_t161_first_run_stage_down.py) in a git archive copy; golden sample, a two-record plain synthetic note, a mixed English/Spanish synthetic packet, the unsplit paste from test_split_llm",
 "exercised": ["python3 tools/board.py show T-161; git show 83f1afd (full diff)", "git archive 83f1afd copy: pytest tests/unit -q -> 4613 passed, 8 skipped; T-161 file 13 passed", "in-process stage matrix on a first run: j1 j2 j3 j4 flags conflicts extract split, on the sample and on a plain note; Spanish extract_es / judge_faithfulness_es / j1 on a mixed packet", "API run of flags-down through POST /run, GET /status, GET /export on the sample (failed, run_partial, export 422 RUN_FAILED) and on the plain note (ready, export 200)", "10 pipeline.py mutants vs the T-161 file and the T-145/T-146/rerun/partial tests: 10 killed", "read flags.py run_flag_pass/merge/judge_flags and pipeline.py _noting/_failure/_partial_error/run_pipeline"],
 "verdict": "fail",
 "scores": {"stage_coverage": 2, "gate_agreement": 4, "message_names_step": 4, "test_strength": 4, "clean_run_stays_ready": 5},
 "findings": [
  {"severity": "blocker", "title": "A first run with the flag step down reads ready (and exports) when the records have no phrase-list hit",
   "evidence": "Repro: two-record note ('Patient seen for follow up of neck stiffness. Range of motion improved.' / 'Patient seen. Physical therapy continued 2x per week.'), every call works except step 'flags' raises AU.LLMFailed. Result: GET /status status 'ready', error null; GET case flags 0, warnings []; accept both verified entries; GET /export -> 200 with the letter. The same note with j1 down is 'failed | run_partial | RUN_FAILED'. Cause: app/backend/pipeline.py:247 _failure and :242 _FLAG_FAIL detect a failed flag step only on a flag row whose reasons carry LLM_FAILED_AFTER_RETRIES or FIXTURE_MISS, and app/backend/flags.py:164 sets that marker only on lexicon flags (merge loop over lex_flags). With no lexicon flag there is no row, so `empty` never gets 'finding the flags'. pipeline.py:443-450 _noting already records failed_steps (it holds 'flags') and pipeline.py:575 already reads it for prune; line 583 does not.",
   "why_it_matters": "This is a silent fallback to 'no AI flags': a paralegal gets a ready case with no pre-existing or causation warnings and an open export, though the step never ran. The card's AC and title name the flags stage; the unit test passes only because the sample's records 3 and 6 happen to carry phrase-list flags (test_first_run_with_the_flag_step_down_fails_the_case_and_names_the_step uses the sample, 7 items).",
   "fix": "In run_pipeline, if 'flags' is in failed_steps and no stub row carried it, add 'finding the flags' to the steps passed to _partial_error (first run and re-run); keep prune logic as is. The message may count records instead of items when there is no item.",
   "acceptance_test": "Unit test: first run of a two-record note with no phrase-list hit and the flags step down (both LLMFailed and FixtureMiss) -> case failed, error.code run_partial, message names 'finding the flags', trace.export_blockers has RUN_FAILED; same note with flags working stays ready; a good second run clears it. Mutant: drop the failed_steps addition and the test fails."},
  {"severity": "minor", "title": "Stage tests all run on the golden sample, which hides stage-detection that depends on the input",
   "evidence": "tests/unit/test_t161_first_run_stage_down.py:first_run uses G.raw('sample') for every parametrized case; j2 on a note with no dollar amount and flags on a note with no lexicon hit are not covered (my probe: plain note j2 and flags down both 'ready').",
   "why_it_matters": "It let finding 1 pass 13 tests and 10 of 10 mutants. For j2 on a case with no amounts there is nothing to judge, so ready is right; the test should say so rather than leave it open.",
   "fix": "Add the plain-note rows: flags down (expects failed), j2 down with no amounts (expects ready, documented).",
   "acceptance_test": "Parametrize first_run over the sample and a plain note; the flags-down row on the plain note fails against HEAD and passes after the fix."}
 ],
 "whats_right": ["one code path: the first run reuses the T-146 _partial_error wording, so the message and the RUN_FAILED gate cannot drift between first run and re-run", "tests pin the clean first run staying ready, a good second run clearing a failed first run, and extract-down keeping its tray shape", "all 10 mutants of the first-run line were killed, including FIXTURE_MISS and the flag-kind check"],
 "questions_for_chris": ["A first run with extract down or the splitter down still reads 'ready' with done_with_errors and tray/split-error items (pinned by T-146 r3 by design). Is that still the intended reading, or should those two also read failed?"]}
```
