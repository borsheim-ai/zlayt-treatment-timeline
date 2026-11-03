# T-214 review, combined M3+M4 gate (D-075), staff-engineer-reviewer

Verdict: **pass**. HEAD a932fc9dcd627e0e5f92a234add6fc41b835a4f1.

Flags found only by the phrase list are 'Found by code' and not 'Prepared answer'. Staff panel mutant and my rerun of the tests at HEAD agree. No blocker or major open.

Panel evidence used: reviews/GATE-M3M4-staff-engineer.md (f6d5c19), reviews/GATE-M3M4-verify-staff.md (43ce6eb), artifacts/gate-M3M4-suite-final.txt (43ce6eb: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0, spec check all true).

## Findings
1. **minor** Gap flag `why` still says the second check agreed although no judge ran (same text as T-202 minor, accepted). Evidence: app/backend/present.py:10 OK_WHY; panel flag_probe f_gap_r6_r7 why with ladder.judge null. UI shows 'Not needed'.

```json
{
 "card": "T-214",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git archive a932fc9: app/backend/present.py:310-312, tests/unit/test_flag_origin_t214.py, test_prepared_property.py",
 "exercised": [
  "git rev-parse HEAD = a932fc9 (docs-only on top of c2dd104); git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so the 43ce6eb unit/e2e runs still describe the app at HEAD",
  "python3 tools/board.py show <card> for the AC of this card",
  "read reviews/GATE-M3M4-{staff-engineer,ux-designer,paralegal,privacy-compliance,installer,product-manager}.md, GATE-M3M4-verify-staff.md, GATE-M3M4-verify-pm-r2.md and artifacts/gate-M3M4-suite-final.txt",
  "git archive a932fc9 into a scratchpad dir (arcC) for every check below, so the dirty main working tree was not read for product claims",
  "pytest test_flag_origin_t214.py test_prepared_property.py (with the T-202 files): 53 passed, 3 skipped in the archive",
  "staff panel mutant: drop `prepared = False` in present.py -> test_code_only_flags_are_not_prepared_on_the_curated_sample fails",
  "UX panel: origin/origin_label for f_r7_1 are lexicon / 'Found by code (phrase list)'; gap, accident-date and PT-plan conflict flags are origin code; the six flags with a prepared answer carry no label",
  "artifacts/gate-M3M4-suite-final.txt: unit 5945 passed, 0 failed"
 ],
 "verdict": "pass",
 "scores": {
  "ac_met_at_head": 5,
  "mutation_kill": 5,
  "label_true": 5
 },
 "findings": [
  {
   "severity": "minor",
   "title": "Gap flag `why` still says the second check agreed although no judge ran (same text as T-202 minor, accepted)",
   "evidence": "app/backend/present.py:10 OK_WHY; panel flag_probe f_gap_r6_r7 why with ladder.judge null. UI shows 'Not needed'.",
   "why_it_matters": "API field and UI row disagree about whether a second check ran.",
   "fix": "Use a code-only why for code-computed flags.",
   "acceptance_test": "unit test: f_gap_* why does not contain 'second check'."
  }
 ],
 "whats_right": [
  "prepared=false plus an origin label is derived from the item's real source, and a mutant that drops it fails a test.",
  "The guided panel and the API agree on which flags are code-found (only f_r7_1 from the phrase list, three code-made flags)."
 ],
 "questions_for_chris": []
}
```
