# T-181 review: guided 4-step UI (D-068), ux-designer-reviewer

Verdict: **changes** (0 blockers, 4 majors, 11 minors, 2 nits). Scores: design quality 4, originality 4, craft 3, functionality 4.

**Does it meet Chris's grandma bar? Not yet.** On a desktop, the sample case meets it. A first-time user goes from Your cases to a downloaded letter without instructions. Every screen says where she is, what to do and how much is left. Nothing moved under me across 23 items at 1440 and 390. The letter matches the golden letter text exactly.

It fails the bar in two places:
- **On a phone.** Step 3's done screen scrolls sideways. On a disputed line, the line she must compare is hidden behind the card header. Tapping "Step 2 of 4" a second time to close it sends her to Step 1.
- **When she corrects a line.** The refusal message is ungrammatical and does not name the words she removed.

All 4 T-180 majors are fixed:
- The primary button sits in a sticky bar.
- At 390 the record card is 231 px, up from 122 px, and Undo is whole.
- Demo mode explains that paste and upload are off.
- "Model" and "itemized" are rewritten on decision screens.

Pinned: `git archive 26287b9` in the scratchpad, served on three private ports, all stopped afterwards (each port then answered 000):
- :7893, public demo (`./run.sh` defaults).
- :7894, `ZLAYT_MODE=local`, for test cases, a disputed line and a date pick.
- :7895, live config, used only for Step 1 input errors; Draft was never pressed.

Live :7860 was looked at too. `git diff --stat 26287b9 -- app/frontend/guided app/backend/api.py` printed nothing, so live serves the same guided UI. Deterministic first: `E2E_REQUIRE_DB=1 pytest tests/e2e/guided -q -x` on the archive gave `100 passed in 141.71s`.

## First-time-user walk (reading only the screen)

| Screen | Where am I | What do I do | Done? | Hesitation, jargon, movement |
|---|---|---|---|---|
| Your cases (empty) | yes | yes: "Start a new case" / "Open the sample case" | n/a | Footer: "...checked each answer against its quote" ("quote" is a banned word in spec section 0). |
| We found 9 records | yes, step bar + "Step 1 of 4" | yes, sticky "Draft the timeline" at y 832 (in view) | n/a | Locked steps 2-4 all say "After step 1" (T-180 minor still open). |
| Drafting | yes, 8 named stages, "2 of 8" | yes ("You can leave this page") | yes | Took under 2 s here. |
| Records added | yes | yes, "Go to step 2" in the sticky bar | yes, green check | Two provenance paragraphs back to back. One reads "...summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item" (no period). The second repeats the "Prepared by our team" sentence. "Flags" and "checked by code" are T-180 major-4 words. "19 timeline items" after "9 records" is not explained. |
| Step 2 items (19) | yes: "Item 4 of 19", "3 answered · 16 to go", step bar "16 of 19 left" | yes, one question and two equal answers | yes | 0 px movement between items (`moved: []` on all 19, both widths). "Keys: A says yes..." on every page, against spec section 0. On the accident-date conflict, record 7's highlight is below the source card's fold (351 of 799 px visible), with no scroll cue. |
| Step 2 done | yes, step 2 stays current (T-180 minor fixed) | yes | yes: "9 kept in the letter · 0 left out · 10 warnings for the attorney · 0 not needed" | none |
| Step 3 (4 amounts) | yes, "Bill total so far $8,390.00" | yes | yes | The provenance sentence wraps to 2 lines and touches the cards (y 286 vs 292). The "Keys" line offers "E fixes or adds a note" where there is no third action. |
| Step 3 done | yes | yes | yes, the total line is large | **390: page is 573 px wide; Change buttons off-screen (M1).** |
| Get your letter | yes | yes, Copy/Download in the sticky bar at y 832 | yes, green "Your letter is ready" | At 390 the copy says "The notes on the right" while the notes are below. |

## Things checked beyond the happy path

- **Second case and multi-case.** Local mode had 6 cases; public mode had 2 started in this browser. Each card has a Next line and one Continue button. A search box appears at 6 cases. Two sample cases look identical: same title, same "Started Nov 2 · 9 records".
- **Returning to a half-done case.** I answered 3 items, went to Your cases and pressed Continue. It landed on `?item=e3` with focus on Yes. A reload kept the same URL, and browser Back/Forward worked.
- **409 stale tab.** Two tabs on e3; tab 2 pressed No, then tab 1 pressed Yes. Tab 1 showed "Not saved. This item changed in another tab. We've loaded the latest." Nothing was overwritten, but she is not told the item is now "left out".
- **Disputed compare confirm (lib10 e1).**
  - Yes is disabled, and pressing A moves focus to the box.
  - The 28 px box reads "I read this line against the highlighted words myself."
  - Ticking it enables Yes and the item saves. Correct at 1440.
  - At 390 the line is hidden (M2).
- **Keyboard only, 1440, Tab and Enter only.** No A/D shortcuts were used. Tab presses to each target:
  - "Open the sample case": 5.
  - Draft the timeline: 0.
  - "Go to step 2": 3.
  - Each of the 23 items: 0, because focus lands on Yes.
  - "Go to step 3" and "Go to step 4": 1 each.
  - Download: 1.

  The whole run took 26.6 s (automated), and the downloaded file is clean.
- **Errors (live-config server).**
  - Empty or whitespace input: Read stays disabled.
  - A 501,960-character paste got "That's more than we can read at once (60,000 characters or 40 records). Split it into two cases." The text was kept.
  - Offline got "We couldn't reach the server. Your text is still here." The text was kept.
  - The case name `Jordan <Rivera>` got an inline name error.
- **Edit and undo.**
  - A bad number got a clear refusal: "...not in the highlighted words: 45."
  - Dropping "complained of" got the garbled refusal (M3).
  - A valid edit showed the compare box again ("You changed the wording...").
  - The letter preview shows the edit.
  - Undo returned to the item: "Undone: item 2 is back to not decided."
- **Step 4 with undecided items.** It said "6 items still need a decision". Copy and Download stay disabled until "Copy it anyway, without 6 items." is ticked.

```json
{"card": "T-181", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "commits f3d42a2, 848bbad, 3944cc2, 26287b9 (git archive 26287b9; repo HEAD was 52e115a with 2875 dirty paths, guided frontend identical per git diff --stat 26287b9 -- app/frontend/guided app/backend/api.py = empty); app at http://127.0.0.1:7893 (public demo, run.sh defaults), :7894 (ZLAYT_MODE=local, fixture), :7895 (live config, Step 1 input only); live http://127.0.0.1:7860 viewed; sample case evals/golden/sample.txt plus library lib01/02/03/09/10; spec docs/GUIDED_UI_SPEC.md; T-180 review majors",
 "exercised": [
  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided -q -x on the archive of 26287b9: 100 passed in 141.71s",
  "Mouse walk at 1440x900 and 390x844, fresh browser, public demo: Your cases -> Open the sample case -> Draft the timeline -> Step 2 (19 items, Yes each) -> Step 3 (4 amounts) -> Step 4 -> Download letter and notes + Copy letter (artifacts/review-evidence/T-181-ux-explore.py, T-181-ux-walk.py, T-181-ux-download.py; screenshots artifacts/review-evidence/T-181-ux/d1-*, d2-*)",
  "Item-to-item box positions of Yes, No, Back, third action, Decide later, step bar, question, both cards and status slot recorded on all 23 items at both widths: 0 px moved",
  "diff of downloaded letter vs evals/golden/sample.export.expected.txt: only the golden's block-1 header line and the notes block differ (letter text identical); clipboard copy identical to the download",
  "Keyboard-only run at 1440 with Tab+Enter only, Tab counts logged (T-181-ux-keyboard.py), downloaded kb1440-letter.txt",
  "Multi-case: local mode 2 then 6 cases (search box appears), public mode 2 sample cases; half-done case B (3 answered) -> Your cases -> Continue lands on ?item=e3 with focus on Yes; reload and Back/Forward (T-181-ux-multicase.py, m-* screenshots)",
  "409 stale tab: two tabs on e3, tab 2 No, tab 1 Yes -> plain message, nothing overwritten (m-08-tab1-stale-409.png)",
  "D-066 disputed lib10 e1 at 1440 and 390: Yes disabled, A key focuses the box, tick enables Yes, accept saved (m-05*, p-disputed-390-open.png)",
  "Date pick lib09 e4 at 1440: two dates with month first / day first and Suggested (l1-12-date.png)",
  "Fix the wording: bad number, dropped 'complained of', valid edit, compare box after edit; Undo; No; Decide later x2; Step 2 done with 2 undecided; Step 4 pending with Copy it anyway (T-181-ux-edit-undo.py, e-* screenshots)",
  "Step 1 errors on the live-config server without drafting: whitespace, 501,960-char paste (413), offline, name with angle brackets, at 1440 and 390 (T-181-ux-step1-errors.py, s1-* screenshots)",
  "Horizontal-overflow probe on Step 3 done at 390 (T-181-ux-overflow.py); network 4xx probe on /, /new, timeline (T-181-ux-net404.py); 390 step toggle open/close (T-181-ux-toggle.py, T-181-ux-moves.py); Rename/Delete in place at 1440; 1366x768 review page",
  "Read docs/GUIDED_UI_SPEC.md in full, reviews/T-180-ux-designer.md, card T-181 notes; grepped app/frontend/guided/review.js (R.plain) and app/backend/review.py (_QUALIFIER_WORDS, SUMMARY_DROPS_QUALIFIER)"
 ],
 "verdict": "changes",
 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 4},
 "findings": [
  {"severity": "major",
   "title": "390 px: Step 3 done screen scrolls sideways; the Never counted table pushes its Change buttons off-screen",
   "evidence": "T-181-ux-overflow.py at 390x844 on /case/<sample>/bills done: documentElement clientWidth 390, scrollWidth 573; TABLE.mini left 35 right 573; both btn-change in the Never counted rows at x 459-561. Screenshots artifacts/review-evidence/T-181-ux/d2-s3-done-overflow.png (Amount column only, From and Change cut) and d2-s3-done-overflow-scrolledright.png. Spec section 8: 'no horizontal scroll anywhere'; dossier checklist 17.",
   "why_it_matters": "On a phone she cannot see where a never-counted amount came from or change her answer without discovering a sideways scroll. That breaks 'clear from start to finish' on the last screen before the letter.",
   "fix": "Stack each row on phones (figure, source and reason on separate lines, Change full-width under them), or drop the table for a list of cards below 760 px. Give long 'Not a money amount: ...' text overflow-wrap:anywhere.",
   "acceptance_test": "Playwright 390x844 and 320x640 on the Step 3 done screen of the sample case: scrollWidth <= clientWidth and every btn-change rect is inside the viewport horizontally."},
  {"severity": "major",
   "title": "390 px: on a disputed line the line she must compare is scrolled out of view behind the card header while the 'I read this line ... myself' box is shown",
   "evidence": "T-181-ux-phone-disputed.py on a fresh lib10 case, item e1, 390x844: line-text rect y 410-482, card-line rect y 433-651 with its tag/date header occupying the top ~75 px, compare box y 594-622. Screenshot artifacts/review-evidence/T-181-ux/p-disputed-390-open.png shows 'AI draft', the date, then the amber dispute text and the box; the sentence 'Driver of a pickup struck at an intersection; patient states chest wall and left knee pain.' is not visible. Same on revisit: l2-14-disputed-390.png. At 1440 the line and the box are both visible (m-05-disputed.png).",
   "why_it_matters": "D-066 exists so she compares before saying yes. On a phone she is asked 'Does this line say the same thing as the highlighted words?' and to tick 'I read this line ... myself' while the line is hidden in a nested scroll with no cue. Verifying now takes a hidden extra action, and the tick can be honest-looking but blind.",
   "fix": "Do not auto-scroll the line card to its footer. Keep the line text pinned at the top of the card and let only the footer area scroll, or move the compare box into the action bar's question row on phones. If the card must scroll, show a 'More above' cue.",
   "acceptance_test": "Playwright 390x844 on lib10 e1 (disputed) and on an edit_to_check item: the line-text element's first line is inside the card-line's visible body (not under the header) and the check-compare box is in the viewport at the same time, without any scrolling."},
  {"severity": "major",
   "title": "Fix the wording: the refusal for a dropped 'whose account' phrase is ungrammatical and does not say which words to put back",
   "evidence": "T-181-ux-edit-undo.py, sample e1, edited to 'Restrained driver rear-ended at approx. 35 mph; neck pain 7/10 and headache; transported to Central ER.' (removed 'complained of'). Footer: 'Not saved. The highlighted words carries a phrase that says whose account the highlighted words gives that the line leaves out. Put it back in the line.' (screenshot artifacts/review-evidence/T-181-ux/e-03-fix-saved.png). The server sentence is app/backend/review.py:444 'The quote carries {what} that the summary leaves out.' with _QUALIFIER_WORDS self_report 'a phrase that says whose account the quote gives' (review.py:416). The UI word swap in app/frontend/guided/review.js R.plain turns 'The quote' into 'The highlighted words' without fixing the verb, because 'carries' and 'gives' are not in its verb list. The number refusal is clear by contrast: 'The line has a number, date or dollar figure that is not in the highlighted words: 45.' (e-02-fix-bad-number.png).",
   "why_it_matters": "Correction is the moment of highest effort. The person in Chris's brief cannot work out from this sentence that 'complained of' (the record says 'C/O') is what she removed. Her only way out is Cancel. This is the 'talks to developers, not users' failure the spec's word table was meant to prevent.",
   "fix": "Name the words. Have the server return the qualifier tokens it found in the quote, and say 'Your line leaves out \"complained of\", which tells whose account this is. Put those words back.' Until then, map SUMMARY_DROPS_QUALIFIER per kind to a fixed plain sentence in the UI instead of word-swapping the server sentence. Add the verbs 'carries' and 'gives' to R.plain, or stop pattern-rewriting full server sentences.",
   "acceptance_test": "e2e: edit sample e1 to remove 'complained of'; the footer contains 'complained of' (or the exact dropped words) and has no 'highlighted words carries' or 'highlighted words gives'. A grammar lint over R.plain output for every message in review.py has no plural-subject/singular-verb pair."},
  {"severity": "major",
   "title": "390 px: tapping 'Step 2 of 4' again to close the step list navigates to Step 1",
   "evidence": "T-181-ux-toggle.py at 390x844 on sample timeline ?item=e3: btn-steps at x 16 y 98 w 86 h 28; after opening (aria-expanded true) the step overlay covers the toggle, and tapping the same spot opened /case/<token>/records with h1 'Records added'. Playwright's own click on btn-steps reported '<span class=\"dot\">✓</span> from <div class=\"stick\" data-testid=\"chrome\"> subtree intercepts pointer events'. Escape and tapping the line card close it without navigating (aria-expanded false, URL unchanged). Screenshot artifacts/review-evidence/T-181-ux/mv-390-steps-open.png. Spec section 0: 'Nothing moves when you click' and 'No collapsing, no hidden menus'.",
   "why_it_matters": "The natural way to close a toggle is to tap it again. Doing so mid-review teleports her out of Step 2 to a 'Records added' page. That is exactly the 'do I know where I am' failure Chris's bar names, and it happens on the device most likely to be used by a non-expert.",
   "fix": "Keep the toggle clickable while open (put the overlay below it, or render a 'Close' button in the same place), or drop the toggle and show the 60 px step bar the spec specifies (2.4).",
   "acceptance_test": "Playwright 390x844 on any review page: click btn-steps twice at its own center; aria-expanded is false and the URL and h1 are unchanged."},
  {"severity": "minor",
   "title": "Provenance text still uses banned words and is repeated: 'against its quote', 'flags', 'checked by code'",
   "evidence": "Title row of every Step 2/3 page and the footer: 'Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.' (d1-06-continue-after-draft.png). Step 1 done: 'In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item' (no period), followed by the same 'Prepared by our team' sentence again (d1-04-drafting-2s.png). Spec section 0 bans 'quote' and 'flag'; T-180 major 4 asked to replace 'checked by code'. Card note: this D-065 sentence was mandated by the orchestrator (T-177 r2).",
   "why_it_matters": "It is the one place where 'quote' survives next to 'highlighted words', and the provenance is said 2-3 times per screen (pill, title row, footer). That reads as noise and teaches her to skip it.",
   "fix": "Say it once per screen in plain words: 'Prepared by our team for this demo, then checked by a second AI against the highlighted words. You decide every item.' Drop the duplicate paragraph on Step 1 done.",
   "acceptance_test": "Text lint over every guided page: no 'quote', 'flags', 'checked by code'; at most one provenance sentence plus the header pill per page."},
  {"severity": "minor",
   "title": "Local mode: an 'AI draft' tag sits next to 'not written by an AI model'",
   "evidence": "m-05-disputed.png (lib10 e1): line tag 'AI draft'; title row 'Prepared by our team for this demo, not written by an AI model.'",
   "why_it_matters": "Two provenance claims that contradict each other on one screen undermine calibrated trust. Public demo (sample only) is unaffected.",
   "fix": "Choose the title-row sentence per item set: when any item on the case is not prepared, use the recorded/live wording, or put the sentence on the tag only.",
   "acceptance_test": "Local mode lib10 timeline: the title-row text does not contain 'not written by an AI model' while any tag reads 'AI draft'."},
  {"severity": "minor",
   "title": "409 stale tab says 'We've loaded the latest' but not what the latest is",
   "evidence": "m-08-tab1-stale-409.png: footer 'Not saved. This item changed in another tab. We've loaded the latest.'; progress silently went from 3 to 4 answered; the other tab's 'left out' answer is not shown. The e2e reaches 'Your answer: left out of the letter.' only after Decide later + Back (tests/e2e/guided/test_step2.py:208).",
   "why_it_matters": "She cannot tell whether to press Yes again (overriding the other tab) or leave it.",
   "fix": "Append the current answer: 'This item changed in another tab: it is now left out of the letter. Choose again if that is wrong.'",
   "acceptance_test": "e2e stale test asserts the footer contains 'left out' immediately after the 409, without Back."},
  {"severity": "minor",
   "title": "Public demo promises 'our test cases' that it never offers; every Home and /new load logs a 404",
   "evidence": "d1-21-new.png: 'This demo can only read the sample case and our test cases.' with only the sample tile enabled. T-181-ux-net404.py on :7893: 'HTTP 404 GET /api/cases' on /, 'HTTP 404 GET /api/library' on /new; console 'Failed to load resource ... 404' on each load. The card's orchestrator note asks the guided UI not to repeat T-182 F11 (404s on page load).",
   "why_it_matters": "She looks for test cases that are not there. The 404s are invisible to her but are the pattern the orchestrator flagged (severity of the console part is outside my lens).",
   "fix": "In public demo say 'This demo can only read the sample case.' Decide local vs public from /api/health instead of probing endpoints that 404 by design.",
   "acceptance_test": "Public demo: /new text has no 'test cases'; loading / and /new produces zero 4xx responses."},
  {"severity": "minor",
   "title": "Two cases with the same name look identical, and 'Keep the case link' has no link to keep",
   "evidence": "d3-01-two-samples.png: two cards 'Sample case / Started Nov 2 · 9 records / Next: Draft the timeline.'; header line 'These are the cases started in this browser. Keep the case link to open it elsewhere.' There is no visible link or copy control on the card or in the case header.",
   "why_it_matters": "Multi-case use needs a way to tell cases apart and to reopen one elsewhere; the browser address bar is not 'the case link' to a novice.",
   "fix": "Show the start time ('Started Nov 2, 3:41 pm') and, for unnamed cases, auto-number them ('Sample case 2'). Add a 'Copy case link' button in the case header.",
   "acceptance_test": "Two sample cases started a minute apart show different card text; a 'Copy case link' control exists on every case page."},
  {"severity": "minor",
   "title": "Shortcut hint shown on every review page although spec section 0 says no shortcuts; the Step 3 hint offers a key for an action that does not exist",
   "evidence": "d1-06-continue-after-draft.png and d1-s3-00.png: 'Keys: A says yes, D says no, E fixes or adds a note, the arrow keys move between items.' Step 3 has no third action. Spec section 0: 'Keyboard shortcuts are not offered in the guided UI.' Single-character shortcuts: accessibility severity deferred to accessibility-reviewer (WCAG 2.1.4).",
   "why_it_matters": "This is a deliberate spec deviation, and a stray 'd' answers the item. Undo exists, so it is recoverable. Preference, not a constraint violation: the hint helps keyboard experts.",
   "fix": "Either update the spec and keep the shortcuts with a visible on/off, or remove the hint and keys. Do not mention E on Step 3.",
   "acceptance_test": "Step 3 pages have no 'E fixes' text; the spec and the UI agree on whether shortcuts exist."},
  {"severity": "minor",
   "title": "T-180 minors not folded: every locked step says 'After step 1'; the step label repeats the circle's number",
   "evidence": "d1-02-after-sample.png: '2 Check the timeline / After step 1', '3 Check the bills / After step 1', '4 Get your letter / After step 1'; the circle shows '1' and the label '1 Add records' (accessible name '1 1 Add records Not started (step 1 of 4)'). Orchestrator note on the card: 'Also fold the 7 minors.'",
   "why_it_matters": "It hides the order of the steps the brief asks for and adds reading.",
   "fix": "'After step 1' / 'After step 2' / 'After step 3'; drop the number from either the circle or the label.",
   "acceptance_test": "On /new the three locked status lines differ; the step link text contains each step number once."},
  {"severity": "minor",
   "title": "Step 4 on a phone says the notes are 'on the right'",
   "evidence": "d2-10-letter.png at 390: 'The notes on the right are for the attorney only.' while the notes box is below the letter (h2 'Notes for the attorney' at y 1136).",
   "why_it_matters": "Small, but it is the instruction on the final screen.",
   "fix": "Say 'The notes for the attorney (below the letter on a phone)', or 'The attorney notes are separate.'",
   "acceptance_test": "At 390 the Step 4 intro has no 'on the right'."},
  {"severity": "minor",
   "title": "Paste box at 1440x900 sits mostly under the sticky action bar",
   "evidence": "T-181-ux-step1-errors.py at 1440: input-box rect y 709-989 while the action bar starts at y ~820; s1-paste-big-after-1440.png shows about 110 px of the textarea.",
   "why_it_matters": "She pastes into a box she sees only the top of, and the page scrolls under a fixed bar.",
   "fix": "Shrink the name block or tiles on desktop so the 280 px box fits above the bar, or let the box grow upward.",
   "acceptance_test": "At 1440x900 on /new with Paste chosen, the input box bottom <= action bar top."},
  {"severity": "minor",
   "title": "Evidence from a second record has no 'more below' cue in the source card; the Step 3 title row is cramped",
   "evidence": "Accident-date conflict at 1440: source card clientHeight 351 vs scrollHeight 799, record 7's highlighted 'Date of accident per intake form: 2026-01-19' below the fold, header says only 'Records 1, 2 and 7' (d1-s2-01.png). At 390: 231 vs 1030 px. Step 3 title row: provenance wraps to y ~286 against the card top at y 292 (d1-s3-00.png).",
   "why_it_matters": "The warning card quotes the intake date, so the evidence is visible, but she does not know two more records are stacked below. The crowded title row costs some polish.",
   "fix": "Add a fade plus 'Record 7 below - scroll' line when the source card overflows; give the Step 3 title row 16 px under the provenance line or move that line to the footer.",
   "acceptance_test": "When the source card scrollHeight > clientHeight a visible cue is rendered; Step 3 title row bottom + 12 <= card top at 1440."},
  {"severity": "nit",
   "title": "'This case is no longer here' leads with Try again",
   "evidence": "l2-12-date-390.png (a token that does not exist on that server): h1 'This case is no longer here', 'No such case.', primary 'Try again', secondary 'Back to your cases'.",
   "why_it_matters": "Retrying a missing case cannot help.",
   "fix": "Make 'Back to your cases' the primary button on a 404.",
   "acceptance_test": "Case 404 page: the first button is Back to your cases."},
  {"severity": "nit",
   "title": "Saved line for the $185 rate drops '/visit'",
   "evidence": "Status slot 'Saved: amount 3 $185.00 listed in the notes for the attorney.' (d1-s3-03.png) while the card shows '$185' and the notes say 'Rate $185/visit'.",
   "why_it_matters": "A rate read back as a lump sum invites a wrong mental total.",
   "fix": "Use the figure as written ('$185 per visit') in the saved sentence for rates.",
   "acceptance_test": "Saved text for sample a2 contains 'per visit' or '/visit'."}
 ],
 "whats_right": [
  "One item at a time with the highlight beside the line, one question, two equal answers, focus landing on Yes and 0 px movement across all 23 items at 1440 and 390; the downloaded letter matches the golden letter text exactly.",
  "Multi-case basics work: each case card has a Next line, and Continue resumes at the first undecided item (?item=e3); reload and Back keep her place; search appears at 6 cases.",
  "Friction where it belongs: the disputed box blocks Yes and the A key; 'Copy it anyway, without 6 items' gates an incomplete letter; 413 and offline errors keep the pasted text with a plain message."
 ],
 "questions_for_chris": [
  "The D-065 provenance sentence (orchestrator-mandated) says 'checked each answer against its quote'. May it say 'against the highlighted words' so the screen uses one word for the evidence?",
  "On phones, do you want the full 4-step bar always visible (spec 2.4, 60 px) or the 'Step 2 of 4' toggle the builder chose? The toggle saves space but hides 'where am I' behind a tap."
 ]}
```
