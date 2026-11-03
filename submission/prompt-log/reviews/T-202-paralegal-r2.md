# T-202 round 2 (D-071 amendment + clarification) — paralegal review (Maria Delgado, senior PI litigation paralegal)

**Verdict: fail.** Both of my round 1 blockers are fixed:
- **Posted-first ledger:** prints the DOS column (June 10, June 17).
- **CMS-1500 "06/24/2026 and 07/08/2026":** prints the not-stated form, with a clear Step 3 note.

The corpus letters (sample, case_09, lib14, lib10) are byte-identical to round 1, and correct. lib10 keeps "June 9–12, 2026" under the D-071 clarification.

**Blocker.** More adversarial bill text shows the same class of error from another direction. A non-service date in the charge's own sentence or row is printed as the date of service:
- a patient birth date;
- the date of injury or accident;
- an onset date;
- a referral or order date.

"Birth date 03/15/1980, CPT 99204 $185.00." prints `Wardlaw Orthopedics, CMS-1500, March 15, 1980: $185.00`. In a visit note dated January 16, "Follow-up for collision of 01/09/2026, visit charge $150.00." prints January 9. That replaces the correct visit date with the accident date. Before T-202, the letter printed the record date here, which was right. letter_check passes all four wrong letters with 0 violations.

**Major.**
- **The letter contradicts its own quote.** When the code cannot settle a date that the bill does write, the letter line says "service date not stated", and the quote directly under it shows the date of service.
- **The confirm note leads nowhere.** It asks me to confirm the date, but nothing I confirm can reach the letter.

**Scope.**
- **Build:** `git archive 986fc55` (archive commit id printed 986fc551078a…) extracted to the session scratchpad (pr2_986fc55/).
- **Server:** fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local (health: demo_mode true), http://127.0.0.1:7976.
- **Shutdown:** listener PID 49534 killed. `lsof` exit 1, `curl` 000.
- **Comparison:** f0921e4 (round 1 archive) used for the before/after on the new probes.
- **Private values seen:** 0.

**Deterministic checks first (from the 986fc55 archive):**
- pytest `test_t202_r2_service_date_layouts.py`, `test_t202_charge_service_dates.py` and `test_t200_undated_charge_label.py`: "67 passed in 7.14s" (pytest-t202.out).
- `python -m evals.letter_check`: `{"value": 0, "cases": 25, ...}` (letter_check.out).

**Not-stated wording and confirm note, read as a demand letter:**
- **Where the quote has no date** (lib11 counted ledger lines: `Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00`, quote "New patient exam charge $250.00"), the wording is true and pastes cleanly. I would still request a dated itemized bill before sending. The internal notes do not tell me to (minor).
- **Where the quote states a date the code would not read** (ambiguous numeric, two-digit year, no year, several dates), "service date not stated" is false on the page. The adjuster sees the firm say the bill states no date of service, right above a quote that reads "Date of service 04/05/2026".
- **The confirm notes are plain and specific** ("This line or its bill states more than one date (06/24/2026, 07/08/2026) and the record does not say which one belongs to this charge."). But "Confirm the date from the quote" is circular when the quote is what is unclear. Nothing I confirm reaches the letter.

**Step 3 (separate frontend card, not graded).** The Step 3 card still shows the statement date bare:
- case_09: "Hobbleton Family Clinic, billing statement · March 1, 2026" (p01.out:95);
- lib14: "· November 12, 2026" (p01.out:163);
- lib10: "· June 19, 2026" (p01.out:240).

The case API now carries the letter's text for each of these: "February 2, 2026", "September 14, 2026", "June 9–12, 2026" (api_service_date.out).

```json
{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 986fc55 (git archive, commit id 986fc551078a6ed6274cc9dd7a6a9efd0af357e3, extracted to session scratchpad pr2_986fc55/); f0921e4 archive (round 1) for the before/after on the new probes. Demo mode: fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, http://127.0.0.1:7976 (health demo_mode true); listener PID 49534 stopped (lsof exit 1, curl 000). Cases: sample (load-sample tile), case_09 (POST /api/cases with the golden text, then opened in the UI), lib14 and lib10 (library tile); lib11 and two SYNTHETIC case_09 variants in-process. Evidence: artifacts/review-evidence/T-202-paralegal-r2/. Private values seen: 0.",
 "exercised": [
  "Read personas/paralegal.md, D-071 + amendment + clarification (memory/ORCHESTRATOR_DECISIONS.md:84-92), my round 1 review, board.py show T-202 (notes, handoff), git show 986fc55 (service_date.py, store.py, export.py, present.py, letter_check.py, api.md)",
  "From the archive: pytest test_t202_r2_service_date_layouts + test_t202_charge_service_dates + test_t200_undated_charge_label '67 passed in 7.14s' (pytest-t202.out); python -m evals.letter_check value 0 over 25 cases (letter_check.out)",
  "Playwright on the running archive app (h.py + p01_cases.py): sample, case_09, lib14, lib10 driven keyboard-first through Steps 1-4; every Step 3 card logged and screenshotted; letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); cmp against my round 1 UI letters: all four identical",
  "GET /api/cases/{token} for the four runs: amounts[].service_date on every charge (api_service_date.out)",
  "Shipped path store.charge_service_date on 50 SYNTHETIC bill shapes: my round 1 texts P1-P10, T1-T3 unchanged, plus N1-N25 (probe_r2.out) and B1-B12 non-service dates (probe_r2b.out); B1-B12 also on f0921e4 (probe_r2b_on_f0921e4.out)",
  "letter_check.charge_date_violations on the round 1 wrong-date letters (T2, T3) and four round 2 wrong-date letters (B7, B8, B9, B12), with right-form controls (probe_eval_teeth_r2.out)",
  "In-process letters + notes (letters_dump_r2.py, all_accepted and counted): sample, case_09, lib14, lib10, lib11, plus SYNTHETIC case_09 variants with an ambiguous DOS and a two-date CMS-1500 (letters/, letters_dump_r2.out), read as a demand letter"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 3, "letter_dates_correct_on_corpus": 5, "adjuster_credibility": 3},
 "findings": [
  {"severity": "blocker",
   "title": "A birth, injury/accident, onset, referral or order date next to a charge prints as its date of service; in a visit note it replaces the correct visit date",
   "evidence": "artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.out. B7 'Birth date 03/15/1980, CPT 99204 $185.00.' gives 'Wardlaw Orthopedics, CMS-1500, March 15, 1980: $185.00'. B12 'Date of accident 01/19/2026 per intake, 99213 office visit $275.00.' gives 'January 19, 2026'. B11 'Onset 01/09/2026, 97110 ...' gives 'January 9, 2026'. B10 'Referral dated 02/10/2026, MRI charge $2,150.00.' gives 'February 10, 2026'. B3 row 'DOI 01/09/2026   99213   Office visit   $275.00' gives 'January 9, 2026'. Non-bill records: B8 'Follow-up for collision of 01/09/2026, visit charge $150.00.' in a note dated 2026-01-16 gives 'Dr. Alvarez, primary care, January 9, 2026'; B9 MRI report dated 2026-02-20, 'Ordered 02/10/2026, MRI cervical spine charge $2,150.00.' gives 'February 10, 2026'. probe_r2.out N11 (date of current injury) and N12 (DOB) give the same. Cause: service_date.py:297 takes any date in the line's own text unless the word before it is in the billing list at service_date.py:35 (statement, posted, paid ...), which has no birth/DOB, injury/DOI, accident, onset, referral or ordered. The non-bill fallback to the record's date (service_date.py:327) runs only when the sentence has no date. The same on f0921e4 (probe_r2b_on_f0921e4.out), so T-202 brought it in: before T-202 these lines printed the record's date. letter_check has the same blind spot (evals/letter_check.py:189 _BILLING_WORD, :263 _own_dates): B7, B8, B9 and B12 letters give 'violations: []' (probe_eval_teeth_r2.out).",
   "why_it_matters": "This is the D-071 error from the other side: a date that is not the date of service, printed in the date-of-service slot. A 1980 service date on a 2026 claim tells the adjuster nobody read the bill. A charge dated to the accident day, or to an intake date the records dispute (the sample case's 01/09 vs 01/19 conflict), puts the firm's own letter on one side of the DOI conflict the tool must not resolve. B8 is a regression: the visit date was right before T-202. The D-071 amendment allows a date only when it is the one certain service date; a birth or injury date is not one. These shapes are not in the corpus or the demo, but CMS-1500 items 3 (birth date) and 14 (date of current illness or injury) and PI bills' 'DOI' header put these dates next to charge lines on every paste.",
   "fix": "Add the non-service leads to the code's deny list: birth, DOB, injury, DOI, accident, DOA, collision, onset, referral or referred, ordered, admit or admission when it stands alone, and 'date of current'. Such a date never becomes the line's date: a bill line with no other date takes the not-stated form; a visit note keeps its own record date. Better still, allow-list: in a bill, take a date from the line's own text only when a service word (DOS, date of service, service date, visit, seen, run of, performed, or a CPT/HCPCS/revenue row under a DOS or Date heading) ties it to the line; otherwise not stated. Mirror the rule in letter_check with its own wording list.",
   "acceptance_test": "Unit fixtures on B3, B7, B8, B9, B10, B11, B12, N11 and N12 text: no line prints 1980, the injury, accident or onset date, or the referral or order date. The bills print the not-stated form; B8 prints January 16, 2026 and B9 February 20, 2026. letter_check reports a violation for each of the four wrong letters in probe_eval_teeth_r2.py. Add one SYNTHETIC library or golden case with a DOI/DOB-bearing bill line to the 25-case corpus."},
  {"severity": "major",
   "title": "Not-stated wording says 'service date not stated' above a quote that states the date of service; the Step 3 confirm note asks for a confirmation that can never reach the letter",
   "evidence": "artifacts/review-evidence/T-202-paralegal-r2/letters/synth_ambiguous_dos-all_accepted-letter.txt (SYNTHETIC case_09 variant, bill dated 2026-06-01). It reads 'Hobbleton Family Clinic, billing statement (statement dated June 1, 2026; service date not stated): $275.00' and then 'Source [Ex. __ / Bates __]: \"Date of service 04/05/2026: office visit charge $275.00.\"'. probe_r2.out N14 note: 'The date written as 04/05/2026 can be read as month/day or day/month, and the record does not settle which. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.' (service_date.py:66, :76). The same contradiction arises for a year-less date (N16 'February 2') and for several dates in the quote (P8 '06/12/26 06/13/26', N3, N7). No API or UI control takes a confirmed date: grep for service_date/confirm_note in the archive app/ finds only export.py, present.py, service_date.py and store.py, and no write route. The internal notes for the variant say nothing about the date (letters/synth_ambiguous_dos-all_accepted-notes.txt).",
   "why_it_matters": "'Service date not stated' is a statement about the record, and here it is untrue: the bill states one, and the letter quotes it one line below. The adjuster reads that as carelessness, or as the firm hiding a date. A Texas paralegal reads 04/05/2026 on a Texas bill as April 5. When she confirms that, the letter still says 'not stated', so she ends up hand-editing the letter in Word, outside the tool and its audit. The note's 'confirm the date from the quote' is circular: the quote is what is unclear, and the chart note or the provider settles it.",
   "fix": "Make the not-stated text true for each reason. No date in the line: keep '(statement dated X; service date not stated)'. A date written but not certain: show it verbatim, without reading it: '(date of service as written: \"04/05/2026\"; statement dated June 1, 2026)'. Several dates: '(claim dates of service 06/24/2026 and 07/08/2026; line date not stated)'. Reword the note so it says where to look: 'Check the visit note or the provider for the date; the letter will print ... until you confirm.' Then let her confirm one reading in Step 3, as the Step 2 date-to-confirm radios do for entries. The confirmed date prints, and the audit records her choice.",
   "acceptance_test": "For each reason (ambiguous_numeric, two_digit_year, no_year, several_dates), a fixture letter line never contains 'service date not stated' when its own quote contains a written date. After a Step 3 confirm of '04/05/2026 = April 5, 2026', the letter prints 'April 5, 2026' and the audit holds the confirm event."},
  {"severity": "minor",
   "title": "The not-stated string differs from the one quoted in the D-071 amendment",
   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:88 (amendment) binds '(service date not stated on this line; statement dated X)'. The build prints '(statement dated June 15, 2026; service date not stated)' (service_date.py:58 not_stated_text; letters/lib11-counted-letter.txt, 3 lines), the T-200 form. api.md documents the T-200 form.",
   "why_it_matters": "Two binding texts now disagree, and the eval pins whichever the code prints. The amendment's order (absence first, statement date second) reads better to an adjuster: the first thing after the provider is not a date that could be read as the DOS.",
   "fix": "Orchestrator to pick one string (see questions_for_chris). Then pin it in the decision, api.md, export and letter_check together.",
   "acceptance_test": "grep finds one not-stated wording across ORCHESTRATOR_DECISIONS.md, api.md, service_date.py and evals/letter_check.py."},
  {"severity": "minor",
   "title": "A ledger column headed 'Trans Date' is read as the date of service",
   "evidence": "artifacts/review-evidence/T-202-paralegal-r2/probe_r2.out N5. Header 'Trans Date   Code   Description             Charges', row '06/11/2026   97140  Manual therapy x1       $70.00' gives 'Larkspur Hollow Physical Therapy, itemized ledger, June 11, 2026: $70.00'. The non-DOS heading list (service_date.py _H_NON) has no 'trans', 'transaction' or 'entry'.",
   "why_it_matters": "In some practice-management ledgers the transaction date is the posting date. The amendment says any parse doubt gives the not-stated form, and a heading that does not name the service is a doubt.",
   "fix": "Treat a date column whose heading names neither the service (DOS, service, visit) nor a billing step as doubtful, and use the not-stated form. Or add trans/transaction/entry date to the non-DOS headings.",
   "acceptance_test": "Unit fixture N5: both lines give the not-stated form with a note naming the 'Trans Date' heading."},
  {"severity": "minor",
   "title": "A bill period the code does not parse gets the note 'The line states no date of service', which misdescribes the bill",
   "evidence": "probe_r2.out P10 'Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 ...' and N17 'Statement covers period June 28-July 2, 2026. Rev 0120 ...'. Both give the not-stated form (safe) with 'The line states no date of service.' (service_date.py:72).",
   "why_it_matters": "The bill does state a service period. Telling me it states none sends me hunting for a missing date, when I could confirm the stated period at a glance. UB-04 FL6 is labelled 'statement covers period'.",
   "fix": "Recognize 'from X to Y' after 'dates of service', and 'statement covers period'. When a period phrase is present but not parsed, use a note that names it ('The bill states a period (...) the code could not tie to this line').",
   "acceptance_test": "Fixtures P10 and N17 print 'January 23–March 6, 2026' and 'June 28–July 2, 2026', or give a note that quotes the period."},
  {"severity": "minor",
   "title": "Internal notes say nothing about charge lines printed without a service date (carried from T-200; the class is larger now)",
   "evidence": "letters/lib11-counted-notes.txt and letters/synth_ambiguous_dos-all_accepted-notes.txt: grep for 'service date' and 'Confirm the date' over every notes file in letters/ returns nothing. Meanwhile 3 lib11 letter lines and the synthetic line print '(statement dated ...; service date not stated)'.",
   "why_it_matters": "The notes are my to-do list before the demand goes out. A charge going to the adjuster without a date of service is the item I most need there, so I can request a dated itemized bill.",
   "fix": "Add a notes line per not-stated charge, under BILLS TO REQUEST or a new 'Charges without a date of service' heading: provider, amount, reason (the confirm_note), and 'request a dated itemized bill'.",
   "acceptance_test": "lib11 counted notes list the three Fennimoor lines with 'request a dated itemized bill'; the synthetic ambiguous-DOS notes list the $275.00 line with its reason."},
  {"severity": "minor",
   "title": "Carried from round 1: some charge quotes name neither the service nor the date the line prints",
   "evidence": "ui-lib14-letter.txt 'Source [Ex. __ / Bates __]: \"charge $187.05.\"'; ui-lib10-letter.txt 'Source [Ex. __ / Bates __]: \"FL47 total charges $4,920.00.\"'. The handoff lists this as not done. The quote span predates T-202.",
   "why_it_matters": "I cannot check the printed date against the quote under it. I have to open the record to see that $187.05 is mileage on the 09/14 run.",
   "fix": "Quote the bill line from its code or description through the figure.",
   "acceptance_test": "Every charge Source line in the 25-case letters contains a service word or code as well as the figure."}
 ],
 "whats_right": [
  "Both round 1 blockers fixed: Posted-first ledgers print the DOS column (T2, N1, N2, N24, N25), headerless two-date rows and the CMS-1500 'X and Y' list give the not-stated form with a specific note",
  "Corpus letters (sample, case_09, lib14, lib10) unchanged and right; lib10 'June 9–12, 2026' under the D-071 clarification; amounts[].service_date.text equals the letter text on all 10 charges",
  "letter_check now fails the round 1 wrong-date letters (posting date; one claim date on a two-date CMS-1500) and passes the right forms"
 ],
 "questions_for_chris": [
  "Which not-stated string binds: the amendment's '(service date not stated on this line; statement dated X)' or the T-200 form '(statement dated X; service date not stated)' the build prints?",
  "Outside T-202 (not graded here): in my SYNTHETIC two-date CMS-1500 variant the export gate blocks the coded lines ('Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’', letters_dump_r2.out). A CPT code before 'charge' is read as money, so a CMS-1500 coded line cannot be exported. Should this get its own card?"
 ]}
```
