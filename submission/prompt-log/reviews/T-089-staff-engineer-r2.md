# T-089 round-2 review: dismissal-pattern suggestions (staff-engineer-reviewer)

**Verdict: pass.** No blocker and no major. Both round-1 majors are closed: the route-level demo-isolation tests fail when the route is forced to local or public scope, and the card files are no longer staged for deletion. Three minors remain: one eligibility rule still has no failing test, the golden identity test's comment does not match what it seeds, and the handoff's "(160 pass)" does not reproduce at the commit. The brief asked for the minors to be fixed; two of the four round-1 minors are closed and one is partly closed, and the new minor comes from the round-2 test rewrite.

Scope: commit 55300e9 (round 2) on top of f667f08. HEAD moved during the review (d3130e3, then 7df65fb, a T-093 commit); I pinned the tree at 7df65fb. The card paths are byte-identical between 55300e9 and 7df65fb. The route wiring at `app/backend/api.py:513` is unchanged.

**Round-1 items**

| Round-1 item | Status | Evidence |
|---|---|---|
| Major: route forced to local passes all tests (89h) | Closed | `mutation_run_r2.txt`: "MUTANT 89h ROUTE forces local scope ... -> CAUGHT :: 1 failed" (`test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route`); 89h2 (route forced public) also CAUGHT by `test_local_mode_counts_the_machine_profile_through_the_route` |
| Major: shared index stages deletion of card files | Closed for these four paths | `git diff --cached --name-status -- <4 paths>` prints nothing |
| Minor: eligibility rules tested only as a conjunction | Partly closed | 89d2 (origin rule) CAUGHT by `test_eligibility_rules_are_each_enforced_on_their_own`; 89d (type rule) still NOT CAUGHT (F1) |
| Minor: category boundary and golden identity sensitivity | Closed for the stated acceptance; comment wrong (F2) | 89b CAUGHT by `test_category_threshold_is_exactly_five`; 89i CAUGHT on case_06, case_07, case_08 and sample (not only sample) |
| Minor: banner not built | Closed by tracking | T-096 AC: "dismissal suggestion banner with Hide-similar action that the paralegal must click (T-089)" |
| Nit: apply not atomic | Closed by documenting | `memory/contracts/api.md:284` now says "The apply is not one transaction: each flag is dismissed and logged on its own, so a failure partway leaves the earlier flags dismissed" (the round-1 fix allowed documenting) |

**Your checks**
1. Route-level isolation: the tests fail when the route is forced. Mutant 89h (`app/backend/api.py:513`, `local_mode=lambda: True`) fails `test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route`. Mutant 89h2 (forced public) fails `test_local_mode_counts_the_machine_profile_through_the_route`. Both are in the scratch copy; the repo was not edited.
2. Minors: 89b, 89d2 and 89i are caught; 89d is not (F1). The golden identity test is sensitive on four of ten cases (F2).
3. Sanity: suggest() is still read-only (89e caught by 7 tests), the GET does not apply (89f caught), bulk-applied flags are not counted (89c caught), and history is scoped to the case in public mode (89g caught).

**Findings**
- **F1 (minor, open).** The gap-type eligibility rule has no failing test. Mutant 89d (gap added to ELIGIBLE_TYPES) gives 30 passed. Adding one pending gap flag to the existing eligibility test makes 89d fail (`experiments_r2_output.txt`, EXP_A). Fix: add that flag and assert `suggest() == []`.
- **F2 (minor, new in round 2).** `tests/unit/test_dismissal_patterns.py:164` seeds `history_from * 8 or [None]`. When a case has no eligible flag, that is `[None]`, one dismissal, not the 8 the docstring states. One dismissal is below PHRASE_MIN, so six of ten golden cases (case_01 to case_05 and case_09) have no sensitivity to history (`experiments_r2_output.txt`, EXP_B: `history_rows_seeded=1`). The pipeline does not read history today, so there is no output change; this is a test-strength and comment-accuracy gap.
- **F3 (minor).** The handoff's "(160 pass)" does not reproduce at the commit. At 7df65fb the selector gives 140 passed; the extra passes come from uncommitted tests in other cards. `tests/unit/test_dismissal_patterns.py` alone gives 21 passed in both trees.

**Exercised** (all run by me; exact outputs in the files named)
- `python3 tools/board.py show T-089`, `show T-096`, `list --role qa`.
- `git show 55300e9` for `tests/unit/test_dismissal_patterns.py` and `memory/contracts/api.md` (full diff read); `git diff 55300e9 7df65fb` for the card paths (empty).
- `.venv/bin/python -m pytest -q tests/unit -k "date or dismiss or suggest"`: clean HEAD **140 passed, 1196 deselected**; dirty main tree **160 passed, 1238 deselected**.
- `pytest tests/unit/test_dismissal_patterns.py` (clean HEAD): **21 passed**.
- `pytest tests/unit` (clean HEAD): **6 failed, 1330 passed**; the same 6 fail at 55300e9. None touches these cards. Outside these cards; see below.
- `mutate_r2.py` on a scratch copy (`mutation_run_r2.txt`): 89a, 89b, 89c, 89d, 89d2, 89e, 89f, 89g, 89h, 89h2, 89i run; baseline and restored both 30 passed.
- `experiments_r2.py` on the scratch copy (`experiments_r2_output.txt`): EXP_A (pending gap flag with mutant 89d: CAUGHT); EXP_B (history rows seeded per golden case).
- `python3 -c "print([] * 8 or [None])"` → `[None]`.
- `git diff --cached --name-status -- <4 card paths>` (empty); `grep -rn dismissal app/frontend` (0).

**Process note.** `git worktree add` was refused by the board-guard (reviewers may not run `git worktree` in the project). I pinned the same tree with `git archive` into `artifacts/review-evidence/T-088-T-089-r2/clean`.

**Outside these cards (not findings on T-089)**
- Clean HEAD has 6 failing unit tests (`test_trace.py` x4, `test_t075_determinism.py`, `test_t037_backend.py`); the same 6 fail at 55300e9. The dirty main tree has 21 failures from in-progress work.
- The shared index currently stages deletions of other cards' paths (`evals/reports/controls-20261102T042306Z.*`, `evals/golden/judge_controls_heldout.jsonl`, `.claude/agent-memory/qa/project_judge_controls.md`). That is the round-1 F3 hazard, for T-093's paths.

```json
{"card": "T-089", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 2, commit 55300e9 (tests/unit/test_dismissal_patterns.py; api.md T-089 section; app/backend/api.py:513 route wiring unchanged); pinned tree HEAD 7df65fb via git archive at artifacts/review-evidence/T-088-T-089-r2/clean (card paths unchanged 55300e9..7df65fb); golden evals/golden/*.txt via G.case_names(); no live app URL (TestClient in-process)",
 "exercised": ["python3 tools/board.py show T-089, show T-096, list --role qa", "git show 55300e9 -- tests/unit/test_dismissal_patterns.py and memory/contracts/api.md (full diff read)", "git diff 55300e9 7df65fb for the card paths (empty)", ".venv/bin/python -m pytest -q tests/unit -k 'date or dismiss or suggest' in clean HEAD: 140 passed, 1196 deselected; dirty main tree: 160 passed, 1238 deselected", "pytest tests/unit/test_dismissal_patterns.py in clean HEAD: 21 passed", "pytest tests/unit in clean HEAD: 6 failed, 1330 passed (none in card files; the same 6 fail at 55300e9)", "mutate_r2.py on a scratch copy (artifacts/review-evidence/T-088-T-089-r2/mutation_run_r2.txt): 89a, 89b, 89c, 89d, 89d2, 89e, 89f, 89g, 89h, 89h2, 89i", "experiments_r2.py on the scratch copy (experiments_r2_output.txt): EXP_A pending gap flag with mutant 89d; EXP_B history rows seeded per golden case", "python3 -c 'print([] * 8 or [None])' → [None] (one history row)", "git diff --cached --name-status -- the four card paths (empty); grep -rn 'dismissal' app/frontend (0)"],
 "verdict": "pass",
 "scores": {"never_auto_dismiss": 5, "no_pipeline_or_recall_effect": 4, "local_only_no_identity": 4, "demo_isolation_tested": 5, "tests_fail_on_mutation": 4, "ac_integrity": 4},
 "findings": [
  {"severity": "minor",
   "title": "The gap-type eligibility rule still has no test that fails when it is removed",
   "evidence": "artifacts/review-evidence/T-088-T-089-r2/mutation_run_r2.txt: 'MUTANT 89d gap type made eligible ... -> NOT CAUGHT :: 30 passed'. tests/unit/test_dismissal_patterns.py:185-194 (test_eligibility_rules_are_each_enforced_on_their_own) has the 6 gap dismissals but no pending gap flag, so no category suggestion can be offered for them. experiments_r2_output.txt: 'EXP_A mutant 89d with pending gap flag: CAUGHT' after a pending gap flag is added in the scratch copy.",
   "why_it_matters": "The AC says ineligible types are never offered. The type rule (ELIGIBLE_TYPES, app/backend/dismissal_patterns.py:22) can be widened to gap flags without any test failing, which is the round-1 minor left open. The origin rule (89d2) is now caught.",
   "fix": "In test_eligibility_rules_are_each_enforced_on_their_own, after the 6-dismissal history, add a pending flag with category gap_over_30, type gap, origin lexicon+llm and status None, then assert DP.suggest(conn, cid) == [] for it.",
   "acceptance_test": "Mutant 89d (ELIGIBLE_TYPES includes gap) fails test_eligibility_rules_are_each_enforced_on_their_own; the unmutated file passes."},
  {"severity": "minor",
   "title": "The golden identity test's comment says 8 generic dismissals; the code seeds 1, so six of ten golden cases are not history-sensitive",
   "evidence": "tests/unit/test_dismissal_patterns.py:164 'for n, f in enumerate(history_from * 8 or [None]):'. With no eligible flag, history_from is [], [] * 8 is [], and the expression gives [None] (python3 -c \"print([] * 8 or [None])\" → [None]). The docstring at lines 157-159 says 'the generic new_onset history' of 8 dismissals. experiments_r2_output.txt 'EXPB' lines: history_rows_seeded=1 for case_01, case_02, case_03, case_04, case_05 and case_09 (eligible_flags=0); 8, 24 or 56 rows for the cases that have eligible flags. Mutant 89i is caught only on case_06, case_07, case_08 and sample.",
   "why_it_matters": "One dismissal is below PHRASE_MIN=3, so the 'generic' history cannot change any output, and a history-fed pipeline would pass the identity test on six of ten cases. The pipeline does not read history today (no output change), so this is a test-strength gap, not a live recall loss. Round 1 asked for per-case sensitivity; that is met for the four cases with eligible flags only.",
   "fix": "Seed the generic history with 8 rows: change line 164 to 'for n, f in enumerate((history_from or [None]) * 8):'. Then the docstring is true. Note in the docstring that the six cases with no eligible flag are covered only through the generic new_onset history.",
   "acceptance_test": "A test asserts that each golden case seeds 8 history rows; mutant 89i fails for every golden case that has a new_onset flag in its pipeline output, not only for case_06, case_07, case_08 and sample."},
  {"severity": "minor",
   "title": "The handoff's '(160 pass)' does not reproduce at the commit",
   "evidence": "T-089 handoff: \"pytest -k 'date or dismiss or suggest' (160 pass)\". Clean HEAD: '140 passed, 1196 deselected'. Dirty main tree: '160 passed, 1238 deselected'; the extra passes come from uncommitted tests in other cards. tests/unit/test_dismissal_patterns.py alone: 21 passed in both trees.",
   "why_it_matters": "The quoted number cannot be reproduced at the commit, so the evidence in the handoff is not checkable from git.",
   "fix": "Quote the card's own file: pytest tests/unit/test_dismissal_patterns.py (21 passed), or the selector count from a clean checkout of the commit.",
   "acceptance_test": "Extract the commit with git archive, run the quoted command there, and check that the quoted number equals the output."}
 ],
 "whats_right": ["Route wiring is now tested in both directions: forcing local scope (mutant 89h, api.py:513) fails test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route, and forcing public scope (89h2) fails test_local_mode_counts_the_machine_profile_through_the_route.", "The golden identity test now fails for a history-fed pipeline (89i) on case_06, case_07, case_08 and sample, not only on the sample, which meets the round-1 acceptance item.", "The category threshold boundary (89b, CATEGORY_MIN 4 vs 5) and the origin rule (89d2) now fail named tests; the apply partial-write behaviour is documented in api.md; the banner is tracked on T-096."],
 "questions_for_chris": ["Round-1 question, still open: in local mode the suggestion counts dismissals across every case on the machine. Is that the intended single-profile scope, or should counts stay per case until a profile concept exists?"]}
```
