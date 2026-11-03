# T-166 MVP UX audit: the whole journey (overview, case, review, export)

Reviewer: ux-designer-reviewer (Priya Raman persona), model claude-opus-5-5. Date 2026-11-02.
Build: `git archive 95ffe36` (HEAD at start) served from scratch on 127.0.0.1:7966, `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, scratch `ZLAYT_DB`. Sample case `evals/golden/sample.txt`.
Evidence: `artifacts/review-evidence/mvp-audit/` (screens `NN-*.png`, scripts `walk*.py`, raw output `walk*.out`, pasted exports `export-*.txt`).

**Verdict: changes.** There are no blockers. Every item has its source one action away, the letter holds only accepted items, and errors keep the pasted text. Seven P0s stop it from feeling finished:
1. No visible way to start a new case.
2. The case header wraps and covers the source pane's heading.
3. Clipped excerpts, including the $2,150 charge's own amount.
4. An alarming edit state that also hides the quote.
5. Dismiss sends the row and the focus off-screen.
6. The keyboard loop dead-ends.
7. Test and developer wording on the paralegal's screens.

All are frontend work except two one-line backend copy edits (F4).

Scores: design quality 3, originality 3, craft 2 (F2, F3), functionality 3.

## Journey as walked
| Step | 1440 light | 1440 dark | 390 light / dark | Keyboard |
|---|---|---|---|---|
| 1 Land on overview | 01-landing-empty-light-1440, 17-overview-5cases-light-1440 | 01-…-dark-1440, 17-…-dark-1440 | 01-…-390, 17-…-390 | 7 Tabs to first case link; 12 Tabs to the name field once 5 cases exist |
| 2 Create + name | 02-create-filled, 02-processing-1 (step names shown) | 12-kbd-ready-to-analyze | 15-phone-sample-preview, 15-phone-processing | after Enter on Analyze, focus fell to BODY |
| 3 Open | 05-case-top-light-1440 | 05-case-top-dark-1440 | 05-case-top-*-390 | 13 Tabs to Start review |
| 4 Review | 06-flags, 06-conflict, 06-charges, 06-unclear, 06-tray | 06-*-dark-1440 | 06-*-light-390 | 8 × `a`: 5 decided, 3 no-ops |
| 5 Edit one, dismiss one | 08-edit-open, 08-edit-saved, 09-after-dismiss | 14-kbd-entry-edit-saved, 14-kbd-entry-dismissed | 15-phone-edit-*, 15-phone-after-dismiss | `e`, Meta+Enter, `d`, `r` |
| 6 Export | 10-export-click, 11-copy-letter-click, 11-export-one-line | 12-kbd-export-copied | 11-export-top-dark-390, 15-phone-export | 92 Shift+Tab to reach Export |

## Ranked friction points
### P0: must fix for "finished" (major)
- **F1 There is no "New case" action.** The create form sits under the list: y 1,015 at 1440 and y 2,027 at 390 with 5 cases, and no button says New case. Fix in `overview.js`/`index.html`: add a primary "New case" button in the Cases card header that scrolls to and focuses `#case-title`, and rename the "Records" heading to "New case". Screens: 17-overview-5cases-light-1440.png, 17-overview-5cases-light-390.png.
- **F2 The case header wraps at 1440 and covers the source pane heading.** The header is 89 px on two rows, with Export dropped to the second row. The pane is `fixed; top:100px` and its heading sits at 113 to 133 px, but the header bottom is at 121 px with z-index 20. Fix in `styles.css` `.app-header-row`: keep it to one row with an ellipsized name and a short progress line, and group the tools at the right. Fix in `sidebyside.css`: set the pane top from a `--chrome-h` variable that `app.js` measures. Screens: 05-case-top-light-1440.png, 06-charges-light-1440.png.
- **F3 Excerpts are clipped mid-sentence, and the $2,150 row hides its own amount.** The $2,150 quote ends "…correlate clinicall…" with a stray sliver of the yellow highlight. 4 of 9 entry excerpts are clipped at 1440, and the only reveal is "More", the fifth link in the row. Fix: in `review.css:59`, window the charge quote around its mark, as the $6,240 row already does, and never clamp it. In `styles.css:154/163/209`, un-clamp pending and needs-review excerpts and put "Show full excerpt" directly under the quote (brief 7.3). Screens: 06-charges-light-1440.png, 06-charges-light-390.png.
- **F4 Edit lands in a "second check failed" state beside a cut-off quote.** On the demo backend every edit shows "The second check failed (the AI check was asked and gave no usable answer)" and asks "I compared it with the quote" while the quote is clamped to one line. An edit takes 3 actions (Edit, Save, compare), and the internal notes print "(JUDGE_UNAVAILABLE)". Frontend fix: un-clamp in this state, show your wording above the quote, and make it one confirm: "Matches the quote, accept". Backend copy only (no new feature): change `why.py:49` to "The second check is not available right now. Compare your wording with the quote, then accept." and drop the codes in `export.py:611`. Screens: 08-edit-saved-light-1440.png, 15-phone-edit-saved-light-390.png.
- **F5 Dismiss makes the row vanish and moves focus off-screen.** The row jumps to "Dismissed (n)". Focus lands at y 1,033 in a 900 px viewport, and at y 1,959 in 844 px at 390. Fix in `review.js` (RV.act / dismissedBox): leave a 6 s placeholder in the row's slot, "Dismissed: Capital PT, visit 8 · Undo", and never focus outside the viewport. Screens: 09-after-dismiss-light-1440.png, 15-phone-after-dismiss-light-390.png.
- **F6 The keyboard loop dead-ends.** `a` stops at the end of a flag group: presses 6 to 8 did nothing while 18 items were open. There is no `n` key, and Export is 92 Shift+Tabs away. Fix in `review.js`: at the end of a group, focus and announce the next group's first open item without deciding it. Add `n` (focusFirstPending) and `x` (focus Export), and list both in `?`. In `input.js`, focus Start review when a run finishes. Screen: 12-kbd-after-8a-dark-1440.png.
- **F7 Test and developer wording is on the paralegal's surfaces.**
  - Header chip "cached demo (curated responses)".
  - An amber box: "older version of the AI prompts … fixture backend (recorded replies, 10 golden cases…)".
  - "JUDGE_UNAVAILABLE" in the notes export.
  - "(the server answered 500). Request failed".
  - An "Audit" link on every row.

  Fix: reword the chip to "Demo: recorded AI answers". Move the calibration box into "How the AI was checked", reworded (`suggestions.js:138`). Strip the codes and move Audit into the Why dialog. Screens: 01-landing-empty-light-1440.png, 06-tray-light-1440.png, 16-err-list500-light-1440.png.

### P1: should fix (minor)
- **F8 "Do this first" and "Start review" point at different items.** "Do this first" points at the $185 rate in Charges. Start review goes to the causation flag. Make Start review use `next_action.item_id`. Screens: 05-case-top-light-1440.png, 07-start-review-light-1440.png.
- **F9 Counts and state names disagree.**
  - Unreviewed count: 18 on the chip, 19 in Case checks and the export count line.
  - After an edit, the live region says "16 left" while the header implies 17.
  - "Ready to send", "Can export" and "Ready to export" name the same state.

  Fix: one open-count helper (`overview.js:39`, `stepper.js:587`, `review.js` live text) and one name. Screens: 17-overview-5cases-light-1440.png, 08-edit-saved-light-1440.png.
- **F10 "checked 18, all agreed with the draft" sits beside "second check failed".** Fix `judges.js:134` to show agreed and not available separately. Screen: 08-edit-saved-light-1440.png.
- **F11 Rows carry too many controls.** An entry row has 8 controls. A flag card has 2 dismiss paths. Keep Accept, Edit, Dismiss and Open record, and put the rest under one "More actions" menu. Screens: 05-case-top-light-1440.png, 06-flags-light-1440.png.
- **F12 Undo or `r` on an edited row throws away her wording without asking.** After the reset, e5's summary is back to "Pain 4/10, improving." and edited is null. Confirm before discarding, or keep the wording as a restorable draft. Screen: 14-kbd-entry-edit-saved-dark-1440.png.
- **F13 One very long page.**
  - The page is 6,813 px at 1440 and 11,693 px at 390.
  - The gap flag sits at y 2,192 and y 4,065.
  - Export opens at the bottom, growing the page to 9,339 and 16,717 px, with no way back except scrolling.

  Add a sticky section nav (Timeline · Flags · Charges · Export) and a "Back to review" link. Screens: 06-gapflag-light-1440.png, 11-export-top-light-1440.png.
- **F14 Overview rows are heavy, and an abandoned sample leaves a ghost case.** Rows are about 190 px with a repeated 4-line paragraph and an "Analysis done" chip. A "Not analyzed yet" duplicate case appears. Slim the rows. Don't persist a case before Analyze, or label it Draft with a Delete action. Screens: 17-overview-5cases-light-1440.png, 15-phone-sample-preview-light-390.png.
- **F15 Error messages lack the next step.** "Request failed", and "This demo only runs the recorded sample cases." with no action. Map these in `input.js` to plain copy with one action button. Screens: 16-err-create500-light-1440.png, 16-err-nomarkers-light-1440.png.
- **F16 "Add a synthetic case" looks broken and repeats on every case page.** The text is flush to the border with no chevron (`switcher.js:46`). Screens: 01-landing-empty-light-1440.png, 06-bottom-light-1440.png.
- **F17 The case top is chrome-heavy.** The queue starts at y 552 at 1440 and y 762 at 390. The Timeline chip says "3 items need review" over nine Quote-matches rows. Merge the checks lines and drop the repeated counts. Screens: 05-case-top-light-1440.png, 05-case-top-light-390.png.

### P2: nice (nit)
- **F18 The empty overview still shows filters, search and sort, and the empty message has no buttons.** Screen: 01-landing-empty-light-1440.png.
- **F19 The case name field is 180 px wide, and its placeholder is cut to "Client or matter, for exa".** Screen: 01-landing-empty-light-1440.png.
- **F20 Dark mode: the search input and the progress track don't match.** The search input is grey (rgb 59,59,59). The progress track is invisible at 0 (rgb 28,34,43 on 21,26,33). Screen: 17-overview-5cases-dark-1440.png.
- **F21 The rate row gives two reasons.** Screen: 06-unclear-light-1440.png.
- **F22 Row links are 36 px tall at 390, against the brief's 44 px.** Severity is deferred to the accessibility reviewer. Screen: 15-phone-entry1-light-390.png.
- **F23 There is no theme toggle at 390.** Screen: 15-phone-case-top-light-390.png.
- **F24 Unclear wording and a UI-added ellipsis.** The "Not in an entry (1)" label is unclear, and the UI adds a leading "…" to the $6,240 quote. Screen: 06-charges-light-1440.png.

## What is right (keep)
- When an item is selected, the source pane highlights its exact excerpt inside the full record (08-edit-open-light-1440.png).
- Input errors are inline and plain, and they keep the pasted text: 71,440 characters kept on oversize, and the full sample kept on a forced 500.
- The export pastes cleanly with citations. Copy asks first and names what is unreviewed. The edited wording reaches the letter once confirmed (export-letter-two-line.txt, walk14.out).

## Probe notes
- The case state seen in later walks reflects earlier walks. In walk5 the first "Undo" button belonged to entry-1, not entry-5, so entry-1 went back to pending.
- In walk7, my edit text was for another record, so the code correctly refused it ("…not in the quote: 10").
- The walk8 page-wide text selection is mine (Meta+a while focus was not in a text box).
- Timings come from the scripts, not from a human: the pointer loop took 9.7 s for 9 clicks, and the keyboard journey took 60.1 s for 159 keys (including probe overhead).

```json
{"card": "T-166", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "HEAD 95ffe36 via git archive into scratch; app http://127.0.0.1:7966 (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch ZLAYT_DB); sample case evals/golden/sample.txt; journey overview -> create+name -> open -> review -> edit+dismiss -> export at 1440x900 and 390x844, light and dark, pointer, touch and keyboard",
 "exercised": [
  "walk1: empty overview at 1440/390 light/dark",
  "walk2: named a case by paste (Rivera v. Northgate (MVA 2026-01)), Analyze, captured processing steps, landed on case",
  "walk3/4: opened the case from the overview row in 4 modes; measured section positions (gap flag y 2,192 / 4,065; doc 6,813 / 11,693 px); shot flags, conflict, charges, unclear, could-not-verify tray, narrative, Bates settings, page bottom",
  "walk5: pointer loop at 1440 light: Start review, Keep in notes, Accept x2, Edit entry-3 + Save, Dismiss entry-5, Undo, Export",
  "walk6: export panel at 1440 light and 390 dark; Copy letter -> confirm -> Copy anyway; clipboard read; one-line layout; notes saved to export-notes.txt",
  "walk7: keyboard-only journey at 1440 dark: Tab to name, type, paste, Analyze, Tab to Start review, 8 x a, k to entry, e, Meta+Enter, d, k, r, Shift+Tab to Export (92), Copy letter",
  "walk8/9: keyboard skip link, j/k, e + Meta+Enter save on entry-5, d on entry-6, r reset, ? sheet; live-region text logged; API read of the case afterwards",
  "walk10: phone 390 light and dark: name + Use the sample case + Analyze, accept, edit + save, dismiss, Export; tap-target sizes; header tools",
  "walk11: empty submit, text without record markers, 71,440-char oversize, forced 500 on create, forced 500 on case list (1440 light, 390 dark)",
  "walk12: overview with 5 cases in 4 modes; keyboard open from the list; counts on header, Case checks, overview row",
  "walk13: measured source-pane top vs sticky header, excerpt clipping on charge and entry rows, dark input and progress colours",
  "walk14: I compared it with the quote on the edited entry; letter contains the edited wording",
  "walk15: create-form position and Tab count with 5 cases",
  "read docs/UI_DESIGN_BRIEF.md, research/ui-references.md, personas/ux-designer.md, D-063; git grep of copy strings at 95ffe36",
  "server stopped by PID 23700; port 7966 then returned 000"
 ],
 "verdict": "changes",
 "scores": {"design_quality": 3, "originality": 3, "craft": 2, "functionality": 3},
 "findings": [
  {"severity": "major", "title": "P0 F1: No New case action; the create form sits below the case list",
   "evidence": "walk15.out: create form y 1015 at 1440x900 and y 2027 at 390x844 with 5 cases; 12 / 11 Tabs to the name field; no visible button matching New case or Create. artifacts/review-evidence/mvp-audit/17-overview-5cases-light-1440.png, 17-overview-5cases-light-390.png",
   "why_it_matters": "Creating a case is step 2 of the core journey and is undiscoverable once a firm has a handful of cases (recognition over recall).",
   "fix": "overview.js / index.html: add a primary New case button in the Cases card header (right of the Showing N of N count) that scrolls to and focuses #case-title; rename the Records heading of #view-input to New case.",
   "acceptance_test": "With 5 cases at 1440x900 and 390x844 a New case button is in the first viewport; Enter on it puts focus in the case-name field."},
  {"severity": "major", "title": "P0 F2: Case header wraps to two rows at 1440 and covers the source-pane heading",
   "evidence": "05-case-top-light-1440.png (header 89 px, Export on row 2 at left, Source record heading cut). walk13.out: pane position fixed top=100px, heading Source record at 113-133 px, header bottom 121 px, header z-index 20, same at scrollY 0 and 2000, light and dark",
   "why_it_matters": "The header and the record pane are on screen for the whole review; a wrapped toolbar and a half-hidden pane title read as unfinished and hide which record is shown.",
   "fix": "styles.css .app-header-row: one row, flex-wrap nowrap; case name max-width ~28ch with ellipsis and title attribute; progress text shortened to '4 of 23 decided · 2 to review' (full sentence stays in the live region); badge, Shortcuts, Theme grouped right or in an overflow menu. sidebyside.css: pane top = var(--chrome-h) + 8px, set by a ResizeObserver on header.app-header in app.js.",
   "acceptance_test": "At 1440x900 on the case named 'Rivera v. Northgate (MVA 2026-01)' with an edit to check, header height <= 60 px and the pane heading top >= header bottom + 8 px at scrollY 0 and 2000."},
  {"severity": "major", "title": "P0 F3: Excerpts are clipped mid-sentence; the $2,150 charge row hides its own amount",
   "evidence": "06-charges-light-1440.png and 06-charges-light-390.png: $2,150 quote shows '…correlate clinicall…' with a sliver of the yellow mark under 'may'. walk13.out: amount-$2,150 CLIPPED (full text ends 'Charge: $2,150.'), 4 of 9 entry excerpts CLIPPED. review.css:59 line-clamp 2 on .rv-c-src .rv-quote; styles.css:154, 163, 209 clamp excerpts to 1-2 lines; the only reveal is the More link, fifth link in the row",
   "why_it_matters": "The paralegal verifies a dollar figure against its own line; when the line is cut she has to open the record, which is the slow path this product exists to remove. The brief (7.3) forbids mid-sentence truncation of the quote.",
   "fix": "review.css:59: drop the clamp for charge quotes and render the sentence that contains the mark (window around it, as the $6,240 row already does). styles.css: no clamp on pending or needs-review entry excerpts; keep a 1-line clamp only for decided rows, with a 'Show full excerpt' button directly under the quote instead of More in the link row.",
   "acceptance_test": "Every [data-testid^=amount-] quote has scrollHeight <= clientHeight and its <mark> inside the box; no pending entry .excerpt has scrollHeight > clientHeight at 1440 and 390."},
  {"severity": "major", "title": "P0 F4: An edit lands in a 'second check failed' state and asks her to compare with a quote that is cut off",
   "evidence": "08-edit-saved-light-1440.png, 15-phone-edit-saved-light-390.png: after Save the row shows '▲ The second check failed (the AI check was asked and gave no usable answer)…', Needs review, Do this first repeats it, the button is 'I compared it with the quote' and the excerpt beside it is clamped to one line. Edit = Edit + Save + I compared it = 3 actions (persona threshold: 2). export-notes.txt: '(edited; second check not available (JUDGE_UNAVAILABLE); …'. Copy source app/backend/why.py:49 JUDGE_FAILED, app/backend/export.py:611",
   "why_it_matters": "The hosted demo runs this backend, so every edit a viewer makes looks like a failure, and the compare step asks for verification without showing the full quote (calibrated trust, efficient correction).",
   "fix": "Frontend (review.js / styles.css): in the edit-to-check state un-clamp the excerpt and show 'Your wording' above 'Quote' with differences marked; one button 'Matches the quote, accept'. Backend copy only, no feature: why.py:49 for JUDGE_UNAVAILABLE reads 'The second check is not available right now. Compare your wording with the quote, then accept.'; export.py:611 drops the reason codes in parentheses.",
   "acceptance_test": "On the fixture backend after Save the row shows the full quote, does not contain the word failed, and one click puts the edit in the letter; the notes export contains no all-caps reason codes."},
  {"severity": "major", "title": "P0 F5: Dismiss makes the row vanish and moves focus off-screen; undo is elsewhere",
   "evidence": "walk5.out click 7: focus on 'Dismissed' at y 1033 in a 900 px viewport; walk10.out: y 1959 in an 844 px viewport at 390. 09-after-dismiss-light-1440.png (Rec 5 gone between Rec 4 and Rec 6 with no trace), 15-phone-after-dismiss-light-390.png. Row moves into 'Dismissed (n)' (review.js RV.dismissedBox). Brief 7.5 asks for an inline Undo in the row",
   "why_it_matters": "No feedback at the point of action and the undo lives in a group she cannot see; user control and freedom, visibility of system status.",
   "fix": "review.js (RV.act dismiss path): keep a one-line placeholder in the row's slot for 6 s, 'Dismissed: Capital PT, visit 8 · Undo'; pointer focus goes to that Undo, keyboard focus to the next item; then collapse into the group. Never focus an element outside the viewport (scrollIntoView block nearest).",
   "acceptance_test": "After Dismiss at 1440 and 390 the focused element is inside the viewport and an Undo control is visible where the row was; Undo restores the row in place."},
  {"severity": "major", "title": "P0 F6: Keyboard review dead-ends: a stops at the end of a flag group, no next-anywhere key, Export is 92 Shift+Tabs away",
   "evidence": "walk7.out: from Start review 8 x a; presses 1-5 decided items, presses 6-8 did nothing (focus stayed on flag-f_r9_1, progress stayed 5 of 23) while 18 items were open; Export reached after 92 Shift+Tab; after Enter on Analyze focus fell to BODY, then 13 Tabs to Start review. review.js:118-130 planAdvance stays inside one group; KEYS (review.js:436) has no n and no export key (brief 9 lists n). 12-kbd-after-8a-dark-1440.png",
   "why_it_matters": "The expert user lives on the keyboard; dead keys and a 92-key trip to Export make the keyboard path slower than the mouse (accelerators).",
   "fix": "review.js: at the end of a group, a and d keep the same-group rule for deciding but then move focus to the next group's first open item and announce it ('Causation flags done. Next: Charges, $185 rate'), without deciding it. Add n = RV.focusFirstPending from any item and x = focus btn-export; add both to the ? sheet. input.js: when a run finishes, focus btn-start-review.",
   "acceptance_test": "A Playwright run from Start review using only a, d and n decides all 23 items with no no-op key; x reaches Export from any row; after Analyze document.activeElement is btn-start-review."},
  {"severity": "major", "title": "P0 F7: Test and developer wording on the paralegal's screens and in the paste-out notes",
   "evidence": "Header chip 'cached demo (curated responses)' on every screen (01-landing-empty-light-1440.png; app.js:11). Amber box between timeline and flags: 'These numbers come from an older version of the AI prompts. What changed / Verified items matched the record 84/85 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)' (06-tray-light-1440.png; suggestions.js:138). export-notes.txt '(JUDGE_UNAVAILABLE)' (export.py:611). Case-list error '(the server answered 500). Request failed' (16-err-list500-light-1440.png; overview.js:194). 'Audit' link on every row and card",
   "why_it_matters": "Terminology must match the user's world (checklist 18); an amber warning with no action about 'older prompts' undercuts trust in a 3-minute demo, and codes in the notes get pasted into the file.",
   "fix": "app.js: badge text 'Demo: recorded AI answers' (tooltip explains) or hide outside local mode. suggestions.js: move the calibration block into the How the AI was checked disclosure, collapsed, reworded 'In testing on 10 synthetic cases, 84 of 85 verified items matched the record'; show the stale-prompts note only in ZLAYT_MODE=local. export.py:611: plain phrases only. overview.js:194: 'Couldn't load your cases. [Try again]'. Move per-row Audit into the Why this status dialog.",
   "acceptance_test": "The rendered text of the overview, case page and both exports contains none of: fixture, golden, prompt, JUDGE_, FIXTURE_, server answered, Request failed."},
  {"severity": "minor", "title": "P1 F8: Do this first and Start review point at different items",
   "evidence": "05-case-top-light-1440.png 'Do this first: This figure is a rate, not a charge…' (amount a2 in Charges); walk5.out click 1: Start review focused flag-f_r7_1 (Causation). 07-start-review-light-1440.png",
   "why_it_matters": "Two different 'first' instructions on one panel; she cannot tell which to follow.",
   "fix": "review.js RV.focusFirstPending: start from case.next_action.item_id when present; label the button 'Start review: $185 rate (Charges)'.",
   "acceptance_test": "After Start review, document.activeElement's data-item-id equals case.next_action.item_id."},
  {"severity": "minor", "title": "P1 F9: Counts and state names disagree across surfaces",
   "evidence": "walk12.out (Rivera): overview chip 'Can export — 18 not reviewed', Case checks 'Ready to export, 19 not reviewed', export count '19 items pending' (walk5.out); walk9.out after an edit save: header '6 of 23 decided' (17 open) while the live region says '16 left to review'. Filter 'Ready to send', chip 'Can export', Case checks 'Ready to export'. 17-overview-5cases-light-1440.png, 08-edit-saved-light-1440.png",
   "why_it_matters": "Visibility of system status depends on one trustworthy count; three names for one state make her wonder if they differ.",
   "fix": "One open-count helper in state.js (pending + edits to check) used by overview.js:39, stepper.js:587, the review.js live message and the export count line; one name 'Ready to export' (rename the filter).",
   "acceptance_test": "On a case with 1 edit to check, header, overview chip, Case checks, live region and export line show the same open count."},
  {"severity": "minor", "title": "P1 F10: 'checked 18, all agreed with the draft' beside 'second check failed'",
   "evidence": "walk12.out Rivera case overview text: 'How the AI was checked / checked 18, all agreed with the draft' in the same block as 'Do this first: The second check failed…'. judges.js:134",
   "why_it_matters": "Claims more than the record supports (checklist 20).",
   "fix": "judges.js:134: report agreed and not available separately ('checked 18 · 17 agreed · 1 not available').",
   "acceptance_test": "With one edit whose second check did not run, the summary does not say 'all agreed'."},
  {"severity": "minor", "title": "P1 F11: Rows carry too many controls",
   "evidence": "walk3 entry1_buttons: Accept, Edit, Dismiss, Why this status, Open record, Audit, Change quote, More (8); flag cards: Accept, Edit note, Dismiss, Dismiss with reason…, Open records 6 and 7, Why this status, Audit (06-flags-light-1440.png); entry-1 height 138 px at 1440, 310 px at 390 (05-case-top-light-1440.png)",
   "why_it_matters": "Visual noise slows the scan of twenty-plus decisions; two dismiss paths invite hesitation.",
   "fix": "timeline.js / review.js / flags.js: visible = Accept, Edit, Dismiss, Open record; Why this status, Change quote and Audit go into one More actions menu; Dismiss opens an optional reason field after dismissing instead of a second link.",
   "acceptance_test": "<= 5 visible controls per entry row and flag card; entry row <= 220 px tall at 390."},
  {"severity": "minor", "title": "P1 F12: Undo / r on an edited row discards her wording without asking",
   "evidence": "walk9.out: r on entry-5 after the edit -> 'Reset: Capital PT, visit 8'; API read afterwards: e5 summary 'Pain 4/10, improving.', edited null. Same reset sits behind the Undo button on edited rows (08-edit-saved-light-1440.png). 14-kbd-entry-edit-saved-dark-1440.png",
   "why_it_matters": "One stray key destroys typed work with no redo (error prevention).",
   "fix": "review.js reset path: on an edited item ask inline 'Discard your wording? [Discard] [Keep]', or keep the wording as a draft that Edit restores.",
   "acceptance_test": "Pressing r on an edited row leaves the summary unchanged until a second confirm."},
  {"severity": "minor", "title": "P1 F13: One very long page; gap flag and Export far down",
   "evidence": "walk3: document 6,813 px at 1440 and 11,693 px at 390; gap flag y 2,192 / 4,065 (checklist 19). walk6/walk10: Export opens at the bottom and the page grows to 9,339 / 16,717 px with no way back but scrolling. 06-gapflag-light-1440.png, 11-export-top-light-1440.png",
   "why_it_matters": "Wayfinding cost on every section switch; the key adverse fact (73-day gap) is three screens down.",
   "fix": "Sticky section nav under the header (Timeline 9 · Flags 10 · Charges 4 · Export) with scroll-spy; Export view gets a 'Back to review' link that returns focus to the last item.",
   "acceptance_test": "From any scroll position one action reaches Flags, Charges or Export; the gap flag is reachable in one action at 1440 and 390."},
  {"severity": "minor", "title": "P1 F14: Overview rows are heavy and an abandoned sample leaves a ghost case",
   "evidence": "17-overview-5cases-light-1440.png: about 190 px per analyzed row, the same 4-line paragraph '1 edit is still marked Needs review…' on three rows, an 'Analysis done' chip on every row; row 3 'Phone light-390 - Rivera sample · Not analyzed yet' was created when Use the sample case showed its preview and I left (15-phone-sample-preview-light-390.png); two rows share one name",
   "why_it_matters": "The overview should answer 'which case needs me' at a glance; ghost and duplicate rows erode that.",
   "fix": "overview.js: show only non-normal chips (drop Analysis done), replace the paragraph with a chip '1 edit to compare', target row height <= 96 px at 1440; input.js: do not persist a case until Analyze, or list it as Draft with Delete; warn on a duplicate name.",
   "acceptance_test": "5 cases fit in 900 px at 1440; leaving the sample preview creates no case."},
  {"severity": "minor", "title": "P1 F15: Error messages lack the next step",
   "evidence": "walk11.out: forced 500 on create -> 'Request failed' (16-err-create500-light-1440.png); text without record markers -> 'This demo only runs the recorded sample cases.' (16-err-nomarkers-light-1440.png, api.py:257); case-list 500 -> '(the server answered 500). Request failed Try again'. Pasted text kept in every case",
   "why_it_matters": "Errors must say what to do next (NN/g error-message guidelines).",
   "fix": "input.js: 500/network -> 'We couldn't start the analysis. Your text is still here. [Try again]'; demo_mode_unsupported_input -> 'The demo runs only the sample and the synthetic cases. [Use the sample case] [Add a synthetic case]'.",
   "acceptance_test": "Each input error shows one action button and no HTTP status or 'Request failed'."},
  {"severity": "minor", "title": "P1 F16: 'Add a synthetic case' looks broken and repeats on every case page",
   "evidence": "01-landing-empty-light-1440.png (summary text flush to the left border, no padding, no chevron); 06-bottom-light-1440.png (same bar at the bottom of the case page). switcher.js:46",
   "why_it_matters": "An unstyled control is the first thing that reads as unfinished; on the case page it is out of context.",
   "fix": "switcher.js / styles: style the details as a card (16 px padding, chevron, one helper line); render it only on the overview.",
   "acceptance_test": "Not present in case view; summary padding >= 12 px with a visible disclosure marker."},
  {"severity": "minor", "title": "P1 F17: The case top is chrome-heavy and repeats counts",
   "evidence": "walk3: queue starts at y 552 at 1440 and y 762 at 390; above it: Records bar, Case overview bars, Do this first, 2 chips, a sentence, 5 jump buttons, Case checks, How the AI was checked, 3 Timeline chips, batch button, order select. Timeline chip '3 items need review' sits over nine Quote-matches rows. 05-case-top-light-1440.png, 05-case-top-light-390.png",
   "why_it_matters": "Hierarchy: the work (the first item) should be in the first screen.",
   "fix": "stepper.js / timeline.js: merge Case checks and How the AI was checked into one 'Checks' line, drop the Timeline chips that repeat header counts (or scope them to the timeline), keep one Start review.",
   "acceptance_test": "Queue top <= 400 px at 1440 and <= 560 px at 390; the Timeline chip count equals timeline needs-review rows."},
  {"severity": "nit", "title": "P2 F18: Empty overview shows filters, search and sort at zero; empty text has no buttons",
   "evidence": "01-landing-empty-light-1440.png: 'All cases (0) Needs attention (0) Ready to send (0)', Search, Sort above 'No cases yet. Paste records below, or add a synthetic case.'",
   "why_it_matters": "Empty states should offer the next action (brief 8).",
   "fix": "overview.js: hide filters/search/sort when there are no cases; empty state with two buttons, New case and Open the sample case.",
   "acceptance_test": "With 0 cases no filter chips render and two action buttons are visible."},
  {"severity": "nit", "title": "P2 F19: Case name field too narrow; placeholder cut",
   "evidence": "01-landing-empty-light-1440.png: about 180 px field, placeholder shows 'Client or matter, for exa'",
   "why_it_matters": "Craft; matter names are long.",
   "fix": "styles.css: #case-title width 100%, max-width 48ch.",
   "acceptance_test": "Placeholder fully visible at 1440 and 390."},
  {"severity": "nit", "title": "P2 F20: Dark mode search input and progress track mismatch",
   "evidence": "walk13.out: search background rgb(59, 59, 59) vs rgb(21, 26, 33) for the name, text and sort fields; progress track rgb(28, 34, 43) on panel rgb(21, 26, 33), invisible at 0 (17-overview-5cases-dark-1440.png)",
   "why_it_matters": "Consistency and legible progress in dark mode.",
   "fix": "overview.css: input[type=search] appearance none, background var(--panel), border var(--border-strong); progress track var(--border-strong).",
   "acceptance_test": "All overview inputs share one background in dark; progress track contrast >= 3:1 against the panel."},
  {"severity": "nit", "title": "P2 F21: The $185 rate row gives two reasons",
   "evidence": "06-unclear-light-1440.png: 'Not counted: a rate, not a bill. rate $185/visit; visit count not stated…' and a second box 'This figure is a rate, not a charge, so it is not added to the total.'",
   "why_it_matters": "Duplicate text in the densest table.",
   "fix": "charges.js: show the reason once.",
   "acceptance_test": "The unclear rate row has one reason line."},
  {"severity": "nit", "title": "P2 F22: Row links are 36 px tall at 390",
   "evidence": "walk10.out: Why this status 111x36, Open record 94x36, Audit 50x36, Change quote 103x36, More 49x36 (brief 3: 44 px at <= 768 px). Severity deferred to accessibility-reviewer. 15-phone-entry1-light-390.png",
   "why_it_matters": "Touch accuracy on phone.",
   "fix": "styles.css @media (max-width: 768px): min-height 44px on row links.",
   "acceptance_test": "All row controls >= 44 px tall at 390."},
  {"severity": "nit", "title": "P2 F23: No theme toggle at 390",
   "evidence": "walk10.out header tools: btn-theme hidden (0x0) at 390, light and dark; 15-phone-case-top-light-390.png",
   "why_it_matters": "User control on phone.",
   "fix": "Put Theme (and Shortcuts) in a header overflow menu at <= 768 px.",
   "acceptance_test": "Theme can be changed at 390."},
  {"severity": "nit", "title": "P2 F24: Unclear 'Not in an entry (1)' label; UI-added leading ellipsis",
   "evidence": "05-case-top-light-1440.png 'Not in an entry (1)' beside Rec 3; 06-charges-light-1440.png $6,240 quote starts '… Rx cyclobenzaprine'",
   "why_it_matters": "Information scent; brief 7.3 says the UI never ellipsizes a quote.",
   "fix": "Label '1 line not in the chronology'; show the full sentence instead of a UI ellipsis.",
   "acceptance_test": "No quote element starts or ends with a UI-inserted ellipsis."}
 ],
 "whats_right": [
  "The source pane highlights the exact excerpt inside the full record for the selected item (08-edit-open-light-1440.png).",
  "Input errors are inline, plain and keep the pasted text (71,440 chars kept on oversize; full sample kept on a forced 500).",
  "Export pastes cleanly with citations, Copy asks first and names what is unreviewed, and a confirmed edit reaches the letter (export-letter-two-line.txt, walk14.out)."
 ],
 "questions_for_chris": [
  "The hosted demo runs recorded AI answers, so every edit has no second check. Should the demo record a second-check reply for edits so viewers see the normal path, or is the plain 'not available, compare it yourself' wording (F4) enough?"
 ]}
```
