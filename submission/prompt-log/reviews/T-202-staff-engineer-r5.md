# T-202 round 5 (D-073) - staff-engineer-reviewer

Verdict: **fail** (1 blocker, 1 major, 4 minor, 2 nit). Scope: commits 43b364d and f9c0faf, read from `git archive f9c0faf` copies under `artifacts/review-evidence/T-202-staff-r5/` (HEAD has since moved to 6b0724a, a docs commit; not reviewed).

The rewrite does what D-073 says for every sentence shape. Every probe from r2, r3, r4b and T-207 r2 that used a prose label ("DOS 03/01/2026", "visit of", "Treatment dates A to B", "next visit date", dotted leaders) now prints the fillable blank, and `service_date.py` has no prose label code left (grep: the only text patterns are `_H_SVC` for column headings and `_UB_SPAN` for the UB-04 statement period). The tests were rebased without weakening. The two sources are not enforced as written, though: the "column heading" test is a bare keyword search over any nearby line, so a key-value line such as `Date of service: 05/01/2026   Provider: Dr. Ames` turns the next row's first date into the date of service. That prints a posted date, a referral date or a next-visit date as the date of service on a classified charge, and `letter_check` has the same detector, so it accepts the wrong date and flags the correct blank. This shape has been in the code since r3 and every earlier probe (mine included) used real header rows.

## What I ran (all from the f9c0faf archive)
- Unit: `cd .../T-202-staff-r5/a && .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider` -> `6668 passed, 6 skipped in 447.30s (0:07:27)`, 0 failed (handoff: 6662 passed + 12 skipped = 6674; mine 6668 + 6 = 6674).
- Guided e2e: `cd .../e && pytest tests/e2e/guided -q` -> `156 passed in 196.08s (0:03:16)`.
- `python -m evals.letter_check` -> `{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", ...}`.
- `LLM_BACKEND=fixture python -m app.pipeline evals/golden/sample.txt` twice: byte-identical (`cmp` clean); the 73-day gap is flagged, the ER $6,240 and MRI $2,150 are charges.
- 84-line charge-header dump (`s/dump.py`) twice: identical; 54 of 84 lines print the blank, 30 print a date.
- All 28 r2/r3/r4b/T-207 probe scripts (`run_all.py`, outputs in `o/*.new` against f9c0faf and `o/*.old` against 8cb5bd2). Compared with the 8cb5bd2 run, the only new BAD lines are probes whose expected value was a prose-read date (p4: 2 lines, p4r4: 3 lines); each now prints the blank, which is the D-073 intent. The other BAD lines in p4 are r3-era harness lines that print the blank without the statement-date suffix and are flagged by the exact-form check at 8cb5bd2 too.
- Mutants: my 37 new ones (`mut5.py`: 35 killed, 2 survived) and the 53 r3/r4b/T-207 ones (`mutport.py`: 24 not applicable because the prose code is deleted, 22 killed, 7 survived).
- Own probes for the two-source rule (`r5probe.py`, `r5cls*.py`, `r5ship.py`, `r5chk.py`, `r5ub*.py`, `pdup.py`), differential production-vs-check run (`r5_pa_diff.py`), corpus label audit (`kinds_corpus.py`), and a diff read of the qa-owned test edits.

## Brief questions
1. Only two sources can lend a date: **no** for source (1), see F1. Sentences cannot lend a date (all prose-label probes blank). One more place still reads prose: the duplicate-promotion flag message (F5).
2. r3, r4b and T-207 r2 probes and mutants: re-run; results above and in F2.
3. `letter_check` applies the two-source rule independently: it is a separate scanner (no import of `service_date`, own matcher over the shared JSON), and it agrees with production on 177 records (`kinds.py`), on 69 of 70 layout probes (`r5_pa_diff.py`; the one disagreement is check-stricter, F7), and it catches a wrong record date. But it shares the F1 heading blind spot, so it cannot guard it.
4. qa-owned test edits (test_t205, test_t206, test_t200, test_t202 x4): sentence rows flipped to blank and each got a DOS-table twin; no test removed, none skipped. One assertion was dropped (F8).
5. Counts above.

```json
{"card": "T-202", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commits 43b364d and f9c0faf (D-073) read from git archive f9c0faf under artifacts/review-evidence/T-202-staff-r5/{a,e,m,m2,m3,p}; fixture backend; sample case plus 25 letter_check cases; no live app",
 "exercised": [
  "pytest tests/unit -q from a/: 6668 passed, 6 skipped in 447.30s (unit.out)",
  "pytest tests/e2e/guided -q from e/: 156 passed in 196.08s (e2e.out)",
  "python -m evals.letter_check from m/: {\"value\": 0, \"cases\": 25} (letter_check.out)",
  "python -m app.pipeline evals/golden/sample.txt twice with LLM_BACKEND=fixture: cmp identical (o/cli1.txt, o/cli2.txt)",
  "s/dump.py twice (84 charge-header lines, 54 blanks): identical (o/d1.txt, o/d2.txt)",
  "run_all.py: 28 earlier probe scripts (r2, r3, r4b, T-207 r2) against f9c0faf and 8cb5bd2 (o/*.new, o/*.old)",
  "mut5.py: 37 new mutants of service_date, store, amounts, encounter_types.json; 35 killed, S18 and S21 survived (mut5.out)",
  "mutport.py: 53 r3/r4b mutants ported; 24 not applicable (prose code deleted), 22 killed, 7 survived: M12, L5, L6, L9, N8, N15 and L6 again in mut4 (mutport_run.out)",
  "s/r5probe.py, r5cls.py, r5cls2.py, r5cls3.py, r5ship.py, r5chk.py, r5ub.py, r5ub2.py, r5sev.py, pdup.py, r5tab.py, r5_pa_diff.py, kinds_corpus.py, kinds.py",
  "git diff ad0d91a f9c0faf on tests/, store.py, amounts.py; grep of service_date.py and amounts.py for remaining prose readers",
  "test_t205 case_09 with the dropped line-sub assertion restored in the e/ copy: passes"],
 "verdict": "fail",
 "scores": {"two_source_rule_enforced": 2, "no_prose_path": 3, "llm_vs_code_boundary": 5, "determinism_and_reproducibility": 5, "letter_check_independence": 3, "tests_fail_when_code_breaks": 3, "test_rebase_integrity": 4, "honest_failure_states": 4},
 "findings": [
  {"severity": "blocker",
   "title": "A key-value or prose line that names the date of service is read as the column heading, so a posted, referral or next-visit date prints as the date of service; letter_check shares the blind spot",
   "evidence": "service_date.py:256-290 (_header_cells takes the nearest line above with >= 2 cells that has no digit OR names service; _column_head falls back to the nearest start column; line 367 then reads the row's date). Shipped letter via tests' own head() helper (s/r5ship.py, o/r5ship.new): ledger 'Itemized ledger / Date of service: 05/01/2026   Provider: Dr. Ames / Date posted 05/11/2026   97110 therapeutic exercise   $180.00' prints 'Brindlewood Physical Therapy, itemized ledger, May 11, 2026: $180.00'; the same with 'Visit date: 05/01/2026   Provider: Dr. Ames' over 'Next visit 05/29/2026 ... charge $180.00' prints 'May 29, 2026'; 'Charges for DOS shown below  (page 1)' (a sentence) over 'Referral 05/11/2026  97110 therapeutic exercise  $180.00' prints 'May 11, 2026'. All three are classified charge (o/r5cls2.new, o/r5cls3.new). Control: a real 'Posted / Service / Charge' header prints the blank. letter_check does not catch it: s/r5chk.py -> charge_date_violations returns [] for the posted date printed as DOS and flags the correct blank ('the quote's date-of-service cell holds one certain date and the line prints a blank'); evals/letter_check.py:381-407 _heading_over is the same logic. Present at 8cb5bd2 too (o/r5cls3.old identical), so it predates r5, but D-073 says prose is not read and a date comes only from 'the date cell of its own row in a bill table whose column header names the date of service'.",
   "why_it_matters": "This is the failure class the paralegal blocked in r2 and r3 (referral, posted and next-visit dates printing as the date of service) re-entering through the one source D-073 keeps. A wrong date of service goes into a demand letter as a fact, with the real DOS (May 1) sitting in the header line that the code mistook for a column title. The independent check cannot warn because it copies the detector. This violates the D-073 two-source constraint, so it is a blocker by the D.2 definition, not a style preference.",
   "fix": "Accept a heading only if it is a header row: every cell of the heading line is a short label (no sentence, no colon-then-value, no date or digit except a 24A cell), and the heading matches the row's cell count (drop the nearest-start fallback; unequal counts give the blank). Match the service cell with a full-cell vocabulary (DOS, date of service, service date, visit date, svc, from/to service, 24A, optionally followed by '(s)'), not a keyword search inside any text. Make letter_check use the same header-row definition in its own code. Add the three shapes above as fixtures in production and in the check.",
   "acceptance_test": "tests/unit: head() for the three shapes returns 'date of service [__________] (statement dated ...)'; charge_date_violations flags a letter that prints May 11 / May 29 for them and passes the blank; the real-header controls (DOS table, 24A From/To, tab, pipe and space-aligned tables) still print their dates. Mutant: replace the full-cell match with a keyword search or restore the nearest-start fallback; the suite must fail."},
  {"severity": "major",
   "title": "Two 'several dates, so the blank' rules have no test: M12 and S18 survive the whole date suite and each prints a date when mutated",
   "evidence": "mutport_run.out: 'mut.py M12_several_dates_first | unit survived (745 passed in 21.52s) | letter_check rc=0'; mut5.out: 'S18 stated reason: UB span any not all | SURVIVED | 736 passed in 10.35s'. M12 is service_date.py:299-301 (`if not (len(same) == 1 and all(...)): return bad several_dates`); with it replaced by 'first = sorted(same)[0]', s/r5sev.py prints 'stated March 21, 2026' for a DOS cell '03/21/2026 and 03/28/2026', for '03/21/2026, 04/05/2026' and for two DOS-type columns with different dates, where f9c0faf prints the blank (reason several_dates). S18 is service_date.py:373-375 (`_decide(span, ...)`): with `span[:1]`, 'UB-04. Statement period 06/09/2026 to 06/12/2026. Statement period 07/01/2026 to 07/03/2026. Rev 0450 ER FL47 charges $2,105.00.' prints 'June 9-12, 2026' instead of the blank (s/r5ub2.py). The old test for the DOS-cell case was converted to a sentence ('test_a_claim_form_sentence_with_two_service_dates_prints_the_blank') and lost its table twin. Also surviving: N8 (_WINDOW 60 -> 40 for the UB label look-back) and N15 (a financial word removed in the check's list only, so check and production disagree and nothing notices).",
   "why_it_matters": "Checklist 13: a test must fail when the code breaks. A charge for two visits would print the first visit's date as 'the' date of service if this rule broke, and the handoff's mutant list (M1-M22, L1-L11, B1-B6 ...) does not include either. The T-207 r2 finding was exactly this: rules stated in the doc but never pinned.",
   "fix": "Add DOS-table tests for: two dates in one DOS cell, two DOS-type columns with different certain dates, one certain and one doubtful; and a UB-04 with two statement periods (blank), with one period (range). Add boundary tests for the 60-character label look-back and a check-vs-production agreement test over the financial list.",
   "acceptance_test": "Re-run mut5.py S18, mutport.py M12, N8 and N15: all four must be KILLED by the unit suite."},
  {"severity": "minor",
   "title": "An encounter record's own date is lent to a charge whose sentence names another time in words the tokenizer does not treat as a date (judgment call: D-073 as written allows it)",
   "evidence": "s/r5cls.py (o/r5cls.new): source 'Dr. Reyes, visit note', record date 2026-02-20: 'Physical therapy charge $400.00 in October 2025.' and 'Physical therapy charge $400.00 (previous provider, earlier episode).' are classified charge and print 'February 20, 2026'. service_date.py:382-390 refuses only a parsed date that differs or a visit count.",
   "why_it_matters": "The printed date contradicts the quote beside it (October 2025). The paralegal sees both, so this is a recoverable error, but the D-073 intent was that prose never decides a date; here prose is ignored where it disagrees with the record date.",
   "fix": "Treat a month-name (with or without a year), 'ago', 'last', 'prior', 'previous', 'earlier', 'next' in the charge sentence like another date: print the blank. Or ask the orchestrator to accept the residual in SCOPE_CUTS row 28.",
   "acceptance_test": "head() for the two sentences above returns the blank; the sample ER and MRI lines are unchanged."},
  {"severity": "minor",
   "title": "The UB-04 'statement period' label has no previous/next guard: a prior statement's period prints as the service period of a coded line",
   "evidence": "s/r5ub.py (o/r5ub.new): 'UB-04. Previous statement period 05/01/2026 to 05/31/2026, balance forward $0.00. Rev 0450 ER FL47 charges $2,105.00.' with record date 2026-06-19 -> classified charge, prints 'May 1-31, 2026'. service_date.py:76 `_UB_SPAN` accepts any 'statement period' / 'statement covers period' label before a date within 60 characters.",
   "why_it_matters": "Same guard-list class as r4 (prose labels with closed qualifier lists), now on the only prose label D-073 still reads. UB-04 form text rarely says 'previous', but a statement of account that carries the prior period does.",
   "fix": "Require the label to start its own cell or sentence (nothing before it but start, a colon, or a header word such as UB-04/FL6), or refuse when previous/prior/next/last/balance forward stands in the same sentence.",
   "acceptance_test": "The probe above prints the blank; lib10's 'June 9-12, 2026' lines are unchanged."},
  {"severity": "minor",
   "title": "The duplicate-promotion flag still prints a date read from prose ('on 2026-03-01') for a line whose letter text is the blank",
   "evidence": "amounts.py:875 `f\"{where}: {_usd(...)} on {target['basis']['dos']}. \"`; s/pdup.py output: 'This looks like the same charge as “DOS 03/01/2026 office visit charge $220.00.” in record 1: $220.00 on 2026-03-01.' while the same line prints the blank in the letter. basis.dos comes from amounts.charge_basis -> _dates_in / _record_period, which still read sentences (it is also the duplicate key).",
   "why_it_matters": "D-073 says prose labels are no longer read for charge dates at all and that Step 3 shows exactly what the letter prints. This message is the one place that still states a prose-read date to the paralegal. Using the date as a dedupe key is fine; showing it is the leak.",
   "fix": "Drop the date from the message ('... the same charge as \"...\" in record 1: $220.00. Counting both ...') or print it only when store.charge_service_date says stated.",
   "acceptance_test": "promotion_flag message for the probe contains no ISO date; a test asserts the message text for a stated and a not-stated pair."},
  {"severity": "minor",
   "title": "The declared encounter table is wider than the D-073 clarification, and 9 of the 15 distinct dated corpus lines depend only on the extra words",
   "evidence": "encounter_types.json line 9 lists mri, x-ray, ct scan, ultrasound, exam, evaluation, follow-up, new patient, consult. The clarification lists visit, progress or office note, ED/ER record, discharge summary, PT or therapy note, ambulance run report, operative report. s/kinds_corpus.py (o/kinds_corpus.out): 38 corpus labels match only through the extra words, including 'Austin Imaging, cervical MRI' (the sample's golden $2,150 line, and 8 other MRI lines). The handoff discloses it ('one line in the JSON to drop').",
   "why_it_matters": "An MRI is a service, not a document type; 'Imaging' was ruled out as a provider name and 'MRI' is the same evidence with a different noun. Dropping the words would blank the sample golden line, so it is a product decision, not a code bug.",
   "fix": "Orchestrator to amend the D-073 clarification to name the extra words, or to restrict them to 'report/note/visit/record' compounds ('mri report', 'follow-up visit').",
   "acceptance_test": "The clarification text and encounter_types.json list the same words; a test compares them."},
  {"severity": "nit",
   "title": "letter_check and production read UB '09/06/2026 to 09/12/2026' differently",
   "evidence": "o/r5_pa_diff.out: 'DISAGREE UB 09/06/2026 to 09/12/2026  September 6-12, 2026  charge line's date is not certain from its quote (the line prints a date no source ties to it)'. Production uses one day/month order for both ends; the check enumerates mixed-order combinations (evals/letter_check.py _readings). Same disagreement at 8cb5bd2.",
   "why_it_matters": "A correct production line would fail the eval if a case like it were added. Stricter, not looser, so no wrong date is hidden.",
   "fix": "Make the check enumerate same-order readings only, or document the stricter rule.",
   "acceptance_test": "A UB period with both ends ambiguous and one feasible order passes the check."},
  {"severity": "nit",
   "title": "test_t205 dropped an assertion without a replacement",
   "evidence": "git diff ad0d91a f9c0faf -- tests/e2e/guided/test_t205.py: removed `assert \"statement dated March 1, 2026\" in page.get_by_test_id(\"line-sub\").inner_text()`. I restored it in the e/ copy and ran `pytest tests/e2e/guided/test_t205.py -k case_09`: 1 passed, so it still holds.",
   "why_it_matters": "Coverage of the review-list sub-line for a not-stated charge was lost for no reason.",
   "fix": "Put the assertion back.",
   "acceptance_test": "test_case_09_shows_the_blank_not_the_statement_date_as_the_service_date asserts line-sub contains 'statement dated March 1, 2026'."}
 ],
 "whats_right": [
  "Every prose-label shape from r2, r3 and r4b (DOS, visit of, Treatment dates A to B, next visit date, dotted leaders, DOI/DOB/authorization) prints the blank, and an identified encounter note without another date or visit count keeps its own date: the sample ER and MRI lines and lib10's UB-04 range are unchanged.",
  "The two classifiers agree on all 177 corpus records, the unit suite is 6668 green, and the 84-line charge dump, the CLI output and letter_check are reproducible run to run.",
  "The test rebase turned each sentence case into a blank assertion and added a DOS-table twin instead of deleting it; 35 of my 37 new mutants and all of the B1-B6, R1-R3, H3-H6, N1, F3 pins from T-207 r2 are killed."],
 "questions_for_chris": [
  "D-073 clarification names seven document types; the table also accepts MRI, exam, evaluation, follow-up and new patient. Is that the intended list? It decides whether the sample's $2,150 MRI line keeps its date (F6)."]}
```
