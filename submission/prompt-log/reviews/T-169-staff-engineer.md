# T-169 review (staff-engineer-reviewer), commit 5ed37ad

Scope: `tests/unit/test_eval_runner.py` at 5ed37ad only (test-only card). Reviewed in a fresh `git clone` in the session scratchpad, detached at 5ed37ad. The project tree's HEAD has moved to 8398bee; findings are for 5ed37ad.

Verdict: **changes** (0 blockers, 2 majors, 2 minors, 1 nit). No §5 red flag: the skip is visible in pytest output with a written reason, nothing swallows errors, no money or LLM arithmetic, and the diff adds no network call or sleep.

What I ran (details in `artifacts/review-evidence/T-169-staff-engineer/`):
- Header positive: `pytest -k committed_calibration_header` on the committed live header (backend claude-cli, source_tree_clean true): PASSED.
- Dirty-tree negative: edited the clone's `evals/reports/calibration.json` to `source_tree_clean=false` with backend claude-cli. Header test FAILED at line 805 with `assert (False is True)`. Restored bytes; header test PASSED again.
- Regeneration skip: on the live header it is SKIPPED at line 853 with reason "committed calibration is a live claude-cli measurement; exact regeneration needs the live backend".
- Regeneration on a real fixture header (`git show f3ac48f:evals/reports/calibration.json`, backend fixture, source 6fa8ecc): the test ran (not skipped) and PASSED.
- Mutant A (clean-tree clause removed from line 805): `test_calibration_header_check_still_fails_on_a_dirty_tree` FAILED, "DID NOT RAISE". The guard is real.
- Mutant B (live skip at line 850 removed): regen test FAILED on the live header. The skip is the only thing that hides this mismatch; it is needed offline, but it means no test checks the live counts.
- `pytest tests/unit/test_eval_runner.py -q`: 108 passed, 1 skipped (the regen skip).
- `pytest tests/unit -q` on the clone at 5ed37ad: 1 failed, 5329 passed, 2 skipped. The failure is `tests/unit/test_e2e_contract.py::test_every_test_id_is_declared`, not in this card's file.

## Findings

**F1 major, AC 1 says "unit suite green" and it is red at the card commit.** The card's evidence cites only `test_eval_runner.py` (108 passed, 1 skipped). The full unit suite at 5ed37ad is 1 failed, 5329 passed, 2 skipped; the failure is `test_every_test_id_is_declared` at `tests/unit/test_e2e_contract.py:13`. That red is not caused by this commit, but the AC as written is not met. Fix: either fix the e2e id declaration in its owner's card, or narrow the AC to the file and say so. Acceptance test: `pytest tests/unit -q` returns rc 0 at the card commit, or the AC text names the file.

**F2 major, the skip removes the only count-level check on the live calibration, and the header cites no report.** The handoff says the live counts are covered by "the live report it cites". `evals/reports/calibration.json` has no report field. The tracked live report `evals/reports/20261102T164038Z.md` does match today (source 312efe6, verified 82/83, needs review 11/11), but only by timestamp. Probe 2 shows that editing one served sentence (82/83 to 83/83) is caught by `test_committed_report_is_valid_when_present` and `test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes`. A coordinated edit of counts and sentences that stays internally consistent is not caught by any test; I did not run that mutant. Fix: record the report path and its sha256 in the header, and add a test that the cited report's counts equal the committed counts. Acceptance test: change `by_state.verified.matched` and the matching sentence together in a clone; the new test must fail.

**F3 minor, the dirty-tree negative test passes for the wrong reason.** `tests/unit/test_eval_runner.py:820` uses `pytest.raises(AssertionError)` with no match, and the clean-tree assert at line 805 has no message. With `CAL_BACKENDS = ("fixture",)` (line 799), `-k dirty_tree` still passes (rc 0, "2 passed", probe2.log). The header test catches that case, but the negative test does not prove what its docstring says. Fix: add a message to line 805 and match it. Acceptance test: `CAL_BACKENDS = ("fixture",)` makes the dirty-tree test fail.

**F4 minor, outside the card AC: the live numbers describe older code.** The live header is `source_commit` 312efe6. Seven commits separate it from 5ed37ad, and 56004f0 (T-168 r2: "every judge (j1-j4) and other step parses strictly") and 235e135 (T-168) change judge reply parsing. The served sentences therefore describe code that is no longer at HEAD. The ancestor test passes, so nothing flags this. Fix: record it in `memory/DECISIONS.md` or re-measure at HEAD. This is an orchestrator decision.

**F5 nit, the skip condition is broader than its reason.** `tests/unit/test_eval_runner.py:850` skips for any `backend != "fixture"`, but the reason only covers claude-cli. The header test rejects unknown backends, so this is harmless today. Fix: skip only when `backend == "claude-cli"`.

## What is right
- The clean-tree requirement holds for both backends: the dirty-tree header fails at line 805, and mutant A kills the negative test.
- The regen skip is visible (SKIPPED with a written reason at line 853), and the fixture branch still runs and passes on the real fixture header from f3ac48f.
- The diff adds no `except`, `float(`, `sleep(`, retry, or network call.

```json
{"card": "T-169", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 5ed37ad, tests/unit/test_eval_runner.py only; fresh clone at scratchpad T169_staff_r1/clone detached at 5ed37ad; project HEAD is 8398bee (moved); sample case n/a (unit tests)",
 "exercised": [
   "fresh git clone detached at 5ed37ad; pytest tests/unit/test_eval_runner.py -q -> 108 passed, 1 skipped (skip = regen test, line 853)",
   "pytest -k committed_calibration_header on committed live header (claude-cli, source_tree_clean true) -> PASSED",
   "edited clone copy of evals/reports/calibration.json to source_tree_clean=false -> header test FAILED at line 805 (AssertionError); restored bytes; PASSED again",
   "regen test on committed live header -> SKIPPED with reason 'committed calibration is a live claude-cli measurement; exact regeneration needs the live backend'",
   "regen test on real fixture header (git show f3ac48f:evals/reports/calibration.json, backend fixture, source 6fa8ecc) -> ran, PASSED (not skipped)",
   "mutant A: clean-tree clause removed at line 805 -> test_calibration_header_check_still_fails_on_a_dirty_tree FAILED (DID NOT RAISE)",
   "mutant B: live skip (line 850) removed -> regen test FAILED on the live header (counts differ under fixture backend)",
   "mutant C: CAL_BACKENDS without claude-cli (line 799) -> dirty-tree test still PASSED (wrong reason)",
   "full pytest tests/unit -q in clone at 5ed37ad -> 1 failed, 5329 passed, 2 skipped; failure test_e2e_contract.py::test_every_test_id_is_declared",
   "mutant D: one served sentence edited (82/83 -> 83/83), counts unchanged, full tests/unit -> 3 failed (incl. test_committed_report_is_valid_when_present and test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes)",
   "git ls-files evals/reports; grep of header keys; dated live report evals/reports/20261102T164038Z.md read (source 312efe6, 82/83 and 11/11)",
   "git rev-list --count 312efe6..5ed37ad = 7; commits 56004f0 and 235e135 touch judge parsing",
   "grep of the 5ed37ad diff for except, float(, sleep(, retry, network, model ids: only comment and docstring matches",
   "board.py show T-169 (AC 1 text and notes)",
   "probe scripts and logs: artifacts/review-evidence/T-169-staff-engineer/t169_probe.py, t169_probe2.py, probe.log, probe2.log"
 ],
 "verdict": "changes",
 "scores": {"dirty_tree_guard": 4, "live_regen_skip_provenance": 2, "suite_green_at_card_commit": 2, "negative_test_specificity": 3, "determinism_offline": 4, "honest_skips": 4},
 "findings": [
   {"severity": "major", "title": "AC 1 says unit suite green; full unit suite is red at 5ed37ad",
    "evidence": "probe2.log baseline: full tests/unit at 5ed37ad 1 failed, 5329 passed, 2 skipped; FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared (test_e2e_contract.py:13); board.py show T-169 AC 1 text ends 'unit suite green'",
    "why_it_matters": "The card's own AC is not met at its commit, and the evidence cites only one file.",
    "fix": "Fix the e2e id declaration in its owner's card, or narrow AC 1 to the file and name the red test.",
    "acceptance_test": "pytest tests/unit -q returns rc 0 at the card commit, or AC 1 text names the file scope"},
   {"severity": "major", "title": "Live skip leaves the served live counts with no test binding them to a run; the header cites no report",
    "evidence": "evals/reports/calibration.json header has no report field; tracked evals/reports/20261102T164038Z.md matches today (82/83, 11/11, source 312efe6) by timestamp only; probe2.log mutant D: served sentence edit caught by test_calibration_route.py::test_committed_report_is_valid_when_present and test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes; coordinated count+sentence edit not run",
    "why_it_matters": "The regen check was the test that caught unreproducible committed counts in T-090 r1. The skip removes it for the live file, and the handoff's 'live report it cites' does not exist in the header.",
    "fix": "Record report path and sha256 in the header; add a test that the cited report's counts equal calibration.json.",
    "acceptance_test": "In a clone, change by_state.verified.matched and its sentence together; the new test fails"},
   {"severity": "minor", "title": "Dirty-tree negative test passes for the wrong reason",
    "evidence": "tests/unit/test_eval_runner.py:820 'with pytest.raises(AssertionError):' (no match); line 805 clean-tree assert has no message; probe2.log C: CAL_BACKENDS=('fixture',) (line 799) -> rc 0, 2 passed",
    "why_it_matters": "The test's docstring claims it proves the clean-tree requirement; it does not, and only the positive test catches the wrong-backend case.",
    "fix": "Give the clean-tree assert at line 805 a message and match it in the test.",
    "acceptance_test": "With CAL_BACKENDS=('fixture',), test_calibration_header_check_still_fails_on_a_dirty_tree fails"},
   {"severity": "minor", "title": "Served live numbers were measured at a commit 7 behind 5ed37ad, before judge parsing changed (outside card AC)",
    "evidence": "calibration.json source_commit 312efe6; git rev-list --count 312efe6..5ed37ad = 7; 56004f0 'every judge (j1-j4) and other step parses strictly'; 235e135 T-168 parser change",
    "why_it_matters": "The served sentences describe code no longer at HEAD; the ancestor test passes, so nothing flags it.",
    "fix": "Record the gap in memory/DECISIONS.md or re-measure at HEAD (orchestrator decision).",
    "acceptance_test": "A decision entry or a fresh live header at HEAD exists and the served sentence matches it"},
   {"severity": "nit", "title": "Regen skip condition broader than its written reason",
    "evidence": "tests/unit/test_eval_runner.py:850 'if c[\"backend\"] != \"fixture\":' with reason text naming claude-cli only (line 853)",
    "why_it_matters": "Any future unknown backend would skip silently. Header test rejects unknown backends, so it is harmless today.",
    "fix": "Skip only when backend == 'claude-cli'.",
    "acceptance_test": "An unknown backend in the header makes the regen test run, not skip"}
 ],
 "whats_right": [
   "Dirty-tree header fails at tests/unit/test_eval_runner.py:805; mutant A kills the negative test",
   "Regen skip is visible with a written reason at line 853; the fixture branch still runs and passes on f3ac48f's header",
   "Diff adds no except, float(, sleep(, retry or network call"
 ],
 "questions_for_chris": ["Should the live calibration be re-measured at HEAD now that judge parsing changed (56004f0, 235e135), or is 312efe6 the accepted source for M2?"]}
```
