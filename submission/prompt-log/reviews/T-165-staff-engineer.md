# T-165 staff-engineer review (commit 312efe6)

Verdict: **fail**. One blocker: a re-run that extracts a hand-entered record again deletes the paralegal's pending entry with no note. The contract says a re-run never erases earlier work. The T-165 hand-entry protection covers only the branch where the record stays down.

Scope: commit 312efe6 (HEAD at review time), read on a `git archive 312efe6` copy. The working tree is dirty with other agents' files and was not used. Golden sample and synthetic two-record notes only.

What holds (checked by running the code):
- A first run with the extract step down on one record (1 of 9), eight of nine, or all nine reads `failed` / `run_partial`, names the records, and the export gate lists `RUN_FAILED`. Probe A, B.
- A run where every record extracted reads `ready`, `error: null`, no warnings. Probe C.
- A record entered by hand before the run, or after a failed run, gives an `ENTERED_BY_HAND` warning and no failure. Probe D, E.
- A re-run where the record is still down keeps the pending hand-entered entry `e1_m`. Probe F. On the parent `ea988f8` the same probe deletes `e1_m`, so the fix is real for this branch.

Blocker, detail: scenario G. A hand-entered record (`e1_m`, pending) is entered, then the re-run extracts record 1 successfully. The final entries are `e1` (AI, pending) only; `e1_m` is gone, the case reads `ready`, and no warning is shown. The sweep at `app/backend/pipeline.py:368-376` skips the delete only when `live_rids` does not cover the record; once the AI writes a live `e1`, the `DELETE` at line 376 removes the paralegal's row. `memory/contracts/api.md:129` says "a re-run never erases earlier work", and the T-165 text in the same line protects a hand-entered entry only "whose extract fails again". The same G probe on `ea988f8` also loses `e1_m`, so this was already present and T-165 did not close it. No test covers it: `tests/unit/test_t165_partial_extract.py:154` (`test_a_rerun_that_extracts_the_record_clears_the_failure`) has no hand entry.

Minor, detail: scenario H. After the paralegal dismisses `e1_m`, the case reads `ready`, the tray is empty, the failure does not come back, and the `ENTERED_BY_HAND` warning still says "you entered it by hand". No test covers dismissal.

Minor, detail: the four pins named in the brief are justified (see the JSON). A fifth changed assertion, `tests/unit/test_t139_charge_text.py` `counts.entries` 3 to 4, counts the hand entry as an entry; it is a workaround for the T-168 fixture gap and should be reverted with T-168.

Pin justification (each one checked against the api.md T-165 text):
1. `test_t161_first_run_stage_down.py::test_first_run_with_extract_down_and_no_entries...`: exact error now carries `records` and `extract_only` and names records 1 to 9. Justified by the AC.
2. `test_t161_first_run_stage_down.py::test_first_run_with_extract_down_for_some_records...`: `ready` flipped to `failed`, `records == [1]`. Justified by "any record whose extract step failed makes the case run_partial".
3. `test_t146_r3_decided_items_never_lowered.py::test_rerun_with_nothing_to_keep...`: exact error gains `records` and `extract_only` and the names. Justified by the AC.
4. `test_t146_r3_decided_items_never_lowered.py::test_nothing_to_keep_and_something_kept...`: message gains "No entry was made for record 4." Justified by the AC.

Mutation spot-checks on scratch copies of the archive (mutant text is in the commands below):
- m1: remove the hand-entry skip at pipeline.py:372. Targeted tests: 2 fail (`test_a_rerun_with_the_record_still_down_keeps_the_hand_entry...`, `test_a_record_entered_by_hand_before_the_run...`). Killed.
- m2: drop `PL.refresh_extract_error` at review.py:678. Targeted tests: 2 fail. Killed.
- m3: `hand_entered_warnings` returns `[]`. Targeted tests: 4 fail. Killed.

Commands and outputs are saved in `artifacts/review-evidence/T-165/` (`probe_t165.py`, `probe_out.txt`, `mut.py`).

```json
{"card": "T-165", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 312efe6 (HEAD at review time) via git archive copy at artifacts-free scratch dir; files: app/backend/pipeline.py, generator.py, present.py, review.py; tests/unit/test_t165_partial_extract.py, _hand_entry.py, test_t161_first_run_stage_down.py, test_t146_r3_decided_items_never_lowered.py, test_t139_charge_text.py, test_api_routes.py, test_case_list.py, test_t114_rates_and_demo_judges.py; contract memory/contracts/api.md:129; synthetic golden sample and two-record synthetic note; no app URL exercised (in-process only)",
 "exercised": [
  "python3 tools/board.py show T-165 (card read: status in_review, ac 1 done, handoff)",
  "reviews/T-161-staff-engineer-r2.md read in full",
  "git show 312efe6 --stat and git diff 312efe6^ 312efe6 for all app and test files in the commit",
  "git archive 312efe6 | tar -x into scratchpad t165-review/head; file list diffed against git ls-tree -r 312efe6 (identical, 1213 fixture files included)",
  "cd head && .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -> 5058 passed, 8 skipped, exit 0 (276 s). Worker handoff quoted 4961 on archive plus hunks; not reconciled, does not change the verdict",
  "artifacts/review-evidence/T-165/probe_t165.py run on HEAD archive, scenarios A-H -> artifacts/review-evidence/T-165/probe_out.txt (status, error, export_blockers via trace.export_blockers, warnings, tray, entries)",
  "same probe scenario F and G on git archive ea988f8 (parent): G deletes e1_m on the parent too (pre-existing); F deletes e1_m on the parent (fixed by T-165)",
  "mutant m1 (pipeline.py:372 continue -> pass) on scratch copy: t165 + t161 + t146_r3 files -> 2 failed, 85 passed",
  "mutant m2 (review.py:678 PL.refresh_extract_error -> pass): 2 failed, 85 passed",
  "mutant m3 (generator.py hand_entered_warnings return [] ): 4 failed, 83 passed",
  "grep of the T-165 diff for except, float(, sleep(, network or key strings: none added (only the word 'retry' in a message string)",
  "grep -rn dismiss on the T-165 test file: no test covers a dismissed hand entry",
  "grep allow_failed and export_blockers call sites in head/app/backend (export gate is trace.export_blockers, per api.md:663 and export.py:836)"
 ],
 "verdict": "fail",
 "scores": {"first_run_partial_names_records": 4, "all_extracted_stays_ready": 5, "hand_entry_warning_not_failure": 4, "rerun_keeps_pending_hand_entry": 2, "dismiss_and_recover_states": 2, "pins_justified": 4, "test_strength_mutants": 4},
 "findings": [
  {"severity": "blocker",
   "title": "A re-run that extracts a hand-entered record again silently deletes the paralegal's pending entry",
   "evidence": "Probe G (artifacts/review-evidence/T-165/probe_out.txt, block '== G'): after hand entry on record 1 and a re-run with record 1 extracting, entries are e1 (AI, pending, verified) only; e1_m is gone; status ready, warnings []. Code: app/backend/pipeline.py:368 live_rids; :372 continue applies only when the record has no live row; :376 DELETE FROM entries ... review_status='pending' removes e1_m. Contract: memory/contracts/api.md:129 'a re-run never erases earlier work'; T-165 text in the same line protects the hand entry only 'whose extract fails again'. Pre-existing: the same probe on git archive ea988f8 also loses e1_m. Repro: git archive 312efe6 | tar -x -C D; cd D && PYTHONPATH=$PWD <repo>/.venv/bin/python <repo>/artifacts/review-evidence/T-165/probe_t165.py G",
   "why_it_matters": "The paralegal's typed summary and quote are removed by a re-run with no note and no warning, while the case reads ready. The contract states that a re-run never erases earlier work. The card that claims to protect hand-entered entries leaves this path open, and the brief's check 'a re-run keeps a pending hand-entered entry' fails for this case.",
   "fix": "Keep a pending hand-entered entry on every re-run, not only while its record has no live AI row. When the AI also now has an entry for that record, keep both and set a rerun_note on the hand entry (for example 'the AI step now has an entry for record 1; your entry was kept, it is pending'). Remove the live_rids condition at pipeline.py:372 for entered_by=reviewer rows.",
   "acceptance_test": "tests/unit/test_t165_partial_extract.py: run with record 1 down, hand-enter record 1, re-run with record 1 extracting. Assert e1_m is still in DB.list_items(conn, cid, 'entry') with review_status 'pending', its ladder.rerun_note is set, and the case status is ready. On HEAD this test fails (e1_m is absent)."},
  {"severity": "minor",
   "title": "Dismissing a hand-entered entry leaves a stale ENTERED_BY_HAND warning and the failure never returns",
   "evidence": "Probe H (probe_out.txt, block '== H'): after RV.apply_review(conn, cid, 'e1_m', {'action': 'dismiss'}), e1_m has review_status 'dismissed', case status ready, error null, tray [], warnings [('ENTERED_BY_HAND', 1, 'e1')]. generator.py:205-207 entered_by_hand counts any non-rejected entry, dismissed included. No test in tests/unit/test_t165_partial_extract.py mentions dismiss.",
   "why_it_matters": "The warning tells the paralegal 'you entered it by hand' about an entry they dismissed. Record 1 has no usable entry, and the case no longer shows the extract failure. The dismissed entry is still visible in the entry list, so this is not silent, but the case-level message is wrong.",
   "fix": "Exclude dismissed hand entries from entered_by_hand, or word the warning by state. Decide with Chris whether dismissing the hand entry re-opens the extract failure (see questions_for_chris).",
   "acceptance_test": "Hand-enter record 1 after a failed run, then dismiss e1_m. Assert the chosen state: either RUN_FAILED and record 1 named again, or no ENTERED_BY_HAND warning. Pin the chosen one."},
  {"severity": "minor",
   "title": "Fifth changed assertion outside the named pins: test_t139 counts.entries 3 to 4 counts a hand entry as an entry",
   "evidence": "tests/unit/test_t139_charge_text.py diff: '-    assert j[\"counts\"][\"entries\"] == 3' / '+    assert j[\"counts\"][\"entries\"] == 4                      # e1, e5, e6 and the hand-entered record 3 (wait_ready)'. Caused by the lib01 fixture gap (T-168) worked around with enter_failed_records_by_hand (tests/unit/_hand_entry.py).",
   "why_it_matters": "An assertion about the AI-made timeline now counts a paralegal entry. It is documented in the comment and is a test-data workaround, but it will need reverting when T-168 lands, and it can hide a real AI regression on lib01.",
   "fix": "Keep the workaround, but assert the AI-made count separately from the hand entry (for example count entries whose ladder.entered_by is not 'reviewer' equals 3, and the hand entry id is present). Revert with T-168.",
   "acceptance_test": "test_t139 lib01 assertion: AI-made entries == 3 and the hand entry e3_m present; mutant that drops one AI entry fails the test."}
 ],
 "whats_right": [
  "A first run with the extract step down on one, eight or all nine records reads failed / run_partial, names the records, and the export gate lists RUN_FAILED; all-extracted stays ready with error null (probe A, B, C)",
  "A hand entry before the run or after a failed run gives an ENTERED_BY_HAND warning, not a failure; a still-down re-run keeps the pending hand entry, where the parent ea988f8 deleted it (probe D, E, F vs parent)",
  "The four pins in tests/unit/test_t161_first_run_stage_down.py and tests/unit/test_t146_r3_decided_items_never_lowered.py each change one assertion to the behaviour the api.md T-165 text names; mutants m1, m2, m3 are killed by the T-165 file"
 ],
 "questions_for_chris": [
  "When a record's extract failed and the paralegal hand-enters it, then dismisses that entry: should the extract failure (RUN_FAILED and the tray placeholder) come back, or stay cleared?",
  "On a re-run that extracts a record the paralegal had entered by hand and that entry is still pending: keep both (with a note), or is the sweep a deliberate decision? Reading of api.md:129 is keep both."
 ]}
```
