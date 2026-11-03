# T-202 (D-071) — paralegal review (Maria Delgado, senior PI litigation paralegal)

**Verdict: fail.** The rule hits two blockers on bill shapes I see every week. The corpus letters are now right.
- **case_09:** "billing statement, February 2, 2026: $275.00". The quote reads "Statement for visit of 2026-02-02".
- **lib14:** both ambulance lines print "September 14, 2026", from "Invoice for the run of 09/14/2026".
- **lib10:** all four UB-04 lines print "June 9–12, 2026", with an en dash, from "statement period 06/09/2026 to 06/12/2026".
- **sample:** unchanged.
- **All 25 cases:** charges are in service-date order. The T-200 form still covers the undated ledger lines (lib06, 09, 11, 12, 15).

An adjuster checking those lines against the bill pages would find nothing to attack.

**Blockers (probe text, live or paste path).** The per-line parse still prints a date the row does not tie to the charge:
- **Posting date as service date.** In a ledger table whose Posted column comes before DOS, the letter prints the posting date as the service date. This is the exact D-071 error.
- **First claim date on every line.** On a CMS-1500 that lists "dates of service 06/24/2026 and 07/08/2026", every line gets June 24. That includes the injection the chart dates July 8.

**Majors:**
- **Step 3 shows a different date from the letter.** Step 3, where I accept the charge, still labels it with the bare statement date ("UB-04 itemized bill · June 19, 2026"). The case API carries no service date, so the date the letter prints is never shown to me before export.
- **The eval cannot catch the wrong date.** letter_check accepts any service date the record states, not the line's own date. The CMS-1500 mis-date passes with 0 violations.

**Scope.**
- **Build:** `git archive f0921e4` extracted to the session scratchpad (t202/).
- **Server:** fixture backend FIXTURE_SET=curated. Demo mode (health: demo_mode true) with ZLAYT_MODE=local for /api/library, on http://127.0.0.1:7972.
- **Shutdown:** listener PID 82425 was killed. `lsof` returned exit 1 and `curl` returned 000.
- **Parent comparison:** a44cfa7, run in-process from its own archive (t202parent/).
- **Evidence:** artifacts/review-evidence/T-202-paralegal/.

**Deterministic checks first (from the f0921e4 archive):**
- `pytest tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py`: "19 passed in 5.78s" (pytest-t202.out).
- `python -m evals.letter_check`: `{"value": 0, "cases": 25, ...}` (letter_check.out).

```json
{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "commit f0921e4 (git archive extracted to session scratchpad t202/), parent a44cfa7 for the before/after diff (t202parent/). Demo mode: fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, http://127.0.0.1:7972 (health demo_mode true); listener PID 82425 stopped (lsof exit 1, curl 000). Cases: sample (load-sample tile), case_09 (POST /api/cases with the golden text because the demo UI turns the paste tile off, then opened in the UI), case_lib14 and case_lib10 (library tile). Evidence dir artifacts/review-evidence/T-202-paralegal/.",
 "exercised": [
  "Read personas/paralegal.md, D-071 (memory/ORCHESTRATOR_DECISIONS.md:84), board.py show T-202 (AC, notes, handoff with letter diffs), git show f0921e4 (amounts.py, export.py, store.py, evals/letter_check.py, tests)",
  "From the archive: pytest test_t202 + test_t200 '19 passed in 5.78s' (pytest-t202.out); python -m evals.letter_check value 0 over 25 cases (letter_check.out)",
  "Playwright on the running archive app (h.py + p01_cases.py): sample, case_09, lib14, lib10 driven keyboard-first through Steps 1-4, every Step 3 bill card logged and screenshotted, letter + notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); scripted times 15.5 s / 7.2 s / 13.1 s / 19.0 s (p01.out, p02.out)",
  "Read every charge line of the four letters against the bill page in the record (service date vs statement date, UB-04 period, order)",
  "Before/after: same letters generated in-process from a44cfa7 and f0921e4; diff shows only the six date changes the handoff lists (parent-vs-f0921e4.diff)",
  "All 25 letter_check cases, counted variant: every BILLED CHARGES line with the record it quotes (all_charge_lines.out), checked by hand for date and order",
  "GET /api/cases/{token} for the lib10, lib14 and case_09 runs: charge amounts carry no service-date field (api-amount-fields.out)",
  "Probes of the shipped date path (store.charge_service_dates -> export._date_range) on SYNTHETIC bill shapes: probe_dates.out (10 shapes), probe_dates2.out (ledger tables, CMS-1500 with two dates), probe_eval_teeth.out (letter_check on the wrong dates)"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 3, "letter_dates_correct_on_corpus": 5, "adjuster_credibility": 3},
 "findings": [
  {"severity": "blocker",
   "title": "Ledger table with the Posted column before DOS: the letter prints the posting date as the date of service",
   "evidence": "artifacts/review-evidence/T-202-paralegal/probe_dates2.out, probe T2. Record 'Posted      DOS         CPT ...' / '06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00' gives 'letter date -> June 11, 2026'; the next row (posted 06/18, DOS 06/17) gives 'June 18, 2026'. With DOS first (T1) it prints June 10 / June 17. The parse takes the first date in the row (amounts.py charge_basis) and ignores the column header.",
   "why_it_matters": "This is the error D-071 exists to stop: a billing-side date printed in the date-of-service slot. The adjuster's first move is to match the letter date to the bill and the chart note, and here neither matches. The paralegal never sees this date before export (see the Step 3 major), so she cannot catch it. Not in the 25-case corpus or the demo; reachable on any pasted ledger in live mode.",
   "fix": "Read the row's date by its column: use the ledger header (billing.py already parses DOS vs Posted columns, api.md GET /billing 'dos' vs 'posted'). When a row has two dates and no header says which is the DOS, use the T-200 form, not a guess.",
   "acceptance_test": "Unit test on the T2 text: the $70.00 line prints 'June 10, 2026' and the $95.00 line 'June 17, 2026'. Same rows without a header give the '(statement dated ...; service date not stated)' form. Add a SYNTHETIC library or golden case with a Posted-first ledger to the letter_check corpus."},
  {"severity": "blocker",
   "title": "CMS-1500 listing two dates of service ('06/24/2026 and 07/08/2026'): every charge line gets the first date",
   "evidence": "artifacts/review-evidence/T-202-paralegal/probe_dates.out P2 and probe_dates2.out T3: 'CMS-1500 for dates of service 06/24/2026 and 07/08/2026 ... CPT 99204, $185.00 ...; CPT 20610, $210.00' -> both '$185.00 ... letter date -> June 24, 2026' and '$210.00 ... letter date -> June 24, 2026'. amounts.py:435-445 _record_period returns the first matched date; 'and' is not a range join, so no end date is kept. This is the shape of lib10 record 8 (Wardlaw Orthopedics CMS-1500), where the chart dates the injection (CPT 20610) 'July 8' (record 7: 'Injection performed').",
   "why_it_matters": "The letter ties the injection charge to June 24, a visit where no injection was done. The record does not say which line is which date, so the pairing is invented. An adjuster who lines the specials up against the chart finds a charge on a day with no matching service and uses it to question the whole bill set.",
   "fix": "Inherit the record's date only for a true period (a range join). For a list of discrete dates with no per-line date, print the T-200 form, or name the claim dates without assigning one: 'Wardlaw Orthopedics, CMS-1500 (claim dates of service June 24 and July 8, 2026; line date not stated)'. D-071 says that when no service date is stated the T-200 form applies.",
   "acceptance_test": "Unit test on the T3 text: neither charge line prints a bare single date. Both carry the not-stated form, or the two-date claim form above. letter_check, run on a corpus case of this shape, reports a violation when a single claim date is printed."},
  {"severity": "major",
   "title": "Step 3 labels each dated bill charge with the statement date, not the date the letter prints; the API carries no service date",
   "evidence": "p02.out Step 3 cards: '[lib10] ... Charge / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $4,920.00'; '[lib14] ... Charge / Tarnwick Fire-Rescue, ambulance invoice · November 12, 2026 /  / $1,380.00'; '[case_09] ... Charge / Hobbleton Family Clinic, billing statement · March 1, 2026 /  / $275.00'. Screenshots lib10-s3-00-a2.png, lib14-s3-01-a2.png, case_09-s3-00-a1.png. The letters for the same items say June 9–12, September 14 and February 2 (ui-lib10-letter.txt, ui-lib14-letter.txt, ui-case_09-letter.txt). api-amount-fields.out: the charge amounts a2-a5 (lib10), a1/a2/a4 (lib14) and a1 (case_09) have no dos/date/service/period field.",
   "why_it_matters": "I accept a charge on a card that shows June 19 bare beside it, which reads as the charge's date. Then the letter says June 9–12, a date I was never shown and cannot check on the screen where I decided. The two blockers above are invisible for the same reason. If I compare the letter to my review, they disagree, and I would either lose trust in the tool or 'correct' a right date.",
   "fix": "Expose the D-071 service date or period on each charge in the case view (backend: dos_iso/dos_end_iso, or the T-200 'not stated' state). Show it on the Step 3 card exactly as the letter will print it, with the statement date labelled as such: 'Service June 9–12, 2026 · statement dated June 19, 2026'.",
   "acceptance_test": "E2E: for lib10, lib14 and case_09, the Step 3 card text of every charge contains the same date string as its BILLED CHARGES line in the downloaded letter. No charge card shows a billing document's record date without the word 'statement'."},
  {"severity": "major",
   "title": "letter_check's date check accepts any service date the record states, not the line's own, so the wrong-date class passes; AC wording ('equals the service date in its quote') is not what it checks",
   "evidence": "evals/letter_check.py:209 'ok = ok or (first in service and (last is None or last in states))', where service is every non-statement-led date in the record. probe_eval_teeth.out: 'T3 injection line dated with the other claim date (what f0921e4 prints) / violations: []'. Card AC 1: 'asserts each dated charge line's date equals the service date in its quote'; the lib10 quotes ('FL47 total charges $4,920.00.') contain no date at all.",
   "why_it_matters": "'value 0 over 25 cases' is the evidence the card was ticked on, but the check cannot tell a right line date from another date on the same bill. The blocker class above would ship green.",
   "fix": "Pin the per-line expected date in the goldens: case_09, lib14 and lib10 expected letters, plus the T2/T3 probe shapes as SYNTHETIC cases. Make the check tie the date to the line's row or the record's stated period, not to any date in the record.",
   "acceptance_test": "Mutant: print the first claim date on every CMS-1500 line, or the posted column of a ledger row. letter_check reports at least one violation on the corpus."},
  {"severity": "minor",
   "title": "Some charge quotes name neither the service nor the date the line now prints (pre-existing quote span, unchanged by T-202)",
   "evidence": "ui-lib10-letter.txt: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00' / 'Source [Ex. __ / Bates __]: \"FL47 total charges $4,920.00.\"'. The record says 'Rev 0120 room and board semi-private, ... FL46 3 days, FL47 total charges $4,920.00'. ui-lib14-letter.txt: '... September 14, 2026: $187.05' / '\"charge $187.05.\"'. The record: 'A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05'. parent-vs-f0921e4.diff shows these quote lines identical on a44cfa7.",
   "why_it_matters": "The date is now right, but its source ('statement period ...', 'Invoice for the run of 09/14/2026') is outside the quoted words. The adjuster has to open the page to see what $4,920 or $187.05 was for and when.",
   "fix": "Quote the whole bill line from its code or description through the figure ('Rev 0120 room and board semi-private ... FL47 total charges $4,920.00.'; 'A0425 ground mileage, loaded, 8.7 miles ... charge $187.05.').",
   "acceptance_test": "Every BILLED CHARGES quote on a bill record contains the line's service code or description. letter_check can assert this for lib10 and lib14."},
  {"severity": "nit",
   "title": "Same-day charges tie-break by record number, so lib14 lists the ED before the ambulance that took the patient there",
   "evidence": "export.py:185 sort key (dos_iso, record_no, id). ui-lib14-letter.txt lists 'Orrin Mere Regional ED, September 14, 2026: $2,960.00' (record 2) before 'Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00' (record 8).",
   "why_it_matters": "Specials usually run in the order care was given (transport, then ED). It is cosmetic, but it reads oddly to an adjuster following the chronology above.",
   "fix": "Optional: on a same-day tie, sort by the earliest timeline entry of the same provider, or put transport first.",
   "acceptance_test": "lib14 letter lists the ambulance lines before the ED line."}
 ],
 "whats_right": [
  "case_09, lib14 and lib10 now print the service date or the UB-04 period ('June 9–12, 2026'), never the statement date; the sample letter is unchanged",
  "The period and single-date parse handles 'to', 'through', a hyphen, a month crossing, an invoice date stated before the run date and 'statement date ..., date of service ...' in one sentence (probe_dates.out P3-P7, P9)",
  "The T-200 '(statement dated X; service date not stated)' form still covers the counted undated ledger lines, and the letter_check count path now exercises it (lib06, 09, 11, 12, 15)"
 ],
 "questions_for_chris": []}
```
