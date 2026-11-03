# T-055 round 2 security review: batch accept refuses non-verified entries (commit 670ed09)

Verdict: **pass**. Round-1 F1 (major) and F2 (minor) are closed; round-1 F3 (nit) is closed. One nit: the commit message and card evidence say the rule mutant fails 3 tests; it fails 2.

Lens: this review applies `personas/security.md` (security-reviewer) at the orchestrator's request, as the brief asks. The reviewer identity in this file is security-reviewer. Model recorded as `claude-haiku-5-5`, the model this session runs as.

## Pinning

- HEAD at review start: `373f8b1`. Commit under review: `670ed09`, an ancestor of HEAD.
- Reviewed code: `git archive 670ed09` at `artifacts/review-evidence/T-055-security-r2/head_670ed09`, with tracked fixtures only (no working-tree fixtures copied in).
- `git diff --stat 670ed09 HEAD -- app/backend/case_extras.py tests/unit/test_case_extras.py` is empty: the batch code and its tests are unchanged since 670ed09.

## Round-1 findings: status

- **F1 (major), AC1 test does not exercise needs_review: closed.** `tests/unit/test_case_extras.py` at 670ed09 now parametrizes `test_batch_refuses_a_non_verified_entry_with_not_verified_and_changes_nothing` over `["needs_review", "rejected"]`. The fixture sets one entry's state with `DB.update_item(conn, odd, now=0, case=tok, state=state)`, asserts the state held, then posts `rest + [odd]` (four verified pending entries plus the odd one). It asserts `422`, `error.code == "invalid_batch"`, `detail.rejected == [{"id": odd, "reason": "not_verified"}]`, store statuses unchanged, and the event list unchanged.
- **F2 (minor), rejected branch not covered: closed.** The `rejected` parameter now runs (no skip). Verified in the collected output: `test_batch_refuses_a_non_verified_entry_with_not_verified_and_changes_nothing[needs_review]` and `[rejected]` both pass at 670ed09.
- **F3 (nit), unused `before` variable: closed.** `git show 670ed09 -- app/backend/case_extras.py` removes `before = {...}`. The archived file (`artifacts/review-evidence/T-055-security-r2/case_extras_670ed09.py.txt`) has no `before` line.

Server rule (unchanged, `case_extras.py:35-36` at 670ed09): `elif action == "accept" and row["state"] != "verified": bad.append({"id": i, "reason": "not_verified"})`.

## Mutation check (scratch copies, not committed)

Output: `artifacts/review-evidence/T-055-security-r2/mutants.out.txt`.

- Drop the whole `not_verified` rule (`elif False:`): 2 failed, both new state tests (`[needs_review]`, `[rejected]`).
- Keep only the needs_review branch: 1 failed (`[rejected]`).
- Keep only the rejected branch: 1 failed (`[needs_review]`).

So each state is pinned by its own test. A regression that lets needs_review or rejected entries through fails the suite.

## Findings

- **nit, the rule-mutant count in the commit message and card evidence is 2, not 3.** Evidence: the commit `670ed09` message says "Mutant 'drop the not_verified rule' now fails 3 tests", and the card's AC1 evidence says "mutant dropping case_extras.py not_verified rule fails 3 tests". Reproduced: `artifacts/review-evidence/T-055-security-r2/full_unit_670ed09_drop_rule_mutant.out.txt` reads `2 failed, 902 passed`, and the baseline `full_unit_670ed09_baseline.out.txt` reads `904 passed`. The two failures are the two new state tests. Why it matters: the protection is correct; the evidence count overstates it, and a future reader may look for a third test that does not exist. Fix: correct the count in the card's AC1 evidence note (a note, not a code change). Acceptance: the card note and the commit-level claim match the 2 failures above.

## AC status

- AC1 (API rejects batch accept containing amounts, flags or needs_review items, 422, test): met at 670ed09. Amount and flag ids are covered by `test_batch_refuses_amounts_flags_and_unverified_and_applies_nothing` (passes); needs_review and rejected by the parametrized test above.
- Round-1 open question 2 (HEAD cannot run `test_case_extras.py` on its own): at 670ed09 the full `tests/unit` suite passes from a tracked-only archive (904 passed, no working-tree fixtures copied). The reproducibility gap does not show at this commit.

## Exercised

Working directory `/Users/arsis/zlayt-pm-project` unless stated.

- Read `personas/security.md` in full and `reviews/T-055-security.md` in full (round-1 F1, F2, F3 and the questions).
- `.venv/bin/python tools/board.py show T-055`: `status: "in_review"`, `commits: ["a79358c", "dbb2c66", "709397e", "670ed09"]`, AC1 `done: true`.
- `git show --stat 670ed09` (2 files: `app/backend/case_extras.py`, `tests/unit/test_case_extras.py`); `git show 670ed09 -- app/backend/case_extras.py`; `git show 670ed09:app/backend/case_extras.py` saved to `case_extras_670ed09.py.txt`; `_check` at lines 24-39 read.
- `git archive 670ed09 | tar -x -C artifacts/review-evidence/T-055-security-r2/head_670ed09`.
- `.venv/bin/python -m pytest tests/unit/test_case_extras.py -q -p no:cacheprovider -v` in the archive: 13 passed.
- `.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider` in the archive: 904 passed (`full_unit_670ed09_baseline.out.txt`).
- Mutants on scratch copies: `mutate_t055.py` (drop rule; only needs_review; only rejected), output in `mutants.out.txt`.
- Full `tests/unit` with the drop-rule mutant: 2 failed, 902 passed (`full_unit_670ed09_drop_rule_mutant.out.txt`).
- `git diff --stat 670ed09 HEAD -- app/backend/case_extras.py tests/unit/test_case_extras.py`: empty.

Not exercised: concurrent batch versus single-item review (the single-item path does not take `_LOCK`; not raced in this round, as in r1); live :7860; the batch UI.

## Machine-readable record

```json
{"card": "T-055", "persona": "security-reviewer", "model": "claude-haiku-5-5",
 "scope": "Round 2 of T-055 at commit 670ed09: app/backend/case_extras.py (apply_batch, _check not_verified rule at lines 35-36) and tests/unit/test_case_extras.py (parametrized needs_review and rejected refusal). Pinned at git archive 670ed09 (artifacts/review-evidence/T-055-security-r2/head_670ed09), tracked fixtures only. HEAD 373f8b1: no change to these files since 670ed09. In-process TestClient; no app URL.",
 "exercised": [
  "read personas/security.md and reviews/T-055-security.md in full",
  "board.py show T-055 (in_review; AC1 done true; commits incl. 670ed09)",
  "git show --stat 670ed09; git show 670ed09 -- app/backend/case_extras.py; git show 670ed09:app/backend/case_extras.py; _check lines 24-39 read",
  "git archive 670ed09 extracted to artifacts/review-evidence/T-055-security-r2/head_670ed09",
  "pytest tests/unit/test_case_extras.py -q -v in the archive: 13 passed (needs_review and rejected cases both run, no skip)",
  "pytest tests/unit -q in the archive: 904 passed",
  "mutants on scratch copies: drop whole not_verified rule -> 2 failed (needs_review, rejected); only needs_review -> 1 failed (rejected); only rejected -> 1 failed (needs_review) (mutants.out.txt)",
  "full tests/unit with drop-rule mutant: 2 failed, 902 passed (full_unit_670ed09_drop_rule_mutant.out.txt)",
  "git diff --stat 670ed09 HEAD over the two files: empty",
  "not exercised: concurrent batch vs single-item race, live :7860, batch UI"],
 "verdict": "pass",
 "scores": {"needs_review_refused_by_test": 5, "rejected_refused_by_test": 5, "rule_mutant_killed_per_state": 5, "card_evidence_accuracy": 3},
 "findings": [
  {"severity": "nit", "title": "Commit 670ed09 message and card AC1 evidence say the rule mutant fails 3 tests; it fails 2",
   "evidence": "git show -s 670ed09 message: \"Mutant 'drop the not_verified rule' now fails 3 tests\". Reproduced: artifacts/review-evidence/T-055-security-r2/full_unit_670ed09_drop_rule_mutant.out.txt = '2 failed, 902 passed'; full_unit_670ed09_baseline.out.txt = '904 passed'; the two failures are test_batch_refuses_a_non_verified_entry_with_not_verified_and_changes_nothing[needs_review] and [rejected].",
   "why_it_matters": "The protection is correct. The overstated count would send a future reader to look for a third test that does not exist.",
   "fix": "Correct the count to 2 in the card's AC1 evidence note. No code change.",
   "acceptance_test": "The card note matches the 2 failures listed above."}
 ],
 "whats_right": [
  "The batch test now sends a needs_review and a rejected id with a verified id and asserts 422 invalid_batch, rejected == [{id, not_verified}], unchanged statuses and no events.",
  "Each state is pinned on its own: dropping the rule fails both state tests; keeping only one branch fails the other (mutants.out.txt).",
  "The unused before variable is removed, and the full tests/unit suite passes from a tracked-only archive at 670ed09 (904 passed), so the round-1 fixture-reproducibility gap does not show at this commit."
 ],
 "questions_for_chris": [
  "Round-1 question carried over: should the sample case include one needs_review and one rejected entry, so these tests do not inject state with DB.update_item? Not a finding in this round."
 ]}
```
