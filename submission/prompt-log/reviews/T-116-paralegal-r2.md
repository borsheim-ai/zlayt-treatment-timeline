# T-116 round 2 review: paralegal-reviewer (Maria Delgado persona)

Commit under review: ea6ac71 (HEAD, "gap exclusion fails safe toward treatment ... (T-116 r2)"). Prior commit c1b44be (round 1).
Scope: app/backend/gaps.py, tests/unit/test_t116_gap_endpoints.py, and the gap output of the 25 golden and library packets plus the
sample case. I ran the code from a `git archive` copy of ea6ac71 (scratchpad `t116r2-head`) and of c1b44be (`t116r2-base`), not from the
dirty project tree. Each probe asserts that `gaps.__file__` sits inside the copy it is testing. I did not drive the running app on
localhost:7860, so the ship-bar `verify_quickly` score (D-015) is not scored in this round.

## Verdict: fail (two blockers, one major, one minor)

Round 2 fixed the four round-1 labels, and lib09 still holds at 42 days. But the exclusion still removes real treatment visits, and it
does so on a realistic label shape (a bare delivery word after the record type). The suite does not catch it because its helper gives every
test record an empty excerpt.

## Answers to the brief

1. **Blocker probe and 19-label sweep (round-1 labels, both excerpt variants).** All 19 are treatment now, with a plain excerpt and with a
   headed excerpt. The round-1 four (initial evaluation with intake form, statement of MMI, records review visit, fax copy of visit 3) now
   keep their endpoints. Output: `artifacts/review-evidence/T-116-paralegal-r2-labels.out.txt`, part A and part B.
2. **Eight new tricky labels.** Four pass, four are still excluded under a plain clinical excerpt (table below).
3. **Real treatment visits excluded?** In the 25 packets and the sample, no. Across 180 records the only golden-encounter records excluded
   are lib09 r4 and lib11 r6, both intake forms that the golden set marks as encounters (the round-1 kind disagreement, unchanged).
   In constructed cases, yes, four of eight new labels and all nine Appendix A visits once a bare `, fax` is appended (F1 below).
4. **lib09 still 42 days.** Yes. `gap_changes []`, 2026-03-03 to 2026-04-14. Output: `T-116-paralegal-r2-lib09-api.out.txt`.
5. **Gap dates across the 25 packets unchanged.** Yes. Gap dates, day counts and flags are identical to c1b44be (25/25) and to the expected
   files (no date, day or flag difference). The record-list difference on lib11 is the same as round 1 (finding F2).
   Output: `T-116-paralegal-r2-packets-compare.out.txt`.
6. **`.venv/bin/python -m pytest -q tests/unit -k gap`.** Project tree: `205 passed, 2384 deselected in 4.38s`. HEAD copy:
   `205 passed, 2384 deselected in 4.26s`. `tests/unit/test_t116_gap_endpoints.py` collects 95 tests, which matches the card.
   Outputs: `T-116-paralegal-r2-pytest-gap-tree.out.txt`, `T-116-paralegal-r2-pytest-gap-head.out.txt`.
7. **F3 and F4 and whether they need cards before the M3 gate.** F3 does need a card before the gate, and I rate it a blocker, not a
   follow-up (finding F3 explains why). F4 does not need its own card; fold it into the card that fixes F1, since both are edits in gaps.py.

## Eight new labels (line-by-line, from `T-116-paralegal-r2-labels.out.txt`)

| Label | Plain clinical excerpt | Expected | Result |
|---|---|---|---|
| Office visit / records request | treatment | treatment | pass |
| PT daily note (billing copy) | treatment | treatment | pass |
| Intake and evaluation | treatment | treatment | pass |
| Capital PT, daily note, fax | excluded (letter or correspondence) | treatment | **FAIL** |
| Capital PT, re-eval visit, statement | excluded (billing statement) | treatment | **FAIL** |
| Hill Country Pain Management, new patient, billing | excluded (billing statement) | treatment | **FAIL** |
| Capital PT, initial evaluation, correspondence | excluded (letter or correspondence) | treatment | **FAIL** |
| Dr. Lee, chiropractic, visit 3 - records request copy | treatment | treatment | pass |

Controls still excluded: "Capital PT, intake form" (intake form) and "Dr. Lee, chiropractic, billing statement" (billing statement).
With a headed excerpt ("Exam: ... Plan: ...") all eight are treatment.

## Findings

**Blocker F1 (round-1 blocker, narrowed and not closed): a visit label with a bare trailing admin word is still excluded from gap endpoints
when the excerpt has no heading. The gap is invented and the why states a false fact.**
Evidence:
- `artifacts/review-evidence/T-116-paralegal-r2-labels.out.txt` part B: the 3/20 visit "Capital PT, daily note, fax" with a clinical
  excerpt → `Gap of 40 days between March 1, 2026 (Capital PT, visit 1) and April 10, 2026 (Capital PT, visit 3). Letter or correspondence on
  March 20, 2026 is not a treatment visit, so it does not start or end a gap.` The same happens for the other three rows of the table.
- `artifacts/review-evidence/T-116-paralegal-r2-appendixA-fax-suffix.out.txt`: with `, fax` appended to the Source line and nothing else
  changed, all nine Appendix A treatment records are excluded as "letter or correspondence", including the EMS run report (record 1),
  the ER discharge summary (record 2), PT initial evaluation (record 4), PT visits 8 and 9 (records 5 and 6), and the MRI follow-up
  (record 9).
- `artifacts/review-evidence/T-116-paralegal-r2-sample-fax.out.txt`: sample.txt verbatim except that record 6's Source is
  "Capital PT, visit 9, fax". Control: `Gap of 73 days ... March 6, 2026 ... May 18, 2026`. Changed: record 6 excluded; the flag becomes
  `Gap of 87 days between February 20, 2026 (Capital PT, visit 8) and May 18, 2026 ... Letter or correspondence on March 6, 2026 is not
  a treatment visit`. The reference case's 73-day flag is replaced by a different, false one.
- Root cause, code: `app/backend/gaps.py:59-68` `_head` keeps only the text after the last comma, so a visit word earlier in the label is
  never read. `gaps.py:32` `^fax$` matches a bare delivery word as a record type. `gaps.py:48-53` `_EVIDENCE` does not count a pain score,
  a range-of-motion finding, or "Plan of care:" as treatment evidence (the Appendix A record 4 excerpt "Plan of care: 12 visits." is not
  matched). `gaps.py:92-99` `non_visit_label` then excludes.
- Why the suite passes: `tests/unit/test_t116_gap_endpoints.py:19` gives the helper `excerpt=""` by default. The paperwork-label test
  (lines 104-119) therefore runs every label with an empty excerpt, so no test has a visit with a bare trailing admin word and clinical text.

Why it matters: a real visit is dropped, the tool reports a gap the records do not show (40 days in the constructed case, and a changed
73-day flag on the Appendix A sample), and it states that a record is not a treatment visit. The card's own docstring says "When unsure,
it counts as treatment"; these labels are visits with a delivery word attached. Persona §5 and §8: an invented fact or gap is a blocker.

Fix: decide the record type from the whole Source label, not the last comma segment. (a) If a visit word (visit, evaluation, daily note,
new patient, follow-up, treatment, and the rest of `_VISIT_WORD`) appears anywhere in the label outside parentheses, keep the record as
treatment. (b) Bare delivery words (fax, faxed, copy, attached) never name a record type. (c) Treat clinical findings in the excerpt
(a pain score "N/10", a range-of-motion finding, "Plan of care:", "Dx:") as treatment evidence. Keep the round-2 rules for the 19 labels
and the controls.

Acceptance test: re-run `artifacts/review-evidence/T-116-paralegal-r2-labels.py`; the "must NOT be excluded" count under the plain
excerpt goes to 0 and both controls stay excluded. Re-run `T-116-paralegal-r2-appendixA-fax-suffix.py`: 0 of 9 excluded. Re-run
`T-116-paralegal-r2-sample-fax.py`: the 73-day flag is unchanged with the ", fax" label. Add to the unit tests: the eight new labels
with a plain clinical excerpt (not the empty one) produce no exclusion and no flag.

**Blocker F3 (raised from round-1 minor): the accident-date baseline counts an intake form as the first recorded treatment, and the tool
states that as fact. This is not a follow-up.**
Evidence:
- `artifacts/review-evidence/T-116-paralegal-r2-f3-conflict.out.txt`: constructed case, intake form dated 2026-01-12 whose own excerpt
  states "Date of accident: 2026-01-15", and a first visit on 2026-01-20. HEAD raises the conflict "Stated accident date January 15, 2026
  ... is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form)". With the intake form's stated date kept but
  the intake form out of the baseline, no conflict. Code: `app/backend/conflicts.py:13` (`kind == "encounter"` baseline) and
  `app/backend/pipeline.py:258` (`_accident_year`).
- Spec: D-017 ("first recorded treatment: <earliest record date>") and R-FL-2 ("first recorded treatment"). The tool states a date for a
  non-treatment record as the first treatment.
- `artifacts/review-evidence/T-116-paralegal-r2-f3-packets.out.txt`: over the 25 packets and sample, the baseline change alters no
  conflict or accident year. So the defect is reached only by a constructed case, not by the packets.

Why it matters: this is the same class as F1 (a non-treatment record counted as treatment, a false statement in the output), and it sits
on checklist item 7, the accident-date conflict the attorney must see. The round-2 card left it out of scope. Scope does not change the
severity under the persona calibration. I rate it a blocker because it states a false fact, and I note that its reach is constructed only.

Fix: route the baseline in `conflicts.py:13` and `pipeline.py:258` through the same `non_visit_label` the gap rule uses, for the baseline
only. Keep stated-date sources from every record (an intake form's own accident-date line still counts as a stated date).

Acceptance test: `T-116-paralegal-r2-f3-conflict.py` shows no conflict after the change. Unit test: an intake form dated before the first
visit, with a stated accident date between the two, raises no "later than first recorded treatment" conflict, and any "first recorded
treatment" wording cites the visit.

**Major F2 (carried from round 1, still open): the lib11 truth file is stale at ea6ac71, and card AC1 is ticked done.**
Evidence: `git show ea6ac71:evals/library/case_lib11_priors_and_ledger.expected.json` still has `gap_excluded_records: [4, 9]` (lines 251-254)
and gap rows `[5, 6]` (lines 276-290). The product returns excluded `[4, 6, 9]` and rows `[5]` and `[5]`
(`T-116-paralegal-r2-packets-compare.out.txt`, "record-list diff vs expected"). Both c1b44be and ea6ac71 leave evals/ unchanged. The
card's round-2 note asks qa to apply five edits; it has not been applied. `test_golden_and_library_gap_figures_are_unchanged` still compares
dates, days and flags only.
Why it matters: the committed truth contradicts the committed product, and no test catches a record-list regression on library packets.
Persona §8: a required item present but not reconciled is at least major, and this must be fixed before the M3 gate.
Fix: qa applies the record-list edits and settles the intake-form kind (see question 1). The gap test then compares
(from_records, to_records) for every golden and library packet. Reopen AC1 until the truth file matches the product.
Acceptance test: the new list test fails on ea6ac71 for lib11 and passes after the edit; `research/validate_library.py` and
`evals/golden/check_golden.py` exit 0 on the edited truth; `T-116-paralegal-r2-packets-compare.out.txt` shows record lists equal to the
expected files.

**Minor F4 (carried from round 1, unchanged): the gap why names the type and the date, not the record number or the header text.**
Evidence: `artifacts/review-evidence/T-116-paralegal-r2-lib09-api.out.txt`: `why: AI translation ... Intake form on March 5, 2026 is not a
treatment visit, so it does not start or end a gap.` Record 4 and the header "formulario de admisión (OCR)" appear only in
`excluded: [{'record_no': 4, ...}]`. `app/backend/flag_templates.py:76-78` is unchanged.
Why it matters: a paralegal must reach the source in one action (checklist 3), and a misclassified visit reads as settled fact.
Fix: add the record number and the verbatim header to the sentence, for example "Intake form on March 5, 2026 (record 4, header:
formulario de admisión (OCR)) is not a treatment visit...".
Acceptance test: the lib09 confirm test asserts the why contains "record 4" and the header text.
Card: fold into the F1 card (same function family); no separate card needed before the gate, but it must land before the gate.

## Probe method notes

- Round-1 probe scripts in `artifacts/review-evidence/` point at a scratchpad archive path that no longer exists (the card handoff noted
  this). I wrote new probes with `T-116-paralegal-r2-` prefixes instead of reusing them.
- Fixture-pipeline lines "llm call failed ..." are filtered from the saved outputs. They appear in the c1b44be run too.
- `case_lib01_er_only_then_gap` finishes `done_with_errors` at both c1b44be and ea6ac71. Not a T-116 change; noted only.
- Scripts take the tree path as an argument and run with `-I`, so the copies are isolated from the dirty project tree.
  The HEAD copy is at `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r2-head`.

## What is right

1. Lib09 confirm of record 4 keeps the gap at 42 days with `gap_changes []`, and the why names the intake form.
2. The round-1 label set and the intake and bill controls now classify correctly. Gap dates, day counts and flags are identical to c1b44be and
   to the expected files across all 25 packets.
3. Exclusion is template-built, not LLM-built. No packet visit is excluded (the two excluded encounters are intake forms).

## Outside my lens

Choice of the kind vocabulary and the intake-form kind is for qa and the researcher. Whether the conflict baseline should be the first visit
or the first record is the litigation lead's call under D-017; I flag only that the tool currently states a non-treatment date as "first
recorded treatment". Classifier architecture (two lists) is for staff-engineer.

## Questions for Chris

1. Intake forms have no golden kind. Round 2 used `phone_note` as a stand-in for lib11 record 6, which mislabels the record as a phone call.
   Should intake forms get a documented kind (a `check_golden.py` change), or stay a documented non-encounter stand-in? qa needs this to
   close F2.
2. F3 moves the accident-date baseline off intake forms and bills. I assumed that is what D-017's "first recorded treatment" means. Confirm?

```json
{"card": "T-116", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit ea6ac71 (HEAD, round 2) and c1b44be (round 1 base) via git archive copies in the scratchpad; app/backend/gaps.py, tests/unit/test_t116_gap_endpoints.py, conflicts.py:13, pipeline.py:258; 25 golden+library packets plus sample (180 records); lib09 API flow; the running app at localhost:7860 was not driven",
 "exercised": [
  "read personas/paralegal.md, reviews/T-116-paralegal.md, board show T-116, git log -5, git show ea6ac71 --stat and gaps.py diff",
  "git archive ea6ac71 -> scratchpad t116r2-head; git archive c1b44be -> scratchpad t116r2-base; every probe run with .venv/bin/python -I and asserts gaps.__file__ is inside the tree it tests",
  ".venv/bin/python -m pytest -q tests/unit -k gap: project tree 205 passed, 2384 deselected in 4.38s; HEAD copy 205 passed, 2384 deselected in 4.26s; test_t116 collect-only 95 tests",
  "T-116-paralegal-r2-labels.py: 19 round-1 labels and 8 new labels, plain and headed excerpts, label-only and as the 3/20 record of a three-visit packet through ingest.ingest + gap_flags; two controls",
  "T-116-paralegal-r2-appendixA-fax-suffix.py: each Appendix A treatment record with ', fax' appended to its Source line",
  "T-116-paralegal-r2-sample-fax.py: sample.txt with record 6 Source changed to 'Capital PT, visit 9, fax'; control and changed gap flags compared",
  "T-116-paralegal-r2-packets.py on HEAD and c1b44be; T-116-paralegal-r2-packets-compare.py: gap rows, flags, excluded lists against each other and the expected files; over-exclusion and recall counts",
  "T-116-paralegal-r2-lib09-api.py: lib09 ingest, then confirm_date on record 4 through the FastAPI TestClient on the HEAD copy",
  "T-116-paralegal-r2-f3-conflict.py (constructed intake-form baseline) and T-116-paralegal-r2-f3-packets.py (baseline-only counterfactual over 25 packets and sample)",
  "git show ea6ac71:evals/library/case_lib11_priors_and_ledger.expected.json lines 251-290 (gap_excluded_records, gap rows)",
  "read gaps.py (lines 16-99), conflicts.py:1-56, pipeline.py:257-258, flag_templates.py:76-78, test_t116_gap_endpoints.py:19 and 104-119, spec R-FL-2 and D-017"
 ],
 "verdict": "fail",
 "scores": {"no_real_visit_excluded": 2, "gap_figures_unchanged": 5, "lib09_gap_42_days": 5, "record_type_detection": 2, "lib11_truth_consistency": 2},
 "findings": [
  {"severity": "blocker",
   "title": "A visit label whose last comma segment is a bare admin word (fax, statement, correspondence) is excluded when the excerpt shows no heading, which invents a gap and states a false fact (round-1 F1, narrowed)",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r2-labels.out.txt part B: 'Capital PT, daily note, fax' with a plain clinical excerpt on 3/20 -> 'Gap of 40 days ... Letter or correspondence on March 20, 2026 is not a treatment visit'; also 'Capital PT, re-eval visit, statement', 'Hill Country Pain Management, new patient, billing', 'Capital PT, initial evaluation, correspondence'. artifacts/review-evidence/T-116-paralegal-r2-appendixA-fax-suffix.out.txt: 9 of 9 Appendix A treatment records excluded with ', fax' appended. artifacts/review-evidence/T-116-paralegal-r2-sample-fax.out.txt: sample record 6 'Capital PT, visit 9, fax' -> 73-day flag becomes 87 days (2026-02-20 -> 2026-05-18) with 'Letter or correspondence on March 6, 2026 is not a treatment visit'. app/backend/gaps.py:59-68 (_head keeps last comma segment), gaps.py:32 (^fax$), gaps.py:48-53 (_EVIDENCE misses pain scores, ROM, 'Plan of care:'), gaps.py:92-99. tests/unit/test_t116_gap_endpoints.py:19 (excerpt default \"\") and 104-119 (paperwork-label test runs with an empty excerpt).",
   "why_it_matters": "A real treatment visit is dropped from gap endpoints; the tool reports a gap the records do not show and states that a record is not a treatment visit. The Appendix A reference case's 73-day flag is replaced by a different false flag when a delivery word is appended. Persona section 5 and calibration: invented fact or gap = blocker. The docstring's fail-safe ('when unsure, it counts as treatment') is not honoured for these labels.",
   "fix": "Decide the record type from the whole Source label, not the last comma segment: (a) any visit word from _VISIT_WORD outside parentheses keeps the record as treatment; (b) bare delivery words (fax, faxed, copy, attached) never name a record type; (c) clinical findings in the excerpt (pain score N/10, range-of-motion finding, 'Plan of care:', 'Dx:') count as treatment evidence. Keep the round-2 rules for the 19 labels and the two controls.",
   "acceptance_test": "T-116-paralegal-r2-labels.py: 0 treatment visits excluded under the plain excerpt, both controls still excluded. T-116-paralegal-r2-appendixA-fax-suffix.py: 0 of 9 excluded. T-116-paralegal-r2-sample-fax.py: sample 73-day flag unchanged with the ', fax' label. Unit test: the 8 new labels with a plain clinical excerpt (not the empty default) produce no exclusion and no flag."},
  {"severity": "blocker",
   "title": "The accident-date conflict baseline counts an intake form as the first recorded treatment and states that as fact (round-1 F3, raised: not a follow-up)",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r2-f3-conflict.out.txt: intake form 2026-01-12 with excerpt 'Date of accident: 2026-01-15', first visit 2026-01-20 -> HEAD conflict 'Stated accident date January 15, 2026 ... is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form)'; counterfactual (intake form out of the baseline, its stated date kept) -> none. app/backend/conflicts.py:13 (kind == 'encounter' baseline), app/backend/pipeline.py:258 (_accident_year). Spec: D-017 ('first recorded treatment: <earliest record date>'), R-FL-2. artifacts/review-evidence/T-116-paralegal-r2-f3-packets.out.txt: no packet or sample output changes (reach is constructed only).",
   "why_it_matters": "The tool asserts a non-treatment record is the first treatment and raises a false accident-date conflict. It is the same class as F1 (a false statement about a record), and it sits on checklist item 7. Scope does not reduce severity under the persona calibration; no packet reaches it, which is the only mitigating fact.",
   "fix": "Route the baseline in conflicts.py:13 and pipeline.py:258 through the same non_visit_label the gap rule uses, for the baseline only. Keep stated-date sources from every record, including an intake form's own accident-date line.",
   "acceptance_test": "T-116-paralegal-r2-f3-conflict.py prints no later-than conflict after the change. Unit test: intake form dated before the first visit with a stated accident date between the two raises no 'later than first recorded treatment' conflict, and any 'first recorded treatment' wording cites the visit."},
  {"severity": "major",
   "title": "lib11 expected truth file is still stale at ea6ac71; card AC1 is ticked done while the list change is pending (round-1 F2, still open)",
   "evidence": "git show ea6ac71:evals/library/case_lib11_priors_and_ledger.expected.json: gap_excluded_records [4, 9] (lines 251-254); gap rows still [5, 6] (lines 276-290). Product (artifacts/review-evidence/T-116-paralegal-r2-packets-compare.out.txt): excluded [4, 6, 9]; rows [5] and [5]. test_t116 test_golden_and_library_gap_figures_are_unchanged compares dates, days and flags only.",
   "why_it_matters": "The committed truth contradicts the committed product and no test catches a record-list regression on library packets. Must be fixed before the M3 gate.",
   "fix": "qa applies the record-list edits once the intake-form kind is decided (question 1); extend the gap test to compare (from_records, to_records) for every golden and library packet; reopen AC1 until the truth matches the product.",
   "acceptance_test": "The new list test fails on ea6ac71 for lib11 and passes after the edit; research/validate_library.py and evals/golden/check_golden.py exit 0 on the edited truth; T-116-paralegal-r2-packets-compare.out.txt shows record lists equal to the expected files."},
  {"severity": "minor",
   "title": "Gap why names the type and date, not the record number or the header text it rests on (round-1 F4, unchanged)",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r2-lib09-api.out.txt: why = '... Intake form on March 5, 2026 is not a treatment visit, so it does not start or end a gap.'; record 4 and 'formulario de admisión (OCR)' appear only in excluded [{'record_no': 4, ...}]. app/backend/flag_templates.py:76-78 unchanged.",
   "why_it_matters": "A paralegal must reach the source in one action (checklist 3); a misclassified visit reads as settled fact.",
   "fix": "Add the record number and the verbatim header to the sentence, e.g. 'Intake form on March 5, 2026 (record 4, header: formulario de admisión (OCR)) is not a treatment visit...'. Fold into the F1 card; it must land before the M3 gate.",
   "acceptance_test": "The lib09 confirm test asserts the why contains 'record 4' and the verbatim header text."}
 ],
 "whats_right": [
  "Lib09 confirm of record 4 keeps the gap at 42 days with gap_changes [], and the why names the intake form (HEAD API run).",
  "The round-1 label set and the intake and bill controls classify correctly under both excerpt variants; gap dates, day counts and flags are identical to c1b44be and to the expected files across all 25 packets.",
  "Exclusion is template-built, not LLM-built; no packet visit is excluded (the two excluded golden encounters are intake forms, lib09 r4 and lib11 r6)."
 ],
 "questions_for_chris": [
  "Intake forms have no golden kind; round 2 used phone_note as a stand-in for lib11 record 6, which mislabels it as a phone call. Should intake forms get a documented kind (a check_golden.py change) or stay a documented non-encounter stand-in? qa needs this to close F2.",
  "F3 moves the accident-date baseline off intake forms and bills. I assumed D-017's 'first recorded treatment' means a treatment visit. Confirm?"
 ]}
```
