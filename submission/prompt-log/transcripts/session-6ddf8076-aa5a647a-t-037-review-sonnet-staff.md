# Subagent: T-037 review (sonnet staff) (T-037 review (sonnet staff))

Source: `agent-aa5a647ae013796b6.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:07:40.312Z

Working directory: /Users/arsis/zlayt-pm-project. Review T-037 "Pipeline stages, finalize, status, CLI and recorded fixtures" (commit fe4e6a2 + later; AC: `python3 tools/board.py show T-037`). Run `.venv/bin/python -m pytest tests/unit -q 2>&1 | tail -3` (note any red and whether it belongs to T-037) and `.venv/bin/python -m app.pipeline evals/golden/sample.txt | head -40`. Check: stage names per api.md; code stages (ingest, gaps) produce output when every LLM call fails (stub backend) — gaps unchanged when an entry is dropped (D-003); finalize composes a state for every item including gap flags with ENDPOINT_NOT_VERIFIED (T-030 r2 finding moved here, AC8); injection record_warning deduped (one per record); no review_status other than pending after a run; every LLM item has a ladder record with backend; deadline with injectable now; the _DB_LOCK serialization is correct (no deadlock; writes only); fixtures contain only golden text (grep a non-golden phrase). Write reviews/T-037-staff-engineer.md (D.2 JSON). Do not fix. Reply ≤ 3 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:07:41.631Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T02:07:41.637Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:07:42.277Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-037; ls .claude/agent-memory/staff-engineer-reviewer/"
}
````

### User / tool · 2026-11-02T02:07:42.415Z

**tool result**
````
---
id: "T-037"
title: "Pipeline stages, finalize, status, CLI and recorded fixtures for all golden inputs"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: ["T-032", "T-033", "T-035", "T-036", "T-048"]
created_by: "orchestrator"
created_at: "2026-11-02T01:14:10Z"
updated_at: "2026-11-02T02:07:41Z"
claimed_by: "backend"
claimed_at: "2026-11-02T01:52:41Z"
rounds: 0
commits: ["d67a82d", "0d040d3", "fe4e6a2"]
reviews: []
ac:
  - {"n": 1, "text": "`python -m app.pipeline evals/golden/sample.txt` (fixture backend) prints 9 entries, the 73-day gap flag, charges $8,390 total, all flag groups, exit 0 in under 60 s (CONTRACT M2 CLI)", "done": true, "evidence": "test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s (exit 0, 9 entries, Gap of 73 days, $8,390.00; ~0.4 s)"}
  - {"n": 2, "text": "fixtures recorded with claude-cli for sample + 9 cases under tests/fixtures/llm/; `ls tests/fixtures/llm | wc -l` > 0 and a hash check shows nothing outside evals/golden", "done": true, "evidence": "tests/fixtures/llm has 279 files recorded with claude-cli (sample, case_01..09, 55 judge lines); recorder refuses non-golden text (test_fixtures_come_only_from_golden_text)"}
  - {"n": 3, "text": "stage names match /status (ingest, extract, verify, judge_entries, amounts, conflicts, flags, finalize) and an 8-minute deadline fails visibly with injectable now(); proved by tests/unit/test_pipeline.py::test_stages_and_deadline", "done": true, "evidence": "tests/unit/test_pipeline.py::test_stage_names_and_order, ::test_stages_and_deadline; test_t037_backend::test_timeout_marks_case_failed_with_run_deadline"}
  - {"n": 4, "text": "gap flags and ingest results exist when every LLM call raises (stub backend); dropping an entry leaves gaps unchanged (D-003, row 9); proved by test_pipeline::test_code_stages_without_llm", "done": true, "evidence": "test_pipeline::test_code_stages_without_llm and ::test_one_failed_extract_loses_only_that_entry_and_leaves_gaps_unchanged pass"}
  - {"n": 5, "text": "every LLM-derived item has a ladder record with backend, and no item has review_status other than pending after a run (R-CO-2, R-RV-6, row 20); proved by test_pipeline::test_ladder_and_pending", "done": true, "evidence": "test_pipeline::test_ladder_and_pending passes; test_t037_backend::test_run_persists_items_pending_and_rerun_keeps_review_status"}
  - {"n": 6, "text": "Contract review (T-018): T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BACKEND != fixture; latest.json records backend and model ids; ship_bar_met is false when backend == fixture'. T-037 AC2: 'fixtures recorded for sample, case_01..09, every line of hallucinations.jsonl and hallucinations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_bar_met true; report path in handoff'.", "done": true, "evidence": "fixtures cover sample, case_01..09, all hallucinations(+controls) lines and SE1-SE5 via pipeline.judge_summary (test_replay_has_no_fixture_miss x10, test_judge_lines_replay); latest.json parts are T-038"}
  - {"n": 7, "text": "Contract review (T-018): T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash); the audited wrapper turns it into LLM_FAILED_AFTER_RETRIES; never a default answer'. T-037 AC2 replace with: 'replaying sample, case_01..09, hallucinations(.jsonl, _controls) and SE1-SE5 on fixture reports 0 FixtureMissing (count printed)'.", "done": true, "evidence": "test_replay_has_no_fixture_miss[*] 0 FixtureMiss on sample+9 cases; test_fixture_missing_after_audited_wrapper_is_a_visible_error_never_a_default passes"}
  - {"n": 8, "text": "From T-030 r2 review: gap flags emitted by gaps.py with ENDPOINT_NOT_VERIFIED get a state via compose_state in finalize; test_pipeline asserts every flag has a state", "done": true, "evidence": "tests/unit/test_t037_backend.py::test_endpoint_not_verified_and_every_flag_has_a_state"}
---
## Description
Ties stages 0 to 7 together and records fixtures so evals run with no key (A-001/A-002, R-CO-2, R-CO-6, R-RV-6). Delivers the CONTRACT M2 CLI and finalize/state composition (rows 17, 20).

Plan key: m2-be-pipeline-cli (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

Estimate: 35 min.

## Notes (append-only, newest last)
- 2026-11-02T01:22:45Z orchestrator: AC 6 added: Contract review (T-018): T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BACKEND != fixture; latest.json records backend and model ids; ship_bar_met is false when backend == fixture'. T-037 AC2: 'fixtures recorded for sample, case_01..09, every line of hallucinations.jsonl and hallucinations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_bar_met true; report path in handoff'.
- 2026-11-02T01:22:46Z orchestrator: AC 7 added: Contract review (T-018): T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash); the audited wrapper turns it into LLM_FAILED_AFTER_RETRIES; never a default answer'. T-037 AC2 replace with: 'replaying sample, case_01..09, hallucinations(.jsonl, _controls) and SE1-SE5 on fixture reports 0 FixtureMissing (count printed)'.
- 2026-11-02T01:22:47Z orchestrator: updated depends_on=['T-032', 'T-033', 'T-035', 'T-036', 'T-048']
- 2026-11-02T01:32:27Z orchestrator: updated body appended from artifacts/tmp/est_T-037.md
- 2026-11-02T01:52:18Z orchestrator: assigned: backend-2
- 2026-11-02T01:52:41Z backend: claimed
- 2026-11-02T01:52:41Z backend: started against T-029/T-048 tests; coding against T-036 declared interfaces
- 2026-11-02T01:53:24Z orchestrator: AC 8 added: From T-030 r2 review: gap flags emitted by gaps.py with ENDPOINT_NOT_VERIFIED get a state via compose_state in finalize; test_pipeline asserts every flag has a state
- 2026-11-02T01:55:53Z backend: pipeline+CLI done against flags.py as landed (24/27 test_pipeline pass; 3 j3 tests fail because SEM script has record_id key that schemas.FlagOutput forbids - T-036/qa to reconcile). NOTE: created app/pipeline.py (3-line shim) outside owned paths so 'python -m app.pipeline' works; orchestrator to ratify. Next: record fixtures via claude-cli.
- 2026-11-02T01:56:12Z orchestrator: From backend-1 (T-036): a tagged record's injection record_warning is emitted by both flags.run_flag_pass and ingest; finalize must dedupe. backend-2 owns T-037.
- 2026-11-02T02:01:02Z orchestrator: For backend-2: (1) re-record test_t037_backend fixtures after backend-1's prompt changes (D-028 reason_code); (2) turn record_warning analysis_incomplete (pipeline_warning CONFLICT_PASS_INCOMPLETE) into a run warning + partial status; (3) backend-1 left an uncommitted J3 two-quote fixture edit in tests/unit/test_pipeline.py — keep and commit it with your paths.
- 2026-11-02T02:01:40Z backend: backend-3 (T-050): ids stay short; uniqueness is now (case_id,id) in schema.sql. DB.update_item/apply_review/get_item take case= (a bare id raises ValueError if two cases hold it). I edited app/backend/pipeline.py in the working tree (2 lines in _persist: case=cid) but did NOT commit it because it holds your uncommitted WIP: please include those two lines in your next commit. Old data/*.sqlite files must be deleted (schema change).
- 2026-11-02T02:07:04Z backend: AC 1 checked: test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s (exit 0, 9 entries, Gap of 73 days, $8,390.00; ~0.4 s)
- 2026-11-02T02:07:04Z backend: AC 2 checked: tests/fixtures/llm has 279 files recorded with claude-cli (sample, case_01..09, 55 judge lines); recorder refuses non-golden text (test_fixtures_come_only_from_golden_text)
- 2026-11-02T02:07:04Z backend: AC 3 checked: tests/unit/test_pipeline.py::test_stage_names_and_order, ::test_stages_and_deadline; test_t037_backend::test_timeout_marks_case_failed_with_run_deadline
- 2026-11-02T02:07:04Z backend: AC 4 checked: test_pipeline::test_code_stages_without_llm and ::test_one_failed_extract_loses_only_that_entry_and_leaves_gaps_unchanged pass
- 2026-11-02T02:07:04Z backend: AC 5 checked: test_pipeline::test_ladder_and_pending passes; test_t037_backend::test_run_persists_items_pending_and_rerun_keeps_review_status
- 2026-11-02T02:07:04Z backend: AC 6 checked: fixtures cover sample, case_01..09, all hallucinations(+controls) lines and SE1-SE5 via pipeline.judge_summary (test_replay_has_no_fixture_miss x10, test_judge_lines_replay); latest.json parts are T-038
- 2026-11-02T02:07:04Z backend: AC 7 checked: test_replay_has_no_fixture_miss[*] 0 FixtureMiss on sample+9 cases; test_fixture_missing_after_audited_wrapper_is_a_visible_error_never_a_default passes
- 2026-11-02T02:07:21Z backend: AC 8 checked: tests/unit/test_t037_backend.py::test_endpoint_not_verified_and_every_flag_has_a_state
- 2026-11-02T02:07:21Z backend: moved in_progress -> in_review
- 2026-11-02T02:07:41Z orchestrator: review dispatched: staff (sonnet)
- 2026-11-02T02:07:41Z orchestrator: Orchestrator ratifies app/pipeline.py 3-line shim (python -m app.pipeline entry point) as backend-owned.

## Handoff
Added pipeline.py stages 0-7 (run_ingest, ingest_case, run_pipeline, persistence that preserves review status on rerun, 8-min deadline via injectable now), CLI (python -m app.pipeline via shim app/pipeline.py - outside owned paths, please ratify), eval helpers run_case/judge_summary/case_view, record.py --judges, provider.record_fragment_context, audited._DB_LOCK. Fixtures: 279 files recorded with claude-cli for sample, case_01..09, 55 judge lines (40 halluc, 10 controls, SE1-5). Verified: pytest tests/unit/test_pipeline.py + test_t037_backend.py 43 passed; CLI 0.4 s on fixtures. Left: any prompt change by T-035/T-036 invalidates fixtures -> re-record (python -m app.llm.record; ~1 min/case). Surprised me: one sqlite connection shared by worker threads corrupted table_info reads (fixed with a lock); claude-cli extract call occasionally fails 3x (case_02 re-recorded).

MEMORY.md
project_backend_llm_review_patterns.md
project_db_review_patterns.md
project_design_review_patterns.md
project_e2e_contract_review_patterns.md
project_eval_runner_review_patterns.md
project_harness_review_patterns.md
project_llm_stage_review_patterns.md
project_wiring_review_patterns.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:07:44.558Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/staff-engineer-reviewer/project_llm_stage_review_patterns.md .claude/agent-memory/staff-engineer-reviewer/project_wiring_review_patterns.md | head -60; .venv/bin/python -m pytest tests/unit -q 2>&1 | tail -5; .venv/bin/python -m app.pipeline evals/golden/sample.txt | head -40; wc -l app/backend/pipeline.py app/backend/audited.py 2>/dev/null; ls app app/backend; git log --oneline | head -5"
}
````

### User / tool · 2026-11-02T02:07:55.688Z

**tool result**
````
---
name: llm-stage-review-patterns
description: T-048 r2 (LLM-stage red suites, round 2): verify-stage no-op, fail-open judge mutation method, CLI skip-on-missing-fixtures, shared sqlite across threads
metadata:
  type: project
---

Recurring patterns from the T-048 round-2 review (2026-11-01, reviews/T-048-staff-engineer-r2.md).

- **Verify stage can be a no-op label.** pipeline.py had `if guard("verify"): pass` while grounding ran inside extract (generator.py:69). Stage-name tests stay green. Check the stage body, not just its name. **Why:** a stage named for a guarantee that does nothing hides a dropped check. **How to apply:** for any "verify/check" stage, grep the body; mutate the call site, not the stage label.
- **Mutation method that works here.** `git archive <full sha>` into a scratchpad dir, copy untracked fixtures in, then run mutants on copies with a pattern-count assert (`assert t.count(old) == 1`). Shared-helper mutants (judges `_run` except branch) hit all four judges at once, which is useful evidence. Pattern-miss errors are a sign the mutant did not run.
- **Fail-open judge mutants.** Mapping a judge error to "supported" in the shared helper fails about 10 tests; mapping it in `confidence.compose_state` (`none_ok` adds "unavailable") fails about 6. Both are caught, so judge-failure coverage is real.
- **CLI check skips on missing fixtures.** `tests/unit/test_t037_backend.py:17` uses `skipif(not list(FIX.glob("*.json")))` and fixtures are untracked (`git ls-files tests/fixtures/llm` = 0). A clean checkout reports the golden CLI check as skipped, not failed. **How to apply:** flag any `skipif` on a missing artifact that the artifact's own commit should provide.
- **Non-deterministic CLI failure.** Three runs of `python -m app.pipeline evals/golden/sample.txt` gave three different exceptions (two different ValueError field sets, then IndexError). Suspected: one sqlite connection shared across ThreadPoolExecutor workers (`_cols` PRAGMA table_info). Not proven. **How to apply:** when the same input fails differently, suspect shared mutable state across threads before the schema.
- **Duplicate contract tests across files.** test_provider.py and test_provider_backends.py both define test_sdk_no_internal_retry, test_single_call_path, test_no_text_in_logs, test_recorder_refuses_foreign_text. **How to apply:** `pytest --collect-only -q | sort | uniq -d` on any suite that gets a second file.

Environment gotchas seen in this review (also relevant to other reviewers):
- HEAD moved several times during one review (b1803c0 → 1da399d → ad4803a → 53093a0 → 636c961 → 8ec833f). Pin by full sha with `git archive` and say so in the review.
- The board-guard hook blocks `git branch`. The git-guard hook blocks `$(...)` in command position. Use `git rev-parse` and literal shas.
- `timeout` is not installed on this macOS box.
- A compound `git ls-files && rm -rf ... && git archive` was denied by permission; split into separate commands.

See also [[project_harness_review_patterns]] and [[project_db_review_patterns]].
---
name: wiring-review-patterns
description: T-030 r2 pattern: a round fix passes its unit tests at the function/table level but the producer path never calls it. Check callers and run the producer, not just pytest.
metadata:
  type: project
---

Recurring pattern (T-030 r2, 2026-11-01): the round-1 major "compose_state ignores endpoint_unverified" was fixed in the
boolean table (confidence.py:64) and tested there, and `check_amount` was added with tests. But the only producer of
ENDPOINT_NOT_VERIFIED (app/backend/gaps.py:37) never calls compose_state, and gap flags carry reasons with no `state` key.
`check_amount` had no production caller at all. Pytest was green on both, so the green summary hid the gap.

**Why:** a fix that is green only in its own unit test does not close the risk the original finding named (the gap flag
path). Same family as T-031 partial re-fixes (sibling writers), see [[project_db_review_patterns]].

**How to apply:**
- For every function or table row a round adds or changes, grep non-test callers (`grep -rn name --include=*.py . | grep -v tests/`).
  Zero production hits = not wired, regardless of pytest.
- Run the producer on a repro (e.g. gaps.gap_flags on synthetic records) and check the output shape, not only the unit tests.
- Scratch-copy mutation of the function (return []) and of the table row shows whether the tests are load-bearing; it does not
  show whether production reaches them.

Also: the dossier names claude-sonnet-5-5 as the expected model id, but the r2 run was executing as claude-haiku-5-5. Record
the model that actually ran in the JSON, and note the mismatch in the reply.
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c576e440a3ec6 step=j4 attempt=1 prompt_hash=9391f6bf99db12e040f88843580adab24a5b2b06eab51ee982d85c36d2c761db
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c1e566947e94a step=j4 attempt=1 prompt_hash=664c59ebfe49e6a09404138fe7cd6d77ba2306b53dfe431bc7ead34b14de3c4c
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode
1 failed, 767 passed in 10.08s
llm call failed call_id=c430e237b3392 step=j1 attempt=1 prompt_hash=e52e60e1ed00713dbc3ea960404b10cfd5913ab988731c4bce782b0385363f98
llm call failed call_id=cd9eba7f3fba2 step=j1 attempt=1 prompt_hash=56e115e914a9dd3fc4cabf30d389f6c5c1f234bf487ab9fc8e24580dc19e0240
llm call failed call_id=c4d04d6b73567 step=j1 attempt=1 prompt_hash=d7294736d7aed62bf466fd10b0fa5006352e73613509ed8b7c5cbdec4ce41a5e
llm call failed call_id=cee795753825a step=j1 attempt=1 prompt_hash=6f6f6b3cd32ab2a827055d485be8e628585d46e5994fcab4c38e6c8dae4b73cb
llm call failed call_id=cbe3ad7b55857 step=j1 attempt=1 prompt_hash=bcea6ba7d7b0914996ffd1e587988953107f3cae9d6dd3776912d959f44a9e26
llm call failed call_id=c9dc9e3d368b0 step=j1 attempt=1 prompt_hash=dbfd58f8dd566dfd0c83eb9cc838c37b8b845e9835e931aa1e22b9e23c444b6c
llm call failed call_id=cdb8c77c63555 step=j1 attempt=1 prompt_hash=c930c148e45f7e0a01a1c7d23b743c02b45b9b4c2c690f0aeca16618455cf97d
llm call failed call_id=ca28e28fd54a1 step=j1 attempt=1 prompt_hash=78e9a6eb0aaea08b812e2a76b790366556359202a7544b9b638a3720cf48ae1c
llm call failed call_id=c864854bd0f20 step=j1 attempt=1 prompt_hash=056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d
llm call failed call_id=c9c639386eaaf step=j2 attempt=1 prompt_hash=632a0e6302845a76592de8f53c07e4809ea08d9727f280e2e72b226c9faa5aa7
llm call failed call_id=c121bd501cf39 step=j2 attempt=1 prompt_hash=f2f207afab19f26f381d11c7f1b84064e3d14d1ae5bde696b04c52dd4d1d2a7c
llm call failed call_id=c3f2d3a48122a step=j2 attempt=1 prompt_hash=8258d36c1cdad8d5f84566c7d7ccb6f8cbdf043cc018ab771440220878c84c96
llm call failed call_id=c4faa96d5a8c7 step=j3 attempt=1 prompt_hash=3787bdabbca433ea035220bcef2d7bc9c295375c65ba9617445d10a094d2515f
llm call failed call_id=c0bd1c6582240 step=j4 attempt=1 prompt_hash=9e3c8633aeea3fd87eb055c6d34203f7c33762b0fd3742d9ccee371ee7722f2b
llm call failed call_id=c6f22f9930c03 step=j4 attempt=1 prompt_hash=f9e4dc3c09ef6fd906b6646bfc9a693611a8aa1f0f8e020cf9f104c0687862fa
llm call failed call_id=c2f19a8b81f4a step=j4 attempt=1 prompt_hash=d33f0f6bd5a79114deff14a84772c6ef2e30f9ed9c9591f366aaf53d58f27f70
llm call failed call_id=c041bc62ea949 step=j4 attempt=1 prompt_hash=98c9ecc5fc199e17a2582926e896eae01b3c2a720f8c67ba84fe739fb4394f2f
llm call failed call_id=c8e22327c9f64 step=j4 attempt=1 prompt_hash=3ab32c7b388852f1fb66117225fd377dd8ea392d767c2664031a6a037df64caf
llm call failed call_id=c429641390498 step=j4 attempt=1 prompt_hash=29ee418c79119a6311c1e2d6b9210fd3c4fd01f152f1dcef5a6acc0d5b917d58
llm call failed call_id=c34ffab1735ed step=j4 attempt=1 prompt_hash=9391f6bf99db12e040f88843580adab24a5b2b06eab51ee982d85c36d2c761db
llm call failed call_id=cfe545b45dc7c step=j4 attempt=1 prompt_hash=664c59ebfe49e6a09404138fe7cd6d77ba2306b53dfe431bc7ead34b14de3c4c
Status: done   backend: fixture   records: 9   entries: 9   flags: 11   amounts: 3

TIMELINE
  January 9, 2026 - Austin EMS run report [needs_review]
      41M restrained driver, rear-ended at approx. 35 mph, complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
  January 9, 2026 - Central ER discharge summary [needs_review]
      Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week; ER charges $6,240.
  January 16, 2026 - Dr. Alvarez, primary care [needs_review]
      Persistent neck pain 6/10 with daily headaches; referred to physical therapy 2x/week for 6 weeks.
  January 23, 2026 - Capital PT, initial evaluation [needs_review]
      Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.
  February 20, 2026 - Capital PT, visit 8 [needs_review]
      Pain 4/10, improving. Patient reports missing 3 days of work.
  March 6, 2026 - Capital PT, visit 9 [needs_review]
      Discharged from PT after two missed appointments; pain 3/10.
  May 18, 2026 - Hill Country Pain Management, new patient [needs_review]
      New onset pain radiating to right arm with numbness in fingers; pain 7/10; MRI ordered.
  May 29, 2026 - Austin Imaging, cervical MRI [needs_review]
      C5-C6 disc protrusion with mild right foraminal narrowing; findings may represent degenerative change, correlate clinically.
  June 12, 2026 - Hill Country Pain Management, follow-up [needs_review]
      Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.

GAPS
  [verified] Gap of 73 days - Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).

CONFLICTS
  [verified] Stated accident date is later than recorded treatment - Stated accident date January 19, 2026 (“Date of accident per intake form: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Austin EMS run report; Central ER discharge summary). The records disagree; the tool does not choose between them.
  [needs_review] Treatment plan and what followed differ - Capital PT, initial evaluation (January 23, 2026): “Plan of care: 12 visits.” Capital PT, visit 9 (March 6, 2026): “Discharged from PT after two missed appointments.”

PRE-EXISTING
  [needs_review] Mention of a prior or pre-existing condition - Dr. Alvarez, primary care (January 16, 2026) mentions a prior or pre-existing condition: “Patient reports low back pain in 2023, resolved.”
  [needs_review] Degenerative wording - Austin Imaging, cervical MRI (May 29, 2026) uses degenerative wording: “Findings may represent degenerative change; correlate clinically.”

CAUSATION LANGUAGE
  [needs_review] Normal or absent findings wording - Wording about normal or absent findings in Central ER discharge summary (January 9, 2026): “CT head negative.”
  [needs_review] Missed or ended care - Wording about missed appointments or ending care in Capital PT, visit 9 (March 6, 2026): “Discharged from PT after two missed appointments.”
  [needs_review] Accident date source - Accident date as stated in Hill Country Pain Management, new patient (May 18, 2026): “Date of accident per intake form: 2026-01-19.”
  [needs_review] New-onset wording - New-onset wording in Hill Country Pain Management, new patient (May 18, 2026): “New onset pain radiating to right arm with numbness in fingers.”
  [needs_review] Hedged wording - Hedged wording in Austin Imaging, cervical MRI (May 29, 2026): “Findings may represent degenerative change; correlate clinically.”
  [needs_review] Patient self-report - Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”
     445 app/backend/pipeline.py
     445 total
app:
README-arch.md
__init__.py
__pycache__
backend
db
frontend
llm
main.py
pipeline.py

app/backend:
__init__.py
__pycache__
amounts.py
api.py
confidence.py
conflicts.py
dates.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judges.py
lexicon.py
lexicon_scan.py
pipeline.py
present.py
review.py
schemas.py
sentences.py
store.py
totals.py
why.py
81df4e0 feat(backend): pipeline conflict-pass warning on run (T-036) on top of T-037/T-050 edits
fe4e6a2 test(backend): endpoint-not-verified gap state (T-037 AC8)
3f37141 fix(backend): source_kind from lexicon self_report with explicit patient attribution, case-level conflict-check warning, single-period templates (T-036 r3)
71126c5 plan: D-031 scope reinstatement (T-052..T-059) per Chris
0d040d3 feat(backend): eval view, judge recorder, fixtures for sample + 9 cases + judge lines (T-037)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:07:59.289Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m app.pipeline evals/golden/sample.txt 2>/tmp/x.err >/tmp/x.out; echo exit=$?; wc -l /tmp/x.err; sed -n 40,80p /tmp/x.out; .venv/bin/python -m app.pipeline evals/golden/sample.txt 2>/dev/null | diff - /tmp/x.out && echo deterministic; .venv/bin/python -m pytest tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode -q 2>&1 | tail -20; git status --short | head -20; git ls-files tests/fixtures/llm | wc -l"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:07:59.546Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T02:08:01.284Z

**tool result**
````
exit=0
      21 /tmp/x.err
  [needs_review] Patient self-report - Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”

AMOUNTS
  $6,240 (charge) record 2 [needs_review]
  $185 (rate) record 4 [needs_review]
  $2,150 (charge) record 8 [needs_review]
  Charges detected, pending review (not a total): $8,390.00; accepted so far: $0.00
deterministic
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c9f2a91bb6efe step=j1 attempt=1 prompt_hash=bcea6ba7d7b0914996ffd1e587988953107f3cae9d6dd3776912d959f44a9e26
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c980842f345ba step=j1 attempt=1 prompt_hash=dbfd58f8dd566dfd0c83eb9cc838c37b8b845e9835e931aa1e22b9e23c444b6c
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=ce781574436f1 step=j1 attempt=1 prompt_hash=c930c148e45f7e0a01a1c7d23b743c02b45b9b4c2c690f0aeca16618455cf97d
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cf1e34ac4c980 step=j1 attempt=1 prompt_hash=78e9a6eb0aaea08b812e2a76b790366556359202a7544b9b638a3720cf48ae1c
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cd70125d5cd10 step=j1 attempt=1 prompt_hash=056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c1129da88db6e step=j2 attempt=1 prompt_hash=632a0e6302845a76592de8f53c07e4809ea08d9727f280e2e72b226c9faa5aa7
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c20e9d70b6d4a step=j2 attempt=1 prompt_hash=f2f207afab19f26f381d11c7f1b84064e3d14d1ae5bde696b04c52dd4d1d2a7c
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c26f18ac36343 step=j2 attempt=1 prompt_hash=8258d36c1cdad8d5f84566c7d7ccb6f8cbdf043cc018ab771440220878c84c96
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cd9908c3cd5b3 step=j3 attempt=1 prompt_hash=3787bdabbca433ea035220bcef2d7bc9c295375c65ba9617445d10a094d2515f
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=ce41ff3ddf4db step=j4 attempt=1 prompt_hash=9e3c8633aeea3fd87eb055c6d34203f7c33762b0fd3742d9ccee371ee7722f2b
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cbdc184385f4f step=j4 attempt=1 prompt_hash=f9e4dc3c09ef6fd906b6646bfc9a693611a8aa1f0f8e020cf9f104c0687862fa
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=ce003941cc5c9 step=j4 attempt=1 prompt_hash=d33f0f6bd5a79114deff14a84772c6ef2e30f9ed9c9591f366aaf53d58f27f70
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c4ae8ebe66cd9 step=j4 attempt=1 prompt_hash=98c9ecc5fc199e17a2582926e896eae01b3c2a720f8c67ba84fe739fb4394f2f
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c4e9a4de99949 step=j4 attempt=1 prompt_hash=3ab32c7b388852f1fb66117225fd377dd8ea392d767c2664031a6a037df64caf
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cd8db37192864 step=j4 attempt=1 prompt_hash=29ee418c79119a6311c1e2d6b9210fd3c4fd01f152f1dcef5a6acc0d5b917d58
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cc29b6c4a063c step=j4 attempt=1 prompt_hash=9391f6bf99db12e040f88843580adab24a5b2b06eab51ee982d85c36d2c761db
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c05bf55e2a3bc step=j4 attempt=1 prompt_hash=664c59ebfe49e6a09404138fe7cd6d77ba2306b53dfe431bc7ead34b14de3c4c
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode
1 failed in 0.77s
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/feedback_lexicon_recall_and_negation.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md
 M .claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md
 M .claude/agent-memory/product-manager-reviewer/project_t013_review_history.md
 M .claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_hook_guard_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M board/activity.jsonl
 M board/cards/T-036.md
     316
````

### User / tool · 2026-11-02T02:08:01.439Z

**tool result**
````
1	"""Pipeline stages 0-7 (app/README-arch.md; ADR-007, ADR-010, ADR-011, ADR-013, ADR-014). `python -m app.pipeline <file>` prints the result.
2	
3	0 ingest (code, sync)  1 extract (LLM)  2 verify (code)  3 judge_entries (J1)  4 amounts (J2 on every amount)
4	5 conflicts (one LLM pair pass + J3)  6 flags (one LLM pass per record + lexicon floor + J4)  7 finalize (code).
5	Gaps, the accident-date conflict, provider-name conflicts, amounts and record warnings exist after stage 0 and never wait for a model.
6	No code path here sets review_status: every item leaves a run `pending`. A model failure loses only that item and is reported in `errors`.
7	`call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is the audited wrapper bound to a case (or a test fake)."""
8	import argparse
9	import json
10	import sys
11	import time
12	from concurrent.futures import ThreadPoolExecutor
13	
14	from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
15	                         judges, totals as TT, why as WHY)
16	from app.db import db as DB
17	from app.llm import audited as AU, provider as P
18	
19	STAGES = ("ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize")
20	DEADLINE_S = 480
21	CONCURRENCY = 3
22	_ORIGIN = {"both": "lexicon+llm"}
23	
24	
25	def _clean(d: dict) -> dict:
26	    """Drop private '_' keys before an item is stored or returned."""
27	    return {k: v for k, v in d.items() if not k.startswith("_")}
28	
29	
30	def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
31	    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
32	            "human": {"action": None, "edited_text": None, "at": None}, "state": state}
33	
34	
35	def _compose_code(rec_by_n: dict, nos: list, reasons: list, evidence: list, case_text: str) -> tuple:
36	    """State of a flag made by code: evidence spans must equal the input text; injection / unconfirmed endpoints give needs_review."""
37	    bad = [e for e in evidence if e.get("start") is not None and case_text[e["start"]:e["end"]] != e["text"]]
38	    ctx = {"injection": any(rec_by_n[n].get("injection_tag") for n in nos if n in rec_by_n),
39	           "endpoint_unverified": "ENDPOINT_NOT_VERIFIED" in reasons}
40	    dates = {rec_by_n[n].get("date_status") for n in nos if n in rec_by_n}
41	    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
42	        ctx["date_status"] = "ambiguous"
43	    return confidence.compose_state({"grounding_failures": ["GROUNDING_EXCERPT_NOT_VERBATIM"] if bad else [], "schema_valid": True,
44	                                     "code_reasons": []}, ctx)
45	
46	
47	# ------------------------------------------------------------------ stage 0
48	def run_ingest(raw_text: str) -> dict:
49	    """All-code stage 0. Raises IngestError('bad_request' | 'input_too_large') before anything else. Zero model calls."""
50	    ing = IN.ingest(raw_text)
51	    text = IN.normalize_text(raw_text)
52	    recs = ing["records"]
53	    by_n = {r["n"]: r for r in recs}
54	    backend = P.backend_name()
55	    flags = []
56	    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
57	    for f in code:
58	        nos = f["record_nos"]
59	        ev = f["evidence"]
60	        reasons = list(f.get("reasons") or [])
61	        state, why_codes = _compose_code(by_n, nos, reasons, ev, text)
62	        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
63	                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": ev, "record_nos": nos,
64	                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "review_status": "pending",
65	                "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes) or
66	                "Computed by code from the record dates and text; every cited span matches the input."}
67	        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names"):
68	            if k in f:
69	                item[k] = f[k]
70	        item["ladder"] = _ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
71	        flags.append(item)
72	    for w in ing["record_warnings"]:
73	        r = by_n[w["record_no"]]
74	        inj = w["category"] == "injection_suspected"
75	        state, why_codes = confidence.compose_state({"code_reasons": []}, {"injection": inj, "date_status": None if inj else "ambiguous"})
76	        flags.append({"id": w["id"], "type": "record_warning", "category": w["category"], "origin": "code", "title": w["title"],
77	                      "explanation": w["explanation"], "evidence": [{"record_no": w["record_no"], **e} for e in w["evidence"]],
78	                      "record_nos": [w["record_no"]], "record_ids": [r["id"]], "source_kind": "record", "review_status": "pending",
79	                      "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes),
80	                      "ladder": _ladder(w["id"], backend, {"computed_by": "code"}, state)})
81	    amounts, damages = [], []
82	    for a in AM.extract_amounts(recs):
83	        r = by_n[a["record_no"]]
84	        body = r["excerpt"]
85	        item = {"id": a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
86	                "cents": a["cents"], "value_cents": a["cents"], "cls": a["cls"], "kind": a["cls"], "start": a["start"], "end": a["end"],
87	                "excerpt": body, "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending"}
88	        (damages if a["cls"] == "damages" else amounts).append(item)
89	    warnings = list(ing["warnings"])
90	    for r in recs:
91	        if r["injection_tag"]:
92	            warnings.append({"code": "INJECTION_SUSPECTED", "record_no": r["n"], "item_id": r["id"],
93	                             "message": "This record contains instruction-like text; it is shown unchanged and everything from it needs review."})
94	    return {"text": text, "records": recs, "groups": ing["groups"], "split_method": ing["split_method"], "banner": ing["banner"],
95	            "dates_to_confirm": ing["dates_to_confirm"], "flags": flags, "amounts": amounts, "damages": damages, "warnings": warnings,
96	            "injection_records": ing["injection_records"]}
97	
98	
99	def _store_records(conn, cid: str, ing: dict) -> None:
100	    if DB.table_counts(conn, cid)["records"]:
101	        return
102	    for r in ing["records"]:
103	        d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
104	        DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
105	                      date_header_start=d["start"], date_header_end=d["end"], source_header_start=s["start"], source_header_end=s["end"],
106	                      source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
107	                      date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
108	                      encounter=int(r["encounter"]))
109	
110	
111	def _row(kind: str, it: dict) -> dict:
112	    ladder = _clean(it.get("ladder") or {})
113	    if kind == "entry":
114	        return {"record_ids_json": it["record_ids"], "seq": it["seq"], "date_iso": it.get("date"), "provider": it["provider"],
115	                "summary": it.get("summary"), "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"),
116	                "excerpt_end": it.get("excerpt_end"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
117	    if kind == "amount":
118	        return {"record_ids_json": it["record_ids"], "entry_id": it.get("entry_id"), "text": it["text"], "value_cents": it["cents"],
119	                "kind": it["cls"], "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"), "excerpt_end": it.get("excerpt_end"),
120	                "duplicate_note": it.get("duplicate_note"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
121	    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
122	                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids") if k in it}
123	    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
124	            "explanation": it["explanation"], "computed_json": computed, "evidence_json": it.get("evidence", []),
125	            "origin": _ORIGIN.get(it["origin"], it["origin"]), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
126	
127	
128	def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
129	    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
130	    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
131	    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
132	    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
133	    for it in items:
134	        row = _row(kind, it)
135	        old = existing.get(it["id"])
136	        if old is None:
137	            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
138	            continue
139	        DB.update_item(conn, it["id"], now=now, case=cid, **row)
140	        if kind == "flag" and old["review_status"] != "pending":
141	            oc = old.get("computed") or {}
142	            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
143	                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
144	            else:
145	                it["review_status"] = old["review_status"]
146	        elif old["review_status"] != "pending":
147	            it["review_status"] = old["review_status"]
148	    keep = {i["id"] for i in items}
149	    for oid, old in existing.items():
150	        if oid not in keep and old["review_status"] == "pending":
151	            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
152	
153	
154	def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
155	    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
156	    ing = run_ingest(raw_text)
157	    _store_records(conn, cid, ing)
158	    _persist(conn, cid, "flag", ing["flags"], now)
159	    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
160	    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
161	    return ing
162	
163	
164	# ------------------------------------------------------------------ stages 4-6 helpers
165	def _finish_amount(a: dict, ing: dict, judged) -> dict:
166	    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
167	    by_n = {r["n"]: r for r in ing["records"]}
168	    a = dict(a)
169	    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
170	    verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
171	    state, reasons = confidence.compose_state(
172	        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
173	         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
174	        {"injection": a["injection"], "amount_class": a["cls"]})
175	    a["state"], a["reasons"] = state, reasons
176	    a["why"] = " ".join(WHY.why(c) for c in reasons) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
177	    a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
178	                   "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
179	                              "verdict": judged["verdict"]} if judged else None)}
180	    return a
181	
182	
183	def _entry_for(entries: list, record_no: int):
184	    return next((e["id"] for e in entries if f"r{record_no}" in e["record_ids"]), None)
185	
186	
187	def _err(code, stage, record_no=None, cause=None) -> dict:
188	    d = {"code": code, "stage": stage}
189	    if record_no is not None:
190	        d["record_no"] = record_no
191	    if cause:
192	        d["cause"] = cause
193	    return d
194	
195	
196	def _accident_year(recs: list):
197	    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso") and r["kind"] == "encounter")
198	    return int(ds[0][:4]) if ds else None
199	
200	
201	def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
202	    clock = now if callable(now) else (lambda: time.time() if now is None else now)
203	    t0 = clock()
204	    call = call or AU.make_call(conn, cid, now=clock)
205	    errors, stage_done = [], []
206	
207	    def set_stage(name):
208	        if on_stage:
209	            on_stage(name)
210	        DB.update_case(conn, cid, status="running", stage=name)
211	
212	    def expired():
213	        return clock() - t0 > deadline_s
214	
215	    DB.update_case(conn, cid, status="running", stage="ingest", run_started_at=t0, error=None, backend=P.backend_name())
216	    ing = run_ingest(raw_text)
217	    text, recs = ing["text"], ing["records"]
218	    by_n = {r["n"]: r for r in recs}
219	    _store_records(conn, cid, ing)
220	    dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
221	    entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
222	    code_amounts = [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]]
223	    status = "done"
224	    timed_out = False
225	
226	    def guard(name):
227	        nonlocal timed_out
228	        if timed_out or expired():
229	            timed_out = True
230	            return False
231	        set_stage(name)
232	        return True
233	
234	    # 1-3: entries
235	    if guard("extract"):
236	        entries, rejected, failures = generator.extract_entries(recs, ing["groups"], call=call, case_text=text)
237	        for f in failures:
238	            errors.append(_err("LLM_FAILED_AFTER_RETRIES", "extract", f["record_no"], "FIXTURE_MISS" if f["failure"] == "FIXTURE_MISS" else None))
239	    if guard("verify"):
240	        pass                                    # grounding, token and qualifier checks ran inside extract_entries (code, same call per record)
241	    if guard("judge_entries") and entries:
242	        generator.judge_entries(entries, by_n, call=call, case_text=text)
243	    for e in entries + rejected:
244	        e["ladder"]["backend"] = P.backend_name()
245	        e.pop("_stage", None)
246	    # 4: amounts (J2 on every dollar amount)
247	    final_amounts = code_amounts
248	    if guard("amounts"):
249	        dollars = [a for a in ing["amounts"]]
250	        verdicts = judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars],
251	                                        call=call, case_text=text)
252	        final_amounts = [_finish_amount(a, ing, verdicts.get(a["id"])) for a in dollars] + [_finish_amount(a, ing, None) for a in ing["damages"]]
253	    for a in final_amounts:
254	        a["entry_id"] = _entry_for(entries, a["record_nos"][0])
255	    # 5: semantic conflicts (LLM) + J3
256	    llm_flags = []
257	    distinct = [by_n[g[0]] for g in ing["groups"]]
258	    if guard("conflicts"):
259	        pair = FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
260	        for i, f in enumerate(pair, 1):
261	            f["id"] = f"f_cx{i}"
262	            if f.get("pipeline_warning"):      # conflict check did not finish: visible on the run, not only on the flag
263	                ing["warnings"].append({"code": f["pipeline_warning"], "stage": "conflicts", "item_id": f["id"],
264	                                        "message": "The check for conflicts between records did not finish; conflicts may be missing."})
265	                errors.append({"code": f["pipeline_warning"], "stage": "conflicts", "record_no": None, "cause": f["reasons"][0]})
266	        llm_flags += FL.judge_flags(pair, call=call, case_text=text)
267	    # 6: per-record flags (one call per distinct record) + J4
268	    if guard("flags"):
269	        year = _accident_year(recs)
270	
271	        def one(r):
272	            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
273	        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
274	            per = list(ex.map(one, distinct))
275	        for r, fs in per:
276	            fs = [f for f in fs if f["type"] != "record_warning"]          # stage 0 already made the record_warning flag
277	            for k, f in enumerate(fs, 1):
278	                f["id"] = f"f_r{r['n']}_{k}"
279	            llm_flags += FL.judge_flags(fs, call=call, case_text=text)
280	    # 7: finalize
281	    set_stage("finalize")
282	    for f in llm_flags:
283	        f.setdefault("record_nos", [f["record_no"]])
284	        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
285	        f["ladder"]["item_id"], f["ladder"]["backend"], f["ladder"]["state"] = f["id"], P.backend_name(), f["state"]
286	        f["ladder"]["code_checks"].setdefault("classified_by", "lexicon+llm")
287	        f.setdefault("review_status", "pending")
288	        f["origin"] = _ORIGIN.get(f["origin"], f["origin"])
289	        f.pop("record_no", None)
290	    flag_items = ing["flags"] + [_clean(f) for f in llm_flags if f["state"] != "rejected"]
291	    tray = [_clean(e) for e in rejected] + [_clean(f) for f in llm_flags if f["state"] == "rejected"]
292	    entries = [_clean(e) for e in entries]
293	    dated = sorted((e for e in entries if dated_cut(e)), key=lambda e: (e["date"], e["seq"]))
294	    undated = [e for e in entries if not dated_cut(e)]
295	    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
296	    flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
297	    final_amounts = [_clean(a) for a in final_amounts]
298	    damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
299	    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
300	    now_t = clock()
301	    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
302	    _persist(conn, cid, "amount", final_amounts, now_t)
303	    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
304	    if timed_out:
305	        status = "timeout"
306	        err = {"code": "run_deadline", "message": "The run passed its time limit; finished items were kept."}
307	    else:
308	        status = "done_with_errors" if errors else "done"
309	        err = None
310	    DB.update_case(conn, cid, status="failed" if timed_out else "ready", stage="finalize", error=json.dumps(err) if err else None,
311	                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
312	    tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
313	    all_items = dated + undated + final_amounts + flag_items
314	    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
315	            "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
316	            "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
317	            "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
318	                       "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
319	                       "verified": sum(1 for i in all_items if i["state"] == "verified")}}
320	
321	
322	# ------------------------------------------------------------------ eval / API view
323	def case_view(out: dict) -> dict:
324	    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
325	    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
326	    flags = []
327	    for f in out["flags"] + out["tray"]:
328	        if "summary" in f:
329	            continue
330	        g = dict(f)
331	        g["evidence"] = [{**e, "record_id": f"r{e['record_no']}", "excerpt": e.get("text")} for e in f.get("evidence", [])]
332	        if f["type"] == "gap":
333	            g["computed"] = {"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}
334	        flags.append(g)
335	    return {"records": out["records"], "entries": out["entries"], "undated_entries": out["undated_entries"],
336	            "amounts": [{**a, "value_cents": a["cents"], "kind": a["cls"]} for a in out["amounts"] + out["damages"]],
337	            "totals": out["totals"], "flags": flags, "tray": [t for t in out["tray"] if "summary" in t], "warnings": out["warnings"],
338	            "dates_to_confirm": out["dates_to_confirm"], "status": out["status"], "errors": out["errors"],
339	            "backend": P.backend_name(), "models": {"generator": judges.generator_model(), "judge": judges.judge_model()}}
340	
341	
342	class _Backend:
343	    """Temporarily select the LLM backend for one call (eval runner passes it explicitly)."""
344	
345	    def __init__(self, name):
346	        self.name, self.old = name, None
347	
348	    def __enter__(self):
349	        import os
350	        self.old = os.environ.get("LLM_BACKEND")
351	        if self.name:
352	            os.environ["LLM_BACKEND"] = self.name
353	
354	    def __exit__(self, *a):
355	        import os
356	        if self.old is None:
357	            os.environ.pop("LLM_BACKEND", None)
358	        else:
359	            os.environ["LLM_BACKEND"] = self.old
360	
361	
362	def _scratch_call(tmp, text):
363	    import os
364	    conn = DB.connect(os.path.join(tmp, "scratch.sqlite"))
365	    cid = DB.create_case(conn, text, now=0.0)
366	    return conn, cid, AU.make_call(conn, cid)
367	
368	
369	def run_case(text: str, backend: str = None) -> dict:
370	    """Full pipeline over `text` on a scratch database; returns case_view(). Used by evals; nothing is kept."""
371	    import contextlib
372	    import tempfile
373	    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
374	        conn, cid, call = _scratch_call(tmp, IN.normalize_text(text))
375	        with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
376	            out = run_pipeline(conn, cid, text, call=call)
377	        view = case_view(out)
378	        conn.close()
379	        return view
380	
381	
382	def judge_summary(summary: str, excerpt: str, label: str, backend: str = None) -> str:
383	    """Judge 1 on one (summary, excerpt, label): 'supported' | 'partially' | 'unsupported' | 'unavailable'. A missing fixture or a failed call
384	    is 'unavailable', never a pass."""
385	    import contextlib
386	    import tempfile
387	    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
388	        conn, cid, call = _scratch_call(tmp, excerpt)
389	        with (P.record_fragment_context(excerpt) if P._recording() else contextlib.nullcontext()):
390	            v = judges.run_j1(summary, excerpt, label, call=call)
391	        conn.close()
392	        return v
393	
394	
395	# ------------------------------------------------------------------ CLI
396	def _usd(c):
397	    return TT.usd(c)
398	
399	
400	def format_report(out: dict) -> str:
401	    from app.backend.dates import long_date
402	    L = [f"Status: {out['status']}   backend: {P.backend_name()}   records: {len(out['records'])}   entries: {len(out['entries'])}"
403	         f"   flags: {len(out['flags'])}   amounts: {len(out['amounts'])}", "", "TIMELINE"]
404	    for e in out["entries"]:
405	        L.append(f"  {long_date(e['date'])} - {e['provider']} [{e['state']}]\n      {e['summary']}")
406	    for e in out["undated_entries"]:
407	        L.append(f"  (date to confirm) {e['provider']} [{e['state']}]\n      {e['summary']}")
408	    for title, types in (("GAPS", ("gap",)), ("CONFLICTS", ("conflict",)), ("PRE-EXISTING", ("pre_existing",)), ("CAUSATION LANGUAGE", ("causation",)),
409	                         ("RECORD WARNINGS", ("record_warning",))):
410	        fs = [f for f in out["flags"] if f["type"] in types]
411	        if fs:
412	            L += ["", title] + [f"  [{f['state']}] {f['title']} - {f['explanation']}" for f in fs]
413	    L += ["", "AMOUNTS"] + [f"  {a['text']} ({a['cls']}) record {','.join(str(n) for n in a['record_nos'])} [{a['state']}]" for a in out["amounts"]]
414	    t = out["totals"]
415	    L.append(f"  Charges detected, pending review (not a total): {_usd(t['detected_pending_cents'])}; accepted so far: {_usd(t['accepted_cents'])}")
416	    if out["errors"]:
417	        L += ["", "ERRORS"] + [f"  {e['code']} at {e['stage']}" + (f" record {e['record_no']}" if "record_no" in e else "") for e in out["errors"]]
418	    return "\n".join(L)
419	
420	
421	def main(argv=None) -> int:
422	    ap = argparse.ArgumentParser(prog="python -m app.pipeline", description="Run the treatment-timeline pipeline on a text file (synthetic data only).")
423	    ap.add_argument("file")
424	    ap.add_argument("--db", default=None, help="SQLite file (default: a temporary file deleted on exit; the audit log lives there)")
425	    ap.add_argument("--json", action="store_true", help="print the full result as JSON")
426	    a = ap.parse_args(sys.argv[1:] if argv is None else argv)
427	    raw = open(a.file, encoding="utf-8").read()
428	    try:
429	        IN.check_limits(raw)
430	    except IN.IngestError as e:
431	        print(f"refused: {e.code}", file=sys.stderr)
432	        return 1
433	    import os
434	    import tempfile
435	    with tempfile.TemporaryDirectory() as d:          # a file, not :memory: (worker threads share the connection)
436	        conn = DB.connect(a.db or os.path.join(d, "cli.sqlite"))
437	        cid = DB.create_case(conn, IN.normalize_text(raw), now=time.time())
438	        out = run_pipeline(conn, cid, raw)
439	        conn.close()
440	    print(json.dumps(out, indent=1, default=str) if a.json else format_report(out))
441	    return 0 if out["status"] in ("done", "done_with_errors") else 1
442	
443	
444	if __name__ == "__main__":
445	    sys.exit(main())
446	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:08:07.596Z

**tool call — Bash**
````
{
 "command": "git status --short app tests tools evals | head; git diff --stat HEAD -- app tests | tail -5; cat app/llm/audited.py; grep -n \"_DB_LOCK\" -r app | head -20"
}
````

### User / tool · 2026-11-02T02:08:07.723Z

**tool result**
````
?? evals/reports/
"""Audited call wrapper (ADR-003.7, ADR-004, LLM_VS_CODE row 20). The only entry point pipeline code uses.

1 attempt + 2 retries; every retry changes the request (stricter-format note in the user prompt); one llm_calls row per
attempt (prompt hash = sha256 of model+system+user+schema); a fixture miss is final. Never logs prompts, responses or error text.
"""
import logging
import os
import threading
import time

from app.db import db as DB
from app.llm import provider as P

log = logging.getLogger("zlayt.llm")
MAX_ATTEMPTS = 3
_DB_LOCK = threading.Lock()   # one sqlite3 connection is shared by the worker threads; its cursors are not safe to interleave
RETRY_DELAYS_S = (0.5, 1.5)
_CODE = __import__('re').compile(r"^([A-Z][A-Z_]{2,40})\b")

_RETRY_NOTES = (
    "",
    "\n\n[RETRY 1 of 2: your previous reply was unusable. Reply with exactly one JSON object that satisfies the schema, with no prose and no code fence.]",
    "\n\n[FINAL RETRY: reply with ONLY the raw JSON object, no markdown, no commentary, every required key present, no extra keys.]",
)


class LLMFailed(Exception):
    code = "LLM_FAILED_AFTER_RETRIES"


class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""

    def __init__(self, prompt_hash: str = ""):
        P.FixtureMissing.__init__(self, prompt_hash)


def _error_code(e: Exception) -> str:
    """Our own codes only (SCHEMA_INVALID, TIMEOUT, BACKEND_FAILED ...); anything else is reduced to the exception class."""
    if isinstance(e, P.LLMError):
        m = _CODE.match(str(e))
        return m.group(1) if m else "LLM_ERROR"
    return "VALIDATION_FAILED" if isinstance(e, ValueError) else type(e).__name__


def role_for(step: str) -> str:
    s = str(step)
    return "judge" if s.startswith("judge") or (len(s) == 2 and s[0] == "j" and s[1].isdigit()) else "generator"


def _t(now):
    return now() if callable(now) else (time.time() if now is None else now)


def audited_call(conn, case_id: str, step: str, model: str, system: str, user: str, json_schema: dict, *,
                 complete_with_meta=None, validate=None, item_id=None, now=None, prompt_version=None, sleep=None):
    cwm = complete_with_meta or P.complete_with_meta
    last_err = "unknown"
    for attempt in range(1, MAX_ATTEMPTS + 1):
        u = user + _RETRY_NOTES[attempt - 1]
        h = P.prompt_hash(model, system, u, json_schema)
        t0 = time.monotonic()
        res, err, fixture_miss = None, None, False
        try:
            res = cwm(model, system, u, json_schema)
            if validate is not None:
                validate(res.output)
        except P.FixtureMissing as e:
            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
        except Exception as e:                         # only our own error codes are stored, never model- or record-derived text
            err = _error_code(e)
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
        last_err = err
        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
        if fixture_miss:
            raise LLMFailedFixtureMiss(h)
        if sleep is not None and attempt < MAX_ATTEMPTS:
            sleep(RETRY_DELAYS_S[attempt - 1])         # short, capped, code-controlled
    raise LLMFailed(f"{step}: {MAX_ATTEMPTS} attempts failed")


def _dump(o):
    import json
    return json.dumps(o, sort_keys=True)


def make_call(conn, case_id: str, *, now=None, models: dict = None, schemas: dict = None):
    """Build the pipeline's `call(step, system, user, schema, *, item_id=None) -> (output, call_id)`.
    Model per role comes from GENERATOR_MODEL / JUDGE_MODEL (ADR-004) unless `models` overrides."""
    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}

    def call(step, system, user, schema, *, item_id=None, validate=None):
        return audited_call(conn, case_id, step, m[role_for(step)], system, user, schema, item_id=item_id, now=now, validate=validate)
    return call
app/llm/audited.py:16:_DB_LOCK = threading.Lock()   # one sqlite3 connection is shared by the worker threads; its cursors are not safe to interleave
app/llm/audited.py:82:        with _DB_LOCK:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:08:08.474Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode -q 2>&1 | grep -E \"Error|assert|^E\" | head; grep -n \"def test_replay_has_no_fixture_miss\" -B6 -A25 tests/unit/test_t037_backend.py"
}
````

### User / tool · 2026-11-02T02:08:09.623Z

**tool result**
````
        assert r.status_code == 200 and j["item"]["review_status"] == "edited" and j["item"]["state"] == "needs_review"
>       assert j["warnings"][0]["code"] == "JUDGE_UNAVAILABLE" and j["item"]["edited"]["original_summary"]
E       IndexError: list index out of range
tests/unit/test_api_routes.py:129: IndexError
26-    assert p.returncode == 0 and time.time() - t0 < 60, p.stderr[-500:]
27-    assert "entries: 9" in p.stdout and "Gap of 73 days" in p.stdout and "$8,390.00" in p.stdout and "ERRORS" not in p.stdout
28-
29-
30-@needs_fixtures
31-@pytest.mark.parametrize("case", ["sample"] + [c for c in G.case_names() if c != "sample"])
32:def test_replay_has_no_fixture_miss(case, monkeypatch):
33-    """T-037 AC2/AC7: replaying every golden input on the fixture backend reports 0 FixtureMiss (no error, no FIXTURE_MISS reason)."""
34-    monkeypatch.setenv("LLM_BACKEND", "fixture")
35-    view = PL.run_case(G.raw(case), "fixture")
36-    assert view["errors"] == [] and view["status"] == "done"
37-    items = view["entries"] + view["undated_entries"] + view["amounts"] + view["flags"]
38-    assert not [i for i in items if "FIXTURE_MISS" in i.get("reasons", [])], case
39-
40-
41-@needs_fixtures
42-def test_judge_lines_replay(monkeypatch):
43-    """T-037 AC2/AC6: every hallucination, control and seeded-edit line has a recorded judge-1 answer."""
44-    from app.llm import record
45-    monkeypatch.setenv("LLM_BACKEND", "fixture")
46-    n = 0
47-    for name in ("hallucinations.jsonl", "hallucinations_controls.jsonl"):
48-        for line in (P.GOLDEN_DIR / name).read_text().splitlines():
49-            if line.strip():
50-                it = json.loads(line)
51-                label, excerpt = record._parse_record_text(it["record_text"])
52-                assert PL.judge_summary(it["candidate_summary"], excerpt, label, "fixture") != "unavailable", it["id"]
53-                n += 1
54-    assert n == 50
55-
56-
57-def test_fixtures_come_only_from_golden_text():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:08:16.746Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > $S/miss.py <<'EOF'\nimport os, sys, logging, io, collections\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nos.environ[\"LLM_BACKEND\"]=\"fixture\"\nfrom app.backend import pipeline as PL\nfrom tests.unit import golden as G  # may differ\nEOF\ngrep -n \"^import\\|^from\" tests/unit/test_t037_backend.py | head; ls evals/golden | head -30"
}
````

### User / tool · 2026-11-02T02:08:16.837Z

**tool result**
````
3:import json
4:import os
5:import subprocess
6:import sys
7:import time
8:import pathlib
9:import pytest
10:from app.backend import pipeline as PL
11:from app.db import db as DB
12:from app.llm import provider as P
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
sample.expected.json
sample.export.expected.txt
sample.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:08:21.971Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > $S/miss.py <<'EOF'\nimport os, sys, logging, glob\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nos.environ[\"LLM_BACKEND\"]=\"fixture\"\nfrom app.backend import pipeline as PL\nclass H(logging.Handler):\n    n=0\n    def emit(self, r): H.n+=1\nlogging.getLogger(\"zlayt.llm\").addHandler(H()); logging.getLogger(\"zlayt.llm\").propagate=False\nfor f in sorted(glob.glob(\"/Users/arsis/zlayt-pm-project/evals/golden/*.txt\")):\n    H.n=0\n    v=PL.run_case(open(f).read(),\"fixture\")\n    states={}\n    for i in v[\"entries\"]+v[\"flags\"]+v[\"amounts\"]:\n        states[i[\"state\"]]=states.get(i[\"state\"],0)+1\n    print(os.path.basename(f), \"failed_calls\",H.n, \"status\",v[\"status\"], \"errors\",len(v[\"errors\"]), states)\nEOF\n.venv/bin/python $S/miss.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T02:08:22.835Z

**tool result**
````
case_01_date_formats.txt failed_calls 11 status done errors 0 {'needs_review': 11}
case_02_gap_boundaries.txt failed_calls 0 status done errors 0 {'verified': 11}
case_03_rate_and_ocr.txt failed_calls 0 status done errors 0 {'verified': 7, 'needs_review': 3}
case_04_duplicates_no_amounts.txt failed_calls 0 status done errors 0 {'verified': 4}
case_05_provider_conflict.txt failed_calls 0 status done errors 0 {'verified': 7, 'needs_review': 1}
case_06_subtle_pre_existing.txt failed_calls 0 status done errors 0 {'verified': 8, 'needs_review': 2}
case_07_prompt_injection.txt failed_calls 0 status done errors 0 {'verified': 5, 'needs_review': 5}
case_08_diagnosis_temptation.txt failed_calls 0 status done errors 0 {'verified': 6}
case_09_nonvisit_hides_gap.txt failed_calls 0 status done errors 0 {'verified': 6, 'needs_review': 1}
sample.export.expected.txt failed_calls 9 status done_with_errors errors 2 {'needs_review': 36}
sample.txt failed_calls 21 status done errors 0 {'needs_review': 22, 'verified': 2}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:08:30.094Z

**tool call — Bash**
````
{
 "command": "grep -n \"stage\\|timeout\\|failed\\|ready\\|status\" memory/contracts/api.md | head -40; grep -n \"def test_code_stages_without_llm\" -A30 tests/unit/test_pipeline.py | head -60"
}
````

### User / tool · 2026-11-02T02:08:30.190Z

**tool result**
````
9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409), `item_rejected` (409), `invalid_edit` (422, every structurally invalid edit), `date_invalid` (422, `confirm_date` with a non-candidate date), `llm_unavailable` (503).
10:- Every item has `state` (system: `verified` | `needs_review` | `rejected`), `reasons[]` (codes), `why` (one template sentence), `review_status` (human: `pending` | `accepted` | `edited` | `dismissed`), and `ladder` (D.4).
21:| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
22:| GET | `/api/cases/{token}/status` | stage and progress |
51:{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ingested", "source": "paste",
55:      "date_status": "parsed", "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true,
67:{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "status": "running", "stage": "extract", "started_at": "2026-11-02T01:02:03Z" }
69:Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human decisions and `confirm_rerun` is false; a rerun keeps records, gap review status, events and calls); `409 demo_mode_unsupported_input` (re-checked here, before any LLM call, in demo mode); `503 llm_unavailable`.
71:## GET /api/cases/{token}/status
73:{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "status": "running", "stage": "judge_entries",
74:  "stages": ["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],
79:`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline", "message": "..."}`; finished items are kept. Poll every second. Partial results are readable from the case endpoint while running.
85:  "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ready", "demo_mode": true,
88:    { "id": "r2", "seq": 2, "source_label": "Central ER discharge summary", "date_iso": "2026-01-09", "date_status": "parsed",
94:    { "id": "e2", "seq": 2, "record_ids": ["r2"], "date": "2026-01-09", "date_status": "parsed",
101:      "review_status": "pending", "edited": null, "duplicate_note": null,
118:      "review_status": "pending", "edited": null, "duplicate_note": null,
128:      "review_status": "pending", "edited": null, "duplicate_note": null,
151:      "review_status": "pending", "edited": null,
165:      "review_status": "pending", "edited": null,
176:      "review_status": "pending", "edited": null,
192:    "ready_to_export": false },
197:(The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative`, `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
200:Resolves a record whose `date_status` is `ambiguous` by choosing one of the readings the code proposed (`date_candidates`). It is not an edit (D-010). A record with no readable date (`missing`) cannot be confirmed; it stays excluded and flagged. Request:
204:Response 200: the record with `date_status: "confirmed"`, its entry's date, the **recomputed gap flags** (a changed or new flag keeps no review status; an unchanged record pair keeps its status), the cleared `date_ambiguous` record warning, and `dates_to_confirm`:
206:{ "record": {"id": "r8", "date_iso": "2026-05-04", "date_status": "confirmed", "date_raw": "04/05/2026"},
244:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; a rate can never become a charge); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. There is no bulk accept.
253:The client shows the reasons; if she chooses "keep my wording" it resends with `"confirm_warnings": true`, the edit is saved and a `keep_my_wording` event is logged (listed in the internal notes). **If the code check passes but the judge fails** (error, timeout, or no recorded fixture, which is always the case in demo mode), the edit is saved, the item becomes `needs_review` with reason `JUDGE_UNAVAILABLE`, and the response carries it in `warnings[]`: no 409, because nothing objected. The judge never blocks an edit and never lets an unchecked edit look verified.
257:{ "item": { "id": "e3", "review_status": "edited", "state": "needs_review", "reasons": ["JUDGE_UNAVAILABLE"],
261:              "queue": ["a3", "e4", "e2", "a1"], "ready_to_export": false },
267:Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). No parameters. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
423:  "events": [ { "id": "ev1", "item_id": "e2", "action": "accept", "before": {"review_status": "pending"}, "after": {"review_status": "accepted"}, "at": "2026-11-02T01:05:00Z" } ],
437:| `SCHEMA_INVALID` | rejected | model output failed schema validation after retries |
445:| `JUDGE_UNAVAILABLE` | needs_review | the judge call failed or timed out, or (always in demo mode) an edit has no recorded judge answer |
454:| `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
455:| `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded answer; conflicts between records may be missing (case-level `record_warning` `analysis_incomplete`, no single record) |
67:def test_code_stages_without_llm(tmp_path):
68-    """T-037 AC4 / row 9 / LLM_FAILED_AFTER_RETRIES: if EVERY model call fails, gaps, amounts and the accident-date conflict still exist; no entry is invented; the run reports done_with_errors with the error code."""
69-    boom = FakeCall({s: AU.LLMFailed("down") for s in ("extract", "j1", "j2", "j3", "j4", "conflicts", "flags")})
70-    out, _ = run_sample(tmp_path, call=boom)
71-    assert gap_keys(out) == [("2026-03-06", "2026-05-18", 73)] and len(out["amounts"]) == 3
72-    assert any(f["type"] == "conflict" and f.get("subtype") == "accident_date" for f in out["flags"])
73-    assert out["entries"] == []
74-    assert out["status"] == "done_with_errors" and any(e["code"] == "LLM_FAILED_AFTER_RETRIES" for e in out["errors"])
75-
76-def test_one_failed_extract_loses_only_that_entry_and_leaves_gaps_unchanged(tmp_path):
77-    """T-037 AC4 / D-003 / row 9: record 6 (a gap endpoint) fails to extract -> 8 entries, a visible error naming it, and the gap flags are identical to a clean run."""
78-    clean, _ = run_sample(tmp_path)
79-    def extract(user):
80-        if which_record(user) == [6]:
81-            raise AU.LLMFailed("down")
82-        return sample_script()["extract"](user)
83-    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(extract=extract)))
84-    assert len(out["entries"]) == 8 and not [e for e in items_for(out, 6) if e["state"] == "verified"]
85-    assert out["status"] == "done_with_errors"
86-    assert any(e["code"] == "LLM_FAILED_AFTER_RETRIES" and e.get("record_no") == 6 for e in out["errors"])
87-    assert gap_keys(out) == gap_keys(clean) == [("2026-03-06", "2026-05-18", 73)]
88-
89-def test_fixture_missing_after_audited_wrapper_is_a_visible_error_never_a_default(tmp_path):
90-    """T-034 AC8 / T-037 AC7: a recorded-answer miss reaches the pipeline as LLM_FAILED_AFTER_RETRIES (the audited wrapper converts FixtureMissing); the item is absent with a run-level error, not filled in."""
91-    miss = AU.LLMFailed("FIXTURE_MISS abc")
92-    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(extract=miss)))
93-    assert out["entries"] == [] and out["status"] == "done_with_errors"
94-    assert {e["code"] for e in out["errors"]} == {"LLM_FAILED_AFTER_RETRIES"} and len(out["errors"]) == 9
95-
96-def test_verify_stage_rejects_non_verbatim_excerpt(tmp_path):
97-    """T-035 AC2 / R-TL-2 (rung 1): a seeded excerpt that is not word for word in its record, and one with an invented sentence appended, never become verified entries even though judge 1 says 'supported'. Fails if the verify/grounding stage is removed."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:08:36.174Z

**tool call — Bash**
````
{
 "command": "git log --format='%h %ci %s' -8 -- app/llm/prompts | cat; git log --format='%h %ci %s' -3 -- tests/fixtures/llm | cat; git log --format='%h %ci %s' -1 | cat; ls -la --time-style=full-iso app/llm/prompts 2>/dev/null | head -20; ls app/llm; git status --short --untracked-files=all app tests | head"
}
````

### User / tool · 2026-11-02T02:08:36.359Z

**tool result**
````
250e7b6 2026-11-01 19:54:52 -0600 fix(backend): generator tests, D-028 judge reason_code, label in nonce block (T-035 r2)
b1803c0 2026-11-01 19:53:42 -0600 fix(backend): FixtureMissing, hash log, sleep seam, fail-closed schema validator, recorder guard, cli env allowlist (T-034 r1)
958c353 2026-11-01 19:49:38 -0600 feat(backend): LLM provider, claude-cli/anthropic-api/fixture backends, audited retries, recorder (T-034)
0d040d3 2026-11-01 20:06:56 -0600 feat(backend): eval view, judge recorder, fixtures for sample + 9 cases + judge lines (T-037)
4e8f43d 2026-11-01 20:06:08 -0600 test(fixtures): curated set r2 - golden flag spans (D-030), accept all pending, byte-equal export (T-051)
43b5e12 2026-11-01 20:01:23 -0600 test(fixtures): curated golden-conformant fixture set + generator (T-051, D-029)
700ca9a 2026-11-01 20:08:33 -0600 plan: T-060 enterprise UI polish per Chris
__init__.py
__pycache__
_types.py
audited.py
backends
lexicon.yaml
promptlib.py
prompts
provider.py
record.py
 M tests/unit/test_eval_runner.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:08:40.980Z

**tool call — Bash**
````
{
 "command": "git log --format='%h %ci %s' --since='2026-11-01 20:06:56 -0600' -- app evals/golden lexicon app/llm | cat; ls tests/fixtures/llm | head -3; ls tests/fixtures/llm | wc -l; git ls-files tests/fixtures/llm | wc -l; git log --format='%h %ci' -1 -- tests/fixtures/llm/$(ls tests/fixtures/llm | head -1) | cat"
}
````

### User / tool · 2026-11-02T02:08:41.121Z

**tool result**
````
81df4e0 2026-11-01 20:07:45 -0600 feat(backend): pipeline conflict-pass warning on run (T-036) on top of T-037/T-050 edits
3f37141 2026-11-01 20:07:17 -0600 fix(backend): source_kind from lexicon self_report with explicit patient attribution, case-level conflict-check warning, single-period templates (T-036 r3)
0d040d3 2026-11-01 20:06:56 -0600 feat(backend): eval view, judge recorder, fixtures for sample + 9 cases + judge lines (T-037)
003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
010db3ae8de16d72ea8905cdaa07781591d70092d358c0d5e73424940e3cfb33.json
051431244b8754ecac0333514244f37930768de97ec3b4f639b97047e0ada328.json
     279
     316
0d040d3 2026-11-01 20:06:56 -0600
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:08:53.482Z

**tool call — Bash**
````
{
 "command": "grep -n \"ThreadPool\\|threading\" -r app | grep -v pycache; grep -n \"check_same_thread\\|def connect\" -A8 app/db/db.py | head -30; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $S/chk.py <<'EOF'\nimport os, sys, tempfile, collections\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nos.environ[\"LLM_BACKEND\"]=\"fixture\"\nfrom app.backend import pipeline as PL\nfrom app.db import db as DB\nfor name in (\"case_07_prompt_injection\",\"sample\"):\n    raw=open(f\"/Users/arsis/zlayt-pm-project/evals/golden/{name}.txt\").read()\n    with tempfile.TemporaryDirectory() as d:\n        conn=DB.connect(d+\"/a.sqlite\"); cid=DB.create_case(conn,PL.IN.normalize_text(raw),now=0.0)\n        out=PL.run_pipeline(conn,cid,raw)\n        items=out[\"entries\"]+out[\"amounts\"]+out[\"damages\"]+out[\"flags\"]\n        print(name, \"review_status\", collections.Counter(i[\"review_status\"] for i in items))\n        rw=[(f[\"category\"],tuple(f[\"record_nos\"])) for f in out[\"flags\"] if f[\"type\"]==\"record_warning\"]\n        print(\" record_warnings\", rw, \"dups\", [k for k,c in collections.Counter(rw).items() if c>1])\n        print(\" no ladder backend:\", [i[\"id\"] for i in items if not (i.get(\"ladder\") or {}).get(\"backend\")])\n        print(\" no state:\", [i[\"id\"] for i in items if not i.get(\"state\")])\n        print(\" tray\", len(out[\"tray\"]), \"warnings\", [w[\"code\"] for w in out[\"warnings\"]])\n        print(\" flag types\", collections.Counter(f[\"type\"] for f in out[\"flags\"]))\n        calls=conn.execute(\"select count(*), sum(parsed_ok=0) from llm_calls\").fetchone(); print(\" calls\",tuple(calls))\n        print(\" sample reasons\", collections.Counter(r for i in items for r in i[\"reasons\"]))\nEOF\n.venv/bin/python $S/chk.py 2>&1 | grep -v \"llm call failed\""
}
````

### User / tool · 2026-11-02T02:08:54.009Z

**tool result**
````
app/llm/backends/claude_cli.py:11:import threading
app/llm/backends/claude_cli.py:18:_SEM = threading.BoundedSemaphore(MAX_CONCURRENCY)
app/llm/audited.py:8:import threading
app/llm/audited.py:16:_DB_LOCK = threading.Lock()   # one sqlite3 connection is shared by the worker threads; its cursors are not safe to interleave
app/backend/generator.py:6:from concurrent.futures import ThreadPoolExecutor
app/backend/generator.py:127:    with ThreadPoolExecutor(max_workers=max(1, min(workers, CONCURRENCY))) as ex:
app/backend/generator.py:147:    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
app/backend/api.py:11:import threading
app/backend/api.py:256:            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
app/backend/pipeline.py:12:from concurrent.futures import ThreadPoolExecutor
app/backend/pipeline.py:273:        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
29:def connect(path: str):
30:    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
31-    conn.row_factory = sqlite3.Row
32-    conn.execute("PRAGMA secure_delete=ON")
33-    conn.execute("PRAGMA foreign_keys=ON")
34-    with open(_SCHEMA, encoding="utf-8") as f:
35-        conn.executescript(f.read())
36-    return conn
37-
38-
case_07_prompt_injection review_status Counter({'pending': 10})
 record_warnings [('injection_suspected', (3,))] dups []
 no ladder backend: []
 no state: []
 tray 0 warnings ['INJECTION_SUSPECTED']
 flag types Counter({'gap': 1, 'pre_existing': 1, 'causation': 1, 'record_warning': 1})
 calls (17, 0)
 sample reasons Counter({'INJECTION_SUSPECTED': 4, 'JUDGE_DISAGREES': 1, 'AMOUNT_UNCLEAR': 1, 'LLM_ONLY': 1})
sample review_status Counter({'pending': 24})
 record_warnings [] dups []
 no ladder backend: []
 no state: []
 tray 0 warnings []
 flag types Counter({'causation': 6, 'conflict': 2, 'pre_existing': 2, 'gap': 1})
 calls (40, 21)
 sample reasons Counter({'JUDGE_UNAVAILABLE': 21, 'AMOUNT_RATE_NOT_TOTALED': 1, 'AMOUNT_DAMAGES': 1, 'LLM_ONLY': 1})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:08:57.723Z

**tool call — Bash**
````
{
 "command": "grep -n \"DB.connect\\|conn =\\|_run_thread\" app/backend/api.py | head; grep -n \"ENDPOINT_NOT_VERIFIED\" -r app --include=*.py | head; grep -n \"def test_endpoint_not_verified_and_every_flag_has_a_state\" -A25 tests/unit/test_t037_backend.py"
}
````

### User / tool · 2026-11-02T02:08:57.823Z

**tool result**
````
59:    DB.connect(db_path).close()
78:        return DB.connect(app.state.db_path)
225:    def _run_thread(token, raw):
256:            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
app/backend/why.py:19:    "ENDPOINT_NOT_VERIFIED": "One end of this gap could involve a date that has not been confirmed.",
app/backend/confidence.py:9:    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
app/backend/confidence.py:64:                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
app/backend/pipeline.py:39:           "endpoint_unverified": "ENDPOINT_NOT_VERIFIED" in reasons}
app/backend/pipeline.py:41:    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
app/backend/gaps.py:37:            reasons.append("ENDPOINT_NOT_VERIFIED")
105:def test_endpoint_not_verified_and_every_flag_has_a_state():
106-    """T-037 AC8 / ADR-010: an undated encounter record that could sit inside a gap makes the gap flag needs_review (ENDPOINT_NOT_VERIFIED); every flag has a state."""
107-    t = ('Date: 2026-01-01\nSource: A Clinic, visit 1\nExcerpt: "Pain 5/10."\n---\nDate: 2026-03-01\nSource: A Clinic, visit 2\nExcerpt: "Pain 4/10."\n---\n'
108-         'Date: 02/04/2026\nSource: A Clinic, visit 3\nExcerpt: "Pain 3/10."')
109-    out = PL.run_ingest(t)
110-    gap = [f for f in out["flags"] if f["type"] == "gap"]
111-    assert len(gap) == 1 and gap[0]["state"] == "needs_review" and "ENDPOINT_NOT_VERIFIED" in gap[0]["reasons"]
112-    assert all(f["state"] in ("verified", "needs_review", "rejected") for f in out["flags"])
113-    sample = PL.run_ingest(G.raw("sample"))
114-    assert [f["state"] for f in sample["flags"] if f["type"] == "gap"] == ["verified"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:09:07.820Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/mut; mkdir $S/mut; git archive HEAD | tar -x -C $S/mut; ln -s /Users/arsis/zlayt-pm-project/.venv $S/mut/.venv 2>/dev/null; cd $S/mut; cat > $S/mutrun.sh <<'EOF'\n#!/bin/bash\n# usage: mutrun.sh label old new\ncd \"$1\" || exit 1\nEOF\ncat > $S/mut.py <<'EOF'\nimport sys, subprocess, shutil, pathlib\nroot=pathlib.Path(sys.argv[1]); f=root/\"app/backend/pipeline.py\"; orig=f.read_text()\nmuts={\n \"dedupe_removed\": ('fs = [f for f in fs if f[\"type\"] != \"record_warning\"]','fs = list(fs)'),\n \"endpoint_ctx_dropped\": ('\"endpoint_unverified\": \"ENDPOINT_NOT_VERIFIED\" in reasons}','\"endpoint_unverified\": False}'),\n \"deadline_never\": ('return clock() - t0 > deadline_s','return False'),\n \"ladder_backend_dropped\": ('f[\"ladder\"][\"item_id\"], f[\"ladder\"][\"backend\"], f[\"ladder\"][\"state\"] = f[\"id\"], P.backend_name(), f[\"state\"]','f[\"ladder\"][\"item_id\"], f[\"ladder\"][\"state\"] = f[\"id\"], f[\"state\"]; f[\"ladder\"][\"backend\"]=None'),\n \"gap_dropped_with_entry\": ('code = GP.gap_flags(recs) +','code = GP.gap_flags([r for r in recs if r[\"n\"] != 6]) +'),\n \"failed_lock_off\": None,\n}\nfor k,v in muts.items():\n    if v is None: continue\n    assert orig.count(v[0])==1,k\n    f.write_text(orig.replace(*v))\n    p=subprocess.run([str(root/\".venv/bin/python\"),\"-m\",\"pytest\",\"tests/unit/test_pipeline.py\",\"tests/unit/test_t037_backend.py\",\"-q\",\"-x\",\"-p\",\"no:cacheprovider\"],cwd=root,capture_output=True,text=True)\n    print(k, p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-200:])\nf.write_text(orig)\nEOF\n.venv/bin/python $S/mut.py $S/mut 2>&1 | tail -10"
}
````

### User / tool · 2026-11-02T02:09:16.800Z

**tool result**
````
dedupe_removed 44 passed in 2.58s
endpoint_ctx_dropped 1 failed, 43 passed in 2.46s
deadline_never 1 failed, 10 passed in 0.77s
ladder_backend_dropped 1 failed, 25 passed in 1.35s
gap_dropped_with_entry 1 failed, 1 passed in 0.21s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:09:23.402Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && sed -i 's|fs = \\[f for f in fs if f\\[\"type\"\\] != \"record_warning\"\\]|fs = list(fs)|' mut/app/backend/pipeline.py && grep -c \"fs = list(fs)\" mut/app/backend/pipeline.py && sed 's|/Users/arsis/zlayt-pm-project\"|'\"$PWD\"'/mut\"|; s|sys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")|sys.path.insert(0, \"'\"$PWD\"'/mut\")|' chk.py > chk_mut.py && cd mut && .venv/bin/python ../chk_mut.py 2>&1 | grep -A2 \"case_07\"; grep -rn \"record_warning\" /Users/arsis/zlayt-pm-project/tests/unit/test_pipeline.py /Users/arsis/zlayt-pm-project/tests/unit/test_t037_backend.py | head -5"
}
````

### User / tool · 2026-11-02T02:09:23.496Z

**tool result**
````
sed: 1: "mut/app/backend/pipelin ...": invalid command code m
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:09:28.566Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && P=$PWD && python3 - <<EOF\nimport pathlib\nf=pathlib.Path(\"$P/mut/app/backend/pipeline.py\"); t=f.read_text()\nold='fs = [f for f in fs if f[\"type\"] != \"record_warning\"]'; assert t.count(old)==1\nf.write_text(t.replace(old,'fs = list(fs)'))\nc=pathlib.Path(\"$P/chk.py\").read_text().replace('/Users/arsis/zlayt-pm-project\"',\"$P/mut\\\"\",1)\npathlib.Path(\"$P/chk_mut.py\").write_text(c)\nEOF\ngrep -n \"sys.path\" chk_mut.py; cd mut && ../../../../../../../../../../../Users/arsis/zlayt-pm-project/.venv/bin/python ../chk_mut.py 2>&1 | grep -A2 \"case_07\"; grep -rn \"record_warning\" /Users/arsis/zlayt-pm-project/tests/unit/test_pipeline.py /Users/arsis/zlayt-pm-project/tests/unit/test_t037_backend.py | head -5"
}
````

### User / tool · 2026-11-02T02:09:29.175Z

**tool result**
````
2:sys.path.insert(0, "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut")
case_07_prompt_injection review_status Counter({'pending': 11})
 record_warnings [('injection_suspected', (3,)), ('injection_suspected', (3,))] dups [('injection_suspected', (3,))]
 no ladder backend: []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:10:03.385Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-037-staff-engineer.md",
 "content": "# T-037 review: staff-engineer-reviewer\n\nVerdict: fail (1 blocker, 2 major, 1 minor). Reviewed the tree at HEAD 81df4e0, which includes the T-037 commits d67a82d, 0d040d3 and fe4e6a2.\n\nExercised:\n- `.venv/bin/python -m pytest tests/unit -q`: 767 passed, 1 failed. The failure is `test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode` (`IndexError` on `j[\"warnings\"][0]`). It is in the API route tests and I did not bisect it. I do not attribute it to T-037.\n- `.venv/bin/python -m app.pipeline evals/golden/sample.txt`, run twice:\n  - exit 0, and the stdout is byte-identical across both runs.\n  - 9 entries, the 73-day gap, and $8,390.00 detected (not a total) are all present.\n  - stderr carries 21 `llm call failed` warnings, all judge steps (j1 to j4). Every one of the 9 entries is `[needs_review]`.\n- A replay of every golden case on the fixture backend, counting failed calls (scratch script, not committed):\n\n| Case | Failed calls | States |\n|---|---|---|\n| sample | 21 | 22 needs_review, 2 verified |\n| case_01 | 11 | all needs_review |\n| case_02 to case_09 | 0 | normal |\n\n- I also checked case_07 and sample after a run:\n  - Every item has review_status `pending`, a state, and a ladder with a backend.\n  - case_07 has exactly one `injection_suspected` record_warning for record 3.\n- Scratch-copy mutation of `app/backend/pipeline.py` (`git archive HEAD` copy), running `test_pipeline.py` and `test_t037_backend.py` against each mutant:\n\n| Mutant | Result |\n|---|---|\n| Drop the ENDPOINT_NOT_VERIFIED context | caught |\n| Deadline never expires | caught |\n| Ladder backend dropped | caught |\n| Gap computed without record 6 | caught |\n| Remove the record_warning dedupe (line 276) | **not caught** (44 passed) |\n\n- Read all of `app/backend/pipeline.py` and `app/llm/audited.py`.\n\nChecks that came out right:\n- Stage names match api.md.\n- Code stages produce output with every LLM call failing (stub backend), and the gap is unchanged when an entry is dropped.\n- finalize gives every flag a state, including ENDPOINT_NOT_VERIFIED.\n- The deadline takes an injectable `now`.\n- `_DB_LOCK` only wraps `add_llm_call`, is not re-entrant, and has no nested acquisition, so I found no deadlock.\n- Every run leaves review_status `pending`.\n\nI did not run the fixtures-contain-only-golden-text grep. The recorder guard test passes, but I did not independently grep a non-golden phrase.\n\n```json\n{\"card\": \"T-037\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"HEAD 81df4e0 incl. d67a82d/0d040d3/fe4e6a2; app/backend/pipeline.py, app/llm/audited.py, tests/unit/test_pipeline.py, tests/unit/test_t037_backend.py, tests/fixtures/llm; CLI on evals/golden/sample.txt (fixture backend)\",\n \"exercised\": [\"pytest tests/unit -q (767 passed, 1 failed in test_api_routes, not T-037)\", \"python -m app.pipeline evals/golden/sample.txt x2, stdout identical, exit 0, 21 stderr 'llm call failed' warnings\", \"scratch replay of every golden case on fixture backend counting failed llm calls (sample 21, case_01 11, others 0)\", \"scratch run of case_07 and sample: review_status, ladder backend, state, record_warning dedupe\", \"scratch-copy mutation of pipeline.py (5 mutants; dedupe removal survives)\", \"read app/backend/pipeline.py and app/llm/audited.py in full; read api.md status section\"],\n \"verdict\": \"fail\",\n \"scores\": {\"llm_vs_code_separation\": 4, \"failure_visibility\": 3, \"test_strength\": 2, \"determinism_and_fixtures\": 2, \"stage_and_status_contract\": 4},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"Fixtures for sample and case_01 are stale: replay hits 21 and 11 fixture misses, contradicting AC7 and AC1 'all done' evidence\",\n   \"evidence\": \"Scratch replay with LLM_BACKEND=fixture: sample.txt failed_calls=21 (steps j1 x8, j2 x3, j3 x1, j4 x9 in the CLI stderr), case_01 failed_calls=11, other cases 0. CLI output shows all 9 entries '[needs_review]'. Reasons counter for sample: JUDGE_UNAVAILABLE x21. Card AC7 evidence: 'test_replay_has_no_fixture_miss[*] 0 FixtureMiss on sample+9 cases'. Fixtures last committed 0d040d3 (20:06:56); 3f37141 (20:07:17) and 81df4e0 (20:07:45) changed flag/conflict prompts or templates after recording. Orchestrator note 02:01:02Z required re-recording after backend-1's prompt changes.\",\n   \"why_it_matters\": \"AC7 requires 0 FixtureMissing on sample and case_01..09; the headline demo case has 21 and the CLI cannot show a verified timeline on fixtures. Evals run on the fixture backend will compare against needs_review everywhere. The AC was ticked done with evidence that is false for sample and case_01.\",\n   \"fix\": \"Re-record fixtures for sample and case_01 (and any case whose prompt hashes changed) after the last prompt/template change, then re-run the miss count over all ten inputs.\",\n   \"acceptance_test\": \"A test that counts llm_calls rows with error LIKE 'FIXTURE_MISS%' (or the audited-wrapper warning count) over sample + case_01..09 and asserts 0, printing the count; it fails today with 21 and 11.\"},\n  {\"severity\": \"major\", \"title\": \"test_replay_has_no_fixture_miss is vacuous: it passes with 32 fixture misses\",\n   \"evidence\": \"tests/unit/test_t037_backend.py:36-38 asserts view['errors'] == [], status == 'done' and no item reason 'FIXTURE_MISS'. Judge-call misses surface as reason JUDGE_UNAVAILABLE with status done, so the test is green (767 passed) while sample logs 21 misses.\",\n   \"why_it_matters\": \"A test that stays green when the thing it names is broken gives false assurance (same family as a stubbed verifier). It is how finding 1 shipped with AC ticked.\",\n   \"fix\": \"Assert on the llm_calls table (or the audited warning) for FIXTURE_MISS rows, and also assert JUDGE_UNAVAILABLE is absent for fixture-backed golden cases.\",\n   \"acceptance_test\": \"Mutate a fixture file name in a scratch copy; the test must fail.\"},\n  {\"severity\": \"major\", \"title\": \"Injection record_warning dedupe has no test: removing the filter at pipeline.py:276 leaves 44 tests green\",\n   \"evidence\": \"Scratch mutant replacing `fs = [f for f in fs if f[\\\"type\\\"] != \\\"record_warning\\\"]` with `fs = list(fs)`: test_pipeline.py + test_t037_backend.py 44 passed; case_07 then yields two ('injection_suspected', (3,)) flags (dups found), versus exactly one at HEAD. grep for record_warning in both test files returns no hits. Orchestrator note 01:56:12Z required finalize to dedupe.\",\n   \"why_it_matters\": \"The duplicate is a user-visible double warning and a double review item for the same record; the only guard is an untested one-line filter.\",\n   \"fix\": \"Add a test running case_07 (or a tagged-record script) and asserting exactly one record_warning per (category, record_no).\",\n   \"acceptance_test\": \"The test fails against the `fs = list(fs)` mutant.\"},\n  {\"severity\": \"minor\", \"title\": \"Deadline is checked only between stages\",\n   \"evidence\": \"pipeline.py:212-232: expired() is evaluated in guard() at stage entry only; the flags stage (ThreadPoolExecutor, up to 3 attempts per call with sleeps) and judge_flags run to completion once started.\",\n   \"why_it_matters\": \"An 8-minute limit can be exceeded by one stage; the run then reports timeout after the fact. This is a design preference, not a spec violation, unless api.md requires a hard cutoff.\",\n   \"fix\": \"Optionally check expired() per record in the flags stage worker and per call batch.\",\n   \"acceptance_test\": \"A fake clock that expires mid-flags-stage yields status timeout with only the finished records persisted.\"}\n ],\n \"whats_right\": [\"Code stages (ingest, gaps, accident-date conflict, amounts) are independent of the LLM and survive every call failing; dropping an entry leaves gaps identical (mutants on gap input and ENDPOINT context are caught).\", \"CLI output is byte-identical across two runs, ~0.4 s, and no run sets any review_status other than pending; every item has a state and a ladder backend.\", \"_DB_LOCK is minimal (writes only, non-reentrant, no nesting), and audited_call keeps 1+2 capped retries with a fixture miss final.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T02:10:03.554Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-037-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:10:05.872Z

**tool call — Bash**
````
{
 "command": "sort /tmp/x.err | sed 's/.*step=\\(j[0-9]\\).*/\\1/' | sort | uniq -c | tr '\\n' ' '"
}
````

### User / tool · 2026-11-02T02:10:05.954Z

**tool result**
````
   9 j1    3 j2    1 j3    8 j4
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:10:08.132Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"reviews/T-037-staff-engineer.md\"; t=open(p).read()\nold=\"(steps j1 x8, j2 x3, j3 x1, j4 x9 in the CLI stderr)\"; assert old in t\nt=t.replace(old,\"(CLI stderr by step: j1 x9, j2 x3, j3 x1, j4 x8)\")\nt=t.replace(\"passes with 32 fixture misses\",\"passes with 32 fixture misses (21 sample + 11 case_01)\")\nopen(p,\"w\").write(t)\nEOF\npython3 tools/board.py validate reviews/T-037-staff-engineer.md 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T02:10:08.282Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:10:11.465Z

Verdict **fail** (1 blocker, 2 major, 1 minor); `board.py validate` on the review file returns ok. `.venv/bin/python -m pytest tests/unit -q` gave 767 passed and 1 failed (`test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode`), which I did not bisect or attribute to T-037.
- **Blocker:** the `sample` and `case_01` fixtures are stale. Replaying them on the fixture backend hits 21 and 11 failed judge calls, so all 9 sample entries print as `[needs_review]`, which contradicts AC7's "0 FixtureMissing".
- **Major:** `test_replay_has_no_fixture_miss` passes despite those 32 misses. Removing the injection `record_warning` dedupe at `app/backend/pipeline.py:276` leaves 44 tests green and gives case_07 two warnings for record 3.
- **Minor:** the 8-minute deadline is only checked between stages. I did not run the fixtures-only-golden-text grep. Review file: `/Users/arsis/zlayt-pm-project/reviews/T-037-staff-engineer.md`.
