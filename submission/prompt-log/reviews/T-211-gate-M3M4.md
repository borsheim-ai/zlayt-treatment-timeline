# T-211 review, combined M3+M4 gate (D-075), staff-engineer-reviewer

Verdict: **pass**. HEAD a932fc9dcd627e0e5f92a234add6fc41b835a4f1.

Guided UI 'How this was checked' panel and 'How each answer is checked' page. My earlier T-211 blocker (UX r1: f_r7_1 false 'second AI then checked it') is fixed per the UX gate panel, and the e2e suite is green at HEAD's app. No blocker or major open; UX panel minors go to SCOPE_CUTS.

Panel evidence used: reviews/GATE-M3M4-staff-engineer.md (f6d5c19), reviews/GATE-M3M4-verify-staff.md (43ce6eb), artifacts/gate-M3M4-suite-final.txt (43ce6eb: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0, spec check all true).

## Findings
1. **minor** UX panel minors M2-M4 remain (accepted debt): f_r7_1 Code row reads 'Did not pass', the phone How panel covers the card, 'Found by code' is explained only in a tooltip. Evidence: reviews/GATE-M3M4-ux-designer.md findings M2, M3, M4; SCOPE_CUTS row 29. M1 (Step 4 date blanks) and M5 (recorded second-check results) were fixed by T-216: step4.js:70 hasDates, how.js:30 how-demo-note.

```json
{
 "card": "T-211",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git archive a932fc9: app/frontend/guided/{how.js,step2.js,step3.js,step4.js}, tests/e2e/guided/test_t211.py; panel UX walk at f6d5c19 and e2e at 43ce6eb",
 "exercised": [
  "git rev-parse HEAD = a932fc9 (docs-only on top of c2dd104); git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so the 43ce6eb unit/e2e runs still describe the app at HEAD",
  "python3 tools/board.py show <card> for the AC of this card",
  "read reviews/GATE-M3M4-{staff-engineer,ux-designer,paralegal,privacy-compliance,installer,product-manager}.md, GATE-M3M4-verify-staff.md, GATE-M3M4-verify-pm-r2.md and artifacts/gate-M3M4-suite-final.txt",
  "git archive a932fc9 into a scratchpad dir (arcC) for every check below, so the dirty main working tree was not read for product claims",
  "ls: app/frontend/guided/validation-ladder.svg and tests/e2e/guided/test_t211.py exist at a932fc9",
  "grep how-demo-note app/frontend/guided/how.js:30 (T-216 demo-mode note: second-check results were recorded earlier)",
  "artifacts/gate-M3M4-suite-final.txt: e2e 614 passed, 0 failed (includes test_t211 at 1440 and 390); git diff --stat 43ce6eb a932fc9 -- app is empty",
  "read reviews/GATE-M3M4-ux-designer.md: all 23 items' panel rows compared with the item trace; f_r7_1 now 'Not run. Only the phrase list found this warning'; gap and date rows say 'Not needed'",
  "test_flag_origin_t214.py (the 'Found by code' label this panel shows) ran inside the 53-passed group in the archive",
  "python3 tools/board.py show T-217: role release (confirms the checklist owner cell is wrong for T-188 minor)"
 ],
 "verdict": "pass",
 "scores": {
  "ac_met_at_head": 5,
  "panel_text_true": 5,
  "tests_green": 5
 },
 "findings": [
  {
   "severity": "minor",
   "title": "UX panel minors M2-M4 remain (accepted debt): f_r7_1 Code row reads 'Did not pass', the phone How panel covers the card, 'Found by code' is explained only in a tooltip",
   "evidence": "reviews/GATE-M3M4-ux-designer.md findings M2, M3, M4; SCOPE_CUTS row 29. M1 (Step 4 date blanks) and M5 (recorded second-check results) were fixed by T-216: step4.js:70 hasDates, how.js:30 how-demo-note.",
   "why_it_matters": "Copy and phone-layout polish; no false statement in the panel.",
   "fix": "Post-MVP per SCOPE_CUTS row 29.",
   "acceptance_test": "existing guided e2e stays green after any change."
  }
 ],
 "whats_right": [
  "Each panel row is true against the trace: code row counts match passing steps, the model id is the recorded one, and 'Not needed' appears only where code does the arithmetic.",
  "Demo mode now says outright that the second-check results were recorded earlier (how.js:30)."
 ],
 "questions_for_chris": []
}
```
