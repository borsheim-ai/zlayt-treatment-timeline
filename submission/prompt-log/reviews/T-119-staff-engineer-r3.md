# T-119 review, round 3: staff-engineer-reviewer

**Verdict: pass.** No blocker, no major. The round-2 major is closed: `test_p_focuses_the_record_pane_only_from_an_item_row` fails on mutant B (`sidebyside.js:102` row gate removed) and passes on HEAD. The round-2 flake fix is partial: `vis()` now exits at the first frame the box is in the viewport, not at a settled position, and the card's five-run full-suite acceptance is not evidenced. Three minors and two nits remain (below). Pinned to `c559ce2`; HEAD has moved since (now `433ac1c`), and I did not review the later commits.

## What I ran

Pin: `git rev-parse HEAD` returned `c559ce20ffbdcac8d4ad17b3c78f9ff0786c12a7` when I started; `git merge-base --is-ancestor c559ce2 HEAD` succeeded. Archive `git archive c559ce2` into scratch `T119_r3/head`: 2038 files, equal to `git ls-tree -r c559ce2 | wc -l` (2038). A second archive `T119_r3/pin_c559` is `diff -rq`-identical to it.

- Mutant B (scratch copy `T119_r3/mutB`, script `T119_r3/scripts/mutB.py` run with `-I`): replaces `&& ZL.rv && ZL.rv.itemRowOf(t)` on `app/frontend/sidebyside.js:102` with nothing. `diff -u` shows that one-line change only.
- New test on HEAD (port 7995): `1 passed in 1.77s`.
- New test on mutB (port 7996): `FAILED test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row`, `AssertionError: p moved focus from the page body: BODY: -> DIV:sbs-body`, at `test_polish_r3.py:117`. Result for the file: `1 failed, 18 passed`.
- `tests/e2e/test_polish_r3.py` on HEAD: `19 passed in 23.91s`.
- `tests/e2e/test_code_check_refusal.py` run five times on HEAD: `23 passed in 36.07s`, `34.75s`, `34.19s`, `35.19s`, `34.04s` (exit 0 each; logs in `T119_r3/refusal-run{1..5}.txt`).
- Full `tests/e2e` on HEAD, one run: `206 passed, 1 skipped in 279.26s`; the skip is `test_ladder_gate.py:37`. `--collect-only` gives 207.
- Reconciling the card artifact: `artifacts/t119-r3-e2e-full.txt` reports `192 passed, 1 skipped` and records no commit. `git archive d56328a` collects 192, so the artifact probably came from an older tree. It does not reproduce on `c559ce2`.
- Greps at `c559ce2`: `time.sleep` appears only at `test_polish_r3.py:21` (a capped `/status` poll, pre-existing); no `sleep(` or `wait_for_timeout` in `test_code_check_refusal.py`; `git show c559ce2:tests/e2e/conftest.py | grep -c "did not confirm; it is not in the letter"` returns 0. `git log -S` puts that removal in `e293daa`, not in `c559ce2` as the handoff says.
- Read at `c559ce2`: `test_code_check_refusal.py:93-102` (vis) and `:117-118` (call site and the 140 px check); `test_polish_r3.py:105-122`; `sidebyside.js:96` (early return for INPUT, TEXTAREA, SELECT) and `:102`; `test_keyboard_mobile.py:9`; `test_stepper.py:204`; `test_ladder_gate.py:37`; `conftest.py:47,53`.
- Ports: my fixture servers were PID 5290 (7995) and 6354 (7996). I first killed PID 6353, which is the PID I had recorded for the 7996 server. It turned out to be a bash wrapper, not the server, and I killed it in error. The listener, 6354, is the `Python -m app.main` process; I then stopped it. `lsof -iTCP:7995 -sTCP:LISTEN` and `lsof -iTCP:7996 -sTCP:LISTEN` both return nothing.

Evidence is under the scratch directory `T119_r3/` (`refusal-run*.txt`, `full-head-run1.txt`, `scripts/mutB.py`). Copies are not in `artifacts/review-evidence/` because I did not change the repo.

## Round-2 status

- r2 major, p gate untested: **closed.** The new test kills mutB and passes on HEAD. The shape differs from the r2 suggestion (a separate test, not an added key in the list), which is fine because the acceptance is met.
- r2 minor, vis flake: **partly closed.** Finding 1.
- r2 minor, stale tray copy: **closed at HEAD** (`e293daa`). The handoff's attribution to `c559ce2` is wrong, which is a note, not a finding.
- r2 nit, `test_keyboard_mobile.py:9` docstring: **closed.**
- r1 minor 4, `inner_text` at `test_stepper.py:204`: **closed.** It is now a retrying `expect`.
- r1 minor 5, the only skip hides the ADR-005 path: **open.** Finding 3.

## Findings

1. **minor: `vis()` stops at the first in-viewport frame, and the flake acceptance is not evidenced.** Evidence: `test_code_check_refusal.py:100` returns True on the first frame where the box is inside the viewport; `:101` polls rAF; `:102` returns False after 120 frames. The call at `:117` is the only positive assertion that uses it. The round-2 fix asked for a wait "until the scroll settles". This returns as soon as the box is in the viewport once, so the assertion means "visible at some frame within about 2 s", not "on screen at rest". The one-shot check at `:118` still reads boxes after the poll. A permanently off-screen box still fails after the loop exhausts, so regression coverage holds for that case. The round-2 flake was seen once in two full runs; this review has one full run (206 passed), so the five-run acceptance is not met. Why it matters: a box that enters and leaves the viewport now passes, and the card's "full e2e green" claim rests on one run. Fix: return True only after two consecutive frames with the same box inside the viewport. Acceptance: five consecutive full `tests/e2e` runs on the pinned tree are green, and a mutant that pushes the reason box below the fold still fails at `:117`.

2. **minor: the card's full-run artifact cannot be tied to a commit and does not reproduce.** Evidence: `artifacts/t119-r3-e2e-full.txt` shows `192 passed, 1 skipped in 255.42s` and 193 progress marks, with no sha. On the archive of `c559ce2`, `pytest tests/e2e --collect-only -q` gives `207 tests collected`, and the full run gives `206 passed, 1 skipped in 279.26s`. The nearest tree I checked, `d56328a`, collects 192. Why it matters: the AC cites this file as proof, and a reviewer cannot reproduce its count. Fix: regenerate the file from a stated sha and include the collected count. Acceptance: the file names `c559ce2` and its numbers match a fresh `--collect-only` and run on that sha.

3. **minor (carried from r1): the only e2e skip hides the ADR-005 rejected-item path.** Evidence: `tests/e2e/test_ladder_gate.py:37`, `if not rej: pytest.skip("no rejected item in the sample fixture run")`; the full run prints `SKIPPED [1] tests/e2e/test_ladder_gate.py:37`. Why it matters: the 409 path never runs in the suite. Fix: seed one rejected item in the curated fixture, or convert to a strict xfail that names a card. Acceptance: the full run reports zero skips, or the xfail names a card.

4. **nit: the p test's docstring says "an input", but its loop presses btn-export, btn-shortcuts and sort.** Evidence: `test_polish_r3.py:106` (docstring), `:118` (loop). `sort` is a SELECT, and `sidebyside.js:96` returns early for SELECT, so that step never reaches the p gate. Fix: reword to "a select" or add a text field. Acceptance: docstring matches the presses.

5. **nit: `vis()` has no timeout on its rAF evaluate.** Evidence: `test_code_check_refusal.py:101`. The archive root has no `pytest.ini`, `pyproject.toml`, `setup.cfg` or `tox.ini`, so no timeout applies. If rAF never fires, the test hangs rather than fails. Fix: use `page.wait_for_function` with a timeout, or add an explicit deadline. Acceptance: a test with rAF stopped fails within the timeout.

## What is right

- The new p test names the focus move in its failure message, so a regression reads as `BODY: -> DIV:sbs-body`, and it passes on HEAD (19/19 in the polish file).
- `vis()` has no wall-clock sleep and a fixed frame budget, and both call sites are positive assertions, so a box that never comes into view still fails.
- The stale tray copy and the keyboard docstring are fixed at HEAD, and `test_code_check_refusal.py` passed 23/23 on each of five runs.

## Limits

Outside my lens: the wording of the shortcut sheet and the notices. I did not run `tests/unit`; the card changes only `tests/e2e`.

```json
{"card": "T-119", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit c559ce2 (tests/e2e/test_polish_r3.py, tests/e2e/test_code_check_refusal.py, tests/e2e/test_keyboard_mobile.py, artifacts/t119-r3-e2e-full.txt, artifacts/t119-r3-mutB.txt); pinned git archive of c559ce2 (2038 files, identical to a second archive); fixture servers 127.0.0.1:7995 (HEAD archive) and 127.0.0.1:7996 (mutB archive), both stopped; HEAD has since moved to 433ac1c and was not reviewed",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-119-staff-engineer-r2.md, board show T-119, memory project_t119_keyboard_coverage_patterns.md",
  "git rev-parse HEAD (c559ce2 at pin time), git merge-base --is-ancestor c559ce2 HEAD, git show --stat and git show c559ce2 for the five changed files",
  "git archive c559ce2 into scratch T119_r3/head (2038 files = git ls-tree count); second archive T119_r3/pin_c559, diff -rq identical",
  "mutB: scratch copy T119_r3/mutB, scripts/mutB.py (run with -I) removes ' && ZL.rv && ZL.rv.itemRowOf(t)' at app/frontend/sidebyside.js:102; diff -u shows the one-line change",
  "pytest tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row on HEAD: 1 passed in 1.77s",
  "same test on mutB: FAILED at test_polish_r3.py:117 'p moved focus from the page body: BODY: -> DIV:sbs-body'",
  "pytest tests/e2e/test_polish_r3.py on HEAD: 19 passed in 23.91s; on mutB: 1 failed, 18 passed in 24.09s",
  "pytest tests/e2e/test_code_check_refusal.py five times on HEAD: 23 passed each (36.07s, 34.75s, 34.19s, 35.19s, 34.04s); logs in T119_r3/refusal-run1..5.txt",
  "pytest tests/e2e full on HEAD, one run: 206 passed, 1 skipped in 279.26s (skip at test_ladder_gate.py:37); --collect-only 207",
  "pytest tests/e2e --collect-only on git archive d56328a: 192 collected (to reconcile artifacts/t119-r3-e2e-full.txt, which reports 192 passed, 1 skipped)",
  "greps at c559ce2: time.sleep only at test_polish_r3.py:21; no sleep( or wait_for_timeout in test_code_check_refusal.py; git show c559ce2:tests/e2e/conftest.py | grep -c old tray sentence = 0; git log -S shows the removal in e293daa",
  "read at c559ce2: test_code_check_refusal.py:93-102 and :117-118; test_polish_r3.py:105-122; sidebyside.js:96 and :102; test_keyboard_mobile.py:9; test_stepper.py:204; test_ladder_gate.py:37; conftest.py:47 and :53",
  "stopped my own servers: PID 5290 (7995) and PID 6354 (7996 listener); PID 6353 (a recorded wrapper, not the server) was killed in error first; lsof shows ports 7995 and 7996 closed"
 ],
 "verdict": "pass",
 "scores": {"e2e_green_on_pinned_head": 4, "negative_key_rule_coverage": 5, "keyboard_reachability_coverage": 5, "flake_resistance": 4, "round1_minors_closed": 4},
 "findings": [
  {"severity": "minor", "title": "vis() stops at the first in-viewport frame; the flake fix and its five-run acceptance are not evidenced",
   "evidence": "tests/e2e/test_code_check_refusal.py:100 (return True on first in-viewport frame), :101 (rAF poll), :102 (return False after 120 frames), :117 (positive call), :118 (one-shot 140 px read after the poll); r2 flake observed once in two full runs (r2-e2e-full-run1.txt); this review: one full run 206 passed",
   "why_it_matters": "A box that enters and leaves the viewport now passes, so the assertion means visible at some frame, not on screen at rest. The card's full-e2e-green claim rests on one run here and the round-2 acceptance asked for five.",
   "fix": "Return True only after two consecutive frames with the same box fully inside the viewport, then keep the 140 px check.",
   "acceptance_test": "Five consecutive full tests/e2e runs on the pinned tree are green, and a mutant that pushes the accept-refused box below the fold still fails at test_code_check_refusal.py:117."},
  {"severity": "minor", "title": "artifacts/t119-r3-e2e-full.txt records no commit and does not reproduce on c559ce2",
   "evidence": "artifacts/t119-r3-e2e-full.txt: '192 passed, 1 skipped in 255.42s' with 193 progress marks and no sha; on the c559ce2 archive, --collect-only gives 207 and the full run gives '206 passed, 1 skipped in 279.26s'; git archive d56328a collects 192",
   "why_it_matters": "The AC cites this file as proof of full e2e green on a clean HEAD, and a reviewer cannot tie its count to a tree.",
   "fix": "Regenerate the file from a stated sha with the collected count in it.",
   "acceptance_test": "The artifact names c559ce2 (or its successor) and its numbers match a fresh --collect-only and full run on that sha."},
  {"severity": "minor", "title": "The only e2e skip hides the ADR-005 rejected-item 409 path (carried from r1)",
   "evidence": "tests/e2e/test_ladder_gate.py:37: if not rej: pytest.skip('no rejected item in the sample fixture run'); full run prints SKIPPED [1] tests/e2e/test_ladder_gate.py:37",
   "why_it_matters": "The 409 path for a rejected item never runs in the suite, so a regression there passes CI.",
   "fix": "Seed one rejected item in the curated fixture, or convert to a strict xfail that names a card.",
   "acceptance_test": "The full run reports zero skips, or the xfail names a card and fails loudly if the path starts to work."},
  {"severity": "nit", "title": "The p test docstring says 'an input' but the loop presses btn-export, btn-shortcuts and sort (a SELECT)",
   "evidence": "tests/e2e/test_polish_r3.py:106 (docstring), :118 (for tid in ('btn-export', 'btn-shortcuts', 'sort')); app/frontend/sidebyside.js:96 returns early for SELECT, so the sort step never reaches the p gate",
   "why_it_matters": "The docstring overstates what the test covers; the p gate itself is exercised by the body step and the Export and shortcuts steps.",
   "fix": "Reword to 'a select', or add a text field to the loop.",
   "acceptance_test": "The docstring matches the controls pressed."},
  {"severity": "nit", "title": "vis() waits on requestAnimationFrame with no timeout",
   "evidence": "tests/e2e/test_code_check_refusal.py:101; no pytest.ini, pyproject.toml, setup.cfg or tox.ini at the archive root",
   "why_it_matters": "If rAF never fires (for example a hidden page), the test hangs instead of failing.",
   "fix": "Use page.wait_for_function with a timeout, or add an explicit deadline.",
   "acceptance_test": "A test with rAF stopped fails within the timeout instead of hanging."}
 ],
 "whats_right": [
  "The new p test names the focus move in its failure message and passes on HEAD (19/19 in test_polish_r3.py); mutB fails it at test_polish_r3.py:117.",
  "vis() has no wall-clock sleep and a fixed frame budget, and both call sites are positive assertions, so a box that never comes into view still fails.",
  "The stale tray copy and the keyboard docstring are fixed at HEAD, and test_code_check_refusal.py passed 23/23 on each of five runs."
 ],
 "questions_for_chris": []}
```
