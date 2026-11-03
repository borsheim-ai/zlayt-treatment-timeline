# T-183 security review, round 2 (security-reviewer, claude-sonnet-5-5)

Scope: commit 275e4ca, tested from `git archive 275e4ca` at `artifacts/review-evidence/T-183-r2/head`. At the first check `git rev-parse --short HEAD` was 275e4ca; at write time it was f3d42a2. `git diff --stat 275e4ca HEAD -- app Dockerfile requirements.txt` shows 17 files changed, all of them frontend/guided files plus `api.py` (+17/-1, a static-file mount that falls back to index.html). `limits.py` and the two limit hooks did not move, and the `/api` routes are registered before that mount. Probes: `probe_r2.py`, `probe_rejudge.py` and their `.out` files beside the archive. I started servers on free ports of my own (ephemeral ports from the OS) and stopped only those PIDs.

Verdict: **pass**. There is no blocker and no major. The round-1 major (unbounded stored cases and runs) is closed. One minor and one nit remain.

## Round-1 major: closed

Public demo build (`ZLAYT_MODE` unset), `LLM_BACKEND=anthropic-api` with a sentinel key present and `ENABLE_LIVE` unset:
- **300 sequential creates:** `Counter({201: 200, 429: 100})` in 3.3 s. The sqlite table held exactly 200 cases.
- **150 concurrent runs on those cases:** `Counter({429: 140, 202: 10})` in 1.4 s. A sample run holds its slot for about 0.1 s, so more than 4 can be admitted over a burst, but never more than 4 at once (see the race answer below).
- **429 bodies are one plain sentence:**
  - `{"error":{"code":"busy","message":"This demo is full right now. Try again later.","detail":{"reason":"demo_full"}}}`
  - `{"error":{"code":"busy","message":"This demo is busy right now. Try again in a minute.","detail":{"reason":"demo_busy"}}}`
- **No leak:** 451 captured responses (headers and bodies) contained none of `Traceback`, `File "`, `/Users`, `sk-ant`, `sqlite`, `DEMO_MAX`, `limits.py` or the sentinel. The server log was 0 bytes. `/api/health` stayed 200 throughout.
- **Order of checks:** a non-sample paste while the table is full still returns 409 "This demo only runs the recorded sample cases." (the demo gate wins over 429, nothing stored).
- **Bad env values:** `DEMO_MAX_CASES` and `DEMO_MAX_RUNS` set to `0`, `-5`, `abc` or empty all fall back to the defaults (3 creates each returned 201), so a typo can neither switch the cap off nor lock the demo shut.

## Is "creates may overshoot by a few under a race" acceptable? Yes, and in this build it does not overshoot

Measured: `DEMO_MAX_CASES=20` with 100 simultaneous creates gave `Counter({429: 80, 201: 20})` and 20 stored. `DEMO_MAX_RUNS` default with 60 simultaneous runs gave 13 admitted and 47 refused, with at most 4 in flight by construction. The reason is structural: `create_case` is `async def` (api.py:286) and `make_case` (api.py:344-357) has no `await` between the `COUNT(*)` and the insert. `run_case` (api.py:436) likewise has no `await` between the `len(runs)` check (api.py:450) and `runs[token] = ...` (api.py:455). Both run on the single event-loop thread. `app/main.py:14` starts one uvicorn process with no `workers=`. So the "few" can only appear if someone adds uvicorn workers or turns these routes into plain `def`. Even then the excess is bounded by the number of simultaneous requests, never unbounded. For a resource bound on a synthetic demo that is acceptable. The wording in the docstring is more pessimistic than the code; see the nit.

## Dev mode is unlimited

`ZLAYT_MODE=local` with `DEMO_MAX_CASES=5` and `DEMO_MAX_RUNS=1` set (so the caps would bite if they applied): 300 creates all 201 with 300 stored, 150 concurrent runs all 202 (`Counter({202: 150})`). `limits.case_full` and `limits.runs_busy` return `None` when `local` is true (limits.py:34-35, 41-42).

## Tests

`tests/unit/test_t183_limits.py` in the archive: 9 passed (`.venv/bin/python -m pytest -p no:cacheprovider`).

## What I would still change (not a spec violation)

A refuse-when-full cap turns resource exhaustion into a lockout. One scripted client creates 200 cases in about 2 s (300 requests took 3.3 s) and every other visitor gets 429 "This demo is full right now" on `POST /api/cases` until the 24 h retention purge (db.py:17, run only from make_case at api.py:356 and api.py:217) reaches the attacker's cases. I confirmed that while full a legitimate create returns 429, and that `DELETE` of one case (needs that case's token) frees one slot (204, then 201). That is the trade-off the worker documented ("oldest cases are not pruned, create is refused instead"); round 1 offered it as an allowed option, so this is a "would have done it differently" call, filed as minor.

```json
{"card": "T-183", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of 275e4ca at artifacts/review-evidence/T-183-r2/head (HEAD was 275e4ca at first check, f3d42a2 at write time; later changes are frontend/guided files and a static-file mount in api.py, limits.py and both hooks unchanged); demo and local builds on ephemeral 127.0.0.1 ports; no live model call",
 "exercised": [
  "read reviews/T-183-security.md (round 1) and python3 tools/board.py show T-183",
  "read personas/security.md and app/backend/limits.py; read the two hooks in api.py (create_case/make_case 286-357, run_case 436-455) and git show 275e4ca -- app/backend/api.py",
  "probe_r2.py A: demo build, sentinel key + LLM_BACKEND=anthropic-api, ENABLE_LIVE unset: 300 sequential creates (201x200, 429x100, 200 stored), 150 concurrent runs (202x10, 429x140), 429 bodies, legitimate create while full (429), DELETE own case then create (204, 201), health 200, non-sample paste while full (409), scan of 451 responses and the server log for Traceback, File, /Users, sk-ant, sqlite, DEMO_MAX, limits.py and the sentinel (none; log 0 bytes)",
  "probe_r2.py B: DEMO_MAX_CASES=20 with 100 simultaneous creates: 201x20, 429x80, 20 stored",
  "probe_r2.py C: default caps, 60 simultaneous runs: 202x13, 429x47; one sample run holds a slot about 0.1 s",
  "probe_r2.py D: DEMO_MAX_CASES/DEMO_MAX_RUNS = 0, -5, abc, empty: default applies (201 each)",
  "probe_r2.py E: ZLAYT_MODE=local with caps set to 5 and 1: 300 creates all 201 (300 stored), 150 concurrent runs all 202",
  "probe_rejudge.py: 90 concurrent /rejudge on 3 finished demo cases: 409x78, 200x12 in 0.3 s, asked 0 (recorded replay only), health 200",
  ".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_t183_limits.py in the archive: 9 passed",
  "git rev-parse --short HEAD (275e4ca, later f3d42a2); git diff --stat 275e4ca HEAD -- app Dockerfile requirements.txt (17 files, frontend plus api.py static mount); grep memory/SCOPE_CUTS.md (row 24 records the limiter cut); grep app/db/db.py RETENTION_SECONDS 24 h"
 ],
 "verdict": "pass",
 "scores": {"key_exposure": 5, "demo_mode_isolation": 5, "input_limits": 5, "error_plainness": 5, "resource_abuse_resistance": 4, "cut_documentation": 5},
 "findings": [
  {"severity": "minor",
   "title": "A full case table locks every visitor out for up to 24 h; one scripted client can do it in about 2 seconds",
   "evidence": "probe_r2.py A: 300 sequential creates in 3.3 s gave 201x200 then 429x100; 'legit create while full: 429 ... This demo is full right now. Try again later.' Only the 24 h purge (db.py:17 RETENTION_SECONDS, purge_expired db.py:297, called at api.py:356 and api.py:217) or a DELETE with that case's token frees a slot; DELETE of one case gave 204 then a create returned 201. The handoff states 'oldest cases are not pruned, create is refused instead'.",
   "why_it_matters": "The cap closes disk and CPU exhaustion, but the public link can still be made unusable by one curl loop, repeated once a day. No money, secret or data is involved, so this is availability only. It is a design preference, not a spec violation: round 1 allowed 'refused' as the alternative to pruning.",
   "fix": "When the table is full, delete the oldest case that is older than a short floor (for example 1 hour) before refusing, so only truly fresh floods get a 429; or give demo-created cases a shorter retention (for example 2 hours) since the sample is a recorded case that is cheap to recreate.",
   "acceptance_test": "With DEMO_MAX_CASES=3, create 3 cases, age one past the floor, then a 4th create returns 201 and the stored count stays 3; with all 3 younger than the floor the 4th returns 429 with the same one-sentence body."},
  {"severity": "nit",
   "title": "The 'soft bound / overshoot by a few' wording understates what the code does, and nothing pins the reason",
   "evidence": "limits.py docstring: 'simultaneous creates can overshoot it by a few'. probe_r2.py B: DEMO_MAX_CASES=20, 100 simultaneous creates, 20 stored. The exactness depends on create_case and run_case being async def with no await between check and insert (api.py:286, 344-357, 436, 450-455) and on one uvicorn process (app/main.py:14).",
   "why_it_matters": "A later change to plain `def` routes or `workers=N` would turn an exact bound into a leaky one without any test failing, and the comment would not tell the next person why it was exact.",
   "fix": "State in the limits.py docstring that the bound is exact because the check and insert run on one event-loop thread, and add a test with many simultaneous creates against a small cap that asserts the stored count equals the cap.",
   "acceptance_test": "A test starts 50 threads creating against DEMO_MAX_CASES=5 and asserts exactly 5 stored."}
 ],
 "whats_right": [
  "Both caps are enforced after input validation and before any state changes, and a refused request leaves nothing stored and returns a one-sentence JSON 429 with no trace, key or env-var name.",
  "A zero, negative or unreadable cap value falls back to the default, so a typo cannot turn the limit off or lock the demo shut.",
  "Local mode is unlimited, so the caps cannot interfere with development or the recorded-answer workflow."
 ],
 "questions_for_chris": []}
```

Correction (line refs): the local early-returns in limits.py are at lines 33-34 (case_full) and 40-41 (runs_busy), not 34-35 and 41-42 as written above.
