# T-062 staff-engineer review

Scope: commit 5f8858f (parent 5f8858f^) touching app/db/db.py, app/db/schema.sql, tests/unit/test_db.py. DB-only card, no app URL, no sample case.

Verdict: **fail**. AC 1 says "schema version bumped so old files rebuild". The version was not bumped (it is still 2), so a review_events file written before this commit keeps the old CHECK and rejects the two new actions with an IntegrityError. The AC test passes without the rebuild code it names, so it does not prove the claim.

What holds: the log-only actions write one event row with before/after and never change review_status. The AST writer guard is unchanged and passes.

Probe housekeeping (not a finding on the artifact): one probe run with swapped arguments created an untracked SQLite file at `/Users/arsis/zlayt-pm-project/new` (94208 bytes, 20:15). The board-guard hook blocked my `rm` of it, so I did not remove it. It needs deleting by the orchestrator or Chris. It is not part of the commit.

Evidence files (under the allowed path): `artifacts/review-evidence/T-062/repro_stale_schema.py`, `artifacts/review-evidence/T-062/mutate.py`, `artifacts/review-evidence/T-062/parent/` (git archive of 5f8858f^ app and tests), `artifacts/review-evidence/T-062/mut/`.

```json
{"card": "T-062", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 5f8858f (parent 5f8858f^); app/db/db.py, app/db/schema.sql, tests/unit/test_db.py; no app URL (DB-only card); no sample case",
 "exercised": [
   "python3 tools/board.py show T-062 -> status in_review; AC 1 done=true, evidence cites 23 passed and SCHEMA_VERSION=2",
   ".venv/bin/python -m pytest tests/unit/test_db.py -q 2>&1 | tail -2 -> '23 passed in 0.27s'",
   ".venv/bin/python -m pytest tests/unit/test_db.py -v -> PASSED for test_log_only_actions_not_duplicate_and_manual_entry, test_old_schema_file_is_rebuilt, test_review_status_only_via_apply_review, and all 4 test_writer_guard_catches_rogue_forms params",
   "git show 5f8858f -- app/db/db.py app/db/schema.sql tests/unit/test_db.py (full diff read)",
   "git show 5f8858f^:app/db/db.py | grep -n 'SCHEMA_VERSION\\|user_version' -> 31:SCHEMA_VERSION = 2 ; 58:PRAGMA user_version (version was already 2 before the commit)",
   "git archive 5f8858f^ app tests | tar -x -C artifacts/review-evidence/T-062/parent (parent tree for stale-file probe)",
   "artifacts/review-evidence/T-062/repro_stale_schema.py: old stage on parent -> 'user_version = 2', 'CHECK has manual_entry: False'; new stage on the stale file -> 'manual_entry RAISED IntegrityError - CHECK constraint failed: action IN (accept,edit,dismiss,reset,confirm_date,keep_my_wording)'; control (file written by HEAD) -> 'manual_entry OK; events: [accept, manual_entry]'",
   "artifacts/review-evidence/T-062/mutate.py (scratch copies, repo unmodified): m1 delete DROP loop db.py:58-61 -> 23 passed; m2 manual_entry->accepted -> 1 failed (log_only test); m3 not_duplicate->dismissed -> 1 failed; m4 schema CHECK without new actions -> 2 failed (log_only, old_schema_rebuilt); m5 no event row for manual_entry -> 1 failed",
   "grep for SCHEMA_VERSION, user_version, schema version, log-only in docs/ and memory/ -> no matches (no doc states the bump rule)",
   "Read app/db/db.py, app/db/schema.sql, tests/unit/test_db.py in full with line numbers"
 ],
 "verdict": "fail",
 "scores": {"ac1_schema_bump_and_rebuild": 1, "log_only_events_before_after": 5, "log_only_status_never_accepted": 5, "ast_writer_guard_intact": 5, "tests_prove_ac1_claim": 2},
 "findings": [
   {"severity": "blocker",
    "title": "AC 1 'schema version bumped so old files rebuild' is not met; version-2 files keep the old CHECK and reject the new actions",
    "evidence": "app/db/db.py:25 and app/db/db.py:33 both read 'SCHEMA_VERSION = 2'; git show 5f8858f^:app/db/db.py shows 'SCHEMA_VERSION = 2' already at line 31, so the value did not change. app/db/schema.sql:57 adds 'not_duplicate','manual_entry' to the review_events CHECK with no version bump. Repro (from repo root): .venv/bin/python artifacts/review-evidence/T-062/repro_stale_schema.py $PWD/artifacts/review-evidence/T-062/parent old $PWD/artifacts/review-evidence/T-062/stale.sqlite, then .venv/bin/python artifacts/review-evidence/T-062/repro_stale_schema.py $PWD new $PWD/artifacts/review-evidence/T-062/stale.sqlite prints 'new: user_version = 2', 'new: review_events CHECK has manual_entry: False', 'new: manual_entry RAISED IntegrityError - CHECK constraint failed: action IN (...)'. Control: a file written by HEAD code accepts manual_entry.",
    "why_it_matters": "The AC names the bump as the mechanism that makes old files rebuild. Without it, connect() (db.py:47 and db.py:58) treats a pre-T-062 file as current and does not move it aside. Any review action of the new kind on that file raises IntegrityError. The failure is loud and the UPDATE and INSERT share one transaction (db.py:197-206), so nothing is half-written, but the AC is not met and the card evidence ('SCHEMA_VERSION=2 via PRAGMA user_version') describes an unchanged value. The schema.sql comment at db.py:25 says 'bump on any schema.sql change', which this commit breaks.",
    "fix": "Set the one SCHEMA_VERSION to 3 (see finding 3 for the duplicate). The existing move-aside at db.py:47-53 then rebuilds any version-2 file.",
    "acceptance_test": "New test: write a file with PRAGMA user_version=2 and the pre-T-062 review_events CHECK (literal CREATE TABLE is enough), call DB.connect(path), assert a '<path>.old-*' sibling exists and DB.apply_review(conn, iid, 'manual_entry', now=2) succeeds with events ['manual_entry']. Red on 5f8858f, green after the bump. Re-run repro_stale_schema.py new step: must print 'manual_entry OK'."},
   {"severity": "major",
    "title": "test_old_schema_file_is_rebuilt does not exercise the T-062 rebuild code; the AC test passes without it",
    "evidence": "tests/unit/test_db.py:188-195 creates a file with no user_version (0), so the pre-existing move-aside at app/db/db.py:47-53 handles it and the new DROP loop at db.py:58-61 is never the cause. Mutant m1 (DROP loop deleted, scratch copy artifacts/review-evidence/T-062/mut/m1_no_drop_loop) gives '.venv/bin/python -m pytest tests/unit/test_db.py -q' -> '23 passed in 0.31s'. Repro: .venv/bin/python artifacts/review-evidence/T-062/mutate.py prints 'm1_no_drop_loop: 23 passed in 0.31s'.",
    "why_it_matters": "The AC 1 evidence is the only proof of the rebuild claim, and it passes with the code it names removed. Per persona 13 and section 7.3, a test that cannot fail on the claimed behaviour does not prove it.",
    "fix": "Make the test use a version-2 file with the old CHECK (see finding 1) so the version comparison is what is under test. Assert the move-aside sibling exists.",
    "acceptance_test": "Mutant A: SCHEMA_VERSION reverted to 2 -> the new test fails. Mutant B: the bump is kept but db.py:47-53 deleted -> the new test fails. Run via artifacts/review-evidence/T-062/mutate.py with those two mutants added."},
   {"severity": "minor",
    "title": "Duplicate SCHEMA_VERSION definition and an effectively dead DROP loop",
    "evidence": "app/db/db.py:25 'SCHEMA_VERSION = 2   # bump on any schema.sql change; ...' (added by this commit) and app/db/db.py:33 'SCHEMA_VERSION = 2  # 1 = global ids (pre T-050); 2 = (case_id, id) keys' (pre-existing). The DROP loop at db.py:58-61 runs only when user_version != 2. Any file that has tables and a mismatched version is already moved aside at db.py:47-53, so the loop sees an empty file. I could not find an input where it drops anything the move-aside has not already moved.",
    "why_it_matters": "Two constants with one name invite a half-edit: bump one and the other wins at import. The dead loop reads like a second rebuild mechanism and is part of why the missing bump in finding 1 was not noticed.",
    "fix": "Keep one SCHEMA_VERSION definition. Delete the DROP loop (db.py:58-61), since the move-aside already covers the case.",
    "acceptance_test": "grep -c '^SCHEMA_VERSION' app/db/db.py prints 1. The finding 2 test stays red when the version is reverted."}
 ],
 "whats_right": [
   "Log-only actions map to None in ACTIONS (db.py:18-20) and apply_review keeps the current status (db.py:192); mutants m2 and m3 that change the status are caught by test_log_only_actions_not_duplicate_and_manual_entry.",
   "Each log-only action writes a review_events row with before and after in the same transaction (db.py:197-203); test_db.py:178-186 asserts the pair, and mutant m5 that drops the row is caught.",
   "The AST writer guard (test_db.py:123-166) is unchanged and passes, and the new SQL added by this commit (DROP TABLE, PRAGMA) does not match its regex."
 ],
 "questions_for_chris": ["Do any review databases survive a deploy on the demo or dev machine (retention is 24 h, db.py:16)? This affects how urgent finding 1 is, not whether it violates AC 1."]}
```
