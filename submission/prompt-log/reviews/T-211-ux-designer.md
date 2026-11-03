# T-211 — UX designer review (Priya Raman, ux-designer-reviewer)

**Verdict: fail** (1 blocker, 0 majors, 5 minors). Severity follows D-075 (Chris, 2026-11-03), which is binding until submission. Only findings that make the demo wrong or misleading, or that make the judge/HITL explanation false or invisible, are blocker-class. Everything else is minor and goes to SCOPE_CUTS. Minors that my dossier (§8) would rate major are labelled "(dossier: major)", so the lower rating is visible.

Scope: HEAD cda2856 (`git rev-parse --short HEAD` printed `cda2856`). T-211 commits 82217e5 and 4e4ff36 are its ancestors. `git diff --stat 4e4ff36 HEAD -- app/` printed nothing, so the app is the same as at the card commit. I extracted the commit with `git archive cda2856` into a new empty scratch directory. I served it in demo mode the way run.sh does (LLM_BACKEND=fixture, FIXTURE_SET=curated) on :7932 with its own DB. `/api/health` returned `"answers":"prepared"`, `"generator":"hand-checked (qa)"`, `"judge":"claude-haiku-5-5"`. I stopped the server afterwards, and `curl` on :7932 returned `000`.

What works: on desktop the panel is clear and well placed. At 1440x900 it is open on 19 of 23 items and folds to chips on the 4 multi-record warnings. The summary row sits at y 536–706, above the action bar (top 729). Yes stays at y 782 on every item, and there are no console errors. The How page is plain and honest about prepared answers.

The problem is one sample item. On f_r7_1 the panel says the second AI checked a prepared answer. The same row also says the second AI did not run and that there is no prepared answer. That makes the judge explanation false on a screen the demo shows.

```json
{"card": "T-211", "persona": "ux-designer-reviewer", "model": "claude-opus-5-5",
 "scope": "HEAD cda2856 (contains 82217e5, 4e4ff36; no app/ diff since 4e4ff36); git archive into a new empty dir; demo mode (fixture, curated) on http://127.0.0.1:7932; sample case (evals/golden/sample.txt via POST /api/cases {sample:true})",
 "exercised": [
  "Read personas/ux-designer.md, D-074, D-065, D-069 note in memory/contracts/api.md, D-075, the T-211 card and handoff, review.js:90-137 and 240-402, how.js, how.css, the T-211 diff of app.js/step2.js/step3.js",
  "artifacts/review-evidence/T-211-ux-probe.py: per-item judge verdicts from GET /items/<id>/trace for all 23 sample items (first on a server started without FIXTURE_SET, which served the 'recorded' set; discarded and rerun on the curated server)",
  "artifacts/review-evidence/T-211-ux-measure.py: opened every Step 2 (19) and Step 3 (4) item at 1440x900, 390x844 (mobile, touch) and 1366x768; measured panel open/closed, summary rect vs action bar, highlights inside the record window, Yes rect, page scroll; opened the folded panel on 6 items and re-measured; console errors collected (none at any size)",
  "How page via the header link at all three sizes: word count, steps text, ladder image size and sideways scroll, Back returns to /",
  "Screenshots in artifacts/review-evidence/T-211-ux/ (measure.json holds every number quoted)",
  "Not exercised (D-075 time box): full e2e, an end-to-end keyboard walk to Step 4, the You row after a decision (covered by test_t211.py, not re-driven live)"],
 "verdict": "fail",
 "scores": {"design quality": 4, "originality": 3, "craft": 3, "functionality": 3},
 "findings": [
  {"severity": "blocker", "title": "f_r7_1: the Second AI check row says a prepared answer was checked by the second AI, then says the check did not run and there is no prepared answer",
   "evidence": "artifacts/review-evidence/T-211-ux/1440x900-f_r7_1.png (Item 13 of 19, accident-date warning, tag 'Prepared answer'). The Second AI check row reads, verbatim: 'Prepared by our team; the second AI check then checked it against the quote.' then 'Not needed. Not run: only the phrase list found this warning, so there is no prepared answer to double-check; it stays marked for review.' The Code check row reads: 'Did not pass: The phrase list found this warning but the prepared answers did not; check that it applies.' Probe: f_r7_1 prepared=True, judge_4 status 'skipped', judge_verdict None. Cause: app/frontend/guided/review.js:117 sets the prepared lead from item.prepared alone, whatever the judge step did; review.js:121 maps every skipped step without a verdict to the word 'Not needed', even when its reason begins 'Not run'.",
   "why_it_matters": "This is the one sample item where the ladder did not run in full, so it is where a first-time viewer learns most about the ladder. The panel tells them a second AI checked a prepared answer. The same row then says neither happened, and it labels a check that did not run as 'Not needed'. D-074 says the app must show the judge's verdict truthfully. D-065 says provenance wording must be truthful. Under D-075 a false judge explanation is blocker-class.",
   "fix": "Show the prepared lead only when the judge step actually returned a verdict (status pass or fail with judge_verdict). Show the verdict word 'Not run' (chip 'AI: not run') when the step was skipped and its reason begins 'Not run', and keep 'Not needed' for code-made items such as the gap and accident-date arithmetic. Backend owner: an item that only the phrase list found should not carry the 'Prepared answer' tag or prepared=true. That is a card for backend, not frontend.",
   "acceptance_test": "Live sample case, f_r7_1, at 1440x900: how-ai-text does not contain 'then checked it'; how-verdict is 'Not run'; how-chip-ai is 'AI: not run'. f_gap_r6_r7 still reads 'Not needed'. e1 still shows the prepared lead with 'Agrees'."},
  {"severity": "minor", "title": "(dossier: major) At 390x844 the panel is below the action bar on 23 of 23 items; only a grey edge hints that it exists",
   "evidence": "artifacts/review-evidence/T-211-ux/390x844-e1.png. measure.json 390x844: the summary's top edge is between y 665 and 972 on every item, and the action bar's top edge is at y 659. The line card is scrollable (scrollHeight 290-597 vs clientHeight 216). After a tap the panel opens in view (390x844-e1-opened.png). The header link 'How it's checked' is visible at x 190, y 50 (390x844-home.png).",
   "why_it_matters": "This answers the brief's question 'is it still discoverable?'. On a phone it is not discoverable without scrolling inside the card. A viewer who never scrolls that inner box never sees the per-item code check, AI check and You rows. I did not rate it blocker because the panel is one scroll away and the header link explains the ladder on every screen.",
   "fix": "On a phone, put the chip row (closed summary) directly under the line's tag and date, or in the line card's head, so the three chips show at first paint. Keep the rows folded.",
   "acceptance_test": "390x844, every sample item: the how-summary rect is fully above the actions top edge with the line card scrolled to 0."},
  {"severity": "minor", "title": "(dossier: major) Once opened, the panel hides the highlighted words, and the choice persists for the rest of the visit",
   "evidence": "measure.json 1366x768 after opening: e1 shows 0 of 1 marks in the record window, f_cx1 0 of 2, f_r7_1 0 of 1, a2 0 of 1, a3 0 of 1. At 1440x900 after opening, f_gap_r6_r7 shows 2 of 4 and f_cx1 1 of 2. Cause: review.js:399 returns early from fitHow once R.howOpen is set, so after one click every later item keeps the panel open even when it pushes the highlight out. Screenshot: 1366x768-e1-opened.png.",
   "why_it_matters": "The quote beside the line is how the paralegal verifies an item. A viewer on a 1366x768 laptop who opens the panel once to learn the ladder then has to scroll the record window to find the quote on every item. The words are still reachable by scrolling, so this is not the §5 blocker.",
   "fix": "After the user opens the panel, still scroll the record window so the first mark is in view (alignMark after layout). Or cap the open panel's height with its own scroll, so the window keeps room for the marks.",
   "acceptance_test": "1366x768: open the panel on e1, then step through e2..e9 and f_cx1; on each, at least the first mark is inside the card-source rect."},
  {"severity": "minor", "title": "The demo never shows the second AI disputing anything; the dispute path is covered only by a stubbed e2e",
   "evidence": "T-211-ux-probe.py on the curated sample: judge verdicts are 'supported' on 18 items, skipped on 5 (gap, accident-date, f_r7_1, a3) and disputed on 0. tests/e2e/guided/test_t211.py rewrite_trace() forces 'partially' on e2 with page.route.",
   "why_it_matters": "D-074 asks a first-time viewer to understand that an independent check can disagree. In the demo every verdict is a green 'AI: agrees', so the judge reads as a rubber stamp. The red 'Disputes' state has never been seen live.",
   "fix": "Product decision. Either have the How page show one disputed example as a static picture of the panel, or add a committed demo case whose recorded judge verdict is a real dispute.",
   "acceptance_test": "A viewer of the demo can reach one screen showing 'AI: disputes' with the server's reason, without stubbing."},
  {"severity": "minor", "title": "The How page is 412 words, not 'about 150', and the picture starts below the fold",
   "evidence": "measure.json 1440x900-how: words 412, steps end at y 497, ladder image top at y 682. At 1440x900 the fold shows an empty white frame (1440x900-how-fold.png). At 390x844 the image is 640 px wide in a 318 px box and scrolls sideways (390x844-how-full.png).",
   "why_it_matters": "The four steps are clear (what's right, below). Below them are three more panels (the picture, the code-vs-AI lists and the repo paths) that repeat the steps. On a phone the picture must be scrolled sideways to read it.",
   "fix": "Put the picture directly beside or under the four steps, and fold the repo list under 'For reviewers'. On a phone use a tall version of the SVG.",
   "acceptance_test": "1440x900: part of the ladder picture is visible above the fold. 390x844: figure scrollWidth <= clientWidth."},
  {"severity": "minor", "title": "'Not needed' covers two different situations, and the 'Code: none' / 'AI: not needed' chips show no reason when the panel is folded",
   "evidence": "Probe: a3 judge_2 skipped with 'Damages and other non-bill figures are not sent to the second check.'; f_gap_r6_r7 judge_not_needed 'arithmetic over dates'. Both show the chip 'AI: not needed' (390x844-a3.png, 1440x900-f_gap_r6_r7.png).",
   "why_it_matters": "For the gap, 'not needed' is accurate: code did the work. For damages, the second check is skipped by policy, so 'Not sent' is the honest word.",
   "fix": "Chip 'AI: not sent' for policy skips; keep 'not needed' for code-made items.",
   "acceptance_test": "a3 shows 'AI: not sent'; f_gap_r6_r7 shows 'AI: not needed'."}],
 "whats_right": [
  "At 1440x900 the panel is open on 19 of 23 items and folds to chips on the 4 multi-record warnings. The primary action never moves (Yes at y 782 on every item), and there were 0 console errors across 69 item views.",
  "The How page's four steps are honest and plain. Step 1 says the demo answers were 'written ahead of time, not by an AI model' (D-065), and step 3 says the second AI 'can be wrong too, which is why the last word is yours'.",
  "The header link is on every screen and fits at 390 ('How it's checked', 137x40 px), and Back returns to where the user came from."],
 "questions_for_chris": [
  "Should the demo include one real recorded judge dispute (a committed case or a static example on the How page), so viewers see the second check disagree at least once?"]}
```
