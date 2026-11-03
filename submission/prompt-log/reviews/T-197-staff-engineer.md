# T-197 review (staff-engineer): GET /api/health reports local_mode

**Verdict: changes** (0 blockers, 1 major, 1 minor, 1 nit).

**Reviewed sha: 612dc2c.** HEAD was dfd9b11 at my first rev-parse and moved to 612dc2c during the review. Every finding is for 612dc2c. The working tree is dirty and was not reviewed. Model recorded is claude-haiku-5-5, the model I ran as; the dossier expected claude-sonnet-5-5.

## What holds at 612dc2c
- The field is `"local_mode": local_mode()` at `app/backend/api.py:266`, the same function that gates `/api/cases` (api.py:272) and `/api/library` (api.py:282). It is read per request.
- In five 200 cases (ZLAYT_MODE unset, `public`, `local`, `LOCAL`, and unset from 192.168.1.5) the body's `local_mode` equals `local_mode()` and is a bool. In local mode a non-loopback peer gets 403 from the middleware at api.py:221 before the body is built.
- The body adds no sensitive value. `local_mode` is a bool, and the ZLAYT_MODE value is not echoed.
- `tests/unit/test_api_routes.py:396-403` asserts True for `local`, False for unset, and False for `public`. Five mutants (hardcoded False, hardcoded True, field removed, public counted as local, string instead of bool) each fail it. The control passes.
- `memory/contracts/api.md:50` shows the field in the example and `:57` documents it.

## Findings
- **major: the card's e2e AC is not met at 612dc2c.** `tests/e2e/guided/test_round2.py` is untracked (`git status` shows `??`) and absent at 612dc2c. No file under `app/frontend` reads `local_mode` at 612dc2c. `app/frontend/guided/step1.js:28` still calls `GET /library` on `/new`, and `home.js:118` still calls `G.api.cases` with no gate. The T-181 r2 first-paint request is still there. The working tree already has the frontend gate uncommitted. Not a blocker: the backend field is correct, the failure is caught, and nothing regressed.
- **minor: `api.md:57` describes UI behaviour in the present tense that does not exist at 612dc2c.** It should read "will" until the frontend lands.
- **nit: `api.md:17`** endpoint summary row omits local_mode.

## Exercised
- `python3 tools/board.py show T-197`: in_progress, claimed by backend, AC1 done false, commits empty.
- `git rev-parse HEAD`, `git log --oneline -i --grep=T-197`, `git show --stat 612dc2c`.
- `git archive 612dc2c` extracted to the session scratchpad. `git show 612dc2c:app/backend/api.py | diff -q` against the archive copy: identical.
- In the archive, with the project venv: `python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -q` gave 35 passed; `-k health` gave 3 passed; `-k health_reports_local_mode -v` gave 1 passed.
- `artifacts/review-evidence/T-197-staff-engineer/health_probe.py` with `python -I` on the archive. Output is in the transcript.
- `artifacts/review-evidence/T-197-staff-engineer/mutants.py` with `python -I` on scratch copies. M0 control 1 passed; M1 to M5 each 1 failed.
- Read `app/backend/api.py` at 83, 221, 263-266, 270-292; `memory/contracts/api.md` at 17, 50, 57; `app/frontend/guided/step1.js:28`; `app/frontend/guided/home.js:118`.
- `grep -rln local_mode app/frontend` in the archive: 0 files.
- Not exercised: a live server on :7860, the public-mode browser first paint, the named e2e test (absent at the sha), the full unit suite.

```json
{"card": "T-197", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "Reviewed commit 612dc2c (feat(backend): GET /api/health reports local_mode (T-197)): app/backend/api.py, memory/contracts/api.md, tests/unit/test_api_routes.py. HEAD was dfd9b11 at the first rev-parse and moved to 612dc2c during the review; all findings are for 612dc2c. The working tree is dirty (uncommitted frontend, e2e and api.py edits) and was not reviewed. No app URL (in-process TestClient only). No sample case run (outside the card AC).",
 "exercised": [
  "python3 tools/board.py show T-197 -> status in_progress, claimed_by backend, AC1 done false, commits []",
  "git rev-parse HEAD -> dfd9b11 at first call, then 612dc2cca3fed1b5f58728042593585056426aca; git log --oneline -i --grep=T-197 -> 612dc2c only",
  "git show --stat 612dc2c -> 3 files, 14 insertions, 2 deletions (app/backend/api.py, memory/contracts/api.md, tests/unit/test_api_routes.py)",
  "git archive 612dc2c | tar -x into scratchpad/T-197-612dc2c; git show 612dc2c:app/backend/api.py | diff -q against the archive copy -> identical",
  "cd archive && .venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -q -> 35 passed in 6.94s; -k health -> 3 passed; -k health_reports_local_mode -v -> 1 passed",
  "artifacts/review-evidence/T-197-staff-engineer/health_probe.py run with python -I against the archive: ZLAYT_MODE unset, public, local, LOCAL (case), unset from 192.168.1.5, local from 192.168.1.5. Body.local_mode equals local_mode() and is a bool in each of the five 200 cases; local from a non-loopback peer returns 403 with no health body (middleware at api.py:221)",
  "artifacts/review-evidence/T-197-staff-engineer/mutants.py run with python -I on scratch copies of the archive (exact-count replacement asserted): M0 control 1 passed; M1 hardcoded False, M2 hardcoded True, M3 field removed, M4 public counted as local, M5 string instead of bool: each 1 failed",
  "Read app/backend/api.py:83 (local_mode), 221 (loopback gate applies to every path), 263-266 (health route returns local_mode: local_mode()), 270-282 and 292 (/api/cases and /api/library 404 when not local_mode())",
  "Read memory/contracts/api.md:50 (example shape with local_mode) and :57 (prose that says the guided UI reads it on first paint)",
  "grep -rln local_mode app/frontend in the 612dc2c archive -> 0 files; app/frontend/guided/step1.js:28 calls GET /library unconditionally on /new; app/frontend/guided/home.js:118 calls G.api.cases with no local_mode check",
  "git cat-file -e 612dc2c:tests/e2e/guided/test_round2.py -> absent; git status --short tests/e2e/guided -> '?? tests/e2e/guided/test_round2.py' (untracked). The named e2e test was not run because it does not exist at the reviewed sha. No browser run",
  "Not exercised: a live server on :7860 (not started), the public-mode browser first paint, the full unit suite (outside the brief)"
 ],
 "verdict": "changes",
 "scores": {"field_equals_local_mode_in_every_mode": 5, "leaks_nothing_sensitive": 5, "api_md_documents_field": 4, "unit_test_asserts_both_values": 5, "mutants_killed_by_unit_test": 5, "card_ac_first_paint_e2e_met_at_sha": 1},
 "findings": [
  {"severity": "major",
   "title": "Card AC1 e2e half is not met at 612dc2c: the named test is untracked, no frontend reads local_mode, and public first paint still requests /library and /api/cases",
   "evidence": "git cat-file -e 612dc2c:tests/e2e/guided/test_round2.py -> absent; git status --short tests/e2e/guided -> '?? tests/e2e/guided/test_round2.py'; grep -rln local_mode app/frontend (612dc2c archive) -> 0 files; app/frontend/guided/step1.js:28 'G.api.call(\"GET\", \"/library\", ...)' runs on /new with no gate; app/frontend/guided/home.js:118 'G.api.cases(signal)' runs with no gate. Card AC1 text: 'tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server passes (no xfail)'.",
   "why_it_matters": "The card title says the guided UI must never probe /api/cases or /api/library in public mode (T-181 r2 first-paint 404). At the reviewed commit the field exists but nothing reads it, so the first-paint request still happens. Not a blocker: the backend field is correct, the probe failure is caught (step1.js:28 sets lib = null), and nothing regressed. It is a must-fix before the card can close, because AC1 is not satisfied.",
   "fix": "Land the frontend half on the same card: gate the /library call in step1.js:28 and the G.api.cases call in home.js:118 on health.local_mode !== false, and commit tests/e2e/guided/test_round2.py without an xfail marker. The working tree already has this change uncommitted (grep shows local_mode in app/frontend/guided/step1.js:28 and home.js:119 there, context only). Then move to in_review at the new sha.",
   "acceptance_test": "At the committed sha: tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server passes; git grep -n xfail <sha> -- tests/e2e/guided/test_round2.py prints nothing; git grep -n local_mode <sha> -- app/frontend is non-empty."},
  {"severity": "minor",
   "title": "api.md states present-tense UI behaviour that is false at 612dc2c",
   "evidence": "memory/contracts/api.md:57: 'The guided UI reads it on first paint and never probes those routes when it is `false`, so a public server sees no 404.' versus grep -rln local_mode app/frontend -> 0 files at 612dc2c, and step1.js:28 / home.js:118 unconditional.",
   "why_it_matters": "A reader of the contract, including the frontend worker writing the missing half, would assume the gate exists. The field itself is documented correctly at api.md:50 and :57 (name, type, meaning, route gating). Minor because the claim describes the intended consumer behaviour, not the backend output; it becomes true only when finding 1 lands.",
   "fix": "Until the frontend lands, reword line 57 to 'The guided UI will read it ...' or land the frontend change in the same commit as the doc.",
   "acceptance_test": "After the frontend commit: git grep -n local_mode <sha> -- app/frontend is non-empty and api.md:57 matches that sha; before it, api.md:57 uses future tense."},
  {"severity": "nit",
   "title": "api.md endpoint summary row does not list local_mode",
   "evidence": "memory/contracts/api.md:17: '| GET | `/api/health` | backend, demo mode, models, limits, banner text |'",
   "why_it_matters": "Minor discoverability gap in the summary table; the full shape at :50 is correct.",
   "fix": "Add 'local mode flag' to the row.",
   "acceptance_test": "grep -n 'local mode' memory/contracts/api.md shows the row at line 17."}
 ],
 "whats_right": [
  "The field is the same local_mode() call that gates /api/cases and /api/library, read per request at api.py:266, so it cannot drift from the gate.",
  "The new unit test asserts True and False, plus a 'public' value that must read False; five mutants (hardcoded False, hardcoded True, field removed, public counted as local, string not bool) each fail it, and the unmutated control passes.",
  "In local mode a non-loopback client gets 403 from the middleware at api.py:221 before the health body is built, so a public client only ever sees local_mode false; the field discloses nothing beyond the existing demo_mode and backend fields."
 ],
 "questions_for_chris": ["Should T-197 close on the backend half alone with the frontend and e2e split into a new card, or stay open until the first-paint e2e passes? The card AC currently requires the e2e."]}
```
