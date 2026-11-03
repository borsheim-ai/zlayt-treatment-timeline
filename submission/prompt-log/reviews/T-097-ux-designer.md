# T-097 ux-designer-reviewer: rerun feedback beside the refused export, panel failure message, panel/gate agreement

Verdict: **fail** (1 blocker, 2 majors, 1 minor, 1 nit).

Scope: card T-097, commit 0e30623 (the card's commit). I ran a `git archive 0e30623` copy from my scratchpad on my own server (:7895, fixture backend, curated set, scratch ZLAYT_DB). Shared-tree HEAD was 8bc7f90 at the start and 172028c at the end (it moved during the review); I did not review either. Server stopped by PID, port returns 000.

## The four brief questions

1. **Rerun feedback directly under the button in the refused-export message: pass.** At 1440 the button is at y=154 (h=44) and the status line at y=202, 4 px below it. At 390 the button is at y=202 and the status at y=250. The Running and the failed sentence are both in view at both widths. Failed sentence: "The second check still did not answer for 3 items of 3. Try again, or dismiss them." The lead sentence is above the button, so "under the button" is the status line, not the lead.
2. **A failed panel rerun shows a plain-words message that survives a repaint: pass.** The AI-check panel group shows the same failed sentence at 1440 (y=879, in view) and 390 (y=448, in view). It survives collapse and reopen and a second failed rerun, which rebuilds the panel. A full page reload clears it; that is expected for in-memory state and I do not count it.
3. **The panel reads the gate's JUDGE_NOT_RUN blockers, and an edited item says "Edited by you, not AI-checked" with no rerun: partly.** The panel rows and group are right: the edited row has the chip "Edited by you, not AI-checked", no "Blocks the export" chip and no button; the accepted row carries "Blocks the export"; the group button reads "for this item" for N=1. Dismissing the accepted item clears the panel block and the rail says "Ready to export". Two places still disagree with the gate: the panel's one-line summary (finding 2) and the item Why dialog for the edited item (finding 3). Finding 1 is a gate defect the walk exposed.
4. **One group button instead of per-row buttons: reasonable in the AI-check panel, incomplete overall.** One POST covers the whole list (the server scope), and the label counts match the rows. But the rail's gate rows still carry one button per row, and the label names one item while the POST answers for all of them (finding 4). Apply the group model to the rail too.

## Findings

**B1 (blocker). An edited summary whose qualifier check fails passes the export gate and goes into the letter.** Walk2 part B: after I accepted one item and edited another so it drops a qualifier from its quote, dismissing the accepted item gives a gate of "pass", an export of 200 that contains the edited sentence, and the edited item's own trace reports `summary_qualifier` fail with `SUMMARY_DROPS_QUALIFIER`. The Why dialog shows "Summary keeps the quote's qualifiers | Code | Needs your decision", and the rail says "Ready to export, 21 not reviewed". D-045(b) says an edited summary "still passes the D-034 code checks". The gate does not enforce that for edits. The probe found no AI draft in the sample with this check failing, so I cannot compare the AI path; the blocker is on the edited path that was exercised. Open question for Chris below.

**M1 (major). The panel summary still says "2 not checked (blocks export)" while the gate blocks 1.** With one accepted item (judge never ran) and one edited item (exempt), the summary reads "18 checked, 18 agreed with the draft, 2 not checked (blocks export)" at both widths, and the rail says "Export blocked by 1". The "(blocks export)" suffix is attached to the full unchecked count. This is the T-082 r3 contradiction, fixed in the rows and group but not in the summary the paralegal sees when the panel is collapsed. The card's own AC says the panel never says "Blocks the export" for items the gate treats as ready.

**M2 (major). The Why dialog for an edited item says "Accepted, second check missing" and offers "Run the second check again".** The verdict and the judge step come from the per-item trace, which still treats the edited item as a failed judge. The same item's panel row says "Edited by you, not AI-checked" with no button. T-081 r3 logged this as minor; I raise it because the card's goal is gate and panel agreement, and the Why dialog is the surface where the paralegal decides the item. The T-097 handoff lists it as left open.

**m1 (minor). Rail gate-row rerun buttons name one item but rerun all of them (carried from T-081 r3, unchanged).** The row's aria-label is "Run the second check again for 2026-01-09 · Austin EMS run report", yet one click posts once and the status reads "for 3 items of 3" (walk2 `A_1440_after_row_click`, same at 390). The rail rows are built by `blockerRow` at stepper.js:419, which passes the per-item label into the shared handler that posts with no item id (stepper.js:137).

**n1 (nit). The Export button is still scrolled out of view when a refused export opens (carried from T-081 r3).** Export button y=-32 at 1440 and y=-179 at 390 after the message opens; `export-blocked` is in view but `btn-export` is not.

## Evidence

- Walk scripts and results: `artifacts/review-evidence/T-097-ux-designer-walk1.py` and `artifacts/review-evidence/T-097-ux-designer-walk1-results.json`; `artifacts/review-evidence/T-097-ux-designer-walk2.py` and `artifacts/review-evidence/T-097-ux-designer-walk2-results.json`; `artifacts/review-evidence/T-097-ux-designer-probe3.py`.
- Screenshots: `artifacts/review-evidence/T-097-ux-designer-1440-s1-refused-export-failed.png`, `artifacts/review-evidence/T-097-ux-designer-390-s1-refused-export-failed.png`, `artifacts/review-evidence/T-097-ux-designer-390-s2-panel-failed.png`, `artifacts/review-evidence/T-097-ux-designer-1440-s3-mixed-panel.png`, `artifacts/review-evidence/T-097-ux-designer-1440-s3-edited-item-dialog.png`, `artifacts/review-evidence/T-097-ux-designer-1440-s3-after-dismiss.png`.
- Code located (not used as evidence of behaviour): `app/frontend/stepper.js:131-143, 163-171, 411-420, 488-507`; `app/frontend/judges.js:1-39, 40-150`; `memory/ORCHESTRATOR_DECISIONS.md:42` (D-034) and `:53` (D-045).

## What I did not exercise

Keyboard-only walk (not in this brief). The item Why dialog for an accepted item was not clicked separately; it uses the same `S.rerunButton` handler as the rail (finding m1). The server log has four `llm call failed step=j1` lines from the walk; I did not trace them to any UI state, and that is outside my lens.

## Three things that are right

- The refused-export message puts the rerun button and its Running and result sentences directly beneath the lead sentence, in view at 1440 and 390 (S1 `status_directly_under_button: true`).
- A failed panel rerun says what happened in plain words and survives collapse, reopen and a second failed rerun at both widths.
- The panel's edited row says "Edited by you, not AI-checked" with no block chip and no button, and dismissing the accepted item clears the panel block and the rail.

```json
{"card": "T-097", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "card commit 0e30623 via git archive copy in scratchpad (t097/wt); shared-tree HEAD was 8bc7f90 at start and 172028c at end (not reviewed); app http://127.0.0.1:7895 on own server (fixture backend, curated set, scratch ZLAYT_DB), stopped by PID; sample case plus synthetic cases created by the walks",
 "exercised": [
  "git rev-parse --short HEAD -> 8bc7f90; git rev-parse --short 0e30623 -> 0e30623; git status --short | wc -l -> 277 (start)",
  "git archive 0e30623 | tar -x into scratchpad t097/wt (card commit, not HEAD)",
  "own server LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7895 ZLAYT_DB in scratchpad: health 200; pids 45474 and 54605 stopped by PID; curl returns 000 after each",
  "E2E_BASE_URL=http://127.0.0.1:7895 pytest -p no:cacheprovider tests/e2e/test_rerun_judge.py -q from the copy: 17 passed in 25.15s",
  "artifacts/review-evidence/T-097-ux-designer-walk1.py at 1440x900 and 390x844: S1 refused export with JudgeNotRun mode still and hold: pressed the message rerun button, read busy and failed sentences, measured positions, scroll, reopen after reload",
  "walk1 S2: AI-check panel group button, failed sentence, collapse/reopen, second failed rerun",
  "walk1 S3: mixed case (accepted judge-never-ran plus edited exempt): rail summary and row aria-labels, panel summary, edited and accepted rows, group button, item Why dialog for the edited item, dismiss accepted and reload",
  "artifacts/review-evidence/T-097-ux-designer-walk2.py: rail gate-row click (aria-label vs POST scope); edited-summary gate and export via GET /trace, GET /export, GET /items/<id>/trace",
  "artifacts/review-evidence/T-097-ux-designer-probe3.py: searched sample AI drafts for summary_qualifier fail: none found",
  "viewed screenshots: 1440 s1 failed, 390 s1 failed, 390 s2 panel failed, 1440 s3 mixed panel, 1440 s3 edited item dialog",
  "read stepper.js 131-143, 163-171, 411-420, 488-507; judges.js 1-39 and 40-150; ORCHESTRATOR_DECISIONS.md D-034 line 42 and D-045 line 53; reviews T-081-ux-r3 and T-082-ux-r3"],
 "verdict": "fail",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 2},
 "findings": [
  {"severity": "blocker", "title": "Edited summary whose qualifier check fails passes the export gate and goes into the letter",
   "evidence": "walk2 part_b (artifacts/review-evidence/T-097-ux-designer-walk2-results.json): B_item_trace_code_steps [summary_qualifier, fail, SUMMARY_DROPS_QUALIFIER]; B_gate_after_dismiss {status: pass, ready: true, blockers: []}; B_export {status: 200, contains_edit: true}. Rail after dismiss: 'Ready to export, 21 not reviewed' (artifacts/review-evidence/T-097-ux-designer-1440-s3-after-dismiss.png). Why dialog: 'Summary keeps the quote's qualifiers | Code | Needs your decision' (artifacts/review-evidence/T-097-ux-designer-1440-s3-edited-item-dialog.png). D-045(b) at memory/ORCHESTRATOR_DECISIONS.md:53.",
   "why_it_matters": "D-045(b) exempts an edited summary from the judge but says it still passes the D-034 code checks. Here the code check fails, the gate says ready, and the letter carries the edited wording with no flag. The export is what the paralegal pastes into a demand letter, so a dropped qualifier reaches the letter with the product's own check failing. Spec-class blocker (invents or loses facts). Whether summary_qualifier is in the D-034 set is an open question for Chris.",
   "fix": "Apply to edited summaries the same code steps the gate enforces on model drafts. Refuse the edit at save time with an inline message naming the dropped qualifier, keeping the typed text in the box. Also have the gate list any edited item whose code step fails as a named blocker, so GET /export is refused while it fails. The rail, the Export message and the item Why dialog must all say the same thing.",
   "acceptance_test": "E2E: edit a summary so it drops a qualifier from its quote. Expect an inline refusal beside the edit box with the typed text preserved; while it fails, GET /api/cases/<t>/export is not 200 and the letter does not contain the edited sentence. Unit: the gate blocker list includes any edited item with a failing code step."},
  {"severity": "major", "title": "Panel summary still says '2 not checked (blocks export)' while the gate blocks 1",
   "evidence": "S3_edited_mixed_1440_panel_summary {summary_counts: '18 checked, 18 agreed with the draft, 2 not checked (blocks export)'}; S3_edited_mixed_1440_rail {summary_gate: 'Export blocked by 1'}; same at 390 (S3_edited_mixed_390_panel_summary). Screenshot artifacts/review-evidence/T-097-ux-designer-1440-s3-mixed-panel.png. judges.js summaryText attaches '(blocks export)' to the full unavailable count when nb > 0.",
   "why_it_matters": "The T-097 AC says the panel never says 'Blocks the export' for items the gate treats as ready. The one-line summary is the signal the paralegal reads when the panel is collapsed; it says two unchecked items block, and the gate says one. It is the same contradiction T-082 r3 named, fixed in the rows and group but not in the summary.",
   "fix": "Build the summary from the gate's JUDGE_NOT_RUN set: '2 not checked, 1 blocks export'. Only the gate-listed count carries the blocking wording.",
   "acceptance_test": "E2E on the mixed case (1 accepted, 1 edited, judge never ran on the accepted one): judge-summary-counts shows the gate count (1) next to 'blocks export' and does not attach it to the edited item; after the accepted item is dismissed, the summary has no 'blocks export'."},
  {"severity": "major", "title": "Why dialog for an edited item says 'Accepted, second check missing' and offers 'Run the second check again'",
   "evidence": "S3_edited_mixed_1440_item_dialog_edited {verdict: 'Accepted, second check missing', rerun_btn: 1}, judge step '✕ ... Did not run ... Run the second check again'; same at 390 (S3_edited_mixed_390_item_dialog_edited). Same item's panel row: S3_edited_mixed_1440_panel_edited_row {chip 'Edited by you, not AI-checked', rerun_btn_in_row: 0}. Screenshot artifacts/review-evidence/T-097-ux-designer-1440-s3-edited-item-dialog.png. The verdict comes from GET /api/cases/<t>/items/<id>/trace, which the stub does not change for edited items. The T-097 handoff lists this as left open.",
   "why_it_matters": "The Why dialog is where the paralegal decides an item. For an item D-045(b) exempts, it says the check is missing, shows a red cross, and offers a button that answers 'nothing to run'. The panel and the gate say the opposite. T-081 r3 logged this as minor; raised here because the card's goal is gate and panel agreement, and this is the third surface showing the state.",
   "fix": "For human-wording items (review_status edited), build the judge step as neutral 'Not needed: you wrote this summary', with verdict 'Edited by you' and no btn-rerun-judge. Do it in the per-item trace builder so the Why dialog and the panel read one source.",
   "acceptance_test": "E2E on the mixed case: the item-stepper for the edited item has no text 'second check missing', no btn-rerun-judge, and no judge step with data-status fail; after the accepted item is dismissed the rail still says Ready to export."},
  {"severity": "minor", "title": "Rail gate-row 'Run the second check again' buttons name one item but rerun every item (carried from T-081 r3)",
   "evidence": "walk2 A_1440_row_before aria_label 'Run the second check again for 2026-01-09 · Austin EMS run report'; A_1440_after_row_click {posts: 1, rail_status_texts: ['The second check still did not answer for 3 items of 3. Try again, or dismiss them.']}; same at 390. stepper.js:419 passes RERUN + ' for ' + name to S.rerunButton (stepper.js:137), which posts with no item id.",
   "why_it_matters": "The label and the effect disagree: a screen-reader user hears a per-item promise, and a sighted user reads a result for three items after pressing one row. T-097 moved the panel to one group button, the right model, but the rail rows and the item Why dialog keep per-item labels.",
   "fix": "Use the group model everywhere: one 'Run the second check again for these N' in the gate step and no per-row button (rows keep Go to item). If per-row buttons stay, send the item id and rerun only that item.",
   "acceptance_test": "E2E: for every rerun button in the rail, the aria-label scope equals the POST scope: a one-item label means one item in the POST, and a label naming N items means N equals the number of JUDGE_NOT_RUN blockers."},
  {"severity": "nit", "title": "Export button is scrolled out of view when a refused export opens (carried from T-081 r3)",
   "evidence": "S1_export_blocked_1440_before export_btn_box {y: -32}, message top y=90; S1_export_blocked_390_before export_btn_box {y: -179}; export_btn_in_view false after the failure at both widths (walk1 results).",
   "why_it_matters": "The message correctly sits under the toolbar, but the Export button it explains is above the fold; to press Export again the user scrolls up.",
   "fix": "Set scroll-margin-top on the export-blocked section to the toolbar height, or scroll the toolbar row into view instead of the message.",
   "acceptance_test": "E2E: after a refused Export at 1440x900 and 390x844, btn-export and export-blocked both have their top inside the viewport."}
 ],
 "whats_right": [
  "Refused-export message: the rerun button and its Running and result sentences sit directly beneath the lead sentence, the status 4 px under the button, in view at 1440 and 390 (walk1 S1, status_directly_under_button true).",
  "A failed panel rerun says what happened in plain words and survives collapse, reopen and a second failed rerun at both widths (walk1 S2).",
  "The panel's edited row says 'Edited by you, not AI-checked' with no block chip and no button; dismissing the accepted item clears the panel block and the rail says Ready to export (walk1 S3)."],
 "questions_for_chris": ["Is summary_qualifier part of the D-034 code-check set that D-045(b) requires edited summaries to pass? If yes, B1 stands as a blocker; if the qualifier check is advisory for edits, B1 becomes a major and the gate copy must say so."]}
```
