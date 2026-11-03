# T-037 review: staff-engineer-reviewer

Verdict: fail (1 blocker, 2 major, 1 minor). Reviewed the tree at HEAD 81df4e0, which includes the T-037 commits d67a82d, 0d040d3 and fe4e6a2.

Exercised:
- `.venv/bin/python -m pytest tests/unit -q`: 767 passed, 1 failed. The failure is `test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode` (`IndexError` on `j["warnings"][0]`). It is in the API route tests and I did not bisect it. I do not attribute it to T-037.
- `.venv/bin/python -m app.pipeline evals/golden/sample.txt`, run twice:
  - exit 0, and the stdout is byte-identical across both runs.
  - 9 entries, the 73-day gap, and $8,390.00 detected (not a total) are all present.
  - stderr carries 21 `llm call failed` warnings, all judge steps (j1 to j4). Every one of the 9 entries is `[needs_review]`.
- A replay of every golden case on the fixture backend, counting failed calls (scratch script, not committed):

| Case | Failed calls | States |
|---|---|---|
| sample | 21 | 22 needs_review, 2 verified |
| case_01 | 11 | all needs_review |
| case_02 to case_09 | 0 | normal |

- I also checked case_07 and sample after a run:
  - Every item has review_status `pending`, a state, and a ladder with a backend.
  - case_07 has exactly one `injection_suspected` record_warning for record 3.
- Scratch-copy mutation of `app/backend/pipeline.py` (`git archive HEAD` copy), running `test_pipeline.py` and `test_t037_backend.py` against each mutant:

| Mutant | Result |
|---|---|
| Drop the ENDPOINT_NOT_VERIFIED context | caught |
| Deadline never expires | caught |
| Ladder backend dropped | caught |
| Gap computed without record 6 | caught |
| Remove the record_warning dedupe (line 276) | **not caught** (44 passed) |

- Read all of `app/backend/pipeline.py` and `app/llm/audited.py`.

Checks that came out right:
- Stage names match api.md.
- Code stages produce output with every LLM call failing (stub backend), and the gap is unchanged when an entry is dropped.
- finalize gives every flag a state, including ENDPOINT_NOT_VERIFIED.
- The deadline takes an injectable `now`.
- `_DB_LOCK` only wraps `add_llm_call`, is not re-entrant, and has no nested acquisition, so I found no deadlock.
- Every run leaves review_status `pending`.

I did not run the fixtures-contain-only-golden-text grep. The recorder guard test passes, but I did not independently grep a non-golden phrase.

```json
{"card": "T-037", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "HEAD 81df4e0 incl. d67a82d/0d040d3/fe4e6a2; app/backend/pipeline.py, app/llm/audited.py, tests/unit/test_pipeline.py, tests/unit/test_t037_backend.py, tests/fixtures/llm; CLI on evals/golden/sample.txt (fixture backend)",
 "exercised": ["pytest tests/unit -q (767 passed, 1 failed in test_api_routes, not T-037)", "python -m app.pipeline evals/golden/sample.txt x2, stdout identical, exit 0, 21 stderr 'llm call failed' warnings", "scratch replay of every golden case on fixture backend counting failed llm calls (sample 21, case_01 11, others 0)", "scratch run of case_07 and sample: review_status, ladder backend, state, record_warning dedupe", "scratch-copy mutation of pipeline.py (5 mutants; dedupe removal survives)", "read app/backend/pipeline.py and app/llm/audited.py in full; read api.md status section"],
 "verdict": "fail",
 "scores": {"llm_vs_code_separation": 4, "failure_visibility": 3, "test_strength": 2, "determinism_and_fixtures": 2, "stage_and_status_contract": 4},
 "findings": [
  {"severity": "blocker", "title": "Fixtures for sample and case_01 are stale: replay hits 21 and 11 fixture misses, contradicting AC7 and AC1 'all done' evidence",
   "evidence": "Scratch replay with LLM_BACKEND=fixture: sample.txt failed_calls=21 (CLI stderr by step: j1 x9, j2 x3, j3 x1, j4 x8), case_01 failed_calls=11, other cases 0. CLI output shows all 9 entries '[needs_review]'. Reasons counter for sample: JUDGE_UNAVAILABLE x21. Card AC7 evidence: 'test_replay_has_no_fixture_miss[*] 0 FixtureMiss on sample+9 cases'. Fixtures last committed 0d040d3 (20:06:56); 3f37141 (20:07:17) and 81df4e0 (20:07:45) changed flag/conflict prompts or templates after recording. Orchestrator note 02:01:02Z required re-recording after backend-1's prompt changes.",
   "why_it_matters": "AC7 requires 0 FixtureMissing on sample and case_01..09; the headline demo case has 21 and the CLI cannot show a verified timeline on fixtures. Evals run on the fixture backend will compare against needs_review everywhere. The AC was ticked done with evidence that is false for sample and case_01.",
   "fix": "Re-record fixtures for sample and case_01 (and any case whose prompt hashes changed) after the last prompt/template change, then re-run the miss count over all ten inputs.",
   "acceptance_test": "A test that counts llm_calls rows with error LIKE 'FIXTURE_MISS%' (or the audited-wrapper warning count) over sample + case_01..09 and asserts 0, printing the count; it fails today with 21 and 11."},
  {"severity": "major", "title": "test_replay_has_no_fixture_miss is vacuous: it passes with 32 fixture misses (21 sample + 11 case_01)",
   "evidence": "tests/unit/test_t037_backend.py:36-38 asserts view['errors'] == [], status == 'done' and no item reason 'FIXTURE_MISS'. Judge-call misses surface as reason JUDGE_UNAVAILABLE with status done, so the test is green (767 passed) while sample logs 21 misses.",
   "why_it_matters": "A test that stays green when the thing it names is broken gives false assurance (same family as a stubbed verifier). It is how finding 1 shipped with AC ticked.",
   "fix": "Assert on the llm_calls table (or the audited warning) for FIXTURE_MISS rows, and also assert JUDGE_UNAVAILABLE is absent for fixture-backed golden cases.",
   "acceptance_test": "Mutate a fixture file name in a scratch copy; the test must fail."},
  {"severity": "major", "title": "Injection record_warning dedupe has no test: removing the filter at pipeline.py:276 leaves 44 tests green",
   "evidence": "Scratch mutant replacing `fs = [f for f in fs if f[\"type\"] != \"record_warning\"]` with `fs = list(fs)`: test_pipeline.py + test_t037_backend.py 44 passed; case_07 then yields two ('injection_suspected', (3,)) flags (dups found), versus exactly one at HEAD. grep for record_warning in both test files returns no hits. Orchestrator note 01:56:12Z required finalize to dedupe.",
   "why_it_matters": "The duplicate is a user-visible double warning and a double review item for the same record; the only guard is an untested one-line filter.",
   "fix": "Add a test running case_07 (or a tagged-record script) and asserting exactly one record_warning per (category, record_no).",
   "acceptance_test": "The test fails against the `fs = list(fs)` mutant."},
  {"severity": "minor", "title": "Deadline is checked only between stages",
   "evidence": "pipeline.py:212-232: expired() is evaluated in guard() at stage entry only; the flags stage (ThreadPoolExecutor, up to 3 attempts per call with sleeps) and judge_flags run to completion once started.",
   "why_it_matters": "An 8-minute limit can be exceeded by one stage; the run then reports timeout after the fact. This is a design preference, not a spec violation, unless api.md requires a hard cutoff.",
   "fix": "Optionally check expired() per record in the flags stage worker and per call batch.",
   "acceptance_test": "A fake clock that expires mid-flags-stage yields status timeout with only the finished records persisted."}
 ],
 "whats_right": ["Code stages (ingest, gaps, accident-date conflict, amounts) are independent of the LLM and survive every call failing; dropping an entry leaves gaps identical (mutants on gap input and ENDPOINT context are caught).", "CLI output is byte-identical across two runs, ~0.4 s, and no run sets any review_status other than pending; every item has a state and a ladder backend.", "_DB_LOCK is minimal (writes only, non-reentrant, no nesting), and audited_call keeps 1+2 capped retries with a fixture miss final."],
 "questions_for_chris": []}
```
