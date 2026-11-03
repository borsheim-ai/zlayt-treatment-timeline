# T-081 round 2, ux-designer-reviewer: vertical steppers for every check and gate

Verdict: **changes** (0 blockers, 2 majors). Frontend commit 8e3c26c (`git diff 8e3c26c HEAD -- app/frontend` is empty at HEAD f49c4c2); backend fe4ee80.

Exercised: own servers at HEAD, `LLM_BACKEND=fixture FIXTURE_SET=curated`, `ZLAYT_DB` in my scratchpad: :7881 `ZLAYT_MODE=local` (sample, case_01, lib06 and a sample case I made "judge never ran") and :7882 demo mode (sample, case_01). Playwright at 1440x900 and 390x844. I clicked every fail/pending action in the case rail on all three cases, opened the Why dialog for e5, a3, a7, f_r5_1, e1, a1, a narrative sentence and an accepted-but-unjudged item, measured focus and visibility inside the dialog, accepted all items on the "judge never ran" case and clicked Export, and checked network POSTs. Both servers stopped (curl returns 000). Evidence: `artifacts/review-evidence/T-081-ux-r2-*.png` and `T-081-ux-r2-walk1..9.py`.

Round-1 majors:
1. Case rail open by default and pushing the queue down: **fixed**. `details.open` is false at 1440 and 390. Demo sample 1440: rail summary is one 58 px line "Case checks 7/10 checks passed, 3 need you, Export blocked by 23", first queue row at y=671 (was 2519 open, 599 closed). Tab stops to the first queue row: 8. In local mode the dev case switcher and library cards put the results at y=1163 at 1440; that is a dev-only block, noted, not charged to this card.
2. Dead or missing case-step actions: **fixed**. Every fail/pending case step on all three cases has a button and each moves focus to the matching place: totals -> charges panel, review/gate -> first pending item, dates -> Dates to confirm, judges (lib06) -> judge panel (auto-opened, `Review the 3 items the AI objected to`). No dead button remained. Landing is imperfect (finding 3).
3. Narrative sentences: **fixed**. Sample after drafting: 9 sentences, 9 `How this sentence was checked` buttons; the dialog shows 5 steps and the active step "Your decision on the paragraph" with `Go to the draft paragraph`.
4. Why dialog focuses the first failed step: **fixed**. e5 at 1440 and 390: 11 steps, `firstFail=4`, `activeIdx=4`, focus is on it, action `Go to the item and edit the summary` is fully inside the dialog viewport. Same for a3, a7, f_r5_1. Items with no failure land on the first pending step.
Round-1 minors also gone: no 'Failed' word in the rail on sample/lib06, no reason codes or "rule row" outside Technical details.

Wiring for T-080 r3 (your three bullets): **missing**. `grep -rniE "rejudge|judge_not_run|JUDGE_NOT_RUN|second check again" app/frontend` returns nothing; `api.js` has no rejudge call.
- JUDGE_NOT_RUN blocker is listed in the gate: yes. 12 blockers with the plain sentence "You accepted this item, but the second AI check never ran on it...", each with Go to item.
- `Run the second check again` calls POST /rejudge: **no**. There is no such button anywhere (0 buttons matching again/second); the RERUN_JUDGE action renders as `Go to the first blocking item` (gate) and `Show the 12 items the AI could not check` (judges step). No POST was sent in any click (network log).
- Export 422 in plain words: the words are right, but the message is not where the user is (finding 2).

```json
{"card": "T-081", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "frontend commit 8e3c26c (identical at HEAD f49c4c2) app/frontend/{stepper.js,stepper.css,judges.js,narrative.js,export.js}; backend fe4ee80; local app :7881 and demo :7882; sample, case_01, lib06, sample with judges blanked; 1440x900 and 390x844",
 "exercised": [
  "Started own servers at HEAD on :7881 (ZLAYT_MODE=local) and :7882 (demo), LLM_BACKEND=fixture FIXTURE_SET=curated, ZLAYT_DB in scratchpad; stopped after (curl 000)",
  "Playwright 1440x900 and 390x844: first viewport, case-rail collapsed state, tab stops to first queue row, scrollW",
  "Opened the case rail and clicked every fail/pending action on sample, case_01 and lib06; recorded dialogs, scrollY and focus target before and after",
  "Why dialog on e5, a3, a7, f_r5_1, e1, a1: first failed step index vs focused step, action button visibility inside dialog",
  "Drafted a narrative on the sample and opened the stepper from a sentence at 1440 and 390",
  "Blanked the judge records of a fresh sample case in my own scratch DB (same helper as tests/unit/test_trace.py _blank_judges), accepted all 23 items by API, read /trace gate, clicked Export in the UI, captured network requests and the 422 message position",
  "Curled /items/e1/trace on the unjudged case and compared next_action with the DOM",
  "grep for rejudge/judge_not_run/RERUN_JUDGE in app/frontend; read stepper.js actionNode, export.js, api.js"],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 4, "craft": 4, "functionality": 3},
 "findings": [
  {"severity": "major", "title": "'Run the second check again' is not wired: no button, no POST /rejudge, and the item stepper does not offer it",
   "evidence": "Sample case with judges blanked and all items accepted (/trace gate: 'fail 12 accepted items have not been double-checked by the second AI check, so the export is blocked. Run the second check again.'). DOM: gate step buttons = Go to item x6, 'Go to the first blocking item' [RERUN_JUDGE]; judges step button 'Show the 12 items the AI could not check' [RERUN_JUDGE]; buttons matching /again|second/ = 0. Click log shows no POST /rejudge (T-081-ux-r2-walk7.py, walk8b.py). `grep -rniE 'rejudge|judge_not_run' app/frontend` is empty; api.js has no rejudge. Item stepper for e1: API gives judge_1 skipped with next_action RERUN_JUDGE 'Run the second check again.' but the dialog shows no 'What you need to do' and no button, verdict chip is green 'Accepted by you', progress '10 passed, 1 skipped' (artifacts/review-evidence/T-081-ux-r2-jnr-1440-item-why.png); stepper.js:SS 'if (st.status === \"fail\" || st.status === \"pending\") actionNode' skips status skipped, and actionNode has no RERUN_JUDGE case (stepper.js:173-186).",
   "why_it_matters": "D-044: an accepted item whose second check never ran blocks export with no override; the only thing that clears it is the judge answering. The UI tells the paralegal to 'Run the second check again' and gives no control that does it, and the only visible path (Go to item, Accept again) is explicitly a no-op for the gate. The user is stuck with a blocked export and no way out except dismissing work. Also the item dialog calls the item 'Accepted by you' in green while it blocks export.",
   "fix": "Add ZL.api.rejudge(token) = POST /cases/{token}/rejudge. Map RERUN_JUDGE (item, gate, judges step, JUDGE_NOT_RUN blocker rows, judge panel unresolved rows) to a button 'Run the second check again' that calls it, disables itself with a status line 'Running the second check on 12 items...' (role=status), then repaints rail, gate, queue and judge panel from the response's export_gate; show a plain error for 409 run_in_progress / 503 llm_unavailable / still_unavailable ('The second check still did not answer for 3 items. Try again, or dismiss them.'). Call actionNode for skipped steps that carry next_action. Make the item verdict say 'Accepted, second check missing' (not green) when blocks_export is true.",
   "acceptance_test": "E2E on a case with blanked judges and all items accepted: gate step and each JUDGE_NOT_RUN blocker row contain button 'Run the second check again'; clicking sends exactly one POST /api/cases/{token}/rejudge; afterwards gate-blocker count drops to the still_unavailable count and Export no longer returns 422. Item Why dialog for e1 shows the same button on the skipped judge step. A failed rejudge (backend returns still_unavailable) leaves blockers in place and shows a message."},
  {"severity": "major", "title": "Export 422 judge_not_run is rendered 12,000 px below the Export button with no scroll or focus; the click looks like nothing happened",
   "evidence": "Same unjudged case. Click Export (top of results): GET /export returns 422; export.js:48-49 renders `<p role=alert class=error>` into #export-body and only scrolls on success (`if (scroll) ... scrollIntoView` is inside the try). Measured: message top y=12499 at 1440 (20341 at 390) with scrollY 834 / 1643, inViewport false (T-081-ux-r2-walk8b.py; screenshot artifacts/review-evidence/T-081-ux-r2-jnr-1440-after-export-click.png shows the unchanged screen). Text is plain and correct ('12 accepted items have not had the second AI check, so the export is blocked. Run the second check again.') but has no button and no list of the 12 items; it also differs in wording from the gate sentence ('not been double-checked by the second AI check').",
   "why_it_matters": "Checklist 10 and 12: a blocked export must warn where the user is and say what to do next. A silent click on the main action is the worst place for a blocked state; screen reader users get an alert, sighted users get nothing.",
   "fix": "On any export error, scroll the export view into view and focus the message; render the server's detail.blockers as the same Go to item list the gate uses plus the 'Run the second check again' button from finding 1. Better: when the gate already says blocked, have Export open the gate step (or show the message beside the Export button) instead of calling the API blind. Use one sentence in both places.",
   "acceptance_test": "E2E at 1440x900 and 390x844 on the unjudged case: after clicking Export the judge_not_run message and the rerun button are inside the viewport (getBoundingClientRect within innerHeight) and document.activeElement is inside the message; blocker items are listed."},
  {"severity": "minor", "title": "Jump targets taller than the screen land in the middle: the heading and first row are above the fold",
   "evidence": "stepper.js:74-76 reveal() uses scrollIntoView({block: 'center'}). lib06 'Review the 3 items the AI objected to' lands with the judge panel top at -453 px (heading and the first objection row off screen; T-081-ux-r2-lib06-action-judges-0.png); 'Go to the totals' lands at -393 px on lib06 and -109 px on the sample (charges heading hidden; T-081-ux-r2-lib06-action-totals-0.png). Walk3 output 'focusTop'.",
   "why_it_matters": "The jump works, but the reader lands mid-table and has to scroll up to find what the button promised.",
   "fix": "Use block 'start' (with scroll-margin-top below the banner) when the target is taller than 60% of the viewport, 'center' only for short rows.",
   "acceptance_test": "E2E: after each case-step action, the target's heading top is within 0..200 px of the viewport top at 1440x900."},
  {"severity": "minor", "title": "'Go to the first blocking item' and 'Go to the first pending item' land on different items",
   "evidence": "lib06: review step -> e5 (needs_review, first in queue order); gate step -> e1 (verified) (T-081-ux-r2-walk3.py output).",
   "why_it_matters": "Two buttons promising 'first' disagree; the gate one skips the item the queue puts first.",
   "fix": "Order gate blockers like the queue (needs_review first) so 'first' means the same thing.",
   "acceptance_test": "Unit/E2E: the first gate blocker id equals the first queue row's data-item-id on lib06."},
  {"severity": "nit", "title": "Why dialog opens scrolled past the verdict chip; 'Show the checks' toggle styles 'Show' differently from 'the checks'",
   "evidence": "T-081-ux-r2-why-lib06-e5-390.png (dialog opens on the failed step, verdict/progress line above the fold); T-081-ux-r2-demo-sample-1440-first-viewport.png ('Show' bold-underlined, 'the checks' underlined only).",
   "why_it_matters": "Small polish; the opening position itself is right.",
   "fix": "Keep the verdict and progress line sticky at the top of the dialog; render the toggle as one underlined phrase.",
   "acceptance_test": "Visual: verdict chip visible after the dialog auto-scrolls to the active step."}
 ],
 "whats_right": [
  "The collapsed one-line case strip ('7/10 checks passed, 3 need you, Export blocked by 23') gives the status without pushing the first queue row below y=671 at 1440.",
  "The Why dialog now opens on the first failed step with its 'What you need to do' button fully visible at both 1440 and 390; every fail/pending case step has a button that lands somewhere real.",
  "Gate listing of JUDGE_NOT_RUN items is in plain words with a jump per item, and narrative sentences now open the same stepper."],
 "questions_for_chris": []}
```
