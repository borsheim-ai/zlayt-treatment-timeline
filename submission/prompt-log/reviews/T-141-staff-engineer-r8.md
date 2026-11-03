# T-141 staff-engineer scoped check, round 8 (fix 78b6a33, HEAD 99438fb)

Verdict: **pass** (0 blockers, 0 majors, 1 minor, 1 nit).

Scope: only the three items named after r7 (the two-digit-year plural-list date guard), plus lib11 unchanged and the conflict suites. Verified on a `git archive 99438fb` copy. The brief names commit 78b6a33 as the card commit. HEAD has moved one commit past it (99438fb, T-161 r2, touches `app/backend/pipeline.py` and T-146/T-161 tests only). `app/backend/conflicts.py` has the same blob (7fffd0b) at 78b6a33 and at HEAD, so the code reviewed is the 78b6a33 code. The e2e red in `tests/e2e/test_conflict_skipped.py` is owned by T-164 and is not counted here.

Results by item:
1. Two-digit-year dates on or after the stated accident date inside a labelled plural history list raise a conflict: PASS. The 25 pins in `tests/unit/test_t141_r7_two_digit_year.py` pass. My 17-row boundary probe matches on 16 rows. The one miss (T14) is a date in a second sentence, which is outside the rule as written (minor, see F1). Before-year two-digit dates stay info (T7, T8, T17). A mutant that disables the two-digit clause (`conflicts.py:80`) turns 10 pins red.
2. The r7 blocker case is fixed: PASS. `'History per patient: car accidents in 2019 and 2022, one on 1/3/26.'` (stated 2026-01-03) now reads conflict. The r7 probe rerun gives 54 rows, 0 mismatches (Q19 ok).
3. lib11 is unchanged: PASS for the case input. `evals/library/case_lib11_priors_and_ledger.txt` is blob 0af8fb2 at ba21b4b, 78b6a33 and 99438fb, and its diff is empty. Note: the sibling `.expected.json` changed in 2ac96cf (T-140, D-062 letter wording, two lines). That is not a T-141 change, so it is not counted against this card.
4. Conflict unit suites: PASS. 579 passed across 10 modules (the 9 from r7 plus the new r7 file). 554 at r7 plus the 25 new pins.

Findings

- **minor, F1 (item 1 boundary):** a labelled plural list followed by a second sentence that names a two-digit date on or after the stated accident date stays info. `History per patient: car accidents in 2019 and 2022. Also one on 1/3/26.` prints info (probe_r8 T14). The four-digit form does the same (T15, the r6 Q28 row). The cause is sentence scope, not the plural exemption: the unit is one sentence (`conflicts.py:87-89`), and `Also one on 1/3/26.` alone has no accident word, so it is info with or without the exemption (`probe_r8_sentence_scope_head_99438fb.txt`: info; `Accident on 1/3/26.` conflict). The written rule is sentence-scoped ("the whole sentence", D-061 / r6 F3), so this is not a violation of the rule as written and I do not rate it a blocker. It is the same loss-of-fact shape the r7 blocker described, and scope cut 13f does not name it. Fix: decide and record it in D-061 (either keep info and say so, or treat a date-only sentence that follows a labelled plural list as a conflict). Acceptance: a pin for T14 that matches the recorded decision.

- **nit, F2 (false conflicts, safe direction):** the two-digit reading is `20xx` for every two-digit year and any slash pair with month 1-12 is read as month/year. `History per patient: car accidents in 2019 and 2022, one on 1/3/99.` reads conflict (probe_r8 T10, 1999 becomes 2099). `... pain 5/30.` reads conflict (T13, 2030). Both are false conflicts that D-055 accepts, so they are not blockers. Fix: record them in 13f or add pins. Acceptance: pins for T10 and T13 with the chosen outcome.

Residuals not counted: none of the r7 F1 forms ('1/3/26', '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26', '1/26') remain open at HEAD.

Exercised
1. Read personas/staff-engineer.md in full; reviews/T-141-staff-engineer-r7.md; memory/SCOPE_CUTS.md line 91 (13f); my r7 memory note.
2. `git rev-parse HEAD` gives 99438fb. `git log --oneline 78b6a33..HEAD` gives one commit (99438fb). `git show 78b6a33 -- app/backend/conflicts.py` read: the new `_TWO_DIGIT_YEARS` regex (conflicts.py:61-66) and the new return clause (conflicts.py:80).
3. `git archive 99438fb | tar -x` into the scratchpad copy `T141r8_head_99438fb`. sha256 of `app/backend/conflicts.py` (a66f164e...) equals `git show 99438fb:app/backend/conflicts.py`.
4. Conflict unit suites on the archive, 10 modules (test_conflicts, test_conflict_candidates, test_t093_j3_controls_reachable, test_t141_checks_per_case, test_t141_r3_variants, test_t116_r4_all_dated_records, test_api_routes, test_t141_d061_closed_exemption, test_t141_r6_probes, test_t141_r7_two_digit_year): `579 passed in 9.15s`. Log: artifacts/review-evidence/T-141-r8/pytest_conflict_suites_head_99438fb.txt.
5. `pytest -v tests/unit/test_t141_r7_two_digit_year.py` on the archive: 25 passed, including test_reviewer_blocker_case_q19. Log: artifacts/review-evidence/T-141-r8/pytest_r7_two_digit_year_head.txt.
6. probe_r7.py (copy of the r7 probe) on the archive: `total=54 mismatches=0`; Q19 ok. Log: artifacts/review-evidence/T-141-r8/probe_r7_head_99438fb.txt.
7. probe_r8.py (17 item-1 boundary rows through accident_date_conflicts / accident_date_note, stated 2026-01-03): 16 match, 1 miss (T14, second sentence). Log: artifacts/review-evidence/T-141-r8/probe_r8_head_99438fb.txt.
8. probe_r8_sentence_scope.py: `Also one on 1/3/26.` info; `Accident on 1/3/26.` conflict; `History: MVC on 1/3/26.` conflict. Log: artifacts/review-evidence/T-141-r8/probe_r8_sentence_scope_head_99438fb.txt.
9. mutant_two_digit_off.py in a fresh copy (`T141r8_mutant_two_digit_off`; the archive is untouched): the conflicts.py:80 return replaced by `return True`. `10 failed, 219 passed`: 9 two-digit ON_OR_AFTER pins and test_reviewer_blocker_case_q19; the four-digit pins still pass. Log: artifacts/review-evidence/T-141-r8/mutant_two_digit_off_result.txt.
10. lib11: `git ls-tree` blob for evals/library/case_lib11_priors_and_ledger.txt is 0af8fb2 at ba21b4b, 78b6a33 and 99438fb. `git diff --stat ba21b4b 99438fb -- evals/library/case_lib11_priors_and_ledger.txt` is empty. `git log --oneline ba21b4b..99438fb -- evals/library/case_lib11_priors_and_ledger.expected.json` gives 2ac96cf (T-140 D-062 wording, two lines in letter_line and good_examples).
11. `python3 tools/board.py show T-164`: T-164 exists (qa, M2) and owns the test_conflict_skipped.py red. That file was not run or counted.

Not run: tests/e2e/test_conflict_skipped.py (T-164), full unit suite, pipeline CLI on sample.txt, eval runner, no server on :7860.

```json
{"card": "T-141", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD 99438fb (card fix 78b6a33 is an ancestor; 99438fb touches pipeline.py and T-146/T-161 tests only). app/backend/conflicts.py (blob 7fffd0b at 78b6a33 and HEAD), tests/unit/test_t141_r7_two_digit_year.py. Archive copy: scratchpad T141r8_head_99438fb. Evidence: artifacts/review-evidence/T-141-r8/. Sample case: evals/library/case_lib11_priors_and_ledger.txt (input). No app URL: unit-level checks only, nothing on :7860.",
 "exercised": [
  "Read personas/staff-engineer.md; reviews/T-141-staff-engineer-r7.md; memory/SCOPE_CUTS.md 13f (line 91).",
  "git rev-parse HEAD (99438fb); git log --oneline 78b6a33..HEAD (one commit); git show 78b6a33 -- app/backend/conflicts.py.",
  "git archive 99438fb into scratchpad T141r8_head_99438fb; sha256 of conflicts.py equals git show 99438fb:app/backend/conflicts.py.",
  "Conflict unit suites on the archive, 10 modules incl. test_t141_r7_two_digit_year.py: 579 passed (pytest_conflict_suites_head_99438fb.txt).",
  "pytest -v tests/unit/test_t141_r7_two_digit_year.py on the archive: 25 passed incl. test_reviewer_blocker_case_q19 (pytest_r7_two_digit_year_head.txt).",
  "probe_r7.py rerun on the archive: total=54 mismatches=0; Q19 ok (probe_r7_head_99438fb.txt).",
  "probe_r8.py: 17 item-1 boundary rows through accident_date_conflicts/accident_date_note, stated 2026-01-03: 16 match, 1 miss T14 second-sentence (probe_r8_head_99438fb.txt).",
  "probe_r8_sentence_scope.py: 'Also one on 1/3/26.' info; 'Accident on 1/3/26.' conflict (probe_r8_sentence_scope_head_99438fb.txt).",
  "mutant_two_digit_off.py in a fresh copy: conflicts.py:80 return replaced by return True; 10 failed, 219 passed (mutant_two_digit_off_result.txt).",
  "git ls-tree blob for evals/library/case_lib11_priors_and_ledger.txt is 0af8fb2 at ba21b4b, 78b6a33, 99438fb; git diff --stat ba21b4b 99438fb on the .txt is empty; .expected.json changed in 2ac96cf (T-140), noted, not counted.",
  "python3 tools/board.py show T-164: owns the test_conflict_skipped.py red; that file not run or counted.",
  "Not run: tests/e2e/test_conflict_skipped.py, full unit suite, pipeline CLI, eval runner, server on :7860."
 ],
 "verdict": "pass",
 "scores": {"item1_two_digit_on_or_after_conflict": 4, "r7_blocker_case_fixed": 5, "lib11_case_input_unchanged": 5, "conflict_unit_suites": 5, "new_clause_pinned_by_mutant": 5, "sentence_scope_consistency": 3},
 "findings": [
  {"severity": "minor",
   "title": "F1: a two-digit date on or after the accident in a second sentence, after a labelled plural list, stays info",
   "evidence": "probe_r8_head_99438fb.txt row T14: 'MISS T14 expect=conflict got=info | History per patient: car accidents in 2019 and 2022. Also one on 1/3/26.'; T15 (four-digit form) info, same shape. conflicts.py:87-89 scopes the plural exemption to one sentence. probe_r8_sentence_scope_head_99438fb.txt: 'info | Also one on 1/3/26.' (no accident word in that sentence); 'conflict | Accident on 1/3/26.'",
   "why_it_matters": "Same loss-of-fact shape as the r7 blocker, but the written rule (D-061, r6 F3 'the whole sentence') is sentence-scoped and the date sits in a sentence with no accident word, so it is not a violation of the rule as written. Scope cut 13f does not name it. I would have decided this differently; it is not counted as a blocker.",
   "fix": "Decide the rule and record it in memory/ORCHESTRATOR_DECISIONS.md D-061: either a date-only sentence that follows a labelled plural list stays info (state that in the rule), or it is a conflict when it names a date on or after the stated accident date.",
   "acceptance_test": "A pin for 'History per patient: car accidents in 2019 and 2022. Also one on 1/3/26.' that matches the recorded decision, for two-digit and four-digit forms."},
  {"severity": "nit",
   "title": "F2: safe-direction false conflicts from two-digit readings (1/3/99 reads 2099; pain 5/30 reads 2030)",
   "evidence": "probe_r8_head_99438fb.txt row T10: conflict for 'History per patient: car accidents in 2019 and 2022, one on 1/3/99.'; row T13: conflict for '... pain 5/30.'. conflicts.py:80 reads every two-digit year as 20xx; _TWO_DIGIT_YEARS (conflicts.py:61-66) matches any month/day or month/year pair.",
   "why_it_matters": "A false conflict is the safe direction under D-055, so this is not a blocker. A paralegal will see extra conflict flags on 1999 dates and on pain scores.",
   "fix": "Record T10 and T13 in scope cut 13f or add pins that name the outcome; narrow the score case only if the team wants fewer false flags.",
   "acceptance_test": "Pins for '1/3/99' and 'pain 5/30' in tests/unit/test_t141_r7_two_digit_year.py with the chosen outcome, and a 13f row if they stay."}
 ],
 "whats_right": [
  "The new two-digit clause is pinned: disabling it turns 9 two-digit ON_OR_AFTER pins and the r7 blocker test red (mutant_two_digit_off_result.txt).",
  "Before-year two-digit controls hold (T7 '12/31/25', T8 'Jan 3, 25', T17 all-before list) and the score and BP controls stay info (T11, T12).",
  "The conflict unit suites pass 579 of 579 across 10 modules, and the r7 probe rerun gives 54 of 54."
 ],
 "questions_for_chris": [
  "Should a date in a following sentence after a labelled plural history list stay info, as the sentence-scoped rule does for four-digit dates today (T14, T15)? I did not count it as a blocker because the written rule is sentence-scoped.",
  "Is the 2ac96cf change to lib11's .expected.json letter wording (T-140, D-062) inside what 'lib11 is unchanged' means for this card? I read it as outside T-141; the input .txt is byte-identical."
 ]}
```
