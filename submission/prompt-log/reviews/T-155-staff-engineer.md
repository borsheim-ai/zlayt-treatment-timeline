# T-155 review (staff-engineer-reviewer): e2e triage, commit 20b3a42 (tests only)

**Verdict: changes** (0 blockers, 2 majors, 2 minors, 1 nit). Reviewed at HEAD 20b3a42 (`git rev-parse HEAD`), tree from `git archive 20b3a42`.

## What I checked

- **Decisions.** D-059 (ORCHESTRATOR_DECISIONS.md:67) explains the L6 count change, and the count matches the live judge output. The T-134 r2 `edit_to_check` wording matches memory/contracts/api.md:370 and app/backend/trace.py:289. D-058 has no assertion in this diff, so it is not applicable here. The T-144 row-height edit does not follow any decision. Its stated premise is false at HEAD (see F2).
- **Red at the reviewed commit.** `test_first_screen_shows_entries_and_rows_are_compact` fails 3 of 3 runs at 20b3a42 (`552 < 520`, tests/e2e/test_polish_r3.py:181). The card's green evidence cites 078c5ae, which is 11 commits behind HEAD (F1).
- **Density edit.** At 078c5ae the original density budgets really fail (`179 <= 150`, `430 <= 420`). f262223 fixed that upstream. At HEAD the original budgets pass, and the collapsed list costs 0 px. The T-155 edit therefore removes a measure that was not needed and discounts 8 px on list rows (F2).
- **T-158.** The 390px refusal box really can end below the fold. The mechanism is that the box sits 132 px under the Accept button, so it is out of a 844 px viewport whenever the button is lower than y=580. One of 24 probe samples hit that (scrollY 734, box bottom 937). The "about 50%" rate on the card was not reproduced. T-158 is the right owner for the product fix (F3).
- **L6 count and EDIT_WAITING.** Both follow the recorded decisions. The count assertion is weak on identity (F4), and one test name is stale (F5).

Evidence files: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-155/` (probe scripts and outputs). Scratch snapshot: `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T155_r1/`.

## Findings

**F1 (major). The card's green claim cites 078c5ae, not the reviewed commit. The first-screen test is red at 20b3a42 and is not triaged.**
Repro: `E2E_BASE_URL=http://127.0.0.1:7955 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_polish_r3.py -k first_screen` on the 20b3a42 archive prints `AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]` at tests/e2e/test_polish_r3.py:181. It failed in 3 of 3 runs. At 078c5ae the same line read `[[518, ...` (artifacts/review-evidence/T-155/at078_density.txt), so the red came in after that sha. The orchestrator note at 14:39 names it. The handoff triage does not.

**F2 (major). The T-144 row-height edit weakens the compact-row budget on a false premise. The density reds it calls stale were real.**
- The density reds at 078c5ae were real: `assert 179 <= 150` and `assert 430.09375 <= 420` (at078_density.txt). f262223 ("the uncovered list opens from a short link in the entry head so compact rows keep their height") is in 078c5ae..20b3a42 and is the fix.
- At 20b3a42 the original measure passes. I removed only line 181 from the pre-change file (`git show 20b3a42^:tests/e2e/test_polish_r3.py`). Then `pytest -k "first_screen or 390"` gave `2 passed`. The current file with the same single-line removal also gave `2 passed`.
- The collapsed list costs 0 px at HEAD. `app/frontend/uncovered.js:21` sets `hidden: !opened.has(entry.id) || null`, and `app/frontend/uncovered.css:4` is `.unc[hidden] { display: none; }`. On the sample at 1440x900 and 390x800, the list is `display: none` with height 0 and computed `margin-top: 8px` on 3 of 9 rows (artifacts/review-evidence/T-155/rows_head.txt).
- The edit at tests/e2e/test_polish_r3.py:168-172 says "~30-57 px with its margins". The ROW_BOXES_JS function subtracts that margin from every row that carries a list, and it is used at :180 and :203. So those rows read 8 px short of the rendered height.
- The constraint itself is real. The T-060 compact-row budget (150/170 px at 1440, 420 px at 390) guards the first screen. The edit does not make that constraint go away, but it does make the measure wrong.

**F3 (minor). T-158 holds the real regression. The "about 50%" rate is not reproduced.**
- Mechanism: the box is `btn_y + 132` at every sample. It is below 844 whenever btn_y is greater than 580. One sample hit it: `{"scrollY": 734, "box_y": 805, "box_bottom": 937, "btn_y": 673, "below_fold": true}` (artifacts/review-evidence/T-155/stub6.txt).
- Rate: 1 of 6 (stub), 0 of 10 (stub), 0 of 8 (real), so 1 of 24 in total (stub6.txt, stub10.txt, real8.txt). In pytest, `test_code_check_refusal.py -k 390` passed in 9 runs, 36 cases in total (t158_mobile_repeat.txt). Load averages were 21 to 24 during these runs (`uptime`). I cannot say what the card's machine was doing.
- The test is correct and stays unchanged. The T-158 note should cite the geometry measurement, not the 3-of-6 rate.

**F4 (minor). The L6 count change asserts a count, not which item moved.**
- `L6_OBJECTIONS = 4` (tests/e2e/test_stepper.py:23). The four rejections on /judges are a3 (unclear $450), a4 (unclear $1,550), a7 (unclear $1,150) and flag f_r5_1 (artifacts/review-evidence/T-155/l6_head.txt).
- The count follows D-059. Whether a7 is correct billing is outside my lens.
- Because the test checks only the count, another item could replace a7 and the test would still pass.

**F5 (nit). A test name overstates what it asserts.**
- tests/e2e/test_rerun_judge.py:308 `test_passing_edit_says_edited_by_you_not_ai_checked_everywhere` now asserts `EDIT_WAITING` for the Why dialog (:318). The D-045(b) wording is still asserted in the panel row (:314). The name should say panel and judge step.

## Notes on what I did not run

- The full tests/e2e suite and tests/unit were not run. The brief asked for the changed files and T-158.
- No mutation check was run on the edited files. Acceptance tests for F2 and F4 are written as proposals and have not been run.
- I did not run `board.py review`.

```json
{"card": "T-155", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 20b3a42 (tests only: tests/e2e/test_polish_r3.py, tests/e2e/test_rerun_judge.py, tests/e2e/test_stepper.py); reviewed at HEAD 20b3a42 from git archive in a scratch snapshot; own server 127.0.0.1:7955 (fixture backend, ZLAYT_MODE=local, E2E_REQUIRE_DB=1); comparison server 127.0.0.1:7956 from archive 078c5ae; library case case_lib06_lop_billed_vs_adjusted and the sample case",
 "exercised": [
   "python3 tools/board.py show T-155; read personas/staff-engineer.md",
   "git show --stat 20b3a42; git show 20b3a42 -- tests/ (full test diff); git rev-parse HEAD -> 20b3a42",
   "git log --oneline 078c5ae..20b3a42 (11 commits); git diff --stat 078c5ae 20b3a42 -- app (13 files)",
   "read memory/ORCHESTRATOR_DECISIONS.md D-058 (line 66), D-059 (67), D-060 (68); memory/contracts/api.md lines 365-374; app/backend/trace.py:289; app/frontend/uncovered.js:21; app/frontend/uncovered.css:4; app/frontend/tokens.css:43; commit f262223 subject",
   "git archive 20b3a42 extracted to scratch T155_r1/head (2217 files); 48 untracked tests/fixtures/llm files in the working tree not copied; no FIXTURE_MISS occurred",
   "E2E_BASE_URL=http://127.0.0.1:7955 ZLAYT_DB=<scratch>/e2e.sqlite3 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_polish_r3.py tests/e2e/test_rerun_judge.py tests/e2e/test_stepper.py tests/e2e/test_code_check_refusal.py -q -rfEs -> 1 failed, 83 passed, 128.70s; failure test_polish_r3.py::test_first_screen_shows_entries_and_rows_are_compact at :181 (552 < 520)",
   "3 repeats of test_polish_r3.py -k first_screen on 20b3a42: 552 each run",
   "pytest test_code_check_refusal.py -k 390 x8 on 20b3a42: 4 passed each run (artifacts/review-evidence/T-155/t158_mobile_repeat.txt)",
   "probe_t158.py (Playwright 390x844, stub 6 and 10, real 8 samples): 1 of 24 below the fold (stub6.txt, stub10.txt, real8.txt)",
   "probe_rows.py on 20b3a42: uncovered-list display none, height 0, margin-top 8px on 3 of 9 rows at 1440x900 and 390x800 (rows_head.txt)",
   "pre-change test file (git show 20b3a42^) and current file, each with only line 181 removed: pytest -k 'first_screen or 390' -> 2 passed each",
   "server 127.0.0.1:7956 from archive 078c5ae: density budgets fail 179 <= 150 and 430.09 <= 420; first-entry y 518 (at078_density.txt)",
   "probe_l6.py and probe_l6b on 20b3a42: judge rejections a3, a4, a7, f_r5_1; a3 unclear $450, a4 unclear $1,550, a7 unclear $1,150 (l6_head.txt)",
   "uptime: load average 21 to 24 during the runs",
   "stopped only my PIDs (listeners 64260 and 86463 and their bash wrappers 64258 and 86406), verified via lsof and cwd; ports 7955 and 7956 closed; shared :7860 untouched",
   "not run: full tests/e2e, tests/unit, evals, mutation checks; board.py review not run"
 ],
 "verdict": "changes",
 "scores": {"test_integrity": 2, "triage_accuracy": 2, "evidence_matches_reviewed_commit": 2, "decision_traceability": 4, "determinism": 4},
 "findings": [
   {"severity": "major",
    "title": "Green claim cites 078c5ae, not the reviewed commit; first-screen test red at 20b3a42 and not triaged",
    "evidence": "tests/e2e/test_polish_r3.py:181 `AssertionError: [[552, 138, 'verified'], [698, 138, 'verified']]` on git archive 20b3a42, 3 of 3 runs; at078_density.txt shows 518 at 078c5ae; git log --oneline 078c5ae..20b3a42 lists 11 commits; card AC evidence says 'clean HEAD 078c5ae ... 281 passed, 2 skipped, 1 failed'",
    "why_it_matters": "The AC requires a green clean-HEAD run with each failure explained on the card. The commit under review is red for a test the card neither fixes nor explains, and the cited evidence describes another tree. A gate reviewer reproducing the card gets a different result.",
    "fix": "Re-run the full tests/e2e on git archive 20b3a42 with E2E_REQUIRE_DB=1, cite that sha and the counts in the AC evidence, and record on the card the owner of the first-screen failure (T-149 r2) or file a card. Do not loosen line 181 inside this card.",
    "acceptance_test": "Full tests/e2e on the 20b3a42 archive: every failure has a card note naming its owner or a passing result; the AC evidence cites 20b3a42."},
   {"severity": "major",
    "title": "T-144 row-height edit weakens the compact-row budget on a false premise; the density reds it calls stale were real",
    "evidence": "at078_density.txt: `assert 179 <= 150` and `assert 430.09375 <= 420` at 078c5ae; f262223 fixed it in 078c5ae..20b3a42. At 20b3a42 the original measure passes: pre-change file with line 181 removed, `-k 'first_screen or 390'` -> 2 passed. rows_head.txt: uncovered-list display none, height 0, margin-top 8px on 3 of 9 rows. app/frontend/uncovered.js:21 `hidden: !opened.has(entry.id) || null`; app/frontend/uncovered.css:4 `.unc[hidden] { display: none; }`. tests/e2e/test_polish_r3.py:168-172 comment '~30-57 px with its margins' and ROW_BOXES_JS subtracting extra; used at :180 and :203.",
    "why_it_matters": "The T-060 compact-row budget (150/170 px at 1440, 420 px at 390) guards the first screen and is still a real constraint. The edit removes a term that is zero at HEAD, the stated reason is false, and it discounts 8 px of an unrendered margin on list rows, so the budget reads short. Any future visible collapsed element would be hidden from the budget under the same comment.",
    "fix": "Revert ROW_BOXES_JS to the pre-20b3a42 measure (r.height) at tests/e2e/test_polish_r3.py:170-172, :180 and :203, and remove the T-144 comment at :168-169. Leave line 181 as it is (see F1).",
    "acceptance_test": "On the reverted file, `pytest tests/e2e/test_polish_r3.py -k 'density or 390'` passes at 20b3a42. Mutation in a scratch copy: `.unc[hidden]{display:block}`; the 390 or 1440 budget test must fail. If it does not, the card must say the budget does not guard the list area."},
   {"severity": "minor",
    "title": "T-158 holds the real regression, but the about-50% rate on the card is not reproduced",
    "evidence": "probe_t158.py: stub 1 of 6 (stub6.txt, `{\"scrollY\": 734, \"box_y\": 805, \"box_bottom\": 937, \"btn_y\": 673, \"below_fold\": true}`), stub 0 of 10 (stub10.txt), real 0 of 8 (real8.txt); box_y = btn_y + 132 in every sample; pytest -k 390 passed 36 cases in 9 runs (t158_mobile_repeat.txt); uptime load 21-24",
    "why_it_matters": "The mechanism is real and T-158 (frontend) is the right owner, so leaving test_code_check_refusal.py unchanged is correct. The 3-of-6 rate is not reproduced, and a repro should rest on measured geometry, not a rate.",
    "fix": "On T-158, replace the about-50% claim with the geometry measurement (btn_y, scrollY, box bottom) and keep the test unchanged.",
    "acceptance_test": "T-158 AC adds a probe with at least 30 samples at 390x844 showing the accept-refused box inside the viewport for every sampled scrollY, plus the existing 10 consecutive green runs."},
   {"severity": "minor",
    "title": "L6 count change asserts a count, not which item moved",
    "evidence": "tests/e2e/test_stepper.py:23 `L6_OBJECTIONS = 4`; judge rejections a3 ($450), a4 ($1,550), a7 ($1,150), f_r5_1 (l6_head.txt); D-059 at memory/ORCHESTRATOR_DECISIONS.md:67",
    "why_it_matters": "The count follows D-059, so the update is right. But a count of 4 still passes if a different item replaces a7, so the test does not protect the item the decision is about.",
    "fix": "Keep the count and add a presence check that the record-5 'Amount due' amount (a7) is in the judge rejections for the case.",
    "acceptance_test": "Mutation: classify 'Amount due' as charge in a scratch copy; the stepper judge tests fail on the presence check, not only on the count."},
   {"severity": "nit",
    "title": "Test name says 'everywhere' but the Why dialog now asserts EDIT_WAITING",
    "evidence": "tests/e2e/test_rerun_judge.py:308 test_passing_edit_says_edited_by_you_not_ai_checked_everywhere; :318 asserts EDIT_WAITING; :314 keeps the D-045(b) panel wording",
    "why_it_matters": "A reader would think the D-045(b) wording is asserted in the Why dialog. It is not.",
    "fix": "Rename to match the assertions (for example ..._in_the_panel_and_judge_step); keep the docstring.",
    "acceptance_test": "The renamed test passes unchanged in assertions."}
 ],
 "whats_right": [
   "L6 count 4 follows D-059: a3 $450, a4 $1,550 and a7 $1,150 are class unclear and flag f_r5_1 is a rejection on /judges (probe_l6.py, l6_head.txt)",
   "EDIT_WAITING matches memory/contracts/api.md:370 and app/backend/trace.py:289; the D-045(b) panel assertion at test_rerun_judge.py:314 still stands",
   "The shortcut-sheet change waits on a condition (test_polish_r3.py:59, focus back on btn-shortcuts) instead of sleeping, and fails loudly on timeout"
 ],
 "questions_for_chris": [
   "After T-149 added the case overview block, the first entry sits at y=552 at 1440x900 (518 at 078c5ae). Is the 520 px 'first entry above the fold' rule (test_polish_r3.py:181) still the product rule, or should the overview block give way? The first Accept is still on screen (y+h < 900)."
 ]}
```
