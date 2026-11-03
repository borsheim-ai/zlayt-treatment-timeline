# T-181 guided 4-step UI, round 2 (9ab8cae): paralegal re-review (Maria Delgado, senior PI paralegal)

**Verdict: changes** (0 blockers, 1 major, 3 minors, 1 nit).

**Scope.** `git archive 9ab8cae` was extracted to the session scratchpad and run with the fixture backend (curated set, no live calls):
- Public demo mode (ZLAYT_MODE unset): port 7941, listener PID 14948.
- Local copy for the lib11 library case: port 7942, PID 15071.
- I stopped both by PID afterwards. `lsof` returned 1 on both ports and `curl` returned 000.

**Deterministic check first.** From the archive, `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py` gave `127 passed in 173.39s` (pytest-guided.out).

## Both round-1 majors are fixed

1. **Disputed-line label: fixed.**
   - The grey box now reads "Also in this record, outside the highlighted words:" (step2.js:66).
   - Disputed lines underline the words that are not in the quote, with the caption "Underlined words are not in the highlighted words."
   - lib11 e1 underlines `Annual`, `visit`. e2 underlines `Patient`, `after`, `passenger`, `vehicle`, `struck`, `from`, `behind`. e4 underlines `Law`, `letter`, `protection`, `Fennimoor`, `Spine`, `Clinic`, `states`, `clinic` (r03.out, lib-s2-00-e1.png, lib-s2-05-e2.png, lib-s2-08-e4.png).
   - This is exactly what I need in order to tick the compare box honestly.
2. **Bates fill-in wording: fixed.**
   - The panel now says "One Bates number per record, not per page. ... Use this only if each of your records is one Bates page in that order." It also tells me to leave the fields blank and fill the cites in Word otherwise.
   - A live preview showed "record 1 reads [Ex. 3 / Bates RIVERA0101], record 2 reads [Ex. 3 / Bates RIVERA0102], and record 9 reads [Ex. 3 / Bates RIVERA0109]". The saved letter matched it exactly (0101 to 0109; the ER charge is 0102 and the MRI charge is 0108).
   - The numbers survived a reload, and clearing the fields restored `[Ex. __ / Bates __]` (r02.out, 08-bates-typed-preview.png, 09-bates-saved.png).

## Sample case end to end, timed

From Home, "Open the sample case" to the downloaded letter took **16.9 s scripted**: 33 key presses and 6 clicks, with drafting at 1.3 s (r01.out, r01_counts.json). At a human reading pace I still estimate 8 to 10 minutes.

Every Appendix A truth held:
- 9 lines, with EMS and ER both on January 9.
- The 73-day gap is flagged and the 28-day interval is not.
- The 01-09 vs 01-19 conflict shows all three highlights on screen. The multi-record window fix works (s2-01-...png).
- 12 planned PT visits vs discharge at visit 9.
- Both prior-condition mentions are flagged.
- The total is $6,240 + $2,150 = $8,390.00.
- The $185 rate goes to the notes only. Lost work is listed under DAMAGES MENTIONS.

My edits and decisions held:
- My record-3 edit is in the letter, and the original wording is under EDITED ITEMS.
- The dismissed flag appears only under FLAGS DISMISSED.
- A reload mid-review kept my place.
- The copied letter matched the downloaded letter.
- No console or HTTP errors in any run (the first-paint 404 is gone).

## The undated-ledger letter line: yes, it is a problem for a demand letter (major)

On lib11 I counted the three ledger lines after ticking "I checked this is a separate charge". The letter's BILLED CHARGES section then reads:
- `Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00`
- `Source ...: "New patient exam charge $250.00"`

The ledger line for $180 and the line for $2,310 follow the same pattern (lib11-letter.txt:39-44).

June 15 is the *statement date*: the record says "statement date 06/15/2026". In the same section, `Wexcombe Memorial ED, March 18, 2026: $3,260.00` uses a date of service, so any reader takes June 15 as the date of service. The chronology above it puts the new-patient visit on March 27, 2026 (lib11-letter.txt:19).

The adjuster will say the exam was billed on a day with no treatment record, after the last visit on May 29. That is checklist item 1: a line dated by something other than the date of service. Step 3 now shows the right label ("No date of service (statement dated June 15, 2026)", r03.out:406-408), so the screen and the letter disagree.

It is backend text (app/backend/export.py:339). I am grading it on the letter this UI produces. I rated it minor in round 1, when it was bundled with the Step 3 table. On its own, the letter line is the half that goes to the adjuster, so it is major. The sample letter is not affected.

## Round-1 minors

These are fixed:
- The e9 refusal now points to Step 3.
- A on a refused line leaves focus off "No".
- lib11 provenance now follows the case ("Demo: recorded AI answers" with "AI draft" cards).
- The Step 3 table shows the statement date correctly.
- Step 3 disputes now name a direction.

I did not re-exercise the public `/new` "our test cases" copy.

```json
{"card": "T-181", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive 9ab8cae (T-181 r2 fix) extracted to the session scratchpad; fixture backend, FIXTURE_SET=curated. Public demo mode (ZLAYT_MODE unset) at http://127.0.0.1:7941 (listener PID 14948); local copy (ZLAYT_MODE=local) at http://127.0.0.1:7942 (PID 15071) for library case lib11, since /api/library is local-only. Both stopped by PID; lsof exit 1 and curl 000 on both ports. Sample case: evals/golden/sample.txt via 'Open the sample case'. Library: case_lib11_priors_and_ledger. Viewport 1440x900. Evidence dir artifacts/review-evidence/T-181-paralegal-r2/.",
 "exercised": [
  "Read personas/paralegal.md, reviews/T-181-paralegal.md (round 1), the T-181 card notes and handoff, git diff 26287b9 9ab8cae for step2.js, step4.js and export.py",
  "From the archive: E2E_REQUIRE_DB=1 pytest -q tests/e2e/guided tests/e2e/test_no_console_errors.py: '127 passed in 173.39s' (pytest-guided.out)",
  "Sample case, timed, one Playwright run (r01_sample_e2e.py, r01.out): Home > Open the sample case > Draft the timeline (1.3 s) > all 19 Step 2 items with each card, highlight and outside-word list logged > E on record 3, retyped the line, Tab to Save, A focused the compare box, Space, A > reload after e5 > E on the gap flag with a note > D on the accident-date-source flag > Step 3: A on the 4 amounts (total chip $6,240.00 then $8,390.00) > Step 4 > Download letter at 16.9 s; Download notes; Copy letter (clipboard equals download)",
  "Read letter-download.txt and notes-download.txt against Appendix A truths",
  "Step 4 Bates panel (r02_bates.py, r02.out): read the panel text blank; typed Exhibit 3, prefix RIVERA, first number 101 and read the live preview after each; saved; compared letter cites to the preview; reloaded; cleared and saved (letter back to [Ex. __ / Bates __])",
  "lib11 on the local copy (r03_lib11.py, r03.out): picked the test case, Read, Draft (2.6 s); all 21 Step 2 items with outside-word lists and grey-box text; compare confirm on e1, e2 and e4; A then D on the refused ledger line e9 (focus stayed on card-foot); Step 3 all 8 amounts, ticking 'separate charge' and compare on the three ledger lines; Step 4 letter and notes downloaded (lib11-letter.txt, lib11-notes.txt)",
  "Read evals/library/case_lib11_priors_and_ledger.txt record 9 and app/backend/export.py:339 in the archive"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "keyboard_speed": 4, "charges_trust": 4, "compare_confirm_clarity": 5, "letter_usable": 3, "where_am_i": 5},
 "findings": [
  {"severity": "major", "title": "Letter dates counted undated ledger charges by the statement date, in the same format as a date of service",
   "evidence": "artifacts/review-evidence/T-181-paralegal-r2/lib11-letter.txt:39-44: 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00' / 'Source [Ex. __ / Bates __]: \"New patient exam charge $250.00\"', and the same pattern for $180.00 and $2,310.00. Record 9 (evals/library/case_lib11_priors_and_ledger.txt:46) says 'Itemized ledger, statement date 06/15/2026'. The same letter dates the new-patient visit March 27, 2026 (lib11-letter.txt:19), and the ED charge line above uses a date of service ('Wexcombe Memorial ED, March 18, 2026: $3,260.00', line 37). Step 3 now labels these 'No date of service (statement dated June 15, 2026)' (r03.out:406-408), but the letter drops that label. Code: app/backend/export.py:339 prints v.rec_date(n) for every charge. The worker's handoff left this line on purpose.",
   "why_it_matters": "The letter is what goes to the adjuster. A $250 new-patient exam dated June 15, after the last visit on May 29 and months after the March 27 exam in the same letter, is a date that matches no date of service. The adjuster will quote it back. That breaks checklist item 1 (nothing dated other than by date of service), and the screen and the letter now disagree.",
   "fix": "In export.py, for a counted charge whose line states no date of service, print 'Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; no date of service stated): $250.00'. Keep the date-of-service format only for charges whose own line carries the date. This is backend-owned and can be split to its own card.",
   "acceptance_test": "Export test on lib11 with a1-a4 counted: each ledger charge line contains 'statement dated June 15, 2026' and no charge line matches the bare pattern '<source>, June 15, 2026: $'; the ED line is unchanged."},
  {"severity": "minor", "title": "Step 3 dispute direction on the payment says 'may be an amount that is not a bill', which is what a payment already is",
   "evidence": "r03.out:360 (lib11 a6): 'Payment: money received, not a charge. / A second AI check thought this may be an amount that is not a bill, not what it was first sorted as.' Source: app/frontend/guided/review.js:82 maps SHOULD_BE_DAMAGES to 'an amount that is not a bill'.",
   "why_it_matters": "The direction was added so the tick is not a formality, but here it reads as agreement. I can't tell what the second check actually disputes (damages vs payment), so I'd tick on trust.",
   "fix": "Map SHOULD_BE_DAMAGES to 'a damages figure (lost wages or similar), not a payment or bill' or name the first sort: 'thought this may be a damages figure rather than a payment'.",
   "acceptance_test": "Guided e2e on lib11 a6: the compare-reason text names 'damages' and does not contain 'an amount that is not a bill'."},
  {"severity": "minor", "title": "Notes list the dismissed accident-date-source flag as 'Causation language' (pre-existing; missed in round 1)",
   "evidence": "artifacts/review-evidence/T-181-paralegal-r2/notes-download.txt:13 '- Causation language: record 7 (Hill Country Pain Management, new patient, May 18, 2026) \"Date of accident per intake form: 2026-01-19.\"'. The screen called the same flag 'Where the accident date comes from / Accident date source' (r01.out:277). The round-1 notes have the same line (artifacts/review-evidence/T-181-paralegal/notes-download.txt:13). The label comes from app/backend/export.py:357 (type causation).",
   "why_it_matters": "The attorney reads 'Causation language' over an accident-date quote and has to work out why. The screen and the notes name the same item differently.",
   "fix": "Label flags in the notes with the same title the guided screen used (e.g. 'Accident date source'), or add a subtype label for accident-date-source causation flags.",
   "acceptance_test": "Export test on the sample with f_r7_1 dismissed: FLAGS DISMISSED line starts 'Accident date source'."},
  {"severity": "minor", "title": "Notes opening line says every answer was checked by a second check, while my edited record-3 line was not",
   "evidence": "notes-download.txt:3 'This chronology was built from answers the team prepared for this demo and checked by a second check; ...' versus notes-download.txt:39 '(accepted by the paralegal after comparing it with the quote; second check not available)'. Text from app/backend/export.py:39 (AI_LINE_PREPARED, T-177 D-069).",
   "why_it_matters": "The notes are my record of how each line was verified. The opening sentence overstates it and repeats itself ('checked by a second check').",
   "fix": "'...prepared for this demo; a second AI check read each prepared answer (lines you rewrote were compared by you, see EDITED ITEMS).'",
   "acceptance_test": "Export test: AI_LINE_PREPARED does not contain 'checked by a second check'; with an edited item, line 3 does not claim every item was second-checked."},
  {"severity": "nit", "title": "Outside-word underline flags 'Patient' where the quote says 'Pt'",
   "evidence": "lib-s2-05-e2.png and r03.out: OUTSIDE-WORDS includes 'Patient'; the highlight reads 'Pt states neck and low back pain 7/10.'",
   "why_it_matters": "Conservative and harmless, but one false mark per abbreviation trains me to skim the underlines.",
   "fix": "Optional: treat a small list of chart abbreviations (Pt/patient, Dx/diagnosed, Rx/prescribed, C/O/complained) as matches in the word diff.",
   "acceptance_test": "lib11 e2 underlines do not include 'Patient'."}
 ],
 "whats_right": [
  "Underlined outside words plus the 'outside the highlighted words' grey box make the D-066 compare tick an actual check.",
  "Bates panel states the one-number-per-record rule and previews record 1, 2 and N; the saved letter matched the preview.",
  "Sample case: every Appendix A truth, $8,390.00 total, $185 only in the notes, and edits/dismissals/reload all held."
 ],
 "questions_for_chris": []}
```
