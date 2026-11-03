# T-042 round 2 UX review (ux-designer-reviewer)

Verdict: changes. No blockers. The round-1 major is only partly fixed: the count line reconciles on the sample case but still contradicts the screen on case_01, so it is re-filed as a major below. Of the round-1 minors, the false red alert on tray records is fixed, as are the chip labels, Analyze-during-run, and the sticky-banner overlap; the record-list focus order and the Why? vocabulary are partly fixed and carried as minors. The round-1 nit (duplicate heading) is fixed.

Scope: commit 348cd0b (app/frontend: input.js, source.js, styles.css, timeline.js), served with `.venv/bin/python -m http.server 7867 --directory app/frontend`, `?api=mock`, sample case plus `evals/golden/case_01_date_formats.txt`, 1280x900 and 375x812. Real backend not exercised.

Round-1 status:
- Major, counts do not reconcile: sample case FIXED; case_01 NOT FIXED, reopened as the new major below.
- Minor, false red alert from tray: FIXED.
- Minor, record list pushes timeline down / first focusable is the sort menu: PARTLY (list collapsed; sort select still first).
- Minor, two state chips ambiguous: FIXED ("Not reviewed yet" chip).
- Minor, Analyze clickable during run: FIXED (hidden while running).
- Minor, sticky banner covers focus: FIXED at 375 (64 px banner, 90 px scroll margin, no overlapped focus stop).
- Minor, Why? developer vocabulary: PARTLY (title and labels renamed; prompt versions and "tokens" still in the main list).
- Nit, duplicated modal heading: FIXED.

Key outputs (full output: artifacts/review-evidence/T-042-r2-ux-designer-check.out.json and the console of the kbd script):

```
1280 A1 review-counts text => "9 entries · 1 needs review · 8 verified"
1280 A2 rows total/needs_review/verified => [9, 1, 8]
1280 A2 header reconciles with rows => true
1280 E2 role=alert inside record-modal => 0
1280 E2 role=alert on page after opening tray record => 12   (hidden nodes; see next line)
VISIBLE role=alert before tray open: []   VISIBLE role=alert after tray open: []   (1280 and 375)
1280 E3 control bad-offset span: role=alert inside modal => 1   (real failure still alerts)
CASE01 review-counts: 2 entries · 0 needs review · 2 verified
CASE01 undated rows (data-state): ['needs_review', 'needs_review', 'needs_review', 'needs_review', 'needs_review', 'needs_review']
KBD path: ["SUMMARY:Records (9)", "start-over:Start over", "sort:Needs review firstBy d", "entry-3[row]:2026-01-16Dr. Alvarez,"]
1280 A4 first needs_review row top => 444.5   (round 1: 624)
375  A4 first needs_review row top => 563.5   (round 1: 955)
1280 F1 during run => analyze_buttons 0 at t=0, 300, 700 ms; stage "Checking summaries 0 of 9"
375 D1 banner box => bottom 64; focused elements overlapped by sticky banner => []
```

Findings are below. Screenshots: artifacts/review-evidence/T-042-r2-{1280,375}-*.png.

```json
{"card": "T-042", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 348cd0b (app/frontend/input.js, source.js, styles.css, timeline.js); app served on http://localhost:7867/index.html?api=mock (mock API, not the real backend on :7860); sample case (evals/golden/sample.txt) and evals/golden/case_01_date_formats.txt; 1280x900 and 375x812",
 "exercised": [
  "Read personas/ux-designer.md, reviews/T-042-ux-designer.md (round 1), artifacts/review-evidence/T-042-ux-designer-walk.py (hardcodes :7865 and overwrites T-042-* evidence, so not re-run; replaced by T-042-r2-ux-designer-walk.py and T-042-r2-ux-designer-kbd.py)",
  "git show 348cd0b --stat (4 files, 23 insertions, 15 deletions) and git show 348cd0b -- app/frontend/ diff",
  "python3 tools/board.py show T-042: status in_review, commits include 348cd0b",
  "curl http://localhost:7867/index.html?api=mock -> 200; python3 -m http.server 7867 --directory app/frontend",
  "Playwright 1280x900 and 375x812, sample case: review-counts text vs queue rows (data-state), review-status and state chip texts, dates-to-confirm and tray text, first focusable in #view-review, records details collapsed state, first needs_review row y-position, horizontal scroll, console errors",
  "Playwright: Why? on entry 7 (title, ladder text, modal text), entry 8 Open record (h3 count, role=alert count), 12 Tab stops with sticky-banner overlap check",
  "Playwright: ?fail=4 tray 'Open record 4' (modal open, role=alert inside and on page, visible role=alert before/after), control span with start=-5 to confirm the real alert still fires",
  "Playwright: Analyze button count and stage text at 0, 300, 700 ms during a run",
  "Playwright: keyboard-only Tab path from page top to first needs_review row (1280)",
  "Playwright: case_01 paste, review-counts, queue rows, dates-to-confirm rows and states",
  "Playwright: empty submit and 600 KB submit (input-side regression; alert text and textarea length 600017 kept)"],
 "verdict": "changes",
 "scores": {"design_quality": 3, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "major",
   "title": "Count line reconciles on the sample case but not on case_01: header says 0 need review while six Needs review items sit below it",
   "evidence": "CASE01 review-counts: '2 entries · 0 needs review · 2 verified'; CASE01 undated rows (data-state): ['needs_review' x6]; dates-to-confirm chips read 'Needs review' / 'Not reviewed yet' (artifacts/review-evidence/T-042-r2-1280-10-case01-counts.png). Sample case is fine: '9 entries · 1 needs review · 8 verified' vs rows [9, 1, 8] (T-042-r2-1280-01-results-header.png).",
   "why_it_matters": "The round-1 major was a count that cannot be reconciled with what is on screen. The round-2 fix counts timeline entries only, which is correct for the sample, but the only status line still says zero need review on a screen that shows six items marked Needs review. Checklist 6 and 'how many remain' are misstated for the paste path that produces Dates to confirm. Visibility of system status; calibrated trust.",
   "fix": "Include the Dates to confirm items in the same line, e.g. '2 entries · 0 need review · 6 dates to confirm', or add 'Dates to confirm: 6 need review' to the same toolbar. Keep the sample case output unchanged.",
   "acceptance_test": "E2E with case_01 paste: needs-review number in review-counts (plus any dates-to-confirm count) equals the number of [data-state=needs_review] rows on screen across timeline and Dates to confirm (6 in this case). E2E with sample: 1 equals the one needs_review row."},
  {"severity": "minor",
   "title": "The Order select is still the first focusable control in the review region (round-1 minor, partly fixed)",
   "evidence": "A4 first focusable in #view-review => '<select data-testid=\"sort\">...'; KBD path from page top: ['SUMMARY:Records (9)', 'start-over:Start over', 'sort:Needs review firstBy d', 'entry-3[row]:2026-01-16Dr. Alvarez,'] (4 Tabs). First needs_review row top: 444.5 px at 1280 (round 1: 624), 563.5 px at 375 (round 1: 955). Collapsing the records list is confirmed: details.reclist-wrap open=false.",
   "why_it_matters": "The collapse fixes the scroll position. Keyboard users still reach a sort control before the first item that needs them, which is checklist 19's first-focusable rule.",
   "fix": "Move the Order select after the queue, or make the first needs_review row the first tab stop inside #view-review.",
   "acceptance_test": "Sample run at 1280x900: first focusable element inside #view-review has data-state=needs_review; first needs_review row top < 450 px (already 444.5)."},
  {"severity": "minor",
   "title": "Why? panel still puts prompt versions and internal wording in the main list (round-1 minor, partly fixed)",
   "evidence": "1280 B1 why-ladder text => '...Drafted by / claude-sonnet-5-5 · extract_v1 ... Checks run by code / ... summary tokens not in excerpt: none ... Second check by another model / supported · claude-haiku-5-5 · judge_faithfulness_v1'. Title now 'Why? Hill Country Pain Management, new patient, 2026-05-18' (fixed); 'Model calls (2)' is collapsed (fine).",
   "why_it_matters": "The renamed labels help. The main view still carries prompt identifiers and the word 'tokens', which mean nothing to a paralegal and belong in Model calls. Not a spec violation; a should-fix.",
   "fix": "Move model and prompt_version lines under the collapsed Model calls details. Reword 'summary tokens not in excerpt' in plain words that match what the check does.",
   "acceptance_test": "why-ladder inner text (outside details) contains none of 'extract_v1', 'judge_faithfulness_v1', 'tokens'."}
 ],
 "whats_right": [
  "Tray 'Open record 4' opens the whole record with no role=alert (E2: 0 inside record-modal; 0 visible alerts before or after), and a real bad span still alerts (E3: 1), so the fix did not suppress genuine failures.",
  "Count line matches the rows on the sample case (9 entries, 1 needs review, 8 verified) and the Needs review rows carry a visible 'Check:' reason.",
  "Analyze is removed while a run is in progress and the stage text shows from the first poll ('Starting…', then 'Checking summaries 0 of 9'); the 375 sticky banner no longer covers any of 12 Tab stops."],
 "questions_for_chris": ["Should the review header's needs-review number include the Dates to confirm items (6 on case_01), or should that group keep its own labelled count? The fix for the major depends on this product call."]}
```
