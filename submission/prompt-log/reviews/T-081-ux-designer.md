# T-081 review, ux-designer-reviewer: vertical steppers for every check and gate

Verdict: **changes** (0 blockers, 4 majors). Commit df5dddd, app/frontend/stepper.js, stepper.css, judges.js.

Exercised: own servers at HEAD on :7871 (ZLAYT_MODE=local, fixture/curated) and :7872 (demo/metadata mode); Playwright at 1440x900 and 390x844 on the sample, case_01_date_formats (paste) and library lib06 (judge objections). I opened the item Why dialog for an entry (e5, failed step), an amount (a3) and a flag (f_r5_1), clicked every action button in the case rail, followed gate-blocker jump links, toggled the case rail by keyboard, tabbed through it, read the aria snapshot, accepted items and watched the gate move, and checked mock mode (`?api=mock`) and narrative sentences. Evidence is in `artifacts/review-evidence/T-081-ux-*.png` and `T-081-ux-designer-walk*.py`. Servers stopped after.

Your questions:
- Every check and gate has pass/fail/skipped/pending plus a plain-words why. On fail there is a concrete next action in the item stepper (e5 "Numbers and dates in the summary are in the quote" -> `Go to the item and edit the summary` opened the edit box with focus in the textarea, 1 click). Dead end found in the case rail (finding 2).
- Colour alone: no. Every status has a glyph and a word; kind (Code / AI draft / AI check / You) is a text chip; "Blocks export" is text. Pass.
- Keyboard/screen reader: ol/li, `aria-label` on the lists, markers aria-hidden, `aria-current="step"`, native details/buttons, Esc layers correctly (record modal over Why modal), focus returns to the trigger. Gaps are minor (finding 7).
- Narrative sentences have no stepper entry point: confirmed (finding 3). The API already serves `GET .../items/ns1/trace` (5 steps), the UI never calls it.
- Mock mode hides both panels: confirmed (`hidden=true`), the Why dialog says "Step-by-step checks need the live server." Dev-only, nit (finding 8).

## Findings in prose
1. The case rail is open by default at >=900 px and pushes the work down. At 1440x900 in demo mode the review queue starts at y=599 with the rail closed and y=2519 with it open; the first screen is "Records" plus passed steps (T-081-ux-A-demo-sample-1440-first-viewport.png). Keyboard users tab through ~8 rail stops before the first item.
2. Case-rail actions are dead or missing. lib06 `judges` step is red with "What you need to do: Compare the item with the quote yourself" and a button `Open the record` that does nothing (0 dialogs before and after, no scroll). `totals` and `review` steps say "Accept, edit or dismiss this item." (singular, at case level) with no button.
3. Narrative sentences, the LLM output closest to the letter, cannot open a stepper.
4. In the item Why dialog the failed step is 5th of 11 and the action is below the fold at 390 (and cut at 1440). Passed steps come first; the same quote is printed twice (extracted and excerpt_verbatim).

## Smaller points
Fresh case shows a red X "Failed" on "Ready to export?" and "Not done yet" on a code step that has finished; developer vocabulary in the primary view (`PENDING_DECISION rule row 8`, "llm split false", "lexicon+llm 6"); "10 of 11 steps settled" counts a failed step as settled while the case line counts passes.

```json
{"card": "T-081", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit df5dddd app/frontend/{stepper.js,stepper.css,judges.js}; local app :7871 (ZLAYT_MODE=local, fixture curated) and :7872 (demo mode); sample, case_01_date_formats, case_lib06_lop_billed_vs_adjusted; 1440x900 and 390x844",
 "exercised": [
  "Started own servers at HEAD on :7871 (local) and :7872 (demo), LLM_BACKEND=fixture FIXTURE_SET=curated",
  "GET /trace, /items/{id}/trace, /judges on sample, case_01, lib06 and compared with the rendered DOM",
  "Playwright 1440x900 and 390x844: case rail, item Why dialog (e5, a3, f_r5_1), every rail action button, gate-blocker jump, Open-record stacked dialog, Esc and focus return",
  "Keyboard: Tab sequence to first queue item, Enter on rail summary, aria_snapshot of case rail",
  "Accepted items in demo mode and watched gate count change; accepted all case_01 blockers by API and re-read the gate",
  "Mock API mode (?api=mock) and narrative sentences (drafted a paragraph, looked for a stepper entry point)",
  "Read stepper.js, judges.js, stepper.css and the <outside project> UX_AUDIT.md and _render_flow_rail_html"],
 "verdict": "changes",
 "scores": {"design_quality": 3, "originality": 3, "craft": 3, "functionality": 3},
 "findings": [
  {"severity": "major", "title": "Case rail is open by default on desktop and pushes the review queue two screens down",
   "evidence": "Demo mode 1440x900, sample: queue top y=2519 with rail open vs y=599 closed (walk3 output 'queue top 2519 ... A2 closed: queue top 599'); rail height 1978 px; screenshot artifacts/review-evidence/T-081-ux-A-demo-sample-1440-first-viewport.png shows Records + 4 passed steps and no review item. stepper.js:236 `det.open = openPref == null ? wide() : openPref`. Tab sequence to first queue item passes 8 stepper stops (walk7).",
   "why_it_matters": "Checklist items 2, 6 and 19: needs_review items first and visible; the paralegal's first screen is a list of things that already passed. The stepper explains, it should not displace the work.",
   "fix": "Default collapsed at every width. Keep a one-line strip that is always visible: verdict pill + '7 of 10 checks passed' + the first thing the human must do with its button. When expanded, collapse passed steps into one 'Passed (7)' details and show only failed/pending steps open.",
   "acceptance_test": "E2E at 1440x900 demo mode on the sample: first needs_review queue row has top < 900 on load; the case rail summary is visible and `details.open` is false; opening it shows failed/pending steps first."},
  {"severity": "major", "title": "Case-rail failed and pending steps have a dead button or no button: no one-click path from the step to the fix",
   "evidence": "lib06 (:7871) step judges (fail): button 'Open the record' (data-action-code COMPARE_BY_HAND) does nothing: dialogs 0 -> 0, scrollY unchanged (walk8: 'case-level judges Open the record click: dialogs before/after 0 0'). Steps totals and review (pending) render 'What you need to do: Accept, edit or dismiss this item.' with buttons=[] (walk7). Cause: stepper.js:71-85 actionNode only maps target.item_id or view==='dates_to_confirm'; the server sends target.view 'judges' / 'amounts' / 'queue' (api trace lib06) and the case-level text is the item-level sentence.",
   "why_it_matters": "Chris asked for a failed step to hand off to the human with a clear next action. A visible button that does nothing is worse than no button, and 'this item' at case level does not say which.",
   "fix": "Map target.view to a panel jump (judges -> judges panel, amounts -> charges panel, queue -> first pending queue row, dates_to_confirm as now) and, for judges, jump to the first questioned item. Write case-level copy with counts ('Review the 3 questioned items', 'Decide the 20 pending items'). Never render a button whose handler can no-op: hide it or fall back to the panel jump.",
   "acceptance_test": "E2E on lib06: for each case-step with status fail or pending, assert a btn-step-action exists and that after clicking it document.activeElement or scroll position moved into the targeted panel/row; fails today for judges, totals and review."},
  {"severity": "major", "title": "Narrative sentences (LLM text headed for the letter) have no stepper entry point",
   "evidence": "Sample case, accepted verified entries, drafted paragraph: 9 narrative-sentence rows, buttons in sentence 1 = [], btn-trace count in narrative-panel = 0 (T-082-ux-designer-walk2.py, screenshot artifacts/review-evidence/T-082-ux-narrative-no-stepper-1440.png). API already serves it: GET /api/cases/{tok}/items/ns1/trace -> steps extracted, cites_accepted_entry, sentence_checks, judge_1, human. Handoff also lists it as 'Left'.",
   "why_it_matters": "D-042: 'every check and gate'. The narrative is the one place the model writes free text that goes into the demand letter; it is the item where a visible check trail matters most.",
   "fix": "Add a 'How it was checked' button (S.traceButton) to each narrative sentence and to removed sentences, reusing S.openTrace; label dialog by the first words of the sentence.",
   "acceptance_test": "E2E: after drafting a narrative, each narrative-sentence contains a btn-trace; clicking it opens an item-stepper with steps ending in human."},
  {"severity": "major", "title": "Item Why dialog buries the failed step and its action under passed steps",
   "evidence": "e5 at 390x844: failed step 'Numbers and dates in the summary are in the quote' is step 5 of 11; action button is below the first screen (screenshots artifacts/review-evidence/T-081-ux-B-e5-why-390.png, T-081-ux-C-a3-active-step-390.png; walk5: 'visible in dialog viewport w/o scrolling? False' for a3 and f_r5_1). At 1440 the dialog opens on four green passed steps and the same quote printed twice (extracted, excerpt_verbatim). The top shows the reason bullet but no action button.",
   "why_it_matters": "Verifying an item should cost at most two actions and the reviewer should see what is wrong without scrolling; the stepper is meant to answer 'what failed and what do I do'.",
   "fix": "Directly under the verdict pill render the active step's one-line why plus its action button (the same actionNode). Render passed steps as a collapsed 'Passed (9)' details, or auto-scroll the dialog to the aria-current step on open. Show the quote once, on the first step that cites it.",
   "acceptance_test": "E2E at 390x844 on lib06 e5: on opening the Why dialog, btn-step-action[data-action-code=EDIT_SUMMARY] is within the dialog's visible viewport without scrolling."},
  {"severity": "minor", "title": "'Failed' is used for 'waiting on you' and for a check that did its job (label choice, I would do it differently)",
   "evidence": "Fresh sample: 'Ready to export?' red X 'Failed' with 23 blockers; 'Billed-charges total' (Code) 'Not done yet' although code finished (T-081-ux-A-demo-case-stepper-1440.png). lib06 judges step 'Failed' because the second AI check correctly questioned 3 items. Top line '7 of 10 checks passed' on a case where nothing went wrong.",
   "why_it_matters": "A red X 'Failed' reads as a pipeline fault; the paralegal cannot tell a to-do from an error. Calibrated trust.",
   "fix": "Keep fail for check errors. Use 'Blocked: waiting for you' for the gate, 'Needs your decision' for pending human-owned steps and for judge objections ('AI questioned 3 items'). Count as '7 checks passed, 3 need you'.",
   "acceptance_test": "Unit/E2E: a fresh sample with no check errors renders no step with the word 'Failed'; the gate step reads 'Blocked' and the progress line names how many need the human."},
  {"severity": "minor", "title": "Developer vocabulary in the primary view",
   "evidence": "'PENDING_DECISION rule row 8', 'ITEMS_PENDING rule row 19', 'rule D-034', chips 'llm split false', 'by origin: code 2, llm 1, lexicon+llm 6, lexicon 1', 'classified by code:amounts' (T-081-ux-A-demo-case-stepper-1440.png, T-081-ux-B-e5-why-1440-dialog-full.png). stepper.js:148 renders reason_code and rule inline.",
   "why_it_matters": "Checklist item 18: the paralegal's vocabulary is chronology, excerpt, charge, not lexicon, llm, rule row.",
   "fix": "Move reason_code, rule and raw count keys into the collapsed 'Technical details'; humanize chips ('read by code, not by AI', 'found by phrase list and AI: 6').",
   "acceptance_test": "E2E: no element in .zs-rail outside details[data-testid=step-tech] matches /[A-Z]{3,}_[A-Z_]+|rule row|lexicon|llm /."},
  {"severity": "minor", "title": "Progress wording is inconsistent and counts a failed step as settled",
   "evidence": "Item: '10 of 11 steps settled' with one failed step and one pending (T-081-ux-B-e5-why-1440-dialog-full.png); case: '7 of 10 checks passed; the rest are for you or still open'.",
   "why_it_matters": "'Settled' implies resolved; one of the ten is a failure.",
   "fix": "Use one formula for both: '9 passed, 1 failed, 1 waiting for you'.",
   "acceptance_test": "Unit: progress label contains a count for each non-zero status and never the word 'settled' when a fail exists."},
  {"severity": "minor", "title": "Screen-reader and touch details (conformance severity deferred to accessibility-reviewer)",
   "evidence": "aria_snapshot: gate blockers render ten identical buttons named 'Go to item' (the blocker name is a sibling, not in the button name); two buttons named 'Open the record' in one item stepper; no live region: accepting a batch changed the gate from 23 to 14 blockers silently (walk9, 'live region announcing? 0'); 'Show the other 14' summary is 32 px tall at 390.",
   "why_it_matters": "Expert keyboard users and screen-reader users cannot tell the repeated buttons apart or hear that the gate changed.",
   "fix": "aria-label 'Go to item <label>' on each jump button and 'Open record 5' on record buttons; wrap the verdict/progress line in role=status; set summary min-height 44px.",
   "acceptance_test": "E2E: all btn-gate-jump accessible names are unique; after Accept the case-progress node is inside an aria-live region."},
  {"severity": "nit", "title": "Mock API mode hides both panels with no explanation; hash navigation to a second case in the same page showed the first case's rail",
   "evidence": "?api=mock: case-stepper and judge-panel both `hidden=true` (T-082-ux-designer-walk3.py). Re-opening #/case/<other token> in the same page showed case_01's dates-fail rail for lib06 until a fresh page (T-081-ux-designer-walk6.py vs walk7); not reproduced through the case switcher.",
   "why_it_matters": "Dev-only and an edge case; noted so the T-060 restyle does not rely on mock mode for screenshots.",
   "fix": "In mock mode show the 'need the live server' note instead of hiding; key the rail's repaint on token change on hashchange.",
   "acceptance_test": "Mock mode shows a visible note in the case-stepper host; changing the hash token repaints the rail with the new token's steps."}
 ],
 "whats_right": [
  "Glyph plus word plus kind chip on every step, so status is never colour alone, and the failed-step card (label, Failed, why, code, 'What you need to do', one button) is exactly the HITL hand-off Chris asked for.",
  "EDIT_SUMMARY action closes the dialog, opens the edit box and focuses the textarea in one click; stacked record modal returns focus to the trigger on Esc.",
  "Export gate lists the exact blocking items with a jump link that focuses and flashes the item, and updates live after Accept (23 -> 14)."],
 "questions_for_chris": ["Should the case rail be always collapsed behind a one-line strip, or do you want it open on first load of the demo as a showpiece?"]}
```
