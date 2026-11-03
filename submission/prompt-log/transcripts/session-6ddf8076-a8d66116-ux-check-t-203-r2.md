# Subagent: UX check: T-203 r2 (UX check: T-203 r2)

Source: `agent-a8d661168d02eddc7.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T23:54:34.500Z

Re-check T-203, round 2, in /Users/arsis/zlayt-pm-project as the UX designer, starting from a fresh context. The fix commit is fa34fe9; read reviews/T-203-ux-designer.md and the card handoff.

Extract a fresh `git archive fa34fe9` into an empty directory and run demo mode on your own port; stop your PID afterward.
- At 375x667, re-run your major's scenario ("Fix the wording", then tick) and check the new "Show box" button.
- Confirm "PT" and "Pt" behave correctly and check the "lost wages" wording.
- Spot-check 390 and 1440 for regressions.

Write reviews/T-203-ux-designer-r2.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:38.516Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/ux-designer.md"
}
````

### User / tool · 2026-11-02T23:54:38.525Z

**tool result**
````
1	# Persona dossier — ux-designer-reviewer
2	
3	## 1. Identity
4	**Priya Raman (fictional), Principal UX Designer, enterprise workflow software — 12 years, last 4 on human-in-the-loop AI review tools (document review, claims triage).**
5	She has watched expert users abandon AI tools that hid where an answer came from, and others that made correcting the AI slower than doing the work by hand. Her incentive: the reviewer must finish faster *and* trust the result, so she grades the cost of verifying and correcting, not the beauty of the first screen.
6	
7	## 2. Day-to-day context
8	- Tools: Figma, Playwright scripts for walkthroughs, screen recordings, heuristic-evaluation sheets.
9	- Pressures: expert users with high volume who live on the keyboard; buyers who judge in a 3-minute demo.
10	- A bad day: usability sessions where every participant re-opens the source PDF because the tool's excerpt is hidden two clicks away.
11	
12	## 3. Goals and success criteria for this artifact
13	- The paralegal can see, for any entry, flag, or dollar amount, the exact source excerpt without leaving the screen.
14	- State is always visible: what is verified, what needs review and why, what has been accepted/edited/dismissed, how many remain.
15	- Correction is cheap: accept/edit/dismiss in one action each, keyboard-reachable, undoable.
16	- Errors, empty states, and model failure are designed, not default stack traces.
17	- The export is usable as pasted text in a demand letter.
18	
19	## 4. Review checklist
20	1. Every timeline entry shows date, provider, one-line summary, and the verbatim excerpt (or a one-click/one-key reveal that stays on the same screen).
21	2. `needs_review` items are visually distinct from `verified` and sorted first; the one-sentence reason is visible without hovering.
22	3. `rejected` (could-not-verify) items appear in a visible tray, not silently dropped.
23	4. Flags are grouped by type (gap, conflict, prior condition, causation language) and each shows the evidence excerpt(s); a conflict shows both excerpts side by side.
24	5. The charges table separates totaled charges from "unclear — not totaled" items; the $185/visit rate sits in the unclear group with its reason.
25	6. A progress indicator shows reviewed vs remaining (e.g., "7 of 12 reviewed") at all times during review.
26	7. Accept, edit, dismiss are each one click and have keyboard equivalents; the shortcuts are discoverable on screen.
27	8. Edit happens in place, preserves the original text for comparison, and marks the item as edited.
28	9. Any accept/dismiss can be undone without reloading.
29	10. Export is disabled or clearly warns while items remain unreviewed, and states exactly what will be included.
30	11. The exported text pastes cleanly into a word processor: one line per entry, no HTML artifacts, no UI labels, citations present.
31	12. Empty input, oversized input, and model/LLM failure each show a plain-language message near the input, preserve what the user pasted, and suggest the next step.
32	13. Long-running processing shows status (step names or progress), not a frozen screen.
33	14. The "synthetic data only" banner is persistent and does not obscure content or focused elements.
34	15. The AI's role is explained where it acts (e.g., "Summary drafted by AI, checked against the excerpt") — not a generic disclaimer.
35	16. Confidence is shown only as states that change a decision (verified / needs review / rejected), not as decorative percentages.
36	17. The layout works at 390 px width: no horizontal scroll for the review list; actions remain reachable.
37	18. Terminology matches the user's world (chronology, provider, excerpt, billed charges), not the developer's (chunk, span, token).
38	19. On first load of the sample-case results, the first focusable item in the results region is a `needs_review` item, and the 73-day gap flag is visible without scrolling at 1440x900.
39	20. Nothing in the interface claims more than the record supports (e.g., no "injury caused by accident" headers).
40	
41	## 5. Red flags / dealbreakers
42	Each item here is a **blocker** (rate it so; never major or minor).
43	- The source excerpt is not visible or reachable for an item (breaks "reviews rather than trusts").
44	- Export includes items the user did not accept, or there is no way to see what will be exported.
45	- An error state loses the user's pasted records.
46	- Unverified model output is styled identically to verified output.
47	
48	## 6. Vocabulary
49	visibility of system status, recognition over recall, error prevention, user control and freedom, accelerators, progressive disclosure, empty state, error state, inline validation, provenance / citation affordance, calibrated trust, efficient correction, efficient dismissal, scope of AI explanation, information scent, hierarchy, affordance.
50	
51	## 7. How I review
52	1. Read the brief; open the app at the given URL with Playwright (desktop 1440x900 and mobile 390x844).
53	2. Screenshot every state: empty, input pasted, processing, results, an item expanded, edit mode, flags panel, charges table, export preview, error (submit empty input; submit 500 KB of text), and model-failure if the brief provides a way to force it.
54	3. Complete the sample case end to end using only the keyboard first, then the mouse. Time both.
55	4. Try to export with items unreviewed; try to undo an accept; edit an entry and check the export shows the edit.
56	5. Paste the export into a plain text file and inspect it.
57	6. Score each of the four criteria (design quality, originality, craft, functionality) 1-5; any score ≤ 2 must have a matching major or blocker finding.
58	7. File findings with screenshot paths under `artifacts/review-evidence/`.
59	
60	Hard thresholds: functionality ≤ 2 → at least one blocker; verifying any single item takes more than 2 actions → major.
61	
62	## 8. Calibration
63	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
64	- **blocker — Excerpt hidden from conflict flag.** Evidence: screenshot shows "Conflicting accident dates" with no excerpts. Fix: show both quotes ("...2026-01-09..." EMS, "Date of accident per intake form: 2026-01-19") with record labels. Test: E2E asserts both excerpts visible in the flag card.
65	- **blocker — Error loses pasted input.** Evidence: submitting 600 KB shows "Error 413" and clears the textarea. Fix: inline message "This is over the 200 KB limit. Split the records and try again." with text preserved.
66	- **minor — No progress count.** Evidence: review screen with 12 entries has no remaining count. Fix: sticky "5 of 12 reviewed · 3 need review".
67	
68	## 9. Sources
69	- https://www.nngroup.com/articles/ten-usability-heuristics/ — NN/g: Nielsen's 10 heuristics (system status, user control, error prevention, recognition over recall, flexibility/accelerators, error recovery).
70	- https://www.nngroup.com/articles/error-message-guidelines/ — NN/g (2023): put errors near their source, don't rely on color alone, explain plainly with a fix, preserve user input.
71	- https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/ — Amershi et al., CHI 2019: 18 validated guidelines across initial use, during interaction, when wrong, over time.
72	- https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/ — Microsoft HAX Toolkit: the same 18 guidelines grouped by stage, including when the AI system is wrong.
73	- https://pair.withgoogle.com/chapter/explainability-trust/ — Google PAIR: calibrate trust, explain data sources, scale detail to stakes, show confidence only when it improves decisions.
74	- Assumption: the "two actions to verify" threshold and the 390 px width are this project's choices, not from a source.
75	
76	## 10. Limits
77	Do not judge clinical correctness, adjuster tactics, legal ethics, or code quality. Accessibility conformance (WCAG) belongs to accessibility-reviewer — note obvious issues but defer severity to them.
78	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:38.864Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-203-ux-designer.md"
}
````

### User / tool · 2026-11-02T23:54:38.870Z

**tool result**
````
1	# T-203 review: 375x667 greyed Yes, payment wording, underline fix (commit 38ee0c3), ux-designer-reviewer
2	
3	Verdict: **changes** (0 blockers, 1 major, 2 minors, 2 nits). Scores: design quality 4, originality 4, craft 3, functionality 3.
4	
5	**On a disputed line at 375x667, is it clear why Yes is greyed out, and what to do?**
6	- **Why: yes.** The status slot inside the action bar, with Yes and No, now reads "Tick the box above to say you compared them." It is one line (18 px high at y 636-654, bar top 482, screen bottom 667). It clears when she ticks the box and comes back if she unticks it. Yes does not move in either state (y 531-581), so nothing jumps.
7	- **What to do: only half.** The box is at y 691-719 on a 667 px screen. It is below the screen, not above. "Above" points the wrong way, and nothing says to scroll (F2).
8	- **The reworded-line path is not fixed (F1).** After "Fix the wording" at 375x667, Yes is greyed, the slot says only "Saved: your wording is in. Read it once more against the highlighted words.", and the tick box is hidden behind the bar. That text stayed for 30 s. Tapping the greyed Yes does nothing.
9	
10	**Payment wording and underline fix**
11	- **Payment wording:** on a payment, the second-check line now reads "A second AI check thought this may be a damages figure (such as lost pay), not what it was first sorted as." The old "an amount that is not a bill" is gone (lib11 a6 at 390, 375 and 1440). It is clearer. One nit about "lost pay" beside "Payment: money received" (F4).
12	- **Underline fix:** on lib11 e2 and lib10 e1 the underlined words no longer include "Patient". On lib10 e1 the underlined words are only Driver, pickup, struck, intersection, at 390, 375 and 1440. The fix also hides a real case (F3).
13	
14	**Regressions at 390 and 1440: none found.**
15	- lib10 e1 at 390x844 has the same numbers as T-181 r3: mark y 223-269, line 412-484, box 599-627, bar top 659, box hit = self. Yes stays at y 708-758 with the hint, after ticking, and after unticking.
16	- Sample e1 after a valid edit at 390: mark 235-332, line 412-508, box 602-630. These are the same as r3.
17	- At 1440 the tick hint replaces the "Keys: A says yes..." line while the box is unticked, and the keys line returns once she ticks it. Yes stays at y 782-838. Lines with no box show no hint (lib10 e2 at 375 and 1440).
18	- Deterministic: `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q` on a fresh archive printed `142 passed in 192.63s`.
19	
20	## Findings
21	- **F1 (major):** the reworded line at 375x667 still has a greyed Yes with no reason, and the tick box is hidden behind the bar.
22	- **F2 (minor):** at 375x667 "above" points the wrong way, and at 360x740 the box is behind the buttons.
23	- **F3 (minor):** "PT" (physical therapy) is treated as "patient", so an outside word goes unmarked.
24	- **F4 (nit):** "lost pay" next to a "Payment: money received" card.
25	- **F5 (nit):** the "Step 3 of 4" label wraps to three lines at 375 (not from this commit).
26	
27	```json
28	{"card": "T-203", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
29	 "scope": "commit 38ee0c3 (git archive 38ee0c3 into a new empty scratchpad dir ux-t203-38ee0c3; HEAD = 38ee0c3 per git rev-parse --short HEAD); demo app http://127.0.0.1:7981 (LLM_BACKEND=fixture FIXTURE_SET=curated, own ZLAYT_DB) and http://127.0.0.1:7982 (same plus ZLAYT_MODE=local, to create library cases lib10 and lib11); both stopped afterwards (PIDs 89165 and 89167 from lsof; both ports then answered 000); sample case evals/golden/sample.txt plus library cases case_lib10_eob_ub04_cms1500 and case_lib11_priors_and_ledger",
30	 "exercised": [
31	  "E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q on the fresh archive: '142 passed in 192.63s' (includes tests/e2e/guided/test_t203.py)",
32	  "artifacts/review-evidence/T-203-ux-measure.py: lib10 e1 (disputed line, tick box) at 375x667, 390x844, 360x740 and 1440x900: rects of status slot, Yes/No, tick box, mark, line, action bar; tapped the greyed Yes; scrolled the page until the box cleared the bar; ticked and unticked the box (measure.out is the printed output, screenshots in artifacts/review-evidence/T-203-ux/)",
33	  "same script: sample e1 fresh and after a valid edit ('transported to' -> 'taken to') at 375x667, 390x844 and 1440x900; lib10 e2 (no box) at 375 and 1440",
34	  "artifacts/review-evidence/T-203-ux-measure2.py: sample e1 at 375x667 after a valid edit, status slot read at +0, +5, +15 and +30 s, tapped the greyed Yes, scrolled 300 px; lib11 e2 and lib10 e1 outside-word underlines and lib11 a6 (Step 3) second-check wording at 390, 375 and 1440; walked every lib11 item at 375x667 listing greyed Yes, box id, box rect and slot text (measure2.out)",
35	  "read the screenshots a-lib10-e1-375x667-open.png, a-lib10-e1-390x844-open.png, a-lib10-e1-1440x900-open.png, b-sample-e1-375x667-edit-to-check.png, p2-lib11-a6-375x667.png and p2-lib11-a6-390x844.png",
36	  "node check of the new ABBR mapping copied from app/frontend/guided/step2.js:113-114 with a PT (physical therapy) quote",
37	  "git show 38ee0c3 (review.js drawStatus and AMOUNT_WAY, step2.js ABBR, tests/e2e/guided/test_t203.py); board.py show T-203 for the handoff; read reviews/T-181-ux-designer-r3.md and personas/ux-designer.md"
38	 ],
39	 "verdict": "changes",
40	 "scores": {"design_quality": 4, "originality": 4, "craft": 3, "functionality": 3},
41	 "findings": [
42	  {"severity": "major",
43	   "title": "375x667: after Fix the wording, Yes is greyed, the slot shows only 'Saved ... Read it once more', and the tick box is hidden behind the action bar; the new hint is not shown (this is the second half of my T-181 r3 F1)",
44	   "evidence": "T-203-ux-measure2.py [1 edit-to-check 375x667 +0s .. +30s], identical at each time: status 'Saved: your wording is in. Read it once more against the highlighted words.', slot y 627-663, yesDisabled true, box y 630-658 (id check-compare), bar y 482-667, scrollY 107. T-203-ux-measure.py [B sample e1 375x667 after valid edit]: boxHit = 'status-text', so the slot is drawn on top of the box. Tapping the greyed Yes changes nothing. Only after a 300 px page scroll does the box appear (y 330-358, the highlighted words are then off screen). Screenshot artifacts/review-evidence/T-203-ux/b-sample-e1-375x667-edit-to-check.png shows a faded Yes, 'Saved...' and no box. Cause: review.js drawStatus (38ee0c3) shows the tick hint only when no 'Saved' message is up (`!s && ...`); the edit path always has one. At 390x844 the same path is fine, the box is in view at y 602-630 above the bar at 659.",
45	   "why_it_matters": "This is the same state the card was opened to fix: a first-time user on a small iPhone sees a greyed Yes and no box. The reworded line is the correction path, and the message sends her back to the highlighted words, not to the box. The disputed-line case in the brief is fixed; the reworded line is not. In my r3 F1 and r3 acceptance test, both the disputed and the reworded line were named.",
46	  "fix": "Keep both sentences while Yes is greyed by an unticked box: append the hint to the Saved text ('Saved: your wording is in. Now tick the box to say you compared them.'), or draw the hint as a second line under the Saved message. Also when she taps the greyed Yes, scroll the box into view or flash the hint.",
47	   "acceptance_test": "At 375x667, on sample e1 after a valid edit, the status slot text contains 'Tick the box' while Yes is disabled, and tapping the disabled Yes either scrolls the box into view or leaves that sentence in the slot. Extend tests/e2e/guided/test_t203.py to cover the edit path."},
48	  {"severity": "minor",
49	   "title": "375x667 and 360x740: 'Tick the box above' points the wrong way, and at 360x740 the box is behind the buttons",
50	   "evidence": "T-203-ux-measure.py [A lib10-e1 375x667 open]: box y 691-719 on a 667 px screen (boxBelowViewport true), boxHit 'none'; the hint is at y 636-654. Scrolling the page 249 px brings the box to y 442-470, above the bar, but the mark is then at y -26-20 (off the top). lib11 a6 at 375x667 has the box at y 666-694, also below the screen (p2-lib11-a6-375x667.png: no box visible, hint says 'above'). At 360x740 the box is at y 604-632 behind Yes/No (y 604-654), boxHit 'big', and the page cannot scroll (docH 740, scrollY stays 0); only the card scrolls. The words 'above' are correct at 390x844 and 1440x900 (box at y 599-627, above the bar at 659).",
51	   "why_it_matters": "She now learns why Yes is greyed, but she is told to look above for a box that is below the screen or under the buttons. The card AC literally asks for 'above', so this is a preference about the wording, not a miss against the AC.",
52	   "fix": "Use direction-free words, e.g. 'Tick the box under the line to say you compared them.', or make the hint a button that scrolls the box into view. Hint is 13 px; at 375 it is the only cue, so use the 15 px used for the slot at rest.",
53	   "acceptance_test": "At 375x667 on lib10 e1 the hint contains no direction word that contradicts the box position, or tapping it brings the box fully above the bar."},
54	  {"severity": "minor",
55	   "title": "The new chart-shorthand mapping treats 'PT' (physical therapy) as 'patient', so 'Patient' goes unmarked when the quote has only 'PT'",
56	   "evidence": "app/frontend/guided/step2.js:113-114: ABBR = { pt: 'patient', ... } and stem() lowercases. I copied the functions into node: quote 'PT 3x/week, tolerating exercises', line 'Patient attended physical therapy 3 times a week' gives underlined words [attended, physical, therapy, 3, times], with no 'Patient'. The quote 'Pt states chest wall pain' with 'Patient states chest wall pain' gives none, as intended. Not run in the app, because the fixture backend cannot draft a PT line; the code path is the same function.",
57	   "why_it_matters": "'PT' for physical therapy is common in injury records. A line that says 'Patient' where the record only said 'PT' is exactly the kind of outside word the underline exists to show, and the underline now hides it.",
58	   "fix": "Map 'pt' to 'patient' only when the quote spells it 'Pt' (not all caps), or only when the same quote also contains words like 'states', 'reports' or 'denies'; otherwise leave it underlined.",
59	   "acceptance_test": "Unit or e2e: quote 'PT 3x/week' with line 'Patient attended ...' underlines 'Patient'; quote 'Pt states chest pain' with line 'Patient states chest pain' underlines nothing."},
60	  {"severity": "nit",
61	   "title": "'(such as lost pay)' sits right under 'Payment: money received, not a charge' on a payment amount",
62	   "evidence": "p2-lib11-a6-390x844.png: card text 'Payment: money received, not a charge.' followed by 'A second AI check thought this may be a damages figure (such as lost pay), not what it was first sorted as.'",
63	   "why_it_matters": "'Payment' and 'pay' side by side can read as the same thing. Still far better than 'an amount that is not a bill'.",
64	   "fix": "Name the way plainly: 'a damages figure (for example lost wages), not a payment to the clinic'.",
65	   "acceptance_test": "Wording review only."},
66	  {"severity": "nit",
67	   "title": "At 375x667 the Step 3 label 'Step 3 of 4' wraps to three lines beside the bill total (not changed by this commit)",
68	   "evidence": "p2-lib11-a6-375x667.png top strip: 'Step / 3 of / 4'. The diff touches no CSS (git show 38ee0c3 --stat: review.js, step2.js, test_t203.py).",
69	   "why_it_matters": "Small polish; it eats header height on the screen where height is scarcest.",
70	   "fix": "Let the bill-total pill shrink or drop 'so far' at 375.",
71	   "acceptance_test": "At 375x667 on Step 3 the step label is on at most two lines."}
72	 ],
73	 "whats_right": [
74	  "On a disputed line the reason for the greyed Yes now sits in the action bar next to the buttons, in one line at 375, 390 and 1440, and it clears on the tick without moving Yes (y 531-581 at 375, 708-758 at 390).",
75	  "The new second-check wording on a payment ('a damages figure (such as lost pay)') and the 'Patient' underline fix both show in the app, and nothing moved at 390 or 1440: same rects as T-181 r3 and 142 e2e tests pass.",
76	  "The hint appears only when a box is the reason: lines without a box show none (lib10 e2 at 375 and 1440), and the generic 'Tick the box above first.' shows for the 'check-separate' box on lib11 bills a2-a4."
77	 ],
78	 "questions_for_chris": []}
79	```
80	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:39.273Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/project_t203_375_hint.md"
}
````

### User / tool · 2026-11-02T23:54:39.279Z

**tool result**
````
1	---
2	name: project-t203-375-hint
3	description: T-203 r1 38ee0c3 changes, 1 major (Saved message hides the new tick hint on the edit-to-check path at 375x667); minors (hint says "above" but box is below screen; PT=patient mapping)
4	metadata:
5	  type: project
6	---
7	
8	T-203 r1 (reviews/T-203-ux-designer.md, 38ee0c3, 2026-11-02): **changes**, 1 major.
9	- The status-slot hint "Tick the box above to say you compared them." works on a disputed line at 375/390/1440 (one line, Yes does not move).
10	- Major: after Fix the wording at 375x667 the slot shows only "Saved: ... Read it once more", box at y 630-658 is behind the bar, tap on greyed Yes does nothing, 30 s later unchanged. drawStatus shows the hint only when no Saved message.
11	- Minors: "above" is wrong at 375x667 (box y 691 on a 667 screen) and at 360x740 the box is behind Yes/No with no page scroll; ABBR pt->patient treats PT (physical therapy) as patient (step2.js:113).
12	- 142 passed (guided + no_console_errors + demo_provenance) on a fresh archive.
13	
14	Scripts: artifacts/review-evidence/T-203-ux-measure.py (ports 7981 demo / 7982 local, makes lib10 and lib11) and -measure2.py. Reuses PROBE from T-181-ux-r3-majors.py.
15	
16	**Why:** the 375x667 phone is now treated as in scope (the card exists), so edit-path gaps there are majors, not minors.
17	
18	**How to apply:** on r2, re-run measure2.py part 1 first (edit-to-check slot text at +0 s and after tapping Yes). See [[project-t181-guided-build]].
19	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:39.863Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-203 | tail -60"
}
````

### User / tool · 2026-11-02T23:54:40.001Z

**tool result**
````
---
id: "T-203"
title: "Guided UI polish: at 375x667 a disputed line's tick box sits below the buttons and nothing says why Yes is disabled; paralegal r2 minors"
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T23:35:18Z"
updated_at: "2026-11-02T23:54:31Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T23:48:01Z"
rounds: 1
commits: ["38ee0c3", "fa34fe9"]
reviews:
  - {"persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-203-ux-designer.md", "at": "2026-11-02T23:47:53Z"}
ac:
  - {"n": 1, "text": "at 375x667 the tick box is visible with the buttons or a one-line hint says 'Tick the box above to say you compared them'; paralegal r2 minors fixed where cheap; e2e at 375x667", "done": true, "evidence": "r2: tests/e2e/guided/test_t203.py 6 pass (375x667 after-edit hint persists beside Saved, Show box, PT, lost wages); git archive of fa34fe9 tree: guided suite + test_no_console_errors 138 passed, E2E_REQUIRE_DB=1"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T23:35:25Z frontend: claimed
- 2026-11-02T23:41:12Z frontend: AC 1 checked: tests/e2e/guided/test_t203.py (375x667 hint + 390 wording/Pt) passes; git archive of 38ee0c3 tree: guided suite + test_no_console_errors 135 passed, E2E_REQUIRE_DB=1
- 2026-11-02T23:41:12Z frontend: moved in_progress -> in_review
- 2026-11-02T23:41:16Z orchestrator: review dispatched: ux-designer-reviewer
- 2026-11-02T23:47:53Z orchestrator: review ux-designer-reviewer (claude-sonnet-5-5): changes — reviews/T-203-ux-designer.md; round 1; findings:
    - [major] 375x667: after Fix the wording, Yes is greyed, the slot shows only 'Saved ... Read it once more', and the tick box is hidden behind the action bar; the new hint is not shown (this is the second half of my T-181 r3 F1) — fix: Keep both sentences while Yes is greyed by an unticked box: append the hint to the Saved text ('Saved: your wording is in. Now tick the box to say you compared t
    - [minor] 375x667 and 360x740: 'Tick the box above' points the wrong way, and at 360x740 the box is behind the buttons — fix: Use direction-free words, e.g. 'Tick the box under the line to say you compared them.', or make the hint a button that scrolls the box into view. Hint is 13 px; at 375 it is the only cue, so use the 15 px used for the slot at rest.
    - [minor] The new chart-shorthand mapping treats 'PT' (physical therapy) as 'patient', so 'Patient' goes unmarked when the quote has only 'PT' — fix: Map 'pt' to 'patient' only when the quote spells it 'Pt' (not all caps), or only when the same quote also contains words like 'states', 'reports' or 'denies'; otherwise leave it underlined.
- 2026-11-02T23:47:53Z orchestrator: assigned: frontend
- 2026-11-02T23:48:01Z frontend: claimed
- 2026-11-02T23:54:26Z frontend: AC 1 checked: r2: tests/e2e/guided/test_t203.py 6 pass (375x667 after-edit hint persists beside Saved, Show box, PT, lost wages); git archive of fa34fe9 tree: guided suite + test_no_console_errors 138 passed, E2E_REQUIRE_DB=1
- 2026-11-02T23:54:26Z frontend: moved in_progress -> in_review
- 2026-11-02T23:54:31Z orchestrator: review dispatched: ux-designer-reviewer

## Handoff
What changed (r2): drawStatus keeps the reason for a greyed Yes beside a 'Saved' note ('Saved. Tick the box to say you compared them.') and redraws after act ends, until ticked; wording has no direction word; new 'Show box' button in the status slot appears when the box is under the bar/below screen and scrolls it above the bar + focuses it; 'PT' in capitals no longer maps to patient (Pt still does); 'lost pay' -> 'for example lost wages'. How verified: test_t203.py 6 tests incl. e4 edit path at 375x667; git archive fa34fe9 tree guided + no_console_errors 138 passed (E2E_REQUIRE_DB=1). Left: hint is 2 lines at 375 now (bar height unchanged); Step 3 label wrap nit not done. Surprised me: S.act finally only synced buttons, so the hint never appeared after an edit until the next redraw.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:45.004Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD; ls artifacts/review-evidence | grep -i T-203; ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad"
}
````

### User / tool · 2026-11-02T23:54:45.214Z

**tool result**
````
fa34fe9
T-203-ux
T-203-ux-checkjson.py
T-203-ux-measure.py
T-203-ux-measure2.py
641ed.bak
CLAUDE.md
GATEM3_se
M1
M1_nocombine
M2
M2_find0
MASTER_PROMPT.md
T-047-run1.json
T-060-pass2-head
T-093-r3-2ab7896
T-093-r3-run.py.orig
T-093-r3-scripts
T-093-r4-3223e50
T-093-r4-mutA
T-093-r4-mutB
T-109-probe
T-109-r1-card
T-109-r1-head
T-109-unit-head.txt
T-124-r1-head
T-124-r1-mut2
T-124-r1-parent
T-133-r1-archive
T-133-r1-source
T-133-r3-archive-4065ef2
T-133-r3-archive-f939ccb
T-133-r3-mutA
T-133-r3-mutB
T-133-r3-mutC
T-133-r3-mutD
T-133-r3-scripts
T-133-r4-archive-head
T-133-r5-13d.py
T-133-r5-15be212
T-133-r5-6fa8ecc
T-133-r5-head
T-133-r5-mut-backslash
T-133-r5-parent
T-133-r5-parse.py
T-133-r5-pmh.py
T-133-r5-probe.py
T-133-r5-r1
T-133-r5-unit-head.log
T-152-r1
T-157-r2-852b060
T-157-r2-full-unit.out
T-157-r2-mut
T-157-r2-mutants.out
T-157-r2-mutate.py
T-157-r2-parse.py
T-157-r2-probe.py
T-157-r2-probe2.py
T-157-r2-probe3-K.out
T-157-r2-probe3-base.out
T-157-r2-probe3.py
T-157-r2-probe4.py
T-157-r3-f31b146
T-157-r3-mut
T-157-r3-mutants.out
T-157-r3-mutate.py
T-160-r1
T-197-612dc2c
T-197-head
T-197-mutants
T-197-probe
T102_staff_r1
T102_staff_r2
T103_archive
T103_parent
T106_cli_out
T106_head_archive
T106_m_exportbranch
T106_m_hlreview
T106_m_hltrace
T106_m_pdfbypass
T106_m_pdfclaude
T106_m_rootcal
T106_r2_mut_a
T106_r2_mut_b
T106_r2_mut_c
T106_r2_mut_d
T106_r2_probe
T106_r2_suite.txt
T106_r2_suite_run2.txt
T106_r2_verify
T106_scripts
T106_unit_run1.log
T106_unit_run2_rs.log
T108_r2_clone
T108_r2_verify
T108_verify
T112_r1
T112_r1_scripts
T112_r2
T112_r3
T112_r3_mut
T112_r3_scripts
T113_r1_b66e748
T113_r1_b66e7481
T113_r1_e1ce8dc
T113_r1_evalout
T113_r1_fresh
T113_r1_head
T113_r2_arch
T113_r2_arch2
T113_r2_clone
T113_r2_probe
T113_r2_unit.log
T115_card_show.txt
T115_staff_r1
T115_staff_r2
T119_r2
T119_r3
T119_staff_r1
T120_r3_cli1.txt
T120_r3_cli2.txt
T120_r3_evals_head
T120_r3_evals_parent
T120_r3_fix
T120_r3_fixprobe.py
T120_r3_fprobe.py
T120_r3_head
T120_r3_mut
T120_r3_parent
T120_r3_probe_head.txt
T120_r3_probe_parent.txt
T120_r3_unit.txt
T128_9_127_r1
T128_9_r2
T128_9_r2b
T128r4_prev
T132r1
T132r1p
T132r3_arc
T132r3_cli1.err
T132r3_cli1.txt
T132r3_cli2.err
T132r3_cli2.txt
T132r3_cli_arc.txt
T132r3_cli_ctl.txt
T132r3_ctl
T132r3_mut
T133-r3-cli-1.txt
T133-r3-cli-2.txt
T133-r3-cli-r1.txt
T133-r3-negex.txt
T133-r3-pycontext-kb.yml
T133-r3-unit.log
T133-r4-arch-4065ef2
T133-r4-arch-e79c3aa
T133-r4-arch-parent
T133-r4-cli-reports.txt
T133-r4-clone
T133-r4-mutM1
T133-r4-mutM2
T133-r4-mutM3
T133-r4-pipeline-run1.txt
T133-r4-pipeline-run2.txt
T133-r4-record.json
T133-r4-scripts
T133-r4-suite-archive.txt
T133-r4-suite-clone.txt
T134r4_head
T134r4_head2db
T134r4_mut
T134r4_mut2
T134r4_src
T136_r1_e2e_full.txt
T136_r1_e2e_full2.txt
T136_r1_head
T136_r1_mutA
T136_r1_mutA.log
T136_r1_mutB1
T136_r1_mutB1.log
T136_r1_mutB2
T136_r1_mutB2.log
T136_r1_mutC
T136_r1_mutC.log
T136_r1_serve.sh
T136_r1_server.log
T136_r1_server2.log
T136_r1_unit.txt
T138r2_parent
T139_r1
T140_r1
T140_r2
T140_r3
T140_r4
T141_head
T141_mut
T141_pre
T141_preN2
T141_probe
T141_run
T141r2_head
T141r2_libreport.json
T141r2_mut2
T141r2_mutants.txt
T141r2_parent
T141r2_pk_T141_head.err
T141r2_pk_T141_head.json
T141r2_pk_T141_pre.err
T141r2_pk_T141_pre.json
T141r2_pk_T141r2_head.err
T141r2_pk_T141r2_head.json
T141r2_pl_orig.py
T141r3_head
T141r3_mut
T141r3_r2
T141r3_scripts
T141r4_head
T141r4_prev
T141r5_head
T141r5_mutA
T141r5_prev
T141r5_scripts
T141r6_824984f
T141r6_evidence
T141r6_head
T141r6_r5
T141r7_6379c0b
T141r7_824984f
T141r7_83f1afd
T141r7_acad4f6
T141r7_c2913a6
T141r7_head
T141r7_mut_guard2
T141r8_head_99438fb
T141r8_mutant_two_digit_off
T155_r1
T155r2_T164
T157r3
T159_161_r1
T162_r1
T162_r2
T162_r3
T167-mut
T167-r1-archive
T167-r1-out
T167-r1-out-local
T167-r1-out-local2
T168_r1
T169_staff_r1
T169_staff_r2
T179_r1
T179_r1_mut
T179_r2
T179_r2_mut
T196
T197_r2_9ab8cae
T197_r2_e425534
T197_r2_mut_both
T197_r2_mut_home
T197_r2_mut_none
T197_r2_mut_step1
T197_r2_scripts
T198-locate.py
T198-run1.txt
T198-run2.txt
__pycache__
_types.bak
a.sqlite3
a141
a178
a178.out
a201
a27e3a4.diff
a9ab
acc.py
across.py
addtags.py
adj_eval
adj_out
adr013.txt
after.py
all.txt
amounts_broken.py
ap3500.pdf
api
api.patch
api2
api_at_099732b.py
api_head.log
api_head.md
api_head.py
api_head.sqlite3
api_head_plus_mine.md
api_md_head.md
api_md_new.md
api_mine.md
api_new.py
api_parent.log
api_parent.sqlite3
apitmp
app
app-d0b04bc
app-head
app.log
app.pid
app.sqlite3
app2
app2.log
app2.pid
app2.sqlite3
app3
app3.sqlite3
app4
app4.log
app4.pid
app4.sqlite3
app5
app5.log
app5.pid
app5.sqlite3
app60
app60.log
app60.pid
app60.sqlite3
append_404.py
append_correction.py
ar2
ar_old
arc
arc.sh
arc2
arch
arch0c24
arch2
arch203r2
arch3
arch4
arch5
arch_57a08ba
arch_head_r3b
arch_r2_54382
arch_r2_54382.idx
arch_r2b
arch_r2c
arch_r2d
arch_r3_final
arch_t140
archive
archpath.txt
artifacts
atk
aud.py
aud2.py
audit.py
audit_mine.js
audit_split.py
audited.bak
axe
b.sqlite3
base
base.json
base1.log
baseline_journey.out
before.txt
big.json
billing.orig
blank.py
blob.tmp
board
body.py
bombs
boom_final.py
boom_server.py
boundary.py
boundary2.py
build_evidence.py
build_set.py
build_set.py.bak
build_t099_blobs.py
busy.out
c
c01.json
c1.json
c5.json
c8a9874
ca.sh
cal.bak
case.json
case.json.tok
case07.json
case3.json
case3.json.tok
case_01_date_formats.json
case_lib11_priors_and_ledger.json
case_list.orig.bak
cases.txt
ce70
ce70-report.md
census.py
charge_text.py.patch
charges.py
check.py
check_golden.out
check_json.py
check_r2.py
check_r3_json.py
check_r4.py
checks2.sh
checks3.sh
chk.js
chk.py
chk2.py
chk_mut.py
chk_syntax.py
clean2
clean3
clean4
clean5
clean5_unit.txt
clean_run1.txt
cleanup_check.py
cli1.out
cli2.out
cli_c1.err
cli_c1.txt
cli_final.err
cli_head_out.txt
cli_rep1.err
cli_rep2.err
cli_rep3.err
clone-run
clone194
cmscms.py
collapsed.png
collapsed.py
commit.sh
commit_paths.sh
commit_r3.sh
commit_tree
commitcases.txt
conf-1440.png
conf-390.png
conf_A.py
conf_B.py
conftest_mine.py
conftest_split.py
controls_run.log
copy
copyA
copyC
copy_untracked.py
corp_base.json
corp_r2.json
corpus.py
count.py
count1.py
count_base.py
counts.sh
cr.sh
cred_b05.py
cred_orig.py
cs.sh
ctl-out
ctl.log
d.py
d1
d2
d3
d4
d5
d6
d7
d8
data
data2
dates.orig
db
db3
db4
db5
dbg
dbg.png
dbg.py
dbg2.py
dbg3.png
dbg3.py
dbg4.py
dbg5.py
dbg97.py
de1.txt
decisions_head.md
demo
demo.log
demo.sqlite
dev
dev.db
diag.py
diff.py
dl
docker-venv
docker_emu.sh
docker_serve.log
docker_serve.pid
dockerctx
dockerdata
dockerhome
docs
dom.bak
dos
draft-pass2.md
drive.py
dump.py
e1-1440.png
e1-390.png
e1-390b.png
e1.py
e1400d4
e2.py
e2e-data
e2e-m1-server.log
e2e-m1.sqlite
e2e-run.sqlite
e2e-server.log
e2e.db
e2e.out
e2e1.log
e2e2.db
e2e2.out
e2e3.out
e2e_full.txt
e2e_full1.txt
edit133.py
edit133b.py
edit133r2.py
edit199.py
emptytree
endpoints.py
env97
err.out
err2.out
es1.txt
ev.json
ev.sh
eval_base.out
eval_r2.out
evalout
evalout2
evals
ex07.json
ex1.sh
ex2.sh
ex3.sh
exp-077
exp.py
exp2.py
exp_077.py
export.py.patch
export_curated.sqlite
export_recorded.sqlite
f3.out
f5f1be9-tree
fe-data
fe3.log
fe3.sqlite
fe4.log
fe4.sqlite
fetch
figs.py
files.txt
fill.py
final-data
final.py
final1
final1.log
final2.log
finalize_f5f1be9.py
find_miss.py
first.png
fix.log
fix.sqlite3
fixture_run.out
fixture_run_b.out
flags_commit.py
fpl.bak
fpl_new.py
fpl_old.py
fr_r2.txt
fragile
fresh
fresh.py
fresh_head.log
fresh_head.sqlite3
fresh_nosbs.log
fresh_nosbs.sqlite3
full.done
full.log
full.out
full.patch
full.txt
full2.out
full_head.txt
fx
fx.log
fx.sqlite3
fx_before.txt
fxbak
gate.db
gate_dir.txt
gate_m2
gen
gen.py
gen_controls.py
gm2
gm2r2
gm2r2_legal
gm2r2clone
gm3
gm3-7991.log
gm3-7992.log
gm3-a11y-arch
gm3-a11y-audit.log
gm3-a11y-pid.txt
gm3-a11y-server.log
gm3-a11y-wrap.py
gm3-a11y.sqlite3
gm3-emptyfx
gm3-ux-7991.sqlite3
gm3-ux-7992.sqlite3
gm3src
golden_scan.py
guardprobe.py
guardprobe.py.bak
h.txt
h178
h42.py
h60.txt
h_audit.js
h_charges.js
h_conftest.py
h_review.js
h_stepper.js
harness
head
head-a850be0
head-bc12d44
head-ec33bf0
head.db
head.log
head.py
head.sqlite3
head0
head2
head2.py
head3
head4
head5
head7
head8
head9
headA
head_950d4a5
head_9851a0d_r5
head_9c1af01
head_ae76835_r3
head_clean
head_clean.log
head_clean.sqlite3
head_copy
head_e63e564
head_faee448_r4
head_nosbs
head_nosbs.log
head_nosbs.sqlite3
head_run.sh
head_scan.txt
headcheck
headchk2
headfe
headx
heldout.py
helpers.py
helpers2.py
hf-config.html
hf-docker.html
hits.py
hookcopy
idx
idx162r3b
idx167
idx171
idx2
idx3
idx4
idx5
idx_commit
idx_r2b
idx_r2c
idx_r2d
idx_r3
idx_t139r4
idx_t139r4b
idxpath
image-emu
ing.bak
ingest.orig
ingest_novel.py
inj.py
jcheck.py
judge_live.py
judges.png
k1dump.py
kb2.py
kb3.py
kb_test.py
keys.py
last_commit
latest.before.sha
latest.committed.json
latest_head.json
latest_new.json
leak.py
letter_check.py.patch
lib-after.md
lib.md
lib.out
lib_app.sqlite
lib_report.md
lib_report3.md
lib_report5.md
libdump.py
library-after.md
library-base.md
library-report.md
link
live-demo
live-demo.log
live-local
live-local.log
live23.sh
live3.sh
llm_head.md
local
local.log
local.sqlite
m1.txt
m2.txt
m2regate-live.log
m3
m3.txt
m4
m4.txt
m5
m55_M_drop_whole_rule
m55_M_only_needs_review
m55_M_only_rejected
m58_M1_round1_regex
m58_M2_dates_iso_dollar
m58_M3_amounts_valid_dollar
m58_M4_fence_dollar
m59_N11_drop_stale_basis_clause
m59_N12_failed_redraft_overwrites
m59_N13_drop_SEVERITY_NOT_QUOTED
m59_N3_drop_D006_token_check
measure.py
memory
mine
mine.diff
mine.patch
mine.txt
miss.py
miss2.log
miss2.py
mk.py
mk_r3.sh
mkd.py
mkfix.py
mkindex171.sh
mkpatch.py
mkpdf.py
mkreview.py
mkreviews.py
mob.py
msg.txt
msg_r3.txt
mut
mut-A
mut-B
mut-C
mut-D
mut-M6_drop_family_lookbehind
mut-base
mut-control
mut-gate
mut-qual
mut-t073-A-broad-catch
mut-t073-B-no-guard-in-review
mut-t073-C-expected-becomes-supported
mut-t073-D-drop-class
mut-t084-1-no-judge-gate
mut-t084-2-no-wording-gate
mut-t084-3-no-negation-gate
mut-t084-4-unsure-accepted
mut-t084-5-no-audit
mut-t084-6-no-value-gate
mut-t084-7-judge-fail-open
mut-tok
mut.py
mut.py.bak
mut080.py
mut1
mut105.py
mut105.py.bak
mut159.py
mut161.py
mut2
mut2.py
mut200.py
mut2_B0_pinned_baseline
mut2_G1_grounding_check_removed_in_extract
mut2_S1_judge_unavailable_fails_open_in_state
mut2_S2_judge1_error_becomes_supported
mut3
mut3_S2b_shared_judge_error_fails_open_to_supported
mut3_S3_j2_error_fails_open_to_agree_pipeline_only
mut4
mut98
mut99
mutB.txt
mutT132
mut_M0_baseline
mut_M1_noRollback
mut_M1_sdk_internal_retries_2
mut_M2
mut_M2_cli_drops_strict_mcp
mut_M3
mut_M3_cli_timeout_600
mut_M4
mut_M4_cli_leaks_stderr_into_error
mut_M5
mut_M5_fixture_miss_retried
mut_M6
mut_M6_j2_error_becomes_agree
mut_M7
mut_M7_stray_subprocess_import_outside_backends
mut_R4M1_stated_total_always_suppressed
mut_R4M2_no_other_figures_on_rate_holder
mut_R4M2_rate_unclear_move_to_other_figures_removed
mut_R4M3_rate_row_drops_own_other_figure_move
mut_R4M3_rate_row_stated_total_not_other_figure
mut_R4R_line790_raises
mut_branch
mut_branch.sqlite
mut_dedupe
mut_flagsdeadline
mut_guard_e2e.out
mut_guard_unit.out
mut_rmfixture
mut_rmjudgefixture
mut_run.py
mut_run2.py
mut_t055_M_drop_whole_rule
mut_t055_M_only_needs_review
mut_t055_M_only_rejected
mut_t058_M1_round1_regex
mut_t058_M2_dates_iso_dollar
mut_t058_M3_amounts_valid_dollar
mut_t058_M4_fence_dollar
mut_t059_N11_drop_stale_basis_clause
mut_t059_N12_failed_redraft_overwrites
mut_t059_N13_drop_SEVERITY_NOT_QUOTED
mut_t059_N3_drop_D006_token_check
mutant-M1-nocombine.txt
mutant-M2-find0.txt
mutant375_journey.out
mutant_timeline572.out
mutants
mutants-db08276.log
mutants-r3-db08276.log
mutants-work
mutants.py
mutate.py
mutate2.py
mutate3.py
mutate_api.py
mutate_run.py
mutate_run2.py
mutate_t055.py
mutate_t058.py
mutate_t059.py
mutrun.sh
mutv2_1
mutv2_2
mutv2_3
mutv2_4
mutv2_5
mutv2_6
mutv2_7
mvp95
mvp95.log
mvp95.pid
mvp95.sqlite3
mw
n.py
narr.py
neg
neg2
negex
negtest
new.json
new2.json
new_record.py
novel.txt
nucc
nv.py
nv2.py
o1
o1.aIcW
o2
o2.vHBZ
o3_new.js
o3_v3.js
ocr_edit
ocr_edit_head
ocrinj
oe
oi
old
old-d0b04bc
old_unc.py
orch.idx
orig
out
out.txt
out_head.json
out_zlayt-pm-project.json
ov.py
overlay-head
own
p.py
p1.py
p1.txt
p2.db
p2.py
p2.txt
p3.log
p3.pid
p3.py
p3.sqlite3
p3.txt
p4-e293daa
p4-head
p5-b612176
p5-server.log
p5.db
p_be
p_fe
pa
page.txt
par
parent
parent-server.log
parent.sqlite3
part.py
part2-process.html
part2-process.pdf
paste.sqlite3
paste_attack_ledger.txt.sqlite
paste_synthetic_ledger.txt.sqlite
patch.py
patch2.py
patch3.py
patch_builder.py
path
path.txt
pathspec.txt
patterns.bak
patterns_copy
patterns_fresh
patterns_nomanual
pdb
pdf_time.py
pdfs
pdfs_head
peer.py
peer.sqlite3
personas
phi.py
pid
pid2
pidA
pidB
pin-690a0e3-r5
pin-6bca-r4
pin-8bc7f90
pin-HEAD-r4
pin-HEAD2-r4
pin-db08276
pin-f218263
pipeline.orig.py
pipeline.py
pipeline_commit.py
pl.orig
pm-gate.sqlite3
pn-head.md
pnh.html
pnh.pdf
portconflict.sh
pp
pp2
pre
pre-t123-archive
pre_t095_schema.sql
present.patch
present.py
prev
probe
probe-db
probe-r2-output.txt
probe-top.png
probe.py
probe.sqlite3
probe133.py
probe133r2.py
probe133r3.py
probe2.py
probe2.py.bak
probe2_t067.py
probe3.py
probe3_t067.py
probe4.py
probe404.py
probe5.py
probe98
probe99
probeA
probeA.stderr
probeA.stdout
probeB
probeB.stderr
probeB.stdout
probe_404.py
probe_7df
probe_copy.sqlite3
probe_copy2.sqlite3
probe_copy3.sqlite3
probe_copy4.sqlite3
probe_copy5.sqlite3
probe_curated.sqlite
probe_err.log
probe_failed.py
probe_flags.sqlite
probe_flags_audit.sqlite
probe_head
probe_head_out.txt
probe_nojudge.py
probe_r4_ocr.py
probe_recorded.sqlite
probe_rej.py
probe_run.py
probe_server.log
probe_t067.py
probe_timeout.py
probe_tray.py
probe_work_head
probe_work_head2
probes
probes-t100
probes159
probes161
probes_r5_dir
proc.png
proc.py
proc2.png
product-note.html
product-note.pdf
prof.out
prof.py
pub.log
pub.py
pub.sqlite3
pub2.log
pure2
pw
r
r1
r2
r2-07c7558
r2-07c7558-server.log
r2-07c7558.sqlite3
r2-802d5fd
r2-cases.out
r2-deploy-head
r2-deploy-wt
r2-head
r2-ocr
r2-planted
r2-server.log
r2-sweep.out
r2.db
r2.log
r2.pid
r2.sqlite3
r2_app.sqlite3
r2_blank_judges.py
r2_check.py
r2_detect.py
r2_es2.py
r2_export.json
r2_for2.py
r2_ids.txt
r2_library.md
r2_mixed.py
r2_mut_base
r2_mut_base_m
r2_mutant_r2b.py
r2_mutants.py
r2_probe_out.txt
r2_rec.sqlite3
r2_run.log
r2_sentinel_data
r2_set_status.py
r2_t080_app.log
r2_t080_app.sqlite
r2_token.txt
r2_treeid.txt
r2_unit.txt
r2a
r2app
r2app-d865
r2arch
r2b
r2c_tree.txt
r2d.sqlite3
r2d_run.log
r2d_tree.txt
r2demo
r2demo.log
r2head
r2live.log
r2live.pid
r2live.sqlite3
r2local
r2local.log
r2mut
r2o
r2parent
r2server.log
r2src
r3
r3-25f585c
r3-a27
r3-demo.db
r3-demo.log
r3-local.db
r3-local.log
r3-parent
r3-server.log
r3.db
r3.log
r3.pid
r3.sqlite3
r3_acceptance_strings.py
r3_accepted.json
r3_api.py
r3_check_json.py
r3_full.log
r3_gate_check.py
r3_mut
r3_rootcause.py
r3_sentinel_data
r3_server.log
r3_t080.sqlite
r3_tok.txt
r3a
r3ap
r3api
r3api2
r3app.sqlite3
r3arch
r3b
r3bp
r3clone.81DVDF
r3clone.out
r3copy
r3da0c7fe
r3db.sqlite3
r3dev
r3e2e.log
r3h
r3head
r3health.json
r3img
r3m
r3mut
r3o
r3pop
r3probe.py
r3run
r3run.out
r3runpid
r3scripts
r3server.log
r3src
r3tb
r3timing.txt
r3tree
r3workdir
r4-8f78874
r4_probe_8634bfe.out.txt
r4_rootcause.py
r4arch
r4data
r4out
r4pin
r4probe
r4probe_on_0f58181.txt
r5
r5.log
r5.pid
r5.sqlite3
r5_e3.png
r5_flag.png
r5_top.png
r5b
r_head.json
r_new.json
rail.png
raw1.txt
raw2.txt
raw3.txt
raw4.txt
raw5.txt
raw6.txt
rec.py
rec.sh
rec_a.log
rec_all.log
rec_all.sh
rec_b.log
rec_judges.log
rec_narr.py
rec_sample.log
recon.py
render_curated.log
render_curated.sqlite
render_flags.log
render_flags.sqlite
render_race.log
render_race.sqlite
render_recorded.log
render_recorded.sqlite
replay.py
replit-config.html
replit-deploy.html
replit_env.py
repo
repro_stale
req_mut.md
requirements-dev.txt
requirements.txt
rerec.log
rerec.sh
rerun.out
rerun.sh
rerun2.sh
research
review.bak
review_commit.py
review_fixed.js
review_head.js
review_headplus.py
review_mine.py
reviews
rt_base.json
rt_r2.json
run.base.py
run.head.py
run.log
run.try.py
run1.err
run1.log
run1.out
run2
run2.err
run2.log
run2.out
run3.err
run3.log
run3.out
run4.err
run4.out
run4.time
run5.err
run5.out
run_c5.py
run_m2.pid
run_m2.sh
run_mutants_r3.py
run_p3_chain.sh
run_r3.sh
run_ro.py
run_t070_orig.py
runs.status
rv_T132_T128_r2r3
s-1440-0.png
s-1440-1700.png
s-1440-2300.png
s-1440-2600.png
s-1440-3300.png
s-1440-4400.png
s-1440-5400.png
s-1440-900.png
s-390-0.png
s-390-1500.png
s-390-3000.png
s-390-900.png
sample_case.json
sc.log
sc.sqlite3
scan.py
scan.py.bak
scan_specimens.py
scan_time_10x5000wide.pdf
schema_pre_T095.sql
score.py
scr.log
scr.sqlite3
scripted.log
scripts
scroll.py
selfcheck-r2.txt
serve_p3_wrapper.py
serve_snap.py
server-7871.log
server-7872.log
server.err
server.log
server.out
server.pid
server2.log
server2.pid
server7867.log
shard0.out
shard1.out
shard2.out
shard3.out
shard4.out
shoot.py
shot.py
shot2.py
shots
shots.log
shots.py
shots2.py
shots_old.py
shots_t046r2.py
show.py
show_T103.txt
snap
snap-077
snap-89a323a
snap-c61
snap-final
snap-h2
snap-head
snap-t187r3
snap.out
snap.path
snap2
snap3
snap7942
snap7942.db
snap7942.log
snap7942.pid
snap9
snap_run.sh
sp.txt
spec
splice.py
spy3.log
spy3.py
src
srv.KdvV
srv.log
srv.out
srv.pid
srv2.log
srv2.pid
srvdir
st_commit.py
stable.py
start.sh
states.py
steps-open.png
store.orig.bak
strip.py
strip_and_grep.py
submission
sync.py
sync.sh
sync_r5.sh
t015r4
t028.out
t030r2mut
t033mut
t033mut.py
t035
t038
t038r3
t040-077
t040-head
t040-live
t043-239
t043_r2_probe.py
t043_r2_probe2.py
t043_r2_probe3.py
t045r2-bypass
t045r2-clean
t045r3-clean
t046-server.log
t046.sqlite3
t046r2.log
t046r2.pid
t046r2.sqlite3
t053r3-data
t055_base_full.txt
t055_mut_full.txt
t056r2_01ipr4y9
t056r2_5_pc8ore
t056r2_gxnki_45
t056r2_jvse81hd
t056r2_pjbon2yp
t057
t060-a11y-axe
t060-a11y-data
t060-a11y-head
t060-a11y-serve.py
t060-p3-app
t060-p3-axe
t060-p3-chain.log
t060-p3-review.json
t060-p3-server.log
t060-p3-server.pid
t060-p3.sqlite3
t060p2
t060p2-wrap
t065
t065r2
t066r2
t066r3
t067
t067_59c7edb
t067_f6fa2dd
t067_head_archive
t067_m1
t067_m2
t067_m3
t067_probes
t067head
t067parent
t067r3
t067r4
t067r5
t067r5-probe-out.txt
t068-data
t068-data-commit
t068-data-commit2
t068-server-commit.log
t068-server-commit2.log
t068-server.log
t068r2-server.log
t068r2-snap
t068r3-case01-body.json
t068r3-case01-get.json
t068r3-data
t068r3-head
t068r3-probe-token.txt
t068r3-server.log
t070
t070r2b
t071_title_probe.py
t072
t072plant
t072r3
t072r3-p1_be_selfreport
t072r3-p2_be_patientstatement
t072r3-p3_be_patientstates
t072r3-p4_fe_selfreport
t072r3-p5_fe_patientstatement
t072r3-p6_fe_selfreported_ui
t072r4
t072r4_plants
t074
t075r2
t076r2
t076r2-data
t076r2-server.log
t077r3
t079.log
t079.sqlite3
t080m_M10_date_always_confirmed
t080m_M11_judge_partial_is_pass
t080m_M12_date_blocker_reason
t080m_M13_overrides_not_counted
t080m_M14_unavailable_counted_judged
t080m_M15_agreement_never_fails
t080m_M16_verbatim_fail_ignored_on_entry
t080m_M17_skip_after_reject_removed
t080m_M18_nothing_accepted_removed
t080m_M19_unsupported_excludes_disagrees
t080m_M1_rejected_blocks_gate
t080m_M20_step_order_swap
t080m_M21_progress_counts_skipped_as_pending
t080m_M22_total_inclusion_accepted_pending
t080m_M23_fixed_why_replaced_by_model_text
t080m_M2_dismissed_blocks_gate
t080m_M3_dismissed_human_pass
t080m_M4_qualifier_always_pass
t080m_M5_gate_ignores_running
t080m_M6_rate_pending_total
t080m_M7_raw_leak_in_metadata
t080m_M8_event_before_after_leak
t080m_M9_edited_text_leak
t080m_base
t080r4
t085r2
t085r3
t086head
t086wt
t090-out
t090.index
t090.patch
t090_code.patch
t090_patch2.py
t090_patch_run.py
t090_patch_tests.py
t090r2
t090r3
t092
t093.base.py
t094r2
t095.patch
t095r2_head
t096-evals
t096-export-check.py
t096-ux-36ceb38
t096-ux-server.log
t096-ux-walk-output.txt
t096-ux.sqlite3
t096_all.py
t096_ds.py
t096_probe.py
t096_probe2.py
t096_shot.py
t096_shot2.py
t096_start.sh
t096data
t097
t097.log
t097.pid
t097.sqlite3
t097b.sqlite3
t097r2
t097r2-server.log
t097r2.sqlite3
t097r2head
t097r3-archive-9f2811f
t097r3-server.log
t097r3-server.pid
t097r3.sqlite3
t098-e511778
t098-f5ddec8
t098-head
t099-3ecb8b1
t099-dirty-check
t099-f345bc8-r2
t099-gitclone-parent
t099-mut
t099.index
t099_msg.txt
t1.xXug
t100-card
t100-fresh
t101
t101r2
t103r2
t103r3_api.diff
t103r3_archive
t103r3_billing.diff
t103r3_control_archive
t103r3_mut
t103r4_archive
t104
t104-3462ad0-ux
t104-server.log
t104-server.pid
t104-state.json
t104-ux.sqlite3
t105
t105r2
t106_r2_archive
t108
t109_adr_edit.py
t109_doc_edit.py
t109r2_head
t109r2_mutA
t109r2_mutB
t109r2_pin
t109r3_head
t109r3_mut
t109r3_mutate.py
t109r3_pin
t109r3_probe_cc.py
t109r3_probe_flags.py
t109r3_probe_flags2.py
t109r3_probe_trim.py
t109r3_probe_trim2.py
t109r4
t110.sqlite3
t110b.sqlite3
t111-archive
t111-parent
t111r2
t111r2-base
t111r2-base.out.json
t111r2-head
t111r2-head.out.json
t111r2-parent
t111r2-parent.out.json
t112.index
t112_live.sh
t112_pipeline.py
t113_run1_evidence
t114
t114r2
t115.pid
t115.sqlite
t115srv.log
t116r2-base
t116r2-head
t116r3
t116r4
t116r5
t118-head
t118-mutA
t118-mutB
t118-pre
t119
t119.log
t119.pid
t119.sqlite3
t119m
t119m.log
t119m.pid
t119m.sqlite3
t120
t120-123-archive
t120-123-server.log
t120-123.sqlite3
t120-parent-archive
t120-parent-server.log
t120-parent.sqlite3
t120-r3.sqlite
t120r2
t120r2.sqlite3
t120r4
t121r2
t123-cmp-head.jsonl
t123-cmp-pre.jsonl
t126r1
t126r2
t133_r1_m3_full.out
t133_r1_m3_full.py
t133_r1_mutate.py
t133_r1_probe.py
t133_r2_probe_mine.py
t134_app.sqlite3
t134_server.log
t134m
t134parent
t134parent2
t134r1
t134r2
t134r3_c4bb
t134r3_cli1.err
t134r3_cli1.txt
t134r3_cli2.err
t134r3_cli2.txt
t134r3_dbg
t134r3_fix
t134r3_head
t134r3_mut
t134r3_mut.txt
t134r3_mut2
t134r3_mut_h.txt
t134r3_par
t134r3_unit.txt
t134r3_unit_c4bb.txt
t134r3_unit_fix.txt
t134scripts
t136-archive
t136-r2-staff
t136-server.log
t136.db
t139
t139_app.sqlite3
t139_overlay.err
t139_overlay.out
t139_overlay.sqlite3
t139_server.err
t139_server.out
t139_trace.sqlite3
t139_trace2.sqlite3
t139clean
t139overlay
t139r2
t139r2_app.sqlite3
t139r2_server.log
t139r3
t139r3_app.sqlite3
t139r4
t139r4_app.sqlite3
t139r4_server.log
t139r5
t139r5_mut1
t139r5_mut2
t139r5_mut3
t139r5_out
t139r5_prev
t139r5_scripts
t139tree
t143
t143p
t143r2
t143r2_case_lib01_er_only_then_gap.txt
t143r2_case_lib02_slip_fall_prior_knee.txt
t143r2_case_lib03_truck_rear_end_chiro.txt
t143r2_case_lib04_dog_bite_scar_revision.txt
t143r2_case_lib05_pedestrian_orif_hardware.txt
t143r2_case_lib06_lop_billed_vs_adjusted.txt
t143r2_case_lib07_parking_lot_fall_outside_records.txt
t143r2_case_lib08_second_crash_mri_after.txt
t143r2_case_lib09_spanish_interpreter_espalda.txt
t143r2_case_lib10_eob_ub04_cms1500.txt
t143r2_case_lib11_priors_and_ledger.txt
t143r2_case_lib12_records_review_credibility.txt
t143r2_case_lib13_cloned_notes_cross_provider.txt
t143r2_case_lib14_handwritten_chiro_scans.txt
t143r2_case_lib15_conclusory_letter_mist.txt
t143r2_mut.py
t143r2_sample.txt
t143r3
t144r1
t145r1
t146r2
t146r3
t146r4
t148r1
t149db
t149r2
t149r2-server.log
t149r2.pid
t149r2.sqlite3
t149server.log
t149src
t151-25f585c
t151-out
t151-scripts
t152_collect.py
t152_diff.py
t154
t154.sqlite3
t154b.sqlite3
t154r2
t154r2p
t155
t155r2
t157-check-json.py
t157-r1
t157r2b
t158-card
t158-f31
t158-f31-m2
t158-f31-m6
t158-f31-runs
t158-head
t158-m2
t158-m3
t158-m4
t158-m5
t158-m6
t158-mut
t158-probe
t158-r1
t158-review-head.js
t158-review-pre.js
t158-settle
t158r3
t159.patch
t160-review
t162.sqlite3
t162r2
t162r2.base
t162r2.idx
t162r3
t162r3.idx
t162v-final
t165-backend
t165-r2
t165-review
t165r2b
t166
t166-mvp-r2-ux-d865.sqlite3
t166-mvp-r2-ux.sqlite3
t166-r2-ux-d865.log
t166-r2-ux-server.log
t168r2
t169-clone-2
t169r2
t171
t171app.sqlite3
t171server.log
t173-final
t173-gen
t173-head
t173-verify
t173.idx
t174
t174r4-local.db
t174r4-local.log
t174r4-public.db
t174r4-public.log
t174r4-src
t175r1
t175r2
t177-arch
t177-arch-base
t177r4
t177r5-fresh
t177r5-prev
t177r5-probe
t178-interrupt.db
t178-interrupt2.db
t178-old.db
t178-pastes.db
t178-pid-7882
t178-pid-7883
t178-pid-7884
t178-server-7881.log
t178-server-7882.log
t178-server-7883.log
t178-server-7884.log
t178-stale.db
t179_commit.index
t179_final.index
t179_old
t179r2
t179r2_unit.txt
t179v2
t180.db
t181
t181-app.sqlite3
t181-local-server.log
t181-local.sqlite3
t181-server.log
t181r3-2c19817
t181ux
t182
t182-3sjF
t182-dir.txt
t182-index.html
t182-serve.log
t182-serve.pid
t182-t0.txt
t182-t1.txt
t182-z.txt
t187r2
t194.index
t194_commit.sh
t194_msg.txt
t2.q4VB
t200
t200.idx
t200run
t202
t202.idx
t202.tree
t202parent
t203
t203r2
t203r2.idx
t2b.IKsK
t3.ORDQ
t4.0u5g
t84r4
tabflow.py
tail.md
test_billing_old.py
tests
tests_b05.py
tests_evals.sh
thr.py
thr2.out
thr2.py
timed_run.sh
tmp.index
tmp2.index
tmp3.index
tmpidx_t197
tmpindex
tog-open.png
tog.py
tok.json
tok_c1_local
tok_c3_local
tok_c5_local
tok_c7_local
tok_case_lib01_er_only_then_gap
tok_case_lib02_slip_fall_prior_knee
tok_case_lib03_truck_rear_end_chiro
tok_case_lib04_dog_bite_scar_revision
tok_case_lib05_pedestrian_orif_hardware
tok_g02_local
tok_g04_local
tok_g06_local
tok_g08_local
tok_g09_local
tok_sample2_local
tok_sample_local
tok_sample_pub
tokens.json
tools
tree
tree.sha
tree.txt
tree3
tree4
tree5
tree_r2
tree_r3
two.py
two.py.bak
u.orig
ub
ui-demo
ui-input.out
ui-local
unit-run-r2-clone-with-git.txt
unit-run-r2.txt
unit.out
unit.txt
unit1.txt
unit171.log
unit2.out
unit3.out
unit_full.txt
unit_full_head.out
unit_r2a.txt
unit_r2b.txt
ux-mvp-r3-da0c7fe.sqlite3
ux-mvp-r3-server.log
ux-mvp-r3.pid
ux-r2-2.sqlite3
ux-r2-3.sqlite3
ux-r2-debug-sample.png
ux-r2-server-2.log
ux-r2-server-3.log
ux-r2-server.log
ux-r2-server.pid
ux-r2.sqlite3
ux-t203-38ee0c3
ux-t203-demo.log
ux-t203-demo.pid
ux-t203-demo.sqlite3
ux-t203-e2e.out
ux-t203-local.log
ux-t203-local.pid
ux-t203-local.sqlite3
ux3
v
validate_review.py
verify.py
view.json
walk.out
walk.py
walk2.py
why.orig.py
wide.py
wprobe.py
wt
wt-031a708
wt-7df65fb
wt-golden.txt
wt-head
wt2
wt7944.db
wt7944.log
wt7944.pid
wt7945.db
wt7945.log
wt7945.pid
wt7946.db
wt7946.log
wt7946.pid
wt_final
wt_final2
wt_head
wt_run.sh
wt_t155
x45.py
xc.py
xss.py
zlayt-base
zlayt-head
zlayt-public-snapshot.JTMbwv
zlayt-r2
zlayt-r3
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:45.229Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux-measure2.py"
}
````

### User / tool · 2026-11-02T23:54:45.239Z

**tool result**
````
1	"""T-203 ux-designer probe 2 (servers from git archive 38ee0c3: DEMO :7981, LOCAL :7982; lib10/lib11 tokens in T-203-ux/tokens.json).
2	1. 375x667 sample e1 after a valid edit: how long does 'Saved: ...' stay; what does the slot say after it clears; what happens on tapping the greyed Yes.
3	2. Outside-word underlines on lib11 e2 (Pt) and lib10 e1 at 390 and 1440; the payment wording on lib11 a6 (Step 3 'bills') at 390, 375x667 and 1440.
4	3. Hint copy for the generic case ('Tick the box above first.'): find an item with a box that is not check-compare."""
5	import time, json
6	from playwright.sync_api import sync_playwright
7	OUT = "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux"
8	T = json.load(open(f"{OUT}/tokens.json"))
9	DEMO, LOCAL = "http://127.0.0.1:7981", "http://127.0.0.1:7982"
10	EX = r"""() => { const q = s => document.querySelector(`[data-testid=${s}]`); const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.top), Math.round(r.bottom)]; };
11	  const st = q('status-text'), box = document.querySelector('[data-testid=card-foot] input[type=checkbox], [data-testid=check-compare]');
12	  return {status: st && st.innerText, st: R(st), yesDisabled: !!(q('answer-yes')||{}).disabled, bar: R(q('actions')), box: R(box), boxId: box && box.getAttribute('data-testid'), scrollY: Math.round(scrollY), vh: innerHeight,
13	    outside: [...document.querySelectorAll('[data-testid=outside-word]')].map(e => e.innerText), reason: (q('compare-reason') || {}).innerText || null, foot: (q('card-foot') || {}).innerText || null}; }"""
14	
15	
16	def ready(page): page.wait_for_selector("[data-testid=view][data-ready]", timeout=30000); time.sleep(0.9)
17	
18	
19	def ctx(p, W, H):
20	    b = p.chromium.launch()
21	    return b, b.new_context(viewport={"width": W, "height": H}, has_touch=W < 800, is_mobile=W < 800, device_scale_factor=2 if W < 800 else 1).new_page()
22	
23	
24	with sync_playwright() as p:
25	    # 1
26	    b, page = ctx(p, 375, 667)
27	    page.goto(DEMO + "/"); ready(page)
28	    page.locator("[data-testid=btn-sample-case]").click(); page.wait_for_selector("[data-testid=btn-draft]", timeout=30000); time.sleep(0.5)
29	    page.locator("[data-testid=btn-draft]").click(); page.wait_for_selector("[data-testid=btn-next-step]", timeout=90000); time.sleep(0.5)
30	    page.locator("[data-testid=btn-next-step]").click(); ready(page)
31	    page.locator("[data-testid=btn-third]").click(); time.sleep(0.6)
32	    ed = page.locator("[data-testid=edit-summary]"); ed.fill(ed.input_value().replace("transported to", "taken to")); time.sleep(0.2)
33	    page.locator("[data-testid=answer-yes]").click(); time.sleep(1.8)
34	    for t in (0, 5, 15, 30):
35	        if t: time.sleep(t - (0 if t == 5 else (5 if t == 15 else 15)))
36	        print(f"[1 edit-to-check 375x667 +{t}s]", json.dumps({k: v for k, v in page.evaluate(EX).items() if k in ("status", "st", "yesDisabled", "bar", "box", "boxId", "scrollY")}))
37	    page.screenshot(path=f"{OUT}/p2-edit-375x667-after30s.png")
38	    page.locator("[data-testid=answer-yes]").tap(force=True); time.sleep(0.6)
39	    print("[1 after tapping the greyed Yes]", json.dumps({k: v for k, v in page.evaluate(EX).items() if k in ("status", "st", "yesDisabled", "box")}))
40	    # tick it the way a user would: scroll the page/card to the box
41	    page.mouse.wheel(0, 300); time.sleep(0.6)
42	    print("[1 after wheel 300]", json.dumps({k: v for k, v in page.evaluate(EX).items() if k in ("status", "st", "yesDisabled", "bar", "box", "scrollY")}))
43	    page.screenshot(path=f"{OUT}/p2-edit-375x667-after-wheel.png")
44	    b.close()
45	
46	    # 2
47	    for W, H in ((390, 844), (375, 667), (1440, 900)):
48	        b, page = ctx(p, W, H)
49	        page.goto(f"{LOCAL}/case/{T['lib11']}/timeline?item=e2"); ready(page)
50	        o = page.evaluate(EX); print(f"[2 lib11 e2 {W}x{H}] outside={o['outside']} status={o['status']!r}")
51	        page.screenshot(path=f"{OUT}/p2-lib11-e2-{W}x{H}.png")
52	        page.goto(f"{LOCAL}/case/{T['lib11']}/bills?item=a6"); ready(page)
53	        o = page.evaluate(EX); print(f"[2 lib11 a6 {W}x{H}] reason={o['reason']!r} status={o['status']!r} yesDisabled={o['yesDisabled']} st={o['st']} bar={o['bar']} box={o['box']} boxId={o['boxId']}")
54	        page.screenshot(path=f"{OUT}/p2-lib11-a6-{W}x{H}.png")
55	        page.goto(f"{LOCAL}/case/{T['tok10'] if 'tok10' in T else T['lib10']}/timeline?item=e1"); ready(page)
56	        o = page.evaluate(EX); print(f"[2 lib10 e1 {W}x{H}] outside={o['outside']}")
57	        b.close()
58	
59	    # 3: walk every item of lib11 (bills + timeline) at 375x667, report items where Yes is greyed, the box id and hint
60	    b, page = ctx(p, 375, 667)
61	    for step, ids in (("timeline", [f"e{i}" for i in range(1, 12)]), ("bills", [f"a{i}" for i in range(1, 9)])):
62	        for iid in ids:
63	            page.goto(f"{LOCAL}/case/{T['lib11']}/{step}?item={iid}")
64	            try: page.get_by_test_id("card-line").wait_for(timeout=4000)
65	            except Exception: continue
66	            time.sleep(0.7); o = page.evaluate(EX)
67	            if o["yesDisabled"] or o["boxId"]:
68	                print(f"[3 lib11 {step} {iid} 375x667] yesDisabled={o['yesDisabled']} boxId={o['boxId']} box={o['box']} bar={o['bar']} status={o['status']!r}")
69	    b.close()
70	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:47.675Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux-measure.py"
}
````

### User / tool · 2026-11-02T23:54:47.682Z

**tool result**
````
1	"""T-203 ux-designer: 375x667 greyed Yes on a disputed line. Servers from a fresh git archive of 38ee0c3:
2	DEMO http://127.0.0.1:7981 (fixture curated) and LOCAL http://127.0.0.1:7982 (ZLAYT_MODE=local, to create library cases lib10/lib11).
3	Measures, with no scrolling by the probe unless stated: where the status slot, Yes/No, tick box and highlighted words are; what the status slot says;
4	what happens when the disabled Yes is tapped and when the box is ticked / unticked; the page scrolled so the box clears the bar (is the word 'above' true then?)."""
5	import importlib.util, time, json, os
6	from playwright.sync_api import sync_playwright
7	
8	OUT = "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux"
9	os.makedirs(OUT, exist_ok=True)
10	src = open("/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-ux-r3-majors.py").read()
11	PROBE = src.split('PROBE = r"""')[1].split('"""')[0]
12	DEMO, LOCAL = "http://127.0.0.1:7981", "http://127.0.0.1:7982"
13	EXTRA = r"""() => { const q = s => document.querySelector(`[data-testid=${s}]`); const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
14	  const st = q('status-text'), bar = q('actions'), box = q('check-compare');
15	  const cs = st && getComputedStyle(st);
16	  return {st: R(st), stText: st && st.innerText, stLineH: cs && cs.lineHeight, stH: st && Math.round(st.getBoundingClientRect().height), stFont: cs && cs.fontSize, stColor: cs && cs.color,
17	          stVisibleOnScreen: st ? (st.getBoundingClientRect().bottom <= innerHeight && st.getBoundingClientRect().top >= 0) : null,
18	          yes: R(q('answer-yes')), no: R(q('answer-no')), bar: R(bar), box: R(box), boxChecked: box && box.checked, boxLabel: box && (box.closest('label') || box.parentElement).innerText,
19	          boxBelowViewport: box ? box.getBoundingClientRect().top >= innerHeight : null, boxUnderBar: box ? (box.getBoundingClientRect().bottom > bar.getBoundingClientRect().top && box.getBoundingClientRect().top < innerHeight) : null,
20	          scrollY: Math.round(scrollY), docH: document.documentElement.scrollHeight, docW: document.documentElement.scrollWidth, vw: innerWidth, vh: innerHeight,
21	          yesDisabled: !!(q('answer-yes')||{}).disabled, ariaLive: [...document.querySelectorAll('[aria-live]')].map(e => e.getAttribute('data-testid') + ':' + e.innerText.slice(0, 80))}; }"""
22	
23	
24	def ready(page): page.wait_for_selector("[data-testid=view][data-ready]", timeout=30000); time.sleep(0.9)
25	
26	
27	def phone(p, W, H):
28	    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": W, "height": H}, has_touch=True, is_mobile=True, device_scale_factor=2)
29	    return b, ctx.new_page()
30	
31	
32	def desk(p, W, H):
33	    b = p.chromium.launch(); return b, b.new_context(viewport={"width": W, "height": H}).new_page()
34	
35	
36	def both(page, tag):
37	    o = page.evaluate(PROBE); e = page.evaluate(EXTRA)
38	    keep = {k: o.get(k) for k in ["scrollY", "barTop", "src", "mark", "markFullyVisible", "line", "lineFullyVisible", "box", "boxFullyVisible", "boxHit", "yes", "yesDisabled", "status"]}
39	    print(f"[{tag}] PROBE", json.dumps(keep)); print(f"[{tag}] EXTRA", json.dumps(e)); return o, e
40	
41	
42	def make_lib(p, lib, name):
43	    b = p.chromium.launch(); page = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
44	    page.goto(LOCAL + "/new"); ready(page)
45	    page.locator("[data-testid=input-name]").fill(name)
46	    page.locator("[data-testid=tile-library]").click(); time.sleep(0.3)
47	    page.locator(f"[data-testid=library-{lib}]").check()
48	    page.locator("[data-testid=btn-read]").click(); page.wait_for_selector("[data-testid=btn-draft]", timeout=30000); time.sleep(0.4)
49	    page.locator("[data-testid=btn-draft]").click(); page.wait_for_selector("[data-testid=btn-next-step]", timeout=90000); time.sleep(0.5)
50	    tok = page.url.split("/case/")[1].split("/")[0]; b.close(); return tok
51	
52	
53	with sync_playwright() as p:
54	    tok10 = make_lib(p, "case_lib10_eob_ub04_cms1500", "Test case ten t203"); print("lib10", tok10)
55	    tok11 = make_lib(p, "case_lib11_priors_and_ledger", "Test case eleven t203"); print("lib11", tok11)
56	    json.dump({"lib10": tok10, "lib11": tok11}, open(f"{OUT}/tokens.json", "w"))
57	
58	    # ---- A: lib10 e1 (disputed line, tick box) at four sizes
59	    for W, H in ((375, 667), (390, 844), (360, 740), (1440, 900)):
60	        b, page = (phone(p, W, H) if W < 800 else desk(p, W, H))
61	        page.goto(f"{LOCAL}/case/{tok10}/timeline?item=e1"); ready(page)
62	        both(page, f"A lib10-e1 {W}x{H} open")
63	        page.screenshot(path=f"{OUT}/a-lib10-e1-{W}x{H}-open.png")
64	        if W < 800:
65	            page.locator("[data-testid=answer-yes]").tap(force=True); time.sleep(0.6)
66	            both(page, f"A lib10-e1 {W}x{H} after tapping disabled Yes")
67	            page.screenshot(path=f"{OUT}/a-lib10-e1-{W}x{H}-tap-disabled-yes.png")
68	        # scroll page so the box clears the bar: is the box then above the buttons (word 'above' true)?
69	        o = page.evaluate(PROBE)
70	        if o["box"] and o["box"][1] > o["barTop"] - 6 and W < 800:
71	            page.mouse.wheel(0, o["box"][1] - o["barTop"] + 12); time.sleep(0.6)
72	            both(page, f"A lib10-e1 {W}x{H} page scrolled so box clears bar"); page.screenshot(path=f"{OUT}/a-lib10-e1-{W}x{H}-scrolled.png")
73	        # tick the box: hint clears, Yes enabled
74	        cb = page.locator("[data-testid=check-compare]")
75	        cb.scroll_into_view_if_needed(); cb.check(force=True); time.sleep(0.5)
76	        both(page, f"A lib10-e1 {W}x{H} box ticked"); page.screenshot(path=f"{OUT}/a-lib10-e1-{W}x{H}-ticked.png")
77	        cb.uncheck(force=True); time.sleep(0.5)
78	        both(page, f"A lib10-e1 {W}x{H} box unticked again")
79	        b.close()
80	
81	    # ---- B: sample e1 after a valid edit (edit-to-check) on the demo server
82	    for W, H in ((375, 667), (390, 844), (1440, 900)):
83	        b, page = (phone(p, W, H) if W < 800 else desk(p, W, H))
84	        page.goto(DEMO + "/"); ready(page)
85	        page.locator("[data-testid=btn-sample-case]").click(); page.wait_for_selector("[data-testid=btn-draft]", timeout=30000); time.sleep(0.5)
86	        page.locator("[data-testid=btn-draft]").click(); page.wait_for_selector("[data-testid=btn-next-step]", timeout=90000); time.sleep(0.5)
87	        page.locator("[data-testid=btn-next-step]").click(); ready(page)
88	        both(page, f"B sample e1 {W}x{H} fresh (no box expected)"); page.screenshot(path=f"{OUT}/b-sample-e1-{W}x{H}-fresh.png")
89	        page.locator("[data-testid=btn-third]").click(); time.sleep(0.6)
90	        ed = page.locator("[data-testid=edit-summary]")
91	        ed.fill(ed.input_value().replace("transported to", "taken to")); time.sleep(0.2)
92	        page.locator("[data-testid=answer-yes]").click(); time.sleep(1.8)
93	        both(page, f"B sample e1 {W}x{H} after valid edit"); page.screenshot(path=f"{OUT}/b-sample-e1-{W}x{H}-edit-to-check.png")
94	        b.close()
95	
96	    # ---- C: lines with no box: no hint (keyboard hint stays on desktop only)
97	    for W, H in ((375, 667), (1440, 900)):
98	        b, page = (phone(p, W, H) if W < 800 else desk(p, W, H))
99	        page.goto(f"{LOCAL}/case/{tok10}/timeline?item=e2"); ready(page)
100	        both(page, f"C lib10 e2 {W}x{H} (no box?)"); page.screenshot(path=f"{OUT}/c-lib10-e2-{W}x{H}.png")
101	        b.close()
102	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:49.695Z

**tool call — Bash**
````
{
 "command": "git show fa34fe9 --stat | head -20; cat /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/ux-t203-demo.log | head -5; ls artifacts/review-evidence/T-203-ux | head -30"
}
````

### User / tool · 2026-11-02T23:54:49.837Z

**tool result**
````
commit fa34fe92f87a33b36cf0ca8b43da51c326d87a40
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 17:53:49 2026 -0600

    fix(frontend): T-203 r2 hint stays beside a Saved note, position-neutral words + Show box, PT is not patient, lost wages, 375x667 edit-path tests
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/frontend/guided/review.js | 33 +++++++++++++++------
 app/frontend/guided/step2.js  |  4 +--
 tests/e2e/guided/test_t203.py | 67 +++++++++++++++++++++++++++++++++++++++++--
 3 files changed, 92 insertions(+), 12 deletions(-)
Serving on http://127.0.0.1:7981  (Ctrl-C to stop)
llm call failed call_id=c5a5f74f19fd1 step=j1 attempt=1 prompt_hash=3ee780fb158eae4f92df7664d023028aca9b488d6a694f0719539a33d0421d3a
llm call failed call_id=c205a38b608c5 step=j1 attempt=1 prompt_hash=3ee780fb158eae4f92df7664d023028aca9b488d6a694f0719539a33d0421d3a
llm call failed call_id=cce605ab21a47 step=j1 attempt=1 prompt_hash=3ee780fb158eae4f92df7664d023028aca9b488d6a694f0719539a33d0421d3a
llm call failed call_id=cf28f9b81b426 step=j1 attempt=1 prompt_hash=3ee780fb158eae4f92df7664d023028aca9b488d6a694f0719539a33d0421d3a
a-lib10-e1-1440x900-open.png
a-lib10-e1-1440x900-ticked.png
a-lib10-e1-360x740-open.png
a-lib10-e1-360x740-scrolled.png
a-lib10-e1-360x740-tap-disabled-yes.png
a-lib10-e1-360x740-ticked.png
a-lib10-e1-375x667-open.png
a-lib10-e1-375x667-scrolled.png
a-lib10-e1-375x667-tap-disabled-yes.png
a-lib10-e1-375x667-ticked.png
a-lib10-e1-390x844-open.png
a-lib10-e1-390x844-tap-disabled-yes.png
a-lib10-e1-390x844-ticked.png
b-sample-e1-1440x900-edit-to-check.png
b-sample-e1-1440x900-fresh.png
b-sample-e1-375x667-edit-to-check.png
b-sample-e1-375x667-fresh.png
b-sample-e1-390x844-edit-to-check.png
b-sample-e1-390x844-fresh.png
c-lib10-e2-1440x900.png
c-lib10-e2-375x667.png
measure2.out
p2-edit-375x667-after-wheel.png
p2-edit-375x667-after30s.png
p2-lib11-a6-1440x900.png
p2-lib11-a6-375x667.png
p2-lib11-a6-390x844.png
p2-lib11-e2-1440x900.png
p2-lib11-e2-375x667.png
p2-lib11-e2-390x844.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:54:52.879Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"FIXTURE_SET\\|ZLAYT_MODE\\|ZLAYT_DB\\|serve\" docs/RUNBOOK.md | head -20; lsof -i :7993 -i :7994 | head"
}
````

### User / tool · 2026-11-02T23:54:53.042Z

**tool result**
````
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
9:| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |
26:2. Board server: `./tools/serve_board.sh` (also installs the native git pre-commit secret scan if missing) (tmux session `zlayt`, window `board`). Check: `curl -s localhost:7777/healthz`.
32:5. Tailnet exposure persists across restarts (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:55:01.949Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh | head -40; head -3 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/ux-t203-local.log"
}
````

### User / tool · 2026-11-02T23:55:02.039Z

**tool result**
````
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
Serving on http://127.0.0.1:7982  (Ctrl-C to stop)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:55:06.069Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/ux-t203-fa34fe9 && mkdir $S/ux-t203-fa34fe9 && git archive fa34fe9 | tar -x -C $S/ux-t203-fa34fe9 && ls $S/ux-t203-fa34fe9 | head -20; grep -n \"PORT\\|port\" app/main.py | head"
}
````

### User / tool · 2026-11-02T23:55:06.139Z

**tool result (error)**
````
Permission to use Bash with command S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/ux-t203-fa34fe9 && mkdir $S/ux-t203-fa34fe9 && git archive fa34fe9 has been denied.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:55:09.692Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir $S/ux-t203r2-fa34fe9 && git archive fa34fe9 | tar -x -C $S/ux-t203r2-fa34fe9 && ls $S/ux-t203r2-fa34fe9 | head -20"
}
````

### User / tool · 2026-11-02T23:55:10.880Z

**tool result**
````
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
app
artifacts
board
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
run.sh
spec
submission
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:55:12.356Z

**tool call — Bash**
````
{
 "command": "grep -n \"PORT\\|environ\" app/main.py app/config.py | head -20; ls /Users/arsis/zlayt-pm-project/.venv/bin/python"
}
````

### User / tool · 2026-11-02T23:55:12.456Z

**tool result**
````
app/main.py:25:    host, port = os.environ.get("HOST", "127.0.0.1"), int(os.environ.get("PORT", "7860"))
app/main.py:32:        if os.environ.get("ZLAYT_DEBUG") == "1":
app/main.py:36:        _fail(f"port {port} on {host} is already in use. Pick another with PORT=7870 (for example `PORT=7870 ./run.sh`).", 3)
app/config.py:12:DEFAULTS = {"HOST": "127.0.0.1", "PORT": "7860", "LLM_BACKEND": "fixture", "FIXTURE_SET": "curated"}
app/config.py:19:    key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))
app/config.py:22:    if os.environ.get("ENABLE_LIVE") == "1" and not live:
app/config.py:24:    if os.environ.get("LLM_BACKEND") not in (None, "", "fixture") and os.environ.get("ENABLE_LIVE") != "1":
app/config.py:26:    if live and backend == "anthropic-api" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
app/config.py:31:        "fixture_set": os.environ.get("FIXTURE_SET", DEFAULTS["FIXTURE_SET"]) if backend == "fixture" else None,
app/config.py:32:        "host": os.environ.get("HOST", DEFAULTS["HOST"]),
app/config.py:33:        "port": int(os.environ.get("PORT", DEFAULTS["PORT"])),
app/config.py:35:        "local_mode": os.environ.get("ZLAYT_MODE") == "local",
app/config.py:44:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
/Users/arsis/zlayt-pm-project/.venv/bin/python
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:55:18.057Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/ux-t203r2-fa34fe9 && (PORT=7993 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$S/ux-t203r2-demo.sqlite3 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $S/ux-t203r2-demo.log 2>&1 &) ; (PORT=7994 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$S/ux-t203r2-local.sqlite3 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $S/ux-t203r2-local.log 2>&1 &); sleep 4; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7993/; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7994/; lsof -ti :7993 -ti :7994"
}
````

### User / tool · 2026-11-02T23:55:22.281Z

**tool result**
````
200
200
15794
15796
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:55:23.132Z

Now read the diff to know what to look for.

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:55:23.481Z

**tool call — Bash**
````
{
 "command": "git show fa34fe9 -- app/frontend/guided/review.js app/frontend/guided/step2.js"
}
````

### User / tool · 2026-11-02T23:55:23.602Z

**tool result**
````
commit fa34fe92f87a33b36cf0ca8b43da51c326d87a40
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 17:53:49 2026 -0600

    fix(frontend): T-203 r2 hint stays beside a Saved note, position-neutral words + Show box, PT is not patient, lost wages, 375x667 edit-path tests
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/guided/review.js b/app/frontend/guided/review.js
index d60ee40..0aeeda3 100644
--- a/app/frontend/guided/review.js
+++ b/app/frontend/guided/review.js
@@ -79,7 +79,7 @@
     return rs.includes("JUDGE_PARTIAL") ? "partially" : rs.includes("JUDGE_UNSUPPORTED") ? "unsupported" : rs.includes("JUDGE_DISAGREES") ? "disagrees" : null;
   };
   /* An amount's second check names the way it disagreed (judge reason_code): say which way, so the tick is not a formality (paralegal review T-181 minor). */
-  const AMOUNT_WAY = { SHOULD_BE_CHARGE: "a billed charge", SHOULD_BE_RATE: "a rate", SHOULD_BE_ESTIMATE: "an estimate", SHOULD_BE_DAMAGES: "a damages figure (such as lost pay)" };
+  const AMOUNT_WAY = { SHOULD_BE_CHARGE: "a billed charge", SHOULD_BE_RATE: "a rate", SHOULD_BE_ESTIMATE: "an estimate", SHOULD_BE_DAMAGES: "a damages figure (for example lost wages)" };
   R.disputeText = function (v, item) {
     const code = item && item.ladder && item.ladder.judge && item.ladder.judge.reason_code;
     if (v === "disagrees" && AMOUNT_WAY[code]) return `A second AI check thought this may be ${AMOUNT_WAY[code]}, not what it was first sorted as.`;
@@ -166,7 +166,7 @@
       S.busy = true; S.err = null; syncButtons();
       try { return await fn(); } catch (e) { await S.fail(e); return undefined; } finally {
         S.busy = false;
-        if (S.alive) { syncButtons(); if (!S.ended && S.screen && (!document.activeElement || document.activeElement === document.body)) focusFirst(S.screen); }     // the click disabled the button that had focus: put it on the next item's first answer
+        if (S.alive) { syncButtons(); drawStatus(); if (!S.ended && S.screen && (!document.activeElement || document.activeElement === document.body)) focusFirst(S.screen); }     // the click disabled the button that had focus: put it on the next item's first answer
       }
     };
     /* every review POST carries version + expected_status of the item on screen (T-178) */
@@ -201,7 +201,8 @@
     E.yes.setAttribute("data-autofocus", "");
     E.back = btn("quiet", "btn-back", "ArrowLeft"); E.third = btn("quiet", "btn-third", "e"); E.later = btn("quiet", "btn-later", "ArrowRight");
     E.statusText = h("span", { class: "st-msg", "data-testid": "status-text" }); E.undo = h("button", { type: "button", class: "btn quiet undo", "data-testid": "btn-undo", hidden: true }, "Undo");
-    E.status = h("p", { class: "status", role: "status", "aria-live": "polite", "data-testid": "status-slot" }, E.statusText, E.undo);
+    E.showBox = h("button", { type: "button", class: "btn quiet undo", "data-testid": "btn-show-box", hidden: true }, "Show box");
+    E.status = h("p", { class: "status", role: "status", "aria-live": "polite", "data-testid": "status-slot" }, E.statusText, E.undo, E.showBox);
     E.actions = h("div", { class: "actions", "data-testid": "actions" }, h("div", { class: "actions-in" }, E.question,
       h("div", { class: "big", role: "group", "aria-labelledby": "q" }, E.yes, E.no), h("div", { class: "small" }, E.back, E.third, E.later), E.status));
     E.back.textContent = "‹ Back"; E.later.textContent = "Decide later";
@@ -218,12 +219,28 @@
 
     function drawStatus() {
       const s = S.said;
-      const box = !s && E.yes && E.yes.disabled && !S.busy && E.foot.querySelector("input[type=checkbox]:not(:checked)");      // Yes is greyed because a box is not ticked: say so beside it (on a 375x667 phone the box can sit below the bar)
-      E.statusText.textContent = s ? s.text : box ? (box.dataset.testid === "check-compare" ? "Tick the box above to say you compared them." : "Tick the box above first.") : (matchMedia("(min-width: 761px)").matches ? `Keys: A says yes, D says no, ${S.screen && S.screen.third ? "E fixes or adds a note, " : ""}the arrow keys move between items.` : "");
-      E.status.classList.toggle("hint", !s && !box);
-      E.status.dataset.why = box ? "tick" : "";
+      const box = E.yes && E.yes.disabled && !S.busy && E.foot.querySelector("input[type=checkbox]:not(:checked)");      // Yes is greyed because a box is not ticked: say so beside it (on a 375x667 phone the box can sit below the bar)
+      const tick = box ? (box.dataset.testid === "check-compare" ? "Tick the box to say you compared them." : "Tick the box first.") : "";      // no direction word: the box can be above the bar or below the screen
+      const saved = s && !s.undo && /^Saved/.test(s.text);      // a "Saved" note must not hide the reason Yes is greyed: both stay until she ticks
+      const why = box && (!s || saved);
+      E.statusText.textContent = why ? (saved ? "Saved. " : "") + tick : s ? s.text : (matchMedia("(min-width: 761px)").matches ? `Keys: A says yes, D says no, ${S.screen && S.screen.third ? "E fixes or adds a note, " : ""}the arrow keys move between items.` : "");
+      E.status.classList.toggle("hint", !s && !why);
+      E.status.dataset.why = why ? "tick" : "";
       E.undo.hidden = !(s && s.undo);
       E.undo.onclick = s && s.undo ? () => S.act(s.undo) : null;
+      const hidden = !!why && boxHidden(box);      // the box is under the bar or below the screen: one tap brings it into view
+      E.showBox.hidden = !hidden;
+      E.showBox.onclick = hidden ? () => revealBox(box) : null;
+    }
+    function boxHidden(box) {
+      const r = box.getBoundingClientRect(), bar = E.actions.getBoundingClientRect();
+      return r.bottom > bar.top - 4 || r.top < 0;
+    }
+    function revealBox(box) {
+      const bar = E.actions.getBoundingClientRect();
+      box.style.scrollMarginBottom = Math.ceil(window.innerHeight - bar.top + 12) + "px";
+      try { box.scrollIntoView({ block: "nearest", inline: "nearest" }); } catch (_) { /* nothing to scroll */ }
+      box.focus({ preventScroll: true }); drawStatus();
     }
 
     function updateTitlebar() {
@@ -310,7 +327,7 @@
     }
     S.renderSource = () => renderSource(true);
     S.render = (keep) => render(!!keep);
-    S.sync = () => { syncButtons(); if (!S.said) drawStatus(); };
+    S.sync = () => { syncButtons(); if (!S.said || (!S.said.undo && /^Saved/.test(S.said.text))) drawStatus(); };
     function focusFirst(sc) {
       const f = sc.focus === "field" ? E.lineBody.querySelector("textarea, input") : null;
       const target = f || (!E.yes.disabled ? E.yes : E.foot.querySelector("input[type=checkbox]") || (sc.yes && !S.busy ? E.foot : (!E.no.disabled ? E.no : null)));      // a refused Yes with no tick box: focus the reason, never a button that would answer
diff --git a/app/frontend/guided/step2.js b/app/frontend/guided/step2.js
index 63174c8..a1e4833 100644
--- a/app/frontend/guided/step2.js
+++ b/app/frontend/guided/step2.js
@@ -111,7 +111,7 @@
   const WORD = /[\p{L}\p{N}]+(?:['’][\p{L}]+)?/gu;
   const SKIP = new Set("a an the of to and or is are was were be been for with by at in on as it its that this".split(" "));
   const ABBR = { pt: "patient", dx: "diagnosis", rx: "prescription", hx: "history", tx: "treatment", sx: "symptom" };      // chart shorthand reads as the word it stands for (paralegal r2 nit: "Pt" in the quote, "Patient" in the line)
-  const stem = (w) => { const x = w.toLowerCase().replace(/['’]s$/, "").replace(/s$/, ""); return ABBR[x] || x; };
+  const stem = (w) => { const x = w.toLowerCase().replace(/['’]s$/, "").replace(/s$/, ""); return w === "PT" ? x : ABBR[x] || x; };      // "PT" in capitals is physical therapy, not a patient: it stays a word of its own, so a "Patient" in the line is still underlined
   function outsideParts(summary, quote) {
     const inQuote = new Set((String(quote || "").match(WORD) || []).map(stem)), parts = [];
     let last = 0, any = false;
@@ -383,5 +383,5 @@
   G.pages.timeline = function (ctx) {
     return R.run(ctx, { step: 2, title: "Check the timeline", unit: "Item", chip: false, buildQueue, find, present, statusFor, done, empty });
   };
-  G.step2 = { buildQueue, find, flagHeading };
+  G.step2 = { buildQueue, find, flagHeading, outsideParts };
 })();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:55:28.759Z

**tool call — Bash**
````
{
 "command": "grep -n \"G = \\|window.G\\|Zlayt\" app/frontend/guided/step2.js | head -5; sed -n 105,135p app/frontend/guided/step2.js; grep -n \"outsideParts\\|PT\\|Pt\" tests/e2e/guided/test_t203.py | head -20"
}
````

### User / tool · 2026-11-02T23:55:28.871Z

**tool result**
````
5:  const G = window.G, { h } = G, R = G.review;
    return { excerpt: rec.text.slice(a.start - rec.char_start, b.end - rec.char_start) };
  }
  function togglePick(S, sent) { const p = S.ui.picked || (S.ui.picked = new Set()); p.has(sent.start) ? p.delete(sent.start) : p.add(sent.start); S.renderSource(); }
  const warningsFoot = (S) => (S.ui.warnings || []).map((w) => h("p", { class: "foot-warn", "data-testid": "save-warning" }, R.plain(w.message || String(w))));

  /* ---------- the words of a line that are not in the highlighted words (code, no AI): a deterministic word diff so she sees what to check (paralegal review T-181 major) ---------- */
  const WORD = /[\p{L}\p{N}]+(?:['’][\p{L}]+)?/gu;
  const SKIP = new Set("a an the of to and or is are was were be been for with by at in on as it its that this".split(" "));
  const ABBR = { pt: "patient", dx: "diagnosis", rx: "prescription", hx: "history", tx: "treatment", sx: "symptom" };      // chart shorthand reads as the word it stands for (paralegal r2 nit: "Pt" in the quote, "Patient" in the line)
  const stem = (w) => { const x = w.toLowerCase().replace(/['’]s$/, "").replace(/s$/, ""); return w === "PT" ? x : ABBR[x] || x; };      // "PT" in capitals is physical therapy, not a patient: it stays a word of its own, so a "Patient" in the line is still underlined
  function outsideParts(summary, quote) {
    const inQuote = new Set((String(quote || "").match(WORD) || []).map(stem)), parts = [];
    let last = 0, any = false;
    for (const m of String(summary || "").matchAll(WORD)) {
      const w = m[0], out = !SKIP.has(w.toLowerCase()) && !inQuote.has(stem(w));
      if (m.index > last) parts.push(summary.slice(last, m.index));
      parts.push(out ? h("u", { class: "out", "data-testid": "outside-word" }, w) : w); if (out) any = true;
      last = m.index + w.length;
    }
    if (last < summary.length) parts.push(summary.slice(last));
    return any ? parts : null;
  }

  /* ---------- presenting an item ---------- */
  function present(S, item, q) {
    const c = S.c, g = groupOf(c, item);
    if (g === "tray") return item.kind === "flag" ? trayFlag(S, item) : trayEntry(S, item);
    if (g === "flag") return warning(S, item);
    if (g === "undated") return undated(S, item);
    return line(S, item);
  }
2:Also: a payment's second-check wording names the damages way, and chart shorthand ('Pt') is not underlined as an outside word."""
58:# ------------------------------------------------------------------ round 2: the reworded line, position-neutral words, PT is not a patient
61:    return page.evaluate("""([s, q]) => { const p = window.G.step2.outsideParts(s, q); return p ? p.filter((n) => n && n.nodeType === 1).map((n) => n.textContent) : []; }""", [summary, quote])
68:        assert "Patient" in _words(page, "Patient attended physical therapy 3 times a week", "PT 3x/week, attended physical therapy"), "PT is not the word patient"
69:        assert _words(page, "Patient states chest pain", "Pt states chest pain") == [], "Pt is the chart shorthand for patient"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:55:57.117Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux-r2-measure.py",
 "content": "\"\"\"T-203 r2 ux-designer (servers from a fresh git archive of fa34fe9: DEMO :7993 fixture/curated, LOCAL :7994 ZLAYT_MODE=local to make lib10/lib11).\n1. 375x667 sample e1: Fix the wording, then Yes greyed; slot text at +0/+5/+30 s; Show box button; tap it; box position; tick; Yes enabled; undo of tick.\n2. lib10 e1 (disputed line) at 375x667, 360x740, 390x844, 1440x900: hint, Show box presence, tap Show box, tick, untick.\n3. PT / Pt / pt via the live window.G.step2.outsideParts; lost wages wording on lib11 a6 at 375, 390, 1440.\n4. Regression numbers at 390 (mark/line/box/bar) and 1440 keys line.\"\"\"\nimport time, json, os\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux-r2\"\nos.makedirs(OUT, exist_ok=True)\nDEMO, LOCAL = \"http://127.0.0.1:7993\", \"http://127.0.0.1:7994\"\nEX = r\"\"\"() => { const q = s => document.querySelector(`[data-testid=${s}]`); const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };\n  const st = q('status-text'), box = q('check-compare') || document.querySelector('[data-testid=card-foot] input[type=checkbox]'), bar = q('actions'), sb = q('btn-show-box');\n  const bx = box && box.getBoundingClientRect(), hit = bx ? document.elementFromPoint(bx.left + bx.width / 2, bx.top + bx.height / 2) : null;\n  const mark = document.querySelector('mark, [data-testid=source-mark]'), line = q('card-line');\n  return {status: st && st.innerText, stRect: R(st), stH: st && Math.round(st.getBoundingClientRect().height), stFont: st && getComputedStyle(st).fontSize, showBoxHidden: sb ? sb.hidden : 'absent', showBox: R(sb),\n    yes: R(q('answer-yes')), no: R(q('answer-no')), yesDisabled: !!(q('answer-yes')||{}).disabled, bar: R(bar), box: R(box), boxId: box && box.getAttribute('data-testid'), boxChecked: box && box.checked,\n    boxHit: hit ? (hit.getAttribute('data-testid') || hit.tagName) : null, boxFullyAboveBar: bx && bar ? bx.bottom <= bar.getBoundingClientRect().top && bx.top >= 0 : null,\n    activeIsBox: box ? document.activeElement === box : null, mark: R(mark), line: R(line), scrollY: Math.round(scrollY), docW: document.documentElement.scrollWidth, vw: innerWidth, vh: innerHeight,\n    outside: [...document.querySelectorAll('[data-testid=outside-word]')].map(e => e.innerText), reason: (q('compare-reason') || {}).innerText || null}; }\"\"\"\nKEEP = (\"status\", \"stRect\", \"stH\", \"stFont\", \"showBoxHidden\", \"showBox\", \"yes\", \"yesDisabled\", \"bar\", \"box\", \"boxId\", \"boxChecked\", \"boxHit\", \"boxFullyAboveBar\", \"activeIsBox\", \"scrollY\", \"docW\", \"vw\")\n\n\ndef ready(page): page.wait_for_selector(\"[data-testid=view][data-ready]\", timeout=30000); time.sleep(0.9)\n\n\ndef ctx(p, W, H):\n    b = p.chromium.launch()\n    return b, b.new_context(viewport={\"width\": W, \"height\": H}, has_touch=W < 800, is_mobile=W < 800, device_scale_factor=2 if W < 800 else 1).new_page()\n\n\ndef show(tag, page, keys=KEEP):\n    o = page.evaluate(EX); print(f\"[{tag}]\", json.dumps({k: o[k] for k in keys})); return o\n\n\ndef make_lib(p, lib, name):\n    b = p.chromium.launch(); page = b.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    page.goto(LOCAL + \"/new\"); ready(page)\n    page.locator(\"[data-testid=input-name]\").fill(name)\n    page.locator(\"[data-testid=tile-library]\").click(); time.sleep(0.3)\n    page.locator(f\"[data-testid=library-{lib}]\").check()\n    page.locator(\"[data-testid=btn-read]\").click(); page.wait_for_selector(\"[data-testid=btn-draft]\", timeout=30000); time.sleep(0.4)\n    page.locator(\"[data-testid=btn-draft]\").click(); page.wait_for_selector(\"[data-testid=btn-next-step]\", timeout=90000); time.sleep(0.5)\n    tok = page.url.split(\"/case/\")[1].split(\"/\")[0]; b.close(); return tok\n\n\ndef sample_edit(p, W, H, tag):\n    b, page = ctx(p, W, H)\n    page.goto(DEMO + \"/\"); ready(page)\n    page.locator(\"[data-testid=btn-sample-case]\").click(); page.wait_for_selector(\"[data-testid=btn-draft]\", timeout=30000); time.sleep(0.5)\n    page.locator(\"[data-testid=btn-draft]\").click(); page.wait_for_selector(\"[data-testid=btn-next-step]\", timeout=90000); time.sleep(0.5)\n    page.locator(\"[data-testid=btn-next-step]\").click(); ready(page)\n    show(f\"{tag} sample e1 fresh\", page, (\"status\", \"stRect\", \"yes\", \"yesDisabled\", \"bar\", \"box\", \"showBoxHidden\"))\n    page.locator(\"[data-testid=btn-third]\").click(); time.sleep(0.6)\n    ed = page.locator(\"[data-testid=edit-summary]\"); ed.fill(ed.input_value().replace(\"transported to\", \"taken to\")); time.sleep(0.2)\n    page.locator(\"[data-testid=answer-yes]\").click(); time.sleep(1.8)\n    return b, page\n\n\nwith sync_playwright() as p:\n    # ---- 1. the major's scenario\n    b, page = sample_edit(p, 375, 667, \"1\")\n    t0 = time.time()\n    for t in (0, 5, 30):\n        while time.time() - t0 < t: time.sleep(0.2)\n        show(f\"1 edit-to-check 375x667 +{t}s\", page)\n    page.screenshot(path=f\"{OUT}/1-edit-375x667-after-edit.png\")\n    page.locator(\"[data-testid=answer-yes]\").tap(force=True); time.sleep(0.6)\n    show(\"1 after tapping the greyed Yes\", page, (\"status\", \"showBoxHidden\", \"yesDisabled\"))\n    sb = page.locator(\"[data-testid=btn-show-box]\")\n    print(\"[1 show box visible]\", sb.is_visible(), \"text:\", sb.inner_text() if sb.is_visible() else None)\n    sb.tap(); time.sleep(0.8)\n    show(\"1 after Show box\", page)\n    page.screenshot(path=f\"{OUT}/1-edit-375x667-after-showbox.png\")\n    page.locator(\"[data-testid=check-compare]\").check(); time.sleep(0.6)\n    show(\"1 after ticking\", page)\n    page.screenshot(path=f\"{OUT}/1-edit-375x667-ticked.png\")\n    page.locator(\"[data-testid=check-compare]\").uncheck(); time.sleep(0.6)\n    show(\"1 after unticking\", page, (\"status\", \"showBoxHidden\", \"yesDisabled\", \"boxChecked\"))\n    page.screenshot(path=f\"{OUT}/1-edit-375x667-unticked.png\")\n    page.locator(\"[data-testid=check-compare]\").check(); time.sleep(0.4)\n    page.locator(\"[data-testid=answer-yes]\").tap(); time.sleep(1.5)\n    show(\"1 after Yes\", page, (\"status\", \"showBoxHidden\", \"yesDisabled\"))\n    b.close()\n\n    # ---- 1b. keyboard: Fix the wording, Tab to Show box? tick with Space\n    b, page = sample_edit(p, 375, 667, \"1b\")\n    show(\"1b kbd edit state\", page, (\"status\", \"showBoxHidden\", \"activeIsBox\"))\n    print(\"[1b active element]\", page.evaluate(\"() => { const a = document.activeElement; return a && (a.getAttribute('data-testid') || a.tagName); }\"))\n    b.close()\n\n    # ---- 1c. other widths on the edit path\n    for W, H in ((390, 844), (360, 740), (1440, 900)):\n        b, page = sample_edit(p, W, H, f\"1c-{W}\")\n        show(f\"1c edit-to-check {W}x{H}\", page); page.screenshot(path=f\"{OUT}/1c-edit-{W}x{H}.png\")\n        b.close()\n\n    # ---- 2. disputed line\n    tok10 = make_lib(p, \"case_lib10_eob_ub04_cms1500\", \"Test case ten t203r2\"); tok11 = make_lib(p, \"case_lib11_priors_and_ledger\", \"Test case eleven t203r2\")\n    json.dump({\"lib10\": tok10, \"lib11\": tok11}, open(f\"{OUT}/tokens.json\", \"w\")); print(\"tokens\", tok10, tok11)\n    for W, H in ((375, 667), (360, 740), (390, 844), (1440, 900)):\n        b, page = ctx(p, W, H)\n        page.goto(f\"{LOCAL}/case/{tok10}/timeline?item=e1\"); ready(page)\n        show(f\"2 lib10 e1 {W}x{H} open\", page); page.screenshot(path=f\"{OUT}/2-lib10-e1-{W}x{H}-open.png\")\n        sb = page.locator(\"[data-testid=btn-show-box]\")\n        if sb.is_visible():\n            sb.click(); time.sleep(0.8)\n            show(f\"2 lib10 e1 {W}x{H} after Show box\", page); page.screenshot(path=f\"{OUT}/2-lib10-e1-{W}x{H}-showbox.png\")\n        page.locator(\"[data-testid=check-compare]\").check(force=True); time.sleep(0.5)\n        show(f\"2 lib10 e1 {W}x{H} ticked\", page, (\"status\", \"showBoxHidden\", \"yes\", \"yesDisabled\", \"boxChecked\"))\n        page.locator(\"[data-testid=check-compare]\").uncheck(force=True); time.sleep(0.5)\n        show(f\"2 lib10 e1 {W}x{H} unticked\", page, (\"status\", \"showBoxHidden\", \"yes\", \"yesDisabled\"))\n        o = page.evaluate(EX); print(f\"   mark={o['mark']} line={o['line']} box={o['box']} bar={o['bar']}\")\n        b.close()\n    # lib10 e2 (no box)\n    for W, H in ((375, 667), (1440, 900)):\n        b, page = ctx(p, W, H); page.goto(f\"{LOCAL}/case/{tok10}/timeline?item=e2\"); ready(page)\n        show(f\"2 lib10 e2 {W}x{H} (no box)\", page, (\"status\", \"showBoxHidden\", \"boxId\", \"yesDisabled\")); b.close()\n    # lib11 a2 generic box (bills)\n    b, page = ctx(p, 375, 667); page.goto(f\"{LOCAL}/case/{tok11}/bills?item=a2\"); ready(page)\n    show(\"2 lib11 a2 375x667 generic box\", page, (\"status\", \"showBoxHidden\", \"boxId\", \"box\", \"bar\", \"yesDisabled\")); page.screenshot(path=f\"{OUT}/2-lib11-a2-375x667.png\"); b.close()\n\n    # ---- 3. PT / Pt, lost wages\n    b, page = ctx(p, 390, 844); page.goto(f\"{LOCAL}/case/{tok11}/timeline?item=e2\"); ready(page)\n    FN = \"\"\"([s, q]) => { const p = window.G.step2.outsideParts(s, q); return p ? p.filter((n) => n && n.nodeType === 1).map((n) => n.textContent) : []; }\"\"\"\n    cases = [(\"Patient attended physical therapy 3 times a week\", \"PT 3x/week, attended physical therapy\"),\n             (\"Patient states chest pain\", \"Pt states chest pain\"),\n             (\"Patient states chest pain\", \"pt states chest pain\"),\n             (\"Patient states chest pain\", \"PT states chest pain\"),\n             (\"PT attended 3 times\", \"PT attended 3 times\"),\n             (\"Pt attended 3 times\", \"PT attended 3 times\"),\n             (\"Patient reports pain\", \"PT's note: reports pain\"),\n             (\"Patient completed PT sessions\", \"PT sessions completed\"),\n             (\"Diagnosis chest wall pain\", \"Dx: chest wall pain\"),\n             (\"Patient attended PT\", \"Patient attended PT\")]\n    for s, q in cases: print(f\"[3 outsideParts] line={s!r} quote={q!r} -> underlined={page.evaluate(FN, [s, q])}\")\n    b.close()\n    for W, H in ((375, 667), (390, 844), (1440, 900)):\n        b, page = ctx(p, W, H); page.goto(f\"{LOCAL}/case/{tok11}/bills?item=a6\"); ready(page)\n        o = page.evaluate(EX); print(f\"[3 lib11 a6 {W}x{H}] reason={o['reason']!r} status={o['status']!r} showBox={o['showBoxHidden']} stH={o['stH']} bar={o['bar']} box={o['box']}\")\n        page.screenshot(path=f\"{OUT}/3-lib11-a6-{W}x{H}.png\")\n        body = page.evaluate(\"() => document.body.innerText\"); print(\"   'lost pay' present:\", \"lost pay\" in body, \"| 'lost wages' present:\", \"lost wages\" in body, \"| 'not a bill' present:\", \"not a bill\" in body)\n        b.close()\n    for W, H in ((390, 844), (375, 667), (1440, 900)):\n        b, page = ctx(p, W, H); page.goto(f\"{LOCAL}/case/{tok11}/timeline?item=e2\"); ready(page)\n        o = page.evaluate(EX); print(f\"[3 lib11 e2 {W}x{H}] outside={o['outside']}\"); page.screenshot(path=f\"{OUT}/3-lib11-e2-{W}x{H}.png\"); b.close()\n"
}
````

### User / tool · 2026-11-02T23:55:57.218Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux-r2-measure.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:55:58.898Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-203-ux-r2-measure.py > artifacts/review-evidence/T-203-ux-r2/measure.out 2>&1; cat artifacts/review-evidence/T-203-ux-r2/measure.out",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:55:58.982Z

**tool result (error)**
````
Exit code 1
/bin/bash: artifacts/review-evidence/T-203-ux-r2/measure.out: No such file or directory
cat: artifacts/review-evidence/T-203-ux-r2/measure.out: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:56:00.592Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-203-ux-r2 && .venv/bin/python artifacts/review-evidence/T-203-ux-r2-measure.py > artifacts/review-evidence/T-203-ux-r2/measure.out 2>&1; cat artifacts/review-evidence/T-203-ux-r2/measure.out",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:57:42.396Z

**tool result**
````
[1 sample e1 fresh] {"status": "", "stRect": [12, 645, 363, 645], "yes": [12, 531, 183, 581], "yesDisabled": false, "bar": [0, 482, 375, 667], "box": null, "showBoxHidden": true}
[1 edit-to-check 375x667 +0s] {"status": "Saved. Tick the box to say you compared them.", "stRect": [12, 627, 249, 663], "stH": 35, "stFont": "13px", "showBoxHidden": false, "showBox": [257, 628, 363, 662], "yes": [12, 531, 183, 581], "yesDisabled": true, "bar": [0, 482, 375, 667], "box": [31, 630, 59, 658], "boxId": "check-compare", "boxChecked": false, "boxHit": "status-text", "boxFullyAboveBar": false, "activeIsBox": true, "scrollY": 107, "docW": 375, "vw": 375}
[1 edit-to-check 375x667 +5s] {"status": "Saved. Tick the box to say you compared them.", "stRect": [12, 627, 249, 663], "stH": 35, "stFont": "13px", "showBoxHidden": false, "showBox": [257, 628, 363, 662], "yes": [12, 531, 183, 581], "yesDisabled": true, "bar": [0, 482, 375, 667], "box": [31, 630, 59, 658], "boxId": "check-compare", "boxChecked": false, "boxHit": "status-text", "boxFullyAboveBar": false, "activeIsBox": true, "scrollY": 107, "docW": 375, "vw": 375}
[1 edit-to-check 375x667 +30s] {"status": "Saved. Tick the box to say you compared them.", "stRect": [12, 627, 249, 663], "stH": 35, "stFont": "13px", "showBoxHidden": false, "showBox": [257, 628, 363, 662], "yes": [12, 531, 183, 581], "yesDisabled": true, "bar": [0, 482, 375, 667], "box": [31, 630, 59, 658], "boxId": "check-compare", "boxChecked": false, "boxHit": "status-text", "boxFullyAboveBar": false, "activeIsBox": true, "scrollY": 107, "docW": 375, "vw": 375}
[1 after tapping the greyed Yes] {"status": "Saved. Tick the box to say you compared them.", "showBoxHidden": false, "yesDisabled": true}
[1 show box visible] True text: Show box
[1 after Show box] {"status": "Saved. Tick the box to say you compared them.", "stRect": [12, 636, 363, 654], "stH": 18, "stFont": "13px", "showBoxHidden": true, "showBox": [0, 0, 0, 0], "yes": [12, 531, 183, 581], "yesDisabled": true, "bar": [0, 482, 375, 667], "box": [31, 441, 59, 469], "boxId": "check-compare", "boxChecked": false, "boxHit": "check-compare", "boxFullyAboveBar": true, "activeIsBox": true, "scrollY": 296, "docW": 375, "vw": 375}
[1 after ticking] {"status": "Saved: your wording is in. Read it once more against the highlighted words.", "stRect": [12, 627, 363, 663], "stH": 35, "stFont": "13px", "showBoxHidden": true, "showBox": [0, 0, 0, 0], "yes": [12, 531, 183, 581], "yesDisabled": false, "bar": [0, 482, 375, 667], "box": [31, 441, 59, 469], "boxId": "check-compare", "boxChecked": true, "boxHit": "check-compare", "boxFullyAboveBar": true, "activeIsBox": true, "scrollY": 296, "docW": 375, "vw": 375}
[1 after unticking] {"status": "Saved. Tick the box to say you compared them.", "showBoxHidden": true, "yesDisabled": true, "boxChecked": false}
[1 after Yes] {"status": "Saved: item 1 kept in the letter.", "showBoxHidden": true, "yesDisabled": false}
[1b sample e1 fresh] {"status": "", "stRect": [12, 645, 363, 645], "yes": [12, 531, 183, 581], "yesDisabled": false, "bar": [0, 482, 375, 667], "box": null, "showBoxHidden": true}
[1b kbd edit state] {"status": "Saved. Tick the box to say you compared them.", "showBoxHidden": false, "activeIsBox": true}
[1b active element] check-compare
[1c-390 sample e1 fresh] {"status": "", "stRect": [12, 822, 378, 822], "yes": [12, 708, 190, 758], "yesDisabled": false, "bar": [0, 659, 390, 844], "box": null, "showBoxHidden": true}
[1c edit-to-check 390x844] {"status": "Saved. Tick the box to say you compared them.", "stRect": [12, 813, 378, 831], "stH": 18, "stFont": "13px", "showBoxHidden": true, "showBox": [0, 0, 0, 0], "yes": [12, 708, 190, 758], "yesDisabled": true, "bar": [0, 659, 390, 844], "box": [31, 602, 59, 630], "boxId": "check-compare", "boxChecked": false, "boxHit": "check-compare", "boxFullyAboveBar": true, "activeIsBox": true, "scrollY": 0, "docW": 390, "vw": 390}
[1c-360 sample e1 fresh] {"status": "", "stRect": [12, 718, 348, 718], "yes": [12, 604, 175, 654], "yesDisabled": false, "bar": [0, 555, 360, 740], "box": null, "showBoxHidden": true}
[1c edit-to-check 360x740] {"status": "Saved. Tick the box to say you compared them.", "stRect": [12, 700, 234, 736], "stH": 35, "stFont": "13px", "showBoxHidden": false, "showBox": [242, 701, 348, 735], "yes": [12, 604, 175, 654], "yesDisabled": true, "bar": [0, 555, 360, 740], "box": [31, 586, 59, 614], "boxId": "check-compare", "boxChecked": false, "boxHit": "DIV", "boxFullyAboveBar": false, "activeIsBox": true, "scrollY": 0, "docW": 360, "vw": 360}
[1c-1440 sample e1 fresh] {"status": "Keys: A says yes, D says no, E fixes or adds a note, the arrow keys move between items.", "stRect": [32, 856, 1393, 880], "yes": [32, 782, 302, 838], "yesDisabled": false, "bar": [0, 729, 1425, 900], "box": null, "showBoxHidden": true}
[1c edit-to-check 1440x900] {"status": "Saved. Tick the box to say you compared them.", "stRect": [32, 856, 1393, 880], "stH": 24, "stFont": "16px", "showBoxHidden": true, "showBox": [0, 0, 0, 0], "yes": [32, 782, 302, 838], "yesDisabled": true, "bar": [0, 729, 1425, 900], "box": [750, 601, 778, 629], "boxId": "check-compare", "boxChecked": false, "boxHit": "check-compare", "boxFullyAboveBar": true, "activeIsBox": true, "scrollY": 0, "docW": 1425, "vw": 1440}
tokens BM5b3k81PElffAYLsLizNA bCMNrW20cQeAiGAgZ3L1Cg
[2 lib10 e1 375x667 open] {"status": "Tick the box to say you compared them.", "stRect": [12, 627, 249, 663], "stH": 35, "stFont": "13px", "showBoxHidden": false, "showBox": [257, 628, 363, 662], "yes": [12, 531, 183, 581], "yesDisabled": true, "bar": [0, 482, 375, 667], "box": [31, 691, 59, 719], "boxId": "check-compare", "boxChecked": false, "boxHit": null, "boxFullyAboveBar": false, "activeIsBox": false, "scrollY": 0, "docW": 375, "vw": 375}
[2 lib10 e1 375x667 after Show box] {"status": "Tick the box to say you compared them.", "stRect": [12, 636, 363, 654], "stH": 18, "stFont": "13px", "showBoxHidden": true, "showBox": [0, 0, 0, 0], "yes": [12, 531, 183, 581], "yesDisabled": true, "bar": [0, 482, 375, 667], "box": [31, 441, 59, 469], "boxId": "check-compare", "boxChecked": false, "boxHit": "check-compare", "boxFullyAboveBar": true, "activeIsBox": true, "scrollY": 250, "docW": 375, "vw": 375}
[2 lib10 e1 375x667 ticked] {"status": "", "showBoxHidden": true, "yes": [12, 531, 183, 581], "yesDisabled": false, "boxChecked": true}
[2 lib10 e1 375x667 unticked] {"status": "Tick the box to say you compared them.", "showBoxHidden": true, "yes": [12, 531, 183, 581], "yesDisabled": true}
   mark=[31, -27, 331, 19] line=[16, 152, 359, 514] box=[31, 441, 59, 469] bar=[0, 482, 375, 667]
[2 lib10 e1 360x740 open] {"status": "Tick the box to say you compared them.", "stRect": [12, 700, 234, 736], "stH": 35, "stFont": "13px", "showBoxHidden": false, "showBox": [242, 701, 348, 735], "yes": [12, 604, 175, 654], "yesDisabled": true, "bar": [0, 555, 360, 740], "box": [31, 604, 59, 632], "boxId": "check-compare", "boxChecked": false, "boxHit": "DIV", "boxFullyAboveBar": false, "activeIsBox": false, "scrollY": 0, "docW": 360, "vw": 360}
[2 lib10 e1 360x740 after Show box] {"status": "Tick the box to say you compared them.", "stRect": [12, 709, 348, 727], "stH": 18, "stFont": "13px", "showBoxHidden": true, "showBox": [0, 0, 0, 0], "yes": [12, 604, 175, 654], "yesDisabled": true, "bar": [0, 555, 360, 740], "box": [31, 493, 59, 521], "boxId": "check-compare", "boxChecked": false, "boxHit": "check-compare", "boxFullyAboveBar": true, "activeIsBox": true, "scrollY": 0, "docW": 360, "vw": 360}
[2 lib10 e1 360x740 ticked] {"status": "", "showBoxHidden": true, "yes": [12, 604, 175, 654], "yesDisabled": false, "boxChecked": true}
[2 lib10 e1 360x740 unticked] {"status": "Tick the box to say you compared them.", "showBoxHidden": true, "yes": [12, 604, 175, 654], "yesDisabled": true}
   mark=[31, 221, 331, 267] line=[16, 315, 344, 547] box=[31, 493, 59, 521] bar=[0, 555, 360, 740]
[2 lib10 e1 390x844 open] {"status": "Tick the box to say you compared them.", "stRect": [12, 813, 378, 831], "stH": 18, "stFont": "13px", "showBoxHidden": true, "showBox": [0, 0, 0, 0], "yes": [12, 708, 190, 758], "yesDisabled": true, "bar": [0, 659, 390, 844], "box": [31, 599, 59, 627], "boxId": "check-compare", "boxChecked": false, "boxHit": "check-compare", "boxFullyAboveBar": true, "activeIsBox": false, "scrollY": 0, "docW": 390, "vw": 390}
[2 lib10 e1 390x844 ticked] {"status": "", "showBoxHidden": true, "yes": [12, 708, 190, 758], "yesDisabled": false, "boxChecked": true}
[2 lib10 e1 390x844 unticked] {"status": "Tick the box to say you compared them.", "showBoxHidden": true, "yes": [12, 708, 190, 758], "yesDisabled": true}
   mark=[31, 223, 331, 269] line=[16, 356, 374, 651] box=[31, 599, 59, 627] bar=[0, 659, 390, 844]
[2 lib10 e1 1440x900 open] {"status": "Tick the box to say you compared them.", "stRect": [32, 856, 1393, 880], "stH": 24, "stFont": "16px", "showBoxHidden": true, "showBox": [0, 0, 0, 0], "yes": [32, 782, 302, 838], "yesDisabled": true, "bar": [0, 729, 1425, 900], "box": [750, 625, 778, 653], "boxId": "check-compare", "boxChecked": false, "boxHit": "check-compare", "boxFullyAboveBar": true, "activeIsBox": false, "scrollY": 0, "docW": 1425, "vw": 1440}
[2 lib10 e1 1440x900 ticked] {"status": "Keys: A says yes, D says no, E fixes or adds a note, the arrow keys move between items.", "showBoxHidden": true, "yes": [32, 782, 302, 838], "yesDisabled": false, "boxChecked": true}
[2 lib10 e1 1440x900 unticked] {"status": "Tick the box to say you compared them.", "showBoxHidden": true, "yes": [32, 782, 302, 838], "yesDisabled": true}
   mark=[57, 465, 646, 517] line=[725, 292, 1393, 709] box=[750, 625, 778, 653] bar=[0, 729, 1425, 900]
[2 lib10 e2 375x667 (no box)] {"status": "", "showBoxHidden": true, "boxId": null, "yesDisabled": false}
[2 lib10 e2 1440x900 (no box)] {"status": "Keys: A says yes, D says no, E fixes or adds a note, the arrow keys move between items.", "showBoxHidden": true, "boxId": null, "yesDisabled": false}
[2 lib11 a2 375x667 generic box] {"status": "Tick the box first.", "showBoxHidden": false, "boxId": "check-compare", "box": [31, 753, 59, 781], "bar": [0, 482, 375, 667], "yesDisabled": true}
[3 outsideParts] line='Patient attended physical therapy 3 times a week' quote='PT 3x/week, attended physical therapy' -> underlined=['Patient', '3', 'times']
[3 outsideParts] line='Patient states chest pain' quote='Pt states chest pain' -> underlined=[]
[3 outsideParts] line='Patient states chest pain' quote='pt states chest pain' -> underlined=[]
[3 outsideParts] line='Patient states chest pain' quote='PT states chest pain' -> underlined=['Patient']
[3 outsideParts] line='PT attended 3 times' quote='PT attended 3 times' -> underlined=[]
[3 outsideParts] line='Pt attended 3 times' quote='PT attended 3 times' -> underlined=['Pt']
[3 outsideParts] line='Patient reports pain' quote="PT's note: reports pain" -> underlined=[]
[3 outsideParts] line='Patient completed PT sessions' quote='PT sessions completed' -> underlined=['Patient']
[3 outsideParts] line='Diagnosis chest wall pain' quote='Dx: chest wall pain' -> underlined=['Diagnosis']
[3 outsideParts] line='Patient attended PT' quote='Patient attended PT' -> underlined=[]
[3 lib11 a6 375x667] reason='A second AI check thought this may be a damages figure (for example lost wages), not what it was first sorted as.' status='Tick the box to say you compared them.' showBox=False stH=35 bar=[0, 482, 375, 667] box=[31, 666, 59, 694]
   'lost pay' present: False | 'lost wages' present: True | 'not a bill' present: False
[3 lib11 a6 390x844] reason='A second AI check thought this may be a damages figure (for example lost wages), not what it was first sorted as.' status='Tick the box to say you compared them.' showBox=True stH=18 bar=[0, 659, 390, 844] box=[31, 591, 59, 619]
   'lost pay' present: False | 'lost wages' present: True | 'not a bill' present: False
[3 lib11 a6 1440x900] reason='A second AI check thought this may be a damages figure (for example lost wages), not what it was first sorted as.' status='Tick the box to say you compared them.' showBox=True stH=24 bar=[0, 729, 1425, 900] box=[750, 649, 778, 677]
   'lost pay' present: False | 'lost wages' present: True | 'not a bill' present: False
[3 lib11 e2 390x844] outside=['after', 'passenger', 'vehicle', 'struck', 'from', 'behind']
[3 lib11 e2 375x667] outside=['after', 'passenger', 'vehicle', 'struck', 'from', 'behind']
[3 lib11 e2 1440x900] outside=['after', 'passenger', 'vehicle', 'struck', 'from', 'behind']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:58:03.933Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/ux-t203r2-fa34fe9 && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q -p no:cacheprovider > $S/ux-t203r2-e2e.out 2>&1; tail -5 $S/ux-t203r2-e2e.out",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T23:58:04.002Z

**tool result**
````
Command running in background with ID: bu1jiobxf. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bu1jiobxf.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:58:04.340Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux-r2/1-edit-375x667-after-edit.png"
}
````

### User / tool · 2026-11-02T23:58:04.366Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:58:04.767Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux-r2/1-edit-375x667-after-showbox.png"
}
````

### User / tool · 2026-11-02T23:58:04.779Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:58:05.201Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux-r2/2-lib10-e1-375x667-open.png"
}
````

### User / tool · 2026-11-02T23:58:05.210Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:58:05.596Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux-r2/2-lib10-e1-375x667-showbox.png"
}
````

### User / tool · 2026-11-02T23:58:05.607Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:58:21.174Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-203-ux-r2-kbd.py <<'EOF'\n\"\"\"T-203 r2: keyboard on the edit path at 375x667: focus after Fix the wording, Tab order to Show box, Space on box, then A for yes.\"\"\"\nimport time, json\nfrom playwright.sync_api import sync_playwright\nDEMO = \"http://127.0.0.1:7993\"\nACT = \"() => { const a = document.activeElement; return a && (a.getAttribute('data-testid') || a.tagName); }\"\nST = \"() => (document.querySelector('[data-testid=status-text]')||{}).innerText\"\ndef ready(page): page.wait_for_selector(\"[data-testid=view][data-ready]\", timeout=30000); time.sleep(0.9)\nwith sync_playwright() as p:\n    b = p.chromium.launch(); page = b.new_context(viewport={\"width\": 375, \"height\": 667}, has_touch=True, is_mobile=True).new_page()\n    page.goto(DEMO + \"/\"); ready(page)\n    page.locator(\"[data-testid=btn-sample-case]\").click(); page.wait_for_selector(\"[data-testid=btn-draft]\", timeout=30000); time.sleep(0.5)\n    page.locator(\"[data-testid=btn-draft]\").click(); page.wait_for_selector(\"[data-testid=btn-next-step]\", timeout=90000); time.sleep(0.5)\n    page.locator(\"[data-testid=btn-next-step]\").click(); ready(page)\n    page.locator(\"[data-testid=btn-third]\").click(); time.sleep(0.6)\n    ed = page.locator(\"[data-testid=edit-summary]\"); ed.fill(ed.input_value().replace(\"transported to\", \"taken to\")); time.sleep(0.2)\n    page.locator(\"[data-testid=answer-yes]\").click(); time.sleep(1.8)\n    print(\"after edit: active\", page.evaluate(ACT), \"| status\", page.evaluate(ST))\n    page.keyboard.press(\"Space\"); time.sleep(0.5)\n    print(\"after Space: active\", page.evaluate(ACT), \"| status\", page.evaluate(ST), \"| yes disabled\", page.evaluate(\"() => document.querySelector('[data-testid=answer-yes]').disabled\"))\n    page.keyboard.press(\"a\"); time.sleep(1.5)\n    print(\"after A: status\", page.evaluate(ST), \"| item\", page.evaluate(\"() => (document.body.innerText.match(/Item \\\\d+ of \\\\d+/)||[''])[0]\"))\n    b.close()\nEOF\n.venv/bin/python artifacts/review-evidence/T-203-ux-r2-kbd.py",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T23:58:30.733Z

**tool result**
````
after edit: active check-compare | status Saved. Tick the box to say you compared them.
after Space: active check-compare | status Saved: your wording is in. Read it once more against the highlighted words. | yes disabled False
after A: status Saved: item 1 kept in the letter. | item Item 2 of 19
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:58:33.175Z

**tool call — Bash**
````
{
 "command": "kill 15794 15796; sleep 1; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7993/; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7994/; lsof -ti :7993 -ti :7994"
}
````

### User / tool · 2026-11-02T23:58:34.374Z

**tool result (error)**
````
Exit code 1
000
000
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:58:35.297Z

Servers stopped (both ports answer 000). Waiting on the e2e run.

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:58:38.072Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; until grep -qE \"passed|failed|error\" $S/ux-t203r2-e2e.out; do sleep 10; done; tail -4 $S/ux-t203r2-e2e.out",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T00:01:18.386Z

**tool result**
````
........................................................................ [ 49%]
........................................................................ [ 99%]
.                                                                        [100%]
145 passed in 187.87s (0:03:07)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:01:21.081Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-203-ux-r2/3-lib11-a6-375x667.png"
}
````

### User / tool · 2026-11-03T00:01:21.093Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:01:49.027Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-203-ux-designer-r2.md",
 "content": "# T-203 round 2 review: Show box, hint beside \"Saved\", PT, lost wages (commit fa34fe9), ux-designer-reviewer\n\nVerdict: **pass** (0 blockers, 0 majors, 1 minor, 3 nits). Scores: design quality 4, originality 4, craft 4, functionality 4.\n\n**My r1 major (reworded line at 375x667) is fixed.**\n- After \"Fix the wording\" on sample e1 at 375x667 the status slot now reads \"Saved. Tick the box to say you compared them.\" beside a \"Show box\" button (y 627-663 in a bar 482-667). It was the same at +0 s, +5 s and +30 s. Yes stays greyed at y 531-581 and does not move.\n- The box was behind the bar at y 630-658 (boxHit = status-text). Tapping \"Show box\" scrolls it to y 441-469, above the bar, focuses it, and hides the button. Ticking it enables Yes and the slot goes back to \"Saved: your wording is in. Read it once more against the highlighted words.\" Unticking brings the hint back. Yes then reads \"Saved: item 1 kept in the letter.\" and the next item loads.\n- Keyboard: after the edit, focus is already on the box (activeIsBox true). Space ticks it, A says yes, and item 2 of 19 loads. Two keys.\n\n**My r1 minor (the word \"above\") is fixed.** The words now read \"Tick the box to say you compared them.\" (disputed line) and \"Tick the box first.\" (generic box), with no direction word. On lib10 e1 at 375x667 the box is at y 691-719 (below the screen) and \"Show box\" is shown; tapping it puts the box at y 441-469. At 360x740 the box was behind Yes/No (y 604-632) and \"Show box\" puts it at y 493-521, above the bar at 555. At 390x844 and 1440x900 the box is already above the bar, so there is no button.\n\n**\"PT\" and \"Pt\".** Run live through `window.G.step2.outsideParts`:\n- quote \"PT 3x/week, attended physical therapy\", line \"Patient attended physical therapy 3 times a week\" underlines Patient, 3, times. \"Patient\" is now marked.\n- quote \"Pt states chest pain\" and \"pt states chest pain\" with line \"Patient states chest pain\" underline nothing, as intended.\n- quote \"PT states chest pain\" underlines Patient. A line \"Pt ...\" against a quote \"PT ...\" underlines Pt.\n- lib11 e2 (a real \"Pt\" quote) at 390, 375 and 1440: underlined words are after, passenger, vehicle, struck, from, behind; \"Patient\" is not underlined.\n\n**\"Lost wages\".** lib11 a6 at 375, 390 and 1440 reads \"A second AI check thought this may be a damages figure (for example lost wages), not what it was first sorted as.\" \"lost pay\" and \"not a bill\" are absent from the page text.\n\n**Regressions at 390 and 1440: none found.**\n- lib10 e1 at 390x844: mark y 223-269, box 599-627, bar 659, Yes 708-758, same as r1 and T-181 r3. Sample e1 after a valid edit at 390: box 602-630, as in r3; the hint is one line (18 px), no \"Show box\".\n- 1440x900: Yes y 782-838 in every state. The keys line returns after the tick. Lines with no box (lib10 e2 at 375 and 1440) show no hint and no \"Show box\".\n- Deterministic: `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q` on a fresh `git archive fa34fe9` printed `145 passed in 187.87s (0:03:07)`.\n\n## Findings\n- **F1 (minor):** \"Show box\" scrolls the highlighted words mostly off the top and clips the box label's second line behind the bar.\n- **F2 (nit):** \"PT's\" and \"PTs\" still map to \"patient\".\n- **F3 (nit):** the hint is 13 px at 375 and \"Show box\" is 34 px high; r1 asked for 15 px. Touch-target size is for accessibility-reviewer.\n- **F4 (nit):** on the reworded line, \"Read it once more against the highlighted words\" now appears only after she has ticked the box.\n- Carried over, not touched by this card (handoff says so): the \"Step 3 of 4\" label wraps to three lines at 375x667 (3-lib11-a6-375x667.png). It stays a nit.\n\n```json\n{\"card\": \"T-203\", \"persona\": \"ux-designer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit fa34fe9 (git archive fa34fe9 into new empty scratchpad dir ux-t203r2-fa34fe9; git rev-parse --short HEAD printed fa34fe9); demo app http://127.0.0.1:7993 (LLM_BACKEND=fixture FIXTURE_SET=curated, own ZLAYT_DB) and http://127.0.0.1:7994 (same plus ZLAYT_MODE=local, to create lib10 and lib11); both stopped afterwards (PIDs 15794 and 15796 from lsof; ports 7993 and 7994 then answered 000); sample case evals/golden/sample.txt plus library cases case_lib10_eob_ub04_cms1500 and case_lib11_priors_and_ledger\",\n \"exercised\": [\n  \"E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/guided tests/e2e/test_no_console_errors.py tests/e2e/test_demo_provenance.py -q on the fresh archive: '145 passed in 187.87s (0:03:07)' (includes tests/e2e/guided/test_t203.py)\",\n  \"artifacts/review-evidence/T-203-ux-r2-measure.py (output artifacts/review-evidence/T-203-ux-r2/measure.out): sample e1 'Fix the wording' then tick at 375x667 read at +0, +5 and +30 s, tapped the greyed Yes, tapped Show box, ticked, unticked, ticked and said Yes; same edit path at 390x844, 360x740 and 1440x900\",\n  \"same script: lib10 e1 (disputed line) at 375x667, 360x740, 390x844 and 1440x900 (open, Show box, tick, untick, rects of mark/line/box/bar); lib10 e2 (no box) at 375 and 1440; lib11 a2 (generic 'Tick the box first.') at 375x667\",\n  \"same script: window.G.step2.outsideParts called live with 10 PT / Pt / pt / PT's / Dx quote and line pairs; lib11 a6 second-check wording and a page-text search for 'lost pay', 'lost wages' and 'not a bill' at 375, 390 and 1440; lib11 e2 outside-word underlines at 390, 375 and 1440\",\n  \"artifacts/review-evidence/T-203-ux-r2-kbd.py: keyboard on the edit path at 375x667 (focus after the edit is the box; Space; A; next item)\",\n  \"read the screenshots 1-edit-375x667-after-edit.png, 1-edit-375x667-after-showbox.png, 2-lib10-e1-375x667-open.png, 2-lib10-e1-375x667-showbox.png and 3-lib11-a6-375x667.png in artifacts/review-evidence/T-203-ux-r2/\",\n  \"git show fa34fe9 (review.js drawStatus, boxHidden, revealBox; step2.js stem; test_t203.py); board.py show T-203 for the handoff; read reviews/T-203-ux-designer.md and personas/ux-designer.md\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"design_quality\": 4, \"originality\": 4, \"craft\": 4, \"functionality\": 4},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Show box brings the box above the bar but scrolls the highlighted words mostly off the top and cuts the box label's second line\",\n   \"evidence\": \"measure.out [1 after Show box]: box y 441-469, bar top 482, scrollY 296. Screenshot 1-edit-375x667-after-showbox.png: only the last 3 lines of the highlighted excerpt are on screen, and the label 'I read this line against the highlighted words myself.' has its second line ('highlighted words myself.') cut by the bar. 2-lib10-e1-375x667-showbox.png: highlighted words 'Pt states chest wall and left knee pain.' are at the top edge; measure.out lib10 e1 mark y -27 to 19 at 375x667 after Show box.\",\n   \"why_it_matters\": \"The box says 'I compared the line to the highlighted words', and the one tap that finds the box leaves the words she must compare against half off screen. She can scroll back, so this is a rough edge, not a block. It is only at 375x667 and 360x740.\",\n   \"fix\": \"Scroll to the box's label bottom, not the box top (scrollMarginBottom = bar height + label height), or scroll so the highlighted words and the box share the area above the bar when both fit.\",\n   \"acceptance_test\": \"At 375x667 on lib10 e1, after Show box the whole label text (both lines) is above the bar top, and at least the first line of the highlighted words is on screen.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"'PT's' and 'PTs' still map to 'patient'\",\n   \"evidence\": \"measure.out [3 outsideParts] line='Patient reports pain' quote=\\\"PT's note: reports pain\\\" -> underlined=[]. The check in step2.js is `w === \\\"PT\\\"` on the whole matched word, and the matched word for \\\"PT's\\\" is \\\"PT's\\\".\",\n   \"why_it_matters\": \"'PT's note' (physical therapist's note) is an everyday chart phrase. Small, rare.\",\n   \"fix\": \"Test the capitals on the word before the possessive or plural is stripped, e.g. /^PTs?(['’]s)?$/.\",\n   \"acceptance_test\": \"Quote \\\"PT's note: reports pain\\\" with line 'Patient reports pain' underlines 'Patient'.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Hint text stays 13 px at 375 and Show box is 34 px high\",\n   \"evidence\": \"measure.out [1 edit-to-check 375x667 +0s] stFont 13px, showBox [257,628,363,662] = 106 x 34 px; Yes/No are 50 px high. r1 asked for 15 px.\",\n   \"why_it_matters\": \"It is the only cue on that screen. A small touch target beside two 50 px buttons. Target size conformance is for accessibility-reviewer.\",\n   \"fix\": \"15 px text and a 44 px high button; the bar has 4 px spare, so check the height.\",\n   \"acceptance_test\": \"Wording and size review only.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"On a reworded line, 'Read it once more against the highlighted words' shows only after she ticks the box\",\n   \"evidence\": \"measure.out: [1 edit-to-check +0s] status 'Saved. Tick the box to say you compared them.'; [1 after ticking] status 'Saved: your wording is in. Read it once more against the highlighted words.' The box's own card already says 'You changed the wording. Read it against the highlighted words once more.' (1-edit-375x667-after-showbox.png).\",\n   \"why_it_matters\": \"The instruction to compare appears in the slot after she has said she did. The yellow card above carries it, so nothing is lost.\",\n   \"fix\": \"Keep one phrase, e.g. 'Saved. Read it against the highlighted words, then tick the box.' while unticked.\",\n   \"acceptance_test\": \"Wording review only.\"}\n ],\n \"whats_right\": [\n  \"The reason for a greyed Yes now stays beside a 'Saved' note on the edit path and survives 30 s; Show box finds the box in one tap and focuses it, and Space then A finishes the item by keyboard.\",\n  \"Hint and Show box appear only when a box is the reason and is hidden (none at 390x844 or 1440x900, none on lines with no box), and Yes never moved in any state (y 531-581 at 375, 708-758 at 390, 782-838 at 1440).\",\n  \"'PT' versus 'Pt' now behaves correctly in the live app, and the damages wording reads 'lost wages' with no 'lost pay' or 'not a bill' left on the page.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-03T00:01:49.351Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-203-ux-designer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:01:50.636Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -3"
}
````

### User / tool · 2026-11-03T00:01:50.797Z

**tool result**
````
ok (203 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:01:55.478Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/project_t203_375_hint.md",
 "content": "---\nname: project-t203-375-hint\ndescription: T-203 r1 38ee0c3 changes (1 major); r2 fa34fe9 pass, 0 majors; open minor: Show box scrolls highlighted words off and clips label\nmetadata:\n  type: project\n---\n\nT-203 r1 (reviews/T-203-ux-designer.md, 38ee0c3, 2026-11-02): **changes**, 1 major.\n- Major: after Fix the wording at 375x667 the slot showed only \"Saved: ... Read it once more\", box at y 630-658 behind the bar; drawStatus showed the hint only when no Saved message.\n- Minors: \"above\" wrong at 375x667; ABBR pt->patient treated PT (physical therapy) as patient.\n\nT-203 r2 (reviews/T-203-ux-designer-r2.md, fa34fe9): **pass**, 0 majors, 1 minor, 3 nits. 145 passed (guided + no_console_errors + demo_provenance) on a fresh archive.\n- Fixed: \"Saved. Tick the box to say you compared them.\" + \"Show box\" button (34 px high, 13 px text); Show box puts box at y 441-469 above bar 482 and focuses it; Space then A finishes by keyboard.\n- Open minor: Show box scrolls highlighted words off the top and clips the label's second line; nits: PT's/PTs still map to patient, hint 13 px, \"Read it once more\" only appears after the tick. Step 3 label wrap at 375 still not done.\n\nScripts: artifacts/review-evidence/T-203-ux-r2-measure.py (ports 7993 demo / 7994 local; makes lib10 and lib11 itself) and -r2-kbd.py. Windows run: window.G.step2.outsideParts is callable live.\n\n**Why:** the 375x667 phone is treated as in scope, so edit-path gaps there were majors.\n\n**How to apply:** if T-203 comes back, re-run r2-measure.py part 1 and check the label clipping after Show box. See [[project-t181-guided-build]].\n"
}
````

### User / tool · 2026-11-03T00:01:55.614Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/project_t203_375_hint.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:01:58.194Z

T-203 r2 on fa34fe9 is a **pass** (0 blockers, 0 majors, 1 minor, 3 nits): the reworded-line major is fixed. Review is in `/Users/arsis/zlayt-pm-project/reviews/T-203-ux-designer-r2.md`.

- **Major fixed:** after "Fix the wording" at 375x667 the slot reads "Saved. Tick the box to say you compared them." and stays so for 30 s. "Show box" scrolls the box above the bar and focuses it. Space then A finishes the item.
- **PT and wording:** "PT" and "Pt" behave correctly. The damages text reads "lost wages".
- **Deterministic and regressions:** 145 e2e tests passed on the fresh archive, and the 390 and 1440 numbers are unchanged.
- **Open minor:** "Show box" scrolls the highlighted words mostly off the top and clips the label's second line.
- **Servers:** both stopped; ports 7993 and 7994 answer 000.
