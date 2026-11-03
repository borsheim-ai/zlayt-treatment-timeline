# T-216 review, combined M3+M4 gate (D-075), staff-engineer-reviewer

Verdict: **pass**. HEAD a932fc9dcd627e0e5f92a234add6fc41b835a4f1.

Gate fix B (frontend): the six e2e failures are fixed, Step 4 names the date blanks, and the How page says demo second-check results were recorded. Full e2e is green at 43ce6eb and the app is unchanged since. No blocker or major open.

Panel evidence used: reviews/GATE-M3M4-staff-engineer.md (f6d5c19), reviews/GATE-M3M4-verify-staff.md (43ce6eb), artifacts/gate-M3M4-suite-final.txt (43ce6eb: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0, spec check all true).

## Findings
1. **minor** UX minor M1 residual: on a phone the Step 3 instruction about the date blank sits inside a scrolling card. Evidence: GATE-M3M4-ux-designer.md M1 (phone part); SCOPE_CUTS row 29 'phone cue for Step 3 blank instruction'. The Step 4 half was fixed in 6371a28.

```json
{
 "card": "T-216",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git archive a932fc9: app/frontend/guided/step4.js, how.js, tests/e2e/guided/*; e2e record at 43ce6eb",
 "exercised": [
  "git rev-parse HEAD = a932fc9 (docs-only on top of c2dd104); git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so the 43ce6eb unit/e2e runs still describe the app at HEAD",
  "python3 tools/board.py show <card> for the AC of this card",
  "read reviews/GATE-M3M4-{staff-engineer,ux-designer,paralegal,privacy-compliance,installer,product-manager}.md, GATE-M3M4-verify-staff.md, GATE-M3M4-verify-pm-r2.md and artifacts/gate-M3M4-suite-final.txt",
  "git archive a932fc9 into a scratchpad dir (arcC) for every check below, so the dirty main working tree was not read for product claims",
  "artifacts/gate-M3M4-suite-final.txt: E2E_REQUIRE_DB=1 pytest tests/e2e 614 passed, 0 failed, 1 skipped (841 s) on a fresh archive of 43ce6eb",
  "git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so that run covers the HEAD app",
  "step4.js:70 hasBlanks/hasDates names both the [Ex. __ / Bates __] blanks and each 'date of service [____]' blank; how.js:30 how-demo-note says the second AI check's results were recorded",
  "verify-staff: Playwright README walk to the letter, zero page errors, letter has the two charge lines with the fillable blank and the exact total line",
  "UX panel: phone walk at 390x844 and desktop walk reached the letter with no console or page errors, no horizontal scroll (at f6d5c19; layout fixes for 375/390 landed in 6371a28)"
 ],
 "verdict": "pass",
 "scores": {
  "ac_met_at_head": 5,
  "tests_green": 5,
  "provenance_wording_true": 5
 },
 "findings": [
  {
   "severity": "minor",
   "title": "UX minor M1 residual: on a phone the Step 3 instruction about the date blank sits inside a scrolling card",
   "evidence": "GATE-M3M4-ux-designer.md M1 (phone part); SCOPE_CUTS row 29 'phone cue for Step 3 blank instruction'. The Step 4 half was fixed in 6371a28.",
   "why_it_matters": "A phone user can miss the Step 3 instruction, though Step 4 now names the blanks again.",
   "fix": "Post-MVP per SCOPE_CUTS row 29.",
   "acceptance_test": "a 390 px e2e asserts the date-blank instruction is visible without scrolling the card."
  }
 ],
 "whats_right": [
  "614 e2e tests pass on a fresh archive with the DB required, so the green is not a skip.",
  "Step 4 now tells the paralegal about the date-of-service blanks before she downloads the letter."
 ],
 "questions_for_chris": []
}
```
