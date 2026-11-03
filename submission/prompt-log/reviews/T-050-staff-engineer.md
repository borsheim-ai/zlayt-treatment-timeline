# T-050 review: staff-engineer (Marcus Lee lens)

Verdict: **fail**. The namespacing design is right (composite key, every writer in `app/db/db.py` takes `case=`, ambiguous bare ids raise). The committed change is not runnable for a second case: commit `6c3aeb1` leaves `app/backend/pipeline.py` `_persist` unscoped, so the card's own AC2 test fails at that commit. The three `case=cid` lines exist only as uncommitted working-tree WIP (mixed in with unrelated backend-2 edits). Blocker: F1. Major: F2 (no migration for DB files made before T-050). Minors: F3, F4.

Labels: F1 violates AC1/AC2 (two cases coexist; "done" evidence fails at the commit), so it is a blocker. F2 is a persistence-upgrade hazard, rated major. F3 and F4 are "the AC names the wrong place / the AC test is weaker than the AC" and are minor.

Tree note: HEAD moved during this review (6c3aeb1 → 4e8f43d by other commits; pipeline.py still has no `case=cid` at 4e8f43d). The first brief-command run gave `36 passed`; a later run gave `1 failed, 40 passed` on a test unrelated to T-050 (see "Outside this card").

Model note: this review ran as `claude-haiku-5-5`. The dossier expects `claude-sonnet-5-5`; the record uses the model that ran.

```json
{"card": "T-050", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 6c3aeb1 (card commits) plus the working tree at review time (uncommitted app/backend/pipeline.py WIP); HEAD 4e8f43d checked at the end (pipeline.py unchanged since 6c3aeb1). No live app URL used: the HTTP API was exercised in-process with fastapi TestClient. Sample case and case_01_date_formats.",
 "exercised": [
  "python3 tools/board.py show T-050 (AC read; commit list 6c3aeb1; ac evidence strings)",
  ".venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_api_routes.py -q -> '36 passed in 4.27s' (first run); same command later -> '1 failed, 40 passed in 4.37s' (FAILED test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode; tree had moved to HEAD 4e8f43d)",
  ".venv/bin/python -m pytest tests/unit -q (working tree) -> '1 failed, 762 passed in 10.38s' (same unrelated test)",
  "git show 6c3aeb1 (full diff of app/db/db.py, app/db/schema.sql, app/backend/review.py, app/backend/present.py, tests/unit/test_api_routes.py, tests/unit/test_multicase.py) read in full",
  "git show HEAD:app/backend/pipeline.py | grep -n: lines 137 (add_item), 141 (update_item without case=), 145 (apply_review without case=); git show HEAD:app/backend/pipeline.py | grep -c 'case=cid' -> 0",
  "git diff HEAD -- app/backend/pipeline.py: adds case=cid at the same _persist calls (uncommitted), plus unrelated removals of sentences/body_offset/judges_failed",
  "artifacts/review-evidence/T-050/t050_check.py run on the working tree (outputs in artifacts/review-evidence/T-050/worktree/stdout.txt): two golden cases into one sqlite file via ingest_case + run_pipeline (Part A) and via POST /api/cases, POST /run, review, DELETE (Part B)",
  "same script on git archive 6c3aeb1 (artifacts/review-evidence/T-050/head_6c3aeb1/stdout.txt): RAISED ValueError 'item id a1 exists in several cases; pass case='; API run status=failed, error run_failed for both cases",
  "same script on git archive 6c3aeb1^ (artifacts/review-evidence/T-050/pre_6c3aeb1p/stdout.txt): baseline collision reproduced: 'ingest_case case_01_date_formats: RAISED IntegrityError: UNIQUE constraint failed: records.id'",
  "artifacts/review-evidence/T-050/legacy_probe.py: pre-T-050 code writes sample into a file, current code opens the same file and ingests case_01 -> 'STEP1 exit 0 ... records= 9', 'STEP2 exit 1 ... sqlite3.IntegrityError: UNIQUE constraint failed: records.id'",
  "artifacts/review-evidence/T-050/single_case_probe.py on the archives (single-case run; used only to rule out the single-case path)",
  "pytest on the 6c3aeb1 archive with the untracked LLM fixtures copied in (artifacts/review-evidence/T-050/h1_head_plus_fixtures): 'FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids ... 1 failed, 65 passed'; with the working-tree pipeline.py also copied in (h2_head_plus_fixtures_plus_wt_pipeline): '66 passed in 5.19s'",
  "pytest on the 4e8f43d archive (artifacts/review-evidence/T-050/head_4e8f43d): '1 failed, 40 passed' (test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode, IndexError at tests/unit/test_api_routes.py:129)",
  "artifacts/review-evidence/T-050/mutate.py (scratch copies under artifacts/review-evidence/T-050/mut/, repo not modified): M1 _find not case-scoped -> 2 failed (test_multicase::test_full_pipeline_twice_in_one_file, test_api_routes::test_two_cases_coexist_with_short_display_ids); M2 schema PK (id) only -> 4 failed; M3 llm_calls dropped from _CASE_TABLES -> 6 failed, NOT including test_multicase::test_delete_case_removes_only_that_case; M4 apply_review UPDATE not case-scoped -> 3 failed",
  "grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py -> 0 and 0",
  "app/db/db.py read in full (_find 104-118, update_item 141-153, apply_review 156-178, delete_case 216-225); app/db/schema.sql read (four PRIMARY KEY (case_id, id) clauses); grep of every DB item call site in app/ (review.py, present.py, pipeline.py, api.py): all pass case=; raw SQL scoped by case_id except llm_calls by random call id"
 ],
 "verdict": "fail",
 "scores": {"composite_pk_and_writers": 4, "committed_state_consistency": 1, "short_display_ids": 5, "delete_case_isolation": 4, "test_adequacy_for_ac": 2, "upgrade_safety": 2, "failure_visibility": 3},
 "findings": [
  {"severity": "blocker",
   "title": "Committed T-050 change leaves pipeline._persist unscoped: a second case's run fails, and the card's own AC2 test fails at 6c3aeb1",
   "evidence": "git show HEAD:app/backend/pipeline.py: line 141 'DB.update_item(conn, it[\"id\"], now=now, **row)' and line 145 'DB.apply_review(conn, it[\"id\"], \"reset\", now=now)' carry no case=; 'git show HEAD:app/backend/pipeline.py | grep -c case=cid' -> 0 at 4e8f43d too. The fix exists only as uncommitted diff (git diff HEAD -- app/backend/pipeline.py, lines 139 and 143 in the working tree). Repro 1: git archive 6c3aeb1 into artifacts/review-evidence/T-050/head_6c3aeb1, copy tests/fixtures/llm/*.json in, run .venv/bin/python -m pytest tests/unit/test_api_routes.py tests/unit/test_multicase.py tests/unit/test_db.py tests/unit/test_pipeline.py -q -> 'FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids ... 1 failed, 65 passed'. Repro 2: same tree with the working-tree pipeline.py copied in -> '66 passed in 5.19s'. Repro 3: artifacts/review-evidence/T-050/t050_check.py on head_6c3aeb1 -> 'run_pipeline sample: RAISED ValueError: item id 'a1' exists in several cases; pass case=' and 'run sample: POST=202 final status=failed ... error={'code': 'run_failed'...}' for both cases.",
   "why_it_matters": "AC1 and AC2 require two cases to coexist in one file. At the committed revision the second case's run fails, and that is the exact sequence the API performs (create, then run). The card is marked done and AC2 cites a test that fails at the commit. The green tests hide it: test_multicase::test_full_pipeline_twice_in_one_file calls run_pipeline on fresh case ids without ingest_case, so it never reaches the update path. Same pattern as T-030 r2: the fix is green in a unit test while the producer path is not wired.",
   "fix": "Commit the case=cid argument on the three _persist calls (pipeline.py:141 and :145 at HEAD; :139 and :143 in the working tree) in a commit that does not carry the unrelated backend-2 WIP, or in the same commit as db.py. Add a test to tests/unit/test_multicase.py that does ingest_case for case B after case A has run, then run_pipeline for case B (the API order).",
   "acceptance_test": "From the fix commit: git archive <fix> | tar -x -C <dir>; cd <dir> && .venv/bin/python -m pytest tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids tests/unit/test_multicase.py -q passes; artifacts/review-evidence/T-050/t050_check.py <dir> <out> Part B reports 'final status=ready' for both cases."},
  {"severity": "major",
   "title": "No migration for sqlite files created before T-050: the new composite key is silently not applied to an existing file",
   "evidence": "artifacts/review-evidence/T-050/legacy_probe.py output: 'STEP1 exit 0 pre-code ingest sample ok, records= 9' then 'STEP2 exit 1 ... sqlite3.IntegrityError: UNIQUE constraint failed: records.id'. Cause: app/db/db.py:34-35 executes schema.sql, which uses CREATE TABLE IF NOT EXISTS, so the old global-PK tables are kept; there is no PRAGMA user_version check. The default DB path is app/backend/api.py:45 (data/zlayt.sqlite). The handoff's 'delete old sqlite files' is a manual step, not in the AC or in code.",
   "why_it_matters": "Any machine with a pre-upgrade DB file gets a raw IntegrityError on the second case, and the first case's data stays under the old schema. This is the persistence failure the dossier warns about: a schema change that does not reach existing data without a visible signal.",
   "fix": "Read PRAGMA user_version in connect(). On an old schema, either migrate (rebuild the four item tables with PRIMARY KEY (case_id, id), copying rows) or raise a named error that tells the user which file to remove. Bump the version in schema.sql.",
   "acceptance_test": "Create a file with the pre-T-050 tree (git archive 6c3aeb1^), then open it with the fix tree and ingest a second case. Either the rows migrate and the second case ingests, or connect() raises a named error. artifacts/review-evidence/T-050/legacy_probe.py must no longer end in IntegrityError."},
  {"severity": "minor",
   "title": "AC1 names tests/unit/test_db.py and test_pipeline.py; neither file has a case-scoped test",
   "evidence": "grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py -> 0 and 0. AC1 evidence cites tests/unit/test_multicase.py (a new file).",
   "why_it_matters": "The AC says where the proof lives. A reader following the card will not find it in the named files.",
   "fix": "Add one case-scoped test to test_db.py (get_item/apply_review with case=, ambiguous bare id raises ValueError) and one to test_pipeline.py, or amend the AC text to name test_multicase.py.",
   "acceptance_test": "grep -l 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py lists both files, and pytest on those two files passes."},
  {"severity": "minor",
   "title": "AC3 delete test asserts only the records count for case A",
   "evidence": "tests/unit/test_multicase.py:46-53: 'assert DB.get_case(conn, a) is None and DB.table_counts(conn, a).get(\"records\", 0) == 0'. Mutant M3 (llm_calls removed from _CASE_TABLES, app/db/db.py:21) leaves this test green; it is caught only by test_db.py (4 tests) and test_api_routes.py (2 tests) in mutate.py.",
   "why_it_matters": "ADR-006 requires prompts (llm_calls) to be deleted with the case. The AC3 test as written would stay green if prompts survived. The protection comes from older tests, not from the test the card cites.",
   "fix": "Assert every table in _CASE_TABLES has zero rows for case A and unchanged counts for case B.",
   "acceptance_test": "Apply mutation M3 (drop llm_calls from _CASE_TABLES) in a scratch copy; tests/unit/test_multicase.py::test_delete_case_removes_only_that_case must fail."}
 ],
 "whats_right": [
  "Composite PK (case_id, id) on records, entries, amounts and flags, and every db.py/review.py writer takes case= and scopes its UPDATE/DELETE by case_id; an ambiguous bare id raises ValueError (app/db/db.py:116-117) instead of picking a row.",
  "Display ids stay short in API JSON (e1, a1, f_gap_r6_r7, no random suffix) and identical across cases, as the AC2 text requires; delete_case leaves the other case's rows unchanged in every table on both code paths.",
  "Four injected defects in scratch copies (unscoped _find, global PK, skipped llm_calls delete, unscoped apply_review UPDATE) were each caught by at least one test."
 ],
 "questions_for_chris": [
  "Is a DB file created before T-050 a state the demo or paralegal machines can be in? If yes, F2 must be fixed before the gate. If no, a documented 'remove data/zlayt.sqlite on upgrade' step is acceptable and F2 drops to a note."
 ]}
```

## Outside this card (observed, not T-050 findings)

- `tests/unit/test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode` fails at HEAD 4e8f43d (`IndexError` at line 129: `warnings` is empty, so the judge did not report JUDGE_UNAVAILABLE). It passed on the 6c3aeb1 tree in my run. Not caused by the T-050 diff as far as I can tell. Flagging for the orchestrator to route.
- In the probe, the fixture backend's judge steps (j1 to j4) raised 64 `llm call failed` lines on the working tree, and every probe entry ended `needs_review` with `["JUDGE_UNAVAILABLE"]`. That is an honest visible state, but it means the probe proves id and isolation behaviour, not verified output.
- At my review start, 251 LLM fixture files under `tests/fixtures/llm/` were untracked, so a clean checkout of 6c3aeb1 could not reproduce the suite. At 4e8f43d `git status` shows 0 untracked fixtures, so this is resolved.

Not exercised: live app at http://localhost:7860, the eval runner, the `python -m app.pipeline evals/golden/sample.txt` CLI run-twice determinism check, export.
