# T-141 staff-engineer review, round 4 (93a2ffc), scoped check

Verdict: **changes** (0 blockers, 1 major, 1 nit).

Scope was limited to the three checks in the brief. Against the section 7.4 rule, 32 of the 33 r3 variants behave correctly. The miss is Y3, "Rear-ended in October 2025" in a 2026-01-05 record. It stays info-only because the month-year cut-off is still two months (conflicts.py:61), while the same record with "November 2025" (Y2) raises a conflict. The r3 acceptance test asked for Y1 and Y3 to conflict; Y1 was fixed and Y3 was pinned as info.

- Negated generic prior history (N1, N2, N3): info. Correct, including N3 "Denies any motor vehicle collision or injury".
- Explicitly prior history (N4 "MVA in 2015", N5 "History of MVA 2015", N6 "Hx: rear-end collision 2018", H11 "MVA remote past"): info. Correct under my reading that a dated or Hx/remote-labelled prior is explicit prior. See questions_for_chris.
- Negated or governed mechanisms (T1 to T10, including "No LOC after the accident", "Has not worked since the accident", "No airbag deployment in the collision"): all conflict. Correct.
- History label or prior-marker wrapped mechanisms (H1 to H10, including "History: rear-ended", "Prior to arrival, pt was in MVC"): all conflict. Correct.
- Bare year and month-year mechanisms (Y1, Y2): conflict. Correct. Y3: info. Rule miss (finding 1).
- Benign (B1 "Fall risk screen negative", B2 "Impact of diabetes"): info. Correct. B3 "Injury prevention handout given" conflicts; a safe-direction over-fire (finding 2).

lib11 is unchanged: the commit touches only conflicts.py and the r3 variants test, and the lib11 case files have an empty diff since 93a2ffc. The conflict suites pass: 352 passed. The seven lib11-referencing test modules pass: 393 passed.

Method and state: HEAD was 93a2ffc when the checks ran, and is 20b3a42 now. `git diff --stat 93a2ffc HEAD` over conflicts.py, the r3 variants test and evals/library/ is empty, so the reviewed code is the current code. Probes ran on git archive copies, not the working tree.

```json
{"card": "T-141", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git 93a2ffc (T-141 round 4, section 7.4 fix-up): app/backend/conflicts.py and tests/unit/test_t141_r3_variants.py. Probes on a git archive of 93a2ffc (/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r4_head) with ad8b7d1 as the control archive (.../scratchpad/T141r4_prev). HEAD was 93a2ffc at check time and is 20b3a42 now; the T-141 files and evals/library/ are unchanged since 93a2ffc. Fixture backend only; no server started.",
 "exercised": [
  "Read personas/staff-engineer.md, reviews/T-141-staff-engineer-r3.md, .claude/agent-memory/staff-engineer-reviewer/project_t141_r3_patterns.md, `python3 tools/board.py show T-141` (round-4 brief and rule note at 14:24:15Z)",
  "`git rev-parse HEAD` = 93a2ffc8595e16d66257207a4a8c2c8a31c99b8f at check time; `git cat-file -t 93a2ffc` = commit; later `git rev-parse HEAD` = 20b3a42be9d2faadf451ff4f5b9375b1f9aa795e with `git diff --stat 93a2ffc HEAD -- app/backend/conflicts.py tests/unit/test_t141_r3_variants.py` empty",
  "`git show --stat 93a2ffc`: 2 files (app/backend/conflicts.py, tests/unit/test_t141_r3_variants.py); `git show 93a2ffc -- app/backend/conflicts.py` read in full",
  "`git archive HEAD` into .../scratchpad/T141r4_head and `git archive ad8b7d1` into .../scratchpad/T141r4_prev",
  ".venv/bin/python -I .../scratchpad/T141r3_scripts/r3_variants.py .../scratchpad/T141r4_head: all 33 variants, classified per the rule (32 match; Y3 'Rear-ended in October 2025' prints info where the rule requires conflict)",
  ".venv/bin/python -I .../scratchpad/T141r3_scripts/r3_variants.py .../scratchpad/T141r4_prev: control; differs from the new archive on exactly T1, T2, T5, T6, T7, T8, T10, H1, H6, H7 (now conflict) and N3 (now info)",
  "Direct probe on the new archive, record 2026-01-05, stated 2026-01-09: 'Rear-ended in October 2025.' -> info; 'Rear-ended in November 2025.' -> conflict; 'Rear-ended in 2025.' -> conflict",
  "grep of app/backend/conflicts.py for the month-year cut-off (line 61: `> 2`) and bare-year rule (line 64: `int(y) <= ry - 2`); grep of tests/unit/test_t141_r3_variants.py lines 152-153 (Y2 conflict, Y3 info pinned)",
  "pytest -I -p no:cacheprovider on the new archive: tests/unit/test_conflicts.py, test_conflict_candidates.py, test_t093_j3_controls_reachable.py, test_t141_checks_per_case.py, test_t141_r3_variants.py, test_t116_r4_all_dated_records.py, test_api_routes.py: 352 passed",
  "lib11: `git ls-files | grep -i lib11` (evals/library/case_lib11_priors_and_ledger.{txt,expected.json}); `git diff --stat ad8b7d1 HEAD` and `93a2ffc HEAD` over those files empty; pytest -I on the 7 tests/ modules that reference lib11: 393 passed",
  "Not run (outside the brief): mutation checks, the pipeline CLI, the full unit suite, the 27-packet differential"
 ],
 "verdict": "changes",
 "scores": {"determinism": 5, "honest_failure": 4, "tests_assert_behaviour": 3, "llm_code_boundary": 5, "controls_discipline": 4},
 "findings": [
  {"severity": "major",
   "title": "Y3 'Rear-ended in October 2025' in a 2026-01-05 record stays info-only; the round-4 rule requires a date conflict and the r3 acceptance test asked for Y3 to conflict",
   "evidence": "Repro: `.venv/bin/python -I <scratchpad>/T141r3_scripts/r3_variants.py <scratchpad>/T141r4_head` prints `info      exp=conflict_or_info | Y3 'rear-ended in October 2025' record 2026-01-05 (3 months)`. Cause: app/backend/conflicts.py:61 `if ((ry * 12 + rm) - (int(m.group(2)) * 12 + mo)) > 2: return True` (a month and year more than two months before the record counts as history). Test pin: tests/unit/test_t141_r3_variants.py:153 `(\"Y3 rear-ended in October 2025\", \"info\", \"ER visit. Rear-ended in October 2025.\")`. Same record with the month one later: tests/unit/test_t141_r3_variants.py:152 `(\"Y2 rear-ended in November 2025\", \"conflict\", ...)` and the probe prints conflict. Direct probe on the new archive, record 2026-01-05: 'Rear-ended in October 2025.' -> info; 'Rear-ended in November 2025.' -> conflict. The bare-year form was fixed at conflicts.py:64 (`int(y) <= ry - 2`), so 'Rear-ended in 2025.' (Y1) now conflicts; the month-year form was not aligned.",
   "why_it_matters": "The section 7.4 rule says info-only only for generic negated or explicitly prior history. 'Rear-ended in October 2025' names the mechanism with no negator and no prior label; it is hidden only by a date window, and a one-month change flips it. A rear-end described in an earlier record is a real discrepancy against a stated accident date of 2026-01-09, which is the lost-conflict class the GATE-M2 finding and r2/r3 majors were about. Severity is major, not blocker, on the same calibration as r3: the record count still appears as a note and the loss is the date-conflict flag, not an entry or a total. The r4 handoff says 'bare year history needs >=2 calendar years', but the month-year window was left at two months, so the r3 acceptance test ('Y1 and Y3 conflict') is only half met. The test file pins Y3 to the code's output, so the handoff's '33 reviewer variants pinned' is pinned to the worker's reading, not the reviewer's.",
   "fix": "Apply the bare-year rule to month-year dates too. In _clause_is_history (conflicts.py:61), delete the `> 2` month window and count a month-and-year as history only when its year is at least two calendar years before the record's year, or when the sub-clause carries a history marker (_CLAUSE_HISTORY or _HIST_WORD). Change tests/unit/test_t141_r3_variants.py:153 to expect conflict.",
   "acceptance_test": "On the r4 archive plus the fix: r3_variants.py prints conflict for Y1, Y2 and Y3; info for N1-N6, H11, B1 and the lib11 shape A (`Car accidents in 2019 and 2022`, `Passenger vehicle struck from behind`, `Date of injury: 2026-03-18`); tests/unit/test_t141_r3_variants.py:153 expects conflict; the seven conflict suites stay green (352 passed) and the 7 lib11-referencing modules stay green (393 passed)."},
  {"severity": "nit",
   "title": "'Injury prevention handout given.' raises a date conflict because 'injury' alone is a mechanism word",
   "evidence": "Repro: `.venv/bin/python -I <scratchpad>/T141r3_scripts/r3_variants.py <scratchpad>/T141r4_head` prints `conflict  exp=conflict_ok | B3 'Injury prevention handout given'`; the same output on the ad8b7d1 control. _EVENT (conflicts.py:18-25) matches `injur\\w*` with no mechanism context.",
   "why_it_matters": "Not a rule violation: the round-3 direction prefers a false positive to a hidden conflict. It is an over-fire, and a paralegal must dismiss it on an annual physical.",
   "fix": "Leave as is and list it as a known over-fire, or match 'injury' only when it is followed by or preceded by mechanism words (collision, MVA, fall, struck, from).",
   "acceptance_test": "Optional. If changed: 'Injury prevention handout given.' returns [] and 'Injury from rear-end collision' still conflicts in test_t141_r3_variants.py."}
 ],
 "whats_right": [
  "The ten negated or governed mechanisms (T1-T10) and the history-labelled mechanisms (H1-H10) now conflict; the control on ad8b7d1 misses seven of T1-T10 and H1, H6, H7, so the fix does what the handoff says.",
  "The scope held: the commit touches only conflicts.py and the r3 variants test; evals/library/ lib11 files are unchanged; the conflict suites (352) and the lib11-referencing modules (393) pass on a clean archive.",
  "The note text no longer asserts that no record names a collision or injury (app/backend/conflicts.py accident_date_note), which closes the false-note part of r3's major."
 ],
 "questions_for_chris": [
  "Non-negotiable 6 says engineering reviewers run Sonnet; this scoped check ran as claude-haiku-5-5 because the brief named that model. Is a Haiku run acceptable for this record, or should T-141 r4 be re-run as Sonnet?",
  "Under the section 7.4 rule, is a month and year more than two months before the record 'explicitly prior'? If yes, Y3 is a nit and the rule needs that sentence; if no, finding 1 stands.",
  "The rule lists 'rear-ended' and 'MVC without prior/previous' as mechanism words. I treated dated or Hx/remote-labelled history ('MVA in 2015', 'Hx: rear-end collision 2018', 'MVA remote past') as explicit prior and info-only. Confirm that reading."
 ]}
```
