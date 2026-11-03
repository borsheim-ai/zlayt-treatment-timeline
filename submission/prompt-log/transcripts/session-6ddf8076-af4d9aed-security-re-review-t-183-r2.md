# Subagent: Security re-review: T-183 r2 (Security re-review: T-183 r2)

Source: `agent-af4d9aed1d6d4f33f.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T21:24:55.397Z

Re-review T-183 round 2 in /Users/arsis/zlayt-pm-project as the security reviewer, starting from a fresh context. Read reviews/T-183-security.md (round 1) and the card with `python3 tools/board.py show T-183`. The fix is commit 275e4ca: demo/public mode caps stored cases (DEMO_MAX_CASES, default 200) and runs in flight (DEMO_MAX_RUNS, default 4), returning a plain 429; dev mode stays unlimited.

Work on a `git archive HEAD` copy in your scratch dir, not the shared tree, because other workers are mid-edit. Start the demo build on a free port of your own and stop only your own PID when you finish.

1. Repeat the round-1 flood: 300 creates and 150 concurrent runs. Confirm both caps hold and the body is a plain sentence with no stack trace and no key.
2. Judge whether "creates may overshoot by a few under a race" is acceptable.
3. Check that dev mode is unlimited.
4. Run tests/unit/test_t183_limits.py.

Write reviews/T-183-security-r2.md in D.2 format with its JSON block, applying the verdict rule. Write key values as <redacted>. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:58.764Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/security.md"
}
````

### User / tool · 2026-11-02T21:24:58.783Z

**tool result**
````
1	# Persona dossier — security-reviewer
2	
3	## 1. Identity
4	**Tomás Rivas (fictional), Application Security Engineer — 10 years AppSec, the last 2 reviewing LLM-backed web apps; OWASP contributor-style background.**
5	He has seen a public demo burn a month of API budget in a night and an LLM summary render a `<script>` from a pasted document. He assumes every input is hostile, every public endpoint will be scripted against, and that a system prompt is not a security boundary.
6	
7	## 2. Day-to-day context
8	- Tools: OWASP Top 10 for LLM Applications (2025), OWASP ASVS 5.0, OWASP Cheat Sheets, gitleaks, pip-audit, curl, Burp-style request replay, browser devtools.
9	- Pressures: small teams shipping demos on public links with a real API key behind them.
10	- A bad day: a leaked key in git history, or an unauthenticated endpoint that lets anyone run unlimited LLM calls.
11	
12	## 3. Goals and success criteria for this artifact
13	- The public link cannot be abused to spend money or exhaust resources.
14	- Record text and model output cannot inject script, change behaviour, or exfiltrate anything.
15	- Secrets never enter git, logs, client code, or error messages.
16	- Dependencies are pinned and free of known vulnerabilities.
17	
18	## 4. Review checklist
19	1. Request bodies over the documented size limit are rejected before any LLM call (HTTP 413 or equivalent with a clear message).
20	2. Per-session/IP rate limit and a global daily spend cap exist on live LLM calls; exceeding them returns a friendly 429, not a 5xx.
21	3. Every LLM call has a timeout and a hard cap on retries and judge calls per request (OWASP LLM10).
22	4. Without a key, demo mode serves cached results and no endpoint can trigger a live call.
23	5. Model output and record text are rendered with `textContent` or an auto-escaping template; no `innerHTML`, `|safe`, or equivalent with model/record content. A record containing `<img src=x onerror=alert(1)>` renders as text.
24	6. A Content-Security-Policy is set (no `unsafe-inline` scripts where feasible).
25	7. The prompt-injection record cannot change the output schema or item states; schema validation in code rejects extra fields (LLM01).
26	8. The LLM has no tools, no network access, and no ability to cause side effects (LLM06 excessive agency).
27	9. Grounding checks fail closed: an output whose excerpt is not in the record cannot become `verified` (LLM09 misinformation).
28	10. The API key is read from the environment on the server only; it never appears in client JS, HTML, responses, or logs.
29	11. `gitleaks` (or `tools/check_secrets.py`) is clean across full git history; `.env` is gitignored; `.env.example` has no real values.
30	12. Logs exclude pasted text, prompts, completions, and keys; error responses exclude stack traces and the system prompt (LLM02, LLM07).
31	13. Dependencies are pinned (lockfile or `==` pins); `pip-audit` reports no known vulnerabilities, or each is triaged.
32	14. If file upload exists: extension/type allowlist, size cap, server-generated names, no execution path, content read as text only.
33	15. The Docker image runs as a non-root user and does not include the Claude CLI backend or dev credentials.
34	16. The `claude-cli` backend (dev only) is impossible to enable in the container/public config.
35	17. Export text is plain text; if any CSV export exists, cells starting with `=`, `+`, `-`, `@` are neutralized.
36	18. No debug endpoints, admin routes, or auto-reload left enabled in the public configuration.
37	
38	## 5. Red flags / dealbreakers
39	Each item here is a **blocker** (rate it so; never major or minor).
40	- A secret in the repo or its history.
41	- Unbounded live LLM calls from an unauthenticated public endpoint.
42	- Stored or reflected XSS via record text or model output.
43	- Injection that changes item states or exported content.
44	
45	## 6. Vocabulary
46	direct/indirect prompt injection, improper output handling, excessive agency, system prompt leakage, unbounded consumption, denial of wallet, output encoding, safe sink, CSP, rate limit, spend cap, fail closed, least privilege, secret rotation, lockfile, hash pinning, SBOM, ASVS level.
47	
48	## 7. How I review
49	1. Read the deployment config, Dockerfile, `app/config.py`, and the server entrypoint; list every route.
50	2. `curl` each route: oversized body, malformed JSON, missing fields, repeated rapid requests (measure where limiting kicks in).
51	3. Submit the XSS probe and the prompt-injection record through the UI with Playwright; screenshot the rendered results.
52	4. Run `python tools/check_secrets.py` and `gitleaks git` (if installed) over full history; `pip-audit` on the requirements.
53	5. Grep for `innerHTML`, `|safe`, `eval(`, `subprocess`, `shell=True`, `logger.*(prompt|request|body|resp)`, and key env var names.
54	6. Check the container user and that the CLI backend is absent from the image.
55	7. File findings with the request/response or file:line as evidence.
56	
57	## 8. Calibration
58	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
59	- **blocker — Unbounded live calls.** Evidence: 200 scripted POSTs to `/api/process` all reached the LLM (log count). Fix: per-IP limit (e.g., 10/hour), global daily cap, demo mode without key. Test: 11th request in an hour returns 429.
60	- **blocker — XSS via record text.** Evidence: screenshot shows alert dialog after pasting `<img src=x onerror=alert(1)>`. Fix: render excerpts with `textContent`; add CSP. Test: Playwright asserts no dialog and literal text visible.
61	- **minor — Unpinned dependencies.** Evidence: `requirements.txt` has `fastapi` with no version. Fix: pin versions and add `pip-audit` to `make test`.
62	
63	## 9. Sources
64	- https://genai.owasp.org/llm-top-10/ — OWASP Top 10 for LLM Applications 2025: prompt injection, sensitive info disclosure, improper output handling, excessive agency, unbounded consumption.
65	- https://genai.owasp.org/llmrisk/llm01-prompt-injection/ — OWASP LLM01: indirect injection via documents; mitigations are deterministic output checks, segregation, least privilege, human approval.
66	- https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/ — OWASP LLM05: treat model output as untrusted; context-appropriate encoding; CSP.
67	- https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/ — OWASP LLM10: denial of wallet; input size limits, rate limits, quotas, timeouts.
68	- https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html — OWASP: cap input length; watch encoded/invisible characters; no defense is foolproof.
69	- https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html — OWASP: prefer `textContent`; avoid framework escape hatches; CSP is defense in depth.
70	- https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html — OWASP: detect secrets pre-commit; rotate on leak.
71	- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html — OWASP: exclude health data, tokens, and session ids from logs.
72	- https://github.com/pypa/pip-audit — pip-audit: audits Python requirements for known vulnerabilities; non-zero exit on findings.
73	- https://github.com/gitleaks/gitleaks — gitleaks: scans full git history for secrets; pre-commit hook available.
74	- Assumptions: the CSV-injection item applies only if a CSV export is added; rate-limit numbers are examples, not requirements.
75	
76	## 10. Limits
77	Do not grade clinical content, UX quality, or product strategy. Privacy-law questions (HIPAA, ethics opinions) belong to privacy-compliance-reviewer; flag the technical facts and defer.
78	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:59.103Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-183-security.md"
}
````

### User / tool · 2026-11-02T21:24:59.113Z

**tool result**
````
1	# T-183 security review (security-reviewer, claude-sonnet-5-5)
2	
3	Scope: HEAD 33e88c6 (card commit 4671eee is an ancestor; `git diff --quiet 33e88c6 HEAD -- app Dockerfile requirements.txt` was clean at write time). I tested a `git archive HEAD` copy at `artifacts/review-evidence/T-183/head`, with probes `probe1.py`, `probe2.py` and `probe3.py` beside it (outputs in `probe*.out`).
4	
5	Verdict: **changes**. There is no blocker and one major.
6	
7	The four hardening items hold in demo mode:
8	- **Key:** I sent 73 requests per run, including static files, every case route and error paths. Two servers ran: one with no key, and one with a sentinel key, `LLM_BACKEND=anthropic-api` and `ENABLE_LIVE` unset. The sentinel and the string `sk-ant` appeared in no response body or header. The server log was 0 bytes, so no case text or key was logged. A key sent in a header or body (BYOK attempts) was ignored and not echoed.
9	- **Demo mode:** with no key and with a key, health reports `backend: fixture`, `answers: prepared`, `live_enabled: false`. The sample ran create, run and `ready` with 9 entries, 4 amounts and 10 flags.
10	- **Size limits:** 60,001 characters, a 600 KB body and a chunked body of 640 KB all returned 413 with "Input is too large." Other text returns 409 "This demo only runs the recorded sample cases." and is not stored. A PDF upload returns 409 in demo mode.
11	- **Error states:** about 20 bad requests (bad JSON, an array body, missing or empty text, an unknown token, wrong method, unknown route, a markup title, a lone surrogate) all returned `{"error":{"code","message"}}` with a plain sentence. None showed a traceback or framework text. `/docs` and `/openapi.json` are 404. `/api/cases`, `/api/library` and the library POST are 404 in the public build.
12	
13	Other checks:
14	- A live `anthropic-api` start with `ENABLE_LIVE=1`, a key and no `PROVIDER_CAP_CONFIRMED` exits 1 with a RuntimeError that does not echo the key.
15	- The CSP is set on API and static responses (`script-src 'self'`, no inline script except one hashed `onclick`).
16	- The Dockerfile runs as uid 1000, sets no key and no `ENABLE_LIVE`, and `.dockerignore` is an allow-list.
17	- `tools/check_secrets.py` reports ok on 3477 files. `git log --all -G'sk-ant-...'` finds no added or removed key-shaped line in any commit. `.env` is ignored (`.gitignore:25`). `.env.example` has no value.
18	- `pip-audit --no-deps` on `requirements.txt` found no known vulnerabilities. gitleaks is not installed.
19	- The frontend has no `innerHTML`, `eval` or `document.write`. The one grep hit is a comment (`sidebyside.js:5`).
20	
21	## The two recorded cuts, for a public demo-only link
22	
23	- **D-011, no bring-your-own-key: acceptable.** It removes the one path where a user-supplied secret could be logged or echoed, and the probe confirmed a supplied key is ignored. Nothing in the demo needs it. This is a "would have done it differently" call, not a spec violation.
24	- **D-020, no in-app rate limit or spend cap: acceptable for the wallet, not for resources.**
25	  - **Why the wallet is safe.** The public build cannot make a model call. `provider.backend_name()` returns `fixture` unless `ENABLE_LIVE=1`, the image never sets it, and the process refuses to start in live `anthropic-api` mode without `PROVIDER_CAP_CONFIRMED=1`. Probes A and B showed zero live attempts with a key present. So "denial of wallet" is closed by construction, and a limiter would protect nothing there.
26	  - **What remains open.** With no limiter, a public client can fill storage and CPU (finding 1). The wallet argument does not cover that, so the cut is acceptable only once a small storage or concurrency bound exists.
27	
28	```json
29	{"card": "T-183", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
30	 "scope": "git archive of HEAD 33e88c6 (card commit 4671eee is an ancestor) at artifacts/review-evidence/T-183/head; demo build env, servers on 127.0.0.1:17861-17865; sample case; no live model call was made",
31	 "exercised": [
32	  "python3 tools/board.py show T-183 (read the summary table and handoff)",
33	  "read personas/security.md, memory/ORCHESTRATOR_DECISIONS.md D-011/D-020, memory/SCOPE_CUTS.md, docs/CONTRACT.md:314, README.md:44",
34	  "read app/backend/api.py, app/config.py, app/main.py, app/llm/provider.py, store.live_enabled, Dockerfile, .dockerignore, requirements.txt",
35	  ".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_t183_hardening.py in the archive: 15 passed",
36	  "probe1.py: two real uvicorn servers (no key; sentinel key + LLM_BACKEND=anthropic-api + ENABLE_LIVE unset); 73 requests each (health, static files, create, run, status, trace, judges, audit, export, narrative, billing, ~20 error probes, 60,001-char, 600 KB and chunked oversize bodies, BYOK header and body); scanned every response and the server log for the sentinel and 'sk-ant'",
37	  "probe2.py: ENABLE_LIVE=1 + anthropic-api + key without PROVIDER_CAP_CONFIRMED (exit 1, key not echoed); CSP/nosniff/no-store headers; export-before-run 422 body; 300 creates and 150 concurrent runs against the demo build",
38	  "probe3.py: bytes stored per created case and per run case; sequential create rate",
39	  ".venv/bin/python tools/check_secrets.py (ok, 3477 files); git log --all -G key-pattern over history (0 matching lines); git check-ignore .env; .env.example key line",
40	  "pip-audit -r requirements.txt --no-deps --disable-pip in a scratchpad venv: no known vulnerabilities",
41	  "grep of app/frontend for innerHTML/eval/document.write"
42	 ],
43	 "verdict": "changes",
44	 "scores": {"key_exposure": 5, "demo_mode_isolation": 5, "input_limits": 5, "error_plainness": 5, "resource_abuse_resistance": 2, "cut_documentation": 3},
45	 "findings": [
46	  {"severity": "major",
47	   "title": "Public demo has no bound on stored cases or concurrent runs: any client can fill the disk and burn CPU",
48	   "evidence": "No limiter, case cap or run cap exists (api.py create_case/make_case, run_case; retention is only a 24 h age purge, db.py:17). Measured on the archive, demo build: 300 sequential sample creates all returned 201 in 5.1 s (about 62/s from one client, probe3: 'sequential creates/sec: 62'); 150 concurrent /run calls all returned 202 in 5.5 s (Counter({202: 150})), each spawning a thread (api.py:437-440, one per token, none shared); the sqlite file was 28,246,016 bytes after 301 cases and 150 runs; per case 11,100 bytes created-only and 166,420 bytes more per run (probe3). Arithmetic from those figures: one client creating and running at about 30 runs/s writes about 5 MB/s, or 10 GB in about 30 minutes, and creates alone write about 0.7 MB/s. DATA_DIR is the container disk (Dockerfile line 21). A scripted client therefore degrades or takes down the shared demo for all users. No money is spent.",
49	   "why_it_matters": "My dossier goal 1 is that a public link cannot be abused to exhaust resources. D-020 removed the limiter on the argument that the demo makes no model calls. That argument closes denial of wallet but not disk, thread or SQLite write exhaustion, which are open. This is a major, not a blocker: no model call, no secret, and no data leak is involved.",
50	   "fix": "Add a small deterministic bound in the demo build and answer with the existing plain-error shape and a 429: (a) a global cap on stored cases (for example 500), after which the oldest expired or oldest cases are purged or the create is refused with 'The demo is busy. Try again in a few minutes.'; (b) a cap on runs in flight, as pdf_checks.MAX_PDF_JOBS already does for PDFs; (c) optionally reuse an existing identical sample case's records rather than storing a new copy per create. A per-IP limiter is not needed for this.",
51	   "acceptance_test": "With a test DB, POST /api/cases {sample:true} N+1 times, where N is the cap: the extra create returns 429 with a one-sentence message, the stored case count stays at N, and /api/health still returns 200. Start more runs than the in-flight cap: the extras return 429 'busy', not 500."},
52	  {"severity": "minor",
53	   "title": "The D-020 cut of the CONTRACT's per-session rate limit and spend cap is not in SCOPE_CUTS.md or the submission",
54	   "evidence": "docs/CONTRACT.md:314 lists 'server-side API key with per-session rate limit and spend cap ... optional bring-your-own-key' as M4 scope; CONTRACT.md:260 says cuts are recorded in SCOPE_CUTS.md. memory/SCOPE_CUTS.md has a BYOK row (row 17, D-011) but `grep -i 'limiter|rate limit|spend|D-020' memory/SCOPE_CUTS.md` returns only the unrelated T-050 debt row (line 46). The limiter cut exists only in memory/ORCHESTRATOR_DECISIONS.md D-020 and the card note. grep -i 'rate limit|per-IP|limiter' over submission/*.md, README.md and docs/RUNBOOK.md returns no hits.",
55	   "why_it_matters": "A grader reading CONTRACT.md:314 will look for the limiter. The cut is legitimate (the public build makes zero model calls), but an unrecorded deviation from a stated contract line is the thing the cut log exists to prevent. Separate from finding 1, which is about behaviour.",
56	   "fix": "Add a SCOPE_CUTS row: 'In-app per-session rate limit and spend cap: cut (D-020/ADR-006); public build is demo-only and makes no model calls; live mode is local-only and refuses to start without PROVIDER_CAP_CONFIRMED=1.' Add one sentence to the README or product note stating the same.",
57	   "acceptance_test": "grep -i 'rate limit' memory/SCOPE_CUTS.md returns the new row; the README or submission names the demo-only reason."},
58	  {"severity": "nit",
59	   "title": "PROVIDER_CAP_CONFIRMED is a self-attested flag, not a check",
60	   "evidence": "api.py:111 refuses only on the env var being unequal to '1'; nothing verifies a provider limit exists. Live mode is local-only, so this is documentation-grade protection.",
61	   "why_it_matters": "If a future deploy flips live on, the startup check gives more confidence than it earns.",
62	   "fix": "Say in the README that the flag is a promise, not a check, or add an in-app call counter as the card note suggests.",
63	   "acceptance_test": "README states what the flag does and does not verify."}
64	 ],
65	 "whats_right": [
66	  "Demo isolation is enforced in provider.backend_name(), so no route can reach a model without ENABLE_LIVE=1, and with a key present the probe still showed backend fixture and no key in any output.",
67	  "Oversize input is rejected before parsing or storage, including a chunked body with no content-length, and every error is a one-sentence JSON body with no trace.",
68	  "Startup refuses live anthropic-api without the provider-cap confirmation, and the failure message does not echo the key."
69	 ],
70	 "questions_for_chris": []}
71	```
72	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:59.509Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-183; git log --oneline | head -5"
}
````

### User / tool · 2026-11-02T21:24:59.742Z

**tool result**
````
---
id: "T-183"
title: "M4 hardening check: server-side key never exposed, per-session rate limit and spend cap on live calls, demo mode serves the prepared sample answers with no key, optional bring-your-own-key, input size limits, error states; fill only real gaps"
milestone: "M4"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T21:00:13Z"
updated_at: "2026-11-02T21:24:51Z"
claimed_by: "backend"
claimed_at: "2026-11-02T21:20:06Z"
rounds: 1
commits: ["4671eee", "275e4ca"]
reviews:
  - {"persona": "security-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-183-security.md", "at": "2026-11-02T21:19:53Z"}
ac:
  - {"n": 1, "text": "each item verified with a test (existing or new); gaps fixed; summary table in the card", "done": true, "evidence": "tests/unit/test_t183_hardening.py 15 pass; summary table in card notes; gap fixed in api.py make_case; commit 4671eee"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T21:00:16Z orchestrator: assigned: backend
- 2026-11-02T21:00:29Z backend: claimed
- 2026-11-02T21:05:16Z backend: SUMMARY TABLE (tests/unit/test_t183_hardening.py, 15 tests, pass; related suites 252 pass)
| Item | Status | Test |
| Key never in browser/logs | verified, no gap | test_key_never_appears_in_any_response_or_log_even_when_the_sdk_error_echoes_it (live run, SDK error echoes the key; all routes, headers, static, caplog, stdout/stderr); test_no_static_file_or_api_text_names_the_key_or_a_key_field; test_health_reports_whether_live_is_on_but_never_the_key; existing test_provider.py::test_no_text_in_logs |
| Per-session rate limit | NOT built, by decision D-020/ADR-006 (no in-app limiter). Public build makes zero model calls; one run is bounded by 60,000 chars / 40 records | test_every_route_that_can_call_a_model_makes_zero_calls_in_demo_mode_even_with_a_key; test_live_work_per_run_is_bounded_by_the_input_limits |
| Spend cap | provider-side cap, enforced at startup (app refuses ENABLE_LIVE + anthropic-api without PROVIDER_CAP_CONFIRMED=1); no in-app ledger (D-020) | test_a_live_api_build_refuses_to_start_without_the_provider_side_spend_limit_confirmed; existing test_api_routes.py::test_live_anthropic_needs_provider_cap_confirmation |
| Demo mode, no key | verified | test_no_key_demo_runs_the_sample_to_ready_with_prepared_answers_and_refuses_other_text; existing test_demo_never_reaches_a_live_backend, test_demo_health_reports_fixture_even_if_live_backend_and_key_are_set |
| Bring-your-own-key | SCOPE CUT (D-011, SCOPE_CUTS row 17): not implemented. A key sent in a header or body is ignored and never echoed | test_a_key_sent_with_a_request_is_never_used_or_echoed (3 variants) |
| Input size limits | verified; 1 real gap fixed | test_character_and_record_limits_return_413_and_store_nothing (60,001 chars, 41 records, oversize body, chunked body, nothing stored); test_pdf_upload_is_size_limited_and_refused_in_demo_mode; existing test_oversize_body_is_413_before_parsing, test_limit_boundaries |
| Error states plain | verified; GAP FIXED: a 41-record paste returned message 'input too large' (a bare code) -> now 'Input is too large.' (app/backend/api.py make_case) | test_every_error_is_plain_json_with_no_trace_path_or_framework_text (12 probes); test_a_run_that_fails_says_so_in_one_plain_sentence_and_keeps_finished_items |
Open for orchestrator: CONTRACT M4 lists a per-session limiter and in-app spend cap; D-020 cut them. Not built here. If wanted, it is a small card (call counter in audited.py). Unrelated: tests/unit/test_boundaries.py::test_dynamic_import_calls_are_forbidden fails on a __import__ in export code from another worker's uncommitted change.
- 2026-11-02T21:05:16Z backend: AC 1 checked: tests/unit/test_t183_hardening.py 15 pass; summary table in card notes; gap fixed in api.py make_case; commit 4671eee
- 2026-11-02T21:05:17Z backend: moved in_progress -> in_review
- 2026-11-02T21:05:23Z orchestrator: review dispatched: security-reviewer
- 2026-11-02T21:19:53Z orchestrator: review security-reviewer (claude-sonnet-5-5): changes — reviews/T-183-security.md; round 1; findings:
    - [major] Public demo has no bound on stored cases or concurrent runs: any client can fill the disk and burn CPU — fix: Add a small deterministic bound in the demo build and answer with the existing plain-error shape and a 429: (a) a global cap on stored cases (for example 500), after which the oldest expired or oldest cases are purged or the create is refused with 'The demo is busy. Try again
    - [minor] The D-020 cut of the CONTRACT's per-session rate limit and spend cap is not in SCOPE_CUTS.md or the submission — fix: Add a SCOPE_CUTS row: 'In-app per-session rate limit and spend cap: cut (D-020/ADR-006); public build is demo-only and makes no model calls; live mode is local-only and refuses to start without PROVIDER_CAP_CONFIRMED=1.' Add one sentence to the README or product note
- 2026-11-02T21:19:53Z orchestrator: Round 2 (backend): demo/public mode caps stored cases (DEMO_MAX_CASES, default 200, oldest demo-created cases pruned or 429) and runs in flight (DEMO_MAX_RUNS, default 4) -> plain-sentence 429; tests. Limiter cut recorded as SCOPE_CUTS row 24 by orchestrator. PROVIDER_CAP_CONFIRMED nit: accepted, documented.
- 2026-11-02T21:20:06Z backend: claimed
- 2026-11-02T21:24:43Z backend: Round 2: app/backend/limits.py (case_full, runs_busy; DEMO_MAX_CASES=200, DEMO_MAX_RUNS=4, public mode only = ZLAYT_MODE!=local; bad env value falls back to default). Hooks in api.py: make_case after purge_expired (429 busy, detail.reason demo_full), run_case after validation and before the case flips to running (429 busy, demo_busy; counts the app's runs dict, no leakable state). Refused-case behaviour: 409/413/400 still win over 429 for bad input. Soft bound under simultaneous creates (overshoot by a few). tests/unit/test_t183_limits.py 9 pass; from git archive of the commit tree: limits+hardening+api_routes+boundaries 86 pass. api.md updated. Unrelated: test_boundaries failure in the working tree comes from another worker's uncommitted why.py.
- 2026-11-02T21:24:43Z backend: moved in_progress -> in_review
- 2026-11-02T21:24:51Z orchestrator: review dispatched: security-reviewer

## Handoff
Changed: app/backend/limits.py plus 3 hook lines in api.py: public demo (ZLAYT_MODE!=local) caps stored cases (DEMO_MAX_CASES, 200) and runs in flight (DEMO_MAX_RUNS, 4) with a plain 429 busy (detail.reason demo_full / demo_busy); local unlimited; api.md updated. Verified: tests/unit/test_t183_limits.py (9 pass, both caps, 429 body has no trace/key/env name, local unlimited, slot frees when a run ends); git archive of commit 275e4ca: limits+hardening+api_routes+boundaries 86 pass. Left: cap is soft under simultaneous creates (overshoot by a few); oldest cases are not pruned, create is refused instead. Surprised: nothing; test_boundaries fails in the dirty tree only from another worker's why.py.

275e4ca feat(backend): public demo caps stored cases and runs in flight, plain 429 (T-183 r2)
ed0508e fix(qa): prompt-log redacts private-network details everywhere, README lists every edit with counts (T-187 r2)
33e88c6 tools: prompt-log export also redacts tailnet hostnames, 100.64/10 addresses and a work email; docstring lists every edit (T-187 privacy review)
59e33ca docs(submission): one-page product note, Part 2 process doc, validation-ladder SVG
f22f8fc tools: prompt-log export writes <redacted> (scanner-safe) and no stale 'capped' header (T-187)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:00.038Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md"
}
````

### User / tool · 2026-11-02T21:25:00.048Z

**tool result**
````
1	---
2	name: round2-review-workflow
3	description: Workflow gotchas for round-2 re-reviews (HEAD moves several times per review, pin with git archive, reviewer-write-guard makes the first Write final, board-guard flags > in strings, probes must restore patched socket/SDK functions)
4	metadata:
5	  type: feedback
6	---
7	
8	Round-2 re-reviews of a card: pin the commit you actually tested. Other agents commit to the same repo during a review. T-034 r2: b1803c0 -> 250e7b6. T-040 r2: 7a450a1 -> 5650eae -> 099732b -> 996f9b4 -> 037cc89. T-053 r2 (2026-11-02): 02f9939 -> dbb2c66 -> 20d866f -> 709397e -> f5444a8 -> e83eb54 -> d796383 -> d0c9cdb -> bee1844, six moves in about 25 minutes. Pin with `git archive <sha> | tar -x -C artifacts/review-evidence/<card>-r2/head_<sha>` and run pytest there with `-p no:cacheprovider`, so the venv is the project one (`/Users/arsis/zlayt-pm-project/.venv/bin/python`) and the copy is the only code on the path. Quote the pinned sha and `git rev-parse --short HEAD` in the same call. Before finishing, check `git diff --quiet <pinned> HEAD -- <gate files>`; if the gate files moved, say so in the review.
9	
10	The git archive pin has no `.git` and no `.venv`, so `git` and `tools/check_secrets.py` must run on the main repo, and the probes must `chdir` into the archive and put it at `sys.path[0]`. A commit can also fail to import on its own: 02f9939 imports `case_extras` before the module exists (added in dbb2c66). Check collection errors before reading any count.
11	
12	The reviewer-write-guard makes the first Write to `reviews/<card>-<persona>.md` final: a later Edit to fix a count or a label is denied ("reviews are append-only; write a new file"). Proofread the JSON and every number before the first Write. Confirm numbers with a query or a grep first; I had to leave one wrong count in T-053 r2 for this reason.
13	
14	The live server on :7860 can predate HEAD. Probes against it are not evidence for HEAD. Other agents also kill listeners between calls, so start probe servers with `subprocess.Popen` inside one Python run and stop them in a `finally`. Check `lsof -iTCP:<port> -sTCP:LISTEN` first, and do not use `timeout` (not installed on macOS). Use `lsof -ti tcp:<port> | xargs kill` for manual cleanup. One Bash call was killed with exit 144 mid-probe; rerun it rather than reading partial output.
15	
16	The git-guard PreToolUse hook rejects `$(...)` in an echo or similar command position. The board-guard hook reads `>` inside quoted strings as a redirect; `curl -w "... -> %{http_code}"` was blocked. Keep arrows and `>` out of shell strings and put probes in files under artifacts/review-evidence/ (Write tool, then `.venv/bin/python -I <file>`).
17	
18	Probe gotchas (T-053 r2): (1) do not re-capture a module attribute after patching it, because the module-level `_orig = socket.create_connection` ran after the patch and captured the stub, so every local HTTP call was blocked; capture originals once, before any patch. (2) Patching `subprocess.run` globally breaks the probe's own subprocess calls; save and restore it in a `try/finally`. (3) A UDP `connect()` to 192.0.2.1 picks the outbound interface address without sending a packet, which gives a LAN address for a non-loopback check.
19	
20	T-055/T-058 (2026-11-01, HEAD moved d796383 -> 08764e7 within an hour): `git archive HEAD` lacks the untracked LLM fixtures the sample case needs, so pinned tests fail unless `tests/fixtures` is copied from the working tree (record that in the review). git-guard blocks `rm` with a variable path ("unresolved expansion"); use literal paths. `timeout` is not installed on macOS. `which gitleaks` returns rc=1 (not installed). pip-audit can be installed into a scratchpad venv (`python3 -m venv <scratch>/pa && <scratch>/pa/bin/pip install pip-audit`) and run with `--no-deps --disable-pip` on a fully pinned requirements file, without touching `.venv`.
21	
22	T-053 r3 (2026-11-01): HEAD was 08764e7 at the first check, 8ec0b25 at the pin, 38421cc at write time (docs and memory only; gate files unchanged). Pin the commit you test, then re-check drift at write time. Brief says `python3 -m pytest`, but system python3 has no pytest: use `.venv/bin/python -m pytest -p no:cacheprovider`, and do not pipe pytest into tail when you need the exit code (the pipe hides it). After the first Write, a self-found error (I cited api.py:103 for live_enabled, which is at :113) was fixed by appending a correction after the JSON block, not by Edit, because reviews are append-only. Proofread line refs with grep before the first Write, not after.
23	
24	Persona scope: if a brief asks security-reviewer to write a record under another persona's name, do not write it. Report the facts and say that persona needs its own run.
25	
26	**Why:** T-034 r2 (first `$()` echo blocked, HEAD changed between pytest and grep). T-040 r2 (four HEAD moves, a live server that predated HEAD, a dirty tree producing a flaky result). T-053 r2 (six HEAD moves, an append-only review file with one wrong count, and a probe bug that made every local request look blocked).
27	**How to apply:** at the start of each round-2 review, record the HEAD sha and the server start time, pin an archive, probe through a file, and proofread the review before the first Write.
28	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:02.989Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git archive 275e4ca | (mkdir -p artifacts/review-evidence/T-183-r2/head && tar -x -C artifacts/review-evidence/T-183-r2/head) && ls artifacts/review-evidence/T-183-r2/head && cat artifacts/review-evidence/T-183-r2/head/app/backend/limits.py && git show 275e4ca --stat | tail -8; ls artifacts/review-evidence/T-183/"
}
````

### User / tool · 2026-11-02T21:25:04.415Z

**tool result**
````
275e4ca
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
app
artifacts
board
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
run.sh
spec
submission
tests
tools
"""T-183 r2: resource bounds for the public demo build (security review: any client could fill the disk and burn CPU; no money is at stake because the
public build makes no model call). Two caps, public mode only (ZLAYT_MODE != local); local/dev stays unlimited:
  DEMO_MAX_CASES  stored cases, default 200  -> POST /api/cases and the PDF upload answer 429 `busy` when the table is full (expired cases are purged first)
  DEMO_MAX_RUNS   runs in flight, default 4  -> POST /api/cases/{token}/run answers 429 `busy`
Pure functions that return a plain sentence (or None); the route turns it into the standard error body. No stack text, no key, no count of other users' data.
The case cap is a soft bound: simultaneous creates can overshoot it by a few, never grow it without limit."""
import os

DEFAULT_MAX_CASES = 200
DEFAULT_MAX_RUNS = 4
FULL_MESSAGE = "This demo is full right now. Try again later."
BUSY_MESSAGE = "This demo is busy right now. Try again in a minute."


def _limit(name: str, default: int) -> int:
    try:
        n = int(os.environ.get(name, "").strip() or default)
    except ValueError:
        return default
    return n if n >= 1 else default           # a zero, negative or unreadable value falls back to the default (a typo must not switch the demo off or lock it shut)


def max_cases() -> int:
    return _limit("DEMO_MAX_CASES", DEFAULT_MAX_CASES)


def max_runs() -> int:
    return _limit("DEMO_MAX_RUNS", DEFAULT_MAX_RUNS)


def case_full(conn, local: bool):
    """The 429 sentence when the public demo already stores the maximum number of cases, else None. Call after expired cases are purged."""
    if local:
        return None
    return FULL_MESSAGE if conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0] >= max_cases() else None


def runs_busy(in_flight: int, local: bool):
    """The 429 sentence when the public demo already has the maximum number of runs in flight, else None."""
    if local:
        return None
    return BUSY_MESSAGE if in_flight >= max_runs() else None
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/api.py             |   5 ++
 app/backend/limits.py          |  42 +++++++++++
 memory/contracts/api.md        |   2 +-
 tests/unit/test_t183_limits.py | 161 +++++++++++++++++++++++++++++++++++++++++
 4 files changed, 209 insertions(+), 1 deletion(-)
__pycache__
head
probe1.full.out
probe1.out
probe1.py
probe2.out
probe2.py
probe3.py
t183_0xnsewsl
t183_8zhyizhh
t183_k3lt11wy
t183_qnjqar2h
t183_rvmtp_d7
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:05.957Z

**tool call — Bash**
````
{
 "command": "git show 275e4ca -- app/backend/api.py; cat artifacts/review-evidence/T-183/probe2.py; grep -n \"ZLAYT_MODE\\|def is_local\\|local\" app/backend/api.py | head -30"
}
````

### User / tool · 2026-11-02T21:25:06.113Z

**tool result**
````
commit 275e4caf0c3977b66b562297dd6a706902c8811c
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 15:24:33 2026 -0600

    feat(backend): public demo caps stored cases and runs in flight, plain 429 (T-183 r2)
    
    DEMO_MAX_CASES (200) and DEMO_MAX_RUNS (4), public mode only; local/dev unlimited. app/backend/limits.py, two hooks in api.py, tests, api.md.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index 41830af..077ccd8 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -21,6 +21,7 @@ from starlette.exceptions import HTTPException as StarletteHTTPException
 
 from starlette.concurrency import run_in_threadpool
 
+from app.backend import limits
 from app.backend import case_extras, case_list, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
 from app.db import db as DB
 
@@ -353,6 +354,8 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         try:
             now = time.time()
             DB.purge_expired(c, now)
+            if (full := limits.case_full(c, local_mode())):          # T-183 r2: public demo stores at most DEMO_MAX_CASES
+                raise ApiError(429, "busy", full, {"reason": "demo_full"})
             cid = DB.create_case(c, text, now=now, name=name or None,
                                  source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                  **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
@@ -444,6 +447,8 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
             if decided and b.get("confirm_rerun") is not True:
                 raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
+            if (busy := limits.runs_busy(len(runs), local_mode())):  # T-183 r2: public demo runs at most DEMO_MAX_RUNS at once
+                raise ApiError(429, "busy", busy, {"reason": "demo_busy"})
             now = time.time()
             store.run_started(token)
             DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
"""T-183 probe 2: CSP header, export 422 body, live-start refusal without provider cap, flood of sample creates and runs in demo mode (resource use)."""
import json, os, subprocess, sys, time, tempfile, threading, urllib.request, urllib.error
sys.path.insert(0, "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183")
import probe1 as P

# C: live without PROVIDER_CAP_CONFIRMED must refuse to start; the sentinel must not be echoed
env = {"PATH": os.environ["PATH"], "HOME": os.environ["HOME"], "DATA_DIR": f"{P.SCR}/dataC", "PORT": "17863", "HOST": "127.0.0.1",
       "LLM_BACKEND": "anthropic-api", "ENABLE_LIVE": "1", "ANTHROPIC_API_KEY": P.SENT, "PYTHONPATH": P.ARCH}
r = subprocess.run([P.PY, "-m", "app.main"], cwd=P.ARCH, env=env, capture_output=True, text=True, timeout=60)
print("C rc", r.returncode, "last stderr line:", (r.stderr.strip().splitlines() or [""])[-1][:200], "| sentinel in output:", P.SENT in r.stdout + r.stderr, "| sk-ant in output:", "sk-ant" in r.stdout + r.stderr)

p, base = P.serve(17864, {})
try:
    s, h, b = P.req(base, "GET", "/api/health"); print("headers:", {k: v[:110] for k, v in h.items() if k.lower() in ("content-security-policy", "x-content-type-options", "referrer-policy", "cache-control", "server")})
    s, h, b = P.req(base, "GET", "/"); print("index headers csp:", h.get("content-security-policy", h.get("Content-Security-Policy"))[:80])
    s, h, b = P.req(base, "POST", "/api/cases", body={"sample": True}); tok = json.loads(b)["token"]
    s, h, b = P.req(base, "GET", f"/api/cases/{tok}/export"); print("export before run:", s, b[:200])
    s, h, b = P.req(base, "POST", f"/api/cases/{tok}/items/zzz/review", body={"action": "accept"}); print("review unknown item:", s, b[:200])
    # flood: 300 creates, then 100 concurrent runs
    t0 = time.time(); toks = []
    for i in range(300):
        s, h, b = P.req(base, "POST", "/api/cases", body={"sample": True}); assert s == 201, (s, b[:100]); toks.append(json.loads(b)["token"])
    print("300 creates all 201 in %.1fs (no limiter)" % (time.time() - t0))
    t0 = time.time(); codes = []
    def go(t):
        s, h, b = P.req(base, "POST", f"/api/cases/{t}/run", body={}); codes.append(s)
    th = [threading.Thread(target=go, args=(t,)) for t in toks[:150]]
    [x.start() for x in th]; [x.join() for x in th]
    from collections import Counter
    print("150 concurrent runs:", Counter(codes), "%.1fs" % (time.time() - t0))
    t0 = time.time(); s, h, b = P.req(base, "GET", "/api/health"); print("health during runs: %d in %.2fs" % (s, time.time() - t0))
    for _ in range(240):
        sts = Counter(json.loads(P.req(base, "GET", f"/api/cases/{t}/status")[2])["status"] for t in toks[:150:15])
        if set(sts) <= {"ready", "failed"}: break
        time.sleep(1)
    print("sampled run status:", dict(sts))
    db = f"{P.SCR}/data17864/zlayt.sqlite"
    print("db bytes after 301 cases + 150 runs:", os.path.getsize(db))
    ps = subprocess.run(["ps", "-o", "rss=,nlwp=", "-p", str(p.pid)], capture_output=True, text=True).stdout.strip()
    print("server rss KB:", ps)
finally:
    p.terminate(); p.wait(timeout=10)
83:def local_mode() -> bool:
84:    return os.environ.get("ZLAYT_MODE") == "local"
105:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
115:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
116:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
221:            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
272:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
282:        if not local_mode():
292:            if not local_mode():
307:        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
358:            if (full := limits.case_full(c, local_mode())):          # T-183 r2: public demo stores at most DEMO_MAX_CASES
451:            if (busy := limits.runs_busy(len(runs), local_mode())):  # T-183 r2: public demo runs at most DEMO_MAX_RUNS at once
604:    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
640:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
645:                return trace.item_trace(c, token, item_id, full=local_mode())
656:            return trace.case_trace(c, token, full=local_mode())
665:            return trace.judge_report(c, token, full=local_mode())
674:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
700:                """T-177 r3 / D-068: /classic is a developer screen. It answers in local mode (ZLAYT_MODE=local) or with ZLAYT_CLASSIC=1; in demo or public mode it sends the visitor to the guided UI at /."""
701:                return local_mode() or os.environ.get("ZLAYT_CLASSIC") == "1"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:08.279Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2/head && sed -n 330,385p app/backend/api.py; sed -n 425,490p app/backend/api.py; grep -n \"runs\\b\\|runs\\[\" app/backend/api.py | head -30; grep -n \"def run_started\" -A12 app/backend/store.py"
}
````

### User / tool · 2026-11-02T21:25:08.419Z

**tool result**
````
            raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
                           (e.detail.get("message") if e.code == "ocr_unavailable" else None) or _PDF_MESSAGES[e.code], {"reason": e.code, **e.detail}) from None
        out = make_case(got["text"], title if title is not None else name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None},
                        strict_name=title is not None)
        out["pdf_checks"] = got.get("pdf_checks")
        return out

    def valid_name(value, strict=True):
        """T-157 r2: a typed title (or legacy `name`) -> the text to store; markup or an over-long typed title is 422 invalid_title with a plain message."""
        try:
            return case_list.validate_title(value) if strict else case_list.clean_title(value)
        except case_list.TitleError as e:
            raise ApiError(422, "invalid_title", str(e)) from None

    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None, strict_name=True):
        name = name if isinstance(name, str) else ("Sample case" if sample else None)
        name = valid_name(name, strict_name)          # before anything is stored: a refused title leaves no case behind
        try:
            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
        except ingest.IngestError as e:
            raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
        if demo_mode() and digest(text) not in allowed_hashes():
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        c = conn()
        try:
            now = time.time()
            DB.purge_expired(c, now)
            if (full := limits.case_full(c, local_mode())):          # T-183 r2: public demo stores at most DEMO_MAX_CASES
                raise ApiError(429, "busy", full, {"reason": "demo_full"})
            cid = DB.create_case(c, text, now=now, name=name or None,
                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
            try:
                ing = pipeline_mod().ingest_case(c, cid, text, now)
                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
                flags = DB.list_items(c, cid, "flag")
            except Exception as e:                       # nothing of a failed create stays stored (ADR-006): drop the case row and its parts
                DB.delete_case(c, cid)
                if isinstance(e, (ingest.IngestError, language.UnsupportedLanguage)):
                    msg, detail = language.api_fields(e)
                    if not msg:             # T-183: a limit hit during splitting (too many records) said "input too large" (the bare code); say it as a sentence
                        msg = "Input is too large." if e.code == "input_too_large" else "Input is empty." if e.code == "bad_request" else "The input could not be read."
                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, msg, detail) from None
                log.error("create failed %s", type(e).__name__)
                raise ApiError(500, "internal", "Something went wrong.") from None
            return {"token": cid, "name": DB.get_case(c, cid)["name"], "title": case_list.case_title(c, DB.get_case(c, cid)), "status": "ingested", "source": "sample" if sample else "paste",
                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
                    "dates_to_confirm": present.dates_to_confirm(c, cid),
                    "gap_flags": [f["id"] for f in flags if f["type"] == "gap"],
                    "record_warning_flags": [f["id"] for f in flags if f["type"] == "record_warning"],
                    "warnings": ing["warnings"]}
        finally:
            c.close()

    @app.get("/api/cases/{token}")
    def get_case_view(token: str):
            if DB.get_case(c, token)["status"] == "running":
                DB.update_case(c, token, status="ready", stage="finalize", run_finished_at=time.time())
        except Exception as e:                                   # code only: no message text from the pipeline
            DB.update_case(c, token, status="failed", run_finished_at=time.time(),
                           error=json.dumps({"code": getattr(e, "code", "run_failed"), "message": "The run stopped; finished items are kept."}))
        finally:
            c.close()
            runs.pop(token, None)
            store.run_ended(token)

    @app.post("/api/cases/{token}/run", status_code=202)
    async def run_case(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            case = get_case(c, token)
            if case["status"] == "running" or token in runs:
                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
            if decided and b.get("confirm_rerun") is not True:
                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
            if (busy := limits.runs_busy(len(runs), local_mode())):  # T-183 r2: public demo runs at most DEMO_MAX_RUNS at once
                raise ApiError(429, "busy", busy, {"reason": "demo_busy"})
            now = time.time()
            store.run_started(token)
            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
            runs[token].start()
            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
        finally:
            c.close()

    @app.post("/api/cases/{token}/rejudge")
    async def rejudge_case(token: str):
        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
        from app.backend import rejudge as RJ
        c = conn()
        try:
            case = get_case(c, token)
            if case["status"] == "running" or token in runs or token in rejudging:
                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
            rejudging.add(token)
            try:
                return await run_in_threadpool(lambda: RJ.rejudge(c, token, make_call(c, token), now=time.time()))
            finally:
                rejudging.discard(token)
        finally:
            c.close()

    @app.get("/api/cases/{token}/status")
    def status(token: str):
        c = conn()
        try:
            case = get_case(c, token)
            stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
            stages = list(stages) if not callable(stages) else STAGES
            stage, done = case_list.run_progress(case, stages)
105:    runs = {}
109:        store.interrupt_orphaned_runs(_boot)        # T-178: a run a stopped process left "running" becomes failed (run again allowed); its accepted items are untouched
307:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
308:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
323:        try:       # parsing runs off the event loop (so /api/health stays responsive) under a time cap
352:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
432:            runs.pop(token, None)
441:            if case["status"] == "running" or token in runs:
444:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
450:            if (busy := limits.runs_busy(len(runs), local_mode())):  # T-183 r2: public demo runs at most DEMO_MAX_RUNS at once
455:            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
456:            runs[token].start()
469:            if case["status"] == "running" or token in runs or token in rejudging:
472:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
21:def run_started(token: str) -> None:
22-    with _LIVE_LOCK:
23-        LIVE_RUNS.add(token)
24-
25-
26-def run_ended(token: str) -> None:
27-    with _LIVE_LOCK:
28-        LIVE_RUNS.discard(token)
29-
30-
31-def is_live_run(token: str) -> bool:
32-    with _LIVE_LOCK:
33-        return token in LIVE_RUNS
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:14.275Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2/head && grep -n \"make_case(\" app/backend/api.py; sed -n 296,322p app/backend/api.py; grep -n \"@app.post(\\\"/api/cases\\\"\" -A14 app/backend/api.py | head -30; cat tests/unit/test_t183_limits.py | head -60"
}
````

### User / tool · 2026-11-02T21:25:14.376Z

**tool result**
````
301:        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample, strict_name=typed)
332:        out = make_case(got["text"], title if title is not None else name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None},
344:    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None, strict_name=True):
        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
        if not isinstance(text, str):
            raise ApiError(400, "bad_request", "Provide text or sample: true.")
        typed = isinstance(b.get("title"), str)
        given = b.get("title") if typed else b.get("name")          # T-157: `title` is the name a paralegal types (refused when over 120 characters); `name` stays accepted (a long file name is cut)
        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample, strict_name=typed)

    @app.post("/api/cases/pdf", status_code=201)
    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer minus hidden text (T-087, `include_hidden`); a scanned PDF is
        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        valid_name(title if title is not None else name, title is not None)          # T-157 r2: a markup title is refused before a byte is read
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
            raise ApiError(413, "input_too_large", "The PDF is too large.")
        data = b""
        async for chunk in request.stream():
            data += chunk
            if len(data) > pdf_text.MAX_PDF_BYTES:
                raise ApiError(413, "input_too_large", "The PDF is too large.")
        opts = {}
        if (ocr or "").lower() in ("1", "true", "yes"):
            opts["ocr"] = True
        if include_hidden:
            opts["include_hidden"] = include_hidden
285:    @app.post("/api/cases", status_code=201)
286-    async def create_case(request: Request):
287-        b = await body_of(request)
288-        sample = b.get("sample") is True
289-        lib = None
290-        if isinstance(b.get("library"), str):
291-            if not local_mode():
292-                raise ApiError(404, "not_found", "Not found.")
293-            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
294-            if lib is None:
295-                raise ApiError(404, "not_found", "No such library case.")
296-        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
297-        if not isinstance(text, str):
298-            raise ApiError(400, "bad_request", "Provide text or sample: true.")
299-        typed = isinstance(b.get("title"), str)
"""T-183 round 2: the public demo bounds stored cases (DEMO_MAX_CASES, default 200) and runs in flight (DEMO_MAX_RUNS, default 4); both answer a plain
429 `busy`; local/dev mode is unlimited. Fixture backend, no network, no key."""
import json
import re
import threading

import pytest
from fastapi.testclient import TestClient

from app.backend import limits
from app.backend.api import create_app

KEY = "sk-" + "ant-SENTINEL-" + "key-0123456789abcdef"


class Hold:
    """A pipeline stand-in whose runs stay in flight until released."""
    def __init__(self):
        self.gate = threading.Event()
        self.started = threading.Semaphore(0)

    def ingest_case(self, c, cid, text, now):
        from app.backend import pipeline as PL
        return PL.ingest_case(c, cid, text, now)

    def run_pipeline(self, c, token, raw, **k):
        self.started.release()
        self.gate.wait(20)


def _app(tmp_path, monkeypatch, *, local=False, pipeline=None, **env):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    for k in ("ENABLE_LIVE", "DEMO_MAX_CASES", "DEMO_MAX_RUNS", "ZLAYT_MODE"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", KEY)           # present, to prove no 429 body can carry it
    if local:
        monkeypatch.setenv("ZLAYT_MODE", "local")
    for k, v in env.items():
        monkeypatch.setenv(k, str(v))
    (tmp_path / "index.html").write_text("<p>hi</p>")
    return TestClient(create_app(str(tmp_path / "l.sqlite"), static_dir=str(tmp_path), pipeline=pipeline), client=("127.0.0.1", 50000), raise_server_exceptions=False)


def _plain_429(r):
    assert r.status_code == 429
    e = r.json()["error"]
    text = r.text
    assert e["code"] == "busy" and e["message"].endswith(".") and not re.fullmatch(r"[a-z_]+", e["message"])
    for bad in ("Traceback", "File \"", "/Users", "sk-ant", KEY, "sqlite", "Exception", "limits.py", "200", "DEMO_MAX"):
        assert bad not in text, bad
    assert set(r.json()) == {"error"} and set(e) <= {"code", "message", "detail"}
    return e


def _count(c):
    import sqlite3
    return sqlite3.connect(c.app.state.db_path).execute("SELECT COUNT(*) FROM cases").fetchone()[0]


def test_defaults_are_200_cases_and_4_runs_and_a_bad_value_falls_back(monkeypatch):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:22.220Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2/head && grep -n \"def purge_expired\" -B3 -A12 app/db/db.py; grep -n \"TTL\\|RETENTION\\|24\" app/db/db.py | head; grep -n \"workers\\|CMD\\|uvicorn\" Dockerfile app/main.py deploy/* 2>/dev/null | head; grep -n \"delete\" app/backend/api.py | head; cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183/probe1.py | sed -n 1,60p"
}
````

### User / tool · 2026-11-02T21:25:22.348Z

**tool result**
````
294-        raise
295-
296-
297:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
298-    ids = [r["id"] for r in conn.execute("SELECT id FROM cases WHERE created_at < ?", (now - retention_seconds,))]
299-    for cid in ids:
300-        delete_case(conn, cid)
301-    return len(ids)
302-
303-
304-def table_counts(conn, case_id: str) -> dict:
305-    return {t: conn.execute(f"SELECT COUNT(*) FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,)).fetchone()[0]
306-            for t in _CASE_TABLES}
17:RETENTION_SECONDS = 24 * 3600
41:    pasted text past the 24 h purge (T-040 security r2)."""
50:            for ext in ("", "-wal", "-shm", "-journal"):          # deleted, not kept: an old file would hold pasted text past the 24 h purge
297:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
Dockerfile:26:  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:7860/api/health', timeout=4).status == 200 else 1)"
Dockerfile:28:CMD ["python", "-m", "app.main"]
app/main.py:4:import uvicorn
app/main.py:9:    """uvicorn app.main:create --factory"""
app/main.py:14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
182:        A route that reads a case after its existence check fails with a TypeError/AttributeError when the case is deleted in that gap (DELETE, the purge): when the case in the
192:                    log.warning("case deleted while a request read it (%s at %s); answered 404", type(e).__name__, where)
367:                DB.delete_case(c, cid)
410:    @app.delete("/api/cases/{token}", status_code=204)
411:    def delete_case(token: str):
415:            DB.delete_case(c, token)
"""T-183 security probe on the git-archive copy. Starts the server as a subprocess (demo build env), exercises routes, scans all output for a sentinel key."""
import json, os, re, subprocess, sys, time, urllib.request, urllib.error, tempfile, socket

ARCH = "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183/head"
PY = "/Users/arsis/zlayt-pm-project/.venv/bin/python"
SENT = "sk-ant-" + "api03-" + "PROBESENTINEL" + "0123456789abcdef"   # built in parts: never a literal key
SCR = tempfile.mkdtemp(prefix="t183_", dir="/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183")


def req(base, method, path, body=None, headers=None, raw=None):
    h = dict(headers or {})
    data = raw
    if body is not None:
        data = json.dumps(body).encode(); h.setdefault("Content-Type", "application/json")
    r = urllib.request.Request(base + path, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def serve(port, env_extra):
    env = {"PATH": os.environ["PATH"], "HOME": os.environ["HOME"], "DATA_DIR": f"{SCR}/data{port}", "PORT": str(port), "HOST": "127.0.0.1",
           "LLM_BACKEND": "fixture", "FIXTURE_SET": "curated", "PYTHONPATH": ARCH}
    env.update(env_extra)
    p = subprocess.Popen([PY, "-m", "app.main"], cwd=ARCH, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"
    for _ in range(60):
        try:
            urllib.request.urlopen(base + "/api/health", timeout=1); break
        except Exception:
            if p.poll() is not None: break
            time.sleep(0.5)
    return p, base


def scenario(label, port, env_extra, key_in_env):
    out = {"label": label}
    p, base = serve(port, env_extra)
    seen = []   # (what, bytes)
    try:
        def R(m, path, **kw):
            s, h, b = req(base, m, path, **kw); seen.append((f"{m} {path}", json.dumps(h).encode() + b)); return s, h, b
        s, h, b = R("GET", "/api/health"); out["health"] = (s, json.loads(b))
        out["csp"] = h.get("Content-Security-Policy", "")[:60]
        # static
        s, h, b = R("GET", "/"); out["index"] = s
        refs = set(re.findall(r'(?:src|href)="(/?[^"#]+\.(?:js|css))"', b.decode()))
        out["static_refs"] = sorted(refs)
        for r in refs:
            R("GET", r if r.startswith("/") else "/" + r)
        # sample -> run -> ready
        s, h, b = R("POST", "/api/cases", body={"sample": True}); tok = json.loads(b).get("token"); out["create_sample"] = s
        s, h, b = R("POST", f"/api/cases/{tok}/run", body={}); out["run"] = s
        for _ in range(120):
            s, h, b = R("GET", f"/api/cases/{tok}/status"); st = json.loads(b)
            if st["status"] in ("ready", "failed"): break
            time.sleep(0.5)
        out["status"] = {k: st[k] for k in ("status", "counts", "error")}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:52.710Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2/probe_r2.py",
 "content": "\"\"\"T-183 r2 probe on git archive of 275e4ca. Public demo build (ZLAYT_MODE unset) vs local (ZLAYT_MODE=local). Own ports, own PIDs, stopped in finally.\"\"\"\nimport json, os, re, socket, sqlite3, subprocess, sys, tempfile, threading, time, urllib.request, urllib.error\nfrom collections import Counter\n\nROOT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2\"\nARCH = ROOT + \"/head\"\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nSENT = \"sk-ant-\" + \"api03-\" + \"R2SENTINEL\" + \"0123456789abcdef\"\nSCR = tempfile.mkdtemp(prefix=\"r2_\", dir=ROOT)\nBAD = (\"Traceback\", 'File \"', \"/Users\", \"sk-ant\", \"sqlite\", \"DEMO_MAX\", \"limits.py\", SENT)\n\n\ndef free_port():\n    s = socket.socket(); s.bind((\"127.0.0.1\", 0)); p = s.getsockname()[1]; s.close(); return p\n\n\ndef req(base, method, path, body=None):\n    h = {}; data = None\n    if body is not None:\n        data = json.dumps(body).encode(); h[\"Content-Type\"] = \"application/json\"\n    r = urllib.request.Request(base + path, data=data, method=method, headers=h)\n    try:\n        with urllib.request.urlopen(r, timeout=60) as resp:\n            return resp.status, dict(resp.headers), resp.read()\n    except urllib.error.HTTPError as e:\n        return e.code, dict(e.headers), e.read()\n\n\ndef serve(env_extra):\n    port = free_port()\n    d = tempfile.mkdtemp(prefix=\"d_\", dir=SCR)\n    env = {\"PATH\": os.environ[\"PATH\"], \"HOME\": os.environ[\"HOME\"], \"DATA_DIR\": d, \"PORT\": str(port), \"HOST\": \"127.0.0.1\",\n           \"LLM_BACKEND\": \"fixture\", \"FIXTURE_SET\": \"curated\", \"PYTHONPATH\": ARCH}\n    env.update(env_extra)\n    log = open(d + \"/server.log\", \"wb\")\n    p = subprocess.Popen([PY, \"-I\", \"-m\", \"app.main\"], cwd=ARCH, env=env, stdout=log, stderr=subprocess.STDOUT)\n    base = f\"http://127.0.0.1:{port}\"\n    for _ in range(80):\n        try:\n            urllib.request.urlopen(base + \"/api/health\", timeout=1); break\n        except Exception:\n            if p.poll() is not None: break\n            time.sleep(0.5)\n    return p, base, d\n\n\ndef dbcount(d, table=\"cases\"):\n    import glob\n    f = glob.glob(d + \"/*.sqlite\")[0]\n    return sqlite3.connect(f).execute(f\"SELECT COUNT(*) FROM {table}\").fetchone()[0]\n\n\ndef creates(base, n, workers=1):\n    codes = []; bodies = []\n    def one():\n        s, h, b = req(base, \"POST\", \"/api/cases\", body={\"sample\": True}); codes.append(s); bodies.append((s, h, b))\n    if workers == 1:\n        for _ in range(n): one()\n    else:\n        ts = [threading.Thread(target=one) for _ in range(n)]\n        [t.start() for t in ts]; [t.join() for t in ts]\n    return codes, bodies\n\n\ndef tokens_from(bodies):\n    return [json.loads(b)[\"token\"] for s, h, b in bodies if s == 201]\n\n\ndef scan(label, items):\n    hits = [(k, w) for k, v in items for w in BAD if (w.encode() in v)]\n    print(f\"  scan {label}: {len(items)} blobs, bad strings found: {hits[:5]}\")\n\n\ndef concurrent_runs(base, toks, n):\n    codes = []; bodies = []\n    def go(t):\n        s, h, b = req(base, \"POST\", f\"/api/cases/{t}/run\", body={}); codes.append(s); bodies.append((s, h, b))\n    ts = [threading.Thread(target=go, args=(t,)) for t in toks[:n]]\n    peak = [0]; stop = [False]\n    def poll():\n        # peak concurrently running cases, sampled from status of the first n tokens\n        while not stop[0]:\n            c = 0\n            for t in toks[:n:5]:\n                try: c += json.loads(req(base, \"GET\", f\"/api/cases/{t}/status\")[2]).get(\"status\") == \"running\"\n                except Exception: pass\n            peak[0] = max(peak[0], c); time.sleep(0.05)\n    pl = threading.Thread(target=poll); pl.start()\n    t0 = time.time(); [t.start() for t in ts]; [t.join() for t in ts]\n    return codes, bodies, time.time() - t0, peak, stop, pl\n\n\ndef main():\n    procs = []\n    try:\n        # ---- 1. DEMO build, sentinel key present, 300 creates then 150 concurrent runs\n        p, base, d = serve({\"ANTHROPIC_API_KEY\": SENT, \"LLM_BACKEND\": \"anthropic-api\"}); procs.append(p)\n        print(\"A demo build\", base, \"health:\", req(base, \"GET\", \"/api/health\")[2][:160])\n        seen = []\n        t0 = time.time(); codes, bodies = creates(base, 300)\n        print(\"A 300 sequential creates:\", Counter(codes), \"%.1fs\" % (time.time() - t0), \"| stored cases:\", dbcount(d))\n        seen += [(f\"create {s}\", json.dumps(h).encode() + b) for s, h, b in bodies]\n        r429 = [b for s, h, b in bodies if s == 429]\n        print(\"  sample 429 body:\", r429[0].decode() if r429 else None)\n        toks = tokens_from(bodies)\n        print(\"  tokens:\", len(toks))\n        codes2, bodies2, dt, peak, stop, pl = concurrent_runs(base, toks, 150)\n        print(\"A 150 concurrent runs:\", Counter(codes2), \"%.1fs\" % dt)\n        r429 = [b for s, h, b in bodies2 if s == 429]\n        print(\"  sample run 429 body:\", r429[0].decode() if r429 else None)\n        seen += [(f\"run {s}\", json.dumps(h).encode() + b) for s, h, b in bodies2]\n        # wait for completion\n        for _ in range(120):\n            sts = Counter(json.loads(req(base, \"GET\", f\"/api/cases/{t}/status\")[2])[\"status\"] for t in toks[:150:10])\n            if \"running\" not in sts: break\n            time.sleep(0.5)\n        stop[0] = True; pl.join()\n        print(\"  peak running seen by sampler (every 5th token, so lower bound):\", peak[0], \"| statuses after:\", dict(sts))\n        # after runs finish, can another run start (slot freed)?\n        started = [t for t, c in zip(toks[:150], [None]*150)]\n        s, h, b = req(base, \"POST\", f\"/api/cases/{toks[-1]}/run\", body={}); print(\"  run after drain on an unused case:\", s)\n        # lockout: a legitimate create now\n        s, h, b = req(base, \"POST\", \"/api/cases\", body={\"sample\": True}); print(\"  legit create while full:\", s, b.decode()[:120])\n        # delete one own case frees a slot?\n        s, h, b = req(base, \"DELETE\", f\"/api/cases/{toks[0]}\"); print(\"  DELETE own case:\", s)\n        s, h, b = req(base, \"POST\", \"/api/cases\", body={\"sample\": True}); print(\"  create after one delete:\", s)\n        s, h, b = req(base, \"GET\", \"/api/health\"); print(\"  health:\", s)\n        # other creation paths while full\n        s, h, b = req(base, \"POST\", \"/api/cases\", body={\"text\": \"x\" * 10}); print(\"  non-sample paste while full:\", s, b.decode()[:120])\n        seen += [(\"last\", b)]\n        scan(\"demo flood A\", seen)\n        log = open(d + \"/server.log\", \"rb\").read(); print(\"  server log bytes:\", len(log), \"| sentinel in log:\", SENT.encode() in log)\n        p.terminate(); p.wait(timeout=10)\n\n        # ---- 2. race test: cap 20, 100 concurrent creates -> stored count\n        p, base, d = serve({\"DEMO_MAX_CASES\": \"20\"}); procs.append(p)\n        codes, bodies = creates(base, 100, workers=100)\n        print(\"B cap=20, 100 simultaneous creates:\", Counter(codes), \"| stored:\", dbcount(d))\n        p.terminate(); p.wait(timeout=10)\n\n        # ---- 3. run cap exact under simultaneous runs: cap=4 default; 60 simultaneous runs on fresh cases\n        p, base, d = serve({}); procs.append(p)\n        codes, bodies = creates(base, 60)\n        toks = tokens_from(bodies)\n        codes2, bodies2, dt, peak, stop, pl = concurrent_runs(base, toks, 60)\n        stop[0] = True; pl.join()\n        print(\"C 60 simultaneous runs, default cap 4:\", Counter(codes2), \"%.1fs\" % dt, \"| peak sampled:\", peak[0])\n        # how long does a sample run take (slot hold time)?\n        for _ in range(200):\n            sts = Counter(json.loads(req(base, \"GET\", f\"/api/cases/{t}/status\")[2])[\"status\"] for t in toks[:60])\n            if \"running\" not in sts: break\n            time.sleep(0.25)\n        print(\"  statuses after:\", dict(sts))\n        t0 = time.time(); s, h, b = req(base, \"POST\", f\"/api/cases/{toks[59]}/run\", body={}); print(\"  fresh run:\", s)\n        while json.loads(req(base, \"GET\", f\"/api/cases/{toks[59]}/status\")[2])[\"status\"] == \"running\": time.sleep(0.1)\n        print(\"  one sample run holds a slot for %.1fs\" % (time.time() - t0))\n        p.terminate(); p.wait(timeout=10)\n\n        # ---- 4. bad env values fall back\n        for v in (\"0\", \"-5\", \"abc\", \"\"):\n            p, base, d = serve({\"DEMO_MAX_CASES\": v, \"DEMO_MAX_RUNS\": v}); procs.append(p)\n            codes, _ = creates(base, 3)\n            print(\"D env=%r: 3 creates ->\" % v, codes, \"(default 200 applies)\")\n            p.terminate(); p.wait(timeout=10)\n\n        # ---- 5. dev mode unlimited\n        p, base, d = serve({\"ZLAYT_MODE\": \"local\", \"DEMO_MAX_CASES\": \"5\", \"DEMO_MAX_RUNS\": \"1\"}); procs.append(p)\n        codes, bodies = creates(base, 300)\n        print(\"E local, caps set to 5/1, 300 creates:\", Counter(codes), \"| stored:\", dbcount(d))\n        toks = tokens_from(bodies)\n        codes2, bodies2, dt, peak, stop, pl = concurrent_runs(base, toks, 150)\n        stop[0] = True; pl.join()\n        print(\"E local 150 concurrent runs:\", Counter(codes2), \"%.1fs\" % dt)\n        p.terminate(); p.wait(timeout=10)\n    finally:\n        for p in procs:\n            if p.poll() is None:\n                p.terminate()\n                try: p.wait(timeout=10)\n                except Exception: p.kill()\n\n\nmain()\n"
}
````

### User / tool · 2026-11-02T21:25:52.801Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2/probe_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:57.598Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2 && sed -i 's/\\[PY, \"-I\", \"-m\", \"app.main\"\\]/[PY, \"-m\", \"app.main\"]/' probe_r2.py && /Users/arsis/zlayt-pm-project/.venv/bin/python -I probe_r2.py 2>&1 | tee probe_r2.out",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:25:57.694Z

**tool result (error)**
````
Exit code 1
sed: 1: "probe_r2.py
": extra characters at the end of p command
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:25:59.655Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2 && python3 -c \"\np='probe_r2.py';s=open(p).read();s=s.replace('[PY, \\\"-I\\\", \\\"-m\\\", \\\"app.main\\\"]','[PY, \\\"-m\\\", \\\"app.main\\\"]');open(p,'w').write(s)\" && grep -n '\"app.main\"' probe_r2.py && /Users/arsis/zlayt-pm-project/.venv/bin/python -I probe_r2.py 2>&1 | tee probe_r2.out",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:26:28.450Z

**tool result**
````
36:    p = subprocess.Popen([PY, "-m", "app.main"], cwd=ARCH, env=env, stdout=log, stderr=subprocess.STDOUT)
A demo build http://127.0.0.1:56484 health: b'{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only \xe2\x80\x94 never paste real records","backend":"fixture","demo_mode":true,"answers":"p'
A 300 sequential creates: Counter({201: 200, 429: 100}) 3.3s | stored cases: 200
  sample 429 body: {"error":{"code":"busy","message":"This demo is full right now. Try again later.","detail":{"reason":"demo_full"}}}
  tokens: 200
A 150 concurrent runs: Counter({429: 140, 202: 10}) 1.4s
  sample run 429 body: {"error":{"code":"busy","message":"This demo is busy right now. Try again in a minute.","detail":{"reason":"demo_busy"}}}
  peak running seen by sampler (every 5th token, so lower bound): 0 | statuses after: {'ready': 1, 'ingested': 14}
  run after drain on an unused case: 202
  legit create while full: 429 {"error":{"code":"busy","message":"This demo is full right now. Try again later.","detail":{"reason":"demo_full"}}}
  DELETE own case: 204
  create after one delete: 201
  health: 200
  non-sample paste while full: 409 {"error":{"code":"demo_mode_unsupported_input","message":"This demo only runs the recorded sample cases.","detail":{}}}
  scan demo flood A: 451 blobs, bad strings found: []
  server log bytes: 0 | sentinel in log: False
B cap=20, 100 simultaneous creates: Counter({429: 80, 201: 20}) | stored: 20
C 60 simultaneous runs, default cap 4: Counter({429: 47, 202: 13}) 1.4s | peak sampled: 1
  statuses after: {'ready': 13, 'ingested': 47}
  fresh run: 202
  one sample run holds a slot for 0.1s
D env='0': 3 creates -> [201, 201, 201] (default 200 applies)
D env='-5': 3 creates -> [201, 201, 201] (default 200 applies)
D env='abc': 3 creates -> [201, 201, 201] (default 200 applies)
D env='': 3 creates -> [201, 201, 201] (default 200 applies)
E local, caps set to 5/1, 300 creates: Counter({201: 300}) | stored: 300
E local 150 concurrent runs: Counter({202: 150}) 7.7s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:46.718Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2 && cat > probe_rejudge.py <<'EOF'\nimport sys, json, time, threading\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2\")\nimport importlib.util\nsrc = open(\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2/probe_r2.py\").read().replace(\"\\nmain()\\n\", \"\\n\")\nns = {}; exec(compile(src, \"p\", \"exec\"), ns)\nfrom collections import Counter\np, base, d = ns[\"serve\"]({})\ntry:\n    codes, bodies = ns[\"creates\"](base, 100)\n    toks = ns[\"tokens_from\"](bodies)\n    # run a few then wait, so rejudge has a finished case\n    for t in toks[:3]:\n        ns[\"req\"](base, \"POST\", f\"/api/cases/{t}/run\", body={})\n        for _ in range(100):\n            if json.loads(ns[\"req\"](base, \"GET\", f\"/api/cases/{t}/status\")[2])[\"status\"] != \"running\": break\n            time.sleep(0.1)\n    out = []\n    def go(t):\n        t0 = time.time(); s, h, b = ns[\"req\"](base, \"POST\", f\"/api/cases/{t}/rejudge\", body={}); out.append((s, time.time() - t0, b[:100]))\n    ts = [threading.Thread(target=go, args=(t,)) for t in toks[:3] * 30]\n    t0 = time.time(); [x.start() for x in ts]; [x.join() for x in ts]\n    print(\"90 concurrent rejudge on 3 finished cases:\", Counter(s for s, _, _ in out), \"total %.1fs\" % (time.time() - t0), \"max single %.2fs\" % max(t for _, t, _ in out))\n    print(\"sample bodies:\", {o[2] for o in out})\n    print(\"health:\", ns[\"req\"](base, \"GET\", \"/api/health\")[0])\nfinally:\n    p.terminate(); p.wait(timeout=10)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I probe_rejudge.py 2>&1 | tee probe_rejudge.out",
 "timeout": 300000
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:48.107Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2/head && ls tests/fixtures 2>&1 | head -3; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_t183_limits.py -q 2>&1 | tail -8; echo rc=$?; cd /Users/arsis/zlayt-pm-project && git rev-parse --short HEAD; git diff --quiet 275e4ca HEAD -- app Dockerfile requirements.txt; echo gate_diff_rc=$?",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T21:26:49.783Z

**tool result**
````
90 concurrent rejudge on 3 finished cases: Counter({409: 78, 200: 12}) total 0.3s max single 0.25s
sample bodies: {b'{"error":{"code":"run_in_progress","message":"A run is already in progress for this case.","detail":', b'{"token":"N8P1a20fcDdfDxt9eESkIg","asked":0,"rejudged":[],"still_unavailable":[],"export_gate":{"rea', b'{"token":"UAMlkVHb70I7CZ0kjoXM-g","asked":0,"rejudged":[],"still_unavailable":[],"export_gate":{"rea', b'{"token":"1sOFgXKLxhmye6aWB-aWdw","asked":0,"rejudged":[],"still_unavailable":[],"export_gate":{"rea'}
health: 200
````

### User / tool · 2026-11-02T21:26:51.039Z

**tool result**
````
llm
make_curated.py
t140_restating_labels.txt
.........                                                                [100%]
9 passed in 0.78s
rc=0
f3d42a2
gate_diff_rc=1
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:26:53.786Z

**tool call — Bash**
````
{
 "command": "git diff --stat 275e4ca HEAD -- app Dockerfile requirements.txt; git diff 275e4ca HEAD -- app/backend/api.py app/backend/limits.py | head -40; pgrep -f \"r2_\" | head; lsof -iTCP -sTCP:LISTEN -P 2>/dev/null | grep -c python"
}
````

### User / tool · 2026-11-02T21:26:54.058Z

**tool result**
````
 app/backend/api.py             |  18 +-
 app/frontend/guided/app.js     | 166 +++++++++++++++
 app/frontend/guided/core.js    | 138 +++++++++++++
 app/frontend/guided/home.css   |   1 +
 app/frontend/guided/home.js    |  14 ++
 app/frontend/guided/index.html |  35 ++++
 app/frontend/guided/review.css |   1 +
 app/frontend/guided/review.js  |   5 +
 app/frontend/guided/step1.css  |   1 +
 app/frontend/guided/step1.js   |  10 +
 app/frontend/guided/step2.css  |   1 +
 app/frontend/guided/step2.js   |  12 ++
 app/frontend/guided/step3.css  |   1 +
 app/frontend/guided/step3.js   |  11 +
 app/frontend/guided/step4.css  |   1 +
 app/frontend/guided/step4.js   |   9 +
 app/frontend/guided/styles.css | 454 +++++++++++++++++++++++++++++++++++++++++
 17 files changed, 877 insertions(+), 1 deletion(-)
diff --git a/app/backend/api.py b/app/backend/api.py
index 077ccd8..3b846f6 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -681,7 +681,23 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         if (guided / "index.html").is_file():                                           # D-068: the guided app is the front door; the old screen stays reachable at /classic
             app.add_api_route("/classic", lambda: RedirectResponse("/classic/"), include_in_schema=False)       # the mount only answers /classic/ ; /classic would fall to the guided mount's 404
             app.mount("/classic", StaticFiles(directory=str(sd), html=True), name="classic")
-            app.mount("/", StaticFiles(directory=str(guided), html=True), name="frontend")
+            from fastapi.responses import FileResponse
+
+            class GuidedFiles(StaticFiles):
+                """The guided app uses real paths (/case/<token>/timeline). A path that is not a file and has no extension is a screen: answer index.html, which routes it in the browser.
+                /api and /classic never fall through to it (an unknown /api path must stay a JSON 404)."""
+                async def get_response(self, path, scope):
+                    try:
+                        resp = await super().get_response(path, scope)
+                    except StarletteHTTPException as e:
+                        if e.status_code != 404 or path.startswith(("api/", "classic/")) or path in ("api", "classic") or "." in path.rsplit("/", 1)[-1]:
+                            raise
+                        return FileResponse(guided / "index.html")
+                    if resp.status_code == 404 and not path.startswith(("api/", "classic/")) and "." not in path.rsplit("/", 1)[-1]:
+                        return FileResponse(guided / "index.html")
+                    return resp
+
+            app.mount("/", GuidedFiles(directory=str(guided), html=True), name="frontend")
         else:
             app.mount("/", StaticFiles(directory=str(sd), html=True), name="frontend")
     return app
0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:03.573Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"rate limit\\|limiter\" memory/SCOPE_CUTS.md | head -5; grep -n \"RETENTION_SECONDS\" app/db/db.py | head -3; grep -n \"purge_expired\" app/backend/*.py | head; sed -n 14p app/main.py; grep -n \"async def create_case\\|def make_case\" app/backend/api.py"
}
````

### User / tool · 2026-11-02T21:27:03.684Z

**tool result**
````
105:| 24 | Per-client rate limit and spend cap on the public demo (D-020, CONTRACT §314) | The public build makes no model calls (demo mode serves prepared answers), so there is no wallet to protect. Storage and in-flight run caps (T-183) bound disk and CPU; a per-IP limiter is not built. | Per-IP token bucket + spend ledger if a live key is ever exposed publicly; ~0.5 day. | post-MVP |
17:RETENTION_SECONDS = 24 * 3600
297:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
app/backend/api.py:217:                DB.purge_expired(c, time.time())
app/backend/api.py:357:            DB.purge_expired(c, now)
    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
287:    async def create_case(request: Request):
305:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
345:    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None, strict_name=True):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:08.582Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2/head && grep -n \"async def create_case(\\|def make_case\\|DB.purge_expired(c, now)\\|limits\\.\\|async def run_case\\|runs\\[token\\] = \" app/backend/api.py"
}
````

### User / tool · 2026-11-02T21:27:08.667Z

**tool result**
````
286:    async def create_case(request: Request):
344:    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None, strict_name=True):
356:            DB.purge_expired(c, now)
357:            if (full := limits.case_full(c, local_mode())):          # T-183 r2: public demo stores at most DEMO_MAX_CASES
436:    async def run_case(token: str, request: Request):
450:            if (busy := limits.runs_busy(len(runs), local_mode())):  # T-183 r2: public demo runs at most DEMO_MAX_RUNS at once
455:            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:09.782Z

Now the review file.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:37.084Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-183-security-r2.md",
 "content": "# T-183 security review, round 2 (security-reviewer, claude-sonnet-5-5)\n\nScope: commit 275e4ca, tested from `git archive 275e4ca` at `artifacts/review-evidence/T-183-r2/head`. At the first check `git rev-parse --short HEAD` was 275e4ca; at write time it was f3d42a2. `git diff --stat 275e4ca HEAD -- app Dockerfile requirements.txt` shows 17 files changed, all of them frontend/guided files plus `api.py` (+17/-1, a static-file mount that falls back to index.html). `limits.py` and the two limit hooks did not move, and the `/api` routes are registered before that mount. Probes: `probe_r2.py`, `probe_rejudge.py` and their `.out` files beside the archive. I started servers on free ports of my own (ephemeral ports from the OS) and stopped only those PIDs.\n\nVerdict: **pass**. There is no blocker and no major. The round-1 major (unbounded stored cases and runs) is closed. One minor and one nit remain.\n\n## Round-1 major: closed\n\nPublic demo build (`ZLAYT_MODE` unset), `LLM_BACKEND=anthropic-api` with a sentinel key present and `ENABLE_LIVE` unset:\n- **300 sequential creates:** `Counter({201: 200, 429: 100})` in 3.3 s. The sqlite table held exactly 200 cases.\n- **150 concurrent runs on those cases:** `Counter({429: 140, 202: 10})` in 1.4 s. A sample run holds its slot for about 0.1 s, so more than 4 can be admitted over a burst, but never more than 4 at once (see the race answer below).\n- **429 bodies are one plain sentence:**\n  - `{\"error\":{\"code\":\"busy\",\"message\":\"This demo is full right now. Try again later.\",\"detail\":{\"reason\":\"demo_full\"}}}`\n  - `{\"error\":{\"code\":\"busy\",\"message\":\"This demo is busy right now. Try again in a minute.\",\"detail\":{\"reason\":\"demo_busy\"}}}`\n- **No leak:** 451 captured responses (headers and bodies) contained none of `Traceback`, `File \"`, `/Users`, `sk-ant`, `sqlite`, `DEMO_MAX`, `limits.py` or the sentinel. The server log was 0 bytes. `/api/health` stayed 200 throughout.\n- **Order of checks:** a non-sample paste while the table is full still returns 409 \"This demo only runs the recorded sample cases.\" (the demo gate wins over 429, nothing stored).\n- **Bad env values:** `DEMO_MAX_CASES` and `DEMO_MAX_RUNS` set to `0`, `-5`, `abc` or empty all fall back to the defaults (3 creates each returned 201), so a typo can neither switch the cap off nor lock the demo shut.\n\n## Is \"creates may overshoot by a few under a race\" acceptable? Yes, and in this build it does not overshoot\n\nMeasured: `DEMO_MAX_CASES=20` with 100 simultaneous creates gave `Counter({429: 80, 201: 20})` and 20 stored. `DEMO_MAX_RUNS` default with 60 simultaneous runs gave 13 admitted and 47 refused, with at most 4 in flight by construction. The reason is structural: `create_case` is `async def` (api.py:286) and `make_case` (api.py:344-357) has no `await` between the `COUNT(*)` and the insert. `run_case` (api.py:436) likewise has no `await` between the `len(runs)` check (api.py:450) and `runs[token] = ...` (api.py:455). Both run on the single event-loop thread. `app/main.py:14` starts one uvicorn process with no `workers=`. So the \"few\" can only appear if someone adds uvicorn workers or turns these routes into plain `def`. Even then the excess is bounded by the number of simultaneous requests, never unbounded. For a resource bound on a synthetic demo that is acceptable. The wording in the docstring is more pessimistic than the code; see the nit.\n\n## Dev mode is unlimited\n\n`ZLAYT_MODE=local` with `DEMO_MAX_CASES=5` and `DEMO_MAX_RUNS=1` set (so the caps would bite if they applied): 300 creates all 201 with 300 stored, 150 concurrent runs all 202 (`Counter({202: 150})`). `limits.case_full` and `limits.runs_busy` return `None` when `local` is true (limits.py:34-35, 41-42).\n\n## Tests\n\n`tests/unit/test_t183_limits.py` in the archive: 9 passed (`.venv/bin/python -m pytest -p no:cacheprovider`).\n\n## What I would still change (not a spec violation)\n\nA refuse-when-full cap turns resource exhaustion into a lockout. One scripted client creates 200 cases in about 2 s (300 requests took 3.3 s) and every other visitor gets 429 \"This demo is full right now\" on `POST /api/cases` until the 24 h retention purge (db.py:17, run only from make_case at api.py:356 and api.py:217) reaches the attacker's cases. I confirmed that while full a legitimate create returns 429, and that `DELETE` of one case (needs that case's token) frees one slot (204, then 201). That is the trade-off the worker documented (\"oldest cases are not pruned, create is refused instead\"); round 1 offered it as an allowed option, so this is a \"would have done it differently\" call, filed as minor.\n\n```json\n{\"card\": \"T-183\", \"persona\": \"security-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive of 275e4ca at artifacts/review-evidence/T-183-r2/head (HEAD was 275e4ca at first check, f3d42a2 at write time; later changes are frontend/guided files and a static-file mount in api.py, limits.py and both hooks unchanged); demo and local builds on ephemeral 127.0.0.1 ports; no live model call\",\n \"exercised\": [\n  \"read reviews/T-183-security.md (round 1) and python3 tools/board.py show T-183\",\n  \"read personas/security.md and app/backend/limits.py; read the two hooks in api.py (create_case/make_case 286-357, run_case 436-455) and git show 275e4ca -- app/backend/api.py\",\n  \"probe_r2.py A: demo build, sentinel key + LLM_BACKEND=anthropic-api, ENABLE_LIVE unset: 300 sequential creates (201x200, 429x100, 200 stored), 150 concurrent runs (202x10, 429x140), 429 bodies, legitimate create while full (429), DELETE own case then create (204, 201), health 200, non-sample paste while full (409), scan of 451 responses and the server log for Traceback, File, /Users, sk-ant, sqlite, DEMO_MAX, limits.py and the sentinel (none; log 0 bytes)\",\n  \"probe_r2.py B: DEMO_MAX_CASES=20 with 100 simultaneous creates: 201x20, 429x80, 20 stored\",\n  \"probe_r2.py C: default caps, 60 simultaneous runs: 202x13, 429x47; one sample run holds a slot about 0.1 s\",\n  \"probe_r2.py D: DEMO_MAX_CASES/DEMO_MAX_RUNS = 0, -5, abc, empty: default applies (201 each)\",\n  \"probe_r2.py E: ZLAYT_MODE=local with caps set to 5 and 1: 300 creates all 201 (300 stored), 150 concurrent runs all 202\",\n  \"probe_rejudge.py: 90 concurrent /rejudge on 3 finished demo cases: 409x78, 200x12 in 0.3 s, asked 0 (recorded replay only), health 200\",\n  \".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_t183_limits.py in the archive: 9 passed\",\n  \"git rev-parse --short HEAD (275e4ca, later f3d42a2); git diff --stat 275e4ca HEAD -- app Dockerfile requirements.txt (17 files, frontend plus api.py static mount); grep memory/SCOPE_CUTS.md (row 24 records the limiter cut); grep app/db/db.py RETENTION_SECONDS 24 h\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"key_exposure\": 5, \"demo_mode_isolation\": 5, \"input_limits\": 5, \"error_plainness\": 5, \"resource_abuse_resistance\": 4, \"cut_documentation\": 5},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"A full case table locks every visitor out for up to 24 h; one scripted client can do it in about 2 seconds\",\n   \"evidence\": \"probe_r2.py A: 300 sequential creates in 3.3 s gave 201x200 then 429x100; 'legit create while full: 429 ... This demo is full right now. Try again later.' Only the 24 h purge (db.py:17 RETENTION_SECONDS, purge_expired db.py:297, called at api.py:356 and api.py:217) or a DELETE with that case's token frees a slot; DELETE of one case gave 204 then a create returned 201. The handoff states 'oldest cases are not pruned, create is refused instead'.\",\n   \"why_it_matters\": \"The cap closes disk and CPU exhaustion, but the public link can still be made unusable by one curl loop, repeated once a day. No money, secret or data is involved, so this is availability only. It is a design preference, not a spec violation: round 1 allowed 'refused' as the alternative to pruning.\",\n   \"fix\": \"When the table is full, delete the oldest case that is older than a short floor (for example 1 hour) before refusing, so only truly fresh floods get a 429; or give demo-created cases a shorter retention (for example 2 hours) since the sample is a recorded case that is cheap to recreate.\",\n   \"acceptance_test\": \"With DEMO_MAX_CASES=3, create 3 cases, age one past the floor, then a 4th create returns 201 and the stored count stays 3; with all 3 younger than the floor the 4th returns 429 with the same one-sentence body.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"The 'soft bound / overshoot by a few' wording understates what the code does, and nothing pins the reason\",\n   \"evidence\": \"limits.py docstring: 'simultaneous creates can overshoot it by a few'. probe_r2.py B: DEMO_MAX_CASES=20, 100 simultaneous creates, 20 stored. The exactness depends on create_case and run_case being async def with no await between check and insert (api.py:286, 344-357, 436, 450-455) and on one uvicorn process (app/main.py:14).\",\n   \"why_it_matters\": \"A later change to plain `def` routes or `workers=N` would turn an exact bound into a leaky one without any test failing, and the comment would not tell the next person why it was exact.\",\n   \"fix\": \"State in the limits.py docstring that the bound is exact because the check and insert run on one event-loop thread, and add a test with many simultaneous creates against a small cap that asserts the stored count equals the cap.\",\n   \"acceptance_test\": \"A test starts 50 threads creating against DEMO_MAX_CASES=5 and asserts exactly 5 stored.\"}\n ],\n \"whats_right\": [\n  \"Both caps are enforced after input validation and before any state changes, and a refused request leaves nothing stored and returns a one-sentence JSON 429 with no trace, key or env-var name.\",\n  \"A zero, negative or unreadable cap value falls back to the default, so a typo cannot turn the limit off or lock the demo shut.\",\n  \"Local mode is unlimited, so the caps cannot interfere with development or the recorded-answer workflow.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T21:27:37.304Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-183-security-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:39.979Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-183-r2/head && grep -n \"if local\" app/backend/limits.py; cd /Users/arsis/zlayt-pm-project && python3 tools/board.py validate 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T21:27:40.166Z

**tool result**
````
33:    if local:
40:    if local:
ok (190 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:44.618Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nopen('reviews/T-183-security-r2.md','a').write('\\nCorrection (line refs): the local early-returns in limits.py are at lines 33-34 (case_full) and 40-41 (runs_busy), not 34-35 and 41-42 as written above.\\n')\" && tail -3 reviews/T-183-security-r2.md && python3 tools/board.py validate | tail -1"
}
````

### User / tool · 2026-11-02T21:27:44.817Z

**tool result**
````
```

Correction (line refs): the local early-returns in limits.py are at lines 33-34 (case_full) and 40-41 (runs_busy), not 34-35 and 41-42 as written above.
ok (190 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:27:48.271Z

T-183 r2 verdict is **pass** (0 blockers, 0 majors, 1 minor, 1 nit). I tested `git archive 275e4ca`. The flood gave 200 of 300 creates at 201 (stored count 200) and 10 of 150 concurrent runs at 202. The rest got a plain-sentence 429 with no trace and no key, dev mode stayed unlimited (300 creates and 150 runs all succeeded), and `tests/unit/test_t183_limits.py` passed 9/9.

The "overshoot by a few" worry doesn't happen: 100 simultaneous creates against a cap of 20 stored exactly 20, because the create and run routes have no `await` between check and insert, on a single uvicorn process. The minor: a full table locks all visitors out until the 24 h purge, and one scripted client can fill it in about 2 s. The review is at `/Users/arsis/zlayt-pm-project/reviews/T-183-security-r2.md`, and `board.py validate` is ok.
