# T-202 (D-071) staff-engineer review, commit f0921e4

Verdict: **fail** (2 blockers, 3 majors, 2 minors).

Date selection is code, with no LLM in the path (`amounts.charge_basis`, `store.charge_service_dates`, `export._date_range`). Output is deterministic: the dump of every charge line over 25 cases is identical on two runs. The missing-date path works: lib06, lib09, lib11, lib12 and lib15 print the T-200 "statement dated X; service date not stated" form, and an invalid date such as 02/30/2026 or 2026-13-04 falls into that form visibly. Unit (5890 passed, 5 skipped) and guided e2e (128 passed) are green from `git archive f0921e4`, and `python -m evals.letter_check` gives value 0 over 25 cases.

The new parser is wrong in three ways the green runs do not show, because the eval check reuses the production regex and compares against the whole record:

1. It guesses ambiguous numeric dates (`04/05/2026` prints "April 5, 2026"). `docs/LLM_VS_CODE.md` row 2 and D-027 say these are never guessed.
2. A month-name period ("June 9-12, 2024") loses its stated year and its end date. With a 2026 statement date it prints "June 9, 2026".
3. `letter_check.charge_date_violations` does not fail when a line prints another line's date from the same record, or when a period's end is dropped.

```json
{"card": "T-202", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit f0921e4 (HEAD at review time): app/backend/amounts.py, export.py, store.py, evals/letter_check.py, tests/unit/test_t202_charge_service_dates.py, memory/contracts/api.md; git archive copy at artifacts/review-evidence/T-202-staff/a; probes and mutants in artifacts/review-evidence/T-202-staff/s; 25 cases in evals/golden and evals/library, fixture backend",
 "exercised": [
  "read personas/staff-engineer.md, D-071 (memory/ORCHESTRATOR_DECISIONS.md:84), card T-202 and handoff, docs/LLM_VS_CODE.md row 2/3, git show f0921e4 (full diff of all 7 files)",
  "git archive f0921e4 into artifacts/review-evidence/T-202-staff/a; HEAD == f0921e4 (git rev-parse HEAD)",
  "pytest tests/unit -q from the archive: 5890 passed, 5 skipped in 459s",
  "pytest tests/e2e/guided -q from the archive: 128 passed in 170s",
  "python -m evals.letter_check from the archive: {value: 0, cases: 25}",
  "s/dump.py: every BILLED CHARGES header+quote over 25 cases x (all_accepted, counted); run twice, diff identical (deterministic)",
  "s/probe1.py and s/probe4.py: charge_basis + store.charge_service_dates on 45 hand-built lines (multi-line ledger, table row, two service dates on one line, posted/paid dates, amount-before-date, 03/04/2026, 13/04/2026, 04/05/26, 4/5, 12/28 on a January statement, ISO, invalid dates, periods crossing month/year, reversed and same-day periods, hyphen/en-dash/through forms, month-name periods, two periods, no date, statement date only, 98 two-digit year)",
  "s/probe2.py: modified lib11 ledger through the full pipeline (dated, ambiguous, two-dates, multi-line variants) and read the printed letter lines",
  "s/probe3.py: charge_date_violations on a two-line ledger with right, wrong-line, not-in-record, statement, ambiguous-reading and dropped-period-end headers",
  "mutants M1..M6 applied in the archive copy (s/mut.py), each run through letter_check; M3/M5/M6 also through test_t202 + test_t200, and M5 through 888 export/letter/charge/golden/api unit tests; files restored (diff -q against s/export.orig and s/store.orig clean)",
  "grep of amounts.py for provider/llm imports, float( and except: none in the date path"],
 "verdict": "fail",
 "scores": {"deterministic_parse_no_llm": 5, "date_correctness_edge_cases": 1, "ambiguity_policy_LLM_VS_CODE_row2": 1, "period_range_handling": 2, "eval_check_has_teeth": 2, "test_quality": 2, "missing_date_visible_state": 4},
 "findings": [
  {"severity": "blocker",
   "title": "Ambiguous numeric dates are guessed and printed as the date of service (violates LLM_VS_CODE row 2, D-027)",
   "evidence": "docs/LLM_VS_CODE.md:30 '04/05/2026 fits two readings ... it is ambiguous, never guessed, and waits for the paralegal'; app/backend/dates.py:3-4 'Nothing is ever guessed'. app/backend/amounts.py:380-395 _dos_iso picks month-first. Repro (s/probe2.py, lib11 ledger with '04/05/2026 x-ray charge $180.00'): the letter prints 'Fennimoor Spine Clinic, itemized ledger, April 5, 2026: $180.00' with no Dates-to-confirm state. s/probe4.py: 'Office visit 03/17/98 charge $220.00' -> 1998-03-17 (D-027 says '03-17-98' is ambiguous 1998/2098); '4/5' takes its year from the statement date. Before f0921e4 this guess only drove the duplicate match; the card now prints it as a fact. The eval check cannot see it: probe3 'ambig April 5' -> [] and 'ambig May 4' is flagged only because it differs from the guess.",
   "why_it_matters": "A paralegal sends a letter that asserts one reading of a date the record does not settle. The adjuster cross-checks dates, and the project's own rule is to ask, not guess.",
   "fix": "For a charge line's own date, reuse dates.parse_date semantics: an ambiguous or two-digit-year-over-pivot date yields no printed service date. Take the existing T-200 'service date not stated' route, or carry an ambiguous state the paralegal resolves with confirm_date. Do not borrow a year for a year-less date.",
   "acceptance_test": "Unit test through export_case: a ledger line '04/05/2026 x-ray charge $180.00' does not print 'April 5, 2026' or 'May 4, 2026' and shows a visible state. '13/04/2026' and '2026-04-05' still print. '03/17/98' does not print 1998. evals/letter_check flags a letter that prints the guessed reading."},
  {"severity": "blocker",
   "title": "A month-name period loses its stated year and its end date; the printed date can be wrong",
   "evidence": "app/backend/amounts.py:274-281 _DOS_RX: the month-name branch needs ',?\\s+YYYY' right after the day, so 'June 9-12, 2024' matches only 'June 9' (year-less) and _year_for (amounts.py:364-369) borrows the statement year. s/probe4.py with record date 2026-06-19: 'statement period June 9-12, 2024' -> dos=2026-06-09 end=None, so the letter prints 'June 9, 2026' for a 2024 stay. 'June 9-12, 2026' -> '2026-06-09', end None (printed 'June 9, 2026', a one-day service); 'June 28-July 2, 2026' -> end None. D-071 prints periods as 'June 9-12, 2026', the month-name form itself.",
   "why_it_matters": "This prints a date the record does not state (wrong year), and collapses a multi-day stay to one day. Late-submitted bills in injury claims routinely sit more than a year after the stay.",
   "fix": "Parse 'Month D-D, YYYY' and 'Month D-Month D, YYYY' as a period with their own year. When a year-less month-name date is followed by a later year, never apply the statement-year heuristic.",
   "acceptance_test": "charge_basis on 'statement period June 9-12, 2024' (record date 2026-06-19) returns dos 2024-06-09, dos_end 2024-06-12. 'June 28-July 2, 2026' returns 2026-06-28 and 2026-07-02. The letter prints 'June 9-12, 2024'. The same cases are added to the golden set so letter_check covers them."},
  {"severity": "major",
   "title": "Hyphen-joined numeric periods without spaces drop the end date",
   "evidence": "_DOS_RX starts with (?<![\\w/.$-]) (amounts.py:275), so the second date after '-' is not matched. s/probe4.py: 'statement period 06/28/2026-07/02/2026' -> dos=2026-06-28 end=None; '06/28-07/02/2026' -> end=None. The spaced and en-dash forms work ('06/28/2026 - 07/02/2026', '06/28/2026–07/02/2026'). Letter prints 'June 28, 2026' for a June 28-July 2 stay; letter_check passes it (M3 below).",
   "why_it_matters": "'MM/DD/YYYY-MM/DD/YYYY' is a common billing period format. D-071 says a period prints as a range.",
   "fix": "Let the range-end match accept a '-' immediately before it when it follows a date, in _record_period and _dates_in. Keep the lookbehind for other uses.",
   "acceptance_test": "charge_basis on '06/28/2026-07/02/2026' returns (2026-06-28, 2026-07-02); the letter prints 'June 28-July 2, 2026'."},
  {"severity": "major",
   "title": "Two service dates on one charge line: the later one is printed and the earlier is lost, with no flag",
   "evidence": "amounts.py:507 'dos = ds[-1][2]' (non-row) / 'ds[0][2]' (row) takes one date. s/probe1.py: 'Office visits 03/01/2026 and 03/08/2026 charge $220.00' -> dos=2026-03-08. Full pipeline (s/probe2.py 'twodates'): 'New patient exam 03/27/2026 and x-ray 03/28/2026 charge $250.00' prints 'March 28, 2026: $250.00'. letter_check passes it.",
   "why_it_matters": "A charge that covers two dates is reported as one. The quote on the next line shows both, but the header asserts one service date.",
   "fix": "When a charge line states more than one service date and they are not a range, do not pick one: take the 'service date not stated' route or a visible 'multiple dates' state.",
   "acceptance_test": "Unit test: a line with two non-range service dates does not print a single bare date; letter_check flags the old output."},
  {"severity": "major",
   "title": "evals/letter_check date check is weaker than the AC: it compares against the whole record using the production parser",
   "evidence": "evals/letter_check.py charge_date_violations: 'ex = r[\"excerpt\"]' (whole record) and states built from AM._DOS_RX / AM._dos_iso (same code as the thing under test). s/probe3.py on a two-line ledger (03/01 $100, 03/08 $120): header 'March 8, 2026' on the $100 line -> [] (should fail). Header with a dropped period end ('June 9, 2026' for 06/09-06/12) -> []. Mutants in the archive (s/mut.py): M1 print record date -> value 28; M2 +1 day -> 148; M4 bare statement date on undated -> 20 (all fail, good). M3 drop period end (_date_range(a['dos_iso'])) -> value 0, survives. M6 print the record's first date -> value 0, survives (the corpus has no multi-date ledger); test_t202 catches M3 (3 failed) and M6 (1 failed) only through lib10 and a charge_basis unit test, not through the eval. AC 1 says 'equals the service date in its quote'.",
   "why_it_matters": "The check is the harness upgrade this card promised. Today it only catches a date that is in no part of the record, which is the T-200 error class. It shares the parser's ambiguity guess (finding 1), so it cannot detect an error in that parser.",
   "fix": "Check per line: when the quote itself contains a date, the printed date must equal the date parsed from the quote; for a period header with the date in a heading line, require the full period (first and last) rather than only the first. Do not call AM._dos_iso for ambiguity, reject ambiguous readings in the check. Add a multi-date ledger and a hyphen period to the golden or library set.",
   "acceptance_test": "charge_date_violations returns a violation for the wrong-line header and for a dropped period end (probe3 cases). Mutants M3 and M6 give a non-zero letter_check value on the committed corpus."},
  {"severity": "minor",
   "title": "Sort-by-service-date has no discriminating test",
   "evidence": "Mutant M5 (export.py in_charges returns 'got' unsorted): letter_check value 0; test_t202 + test_t200 19 passed; 888 export/letter/charge/golden/api unit tests passed. tests/unit/test_t202_charge_service_dates.py:test_charges_are_listed_in_service_date_order uses lib06, whose record order already equals date order.",
   "why_it_matters": "A stated behavior of the commit can be removed with no test failing.",
   "fix": "Test with a case where record order differs from service-date order (a later-dated statement record listed before an earlier visit).",
   "acceptance_test": "M5 fails at least one unit test."},
  {"severity": "minor",
   "title": "store.charge_service_dates falls back to the record's date when the line cannot be read, which for a bill is the statement date",
   "evidence": "app/backend/store.py (charge_service_dates): 'return (None, None) if counted_undated else ((rec or {}).get(\"date_iso\"), None)'. s/probe4.py: pos=None on a ledger line with only a statement date returns ('2026-06-15', None). The docstring admits the fallback. I could not show a production path that produces pos=None; amount_pos is None only when the stored excerpt does not hold the raw text at the stored index.",
   "why_it_matters": "It is a silent fallback to the exact error D-071 removes, in the one branch no test reaches.",
   "fix": "For a billing document return (None, None) there (the statement form); keep the record date only for a non-billing encounter record (AM.billing_document).",
   "acceptance_test": "Unit test: pos=None on a ledger record returns (None, None); on a visit note returns the visit date."}
 ],
 "whats_right": [
  "Date choice is code only and byte-deterministic (two full dumps identical); a line with no readable service date takes the visible T-200 statement form (lib06/09/11/12/15) instead of a bare date.",
  "The three mutants the handoff claims (record date, +1 day, bare statement date) do fail letter_check (28 / 148 / 20 violations) from a git-archive copy; unit and guided e2e are green from the archive.",
  "_date_range handles same-month, cross-month and cross-year periods and a same-day period collapses to one date, with a unit test on each."],
 "questions_for_chris": []}
```
