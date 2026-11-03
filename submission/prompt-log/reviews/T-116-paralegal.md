# T-116 review: paralegal-reviewer (Maria Delgado persona)

Commit under review: c1b44be (HEAD, `git rev-parse --short HEAD` = c1b44be). Scope: app/backend/gaps.py, the T-116 unit tests, and the
gap figures of the 25 golden and library packets plus the sample case. I read the code and drove the gap flow through the backend
(fixture backend, FastAPI TestClient). I did not drive the running app on localhost:7860 and did not run the full unit suite.

## Verdict: fail (one blocker)

The lib09 requirement holds: confirming record 4 keeps the gap at 42 days with `gap_changes []`, and the why names the intake form.
The defect is in the classifier. Any treatment visit whose Source label contains a paperwork word is excluded from gap endpoints,
which invents a gap and states a false fact about the visit. The lib11 change on the card is the right answer, but the committed
truth file was not updated, and the change as posted fails the library validator.

## What I checked

1. **Lib09 after confirming record 4.** The API flow (`artifacts/review-evidence/T-116-paralegal-lib09-api.py`) gives Gap of 42 days,
   from 2026-03-03 to 2026-04-14, `gap_changes []`. The why reads "Intake form on March 5, 2026 is not a treatment visit, so it does not
   start or end a gap." Output: `artifacts/review-evidence/T-116-paralegal-lib09-api.out.txt`.
2. **Record-type detection, 10 spot-checks against the packet headers** (all 180 records were classified; 21 are labelled non-visit):
   - case_01 r8 "Dr. Orla Pennywhistle, phone note": non-visit, correct.
   - case_09 r2 "Hobbleton Family Clinic, billing statement": non-visit, correct.
   - lib09 r4 "Consultorio Médico Aguaclara, formulario de admisión (OCR)": intake form, correct.
   - lib09 r7 "estado de cuenta (billing statement)": billing statement, correct.
   - lib10 r4 "Saltmarrow General Hospital, UB-04 itemized bill": claim form, correct.
   - lib10 r6 "Quoinmere Mutual Health Plan, EOB": EOB, correct.
   - lib11 r6 "Fennimoor Spine Clinic, new patient intake form (OCR text)": intake form, correct under the card's rule (see finding 2).
   - lib12 r9 "Marlowe Assurance Group, correspondence, records review letter": records review, correct.
   - lib15 r9 "Pennyroyal Records Retrieval, 18.001 affidavit": affidavit, correct.
   - lib14 r8 "Tarnwick Fire-Rescue, ambulance invoice": billing statement, correct.
   - Treatment visits that stay endpoints, including bare "intake" (case_04 r6, lib07 r1), the EMS and ER runs, operative reports and the
     undated handwritten page (lib14 r5): all correct.
   - No treatment visit in the 25 packets is wrongly excluded. The one disagreement with a golden kind is lib11 r6, where the golden says
     encounter and the product says intake form.
3. **Adversarial labels for visits** (`artifacts/review-evidence/T-116-paralegal-label-sweep.py`): 15 of 19 plausible visit labels are
   excluded (examples: "Capital PT, initial evaluation (intake form completed same day)" → intake form; "Dr. Reyes, orthopedics,
   statement of MMI" → billing statement; "Dr. Nguyen, records review visit" → records review). The four that pass include
   "Dr. Lee, chiropractic, visit 3 (faxed)" and "Hill Country Pain Management, new patient".
4. **Reproduction of the invented gap** through the real ingest path (`artifacts/review-evidence/T-116-paralegal-repro-false-exclusion.py`).
   Visits on 2026-03-01 and 2026-04-10 with a visit on 2026-03-20 in between: control (plain label) → no flag. Label "initial evaluation
   (intake form completed same day)" → `Gap of 40 days ... Intake form on March 20, 2026 is not a treatment visit`.
5. **Gap figures, 25 packets** (`artifacts/review-evidence/T-116-paralegal-packet-sweep.py`): dates, day counts and flags match the
   expected files for all 25. Record lists match for 24; lib11 is the exception (finding 2).
6. **Lib11 change on the card**: product output on lib11 gives gap rows 2026-03-18→03-27 to_records [5], 2026-03-27→04-24 from_records [5],
   gap_excluded_records [4, 6, 9]. That is what the card says. The 28-day interval stays unflagged and the 35-day flag is unchanged.
7. **Validator**: `research/validate_library.py` on HEAD exits 0 (`artifacts/review-evidence/T-116-paralegal-validator-HEAD.out.txt`).
   With the card's three list changes applied to a scratch copy it exits 1 (`...lib11-validator-lists-only.out.txt`). With record 6's
   kind also changed to records_admin it fails again (`...lib11-validator-lists-and-kind6.out.txt`).
8. **Tests**: `.venv/bin/python -m pytest -q tests/unit -k gap` in the project tree → `176 passed, 2384 deselected in 4.53s`. Same count on
   a `git archive HEAD` copy → `176 passed, 2384 deselected in 4.50s`. Output saved at
   `artifacts/review-evidence/T-116-paralegal-pytest-gap.out.txt`. `tests/unit/test_t116_gap_endpoints.py` collects 66 tests (card says 49).
9. **Code read**: app/backend/gaps.py:16-52 (regex list, `non_visit_label`), flag_templates.py:76-78, conflicts.py:13,
   pipeline.py:258, app/llm/lexicon.yaml `non_encounter` (line 1280 onward), tests/unit/test_t116_gap_endpoints.py.

## Findings

**Blocker, F1: a treatment visit whose label contains a paperwork word is dropped from gap endpoints, which invents a gap.**
`gaps.py:16-32` tests unanchored regexes with `re.search` against the whole Source line, and the first match wins (`gaps.py:43-45`).
"statement", "billing", "letter", "records review" and "intake form" anywhere in the label are enough. The reproduction shows a 40-day
gap flagged between visits that the records show on 3/01, 3/20 and 4/10. The explanation then asserts that the visit "is not a
treatment visit". That is an invented gap and a false statement about a record, which the persona treats as a blocker. The 25 packets are
clean today; the defect is in the classifier, and the T-116 tests cover only labels with no paperwork word in a visit label.

**Major, F2: the lib11 truth file is stale at HEAD, and the posted change fails the golden checker as written.**
At HEAD, `evals/library/case_lib11_priors_and_ledger.expected.json` still says `gap_excluded_records: [4, 9]` (lines 251-254), and the
gap rows still list `[5, 6]` (lines 276 and 286). c1b44be did not touch evals. The product now returns [5], [5] and [4, 6, 9]. Applying the
card's three list changes fails `research/validate_library.py`: `gap_excluded_records [4, 6, 9] != non-encounter/ambiguous records [4, 9]`
and two "record lists wrong". To finish it, record 6 needs a fourth kind, but `evals/golden/check_golden.py:200` accepts only encounter,
billing_statement and phone_note, and `E6: encounter flag disagrees with record kind` also fails. The HEAD validator passes only because the
truth still calls the intake form an encounter. `test_golden_and_library_gap_figures_are_unchanged` (test_t116 lines 106-115) compares
dates, days and flags only, so nothing guards the record lists. Card AC1 is ticked done while the change it describes is pending.

**Minor, F3: two more consumers still treat intake forms as encounters.** `conflicts.py:13` builds the "earliest recorded treatment date"
baseline for the accident-date conflict, and `pipeline.py:258` sets the accident year, both from `kind == "encounter"`. The same record is
excluded from gap endpoints and counted as treatment elsewhere. The handoff calls this out of scope. I did not construct a case that changes
output. My checklist item 7 depends on this baseline, so it needs its own card. The two classification lists (the researcher-owned
`non_encounter` entry in lexicon.yaml and the new `_NON_VISIT` list in gaps.py) are also a drift risk; that is architecture, outside my lens.

**Minor, F4: the gap why names the type and date but not the record or the header text it was classified from.** The sentence in
`flag_templates.non_visit_sentence` (flag_templates.py:76-78) reads "Intake form on March 5, 2026 is not a treatment visit...". The lib09
output carries `record_no: 4` and the header "formulario de admisión (OCR)" only in `computed.excluded_records`. A paralegal cannot see the
basis for the classification in one action.

**Nit, F5: card evidence says 49 tests; the file collects 66.**

## What is right

1. Lib09 confirm keeps 42 days with `gap_changes []`, and the why names the intake form.
2. Gap dates, day counts and flags match the expected files for all 25 packets. The sample's 73-day flag stays, and the 28-day interval is not flagged.
3. Excluded records appear in a gap explanation only when they fall inside a flagged span, and the sentence comes from templates, not an LLM.

## Outside my lens

Classifier architecture (one list in lexicon.yaml, a second in gaps.py) and the code quality of the regex list are for staff-engineer. The
choice of golden kind vocabulary is for qa and researcher.

## Questions for Chris

- The golden schema has no kind for an intake form. Should it gain one (a `check_golden.py` change), or should intake forms be recorded as a
  documented non-encounter kind? I did not decide this.

```json
{"card": "T-116", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit c1b44be (HEAD); app/backend/gaps.py, tests/unit/test_t116_gap_endpoints.py, flag_templates.py; evals/golden and evals/library packets (25) and the sample case; fixture backend via TestClient on a git archive HEAD copy in the scratchpad; the running app at localhost:7860 was not driven",
 "exercised": [
  "read personas/paralegal.md, board show T-116, git show c1b44be (stat and gaps.py diff); git rev-parse --short HEAD = c1b44be",
  ".venv/bin/python -m pytest -q tests/unit -k gap in the project tree: 176 passed, 2384 deselected; same on the HEAD archive copy: 176 passed, 2384 deselected; test_t116 file collects 66",
  "ran the fixture pipeline over all 25 golden and library packets plus sample.txt (180 records); compared gap rows, record lists and excluded lists with the expected files",
  "classified all 180 records with gaps.non_visit_label; 21 labelled non-visit; spot-checked 10 against headers (see review body)",
  "adversarial label sweep (19 visit labels) and an A/B packet repro through ingest.ingest + gaps.gap_flags (artifacts/review-evidence/T-116-paralegal-repro-false-exclusion.py)",
  "driven lib09 confirm_date flow through the API on the HEAD archive (artifacts/review-evidence/T-116-paralegal-lib09-api.py)",
  "research/validate_library.py on HEAD (exit 0), and on scratch copies with the card's lib11 list change (exit 1) and with record 6 kind also changed (fails bad kind and E6)",
  "read gaps.py, flag_templates.py, conflicts.py:13, pipeline.py:258, lexicon.yaml non_encounter, check_golden.py:200, test_t116 and test_gaps"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 2, "gap_figures_unchanged": 5, "record_type_detection": 2, "lib11_truth_consistency": 2},
 "findings": [
  {"severity": "blocker",
   "title": "A treatment visit whose Source label contains a paperwork word is excluded from gap endpoints, which invents a gap and a false statement",
   "evidence": "artifacts/review-evidence/T-116-paralegal-repro-false-exclusion.out.txt: visits 2026-03-01 and 2026-04-10 with a middle visit labelled 'Capital PT, initial evaluation (intake form completed same day)' on 2026-03-20 -> 'Gap of 40 days ... Intake form on March 20, 2026 is not a treatment visit, so it does not start or end a gap.'; plain-label control -> no flag. 'Dr. Reyes, orthopedics, statement of MMI' -> billing statement, 40-day flag. app/backend/gaps.py:16-32 (unanchored re.search over the whole Source line) and gaps.py:43-45 (first match wins). artifacts/review-evidence/T-116-paralegal-label-sweep.out.txt: 15 of 19 visit labels excluded.",
   "why_it_matters": "Only treatment encounters may end a gap. Here a real visit is dropped, the tool reports a 40-day gap the records do not show, and it states that a visit is not a treatment visit. Persona section 5 and calibration: an invented fact or gap is a blocker. The 25 packets are unaffected today, but the T-116 tests cover no label in which a visit mentions a paperwork word.",
   "fix": "Classify on the record-type head of the Source label, not on any substring: an encounter term (visit, evaluation, new patient, daily note, follow-up, operative, run report, imaging, discharge summary) keeps the record an encounter; paperwork terms exclude only when they name the record type. Treat bare 'statement', 'letter', 'fax' and 'records review' with the same rule. Show the matched header text in the why (see F4).",
   "acceptance_test": "Add to tests/unit/test_t116_gap_endpoints.py: gap_flags over [2026-03-01 'Capital PT, visit 1', 2026-03-20 X, 2026-04-10 'Capital PT, visit 3'] returns no flag for X in {'Capital PT, initial evaluation (intake form completed same day)', 'Dr. Reyes, orthopedics, statement of MMI', 'Dr. Nguyen, records review visit', 'Dr. Lee, chiropractic, visit 3 (faxed)', 'Hill Country Pain Management, new patient'}; all existing non-visit label tests still pass. Re-run artifacts/review-evidence/T-116-paralegal-repro-false-exclusion.py: case A must show no flag."},
  {"severity": "major",
   "title": "lib11 expected truth file is stale at HEAD and the posted list change fails the golden checker as written",
   "evidence": "git show HEAD:evals/library/case_lib11_priors_and_ledger.expected.json: gap_excluded_records [4, 9] (lines 251-254); gap rows still list [5, 6] (lines 276, 286). Product: exact False, excl [4, 6, 9] (artifacts/review-evidence/T-116-paralegal-packet-sweep.out.txt). Card's list change on a scratch copy: research/validate_library.py -> 'gap_excluded_records [4, 6, 9] != non-encounter/ambiguous records [4, 9]' and two 'record lists wrong' (artifacts/review-evidence/T-116-paralegal-lib11-validator-lists-only.out.txt). With record 6 kind records_admin: 'record 6: bad kind' and 'E6: encounter flag disagrees' (artifacts/review-evidence/T-116-paralegal-lib11-validator-lists-and-kind6.out.txt); evals/golden/check_golden.py:200 accepts only encounter, billing_statement, phone_note. HEAD validator exit 0: artifacts/review-evidence/T-116-paralegal-validator-HEAD.out.txt. tests/unit/test_t116_gap_endpoints.py:106-115 compares dates, days and flags only.",
   "why_it_matters": "The card's list values are the correct answer under the rule (verified: the 3/27 intake form shares a date with visit 5, so visit 5 is the only endpoint; the 28-day interval stays unflagged). But the committed truth contradicts the committed product, the schema cannot express the change, and no test catches a record-list regression on library packets. AC1 is ticked done while this change is pending.",
   "fix": "qa and researcher: decide the kind vocabulary for intake forms (extend check_golden.py's allowed kinds and the entry encounter rule), set lib11 record 6 accordingly, apply the three list changes, and make the gap test compare (from_records, to_records) for all golden and library packets. Reopen AC1 until the truth file matches the product.",
   "acceptance_test": "The new record-list test fails on HEAD (lib11 lists differ) and passes after the fix. research/validate_library.py exits 0 with lib11 gap_excluded_records [4, 6, 9], gap row 2026-03-18->03-27 to_records [5], and row 2026-03-27->04-24 from_records [5]."},
  {"severity": "minor",
   "title": "Conflict and accident-year logic still treat intake forms and bills as encounters",
   "evidence": "app/backend/conflicts.py:13 (enc = kind == 'encounter' baseline for accident_date_conflicts); app/backend/pipeline.py:258 (_accident_year uses r['kind'] == 'encounter'). Card handoff: 'out of scope'. No packet output changed in my runs; not reproduced on a constructed case.",
   "why_it_matters": "The accident-date conflict (checklist item 7) compares stated dates with the earliest recorded treatment date. An intake form dated before the first visit would become that baseline while the gap rule excludes it.",
   "fix": "Open a follow-up card to route conflicts.py and pipeline._accident_year through the same non-visit classifier used by gaps.py, after the F1 fix.",
   "acceptance_test": "Constructed packet where an intake form is the earliest dated record: accident-date conflict and accident year use the first visit date."},
  {"severity": "minor",
   "title": "Gap why names the type and date, not the record number or the header text the classification came from",
   "evidence": "artifacts/review-evidence/T-116-paralegal-lib09-api.out.txt: why = '... Intake form on March 5, 2026 is not a treatment visit, so it does not start or end a gap.' The source 'Consultorio Médico Aguaclara, formulario de admisión (OCR)' and record_no 4 appear only in computed.excluded_records. app/backend/flag_templates.py:76-78.",
   "why_it_matters": "The paralegal must be able to reach the source in one action. A sentence that asserts a record type without the header text it rests on cannot be checked quickly, and a misclassified visit reads as settled fact.",
   "fix": "Add the record number and the verbatim header to the sentence from flag_templates.non_visit_sentence, e.g. 'Intake form on March 5, 2026 (record 4, header: formulario de admisión (OCR)) is not a treatment visit...'.",
   "acceptance_test": "test_lib09_confirming... asserts the why contains 'record 4' and the verbatim header text."},
  {"severity": "nit",
   "title": "Card evidence says 49 tests; test_t116_gap_endpoints.py collects 66",
   "evidence": "artifacts/review-evidence/T-116-paralegal-pytest-gap.out.txt; .venv/bin/python -m pytest --collect-only -q tests/unit/test_t116_gap_endpoints.py -> '66 tests collected in 0.24s'.",
   "why_it_matters": "A stale count in the evidence weakens the card record.",
   "fix": "Correct the count in the card evidence when the card is next updated.",
   "acceptance_test": "Card evidence matches collect-only output."}
 ],
 "whats_right": [
  "Lib09 confirm of record 4 keeps the gap at 42 days with gap_changes [], and the why names the intake form (API run on HEAD).",
  "Gap dates, day counts and flags match the expected files for all 25 golden and library packets; the sample's 73-day flag stays and the 28-day interval stays unflagged.",
  "Excluded records appear in a gap explanation only when they fall inside a flagged span, and the sentence is built from templates, not an LLM."
 ],
 "questions_for_chris": [
  "The golden schema has no kind for an intake form. Should it gain one (a check_golden.py change), or should intake forms be recorded as a documented non-encounter kind? I did not decide this."
 ]}
```
