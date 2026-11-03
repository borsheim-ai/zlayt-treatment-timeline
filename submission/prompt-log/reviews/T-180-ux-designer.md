# T-180 review: guided UI spec + clickable mockup (ux-designer-reviewer)

Verdict: **changes** (0 blockers, 4 majors, 8 minors/nits). Scores: design quality 4, originality 4, craft 3, functionality 3 (static mockup; no score at or below 2).

I opened `artifacts/mockups/guided/*.html` over `file://` in Playwright at 1440x900, 1366x768, 390x844 and 320x640 and walked it as a first-time, non-technical user BEFORE opening the spec: Your cases -> Start a new case -> Add records (sample) -> We found 9 records -> Drafting (waited out the animation) -> 19 items of Step 2 (entry, fix, flag, gap, disputed, could-not-check, write-it-myself, date pick, done) -> Step 3 (charge, count-with-check, never-counted, done) -> Step 4 (ready, pending, blocked) -> clicked Download letter and read the saved file. Then I read `docs/GUIDED_UI_SPEC.md` in full and grepped `memory/contracts/api.md` and `app/backend/*.py` for every endpoint, field and error code the spec's section 11 uses.

## First-time-user walk (per screen: where am I / what do I do / am I done)

| Screen | Where | What to do | Done? | Hesitation, unknown words, movement |
|---|---|---|---|---|
| Your cases (index) | Yes, big h1, 4-bar track per card | Yes, one blue Continue per card, "Next:" line | Yes, Finished section, "Open letter" | Six cards at 1440 is calm. "Rename"/"Delete" read fine; Delete confirm swaps in place (nothing moved). "Demo: sample answers prepared by our team" shows 3 times (pill, footer, phone banner): noise. |
| Add records | Yes, step bar + "Step 1 of 4" | Partly: three tiles, but the button "Read the records" is at y 975-1031, below the 900 px fold | Not applicable | Clicked "Paste text": nothing changed, no textarea. "This demo can only read the sample..." sits under the button, after I could already pick Paste. |
| We found 9 records | Yes | Partly: "Draft the timeline" top at y 897, bottom 953 (cut by the fold) | Yes (green line) | "Start over with other records" is a second full button of equal weight. |
| Drafting | Yes | Yes (wait; "you can leave this page") | Yes ("All set", big button, focus moves) | "Loading the prepared line for each record" and "checked by code" mean nothing to a layperson. "19 timeline items" vs "9 records": unexplained jump. |
| Entry (Item 4 of 19) | Yes | Yes, one question, two big answers; highlight beside the line | Yes ("3 answered, 16 to go", bar) | "How it was checked ... second check agreed": what is the second check? Three numbers on screen: "Item 4", "Record 3", "Saved: item 3". |
| Fix the wording | Yes | Yes | Yes | Red "Not saved ... Remove it or change the quote": I can change the quote? (only by tapping sentences, which the left card explains). "Fix the wording" greys out while editing with no reason. |
| Warning / gap | Yes | Yes ("Should the attorney be told about this?") | Yes | "Gap of 73 days. Gap of 73 days between..." repeats itself. |
| Disputed | Yes | Yes, yellow box + ticking "I read this line myself" unlocks Yes | Yes | Good friction. "second check found this only partly supported" again undefined. |
| Could not check | Yes (amber tag) | Yes, "Write it myself" / "Skip it" | Yes ("Optional item") | "The model's quote does not appear word for word": "model" and "Its quote" (the spec renames quote to "the highlighted words"). |
| Pick the date | Yes | Yes, two dates plus "Suggested" | Yes | "month first / day first" is clear. "Decide later" leaves the case (goes to Your cases). |
| Step 2 done | Mostly: the step bar underlines both step 2 and step 3 | Yes | Yes, big check and counts add to 19 | Moved? No. "9 warnings for the attorney . 1 not needed" is clear. |
| Charge / count / never counted | Yes ("Bill total so far") | Yes | Yes | "itemized service line", "separate charge for a service" are billing words. "Yes, list it" is vague (list where?). Demo sentence is cut to "you decide ever..." by the total chip. |
| Step 3 done | Yes | Yes (total line is large) | Yes | Row "Amount: missing 3 days of work" in Never counted is not an amount. |
| Get your letter | Yes (all four green) | NO on arrival: Copy letter / Download are at y 1016, a 700 px scroll below a long letter | Yes (green row) | Downloaded file is clean plain text, 9 lines + 2 charges, total line, citations. "[Ex. __ / Bates __]" blanks have no cue until you scroll further. |
| Pending / blocked | Yes | Yes (amber row, "Go to the first one", ticking "Copy it anyway" enables Copy) | Yes | Good: shows exactly what would be sent. |

Nothing moved on click anywhere I tried (every answer is a page link, so this is a weak test of the real thing; the worker's own check_stability.py covers the same ground).

## Spec vs mockup vs API

- Control-to-API: all of section 11 maps to endpoints in `memory/contracts/api.md` EXCEPT three details documented only in code: `compared: true` and `422 COMPARE_REQUIRED` (`grep -c COMPARE_REQUIRED api.md` = 0; `app/backend/review.py:308` has it) and `POST /api/cases/pdf?title=` (api.md:83 says query `name`; `app/backend/api.py:303` accepts `title`). The spec discloses the first; the handoff says backend will add it.
- Spec contradicts itself: phone line card is "fixed 180 px" (2.7) and "fixed 256 px" (8).
- Spec says the paste/upload box, the Rename edit state, "Add a note", the home public-mode list and every Step 1 error line exist; the mockup has none of them (clicks do nothing).

```json
{"card": "T-180", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "docs/GUIDED_UI_SPEC.md; artifacts/mockups/guided/index.html + screens.html + 28 step/home pages; memory/contracts/api.md section mapping; static file:// mockup, no app server; sample case + two library cases as mocked",
 "exercised": [
  "Opened artifacts/mockups/guided/index.html in Playwright (chromium) at 1440x900, 1366x768, 390x844, 320x640 and walked Your cases -> Start a new case -> step1-add -> step1-found -> step1-drafting (waited 9.5 s for the animation) -> step2-entry/fix/flag/gap/disputed/cannot-check/write/date/date-confirmed/done -> step3-charge/count/never/done -> step4-letter/pending/blocked, before reading the spec",
  "Dumped visible text, every control, its href and its y position per page (artifacts/review-evidence/T-180-ux-pages.py); 50+ screenshots T-180-ux-*.png in artifacts/review-evidence/",
  "Clicked Download letter (.txt) on step4-letter, saved jordan-rivera-letter.txt to artifacts/review-evidence/T-180-dl/letter.txt and read it: one line per entry, citations, total line, no UI labels",
  "Clicked Paste text, Rename, Delete/Keep, Find a case on index/step1-add: Paste and Rename do nothing; Delete confirm and search work",
  "Measured Tab presses to the primary action (index 6, add 6, entry 8, step3-done 7, letter 8) and scrolling inner cards (T-180-ux-scrollcards.py): at 390 the source card is 122 px for 323/520/331 px of content",
  "Measured primary-button position at 1440x900 and 1366x768 (T-180-ux-fold.py): Read the records y975, Draft the timeline y897-953, Copy letter y1016",
  "Dark-mode screenshots of step2-entry and step4-pending",
  "Read docs/GUIDED_UI_SPEC.md lines 1-572 in full; grepped memory/contracts/api.md, app/backend/review.py and app/backend/api.py for every section 11 endpoint, field and error code"
 ],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 3},
 "findings": [
  {"severity": "major",
   "title": "The one action on three key screens is below the fold: Read the records, Draft the timeline, Copy/Download letter",
   "evidence": "artifacts/review-evidence/T-180-ux-fold.py at 1440x900 and 1366x768: step1-add 'Read the records' top 975 bottom 1031; step1-found 'Draft the timeline' top 897 bottom 953 (screenshot artifacts/review-evidence/T-180-ux-step1-found-1440.png shows only its top edge); step4-letter 'Copy letter' top 1016 (page scrolls to 1406; T-180-ux-step4-letter-1440.png shows the letter, no button). Review pages have a fixed action bar, these do not. Spec section 0 promises 'what do I do now' is next to the buttons.",
   "why_it_matters": "A first-time user on the 'Get your letter' screen sees a long wall of text and a green 'ready' row but not the Copy or Download button, which is the whole point of the product. Same for starting the read and starting the draft. 'Know what to do' fails until she scrolls, and the page-level scroll plus the letter box's own scroll is a nested-scroll trap.",
   "fix": "Give Step 1 and Step 4 the same fixed action bar as the review pages (primary button always on screen), or move Copy letter / Download letter above the preview. Keep the 'Draft the timeline' list height so the button fits at 1366x768.",
   "acceptance_test": "Playwright at 1440x900 and 1366x768: on step1-add, step1-found and step4-letter the primary button's bounding box bottom is <= viewport height with no scrolling."},
  {"severity": "major",
   "title": "At 390 px the record is squeezed to 122 px, so the words she is asked to compare are mostly hidden, and Undo is cut off",
   "evidence": "T-180-ux-scrollcards.py: at 390x844 the source card body is 122 px tall holding 323 px (entry), 520 px (gap, two records) and 331 px (count) of content, no scroll cue; the prepared-answer card also scrolls (93/115 px, 72/126 px). Screenshots T-180-ux-step2-entry-390.png (highlight cut after 'Refer to physical therapy', 'How it was checked' cut mid-sentence), T-180-ux-step2-gap-390.png (shows record 6 only; record 7 and the 73-day dates are off-screen), T-180-ux-step3-count-390.png (reason 'The line states no date of service, so it is not an itemized...' is cut; 'Saved: ... counted...' ellipsized). Status slot at 390: 'kept in the letter. U...' (step2-gap-390.png). Spec 2.7 says line card 180 px, section 8 says 256 px, mockup shows less than either leaves for the record.",
   "why_it_matters": "The product's promise is that she checks the line against the words in the record. On a phone the Yes button is fully visible and the evidence 23-38 percent visible. Undo is the safety net for a wrong tap and its label is clipped.",
   "fix": "Rebalance the phone layout: shorter action bar (small buttons in one row, status slot on its own line that wraps), give the source card the larger share and cap the line card to its text, add a visible 'Scroll for more' fade or 'Show all of this record' control, and let the status line wrap so Undo is always whole. Reconcile 2.7 and 8.",
   "acceptance_test": "At 390x844 on step2-entry, step2-gap, step3-count: source card clientHeight >= 220 px or scrollHeight - clientHeight <= 24 px; the Undo link's rect is fully inside the viewport and its text is not ellipsized; the reason sentence in the line card is not clipped."},
  {"severity": "major",
   "title": "The first real screen (paste/upload) and its errors are not in the mockup, and the demo offers paste and upload that it then refuses",
   "evidence": "T-180-ux-interact.py: clicking 'Paste text' on step1-add.html leaves 0 textareas visible and the panel unchanged (T-180-ux-step1-paste-click-1440.png); Upload does nothing either; no page shows the 400/413/409/429/pdf error lines, the 'Reading...' state, the Rename input (0 inputs after clicking Rename on index.html) or 'Add a note'. Spec 4.1 describes a 280 px box 'that does not change size between choices' and a reserved error line; spec 3.1 describes Rename in place. On the same screen the line 'This demo can only read the sample and our test cases.' sits BELOW the Read button.",
   "why_it_matters": "Paste is how every real user starts and its error states (empty, oversized, busy, offline with 'Your text is still here') are exactly where trust is lost. The layout-stability claim in spec section 13 is untested for the largest input box. In demo mode a grandma will pick Paste, type, press Read and get a 409: error prevention failure.",
   "fix": "Add mockup pages for paste (empty, filled, empty-submit error, too large, offline with text kept), upload, scanned PDF, Rename editing and Add a note. In demo mode show the demo sentence above the tiles and mark Paste/Upload as 'not available in this demo' (disabled with the reason) instead of failing after the click.",
   "acceptance_test": "check_stability.py covers the new pages with 0 moved boxes at 1440/390/320; Playwright: in demo mode the Paste and Upload tiles are aria-disabled and the reason is visible without hover; every Step 1 error row in spec 4.1 has a mockup page."},
  {"severity": "major",
   "title": "Words a grandma cannot decide with remain on decision screens: 'second check', 'the model's quote', 'checked by code', 'itemized service line'",
   "evidence": "step2-entry 'How it was checked: Quote found word for word, every number in the summary is in the quote, and the second check agreed.'; step2-disputed 'The second check found this only partly supported by the quote.'; step2-cannot-check 'The model's quote does not appear word for word in the record' / 'Its quote:'; header line on steps 2-3 'prepared by our team and checked by code'; step3-count 'it is not an itemized service line and is not totaled'; drafting list 'Loading the prepared line for each record'. Spec section 10 renames 'excerpt/quote' to 'the highlighted words' and 'judge' to 'the second check' but nothing on screen says what the second check is; spec 0 says server sentences are 'shown as given', which is how 'model' and 'quote' get through.",
   "why_it_matters": "Brief: 'someone's <Chris's message omitted>'. The disputed screen asks her to overrule the second check, so she must know what it is. 'Quote' and 'highlighted words' name the same thing on neighbouring screens.",
   "fix": "Add one plain sentence where the second check first appears ('A second AI pass re-read each line against the record') and use one word for the evidence everywhere (highlighted words). Because server `why` text is shown as given, either ask backend for plain-language variants or have the UI map reason codes to its own sentences, and say so in the spec. Replace 'checked by code' with 'checked by the computer, not by a person'. Reword 'itemized service line' to 'a single dated bill line'.",
   "acceptance_test": "A text lint over every mockup page and every spec section 11 server sentence finds no occurrence of 'model', 'its quote', 'checked by code', 'itemized'; the Step 2 entry page contains a one-sentence definition of 'second check'; a 3-person read-aloud test of step2-disputed and step3-count with no questions asked."},
  {"severity": "minor",
   "title": "Step bar shows two current steps on the Step 2 done screen",
   "evidence": "T-180-ux-step2-done-1440.png: step 2 (blue check, underline) and step 3 ('3', '4 of 4 left', underline) both marked current while the page says 'Step 2 of 4'. Spec 9.2: current step is the first step not done.",
   "why_it_matters": "Where am I? The bar moves its highlight from step 2 to step 3 before she has pressed 'Go to step 3'.",
   "fix": "On a step's done screen keep that step current; show the next step as remaining.",
   "acceptance_test": "On step2-done exactly one segment has aria-current=step and the accent underline, and it is step 2."},
  {"severity": "minor",
   "title": "Locked steps all read 'After step 1', including step 4",
   "evidence": "T-180-ux-step1-add-1440.png / T-180-ux-01-add-1440.png step bar: '2 After step 1', '3 After step 1', '4 After step 1'. Spec 2.4 table.",
   "why_it_matters": "Reads as if step 4 happens right after step 1; hides the order the brief asks for (clear defined steps).",
   "fix": "Use 'After step 1', 'After step 2', 'After step 3', or 'Not yet' for all three.",
   "acceptance_test": "Step bar text on step1-add lists three distinct status lines."},
  {"severity": "minor",
   "title": "Spec depends on API details that api.md does not document, and contradicts itself on phone card height",
   "evidence": "grep -c COMPARE_REQUIRED memory/contracts/api.md -> 0 (code: app/backend/review.py:308 compare_error); memory/contracts/api.md:83 documents 'optional query name' for POST /api/cases/pdf but app/backend/api.py:303 accepts title; docs/GUIDED_UI_SPEC.md 2.7 'fixed 180 px' vs section 8 'fixed 256 px'.",
   "why_it_matters": "The build card will implement 'every control maps to a real API' from api.md. Undocumented fields are where a frontend/back-end mismatch hides (this is the D-066 accept path).",
   "fix": "Backend adds `compared`, `422 COMPARE_REQUIRED` and PDF `title` to api.md (spec already flags the first); spec picks one phone card height.",
   "acceptance_test": "grep finds COMPARE_REQUIRED, compared and the pdf title query in memory/contracts/api.md; the spec has one phone card height."},
  {"severity": "minor",
   "title": "Never-counted list can show a non-amount as the Amount",
   "evidence": "step3-done page: 'Never counted (2)' row 'missing 3 days of work | Capital PT, visit 8 | This figure is not a bill (for example a damages or settlement figure)'. Spec 6.3 shows the figure 'as written (text)'.",
   "why_it_matters": "A first-time user cannot tell what this row is or why it is in the Bills step; it looks like a bug.",
   "fix": "When `text` has no currency symbol, label it 'Number found in the record: 3 days' or drop it from Step 3 and tell the backend it is not an amount.",
   "acceptance_test": "No Step 3 row's Amount cell lacks a digit-with-currency pattern unless it carries a plain 'not a money amount' label."},
  {"severity": "minor",
   "title": "Letter can be copied with unfilled [Ex. __ / Bates __] and no warning; the number fields sit below the buttons",
   "evidence": "T-180-ux-step4-letter-scroll700-1440.png: Copy/Download above, 'Exhibit and page numbers (optional)' below; T-180-dl/letter.txt has 11 'Source [Ex. __ / Bates __]' placeholders.",
   "why_it_matters": "She pastes into a demand letter with blanks she did not know to fill. Optional, but unflagged.",
   "fix": "Move the box above the buttons or add one line under Copy: 'The [Ex. __ / Bates __] blanks are for you to fill in.'",
   "acceptance_test": "Step 4 shows a visible sentence about the blanks next to Copy letter."},
  {"severity": "minor",
   "title": "Three numbering schemes and two labels for the same thing on one review screen",
   "evidence": "step2-entry: 'Item 4 of 19', 'Record 3', 'Saved: item 3 (Central ER discharge summary)'; step2-entry tag 'Prepared answer' vs step2-date-confirmed 'AI draft'; step bar circle '2' plus label '2 Check the timeline' (visible duplication in T-180-ux-step2-entry-1440.png); spec 7.1 'Download notes (.txt)' vs mockup 'Download notes'.",
   "why_it_matters": "Small contradictions add reading effort for the person the brief is about; tag names are explained nowhere.",
   "fix": "Say 'Line 4 of 19' and 'Record 3' consistently or drop the record number from the card header; explain the tags in one footer sentence; drop the number from the label or the circle.",
   "acceptance_test": "One counting word per screen; both tags have an on-screen explanation."},
  {"severity": "minor",
   "title": "Step 3 title row truncates the demo sentence and the title row sits 16 px under the step bar",
   "evidence": "T-180-ux-step3-count-1440.png: 'In this demo the sample summaries and flags were prepared by our team and checked by code; you decide ever...' cut by the 'Bill total so far' chip; 'Step 2 of 4 / Check the timeline' starts at y187 under a bar ending at y171 (T-180-ux-step2-entry-1440.png).",
   "why_it_matters": "Truncated provenance text and a cramped title weaken the 'look nice' goal and the D-065 provenance statement.",
   "fix": "Let the demo sentence wrap on its own row or move it to the footer slot; add 16-24 px above the eyebrow.",
   "acceptance_test": "No ellipsis in the title row at 1440 and 390; title row top margin >= 16 px."},
  {"severity": "nit",
   "title": "Preference, not a spec violation: 'No, leave it out' is the only 'No' to 'Does this line say the same thing?', and 'Fix the wording' is a small text link",
   "evidence": "step2-entry-1440.png action bar: Yes (filled), 'No, leave it out' (outlined), 'Fix the wording' same weight as 'Back'.",
   "why_it_matters": "A user who honestly answers 'No, it does not match' deletes the line instead of repairing it. I would have done it differently; the spec's equal-size answers are a deliberate choice.",
   "fix": "Consider 'No, it doesn't match' leading to Fix the wording / Leave it out as a second step.",
   "acceptance_test": "n/a (design preference)"}
 ],
 "whats_right": [
  "Fixed frame with the highlighted record beside the line, one question, two equal answers, 'N answered . N to go' and a green done screen: it answers where/what/done on every review page at 1440.",
  "Friction is placed correctly: ticking 'I read this line myself' unlocks Yes on a disputed line; 'Copy it anyway' gates a letter with undecided items, and the preview shows exactly what would be sent.",
  "The downloaded letter is clean pasteable text with citations and the exact total line, and the notes box is plainly marked 'Do not send'."
 ],
 "questions_for_chris": [
  "Is 1366x768 a target screen for the 'grandma' user? Finding 1 gets worse there (nothing below the step bar fits).",
  "In the public demo, should Paste and Upload be shown disabled up front (my recommendation) or hidden entirely?"
 ]}
```
