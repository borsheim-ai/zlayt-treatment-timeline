# Subagent: T-050 r2 verdict (haiku staff) (T-050 r2 verdict (haiku staff))

Source: `agent-a6150e9f5884d2263.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:17:09.492Z

Working directory: /Users/arsis/zlayt-pm-project. Round 2 of T-050 vs reviews/T-050-staff-engineer.md. Run `.venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_db.py -q 2>&1 | tail -2`; confirm app/db/db.py has a user_version check + move-aside/rebuild and test_multicase.py has the rebuild test and a two-case-coexist test at HEAD. Quote outputs. Write reviews/T-050-staff-engineer-r2.md (D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:11.198Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T02:17:11.220Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:11.411Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-050-staff-engineer.md"
}
````

### User / tool · 2026-11-02T02:17:11.417Z

**tool result**
````
1	# T-050 review: staff-engineer (Marcus Lee lens)
2	
3	Verdict: **fail**. The namespacing design is right (composite key, every writer in `app/db/db.py` takes `case=`, ambiguous bare ids raise). The committed change is not runnable for a second case: commit `6c3aeb1` leaves `app/backend/pipeline.py` `_persist` unscoped, so the card's own AC2 test fails at that commit. The three `case=cid` lines exist only as uncommitted working-tree WIP (mixed in with unrelated backend-2 edits). Blocker: F1. Major: F2 (no migration for DB files made before T-050). Minors: F3, F4.
4	
5	Labels: F1 violates AC1/AC2 (two cases coexist; "done" evidence fails at the commit), so it is a blocker. F2 is a persistence-upgrade hazard, rated major. F3 and F4 are "the AC names the wrong place / the AC test is weaker than the AC" and are minor.
6	
7	Tree note: HEAD moved during this review (6c3aeb1 → 4e8f43d by other commits; pipeline.py still has no `case=cid` at 4e8f43d). The first brief-command run gave `36 passed`; a later run gave `1 failed, 40 passed` on a test unrelated to T-050 (see "Outside this card").
8	
9	Model note: this review ran as `claude-haiku-5-5`. The dossier expects `claude-sonnet-5-5`; the record uses the model that ran.
10	
11	```json
12	{"card": "T-050", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
13	 "scope": "commit 6c3aeb1 (card commits) plus the working tree at review time (uncommitted app/backend/pipeline.py WIP); HEAD 4e8f43d checked at the end (pipeline.py unchanged since 6c3aeb1). No live app URL used: the HTTP API was exercised in-process with fastapi TestClient. Sample case and case_01_date_formats.",
14	 "exercised": [
15	  "python3 tools/board.py show T-050 (AC read; commit list 6c3aeb1; ac evidence strings)",
16	  ".venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_api_routes.py -q -> '36 passed in 4.27s' (first run); same command later -> '1 failed, 40 passed in 4.37s' (FAILED test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode; tree had moved to HEAD 4e8f43d)",
17	  ".venv/bin/python -m pytest tests/unit -q (working tree) -> '1 failed, 762 passed in 10.38s' (same unrelated test)",
18	  "git show 6c3aeb1 (full diff of app/db/db.py, app/db/schema.sql, app/backend/review.py, app/backend/present.py, tests/unit/test_api_routes.py, tests/unit/test_multicase.py) read in full",
19	  "git show HEAD:app/backend/pipeline.py | grep -n: lines 137 (add_item), 141 (update_item without case=), 145 (apply_review without case=); git show HEAD:app/backend/pipeline.py | grep -c 'case=cid' -> 0",
20	  "git diff HEAD -- app/backend/pipeline.py: adds case=cid at the same _persist calls (uncommitted), plus unrelated removals of sentences/body_offset/judges_failed",
21	  "artifacts/review-evidence/T-050/t050_check.py run on the working tree (outputs in artifacts/review-evidence/T-050/worktree/stdout.txt): two golden cases into one sqlite file via ingest_case + run_pipeline (Part A) and via POST /api/cases, POST /run, review, DELETE (Part B)",
22	  "same script on git archive 6c3aeb1 (artifacts/review-evidence/T-050/head_6c3aeb1/stdout.txt): RAISED ValueError 'item id a1 exists in several cases; pass case='; API run status=failed, error run_failed for both cases",
23	  "same script on git archive 6c3aeb1^ (artifacts/review-evidence/T-050/pre_6c3aeb1p/stdout.txt): baseline collision reproduced: 'ingest_case case_01_date_formats: RAISED IntegrityError: UNIQUE constraint failed: records.id'",
24	  "artifacts/review-evidence/T-050/legacy_probe.py: pre-T-050 code writes sample into a file, current code opens the same file and ingests case_01 -> 'STEP1 exit 0 ... records= 9', 'STEP2 exit 1 ... sqlite3.IntegrityError: UNIQUE constraint failed: records.id'",
25	  "artifacts/review-evidence/T-050/single_case_probe.py on the archives (single-case run; used only to rule out the single-case path)",
26	  "pytest on the 6c3aeb1 archive with the untracked LLM fixtures copied in (artifacts/review-evidence/T-050/h1_head_plus_fixtures): 'FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids ... 1 failed, 65 passed'; with the working-tree pipeline.py also copied in (h2_head_plus_fixtures_plus_wt_pipeline): '66 passed in 5.19s'",
27	  "pytest on the 4e8f43d archive (artifacts/review-evidence/T-050/head_4e8f43d): '1 failed, 40 passed' (test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode, IndexError at tests/unit/test_api_routes.py:129)",
28	  "artifacts/review-evidence/T-050/mutate.py (scratch copies under artifacts/review-evidence/T-050/mut/, repo not modified): M1 _find not case-scoped -> 2 failed (test_multicase::test_full_pipeline_twice_in_one_file, test_api_routes::test_two_cases_coexist_with_short_display_ids); M2 schema PK (id) only -> 4 failed; M3 llm_calls dropped from _CASE_TABLES -> 6 failed, NOT including test_multicase::test_delete_case_removes_only_that_case; M4 apply_review UPDATE not case-scoped -> 3 failed",
29	  "grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py -> 0 and 0",
30	  "app/db/db.py read in full (_find 104-118, update_item 141-153, apply_review 156-178, delete_case 216-225); app/db/schema.sql read (four PRIMARY KEY (case_id, id) clauses); grep of every DB item call site in app/ (review.py, present.py, pipeline.py, api.py): all pass case=; raw SQL scoped by case_id except llm_calls by random call id"
31	 ],
32	 "verdict": "fail",
33	 "scores": {"composite_pk_and_writers": 4, "committed_state_consistency": 1, "short_display_ids": 5, "delete_case_isolation": 4, "test_adequacy_for_ac": 2, "upgrade_safety": 2, "failure_visibility": 3},
34	 "findings": [
35	  {"severity": "blocker",
36	   "title": "Committed T-050 change leaves pipeline._persist unscoped: a second case's run fails, and the card's own AC2 test fails at 6c3aeb1",
37	   "evidence": "git show HEAD:app/backend/pipeline.py: line 141 'DB.update_item(conn, it[\"id\"], now=now, **row)' and line 145 'DB.apply_review(conn, it[\"id\"], \"reset\", now=now)' carry no case=; 'git show HEAD:app/backend/pipeline.py | grep -c case=cid' -> 0 at 4e8f43d too. The fix exists only as uncommitted diff (git diff HEAD -- app/backend/pipeline.py, lines 139 and 143 in the working tree). Repro 1: git archive 6c3aeb1 into artifacts/review-evidence/T-050/head_6c3aeb1, copy tests/fixtures/llm/*.json in, run .venv/bin/python -m pytest tests/unit/test_api_routes.py tests/unit/test_multicase.py tests/unit/test_db.py tests/unit/test_pipeline.py -q -> 'FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids ... 1 failed, 65 passed'. Repro 2: same tree with the working-tree pipeline.py copied in -> '66 passed in 5.19s'. Repro 3: artifacts/review-evidence/T-050/t050_check.py on head_6c3aeb1 -> 'run_pipeline sample: RAISED ValueError: item id 'a1' exists in several cases; pass case=' and 'run sample: POST=202 final status=failed ... error={'code': 'run_failed'...}' for both cases.",
38	   "why_it_matters": "AC1 and AC2 require two cases to coexist in one file. At the committed revision the second case's run fails, and that is the exact sequence the API performs (create, then run). The card is marked done and AC2 cites a test that fails at the commit. The green tests hide it: test_multicase::test_full_pipeline_twice_in_one_file calls run_pipeline on fresh case ids without ingest_case, so it never reaches the update path. Same pattern as T-030 r2: the fix is green in a unit test while the producer path is not wired.",
39	   "fix": "Commit the case=cid argument on the three _persist calls (pipeline.py:141 and :145 at HEAD; :139 and :143 in the working tree) in a commit that does not carry the unrelated backend-2 WIP, or in the same commit as db.py. Add a test to tests/unit/test_multicase.py that does ingest_case for case B after case A has run, then run_pipeline for case B (the API order).",
40	   "acceptance_test": "From the fix commit: git archive <fix> | tar -x -C <dir>; cd <dir> && .venv/bin/python -m pytest tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids tests/unit/test_multicase.py -q passes; artifacts/review-evidence/T-050/t050_check.py <dir> <out> Part B reports 'final status=ready' for both cases."},
41	  {"severity": "major",
42	   "title": "No migration for sqlite files created before T-050: the new composite key is silently not applied to an existing file",
43	   "evidence": "artifacts/review-evidence/T-050/legacy_probe.py output: 'STEP1 exit 0 pre-code ingest sample ok, records= 9' then 'STEP2 exit 1 ... sqlite3.IntegrityError: UNIQUE constraint failed: records.id'. Cause: app/db/db.py:34-35 executes schema.sql, which uses CREATE TABLE IF NOT EXISTS, so the old global-PK tables are kept; there is no PRAGMA user_version check. The default DB path is app/backend/api.py:45 (data/zlayt.sqlite). The handoff's 'delete old sqlite files' is a manual step, not in the AC or in code.",
44	   "why_it_matters": "Any machine with a pre-upgrade DB file gets a raw IntegrityError on the second case, and the first case's data stays under the old schema. This is the persistence failure the dossier warns about: a schema change that does not reach existing data without a visible signal.",
45	   "fix": "Read PRAGMA user_version in connect(). On an old schema, either migrate (rebuild the four item tables with PRIMARY KEY (case_id, id), copying rows) or raise a named error that tells the user which file to remove. Bump the version in schema.sql.",
46	   "acceptance_test": "Create a file with the pre-T-050 tree (git archive 6c3aeb1^), then open it with the fix tree and ingest a second case. Either the rows migrate and the second case ingests, or connect() raises a named error. artifacts/review-evidence/T-050/legacy_probe.py must no longer end in IntegrityError."},
47	  {"severity": "minor",
48	   "title": "AC1 names tests/unit/test_db.py and test_pipeline.py; neither file has a case-scoped test",
49	   "evidence": "grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py -> 0 and 0. AC1 evidence cites tests/unit/test_multicase.py (a new file).",
50	   "why_it_matters": "The AC says where the proof lives. A reader following the card will not find it in the named files.",
51	   "fix": "Add one case-scoped test to test_db.py (get_item/apply_review with case=, ambiguous bare id raises ValueError) and one to test_pipeline.py, or amend the AC text to name test_multicase.py.",
52	   "acceptance_test": "grep -l 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py lists both files, and pytest on those two files passes."},
53	  {"severity": "minor",
54	   "title": "AC3 delete test asserts only the records count for case A",
55	   "evidence": "tests/unit/test_multicase.py:46-53: 'assert DB.get_case(conn, a) is None and DB.table_counts(conn, a).get(\"records\", 0) == 0'. Mutant M3 (llm_calls removed from _CASE_TABLES, app/db/db.py:21) leaves this test green; it is caught only by test_db.py (4 tests) and test_api_routes.py (2 tests) in mutate.py.",
56	   "why_it_matters": "ADR-006 requires prompts (llm_calls) to be deleted with the case. The AC3 test as written would stay green if prompts survived. The protection comes from older tests, not from the test the card cites.",
57	   "fix": "Assert every table in _CASE_TABLES has zero rows for case A and unchanged counts for case B.",
58	   "acceptance_test": "Apply mutation M3 (drop llm_calls from _CASE_TABLES) in a scratch copy; tests/unit/test_multicase.py::test_delete_case_removes_only_that_case must fail."}
59	 ],
60	 "whats_right": [
61	  "Composite PK (case_id, id) on records, entries, amounts and flags, and every db.py/review.py writer takes case= and scopes its UPDATE/DELETE by case_id; an ambiguous bare id raises ValueError (app/db/db.py:116-117) instead of picking a row.",
62	  "Display ids stay short in API JSON (e1, a1, f_gap_r6_r7, no random suffix) and identical across cases, as the AC2 text requires; delete_case leaves the other case's rows unchanged in every table on both code paths.",
63	  "Four injected defects in scratch copies (unscoped _find, global PK, skipped llm_calls delete, unscoped apply_review UPDATE) were each caught by at least one test."
64	 ],
65	 "questions_for_chris": [
66	  "Is a DB file created before T-050 a state the demo or paralegal machines can be in? If yes, F2 must be fixed before the gate. If no, a documented 'remove data/zlayt.sqlite on upgrade' step is acceptable and F2 drops to a note."
67	 ]}
68	```
69	
70	## Outside this card (observed, not T-050 findings)
71	
72	- `tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode` fails at HEAD 4e8f43d (`IndexError` at line 129: `warnings` is empty, so the judge did not report JUDGE_UNAVAILABLE). It passed on the 6c3aeb1 tree in my run. Not caused by the T-050 diff as far as I can tell. Flagging for the orchestrator to route.
73	- In the probe, the fixture backend's judge steps (j1 to j4) raised 64 `llm call failed` lines on the working tree, and every probe entry ended `needs_review` with `["JUDGE_UNAVAILABLE"]`. That is an honest visible state, but it means the probe proves id and isolation behaviour, not verified output.
74	- At my review start, 251 LLM fixture files under `tests/fixtures/llm/` were untracked, so a clean checkout of 6c3aeb1 could not reproduce the suite. At 4e8f43d `git status` shows 0 untracked fixtures, so this is resolved.
75	
76	Not exercised: live app at http://localhost:7860, the eval runner, the `python -m app.pipeline evals/golden/sample.txt` CLI run-twice determinism check, export.
77	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:11.672Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t050_namespacing_review_patterns.md"
}
````

### User / tool · 2026-11-02T02:17:11.678Z

**tool result**
````
1	---
2	name: t050-namespacing-review-patterns
3	description: T-050 (per-case id namespacing, commit 6c3aeb1) round-1 review - committed fix missing producer lines, no DB migration, delete test checks records only; how to reproduce a commit without the working tree
4	metadata:
5	  type: project
6	---
7	
8	Recurring pattern from the T-050 review (reviews/T-050-staff-engineer.md, verdict fail, 2026-11-01).
9	
10	- **A commit can be green in its own unit tests and still not run.** 6c3aeb1 changed db.py to require `case=` for ambiguous ids,
11	  but the producer `_persist` in app/backend/pipeline.py (HEAD lines 141, 145) still called update_item/apply_review without it.
12	  The fix lived only as uncommitted working-tree diff, mixed with unrelated backend WIP. test_multicase passed at HEAD because it
13	  calls run_pipeline on fresh case ids and never does the API order (ingest_case for B, then run B). Same family as
14	  [[project_wiring_review_patterns]].
15	- **Reproduce a committed state without the working tree:** `git archive <sha> | tar -x -C artifacts/review-evidence/<card>/<dir>`,
16	  then run pytest there. Before reading any red, check untracked fixtures: at review time 251 files under tests/fixtures/llm/
17	  were untracked, so a clean archive fails 7 API tests for reasons unrelated to the card. Compare three trees: the commit, the commit plus
18	  the untracked fixtures, and the commit plus the working-tree file in question.
19	- **Schema change with CREATE TABLE IF NOT EXISTS is not a migration.** An existing file keeps the old global PRIMARY KEY, and the
20	  second case dies with `IntegrityError: UNIQUE constraint failed: records.id`. Probe with the pre-change tree (git archive <sha>^)
21	  writing the file, then the new tree opening it. The handoff's "delete old sqlite files" is not a fix.
22	- **Delete-isolation tests can check one table.** test_delete_case_removes_only_that_case checked only `records`, so dropping llm_calls
23	  (ADR-006 prompts) from _CASE_TABLES left it green. Other tests caught it. Check the mutant against the card's own test, not the suite.
24	- **Mutation method that worked:** copy app/, tests/, evals/ from the working tree into artifacts/review-evidence/<card>/mut/<name>/,
25	  assert the pattern occurs once, apply one replacement, run the card's test files. Never edit the repo.
26	
27	Reviewer environment gotchas (this card):
28	- `timeout` is not installed on this macOS shell; do not use it.
29	- The git-guard hook blocks `rm -rf $var/...` when the variable is unresolved. Use literal paths.
30	- HEAD moved during the review (other agents committed). Record `git rev-parse --short HEAD` at start and at each test run; a test
31	  that passed at the start can fail at the end (test_judge_unavailable_edit... went red on HEAD 4e8f43d).
32	
33	Related: [[project_db_review_patterns]], [[project_wiring_review_patterns]], [[project_harness_review_patterns]].
34	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:12.314Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_db.py -q 2>&1 | tail -2; echo \"EXIT=$?\"; git rev-parse --is-inside-work-tree 2>&1; git log --oneline -5 2>&1; git rev-parse HEAD 2>&1",
 "description": "Run T-050 unit tests and show git HEAD"
}
````

### User / tool · 2026-11-02T02:17:13.517Z

**tool result**
````
............................                                             [100%]
28 passed in 0.78s
EXIT=0
true
037cc89 chore(orchestrator): D-032/D-033; debt-close from in_review; T-036/T-038 closed
996f9b4 feat(frontend): local-mode case switcher and library loader (T-053 AC2)
5f8858f feat(db): log-only review actions not_duplicate, manual_entry; schema version rebuild (T-062)
dd545e3 feat(research): narrow lexicon self_report to explicit patient attribution (T-061)
099732b feat(backend): LLM split fallback for unsplit pastes, validated by code, flagged LLM_SPLIT (T-057, D-031)
037cc89bf378150813f286d74dff982c163a4238
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:17.859Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD=$(git rev-parse --short HEAD)\"; git status --short | head -30; echo '--- user_version / move-aside grep at HEAD (app/db/db.py)'; git show HEAD:app/db/db.py | grep -n -i -E 'user_version|move|rename|rebuild|aside|backup|os\\.replace|shutil|version' ; echo \"--- working tree db.py\"; grep -n -i -E 'user_version|move|rename|rebuild|aside|backup|os\\.replace|shutil|version' app/db/db.py; echo '--- test_multicase at HEAD'; git show HEAD:tests/unit/test_multicase.py | grep -n -E '^def |user_version|rebuild|aside|coexist' ; echo '--- test_multicase working tree'; grep -n -E '^def |user_version|rebuild|aside|coexist' tests/unit/test_multicase.py; echo '--- git log T-050/T-062 related'; git log --oneline | grep -n -E 'T-050|T-062|T-03|migrat|schema' | head -20",
 "description": "Check HEAD and grep db.py and test_multicase.py for version/rebuild logic"
}
````

### User / tool · 2026-11-02T02:17:18.067Z

**tool result**
````
HEAD=037cc89
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
 M app/backend/api.py
 M app/backend/export.py
 M app/backend/ingest.py
 M app/backend/pipeline.py
 M app/backend/present.py
 M app/backend/review.py
 M app/backend/store.py
 M app/db/db.py
 M board/activity.jsonl
 M board/cards/T-040.md
 M board/cards/T-052.md
 M evals/reports/latest.json
--- user_version / move-aside grep at HEAD (app/db/db.py)
25:SCHEMA_VERSION = 2   # bump on any schema.sql change; an older file is dropped and rebuilt (data is ephemeral, 24 h)
33:SCHEMA_VERSION = 2          # 1 = global ids (pre T-050); 2 = (case_id, id) keys
38:    """Open (and create) the database. A file written by an older schema version is moved aside to <path>.old-<ts> and rebuilt
43:            version = probe.execute("PRAGMA user_version").fetchone()[0]
47:        if has_tables and version != SCHEMA_VERSION:
48:            moved = f"{path}.old-{int(time.time())}"
49:            os.replace(path, moved)
52:                    os.replace(path + ext, moved + ext)
53:            log.warning("database schema version %s != %s: moved %s aside and rebuilt", version, SCHEMA_VERSION, os.path.basename(moved))
58:    if conn.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
64:    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
--- working tree db.py
25:SCHEMA_VERSION = 2   # bump on any schema.sql change; an older file is dropped and rebuilt (data is ephemeral, 24 h)
33:SCHEMA_VERSION = 2          # 1 = global ids (pre T-050); 2 = (case_id, id) keys
38:    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
39:    text): the schema uses CREATE IF NOT EXISTS, so an old file would otherwise keep its old keys, and keeping it aside would keep
44:            version = probe.execute("PRAGMA user_version").fetchone()[0]
48:        if has_tables and version != SCHEMA_VERSION:
51:                    os.remove(path + ext)
52:            log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
57:    if conn.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
63:    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
--- test_multicase at HEAD
9:def seeded(conn, case, text):
15:def test_two_golden_cases_back_to_back_in_one_file(tmp_path):
26:def test_full_pipeline_twice_in_one_file(tmp_path):
46:def test_delete_case_removes_only_that_case(tmp_path):
62:def test_case_scoped_lookup_and_ambiguous_bare_id(tmp_path):
75:def test_old_schema_file_is_moved_aside_and_rebuilt(tmp_path, caplog):
85:    assert len(glob.glob(path + ".old-*")) == 1 and conn.execute("PRAGMA user_version").fetchone()[0] == DB.SCHEMA_VERSION
--- test_multicase working tree
9:def seeded(conn, case, text):
15:def test_two_golden_cases_back_to_back_in_one_file(tmp_path):
26:def test_full_pipeline_twice_in_one_file(tmp_path):
46:def test_delete_case_removes_only_that_case(tmp_path):
62:def test_case_scoped_lookup_and_ambiguous_bare_id(tmp_path):
75:def test_old_schema_file_is_deleted_and_rebuilt(tmp_path, caplog):
85:    assert conn.execute("PRAGMA user_version").fetchone()[0] == DB.SCHEMA_VERSION and conn.execute("SELECT count(*) FROM cases").fetchone()[0] == 0
90:    assert DB.connect(path).execute("PRAGMA user_version").fetchone()[0] == DB.SCHEMA_VERSION
--- git log T-050/T-062 related
1:037cc89 chore(orchestrator): D-032/D-033; debt-close from in_review; T-036/T-038 closed
3:5f8858f feat(db): log-only review actions not_duplicate, manual_entry; schema version rebuild (T-062)
10:8d485ec test(backend): replay counts failed calls, one injection warning, per-record deadline (T-037 r1)
13:d6a89ad fix(evals): judge-unavailable is never a catch; reported separately and makes bar 4 not_measured (T-038)
14:7a450a1 feat(db): schema version, old files moved aside and rebuilt; stronger multi-case tests (T-050 r2, T-040)
15:7364096 fix(evals): grounding reads run_case record key 'source'; exit 1 for unmet bar; first full run on recorded fixtures (T-038 r3)
17:81df4e0 feat(backend): pipeline conflict-pass warning on run (T-036) on top of T-037/T-050 edits
18:fe4e6a2 test(backend): endpoint-not-verified gap state (T-037 AC8)
19:3f37141 fix(backend): source_kind from lexicon self_report with explicit patient attribution, case-level conflict-check warning, single-period templates (T-036 r3)
21:0d040d3 feat(backend): eval view, judge recorder, fixtures for sample + 9 cases + judge lines (T-037)
31:c8c7ba6 fix(evals): exactly-3-run gate, check-spec recomputes bar, no swallowed exceptions, per-bar mutation tests (T-038 r1)
32:6c3aeb1 fix(db): per-case id namespacing via composite primary key (T-050)
33:7b7c8a5 test(review): any judge exception on edit is JUDGE_UNAVAILABLE and needs_review (T-039 debt)
35:cd4bc60 fix(backend): neutral flag templates, visible conflict-pass failure, patient_report only on explicit attribution (T-036 r2)
37:6252c0a test: judge outputs carry reason_code per D-028 (fakes, judges, schemas, pipeline, review rules)
38:53093a0 fix(backend): missing judge reason_code is invalid output, not NONE (T-035 follow-up)
39:e274322 fix(backend): T-033 follow-up - scope the rate cue to the amount's own clause
40:f861159 fix(backend): audited role_for treats j1..j4 steps as judge (T-034)
43:ad4803a fix(backend): T-033 r2 - unit-rate-only rate cue, no decimal truncation, conflict over-firing test
44:d67a82d feat(backend): pipeline stages 0-7, persistence, CLI (T-037 part 1)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:22.893Z

**tool call — Bash**
````
{
 "command": "echo '--- HEAD db.py 20-70'; git show HEAD:app/db/db.py | sed -n '18,70p'; echo '--- HEAD pipeline case=cid count'; git show HEAD:app/backend/pipeline.py | grep -c 'case=cid'; git show HEAD:app/backend/pipeline.py | grep -n -E 'update_item|apply_review|add_item'; echo '--- HEAD test_multicase 15-100'; git show HEAD:tests/unit/test_multicase.py | sed -n '1,100p'; echo '--- untracked count'; git status --short | grep -c '^??'; git status --short | grep -E '^\\?\\?' | head -5; git status --short -- app/backend/pipeline.py app/db tests/unit/test_multicase.py tests/unit/test_api_routes.py",
 "description": "Read HEAD db.py open logic, HEAD pipeline call sites, HEAD test_multicase, untracked status"
}
````

### User / tool · 2026-11-02T02:17:23.137Z

**tool result**
````
--- HEAD db.py 20-70
ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
           "confirm_date": None, "keep_my_wording": None,
           "not_duplicate": None, "manual_entry": None}          # None = logged only, status unchanged
_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
_PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
SCHEMA_VERSION = 2   # bump on any schema.sql change; an older file is dropped and rebuilt (data is ephemeral, 24 h)
_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")


def init(path: str = ":memory:"):
    return connect(path)


SCHEMA_VERSION = 2          # 1 = global ids (pre T-050); 2 = (case_id, id) keys
log = logging.getLogger("zlayt.db")


def connect(path: str):
    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
    text): the schema uses CREATE IF NOT EXISTS, so an old file would otherwise keep its old keys, and keeping it aside would keep
    pasted text past the 24 h purge (T-040 security r2)."""
    if path != ":memory:" and os.path.exists(path) and os.path.getsize(path) > 0:
        probe = sqlite3.connect(path)
        try:
            version = probe.execute("PRAGMA user_version").fetchone()[0]
            has_tables = probe.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0] > 0
        finally:
            probe.close()
        if has_tables and version != SCHEMA_VERSION:
            for ext in ("", "-wal", "-shm", "-journal"):          # deleted, not kept: an old file would hold pasted text past the 24 h purge
                if os.path.exists(path + ext):
                    os.remove(path + ext)
            log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA secure_delete=ON")
    conn.execute("PRAGMA foreign_keys=ON")
    if conn.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
        for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','index') AND name NOT LIKE 'sqlite_%'").fetchall():
            if r["name"] and not r["name"].startswith("ix_"):
                conn.execute(f"DROP TABLE IF EXISTS {r['name']}")
    with open(_SCHEMA, encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
    return conn


def _tok(prefix: str) -> str:
    return prefix + secrets.token_hex(6)


--- HEAD pipeline case=cid count
2
139:            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
141:        DB.update_item(conn, it["id"], now=now, case=cid, **row)
145:                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
--- HEAD test_multicase 15-100
"""T-050: many cases share one sqlite file; ids are short per case and never collide; delete_case touches only its own rows."""
import pytest
from app.backend import pipeline as PL
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, which_record


def seeded(conn, case, text):
    cid = DB.create_case(conn, text, now=1.0)
    PL.ingest_case(conn, cid, text, 1.0)
    return cid


def test_two_golden_cases_back_to_back_in_one_file(tmp_path):
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    a = seeded(conn, "sample", G.raw("sample"))
    b = seeded(conn, "case_01", G.raw("case_01_date_formats"))
    c = seeded(conn, "sample again", G.raw("sample"))
    ids = lambda cid: sorted(r["id"] for r in DB.list_items(conn, cid, "flag"))   # noqa: E731
    assert ids(a) == ids(c) and ids(a)                                              # same short ids in two cases
    assert conn.execute("SELECT count(*) FROM records WHERE case_id=?", (a,)).fetchone()[0] == 9
    assert conn.execute("SELECT count(*) FROM records WHERE case_id=?", (b,)).fetchone()[0] >= 8


def test_full_pipeline_twice_in_one_file(tmp_path):
    sums = golden_summaries()
    script = {"extract": lambda u: dict(summary=sums[which_record(u)[0]][0], excerpt=sums[which_record(u)[0]][1]),
              "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"}, "j3": {"verdict": "conflict", "reason_code": "NONE"},
              "j4": {"verdict": "agree", "reason_code": "NONE"}, "conflicts": {"flags": []}, "flags": {"flags": []}}
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    outs = []
    for _ in range(2):
        cid = DB.create_case(conn, G.raw("sample"), now=1.0)
        outs.append((cid, PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(script), now=lambda: 1.0)))
    (a, oa), (b, ob) = outs
    assert [e["id"] for e in oa["entries"]] == [e["id"] for e in ob["entries"]] and len(oa["entries"]) == 9
    eid = oa["entries"][0]["id"]
    with pytest.raises(ValueError):                      # a bare id is ambiguous once two cases hold it
        DB.get_item(conn, eid)
    assert DB.get_item(conn, eid, a)["case_id"] == a and DB.get_item(conn, eid, b)["case_id"] == b
    DB.apply_review(conn, eid, "accept", now=2.0, case=a)
    assert DB.get_item(conn, eid, a)["review_status"] == "accepted" and DB.get_item(conn, eid, b)["review_status"] == "pending"


def test_delete_case_removes_only_that_case(tmp_path):
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    a = seeded(conn, "a", G.raw("sample"))
    b = seeded(conn, "b", G.raw("sample"))
    for cid in (a, b):                                   # give both cases an audit row and an event so every table has content
        DB.add_llm_call(conn, cid, "prompt text", "{}", now=1.0)
        DB.apply_review(conn, DB.list_items(conn, cid, "flag")[0]["id"], "accept", now=2.0, case=cid)
    before = DB.table_counts(conn, b)
    DB.delete_case(conn, a)
    assert DB.get_case(conn, a) is None
    for t in DB._CASE_TABLES:                            # every per-case table, prompts included
        col = "id" if t == "cases" else "case_id"
        assert conn.execute(f"SELECT count(*) FROM {t} WHERE {col}=?", (a,)).fetchone()[0] == 0, t
    assert DB.table_counts(conn, b) == before and before["records"] == 9 and before["llm_calls"] == 1


def test_case_scoped_lookup_and_ambiguous_bare_id(tmp_path):
    """AC1 (named in test_db/test_pipeline too): case= scopes get_item/apply_review; a bare id held by two cases raises."""
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    a, b = seeded(conn, "a", G.raw("sample")), seeded(conn, "b", G.raw("sample"))
    fid = DB.list_items(conn, a, "flag")[0]["id"]
    with pytest.raises(ValueError):
        DB.get_item(conn, fid)
    DB.apply_review(conn, fid, "dismiss", now=3.0, case=b)
    assert DB.get_item(conn, fid, b)["review_status"] == "dismissed" and DB.get_item(conn, fid, a)["review_status"] == "pending"
    with pytest.raises(KeyError):
        DB.get_item(conn, fid, "nonexistent-case")


def test_old_schema_file_is_deleted_and_rebuilt(tmp_path, caplog):
    """T-050 r2 / T-040 security r2: a file from schema version 1 is deleted (no *.old copy keeps its text) and a fresh v2 file is created; one log line."""
    import glob, sqlite3
    path = str(tmp_path / "old.sqlite")
    old = sqlite3.connect(path)
    old.executescript("CREATE TABLE cases (id TEXT PRIMARY KEY, raw_text TEXT); CREATE TABLE records (id TEXT PRIMARY KEY, case_id TEXT);"
                      "INSERT INTO cases VALUES ('x', 'SYNTHETIC old pasted text');")
    old.commit(); old.close()
    caplog.set_level("WARNING", logger="zlayt.db")
    conn = DB.connect(path)
    assert conn.execute("PRAGMA user_version").fetchone()[0] == DB.SCHEMA_VERSION and conn.execute("SELECT count(*) FROM cases").fetchone()[0] == 0
    assert glob.glob(str(tmp_path / "old.sqlite*")) == [path] or sorted(glob.glob(str(tmp_path / "*"))) == [path]       # nothing else left behind
    assert b"SYNTHETIC old pasted text" not in open(path, "rb").read()
    assert len([r for r in caplog.records if r.name == "zlayt.db"]) == 1 and "SYNTHETIC" not in caplog.text
    DB.connect(path).close()                              # reopening a current file deletes nothing
    assert DB.connect(path).execute("PRAGMA user_version").fetchone()[0] == DB.SCHEMA_VERSION
--- untracked count
182
?? .claude/agent-memory/backend/
?? .claude/agent-memory/claims-adjuster-reviewer/feedback_review_commit_not_worktree.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_flag_pass_review_patterns.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_flag_source_kind_and_run_signal.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t036_r4_split_and_judge_fixtures.md
 M app/backend/pipeline.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:31.355Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD now=$(git rev-parse --short HEAD)\"; git log --oneline -6; echo '--- reflog'; git reflog -6 --date=iso 2>&1 | head -8; echo '--- HEAD db.py grep (re-run)'; git show HEAD:app/db/db.py | grep -n -E 'moved aside|deleted and rebuilt|os\\.replace|os\\.remove|user_version'; echo \"HEAD after=$(git rev-parse --short HEAD)\"",
 "description": "Re-pin HEAD and re-grep HEAD db.py for migration logic"
}
````

### User / tool · 2026-11-02T02:17:31.408Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may not run `git reflog` in the project (allowed only in scratch repos under /tmp)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:33.030Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD now=$(git rev-parse --short HEAD)\"; git log --oneline -6; echo '--- HEAD db.py grep (re-run)'; git show HEAD:app/db/db.py | grep -n -E 'moved aside|deleted and rebuilt|os\\.replace|os\\.remove|user_version'; echo \"HEAD after=$(git rev-parse --short HEAD)\"",
 "description": "Re-pin HEAD and re-grep HEAD db.py for migration logic"
}
````

### User / tool · 2026-11-02T02:17:33.188Z

**tool result**
````
HEAD now=864676f
864676f fix(db): delete old-schema database at rebuild instead of keeping a copy (T-050, T-040 security r2)
037cc89 chore(orchestrator): D-032/D-033; debt-close from in_review; T-036/T-038 closed
996f9b4 feat(frontend): local-mode case switcher and library loader (T-053 AC2)
5f8858f feat(db): log-only review actions not_duplicate, manual_entry; schema version rebuild (T-062)
dd545e3 feat(research): narrow lexicon self_report to explicit patient attribution (T-061)
099732b feat(backend): LLM split fallback for unsplit pastes, validated by code, flagged LLM_SPLIT (T-057, D-031)
--- HEAD db.py grep (re-run)
38:    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
44:            version = probe.execute("PRAGMA user_version").fetchone()[0]
51:                    os.remove(path + ext)
52:            log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
57:    if conn.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
63:    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
HEAD after=864676f
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:45.952Z

**tool call — Bash**
````
{
 "command": "SHA=$(git rev-parse HEAD) && echo \"PIN=$SHA\" && ls artifacts/review-evidence/T-050/ && D=artifacts/review-evidence/T-050/r2_head_$(git rev-parse --short HEAD) && mkdir -p \"$D\" && git archive \"$SHA\" | tar -x -C \"$D\" && echo \"ARCHIVE=$D\" && echo \"untracked-llm-fixtures-in-wt=$(git status --short --untracked-files=all tests/fixtures/llm | grep -c '^??')\" && echo \"tracked-llm-fixtures-at-HEAD=$(git ls-tree -r --name-only $SHA tests/fixtures/llm | wc -l)\" && echo \"pipeline case=cid at HEAD=$(git show $SHA:app/backend/pipeline.py | grep -c 'case=cid')\" && git show $SHA:app/backend/pipeline.py | grep -n -E 'update_item|apply_review|add_item'; echo \"--- wt pipeline diff summary\"; git diff --stat HEAD -- app/backend/pipeline.py; git diff HEAD -- app/backend/pipeline.py | grep -n 'case=cid'",
 "description": "Pin HEAD sha, extract archive, check pipeline producer call sites"
}
````

### User / tool · 2026-11-02T02:17:46.011Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: SHA=$(git rev-parse HEAD) && echo "PIN=$SHA" && ls artifacts/review-evidence/T-050/ && D=artifacts/review-evidence/T-050/r2_head_$(git rev-parse --short HEAD) && mkdir -p "$D" && git archive "$SHA" | 
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:48.694Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && ls artifacts/review-evidence/T-050/ && mkdir -p artifacts/review-evidence/T-050/r2_head_864676f && git archive 864676f | tar -x -C artifacts/review-evidence/T-050/r2_head_864676f && echo ARCHIVE_OK && echo \"tracked-llm-fixtures-at-864676f: $(git ls-tree -r --name-only 864676f tests/fixtures/llm | wc -l)\" && echo \"untracked-llm-in-wt: $(git status --short --untracked-files=all tests/fixtures/llm | grep -c '^??')\" && echo \"pipeline case=cid at 864676f: $(git show 864676f:app/backend/pipeline.py | grep -c 'case=cid')\" && git show 864676f:app/backend/pipeline.py | grep -n -E 'update_item|apply_review|add_item'; echo \"--- wt pipeline vs HEAD\"; git diff --stat HEAD -- app/backend/pipeline.py; git diff HEAD -- app/backend/pipeline.py | grep -n 'case=cid'",
 "description": "Extract HEAD 864676f archive and check pipeline producer call sites"
}
````

### User / tool · 2026-11-02T02:17:49.079Z

**tool result**
````
d548ccda26c871c6540dbfdc7bc1d29d8f3e4e99
h1_head_plus_fixtures
h2_head_plus_fixtures_plus_wt_pipeline
head_4e8f43d
head_6c3aeb1
legacy.sqlite
legacy_probe.py
mut
mutate.py
pre_6c3aeb1p
single_case_probe.py
t050_check.py
tmpgjlc5p7t
worktree
ARCHIVE_OK
tracked-llm-fixtures-at-864676f:      317
untracked-llm-in-wt: 41
pipeline case=cid at 864676f: 2
139:            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
141:        DB.update_item(conn, it["id"], now=now, case=cid, **row)
145:                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
--- wt pipeline vs HEAD
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:51.701Z

**tool call — Bash**
````
{
 "command": "git log --oneline -4 && git rev-parse --short HEAD && git show --stat --format='%h %s' HEAD | head -15",
 "description": "Check current HEAD log and latest commit stat"
}
````

### User / tool · 2026-11-02T02:17:51.831Z

**tool result**
````
c61e84f fix(db): bump schema version to 3, real v2 rebuild test (T-062 r2)
d548ccd feat(backend): manual entry for a rejected record and 'not a duplicate' split (T-056, D-031)
c143c4b docs(research): UI reference study and UI design brief draft (T-060 pass 1)
864676f fix(db): delete old-schema database at rebuild instead of keeping a copy (T-050, T-040 security r2)
c61e84f
c61e84f fix(db): bump schema version to 3, real v2 rebuild test (T-062 r2)

 app/db/db.py          |  7 +------
 tests/unit/test_db.py | 20 +++++++++++++++-----
 2 files changed, 16 insertions(+), 11 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:59.378Z

**tool call — Bash**
````
{
 "command": "git rev-parse c61e84f && mkdir -p artifacts/review-evidence/T-050/r2_head_c61e84f && git archive c61e84f | tar -x -C artifacts/review-evidence/T-050/r2_head_c61e84f && echo ARCHIVE_OK && echo \"tracked llm fixtures: $(git ls-tree -r --name-only c61e84f tests/fixtures/llm | wc -l)\" && cd artifacts/review-evidence/T-050/r2_head_c61e84f && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_db.py -q 2>&1 | tail -3; echo \"--- full unit suite on c61e84f archive\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q 2>&1 | tail -4",
 "description": "Extract HEAD c61e84f archive and run brief tests plus full unit suite there"
}
````

### User / tool · 2026-11-02T02:18:15.521Z

**tool result**
````
c61e84fbed0e9818cf04bea77230f047027b3ef8
ARCHIVE_OK
tracked llm fixtures:      317
............................                                             [100%]
28 passed in 0.81s
--- full unit suite on c61e84f archive
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[sample]
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[case_01_date_formats]
FAILED tests/unit/test_t037_backend.py::test_sample_replay_shows_verified_entries
4 failed, 827 passed in 14.12s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:18.276Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_head_c61e84f && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_t037_backend.py -q 2>&1 | grep -E -m6 'Error|assert|fixture|FAILED' ; echo \"--- working tree same file\"; cd /Users/arsis/zlayt-pm-project && .venv/bin/python -m pytest tests/unit/test_t037_backend.py -q 2>&1 | tail -2; echo \"--- untracked llm fixtures in wt\"; git status --short --untracked-files=all tests/fixtures/llm | head -5",
 "description": "Inspect the 4 failures in archive and compare to working tree"
}
````

### User / tool · 2026-11-02T02:18:22.455Z

**tool result**
````
___________________ test_replay_has_no_fixture_miss[sample] ____________________
tmp_path = PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-2028/test_replay_has_no_fixture_mis0')
    @needs_fixtures
    def test_replay_has_no_fixture_miss(case, monkeypatch, tmp_path):
        """T-037 AC2/AC7: replaying every golden input on the fixture backend makes 0 failed model calls (llm_calls rows with an error) and leaves no
        JUDGE_UNAVAILABLE / FIXTURE_MISS reason on any item. Fails when a fixture is missing or stale (a prompt changed since recording)."""
--- working tree same file
....................                                                     [100%]
20 passed in 1.81s
--- untracked llm fixtures in wt
 M tests/fixtures/llm/003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
 M tests/fixtures/llm/010db3ae8de16d72ea8905cdaa07781591d70092d358c0d5e73424940e3cfb33.json
 M tests/fixtures/llm/06ba451c413e5628f554f915316d53a63820f262b930020da1cd2ecb147c5fea.json
 M tests/fixtures/llm/06bbeeec2801064baeb024b1338ce8a0263644a7a2dca09efdaeed154ed50299.json
 M tests/fixtures/llm/070338b4178e1104318ebbd4481be4bca1fed8df4ac2c0acbb4fd7cc09278f46.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:29.102Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_head_c61e84f && echo '--- pipeline producer at c61e84f'; grep -n -E 'update_item|apply_review|add_item' app/backend/pipeline.py; echo '--- F1 test: two cases coexist via API order'; grep -n -E 'def test_two_cases_coexist' tests/unit/test_api_routes.py; echo '--- F2 rebuild at c61e84f db.py'; grep -n -E 'SCHEMA_VERSION =|os\\.remove|os\\.replace|user_version|moved aside|deleted' app/db/db.py; echo '--- F4 delete test at c61e84f test_multicase'; grep -n -A12 'def test_delete_case_removes_only_that_case' tests/unit/test_multicase.py | head -16; echo '--- F3 case= in test_db/test_pipeline'; grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py; echo '--- user-visible signal for rebuild?'; grep -rn -E 'old file deleted|schema version|SCHEMA_VERSION' app/ --include=*.py --include=*.js --include=*.ts --include=*.tsx --include=*.html 2>/dev/null | grep -v 'app/db/db.py' | head -5; echo '--- 24h purge policy docs'; grep -rn -i -E '24 ?h|24 hours|purge' /Users/arsis/zlayt-pm-project/docs 2>/dev/null | head -6",
 "description": "Check F1-F4 status at c61e84f archive and purge policy docs"
}
````

### User / tool · 2026-11-02T02:18:29.251Z

**tool result**
````
--- pipeline producer at c61e84f
146:            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
148:        DB.update_item(conn, it["id"], now=now, case=cid, **row)
152:                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
--- F1 test: two cases coexist via API order
200:def test_two_cases_coexist_with_short_display_ids(env):
--- F2 rebuild at c61e84f db.py
32:SCHEMA_VERSION = 3          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062)
37:    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
43:            version = probe.execute("PRAGMA user_version").fetchone()[0]
48:            for ext in ("", "-wal", "-shm", "-journal"):          # deleted, not kept: an old file would hold pasted text past the 24 h purge
50:                    os.remove(path + ext)
51:            log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
58:    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
--- F4 delete test at c61e84f test_multicase
46:def test_delete_case_removes_only_that_case(tmp_path):
47-    conn = DB.connect(str(tmp_path / "m.sqlite"))
48-    a = seeded(conn, "a", G.raw("sample"))
49-    b = seeded(conn, "b", G.raw("sample"))
50-    for cid in (a, b):                                   # give both cases an audit row and an event so every table has content
51-        DB.add_llm_call(conn, cid, "prompt text", "{}", now=1.0)
52-        DB.apply_review(conn, DB.list_items(conn, cid, "flag")[0]["id"], "accept", now=2.0, case=cid)
53-    before = DB.table_counts(conn, b)
54-    DB.delete_case(conn, a)
55-    assert DB.get_case(conn, a) is None
56-    for t in DB._CASE_TABLES:                            # every per-case table, prompts included
57-        col = "id" if t == "cases" else "case_id"
58-        assert conn.execute(f"SELECT count(*) FROM {t} WHERE {col}=?", (a,)).fetchone()[0] == 0, t
--- F3 case= in test_db/test_pipeline
tests/unit/test_db.py:0
tests/unit/test_pipeline.py:0
--- user-visible signal for rebuild?
--- 24h purge policy docs
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:42.968Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-050/legacy_probe.py; echo '--- board show T-050 (AC section)'; .venv/bin/python tools/board.py show T-050 2>&1 | head -60; echo '--- 24h policy in board/docs'; grep -rn -i -E '24 ?h\\b|24 hours|purge' board/cards docs 2>/dev/null | grep -v -i 'token' | head -8",
 "description": "Read legacy probe script and T-050 card AC via board.py show"
}
````

### User / tool · 2026-11-02T02:18:43.121Z

**tool result**
````
"""Upgrade hazard probe: a DB file created by pre-T-050 code, then opened by the current code.
Usage: legacy_probe.py <pre_root> <new_root> <dbpath>"""
import os, re, sys
pre, new, dbp = sys.argv[1], sys.argv[2], sys.argv[3]
for suffix in ("", "-wal", "-shm", "-journal"):
    if os.path.exists(dbp + suffix):
        os.remove(dbp + suffix)
os.environ["LLM_BACKEND"] = "fixture"
# step 1: pre-T-050 code writes sample into the file (run in a subprocess so module names do not clash)
import subprocess
code = (
    "import sys,os; sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1]);"
    "from app.db import db as DB; from app.backend import pipeline as PL; from tests.unit import _golden as G;"
    "c=DB.connect(sys.argv[2]); cid=DB.create_case(c, G.raw('sample'), now=1.0); PL.ingest_case(c, cid, G.raw('sample'), 1.0);"
    "print('pre-code ingest sample ok, records=', c.execute('select count(*) from records').fetchone()[0])"
)
r = subprocess.run([sys.executable, "-c", code, pre, dbp], capture_output=True, text=True, env=dict(os.environ))
print("STEP1 exit", r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1])
# step 2: current code opens the same file and ingests a second case
code2 = (
    "import sys,os; sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1]);"
    "from app.db import db as DB; from app.backend import pipeline as PL; from tests.unit import _golden as G;"
    "c=DB.connect(sys.argv[2]);"
    "print('entries PK clause now:', __import__('re').findall(r'CREATE TABLE IF NOT EXISTS entries \\(\\n  id [^,]*', c.execute(\"select sql from sqlite_master where name='entries'\").fetchone()[0]));"
    "cid=DB.create_case(c, G.raw('case_01_date_formats'), now=1.0); PL.ingest_case(c, cid, G.raw('case_01_date_formats'), 1.0);"
    "print('second case ingest ok')"
)
r2 = subprocess.run([sys.executable, "-c", code2, new, dbp], capture_output=True, text=True, env=dict(os.environ))
print("STEP2 exit", r2.returncode, (r2.stdout + r2.stderr).strip().splitlines()[-3:])
--- board show T-050 (AC section)
---
id: "T-050"
title: "Per-case ID namespacing (records/entries/amounts/flags) so multiple cases coexist in one DB"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T01:59:33Z"
updated_at: "2026-11-02T02:17:22Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:09:11Z"
rounds: 1
commits: ["6c3aeb1", "81df4e0", "7a450a1", "864676f"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-050-staff-engineer.md", "at": "2026-11-02T02:08:59Z"}
ac:
  - {"n": 1, "text": "Two different golden cases run back to back in one DB file without collision; ids unique per case (e.g. <case_token_prefix>:r1) or composite keys; test in tests/unit/test_db.py and test_pipeline.py", "done": true, "evidence": "tests/unit/test_multicase.py (3 passed: two golden cases + two full pipeline runs in one file); db PK is now (case_id, id), ids stay short"}
  - {"n": 2, "text": "API responses keep short display ids (r1, e5) per memory/contracts/api.md while storage is unique", "done": true, "evidence": "test_api_routes::test_two_cases_coexist_with_short_display_ids (ids e1/r1, no suffix)"}
  - {"n": 3, "text": "delete_case removes only that case's rows (test)", "done": true, "evidence": "test_multicase::test_delete_case_removes_only_that_case"}
---
## Description
Defect found by backend-3 on T-040: pipeline and db use global ids (r1, e5); a second case in the same sqlite file collides. Fix in app/db + pipeline id generation.

## Notes (append-only, newest last)
- 2026-11-02T01:59:37Z orchestrator: assigned: backend-3
- 2026-11-02T01:59:47Z backend: claimed
- 2026-11-02T02:01:40Z backend: AC 1 checked: tests/unit/test_multicase.py (3 passed: two golden cases + two full pipeline runs in one file); db PK is now (case_id, id), ids stay short
- 2026-11-02T02:01:40Z backend: AC 2 checked: test_api_routes::test_two_cases_coexist_with_short_display_ids (ids e1/r1, no suffix)
- 2026-11-02T02:01:40Z backend: AC 3 checked: test_multicase::test_delete_case_removes_only_that_case
- 2026-11-02T02:01:40Z backend: moved in_progress -> in_review
- 2026-11-02T02:01:47Z orchestrator: review dispatched: haiku
- 2026-11-02T02:08:59Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-050-staff-engineer.md; round 1; findings:
    - [blocker] Committed T-050 change leaves pipeline._persist unscoped: a second case's run fails, and the card's own AC2 test fails at 6c3aeb1 — fix: Commit the case=cid argument on the three _persist calls (pipeline.py:141 and :145 at HEAD; :139 and :143 in the working tree) in a commit that does not carry the unrelated backend-2 WIP, or in the same commit as db.py. Add a test to tests/unit/te
    - [major] No migration for sqlite files created before T-050: the new composite key is silently not applied to an existing file — fix: Read PRAGMA user_version in connect(). On an old schema, either migrate (rebuild the four item tables with PRIMARY KEY (case_id, id), copying rows) or raise a named error that tells the user which file to remove. Bump the version in schema.sql.
    - [minor] AC1 names tests/unit/test_db.py and test_pipeline.py; neither file has a case-scoped test — fix: Add one case-scoped test to test_db.py (get_item/apply_review with case=, ambiguous bare id raises ValueError) and one to test_pipeline.py, or amend the AC text to name test_multicase.py.
    - [minor] AC3 delete test asserts only the records count for case A — fix: Assert every table in _CASE_TABLES has zero rows for case A and unchanged counts for case B.
- 2026-11-02T02:08:59Z orchestrator: Triage: blocker (pipeline._persist case=) resolved after review in 0d040d3/81df4e0. Migration decision: synthetic dev DBs with 24h purge get no migration; app checks a schema_version and rebuilds an old file with a clear log line.
- 2026-11-02T02:08:59Z orchestrator: assigned: backend-3
- 2026-11-02T02:09:11Z backend: claimed
- 2026-11-02T02:10:02Z backend: r2: blocker already fixed at HEAD (two-case tests pass: test_multicase 5, test_api_routes::test_two_cases_coexist). Added schema version (PRAGMA user_version=2): an older-version file is moved to <path>.old-<ts> and rebuilt with one log line (test_old_schema_file_is_moved_aside_and_rebuilt). AC3 test now checks every _CASE_TABLES table incl. llm_calls + events for the deleted case and unchanged counts for the other. Case-scoped lookup test lives in tests/unit/test_multicase.py (test_db/test_pipeline are qa-owned; AC1 should name test_multicase.py).
- 2026-11-02T02:10:02Z backend: moved in_progress -> in_review
- 2026-11-02T02:10:18Z orchestrator: review dispatched: haiku r2
- 2026-11-02T02:17:21Z backend: T-040 security r2 follow-up: schema-version migration now DELETES the old-version file (and -wal/-shm/-journal) at rebuild instead of moving it to *.old-<ts>, so no copy of pasted text outlives the 24 h purge. Test: test_multicase::test_old_schema_file_is_deleted_and_rebuilt (no leftover files, old text not in the new file, one log line). 51 db/multicase/api tests pass.

## Handoff
r2: schema_version migration (db.connect moves old files aside), stronger delete test, case-scoped/ambiguous-id test; 100 tests pass across api_routes/multicase/db/pipeline/review_rules.

--- 24h policy in board/docs
board/cards/T-014.md:66:    - [major] Public demo-only build still accepts and stores arbitrary pasted text for 24 h, which it can never process — fix: In demo mode, POST /api/cases accepts only `sample: true` or text whose sha256 equals the shipped sample (or a golden case). Any other text gets `409 demo_mode_unsupported_input` before anything is written. If an ingest-only preview of arbitrary text is wanted, compute it
board/cards/T-014.md:71:    - [minor] 24 h purge scope over llm_calls / review_events is unstated, and deleted text may persist in SQLite pages — fix: State that purge and DELETE share one function that deletes from every table by case_id (or enable `PRAGMA foreign_keys=ON` with ON DELETE CASCADE). Optionally set `PRAGMA secure_delete=ON`.
board/cards/T-034.md:25:  - {"n": 6, "text": "Contract review (T-018): Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md.", "done": true, "evidence": "orchestrator-owned: docs/M2M3_COVERAGE.md critical path + M2 cut order + cut trigger (commit after 2329ac2)"}
board/cards/T-034.md:37:- 2026-11-02T01:22:45Z orchestrator: AC 6 added: Contract review (T-018): Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md.
board/cards/T-050.md:39:- 2026-11-02T02:08:59Z orchestrator: Triage: blocker (pipeline._persist case=) resolved after review in 0d040d3/81df4e0. Migration decision: synthetic dev DBs with 24h purge get no migration; app checks a schema_version and rebuilds an old file with a clear log line.
board/cards/T-050.md:45:- 2026-11-02T02:17:21Z backend: T-040 security r2 follow-up: schema-version migration now DELETES the old-version file (and -wal/-shm/-journal) at rebuild instead of moving it to *.old-<ts>, so no copy of pasted text outlives the 24 h purge. Test: test_multicase::test_old_schema_file_is_deleted_and_rebuilt (no leftover files, old text not in the new file, one log line). 51 db/multicase/api tests pass.
board/cards/T-040.md:19:  - {"persona": "orchestrator-§7.4", "model": "claude-opus-5-5", "verdict": "pass", "file": "memory/SCOPE_CUTS.md", "at": "2026-11-02T02:17:14Z", "debt": "r2: round-1 blocker+majors resolved; new majors routed: PDF route gating/threadpool (backend-2, T-054), migration .old files purged (backend-3, T-050)"}
board/cards/T-040.md:54:    - [minor] Spec'd live-mode guard PROVIDER_CAP_CONFIRMED is not enforced anywhere; lazy purge only on create — fix: Fail fast in create_app when backend=='anthropic-api' and live is enabled and PROVIDER_CAP_CONFIRMED!='1'; call purge_expired in the `_headers` middleware or a dependency.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:49.368Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_head_c61e84f && echo '--- purge in app/ at c61e84f'; grep -rn -i 'purge' app/ | head -8; echo \"count=$(grep -rn -i 'purge' app/ | wc -l)\"; echo '--- delete_case / _CASE_TABLES at c61e84f'; grep -n -E '_CASE_TABLES = |def delete_case' app/db/db.py; echo '--- rebuild log line visible to UI?'; grep -rn -E 'schema version' app/ frontend/ 2>/dev/null | grep -v '\\.pyc' | head -3; echo '--- M4 card AC for purge'; cd /Users/arsis/zlayt-pm-project && grep -n -E 'T-031' board/cards/T-031.md | head -2; grep -n -i 'purge' board/cards/T-031.md | head -4",
 "description": "Check whether a 24h purge exists in code and where it is tracked"
}
````

### User / tool · 2026-11-02T02:18:49.529Z

**tool result**
````
--- purge in app/ at c61e84f
app/README-arch.md:15:  main.py          routes from memory/contracts/api.md (11 endpoints), static files, error format, demo gate (hash of normalised text), lazy 24 h purge via the one delete_case()
app/README-arch.md:37:app/db/ [db]       schema.sql, db.py (connection, helpers, purge)
app/README-arch.md:39:app/config.py [release]   env: LLM_BACKEND, GENERATOR_MODEL, JUDGE_MODEL, ENABLE_LIVE, PROVIDER_CAP_CONFIRMED, DATA_DIR, limits; injectable now() for every deadline and purge
app/README-arch.md:57:- Purge and `DELETE` are one function that deletes from every table by case id (prompts included); SQLite runs with `secure_delete`. Access logging is off (the case token is in the URL path) and responses send `Referrer-Policy: no-referrer`.
app/backend/api.py:93:    purged = {"at": 0.0}
app/backend/api.py:154:        if request.url.path.startswith("/api") and time.time() - purged["at"] > 60:     # expired cases vanish even with no create
app/backend/api.py:155:            purged["at"] = time.time()
app/backend/api.py:158:                DB.purge_expired(c, time.time())
count=      14
--- delete_case / _CASE_TABLES at c61e84f
24:_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
239:def delete_case(conn, case_id: str) -> None:
--- rebuild log line visible to UI?
app/db/db.py:37:    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
app/db/db.py:51:            log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
--- M4 card AC for purge
2:id: "T-031"
17:  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-031-staff-engineer.md", "at": "2026-11-02T01:47:13Z"}
3:title: "SQLite schema, helpers, ladder/audit/event tables, single purge function"
23:  - {"n": 3, "text": "delete_case(case_id) removes rows from every table including prompts, secure_delete is on, lazy 24h purge uses injectable now(); proved by test_db::test_delete_case_removes_all_tables and test_purge_24h", "done": true, "evidence": "tests/unit/test_db.py 9 passed (delete_case, purge 24h injectable now); secure_delete ON"}
26:  - {"n": 6, "text": "Contract review (T-018): Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md.", "done": true, "evidence": "n/a for db: orchestrator doc item"}
30:Persistence for decisions that must survive reload (R-RV-8) and the audit trail every LLM item needs (R-CO-2; LLM_VS_CODE row 20). Includes the one purge function required by the architecture invariants and keeps originals of edited items for the internal notes (R-RV-2).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:01.959Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050 && cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_mutate.py <<'EOF'\n\"\"\"Round-2 mutation check on the committed tree (git archive c61e84f). Copies the archive, applies one edit per mutant, runs tests.\nUsage: r2_mutate.py <archive_root> <out_root>. Never edits the repo.\"\"\"\nimport os, shutil, subprocess, sys\nSRC, OUT = sys.argv[1], sys.argv[2]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nMUTANTS = {\n    \"M1_pipeline_unscoped_persist\": (\"app/backend/pipeline.py\",\n        ['DB.update_item(conn, it[\"id\"], now=now, case=cid, **row)', 'DB.apply_review(conn, it[\"id\"], \"reset\", now=now, case=cid)'],\n        ['DB.update_item(conn, it[\"id\"], now=now, **row)', 'DB.apply_review(conn, it[\"id\"], \"reset\", now=now)'],\n        [\"tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids\"]),\n    \"M1b_pipeline_unscoped_vs_test_multicase_only\": (\"app/backend/pipeline.py\",\n        ['DB.update_item(conn, it[\"id\"], now=now, case=cid, **row)', 'DB.apply_review(conn, it[\"id\"], \"reset\", now=now, case=cid)'],\n        ['DB.update_item(conn, it[\"id\"], now=now, **row)', 'DB.apply_review(conn, it[\"id\"], \"reset\", now=now)'],\n        [\"tests/unit/test_multicase.py\"]),\n    \"M2_llm_calls_dropped_from_case_tables\": (\"app/db/db.py\",\n        ['\"llm_calls\", \"review_events\"'], ['\"review_events\"'],\n        [\"tests/unit/test_multicase.py::test_delete_case_removes_only_that_case\"]),\n    \"M3_rebuild_does_not_delete_old_file\": (\"app/db/db.py\",\n        ['os.remove(path + ext)'], ['pass'],\n        [\"tests/unit/test_multicase.py::test_old_schema_file_is_deleted_and_rebuilt\"]),\n}\nfor name, (rel, olds, news, tests) in MUTANTS.items():\n    dst = os.path.join(OUT, name)\n    if os.path.exists(dst):\n        shutil.rmtree(dst)\n    shutil.copytree(SRC, dst)\n    p = os.path.join(dst, rel)\n    text = open(p, encoding=\"utf-8\").read()\n    for old, new in zip(olds, news):\n        n = text.count(old)\n        assert n == 1, (name, old, n)\n        text = text.replace(old, new)\n    open(p, \"w\", encoding=\"utf-8\").write(text)\n    r = subprocess.run([PY, \"-m\", \"pytest\", *tests, \"-q\"], cwd=dst, capture_output=True, text=True)\n    print(f\"== {name}: {rel} edited ({len(olds)} replacement(s)); tests={tests}\")\n    print(\"   \", (r.stdout.strip().splitlines() or [\"<no output>\"])[-1])\n    for line in r.stdout.splitlines():\n        if line.startswith(\"FAILED\"):\n            print(\"   \", line[:160])\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python artifacts/review-evidence/T-050/r2_mutate.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_head_c61e84f /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_mut 2>&1 | tail -40",
 "description": "Write and run round-2 mutation script on committed tree copy"
}
````

### User / tool · 2026-11-02T02:19:05.735Z

**tool result**
````
== M1_pipeline_unscoped_persist: app/backend/pipeline.py edited (2 replacement(s)); tests=['tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids']
    1 failed in 1.10s
    FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids
== M1b_pipeline_unscoped_vs_test_multicase_only: app/backend/pipeline.py edited (2 replacement(s)); tests=['tests/unit/test_multicase.py']
    5 passed in 0.52s
== M2_llm_calls_dropped_from_case_tables: app/db/db.py edited (1 replacement(s)); tests=['tests/unit/test_multicase.py::test_delete_case_removes_only_that_case']
    1 failed in 0.23s
    FAILED tests/unit/test_multicase.py::test_delete_case_removes_only_that_case
== M3_rebuild_does_not_delete_old_file: app/db/db.py edited (1 replacement(s)); tests=['tests/unit/test_multicase.py::test_old_schema_file_is_deleted_and_rebuilt']
    1 failed in 0.14s
    FAILED tests/unit/test_multicase.py::test_old_schema_file_is_deleted_and_rebuilt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:10.244Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-050/pre_6c3aeb1p | head -3 && .venv/bin/python artifacts/review-evidence/T-050/legacy_probe.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/pre_6c3aeb1p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_head_c61e84f /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_legacy.sqlite 2>&1 | tail -6; echo \"--- files left beside legacy db\"; ls artifacts/review-evidence/T-050/ | grep r2_legacy; echo \"--- old 6c3aeb1^ marker in r2 db? user_version:\"; .venv/bin/python -c \"import sqlite3;c=sqlite3.connect('/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_legacy.sqlite');print(c.execute('PRAGMA user_version').fetchone(), c.execute('select count(*) from cases').fetchone())\"",
 "description": "Run legacy upgrade probe against committed tree"
}
````

### User / tool · 2026-11-02T02:19:10.909Z

**tool result**
````
CLAUDE.md
MASTER_PROMPT.md
app
STEP1 exit 0 pre-code ingest sample ok, records= 9
STEP2 exit 0 ['entries PK clause now: []', 'second case ingest ok', 'database schema version 0 != 3: old file deleted and rebuilt']
--- files left beside legacy db
r2_legacy.sqlite
--- old 6c3aeb1^ marker in r2 db? user_version:
(3,) (1,)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:18.516Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_head_c61e84f && grep -c 'PRIMARY KEY (case_id, id)' app/db/schema.sql; grep -n -E 'except|float\\(' app/db/db.py | head; echo '--- CLI run 1'; LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.pipeline evals/golden/sample.txt > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_cli_run1.txt 2>/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_cli_run1.err; echo \"exit=$?\"; echo '--- CLI run 2'; LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.pipeline evals/golden/sample.txt > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_cli_run2.txt 2>/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_cli_run2.err; echo \"exit=$?\"; cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050 && wc -l r2_cli_run1.txt r2_cli_run2.txt && diff r2_cli_run1.txt r2_cli_run2.txt && echo DETERMINISTIC_STDOUT_SAME; head -c 600 r2_cli_run1.txt; echo; tail -3 r2_cli_run1.err",
 "description": "Check schema PKs, except/float in db.py, run sample CLI twice and diff"
}
````

### User / tool · 2026-11-02T02:19:19.546Z

**tool result**
````
4
198:    except Exception:
246:    except Exception:
--- CLI run 1
exit=0
--- CLI run 2
exit=0
      45 r2_cli_run1.txt
      45 r2_cli_run2.txt
      90 total
DETERMINISTIC_STDOUT_SAME
Status: done   backend: fixture   records: 9   entries: 9   flags: 10   amounts: 3

TIMELINE
  January 9, 2026 - Austin EMS run report [needs_review]
      41M restrained driver, rear-ended at approx. 35 mph, complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
  January 9, 2026 - Central ER discharge summary [needs_review]
      Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week; ER charges $6,240.
  January 16, 2026 - Dr. Alvarez, primary care [needs
llm call failed call_id=c44f496aa09bf step=j4 attempt=1 prompt_hash=29ee418c79119a6311c1e2d6b9210fd3c4fd01f152f1dcef5a6acc0d5b917d58
llm call failed call_id=c97084d3f3a55 step=j4 attempt=1 prompt_hash=9391f6bf99db12e040f88843580adab24a5b2b06eab51ee982d85c36d2c761db
llm call failed call_id=cc55a5837a07f step=j4 attempt=1 prompt_hash=664c59ebfe49e6a09404138fe7cd6d77ba2306b53dfe431bc7ead34b14de3c4c
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:23.748Z

**tool call — Bash**
````
{
 "command": "LLM_BACKEND=fixture .venv/bin/python -m app.pipeline evals/golden/sample.txt > artifacts/review-evidence/T-050/r2_cli_wt.txt 2>artifacts/review-evidence/T-050/r2_cli_wt.err; echo \"wt exit=$?\"; head -1 artifacts/review-evidence/T-050/r2_cli_wt.txt; echo \"wt needs_review lines: $(grep -c 'needs_review' artifacts/review-evidence/T-050/r2_cli_wt.txt)  verified-or-ready lines: $(grep -c -E '\\[(verified|ready|supported)' artifacts/review-evidence/T-050/r2_cli_wt.txt)\"; echo \"committed needs_review lines: $(grep -c 'needs_review' artifacts/review-evidence/T-050/r2_cli_run1.txt)  fixture-miss lines in committed stderr: $(grep -c 'llm call failed' artifacts/review-evidence/T-050/r2_cli_run1.err)\"; echo \"wt fixture-miss lines: $(grep -c 'llm call failed' artifacts/review-evidence/T-050/r2_cli_wt.err)\"",
 "description": "Run sample CLI on working tree and compare judge fixture misses"
}
````

### User / tool · 2026-11-02T02:19:24.313Z

**tool result**
````
wt exit=0
Status: done   backend: fixture   records: 9   entries: 9   flags: 10   amounts: 3
wt needs_review lines: 6  verified-or-ready lines: 16
committed needs_review lines: 20  fixture-miss lines in committed stderr: 20
wt fixture-miss lines: 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:40.837Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_head_c61e84f && grep -n -E '^def test_' tests/unit/test_multicase.py; grep -n -E 'def connect|PRAGMA user_version|os\\.remove|old file deleted|for t in DB|_CASE_TABLES' app/db/db.py | head -12; grep -n -E 'def test_two_cases_coexist' tests/unit/test_api_routes.py; grep -n -E 'def purge_expired' app/db/db.py; cd /Users/arsis/zlayt-pm-project && git diff --stat 864676f c61e84f | tail -3",
 "description": "Collect exact line numbers at committed tree for finding evidence"
}
````

### User / tool · 2026-11-02T02:19:40.973Z

**tool result**
````
15:def test_two_golden_cases_back_to_back_in_one_file(tmp_path):
26:def test_full_pipeline_twice_in_one_file(tmp_path):
46:def test_delete_case_removes_only_that_case(tmp_path):
62:def test_case_scoped_lookup_and_ambiguous_bare_id(tmp_path):
75:def test_old_schema_file_is_deleted_and_rebuilt(tmp_path, caplog):
24:_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
36:def connect(path: str):
43:            version = probe.execute("PRAGMA user_version").fetchone()[0]
50:                    os.remove(path + ext)
51:            log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
58:    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
243:        for t in _CASE_TABLES:
260:            for t in _CASE_TABLES}
200:def test_two_cases_coexist_with_short_display_ids(env):
251:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
 tests/unit/test_manual_and_split.py | 121 ++++++++++++++++
 tests/unit/test_pdf_upload.py       |  57 ++++++++
 15 files changed, 737 insertions(+), 51 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:51.174Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-050/r2_head_c61e84f && sed -n '194,200p;242,248p' app/db/db.py",
 "description": "Inspect the two except clauses in db.py at committed tree"
}
````

### User / tool · 2026-11-02T02:19:51.280Z

**tool result**
````
                     (status, _enc(new_edited), now, item_id, row["case_id"]))
        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    try:
        for t in _CASE_TABLES:
            conn.execute(f"DELETE FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:20.929Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-050-staff-engineer-r2.md",
 "content": "# T-050 round 2 review: staff-engineer (Marcus Lee lens)\n\nVerdict: **changes**. No blocker remains. Round-1 blocker F1 (unscoped `_persist` at HEAD) is closed at the committed revision. Round-1 F4 (delete test checks only `records`) is closed. Round-1 F2 (no migration) is closed by a different mechanism, a delete-and-rebuild, which I rate major because it is silent to the user. Round-1 F3 (AC1 names the wrong files) is still open, minor.\n\nPinning: HEAD moved three times during this review (037cc89, then 864676f \"delete old-schema database at rebuild\", then c61e84f \"bump schema version to 3, real v2 rebuild test\"). All committed-tree checks ran against `git archive c61e84f` at `artifacts/review-evidence/T-050/r2_head_c61e84f`. The brief's first pytest run was against the working tree at 037cc89 (unpinned); its result is recorded below as well.\n\nBrief corrections (the brief's premises are out of date at HEAD c61e84f):\n- The brief says the rebuild is \"move-aside\". That was 7a450a1. At 864676f and c61e84f it is delete (`app/db/db.py:48-51`).\n- The brief says test_multicase.py has the two-case-coexist test. It has `test_two_golden_cases_back_to_back_in_one_file` (ingest only, no run) and `test_full_pipeline_twice_in_one_file` (run only, no ingest between). The API-order coexist test (ingest B after A ran, then run B) is `tests/unit/test_api_routes.py:200`. See F5.\n\nLabels: F2 and F5 are not spec violations of the card text, so they are major and minor respectively. F3 is a card-text mismatch, minor.\n\nCommands run (all pinned or quoted):\n```\n$ .venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_db.py -q 2>&1 | tail -2     (working tree, HEAD 037cc89 at the time, unpinned)\n............................                                             [100%]\n28 passed in 0.78s\n```\n```\n$ (cd artifacts/review-evidence/T-050/r2_head_c61e84f && .venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_db.py -q 2>&1 | tail -3)   (pinned c61e84f)\n28 passed in 0.81s\n$ ... pytest tests/unit -q  (pinned c61e84f)\n4 failed, 827 passed in 14.12s     (all 4 in tests/unit/test_t037_backend.py, see Outside this card)\n```\n```\n$ git show c61e84f:app/db/db.py | sed -n '36,58p'   (equivalently app/db/db.py at the archive)\n36: def connect(path: str):\n43:     version = probe.execute(\"PRAGMA user_version\").fetchone()[0]\n48:             for ext in (\"\", \"-wal\", \"-shm\", \"-journal\"):\n50:                     os.remove(path + ext)\n51:             log.warning(\"database schema version %s != %s: old file deleted and rebuilt\", version, SCHEMA_VERSION)\n58:     conn.execute(f\"PRAGMA user_version={SCHEMA_VERSION}\")\n```\n`user_version` check: present (db.py:43, 58). Move-aside: absent. Delete-and-rebuild: present (db.py:48-51). Test: `tests/unit/test_multicase.py:75` `test_old_schema_file_is_deleted_and_rebuilt`, which asserts no `*.old-*` leftovers and one log line.\n\nLegacy upgrade probe (pre-T-050 file written by `git archive 6c3aeb1^`, opened by c61e84f):\n```\n$ .venv/bin/python artifacts/review-evidence/T-050/legacy_probe.py <pre_6c3aeb1p> <r2_head_c61e84f> <r2_legacy.sqlite>\nSTEP1 exit 0 pre-code ingest sample ok, records= 9\nSTEP2 exit 0 ['entries PK clause now: []', 'second case ingest ok', 'database schema version 0 != 3: old file deleted and rebuilt']\n$ sqlite3-equivalent check on r2_legacy.sqlite: PRAGMA user_version -> 3, count(cases) -> 1\n```\nThe IntegrityError from round 1 is gone. The sample case from step 1 is also gone: only case_01 survives. The only signal is one server log line.\n\nMutation checks on the pinned tree (script `artifacts/review-evidence/T-050/r2_mutate.py`, output below):\n```\nM1_pipeline_unscoped_persist (pipeline.py: case=cid removed from update_item and apply_review)\n  tests=test_api_routes::test_two_cases_coexist_with_short_display_ids -> 1 failed (caught)\nM1b same mutant, tests=tests/unit/test_multicase.py -> 5 passed (NOT caught)\nM2_llm_calls_dropped_from_case_tables -> test_multicase::test_delete_case_removes_only_that_case -> 1 failed (caught)\nM3_rebuild_does_not_delete_old_file -> test_multicase::test_old_schema_file_is_deleted_and_rebuilt -> 1 failed (caught)\n```\n\nSample CLI, run twice on the pinned tree:\n```\n$ LLM_BACKEND=fixture .venv/bin/python -m app.pipeline evals/golden/sample.txt   (x2, archive c61e84f)\nexit 0, exit 0; diff run1 run2 -> empty (45 lines each, deterministic stdout)\nstderr: 20 x \"llm call failed ... step=j4\"; stdout: 20 needs_review lines\n```\nSame CLI on the working tree: exit 0, 0 \"llm call failed\", 6 needs_review lines. The committed tree is missing judge fixtures that exist in the working tree. See Outside this card.\n\nOther greps: `grep -c 'PRIMARY KEY (case_id, id)' app/db/schema.sql` -> 4. The two `except Exception:` clauses in db.py (lines 198 and 246) both `ROLLBACK` and `raise`. No swallowed exception in the rebuild path.\n\n## Round-1 status\n\n| Round-1 item | Status at c61e84f | Evidence |\n|---|---|---|\n| F1 blocker: `_persist` unscoped | Closed | `app/backend/pipeline.py:148,152` pass `case=cid`; M1 caught by test_api_routes |\n| F2 major: no migration | Changed. Major, open | Delete-on-upgrade, log line only; see finding 1 |\n| F3 minor: AC1 names test_db/test_pipeline | Open | `grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py` -> 0 and 0 at c61e84f; card AC1 text unchanged |\n| F4 minor: delete test checks records only | Closed | `tests/unit/test_multicase.py:56-58` loops `DB._CASE_TABLES`; M2 caught |\n\n## Findings\n\n1. **major: an upgrade silently deletes the user's cases; the only signal is a server log line.** `app/db/db.py:48-51` deletes the file when `user_version` differs, and the probe output above shows the step-1 sample case is gone. Retention is bounded (`app/backend/api.py:154-158` runs `purge_expired`), so the loss is within the 24 h policy, not corruption. The defect is invisibility, and it recurs on every future schema bump (`SCHEMA_VERSION` is 3 now and bumps on any `schema.sql` change). Fix: when the rebuild happens, expose a one-time visible reset (for example a `schema_reset` flag on the case-list response that the UI shows), or refuse to delete when non-expired cases exist and raise a named error. Acceptance: `legacy_probe.py` against c61e84f ends with the reset visible through the API response, not only `caplog`; a test asserts the flag.\n\n2. **minor (F3, still open): AC1 names files that have no case-scoped test.** The card's AC1 text (board card T-050) still says \"test in tests/unit/test_db.py and test_pipeline.py\"; `grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py` -> 0 and 0. The AC1 evidence cites `test_multicase.py \"3 passed\"`; the file now has 5 tests. Fix: amend the AC text to name test_multicase.py and update the evidence count, or add the case-scoped tests to the named files.\n\n3. **minor (new, F5): the F1 regression is guarded only by test_api_routes.** M1b (unscoped `_persist`) leaves `tests/unit/test_multicase.py` at 5 passed. Round 1 asked for an API-order test in test_multicase (ingest B after A has run, then run B). Not present: `test_two_golden_cases_back_to_back_in_one_file` only ingests, and `test_full_pipeline_twice_in_one_file` only runs. Fix: add that test to test_multicase.py. Acceptance: `r2_mutate.py` M1b reports at least one failure.\n\n## Outside this card (observed, not T-050 findings)\n\n- At committed c61e84f, `pytest tests/unit -q` -> `4 failed, 827 passed`, all in `tests/unit/test_t037_backend.py` (replay fixture misses). The working tree passes that file: `20 passed in 1.81s`. `git status` shows `tests/fixtures/llm/*.json` modified or untracked in the working tree. The committed sample CLI has 20 \"llm call failed ... step=j4\" and 20 needs_review. Route to the orchestrator: commit the judge fixtures.\n- `grep -rn -i purge app/` returns 14 hits, so the 24 h purge exists in code. T-034 AC6 says the T-031 AC3 purge \"moves to M4\"; the card and the code disagree. Outside my lens to resolve.\n\n## What is right\n\n- Composite PK `(case_id, id)` on all four item tables (`app/db/schema.sql`, 4 matches), and every writer in `pipeline.py` passes `case=`.\n- The delete test now checks every per-case table including `llm_calls`, and M2 is caught.\n- The rebuild path re-raises on error and has a test that checks no leftover `-wal`/`-shm` files and no copy of the old text.\n\n```json\n{\"card\": \"T-050\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git archive c61e84f (HEAD at review end; HEAD moved 037cc89 -> 864676f -> c61e84f during the review), extracted to artifacts/review-evidence/T-050/r2_head_c61e84f; working tree for the brief's first pytest run (unpinned); sample case and case_01_date_formats; no live app URL (in-process pytest and the CLI only)\",\n \"exercised\": [\n  \".venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_db.py -q 2>&1 | tail -2 (working tree, HEAD 037cc89) -> '28 passed in 0.78s'\",\n  \"pinned c61e84f archive: pytest tests/unit/test_multicase.py tests/unit/test_db.py -q -> '28 passed in 0.81s'; pytest tests/unit -q -> '4 failed, 827 passed in 14.12s' (all test_t037_backend.py, fixture misses)\",\n  \"git show HEAD:app/db/db.py (037cc89 move-aside; 864676f and c61e84f delete) and sed/grep of app/db/db.py at c61e84f: user_version check db.py:43,58; delete loop db.py:48-51\",\n  \"artifacts/review-evidence/T-050/legacy_probe.py with pre_6c3aeb1p (git archive 6c3aeb1^) -> r2_head_c61e84f -> r2_legacy.sqlite: 'STEP2 exit 0 ... database schema version 0 != 3: old file deleted and rebuilt'; post-check user_version 3, cases count 1 (sample case lost)\",\n  \"artifacts/review-evidence/T-050/r2_mutate.py on the pinned archive copy (repo not modified): M1 -> test_api_routes coexist 1 failed; M1b -> test_multicase 5 passed; M2 -> test_delete_case 1 failed; M3 -> test_old_schema 1 failed\",\n  \"LLM_BACKEND=fixture .venv/bin/python -m app.pipeline evals/golden/sample.txt, run twice on the pinned archive: exit 0 both, stdout diff empty; 20 'llm call failed' on stderr; same on working tree: 0 misses, 6 needs_review\",\n  \"grep -c 'PRIMARY KEY (case_id, id)' app/db/schema.sql -> 4; grep -n 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py -> 0 and 0; sed of db.py except blocks at 194-200 and 242-248 (both ROLLBACK and raise)\",\n  \"board.py show T-050 (AC1-3 text and evidence; commit list 6c3aeb1, 81df4e0, 7a450a1, 864676f; round-2 notes)\",\n  \"git log --oneline -6 and git rev-parse HEAD at three points during the review (HEAD moved)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"composite_pk_and_writers\": 5, \"committed_state_consistency\": 3, \"short_display_ids\": 5, \"delete_case_isolation\": 5, \"test_adequacy_for_ac\": 3, \"upgrade_safety\": 2, \"failure_visibility\": 2},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Schema-version upgrade silently deletes the user's cases; the only signal is one server log line\",\n   \"evidence\": \"app/db/db.py:48-51 (for ext ... os.remove(path + ext)) and :51 log.warning(...'old file deleted and rebuilt'); r2 legacy_probe output: 'STEP2 exit 0 [... database schema version 0 != 3: old file deleted and rebuilt]'; post-probe count(cases)=1, the step-1 sample case is gone; retention bounded by app/backend/api.py:154-158 (purge_expired)\",\n   \"why_it_matters\": \"Round-1 F2 asked for a migration or a named error that tells the user what to do. A log line is neither, and a paralegal never sees it. The reset repeats on every SCHEMA_VERSION bump (currently 3). Within the 24 h policy this is loss of in-flight work with no visible signal, which violates 'failures are visible'.\",\n   \"fix\": \"On rebuild, set a one-time reset flag that the case-list response carries and the UI shows (for example 'data reset after upgrade, paste again'); or refuse to delete while non-expired cases exist and raise a named error naming the file. Either way, record the choice on the card.\",\n   \"acceptance_test\": \"Run artifacts/review-evidence/T-050/legacy_probe.py against artifacts/review-evidence/T-050/r2_head_c61e84f (or its successor sha); the API case-list response for the rebuilt file carries the reset flag; a unit test in tests/unit/test_multicase.py asserts the flag, not only caplog.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"AC1 still names test_db.py and test_pipeline.py, which have no case-scoped tests\",\n   \"evidence\": \"board card T-050 ac n=1 text: 'test in tests/unit/test_db.py and test_pipeline.py'; `grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py` -> 0 and 0 at c61e84f; AC1 evidence says 'tests/unit/test_multicase.py (3 passed ...)' but test_multicase.py now has 5 tests (grep -n '^def test_')\",\n   \"why_it_matters\": \"The AC names where the proof lives. A reader following the card will not find it there. The evidence count is stale.\",\n   \"fix\": \"Amend AC1 text to name tests/unit/test_multicase.py and update the evidence count to the current result, or add one case-scoped test to each named file.\",\n   \"acceptance_test\": \"grep -n 'test_multicase' on the AC1 text; the evidence count matches `pytest tests/unit/test_multicase.py -q`.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The F1 regression (unscoped _persist) is guarded only by test_api_routes, not test_multicase\",\n   \"evidence\": \"artifacts/review-evidence/T-050/r2_mutate.py M1b: pipeline.py case=cid removed from update_item and apply_review; `pytest tests/unit/test_multicase.py -q` -> '5 passed'. The same mutant under tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids -> '1 failed'. test_multicase.py:15 ingests only; :26 runs only, with no ingest between.\",\n   \"why_it_matters\": \"Round-1 F1 asked for an API-order test in test_multicase.py. Without it the multicase file would pass with the blocker reintroduced; the guard sits in a different file.\",\n   \"fix\": \"Add a test to tests/unit/test_multicase.py that ingests case B after case A has run, then calls run_pipeline for case B (the API order), and asserts both cases finish with status ready.\",\n   \"acceptance_test\": \"r2_mutate.py M1b (tests=tests/unit/test_multicase.py) reports at least one failure.\"}\n ],\n \"whats_right\": [\n  \"Round-1 blocker closed at the committed revision: app/backend/pipeline.py:148 and :152 pass case=cid; the API-order coexist test catches the unscoped mutant.\",\n  \"The delete-isolation test (tests/unit/test_multicase.py:56-58) loops over every DB._CASE_TABLES table; dropping llm_calls is caught.\",\n  \"Composite PK (case_id, id) on four tables and a rebuild path with no swallowed exceptions (db.py:198,246 re-raise) and a test for leftover files.\"\n ],\n \"questions_for_chris\": [\n  \"Is a silent delete of up to 24 h of in-flight cases on each schema bump acceptable for the demo and paralegal machines, or must the UI show a reset notice (finding 1)?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:20:21.121Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-050-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:26.201Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t050_namespacing_review_patterns.md",
 "old_string": "Related: [[project_db_review_patterns]], [[project_wiring_review_patterns]], [[project_harness_review_patterns]].",
 "new_string": "Round 2 (reviews/T-050-staff-engineer-r2.md, verdict changes, pinned c61e84f):\n- Round-1 blocker closed (case=cid committed); delete test now loops _CASE_TABLES. Rebuild changed from move-aside (7a450a1) to\n  delete-on-upgrade (864676f, T-040 security r2) with a log line only. Rated major: the user's in-flight cases vanish with no UI signal.\n- Guard location gap: the F1 regression is caught only by test_api_routes (API-order test), not test_multicase (ingest-only and\n  run-only tests). Mutant M1b passes test_multicase. Pattern: check which file guards a regression, not only that some test does.\n- Committed tree lacked judge fixtures (tests/fixtures/llm modified/untracked in the working tree): test_t037 4 failures and\n  20 \"llm call failed\" in the committed sample CLI. Working tree is clean. Route to orchestrator as outside-card.\n- HEAD moved 3 times during the review. Pin with `git archive <short sha>` into one dir and run everything there.\n  The git-guard hook rejects `$(...)` and `$VAR` in bash commands; use literal shas and paths. `git reflog` is blocked for reviewers.\n\nRelated: [[project_db_review_patterns]], [[project_wiring_review_patterns]], [[project_harness_review_patterns]]."
}
````

### User / tool · 2026-11-02T02:20:26.354Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t050_namespacing_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:28.089Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1: commit missing producer case= lines, no DB migration, git-archive reproduction method",
 "new_string": "- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1-r2: producer case= fix, delete-on-upgrade silent loss, guard in wrong file, pin HEAD by archive"
}
````

### User / tool · 2026-11-02T02:20:28.188Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:30.300Z

Verdict changes, no blockers: the round-1 blocker is closed at c61e84f, the one open major is that schema-version rebuild silently deletes in-flight cases with only a log line (`/Users/arsis/zlayt-pm-project/reviews/T-050-staff-engineer-r2.md`; HEAD moved during the review, so checks are pinned to `git archive c61e84f`).
