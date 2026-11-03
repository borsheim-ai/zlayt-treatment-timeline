# T-161 staff-engineer review, round 2 (flag step read from failed_steps; extract-down first run with no entries is failed)

Reviewed commit 99438fb as contained in c0e2b86, on a `git archive` copy taken at c0e2b86. HEAD later moved to 67be38d; `git diff c0e2b86 HEAD --stat` for app/backend/pipeline.py, flags.py, tests/unit/test_t161_first_run_stage_down.py and the two T-146 test files is empty.

Verdict: **pass**. No blocker, no major. The round-1 blocker is closed: a first run with the flag step down on a note with no phrase-list hit now reads `failed | run_partial | RUN_FAILED` with the step named, and the export is blocked. Extract down with no entry at all on a first run reads failed with the step named. Two minors (one surviving mutant, one case that still reads ready) and one nit.

What I exercised (archive copy of c0e2b86, `.venv/bin/python`):
- `pytest tests/unit -q`: 4880 passed, 8 skipped (281 s). The T-161 file, both T-146 pin files and the T-146 re-run files pass.
- Round-1 repro, in-process (`PL.run_pipeline`, FakeCall) on the two-record plain note: flags down (LLMFailed) and flags fixture-miss both give `failed`, code `run_partial`, message "The AI step (finding the flags) failed on this run, so nothing from it could be used. Run it again to retry.", blockers `RUN_FAILED`. The golden sample with flags down still gives "The AI step failed for 7 items (finding the flags) on this run, and there is no earlier result to keep." (no double naming).
- Same repro through the API (TestClient POST /run, GET /status, accept both entries, GET /export): status `failed`, error run_partial as above, export 422 `export_blocked` with blocker `RUN_FAILED`. Round 1 had status ready and export 200.
- Extract matrix: all 9 records down gives failed with "9 items (writing the entries)"; 8 of 9 down gives `done_with_errors`, 1 entry, case `ready`, no error (the tray-shape rule, see question).
- Three flipped pins, read in full: see the section below.
- 9 mutants of pipeline.py (down always empty, flags never in failed_steps, drop the `named` dedupe, old extract filter, extract never filtered, `not dated` instead of `not (dated or undated)`, `_partial_error` ignoring `down`, wording without the step name, down on first run only) against the T-161 file and the T-146 r2, r3, r4 and re-run files: 8 killed, 1 survived (finding 1).
- Read `git show 99438fb` in full, and run_flag_pass, _noting, _failure and run_pipeline.

The three flipped pins (checked one by one):
- `test_t146_r2_failed_rerun_keeps_items.py` (renamed `test_first_run_with_extract_down_still_stores_its_stubs_and_is_failed_with_the_step_named`): still asserts 9 stored stub rows, all rejected with LLM_FAILED_AFTER_RETRIES; the only flip is `err is None / ready` to `failed`, `run_partial` and "(writing the entries)". Justified: it is exactly the decision the orchestrator made for r2; the stub assertions are kept.
- `test_t146_r3_decided_items_never_lowered.py` (`test_rerun_with_nothing_to_keep_still_says_the_step_failed`): `== ("ready", None)` became `case_error(...)[0] == "failed"`. Justified, but the status-only assertion is looser than the old exact tuple; the exact first-run message is pinned in test_t161 (`err == {...9 items (writing the entries)...}`) so nothing is lost. The re-run half of that test is unchanged and exact.
- The T-161 file's own extract-down test: rewritten from "unchanged ready" to the failed shape, and a partial-extract test added that keeps the old ready shape. Justified.
None of the three flips hides a regression: each moves one assertion to the behaviour the brief named, and the surrounding assertions still bite (mutants 4 and 5 are killed by these files).

Labels: both findings are test or edge gaps, not spec violations (minor). The nit is a defensive branch that the production call layer cannot reach.

```json
{"card": "T-161", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 99438fb within c0e2b86 (app/backend/pipeline.py hunk, tests/unit/test_t161_first_run_stage_down.py, test_t146_r2 and r3 pin flips) in a git archive copy; golden sample and a two-record plain synthetic note; HEAD later 67be38d with none of these files changed",
 "exercised": ["python3 tools/board.py show T-161; read reviews/T-161-staff-engineer.md", "git archive c0e2b86 copy: pytest tests/unit -q -> 4880 passed, 8 skipped", "git show 99438fb in full (pipeline.py, T-161 file, both T-146 files); git diff c0e2b86 HEAD --stat on these files: empty", "round-1 repro in-process: plain note with flags down (LLMFailed and fixture-miss) -> failed/run_partial/RUN_FAILED; sample with flags down -> one naming of the step", "API run: POST /run, GET /status, accept entries, GET /export on the plain note with flags down -> 422 export_blocked RUN_FAILED", "extract matrix: 9 of 9 down -> failed, 8 of 9 down -> ready with 1 entry", "9 pipeline.py mutants vs T-161 + T-146 r2/r3/r4/re-run files: 8 killed, 1 survived", "schema-invalid flag output via FakeCall on the plain note (ready), then read app/llm/provider.py:107 validate_schema"],
 "verdict": "pass",
 "scores": {"stage_coverage": 4, "gate_agreement": 5, "message_names_step": 5, "test_strength": 4, "pin_flips_justified": 5},
 "findings": [
  {"severity": "minor", "title": "Mutant survives: the 'no entry at all' test counts dated entries only",
   "evidence": "app/backend/pipeline.py:590 `empty if (rerun or not (dated or undated)) else ...`; change `not (dated or undated)` to `not dated` -> 134 passed (tests/unit/test_t161_first_run_stage_down.py + test_t146_r2/r3/r4/re-run files). Every extract-down test in the T-161 file produces dated entries or none.",
   "why_it_matters": "A first run where the only entry that came out is undated, and every other record failed extraction, must keep the tray shape (some entries came out). With the mutant it would read failed. The boundary of the new rule is unpinned.",
   "fix": "Add a first-run test with one record whose extract gives an undated entry and the rest down: case ready, failed records as tray items, no RUN_FAILED.",
   "acceptance_test": "The `not dated` mutant fails that test; HEAD passes it."},
  {"severity": "minor", "title": "A first run where extract fails for 8 of 9 records still reads ready with no error",
   "evidence": "probe on the sample, extract raises LLMFailed for every record except record 1: out['status'] done_with_errors, counts.entries 1, case status ready, error None. Pinned by tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_extract_down_for_some_records_keeps_its_old_shape (written for one record down).",
   "why_it_matters": "The orchestrator's rule is 'no entry at all'; the stubs are visible in the tray, so this is not a silent fallback. But a case where most records produced nothing reads the same as one record down, and the message that names the step appears only at zero.",
   "fix": "Decide whether a majority-down first run should read failed or carry a non-blocking note; if the current rule stays, say so in the test name and in api.md.",
   "acceptance_test": "A test for a mostly-down first run asserting the chosen status and message."},
  {"severity": "nit", "title": "The flag step's schema-invalid branch is not recorded in failed_steps",
   "evidence": "app/backend/flags.py:255-256 sets failed = True on a pydantic ValidationError without raising, so _noting never appends 'flags'. FakeCall returning {'flags': 'not a list'} on the plain note gives ('ready', None). In production the provider validates the JSON schema first (app/llm/provider.py:107 validate_schema), which raises and reaches _noting as LLMFailed, so I could not reach the branch outside a test double.",
   "why_it_matters": "If the pydantic model ever gets a rule the JSON schema does not carry, the r1 blocker returns through that door.",
   "fix": "Raise or record the step in failed_steps on that branch, or delete the branch and let validation failures propagate.",
   "acceptance_test": "Plain note, flags returns a schema-invalid object -> case failed, run_partial, 'finding the flags'."}
 ],
 "whats_right": ["the flag step is now read from the steps that were down, with a dedupe against rows that already carry the failure, so the sample's message names the step once and the plain note's names it without an item count", "the same _partial_error path serves first run and re-run, so message and RUN_FAILED gate cannot drift apart; 8 of 9 mutants die", "the three flipped pins each change one assertion to the decided behaviour and keep the surrounding stub and message assertions"],
 "questions_for_chris": ["An extract-down first run with some entries (even 1 of 9) reads ready with tray stubs. Is 'failed only at zero entries' the intended threshold?"]}
```
