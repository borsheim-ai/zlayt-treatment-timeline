# T-065 round 2 review: mock batch rules, undo fallback test (commit e0ca2b0)

Reviewer: staff-engineer-reviewer (model claude-haiku-5-5). Verdict: **changes** (one major, four minors, no blockers).

## Summary

The three checks in the brief hold at e0ca2b0, with one exception on the contract test.

1. **Mock batch is verified-only and all-or-nothing.** Confirmed. `app/frontend/mock.js:194-202` checks every id before the first write and returns 422 `invalid_batch` with nothing changed. A mixed batch (eight verified ids plus one `needs_review` id) was refused with zero accepted entries and zero per-item POSTs. Two gaps against `memory/contracts/api.md:73` remain (minors 2 and 3).
2. **No per-item fan-out in `app/frontend`.** Confirmed. `mock_extra.js` no longer touches `/items/<id>/review` for batch calls. The r1 major is closed. `batch.js` makes two batch calls (accept, reset). The only `api.review` callers are single-item UI actions in `review.js`, `excerpt.js` and `narrative.js`. In the mock UI, accept-all made one `POST /review/batch accept` and undo made one `POST /review/batch reset`, with zero per-item calls.
3. **The undo test fails when the undo fallback is restored.** Confirmed. Mutant M4 (undo fallback restored in a scratch copy of e0ca2b0, served on port 7864) makes both `test_batch_undo_route_missing_resets_nothing[404]` and `[405]` fail. The UI shows "Undone: 9 entries back to not reviewed." where the test expects a refusal.
4. **`pytest tests/e2e/test_edit.py -k batch` passes.** Confirmed: 5 passed, 4 deselected, on the pinned e0ca2b0 archive and on the live server at 7860. The brief's count of 2 is out of date: the new undo tests and the static guard make 5.
5. **Contract test.** `tests/unit/test_e2e_contract.py` fails on the e0ca2b0 archive with `AssertionError: ['btn-undo-batch']` (1 failed, 2 passed). Recorded as major 1. Commit 4594bb7 declares the id, and it is an ancestor of HEAD. The id is no longer in the failure list at HEAD.

Round-1 status: r1 major 1 (mock fan-out) resolved. r1 minor 2 (undo untested) resolved and killed by M4. r1 minor 3 (fixed 300 ms sleep) still open, now minor 5. r1 question 1 (is `?api=mock` reachable on the public build) still unanswered.

Observation outside this card (not scored): at HEAD 312ed92, `tests/unit/test_e2e_contract.py` fails on other cards' ids (`date-to-confirm-excerpt`, `missing-date-confirmed`, `confirm-date`, `date-to-confirm-item`, `btn-manual-entry`) and on `data-record-id` in `tests/e2e/test_input.py`. These belong to the owners of those specs. This review does not rate them.

## Exercised

- Pinned: `git archive e0ca2b0` into scratchpad `t065r2/base`. Read `app/frontend/mock.js:191-203`, `mock_extra.js` (full), `batch.js` (full), `api.js:4-6`, `index.html:41-46`, `tests/e2e/test_edit.py:52-79`, `tests/e2e/conftest.py` (contract docstring and `pytest_collection_modifyitems`), `memory/contracts/api.md:73`, `app/backend/case_extras.py:24-38, 42-56, 105-118`.
- `git show e0ca2b0 -- app/frontend/mock.js app/frontend/mock_extra.js tests/e2e/test_edit.py` (full diff).
- `grep -rn 'items/\|/review`\|api.review\|RV.http\|action: "accept"\|action: "reset"' app/frontend/` (listed call sites above).
- `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_e2e_contract.py` on the pinned archive: 1 failed, 2 passed, `['btn-undo-batch']`. On HEAD 312ed92: 2 failed, 1 passed (other cards' ids, see the observation above).
- `E2E_BASE_URL=http://localhost:7861 ... pytest tests/e2e/test_edit.py -k batch` on the pinned archive: 5 passed, 4 deselected.
- Mutant M4 (diff in outputs.txt: `batch.js:34-35` restores `ZL.api.review(..., {action:"reset"})` on 404/405), served on 7864: `FAILED test_batch_undo_route_missing_resets_nothing[404]`, `[405]`, and the static test; 2 passed.
- Brief command `pytest tests/e2e/test_edit.py -k batch` against the live server at 7860: 5 passed, 4 deselected.
- Static guard with no server (`E2E_BASE_URL=http://localhost:7999`): `1 skipped`.
- Headless Chromium on the pinned copy in `?api=mock` mode, scripts `mock_batch_probe.py`, `mock_dup_probe.py`, `mock_ui_probe.py`. Results: mixed batch 422 / 0 accepted / 1 batch POST / 0 per-item POSTs; verified accept 200 / 8 accepted; repeat accept 422 `not_pending`-style free text; reset 200 / 0 accepted; duplicate ids 200 (see minor 2); UI accept-all and undo one batch call each.
- Real server duplicate-id check: `curl -X POST .../review/batch` with `[e1, e1]` on port 7861 returns HTTP 400 `bad_request`.
- Read `reviews/T-065-staff-engineer.md` (r1) for the carried-over items.
- Evidence: `artifacts/review-evidence/T-065-staff-engineer-r2/outputs.txt` and the three probe scripts beside it.
- Not exercised: the mock UI under a real network failure midway through a batch (the mock has no write path that can fail).

## Findings

**Major 1: `btn-undo-batch` undeclared at e0ca2b0 (contract unit test red on the reviewed commit).**
Evidence: `tests/unit/test_e2e_contract.py` on the `git archive e0ca2b0` tree: `AssertionError: ['btn-undo-batch']`, `1 failed, 2 passed`. The id is used at `tests/e2e/test_edit.py:60` and `:66`. `git show e0ca2b0:tests/e2e/conftest.py | grep -c btn-undo-batch` prints `0`. Resolved on HEAD: commit 4594bb7 ("declare btn-undo-batch test id") is an ancestor of HEAD, and the id is absent from the contract failure list at HEAD 312ed92.
Why it matters: the reviewed commit leaves the unit suite red. The brief asked for this to be recorded. The rule (new `data-testid` needs its contract line in the same commit) was broken here and fixed one commit later.
Fix: already applied by 4594bb7. Keep it. Add the rule to the QA checklist: a spec that adds a hook and its contract line in the same commit.
Acceptance test: `tests/unit/test_e2e_contract.py` passes on e0ca2b0 with 4594bb7 cherry-picked; it fails on the bare e0ca2b0 archive (current state).

**Minor 2: mock accepts duplicate ids and over-long batches; the server refuses both.**
Evidence: mock probe on 7861 (`mock_dup_probe.py`): `{"duplicate_ids": {"status": 200, "accepted_now": 1}}`. Real server, same request shape: `curl -X POST http://localhost:7861/api/cases/<tok>/review/batch -d '{"action":"accept","item_ids":["e1","e1"]}'` returns HTTP 400 `{"error":{"code":"bad_request",...}}`. `memory/contracts/api.md:73` says "1 to 200 distinct ids". `app/frontend/mock.js:194-202` has no duplicate or length check.
Why it matters: a mock that accepts what the real server refuses is a contract divergence. It is dev/test only (`mock.js:1`), so this is minor, not blocker.
Fix: in `mock.js`, return 400 `bad_request` for an empty list, more than 200 ids, or duplicate ids, before the verified-only check.
Acceptance test: `mock_dup_probe.py` gets 400 for `[e1, e1]`; a 201-id batch gets 400.

**Minor 3: mock rejection reasons are free text, not the documented codes.**
Evidence: `app/frontend/mock.js:197` `reason: "only entries can be decided in a batch"`; `mock.js:199` `reason: "only verified, not-yet-reviewed entries can be accepted in a batch"`. `memory/contracts/api.md:73` requires `not_an_entry | not_verified | not_pending | not_found`. The server emits those codes at `app/backend/case_extras.py:31-38`. The probe output shows the free text in `detail.rejected[].reason`.
Why it matters: a UI or test that branches on `reason` behaves differently in mock mode and in real mode.
Fix: use the four codes in the mock; keep the human text in `message`.
Acceptance test: `mock_batch_probe.py` asserts the same `rejected[].reason` codes that the real server returns for the same ids.

**Minor 4: the static guard test runs only when the app server is up.**
Evidence: `tests/e2e/test_edit.py:72-79` (`test_no_frontend_code_posts_to_the_per_item_review_route_for_a_batch`) is in `tests/e2e/`. `tests/e2e/conftest.py` `pytest_collection_modifyitems` skips every e2e item when `/api/health` is unreachable. Run with `E2E_BASE_URL=http://localhost:7999`: `SKIPPED [1] ... app server not running`. The test is also a string search of `app/frontend` sources (dossier 4.13: assert behaviour, not implementation).
Why it matters: in an unattended run without a server, the only guard on per-item fan-out is silently skipped. M4 was caught by this test through a heuristic (`action: "reset"` plus `for (const`), not by what the user sees.
Fix: move the source check to `tests/unit/` (it needs no server). Keep the behavioural E2E test as the main guard.
Acceptance test: with no server, the moved test runs and fails on M4 and on the 5900040 `batch.js`.

**Minor 5: fixed 300 ms sleep before a negative assertion (carried from r1 minor 3).**
Evidence: `tests/e2e/test_edit.py:49` `page.wait_for_timeout(300)` at e0ca2b0; unchanged at HEAD 312ed92 (`git show HEAD:tests/e2e/test_edit.py | grep -n wait_for_timeout` prints `49:`).
Why it matters: Fowler (no bare sleeps). The "no per-item POST" check can pass before a late request on a slow runner.
Fix: wait on `page.expect_response` for the `/review/batch` call, then `wait_for_load_state("networkidle")`, before the request-list assertion.
Acceptance test: 20 consecutive runs pass with the sleep removed, and the test still fails on mutant M2 (9 per-item POSTs).

## What is right

- `mock.js:194-202`: every id is validated before any write. The probe confirms the refusal leaves zero entries accepted and makes no per-item call.
- The undo test (`test_edit.py:52-68`) asserts the refusal text, zero `/review` POSTs and an unchanged accepted count. M4 turns it red on 404 and 405.
- In `?api=mock`, accept-all and undo each make exactly one batch call (`mock_ui_probe.py`, outputs.txt).

```json
{"card": "T-065", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit e0ca2b0 (app/frontend/mock.js, app/frontend/mock_extra.js, tests/e2e/test_edit.py); pinned via git archive into scratchpad t065r2/base; live app http://localhost:7860 (HEAD 312ed92 at review time); scratch servers 7861 (e0ca2b0) and 7864 (M4 undo fallback restored); sample case via tests/e2e/conftest.py sample_case",
 "exercised": [
  "git show e0ca2b0 (mock.js, mock_extra.js, test_edit.py); read batch.js, mock_extra.js, mock.js:191-203, api.js:4-6, index.html:41-46, test_edit.py:52-79, conftest.py contract and skip hook, api.md:73, case_extras.py:24-118",
  "grep app/frontend for items/, /review`, api.review, RV.http, action accept/reset",
  "pytest tests/unit/test_e2e_contract.py on git archive e0ca2b0: 1 failed, 2 passed (['btn-undo-batch']); on HEAD 312ed92: 2 failed, 1 passed (other ids)",
  "pytest tests/e2e/test_edit.py -k batch on pinned e0ca2b0 @7861: 5 passed, 4 deselected",
  "mutant M4 (batch.js:34-35 undo fallback restored) @7864: undo [404] and [405] FAILED, static guard FAILED; 2 passed",
  "brief command pytest tests/e2e/test_edit.py -k batch @ live 7860: 5 passed, 4 deselected",
  "E2E_BASE_URL dead port: static guard SKIPPED (no server)",
  "headless Chromium ?api=mock: mock_batch_probe.py (mixed refusal 422 / 0 accepted / 0 per-item POSTs; verified accept 200; repeat accept 422; reset 200), mock_dup_probe.py (duplicate ids 200), mock_ui_probe.py (accept-all and undo one batch call each)",
  "curl POST /review/batch duplicate ids on 7861: HTTP 400 bad_request",
  "git log for conftest.py, git show HEAD test_edit.py grep (sleep at line 49), git diff in-scope files since e0ca2b0 (empty for batch.js, mock.js, mock_extra.js, test_edit.py)",
  "evidence: artifacts/review-evidence/T-065-staff-engineer-r2/outputs.txt and mock_*_probe.py"
 ],
 "verdict": "changes",
 "scores": {"batch_404_405_accepts_nothing": 4, "no_per_item_accept_or_undo_path": 4, "mock_batch_matches_server_contract": 3, "test_sensitivity_to_undo_fallback": 5, "determinism_no_sleep": 2, "contract_suite_green_at_commit": 2, "honest_failure_visible": 4},
 "findings": [
  {"severity": "major",
   "title": "btn-undo-batch undeclared at e0ca2b0: contract unit test red on the reviewed commit (resolved on HEAD by 4594bb7)",
   "evidence": "tests/unit/test_e2e_contract.py on git archive e0ca2b0: AssertionError: ['btn-undo-batch']; 1 failed, 2 passed. Used at tests/e2e/test_edit.py:60 and :66; git show e0ca2b0:tests/e2e/conftest.py | grep -c btn-undo-batch prints 0. 4594bb7 declares it and is an ancestor of HEAD; absent from the failure list at HEAD 312ed92.",
   "why_it_matters": "The reviewed commit leaves the unit suite red, against 'tests fail when the code breaks and pass reproducibly'. The brief asked for this to be recorded. Already fixed one commit later, so the card's current state is green for this check.",
   "fix": "Keep 4594bb7. Add to the QA checklist: a spec that adds a data-testid lands its contract line in the same commit.",
   "acceptance_test": "pytest tests/unit/test_e2e_contract.py passes on e0ca2b0 with 4594bb7 applied; fails on the bare e0ca2b0 archive."},
  {"severity": "minor",
   "title": "Mock batch accepts duplicate ids (and over-long batches); the server refuses both",
   "evidence": "mock_dup_probe.py on 7861: {\"duplicate_ids\": {\"status\": 200, \"accepted_now\": 1}}. Real server on 7861: POST /api/cases/<tok>/review/batch with [e1, e1] returns HTTP 400 bad_request. memory/contracts/api.md:73 says 1 to 200 distinct ids. app/frontend/mock.js:194-202 has no duplicate or length check.",
   "why_it_matters": "The mock accepts what the real contract refuses. Dev/test only (mock.js:1), so minor.",
   "fix": "In mock.js, return 400 bad_request for an empty list, more than 200 ids, or duplicate ids, before the verified-only check.",
   "acceptance_test": "mock_dup_probe.py gets 400 for [e1, e1]; a 201-id batch gets 400."},
  {"severity": "minor",
   "title": "Mock rejection reasons are free text, not the documented codes",
   "evidence": "app/frontend/mock.js:197 reason \"only entries can be decided in a batch\"; mock.js:199 reason \"only verified, not-yet-reviewed entries can be accepted in a batch\". memory/contracts/api.md:73 requires not_an_entry, not_verified, not_pending, not_found; app/backend/case_extras.py:31-38 emits them.",
   "why_it_matters": "UI or tests that branch on rejected[].reason behave differently in mock mode and real mode.",
   "fix": "Use the four codes in the mock; keep the human text in message.",
   "acceptance_test": "mock_batch_probe.py asserts the same rejected[].reason codes the real server returns for the same ids."},
  {"severity": "minor",
   "title": "Static guard against per-item fan-out lives in tests/e2e and is skipped when the server is down",
   "evidence": "tests/e2e/test_edit.py:72-79 (test_no_frontend_code_posts_to_the_per_item_review_route_for_a_batch). tests/e2e/conftest.py pytest_collection_modifyitems skips all e2e items when /api/health is down; E2E_BASE_URL=http://localhost:7999 gives SKIPPED [1] app server not running. The test is a string search of app/frontend sources; M4 was caught by a heuristic ('action: \"reset\"' and 'for (const').",
   "why_it_matters": "Without a server the only guard on per-item fan-out is silently skipped. Dossier 4.13: assert behaviour, not implementation.",
   "fix": "Move the source check to tests/unit/ (no server needed). Keep the behavioural E2E test as the main guard.",
   "acceptance_test": "With no server the moved test runs and fails on mutant M4 and on the 5900040 batch.js."},
  {"severity": "minor",
   "title": "Fixed 300 ms sleep before the negative per-item assertion (carried from r1 minor 3)",
   "evidence": "tests/e2e/test_edit.py:49 page.wait_for_timeout(300) at e0ca2b0; unchanged at HEAD 312ed92 (git show HEAD:tests/e2e/test_edit.py | grep -n wait_for_timeout prints 49).",
   "why_it_matters": "Fowler: no bare sleeps. A slow runner can pass before a late per-item POST.",
   "fix": "Wait on page.expect_response for the /review/batch call, then networkidle, before the request-list assertion.",
   "acceptance_test": "20 consecutive passes with the sleep removed; the test still fails on mutant M2 (9 per-item POSTs)."}
 ],
 "whats_right": [
  "mock.js:194-202 validates every id before any write; a mixed batch is refused with 0 accepted and 0 per-item POSTs (mock_batch_probe.py).",
  "The undo test (test_edit.py:52-68) asserts the refusal text, zero /review POSTs and an unchanged accepted count; M4 turns it red on 404 and 405.",
  "In ?api=mock, accept-all and undo each make exactly one batch call (mock_ui_probe.py)."
 ],
 "questions_for_chris": [
  "Is ?api=mock (api.js:6, mock_extra.js loaded from index.html:46) reachable on the public build? It can no longer fan out per item, and it writes nothing to the real case, so I now rate the reachability as a question, not a blocker. Keep it or gate it?",
  "CLAUDE.md section 6 and the dossier assign engineering reviewers to Sonnet. This review ran as claude-haiku-5-5. Keep this record as-is, or re-run on Sonnet?"
 ]}
```
