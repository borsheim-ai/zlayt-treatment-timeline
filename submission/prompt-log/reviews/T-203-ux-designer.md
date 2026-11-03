# T-203 review: 375x667 greyed Yes, payment wording, underline fix (commit 38ee0c3), ux-designer-reviewer

Verdict: **changes** (0 blockers, 1 major, 2 minors, 2 nits). Scores: design quality 4, originality 4, craft 3, functionality 3.

**On a disputed line at 375x667, is it clear why Yes is greyed out, and what to do?**
- **Why: yes.** The status slot inside the action bar, with Yes and No, now reads "Tick the box above to say you compared them." It is one line (18 px high at y 636-654, bar top 482, screen bottom 667). It clears when she ticks the box and comes back if she unticks it. Yes does not move in either state (y 531-581), so nothing jumps.
- **What to do: only half.** The box is at y 691-719 on a 667 px screen. It is below the screen, not above. "Above" points the wrong way, and nothing says to scroll (F2).
- **The reworded-line path is not fixed (F1).** After "Fix the wording" at 375x667, Yes is greyed, the slot says only "Saved: your wording is in. Read it once more against the highlighted words.", and the tick box is hidden behind the bar. That text stayed for 30 s. Tapping the greyed Yes does nothing.

**Payment wording and underline fix**
- **Payment wording:** on a payment, the second-check line now reads "A second AI check thought this may be a damages figure (such as lost pay), not what it was first sorted as." The old "an amount that is not a bill" is gone (lib11 a6 at 390, 375 and 1440). It is clearer. One nit about "lost pay" beside "Payment: money received" (F4).
- **Underline fix:** on lib11 e2 and lib10 e1 the underlined words no longer include "Patient". On lib10 e1 the underlined words are only Driver, pickup, struck, intersection, at 390, 375 and 1440. The fix also hides a real case (F3).

**Regressions at 390 and 1440: none found.**
- lib10 e1 at 390x844 has the same numbers as T-181 r3: mark y 223-269, line 412-484, box 599-627, bar top 659, box hit = self. Yes stays at y 708-758 with the hint, after ticking, and after unticking.
- Sample e1 after a valid edit at 390: mark 235-332, line 412-508, box 602-630. These are the same as r3.
- At 1440 the tick hint replaces the "Keys: A says yes..." line while the box is unticked, and the keys line returns once she ticks it. Yes stays at y 782-838. Lines with no box show no hint (lib10 e2 at 375 and 1440).
- Deterministic: `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q` on a fresh archive printed `142 passed in 192.63s`.

## Findings
- **F1 (major):** the reworded line at 375x667 still has a greyed Yes with no reason, and the tick box is hidden behind the bar.
- **F2 (minor):** at 375x667 "above" points the wrong way, and at 360x740 the box is behind the buttons.
- **F3 (minor):** "PT" (physical therapy) is treated as "patient", so an outside word goes unmarked.
- **F4 (nit):** "lost pay" next to a "Payment: money received" card.
- **F5 (nit):** the "Step 3 of 4" label wraps to three lines at 375 (not from this commit).

```json
{"card": "T-203", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 38ee0c3 (git archive 38ee0c3 into a new empty scratchpad dir ux-t203-38ee0c3; HEAD = 38ee0c3 per git rev-parse --short HEAD); demo app http://127.0.0.1:7981 (LLM_BACKEND=fixture FIXTURE_SET=curated, own ZLAYT_DB) and http://127.0.0.1:7982 (same plus ZLAYT_MODE=local, to create library cases lib10 and lib11); both stopped afterwards (PIDs 89165 and 89167 from lsof; both ports then answered 000); sample case evals/golden/sample.txt plus library cases case_lib10_eob_ub04_cms1500 and case_lib11_priors_and_ledger",
 "exercised": [
  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q on the fresh archive: '142 passed in 192.63s' (includes tests/e2e/guided/test_t203.py)",
  "artifacts/review-evidence/T-203-ux-measure.py: lib10 e1 (disputed line, tick box) at 375x667, 390x844, 360x740 and 1440x900: rects of status slot, Yes/No, tick box, mark, line, action bar; tapped the greyed Yes; scrolled the page until the box cleared the bar; ticked and unticked the box (measure.out is the printed output, screenshots in artifacts/review-evidence/T-203-ux/)",
  "same script: sample e1 fresh and after a valid edit ('transported to' -> 'taken to') at 375x667, 390x844 and 1440x900; lib10 e2 (no box) at 375 and 1440",
  "artifacts/review-evidence/T-203-ux-measure2.py: sample e1 at 375x667 after a valid edit, status slot read at +0, +5, +15 and +30 s, tapped the greyed Yes, scrolled 300 px; lib11 e2 and lib10 e1 outside-word underlines and lib11 a6 (Step 3) second-check wording at 390, 375 and 1440; walked every lib11 item at 375x667 listing greyed Yes, box id, box rect and slot text (measure2.out)",
  "read the screenshots a-lib10-e1-375x667-open.png, a-lib10-e1-390x844-open.png, a-lib10-e1-1440x900-open.png, b-sample-e1-375x667-edit-to-check.png, p2-lib11-a6-375x667.png and p2-lib11-a6-390x844.png",
  "node check of the new ABBR mapping copied from app/frontend/guided/step2.js:113-114 with a PT (physical therapy) quote",
  "git show 38ee0c3 (review.js drawStatus and AMOUNT_WAY, step2.js ABBR, tests/e2e/guided/test_t203.py); board.py show T-203 for the handoff; read reviews/T-181-ux-designer-r3.md and personas/ux-designer.md"
 ],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 3},
 "findings": [
  {"severity": "major",
   "title": "375x667: after Fix the wording, Yes is greyed, the slot shows only 'Saved ... Read it once more', and the tick box is hidden behind the action bar; the new hint is not shown (this is the second half of my T-181 r3 F1)",
   "evidence": "T-203-ux-measure2.py [1 edit-to-check 375x667 +0s .. +30s], identical at each time: status 'Saved: your wording is in. Read it once more against the highlighted words.', slot y 627-663, yesDisabled true, box y 630-658 (id check-compare), bar y 482-667, scrollY 107. T-203-ux-measure.py [B sample e1 375x667 after valid edit]: boxHit = 'status-text', so the slot is drawn on top of the box. Tapping the greyed Yes changes nothing. Only after a 300 px page scroll does the box appear (y 330-358, the highlighted words are then off screen). Screenshot artifacts/review-evidence/T-203-ux/b-sample-e1-375x667-edit-to-check.png shows a faded Yes, 'Saved...' and no box. Cause: review.js drawStatus (38ee0c3) shows the tick hint only when no 'Saved' message is up (`!s && ...`); the edit path always has one. At 390x844 the same path is fine, the box is in view at y 602-630 above the bar at 659.",
   "why_it_matters": "This is the same state the card was opened to fix: a first-time user on a small iPhone sees a greyed Yes and no box. The reworded line is the correction path, and the message sends her back to the highlighted words, not to the box. The disputed-line case in the brief is fixed; the reworded line is not. In my r3 F1 and r3 acceptance test, both the disputed and the reworded line were named.",
  "fix": "Keep both sentences while Yes is greyed by an unticked box: append the hint to the Saved text ('Saved: your wording is in. Now tick the box to say you compared them.'), or draw the hint as a second line under the Saved message. Also when she taps the greyed Yes, scroll the box into view or flash the hint.",
   "acceptance_test": "At 375x667, on sample e1 after a valid edit, the status slot text contains 'Tick the box' while Yes is disabled, and tapping the disabled Yes either scrolls the box into view or leaves that sentence in the slot. Extend tests/e2e/guided/test_t203.py to cover the edit path."},
  {"severity": "minor",
   "title": "375x667 and 360x740: 'Tick the box above' points the wrong way, and at 360x740 the box is behind the buttons",
   "evidence": "T-203-ux-measure.py [A lib10-e1 375x667 open]: box y 691-719 on a 667 px screen (boxBelowViewport true), boxHit 'none'; the hint is at y 636-654. Scrolling the page 249 px brings the box to y 442-470, above the bar, but the mark is then at y -26-20 (off the top). lib11 a6 at 375x667 has the box at y 666-694, also below the screen (p2-lib11-a6-375x667.png: no box visible, hint says 'above'). At 360x740 the box is at y 604-632 behind Yes/No (y 604-654), boxHit 'big', and the page cannot scroll (docH 740, scrollY stays 0); only the card scrolls. The words 'above' are correct at 390x844 and 1440x900 (box at y 599-627, above the bar at 659).",
   "why_it_matters": "She now learns why Yes is greyed, but she is told to look above for a box that is below the screen or under the buttons. The card AC literally asks for 'above', so this is a preference about the wording, not a miss against the AC.",
   "fix": "Use direction-free words, e.g. 'Tick the box under the line to say you compared them.', or make the hint a button that scrolls the box into view. Hint is 13 px; at 375 it is the only cue, so use the 15 px used for the slot at rest.",
   "acceptance_test": "At 375x667 on lib10 e1 the hint contains no direction word that contradicts the box position, or tapping it brings the box fully above the bar."},
  {"severity": "minor",
   "title": "The new chart-shorthand mapping treats 'PT' (physical therapy) as 'patient', so 'Patient' goes unmarked when the quote has only 'PT'",
   "evidence": "app/frontend/guided/step2.js:113-114: ABBR = { pt: 'patient', ... } and stem() lowercases. I copied the functions into node: quote 'PT 3x/week, tolerating exercises', line 'Patient attended physical therapy 3 times a week' gives underlined words [attended, physical, therapy, 3, times], with no 'Patient'. The quote 'Pt states chest wall pain' with 'Patient states chest wall pain' gives none, as intended. Not run in the app, because the fixture backend cannot draft a PT line; the code path is the same function.",
   "why_it_matters": "'PT' for physical therapy is common in injury records. A line that says 'Patient' where the record only said 'PT' is exactly the kind of outside word the underline exists to show, and the underline now hides it.",
   "fix": "Map 'pt' to 'patient' only when the quote spells it 'Pt' (not all caps), or only when the same quote also contains words like 'states', 'reports' or 'denies'; otherwise leave it underlined.",
   "acceptance_test": "Unit or e2e: quote 'PT 3x/week' with line 'Patient attended ...' underlines 'Patient'; quote 'Pt states chest pain' with line 'Patient states chest pain' underlines nothing."},
  {"severity": "nit",
   "title": "'(such as lost pay)' sits right under 'Payment: money received, not a charge' on a payment amount",
   "evidence": "p2-lib11-a6-390x844.png: card text 'Payment: money received, not a charge.' followed by 'A second AI check thought this may be a damages figure (such as lost pay), not what it was first sorted as.'",
   "why_it_matters": "'Payment' and 'pay' side by side can read as the same thing. Still far better than 'an amount that is not a bill'.",
   "fix": "Name the way plainly: 'a damages figure (for example lost wages), not a payment to the clinic'.",
   "acceptance_test": "Wording review only."},
  {"severity": "nit",
   "title": "At 375x667 the Step 3 label 'Step 3 of 4' wraps to three lines beside the bill total (not changed by this commit)",
   "evidence": "p2-lib11-a6-375x667.png top strip: 'Step / 3 of / 4'. The diff touches no CSS (git show 38ee0c3 --stat: review.js, step2.js, test_t203.py).",
   "why_it_matters": "Small polish; it eats header height on the screen where height is scarcest.",
   "fix": "Let the bill-total pill shrink or drop 'so far' at 375.",
   "acceptance_test": "At 375x667 on Step 3 the step label is on at most two lines."}
 ],
 "whats_right": [
  "On a disputed line the reason for the greyed Yes now sits in the action bar next to the buttons, in one line at 375, 390 and 1440, and it clears on the tick without moving Yes (y 531-581 at 375, 708-758 at 390).",
  "The new second-check wording on a payment ('a damages figure (such as lost pay)') and the 'Patient' underline fix both show in the app, and nothing moved at 390 or 1440: same rects as T-181 r3 and 142 e2e tests pass.",
  "The hint appears only when a box is the reason: lines without a box show none (lib10 e2 at 375 and 1440), and the generic 'Tick the box above first.' shows for the 'check-separate' box on lib11 bills a2-a4."
 ],
 "questions_for_chris": []}
```
