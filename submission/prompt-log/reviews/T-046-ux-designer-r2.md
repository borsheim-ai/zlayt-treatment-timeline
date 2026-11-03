# T-046 round 2 review: side-by-side source viewer, ux-designer-reviewer

**Verdict: changes.** No blocker. One major (new in this round: the one-action summary link is one action only with a pointer). Three minors and one nit.

Scope: commit bc12d44 (round 2), exported with `git archive bc12d44` and served from scratch on http://127.0.0.1:7951 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, separate ZLAYT_DB). HEAD moved during the review to 172028c (T-097, T-083, T-090 commits); this review is pinned to bc12d44 as the card's commit. The repo-root tree was not used (`git status --short | wc -l` gave 259 uncommitted entries). `git worktree add` was refused by board-guard for reviewers, so the clean tree is a `git archive` export of bc12d44, which is the same content. The export and server were removed after use (server PID stopped; `curl` returns 000).

## Answers to the four questions

1. **Does the one-action link satisfy the round-1 acceptance test?** Partly. The second branch of the test ("a visible summary link focuses the gap flag in one action") is met for a pointer: at 1440x900 after the sample loads, "Show gap flag" is in the viewport at load (box x 1161, y 85, 117x36). One click focuses the gap flag row and the pane shows Records 6 and 7. Enter on the focused button does the same. For a keyboard user it is not one action: 190 Tab presses from the top of the document (F1). The gap flag itself is still far below the fold (F2). Because the acceptance test's pointer branch is now met, I lower the round-1 major to a minor residual (F2). F1 is new and is a major.
2. **Enter selects a row into the pane:** yes at 1440 and 1100. Enter on entry-8 sets the pane to "Record 8: Austin Imaging, cervical MRI", the highlight equals the excerpt, no modal opens, and j then moves the pane. At 1000 px Enter still does nothing (F4, round-1 minor still open).
3. **Single heading:** yes. The pane contains one heading for entry-8 (the title). Round-1 minor 3 is resolved.
4. **Overlay on a long record (the known issue):** confirmed, and wider than the library list. The fixed pane covers the right end of the Cases-list cards at the top of the page and the right 25 to 30% of the Load rows as the page scrolls (F3). The pane grows with the selected record (213 px empty, 330 to 393 px at 1440 with an item, 399 px at 1100), so the covered band grows too. The queue and excerpts are not covered. The longest library case (case_lib15, 9 records) gave short records (pane body scrollHeight equals clientHeight), so a long record that scrolls inside the pane was not exercised.

## Findings

### F1. major: the one-action summary link is not one action for a keyboard user
- Measured: Tab presses from the top of the document to `sbs-show-flag` at 1440x900 = 190. The pane is last in document order, after the export configuration fields (`cfg-exhibit`, `cfg-bates_prefix`, `cfg-bates_start`, `btn-save-config`, `btn-reset-config`). There is no keyboard accelerator for the gap flag, and `j` steps through queue items, not flags.
- Evidence: `artifacts/review-evidence/T-046-ux-designer-r2-keyboard-and-top-results.json` (`tab_presses_to_show_flag_1440`: 190; `tab_sequence_last_5_before_flag`). Script: `artifacts/review-evidence/T-046-ux-designer-r2-keyboard-and-top.py`.
- Why it matters: the round-1 acceptance test and checklist item 7 expect keyboard-first reviewers to reach the flag in one action. A pointer user can, a keyboard user needs about 190 presses. The sample-case gap is the headline flag.
- Fix: move the pane's flag link to the start of the review region in DOM order (the pane is `position: fixed`, so visual placement does not change), and add a keyboard accelerator for the next gap flag (for example `g`), listed in the on-screen legend at `app/frontend/review.js:240`.
- Acceptance test: Playwright from document start at 1440x900: Tab count to `sbs-show-flag` is 5 or fewer, or one key press (`g`) focuses the first `[data-flag-type=gap]` row; the legend text contains that key.

### F2. minor (residual of round-1 major): the gap flag is still below the fold
- Measured at bc12d44 after the sample loads: gap flag doc y 4974 px at 1440 (bottom 5525), 5180 px at 1100, 5425 px at 1000. The page map at 1440 shows the case stepper (y 2153), judge panel (y 2225), queue (y 2420 to 4660) and then the flags panel (y 4874). Checklist item 19 ("visible without scrolling at 1440x900") is not met.
- Cause of the growth: round 1 measured 3684 px at 5616dc3. Between 5616dc3 and bc12d44 the only frontend commit outside T-046 is e92b6ed (T-081 r3 / T-082 r3), which changed `stepper.js` (200 lines) and `judges.js`. The T-046 diff does not change the queue or the flags panel (queue 926 px wide, 2240 px tall at 1440).
- Status: the round-1 acceptance test is met by the pointer link (F1 covers the keyboard gap), so the finding drops from major to minor. Checklist item 19 literal remains open and belongs on a separate card.
- Evidence: `artifacts/review-evidence/T-046-ux-designer-r2-results.json` (`layout.1440.gap_flag_box_at_top_of_page`, `layout.1100`), `artifacts/review-evidence/T-046-ux-designer-r2-overlap-click-results.json` (`runs.1000.gap_flag_doc_y` 5425), `artifacts/review-evidence/T-046-ux-designer-r2-overlay-results.json` (`page_map_1440`), `git log --oneline 5616dc3..bc12d44 -- app/frontend`.
- Fix: as round 1: a flag summary in the case-summary row, or collapse the library and case lists once a case is open. Separate card.
- Acceptance test: at 1440x900 after the sample loads, either the gap flag bottom is 900 px or less, or `sbs-show-flag` is in the viewport and one click focuses the gap flag.

### F3. minor (new in bc12d44): the fixed pane covers case cards and library rows while the page scrolls
- Top of page, sample loaded, scroll 0: "Open now: Sample case" card is 27% under the pane at 1440 (its right-edge point hits the pane) and 23% at 1100. Its meta line is not under the pane in that card; a second card in the same run is under the pane with its meta line.
- Scrolling: at 1440 with an empty pane (213 px tall), Load rows are 19 to 27% under the pane for scroll 400 to 1700. With an item selected (330 px) they are 25 to 27% under it (right-edge hit PANE) for scroll 300 to 1500. At 1100 with a selected item (399 px) 25 to 30% of each Load row is under the pane for scroll 500 to 1500. The label text (`.cs-meta`) is under the pane for many rows.
- Not a blocker: the queue and excerpts are not covered (queue right edge 1007 px, pane left edge 1050 px, `queue_rows_overlapping_pane` 0 at 1440 and 1100). The banner (0 to 40 px) is clear of the pane (top 48 px).
- Limit: a real mouse click on a covered row did not produce a clean result on my server (see exercised list). The click-through claim rests on elementFromPoint returning the pane at the right edge, not on a confirmed click.
- Evidence: `artifacts/review-evidence/T-046-ux-designer-r2-keyboard-and-top-results.json` (`top_1440`, `top_1100`), `artifacts/review-evidence/T-046-ux-designer-r2-overlay-selected-results.json` (sweeps at 1440 and 1100), `artifacts/review-evidence/T-046-ux-designer-r2-1440-load.png` (the "Open: case lib13" card cut at the pane edge at 1440), `artifacts/review-evidence/T-046-ux-designer-r2-1440-sample-scroll500-overlap.png`.
- Why it matters: the first screen shows a pane over the case list, and the right part of each case or library row (including its count or description line) is hidden while the pane is open. Right-edge clicks go to the pane.
- Fix: apply the pane's right margin to the switcher (it sits outside `main`, so `main` margin does not move it), or collapse the case list when a case is open. Keep the pane out of the switcher's box.
- Acceptance test: at 1440 and 1100, sample loaded and an item selected, for every visible `[data-testid^=case-]` and `[data-testid^=library-case]` button: `elementFromPoint` at its right-edge point is not inside `sbs-pane`, and its `.cs-meta` box does not intersect the pane box, at scroll 0, 500 and 1000.

### F4. minor (round-1 minor 2, still open below 1024 px): Enter does nothing at 1000 px
- Measured: at 1000x900, focus on `entry-8`, Enter: `record-modal` not visible, focus stays on entry-8. The pane is `display: none` below 1024, so the Enter handler in `sidebyside.js` never runs; `review.js` has no Enter branch.
- Evidence: `artifacts/review-evidence/T-046-ux-designer-r2-overlap-click-results.json` (`runs.1000`), `artifacts/review-evidence/T-046-ux-designer-r2-1000-enter-entry8.png`, walk check `1000.enter_opens_record_modal` FAIL in `artifacts/review-evidence/T-046-ux-designer-r2-results.json`.
- Why it matters: the test contract (tests/e2e/conftest.py docstring) says Enter opens the source record. At 1000 px it does nothing.
- Fix: bind Enter on a focused `[data-item-id]` row in `review.js` to open `record-modal` when the pane is not shown (the worker noted this is outside T-046's files).
- Acceptance test: at 1000 px, focus entry-8, press Enter: `record-modal` is visible.

### F5. nit (round-1 nit 4, still open): the legend does not list p, Esc or Enter
- The on-screen legend (`app/frontend/review.js:240`) reads "j next, k previous, a accept, e edit, d dismiss, r reset, o open the record, Shift+A accept all verified entries." It does not list p (focus the record), Esc (return to the row), or Enter (select into the pane at 1024 px and up).
- Fix: add "Enter or p focus the source record, Esc returns" to the legend.
- Acceptance test: the legend text contains "Enter", "p" and "Esc".

## Round-1 status
- Major (gap flag fold): residual minor (F2). The pointer link meets the acceptance test; the keyboard path does not (F1).
- Minor (Enter): partly resolved at 1024 px and up (Enter selects into the pane, verified at 1440 and 1100); still open below 1024 px (F4).
- Minor (double record heading): resolved (one heading, verified).
- Nit (p/Esc in the legend): still open (F5).

## Scores
- design quality: 3 (the pane is a clear reading surface, but it overlaps the case list on first load and at scroll)
- originality: 3 (standard master-detail with a floating pane)
- craft: 3 (no overflow at 1100 or 1440, no console or page errors, textContent path unchanged; overlap and keyboard order are unfinished)
- functionality: 3 (pointer link and Enter selection work at 1024 px and up; keyboard path to the gap flag and Enter below 1024 px are incomplete)

## Exercised
- `python3 tools/board.py show T-046` (ACs, round-2 handoff, commits 5616dc3 and bc12d44).
- `git show --stat bc12d44`; `git diff 5616dc3 bc12d44 -- app/frontend/sidebyside.css app/frontend/sidebyside.js`; `git log --oneline 5616dc3..bc12d44 -- app/frontend`; `git log --oneline bc12d44..HEAD` (HEAD now 172028c); `git status --short | wc -l` (259).
- `git worktree add` refused by board-guard; used `git archive bc12d44 | tar -x -C <scratch>/ux-r2-bc12d44` (same tree), server from that copy with `.venv/bin/python -m app.main` on PORT 7951, HOST 127.0.0.1, separate ZLAYT_DB in scratch; `/api/health` 200; server PID stopped; port 000; export removed.
- `artifacts/review-evidence/T-046-ux-designer-r2-walk.py` at 1440 and 1100 (and 1000 for Enter): Show gap flag click and keyboard Enter (focus lands on gap flag, pane shows Records 6 and 7); Enter on entry-8 (pane title Record 8, highlight equals excerpt, no modal, one heading); j after Enter moves the pane; gap flag box and queue metrics; 1000 Enter FAIL. Console errors 0, page errors 0. Result: `artifacts/review-evidence/T-046-ux-designer-r2-results.json`.
- `artifacts/review-evidence/T-046-ux-designer-r2-overlay.py`: scroll sweep 0 to 1700 at 1440 and 1100 with an empty pane (library rows under the pane, coverage, elementFromPoint at centre and right edge); sample page map at 1440. Result: `artifacts/review-evidence/T-046-ux-designer-r2-overlay-results.json`.
- `artifacts/review-evidence/T-046-ux-designer-r2-overlay-selected.py`: scroll sweep with an item selected (pane 330 px at 1440, 399 px at 1100), pane body scroll height. Result: `artifacts/review-evidence/T-046-ux-designer-r2-overlay-selected-results.json`.
- `artifacts/review-evidence/T-046-ux-designer-r2-overlap-click.py`: banner versus pane (0 to 40 px vs 48 px, no overlap); 1000 px: `sbs-show-flag` in the DOM but pane hidden, gap flag y 5425. The real-click part of this script was inconclusive (see below) and is not used as a finding. Result: `artifacts/review-evidence/T-046-ux-designer-r2-overlap-click-results.json`.
- `artifacts/review-evidence/T-046-ux-designer-r2-keyboard-and-top.py`: Tab count to `sbs-show-flag` (190) and the top-of-page covered cards at 1440 and 1100. Result: `artifacts/review-evidence/T-046-ux-designer-r2-keyboard-and-top-results.json`.
- Viewed screenshots: `artifacts/review-evidence/T-046-ux-designer-r2-1440-load.png`, `artifacts/review-evidence/T-046-ux-designer-r2-1440-sample-scroll500-overlap.png`, and the clip of the top-of-page card under the pane.
- Not verified: a real mouse click on a covered row. Two attempts were inconclusive: after a library click the element sat off-screen in the script, and the sample analysis stalled on one fresh server start (the server log was empty; the same load took 1.3 s on a warm server). I did not use either as evidence.
- Not exercised: a long record that makes the pane body scroll (every record I loaded was under 300 px); 390 px; the 500 KB and model-failure states; a timed keyboard-only versus mouse run; the full e2e suite (the worker ran it).

```json
{"card": "T-046", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 2, commit bc12d44 (pinned; HEAD moved to 172028c during the review), exported with git archive and served at http://127.0.0.1:7951 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local); sample case at 1440x900, 1100x900 and 1000x900; library case_lib15 for the overlay sweep; round-1 findings checked against reviews/T-046-ux-designer.md",
 "exercised": [
  "python3 tools/board.py show T-046 (ACs, round-2 handoff, commits 5616dc3 and bc12d44)",
  "git show --stat bc12d44; git diff 5616dc3 bc12d44 -- app/frontend/sidebyside.css app/frontend/sidebyside.js",
  "git log --oneline 5616dc3..bc12d44 -- app/frontend (e92b6ed touched stepper.js and judges.js)",
  "git log --oneline bc12d44..HEAD (HEAD is 172028c); git status --short | wc -l (259 at the repo root, not used)",
  "git worktree add refused by board-guard for reviewers; git archive bc12d44 | tar -x into scratch; server from that copy on PORT 7951 with a separate ZLAYT_DB; /api/health 200; server stopped by PID; port 000; export removed",
  "artifacts/review-evidence/T-046-ux-designer-r2-walk.py at 1440, 1100, 1000: Show gap flag click and keyboard Enter (focus on gap flag; Records 6 and 7 in pane); Enter on entry-8 (Record 8 title, highlight equals excerpt, no modal, one heading); j moves the pane; 1000 Enter does not open record-modal; console and page errors 0",
  "artifacts/review-evidence/T-046-ux-designer-r2-overlay.py: scroll sweep 0 to 1700 at 1440 and 1100 (empty pane): library rows under the pane, coverage, elementFromPoint at centre and right edge; sample page map at 1440",
  "artifacts/review-evidence/T-046-ux-designer-r2-overlay-selected.py: scroll sweep with an item selected (pane 330 px at 1440, 399 px at 1100); pane body scroll height equal to client height",
  "artifacts/review-evidence/T-046-ux-designer-r2-overlap-click.py: banner vs pane (no overlap); 1000 px sbs-show-flag present in DOM but pane hidden; real-click result inconclusive and not used",
  "artifacts/review-evidence/T-046-ux-designer-r2-keyboard-and-top.py: Tab presses from document start to sbs-show-flag = 190 at 1440; top-of-page covered cards at 1440 and 1100",
  "viewed artifacts/review-evidence/T-046-ux-designer-r2-1440-load.png, T-046-ux-designer-r2-1440-sample-scroll500-overlap.png and the top-of-page clip",
  "not exercised: a long record that scrolls inside the pane, 390 px, 500 KB paste, model failure, timed keyboard-only versus mouse run, full e2e suite"
 ],
 "verdict": "changes",
 "scores": {"design_quality": 3, "originality": 3, "craft": 3, "functionality": 3},
 "findings": [
  {"severity": "major",
   "title": "The one-action summary link to the gap flag is one action only for a pointer: 190 Tab presses from the top for a keyboard user, and no keyboard accelerator",
   "evidence": "artifacts/review-evidence/T-046-ux-designer-r2-keyboard-and-top-results.json: tab_presses_to_show_flag_1440 = 190; tab_sequence_last_5_before_flag = cfg-exhibit, cfg-bates_prefix, cfg-bates_start, btn-save-config, btn-reset-config (the pane is last in document order); script artifacts/review-evidence/T-046-ux-designer-r2-keyboard-and-top.py",
   "why_it_matters": "The round-1 acceptance test and checklist item 7 expect keyboard-first reviewers to reach the headline gap flag in one action. The link works for a pointer (artifacts/review-evidence/T-046-ux-designer-r2-results.json: after_show_flag_active.flag = gap), but a keyboard user has to tab through the whole queue and the export settings first.",
   "fix": "Move the pane's flag link to the start of the review region in DOM order (the pane is position fixed, so its visual place does not change). Add a keyboard accelerator for the next gap flag (for example g) and list it in the legend at app/frontend/review.js:240.",
   "acceptance_test": "Playwright from document start at 1440x900 after the sample loads: Tab presses to sbs-show-flag are 5 or fewer, or one key press (g) focuses the first [data-flag-type=gap] row; the legend text contains that key."},
  {"severity": "minor",
   "title": "Residual of round-1 major: the gap flag is still below the fold at 1440x900 (checklist item 19 literal unmet); growth comes from e92b6ed, not T-046",
   "evidence": "artifacts/review-evidence/T-046-ux-designer-r2-results.json layout.1440.gap_flag_box_at_top_of_page y = 4974.05 (bottom 5525); layout.1100 y = 5180.03; artifacts/review-evidence/T-046-ux-designer-r2-overlap-click-results.json runs.1000.gap_flag_doc_y = 5425; artifacts/review-evidence/T-046-ux-designer-r2-overlay-results.json page_map_1440 (flags-panel y 4874); round-1 f667f08 3609.5 and 5616dc3 3684.2 in reviews/T-046-ux-designer.md; git log 5616dc3..bc12d44 -- app/frontend lists e92b6ed (stepper.js, judges.js)",
   "why_it_matters": "The headline 73-day gap is not visible without scrolling about 4,100 px at 1440x900. The round-1 acceptance test is met for a pointer through the summary link (F1 covers keyboard), so the finding drops from major to minor; checklist item 19 literal stays open.",
   "fix": "As round 1: put a flag summary in the case-summary row, or collapse the library and case lists once a case is open. Separate card; T-046 should not widen the gap.",
   "acceptance_test": "At 1440x900 after the sample loads: either the gap flag bottom is 900 px or less, or sbs-show-flag is in the viewport and one click focuses the gap flag."},
  {"severity": "minor",
   "title": "The fixed pane covers the right part of the case-list cards at the top of the page and of the library rows while scrolling (new in bc12d44)",
   "evidence": "artifacts/review-evidence/T-046-ux-designer-r2-keyboard-and-top-results.json top_1440: 'Open now: Sample case' card 27% under the pane, right-edge point hits PANE; top_1100: 23% under the pane. artifacts/review-evidence/T-046-ux-designer-r2-overlay-selected-results.json: Load rows 25 to 30% under the pane, right-edge hit PANE, at scroll 300 to 1500 (1440, pane 330 px) and 500 to 1500 (1100, pane 399 px). artifacts/review-evidence/T-046-ux-designer-r2-1440-load.png: the 'Open: case lib13' card cut at the pane edge.",
   "why_it_matters": "The pane sits over the switcher, which is outside main, so the main-column margin does not move it. While it is open, the right part of each case or library row, including its count or description line, is hidden, and clicks on that part land on the pane. The queue and excerpts are not covered (queue right 1007 px, pane left 1050 px, queue_rows_overlapping_pane 0), so this is not a blocker.",
   "fix": "Apply the pane's right margin to the switcher as well as main, or collapse the case list once a case is open, so the pane never sits over a clickable row.",
   "acceptance_test": "At 1440 and 1100, sample loaded and an item selected: for every visible [data-testid^=case-] and [data-testid^=library-case] button, elementFromPoint at its right-edge point is not inside sbs-pane, and its .cs-meta box does not intersect the pane box, at scroll 0, 500 and 1000."},
  {"severity": "minor",
   "title": "Round-1 minor, still open below 1024 px: Enter on a focused queue row does nothing at 1000 px",
   "evidence": "artifacts/review-evidence/T-046-ux-designer-r2-overlap-click-results.json runs.1000 and enter_1000: record-modal not visible, active element stays entry-8; artifacts/review-evidence/T-046-ux-designer-r2-results.json checks 1000.enter_opens_record_modal FAIL; artifacts/review-evidence/T-046-ux-designer-r2-1000-enter-entry8.png; tests/e2e/conftest.py docstring says Enter = open source record",
   "why_it_matters": "The test contract and the product disagree below 1024 px. Keyboard-first reviewers on a narrower window press Enter and nothing happens. Enter works at 1024 px and up (fixed in this round).",
   "fix": "In review.js, bind Enter on a focused [data-item-id] row to open record-modal when the side-by-side pane is not shown. This sits outside T-046's files, so it needs its own owner.",
   "acceptance_test": "At 1000 px: focus entry-8, press Enter; record-modal is visible."},
  {"severity": "nit",
   "title": "Round-1 nit, still open: the on-screen legend does not list p, Esc or Enter",
   "evidence": "app/frontend/review.js:240 legend text: 'j next, k previous, a accept, e edit, d dismiss, r reset, o open the record, Shift+A accept all verified entries. Tab reaches every button.'",
   "why_it_matters": "The pane header says 'p moves here, Esc returns', and Enter now selects a row into the pane at 1024 px and up, but a keyboard user reading the legend finds neither.",
   "fix": "Add 'Enter or p focus the source record, Esc returns' to the legend.",
   "acceptance_test": "The legend text contains 'Enter', 'p' and 'Esc'."}
 ],
 "whats_right": [
  "The Show gap flag button is visible at load at 1440x900 (box x 1161, y 85) and one click focuses the gap flag and shows Records 6 and 7 in the pane; Enter on the focused button does the same.",
  "Enter on a focused queue row selects it into the pane at 1440 and 1100: title Record 8, highlight equal to the excerpt, no modal, one Record 8 heading, and j then moves the pane.",
  "The queue keeps its full width (926 px at 1440, nothing under the pane), there is no horizontal overflow at 1440 or 1100, and console and page errors are 0."
 ],
 "questions_for_chris": [
  "Is the Load and Open case list (a local-mode switcher, outside the demo path) in scope for the pane overlap in F3, or may it be cut from M3 with a note?",
  "Should the keyboard route to the gap flag (F1) be a must-have for M3, given that checklist item 7 asks for keyboard equivalents and the flag is the headline item?"
 ]}
```
