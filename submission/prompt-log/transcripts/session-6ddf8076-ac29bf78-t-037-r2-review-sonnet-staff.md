# Subagent: T-037 r2 review (sonnet staff) (T-037 r2 review (sonnet staff))

Source: `agent-ac29bf784ea99f62d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:31:25.780Z

Do the round-2 review of board card T-037 in /Users/arsis/zlayt-pm-project. Run `python3 tools/board.py show T-037` for the ACs, the round-1 review, and the notes. Since round 1, the fixtures were re-recorded (commit 31070c3), golden was aligned to D-035 (d6ea199), and unsplit_paste scoring was added (bee1844). The latest eval report is evals/reports/20261102T023039Z.md.

Verify for yourself:
- `python3 -m pytest -q tests/unit` passes.
- `python3 tests/fixtures/make_curated.py --check` passes.
- `python3 -m evals.run` (fixture backend) reproduces the headline metrics.
- Each round-1 finding is resolved or explicitly carried.

Write reviews/T-037-staff-engineer-r2.md, append-only, with a ```json block containing card, persona, verdict and findings. Reply in 2 lines: the verdict, and blockers if any.

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:31:27.028Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T02:31:27.040Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:31:27.373Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-037"
}
````

### User / tool · 2026-11-02T02:31:27.503Z

**tool result**
````
---
id: "T-037"
title: "Pipeline stages, finalize, status, CLI and recorded fixtures for all golden inputs"
milestone: "M2"
role: "backend"
status: "in_progress"
priority: "P0"
depends_on: ["T-032", "T-033", "T-035", "T-036", "T-048"]
created_by: "orchestrator"
created_at: "2026-11-02T01:14:10Z"
updated_at: "2026-11-02T02:31:06Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:10:50Z"
rounds: 1
commits: ["d67a82d", "0d040d3", "fe4e6a2", "81df4e0", "8d485ec"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "fail", "file": "reviews/T-037-staff-engineer.md", "at": "2026-11-02T02:10:27Z"}
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
- 2026-11-02T02:10:27Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): fail — reviews/T-037-staff-engineer.md; round 1; findings:
    - [blocker] Fixtures for sample and case_01 are stale: replay hits 21 and 11 fixture misses, contradicting AC7 and AC1 'all done' evidence — fix: Re-record fixtures for sample and case_01 (and any case whose prompt hashes changed) after the last prompt/template change, then re-run the miss count over all ten inputs.
    - [major] test_replay_has_no_fixture_miss is vacuous: it passes with 32 fixture misses (21 sample + 11 case_01) — fix: Assert on the llm_calls table (or the audited warning) for FIXTURE_MISS rows, and also assert JUDGE_UNAVAILABLE is absent for fixture-backed golden cases.
    - [major] Injection record_warning dedupe has no test: removing the filter at pipeline.py:276 leaves 44 tests green — fix: Add a test running case_07 (or a tagged-record script) and asserting exactly one record_warning per (category, record_no).
    - [minor] Deadline is checked only between stages — fix: Optionally check expired() per record in the flags stage worker and per call batch.
- 2026-11-02T02:10:27Z orchestrator: assigned: backend-2
- 2026-11-02T02:10:50Z backend: claimed
- 2026-11-02T02:11:24Z backend: r1 majors done: replay test now counts failed llm_calls (+ JUDGE_UNAVAILABLE reasons), injection dedupe test (mutant-verified), deadline checked per record in flags stage. test_replay_has_no_fixture_miss[sample/case_01] and test_sample_replay_shows_verified_entries FAIL until backend-1's re-record lands (expected). Committed only my pipeline.py hunks via index (working tree also holds another worker's split_llm edits).
- 2026-11-02T02:31:06Z backend: Re-record (commit 31070c3): golden sample+case_01..09, judge lines (55) and all 7 evals/library packets re-recorded with claude-cli (recorder now accepts evals/library; live recording needs ENABLE_LIVE=1 since the T-053 fixture-by-default rule). Replay on fixture backend: 0 FixtureMiss and 0 judge failures on sample, case_01..09, lib02..07; ONE exception: case_lib01 record 3 extract fails live on all attempts because the model reasons aloud and emits two JSON objects (INVALID_JSON); shows as LLM_FAILED_AFTER_RETRIES. Fix = harden extract_v1 ('your whole reply is one JSON object'), which re-records every extract call and rebuilds curated; not done, say if wanted. Eval evals/reports/20261102T023039Z.md: grounding 1.0, entry_recall 0.982, amount_recall 1.0, halluc catch 1.0 (40/40), flag precision/recall 1.0 all four types, must_not hits 0; ship_bar false only for live-only metrics (fixture backend).

## Handoff
Added pipeline.py stages 0-7 (run_ingest, ingest_case, run_pipeline, persistence that preserves review status on rerun, 8-min deadline via injectable now), CLI (python -m app.pipeline via shim app/pipeline.py - outside owned paths, please ratify), eval helpers run_case/judge_summary/case_view, record.py --judges, provider.record_fragment_context, audited._DB_LOCK. Fixtures: 279 files recorded with claude-cli for sample, case_01..09, 55 judge lines (40 halluc, 10 controls, SE1-5). Verified: pytest tests/unit/test_pipeline.py + test_t037_backend.py 43 passed; CLI 0.4 s on fixtures. Left: any prompt change by T-035/T-036 invalidates fixtures -> re-record (python -m app.llm.record; ~1 min/case). Surprised me: one sqlite connection shared by worker threads corrupted table_info reads (fixed with a lock); claude-cli extract call occasionally fails 3x (case_02 re-recorded).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:31:28.009Z

**tool call — Bash**
````
{
 "command": "ls .claude/agent-memory/staff-engineer-reviewer/ && git log --oneline | head -15"
}
````

### User / tool · 2026-11-02T02:31:28.108Z

**tool result**
````
MEMORY.md
project_backend_llm_review_patterns.md
project_db_review_patterns.md
project_design_review_patterns.md
project_e2e_contract_review_patterns.md
project_eval_runner_review_patterns.md
project_harness_review_patterns.md
project_llm_stage_review_patterns.md
project_round2_snapshot_review_patterns.md
project_split_llm_review_patterns.md
project_t050_namespacing_review_patterns.md
project_wiring_review_patterns.md
636a042 feat(frontend): draft treatment paragraph panel with citations, accept/dismiss (T-059 UI)
31070c3 chore(backend): re-record fixtures for D-028 prompts, record library packets (T-037/T-053)
bee1844 feat(evals): score unsplit_paste (D-031) in evals.run; report on recorded fixtures (T-057 minor)
d6ea199 test(golden): D-035 patient_report only on explicit Patient/Pt clauses (sample E1, case_06 E3)
d0c9cdb test(backend): month May is not the modal hedge (T-030 follow-up)
a27b358 feat(backend): D-035 clause-level patient_report, no speaker lists (T-061 r3)
473ac2a docs(architect): T-063 LLM_SPLIT row and D-031..D-035 additions
b365af3 fix(backend): T-057 r1 - re-split replaces stored records, split failures surface, audit prompt_version, pinned coverage tests, eval report
d796383 feat(frontend): manual entry for records without an entry, Entered by reviewer chip (T-056 B1)
e83eb54 fix(backend): T-056 r1 - hard 422 for figures absent from the quote (D-034), duplicate charge follows the split, entered_by label and override notes
37c0923 fix(backend): silence pypdf logging, stop extraction at the deadline, pin runtime deps (T-054 r1)
f5444a8 fix(frontend): keep an amount's own kind after review; stable needs-review ordering (T-044)
709397e docs(contract): review/batch and export_config (T-055, T-058)
20d866f feat(backend): draft treatment paragraph in firm voice, grounded and judged (T-059, D-031)
dbb2c66 feat(backend): batch accept of verified entries and per-case export config (T-055, T-058)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:31:29.782Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/staff-engineer-reviewer/project_round2_snapshot_review_patterns.md .claude/agent-memory/staff-engineer-reviewer/project_llm_stage_review_patterns.md | head -80; git status --short | head -20; git rev-parse HEAD; cat reviews/T-037-staff-engineer.md | head -60"
}
````

### User / tool · 2026-11-02T02:31:29.942Z

**tool result**
````
---
name: round2-snapshot-review-patterns
description: T-040 r2 and T-043 r2 (2026-11-01): HEAD moves mid-review, git archive needs untracked fixtures, mutation method, guard traps, overwritten review file
metadata:
  type: project
---

Round-2 reviews of T-040 (security) and T-043 (paralegal) ran while other agents committed to the same branch. HEAD moved about six times in one session (5542dfd -> 700ca9a -> 7364096 -> 7a450a1 -> 5216d06 -> 099732b -> dd545e3 -> c61e84f).

**Why:** A test result or live check is only valid for the hash it ran against. Quote the hash in every review, and re-run the required command at the end of the review.

**How to apply:**
- Snapshot the reviewed commit with `git archive <sha> | tar -x -C <scratch>`, then copy untracked files in (`git ls-files --others --exclude-standard`, through a small Python copier because BSD `cp` has no `--parents`). `.gitattributes` has no export-ignore, but a commit can lack files that a later commit adds. 077e294 lacks `tests/fixtures/llm/*.json` (added by 0d040d3), so `FIXTURE_MISS` fails 7 tests. Overlaying HEAD's fixtures isolates the code question from the fixture-ordering question.
- Mutation checks run in a scratch copy via a Python driver (`mutate_api.py` pattern in artifacts/review-evidence/T-040-r2-mutate_api.py). Result shape: drop the delete_case line, drop the CSP line, disable the Content-Length precheck. A test that still passes with the control removed is a finding (here the body-cap test).
- Live checks: start uvicorn from the snapshot with DATA_DIR in scratch, get listener PIDs with `lsof -nP -iTCP:<port> -sTCP:LISTEN`, and kill those PIDs by number. A PID file from `nohup ... &` in a subshell can point at a dead parent.
- Guard traps (board-guard / git-guard in this repo): `kill $(cat ...)` is denied (command substitution in command position); `rm -rf "$VAR/..."` is denied; `awk` with `>` or `NR>1` is read as a redirect into a product path; `grep "<style"` is read as redirect; a `2>&1 | tail` inside an echo string is denied. Put shell logic in a scratch .py file and run it with `.venv/bin/python -I`.
- Overwrite hazard: `Write` on an existing reviews/ file replaces it silently. Before writing `reviews/<card>-<persona>-r2.md`, check for an existing file and the card's reviews list (`board show <card>`). An earlier round-2 review for T-040 existed (verdict changes, 02:17:03Z) and was overwritten; it was untracked, so it could not be restored from git.
- Fixes can land between a review's findings and its re-check: at c61e84f the PDF route moved to a threadpool with a 10 s cap and a demo refusal before parse. Re-measure any performance claim on the current HEAD before rating it.
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
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
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
 M .claude/hooks/reviewer_write_guard.py
636a0423cdce02e36c12352223e6176440de105d
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:31:32.355Z

**tool call — Bash**
````
{
 "command": "ls reviews | grep T-037; git rev-parse --short HEAD; .venv/bin/python -m pytest -q tests/unit 2>&1 | tail -8"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:31:32.676Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python tests/fixtures/make_curated.py --check 2>&1 | tail -8; echo exit=$?"
}
````

### User / tool · 2026-11-02T02:31:51.598Z

**tool result**
````
T-037-staff-engineer.md
636a042
........................................................................ [ 56%]
........................................................................ [ 64%]
........................................................................ [ 72%]
........................................................................ [ 80%]
........................................................................ [ 88%]
........................................................................ [ 96%]
...............................                                          [100%]
895 passed in 18.49s
````

### User / tool · 2026-11-02T02:31:52.102Z

**tool result**
````
entries: 9 non-verified: []
letter equal: True | notes equal: True
exit=0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:31:53.761Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python tests/fixtures/make_curated.py --check >/dev/null 2>&1; echo check_exit=$?; ls evals/reports | tail -5; cp evals/reports/latest.json /private/tmp/claude-501/x.json 2>/dev/null; .venv/bin/python -m evals.run 2>&1 | tail -40; echo exit=$?; ls evals/reports | tail -5"
}
````

### User / tool · 2026-11-02T02:31:55.740Z

**tool result**
````
check_exit=0
20261102T021046Z.md
20261102T022701Z.md
20261102T022927Z.md
20261102T023039Z.md
latest.json
llm call failed call_id=c541f7329696b step=extract attempt=1 prompt_hash=e02650eaff3b56a59664e6c6efe611cfde00a438a6671ac91403a65ebcdb3431
llm call failed call_id=c8d24dbf0c290 step=extract attempt=1 prompt_hash=4b3235bcc27fc57d8df381ddb636080623de75ee126ef90ad5acc8fb69609bfb
llm call failed call_id=cadbf74b06796 step=extract attempt=1 prompt_hash=dd11310acca4a716f8a2e2bd69d7bac58b0fb9eb95ccb23835d4e980bdde1011
llm call failed call_id=c9aa44d61d01f step=conflicts attempt=1 prompt_hash=72f2b8a330ffbf0fe899b1558f048a20e812d19112dca07a3b4e2469aba19140
llm call failed call_id=cdd6d977eb63a step=flags attempt=1 prompt_hash=aba7985fd2cf66130a268227a931481f6fd49a86d8fc7dc85134687ef05737ef
llm call failed call_id=c9fb690ae29a5 step=flags attempt=1 prompt_hash=8ef7ba54619423c4d84c9bc0e224a30770fe63001b5b91d7bb0db899efbdffef
llm call failed call_id=c037436b661f4 step=flags attempt=1 prompt_hash=6492c1869040382bbd047206c9f36c4c49e8a71b2c3d09c8de75be6be2747427
ship_bar_met=False backend=fixture report=/Users/arsis/zlayt-pm-project/evals/reports/20261102T023155Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
exit=0
20261102T022701Z.md
20261102T022927Z.md
20261102T023039Z.md
20261102T023155Z.md
latest.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:31:58.666Z

**tool call — Bash**
````
{
 "command": "git status --short evals | head; diff <(sed 1d evals/reports/20261102T023039Z.md) <(sed 1d evals/reports/20261102T023155Z.md) | head -40; head -60 evals/reports/20261102T023155Z.md"
}
````

### User / tool · 2026-11-02T02:31:58.781Z

**tool result**
````
 M evals/reports/latest.json
?? evals/reports/20261102T023155Z.md
# Eval report 2026-11-02T02:31:55Z

**ship_bar_met: False**  backend `fixture`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`

Blockers: 4_no_invented_facts; backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
| grounding_rate | 1.000 (236 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
| unsupported_count_3run | None | 0 | R-TL-4 |
| determinism_3run | None | 1.0 | R-CO-7 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| lexicon_recall_must_flags (reported, not gated) | 1.000 | none (D-026) | R-FL-3, R-RV-6 |

Assertions: {"gap_28_not_flagged": true, "gap_73_flagged": true, "all_gap_rows_correct": true}
spec_matches_golden: True

## Misses (report what was found)

- entry misses: {"case_06_subtle_pre_existing": [{"entry": "E3", "why": "excerpt misses must_contain_excerpt"}]}
- missed must flags: {}
- grounding failures: []
- seeded hallucinations not caught: []
- must_not detail: {}

## Prompt and lexicon hashes

- `app/llm/prompts/conflicts_v1.md` 16c18d05e68a5cfa0fa6496497b377dfbcda3c19fbf04dfaa9c9cf36139932ca
- `app/llm/prompts/extract_v1.md` 11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2
- `app/llm/prompts/flags_v1.md` d5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725
- `app/llm/prompts/judge_amount_class_v1.md` e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8
- `app/llm/prompts/judge_conflict_v1.md` 10c7cfddbd32d78cbdb005a14731abcb40ef55c83265b87abb88f74c48551daa
- `app/llm/prompts/judge_faithfulness_v1.md` 636bd46d728af66608aba566efe431371e49e32a066fca71b2046534adbd002b
- `app/llm/prompts/judge_flag_v1.md` 97dd90e3d9546a836d327e12953c9c30ba574ebdcc6073ada9162cd480d2e432
- `app/llm/prompts/narrative_v1.md` 3d75a823c717359208322d17ba8b77fd58893a4aa15bc92a18c48c78e94e12ac
- `app/llm/prompts/split_v1.md` 9a2d0cffafa37f318e18a9c076c82f9f5c404ecb53781956813fafe7bf66197b
- `app/llm/lexicon.yaml` a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:02.046Z

**tool call — Bash**
````
{
 "command": "grep -rn \"4_no_invented_facts\" evals/run.py | head; .venv/bin/python -m evals.run 2>&1 >/dev/null | grep -c \"llm call failed\"; .venv/bin/python -m evals.run 2>&1 >/dev/null | grep \"llm call failed\" | sed 's/.*step=\\([a-z_0-9]*\\).*/\\1/' | sort | uniq -c; git status --short evals/reports"
}
````

### User / tool · 2026-11-02T02:32:04.296Z

**tool result**
````
evals/run.py:510:        "4_no_invented_facts": m["hallucination_catch_rate"].get("judge_unavailable_count", 0) == 0 and m["judge_unavailable_in_cases"]["value"] == 0
7
   1 conflicts
   3 extract
   3 flags
 M evals/reports/latest.json
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:07.249Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json\nd=json.load(open('evals/reports/latest.json'))\nprint(d.keys())\nfor k in ('judge_unavailable_in_cases','blockers','ship_bar'):\n    print(k, json.dumps(d.get(k) or d.get('metrics',{}).get(k))[:800])\nEOF\n.venv/bin/python -m evals.run 2>&1 >/dev/null | grep \"llm call failed\" | head -3"
}
````

### User / tool · 2026-11-02T02:32:08.654Z

**tool result**
````
dict_keys(['assertions', 'backend', 'backend_requested', 'bars', 'blockers', 'cases', 'generated_at', 'hashes', 'internal_notes_equal', 'letter_equal', 'metrics', 'models', 'per_case', 'schema', 'ship_bar_met', 'spec_matches_golden', 'thresholds'])
judge_unavailable_in_cases {"per_case": {}, "value": 0}
blockers ["4_no_invented_facts", "backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)"]
ship_bar null
llm call failed call_id=c6afb1cd52393 step=extract attempt=1 prompt_hash=e02650eaff3b56a59664e6c6efe611cfde00a438a6671ac91403a65ebcdb3431
llm call failed call_id=c8ade665a039f step=extract attempt=1 prompt_hash=4b3235bcc27fc57d8df381ddb636080623de75ee126ef90ad5acc8fb69609bfb
llm call failed call_id=cf85a77cc44aa step=extract attempt=1 prompt_hash=dd11310acca4a716f8a2e2bd69d7bac58b0fb9eb95ccb23835d4e980bdde1011
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:10.740Z

**tool call — Bash**
````
{
 "command": "sed -n 495,540p evals/run.py; .venv/bin/python -I -c \"\nimport json;d=json.load(open('evals/reports/latest.json'));print(json.dumps(d['bars'],indent=0)); print(d['metrics']['hallucination_catch_rate'])\""
}
````

### User / tool · 2026-11-02T02:32:10.863Z

**tool result**
````
        return {"value": False, "status": "not_run"}
    ok = results["case_07_prompt_injection"]["amounts"]["total_ok"] and results["case_07_prompt_injection"]["amounts"]["charge_sum_cents"] == 42000
    return {"value": bool(ok), "r_ids": RIDS["case_07_total_420"]}


def ship_bar(m, a, backend, spec_ok):
    """Four automated bars (row 5, reviewability, is persona + E2E and is not computed here). Missing/unmeasured => bar fails."""
    th = THRESHOLDS
    def ge(x, t):
        return x is not None and x >= t
    b = {
        "1_grounding": ge(m["grounding_rate"]["value"], th["grounding_rate"]),
        "2_recall": ge(m["entry_recall"]["value"], th["entry_recall"]) and ge(m["amount_recall"]["value"], th["amount_recall"]),
        "3_flags": all(ge(m["flag_precision"][t], th["flag_precision"]) and ge(m["flag_recall"][t], th["flag_recall"]) for t in FLAG_TYPES)
                   and a["gap_28_not_flagged"] and a["gap_73_flagged"],
        "4_no_invented_facts": m["hallucination_catch_rate"].get("judge_unavailable_count", 0) == 0 and m["judge_unavailable_in_cases"]["value"] == 0
                               and ge(m["hallucination_catch_rate"]["value"], th["hallucination_catch_rate"]) and not m["hallucination_catch_rate"]["controls_unsupported"]
                               and m["golden_must_not_hits"]["value"] == 0 and m["unsplit_paste"]["value"] is True and m["case_07_total_420"]["value"] is True
                               and m["unsupported_count_3run"].get("value") == 0 and m["unsupported_count_3run"].get("runs") == 3
                               and m["determinism_3run"].get("value") == 1.0 and m["determinism_3run"].get("runs") == 3,
    }
    blockers = [k for k, v in b.items() if not v]
    for k in ("determinism_3run", "unsupported_count_3run"):
        if backend in LIVE_BACKENDS and m[k].get("runs") != 3:
            blockers.append(f"{k}: {m[k].get('reason') or 'not measured over exactly 3 live runs'}")
    if backend not in LIVE_BACKENDS:
        blockers.append(f"backend={backend}: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)")
    if m["hallucination_catch_rate"].get("judge_unavailable_count", 0):
        blockers.append(f"hallucination_catch_rate not_measured: judge unavailable on {m['hallucination_catch_rate']['judge_unavailable_count']} line(s) (stale or missing judge fixtures?)")
    if m["judge_unavailable_in_cases"]["value"]:
        blockers.append(f"judge unavailable on {m['judge_unavailable_in_cases']['value']} item(s) in the golden cases: {m['judge_unavailable_in_cases']['per_case']}")
    if m["amount_recall"]["total_mismatch"]:
        blockers.append("charge total differs from golden in " + ", ".join(m["amount_recall"]["total_mismatch"]))
    if m["entry_recall"]["dedupe_failures"]:
        blockers.append("dedupe failures in " + ", ".join(m["entry_recall"]["dedupe_failures"]))
    if not spec_ok:
        blockers.append("spec_matches_golden is false")
    return b, blockers


def evaluate_report(report):
    """Recompute ship_bar_met from a report's own numbers (used by the tampered-report test and the runner)."""
    b, blockers = ship_bar(report["metrics"], report["assertions"], report["backend"], report["spec_matches_golden"])
    return not blockers, b, blockers


{
"1_grounding": true,
"2_recall": true,
"3_flags": true,
"4_no_invented_facts": false
}
{'caught': 40, 'caught_by_code': 31, 'caught_by_judge_only': 9, 'controls_flagged_by_code': ['S07'], 'controls_partially': [], 'controls_total': 10, 'controls_unsupported': [], 'judge_unavailable_count': 0, 'judge_unavailable_ids': [], 'missed': [], 'r_ids': ['R-TL-4', 'R-TL-10'], 'status': 'measured', 'total': 40, 'value': 1.0}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:13.519Z

**tool call — Bash**
````
{
 "command": "git diff 81df4e0 HEAD --stat -- app/backend/pipeline.py app/llm tests/unit/test_t037_backend.py tests/unit/test_pipeline.py | tail -20; sed -n 1,80p tests/unit/test_t037_backend.py"
}
````

### User / tool · 2026-11-02T02:32:13.644Z

**tool result**
````
 app/backend/pipeline.py         | 51 +++++++++++++++++++++++++++-----------
 app/llm/audited.py              |  7 +++++-
 app/llm/lexicon.yaml            | 23 ++++++++++++-----
 app/llm/prompts/narrative_v1.md | 14 +++++++++++
 app/llm/prompts/split_v1.md     | 13 ++++++++++
 app/llm/provider.py             | 11 +++++++--
 app/llm/record.py               |  6 ++---
 tests/unit/test_t037_backend.py | 55 ++++++++++++++++++++++++++++++++++++-----
 8 files changed, 148 insertions(+), 32 deletions(-)
"""T-037 additions (backend): CLI on the fixture backend, fixture replay completeness (0 FixtureMiss), eval-facing helpers, persistence.
Golden data only; no key, no network."""
import json
import os
import subprocess
import sys
import time
import pathlib
import pytest
from app.backend import pipeline as PL
from app.db import db as DB
from app.llm import provider as P
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]
FIX = ROOT / "tests" / "fixtures" / "llm"
needs_fixtures = pytest.mark.skipif(not list(FIX.glob("*.json")), reason="no recorded fixtures yet")


@needs_fixtures
def test_cli_sample_on_fixture_backend_under_60s():
    """T-037 AC1: `python -m app.pipeline evals/golden/sample.txt` prints 9 entries, the 73-day gap, $8,390 detected, exit 0, < 60 s."""
    t0 = time.time()
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "LLM_BACKEND")}
    p = subprocess.run([sys.executable, "-m", "app.pipeline", "evals/golden/sample.txt"], cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)
    assert p.returncode == 0 and time.time() - t0 < 60, p.stderr[-500:]
    assert "entries: 9" in p.stdout and "Gap of 73 days" in p.stdout and "$8,390.00" in p.stdout and "ERRORS" not in p.stdout


def replay(case, tmp_path):
    """Run the whole pipeline on the fixture backend against a real DB; returns (output, llm_calls rows)."""
    conn = DB.connect(str(tmp_path / f"{case}.sqlite"))
    cid = DB.create_case(conn, G.raw(case), now=1.0)
    out = PL.run_pipeline(conn, cid, G.raw(case), now=lambda: 1.0)
    return out, DB.list_llm_calls(conn, cid)


@needs_fixtures
@pytest.mark.parametrize("case", ["sample"] + [c for c in G.case_names() if c != "sample"])
def test_replay_has_no_fixture_miss(case, monkeypatch, tmp_path):
    """T-037 AC2/AC7: replaying every golden input on the fixture backend makes 0 failed model calls (llm_calls rows with an error) and leaves no
    JUDGE_UNAVAILABLE / FIXTURE_MISS reason on any item. Fails when a fixture is missing or stale (a prompt changed since recording)."""
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    out, calls = replay(case, tmp_path)
    failed = [c for c in calls if c["error"]]
    assert not failed, f"{case}: {len(failed)} failed calls, steps {sorted({c['step'] for c in failed})}"
    assert out["errors"] == [] and out["status"] == "done"
    items = out["entries"] + out["undated_entries"] + out["amounts"] + out["flags"]
    assert not [i for i in items if {"FIXTURE_MISS", "JUDGE_UNAVAILABLE"} & set(i.get("reasons", []))], case


@needs_fixtures
def test_sample_replay_shows_verified_entries(monkeypatch, tmp_path):
    """The headline demo case replays with its entries verified (not all needs_review)."""
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    out, _ = replay("sample", tmp_path)
    assert len(out["entries"]) == 9 and sum(e["state"] == "verified" for e in out["entries"]) >= 7


@needs_fixtures
def test_injection_record_gets_exactly_one_record_warning(monkeypatch, tmp_path):
    """Review: stage 0 makes the record_warning flag; the per-record flag pass must not add a second one. case_07 -> one for record 3."""
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    out, _ = replay("case_07_prompt_injection", tmp_path)
    ws = [f for f in out["flags"] if f["type"] == "record_warning" and f["category"] == "injection_suspected"]
    assert [f["record_ids"] for f in ws] == [["r3"]]


def test_deadline_applies_inside_the_flags_stage(tmp_path):
    """Review minor: a clock that expires mid-flags-stage stops the remaining records; status is timeout and only finished flags are kept."""
    from tests.unit._fakes import FakeCall, sample_script
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    ticks = {"n": 0}

    def clock():                           # stays under the limit through the stage guards, then jumps past it once flags start
        ticks["n"] += 1
        return 0.0 if ticks["n"] < 12 else 1000.0
    call = FakeCall(sample_script())
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=clock, deadline_s=480)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:16.354Z

**tool call — Bash**
````
{
 "command": "git ls-files tests/fixtures/llm | wc -l; ls tests/fixtures/llm | wc -l; git status --short tests/fixtures | head -3; .venv/bin/python -m pytest -q tests/unit -rs 2>&1 | tail -3; .venv/bin/python -m pytest -q tests/unit/test_t037_backend.py -k replay_has_no 2>&1 | tail -3"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:16.881Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p evals/run.py | head -80; grep -n \"def run_case\\|library\\|lib0\" evals/run.py | head -30"
}
````

### User / tool · 2026-11-02T02:32:35.064Z

**tool result**
````
     577
     532
 M tests/fixtures/llm/3571166930f3ee019a7d2d0b254863e710d259d1b5da4d458ca4eadae9cf7c6b.json
 M tests/fixtures/llm/35f88fbe68632afb7e5f3efb286b5364006950e624594f057dca25d7ef3d2192.json
 M tests/fixtures/llm/3a5c185e71a4fab40b3d4a735c2af0eb9d14eef489161f85fda8e8c0586c3048.json
........................................................................ [ 96%]
...............................                                          [100%]
895 passed in 16.90s
..........                                                               [100%]
10 passed, 10 deselected in 0.69s
````

### User / tool · 2026-11-02T02:32:35.149Z

**tool result**
````
"""Eval runner: `python -m evals.run` scores the product against the golden set and writes
evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).

    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)
    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk

Pipeline contract consumed (backend T-037 provides; the runner is unit-tested against a fake):
    app.pipeline.run_case(text: str, backend: str) -> dict          the GET /api/cases/{token} shape (memory/contracts/api.md):
        records, entries, undated_entries, amounts, totals, flags, tray, warnings, backend, models{generator,judge}
        entry: record_ids, date, date_status, provider, summary, excerpt, state, reasons, ladder{judge{verdict}}
        amount: record_ids, text, value_cents, kind;  flag: type, evidence[{record_id, excerpt}], computed{from,to,days}
    app.pipeline.judge_summary(summary, excerpt, label, backend) -> "supported" | "partially" | "unsupported" | "unavailable"
Metrics that need a live model (determinism_3run, unsupported_count_3run) are `not_measured` on the fixture backend, and
ship_bar_met is false there (R-CO-7). Names mirror REQUIREMENTS section 7.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import sys

from evals.matching import assign_detail, norm

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ROOT / "evals" / "golden"
REPORTS = ROOT / "evals" / "reports"
REQUIREMENTS = ROOT / "spec" / "REQUIREMENTS.md"
LIVE_BACKENDS = ("claude-cli", "anthropic-api")
NOT_MEASURED = {"value": None, "status": "not_measured"}

THRESHOLDS = {"grounding_rate": 1.0, "entry_recall": 0.95, "amount_recall": 0.95, "flag_precision": 0.9, "flag_recall": 0.9,
              "hallucination_catch_rate": 0.95, "unsupported_count_3run": 0, "determinism_3run": 1.0}
RIDS = {"grounding_rate": ["R-TL-2", "R-TL-9", "R-FL-5", "R-EX-2"], "entry_recall": ["R-TL-1", "R-TL-7"], "amount_recall": ["R-CH-1"],
        "flag_precision": ["R-FL-1", "R-FL-2", "R-FL-3", "R-FL-4"], "flag_recall": ["R-FL-1", "R-FL-2", "R-FL-3", "R-FL-4"],
        "hallucination_catch_rate": ["R-TL-4", "R-TL-10"], "unsupported_count_3run": ["R-TL-4", "R-CH-7"], "determinism_3run": ["R-CO-7"],
        "lexicon_recall_must_flags": ["R-FL-3", "R-RV-6"], "golden_must_not_hits": ["R-CO-3"], "case_07_total_420": ["R-RV-6"]}
FLAG_TYPES = ("gap", "conflict", "pre_existing", "causation")


# ---------------------------------------------------------------- helpers
def rn(rid):
    """'r12' -> 12 (record id to record number); ints pass through."""
    if isinstance(rid, int):
        return rid
    m = re.search(r"\d+", str(rid))
    return int(m.group()) if m else None


def low(s):
    return norm(s).lower()


def ratio(num, den):
    return None if den == 0 else num / den


334:def run_cases(pipeline, backend, cases=None):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:37.682Z

**tool call — Bash**
````
{
 "command": "git status --short tests/fixtures | awk '{print $1}' | sort | uniq -c; git status --short | grep -v agent-memory | head -30; ls -lt tests/fixtures/llm | head -5; git log -3 --format='%h %ci %s'"
}
````

### User / tool · 2026-11-02T02:32:37.843Z

**tool result**
````
   4 M
 M .claude/hooks/reviewer_write_guard.py
 M app/backend/api.py
 M board/activity.jsonl
 M board/cards/T-030.md
 M board/cards/T-036.md
 M board/cards/T-037.md
 M board/cards/T-039.md
 M board/cards/T-040.md
 M board/cards/T-043.md
 M board/cards/T-044.md
 M board/cards/T-045.md
 M board/cards/T-050.md
 M board/cards/T-052.md
 M board/cards/T-053.md
 M board/cards/T-054.md
 M board/cards/T-055.md
 M board/cards/T-056.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-060.md
 M board/cards/T-061.md
 M board/cards/T-062.md
 M evals/reports/latest.json
 M memory/LESSONS.md
 M memory/SCOPE_CUTS.md
 M tests/e2e/test_charges.py
 M tests/e2e/test_edit.py
 M tests/e2e/test_export_ui.py
 M tests/e2e/test_flags_panel.py
total 4232
-rw-r--r--@  1 arsis  staff   261 Nov  1 20:31 3571166930f3ee019a7d2d0b254863e710d259d1b5da4d458ca4eadae9cf7c6b.json
-rw-r--r--@  1 arsis  staff   281 Nov  1 20:31 d32270051a558dc270ee37faf3470cd58015a790d4d615c10ea470c4a547c389.json
-rw-r--r--@  1 arsis  staff   425 Nov  1 20:31 35f88fbe68632afb7e5f3efb286b5364006950e624594f057dca25d7ef3d2192.json
-rw-r--r--@  1 arsis  staff   474 Nov  1 20:31 3a5c185e71a4fab40b3d4a735c2af0eb9d14eef489161f85fda8e8c0586c3048.json
fa8a36e 2026-11-01 20:32:06 -0600 docs: D-036 amends D-020 for local-mode library packets (T-053 r2 F2)
636a042 2026-11-01 20:31:16 -0600 feat(frontend): draft treatment paragraph panel with citations, accept/dismiss (T-059 UI)
31070c3 2026-11-01 20:30:53 -0600 chore(backend): re-record fixtures for D-028 prompts, record library packets (T-037/T-053)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:39.844Z

**tool call — Bash**
````
{
 "command": "date; git diff --stat tests/fixtures | tail -5; git diff tests/fixtures | head -40"
}
````

### User / tool · 2026-11-02T02:32:39.968Z

**tool result**
````
Sun Nov  1 20:32:39 CST 2026
 ...66930f3ee019a7d2d0b254863e710d259d1b5da4d458ca4eadae9cf7c6b.json | 2 +-
 ...fbe68632afb7e5f3efb286b5364006950e624594f057dca25d7ef3d2192.json | 6 +++---
 ...85e71a4fab40b3d4a735c2af0eb9d14eef489161f85fda8e8c0586c3048.json | 2 +-
 ...0051a558dc270ee37faf3470cd58015a790d4d615c10ea470c4a547c389.json | 2 +-
 4 files changed, 6 insertions(+), 6 deletions(-)
diff --git a/tests/fixtures/llm/3571166930f3ee019a7d2d0b254863e710d259d1b5da4d458ca4eadae9cf7c6b.json b/tests/fixtures/llm/3571166930f3ee019a7d2d0b254863e710d259d1b5da4d458ca4eadae9cf7c6b.json
index ea4c581..c9e92eb 100644
--- a/tests/fixtures/llm/3571166930f3ee019a7d2d0b254863e710d259d1b5da4d458ca4eadae9cf7c6b.json
+++ b/tests/fixtures/llm/3571166930f3ee019a7d2d0b254863e710d259d1b5da4d458ca4eadae9cf7c6b.json
@@ -6,6 +6,6 @@
  "recorded_from": {
   "backend": "claude-cli",
   "model": "claude-sonnet-5-5",
-  "recorded_at": "2026-11-02T02:28:39Z"
+  "recorded_at": "2026-11-02T02:31:35Z"
  }
 }
\ No newline at end of file
diff --git a/tests/fixtures/llm/35f88fbe68632afb7e5f3efb286b5364006950e624594f057dca25d7ef3d2192.json b/tests/fixtures/llm/35f88fbe68632afb7e5f3efb286b5364006950e624594f057dca25d7ef3d2192.json
index 33702a0..2bdce3a 100644
--- a/tests/fixtures/llm/35f88fbe68632afb7e5f3efb286b5364006950e624594f057dca25d7ef3d2192.json
+++ b/tests/fixtures/llm/35f88fbe68632afb7e5f3efb286b5364006950e624594f057dca25d7ef3d2192.json
@@ -1,11 +1,11 @@
 {
  "output": {
-  "excerpt": "C/O neck stiffness. Transported to Marrowgate General ED.",
-  "summary": "Driver of a sedan struck from behind while stopped at a light complained of neck stiffness and was transported to Marrowgate General ED."
+  "excerpt": "Driver of a sedan struck from behind while stopped at a light. C/O neck stiffness. Transported to Marrowgate General ED.",
+  "summary": "Driver of a sedan struck from behind while stopped at a light; complained of neck stiffness; transported to Marrowgate General ED."
  },
  "recorded_from": {
   "backend": "claude-cli",
   "model": "claude-sonnet-5-5",
-  "recorded_at": "2026-11-02T02:28:33Z"
+  "recorded_at": "2026-11-02T02:31:29Z"
  }
 }
\ No newline at end of file
diff --git a/tests/fixtures/llm/3a5c185e71a4fab40b3d4a735c2af0eb9d14eef489161f85fda8e8c0586c3048.json b/tests/fixtures/llm/3a5c185e71a4fab40b3d4a735c2af0eb9d14eef489161f85fda8e8c0586c3048.json
index 6c9b994..13be14e 100644
--- a/tests/fixtures/llm/3a5c185e71a4fab40b3d4a735c2af0eb9d14eef489161f85fda8e8c0586c3048.json
+++ b/tests/fixtures/llm/3a5c185e71a4fab40b3d4a735c2af0eb9d14eef489161f85fda8e8c0586c3048.json
@@ -6,6 +6,6 @@
  "recorded_from": {
   "backend": "claude-cli",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:44.453Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/snap && git archive fa8a36e | tar -x -C $S/snap && ls $S/snap | head; ls $S/snap/tests/fixtures/llm | wc -l; ls .venv >/dev/null && echo venv"
}
````

### User / tool · 2026-11-02T02:32:44.834Z

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
     532
venv
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:32:48.835Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap && P=/Users/arsis/zlayt-pm-project/.venv/bin/python; $P -m pytest -q tests/unit 2>&1 | tail -3; $P tests/fixtures/make_curated.py --check 2>&1 | tail -3; echo check=$?; $P -m evals.run 2>/tmp/ignore.err | tail -5; grep -c \"llm call failed\" /tmp/ignore.err; grep \"llm call failed\" /tmp/ignore.err | sed 's/.*step=\\([a-z_0-9]*\\).*/\\1/' | sort | uniq -c; head -12 evals/reports/latest.json >/dev/null; ls evals/reports | tail -2"
}
````

### User / tool · 2026-11-02T02:33:09.441Z

**tool result**
````
........................................................................ [ 96%]
...............................                                          [100%]
895 passed in 18.12s
entries: 9 non-verified: []
letter equal: True | notes equal: True
check=0
ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap/evals/reports/20261102T023309Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
7
   1 conflicts
   3 extract
   3 flags
20261102T023309Z.md
latest.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:14.080Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap && sed -n 334,380p evals/run.py; grep -n \"case_names\\|def cases\" evals/run.py | head"
}
````

### User / tool · 2026-11-02T02:33:14.169Z

**tool result**
````
def run_cases(pipeline, backend, cases=None):
    """Score every golden case. Returns per-case dicts plus the raw outputs for the live-only checks."""
    results, outs = {}, {}
    for name, text, exp in (cases or golden_cases()):
        out = pipeline.run_case(text, backend)
        outs[name] = out
        results[name] = {"entries": score_entries(exp, out), "amounts": score_amounts(exp, out), "flags": score_flags(exp, out),
                         "record_warning_misses": score_record_warnings(exp, out), "must_not_hits": check_must_not(exp, out),
                         "unsupported_summaries": unsupported_summaries(out), "judge_unavailable": judge_unavailable_in(out), "grounding": grounding(text, out)}
    return results, outs


# ---------------------------------------------------------------- hallucinations (rung 1 code + rung 2 judge)
def parse_record_text(rt):
    """'Record 8 | 2026-05-29 | Austin Imaging, cervical MRI | "excerpt"' -> (label, date, excerpt)."""
    m = re.match(r'Record \d+ \| ([^|]*) \| (.*?) \| "(.*)"\s*$', rt, re.S)
    if not m:
        return "", "", rt
    return m.group(2).strip(), m.group(1).strip(), m.group(3)


def judge_item(item, judge, check_summary):
    label, date, excerpt = parse_record_text(item["record_text"])
    code = list(check_summary(item["candidate_summary"], excerpt, label, date)) if check_summary else []   # a crash propagates: no silent code-rung loss
    verdict = judge(item["candidate_summary"], excerpt, label)
    return {"id": item["id"], "code_reasons": code, "verdict": verdict}


def hallucination_metrics(items, controls, judge, check_summary=None):
    """catch = code check raised a reason OR judge said partially/unsupported/unavailable-is-NOT-a-catch. Rate over EVERY seeded line."""
    rows = [judge_item(i, judge, check_summary) for i in items]
    caught = [r for r in rows if r["code_reasons"] or r["verdict"] in ("partially", "unsupported")]
    crows = [judge_item(c, judge, check_summary) for c in controls]
    unavailable = [r["id"] for r in rows + crows if r["verdict"] == "unavailable"]
    return {"total": len(items), "caught": len(caught), "judge_unavailable_count": len(unavailable), "judge_unavailable_ids": unavailable,
            "status": "not_measured" if unavailable else "measured", "value": ratio(len(caught), len(items)),
            "missed": [r["id"] for r in rows if r not in caught],
            "caught_by_code": sum(1 for r in rows if r["code_reasons"]), "caught_by_judge_only": sum(1 for r in caught if not r["code_reasons"]),
            "controls_total": len(controls), "controls_unsupported": [r["id"] for r in crows if r["verdict"] == "unsupported"],
            "controls_flagged_by_code": [r["id"] for r in crows if r["code_reasons"]],
            "controls_partially": [r["id"] for r in crows if r["verdict"] == "partially"]}


def load_jsonl(p):
    return [json.loads(l) for l in pathlib.Path(p).read_text().splitlines() if l.strip()]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:18.726Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap && cat > ../probe.py <<'EOF'\nimport os, sys\nos.environ[\"LLM_BACKEND\"]=\"fixture\"\nsys.path.insert(0, os.getcwd())\nfrom evals import run as R\nimport logging\nfrom app import pipeline as PL\nfor name, text, exp in R.golden_cases():\n    import io, contextlib\n    buf=io.StringIO()\n    h=logging.StreamHandler(buf); logging.getLogger().addHandler(h)\n    out = PL.run_case(text, \"fixture\")\n    logging.getLogger().removeHandler(h)\n    n=buf.getvalue().count(\"llm call failed\")\n    print(name, \"failed_calls_logged=\", n, \"warnings=\", [w.get(\"code\") if isinstance(w,dict) else w for w in out.get(\"warnings\",[])][:4])\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I ../probe.py 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T02:33:19.526Z

**tool result**
````
sample failed_calls_logged= 0 warnings= []
case_01_date_formats failed_calls_logged= 0 warnings= ['DATE_EXCLUDED_FROM_GAPS']
case_02_gap_boundaries failed_calls_logged= 0 warnings= []
case_03_rate_and_ocr failed_calls_logged= 0 warnings= []
case_04_duplicates_no_amounts failed_calls_logged= 0 warnings= ['DUPLICATE_MERGED']
case_05_provider_conflict failed_calls_logged= 0 warnings= []
case_06_subtle_pre_existing failed_calls_logged= 0 warnings= []
case_07_prompt_injection failed_calls_logged= 0 warnings= ['INJECTION_SUSPECTED']
case_08_diagnosis_temptation failed_calls_logged= 0 warnings= []
case_09_nonvisit_hides_gap failed_calls_logged= 0 warnings= []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:23.448Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap && grep -rn \"lib01\\|case_lib\" evals/*.py tests/unit/*.py | head -8; ls evals/library | head -12; grep -n \"evals/library\\|library\" evals/run.py | head"
}
````

### User / tool · 2026-11-02T02:33:23.546Z

**tool result**
````
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
case_lib06_lop_billed_vs_adjusted.expected.json
case_lib06_lop_billed_vs_adjusted.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:28.100Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap && grep -n \"def golden_cases\" -A14 evals/run.py; grep -n \"def main\" -A40 evals/run.py | grep -n \"pipeline\\.\\|run_case\\|unsplit\\|split\" | head"
}
````

### User / tool · 2026-11-02T02:33:28.197Z

**tool result**
````
61:def golden_cases():
62-    names = ["sample"] + sorted(p.name[:-len(".expected.json")] for p in GOLD.glob("case_*.expected.json"))
63-    return [(n, (GOLD / f"{n}.txt").read_text(), json.loads((GOLD / f"{n}.expected.json").read_text())) for n in names]
64-
65-
66-def sha256_file(p):
67-    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
68-
69-
70-def hashes(root=ROOT):
71-    """sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml (CONTRACT 8.3 regression discipline)."""
72-    out = {}
73-    for p in sorted((root / "app" / "llm" / "prompts").glob("*.md")):
74-        out[p.relative_to(root).as_posix()] = sha256_file(p)
75-    lex = root / "app" / "llm" / "lexicon.yaml"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:31.209Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap && grep -n \"unsplit\" evals/run.py | head -12"
}
````

### User / tool · 2026-11-02T02:33:31.302Z

**tool result**
````
295:def score_unsplit(pipeline, backend):
296:    """D-031 / T-057: evals/golden/unsplit_paste.{txt,split.json}. The code split sees one block; the model proposes boundaries; code validates
299:    exp = json.loads((GOLD / "unsplit_paste.split.json").read_text())
300:    text = (GOLD / "unsplit_paste.txt").read_text()
512:                               and m["golden_must_not_hits"]["value"] == 0 and m["unsplit_paste"]["value"] is True and m["case_07_total_420"]["value"] is True
552:    m["unsplit_paste"] = score_unsplit(pipeline, backend)
597:          f"| unsplit_paste (LLM split, D-031) | {m['unsplit_paste']['value']} {m['unsplit_paste']['misses']} | true | R-IN-1 |",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:34.171Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap && sed -n 295,332p evals/run.py"
}
````

### User / tool · 2026-11-02T02:33:34.259Z

**tool result**
````
def score_unsplit(pipeline, backend):
    """D-031 / T-057: evals/golden/unsplit_paste.{txt,split.json}. The code split sees one block; the model proposes boundaries; code validates
    them and parses every field. Expected: 3 records with the golden date and source (from code), each carrying exactly one LLM_SPLIT record_warning.
    On the fixture backend the recorded split reply lives in tests/fixtures/llm/split."""
    exp = json.loads((GOLD / "unsplit_paste.split.json").read_text())
    text = (GOLD / "unsplit_paste.txt").read_text()
    saved = os.environ.get("LLM_FIXTURE_DIR")
    if backend == "fixture":
        os.environ["LLM_FIXTURE_DIR"] = str(ROOT / "tests" / "fixtures" / "llm" / "split")
    try:
        out = pipeline.run_case(text, backend)
    finally:
        if saved is None:
            os.environ.pop("LLM_FIXTURE_DIR", None)
        else:
            os.environ["LLM_FIXTURE_DIR"] = saved
    recs = {rn(r.get("n", r.get("id"))): r for r in out.get("records") or []}
    misses = []
    if len(recs) != len(exp["records"]):
        misses.append(f"record count {len(recs)} != {len(exp['records'])}")
    warn = {}
    for f in out.get("flags") or []:
        if f.get("type") == "record_warning" and f.get("category") == "llm_split":
            for e in f.get("evidence", [])[:1]:
                warn[rn(e.get("record_id", e.get("record_no")))] = warn.get(rn(e.get("record_id", e.get("record_no"))), 0) + 1
    for g in exp["records"]:
        r = recs.get(g["record_no"])
        if r is None:
            misses.append(f"record {g['record_no']} missing")
            continue
        if r.get("date_iso") != g["date"]:
            misses.append(f"record {g['record_no']} date {r.get('date_iso')} != {g['date']}")
        if norm(r.get("source")) != norm(g["source"]):
            misses.append(f"record {g['record_no']} source differs")
        if warn.get(g["record_no"], 0) != 1:
            misses.append(f"record {g['record_no']} has {warn.get(g['record_no'], 0)} LLM_SPLIT warnings, want 1")
    return {"value": not misses, "misses": misses, "records": len(recs), "r_ids": ["R-IN-1", "R-RV-6"]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:42.544Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap && ls tests/fixtures/llm/split | wc -l; cat > ../probe2.py <<'EOF'\nimport os, sys\nos.environ[\"LLM_BACKEND\"]=\"fixture\"; sys.path.insert(0, os.getcwd())\nos.environ[\"LLM_FIXTURE_DIR\"]=os.path.join(os.getcwd(),\"tests/fixtures/llm/split\")\nfrom evals import run as R\nfrom app import pipeline as PL\nt=(R.GOLD/\"unsplit_paste.txt\").read_text()\nout=PL.run_case(t,\"fixture\")\nprint(\"entries\",len(out[\"entries\"]),[e[\"state\"] for e in out[\"entries\"]], \"undated\", len(out.get(\"undated_entries\",[])))\nprint(\"warnings\", out.get(\"warnings\"))\nprint(\"errors\", out.get(\"errors\"), \"status\", out.get(\"status\"))\nprint(\"flags\", [(f[\"type\"],f.get(\"category\")) for f in out[\"flags\"]])\nprint({k:v for k,v in R.score_unsplit(PL,\"fixture\").items()})\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I ../probe2.py 2>&1 | grep -v \"llm call failed\""
}
````

### User / tool · 2026-11-02T02:33:42.891Z

**tool result**
````
       1
entries 0 [] undated 0
warnings [{'code': 'LLM_SPLIT', 'message': 'The pasted text had no recognisable record markers; the AI proposed the record boundaries and code checked them. Check the split.', 'item_id': None}, {'code': 'CONFLICT_PASS_INCOMPLETE', 'stage': 'conflicts', 'item_id': 'f_cx1', 'message': 'The check for conflicts between records did not finish; conflicts may be missing.'}]
errors [{'code': 'LLM_FAILED_AFTER_RETRIES', 'stage': 'extract', 'record_no': 1, 'cause': 'FIXTURE_MISS'}, {'code': 'LLM_FAILED_AFTER_RETRIES', 'stage': 'extract', 'record_no': 2, 'cause': 'FIXTURE_MISS'}, {'code': 'LLM_FAILED_AFTER_RETRIES', 'stage': 'extract', 'record_no': 3, 'cause': 'FIXTURE_MISS'}, {'code': 'CONFLICT_PASS_INCOMPLETE', 'stage': 'conflicts', 'record_no': None, 'cause': 'CONFLICT_CHECK_INCOMPLETE'}] status done_with_errors
flags [('record_warning', 'analysis_incomplete'), ('record_warning', 'llm_split'), ('record_warning', 'llm_split'), ('record_warning', 'llm_split')]
{'value': True, 'misses': [], 'records': 3, 'r_ids': ['R-IN-1', 'R-RV-6']}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:53.790Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap && cat > ../probe3.py <<'EOF'\nimport os, sys, glob\nos.environ[\"LLM_BACKEND\"]=\"fixture\"; sys.path.insert(0, os.getcwd())\nfrom app import pipeline as PL\nfor p in sorted(glob.glob(\"evals/library/*.txt\")):\n    out=PL.run_case(open(p).read(),\"fixture\")\n    print(os.path.basename(p), out[\"status\"], len(out[\"entries\"]), [e[\"code\"]+\":\"+str(e.get(\"record_no\")) for e in out[\"errors\"]], sorted({e[\"state\"] for e in out[\"entries\"]}))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I ../probe3.py 2>&1 | grep -v \"llm call failed\"; grep -rn \"evals/library\\|case_lib\" tests/unit/*.py | head -5\nfor i in 1 2; do /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.pipeline evals/golden/sample.txt > ../cli$i.out 2> ../cli$i.err; echo exit=$?; done; cmp ../cli1.out ../cli2.out && echo identical; wc -c ../cli1.err; grep -c \"needs_review\" ../cli1.out; grep -E \"entries:|Gap of|8,390\" ../cli1.out | head"
}
````

### User / tool · 2026-11-02T02:33:55.268Z

**tool result**
````
case_lib01_er_only_then_gap.txt done_with_errors 5 ['LLM_FAILED_AFTER_RETRIES:3'] ['needs_review', 'verified']
case_lib02_slip_fall_prior_knee.txt done 7 [] ['needs_review', 'verified']
case_lib03_truck_rear_end_chiro.txt done 7 [] ['verified']
case_lib04_dog_bite_scar_revision.txt done 6 [] ['verified']
case_lib05_pedestrian_orif_hardware.txt done 8 [] ['verified']
case_lib06_lop_billed_vs_adjusted.txt done 7 [] ['needs_review', 'verified']
case_lib07_parking_lot_fall_outside_records.txt done 7 [] ['verified']
exit=0
exit=0
identical
       0 ../cli1.err
6
Status: done   backend: fixture   records: 9   entries: 9   flags: 10   amounts: 3
  [verified] Gap of 73 days - Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).
  Charges detected, pending review (not a total): $8,390.00; accepted so far: $0.00
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:33:59.329Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cut -c1-150 cli1.out | head -40"
}
````

### User / tool · 2026-11-02T02:33:59.408Z

**tool result**
````
Status: done   backend: fixture   records: 9   entries: 9   flags: 10   amounts: 3

TIMELINE
  January 9, 2026 - Austin EMS run report [verified]
      41M restrained driver, rear-ended at approx. 35 mph, complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
  January 9, 2026 - Central ER discharge summary [verified]
      Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with 
  January 16, 2026 - Dr. Alvarez, primary care [verified]
      Persistent neck pain 6/10 with daily headaches; referred to physical therapy 2x/week for 6 weeks.
  January 23, 2026 - Capital PT, initial evaluation [verified]
      Cervical range of motion reduced approx. 40%. Plan of care is 12 visits. Charge per visit $185.
  February 20, 2026 - Capital PT, visit 8 [verified]
      Pain 4/10, improving. Patient reports missing 3 days of work.
  March 6, 2026 - Capital PT, visit 9 [verified]
      Discharged from PT after two missed appointments. Pain 3/10.
  May 18, 2026 - Hill Country Pain Management, new patient [verified]
      New onset pain radiating to right arm with numbness in fingers; pain 7/10; MRI ordered.
  May 29, 2026 - Austin Imaging, cervical MRI [verified]
      Cervical MRI showed C5-C6 disc protrusion with mild right foraminal narrowing; findings may represent degenerative change, correlate clinically.
  June 12, 2026 - Hill Country Pain Management, follow-up [verified]
      Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.

GAPS
  [verified] Gap of 73 days - Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).

CONFLICTS
  [verified] Stated accident date is later than recorded treatment - Stated accident date January 19, 2026 (“Date of accident per intake form: 2026-
  [needs_review] Treatment plan and what followed differ - Capital PT, initial evaluation (January 23, 2026): “Plan of care: 12 visits.” Capital P

PRE-EXISTING
  [verified] Mention of a prior or pre-existing condition - Dr. Alvarez, primary care (January 16, 2026) mentions a prior or pre-existing condition: �
  [needs_review] Degenerative wording - Austin Imaging, cervical MRI (May 29, 2026) uses degenerative wording: “Findings may represent degenerative 

CAUSATION LANGUAGE
  [verified] Missed or ended care - Wording about missed appointments or ending care in Capital PT, visit 9 (March 6, 2026): “Discharged from PT aft
  [needs_review] Accident date source - Accident date as stated in Hill Country Pain Management, new patient (May 18, 2026): “Date of accident per i
  [needs_review] New-onset wording - New-onset wording in Hill Country Pain Management, new patient (May 18, 2026): “New onset pain radiating to rig
  [verified] Hedged wording - Hedged wording in Austin Imaging, cervical MRI (May 29, 2026): “Findings may represent degenerative change; correlate 
  [needs_review] Patient self-report - Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:34:03.785Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/snap && grep -n \"injection_suspected\\|expired\\|record_warning\" app/backend/pipeline.py | head -30"
}
````

### User / tool · 2026-11-02T02:34:03.874Z

**tool result**
````
73:    for w in ing["record_warnings"]:
75:        inj = w["category"] == "injection_suspected"
78:        flags.append({"id": w["id"], "type": "record_warning", "category": w["category"], "origin": "code", "title": w["title"],
224:    def expired():
246:        if timed_out or expired():
290:            if expired():                    # the deadline also applies inside the stage, record by record
296:            if fs is None or expired():
299:            fs = [f for f in fs if f["type"] != "record_warning"]          # stage 0 already made the record_warning flag
318:    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
432:                         ("RECORD WARNINGS", ("record_warning",))):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:34:10.806Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > mut.py <<'EOF'\nimport shutil, subprocess, sys, os, pathlib\nSNAP=pathlib.Path(\"snap\"); PY=\"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\ndef run(name, edit):\n    d=pathlib.Path(\"mut_\"+name)\n    if d.exists(): shutil.rmtree(d)\n    shutil.copytree(SNAP,d,ignore=shutil.ignore_patterns(\"evals/reports\",\"__pycache__\",\".pytest_cache\"))\n    edit(d)\n    r=subprocess.run([PY,\"-m\",\"pytest\",\"-q\",\"-x\",\"tests/unit/test_pipeline.py\",\"tests/unit/test_t037_backend.py\",\"-p\",\"no:cacheprovider\"],cwd=d,capture_output=True,text=True)\n    print(name, \"->\", r.stdout.strip().splitlines()[-1])\ndef sub(rel, old, new):\n    def f(d):\n        p=d/rel; t=p.read_text(); assert t.count(old)==1,(rel,old,t.count(old)); p.write_text(t.replace(old,new))\n    return f\nrun(\"dedupe\", sub(\"app/backend/pipeline.py\",\"fs = [f for f in fs if f[\\\"type\\\"] != \\\"record_warning\\\"]\",\"fs = list(fs)\"))\nrun(\"flagsdeadline\", sub(\"app/backend/pipeline.py\",\"            if expired():                    # the deadline also applies inside the stage, record by record\",\"            if False:\"))\ndef rmfix(d):\n    import json\n    # remove one sample extract fixture (a golden extract call)\n    fs=sorted((d/\"tests/fixtures/llm\").glob(\"*.json\"))\n    # find a fixture whose output has an excerpt from sample record 1\n    for f in fs:\n        t=f.read_text()\n        if \"Austin EMS\" in t and '\"excerpt\"' in t:\n            f.unlink(); return\n    raise SystemExit(\"none\")\nrun(\"rmfixture\", rmfix)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I mut.py 2>&1 | tail"
}
````

### User / tool · 2026-11-02T02:34:17.067Z

**tool result**
````
dedupe -> 1 failed, 39 passed in 2.46s
flagsdeadline -> 1 failed, 40 passed in 2.32s
none
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:34:22.384Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && sed -i.bak 's/\"Austin EMS\" in t and/\"cyclobenzaprine\" in t and/; s/^run(\"dedupe\".*$//; s/^run(\"flagsdeadline\".*$//' mut.py && cat >> mut.py <<'EOF'\ndef rmjudge(d):\n    for f in sorted((d/\"tests/fixtures/llm\").glob(\"*.json\")):\n        t=f.read_text()\n        if '\"verdict\"' in t:\n            f.unlink(); return\nrun(\"rmjudgefixture\", rmjudge)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I mut.py 2>&1 | tail"
}
````

### User / tool · 2026-11-02T02:34:27.937Z

**tool result**
````
rmfixture -> 1 failed, 27 passed in 1.86s
rmjudgefixture -> 1 failed, 41 passed in 2.53s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:34:30.904Z

**tool call — Bash**
````
{
 "command": "git diff 81df4e0 fa8a36e -- app/backend/pipeline.py app/llm/audited.py app/llm/provider.py app/llm/record.py | grep -E '^[+-]' | grep -vE '^(\\+\\+\\+|---)' | cut -c1-200 | head -120"
}
````

### User / tool · 2026-11-02T02:34:31.013Z

**tool result**
````
-                         judges, totals as TT, why as WHY)
+                         judges, split_llm, totals as TT, why as WHY)
-def run_ingest(raw_text: str) -> dict:
-    """All-code stage 0. Raises IngestError('bad_request' | 'input_too_large') before anything else. Zero model calls."""
-    ing = IN.ingest(raw_text)
+def run_ingest(raw_text: str, call=None, not_duplicates=()) -> dict:
+    """Stage 0. Raises IngestError('bad_request' | 'input_too_large') before anything else. Zero model calls, except the D-031 split
+    fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
+    ing = IN.ingest(raw_text, splitter=split_llm.make_splitter(call) if call else None, not_duplicates=not_duplicates)
-        state, why_codes = confidence.compose_state({"code_reasons": []}, {"injection": inj, "date_status": None if inj else "ambiguous"})
+        ctx = {"llm_split": True} if w["category"] == "llm_split" else {"injection": inj, "date_status": None if inj else "ambiguous"}
+        state, why_codes = confidence.compose_state({"code_reasons": []}, ctx)
+        if w["category"] == "llm_split":      # trace the flag to the audited split call (prompt version, model, call id)
+            flags[-1]["ladder"]["generator"] = {"model": judges.generator_model(), "prompt_version": "split_v1", "call_id": w.get("call_id")}
-    for a in AM.extract_amounts(recs):
-        r = by_n[a["record_no"]]
-        body = r["excerpt"]
-        item = {"id": a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
-                "cents": a["cents"], "value_cents": a["cents"], "cls": a["cls"], "kind": a["cls"], "start": a["start"], "end": a["end"],
-                "excerpt": body, "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending"}
+    sep = {int(str(i)[1:]) for i in not_duplicates if str(i)[1:].isdigit()}
+    for a in AM.extract_amounts(recs, separate=sep):
+        item = amount_item(a, by_n[a["record_no"]])
-    return {"text": text, "records": recs, "groups": ing["groups"], "split_method": ing["split_method"], "banner": ing["banner"],
+    return {"text": text, "records": recs, "groups": ing["groups"], "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "banner": ing["banner"],
+def amount_item(a: dict, r: dict, item_id: str = None) -> dict:
+    """The pipeline's amount item from an amounts.extract_amounts row and its record."""
+    return {"id": item_id or a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
+            "cents": a["cents"], "value_cents": a["cents"], "cls": a["cls"], "kind": a["cls"], "start": a["start"], "end": a["end"],
+            "excerpt": r["excerpt"], "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending"}
+
+
+def _not_duplicates(conn, cid: str) -> list:
+    return list(((DB.get_case(conn, cid) or {}).get("config") or {}).get("not_duplicates", []))
+
+
-    ing = run_ingest(raw_text)
+    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
-    ing = run_ingest(raw_text)
+    ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid))
+    if ing.get("split_failure") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
+        errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_failure"] == "FIXTURE_MISS" else None))
+    if ing["split_method"] == "llm":
+        # the stored records come from the creation-time code split (one unsplit block) or from an earlier run's model split: the model is
+        # not deterministic, so the records are replaced on EVERY LLM-split run, before any entry or flag is written
+        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
+            if expired():                    # the deadline also applies inside the stage, record by record
+                return r, None
+            if fs is None or expired():
+                timed_out = True
+                continue
+PROMPT_OF_STEP = {"extract": "extract_v1", "j1": "judge_faithfulness_v1", "j2": "judge_amount_class_v1", "j3": "judge_conflict_v1",
+                  "j4": "judge_flag_v1", "conflicts": "conflicts_v1", "flags": "flags_v1", "split": "split_v1", "narrative": "narrative_v1"}
+
+
-        return audited_call(conn, case_id, step, m[role_for(step)], system, user, schema, item_id=item_id, now=now, validate=validate)
+        return audited_call(conn, case_id, step, m[role_for(step)], system, user, schema, item_id=item_id, now=now, validate=validate,
+                            prompt_version=PROMPT_OF_STEP.get(step))
+LIBRARY_DIR = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"    # committed SYNTHETIC packets (D-031, T-052)
-    return os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
+    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
+    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
+    (D-008/D-020, T-053 security r1): no code path sends a model call from a demo."""
+    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
+    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
+        return "fixture"
+    return name
-        for p in sorted(GOLDEN_DIR.glob("*.txt")):
+        for p in sorted(GOLDEN_DIR.glob("*.txt")) + sorted(LIBRARY_DIR.glob("*.txt")):
-    golden = P.GOLDEN_DIR.resolve()
-    if golden not in p.parents or p.suffix != ".txt":
-        raise ValueError(f"{path} is not a .txt under evals/golden; refusing to record")
+    allowed = [P.GOLDEN_DIR.resolve(), P.LIBRARY_DIR.resolve()]
+    if not any(a in p.parents for a in allowed) or p.suffix != ".txt":
+        raise ValueError(f"{path} is not a .txt under evals/golden or evals/library; refusing to record")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:34:31.999Z

**tool call — Bash**
````
{
 "command": "grep -rlE \"sk-ant|ANTHROPIC_API_KEY=<redacted> (RSA|PRIVATE)\" tests/fixtures | head -3; echo secrets-grep-done; grep -nE \"except:|except Exception: *pass|float\\(|sleep\\(\" app/backend/pipeline.py app/llm/audited.py | head"
}
````

### User / tool · 2026-11-02T02:34:32.099Z

**tool result**
````
secrets-grep-done
app/llm/audited.py:91:            sleep(RETRY_DELAYS_S[attempt - 1])         # short, capped, code-controlled
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:34:36.069Z

**tool call — Bash**
````
{
 "command": "rm -f evals/reports/20261102T023155Z.md evals/reports/20261102T023203Z.md evals/reports/20261102T023204Z.md; git checkout -- evals/reports/latest.json; git status --short evals; rm -f /tmp/ignore.err"
}
````

### User / tool · 2026-11-02T02:34:36.122Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (rm evals/reports/20261102T023155Z.md)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:35:12.954Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-037-staff-engineer-r2.md",
 "content": "# T-037 round 2: staff-engineer-reviewer\n\nVerdict: pass (0 blockers, 0 majors, 2 minors). All four round-1 findings are resolved. Two new minors are noted. One is the lib01 failure that the worker already disclosed.\n\nPinned commit: fa8a36e (the HEAD observed at 20:32 local time, after 31070c3, bee1844 and d6ea199). HEAD moved during the review (636a042, then fa8a36e). The working tree also had 4 fixture JSONs under tests/fixtures/llm modified by another agent's live recording (`recorded_at` 02:31:29 and 02:31:35). So I ran every check twice, once in the live tree and once in a `git archive fa8a36e` snapshot in the scratchpad (532 fixture files, same as the tree). The snapshot results are the ones I rely on.\n\n## Exercised\n- `.venv/bin/python -m pytest -q tests/unit`: 895 passed, 0 skipped. Same result in the live tree and in the fa8a36e snapshot.\n- `.venv/bin/python tests/fixtures/make_curated.py --check`: exit 0 (\"entries: 9 non-verified: []\", \"letter equal: True | notes equal: True\").\n- `.venv/bin/python -m evals.run` (fixture backend), live tree and snapshot. The headline metrics match `evals/reports/20261102T023039Z.md` line for line: grounding 1.000 (236 checked), entry_recall 0.982, amount_recall 1.000, all four flag types 1.000/1.000, hallucination catch 40/40 with 0 judge unavailable, controls 0 of 10, must_not 0, unsplit_paste True, case_07_total_420 True. `diff` of the two reports (header line removed) is empty. ship_bar_met is False with blockers `4_no_invented_facts` and the live-only determinism/unsupported_3run. I confirmed in `evals/run.py:510` and in latest.json that bar 4 fails only because `unsupported_count_3run` and `determinism_3run` are unmeasured on the fixture backend. The hallucination, controls and judge-unavailable sub-conditions are all clean.\n- `python -m app.pipeline evals/golden/sample.txt` in the snapshot, twice. Exit 0 both times, stdout byte-identical (`cmp`), stderr 0 bytes. Output shows 9 entries (all `[verified]`), \"Gap of 73 days\" `[verified]`, \"$8,390.00\" detected and not a total, 10 flags.\n- A per-case replay on the fixture backend, with a probe script in the scratchpad. All ten golden inputs have 0 failed model calls, and the test `test_replay_has_no_fixture_miss` passes for all ten.\n- A replay of the seven `evals/library` packets: lib02 to lib07 are clean. lib01 is `done_with_errors` (see finding 1).\n- A replay of `evals/golden/unsplit_paste.txt` with `LLM_FIXTURE_DIR=tests/fixtures/llm/split` (see finding 2).\n- Scratch-copy mutation of `app/backend/pipeline.py` and of the fixture dir (`mut.py` in the scratchpad), running test_pipeline.py and test_t037_backend.py:\n\n| Mutant | Round 1 | Round 2 |\n|---|---|---|\n| Remove the record_warning dedupe (`fs = [f for f in fs if f[\"type\"] != \"record_warning\"]`) | not caught (44 passed) | caught (1 failed) |\n| Disable the per-record `expired()` check inside the flags stage | not tested | caught (1 failed) |\n| Delete one sample extract fixture | stale fixtures went unnoticed | caught (1 failed) |\n| Delete one judge fixture | not tested | caught (1 failed) |\n\n- Read the diff 81df4e0..fa8a36e for `app/backend/pipeline.py`, `app/llm/audited.py`, `app/llm/provider.py` and `app/llm/record.py`, and the new tests in `tests/unit/test_t037_backend.py`. Grepped those files for bare `except:`, `except Exception: pass`, `float(` and `sleep(`: the only hit is `audited.py:91`, a capped code-controlled retry delay. Grepped tests/fixtures for `sk-ant`, `ANTHROPIC_API_KEY=<redacted> and private-key headers: no hits.\n\n## Round-1 findings, status\n1. **Blocker, stale fixtures (sample 21 misses, case_01 11 misses): resolved.** Commit 31070c3 re-recorded the fixtures. Sample and case_01 now make 0 failed calls (replay probe and 10 parametrized tests). The CLI prints all 9 entries `[verified]` with an empty stderr.\n2. **Major, vacuous `test_replay_has_no_fixture_miss`: resolved.** The test at `tests/unit/test_t037_backend.py:41-52` now asserts no `llm_calls` row has an error. It also asserts no FIXTURE_MISS or JUDGE_UNAVAILABLE reason on any item, and that `out[\"errors\"] == []`. Deleting one fixture makes it fail.\n3. **Major, injection dedupe untested: resolved.** `test_injection_record_gets_exactly_one_record_warning` (case_07 gives `[[\"r3\"]]`) fails when the filter at `pipeline.py:299` is removed.\n4. **Minor, deadline checked only between stages: resolved.** `pipeline.py:290` and `:296` check `expired()` per record. `test_deadline_applies_inside_the_flags_stage` fails when the check is disabled.\n\n## New findings\nBoth are minor. Neither blocks the card.\n\n1. **Minor (carried): case_lib01 record 3 fails extract live and on the fixture replay.** The extract reply contains two JSON objects, so INVALID_JSON, then LLM_FAILED_AFTER_RETRIES. The library packet replays as `done_with_errors`. The failure is visible, not a silent default, and the backend disclosed it in the 02:31:06Z note and offered the `extract_v1` fix. But no unit test replays the library packets, so lib02 to lib07 are unguarded against the next prompt change, and lib01 would go red as soon as one was added. The product already shows the error, so I did not rate it higher. It is T-053's packet, but the root cause (the extract prompt allowing a reply with prose and two objects) sits in T-037's recorded-fixture scope.\n2. **Minor: `unsplit_paste` scores True while its pipeline run mostly fails, and every eval run logs 7 \"llm call failed\" lines.** `evals/run.py:295-332` points `LLM_FIXTURE_DIR` at `tests/fixtures/llm/split`, which holds one file (the split reply). Running that input gives status `done_with_errors`, 0 entries, 3 extract errors with `cause: FIXTURE_MISS`, and `CONFLICT_PASS_INCOMPLETE`. The metric only checks the record count, dates, sources and LLM_SPLIT warnings, so True is correct for what it claims (R-IN-1). The cost is that every `python -m evals.run` prints 7 `llm call failed` lines (3 extract, 3 flags, 1 conflicts) that look like the failure round 1 was about, and someone triaging stderr cannot tell them from real misses.\n\n## Hygiene note\nMy two `python -m evals.run` runs in the live tree wrote four new untracked report files and rewrote the tracked `evals/reports/latest.json`. I could not delete them because the reviewer hook blocks writes outside `reviews/`. The metrics are identical to the committed report. The orchestrator can remove the untracked `evals/reports/20261102T0231*.md` and `20261102T02320*.md` files and `git checkout evals/reports/latest.json`.\n\n```json\n{\"card\": \"T-037\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"round 2; pinned fa8a36e (git archive snapshot in scratchpad plus live tree); commits 31070c3, d6ea199, bee1844 since round 1; app/backend/pipeline.py, app/llm/audited.py, app/llm/provider.py, app/llm/record.py, tests/unit/test_t037_backend.py, tests/unit/test_pipeline.py, tests/fixtures/llm, evals/run.py; CLI on evals/golden/sample.txt (fixture backend)\",\n \"exercised\": [\"pytest -q tests/unit: 895 passed, 0 skipped (live tree and fa8a36e snapshot)\", \"tests/fixtures/make_curated.py --check: exit 0\", \"python -m evals.run on fixture backend in live tree and snapshot: headline metrics identical to evals/reports/20261102T023039Z.md; ship_bar_met False only for live-only 3-run metrics\", \"python -m app.pipeline evals/golden/sample.txt x2 in snapshot: exit 0, stdout byte-identical, stderr empty, 9 verified entries, 73-day gap, $8,390.00\", \"probe replay of all 10 golden inputs on fixture backend: 0 failed calls\", \"probe replay of 7 evals/library packets: lib02..07 clean, lib01 record 3 LLM_FAILED_AFTER_RETRIES\", \"probe replay of unsplit_paste with LLM_FIXTURE_DIR=tests/fixtures/llm/split: done_with_errors, 0 entries, 3 extract FIXTURE_MISS\", \"scratch-copy mutation: dedupe removal, flags-stage deadline check, delete one extract fixture, delete one judge fixture - all caught\", \"read diff 81df4e0..fa8a36e of pipeline.py, audited.py, provider.py, record.py and test_t037_backend.py; grep for bare except, float(, sleep(, secrets in fixtures\"],\n \"verdict\": \"pass\",\n \"scores\": {\"llm_vs_code_separation\": 4, \"failure_visibility\": 4, \"test_strength\": 4, \"determinism_and_fixtures\": 4, \"stage_and_status_contract\": 4},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"Carried: case_lib01 record 3 extract fails (INVALID_JSON, two JSON objects) and no test replays the library packets\",\n   \"evidence\": \"Probe replay of evals/library/case_lib01_er_only_then_gap.txt on fixture backend: status done_with_errors, errors [LLM_FAILED_AFTER_RETRIES record 3]; lib02..07 status done with no errors. grep -rn 'evals/library|case_lib' tests/unit/*.py returns nothing. Backend note 02:31:06Z discloses the failure and the extract_v1 hardening is 'not done, say if wanted'.\",\n   \"why_it_matters\": \"The failure is visible (not a silent default), but a demo packet shows an error and lib02..07 are unprotected against the next prompt change; the extract prompt tolerating a reply with two JSON objects is a reliability gap in the recorded-fixture work.\",\n   \"fix\": \"Harden extract_v1 ('your whole reply is one JSON object'), re-record, and add library packets to the replay parametrization of test_replay_has_no_fixture_miss.\",\n   \"acceptance_test\": \"test_replay_has_no_fixture_miss is parametrized over evals/library/*.txt and passes for all seven; deleting one library fixture makes it fail.\"},\n  {\"severity\": \"minor\", \"title\": \"unsplit_paste scores True while its pipeline run has 3 extract fixture misses; every eval run logs 7 'llm call failed' lines\",\n   \"evidence\": \"evals/run.py:295-332 sets LLM_FIXTURE_DIR to tests/fixtures/llm/split (1 file). Replay: status done_with_errors, entries 0, errors [extract record 1, 2, 3: FIXTURE_MISS, CONFLICT_PASS_INCOMPLETE]. `python -m evals.run 2>&1 >/dev/null | grep 'llm call failed'` gives 7 lines (3 extract, 3 flags, 1 conflicts).\",\n   \"why_it_matters\": \"The metric is correctly scoped to the split stage, but the expected failures are logged exactly like real fixture misses, so a reader of stderr cannot tell round-1-style staleness from the known split-only packet.\",\n   \"fix\": \"Either record the downstream calls for unsplit_paste into the split fixture dir, or have score_unsplit state in the report that downstream stages are intentionally unfixtured and silence or label those log lines.\",\n   \"acceptance_test\": \"`python -m evals.run` on the fixture backend prints 0 'llm call failed' lines, or the report contains a line stating the 7 expected misses for unsplit_paste.\"}\n ],\n \"whats_right\": [\"test_replay_has_no_fixture_miss now counts failed llm_calls rows and reason codes, and fails when a fixture file is deleted\", \"Fixtures are committed, the CLI is byte-identical across runs with empty stderr, and the eval headline reproduces exactly from the report\", \"Every round-1 gap (dedupe, per-record deadline) now has a test that a scratch mutant breaks\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T02:35:13.115Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-037-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:35:16.253Z

**tool call — Bash**
````
{
 "command": "git status --short evals/reports"
}
````

### User / tool · 2026-11-02T02:35:16.346Z

**tool result**
````
 M evals/reports/latest.json
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:35:19.530Z

Four, as written. The file is correct.

Verdict: pass for T-037 round 2 (0 blockers, 0 majors, 2 minors). All four round-1 findings are resolved, and I confirmed each with a scratch-copy mutation test that now fails. The 895 unit tests pass, `make_curated.py --check` exits 0, and the `evals.run` headline metrics match report `20261102T023039Z.md`.
Minors: lib01 record 3 extract still fails with INVALID_JSON and no test replays the library packets; unsplit_paste scores True while its run logs 7 "llm call failed" lines.

My `evals.run` runs left four untracked reports in `evals/reports` and rewrote `latest.json`; the reviewer hook blocked me from cleaning them up.

The review is at `/Users/arsis/zlayt-pm-project/reviews/T-037-staff-engineer-r2.md`.
