# T-141 staff-engineer scoped check, round 7 (ff1256e, HEAD ba21b4b)

Verdict: **fail** (1 blocker, 1 major).

Scope: only the three items the orchestrator named after r6 (ff1256e), plus lib11 unchanged and the conflict suites. Verified on a `git archive ba21b4b` copy. HEAD ba21b4b differs from ff1256e only in memory/SCOPE_CUTS.md, so the code reviewed is the ff1256e code.

Results by item:
1. Governance per clause: PASS. 19 probe rows (G1-G19) match. 'No prior accidents and was rear-ended 3/1.' is a conflict.
2. Plural and bare hit/impact forms: PASS for every form in the r6 F2 spec and the orchestrator's list (20 rows, P1-P20, plus controls). Residual bare-hit phrasings ('Hit in the head', 'Hit the windshield', 'Hit his head') read info-only. Not counted: they are residual phrasings under scope cut 13f.
3. Plural-history exemption vs date on/after the accident, or this/the/current: FAIL. Q15, Q11, and the this/the/current/last rows hold, but a labelled plural list that names the accident date in a two-digit-year form still prints info. Blocker (finding 1). I did not count it under 13f: 13f records word-rule phrasings that D-061 leaves info, and this is a date the rule names explicitly and the code's own comment says it covers ('a year counts at its year', conflicts.py:61-62).

Also checked: lib11 is byte-identical from 824984f to HEAD (blob 0af8fb2). The conflict unit suites pass (554 across 9 modules). The e2e file that tests the lib11 conflict UI is red at HEAD (finding 2). The red predates ff1256e.

Findings

- **blocker, F1 (item 3):** a labelled plural list that names the accident date with a two-digit year stays info. 'History per patient: car accidents in 2019 and 2022, one on 1/3/26.' (stated accident date 2026-01-03) prints info. Date forms in the same miss class: '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26', '1/26'. The guard at conflicts.py:67 counts only parsed dates; `dates.find_dates` returns status 'ambiguous' with no iso for numeric forms like '1/3/26', and 'Jan 3, 26' and '3rd Jan 26' are not parsed either. The year fallback at conflicts.py:69 only matches four-digit years. Repro: probe_r7.py row Q19 (artifacts/review-evidence/T-141-r7/probe_r7_head_ba21b4b.txt: 'MISS Q19 item3 expect=conflict got=info'). Pins: `grep -c "/26" tests/unit/test_t141_r6_probes.py` returns 0. Mutant (mutant_plural_guard_off.txt): disabling the parsed-date and referent clauses turns only X12 and X13 red. Q15 and Q11 are carried by the four-digit-year clause alone, so the two-digit form is the untested hole.
  Why it matters: item 3 says the exemption does not apply when the list names a date on or after the accident. The code hides that date conflict, which loses a fact the paralegal needs (D.2 blocker). The gap is in the code, not in D-061's wording, so it is not the major-class gap r6 recorded for Q15.
  Fix: in `_plural_list_ok` (conflicts.py:60-69), read a two-digit year as 20xx and compare it with the stated year. Also treat an 'ambiguous' numeric date whose year is on or after the stated year as on or after it (safe direction, D-055). Keep the parsed-date and four-digit-year clauses.
  Acceptance test: probe_r7.py row Q19 prints conflict. Add pins to tests/unit/test_t141_r6_probes.py for '1/3/26', '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26' and '1/26' on the stated date, each conflict. 'one 2015' and the lib11 record 1 text stay info. A mutant that removes the new two-digit clause turns the new pins red.

- **major, F2 (conflict suite, e2e):** tests/e2e/test_conflict_skipped.py is 8 of 9 red on HEAD. The red is not from ff1256e. The same file passes 9 of 9 at 824984f (the r6-reviewed commit) and is 8 of 9 at 83f1afd (the parent of ff1256e) and at acad4f6. At 6379c0b and c2913a6, tests/e2e/conftest.py has a SyntaxError (line 89), so the module does not collect there. Evidence: pytest_e2e_skip_824984f.txt ('9 passed'), pytest_e2e_skip_83f1afd.txt and pytest_e2e_skip_acad4f6.txt ('8 failed, 1 passed'), pytest_e2e_skip_6379c0b.txt and pytest_e2e_skip_c2913a6.txt (collection error), pytest_lib11_modules_head.txt lines 30 and 45 (test_conflict_skipped.py:69 and :83). The UI difference I could establish: at HEAD the case opens on the Case overview step and `[data-testid="flags-panel"]` is not in the DOM after the timeline loads (repro_lib11_ui_head.txt: 'no flags-panel on open'). At 824984f the panel is present on open with 2 conflict cards and 1 note (repro_lib11_ui_824984f.txt). The backend data is correct at HEAD (repro_lib11_api_head.txt: denial_vs_history checked, skipped [], 1 RECORDS_PREDATE_ACCIDENT note, 2 pending conflict flags). I did not find the route from the overview to the flags panel at HEAD; clicking btn-start-review did not reveal it in my script.
  Why it matters: the brief asks me to confirm the conflict suites pass. This module is a conflict suite and it is red at HEAD. Whether the landing step change is intended (frontend commits in 824984f..acad4f6, e.g. 6379c0b, 0b2ce9c) or the test is stale is an orchestrator decision, so I rate it major, not blocker.
  Fix: decide the intended landing. Either restore the flags group on open for a case with conflicts, or update the test to the documented route to the flags group and say so in the test. Also add a collection check so a conftest SyntaxError cannot hide a red suite.
  Acceptance test: `tests/e2e/test_conflict_skipped.py` 9 of 9 on a git archive of the fix commit. repro_lib11_ui.py shows the conflict group with the lib11 note and the two denial cards on the documented route.

Residuals not counted (scope cut 13f)
- Bare hit forms outside the r6 F2 spec read info: 'Hit in the head in October 2025.', 'Hit the windshield in October 2025.', 'Hit his head in 2025.' (probe output in probe_r7_head_ba21b4b.txt is the item-2 set; these three were run inline with the same function).
- 13f names 'Denies any accident on 01/03/2026' (info) and 'No prior accidents or collisions' (conflict). The second has the same shape as G7 and conflicts. I did not re-run the first.

Minor (I would have done it differently; does not violate the rule as written)
- Q27 'History per patient: car accidents in 2019 and 2022, treated at the clinic.' is a conflict because the literal word 'the' is in `_PLURAL_REFERENT` (conflicts.py:30). The rule text says 'this/the/current', so this matches it. Narrowing to 'the latest' or 'the most recent' would avoid false conflicts on benign lists. Safe direction.

Exercised
1. Read personas/staff-engineer.md in full; reviews/T-141-staff-engineer-r6.md; `python3 tools/board.py show T-141` (notes through the 15:11:07 dispatch); memory/ORCHESTRATOR_DECISIONS.md D-061 (line 69); memory/SCOPE_CUTS.md 13f (line 91); my T-141 r5, r6 and evidence-sha memory notes.
2. `git log --oneline -3` shows ba21b4b, ff1256e, 83f1afd. `git diff --stat ff1256e HEAD` shows memory/SCOPE_CUTS.md only.
3. `git archive ba21b4b | tar -x` into the scratchpad copy T141r7_head. sha256 of app/backend/conflicts.py (32433731...) equals `git show ba21b4b:app/backend/conflicts.py`.
4. Conflict unit suites on the archive, `.venv/bin/python -I -m pytest -q -p no:cacheprovider` over 9 modules (test_conflicts, test_conflict_candidates, test_t093_j3_controls_reachable, test_t141_checks_per_case, test_t141_r3_variants, test_t116_r4_all_dated_records, test_api_routes, test_t141_d061_closed_exemption, test_t141_r6_probes): 554 passed. Log: pytest_conflict_suites_head.txt.
5. lib11-referencing modules on the archive (the 9 above minus the ones not referencing lib11, plus test_amounts_t140, test_t139_unmarked and tests/e2e/test_conflict_skipped.py): 8 failed, 590 passed. All 8 failures are in test_conflict_skipped.py. Log: pytest_lib11_modules_head.txt.
6. e2e skip file on archives 824984f, 83f1afd, acad4f6, 6379c0b, c2913a6 (logs pytest_e2e_skip_<sha>.txt).
7. lib11: `git ls-tree` blob for evals/library/case_lib11_priors_and_ledger.txt is 0af8fb2 at 824984f, ff1256e and ba21b4b. `git diff --stat 824984f ba21b4b -- evals/library/case_lib11_priors_and_ledger.*` is empty.
8. Probe set for the three items, probe_r7.py run on the archive: 54 rows, 53 match, 1 miss (Q19). Log: probe_r7_head_ba21b4b.txt. Inline `dates.find_dates` and `_describes_event` checks on 14 date spellings (output in the exercised notes above).
9. Private fixture server from the archive, lib11 run through the HTTP API (repro_lib11_api.py): repro_lib11_api_head.txt.
10. Headless Chromium on the archive servers (repro_lib11_ui.py): repro_lib11_ui_head.txt (no flags-panel on open) and repro_lib11_ui_824984f.txt (conflict group, 2 cards, 1 note).
11. Mutant in a fresh scratch copy (mutant_guard.py, no product file touched): parsed-date and referent clauses of `_plural_list_ok` disabled. tests/unit/test_t141_r6_probes.py and test_t141_d061_closed_exemption.py: 2 failed (X12, X13), 202 passed. Log: mutant_plural_guard_off.txt.
12. `grep -c "/26" tests/unit/test_t141_r6_probes.py`: 0.
13. `python3 tools/board.py validate`: ok (163 files), before this file was written.
Not run: full unit suite (the handoff reports other cards' dirty files), pipeline CLI on sample.txt, eval runner, live judge controls, E2E beyond the skip file. No server on :7860.

```json
{"card": "T-141", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git ba21b4b (HEAD; code identical to ff1256e, only memory/SCOPE_CUTS.md differs). app/backend/conflicts.py, tests/unit/test_t141_r6_probes.py, tests/unit/test_t141_d061_closed_exemption.py, tests/e2e/test_conflict_skipped.py. Evidence: artifacts/review-evidence/T-141-r7/. App: private fixture servers started from git archives on loopback (lib11 library case); nothing on :7860.",
 "exercised": [
  "Read personas/staff-engineer.md; reviews/T-141-staff-engineer-r6.md; board.py show T-141; memory/ORCHESTRATOR_DECISIONS.md D-061; memory/SCOPE_CUTS.md 13f.",
  "git log -3 (ba21b4b, ff1256e, 83f1afd); git diff --stat ff1256e HEAD (memory/SCOPE_CUTS.md only); git archive ba21b4b into scratchpad T141r7_head; sha256 of conflicts.py matches git show.",
  "Conflict unit suites on the archive, 9 modules incl. test_t141_r6_probes: 554 passed (pytest_conflict_suites_head.txt).",
  "lib11-referencing modules on the archive, 9 modules incl. tests/e2e/test_conflict_skipped.py: 8 failed, 590 passed; all 8 failures in test_conflict_skipped.py (pytest_lib11_modules_head.txt).",
  "tests/e2e/test_conflict_skipped.py on archives 824984f (9 passed), 83f1afd (8 failed), acad4f6 (8 failed), 6379c0b and c2913a6 (conftest SyntaxError at line 89); logs pytest_e2e_skip_<sha>.txt.",
  "lib11 blob 0af8fb2 at 824984f, ff1256e, ba21b4b (git ls-tree); git diff --stat 824984f ba21b4b on lib11 files is empty.",
  "probe_r7.py on the archive: 54 rows (G1-G19 governance, P1-P20 plural and bare forms, Q11-Q28 labelled-list date and referent guard): 53 match, 1 miss Q19 (probe_r7_head_ba21b4b.txt).",
  "dates.find_dates and _describes_event on 14 date spellings (1/3/26, 01/03/26, 3/27/26, 1-3-26, 01.03.26, Jan 3, 26, 3rd Jan 26, 1/26, 1/3/2026, 01/03/2026, Jan 3 2026, 2026-01-03, in Jan 2026, 01/2026).",
  "repro_lib11_api.py on the HEAD archive: status ready, conflict_types include denial_vs_history, skipped [], 1 RECORDS_PREDATE_ACCIDENT note, 2 pending conflict flags (repro_lib11_api_head.txt).",
  "repro_lib11_ui.py (headless Chromium) on HEAD: no flags-panel on open, case opens on Case overview (repro_lib11_ui_head.txt); on 824984f: conflict group with 2 cards and 1 note (repro_lib11_ui_824984f.txt).",
  "mutant_guard.py on a fresh scratch copy: parsed-date and referent clauses of _plural_list_ok disabled; r6 probes and d061 suite: 2 failed (X12, X13), 202 passed (mutant_plural_guard_off.txt).",
  "grep -c '/26' tests/unit/test_t141_r6_probes.py: 0 two-digit-year rows.",
  "python3 tools/board.py validate: ok (163 files).",
  "Not run: full unit suite, pipeline CLI on sample.txt, eval runner, live judge controls, E2E beyond the skip file."
 ],
 "verdict": "fail",
 "scores": {"item1_per_clause_governance": 5, "item2_plural_and_bare_forms": 4, "item3_plural_list_date_guard": 2, "lib11_unchanged": 5, "conflict_unit_suites": 5, "conflict_e2e_suite": 2, "tests_assert_behaviour": 3, "llm_code_boundary": 5},
 "findings": [
  {"severity": "blocker",
   "title": "F1 (item 3): a labelled plural list that names the accident date with a two-digit year stays info",
   "evidence": "probe_r7.py row Q19 in artifacts/review-evidence/T-141-r7/probe_r7_head_ba21b4b.txt: 'MISS Q19 item3 expect=conflict got=info | History per patient: car accidents in 2019 and 2022, one on 1/3/26.' Date guard counts parsed dates only (conflicts.py:67); find_dates returns status 'ambiguous' with no iso for '1/3/26'; 'Jan 3, 26' and '3rd Jan 26' are not parsed. Year fallback matches four-digit years only (conflicts.py:69). grep -c '/26' tests/unit/test_t141_r6_probes.py = 0. mutant_plural_guard_off.txt: disabling the parsed-date and referent clauses turns only X12, X13 red.",
   "why_it_matters": "Item 3 says the plural-history exemption does not apply when the list names a date on or after the accident. The code hides that date conflict for two-digit-year and month-name short forms, so a fact the paralegal needs is lost (D.2 blocker). The gap is in the code, not in D-061's wording, so it is not the major-class wording gap r6 recorded for Q15. Scope cut 13f does not cover it: 13f records word-rule phrasings that D-061 leaves info, and this date is inside the rule the orchestrator named.",
   "fix": "In _plural_list_ok (conflicts.py:60-69), read a two-digit year as 20xx and compare it with the stated year. Treat an ambiguous numeric date whose year is on or after the stated year as on or after it (safe direction, D-055). Keep the parsed-date and four-digit-year clauses.",
   "acceptance_test": "probe_r7.py row Q19 prints conflict. New pins in tests/unit/test_t141_r6_probes.py: '1/3/26', '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26', '1/26' on the stated date each conflict; 'one 2015' and the lib11 record 1 text stay info. A mutant removing the new two-digit clause turns the new pins red."},
  {"severity": "major",
   "title": "F2 (conflict suite): tests/e2e/test_conflict_skipped.py is 8 of 9 red on HEAD; the red predates ff1256e",
   "evidence": "pytest_lib11_modules_head.txt:30 (test_conflict_skipped.py:69, conflict-note count 0) and :45 (:83, data-item-id count 0). pytest_e2e_skip_824984f.txt '9 passed'; pytest_e2e_skip_83f1afd.txt and pytest_e2e_skip_acad4f6.txt '8 failed, 1 passed'; pytest_e2e_skip_6379c0b.txt and pytest_e2e_skip_c2913a6.txt: SyntaxError in tests/e2e/conftest.py (line 89). repro_lib11_ui_head.txt: 'no flags-panel on open' (case opens on Case overview). repro_lib11_ui_824984f.txt: conflict group count 1, 2 cards, 1 note. repro_lib11_api_head.txt: backend data correct (denial_vs_history checked, skipped [], 1 note, 2 pending conflict flags).",
   "why_it_matters": "The brief asks for confirmation that the conflict suites pass. This module is a conflict suite and it is red at HEAD, and the lib11 conflict is not visible on open in the browser. The red is not from the ff1256e logic (the API output is correct and the file is red at 83f1afd, the parent). Whether the landing change is intended (frontend commits between 824984f and acad4f6, e.g. 6379c0b and 0b2ce9c) or the test is stale is an orchestrator decision, so it is major, not blocker. I did not establish the route from the overview to the flags group at HEAD.",
   "fix": "Decide the intended landing. Either show the flags group on open for a case with conflicts, or update the test to the documented route to the flags group and say so in the test. Add a collection check so a conftest SyntaxError cannot hide a red suite.",
   "acceptance_test": "tests/e2e/test_conflict_skipped.py 9 of 9 on a git archive of the fix commit. repro_lib11_ui.py shows the lib11 note and the two denial cards on the documented route."}
 ],
 "whats_right": [
  "Item 1 holds: 19 governance rows match, including 'No prior accidents and was rear-ended 3/1.', the r6 F1 examples and semicolon and comma splits; the walk crosses and/or/with/for/of only to injury words (conflicts.py:50).",
  "Item 2 holds for every r6 F2 form: plural collisions, MVAs, MVCs, MVIs, crashes, wrecks, incidents, 'hit from', 'hit by', 'hit a object', bare and plural impact; 'Patient hit her weight goal' and 'Impact of ...' stay info.",
  "lib11 is byte-identical from 824984f to HEAD (blob 0af8fb2), and the 9 conflict unit modules pass 554 of 554."
 ],
 "questions_for_chris": [
  "Was the case landing on Case overview (not the flags group) an intended change? The lib11 e2e test assumes the flags group on open and is red at HEAD.",
  "Does scope cut 13f cover the bare-hit residuals ('Hit in the head', 'Hit the windshield')? I read 13f as covering them and I did not count them. I read it as not covering the two-digit-year date miss in F1."
 ]}
```
