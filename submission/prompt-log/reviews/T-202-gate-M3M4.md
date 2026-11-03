# T-202 review, combined M3+M4 gate (D-075), staff-engineer-reviewer

Verdict: **pass**. HEAD a932fc9dcd627e0e5f92a234add6fc41b835a4f1.

D-071 letter charge dates, finished as the D-073 fallback (every charge line prints the fillable 'date of service [__________]' blank, no service date extracted). The staff, paralegal and PM panels all passed it; my own run of letter_check and the T-202 tests at HEAD agrees. No blocker or major open. Two minors.

Panel evidence used: reviews/GATE-M3M4-staff-engineer.md (f6d5c19), reviews/GATE-M3M4-verify-staff.md (43ce6eb), artifacts/gate-M3M4-suite-final.txt (43ce6eb: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0, spec check all true).

## Findings
1. **minor** Code-computed gap flag carries 'and the second check agreed' with no judge (SCOPE_CUTS, from the staff panel). Evidence: app/backend/present.py:10 OK_WHY = '... and the second check agreed.'; flags.py:45 and generator.py:171 use the same sentence as the no-reason fallback; panel flag_probe: f_gap_r6_r7 why carries it with ladder.judge null. Guided UI shows 'Not needed' for that row, so the demo is not affected.
2. **minor** Paralegal non-blockers on lib10 notes (gap 43 vs card 49 days, chronology line fragment 'room', CMS-1500 figures omitted from notes) are accepted debt. Evidence: reviews/GATE-M3M4-paralegal.md 'Not blockers' section; memory/SCOPE_CUTS.md row 29 (git show HEAD:memory/SCOPE_CUTS.md).

```json
{
 "card": "T-202",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git archive a932fc9; app/backend/export.py charge_when, service_date.py resolve, evals/letter_check.py, tests t202_r7/t200",
 "exercised": [
  "git rev-parse HEAD = a932fc9 (docs-only on top of c2dd104); git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so the 43ce6eb unit/e2e runs still describe the app at HEAD",
  "python3 tools/board.py show <card> for the AC of this card",
  "read reviews/GATE-M3M4-{staff-engineer,ux-designer,paralegal,privacy-compliance,installer,product-manager}.md, GATE-M3M4-verify-staff.md, GATE-M3M4-verify-pm-r2.md and artifacts/gate-M3M4-suite-final.txt",
  "git archive a932fc9 into a scratchpad dir (arcC) for every check below, so the dirty main working tree was not read for product claims",
  "python -m evals.letter_check (fixture backend, key unset) in the archive: {\"value\": 0, \"cases\": 25, \"held_out_entries\": 11}",
  "pytest tests/unit/test_t202_r7_all_blank.py test_flag_origin_t214.py test_prepared_property.py test_t200_undated_charge_label.py: 53 passed, 3 skipped",
  "python -m app.pipeline evals/golden/sample.txt twice, cmp: identical (3842 bytes)",
  "read artifacts/gate-M3M4-suite-final.txt: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter 0, spec check all true",
  "panel evidence: GATE-M3M4-staff-engineer.md mutants (charge_when prints record date: letter_check lists violations in lib13/14/15 and 6 tests fail; resolve returns raw read: 5 tests fail); paralegal lib10/lib11/case_09 hand sums; PM B1 over-claim fixed (note:25, Part 2:116)"
 ],
 "verdict": "pass",
 "scores": {
  "llm_code_boundary": 5,
  "determinism": 5,
  "mutation_kill": 5,
  "failure_visibility": 4
 },
 "findings": [
  {
   "severity": "minor",
   "title": "Code-computed gap flag carries 'and the second check agreed' with no judge (SCOPE_CUTS, from the staff panel)",
   "evidence": "app/backend/present.py:10 OK_WHY = '... and the second check agreed.'; flags.py:45 and generator.py:171 use the same sentence as the no-reason fallback; panel flag_probe: f_gap_r6_r7 why carries it with ladder.judge null. Guided UI shows 'Not needed' for that row, so the demo is not affected.",
   "why_it_matters": "An API field names a check that did not run; any surface printing item.why for a gap flag would mislead.",
   "fix": "Give code-computed flags a why that names only the code checks.",
   "acceptance_test": "a unit test asserts f_gap_* why does not contain 'second check'."
  },
  {
   "severity": "minor",
   "title": "Paralegal non-blockers on lib10 notes (gap 43 vs card 49 days, chronology line fragment 'room', CMS-1500 figures omitted from notes) are accepted debt",
   "evidence": "reviews/GATE-M3M4-paralegal.md 'Not blockers' section; memory/SCOPE_CUTS.md row 29 (git show HEAD:memory/SCOPE_CUTS.md).",
   "why_it_matters": "They are local-mode library cases, not the public sample, and the letter total is correct on all four cases the paralegal hand-summed.",
   "fix": "Post-MVP per row 29.",
   "acceptance_test": "lib10 notes line for the gap names the 49-day warning, or SCOPE_CUTS row 29 stays."
  }
 ],
 "whats_right": [
  "The blank is enforced twice (charge_when for the letter, an independent letter_check scanner over 25 cases), and the record-date mutant fails both.",
  "The letter total is $8,390.00 on the sample (6,240 + 2,150, the $185 rate excluded) and every paralegal hand sum matched."
 ],
 "questions_for_chris": []
}
```
