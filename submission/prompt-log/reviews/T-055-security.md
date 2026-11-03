# T-055 security review (security-reviewer, Tomás Rivas lens): batch accept

Verdict: **changes**. No blocker. One major: the card's own AC1 test does not exercise the needs_review refusal that AC1 names. The server rule itself holds; my probe proves it. Batch accept is entries-only, all-or-nothing, and cross-item safe (my tests).

Model recorded as `claude-haiku-5-5`, the model this session runs as.

## Commit pinning

HEAD moved during the review (d796383 when I pinned, then a27b358, bee1844, fa8a36e, 08764e7 now). The batch code is `app/backend/case_extras.py`, `app/backend/review.py` and the route in `case_extras.add_routes`. None of those changed between d796383 and 08764e7 (`git diff --stat d796383 HEAD -- app/backend/case_extras.py app/backend/review.py app/backend/store.py` empty). The reviewed code is `git archive d796383` at `artifacts/review-evidence/T-055-security/head_d796383`. The fixture set was copied from the working tree (see exercised).

## AC1 status

`python3 tools/board.py show T-055` shows AC1 "API rejects batch accept containing amounts, flags or needs_review items (422, test)" with `done: false`. My evidence for AC1:

- Amount id or flag id in a batch: 422 `invalid_batch`, `rejected == {id: "not_an_entry"}`, store and events unchanged. Passes (two parametrised tests).
- needs_review entry in a batch: 422 `invalid_batch`, `rejected == {id: "not_verified"}`, store unchanged. Passes, but only because I set the state through `DB.update_item`. The sample has no needs_review entry (see finding 1).
- Amount plus flag in one batch: both reported, nothing applied. Passes.
- Reset containing an amount or flag: 422, nothing applied. Passes.

## Findings

Finding 1 is the only one that changes the verdict.

- **major, the AC1 test does not cover needs_review.** `tests/unit/test_case_extras.py:57` is `nonver = [i for i, (rs, s) in st["entry"].items() if s != "verified"]` and `:59` is `bad = [amount, flag] + nonver[:1]`. In the sample, every entry is verified and pending, so `nonver` is empty and the needs_review branch is never sent. Evidence, run at d796383 with the sample case: `[('verified', 'pending')]` for the entries of both cases, and the ids `['e1', 'e2', ..., 'e9']` (`artifacts/review-evidence/T-055-security/probe_states.py`). The server rule is at `app/backend/case_extras.py:35-36` (`elif action == "accept" and row["state"] != "verified": bad.append({"id": i, "reason": "not_verified"})`). My test covers it and passes. A regression that dropped that line would still pass the card's suite. Fix: add the needs_review case to `test_case_extras.py`, setting one entry's state with `DB.update_item` as in my probe or with a fixture that has one. Acceptance: `tests/unit/test_r2_batch_security.py::test_needs_review_entry_gives_422_not_verified_and_nothing_changes` passes at d796383 and fails when `case_extras.py:35` is removed.
- **minor, the rejected branch is not covered.** The sample has no rejected entry, so `test_rejected_entry_gives_422_and_nothing_changes` skips (`1 skipped` in the run). Same fix idea as finding 1.
- **nit, dead variable.** `app/backend/case_extras.py:52` computes `before` and never reads it.

Things I checked and found fine (not findings): cross-case ids resolve inside the caller's case (`review.py:33` returns 404, which the batch reports as `not_found`); item ids are per case (`e1`..`e9` in both sample cases), so the same id in another case is never touched (my test `test_same_item_ids_in_another_case_are_never_touched` passes); malformed bodies return 400 `bad_request` including a JSON list, `null`, a bare string and non-JSON bytes, not 500 (`apply_batch` raises ValueError and the route maps it to 400); a 201-id batch returns 400 (`MAX_BATCH = 200`); a mid-batch write failure puts the applied items back and each undo is an audited `reset` event (`test_mid_batch_failure_puts_applied_items_back` passes).

## Exercised

Working directory `/Users/arsis/zlayt-pm-project` unless stated.

- `git rev-parse --short HEAD` before and after each run; pinned to d796383 for the code.
- `git archive d796383 | tar -x -C artifacts/review-evidence/T-055-security/head_d796383`; `tests/fixtures` copied from the working tree (`cp -R tests/fixtures ...`). Reason: the HEAD archive alone fails 2 of 5 existing `test_case_extras.py` tests (`assert 0 >= 7` and a 400 instead of 500), because the sample case needs LLM fixture files that are not tracked (see question 2).
- `pytest tests/unit/test_r2_batch_security.py tests/unit/test_case_extras.py -q -p no:cacheprovider` in the pinned archive: `29 passed, 1 skipped in 9.40s`. The skip is the rejected-entry test.
- `pytest tests/unit/test_case_extras.py -q` in the working tree: `5 passed in 1.39s`. Pinned archive with HEAD fixtures only (no copy): `2 failed, 3 passed` (`test_batch_accepts_verified_entries_only_and_logs_one_event_each`, `test_batch_is_atomic_when_a_write_fails_midway`).
- `artifacts/review-evidence/T-055-security/probe_states.py` (run from the pinned archive with `-I`): entry states per case and the id list.
- `board show T-055` (quoted in the AC section).
- `read app/backend/case_extras.py` (full), `app/backend/review.py:28-35` and `:348-351`, `docs` contract text (`memory/contracts/api.md`, commit 709397e, the review/batch section).

**Not exercised:** concurrent batch and single-item review (the single-item path does not take `_LOCK`; I did not race it), live :7860, UI.

## Findings (machine-readable summary)

```
F1 major  AC1 test does not exercise needs_review (case_extras.py:35 is correct; test_case_extras.py:57-59 leaves nonver empty).
F2 minor  rejected branch not covered (skip in pinned run).
F3 nit    case_extras.py:52 `before` unused.
```

## Questions for Chris

1. Should the sample case include one needs_review entry so the card's tests can exercise AC1 without state injection?
2. The HEAD checkout cannot run `test_case_extras.py` on its own: `tests/fixtures/llm` has 326 tracked files and 502 on disk, and some tracked fixture files are modified in the working tree. Is that outside my lens (qa or orchestrator) or a reproducibility gap to fix before the gate?

## Machine-readable record

```json
{"card": "T-055", "persona": "security-reviewer", "model": "claude-haiku-5-5",
 "scope": "T-055 batch accept: app/backend/case_extras.py apply_batch and review/batch route, app/backend/review.py batch_apply. Pinned at git archive d796383 (artifacts/review-evidence/T-055-security/head_d796383, with working-tree tests/fixtures copied). HEAD moved to 08764e7 during review; batch code unchanged d796383..HEAD. No app URL; in-process TestClient only.",
 "exercised": [
  "pytest tests/unit/test_r2_batch_security.py tests/unit/test_case_extras.py -q at d796383 archive: 29 passed, 1 skipped in 9.40s",
  "pytest tests/unit/test_case_extras.py -q working tree: 5 passed in 1.39s; HEAD-only archive without fixtures: 2 failed, 3 passed",
  "artifacts/review-evidence/T-055-security/probe_states.py: entry states [('verified','pending')] in both sample cases; ids e1..e9",
  "git diff --stat d796383 HEAD over batch files: empty",
  "board show T-055 (AC1 done:false)",
  "read case_extras.py (full), review.py:28-35 and :348-351, memory/contracts/api.md review/batch section",
  "not exercised: concurrent batch vs single review race, live :7860, UI"],
 "verdict": "changes",
 "scores": {"batch_refuses_amount_flag_needs_review": 5, "atomic_on_failure": 5, "malformed_body_400": 5, "cross_case_and_same_id_isolation": 5, "card_test_covers_ac1": 3},
 "findings": [
  {"severity": "major", "title": "AC1 test does not exercise the needs_review refusal",
   "evidence": "tests/unit/test_case_extras.py:57 nonver empty and :59 bad = [amount, flag] + nonver[:1]; probe_states.py output [('verified','pending')] for both sample cases; server rule app/backend/case_extras.py:35-36 correct (tests/unit/test_r2_batch_security.py::test_needs_review_entry... passes)",
   "why_it_matters": "AC1 names needs_review explicitly. A regression that let needs_review items through the batch would pass the suite.",
   "fix": "Add a needs_review case to tests/unit/test_case_extras.py: set one entry's state with DB.update_item (or use a fixture with one) and assert 422 invalid_batch with rejected not_verified and nothing changed.",
   "acceptance_test": "The needs_review test in test_case_extras.py passes at d796383 and fails when case_extras.py:35 is removed."},
  {"severity": "minor", "title": "Rejected-entry refusal is not exercised",
   "evidence": "test_r2_batch_security.py::test_rejected_entry_gives_422_and_nothing_changes skips (sample has no rejected entry); the same branch as needs_review.",
   "why_it_matters": "A rejected entry could be batch-accepted without a failing test.",
   "fix": "Set one entry to state rejected in a test (DB.update_item) and assert 422 not_verified.",
   "acceptance_test": "The test runs (no skip) and passes at HEAD."},
  {"severity": "nit", "title": "Unused variable in apply_batch",
   "evidence": "app/backend/case_extras.py:52 before = {...} never read",
   "why_it_matters": "Dead code in the atomicity path; misleads the next reader.",
   "fix": "Remove the line.",
   "acceptance_test": "none required"}
 ],
 "whats_right": [
  "Amount, flag, needs_review, rejected, cross-case and already-applied ids are all refused with 422 invalid_batch and nothing is written (24 probe tests pass).",
  "Malformed bodies (JSON list, null, bare string, non-JSON, duplicate ids, 201 ids, string ids) return 400 bad_request, never 500.",
  "A mid-batch write failure restores the applied items and each undo is an audited reset event."
 ],
 "questions_for_chris": [
  "Should the sample case include one needs_review entry so the card's tests can exercise AC1 without state injection?",
  "tests/fixtures/llm is partly untracked (326 tracked, 502 on disk, some tracked files modified in the working tree); HEAD alone cannot run test_case_extras.py. Outside my lens (qa or orchestrator): fix before the gate?"
 ]}
```
