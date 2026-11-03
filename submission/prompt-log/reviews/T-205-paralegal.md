# T-205 review — paralegal-reviewer (Maria Delgado)

Commit 203ac6a, fresh `git archive` in an empty scratch directory, demo mode (fixture backend, `ZLAYT_MODE=local`, health `demo_mode: true`) on port 7981. Listener PID 63090 stopped afterward (`lsof` exit 1, `curl` = 000). Private values seen: 0 (<redacted> count 0).

**Verdict: pass (2 minors, 1 nit).** The service date on the Step 3 charge card equals what the letter prints on all three cases. The statement date is labeled "statement dated" wherever a charge card shows one, with one gap on uncounted ledger lines.

- case_09: card "Date of service February 2, 2026 · statement dated March 1, 2026". Letter: "Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00". Match.
- lib10: all four charges show "Date of service June 9–12, 2026 · statement dated June 19, 2026". Letter prints "June 9–12, 2026" on each line. Match.
- lib11: ED line "Date of service March 18, 2026" (no statement label, correct for a dated visit note). Counted ledger lines show "(statement dated June 15, 2026; service date not stated)" in the Step 3 done list, on revisit, and in the letter. Match.
- Confirm note: the fixture set has no bill with a doubtful date, so no real note appeared on any of the three cases. I rendered all 7 backend reasons by rewriting only `service_date` in the GET case response (the worker's own method). The note shows in the card foot, in plain words, visible without scrolling at 1440x900, and says what the letter will do and what to do. Wording gaps are in the findings. Grade-only-the-display applies; T-202 r3 may change which lines are certain.

```json
{"card": "T-205", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 203ac6a (git archive extracted to session scratchpad a203/); app http://127.0.0.1:7981 demo mode (fixture backend, curated set, ZLAYT_MODE=local, health demo_mode true); case_09 (POST /api/cases with golden text, opened in UI), lib10 and lib11 (library tile). Display only; T-202 r3 parse changes not graded. Private values seen: 0.",
 "exercised": ["Read personas/paralegal.md, board show T-205 (handoff), D-071 and its amendment/clarification in memory/ORCHESTRATOR_DECISIONS.md:84-92, git show 203ac6a (step3.js/css diff)",
  "git archive 203ac6a into scratchpad a203; started server on 7981; health check demo_mode true; later killed PID 63090 and confirmed lsof exit 1 and curl 000",
  "artifacts/review-evidence/T-205-paralegal/p01.py via h.py: for case_09, lib10, lib11 did Step 2 by keyboard, walked every Step 3 card (DOM probe of service-date-text, statement-date, confirm-note, card text), counted charges, Step 4 download of letter and notes; output p01.out, letters ui-*-letter.txt, ui-*-notes.txt",
  "api.py / api.out: GET /api/cases/{token} amounts[].service_date for all three cases next to the record date",
  "p02_notes.py / p02.out: all 7 confirm_note reasons rendered on case_09 a1 and lib10 a2 with service_date stubbed in the GET response (fixtures have no real doubtful-date bill); measured note position vs viewport; screenshots note-lib10-ambiguous_numeric.png, note-lib10-no_date.png",
  "p03_revisit.py / p03.out: revisited counted lib11 a2 and a1; screenshots lib11-revisit-a2.png, lib11-s3-01-a2.png (pre-count card)",
  "Compared Step 3 date text with letter lines by grep (case_09 line 21, lib10 lines 37-44, lib11 lines 37-44); console/http errors: none (ERRORS count 0 in p01/p02/p03 outputs)"],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "step3_date_matches_letter": 5, "statement_date_labeled": 4, "confirm_note_plain_and_actionable": 3},
 "findings": [
  {"severity": "minor", "title": "Uncounted lib11 ledger lines show the statement date bare, with no Date of service line and no 'statement dated' label",
   "evidence": "p01.out:200 (PROBE lib11 a2): card 'Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 / $250.00 / The line states no date of service...', svc null; same for a3, a4. Screenshot artifacts/review-evidence/T-205-paralegal/lib11-s3-01-a2.png (card head and source head read 'June 15, 2026'). After counting, the same line reads 'statement dated June 15, 2026' (p03.out:2, lib11-revisit-a2.png) and the letter prints '(statement dated June 15, 2026; service date not stated)' (ui-lib11-letter.txt:39). sdOf in app/frontend/guided/step3.js requires kind === 'charge', and an uncounted ledger line is kind unclear, so service_date is null (api.out lib11 a5 shows the same for unclear rows).",
   "why_it_matters": "Those are the lines I am most careful with. Before I count them the card shows a bare June 15, 2026 in two places, which reads like a date of service, and it differs from what the letter will print. The body sentence says no date of service, so the risk is low, but the label I was asked to check is missing on this state. Never-counted UB-04 and ledger cards (lib10 a1/a6, lib11 a5-a8) show a bare record date too, though those carry no service-date claim.",
   "fix": "Apply the same 'statement dated X' wording to the card head, source head and sub for any amount whose record is a bill document (ledger, invoice, UB-04, billing statement), whatever its kind, and show the letter's not-stated text as the Date of service line on a countable ledger line before it is counted.",
   "acceptance_test": "E2E on lib11 a2 before counting: card head and src-head contain 'statement dated June 15, 2026', no bare 'June 15, 2026' without that prefix; the card shows '(statement dated June 15, 2026; service date not stated)' and it equals the text the letter prints after counting."},
  {"severity": "minor", "title": "The confirm note says to confirm the date but gives me nowhere to use it",
   "evidence": "p02.out:2 (and 16 variants): note text ends 'The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.' The card offers only 'Yes, count it' / 'No, don't count it' / 'Decide later'; screenshot note-lib10-ambiguous_numeric.png. The note does not say what to do once I have confirmed: add the date by hand in the Word letter, ask for the bill, or just count it.",
   "why_it_matters": "Plain wording and placement are good, but the instruction is half of one: I confirm the date from the highlighted words, and then the tool cannot take it and the letter still prints none. I need one sentence of next step so I do not guess.",
   "fix": "Append the next step to confirm_note, e.g. 'Counting the charge keeps it in the total; type the date into your letter yourself, or request the itemized bill.' Or tell me this tool cannot record a confirmed date.",
   "acceptance_test": "Unit test on service_date.confirm_note for all 7 reasons: each ends with a sentence naming the next action (not just 'confirm'); E2E asserts the foot note shows it beside the quote."},
  {"severity": "nit", "title": "Two notes say 'the code' to a paralegal",
   "evidence": "p02.out:3-4: 'The date 04/05/26 has a two-digit year, which the code does not guess.' and 'The date April 5 states no year, which the code does not borrow from the statement.' (app/backend/service_date.py _WHY).",
   "why_it_matters": "I do not know which code is meant; 'the tool' or no subject reads the same and is clearer.",
   "fix": "Reword: 'a two-digit year, which is not guessed' / 'no year, which is not taken from the statement date'.",
   "acceptance_test": "Unit test: no confirm_note contains the word 'code'."}
 ],
 "whats_right": ["Date of service on the Step 3 card is the letter's own text on case_09, lib10 and lib11 (period 'June 9–12, 2026' kept as a range), and the done-list column is now 'Date of service'.",
  "'statement dated March 1, 2026' / 'June 19, 2026' is named as a statement date in the card head, the Date of service line and the source head; the ED visit date is left unlabeled, correctly.",
  "The note sits in the card foot under the highlighted quote, is visible without scrolling, keeps Yes/No enabled, and states the letter will print no date."],
 "questions_for_chris": []}
```
