# T-166 MVP UX audit, round 2: the same journey on the polished build

Reviewer: ux-designer-reviewer (Priya Raman persona), model claude-opus-5-5. Date 2026-11-02.
Build: `git archive 63f0a49` (HEAD at start; contains T-149 f7a8f2a and T-167 da6afb2, checked with `git merge-base --is-ancestor` → `ancestors-ok`). Served from scratch on 127.0.0.1:7967 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a fresh scratch `ZLAYT_DB` (`/api/cases` → `{"cases":[]}` at start). HEAD moved to d865d21 during the review (T-171/T-172/T-173: amounts.py, present.py, charges.js). I re-checked only the charges panel at d865d21, on port 7968; F21 and F3 read the same there.
Evidence: `artifacts/review-evidence/mvp-audit-r2/` holds the scripts `r2w1..r2w10*.py`, their raw output `r2w*.out`, the screens `NN-*.png`, and the pasted exports `export-*.txt`.

**Verdict: pass.** All seven P0s are closed. Measured results:
- New case sits in the first screen.
- The header is one row (56 px) and the source pane starts below it.
- No quote is clipped.
- Edit then "Save and accept" takes 2 clicks, and the copy no longer says "failed".
- Dismiss leaves an Undo in the row's own slot.
- 23 presses of `a` decide all 23 items with no dead key.
- No test or developer wording remains on the screens.

What remains is 13 minor and nit items, partial or open, plus 3 new minors. None of them breaks the review loop.

Scores: design quality 4, originality 3, craft 3, functionality 4.

## Status of the 24 round-1 findings
| # | Was | Now | Evidence (r2) |
|---|---|---|---|
| F1 New case | P0 | **fixed** | "New case" primary button at y 121 (1440) / 179 (390), also with 12 cases. 2 Tabs, then Enter, puts focus in `input-title`. The form heading reads "New case" (r2w1.out, r2w7.out, 01-empty-*, 17-overview-many-*, 17-new-case-focus-light-1440) |
| F2 Header wrap | P0 | **fixed** | Header 56 px on one row with Export on the same row. Pane top 100 ≥ header bottom 88 + 8, at scrollY 0 and 2000, light and dark. At 390 the name is ellipsized and there is no horizontal scroll (r2w2.out, 05-case-top-*) |
| F3 Clipped quotes | P0 | **fixed** | 0 of 9 entry excerpts clipped. All 4 charge quotes are full with their mark; $2,150 reads "…correlate clinically. Charge: $2,150." This holds at 1440 and 390, light and dark, and at d865d21. Decided rows keep a single line with "Show full excerpt" under the quote (r2w2.out, 06-charges-*, r2w10 output) |
| F4 Edit state | P0 | **fixed** | Edit, then Save and accept = 2 clicks, and the row reads "Compared by you · Accepted". Save-only reads "The AI second check is not available in this demo…" with the quote not clipped, and nothing says "failed". The notes contain no reason codes (r2w3-*.out, 08-edit-saved-accepted-*, 08-edit-saved-tocheck-*, export-notes-*.txt). The keyboard residual is filed as N1 |
| F5 Dismiss | P0 | **fixed** | A placeholder "Dismissed: Capital PT, visit 8, February 20, 2026 · Undo" sits at the row's own y (790 at 1440, 380 at 390). Focus goes to that Undo, inside the viewport. Undo restores the row at the same y. After 6 s focus is on entry-6, still in view. Keyboard `d` behaves the same (r2w3-*.out, r2w5.out, 09-after-dismiss-*). One e2e flake is filed as N3 |
| F6 Keyboard loop | P0 | **fixed** | From Go to it, 23 presses of `a` decide 23 of 23 with 0 no-ops. Each list end announces the next, e.g. "Timeline done. Next: Treatment gaps, Gap of 73 days". The last press lands on Export with "Nothing left to decide. Export is next." `n` and `x` work and are listed in `?`. `x`, Enter, 2 Tabs reaches Copy letter (r2w4.out, r2w5.out, r2w6.out, 14-kbd-shortcuts-dark-1440). Sub-item still open: after Analyze, focus sits on the 0-px skip nav, not on Start review. Filed under F8 (minor), because Tab then Enter on the skip link enters the list in 2 keys |
| F7 Dev wording | P0 | **fixed** | The chip reads "Demo: recorded AI answers". A body-text scan finds none of fixture, golden, JUDGE_, curated, "server answered" or "Request failed". The calibration line reads "In testing on 10 synthetic cases, 82 of 83 verified items matched the record.", with the raw sentence behind Technical detail. Audit has moved under More plus one section at the page bottom. A list error reads "We could not load your cases… [Try again]" (r2w1.out, r2w2b output, 06-tray-*, 16-err-list500-*) |
| F8 Two "firsts" | P1 | **partial** | Start review and Do this first now both go to $185 (focus `amount-$185`). The skip link "Skip to the first item to review" and `n` go to flag-f_r7_1 "Accident date source" instead (r2w5.out [2], [3]; r2w6.out [2]) |
| F9 Counts / names | P1 | **partial** | Header, live region and export line agree: 19 open. The Case-checks chip says "Can export — 18 not reviewed" because it leaves out the edit to check. The filter is still "Ready to send" while the chip says "Can export" (r2w8.out, r2w3-light-1440.out COUNTS) |
| F10 "all agreed" | P1 | **fixed** | "17 checked, 17 agreed with the draft, 2 edited by you, second check not available" (r2w8.out) |
| F11 Row controls | P1 | **fixed** | 5 visible controls per entry row and flag card (Accept, Edit, Dismiss, Open record, More). I withdraw the ≤220 px row height at 390 (it is now 322 px), because F3's rule of no clipping outranks it (r2w2.out) |
| F12 Undo discards wording | P1 | **fixed** | Undo or `r` on an edited row asks "Discard your wording?" with Keep focused. Enter keeps the wording (r2w3-*.out [11]–[12], r2w6.out [22]–[23], 10-undo-edited-confirm-*) |
| F13 Long page | P1 | **open** | The page is 6,752 / 10,975 px with the gap flag at y 2,153 / 3,883. There is no sticky section nav. The Export view offers only Copy letter, Download, Copy notes and Download, with no Back to review (r2w2.out, r2w3-light-1440.out) |
| F14 Heavy rows, ghost case | P1 | **partial** | Rows at 1440 are 90 to 191 px (were ~190). "Analysis done" is still on every row. Leaving the sample preview still creates a case: 11 → 12 cases, "Ghost check - sample preview · Not analyzed yet" (r2w7.out, 17-overview-many-*) |
| F15 Errors lack next step | P1 | **partial** | The case-list 500 has a Try again button. A create 500 shows "Something went wrong. Try again." with no button (text kept, 1,879 chars). No markers gives "This demo only runs the recorded sample cases." with no action (r2w7.out, 16-err-*) |
| F16 "Add a synthetic case" | P1 | **open** | `summary` padding-left 0px, and it is still shown at the bottom of the case page (r2w1.out, r2w9 output, 06-bottom-light-1440) |
| F17 Chrome above queue | P1 | **partial** | Queue top is y 519 / 617 (was 552 / 762; targets 400 / 560). The Timeline chip "3 items need review" sits over 9 rows that are all `verified` (r2w2.out timeline row states) |
| F18 Empty overview | P2 | **open** | At 0 cases the filters, search and sort still show, and the text "No cases yet. Paste records below, or add a synthetic case." has no buttons. New case in the card header helps (01-empty-light-1440) |
| F19 Name field | P2 | **fixed** | The placeholder is now "Client or matter" and fits (scrollWidth not > clientWidth). The field is still 180 px |
| F20 Dark search / track | P2 | **open** | Search is rgb(59, 59, 59) against rgb(21, 26, 33). The progress track is still rgb(28, 34, 43) (r2w7.out, 17-overview-many-dark-1440) |
| F21 Rate row two reasons | P2 | **open** | "Not counted: This figure is a rate…" and "Not counted: a rate, not a bill. rate $185/visit…" both appear, at 63f0a49 and at d865d21 (06-charges-light-1440, 19-d865-rate-row-light-1440) |
| F22 36 px links at 390 | P2 | **partial** | Buttons are 44 px. Open record and More are 36 px; "Not in an entry (1)" is 24 px. Severity is deferred to accessibility-reviewer (r2w2.out) |
| F23 Theme at 390 | P2 | **open** | `btn-theme` is 0×0 at 390 (r2w1.out, r2w2.out) |
| F24 Label / ellipsis | P2 | **partial** | The UI ellipsis on $6,240 is gone ("ER charges: $6,240."). The "Not in an entry (1)" label is unchanged |

Tally: 11 fixed, 7 partial, 6 open.

## New (minor)
- **N1 Keyboard edit costs 4 keys and the edit copy repeats itself.** `e`, then Meta+Enter (Save only), then `a`, then Enter on "I compared it with the quote" (r2w6.out [15]–[20]). The pointer path is 2 clicks. The Save-only note ends "…Compare the summary with the quote yourself; if they match, accept it. Until you do, the item stays marked for review. Compare it with the quote yourself." (08-edit-saved-tocheck-light-1440). An open edit form also shows Accept beside Save and accept (08-edit-open-light-1440).
- **N2 A finished edit still reads as a warning.** The accepted, edited row carries an amber "▲ Compared by you with the quote. The second AI check did not run." (08-edit-saved-accepted-light-1440). The Case overview says the edit is pending because "the second check did not confirm it", but in the demo the check never ran (r2w8.out).
- **N3 The e2e for focus after a charge dismiss is flaky.** Full run 1 of `tests/e2e/test_mvp_polish.py` against my server: `1 failed, 24 passed in 43.42s` (FAILED `test_dismissing_a_flag_and_a_charge_leaves_a_placeholder_in_their_panels`, AssertionError at :186, the focus-in-view check after the charge dismiss). Full run 2: `25 passed in 42.90s`. Alone, 3 of 3 runs gave `1 passed, 24 deselected`.

## As the designer: is this a finished, polished MVP a PI firm could pilot?
**Pilot: yes. "Finished": not quite.** A paralegal can now do the whole job without the tool fighting her:
- Name and paste the records.
- Review with the source beside every item.
- Correct an item in 2 clicks.
- Undo where she acted.
- Clear the queue by keyboard.
- Paste a clean, cited letter.

None of the remaining items loses work or misleads her about what goes into the letter. What still reads unfinished in a 3-minute demo or a first week of use, in order:
1. One "first item" and one open count everywhere: the skip link and `n` should match Do this first, focus should go there after a run, and the chip should agree with the header (F8, F9).
2. No ghost case when she backs out of the sample preview (F14).
3. Every error gets one action button (F15).
4. Clean up the unstyled "Add a synthetic case" bar on the case page and the grey search box in dark mode (F16, F20).
5. One reason line per not-counted amount (F21).
6. A section nav and a "Back to review" link from Export (F13).

## What is right (keep)
- Dismiss leaves an Undo in the row's own place, and the row comes back where it was (09-after-dismiss-light-390).
- `a` walks the whole case, announcing each list it moves to, and stops on Export (r2w4.out).
- A quote is never clipped while the item needs a decision, and every charge shows the sentence that holds its amount (06-charges-light-1440).

## Probe notes
- Scratchpad trap: `r2.sqlite3` already existed from an earlier session and held 6 cases. I restarted the server on a new DB name and discarded the first r2w1 run.
- r2w4: after the `a` loop, focus was on Export, where letter keys are inert by design. My `k`, `r`, `e` and `x` presses there were no-ops. Ignore r2w4 from [45] on. r2w5 likewise lost state: `goto` to the same hash URL did not reload, and a source dialog swallowed keys. The keyboard edit results come from r2w6.
- Timings are from scripts. The pointer loop took 12 clicks in 19.3 s. The keyboard path from landing took 12 Tabs + Enter + 23 × `a` = 36 keys to decide everything.
- Servers stopped: PID 49474 (7967) and PID 63296 (7968); both ports then returned 000.

```json
{"card": "T-166", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive 63f0a49 (HEAD at start; includes f7a8f2a T-149 and da6afb2 T-167) served from scratch on http://127.0.0.1:7967, LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, fresh scratch ZLAYT_DB; charges panel re-checked at d865d21 on :7968 after HEAD moved; sample case evals/golden/sample.txt; overview -> create+name -> open -> review -> edit+dismiss -> export at 1440x900 and 390x844, light and dark, pointer, touch and keyboard",
 "exercised": [
  "r2w1: empty overview in 4 modes (New case position, filters at 0, name field, synthetic bar padding, header chip, theme button size, bad-word scan); create by name + paste at 1440 light, processing text, focus after the run",
  "r2w2: case page in 4 modes: header height vs source pane at scrollY 0 and 2000, entry/charge quote clipping, controls per row/flag, tap targets at 390, queue top, page length, gap flag y, nav, bad-word scan; Start review target vs Do this first; section shots",
  "r2w2b/r2w2c: located visible Audit/prompt/testing wording; judge details closed by default",
  "r2w3 at 1440 light, 1440 dark, 390 light, 390 dark (touch): Start review, Accept x2, Edit + Save and accept, Edit + Save only, Dismiss + placeholder + Undo + re-dismiss + 7 s wait, Undo on edited row -> Keep, counts on every surface, Export, Copy letter (Copy anyway), Copy notes, code scan of notes",
  "r2w4: keyboard-only from overview: New case (2 Tabs), name, paste, Analyze, focus after run, 12 Tabs to Go to it, 23 x a to 23 of 23 decided with 0 no-ops, landed on Export",
  "r2w5/r2w6: skip link, n, x, Enter on Export, Tabs to Copy letter; keyboard edit e + Meta+Enter + a + Enter; r on edited row -> confirm, Enter keeps; d placeholder; ? sheet; letter carries the edit",
  "r2w7: empty, no markers, 71,440-char oversize, forced 500 on create and on the case list at 1440 light and 390 dark; ghost case from the sample preview; overview with 12 cases in 4 modes; dark search/progress colours",
  "r2w8: judge summary and count surfaces with 1 edit to check; r2w9: case-page bottom; r2w10: charges panel at d865d21",
  "pytest tests/e2e/test_mvp_polish.py against :7967: run 1 '1 failed, 24 passed', run 2 '25 passed', flaky spec alone 3 x '1 passed'",
  "read personas/ux-designer.md, reviews/MVP-ux-audit.md, board.py show T-166 handoff, git show --stat for 28437b2 9071912 46df34e 63f0a49 f7a8f2a da6afb2",
  "servers stopped by PID 49474 and 63296; ports 7967 and 7968 returned 000"
 ],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 3, "craft": 3, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "F8 partial (+ F6 sub-item): the skip link and n go to a different first item than Do this first; focus after a run is on the hidden skip nav",
   "evidence": "r2w2.out: Start review focuses amount-$185 = Do this first '$185 (record 4)'. r2w5.out [2]: 'Skip to the first item to review' focuses flag-f_r7_1; [3] n says 'First open item: Causation language, Accident date source'. r2w4.out: after Analyze focus is NAV skip-nav (h 0); 12 Tabs to Go to it",
   "why_it_matters": "Three different 'first' items erode trust in the guidance (recognition over recall, visibility of status).",
   "fix": "review.js: RV.focusFirstPending and the skip-review link start from case.next_action.item_id when present; input.js: when a run finishes, focus btn-start-review (btn-do-first on phone).",
   "acceptance_test": "After a run, document.activeElement is the Start review/Go to it button; Enter on it, Enter on the skip link and n from entry-1 all focus the item whose data-item-id equals case.next_action.item_id."},
  {"severity": "minor", "title": "F9 partial: the Case-checks chip leaves the edit to check out of its open count; Ready to send and Can export name the same state",
   "evidence": "r2w8.out: header '4 of 23 decided · 4 to review' (19 open), live 'First open item … 19 items are open', export '19 items pending', chip 'Can export — 18 not reviewed'. Overview filter 'Ready to send (1)' vs chip 'Can export' (17-overview-many-dark-1440.png)",
   "why_it_matters": "One trustworthy number is the core of visibility of system status.",
   "fix": "overview.js / stepper.js: use ZL.progressOf(c).left for the chip; rename the filter to 'Can export' (or the chip to 'Ready to send').",
   "acceptance_test": "With 1 edit to check, header, chip, overview row, live region and export line show the same open count; one state name across filter and chip."},
  {"severity": "minor", "title": "F13 open: one very long page; no section nav; no way back from Export",
   "evidence": "r2w2.out doc_h 6752 / 10975, gap_y 2153 / 3883; navs only skip-nav (absolute) and btn-gate-warning-jump. r2w3-light-1440.out export controls: Copy letter, Download .txt, Copy notes, Download .txt (no Back to review); doc 9,640 px with Export open",
   "why_it_matters": "Wayfinding on every section switch; the 73-day gap is three screens down (checklist 19).",
   "fix": "Sticky section nav under the header (Timeline · Flags · Charges · Export) with counts; Back to review in the Export view returning focus to the last item.",
   "acceptance_test": "One action reaches Flags, Charges or Export from any scroll position at 1440 and 390; Back to review is the first control in Export."},
  {"severity": "minor", "title": "F14 partial: leaving the sample preview still creates a case; Analysis done chip on every row",
   "evidence": "r2w7.out: 'cases before preview 11 after leaving preview 12', top row 'Ghost check - sample preview … Not analyzed yet'; row heights 90-191 px at 1440, 238-361 px at 390; 17-overview-many-dark-1440.png",
   "why_it_matters": "Ghost rows make the overview less trustworthy as the list of real work.",
   "fix": "input.js: do not persist a case until Analyze (or list it as Draft with Delete); overview.js: drop the Analysis done chip.",
   "acceptance_test": "Leaving the sample preview creates no case; no row shows Analysis done."},
  {"severity": "minor", "title": "F15 partial: create-500 and no-markers errors still have no action button",
   "evidence": "r2w7.out: create 500 -> 'Something went wrong. Try again.' with no button (text kept 1,879 chars); no markers -> 'This demo only runs the recorded sample cases.' with no button; case-list 500 now has Try again. 16-err-create500-light-1440.png, 16-err-nomarkers-light-1440.png",
   "why_it_matters": "Errors must offer the next step (NN/g error-message guidelines).",
   "fix": "input.js: create failure -> 'We couldn't start the analysis. Your text is still here.' + [Try again]; demo_mode_unsupported_input -> [Use the sample case] [Add a synthetic case].",
   "acceptance_test": "Each input error shows exactly one primary action button."},
  {"severity": "minor", "title": "F16 open: 'Add a synthetic case' is unstyled and still on the case page",
   "evidence": "r2w1.out synthetic_summary padding '0px'; r2w9 output [['Add a synthetic case', True, '0px']] on the case page; 06-bottom-light-1440.png",
   "why_it_matters": "The most visibly unfinished control, at the end of every case.",
   "fix": "switcher.js: render only on the overview; style as a card with 16 px padding and a disclosure marker.",
   "acceptance_test": "Absent from the case view; summary padding >= 12 px."},
  {"severity": "minor", "title": "F17 partial: queue still starts low; the Timeline chip counts items that are not in the timeline",
   "evidence": "r2w2.out entry1_y 519 (1440) / 617 (390) vs targets 400 / 560; Timeline chip '3 items need review' while timeline row states are 9 x 'verified' (05-case-top-light-1440.png)",
   "why_it_matters": "Hierarchy and information scent: the chip points at the wrong list.",
   "fix": "timeline.js: scope the chip to timeline rows (or drop it); merge Case checks and How the AI was checked into one line.",
   "acceptance_test": "Timeline chip count equals timeline needs_review rows; queue top <= 400 / 560 px."},
  {"severity": "minor", "title": "N1: keyboard edit is 4 keys while pointer is 2; Save-only note repeats itself; edit form shows Accept beside Save and accept",
   "evidence": "r2w6.out [15] e, [18] Meta+Enter -> data-review edited, [19] a -> focus 'I compared it with the quote', [20] Enter -> accepted. 08-edit-saved-tocheck-light-1440.png ('…if they match, accept it. Until you do, the item stays marked for review. Compare it with the quote yourself.'); 08-edit-open-light-1440.png (Accept, Edit, Dismiss above Save and accept, Save, Cancel)",
   "why_it_matters": "Accelerators: the expert keyboard path is slower than the mouse for the most common correction.",
   "fix": "review.js: Meta+Enter = Save and accept (Shift+Meta+Enter = Save only), list it in ?; drop the trailing duplicate sentence; hide the row's Accept/Edit while the edit form is open.",
   "acceptance_test": "e, type, Meta+Enter leaves the item accepted with the edit; the note has no repeated sentence; an open edit form shows one accept control."},
  {"severity": "minor", "title": "N2: an accepted edit still wears an amber warning; overview says the second check 'did not confirm it' when it never ran",
   "evidence": "08-edit-saved-accepted-light-1440.png: '▲ Compared by you with the quote. The second AI check did not run.' on an Accepted row; r2w8.out overview: '1 edit is still marked Needs review (the second check did not confirm it)'",
   "why_it_matters": "Calibrated trust: warning styling on a finished decision, and copy that says the check disagreed when it did not run.",
   "fix": "Accepted edited rows: neutral info line; stepper/overview copy: 'the second check did not run' in demo.",
   "acceptance_test": "No amber/▲ on an accepted row; the overview sentence matches the judge record."},
  {"severity": "minor", "title": "N3: e2e for focus after a charge dismiss is flaky",
   "evidence": "pytest tests/e2e/test_mvp_polish.py vs :7967 run 1: '1 failed, 24 passed in 43.42s' FAILED test_dismissing_a_flag_and_a_charge_leaves_a_placeholder_in_their_panels (AssertionError at :186, focus-in-view after the charge dismiss); run 2: '25 passed in 42.90s'; -k alone 3 x '1 passed, 24 deselected'",
   "why_it_matters": "Either focus sometimes leaves the viewport after a charge dismiss (F5 regression) or the gate is unreliable.",
   "fix": "Wait for the placeholder's Undo to be focused before measuring, or scrollIntoView block 'nearest' after the table re-renders.",
   "acceptance_test": "10 consecutive full runs of test_mvp_polish.py pass."},
  {"severity": "nit", "title": "F18 open: empty overview shows filters, search and sort; empty text has no buttons",
   "evidence": "01-empty-light-1440.png; r2w1.out visible_filters_search_sort 5 at 0 cases",
   "why_it_matters": "Empty states should offer the next action.",
   "fix": "overview.js: hide filters/search/sort at 0 cases; add Open the sample case beside New case.",
   "acceptance_test": "At 0 cases no filter chips render."},
  {"severity": "nit", "title": "F20 open: dark search input grey; progress track invisible at 0",
   "evidence": "r2w7.out dark: search_bg rgb(59, 59, 59) vs title_bg rgb(21, 26, 33); track rgb(28, 34, 43); 17-overview-many-dark-1440.png",
   "why_it_matters": "Consistency in dark mode.",
   "fix": "overview.css: search appearance none, background var(--panel); track var(--border-strong).",
   "acceptance_test": "All overview inputs share one dark background; track contrast >= 3:1."},
  {"severity": "nit", "title": "F21 open: the $185 rate row gives two Not counted reasons",
   "evidence": "06-charges-light-1440.png and 19-d865-rate-row-light-1440.png (d865d21): 'Not counted: This figure is a rate…' and 'Not counted: a rate, not a bill. rate $185/visit; visit count not stated…'",
   "why_it_matters": "Duplicate text in the densest table.",
   "fix": "charges.js: one reason line (the plain sentence; the detail in More).",
   "acceptance_test": "The rate row has one Not counted line."},
  {"severity": "nit", "title": "F22 partial: Open record, More (36 px) and Not in an entry (24 px) below 44 px at 390",
   "evidence": "r2w2.out light-390 small_targets: 'Open record 36', 'More 36', 'Not in an entry (1 24'; severity deferred to accessibility-reviewer",
   "why_it_matters": "Touch accuracy.",
   "fix": "styles.css @media (max-width: 768px): min-height 44px on row links.",
   "acceptance_test": "All row controls >= 44 px at 390."},
  {"severity": "nit", "title": "F23 open: no theme toggle at 390",
   "evidence": "r2w1.out / r2w2.out theme [0, 0] at 390",
   "why_it_matters": "User control on phone.",
   "fix": "Header overflow menu with Theme and Shortcuts at <= 768 px.",
   "acceptance_test": "Theme can be changed at 390."},
  {"severity": "nit", "title": "F24 partial: 'Not in an entry (1)' label unchanged",
   "evidence": "05-case-top-light-1440.png; r2w2.out entry_controls 'Not in an entr…' on entry-3",
   "why_it_matters": "Information scent.",
   "fix": "Label '1 line not in the chronology'.",
   "acceptance_test": "No 'Not in an entry' label."}
 ],
 "whats_right": [
  "Dismiss leaves an Undo in the row's own slot and Undo restores it in place (09-after-dismiss-light-390.png).",
  "a walks the whole case with list-to-list announcements and stops on Export: 23 presses, 23 decided, 0 dead keys (r2w4.out).",
  "No quote is clipped while undecided, and every charge shows the sentence that holds its amount (06-charges-light-1440.png)."
 ],
 "questions_for_chris": []}
```
