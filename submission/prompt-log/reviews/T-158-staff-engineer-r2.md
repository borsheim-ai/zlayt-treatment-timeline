# T-158 review r2: refused-Accept reason box at 390x844 (staff-engineer-reviewer)

**This file supersedes `reviews/T-158-staff-engineer.md` (r1).** The r1 JSON verdict and findings stand. Three body statements in r1 were wrong and cannot be edited in place under the reviewer guard, so they are corrected here:

1. r1 said the file failed 4 of 23 in each of 10 runs "at 0b2ce9c and 83f1afd". I ran the 10 runs at 83f1afd (same frontend and tests as 0b2ce9c). At 0b2ce9c I ran only the batch DOM probe, which shows the same missing batch bar.
2. r1 said "40 probe runs". The count is 70 settle runs across seven variants (see finding 1).
3. r1's pytest rows for the one-shot and click-time copies were built on 83f1afd. The no-scroll copy in pytest was built on 83f1afd with the stray block removed. The table below names the base of each row.

**Pinned sha: f31b146.** It was HEAD when I archived it (2026-11-02 15:43 UTC) and the sha all runs below used. HEAD moved during the review: 83f1afd at start, then a7302fe, f31b146, and 9db2cec at 15:52 UTC. The 9db2cec change to frontend is one line in `RV.registerPanel` (f31b146 review.js:503), outside T-158's paths. The card commit is 0b2ce9c.

## Summary

Verdict: **changes** (two majors, no blocker at f31b146).

- At f31b146 `tests/e2e/test_code_check_refusal.py` passed 23/23 in each of 10 consecutive runs (E2E_REQUIRE_DB=1, private server per run). The 390x844 cases pass in every run, and the on-screen assertion (test:117) is unchanged from 0b2ce9c.
- The fix does not demonstrate the claim the card makes. "After layout settles" is not tested, and the 250 ms and 700 ms passes have no observed effect (finding 1).
- The card's AC evidence cannot be reproduced at its own commit (finding 2). At 83f1afd, which has no frontend or e2e diff from 0b2ce9c, the same file failed 4 of 23 in each of 10 runs. The file went green through 2de5ba9 (T-154 r3), not through this card.

Resolved during the review, not a finding against f31b146: a keydown guard that T-154 r2 (6379c0b) spliced into `mountSection()` threw `ReferenceError: key is not defined` (83f1afd:app/frontend/review.js:491). Every side panel after `flags` stopped mounting: the batch bar, the charges panel and the audit panel. The four batch tests failed on that. 2de5ba9 moved the guard into the keydown handler (f31b146:app/frontend/review.js:484), and the batch bar mounts again.

## Evidence summary

| Check | Result | Where |
|---|---|---|
| refusal file, 10 consecutive runs, f31b146 | 23 passed each, 0 failed | artifacts/review-evidence/T-158/f31b146-refusal-x10/ |
| refusal file, 10 consecutive runs, 83f1afd | 4 failed, 19 passed each (the four batch tests) | artifacts/review-evidence/T-158/83f1afd-refusal-x10/ |
| batch DOM probe, sample case, 1280x900 | 0b2ce9c and 83f1afd: no batch-bar, no btn-accept-verified, manual ZL.renderReview throws at review.js:491. f31b146: batch bar present, render ok | artifacts/review-evidence/T-158/probes/batch-dom-probe.py |
| settle probe, 390x844, 10 runs, f31b146 with the fix | box inside 10/10, y 696-828, scrollY 379 at every sample | artifacts/review-evidence/T-158/probes/settle-f31b146-fix.json |
| settle probe, f31b146 with the 70af4a7 one-shot restored | inside 10/10, same numbers | probes/settle-f31b146-pre-fix-one-shot.json |
| settle probe, f31b146 with no scroll call | inside 0/10, box y 847-979 | probes/settle-f31b146-no-scroll.json |
| settle probe, 83f1afd minus the stray block: fix / one-shot / no scroll | inside 10/10, 10/10, 6/10 (the other 4 at y 805-1064) | probes/settle-83f1afd-minus-stray-block-{fix,pre-fix,no-scroll}.json |
| pytest -k 'shows_the_reason and 390' on 83f1afd: one-shot copy | 6 of 6 runs pass | probes/mutant-390-pytest-summary.txt |
| pytest -k 'shows_the_reason and 390' on 83f1afd: click-time pass only | 6 of 6 runs pass | probes/mutant-390-pytest-summary.txt |
| pytest -k 'shows_the_reason and 390' on 83f1afd minus the stray block: no scroll call | 2 of 8 runs fail, both stub-390-844 | probes/m6-*.out |
| settle tally of all settle JSON files | 70 runs in 7 variants; position identical at every sample in every run | probes/settle-tally.py |

## Findings

1. **Major: the "after layout settles" clause is not proven.** The fix's timers (250 ms and 700 ms) are a guess. No test waits for rest, and `vis()` returns at the first frame the box is in view (test:93-102). In 70 settle-probe runs across seven variants the box position was identical at every sample in every run, so I did not observe any movement after the click. The card's handoff says layout moves for about 700 ms after the click, and I could not reproduce that. The pre-fix one-shot also keeps the box in view (10/10 at f31b146, 6/6 under pytest on 83f1afd). The scroll that matters is the one at click time: with no scroll call the box is below the fold in 10 of 10 settle runs at f31b146 and in 4 of 10 at 83f1afd minus the stray block. The extra passes are not shown to matter, and a regression back to one scroll would not be caught.

2. **Major: the card's AC 1 evidence cannot be reproduced at the card commit, and the green came from another card.** The cited artifact (`/private/tmp/claude-501/fe149/t158.out`) has ten '23 passed' lines and a 'done' line, with no sha, command or date. The same file on 83f1afd (`git diff --stat 0b2ce9c 83f1afd -- app/frontend tests/e2e` printed nothing) failed 4 of 23 in each of 10 runs. The batch-bar failure came from the stray block at 83f1afd:app/frontend/review.js:491, cured by 2de5ba9 (T-154 r3). f31b146 is 10/10 green.

3. **Minor: the rerun-count fallback swallows the trace error without a status or a log.** `app/frontend/stepper.js:216`: `catch (_) { /* the sentence falls back to no count */ }`. The fallback is visible, so this is not a silent verdict, but the error should reach the status line or the console (persona section 4 item 12).

4. **Minor: the rerun count change has no test.** The card changes two things; the refusal test covers only the scroll. Nothing covers `stepper.js:216-217` (the count when the trace is not cached). `git show 0b2ce9c --stat` lists only review.js and stepper.js, and the rerun test file is unchanged.

5. **Nit: the timers scroll the page regardless of user input.** `app/frontend/review.js:267` runs `pass()` at 250 ms and 700 ms unconditionally. A user who scrolls within 0.7 s after a refusal is pulled back. I did not reproduce this in a browser, so it is an opinion, not a verdict.

## Verdict rule

No finding is a blocker at f31b146. Two majors give `changes`.

## What I did not run

`pytest tests/unit`, the full e2e suite, and `test_rerun_judge.py` (the rerun-count path) were not run. The backend and LLM checklist items in my dossier are outside this frontend card.

## Process notes

I stopped only my own processes. Every probe server exited (`server exited -15`), and no listener remains on ports 17861 to 17874. Port 7860 was not used, and I did not touch other agents' app servers or tmux.

```json
{"card": "T-158", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD f31b146 (git archive, pinned at 2026-11-02 15:43 UTC; HEAD later moved to 9db2cec, one-line review.js registerPanel delta outside T-158 paths); card commit 0b2ce9c; private test server per run on a random 127.0.0.1 port with E2E_REQUIRE_DB=1 and the curated fixture backend; port 7860 not used; sample case",
 "exercised": [
  "read personas/staff-engineer.md, board show T-158, git show 0b2ce9c (review.js and stepper.js hunks), and the full test file tests/e2e/test_code_check_refusal.py",
  "git archive f31b146 into a fresh scratch dir; E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_code_check_refusal.py -q, 10 consecutive runs: 23 passed in each (artifacts/review-evidence/T-158/f31b146-refusal-x10/)",
  "git archive 83f1afd (HEAD at review start) into a fresh scratch dir; same command, 10 runs: 4 failed, 19 passed in each; the failing tests are the four batch tests (artifacts/review-evidence/T-158/83f1afd-refusal-x10/)",
  "git diff --stat 0b2ce9c 83f1afd -- app/frontend tests/e2e (empty) and git diff --quiet 0b2ce9c f31b146 -- tests/e2e/test_code_check_refusal.py (unchanged)",
  "batch DOM probe (Playwright, 1280x900, sample case, own server) on archives 0b2ce9c, 83f1afd and f31b146: batch-bar and btn-accept-verified presence, window errors, and a manual ZL.renderReview call; on 83f1afd the call threw ReferenceError key is not defined at review.js:491",
  "settle probe (Playwright, 390x844, 10 runs each): f31b146 with the fix, with the 70af4a7 one-shot restored, and with no scroll call; 83f1afd minus the stray block with the fix, the one-shot, and no scroll call; tally of all 70 runs (artifacts/review-evidence/T-158/probes/settle-tally.py)",
  "pytest -k 'shows_the_reason and 390' on mutant copies: one-shot 6 of 6 pass; click-time pass only 6 of 6 pass; no scroll call 2 of 8 fail (stub-390-844), all on 83f1afd minus the stray block except the first two which are on 83f1afd",
  "full refusal file once on 83f1afd with the stray block removed: 23 passed",
  "ps and lsof: every probe server I started exited; no listener on ports 17861-17874; port 7860 not touched"
 ],
 "verdict": "changes",
 "scores": {"AC1 ten consecutive green at the reviewed sha": 5, "AC1 evidence reproducible at the card commit": 1, "after-settle behaviour proven": 2, "test asserts on-screen and was not loosened": 4, "no swallowed errors in the diff": 3, "change covered by tests": 2},
 "findings": [
  {"severity": "major",
   "title": "The 'after layout settles' clause is not proven: the 250 ms and 700 ms passes have no observed effect and no test holds the box at rest",
   "evidence": "app/frontend/review.js:267 (pass(); requestAnimationFrame(...); setTimeout(pass, 250); setTimeout(pass, 700)); tests/e2e/test_code_check_refusal.py:93-102 (vis returns at the first in-viewport frame) and :117; artifacts/review-evidence/T-158/probes/settle-f31b146-fix.json (inside 10/10, box y 696-828, scrollY 379 at every sample); settle-f31b146-pre-fix-one-shot.json (inside 10/10, same numbers); settle-f31b146-no-scroll.json (inside 0/10, box y 847-979); settle-tally.py (70 runs, position identical at every sample in every run); mutant-390-pytest-summary.txt (one-shot 6/6 pass, click-time only 6/6 pass)",
   "why_it_matters": "The AC asks for the box inside the viewport after layout settles. Nothing in the test waits for rest, and the fix's timers are a guess. The handoff says layout moves for about 700 ms after the click; in 70 settle runs across seven variants I did not observe any movement. The pre-fix one-shot also keeps the box in view, so the fix is not shown to address the failure QA recorded. A regression back to one scroll is not caught, and a box that enters the viewport for one frame then leaves passes the test.",
   "fix": "Name the event that moves the layout after a refused Accept (the trace fetch or the panel repaint) and trigger the scroll from that event instead of guessing a time. Make the test prove rest: after that event, poll until the box is inside for N consecutive frames. Keep the on-screen assertion as it is.",
   "acceptance_test": "New case in tests/e2e/test_code_check_refusal.py at 390x844: delay the GET trace response by about 600 ms after the refused Accept (route stub); assert the box is inside the viewport and stays inside for 30 frames. It must fail on a build with the showRefusalInView call removed and on a build with only the one-shot line at review.js:324, provided the delayed trace moves the layout; if it does not, name the event that does. Run: git archive <sha> | tar -x, then E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_code_check_refusal.py -k 'shows_the_reason and 390' -q"},
  {"severity": "major",
   "title": "AC 1 evidence cannot be reproduced at the card commit; the green came from another card (2de5ba9)",
   "evidence": "/private/tmp/claude-501/fe149/t158.out (ten '23 passed' lines and a 'done' line; no sha, command or date). Same file on 83f1afd, which has no app/frontend or tests/e2e diff from 0b2ce9c: artifacts/review-evidence/T-158/83f1afd-refusal-x10/summary.txt and run-01.out to run-10.out, each '4 failed, 19 passed'; failing tests test_refused_batch_lists_the_items_it_refused_and_nothing_is_accepted[real|stub] and test_refused_batch_on_a_quote_check_offers_change_the_quote_per_item[real|stub]. Cause: 83f1afd:app/frontend/review.js:491 (ReferenceError: key is not defined in mountSection, from 6379c0b). 2de5ba9 moved the guard; f31b146 is 10/10 green (artifacts/review-evidence/T-158/f31b146-refusal-x10/).",
   "why_it_matters": "The card is closed on a green run that cannot be repeated at its own commit, and the fix it describes did not make the batch tests pass. AC evidence without a sha and command cannot be checked by the next reviewer or by Chris.",
   "fix": "Record the sha, the exact command, the date and the count in the AC evidence, for the sha that will merge. Re-run at that sha. In the handoff, state which commit made the batch tests green (2de5ba9) so the card is not credited with it.",
   "acceptance_test": "git archive <final sha> | tar -x -C <empty dir>, then E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_code_check_refusal.py -q, run 10 times: 23 passed each. The AC evidence line names the sha and the command."},
  {"severity": "minor",
   "title": "The rerun-count fallback swallows the trace error without a status or a log",
   "evidence": "app/frontend/stepper.js:216: `catch (_) { /* the sentence falls back to no count */ }`",
   "why_it_matters": "A failed trace fetch is dropped. The user sees a count-free sentence and nothing tells them the fetch failed. The fallback is visible, so this is not a silent verdict, but the error should still reach the status line or the console (persona section 4 item 12).",
   "fix": "Keep the count-free sentence, and also surface the failure in the rerun status or the console so it can be diagnosed.",
   "acceptance_test": "Route stub that fails GET trace before Run judge is pressed: the rerun status shows the count-free sentence and the failure is visible in the status or the console (asserted in a test)."},
  {"severity": "minor",
   "title": "The rerun count change has no test",
   "evidence": "git show 0b2ce9c --stat lists only app/frontend/review.js and app/frontend/stepper.js; stepper.js:216-217 (trace fetched first, then the count); tests/e2e/test_code_check_refusal.py is the only test the card names and does not reach this path",
   "why_it_matters": "The card's second change (the sentence keeps its count when the trace was not cached) is unverified. The race is described as 'under load', so it is a flake claim with no test.",
   "fix": "Add a test that presses Run judge before the trace is cached (for example a delayed GET trace route) and asserts the sentence carries the count.",
   "acceptance_test": "Delayed GET trace; press Run judge; the rerun status reads 'Running the second check on N items' with the right N."},
  {"severity": "nit",
   "title": "The 250 ms and 700 ms timers scroll the page regardless of user input",
   "evidence": "app/frontend/review.js:267 (setTimeout(pass, 250); setTimeout(pass, 700)); pass() calls window.scrollBy whenever the box is outside the band",
   "why_it_matters": "I would have done it differently: a user who scrolls within 0.7 s after a refusal is pulled back. I did not reproduce this in a browser.",
   "fix": "Stop the later passes once the user has scrolled, or drop them if finding 1 shows they are not needed.",
   "acceptance_test": "If kept: a test that scrolls the page by 200 px within 300 ms after the refusal and asserts the scroll position holds for 1 s."}
 ],
 "whats_right": [
  "showRefusalInView looks the box up again by item id on every pass and does nothing once it is inside the band (review.js:259-268), so it does not hold stale nodes.",
  "The test file is unchanged from 0b2ce9c to f31b146, still asserts on-screen (test:117), and the 390x844 cases pass 10 of 10 at f31b146.",
  "The handoff names the timers, the test and the run count, which made the claims checkable."
 ],
 "questions_for_chris": [
  "This review ran as claude-haiku-5-5 because the brief said so. CLAUDE.md's model table lists engineering reviewers as Sonnet. Is Haiku acceptable for this card?",
  "QA's repro note (board T-158, 14:40Z) saw accept-refused at y 805-937 at 078c5ae. My no-scroll copy reproduces that range, but the one-shot pre-fix does not fail. Does QA's probe script exist, and which trigger did it use?"
 ]}
```
