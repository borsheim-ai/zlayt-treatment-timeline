# T-046 review: side-by-side source viewer (R-ST-1), ux-designer-reviewer

**Verdict: changes.** No blocker. One major (pre-existing, made 75 px worse by this card). Two minors.

Scope: commit 5616dc3, exported with `git archive` to a scratch directory and served on http://127.0.0.1:7888 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local). The repo-root working tree was NOT used: `git status --short` showed 269 uncommitted changes there, and HEAD moved during the review (5616dc3 → e92b6ed → e2b4e3f). An earlier walk and an earlier e2e run against the repo-root tree are discarded. Their judge-panel failure (`test_judge_panel_one_row_per_item_with_record_cue`, "f_r5_1 has no Record cue") does not reproduce on the 5616dc3 export and is not caused by T-046. `T-046-ux-designer-probe-judge-title.py` came from that dirty run and is superseded.

## What works (AC by AC)
- **AC1, record beside the queue with the excerpt highlighted (1280 and 1440):** every entry (e1 to e9) shows a highlight whose text equals its excerpt, with no missing-highlight alert. The 73-day gap flag shows Records 6 and 7. `j` moves focus and the pane follows, three times in a row. Evidence: `artifacts/review-evidence/T-046-ux-designer-walk-results.json`, `artifacts/review-evidence/T-046-ux-designer-1440-entry8-highlight.png`.
- **AC2, mobile fallback:** at 1000 px and 1023 px the pane is hidden and `body.sbs-on` is absent. The row click does not open the modal. `btn-source` and `o` open the modal with the highlight equal to the excerpt. The pane appears at 1024 px exactly. At 390 px there is no horizontal scroll and no pane.
- **AC3, no backend change:** `git show --stat 5616dc3` lists only `app/frontend/{index.html,sidebyside.css,sidebyside.js}`, `tests/e2e/{conftest.py,test_side_by_side.py}` and four PNGs.
- **Text as text:** `sidebyside.js` contains no `innerHTML` (the single match is in a comment). `dom.js` `ZL.el` appends strings with `createTextNode`. A route-rewrite probe put `<img src=x onerror="window.__xss=1"><b>BOLD</b>` into `source_label`. It rendered as literal text, `window.__xss` stayed undefined, and the pane had 0 `img` and 0 `b` elements (`T-046-ux-designer-textcontent-probe.json`).
- **Stepper and judge panel unaffected:** at 1440 and 1000 the case stepper opens with 10 steps, the item stepper opens from the gap flag, and the judge panel opens with 6 rows, each title carrying a Record cue.
- **No overflow:** `scrollWidth == clientWidth` at 1024, 1100, 1280 and 390 px. Console errors 0, page errors 0.

## Findings

### 1. major: gap flag is not visible without scrolling at 1440x900 (checklist item 19)
Pre-existing at f667f08. T-046 narrows the main column from 926 px to 788 px at 1440, which pushes the gap flag 75 px lower. Measured on the 1440 sample load: flags-panel y 3,498 px, gap flag y 3,684 px (bottom 4,258 px). The queue is 2,312 px tall. The Records card and the library list sit above it. The pane only appears after the user selects something, so it does not help find the flag.
Evidence: `artifacts/review-evidence/T-046-ux-designer-baseline-compare.json` (`1440_gap_flag_box`: f667f08 y 3609.5, 5616dc3 y 3684.2), `artifacts/review-evidence/T-046-ux-designer-1440-results.png`.
Why it matters: the 73-day gap is the headline flag. A paralegal on a 1440x900 screen has to scroll about 3,700 px to see it.
Fix: put a flag summary in the case summary row with a link that focuses the first gap flag (for example "1 gap flag · Show"), or move the flags summary above the queue. Collapse the library list once a case is loaded. This can be a separate card. T-046 should not widen the gap.
Acceptance test: at 1440x900 after the sample case loads, either the gap flag's bounding box bottom is at or below 900 px, or a visible summary link focuses the gap flag in one action. Playwright asserts it.

### 2. minor: Enter on a focused queue row does nothing (pre-existing; the test contract says it should)
Walk check `1000.enter_opens_modal` fails. `T-046-ux-designer-baseline-compare.json` shows `1000_enter_on_row_opens_modal: false` at both f667f08 and 5616dc3. The keydown handler (`app/frontend/review.js:243` onward) has no Enter branch. `tests/e2e/conftest.py` docstring says "Keyboard (when a queue row is focused): ... Enter = open source record". The on-screen legend (`review.js:240`) lists `o open the record` and not Enter.
Why it matters: the contract and the product disagree. Keyboard-first reviewers will press Enter.
Fix: bind Enter to open the record on a focused `[data-item-id]` row, or remove Enter from the contract and keep `o` as the documented key.
Acceptance test: at 1000 px, focus `entry-8` and press Enter. Assert `record-modal` is visible. Or correct the docstring and assert the `o` path only.

### 3. minor: the pane shows the record name twice
Under the pane title "Record 8 (source of the selected item)" there is a section heading "Record 8: Austin Imaging, cervical MRI" (`sidebyside.js` `recordSection`). Two headings say the same thing above the record text.
Evidence: `artifacts/review-evidence/T-046-ux-designer-1440-entry8-highlight.png`.
Fix: keep one heading for single-record items. Keep the pane title, which also covers two-record flags.
Acceptance test: for entry-8 the pane contains exactly one heading that starts with "Record 8".

### 4. nit: p and Esc are discoverable only from the pane header
The pane header says "Press p to move here, Esc to return." The on-screen keyboard legend (`review.js:240`) does not list `p` or `Esc`. This is acceptable, but a keyboard-first user will find it from the legend.
Fix: add `p focus source record` to the legend.

## Scores
- design quality: 4 (clear two-pane layout, sticky pane, highlight is legible, no layout breaks at 1024 to 1440)
- originality: 3 (standard master-detail, applied well)
- craft: 4 (textContent path, no console errors, exact 1023/1024 boundary, 45 tests green on the clean export)
- functionality: 4 (all three ACs met; Enter and the gap-flag fold are the gaps)

## Exercised
- `python3 tools/board.py show T-046` (ACs, commit 5616dc3)
- `git show --stat 5616dc3`, `git diff --stat f667f08 5616dc3`, `git status --short` (269 uncommitted changes at repo root; HEAD moved to e92b6ed, then e2b4e3f)
- `git archive 5616dc3` and `git archive f667f08` extracted to scratchpad; app started from each with `python -m app.main` (PORT 7888 and 7882, separate ZLAYT_DB)
- `E2E_BASE_URL=http://127.0.0.1:7888 .venv/bin/python -m pytest tests/e2e/test_side_by_side.py -v`: 7 passed
- `... pytest tests/e2e/test_stepper.py tests/e2e/test_source_record.py tests/e2e/test_keyboard_mobile.py tests/e2e/test_timeline.py tests/e2e/test_flags_panel.py tests/e2e/test_charges.py -q`: 38 passed
- `artifacts/review-evidence/T-046-ux-designer-walk.py` (Playwright, 32 checks at 1440, 1000, 1023, 1024, 390, and the judge panel on lib06): 30 pass, 2 fail (findings 1 and 2)
- `artifacts/review-evidence/T-046-ux-designer-baseline-compare.py` (f667f08 vs 5616dc3)
- `artifacts/review-evidence/T-046-ux-designer-textcontent-probe.py` (markup in `source_label`, 1440 and 1000)
- Keyboard path: `j` x3, `p`, `Esc`, `o` (1440); `o`, `Enter` (1000)
- Viewed `artifacts/screenshots/sidebyside-1280-entry8.png` (matches my 1440 capture) and my own captures under `artifacts/review-evidence/T-046-ux-designer-*.png`
- Servers on 7882, 7883 and 7888 stopped; `curl` returns 000 on all of them

Not exercised: a 500 KB paste or model failure (not in this card's scope); the full `tests/e2e` suite; a timed keyboard-only vs mouse run.

```json
{"card": "T-046", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 5616dc3 (T-046, R-ST-1), exported with git archive and served at http://127.0.0.1:7888 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local); sample case (btn-sample / API sample) at 1440x900, 1024, 1100, 1280, 1000, 1023 and 390 px; library case case_lib06_lop_billed_vs_adjusted for the judge panel; baseline f667f08 for regression comparison",
 "exercised": [
  "python3 tools/board.py show T-046 (ACs, commit 5616dc3)",
  "git show --stat 5616dc3; git diff --stat f667f08 5616dc3; git status --short (269 uncommitted changes at repo root, so the repo-root tree was not used)",
  "git archive 5616dc3 and f667f08 extracted to scratchpad and served with python -m app.main on :7888 and :7882",
  "E2E_BASE_URL=http://127.0.0.1:7888 pytest tests/e2e/test_side_by_side.py -v: 7 passed",
  "pytest tests/e2e/test_stepper.py test_source_record.py test_keyboard_mobile.py test_timeline.py test_flags_panel.py test_charges.py on :7888: 38 passed",
  "artifacts/review-evidence/T-046-ux-designer-walk.py on :7888: 32 checks, 30 pass, 2 fail (gap flag fold at 1440x900; Enter on row below 1024)",
  "artifacts/review-evidence/T-046-ux-designer-baseline-compare.py on :7882 (f667f08) and :7888 (5616dc3): gap flag y and Enter behaviour",
  "artifacts/review-evidence/T-046-ux-designer-textcontent-probe.py on :7888: markup in source_label rendered as literal text, not executed, 0 img/b in pane",
  "keyboard: j x3, p, Esc, o at 1440; o, Enter at 1000; charge row and gap flag clicks move the pane",
  "layout: scrollWidth == clientWidth at 390, 1024, 1100, 1280; pane visible at 1024 and hidden at 1023",
  "viewed artifacts/screenshots/sidebyside-1280-entry8.png and artifacts/review-evidence/T-046-ux-designer-{1440,1000}-*.png",
  "console errors 0 and page errors 0 across the walk; servers on 7882, 7883, 7888 stopped"
 ],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "major",
   "title": "Gap flag is not visible without scrolling at 1440x900 (checklist item 19); pre-existing, and T-046 adds 75 px",
   "evidence": "artifacts/review-evidence/T-046-ux-designer-baseline-compare.json: 1440_gap_flag_box y 3609.5 at f667f08, y 3684.2 at 5616dc3; queue height 2312; artifacts/review-evidence/T-046-ux-designer-1440-results.png (library list and Records card above the queue)",
   "why_it_matters": "The 73-day gap is the headline flag. On a 1440x900 screen the paralegal must scroll about 3,700 px to reach it. The pane appears only after a selection, so it does not help find the flag. T-046 narrows the column from 926 to 788 px and pushes the flag 75 px lower.",
   "fix": "Add a flag summary to the case summary row with a link that focuses the first gap flag (for example '1 gap flag · Show'), or move the flags summary above the queue. Collapse the library list once a case is loaded. This may be a separate card; T-046 should not widen the gap.",
   "acceptance_test": "At 1440x900 after the sample case loads, either the gap flag bounding box bottom is <= 900, or a visible summary link focuses the gap flag in one action. Playwright asserts it."},
  {"severity": "minor",
   "title": "Enter on a focused queue row does nothing; the test contract says it opens the record (pre-existing)",
   "evidence": "artifacts/review-evidence/T-046-ux-designer-walk-results.json check 1000.enter_opens_modal = FAIL; artifacts/review-evidence/T-046-ux-designer-baseline-compare.json 1000_enter_on_row_opens_modal = false at f667f08 and 5616dc3; app/frontend/review.js:243 (keydown has no Enter branch); tests/e2e/conftest.py docstring 'Enter = open source record'; review.js:240 legend lists 'o open the record' and not Enter",
   "why_it_matters": "The documented contract and the product disagree. Keyboard-first reviewers will press Enter on a row.",
   "fix": "Bind Enter to open the record on a focused [data-item-id] row, or remove Enter from the contract and keep o as the documented key.",
   "acceptance_test": "At 1000 px, focus entry-8 and press Enter; assert record-modal is visible. Or correct the docstring and assert only the o path."},
  {"severity": "minor",
   "title": "The pane shows the record name twice",
   "evidence": "artifacts/review-evidence/T-046-ux-designer-1440-entry8-highlight.png: pane title 'Record 8 (source of the selected item)' then section heading 'Record 8: Austin Imaging, cervical MRI' (app/frontend/sidebyside.js recordSection)",
   "why_it_matters": "Two headings say the same thing above the record text and use space in a pane that is only about 220 px tall.",
   "fix": "Keep one heading for single-record items. Keep the pane title, which also covers two-record flags.",
   "acceptance_test": "For entry-8 the pane contains exactly one heading that starts with 'Record 8'."},
  {"severity": "nit",
   "title": "p and Esc are discoverable only from the pane header",
   "evidence": "pane header text 'Press p to move here, Esc to return.' (artifacts/review-evidence/T-046-ux-designer-1440-pane-keyboard-focus.png); the on-screen legend at app/frontend/review.js:240 does not list p or Esc",
   "why_it_matters": "A keyboard-first user will look for the shortcut in the legend.",
   "fix": "Add 'p focus source record' to the legend.",
   "acceptance_test": "The legend text contains 'p' and 'Esc' near the source record entry."}
 ],
 "whats_right": [
  "Every entry's highlight equals its excerpt at 1440 (9 of 9), and a click, a j press, or a flag click moves the pane in one action.",
  "The pane sits beside the queue, is sticky, scrolls inside itself, and causes no overflow from 1024 to 1280 px and at 390 px; the 1023/1024 boundary is exact.",
  "Record text is inserted as text nodes: injected img/onerror markup showed as literal text and never ran."
 ],
 "questions_for_chris": [
  "The reviewer dossier and CLAUDE.md name claude-opus-5-5 for judgment reviewers. This review ran as claude-haiku-5-5, as the brief specified. Should UX judgment reviews run on Opus, or is Haiku acceptable for this card?",
  "Is checklist item 19 (gap flag visible at 1440x900) a required M3 gate item? It is filed as major and is pre-existing, so it may be scheduled as its own card."
 ]}
```
