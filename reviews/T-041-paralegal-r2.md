# T-041 paralegal review, round 2 (Maria Delgado persona)

Verdict: pass. Commit a90d1b0 resolves the round-1 major and both round-1 minors.

- Major (AC4 proof test missing): resolved. `tests/unit/test_api.py:17` defines `test_export_endpoint`. It runs through `export_routes.router` with a fake loader. It asserts that entry 5 (dismissed) and entry 6 (pending) are absent from the letter, the total line is exact, the items list excludes the pending amount, and an unknown token returns 404 `not_found`.
- Minor (non-verbatim excerpt guard): resolved. `app/backend/export.py:115-116` defines `verbatim()`, which requires the whitespace-normalized excerpt to be a substring of its record. It is applied in `in_entries` and `in_charges`, so a failing entry or charge is dropped from the letter. `test_export_edge.py::test_non_verbatim_excerpt_not_exported_and_listed` checks this. I disabled the guard at runtime and the test failed, so the test catches it.
- Minor (could-not-process and rate-reason tests): resolved. `test_export_edge.py:7` covers the could-not-process line. `test_export_edge.py:36` covers the rate reason "(12 planned; discharged at visit 9)".

Residual, not a finding for this round: the live route is still unreachable. `curl` returns 000 because T-040 has not wired the loader (`export_routes.py:3-4`). AC4's evidence in the board says "router standalone, fake loader", which is accurate. The live endpoint needs its own check when T-040 lands.

Not re-scored: `verify_quickly`. I did not drive the running app this round, so I did not re-rate it. Round 1 scored it 4.

## What I exercised
- `.venv/bin/python -m pytest tests/unit/test_api.py tests/unit/test_export.py tests/unit/test_export_edge.py -q 2>&1 | tail -3` -> `24 passed in 0.22s`
- `.venv/bin/python -m pytest` on the four round-2 named tests with `-v` -> `4 passed in 0.20s`, each marked PASSED
- `grep -rn "test_export_endpoint" tests app` -> `tests/unit/test_api.py:17:def test_export_endpoint():`
- `grep -rni "could_not_process\|could not process" tests` -> `tests/unit/test_export_edge.py:7`, `:10`, `:13`
- `grep -n` on `app/backend/export.py` for the verbatim guard -> `:115-116` `verbatim()`, and its uses in `in_entries` / `in_charges`
- Read in full: `tests/unit/test_api.py`, `tests/unit/test_export_edge.py`
- `git show --stat a90d1b0` -> 3 files changed (`app/backend/export.py`, `tests/unit/test_api.py`, `tests/unit/test_export_edge.py`)
- `.venv/bin/python tools/board.py show T-041` -> AC4 `done: true`, evidence "tests/unit/test_api.py::test_export_endpoint passes (router standalone, fake loader ...)"
- `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:7860/api/cases/x/export` -> `000`
- Mutation check: `artifacts/review-evidence/T-041-r2-mutation.py` disables `verbatim()` at runtime. Output: `MUTANT KILLED: guard test fails with guard disabled` / `UNMUTATED: guard test passes`. No product code was edited.
- Not run: the running app UI (Playwright). The HTTP route is not exercised end to end.

## Model note
`personas/paralegal.md` expects `claude-opus-5-5`. This session runs as `claude-haiku-5-5`, so the JSON records `claude-haiku-5-5`.

```json
{"card": "T-041", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit a90d1b0 (round 2) on app/backend/export.py, tests/unit/test_api.py, tests/unit/test_export_edge.py; test-level verification, no running app; sample case via build_case",
 "exercised": [
  ".venv/bin/python -m pytest tests/unit/test_api.py tests/unit/test_export.py tests/unit/test_export_edge.py -q 2>&1 | tail -3 -> 24 passed in 0.22s",
  "pytest -v on test_api::test_export_endpoint and three test_export_edge tests -> 4 PASSED",
  "grep test_export_endpoint tests app -> tests/unit/test_api.py:17",
  "grep could_not_process / could not process tests -> tests/unit/test_export_edge.py:7,10,13",
  "grep export.py verbatim guard -> export.py:115-116 verbatim(); used in in_entries and in_charges",
  "read tests/unit/test_api.py and tests/unit/test_export_edge.py in full",
  "git show --stat a90d1b0 -> 3 files changed",
  "tools/board.py show T-041 -> AC4 done, evidence names test_api::test_export_endpoint",
  "curl http://localhost:7860/api/cases/x/export -> 000 (loader not wired until T-040)",
  "artifacts/review-evidence/T-041-r2-mutation.py: guard disabled at runtime -> test_non_verbatim_excerpt_not_exported_and_listed fails (killed); unmutated passes"],
 "verdict": "pass",
 "scores": {"endpoint_test_present": 4, "verbatim_guard_test_kills_mutant": 5, "could_not_process_test": 5, "rate_reason_test": 5},
 "findings": [
  {"severity": "nit", "title": "Live GET /api/cases/{token}/export still unreachable until T-040 wires the loader",
   "evidence": "curl http://localhost:7860/api/cases/x/export -> 000; app/backend/export_routes.py:3-4 'The app factory (T-040) does app.include_router(export_routes.router) and registers the case loader'; board AC4 evidence 'router standalone, fake loader'",
   "why_it_matters": "test_export_endpoint proves the router, not the deployed app. The dismissed/pending exclusion is therefore proven on a standalone FastAPI app, not on the route the demand export will use.",
   "fix": "No change in T-041. When T-040 lands, add one test that builds the real app factory and hits the export route for a dismissed and a pending entry.",
   "acceptance_test": "T-040: TestClient on the app factory; GET /api/cases/{token}/export returns 200 with February 20, 2026 and March 6, 2026 absent from letter_text; unknown token returns 404."}
 ],
 "whats_right": [
  "The guard is a real invariant: disabling verbatim() makes test_non_verbatim_excerpt_not_exported_and_listed fail, so the test is not decorative.",
  "test_export_endpoint checks the dismissed, pending and unknown-token behavior that the export dealbreaker depends on, and asserts the letter and notes are separate fields.",
  "The could-not-process and rate-reason tests assert exact strings from the spec, so a wording change in export.py would fail the suite."],
 "questions_for_chris": ["personas/paralegal.md expects model claude-opus-5-5 but this session runs as claude-haiku-5-5; which id should the board record for paralegal reviews?"]}
```
