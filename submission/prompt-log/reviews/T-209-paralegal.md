# T-209 review — paralegal-reviewer (Maria Delgado persona)

Scope: commit 88c73dd (Step 3 `confirmNext` in `app/frontend/guided/step3.js:36`, and `tests/e2e/guided/test_t206.py:66`). HEAD is 88c73dd. Letter wording checked at HEAD in `app/backend/export.py:218` and `app/backend/service_date.py:76, 83`. The app was driven as commit 88c73dd exported to a scratch tree and served on 127.0.0.1:7893. I did not use localhost:7860 (see questions). Synthetic data only.

Verdict: **changes**. No blocker. Four majors and three minors. The new sentence now names the exact blank the letter prints. It also gives one instruction that the highlighted words cannot satisfy for lines with no service date, and it contradicts the note above it on that card.

What the letter shows (verified, not from the card copy). A counted ledger line at HEAD prints:
`Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00`
with the total line `Billed charges accepted from these records: $250.00`. The note never mentions the parenthetical or the line's effect on the total.

Findings in short:
1. major: for a no-date line, the note says "fill the blank from the record" and the sentence says "fill in from the highlighted words". The highlighted words contain no service date.
2. major (pre-existing at HEAD, outside the 88c73dd diff): a labeled DOS followed by a dotted leader ("99213 ... $250.00") resolves to "The line states no date of service."
3. minor: the note omits "(statement dated X)" and never says the statement date is not the service date.
4. minor: counting consequences are not stated; the "added to the bill total" line is suppressed on these items.
5. minor: the sentence's last clause is clipped in its scroll box at 1280x900.
6. minor (pre-existing, same card): the card reads "Date of service date of service [__________]".
7. minor: 0 of 16 curated cases reach this sentence; the AC evidence relies on injected backend output.

---

```json
{"card": "T-209", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 88c73dd (app/frontend/guided/step3.js:31-36,59,63; tests/e2e/guided/test_t206.py:66); HEAD 88c73dd; letter wording at HEAD app/backend/export.py:218-230 and app/backend/service_date.py:76-83; app served from git archive of 88c73dd at http://127.0.0.1:7893 (LLM_BACKEND=fixture, FIXTURE_SET=curated, local mode); sample cases from the curated library (lib10, lib11, and 15 other library cases plus the sample)",
 "exercised": [
  "Read personas/paralegal.md in full; board.py show T-209 (AC 1 claims guided e2e 143 passed, not re-run by me)",
  "git show 88c73dd -- app/frontend/guided/step3.js tests/e2e/guided/test_t206.py (2 lines changed in step3.js, 1 assertion in test_t206.py)",
  "git show 88c73dd:app/frontend/guided/step3.js | sed -n '28,40p' and lines 31-36, 59, 63 (dateLine, confirmNote, confirmNext, the foot branch that suppresses the bill-total line)",
  "git grep -n 'date of service \\[' HEAD -- app/ tests/ (export.py:218, service_date.py:18,76,81, test_t200 and test_t202 assertions)",
  "curl http://localhost:7860/api/cases POST -> 404 (listener PID 22647 is a stale process; the RUNBOOK URL could not load a case); started my own 88c73dd server on 127.0.0.1:7893 from git archive",
  "artifacts/review-evidence/T-209-paralegal-probe.py -> T-209-paralegal-probe.json (5 bill libraries: 0 charges with a not-certain date and a note)",
  "artifacts/review-evidence/T-209-paralegal-reach-scan.py -> T-209-paralegal-reach-scan.json (16 cases loaded through the API: 0 charges with confirm_note)",
  "artifacts/review-evidence/T-209-paralegal-note-probe.py -> T-209-paralegal-note-probe.json (store.charge_service_date at 88c73dd on three bill lines: no-date, birth-date-only, labeled ambiguous)",
  "Resolver variant checks (SD.resolve at 88c73dd, scratch scripts): 'DOS 04/05/2026 Office visit 99213 $250.00' -> ambiguous_numeric; same with ' ... ' before $250.00 -> no_date (verbatim outputs quoted in finding 2)",
  "Counted the no-date ledger line a2 of case_lib11 through POST /api/cases/{tok}/items/a2/review (count), then GET /api/cases/{tok}/export; read letter_text and the total line",
  "artifacts/review-evidence/T-209-paralegal-step3-walk.py (Chromium, lib10 a2 with two backend-computed outcomes injected) -> T-209-step3-walk.json and screenshots T-209-step3-A_no_date_of_service.png and T-209-step3-B_labeled_ambiguous_dos.png; read the screenshot of A; did not press Yes or No",
  "artifacts/review-evidence/T-209-paralegal-foot-clip.py -> T-209-paralegal-foot-clip.json, screenshot T-209-step3-foot-desktop_1280x900.png (clip measurement); phone_390x844 measured too",
  "Walked the card with the real confirm-note wording and the real answer labels: 'Yes, count it' / 'No, don't count it' match the rendered buttons"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "note_says_what_letter_shows": 3, "note_says_what_to_do": 2, "statement_date_kept_out_of_dos": 3},
 "findings": [
  {"severity": "major",
   "title": "For a line with no service date, the sentence tells her to fill the blank from the highlighted words, which contain no service date, and contradicts the note above it",
   "evidence": "Card at 88c73dd, scenario A (T-209-step3-walk.json, key A_no_date_of_service). confirm_note: 'The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated line-by-line bill, or fill the blank from the record, before you rely on it.' confirm_next: 'What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, the letter shows a blank date of service [__________] for you to fill in from the highlighted words.' Backend pairing with a quote that has no DOS: T-209-paralegal-note-probe.json, case 1_birth_date_only_ledger_line, reason no_date, excerpt 'Fennimoor Spine Clinic itemized ledger. Office visit, established patient, 99213 ... $250.00'. The sentence is static (step3.js:36) and does not branch on sd.reason. Screenshot: T-209-step3-A_no_date_of_service.png.",
   "why_it_matters": "On a no-date line the highlighted words give her no date to copy. The box tells her two things: request a bill or fill from the record, and fill from the highlighted words. A paralegal who follows the second can copy a birth, injury or statement date into the date-of-service blank. That is the adjuster-catches-a-wrong-date case in the persona's bad day. The service_date.py design says the paralegal fills the blank from the quote, and nothing is inferred; for these lines the quote has nothing to fill from.",
   "fix": "Branch the sentence on sd.reason in step3.js. For written-date reasons (ambiguous_numeric, two_digit_year, no_year, invalid, several_dates, implausible): 'If you count it, the letter shows a blank date of service [__________] (statement dated X). Fill the blank with the date the highlighted words label as the date of service.' For no_date and non_service_date: 'The highlighted words give no date of service. Do not use any date from the record for the blank. Request a dated bill, or fill it from the record, before you count it.' Keep the button names.",
   "acceptance_test": "Unit: confirmNext(sd) for reason no_date contains no 'fill in from the highlighted words' and contains 'Request a dated bill'; for reason ambiguous_numeric it contains 'the date the highlighted words label as the date of service'. E2E (real backend output, no route rewrite for the reason): a no-date bill line shows no sentence that tells her to fill from the highlighted words, and the note and the sentence give the same instruction."},
  {"severity": "major",
   "title": "A labeled date of service followed by a dotted leader is read as no date, so the note says the line states no date of service (pre-existing at HEAD, outside the 88c73dd diff)",
   "evidence": "SD.resolve at 88c73dd, source 'Fennimoor Spine Clinic, itemized ledger', date 2026-06-15: 'Fennimoor Spine Clinic itemized ledger. DOS 04/05/2026 Office visit 99213 $250.00' -> ambiguous_numeric, raw '04/05/2026'. The same line with '99213 ... $250.00' -> no_date, raw ''. The note then reads 'The line states no date of service.' Also 'Date of service 04/05/2026 Office visit 99213 $250.00' -> ambiguous_numeric. Outputs printed from the scratch resolver run; the leader variant is my constructed line, not a fixture record (the curated set has no leader lines). Screen-level: the card would show that note above a quote that contains 'DOS 04/05/2026'.",
   "why_it_matters": "service_date.py:19 promises the letter never says 'service date not stated' above a quote that states one. The note here says the same thing in a different form. The paralegal would believe the record has no date of service and could request a bill she does not need. The letter output is not wrong (the blank prints), so this is a misleading explanation, not a wrong date in the letter. Itemized ledgers with dot leaders are common, so this is not a rare edge.",
   "fix": "In service_date.resolve, allow a dotted leader (runs of '.' or '…' with spaces) between the label and the amount when building the clause, or stop splitting segments at '...'. Route to the T-202 owner (service_date.py), not the T-209 frontend card. Add the leader case to the resolver tests.",
   "acceptance_test": "Unit: resolve('Fennimoor Spine Clinic itemized ledger. DOS 04/05/2026 Office visit 99213 ... $250.00', pos of $250.00, 'Fennimoor Spine Clinic, itemized ledger', '2026-06-15') returns reason ambiguous_numeric with raw '04/05/2026'. Same string without the leader returns the same result."},
  {"severity": "minor",
   "title": "The note does not describe the letter text: the letter prints '(statement dated June 15, 2026)' after the blank, and nothing says that statement date is not the service date",
   "evidence": "Letter at HEAD, counted line a2 of case_lib11 via /api/cases/{tok}/export letter_text: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00'. Card line (T-209-step3-walk.json, service_date_line): 'Date of service date of service [__________] (statement dated June 15, 2026)'. confirmNext says only 'a blank date of service [__________]'. export.py:218 says the statement date is never printed as the date bare; the sentence does not say it.",
   "why_it_matters": "The clause she has to copy into the letter is not the clause the sentence names. The parenthetical is the statement date, which the design is built to keep out of the date-of-service slot. She may keep it, or read the blank as already filled with the statement date.",
   "fix": "Name the full printed text in confirmNext, and say that the date in parentheses is the statement's date and is not the service date. Example: 'The letter shows date of service [__________] (statement dated X). The date in brackets is the statement date, not the service date. Fill only the blank.'",
   "acceptance_test": "E2E: the confirm-next text contains '(statement dated' and 'is not the service date' for a not-stated line whose sd.statement_date_iso is set; test_t206.py:66 asserts this sentence."},
  {"severity": "minor",
   "title": "Counting consequences are not stated: a doubtful-date line loses the 'added to the bill total' line, and the note never says what counting or not counting does to the letter total",
   "evidence": "step3.js:59 at 88c73dd: `else if (!(sd && sd.confirm_note)) foot.push(\"If you count it, it's added to the bill total in the letter, with the highlighted words as its source.\");` The confirm branch (step3.js:63) drops that line when confirm_note is set. The counted blank line in the letter total at HEAD: 'Billed charges accepted from these records: $250.00' (counted a2 of case_lib11, export letter_text). The question on the card reads 'Should this charge count toward the bill total?' and the sentence never says a counted blank line adds its amount to that total, or that 'No, don't count it' leaves it out of the letter.",
   "why_it_matters": "The persona needs to know what each answer does to the letter total before she answers. The total then carries a $250 line whose date of service is still a blank. That is the reconciliation question she will be asked on the adjuster call.",
   "fix": "Add to confirmNext: 'If you count it, its amount is added to the billed total with the blank date. If you do not count it, it is left out of the letter.'",
   "acceptance_test": "E2E: for a doubtful-date line the foot states that counting adds the amount to the billed total, and that not counting leaves it out of the letter."},
  {"severity": "minor",
   "title": "The sentence's last clause is cut off in its scroll box at a 1280x900 desktop",
   "evidence": "T-209-paralegal-foot-clip.json, desktop_1280x900: clippingAncestors [{tag DIV, cls 'card-f attn', overflowY auto, clientHeight 149, scrollHeight 174}]; sentence top 649, bottom 721. Screenshot T-209-step3-foot-desktop_1280x900.png and T-209-step3-A_no_date_of_service.png show 'What to do: ... If you count it, the letter shows a blank / date of service [__________] for you to fill in from the highlighted words' cut mid-line at the box edge. Phone 390x844: the card section scrolls (clientHeight 292, scrollHeight 455).",
   "why_it_matters": "The clause that tells her what the letter will show is the one that is cut. She must scroll inside the foot to read it. The Yes and No buttons stay visible, so she can answer without reading the clause.",
   "fix": "Let the foot grow to fit the note and the sentence at 1280x900 (no inner scroll for the confirm block), or move the sentence above the note's second paragraph so the clipped part is the least important text.",
   "acceptance_test": "E2E at 1280x900: confirm-next's bounding box lies inside the card-foot's client rectangle (scrollHeight <= clientHeight), with the 'for you to fill in from the highlighted words' text visible without scrolling the foot."},
  {"severity": "minor",
   "title": "The card's date line reads 'Date of service date of service [__________]' (pre-existing, same card as the note)",
   "evidence": "step3.js:31-33 at 88c73dd: the label h('span', {class:'label-cap'}, 'Date of service') followed by sd.text, which already starts with 'date of service [__________]' (service_date.py:76, 81). Walk output (T-209-step3-walk.json, service_date_line, both scenarios): 'Date of service date of service [__________] (statement dated June 15, 2026)'. Screenshot T-209-step3-A_no_date_of_service.png shows the doubled label.",
   "why_it_matters": "The paralegal reads the line she is about to fill. The doubled label looks like a rendering bug and weakens trust in the card. It is not a letter error: the letter line reads once.",
   "fix": "Show the label once. Either drop the 'Date of service' span when sd.text starts with 'date of service', or strip the prefix from sd.text for the card.",
   "acceptance_test": "E2E: service-date text on a not-stated line contains 'date of service' exactly once."},
  {"severity": "minor",
   "title": "No curated case reaches this sentence; its acceptance evidence relies on injected backend output",
   "evidence": "T-209-paralegal-reach-scan.json: loaded 16 cases; charges_with_confirm_note 0; not_certain_without_note 0. The guided tests (test_t206.py:55-66, test_t205.py:107-135) inject the sd with a route rewrite ('the fixture set has no bill that parses to a doubtful date'). The card AC cites 'guided e2e ... 143 passed' for that injected case.",
   "why_it_matters": "The demo paralegal will never see this sentence on the curated set. The wording was checked only against text the test author wrote. The first real doubtful date will show it to someone who has not seen it on a real record.",
   "fix": "Add one curated bill line with a doubtful written date (for example 'DOS 04/05/2026' with no year ambiguity resolved) so the sentence is shown by the real backend once. Keep the injected test as the wording check.",
   "acceptance_test": "Reach scan: at least one charge in the curated set has a confirm_note, and the card shows confirm-next for it."}
 ],
 "whats_right": [
  "The sentence names the blank the letter prints ('date of service [__________]'), matching service_date.py:76 and the counted letter line at HEAD.",
  "The 'type the date into your letter yourself' instruction is gone, and the named buttons 'Yes, count it' and 'No, don't count it' match the rendered answer buttons.",
  "The change is two lines in one file plus one assertion; the card does not invent a date and the letter wording is unchanged."
 ],
 "questions_for_chris": [
  "This review ran on claude-haiku-5-5 (the model this session runs as), not the expected claude-opus-5-5 in the persona file, and CLAUDE.md section 6 puts judgment reviewers on Opus. Should this review count toward the T-209 gate, or be rerun on Opus?",
  "localhost:7860 (RUNBOOK) is a stale listener here: POST /api/cases returns 404 (PID 22647, cwd /Users/arsis/zlayt-pm-project). I drove 88c73dd from a scratch export on 127.0.0.1:7893 instead. Restart 7860 with ./tools/serve_app.sh before the next review round?",
  "Is the finding-2 resolver gap (dotted leader) in scope for T-202 or for a new card? It is outside the 88c73dd diff."
 ]}
```
