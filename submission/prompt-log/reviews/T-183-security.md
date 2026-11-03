# T-183 security review (security-reviewer, claude-sonnet-5-5)

Scope: HEAD 33e88c6 (card commit 4671eee is an ancestor; `git diff --quiet 33e88c6 HEAD -- app Dockerfile requirements.txt` was clean at write time). I tested a `git archive HEAD` copy at `artifacts/review-evidence/T-183/head`, with probes `probe1.py`, `probe2.py` and `probe3.py` beside it (outputs in `probe*.out`).

Verdict: **changes**. There is no blocker and one major.

The four hardening items hold in demo mode:
- **Key:** I sent 73 requests per run, including static files, every case route and error paths. Two servers ran: one with no key, and one with a sentinel key, `LLM_BACKEND=anthropic-api` and `ENABLE_LIVE` unset. The sentinel and the string `sk-ant` appeared in no response body or header. The server log was 0 bytes, so no case text or key was logged. A key sent in a header or body (BYOK attempts) was ignored and not echoed.
- **Demo mode:** with no key and with a key, health reports `backend: fixture`, `answers: prepared`, `live_enabled: false`. The sample ran create, run and `ready` with 9 entries, 4 amounts and 10 flags.
- **Size limits:** 60,001 characters, a 600 KB body and a chunked body of 640 KB all returned 413 with "Input is too large." Other text returns 409 "This demo only runs the recorded sample cases." and is not stored. A PDF upload returns 409 in demo mode.
- **Error states:** about 20 bad requests (bad JSON, an array body, missing or empty text, an unknown token, wrong method, unknown route, a markup title, a lone surrogate) all returned `{"error":{"code","message"}}` with a plain sentence. None showed a traceback or framework text. `/docs` and `/openapi.json` are 404. `/api/cases`, `/api/library` and the library POST are 404 in the public build.

Other checks:
- A live `anthropic-api` start with `ENABLE_LIVE=1`, a key and no `PROVIDER_CAP_CONFIRMED` exits 1 with a RuntimeError that does not echo the key.
- The CSP is set on API and static responses (`script-src 'self'`, no inline script except one hashed `onclick`).
- The Dockerfile runs as uid 1000, sets no key and no `ENABLE_LIVE`, and `.dockerignore` is an allow-list.
- `tools/check_secrets.py` reports ok on 3477 files. `git log --all -G'sk-ant-...'` finds no added or removed key-shaped line in any commit. `.env` is ignored (`.gitignore:25`). `.env.example` has no value.
- `pip-audit --no-deps` on `requirements.txt` found no known vulnerabilities. gitleaks is not installed.
- The frontend has no `innerHTML`, `eval` or `document.write`. The one grep hit is a comment (`sidebyside.js:5`).

## The two recorded cuts, for a public demo-only link

- **D-011, no bring-your-own-key: acceptable.** It removes the one path where a user-supplied secret could be logged or echoed, and the probe confirmed a supplied key is ignored. Nothing in the demo needs it. This is a "would have done it differently" call, not a spec violation.
- **D-020, no in-app rate limit or spend cap: acceptable for the wallet, not for resources.**
  - **Why the wallet is safe.** The public build cannot make a model call. `provider.backend_name()` returns `fixture` unless `ENABLE_LIVE=1`, the image never sets it, and the process refuses to start in live `anthropic-api` mode without `PROVIDER_CAP_CONFIRMED=1`. Probes A and B showed zero live attempts with a key present. So "denial of wallet" is closed by construction, and a limiter would protect nothing there.
  - **What remains open.** With no limiter, a public client can fill storage and CPU (finding 1). The wallet argument does not cover that, so the cut is acceptable only once a small storage or concurrency bound exists.

```json
{"card": "T-183", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of HEAD 33e88c6 (card commit 4671eee is an ancestor) at artifacts/review-evidence/T-183/head; demo build env, servers on 127.0.0.1:17861-17865; sample case; no live model call was made",
 "exercised": [
  "python3 tools/board.py show T-183 (read the summary table and handoff)",
  "read personas/security.md, memory/ORCHESTRATOR_DECISIONS.md D-011/D-020, memory/SCOPE_CUTS.md, docs/CONTRACT.md:314, README.md:44",
  "read app/backend/api.py, app/config.py, app/main.py, app/llm/provider.py, store.live_enabled, Dockerfile, .dockerignore, requirements.txt",
  ".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_t183_hardening.py in the archive: 15 passed",
  "probe1.py: two real uvicorn servers (no key; sentinel key + LLM_BACKEND=anthropic-api + ENABLE_LIVE unset); 73 requests each (health, static files, create, run, status, trace, judges, audit, export, narrative, billing, ~20 error probes, 60,001-char, 600 KB and chunked oversize bodies, BYOK header and body); scanned every response and the server log for the sentinel and 'sk-ant'",
  "probe2.py: ENABLE_LIVE=1 + anthropic-api + key without PROVIDER_CAP_CONFIRMED (exit 1, key not echoed); CSP/nosniff/no-store headers; export-before-run 422 body; 300 creates and 150 concurrent runs against the demo build",
  "probe3.py: bytes stored per created case and per run case; sequential create rate",
  ".venv/bin/python tools/check_secrets.py (ok, 3477 files); git log --all -G key-pattern over history (0 matching lines); git check-ignore .env; .env.example key line",
  "pip-audit -r requirements.txt --no-deps --disable-pip in a scratchpad venv: no known vulnerabilities",
  "grep of app/frontend for innerHTML/eval/document.write"
 ],
 "verdict": "changes",
 "scores": {"key_exposure": 5, "demo_mode_isolation": 5, "input_limits": 5, "error_plainness": 5, "resource_abuse_resistance": 2, "cut_documentation": 3},
 "findings": [
  {"severity": "major",
   "title": "Public demo has no bound on stored cases or concurrent runs: any client can fill the disk and burn CPU",
   "evidence": "No limiter, case cap or run cap exists (api.py create_case/make_case, run_case; retention is only a 24 h age purge, db.py:17). Measured on the archive, demo build: 300 sequential sample creates all returned 201 in 5.1 s (about 62/s from one client, probe3: 'sequential creates/sec: 62'); 150 concurrent /run calls all returned 202 in 5.5 s (Counter({202: 150})), each spawning a thread (api.py:437-440, one per token, none shared); the sqlite file was 28,246,016 bytes after 301 cases and 150 runs; per case 11,100 bytes created-only and 166,420 bytes more per run (probe3). Arithmetic from those figures: one client creating and running at about 30 runs/s writes about 5 MB/s, or 10 GB in about 30 minutes, and creates alone write about 0.7 MB/s. DATA_DIR is the container disk (Dockerfile line 21). A scripted client therefore degrades or takes down the shared demo for all users. No money is spent.",
   "why_it_matters": "My dossier goal 1 is that a public link cannot be abused to exhaust resources. D-020 removed the limiter on the argument that the demo makes no model calls. That argument closes denial of wallet but not disk, thread or SQLite write exhaustion, which are open. This is a major, not a blocker: no model call, no secret, and no data leak is involved.",
   "fix": "Add a small deterministic bound in the demo build and answer with the existing plain-error shape and a 429: (a) a global cap on stored cases (for example 500), after which the oldest expired or oldest cases are purged or the create is refused with 'The demo is busy. Try again in a few minutes.'; (b) a cap on runs in flight, as pdf_checks.MAX_PDF_JOBS already does for PDFs; (c) optionally reuse an existing identical sample case's records rather than storing a new copy per create. A per-IP limiter is not needed for this.",
   "acceptance_test": "With a test DB, POST /api/cases {sample:true} N+1 times, where N is the cap: the extra create returns 429 with a one-sentence message, the stored case count stays at N, and /api/health still returns 200. Start more runs than the in-flight cap: the extras return 429 'busy', not 500."},
  {"severity": "minor",
   "title": "The D-020 cut of the CONTRACT's per-session rate limit and spend cap is not in SCOPE_CUTS.md or the submission",
   "evidence": "docs/CONTRACT.md:314 lists 'server-side API key with per-session rate limit and spend cap ... optional bring-your-own-key' as M4 scope; CONTRACT.md:260 says cuts are recorded in SCOPE_CUTS.md. memory/SCOPE_CUTS.md has a BYOK row (row 17, D-011) but `grep -i 'limiter|rate limit|spend|D-020' memory/SCOPE_CUTS.md` returns only the unrelated T-050 debt row (line 46). The limiter cut exists only in memory/ORCHESTRATOR_DECISIONS.md D-020 and the card note. grep -i 'rate limit|per-IP|limiter' over submission/*.md, README.md and docs/RUNBOOK.md returns no hits.",
   "why_it_matters": "A grader reading CONTRACT.md:314 will look for the limiter. The cut is legitimate (the public build makes zero model calls), but an unrecorded deviation from a stated contract line is the thing the cut log exists to prevent. Separate from finding 1, which is about behaviour.",
   "fix": "Add a SCOPE_CUTS row: 'In-app per-session rate limit and spend cap: cut (D-020/ADR-006); public build is demo-only and makes no model calls; live mode is local-only and refuses to start without PROVIDER_CAP_CONFIRMED=1.' Add one sentence to the README or product note stating the same.",
   "acceptance_test": "grep -i 'rate limit' memory/SCOPE_CUTS.md returns the new row; the README or submission names the demo-only reason."},
  {"severity": "nit",
   "title": "PROVIDER_CAP_CONFIRMED is a self-attested flag, not a check",
   "evidence": "api.py:111 refuses only on the env var being unequal to '1'; nothing verifies a provider limit exists. Live mode is local-only, so this is documentation-grade protection.",
   "why_it_matters": "If a future deploy flips live on, the startup check gives more confidence than it earns.",
   "fix": "Say in the README that the flag is a promise, not a check, or add an in-app call counter as the card note suggests.",
   "acceptance_test": "README states what the flag does and does not verify."}
 ],
 "whats_right": [
  "Demo isolation is enforced in provider.backend_name(), so no route can reach a model without ENABLE_LIVE=1, and with a key present the probe still showed backend fixture and no key in any output.",
  "Oversize input is rejected before parsing or storage, including a chunked body with no content-length, and every error is a one-sentence JSON body with no trace.",
  "Startup refuses live anthropic-api without the provider-cap confirmation, and the failure message does not echo the key."
 ],
 "questions_for_chris": []}
```
