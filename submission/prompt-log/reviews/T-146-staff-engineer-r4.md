# T-146 staff-engineer review, round 4 (fix-up c2913a6, scoped check)

Verdict: **pass** (0 blockers, 0 majors, 2 minors). Both requested checks hold on `git archive HEAD` (HEAD = c2913a6).

Scope note: the working tree has uncommitted T-161 edits to `app/backend/pipeline.py` and `memory/contracts/api.md` (`git diff --stat HEAD`). I did not review them. Every line number below is HEAD.

## 1. Keep-and-note compares the whole ladder (a2 repro): holds

Repro: a complete sample run, then accept (and, in a second run, dismiss) a2 ($185 rate, needs_review, `AMOUNT_RATE_NOT_TOTALED`, judge agree). The re-run uses `j2` = disagree.

- a2's stored row is unchanged apart from `rerun_note`. The probe compares every stored column of every item (`artifacts/review-evidence/T-146-r4/p1_head.out`). The only other differing row is a4, which is undecided and takes the new check result as designed.
- a2 carries a note: `kind` disagreed, step "a different result". The item view shows the message.
- Case: `failed` / `run_partial`. The message says "The re-run gave a different result for 2 items you had already decided ... each item carries a note", because a1 (accepted, verified) is kept whole and noted too.
- Gate: `trace.export_blockers` returns `['RUN_FAILED']` (`app/backend/trace.py:1197`, `cx.case["status"] == "failed"`).
- The equal-rank table (`tests/unit/test_t146_r4_ladder_compare_and_conflicts.py:33-54`) pins each arm of `_checks_worse` (pipeline.py:275-287). A reason-only change, a judge change, a code-check flip and unsupported summary tokens each return True.

## 2. Conflicts-step failure gives RUN_FAILED: the worker is right

- The real step key is `j3`. `app/backend/judges.py:59` calls `_run("j3", ...)`, and `app/backend/flags.py:333` sets `step = "j3"`.
- Nothing calls a step named `conflicts`. The `"conflicts"` entries in the test scripts are never read, so `sample_script(conflicts=...)` does nothing. My r3 probe used `conflicts=down(...)` and reported that path as a failure probe. It tested nothing, and my r3 count of "14 failure probes" included it.
- Probe with the real key (`p1_head.out`, section B). Judge 3 down or fixture-miss, with f_cx1 decided and undecided, in all four variants:
  - case `failed`, `run_partial`, message "The AI step failed for 1 item (the second check) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry.";
  - gate `RUN_FAILED`;
  - f_cx1's stored row unchanged. The note is present only when the item was decided.
- Control (section C): `conflicts=down("conflicts")` gives status done, error None, case `ready`, no blockers. The dead key is a no-op.
- Not re-probed: "down twice with nothing to keep" and "deadline before the conflicts stage". The r4 tests cover both and pass.

## Tests run (archive of c2913a6, `/Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest <file> -q -p no:cacheprovider --tb=no`)

- `test_t146_r4_ladder_compare_and_conflicts.py`: 36 passed
- `test_t146_r3_decided_items_never_lowered.py`: 56 passed
- `test_t146_r2_failed_rerun_keeps_items.py`: 16 passed
- `test_t146_rerun_keeps_items.py`: 6 passed
- `test_reclassify.py`: 92 passed
- Total: 206 passed, 0 failed.

I did not run the full unit suite or the CLI in this scoped check.

## Mutants (`artifacts/review-evidence/T-146-r4/mutants.out`, run on archive copies, not the repo)

- M1 `_disagrees` ignores `_checks_worse`: killed (12 fail). The two a2 end-to-end tests fail on accept and dismiss (`mutant_M1_e2e.out`).
- M2 new-reason clause removed: killed (2 fail).
- M3 judge clause removed: killed (4 fail).
- M4 code-check clause removed: killed (1 fail).
- M5 no-answer treated as negative: killed (1 fail).
- M6 export gate ignores a failed case: killed (15 fail).
- M7 partial message drops the second-check step: killed (11 fail).
- M8 `_degrades` never degrades a no-answer flag: killed (8 fail).

## Findings

**F1 (minor). An identical re-run rewrites every decided row. The updated_at value moves and the judge call_id is replaced.** `artifacts/review-evidence/T-146-r4/p2_head.out` shows all six decided items with `row rewritten=True (updated_at 2.0 -> 3.0)`. Judge call_id changes: e1 `call18 -> call10`, e3 `call11 -> call12`. Cause: pipeline.py:351 `DB.update_item(conn, it["id"], now=now, case=cid, **row)` runs for every decided row that is not kept (the `_disagrees` branch at pipeline.py:335 is not taken). The helper `full()` at tests/unit/test_t146_r3_decided_items_never_lowered.py:34 drops `updated_at` and call ids, so the "0 rows differing" checks in r3 and r4 cannot see this. api.md:129 says "a re-run never lowers or replaces a *decided* item". I rated this minor because the content, state, decision and note are unchanged and nothing the paralegal sees changes. I could not check whether an earlier call stays in `llm_calls` on the production path, since `FakeCall` does not write that table. My r3 "identical re-runs: 0 rows differing" line came from this helper and missed the rewrite.

**F2 (minor). The dead `conflicts` script key is in at least ten FakeCall scripts, so a "conflicts down" test can pass without judge 3 ever running.** `git grep -n` for `"conflicts"` and `conflicts=` under `tests/unit` at HEAD finds `_fakes.py:50` (the default `sample_script`), `test_pipeline.py:180` (`sample_script(conflicts={"flags": SEM})`) and `test_flags_pass.py:72` (`FakeCall({"conflicts": AU.LLMFailed("x")})) == []`), plus about seven more. `FakeCall.__call__` (`tests/unit/_fakes.py:14`) returns `self.script.get(step, {})` for an unknown key, so nothing fails. Control run (p1 section C): status done, case ready, no blockers. `test_flags_pass.py:72` passes whatever the step does, since `rec(1)` has no candidate. This is how my r3 probe went wrong. It is a qa-owned test-quality issue, and the r4 tests use the real key `j3`, so the card's claim stands.

## Not counted (per brief)

At HEAD, `pipeline.py:567` sets `rerun = bool(DB.list_items(conn, cid, "entry"))`, and `pipeline.py:582` passes `empty` only when `rerun` is true. A case with no stored entries never gets the "no earlier result to keep" message. The working-tree T-161 edit is changing that line. I did not probe it.

## Right

- Judge 3 is covered on the real key `j3`: decided and undecided, judge down and fixture-miss, all keep the row and read run_partial with RUN_FAILED.
- The a2 repro is kept whole on accept and on dismiss, and the 8 mutants of the new compare and gate code are killed.
- The worker's dead-key diagnosis is correct, and the r3 test file is unchanged.

```json
{"card": "T-146", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit c2913a6 (HEAD; fix-up after bf53087): app/backend/pipeline.py (_checks_worse, _disagrees, _persist, run_pipeline), memory/contracts/api.md:129, tests/unit/test_t146_r4_ladder_compare_and_conflicts.py; git archive of HEAD in scratchpad t146r4/archive; fixture backend; sample case evals/golden/sample.txt; no app URL (not run); working-tree T-161 edits not reviewed",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-146-staff-engineer-r3.md, memory project_t146_r3/r2 patterns, python3 tools/board.py show T-146 (orchestrator 14:47:33Z §7.4 note, handoff)",
  "git rev-parse HEAD (c2913a6); git merge-base --is-ancestor c2913a6 HEAD (ancestor); git diff --stat c2913a6 HEAD on the r4 paths (no change); git status (working tree has uncommitted T-161 edits to pipeline.py and api.md, not reviewed)",
  "git show c2913a6 -- app/backend/pipeline.py memory/contracts/api.md (full diff); the r4 test file read in full (tests/unit/test_t146_r4_ladder_compare_and_conflicts.py, 170 lines)",
  "git archive HEAD into scratchpad t146r4/archive; judges.py:59 and flags.py:333 (step key j3), _fakes.py:14 FakeCall dispatch, trace.py:1197 export gate, git show HEAD:app/backend/pipeline.py line citations",
  "pytest on the archive, python -I: test_t146_r4_ladder_compare_and_conflicts.py 36 passed; test_t146_r3_decided_items_never_lowered.py 56 passed; test_t146_r2_failed_rerun_keeps_items.py 16 passed; test_t146_rerun_keeps_items.py 6 passed; test_reclassify.py 92 passed (206 total, 0 failed)",
  "artifacts/review-evidence/T-146-r4/probes/p1.py on the archive (p1_head.out): a2 repro accept and dismiss (row whole, note on a2 and a1, run_partial, RUN_FAILED); judge 3 down and fixture-miss x decided/undecided f_cx1 (run_partial, exact message, RUN_FAILED, row unchanged); control conflicts=down (dead key) -> ready, no blockers",
  "artifacts/review-evidence/T-146-r4/probes/p2.py on the archive (p2_head.out): identical re-run of a decided case; updated_at and judge call_id compared per decided item",
  "artifacts/review-evidence/T-146-r4/probes/mutate.py on archive copies (mutants.out; mutant_M1_e2e.out): 8 mutants (M1 _checks_worse call removed, M2 reason clause, M3 judge clause, M4 code-check clause, M5 no-answer as negative, M6 export gate, M7 second-check message, M8 _degrades judge arm): 8 killed",
  "git grep -n '\"conflicts\"' and conflicts= under tests/unit at HEAD (dead script keys); sed/grep line citations at HEAD (pipeline.py 275, 289, 303, 335, 351, 567, 582; test helper full() at 34; api.md:129; r4 test lines 33-54 and 42)",
  "not run: full unit suite (worker reports 4531 pass, 1 fail outside this card), python -m app.pipeline CLI, E2E; scoped check only"
 ],
 "verdict": "pass",
 "scores": {"whole_ladder_keep_and_note": 5, "conflicts_step_key_j3_gate": 5, "case_message_and_gate_agree": 5, "decided_rows_untouched_on_identical_rerun": 3, "test_quality_mutation_sensitivity": 4},
 "findings": [
  {"severity": "minor", "title": "An identical re-run rewrites every decided row: updated_at moves and the judge call_id is replaced; the r3/r4 whole-row helper excludes both, so no test sees it",
   "evidence": "artifacts/review-evidence/T-146-r4/p2_head.out: 'e3 decided=accepted row rewritten=True (updated_at 2.0 -> 3.0) judge call_id 'call11' -> 'call12''; all six decided items rewritten=True. pipeline.py:351 DB.update_item(conn, it['id'], now=now, case=cid, **row) runs for a decided row that is not kept (the _disagrees branch at pipeline.py:335 is not taken). tests/unit/test_t146_r3_decided_items_never_lowered.py:34 full() drops updated_at and call ids. memory/contracts/api.md:129: 'a re-run never lowers or replaces a *decided* item'.",
   "why_it_matters": "Content, state, decision and note are unchanged, so nothing the paralegal sees changes. But the rule text says 'replaces', and the audit pointer of a decided item moves to the newest call. My r3 'identical re-runs: 0 rows differing' came from this helper and missed it. Minor, not blocker: no fact is lost if llm_calls keeps the earlier call (not verified: FakeCall does not write llm_calls, so the production path was not checked).",
   "fix": "Skip the write for a decided row whose content, state, reasons, checks and judge verdict are identical (keep its ladder and updated_at), or state in api.md that an identical re-run refreshes the audit pointer and updated_at. Remove updated_at and call_id from the exclusion list in full() so the test sees the change.",
   "acceptance_test": "Identical re-run of a decided case: updated_at is unchanged for every decided item and ladder.judge.call_id equals the stored value. Mutation: restoring the unconditional update at pipeline.py:351 fails it."},
  {"severity": "minor", "title": "The dead 'conflicts' script key is in at least ten FakeCall scripts, so a 'conflicts down' test can pass without judge 3 ever running",
   "evidence": "git grep -n for '\"conflicts\"' and 'conflicts=' under tests/unit at HEAD: tests/unit/_fakes.py:50 (default sample_script), tests/unit/test_pipeline.py:180 (sample_script(conflicts={'flags': SEM})), tests/unit/test_flags_pass.py:72 (FakeCall({'conflicts': AU.LLMFailed('x')})) == []), plus about seven more. tests/unit/_fakes.py:14 returns self.script.get(step, {}) for an unknown key. Control run (artifacts/review-evidence/T-146-r4/p1_head.out, section C): conflicts=down('conflicts') -> status done, error None, case ready, blockers [].",
   "why_it_matters": "This is how my r3 probe reported a conflicts-down path that never called judge 3. test_flags_pass.py:72 passes whatever the step does, because rec(1) has no candidate and no call reads the key. Test-quality issue for qa; the card's claim is correct because the r4 tests use the real key j3.",
   "fix": "Make FakeCall raise on any script key that is not a step name (audited.PROMPT_OF_STEP keys and the pipeline's step names), delete the dead 'conflicts' entries, and point test_pipeline.py:180 and test_flags_pass.py:72 at 'j3'.",
   "acceptance_test": "A unit test that FakeCall({'conflicts': ...}) raises on the first call; a test that every key in sample_script() is a real step name. Mutation: putting 'conflicts' back into sample_script fails it."}
 ],
 "whats_right": [
  "Judge 3 is covered on the real key j3: decided and undecided, judge down and fixture-miss, each keeps the row, reads run_partial with the exact message, and gates RUN_FAILED.",
  "The a2 repro is kept whole on accept and on dismiss, with a note on a2 and a1 and RUN_FAILED at the gate; 8 of 8 mutants of the new compare and gate code are killed.",
  "The worker's dead-key diagnosis is correct, and the sealed r3 test file is unchanged."
 ],
 "questions_for_chris": [
  "A better result on a decided item is applied silently, including needs_review to verified on an accepted item: _disagrees returns False for a judge that goes disagree to agree (tests/unit/test_t146_r4_ladder_compare_and_conflicts.py:42), and api.md:129 lists only worse results as triggers. Is silent improvement intended, or should a better result on a decided item also be noted?",
  "Should an identical re-run leave decided rows untouched (F1), or is refreshing updated_at and the judge call_id on each re-run intended?"
 ]}
```
