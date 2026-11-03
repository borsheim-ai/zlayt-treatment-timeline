# T-215 review, combined M3+M4 gate (D-075), staff-engineer-reviewer

Verdict: **pass**. HEAD a932fc9dcd627e0e5f92a234add6fc41b835a4f1.

Gate fix A (docs and spec): all three prior blockers (LLM_VS_CODE row 19, api.md charge-line date text, README `make evals` fourth blocker line) are fixed at 43ce6eb per the verify pass, and I re-checked them at HEAD. No blocker or major open. Two minors.

Panel evidence used: reviews/GATE-M3M4-staff-engineer.md (f6d5c19), reviews/GATE-M3M4-verify-staff.md (43ce6eb), artifacts/gate-M3M4-suite-final.txt (43ce6eb: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0, spec check all true).

## Findings
1. **minor** api.md:574 retained-reader sentence says a hand-built case without dos_iso keeps the old record-date line; the code always prints the blank. Evidence: memory/contracts/api.md:574 'a hand-built case without `dos_iso` keeps the old `<provider>, <record date>` line'; app/backend/export.py:210-215 charge_when ignores dos_iso; same paragraph says dos_* are ignored. grep -n 'keeps the old' memory/contracts/api.md at a932fc9 returns line 574 (GATE-M3M4-verify-staff.md minor 2).
2. **minor** `python -m evals.run --check-spec` rewrites the tracked evals/reports/latest.json, turning test_t045_r2 red until the file is reset. Evidence: GATE-M3M4-verify-staff.md minor 1: pristine archive pytest tests/unit/test_t045_r2.py 19 passed; after --check-spec 1 failed ('Left contains 2 more items: internal_notes_equal, letter_equal'). The final suite file ran check-spec in a second archive to avoid it (artifacts/gate-M3M4-suite-final.txt lines 3-4).

```json
{
 "card": "T-215",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git archive a932fc9: docs/LLM_VS_CODE.md row 19, memory/contracts/api.md 574-575, spec/REQUIREMENTS.md:260, evals/run.py --check-spec, evals/reports/latest.json",
 "exercised": [
  "git rev-parse HEAD = a932fc9 (docs-only on top of c2dd104); git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so the 43ce6eb unit/e2e runs still describe the app at HEAD",
  "python3 tools/board.py show <card> for the AC of this card",
  "read reviews/GATE-M3M4-{staff-engineer,ux-designer,paralegal,privacy-compliance,installer,product-manager}.md, GATE-M3M4-verify-staff.md, GATE-M3M4-verify-pm-r2.md and artifacts/gate-M3M4-suite-final.txt",
  "git archive a932fc9 into a scratchpad dir (arcC) for every check below, so the dirty main working tree was not read for product claims",
  "grep -c 'stated in these records' docs/LLM_VS_CODE.md = 0; grep -c 'Exactly two sources' memory/contracts/api.md = 0; export.py:36 TOTAL_PREFIX = 'Billed charges accepted from these records: '",
  "artifacts/gate-M3M4-suite-final.txt: spec {\"spec_matches_golden\": true, \"letter_equal\": true, \"internal_notes_equal\": true}; unit 5945 passed, 0 failed",
  "verify-staff: env -i make evals names exactly three blocker lines and leaves latest.json untouched; --check-spec exit 0 in clone and archive; spec/REQUIREMENTS.md:260 equals golden line 42",
  "grep -n 'keeps the old' memory/contracts/api.md at a932fc9: still 1 hit at line 574",
  "python -m evals.letter_check: value 0, 25 cases"
 ],
 "verdict": "pass",
 "scores": {
  "ac_met_at_head": 5,
  "doc_accuracy": 4,
  "side_effect_free_checks": 3
 },
 "findings": [
  {
   "severity": "minor",
   "title": "api.md:574 retained-reader sentence says a hand-built case without dos_iso keeps the old record-date line; the code always prints the blank",
   "evidence": "memory/contracts/api.md:574 'a hand-built case without `dos_iso` keeps the old `<provider>, <record date>` line'; app/backend/export.py:210-215 charge_when ignores dos_iso; same paragraph says dos_* are ignored. grep -n 'keeps the old' memory/contracts/api.md at a932fc9 returns line 574 (GATE-M3M4-verify-staff.md minor 2).",
   "why_it_matters": "Two sentences in one paragraph of the API contract disagree; the first is false for the code.",
   "fix": "Delete that clause from the retained-reader description.",
   "acceptance_test": "grep -c 'keeps the old' memory/contracts/api.md returns 0."
  },
  {
   "severity": "minor",
   "title": "`python -m evals.run --check-spec` rewrites the tracked evals/reports/latest.json, turning test_t045_r2 red until the file is reset",
   "evidence": "GATE-M3M4-verify-staff.md minor 1: pristine archive pytest tests/unit/test_t045_r2.py 19 passed; after --check-spec 1 failed ('Left contains 2 more items: internal_notes_equal, letter_equal'). The final suite file ran check-spec in a second archive to avoid it (artifacts/gate-M3M4-suite-final.txt lines 3-4).",
   "why_it_matters": "Anyone who runs the gate's own check then the suite sees a red that is not a product defect.",
   "fix": "Commit latest.json with the two keys, or make --check-spec write elsewhere.",
   "acceptance_test": "from a pristine archive: python -m evals.run --check-spec then pytest tests/unit/test_t045_r2.py passes."
  }
 ],
 "whats_right": [
  "Row 19, api.md and spec section 6 now say 'accepted from these records' and the fillable blank, matching export.py, the golden file and the downloaded letter.",
  "make evals names exactly the three expected blocker lines, as the README says."
 ],
 "questions_for_chris": []
}
```
