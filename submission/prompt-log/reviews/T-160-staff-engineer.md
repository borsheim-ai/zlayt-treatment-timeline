# T-160 review: staff-engineer-reviewer (commit 94a31a4)

Scope: commit 94a31a4 (app/frontend/uncovered.js, app/frontend/uncovered.css), checked with tests/e2e/test_polish_r3.py and tests/e2e/test_uncovered_ui.py. HEAD moved to 985dbd2 during the review (3 later commits: a4eeb2b, 67be38d, 985dbd2; none touch the four files). The findings are for 94a31a4. Both shas were run and both pass the two files.

Verdict: pass. 0 blockers, 0 majors, 3 minors, 1 nit. The verdict rule gives pass because no blocker or major was found.

The three checks in the brief:

1. Original budget restored, not loosened: confirmed. The density section of tests/e2e/test_polish_r3.py at 94a31a4 (lines 168-197) matches the pre-T-144 version at ded5ca4^ (budgets 150 and 170 at 1440, 420 at 390, raw getBoundingClientRect height). The only other diff in that file since ded5ca4^ is the T-155 focus-wait line in the shortcut test. The T-144 ROW_BOXES_JS subtraction is gone.
2. Link in the head line, reachable by click and keyboard: confirmed. In the head, the uncovered-summary sits directly after chip--rec (1440 px: summary top 1159.1, chip top 1160.1, same line). From the document start, Tab reaches it on stop 25; Enter then sets aria-expanded to true. A click opens the list (test_one_click_opens_the_record_with_that_sentence_highlighted passes).
3. test_uncovered_ui.py: 7 passed on 94a31a4 and on HEAD.

Findings, in short:
- F1 (minor): the commit and handoff say the rows are back inside the budget. Only the sample case is checked. At 1440 px, a lib09 needs_review row is 179.09 px against a 170 budget, with the link present.
- F2 (minor): the title's premise (rows over budget since T-144) does not reproduce against the budgets the suite enforces. The link added 22 px at 390 on a lib09 row, which was 391 px against a 420 budget.
- F3 (minor): no test fails if the placement is reverted. The density tests pass on the pre-fix placement (802d5fd).
- F4 (minor): "it never takes a line of its own" is false at 320 px. The sample e3 link wraps below its chip.
- F5 (nit): test_keyboard_only starts with summ.focus(), so Tab reach is not asserted by any test.

Full commands and output paths are in the exercised list in the JSON block.

```json
{"card": "T-160", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 94a31a4 (app/frontend/uncovered.js, app/frontend/uncovered.css); tests tests/e2e/test_polish_r3.py and tests/e2e/test_uncovered_ui.py; HEAD 985dbd2 checked (3 later commits, none touch the four files); private app servers on 127.0.0.1:7891 (94a31a4) and 127.0.0.1:7892 (parent 802d5fd), both stopped; fixture backend; sample case and library case case_lib09_spanish_interpreter_espalda",
 "exercised": [
  "read personas/staff-engineer.md; python3 tools/board.py show T-160 (status in_review, commits [94a31a4], AC 1 done with evidence)",
  "git show 94a31a4 (uncovered.js +5/-2 lines, uncovered.css +3 lines; commit subject verbatim: 'the Not in an entry (n) link sits in the entry head line right after the record chip, so it never takes a line of its own; rows are back inside the T-060 compact-row budget (<=2 px)')",
  "git diff ded5ca4^ 94a31a4 -- tests/e2e/test_polish_r3.py (only the shortcut-sheet focus-wait line differs; density section identical to pre-T-144); git log -S for the 150/170/420 budgets (introduced d9efc5c) and for the xfail marker (removed in 802d5fd, not in this commit)",
  "git archive 94a31a4 | tar -x into scratchpad T-160-r1/card-94a31a4; git archive 802d5fd into T-160-r1/parent-802d5fd; git archive 985dbd2 into T-160-r1/head-985dbd2 (scratchpad dirs are under /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad)",
  "card archive: E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_polish_r3.py -q -rsxX -p no:cacheprovider -> 19 passed, 0 skipped, 25.06s (conftest started a private server, no E2E_BASE_URL)",
  "card archive: E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_uncovered_ui.py -v -rsxX -> 7 passed (all 7 named tests PASSED)",
  "card archive, both files again: 26 passed (34.81s); HEAD archive 985dbd2, both files: 26 passed (35.45s)",
  "control on parent 802d5fd: E2E_REQUIRE_DB=1 pytest tests/e2e/test_polish_r3.py -k 'first_screen or 390_needs or row_opens' -> 3 passed, 16 deselected (the placement this card removes is not caught)",
  "own server on 127.0.0.1:7891 (card) and 127.0.0.1:7892 (parent), listener PIDs 4187 and 6083 confirmed with lsof and ps before stopping; both stopped by PID; ports closed afterwards; other listeners (7860, 7875, 8787 and others) not touched",
  "probe measure.py (T-160-r1/probe/measure.py) on 7891 and 7892: every queue row's height with the link and with the uncovered-summary node removed from the DOM (control), head children geometry at 1440 and 390, Tab-from-body reach count; outputs T-160-r1/probe/card-94a31a4.json and T-160-r1/probe/parent-802d5fd.json",
  "probe budget.py (T-160-r1/probe/budget.py) on 7891 and 7892: sample and lib09 rows at 1440 and 390 against the 150/170/420 budgets; outputs T-160-r1/probe/budget-7891.json and budget-7892.json",
  "probe narrow.py (T-160-r1/probe/narrow.py) on 7891 at 320 px: summary and record-chip tops for sample and lib09",
  "not run: the full e2e suite, unit tests, the eval runner (outside the card's AC); no real-data or live-model paths touched"
 ],
 "verdict": "pass",
 "scores": {"budget_restored_not_loosened": 5, "link_in_head_line_click_and_keyboard": 4, "uncovered_ui_tests_green": 5, "test_guards_the_regression": 2, "claims_match_measurements": 3},
 "findings": [
  {"severity": "minor",
   "title": "Commit and handoff say rows are back inside the budget; only the sample case is checked against it",
   "evidence": "T-160-r1/probe/budget-7891.json: lib09@1440 rows e2 needs_review h=179.09 (h_without_link=177.09) and e7 needs_review h=173.09 with no uncovered-summary. The budget is 170 for needs_review (tests/e2e/test_polish_r3.py:180), but the first-screen test uses sample_case (tests/e2e/test_polish_r3.py:168) and no lib09 row is measured at 1440. Commit subject: 'rows are back inside the T-060 compact-row budget (<=2 px)'.",
   "why_it_matters": "The claim is true for the sample only. A paralegal opening the library case sees needs_review rows above the budget the commit cites, and the suite cannot see it. The e7 row is over with no link at all, so the link is not the whole story for that case.",
   "fix": "Scope the commit and card wording to the sample case, or extend the 1440 budget check to lib09 and decide the budget for it (the e7 row at 173.09 with no link is a pre-existing overage).",
   "acceptance_test": "Either a 1440 lib09 assertion (needs_review rows at most 170 px) that passes, or the handoff and card state that the budget covers the sample case only. Repro: the budget probe on any server with lib09 at 1440."},
  {"severity": "minor",
   "title": "The premise (rows over budget since T-144) does not reproduce against the enforced budgets",
   "evidence": "T-160-r1/probe/budget-7892.json (parent 802d5fd, link at end of head): sample@1440 max 138 px (verified budget 150); sample@390 max 330 px; lib09@390 e2 needs_review 391.09 px (budget 420). The density tests pass on the parent: 3 passed (control run, see exercised). Link cost on the parent: +6 px at 1440 and +22 px at 390 (T-160-r1/probe/parent-802d5fd.json, max_row_delta_px 6.0 and 22.0). Card: +2 px at both widths (T-160-r1/probe/card-94a31a4.json).",
   "why_it_matters": "The fix is real and worth having: 22 px at 390 went to 2 px. But the title says the link made rows exceed the budget, and no enforced budget was exceeded by any measured row. A future reader who trusts the title will look for a breach that is not there.",
   "fix": "Restate the title and commit as: the link added 22 px at 390 per row (2 px after the move), and no enforced budget was breached. Keep the 2 px figure.",
   "acceptance_test": "Title and handoff match the probe numbers above; the claim is checkable with the same probe on 802d5fd and 94a31a4."},
  {"severity": "minor",
   "title": "No test fails if the link goes back to the end of the head; the budget test passes on the pre-fix placement",
   "evidence": "git show 94a31a4 -- app/frontend/uncovered.js (the removed line: if (head) head.append(toggle); else row.append(toggle);). Control: E2E_REQUIRE_DB=1 pytest tests/e2e/test_polish_r3.py -k 'first_screen or 390_needs or row_opens' on the parent archive gives 3 passed. The 390 test (tests/e2e/test_polish_r3.py:193-197) uses the lib09 needs_review max, which is 391 on the parent and 371 on the card, both under 420.",
   "why_it_matters": "This card is a layout regression fix. As written, the same regression can come back and every green check stays green. That is the failure mode the persona exists to catch: a fix with no test that fails without it.",
   "fix": "Add one assertion that the uncovered-summary shares the record chip's line at 390 (summary.top minus chip.top is less than the chip height) on lib09, or tighten the lib09 needs_review budget at 390 to 380 px (card 371, parent 391).",
   "acceptance_test": "Put the parent placement (if (head) head.append(toggle)) into a scratch copy of uncovered.js: the new test fails. Restore 94a31a4: it passes. Record both runs in the card's evidence."},
  {"severity": "minor",
   "title": "'It never takes a line of its own' is false at 320 px",
   "evidence": "T-160-r1/probe/narrow.py on 7891 at 320 px: sample e3 uncovered-summary top=1587 left=27 vs chip--rec top=1565 (the link is 22 px below the chip, on its own line). Other sample rows: e5 left=89 top=2223 chipTop=2224 (same line). Comment in app/frontend/uncovered.css:17: '/* T-160: the link lives in the head line; it never takes a line of its own */'.",
   "why_it_matters": "The 320 px reflow requirement is in scope for this UI (test_polish_r3.py:224-233 checks overflow only, and it stays green). The link does not overflow, but it does take its own line on a real row, which contradicts the comment and the commit message.",
   "fix": "Scope the comment and commit wording to 390 and up, or let the head wrap in a way that keeps the link with its chip at 320 (for example, group the chip and link in one flex item).",
   "acceptance_test": "At 320 px for sample and lib09, uncovered-summary.top minus chip--rec.top is smaller than the chip height on every row that has a chip. Repro: narrow.py against the card server."},
  {"severity": "nit",
   "title": "test_keyboard_only starts from summ.focus(), so Tab reach to the link is not asserted",
   "evidence": "tests/e2e/test_uncovered_ui.py:92 summ.focus(). Probe on 7891 (T-160-r1/probe/card-94a31a4.json, tab_reach): from document start, Tab reaches uncovered-summary on stop 25 (stop before: entry-4 row), and Enter gives aria-expanded=true. The test never performs that Tab walk.",
   "why_it_matters": "A tabindex=-1 or a DOM move that takes the link out of the Tab order would pass the test. The card's claim is reachable by keyboard, and the test only proves the button works once focused.",
   "fix": "Add a Tab walk from the document start to the first uncovered-summary, with a stop count bound.",
   "acceptance_test": "Set tabindex=-1 on the link in a scratch copy: the Tab walk test fails. Restore: it passes."}
 ],
 "whats_right": [
  "The density section of tests/e2e/test_polish_r3.py is identical to the pre-T-144 version: budgets 150/170/420 and the raw height. The T-155 subtraction is gone, not loosened.",
  "The link is measured at +2 px per row at 1440 and 390 against a no-link DOM control (22 px to 2 px at 390 versus 802d5fd), and it shares the record chip's line at both widths.",
  "test_uncovered_ui.py is 7 of 7 and test_polish_r3.py is 19 of 19 on the card archive, repeated, and on HEAD with no skips (E2E_REQUIRE_DB=1, private server)."
 ],
 "questions_for_chris": ["Is the 150/170/420 row budget meant for every case or only the sample? lib09 rows are 179.09 px (needs_review, 1440, with the link) and 173.09 px (needs_review, no link, 1440). The answer decides whether F1 is a fix or a scope note."]}
```
