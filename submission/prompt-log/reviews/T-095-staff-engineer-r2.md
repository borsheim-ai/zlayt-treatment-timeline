# T-095 r2 review: staff-engineer-reviewer

**Verdict: pass.** HEAD 31b7ceb carries the T-095 change. The 2fca530 revert is undone by 6feb2ff, and no later commit touches the card's files in a way that removes it. The v4 schema, the in-place v3 to v4 migration, the reclassify and rejudge writers, and rejudge's `_log` are all on HEAD, and the migration probe passes on HEAD (41 PASS, 0 FAIL).

All seven items from r1 (five minors, two nits) are still open. None is a blocker or a major, and you said they do not block, so the verdict is pass. I kept each one at its r1 severity and listed it in the JSON so it stays tracked. One item is outside T-095 and is not in the verdict: the sample CLI crashes on HEAD (see "Outside T-095 scope").

Scope pins: HEAD 31b7cebc96191cb54f91d8d68b46f651c71dfc2d, exported with `git archive 31b7ceb | tar -x` into the reviewer scratchpad (`t095r2_head`). Card commit 031a708. Restore commit 6feb2ff. The working tree was not used as evidence.

## Restore check (r1 F1, the blocker)

| Check | Command and result |
|---|---|
| Four card files byte-identical to the card commit | `git diff --stat 031a708 HEAD -- app/db/db.py app/db/schema.sql tests/unit/test_db.py tests/unit/test_trace.py` prints nothing |
| Three card files still carry the T-095 lines | `app/backend/reclassify.py:27` `AUDIT_ACTION = "reclassify"`; `app/backend/rejudge.py:57` `def _log` (writes via `DB.log_event`); `tests/unit/test_reclassify.py:319` asserts `["reclassify"]`. These files differ from 031a708 only by later cards (865b186 T-085, c8a9874 T-084), which I checked hunk by hunk: no removed line contains a T-095 identifier. |
| No commit after the restore touches the seven files | `git log --oneline 6feb2ff..HEAD -- <seven files>` prints nothing |
| Requested anchors on HEAD | SCHEMA_VERSION 4 at `app/db/db.py:33`; CHECK with `'reclassify','rejudge'` at `app/db/schema.sql:57`; v3 to v4 migration `app/db/db.py:60-62` and `:68-95` (`BEGIN IMMEDIATE` at `:73`, `COMMIT` at `:92`, `ROLLBACK` at `:94`); `log_event` with `AUDIT_ONLY_ACTIONS` guard at `app/db/db.py:240-243`; rejudge `_log` at `app/backend/rejudge.py:57`, called at `:80` and `:88` |

## Deterministic checks on HEAD

| Check | Result |
|---|---|
| `.venv/bin/python -m pytest -q tests/unit/test_db.py tests/unit/test_trace.py` in the archive | `83 passed in 5.74s` |
| `pytest -q tests/unit/test_reclassify.py` plus the four T-095 tests by name | `51 passed in 2.00s` |
| `pytest -q tests/unit` in the archive | `1 failed, 1398 passed, 2 skipped in 40.10s`. The failure is `tests/unit/test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s`, which is the CLI crash below, not T-095. The r1 failures at 7df65fb (test_trace x4, test_t075, test_t037 count) are gone except test_t037. |
| Migration probe `python3 -I artifacts/review-evidence/T-095/migration_probe.py <archive> <pre-T-095 schema> <scratch>` | 41 PASS, 0 FAIL, exit 0. Scenario 1: all tables identical, ids and order kept, exactly v03, v04, v20 converted, CHECK rejects `bogus`, `Reclassify`, `edits`, `''`. Scenario 2: mid-copy FK failure raises and leaves the file at user_version 3 with all rows and actions. |
| Mutants on scratch copies of HEAD, run with `artifacts/review-evidence/T-095/mutate.py` (M2 to M7) and a `sed -i '' '94d'` on `app/db/db.py` (M1) | M2 no transaction: 1 failed (`test_v3_migration_rolls_back_if_it_fails`), killed. M4 no rejudge row: 1 failed (`test_rejudge_writes_one_rejudge_event...`), killed. M5 no conversion: 1 failed (`test_v3_to_v4_migrates_in_place...`), killed. M6 reclassify writes `edit`: 1 failed (`test_reclassify.py::test_route`), killed. M7 `log_event` guard removed: 1 failed (`test_log_event_only_writes_audit_actions...`), killed. M1 no explicit ROLLBACK: `26 passed`, survives. M3 substring conversion rule: `130 passed`, survives. |

## Outside T-095 scope (not in the verdict)

`app/backend/pipeline.py:501` calls `language.case_check(language.annotate(IN.ingest(raw)["records"]))` before `raw` is assigned at `:506`. Running the sample CLI on the HEAD archive fails:

```
$ env -u ANTHROPIC_API_KEY -u LLM_BACKEND .venv/bin/python -m app.pipeline evals/golden/sample.txt; echo exit=$?
UnboundLocalError: cannot access local variable 'raw' where it is not associated with a value
exit=1
```

`git blame` puts line 501 in 865b186 (T-085, Spanish records). This breaks checklist item 20 (the sample CLI must run) and will fail the M3 gate. It belongs to the T-085 owner, not to T-095. I did not write it into this card's findings, so the T-095 verdict is not affected. The orchestrator should route it.

## Still open from r1

| r1 item | Status at HEAD 31b7ceb | Evidence |
|---|---|---|
| F2 minor, AC evidence count | OPEN. The card still says "full tests/unit 1350 passed (1 flaky spanish test passes on rerun)". HEAD gives 1398 passed, 1 failed, 2 skipped. The flake was not seen. | `python3 tools/board.py show T-095`; archive run above |
| F3 minor, rollback test does not prove the ROLLBACK | OPEN. Deleting `app/db/db.py:94` leaves `test_db.py` at 26 passed. The test reads through a fresh `sqlite3.connect` at `tests/unit/test_db.py:264`. | M1 above |
| F4 minor, conversion rule is substring, not key | OPEN. `app/db/db.py:86` is still `after.get("event") == "reclassify"`, so the fixture has no edit whose text contains the trigger word (grep of `tests/unit/test_db.py` for `reclassify this` and `event reclassify` prints nothing). The substring mutant M3 keeps 130 passed. | M3 above |
| F5 minor, reclassify bypasses `log_event` | OPEN. `app/backend/reclassify.py:88` is still a raw `INSERT INTO review_events`. | `git show HEAD:app/backend/reclassify.py \| sed -n 87,88p` |
| F6 minor, rejudge state and audit row in separate autocommits | OPEN. `app/backend/rejudge.py:79-80` and `:87-88` are still `DB.update_item` then `_log`. No `BEGIN`, `COMMIT` or `ROLLBACK` in `rejudge.py`. No test makes `log_event` raise. | `grep -n 'BEGIN\|COMMIT\|ROLLBACK' app/backend/rejudge.py` prints nothing |
| F7 nit, version read outside the migration transaction | OPEN. `app/db/db.py:60` reads user_version before `BEGIN IMMEDIATE` at `:73`. | `grep -n 'BEGIN IMMEDIATE' app/db/db.py` |
| F8 nit, orphan row gives no named error | OPEN. Scenario 2 still raises a bare `IntegrityError: FOREIGN KEY constraint failed`. | probe output; `grep -n 'IntegrityError\|class .*Error' app/db/db.py` prints nothing |

## Method notes

- `git worktree` is denied for reviewers, so HEAD was exported with `git archive` into the scratchpad. Nothing was written to the repo or its `.git`.
- Mutants ran in fresh copies of the archive. The `mutate.py` script was not changed.
- The migration probe is untracked under `artifacts/review-evidence/`, so it was run from its working-tree path against the archive tree (`sys.path` points at the archive).

## What is right

- HEAD equals 031a708 on `db.py`, `schema.sql`, `test_db.py` and `test_trace.py`, and no commit after 6feb2ff touches the seven card files.
- The probe on HEAD gives 41 PASS, 0 FAIL: all rows kept, exactly v03, v04 and v20 converted, mid-copy failure rolls back.
- Mutants M2, M4, M5, M6 and M7 each fail at least one test on HEAD, so the transaction, the rejudge audit row, the conversion, the reclassify action and the `log_event` guard are each pinned.

```json
{"card": "T-095", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 31b7cebc96191cb54f91d8d68b46f651c71dfc2d via git archive (card commit 031a708, restore 6feb2ff); no app URL (no UI exercised); migration probe artifacts/review-evidence/T-095/migration_probe.py on a v3 file from git show 031a708^:app/db/schema.sql; sample CLI python -m app.pipeline evals/golden/sample.txt on the HEAD archive",
 "exercised": [
  "git rev-parse HEAD; git log --oneline 031a708..HEAD and 6feb2ff..HEAD over the seven card files (empty after 6feb2ff)",
  "git diff --stat 031a708 HEAD -- app/db/db.py app/db/schema.sql tests/unit/test_db.py tests/unit/test_trace.py (empty); git diff 031a708 HEAD on reclassify.py, rejudge.py, test_reclassify.py (later cards only; removed lines checked for T-095 identifiers, none)",
  "git show HEAD:app/db/db.py | grep SCHEMA_VERSION/AUDIT_ONLY_ACTIONS/BEGIN IMMEDIATE/ROLLBACK/log_event; git show HEAD:app/db/schema.sql:57; git show HEAD:app/backend/reclassify.py:27; HEAD rejudge.py:57-88; HEAD test_db.py:226,255-266,270; test_trace.py:1004; test_reclassify.py:319",
  "git archive 31b7ceb | tar -x into the reviewer scratchpad t095r2_head (git worktree denied)",
  ".venv/bin/python -m pytest -q tests/unit/test_db.py tests/unit/test_trace.py in the archive: 83 passed",
  ".venv/bin/python -m pytest -q tests/unit/test_reclassify.py + the four named T-095 tests: 51 passed",
  ".venv/bin/python -m pytest -q tests/unit in the archive: 1 failed, 1398 passed, 2 skipped (failure test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s, UnboundLocalError at pipeline.py:501)",
  ".venv/bin/python -I artifacts/review-evidence/T-095/migration_probe.py <archive> <pre-T-095 schema> <scratch>: 41 PASS, 0 FAIL, exit 0",
  "Mutants in scratch copies of the archive: M1 (sed -i '' '94d' on db.py) 26 passed survives; M2 1 failed killed; M3 substring rule 130 passed survives; M4 1 failed killed; M5 1 failed killed; M6 1 failed killed; M7 1 failed killed (artifacts/review-evidence/T-095/mutate.py)",
  "env -u ANTHROPIC_API_KEY -u LLM_BACKEND .venv/bin/python -m app.pipeline evals/golden/sample.txt in the archive: exit 1, UnboundLocalError at app/backend/pipeline.py:501 (blame: 865b186)",
  "grep on HEAD for the r1 open items: rejudge.py BEGIN/COMMIT/ROLLBACK (none); reclassify.py:88 raw INSERT; db.py:86 substring-free rule; db.py:60 vs :73; no IntegrityError handling in db.py; no 'reclassify this' fixture in test_db.py",
  "python3 tools/board.py show T-095 (read-only): AC 1 evidence still reads 'full tests/unit 1350 passed'"
 ],
 "verdict": "pass",
 "scores": {"migration_keeps_rows": 5, "conversion_correct": 5, "check_rejects_unknown_actions": 5, "writers_own_action": 4, "rollback_on_failure": 4, "tests_bind_behaviour": 3, "evidence_reproducible": 2, "head_carries_change": 5},
 "findings": [
  {"severity": "minor", "title": "[still open, r1 F2] AC evidence count (1350 passed) is not reproducible; the card's full-suite claim is false at HEAD",
   "evidence": "board/cards/T-095.md ac[0].evidence: \"full tests/unit 1350 passed (1 flaky spanish test passes on rerun)\"; archive of 31b7ceb: .venv/bin/python -m pytest -q tests/unit -> \"1 failed, 1398 passed, 2 skipped in 40.10s\"; the failure is test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s (outside T-095)",
   "why_it_matters": "The AC cites a count the commit does not produce, and HEAD now fails one test in the suite the AC names. A reader cannot reproduce the claim. The unnamed flake is still unnamed.",
   "fix": "Replace the AC evidence line with the command, the count and the commit from a clean export. Name any flaky test and quarantine it with a reason, or remove the claim.",
   "acceptance_test": "The AC evidence names the command and count from a clean export of the final commit; two consecutive runs on that export give the same result."},
  {"severity": "minor", "title": "[still open, r1 F3] Rollback test passes with the explicit ROLLBACK removed",
   "evidence": "app/db/db.py:94 `conn.execute(\"ROLLBACK\")`. Scratch copy of 31b7ceb with line 94 deleted: .venv/bin/python -m pytest -q tests/unit/test_db.py -> \"26 passed in 0.38s\". Test at tests/unit/test_db.py:255-265 reads through a fresh `sqlite3.connect` (line 264).",
   "why_it_matters": "A leaked open transaction looks the same to this test as a real rollback, so the claim that a failed migration rolls back is not proven by the suite.",
   "fix": "After a failed _migrate_v3_to_v4 call on the migration connection, assert conn.in_transaction is False and user_version is 3. Add the FK orphan-row failure from the probe as a second failure mode.",
   "acceptance_test": "With db.py:94 deleted in a scratch copy, pytest tests/unit/test_db.py fails at least one test."},
  {"severity": "minor", "title": "[still open, r1 F4] One-shot v3 to v4 conversion matches a substring, not the top-level event key",
   "evidence": "app/db/db.py:86 `if isinstance(after, dict) and after.get(\"event\") == \"reclassify\":`. Scratch copy with that line replaced by `if \"reclassify\" in (r[\"after_json\"] or \"\"):`: pytest tests/unit/test_db.py tests/unit/test_reclassify.py tests/unit/test_trace.py -q -> \"130 passed\". grep for `reclassify this` and `event reclassify` in tests/unit/test_db.py: no match.",
   "why_it_matters": "A paralegal edit whose note contains the word reclassify would be rewritten from edit to reclassify by the migration. That corrupts the audit history and the migration cannot be reversed once it has run.",
   "fix": "Add to the test_v3_to_v4 fixture an edit row with after_json {\"review_status\": \"edited\", \"edited\": {\"note\": \"reclassify this\"}} and a non-JSON after containing the words event reclassify. Both must stay edit.",
   "acceptance_test": "With the substring rule applied in a scratch copy, pytest tests/unit/test_db.py fails at least one test."},
  {"severity": "minor", "title": "[still open, r1 F5] reclassify writes review_events with a raw INSERT, bypassing log_event and its audit-only guard",
   "evidence": "app/backend/reclassify.py:88 `conn.execute(\"INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)\",`. The guarded writer is app/db/db.py:240-243 (log_event, raises on actions outside AUDIT_ONLY_ACTIONS).",
   "why_it_matters": "There are two writers for review_events. The CHECK still limits the action set, so there is no data bug today, but the single-writer rule for audit rows is not enforced in code for reclassify.",
   "fix": "Replace _log in reclassify.py with DB.log_event(conn, case_id, item_id, \"reclassify\", before, after, now=t) and delete the raw SQL.",
   "acceptance_test": "grep -n 'INSERT INTO review_events' app/backend/reclassify.py prints nothing, and test_reclassify.py::test_route still asserts the reclassify action."},
  {"severity": "minor", "title": "[still open, r1 F6] rejudge state change and its audit row are separate autocommit statements",
   "evidence": "app/backend/rejudge.py:79-80 `DB.update_item(...)` then `_log(...)`; rejudge.py:87-88 the same pair. app/db/db.py:54 sets isolation_level=None, so each statement commits alone. grep -n 'BEGIN\\|COMMIT\\|ROLLBACK' app/backend/rejudge.py: no match. tests/unit/test_trace.py:1004 covers only the happy path.",
   "why_it_matters": "An exception or crash between the two statements leaves a changed judge state with no rejudge row, which breaks the audit-trail rule for that item.",
   "fix": "Wrap update_item and log_event in one BEGIN IMMEDIATE / COMMIT with ROLLBACK on error, as apply_review does at app/db/db.py:227-236.",
   "acceptance_test": "A test that makes DB.log_event raise during rejudge asserts the item's state, judge and review_status are unchanged afterwards."},
  {"severity": "nit", "title": "[still open, r1 F7] Migration version check runs outside the BEGIN IMMEDIATE transaction",
   "evidence": "app/db/db.py:60 reads `PRAGMA user_version` == 3 before `_migrate_v3_to_v4` runs; app/db/db.py:73 `conn.execute(\"BEGIN IMMEDIATE\")` is inside it.",
   "why_it_matters": "Two processes opening the same v3 file can both enter the migration. The second copies the same rows, so the result should match, but no test covers two openers.",
   "fix": "After BEGIN IMMEDIATE, re-read user_version and return if it is already 4.",
   "acceptance_test": "Optional: two connect() calls on one v3 file, run in sequence, leave the same rows and version 4."},
  {"severity": "nit", "title": "[still open, r1 F8] A v3 file with an orphan review_events row fails to open with a bare SQLite error",
   "evidence": "Probe scenario 2 on HEAD: \"raised: IntegrityError: FOREIGN KEY constraint failed\"; user_version stays 3. grep -n 'IntegrityError\\|class .*Error' app/db/db.py: no match.",
   "why_it_matters": "Failing loud is right and the file is not corrupted, but the operator is not told which review_events row or case is at fault, or what to do.",
   "fix": "Catch IntegrityError in the migration after the rollback and raise a named error that includes the offending review_events id.",
   "acceptance_test": "The orphan-row fixture raises a named error whose message includes the offending review_events id."}
 ],
 "whats_right": [
  "6feb2ff is a clean restore: HEAD equals 031a708 on db.py, schema.sql, test_db.py and test_trace.py, and no commit after 6feb2ff touches the seven card files.",
  "The probe on HEAD gives 41 PASS, 0 FAIL: every row kept, exactly v03, v04 and v20 converted, and a mid-copy FK failure leaves the v3 file untouched.",
  "Mutants M2, M4, M5, M6 and M7 each fail at least one test on HEAD, so the transaction, rejudge audit row, conversion, reclassify action and log_event guard are pinned."
 ],
 "questions_for_chris": [
  "Reviews are running on claude-haiku-5-5. CLAUDE.md section 6 lists Sonnet for engineering reviewers and Opus for judgment reviewers. Should this review count toward the M3 gate, or should the card be re-reviewed on Sonnet?"
 ]}
```
