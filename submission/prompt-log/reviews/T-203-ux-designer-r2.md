# T-203 round 2 review: Show box, hint beside "Saved", PT, lost wages (commit fa34fe9), ux-designer-reviewer

Verdict: **pass** (0 blockers, 0 majors, 1 minor, 3 nits). Scores: design quality 4, originality 4, craft 4, functionality 4.

**My r1 major (reworded line at 375x667) is fixed.**
- After "Fix the wording" on sample e1 at 375x667 the status slot now reads "Saved. Tick the box to say you compared them." beside a "Show box" button (y 627-663 in a bar 482-667). It was the same at +0 s, +5 s and +30 s. Yes stays greyed at y 531-581 and does not move.
- The box was behind the bar at y 630-658 (boxHit = status-text). Tapping "Show box" scrolls it to y 441-469, above the bar, focuses it, and hides the button. Ticking it enables Yes and the slot goes back to "Saved: your wording is in. Read it once more against the highlighted words." Unticking brings the hint back. Yes then reads "Saved: item 1 kept in the letter." and the next item loads.
- Keyboard: after the edit, focus is already on the box (activeIsBox true). Space ticks it, A says yes, and item 2 of 19 loads. Two keys.

**My r1 minor (the word "above") is fixed.** The words now read "Tick the box to say you compared them." (disputed line) and "Tick the box first." (generic box), with no direction word. On lib10 e1 at 375x667 the box is at y 691-719 (below the screen) and "Show box" is shown; tapping it puts the box at y 441-469. At 360x740 the box was behind Yes/No (y 604-632) and "Show box" puts it at y 493-521, above the bar at 555. At 390x844 and 1440x900 the box is already above the bar, so there is no button.

**"PT" and "Pt".** Run live through `window.G.step2.outsideParts`:
- quote "PT 3x/week, attended physical therapy", line "Patient attended physical therapy 3 times a week" underlines Patient, 3, times. "Patient" is now marked.
- quote "Pt states chest pain" and "pt states chest pain" with line "Patient states chest pain" underline nothing, as intended.
- quote "PT states chest pain" underlines Patient. A line "Pt ..." against a quote "PT ..." underlines Pt.
- lib11 e2 (a real "Pt" quote) at 390, 375 and 1440: underlined words are after, passenger, vehicle, struck, from, behind; "Patient" is not underlined.

**"Lost wages".** lib11 a6 at 375, 390 and 1440 reads "A second AI check thought this may be a damages figure (for example lost wages), not what it was first sorted as." "lost pay" and "not a bill" are absent from the page text.

**Regressions at 390 and 1440: none found.**
- lib10 e1 at 390x844: mark y 223-269, box 599-627, bar 659, Yes 708-758, same as r1 and T-181 r3. Sample e1 after a valid edit at 390: box 602-630, as in r3; the hint is one line (18 px), no "Show box".
- 1440x900: Yes y 782-838 in every state. The keys line returns after the tick. Lines with no box (lib10 e2 at 375 and 1440) show no hint and no "Show box".
- Deterministic: `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q` on a fresh `git archive fa34fe9` printed `145 passed in 187.87s (0:03:07)`.

## Findings
- **F1 (minor):** "Show box" scrolls the highlighted words mostly off the top and clips the box label's second line behind the bar.
- **F2 (nit):** "PT's" and "PTs" still map to "patient".
- **F3 (nit):** the hint is 13 px at 375 and "Show box" is 34 px high; r1 asked for 15 px. Touch-target size is for accessibility-reviewer.
- **F4 (nit):** on the reworded line, "Read it once more against the highlighted words" now appears only after she has ticked the box.
- Carried over, not touched by this card (handoff says so): the "Step 3 of 4" label wraps to three lines at 375x667 (3-lib11-a6-375x667.png). It stays a nit.

```json
{"card": "T-203", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit fa34fe9 (git archive fa34fe9 into new empty scratchpad dir ux-t203r2-fa34fe9; git rev-parse --short HEAD printed fa34fe9); demo app http://127.0.0.1:7993 (LLM_BACKEND=fixture FIXTURE_SET=curated, own ZLAYT_DB) and http://127.0.0.1:7994 (same plus ZLAYT_MODE=local, to create lib10 and lib11); both stopped afterwards (PIDs 15794 and 15796 from lsof; ports 7993 and 7994 then answered 000); sample case evals/golden/sample.txt plus library cases case_lib10_eob_ub04_cms1500 and case_lib11_priors_and_ledger",
 "exercised": [
  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q on the fresh archive: '145 passed in 187.87s (0:03:07)' (includes tests/e2e/guided/test_t203.py)",
  "artifacts/review-evidence/T-203-ux-r2-measure.py (output artifacts/review-evidence/T-203-ux-r2/measure.out): sample e1 'Fix the wording' then tick at 375x667 read at +0, +5 and +30 s, tapped the greyed Yes, tapped Show box, ticked, unticked, ticked and said Yes; same edit path at 390x844, 360x740 and 1440x900",
  "same script: lib10 e1 (disputed line) at 375x667, 360x740, 390x844 and 1440x900 (open, Show box, tick, untick, rects of mark/line/box/bar); lib10 e2 (no box) at 375 and 1440; lib11 a2 (generic 'Tick the box first.') at 375x667",
  "same script: window.G.step2.outsideParts called live with 10 PT / Pt / pt / PT's / Dx quote and line pairs; lib11 a6 second-check wording and a page-text search for 'lost pay', 'lost wages' and 'not a bill' at 375, 390 and 1440; lib11 e2 outside-word underlines at 390, 375 and 1440",
  "artifacts/review-evidence/T-203-ux-r2-kbd.py: keyboard on the edit path at 375x667 (focus after the edit is the box; Space; A; next item)",
  "read the screenshots 1-edit-375x667-after-edit.png, 1-edit-375x667-after-showbox.png, 2-lib10-e1-375x667-open.png, 2-lib10-e1-375x667-showbox.png and 3-lib11-a6-375x667.png in artifacts/review-evidence/T-203-ux-r2/",
  "git show fa34fe9 (review.js drawStatus, boxHidden, revealBox; step2.js stem; test_t203.py); board.py show T-203 for the handoff; read reviews/T-203-ux-designer.md and personas/ux-designer.md"
 ],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 4, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor",
   "title": "Show box brings the box above the bar but scrolls the highlighted words mostly off the top and cuts the box label's second line",
   "evidence": "measure.out [1 after Show box]: box y 441-469, bar top 482, scrollY 296. Screenshot 1-edit-375x667-after-showbox.png: only the last 3 lines of the highlighted excerpt are on screen, and the label 'I read this line against the highlighted words myself.' has its second line ('highlighted words myself.') cut by the bar. 2-lib10-e1-375x667-showbox.png: highlighted words 'Pt states chest wall and left knee pain.' are at the top edge; measure.out lib10 e1 mark y -27 to 19 at 375x667 after Show box.",
   "why_it_matters": "The box says 'I compared the line to the highlighted words', and the one tap that finds the box leaves the words she must compare against half off screen. She can scroll back, so this is a rough edge, not a block. It is only at 375x667 and 360x740.",
   "fix": "Scroll to the box's label bottom, not the box top (scrollMarginBottom = bar height + label height), or scroll so the highlighted words and the box share the area above the bar when both fit.",
   "acceptance_test": "At 375x667 on lib10 e1, after Show box the whole label text (both lines) is above the bar top, and at least the first line of the highlighted words is on screen."},
  {"severity": "nit",
   "title": "'PT's' and 'PTs' still map to 'patient'",
   "evidence": "measure.out [3 outsideParts] line='Patient reports pain' quote=\"PT's note: reports pain\" -> underlined=[]. The check in step2.js is `w === \"PT\"` on the whole matched word, and the matched word for \"PT's\" is \"PT's\".",
   "why_it_matters": "'PT's note' (physical therapist's note) is an everyday chart phrase. Small, rare.",
   "fix": "Test the capitals on the word before the possessive or plural is stripped, e.g. /^PTs?(['’]s)?$/.",
   "acceptance_test": "Quote \"PT's note: reports pain\" with line 'Patient reports pain' underlines 'Patient'."},
  {"severity": "nit",
   "title": "Hint text stays 13 px at 375 and Show box is 34 px high",
   "evidence": "measure.out [1 edit-to-check 375x667 +0s] stFont 13px, showBox [257,628,363,662] = 106 x 34 px; Yes/No are 50 px high. r1 asked for 15 px.",
   "why_it_matters": "It is the only cue on that screen. A small touch target beside two 50 px buttons. Target size conformance is for accessibility-reviewer.",
   "fix": "15 px text and a 44 px high button; the bar has 4 px spare, so check the height.",
   "acceptance_test": "Wording and size review only."},
  {"severity": "nit",
   "title": "On a reworded line, 'Read it once more against the highlighted words' shows only after she ticks the box",
   "evidence": "measure.out: [1 edit-to-check +0s] status 'Saved. Tick the box to say you compared them.'; [1 after ticking] status 'Saved: your wording is in. Read it once more against the highlighted words.' The box's own card already says 'You changed the wording. Read it against the highlighted words once more.' (1-edit-375x667-after-showbox.png).",
   "why_it_matters": "The instruction to compare appears in the slot after she has said she did. The yellow card above carries it, so nothing is lost.",
   "fix": "Keep one phrase, e.g. 'Saved. Read it against the highlighted words, then tick the box.' while unticked.",
   "acceptance_test": "Wording review only."}
 ],
 "whats_right": [
  "The reason for a greyed Yes now stays beside a 'Saved' note on the edit path and survives 30 s; Show box finds the box in one tap and focuses it, and Space then A finishes the item by keyboard.",
  "Hint and Show box appear only when a box is the reason and is hidden (none at 390x844 or 1440x900, none on lines with no box), and Yes never moved in any state (y 531-581 at 375, 708-758 at 390, 782-838 at 1440).",
  "'PT' versus 'Pt' now behaves correctly in the live app, and the damages wording reads 'lost wages' with no 'lost pay' or 'not a bill' left on the page."
 ],
 "questions_for_chris": []}
```
