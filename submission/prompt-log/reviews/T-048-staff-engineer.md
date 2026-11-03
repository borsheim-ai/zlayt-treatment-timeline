# T-048 review - staff-engineer-reviewer (Marcus Lee lens)

Scope: commit 25c8312, red LLM-stage suites (test_provider, test_audited, test_schemas, test_judges, test_flags_sample, test_flags_injection, test_pipeline, `_fakes.py`) and stubs under `app/llm/` and `app/backend/`.

Deterministic run: `.venv/bin/python -m pytest tests/unit -q -k "provider or audited or schemas or judges or flags or pipeline or conflicts or flag_templates"` gives `127 failed, 18 passed, 344 deselected, 4 errors`. Every `E` line is `NotImplementedError` (131 of 131 incl. the 4 setup errors), with no collection errors. Fixture/fake only: grep of the new tests for anthropic, requests, socket, urllib, subprocess, sleep(, time.time and datetime.now found nothing.

The suites are good on the audited-call retry shape and on judge/flag-schema closure. They do not yet encode several of the ACs they exist to pin for T-034 to T-037, and three pipeline assertions pass vacuously. The blocker is the missing wiring test for the grounding verifier: the checklist item 13 and section 5 red flag "tests pass even when the verifier is stubbed out" applies to the pipeline suite.

Spec-constraint findings (blocker or major) are separate from preference findings (minor or nit). The labels are in each finding.

```json
{"card": "T-048", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 25c8312; tests/unit/{test_provider,test_audited,test_schemas,test_judges,test_flags_sample,test_flags_injection,test_pipeline,_fakes}.py + stubs app/llm/*.py app/backend/{flags,judges,pipeline,schemas}.py; sample case via fake call; no app URL",
 "exercised": [
  "python3 tools/board.py show T-048, T-034, T-035, T-036, T-037 (AC text)",
  "git show --stat 25c8312",
  ".venv/bin/python -m pytest tests/unit -q -k \"provider or audited or schemas or judges or flags or pipeline or conflicts or flag_templates\" -> 127 failed, 18 passed, 344 deselected, 4 errors; grep of E lines: all NotImplementedError, no collection errors",
  "read all 7 new test files, _fakes.py, and all 6 stub modules in full",
  "grep for max_retries/timeout/FixtureMissing/non-verbatim across tests/ app/ docs/",
  "grep of new tests for network/clock/sleep imports (none)",
  "read tests/unit/test_grounding.py header and evals/golden/case_07 line 16 to check the injection assertion is real"
 ],
 "verdict": "fail",
 "scores": {"ac_coverage_of_T034_T037": 2, "fixture_only_determinism": 5, "assertion_strength": 2, "stub_signatures": 4, "docstring_citations": 4},
 "findings": [
  {"severity": "blocker", "title": "No pipeline test fails if the grounding/verify stage is removed (T-035 AC2 untested)",
   "evidence": "tests/unit/test_pipeline.py script(): extract returns the golden excerpt verbatim for every record (lines 11-17), so a pipeline that skips `verify` still passes test_nine_entries_all_verified_with_code_set_provider_and_date (line 40). No test seeds a non-verbatim excerpt. `grep -n 'non-verbatim\\|not_verbatim\\|seeded' tests/unit/test_pipeline.py` returns nothing. tests/unit/test_grounding.py only exercises app.backend.grounding in isolation, not its wiring.",
   "why_it_matters": "This is the exact section 5 dealbreaker: tests that pass when the verifier is stubbed out. Rung 1 is the product's anti-fabrication guarantee (R-TL-2); backend can drop the call to the verifier and every suite stays green.",
   "fix": "Add test_pipeline test: extract script returns an excerpt that is not a substring of its record (and one with an invented sentence appended); assert the entry state is needs_review (or rejected) with a reason, it is absent from the verified set, and the J1 call is not what rescued it. Name it so T-035 AC2 can cite it.",
   "acceptance_test": "Comment out the verify call in run_pipeline: the new test fails. Restore: it passes."},
  {"severity": "major", "title": "Fixture-miss contract contradicts T-034 AC8 / T-037 AC7 and uses a different name",
   "evidence": "tests/unit/test_audited.py:56-62 `test_fixture_miss_is_never_retried` asserts `pytest.raises(P.FixtureMiss)` propagates out of audited_call after one attempt. T-034 AC8: 'a fixture miss raises FixtureMissing (logged with the prompt hash); the audited wrapper turns it into LLM_FAILED_AFTER_RETRIES; never a default answer'. app/llm/provider.py:5 defines `FixtureMiss`, not `FixtureMissing`. test_pipeline.py:79-84 expects reason FIXTURE_MISS, not LLM_FAILED_AFTER_RETRIES.",
   "why_it_matters": "qa's tests will force backend to implement the opposite of the written AC (or the AC is stale). The two paths surface different states to the UI and to the eval 'FixtureMissing count' (T-037 AC7). This is a spec divergence, not a style choice. The prompt hash logging from AC8 is also untested.",
   "fix": "Decide which is binding (ask Chris / orchestrator, see questions). Then make the tests, the stub class name, and the AC agree. If AC8 stands: audited_call raises LLMFailed(code=LLM_FAILED_AFTER_RETRIES) on a miss with a logged prompt hash, and the pipeline test expects that reason. If the tests stand: amend T-034 AC8 and T-037 AC7.",
   "acceptance_test": "grep -rn 'FixtureMiss' app tests docs shows one spelling and one documented outcome; a test asserts the logged line contains the prompt hash and no record text."},
  {"severity": "major", "title": "Required provider tests from T-034 are absent (SDK max_retries=0, timeout, single call path, no text in logs, claude-cli argv)",
   "evidence": "`grep -rn max_retries tests/ app/` returns no matches in tests. tests/unit/test_provider.py has 7 tests (hash, hit, miss, meta, invalid recording, no key, recorder). T-034 AC7 names test_provider::test_sdk_no_internal_retry (max_retries=0 and timeout <= 120 s on the constructed client); AC4 claude-cli argv test (pinned --model, no tools/MCP, disableAllHooks, cwd outside project, 120 s timeout, concurrency <= 3); AC5 test_single_call_path and test_no_text_in_logs. None exist. test_provider.py also never asserts a timeout is passed.",
   "why_it_matters": "Checklist 8 (every LLM call has a timeout, retries capped at one layer) is the item most likely to regress silently: an SDK default of 2 internal retries multiplies the audited 1+2 loop into 9 calls and hides failures. The card exists to write these tests first.",
   "fix": "Add the five tests with a mocked SDK class / patched subprocess.run (no network). test_sdk_no_internal_retry should construct the backend client with a fake `anthropic.Anthropic` and assert max_retries == 0 and timeout <= 120. Add a source-scan test that no `anthropic` / `subprocess` import exists outside app/llm/backends.",
   "acceptance_test": "Set max_retries=2 in the backend: test_sdk_no_internal_retry fails."},
  {"severity": "major", "title": "Judge-unavailable -> needs_review is tested only for J1 and only at the judge layer",
   "evidence": "tests/unit/test_judges.py:31 test_j1_unavailable_when_call_fails is the only failure-path test; J2/J3/J4 have none. T-035 AC7 / T-036 AC9: J2 unsure, error or timeout -> needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE), a charge verified only on agree; J3/J4 error -> needs_review JUDGE_UNAVAILABLE. test_pipeline.py script() never makes a judge fail or disagree, so no test shows an entry or amount becoming needs_review with a judge reason (J1 partially/unsupported -> needs_review with reason, T-035 AC3, is also untested; run_j1 returns a bare verdict).",
   "why_it_matters": "The section 5 silent-fallback dealbreaker (judge error marks item verified) has no test guarding it for 3 of 4 judges or at the state-composition level, where the fallback would actually live.",
   "fix": "Parametrize the unavailable/unsure test over run_j2/j3/j4. Add pipeline tests: J1 returns partially -> entry needs_review with a reason; J2 error -> charge amount not verified, JUDGE_UNAVAILABLE; J2 unsure -> JUDGE_UNSURE; J3/J4 error -> flag needs_review JUDGE_UNAVAILABLE.",
   "acceptance_test": "Make run_j2 return 'agree' on exception: new test fails."},
  {"severity": "major", "title": "Vacuous assertions let the outage and fixture-miss tests pass with every entry silently dropped",
   "evidence": "tests/unit/test_pipeline.py:76 `assert not out[\"entries\"] or all(\"LLM_FAILED_AFTER_RETRIES\" in e[\"reasons\"] ...)`; :84 `assert out[\"entries\"] == [] or all(\"FIXTURE_MISS\" in e[\"reasons\"] ...)`; :77 `status in (\"done_with_errors\", \"done\")`.",
   "why_it_matters": "Both tests pass if the pipeline returns no entries and no reason - a lost-facts outcome with a green test. A total LLM outage reporting status 'done' is also the 'no silent failure' case checklist 12 forbids.",
   "fix": "Pick one defined behaviour per scenario (entries absent but a pipeline-level reason/warning code exists, or entries present as needs_review) and assert it; assert status == 'done_with_errors' and that the error code is present at the run level.",
   "acceptance_test": "A stub run_pipeline that returns entries=[], flags from code, status 'done' and no error code fails both tests."},
  {"severity": "major", "title": "Test names cited in the downstream ACs do not exist, and some AC behaviours are untested",
   "evidence": "ACs cite test_generator_schema_minimal (T-035 AC1), test_j1_states (AC3), test_j2_every_amount (AC4), test_flag_schema_no_prose (T-036 AC1), test_stages_and_deadline (T-037 AC3), test_code_stages_without_llm (AC4), test_ladder_and_pending (AC5), test_recorder_refuses_foreign_text (T-034 AC3). `grep -n` of the new files finds none of these names. Behaviours with no test: 'dropping an entry leaves gaps unchanged' (T-037 AC4); ladder record with backend on every LLM-derived item and review_status pending on all (AC5); J2 re-reads every amount incl. rule-made ones (T-035 AC4); distinct causation flags K1-K5 via the one-to-one check_golden matcher (T-036 AC2, test_flags_sample.py `covers` is an any-overlap rule and does not enforce one-to-one); semantic conflict (b) 12-visit plan vs discharge via run_conflict_pass on the sample (test_pipeline script() returns conflicts: [] and J3 is never reached); 'exactly one accident-date conflict flag' (test_pipeline.py:63 only checks presence).",
   "why_it_matters": "Backend cards will claim AC evidence by test name and by behaviour; as written, they either cannot cite a name or will mark ACs done without a test that proves them.",
   "fix": "Rename or alias tests to the AC names (or edit the ACs to the real names - one decision, same commit), and add the missing behaviour tests listed.",
   "acceptance_test": "For each AC that cites a test node id, `pytest <node id> --collect-only` finds it."},
  {"severity": "minor", "title": "Per-record isolation test does not assert exactly one nonce block per prompt",
   "evidence": "tests/unit/test_flags_sample.py:46-53 checks `which_record(p) == [n]` (excerpt substring presence). T-036 AC4 says 'each prompt contains exactly one record nonce block'. test_flags_injection.py asserts a count of '</record-' only in the lookalike test.",
   "why_it_matters": "A prompt that wraps the same record twice, or includes an empty second block, passes today.",
   "fix": "Assert `p.count('<record-') == 1 and p.count('</record-') == 1` for all nine prompts.",
   "acceptance_test": "A flag prompt template that emits two record blocks fails the test."},
  {"severity": "minor", "title": "audited_call stub has no injectable sleep and the audit-row assertions check counts only",
   "evidence": "app/llm/audited.py signature has `now=None` but no sleep/backoff hook; tests/unit/test_audited.py `rows()` only counts llm_calls rows. Nothing asserts each row records backend, pinned model, attempt number or error code (checklist 9, T-034 AC2 'one llm_calls row per attempt, each retry with changed conditions').",
   "why_it_matters": "If backend adds backoff, three-failure tests either slow down or monkeypatch time.sleep globally (Fowler: no bare sleeps). 'One row per attempt' without model/backend/attempt content cannot reproduce a bad run, which is the persona's bad day.",
   "fix": "Add `sleep=` to the signature (default time.sleep) and have tests pass a no-op; assert on the stored rows' model, backend, attempt index and failure code (and that no prompt text appears in the error column).",
   "acceptance_test": "Row for attempt 2 of a 3-attempt failure shows attempt=2 and the error code."},
  {"severity": "nit", "title": "Small stub/test inconsistencies",
   "evidence": "test_flags_sample.py:22 `nothing` is assigned and never used (the lexicon test never involves a model call); test_audited.py uses DB.create_case(now=1.0) while pipeline passes now=callable and audited_call takes `now=None` untyped; provider.LLMResult.cost_usd is a float (not billed money, acceptable, but say so in a comment).",
   "why_it_matters": "Backend will have to guess the clock type for audited_call.",
   "fix": "Document `now` as a callable (or float) once in the stub docstrings; drop the unused variable.",
   "acceptance_test": "n/a"}
 ],
 "whats_right": [
  "Fake call / fixture env only: no network, no key, no wall clock; deadline test uses an injected clock iterator.",
  "test_audited covers 1+2 retries, exactly three attempts with no fourth call, a retry that changes the prompt, schema-invalid counted as a failed attempt, and no record text in output or logs.",
  "Schema tests close the generator and flag outputs (extras rejected, no prose fields, closed flag-type list) and the case_07 record 2 prior-ACL flag is proven to survive an obedient model via the lexicon floor."
 ],
 "questions_for_chris": [
  "On a fixture miss: should audited_call raise FixtureMissing and surface the FIXTURE_MISS reason (as the tests do), or convert it to LLM_FAILED_AFTER_RETRIES (as T-034 AC8 / T-037 AC7 say)? The tests and the AC cannot both stand."
 ]}
```
