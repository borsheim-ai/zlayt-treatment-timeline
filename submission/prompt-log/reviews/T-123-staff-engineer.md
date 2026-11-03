# T-123 staff-engineer review (commit 0c47356)

Verdict: pass. The baseline sentence now uses the warn wording whenever any record on the earliest date is paperwork, in either order, and the bare questionnaire and authorization request headers count as paperwork. The change is code only and warning-only; it cannot add or hide a gap.

Exercised (archive of c26ff04, project venv):
- `pytest tests/unit -q`: 2816 passed, 4 skipped, which includes tests/unit/test_t123_baseline_same_day_paperwork.py and test_t116_gap_endpoints.py.
- Five mutants against test_t123: `any` changed to `all`, removing bare `questionnaires?`, removing `authorization request`, and dropping the alternative-visit extra are all killed. Replacing the paperwork-first provider ordering survives (see the minor finding).
- Read the diff in full. `admin_label` reads the header only, with a visit-word guard, and is used for warnings only. There is no LLM call and no float. The older test that asserted no warning was changed to the new reading, with a comment citing T-116 r5.

```json
{"card": "T-123", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive c26ff04: app/backend/conflicts.py, app/backend/gaps.py, tests/unit/test_t123_baseline_same_day_paperwork.py, tests/unit/test_t116_gap_endpoints.py",
 "exercised": ["pytest tests/unit -q on archive: 2816 passed, 4 skipped", "5 mutants on test_t123: 4 killed, 1 survived (provider ordering)", "read git show 0c47356 in full", "read gaps.admin_label and its callers"],
 "verdict": "pass",
 "scores": {"correctness": 4, "determinism": 5, "llm_code_boundary": 5, "test_quality": 4},
 "findings": [
  {"severity": "minor",
   "title": "Provider ordering in the same-day sentence is untested",
   "evidence": "app/backend/conflicts.py:73-76 `ordered = paper + [...]` feeds provider_a/provider_b. Mutant `ordered = list(first_recs)` SURVIVED all 21 tests in test_t123_baseline_same_day_paperwork.py. The tests assert the absence of 'first recorded treatment', the presence of 'looks like paperwork' and 'initial evaluation', but not which provider is named as the paperwork.",
   "why_it_matters": "The reorder exists so the paperwork record is named as paperwork when it is second in file order; nothing fails if it regresses.",
   "fix": "In test_same_day_paperwork_and_visit_never_call_the_paperwork_treatment, also assert the paperwork header appears in the sentence in both orders and is the one named with 'looks like paperwork'.",
   "acceptance_test": "The ordered=first_recs mutant must fail the paper_first=False case."}
 ],
 "whats_right": ["Warning-only: gap math and endpoints are untouched, so the fix cannot invent or hide a gap (D-055).", "Tests cover both record orders and six header spellings, including the faxed and parenthetical forms.", "The old test was updated to the new reading with a comment, not deleted."],
 "questions_for_chris": []}
```
