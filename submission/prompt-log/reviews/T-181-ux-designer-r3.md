# T-181 review, round 3: guided UI phone fixes (fix commit 2c19817), ux-designer-reviewer

Verdict: **pass** (0 blockers, 0 majors, 3 minors, 1 nit). Scores: design quality 4, originality 4, craft 4, functionality 4.

**Does it meet Chris's grandma bar?**
- **Desktop (1440x900): yes.** Nothing regressed. The keyboard run is the same, the edit path is the same, and the letter is byte-identical to r2's.
- **Phone (390x844): yes.** Both moments that failed in r2 now work.
  - On a disputed line she sees the highlighted words, the line with the outside words underlined, and the tick box together, with no scrolling (`T-181-ux-r3/a-lib10-e1-390x844.png`).
  - After a rewording she sees the same three things together (`a-e1-390x844-edit-to-check.png`).
  - A refused save shows its message above the action bar (`b-e1-390x844-refused-qualifier.png`).
- **Small iPhone (375x667): mostly, with one rough spot.**
  - The refusal is fully visible, together with her whole text.
  - On a disputed line, the highlighted words and the start of the line show together. But the tick box and its reason are below the action bar, and the Yes button is greyed with no reason on screen. She has to scroll the page to find out why (F1). Scrolling a page is normal on a phone, so I keep this at minor, as in r2.

## My 2 r2 majors, same scenarios (no scrolling by the probe)
| r2 major | 390x844 | 375x667 | Evidence |
|---|---|---|---|
| A: tick box shows, highlighted words hidden | **Fixed.** lib10 e1: the mark (y 223-269) is inside the window (y 193-347), the line (y 412-484) is below the header (bottom 402), and the box (y 599-627) is above the bar (top 659); elementFromPoint at the box returns the box. Sample e1 after a valid edit: mark y 235-332 in window y 193-347, line y 412-508, box y 602-630. | **Mark fixed; line and box are not in one view.** lib10 e1: the mark (y 223-269) is in the window, the line (y 458-530) runs under the bar (top 482), and the box is at y 691-719. Once the page is scrolled so the box clears the bar (scrollY 249), the mark is at y -26-20. Same pattern after an edit. Rated minor (F1); see note. | `T-181-ux-r3-majors.py`, `T-181-ux-r3-se.py`; `a-lib10-e1-{390x844,375x667}.png`, `se-lib10-375x667-scrolled.png`, `se-e1-375x667-edit-to-check-fresh.png` |
| B: refused edit behind the action bar | **Fixed.** The refusal (y 566-650) is above the bar (659) and the hit test returns itself. It says: "Not saved. Your line leaves out "complained of", which says whose account this is. Put it back in the line." The '45' refusal shows in the same place. But only the last line of her text is visible (F2). | **Fixed.** The refusal (y 390-473) is above the bar (482), and the whole editor (y 242-370) is visible. | `b-e1-390x844-refused-qualifier.png`, `b-e1-375x667-refused-qualifier.png` |

Note on A at 375x667: my r2 acceptance test named 375x667, and its line and box parts are still not met there. In r2 I rated the 375x667 tick-box problem separately as a minor, because the project's target is 390 px (checklist 17). I am keeping that severity rather than changing the rule in the last round. If Chris counts the iPhone SE in the grandma bar, F1 becomes a major (see questions).

## Regressions
- **None found.**
  - Sample case, mouse, walked item by item: 19 + 4 items with 0 px movement at 1440 and at 390, no stuck items and no console errors.
  - Keyboard only at 1440: the Tab counts are the same as r2 (5, 0, 3, then 0 per item, 1, 1, 1). The run took 26.7 s.
  - The letters downloaded at 390 and 1440, and the keyboard letter, are byte-identical to r2's (`diff` empty). The notes are identical too.
  - Edit path at 1440: both refusals, edit-to-check, Undo, and Step 4 still holding the downloads until items are decided. All unchanged.
- **Improved:** on the date-conflict item at 390, the record window now shows each record's highlighted sentence with "Show the whole of record N", and "Record 7 · Hill Country Pain" is visible at the bottom (`d2-s2-01.png`). That closes my r2 minor about Record 7 having no cue.
- **Deterministic check:** I ran `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q` on a fresh `git archive 2c19817`. It printed `139 passed in 187.23s`. Per the brief, I did not run or grade the 2 known HEAD failures, which come from backend wording.
- **Retraction:** my r2 minor "134 passed does not reproduce, 133 passed 1 failed" was a false finding. `git ls-tree -r --name-only 9ab8cae -- app/frontend | grep -c narrative` prints `0`. The narrative.js that failed the test came from a reused archive directory on my side.

```json
{"card": "T-181", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "fix commit 2c19817 (git archive 2c19817 into a new empty scratchpad dir t181r3-2c19817; HEAD = 2c19817 per git rev-parse --short HEAD); r2 baseline 9ab8cae; app at http://127.0.0.1:7906 (demo: LLM_BACKEND=fixture FIXTURE_SET=curated, own ZLAYT_DB) and http://127.0.0.1:7907 (same plus ZLAYT_MODE=local, only to create lib10 for the r2 scenario); stopped afterwards (PIDs 63184 and 63186 from lsof; both ports then answered 000); sample case evals/golden/sample.txt plus library case_lib10_eob_ub04_cms1500",
 "exercised": [
  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q on the fresh archive: '139 passed in 187.23s' (includes test_round3.py)",
  "r2 major A: T-181-ux-r3-majors.py creates a fresh lib10 case and opens e1 at 390x844, 375x667, 360x740 and 1440x900; for sample e1 after a valid edit at 390x844, 375x667 and 360x740 it records the rects of the record window, mark, line card header, line text, tick box, foot and action bar, plus elementFromPoint hit tests",
  "T-181-ux-r3-se.py at 375x667 and 390x844: lib10 e1 opened, the disabled Yes tapped and the status slot read, the page scrolled until the tick box clears the bar, then re-measured; sample e1 valid edit with no refusal first",
  "r2 major B: in T-181-ux-r3-majors.py, sample e1 -> Fix the wording -> 'complained of' dropped -> Save, then '45 mph' -> Save, at 390x844, 375x667 and 360x740; refusal rect against the bar top, hit test, editor rect against the line-card header",
  "Regression, mouse: T-181-ux-r3-explore.py (Home -> Open the sample case -> Draft) then T-181-ux-r3-walk.py for Step 2 (19 items) and Step 3 (4 amounts) at 1440x900 and 390x844: 0 px movement on every item, no ticks needed, no console errors",
  "Regression downloads: T-181-ux-r3-download.py at 390 and 1440; letter and notes diffed against T-181-ux-r2 files (identical); clipboard 2,728 chars",
  "Regression keyboard: T-181-ux-r3-keyboard.py at 1440 (Tab and Enter only), 26.7 s; kb1440-letter.txt equals r2's",
  "Regression edit path at 1440: T-181-ux-r3-edit.py (drop qualifier, 45 mph, valid edit -> tick box, accept, Undo, Decide later, Step 4 pending, letter has the edit)",
  "git ls-tree on 9ab8cae and 2c19817 for narrative.js (0 both); git show 2c19817 diff of review.js, review.css and styles.css",
  "Read reviews/T-181-ux-designer-r2.md, card T-181 notes and handoff (board.py show T-181), personas/ux-designer.md, tests/e2e/guided/test_round3.py"
 ],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 4, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor",
   "title": "375x667: on a disputed or reworded line, the tick box and its reason are below the action bar, and Yes is greyed with no reason on screen (carried from r2; the mark part is now fixed)",
   "evidence": "T-181-ux-r3-se.py. lib10 e1 at 375x667: the mark (y 223-269) is in the window (y 193-393), but the line (y 458-530) runs under the bar (top 482) and the box is at y 691-719, so hit = none. Tapping the disabled Yes leaves the status slot empty. After a page scroll to scrollY 249 the box (y 442-470) is clear but the mark is at y -26-20. Sample e1 after a valid edit: line y 415-511 and box y 630-658, with the bar at 482. Screenshots a-lib10-e1-375x667.png, se-lib10-375x667-scrolled.png, se-e1-375x667-edit-to-check-fresh.png. At 360x740 the box is also under the bar (y 586-614 vs 555 after an edit; y 604-632 on lib10). This does not violate the spec's 390 px target (checklist 17), so it is a preference. My r2 acceptance test named 375x667 and is not met there.",
   "why_it_matters": "On a small iPhone a first-time user sees a greyed Yes and nothing that says why. The tick box is reachable, but only by scrolling, and only after the highlighted words have scrolled away.",
   "fix": "On short phones, when the tick box shows, put a one-line cue in the status slot ('Tick the box under the line first'), and show the same cue when the greyed Yes is tapped. Or tighten the line card (smaller hint text and padding) so the box sits above the bar at 667 px.",
   "acceptance_test": "At 375x667 on lib10 e1 the check-compare box is in view above the action bar, or tapping the disabled Yes puts a sentence naming the tick box in the status slot."},
  {"severity": "minor",
   "title": "390x844: after a refused save, only the last line of her text shows; the top of the editor is under the line-card header",
   "evidence": "T-181-ux-r3-majors.py, sample e1, 'complained of' dropped, at 390x844: the editor is at y 419-547, the line-card header at y 434-512 (card scrollTop 218), so about 35 px of the editor shows: 'transported to Central ER.' (b-e1-390x844-refused-qualifier.png). The place where 'complained of' goes is hidden. At 360x740 the editor (y 315-443) is fully under the header (bottom 454). At 375x667 the page scrolls instead, and the whole editor and the message are visible (b-e1-375x667-refused-qualifier.png).",
   "why_it_matters": "The message now shows, which fixes the r2 major. But to act on 'Put it back in the line' she has to scroll the card back up to find where it goes. That is a hidden extra step on the correction path.",
   "fix": "In showRefusal(), scroll the card only far enough that the refusal's bottom is at the card's bottom, then keep the editor's top below the header. If both cannot fit, hide the hint paragraph ('Change the line so it says only ...') while a refusal shows.",
   "acceptance_test": "At 390x844, after a refused save on sample e1, the refusal is above the bar and the first line of edit-summary is below the line-card header (its top >= the header bottom)."},
  {"severity": "minor",
   "title": "Carried from r1/r2 and not done (per the handoff): provenance said twice in the Step 4 intro, 'After step 1' on every locked step, shortcut hint on every page, same-name cases, no case link, paste box under the sticky bar at 1440",
   "evidence": "The Step 4 intro at 2c19817 still reads 'Prepared by our team Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.' (T-181-ux-r3-edit.py output). The 1440 status slot still shows 'Keys: A says yes, D says no, E fixes or adds a note, the arrow keys move between items.' (T-181-ux-r3-majors.py, lib10 1440). The handoff says: 'minors from r2 not done (locked 'After step 1', shortcut hint, same-name cases)'. Same-name cases, case link and paste box were not re-tested.",
   "why_it_matters": "Repeated provenance teaches her to skip it. Identical locked-step lines hide the order of the steps. Multi-case use needs a way to tell cases apart.",
   "fix": "As in r2: one provenance sentence per page in plain words; 'After step 1/2/3'; settle the shortcut hint with the spec; start time on case cards and a 'Copy case link' button.",
   "acceptance_test": "As in r2."},
  {"severity": "nit",
   "title": "Case-404 page polish (carried from r2, not re-tested)",
   "evidence": "r2 evidence T-181-ux-r2/d1-23-case-404.png. The r3 diff touches only review.js, review.css and styles.css textarea sizing (git show 2c19817), so I assume it is unchanged.",
   "why_it_matters": "Small polish on a page she reaches from an old link.",
   "fix": "As in r2: centre the button, show no current step, say 'It may have been deleted, or it was started in another browser.'",
   "acceptance_test": "As in r2."}
 ],
 "whats_right": [
  "At 390x844, a disputed or reworded line shows the highlighted words, the line with the outside words underlined, and the tick box on one screen. The rect-based alignMark puts the mark at the top of the window. Keep it.",
  "A refused save is never under the action bar at 390 or 375, and the textarea no longer covers the card foot.",
  "No regressions: 0 px movement on all 23 items at both widths, the same keyboard Tab counts, byte-identical letter and notes, and 139 guided e2e tests passing on a fresh archive."
 ],
 "questions_for_chris": [
  "Is a 375x667 phone (iPhone SE, common among older users) part of the grandma bar? If yes, F1 (tick box below the action bar, greyed Yes with no reason in view) should be fixed before the gate."
 ]}
```
