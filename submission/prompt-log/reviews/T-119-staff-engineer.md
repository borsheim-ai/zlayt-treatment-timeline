# T-119 review: staff-engineer-reviewer (round 1)

**Verdict: changes.** No blocker. Two majors: the WCAG 2.1.4 row-only key rule that the card's rewritten tests were built around has no negative test (two scratch mutants survive the keyboard files), and no e2e test reaches a row by Tab, so the spec's keyboard-only E2E (R-RV-4) is still unproven.

## What I ran

- Pinned the review to `git archive 288affc` (HEAD at review time; 288affc touches only `evals/` and one unit test, no `app/` or `tests/e2e/`). Card commit is 6e880e6. Working tree was dirty and was not used.
- Own fixture server on 127.0.0.1:7972, env `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch>/zlayt.sqlite`, pytest with the same env. Full `tests/e2e`: **172 passed, 1 skipped, 1 xfailed** in 229.47s. Server stopped by PID; port closed.
- Changed files re-run twice on a second server (127.0.0.1:7973): `test_side_by_side.py test_stepper.py test_suggestions.py` gave 50 passed, 1 xfailed both times. Judge-panel tests from `test_stepper.py` repeated 5 times: 3 passed each run.
- `tests/unit/test_e2e_contract.py`: 3 passed.
- Probe (scratch copy only, saved to `artifacts/review-evidence/T-119/probe_t119_keys.py`): Tab from page load reaches an item row after 20 presses, and `a` then accepts. Pressing `a`, `d`, `j`, `p` from the body changes nothing.
- Mutants (scratch copies, product code untouched):
  - mutA: `app/frontend/review.js:311` `RV.itemRowOf(t)` falls back to the first row, so letter keys act from the body. Probe fails ("key a changed a decision from the body"). The six keyboard-related files give 87 passed, 1 xfailed.
  - mutB: `app/frontend/sidebyside.js:102` drops `&& ZL.rv.itemRowOf(t)`, so `p` works from the body. Probe fails ("key p moved focus from the body to DIV"). The same six files give 87 passed, 1 xfailed.
- Greps: `keyboard.press` sites, `inner_text()` reads, `ZLAYT_DB` skip sites, `pytest.skip`, and the tray-flag copy in `timeline.js:135`, `conftest.py:45,51` and `board/cards/T-096.md:39`.
- Evidence: `artifacts/review-evidence/T-119/` (`e2e-full.txt`, `repeat-judge.txt`, `mutA-keyboard-files.txt`, `mutB-keyboard-files.txt`, `probe_t119_keys.py`, `mutate.py`).

## Skips and xfails (asked by the brief)

- **1 skip, no environment skips.** `tests/e2e/test_ladder_gate.py:37`: `pytest.skip("no rejected item in the sample fixture run")`. The ADR-005 409 check runs only when the fixture has a rejected item, which the curated sample never has.
- **Card's 16 skips reconcile with ZLAYT_DB unset.** The card reports 156 pass, 16 skip, 1 xfail, plus its one pre-fix failure, which is 174 in total. That matches the 174 collected. The 15 extra skips are the ZLAYT_DB-gated variants (`test_code_check_refusal.py:26,183` and `test_change_the_quote.py`). I did not re-run with ZLAYT_DB unset, so this is reconciliation, not a measurement.
- **Only xfail:** `tests/e2e/test_stepper.py::test_judge_panel_one_row_per_item_with_record_cue`, `strict=True` at `test_stepper.py:220` (T-117). The AC "only T-117 strict xfail remains" holds.

## Coverage question (asked by the brief)

The three assertions themselves are not weaker. The judge-count check (`test_stepper.py:257`) moved from a snapshot read to a retrying `expect(...).to_have_text(re.compile(...))`, which is substring-equivalent to the old `re.search`. The tray-why check (`test_suggestions.py:243`) asserts the disclosure is closed, not just the text.

But "focus a row first, by design" removed the only keyboard route to a row in `test_p_moves` (the old `j` press at 6e880e6^). The suite gained no test for the rule that replaced it. Each keyboard test now starts with a programmatic `.focus()`. Mutants A and B survive 87 passing tests. So the T-060 rule (conftest.py:46) is documented but not enforced, and the keyboard-only path is not exercised. Those are findings 1 and 2.

## Findings

1. **major: nothing tests that letter keys are inert outside an item row.** Evidence: mutA (`review.js:311`) and mutB (`sidebyside.js:102`) each fail the probe and pass the six keyboard files (`artifacts/review-evidence/T-119/mutA-keyboard-files.txt`, `mutB-keyboard-files.txt`). Contract at `tests/e2e/conftest.py:46`. Why it matters: a regression that re-enables shortcuts from the body or Export breaks WCAG 2.1.4 and passes CI. Fix: add the probe's body-key test as a permanent E2E, covering body, Export, header and dialog focus with a/d/j/k/p/o/e/r. Acceptance: it passes on 288affc and fails on both mutants.

2. **major: no e2e reaches a row by Tab, so R-RV-4 is unproven.** Evidence: `test_side_by_side.py:61` `.focus()` followed by `:62` `keyboard.press("p")`; `test_keyboard_mobile.py:9` docstring says "Tab to the first queue item", and `:10` calls `.focus()`; no `keyboard.press("Tab")` anywhere in `tests/e2e`. Spec `spec/REQUIREMENTS.md:95`: "E2E completes the sample case by keyboard only." Probe: Tab reaches a row after 20 presses and `a` accepts (passes). So the product works, but the suite does not check it. Why it matters: the card traded the only keyboard route in `test_p_moves` for a programmatic focus, and the spec's verification method is still missing. Fix: add a Tab-only E2E from page load to an item row, no `.focus()`, then `a`, and correct the `test_keyboard_mobile.py:9` docstring. Acceptance: the probe's Tab test passes as a permanent test on HEAD.

3. **minor: stale contract docstring.** Evidence: `tests/e2e/conftest.py:45` still quotes "AI suggested a flag that the second check did not confirm; it is not in the letter." The same file's line 51, `app/frontend/timeline.js:135` and `test_suggestions.py:225` use the T-060 sentence. Why: the conftest is the declared DATA-TESTID contract, and it now contradicts the test and product. Fix: update line 45. Acceptance: `grep -n "did not confirm; it is not in the letter" tests/e2e/conftest.py` returns nothing; `pytest tests/unit/test_e2e_contract.py` still passes (it did not catch this drift).

4. **minor: one-shot `inner_text()` read remains.** Evidence: `tests/e2e/test_stepper.py:204` reads `judge-summary-counts` with `inner_text()` after waiting only for `judge-summary`. T-115 flagged the same pattern at :204 and :257, and this card fixed only :257. Not reproduced: 5 of 5 runs of the judge-panel tests passed (`repeat-judge.txt`). Why: a race is still possible, and it sits in a live test. Fix: `expect(...).to_have_text(re.compile(r"\d+ checked, \d+ agreed with the draft, 3 questioned"))`. Acceptance: no `inner_text()` read follows a parent `wait_for` in `test_stepper.py`.

5. **minor: the only skip hides the ADR-005 path.** Evidence: `tests/e2e/test_ladder_gate.py:37`. Pre-existing and outside the 6e880e6 diff. Why: the 409 `item_rejected` check never runs on the curated fixture. Fix: seed a rejected item in the fixture, or convert to a strict xfail with a card. Acceptance: the e2e run reports 0 skips, or the skip becomes a strict xfail.

## What is right

- Pinned-HEAD e2e reproduces the card: 172 pass, 1 skip (ladder gate), 1 strict xfail (T-117), 0 failures.
- The judge-count fix is a real strengthening (retrying expect instead of a snapshot), and the tray-why check verifies placement, not only the text.
- The product's row gate is real and matches T-060: `review.js:307-311`, `sidebyside.js:102`, `batch.js:124-127`. Tab reaches rows (probe).

## Limits

Outside my lens: UX wording of the tray-flag sentence (I checked only that the test, product and T-096 copy agree). I did not run the full `tests/unit` suite; this card changes only `tests/e2e`.

```json
{"card": "T-119", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 6e880e6 (tests/e2e/test_side_by_side.py, test_stepper.py, test_suggestions.py); pinned git archive of HEAD 288affc (no app/ or tests/e2e change after 6e880e6); own fixture server 127.0.0.1:7972 and 7973 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB in scratch), all stopped",
 "exercised": [
  "read personas/staff-engineer.md, board show T-119, git show 6e880e6 (tests/e2e diff), git show --stat 288affc, git diff --stat 6e880e6 288affc",
  "git archive 288affc into scratch T119_staff_r1/archive (1977 files, equal to git ls-tree count)",
  "pytest tests/e2e -p no:cacheprovider -q -rsxX with E2E_BASE_URL=127.0.0.1:7972 and ZLAYT_DB exported: 172 passed, 1 skipped (tests/e2e/test_ladder_gate.py:37), 1 xfailed (test_stepper.py:220, T-117); 174 collected",
  "changed files x2 (test_side_by_side.py, test_stepper.py, test_suggestions.py) on 7973: 50 passed, 1 xfailed each run",
  "judge-panel stepper tests x5 on 7973: 3 passed each run",
  "tests/unit/test_e2e_contract.py: 3 passed",
  "scratch probe tests/e2e/probe_t119_keys.py on 288affc: Tab reaches an item row after 20 presses and a accepts (pass); body letter keys a/d/j/p change nothing (pass)",
  "mutA (review.js:311 letter keys fall back to the first row): probe fails; six keyboard files 87 passed, 1 xfailed",
  "mutB (sidebyside.js:102 p without row gate): probe fails; six keyboard files 87 passed, 1 xfailed",
  "greps: keyboard.press sites, inner_text reads, ZLAYT_DB skip sites, pytest.skip, tray-flag copy in timeline.js:135, conftest.py:45/51, board/cards/T-096.md:39, spec/REQUIREMENTS.md:95",
  "stopped every scratch server by PID; ports 7971-7975 verified closed",
  "evidence copied to artifacts/review-evidence/T-119/ (e2e-full.txt, repeat-judge.txt, mutA-keyboard-files.txt, mutB-keyboard-files.txt, probe_t119_keys.py, mutate.py)"
 ],
 "verdict": "changes",
 "scores": {"e2e_green_on_pinned_head": 5, "changed_test_assertion_strength": 4, "keyboard_rule_negative_coverage": 2, "keyboard_reachability_coverage": 2, "skip_and_env_hygiene": 4, "repeatability": 4},
 "findings": [
  {"severity": "major", "title": "No e2e test proves letter keys are inert outside an item row (WCAG 2.1.4 rule untested)",
   "evidence": "mutA: app/frontend/review.js:311 `const row = RV.itemRowOf(t) || document.querySelector(\"[data-item-id]\");` -> probe test_probe_letter_keys_from_body_do_nothing FAILS ('key a changed a decision from the body'); mutB: app/frontend/sidebyside.js:102 without `&& ZL.rv.itemRowOf(t)` -> FAILS ('key p moved focus from the body to DIV'); six keyboard files pass 87 / xfail 1 on both mutants (artifacts/review-evidence/T-119/mutA-keyboard-files.txt, mutB-keyboard-files.txt); rule stated at tests/e2e/conftest.py:46",
   "why_it_matters": "A regression that re-enables shortcuts from the body, Export or the header breaks WCAG 2.1.4 and passes the suite. T-119 removed the j-from-body route and added no negative test in its place.",
   "fix": "Make the probe's body-key test permanent (e.g. in tests/e2e/test_keyboard_mobile.py): from body, Export, header and an open dialog, a d j k p o e r do nothing and focus stays put.",
   "acceptance_test": "The new E2E passes on HEAD 288affc and fails on both mutA and mutB (scratch copies in artifacts/review-evidence/T-119/)."},
  {"severity": "major", "title": "No e2e reaches a row by Tab; spec R-RV-4 keyboard-only E2E is not implemented",
   "evidence": "tests/e2e/test_side_by_side.py:61 `.focus()` then :62 `keyboard.press(\"p\")`; tests/e2e/test_keyboard_mobile.py:9 docstring 'Tab to the first queue item' with :10 `.focus()`; no keyboard.press(\"Tab\") in tests/e2e; spec/REQUIREMENTS.md:95 'E2E completes the sample case by keyboard only'; probe: Tab reaches a row after 20 presses and a accepts (pass)",
   "why_it_matters": "The card replaced the only keyboard route to a row in test_p_moves with a programmatic focus, and the spec's keyboard-only verification is still absent. The product path works, but nothing checks it.",
   "fix": "Add a Tab-only E2E from page load to the first item row (no .focus()), press a, and assert the accept. Correct the test_keyboard_mobile.py:9 docstring if it stays on focus().",
   "acceptance_test": "The Tab-only E2E passes on HEAD 288affc with no .focus() call on its path; probe test_probe_tab_reaches_a_row_then_a_accepts is the reference."},
  {"severity": "minor", "title": "Stale tray-flag copy in the E2E data-testid contract",
   "evidence": "tests/e2e/conftest.py:45 quotes 'AI suggested a flag that the second check did not confirm; it is not in the letter.'; conftest.py:51, app/frontend/timeline.js:135 and tests/e2e/test_suggestions.py:225 use 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.'",
   "why_it_matters": "The conftest is the declared contract for the frontend hooks and now contradicts the product and the test. tests/unit/test_e2e_contract.py passes regardless.",
   "fix": "Update conftest.py:45 to the T-060 sentence.",
   "acceptance_test": "grep -n 'did not confirm; it is not in the letter' tests/e2e/conftest.py returns nothing; pytest tests/unit/test_e2e_contract.py passes."},
  {"severity": "minor", "title": "One-shot inner_text() read after a parent wait remains (T-115 pattern, :204 not fixed)",
   "evidence": "tests/e2e/test_stepper.py:204 `assert re.search(..., jp.get_by_test_id(\"judge-summary-counts\").inner_text())` after `jp.get_by_test_id(\"judge-summary\").wait_for()` at :202; T-115 flagged :204 and :257; T-119 fixed only :257 (test_stepper.py:257 now expect(...).to_have_text). Not reproduced: 5/5 judge-panel runs passed (artifacts/review-evidence/T-119/repeat-judge.txt).",
   "why_it_matters": "The race that T-115 saw can still fail the live test test_judge_panel_collapsed_summary_and_labels.",
   "fix": "Replace with expect(jp.get_by_test_id('judge-summary-counts')).to_have_text(re.compile(r'\\d+ checked, \\d+ agreed with the draft, 3 questioned')).",
   "acceptance_test": "No inner_text() read follows a parent wait_for for judge-summary-counts in tests/e2e/test_stepper.py; the test passes 10 consecutive runs."},
  {"severity": "minor", "title": "The only e2e skip hides the ADR-005 rejected-item 409 path",
   "evidence": "tests/e2e/test_ladder_gate.py:37 `if not rej: pytest.skip(\"no rejected item in the sample fixture run\")`; full run reports 1 skipped for this test. Pre-existing, outside the 6e880e6 diff.",
   "why_it_matters": "On the curated fixture the 409 item_rejected behaviour never runs in e2e; the skip is green in the summary.",
   "fix": "Seed one rejected item in the curated fixture, or convert to a strict xfail that names a card.",
   "acceptance_test": "The e2e run shows 0 skipped, or the test reports as a strict xfail with a card number."}
 ],
 "whats_right": [
  "Pinned-HEAD full e2e reproduces the card: 172 passed, 1 skipped (ladder gate), 1 strict xfail (T-117), 0 failed.",
  "The judge-count fix is a real strengthening (retrying expect instead of a snapshot) and the tray-why check asserts placement, not only the text.",
  "The product row gate is real and matches T-060 (review.js:307-311, sidebyside.js:102, batch.js:124-127); Tab reaches rows in the probe."
 ],
 "questions_for_chris": ["Is the WCAG 2.1.4 row-only shortcut rule a must-have for the M3 gate under the T-060 AC? I treated it as one, which is why findings 1 and 2 are major."]}
```
