# T-141 staff-engineer review, round 3 (ad8b7d1), Marcus Lee persona

Verdict: **changes** (0 blockers, 1 major, 2 nits). The read-time notes, the no-summary rule and the mutant kills are all fixed and verified. The worker's deviation is the problem: "negated or plainly history stays info-only" is implemented as a bag-of-words window, and the window hides true date conflicts. 10 of my 33 fresh variants are real earlier-collision descriptions that come back info-only, and the note then says "No record names a collision, crash, accident, injury or similar in words of its own", which is false for each.

Method: all probes ran on `git archive ad8b7d1` copies in the scratchpad (T141r3_head, T141r3_mut for mutants), not the dirty working tree. HEAD moved to 25f585c during the review (frontend and T-139 commits); `git diff --stat ad8b7d1 HEAD` over conflicts.py, conflict_candidates.py, present.py and the T-141 test files is empty, so ad8b7d1 is the T-141 state.

## Answers to the brief

1. **Does the deviation hide a true date conflict? Yes.** Scripts: `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r3_scripts/r3_variants.py` (33 fresh variants). Each case is one record dated 2026-01-05, a PT visit 2026-01-12 and an intake "Date of accident per intake form: 2026-01-09".
   - Correct as the worker intended: `No prior accidents.`, `Denies MVC.`, `MVA in 2015, resolved.`, `History of MVA 2015.`, `Hx rear-end collision 2018.`, `MVA remote past`, `Fall risk screen negative.` all info-only. lib11 still has no date conflict.
   - Hidden true conflicts (info-only, should conflict): T1 `No LOC after the accident.`; T2 `Has not worked since the accident.`; T5 `No improvement since the crash.`; T6 `No airbag deployment in the collision.`; T7 `Without fracture after the MVC.`; T8 `Never lost consciousness during the crash.`; T10 `Negative for fracture after rear-end collision.`; H1 `History: rear-ended at a stoplight.`; H6 `Old man hit by a car crossing the street.`; H7 `Neck pain started years ago and worsened after the rear-end collision.` Cause: conflicts.py `_is_event_word` negates any event word with a negator in the five words before it, whatever sits between ("after", "since", "during", "in"); `_HIST_WORD` ("history", "old", "past") within three words counts as history even as a section label ("History:"); `_CLAUSE_HISTORY` makes the whole clause history when "years ago" appears anywhere in it.
   - Still conflict, correctly: T3, T4, T9, H2-H5, H8-H10, Y2, and all reviewer r2 variants V1-V3, V5-V8, V11, V16-V19, W3-W5, W9 (r2 variants rerun: 1 mismatch, V4, which is the intake-form self-contradiction I called right in round 2). Round-1 A-L: unchanged, B-H conflict, A, J, K, L quiet, I conflicts.
   - Safe-direction false positives (conflict where info is better): `Denies any motor vehicle collision or injury.` (the word "injury" is six words from "denies") and `Impact of diabetes on diet counselled.` The brief prefers these to hidden conflicts, so nit only.
2. **Notes at read time, refresh after confirm_date: fixed.** `r2_stale_checks.py` on the archive: ingested shows the predates note and no flag; after `review.confirm_date(.., '2026-03-06')` notes `[]` and flag `accident_date_after_treatment`. The note and the NO_DATED_RECORD count are computed in `checks(..., records)` from `store.load_records` (present.py case_view).
3. **No stored summary: fixed.** `r2_checks_matrix.py`: S5 (legacy ready) and S5b (legacy failed) report `ran=[]`, all four types skipped NOT_RUN, notes `[]`. A failed legacy case says NOT_RUN rather than RUN_FAILED; the reason text is honest about it.
   Other matrix rows are unchanged from round 2: ingested only, deadline at each stage, re-run in flight, lib09 partial Spanish (records 2, 4, 7), all-Spanish, crashed re-run RUN_FAILED (`r2_real_crash.py`).
4. **Mutants.** `r3_mutate.py` (32 mutants over conflicts.py, conflict_candidates.py, present.py, pipeline.py, with the r2 survivors): 31 of 31 applied mutants killed, 0 survived, plus the present.py "no records passed" mutant applied by hand (3 failed). The r2 survivors N6/N18 (old full date), P2 (run-start pending), P3, C7 (uncertain) and the word members t-bone, sideswipe, run over, airbag, seatbelt and 'vehicle'/'hit' replacements are all red now. Archive restored and diffed against the head copy (source files identical).
5. **Suites.** `tests/unit/test_conflicts.py test_conflict_candidates.py test_t093_j3_controls_reachable.py test_t141_checks_per_case.py test_t141_r3_variants.py test_t116_r4_all_dated_records.py test_api_routes.py` on the ad8b7d1 archive: 291 passed. 27-packet differential (`diff_packets.py`) between 68b8685 and ad8b7d1: identical, 27 accident-date result sets, sample still raises accident_date_after_treatment (2026-01-19). lib11 case view after a fixture run: two denial conflicts, no accident-date flag, note present.

```json
{
 "card": "T-141",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git ad8b7d1 (T-141 round 3, final) vs 68b8685; probes on git archives of ad8b7d1 and 68b8685 in the scratchpad (T141r3_head, T141r3_mut, T141r3_r2), never the dirty working tree; HEAD moved to 25f585c mid-review with no change to the T-141 files; fixture backend, no server started",
 "exercised": [
  "Read personas/staff-engineer.md, reviews/T-141-staff-engineer-r2.md, `python3 tools/board.py show T-141` (round-3 note, handoff), `git show ad8b7d1` for conflicts.py, conflict_candidates.py, present.py; `git rev-parse HEAD` = ad8b7d1 at start, 25f585c at end; `git diff --stat ad8b7d1 HEAD` over the T-141 files empty",
  "git archive ad8b7d1 into T141r3_head and T141r3_mut; git archive 68b8685 into T141r3_r2",
  "Reviewer r2 variants V1-V20 (r2_variants.py) and W1-W10 (r2_variants2.py) and round-1 A-L (probe2.py) on the r3 archive",
  "33 fresh variants (scratchpad T141r3_scripts/r3_variants.py): negations (No prior accidents, Denies MVC, Denies any motor vehicle collision or injury), historical (MVA in 2015, History of MVA 2015, Hx rear-end collision 2018), negator-before-true-collision (T1-T10), history-word-before-true-collision (H1-H11), bare year and month-year (Y1-Y3), benign (B1-B3); r3_note.py for the note text on a hidden case",
  "Read-time notes: r2_stale_checks.py (ingest then review.confirm_date); checks matrix r2_checks_matrix.py (ingested, complete, deadline at each stage, re-run in flight, legacy rows with no run_checks, lib09, lib11, all-Spanish, defaults); r2_real_crash.py (crash in the conflict stage of a re-run)",
  "27-packet differential diff_packets.py 68b8685 vs ad8b7d1 (identical, sample accident-date conflict kept); r2_lib11.py case view after a fixture run",
  "Mutation: r3_mutate.py, 31 mutants on T141r3_mut (all killed), plus a manual present.py mutant (records not passed, 3 tests failed); archive diffed against T141r3_head after (source identical)",
  "pytest on the ad8b7d1 archive: 7 conflict and checks modules, 291 passed"
 ],
 "verdict": "changes",
 "scores": {
  "determinism": 5,
  "honest_failure": 4,
  "tests_assert_behaviour": 3,
  "llm_code_boundary": 5,
  "controls_discipline": 4
 },
 "findings": [
  {
   "severity": "major",
   "title": "Negated-or-history exemption hides true accident-date conflicts: 10 of 33 fresh variants where an earlier record describes the collision come back info-only, and the note says no record names a collision or injury",
   "evidence": "app/backend/conflicts.py `_is_event_word` (negator anywhere in the 5 words before the event word negates it, so prepositions between them do not stop it; `_HIST_WORD` includes 'history', 'old', 'past' within 3 words before, so a 'History:' label counts), `_CLAUSE_HISTORY` ('years ago' anywhere in the clause makes the whole clause history), `_describes_event` (all event words must fail). Repro on a git archive of ad8b7d1: `.venv/bin/python -I <scratchpad>/T141r3_scripts/r3_variants.py <archive>`; info-only but a real collision: T1 'No LOC after the accident.'; T2 'Has not worked since the accident.'; T5 'No improvement since the crash.'; T6 'No airbag deployment in the collision.'; T7 'Without fracture after the MVC.'; T8 'Never lost consciousness during the crash.'; T10 'Negative for fracture after rear-end collision.'; H1 'History: rear-ended at a stoplight.'; H6 'Old man hit by a car crossing the street.'; H7 'Neck pain started years ago and worsened after the rear-end collision.' (each as the only mention in a record dated 2026-01-05 with the stated accident date 2026-01-09; `accident_date_conflicts` returns [] and `accident_date_note` text reads: '1 record predates the stated accident date, January 9, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care.', r3_note.py). Correctly still conflict: T3, T4, T9, H2-H5, H8-H10, Y2. 'No LOC after the accident' and 'has not worked since the accident' are among the commonest ER and follow-up phrasings, so this is not contrived.",
   "why_it_matters": "This is the same lost-conflict class as round-1 major 1 and round-2 major 1 (a deterministic R-FL-2 check becomes a word guess and a true discrepancy between the stated accident date and an earlier record disappears), now moved from 'wording the list misses' to 'wording the exemption over-reaches on'. The worker's reading of the Round 3 note (keep history and negation info-only so lib11 stays closed) is defensible, but the implementation negates the whole event instead of the noun the negator governs, and the note text then asserts the opposite of what the record says. Not a blocker for the same reason as rounds 1 and 2: it needs a stated accident date later than the earliest record plus one of these wordings, the record count is still surfaced as a note, and the loss is limited to the date-conflict flag, not an entry or a total.",
   "fix": "Scope the exemptions to the phrase they govern. (a) Negation: a negator only negates an event word when nothing but determiners, adjectives and event-noun modifiers sit between them ('no prior accidents', 'denies any motor vehicle collision', 'no recent injuries'); any of after, since, during, in, following, from, at, with, when, while, because, of between the two ends the scope. (b) History: 'history', 'hx', 'prior', 'previous', 'remote', 'old' count only immediately before the event noun or 'of <event>' ('prior accident', 'history of MVA', 'old MVC'), never when the word ends a label ('History:', 'History of present illness') or is followed by 'to'. (c) 'years ago', 'last year', 'as a child' make history only the sub-clause they sit in, split on 'and', 'but', 'worse', 'worsened', 'since', 'after'. (d) Reword the note so it says what was looked for and does not assert absence of injury: 'Records predate the stated accident date; none was read as describing a collision, so no date conflict is raised. Read them.'",
   "acceptance_test": "tests/unit/test_t141_r3_variants.py: T1, T2, T5, T6, T7, T8, T10, H1, H6, H7 each return one accident_date_after_treatment conflict; the info-only set (No prior accidents, Denies MVC, Denies any motor vehicle collision or injury, MVA in 2015, History of MVA 2015, Hx rear-end collision 2018, Fall risk screen negative) and the lib11 shape still return []; mutants that widen the negator window back to 5 words regardless of prepositions are killed."
  },
  {
   "severity": "nit",
   "title": "Two safe-direction false positives: 'Denies any motor vehicle collision or injury' and 'Impact of diabetes on diet' still raise a date conflict",
   "evidence": "r3_variants.py N3 (conflict; 'injury' sits six words after 'denies', outside the 5-word window) and B2 (conflict; bare 'impact\\w*' in conflicts.py `_EVENT`). The paralegal can dismiss the conflict; nothing is lost.",
   "why_it_matters": "The Round 3 direction prefers a false positive to a hidden conflict, so this is not a defect. It does show the negation window is by word count, which is the cause of the major finding in the other direction.",
   "fix": "Fixing the major finding's negation scope (adjective list, not a word count) also closes N3; restrict 'impact' to 'impact with/of the collision' or 'on impact'.",
   "acceptance_test": "N3 returns [] and B2 returns [] in test_t141_r3_variants.py after the scope change."
  },
  {
   "severity": "nit",
   "title": "A bare year earlier than the record's own year always counts as history, so 'Rear-ended in 2025' in a record dated mid-2026 is info-only",
   "evidence": "conflicts.py `_clause_is_history` last line `int(y) < ry - (0 if rm > 2 else 1)`; r3_variants.py Y1 (record 2026-06-05 'Intake. Rear-ended in 2025.', stated 2026-06-09): info-only. Y3 'Rear-ended in October 2025' in a 2026-01-05 record is also info-only (three months, outside the two-month month-year window). Both are ambiguous rather than clearly wrong; lib11's '2019 and 2022' needs the rule.",
   "why_it_matters": "A bare year says nothing about whether the event is the index accident; within the last ~15 months it could be. Low likelihood, and the brief set the threshold as 'plainly history'.",
   "fix": "Treat a bare year as history only when it is at least two calendar years before the record's year, or when the clause also has a history marker.",
   "acceptance_test": "Y1 and Y3 conflict; lib11 (2019, 2022) and 'MVA in 2015' stay info-only."
  }
 ],
 "whats_right": [
  "Notes and the dated-record count are computed from the current records at GET time; confirm_date now moves the flag and the note together, and the stored run summary keeps only language, read count and stage.",
  "A case with no stored summary reports all four checks as NOT_RUN with an honest reason and conflict_types [], and the matrix (deadline at each stage, crashed re-run, partial and all-Spanish) still never claims a check that did not run.",
  "Mutant discipline: 31 of 31 mutants killed including every round-2 survivor (old full date, run-start pending, uncertain language, individual word-list members), and the 27-packet differential is identical to 68b8685 with the sample conflict kept."
 ],
 "questions_for_chris": []
}
```
