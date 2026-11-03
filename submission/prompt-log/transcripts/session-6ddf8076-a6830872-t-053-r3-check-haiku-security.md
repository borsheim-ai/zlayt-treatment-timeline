# Subagent: T-053 r3 check (haiku security) (T-053 r3 check (haiku security))

Source: `agent-a68308728482094b9.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:33:32.683Z

Round-3 check of board card T-053 in /Users/arsis/zlayt-pm-project. Read reviews/T-053-security-r2.md and confirm both majors are closed:

1. Commit 08764e7: in ZLAYT_MODE=local, non-loopback peers get 403, whatever bind address is used. Reproduce your r2 probe: `uvicorn app.main:create --factory --host 0.0.0.0` on a spare port with ZLAYT_MODE=local, then GET /api/cases from the LAN address (expect 403) and from 127.0.0.1 (expect 200). Stop the server afterwards. Use a dummy key only.
2. D-036 in memory/ORCHESTRATOR_DECISIONS.md amends D-020, and R-CO-4 in spec/REQUIREMENTS.md cites it.

Also run `python3 -m pytest -q tests/unit/test_api_routes.py`.

Write reviews/T-053-security-r3.md, append-only, with a ```json block containing card, persona, verdict and findings. Reply in 2 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:33:34.697Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/security.md"
}
````

### User / tool · 2026-11-02T02:33:34.704Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:33:34.881Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-053-security-r2.md"
}
````

### User / tool · 2026-11-02T02:33:34.887Z

**tool result**
````
1	# T-053 security review, round 2 (security-reviewer, Tomas Rivas lens)
2	
3	Pinned code: HEAD e83eb54, extracted with `git archive` to `artifacts/review-evidence/T-053-r2/head_e83eb54`. HEAD moved during the review (02f9939 when the card went to review, then 709397e, f5444a8, e83eb54, d796383, d0c9cdb). The gate files `app/llm/provider.py`, `app/llm/backends/anthropic_api.py`, `app/main.py` and `app/backend/api.py` are byte-identical from 02f9939 through d0c9cdb (`git diff --quiet 02f9939 d0c9cdb -- ...` not run on d0c9cdb; checked 02f9939..e83eb54 exit 0, and e83eb54..d0c9cdb touches only `pipeline.py`, `audited.py` and `split_v1.md`). Everything below was run on e83eb54.
4	
5	Verdict: **changes**. The round-1 blocker (demo mode sends live SDK calls) is closed on every path I could reach. Two majors remain: the local-mode loopback refusal is bypassed by the uvicorn CLI, and the library-in-local-demo admission still has no written amendment of D-020 / R-CO-4. No new blocker.
6	
7	Checks requested by the brief:
8	1. Demo mode with `LLM_BACKEND=anthropic-api`, `ANTHROPIC_API_KEY=<redacted> `ENABLE_LIVE` unset selects the fixture backend. The SDK constructor and `messages.create` were counted and blocked: 0 events and 0 socket attempts, for `provider.complete`, the claude-cli selection, and a full API sample run. PASS.
9	2. `ZLAYT_MODE=local HOST=0.0.0.0` refuses to start under `python -m app.main`: exit 1, no listener. PASS for that entry point. FAIL for `uvicorn app.main:create --factory --host 0.0.0.0` with HOST unset (finding 1).
10	3. Library texts are admitted only in local mode: public 404 / 409, local 201. PASS for the code. The spec conflict is open (finding 2).
11	
12	Probe scripts: `artifacts/review-evidence/T-053-r2-probe.py` (parts 1, 2, 2b, 3, 3b) and `artifacts/review-evidence/T-053-r2-probe2.py` (checks A, B, C). Outputs: `artifacts/review-evidence/T-053-r2/out_parts_1_2_2b.txt`, `out_part3.txt`, `out_part3b.txt`, `out_probe2.txt`.
13	
14	Exercised (all on e83eb54 unless noted):
15	- `python3 tools/board.py show T-053`; read `personas/security.md`, my memory dir, `reviews/T-053-security.md`.
16	- `git log --oneline -n 8`, `git show --stat 02f9939`, `git diff --stat 02f9939 709397e -- app tests`, `git diff --quiet` on the gate files between each HEAD pair listed above.
17	- `git archive e83eb54 | tar -x -C artifacts/review-evidence/T-053-r2/head_e83eb54` (and the same for 709397e and 02f9939 during the review).
18	- `.venv/bin/python -m pytest -p no:cacheprovider` in the pinned copy, with the six new or changed round-1 tests named by the card note: `test_demo_never_reaches_a_live_backend[claude-cli]`, `[anthropic-api]`, `test_demo_health_reports_fixture_even_if_live_backend_and_key_are_set`, `test_local_mode_refuses_non_loopback_host` (5 hosts), `test_library_texts_are_admitted_only_in_local_mode`, `test_case_list_and_library_exist_only_in_local_mode`, `test_cases_do_not_leak_decisions_between_each_other`: `11 passed in 1.87s`.
19	- `.venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_provider_backends.py tests/unit/test_api_routes.py tests/e2e/test_api.py -q`: `57 passed in 8.14s`.
20	- `.venv/bin/python -m pytest -p no:cacheprovider tests/unit -q` (full unit suite): `6 failed, 867 passed in 17.34s` (see outside-lens note).
21	- `.venv/bin/python -I artifacts/review-evidence/T-053-r2-probe.py 1 2 2b`: output in `out_parts_1_2_2b.txt`.
22	- `.venv/bin/python -I artifacts/review-evidence/T-053-r2-probe.py 3` and `3b`: outputs in `out_part3.txt` and `out_part3b.txt`. Part 3b started uvicorn on port 7972 for about 5 seconds, made one HTTP GET to the machine's LAN address, and killed it. Logged output shows `uvicorn stopped`.
23	- `.venv/bin/python -I artifacts/review-evidence/T-053-r2-probe2.py` (checks A, B, C): output in `out_probe2.txt`.
24	- Manual uvicorn start on port 7973 with `--host 0.0.0.0` and `ZLAYT_MODE=local` for a debug check (killed afterwards via `lsof -ti tcp:7973 | xargs kill`; listener count 0 after).
25	- `.venv/bin/python -c "inspect.signature(anthropic.resources.Messages.create)"`: `anthropic 2.3.0`, `temperature in Messages.create signature: False`.
26	- `ls requirements*.txt pyproject.toml Makefile Dockerfile` in the pinned copy: `requirements-dev.txt`, `requirements.txt` present; no pyproject, Makefile or Dockerfile. `.venv/bin/pip-audit`: `No such file or directory`.
27	- `.venv/bin/python tools/check_secrets.py` on the working tree at d0c9cdb: `check_secrets: ok (740 file(s) scanned)`. Key-shaped grep (`sk-ant-|sk-proj-`) over `app` and `tests` in the pinned copy: 0 hits.
28	- `grep` of D-020 in `memory/ORCHESTRATOR_DECISIONS.md` at e83eb54 (line 28, unchanged from 02f9939) and R-CO-4 in `spec/REQUIREMENTS.md:138`.
29	- `app/backend/api.py` `BANNER` at e83eb54: `Synthetic data only — never paste real records`.
30	
31	Findings detail:
32	
33	Finding 1 (major, new in round 2). The round-1 loopback rule reads the `HOST` environment variable, not the address uvicorn binds. `uvicorn app.main:create --factory --host 0.0.0.0` with `ZLAYT_MODE=local` and `HOST` unset starts, and the case list is served to the LAN. Verbatim from `out_part3b.txt`: `GET http://LAN-address:7972/api/cases -> 200 body keys: ['cases']` and `Python 73551 arsis 9u IPv4 ... TCP *:7972 (LISTEN)`. The gate at `app/backend/api.py:93-94` reads `os.environ.get("HOST", "127.0.0.1")`; `app/main.py:9` documents `uvicorn app.main:create --factory` as a launch line. The probe uses `--host` only, so `HOST` is never set. This is a partial fix of the round-1 major and the card decision (2): the refusal covers `python -m app.main` only.
34	
35	Finding 2 (major, carried from round 1, not closed). Library texts are admitted in local demo mode, and nothing in `memory/ORCHESTRATOR_DECISIONS.md` amends D-020 for this. Verbatim D-020 (line 28, unchanged): `in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and not stored`. R-CO-4 (`spec/REQUIREMENTS.md:138`) says the same. In local mode `demo_mode()` is true whenever `ENABLE_LIVE` is unset (`app/backend/api.py:103-106`), so the spec text applies. Observed: `POST {text: library text} -> 201` in local mode and `-> 409` in public mode. The card decision (3) is a reasonable call, but it is not an amendment. Per D.2 a spec conflict is a blocker; I am holding it at major because the path is local-only and the data is synthetic. If the amendment is not written before the milestone gate, re-rate to blocker.
36	
37	Finding 3 (minor). With `ENABLE_LIVE=1`, `LLM_BACKEND=anthropic-api` and no key, the server reports the live backend while demo mode is on, and every run fails. Verbatim from `out_probe2.txt` check A: `/api/health: backend=anthropic-api demo_mode=True live_enabled=False` and `llm_calls (backend, error[:60], n): [('anthropic-api', 'BACKEND_UNAVAILABLE', 66)]`, with `SDK ctor/create events: 0`. No live call happens (the key check runs before the client is built), so this fails closed. It does break card decision (1), "demo mode ALWAYS uses the fixture backend", and the sample demo cannot run in this configuration. Cause: `app/llm/provider.py:27-29` returns the live name whenever `ENABLE_LIVE=1`, without the key check that `live_enabled()` applies (`app/backend/api.py:103`).
38	
39	Finding 4 (minor). `RECORD_FIXTURES=1` alone opens live SDK calls on the dev eval path. Verbatim from `out_probe2.txt` check B: `backend_name() outside any context = fixture`, `run_case returned`, `[B] SDK ctor/create events: 132`. The mechanism is `app/backend/pipeline.py:392-393` and `:406`, which call `P.record_context` / `record_fragment_context` when `P._recording()` is true (`provider.py:88-89`), and those contexts set `_record_ok`, which bypasses the ENABLE_LIVE check in `provider.py:27-29`. The server does not reach this: `run_case` has no caller in `app/backend/api.py`, and `judge_summary` is called only from `app/llm/record.py:60,66`. With `RECORD_FIXTURES=1` the API sample run made `0` SDK events (`out_parts_1_2_2b.txt`, `[API run, RECORD_FIXTURES=1]`). The docstring at `provider.py:24-26` ("ALWAYS 'fixture'") is therefore true for the server and false for the dev tools. Fix: require ENABLE_LIVE=1 in addition to record mode before `_record_ok` can be set, or narrow the docstring.
40	
41	Finding 5 (minor, carried from round 1, partly addressed). Pins now exist: `requirements.txt` has `anthropic==2.3.0` at line 5, with `==` pins throughout. But the pinned SDK does not accept the kwarg the backend passes: `temperature in Messages.create signature: False`, while `app/llm/backends/anthropic_api.py:26` passes `temperature=0`. So the live path cannot work with the pinned version. `pip-audit` is not installed (`.venv/bin/pip-audit: No such file or directory`), and there is no Makefile, so the round-1 request to add `pip-audit` to `make test` has no target.
42	
43	Outside my lens (reported, not graded):
44	- Six unit tests fail at e83eb54: `test_case_extras.py` x2, `test_narrative.py` x1, `test_t037_backend.py` x3. They fail on fixture misses (judge and extract steps, `FIXTURE_MISS` rows), not on the gate. `LLM_BACKEND=fixture` resolves to `fixture` before and after round 1, so the gate change does not touch them. The card note says 865 passed; the current run is 867 passed, 6 failed.
45	- With the default fixture directory, the sample demo run has 18 `FIXTURE_MISS` rows out of 37 calls. With `FIXTURE_SET=curated` (`out_probe2.txt` check C) it has 38 rows and 0 errors. The public deploy needs `FIXTURE_SET=curated`, and nothing in the repo sets it (no Dockerfile or config file).
46	
47	What is right:
48	- Demo mode cannot reach the SDK or the network: with the dummy key, `ENABLE_LIVE` unset, `LLM_BACKEND` set to anthropic-api or claude-cli, the provider call, the API sample run and the RECORD_FIXTURES=1 API run each showed `SDK constructor/create calls: 0 | socket attempts: 0`.
49	- The `python -m app.main` refusal is clean: `python -m app.main exit code: 1`, `stderr last line: RuntimeError: ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost`, and `listener on 7971 after refusal: none`.
50	- Public route gating holds with `ZLAYT_MODE` unset: `GET /api/cases -> 404 | GET /api/library -> 404`, `POST {library} -> 404`, `POST {text: library text} -> 409`.
51	
52	```json
53	{"card": "T-053", "persona": "security-reviewer", "model": "claude-haiku-5-5",
54	 "scope": "HEAD e83eb54 (pinned archive artifacts/review-evidence/T-053-r2/head_e83eb54); fix commit 02f9939 and HEAD d0c9cdb checked for gate-file drift; local app runs on 127.0.0.1 (7971 refusal, 7972 and 7973 bypass checks, stopped); sample case and library case lib01 (case_lib01_er_only_then_gap); dummy key only",
55	 "exercised": [
56	  "python3 tools/board.py show T-053; read personas/security.md, memory dir, reviews/T-053-security.md",
57	  "git log --oneline; git show --stat 02f9939; git diff --stat 02f9939 709397e -- app tests; git diff --quiet on app/llm/provider.py, app/llm/backends/anthropic_api.py, app/main.py, app/backend/api.py between each HEAD pair (exit 0 through e83eb54 and d0c9cdb)",
58	  "git archive e83eb54 into artifacts/review-evidence/T-053-r2/head_e83eb54 (also 709397e and 02f9939 during the review)",
59	  "pytest -p no:cacheprovider on the 7 round-1 tests named in the card note: 11 passed in 1.87s",
60	  "pytest tests/unit/test_provider_backends.py tests/unit/test_api_routes.py tests/e2e/test_api.py -q: 57 passed in 8.14s",
61	  "pytest tests/unit -q: 6 failed, 867 passed in 17.34s (failures are fixture misses outside the gate)",
62	  "artifacts/review-evidence/T-053-r2-probe.py parts 1, 2, 2b, 3, 3b with SDK constructor and socket counting: out_parts_1_2_2b.txt, out_part3.txt, out_part3b.txt",
63	  "artifacts/review-evidence/T-053-r2-probe2.py checks A (ENABLE_LIVE=1 no key), B (RECORD_FIXTURES=1 dev eval path), C (FIXTURE_SET=curated sample run): out_probe2.txt",
64	  "manual uvicorn app.main:create --factory --host 0.0.0.0 on port 7973 with ZLAYT_MODE=local; killed afterwards",
65	  "inspect.signature(anthropic.resources.Messages.create) under .venv: anthropic 2.3.0, temperature not in signature",
66	  "ls requirements*.txt pyproject.toml Makefile Dockerfile; .venv/bin/pip-audit absent; requirements.txt line 5 anthropic==2.3.0",
67	  "tools/check_secrets.py on the working tree: check_secrets: ok (740 file(s) scanned); key-shaped grep over app and tests in the pinned copy: 0 hits",
68	  "grep memory/ORCHESTRATOR_DECISIONS.md:28 (D-020) and spec/REQUIREMENTS.md:138 (R-CO-4); api.py BANNER line 33"
69	 ],
70	 "verdict": "changes",
71	 "scores": {"live-call gating in demo mode (checklist 4)": 4, "local-mode exposure and bind address (checklist 18, round-1 major 2)": 2, "library admission scope vs D-020 and R-CO-4": 3, "secrets and key handling (checklist 10-11)": 4, "dependency pinning and audit (checklist 13)": 2},
72	 "findings": [
73	  {"severity": "major",
74	   "title": "Local-mode loopback refusal reads the HOST env var, not the bind address: uvicorn --host 0.0.0.0 exposes the case list",
75	   "evidence": "out_part3b.txt: 'server started (process alive): True' ; 'GET http://LAN-address:7972/api/cases -> 200 body keys: ['cases']' ; lsof 'Python 73551 ... TCP *:7972 (LISTEN)'. Gate app/backend/api.py:93-94 reads os.environ.get('HOST', '127.0.0.1'); app/main.py:9 documents 'uvicorn app.main:create --factory'. Probe launched with --host 0.0.0.0 and HOST unset under ZLAYT_MODE=local.",
76	   "why_it_matters": "Local mode has no authentication. GET /api/cases returns every case token, and each token is the only capability for that case. The data is synthetic (BANNER at app/backend/api.py:33), which limits the impact. The round-1 decision (2) was that local mode refuses to start unless HOST is loopback; the implemented refusal covers python -m app.main only.",
77	   "fix": "Enforce the rule on the peer, not the configured host: in local mode, return 404 for any /api request whose request.client.host is not a loopback address (127.0.0.1, ::1). Keep the startup check as well. Document that local mode is launched with python -m app.main.",
78	   "acceptance_test": "tests/unit/test_api_routes.py: TestClient(create_app(...), client=('192.168.1.20', 50000)) with ZLAYT_MODE=local returns 404 on GET /api/cases; with client=('127.0.0.1', 50000) returns 200. Probe: uvicorn --host 0.0.0.0 with ZLAYT_MODE=local: GET from the LAN address returns non-200."},
79	  {"severity": "major",
80	   "title": "Library texts admitted in local demo mode with no written amendment of D-020 / R-CO-4 (carried from round 1)",
81	   "evidence": "out_parts_1_2_2b.txt PART2b: public 'POST {text: library text} -> 409'; local (ZLAYT_MODE=local, HOST=127.0.0.1) 'POST {text: library text} -> 201'. memory/ORCHESTRATOR_DECISIONS.md:28 (D-020) at e83eb54: 'in demo mode accepts only text whose normalized hash ... equals a recorded fixture; anything else is rejected and not stored'. spec/REQUIREMENTS.md:138 (R-CO-4) same. app/backend/api.py:88 and :260 admit library hashes; demo_mode() true in local mode without ENABLE_LIVE (api.py:103-106).",
82	   "why_it_matters": "The spec says demo mode accepts only recorded text. The card decision (3) admits unrecorded library texts in local demo mode, and the decision is not written as an amendment, so the code and the spec disagree. Public build is unaffected (409). If the amendment is not recorded before the gate, this is a blocker under D.2.",
83	   "fix": "Chris rules. If yes, add a dated amendment to D-020 and R-CO-4 scoped to ZLAYT_MODE=local, and keep library texts on recorded fixtures only. If no, admit only texts whose hash is in app.state.recorded until T-052 records library fixtures.",
84	   "acceptance_test": "Either memory/ORCHESTRATOR_DECISIONS.md carries a dated D-0xx that amends D-020 for ZLAYT_MODE=local and R-CO-4 cites it, or tests/unit/test_api_routes.py asserts 409 for an unrecorded library text in local mode."},
85	  {"severity": "minor",
86	   "title": "ENABLE_LIVE=1 without a key: health reports anthropic-api while demo_mode is true; every run fails with BACKEND_UNAVAILABLE",
87	   "evidence": "out_probe2.txt check A: '/api/health: backend=anthropic-api demo_mode=True live_enabled=False'; \"llm_calls (backend, error[:60], n): [('anthropic-api', 'BACKEND_UNAVAILABLE', 66)]\"; 'SDK ctor/create events: 0'. Cause app/llm/provider.py:27-29 (backend_name returns the live name whenever ENABLE_LIVE=1), versus app/backend/api.py:103 (live_enabled also needs a key).",
88	   "why_it_matters": "No live call happens, so this fails closed. It does contradict card decision (1), 'demo mode ALWAYS uses the fixture backend', and it means the sample demo cannot run under this configuration, with the audit rows labelled as the live backend.",
89	   "fix": "In provider.backend_name, return 'fixture' unless ENABLE_LIVE=1 and the backend has its credential (ANTHROPIC_API_KEY for anthropic-api; claude CLI present for claude-cli), matching live_enabled().",
90	   "acceptance_test": "tests/unit/test_provider_backends.py: ENABLE_LIVE=1, LLM_BACKEND=anthropic-api, ANTHROPIC_API_KEY unset: backend_name() == 'fixture'; /api/health backend == 'fixture'; a sample run writes no llm_calls row with backend 'anthropic-api'."},
91	  {"severity": "minor",
92	   "title": "RECORD_FIXTURES=1 alone opens live SDK calls on the dev eval path (not reachable from the server)",
93	   "evidence": "out_probe2.txt check B: 'backend_name() outside any context = fixture'; 'run_case returned'; '[B] SDK ctor/create events: 132'. Mechanism: app/backend/pipeline.py:392-393 and :406 call P.record_context / record_fragment_context when P._recording() (provider.py:88-89), and those set _record_ok, which bypasses provider.py:27-29. Server path: out_parts_1_2_2b.txt '[API run, RECORD_FIXTURES=1] SDK constructor/create calls: 0'. run_case has no caller in app/backend/api.py; judge_summary is called only from app/llm/record.py:60,66.",
94	   "why_it_matters": "provider.py:24-26 says live calls need ENABLE_LIVE=1 'or an explicit record_context() (dev recording)', and says demo is ALWAYS fixture. The docstring is true for the server and false for the dev tools. A second env var that opens live calls is a configuration trap if the dev tools ever run on the public host.",
95	   "fix": "In record_context and record_fragment_context, require ENABLE_LIVE=1 before setting _record_ok (record mode then needs both env vars), or narrow the docstring to say which entry points can record.",
96	   "acceptance_test": "tests/unit/test_provider_backends.py: RECORD_FIXTURES=1, LLM_BACKEND=anthropic-api, key set, ENABLE_LIVE unset: pipeline.run_case(golden sample) makes 0 SDK calls (SDK constructor patched to count)."},
97	  {"severity": "minor",
98	   "title": "Pinned anthropic SDK (2.3.0) cannot accept the temperature kwarg the live backend passes; pip-audit not run; no make target",
99	   "evidence": "requirements.txt:5 'anthropic==2.3.0'. Under .venv: inspect.signature(anthropic.resources.Messages.create) has 'temperature' False. app/llm/backends/anthropic_api.py:26 passes temperature=0. '.venv/bin/pip-audit: No such file or directory'. ls: no Makefile, pyproject.toml or Dockerfile.",
100	   "why_it_matters": "The round-1 minor asked for pins plus pip-audit. Pins now exist, but the pinned SDK makes the live path fail with TypeError, and no audit is run. Checklist 13 is only partly met.",
101	   "fix": "Pin an SDK release whose Messages.create accepts temperature, verify the live path with a stub, install pip-audit into the venv and record 'pip-audit -r requirements.txt' output, and add a Makefile test target or a documented check command.",
102	   "acceptance_test": "A test asserts 'temperature' in inspect.signature(anthropic.resources.Messages.create).parameters for the pinned version; pip-audit -r requirements.txt exits 0 or each finding is triaged."}
103	 ],
104	 "whats_right": [
105	  "Demo mode makes no SDK or socket call: with LLM_BACKEND=anthropic-api, a dummy key and ENABLE_LIVE unset, the provider call, the API sample run and the RECORD_FIXTURES=1 API run each showed 0 SDK constructor/create calls and 0 socket attempts (out_parts_1_2_2b.txt).",
106	  "The python -m app.main refusal is clean: exit code 1 with the RuntimeError message, and no listener on the refused port (out_part3.txt).",
107	  "Public routes are gated with ZLAYT_MODE unset: GET /api/cases and GET /api/library return 404, POST {library} returns 404, and an unrecorded text returns 409 (out_parts_1_2_2b.txt PART2b)."
108	 ],
109	 "questions_for_chris": [
110	  "Does local demo mode admit unrecorded library texts (card decision 3)? If yes, please record the amendment to D-020 and R-CO-4 for ZLAYT_MODE=local; if no, library texts stay recorded-only until T-052 lands (finding 2).",
111	  "Should local mode refuse non-loopback peers outright (finding 1), or is a LAN override wanted? Round-1 question 3 is still open."
112	 ]}
113	```
114	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:33:35.129Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/project_config_gate_patterns.md"
}
````

### User / tool · 2026-11-02T02:33:35.137Z

**tool result**
````
1	---
2	name: config-gate-patterns
3	description: Recurring weaknesses in env-var gates of the Zlayt app (bind host read from env not the listener, record/live env toggles, label vs behaviour when ENABLE_LIVE is set without a key); where to probe first
4	metadata:
5	  type: project
6	---
7	
8	Pattern 1: a gate that reads an env var instead of the thing it protects. T-053 r2: `create_app` refuses `ZLAYT_MODE=local` unless `HOST` is loopback (api.py:93-94), but `uvicorn app.main:create --factory --host 0.0.0.0` with HOST unset serves `/api/cases` on the LAN (verified: 200 from a non-loopback address). The `python -m app.main` path is safe because it passes the same env HOST to uvicorn. Fix shape: check the peer address per request (`request.client.host`) in local mode, not the configured host.
9	
10	Pattern 2: a second env toggle that opens the same switch. `RECORD_FIXTURES=1` sets `_record_ok` through `record_context` and bypasses the ENABLE_LIVE check on the dev eval path (132 live stub calls in run_case). It is unreachable from the server today. Re-check whenever a new caller of `record_context`, `record_fragment_context` or `judge_summary` appears in app/backend/.
11	
12	Pattern 3: the label disagrees with the behaviour. `ENABLE_LIVE=1` without a key makes `/api/health` report `backend: anthropic-api` while `demo_mode: true`, because `backend_name()` does not check the key that `live_enabled()` checks. No live call happens (fail closed), but the audit rows and the health label are wrong.
13	
14	Pattern 4: a spec amendment that lives only in the card note. Local-mode library admission (T-053 decision 3) is not in memory/ORCHESTRATOR_DECISIONS.md; D-020 and R-CO-4 still say demo accepts only recorded hashes. Under D.2 that is a blocker if not amended before the gate.
15	
16	**Why:** these are the four ways the T-053 gates were weakened or left inconsistent in rounds 1-2. The round-1 demo blocker (provider.py had no ENABLE_LIVE check) was of the same kind as pattern 1.
17	**How to apply:** for any card that adds an env var, a launch path, or a second caller of record or live code, check (a) what the gate reads versus what it protects, (b) every env toggle that can reach the same switch, (c) that health and audit labels match the backend that ran, and (d) that the spec text, not just the card note, carries the decision. Probe with a counting stub and a blocked socket, and launch through every documented entry point.
18	
19	Related: [[demo-live-gate]], [[round2-review-workflow]]
20	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:33:35.373Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md"
}
````

### User / tool · 2026-11-02T02:33:35.379Z

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
20	Persona scope: if a brief asks security-reviewer to write a record under another persona's name, do not write it. Report the facts and say that persona needs its own run.
21	
22	**Why:** T-034 r2 (first `$()` echo blocked, HEAD changed between pytest and grep). T-040 r2 (four HEAD moves, a live server that predated HEAD, a dirty tree producing a flaky result). T-053 r2 (six HEAD moves, an append-only review file with one wrong count, and a probe bug that made every local request look blocked).
23	**How to apply:** at the start of each round-2 review, record the HEAD sha and the server start time, pin an archive, probe through a file, and proofread the review before the first Write.
24	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:33:35.592Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/project_demo_live_gate.md"
}
````

### User / tool · 2026-11-02T02:33:35.599Z

**tool result**
````
1	---
2	name: demo-live-gate
3	description: Status of the demo live-call gate in provider.py (T-053 r1 blocker fixed in 02f9939, verified r2 at e83eb54); residual env-var paths to recheck on any card touching LLM_BACKEND, ENABLE_LIVE, RECORD_FIXTURES or runs
4	metadata:
5	  type: project
6	---
7	
8	T-053 r1 (c61e84f): `provider.complete_with_meta` sent `claude-cli` and `anthropic-api` straight to the SDK with no ENABLE_LIVE or demo check. Fixed in 02f9939 by `provider.backend_name()` (provider.py:23-30): returns 'fixture' unless ENABLE_LIVE=1 or `_record_ok` (set only by record_context).
9	
10	T-053 r2 (pinned e83eb54, archive artifacts/review-evidence/T-053-r2/head_e83eb54): with LLM_BACKEND=anthropic-api, dummy key, ENABLE_LIVE unset, the provider call, API sample run and RECORD_FIXTURES=1 API run all showed 0 SDK constructor/create calls and 0 socket attempts. Closed for the server path.
11	
12	Residuals (all minor in r2):
13	- ENABLE_LIVE=1 with no key: health says backend anthropic-api, demo_mode true; runs fail BACKEND_UNAVAILABLE (fail closed, label wrong).
14	- RECORD_FIXTURES=1 without ENABLE_LIVE: dev path `pipeline.run_case` makes live calls (132 stub events). Server path does not reach it (judge_summary only from app/llm/record.py).
15	
16	**Why:** D-008 says live needs an explicit ENABLE_LIVE opt-in; spec DECISIONS.md:163 says demo uses fixtures. The gate lives in provider.py, not only in the API layer, so check provider first.
17	
18	**How to apply:** on any card touching runs, library loading, pasted text, LLM_BACKEND, ENABLE_LIVE or RECORD_FIXTURES, re-run the stub probe (counting `anthropic.Anthropic` ctor and `messages.create`, socket connect blocked) on the pinned commit. Note the installed SDK (anthropic 2.3.0) lacks the `temperature` kwarg the backend passes, so use a stub, not a real key.
19	
20	Related: [[round2-review-workflow]], [[config-gate-patterns]]
21	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:33:37.607Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log --oneline -n 8 && git show --stat 08764e7 | head -40 && python3 tools/board.py show T-053 | head -80",
 "description": "Show HEAD, recent log, commit 08764e7 stat, and T-053 card"
}
````

### User / tool · 2026-11-02T02:33:37.800Z

**tool result**
````
08764e7
08764e7 fix(backend): local mode refuses non-loopback peers by address (T-053 F1, D-036)
fa8a36e docs: D-036 amends D-020 for local-mode library packets (T-053 r2 F2)
636a042 feat(frontend): draft treatment paragraph panel with citations, accept/dismiss (T-059 UI)
31070c3 chore(backend): re-record fixtures for D-028 prompts, record library packets (T-037/T-053)
bee1844 feat(evals): score unsplit_paste (D-031) in evals.run; report on recorded fixtures (T-057 minor)
d6ea199 test(golden): D-035 patient_report only on explicit Patient/Pt clauses (sample E1, case_06 E3)
d0c9cdb test(backend): month May is not the modal hedge (T-030 follow-up)
a27b358 feat(backend): D-035 clause-level patient_report, no speaker lists (T-061 r3)
commit 08764e725280366af9031335a2bf9bcdfc655661
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:33:16 2026 -0600

    fix(backend): local mode refuses non-loopback peers by address (T-053 F1, D-036)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/api.py            | 16 +++++++++++++++-
 tests/unit/test_api_routes.py | 16 +++++++++++++++-
 2 files changed, 30 insertions(+), 2 deletions(-)
---
id: "T-053"
title: "Multi-case: case list + switcher (local/dev mode only), library loader"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: ["T-040", "T-041"]
created_by: "orchestrator"
created_at: "2026-11-02T02:06:39Z"
updated_at: "2026-11-02T02:33:29Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:32:08Z"
rounds: 2
commits: ["2c2eb1f", "996f9b4", "02f9939", "08764e7"]
reviews:
  - {"persona": "security-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-053-security.md", "at": "2026-11-02T02:21:00Z"}
  - {"persona": "security-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-053-security-r2.md", "at": "2026-11-02T02:31:45Z"}
ac:
  - {"n": 1, "text": "GET /api/cases lists cases only in local mode; 404 in demo/public mode (test)", "done": true, "evidence": "tests/unit/test_api_routes.py::test_local_mode_refuses_non_loopback_peer_by_address: 403 for 192.168.1.5/10.x/<redacted-private>x/0.0.0.0, 200 for 127.x, ::1, ::ffff:127.0.0.1; unit suite 896 passed"}
  - {"n": 2, "text": "UI case switcher in local mode; library cases loadable in one click; cases isolated (T-050)", "done": true, "evidence": "Playwright vs local-mode server (ZLAYT_MODE=local, port 7871): switcher hidden on demo server (GET /api/cases 404), shown in local mode; library case loads and runs with one keyboard Enter; list opens cases; accepted flag in case 1 not present in case 2 and restored on switching back; 375 px no horizontal scroll; no console errors. Note: fixture backend has no recordings for library texts so their entries land in the could-not-verify tray (flags and amounts still show)"}
  - {"n": 3, "text": "E2E: two cases reviewed side by side, decisions do not leak between cases", "done": true, "evidence": "moved to T-045 AC (two library cases side by side, no leakage E2E); API-level isolation test in tests/unit/test_api_routes.py"}
---
## Description
D-031 + D-008: case list exists only when ZLAYT_MODE=local; public demo stays token-only. Loader seeds evals/library cases.

## Notes (append-only, newest last)
- 2026-11-02T02:11:17Z orchestrator: assigned: backend-3
- 2026-11-02T02:11:36Z backend: claimed
- 2026-11-02T02:12:32Z backend: AC 1 checked: test_api_routes::test_case_list_and_library_exist_only_in_local_mode (404 in demo, list+library+library load in local)
- 2026-11-02T02:12:33Z backend: API done: GET /api/cases, GET /api/library, POST /api/cases {library:id} (all ZLAYT_MODE=local only; 404 otherwise); library loader reads evals/library/*.txt (+ .expected.json name/description), falls back to evals/golden until T-052 lands. In local mode library texts pass the demo gate. AC2 (UI switcher) is frontend: needs a card; AC3 browser E2E is qa. api.md updated (audit both shapes + these routes). NB: another agent is editing api.py concurrently (PDF upload make_case); I merged around it.
- 2026-11-02T02:12:39Z backend: moved in_progress -> in_review: AC2 UI switcher is frontend, AC3 browser E2E is qa; API halves checked
- 2026-11-02T02:12:46Z orchestrator: review dispatched: security (haiku)
- 2026-11-02T02:14:58Z frontend: AC 2 checked: Playwright vs local-mode server (ZLAYT_MODE=local, port 7871): switcher hidden on demo server (GET /api/cases 404), shown in local mode; library case loads and runs with one keyboard Enter; list opens cases; accepted flag in case 1 not present in case 2 and restored on switching back; 375 px no horizontal scroll; no console errors. Note: fixture backend has no recordings for library texts so their entries land in the could-not-verify tray (flags and amounts still show)
- 2026-11-02T02:14:58Z frontend: AC2 UI done: app/frontend/switcher.js (+ .cs-* styles in review.css, script tag in index.html). Local mode detected by GET /api/cases 200 vs 404; lists cases and /api/library; one click POST /cases {library:id} then run. textContent only, buttons keyboard reachable. AC3 (two cases side by side E2E) still qa.
- 2026-11-02T02:15:28Z orchestrator: AC 3 checked: moved to T-045 AC (two library cases side by side, no leakage E2E); API-level isolation test in tests/unit/test_api_routes.py
- 2026-11-02T02:15:28Z orchestrator: Follow-up after T-052 review: record claude-cli fixtures for evals/library packets (python -m app.llm.record) so library cases verify in fixture mode.
- 2026-11-02T02:21:00Z orchestrator: review security-reviewer (claude-haiku-5-5): fail — reviews/T-053-security.md; round 1; findings:
    - [blocker] Demo mode sends live Anthropic SDK calls when LLM_BACKEND=anthropic-api and a key is set, with ENABLE_LIVE unset (pre-existing gate hole; T-053 library route reaches it too) — fix: In app/llm/provider.py complete_with_meta, refuse claude-cli and anthropic-api unless ENABLE_LIVE=1 and the key (or claude CLI) is present, raising LLMError('BACKEND_UNAVAILABLE live not enabled') before
    - [major] Local demo mode now admits seven unrecorded library texts through the demo gate; this conflicts with D-020/R-CO-4 wording and needs a ruling — fix: Chris rules on whether D-031 amends D-020 for local mode. If yes, amend D-020 in writing and require that library texts run only on recorded fixtures and never on a live backend (finding 1). If no, admit only texts whose hash is in app.st
    - [major] Local-mode case list hands every case token to any caller that can reach the server; the bind address is configurable — fix: Refuse to start when ZLAYT_MODE=local and HOST is not 127.0.0.1 or ::1 (or require an explicit ZLAYT_LOCAL_ALLOW_LAN=1 acknowledgement). Keep the list shape unchanged.
    - [minor] Live backend cannot be pinned or reproduced: no requirements or lock file, and the installed anthropic SDK rejects the kwarg the backend passes — fix: Add requirements.txt with == pins for the SDK version the code targets, add pip-audit to a make test target, and add a unit test that inspects the pinned SDK's messages.create signature.
- 2026-11-02T02:21:00Z orchestrator: assigned: backend-3
- 2026-11-02T02:21:00Z orchestrator: Decisions for the fix: (1) demo mode ALWAYS uses the fixture backend regardless of LLM_BACKEND/key; live calls only when ENABLE_LIVE=1 and not demo (D-008/D-020). (2) ZLAYT_MODE=local refuses to start unless HOST is loopback (127.0.0.1/::1/localhost) — protects the case list and token exposure. (3) Library texts are admitted only in local mode (dev), never in public demo.
- 2026-11-02T02:22:16Z backend: claimed
- 2026-11-02T02:22:17Z backend: security r1 fixes: (1) provider.backend_name() returns 'fixture' unless ENABLE_LIVE=1 (or an explicit record_context for dev recording), whatever LLM_BACKEND/key say; /health and audit rows show the real backend; test_demo_never_reaches_a_live_backend (subprocess and SDK patched to explode) + test_demo_health_reports_fixture. (2) create_app refuses ZLAYT_MODE=local unless HOST is 127.0.0.1/::1/localhost (test, 5 hosts). (3) Library texts admitted only in local mode (test with a tmp library: 409 in public, 201 in local). Tests that drive claude-cli through the provider now set ENABLE_LIVE=1. Also allowed case_extras.py (batch accept, someone else's) in the review-writer grep test. Not done: pinned requirements.txt / pip-audit (minor) - no owner yet (release?).
- 2026-11-02T02:22:17Z backend: moved in_progress -> in_review
- 2026-11-02T02:22:25Z orchestrator: review dispatched: security haiku r2
- 2026-11-02T02:31:06Z backend: Re-record (commit 31070c3): golden sample+case_01..09, judge lines (55) and all 7 evals/library packets re-recorded with claude-cli (recorder now accepts evals/library; live recording needs ENABLE_LIVE=1 since the T-053 fixture-by-default rule). Replay on fixture backend: 0 FixtureMiss and 0 judge failures on sample, case_01..09, lib02..07; ONE exception: case_lib01 record 3 extract fails live on all attempts because the model reasons aloud and emits two JSON objects (INVALID_JSON); shows as LLM_FAILED_AFTER_RETRIES. Fix = harden extract_v1 ('your whole reply is one JSON object'), which re-records every extract call and rebuilds curated; not done, say if wanted. Eval evals/reports/20261102T023039Z.md: grounding 1.0, entry_recall 0.982, amount_recall 1.0, halluc catch 1.0 (40/40), flag precision/recall 1.0 all four types, must_not hits 0; ship_bar false only for live-only metrics (fixture backend).
- 2026-11-02T02:31:45Z orchestrator: review security-reviewer (claude-haiku-5-5): changes — reviews/T-053-security-r2.md; round 2; findings:
    - [major] Local-mode loopback refusal reads the HOST env var, not the bind address: uvicorn --host 0.0.0.0 exposes the case list — fix: Enforce the rule on the peer, not the configured host: in local mode, return 404 for any /api request whose request.client.host is not a loopback address (127.0.0.1, ::1). Keep the startup check as well. Document that local mode is launched with python -m app.
    - [major] Library texts admitted in local demo mode with no written amendment of D-020 / R-CO-4 (carried from round 1) — fix: Chris rules. If yes, add a dated amendment to D-020 and R-CO-4 scoped to ZLAYT_MODE=local, and keep library texts on recorded fixtures only. If no, admit only texts whose hash is in app.state.recorded until T-052 records library fixtures.
    - [minor] ENABLE_LIVE=1 without a key: health reports anthropic-api while demo_mode is true; every run fails with BACKEND_UNAVAILABLE — fix: In provider.backend_name, return 'fixture' unless ENABLE_LIVE=1 and the backend has its credential (ANTHROPIC_API_KEY for anthropic-api; claude CLI present for claude-cli), matching live_enabled().
    - [minor] RECORD_FIXTURES=1 alone opens live SDK calls on the dev eval path (not reachable from the server) — fix: In record_context and record_fragment_context, require ENABLE_LIVE=1 before setting _record_ok (record mode then needs both env vars), or narrow the docstring to say which entry points can record.
    - [minor] Pinned anthropic SDK (2.3.0) cannot accept the temperature kwarg the live backend passes; pip-audit not run; no make target — fix: Pin an SDK release whose Messages.create accepts temperature, verify the live path with a stub, install pip-audit into the venv and record 'pip-audit -r requirements.txt' output, and add a Makefile test target or a documented check command.
- 2026-11-02T02:32:08Z backend: claimed
- 2026-11-02T02:33:22Z backend: AC 1 checked: tests/unit/test_api_routes.py::test_local_mode_refuses_non_loopback_peer_by_address: 403 for 192.168.1.5/10.x/<redacted-private>x/0.0.0.0, 200 for 127.x, ::1, ::ffff:127.0.0.1; unit suite 896 passed
- 2026-11-02T02:33:22Z backend: Round 3 fix for security r2 F1 (D-036): app/backend/api.py middleware returns 403 {error.code=forbidden} when ZLAYT_MODE=local and request.client.host is not loopback; HOST startup check kept. Test env fixture now uses a loopback client. Commit 08764e7. Unit suite: 896 passed. F2 resolved by D-036 (no change).
- 2026-11-02T02:33:22Z backend: moved in_progress -> in_review
- 2026-11-02T02:33:29Z orchestrator: review dispatched: security-reviewer

## Handoff
What changed: local mode now gates by peer address (api.py middleware + is_loopback_peer), 403 JSON for non-loopback, works behind tailscale serve (loopback peer). How verified: tests/unit/test_api_routes.py::test_local_mode_refuses_non_loopback_peer_by_address; python -m pytest tests/unit 896 passed. Left: nothing for F1; F2 closed by D-036. Surprised: TestClient default peer is 'testclient', so local-mode tests needed an explicit loopback client.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:33:38.262Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-020\\|D-036\" memory/ORCHESTRATOR_DECISIONS.md; echo ---; grep -n \"R-CO-4\" spec/REQUIREMENTS.md; echo ---; date; lsof -iTCP -sTCP:LISTEN -nP 2>/dev/null | grep -E \"Python|uvicorn\" | head",
 "description": "Grep D-020, D-036, R-CO-4 and check listeners"
}
````

### User / tool · 2026-11-02T02:33:38.464Z

**tool result**
````
28:| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
44:| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
---
138:| R-CO-4 | **Runs from a link or from the repo in under 5 minutes.** The public link works without a key: public deployment is demo-only by default (D-008), replaying the cached sample run through the real pipeline code (A-002). In demo mode `POST /api/cases` accepts only text whose normalized hash equals a recorded fixture; anything else is rejected and not stored (D-020). Local mode (`ZLAYT_MODE=local`, loopback only) also admits the synthetic `evals/library` packets by exact hash (D-036). | `tools/install_test.sh`: clean clone to first screen with the sample loaded < 300 s. The public link opens with no login. | INST + PR (installer-reviewer) |
151:| R-SU-1 | Prototype link or repo with run instructions. README has a timed run path. | See R-CO-4. | INST |
331:Other gates (not ship-bar numbers, still required): `python tools/check_secrets.py` clean; `tools/install_test.sh` under 5 minutes (R-CO-4).
345:| A-001 / A-002 | Dev runs on `claude-cli`; reviewers get demo mode with cached sample output and no key. | R-CO-4, R-CO-6 |
---
Sun Nov  1 20:33:38 CST 2026
Python      824 arsis   10u  IPv4 0xd89fda7756feeb64      0t0  TCP 127.0.0.1:8000 (LISTEN)
Python    38450 arsis    3u  IPv4 0xe3e90fe2e5c7d085      0t0  TCP 127.0.0.1:7777 (LISTEN)
Python    68574 arsis    3u  IPv4 0x71132eb8f1361cf1      0t0  TCP 127.0.0.1:5173 (LISTEN)
Python    68578 arsis    3u  IPv4 0x71132eb8f1361cf1      0t0  TCP 127.0.0.1:5173 (LISTEN)
Python    71204 arsis    3u  IPv4 0xfe895c99ddbd0cc6      0t0  TCP 127.0.0.1:8787 (LISTEN)
Python    79764 arsis    9u  IPv4 0x660f786af1e0eb3a      0t0  TCP 127.0.0.1:7871 (LISTEN)
Python    81950 arsis    9u  IPv4 0x8356abfce73440f5      0t0  TCP 127.0.0.1:7860 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:33:44.765Z

**tool call — Bash**
````
{
 "command": "git show 08764e7 -- app/backend/api.py tests/unit/test_api_routes.py && echo ==== && git show --stat fa8a36e | head -20 && echo ==== && grep -n \"loopback\\|ZLAYT_MODE\\|HOST\\|client.host\\|forwarded\\|proxy\" app/backend/api.py app/main.py app/config.py 2>/dev/null",
 "description": "Show commit diffs and loopback/mode gate references"
}
````

### User / tool · 2026-11-02T02:33:44.887Z

**tool result (error)**
````
Exit code 2
commit 08764e725280366af9031335a2bf9bcdfc655661
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:33:16 2026 -0600

    fix(backend): local mode refuses non-loopback peers by address (T-053 F1, D-036)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index 04822d0..376b1b0 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -4,6 +4,7 @@ Demo mode (D-008/D-020): only text whose normalised sha256 is a golden input is
 anything is stored. Never logs record text, tokens or prompts (run uvicorn with access_log off; see app/main.py).
 """
 import hashlib
+import ipaddress
 import asyncio
 import json
 import logging
@@ -77,6 +78,16 @@ def local_mode() -> bool:
     return os.environ.get("ZLAYT_MODE") == "local"
 
 
+def is_loopback_peer(request) -> bool:
+    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
+    host = request.client.host if request.client else None
+    try:
+        ip = ipaddress.ip_address(host)
+    except (TypeError, ValueError):
+        return False
+    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback
+
+
 def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
     db_path = db_path or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")
     os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
@@ -162,7 +173,10 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             finally:
                 c.close()
         try:
-            resp = await call_next(request)
+            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
+                resp = JSONResponse({"error": {"code": "forbidden", "message": "Local mode accepts loopback clients only.", "detail": {}}}, status_code=403)
+            else:
+                resp = await call_next(request)
         except Exception as e:                                                          # last line of defence: standard JSON, no detail
             log.error("unhandled %s", type(e).__name__)
             resp = JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
diff --git a/tests/unit/test_api_routes.py b/tests/unit/test_api_routes.py
index bc5c58a..8a1a141 100644
--- a/tests/unit/test_api_routes.py
+++ b/tests/unit/test_api_routes.py
@@ -18,7 +18,7 @@ def env(tmp_path, monkeypatch):
     monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
     monkeypatch.delenv("ENABLE_LIVE", raising=False)
     db = str(tmp_path / "api.sqlite")
-    return db, TestClient(create_app(db, static_dir=str(tmp_path)))
+    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)
 
 
 def wait_ready(c, tok):
@@ -335,3 +335,17 @@ def test_library_texts_are_admitted_only_in_local_mode(env, tmp_path, monkeypatc
     monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.setenv("HOST", "127.0.0.1")
     assert c.post("/api/cases", json={"library": "lib_case"}).status_code == 201
     assert c.post("/api/cases", json={"text": text}).status_code == 201
+
+
+def test_local_mode_refuses_non_loopback_peer_by_address(tmp_path, monkeypatch):
+    """D-036: peer address, not the HOST env var, gates local mode (covers `uvicorn --host 0.0.0.0`)."""
+    monkeypatch.setenv("LLM_BACKEND", "fixture"); monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.delenv("HOST", raising=False)
+    app = create_app(str(tmp_path / "p.sqlite"), static_dir=str(tmp_path))
+    for peer in ("127.0.0.1", "127.0.0.5", "::1", "::ffff:127.0.0.1"):
+        assert TestClient(app, client=(peer, 5000)).get("/api/cases").status_code == 200, peer
+    for peer in ("192.168.1.5", "10.0.0.2", "<redacted-private>", "0.0.0.0", "testclient"):
+        r = TestClient(app, client=(peer, 5000)).get("/api/cases")
+        assert r.status_code == 403 and r.json()["error"]["code"] == "forbidden", peer
+        assert TestClient(app, client=(peer, 5000)).get("/api/health").status_code == 403
+    monkeypatch.delenv("ZLAYT_MODE")                                    # public build: no peer restriction
+    assert TestClient(app, client=("192.168.1.5", 5000)).get("/api/health").status_code == 200
====
commit fa8a36e38b58665f13d9a338f1a320277e985b4c
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:32:06 2026 -0600

    docs: D-036 amends D-020 for local-mode library packets (T-053 r2 F2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 memory/ORCHESTRATOR_DECISIONS.md | 3 +++
 spec/REQUIREMENTS.md             | 2 +-
 2 files changed, 4 insertions(+), 1 deletion(-)
====
app/main.py:14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
app/backend/api.py:78:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:81:def is_loopback_peer(request) -> bool:
app/backend/api.py:82:    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
app/backend/api.py:83:    host = request.client.host if request.client else None
app/backend/api.py:88:    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback
app/backend/api.py:104:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
app/backend/api.py:105:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
app/backend/api.py:176:            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
app/backend/api.py:177:                resp = JSONResponse({"error": {"code": "forbidden", "message": "Local mode accepts loopback clients only.", "detail": {}}}, status_code=403)
app/backend/api.py:504:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:33:48.347Z

**tool call — Bash**
````
{
 "command": "sed -n 95,200p app/backend/api.py",
 "description": "Read middleware and local-mode gate in api.py"
}
````

### User / tool · 2026-11-02T02:33:48.422Z

**tool result**
````
    app.state.db_path = db_path
    app.state.recorded = recorded_hashes()

    def allowed_hashes():
        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
    runs = {}
    DB.connect(db_path).close()
    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
    purged = {"at": 0.0}

    # -------------------------------------------------- config (read per call so tests can monkeypatch env)
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
        return DB.connect(app.state.db_path)

    def make_call(c, cid):
        if call_factory:
            return call_factory(c, cid)
        from app.llm import audited
        return audited.make_call(c, cid)

    def pipeline_mod():
        if pipeline is not None:
            return pipeline
        from app.backend import pipeline as PL
        return PL

    def get_case(c, token):
        case = DB.get_case(c, token)
        if case is None:
            raise ApiError(404, "not_found", "No such case.")
        return case

    # -------------------------------------------------- errors / headers
    @app.exception_handler(ApiError)
    async def _api_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(review.ReviewError)
    async def _review_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(_, e):
        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
        return JSONResponse({"error": {"code": code, "message": code.replace("_", " "), "detail": {}}}, status_code=e.status_code)

    @app.exception_handler(Exception)
    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log
        log.error("unhandled %s", type(e).__name__)
        return JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)

    @app.exception_handler(RequestValidationError)
    async def _validation(_, e):
        return JSONResponse({"error": {"code": "bad_request", "message": "Malformed request.", "detail": {}}}, status_code=400)

    @app.middleware("http")
    async def _headers(request, call_next):
        if request.url.path.startswith("/api") and time.time() - purged["at"] > 60:     # expired cases vanish even with no create
            purged["at"] = time.time()
            c = conn()
            try:
                DB.purge_expired(c, time.time())
            finally:
                c.close()
        try:
            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
                resp = JSONResponse({"error": {"code": "forbidden", "message": "Local mode accepts loopback clients only.", "detail": {}}}, status_code=403)
            else:
                resp = await call_next(request)
        except Exception as e:                                                          # last line of defence: standard JSON, no detail
            log.error("unhandled %s", type(e).__name__)
            resp = JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
        resp.headers["Content-Security-Policy"] = CSP
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api") else resp.headers.get("Cache-Control", "no-cache")
        return resp

    async def body_of(request: Request) -> dict:
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > MAX_BODY_BYTES:
            raise ApiError(413, "input_too_large", "Input is too large.")
        raw = b""
        async for chunk in request.stream():
            raw += chunk
            if len(raw) > MAX_BODY_BYTES:
                raise ApiError(413, "input_too_large", "Input is too large.")
        if not raw:
            return {}
        try:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:33:58.940Z

**tool call — Bash**
````
{
 "command": "python3 -m pytest -q tests/unit/test_api_routes.py 2>&1 | tail -15; echo \"exit=$?\"; echo ---; .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_api_routes.py 2>&1 | tail -5; echo ---; grep -rn -i \"tailscale\\|FORWARDED_ALLOW\\|forwarded-allow\\|proxy-headers\\|--host\" --include=*.md --include=*.sh --include=*.py --include=Makefile --include=*.yml . 2>/dev/null | grep -v \"^./.venv\\|^./node_modules\\|^./artifacts/review-evidence\" | head -30",
 "description": "Run api route unit tests and grep proxy and bind references"
}
````

### User / tool · 2026-11-02T02:34:04.960Z

**tool result**
````
/opt/homebrew/opt/python@3.12/bin/python3.12: No module named pytest
exit=0
---
...............................                                          [100%]
31 passed in 5.21s
---
MASTER_PROMPT.md:71:   via Tailscale           │  kanban · personas · milestones · feed   │
MASTER_PROMPT.md:97:| Board | Markdown cards in `board/cards/*.md` + `tools/board.py` CLI + `tools/board_server.py` web UI | Single system of record. Validated by hook on every write. Exposed with `tailscale serve`. |
MASTER_PROMPT.md:225:- Read-only except inbox/STOP. No auth (tailnet only). Never expose with `tailscale funnel`.
MASTER_PROMPT.md:227:**Exposure:** run the server under `nohup`/`setsid` (or a tmux window if available) so it survives your tool calls; then `tailscale serve --bg --https=443 localhost:7777` (fallback `--http=80` if HTTPS certs aren't provisioned; fallback to LAN IP if `tailscale` is missing — record the gap in NEEDS_CHRIS). Expose the prototype later on `--https=8443 localhost:7860`. Write all URLs to `docs/RUNBOOK.md` and `memory/ENVIRONMENT.md`; verify each with `curl`.
MASTER_PROMPT.md:249:2. Board UI reachable on the Tailscale URL from a `curl` on localhost and the activity feed updates live. Inbox form writes a file; `board.py inbox` prints it.
MASTER_PROMPT.md:452:- Tailscale: board on 443 → 7777; app on 8443 → 7860. Never Funnel.
MASTER_PROMPT.md:483:1. `pwd`; verify `python3 --version` (≥3.11), `git`, `node`/`npx`, `jq`, `claude --version` (the CLI must be installed and logged in — it is the development LLM backend, §5.2), `tailscale status`, `tmux` (optional), `pandoc` (optional), `docker` (optional). Write `memory/ENVIRONMENT.md`. **Do not expect `.env` or an API key**; development uses the `claude-cli` backend. If `.env` with `ANTHROPIC_API_KEY` appears later, use the `anthropic-api` backend for a cross-check eval run and note it in `STATE.md`. You may be running inside the Claude Desktop app's Code tab rather than a terminal; nothing changes except: write `.claude/launch.json` with `"autoVerify": false` and URL-only preview entries for the board (`http://localhost:7777`) and the app (`http://localhost:7860`) so Chris's Browser pane can show them without Desktop starting servers, and never rely on terminal-only UI (the teammate panel) for anything the board already shows.
MASTER_PROMPT.md:486:4. Start the board server detached; `tailscale serve --bg`; write `docs/RUNBOOK.md` with URLs; verify with `curl`.
MASTER_PROMPT.md:738:- Tailscale serve: https://tailscale.com/kb/1242/tailscale-serve
artifacts/review-evidence/T-053-r2-probe.py:213:    """Bypass check: the same gate runs inside create_app, which reads HOST from the environment, not from uvicorn's --host flag."""
artifacts/review-evidence/T-053-r2-probe.py:214:    print("PART3b uvicorn CLI with --host 0.0.0.0 (HOST env unset, ZLAYT_MODE=local)")
artifacts/review-evidence/T-053-r2-probe.py:222:    p = subprocess.Popen([os.path.join(VENV_BIN, "uvicorn"), "app.main:create", "--factory", "--host", "0.0.0.0", "--port", "7972", "--log-level", "warning"],
artifacts/review-evidence/T-057-staff-engineer-r2/tree/MASTER_PROMPT.md:71:   via Tailscale           │  kanban · personas · milestones · feed   │
artifacts/review-evidence/T-057-staff-engineer-r2/tree/MASTER_PROMPT.md:97:| Board | Markdown cards in `board/cards/*.md` + `tools/board.py` CLI + `tools/board_server.py` web UI | Single system of record. Validated by hook on every write. Exposed with `tailscale serve`. |
artifacts/review-evidence/T-057-staff-engineer-r2/tree/MASTER_PROMPT.md:225:- Read-only except inbox/STOP. No auth (tailnet only). Never expose with `tailscale funnel`.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/MASTER_PROMPT.md:227:**Exposure:** run the server under `nohup`/`setsid` (or a tmux window if available) so it survives your tool calls; then `tailscale serve --bg --https=443 localhost:7777` (fallback `--http=80` if HTTPS certs aren't provisioned; fallback to LAN IP if `tailscale` is missing — record the gap in NEEDS_CHRIS). Expose the prototype later on `--https=8443 localhost:7860`. Write all URLs to `docs/RUNBOOK.md` and `memory/ENVIRONMENT.md`; verify each with `curl`.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/MASTER_PROMPT.md:249:2. Board UI reachable on the Tailscale URL from a `curl` on localhost and the activity feed updates live. Inbox form writes a file; `board.py inbox` prints it.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/MASTER_PROMPT.md:452:- Tailscale: board on 443 → 7777; app on 8443 → 7860. Never Funnel.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/MASTER_PROMPT.md:483:1. `pwd`; verify `python3 --version` (≥3.11), `git`, `node`/`npx`, `jq`, `claude --version` (the CLI must be installed and logged in — it is the development LLM backend, §5.2), `tailscale status`, `tmux` (optional), `pandoc` (optional), `docker` (optional). Write `memory/ENVIRONMENT.md`. **Do not expect `.env` or an API key**; development uses the `claude-cli` backend. If `.env` with `ANTHROPIC_API_KEY` appears later, use the `anthropic-api` backend for a cross-check eval run and note it in `STATE.md`. You may be running inside the Claude Desktop app's Code tab rather than a terminal; nothing changes except: write `.claude/launch.json` with `"autoVerify": false` and URL-only preview entries for the board (`http://localhost:7777`) and the app (`http://localhost:7860`) so Chris's Browser pane can show them without Desktop starting servers, and never rely on terminal-only UI (the teammate panel) for anything the board already shows.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/MASTER_PROMPT.md:486:4. Start the board server detached; `tailscale serve --bg`; write `docs/RUNBOOK.md` with URLs; verify with `curl`.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/MASTER_PROMPT.md:738:- Tailscale serve: https://tailscale.com/kb/1242/tailscale-serve
artifacts/review-evidence/T-057-staff-engineer-r2/tree/tools/board_server.py:6:Tailnet-only exposure via `tailscale serve` (never Funnel). No auth by design.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/tools/board_server.py:423:    ap.add_argument("--host", default="127.0.0.1")
artifacts/review-evidence/T-057-staff-engineer-r2/tree/memory/ENVIRONMENT.md:13:| tailscale | installed; node `<device>` <redacted-private> | Chris's phone `<device>` on tailnet |
artifacts/review-evidence/T-057-staff-engineer-r2/tree/memory/LESSONS.md:7:- 2026-11-02T00:15:25Z **orchestrator**: tailscale serve --https=443 silently replaced an existing mapping on Chris's tailnet (443 -> 127.0.0.1:4173). Restored it; board now on :7777, app will use :7860. Rule: run 'tailscale serve status' before any serve command and never reuse an occupied port.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/memory/PROGRESS.md:12:- 2026-11-02T00:22Z orchestrator: Decision: started M1 workers (researcher x2, architect, writer, qa) before the m0 tag because M1 is research/spec, not product code; M0 Tier-1 reviews running in parallel. Lessons logged: git-guard heredoc/quoted text; tailscale 443 clobber (restored); agent defs not loaded mid-session.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/memory/DECISIONS.md:48:- Context: the contract (§10) maps the board to 443 and the app to 8443 on Tailscale. Chris's tailnet already maps 443 to 127.0.0.1:4173 and 8443 to 127.0.0.1:8787.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/memory/DECISIONS.md:49:- Decision: use separate serve HTTPS ports that match the local ports: `tailscale serve --https=7777 → http://127.0.0.1:7777` for the board (verified: the https URL returns 200, the http URL returns 400) and `--https=7860 → http://127.0.0.1:7860` for the app. Never overwrite or reset an existing `tailscale serve` mapping. Never use Funnel.
artifacts/review-evidence/T-057-staff-engineer-r2/tree/board/cards/T-005.md:50:    - [major] ADR-000e describes a setup that wasn't built, and its rejected alternative is the one in use — fix: Architect: rewrite the ADR-000e Decision and Consequences to match what was built: 'serve --https=7777 and --https=7860, TLS from tailscale serve; never reuse an occupied serve port (run `tailscale serve status` first)'. Move the plain-http option into Alternatives. Mention that 10000 
artifacts/review-evidence/T-057-staff-engineer-r2/tree/board/cards/T-002.md:3:title: "Board web UI (tools/board_server.py) + Tailscale serve"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:34:09.397Z

**tool call — Bash**
````
{
 "command": "python3 -m pytest -q tests/unit/test_api_routes.py >/dev/null 2>&1; echo \"system python3 pytest exit=$?\"; .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_api_routes.py; echo \"venv pytest exit=$?\"; echo ---; grep -rn \"ZLAYT_MODE\\|local mode\\|tailscale\" docs/RUNBOOK.md memory/ENVIRONMENT.md memory/DECISIONS.md memory/ORCHESTRATOR_DECISIONS.md 2>/dev/null | head -30; echo ---; grep -rn \"D-031\\|D-008\" memory/ORCHESTRATOR_DECISIONS.md | head -8",
 "description": "Rerun unit tests with real exit codes; grep runbook for local-mode exposure"
}
````

### User / tool · 2026-11-02T02:34:15.590Z

**tool result**
````
system python3 pytest exit=1
...............................                                          [100%]
31 passed in 5.63s
venv pytest exit=0
---
docs/RUNBOOK.md:32:5. Tailnet exposure persists across restarts (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.
memory/DECISIONS.md:49:- Decision: use separate serve HTTPS ports that match the local ports: `tailscale serve --https=7777 → http://127.0.0.1:7777` for the board (verified: the https URL returns 200, the http URL returns 400) and `--https=7860 → http://127.0.0.1:7860` for the app. Never overwrite or reset an existing `tailscale serve` mapping. Never use Funnel.
memory/ORCHESTRATOR_DECISIONS.md:39:| D-031 | **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_SPLIT); 'not a duplicate' split; full audit view (local mode); exhibit/Bates numbering as a per-case config; draft treatment paragraph in firm voice (stretch from spec; every sentence grounded + judged, internal until accepted). **Still cut, with reason:** charge reclassification (a rate must never become a charge — safety), auth/roles (needs an identity provider), per-user learning (needs its own evals), numeric confidence (unverifiable precision), non-English/handwriting, date-convention inference (silent-guess risk), OCR. | Chris asked; each reinstated item keeps the ladder and grounding rules. | Chris inbox 02:05Z |
memory/ORCHESTRATOR_DECISIONS.md:44:| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
memory/ENVIRONMENT.md:13:| tailscale | installed; node `<device>` <redacted-private> | Chris's phone `<device>` on tailnet |
---
memory/ORCHESTRATOR_DECISIONS.md:16:| D-008 | Public deployment is demo-only by default (cached sample run through real pipeline code); live mode needs an explicit env opt-in. No case list; random 128-bit case tokens; spend counter append-only and separate from case data. | Exposure + key abuse risk. NEEDS_CHRIS #7. | T-014 privacy |
memory/ORCHESTRATOR_DECISIONS.md:28:| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
memory/ORCHESTRATOR_DECISIONS.md:39:| D-031 | **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_SPLIT); 'not a duplicate' split; full audit view (local mode); exhibit/Bates numbering as a per-case config; draft treatment paragraph in firm voice (stretch from spec; every sentence grounded + judged, internal until accepted). **Still cut, with reason:** charge reclassification (a rate must never become a charge — safety), auth/roles (needs an identity provider), per-user learning (needs its own evals), numeric confidence (unverifiable precision), non-English/handwriting, date-convention inference (silent-guess risk), OCR. | Chris asked; each reinstated item keeps the ladder and grounding rules. | Chris inbox 02:05Z |
memory/ORCHESTRATOR_DECISIONS.md:44:| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:34:25.928Z

**tool call — Bash**
````
{
 "command": "grep -n \"7860\\|8443\\|serve\" docs/RUNBOOK.md | head; echo ---; sed -n 1,30p app/main.py; echo ---; grep -n \"^def \\|^async def \\|^class \" app/backend/api.py | head -20; echo; ls artifacts/review-evidence | head -50; echo; mkdir -p artifacts/review-evidence/T-053-r3 && echo dir-ok",
 "description": "Check runbook app exposure, main.py entrypoint, and evidence dirs"
}
````

### User / tool · 2026-11-02T02:34:26.044Z

**tool result**
````
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
9:| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |
11:Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
26:2. Board server: `./tools/serve_board.sh` (also installs the native git pre-commit secret scan if missing) (tmux session `zlayt`, window `board`). Check: `curl -s localhost:7777/healthz`.
32:5. Tailnet exposure persists across restarts (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.
---
"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens)."""
import os

import uvicorn

from app.backend.api import create_app

def create():
    """uvicorn app.main:create --factory"""
    return create_app()


if __name__ == "__main__":
    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
---
46:class ApiError(Exception):
52:def digest(text: str) -> str:
56:def recorded_hashes() -> set:
60:def library_cases() -> list:
77:def local_mode() -> bool:
81:def is_loopback_peer(request) -> bool:
91:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:

M0-r2-staff-resolution.md
T-001-exercise-1.txt
T-001-exercise-2.txt
T-001-exercise-3.txt
T-001-r2-readonly-repros.txt
T-001-r3-repro.out.txt
T-001-r3-repro.sh
T-002-curl.txt
T-002-r2-activity-390.png
T-002-r2-board-390.png
T-002-r2-csrf-curl.txt
T-002-r2-inbox-390.png
T-002-r2-milestones-390.png
T-002-r2-personas-390.png
T-002-r2-state-390.png
T-002-r2-xss.json
T-002-r3-404.py
T-002-r3-activity-390.png
T-002-r3-board-390.png
T-002-r3-inbox-390.png
T-002-r3-milestones-390.png
T-002-r3-personas-390.png
T-002-r3-probe.out.txt
T-002-r3-probe.py
T-002-r3-state-390.png
T-002-r3-ui.out.txt
T-002-r3-ui.py
T-003-git-guard-commit-secret-probe.txt
T-003-git-guard-probe.txt
T-003-other-hooks-probe.txt
T-003-r2-commit-secret-probe.out.txt
T-003-r2-commit-secret-probe.py
T-003-r2-git-guard-results.txt
T-003-r2-probe-board2.out.txt
T-003-r2-probe-board2.py
T-003-r2-probe-corpus.txt
T-003-r2-probe-direct.out.txt
T-003-r2-probe-direct.out2.txt
T-003-r2-probe-direct.py
T-003-r3-probe-board2.out.txt
T-003-r3-probe-corpus.out.txt
T-003-r3-probe-corpus.py
T-003-r3-probe-direct.out.txt
T-003-r3-probe-legit.out.txt
T-003-r3-probe-legit.py
T-003-r3-probe-pwd.out.txt
T-003-r3-probe-pwd.py
T-003-r3-probe-rwg.out.txt
T-003-r3-probe-rwg.py
T-003-r3-probe-targeted.out.txt

dir-ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:34:28.406Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh 2>/dev/null; echo \"---rc=$?\"; grep -rn \"ZLAYT_MODE\" tools/ docs/ README.md 2>/dev/null | head; echo ---; sed -n 1,12p docs/RUNBOOK.md",
 "description": "Read app serve script and check ZLAYT_MODE in tools and docs"
}
````

### User / tool · 2026-11-02T02:34:28.503Z

**tool result**
````
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
---rc=0
---
# RUNBOOK (for Chris)

## URLs
| What | URL | Notes |
|---|---|---|
| Board (tailnet) | https://<redacted-private>:7777 | open on your phone (Tailscale on). Kanban, personas, milestones, activity, inbox, STOP. |
| Board (local) | http://localhost:7777 | also in the Desktop Browser pane (`.claude/launch.json` → "board") |
| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |

Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
We restored those and gave the board and app their own ports so nothing of yours was clobbered.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:35:07.053Z

**tool call — Bash**
````
{
 "command": "ls -la .venv/bin/uvicorn && .venv/bin/python -c \"import uvicorn,fastapi,starlette;print('uvicorn',uvicorn.__version__,'starlette',starlette.__version__)\"; ls -la .env 2>&1 | head -2; grep -rln \"dotenv\\|load_dotenv\" app tools 2>/dev/null | head; for p in 7981 7982 7983 7984 7985; do echo \"port $p listeners: $(lsof -nP -iTCP:$p -sTCP:LISTEN 2>/dev/null | wc -l)\"; done; git rev-parse --short HEAD; git status --short | head -5",
 "description": "Check uvicorn install, .env presence, and probe port availability"
}
````

### User / tool · 2026-11-02T02:35:07.803Z

**tool result**
````
-rwxr-xr-x@ 1 arsis  staff  245 Nov  1 18:03 .venv/bin/uvicorn
uvicorn 0.54.0 starlette 1.10.0
-rw-r--r--  1 arsis  staff  29 Nov  1 17:49 .env
port 7981 listeners:        0
port 7982 listeners:        0
port 7983 listeners:        0
port 7984 listeners:        0
port 7985 listeners:        0
8ec0b25
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/feedback_lexicon_recall_and_negation.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:35:11.820Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log --oneline 08764e7..HEAD && echo \"--- gate files 08764e7..HEAD:\" && git diff --stat 08764e7 HEAD -- app/backend/api.py app/main.py app/llm/provider.py app/llm/backends/anthropic_api.py tests/unit/test_api_routes.py; echo \"diff-exit=$?\"; echo \"--- ignore/track checks:\"; git check-ignore -v .env; git ls-files .env | wc -l; echo \"--- archive pin:\"; rm -rf artifacts/review-evidence/T-053-r3/head_8ec0b25 && mkdir -p artifacts/review-evidence/T-053-r3/head_8ec0b25 && git archive 8ec0b25 | tar -x -C artifacts/review-evidence/T-053-r3/head_8ec0b25 && ls artifacts/review-evidence/T-053-r3/head_8ec0b25/app/backend/api.py && cd artifacts/review-evidence/T-053-r3/head_8ec0b25 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_api_routes.py 2>&1 | tail -3",
 "description": "Pin HEAD via git archive and check gate-file drift"
}
````

### User / tool · 2026-11-02T02:35:18.176Z

**tool result**
````
8ec0b25
8ec0b25 docs: D-037 patient_report chip only on whole-excerpt patient clause (T-061 r3)
--- gate files 08764e7..HEAD:
diff-exit=0
--- ignore/track checks:
.gitignore:25:*.env	.env
       0
--- archive pin:
artifacts/review-evidence/T-053-r3/head_8ec0b25/app/backend/api.py
...............................                                          [100%]
31 passed in 5.58s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:35:26.451Z

**tool call — Bash**
````
{
 "command": "ls board/inbox/ 2>/dev/null | tail -5; grep -il \"library\\|D-036\\|D-020\" board/inbox/* 2>/dev/null | tail -3; ls submission/NEEDS_CHRIS.md 2>/dev/null && grep -n -i \"library\\|D-036\\|D-020\\|tailscale\\|local mode\" submission/NEEDS_CHRIS.md | tail -10",
 "description": "Check inbox and NEEDS_CHRIS for a ruling on library admission"
}
````

### User / tool · 2026-11-02T02:35:26.551Z

**tool result**
````
archive
submission/NEEDS_CHRIS.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:35:43.875Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-r3-probe.py",
 "content": "\"\"\"T-053 round-3 security probe (security-reviewer). Run: .venv/bin/python -I artifacts/review-evidence/T-053-r3-probe.py\n\nPinned code: git archive 8ec0b25 extracted to artifacts/review-evidence/T-053-r3/head_8ec0b25 (fix commit 08764e7 is an ancestor;\ngate files unchanged 08764e7..8ec0b25). Servers run from the pinned copy. Dummy key only. ENABLE_LIVE unset.\nParts:\n  A  uvicorn CLI, --host 0.0.0.0, HOST unset, ZLAYT_MODE=local: 127.0.0.1 peer vs LAN peer, spoofed forwarding headers.\n  B  loopback reverse-proxy simulation (the tailscale-serve-shaped path): plain relay and header-adding relay, LAN client.\n  C  python -m app.main with HOST=0.0.0.0 and ZLAYT_MODE=local: startup refusal still in place.\nPrints status codes and key names only. Never prints tokens or record text.\n\"\"\"\nimport http.client\nimport json\nimport os\nimport socket\nimport subprocess\nimport sys\nimport threading\nimport time\n\nROOT = \"/Users/arsis/zlayt-pm-project\"\nPINNED = os.path.join(ROOT, \"artifacts/review-evidence/T-053-r3/head_8ec0b25\")\nVENV_PY = os.path.join(ROOT, \".venv/bin/python\")\nSCRATCH = \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\"\nDATA = os.path.join(SCRATCH, \"t053r3-data\")\nPORT_A, PORT_B_APP, PORT_B_PLAIN, PORT_B_XFF, PORT_C = 7981, 7982, 7984, 7985, 7983\nDUMMY_KEY = \"dummy-not-a-real-key-r3-probe\"\nFAKE_KEY_ENV = {\"PATH\": os.environ.get(\"PATH\", \"\"), \"HOME\": os.environ.get(\"HOME\", \"\"),\n                \"ZLAYT_MODE\": \"local\", \"LLM_BACKEND\": \"anthropic-api\", \"ANTHROPIC_API_KEY\": DUMMY_KEY,\n                \"DATA_DIR\": DATA, \"PYTHONDONTWRITEBYTECODE\": \"1\"}\n\n\ndef lan_ip():\n    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n    try:\n        s.connect((\"192.0.2.1\", 9))          # UDP connect sends no packet; it only picks the outbound interface address\n        return s.getsockname()[0]\n    finally:\n        s.close()\n\n\ndef wait_port(port, proc, secs=30):\n    end = time.time() + secs\n    while time.time() < end:\n        if proc.poll() is not None:\n            return False\n        try:\n            with socket.create_connection((\"127.0.0.1\", port), timeout=0.5):\n                return True\n        except OSError:\n            time.sleep(0.2)\n    return False\n\n\ndef req(host, port, method, path, body=None, headers=None):\n    conn = http.client.HTTPConnection(host, port, timeout=10)\n    h = {\"Connection\": \"close\"}\n    h.update(headers or {})\n    data = None\n    if body is not None:\n        data = json.dumps(body).encode()\n        h[\"Content-Type\"] = \"application/json\"\n    conn.request(method, path, body=data, headers=h)\n    src = conn.sock.getsockname()[0]\n    r = conn.getresponse()\n    raw = r.read()\n    conn.close()\n    return r.status, src, raw\n\n\ndef summarise(status, raw):\n    keys = \"\"\n    try:\n        j = json.loads(raw)\n        if isinstance(j, dict):\n            keys = sorted(j.keys())\n            if \"error\" in j and isinstance(j[\"error\"], dict):\n                keys = \"error.code=\" + str(j[\"error\"].get(\"code\"))\n    except ValueError:\n        keys = \"non-json body, %d bytes\" % len(raw)\n    return \"%s %s\" % (status, keys)\n\n\ndef start_server(port, host_args, extra_env=None):\n    env = dict(FAKE_KEY_ENV)\n    env.update(extra_env or {})\n    cmd = [os.path.join(os.path.dirname(VENV_PY), \"uvicorn\"), \"app.main:create\", \"--factory\",\n           \"--port\", str(port), \"--log-level\", \"warning\"] + host_args\n    return subprocess.Popen(cmd, cwd=PINNED, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n\n\ndef stop(proc):\n    if proc and proc.poll() is None:\n        proc.terminate()\n        try:\n            proc.wait(10)\n        except subprocess.TimeoutExpired:\n            proc.kill()\n            proc.wait(5)\n\n\ndef listeners(port):\n    out = subprocess.run([\"lsof\", \"-nP\", \"-iTCP:%d\" % port, \"-sTCP:LISTEN\"], capture_output=True, text=True).stdout\n    return len([l for l in out.splitlines() if l.strip()]) - (1 if out.strip() else 0)\n\n\ndef relay(listen_port, backend_port, add_xff=None):\n    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n    srv.bind((\"0.0.0.0\", listen_port))\n    srv.listen(16)\n    srv.settimeout(0.5)\n    stop_evt = threading.Event()\n\n    def handle(c):\n        try:\n            c.settimeout(10)\n            buf = b\"\"\n            while b\"\\r\\n\\r\\n\" not in buf:\n                chunk = c.recv(4096)\n                if not chunk:\n                    break\n                buf += chunk\n            head, _, rest = buf.partition(b\"\\r\\n\\r\\n\")\n            if add_xff:\n                head += b\"\\r\\nX-Forwarded-For: \" + add_xff.encode()\n            up = socket.create_connection((\"127.0.0.1\", backend_port), timeout=10)\n            up.sendall(head + b\"\\r\\n\\r\\n\" + rest)\n            while True:\n                d = up.recv(65536)\n                if not d:\n                    break\n                c.sendall(d)\n            up.close()\n        except OSError:\n            pass\n        finally:\n            c.close()\n\n    def loop():\n        while not stop_evt.is_set():\n            try:\n                c, _ = srv.accept()\n            except socket.timeout:\n                continue\n            except OSError:\n                break\n            threading.Thread(target=handle, args=(c,), daemon=True).start()\n        srv.close()\n\n    threading.Thread(target=loop, daemon=True).start()\n    return stop_evt\n\n\ndef part_a(lan):\n    print(\"PART A uvicorn app.main:create --factory --host 0.0.0.0, HOST unset, ZLAYT_MODE=local\")\n    proc = start_server(PORT_A, [\"--host\", \"0.0.0.0\"])\n    try:\n        print(\"  server up:\", wait_port(PORT_A, proc), \"| pid\", proc.pid)\n        probe_path = subprocess.run([VENV_PY, \"-c\", \"import app.backend.api as a;print(a.__file__)\"],\n                                    cwd=PINNED, capture_output=True, text=True).stdout.strip()\n        print(\"  code under test:\", probe_path)\n        print(\"  listener on 0.0.0.0:%d count (LISTEN lines): %d\" % (PORT_A, listeners(PORT_A)))\n        cases = [\n            (\"loopback GET /api/cases\", \"127.0.0.1\", \"GET\", \"/api/cases\", None, None),\n            (\"loopback GET /api/health\", \"127.0.0.1\", \"GET\", \"/api/health\", None, None),\n            (\"LAN GET /api/cases\", lan, \"GET\", \"/api/cases\", None, None),\n            (\"LAN GET /api/health\", lan, \"GET\", \"/api/health\", None, None),\n            (\"LAN GET /\", lan, \"GET\", \"/\", None, None),\n            (\"LAN POST /api/cases\", lan, \"POST\", \"/api/cases\", {\"library\": \"x\"}, None),\n            (\"LAN GET /api/cases + XFF/XRI/Forwarded=127.0.0.1\", lan, \"GET\", \"/api/cases\", None,\n             {\"X-Forwarded-For\": \"127.0.0.1\", \"X-Real-IP\": \"127.0.0.1\", \"Forwarded\": \"for=127.0.0.1\"}),\n            (\"loopback GET /api/cases + XFF=192.168.1.20 (local proxy case)\", \"127.0.0.1\", \"GET\", \"/api/cases\", None,\n             {\"X-Forwarded-For\": \"192.168.1.20\"}),\n        ]\n        for label, host, method, path, body, hdrs in cases:\n            st, src, raw = req(host, PORT_A, method, path, body, hdrs)\n            print(\"  %-58s src=%-14s -> %s\" % (label, src, summarise(st, raw)))\n        r = subprocess.run([\"lsof\", \"-a\", \"-p\", str(proc.pid), \"-nP\", \"-iTCP\"], capture_output=True, text=True).stdout\n        est = [l for l in r.splitlines() if \"ESTABLISHED\" in l or \"SYN_SENT\" in l]\n        print(\"  server outbound TCP (ESTABLISHED/SYN_SENT) lines after requests: %d\" % len(est))\n        for l in est:\n            print(\"   \", l)\n    finally:\n        stop(proc)\n        time.sleep(0.5)\n        print(\"  server stopped; listener count on %d: %d\" % (PORT_A, listeners(PORT_A)))\n\n\ndef part_b(lan):\n    print(\"PART B loopback reverse-proxy simulation (server bound 127.0.0.1, ZLAYT_MODE=local, HOST unset)\")\n    proc = start_server(PORT_B_APP, [])\n    stops = []\n    try:\n        print(\"  app up on 127.0.0.1:%d:\" % PORT_B_APP, wait_port(PORT_B_APP, proc))\n        stops.append(relay(PORT_B_PLAIN, PORT_B_APP))\n        stops.append(relay(PORT_B_XFF, PORT_B_APP, add_xff=lan))\n        time.sleep(0.5)\n        print(\"  direct LAN GET to app port (no proxy):\", end=\" \")\n        try:\n            st, src, raw = req(lan, PORT_B_APP, \"GET\", \"/api/cases\")\n            print(\"src=%s -> %s\" % (src, summarise(st, raw)))\n        except OSError as e:\n            print(\"connect refused/failed (%s): app not reachable from LAN\" % type(e).__name__)\n        st, src, raw = req(lan, PORT_B_PLAIN, \"GET\", \"/api/cases\")\n        print(\"  LAN GET via plain loopback relay :%d (no header added) src=%s -> %s\" % (PORT_B_PLAIN, src, summarise(st, raw)))\n        st, src, raw = req(lan, PORT_B_XFF, \"GET\", \"/api/cases\")\n        print(\"  LAN GET via loopback relay adding X-Forwarded-For=%s :%d src=%s -> %s\" % (lan, PORT_B_XFF, src, summarise(st, raw)))\n    finally:\n        for s in stops:\n            s.set_result = None\n            s.set()\n        stop(proc)\n        time.sleep(1.0)\n        print(\"  stopped; listener counts %d/%d/%d: %d/%d/%d\" % (PORT_B_APP, PORT_B_PLAIN, PORT_B_XFF,\n              listeners(PORT_B_APP), listeners(PORT_B_PLAIN), listeners(PORT_B_XFF)))\n\n\ndef part_c():\n    print(\"PART C python -m app.main with HOST=0.0.0.0, ZLAYT_MODE=local (startup refusal)\")\n    env = dict(FAKE_KEY_ENV)\n    env.update({\"HOST\": \"0.0.0.0\", \"PORT\": str(PORT_C)})\n    p = subprocess.Popen([VENV_PY, \"-m\", \"app.main\"], cwd=PINNED, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)\n    try:\n        _, err = p.communicate(timeout=60)\n        last = [l for l in err.strip().splitlines() if l.strip()][-1:] if err else []\n        print(\"  exit code:\", p.returncode, \"| stderr last line:\", last[0] if last else \"(none)\")\n    except subprocess.TimeoutExpired:\n        p.kill()\n        print(\"  did not exit within 60 s (started a server?)\")\n    print(\"  listener count on %d: %d\" % (PORT_C, listeners(PORT_C)))\n\n\nif __name__ == \"__main__\":\n    os.makedirs(DATA, exist_ok=True)\n    lan = lan_ip()\n    print(\"LAN address for non-loopback client:\", lan)\n    if lan.startswith(\"127.\") or lan == \"0.0.0.0\":\n        sys.exit(\"no non-loopback interface address\")\n    parts = sys.argv[1:] or [\"A\", \"B\", \"C\"]\n    if \"A\" in parts:\n        part_a(lan)\n    if \"B\" in parts:\n        part_b(lan)\n    if \"C\" in parts:\n        part_c()\n"
}
````

### User / tool · 2026-11-02T02:35:43.968Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-r3-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:35:46.033Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-r3-probe.py",
 "old_string": "        for s in stops:\n            s.set_result = None\n            s.set()",
 "new_string": "        for s in stops:\n            s.set()"
}
````

### User / tool · 2026-11-02T02:35:46.133Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-r3-probe.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:35:47.490Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-053-r3-probe.py A B C 2>&1 | tee artifacts/review-evidence/T-053-r3/out_probe.txt; echo \"probe-exit=${PIPESTATUS[0]}\"",
 "description": "Run round-3 probe parts A, B and C and save output",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:35:51.968Z

**tool result**
````
LAN address for non-loopback client: 192.168.199.106
PART A uvicorn app.main:create --factory --host 0.0.0.0, HOST unset, ZLAYT_MODE=local
  server up: True | pid 85679
  code under test: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-r3/head_8ec0b25/app/backend/api.py
  listener on 0.0.0.0:7981 count (LISTEN lines): 1
  loopback GET /api/cases                                    src=127.0.0.1      -> 200 ['cases']
  loopback GET /api/health                                   src=127.0.0.1      -> 200 ['ai_banner', 'backend', 'banner', 'demo_mode', 'limits', 'live_enabled', 'models', 'ok', 'retention_hours', 'sample_available', 'synthetic_only', 'version']
  LAN GET /api/cases                                         src=192.168.199.106 -> 403 error.code=forbidden
  LAN GET /api/health                                        src=192.168.199.106 -> 403 error.code=forbidden
  LAN GET /                                                  src=192.168.199.106 -> 403 error.code=forbidden
  LAN POST /api/cases                                        src=192.168.199.106 -> 403 error.code=forbidden
  LAN GET /api/cases + XFF/XRI/Forwarded=127.0.0.1           src=192.168.199.106 -> 403 error.code=forbidden
  loopback GET /api/cases + XFF=192.168.1.20 (local proxy case) src=127.0.0.1      -> 403 error.code=forbidden
  server outbound TCP (ESTABLISHED/SYN_SENT) lines after requests: 0
  server stopped; listener count on 7981: 0
PART B loopback reverse-proxy simulation (server bound 127.0.0.1, ZLAYT_MODE=local, HOST unset)
  app up on 127.0.0.1:7982: True
  direct LAN GET to app port (no proxy): connect refused/failed (ConnectionRefusedError): app not reachable from LAN
  LAN GET via plain loopback relay :7984 (no header added) src=192.168.199.106 -> 200 ['cases']
  LAN GET via loopback relay adding X-Forwarded-For=192.168.199.106 :7985 src=192.168.199.106 -> 403 error.code=forbidden
  stopped; listener counts 7982/7984/7985: 0/0/0
PART C python -m app.main with HOST=0.0.0.0, ZLAYT_MODE=local (startup refusal)
  exit code: 1 | stderr last line: RuntimeError: ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost
  listener count on 7983: 0
probe-exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:36:11.483Z

**tool call — Bash**
````
{
 "command": "git diff --quiet e83eb54 8ec0b25 -- app/llm/provider.py app/llm/backends/anthropic_api.py requirements.txt; echo \"r2 minors' files unchanged since e83eb54: exit=$?\"; grep -n \"anthropic\" requirements.txt; cd artifacts/review-evidence/T-053-r3/head_8ec0b25 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"import inspect,anthropic;print('temperature' in inspect.signature(anthropic.resources.Messages.create).parameters, anthropic.__version__)\"; cd /Users/arsis/zlayt-pm-project && grep -n \"temperature\" app/llm/backends/anthropic_api.py | head -3; ls reviews/ | grep T-053",
 "description": "Check r2 minor gate files unchanged and SDK pin status"
}
````

### User / tool · 2026-11-02T02:36:12.241Z

**tool result**
````
r2 minors' files unchanged since e83eb54: exit=0
5:anthropic==2.3.0
False 2.3.0
1:"""anthropic-api backend: Anthropic SDK, temperature 0, schema via a forced tool call. ADR-004. One attempt, no retry."""
26:            model=model, max_tokens=MAX_TOKENS, temperature=0, system=system,
T-053-security-r2.md
T-053-security.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:36:37.051Z

**tool call — Bash**
````
{
 "command": "git show --stat --format='%h %s' 8ec0b25 | head -12; echo ---; git rev-parse --short HEAD; echo ---; sed -n 81,88p app/backend/api.py; echo ---; sed -n 8,9p docs/RUNBOOK.md | cut -c1-160; echo ---; sed -n 84,88p artifacts/review-evidence/T-053-r3-probe.py >/dev/null; grep -n \"Local mode\\|tailscale serve\" board/cards/T-053.md | cut -c1-200",
 "description": "Confirm 8ec0b25 scope and cite gate and runbook lines"
}
````

### User / tool · 2026-11-02T02:36:37.198Z

**tool result**
````
8ec0b25 docs: D-037 patient_report chip only on whole-excerpt patient clause (T-061 r3)

 memory/ORCHESTRATOR_DECISIONS.md | 1 +
 1 file changed, 1 insertion(+)
---
38421cc
---
def is_loopback_peer(request) -> bool:
    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
    host = request.client.host if request.client else None
    try:
        ip = ipaddress.ip_address(host)
    except (TypeError, ValueError):
        return False
    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback
---
| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` 
---
35:- 2026-11-02T02:14:58Z frontend: AC2 UI done: app/frontend/switcher.js (+ .cs-* styles in review.css, script tag in index.html). Local mode detected by GET /api/cases 200 vs 404; lists cases and /a
63:What changed: local mode now gates by peer address (api.py middleware + is_loopback_peer), 403 JSON for non-loopback, works behind tailscale serve (loopback peer). How verified: tests/unit/test_api
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:36:39.567Z

**tool call — Bash**
````
{
 "command": "git log --oneline 08764e7..HEAD | head; echo ---; git diff --stat 08764e7 HEAD -- app/backend/api.py app/main.py app/llm/provider.py app/llm/backends/anthropic_api.py tests/unit/test_api_routes.py requirements.txt; echo \"gate-diff-exit=$?\"; echo ---; git diff --stat 8ec0b25 HEAD | tail -3",
 "description": "Check what moved since the pinned commit"
}
````

### User / tool · 2026-11-02T02:36:39.708Z

**tool result**
````
38421cc memory: record §7.4 debt rows and scope cut 20
8ec0b25 docs: D-037 patient_report chip only on whole-excerpt patient clause (T-061 r3)
---
gate-diff-exit=0
---
 memory/SCOPE_CUTS.md | 12 ++++++++++++
 1 file changed, 12 insertions(+)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:36:50.574Z

**tool call — Bash**
````
{
 "command": "grep -n \"ENABLE_LIVE\\|_record_ok\\|def backend_name\\|ALWAYS\" app/llm/provider.py | head -12; echo ---; grep -n \"_record_ok\\|record_context\\|def _recording\" app/llm/provider.py | head; echo ---; sed -n 176,178p app/backend/api.py | cut -c1-120; echo ---; .venv/bin/pip-audit --version 2>&1 | head -1",
 "description": "Confirm provider.py line references and pip-audit presence"
}
````

### User / tool · 2026-11-02T02:36:50.682Z

**tool result**
````
20:_record_ok = False
23:def backend_name() -> str:
24:    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
25:    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
28:    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
67:    global _record_ok
69:    prev, _record_ok = _record_ok, True
73:        _record_ok = prev
79:    global _record_ok
81:    prev, _record_ok = _record_ok, True
85:        _record_ok = prev
98:        if _recording() and not _record_ok:
---
6:refused unless a `record_context(text)` for text found in evals/golden is active (ADR-004).
20:_record_ok = False
24:    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
28:    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
65:def record_context(source_text: str):
67:    global _record_ok
69:    prev, _record_ok = _record_ok, True
73:        _record_ok = prev
79:    global _record_ok
81:    prev, _record_ok = _record_ok, True
---
            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopb
                resp = JSONResponse({"error": {"code": "forbidden", "message": "Local mode accepts loopback clients only
            else:
---
/bin/bash: .venv/bin/pip-audit: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:20.384Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-053-security-r3.md",
 "content": "# T-053 security review, round 3 (security-reviewer, Tomas Rivas lens)\n\nPinned code: `git archive 8ec0b25` extracted to `artifacts/review-evidence/T-053-r3/head_8ec0b25`. HEAD was 08764e7 at my first check, 8ec0b25 at the pin (docs only, one line in `memory/ORCHESTRATOR_DECISIONS.md`), and 38421cc when I wrote this (`memory/SCOPE_CUTS.md` only). `git diff --stat 08764e7 HEAD -- app/backend/api.py app/main.py app/llm/provider.py app/llm/backends/anthropic_api.py tests/unit/test_api_routes.py requirements.txt` printed nothing (exit 0), so the fix commit and everything after it leave the gate files unchanged.\n\nModel note: the brief expected `claude-sonnet-5-5`. This session runs as Haiku 5.5 (model id `claude-haiku-5-5`), so that id is recorded.\n\nVerdict: **changes**. Both round-2 majors are closed as written.\n\n- F1 (uvicorn `--host 0.0.0.0` with `HOST` unset) is closed. A LAN peer gets 403 on every path, a loopback peer gets 200, and the server opened no outbound connections. Spoofed forwarding headers from the LAN are ignored.\n- F2 (library texts in local demo mode, no amendment) is closed on paper. D-036 amends D-020 and R-CO-4 cites it. The basis question is in `questions_for_chris`.\n\nThe peer-address rule does not give loopback-only behaviour once a loopback reverse proxy is in front of the app. The project's own tailnet exposure is a proxy shape. That is a new **major** (finding 1). It becomes a blocker if local mode is started behind a proxy before the fix lands. Findings 2 to 4 are round-2 minors, still open, not re-graded to major.\n\n## Checks\n\n1. Round-2 F1 reproduction (`uvicorn app.main:create --factory --host 0.0.0.0`, `ZLAYT_MODE=local`, HOST unset, dummy key, `ENABLE_LIVE` unset, port 7981, stopped afterwards). From the LAN address 192.168.199.106: GET /api/cases, /api/health, /, POST /api/cases, and GET /api/cases with `X-Forwarded-For`/`X-Real-IP`/`Forwarded: for=127.0.0.1` all returned 403 `forbidden`. From 127.0.0.1: GET /api/cases 200 `['cases']`. Server outbound TCP lines after the requests: 0. Listener count after stop: 0. Verbatim: `LAN GET /api/cases  src=192.168.199.106 -> 403 error.code=forbidden`.\n2. Round-2 F2 (D-036). `memory/ORCHESTRATOR_DECISIONS.md:44` reads \"Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash ... Local mode must refuse any non-loopback client by peer address\". `spec/REQUIREMENTS.md:138` (R-CO-4) cites \"(D-036)\". D-020 at line 28 is unchanged. No ruling on this exact point is in `submission/NEEDS_CHRIS.md` or `board/inbox/`.\n3. Unit tests. The brief's `python3 -m pytest -q tests/unit/test_api_routes.py` does not run here: system `python3` has no pytest (`No module named pytest`, exit 1). The project venv runs it: `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_api_routes.py` gives `31 passed in 5.63s`, and the same in the pinned archive gives `31 passed in 5.58s`.\n4. Carried round-2 minors (findings 2 to 4): gate files unchanged since e83eb54 (`git diff --quiet e83eb54 8ec0b25 -- app/llm/provider.py app/llm/backends/anthropic_api.py requirements.txt` exit 0). The round-2 evidence for these stands. I re-checked the SDK signature only.\n5. Proxy shape (new finding 1). Probe Part B: app bound to 127.0.0.1 with `ZLAYT_MODE=local`, a plain TCP relay on 0.0.0.0:7984 and a header-adding relay on 0.0.0.0:7985. Output verbatim: `direct LAN GET to app port (no proxy): connect refused/failed (ConnectionRefusedError)`; `LAN GET via plain loopback relay :7984 (no header added) src=192.168.199.106 -> 200 ['cases']`; `LAN GET via loopback relay adding X-Forwarded-For=192.168.199.106 :7985 ... -> 403 error.code=forbidden`.\n6. Startup refusal (`python -m app.main`, `HOST=0.0.0.0`, `ZLAYT_MODE=local`): exit 1, stderr last line `RuntimeError: ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost`, no listener.\n7. Secrets: `git check-ignore -v .env` gives `.gitignore:25:*.env\t.env`; `git ls-files .env | wc -l` gives `0`. The app does not load `.env` (no dotenv reference in `app/` or `tools/`). I did not read the `.env` contents.\n\n## Findings\n\n**1 (major, new in r3): the peer-address gate is not loopback-only behind a loopback proxy.** F1 is closed as written, and the peer check is right for direct access. But `is_loopback_peer` (`app/backend/api.py:81-88`) sees the proxy's address, not the client's. Every client a loopback proxy forwards passes the gate. The project's documented tailnet exposure is a proxy in front of the app port (`docs/RUNBOOK.md:8`, tailnet URL on :7860). The card handoff says the design \"works behind tailscale serve (loopback peer)\" (`board/cards/T-053.md`, Handoff). That is the failing shape. It is dormant today: `tools/serve_app.sh` does not set `ZLAYT_MODE`, so the tailnet app runs demo mode and `/api/cases` is 404. The data is synthetic, which limits the impact. I did not run `tailscale serve`, because it would change Chris's tailnet mapping, so I cannot say which headers it adds. A relay that adds `X-Forwarded-For` fails closed (uvicorn honours it from a loopback peer), so the tailnet outcome depends on what Tailscale sends.\n\n**2 (minor, carried from r2 F3, still open): `ENABLE_LIVE=1` without a key reports the live backend.** `app/llm/provider.py:28` checks only `ENABLE_LIVE`, while `live_enabled()` (`app/backend/api.py:103`) also needs a key. No live call happens (fail closed). The health label and the audit rows are wrong, and card decision (1) is not met as written. Source unchanged since e83eb54. Round-2 evidence: `out_probe2.txt` check A.\n\n**3 (minor, carried from r2 F4, still open): `RECORD_FIXTURES=1` alone opens live SDK calls on the dev path.** `provider.py:65-85` (`record_context`, `record_fragment_context`) set `_record_ok`, which bypasses the `ENABLE_LIVE` check at `provider.py:28`. The server path does not reach it (no caller in `app/backend/api.py`). Round-2 evidence: 132 SDK events in check B. Source unchanged since e83eb54.\n\n**4 (minor, carried from r2 F5, still open): pinned SDK cannot accept the `temperature` kwarg; `pip-audit` not run.** Re-checked this round: `inspect.signature(anthropic.resources.Messages.create).parameters` contains `'temperature'`: False, with `anthropic 2.3.0`. `requirements.txt:5` pins `anthropic==2.3.0`. `app/llm/backends/anthropic_api.py:26` passes `temperature=0`, so the live path raises `TypeError`. `.venv/bin/pip-audit` is absent (`No such file or directory`), and I did not re-run an audit this round.\n\n## What is right\n\n- F1 closed: the peer gate returns 403 for every LAN path with `uvicorn --host 0.0.0.0` and HOST unset, and 200 for loopback (out_probe.txt Part A).\n- Forwarding headers from a LAN peer are ignored (`LAN GET /api/cases + XFF/XRI/Forwarded=127.0.0.1 -> 403`).\n- D-036 is written and cited: `memory/ORCHESTRATOR_DECISIONS.md:44`, `spec/REQUIREMENTS.md:138`.\n\n## Exercised\n\n- `python3 tools/board.py show T-053`; read `personas/security.md`, `reviews/T-053-security-r2.md`, my memory dir (project_config_gate_patterns, feedback_round2_review_workflow, project_demo_live_gate).\n- `git rev-parse --short HEAD` (08764e7, then 8ec0b25, then 38421cc); `git log --oneline 08764e7..HEAD`; `git show --stat 08764e7`, `fa8a36e`, `8ec0b25`; `git show 08764e7 -- app/backend/api.py tests/unit/test_api_routes.py`; gate-file diffs listed above.\n- `git archive 8ec0b25` into `artifacts/review-evidence/T-053-r3/head_8ec0b25`.\n- `grep` of D-020 (line 28), D-036 (line 44), R-CO-4 (`spec/REQUIREMENTS.md:138`); read `app/backend/api.py` 77-106 and 170-190; `docs/RUNBOOK.md` 8-9 and 32; `tools/serve_app.sh`; `board/cards/T-053.md` Handoff; `grep` of `submission/NEEDS_CHRIS.md` and `board/inbox/` for library or D-036 rulings (none).\n- `python3 -m pytest -q tests/unit/test_api_routes.py` (system python3: exit 1, no pytest); `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_api_routes.py` in the repo and in the pinned archive: 31 passed both times.\n- `.venv/bin/python -I artifacts/review-evidence/T-053-r3-probe.py A B C` (output `artifacts/review-evidence/T-053-r3/out_probe.txt`): uvicorn CLI with `--host 0.0.0.0` on 7981 (killed; listener count 0); loopback relay on 7984/7985 with app on 7982 (all stopped, counts 0); `python -m app.main` with HOST=0.0.0.0 on 7983 (exit 1, no listener). Dummy key only.\n- `lsof` listener counts on 7981 to 7985 before and after.\n- `inspect.signature` check of `anthropic.resources.Messages.create` under `.venv` (anthropic 2.3.0).\n- Not run: `tailscale serve` (would change Chris's tailnet mapping), full unit suite, `pip-audit` (not installed), `tools/check_secrets.py` and gitleaks (not part of this round's brief).\n\n```json\n{\"card\": \"T-053\", \"persona\": \"security-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"HEAD 8ec0b25 pinned (git archive at artifacts/review-evidence/T-053-r3/head_8ec0b25; fix commit 08764e7 is an ancestor; HEAD 38421cc at write time, gate files unchanged 08764e7..HEAD); local app and relays on 127.0.0.1 and the LAN address, ports 7981-7985, all stopped; dummy key only, ENABLE_LIVE unset; sample case not run (access checks only)\",\n \"exercised\": [\n  \"python3 tools/board.py show T-053; read personas/security.md, reviews/T-053-security-r2.md, memory dir\",\n  \"git rev-parse --short HEAD (08764e7, 8ec0b25, 38421cc); git log --oneline 08764e7..HEAD; git show --stat 08764e7, fa8a36e, 8ec0b25; git show 08764e7 -- app/backend/api.py tests/unit/test_api_routes.py\",\n  \"git diff --stat 08764e7 HEAD -- app/backend/api.py app/main.py app/llm/provider.py app/llm/backends/anthropic_api.py tests/unit/test_api_routes.py requirements.txt: empty, exit 0; git diff --quiet e83eb54 8ec0b25 -- provider.py anthropic_api.py requirements.txt: exit 0\",\n  \"git archive 8ec0b25 into artifacts/review-evidence/T-053-r3/head_8ec0b25\",\n  \"grep ORCHESTRATOR_DECISIONS.md line 28 (D-020) and line 44 (D-036); spec/REQUIREMENTS.md:138 (R-CO-4 cites D-036); grep NEEDS_CHRIS.md and board/inbox for library ruling: none\",\n  \"read app/backend/api.py 77-106 and 170-190; docs/RUNBOOK.md 8-9, 32; tools/serve_app.sh; board/cards/T-053.md Handoff\",\n  \"python3 -m pytest -q tests/unit/test_api_routes.py: system python3 has no pytest (exit 1); .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_api_routes.py: 31 passed (repo and pinned archive)\",\n  \"artifacts/review-evidence/T-053-r3-probe.py parts A, B, C with .venv/bin/python -I: output artifacts/review-evidence/T-053-r3/out_probe.txt\",\n  \"lsof listener counts on 7981-7985 before and after; server outbound TCP lines after requests: 0\",\n  \"inspect.signature(anthropic.resources.Messages.create) under .venv: anthropic 2.3.0, 'temperature' False\",\n  \"git check-ignore -v .env: .gitignore:25; git ls-files .env: 0 lines\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"live-call gating in demo mode (checklist 4)\": 4, \"local-mode exposure and bind address, peer and proxy (checklist 18, r2 F1)\": 3, \"library admission vs D-020 and R-CO-4 (r2 F2)\": 4, \"secrets and key handling (checklist 10-11)\": 4, \"dependency pinning and audit (checklist 13)\": 2},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Local mode admits clients behind a loopback reverse proxy: the peer-address gate is not loopback-only (new in r3; r2 F1 closed as written)\",\n   \"evidence\": \"artifacts/review-evidence/T-053-r3/out_probe.txt PART B: 'direct LAN GET to app port (no proxy): connect refused/failed (ConnectionRefusedError)'; 'LAN GET via plain loopback relay :7984 (no header added) src=192.168.199.106 -> 200 ['cases']'; 'LAN GET via loopback relay adding X-Forwarded-For=192.168.199.106 :7985 ... -> 403 error.code=forbidden'. app/backend/api.py:81-88 (is_loopback_peer reads request.client.host) and :176 (gate). docs/RUNBOOK.md:8 (App tailnet URL on :7860). board/cards/T-053.md Handoff: 'works behind tailscale serve (loopback peer)'.\",\n   \"why_it_matters\": \"D-036 (memory/ORCHESTRATOR_DECISIONS.md:44) says local mode refuses any non-loopback client by peer address, and R-CO-4 (spec/REQUIREMENTS.md:138) says local mode is loopback only. A reverse proxy on 127.0.0.1 makes every client it forwards look like a loopback peer, so /api/cases and every case token reach any client that can reach the proxy. The project's documented tailnet exposure is a proxy in front of the app port (RUNBOOK.md:8). Dormant today: tools/serve_app.sh does not set ZLAYT_MODE, so the tailnet app runs demo mode. Data is synthetic, which limits impact. Re-rate to blocker if local mode is started behind tailscale serve or any proxy before the fix lands. A relay that adds X-Forwarded-For fails closed, so the tailscale serve outcome depends on the headers it sends; not verified (tailscale serve not run, it would change Chris's tailnet mapping).\",\n   \"fix\": \"In local mode, fail closed on the request as well as the socket peer: (a) refuse any request whose Host header is not localhost, 127.0.0.1 or [::1] with an optional port (DNS-rebinding style allowlist); (b) refuse any request carrying Forwarded, X-Forwarded-For, X-Real-IP or Tailscale-* headers. Keep is_loopback_peer. Document that local mode is for direct loopback access only and must not be served through tailscale serve or any proxy. Update the test client default (TestClient uses Host testserver) to a localhost Host.\",\n   \"acceptance_test\": \"tests/unit/test_api_routes.py: with ZLAYT_MODE=local and client=('127.0.0.1',5000): Host '192.168.199.106:7984' returns 403; Host 'localhost:7860' returns 200; a request with X-Forwarded-For returns 403; a request with Host 'localhost:7860' and no forwarding headers returns 200. Probe: rerun artifacts/review-evidence/T-053-r3-probe.py B; the plain-relay line must read 403.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"ENABLE_LIVE=1 without a key: health reports anthropic-api while demo_mode is true; every run fails BACKEND_UNAVAILABLE (carried from r2 F3, still open)\",\n   \"evidence\": \"app/llm/provider.py:28 (backend_name checks ENABLE_LIVE only); app/backend/api.py:103 (live_enabled also needs ANTHROPIC_API_KEY). Source unchanged since e83eb54 (git diff --quiet exit 0). Round-2 evidence: artifacts/review-evidence/T-053-r2/out_probe2.txt check A.\",\n   \"why_it_matters\": \"No live call happens, so this fails closed. It contradicts card decision (1) ('demo mode ALWAYS uses the fixture backend') and mislabels the audit rows. Not re-probed this round.\",\n   \"fix\": \"In provider.backend_name, return 'fixture' unless ENABLE_LIVE=1 and the backend's credential is present (ANTHROPIC_API_KEY for anthropic-api; claude CLI for claude-cli), matching live_enabled().\",\n   \"acceptance_test\": \"tests/unit/test_provider_backends.py: ENABLE_LIVE=1, LLM_BACKEND=anthropic-api, ANTHROPIC_API_KEY unset: backend_name() == 'fixture'; /api/health backend == 'fixture'.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"RECORD_FIXTURES=1 alone opens live SDK calls on the dev eval path (carried from r2 F4, still open)\",\n   \"evidence\": \"app/llm/provider.py:65-85 (record_context and record_fragment_context set _record_ok) and :28 (ENABLE_LIVE check bypassed when _record_ok). Source unchanged since e83eb54. Round-2 evidence: out_probe2.txt check B, 132 SDK events.\",\n   \"why_it_matters\": \"Not reachable from the server today (run_case and judge_summary have no caller in app/backend/api.py). A second env var that opens live calls is a configuration trap if the dev tools run on the public host.\",\n   \"fix\": \"Require ENABLE_LIVE=1 before record_context or record_fragment_context can set _record_ok, or narrow the docstring at provider.py:6 and :24-26 to name the entry points that may record.\",\n   \"acceptance_test\": \"tests/unit/test_provider_backends.py: RECORD_FIXTURES=1, LLM_BACKEND=anthropic-api, key set, ENABLE_LIVE unset: pipeline.run_case(golden sample) makes 0 SDK calls (SDK constructor patched to count).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Pinned anthropic SDK 2.3.0 cannot accept the temperature kwarg the live backend passes; pip-audit not installed (carried from r2 F5, still open)\",\n   \"evidence\": \"requirements.txt:5 'anthropic==2.3.0'. inspect.signature(anthropic.resources.Messages.create).parameters: 'temperature' in it: False (anthropic 2.3.0, .venv). app/llm/backends/anthropic_api.py:26 passes temperature=0. '.venv/bin/pip-audit: No such file or directory'.\",\n   \"why_it_matters\": \"The live path raises TypeError with the pinned SDK, and no dependency audit is recorded. Checklist 13 stays partly met.\",\n   \"fix\": \"Pin an SDK release whose Messages.create accepts temperature, verify the live path with a stub, install pip-audit and record 'pip-audit -r requirements.txt' output (or triage each finding), and add a check command.\",\n   \"acceptance_test\": \"A unit test asserts 'temperature' in inspect.signature(anthropic.resources.Messages.create).parameters for the pinned version; pip-audit -r requirements.txt exits 0 or each finding is triaged in the review.\"}\n ],\n \"whats_right\": [\n  \"F1 closed: with uvicorn --host 0.0.0.0 and HOST unset, every LAN request gets 403 and loopback gets 200; zero outbound connections from the server (out_probe.txt Part A).\",\n  \"Forwarding headers sent by a LAN peer (X-Forwarded-For, X-Real-IP, Forwarded) are ignored: the request is still 403.\",\n  \"D-036 is written and cited: memory/ORCHESTRATOR_DECISIONS.md:44 amends D-020 and spec/REQUIREMENTS.md:138 (R-CO-4) cites it.\"\n ],\n \"questions_for_chris\": [\n  \"D-036 rests on D-031 (multi-case scope). Is that your ruling that library texts may pass the demo gate in local mode? No ruling on this exact point is in NEEDS_CHRIS.md or board/inbox. If you did not intend it, say so and the amendment is reversed.\",\n  \"Do you want local mode reachable from your tailnet (phone)? If yes, the rule must change (peer address cannot give loopback-only behind a proxy). If no, keep local mode off the tailnet app URL and apply the Host and forwarding-header fix (finding 1).\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:37:20.540Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-053-security-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:26.529Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport json,re\ntxt=open(\"reviews/T-053-security-r3.md\",encoding=\"utf-8\").read()\nm=re.search(r\"```json\\n(.*?)\\n```\",txt,re.S)\nj=json.loads(m.group(1))\nprint(\"json ok; keys:\",sorted(j.keys()))\nprint(\"verdict:\",j[\"verdict\"],\"| severities:\",[f[\"severity\"] for f in j[\"findings\"]])\nblockers=[f for f in j[\"findings\"] if f[\"severity\"]==\"blocker\"]; majors=[f for f in j[\"findings\"] if f[\"severity\"]==\"major\"]\nexp=\"fail\" if blockers else (\"changes\" if majors else \"pass\")\nprint(\"rule-expected verdict:\",exp,\"matches:\",exp==j[\"verdict\"])\nEOF\ngrep -n \"def live_enabled\\|def backend\\b\\|def demo_mode\" app/backend/api.py; grep -n \"def record_context\\|def record_fragment_context\" app/llm/provider.py; grep -n \"temperature\" app/llm/backends/anthropic_api.py | head -2; grep -n \"anthropic==\" requirements.txt",
 "description": "Validate review JSON block against verdict rule and check line refs"
}
````

### User / tool · 2026-11-02T02:37:26.662Z

**tool result**
````
json ok; keys: ['card', 'exercised', 'findings', 'model', 'persona', 'questions_for_chris', 'scope', 'scores', 'verdict', 'whats_right']
verdict: changes | severities: ['major', 'minor', 'minor', 'minor']
rule-expected verdict: changes matches: True
109:    def backend():
113:    def live_enabled():
116:    def demo_mode():
65:def record_context(source_text: str):
77:def record_fragment_context(fragment: str):
1:"""anthropic-api backend: Anthropic SDK, temperature 0, schema via a forced tool call. ADR-004. One attempt, no retry."""
26:            model=model, max_tokens=MAX_TOKENS, temperature=0, system=system,
5:anthropic==2.3.0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:36.020Z

**tool call — Bash**
````
{
 "command": "cat >> reviews/T-053-security-r3.md <<'EOF'\n\n---\n\nCorrection, appended after the JSON block (the record above stands otherwise): in finding 2 the `live_enabled()` reference is `app/backend/api.py:113`, not `:103`. I checked line numbers with grep after writing the record. No other line reference is affected.\nEOF\ntail -4 reviews/T-053-security-r3.md | cut -c1-160; python3 -c \"import re,json;t=open('/Users/arsis/zlayt-pm-project/reviews/T-053-security-r3.md').read();print('json fences:',len(re.findall(r'\\x60\\x60\\x60json',t)))\"",
 "description": "Append line-reference correction to the review and count json fences"
}
````

### User / tool · 2026-11-02T02:37:36.136Z

**tool result**
````
---

Correction, appended after the JSON block (the record above stands otherwise): in finding 2 the `live_enabled()` reference is `app/backend/api.py:113`, not `:10
json fences: 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:40.809Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/project_config_gate_patterns.md",
 "old_string": "**Why:** these are the four ways the T-053 gates were weakened or left inconsistent in rounds 1-2.",
 "new_string": "Pattern 5 (T-053 r3): a peer-address gate is not loopback-only behind a loopback proxy. After the peer check (api.py:81-88, gate api.py:176) the uvicorn --host 0.0.0.0 bypass is closed (LAN 403, loopback 200), but a relay on 127.0.0.1 forwarding LAN clients gives 200 with no header added (out_probe Part B). The project's own tailnet exposure is `tailscale serve` in front of :7860 (RUNBOOK.md:8), and the card handoff says \"works behind tailscale serve (loopback peer)\". Forwarding headers are ignored from a LAN peer, and uvicorn honours X-Forwarded-For from a loopback peer, so a header-adding proxy fails closed. Fix shape: Host allowlist (localhost/127.0.0.1/[::1]) plus refusing Forwarded/X-Forwarded-*/X-Real-IP/Tailscale-* in local mode. Any \"loopback only\" rule must be checked behind every proxy the RUNBOOK documents.\n\n**Why:** these are the five ways the T-053 gates were weakened or left inconsistent in rounds 1-3."
}
````

### User / tool · 2026-11-02T02:37:40.901Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/project_config_gate_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:42.672Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md",
 "old_string": "Persona scope: if a brief asks",
 "new_string": "T-053 r3 (2026-11-01): HEAD was 08764e7 at the first check, 8ec0b25 at the pin, 38421cc at write time (docs and memory only; gate files unchanged). Pin the commit you test, then re-check drift at write time. Brief says `python3 -m pytest`, but system python3 has no pytest: use `.venv/bin/python -m pytest -p no:cacheprovider`, and do not pipe pytest into tail when you need the exit code (the pipe hides it). After the first Write, a self-found error (I cited api.py:103 for live_enabled, which is at :113) was fixed by appending a correction after the JSON block, not by Edit, because reviews are append-only. Proofread line refs with grep before the first Write, not after.\n\nPersona scope: if a brief asks"
}
````

### User / tool · 2026-11-02T02:37:42.774Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:43.456Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md",
 "old_string": "- [Demo live-call gate]",
 "new_string": "- [Config gate patterns](project_config_gate_patterns.md) — now includes Pattern 5: peer-address gate defeated by a loopback proxy (tailscale serve shape, T-053 r3)\n- [Demo live-call gate]"
}
````

### User / tool · 2026-11-02T02:37:43.564Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:45.147Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T02:37:45.153Z

**tool result**
````
1	- [Hook/guard review patterns](project_hook_guard_review_patterns.md) — recurring bypass classes in git-guard/board-guard/check_secrets and reviewer-workflow gotchas
2	- [Round-2 review workflow](feedback_round2_review_workflow.md) — pin with git archive, HEAD moves 6+ times, reviewer-write-guard makes first Write final, probe capture bugs
3	- [Config gate patterns](project_config_gate_patterns.md) — now includes Pattern 5: peer-address gate defeated by a loopback proxy (tailscale serve shape, T-053 r3)
4	- [Demo live-call gate](project_demo_live_gate.md) — r1 blocker fixed in provider.backend_name (T-053 r2 verified); residual ENABLE_LIVE/RECORD_FIXTURES paths
5	- [Config gate patterns](project_config_gate_patterns.md) — env-var gates vs the real bind/peer (uvicorn --host bypass), second toggles, label mismatch, spec amendments in card notes only
6	- [PDF upload review patterns](project_pdf_upload_review_patterns.md) — pypdf logs record text to stderr, unpinned parser, demo-gate ordering, parse-time DoS (T-054, r2: fixed; pypdf 75 MB array cap)
7	- [Batch and export_config patterns](project_batch_export_review_patterns.md) — regex `$` lets a trailing newline through; per-case ids; sample has no needs_review; untracked LLM fixtures break archive pins (T-055/T-058)
8	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:46.719Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md",
 "old_string": "- [Config gate patterns](project_config_gate_patterns.md) — now includes Pattern 5: peer-address gate defeated by a loopback proxy (tailscale serve shape, T-053 r3)\n- [Demo live-call gate]",
 "new_string": "- [Demo live-call gate]"
}
````

### User / tool · 2026-11-02T02:37:46.809Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:47.583Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md",
 "old_string": "- [Config gate patterns](project_config_gate_patterns.md) — env-var gates vs the real bind/peer (uvicorn --host bypass), second toggles, label mismatch, spec amendments in card notes only",
 "new_string": "- [Config gate patterns](project_config_gate_patterns.md) — env-var gates vs the real bind/peer, loopback-proxy bypass (T-053 r3 pattern 5), second toggles, label mismatch, spec amendments"
}
````

### User / tool · 2026-11-02T02:37:47.682Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:51.905Z

Verdict: changes. Both round-2 majors are closed as written: F1 (uvicorn `--host 0.0.0.0`, HOST unset) returns 403 from the LAN and 200 from 127.0.0.1, and D-036 amends D-020 with R-CO-4 citing it. `python3 -m pytest -q tests/unit/test_api_routes.py` does not run on system python3 (no pytest). The venv run gives 31 passed.
New major: a loopback reverse proxy (the `tailscale serve` shape in RUNBOOK) gives LAN clients 200 on /api/cases, so local mode is not loopback-only behind a proxy. Review: /Users/arsis/zlayt-pm-project/reviews/T-053-security-r3.md; probe output: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-r3/out_probe.txt.
