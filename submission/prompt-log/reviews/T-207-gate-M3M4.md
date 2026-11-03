# T-207 review, combined M3+M4 gate (D-075), staff-engineer-reviewer

Verdict: **pass**. HEAD a932fc9dcd627e0e5f92a234add6fc41b835a4f1.

LLM_VS_CODE rows 2-3 (date parsing, date of service and provider). After the D-073 fallback the rows describe the blank, the statement/record label and the bare blank, and match the code row by row per the staff panel. Row 19, which the panel had as a blocker, is fixed at HEAD. No blocker or major open.

Panel evidence used: reviews/GATE-M3M4-staff-engineer.md (f6d5c19), reviews/GATE-M3M4-verify-staff.md (43ce6eb), artifacts/gate-M3M4-suite-final.txt (43ce6eb: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0, spec check all true).

## Findings
1. **minor** Card AC evidence names f9c0faf/6b0724a (the allow-list wording); the rows were rewritten for D-073 later. Evidence: python3 tools/board.py show T-207 AC 1 evidence: 'rows 2-3 rewritten from service_date.py ... at f9c0faf; ... commit 6b0724a'; row 3 at HEAD describes the blank form, not an allow-list of positive evidence (the card title still says 'allow-list of positive evidence').

```json
{
 "card": "T-207",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git archive a932fc9: docs/LLM_VS_CODE.md rows 2, 3, 19; memory/contracts/api.md 574-575; export.charge_when; evals/letter_check.charge_date_violations",
 "exercised": [
  "git rev-parse HEAD = a932fc9 (docs-only on top of c2dd104); git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so the 43ce6eb unit/e2e runs still describe the app at HEAD",
  "python3 tools/board.py show <card> for the AC of this card",
  "read reviews/GATE-M3M4-{staff-engineer,ux-designer,paralegal,privacy-compliance,installer,product-manager}.md, GATE-M3M4-verify-staff.md, GATE-M3M4-verify-pm-r2.md and artifacts/gate-M3M4-suite-final.txt",
  "git archive a932fc9 into a scratchpad dir (arcC) for every check below, so the dirty main working tree was not read for product claims",
  "grep -c 'stated in these records' docs/LLM_VS_CODE.md = 0; grep -n TOTAL_PREFIX app/backend/export.py:36 = 'Billed charges accepted from these records: '; row 19 now says 'accepted from these records'",
  "grep -c 'Exactly two sources' memory/contracts/api.md = 0",
  "read row 3 text: blank form '(statement dated ...)' on a bill, '(record dated ...)' elsewhere, bare blank when undated, enforced by evals/letter_check.charge_date_violations",
  "python -m evals.letter_check: value 0, 25 cases (the enforcing test row 3 names)",
  "panel: GATE-M3M4-staff-engineer.md T-207 pass (row 2 and 3 vs code); verify-staff B1 fixed"
 ],
 "verdict": "pass",
 "scores": {
  "doc_matches_code_rows_2_3_19": 5,
  "cited_tests_exist": 4
 },
 "findings": [
  {
   "severity": "minor",
   "title": "Card AC evidence names f9c0faf/6b0724a (the allow-list wording); the rows were rewritten for D-073 later",
   "evidence": "python3 tools/board.py show T-207 AC 1 evidence: 'rows 2-3 rewritten from service_date.py ... at f9c0faf; ... commit 6b0724a'; row 3 at HEAD describes the blank form, not an allow-list of positive evidence (the card title still says 'allow-list of positive evidence').",
   "why_it_matters": "The card title and evidence describe a rule D-073 replaced; the rows themselves are right.",
   "fix": "Add a note on the card that D-073 (b50952d) superseded the allow-list wording and rows 2-3 were re-synced at 43ce6eb.",
   "acceptance_test": "board.py show T-207 notes mention D-073."
  }
 ],
 "whats_right": [
  "Rows 2, 3 and 19 now agree with export.py, the golden file and the downloaded letter; the two 'doc says something false' blockers from the f6d5c19 panel are gone.",
  "Row 3 names the independent scanner that enforces the rule, so the doc points at a test, not a promise."
 ],
 "questions_for_chris": []
}
```
