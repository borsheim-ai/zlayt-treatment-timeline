# GATE M3+M4 combined panel: UX designer (Priya Raman)

Pinned commit f6d5c19, extracted with `git archive f6d5c19` into a new empty directory and served in demo mode (`LLM_BACKEND=fixture FIXTURE_SET=curated`, port 7891). I stopped it afterwards: the listener PID was 52544, not the nohup PID, and `curl` to the port returned 000 after `kill 52544`. Rules applied: D-075 (blockers only), D-074, and Chris's D-068 bar ("grandma can use it"). Evidence is in `artifacts/review-evidence/GATE-M3M4-ux/`.

**Verdict: pass. 0 blockers, 0 majors, 5 minors.** Per D-075 the minors go to SCOPE_CUTS as accepted debt; none needs a fix round.

## What I walked
A first-time user at 1440x900 and 390x844, in a fresh browser context each time: Your cases, Open the sample case, Step 1 (records, Draft the timeline), Step 2 (19 items), Step 3 (4 amounts), Step 4 (letter). I answered Yes to every item. The phone walk and the desktop walk both reached the letter with no console errors, no page errors and no horizontal scroll.

I also checked: Start a new case (the demo refuses own text plainly and points to the sample, so it is not a dead end), Your cases with a started case (Continue button and step progress), Back then re-reading the You row after Yes and after No, the How page, and the letter page text.

## T-211: "How this was checked" is visible and true
For all 23 items (19 timeline items plus 4 amounts) the panel shows the three rows: Code check (tagged "no AI"), Second AI check, and You. I compared each row with the item trace from `/api/cases/<token>/items/e1/trace`.
- e1: code row "Passed ... All 8 checks" matches 8 passing code steps. The second AI row says "Agrees" with model `claude-haiku-5-5`. The trace's `recorded_from` is a `claude-cli` run on `claude-haiku-5-5`, so the model name is true.
- The You row changes: "Waiting for you." becomes "You kept it in the letter." after Yes, and "You left it out of the letter." after No, including when I go Back to the item.
- f_r7_1, which was my T-211 r1 blocker, is fixed. The row now reads "Not run. Only the phrase list found this warning, so there is no prepared answer to double-check; it stays marked for review." There is no false "second AI then checked it" lead.
- "Not needed" appears only for gaps and dates, and for non-bill figures (the missed-work amount). Each states a true reason ("arithmetic over dates ... which code does exactly").
- The panel is open by default on desktop. On a phone it sits inside the action bar as a one-line strip of chips ("Code: passed", "AI: agrees", "You: waiting"), which is always on screen.

**"How each answer is checked" page.** It is reachable from the header on every screen, including the letter, at both sizes (at 390 the link reads "How it's checked"). It has four plain numbered steps, then the picture, a code-versus-AI list, and the repo pointers. Its claims match what the panel shows. At 390 the first screen is the heading and steps 1 to 3 at a readable size. I found nothing false or hidden.

**"Found by code" label.** It is true. I read `origin` and `origin_label` from the case payload: the gap, accident-date and PT-plan conflict flags are `origin: code`, and f_r7_1 is `origin: lexicon` with the label "Found by code (phrase list)". The six flags where a prepared answer also exists carry no label. The label is shown on the chip and again in the Code row.

## Letter date blanks
The letter prints `date of service [__________] (record dated January 9, 2026)` on each charge line.
- **Step 3 on desktop is clear.** An amber box says "What to do: find the date of service in the record ... then write it in the blank" and that the date in parentheses is the record date. The notes for the attorney repeat it under "CHARGES WITHOUT A CERTAIN DATE OF SERVICE".
- **Step 4 is not clear.** See M1.

## Findings (all minor)
M1 is the one the brief asked about. The rest are small.

```json
{"card": "GATE-M3M4", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive f6d5c19 in a fresh dir, demo mode (fixture, curated) on port 7891; sample case; 1440x900 and 390x844; guided flow Your cases, sample, Steps 1-4, letter, How page; rules D-075, D-074, D-068",
 "exercised": [
  "git archive f6d5c19 into a new empty scratch dir; started app.main with LLM_BACKEND=fixture FIXTURE_SET=curated on 127.0.0.1:7891; stopped listener PID 52544; curl then returned 000",
  "artifacts/review-evidence/GATE-M3M4-ux/walk.py: full first-time walk at 1440x900 and at 390x844 (mobile, touch): home, Open the sample case, Draft the timeline, all 19 Step 2 items, all 4 Step 3 items, letter; read the How panel of every item",
  "items.py: screenshots of e1, f_r7_1, f_cx1, f_gap_r6_r7, a2, a3 at both sizes; How page at both sizes; link-how visible from a step and from the letter",
  "open390.py and a1_390.py / a1_390b.py: How panel opened at 390, and where the Step 3 date-blank instruction sits on a phone",
  "letter_probe.py: letter and notes text, bar message, letter at both sizes (all items accepted via the API as a shortcut)",
  "newcase.py: Start a new case in demo mode (own text refused plainly; the sample path still works); home2.py: Your cases with a started case; youstate.py: You row after Yes, Back, No",
  "API: GET /api/cases/<token>/items/e1/trace (judge evidence: model id and recorded_from); GET /api/cases/<token> flag origin and origin_label for all 10 flags",
  "Read app/frontend/guided/{how,review,step4}.js, app/backend/present.py:310-320, flags.py:233,286 (origins), memory/ORCHESTRATOR_DECISIONS.md D-065/D-068/D-074/D-075"],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 4, "craft": 4, "functionality": 5},
 "findings": [
  {"severity": "minor", "title": "M1: Step 4 says the letter is ready and names only the Ex/Bates blanks; the date-of-service blanks are not mentioned there, and on a phone the Step 3 instruction is hidden inside a scrolling card",
   "evidence": "1440x900-08-letter.png and 390x844-08-letter.png: status 'Your letter is ready. Every item has an answer.' and bar message 'Copy this into your demand letter. The [Ex. __ / Bates __] blanks are yours to fill in.' The letter text below has two lines 'date of service [__________] (record dated ...)'. step4.js:91 builds the blanks sentence from /\\[Ex\\. __|Bates __/ only. 390x844-a1-closed.png and 390x844-a1-scrolled.png: the amber 'What to do' box is below the first screen of the charge card (card-line scrolls inside the card; no cue). 1440x900-s3-20-item.png shows it clear on desktop. The instruction is also in the notes under CHARGES WITHOUT A CERTAIN DATE OF SERVICE (letter_probe output).",
   "why_it_matters": "A user who skips the Step 3 box, or never scrolls the phone card, sees 'ready' and copies a letter with unfilled dates, believing only Ex/Bates remain. Filed minor, not blocker: the text is not false (the blank is visible in the pasted text and explained on desktop and in the notes) and the flow finishes. It would be a major under the dossier; filed per D-075 and for the orchestrator to put in SCOPE_CUTS.",
   "fix": "In step4.js, extend `blanks` and the bar sentence: 'The [Ex. __ / Bates __] blanks and each \"date of service [____]\" blank are yours to fill in.' On a phone, show a one-line 'Fill in the date of service blank' reminder in the status box when the letter has one.",
   "acceptance_test": "Letter page with a charge accepted: the bar message mentions 'date of service'; Playwright at 390x844 asserts the same words are visible without scrolling the letter pane."},
  {"severity": "minor", "title": "M2: f_r7_1 Code row reads 'Did not pass' (red, chip 'Code: not passed') for a warning code itself found",
   "evidence": "1440x900-item-f_r7_1.png and 390x844-item-f_r7_1.png: 'Did not pass: The phrase list found this warning but the prepared answers did not; check that it applies. ... Found by code (phrase list).' next to 'Second AI check: Not run'. Walk data: 1440x900-walk.json item f_r7_1.",
   "why_it_matters": "True and actionable, but 'code did not pass' plus 'found by code' reads as a contradiction to a first-time user. It does not claim anything false.",
   "fix": "For a phrase-list-only flag, show 'Needs your check' on the Code row instead of 'Did not pass', and a neutral chip.",
   "acceptance_test": "f_r7_1 trace row and chip contain no 'not passed' wording."},
  {"severity": "minor", "title": "M3: on a phone the opened How panel covers most of the line card, and the open state persists across items",
   "evidence": "390x844-open-f_cx1.png, 390x844-open-a2.png, 390x844-s3-20-item.png: with the panel open only the tag of the line card shows above it. Panel top y 623, Yes button top y 708, viewport 844.",
   "why_it_matters": "She can close it, so no dead end, but after one open she may think the item has no text.",
   "fix": "Close the panel when the item changes on a phone, or cap its height.",
   "acceptance_test": "At 390x844 the line card's first line stays visible after the panel is opened."},
  {"severity": "minor", "title": "M4: 'Found by code' is explained only in a hover tooltip",
   "evidence": "review.js:66 title 'Found by a program, not drafted by an AI.' (title attribute; not shown on touch). The Code row repeats 'Found by code.' with no explanation.",
   "why_it_matters": "'Code' is the one remaining developer word on a chip a grandma sees. The How page does explain code versus AI, but not from the chip.",
   "fix": "Say 'Found by a program' on the chip, or link the chip to the How page.",
   "acceptance_test": "Chip text or an on-screen sentence explains it without hover."},
  {"severity": "minor", "title": "M5: the demo never says the second AI verdicts were recorded earlier and are replayed",
   "evidence": "Trace for e1: judge evidence backend 'fixture', recorded_from {backend: 'claude-cli', model: 'claude-haiku-5-5', recorded_at: '2026-11-02T10:06:17Z'}. The Drafting screen (1440x900-03-drafting.png) lists 'A second AI check of each line' as a step in progress and finishes in 1.4 s ('This usually takes under a minute'). README.md:66 says no model is called in demo mode; the app does not.",
   "why_it_matters": "The wording follows D-065 and is true (a real model did check that exact answer, recorded), so not a blocker. A Zlayt reviewer who reads only the app may think the check ran live. See questions_for_chris.",
   "fix": "On the How page, step 3 and the demo badge tooltip: 'In this demo the second check's answers were recorded from a real run earlier.'",
   "acceptance_test": "The How page in demo mode states that the second-check answers were recorded earlier."}],
 "whats_right": [
  "The f_r7_1 and all-items How panel is now true on every item I read: the lead sentence is said only when a verdict exists, and the You row follows her decision.",
  "The flow is finishable at both sizes with no dead end: demo Start a new case says plainly that only the sample works, and Step 4 gives Copy, Download and a clear ready status.",
  "The How page is short and plain, reachable from every screen, and its claims match the per-item panel."],
 "questions_for_chris": [
  "Do you want the How page to say the demo's second-check answers were recorded earlier and are replayed (M5)? It is true and cheap, but it changes what a Zlayt reader believes about the demo."]}
```
