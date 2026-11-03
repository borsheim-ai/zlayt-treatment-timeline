# T-050 round 2 review: staff-engineer (Marcus Lee lens)

Verdict: **changes**. No blocker remains. Round-1 blocker F1 (unscoped `_persist` at HEAD) is closed at the committed revision. Round-1 F4 (delete test checks only `records`) is closed. Round-1 F2 (no migration) is closed by a different mechanism, a delete-and-rebuild, which I rate major because it is silent to the user. Round-1 F3 (AC1 names the wrong files) is still open, minor.

Pinning: HEAD moved three times during this review (037cc89, then 864676f "delete old-schema database at rebuild", then c61e84f "bump schema version to 3, real v2 rebuild test"). All committed-tree checks ran against `git archive c61e84f` at `artifacts/review-evidence/T-050/r2_head_c61e84f`. The brief's first pytest run was against the working tree at 037cc89 (unpinned); its result is recorded below as well.

Brief corrections (the brief's premises are out of date at HEAD c61e84f):
- The brief says the rebuild is "move-aside". That was 7a450a1. At 864676f and c61e84f it is delete (`app/db/db.py:48-51`).
- The brief says test_multicase.py has the two-case-coexist test. It has `test_two_golden_cases_back_to_back_in_one_file` (ingest only, no run) and `test_full_pipeline_twice_in_one_file` (run only, no ingest between). The API-order coexist test (ingest B after A ran, then run B) is `tests/unit/test_api_routes.py:200`. See F5.

Labels: F2 and F5 are not spec violations of the card text, so they are major and minor respectively. F3 is a card-text mismatch, minor.

Commands run (all pinned or quoted):
```
$ .venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_db.py -q 2>&1 | tail -2     (working tree, HEAD 037cc89 at the time, unpinned)
............................                                             [100%]
28 passed in 0.78s
```
```
$ (cd artifacts/review-evidence/T-050/r2_head_c61e84f && .venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_db.py -q 2>&1 | tail -3)   (pinned c61e84f)
28 passed in 0.81s
$ ... pytest tests/unit -q  (pinned c61e84f)
4 failed, 827 passed in 14.12s     (all 4 in tests/unit/test_t037_backend.py, see Outside this card)
```
```
$ git show c61e84f:app/db/db.py | sed -n '36,58p'   (equivalently app/db/db.py at the archive)
36: def connect(path: str):
43:     version = probe.execute("PRAGMA user_version").fetchone()[0]
48:             for ext in ("", "-wal", "-shm", "-journal"):
50:                     os.remove(path + ext)
51:             log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
58:     conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
```
`user_version` check: present (db.py:43, 58). Move-aside: absent. Delete-and-rebuild: present (db.py:48-51). Test: `tests/unit/test_multicase.py:75` `test_old_schema_file_is_deleted_and_rebuilt`, which asserts no `*.old-*` leftovers and one log line.

Legacy upgrade probe (pre-T-050 file written by `git archive 6c3aeb1^`, opened by c61e84f):
```
$ .venv/bin/python artifacts/review-evidence/T-050/legacy_probe.py <pre_6c3aeb1p> <r2_head_c61e84f> <r2_legacy.sqlite>
STEP1 exit 0 pre-code ingest sample ok, records= 9
STEP2 exit 0 ['entries PK clause now: []', 'second case ingest ok', 'database schema version 0 != 3: old file deleted and rebuilt']
$ sqlite3-equivalent check on r2_legacy.sqlite: PRAGMA user_version -> 3, count(cases) -> 1
```
The IntegrityError from round 1 is gone. The sample case from step 1 is also gone: only case_01 survives. The only signal is one server log line.

Mutation checks on the pinned tree (script `artifacts/review-evidence/T-050/r2_mutate.py`, output below):
```
M1_pipeline_unscoped_persist (pipeline.py: case=cid removed from update_item and apply_review)
  tests=test_api_routes::test_two_cases_coexist_with_short_display_ids -> 1 failed (caught)
M1b same mutant, tests=tests/unit/test_multicase.py -> 5 passed (NOT caught)
M2_llm_calls_dropped_from_case_tables -> test_multicase::test_delete_case_removes_only_that_case -> 1 failed (caught)
M3_rebuild_does_not_delete_old_file -> test_multicase::test_old_schema_file_is_deleted_and_rebuilt -> 1 failed (caught)
```

Sample CLI, run twice on the pinned tree:
```
$ LLM_BACKEND=fixture .venv/bin/python -m app.pipeline evals/golden/sample.txt   (x2, archive c61e84f)
exit 0, exit 0; diff run1 run2 -> empty (45 lines each, deterministic stdout)
stderr: 20 x "llm call failed ... step=j4"; stdout: 20 needs_review lines
```
Same CLI on the working tree: exit 0, 0 "llm call failed", 6 needs_review lines. The committed tree is missing judge fixtures that exist in the working tree. See Outside this card.

Other greps: `grep -c 'PRIMARY KEY (case_id, id)' app/db/schema.sql` -> 4. The two `except Exception:` clauses in db.py (lines 198 and 246) both `ROLLBACK` and `raise`. No swallowed exception in the rebuild path.

## Round-1 status

| Round-1 item | Status at c61e84f | Evidence |
|---|---|---|
| F1 blocker: `_persist` unscoped | Closed | `app/backend/pipeline.py:148,152` pass `case=cid`; M1 caught by test_api_routes |
| F2 major: no migration | Changed. Major, open | Delete-on-upgrade, log line only; see finding 1 |
| F3 minor: AC1 names test_db/test_pipeline | Open | `grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py` -> 0 and 0 at c61e84f; card AC1 text unchanged |
| F4 minor: delete test checks records only | Closed | `tests/unit/test_multicase.py:56-58` loops `DB._CASE_TABLES`; M2 caught |

## Findings

1. **major: an upgrade silently deletes the user's cases; the only signal is a server log line.** `app/db/db.py:48-51` deletes the file when `user_version` differs, and the probe output above shows the step-1 sample case is gone. Retention is bounded (`app/backend/api.py:154-158` runs `purge_expired`), so the loss is within the 24 h policy, not corruption. The defect is invisibility, and it recurs on every future schema bump (`SCHEMA_VERSION` is 3 now and bumps on any `schema.sql` change). Fix: when the rebuild happens, expose a one-time visible reset (for example a `schema_reset` flag on the case-list response that the UI shows), or refuse to delete when non-expired cases exist and raise a named error. Acceptance: `legacy_probe.py` against c61e84f ends with the reset visible through the API response, not only `caplog`; a test asserts the flag.

2. **minor (F3, still open): AC1 names files that have no case-scoped test.** The card's AC1 text (board card T-050) still says "test in tests/unit/test_db.py and test_pipeline.py"; `grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py` -> 0 and 0. The AC1 evidence cites `test_multicase.py "3 passed"`; the file now has 5 tests. Fix: amend the AC text to name test_multicase.py and update the evidence count, or add the case-scoped tests to the named files.

3. **minor (new, F5): the F1 regression is guarded only by test_api_routes.** M1b (unscoped `_persist`) leaves `tests/unit/test_multicase.py` at 5 passed. Round 1 asked for an API-order test in test_multicase (ingest B after A has run, then run B). Not present: `test_two_golden_cases_back_to_back_in_one_file` only ingests, and `test_full_pipeline_twice_in_one_file` only runs. Fix: add that test to test_multicase.py. Acceptance: `r2_mutate.py` M1b reports at least one failure.

## Outside this card (observed, not T-050 findings)

- At committed c61e84f, `pytest tests/unit -q` -> `4 failed, 827 passed`, all in `tests/unit/test_t037_backend.py` (replay fixture misses). The working tree passes that file: `20 passed in 1.81s`. `git status` shows `tests/fixtures/llm/*.json` modified or untracked in the working tree. The committed sample CLI has 20 "llm call failed ... step=j4" and 20 needs_review. Route to the orchestrator: commit the judge fixtures.
- `grep -rn -i purge app/` returns 14 hits, so the 24 h purge exists in code. T-034 AC6 says the T-031 AC3 purge "moves to M4"; the card and the code disagree. Outside my lens to resolve.

## What is right

- Composite PK `(case_id, id)` on all four item tables (`app/db/schema.sql`, 4 matches), and every writer in `pipeline.py` passes `case=`.
- The delete test now checks every per-case table including `llm_calls`, and M2 is caught.
- The rebuild path re-raises on error and has a test that checks no leftover `-wal`/`-shm` files and no copy of the old text.

```json
{"card": "T-050", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive c61e84f (HEAD at review end; HEAD moved 037cc89 -> 864676f -> c61e84f during the review), extracted to artifacts/review-evidence/T-050/r2_head_c61e84f; working tree for the brief's first pytest run (unpinned); sample case and case_01_date_formats; no live app URL (in-process pytest and the CLI only)",
 "exercised": [
  ".venv/bin/python -m pytest tests/unit/test_multicase.py tests/unit/test_db.py -q 2>&1 | tail -2 (working tree, HEAD 037cc89) -> '28 passed in 0.78s'",
  "pinned c61e84f archive: pytest tests/unit/test_multicase.py tests/unit/test_db.py -q -> '28 passed in 0.81s'; pytest tests/unit -q -> '4 failed, 827 passed in 14.12s' (all test_t037_backend.py, fixture misses)",
  "git show HEAD:app/db/db.py (037cc89 move-aside; 864676f and c61e84f delete) and sed/grep of app/db/db.py at c61e84f: user_version check db.py:43,58; delete loop db.py:48-51",
  "artifacts/review-evidence/T-050/legacy_probe.py with pre_6c3aeb1p (git archive 6c3aeb1^) -> r2_head_c61e84f -> r2_legacy.sqlite: 'STEP2 exit 0 ... database schema version 0 != 3: old file deleted and rebuilt'; post-check user_version 3, cases count 1 (sample case lost)",
  "artifacts/review-evidence/T-050/r2_mutate.py on the pinned archive copy (repo not modified): M1 -> test_api_routes coexist 1 failed; M1b -> test_multicase 5 passed; M2 -> test_delete_case 1 failed; M3 -> test_old_schema 1 failed",
  "LLM_BACKEND=fixture .venv/bin/python -m app.pipeline evals/golden/sample.txt, run twice on the pinned archive: exit 0 both, stdout diff empty; 20 'llm call failed' on stderr; same on working tree: 0 misses, 6 needs_review",
  "grep -c 'PRIMARY KEY (case_id, id)' app/db/schema.sql -> 4; grep -n 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py -> 0 and 0; sed of db.py except blocks at 194-200 and 242-248 (both ROLLBACK and raise)",
  "board.py show T-050 (AC1-3 text and evidence; commit list 6c3aeb1, 81df4e0, 7a450a1, 864676f; round-2 notes)",
  "git log --oneline -6 and git rev-parse HEAD at three points during the review (HEAD moved)"
 ],
 "verdict": "changes",
 "scores": {"composite_pk_and_writers": 5, "committed_state_consistency": 3, "short_display_ids": 5, "delete_case_isolation": 5, "test_adequacy_for_ac": 3, "upgrade_safety": 2, "failure_visibility": 2},
 "findings": [
  {"severity": "major",
   "title": "Schema-version upgrade silently deletes the user's cases; the only signal is one server log line",
   "evidence": "app/db/db.py:48-51 (for ext ... os.remove(path + ext)) and :51 log.warning(...'old file deleted and rebuilt'); r2 legacy_probe output: 'STEP2 exit 0 [... database schema version 0 != 3: old file deleted and rebuilt]'; post-probe count(cases)=1, the step-1 sample case is gone; retention bounded by app/backend/api.py:154-158 (purge_expired)",
   "why_it_matters": "Round-1 F2 asked for a migration or a named error that tells the user what to do. A log line is neither, and a paralegal never sees it. The reset repeats on every SCHEMA_VERSION bump (currently 3). Within the 24 h policy this is loss of in-flight work with no visible signal, which violates 'failures are visible'.",
   "fix": "On rebuild, set a one-time reset flag that the case-list response carries and the UI shows (for example 'data reset after upgrade, paste again'); or refuse to delete while non-expired cases exist and raise a named error naming the file. Either way, record the choice on the card.",
   "acceptance_test": "Run artifacts/review-evidence/T-050/legacy_probe.py against artifacts/review-evidence/T-050/r2_head_c61e84f (or its successor sha); the API case-list response for the rebuilt file carries the reset flag; a unit test in tests/unit/test_multicase.py asserts the flag, not only caplog."},
  {"severity": "minor",
   "title": "AC1 still names test_db.py and test_pipeline.py, which have no case-scoped tests",
   "evidence": "board card T-050 ac n=1 text: 'test in tests/unit/test_db.py and test_pipeline.py'; `grep -c 'case=' tests/unit/test_db.py tests/unit/test_pipeline.py` -> 0 and 0 at c61e84f; AC1 evidence says 'tests/unit/test_multicase.py (3 passed ...)' but test_multicase.py now has 5 tests (grep -n '^def test_')",
   "why_it_matters": "The AC names where the proof lives. A reader following the card will not find it there. The evidence count is stale.",
   "fix": "Amend AC1 text to name tests/unit/test_multicase.py and update the evidence count to the current result, or add one case-scoped test to each named file.",
   "acceptance_test": "grep -n 'test_multicase' on the AC1 text; the evidence count matches `pytest tests/unit/test_multicase.py -q`."},
  {"severity": "minor",
   "title": "The F1 regression (unscoped _persist) is guarded only by test_api_routes, not test_multicase",
   "evidence": "artifacts/review-evidence/T-050/r2_mutate.py M1b: pipeline.py case=cid removed from update_item and apply_review; `pytest tests/unit/test_multicase.py -q` -> '5 passed'. The same mutant under tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids -> '1 failed'. test_multicase.py:15 ingests only; :26 runs only, with no ingest between.",
   "why_it_matters": "Round-1 F1 asked for an API-order test in test_multicase.py. Without it the multicase file would pass with the blocker reintroduced; the guard sits in a different file.",
   "fix": "Add a test to tests/unit/test_multicase.py that ingests case B after case A has run, then calls run_pipeline for case B (the API order), and asserts both cases finish with status ready.",
   "acceptance_test": "r2_mutate.py M1b (tests=tests/unit/test_multicase.py) reports at least one failure."}
 ],
 "whats_right": [
  "Round-1 blocker closed at the committed revision: app/backend/pipeline.py:148 and :152 pass case=cid; the API-order coexist test catches the unscoped mutant.",
  "The delete-isolation test (tests/unit/test_multicase.py:56-58) loops over every DB._CASE_TABLES table; dropping llm_calls is caught.",
  "Composite PK (case_id, id) on four tables and a rebuild path with no swallowed exceptions (db.py:198,246 re-raise) and a test for leftover files."
 ],
 "questions_for_chris": [
  "Is a silent delete of up to 24 h of in-flight cases on each schema bump acceptable for the demo and paralegal machines, or must the UI show a reset notice (finding 1)?"
 ]}
```
