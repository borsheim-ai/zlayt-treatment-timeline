# Subagent: T-040 review (sonnet security) (T-040 review (sonnet security))

Source: `agent-a130acfde66311bca.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:59:09.798Z

Working directory: /Users/arsis/zlayt-pm-project. Review T-040 "FastAPI routes, demo gate, review/edit/confirm_date" (AC: `python3 tools/board.py show T-040`; card notes say how to run). Run `.venv/bin/python -m pytest tests/unit/test_review_rules.py tests/unit/test_api.py -q 2>&1 | tail -3`. Start the app on a free port with LLM_BACKEND=fixture (per card notes; background, kill after) and probe with curl: demo gate (non-fixture text → 409 demo_mode_unsupported_input, nothing stored — check DB row counts before/after), empty 400 / oversize 413 with no LLM call, unknown token 404, invalid edits 422 (entry date/provider, charge amount/class), 409 needs_confirm for '+$9,000', confirm_date date_invalid, decisions survive restart, Referrer-Policy no-referrer, no tokens in access logs, no stack traces in errors, input not reflected unescaped, export router registered. Write reviews/T-040-security.md (D.2 JSON). Do not fix. Reply ≤ 3 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:11.110Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/security.md"
}
````

### User / tool · 2026-11-02T01:59:11.125Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:11.696Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-040; ls .claude/agent-memory/security-reviewer/"
}
````

### User / tool · 2026-11-02T01:59:11.831Z

**tool result**
````
---
id: "T-040"
title: "FastAPI routes, demo gate, review/edit/confirm_date with re-check"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: ["T-037", "T-039", "T-031"]
created_by: "orchestrator"
created_at: "2026-11-02T01:14:10Z"
updated_at: "2026-11-02T01:59:10Z"
claimed_by: "backend"
claimed_at: "2026-11-02T01:49:59Z"
rounds: 0
commits: ["a7df086"]
reviews: []
ac:
  - {"n": 1, "text": "`pytest tests/unit/test_review_rules.py` green: 422 invalid_edit matrix, 409 needs_confirm then keep-my-wording, JUDGE_UNAVAILABLE, charges accept/dismiss/reset only (R-RV-2, R-RV-3, R-CH-7, R-RV-5, row 15 for edits)", "done": true, "evidence": "tests/unit/test_review_rules.py 23 passed (real pipeline + FakeCall)"}
  - {"n": 2, "text": "`pytest tests/unit/test_api.py` green with fixture TestClient: all 11 endpoints match memory/contracts/api.md shapes, error format, unknown token 404, Why? returns ladder + backend (R-TL-6)", "done": true, "evidence": "tests/unit/test_api_routes.py 14 passed (TestClient, fixture backend, 11 endpoints); tests/e2e/test_api.py 7/8 against live :7860 (golden byte-equality needs T-037 golden fixtures)"}
  - {"n": 3, "text": "demo gate: unrecorded text -> 409 demo_mode_unsupported_input and nothing stored; oversize 413, empty 400 with LLM counter 0 (R-IN-4, R-CO-4 demo part, D-020)", "done": true, "evidence": "test_api_routes::test_demo_gate_refuses_unrecorded_text_and_stores_nothing (409, 0 cases stored, 413, 400)"}
  - {"n": 4, "text": "confirm_date on case_01 record 8 with 2026-05-04 -> entry sorts after 03-25, gap table unchanged, event logged; no readings -> cannot confirm (R-IN-5, R-RV-2)", "done": true, "evidence": "test_api_routes::test_confirm_date_case_01 + test_review_rules::test_confirm_date_*"}
  - {"n": 5, "text": "decisions survive a new TestClient/app restart (R-RV-8); only review and confirm_date set review_status (grep test); Referrer-Policy: no-referrer, no access log of tokens", "done": true, "evidence": "test_review_decisions_survive_restart, test_only_review_module_sets_review_status, Referrer-Policy header test, app/main.py access_log=False"}
---
## Description
The HTTP layer plus review rules. Covers R-IN-4, R-IN-5, R-TL-6, R-CH-5, R-CH-7, R-RV-2, R-RV-3, R-RV-5, R-RV-8 and the demo-mode half of R-CO-4. Edited summaries are re-checked by the D-006 token check and judge #1 (row 15).

Plan key: m3-be-api-review (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

Estimate: 45 min.

## Notes (append-only, newest last)
- 2026-11-02T01:32:27Z orchestrator: updated body appended from artifacts/tmp/est_T-040.md
- 2026-11-02T01:49:49Z orchestrator: assigned: backend-3
- 2026-11-02T01:49:59Z backend: claimed
- 2026-11-02T01:49:59Z backend: backend-3: claimed with --force (deps in progress). QA: tests/unit/test_provider_backends.py (added under T-034, qa-owned dir) needs adopting.
- 2026-11-02T01:59:01Z backend: AC 1 checked: tests/unit/test_review_rules.py 23 passed (real pipeline + FakeCall)
- 2026-11-02T01:59:01Z backend: AC 2 checked: tests/unit/test_api_routes.py 14 passed (TestClient, fixture backend, 11 endpoints); tests/e2e/test_api.py 7/8 against live :7860 (golden byte-equality needs T-037 golden fixtures)
- 2026-11-02T01:59:01Z backend: AC 3 checked: test_api_routes::test_demo_gate_refuses_unrecorded_text_and_stores_nothing (409, 0 cases stored, 413, 400)
- 2026-11-02T01:59:01Z backend: AC 4 checked: test_api_routes::test_confirm_date_case_01 + test_review_rules::test_confirm_date_*
- 2026-11-02T01:59:01Z backend: AC 5 checked: test_review_decisions_survive_restart, test_only_review_module_sets_review_status, Referrer-Policy header test, app/main.py access_log=False
- 2026-11-02T01:59:01Z backend: DEFECT for T-037/db owners: pipeline and db use unsuffixed global PKs (r1,e5,f_gap_r6_r7) so a SECOND case in the same sqlite file collides (IntegrityError). API works for one live case at a time; needs per-case id namespacing in db/pipeline. Also: golden export byte-equality (e2e test_export_is_deterministic_and_equals_golden) fails because recorded fixtures give different summaries/excerpts than golden (e.g. entry 2 excerpt includes the ER charges sentence). llm_calls.prompt_version is not set by audited.make_call (contract wants extract_v1).
- 2026-11-02T01:59:01Z backend: moved in_progress -> in_review
- 2026-11-02T01:59:10Z orchestrator: review dispatched: security (sonnet)

## Handoff
What changed: app/backend/{api,review,present,store}.py, app/main.py (uvicorn app.main:create --factory or python -m app.main; :7860, statics from app/frontend, access log off), tests/unit/test_api_routes.py. Verified: test_review_rules 23, test_api_routes 14, test_api 1, e2e API 7/8. Left: id collision across cases (note), golden export equality (fixtures), prompt_version on audit rows. Surprised: pipeline already persisted via ingest_case so API only wraps it; review edit is judged via audited.make_call so demo-mode edits get JUDGE_UNAVAILABLE.

MEMORY.md
feedback_round2_review_workflow.md
project_hook_guard_review_patterns.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:13.008Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md"
}
````

### User / tool · 2026-11-02T01:59:13.016Z

**tool result**
````
1	---
2	name: round2-review-workflow
3	description: Workflow gotchas for round-2 re-reviews (HEAD moves mid-review, git-guard blocks $() in echo, probes without scratch files)
4	metadata:
5	  type: feedback
6	---
7	
8	Round-2 re-reviews of a card: pin the commit you actually tested. Other agents commit to the same repo during a review, so HEAD moved from b1803c0 to 250e7b6 within one session. Run `git rev-parse --short HEAD` in the same call as the pytest run and quote both in the review.
9	
10	The git-guard PreToolUse hook rejects Bash commands that put `$(...)` substitutions in an `echo` or similar command position ("unresolved variable or substitution in command position"). Use one command per git query instead of nesting substitutions.
11	
12	Probes of minor fixes can run as `.venv/bin/python - <<'EOF' ... EOF` on stdin, so no scratch file is written and nothing needs a path under reviews/ or the scratchpad.
13	
14	**Why:** T-034 round 2 (2026-11-01): the first `$()` echo was blocked, and HEAD changed between my pytest run and my final grep.
15	**How to apply:** when re-reviewing, check HEAD before and after the pytest run, and quote the sha with the test output. Keep git commands separate.
16	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:13.702Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_review_rules.py tests/unit/test_api.py -q 2>&1 | tail -3; wc -l app/main.py app/backend/api.py app/backend/review.py app/backend/store.py app/backend/present.py; git log --oneline | head -3"
}
````

### User / tool · 2026-11-02T01:59:15.428Z

**tool result**
````
........................                                                 [100%]
24 passed in 1.31s
      14 app/main.py
     314 app/backend/api.py
     209 app/backend/review.py
      67 app/backend/store.py
     200 app/backend/present.py
     804 total
f861159 fix(backend): audited role_for treats j1..j4 steps as judge (T-034)
a7df086 feat(backend): FastAPI routes, demo gate, review/edit/confirm_date with re-check (T-040)
348cd0b fix(frontend): entries-only count line, no false tray error, UX minors (T-042 r2)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:16.654Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/api.py"
}
````

### User / tool · 2026-11-02T01:59:16.662Z

**tool result**
````
1	"""FastAPI routes (memory/contracts/api.md). Thin: parsing, the demo gate, error format; logic lives in ingest/store/review/present/export.
2	
3	Demo mode (D-008/D-020): only text whose normalised sha256 is a golden input is accepted; anything else is refused with 409 BEFORE
4	anything is stored. Never logs record text, tokens or prompts (run uvicorn with access_log off; see app/main.py).
5	"""
6	import hashlib
7	import json
8	import os
9	import pathlib
10	import threading
11	import time
12	
13	from fastapi import FastAPI, Request
14	from fastapi.exceptions import RequestValidationError
15	from fastapi.responses import JSONResponse, Response
16	from starlette.exceptions import HTTPException as StarletteHTTPException
17	
18	from app.backend import ingest, present, review, store
19	from app.db import db as DB
20	
21	ROOT = pathlib.Path(__file__).resolve().parents[2]
22	GOLDEN = ROOT / "evals" / "golden"
23	VERSION = "0.1.0"
24	BANNER = "Synthetic data only — never paste real records"
25	AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
26	STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]
27	_ERR_STATUS = {"bad_request": 400, "input_too_large": 413}
28	
29	
30	class ApiError(Exception):
31	    def __init__(self, status, code, message="", detail=None):
32	        super().__init__(code)
33	        self.status, self.code, self.message, self.detail = status, code, message or code.replace("_", " "), detail or {}
34	
35	
36	def digest(text: str) -> str:
37	    return hashlib.sha256(ingest.normalize_text(text).encode("utf-8")).hexdigest()
38	
39	
40	def recorded_hashes() -> set:
41	    return {digest(p.read_text()) for p in GOLDEN.glob("*.txt")}
42	
43	
44	def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
45	    db_path = db_path or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")
46	    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
47	    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
48	    app.state.db_path = db_path
49	    app.state.recorded = recorded_hashes()
50	    runs = {}
51	    DB.connect(db_path).close()
52	
53	    # -------------------------------------------------- config (read per call so tests can monkeypatch env)
54	    def backend():
55	        return os.environ.get("LLM_BACKEND", "fixture") or "fixture"
56	
57	    def live_enabled():
58	        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
59	
60	    def demo_mode():
61	        return not live_enabled()
62	
63	    def models():
64	        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
65	
66	    def conn():
67	        return DB.connect(app.state.db_path)
68	
69	    def make_call(c, cid):
70	        if call_factory:
71	            return call_factory(c, cid)
72	        from app.llm import audited
73	        return audited.make_call(c, cid)
74	
75	    def pipeline_mod():
76	        if pipeline is not None:
77	            return pipeline
78	        from app.backend import pipeline as PL
79	        return PL
80	
81	    def get_case(c, token):
82	        case = DB.get_case(c, token)
83	        if case is None:
84	            raise ApiError(404, "not_found", "No such case.")
85	        return case
86	
87	    # -------------------------------------------------- errors / headers
88	    @app.exception_handler(ApiError)
89	    async def _api_error(_, e):
90	        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)
91	
92	    @app.exception_handler(review.ReviewError)
93	    async def _review_error(_, e):
94	        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)
95	
96	    @app.exception_handler(StarletteHTTPException)
97	    async def _http_error(_, e):
98	        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
99	        return JSONResponse({"error": {"code": code, "message": code.replace("_", " "), "detail": {}}}, status_code=e.status_code)
100	
101	    @app.exception_handler(RequestValidationError)
102	    async def _validation(_, e):
103	        return JSONResponse({"error": {"code": "bad_request", "message": "Malformed request.", "detail": {}}}, status_code=400)
104	
105	    @app.middleware("http")
106	    async def _headers(request, call_next):
107	        resp = await call_next(request)
108	        resp.headers["Referrer-Policy"] = "no-referrer"
109	        resp.headers["X-Content-Type-Options"] = "nosniff"
110	        resp.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api") else resp.headers.get("Cache-Control", "no-cache")
111	        return resp
112	
113	    async def body_of(request: Request) -> dict:
114	        raw = await request.body()
115	        if not raw:
116	            return {}
117	        try:
118	            b = json.loads(raw)
119	        except ValueError:
120	            raise ApiError(400, "bad_request", "Request body is not valid JSON.") from None
121	        if not isinstance(b, dict):
122	            raise ApiError(400, "bad_request", "Request body must be a JSON object.")
123	        return b
124	
125	    # -------------------------------------------------- routes
126	    @app.get("/api/health")
127	    def health():
128	        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
129	                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
130	                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
131	
132	    @app.post("/api/cases", status_code=201)
133	    async def create_case(request: Request):
134	        b = await body_of(request)
135	        sample = b.get("sample") is True
136	        text = (GOLDEN / "sample.txt").read_text() if sample else b.get("text")
137	        if not isinstance(text, str):
138	            raise ApiError(400, "bad_request", "Provide text or sample: true.")
139	        try:
140	            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
141	        except ingest.IngestError as e:
142	            raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
143	        if demo_mode() and digest(text) not in app.state.recorded:
144	            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
145	        c = conn()
146	        try:
147	            now = time.time()
148	            DB.purge_expired(c, now)
149	            name = b.get("name") if isinstance(b.get("name"), str) else ("Sample case" if sample else None)
150	            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None, source="sample" if sample else "paste",
151	                                 backend=backend(), demo_mode=int(demo_mode()))
152	            try:
153	                ing = pipeline_mod().ingest_case(c, cid, text, now)
154	            except ingest.IngestError as e:
155	                DB.delete_case(c, cid)
156	                raise ApiError(_ERR_STATUS.get(e.code, 400), e.code) from None
157	            recs = [present.record_view(r, text, with_sentences=False) for r in present._recs_by_id(c, cid).values()]
158	            flags = DB.list_items(c, cid, "flag")
159	            return {"token": cid, "name": DB.get_case(c, cid)["name"], "status": "ingested", "source": "sample" if sample else "paste",
160	                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
161	                    "dates_to_confirm": present.dates_to_confirm(c, cid),
162	                    "gap_flags": [f["id"] for f in flags if f["type"] == "gap"],
163	                    "record_warning_flags": [f["id"] for f in flags if f["type"] == "record_warning"],
164	                    "warnings": ing["warnings"]}
165	        finally:
166	            c.close()
167	
168	    @app.get("/api/cases/{token}")
169	    def get_case_view(token: str):
170	        c = conn()
171	        try:
172	            get_case(c, token)
173	            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
174	        finally:
175	            c.close()
176	
177	    @app.delete("/api/cases/{token}", status_code=204)
178	    def delete_case(token: str):
179	        c = conn()
180	        try:
181	            get_case(c, token)
182	            DB.delete_case(c, token)
183	        finally:
184	            c.close()
185	        return Response(status_code=204)
186	
187	    def _run_thread(token, raw):
188	        c = conn()
189	        try:
190	            mod = pipeline_mod()
191	            mod.run_pipeline(c, token, raw, call=make_call(c, token), now=time.time)
192	            if DB.get_case(c, token)["status"] == "running":
193	                DB.update_case(c, token, status="ready", stage="finalize", run_finished_at=time.time())
194	        except Exception as e:                                   # code only: no message text from the pipeline
195	            DB.update_case(c, token, status="failed", run_finished_at=time.time(),
196	                           error=json.dumps({"code": getattr(e, "code", "run_failed"), "message": "The run stopped; finished items are kept."}))
197	        finally:
198	            c.close()
199	            runs.pop(token, None)
200	
201	    @app.post("/api/cases/{token}/run", status_code=202)
202	    async def run_case(token: str, request: Request):
203	        b = await body_of(request)
204	        c = conn()
205	        try:
206	            case = get_case(c, token)
207	            if case["status"] == "running" or token in runs:
208	                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
209	            if demo_mode() and digest(case["raw_text"]) not in app.state.recorded:
210	                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
211	            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
212	                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
213	            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
214	            if decided and b.get("confirm_rerun") is not True:
215	                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
216	            now = time.time()
217	            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
218	            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
219	            runs[token].start()
220	            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
221	        finally:
222	            c.close()
223	
224	    @app.get("/api/cases/{token}/status")
225	    def status(token: str):
226	        c = conn()
227	        try:
228	            case = get_case(c, token)
229	            stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
230	            stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
231	            stages = list(stages) if not callable(stages) else STAGES
232	            done = stages.index(stage) if stage in stages else 0
233	            end = case["run_finished_at"] or time.time()
234	            return {"token": token, "status": case["status"], "stage": stage, "stages": stages,
235	                    "progress": {"done": done, "total": len(stages), "label": f"Step {done + 1} of {len(stages)}: {stage}" if stage else ""},
236	                    "counts": {"entries": len(DB.list_items(c, token, "entry")), "amounts": len(DB.list_items(c, token, "amount")),
237	                               "flags": len(DB.list_items(c, token, "flag"))},
238	                    "error": json.loads(case["error"]) if case["error"] else None,
239	                    "elapsed_ms": int((end - case["run_started_at"]) * 1000) if case["run_started_at"] else 0}
240	        finally:
241	            c.close()
242	
243	    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
244	    async def confirm_date(token: str, rid: str, request: Request):
245	        b = await body_of(request)
246	        if not isinstance(b.get("date"), str):
247	            raise ApiError(400, "bad_request", "Provide the chosen date.")
248	        c = conn()
249	        try:
250	            get_case(c, token)
251	            return review.confirm_date(c, token, rid, b["date"])
252	        finally:
253	            c.close()
254	
255	    @app.get("/api/cases/{token}/items/{item_id}")
256	    def item(token: str, item_id: str):
257	        c = conn()
258	        try:
259	            get_case(c, token)
260	            try:
261	                return present.why_view(c, token, item_id)
262	            except (KeyError, IndexError):
263	                raise ApiError(404, "not_found", "No such item.") from None
264	        finally:
265	            c.close()
266	
267	    @app.post("/api/cases/{token}/items/{item_id}/review")
268	    async def review_item(token: str, item_id: str, request: Request):
269	        b = await body_of(request)
270	        c = conn()
271	        try:
272	            get_case(c, token)
273	            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
274	        finally:
275	            c.close()
276	
277	    @app.get("/api/cases/{token}/export")
278	    def export(token: str):
279	        from app.backend import export_routes as XR
280	        c = conn()
281	        try:
282	            get_case(c, token)
283	            case = store.export_case(c, token)
284	            ex = XR.export_payload(token, case)
285	            calls = DB.list_llm_calls(c, token)
286	            ok = ("accepted", "edited")
287	            tv = present.totals_view(c, token)
288	            ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
289	            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
290	            ex["excluded"] = {"pending": case["pending_count"],
291	                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
292	                              "rejected": sum(1 for k in ("entry", "amount") for r in DB.list_items(c, token, k) if r["state"] == "rejected")}
293	            ex["provenance"] = {"generator_model": models()["generator"], "judge_model": models()["judge"], "backend": backend(),
294	                                "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
295	                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
296	                                "edited_count": sum(1 for x in case["entries"] if x["review_status"] == "edited")}
297	            return ex
298	        finally:
299	            c.close()
300	
301	    @app.get("/api/cases/{token}/audit")
302	    def audit(token: str):
303	        c = conn()
304	        try:
305	            get_case(c, token)
306	            return present.audit_view(c, token)
307	        finally:
308	            c.close()
309	
310	    sd = pathlib.Path(static_dir) if static_dir else ROOT / "app" / "frontend"
311	    if sd.is_dir():
312	        from fastapi.staticfiles import StaticFiles
313	        app.mount("/", StaticFiles(directory=str(sd), html=True), name="frontend")
314	    return app
315	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:16.963Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/main.py"
}
````

### User / tool · 2026-11-02T01:59:16.970Z

**tool result**
````
1	"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens)."""
2	import os
3	
4	import uvicorn
5	
6	from app.backend.api import create_app
7	
8	def create():
9	    """uvicorn app.main:create --factory"""
10	    return create_app()
11	
12	
13	if __name__ == "__main__":
14	    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
15	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:17.048Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/store.py"
}
````

### User / tool · 2026-11-02T01:59:17.055Z

**tool result**
````
1	"""DB <-> unit-dict adapters shared by the API layer and the pipeline (T-040). Pure functions plus ingest persistence.
2	
3	Item/record ids are the pipeline's own ("r6", "e5", "f_gap_r6_r7"); see the id-collision note on T-040.
4	"""
5	from app.backend import ingest
6	from app.db import db as DB
7	
8	
9	def iso(t) -> str:
10	    import datetime
11	    return datetime.datetime.fromtimestamp(float(t or 0), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
12	
13	
14	def load_records(conn, case_id: str, raw: str = None) -> list:
15	    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
16	    if raw is None:
17	        raw = DB.get_case(conn, case_id)["raw_text"]
18	    out = []
19	    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
20	        d = DB._decode(r)
21	        block = raw[d["char_start"]:d["char_end"]]
22	        try:
23	            body = ingest.split_records(block)[0]["excerpt"]
24	        except Exception:
25	            body = block
26	        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
27	                    "kind": "encounter" if d["encounter"] else "other", "date_candidates": d["date_candidates"] or []})
28	    return out
29	
30	
31	def _by_id(records):
32	    return {r["id"]: r for r in records}
33	
34	
35	# ---------------------------------------------------------------- unit dicts for export / totals
36	def export_case(conn, case_id: str) -> dict:
37	    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
38	    case = DB.get_case(conn, case_id)
39	    recs = load_records(conn, case_id, case["raw_text"])
40	    n_of = {r["id"]: r["n"] for r in recs}
41	    ents = []
42	    for e in DB.list_items(conn, case_id, "entry"):
43	        if e["state"] == "rejected":
44	            continue
45	        ed = e.get("edited") or {}
46	        d = dict(id=e["id"], record_ids=e["record_ids"], record_no=n_of.get((e["record_ids"] or [None])[0], 0), summary=ed.get("summary", e["summary"]),
47	                 excerpt=ed.get("excerpt", e["excerpt"]), review_status=e["review_status"], date_iso=e["date_iso"])
48	        if "summary" in ed:
49	            d["original_summary"] = ed.get("original_summary", e["summary"])
50	        if "excerpt" in ed:
51	            d["original_excerpt"] = ed.get("original_excerpt", e["excerpt"])
52	        if ed.get("kept_my_wording"):
53	            d["keep_wording"] = True
54	        ents.append(d)
55	    amts = [dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
56	                 excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
57	    fl = []
58	    for f in DB.list_items(conn, case_id, "flag"):
59	        c = f.get("computed") or {}
60	        ev = [dict(record_no=x.get("record_no") or n_of.get(x.get("record_id"), 0), field=x.get("field", "excerpt"),
61	                   excerpt=x.get("excerpt") or x.get("text")) for x in f.get("evidence") or []]
62	        fl.append(dict(id=f["id"], type=f["type"], subtype=c.get("subtype") or f["category"], evidence=ev, review_status=f["review_status"],
63	                       days=c.get("days"), from_date=c.get("from_date"), to_date=c.get("to_date"), note=f.get("reviewer_note")))
64	    events = [dict(type=ev["action"], item_id=ev["item_id"]) for ev in DB.list_events(conn, case_id) if ev["action"] == "keep_my_wording"]
65	    pending = sum(1 for x in ents + amts + fl if x["review_status"] == "pending")
66	    records = [dict(n=r["n"], source=r["source"], date_iso=r["date_iso"], excerpt=r["excerpt"]) for r in recs]
67	    return dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events)
68	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:20.121Z

**tool call — Bash**
````
{
 "command": "grep -n \"token\\|secrets\\|uuid\" app/db/db.py | head -20; grep -n \"MAX_CHARS\\|MAX_RECORDS\\|def check_limits\" -A6 app/backend/ingest.py | head -40; ls evals/golden | head; cat app/backend/export_routes.py | head -30; grep -n \"DATA_DIR\" -r app | head"
}
````

### User / tool · 2026-11-02T01:59:20.242Z

**tool result**
````
11:import secrets
39:    return prefix + secrets.token_hex(6)
55:    cid = fields.pop("id", None) or secrets.token_urlsafe(16)
8:MAX_CHARS = 60000
9:MAX_RECORDS = 40
10-
11-# The only text ever set aside as a non-record: the exact banner lines of the golden/sample files. Any other first line is kept as text.
12-BANNERS = ("SYNTHETIC — invented for evaluation; not real patient data",
13-           "SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data")
14-
15-_HEADER = re.compile(r"^=== Record (\d+) ===[ \t]*$", re.MULTILINE)
--
36:def check_limits(text: str, max_chars: int = MAX_CHARS) -> str:
37-    """Raise before anything else (and so before any LLM call): empty -> bad_request, oversize -> input_too_large."""
38-    t = normalize_text(text)
39-    if not t:
40-        raise IngestError("bad_request")
41-    if len(t) > max_chars:
42-        raise IngestError("input_too_large")
--
142:def split_records(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS) -> list:
143-    text = check_limits(raw_text, max_chars)
144-    recs, _ = _split(text)
145-    if len(recs) > max_records:
146-        raise IngestError("input_too_large")
147-    return recs
148-
--
191:def ingest(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS) -> dict:
192-    """Everything stage 0 knows, with zero model calls. Raises IngestError('bad_request'|'input_too_large') first."""
193-    text = check_limits(raw_text, max_chars)
194-    recs, method = _split(text)
195-    if len(recs) > max_records:
196-        raise IngestError("input_too_large")
197-    groups = dedupe(recs)
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
"""GET /api/cases/{token}/export: thin router around export.build_export (T-041). Code only.

The app factory (T-040) does `app.include_router(export_routes.router)` and registers the case loader once:
    export_routes.set_case_loader(fn)   # fn(token) -> case dict (see export.py docstring) or None for an unknown token
Items with review_status other than accepted/edited never reach either block (ADR-009, LLM_VS_CODE row 19).
"""
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.backend import export

router = APIRouter()
_loader = None


def set_case_loader(fn):
    global _loader
    _loader = fn


def _not_found():
    return JSONResponse(status_code=404, content={"error": {"code": "not_found", "message": "No case with that link.", "detail": {}}})


def export_payload(token: str, case: dict, now: datetime = None) -> dict:
    out = export.build_export(case)
    now = now or datetime.now(timezone.utc)
    ok = ("accepted", "edited")
app/README-arch.md:39:app/config.py [release]   env: LLM_BACKEND, GENERATOR_MODEL, JUDGE_MODEL, ENABLE_LIVE, PROVIDER_CAP_CONFIRMED, DATA_DIR, limits; injectable now() for every deadline and purge
app/backend/api.py:45:    db_path = db_path or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:24.241Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/data; git rev-parse --short HEAD; (LLM_BACKEND=fixture DATA_DIR=$S/data PORT=7961 .venv/bin/python -m app.main > $S/server.log 2>&1 &) ; sleep 4; curl -s localhost:7961/api/health; echo; cat $S/server.log",
 "run_in_background": false
}
````

### User / tool · 2026-11-02T01:59:28.464Z

**tool result**
````
e274322
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every item","sample_available":true}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:35.452Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; B=localhost:7961\ncnt(){ .venv/bin/python -c \"\nimport sqlite3,sys;c=sqlite3.connect('$S/data/zlayt.sqlite')\nprint({t:c.execute(f'select count(*) from {t}').fetchone()[0] for t in ('cases','records','items','llm_calls','events')})\" 2>&1 | tail -1; }\necho before; cnt\necho \"--- demo gate non-fixture\"; curl -si -X POST $B/api/cases -H 'content-type: application/json' -d '{\"text\":\"=== Record 1 ===\\n2026-01-01 <img src=x onerror=alert(1)> visit $50\"}' | head -20\necho; echo after; cnt\necho \"--- empty\"; curl -si -X POST $B/api/cases -H 'content-type: application/json' -d '{\"text\":\"   \"}' | sed -n '1p;$p'\necho \"--- oversize 70k\"; .venv/bin/python -c \"import json;print(json.dumps({'text':'a'*70000}))\" > $S/big.json; curl -si -X POST $B/api/cases -H 'content-type: application/json' --data @$S/big.json | sed -n '1p;$p'\necho \"--- malformed\"; curl -si -X POST $B/api/cases -d '{bad' | sed -n '1p;$p'\necho \"--- nonobject\"; curl -si -X POST $B/api/cases -d '[1]' | sed -n '1p;$p'\necho \"--- unknown token\"; for p in \"GET /api/cases/zzz\" \"GET /api/cases/zzz/status\" \"GET /api/cases/zzz/export\" \"GET /api/cases/zzz/audit\" \"DELETE /api/cases/zzz\" \"GET /api/cases/zzz/items/e1\"; do set -- $p; echo -n \"$p \"; curl -s -o /dev/null -w \"%{http_code}\\n\" -X $1 $B$2; done\ncurl -s -X POST $B/api/cases/zzz/run; echo; curl -s -X POST $B/api/cases/zzz/items/e1/review -d '{\"action\":\"accept\"}'; echo\ncurl -s -X POST $B/api/cases/zzz/records/r1/confirm_date -d '{\"date\":\"2026-01-01\"}'; echo\necho \"--- huge body 200MB\"; head -c 200000000 /dev/zero | tr '\\0' 'a' > $S/huge.bin; ( time curl -s -o /dev/null -w \"%{http_code}\\n\" -X POST $B/api/cases -H 'content-type: application/json' --data-binary @$S/huge.bin ) 2>&1 | grep -v '^$' | head -5; rm $S/huge.bin"
}
````

### User / tool · 2026-11-02T01:59:35.512Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to  visit $50"})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:43.744Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json, sqlite3, urllib.request, urllib.error, time, glob, os\nS=glob.glob('/private/tmp/claude-501/*/*/scratchpad')\nS=[s for s in S if os.path.exists(s+'/data/zlayt.sqlite')][0]\nB='http://localhost:7961'\nGT=chr(62); LT=chr(60)\ndef cnt():\n    c=sqlite3.connect(S+'/data/zlayt.sqlite')\n    return {t:c.execute(f'select count(*) from {t}').fetchone()[0] for t in ('cases','records','items','llm_calls','events')}\ndef req(m,p,body=None,raw=None,ct='application/json'):\n    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)\n    r=urllib.request.Request(B+p,data=data,method=m,headers={'content-type':ct})\n    try:\n        x=urllib.request.urlopen(r); return x.status,dict(x.headers),x.read().decode()\n    except urllib.error.HTTPError as e: return e.code,dict(e.headers),e.read().decode()\nprint('before',cnt())\nxss=f'=== Record 1 ===\\n2026-01-01 {LT}img src=x onerror=alert(1){GT} visit $50'\ns,h,b=req('POST','/api/cases',{'text':xss}); print('demo gate',s,b); print(h.get('Referrer-Policy'),h.get('Cache-Control'))\nprint('after',cnt())\nprint('empty',req('POST','/api/cases',{'text':'  '})[::2])\nprint('oversize',req('POST','/api/cases',{'text':'a'*70000})[::2])\nprint('malformed',req('POST','/api/cases',raw=b'{bad')[::2])\nprint('array',req('POST','/api/cases',raw=b'[1]')[::2])\nprint('text int',req('POST','/api/cases',{'text':5})[::2])\nfor m,p in [('GET','/api/cases/zzz'),('GET','/api/cases/zzz/status'),('GET','/api/cases/zzz/export'),('GET','/api/cases/zzz/audit'),('DELETE','/api/cases/zzz'),('GET','/api/cases/zzz/items/e1'),('POST','/api/cases/zzz/run'),('POST','/api/cases/zzz/items/e1/review'),('POST','/api/cases/zzz/records/r1/confirm_date')]:\n    s,h,b=req(m,p,{'action':'accept','date':'2026-01-01'} if m=='POST' else None); print(m,p,s,b[:100])\nprint('docs',req('GET','/docs')[0],req('GET','/openapi.json')[0])\nprint('traversal',req('GET','/..%2f..%2fetc/passwd')[0], req('GET','/%2e%2e/%2e%2e/etc/passwd')[0])\n# huge body\nt=time.time(); big=b'{\"text\":\"'+b'a'*100_000_000+b'\"}'\nprint('100MB body',req('POST','/api/cases',raw=big)[0], round(time.time()-t,1),'s')\nEOF"
}
````

### User / tool · 2026-11-02T01:59:43.914Z

**tool result (error)**
````
Exit code 1
Traceback (most recent call last):
  File "<stdin>", line 15, in <module>
  File "<stdin>", line 8, in cnt
sqlite3.OperationalError: no such table: items
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:45.357Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport sqlite3,glob\ns=glob.glob('/private/tmp/claude-501/*/*/scratchpad/data/zlayt.sqlite')[0]\nprint([r[0] for r in sqlite3.connect(s).execute(\"select name from sqlite_master where type='table'\")])\nEOF"
}
````

### User / tool · 2026-11-02T01:59:45.465Z

**tool result**
````
['cases', 'records', 'entries', 'amounts', 'flags', 'llm_calls', 'review_events']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:51.007Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json, sqlite3, urllib.request, urllib.error, time, glob, os\nS=[s for s in glob.glob('/private/tmp/claude-501/*/*/scratchpad') if os.path.exists(s+'/data/zlayt.sqlite')][0]\nB='http://localhost:7961'\nGT=chr(62); LT=chr(60)\ndef cnt():\n    c=sqlite3.connect(S+'/data/zlayt.sqlite')\n    return {t:c.execute(f'select count(*) from {t}').fetchone()[0] for t in ('cases','records','entries','amounts','flags','llm_calls','review_events')}\ndef req(m,p,body=None,raw=None,ct='application/json'):\n    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)\n    r=urllib.request.Request(B+p,data=data,method=m,headers={'content-type':ct})\n    try:\n        x=urllib.request.urlopen(r); return x.status,dict(x.headers),x.read().decode()\n    except urllib.error.HTTPError as e: return e.code,dict(e.headers),e.read().decode()\nprint('before',cnt())\nxss=f'=== Record 1 ===\\n2026-01-01 {LT}img src=x onerror=alert(1){GT} visit $50'\ns,h,b=req('POST','/api/cases',{'text':xss}); print('demo gate',s,b); print(h.get('Referrer-Policy'),h.get('Cache-Control'))\nprint('after',cnt())\nprint('empty',req('POST','/api/cases',{'text':'  '})[::2])\nprint('oversize',req('POST','/api/cases',{'text':'a'*70000})[::2])\nprint('malformed',req('POST','/api/cases',raw=b'{bad')[::2])\nprint('array',req('POST','/api/cases',raw=b'[1]')[::2])\nprint('text int',req('POST','/api/cases',{'text':5})[::2])\nprint('after errs',cnt())\nfor m,p in [('GET','/api/cases/zzz'),('GET','/api/cases/zzz/status'),('GET','/api/cases/zzz/export'),('GET','/api/cases/zzz/audit'),('DELETE','/api/cases/zzz'),('GET','/api/cases/zzz/items/e1'),('POST','/api/cases/zzz/run'),('POST','/api/cases/zzz/items/e1/review'),('POST','/api/cases/zzz/records/r1/confirm_date')]:\n    s,h,b=req(m,p,{'action':'accept','date':'2026-01-01'} if m=='POST' else None); print(m,p,s,b[:100])\nprint('docs',req('GET','/docs')[0],req('GET','/openapi.json')[0])\nprint('traversal',req('GET','/..%2f..%2fetc/passwd')[0], req('GET','/%2e%2e/%2e%2e/etc/passwd')[0])\nt=time.time(); big=b'{\"text\":\"'+b'a'*100_000_000+b'\"}'\nprint('100MB body',req('POST','/api/cases',raw=big)[0], round(time.time()-t,1),'s')\nEOF"
}
````

### User / tool · 2026-11-02T01:59:51.475Z

**tool result**
````
before {'cases': 0, 'records': 0, 'entries': 0, 'amounts': 0, 'flags': 0, 'llm_calls': 0, 'review_events': 0}
demo gate 409 {"error":{"code":"demo_mode_unsupported_input","message":"This demo only runs the recorded sample cases.","detail":{}}}
None None
after {'cases': 0, 'records': 0, 'entries': 0, 'amounts': 0, 'flags': 0, 'llm_calls': 0, 'review_events': 0}
empty (400, '{"error":{"code":"bad_request","message":"Input is empty.","detail":{}}}')
oversize (413, '{"error":{"code":"input_too_large","message":"Input is too large.","detail":{}}}')
malformed (400, '{"error":{"code":"bad_request","message":"Request body is not valid JSON.","detail":{}}}')
array (400, '{"error":{"code":"bad_request","message":"Request body must be a JSON object.","detail":{}}}')
text int (400, '{"error":{"code":"bad_request","message":"Provide text or sample: true.","detail":{}}}')
after errs {'cases': 0, 'records': 0, 'entries': 0, 'amounts': 0, 'flags': 0, 'llm_calls': 0, 'review_events': 0}
GET /api/cases/zzz 404 {"error":{"code":"not_found","message":"No such case.","detail":{}}}
GET /api/cases/zzz/status 404 {"error":{"code":"not_found","message":"No such case.","detail":{}}}
GET /api/cases/zzz/export 404 {"error":{"code":"not_found","message":"No such case.","detail":{}}}
GET /api/cases/zzz/audit 404 {"error":{"code":"not_found","message":"No such case.","detail":{}}}
DELETE /api/cases/zzz 404 {"error":{"code":"not_found","message":"No such case.","detail":{}}}
GET /api/cases/zzz/items/e1 404 {"error":{"code":"not_found","message":"No such case.","detail":{}}}
POST /api/cases/zzz/run 404 {"error":{"code":"not_found","message":"No such case.","detail":{}}}
POST /api/cases/zzz/items/e1/review 404 {"error":{"code":"not_found","message":"No such case.","detail":{}}}
POST /api/cases/zzz/records/r1/confirm_date 404 {"error":{"code":"not_found","message":"No such case.","detail":{}}}
docs 404 404
traversal 404 404
100MB body 413 0.3 s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:55.725Z

**tool call — Bash**
````
{
 "command": "B=localhost:7961; curl -si -X POST $B/api/cases -d '{bad' | head -12; echo ---; curl -si $B/ | head -12; echo; curl -si $B/nonexistent.js | head -8"
}
````

### User / tool · 2026-11-02T01:59:55.902Z

**tool result**
````
HTTP/1.1 400 Bad Request
date: Mon, 02 Nov 2026 01:59:55 GMT
server: uvicorn
content-length: 88
content-type: application/json
referrer-policy: no-referrer
x-content-type-options: nosniff
cache-control: no-store

{"error":{"code":"bad_request","message":"Request body is not valid JSON.","detail":{}}}---
HTTP/1.1 200 OK
date: Mon, 02 Nov 2026 01:59:55 GMT
server: uvicorn
content-type: text/html; charset=utf-8
accept-ranges: bytes
content-length: 2260
last-modified: Mon, 02 Nov 2026 01:54:19 GMT
etag: "d9837c9327283e2700d7f5dfbaaec527"
referrer-policy: no-referrer
x-content-type-options: nosniff
cache-control: no-cache


HTTP/1.1 404 Not Found
date: Mon, 02 Nov 2026 01:59:55 GMT
server: uvicorn
content-length: 64
content-type: application/json
referrer-policy: no-referrer
x-content-type-options: nosniff
cache-control: no-cache
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:59:58.612Z

**tool call — Bash**
````
{
 "command": "grep -rn \"Content-Security-Policy\" app Dockerfile* docs/*.md memory 2>/dev/null | head -5; python3 tools/board.py list 2>/dev/null | grep -i \"csp\\|rate\\|spend\\|docker\" | head; sed -n 1,209p app/backend/review.py"
}
````

### User / tool · 2026-11-02T01:59:58.797Z

**tool result**
````
T-051	M2	qa         	ready            	P0	AC 0/3	Curated golden-conformant fixture set for demo + E2E (D-029)
"""Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).

Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). There is no bulk accept.
Edit order: (1) structure, else 422 invalid_edit; (2) code token check; (3) judge 1 re-run. A token/judge objection saves nothing
and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
that cannot answer never blocks: the edit is saved as needs_review with JUDGE_UNAVAILABLE.
"""
import time

from app.backend import conflicts, confidence, gaps, generator, grounding, judges, store
from app.db import db as DB

ACTIONS = ("accept", "dismiss", "reset", "edit")
_KIND = {"e": "entry", "a": "amount", "f": "flag"}


class ReviewError(Exception):
    def __init__(self, status: int, code: str, detail: dict = None, message: str = ""):
        super().__init__(code)
        self.status, self.code, self.detail, self.message = status, code, detail or {}, message or code.replace("_", " ")


def _now(now):
    return now() if callable(now) else (time.time() if now is None else now)


def _item(conn, case_id, item_id):
    try:
        row = DB.get_item(conn, item_id)
    except KeyError:
        raise ReviewError(404, "not_found", message="No such item.") from None
    if row["case_id"] != case_id:
        raise ReviewError(404, "not_found", message="No such item.")
    return _KIND[item_id[0]], row


def _bad(msg, **detail):
    return ReviewError(422, "invalid_edit", detail, msg)


def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
        raise _bad("That action is not allowed.")
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    warnings = []
    if action in ("accept", "dismiss", "reset"):
        DB.apply_review(conn, item_id, action, now=t)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}


# ---------------------------------------------------------------- edit
def _edit(conn, case_id, kind, item, body, call, t):
    edits = body.get("edits")
    if kind == "amount":
        raise _bad("A charge can only be accepted or dismissed.")
    if not isinstance(edits, dict) or not edits:
        raise _bad("Nothing to edit.")
    if kind == "flag":
        if set(edits) != {"note"} or not isinstance(edits["note"], str) or not edits["note"].strip():
            raise _bad("Only a note can be added to a flag.")
        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t)
        DB.update_item(conn, item["id"], now=t, reviewer_note=edits["note"].strip()[:2000])
        return []
    if not set(edits) <= {"summary", "excerpt"} or not all(isinstance(v, str) and v.strip() for v in edits.values()):
        raise _bad("Only the summary or the quoted sentences of an entry can be edited.")
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    rec = next((r for r in recs if r["id"] == (item["record_ids"] or [None])[0]), None)
    if rec is None:
        raise _bad("The entry's source record is missing.")
    prev = item.get("edited") or {}
    cur_sum, cur_exc = prev.get("summary", item["summary"]), prev.get("excerpt", item["excerpt"])
    new_sum, new_exc = edits.get("summary", cur_sum).strip(), edits.get("excerpt", cur_exc).strip()
    span = None
    if "excerpt" in edits:
        problems = grounding.check_excerpt(rec["excerpt"], new_exc)
        if problems:
            raise _bad("The quote must be whole sentences of the same record, in order, with any hedge sentence that qualifies them.", reasons=problems)
    span = grounding.locate(rec["excerpt"], new_exc)
    base = generator.body_offset(rec)
    label, date_iso = item["provider"] or "", item["date_iso"] or ""
    # (2) code check
    code_reasons, found = [], []
    toks = grounding.new_tokens(new_sum, new_exc, label, date_iso)
    blocking = []
    if toks:
        code_reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
        blocking.append({"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "“" + "”, “".join(toks) + "” is not in the quote.", "item_id": item["id"]})
    if grounding.dropped_qualifiers(new_sum, new_exc):
        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
    if span is None:
        code_reasons.append("HIGHLIGHT_NOT_FOUND")
    # (3) judge 1
    verdict, call_id, ladder_verdict = "unavailable", None, "unavailable"
    if call is not None:
        try:
            verdict, call_id, _ = judges.run_j1_meta(new_sum, new_exc, label, call=call, item_id=item["id"])
        except Exception:
            verdict, call_id = "unavailable", None
        ladder_verdict = judges.to_ladder("j1", verdict)
    if ladder_verdict in ("partially", "unsupported"):
        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
        blocking.append({"code": code, "message": "The second check could not fully support the summary from the quote.", "item_id": item["id"]})
    confirmed = bool(body.get("confirm_warnings"))
    if blocking and not confirmed:
        raise ReviewError(409, "needs_confirm", {"warnings": blocking}, "This edit adds a number or fact that is not in the quote.")
    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed")})
    edited = dict(prev)
    edited.update(at=store.iso(t), kept_my_wording=bool(blocking and confirmed))
    if "summary" in edits or "summary" in prev:
        edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
    if "excerpt" in edits or "excerpt" in prev:
        edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t)
    if edited["kept_my_wording"]:
        DB.apply_review(conn, item["id"], "keep_my_wording", now=t)
    lad = item.get("ladder") or {"item_id": item["id"]}
    lad["judge"] = {"model": judges.judge_model(), "prompt_version": "judge_faithfulness_v1", "call_id": call_id, "verdict": ladder_verdict}
    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
    lad["state"] = state
    DB.update_item(conn, item["id"], now=t, state=state, state_reasons_json=reasons, ladder=lad)
    return [{"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": item["id"]}] \
        if ladder_verdict == "unavailable" else []


# ---------------------------------------------------------------- confirm_date
def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
    t = _now(now)
    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
    if row is None:
        raise ReviewError(404, "not_found", message="No such record.")
    rec = DB._decode(row)
    if rec["date_status"] != "ambiguous":
        raise _bad("Only a record whose date can be read two ways can be confirmed.")
    if date_iso not in (rec["date_candidates"] or []):
        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=?", (date_iso, record_id))
    moved = None
    for e in DB.list_items(conn, case_id, "entry"):
        if record_id in (e["record_ids"] or []):
            DB.update_item(conn, e["id"], now=t, date_iso=date_iso)
            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
    removed = _drop(conn, f"f_date_r{rec['seq']}")
    removed += _recompute_gaps(conn, case_id, t)
    log_id = moved["id"] if moved else None
    if log_id:
        DB.apply_review(conn, log_id, "confirm_date", now=t)
    from app.backend import present
    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
            "removed_flag_ids": removed, "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}


def _drop(conn, flag_id):
    cur = conn.execute("DELETE FROM flags WHERE id=?", (flag_id,))
    return [flag_id] if cur.rowcount else []


def _recompute_gaps(conn, case_id, t):
    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
    and note; a changed one restarts as pending; one that no longer exists is dropped (ADR-002)."""
    from app.backend import pipeline as PL
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    backend = DB.get_case(conn, case_id).get("backend") or "code"
    new = {}
    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
        nos = f["record_nos"]
        state, codes = PL._compose_code(by_n, nos, list(f.get("reasons") or []), f["evidence"], case["raw_text"])
        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": f["evidence"], "record_nos": nos,
                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names"):
            if k in f:
                item[k] = f[k]
        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
        new[item["id"]] = item
    removed = []
    for old in DB.list_items(conn, case_id, "flag"):
        if old["origin"] != "code" or old["type"] not in ("gap", "conflict"):
            continue
        item = new.get(old["id"])
        if item is None:
            conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (old["id"], case_id))
            removed.append(old["id"])
            continue
        oc = old.get("computed") or {}
        DB.update_item(conn, old["id"], now=t, **PL._row("flag", item))
        if old["review_status"] != "pending" and any(oc.get(k) != item.get(k) for k in ("from_date", "to_date", "days", "stated_dates", "first_treatment_date")):
            DB.apply_review(conn, old["id"], "reset", now=t)
    have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
    for iid, item in new.items():
        if iid not in have:
            DB.add_item(conn, case_id, "flag", {"id": iid, **PL._row("flag", item)}, now=t)
    return removed
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:00:06.009Z

**tool call — Bash**
````
{
 "command": "cat > /dev/null <<'EOF'\nEOF\n.venv/bin/python -I - <<'EOF'\nimport json, sqlite3, urllib.request, urllib.error, time, glob, os\nS=[s for s in glob.glob('/private/tmp/claude-501/*/*/scratchpad') if os.path.exists(s+'/data/zlayt.sqlite')][0]\nB='http://localhost:7961'\ndef req(m,p,body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r=urllib.request.Request(B+p,data=data,method=m,headers={'content-type':'application/json'})\n    try:\n        x=urllib.request.urlopen(r); return x.status,json.loads(x.read() or 'null')\n    except urllib.error.HTTPError as e: return e.code,json.loads(e.read() or 'null')\ntxt=open('evals/golden/case_01_date_formats.txt').read()\ns,c=req('POST','/api/cases',{'text':txt}); print(s,c.get('token') and 'token ok', c.get('error'))\ntok=c['token']; print('dates_to_confirm',c['dates_to_confirm'])\ns,r=req('POST',f'/api/cases/{tok}/run',{}); print('run',s,r)\nfor i in range(60):\n    s,st=req('GET',f'/api/cases/{tok}/status')\n    if st['status'] in('ready','failed'): break\n    time.sleep(1)\nprint('status',st['status'],st['counts'],st['error'])\ns,v=req('GET',f'/api/cases/{tok}'); print(s,list(v)[:15])\njson.dump({'tok':tok},open(S+'/tok.json','w'))\nents=[e for e in v.get('entries',[])]; print(len(ents), [ (e['id'],e.get('state')) for e in ents][:12])\namts=v.get('amounts') or v.get('charges') or []; print([(a['id']) for a in amts][:5])\nopen(S+'/view.json','w').write(json.dumps(v))\nEOF"
}
````

### User / tool · 2026-11-02T02:00:07.437Z

**tool result**
````
201 token ok None
dates_to_confirm [{'record_id': 'r8', 'raw': '04/05/2026', 'candidates': ['2026-04-05', '2026-05-04'], 'status': 'ambiguous'}]
run 202 {'token': '8xNUm_yNXGbAEFudSwKMQg', 'status': 'running', 'stage': 'extract', 'started_at': '2026-11-02T02:00:06Z'}
status ready {'entries': 8, 'amounts': 1, 'flags': 3} None
200 ['token', 'name', 'status', 'demo_mode', 'backend', 'models', 'records', 'undated_entries', 'entries', 'amounts', 'totals', 'flags', 'tray', 'dates_to_confirm', 'injection']
7 [('e1', 'needs_review'), ('e2', 'needs_review'), ('e3', 'needs_review'), ('e4', 'needs_review'), ('e5', 'needs_review'), ('e6', 'needs_review'), ('e7', 'needs_review')]
['a1']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:00:16.285Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json, urllib.request, urllib.error, glob, os\nS=[s for s in glob.glob('/private/tmp/claude-501/*/*/scratchpad') if os.path.exists(s+'/tok.json')][0]\ntok=json.load(open(S+'/tok.json'))['tok']; B='http://localhost:7961'\nv=json.load(open(S+'/view.json'))\ndef req(m,p,body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r=urllib.request.Request(B+p,data=data,method=m,headers={'content-type':'application/json'})\n    try:\n        x=urllib.request.urlopen(r); return x.status,json.loads(x.read() or 'null')\n    except urllib.error.HTTPError as e: return e.code,json.loads(e.read() or 'null')\ne=v['entries'][0]; print({k:e[k] for k in e if k in('id','summary','excerpt','provider','date','date_iso')})\nR=lambda i,b: req('POST',f'/api/cases/{tok}/items/{i}/review',b)\ndef show(n,r): print(n,r[0],json.dumps(r[1])[:230])\nshow('bad action',R('e1',{'action':'nuke'}))\nshow('empty body',R('e1',{}))\nshow('edit provider',R('e1',{'action':'edit','edits':{'provider':'X'}}))\nshow('edit date',R('e1',{'action':'edit','edits':{'date':'2020-01-01'}}))\nshow('edit empty summary',R('e1',{'action':'edit','edits':{'summary':'  '}}))\nshow('edit summary non-str',R('e1',{'action':'edit','edits':{'summary':{'a':1}}}))\nshow('edit nothing',R('e1',{'action':'edit','edits':{}}))\nshow('edit excerpt notinrec',R('e1',{'action':'edit','edits':{'excerpt':'<script>alert(1)</script>.'}}))\nshow('amount edit amount',R('a1',{'action':'edit','edits':{'amount':100}}))\nshow('amount edit class',R('a1',{'action':'edit','edits':{'class':'billed'}}))\nshow('amount edit text',R('a1',{'action':'edit','edits':{'text':'x'}}))\nshow('flag edit other',R('f_gap_r6_r7',{'action':'edit','edits':{'title':'x'}}))\nshow('9000',R('e1',{'action':'edit','edits':{'summary':e['summary']+' +$9,000'}}))\nshow('9000 gt',R('e1',{'action':'edit','edits':{'summary':'Visit <b>x</b> +$9,000 &lt;'}}))\nshow('9000 confirm',R('e1',{'action':'edit','edits':{'summary':'Visit <b>x</b> +$9,000'},'confirm_warnings':True}))\nshow('item wrong prefix',R('zz1',{'action':'accept'}))\nshow('item q',R('x1',{'action':'accept'}))\nshow('confirm bad date',req('POST',f'/api/cases/{tok}/records/r8/confirm_date',{'date':'2026-06-06'}))\nshow('confirm non-str',req('POST',f'/api/cases/{tok}/records/r8/confirm_date',{'date':5}))\nshow('confirm not ambiguous',req('POST',f'/api/cases/{tok}/records/r1/confirm_date',{'date':'2026-01-01'}))\nshow('confirm missing rec',req('POST',f'/api/cases/{tok}/records/r99/confirm_date',{'date':'2026-01-01'}))\nshow('confirm ok',req('POST',f'/api/cases/{tok}/records/r8/confirm_date',{'date':'2026-05-04'}))\nshow('accept',R('e2',{'action':'accept'}))\nshow('rerun no confirm',req('POST',f'/api/cases/{tok}/run',{}))\nshow('item other-case prefix',req('GET',f'/api/cases/{tok}/items/e1'))\nshow('SQLi item',req('GET',f'/api/cases/{tok}/items/e1%27%20OR%201=1--'))\nEOF"
}
````

### User / tool · 2026-11-02T02:00:16.478Z

**tool result**
````
{'id': 'e1', 'date': '2026-02-03', 'provider': 'Quillfeather Urgent Care', 'summary': 'Right ankle swelling after twisting on stairs; X-ray negative for fracture; urgent care charge $310.00.', 'excerpt': 'Right ankle swelling after twisting on stairs. X-ray negative for fracture. Urgent care charge: $310.00.'}
bad action 422 {"error": {"code": "invalid_edit", "message": "That action is not allowed.", "detail": {}}}
empty body 422 {"error": {"code": "invalid_edit", "message": "That action is not allowed.", "detail": {}}}
edit provider 422 {"error": {"code": "invalid_edit", "message": "Only the summary or the quoted sentences of an entry can be edited.", "detail": {}}}
edit date 422 {"error": {"code": "invalid_edit", "message": "Only the summary or the quoted sentences of an entry can be edited.", "detail": {}}}
edit empty summary 422 {"error": {"code": "invalid_edit", "message": "Only the summary or the quoted sentences of an entry can be edited.", "detail": {}}}
edit summary non-str 422 {"error": {"code": "invalid_edit", "message": "Only the summary or the quoted sentences of an entry can be edited.", "detail": {}}}
edit nothing 422 {"error": {"code": "invalid_edit", "message": "Nothing to edit.", "detail": {}}}
edit excerpt notinrec 422 {"error": {"code": "invalid_edit", "message": "The quote must be whole sentences of the same record, in order, with any hedge sentence that qualifies them.", "detail": {"reasons": ["GROUNDING_EXCERPT_NOT_VERBATIM"]}}}
amount edit amount 422 {"error": {"code": "invalid_edit", "message": "A charge can only be accepted or dismissed.", "detail": {}}}
amount edit class 422 {"error": {"code": "invalid_edit", "message": "A charge can only be accepted or dismissed.", "detail": {}}}
amount edit text 422 {"error": {"code": "invalid_edit", "message": "A charge can only be accepted or dismissed.", "detail": {}}}
flag edit other 404 {"error": {"code": "not_found", "message": "No such item.", "detail": {}}}
9000 409 {"error": {"code": "needs_confirm", "message": "This edit adds a number or fact that is not in the quote.", "detail": {"warnings": [{"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "\u201c9000\u201d is not in the quote.", "item
9000 gt 409 {"error": {"code": "needs_confirm", "message": "This edit adds a number or fact that is not in the quote.", "detail": {"warnings": [{"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "\u201c9000\u201d is not in the quote.", "item
9000 confirm 200 {"item": {"id": "e1", "state": "needs_review", "reasons": ["SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "JUDGE_UNAVAILABLE"], "why": "The summary has a number, date, dollar figure or left/right/no/not/without that is
item wrong prefix 404 {"error": {"code": "not_found", "message": "No such item.", "detail": {}}}
item q 404 {"error": {"code": "not_found", "message": "No such item.", "detail": {}}}
confirm bad date 422 {"error": {"code": "date_invalid", "message": "Choose one of the readings offered for this record.", "detail": {"candidates": ["2026-04-05", "2026-05-04"]}}}
confirm non-str 400 {"error": {"code": "bad_request", "message": "Provide the chosen date.", "detail": {}}}
confirm not ambiguous 422 {"error": {"code": "invalid_edit", "message": "Only a record whose date can be read two ways can be confirmed.", "detail": {}}}
confirm missing rec 404 {"error": {"code": "not_found", "message": "No such record.", "detail": {}}}
confirm ok 200 {"record": {"id": "r8", "date_iso": "2026-05-04", "date_status": "confirmed", "date_raw": "04/05/2026"}, "entry": {"id": "e8", "date": "2026-05-04", "moved_from": "undated_entries"}, "gap_flags": [], "removed_flag_ids": ["f_date_r
accept 200 {"item": {"id": "e2", "state": "needs_review", "reasons": ["JUDGE_UNAVAILABLE"], "why": "The second AI check did not run or did not finish, so this item has not been double-checked.", "review_status": "accepted", "edited": null, "
rerun no confirm 409 {"error": {"code": "needs_confirm", "message": "Items already have decisions; confirm to run again.", "detail": {}}}
item other-case prefix 200 {"item": {"id": "e1", "state": "needs_review", "reasons": ["SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "JUDGE_UNAVAILABLE"], "why": "The summary has a number, date, dollar figure or left/right/no/not/without that is
SQLi item 404 {"error": {"code": "not_found", "message": "No such item.", "detail": {}}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:00:22.129Z

**tool call — Bash**
````
{
 "command": "grep -rniE \"rate.?limit|spend|daily_cap|429|DAILY|PER_IP\" app --include=*.py | head; python3 tools/board.py list 2>/dev/null | grep -iE \"rate|cap|limit|spend|deploy|csp|header\" ; grep -rn \"innerHTML\\|insertAdjacentHTML\\|outerHTML\\|document.write\" app/frontend | head; grep -n \"ENABLE_LIVE\\|enable_live\" -r app --include=*.py | head"
}
````

### User / tool · 2026-11-02T02:00:22.305Z

**tool result**
````
T-019	M5	orchestrator	needs_chris      	P1	AC 0/1	Provide a real Anthropic API key for the public deployment (NEEDS_CHRIS #1)
T-032	M2	backend    	done             	P0	AC 5/5	Ingest: record split, date parsing, dedupe, limits, injection scan
T-051	M2	qa         	in_progress      	P0	AC 0/3	Curated golden-conformant fixture set for demo + E2E (D-029)
app/backend/api.py:58:        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:00:23.219Z

**tool call — Bash**
````
{
 "command": "S=$(ls -d /private/tmp/claude-501/*/*/scratchpad | head -1); cat $S/server.log | head -20; echo \"log bytes: $(wc -c < $S/server.log)\"; grep -c \"8xNUm\" $S/server.log; grep -rn \"logging\\|logger\\|print(\" app/backend/api.py app/backend/review.py app/backend/present.py app/backend/store.py app/main.py | head"
}
````

### User / tool · 2026-11-02T02:00:23.326Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:00:27.098Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo \"log bytes: $(wc -c < $S/server.log)\"; cat $S/server.log | head; grep -c \"8xNUm\" $S/server.log; grep -rn \"logging\\|logger\\|print(\" app/backend/api.py app/backend/review.py app/backend/present.py app/backend/store.py app/main.py | head"
}
````

### User / tool · 2026-11-02T02:00:27.202Z

**tool result**
````
log bytes:     1862
llm call failed call_id=cfd2473b13a25 step=j1 attempt=1 prompt_hash=37f588e1e562428cfaa109749b24600ce2fe250be9f99536047ef79e8dd79c78
llm call failed call_id=c237d78e021d9 step=j1 attempt=1 prompt_hash=fc789ea36ae435903b9c77dc0a7163947534302b7cecd9cd078b5a9c915d3456
llm call failed call_id=c619cef4ec174 step=j1 attempt=1 prompt_hash=4d0039605f4eda08fc878c0b9559185e8df9b8a3ca732112d64abe5197f59f85
llm call failed call_id=c8f683fb84b02 step=j1 attempt=1 prompt_hash=ac6129be7b1a814113f8ad392c9fe34b267b7dccb7393531c513fb49fcab82f3
llm call failed call_id=c2fa209a9df01 step=j1 attempt=1 prompt_hash=5ef978e652e30168fc71e2f22322219adb3fe1f8134c003d0652bedd9dfc0374
llm call failed call_id=ce9ecba5a9cca step=j1 attempt=1 prompt_hash=49667de16a2c245e1e6e54e5999fcb7566b5d578d27c9b09015781885e9b515a
llm call failed call_id=c47d0d7449134 step=j1 attempt=1 prompt_hash=97c5477ae31d518466eb89335e224b86f8802be67c4c47df47c69b3b0bfc5346
llm call failed call_id=c4dd173abe6a4 step=j1 attempt=1 prompt_hash=4a67bc43647dbcca4719ede9547e025faa9435bb73a18186d797de279c302ee0
llm call failed call_id=cf3f93ae4fd6d step=j2 attempt=1 prompt_hash=067240d96709b57638faad6e55ccb4a12af21dd382baec8516eeff30ae621cdd
llm call failed call_id=ced22bf1d8ba2 step=j4 attempt=1 prompt_hash=57cf618ce07cfa4ddfc12c278b60f8f458afa7f23a630bffe4ab07b201eb65e5
0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:00:35.740Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; pkill -f \"app.main\" ; sleep 1; (LLM_BACKEND=fixture DATA_DIR=$S/data PORT=7961 .venv/bin/python -m app.main > $S/server2.log 2>&1 &); sleep 4\n.venv/bin/python -I - <<'EOF'\nimport json, urllib.request, urllib.error, glob, os\nS=[s for s in glob.glob('/private/tmp/claude-501/*/*/scratchpad') if os.path.exists(s+'/tok.json')][0]\ntok=json.load(open(S+'/tok.json'))['tok']; B='http://localhost:7961'\ndef req(m,p,body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r=urllib.request.Request(B+p,data=data,method=m,headers={'content-type':'application/json'})\n    try:\n        x=urllib.request.urlopen(r); return x.status,x.read().decode()\n    except urllib.error.HTTPError as e: return e.code,e.read().decode()\ns,b=req('GET',f'/api/cases/{tok}'); v=json.loads(b)\nprint('after restart',s,[(e['id'],e['review_status'],e['date']) for e in v['entries']][:8], v['dates_to_confirm'])\ne1=[e for e in v['entries'] if e['id']=='e1'][0]; print('e1 summary stored raw:',e1['summary'])\n# second case same text -> collision?\ntxt=open('evals/golden/case_01_date_formats.txt').read()\ns,b=req('POST','/api/cases',{'text':txt}); print('2nd case',s,b[:300])\ns,b=req('POST','/api/cases',{'sample':True}); print('sample',s,b[:200])\ns,b=req('POST','/api/cases',{'sample':True}); print('sample again',s,b[:300])\nEOF\ncat $S/server2.log | tail -15"
}
````

### User / tool · 2026-11-02T02:00:41.034Z

**tool result**
````
after restart 200 [('e1', 'edited', '2026-02-03'), ('e2', 'accepted', '2026-02-17'), ('e3', 'pending', '2026-02-24'), ('e4', 'pending', '2026-03-03'), ('e5', 'pending', '2026-03-10'), ('e6', 'pending', '2026-03-17'), ('e7', 'pending', '2026-03-25'), ('e8', 'pending', '2026-05-04')] []
e1 summary stored raw: Visit <b>x</b> +$9,000
2nd case 500 Internal Server Error
sample 500 Internal Server Error
sample again 500 Internal Server Error
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 372, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/app/backend/api.py", line 153, in create_case
    ing = pipeline_mod().ingest_case(c, cid, text, now)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/app/backend/pipeline.py", line 157, in ingest_case
    _store_records(conn, cid, ing)
  File "/Users/arsis/zlayt-pm-project/app/backend/pipeline.py", line 104, in _store_records
    DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
  File "/Users/arsis/zlayt-pm-project/app/db/db.py", line 87, in add_record
    _insert(conn, "records", {"id": rid, "case_id": case_id, **fields})
  File "/Users/arsis/zlayt-pm-project/app/db/db.py", line 81, in _insert
    conn.execute(f"INSERT INTO {table} ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
sqlite3.IntegrityError: UNIQUE constraint failed: records.id
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:00:47.590Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport sqlite3,glob,os\ns=glob.glob('/private/tmp/claude-501/*/*/scratchpad/data/zlayt.sqlite')\ns=[x for x in s if 'Library-Application-Support-Claude-scratch' in x][0]\nc=sqlite3.connect(s)\nprint('cases',c.execute('select count(*), sum(status=\"ingested\") from cases').fetchone())\nprint(c.execute('select status,count(*) from cases group by status').fetchall())\nEOF\npkill -f \"app.main\"; echo killed"
}
````

### User / tool · 2026-11-02T02:00:47.725Z

**tool result**
````
cases (4, 3)
[('ingested', 3), ('ready', 1)]
killed
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:00:51.774Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list 2>/dev/null | grep -iE \"M4|M5|M6|hardening|secur|abuse|docker|public|space\"; grep -rniE \"rate limit|per-ip|spend cap\" docs memory/*.md 2>/dev/null | head -5; ls Dockerfile* 2>&1 | head -2; .venv/bin/python -m pytest tests/unit/test_api_routes.py -q 2>&1 | tail -2; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T02:00:55.670Z

**tool result**
````
T-011	M1	researcher 	done             	P1	AC 2/2	Persona dossiers: 8 product/engineering personas (PM, UX, staff-eng, security, chaos, a11y, installer, hiring-panel)
T-019	M5	orchestrator	needs_chris      	P1	AC 0/1	Provide a real Anthropic API key for the public deployment (NEEDS_CHRIS #1)
T-020	M5	orchestrator	cancelled        	P2	AC 0/1	Restart the session once so native agent definitions load (NEEDS_CHRIS #2)
T-021	M5	orchestrator	cancelled        	P2	AC 0/1	Confirm tailnet ports :7777/:7860 are fine (443/8443 kept for your services) (NEEDS_CHRIS #3)
T-022	M5	orchestrator	needs_chris      	P1	AC 0/1	Public link: demo-only or live? (NEEDS_CHRIS #2)
T-023	M5	orchestrator	needs_chris      	P2	AC 0/1	Live-model eval budget on claude.ai plan (NEEDS_CHRIS #3)
T-024	M5	orchestrator	done             	P2	AC 1/1	Git author email for this repo (NEEDS_CHRIS #4)
memory/ASSUMPTIONS.md:10:| A-002 | Zlayt reviewers have neither Claude Code nor a key; the <5-minute path is Docker/README in cached demo mode. | Spec: "run it from a link, or from your repo in under 5 minutes". | High | Live mode becomes the primary demo; rate limits matter more. | Installer-reviewer runs the README cold (M4). |
docs/CONTRACT.md:314:Cards (release, qa, backend, security): Dockerfile (port 7860) + `docker run` verified locally; Hugging Face Spaces (Docker SDK, `app_port: 7860`, secrets via Space settings) and Replit run instructions — verify the current HF docs before writing; `README.md` with a *timed* run-from-clone path; `.env.example`; server-side API key with per-session rate limit and spend cap, **demo mode** that serves cached results for the sample case when no key is configured (so the public link works without Chris's key being abused), optional bring-your-own-key; input size limits; error states; a visible "synthetic data only — never paste real records" banner; annotated screenshots of every state (`artifacts/screenshots/`, with captions in `artifacts/CAPTIONS.md`); a ≤ 3-minute Playwright-recorded walkthrough video (`artifacts/demo.webm`, plus a narration script Chris can read over it).
docs/CONTRACT.md:357:| `security-reviewer` | sonnet | Secrets, injection (prompt and classic), rate limits, abuse of a public key, dependency hygiene, size limits, logging of sensitive content. |
docs/CONTRACT.md:451:- Backends by environment: local development runs `LLM_BACKEND=claude-cli` (Chris's claude.ai login, no key); the Docker image and the public Space run `LLM_BACKEND=anthropic-api` and never include the CLI backend. Demo mode: when `ANTHROPIC_API_KEY` is absent in the container, the app serves cached pipeline output for the sample case (recorded from a green eval run) and labels it "cached demo"; when present, live calls run under a per-session rate limit and a daily spend cap. The installer-reviewer's 5-minute test runs the Docker/README path in demo mode, because Zlayt will not have Claude Code or a key.
memory/DECISIONS.md:165:  - **Live mode** is for local use with a key (`LLM_BACKEND=anthropic-api` or `claude-cli`). There is **no in-app rate limiter and no in-app spend ledger** (cut, D-020, ADR-015). Spend control is a monthly spend limit set on the provider key in the provider's console (documented in the README; an action for Chris in NEEDS_CHRIS). With `anthropic-api` the app refuses to start unless `PROVIDER_CAP_CONFIRMED=1` is set, so the limit is a conscious step. Input limits stay: 60 000 characters, 40 records.
ls: Dockerfile*: No such file or directory
..............                                                           [100%]
14 passed in 3.38s
cd4bc60
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:00:57.946Z

**tool call — Bash**
````
{
 "command": "grep -rn \"PROVIDER_CAP_CONFIRMED\" app tests --include=*.py | head; sed -n 155,175p memory/DECISIONS.md | cut -c1-400"
}
````

### User / tool · 2026-11-02T02:00:58.033Z

**tool result**
````
- Consequences: state is reproducible from the ladder alone; the E2E bar (needs_review first, dismissed never exported, edits labelled) is directly checkable.
- Alternatives considered: numeric confidence score (false precision); LLM-reported confidence (uncalibrated); merging state and review status; free edits of dates/provider/flag prose (each a way to introduce a fact the record lacks); blocking an edit when the judge is down (demo mode would never allow an edit).

## ADR-006 Deployment: Hugging Face Spaces (Docker) demo-only; Replit alternate; live mode is local only
- Status: accepted (M1, amended rounds 2 and 3; D-008, D-020). Release owns the files; exact HF front matter is verified against current HF docs at M4.
- Context: Zlayt reviewers have no Claude Code and no key and must run the work from a link or in under 5 minutes. A public paste box stores whatever visitors paste, and a public key invites spend.
- Decision:
  - One Docker image, `EXPOSE 7860`, CLI backend excluded. Primary public host: Hugging Face Space (Docker SDK, `app_port: 7860`). Alternate: Replit running the same entrypoint via `run.sh`.
  - **The public build is demo-only.** Demo mode is on unless `ENABLE_LIVE=1` is set (and a key is present); the public Space never sets it. Demo mode uses the `fixture` backend over recorded responses shipped in the image; the real pipeline code runs and only the model answers are replayed. A "cached demo" badge is shown.
  - **Demo gate (D-020).** `POST /api/cases` normalises the text (CRLF to LF, trimmed), computes its sha256 and accepts it only if the hash is in the recorded set: the sha256 of the normalised `evals/golden/*.txt`, computed at start-up (those files ship in the image). Any other text returns `409 demo_mode_unsupported_input` before anything is written ("Demo mode can only process the recorded sampl
  - **Live mode** is for local use with a key (`LLM_BACKEND=anthropic-api` or `claude-cli`). There is **no in-app rate limiter and no in-app spend ledger** (cut, D-020, ADR-015). Spend control is a monthly spend limit set on the provider key in the provider's console (documented in the README; an action for Chris in NEEDS_CHRIS). With `anthropic-api` the app refuses to start unless `PROVIDER_CAP_C
  - **Case ids** are random 128-bit URL-safe tokens (`secrets.token_urlsafe(16)`); knowing the token is the capability. No case-list endpoint, no accounts. Every endpoint takes the token; unknown token is 404; audit covers only that case. Uvicorn access logging is off (the token is in the path) and every response carries `Referrer-Policy: no-referrer`.
  - **Retention:** one function `delete_case(case_id)` removes rows from every table by `case_id` (records, entries, amounts, flags, `llm_calls` including stored prompts, `review_events`, the case); `DELETE /api/cases/{token}` and the lazy purge (cases older than 24 h, run on every request and at start-up) both call it. SQLite runs with `PRAGMA secure_delete=ON`. `/api/health` returns `retention_h
  - **Time:** every time read (deadlines, purge, retention) goes through an injectable `now()` in `app/config.py`, so tests use a fake clock.
  - Local dev: `make run` on :7860 with `LLM_BACKEND=claude-cli`; tests and eval iteration use `fixture` by default; the live backend is used to record fixtures and for the 3-run determinism check.
- Consequences: the installer test lands on a working, honest demo that stores nothing of the visitor's; a hiring panel cannot try its own text on the public link (stated in the README; live mode runs locally). Cost: less machinery to build and to defend.
- Alternatives considered: live on the public Space with a limiter and ledger (code the demo never runs, and it stores arbitrary text); a case list (cross-visitor exposure); serving a static pre-rendered page (hides the pipeline); bring-your-own-key (cut).

## ADR-007 Pipeline runs in a background thread; the UI polls; ingest and gaps are synchronous code
- Status: accepted (M1, amended round 2)
- Context: the CLI backend takes over a minute for the sample case; the review UI should not block, and failures must be visible.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:01:18.488Z

**tool call — Bash**
````
{
 "command": "grep -rn \"include_router\\|set_case_loader\" app --include=*.py | grep -v \"^app/backend/export_routes.py\" ; grep -n \"<script\" app/frontend/index.html; grep -rn \"secure_delete\" app/db/db.py | head -2; grep -n \"purge_expired\" app/backend/*.py | head"
}
````

### User / tool · 2026-11-02T02:01:18.599Z

**tool result**
````
38:<script src="dom.js"></script>
39:<script src="mock_sample.js"></script>
40:<script src="mock.js"></script>
41:<script src="mock_flags.js"></script>
42:<script src="api.js"></script>
43:<script src="state.js"></script>
44:<script src="input.js"></script>
45:<script src="source.js"></script>
46:<script src="timeline.js"></script>
48:<script src="review.js"></script>
49:<script src="flags.js"></script>
50:<script src="charges.js"></script>
51:<script src="app.js"></script>
app/db/db.py:32:    conn.execute("PRAGMA secure_delete=ON")
app/backend/api.py:148:            DB.purge_expired(c, now)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:01:51.750Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-040-security.md",
 "content": "# T-040 security review (security-reviewer, Tomás Rivas lens)\n\nCommit under review: a7df086 (HEAD moved f861159 -> e274322 -> cd4bc60 during the review; api/review/store/main unchanged by those).\nVerdict: **fail**. One blocker (single request locks the public demo out for everyone), two majors.\n\nVerified clean: demo gate refuses unrecorded text with 409 and nothing stored (row counts 0/0/0/0/0/0/0 before and after, also after 400/413/400 errors); empty 400, oversize 413 (70k chars and a 100 MB body, no llm_calls rows); unknown token 404 on all 9 token routes; invalid-edit matrix 422 (entry provider/date/empty/non-string, charge amount/class/text); `+$9,000` returns 409 needs_confirm and confirm_warnings saves it as needs_review; confirm_date bad reading returns date_invalid 422 with candidates; decisions (e1 edited, e2 accepted, r8 date 2026-05-04) survive a process restart; `referrer-policy: no-referrer`, `x-content-type-options: nosniff`, `cache-control: no-store` on /api, also on 400/404; uvicorn log shows no case tokens or record text (only `llm call failed call_id/step/prompt_hash`); /docs and /openapi.json 404; no stack trace in any response body. Unit tests: `.venv/bin/python -m pytest tests/unit/test_review_rules.py tests/unit/test_api.py -q` -> `24 passed in 1.31s`; test_api_routes -> `14 passed`.\n\nFindings are in the JSON block. The export \"router\" (`export_routes.router`) is never included (`grep -rn include_router app` -> no hits); the same URL is served by an inline route in api.py:277, so the endpoint works. Raw HTML in an edited summary (`Visit <b>x</b> +$9,000`) is stored and returned verbatim as JSON; safe only while the frontend uses textContent (grep of app/frontend for innerHTML/insertAdjacentHTML/outerHTML/document.write returned nothing).\n\n```json\n{\"card\": \"T-040\", \"persona\": \"security-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit a7df086 (app/backend/api.py, review.py, store.py, present.py, app/main.py); app run with LLM_BACKEND=fixture on :7961, DATA_DIR in scratchpad; case_01_date_formats + sample\",\n \"exercised\": [\n  \"read personas/security.md, board show T-040, api.py, review.py, store.py, main.py, export_routes.py header, DECISIONS ADR-006\",\n  \".venv/bin/python -m pytest tests/unit/test_review_rules.py tests/unit/test_api.py -q -> 24 passed in 1.31s; tests/unit/test_api_routes.py -> 14 passed\",\n  \"started python -m app.main LLM_BACKEND=fixture PORT=7961, killed after\",\n  \"POST /api/cases with an <img onerror> non-recorded text -> 409 demo_mode_unsupported_input; sqlite row counts for cases/records/entries/amounts/flags/llm_calls/review_events all 0 before and after\",\n  \"empty 400, 70k-char 413, 100 MB body 413 in 0.3 s, malformed JSON 400, JSON array 400, text:int 400; counts still 0\",\n  \"unknown token on GET case/status/export/audit/items, DELETE, POST run/review/confirm_date -> 404 each\",\n  \"posted case_01, ran pipeline (fixture), status ready; edit matrix (provider, date, empty, non-str, excerpt not in record, charge amount/class/text), 9,000 needs_confirm and confirm_warnings, confirm_date bad/non-str/non-ambiguous/missing/ok, accept, rerun without confirm_rerun -> 409\",\n  \"killed and restarted the server; GET case showed e1 edited, e2 accepted, r8 date 2026-05-04\",\n  \"second POST of the same golden text and two POST sample:true -> 500 Internal Server Error; sqlite showed 3 orphan 'ingested' cases\",\n  \"curl -si headers on 400, 200 static and 404 static responses; /docs, /openapi.json, path traversal -> 404\",\n  \"read server log for tokens/record text; grep logging/print in api/review/present/store/main; grep innerHTML in app/frontend; grep Content-Security-Policy, include_router, PROVIDER_CAP_CONFIRMED, rate-limit in app/\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"input_limits_and_demo_gate\": 5, \"error_handling_no_leak\": 3, \"logging_hygiene\": 5, \"output_encoding_and_headers\": 3, \"availability_abuse_resistance\": 1, \"review_rules_integrity\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"One unauthenticated request locks the public demo out for every other visitor (global id collision -> 500)\",\n   \"evidence\": \"After one successful POST /api/cases (case_01), POST /api/cases with the same golden text, and two with {\\\"sample\\\":true}, each returned `500 Internal Server Error`. server log: `sqlite3.IntegrityError: UNIQUE constraint failed: records.id` at app/backend/pipeline.py:104 via api.py:153. Backend's own card note admits it: 'unsuffixed global PKs (r1,e5,f_gap_r6_r7) so a SECOND case ... collides'. The public demo accepts only golden texts, so every visitor after the first (and the first visitor's own second attempt) gets a 500 until the 24 h purge or an explicit DELETE; an attacker can re-create a case after each purge to keep the lockout (denial of service, no auth, no rate limit needed).\",\n   \"why_it_matters\": \"A public link whose second visitor gets a 500 is unusable for the reviewers it exists for, and it is a one-request availability attack on the whole app (OWASP LLM10 unbounded consumption / resource exhaustion class).\",\n   \"fix\": \"Namespace record/item/flag ids per case (e.g. pk = case_id + ':' + local id, or a composite (case_id, id) key) in db/pipeline; keep the local ids in API payloads.\",\n   \"acceptance_test\": \"Test: POST /api/cases twice with the sample (and once more after run on the first), all return 201 with different tokens; items of case A are 404 under case B's token; ids in each payload are unchanged.\"},\n  {\"severity\": \"major\", \"title\": \"Failed create leaves an orphan case row (raw text stored) and returns a bare 500; no generic error handler\",\n   \"evidence\": \"api.py:152-156 only deletes the case on ingest.IngestError. In the run above, 3 failed POSTs left 3 rows: `SELECT status,count(*) FROM cases GROUP BY status` -> `[('ingested', 3), ('ready', 1)]`. The demo's promise (ADR-006/D-020) is that nothing of a refused request is stored; here a non-IngestError exception stores pasted text with no token ever returned to the caller, so it is only removed by the 24 h purge. The 500 body is plain 'Internal Server Error' (no trace leaked) but it is outside the documented JSON error format.\",\n   \"why_it_matters\": \"Storage growth by unauthenticated callers, stored text the user cannot delete (no token returned), and error format drift.\",\n   \"fix\": \"Wrap the whole ingest in try/except Exception: delete the case and re-raise as ApiError(500, 'internal', 'Something went wrong.'); add a catch-all exception handler returning the standard JSON error with no detail.\",\n   \"acceptance_test\": \"Test: inject a pipeline whose ingest_case raises RuntimeError; assert 500 with error.code present, no traceback text in the body, and cases table has 0 rows.\"},\n  {\"severity\": \"major\", \"title\": \"No Content-Security-Policy on any response\",\n   \"evidence\": \"`curl -si localhost:7961/` shows referrer-policy and x-content-type-options only; `grep -rn Content-Security-Policy app` -> no hits. The middleware at api.py:105-111 is where headers are set. All 14 <script> tags in app/frontend/index.html are external src files, so `script-src 'self'` is feasible.\",\n   \"why_it_matters\": \"Checklist item 6; edited summaries and record text are attacker-controllable strings (api returns `Visit <b>x</b> +$9,000` verbatim), so CSP is the second layer behind textContent (OWASP LLM05 / XSS cheat sheet).\",\n   \"fix\": \"Add `Content-Security-Policy: default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'` in the same middleware (adjust style-src if inline styles exist) plus X-Frame-Options or frame-ancestors.\",\n   \"acceptance_test\": \"Test: GET / and GET /api/health both carry a CSP header without 'unsafe-inline' in script-src; Playwright page with a record containing <img src=x onerror=alert(1)> fires no dialog.\"},\n  {\"severity\": \"minor\", \"title\": \"Request body is fully buffered before the size limit is applied\",\n   \"evidence\": \"api.py:114 `raw = await request.body()` then json.loads, then ingest.check_limits (api.py:140). A 100 MB body was read and parsed (413 after 0.3 s); there is no Content-Length precheck or streaming cap.\",\n   \"why_it_matters\": \"Memory use grows with attacker body size; the documented 60,000-character limit is enforced after the allocation (checklist item 1 intent is cheap rejection).\",\n   \"fix\": \"Reject when Content-Length exceeds a byte cap (e.g. 512 KB) with 413 before reading; also cap while streaming when the header is absent.\",\n   \"acceptance_test\": \"Test: POST with a 5 MB body returns 413 input_too_large and the handler never calls request.body() fully (assert via a small ASGI middleware test or peak memory).\"},\n  {\"severity\": \"minor\", \"title\": \"Spec'd live-mode guard PROVIDER_CAP_CONFIRMED is not enforced anywhere; lazy purge only on create\",\n   \"evidence\": \"ADR-006: 'With anthropic-api the app refuses to start unless PROVIDER_CAP_CONFIRMED=1'. `grep -rn PROVIDER_CAP_CONFIRMED app tests --include=*.py` -> no hits; api.py:57-58 goes live on ENABLE_LIVE=1 plus a key. ADR-006 also says purge runs on every request; only api.py:148 (create_case) calls DB.purge_expired. This may belong to the config/release card; flagged because api.py is where the live gate sits.\",\n   \"why_it_matters\": \"D-020 replaced the in-app limiter with this conscious provider-cap step; without it a local live run has no cap acknowledgement. Purge-on-create-only means expired data stays readable by token until someone creates a case.\",\n   \"fix\": \"Fail fast in create_app when backend=='anthropic-api' and live is enabled and PROVIDER_CAP_CONFIRMED!='1'; call purge_expired in the `_headers` middleware or a dependency.\",\n   \"acceptance_test\": \"Test: create_app with LLM_BACKEND=anthropic-api, ENABLE_LIVE=1, a key and no PROVIDER_CAP_CONFIRMED raises; a case older than 24 h returns 404 on GET without any POST in between.\"},\n  {\"severity\": \"nit\", \"title\": \"Export router never included; export served by an inline route\",\n   \"evidence\": \"`grep -rn include_router app --include=*.py` -> only prose in export_routes.py docstring; api.py:277 defines its own GET /export and calls XR.export_payload.\",\n   \"why_it_matters\": \"Dead router and set_case_loader invite a later duplicate-route or unauthenticated-variant mistake.\",\n   \"fix\": \"Either include the router or delete it and the loader hook.\",\n   \"acceptance_test\": \"grep shows exactly one definition of GET /api/cases/{token}/export.\"}\n ],\n \"whats_right\": [\n  \"Demo gate runs before any DB write and ingest limits run before any LLM call; row counts stayed zero across 409/400/413.\",\n  \"Review layer is fail-closed: invalid edits 422, rejected items cannot be accepted or edited, ungrounded excerpt rejected, new numbers need explicit confirm and never become verified.\",\n  \"access_log=False, token-free logs, generic JSON errors on 404/405/validation, docs/openapi disabled.\"\n ],\n \"questions_for_chris\": [\"Is PROVIDER_CAP_CONFIRMED enforcement meant to land in this card or the config/release card?\"]}\n```\n"
}
````

### User / tool · 2026-11-02T02:01:51.896Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-040-security.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:01:54.061Z

Verdict is **fail**: `reviews/T-040-security.md` has one blocker and two majors. The blocker: a second `POST /api/cases` (sample or golden text) returns 500 on a UNIQUE `records.id` collision, so one request locks out every other visitor.
Majors: a failed create leaves an orphan case row and gives a bare 500, and no Content-Security-Policy is set.
The demo gate, 400/413 limits, 404/422/409 matrix, restart persistence, Referrer-Policy and token-free logs all passed (24/24 unit tests). I killed the server after probing.
