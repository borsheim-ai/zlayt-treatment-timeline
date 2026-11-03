# T-062 staff-engineer review, round 2

Scope: commit c61e84f (parent d548ccd), touching app/db/db.py and tests/unit/test_db.py. DB-only card, no app URL, no sample case. Round 1 is reviews/T-062-staff-engineer.md (verdict fail, one blocker, one major, one minor).

Verdict: **pass**. All three round-1 findings are closed and each closure is backed by a mutant that the test suite now catches. The stale-file blocker is fixed: SCHEMA_VERSION is 3, and a real version-2 file is deleted and rebuilt on connect. I raise one new minor (nothing guards the "bump on every schema.sql change" rule) and one nit (the new test opens its schema path relative to the working directory). Neither is a spec violation.

Round-1 findings, status:
- Blocker, AC 1 version not bumped: closed. `app/db/db.py:32` reads `SCHEMA_VERSION = 3`. Mutant M1 (version reverted to 2) fails `test_old_v2_file_is_rebuilt_and_accepts_new_actions`.
- Major, rebuild test passes without the rebuild code: closed. The new test builds a real v2 file (old CHECK, `user_version=2`) and asserts the old row is gone. Mutant M2 (rebuild block disabled) fails it and `test_multicase.py::test_old_schema_file_is_deleted_and_rebuilt`.
- Minor, duplicate constant and dead DROP loop: closed. `grep -c '^SCHEMA_VERSION' app/db/db.py` prints 1, and the DROP loop is gone from `connect()`.

What I exercised:
- `.venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_multicase.py -q` gave `28 passed in 0.79s`. A second run gave `28 passed in 0.80s`.
- `.venv/bin/python -m pytest tests/unit -q` (working tree) gave one run with `1 failed, 830 passed` and then `834 passed`. The failure was `tests/unit/test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution`. That file has uncommitted edits from another agent, so it is outside this commit. I did not reproduce it on the two later runs, so it looks intermittent. Someone should check it.
- `grep -rn SCHEMA_VERSION app/db` gave `db.py:32` (`= 3`), `db.py:47`, `db.py:51`, `db.py:58`.
- `git show c61e84f -- app/db/db.py tests/unit/test_db.py` read in full.
- `sed -n 20,70p app/db/db.py` and `sed -n 185,215p tests/unit/test_db.py` read in full.
- `grep -n not_duplicate app/db/schema.sql` gave `schema.sql:57`; the CHECK lists `'not_duplicate','manual_entry'`.
- `git archive c61e84f app tests evals | tar -x -C /tmp/t062r2/base`, then the same two test files there: `28 passed`.
- Mutants run by `/tmp/t062r2/mutate_r2.py` on the clean export:
  - M1 `SCHEMA_VERSION` 3 to 2: `1 failed, 27 passed`; the new test fails.
  - M2 rebuild `if` replaced with `if False:`: `2 failed, 26 passed`; the new test and `test_old_schema_file_is_deleted_and_rebuilt` fail.
  - M3 `not_duplicate`,`manual_entry` removed from schema.sql CHECK: `2 failed, 26 passed`; `test_log_only_actions_not_duplicate_and_manual_entry` and the new test fail.
- Stale-file replay: copied `artifacts/review-evidence/T-062/stale.sqlite` to `/tmp/t062r2/stale_copy.sqlite` and ran `repro_stale_schema.py /tmp/t062r2/base new /tmp/t062r2/stale_copy.sqlite`. Output: `database schema version 2 != 3: old file deleted and rebuilt`, `new: user_version = 3`, `new: review_events CHECK has manual_entry: True`. The script then raised `TypeError` at line 27 because the rebuilt file has no entries. That is the intended result of the rebuild, and the script assumed the old file's rows.
- `cd /tmp && .venv/bin/python -m pytest /tmp/t062r2/base/tests/unit/test_db.py --rootdir=/tmp/t062r2/base`: the new test fails with `FileNotFoundError: 'app/db/schema.sql'` (test_db.py:192). `test_review_status_only_via_apply_review` also fails from `/tmp` (pre-existing, not in this commit).
- `python3 tools/board.py show T-062`: status `in_review`, commits `[5f8858f, c61e84f]`, AC 1 `done: true`.
- `ls /Users/arsis/zlayt-pm-project/new` gives `No such file or directory`. The stray probe file from round 1 is gone.
- `git show c61e84f | grep -nE '^\+.*(except|float\(|sleep\()'` printed nothing.

Findings:

1. Minor, version discipline is unguarded. `app/db/db.py:32` says "bump on EVERY schema.sql change", but nothing enforces it. The only test that touches `schema.sql` is the new fixture builder at `tests/unit/test_db.py:192`. Round 1's blocker was this exact miss, and it would recur on the next schema edit. This is not an AC violation, because AC 1 is met now. Fix: add a test that records a hash of `app/db/schema.sql` next to `SCHEMA_VERSION` and fails when the file changes without the version changing. Acceptance: edit `schema.sql` in a scratch copy without bumping, and the test goes red.

2. Nit, cwd-dependent fixture. `tests/unit/test_db.py:192` opens `"app/db/schema.sql"` relative to the working directory. Run from anywhere but the repo root, it fails with `FileNotFoundError` (repro above). The suite already needs the repo root, through the pre-existing writer-guard test, so this is cosmetic. Fix: `Path(__file__).resolve().parents[2] / "app/db/schema.sql"`.

Questions for Chris: none blocking. Round 2 deletes the old file (no move-aside). The code comment at `app/db/db.py:43-50` gives the reason (24 h purge, pasted text). I read that as intended, so I did not raise it.

```json
{"card": "T-062", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit c61e84f (parent d548ccd); app/db/db.py, tests/unit/test_db.py; no app URL (DB-only card); no sample case",
 "exercised": [
   ".venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_multicase.py -q -> 28 passed (two runs)",
   ".venv/bin/python -m pytest tests/unit -q (working tree) -> 1 failed, 830 passed, then 834 passed; the failure was test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution, a file with uncommitted edits outside c61e84f",
   "grep -rn SCHEMA_VERSION app/db -> db.py:32 (= 3), db.py:47, db.py:51, db.py:58; grep -c '^SCHEMA_VERSION' app/db/db.py -> 1",
   "git show c61e84f -- app/db/db.py tests/unit/test_db.py (full diff read); sed -n 20,70p app/db/db.py and sed -n 185,215p tests/unit/test_db.py read in full",
   "grep -n not_duplicate app/db/schema.sql -> schema.sql:57 CHECK lists 'not_duplicate','manual_entry'",
   "git archive c61e84f app tests evals | tar -x -C /tmp/t062r2/base; the same two test files there -> 28 passed",
   "/tmp/t062r2/mutate_r2.py on the clean export: M1 SCHEMA_VERSION 3->2 -> 1 failed (test_old_v2_file_is_rebuilt_and_accepts_new_actions); M2 rebuild if replaced with if False -> 2 failed (new test, test_old_schema_file_is_deleted_and_rebuilt); M3 new actions removed from schema CHECK -> 2 failed (log_only test, new test)",
   "artifacts/review-evidence/T-062/stale.sqlite copied to /tmp/t062r2/stale_copy.sqlite; repro_stale_schema.py /tmp/t062r2/base new /tmp/t062r2/stale_copy.sqlite -> 'database schema version 2 != 3: old file deleted and rebuilt', 'new: user_version = 3', 'new: review_events CHECK has manual_entry: True'; script then TypeError at line 27 because the rebuilt file is empty (expected)",
   "cd /tmp && .venv/bin/python -m pytest /tmp/t062r2/base/tests/unit/test_db.py --rootdir=/tmp/t062r2/base -> new test FileNotFoundError 'app/db/schema.sql' at test_db.py:192",
   "python3 tools/board.py show T-062 -> status in_review; commits [5f8858f, c61e84f]; AC 1 done true",
   "ls /Users/arsis/zlayt-pm-project/new -> No such file or directory (round-1 stray probe file is gone)",
   "git show c61e84f | grep -nE '^\\+.*(except|float\\(|sleep\\()' -> no output"
 ],
 "verdict": "pass",
 "scores": {"ac1_schema_bump_and_rebuild": 5, "tests_prove_ac1_claim": 5, "round1_blocker_closed": 5, "round1_major_closed": 5, "round1_minor_closed": 5, "version_discipline_guarded": 2, "log_only_events_before_after": 5, "log_only_status_never_accepted": 5},
 "findings": [
   {"severity": "minor",
    "title": "Version discipline ('bump on EVERY schema.sql change') is unguarded",
    "evidence": "app/db/db.py:32 comment 'bump on EVERY schema.sql change'; grep -rn schema.sql tests/ app/ tools/ --include=*.py returns only tests/unit/test_db.py:192 (the new fixture builder) and app/db/db.py:25 (_SCHEMA path); no test compares schema.sql to SCHEMA_VERSION",
    "why_it_matters": "Round 1's blocker was exactly this miss. The AC is met now, but the next schema.sql edit can repeat it with nothing to catch it.",
    "fix": "Add a unit test that records a hash of app/db/schema.sql alongside SCHEMA_VERSION and fails when the file changes without the version changing.",
    "acceptance_test": "In a scratch copy, edit app/db/schema.sql without bumping SCHEMA_VERSION; the new test fails. Restore the bump; it passes."},
   {"severity": "nit",
    "title": "New test opens schema.sql via a cwd-relative path",
    "evidence": "tests/unit/test_db.py:192: ddl = open(\"app/db/schema.sql\", encoding=\"utf-8\")...; cd /tmp && .venv/bin/python -m pytest /tmp/t062r2/base/tests/unit/test_db.py --rootdir=/tmp/t062r2/base -> FileNotFoundError: [Errno 2] No such file or directory: 'app/db/schema.sql'",
    "why_it_matters": "The test only runs from the repo root. The suite already has this dependence through a pre-existing test, so the impact is cosmetic.",
    "fix": "Anchor the path to the test file: Path(__file__).resolve().parents[2] / 'app/db/schema.sql'.",
    "acceptance_test": "Run pytest tests/unit/test_db.py from /tmp with --rootdir pointing at the repo; the new test passes."}
 ],
 "whats_right": [
   "SCHEMA_VERSION is now a single constant at app/db/db.py:32 = 3, and the duplicate and dead DROP loop from round 1 are removed.",
   "The v2 fixture asserts it really rejects the new action before connect() runs, so the test cannot pass on a non-v2 file (test_db.py:196-199).",
   "Stale-file handling deletes the file and logs one line without data text (db.py:47-52), consistent with the 24 h purge rule."
 ],
 "questions_for_chris": []}
```
