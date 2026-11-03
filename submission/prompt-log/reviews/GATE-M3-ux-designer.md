# GATE-M3 — ux-designer-reviewer (Priya Raman persona)

Model claude-opus-5-5. Date 2026-11-02. Baseline: reviews/MVP-ux-audit-r4.md (489f1bc, pass).

## Build and setup
- **Commit.** `git rev-parse --short HEAD` gave `d0b04bc`. `git merge-base --is-ancestor 489f1bc d0b04bc` gave `ancestor_ok`.
- **No app changes since r4.** `git diff --stat 489f1bc d0b04bc -- app` printed nothing. The 9 changed files are tests only.
- **Servers.** Both ran from a `git archive d0b04bc` copy in my scratchpad, each with its own scratch `ZLAYT_DB`.
  - 127.0.0.1:7991: `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`. `/api/cases` returned `{"cases":[]}` at start.
  - 127.0.0.1:7992: the same, plus `LLM_FIXTURE_DIR` set to an empty directory. This gives a real model failure (fixture miss), not a stub.
  - I stopped both by PID (49978, 50285). Both ports then returned `000`.
- **Evidence.** `artifacts/review-evidence/gate-m3-ux/`: scripts `w0..w6*.py`, raw output `w*.out`, screenshots `NN-*.png`, and the exported letters as `.txt`.

## Deterministic check first
I ran `pytest tests/e2e/test_journey_modes.py tests/e2e/test_mvp_finish.py tests/e2e/test_adversarial_ui.py` from the archive copy. Each spec starts its own server. Result: `31 passed in 53.37s` (pytest-e2e.out).

## Verdict: **pass**
- 0 blockers, 0 majors, 8 minors, 3 nits.
- **Scores:** design quality 4, originality 3, craft 4, functionality 4.

## What I graded
**Hierarchy.**
- At 1440 the case top shows four things in order: one "Do this first" line, the needs-review and export-blocked chips, jump buttons with counts, then the timeline.
- Needs-review entries sort first. Each has an amber 3 px border, a "Needs review" chip and its one-sentence reason in the row. On lib11, e1, e2, e4 and e9 come before the verified rows.
- Verified rows use a grey border and a "Quote matches" chip. Unverified and verified are never styled alike.

**Review-not-trust affordances.**
- Every entry, flag and charge shows its verbatim excerpt inline, with the record label. Verifying an item takes 0 actions.
- Conflicts show each record's quote in the same card.
- The $185 rate sits under "Unclear — not totaled" with its reason.
- "Could not verify (2)" on lib11 is visible and says why each item was left out.
- The Why dialog lays out the validation ladder step by step.

**States.**
- **Empty input, 513,071 characters, and a refused paste.** Each shows a plain message beside the input with a next-step button. The text is kept every time (181 of 181 characters, 513,071 kept).
- **Model failure.** It keeps the 9 records and offers Try again.
- **Loading.** It shows a progress element and skeleton rows.
- **Overview.** Both the empty and the 17-case lists have counts, filters and per-case progress.

**Mobile.**
- At 390, scrollWidth equals 390 on every screen, in light and dark.
- Accept, Edit, Dismiss, Export, Copy and Analyze are 44 px tall.
- The sticky section nav reaches Timeline, Flags, Charges and Export in one tap.

**Export.**
- **Nothing accepted.** The export is blocked and says why.
- **Some items pending.** The letter shows only accepted items. The count line reads "4 entries, 0 charges in letter · … · 19 items pending (10 flags)". Copy and Download both ask "Copy the letter anyway?" with the pending counts.
- **Edits and dismissals.** An edited summary appears in its edited form. Dismissed entries are absent.
- **Pasted text.** The clipboard equals the letter. It has no HTML or UI labels, and each entry carries a `Source [Ex. __ / Bates __]` citation. A one-line layout is offered.

**Timing.**
- Keyboard-only sample journey, from the home screen to the letter: about 126 key presses and 0 pointer clicks, 52.6 s of script time.
- Mouse journey with "Accept all verified entries" and then per-item clicks: 18 clicks, 41.1 s.

## Findings (none blocks)
- **F1 minor.** After Undo on a dismissed entry, the restored row and its focused Accept button sit behind the sticky header (focus top 0, header bottom 124).
- **F2 minor.** An edit that drops "complained of" is refused with a message that names a category, not the words.
- **F3 minor.** The edit hint promises that the second AI check gates the letter. Under D-045(b) it does not.
- **F4 minor.** The model-failure notice says "finished items are saved" and, in the same box, that nothing was made.
- **F5 minor (opinion).** Every untouched case on the overview wears a red "✕ Export blocked (1)".
- **F6 minor, carried from r4 F1.** The counted-charge Why dialog still says "Flagged by the code" / "confirmed this flag".
- **F7 minor, carried from r4 F4.** The letter prints the ledger's statement date as the date of service.
- **F8 minor, carried.** The 73-day gap flag is at y 2,139 at 1440x900. A one-click "Show gap flag" at the top makes up for it. This improves on about 5,000 at bc12d44.
- **Nits.** "Starting……" shows a double ellipsis. At 390 the Export screen highlights "Charges" in the section nav. The refusal note names `ENABLE_LIVE=1`.

## r4 carry-overs at d0b04bc
- **F1 (Why wording).** Still present.
- **F3 (refusal off-screen).** Not reproduced: with 29 cases the box sat at y 748–850 of 900.
- **F4 (statement date).** Still present.
- **T-176 (Undo on a counted line).** The row now reads coherently: "Count taken back … Accept it to count this line again". No finding.

## What is right (keep)
- The excerpt is beside every entry, flag and charge. Needs-review items sort first with their reason in the row. Could-not-verify items have their own visible tray.
- The letter holds exactly the accepted set, including edits. The count line says what is in it. Copy and Download ask when items are pending. The pasted text is clean.
- Every error keeps her text or records, sits beside the input, and offers one next step, at both widths and in both themes.

```json
{"card": "GATE-M3", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive d0b04bc (HEAD d0b04bc; app unchanged since 489f1bc per git diff --stat 489f1bc d0b04bc -- app); app at 127.0.0.1:7991 (fixture curated, ZLAYT_MODE=local, scratch ZLAYT_DB) and 127.0.0.1:7992 (same, empty LLM_FIXTURE_DIR for a real model failure); sample case evals/golden/sample.txt and library case case_lib11_priors_and_ledger; 1440x900 and 390x844, light and dark",
 "exercised": [
  "pytest tests/e2e/test_journey_modes.py tests/e2e/test_mvp_finish.py tests/e2e/test_adversarial_ui.py from the archive copy: 31 passed in 53.37s",
  "w0: API inventory of the sample + 15 library cases (entry states, flag types, amounts, tray counts)",
  "w1, at 1440/390 x light/dark: empty overview; Analyze with empty input; 513,071-char paste; refused non-sample paste (case count 0 to 0, text kept); sample preview; loading (real /run and /status responses held 2.5 s); results top; model failure on :7992 (run_partial, 9 records kept, Try again)",
  "w2, at 1440/390 x light/dark: populated overview (17 cases); Start review / Do this first lands on a2 ($185, needs review); gap flag position and Show gap flag; flags panel; both conflict cards; charges + unclear tray; edit refused for a dropped qualifier; dismiss; accept; export with nothing accepted (blocked); all 23 decided; letter; Copy (clipboard == letter, no HTML)",
  "w3, at 1440 light and 390 dark: More > Why this status dialog; valid edit via Save and accept (original kept, Edited by you, in letter); dismiss then Undo; accept 3 then Export (count line, letter of 4, Copy anyway confirm)",
  "w4, at 1440/390 x light/dark: lib11 opened via Add a synthetic case (results in ~32 s, of which up to 15 s was my script waiting for an Analyze button the library flow does not show); needs-review rows first with reason and border colours; Could not verify tray (2 items); Count this charge on $250 with confirm; dismiss a gap flag",
  "w5, at 1440 light: keyboard-only sample journey from home to letter (0 pointer clicks, ~126 keys, 52.6 s script time); ? shortcuts dialog; j through all items (0 rows behind the sticky header); e edit, Esc; a then r undo; n/a/d through all; x Enter export; one-line layout; mouse journey with Accept all (18 clicks, 41.1 s)",
  "w6, at 1440 light: refusal position with 29 cases; counted-charge Why dialog wording; letter lines for counted $250/$180; Undo on a counted line",
  "read input.js (showError, demoRefusal, runningNode), review.js:527, review.py:336-364, trace.py:530-533, export.js:40-64; memory/ORCHESTRATOR_DECISIONS.md D-044, D-045, D-058",
  "stopped servers PID 49978 and 50285; both ports then returned 000"
 ],
 "verdict": "pass",
 "scores": {"design quality": 4, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "After Undo on a dismissed entry, the restored row and its focused Accept button are hidden behind the sticky header",
   "evidence": "w3.out 'AFTER UNDO e2: pending | focus {tid: btn-accept, item: e2, y: 0, h: 28}' at 1440 (sticky header bottom 124 per w5 sticky_bottom) and 'y: 0, h: 44' at 390; artifacts/review-evidence/gate-m3-ux/18b-undo-dismiss-light-1440.png and 18b-undo-dismiss-dark-390.png show neither e2 nor its focus. j/k stepping had 0 obscured rows (w5.out), so the problem is on the Undo path only",
   "why_it_matters": "She presses Undo in the Dismissed group, and the item jumps back up out of sight while focus goes under the header. She cannot see what she restored (visibility of system status; checklist 14). Accessibility severity (WCAG 2.4.11) is deferred to accessibility-reviewer.",
   "fix": "Give item rows scroll-margin-top equal to the sticky banner + header + section nav height, and scroll the restored row to the 'nearest' block after the reset.",
   "acceptance_test": "E2E at 1440x900 and 390x844: dismiss e2, press Undo in the Dismissed group; the e2 row's top and document.activeElement are both below the sticky nav's bottom edge and inside the viewport."},
  {"severity": "minor", "title": "An edit that drops 'complained of' is refused with a category, not the words to keep",
   "evidence": "artifacts/review-evidence/gate-m3-ux/17-after-edit-light-1440.png: 'The quote carries a phrase that says whose account the quote gives that the summary leaves out. Put it back in the summary.' The edit removed 'complained of' (quote 'C/O'). Source app/backend/review.py:336 (_QUALIFIER_WORDS self_report has no example) and :364. The number and word refusals at review.py:356-360 do quote the tokens. The edit hint app/frontend/review.js:527 lists only 'number, date and negation'",
   "why_it_matters": "Correction must be cheap. She is told something is missing but not what, so she must guess. Shortening a summary is the most common edit. NN/g: error messages should say precisely what is wrong.",
   "fix": "Quote the qualifier the code found and its summary form: 'The quote says “C/O” (complained of): keep “complained of” or “reports” in the summary.' Add 'hedges, approximations and whose account it is' to the edit hint.",
   "acceptance_test": "Edit sample e1 to drop 'complained of'; the refusal contains '“C/O”' and 'complained of'. The edit hint mentions whose account it is."},
  {"severity": "minor", "title": "The edit hint says the second AI check gates the letter, but an edited summary reaches the letter without it",
   "evidence": "app/frontend/review.js:527: 'When you save, the code checks every number, date and negation … then a second AI check reads it. Nothing is added to the letter until it passes.' After Save and accept the row says 'Compared by you with the quote. The second AI check did not run.' and the letter contains the edited text (w3.out 'partial letter has edited GOOD: True'). That behaviour is correct under D-045(b) (human-authored text is exempt from the judge); the copy is not",
   "why_it_matters": "The AI's role must be explained accurately where it acts (checklist 15). Calibrated trust breaks when the screen promises a check that does not gate the letter.",
   "fix": "'When you save, the code checks your wording against the quote; nothing is saved until it passes. A second AI check then reads it and may mark it for review.'",
   "acceptance_test": "Hint text has no 'until it passes' tied to the AI check, and matches the row copy after Save and accept when the judge did not run."},
  {"severity": "minor", "title": "The model-failure notice contradicts itself",
   "evidence": "artifacts/review-evidence/gate-m3-ux/08-model-failure-light-1440.png and 08-model-failure-dark-390.png: 'The analysis did not finish. Your records are kept and finished items are saved. The AI step failed for 20 items (finding the flags and the second check and writing the entries) on this run, and there is no earlier result to keep. No entry was made for records 1, 2, 3, 4, 5, 6, 7, 8 and 9.' The static half is app/frontend/input.js:120. 'Try again' wraps to two lines at 1440",
   "why_it_matters": "Error states must be designed: one says items are saved, the next says nothing was made. The middle clause is in process words ('the second check'), not hers.",
   "fix": "When counts are zero, render 'Your 9 records are kept. Nothing was finished on this run.' and drop 'finished items are saved'; keep the server's record list; keep Try again on one line (white-space: nowrap).",
   "acceptance_test": "Fixture-miss sample run: run-error does not contain both 'finished items are saved' and 'No entry was made'; Try again is one line at 1440."},
  {"severity": "minor", "title": "Opinion, not a spec breach: every untouched case on the overview shows a red '✕ Export blocked (1)'",
   "evidence": "artifacts/review-evidence/gate-m3-ux/10-overview-cases-light-1440.png: 17 of 17 rows show the red chip with 'Nothing is accepted or edited yet, so the letter would be empty.'",
   "why_it_matters": "Red error styling for the normal starting state teaches her to ignore red. A case that is actually blocked (judge never ran, D-044) then looks the same as one she has not started.",
   "fix": "For the 'nothing accepted yet' reason, show a neutral 'Not started' chip; keep red '✕ Export blocked' for real blockers.",
   "acceptance_test": "Overview with a fresh case and a D-044-blocked case: only the second shows the red chip."},
  {"severity": "minor", "title": "Carried from r4 F1: the counted-charge Why dialog still says 'Flagged by the code' and 'confirmed this flag'",
   "evidence": "w6.out 'flag' words: 4 | 'Flagged by the code' present: True | 'confirmed this flag': True; artifacts/review-evidence/gate-m3-ux/51-counted-why-light-1440.png; app/backend/trace.py:530, :533",
   "why_it_matters": "The row reads 'Counted by you'. One click away, the same decision is called a code flag she confirmed.",
   "fix": "As r4: label the step 'Counted by you', with no 'flag' wording.",
   "acceptance_test": "After Count this charge, the Why dialog contains 'Counted by you' and no 'flag'."},
  {"severity": "minor", "title": "Carried from r4 F4: a counted ledger line prints the statement date as its date of service",
   "evidence": "w6.out letter lines: 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00' and '… June 15, 2026: $180.00'; the row's own reason is 'The line states no date of service'",
   "why_it_matters": "The letter implies a date of service the record does not state (checklist 20).",
   "fix": "'itemized ledger (statement dated June 15, 2026; no service date stated): $250.00'.",
   "acceptance_test": "lib11 export with $250 counted contains 'statement dated' and no bare 'June 15, 2026: $250.00'."},
  {"severity": "minor", "title": "Carried (checklist 19): the 73-day gap flag is below the fold at 1440x900; a one-click link makes up for it",
   "evidence": "w2-light-1440.out 'GAP FLAG box at load (scroll 0): y 2139 … vh 900 | show-gap button: y 174'; one click on Show gap flag focuses it at y 387. Down from about 5,000 at bc12d44",
   "why_it_matters": "The most damaging fact in the sample is 2.4 screens down. The link is the accepted alternative but depends on her noticing a side-panel button.",
   "fix": "Put the gap flag (type and days) in the Case overview line beside 'Do this first'.",
   "acceptance_test": "At 1440x900, scroll 0, the text 'Gap of 73 days' is inside the viewport."},
  {"severity": "nit", "title": "Loading reads 'Starting……' (double ellipsis)",
   "evidence": "w1.out 'LOADING visible True stage: Starting……' at all four combos; artifacts/review-evidence/gate-m3-ux/06-loading-dark-1440.png; app/frontend/input.js:142 sets 'Starting…' and runningNode appends '…' when no step count",
   "why_it_matters": "Small craft slip on the first state after Analyze.",
   "fix": "Do not append the ellipsis when the label already ends with one.",
   "acceptance_test": "status-stage text right after Analyze is 'Starting…'."},
  {"severity": "nit", "title": "At 390 the Export screen highlights 'Charges' in the sticky section nav",
   "evidence": "artifacts/review-evidence/gate-m3-ux/22-export-letter-dark-390.png (Charges underlined, Export heading on screen); at 1440 22-export-letter-light-1440.png highlights Export correctly",
   "why_it_matters": "Wrong 'you are here' cue on the phone.",
   "fix": "Set the active tab from the view, not scroll position, when the Export view is open.",
   "acceptance_test": "At 390 on Export, the nav's aria-current item is Export."},
  {"severity": "nit", "title": "Carried from r4: the refusal note names an environment variable",
   "evidence": "w1.out refusal text '… start the app on your own computer with ENABLE_LIVE=1 and a model key.'; app/frontend/input.js:45",
   "why_it_matters": "Developer terms in her screen (checklist 18). Acceptable for a demo.",
   "fix": "Link to the README's Run live section instead.",
   "acceptance_test": "Refusal note has no 'ENABLE_LIVE'."}
 ],
 "whats_right": [
  "Every entry, flag and charge shows its verbatim excerpt inline with its record; needs-review items sort first with an amber border and the reason in the row; the Could not verify tray is visible.",
  "The letter holds exactly the accepted set (edits in, dismissed and pending out); the count line says what is in it; Copy and Download ask when items are pending; the pasted text is clean with citations.",
  "Empty, oversized, refused and model-failure states each keep her text or records, sit beside the input and offer one next step, with no sideways scroll at 390 in light or dark."
 ],
 "questions_for_chris": []}
```
