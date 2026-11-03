# T-207 staff-engineer review, r1

Reviewer: staff-engineer-reviewer (Marcus Lee persona). Fresh context, read-only on product code. Pinned to HEAD fc37fbc (archived to a scratch copy; the product tree was not edited).

Scope: docs/LLM_VS_CODE.md rows 2 and 3 (commits 901ad5a and fc37fbc), checked against app/backend/service_date.py, app/backend/store.py charge_service_date (lines 118-147) and app/backend/export.py charge_when (lines 215-226). Rules: memory/ORCHESTRATOR_DECISIONS.md D-071 and its amendment, clarification and addendum (lines 84-93). Spec: spec/REQUIREMENTS.md R-TL-3 (lines 50 and 356).

## Answers to the four questions

1. The date is code only, never the LLM. Holds. service_date.py imports only datetime, re and app.backend.amounts (lines 22-25). The charge path (store.py:118-147, export.py:215-226, present.py:152) calls no model. evals/letter_check.py has its own scanner and does not import service_date.
2. An allow-list of positive evidence decides it. Holds for the four listed ties, with gaps. The row's column-header list is narrower than the code (F6). Two other paths decide a printed date that row 2 does not name: a same-period locale rule (F1) and the header date of a visit note (F3).
3. The statement-date disambiguation rule applies. Holds. A date that reads two ways is blank when both readings fall on or before the statement (probe P1), and a single reading is printed when the other is after it (probe P2). Mutants M1 and M2 are killed.
4. A not-certain case gets the fillable blank plus a Step 3 note. The blank holds: it matches the D-071 addendum text (probe P7). The note holds except for counted undated charges (F4), and its wording for the no-label case differs from row 3 (F7).

Verdict: changes. No blocker. Five majors, three minors. I did not downgrade any finding for convenience.

Model note: the dossier and the brief expect claude-sonnet-5-5. The model I am running as is claude-haiku-5-5, and that is the id recorded below.

## Exercised

1. git show 901ad5a and git show fc37fbc: each changes only docs/LLM_VS_CODE.md (2 lines and 1 line). git rev-parse HEAD gives fc37fbcec0ebdb7705e4d91c2ad43afd67a82568. git diff --stat HEAD -- docs/LLM_VS_CODE.md is empty, so the working copy matches HEAD.
2. git archive HEAD into a scratch copy at the pinned sha (read and run only).
3. Read rows 2 and 3 at HEAD (docs/LLM_VS_CODE.md:30-31), the D-071 block (memory/ORCHESTRATOR_DECISIONS.md:84-93), spec R-TL-3 (spec/REQUIREMENTS.md:50, :356), and board.py show T-207 (reviews: []; commits 901ad5a, fc37fbc).
4. Read app/backend/service_date.py in full (377 lines) at HEAD. Grepped the dos_iso and dos_text writers, and the import lines of the date path.
5. pytest tests/unit -q on the HEAD archive: 6137 passed, 12 skipped (428 s).
6. pytest on the four T-202 date files (test_t202_r3_allow_list, test_t202_r2_service_date_layouts, test_t202_charge_service_dates, test_t200_undated_charge_label): 211 passed.
7. Probes P1 to P8 against the HEAD archive: artifacts/review-evidence/T-207-r1/probe_t207.py with probe_t207.out, and probe_t207_p8.py with probe_t207_p8.out.
8. Nine mutants on scratch copies: artifacts/review-evidence/T-207-r1/mutants_t207.py with mutants_t207.out. Baseline 211 passed. M1, M2, M3, M5, M7 and M9 killed; M4, M6 and M8 survived.
9. letter-check eval (evals/letter_check.py main, fixture backend): artifacts/review-evidence/T-207-r1/letter_eval_t207.py with letter_eval_t207.out. Output: value 0, cases 25, exit 0.
10. grep -rn -i mutant tests/unit evals --include=*.py: 28 hits, all comments from other cards. None is a harness for the date resolver's 24 mutants.

## Findings

F1 (major). Row 2 says a two-reading date is certain "only when" the statement rule decides it. The code also settles an end from the other end's order inside the same period. Probe P3, input "DOS 04/05/2026 - 13/05/2026 therapy $120.00." with statement 2026-06-30, prints "stated | 2026-05-04 | 2026-05-13". The row says that case is ambiguous and prints the blank. The code path is service_date.py:215-217 (if determined: order = next(iter(determined))). It is pinned by tests/unit/test_t202_r2_service_date_layouts.py:129 (mutant M3 is killed by it). D-071's amendment (memory/ORCHESTRATOR_DECISIONS.md:87) mentions "no locale rule from the record", so a locale rule is contemplated, but the table does not state it. Not a blocker: the rule is deterministic, tested, and uses the record's own other end.

F2 (major). Row 2 says a bill date "more than five years before it is not read". The code allows 1830 days (service_date.py:55 _YEARS_BEFORE = 5; :274 days=366 * _YEARS_BEFORE). Probe P4 with statement 2026-06-30: "P4 06/29/2021 | $120.00 | stated | 2021-06-29" (five years and one day before) and "P4 06/26/2021 | $120.00 | stated | 2021-06-26" (five years and four days before). The day 06/25/2021 is refused as implausible. Mutant M4 (calendar-exact bound 365*5+1) survives all 211 tests. The only bound tests are 1998 and 2031 (tests/unit/test_t202_r3_allow_list.py:187-188). Persona calibration: a missing boundary test is major.

F3 (major). A charge with no labeled service date takes the visit note's header date. Probe P5: "Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain." on a progress note dated 2026-01-09 prints "stated | 2026-01-09 | text='January 9, 2026'". Probe P8 shows the same default when the figure offset cannot be located (store.py:133-136 falls back to the header date for a non-bill record; a ledger prints the blank). The default is at service_date.py:375-376 and is pinned by test_t202_r3_allow_list.py:98 (mutant M7 killed). Row 2 says "Only a date tied to the line by" four listed ties counts, and row 3 says the header date is not the DOS "for a bill". Spec R-TL-3 (spec/REQUIREMENTS.md:50) says "Date of service is the record's header date, parsed by code", so the code follows the spec and the table is incomplete. Persona §5 would treat a silent default as a blocker. I do not rate it one because the spec authorizes the header date, no fact is invented, and nothing is hidden. The defect is that the table says otherwise. Chris must rule (Q1).

F4 (major). A counted undated charge gets no Step 3 note. Probe P6, counted via D-064 ("Count this charge"), prints "not_stated | reason=no_date | text='date of service [__________] (statement dated June 30, 2026)' | note=None". The uncounted line (P6-uncounted) gets a note. The suppression is store.py:139 (if not stated and not counted_undated:), and mutant M6 survives. Row 3 (docs/LLM_VS_CODE.md:31) says "Every charge line with no certain service date ... the Step 3 confirm note names the date as the quote writes it". The brief also requires a note for every not-certain case. The blank still prints in the letter, so nothing is invented or lost. Major, not blocker.

F5 (major). The row 3 Validation cell says "24 mutants of the resolver and the check all fail the unit suite" (docs/LLM_VS_CODE.md:31). Two resolver mutants survive the 211-test date suite: M4 (five-year bound, service_date.py:274) and M8 (the "Encounter date" heading, service_date.py:53). The count of 24 cannot be reproduced: no harness exists in the repo (item 10 above). The claim is refuted, so it is a finding.

F6 (minor). Row 2 lists "a DOS or service column header". The code's heading set (service_date.py:53-54) also accepts Visit Date, Date of Visit, Encounter Date, SVC and 24A. Encounter Date has no test (M8 survives). Fix: list the set in row 2 and test it.

F7 (minor). Row 3 says the note asks the paralegal to "read the date from the quote" and "names the date as the quote writes it". That holds for the written-date reasons (service_date.py:102). For the no-label reason the note says "Request a dated itemized bill, or fill the blank from the record" and names no date (service_date.py:103; probe P7b). Fix: align the row or the note.

F8 (minor). billing.py:141 (_dos, via dates.parse_date) and billing.py:339 emit a per-line dos_iso served at GET /api/cases/{token}/billing (billing.py:1062, registered at api.py:599). This is a second date-of-service derivation outside row 2's "only" claim. It does not reach the letter (dos_iso writers listed in item 4) and I found no frontend consumer. Fix: say in row 2 that it is not a charge date, or remove it.

## What is right

1. The date path makes no model call: service_date.py imports only datetime, re and amounts, and the letter-check scanner is independent of it.
2. The statement-date rule works as written: P1 prints the blank, P2 prints April 5, and mutants M1 and M2 are killed.
3. The blank matches the D-071 addendum text exactly ("date of service [__________] (statement dated June 30, 2026)", probe P7), and letter_check reports value 0 over 25 cases.

Outside my lens: the wording of Step 3 UI copy beyond the note strings, and the legal weight of the blank.

```json
{"card": "T-207", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "docs/LLM_VS_CODE.md rows 2-3 at HEAD fc37fbc (commits 901ad5a, fc37fbc); app/backend/service_date.py, app/backend/store.py:118-147, app/backend/export.py:215-226; memory/ORCHESTRATOR_DECISIONS.md D-071 lines 84-93; spec/REQUIREMENTS.md R-TL-3; no app URL exercised",
 "exercised": ["git show 901ad5a and fc37fbc (docs only); git rev-parse HEAD = fc37fbcec0eb; git diff --stat HEAD -- docs/LLM_VS_CODE.md empty",
               "git archive HEAD into scratch copy head-fc37fbc (pinned, read and run only)",
               "read rows 2-3 (docs/LLM_VS_CODE.md:30-31), D-071 block (ORCHESTRATOR_DECISIONS.md:84-93), spec R-TL-3 (REQUIREMENTS.md:50, 356), board.py show T-207",
               "read service_date.py in full (377 lines) at HEAD; store.py:118-147; export.py:215-226; grep dos_iso writers and date-path imports",
               "pytest tests/unit -q at HEAD archive: 6137 passed, 12 skipped",
               "pytest on 4 T-202 date files: 211 passed",
               "probes P1-P8: artifacts/review-evidence/T-207-r1/probe_t207.py (+.out), probe_t207_p8.py (+.out)",
               "9 mutants on scratch copies: artifacts/review-evidence/T-207-r1/mutants_t207.py (+.out); M4, M6, M8 survived; M1 M2 M3 M5 M7 M9 killed",
               "letter_check eval via letter_eval_t207.py (+.out): value 0, 25 cases, exit 0",
               "grep -rn -i mutant tests/unit evals: 28 comment hits, no 24-mutant harness"],
 "verdict": "changes",
 "scores": {"row2_matches_code": 3, "row3_matches_code": 3, "date_is_code_only": 5, "allow_list_decides": 3, "statement_date_rule": 4, "not_certain_blank_and_note": 3, "tests_and_validation_claims": 2},
 "findings": [
  {"severity": "major", "title": "Row 2 says a two-reading date is certain only by the statement rule; code also settles it from the other end of the same period",
   "evidence": "probe_t207.out line 'P3 | $120.00 | stated | 2026-05-04 | 2026-05-13' for 'DOS 04/05/2026 - 13/05/2026 therapy $120.00.' (statement 2026-06-30); app/backend/service_date.py:215-217 'if determined: order = next(iter(determined))'; docs/LLM_VS_CODE.md:30 'it is certain only when a reading after the bill's own (statement) date is impossible'; tests/unit/test_t202_r2_service_date_layouts.py:129 kills M3",
   "why_it_matters": "The table is the binding description of how a printed date is decided. It says the statement rule is the only resolver; the code and a tested test use a second rule. D-071's amendment contemplates a record-level locale rule, but the table does not state one.",
   "fix": "Architect amends row 2 to state the same-period locale rule (cite D-071 amendment 'no locale rule from the record'), or the code drops the rule and the period prints the blank.",
   "acceptance_test": "Row 2 names the rule the code applies; a test pins '04/05/2026 - 13/05/2026' to the decided answer; mutant M3 stays killed."},
  {"severity": "major", "title": "Five-year bound is 1830 days, not 'more than five years'; no test sits at the boundary",
   "evidence": "app/backend/service_date.py:55 '_YEARS_BEFORE = 5'; :274 'days=366 * _YEARS_BEFORE'; probe_t207.out 'P4 06/29/2021 | $120.00 | stated | 2021-06-29' (5y+1d before 2026-06-30) and 'P4 06/26/2021 | $120.00 | stated | 2021-06-26'; mutants_t207.out 'M4 ... SURVIVED | exit=0 | 211 passed'; tests only at 1998/2031 (tests/unit/test_t202_r3_allow_list.py:187-188); docs/LLM_VS_CODE.md:30 'more than five years before it is not read'",
   "why_it_matters": "A service date 5y+1d to 5y+4d before the statement is printed as a date of service though row 2 says it is not read. No test would catch it. Persona calibration: missing boundary test is major.",
   "fix": "Compare calendar years (statement date minus five years, same month and day, 29 Feb handled) instead of 366-day arithmetic; keep 1998 and 2031.",
   "acceptance_test": "Statement 2026-06-30: 06/29/2021 prints the blank with reason implausible; 06/30/2021 is stated; M4 is killed."},
  {"severity": "major", "title": "A charge with no labeled date takes the visit note's header date; row 2 says only the allow-list counts",
   "evidence": "probe_t207.out 'P5-store | $240.00 | stated | 2026-01-09 | None | None | text='January 9, 2026' | note=None' for 'Office visit, charge $240.00. Injury date 12/01/2025. Patient reports neck pain.'; probe_t207_p8.out 'P8 pos=None non-bill | state=stated | date_iso=2026-01-09' vs 'P8 pos=None ledger | state=not_stated'; app/backend/service_date.py:375-376 'if date_iso:' ... 'state=\"stated\", first=date_iso'; app/backend/store.py:133-136; tests/unit/test_t202_r3_allow_list.py:98 pins it; mutants_t207.out 'M7 ... KILLED'; docs/LLM_VS_CODE.md:30 'Only a date tied to the line by ... counts'; spec/REQUIREMENTS.md:50 'Date of service is the record's header date, parsed by code.'",
   "why_it_matters": "The code follows R-TL-3 for encounter records and nothing is invented, but the table says the allow-list decides and that the header date is not the DOS for a bill only. The table misstates a rule that decides a printed date. Under persona §5 an unannounced default would be a blocker; R-TL-3 authorizes it here, so I rate it major.",
   "fix": "Chris rules (Q1). If yes, row 2 names the encounter-header rule and cites R-TL-3. The pos-None branch at store.py:133 then either follows the same rule and says so, or prints the blank as the ledger path does.",
   "acceptance_test": "Row 2 states the rule; a test with pos=None on a visit-note charge matches the ruling; M7 stays killed."},
  {"severity": "major", "title": "A counted undated charge prints the blank with no Step 3 confirm note",
   "evidence": "probe_t207.out 'P6 | $250.00 | not_stated | None | reason=no_date | text='date of service [__________] (statement dated June 30, 2026)' | note=None' vs 'P6-uncounted ... note=' with a note; app/backend/store.py:129 (counted_undated) and :139 'if not stated and not counted_undated:'; mutants_t207.out 'M6 ... SURVIVED'; docs/LLM_VS_CODE.md:31 'Every charge line with no certain service date ... the Step 3 confirm note names the date as the quote writes it'; memory/ORCHESTRATOR_DECISIONS.md:72 D-064 'then sums like any accepted charge'",
   "why_it_matters": "Row 3 and the brief require a Step 3 note for every not-certain case. Once the paralegal counts the line, the prompt disappears; the blank still prints, so nothing is invented or lost. Major, not blocker.",
   "fix": "Either row 3 says counted lines carry no note and cites D-064, or store.py:139 keeps the note with 'Count this charge' wording.",
   "acceptance_test": "A test on a counted undated charge asserts the decided note behaviour; M6 is killed or the row is amended."},
  {"severity": "major", "title": "Validation cell claims 24 mutants all fail; two resolver mutants survive and no 24-mutant harness exists",
   "evidence": "docs/LLM_VS_CODE.md:31 '24 mutants of the resolver and the check all fail the unit suite'; mutants_t207.out 'M4 five-year bound ... SURVIVED' (service_date.py:274) and 'M8 Encounter date heading dropped ... SURVIVED' (service_date.py:53); grep -rn -i mutant tests/unit evals --include=*.py returns 28 comment hits from other cards",
   "why_it_matters": "A validation claim that the reviewer can refute is a finding. The cell is part of the checked artifact (row 3 'How it is checked').",
   "fix": "Amend the cell to the tests that exist, or commit the mutation harness with its count; add tests that kill M4 and M8.",
   "acceptance_test": "The cell names only committed tests; the harness, if committed, reports 24 of 24 killed; M4 and M8 are killed."},
  {"severity": "minor", "title": "Row 2's column-heading list is narrower than the code",
   "evidence": "docs/LLM_VS_CODE.md:30 'a DOS or service column header'; app/backend/service_date.py:53-54 _H_SVC also matches visit date, date of visit, encounter date, svc, 24A, from/to service; M8 survives",
   "why_it_matters": "A reader cannot tell which headings decide a printed date.",
   "fix": "List the heading set in row 2; add a test for Encounter Date.",
   "acceptance_test": "Row 2 lists the set; M8 is killed."},
  {"severity": "minor", "title": "Row 3's note wording holds only for written-date reasons",
   "evidence": "docs/LLM_VS_CODE.md:31 'asking the paralegal to read the date from the quote' and 'names the date as the quote writes it'; app/backend/service_date.py:102 (written-date note) vs :103 'Request a dated itemized bill, or fill the blank from the record'; probe_t207.out 'P7b ... note=The line states no date of service ...'",
   "why_it_matters": "The no-label note does not name a date and does not ask for the quote, so row 3 overstates the note.",
   "fix": "Align row 3 with the two note forms, or change the no-label note to point to the quote.",
   "acceptance_test": "The row and the note text agree; the existing confirm-note test still passes."},
  {"severity": "minor", "title": "A second date-of-service parser on billing lines sits outside row 2's only-path claim",
   "evidence": "app/backend/billing.py:141 'def _dos(raw): p = dates.parse_date(raw or \"\")'; billing.py:339 'dos_iso': _dos(dos); billing.py:1062 GET /api/cases/{token}/billing; api.py:599 billing.add_routes; no frontend consumer (grep app/frontend for /billing empty)",
   "why_it_matters": "Row 2 says a charge line's date of service is read only by service_date.py. This endpoint returns a DOS per bill line by a generic parser. It does not reach the letter, but it is a second source of the same fact.",
   "fix": "Document the endpoint's dos_iso as not a charge date in row 2, or remove it.",
   "acceptance_test": "Row 2 names the endpoint's status; grep for dos_iso writers shows no second charge-date path."}
 ],
 "whats_right": ["The date path makes no model call: service_date.py imports only datetime, re and amounts, and the letter-check scanner is independent of it.",
                 "The statement-date rule works as written: P1 prints the blank, P2 prints April 5, and mutants M1 and M2 are killed.",
                 "The blank matches the D-071 addendum text exactly (probe P7), and letter_check reports value 0 over 25 cases."],
 "questions_for_chris": ["Q1 (F3): Should a dated visit note's header date be the date of service for a charge with no labeled date? R-TL-3 says yes; row 2 says only the allow-list counts.",
                         "Q2 (F1): Is the same-period locale rule approved ('04/05/2026 - 13/05/2026' as May 4-13), or should that period print the blank as row 2 states?",
                         "Q3 (F4): Should a counted undated charge (D-064) show the Step 3 confirm note?"]}
```
