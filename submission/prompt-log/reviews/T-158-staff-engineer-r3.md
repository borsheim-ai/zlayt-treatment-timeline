# T-158 review r3: refused-Accept reason box at 390x844, judged at HEAD 3ddfdc6 (staff-engineer-reviewer)

**Verdict: changes.** No blocker. Two majors from r2 are still open at HEAD 3ddfdc6: the "after layout settles" clause is still not proven (finding 1), and AC 1 still cites a sha-less artifact that is red at the card commit (finding 2). The refusal file is green at HEAD, and the box is inside the viewport at 1 s and at rest in every probe run, but the probe cannot tell the card's timers from a single scroll.

## What I ran (sha and scope)

- Reviewed sha: **3ddfdc6** (HEAD when I archived it, 2026-11-02 19:16 UTC). Card commit: 0b2ce9c. HEAD is 57 commits after the card commit and includes the T-166 and T-174 frontend work. The card's showRefusalInView (app/frontend/review.js:344-353 at HEAD) is unchanged from 0b2ce9c.
- The e2e file changed only in its import line and one `reveal()` call between 0b2ce9c and HEAD (`git diff 0b2ce9c HEAD -- tests/e2e/test_code_check_refusal.py`), so the on-screen check and the first-frame `vis()` poll are the same as in r2.

## Round-2 majors at HEAD

| r2 finding | status at 3ddfdc6 | evidence |
|---|---|---|
| 1. "after layout settles" not proven | **open** | review.js:352 timers unchanged. A one-shot copy (single pass at click time) passes the 390 probe 10/10 and `-k 'shows_the_reason and 390'` 2/2. control-oneshot-head-3ddfdc6-390x844/, control-oneshot-head-3ddfdc6-pytest-390.txt |
| 2. AC 1 evidence not reproducible at the card commit | **open** | AC 1 on the board still reads "23 passed each, 0 failed (artifacts: /private/tmp/claude-501/fe149/t158.out)" with no sha, command or date. 0b2ce9c gives 4 failed, 19 passed. card-0b2ce9c-refusal-once.txt |
| 3. stepper.js:216 swallows the trace error | open (minor) | stepper.js:216 unchanged |
| 4. rerun count path has no test | open (minor) | no test in tests/e2e/test_rerun_judge.py routes GET trace |
| 5. timers scroll regardless of input | open (nit) | review.js:352 unchanged |

## Results

- Refusal file at HEAD 3ddfdc6, 10 consecutive runs, E2E_REQUIRE_DB=1, a private server per run: **23 passed in each of 10 runs, rc 0** (head-3ddfdc6-refusal-x10/run-01.out to run-10.out, summary.txt).
- Rest probe at HEAD, 390x844, own server on port 58037, fixture backend, two modes (stub = route-stubbed 422; real = summary broken in SQLite): **20 of 20 pass**. The box is inside at 1.0 s, and its y is 696 at every sample from 1.0 s to 2.0 s (probe-head-3ddfdc6-390x844/summary.txt).
- Controls on copies of HEAD (never the repo):
  - No scroll call (review.js:411 removed): **5 of 5 fail**, box at y 847 (control-noscroll-head-3ddfdc6-390x844/). The probe can see the defect.
  - One-shot pass at click time (review.js:352 cut to `pass();`): **10 of 10 pass** in the probe, and 2 of 2 pass in the 390 pytest cases (control-oneshot-head-3ddfdc6-390x844/, control-oneshot-head-3ddfdc6-pytest-390.txt).
- Card commit 0b2ce9c, refusal file once: **4 failed, 19 passed** in 156.69 s. All four failures are the batch tests (card-0b2ce9c-refusal-once.txt).

## Findings

1. **Major: the "after layout settles" clause is still not proven.** The 250 ms and 700 ms passes (review.js:352) are guesses. The one-shot copy keeps the box inside in the probe and in the pytest cases, so no run here shows the layout moving after the click. vis() (test:93-103) still returns at the first in-viewport frame, so a box that enters and leaves for one frame passes. The handoff's claim that layout moves for about 700 ms is still not observed. The 1-second probe above is evidence for the AC, not a test in the repo.
2. **Major: AC 1 still cites a sha-less artifact, and the batch tests are red at the card commit.** The AC has no sha, command or date, and the handoff does not say that 2de5ba9 made the batch tests green. The 10/10 result is at HEAD, which is not the card's commit. The worker should record the sha the card will merge with, the exact command and the artifact path, and then re-run at that sha.
3. **Minor: the rerun-count fallback swallows the trace error without a status or a log.** stepper.js:216 is `catch (_) { /* the sentence falls back to no count */ }`. The count-free sentence is visible, but the failed fetch is not reported anywhere.
4. **Minor: no test covers the uncached-trace path of the rerun count.** `grep -n 'trace.*route\|route.*trace' tests/e2e/test_rerun_judge.py` returns nothing at HEAD, so no test delays or fails the trace fetch that stepper.js:215-216 makes before the count.
5. **Nit: the timers scroll the page regardless of user input.** review.js:352. Not reproduced in a browser; my opinion only.

## Not run

`pytest tests/unit`, the full e2e suite, and `test_rerun_judge.py` were not run. The backend and LLM checklist items are outside this frontend card. The 0b2ce9c check is one run, not ten.

## Process notes

- I started three probe servers (PIDs 31017, 31548, 31751), and each exited with rc -15 after its probe. No listener remains on ports 58037, 58599 or 58776.
- I did not touch port 7860 (PID 19991, not mine) or the other app.main processes (PIDs 23429 and 37589, not mine).
- All helper scripts and outputs are under artifacts/review-evidence/T-158-r3/. The pinned archives are in the session scratchpad.

```json
{"card": "T-158", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 3ddfdc6 (git archive into a fresh scratch dir; 57 commits after card commit 0b2ce9c, includes T-166 and T-174); card commit 0b2ce9c for one control run; private test server per run from conftest (free loopback port, E2E_REQUIRE_DB=1, fixture backend, curated set); own probe server on port 58037; sample case; 390x844 probe, 390x844 and 1440x900 pytest cases",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-158-staff-engineer-r2.md, board show T-158 (AC 1 evidence and handoff verbatim), .claude/agent-memory project_t158_settle_patterns.md",
  "git rev-parse HEAD (3ddfdc680952df4a53d65c537047852aa62bd007); git rev-list --count 0b2ce9c..HEAD (57); git diff 0b2ce9c HEAD -- tests/e2e/test_code_check_refusal.py (import and reveal lines only); git show HEAD:app/frontend/review.js grep showRefusalInView (lines 344, 411); git show HEAD:app/frontend/stepper.js line 216",
  "git archive 3ddfdc6 | tar -x into a fresh scratch dir (2323 files); git archive 0b2ce9c | tar -x into a second fresh scratch dir",
  "artifacts/review-evidence/T-158-r3/run_x10.py: tests/e2e/test_code_check_refusal.py 10 consecutive runs at the HEAD archive, python -I -m pytest, E2E_REQUIRE_DB=1, E2E_BASE_URL and ZLAYT_DB unset, private server per run: 23 passed each, rc 0 (head-3ddfdc6-refusal-x10/)",
  "artifacts/review-evidence/T-158-r3/probe_refusal_rest.py (with launch_server.py) on the HEAD archive, own server on port 58037, 390x844, stub and real modes, 10 runs each: 20 of 20 pass; box inside at 1.0 s and y 696 at every sample 1.0-2.0 s (probe-head-3ddfdc6-390x844/)",
  "mutate_no_scroll.py on a copy of HEAD (review.js:411 call removed), probe 5 runs stub: 0 of 5 pass, box y 847 (control-noscroll-head-3ddfdc6-390x844/)",
  "mutate_one_shot.py on a copy of HEAD (review.js:352 cut to pass()), probe 5 runs stub and 5 real: 10 of 10 pass; pytest -k 'shows_the_reason and 390' on that copy: 2 passed (control-oneshot-head-3ddfdc6-390x844/, control-oneshot-head-3ddfdc6-pytest-390.txt)",
  "card commit 0b2ce9c archive: python -I -m pytest tests/e2e/test_code_check_refusal.py -q, E2E_REQUIRE_DB=1: 4 failed (test_refused_batch_* real and stub), 19 passed in 156.69 s (card-0b2ce9c-refusal-once.txt)",
  "grep -n 'trace.*route|route.*trace|second check' tests/e2e/test_rerun_judge.py at HEAD (no trace route); ps and lsof: the three probe servers I started exited (rc -15); no listener on 58037, 58599, 58776; 7860 and PIDs 23429, 37589 not touched",
  "not run: pytest tests/unit, the full e2e suite, test_rerun_judge.py"
 ],
 "verdict": "changes",
 "scores": {"AC1 ten consecutive green at the reviewed sha": 5, "AC1 evidence reproducible at the card commit": 1, "after-settle behaviour proven": 2, "test asserts on-screen and was not loosened": 4, "no swallowed errors in the diff": 3, "change covered by tests": 2},
 "findings": [
  {"severity": "major",
   "title": "The 'after layout settles' clause is still not proven at HEAD: a single click-time scroll passes the same probe and tests as the card's timers",
   "evidence": "app/frontend/review.js:352 (HEAD: pass(); requestAnimationFrame(() => { pass(); requestAnimationFrame(pass); }); setTimeout(pass, 250); setTimeout(pass, 700)); tests/e2e/test_code_check_refusal.py:93-103 (vis() returns at the first in-viewport frame; unchanged 0b2ce9c..HEAD apart from the import and reveal lines); artifacts/review-evidence/T-158-r3/control-oneshot-head-3ddfdc6-390x844/summary.txt (one-shot copy: 10 of 10 pass, box y 696 at 1.0-2.0 s); control-oneshot-head-3ddfdc6-pytest-390.txt ('2 passed in 3.80s')",
   "why_it_matters": "The AC says the box is inside after layout settles. At HEAD it is inside at 1 s and at rest in 20 of 20 probe runs, but a single scroll at click time does the same, so the 250 ms and 700 ms passes are not shown to do anything and the test cannot tell them from one scroll. A regression to one scroll is not caught, and the handoff's claim that layout moves for about 700 ms after the click has still not been observed (r2 finding 1, carried over).",
   "fix": "Name the event that moves the layout after a refused Accept (the delayed trace fetch or the panel repaint), trigger the scroll from that event, and add a rest check: after a delayed GET trace, assert the box is inside for 30 consecutive frames. If no event moves the layout, drop the timers and say in the handoff that one scroll is enough.",
   "acceptance_test": "New case in tests/e2e/test_code_check_refusal.py at 390x844 with a route stub that delays GET trace by about 600 ms after the refused Accept: the box is inside and stays inside for 30 frames. It must fail on a copy with review.js:352 cut to pass() if the delayed trace moves the layout; if it does not, the handoff names the event that does. Repro: git archive <sha> | tar -x into an empty dir; E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_code_check_refusal.py -k 'shows_the_reason and 390' -q"},
  {"severity": "major",
   "title": "AC 1 still cites a sha-less artifact, and the batch tests are red at the card commit 0b2ce9c",
   "evidence": "board show T-158, AC 1 evidence (unchanged since r2): '... 23 passed each, 0 failed (artifacts: /private/tmp/claude-501/fe149/t158.out)' with no sha, command or date; handoff unchanged and does not name 2de5ba9; artifacts/review-evidence/T-158-r3/card-0b2ce9c-refusal-once.txt ('4 failed, 19 passed in 156.69s', all four test_refused_batch_* cases); artifacts/review-evidence/T-158-r3/head-3ddfdc6-refusal-x10/summary.txt (10 of 10 at 3ddfdc6, 23 passed each)",
   "why_it_matters": "The card is credited with a green run that cannot be tied to a commit, and at its own commit the batch tests fail. The 10 of 10 result is at HEAD 3ddfdc6, which has 57 later commits, so it is not the card's own green either. Nothing on the card lets the next reviewer or Chris repeat the claim at a sha (r2 finding 2, carried over).",
   "fix": "Put the sha that will merge, the exact command, the date, the count and the artifact path under artifacts/review-evidence/T-158/ into AC 1. In the handoff, say that 2de5ba9 (T-154 r3) made the batch tests green at the card commit. Re-run 10 times at the merge sha and record it.",
   "acceptance_test": "board show T-158 AC 1 evidence names a sha, a command and a path under artifacts/review-evidence/T-158/; that path holds 10 run outputs at that sha, each '23 passed'."},
  {"severity": "minor",
   "title": "The rerun-count fallback swallows the trace error without a status or a log",
   "evidence": "app/frontend/stepper.js:216: catch (_) { /* the sentence falls back to no count */ } (unchanged at HEAD)",
   "why_it_matters": "A failed trace fetch is dropped. The sentence loses its count and nothing tells the user or the console that the fetch failed. The fallback is visible, so this is not a silent verdict, but the error should still reach the status line or the console (persona section 4 item 12; r2 finding 3, carried over).",
   "fix": "Keep the count-free sentence, and also surface the failure in the rerun status or the console so it can be diagnosed.",
   "acceptance_test": "Route stub that fails GET trace before Run judge is pressed: the rerun status shows the count-free sentence and the failure is visible in the status or the console (asserted in a test)."},
  {"severity": "minor",
   "title": "No test covers the uncached-trace path of the rerun count",
   "evidence": "grep -n 'trace.*route|route.*trace' tests/e2e/test_rerun_judge.py returns nothing at 3ddfdc6; stepper.js:215-216 is the only path that fetches the trace before the count (r2 finding 4, carried over)",
   "why_it_matters": "The card's second change (the sentence keeps its count when the trace was not cached) is still unverified. The race is described as 'under load', so it is a flake claim with no test.",
   "fix": "Add a test that presses Run judge before the trace is cached (for example a delayed GET trace route) and asserts the sentence carries the count.",
   "acceptance_test": "Delayed GET trace; press Run judge; the rerun status reads 'Running the second check on N items' with the right N."},
  {"severity": "nit",
   "title": "The 250 ms and 700 ms timers scroll the page regardless of user input",
   "evidence": "app/frontend/review.js:352 (setTimeout(pass, 250); setTimeout(pass, 700)); pass() calls window.scrollBy whenever the box is outside the band (r2 finding 5, carried over)",
   "why_it_matters": "I would have done it differently: a user who scrolls within 0.7 s after a refusal is pulled back. I did not reproduce this in a browser, so it is an opinion, not a verdict.",
   "fix": "Stop the later passes once the user has scrolled, or drop them if finding 1 shows they are not needed.",
   "acceptance_test": "If kept: a test that scrolls the page by 200 px within 300 ms after the refusal and asserts the scroll position holds for 1 s."}
 ],
 "whats_right": [
  "At HEAD 3ddfdc6 the refusal file passed 23 of 23 in each of 10 consecutive runs (artifacts/review-evidence/T-158-r3/head-3ddfdc6-refusal-x10/).",
  "The 390x844 probe had the box fully inside at 1.0 s and at rest from 1.0 to 2.0 s in 20 of 20 runs, stub and real (artifacts/review-evidence/T-158-r3/probe-head-3ddfdc6-390x844/).",
  "The on-screen assertion at tests/e2e/test_code_check_refusal.py:117 is unchanged and still requires the box fully inside the viewport."
 ],
 "questions_for_chris": [
  "This review ran as claude-haiku-5-5 because the brief said so. CLAUDE.md's model table lists engineering reviewers as Sonnet. Is Haiku acceptable for this card?"
 ]}
```
