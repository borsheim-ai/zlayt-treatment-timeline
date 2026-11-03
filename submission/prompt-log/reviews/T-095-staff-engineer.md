# T-095 review: staff-engineer-reviewer

**Verdict: fail.** Commit 031a708 passes every check I ran against it: the v3 to v4 migration is one transaction, keeps every row, converts only the right rows, the CHECK rejects unknown actions, and the writers record their own action. But the change is not on HEAD. Commit 2fca530 (T-086/T-087, PDF hidden text and OCR) restored the pre-T-095 bytes of all seven files. HEAD 7df65fb still has them reverted, so the v4 schema, the migration, the reclassify action and the rejudge audit row are absent from the tree the milestone ships from. The card cannot be done until T-095 is back on HEAD.

Scope pins: card commit 031a708; HEAD 02ff244 (when first tested) and HEAD 7df65fb (current, tested again). The working tree was not used as evidence; other workers have uncommitted edits in it.

## Summary of checks

| Check | Result at 031a708 | Result at HEAD 7df65fb |
|---|---|---|
| v3 to v4 migration keeps every row, converts only top-level `event == reclassify` edits | 41 PASS, 0 FAIL (probe) | FAIL: user_version 3, v03/v04/v20 still `edit` |
| Converted rows correct (independent expected mapping) | PASS | FAIL (not migrated) |
| CHECK rejects unknown actions (`bogus`, `Reclassify`, `edits`, empty) | PASS | crash: CHECK has no reclassify/rejudge |
| reclassify and rejudge write their own action | PASS (tests and mutants) | FAIL: reclassify writes `edit`, rejudge writes no row |
| Mid-migration failure rolls back to v3 | PASS (FK failure at row 11, probe scenario 2) | not applicable |
| Full `pytest tests/unit -q` | 1187 passed (twice) | 6 failed, 1330 passed |

The card's AC claims "full tests/unit 1350 passed". The commit does not reproduce that number (see F2).

## Findings

**F1 (blocker): T-095 is not on HEAD. Commit 2fca530 silently reverted the seven files.** Details are in the JSON. The fix is a new commit that restores the 031a708 content of the seven files on top of HEAD, keeping the Spanish hunks in `rejudge.py` that landed after 031a708. Do not rewrite 2fca530; it belongs to other cards. The orchestrator lesson at `board/activity.jsonl:2183` names the cause (a shared index about 50 entries behind HEAD). I did not verify the cause beyond that lesson. The e2b4e3f commit restored T-083 after the same kind of loss, but nothing restored T-095.

**F2 (minor): AC evidence is not reproducible.** `pytest tests/unit -q` at 031a708 gives 1187 passed on both runs. The card says 1350. The card also says "1 flaky spanish test passes on rerun"; I saw no failure in any full run at 031a708 or 02ff244, so the flake is unproven. Cite the count from a clean export of the commit, and quarantine or name the flaky test if it exists.

**F3 (minor): the rollback test does not prove the explicit ROLLBACK.** Removing the `ROLLBACK` line at `app/db/db.py:94` (in the card commit) leaves `pytest tests/unit/test_db.py -q` at 26 passed. The test reads through a fresh connection, so a leaked open transaction looks the same as a rollback.

**F4 (minor): conversion rule is not pinned to the top-level key.** Replacing the rule at `app/db/db.py:86` with `"reclassify" in (r["after_json"] or "")` keeps all 101 tests in test_db, test_reclassify and test_trace green. A real paralegal note that contains the word "reclassify" would then be rewritten from `edit` to `reclassify` in a one-shot migration. The probe rows v10, v13 and v22 are the cases the test should pin.

**F5 (minor): reclassify bypasses the audit writer.** `app/backend/reclassify.py:76-77` does a raw INSERT into review_events, skipping `DB.log_event` and its `AUDIT_ONLY_ACTIONS` guard (`app/db/db.py:240-242`). The CHECK still limits the action set, so there is no data bug today, but there are now two writers for the table.

**F6 (minor): rejudge writes its audit row in a separate statement from the state change.** `app/backend/rejudge.py:79-80` and `:87-88` call `DB.update_item` and then `_log`. `connect()` uses `isolation_level=None` (`app/db/db.py:54`), so each runs in its own autocommit. A failure between them leaves a changed judge state with no `rejudge` row. Wrap both in one BEGIN/COMMIT, as `apply_review` does at `app/db/db.py:227-236`.

**F7 (nit): version check runs outside the migration transaction.** `app/db/db.py:60` reads user_version before `BEGIN IMMEDIATE` at line 73. Two processes can both enter the migration. The second rebuild copies the same rows, so the result should be the same, but this is by reading, not by test. Re-read user_version after BEGIN.

**F8 (nit): an orphan row makes the v3 file unopenable with no explanation.** Probe scenario 2 gives `IntegrityError: FOREIGN KEY constraint failed` on every open. The file stays at v3, which is correct. The operator gets no message saying which row or case is at fault. Raise a named error instead.

## Method notes

- The brief asked for `git worktree add`. The board-guard hook denies `git worktree` for reviewers. I used `git archive <sha> | tar -x` into scratch directories, which gives the same clean tree. Nothing was written to the repo or its `.git`.
- HEAD moved during the review (02ff244, then 7df65fb after commits 55300e9 to 7df65fb). Both are tested and cited by sha.
- The migration probe (`artifacts/review-evidence/T-095/migration_probe.py`) builds a real v3 file from `git show 031a708^:app/db/schema.sql`, with 22 mixed review_events rows and rows in all other tables. It runs in a separate process from the product code, and it expects actions from its own rule.
- Mutants (`artifacts/review-evidence/T-095/mutate.py`) ran in scratch copies only.

## What is right

- The migration runs in one `BEGIN IMMEDIATE` transaction and keeps every row. The probe shows identical non-event tables, identical review_events ids, order and payloads, and exactly v03, v04 and v20 converted.
- The CHECK rejects `bogus`, `Reclassify`, `edits` and the empty string. `log_event` refuses `accept`, and `apply_review` refuses `reclassify` and `rejudge`. No code in `app/` reads an event's `edit` action to make a decision, so the conversion changes no downstream result.
- Mutants M2 (no transaction), M4 (no rejudge audit row), M5 (no conversion), M6 (reclassify writes `edit`) and M7 (guard removed) each fail at least one test.

```json
{"card": "T-095", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "Card commit 031a708 (app/db/db.py, app/db/schema.sql, app/backend/reclassify.py, app/backend/rejudge.py, tests/unit/test_db.py, tests/unit/test_reclassify.py, tests/unit/test_trace.py) and HEAD (02ff244 at first run, 7df65fb now) via clean git archive exports. No app URL (no UI exercised). Synthetic probe case built in artifacts/review-evidence/T-095/migration_probe.py, not evals/golden/sample.txt.",
 "exercised": [
  "python3 tools/board.py show T-095 (status in_review, commits [031a708], AC 1 done with 1350 count)",
  "git show 031a708 -- <the seven files> (full diff read)",
  "git log --oneline 031a708..HEAD; git show --stat 2fca530 -- <seven files> (7 files, 7 insertions, 152 deletions); git diff --stat 031a708^ 2fca530 -- <seven files> (empty: exact revert); git diff --stat 031a708^ 7df65fb -- app/db/db.py app/db/schema.sql (empty: HEAD still pre-T-095)",
  "git show 7df65fb:app/backend/reclassify.py | grep ^AUDIT_ACTION (line 22: AUDIT_ACTION = \"edit\"); git show 7df65fb:app/backend/rejudge.py has no _log; git diff 031a708 7df65fb -- app/backend/rejudge.py",
  "board/activity.jsonl:2138-2139 (commit events for T-086 and T-087 at 2fca530) and :2183 (orchestrator lesson on the drifted shared index); git log -1 e2b4e3f and d3130e3 messages",
  "git archive 031a708, 02ff244 and 7df65fb into scratch dirs (git worktree denied by board-guard)",
  ".venv/bin/python -m pytest tests/unit/test_db.py tests/unit/test_reclassify.py tests/unit/test_trace.py -q: 031a708 101 passed; 02ff244 97 passed (T-095 tests absent)",
  ".venv/bin/python -m pytest tests/unit -q: 031a708 1187 passed (run twice); 02ff244 1224 passed; 7df65fb 6 failed, 1330 passed (test_trace x4, test_t075, test_t037; not diagnosed, outside T-095)",
  "python3 -I artifacts/review-evidence/T-095/migration_probe.py <tree> <pre-T-095 schema from git show 031a708^:app/db/schema.sql> <scratch>: 031a708 41 PASS 0 FAIL exit 0; 7df65fb 3 FAIL then IntegrityError at the CHECK acceptance step",
  "Mid-copy failure: orphan review_events row at position 11 (FK violation inside the copy loop); connect raised IntegrityError, file stayed user_version 3 with all 23 rows and original actions",
  "python3 -I artifacts/review-evidence/T-095/mutate.py <copy> <mutant>: M2 no transaction killed (test_v3_migration_rolls_back); M3 substring conversion survived (101 passed); M4 no rejudge log killed (test_rejudge_writes_one_rejudge_event); M5 no conversion killed; M6 reclassify writes edit killed (test_route); M7 log_event guard removed killed (test_log_event_only_writes); M1 no explicit ROLLBACK survived (test_db 26 passed)",
  "grep of app/ for event action consumers (db.py, present.py, trace.py, store.py, review.py): none reads action 'edit' for a decision; app/frontend/audit.js renders e.action verbatim"
 ],
 "verdict": "fail",
 "scores": {"migration_keeps_rows": 5, "conversion_correct": 5, "check_rejects_unknown_actions": 5, "writers_own_action": 4, "rollback_on_failure": 4, "tests_bind_behaviour": 3, "evidence_reproducible": 2, "head_carries_change": 1},
 "findings": [
  {"severity": "blocker", "title": "T-095 content is not on HEAD: commit 2fca530 reverted the seven files; HEAD 7df65fb has v3 schema, reclassify writes edit, rejudge writes no audit row",
   "evidence": "git diff --stat 031a708^ 2fca530 -- app/db/db.py app/db/schema.sql tests/unit/test_db.py app/backend/reclassify.py app/backend/rejudge.py tests/unit/test_reclassify.py tests/unit/test_trace.py prints nothing (2fca530 restores the pre-T-095 bytes); git show --stat 2fca530 -- <same files> prints 7 files changed, 7 insertions(+), 152 deletions(-); git diff --stat 031a708^ 7df65fb -- app/db/db.py app/db/schema.sql prints nothing; git show 7df65fb:app/db/db.py | grep ^SCHEMA_VERSION prints SCHEMA_VERSION = 3; git show 7df65fb:app/backend/reclassify.py line 22 is AUDIT_ACTION = \"edit\"; 7df65fb rejudge.py has no _log (card commit has it at rejudge.py:56, 79, 87); probe on wt of 7df65fb fails user_version 4, and dies with CHECK constraint failed: action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry'); board/activity.jsonl:2138-2139 records the 2fca530 commit for T-086 and T-087; 2fca530 message does not mention T-095",
   "why_it_matters": "The card is in_review with 031a708 as its only commit and its AC marked done, but the tree the milestone ships from does not carry the change. On HEAD the audit trail for rejudge is gone, reclassify is back to the stand-in action, the CHECK lacks the two actions, and the v3 to v4 migration is absent. Other commits went in on top of it, so the loss is silent. The board cannot tell that the card's commit is no longer in the product. Per D.2 this loses the rejudge audit facts from the branch and makes the must-have unusable on HEAD. The cause is likely a commit built from a stale shared index (see d3130e3 message and the orchestrator lesson at board/activity.jsonl:2183); I did not verify that beyond the lesson text.",
   "fix": "Add a new commit on HEAD that restores the 031a708 content of the seven files, keeping the Spanish hunks in rejudge.py that landed after 031a708 (7df65fb). Do not rewrite 2fca530. Re-run the probe and the unit suite on a clean export of the new HEAD. Keep T-095 in_review until HEAD carries the change.",
   "acceptance_test": "On a clean git archive of the new HEAD: (a) git diff --stat 031a708 HEAD -- app/db/db.py app/db/schema.sql tests/unit/test_db.py app/backend/reclassify.py app/backend/rejudge.py tests/unit/test_reclassify.py tests/unit/test_trace.py shows no removals of T-095 lines; (b) python3 -I artifacts/review-evidence/T-095/migration_probe.py prints TOTAL FAILS: 0; (c) pytest tests/unit/test_db.py::test_v3_to_v4_migrates_in_place_keeping_rows_and_converts_reclassify_edits tests/unit/test_trace.py::test_rejudge_writes_one_rejudge_event_per_asked_item_and_leaves_review_status_alone -q passes."},
  {"severity": "minor", "title": "AC evidence count (1350 passed) and the flaky spanish test claim are not reproducible from the commit",
   "evidence": "cd <clean export of 031a708> && .venv/bin/python -m pytest tests/unit -q -> \"1187 passed in 33.27s\" (run twice); card AC text: \"full tests/unit 1350 passed (1 flaky spanish test passes on rerun)\"; no failure seen in any full run at 031a708 or 02ff244 (1224 passed)",
   "why_it_matters": "The AC evidence cites a count the commit cannot produce, so the evidence came from a different tree (the dirty working tree with other workers' edits). A reader cannot reproduce the claim. An unnamed flaky test is a determinism problem that nobody can find.",
   "fix": "Re-run the full suite on a clean export of the fixed commit and quote the count and command. If a flaky test exists, name it and quarantine it with a reason, or remove the claim.",
   "acceptance_test": "The AC evidence line names the command and the count from a clean export; two consecutive full runs on that export give the same count with no failures."},
  {"severity": "minor", "title": "Rollback test does not prove the explicit ROLLBACK; removing it leaves the suite green",
   "evidence": "Mutant: delete the line conn.execute(\"ROLLBACK\") at app/db/db.py:94 (card commit) in a scratch copy; .venv/bin/python -m pytest tests/unit/test_db.py -q -> \"26 passed\" (mutant M1 survives). The test at tests/unit/test_db.py:255 reads through a fresh sqlite3.connect after the exception.",
   "why_it_matters": "A leaked open transaction would look the same to this test as a real rollback. The persona's rule is that a rollback claim needs a test that fails when the rollback is removed. In this code the leak keeps a write lock until the connection is garbage-collected, which is not something the test checks.",
   "fix": "Call DB._migrate_v3_to_v4(conn, schema) directly on a connection in the test, then assert conn.in_transaction is False and user_version is 3. Keep the monkeypatch test, and add the orphan-row (FK) failure from the probe as a second failure mode.",
   "acceptance_test": "With the ROLLBACK line deleted in a scratch copy, pytest tests/unit/test_db.py fails at least one test."},
  {"severity": "minor", "title": "Conversion rule is not pinned to the top-level event key; a substring match passes every test",
   "evidence": "app/db/db.py:86 (card commit): if isinstance(after, dict) and after.get(\"event\") == \"reclassify\":. Mutant replacing it with if \"reclassify\" in (r[\"after_json\"] or \"\"): keeps 101 passed in test_db, test_reclassify and test_trace (mutant M3). The probe rows v10 (not json: event reclassify), v13 (nested event), and v22 (wrapped edited note) are the cases the substring rule gets wrong.",
   "why_it_matters": "Real apply_review edits store after_json as {\"review_status\": ..., \"edited\": {...}} (app/db/db.py:226). A paralegal note or summary containing the word reclassify would be rewritten from edit to reclassify by the one-shot migration. That corrupts the audit history silently and cannot be undone once the migration runs.",
   "fix": "Add to the test_v3_to_v4 fixture: an edit row whose after_json is {\"review_status\": \"edited\", \"edited\": {\"note\": \"reclassify this\"}} and a non-JSON after containing the words event reclassify; both must stay edit.",
   "acceptance_test": "With the substring mutant applied in a scratch copy, pytest tests/unit/test_db.py fails at least one test."},
  {"severity": "minor", "title": "reclassify writes review_events with a raw INSERT, bypassing DB.log_event and its audit-only guard",
   "evidence": "app/backend/reclassify.py:76-77 (card commit): conn.execute(\"INSERT INTO review_events (...) VALUES (?,?,?,?,?,?,?)\", (DB._tok(\"v\"), case_id, item_id, AUDIT_ACTION, DB._enc(before), DB._enc(after), t)). The helper that the schema comment and db.py:240-247 name as the audit-only writer is log_event, which enforces AUDIT_ONLY_ACTIONS.",
   "why_it_matters": "There are now two ways to write review_events for the same action. The CHECK still limits the action set, so there is no data bug today, but the single-writer rule for audit rows is no longer enforced in code for reclassify.",
   "fix": "Replace _log in reclassify.py with DB.log_event(conn, case_id, item_id, \"reclassify\", before, after, now=t) and delete the raw SQL.",
   "acceptance_test": "grep -n \"INSERT INTO review_events\" app/backend/reclassify.py prints nothing, and test_route in tests/unit/test_reclassify.py still asserts the reclassify action."},
  {"severity": "minor", "title": "rejudge state change and its audit row are two autocommit statements; a failure between them leaves no audit row",
   "evidence": "app/backend/rejudge.py:79-80 (unavailable path: DB.update_item then _log) and rejudge.py:87-88 (answer path: DB.update_item then _log). app/db/db.py:54 sets isolation_level=None, so each statement commits on its own. Compare apply_review, which wraps its update and insert in BEGIN/COMMIT at app/db/db.py:227-236.",
   "why_it_matters": "A crash or an exception from log_event between the two statements leaves a changed judge verdict and state with no rejudge row. The test at tests/unit/test_trace.py:1004 only checks the happy path, so this is not caught. The persona's audit-trail rule requires the record for every item.",
   "fix": "Wrap update_item and log_event in one BEGIN/COMMIT with a ROLLBACK on error, or write the audit row first in the same transaction.",
   "acceptance_test": "A test that monkeypatches DB.log_event to raise during rejudge asserts the item's state and judge are unchanged afterwards."},
  {"severity": "nit", "title": "Migration version check runs outside the BEGIN IMMEDIATE transaction",
   "evidence": "app/db/db.py:60 reads PRAGMA user_version == 3 before app/db/db.py:73 BEGIN IMMEDIATE.",
   "why_it_matters": "Two processes opening the same v3 file can both enter the migration. The second rebuild runs after the first commits and copies the same rows, so the result should match, but no test covers two openers.",
   "fix": "Re-read user_version inside the transaction after BEGIN IMMEDIATE and return if it is already 4.",
   "acceptance_test": "Optional: two connect() calls on one v3 file, run in sequence, leave the same rows and version 4."},
  {"severity": "nit", "title": "A v3 file with an orphan review_events row can never be opened, and the error does not say why",
   "evidence": "Probe scenario 2 on 031a708: connect raises \"IntegrityError: FOREIGN KEY constraint failed\" and the file stays user_version 3 (the rollback itself is correct).",
   "why_it_matters": "Failing loud is right, and the file is not corrupted. But the operator gets a bare SQLite error with no table, row or case named, and no path forward other than manual deletion. The v1/v2 path deletes automatically, so the two paths behave differently.",
   "fix": "Catch the IntegrityError in _migrate_v3_to_v4 (after the rollback) and raise a named error that says which review_events row or case failed, and what to do.",
   "acceptance_test": "The orphan-row fixture raises a named error whose message includes the offending review_events id."}
 ],
 "whats_right": [
  "The migration runs in one BEGIN IMMEDIATE transaction and keeps every row: 22 mixed review_events rows plus all other tables are identical after migration, with only v03, v04 and v20 converted (probe, 41 PASS at 031a708).",
  "The CHECK rejects bogus, Reclassify, edits and the empty string; log_event refuses accept and apply_review refuses reclassify and rejudge, and no code in app/ reads an event's edit action to make a decision.",
  "A mid-copy FK failure (orphan row at position 11) rolls back to user_version 3 with all 23 rows, the original actions and the v3 CHECK intact."
 ],
 "questions_for_chris": [
  "Restoring T-095 as a new commit on top of HEAD is non-destructive; rewriting 2fca530 would change other cards' history. I recommend the new commit and did not change history. Do you agree?"
 ]}
```
