# T-089 review: dismissal-pattern suggestions (staff-engineer-reviewer)

**Verdict: changes.** No blocker. The core rules hold: nothing is auto-dismissed, the GET is read-only, bulk-applied flags never feed back into the count, the pipeline does not read the history, and storage adds no identity. Two majors and one minor-level test gap need fixing before the gate. The majors are the demo-isolation test gap (F1) and the shared git index that stages deletion of this card's files (F3). Suggestions only, no auto-dismiss, and no change to pipeline output or golden recall are all verified, not assumed.

Scope: commit f667f08 (`app/backend/dismissal_patterns.py`, `app/backend/api.py:497`, `tests/unit/test_dismissal_patterns.py`, the T-089 contract section in `memory/contracts/api.md`). Checked against D-042 in `memory/ORCHESTRATOR_DECISIONS.md` line 50.

**Checks against your three points**
1. Nothing auto-dismissed: holds. `suggest()` (`dismissal_patterns.py:51-72`) only reads. The GET route (`:92-99`) does not call `apply`. The POST route (`:101-114`) is the only writer, and it needs a key. Mutants 89e (suggest writes) and 89f (GET auto-applies) are both caught.
2. No effect on pipeline output or golden recall: holds. `pipeline.py` does not import `dismissal_patterns`. The golden identity test (`test_dismissal_patterns.py:116-134`) passes, and mutant 89i (history filters pipeline flags) is caught. Sensitivity is limited, see F4.
3. Storage local only, no user identity: holds. The module reads the existing `flags` table with no new column, table, or identity field. `grep -n "user|email|identity|account"` on the module returns only the docstring that says there are no users. Scope is case-only unless `ZLAYT_MODE=local`, mutant 89g is caught.

**Exercised**
- `python3 tools/board.py show T-089`; `git show f667f08` (stat and per-file); `git show f667f08:<path>` for in-scope files; D-042 in `memory/ORCHESTRATOR_DECISIONS.md`.
- `.venv/bin/python -m pytest -q tests/unit -k "date or dismiss or suggest"`: 151 passed, 1106 deselected. `pytest tests/unit/test_dismissal_patterns.py -v`: 17 passed (of 25 across both cards).
- Mutation suite in scratch copy `artifacts/review-evidence/T-088-T-089/mut` (runner `mutate.py`, output `mutation_run.txt`): 89a, 89c, 89e, 89f, 89g, 89i caught; 89b, 89d, 89d2, 89h not caught (see findings).
- `git diff --cached --name-status`; `git cat-file -e HEAD:<path>` (F3).
- `grep -rn dismissal app/frontend`: 0 matches (no banner built yet).

```json
{"card": "T-089", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f667f08: app/backend/dismissal_patterns.py, app/backend/api.py:497 (route registration), tests/unit/test_dismissal_patterns.py, memory/contracts/api.md (T-089 section); golden evals/golden/*.txt via G.case_names(); no live app URL (TestClient in-process)",
 "exercised": ["board.py show T-089 and T-088", "git show f667f08 --stat and per-file diffs", "git show f667f08:<path> for in-scope files", "memory/ORCHESTRATOR_DECISIONS.md D-042", "pytest -q tests/unit -k 'date or dismiss or suggest' (151 passed, 1106 deselected)", "pytest tests/unit/test_dismissal_patterns.py -v (17 passed)", "mutation suite 89a-89i incl. 89d2 in scratch copy (artifacts/review-evidence/T-088-T-089/mutation_run.txt)", "git diff --cached --name-status; git cat-file -e HEAD:<path>", "grep -rn dismissal app/frontend (0)", "grep for pipeline imports of dismissal_patterns (none)"],
 "verdict": "changes",
 "scores": {"never_auto_dismiss": 5, "no_pipeline_or_recall_effect": 4, "local_only_no_identity": 4, "demo_isolation_tested": 2, "tests_fail_on_mutation": 3, "ac_integrity": 3},
 "findings": [
  {"severity": "major",
   "title": "Demo-mode isolation at the route is not tested; forcing local scope in the route passes all 25 tests",
   "evidence": "app/backend/api.py:497 registers the route with local_mode=local_mode. Mutant 89h replaces it with local_mode=lambda: True in the scratch copy: '25 passed' (artifacts/review-evidence/T-088-T-089/mutation_run.txt, line 'MUTANT 89h ... NOT CAUGHT'). tests/unit/test_dismissal_patterns.py:94-113 (test_routes_and_demo_mode_isolation) creates one case only and seeds history in that case, so it cannot tell local from non-local scope. The unit test at :84-91 tests the function with local=True/False, not the route. memory/contracts/api.md (T-089 section) says 'a public/demo token never sees another case's dismissals'; the test named 'demo-mode isolation' does not assert that.",
   "why_it_matters": "The suggestion message counts dismissals in other cases ('all cases on this computer'). If the route's scope regresses, a public demo token would see phrase counts from other cases. The data is synthetic and the counts carry little content, so this is a test-coverage gap, not a live leak; the code today is correct. Depth on exposure belongs to security-reviewer. The card's AC evidence names a demo-isolation test that does not test isolation.",
   "fix": "Add a route test: create case A with 3 dismissals of a phrase and case B with the pending match, run without ZLAYT_MODE, and assert GET /api/cases/B/dismissal_suggestions returns suggestions == []. Then run with ZLAYT_MODE=local and assert the suggestion appears. Rename the test to describe what it asserts.",
   "acceptance_test": "Mutant 89h (local_mode forced True in api.py:497) must fail the new test. The unmodified route must pass it."},
  {"severity": "major",
   "title": "Shared git index stages deletion of this card's files (blast radius: T-088 and T-089)",
   "evidence": "git diff --cached --name-status: 'D app/backend/dismissal_patterns.py' and 'D tests/unit/test_dismissal_patterns.py' (plus the T-088 files and app/llm/prompts/conflicts_v1.md). git cat-file -e HEAD:app/backend/dismissal_patterns.py succeeds and the on-disk file matches HEAD (git show f667f08:<path> | diff: no output).",
   "why_it_matters": "HEAD is intact, so f667f08 itself is fine. The next commit made from this index deletes the T-089 module, its routes' code path and its tests, which is a silent loss of the deliverable.",
   "fix": "Orchestrator restores the index for these paths without touching the working tree, then commits with explicit paths. The reviewer does not run git reset.",
   "acceptance_test": "git diff --cached --name-status -- app/backend/dismissal_patterns.py tests/unit/test_dismissal_patterns.py prints nothing."},
  {"severity": "minor",
   "title": "Eligibility rules are tested only as a conjunction; neither the type rule nor the origin rule is isolated",
   "evidence": "app/backend/dismissal_patterns.py:22 (ELIGIBLE_TYPES) and :28 (origin must contain 'lexicon'). tests/unit/test_dismissal_patterns.py:49-50 builds the gap and record_warning flags with origin='code', so the origin check alone excludes them. Mutant 89d (gap added to ELIGIBLE_TYPES) and mutant 89d2 (origin requirement removed) both give '25 passed' (mutation_run.txt).",
   "why_it_matters": "The AC says 'ineligible types never offered'. Today a lexicon-origin gap flag would be offered for hiding if the type list were widened, and no test would notice.",
   "fix": "Add cases: a gap flag and a record_warning flag with origin 'lexicon+llm' (must not be suggested); a pre_existing flag with origin 'llm' only (must not be suggested).",
   "acceptance_test": "Mutants 89d and 89d2 must each fail a test."},
  {"severity": "minor",
   "title": "Category threshold boundary (CATEGORY_MIN) has no negative test; golden identity test seeds only one category",
   "evidence": "app/backend/dismissal_patterns.py:21 CATEGORY_MIN = 5. The category test (tests/unit/test_dismissal_patterns.py:54-63) only asserts the positive case at 5. Mutant 89b (CATEGORY_MIN = 4) gives '25 passed'. Also tests/unit/test_dismissal_patterns.py:15 defaults the seeded history to category 'new_onset'. Mutant 89i fails only the [sample] parametrization of the golden identity test (mutation_run.txt), so the other nine golden cases are not sensitive to history at all.",
   "why_it_matters": "The AC claim 'pipeline output identical on all golden cases with and without history' is true, but the test can only detect pipeline influence on flags of category new_onset. For the other nine cases it is a vacuous equality. The AC item also says 'eval shows no recall loss', and no eval report path exists; this unit equivalence test is the only evidence.",
   "fix": "Add a 4-dismissal negative case for the category rule. In the golden identity test, seed history with each case's own flag categories and phrases (taken from its pipeline output) so the equality is sensitive per case. Name the unit test as the recall evidence in the card, or add an eval report.",
   "acceptance_test": "Mutants 89b and 89i must each fail on at least one golden case other than sample."},
  {"severity": "minor",
   "title": "AC 'surface as a suggestion' is evidenced only by the API payload; the banner is not built",
   "evidence": "board show T-089, AC 1 done=true. Handoff: 'Left: frontend banner'. grep -rn dismissal app/frontend: 0 matches. The AC text does not name a UI element, so the API payload is the AC's surface.",
   "why_it_matters": "Acceptable for this AC as written, but the card's notes ask the frontend to show a banner with two buttons, and nothing in the card records that as a later AC. The surfacing will be lost unless a follow-up card tracks it.",
   "fix": "Create a follow-up frontend card for the banner, or add the banner to this card's AC before closing it.",
   "acceptance_test": "A UI test shows the banner after three dismissals, and flags stay unchanged until the 'Hide similar' click."},
  {"severity": "nit",
   "title": "apply() is not atomic across flags",
   "evidence": "app/backend/dismissal_patterns.py:86-87: the loop calls review.apply_review once per flag id with no transaction. A failure partway leaves earlier flags dismissed. Not reproduced; the flag ids come from pending flags and no test exercises a mid-loop failure.",
   "why_it_matters": "Low risk because each dismissal is individually logged and reversible with reset. Still a partial write with no explicit response.",
   "fix": "Wrap the loop in one transaction, or document the partial-write behaviour in api.md.",
   "acceptance_test": "A test that forces apply_review to raise on the second flag and asserts the first flag is not dismissed."}
 ],
 "whats_right": [
  "The GET path is read-only (mutant 89e, which writes on read, fails four tests; mutant 89f, which auto-applies on GET, fails the route test).",
  "Bulk-applied flags carry APPLIED_NOTE and are excluded from the count (dismissal_patterns.py:44); mutant 89c, which counts them, fails the self-reinforcement test.",
  "The pipeline does not import the module, and the history can change no pipeline output (mutant 89i is caught by the golden identity test)."
 ],
 "questions_for_chris": ["In local mode the suggestion counts dismissals across every case on the machine. Is that the intended single-profile scope, or should counts stay per case until a profile concept exists?"]}
```
