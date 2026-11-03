# T-169 round 2 review (staff-engineer-reviewer), commit 6e1294f

Scope: `tests/unit/test_eval_runner.py` at 6e1294f only (test-only card). Reviewed in a fresh `git clone` detached at 6e1294f, in the session scratchpad (`T169_staff_r2/clone`), status clean. The project tree's HEAD is 28437b2 at review time; these findings are for 6e1294f.

Verdict: **changes** (0 blockers, 1 major, 2 minors). Count binding and forge detection work, and the two r1 minors F3 and F5 are closed. The run-folder binding does not do what the card and the orchestrator's round-2 request say: the test never reads the run folder the report names, and it still passes when that folder is deleted. The r1 F4 minor is not closed.

Brief checks:
- Ties to report 20261102T164038Z.md: yes. The link is derived from `generated_at`, and the test compares the report's sentences, per-type table, backend and source commit with the file. Seven forges of `calibration.json` each turn at least one binding or route test red (probe.log section A).
- Ties to the run folder: no. The brief's `runs/20261102T161327Z` is `evals/reports/runs/20261102T161327Z` in the tree. The test picks the newest folder at or before the report id and checks file-name presence only. See F1.
- Forged counts fail: yes, A1 to A7.
- Minors: F3 fixed, F5 fixed, F4 not closed (F3 below).
- `tests/unit/test_eval_runner.py`: 111 passed, 1 skipped in the clone. The skip is the live regen test (line 851).
- Not counted: the r1 F1 red e2e test (T-166), per the brief.

## Findings

**F1 major (round 2), the run binding picks "the newest folder at or before the report id", not the folder the report names.** `tests/unit/test_eval_runner.py:1124-1126` sorts `runs/<id>` folders with `d.name <= rid` and checks `runs[-1]` for the ten case stems. The report itself names its folder at `evals/reports/20261102T164038Z.md:131`: "per-run artifacts: `evals/reports/runs/20261102T161327Z`". The test never reads that line. Probe D2 deletes `evals/reports/runs/20261102T161327Z` in a copy, adds `runs/20261102T163000Z` with the same ten case files, and runs `test_committed_calibration_run_directory_exists_with_every_case`: `1 passed` (probe.log, section D). Today the test passes only because no other folder falls between 161327Z and 164038Z. Why it matters: r1 F2 was about live counts with no test binding them to a run. A run folder can be deleted or replaced without a red test. Fix: take the run id from the report's "per-run artifacts" line (or record it in the header), assert that exact folder exists and holds all ten case files, and keep the newest-folder rule out. Acceptance: in a clone, delete `evals/reports/runs/20261102T161327Z` and add `runs/20261102T163000Z` with the ten case files; the run test must fail and name 161327Z.

**F2 minor (round 2), the binding tests do not pin the table or by_state comparisons on their own.** Removing the per-type table assertion (line 1114) or the by_state-vs-sentence assertion (line 1116), and then forging only that dimension, leaves the three binding tests green: probe2.log P1 `3 passed` (table-only forge, `by_type.entry.verified.matched` 52 to 53) and P3 `3 passed` (by_state-only forge, `by_state.verified.matched` 82 to 83). The same forges are caught by `test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes` and `test_committed_report_is_valid_when_present` (probe.log A1, A2), so the suite as a whole is not blind to them. The binding test itself is only kill-tested by the coordinated forge. Fix: add single-dimension forge cases (table-only and by_state-only) to `test_report_binding_fails_on_a_coordinated_count_and_sentence_edit`. Acceptance: deleting line 1114 or line 1116 turns a single-dimension forge of the binding test red.

**F3 minor (r1 F4 carried, not closed), the served live numbers describe 312efe6; the decision is only in a card note.** `grep -n` of `memory/DECISIONS.md`, `memory/ORCHESTRATOR_DECISIONS.md`, `memory/ASSUMPTIONS.md` and `memory/SCOPE_CUTS.md` for `312efe6`, `T-169` and `calibration` finds no decision entry for the gap (only a T-090 line in SCOPE_CUTS). The r1 fix was "record the gap in memory/DECISIONS.md or re-measure". The orchestrator note of 17:17:13Z is a rationale in the board, not a decision entry. Facts I checked: `git log --oneline 312efe6..6e1294f` lists 10 commits, including 56004f0 and 235e135 (judge parsing) and 2bfd396 (T-171, `app/backend/pipeline.py`, `count_charge.py`). `git diff 312efe6 6e1294f -- app/llm/_types.py app/llm/audited.py app/llm/backends/claude_cli.py` shows the closing-object read is opt-in and applies to the extract and extract_es steps only (`app/llm/audited.py`, `LENIENT_JSON_STEPS`); judges parse strictly. Mitigation: probe3.log shows that the fixture eval at 312efe6 and at 6e1294f gives identical by_state (82/83, 11/11), by_type, sentences and hashes. That covers the deterministic path only. The live extract path changed, and nothing in the card shows that it changes only the lib01 record-3 answer. Fix: write a decision entry in `memory/DECISIONS.md` naming 312efe6, the ten later commits, the identical fixture result and the live-only residual, or re-measure at HEAD. Acceptance: `grep -n 312efe6 memory/DECISIONS.md` finds the entry, or a live header at HEAD exists and the served sentence matches it.

Round-1 minors closed:
- F3 (dirty-tree negative test): line 805 has a message and line 821 matches it. Probe B4 (`CAL_BACKENDS` shrunk to fixture, line 799) turns the dirty-tree test red (2 failed); probe B5 (message removed) turns it red (1 failed). The literal tuple at line 815 is what makes B4 fail, as the comment says.
- F5 (regen skip too broad): line 851 now skips only for `claude-cli`. Probe C2 (condition reverted) skips a header with backend `foo`; with the fix (C1) the regen test runs and fails.

Checks with no finding: the r2 diff adds no `except`, `float(`, `sleep(`, retry, or network call (grep of the `+` lines: 0 matches). The regen skip is visible with its reason at line 853 and the fixture branch still runs.

## What is right
- Forged counts are caught: seven single or coordinated forges of `calibration.json` each turn a binding or route test red, and a dangling `generated_at` fails loudly (probe.log A1 to A7).
- F3 and F5 are closed, and each has a mutant that proves it (B4, B5, C1, C2).
- The report link fails loudly when the report is missing (A6), so the derived link is not silent.

```json
{"card": "T-169", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 6e1294f, tests/unit/test_eval_runner.py (round 2); fresh clone detached at 6e1294f in the session scratchpad (T169_staff_r2/clone), status clean; project HEAD is 28437b2 at review time and was not used; cited run folder is evals/reports/runs/20261102T161327Z; sample case n/a (unit tests)",
 "exercised": [
   "git rev-parse 6e1294f and git clone of the project into the scratchpad, detached at 6e1294f (6e1294f171cd1e9a3e82014a9d321286d1a527eb), git status clean",
   "board.py show T-169 (round-1 findings, orchestrator notes 17:12:52Z and 17:17:13Z, handoff); read reviews/T-169-staff-engineer.md (round-1 F1 to F5)",
   "git diff 5ed37ad 6e1294f -- tests/unit/test_eval_runner.py read in full; grep of the + lines for except, float(, sleep(, retry, http: 0 matches",
   ".venv/bin/python -m pytest tests/unit/test_eval_runner.py -q in the clone: 111 passed, 1 skipped (regen skip at line 851)",
   ".venv/bin/python -m pytest -v -k calibration subset in the clone: 25 passed, 1 skipped; the three new tests PASSED",
   "git show 6e1294f:evals/reports/calibration.json and evals/reports/20261102T164038Z.md read in the clone: generated_at 2026-11-02T16:40:38Z, source 312efe6, backend claude-cli, by_state verified 82/83, needs_review 11/11; report line 131 names evals/reports/runs/20261102T161327Z",
   "artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe.py -> probe.log: section A seven forges of calibration.json (by_state verified matched 83; by_type entry matched 53; by_type amount matched 8; sentence 83/83; by_state needs_review matched 10; generated_at moved to a missing report; coordinated by_state plus sentence): each rc=1, 2 or 3 failures; section B mutants B1 to B5; section C regen with backend foo (C1 fixed FAILED, C2 reverted SKIPPED); section D baseline 1 passed and decoy copy with the cited folder removed 1 passed; calibration and test sha256 restored (True, True)",
   "artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe2.py -> probe2.log: binding-only node set; P0 pristine 3 passed; P1 table check removed plus table-only forge 3 passed; P2 sentence check removed plus sentence-only forge 1 failed; P3 by_state check removed plus by_state-only forge 3 passed; restored True True",
   "artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe3.py -> probe3.log: git archive of 312efe6 and 6e1294f, evals.run --out with the fixture backend (LLM_BACKEND and ENABLE_LIVE unset): by_state, by_type, sentences and hashes identical at both shas (rc=1 at both, not investigated)",
   "git log --oneline 312efe6..6e1294f (10 commits); git diff 312efe6 6e1294f -- app/llm/_types.py app/llm/audited.py app/llm/backends/claude_cli.py: lenient read opt-in, extract and extract_es only; judges strict",
   "grep -n 312efe6, T-169 and calibration over memory/DECISIONS.md, memory/ORCHESTRATOR_DECISIONS.md, memory/ASSUMPTIONS.md, memory/SCOPE_CUTS.md: no 312efe6 or T-169 decision entry",
   "Not run: full pytest tests/unit (its one red test is T-166's, excluded by the brief)"
 ],
 "verdict": "changes",
 "scores": {"report_binding": 4, "run_binding": 2, "forged_count_detection": 4, "minors_closed": 3, "eval_runner_suite_green": 5, "honest_skips": 4},
 "findings": [
   {"severity": "major", "title": "Run binding picks the newest run folder at or before the report id, not the folder the report names; a deleted cited folder still passes",
    "evidence": "tests/unit/test_eval_runner.py:1124-1126 (runs = sorted(... if d.name <= rid); have = ... runs[-1]); evals/reports/20261102T164038Z.md:131 '- per-run artifacts: `evals/reports/runs/20261102T161327Z`'; probe.log section D: D2 cited folder removed, decoy runs/20261102T163000Z with the ten case files -> 1 passed",
    "why_it_matters": "r1 F2 asked for a test that binds the live counts to a run. As written, any folder with the ten case stems at or before the report id satisfies it, so the cited run can be deleted or replaced with no red test. It passes today only because no other folder falls between 161327Z and 164038Z.",
    "fix": "Take the run id from the report's 'per-run artifacts' line (or record it in the header); assert that exact folder exists and holds all ten case files; drop the newest-folder rule.",
    "acceptance_test": "In a clone, delete evals/reports/runs/20261102T161327Z and add runs/20261102T163000Z with the ten case files; the run test fails and names 161327Z"},
   {"severity": "minor", "title": "Binding tests do not pin the table or by_state comparisons on their own",
    "evidence": "tests/unit/test_eval_runner.py:1114 (assert got[\"table\"] == want) and :1116 (by_state disagrees with its own sentence); probe2.log P1 3 passed (table-only forge), P3 3 passed (by_state-only forge); probe.log A1 and A2 caught only by test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes and test_committed_report_is_valid_when_present",
    "why_it_matters": "A future edit that drops either comparison in the binding test is invisible to the binding tests; the other tests still catch the forges, so the gap is in the card's own test, not in the suite.",
    "fix": "Add single-dimension forge cases (table-only, by_state-only) to the binding tests alongside the coordinated one.",
    "acceptance_test": "Deleting line 1114 or line 1116 makes a single-dimension forge of test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts fail"},
   {"severity": "minor", "title": "r1 F4 not closed: the live numbers at 312efe6 have no decision entry; the rationale is in a card note",
    "evidence": "grep of memory/DECISIONS.md, ORCHESTRATOR_DECISIONS.md, ASSUMPTIONS.md, SCOPE_CUTS.md for 312efe6 or T-169: no entry; git log 312efe6..6e1294f = 10 commits incl. 56004f0, 235e135, 2bfd396; git diff 312efe6 6e1294f -- app/llm/audited.py: LENIENT_JSON_STEPS = frozenset({\"extract\", \"extract_es\"}); probe3.log: fixture counts identical at 312efe6 and 6e1294f",
    "why_it_matters": "The served sentences describe code that is no longer at HEAD, and the disposition rests on the claim that extract-only leniency changes only the lib01 record-3 answer. The fixture path does not exercise the live lenient read, so the claim is unverified for the other nine golden cases.",
    "fix": "Write a memory/DECISIONS.md entry naming 312efe6, the ten later commits, the identical fixture result and the live-only residual; or re-measure the live calibration at HEAD.",
    "acceptance_test": "grep -n 312efe6 memory/DECISIONS.md finds the entry, or a live calibration header at HEAD exists and the served sentence matches it"}
 ],
 "whats_right": [
   "Seven forges of calibration.json each turn a binding or route test red, and a dangling generated_at fails loudly (probe.log A1 to A7)",
   "r1 F3 and F5 are closed: the clean-tree message and match (lines 805, 821) and the claude-cli-only skip (line 851) each have a mutant that proves them (B4, B5, C1, C2)",
   "The diff adds no except, float(, sleep(, retry or network call; test_eval_runner.py is 111 passed, 1 skipped in a clean clone"
 ],
 "questions_for_chris": []}
```
