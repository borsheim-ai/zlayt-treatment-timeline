# T-165 staff-engineer review, round 2 (commit 56d746c)

Verdict: **pass**. The r1 blocker is fixed. A re-run that extracts a hand-entered record now keeps the paralegal's pending entry, adds a `rerun_note` that says the AI now also has an entry, and never deletes it. Two r1 minors are still open and are carried forward below; neither is a blocker or major.

Scope: commit 56d746c (HEAD at review time), read on a `git archive 56d746c` copy in scratch (`$S/t165-r2/head`, where `$S` is the scratchpad). The working tree is dirty with other agents' files and was not used. The archive file list matches `git ls-tree -r --name-only 56d746c` exactly.

What holds:
- The r1 blocker (scenario G) is closed. Probe G on HEAD: `e1` (AI, verified) and `e1_m` (hand, pending) are both present, `e1_m` is untouched, and the case reads `ready`. The new test `test_a_rerun_that_recovers_the_record_keeps_the_hand_entry_and_says_the_ai_now_has_one_too` (test_t165_partial_extract.py:161) asserts this and the API note text.
- Round-1 checks still hold. The probe A to F and H output on HEAD matches the r1 `probe_out.txt` line for line, except G (the intended change). A to F are unchanged, so the first-run partial naming, all-extracted-ready, and hand-entry-warning behaviour are intact.
- The note reaches the paralegal: `app/frontend/review.js:372` renders `item.rerun_note` on every item card, and the note is in the view payload (test line 173).
- No new DELETE path. The only remaining `DELETE` in `_persist` is at `app/backend/pipeline.py:381`, reached only for non-hand pending rows; the hand-entry branch (`pipeline.py:375-377`) `continue`s before it.
- Mutants on scratch copies of the archive, each applied to one site, are all killed by the T-165 file: m1 reinstates the r1 `not any(r in live ...)` condition (2 failed), m2 disables the note (1 failed), m3 disables the note clear (1 failed).

Out of scope, not counted: the full unit suite on the archive gives 5279 passed, 8 skipped, 1 failed. The failure is `tests/unit/test_e2e_contract.py::test_every_test_id_is_declared` (missing `cases-keys`, `btn-new-case`, `do-first-item`). Those test ids are introduced by frontend commit f7a8f2a (`git show f7a8f2a` lines 122, 124, 193). The brief says this is being fixed elsewhere.

Carried-forward minors from r1 (not changed by 56d746c, so not re-graded as new findings):
1. Dismissing a hand-entered entry leaves a stale `ENTERED_BY_HAND` warning and the failure never returns (probe H: `e1_m` dismissed, warnings still `[('ENTERED_BY_HAND', 1, 'e1')]`, status `ready`). No test covers dismissal. Still open.
2. `tests/unit/test_t139_charge_text.py:224` still asserts `counts.entries == 4`, which counts the hand-entry as an entry. This is the T-168 fixture workaround. Still open; revert with T-168.

Evidence: `artifacts/review-evidence/T-165/r2/probe_out_r2.txt` (probe A to H on the HEAD archive) and `artifacts/review-evidence/T-165/r2/mut_r2.py` (mutant script; mutants m1 to m3 as described above).

```json
{"card": "T-165", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 56d746c (HEAD at review time) via git archive copy at $S/t165-r2/head; files: app/backend/pipeline.py (_persist 365-382, _keep_hand_entry 385-398), tests/unit/test_t165_partial_extract.py (new tests 161-196), app/frontend/review.js:372 (note render, read only); synthetic golden sample; no app URL exercised (in-process only)",
 "exercised": [
  "python3 tools/board.py show T-165 not run; card scope taken from the brief and reviews/T-165-staff-engineer.md (r1, read in full)",
  "git show 56d746c -- app/backend/pipeline.py tests/unit/test_t165_partial_extract.py (full diff read)",
  "git archive 56d746c | tar -x into $S/t165-r2/head; file list diffed against git ls-tree -r --name-only 56d746c (diff exit 0)",
  "cd $S/t165-r2/head && PYTHONPATH=$S/t165-r2/head <repo>/.venv/bin/python -m pytest tests/unit/test_t165_partial_extract.py tests/unit/test_t146_r2_failed_rerun_keeps_items.py tests/unit/test_t146_r3_decided_items_never_lowered.py tests/unit/test_t146_r4_ladder_compare_and_conflicts.py tests/unit/test_t146_rerun_keeps_items.py -q -p no:cacheprovider -> 128 passed, exit 0",
  "PYTHONPATH=$H <repo>/.venv/bin/python probe_t165.py (copy of artifacts/review-evidence/T-165/probe_t165.py) on HEAD archive, scenarios A-H -> artifacts/review-evidence/T-165/r2/probe_out_r2.txt",
  "diff of r1 artifacts/review-evidence/T-165/probe_out.txt against probe_out_r2.txt (TMP line removed): only line 46 differs, scenario G entries now include e1_m pending verified",
  "mutant m1 (pipeline.py:375 adds 'and not any(r in live ...)', reinstating the r1 sweep) on scratch copy: tests/unit/test_t165_partial_extract.py -> 2 failed, 12 passed",
  "mutant m2 (pipeline.py _keep_hand_entry 'if ai:' -> 'if False:', no note written) -> 1 failed, 13 passed",
  "mutant m3 (pipeline.py _keep_hand_entry 'elif ... ai_entry' -> 'elif False:', note never cleared) -> 1 failed, 13 passed",
  "full unit suite on HEAD archive: cd $S/t165-r2/head && <repo>/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -> 5279 passed, 8 skipped, 1 failed (tests/unit/test_e2e_contract.py::test_every_test_id_is_declared, out of scope; ids from f7a8f2a)",
  "grep -n 'DELETE FROM' app/backend/pipeline.py on archive -> line 381 (f-string table delete, reached only for non-hand pending rows)",
  "read app/frontend/review.js:337 and :372 on archive (rerun_note rendered on item cards; not exercised in a browser)"
 ],
 "verdict": "pass",
 "scores": {"first_run_partial_names_records": 5, "all_extracted_stays_ready": 5, "hand_entry_warning_not_failure": 4, "rerun_keeps_pending_hand_entry": 5, "dismiss_and_recover_states": 2, "pins_justified": 4, "test_strength_mutants": 5},
 "findings": [
  {"severity": "minor",
   "title": "Carried from r1: dismissing a hand-entered entry leaves a stale ENTERED_BY_HAND warning and the failure never returns",
   "evidence": "probe_out_r2.txt block '== H': e1_m review_status 'dismissed', case status ready, error null, warnings [('ENTERED_BY_HAND', 1, 'e1')]; app/backend/generator.py:205-219 counts any non-rejected hand entry; no test in tests/unit/test_t165_partial_extract.py covers dismissal",
   "why_it_matters": "The case-level message tells the paralegal she entered record 1 by hand after she has dismissed that entry. The state of record 1 (no usable entry) is not reported. Unchanged by 56d746c, so not a new defect.",
   "fix": "Exclude dismissed hand entries from entered_by_hand, or word the warning by state; decide with Chris whether dismissing a hand entry re-opens RUN_FAILED (r1 questions_for_chris).",
   "acceptance_test": "Hand-enter record 1 after a failed run, dismiss e1_m; assert the chosen state (RUN_FAILED with record 1 named, or no ENTERED_BY_HAND warning). Pin it."},
  {"severity": "minor",
   "title": "Carried from r1: test_t139 counts.entries == 4 counts a hand entry as an AI entry",
   "evidence": "tests/unit/test_t139_charge_text.py:224 'assert j[\"counts\"][\"entries\"] == 4  # e1, e5, e6 and the hand-entered record 3 (wait_ready)'",
   "why_it_matters": "An AI-timeline assertion now counts a paralegal entry. It is a documented workaround for the T-168 lib01 fixture gap and can hide an AI regression on lib01. Unchanged by 56d746c.",
   "fix": "Keep the workaround; assert AI-made entries (ladder.entered_by != 'reviewer') == 3 and the hand entry id present. Revert with T-168.",
   "acceptance_test": "test_t139 lib01: AI-made entries == 3, e3_m present; mutant dropping one AI entry fails."}
 ],
 "whats_right": [
  "A re-run that extracts a hand-entered record keeps the pending entry, adds rerun_note (kind ai_entry) naming the AI entry, and never deletes it (probe G, test line 161; m1 killed)",
  "The round-1 probe scenarios A to F are unchanged on HEAD; only G differs, as intended (probe_out_r2.txt vs r1 probe_out.txt)",
  "The note is cleared when a later run has no AI entry for the record (test line 187; m3 killed)"
 ],
 "questions_for_chris": [
  "Dismissing a hand entry after a failed extract: should RUN_FAILED and the tray placeholder come back, or stay cleared? (carried from r1)"
 ]}
```
