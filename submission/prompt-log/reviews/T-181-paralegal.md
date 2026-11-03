# T-181 guided 4-step UI (D-068): paralegal review (Maria Delgado, senior PI paralegal)

**Verdict: changes** (0 blockers, 2 majors, 7 minors, 2 nits). Scope: `git archive 26287b9` run in demo mode (fixture backend, curated set, no live calls).
- Public demo copy: port 7931, listener PID 49893.
- Library run: the same archive with `ZLAYT_MODE=local`, port 7932, PID 57169. The library is local-only by design (api.py:282).
- Both servers were stopped afterwards (`lsof` returned nothing, `curl` returned 000).

I took the sample case from **Your cases** to a downloaded letter using only what the screen said. Then I opened lib11 (priors and ledger) and did Step 2 and Step 3. The guided suite run from the archive: `100 passed in 148.47s`.

**Timing for the sample case:**
- Wall clock was about 5 min 10 s, from "Open the sample case" (16:10:21) to the downloaded letter (about 16:15:30). That includes reading all 23 items against the raw records.
- Drafting took about 1.5 s.
- The decision pass was 34 key actions and 5 clicks: Continue on Your cases ×3 (I resumed between script runs), one deliberate Undo, and Go to step 4. Before that came Open the sample case and Draft the timeline. The scripted keys took 17.5 s.
- At a human reading pace I'd expect about 8 to 10 minutes for this case.

**What I would tell my attorney:**
- I would use this letter. Every Appendix A truth is right:
  - 9 lines, with EMS and ER both on 01-09.
  - The 73-day gap is flagged and the 28-day interval is not.
  - The 01-09 / 01-19 conflict is flagged with both quotes, and the tool does not pick one.
  - 12 planned PT visits vs. discharge after two missed appointments.
  - Both prior-condition mentions.
  - $6,240 + $2,150 = **$8,390.00**.
  - $185 is never counted ("Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger." appears in the notes only).
  - Lost work appears under DAMAGES MENTIONS, not as a charge.
- My edit to record 3 reached the letter. The original wording is kept under EDITED ITEMS. My dismissed flag appears only under FLAGS DISMISSED. Decisions survived a reload. With undecided items, Copy and Download stay disabled until "Copy it anyway" is ticked.

**What I would fix before the gate (majors):**
1. **The disputed-item screen doesn't show what is disputed, and the grey box contradicts the line.** On lib11 e1, e2 and e4, the line uses a sentence from outside the highlighted quote. The grey box lists that same sentence under "Also in this record, not in any line:".
2. **The Bates helper assumes one page per record without saying so.** It numbers one Bates page per record in record order, but the screen never says that. The letter then carries specific page cites that nothing in the records supports.

**Grades asked for:**
- verify_quickly **4**: every item puts the full record, the highlighted verbatim quote and the line side by side, and the check is explained in one sentence.
- Keyboard **4**: A, D and E plus Space and Tab handle everything. The arrows move between items. Reload keeps working. No key moves between steps.
- Charges **4**: counting matches D-059 to D-062 and D-064, and lib11 comes to $6,000 with each ledger line cited. Undated ledger lines carry the statement date in a "Date" column.
- Compare confirm **3**: the box is deliberate and never pre-ticked, but it doesn't say which words are in dispute.
- Letter **4**: I'd paste it, but I'd leave the Bates helper empty.
- Where you are **5**: the step bar, "Item N of M · X answered · Y to go", the done screens and "Finished. Your letter is ready." on home were right every time.

```json
{"card": "T-181", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive 26287b9 (guided UI: f3d42a2, 848bbad, 3944cc2, 26287b9) extracted to the session scratchpad. Public demo mode (LLM_BACKEND=fixture FIXTURE_SET=curated, ZLAYT_MODE unset) at http://127.0.0.1:7931 (listener PID 49893). Library run: the same archive with ZLAYT_MODE=local at http://127.0.0.1:7932 (PID 57169), because /api/library is local-only (app/backend/api.py:282). Both were stopped with kill; lsof found no listener and curl returned 000 on both ports. Sample case: evals/golden/sample.txt via 'Open the sample case'. Library: case_lib11_priors_and_ledger via Start a new case > Choose a test case. Viewport 1440x900.",
 "exercised": [
  "Read personas/paralegal.md, the T-181 card notes, D-059 to D-068 in memory/ORCHESTRATOR_DECISIONS.md, and docs/GUIDED_UI_SPEC.md sections 3 to 7 and 9",
  "Guided e2e suite from the archive: E2E_REQUIRE_DB=1 pytest tests/e2e/guided -q gave '100 passed in 148.47s'",
  "Sample case, Playwright with a persistent profile. Steps:",
  "  Opened the empty Your cases page and clicked Open the sample case: Step 1 showed 'We found 9 records'",
  "  Clicked Draft the timeline (about 1.5 s), saw 'All set', then went to Step 2",
  "  Paged through all 19 Step 2 items with ArrowRight without deciding, and compared each date, provider, line and highlighted quote with sample.txt (s05_catalogue.out)",
  "  Timed keyboard pass: A on most items; E on record 3, retyped the line, Tab to Save my wording; the compare box showed; A moved focus to the checkbox, Space ticked it, A accepted",
  "  Reloaded the page mid-review: position and decisions were kept",
  "  E on the gap flag: typed a note, saved it with Tab and Enter (the flag was accepted with the note)",
  "  D on the accident-date-source flag; A on the new-onset flag, clicked Undo, then A again; reached the Step 2 done screen",
  "  Step 3: catalogued the 4 amounts, then A on each; the total chip showed $6,240.00 then $8,390.00; done screen",
  "  Step 4: read the letter and the notes; Download letter and Download notes; Copy letter (clipboard text equals the download); clean-text check (check_letter.py)",
  "  Filled Exhibit 3 / Bates prefix RIVERA / First number 1, saved, and reloaded",
  "  Home shows 'Finished. Your letter is ready.' with an 'Open letter' button",
  "Second sample case: decided 2 items, jumped to Step 4. Copy and Download were disabled until 'Copy it anyway, without 21 items'; the preview held only the 2 accepted lines",
  "Public demo Start a new case: only the sample tile is offered; GET /api/library returned 404",
  "lib11 on port 7932: picked the test case, Read the records, Draft (1.5 s)",
  "lib11 Step 2: worked all 21 items. Compare confirm on the disputed lines e1, e2 and e4. The ledger line e9 was refused (CHARGE_TEXT_IN_ENTRY)",
  "lib11 Step 3: all 8 amounts. Counted ED $3,260; counted ledger lines $250, $180 and $2,310 with the 'separate charge' and compare boxes; listed the total, payment, adjustment and balance; done screen showed $6,000.00",
  "API reads (api_e1.py, curl): item e1/e2/e4/e9 why, reasons and ladder.judge; the lib11 export letter_text"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "keyboard_speed": 4, "charges_trust": 4, "compare_confirm_clarity": 3, "letter_usable": 4, "where_am_i": 5},
 "findings": [
  {"severity": "major", "title": "Disputed-item screen doesn't say what is disputed, and its grey box says the borrowed sentence is 'not in any line' when the line uses it",
   "evidence": "artifacts/review-evidence/T-181-paralegal/28-lib-s2-00-e1.png: the line reads 'Annual visit; history per patient of car accidents in 2019 and 2022...', the highlighted quote starts at 'History per patient', and the grey box reads 'Also in this record, not in any line: “Annual visit.”'. The same pattern is in 28-lib-s2-05-e2.png ('...after passenger vehicle was struck from behind' vs 'not in any line: “Passenger vehicle struck from behind.”') and 28-lib-s2-08-e4.png ('Law firm letter of protection to Fennimoor Spine Clinic...' vs 'not in any line: “Letter of protection to Fennimoor Spine Clinic.”'). The dispute box only says 'A second AI check found this only partly supported by the highlighted words.' The API has no more detail: why 'A second AI check found the summary only partly supported by the quoted text.', ladder.judge reason_code 'OTHER_UNSUPPORTED', and code_checks.summary_tokens_not_in_excerpt [] (api_e1.out). The label comes from app/frontend/guided/step2.js:66.",
   "why_it_matters": "D-066 asks me to compare deliberately, and this is the screen where I do it. The screen has the exact words the line borrowed from outside the quote, but it tells me they are in no line, which contradicts the line beside it. If I tick 'I read this line...' on trust, the letter carries 'Annual visit' and 'after ... struck from behind' with a Source quote that does not contain them. The adjuster can quote that back at us.",
   "fix": "Relabel the grey box 'In this record but not in the highlighted words'. On a disputed or edited item, mark (underline) the words in the line that are not in the highlighted quote, using a deterministic word diff, with a caption such as 'These words are not in the highlighted quote'. Keep the checkbox as it is.",
   "acceptance_test": "Guided e2e on lib11 e1: the grey box heading does not contain 'not in any line', and the line card marks 'Annual visit' as outside the quote. Same check on e2 for 'struck from behind'."},
  {"severity": "major", "title": "Bates helper numbers one page per record in record order, and the screen never says so",
   "evidence": "Step 4 panel text: 'Exhibit and page numbers (optional) / Fill these in to replace “[Ex. __ / Bates __]” in every source line.' (app/frontend/guided/step4.js:148). With Exhibit 3, prefix RIVERA and first number 1, letter-with-bates.txt reads line 5 'Source [Ex. 3 / Bates RIVERA0001]' (record 1), line 33 '[Ex. 3 / Bates RIVERA0008]' (MRI, record 8) and line 42 '[Ex. 3 / Bates RIVERA0002]' (the ER charge). The rule is memory/contracts/api.md:115 'NNNN = first number + record number - 1'. The backend has worked this way since T-058 (dbb2c66). T-181 puts it on the new Step 4 screen without the rule. Screenshot 22-step4-bates-filled.png.",
   "why_it_matters": "Real records run many pages each, so record 8 is almost never page 8. The letter would then send the adjuster specific Bates cites that nothing in the records supports, and these are exactly the cites they check first. The screen reads as if the tool knows the pages. The default with the panel blank is safe.",
   "fix": "On the panel, state the rule and preview it before Save, for example: 'Each record gets one number, in order: record 1 = RIVERA0001 ... record 9 = RIVERA0009. Use this only if each record is one Bates page in this order; otherwise leave it blank and fill the cites in Word.' Better still, accept a starting Bates number per record.",
   "acceptance_test": "Guided e2e test_step4: the cfg panel text names the one-number-per-record rule. After the prefix and first number are typed, a preview shows record 1 and the last record's cite before Save."},
  {"severity": "minor", "title": "Step 2 tells me no ledger amount will be in billed charges; Step 3 then lets me count three of them",
   "evidence": "lib11 e9 card (28-lib-s2-19-e9.png, s13.out): '...Its amounts were read but not totaled (the notes for the attorney say why), so none of them is in Billed charges; dismiss this line unless it states treatment.' It also says 'pick a highlighted words without the amount'. Step 3 for the same ledger (s14.out) offers 'You can still count it if you checked the ledger yourself'. After counting, Step 3 done reads 'Billed charges accepted from these records: $6,000.00' with $250, $180 and $2,310 counted.",
   "why_it_matters": "On the charges question the two steps contradict each other. A paralegal who believes Step 2 would leave real ledger charges out of the specials.",
   "fix": "In the guided UI, replace the reason's last clause with 'Its amounts are decided in step 3, Check the bills.' Fix 'a highlighted words'.",
   "acceptance_test": "Guided e2e on lib11 e9: the card text does not contain 'none of them is in Billed charges' and does name step 3."},
  {"severity": "minor", "title": "Pressing A on a refused line moves focus to 'No, leave it out', so the next Space or Enter leaves the line out",
   "evidence": "s13.out on lib11 e9 (Yes disabled, no checkbox): 'after a on disabled: focus answer-no'. My next Space left the line out. The Step 2 done list shows '20 / Jun 15, 2026 / Fennimoor Spine Clinic, itemized ledger / Left out'. Code: review.js:308 (press() looks for an unticked checkbox and finds none).",
   "why_it_matters": "Working fast by keyboard, A then Space is a natural rhythm, and it quietly turns a 'yes' into a dismissal. Undo exists, but only if I notice.",
   "fix": "When Yes is refused and there is no checkbox, keep focus where it was (or on the refusal message) and say 'Yes is not available for this line: <reason>'. Don't move focus onto a decision button.",
   "acceptance_test": "Guided e2e: on a CHARGE_TEXT_IN_ENTRY item, press 'a' and assert the active element is not answer-no and no review POST was sent."},
  {"severity": "minor", "title": "lib11 screens say the answers were 'not written by an AI model' while each card says 'AI draft'",
   "evidence": "28-lib-s2-00-e1.png: the title row reads 'Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.' The header pill reads 'Demo: sample answers prepared by our team'. The card tag reads 'AI draft' (the case's models.generator is 'claude-sonnet-5-5', generator_prepared false). The note is taken from server health, not from the case (review.js:45 R.aiNote; G.provenance). The Step 2 done legend says 'A second AI check read each one against the record' (step2.js:331), but my edited record-3 line said 'A second AI check is not available in this demo, so this item has not been double-checked' (10-step2-compare-ticked.png).",
   "why_it_matters": "Whether an AI or a person wrote a line decides how hard I read it. The same screen tells me both. D-065 provenance is the PM's lens; I raise it only because it changes how carefully I verify.",
   "fix": "Build the title-row note from the case (models.generator_prepared / item.prepared), not from health. In the legend, say a second check read each line 'unless the line says it was not double-checked'.",
   "acceptance_test": "Guided e2e on lib11 in demo mode: the title row does not contain 'not written by an AI model' while any queue item is tagged 'AI draft'."},
  {"severity": "minor", "title": "Undated ledger lines are listed under a 'Date' column with the statement date",
   "evidence": "lib11 Step 3 card: 'The line states no date of service, so it is not a single dated bill line and is not totaled.' The Step 3 done 'Counted' table (s14.out) then lists '$250.00 / Fennimoor Spine Clinic, itemized ledger / June 15, 2026' under the header 'Date'. The letter reads 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00'. In the record, 06/15/2026 is the statement date, and the new-patient exam was seen 2026-03-27 (record 5).",
   "why_it_matters": "Checklist 1: nothing may look as if it is dated by something other than the date of service. An adjuster reading 'June 15, 2026: $250.00' as the exam date would say the exam was billed months after the visit.",
   "fix": "For a counted line with no date of service, show 'no date of service (statement June 15, 2026)' in the Step 3 table, and use 'statement dated June 15, 2026' in the letter line.",
   "acceptance_test": "Export test on lib11 with the three ledger lines counted: each ledger charge line contains 'statement' and no bare 'June 15, 2026:' before the amount."},
  {"severity": "minor", "title": "Step 3 dispute line doesn't say what the second check disagreed about",
   "evidence": "lib11 a2 to a6 and a8 (s14.out, 31-lib-s3-01-a2.png): 'A second AI check disagreed with the first result for this item.' plus the box 'I read this amount against the highlighted words myself.' The string is fixed text (review.js:49).",
   "why_it_matters": "On an amount, the disagreement is either 'this is a charge' or 'this is not a charge', and those mean opposite things for the total. As written I can't tell which way it went, so the compare tick is a formality.",
   "fix": "Name the direction from the judge verdict. For example: 'A second AI check thought this may not be a separate charge.' or '... thought this may be a charge, not a total.'",
   "acceptance_test": "Guided e2e on lib11 a2: the dispute sentence contains 'charge' and is not the bare 'disagreed with the first result' string."},
  {"severity": "minor", "title": "On the conflict warning, the record-7 sentence that makes the conflict is below the fold of the record pane",
   "evidence": "07-cat-01-f_accident_date_after_treatment_1_2_7.png at 1440x900: the left pane opens on records 1 and 2 ('Date: 2026-01-09' highlighted). Record 7's 'Date of accident per intake form: 2026-01-19' needs scrolling inside the pane. The right card quotes it.",
   "why_it_matters": "This is the flag the adjuster will use. I should see both sides of the conflict highlighted without scrolling inside a box.",
   "fix": "For multi-record warnings, show only each record's highlighted sentence (with 'show whole record'), or scroll the pane so every highlight is in view.",
   "acceptance_test": "Guided e2e at 1440x900 on the sample conflict flag: every <mark> in the source pane is within the pane's visible rect."},
  {"severity": "minor", "title": "Public demo says it can read 'our test cases' but offers none",
   "evidence": "s11.out at /new on port 7931: 'This demo can only read the sample case and our test cases.' The only tile that works is 'Use the sample case', and the browser logged 'http 404 GET /api/library' (app/backend/api.py:282, local-only).",
   "why_it_matters": "On the public demo I went looking for the test cases the page promised and found nothing to click.",
   "fix": "In public mode, drop 'and our test cases' (or expose the library read-only if Chris wants it in the demo).",
   "acceptance_test": "Guided e2e in public mode: the demo note on /new contains no 'test cases' when GET /api/library is 404."},
  {"severity": "nit", "title": "After an edit, Step 2 shows only my wording; the original is only in the Step 4 notes",
   "evidence": "10-step2-compare-ticked.png: the card shows 'Written by you' and my text. The Step 2 done list shows item 4 as plain 'Kept'. The original appears only in the notes: 'EDITED ITEMS - Record 3 ... summary was \"Persistent neck pain 6/10 and daily headaches; referred to physical therapy...\", now \"...\"'.",
   "why_it_matters": "Checklist 14 is met through the notes. When I go back to check an edit, a 'was:' line on the card would save me a trip to Step 4.",
   "fix": "Show 'Was: <original>' muted under the line on an edited item, and 'Kept (your wording)' in the done list.",
   "acceptance_test": "Guided e2e: after editing sample e3, the card and the done-list row both show that it was edited."},
  {"severity": "nit", "title": "Status from the previous item sits under the Fix-the-wording box, with an Undo for that other item",
   "evidence": "08-step2-fix-wording.png: editing item 4 while the footer reads 'Saved: item 3 kept in the letter.' with an Undo button.",
   "why_it_matters": "It's easy to think Undo cancels the edit in front of me.",
   "fix": "Clear the previous status when Fix the wording opens.",
   "acceptance_test": "Guided e2e: after pressing E on an item, the footer has no Undo button."}
 ],
 "whats_right": [
  "One item per screen: the whole record with the verbatim quote highlighted, next to the line, with one plain question. I verified all 19 sample items against sample.txt with no mismatch.",
  "Charges: only cited charges count. The sample total is $8,390.00, with the $185 rate and lost work never counted. lib11 ledger lines count only after the 'separate charge' tick and come to $6,000.00, each cited to its own line.",
  "The letter has only accepted items, each with a verbatim quote and [Ex. __ / Bates __], the D-062 total and clean text. Dismissed and undecided items stay out, and copying with undecided items needs an explicit tick."
 ],
 "questions_for_chris": [
  "Should the Bates fill-in stay in the MVP, given it assumes each record is one Bates page in record order? Or should it be hidden until it can take a start number per record?"
 ]}
```
