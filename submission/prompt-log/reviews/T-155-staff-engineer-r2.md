# T-155 round 2 review (staff-engineer-reviewer)

**Verdict: pass** (0 blockers, 0 majors, 2 minors, 1 nit). Reviewed at commit 95ffe36, the sha the card's AC cites. HEAD was 9db2cec when I started and was still 9db2cec when I finished, so I also ran the full suite at 9db2cec. The HEAD diff touches tests/e2e/conftest.py, test_no_console_errors.py and test_rerun_note.py; the result is 321 passed, 2 skipped, 0 failed.

## What I checked

- **Full suite at 95ffe36** (git archive, own server 127.0.0.1:7971, E2E_REQUIRE_DB=1): `319 passed, 2 skipped in 473.15s`, exit 0, 0 failed. The worker's record says `318 passed, 3 skipped`. The difference is one skip. The third skip in the worker's run is test_polish_r4.py:175, which is an order-dependent conditional skip (finding 1). The total is the same 321 in both runs.
- **Full suite at 9db2cec** (HEAD, own server 127.0.0.1:7972): `321 passed, 2 skipped in 456.78s`, exit 0.
- **T-144 revert.** `git diff 20b3a42^ 95ffe36 -- tests/e2e/test_polish_r3.py` has one hunk, a focus wait at :59. ROW_BOXES_JS is gone, the measure at :173 is `r.height`, and the budgets (520 at :174, 170/150 at :180, 420 at :197) are unchanged. The T-144 comment is gone.
- **No weakening.** `git diff 20b3a42 95ffe36 -- tests/e2e` adds no xfail. The only added skip is a pytest.skip for library cases in test_multicase.py. It shows 29 removed assert/expect lines across cards, mostly from the T-149 r2 overview restructure. I spot-checked test_multicase.py: the replacements tighten the checks, for example "ready" now means export passes and nothing is undecided, and `not (got & ready)` is added. I did not read all 29 lines.
- **L6 under D-060.** test_stepper.py:23 is `L6_OBJECTIONS = 5`, and D-059/D-060 at memory/ORCHESTRATOR_DECISIONS.md:67-68 record it. The presence check at test_stepper.py:238 asserts that a2 and a7 are in the judge rejections, and the per-item loop at :239-240 requires each to appear once. This answers r1b F4.
- **Wording.** test_rerun_judge.py:308 is renamed to match its assertions, which answers r1b F5. The EDIT_WAITING wording matches app/backend/trace.py:293 and memory/contracts/api.md:365-374.
- **test_conflict_skipped.py.** Alone at 95ffe36: `9 passed in 10.77s`. The file is unchanged since b5f40c0 (T-151), so it was not edited to pass.
- **Mutation of the reverted budget.** A first mutation, `.unc[hidden]{display:block}`, had no effect. styles.css:3 `[hidden] { display: none !important; }` is the operative rule, so the uncovered.css:4 rule is shadowed. With the list forced visible instead (`hidden: null` in uncovered.js:21 in a scratch copy), test_polish_r3.py:180 fails for a row at 243 px, and :197 fails with `[600.09375, 407.09375]`. The reverted budget does guard a visible list. This answers the r1b F2 acceptance test.

## Findings

**F1 (minor). Order-dependent conditional skip in test_polish_r4.py:174-175. The card's skip count does not reproduce.**
- Isolation, 95ffe36, five runs: `pytest tests/e2e/test_polish_r4.py -k tray_flag_agrees -q -rs` gave `SKIPPED [1] tests/e2e/test_polish_r4.py:175: the AI check did not list the tray flag in this fixture` and `1 skipped, 13 deselected` every time (5 of 5).
- Full suite at 95ffe36 (my run): the test passed. The skip list is test_ladder_gate.py:37 and test_multicase.py:666 only.
- Worker's full run (scratch t155r2/full3.txt): `318 passed, 3 skipped`, with `SKIPPED [1] tests/e2e/test_polish_r4.py:175`.
- The skip line was added in e293daa (T-060 r4). T-155 did not introduce it.
- Why it matters: when the row is missing, the T-117 check (the AI-check row for a tray flag must say "Left out of the letter", not "accept") does not run and the test reports skip. Whether it runs depends on the order of the full suite. This is not a spec violation, so it is minor, but it is a determinism gap, and the card's "318 passed, 3 skipped" cannot be reproduced.
- Fix: replace the `if row.count() == 0: pytest.skip(...)` with a retrying wait after the panel is opened (for example `expect(row).to_have_count(1)`), so a missing row fails. Cite the skip list in the card's AC.
- Acceptance test: `pytest tests/e2e/test_polish_r4.py -k tray_flag_agrees` passes 5 of 5 with 0 skips. A scratch mutation of the "Left out of the letter" wording in the AI-check row fails it.

**F2 (minor). T-158 still carries the "about 50%" claim that r1b F3 asked to replace.**
- `python3 tools/board.py show T-158`, line 3: `title: "Flaky ~50% at 390x844: ..."`. The card has no geometry measurement.
- Owner: T-158 (frontend). Not changed by this card, and not a T-155 blocker.
- Fix: retitle T-158, and replace the rate with the geometry measurement from artifacts/review-evidence/T-155/stub6.txt (btn_y, scrollY, box bottom).
- Acceptance test: the T-158 title has no rate, and its AC has a probe of at least 30 samples at 390x844 showing the accept-refused box inside the viewport.

**F3 (nit). The r1b F2 evidence names the wrong hiding rule.**
- r1b cites app/frontend/uncovered.css:4 as the rule that hides the list. That rule is shadowed by app/frontend/styles.css:3 `[hidden] { display: none !important; }`.
- The 0 px conclusion still holds. Only the citation is wrong. The r1b file is write-once, so the correction is recorded here.

## Notes on what I did not run

- A mutation of the a7 presence check itself. I ran the reverted budget mutation only.
- board.py review (reviewers do not run it).
- Full suite on the mutated copy (the mutation runs were the three budget tests only).

Stopped only my own servers: listeners 36050 (127.0.0.1:7971, archive 95ffe36), 49256 (127.0.0.1:7972, archive 9db2cec), 49923 (127.0.0.1:7973, archive 2de5ba9^), 63558 (127.0.0.1:7974, mutated copy). Each was checked with lsof for its cwd in my scratch folder and for the app.main command before the kill. Ports 7971-7974 are closed. The shared app on :7860 (PID 99144) was not touched.

```json
{"card": "T-155", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "tests/e2e at 95ffe36 (the sha the card cites; full suite run from git archive); HEAD at review start and end was 9db2cec (full suite run from git archive, diff 95ffe36..9db2cec touches conftest.py, test_no_console_errors.py, test_rerun_note.py and app/frontend); own servers 127.0.0.1:7971 (95ffe36), 127.0.0.1:7972 (9db2cec), 127.0.0.1:7973 (2de5ba9^), 127.0.0.1:7974 (scratch mutant of 95ffe36); sample case and library cases through the API; shared :7860 not touched",
 "exercised": [
   "python3 tools/board.py show T-155; show T-164; show T-158 (line 3 title); read reviews/T-155-staff-engineer-r1b.md and personas/staff-engineer.md",
   "git rev-parse HEAD -> 9db2cec at start and at end; git merge-base --is-ancestor: 95ffe36, d967488, 0e3e8ba, 2de5ba9, 802d5fd, 94a31a4, f262223, 20b3a42 are ancestors of 95ffe36; 9db2cec is not",
   "git archive 95ffe36 | tar -x into scratch T155r2_T164/head95 (2246 files; no untracked fixtures copied; no FIXTURE_MISS)",
   "own server 127.0.0.1:7971 from head95 (listener 36050): E2E_BASE_URL=http://127.0.0.1:7971 ZLAYT_DB=<scratch>/db/e2e.sqlite3 E2E_REQUIRE_DB=1 pytest tests/e2e -q -rfEs -> 319 passed, 2 skipped in 473.15s, exit 0 (skips: test_ladder_gate.py:37, test_multicase.py:666)",
   "git archive 9db2cec into scratch headHEAD; own server 127.0.0.1:7972 (listener 49256); same command -> 321 passed, 2 skipped in 456.78s, exit 0",
   "test_conflict_skipped.py -v on head95 -> 9 passed in 10.77s; git log -- tests/e2e/test_conflict_skipped.py: last change b5f40c0 (T-151), unchanged by T-155/T-164",
   "git archive 2de5ba9^ (c3a2af8) into scratch pre2de; own server 127.0.0.1:7973 (listener 49923); test_conflict_skipped.py -> 8 failed, 1 passed in 70.51s",
   "git show --format=%s 2de5ba9 -- app/frontend: the mountSection a-key guard that threw ReferenceError on case load is moved into the keydown handler (review.js)",
   "git diff 20b3a42^ 95ffe36 -- tests/e2e/test_polish_r3.py, test_stepper.py, test_rerun_judge.py: one-hunk focus wait (polish_r3), L6_OBJECTIONS and presence checks (stepper), EDIT_WAITING and rename (rerun_judge)",
   "git diff 20b3a42 95ffe36 -- tests/e2e: 29 removed assert/expect lines across cards; no added xfail; one added pytest.skip (test_multicase library cases); spot-checked test_multicase.py replacements (tightenings)",
   "git show 95ffe36:tests/e2e/test_stepper.py lines 21-23, 174-193, 231-240 (L6 count 5, presence checks a2 and a7); memory/ORCHESTRATOR_DECISIONS.md:67-68 (D-059, D-060); app/backend/trace.py:293 (Edited; waiting for your check); memory/contracts/api.md:365-374",
   "git show 95ffe36 greps: test_polish_r3.py has no ROW_BOXES_JS or T-144 comment; measure at :173 is r.height; budgets :174 (520), :180 (170/150), :197 (420); no xfail under tests/e2e",
   "pytest tests/e2e/test_polish_r4.py -k tray_flag_agrees, five runs on head95 -> SKIPPED at test_polish_r4.py:175 each time (1 skipped, 13 deselected); git log -S shows the skip line added in e293daa",
   "worker scratch t155r2/full3.txt: 318 passed, 3 skipped; third skip test_polish_r4.py:175 (read, not re-run)",
   "mutation 1 on scratch copy mut95 (uncovered.css .unc[hidden]{display:block}): no effect; computed display stayed none (playwright probe); styles.css:3 is the operative rule; mutation discarded",
   "mutation 2 on scratch copy mut95 (uncovered.js:21 hidden: null, list always visible), own server 127.0.0.1:7974 (listener 63558): pytest tests/e2e/test_polish_r3.py -k 'first_screen or 390 or density' -> 2 failed (test_polish_r3.py:180 row 243 px; :197 [600.09375, 407.09375]); the same tests pass on the unmutated tree in the full run above",
   "playwright probes (scratch probe_mut.py, probe_css.py) at 1440x900 on the sample case: row heights, uncovered-list display and hidden state",
   "stopped only my own listeners 36050, 49256, 49923, 63558 after checking cwd (scratch folder) and app.main command with lsof and ps; ports 7971-7974 closed; shared :7860 (PID 99144) and :7966 (not mine) untouched",
   "not run: mutation of the a7 presence check itself; board.py review (not a reviewer action)"
 ],
 "verdict": "pass",
 "scores": {"test_integrity": 4, "triage_accuracy": 5, "evidence_matches_reviewed_commit": 4, "decision_traceability": 5, "determinism": 3},
 "findings": [
   {"severity": "minor",
    "title": "Order-dependent conditional skip at test_polish_r4.py:174-175 hides the T-117 tray-flag check; the card's 318-passed-3-skipped count does not reproduce",
    "evidence": "Isolation at 95ffe36, five runs: `pytest tests/e2e/test_polish_r4.py -k tray_flag_agrees -q -rs` -> `SKIPPED [1] tests/e2e/test_polish_r4.py:175: the AI check did not list the tray flag in this fixture`, `1 skipped, 13 deselected` (5 of 5). Full suite at 95ffe36 (my run, scratch head95): `319 passed, 2 skipped in 473.15s`, skips only test_ladder_gate.py:37 and test_multicase.py:666. Worker scratch t155r2/full3.txt: `318 passed, 3 skipped`, third skip test_polish_r4.py:175. Line 174 is `if row.count() == 0:` (no wait); the skip line was added in e293daa (T-060 r4).",
    "why_it_matters": "The check's assertions do not run when the row is missing, and whether it runs depends on suite order (0 of 5 in isolation, passed in 2 of 3 full runs). That is a determinism gap, not a spec violation, so it is minor. It also means the card's skip count is not reproducible.",
    "fix": "Replace the count-zero skip with a retrying wait after the panel is opened (for example expect(row).to_have_count(1)), so a missing row fails. Cite the skip list in the card's AC evidence.",
    "acceptance_test": "`pytest tests/e2e/test_polish_r4.py -k tray_flag_agrees` passes 5 of 5 in isolation with 0 skips; a scratch mutation of the 'Left out of the letter' wording in the AI-check row makes it fail."},
   {"severity": "minor",
    "title": "T-158 still says 'Flaky ~50%'; the geometry measurement that r1b F3 asked for is not on the card",
    "evidence": "`python3 tools/board.py show T-158`, line 3: title \"Flaky ~50% at 390x844: after a refused Accept the reason box ... sometimes ends below the fold\". No geometry sample on the card. r1b F3 (reviews/T-155-staff-engineer-r1b.md) asked for the rate to be replaced by btn_y, scrollY and box bottom.",
    "why_it_matters": "The mechanism is real and T-158 owns it, but the card's rate was not reproduced (1 of 24 samples, per r1b). A rate in a title tells the next reader to expect flakiness the measurements do not show. This is not a T-155 blocker.",
    "fix": "On T-158, retitle the card without the rate and add the geometry measurement (btn_y, scrollY, box bottom) from artifacts/review-evidence/T-155/stub6.txt.",
    "acceptance_test": "The T-158 title has no rate; its AC includes a probe of at least 30 samples at 390x844 showing the accept-refused box inside the viewport for every sampled scrollY."},
   {"severity": "nit",
    "title": "r1b F2 cites the wrong hiding rule (uncovered.css:4); the operative rule is styles.css:3",
    "evidence": "`git show 95ffe36:app/frontend/uncovered.css | grep -n 'unc\\[hidden\\]'` -> `4:.unc[hidden] { display: none; }`; `git show 95ffe36:app/frontend/styles.css | grep -n '\\[hidden\\]'` -> `3:[hidden] { display: none !important; }`. A scratch mutation of uncovered.css:4 to display:block left computed display at none.",
    "why_it_matters": "The conclusion that a collapsed list costs 0 px still holds, but a future reader who edits uncovered.css:4 will change nothing. The r1b file is write-once, so the correction is recorded here.",
    "fix": "Cite styles.css:3 as the operative hide rule in any later note on the list budget.",
    "acceptance_test": "A note that names styles.css:3 as the hide rule, with the computed display check in the evidence."}
 ],
 "whats_right": [
   "The T-144 row-height loosening is fully reverted: test_polish_r3.py at 95ffe36 differs from its pre-card version by one focus-wait hunk, and the 520/170/150/420 budgets are unchanged",
   "The reverted budget guards a visible list: forcing the list visible in a scratch copy fails test_polish_r3.py:180 (243 px row) and :197 ([600.09375, 407.09375])",
   "The L6 change is evidenced both ways: count 5 under D-060 and a presence check that a2 and a7 are among the judge rejections (test_stepper.py:238), which answers r1b F4"
 ],
 "questions_for_chris": []}
```
