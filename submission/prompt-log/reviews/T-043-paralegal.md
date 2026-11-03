# T-043 review: paralegal-reviewer (Maria Delgado)

Verdict: changes (0 blockers, 1 major, 4 minors). No blocker-class red flag found in what I could exercise.

Exercised: dev harness (`/dev/panels.html`, variants sample, 01, 03, 07) and `index.html?api=mock` with the sample case, in Playwright at 1280 and 375 px. The real backend was down (`curl localhost:7860/api/health` returned 000), so `tests/e2e/*` were not run live by me, and reload persistence is not verified.

What held up against the checklist:
- Four flag groups plus "Record warnings" render; the accident-date conflict card shows "Date of accident per intake form: 2026-01-19." beside the 2026-01-09 header lines of records 1 and 2, unmerged, with none of "resolved", "correct date", "delay", and the line "the tool does not choose between them".
- Gap card: "Gap of 73 days", both dates in long form, one "Open records 6 and 7" button that opens both records. No 28-day flag.
- Charges: "Accepted charges: $0 | Detected, not yet accepted: $8,390 (not a total)", then $8,390 after accepting both, then $2,150 after dismissing the ER charge. The $185 sits in the unclear tray as "rate $185/visit; visit count not stated; needs review", with no PT total. "$1,2OO" stays in the tray after Accept as noted ("Noted for the internal notes only; not in the letter or the total"). "Missing 3 days of work" is not listed as a charge.
- No `innerHTML` anywhere in `app/frontend/*.js` (grep returned nothing). `charges.js` has `+` only for string concatenation, and `RV.money` formats by string slicing.
- Keyboard: e, Ctrl+Enter, Escape, d, a, o, j, k all work from a focused card. At 375 px scrollWidth is 375, 0 buttons are off-screen, and 0 of 66 buttons are under 44 px tall.

Evidence: `artifacts/review-evidence/T-043-paralegal-probe*.py` and `T-043-*.png` (for example `T-043-1280-10-conflict-card.png`, `T-043-375-03-charges.png`).

```json
{"card": "T-043", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 636c961; app/frontend/{review,flags,charges}.js, review.css, dev/panels.html harness and index.html?api=mock served at http://localhost:7866; sample case (Appendix A); 1280 and 375 px. Backend (7860) was down; live E2E not run.",
 "exercised": [
  "python3 tools/board.py show T-043 (AC and handoff read)",
  "grep innerHTML|outerHTML|insertAdjacentHTML in app/frontend/*.js: 0 hits; grep '+' in charges.js: only string concatenation; RV.money formats cents by string slicing",
  ".venv/bin/python -m http.server 7866 --directory app/frontend (killed afterwards)",
  "artifacts/review-evidence/T-043-paralegal-probe.py, -probe2.py, -probe3.py, -probe4.py (Playwright, 1280 and 375 px)",
  "harness sample: 4 groups + Record warnings, 73-day gap, accident-date conflict card (no resolved/correct date/delay), plan-vs-actual card, 2 pre-existing, patient self-report chip, gap card Open records 6 and 7",
  "harness charges: totals $0/$8,390 pending -> $8,390 accepted -> $2,150 after dismiss ER; $185 in unclear tray; no PT total",
  "harness variants: ?case=01 confirm_date radios, ?case=03 $1,2OO accepted stays in tray with total unchanged, ?case=07 injection banner",
  "keyboard-only: j/k/a/d/e/o/r, Ctrl+Enter, Escape, Tab, from queue rows and from flag and charge cards",
  "375 px: scrollWidth 375, no off-screen buttons, 0 of 66 buttons under 44 px; screenshots T-043-375-*.png",
  "index.html?api=mock Use the sample case + Analyze at 1280 and 375: flag groups, totals, tray, console errors (none)"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "flags_visible_and_sourced": 4, "charges_total_integrity": 5, "keyboard_flow": 3, "mobile_375": 5},
 "findings": [
  {"severity": "major",
   "title": "ACs 1-5 are ticked done on specs that were not run, and the integrated mock shows only the gap group",
   "evidence": "T-043 AC 1-5 text says 'proved by tests/e2e/test_*.py'; every evidence line says 'server-side E2E specs not run (backend not up)'. My run of index.html?api=mock + sample: flag headings ['Treatment gaps (1)', 'Conflicts between records (0)', 'Pre-existing conditions (0)', 'Causation language (0)', 'Record warnings (0)']. The conflict, pre-existing and causation cards exist only in the hand-built fixture app/frontend/dev/mock-data.js (harness). curl localhost:7860/api/health -> 000.",
   "why_it_matters": "The AC requires at least one flag per group in the sample and names the specs as the proof. As shipped, nobody has seen the accident-date conflict, the prior-condition flags or the reload-persisted statuses come through the real API and render. If the live evidence shape differs (the handoff admits it added 'Quoted line from this record' client-side because api.md evidence is only header lines), the card I approved here will not be the one the paralegal sees.",
  "fix": "Do not close the card on harness evidence alone. Run tests/e2e/test_flags_panel.py, test_charges.py, test_review_matrix.py, test_keyboard_mobile.py and test_source_record.py::test_gap_flag_two_records against the live backend once T-039/T-040 land, and attach the output. Until then, mark AC 1-5 as mock-verified in the notes.",
   "acceptance_test": "Those five specs pass against the real API; the live sample shows 'Conflicts between records (2)' with the 2026-01-19 / 2026-01-09 card unmerged, and a reload restores statuses and the accepted total."},
  {"severity": "minor",
   "title": "Pressing a or d on a flag or charge card throws focus and scroll up to the timeline",
   "evidence": "T-043-paralegal-probe4.py on index.html?api=mock at 1280: focused the gap flag at scrollY 2758, pressed a; result 'scrollY before/after 2758 77', focus on ARTICLE e3 with queue=true, and the flag was no longer in view (T-043-1280-13-after-a-on-flag.png). review.js focusItem() prefers the [data-testid=queue] row.",
   "why_it_matters": "A paralegal working down the Flags panel with the keyboard loses her place after every accept or dismiss and cannot see the item she just decided. That slows verification, which is the whole job. Keyboard completion still works (R-RV-4 is met), so this is not a blocker.",
   "fix": "After a or d from a flag or charge card, advance to the next pending item inside the same panel (or keep focus on the decided card) and only fall back to the queue when the panel has none left. Keep the live-region message.",
   "acceptance_test": "E2E: focus the first flag, press a, assert scrollY change is under one viewport and document.activeElement is inside [data-testid=flags-panel]."},
  {"severity": "minor",
   "title": "$185 row says 'rate $185/visit; visit count not stated' without the plan-versus-attended context",
   "evidence": "Tray text at 1280 and 375: 'rate $185/visit; visit count not stated; needs review'. Checklist 12 expects '12 planned; discharged at visit 9' beside it. The plan-vs-actual flag (f_plan_4_6) is in another panel.",
   "why_it_matters": "The paralegal reconciling specials has to jump to the flags panel to see why the visit count cannot be guessed (12 planned, discharged at visit 9). The total is correct; only the reason is thin.",
   "fix": "When a rate has a linked plan-vs-actual flag, append its two numbers from the evidence: 'visit count not stated (12 planned; discharged at visit 9)'. Quote only what the backend supplies.",
   "acceptance_test": "Unit/E2E: tray row for $185 contains '12 planned' and 'visit 9'; accepted-total unchanged."},
  {"severity": "minor",
   "title": "Reason typed in 'Dismiss with reason' is not shown anywhere after the flag is dismissed",
   "evidence": "probe3: dismissed f_pat_9 with reason 'Not relevant'; card text after dismissal ends '... Open record 9 / Accept / Edit note / Dismiss / Reset' with no reason shown (while an edited flag shows 'Your note: ...').",
   "why_it_matters": "Checklist 14 wants a visible trace of what I changed. A dismissed flag the attorney asks about later should show why it was dismissed without opening anything else.",
   "fix": "Show 'Dismissed because: <reason>' on dismissed flag cards when the API returns it (api.md note field), and next to Reset.",
   "acceptance_test": "E2E: dismiss with reason 'Not relevant', assert the card contains 'Not relevant'; reset removes it."},
  {"severity": "minor",
   "title": "Flags panel does not put needs-review cards first within a group",
   "evidence": "Harness sample, 'Conflicts between records (2)': the verified accident-date card is listed before 'Planned visits differ from visits attended' (Needs review). Cards are in API order (flags.js render filters flags by type, no sort). Checklist 16 wants items needing review first, each with a one-sentence reason (the reason sentence itself is present).",
   "why_it_matters": "In the flags panel the card that most needs a decision can sit under one that is already verified, so a skim of the first card of each group misses it. The queue at the top of the page partly covers this, so I rate it minor.",
   "fix": "Within each group, sort state=needs_review before verified (stable order otherwise). Do the same in the charges table.",
   "acceptance_test": "Unit: with one verified and one needs_review flag in a group, the needs_review card renders first."}
 ],
 "whats_right": [
  "Accident-date conflict card shows 2026-01-19 and both 2026-01-09 header lines side by side, unmerged, with the explicit line 'the tool does not choose between them' and none of resolved/correct date/delay.",
  "Charges never add on the client: accepted total comes from the API ($8,390, then $2,150 after dismissing ER), pending is labelled '(not a total)', $185 and $1,2OO stay in the unclear tray and 'Accept as noted' says it is internal-only.",
  "375 px works: scrollWidth 375, every action reachable, all 66 buttons at least 44 px tall, stacked cards with labelled fields; no innerHTML anywhere."
 ],
 "questions_for_chris": [
  "In the harness fixture the PT discharge with two missed appointments sits under type 'conflict' (treatment_plan_vs_actual). Checklist 10 / D-013 expects a `causation` flag for missed appointments. Should the backend emit both, or is the conflict-type card the intended home? (Backend question, not T-043.)"
 ]}
```
