# T-149 UX review, round 3 (final): multi-case overview and detail (Priya Raman lens)

Verdict: pass (0 blockers, 0 majors, 3 minors, 1 nit). All four round-2 items I was asked to verify are fixed in the running app.

Served from `git archive HEAD` (f7a8f2a, `git merge-base --is-ancestor f7a8f2a HEAD` printed ancestor-ok) into the scratchpad, started with `python -m app.main` on port 7963 (PID 74897), `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, scratch DB. Checked at 1440x900 and 390x844.

Round-2 items, one by one:
1. Stale overview chip: FIXED. The list payload now carries `hitl.needs_review_open` (seen in GET /api/cases). On lib03 (4 needs-review items) and the sample (3), I dismissed the needs-review items one at a time through the UI buttons while other items stayed open, returned with All cases after each step and compared three numbers: open needs-review items in the DOM, the detail chip, the row chip. They matched at every step (4,3,2,1,0 and 3,2,1,0) at 1440 and at 390 (T-149-ux-r3-walk7.py, walk8.py). The singular "1 needs review" is shown correctly. After the last one the chip is gone while "N of 14 decided" still shows the rest are open.
2. Green "Ready" while unreviewed: FIXED. With 18 (lib06) and 11 (lib03) items undecided: overview row, block chip, Case checks summary and the expanded Case checks verdict all read "Can export — N not reviewed (they stay out of the letter)" in amber (verdict computed rgb(107,68,0) on rgb(255,241,204), class `zs-v-ready_for_decision`; no `zs-v-ready`). "Ready to export" in page text appears once, only as the question label "Ready to export?" above the amber verdict. Green "Ready to export" with a green chip appears only on a fully decided case (14 of 14 accepted via API: block "Everything decided", verdict rgb(19,97,58)). Same at 390.
3. "Do this first" names the item and Start review opens it: FIXED. Sample: "$185 (record 4) — This figure is a rate..."; lib06: "Attorney referral (record 3)"; lib03: "$120 (record 3)"; lib09: "Gap of 42 days (records 1, 2)". At 1440 "Go to it" and "Start review" both put focus on the same element (amount-$185, flag-f_r3_2, amount-$120, flag-f_gap_r1_r2), which equals the server's `next_action.item_id` (a2, f_r3_2, a2, f_gap_r1_r2). At 390 Start review is hidden by design and Go to it lands on the same items. When the AI-flagged items are all decided and none is accepted, the line falls back to the case-level sentence and both buttons land on entry 1.
4. New case button: FIXED. "New case" (btn-new-case) is in the Cases header at 1440 (91x36) and 390 (91x44); clicking it moves focus to the Case name field (input-title) and brings it into view.

Scores (1-5): design quality 4, originality 3, craft 4, functionality 4. None is 2 or below.

Known leftovers, graded as minors as agreed: kinds line needs a backend change; stepper fail-vs-waiting wording; first Accept near the fold at 390 (see F1 for the numbers).

Evidence: `artifacts/review-evidence/T-149-ux-r3-*` (scripts setup, walk1-walk10, screenshots).

```json
{"card": "T-149", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive HEAD f7a8f2a served at http://127.0.0.1:7963 (stopped, PID 74897); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratch ZLAYT_DB; overview and detail block, round-2 majors only; 1440x900 and 390x844",
 "exercised": [
  "python3 tools/board.py show T-149 (r3 handoff, round-3 scope); read reviews/T-149-ux-designer-r2.md and reviews/T-149-paralegal-r2.md",
  "git rev-parse --short HEAD (f7a8f2a); git merge-base --is-ancestor f7a8f2a HEAD (ancestor-ok); git archive HEAD into the scratchpad; python -m app.main on PORT=7963 (PID 74897), curl 200",
  "created cases through POST /api/cases and /run (sample, lib01 [analysis failed in the fixture run], lib06, lib03, lib02 ingested only, lib09, two pastes) plus fresh sample and lib03 copies for each stale-chip pass (T-149-ux-r3-setup.py, walk5.py)",
  "New case button at 1440 and 390: presence, box, click, focus on input-title, scroll position, overview row text, keys hint (walk1)",
  "Do this first text, Go to it and Start review focus targets vs the server's next_action.item_id for sample, lib06, lib03, lib09 at both widths (walk2)",
  "Accepted entries in lib06 (1) and lib03 (3) so the gate opens with items undecided; scanned overview, block, expanded Case checks (summary click) for green computed colours and the string 'Ready to export'; read case-verdict class and colour at both widths (walk3, probe)",
  "Stale chip: dismissed needs-review items one at a time in the UI on lib03 and the sample, returning to All cases after each step, comparing DOM open needs-review count, detail chip and row chip, at 1440 and 390 (walk6, walk7, walk8; my first walk4 regex missed the singular '1 needs review' and was discarded)",
  "Partly decided lib03 (needs-review items done, 10 open): Do this first fallback and Start review target; then accepted everything via the API and read the green Everything decided block and Ready to export verdict (walk9)",
  "First Accept and entry-1 date y at 1440 and 390 for sample, lib06, lib09, scrollWidth (walk10)",
  "Stopped the server by PID 74897 and confirmed the port no longer answers"],
 "verdict": "pass",
 "scores": {"design_quality": 4, "originality": 3, "craft": 4, "functionality": 4},
 "findings": [
  {"severity": "minor", "title": "At 390 the first Accept is below the fold on most cases, and the 30 px figure in the handoff holds only for the sample",
   "evidence": "walk10 at 390x844: first Accept top y 782 (sample, inside the screen), 1,560 (lib06), 1,764 (lib09). At 1440x900: 620 (sample), 879 (lib06, at the edge), 1,615 (lib09). The handoff reports one number (~875 px) for the sample only. Screenshot artifacts/review-evidence/T-149-ux-r3-first-screen-390.png.",
   "why_it_matters": "A paralegal opening lib06 or lib09 on a phone scrolls two screens past progress, Do this first and chips before she can act on an entry; the fix helped the sample more than the other cases.",
   "fix": "Keep Do this first to the item name plus a shortened reason on the phone, with the full reason on tap; check lib06 and lib09, not only the sample.",
   "acceptance_test": "E2E at 390x844 on lib06 and lib09: the first entry's Accept top is within 1.2 screens (y <= 1,013)."},
  {"severity": "minor", "title": "Do this first falls back to a case-level sentence that names no item",
   "evidence": "walk9, lib03 after the needs-review items were decided and nothing accepted: 'Do this first: Nothing is accepted or edited yet, so the letter would be empty.' with Go to it landing on entry-1 (server next_action kind 'case', item_id null). The same sentence repeats in the chip row below it.",
   "why_it_matters": "It is true and the button works, but the line no longer says what to do (open the first entry and decide it) and repeats the blocker text.",
   "fix": "For kind 'case' say 'Decide the first entry: <date, provider>' and let the blocker sentence appear once.",
   "acceptance_test": "E2E: with next_action.kind == 'case', the Do this first text names an entry and the blocker sentence appears once in the block."},
  {"severity": "minor", "title": "Known leftovers: kinds line on overview rows and fail-vs-waiting stepper wording",
   "evidence": "walk1: rows read '13 need review' and the same blocker sentence on six rows, no kind of item. Stepper wording unchanged per handoff ('Failed/Blocked vs Needs your decision/Not done yet'). Accepted by the scope as minors; carried unchanged.",
   "why_it_matters": "Rows still say how many, not what kind; the stepper words are distinct but not visually distinct.",
   "fix": "Have the list send item kinds and show 'date conflict, gap' under the chips; add a glyph difference for failed vs waiting.",
   "acceptance_test": "E2E: a row with a date-conflict flag names it; a failed step has a glyph no waiting step uses."},
  {"severity": "nit", "title": "Small colour and label details in the overview and Case checks",
   "evidence": "walk3: the 'All cases (8)' filter text is green rgb(19,97,58) on white (a selected-filter style, not a status); the Case checks panel keeps the question label 'Ready to export?' above the amber 'Can export — N not reviewed' verdict.",
   "why_it_matters": "Green is meant to mean decided; a green filter label and a 'Ready' question label sit next to amber statuses and slightly dilute that.",
   "fix": "Use the neutral selected style for the active filter; change the label to 'Export status'.",
   "acceptance_test": "Screenshot check: no green text outside decided states; 'Ready to export' appears only on fully decided cases."}
 ],
 "whats_right": [
  "The overview row, detail chip and gate wording now come from the same numbers: the chip tracked the DOM count at every step at both widths, and green appears only when nothing is undecided.",
  "Do this first names a concrete item (amount, flag, record) and Go to it and Start review land on the server's item, not a different one.",
  "New case is one visible primary button that puts the cursor in the name field, at 44 px height on the phone with no sideways scroll."],
 "questions_for_chris": []}
```
