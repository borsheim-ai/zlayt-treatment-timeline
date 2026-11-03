# T-164 review, corrected record (staff-engineer-reviewer)

This file is the corrected record for `reviews/T-164-staff-engineer.md`, which the reviewer write guard now keeps as written. Use this file for the board record. One sentence in the first file is wrong: it says the nine tests are "the ones the card names". The card does not name them; I took the nine names from the file itself. The corrected sentence is in the "What I checked" list below. The verdict, the findings (none) and every number are unchanged.

**Verdict: pass** (0 blockers, 0 majors, 0 minors, 0 nits). Reviewed at commit 95ffe36, the sha the card's AC cites. HEAD was 9db2cec when I started and when I finished; the full suite at 9db2cec also passes (321 passed, 0 failed), so the file is green at HEAD as well.

## What I checked

- **The file at the cited sha.** Clean git archive of 95ffe36 with E2E_REQUIRE_DB=1 on my own server 127.0.0.1:7971: `pytest tests/e2e/test_conflict_skipped.py -v` gives `9 passed in 10.77s`. The nine tests cover the lib11 note and the not-checked line, the Spanish skipped-check cases, the skipped-reason wording, and the empty-group cases. The card's AC does not list them.
- **The full suite at 95ffe36** (same server): `319 passed, 2 skipped in 473.15s`, 0 failed. The file is part of that run. The three letter-total specs and test_adversarial case_07 are named in the orchestrator's note on the card (14:36 entry), and they are in the same run with 0 failures.
- **The full suite at HEAD 9db2cec** (own server 127.0.0.1:7972): `321 passed, 2 skipped in 456.78s`, 0 failed.
- **The triage claim.** The card says the 8-of-9 red was a transient frontend ReferenceError, not a stale test or a real regression. I checked that at the parent of the fix. `git archive 2de5ba9^` (c3a2af8) run on my own server 127.0.0.1:7973 gives `test_conflict_skipped.py`: `8 failed, 1 passed in 70.51s`. The fix commit 2de5ba9 moves the a-key guard out of `mountSection()` in app/frontend/review.js, which is where the ReferenceError came from (`git show --format=%s 2de5ba9 -- app/frontend`).
- **No test edit.** `git log --oneline -- tests/e2e/test_conflict_skipped.py` ends at b5f40c0 (T-151), before the card. The card's handoff says "nothing (no commit)", and that holds.
- **Card state.** `python3 tools/board.py show T-164` has `commits: []`, `rounds: 0`, and the AC evidence cites 95ffe36 with the same counts I reproduced.

## Findings

None.

## Notes on what I did not run

- The three letter-total specs and test_adversarial case_07 individually. They passed inside the full run at 95ffe36 (0 failed); I did not re-run them alone.
- Repeated runs of the file. One isolated run at 95ffe36 and one full-suite run at each of two shas.
- A mutation of the frontend fix. The 2de5ba9^ red is the control for this card's claim.

The order-dependent skip in test_polish_r4.py:175 is outside this card's file. It is recorded on the T-155 round-2 corrected review (reviews/T-155-staff-engineer-r2b.md, F1), and it does not affect this verdict.

Stopped only my own servers: listeners 36050 (7971, 95ffe36), 49256 (7972, 9db2cec), 49923 (7973, 2de5ba9^). Each was checked with lsof and ps (app.main, scratch cwd) before the kill; ports closed. The shared app on :7860 (PID 99144) was not touched.

```json
{"card": "T-164", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "tests/e2e/test_conflict_skipped.py at 95ffe36 (the sha the card's AC cites; clean git archive, E2E_REQUIRE_DB=1, own server 127.0.0.1:7971); full tests/e2e at 95ffe36 and at HEAD 9db2cec (own server 127.0.0.1:7972); parent of the fix 2de5ba9^ (c3a2af8, own server 127.0.0.1:7973); shared :7860 not touched",
 "exercised": [
   "python3 tools/board.py show T-164 (AC, commits, rounds, notes); git log --oneline -- tests/e2e/test_conflict_skipped.py (last change b5f40c0, T-151)",
   "git rev-parse HEAD -> 9db2cec at start and end; git merge-base --is-ancestor 9db2cec 95ffe36 -> not an ancestor, and git log --oneline 95ffe36..HEAD lists only 9db2cec (HEAD moved past the cited sha)",
   "git archive 95ffe36 | tar -x into scratch T155r2_T164/head95; own server 127.0.0.1:7971 (listener 36050, verified app.main and scratch cwd)",
   "E2E_BASE_URL=http://127.0.0.1:7971 ZLAYT_DB=<scratch>/db/e2e.sqlite3 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_conflict_skipped.py -v -> 9 passed in 10.77s (nine PASSED lines, 100%)",
   "E2E_BASE_URL=http://127.0.0.1:7971 ... pytest tests/e2e -q -rfEs (full suite at 95ffe36) -> 319 passed, 2 skipped in 473.15s, exit 0; the file and the letter-total and case_07 specs are in that run with 0 failed",
   "git archive 9db2cec into scratch headHEAD; own server 127.0.0.1:7972 (listener 49256); full tests/e2e -> 321 passed, 2 skipped in 456.78s, exit 0",
   "git archive 2de5ba9^ (c3a2af8) into scratch pre2de; own server 127.0.0.1:7973 (listener 49923); test_conflict_skipped.py -> 8 failed, 1 passed in 70.51s (the card's 8-of-9 red reproduced at the parent of the fix); failure text includes 'Locator expected to have count 1' and 'element(s) not found'",
   "git show --format=%s 2de5ba9 -- app/frontend (diff): the mountSection a-key guard, which referenced an undefined key, moves into the keydown handler in app/frontend/review.js (ReferenceError on every case load)",
   "git diff 20b3a42 95ffe36 -- tests/e2e/test_conflict_skipped.py: empty (no edit by T-155 or T-164)",
   "read reviews/T-155-staff-engineer-r1b.md and personas/staff-engineer.md for the review format and scope",
   "stopped only my own listeners 36050, 49256, 49923 after checking cwd and app.main with lsof and ps; ports 7971-7973 closed; shared :7860 (PID 99144) untouched",
   "not run: individual re-runs of the three letter-total specs and test_adversarial case_07 (they passed in the full run); repeated runs of the file; board.py review (not a reviewer action)"
 ],
 "verdict": "pass",
 "scores": {"test_integrity": 5, "triage_accuracy": 5, "evidence_matches_reviewed_commit": 4, "determinism": 4},
 "findings": [],
 "whats_right": [
   "The triage is right and reproducible: the 8-of-9 red reproduces at 2de5ba9^ (8 failed, 1 passed), and the fix is a frontend change, not a test edit",
   "No test was edited to get green: the file's last change predates the card (b5f40c0), and the card's handoff records no commit",
   "The card records the sha it ran on and the reds at the earlier state, so a later reader can reproduce both"
 ],
 "questions_for_chris": []}
```
