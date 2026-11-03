# T-202 round 6 (D-073 round-6 rules): paralegal review (Maria Delgado, senior PI litigation paralegal)

**Verdict: fail.** The bar for this round: no charge line ever prints a wrong date of service. Round 6 does not meet it.

**What round 6 fixed.** The round 5 findings are closed in the full pipeline:
- Provider names. "Austin MRI", "Open MRI of Austin", "Hobbleton Follow-Up Clinic", "Hobbleton X-Ray", "Hobbleton Hand Evaluation Center" and "Express Exam Urgent Care" bills now print the blank.
- The "Date of service: 02/02/2026  Account: 4471" line over a row, and the brief's "Date of service: X" line over a "Date posted" table, now print the blank.
- A "Visit date" column over a "Next visit" column prints the visit date, in either column order.
- Blank labels. On the 25-case corpus, all 74 blanks carry the right label: 16 "statement dated" lines, all on bills, and 58 "record dated" lines, all on ED, urgent-care, imaging, radiology or chiropractic records.
- The 5 dated corpus lines (the sample ER line and the four lib10 UB-04 lines) are correct. They are the same lines as on f9c0faf.
- The sample, case_09, lib14, lib10 and lib11 letters I generated in the UI are all correct.

**What still prints a wrong date.** The second date source is the encounter record's own date. It is lent to any charge in an identified visit note whose own sentence holds none of the guard words: earlier, previous, prior, next, last, later, ago, former, subsequent, a month-year, or a visit count. Charges in a visit note for another time pass straight through:
- "Initial evaluation 97161 charge $250.00." in the visit-9 PT note prints March 6. Record 4 dates the initial evaluation January 23.
- "Patient went to urgent care yesterday, urgent care visit charge $310.00." prints January 16.
- "ER facility charge $6,240.00." in the PCP office visit note prints January 16.
- A late entry dated 01/20 "for the visit of 01/16/2026" prints January 20.
- The sample ER summary with "Arrived 01/09/2026 ... Discharged 01/10/2026" prints January 10.

For every one of these, letter_check accepts the wrong line and rejects both the blank and the true date.

One source (1) shape is also wrong. A UB-04 coded line that states its own "service date 02/05/2026" prints the statement period "February 9–12, 2026", with that quote directly under it.

The ER overnight shape was already in my round 4 probe set (r4 T3). It printed January 10 in my round 5 run as well (r5 probe_r5.out:669), and I counted it as correct there. That was my miss.

D-073 pre-declares the outcome: "If round 6 still prints a wrong date, the MVP letter prints the fillable blank on every charge line (no date extraction at all) and SCOPE_CUTS 28 covers it."

**Usability (brief).** A letter of blanks works for a demand. Filling a date is the same job as filling the Bates placeholders. Now that the label reads "(record dated March 18, 2026)" on an ED record, I can fill most blanks from the date printed next to them. The internal notes still tell me to "fill it from the quote" when the quote has no date, while Step 3 says "Take the date from the matching visit note". A dated line from a visit note still has to be opened, because the eval protects a wrong one. `verify_quickly` is 3.

**Scope.** I extracted `git archive 9655f1d` (tree 823f8e2e8d56) to the session scratchpad and served it in demo mode on 127.0.0.1:7986: fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local. /api/health returned demo_mode true and local_mode true. I stopped listener PID 94928 afterwards (lsof exit 1, curl 000).

HEAD moved to 6be191f during the review. `git diff --stat 9655f1d HEAD -- app/backend app/llm app/frontend evals/letter_check.py` is empty.

The adversarial texts ran in-process through `evals.letter_check.letters_for`, which is the export path, because demo mode refuses unrecorded text. Private values seen: 0. Per the brief, the Step 3 header ("statement dated" on record blanks) belongs to another card and is not graded here.

```json
{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "commits b72acb9, 3654cf9, 756546b, 9655f1d (git archive 9655f1d, tree 823f8e2e8d56, extracted to the session scratchpad pr6_9655f1d/); served in demo mode (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local; /api/health demo_mode true, local_mode true) at http://127.0.0.1:7986; listener PID 94928 stopped (lsof exit 1, curl 000). Parent f9c0faf archive (pr6_f9c0faf/) run in-process for the corpus diff. HEAD moved to 6be191f during the review; git diff --stat 9655f1d HEAD -- app/backend app/llm app/frontend evals/letter_check.py is empty. Cases: sample, case_09 (POST /api/cases with the golden text, opened in the UI), lib14, lib10, lib11 in the UI; all 25 letter_check cases in-process; SYNTHETIC variants in-process (demo mode refuses unrecorded text). Step 3 header wording excluded per the brief (another card). Evidence: artifacts/review-evidence/T-202-paralegal-r6/. Private values seen: 0.",
 "exercised": [
  "Read personas/paralegal.md, D-073 and its round-6 rules (memory/ORCHESTRATOR_DECISIONS.md:97-100), memory/SCOPE_CUTS.md:113 (row 28), reviews/T-202-paralegal-r5.md, board.py show T-202 (r6 notes and the handoff with its 84-line corpus diff), service_date.py, store.charge_service_date and encounter_types.json at 9655f1d",
  "From the archive: pytest test_t202_r6_d073 + r5 + r4 + r3 + r2 layouts + test_t202_charge_service_dates + test_t200_undated_charge_label + test_export: '913 passed in 10.78s' (pytest-t202.out); python -m evals.letter_check: value 0 over 25 cases (letter_check.out)",
  "probe_r6.py: all 162 round 1-5 texts loaded by ast from my earlier probe files (r1 probe_dates/probe_dates2, r2, r3, r4 NEW, r5 NEW incl. the MRI/X-Ray/Follow-Up/Evaluation/Exam provider names, the key-value DOS line over a row, Visit Date/Next Visit Date) plus 31 round 6 shapes (A1-A20 charges in whole-phrase visit notes for another time, B1-B9 bill tables incl. the brief's 'Date of service: X' over 'Date posted' and 'Visit date' over 'Next visit', U1-U2 UB-04), through store.charge_service_date; every STATED result checked by hand (probe_r6.out)",
  "fullpipe_r6.py: 30 shapes (28 in fullpipe_r6.out, a15 and u1 in fullpipe_r6_a15_u1.out) through the full pipeline and letter (round 6 A-shapes, the r5 m1-m2/c1-c4 provider-name bills, t4/t4b key-value DOS lines, t5/t5b visit/next-visit tables, t1 control) with letter_check on each (fullpipe_r6.out, fullpipe_r6_a15_u1.out); fullpipe_lib10.py (an added charge in lib10 record 3 did not reach the letter: fullpipe_lib10.out)",
  "eval_teeth_r6.py: letter_check on the build's line vs the blank and the true date for A2, A5, A6b, A10; blank label on six records whose label or excerpt opening holds a money word (eval_teeth_r6.out)",
  "corpus_blanks.py on 9655f1d and f9c0faf: every BILLED CHARGES line of the 25 cases, all_accepted and counted (corpus_blanks_*.out, corpus_blanks.diff): 37 all_accepted lines, 32 blank and 5 dated on 9655f1d; the 5 dated lines are unchanged from f9c0faf; 74 blank labels checked against record type",
  "Playwright on the running archive (h.py + p01_cases.py): sample, case_09, lib14, lib10, lib11 keyboard-first through Steps 1-4, every Step 3 card logged and screenshotted, letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt, p01.out); drafting took 2.3-2.5 s per case"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 3, "letter_dates_correct_on_corpus": 5, "adversarial_dates_correct": 3, "blank_label_correct": 4},
 "findings": [
  {"severity": "blocker",
   "title": "A visit note's own date is printed as the date of service of a charge the note itself places at another time (initial evaluation, first visit, yesterday, the ER, the day of the collision, February, a late entry, an overnight ER stay, a course total); letter_check accepts only the wrong line",
   "evidence": "fullpipe_r6.out (sample with one SYNTHETIC record added or record 6 replaced; full pipeline, every item accepted): a2 PT note 03/06 -> 'Capital PT, physical therapy note, March 6, 2026: $250.00 | Initial evaluation 97161 charge $250.00.' (record 4 dates the initial evaluation 2026-01-23); a3 'First visit charge $250.00.' -> March 6; a10 PCP note 01/16 -> 'Dr. Alvarez, office visit note, January 16, 2026: $310.00 | Patient went to urgent care yesterday, urgent care visit charge $310.00.'; a1 -> 'Dr. Alvarez, office visit note, January 16, 2026: $6,240.00 | ER facility charge $6,240.00.'; a16 'Original ER charge $6,240.00 reviewed with patient.' -> January 16; a11 'Ambulance transport on the day of the collision, charge $1,380.00.' -> January 16; a12 note 03/05 'February follow-up visit 99213 charge $150.00.' -> March 5; a20 MRI report 05/29 'ER x-ray charge $240.00.' -> May 29; a5 note dated 01/20 'Late entry for the visit of 01/16/2026. Office visit 99213 charge $150.00.' -> January 20; a6b the sample ER summary dated 01/10 with 'Arrived 01/09/2026 by EMS. Discharged 01/10/2026.' -> 'Central ER discharge summary, January 10, 2026: $6,240.00'; a7 'Physical therapy charges: $1,665.' -> March 6. Every one: 'date violations: []'. eval_teeth_r6.out (A2, A5, A6b, A10): the build's line -> []; the blank -> 'the line prints a blank above a source that gives its date'; the true date -> 'the line prints a date no source ties to it'. probe_r6.out: r4 T3 (my round 4 probe, same as a6b) prints January 10; it printed the same in my round 5 run (r5 probe_r5.out:669), and I did not flag it there. Cause: service_date.py:447 gives the record date unless the charge's own segment matches _MULTI (:374), _OTHER_TIME (:87; earlier, previous, prior, next, last, later, ago, former, subsequent) or a month-year; a previous sentence is never read (a5, a6b). evals/letter_check.py:264 uses the same word list, so it shares the blind spot. Controls print correctly: a17 ER record 'ER facility charge' -> January 9; a18 PT note 'Discharge visit 97110 charge $185.00.' -> March 6.",
   "why_it_matters": "This is the bar for this round, and §5 of my dossier: a date in the letter that the record contradicts. The adjuster will compare the PT initial-evaluation charge with the PT ledger and find January 23, not March 6. The ER overnight shape is common: an ER visit that crosses midnight, with its summary dated the discharge day. There it prints January 10 against an EMS run and accident date of January 9, which creates a date conflict that is not in the records. The quote printed under each line holds no date, so checking the quote does not catch it. The eval rejects both the blank and the true date, so a careful fix would be pushed back.",
   "fix": "Apply the outcome D-073 pre-declares for a round-6 failure: every charge line prints the fillable blank '(record dated X)' / '(statement dated X)', no date extraction, and SCOPE_CUTS 28 covers it. letter_check then accepts the blank and nothing else on every charge line. On the corpus this moves 5 of 37 lines (the sample ER line and the four lib10 UB-04 lines) to blanks with correct labels.",
   "acceptance_test": "fullpipe_r6.py a1, a2, a3, a5, a6b, a7, a10, a11, a12, a16, a20 and u1 each print '<source>, date of service [__________] (record dated ...)' or '(statement dated ...)'. letter_check reports a violation on 'Capital PT, physical therapy note, March 6, 2026: $250.00' and accepts the blank. The corpus has 0 dated charge lines and 74 blanks with unchanged labels."},
  {"severity": "blocker",
   "title": "A UB-04 statement period is printed over a coded line that states its own, different service date (rule 3: the UB-04 period gets the same several-dates guard)",
   "evidence": "fullpipe_r6_a15_u1.out u1 (case_09 record 2 replaced by 'Saltmarrow General Hospital, UB-04', excerpt 'UB-04. Statement covers period 02/09/2026 through 02/12/2026. Rev 0450 99285 emergency room, service date 02/05/2026, FL47 total charges $2,105.00.') -> 'Saltmarrow General Hospital, UB-04, February 9–12, 2026: $2,105.00 | Rev 0450 99285 emergency room, service date 02/05/2026, FL47 total charges $2,105.00.', date violations: []. probe_r6.out U1 gives the same at the resolver (06/05 line date, June 9–12 printed). Cause: service_date.py:427 blanks the span only for _OTHER_TIME words in the span's sentence; a second candidate date in the charge's own line is not checked.",
   "why_it_matters": "The head of the line says February 9–12 and the quote directly under it says 02/05. This bill contradicts itself, and the tool picks one reading silently. That is the case my dossier treats as a dealbreaker for the accident dates. The adjuster sees the mismatch on the face of the letter.",
   "fix": "Covered by the D-073 final step above. If source (1) is kept, a coded line whose own sentence holds any date gets the blank, the same guard as the encounter sentence.",
   "acceptance_test": "fullpipe_r6.py u1 prints 'Saltmarrow General Hospital, UB-04, date of service [__________] (statement dated March 1, 2026)'; letter_check flags 'February 9–12, 2026' for it."},
  {"severity": "major",
   "title": "The blank says '(statement dated X)' on clinical records whose excerpt opens with a money word or whose label carries one (rule 4)",
   "evidence": "eval_teeth_r6.out part 2: L1 'Central ER discharge summary', excerpt 'ER charges: $6,240. Dx: cervical strain. CT head negative.' -> kind=bill, '... date of service [__________] (statement dated January 9, 2026)'; L2 'Dr. Alvarez, office visit note', 'Copay collected $40. Persistent neck pain 6/10. ...' -> statement dated; L3 'Capital PT, physical therapy note', 'Payment plan discussed. ...' -> statement dated; L4 'Central ER, emergency department record, account 4471' -> statement dated. Cause: service_date.py:50-51 calls a record a bill when the first 40 characters of the excerpt (cut at the first colon or full stop) or the label match the financial list, before the whole document-type phrase is looked at. Corpus: 0 of 74 blanks mislabelled (corpus_blanks_9655f1d.out).",
   "why_it_matters": "If I fill the blank and keep the parenthetical, the letter tells the adjuster that an ER discharge summary is a statement. The record says no such thing, and it invites a request for a statement that does not exist. It is rated major, not blocker, because the date in parentheses is still the record's own date and no corpus line is affected. The same shape was a round 4 minor ('ER charges:' opening).",
   "fix": "Let a whole document-type phrase in the source label (discharge summary, office visit note, physical therapy note, emergency department record) outrank money words in the excerpt opening and in the rest of the label. Use the opening only when the label has no document-type phrase.",
   "acceptance_test": "eval_teeth_r6.py L1-L4 print '(record dated ...)'; L5 (no document type, opens 'Charges:') and L6 (billing statement) keep '(statement dated ...)'; the corpus labels are unchanged."},
  {"severity": "minor",
   "title": "Carried from rounds 3-5: the internal notes say 'fill it from the quote' for quotes with no date, while Step 3 says 'Take the date from the matching visit note'",
   "evidence": "ui-sample-notes.txt:36 '- Austin Imaging, $2,150: The line states no date of service the code can read ... fill it from the quote or request a dated itemized bill from the provider.' The quote is 'Charge: $2,150.' (ui-sample-letter.txt). ui-lib11-notes.txt:39-42 say the same for 'ED charge: $3,260.' and the Fennimoor ledger lines. p01.out [sample] s3 item=a4: 'Take the date from the matching visit note, or request a dated line-by-line bill, and fill the blank'.",
   "why_it_matters": "The notes and the screen give different instructions for the same line, and there is nothing in the quote to fill from.",
   "fix": "Use the Step 3 sentence (service_date.py _ASK_NONE) in the notes for the no-date reasons.",
   "acceptance_test": "No notes line says 'fill it from the quote' when the quote has no date."},
  {"severity": "minor",
   "title": "Carried from rounds 3-5: one single-date blank covers a 14-visit charge, and some quotes are only the figure",
   "evidence": "ui-lib11-letter.txt: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $2,310.00' over 'treatment visits 1 through 14 charge $2,310.00'. ui-lib14-letter.txt: 'Source [Ex. __ / Bates __]: \"charge $187.05.\"'; ui-sample-letter.txt: 'Source [Ex. __ / Bates __]: \"Charge: $2,150.\"'.",
   "why_it_matters": "A 14-visit charge needs a range. A bare-figure quote does not tell the adjuster what was billed.",
   "fix": "Print 'dates of service [__________]' when the quote counts visits. Quote the bill line from its code or description through the figure.",
   "acceptance_test": "The lib11 $2,310.00 line reads 'dates of service [__________]'. The lib14 $187.05 quote names its service."}
 ],
 "whats_right": [
  "Provider names no longer lend dates: Austin MRI, Open MRI of Austin, Follow-Up Clinic, X-Ray, Evaluation Center, Exam Urgent Care bills all print the blank with '(record dated ...)' (fullpipe_r6.out m1-m2, c1-c4).",
  "Real-table rule holds: 'Date of service: X' key-value lines over rows or a 'Date posted' table give the blank; 'Visit date' beside 'Next visit' prints the visit date in either column order (t4, t4b, t5, t5b, B1-B9).",
  "Corpus labels are right: 16 'statement dated' all on bills, 58 'record dated' all on ED/UC/imaging/chiro records; the 5 dated lines are correct and unchanged; sample total $8,390.00."
 ],
 "questions_for_chris": []}
```
