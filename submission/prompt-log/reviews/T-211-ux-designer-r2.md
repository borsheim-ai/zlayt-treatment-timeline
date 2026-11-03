# T-211 r2: UX designer review (Priya Raman, ux-designer-reviewer)

**Verdict: pass. 0 blockers, 0 majors, 2 minors.** Scope is HEAD a932fc9, served from a `git archive` copy in demo mode.

**r1 blocker closed.** On f_r7_1 the Second AI check row now says one thing: "Not run. Only the phrase list found this warning, so there is no prepared answer to double-check; it stays marked for review." The chip reads "AI: not run" and the "Prepared by our team ... then checked it" lead is gone. That matches the trace (judge_4 skipped, reason LEXICON_ONLY). The true path is intact: e1 and e2 still show the lead with "Agrees".

**r1 phone finding closed at 390x844.** The strip sits above the answer row on 19 of 19 items with Yes at y 708. At 390x667 the strip is below the first screen on the first paint, one page scroll away. I filed that as a minor, following the r1 precedent for scroll-reachable explanation (see questions_for_chris).

**Carried, not re-measured here.** The r1 minors at 1366x768 (highlights hidden after the panel opens), the missing live dispute, the How page word count, and the "not needed" vs "not sent" chip. The gate's M3 (the opened phone panel covers part of the line card) is still present; I saw it on the 390x844 opened screenshot. Originality is carried at 3 from r1 because it was not re-scored.

**Recorded model.** `claude-haiku-5-5`, the model this session runs as. The brief expected `claude-opus-5-5`.

```json
{"card": "T-211", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD a932fc9 (contains e22cae8, the T-211 r2 fix: `git merge-base --is-ancestor e22cae8 HEAD` exit 0; 9 files under app/ changed since e22cae8); git archive a932fc9 into a new empty scratch dir (scratchpad/t211r2-a932fc9); demo mode LLM_BACKEND=fixture FIXTURE_SET=curated on http://127.0.0.1:7941 with its own ZLAYT_DB; sample case (POST /api/cases {sample:true}, then POST /run); viewports 1440x900, 390x844 and 390x667 (touch)",
 "exercised": [
  "git rev-parse --short HEAD printed a932fc9; git merge-base --is-ancestor e22cae8 HEAD exited 0; git status --short | wc -l printed 3438 (dirty root tree, not used: all runs served from the archive)",
  "git archive a932fc9 | tar -x into a new empty scratch dir; started .venv/bin/python -m app.main from that dir on 127.0.0.1:7941; /api/health returned answers 'prepared', backend 'fixture', demo_mode true; listener PIDs stopped each time; curl returned 000 after the last stop",
  "API: sample case token QessMPklq_i17rOjwpNGiw, status ready, 9 entries, 4 amounts, 10 flags; GET /api/cases/<token>/items/f_r7_1/trace: proposed_by_ai skipped, judge_4 skipped with why 'Not run: only the phrase list found this flag, so there is no prepared answer to double-check', agreement fail with reason_code LEXICON_ONLY",
  "artifacts/review-evidence/T-211-r2-ux-probe.py: walked all 19 Step 2 items at 1440x900 and at 390x844, answering Yes; recorded the chips and panel text of every item; 0 page errors and 0 console errors (artifacts/review-evidence/T-211-r2-ux/T-211-r2-ux-probe.json)",
  "artifacts/review-evidence/T-211-r2-ux-phone.py: 390x844 and 390x667 touch; measured the how-summary strip against actions-in and Yes on all 19 items; on f_r7_1 took the closed-strip screenshot, tapped the strip, read the opened panel and took the opened screenshot (T-211-r2-ux-phone.json)",
  "artifacts/review-evidence/T-211-r2-ux-667-firstpaint.py: 390x667 first paint of e1 and f_r7_1 with scrollY 0 (T-211-r2-ux-667-firstpaint.json)",
  "Read app/frontend/guided/review.js:116-135 (judge state and You row), review.js:255-257 (strip placement by media query), review.js:382 (default open state), in the archived copy; reviews/T-211-ux-designer.md; reviews/GATE-M3M4-ux-designer.md",
  "Viewed artifacts/review-evidence/T-211-r2-ux/1440x900-f_r7_1-n13.png, T-211-r2-ux-390x844-f_r7_1-strip-opened.png, T-211-r2-ux-390x667-e1-firstpaint.png",
  "Not re-measured in r2 (outside the two asked checks): r1 minors at 1366x768, live dispute, How page word count, a3 'not needed' chip; gate M3 seen again on the 390x844 opened screenshot"],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "(dossier: major) At 390x667 the phone strip is below the first screen on first paint; it is one page scroll away",
   "evidence": "artifacts/review-evidence/T-211-r2-ux/T-211-r2-ux-667-firstpaint.json: e1 how_summary y 718.9 and f_r7_1 y 751.8 on a 667 px viewport with scrollY 0; doc_scroll_h 949. Screenshot artifacts/review-evidence/T-211-r2-ux/T-211-r2-ux-390x667-e1-firstpaint.png shows the Prepared answer tag and the bar (Yes at y 531) with no strip; the 'How it's checked' header link is on screen. T-211-r2-ux-phone.json: at 390x667 the strip is fully on screen and above the answer row on 3 of 19 items. Cause: app/frontend/guided/review.js:257 moves the strip into E.work, below the line card, when the screen is short (shortMQ: max-width 760px and max-height 720px); at 390x844 it sits in the bar above the answer row.",
   "why_it_matters": "On a short phone the code, AI and You chips appear only after the viewer scrolls the page. The explanation is reachable and the header link is visible at first paint, so nothing is false or missing; that is why this is minor under D-075. The dossier rates a panel that needs a scroll to find as major; r1 filed the same condition as minor and this follows it.",
   "fix": "On short phones keep the chip strip inside the bar above the question, as at 390x844, or move it into the line card head so it shows at first paint. Keep the rows folded.",
   "acceptance_test": "Playwright at 390x667, sample case Step 2, items e1 and f_r7_1, scrollY 0: how-summary rect fully inside the viewport, and its bottom at or above the top of the answer row."},
  {"severity": "minor", "title": "Carried from GATE-M3M4 M2: the f_r7_1 Code row says 'Did not pass' beside 'Found by code (phrase list)'",
   "evidence": "artifacts/review-evidence/T-211-r2-ux/1440x900-f_r7_1-n13.png: red 'Did not pass: The phrase list found this warning but the prepared answers did not; check that it applies.' then 'Found by code (phrase list).'. T-211-r2-ux-probe.json, f_r7_1.how_code_text. Trace agreement step: status fail, reason_code LEXICON_ONLY.",
   "why_it_matters": "The sentence is true: the agreement step failed. The Second AI row no longer contradicts it, so this is not the r1 blocker. A first-time viewer still reads 'did not pass' next to 'found by code' and may take it as the code finding nothing. Filed minor, as at the gate.",
   "fix": "For phrase-list-only flags, the Code row says 'Needs your check' with a neutral chip instead of 'Did not pass' (gate M2 fix).",
   "acceptance_test": "At 1440x900 on f_r7_1: how-code-text and how-chip-code contain no 'Did not pass' or 'not passed'; how-ai-text still reads 'Not run'."}],
 "whats_right": [
  "f_r7_1's Second AI check row now says one thing ('Not run. Only the phrase list found this warning...', chip 'AI: not run'), with no 'then checked it' lead, matching trace step judge_4 (skipped, LEXICON_ONLY).",
  "The true-positive path is intact: e1 and e2 still show 'Prepared by our team; the second AI check then checked it against the quote. Agrees.'",
  "At 390x844 the strip sits above the answer row on 19 of 19 items with Yes at y 708; 0 page errors and 0 console errors at 1440x900 and 390x844."],
 "questions_for_chris": [
  "Does D-075's 'invisible explanation' class cover a strip that is one page scroll away on a 390x667 phone while the 'How it's checked' link is on screen? I filed it minor, following the r1 precedent. If you read it as blocker, the verdict is fail."]}
```
