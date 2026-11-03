# T-174 MVP UX audit, round 4: final scoped check

Reviewer: ux-designer-reviewer (Priya Raman persona), model claude-opus-5-5. Date 2026-11-02. Baseline: reviews/MVP-ux-audit-r3.md (da0c7fe, changes, 2 majors).

**Build.** `git archive 489f1bc`. `git rev-parse --short HEAD` gave `489f1bc` at the start and at the end.
- Two servers ran from the scratch copy, both with `LLM_BACKEND=fixture FIXTURE_SET=curated` and each with its own scratch `ZLAYT_DB`:
  - 127.0.0.1:7981 with `ZLAYT_MODE=local`. The library is on the page. `/api/cases` returned `{"cases":[]}` at the start.
  - 127.0.0.1:7982 in public mode, with no library, to check the "where the library exists" branch.
- Both servers were stopped by PID (python 20424 and 20460). Both ports then returned `000`.

**Evidence.** Everything is in `artifacts/review-evidence/mvp-audit-r4/`:
- the scripts `r4w1..r4w4*.py`
- their raw output `r4w*.out`
- the screenshots `NN-*.png`

**Verdict: pass.** Both r3 majors are fixed on the real path, with no stubs. F14 is fixed. What is left is 5 minors and 3 nits.

**Scores:** design quality 4, originality 3, craft 4, functionality 4.

## Deterministic check first
- I ran `pytest tests/e2e/test_mvp_finish.py` with its own private server (empty DB): `22 passed in 33.08s`.
- Against my :7981 server, which already held 6 cases: `2 failed, 20 passed in 56.95s`. Both failures are the new refusal specs (`btn-error-library` count 0). r4w4 shows why: see minor F2.

## Major 1: the demo refusal (r3 F15). **Fixed.**
I drove the real POST /api/cases with no stubs (r4w1.out, r4w1b.out). The paste was a synthetic PT note with no record markers.
- **Message.** The box reads: "This demo only runs the recorded sample and library cases, so it can't analyze other text. Nothing was started."
  - It is shown as `role="alert"`.
  - The pasted text is kept (154 of 154 characters).
  - The only call made was the POST, and the case count did not change (0 to 0, 1 to 1, 2 to 2).
- **Buttons with the library (local).** "Open the sample" and "Choose a library case".
- **Buttons without the library (public).** Only "Open the sample". The copy changes to "the recorded sample case".
- **Run-live note.** "To run your own records, start the app on your own computer with ENABLE_LIVE=1 and a model key."
- **There is no "Edit the text" button anywhere.**
- **Choose a library case.** It opens the group and moves focus to the first library case, in view at 1440 and 390. The pasted text stays.
- **Open the sample.** It opens the 9-record sample preview, ready for Analyze.
- **Keyboard.** From Analyze, it is Tab, Tab, then the two buttons in order.
- **Layout.** No horizontal scroll at 390. Buttons are 44 px tall on touch (10-refusal-local-light-1440.png, 10-refusal-local-dark-390.png, 10-refusal-public-*).

## Major 2: the counted charge on lib11. **Fixed.**
I opened lib11 through "Add a synthetic case", then measured the row after "Count this charge" (r4w2.out, 21-counted-row-light-1440.png, 25-counted-row-dark-390.png, 26-counted-row-*.png).
- **The row reads:** chip "✓ Counted by you", then "You confirmed it is a separate charge for a service. No AI check was asked about it."
- **Wording.** "flag" appears 0 times, "confirm" once and "separate charge" once. The old present.py sentence is suppressed (charges.js:228).
- **Colour.** The chip is `chip--info`, not amber: rgb(230,239,253) on rgb(11,79,158) in light, and rgb(22,40,74) on rgb(156,194,255) in dark. The row has 0 `chip--warn`.
- **Fit.** At 1440 the chip spans x 586–716 inside its 578–786 cell (scrollWidth 128 = clientWidth 128). At 390 it spans 27–157 inside 19–373, with no horizontal scroll. I checked light and dark at both widths.
- **Other flags keep their warning.** The $2,740 and $300 rows still show amber "Needs review".
- **Feedback and keyboard.** The live region says "Counted $250.00 as a separate charge. Accepted charges now $250.00." Focus returns to the row. By keyboard it is 3 Tabs, then Enter, Tab, Enter.

## F14: the sample preview is deleted when she leaves (r4w3.out). **Fixed.**
- For each way of leaving, the case count went from 4 (before) to 5 (during the preview) to 4 (after), with no Ghost case left. I tried:
  - reload
  - browser Back
  - tab close (`page.close(run_before_unload=True)`)
  - navigating to about:blank
  - All cases
  - Back then Forward
- A reload lands on the overview, not on a missing case.
- No regression: an analyzed sample and a library case both survive a reload.
- Only a hard browser kill, which fires no page events, leaves the preview (nit N3).

## Remaining findings (none blocks)
- **F1 minor.** The Why dialog still uses the old flag wording for her count.
- **F2 minor.** The refusal specs race the library list.
- **F3 minor.** The refusal can land below the fold.
- **F4 minor, carried from r3.** The letter prints the ledger's statement date as if it were the date of service.
- **F5 minor, carried from r3, now card T-176.** Undo on a counted line half-reverses it. Noted only, not blocking.
- **Nits.** After "Open the sample", focus falls to `<body>`. The live note uses an env-var name. A hard browser kill leaves the preview.

## As the designer: is this a finished, polished MVP?
**Yes, for its stated scope.**
- The paralegal loop is complete and consistent. She sees every excerpt in place, has one first item and one count, and has one-key accept, edit and dismiss with undo.
- She can reach any section in one action and get back from Export.
- The export is a clean letter.
- The demo's most likely error now explains itself and offers two working ways forward.
- Her own decisions now read as hers, not as warnings.

What is left is wording and robustness polish:
- F1: one backend copy line.
- F2: the e2e wait.
- F3: scroll the error into view.
- F4: the letter date.
- T-176: undo.

A pilot can carry all of these. None makes a must-have unusable or hides provenance.

## What is right (keep)
- The refusal names what happened, says nothing was started, keeps her text and offers only actions that work, with the copy adjusted to the mode.
- "Counted by you" in calm info blue, said once and fitting its cell at both widths: her decision reads as hers.
- The preview cleanup covers reload, Back, close and navigate, without touching analyzed or library cases.

```json
{"card": "T-174", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive 489f1bc (HEAD 489f1bc at start and end); app at 127.0.0.1:7981 (fixture curated, ZLAYT_MODE=local, scratch ZLAYT_DB) and 127.0.0.1:7982 (fixture curated, public mode); library case case_lib11_priors_and_ledger, sample case evals/golden/sample.txt; baseline reviews/MVP-ux-audit-r3.md",
 "exercised": [
  "pytest tests/e2e/test_mvp_finish.py with its own private server: 22 passed in 33.08s; against :7981 holding 6 cases: 2 failed, 20 passed in 56.95s (both refusal specs)",
  "r4w1: real unstubbed paste refused at POST /api/cases on local and public servers, 1440 light pointer, 390 dark touch, 1440 keyboard; error text, buttons, note, text kept, case count, both buttons pressed",
  "r4w1b: position of the refusal right after Analyze, before any scroll, local and public at 390 and 1440",
  "r4w2: lib11 opened via Add a synthetic case; Count this charge on $250, $180, $2,310 by pointer, touch and keyboard; chip class, colours, box vs cell at 1440/390 light/dark; flag and confirm word counts; Why this status dialog; Undo; letter export via API",
  "r4w3: sample preview left by reload, Back, tab close, navigate away, All cases, Back+Forward, browser kill; analyzed sample and library case reloaded",
  "r4w4: refusal at 0, 0.5, 1.5 and 3 s after the form appears, 1440 and 390, library switcher state at click time",
  "read the 489f1bc diff of charges.js, input.js, review.css, styles.css; trace.py:526-537; stepper.js:481"
 ],
 "verdict": "pass",
 "scores": {"design quality": 4, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "The Why dialog for a counted line still says 'Flagged by the code' and 'You confirmed this flag by name'",
   "evidence": "artifacts/review-evidence/mvp-audit-r4/22-counted-why-light-1440.png; r4w2.out 'WHY flag words: 4 | confirm mentions: 5'; step reads 'Flagged by the code: Counted as a separate charge ... You confirmed this flag by name (Counted as a separate charge) on 2026-11-02'; source app/backend/trace.py:530 and :533; app/frontend/stepper.js:481 skips the new chargeFlagNote whenever a charge_flag step exists, so the frontend fix never shows here",
   "why_it_matters": "The row now says her count is her own decision, but one click away the same decision is called a code flag she confirmed. That is the wording r3 asked to remove, still shown on a second surface.",
   "fix": "For flag separate_charge, trace.py labels the step 'Counted by you' and says once: 'You confirmed it is a separate charge for a service on <date>.' No 'flag' wording. (Backend card.)",
   "acceptance_test": "E2E: after Count this charge, open More > Why this status; the dialog contains 'Counted by you' and no word 'flag'; 'confirm' appears once in that step."},
  {"severity": "minor", "title": "The refusal specs race the library list: red against a server that already has cases",
   "evidence": "pytest tests/e2e/test_mvp_finish.py against :7981 (6 cases): '2 failed, 20 passed' (btn-error-library count 0); private empty server: '22 passed'. r4w4.out: Analyze at 0 s after input-text appears gives buttons ['Open the sample'] with switcher absent; at 0.5 s and later gives both buttons. input.js:39-41 decides once, at refusal time",
   "why_it_matters": "The acceptance evidence for the main fix depends on server state. A quick Analyze also gets the refusal without the library option, even though the list arrives a moment later.",
   "fix": "The spec waits for [data-testid=library-list] before Analyze. demoRefusal re-renders when the case switcher finishes loading.",
   "acceptance_test": "test_mvp_finish.py passes 5 runs in a row against a server pre-loaded with 6+ cases."},
  {"severity": "minor", "title": "The refusal is not scrolled into view and can appear just below the fold",
   "evidence": "r4w1b.out local 1440 with 3 cases: Analyze at viewport y 864-900, error top at y 912 with vh 900, 'error top inside viewport: False'; 13-refusal-as-seen-local-light-1440.png",
   "why_it_matters": "She clicks Analyze and nothing on screen changes. Errors belong next to their source and in view (NN/g error guidelines).",
   "fix": "On showError, call scrollIntoView({block: 'nearest'}) on #input-error.",
   "acceptance_test": "With 3+ cases at 1440x900, after Analyze on a refused paste, the error box's top and its first button are inside the viewport."},
  {"severity": "minor", "title": "Carried from r3: a counted ledger line prints the statement date as its service date",
   "evidence": "r4w2.out letter_text: 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00'; the same line was held back because 'The line states no date of service'",
   "why_it_matters": "The letter implies a date of service the record does not state.",
   "fix": "Print 'itemized ledger (statement dated June 15, 2026; no service date stated)' for counted no-date lines.",
   "acceptance_test": "Export of lib11 with $180 counted contains 'statement dated' and no bare 'June 15, 2026: $180.00'."},
  {"severity": "minor", "title": "Carried from r3, now backend card T-176: Undo on a counted line half-reverses it",
   "evidence": "r4w2.out AFTER UNDO $250: stays in group charges, review pending, chip 'Count taken back', and the text says both 'You took back your count' and 'You counted this line as a separate charge and confirmed it by name'; pending reads '$3,510.00 (not a total)'; 23-after-undo-light-1440.png",
   "why_it_matters": "Undo should return her to where she was. The row contradicts itself and the pending figure double-counts the line. Noted only; tracked on T-176.",
   "fix": "Per T-176: Undo returns the line to 'Unclear — not totaled' with Count this charge.",
   "acceptance_test": "Per T-176."},
  {"severity": "nit", "title": "After 'Open the sample', focus drops to <body>",
   "evidence": "r4w1.out OPEN SAMPLE => focus {'tag': 'BODY'} in all 5 walks",
   "why_it_matters": "A keyboard user has to Tab from the top to reach Analyze. Accessibility severity is deferred to accessibility-reviewer.",
   "fix": "Focus the records heading or Analyze after the preview loads.",
   "acceptance_test": "After Open the sample, document.activeElement is the records heading or btn-analyze."},
  {"severity": "nit", "title": "The run-live note names an environment variable",
   "evidence": "'To run your own records, start the app on your own computer with ENABLE_LIVE=1 and a model key.' (10-refusal-local-light-1440.png)",
   "why_it_matters": "This is developer terms, not paralegal terms (checklist 18). It is acceptable for a demo whose audience runs it, but it could link to the README instead.",
   "fix": "'To run your own records, run the app on your own computer (see README, Run live).'",
   "acceptance_test": "The note has no ENABLE_LIVE text and links to the README section."},
  {"severity": "nit", "title": "A hard browser kill leaves the sample preview behind",
   "evidence": "r4w3.out 'GHOST browser-kill: ... after 5 | ghost left: [\"Ghost browser-kill\"]'",
   "why_it_matters": "A crash fires no page events, so client-side cleanup cannot cover it. It is rare.",
   "fix": "Server-side expiry for never-run sample previews.",
   "acceptance_test": "An unrun preview older than N minutes is not listed."}
 ],
 "whats_right": [
  "The refusal names what happened, says nothing was started, keeps her text and offers only working actions, with copy matched to the mode (local vs public).",
  "'Counted by you' in calm info blue, said once and fitting its cell at 1440 and 390, light and dark: her decision reads as hers.",
  "Preview cleanup covers reload, Back, tab close, navigate away and Back+Forward, and never deletes an analyzed or library case."
 ],
 "questions_for_chris": []}
```
