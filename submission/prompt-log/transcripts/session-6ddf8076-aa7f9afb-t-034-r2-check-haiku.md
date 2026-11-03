# Subagent: T-034 r2 check (haiku) (T-034 r2 check (haiku))

Source: `agent-aa7f9afb49aef3e71.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:53:59.552Z

Working directory: /Users/arsis/zlayt-pm-project. Round 2 of T-034 against reviews/T-034-security.md (major: tests expecting FixtureMissing, `sleep` kwarg on audited_call, prompt hash in miss log; minors: recorder substring guard, schema validator ignoring maxLength/maximum/anyOf, claude-cli child env, audit error column). Run `.venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q 2>&1 | tail -3` and quote; grep app/llm for each minor fix and quote the line. Pass if tests green and the major is resolved. Write reviews/T-034-security-r2.md (D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:01.443Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/security.md"
}
````

### User / tool · 2026-11-02T01:54:01.451Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:01.630Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-034-security.md"
}
````

### User / tool · 2026-11-02T01:54:01.636Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:01.858Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T01:54:01.870Z

**tool result**
````
1	- [Hook/guard review patterns](project_hook_guard_review_patterns.md) — recurring bypass classes in git-guard/board-guard/check_secrets and reviewer-workflow gotchas
2	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:02.310Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q 2>&1 | tail -3",
 "description": "Run the three T-034 unit test files and tail output"
}
````

### User / tool · 2026-11-02T01:54:03.715Z

**tool result**
````
........................................                                 [100%]
40 passed in 0.95s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:06.987Z

**tool call — Bash**
````
{
 "command": "echo \"--- FixtureMissing / FixtureMiss\" && grep -rn \"FixtureMissing\\|FixtureMiss\\b\" app/llm tests/unit/test_provider.py tests/unit/test_audited.py | head -40; echo \"--- sleep\" && grep -rn \"sleep\" app/llm tests/unit/test_audited.py tests/unit/test_provider.py tests/unit/test_provider_backends.py | head -40; echo \"--- hash\" && grep -rn \"hash\" app/llm tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py | head -60",
 "description": "Grep the LLM package and tests for major-finding symbols"
}
````

### User / tool · 2026-11-02T01:54:07.088Z

**tool result**
````
--- FixtureMissing / FixtureMiss
app/llm/provider.py:15:from app.llm._types import FixtureMiss, FixtureMissing, LLMError, LLMResult, validate_schema  # noqa: F401  (re-exported API)
app/llm/_types.py:11:class FixtureMissing(LLMError):
app/llm/_types.py:19:FixtureMiss = FixtureMissing   # old spelling, kept as an alias
app/llm/audited.py:29:class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
app/llm/audited.py:30:    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""
app/llm/audited.py:33:        P.FixtureMissing.__init__(self, prompt_hash)
app/llm/audited.py:65:        except P.FixtureMissing as e:
app/llm/audited.py:85:            raise LLMFailedFixtureMiss(h)
app/llm/backends/fixture.py:1:"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
app/llm/backends/fixture.py:7:from app.llm._types import FixtureMiss, LLMError, LLMResult
app/llm/backends/fixture.py:20:        raise FixtureMiss(key)
tests/unit/test_provider.py:6:MISS = getattr(P, "FixtureMissing", None) or P.FixtureMiss
tests/unit/test_provider.py:32:    """ADR-004 / T-034 AC8: a miss raises FixtureMissing (an LLMError) carrying the prompt hash; no answer is invented."""
tests/unit/test_provider.py:38:    """T-034 AC8 / T-037 AC7: the exception is called FixtureMissing (one spelling across app, tests and docs)."""
tests/unit/test_provider.py:39:    assert hasattr(P, "FixtureMissing") and issubclass(P.FixtureMissing, P.LLMError)
tests/unit/test_provider.py:58:    """ADR-004: output is re-validated against the schema; invalid -> LLMError (not FixtureMiss)."""
tests/unit/test_audited.py:6:MISS = getattr(P, "FixtureMissing", None) or P.FixtureMiss   # T-034 AC8 name is FixtureMissing; test_provider pins that the name exists
--- sleep
app/llm/audited.py:53:                 complete_with_meta=None, validate=None, item_id=None, now=None, prompt_version=None, sleep=None):
app/llm/audited.py:86:        if sleep is not None and attempt < MAX_ATTEMPTS:
app/llm/audited.py:87:            sleep(RETRY_DELAYS_S[attempt - 1])         # short, capped, code-controlled
tests/unit/test_audited.py:27:    """audited_call; retries are immediate (no backoff, so no sleep hook is needed - if backend adds one, patch it here)."""
tests/unit/test_provider_backends.py:40:        time.sleep(0.05)
tests/unit/test_provider_backends.py:184:def test_audited_sleep_seam_is_capped_and_injectable(tmp_path):
tests/unit/test_provider_backends.py:189:        AU.audited_call(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f, sleep=naps.append)
--- hash
app/llm/_types.py:12:    """No recorded answer for this prompt hash. Never retried, never answered with a default."""
app/llm/_types.py:14:    def __init__(self, prompt_hash: str = ""):
app/llm/_types.py:15:        super().__init__(f"FIXTURE_MISS {prompt_hash}")
app/llm/_types.py:16:        self.prompt_hash = prompt_hash
app/llm/provider.py:5:Record mode (RECORD_FIXTURES=1 or LLM_FIXTURE_RECORD=1, live backend only) writes tests/fixtures/llm/<hash>.json and is
app/llm/provider.py:9:import hashlib
app/llm/provider.py:26:def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
app/llm/provider.py:29:    return hashlib.sha256(blob.encode("utf-8")).hexdigest()
app/llm/provider.py:69:    key = prompt_hash(model, system, user, json_schema)
app/llm/audited.py:4:attempt (prompt hash = sha256 of model+system+user+schema); a fixture miss is final. Never logs prompts, responses or error text.
app/llm/audited.py:32:    def __init__(self, prompt_hash: str = ""):
app/llm/audited.py:33:        P.FixtureMissing.__init__(self, prompt_hash)
app/llm/audited.py:58:        h = P.prompt_hash(model, system, u, json_schema)
app/llm/audited.py:66:            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
app/llm/audited.py:83:        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
app/llm/backends/fixture.py:31:    """Record mode: store a live result keyed by the prompt hash, with provenance."""
app/llm/record.py:3:Runs the pipeline over one golden input with a live backend; provider.py writes tests/fixtures/llm/<hash>.json for
app/llm/promptlib.py:3:import hashlib
app/llm/promptlib.py:16:    sha256: str     # hash of the whole file, changelog included (what evals record)
app/llm/promptlib.py:24:    return Prompt(name, _CHANGELOG.sub("", raw).strip(), hashlib.sha256(raw.encode()).hexdigest())
app/llm/promptlib.py:29:    h = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()
tests/unit/test_provider.py:17:    h = P.prompt_hash(model, system, user, SCHEMA)
tests/unit/test_provider.py:20:def test_prompt_hash_is_stable_and_sensitive():
tests/unit/test_provider.py:22:    a = P.prompt_hash("m", "s", "u", SCHEMA)
tests/unit/test_provider.py:23:    assert a == P.prompt_hash("m", "s", "u", SCHEMA) and len(a) == 64
tests/unit/test_provider.py:24:    assert len({a, P.prompt_hash("m2", "s", "u", SCHEMA), P.prompt_hash("m", "s2", "u", SCHEMA), P.prompt_hash("m", "s", "u2", SCHEMA), P.prompt_hash("m", "s", "u", {})}) == 5
tests/unit/test_provider.py:32:    """ADR-004 / T-034 AC8: a miss raises FixtureMissing (an LLMError) carrying the prompt hash; no answer is invented."""
tests/unit/test_provider.py:35:    assert isinstance(e.value, P.LLMError) and e.value.prompt_hash == P.prompt_hash("m", "s", "nothing recorded", SCHEMA)
tests/unit/test_provider.py:41:def test_fixture_miss_reports_hash_not_text(fx, caplog, capsys):
tests/unit/test_provider.py:42:    """T-034 AC8 + arch invariant: the miss message carries the prompt hash (the audited row stores it) and never the prompt text; nothing is printed."""
tests/unit/test_provider.py:48:    assert P.prompt_hash("m", "s", "SECRET RECORD TEXT", SCHEMA) in str(e.value)
tests/unit/test_provider_backends.py:141:    assert len(rows) == 1 and rows[0]["backend"] == "fixture" and rows[0]["attempt"] == 1 and rows[0]["prompt_sha256"] == P.prompt_hash("m", "s", "u", SCHEMA)
tests/unit/test_provider_backends.py:146:    (tmp_path / f"{P.prompt_hash('m', 's', 'u', SCHEMA)}.json").write_text(json.dumps(dict(output={"summary": "ok"}, recorded_from=dict(backend="claude-cli", model="m", recorded_at="t"))))
tests/unit/test_audited.py:62:    """T-034 AC8 / T-037 AC7 / FIXTURE_MISS: a miss is final (one attempt, one row); the wrapper turns it into LLMFailed(LLM_FAILED_AFTER_RETRIES) and the row logs the prompt hash."""
tests/unit/test_audited.py:64:    f = seq(MISS("abc123hash"))
tests/unit/test_audited.py:69:    assert "abc123hash" in (row["error"] or "")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:08.226Z

**tool call — Bash**
````
{
 "command": "echo \"--- recorder guard\" && grep -n \"_norm\\|in _norm\\|record_context\\|_record_ok\\|def assert_recordable\\|def record_file\" app/llm/provider.py; echo \"--- schema\" && grep -n \"maxLength\\|maximum\\|anyOf\\|_TYPES\\|raise\\|def validate_schema\\|KeyError\" app/llm/_types.py; echo \"--- cli env\" && grep -n \"env\\|ANTHROPIC\\|ZLAYT_DEV\\|environ\" app/llm/backends/claude_cli.py; echo \"--- audit error\" && grep -n \"error\\|str(e)\\|\\[:200\\]\" app/llm/audited.py; echo \"--- git\" && git -C /Users/arsis/zlayt-pm-project status --short 2>&1 | head -20; git -C /Users/arsis/zlayt-pm-project log --oneline -3 2>&1",
 "description": "Grep minor-fix locations and git state"
}
````

### User / tool · 2026-11-02T01:54:08.387Z

**tool result**
````
--- recorder guard
6:refused unless a `record_context(text)` for text found in evals/golden is active (ADR-004).
19:_record_ok = False
32:def _norm(s: str) -> str:
39:def assert_recordable(text: str, *, whole_file: bool = False) -> None:
42:    t = _norm(text or "")
45:            g = _norm(p.read_text())
52:def record_context(source_text: str):
54:    global _record_ok
56:    prev, _record_ok = _record_ok, True
60:        _record_ok = prev
73:        if _recording() and not _record_ok:
74:            raise ValueError("record mode needs record_context() over text from evals/golden")
--- schema
47:        raise LLMError("INVALID_JSON: reply is not a single JSON object") from None
49:        raise LLMError("INVALID_JSON: reply is not a JSON object")
54:_KEYWORDS = _ANNOTATIONS | {"type", "enum", "const", "required", "properties", "additionalProperties", "items", "$ref", "anyOf",
55:                            "maxLength", "minLength", "maximum", "minimum", "maxItems", "minItems"}
73:    raise LLMError(f"SCHEMA_UNSUPPORTED type {str(x)[:20]}")
77:    """Fail closed: a schema keyword outside _KEYWORDS raises LLMError instead of being silently ignored."""
82:        raise LLMError(f"SCHEMA_UNSUPPORTED keyword {sorted(bad)}")
86:            raise LLMError("SCHEMA_UNSUPPORTED $ref")
89:            raise LLMError("SCHEMA_UNSUPPORTED $ref target")
91:    if "anyOf" in s:
93:        for sub in s["anyOf"]:
98:        if errs == len(s["anyOf"]):
99:            raise ValueError(f"{path or '$'}: matches no anyOf branch")
104:            raise ValueError(f"{path or '$'}: expected {t}")
106:        raise ValueError(f"{path or '$'}: not in enum")
108:        raise ValueError(f"{path or '$'}: not const")
110:        if "maxLength" in s and len(v) > s["maxLength"]:
111:            raise ValueError(f"{path or '$'}: too long")
113:            raise ValueError(f"{path or '$'}: too short")
115:        if "maximum" in s and v > s["maximum"]:
116:            raise ValueError(f"{path or '$'}: above maximum")
118:            raise ValueError(f"{path or '$'}: below minimum")
123:                raise ValueError(f"{path or '$'}: missing {r}")
126:            raise ValueError(f"{path or '$'}: unexpected key")      # key names are model output: not echoed
135:            raise ValueError(f"{path or '$'}: too many items")
137:            raise ValueError(f"{path or '$'}: too few items")
143:def validate_schema(output, schema: dict) -> None:
149:        raise LLMError(f"SCHEMA_INVALID {e}") from None
--- cli env
25:def child_env() -> dict:
26:    """Minimal environment for the CLI child (claude.ai login via HOME): no ANTHROPIC_* variable or other secret is inherited."""
27:    return {k: os.environ[k] for k in ENV_ALLOW if k in os.environ}
37:    return [os.environ.get("CLAUDE_BIN") or shutil.which("claude") or "claude", "-p", "--model", model,
45:    env = child_env()
51:                p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=TIMEOUT_S, stdin=subprocess.DEVNULL)
61:        env_json = json.loads(p.stdout)
63:        raise LLMError("BACKEND_FAILED claude-cli envelope not JSON") from None
64:    if not isinstance(env_json, dict) or env_json.get("is_error"):
66:    text = env_json.get("result") or ""
68:    mu = env_json.get("modelUsage") or {}
72:                     latency_ms=int((time.monotonic() - t0) * 1000), cost_usd=float(env_json.get("total_cost_usd") or 0.0),
--- audit error
4:attempt (prompt hash = sha256 of model+system+user+schema); a fixture miss is final. Never logs prompts, responses or error text.
36:def _error_code(e: Exception) -> str:
39:        m = _CODE.match(str(e))
67:        except Exception as e:                         # only our own error codes are stored, never model- or record-derived text
68:            err = _error_code(e)
72:                      parsed_ok=1 if err is None else 0, error=err)
--- git
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/feedback_lexicon_recall_and_negation.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md
 M .claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md
 M .claude/agent-memory/product-manager-reviewer/project_t013_review_history.md
 M .claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md
 M .claude/agent-memory/security-reviewer/project_hook_guard_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M app/backend/confidence.py
 M app/backend/flags.py
 M app/backend/generator.py
b1803c0 fix(backend): FixtureMissing, hash log, sleep seam, fail-closed schema validator, recorder guard, cli env allowlist (T-034 r1)
117f2ec feat(frontend): input, banners, timeline, Why?, rejected tray, source-record modal (T-042)
11ab4fb test: T-039 review fixes - complete E2E hook contract, record_ids helpers, non-vacuous assertions
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:12.440Z

**tool call — Bash**
````
{
 "command": "echo \"--- provider.py 28-80\" && sed -n '28,80p' app/llm/provider.py; echo \"--- claude_cli.py 1-30\" && sed -n '1,30p' app/llm/backends/claude_cli.py; echo \"--- gating grep\" && grep -rn \"ZLAYT_DEV\\|claude-cli\\|claude_cli\" app/ tools/ 2>/dev/null | grep -v \"\\.pyc\" | head -30; echo \"--- commit stat\" && git show --stat b1803c0 | head -40",
 "description": "Read recorder guard, CLI env allowlist, and backend gating"
}
````

### User / tool · 2026-11-02T01:54:12.567Z

**tool result**
````
--- provider.py 28-80
    blob = json.dumps([model, system, user, json_schema], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


MIN_FRAGMENT = 20


def assert_recordable(text: str, *, whole_file: bool = False) -> None:
    """ValueError unless `text` (whitespace-normalised) is a golden file's full text (whole_file) or a fragment of at least
    MIN_FRAGMENT characters inside one. No other text may be recorded."""
    t = _norm(text or "")
    if len(t) >= (1 if whole_file else MIN_FRAGMENT):
        for p in sorted(GOLDEN_DIR.glob("*.txt")):
            g = _norm(p.read_text())
            if t == g or (not whole_file and t in g):
                return
    raise ValueError("text is not an evals/golden input; refusing to record")


@contextlib.contextmanager
def record_context(source_text: str):
    """Used by record.py only: allow record-mode writes while the pipeline runs over a COMPLETE golden input."""
    global _record_ok
    assert_recordable(source_text, whole_file=True)
    prev, _record_ok = _record_ok, True
    try:
        yield
    finally:
        _record_ok = prev


def _recording() -> bool:
    return os.environ.get("RECORD_FIXTURES") == "1" or os.environ.get("LLM_FIXTURE_RECORD") == "1"


def complete_with_meta(model: str, system: str, user: str, json_schema: dict) -> LLMResult:
    name = backend_name()
    key = prompt_hash(model, system, user, json_schema)
    if name == "fixture":
        res = _fixture.call(model, system, user, json_schema, key=key)
    elif name in ("claude-cli", "anthropic-api"):
        if _recording() and not _record_ok:
            raise ValueError("record mode needs record_context() over text from evals/golden")
        if name == "claude-cli":
            from app.llm.backends import claude_cli as be
        else:
            from app.llm.backends import anthropic_api as be
        res = be.call(model, system, user, json_schema, key=key)
    else:
--- claude_cli.py 1-30
"""claude-cli backend (development only, never in the Docker image). ADR-004; flags verified in memory/ENVIRONMENT.md.

Runs `claude -p` from a throwaway cwd outside the project with hooks, tools and MCP disabled. One attempt, no retry.
Never logs prompts or replies.
"""
import json
import os
import shutil
import subprocess
import tempfile
import threading
import time

from app.llm._types import LLMError, LLMResult, parse_json_reply

TIMEOUT_S = 120
MAX_CONCURRENCY = 3
_SEM = threading.BoundedSemaphore(MAX_CONCURRENCY)


ENV_ALLOW = ("PATH", "HOME", "USER", "LOGNAME", "LANG", "LC_ALL", "TMPDIR", "CLAUDE_BIN", "CLAUDE_CONFIG_DIR", "XDG_CONFIG_HOME",
             "XDG_DATA_HOME", "XDG_CACHE_HOME")


def child_env() -> dict:
    """Minimal environment for the CLI child (claude.ai login via HOME): no ANTHROPIC_* variable or other secret is inherited."""
    return {k: os.environ[k] for k in ENV_ALLOW if k in os.environ}


def _system_with_schema(system: str, json_schema: dict) -> str:
--- gating grep
app/README-arch.md:9:                                                                                              claude-cli | anthropic-api | fixture
app/README-arch.md:34:  backends/        claude_cli.py  anthropic_api.py  fixture.py (+ record mode)
app/llm/provider.py:3:LLM_BACKEND = fixture (default; no key, no network) | claude-cli (dev) | anthropic-api (live).
app/llm/provider.py:72:    elif name in ("claude-cli", "anthropic-api"):
app/llm/provider.py:75:        if name == "claude-cli":
app/llm/provider.py:76:            from app.llm.backends import claude_cli as be
app/llm/backends/claude_cli.py:1:"""claude-cli backend (development only, never in the Docker image). ADR-004; flags verified in memory/ENVIRONMENT.md.
app/llm/backends/claude_cli.py:53:                raise LLMError("TIMEOUT claude-cli") from None
app/llm/backends/claude_cli.py:55:                raise LLMError("BACKEND_UNAVAILABLE claude-cli not runnable") from None
app/llm/backends/claude_cli.py:59:        raise LLMError(f"BACKEND_FAILED claude-cli exit {p.returncode}")
app/llm/backends/claude_cli.py:63:        raise LLMError("BACKEND_FAILED claude-cli envelope not JSON") from None
app/llm/backends/claude_cli.py:65:        raise LLMError("BACKEND_FAILED claude-cli reported an error")
app/llm/backends/claude_cli.py:71:    return LLMResult(output=out, backend="claude-cli", model_resolved=resolved,
app/llm/record.py:1:"""Fixture recorder: LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record evals/golden/<case>.txt
app/llm/record.py:22:        raise ValueError("record mode needs a live LLM_BACKEND (claude-cli or anthropic-api)")
app/frontend/mock.js:72:      generator: { model: "claude-sonnet-5-5", prompt_version: "extract_v1", call_id: "c" + id, recorded_from: { backend: "claude-cli", model: "claude-sonnet-5-5", recorded_at: "2026-11-02T00:50:00Z" }, output: { summary: opts.summary, excerpt: ex.text } },
--- commit stat
commit b1803c009d3c972061494b1df21166edf5c95dec
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 19:53:42 2026 -0600

    fix(backend): FixtureMissing, hash log, sleep seam, fail-closed schema validator, recorder guard, cli env allowlist (T-034 r1)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/llm/_types.py                    | 106 +++++++++++++++++++++++++++--------
 app/llm/audited.py                   |  28 ++++++---
 app/llm/backends/claude_cli.py       |  13 ++++-
 app/llm/prompts/conflicts_v1.md      |  14 +++++
 app/llm/prompts/flags_v1.md          |  26 +++++++++
 app/llm/provider.py                  |  21 ++++---
 tests/unit/test_provider_backends.py |   4 +-
 7 files changed, 168 insertions(+), 44 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:13.090Z

**tool call — Bash**
````
{
 "command": "echo \"--- provider.py 1-27 and 32-62\" && sed -n '1,27p;32,62p' app/llm/provider.py; echo \"--- audited.py 30-90\" && sed -n '30,90p' app/llm/audited.py; echo \"--- _types.py 1-22 and 140-150\" && sed -n '1,22p;140,150p' app/llm/_types.py",
 "description": "Read provider, audited, and _types core sections"
}
````

### User / tool · 2026-11-02T01:54:13.181Z

**tool result**
````
--- provider.py 1-27 and 32-62
"""Provider interface (ADR-004, R-CO-2/6): complete(model, system, user, json_schema) -> dict over three backends.

LLM_BACKEND = fixture (default; no key, no network) | claude-cli (dev) | anthropic-api (live).
Backends make exactly one attempt and never log text; retries and audit rows live in audited.py.
Record mode (RECORD_FIXTURES=1 or LLM_FIXTURE_RECORD=1, live backend only) writes tests/fixtures/llm/<hash>.json and is
refused unless a `record_context(text)` for text found in evals/golden is active (ADR-004).
"""
import contextlib
import hashlib
import json
import os
import pathlib
import re

from app.llm._types import FixtureMiss, FixtureMissing, LLMError, LLMResult, validate_schema  # noqa: F401  (re-exported API)
from app.llm.backends import fixture as _fixture

GOLDEN_DIR = pathlib.Path(__file__).resolve().parents[2] / "evals" / "golden"
_record_ok = False


def backend_name() -> str:
    return os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"


def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
    """sha256 over model+system+user+schema (canonical JSON). Any change to any part changes the key."""
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


MIN_FRAGMENT = 20


def assert_recordable(text: str, *, whole_file: bool = False) -> None:
    """ValueError unless `text` (whitespace-normalised) is a golden file's full text (whole_file) or a fragment of at least
    MIN_FRAGMENT characters inside one. No other text may be recorded."""
    t = _norm(text or "")
    if len(t) >= (1 if whole_file else MIN_FRAGMENT):
        for p in sorted(GOLDEN_DIR.glob("*.txt")):
            g = _norm(p.read_text())
            if t == g or (not whole_file and t in g):
                return
    raise ValueError("text is not an evals/golden input; refusing to record")


@contextlib.contextmanager
def record_context(source_text: str):
    """Used by record.py only: allow record-mode writes while the pipeline runs over a COMPLETE golden input."""
    global _record_ok
    assert_recordable(source_text, whole_file=True)
    prev, _record_ok = _record_ok, True
    try:
        yield
    finally:
        _record_ok = prev


--- audited.py 30-90
    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""

    def __init__(self, prompt_hash: str = ""):
        P.FixtureMissing.__init__(self, prompt_hash)


def _error_code(e: Exception) -> str:
    """Our own codes only (SCHEMA_INVALID, TIMEOUT, BACKEND_FAILED ...); anything else is reduced to the exception class."""
    if isinstance(e, P.LLMError):
        m = _CODE.match(str(e))
        return m.group(1) if m else "LLM_ERROR"
    return "VALIDATION_FAILED" if isinstance(e, ValueError) else type(e).__name__


def role_for(step: str) -> str:
    return "judge" if str(step).startswith("judge") else "generator"


def _t(now):
    return now() if callable(now) else (time.time() if now is None else now)


def audited_call(conn, case_id: str, step: str, model: str, system: str, user: str, json_schema: dict, *,
                 complete_with_meta=None, validate=None, item_id=None, now=None, prompt_version=None, sleep=None):
    cwm = complete_with_meta or P.complete_with_meta
    last_err = "unknown"
    for attempt in range(1, MAX_ATTEMPTS + 1):
        u = user + _RETRY_NOTES[attempt - 1]
        h = P.prompt_hash(model, system, u, json_schema)
        t0 = time.monotonic()
        res, err, fixture_miss = None, None, False
        try:
            res = cwm(model, system, u, json_schema)
            if validate is not None:
                validate(res.output)
        except P.FixtureMissing as e:
            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
        except Exception as e:                         # only our own error codes are stored, never model- or record-derived text
            err = _error_code(e)
        ms = int((time.monotonic() - t0) * 1000)
        fields = dict(role=role_for(step), step=step, backend=(res.backend if res else P.backend_name()), model=(res.model_resolved if res and res.model_resolved else model),
                      prompt_version=prompt_version, prompt_sha256=h, attempt=attempt, latency_ms=(res.latency_ms if res and res.latency_ms else ms),
                      parsed_ok=1 if err is None else 0, error=err)
        if item_id:
            fields["item_id"] = item_id
        if res:
            import json as _j
            fields.update(cost_usd=res.cost_usd, tokens_in=res.tokens_in, tokens_out=res.tokens_out,
                          recorded_from_json=_j.dumps(res.recorded_from) if res.recorded_from else None)
        call_id = DB.add_llm_call(conn, case_id, u, (res.raw or _dump(res.output)) if res else None, now=_t(now), system=system, **fields)
        if err is None:
            return res.output, call_id
        last_err = err
        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
        if fixture_miss:
            raise LLMFailedFixtureMiss(h)
        if sleep is not None and attempt < MAX_ATTEMPTS:
            sleep(RETRY_DELAYS_S[attempt - 1])         # short, capped, code-controlled
    raise LLMFailed(f"{step}: {MAX_ATTEMPTS} attempts failed")


--- _types.py 1-22 and 140-150
"""Shared provider types, JSON parsing and a small JSON-Schema checker (no jsonschema dependency). ADR-004."""
import json
import re
from dataclasses import dataclass, field


class LLMError(Exception):
    """Timeout, backend failure, invalid JSON or schema-invalid output. Messages must never contain record text."""


class FixtureMissing(LLMError):
    """No recorded answer for this prompt hash. Never retried, never answered with a default."""

    def __init__(self, prompt_hash: str = ""):
        super().__init__(f"FIXTURE_MISS {prompt_hash}")
        self.prompt_hash = prompt_hash


FixtureMiss = FixtureMissing   # old spelling, kept as an alias


@dataclass
                _check(x, s["items"], f"{path}[{i}]", root)


def validate_schema(output, schema: dict) -> None:
    """Raise LLMError if output does not satisfy the schema (supported subset; anything else is refused)."""
    root = {"$defs": (schema or {}).get("$defs", {}), "definitions": (schema or {}).get("definitions", {})}
    try:
        _check(output, schema or {}, "", root)
    except ValueError as e:
        raise LLMError(f"SCHEMA_INVALID {e}") from None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:26.618Z

**tool call — Bash**
````
{
 "command": "echo \"--- tests status\" && git status --short tests/ app/llm/ evals/ 2>&1; echo \"--- test diff vs HEAD (stat)\" && git diff --stat HEAD -- tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py app/llm; echo \"--- test_provider_backends 184-200\" && sed -n '180,200p' tests/unit/test_provider_backends.py; echo \"--- test_audited 20-35\" && sed -n '20,35p' tests/unit/test_audited.py; echo \"--- _types 50-100\" && sed -n '50,100p' app/llm/_types.py; echo \"--- _CODE\" && grep -n \"_CODE\\|RETRY_DELAYS_S\\|MAX_ATTEMPTS\\|_RETRY_NOTES\" app/llm/audited.py | head; echo \"--- recorder users\" && grep -rn \"assert_recordable\\|record_context\\|_record_ok\" app tools evals tests 2>/dev/null | grep -v \"\\.pyc\"",
 "description": "Check test tree state, test diffs, validator, and recorder callers"
}
````

### User / tool · 2026-11-02T01:54:26.783Z

**tool result**
````
--- tests status
 M app/llm/prompts/judge_amount_class_v1.md
 M app/llm/prompts/judge_conflict_v1.md
 M app/llm/prompts/judge_faithfulness_v1.md
 M app/llm/prompts/judge_flag_v1.md
A  tests/unit/test_api.py
A  tests/unit/test_export_edge.py
?? evals/run.py
?? tests/unit/test_eval_runner.py
?? tests/unit/test_eval_spec_check.py
--- test diff vs HEAD (stat)
 app/llm/prompts/judge_amount_class_v1.md | 5 +++--
 app/llm/prompts/judge_conflict_v1.md     | 5 +++--
 app/llm/prompts/judge_faithfulness_v1.md | 5 +++--
 app/llm/prompts/judge_flag_v1.md         | 5 +++--
 4 files changed, 12 insertions(+), 8 deletions(-)
--- test_provider_backends 184-200
        AU.audited_call(conn, cid, "extract", "m", "s", "u", {"type": "object", "properties": {}, "additionalProperties": False}, complete_with_meta=f, validate=lambda o: P.validate_schema(o, {"type": "object", "properties": {}, "additionalProperties": False}))
    errs = [r["error"] for r in DB.list_llm_calls(conn, cid)]
    assert errs == ["SCHEMA_INVALID"] * 3 and not any("<img" in e for e in errs)

def test_audited_sleep_seam_is_capped_and_injectable(tmp_path):
    conn = DB.connect(str(tmp_path / "a.sqlite")); cid = DB.create_case(conn, "SYNTHETIC", now=1.0)
    naps = []
    def f(model, system, user, schema): raise P.LLMError("TIMEOUT x")
    with pytest.raises(AU.LLMFailed):
        AU.audited_call(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f, sleep=naps.append)
    assert naps == list(AU.RETRY_DELAYS_S) and max(naps) <= 2
--- test_audited 20-35
        if isinstance(o, Exception):
            raise o
        return P.LLMResult(output=o, backend="fixture", model_resolved=model)
    f.state = state
    return f

def ac(conn, cid, *a, **kw):
    """audited_call; retries are immediate (no backoff, so no sleep hook is needed - if backend adds one, patch it here)."""
    return AU.audited_call(conn, cid, *a, **kw)

def rows(conn, cid):
    return DB.table_counts(conn, cid).get("llm_calls", 0)

def test_first_success_writes_one_row_and_returns_call_id(env):
    """ADR-004: returns (output, call_id); one llm_calls row per attempt."""
    conn, cid = env
--- _types 50-100
    return obj


_ANNOTATIONS = {"title", "description", "default", "examples", "$schema", "$id", "$defs", "definitions", "format"}
_KEYWORDS = _ANNOTATIONS | {"type", "enum", "const", "required", "properties", "additionalProperties", "items", "$ref", "anyOf",
                            "maxLength", "minLength", "maximum", "minimum", "maxItems", "minItems"}


def _type_ok(v, x):
    if x == "object":
        return isinstance(v, dict)
    if x == "array":
        return isinstance(v, list)
    if x == "string":
        return isinstance(v, str)
    if x == "boolean":
        return isinstance(v, bool)
    if x == "null":
        return v is None
    if x == "integer":
        return isinstance(v, int) and not isinstance(v, bool)
    if x == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    raise LLMError(f"SCHEMA_UNSUPPORTED type {str(x)[:20]}")


def _check(v, s, path, root):
    """Fail closed: a schema keyword outside _KEYWORDS raises LLMError instead of being silently ignored."""
    if s is True or s == {}:
        return
    bad = set(s) - _KEYWORDS
    if bad:
        raise LLMError(f"SCHEMA_UNSUPPORTED keyword {sorted(bad)}")
    if "$ref" in s:
        ref = s["$ref"]
        if not ref.startswith("#/") or ref.count("/") != 2:
            raise LLMError("SCHEMA_UNSUPPORTED $ref")
        target = (root.get(ref.split("/")[1]) or {}).get(ref.split("/")[2])
        if target is None:
            raise LLMError("SCHEMA_UNSUPPORTED $ref target")
        return _check(v, target, path, root)
    if "anyOf" in s:
        errs = 0
        for sub in s["anyOf"]:
            try:
                _check(v, sub, path, root)
            except ValueError:
                errs += 1
        if errs == len(s["anyOf"]):
            raise ValueError(f"{path or '$'}: matches no anyOf branch")
    t = s.get("type")
--- _CODE
1:"""Audited call wrapper (ADR-003.7, ADR-004, LLM_VS_CODE row 20). The only entry point pipeline code uses.
14:MAX_ATTEMPTS = 3
15:RETRY_DELAYS_S = (0.5, 1.5)
16:_CODE = __import__('re').compile(r"^([A-Z][A-Z_]{2,40})\b")
18:_RETRY_NOTES = (
39:        m = _CODE.match(str(e))
56:    for attempt in range(1, MAX_ATTEMPTS + 1):
57:        u = user + _RETRY_NOTES[attempt - 1]
86:        if sleep is not None and attempt < MAX_ATTEMPTS:
87:            sleep(RETRY_DELAYS_S[attempt - 1])         # short, capped, code-controlled
--- recorder users
app/llm/provider.py:6:refused unless a `record_context(text)` for text found in evals/golden is active (ADR-004).
app/llm/provider.py:19:_record_ok = False
app/llm/provider.py:39:def assert_recordable(text: str, *, whole_file: bool = False) -> None:
app/llm/provider.py:52:def record_context(source_text: str):
app/llm/provider.py:54:    global _record_ok
app/llm/provider.py:55:    assert_recordable(source_text, whole_file=True)
app/llm/provider.py:56:    prev, _record_ok = _record_ok, True
app/llm/provider.py:60:        _record_ok = prev
app/llm/provider.py:73:        if _recording() and not _record_ok:
app/llm/provider.py:74:            raise ValueError("record mode needs record_context() over text from evals/golden")
app/llm/record.py:20:    P.assert_recordable(raw)
app/llm/record.py:34:        with P.record_context(raw):
tests/unit/test_provider.py:72:    P.assert_recordable(G.record("sample", 1)["excerpt"])
tests/unit/test_provider.py:74:        P.assert_recordable("Jane Doe, SSN 123-45-6789, real patient text")
tests/unit/test_provider_backends.py:107:            with P.record_context(bad):
tests/unit/test_provider_backends.py:109:    with P.record_context(G.raw("sample")):           # a complete golden input is accepted
tests/unit/test_provider_backends.py:112:        P.assert_recordable("a"); 
tests/unit/test_provider_backends.py:123:    with pytest.raises(ValueError):                       # live call outside record_context is refused in record mode
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:31.460Z

**tool call — Bash**
````
{
 "command": "echo \"--- log for test files\" && git log --oneline -4 -- tests/unit/test_provider.py tests/unit/test_audited.py; echo \"--- diff 958c353..HEAD for test files\" && git diff --stat 958c353 HEAD -- tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py; git diff 958c353 HEAD -- tests/unit/test_provider.py tests/unit/test_audited.py | head -150; echo \"--- HEAD sha\" && git rev-parse --short HEAD",
 "description": "Compare LLM test files between base commit and HEAD"
}
````

### User / tool · 2026-11-02T01:54:31.623Z

**tool result**
````
--- log for test files
f3da5b9 test(unit): T-048 r2 - verify-stage wiring, FixtureMissing contract, backend/provider tests, judge-failure states, AC test names
25c8312 test(unit): red LLM-stage suites (provider, audited, schemas, judges, flags, pipeline) + stubs (T-048)
--- diff 958c353..HEAD for test files
 tests/unit/test_audited.py           | 44 ++++++++++++------
 tests/unit/test_provider.py          | 88 ++++++++++++++++++++++++++++++++++--
 tests/unit/test_provider_backends.py | 37 +++++++++++++--
 3 files changed, 148 insertions(+), 21 deletions(-)
diff --git a/tests/unit/test_audited.py b/tests/unit/test_audited.py
index 04bbe0d..33486fc 100644
--- a/tests/unit/test_audited.py
+++ b/tests/unit/test_audited.py
@@ -3,6 +3,7 @@ import pytest
 from app.llm import audited as AU, provider as P
 from app.db import db as DB
 
+MISS = getattr(P, "FixtureMissing", None) or P.FixtureMiss   # T-034 AC8 name is FixtureMissing; test_provider pins that the name exists
 SCHEMA = {"type": "object", "properties": {"v": {"type": "string"}}, "required": ["v"]}
 
 @pytest.fixture
@@ -22,20 +23,24 @@ def seq(*outs):
     f.state = state
     return f
 
+def ac(conn, cid, *a, **kw):
+    """audited_call; retries are immediate (no backoff, so no sleep hook is needed - if backend adds one, patch it here)."""
+    return AU.audited_call(conn, cid, *a, **kw)
+
 def rows(conn, cid):
     return DB.table_counts(conn, cid).get("llm_calls", 0)
 
 def test_first_success_writes_one_row_and_returns_call_id(env):
     """ADR-004: returns (output, call_id); one llm_calls row per attempt."""
     conn, cid = env
-    out, call_id = AU.audited_call(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=seq({"v": "x"}))
+    out, call_id = ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=seq({"v": "x"}))
     assert out == {"v": "x"} and call_id and rows(conn, cid) == 1
 
 def test_retries_up_to_two_then_succeeds(env):
     """ADR-003.7: 1 + 2 retries; third attempt succeeds -> 3 rows."""
     conn, cid = env
     f = seq(P.LLMError("timeout"), P.LLMError("bad json"), {"v": "ok"})
-    out, _ = AU.audited_call(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
+    out, _ = ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
     assert out == {"v": "ok"} and rows(conn, cid) == 3
 
 def test_three_failures_raise_llm_failed_after_retries(env):
@@ -43,23 +48,36 @@ def test_three_failures_raise_llm_failed_after_retries(env):
     conn, cid = env
     f = seq(P.LLMError("x"))
     with pytest.raises(AU.LLMFailed) as e:
-        AU.audited_call(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
+        ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
     assert e.value.code == "LLM_FAILED_AFTER_RETRIES" and len(f.state["users"]) == 3 and rows(conn, cid) == 3
 
 def test_retries_change_something(env):
     """ADR-003.7: a retry is never an identical request - the user prompt carries a stricter-format request."""
     conn, cid = env
     f = seq(P.LLMError("x"), {"v": "ok"})
-    AU.audited_call(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
+    ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
     assert f.state["users"][0] != f.state["users"][1]
 
-def test_fixture_miss_is_never_retried(env):
-    """ADR-004 / FIXTURE_MISS: a miss is final - one attempt, FixtureMiss propagates."""
+def test_fixture_missing_is_one_attempt_and_becomes_llm_failed(env):
+    """T-034 AC8 / T-037 AC7 / FIXTURE_MISS: a miss is final (one attempt, one row); the wrapper turns it into LLMFailed(LLM_FAILED_AFTER_RETRIES) and the row logs the prompt hash."""
+    conn, cid = env
+    f = seq(MISS("abc123hash"))
+    with pytest.raises(AU.LLMFailed) as e:
+        ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
+    assert e.value.code == "LLM_FAILED_AFTER_RETRIES" and len(f.state["users"]) == 1
+    (row,) = DB.list_llm_calls(conn, cid)
+    assert "abc123hash" in (row["error"] or "")
+
+def test_audit_rows_record_model_backend_attempt_and_error_code(env):
+    """Checklist 9 / ADR-004: one row per attempt with the pinned model, backend, attempt index and a failure code; no prompt text in the error column."""
     conn, cid = env
-    f = seq(P.FixtureMiss("no recording"))
-    with pytest.raises(P.FixtureMiss):
-        AU.audited_call(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
-    assert len(f.state["users"]) == 1
+    f = seq(P.LLMError("TIMEOUT"), P.LLMError("INVALID_JSON"), {"v": "ok"})
+    ac(conn, cid, "extract", "model-x", "s", "SECRET RECORD TEXT", SCHEMA, complete_with_meta=f)
+    rs = sorted(DB.list_llm_calls(conn, cid), key=lambda r: r["attempt"])
+    assert [r["attempt"] for r in rs] == [1, 2, 3]
+    assert all(r["model"] == "model-x" and r["backend"] == "fixture" and r["step"] == "extract" for r in rs)
+    assert rs[0]["error"] and rs[1]["error"] and not rs[2]["error"]
+    assert all("SECRET RECORD TEXT" not in (r["error"] or "") for r in rs)
 
 def test_schema_invalid_output_counts_as_failed_attempt(env):
     """ADR-005 SCHEMA_INVALID: output failing `validate` is retried; after 3 -> LLMFailed."""
@@ -69,13 +87,13 @@ def test_schema_invalid_output_counts_as_failed_attempt(env):
             raise ValueError("missing v")
     f = seq({"zzz": 1})
     with pytest.raises(AU.LLMFailed):
-        AU.audited_call(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f, validate=validate)
+        ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f, validate=validate)
     assert len(f.state["users"]) == 3
 
 def test_prompts_stored_so_delete_case_removes_them(env):
     """ADR-006: prompts live in llm_calls, which delete_case empties."""
     conn, cid = env
-    AU.audited_call(conn, cid, "extract", "m", "s", "RECORD TEXT HERE", SCHEMA, complete_with_meta=seq({"v": "x"}))
+    ac(conn, cid, "extract", "m", "s", "RECORD TEXT HERE", SCHEMA, complete_with_meta=seq({"v": "x"}))
     DB.delete_case(conn, cid)
     assert rows(conn, cid) == 0
 
@@ -83,6 +101,6 @@ def test_never_prints_record_text(env, capsys, caplog):
     """Arch invariant: never log record text, prompts or responses (errors log call_id only)."""
     conn, cid = env
     with pytest.raises(AU.LLMFailed):
-        AU.audited_call(conn, cid, "extract", "m", "s", "SECRET RECORD TEXT", SCHEMA, complete_with_meta=seq(P.LLMError("SECRET RECORD TEXT in error")))
+        ac(conn, cid, "extract", "m", "s", "SECRET RECORD TEXT", SCHEMA, complete_with_meta=seq(P.LLMError("SECRET RECORD TEXT in error")))
     out = capsys.readouterr()
     assert "SECRET RECORD TEXT" not in out.out + out.err + caplog.text
diff --git a/tests/unit/test_provider.py b/tests/unit/test_provider.py
index 4b9b338..f903e01 100644
--- a/tests/unit/test_provider.py
+++ b/tests/unit/test_provider.py
@@ -3,6 +3,7 @@ import json
 import pytest
 from app.llm import provider as P
 
+MISS = getattr(P, "FixtureMissing", None) or P.FixtureMiss
 SCHEMA = {"type": "object", "properties": {"summary": {"type": "string"}}, "required": ["summary"], "additionalProperties": False}
 
 @pytest.fixture
@@ -28,9 +29,24 @@ def test_fixture_hit_returns_recorded_output(fx):
     assert P.complete("m", "s", "u", SCHEMA) == {"summary": "ok"}
 
 def test_fixture_miss_raises_never_invents(fx):
-    """ADR-004: a miss raises FixtureMiss (an LLMError); no answer is invented."""
-    with pytest.raises(P.FixtureMiss):
+    """ADR-004 / T-034 AC8: a miss raises FixtureMissing (an LLMError) carrying the prompt hash; no answer is invented."""
+    with pytest.raises(MISS) as e:
         P.complete("m", "s", "nothing recorded", SCHEMA)
+    assert isinstance(e.value, P.LLMError) and e.value.prompt_hash == P.prompt_hash("m", "s", "nothing recorded", SCHEMA)
+
+def test_fixture_missing_name_is_exported():
+    """T-034 AC8 / T-037 AC7: the exception is called FixtureMissing (one spelling across app, tests and docs)."""
+    assert hasattr(P, "FixtureMissing") and issubclass(P.FixtureMissing, P.LLMError)
+
+def test_fixture_miss_reports_hash_not_text(fx, caplog, capsys):
+    """T-034 AC8 + arch invariant: the miss message carries the prompt hash (the audited row stores it) and never the prompt text; nothing is printed."""
+    import logging
+    caplog.set_level(logging.DEBUG)
+    with pytest.raises(MISS) as e:
+        P.complete("m", "s", "SECRET RECORD TEXT", SCHEMA)
+    out = capsys.readouterr()
+    assert P.prompt_hash("m", "s", "SECRET RECORD TEXT", SCHEMA) in str(e.value)
+    assert "SECRET RECORD TEXT" not in str(e.value) + caplog.text + out.out + out.err
 
 def test_meta_surfaces_recorded_from(fx):
     """ADR-004 / ADR-003: LLMResult carries backend='fixture' and recorded_from for the audit trail."""
@@ -43,16 +59,80 @@ def test_schema_invalid_recording_is_llmerror(fx):
     put(fx, "m", "s", "u", {"summary": 5, "extra": 1})
     with pytest.raises(P.LLMError) as e:
--- HEAD sha
a90d1b0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:45.239Z

**tool call — Bash**
````
{
 "command": "git log --oneline -6 && echo \"HEAD=$(git rev-parse --short HEAD)\" && git merge-base --is-ancestor b1803c0 HEAD && echo \"b1803c0 is ancestor of HEAD\" ; echo \"--- probes\" && .venv/bin/python - <<'EOF'\nimport os, json\nos.environ.pop(\"RECORD_FIXTURES\", None)\nfrom app.llm import provider as P, audited as AU, _types as T\nfrom app.llm.backends import claude_cli as CLI\nfrom app.db import db as DB\nimport tempfile, logging, io\n\ndef tryit(label, fn):\n    try:\n        r = fn(); print(f\"{label}: no error ({r!r})\")\n    except Exception as e:\n        print(f\"{label}: {type(e).__name__}: {str(e)[:120]}\")\n\n# recorder guard\ntryit(\"assert_recordable('a')\", lambda: P.assert_recordable(\"a\"))\ntryit(\"assert_recordable('the')\", lambda: P.assert_recordable(\"the\"))\ntryit(\"assert_recordable('2019')\", lambda: P.assert_recordable(\"2019\"))\ntryit(\"record_context('a')\", lambda: P.record_context(\"a\").__enter__())\ng = sorted(P.GOLDEN_DIR.glob(\"*.txt\"))[0]\ntryit(\"record_context(full golden)\", lambda: P.record_context(g.read_text()).__enter__())\ntryit(\"assert_recordable(20-char fragment)\", lambda: P.assert_recordable(g.read_text()[:25]))\n\n# schema validator\nS = lambda **kw: dict(type=\"object\", properties={\"s\": dict(type=\"string\", **kw)}, required=[\"s\"])\ntryit(\"maxLength 3 on 10 chars\", lambda: T.validate_schema({\"s\": \"x\"*10}, S(maxLength=3)))\ntryit(\"maximum 10 on 99999\", lambda: T.validate_schema({\"n\": 99999}, {\"type\":\"object\",\"properties\":{\"n\":{\"type\":\"integer\",\"maximum\":10}}}))\ntryit(\"anyOf non-match\", lambda: T.validate_schema({\"s\": \"z\"}, {\"type\":\"object\",\"properties\":{\"s\":{\"anyOf\":[{\"enum\":[\"a\"]},{\"enum\":[\"b\"]}]}}}))\ntryit(\"unknown keyword 'pattern'\", lambda: T.validate_schema({\"s\": \"z\"}, {\"type\":\"object\",\"properties\":{\"s\":{\"type\":\"string\",\"pattern\":\"^a\"}}}))\ntryit(\"unknown type 'foo'\", lambda: T.validate_schema({\"s\": \"z\"}, {\"type\":\"object\",\"properties\":{\"s\":{\"type\":\"foo\"}}}))\ntryit(\"extra key\", lambda: T.validate_schema({\"s\": \"z\", \"x\": 1}, {\"type\":\"object\",\"properties\":{\"s\":{\"type\":\"string\"}},\"additionalProperties\":False}))\n\n# claude-cli child env\nos.environ[\"ANTHROPIC_AUTH_TOKEN\"]=\"tok-probe\"; os.environ[\"ANTHROPIC_BASE_URL\"]=\"http://evil\"; os.environ[\"ANTHROPIC_API_KEY\"]=\"sk-probe\"; os.environ[\"AWS_SECRET_ACCESS_KEY\"]=\"aws-probe\"\nenv = CLI.child_env()\nprint(\"child_env keys:\", sorted(env.keys()))\nprint(\"ANTHROPIC/AWS in child env:\", [k for k in env if k.startswith((\"ANTHROPIC\",\"AWS\"))])\n\n# audit error column with injected model key\ndef mk_fn(exc_or_out):\n    def f(model, system, user, schema):\n        if isinstance(exc_or_out, Exception): raise exc_or_out\n        return P.LLMResult(output=exc_or_out, backend=\"fixture\", model_resolved=model)\n    return f\nd = tempfile.mkdtemp()\nconn = DB.connect(os.path.join(d, \"a.sqlite\")); cid = DB.create_case(conn, \"SYNTHETIC\", now=1.0)\nSCH={\"type\":\"object\",\"properties\":{\"s\":{\"type\":\"string\"}},\"required\":[\"s\"],\"additionalProperties\":False}\ninj = \"<img src=x onerror=alert(1)>\"\ntry:\n    AU.audited_call(conn, cid, \"extract\", \"m\", \"s\", \"u\", SCH, complete_with_meta=mk_fn({\"s\":\"ok\", inj: 1}), validate=lambda o: P.validate_schema(o, SCH))\nexcept Exception as e: print(\"audited raised:\", type(e).__name__, e.code if hasattr(e,'code') else '')\nrows = DB.list_llm_calls(conn, cid)\nprint(\"error column values:\", [r[\"error\"] for r in rows])\nprint(\"injected string in any error column:\", any(inj in (r[\"error\"] or \"\") for r in rows))\n\n# fixture-miss: hash in log, not text; one attempt; sleep seam\nimport app.llm.backends.fixture as FX\ncid2 = DB.create_case(conn, \"SYNTHETIC\", now=2.0)\ncaplog_stream = io.StringIO(); h = logging.StreamHandler(caplog_stream); logging.getLogger().addHandler(h)\nnaps=[]\ndef miss(model, system, user, schema): raise P.FixtureMissing(P.prompt_hash(model, system, user, schema))\ntry:\n    AU.audited_call(conn, cid2, \"extract\", \"m\", \"s\", \"SECRET RECORD TEXT\", SCH, complete_with_meta=miss, sleep=naps.append)\nexcept AU.LLMFailed as e: print(\"miss ->\", type(e).__name__, e.code)\nlogging.getLogger().removeHandler(h)\nph = P.prompt_hash(\"m\",\"s\",\"SECRET RECORD TEXT\"+AU._RETRY_NOTES[0], SCH)\nlogtxt = caplog_stream.getvalue()\nprint(\"miss log line:\", logtxt.strip()[:200])\nprint(\"miss log contains prompt text:\", \"SECRET RECORD TEXT\" in logtxt)\nprint(\"sleep calls on miss (expect []):\", naps)\nprint(\"rows for miss:\", len(DB.list_llm_calls(conn, cid2)))\nEOF",
 "description": "Check HEAD ancestry and probe each minor and major fix"
}
````

### User / tool · 2026-11-02T01:54:45.448Z

**tool result**
````
40c882d feat(evals): eval runner with ship bar, spec check, freshness hashes, lexicon recall (T-038, code-only part)
a90d1b0 fix(backend): T-041 r1 - verbatim-excerpt guard, export endpoint and edge tests
b1803c0 fix(backend): FixtureMissing, hash log, sleep seam, fail-closed schema validator, recorder guard, cli env allowlist (T-034 r1)
117f2ec feat(frontend): input, banners, timeline, Why?, rejected tray, source-record modal (T-042)
11ab4fb test: T-039 review fixes - complete E2E hook contract, record_ids helpers, non-vacuous assertions
1c8a24d fix(evals): record_warning vocabulary per ADR-013, case_01 date_ambiguous warning
HEAD=40c882d
b1803c0 is ancestor of HEAD
--- probes
llm call failed call_id=c9cdf0750ac75 step=extract attempt=1
llm call failed call_id=c5b3fd04b946c step=extract attempt=2
llm call failed call_id=c058b4209ff44 step=extract attempt=3
assert_recordable('a'): ValueError: text is not an evals/golden input; refusing to record
assert_recordable('the'): ValueError: text is not an evals/golden input; refusing to record
assert_recordable('2019'): ValueError: text is not an evals/golden input; refusing to record
record_context('a'): ValueError: text is not an evals/golden input; refusing to record
record_context(full golden): no error (None)
assert_recordable(20-char fragment): no error (None)
maxLength 3 on 10 chars: LLMError: SCHEMA_INVALID .s: too long
maximum 10 on 99999: LLMError: SCHEMA_INVALID .n: above maximum
anyOf non-match: LLMError: SCHEMA_INVALID .s: matches no anyOf branch
unknown keyword 'pattern': LLMError: SCHEMA_UNSUPPORTED keyword ['pattern']
unknown type 'foo': LLMError: SCHEMA_UNSUPPORTED type foo
extra key: LLMError: SCHEMA_INVALID $: unexpected key
child_env keys: ['HOME', 'LOGNAME', 'PATH', 'TMPDIR', 'USER']
ANTHROPIC/AWS in child env: []
audited raised: LLMFailed LLM_FAILED_AFTER_RETRIES
error column values: ['SCHEMA_INVALID', 'SCHEMA_INVALID', 'SCHEMA_INVALID']
injected string in any error column: False
miss -> LLMFailedFixtureMiss LLM_FAILED_AFTER_RETRIES
miss log line: llm call failed call_id=cb67aee9e496b step=extract attempt=1 prompt_hash=a3a128eb989be74ee040a3aae2c58601e688166870a94616ce23326192ae22a3
miss log contains prompt text: False
sleep calls on miss (expect []): []
rows for miss: 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:57.367Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD=$(git rev-parse --short HEAD) $(git log -1 --format=%s)\" && .venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q 2>&1 | tail -3; echo \"--- status of scoped paths\"; git status --short -- tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py app/llm; echo \"(end status)\"; echo \"--- build_argv\"; sed -n '30,46p' app/llm/backends/claude_cli.py; echo \"--- Dockerfile/ZLAYT_DEV\"; ls Dockerfile* 2>&1; grep -rn \"ZLAYT_DEV\" --include=*.py --include=*.md --include=Makefile . 2>/dev/null | grep -v \"\\.venv\" | head -5; echo \"--- record.py 15-36\"; sed -n '15,36p' app/llm/record.py",
 "description": "Rerun pinned pytest, check scoped git status, and read CLI argv and recorder"
}
````

### User / tool · 2026-11-02T01:54:57.423Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: echo "HEAD=$(git rev-parse --short HEAD) $(git log -1 --format=%s)" && .venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q 2>&1 | 
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:59.415Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log -1 --format=%s && .venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q 2>&1 | tail -3; echo \"--- status of scoped paths\"; git status --short -- tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py app/llm; echo \"(end status)\"; echo \"--- build_argv\"; sed -n '30,46p' app/llm/backends/claude_cli.py; echo \"--- Dockerfile/ZLAYT_DEV\"; ls Dockerfile* 2>&1; grep -rln \"ZLAYT_DEV\" --include=*.py --include=*.md --include=Makefile . 2>/dev/null | grep -v \"\\.venv\" | head -5; echo \"--- record.py 15-36\"; sed -n '15,36p' app/llm/record.py",
 "description": "Rerun pinned pytest, check scoped git status, and read CLI argv and recorder"
}
````

### User / tool · 2026-11-02T01:55:00.944Z

**tool result**
````
250e7b6
fix(backend): generator tests, D-028 judge reason_code, label in nonce block (T-035 r2)
........................................                                 [100%]
40 passed in 0.97s
--- status of scoped paths
(end status)
--- build_argv
def _system_with_schema(system: str, json_schema: dict) -> str:
    return (f"{system}\n\nReply with exactly one JSON object and nothing else (no prose, no code fence) "
            f"that satisfies this JSON Schema:\n{json.dumps(json_schema, sort_keys=True)}")


def build_argv(model: str, system: str, user: str, json_schema: dict) -> list:
    # --tools is variadic, so it is followed by another flag; the user prompt comes last after `--` (qa-pinned contract).
    return [os.environ.get("CLAUDE_BIN") or shutil.which("claude") or "claude", "-p", "--model", model,
            "--settings", '{"disableAllHooks":true}', "--tools", "", "--strict-mcp-config",
            "--no-session-persistence", "--output-format", "json",
            "--system-prompt", _system_with_schema(system, json_schema), "--", user]


def call(model: str, system: str, user: str, json_schema: dict, *, key: str = "") -> LLMResult:
    argv = build_argv(model, system, user, json_schema)
    env = child_env()
    cwd = tempfile.mkdtemp(prefix="zlayt-cli-")
--- Dockerfile/ZLAYT_DEV
ls: Dockerfile*: No such file or directory
board/cards/T-034.md
reviews/T-034-security.md
--- record.py 15-36
    p = pathlib.Path(path).resolve()
    golden = P.GOLDEN_DIR.resolve()
    if golden not in p.parents or p.suffix != ".txt":
        raise ValueError(f"{path} is not a .txt under evals/golden; refusing to record")
    raw = p.read_text()
    P.assert_recordable(raw)
    if P.backend_name() == "fixture":
        raise ValueError("record mode needs a live LLM_BACKEND (claude-cli or anthropic-api)")
    if not P._recording():
        raise ValueError("set RECORD_FIXTURES=1 to record")
    from app.db import db as DB
    from app.llm import audited as AU
    if run is None:
        from app.backend import pipeline as PL
        run = lambda conn, cid, text, call: PL.run_pipeline(conn, cid, text, call=call)   # noqa: E731
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        conn = DB.connect(os.path.join(d, "rec.sqlite"))
        cid = DB.create_case(conn, raw, now=0.0)
        with P.record_context(raw):
            run(conn, cid, raw, AU.make_call(conn, cid))
    return len(list(P._fixture.fixture_dir().glob("*.json")))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:55:12.461Z

**tool call — Bash**
````
{
 "command": "grep -rn \"caplog\" tests/unit/test_audited.py tests/unit/test_provider_backends.py | head; echo \"---\"; grep -rn \"prompt_hash=\" tests/ | head -5; echo \"(end)\"; grep -rn \"test_fixture_miss_logs_hash_not_text\" tests/ board/ 2>/dev/null | head -3; echo \"(end2)\"; .venv/bin/python tools/board.py --help 2>&1 | head -15",
 "description": "Check whether any test pins the miss log line and board CLI usage"
}
````

### User / tool · 2026-11-02T01:55:12.624Z

**tool result**
````
tests/unit/test_audited.py:100:def test_never_prints_record_text(env, capsys, caplog):
tests/unit/test_audited.py:106:    assert "SECRET RECORD TEXT" not in out.out + out.err + caplog.text
tests/unit/test_provider_backends.py:161:def test_no_text_in_logs(tmp_path, monkeypatch, caplog, capsys):
tests/unit/test_provider_backends.py:163:    caplog.set_level("DEBUG")
tests/unit/test_provider_backends.py:171:    assert "XYZZY" not in caplog.text + o.out + o.err
---
(end)
(end2)
usage: board.py [-h]
                {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}
                ...

Zlayt PM project board CLI

positional arguments:
  {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}

options:
  -h, --help            show this help message and exit
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:55:21.805Z

**tool call — Bash**
````
{
 "command": "git diff --stat b1803c0 HEAD -- app/llm tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py; echo \"(end diff)\"; git rev-parse --short b1803c0",
 "description": "Check whether T-034 LLM code changed after the r1 fix commit"
}
````

### User / tool · 2026-11-02T01:55:21.918Z

**tool result**
````
 app/llm/prompts/judge_amount_class_v1.md | 5 +++--
 app/llm/prompts/judge_conflict_v1.md     | 5 +++--
 app/llm/prompts/judge_faithfulness_v1.md | 5 +++--
 app/llm/prompts/judge_flag_v1.md         | 5 +++--
 4 files changed, 12 insertions(+), 8 deletions(-)
(end diff)
b1803c0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:55:50.038Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-034-security-r2.md",
 "content": "# T-034 security review, round 2 (security-reviewer, claude-haiku-5-5)\n\nVerdict: **pass**. No blockers, no majors. The round-1 major (red tests against FixtureMissing, the sleep seam and the hash-bearing miss log) is resolved and the three named files are green. All five round-1 minors are resolved or reduced to residual minors and nits; three residuals are recorded below.\n\nTree at review time: HEAD `250e7b6` (other cards committed during the review; the T-034 LLM code under `app/llm/` and the three test files are unchanged since `b1803c0`, the round-1 fix commit. Only four judge prompt `.md` files changed in the same range, which are outside this card and were not reviewed for content).\n\nPytest, quoted verbatim:\n```\n$ .venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q 2>&1 | tail -3\n........................................                                 [100%]\n40 passed in 0.97s\n```\nRound 1 was `12 failed, 25 passed`. An earlier run in this round also gave `40 passed in 0.95s`.\n\n## Major (round 1): resolved\n- `FixtureMissing` exists and is exported. `app/llm/provider.py:15` re-exports it, `app/llm/_types.py:11` defines it, and `_types.py:19` keeps `FixtureMiss` as an alias.\n- The `sleep` seam exists. `app/llm/audited.py:53` takes `sleep=None`, and `audited.py:86-87` calls `sleep(RETRY_DELAYS_S[attempt - 1])` only for non-final attempts. `tests/unit/test_provider_backends.py:184-190` checks that the naps are capped at 2 s and that `sleep` is injectable.\n- The miss is logged with the prompt hash. `audited.py:83`: `log.warning(\"llm call failed call_id=%s step=%s attempt=%d%s\", ..., f\" prompt_hash={h}\" if fixture_miss else \"\")`. A fixture miss is one attempt and one row, and it raises `LLMFailedFixtureMiss` (`audited.py:85`).\n- The tests were tightened, not loosened. The `FixtureMiss` expectations became `FixtureMissing` plus `LLM_FAILED_AFTER_RETRIES` (`git diff 958c353 HEAD -- tests/unit/test_audited.py`). The test edits were committed in `f3da5b9` (T-048).\n\n## Minor findings (round 1): status\n1. Recorder guard. Largely resolved. `record_context` now requires a whole-file golden match. Residual is nit 3 below.\n2. Schema validator. Resolved. Probes show `maxLength`, `maximum` and `anyOf` are enforced, and unknown keywords and types fail closed (see Exercised).\n3. claude-cli child env. The env part is resolved. The gating and argv-prompt parts of the same round-1 finding remain open; see minor 2 below.\n4. Audit error column. Resolved. Only codes are stored.\n\n## Findings\n\n**minor 1. The miss-log hash line has no test.** `audited.py:83` logs `prompt_hash=<sha256>` on a miss, and the probe shows it. But `grep -rn \"prompt_hash=\" tests/` returns nothing, and no test named `test_fixture_miss_logs_hash_not_text` exists (the round-1 acceptance name). `tests/unit/test_provider.py:41` `test_fixture_miss_reports_hash_not_text` checks the exception message and that the prompt text is absent from caplog. It does not check that the hash is in the log. A future edit could drop the suffix and every test would stay green.\n\n**minor 2. claude-cli gating and argv prompt remain open.** `app/llm/provider.py:72-76` selects `claude-cli` on `LLM_BACKEND` alone, with no dev flag. `grep -rln ZLAYT_DEV` (code, md, Makefile) matches only `board/cards/T-034.md` and `reviews/T-034-security.md`, so no gate exists. `app/llm/backends/claude_cli.py:37-40` puts the user prompt in argv after `--` (the comment marks it as a qa-pinned contract), so the record text is visible in `ps` on a shared box. `ls Dockerfile*` returns \"No such file or directory\", so this is not exploitable in a public build yet. It is still checklist 16 and must close before the Docker card.\n\n**nit 3. Recorder guard residual.** `app/llm/provider.py:36` sets `MIN_FRAGMENT = 20` and `provider.py:42-46` still accepts any 20-character substring of a golden file when `whole_file` is false. `record_context` (`provider.py:52`) is still public. Record writes are gated by the whole-file check, so this is not exploitable: the probe shows `record_context('a')` raises `ValueError`, and `record_context(<full golden text>)` is accepted. `app/llm/record.py:20` uses the fragment default as a pre-check only.\n\n## Checks against the brief\n- Retries are capped at 3 and the timeout is 120 s (`audited.py:14`, `claude_cli.py:12`). Pass.\n- `ANTHROPIC_*` and cloud credentials are absent from the CLI child env. Pass.\n- Audit error column holds codes only (`audited.py:36-42`, `:67-68`). Pass.\n- The LLM prompt-injection record cannot change the schema (`_types.py:54-55`, `:76-82`). Pass.\n\nOutside my lens: whether the `llm_calls` retention and prompt storage meet the rules (privacy-compliance-reviewer).\n\n```json\n{\"card\": \"T-034\", \"persona\": \"security-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"HEAD 250e7b6 working tree; LLM code app/llm/{provider,audited,_types,record}.py and backends/{claude_cli,anthropic_api,fixture}.py unchanged since b1803c0; tests/unit/test_provider.py, test_audited.py, test_provider_backends.py at HEAD; no app URL (library card)\",\n \"exercised\": [\n  \"git rev-parse --short HEAD -> 250e7b6; git log -1 -> 'fix(backend): generator tests, D-028 judge reason_code, label in nonce block (T-035 r2)'\",\n  \"git merge-base --is-ancestor b1803c0 HEAD -> ancestor; git diff --stat b1803c0 HEAD -- app/llm tests/unit/test_provider*.py tests/unit/test_audited.py -> only 4 judge prompt .md files differ\",\n  \".venv/bin/python -m pytest tests/unit/test_provider.py tests/unit/test_audited.py tests/unit/test_provider_backends.py -q 2>&1 | tail -3 -> '40 passed in 0.97s' (run twice; 40 passed in 0.95s on the earlier run)\",\n  \"git status --short on the three test files and app/llm -> empty (clean)\",\n  \"git diff 958c353 HEAD -- tests/unit/test_audited.py tests/unit/test_provider.py (read in full) to confirm the tightening, not loosening\",\n  \"grep -n on app/llm for FixtureMissing, FixtureMiss, sleep, prompt_hash, maxLength, maximum, anyOf, _KEYWORDS, child_env, ENV_ALLOW, _CODE, log.warning; grep -rn in tests/ for sleep, caplog, prompt_hash=, test_fixture_miss_logs_hash_not_text\",\n  \"grep -rln ZLAYT_DEV across repo (code, md, Makefile); ls Dockerfile* -> no such file\",\n  \"read provider.py, audited.py, _types.py (validator 50-150), claude_cli.py (1-75), record.py (15-36) in full\",\n  \"probe via .venv/bin/python heredoc (no file written): assert_recordable('a'|'the'|'2019') -> ValueError; record_context('a') -> ValueError; record_context(full golden) -> accepted; validate_schema maxLength 3 on 10 chars -> SCHEMA_INVALID too long; maximum 10 on 99999 -> SCHEMA_INVALID above maximum; anyOf non-match -> SCHEMA_INVALID matches no anyOf branch; unknown keyword 'pattern' -> SCHEMA_UNSUPPORTED keyword; unknown type 'foo' -> SCHEMA_UNSUPPORTED type foo; extra key -> SCHEMA_INVALID unexpected key\",\n  \"probe child_env() with ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL, ANTHROPIC_API_KEY, AWS_SECRET_ACCESS_KEY set -> keys ['HOME','LOGNAME','PATH','TMPDIR','USER']; no ANTHROPIC/AWS key\",\n  \"probe audited_call with schema-invalid output containing key '<img src=x onerror=alert(1)>' -> error column ['SCHEMA_INVALID' x3]; injected string in any row: False\",\n  \"probe audited_call with FixtureMissing and sleep=naps.append -> LLMFailedFixtureMiss LLM_FAILED_AFTER_RETRIES; warning line 'llm call failed ... attempt=1 prompt_hash=a3a128eb...'; prompt text in log: False; sleep calls: []; rows: 1\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"retry_timeout_caps\": 5, \"claude_cli_isolation\": 4, \"key_handling\": 5, \"log_hygiene\": 5, \"fixture_recorder_guard\": 4, \"output_schema_validation\": 5, \"audit_error_column\": 5, \"ac_conformance\": 4},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"The miss-log hash line (prompt_hash=) is not pinned by any test\",\n   \"evidence\": \"app/llm/audited.py:83 log.warning(... prompt_hash={h} if fixture_miss); grep -rn 'prompt_hash=' tests/ returns nothing; tests/unit/test_provider.py:41 test_fixture_miss_reports_hash_not_text checks only str(e.value) and absence of prompt text in caplog; round-1 acceptance name test_fixture_miss_logs_hash_not_text does not exist\",\n   \"why_it_matters\": \"The hash in the miss log is the audit trail that makes a silent fixture miss visible (LLM09). Nothing fails if the suffix is removed from audited.py:83.\",\n   \"fix\": \"In tests/unit/test_audited.py add a test that runs audited_call with a FixtureMissing carrying a known hash under caplog at WARNING, and asserts 'prompt_hash=' + that hash is in caplog.text and the prompt text is not.\",\n   \"acceptance_test\": \"pytest tests/unit/test_audited.py -q passes with the new test, and fails when the prompt_hash suffix at app/llm/audited.py:83 is removed.\"},\n  {\"severity\": \"minor\", \"title\": \"claude-cli is selectable with one env var and puts the prompt on argv (round-1 finding 4, remainder)\",\n   \"evidence\": \"app/llm/provider.py:72-76 selects claude-cli on LLM_BACKEND alone; no ZLAYT_DEV gate in code (grep -rln ZLAYT_DEV hits only board/cards/T-034.md and reviews/T-034-security.md); app/llm/backends/claude_cli.py:37-40 build_argv ends with '--', user (prompt on argv, comment: qa-pinned contract); ls Dockerfile* -> No such file or directory\",\n   \"why_it_matters\": \"Checklist 16 requires the dev-only claude-cli backend to be impossible to enable in the container or public config. Today it is one env var away. Pasted record text in argv is visible to other local users via ps. Not exploitable yet because no Dockerfile exists.\",\n   \"fix\": \"Raise BACKEND_UNAVAILABLE for claude-cli unless ZLAYT_DEV=1 is set. When the Docker card lands, exclude app/llm/backends/claude_cli.py from the image and fail startup if LLM_BACKEND=claude-cli. Move the prompt to stdin if the CLI supports it, or record the qa-pinned argv exception in the card.\",\n   \"acceptance_test\": \"with ZLAYT_DEV unset and LLM_BACKEND=claude-cli, provider.complete raises LLMError starting BACKEND_UNAVAILABLE; with ZLAYT_DEV=1 it proceeds to the subprocess call.\"},\n  {\"severity\": \"nit\", \"title\": \"Recorder guard: fragment path and public record_context remain\",\n   \"evidence\": \"app/llm/provider.py:36 MIN_FRAGMENT = 20; provider.py:42-46 'if t == g or (not whole_file and t in g)'; provider.py:52 def record_context (public); app/llm/record.py:20 P.assert_recordable(raw) uses the fragment default\",\n   \"why_it_matters\": \"Record writes are still gated by whole-file record_context (record.py:34; probe: record_context('a') raises ValueError, full golden text accepted), so this is not exploitable. Keeping a 20-character substring path and a public context manager leaves an easy way to widen the gate later.\",\n   \"fix\": \"Make record_context private to record.py, and call assert_recordable(raw, whole_file=True) in record.py:20.\",\n   \"acceptance_test\": \"P.record_context('2019') and P.record_context('x'*25) raise ValueError; record.py calls the whole-file check; full golden text is accepted.\"}\n ],\n \"whats_right\": [\n  \"The schema validator now fails closed: probes show maxLength, maximum and anyOf are enforced, and unknown keywords and types raise SCHEMA_UNSUPPORTED instead of passing.\",\n  \"claude-cli child env is an allowlist (app/llm/backends/claude_cli.py:25-27); ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL and cloud keys are absent from the child env in the probe.\",\n  \"The audit error column stores only codes; the injected key '<img src=x onerror=alert(1)>' appears in no llm_calls row, and a fixture-miss row carries the hash, not the prompt text.\"],\n \"questions_for_chris\": [\"Should the T-034 card's acceptance-test name (test_fixture_miss_logs_hash_not_text) be updated to match the existing test_fixture_miss_reports_hash_not_text, or should minor 1 add the log-line test under the card's name?\"]}\n```\n"
}
````

### User / tool · 2026-11-02T01:55:50.186Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-034-security-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:55:52.391Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport json,re\nt=open(\"reviews/T-034-security-r2.md\").read()\nm=re.findall(r\"```json\\n(.*?)\\n```\", t, re.S)\nprint(\"json blocks:\", len(m))\nd=json.loads(m[0])\nprint(\"parsed ok; verdict:\", d[\"verdict\"], \"model:\", d[\"model\"], \"findings:\", [f[\"severity\"] for f in d[\"findings\"]])\nEOF\necho \"--- board validate\"; .venv/bin/python tools/board.py validate 2>&1 | tail -5",
 "description": "Parse the review JSON block and run the board validator"
}
````

### User / tool · 2026-11-02T01:55:52.556Z

**tool result**
````
json blocks: 1
parsed ok; verdict: pass model: claude-haiku-5-5 findings: ['minor', 'minor', 'nit']
--- board validate
ok (49 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:55:57.137Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md",
 "content": "---\nname: round2-review-workflow\ndescription: Workflow gotchas for round-2 re-reviews (HEAD moves mid-review, git-guard blocks $() in echo, probes without scratch files)\nmetadata:\n  type: feedback\n---\n\nRound-2 re-reviews of a card: pin the commit you actually tested. Other agents commit to the same repo during a review, so HEAD moved from b1803c0 to 250e7b6 within one session. Run `git rev-parse --short HEAD` in the same call as the pytest run and quote both in the review.\n\nThe git-guard PreToolUse hook rejects Bash commands that put `$(...)` substitutions in an `echo` or similar command position (\"unresolved variable or substitution in command position\"). Use one command per git query instead of nesting substitutions.\n\nProbes of minor fixes can run as `.venv/bin/python - <<'EOF' ... EOF` on stdin, so no scratch file is written and nothing needs a path under reviews/ or the scratchpad.\n\n**Why:** T-034 round 2 (2026-11-01): the first `$()` echo was blocked, and HEAD changed between my pytest run and my final grep.\n**How to apply:** when re-reviewing, check HEAD before and after the pytest run, and quote the sha with the test output. Keep git commands separate.\n"
}
````

### User / tool · 2026-11-02T01:55:57.231Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:55:58.860Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md",
 "old_string": "- [Hook/guard review patterns](project_hook_guard_review_patterns.md) — recurring bypass classes in git-guard/board-guard/check_secrets and reviewer-workflow gotchas",
 "new_string": "- [Hook/guard review patterns](project_hook_guard_review_patterns.md) — recurring bypass classes in git-guard/board-guard/check_secrets and reviewer-workflow gotchas\n- [Round-2 review workflow](feedback_round2_review_workflow.md) — HEAD moves mid-review, git-guard blocks $() in echo, probe via stdin not scratch files"
}
````

### User / tool · 2026-11-02T01:55:58.975Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:56:00.284Z

T-034 round 2 passes: `40 passed in 0.97s` at HEAD 250e7b6, and the major is resolved. Review is at `/Users/arsis/zlayt-pm-project/reviews/T-034-security-r2.md` (verdict pass, 0 blockers, 0 majors, 2 minors, 1 nit; `board.py validate` ok).
