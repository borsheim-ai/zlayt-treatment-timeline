# T-204 review — staff-engineer-reviewer (round 1), commit 9b37b9c

Verdict: fail (one blocker). The commit itself is clean and the two things the card changed work and are well pinned. But AC 1 says "for a prepared case no screen ever paints 'AI' wording", and the same prepared item the new test drives still gets "kept the AI's summary" on the case rail and in the AI-check panel, in static text the card never touched.

1. Commit content: confirmed. `git diff --name-status 105d212 9b37b9c` lists exactly app/frontend/input.js, review.js, switcher.js (M) and tests/e2e/test_prepared_first_paint.py (A). 9b37b9c has parent 105d212, and `git diff b4af023 9b37b9c` over those four paths is empty (same content as the replaced commit). b4af023 also had parent 105d212, but its tree was stale: `git diff --stat b4af023^ b4af023` = 151 files changed, 49927 deletions. It is not an ancestor of HEAD, so it is orphaned; HEAD (d23687e) descends from 9b37b9c. Nobody's work is reverted by 9b37b9c. One caveat is the shared index (finding 3).
2. Prepared items, classic review.js: first paint and swap are correct for the three nodes it watches (edit-check-hint, edit-compare-prompt, compare-export-note). Mutants M1-M3 (isPrepared always false; heldText always AI; accepted note always AI) each fail the new test. Guided review.js: confirmed no client-side AI fallback. Item text goes through R.plain(item.why) from the server, R.tagFor checks item.prepared first, and step4 blockers come from the server trace. Grep for "no answer", "AI's wording" and "AI wrote" in app/frontend/guided/*.js found nothing painted for an item. Read and grep only, not exercised in a browser. Not covered by the card: stepper.js and judges.js (finding 1).
3. Late library: works. Removing the listener (M4), removing the dispatch in switcher.js (M5) and rebuilding on every event (M6, overwrites an unrelated error) each fail one of the three tests.
4. Tests: new file 3 passed on the clean archive. Full tests/e2e from a fresh `git archive 9b37b9c` with E2E_REQUIRE_DB=1: 561 passed, 1 skipped, 0 failed (796.88 s). test_code_check_refusal::test_case_verdict_reads_the_backend_label_in_rail_and_panel passed in that run and 5 of 5 alone (about 2 s each). I could not reproduce the worker's failure. It is outside the card's four files. My hypothesis, not tested: open_rail clicks the summary only if the details is closed, so a late auto-open could toggle it shut under load. Machine load average was 11-14 during my run.

```json
{"card": "T-204", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 9b37b9c vs parent 105d212 (app/frontend/input.js, review.js, switcher.js, tests/e2e/test_prepared_first_paint.py); stepper.js and judges.js read for the same prepared-item flow; git archive copies of 9b37b9c with private fixture-backend servers; HEAD at review time d23687e (descends from 9b37b9c)",
 "exercised": [
  "Read personas/staff-engineer.md, the card and handoff (board.py show T-204), memory/ORCHESTRATOR_DECISIONS.md D-065 and D-069",
  "git diff --name-status 105d212 9b37b9c: 4 files (3 M, 1 A); git diff 105d212 9b37b9c -- app/frontend read in full; git diff b4af023 9b37b9c on the four paths: empty",
  "git merge-base --is-ancestor: b4af023 NOT an ancestor of HEAD, 9b37b9c is; git diff --stat b4af023^ b4af023: 151 files, 49927 deletions (the stale commit)",
  "git diff --cached --stat in the shared repo: index holds the reverse of the card (6 files, 122 deletions); git status shows 'D  tests/e2e/test_prepared_first_paint.py' staged, the file untracked in the tree, identical content to HEAD for the other three",
  "Read tests/e2e/test_prepared_first_paint.py in full; read guided/review.js 1-130, guided step2/3/4 reason paths, stepper.js 505-535, judges.js lines 96/163/189 by grep and sed",
  "git archive 9b37b9c into scratchpad T204_r1/clean; tests/e2e/test_prepared_first_paint.py with E2E_REQUIRE_DB=1: 3 passed",
  "Mutants in separate archive copies (grep-confirmed counts): M1 isPrepared=>false, M2 heldText=>AI_HELD, M3 accepted note=>ACCEPTED_HELD: each 1 failed, 2 passed (first_paint test, lines 46/46/60); M4 no zl:switcher listener, M5 no dispatch: late-library test fails; M6 always rebuild: unrelated-error test fails (scripts artifacts/review-evidence/T204_mutate.py and T204_mutate_input.py)",
  "Full tests/e2e from a fresh archive (diff -rq clean == full) at 9b37b9c, E2E_REQUIRE_DB=1: 561 passed, 1 skipped in 796.88s (artifacts/review-evidence/T204_full_e2e_9b37b9c.log)",
  "test_case_verdict_reads_the_backend_label_in_rail_and_panel alone x5 on the same archive: 5 passed",
  "Probe artifacts/review-evidence/T204_probe_rail.py copied into the clean archive as tests/e2e/test_probe_t204.py: same prepared held item as the card's test, then reload, open the case rail and the AI-check panel: fails with 'kept the AI's summary' in rail_all (3 places) and judge_panel (screenshot artifacts/review-evidence/T204_probe_rail.png)",
  "grep of the new test for except/float(/sleep(/wait_for_timeout/setInterval: wait_for_timeout 200 and 800, setInterval 20"
 ],
 "verdict": "fail",
 "scores": {"AC 1 coverage of prepared wording": 2, "input.js late-library fix": 5, "test strength (mutation)": 4, "commit hygiene": 4, "determinism of tests": 4},
 "findings": [
  {"severity": "blocker",
   "title": "Prepared held item still reads 'kept the AI's summary' on the case rail and the AI-check panel, so AC 1 ('no screen ever paints AI wording') is not met",
   "evidence": "app/frontend/stepper.js:523-526 S.HELD_NO_RERUN / S.HELD_CAN_RERUN hard-code \"kept the AI's summary ... the second AI check\", used by heldWords at stepper.js:273 and :292 and by judges.js:96 and :189; none of them checks item.prepared or models.generator_prepared (judges.js:163 does for another sentence). Repro: cp artifacts/review-evidence/T204_probe_rail.py <git archive 9b37b9c>/tests/e2e/test_probe_t204.py; E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_probe_t204.py -q -s. The probe first asserts the entry is prepared (entries[].prepared is True), then output: PROBE rail_all -> [\" You changed the quote on an accepted entry and kept the AI's summary, and the second AI check has no answer on the new quote.\", \"... What you need to do: You changed the quote on an accepted entry and kept the AI's summary, ...\"] and PROBE judge_panel -> [\"... What you need to do: You changed the quote on an accepted entry and kept the AI's summary, and the second AI check has no answer on the new quote.\"]. The card's WATCH in tests/e2e/test_prepared_first_paint.py:14-19 only observes edit-check-hint, edit-compare-prompt and compare-export-note, so the green test cannot see this.",
   "why_it_matters": "D-065 forbids presenting a curated answer as the AI's, and D-069 requires every user-facing string for a prepared item to come from a prepared-specific template. The card's own AC is 'no screen ever' for a prepared case. These sentences are static, not transient, and appear on the same page and item the new test drives, so the card reports a fixed over-claim that is still on screen. This is the GATE-M3 PM blocker class (an over-claim of provenance).",
   "fix": "Give S.HELD_NO_RERUN / S.HELD_CAN_RERUN a prepared twin keyed by the item (isPrepared in the same way as review.js: item.prepared or case models.generator_prepared), without rewriting the AI text. Pass the item or case into heldWords (stepper.js:273, :292) and the two judges.js call sites. Share one isPrepared helper rather than a second copy. Use plural-aware prepared wording (one and many), and keep 'second AI check' only where the real judge is meant, or drop AI to match the card's own regex.",
   "acceptance_test": "Extend tests/e2e/test_prepared_first_paint.py: after the held accept, open the case rail and the AI-check panel and assert no /\\bAI\\b|\\bmodel\\b/i match in gate-blocker, case-step, zs-todo-text and the export-blocked message text (or one page-text scan with a named allow-list for real judge verdict chips such as 'AI did not check'); mutate S.HELD_* back to the AI wording and confirm the test fails."},
  {"severity": "minor",
   "title": "Shared index stages the reverse of the card, including a staged delete of the new test",
   "evidence": "git diff --cached --stat: .claude/hooks/git_guard.py, app/frontend/input.js (6), review.js (12), switcher.js (1), tests/e2e/test_prepared_first_paint.py (104 deletions), tools/tests/test_git_guard.py; git status --short: 'D  tests/e2e/test_prepared_first_paint.py' and '?? tests/e2e/test_prepared_first_paint.py'; MM on the three frontend files. The staged state is the 105d212 tree, left behind when HEAD was moved by plumbing.",
   "why_it_matters": "Any commit without a pathspec (the CLAUDE.md rule exists for this) would silently revert T-204 and the git_guard change from the very commit this review approves, and the tree would show no diff. The 9b37b9c content is fine; the hazard is the index.",
   "fix": "Orchestrator resets the index for those paths (git reset -q -- <the 6 paths>) after confirming nobody has real staged work there; commit by pathspec only.",
   "acceptance_test": "git diff --cached --name-only is empty for those paths and git status does not show the staged D."},
  {"severity": "minor",
   "title": "AC 1 evidence ran on the stale tree and recorded a red; it does not support the checked box",
   "evidence": "Card AC 1 evidence: '555 passed, 1 skipped, 1 failed ... full tests/e2e from git archive of the commit tree'. Note 2026-11-03T00:35:51Z says that run was on the older base tree and only 5 touching files were re-run on 9b37b9c. The AC text is 'full tests/e2e green from a fresh archive'. My run on 9b37b9c: 561 passed, 1 skipped, 0 failed.",
   "why_it_matters": "A checked AC cited a run that was not green and was not on the reviewed commit; evidence should be at the same sha as the commit that ships.",
   "fix": "Re-record AC 1 evidence with the sha and the 561/1/0 result (or this review's log path).",
   "acceptance_test": "AC evidence names 9b37b9c and a green full-suite count."},
  {"severity": "nit",
   "title": "New test settles with fixed timeouts",
   "evidence": "tests/e2e/test_prepared_first_paint.py:31 page.wait_for_timeout(200) before releasing held routes; :101 wait_for_timeout(800) before the negative assertion; WATCH setInterval(scan, 20) at :20. The negative tests have teeth (M6 killed it), so this is a determinism preference, not a failure.",
   "why_it_matters": "Fowler: avoid bare sleeps. Under heavy load 800 ms may elapse before the late event, making the check weaker, not flaky-red.",
   "fix": "Wait on a condition (the held route was released and the library request finished) instead of a sleep.",
   "acceptance_test": "No wait_for_timeout in the file; the three tests and mutants M4-M6 behave as above."}
 ],
 "whats_right": [
  "Prepared fallback sentences in review.js are keyed by the item, not by rewriting the AI text, and the new test watches every text a node held via MutationObserver: three mutants all die.",
  "The zl:switcher event plus a refusing flag rebuilds only the demo refusal; M4, M5 and M6 are each caught by a different one of the three tests.",
  "Replacement commit 9b37b9c has exactly the four intended files on the right parent, and the full tests/e2e is green at that sha (561 passed, 1 skipped)."
 ],
 "questions_for_chris": []}
```
