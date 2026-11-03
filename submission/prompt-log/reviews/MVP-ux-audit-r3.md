# T-174 MVP UX audit, round 3: the "finished" list, re-walked

Reviewer: ux-designer-reviewer (Priya Raman persona), model claude-opus-5-5. Date 2026-11-02.

**Build.** `git archive da0c7fe`. HEAD was da0c7fe at the start and still da0c7fe at the end (`git rev-parse --short HEAD` → `da0c7fe`).
- Served from scratch on 127.0.0.1:7969 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`.
- Fresh scratch `ZLAYT_DB` (`/api/cases` → `{"cases":[]}` at start).
- Server PID 3777, stopped by PID; the port then returned `000`.

**Evidence.** `artifacts/review-evidence/mvp-audit-r3/` holds:
- the scripts `r3w0..r3w5*.py`
- their raw output `r3w*.out`
- the screens `NN-*.png`
- the letters `export-letter-keyboard.txt` and `export-letter-lib11.txt`

**Verdict: changes.** Seven of the nine items are fixed: F8, F9, F13, F16, F20, F21 and the flaky spec. Two block "finished", and I map both to major:
- **F15 is partial.** The most likely error in the demo leads to a dead-end button.
- **The new "Count this charge" flow ends on a bad row.** It works, but the counted row is wrong: it gives a warning-styled "You confirmed this flag" for a flag she never saw, the same point twice, and a chip that overflows its cell at 1440.

Scores: design quality 4, originality 3, craft 3, functionality 4.

## Status of the "finished" items
| Item | Now | Evidence (r3) |
|---|---|---|
| F8 one first item | **fixed** | On the sample case, in all 4 modes, the skip link, `n` from entry-1 and Start review (Go to it at 390) all focus `a2` = "Do this first: $185 (record 4)" (r3w2.out `all equal do-first: True`). By keyboard it takes 2 keys from the end of the run to that item: Tab, then Enter on the skip link (r3w3.out [9]–[10]). Nit left over: after a run, focus sits on the 0-px `skip-nav`, so nothing on screen shows focus until the first Tab |
| F9 one count | **fixed** | With 1 accepted, 1 edit to check and 1 dismissed, every surface reads 21 open: header "2 of 23 decided · 4 to review", Case-checks chip, summary gate, live region on `n`, export line, nav (8 + 10 + 3), server `pending 20 + edits_to_check 1`, and the list row. Need-review reads 4 everywhere. The filter now reads "Everything decided" (r3w2.out F9 COUNTS, r3w5.out ROW lines) |
| F14 no ghost case | **partial** | Leaving the preview by All cases leaves no case (2 → 3 → 2). Leaving by reload, or by browser Back out of the app, keeps the case: "Ghost check reload-root" and "Ghost check history-back" are listed as "Not analyzed yet". They also count toward "Needs attention (11)" (r3w1.out GHOST lines, r3w5.out ROW lines, 17-overview-many-light-1440.png) |
| F15 every error has an action | **partial (major)** | Each error now has one button: empty → Use the sample case; oversize → Edit the text (71,440 chars kept, focus goes to the textarea); create 500 → "We couldn't start the analysis. Your text is still here." + Try again (1,879 chars kept); PDF → Choose a .txt file; case list 500 → Try again. **But** a real paste that is not a recorded case is refused at create, and the box then shows "This demo only runs the recorded sample cases. **Edit the text**" (r3w1.out `[no markers real]`, 16-err-nomarkers-light-1440.png). No edit can make that run. The "Use the sample case" mapping exists only on the /run path (input.js:124). The create path falls through to `toText()` (input.js:39). The e2e passes only because it stubs `**/api/cases/*/run` (tests/e2e/test_mvp_finish.py:169), a route the real server never reaches for this input. The run-500 copy also doubles: "Something went wrong. Try again. [Try again]" (16-err-run500-light-1440.png) |
| F16 synthetic-case bar | **fixed** | A card on the overview only: summary padding 16/12 px, height 46, 1 px border, radius 6, in light and dark (r3w1.out EMPTY bar, 01-empty-dark-1440.png). It is not shown under an open case |
| F20 dark search / track | **fixed** | In dark mode, search, sort and the name field are all rgb(21, 26, 33). The progress track has a 1 px rgb(122, 134, 150) border (r3w5.out dark-1440, 17-overview-many-dark-1440.png) |
| F21 one reason per rate row | **fixed** | The $185 status cell holds one line: "Not counted: This figure is a rate, not a charge, so it is not added to the total." This holds in all 4 modes (r3w2.out F21, 22-rate-row-*.png) |
| F13 section nav + way back | **fixed** | A sticky nav sits under the header, 37 px at 1440 and 45 px at 390. It reads Overview/Top, Timeline 8, Flags 10, Charges 3, Export, with open counts. From the page bottom, each button lands its heading at y 133 / 173, just under the chrome (bottom 125 / 165), with focus on the heading. Twelve `j` presses never hid a focused row under the chrome. There is no horizontal scroll at 390. In Export, Back to review is the first control, and it returns focus to the row she left (`e4`). By keyboard it is `x`, Enter, Tab, Enter (r3w2.out, r3w3b.out, 21-nav-flags-dark-390.png, 25-export-*.png, 26-back-to-review-*.png). The page is still 6,602 / 10,845 px with the gap flag at y 2,019 / 3,736, but it is now one action away |
| Flaky e2e (N3) | **fixed** | `tests/e2e/test_mvp_polish.py` against :7969 passed 10 full runs in a row, each `25 passed in 38.93s`–`39.39s`. `tests/e2e/test_mvp_finish.py` passed 2 runs, each `18 passed in 34.07s` / `34.15s` |

Tally: 7 fixed, 2 partial (F15 major, F14 minor).

## The new "Count this charge" flow (lib11)
- **What works.** The lib11 case was loaded through "Add a synthetic case". Rows $250, $180 and $2,310 offer Count this charge. The $2,740 subtotal, the $300 payment, the adjustment and the balance offer only Keep in notes or Dismiss.
- **The dialog is good:**
  - It shows the amount and the plain reason.
  - It shows the ledger sentence with the figure highlighted.
  - The confirm button is named: "I checked this is a separate charge for a service".
  - Focus starts on Cancel, Escape returns focus to the button, and at 390 it fits (356×430).
- **After confirming:**
  - The row moves to Detected charges as Accepted, with focus on it in view.
  - The live region says "Counted $250.00 as a separate charge. Accepted charges now $250.00."
  - The header goes from 17 to 16 to review.
  - With all three lines counted, the subtotal stays not counted. The letter lists $180.00 and $2,310.00 with their own clause as the quote, total $2,490.00 (export-letter-lib11.txt; $250 had been undone).
  - By keyboard it is 3 Tabs from the row, then Enter, Tab, Enter.
- **What is wrong:**
  - **The counted row (major).** It carries an amber "▲ Counted as a separate charge" chip with "You confirmed this flag and counted the charge." (charges.js:82). She saw no flag. A second sentence then repeats the point: "You counted this line as a separate charge and confirmed it by name…" (present.py:140). At 1440 the chip overflows its amber box into the Decision column (43-lib11-after-count-light-1440.png). An accepted decision she made herself reads as a warning.
  - **Undo only half-reverses (minor).** Undo on a counted line does not send it back to "Unclear — not totaled". It stays in Detected charges as a pending Charge, with no Count button, and the pending figure becomes "$3,510.00 (not a total)" (44-lib11-after-undo-light-1440.png).
  - **Letter date (minor).** The counted lines print the ledger's statement date as if it were the service date: "Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00". The same lines were held back because they state no date of service.

## As the designer: is this a finished, polished MVP?
**Almost. It is not finished yet.**
- **Ready:**
  - The review loop is now complete and consistent.
  - There is one first item and one count everywhere.
  - She can jump between sections and come back from Export.
  - The overview and dark mode look deliberate.
  - The keyboard path is 2 keys to the first item, then 23 presses of `a` with 0 dead keys, then `x`, Enter, Tab, Enter to copy a clean 46-line letter (r3w3.out, export-letter-keyboard.txt).
- **The shortest set left:**
  1. A demo refusal at create offers **Use the sample case**, and the e2e drives the real create path instead of a stubbed /run (input.js:39).
  2. The counted-charge row gets one neutral line, "You counted this line as a separate charge.", with no "flag" wording, no amber, no ▲ on an accepted row, and the chip inside its cell (charges.js:82, present.py:140).

Both are copy and wiring changes, each about an hour. The rest are minors that a pilot can carry.

## What is right (keep)
- One first item: the skip link, `n`, Start review and Do this first all land on the same row, in every mode (r3w2.out).
- Section nav plus Back to review: one action to any section, and Export returns her to the row she left (26-back-to-review-light-1440.png).
- The Count dialog names what she is confirming and shows the highlighted ledger sentence before she commits (42-lib11-count-dialog-light-1440.png).

## Probe notes
- The `x` key focuses the Export button; it does not open Export. My first r3w3 tail ran on the wrong assumption and is superseded by r3w3b.
- The two "Sample case" rows in the overview came from my run-500 walk. Analyze was pressed and the stubbed run failed, so I do not count them as ghosts.
- The lib11 probe case from r3w0 was deleted before the empty-state shots.

```json
{"card": "T-174", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive da0c7fe (HEAD at start and end) served from scratch on http://127.0.0.1:7969, LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, fresh scratch ZLAYT_DB; sample case evals/golden/sample.txt and library case_lib11_priors_and_ledger; 1440x900 and 390x844, light and dark, pointer, touch and keyboard",
 "exercised": [
  "read personas/ux-designer.md, reviews/MVP-ux-audit-r2.md, board.py show T-174 handoff, tests/e2e/test_mvp_finish.py, input.js and charges.js error/count code",
  "r3w0: lib11 by API, amounts with countable/kind/reason",
  "r3w1: empty overview in 4 modes (synthetic bar style); errors at 1440 light and 390 dark touch: empty, real non-sample paste, 71,440-char oversize, create 500, run 500, PDF, case list 500, with each action button clicked or checked; ghost case by All cases, reload and browser Back",
  "r3w2: sample case in 4 modes (UI create at 1440 light): focus after run; skip link, n and Start review/Go to it against Do this first; section nav from page bottom to Flags, Charges, Timeline; gap flag y; rate row; accept + edit to check + charge dismiss; every count surface + server hitl; 12 j presses against the sticky chrome; Export via nav, first control, Back to review focus",
  "r3w3 / r3w3b: keyboard only at 1440 dark: New case, name, paste, Analyze, 2 keys to the first item, 23 a presses with 0 no-ops to 'Nothing left to decide', x + Enter, Tab to Back to review, Enter, x + Enter, 3 Tabs, Copy letter; clipboard letter inspected (2,728 chars, 46 lines, no HTML)",
  "r3w4: lib11 Count this charge at 1440 light (library loaded through the overview UI), 390 dark touch and 1440 dark keyboard: dialog content and focus, Escape, confirm, row/total/live after, Undo on a counted line, counting $180 and $2,310, subtotal row after, letter via /api/cases/{token}/export",
  "r3w5: overview with 12 cases in 4 modes: list chips vs the case, filters, ghost rows, dark search/sort/title and track",
  "pytest tests/e2e/test_mvp_polish.py vs :7969 x10: all '25 passed'; tests/e2e/test_mvp_finish.py x2: '18 passed'",
  "server PID 3777 stopped; port 7969 returned 000"
 ],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 3, "craft": 3, "functionality": 4},
 "findings": [
  {"severity": "major", "title": "F15 partial: a real non-sample paste in the demo is refused with a dead-end 'Edit the text' button; the e2e stubs a route the server never reaches",
   "evidence": "r3w1.out '[no markers real] This demo only runs the recorded sample cases. Edit the text' at light-1440 and dark-390; 16-err-nomarkers-light-1440.png; app/frontend/input.js:39 (create catch falls to toText()) vs :124 (useSample only on startRun); api.py:321-322 refuses at create; tests/e2e/test_mvp_finish.py:169 stubs **/api/cases/*/run. Also 16-err-run500-light-1440.png 'Something went wrong. Try again. [Try again]'",
   "why_it_matters": "This is the first thing a demo visitor tries. The only offered step can never succeed (error recovery, NN/g error-message guidelines). The green test hides it.",
   "fix": "input.js create(): when e.code === 'demo_mode_unsupported_input', use useSample(). Drop the trailing 'Try again.' from the run-500 message, or word it 'The analysis did not start.'",
   "acceptance_test": "Without stubs, fill the textarea with a non-sample record and click Analyze: the error box has one btn-error-action reading 'Use the sample case', and clicking it shows '9 records found'."},
  {"severity": "major", "title": "Count this charge: the counted row shows an amber '▲ Counted as a separate charge' with 'You confirmed this flag' (no flag was shown), repeats itself, and the chip overflows at 1440",
   "evidence": "43-lib11-after-count-light-1440.png, 43-lib11-after-count-dark-390.png; app/frontend/charges.js:82 (chip--warn + 'You confirmed this flag and counted the charge.'); app/backend/present.py:140 ('You counted this line as a separate charge and confirmed it by name…'); r3w4.out '$250 now' text",
   "why_it_matters": "This is the end state of the new flow. A decision she made herself wears warning styling and refers to a flag she never saw (calibrated trust, nothing claims more than happened), in the densest table, in the demo's charges story.",
   "fix": "For flag 'separate_charge' with review accepted, render a neutral info line 'You counted this line as a separate charge.' with no chip--warn or ▲. Drop one of the two sentences. Keep the chip inside .rv-c-status (wrap or max-width: 100%).",
   "acceptance_test": "After counting $250 on lib11, the row has no .chip--warn, contains no 'flag' wording, has exactly one sentence about counting, and every chip's right edge is ≤ its cell's right edge at 1440."},
  {"severity": "minor", "title": "F14 partial: reload or browser Back from the sample preview still leaves a 'Not analyzed yet' case that counts toward Needs attention",
   "evidence": "r3w1.out 'GHOST reload-root before 2 during preview 3 after leaving 3', 'GHOST history-back before 3 during preview 4 after leaving 4'; r3w5.out ROW 'Ghost check reload-root … Not analyzed yet'; filter 'Needs attention (11)'",
   "why_it_matters": "The overview stops being the list of real work.",
   "fix": "Do not persist a preview, or mark it a draft server-side and sweep drafts on list load; leave them out of Needs attention.",
   "acceptance_test": "Use the sample case, reload: /api/cases count is unchanged."},
  {"severity": "minor", "title": "Undo on a counted line leaves it a pending Charge in Detected charges instead of returning it to Unclear — not totaled",
   "evidence": "44-lib11-after-undo-light-1440.png; r3w4.out 'after Undo: kind charge, review pending, panel charges … Detected, not yet accepted: $3,510.00'",
   "why_it_matters": "User control and freedom: Undo should restore the state before the action.",
   "fix": "Undo of a count restores kind unclear and the Count this charge button (or label the control 'Uncount').",
   "acceptance_test": "Count $250, Undo: the row is back in unclear-amounts with btn-count-charge, and the pending figure is unchanged from before."},
  {"severity": "minor", "title": "Letter prints a counted ledger line with the statement date as if it were the service date",
   "evidence": "export-letter-lib11.txt 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00'; the line was held back because 'The line states no date of service'",
   "why_it_matters": "Pasted into a demand letter, the date reads as the date of service.",
   "fix": "For a counted line with no service date, print 'itemized ledger (statement dated June 15, 2026)'.",
   "acceptance_test": "The letter line for a counted ledger charge contains 'statement dated'."},
  {"severity": "nit", "title": "After a run, focus sits on the 0-px skip nav with nothing visible",
   "evidence": "r3w2.out / r3w3.out 'focus after run: NAV skip-nav h 0'",
   "why_it_matters": "Visibility of system status for keyboard users.",
   "fix": "Focus btn-start-review (btn-do-first at 390) when the run finishes.",
   "acceptance_test": "After Analyze, document.activeElement is the Start review / Go to it button."},
  {"severity": "nit", "title": "Unclear-tray notice says 'for this item' at table level",
   "evidence": "42-lib11-count-dialog-light-1440.png background: 'A second AI check disagreed with the first result for this item. The line states no date of service…' above the lib11 Unclear table",
   "why_it_matters": "Information scent: which item?",
   "fix": "When the sentence is hoisted, say 'for 3 of these lines'.",
   "acceptance_test": "The hoisted tray notice contains no 'this item'."}
 ],
 "whats_right": [
  "The skip link, n, Start review and Do this first land on the same row in all 4 modes (r3w2.out).",
  "Section nav plus Back to review: one action to any section, and Export returns focus to the row she left (26-back-to-review-light-1440.png).",
  "The Count dialog names what she confirms and shows the highlighted ledger sentence first (42-lib11-count-dialog-light-1440.png)."
 ],
 "questions_for_chris": []}
```
