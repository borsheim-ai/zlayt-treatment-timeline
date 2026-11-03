# T-065 review: batch accept 404/405 fallback removal (commit 5900040)

Reviewer: staff-engineer-reviewer. Verdict: **changes** (one major, two minor, no blockers).

## Summary

The card's acceptance criterion holds. On 404 or 405 from `POST /review/batch`, `app/frontend/batch.js` shows a plain refusal and returns before any write. The fallback is also gone from undo. The two `-k batch` E2E tests pass on the live server and on a clean archive of 5900040. Restoring the old accept fallback turns both tests red.

Your three checks, one by one:

1. **No per-item accept or undo path remains.** Not confirmed. `batch.js` now has no per-item call. The mock overlay still has one: `app/frontend/mock_extra.js:19` fans a batch accept or reset out to `/items/<id>/review`, and it is loaded unconditionally by `index.html:46`. The mode is selected from `?api=mock` (`api.js:6`). That is major finding 1.
2. **Test fails with the fallback restored.** Confirmed for accept (mutants M1 and M2 both fail). Not confirmed for undo: mutant M4 passes the suite. That is minor finding 2.
3. **`pytest -k batch` passes.** Confirmed: 2 passed on the live server, and 2 passed on the 5900040 archive. System python has no pytest, so I used `.venv/bin/python` (Python 3.12.2, pytest 9.2.0).

## Exercised

- `git show 5900040` (full diff); `git show 5900040^:app/frontend/batch.js` (pre-fix file, used as mutant M1).
- `cat app/frontend/batch.js`; `cat tests/e2e/conftest.py`; `app/frontend/mock_extra.js` (full); `app/frontend/mock.js:1`; `app/frontend/api.js:5-7`; `app/frontend/index.html:42-64`; `app/frontend/review.js:35-41,54-58`.
- Grep of `app/frontend/` for `api.review`, `RV.http`, `action: "accept"`, `action: "reset"`, `items/`. Also grep of `tests/` for `btn-undo-batch` and `undo` (no match).
- `curl http://localhost:7860/api/health` (200). `curl .../batch.js` on 7860 matches the 5900040 text (1 hit for the new comment, 0 for `ZL.api.review`).
- `.venv/bin/python -m pytest -q -p no:cacheprovider -rs -v tests/e2e/test_edit.py -k batch` against the live 7860 server: `2 passed, 4 deselected`.
- Clean archive `git archive 5900040` into the session scratchpad (`t065/base`), run against a scratch server on port 7861 (`LLM_BACKEND=fixture`, scratch DATA_DIR): `2 passed`.
- Mutant M1 (`t065/m1`, pre-fix batch.js with accept and undo fallbacks), port 7862: `FAILED ...[404]`, `FAILED ...[405]`, `2 failed`. Failure at test_edit.py:49 (the success message "Accepted 9 verified entries" shows instead of the refusal).
- Mutant M2 (`t065/m2`, accept fallback fires per-item, then the refusal still shows), port 7863: both fail at test_edit.py:51 with 9 `POST .../items/eN/review` requests recorded. This proves the per-item assertion is effective on its own.
- Mutant M4 (`t065/m4`, undo fallback only restored at batch.js:34-35), port 7864: `2 passed`.
- Scratch servers stopped (ports 7861-7864 down; 7860 still 200). Scratch copies live only under the session scratchpad. Nothing under the project tree was modified.
- Git state: `git diff --stat 5900040 HEAD -- app/frontend/batch.js app/frontend/mock_extra.js tests/e2e/test_edit.py` is empty (HEAD was 1855b76 at start, f201e3b at the last check; the files did not change).

Not exercised: the mock path in a browser (`?api=mock`). The finding about it is from code reading, with the line citations above.

## Findings

**Major 1: per-item accept and undo fan-out remains in the mock overlay.** `mock_extra.js:19` loops over batch ids and calls the per-item review endpoint without checking the status, and line 21 returns 200 regardless. This matches the spec-level concern: `memory/contracts/api.md:73` says the batch is atomic (one `apply_review` per item, all ids checked first, applied items put back if a write fails midway). The overlay does not roll back and reports success. It is not a bypass of the real API, because the UI batch code does no per-item calls, and the overlay checks verified/pending before fanning out (`mock_extra.js:15-17`). I rate it major and not blocker because `mock.js:1` labels the mock "Dev/test only". If `?api=mock` is reachable on the public build, re-rate it as a blocker under D.2 (spec constraint violated). See question 1.

**Minor 2: undo fallback removal has no test.** No test references `btn-undo-batch` (`grep -rn btn-undo-batch tests/` returns nothing). Mutant M4 restores the undo fallback and the suite stays green. Reset does not change verified-only, so there is no safety bypass here. It is still an untested behaviour change in the diff.

**Minor 3: fixed sleep in the negative assertion.** `tests/e2e/test_edit.py:50` (5900040) is `page.wait_for_timeout(300)` before the "no per-item POST" assertion. It is timing-dependent (Fowler: no bare sleeps). Replace it with a wait on a real signal.

## Outside this card (observation only)

The working tree has an uncommitted edit to `tests/e2e/test_edit.py` that removes the `xfail(strict=True)` marker from `test_notes_list_edited_item_with_both_texts` (`git diff HEAD -- tests/e2e/test_edit.py`). The batch tests are unaffected. Whoever owns that edit should know it changes a test's expected state.

## Whats right

- `batch.js:16-21`: the accept path has no per-item fallback. 404 and 405 show a plain refusal and return before any write (M1 red, control green).
- `test_edit.py:51`: the per-item request assertion catches a fallback even when the refusal message still shows (M2).
- The test intercepts the real batch route with real status codes and asserts on network requests, not only on UI text.

```json
{"card": "T-065", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 5900040 (app/frontend/batch.js, tests/e2e/test_edit.py); HEAD f201e3b at last check (both files unchanged since 5900040); live app http://localhost:7860 (LLM_BACKEND=fixture); sample case via tests/e2e/conftest.py sample_case (evals/golden/sample.txt); scratch mutants on ports 7861-7864 from git archive 5900040",
 "exercised": [
  "git show 5900040; git show 5900040^:app/frontend/batch.js",
  "cat app/frontend/batch.js, tests/e2e/conftest.py, app/frontend/mock_extra.js, mock.js:1, api.js:5-7, index.html:42-64, review.js:35-58",
  "grep app/frontend for api.review / RV.http / action accept|reset / items/ ; grep tests for btn-undo-batch (no match)",
  "curl http://localhost:7860/api/health (200) and /batch.js (matches 5900040)",
  ".venv/bin/python -m pytest -q -p no:cacheprovider -rs -v tests/e2e/test_edit.py -k batch against 7860: 2 passed, 4 deselected",
  "same command on clean git archive of 5900040 (scratch, port 7861): 2 passed",
  "mutant M1 = pre-fix batch.js (accept+undo fallback), port 7862: 2 failed at test_edit.py:49",
  "mutant M2 = accept fallback that still shows refusal, port 7863: 2 failed at test_edit.py:51 with 9 per-item POSTs",
  "mutant M4 = undo fallback only, port 7864: 2 passed",
  "git diff --stat 5900040 HEAD -- app/frontend/batch.js app/frontend/mock_extra.js tests/e2e/test_edit.py (empty)",
  "scratch servers stopped; no project files modified"
 ],
 "verdict": "changes",
 "scores": {"batch_404_405_accepts_nothing": 4, "no_per_item_accept_or_undo_path": 2, "test_sensitivity_to_fallback": 3, "determinism_no_sleep": 3, "api_contract_atomicity_in_frontend": 2, "honest_failure_visible": 4},
 "findings": [
  {"severity": "major",
   "title": "Per-item accept/undo fan-out remains in the mock overlay (grep check fails)",
   "evidence": "app/frontend/mock_extra.js:19: `for (const id of ids) await orig(\"POST\", `/cases/${token}/items/${id}/review`, { action: act });` (no status check; line 21 returns 200). Loaded unconditionally at app/frontend/index.html:46. Mode chosen from URL at app/frontend/api.js:6 (`new URLSearchParams(location.search).get(\"api\") || API_MODE`). Reproduce: grep -rn 'items/\\${id}/review' app/frontend/ -> mock_extra.js:19. Browser run of ?api=mock not performed (code read).",
   "why_it_matters": "The card asked to confirm no per-item accept or undo path remains; one does, reachable via ?api=mock. It breaks the api.md:73 batch contract (atomic; all ids checked first; applied items put back if a write fails midway): no rollback, statuses ignored, 200 returned claiming all items changed. Not a bypass of the real API: batch.js makes no per-item call and mock_extra.js:15-17 checks verified/pending before fanning out. Rated major, not blocker, because mock.js:1 says Dev/test only; re-rate to blocker if ?api=mock is reachable on the public build.",
   "fix": "Delete the per-item loop in mock_extra.js. Implement batch in the mock as one all-or-nothing step (validate every id, apply, roll back on any failure) per api.md:73, or have the mock answer /review/batch with 404 so only the UI refusal path runs under mock. Do not reintroduce any UI fallback.",
   "acceptance_test": "grep -rn 'items/${id}/review' app/frontend/mock_extra.js returns nothing inside the batch handler. A mock-mode E2E (?api=mock) that forces one per-item write to fail asserts a visible error and zero accepted entries."},
  {"severity": "minor",
   "title": "Undo fallback removal is untested; restoring it keeps the suite green",
   "evidence": "grep -rn btn-undo-batch tests/ -> no match (exit 1). Mutant M4 = 5900040 with batch.js:34-35 undo fallback restored (`if (r.status === 404 || r.status === 405) { for (const id of ids) await ZL.api.review(c.token, id, { action: \"reset\" }); r = { status: 200 }; }`): pytest -k batch -> 2 passed.",
   "why_it_matters": "The commit removes the undo fallback (batch.js:34-36) but nothing guards it. Reset does not change verified-only, so there is no safety bypass; it is an untested change in the same fallback class.",
   "fix": "Add an E2E test: accept one batch on the live server, stub **/review/batch with 404 for the reset call, click btn-undo-batch; assert the refusal text, zero POST to /review, and the entry still data-review=accepted.",
   "acceptance_test": "The new test fails on mutant M4 and passes on 5900040."},
  {"severity": "minor",
   "title": "Fixed 300 ms sleep before the negative 'no per-item POST' assertion",
   "evidence": "tests/e2e/test_edit.py:50 at 5900040: `page.wait_for_timeout(300)` (line numbers from git show 5900040:tests/e2e/test_edit.py; the working tree has an unrelated uncommitted edit shifting lines by one).",
   "why_it_matters": "Fowler: never bare sleeps. The negative assertion depends on timing: a slow runner can pass before a late per-item POST, a fast one can miss it.",
   "fix": "Replace the sleep with a deterministic wait, e.g. wrap the click in page.expect_response(lambda r: r.url.endswith('/review/batch')) and then page.wait_for_load_state('networkidle') before the request-list assertion.",
   "acceptance_test": "Test passes 20 consecutive runs with the sleep removed and still fails on mutant M2."}
 ],
 "whats_right": [
  "batch.js:16-21 accept path has no per-item fallback; 404/405 shows a refusal and returns before any write (M1 red, 5900040 green).",
  "test_edit.py:51 per-item request assertion catches a fallback even when the refusal message still shows (M2: 9 per-item POSTs).",
  "The test intercepts the real batch route with real status codes and asserts on network requests, not only UI text."
 ],
 "questions_for_chris": [
  "Is ?api=mock (app/frontend/api.js:6, mock_extra.js loaded in index.html:46) reachable on the public build? If yes, major finding 1 becomes a blocker.",
  "CLAUDE.md and the dossier expect engineering reviewers on claude-sonnet-5-5; this review ran on claude-haiku-5-5. Keep this record as-is, or re-run on Sonnet?"
 ]}
```
