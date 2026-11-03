# T-119 review, round 2: staff-engineer-reviewer

**Verdict: changes.** No blocker. Of the two round-1 majors, the Tab/Enter/Space-only R-RV-4 test is fixed and kills its mutants. The row-only key test is mostly fixed: it kills four of five scratch mutants, but the `p` gate (`app/frontend/sidebyside.js:102`) is still untested. That was the round-1 mutB, whose acceptance test said the new E2E "fails on both mutants". Three round-1 minors are unchanged.

## What I ran

- Pinned to `git archive e1ce8dc` (HEAD when I started: `e1ce8dc620e6ec0778320456ac79a25f1832bfee`; card commit d9efc5c). Archive file count 1979 equals `git ls-tree -r HEAD`. HEAD later moved to c26ff04; `git diff --stat e1ce8dc HEAD -- app/frontend tests/e2e` shows only a two-line `tests/e2e/conftest.py` comment change (d56328a), so the pin still holds.
- Own fixture server on 127.0.0.1:7991 (`LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch>`). Both servers (7991, 7992) stopped by PID; ports verified closed.
- `tests/e2e/test_polish_r3.py`: **18 passed** in 23.6s.
- Full `tests/e2e`, run twice. Run 1: **1 failed, 190 passed, 1 skipped** in 253s; the failure was `test_code_check_refusal.py:110` (`vis(...)` "the reason must be on screen beside the button"). Run 2: **191 passed, 1 skipped** in 253s. The failing file then passed 3 of 3 isolated runs (23 passed each). The handoff's 176 passed + 16 skipped = 192 equals my 191 + 1 skipped = 192 collected; the 15 extra skips are the ZLAYT_DB gates, which I set.
- Mutants on a second scratch copy (own port 7992 and sqlite), control green (18 passed) before and after each swap:
  - A, `review.js` letter keys fall back to the first row (`const row = RV.itemRowOf(t) || document.querySelector("[data-item-id]")`): **killed**, `test_letter_keys_do_nothing_from_body_export_or_an_input` fails.
  - B, `sidebyside.js:102` `p` without `ZL.rv.itemRowOf(t)`: **survived 18 of 18, and survived 129 of 129** across all 8 e2e files that press keys (`test_code_check_refusal, test_keyboard_mobile, test_input, test_rerun_judge, test_suggestions, test_polish_r3, test_stepper, test_side_by_side`).
  - C, `batch.js` Shift+A without the row gate: **killed**, same test.
  - D, `review.js` `typing(t)` exemption removed: **killed**, same test (the `jadA` typed-not-run assertion).
  - E, `review.js` dialog-open swallow removed: **killed**, `test_letter_key_with_a_window_open_says_so`.
- Probe (scratch, `artifacts/review-evidence/T-119/r2-probe_p.py`): select an item so the pane is on, blur to body, press `p`. Unmutated HEAD: passes (focus stays). Mutant B: fails with `p moved focus from the body: BODY: -> DIV:sbs-body`. So B has a real effect that no committed test sees.
- Read `tests/e2e/test_polish_r3.py` in full, the `test_stepper.py:204` retry, `review.js:309-345`, `sidebyside.js:98-106`, `batch.js:124-128`. Greps for `sleep(`, `wait_for_timeout`, `keyboard.press("Tab")`, `inner_text()` after a parent wait, `pytest.skip`, and the stale tray copy in `conftest.py`.
- Evidence in `artifacts/review-evidence/T-119/`: `r2-e2e-full-run1.txt`, `r2-e2e-full-run2.txt`, `r2-mutants-polish.txt`, `r2-probe_p.py`, `r2-mut.py`.

## Judgement of the new tests

- **Negative key test** (`test_polish_r3.py:74-102`): asserts decision count, open dialogs and typed text (not implementation). It drives j, a, d, Shift+A and `?` from the body, from Export, from the edit textarea and from the sort control. The "active" field in `_snapshot` compares the snapshot to itself, so it proves nothing, but the next line (`closest('[data-item-id]')` is falsy) does check that focus did not enter a row. Real, mutation-tested for decision keys. Gap: `p` (and `k o e r` only through the shared gate, which mutant A covers) and the header; `p` has its own gate and is not pressed.
- **Dialog case** (`:105-111`): `o` then `a`, expects the "Press Escape" notice and zero accepted. Killed mutant E.
- **Tab/Enter/Space-only flow** (`:115-143`): no `.focus()` on the path; `tab_until` raises if the target is never reached, so a lost skip link, a lost tab stop or a swallowed Enter fails it. It asserts the real outcome (`data-review="dismissed"`, `export-letter` visible, `copy-confirm`, then `Copied the treatment section`). Setup accepts go through the API, which is fine for a keyboard test of one item plus export. It covers one item, not "the sample case", so R-RV-4 is met in kind, not in full; I rate that as a note, not a finding.
- **Determinism:** no `wait_for_timeout`. The one `time.sleep(.5)` (`:21`) is a bounded `/status` poll for the run to reach `ready` (150 s cap, asserts `ready`), the same helper pattern as `test_stepper.py:17`. Assertions after UI actions use `expect(...)` retries. No wall clock, no network beyond the local fixture server.
- **`test_stepper.py:204`:** now `expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(...))`, a retrying assert. Round-1 minor 4 is fixed. No `inner_text()` follows a parent `wait_for` for that testid.

## Round-1 minors

- Minor 3 (stale tray-flag copy): **not fixed.** `tests/e2e/conftest.py:45` still says "AI suggested a flag that the second check did not confirm; it is not in the letter."
- Minor 4 (`inner_text` at :204): **fixed**, see above.
- Minor 5 (the only skip hides ADR-005): **unchanged.** `tests/e2e/test_ladder_gate.py:37` still skips; it is the one skip in both full runs. Pre-existing and not in the T-119 diff.
- Docstring from round-1 finding 2: `tests/e2e/test_keyboard_mobile.py:9` still says "Tab to the first queue item" and `:10` calls `.focus()`. The Tab test now exists elsewhere, so this is a misleading comment only.

## Findings

1. **major: the `p` gate is untested; the new negative test does not fail on round-1 mutB.** Evidence: mutant B (`app/frontend/sidebyside.js:102`, `&& ZL.rv && ZL.rv.itemRowOf(t)` removed) gives 18 passed on `test_polish_r3.py` and 129 passed across the 8 keyboard files (`r2-mutants-polish.txt`); the probe fails on it with `p moved focus from the body: BODY: -> DIV:sbs-body`. The test presses only `j a d Shift+A ?` (`test_polish_r3.py:79,85,93,100`). Round-1 finding 1 asked for a d j k p o e r and its acceptance said it fails on both mutants. Why it matters: `p` is a single-character shortcut that acts from the page body and Export, which is the WCAG 2.1.4 rule T-060 made a blocker; it can regress without CI noticing. Fix: add `p` to the key lists in `test_letter_keys_do_nothing_from_body_export_or_an_input`, after first putting an item in the pane (focus a row, press `p`, Escape, then blur) so the pane is visible; assert focus stays on body or Export. Acceptance: the test passes on HEAD and fails on mutant B (`r2-probe_p.py` is the reference).

2. **minor: full-suite flake in `test_code_check_refusal.py:110`.** Evidence: run 1 failed `test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action` with "the reason must be on screen beside the button, not below the fold"; run 2 passed; the file alone passed 3 of 3. `vis()` (`:93-95`) reads `bounding_box()` once, after `expect(...).to_be_visible()`, against the viewport. This is a one-shot layout read after a click. File is outside the T-119 diff, but the card's AC says "full e2e green". Fix: wait for scroll to settle before the check, e.g. `expect` on a stable box position, or poll `vis` with a retrying assertion. Acceptance: 5 consecutive full-suite runs without this failure.

3. **minor: stale tray-flag copy still in the E2E contract (round-1 minor, unchanged).** Evidence: `tests/e2e/conftest.py:45`. Fix: use the T-060 sentence from `app/frontend/timeline.js:135`. Acceptance: `grep -n "did not confirm; it is not in the letter" tests/e2e/conftest.py` returns nothing.

4. **nit: misleading docstring.** `tests/e2e/test_keyboard_mobile.py:9-10` says "Tab to the first queue item" while calling `.focus()`. Fix: reword to "focus the first item" or point to `test_polish_r3.py`.

## What is right

- The Tab/Enter/Space-only test is genuine keyboard reach with no `.focus()` and real end-state assertions.
- The negative key test kills four of five gate mutants, including the typing exemption and the dialog swallow.
- `test_stepper.py:204` now uses a retrying `expect`; the polish file has no fixed sleeps in UI waits.

## Limits

Outside my lens: UX wording of the shortcut sheet and notices. I did not run `tests/unit`; the card changes only `tests/e2e`.

```json
{"card": "T-119", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit d9efc5c (tests/e2e/test_polish_r3.py, conftest.py) and the test_stepper.py:204 retry; pinned git archive of HEAD e1ce8dc (later HEAD c26ff04 changes only a two-line tests/e2e/conftest.py comment); own fixture servers 127.0.0.1:7991 and 7992 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB in scratch), both stopped by PID",
 "exercised": [
  "read personas/staff-engineer.md, board show T-119, reviews/T-119-staff-engineer.md, git show --stat d9efc5c, git diff --stat d9efc5c HEAD for app/frontend and tests/e2e",
  "git archive e1ce8dc into scratch T119_r2/archive (1979 files, equal to git ls-tree count)",
  "pytest tests/e2e/test_polish_r3.py: 18 passed",
  "pytest tests/e2e full, run 1: 1 failed (test_code_check_refusal.py:110 vis check), 190 passed, 1 skipped (test_ladder_gate.py:37); run 2: 191 passed, 1 skipped",
  "pytest tests/e2e/test_code_check_refusal.py alone x3: 23 passed each",
  "mutants A, B, C, D, E on a scratch copy with control green: polish file kills A, C, D, E; B survives 18/18",
  "mutant B across the 8 e2e files that press keys: 129 passed (survives)",
  "scratch probe r2-probe_p.py: passes on unmutated, fails on mutant B with 'p moved focus from the body: BODY: -> DIV:sbs-body'",
  "read review.js:309-345, sidebyside.js:98-106, batch.js:124-128, test_stepper.py:196-215, test_keyboard_mobile.py:1-20",
  "greps: sleep(, wait_for_timeout, keyboard.press(Tab), inner_text(), pytest.skip, conftest.py stale tray copy, xfail",
  "stopped scratch servers by PID (52563, 59175); ports 7991 and 7992 verified closed",
  "evidence copied to artifacts/review-evidence/T-119/ (r2-e2e-full-run1.txt, r2-e2e-full-run2.txt, r2-mutants-polish.txt, r2-probe_p.py, r2-mut.py)"
 ],
 "verdict": "changes",
 "scores": {"e2e_green_on_pinned_head": 4, "negative_key_rule_coverage": 3, "keyboard_reachability_coverage": 5, "flake_resistance": 4, "round1_minors_closed": 2},
 "findings": [
  {"severity": "major", "title": "The p gate is untested; the new negative key test does not fail on round-1 mutB",
   "evidence": "mutant B (app/frontend/sidebyside.js:102, '&& ZL.rv && ZL.rv.itemRowOf(t)' removed): test_polish_r3.py 18 passed, 8 keyboard files 129 passed (artifacts/review-evidence/T-119/r2-mutants-polish.txt); probe r2-probe_p.py fails with 'p moved focus from the body: BODY: -> DIV:sbs-body'; the test presses only j a d Shift+A ? (tests/e2e/test_polish_r3.py:79,85,93,100)",
   "why_it_matters": "p is a single-character shortcut that must act only from an item row (WCAG 2.1.4, T-060 blocker). It can regress with all 129 keyboard tests green. Round-1 finding 1 named p and its acceptance test required failing on both mutants.",
   "fix": "Add p to the key lists in test_letter_keys_do_nothing_from_body_export_or_an_input after putting an item in the pane (focus a row, press p, Escape, blur), and assert focus stays on the body or Export.",
   "acceptance_test": "The test passes on HEAD and fails on mutant B; artifacts/review-evidence/T-119/r2-probe_p.py is the reference."},
  {"severity": "minor", "title": "Full-suite flake: one-shot bounding-box read in test_code_check_refusal.py:110",
   "evidence": "run 1 of tests/e2e failed test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action 'the reason must be on screen beside the button, not below the fold' (r2-e2e-full-run1.txt); run 2 passed (r2-e2e-full-run2.txt); file alone 23 passed x3; vis() at test_code_check_refusal.py:93-95 reads bounding_box() once",
   "why_it_matters": "The card AC says full e2e green; a one-shot layout read after a click fails intermittently under a full run. Outside the T-119 diff.",
   "fix": "Retry the position check until the scroll settles (poll vis, or use a retrying expect on a stable position).",
   "acceptance_test": "5 consecutive full tests/e2e runs without this failure."},
  {"severity": "minor", "title": "Stale tray-flag copy still in the E2E data-testid contract (round-1 minor, unchanged)",
   "evidence": "tests/e2e/conftest.py:45 quotes 'AI suggested a flag that the second check did not confirm; it is not in the letter.'; the product (app/frontend/timeline.js:135) and test_suggestions.py use the T-060 sentence",
   "why_it_matters": "The conftest is the declared contract for the frontend hooks and contradicts the product and the test.",
   "fix": "Update conftest.py:45 to the T-060 sentence.",
   "acceptance_test": "grep -n 'did not confirm; it is not in the letter' tests/e2e/conftest.py returns nothing."},
  {"severity": "nit", "title": "Misleading docstring in test_keyboard_mobile.py",
   "evidence": "tests/e2e/test_keyboard_mobile.py:9 'Tab to the first queue item' with :10 calling .focus()",
   "why_it_matters": "The docstring claims keyboard reach the test does not exercise; the real Tab test now lives in test_polish_r3.py.",
   "fix": "Reword to 'focus the first item' or point to test_polish_r3.py.",
   "acceptance_test": "The docstring no longer says Tab."}
 ],
 "whats_right": [
  "The Tab/Enter/Space-only test has no .focus() on its path and asserts real end states (dismissed row, export visible, copy confirmed).",
  "The negative key test kills four of five gate mutants (body fallback, Shift+A, typing exemption, dialog swallow).",
  "test_stepper.py:204 is a retrying expect, and test_polish_r3.py has no fixed sleeps in UI waits (one bounded status poll)."
 ],
 "questions_for_chris": []}
```
