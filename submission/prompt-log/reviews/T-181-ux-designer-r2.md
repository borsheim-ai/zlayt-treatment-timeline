# T-181 review, round 2: guided 4-step UI (fix commit 9ab8cae), ux-designer-reviewer

Verdict: **changes** (0 blockers, 2 majors, 6 minors, 1 nit). Scores: design quality 4, originality 4, craft 3, functionality 4.

**Does it meet Chris's grandma bar?**
- **Desktop (1440x900): yes.** A first-time user gets from Your cases to a downloaded letter without help. Correcting a line now works too: the refusal names the words she removed. On a disputed line she sees the record, the line with the outside words underlined, and the tick box all at once.
- **Phone (390x844): not yet.** The happy path passes: nothing scrolls sideways, nothing moves between items, and the step toggle closes. It fails at the two moments the tool asks her to think:
  - When the tick box shows (a disputed line, or a line she just reworded), the highlighted words she must compare against are scrolled out of the record window.
  - When an edit is refused, the message is hidden behind the action bar. "Save my wording" seems to do nothing.

**The 3-line tradeoff: not acceptable as built.** Three lines would be enough if they were the highlighted words. They are not. On lib10 e1 the record window is 81 px (y 193-274) and the highlight starts at y 270. She sees "Date / Source / Excerpt: Driver of a pickup struck at an" and a 4 px yellow sliver. Meanwhile the line card has about 95 px of empty space under the tick box (box bottom 554, card bottom 651). After a reworded line, the window shows "=== Record 1 === / Date / Source" with the highlight fully below it (mark y 284-381, window bottom 274). The problem is which three lines show, not how many.

## My 4 round-1 majors, same scenarios
| r1 major | r2 result | Evidence |
|---|---|---|
| M1: Step 3 done scrolls sideways at 390 | **Fixed** | At 390, clientWidth 375 = scrollWidth 375. At 320, clientWidth 305 = scrollWidth 305. No element extends past the right edge. The rows are now cards with full-width Change buttons (`T-181-ux-r2/d2-s3-done-overflow.png`, `d2-s3-done-320.png`). |
| M2: disputed line hidden under the card header at 390 | **Half fixed, still major** | Fresh lib10 e1: the line (y 339-411) is below the header (y 284-329) and the box (y 572-600) is in view. The comparison target is now hidden instead (above). The r1 acceptance test also named an edit-to-check item. On sample e1 after a valid edit, the first line of the line text is under the header: line y 319 vs header bottom 329 in one run; in another run (y 249-345) only "ER." shows (`ed390-e04-valid-edit.png`, `ed390-edit-to-check-2x.png`). |
| M3: garbled refusal for a dropped "complained of" | **Fixed in words** | "Not saved. Your line leaves out "complained of", which says whose account this is. Put it back in the line." (`ed1440-e02-drop-qualifier.png`). The bad-number refusal is still clear. At 390 this message cannot be seen (F2). |
| M4: second tap on "Step 2 of 4" goes to Step 1 | **Fixed** | Touch and mouse: open sets aria-expanded true, and a second tap at the toggle's centre sets it false with the URL and h1 unchanged. The element at the toggle centre while open is btn-steps itself. Escape returns focus to the toggle (`tg-touch-open.png`, `tg-touch-after-2nd.png`). |

## Regressions and other r1 items
- **No regressions on the happy path.**
  - Step 2 and Step 3 were walked item by item: 0 px movement on all 23 items at 1440 and at 390.
  - Keyboard only at 1440 (Tab and Enter): the Tab counts are the same as r1 (5, 0, 3, 0 per item, 1, 1, 1). The run took 26.7 s.
  - The downloaded letter is byte-identical to r1's, at 1440 by keyboard and at 390 by mouse.
- **Fixed r1 minors:**
  - The stale-tab 409 now says "It is now left out. Choose again if that is wrong."
  - Public /new no longer mentions test cases.
  - There are no 4xx responses on first paint of /, /new, letter or timeline.
  - Step 3 has no "E fixes" hint.
  - Step 4 no longer says "on the right".
  - The local-mode title row now matches the "AI draft" tag.
  - At 1440, record 7 of the date conflict is in view.
  - The 404 page leads with "Back to your cases".
- **Deterministic check:** `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q` on the 9ab8cae archive printed `1 failed, 133 passed in 178.47s`. The failure is `test_no_console_errors.py::test_every_registered_panel_is_listed` ('narrative' is registered but not in PANELS). That is a classic-screen test, so its cause is outside my lens. The handoff says 134 passed.

```json
{"card": "T-181", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "fix commit 9ab8cae (git archive 9ab8cae into the scratchpad); round-1 baseline 26287b9; app at http://127.0.0.1:7896 (public demo, run.sh defaults: LLM_BACKEND=fixture FIXTURE_SET=curated, own ZLAYT_DB) and http://127.0.0.1:7897 (same plus ZLAYT_MODE=local, only to create lib10 for the M2 scenario); both stopped afterwards (PIDs 14831 and 14830 from lsof; both ports then answered 000); sample case evals/golden/sample.txt plus library case_lib10_eob_ub04_cms1500",
 "exercised": [
  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q on the archive: '1 failed, 133 passed in 178.47s' (test_every_registered_panel_is_listed); a first run with -x stopped at the same test after 125 passed",
  "First-time-user mouse walk at 1440x900, fresh browser: Your cases -> Open the sample case -> Draft the timeline -> Go to step 2 -> 19 items -> 4 amounts -> Step 3 done (T-181-ux-r2-explore.py, T-181-ux-r2-walk.py; screenshots T-181-ux-r2/d1-*)",
  "Same walk at 390x844 in a fresh browser (d2-*); 0 px movement of Yes/No/Back/third/later/question/cards/status on every item at both widths",
  "M1: T-181-ux-r2-overflow.py on Step 3 done at 390x844 and 320x640: scrollWidth equals clientWidth and no element past the right edge",
  "M2 and the tradeoff: T-181-ux-r2-disputed.py (fresh lib10 case, e1 at 390x844, 1440x900, 360x740) and T-181-ux-r2-disputed-scroll.py (390x844, 375x667, 360x740 with touch): rects of the record window, highlight, line text, header, tick box and action bar",
  "M3 and edits: T-181-ux-r2-edit.py at 1440 and 390 (drop 'complained of', 45 mph, valid edit -> tick box, accept, Undo, No, Decide later x2, Step 4 pending, letter has the edit); T-181-ux-r2-edit390.py measures what is visible after a refused save and after a valid edit at 390",
  "M4: T-181-ux-r2-toggle.py at 390 with touchscreen.tap and mouse.click at the toggle centre, then Escape, then a tap on the card",
  "T-181-ux-r2-se.py at 375x667: tick-box reachability, page scroll, tap on disabled Yes",
  "Keyboard only at 1440 (T-181-ux-r2-keyboard.py): Tab counts and a 26.7 s run; kb1440-letter.txt equals r1's T-181-ux/kb1440-letter.txt (diff empty); 390 download (T-181-ux-r2-download.py) equals the keyboard letter (diff empty); clipboard 2,728 chars",
  "409 stale tab at 390 (T-181-ux-r2-stale.py); network 4xx probe on /, /new, letter, timeline and a missing token (T-181-ux-r2-net404.py); /new, Home and the case-404 page at 1440",
  "Read reviews/T-181-ux-designer.md (r1), card T-181 notes and handoff, personas/ux-designer.md"
 ],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 4},
 "findings": [
  {"severity": "major",
   "title": "390 px: when the tick box shows, she cannot see both the highlighted words and the line she must compare (r1 M2 half fixed; the 3-line tradeoff hides the highlight)",
   "evidence": "Disputed lib10 e1 at 390x844 (T-181-ux-r2-disputed.py / -disputed-scroll.py): the record window card-source is y 193-274 (81 px, scrollTop 39 of 431) and the first highlight is y 270-316, so a 4 px yellow sliver shows; line y 339-411; box y 526-554 (572-600 in the first run); line card y 283-651 with about 95 px empty under the box. Screenshots T-181-ux-r2/p-disputed-390-open.png and tr-e1-390x844-open.png; the highlight shows only after scrolling the record card (tr-e1-390x844-highlight.png). At 360x740 the window is 55 px and the highlight y 251-297 is fully out (p-disputed-360-open.png). Edit-to-check (sample e1 after a valid edit, 390): the window shows '=== Record 1 === / Date / Source', the highlight y 284-381 is fully below the window bottom 274, and the line text y 319-391 starts under the header (bottom 329) in one run; in another run (y 249-345) only 'ER.' shows (ed390-edit-to-check-2x.png, ed390-e04-valid-edit.png). At 1440 all three are visible (p-disputed-1440-open.png).",
   "why_it_matters": "D-066 asks her to compare before saying yes. On a phone she ticks 'I read this line against the highlighted words myself' while the highlighted words are out of view, with no cue that the record window scrolls. That is the same blind-tick failure as r1 M2, moved to the other card. Verifying now needs a hidden extra action.",
   "fix": "On phones, while a tick box is showing, size the line card to its content and give the freed space to the record window. Scroll the record window so the first highlight sits at its top, not its bottom edge. Or repeat the highlighted words as a short quote in the tick-box panel ('Highlighted words: \"Pt states chest wall and left knee pain.\"'), so both sides of the comparison sit in one card.",
   "acceptance_test": "Playwright at 390x844 and 375x667, on lib10 e1 and on sample e1 after a valid edit, without scrolling: the first mark in card-source is fully inside the card's visible body; line-text is fully below the card-line header and inside the card; check-compare is in the viewport above the action bar."},
  {"severity": "major",
   "title": "390 px: a refused edit shows its message behind the action bar, so 'Save my wording' seems to do nothing",
   "evidence": "T-181-ux-r2-edit390.py, sample e1, Fix the wording, 'complained of' removed, Save my wording: the refusal rect is y 661-745 while the action bar is y 659-844. The element at the refusal's top is the action-bar question. The line card (y 433-651, scrollTop 71 of 407) does not bring the refusal into view. The status slot is empty and no aria-live region has text. Screenshot T-181-ux-r2/ed390-refused-2x.png shows the record, the editor and 'Change the line, then save it.' with no refusal. At 1440 the same refusal is visible in the card (ed1440-e02-drop-qualifier.png).",
   "why_it_matters": "This is the error state on the correction path, the moment of highest effort. The r1 M3 wording is now good, but on a phone she never sees it. She presses Save, nothing changes, and her likely next step is Cancel or giving up. NN/g says errors go near their source and are visible.",
   "fix": "After a refusal, scroll the line card so the refusal and the editor's first line are both visible, or show the refusal in the status slot under the buttons (also announced through aria-live). Keep the edited text in the box, as now.",
   "acceptance_test": "Playwright at 390x844: after a refused save on sample e1 (drop 'complained of'), the refusal text is fully inside the viewport above the action bar, elementFromPoint at its centre is inside it, and it contains 'complained of'."},
  {"severity": "minor",
   "title": "375x667: on a disputed line the tick box and its reason sit under the action bar; tapping the greyed Yes gives no hint",
   "evidence": "T-181-ux-r2-se.py at 375x667 on lib10 e1: box y 600-628 and the element at its centre is btn-back; status slot empty after tapping the disabled Yes. The page scrolls (scrollY 290 puts the box at y 310, se-375-after-scroll.png), but nothing says so (tr-e1-375x667-open.png). This is below the project's 390 px target, so it is a preference, not a spec violation.",
   "why_it_matters": "On a small iPhone a first-time user sees a greyed Yes and no reason, which is a stuck state.",
   "fix": "Same as the first major (give the tick box room). Also, when the disabled Yes is tapped, say 'Tick the box above first' in the status slot.",
   "acceptance_test": "At 375x667 on lib10 e1 the check-compare box is in view above the action bar; tapping Yes while disabled puts a sentence in the status slot."},
  {"severity": "minor",
   "title": "390 px: on the accident-date conflict, records 2 and 7 are below the 231 px record window with no 'more below' cue",
   "evidence": "T-181-ux-r2/d2-s2-01.png: the window shows record 1 and part of record 2; card-source clientHeight 231 vs scrollHeight 622; the record-7 sentence 'Date of accident per intake form: 2026-01-19' is out of view. Fixed at 1440 (d1-s2-01.png shows all three).",
   "why_it_matters": "The warning card quotes the intake date, so the evidence is on screen, but she does not know a third record is stacked below.",
   "fix": "Add a fade plus 'Record 7 below' cue when the window overflows, or on phones show only each record's highlighted sentence.",
   "acceptance_test": "At 390 on the conflict item, when card-source scrollHeight > clientHeight a visible cue is rendered."},
  {"severity": "minor",
   "title": "Carried from r1 and not folded: provenance said 2-3 times per page with 'quote'; every locked step says 'After step 1'; shortcut hint on every page",
   "evidence": "Step 4 intro text: 'Prepared by our team Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.' (T-181-ux-r2-edit.py output, ed1440-e07-letter-pending.png). Step 1 done repeats it as two paragraphs (d1-03-drafted.png). /new: '2 Check the timeline / After step 1', '3 ... / After step 1', '4 ... / After step 1' (d1-21-new.png). Step 2: 'Keys: A says yes, D says no, E fixes or adds a note, the arrow keys move between items.' (d1-04-step2.png), against spec section 0. The handoff lists these as not done; the 'quote' wording waits on Chris.",
   "why_it_matters": "Repeated provenance teaches her to skip it; 'After step 1' three times hides the order of the steps.",
   "fix": "As in r1: one provenance sentence per page in plain words; 'After step 1/2/3'; settle the shortcuts with the spec.",
   "acceptance_test": "Text lint over guided pages: at most one provenance sentence plus the pill, no 'quote'; the three locked step lines on /new differ."},
  {"severity": "minor",
   "title": "The handoff's '134 passed' does not reproduce on the commit tree: 133 passed, 1 failed",
   "evidence": "E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q on git archive 9ab8cae: 'FAILED tests/e2e/test_no_console_errors.py::test_every_registered_panel_is_listed ... 1 failed, 133 passed in 178.47s'; the assertion: registered panels [... 'narrative'] differ from PANELS [...] (app/frontend/narrative.js is in the tree). The cause is in the classic screen and its tests, outside my lens.",
   "why_it_matters": "The card's AC evidence claims a green run that a fresh reviewer cannot reproduce from the commit.",
   "fix": "Add 'narrative' to PANELS (or stop registering it) and rerun from a git archive of the commit; quote the exact output in the AC.",
   "acceptance_test": "The same command on a git archive of the fix commit prints 0 failed."},
  {"severity": "minor",
   "title": "Not re-tested, per the handoff not done: two same-name cases look identical and 'Keep the case link' has no link; paste box under the sticky bar at 1440",
   "evidence": "Handoff 'minors not done: ... Step 4/new paste box vs sticky bar ... case copy link'; r1 evidence T-181-ux/d3-01-two-samples.png and s1-paste-big-after-1440.png. Home at 9ab8cae still says it has cases 'started in this browser' (d1-22-home-with-case.png).",
   "why_it_matters": "Multi-case use needs a way to tell cases apart and to reopen one elsewhere.",
   "fix": "As in r1: start time or auto-number on cards; a 'Copy case link' button; fit the paste box above the bar.",
   "acceptance_test": "As in r1."},
  {"severity": "nit",
   "title": "Case-404 page: button sits left of the centred heading, step 2 is highlighted for a case that does not exist, and 'No such case.' reads like a server message",
   "evidence": "T-181-ux-r2/d1-23-case-404.png: heading centred at x ~712, button at x 353-581, step 2 shown as current; text 'No such case.'",
   "why_it_matters": "Small polish on a page she reaches from an old link.",
   "fix": "Centre the button, show no current step, and say 'It may have been deleted, or it was started in another browser.'",
   "acceptance_test": "On the case-404 page the button's centre x is within 4 px of the heading's, and no step has aria-current."}
 ],
 "whats_right": [
  "The r1 M1/M3/M4 fixes hold. Step 3 done has no sideways scroll at 390 or 320. The refusal names 'complained of' in plain words. The step toggle closes on a second tap by touch or mouse.",
  "At 1440 a disputed line now shows the record, the line with the outside words underlined, and the tick box at once. That is the best compare screen in the project; keep it.",
  "Nothing moved on any of the 23 items at either width. The keyboard path is unchanged, and the letter is byte-identical to r1's at 1440 and 390."
 ],
 "questions_for_chris": [
  "On phones, is it acceptable for the disputed-line check to show only the highlighted sentence (not the whole record) next to the line, with 'Show the whole record' one tap away? That is the cheapest way to fit both sides of the comparison on one screen."
 ]}
```
