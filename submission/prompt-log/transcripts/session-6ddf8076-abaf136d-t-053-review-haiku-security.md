# Subagent: T-053 review (haiku security) (T-053 review (haiku security))

Source: `agent-abaf136db1988a8ec.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:12:45.909Z

Working directory: /Users/arsis/zlayt-pm-project. Review T-053 "Multi-case: case list + switcher (local mode only), library loader" (AC: `python3 tools/board.py show T-053`). Run the tests the card names and quote. Verify: GET /api/cases lists only when ZLAYT_MODE=local and 404 otherwise (start the app on a free port twice with/without the env var, background, kill after, curl); library cases loadable; two cases' decisions don't leak (test); UI switcher present only in local mode. Write reviews/T-053-security.md (D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:12:46.920Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/security.md"
}
````

### User / tool · 2026-11-02T02:12:46.928Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:12:47.125Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T02:12:47.132Z

**tool result**
````
1	- [Hook/guard review patterns](project_hook_guard_review_patterns.md) — recurring bypass classes in git-guard/board-guard/check_secrets and reviewer-workflow gotchas
2	- [Round-2 review workflow](feedback_round2_review_workflow.md) — HEAD moves mid-review, git-guard blocks $() in echo, probe via stdin not scratch files
3	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:12:47.453Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-053",
 "description": "Show card T-053 from the board"
}
````

### User / tool · 2026-11-02T02:12:47.585Z

**tool result**
````
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
updated_at: "2026-11-02T02:12:46Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:11:36Z"
rounds: 0
commits: ["2c2eb1f"]
reviews: []
ac:
  - {"n": 1, "text": "GET /api/cases lists cases only in local mode; 404 in demo/public mode (test)", "done": true, "evidence": "test_api_routes::test_case_list_and_library_exist_only_in_local_mode (404 in demo, list+library+library load in local)"}
  - {"n": 2, "text": "UI case switcher in local mode; library cases loadable in one click; cases isolated (T-050)", "done": false, "evidence": null}
  - {"n": 3, "text": "E2E: two cases reviewed side by side, decisions do not leak between cases", "done": false, "evidence": null}
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

## Handoff
API half: list/library/library-load, local-mode gated, isolated cases; 23 route tests pass; api.md updated (audit public vs local shapes, new routes). Left: AC2 UI switcher (frontend card), AC3 browser E2E (qa), loader will pick up evals/library once T-052 lands.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:12:50.567Z

**tool call — Bash**
````
{
 "command": "ls -la && ls reviews artifacts 2>/dev/null; ls .venv/bin/python 2>/dev/null; cat Makefile 2>/dev/null | head -60; find . -path ./.venv -prune -o -path ./node_modules -prune -o -type f -name '*.py' -print | grep -v '/\\.' | head -100",
 "description": "List project root, reviews dir, and Python files"
}
````

### User / tool · 2026-11-02T02:12:50.690Z

**tool result**
````
total 200
drwxr-xr-x   25 arsis  staff    800 Nov  1 20:05 .
drwxr-xr-x+  99 arsis  staff   3168 Nov  1 20:12 ..
drwxr-xr-x    9 arsis  staff    288 Nov  1 18:18 .claude
-rw-r--r--    1 arsis  staff     29 Nov  1 17:49 .env
drwxr-xr-x@  13 arsis  staff    416 Nov  1 20:12 .git
-rw-r--r--@   1 arsis  staff    403 Nov  1 19:05 .gitignore
drwxr-xr-x@   6 arsis  staff    192 Nov  1 18:07 .pytest_cache
drwxr-xr-x@   6 arsis  staff    192 Nov  1 18:02 .venv
-rw-r--r--@   1 arsis  staff   6708 Nov  1 18:39 CLAUDE.md
-rw-r--r--@   1 arsis  staff  83742 Nov  1 18:01 MASTER_PROMPT.md
drwxr-xr-x@  11 arsis  staff    352 Nov  1 19:55 app
drwxr-xr-x@   6 arsis  staff    192 Nov  1 18:20 artifacts
drwxr-xr-x@  12 arsis  staff    384 Nov  1 20:12 board
drwxr-xr-x@   3 arsis  staff     96 Nov  1 20:11 data
drwxr-xr-x@   2 arsis  staff     64 Nov  1 18:03 deploy
drwxr-xr-x    6 arsis  staff    192 Nov  1 19:14 docs
drwxr-xr-x@   9 arsis  staff    288 Nov  1 20:12 evals
drwxr-xr-x@  12 arsis  staff    384 Nov  1 20:00 memory
drwxr-xr-x@  15 arsis  staff    480 Nov  1 18:50 personas
drwxr-xr-x@  12 arsis  staff    384 Nov  1 20:12 research
drwxr-xr-x@ 113 arsis  staff   3616 Nov  1 20:12 reviews
drwxr-xr-x    5 arsis  staff    160 Nov  1 18:40 spec
drwxr-xr-x@   4 arsis  staff    128 Nov  1 18:12 submission
drwxr-xr-x@   8 arsis  staff    256 Nov  1 20:09 tests
drwxr-xr-x@  15 arsis  staff    480 Nov  1 20:05 tools
artifacts:
m0-smoke
review-evidence
screenshots
tmp

reviews:
CONTRACT-M2M3-paralegal.md
CONTRACT-M2M3-product-manager.md
CONTRACT-M2M3-staff-engineer.md
GATE-M0-summary.md
GATE-M1-summary.md
T-001-staff-engineer-r2.md
T-001-staff-engineer-r3.md
T-001-staff-engineer.md
T-002-staff-engineer-r2.md
T-002-staff-engineer-r3.md
T-002-staff-engineer.md
T-003-security-r2.md
T-003-security-r3.md
T-003-security.md
T-004-staff-engineer-r2.md
T-004-staff-engineer-r3.md
T-004-staff-engineer.md
T-005-product-manager-r2.md
T-005-product-manager-r3.md
T-005-product-manager.md
T-006-security-r2.md
T-006-security-r3.md
T-006-security.md
T-007-staff-engineer-r2.md
T-007-staff-engineer.md
T-008-claims-adjuster-r2.md
T-008-claims-adjuster-r3.md
T-008-claims-adjuster-r4.md
T-008-claims-adjuster.md
T-009-claims-adjuster.md
T-009-legal-nurse-r2.md
T-009-legal-nurse.md
T-010-litigation-lead-r2.md
T-010-litigation-lead-r3.md
T-010-litigation-lead.md
T-010-product-manager-r2.md
T-010-product-manager.md
T-011-product-manager-r2.md
T-011-product-manager.md
T-012-privacy-compliance-r2.md
T-012-privacy-compliance-r3.md
T-012-privacy-compliance.md
T-013-paralegal-r2.md
T-013-paralegal-r3.md
T-013-paralegal.md
T-013-product-manager-r2.md
T-013-product-manager-r3.md
T-013-product-manager.md
T-014-privacy-compliance-r2.md
T-014-privacy-compliance-r3.md
T-014-privacy-compliance.md
T-014-staff-engineer-r2.md
T-014-staff-engineer-r3.md
T-014-staff-engineer.md
T-015-legal-nurse-r2.md
T-015-legal-nurse-r3.md
T-015-legal-nurse.md
T-015-paralegal-r2.md
T-015-paralegal-r3.md
T-015-paralegal-r4.md
T-015-paralegal.md
T-016-staff-engineer.md
T-017-product-manager-r2.md
T-017-product-manager-r3.md
T-017-product-manager.md
T-018-product-manager-r2.md
T-018-product-manager.md
T-025-product-manager-r2.md
T-025-product-manager.md
T-026-ux-designer.md
T-027-legal-nurse.md
T-028-staff-engineer-r2.md
T-028-staff-engineer.md
T-029-staff-engineer-r2.md
T-029-staff-engineer.md
T-030-staff-engineer-r2.md
T-030-staff-engineer-r3.md
T-030-staff-engineer.md
T-031-staff-engineer-r2.md
T-031-staff-engineer.md
T-032-staff-engineer-r2.md
T-032-staff-engineer.md
T-033-staff-engineer-r2.md
T-033-staff-engineer.md
T-034-security-r2.md
T-034-security.md
T-035-staff-engineer-r2.md
T-035-staff-engineer.md
T-036-claims-adjuster-r2.md
T-036-claims-adjuster-r3.md
T-036-claims-adjuster.md
T-037-staff-engineer.md
T-038-staff-engineer-r2.md
T-038-staff-engineer-r3.md
T-038-staff-engineer.md
T-039-staff-engineer-r2.md
T-039-staff-engineer.md
T-040-security.md
T-041-paralegal-r2.md
T-041-paralegal.md
T-042-ux-designer-r2.md
T-042-ux-designer.md
T-043-paralegal.md
T-047-ux-designer.md
T-048-staff-engineer-r2.md
T-048-staff-engineer.md
T-049-ux-designer.md
T-050-staff-engineer.md
T-051-privacy-compliance-r2.md
T-051-privacy-compliance-r3.md
T-051-privacy-compliance.md
.venv/bin/python
./research/lexicon_selfcheck.py
./research/validate_library.py
./research/library_build.py
./evals/run.py
./evals/__init__.py
./evals/matching.py
./tools/check_secrets.py
./tools/board.py
./tools/compile_agents.py
./tools/agent_prompt.py
./tools/screenshot_board.py
./tools/export_prompt_log.py
./tools/board_server.py
./app/__init__.py
./app/pipeline.py
./app/main.py
./tests/conftest.py
./tests/__init__.py
./evals/golden/check_golden.py
./artifacts/review-evidence/T-006-r2-probe.py
./artifacts/review-evidence/T-032-ingest.py
./artifacts/review-evidence/T-015-r3-paralegal-s6diff.py
./artifacts/review-evidence/T-043-paralegal-probe2.py
./artifacts/review-evidence/T-003-r3-probe-rwg.py
./artifacts/review-evidence/T-015-r3-paralegal-jsoncheck.py
./artifacts/review-evidence/T-042-ux-designer-walk.py
./artifacts/review-evidence/T-014-r2-amount-demo.py
./artifacts/review-evidence/T-002-r3-404.py
./artifacts/review-evidence/T-025-pm-probe.py
./artifacts/review-evidence/T-012-r2-fetch.py
./artifacts/review-evidence/T-047-ux-designer-check.py
./artifacts/review-evidence/T-003-r2-probe-board2.py
./artifacts/review-evidence/T-051-r2-probe.py
./artifacts/review-evidence/T-015-r4-paralegal-jsoncheck.py
./artifacts/review-evidence/T-031-mutation.py
./artifacts/review-evidence/T-036-r2-probe4.py
./artifacts/review-evidence/T-018-r2-applied-check.py
./artifacts/review-evidence/T-036-probe3.py
./artifacts/review-evidence/T-036-r2-probe5.py
./artifacts/review-evidence/T-009-adjuster-probes.py
./artifacts/review-evidence/T-003-r3-probe-pwd.py
./artifacts/review-evidence/T-047-ux-designer-nav-keyboard.py
./artifacts/review-evidence/T-014-r3-amount-demo.py
./artifacts/review-evidence/T-039-r2-letter-stub.py
./artifacts/review-evidence/T-043-paralegal-probe3.py
./artifacts/review-evidence/T-033-golden.py
./artifacts/review-evidence/T-003-r3-probe-legit.py
./artifacts/review-evidence/T-006-r2-fp-probe.py
./artifacts/review-evidence/T-012-h2t.py
./artifacts/review-evidence/T-003-r3-probe-corpus.py
./artifacts/review-evidence/T-010-r2-count.py
./artifacts/review-evidence/T-041-r2-mutation.py
./artifacts/review-evidence/T-028-r2-checks.py
./artifacts/review-evidence/T-010-r2-srch.py
./artifacts/review-evidence/T-015-r3-paralegal-mutation.py
./artifacts/review-evidence/T-028-review-json-check.py
./artifacts/review-evidence/T-003-r2-commit-secret-probe.py
./artifacts/review-evidence/T-049-ux-designer-check.py
./artifacts/review-evidence/T-015-r2-paralegal-probe.py
./artifacts/review-evidence/T-011-r2-check.py
./artifacts/review-evidence/T-027-nurse-fresh-probe.py
./artifacts/review-evidence/T-043-paralegal-probe.py
./artifacts/review-evidence/T-014-json-check.py
./artifacts/review-evidence/T-015-r3-paralegal-entries.py
./artifacts/review-evidence/T-009-r2-nurse-variants.py
./artifacts/review-evidence/T-003-r2-probe-direct.py
./artifacts/review-evidence/T-006-r3-commit-paths-probe.py
./artifacts/review-evidence/T-009-nurse-probe.py
./artifacts/review-evidence/T-015-r2-nurse-probe.py
./artifacts/review-evidence/T-036-adjuster-probe.py
./artifacts/review-evidence/T-039-r2-mutation.py
./artifacts/review-evidence/T-025-pm-r2-probe.py
./artifacts/review-evidence/T-014-r3-amount-sim.py
./artifacts/review-evidence/T-015-r2-paralegal-jsoncheck.py
./artifacts/review-evidence/T-039-r2-jsoncheck.py
./artifacts/review-evidence/T-009-r2-nurse-probe.py
./artifacts/review-evidence/T-028-review-checks.py
./artifacts/review-evidence/T-030-exercise.py
./artifacts/review-evidence/T-028-r2-json-check.py
./artifacts/review-evidence/T-039-r2-checks.py
./artifacts/review-evidence/T-002-r3-probe.py
./artifacts/review-evidence/T-013-r3-paralegal-golden-cmp.py
./artifacts/review-evidence/T-051-r3-check.py
./artifacts/review-evidence/T-051-r2-check.py
./artifacts/review-evidence/T-013-r2-paralegal-walk.py
./artifacts/review-evidence/T-014-r2-amount-sim.py
./artifacts/review-evidence/T-018-contract-probe.py
./artifacts/review-evidence/T-002-r3-ui.py
./artifacts/review-evidence/T-005-r2-pathcheck.py
./artifacts/review-evidence/T-036-r2-validate.py
./artifacts/review-evidence/T-015-r3-paralegal-probe.py
./artifacts/review-evidence/T-003-r3-probe-targeted2.py
./artifacts/review-evidence/T-036-adjuster-probe2.py
./artifacts/review-evidence/T-013-r3-paralegal-walk.py
./artifacts/review-evidence/T-004-r2-board-guard-probe.py
./artifacts/review-evidence/T-014-amount-cue-demo.py
./artifacts/review-evidence/T-031-r2-check.py
./artifacts/review-evidence/T-013-r2-paralegal-jsoncheck.py
./artifacts/review-evidence/T-043-paralegal-probe4.py
./artifacts/review-evidence/T-013-r3-paralegal-jsoncheck.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:12:52.392Z

**tool call — Bash**
````
{
 "command": "git log --oneline -n 8 2>&1; echo ---; git show --stat 2c2eb1f 2>&1 | head -40; echo ---; find app tests deploy -type f | head -80; echo ---; cat .gitignore; echo ---; cat .env | sed -E 's/=.*/=<redacted>/'",
 "description": "Inspect git log, T-053 commit, app layout, and env file keys"
}
````

### User / tool · 2026-11-02T02:12:52.454Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to /)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:12:54.732Z

**tool call — Bash**
````
{
 "command": "git log --oneline -n 8; echo ---; git show --stat 2c2eb1f | head -40; echo ---; find app tests deploy -type f | head -80; echo ---; cat .gitignore; echo ---; cut -d= -f1 .env",
 "description": "Inspect git log, T-053 commit, app layout, and env key names"
}
````

### User / tool · 2026-11-02T02:12:54.864Z

**tool result**
````
2c2eb1f feat(backend): local-mode case list, library loader; api.md audit shapes (T-053)
5650eae docs(contract): POST /api/cases/pdf and record page (T-054)
5edd556 feat(backend): PDF text-layer upload with page-mapped citations, scanned PDFs refused (T-054)
8d485ec test(backend): replay counts failed calls, one injection warning, per-record deadline (T-037 r1)
ce191d9 feat(backend): audit endpoint is metadata-only unless ZLAYT_MODE=local (T-040)
5216d06 fix(backend): D-032 objective_negative context only, scene_facts need phrase list, one flag per prior-condition sentence
d6a89ad fix(evals): judge-unavailable is never a catch; reported separately and makes bar 4 not_measured (T-038)
7a450a1 feat(db): schema version, old files moved aside and rebuilt; stronger multi-case tests (T-050 r2, T-040)
---
commit 2c2eb1f538608f78caab151375d5e04b0c7ba268
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:12:39 2026 -0600

    feat(backend): local-mode case list, library loader; api.md audit shapes (T-053)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/api.py            | 56 +++++++++++++++++++++++++++++++++++++++----
 app/backend/present.py        | 14 +++++++++++
 memory/contracts/api.md       | 28 +++++++++++++++++-----
 tests/unit/test_api_routes.py | 28 ++++++++++++++++++++++
 4 files changed, 116 insertions(+), 10 deletions(-)
---
app/__init__.py
app/README-arch.md
app/pipeline.py
app/main.py
tests/conftest.py
tests/__init__.py
app/llm/_types.py
app/llm/provider.py
app/llm/audited.py
app/llm/lexicon.yaml
app/llm/__init__.py
app/llm/record.py
app/llm/promptlib.py
app/frontend/review.css
app/frontend/flags.js
app/frontend/review.js
app/frontend/index.html
app/frontend/styles.css
app/frontend/charges.js
app/frontend/mock_flags.js
app/frontend/timeline.js
app/frontend/mock.js
app/frontend/state.js
app/frontend/dom.js
app/frontend/mock_sample.js
app/frontend/source.js
app/frontend/api.js
app/frontend/app.js
app/frontend/input.js
app/backend/injection.py
app/backend/sentences.py
app/backend/why.py
app/backend/store.py
app/backend/ingest.py
app/backend/confidence.py
app/backend/pdf_text.py
app/backend/split_llm.py
app/backend/present.py
app/backend/flags.py
app/backend/flag_templates.py
app/backend/lexicon_scan.py
app/backend/__init__.py
app/backend/export.py
app/backend/review.py
app/backend/api.py
app/backend/lexicon.py
app/backend/generator.py
app/backend/export_routes.py
app/backend/judges.py
app/backend/schemas.py
app/backend/pipeline.py
app/backend/conflicts.py
app/backend/dates.py
app/backend/totals.py
app/backend/gaps.py
app/backend/grounding.py
app/backend/amounts.py
app/__pycache__/main.cpython-312.pyc
app/__pycache__/__init__.cpython-312.pyc
app/db/db.py
app/db/schema.sql
app/db/__init__.py
app/db/__pycache__/db.cpython-312.pyc
app/db/__pycache__/__init__.cpython-312.pyc
tests/unit/test_conflicts.py
tests/unit/test_audited.py
tests/unit/test_eval_spec_check.py
tests/unit/test_judges.py
tests/unit/test_flags_sample.py
tests/unit/test_generator.py
tests/unit/test_flags_injection.py
tests/unit/test_eval_matching.py
tests/unit/test_db.py
tests/unit/test_dates.py
tests/unit/test_totals.py
tests/unit/test_t037_backend.py
tests/unit/test_grounding.py
tests/unit/__init__.py
tests/unit/test_pdf_upload.py
tests/unit/test_provider.py
---
.env
.env.*
!.env.example
.venv/
__pycache__/
*.pyc
.pytest_cache/
node_modules/
.claude/agent-memory-local/
.claude/settings.local.json
artifacts/tmp/
board/.locks/
board/.stop_guard_state
board/.hook_debug.log
board/.server.log
app/db/*.sqlite3
*.sqlite3
.DS_Store
board/.hook_input_keys.log
board/.state.json
*.pem
*.key
id_rsa*
.envrc
*.env
.ruff_cache/
.coverage
*.log
.claude/scheduled_tasks.lock
---
ANTHROPIC_API_KEY
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:12:56.289Z

**tool call — Bash**
````
{
 "command": "git show 2c2eb1f -- app/backend/api.py app/backend/present.py tests/unit/test_api_routes.py",
 "description": "Show T-053 code diff for api, present, and tests"
}
````

### User / tool · 2026-11-02T02:12:56.387Z

**tool result**
````
commit 2c2eb1f538608f78caab151375d5e04b0c7ba268
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:12:39 2026 -0600

    feat(backend): local-mode case list, library loader; api.md audit shapes (T-053)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index 3d77fc9..654383c 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -25,6 +25,7 @@ CSP = ("default-src 'none'; script-src 'self'; script-src-attr 'unsafe-hashes' '
        "connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'") % "95nblrfVsK8W4muMQZ2m4mrNYEqpgFiSJOd2xYMkbfU="
 ROOT = pathlib.Path(__file__).resolve().parents[2]
 GOLDEN = ROOT / "evals" / "golden"
+LIBRARY = ROOT / "evals" / "library"
 VERSION = "0.1.0"
 BANNER = "Synthetic data only — never paste real records"
 AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
@@ -52,12 +53,36 @@ def recorded_hashes() -> set:
     return {digest(p.read_text()) for p in GOLDEN.glob("*.txt")}
 
 
+def library_cases() -> list:
+    """Synthetic case library (evals/library, same file format as evals/golden: <id>.txt + optional <id>.expected.json). Falls back to
+    evals/golden until the library exists. [{id, name, description, path}]"""
+    base = LIBRARY if any(LIBRARY.glob("*.txt")) else GOLDEN
+    out = []
+    for p in sorted(base.glob("*.txt")):
+        meta = {}
+        ej = p.with_name(p.stem + ".expected.json")
+        if ej.exists():
+            try:
+                meta = json.loads(ej.read_text())
+            except ValueError:
+                meta = {}
+        out.append({"id": p.stem, "name": meta.get("name") or p.stem.replace("_", " "), "description": (meta.get("description") or "")[:240], "path": p})
+    return out
+
+
+def local_mode() -> bool:
+    return os.environ.get("ZLAYT_MODE") == "local"
+
+
 def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
     db_path = db_path or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")
     os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
     app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
     app.state.db_path = db_path
     app.state.recorded = recorded_hashes()
+
+    def allowed_hashes():
+        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
     runs = {}
     DB.connect(db_path).close()
     if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
@@ -167,14 +192,37 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
                 "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
                 "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
 
+    @app.get("/api/cases")
+    def list_cases():
+        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
+            raise ApiError(404, "not_found", "Not found.")
+        c = conn()
+        try:
+            return {"cases": present.case_list(c)}
+        finally:
+            c.close()
+
+    @app.get("/api/library")
+    def library():
+        if not local_mode():
+            raise ApiError(404, "not_found", "Not found.")
+        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}
+
     @app.post("/api/cases", status_code=201)
     async def create_case(request: Request):
         b = await body_of(request)
         sample = b.get("sample") is True
-        text = (GOLDEN / "sample.txt").read_text() if sample else b.get("text")
+        lib = None
+        if isinstance(b.get("library"), str):
+            if not local_mode():
+                raise ApiError(404, "not_found", "Not found.")
+            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
+            if lib is None:
+                raise ApiError(404, "not_found", "No such library case.")
+        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
         if not isinstance(text, str):
             raise ApiError(400, "bad_request", "Provide text or sample: true.")
-        return make_case(text, b.get("name"), sample)
+        return make_case(text, b.get("name") if isinstance(b.get("name"), str) else (lib["name"] if lib else None), sample)
 
     @app.post("/api/cases/pdf", status_code=201)
     async def create_case_from_pdf(request: Request, name: str = None):
@@ -199,7 +247,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
         except ingest.IngestError as e:
             raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
-        if demo_mode() and digest(text) not in app.state.recorded:
+        if demo_mode() and digest(text) not in allowed_hashes():
             raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
         c = conn()
         try:
@@ -269,7 +317,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             case = get_case(c, token)
             if case["status"] == "running" or token in runs:
                 raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
-            if demo_mode() and digest(case["raw_text"]) not in app.state.recorded:
+            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
                 raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
             if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
                 raise ApiError(503, "llm_unavailable", "The AI service is not available.")
diff --git a/app/backend/present.py b/app/backend/present.py
index 439254a..d9be4f7 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -202,3 +202,17 @@ def audit_view(conn, case_id, full=False):
                        for e in DB.list_events(conn, case_id)],
             "summary": {"calls": len(calls), "cost_usd": round(sum(c["cost_usd"] or 0 for c in calls), 6),
                         "latency_ms_total": sum(c["latency_ms"] or 0 for c in calls), "by_backend": by}}
+
+
+def case_list(conn):
+    """Local mode only (D-008/D-031): newest first. Metadata and counts, never record text."""
+    out = []
+    for r in conn.execute("SELECT id FROM cases ORDER BY created_at DESC, rowid DESC"):
+        cid = r["id"]
+        case = DB.get_case(conn, cid)
+        counts = review_view(conn, cid)["counts"]
+        out.append({"token": cid, "name": case["name"], "status": case["status"], "source": case["source"],
+                    "record_count": conn.execute("SELECT count(*) FROM records WHERE case_id=?", (cid,)).fetchone()[0],
+                    "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},
+                    "created_at": store.iso(case["created_at"])})
+    return out
diff --git a/tests/unit/test_api_routes.py b/tests/unit/test_api_routes.py
index 2fe7cf4..6b2e730 100644
--- a/tests/unit/test_api_routes.py
+++ b/tests/unit/test_api_routes.py
@@ -273,3 +273,31 @@ def test_audit_is_metadata_only_unless_local_mode(env, monkeypatch):
     monkeypatch.setenv("ZLAYT_MODE", "local")
     full = c.get(f"/api/cases/{tok}/audit").json()
     assert full["calls"][0]["user_text"] and full["calls"][0]["system_text"] and "before" in full["events"][0]
+
+
+def test_case_list_and_library_exist_only_in_local_mode(env, monkeypatch):
+    """T-053 AC1: public/demo stays token-only (404); local mode lists cases and the library and loads a library case in one call."""
+    _, c = env
+    monkeypatch.delenv("ZLAYT_MODE", raising=False)
+    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
+    assert c.get("/api/cases").status_code == 404 and c.get("/api/library").status_code == 404
+    assert c.post("/api/cases", json={"library": "case_01_date_formats"}).status_code == 404
+    monkeypatch.setenv("ZLAYT_MODE", "local")
+    lib = c.get("/api/library").json()["cases"]
+    assert lib and "path" not in lib[0] and {"id", "name", "description"} <= set(lib[0])
+    r = c.post("/api/cases", json={"library": lib[0]["id"]})
+    assert r.status_code == 201 and r.json()["token"] != tok
+    listed = c.get("/api/cases").json()["cases"]
+    assert [x["token"] for x in listed][:2] == [r.json()["token"], tok] and {"name", "status", "record_count", "counts", "created_at"} <= set(listed[0])
+    assert "text" not in listed[0] and c.post("/api/cases", json={"library": "nope"}).status_code == 404
+
+
+def test_cases_do_not_leak_decisions_between_each_other(env, monkeypatch):
+    """T-053 AC3 (API half): decisions on one case never show on the other."""
+    _, c = env
+    monkeypatch.setenv("ZLAYT_MODE", "local")
+    a, b = run_case(c), run_case(c, G.raw("case_01_date_formats"))
+    ea = c.get(f"/api/cases/{a}").json()["entries"][0]["id"]
+    assert c.post(f"/api/cases/{a}/items/{ea}/review", json={"action": "accept"}).status_code == 200
+    la = {x["token"]: x["counts"] for x in c.get("/api/cases").json()["cases"]}
+    assert la[a]["accepted"] == 1 and la[b]["accepted"] == 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:13:05.456Z

**tool call — Bash**
````
{
 "command": "grep -rn \"ZLAYT_MODE\\|local_mode\\|demo_mode\\b\" --include=* -r app tests deploy tools evals memory/contracts CLAUDE.md 2>/dev/null | grep -v __pycache__ | head -60; echo ---; ls deploy; echo ---; cat app/main.py; echo ---; grep -rn \"def demo_mode\\|def backend\\|def live_enabled\\|def models\" -A6 app/backend/api.py",
 "description": "Locate ZLAYT_MODE usage, deploy files, and demo/backend helpers"
}
````

### User / tool · 2026-11-02T02:13:05.564Z

**tool result**
````
app/frontend/mock.js:118:    const c = { token, name, status: "ingested", demo_mode: false, backend: "fixture", models: { generator: "claude-sonnet-5-5", judge: "claude-haiku-5-5" }, records,
app/frontend/mock.js:144:      if (method === "GET" && path === "/health") return ok({ ok: true, version: "0.1.0-mock", synthetic_only: true, banner: "Synthetic data only — never paste real records", backend: "fixture", demo_mode: false, live_enabled: false,
app/frontend/mock.js:156:        return ok({ token, name: c.name, status: "ingested", source: body && body.sample ? "sample" : "paste", demo_mode: false, record_count: c.records.length, split_method: "code",
app/frontend/app.js:11:    const badge = $("#badge"); badge.textContent = h ? (h.demo_mode ? "cached demo" : (ZL.API_MODE === "mock" ? "mock API" : h.backend)) : "";
app/frontend/app.js:13:    const live = $("#retention"); live.hidden = !(h && !h.demo_mode && s.token && ZL.API_MODE !== "mock");
app/frontend/dev/mock-data.js:6: "demo_mode": true,
app/backend/present.py:143:def case_view(conn, case_id, *, backend, models, demo_mode):
app/backend/present.py:157:    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
app/backend/present.py:194:    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
app/backend/api.py:73:def local_mode() -> bool:
app/backend/api.py:74:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:85:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
app/backend/api.py:99:    def demo_mode():
app/backend/api.py:191:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
app/backend/api.py:197:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
app/backend/api.py:207:        if not local_mode():
app/backend/api.py:217:            if not local_mode():
app/backend/api.py:250:        if demo_mode() and digest(text) not in allowed_hashes():
app/backend/api.py:258:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
app/backend/api.py:271:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
app/backend/api.py:284:            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
app/backend/api.py:320:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
app/backend/api.py:322:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py:406:                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
app/backend/api.py:417:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
app/db/schema.sql:8:  stage TEXT, error TEXT, backend TEXT, demo_mode INTEGER DEFAULT 0, config_json TEXT,
tests/unit/test_api_routes.py:43:    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
tests/unit/test_api_routes.py:122:def test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode(env):
tests/unit/test_api_routes.py:262:def test_audit_is_metadata_only_unless_local_mode(env, monkeypatch):
tests/unit/test_api_routes.py:263:    """T-040 AC (T-051 privacy): public/demo audit has no prompt, response, record or edit text; ZLAYT_MODE=local adds them."""
tests/unit/test_api_routes.py:268:    monkeypatch.delenv("ZLAYT_MODE", raising=False)
tests/unit/test_api_routes.py:273:    monkeypatch.setenv("ZLAYT_MODE", "local")
tests/unit/test_api_routes.py:278:def test_case_list_and_library_exist_only_in_local_mode(env, monkeypatch):
tests/unit/test_api_routes.py:281:    monkeypatch.delenv("ZLAYT_MODE", raising=False)
tests/unit/test_api_routes.py:285:    monkeypatch.setenv("ZLAYT_MODE", "local")
tests/unit/test_api_routes.py:298:    monkeypatch.setenv("ZLAYT_MODE", "local")
tests/e2e/test_api.py:8:    """api.md health: backend fixture, demo_mode true on the public build."""
tests/e2e/test_api.py:21:def test_non_recorded_text_refused_in_demo_mode():
memory/contracts/api.md:27:| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
memory/contracts/api.md:28:| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
memory/contracts/api.md:36:  "backend": "fixture", "demo_mode": true, "live_enabled": false,
memory/contracts/api.md:43:`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every view and `ai_banner` on the review view; in live mode it also shows "Pasted text is deleted after `retention_hours` hours" with a Delete now button.
memory/contracts/api.md:53:  "demo_mode": true, "record_count": 9, "split_method": "code",
memory/contracts/api.md:90:  "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ready", "demo_mode": true,
memory/contracts/api.md:406:    "demo_mode": true,
memory/contracts/api.md:422:JSON for this case only. **Public/demo (default): metadata only**: no prompt, response, record or edit text. With `ZLAYT_MODE=local` the same call also returns the full prompts and responses and the before/after of each human event (T-040, T-051 privacy check).
memory/contracts/api.md:433:Local shape (`ZLAYT_MODE=local`): each call also has `system_text`, `user_text`, `response_raw`, `error`; each event also has `before` and `after`:
memory/contracts/api.md:442:Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays token-only and has no case list.
---
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
app/backend/api.py:93:    def backend():
app/backend/api.py-94-        return os.environ.get("LLM_BACKEND", "fixture") or "fixture"
app/backend/api.py-95-
app/backend/api.py:96:    def live_enabled():
app/backend/api.py-97-        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
app/backend/api.py-98-
app/backend/api.py:99:    def demo_mode():
app/backend/api.py-100-        return not live_enabled()
app/backend/api.py-101-
app/backend/api.py:102:    def models():
app/backend/api.py-103-        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
app/backend/api.py-104-
app/backend/api.py-105-    def conn():
app/backend/api.py-106-        return DB.connect(app.state.db_path)
app/backend/api.py-107-
app/backend/api.py-108-    def make_call(c, cid):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:13:13.235Z

**tool call — Bash**
````
{
 "command": "sed -n 105,135p app/backend/api.py; echo ...; sed -n 236,262p app/backend/api.py; echo ...; sed -n 300,345p app/backend/api.py",
 "description": "Read make_call, create/run handlers in api.py"
}
````

### User / tool · 2026-11-02T02:13:13.327Z

**tool result**
````
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
...
            if len(data) > pdf_text.MAX_PDF_BYTES:
                raise ApiError(413, "input_too_large", "The PDF is too large.")
        try:
            got = pdf_text.extract(data)
        except pdf_text.PdfError as e:
            raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
                           _PDF_MESSAGES[e.code], {"reason": e.code}) from None
        return make_case(got["text"], name, False, pdf_pages=got["pages"])

    def make_case(text, name, sample, pdf_pages=None):
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
            name = name if isinstance(name, str) else ("Sample case" if sample else None)
            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None,
                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages}} if pdf_pages else {}))
            try:
                ing = pipeline_mod().ingest_case(c, cid, text, now)
                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
...
        try:
            mod = pipeline_mod()
            mod.run_pipeline(c, token, raw, call=make_call(c, token), now=time.time)
            if DB.get_case(c, token)["status"] == "running":
                DB.update_case(c, token, status="ready", stage="finalize", run_finished_at=time.time())
        except Exception as e:                                   # code only: no message text from the pipeline
            DB.update_case(c, token, status="failed", run_finished_at=time.time(),
                           error=json.dumps({"code": getattr(e, "code", "run_failed"), "message": "The run stopped; finished items are kept."}))
        finally:
            c.close()
            runs.pop(token, None)

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
            now = time.time()
            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
            runs[token].start()
            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
        finally:
            c.close()

    @app.get("/api/cases/{token}/status")
    def status(token: str):
        c = conn()
        try:
            case = get_case(c, token)
            stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
            stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
            stages = list(stages) if not callable(stages) else STAGES
            done = stages.index(stage) if stage in stages else 0
            end = case["run_finished_at"] or time.time()
            return {"token": token, "status": case["status"], "stage": stage, "stages": stages,
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:13:16.265Z

**tool call — Bash**
````
{
 "command": "wc -l app/llm/provider.py app/llm/audited.py && sed -n 1,200p app/llm/provider.py",
 "description": "Read LLM provider selection and live-call guard"
}
````

### User / tool · 2026-11-02T02:13:16.407Z

**tool result**
````
     107 app/llm/provider.py
     107 app/llm/audited.py
     214 total
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
        if not whole_file:       # synthetic seeded-hallucination lines (their record_text) are golden input too
            import json as _json
            for p in sorted(GOLDEN_DIR.glob("hallucinations*.jsonl")):
                for line in p.read_text().splitlines():
                    if line.strip() and t in _norm(_json.loads(line).get("record_text", "")):
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


@contextlib.contextmanager
def record_fragment_context(fragment: str):
    """Judge-line recording: allow record-mode writes for a judge call whose record text is a fragment (>= MIN_FRAGMENT chars) of a golden file."""
    global _record_ok
    assert_recordable(fragment)
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
        raise LLMError(f"UNKNOWN_BACKEND {name}")
    validate_schema(res.output, json_schema)
    if name != "fixture" and _recording():
        _fixture.write(key, res, model)
    return res


def complete(model: str, system: str, user: str, json_schema: dict) -> dict:
    return complete_with_meta(model, system, user, json_schema).output
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:13:20.913Z

**tool call — Bash**
````
{
 "command": "ls app/llm/backends/ && sed -n 1,80p app/llm/backends/anthropic_api.py; echo ...; sed -n 1,107p app/llm/audited.py",
 "description": "Read anthropic-api backend and audited call wrapper"
}
````

### User / tool · 2026-11-02T02:13:21.002Z

**tool result**
````
__init__.py
__pycache__
anthropic_api.py
claude_cli.py
fixture.py
"""anthropic-api backend: Anthropic SDK, temperature 0, schema via a forced tool call. ADR-004. One attempt, no retry."""
import json
import os
import time

from app.llm._types import LLMError, LLMResult

TIMEOUT_S = 120.0
MAX_TOKENS = 4096


def make_client():
    """SDK retries are off (audited.py owns retries) and the timeout is explicit (CONTRACT 5.2)."""
    import anthropic
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"), max_retries=0, timeout=TIMEOUT_S)


def call(model: str, system: str, user: str, json_schema: dict, *, key: str = "", client=None) -> LLMResult:
    if client is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise LLMError("BACKEND_UNAVAILABLE anthropic-api has no key")
        client = make_client()
    t0 = time.monotonic()
    try:
        r = client.messages.create(
            model=model, max_tokens=MAX_TOKENS, temperature=0, system=system,
            messages=[{"role": "user", "content": user}],
            tools=[{"name": "emit", "description": "Return the answer as this JSON object.", "input_schema": json_schema}],
            tool_choice={"type": "tool", "name": "emit"})
    except Exception as e:                                   # SDK errors may echo request data: keep only the class
        raise LLMError(f"BACKEND_FAILED anthropic-api {type(e).__name__}") from None
    blocks = [b for b in (getattr(r, "content", None) or []) if getattr(b, "type", "") == "tool_use"]
    if not blocks or not isinstance(blocks[0].input, dict):
        raise LLMError("INVALID_JSON: no tool_use object in reply")
    out = blocks[0].input
    u = getattr(r, "usage", None)
    return LLMResult(output=out, backend="anthropic-api", model_resolved=getattr(r, "model", model) or model,
                     latency_ms=int((time.monotonic() - t0) * 1000), tokens_in=int(getattr(u, "input_tokens", 0) or 0),
                     tokens_out=int(getattr(u, "output_tokens", 0) or 0), raw=json.dumps(out))
...
"""Audited call wrapper (ADR-003.7, ADR-004, LLM_VS_CODE row 20). The only entry point pipeline code uses.

1 attempt + 2 retries; every retry changes the request (stricter-format note in the user prompt); one llm_calls row per
attempt (prompt hash = sha256 of model+system+user+schema); a fixture miss is final. Never logs prompts, responses or error text.
"""
import logging
import os
import threading
import time

from app.db import db as DB
from app.llm import provider as P

log = logging.getLogger("zlayt.llm")
MAX_ATTEMPTS = 3
_DB_LOCK = threading.Lock()   # one sqlite3 connection is shared by the worker threads; its cursors are not safe to interleave
RETRY_DELAYS_S = (0.5, 1.5)
_CODE = __import__('re').compile(r"^([A-Z][A-Z_]{2,40})\b")

_RETRY_NOTES = (
    "",
    "\n\n[RETRY 1 of 2: your previous reply was unusable. Reply with exactly one JSON object that satisfies the schema, with no prose and no code fence.]",
    "\n\n[FINAL RETRY: reply with ONLY the raw JSON object, no markdown, no commentary, every required key present, no extra keys.]",
)


class LLMFailed(Exception):
    code = "LLM_FAILED_AFTER_RETRIES"


class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
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
    s = str(step)
    return "judge" if s.startswith("judge") or (len(s) == 2 and s[0] == "j" and s[1].isdigit()) else "generator"


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
        with _DB_LOCK:
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


def _dump(o):
    import json
    return json.dumps(o, sort_keys=True)


def make_call(conn, case_id: str, *, now=None, models: dict = None, schemas: dict = None):
    """Build the pipeline's `call(step, system, user, schema, *, item_id=None) -> (output, call_id)`.
    Model per role comes from GENERATOR_MODEL / JUDGE_MODEL (ADR-004) unless `models` overrides."""
    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}

    def call(step, system, user, schema, *, item_id=None, validate=None):
        return audited_call(conn, case_id, step, m[role_for(step)], system, user, schema, item_id=item_id, now=now, validate=validate)
    return call
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:13:33.522Z

**tool call — Bash**
````
{
 "command": "grep -rn \"load_dotenv\\|dotenv\" app tools evals tests 2>/dev/null | grep -v pycache | head; echo ---; grep -rln \"D-008\\|D-031\\|ADR-006\" spec memory docs 2>/dev/null | head -20; echo ---; grep -rn \"D-008\\|D-031\" spec memory docs 2>/dev/null | grep -v \"^Binary\" | head -20",
 "description": "Check dotenv loading and find D-008/D-031 decision text"
}
````

### User / tool · 2026-11-02T02:13:33.634Z

**tool result**
````
---
spec/REQUIREMENTS.md
memory/ORCHESTRATOR_DECISIONS.md
memory/DECISIONS.md
memory/contracts/api.md
---
spec/REQUIREMENTS.md:138:| R-CO-4 | **Runs from a link or from the repo in under 5 minutes.** The public link works without a key: public deployment is demo-only by default (D-008), replaying the cached sample run through the real pipeline code (A-002). In demo mode `POST /api/cases` accepts only text whose normalized hash equals a recorded fixture; anything else is rejected and not stored (D-020). | `tools/install_test.sh`: clean clone to first screen with the sample loaded < 300 s. The public link opens with no login. | INST + PR (installer-reviewer) |
memory/ORCHESTRATOR_DECISIONS.md:16:| D-008 | Public deployment is demo-only by default (cached sample run through real pipeline code); live mode needs an explicit env opt-in. No case list; random 128-bit case tokens; spend counter append-only and separate from case data. | Exposure + key abuse risk. NEEDS_CHRIS #7. | T-014 privacy |
memory/ORCHESTRATOR_DECISIONS.md:28:| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
memory/ORCHESTRATOR_DECISIONS.md:39:| D-031 | **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_SPLIT); 'not a duplicate' split; full audit view (local mode); exhibit/Bates numbering as a per-case config; draft treatment paragraph in firm voice (stretch from spec; every sentence grounded + judged, internal until accepted). **Still cut, with reason:** charge reclassification (a rate must never become a charge — safety), auth/roles (needs an identity provider), per-user learning (needs its own evals), numeric confidence (unverifiable precision), non-English/handwriting, date-convention inference (silent-guess risk), OCR. | Chris asked; each reinstated item keeps the ladder and grounding rules. | Chris inbox 02:05Z |
memory/DECISIONS.md:159:- Status: accepted (M1, amended rounds 2 and 3; D-008, D-020). Release owns the files; exact HF front matter is verified against current HF docs at M4.
memory/contracts/api.md:63:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
memory/contracts/api.md:65:## POST /api/cases/pdf (D-031)
memory/contracts/api.md:441:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:13:46.872Z

**tool call — Bash**
````
{
 "command": "ls evals/library 2>&1 | head; echo ---; ls evals/golden | head -30; echo ---; grep -n \"def create_case\\|token\\|secrets\\|token_hex\\|urlsafe\" app/db/db.py | head -20; echo ---; grep -rn \"api/cases\\|library\\|switch\" app/frontend/*.js app/frontend/index.html | grep -v mock | head -30",
 "description": "Check library dir, token generation, and frontend switcher references"
}
````

### User / tool · 2026-11-02T02:13:46.977Z

**tool result**
````
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
---
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
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
case_09_nonvisit_hides_gap.expected.json
case_09_nonvisit_hides_gap.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
sample.expected.json
sample.export.expected.txt
sample.txt
unsplit_paste.split.json
unsplit_paste.txt
---
12:import secrets
63:    return prefix + secrets.token_hex(6)
78:def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
79:    cid = fields.pop("id", None) or secrets.token_urlsafe(16)
---
app/frontend/index.html:51:<script src="switcher.js"></script>
app/frontend/switcher.js:1:/* Case switcher (T-053 AC2, local mode only). Shown only when GET /api/cases answers 200 (404 in demo/public mode).
app/frontend/switcher.js:2:   Lists cases (open with one click) and the synthetic library (POST /cases {library:id}, then run). Text via ZL.el only. */
app/frontend/switcher.js:27:    const resp = await ZL.api.createCase({ library: id });
app/frontend/switcher.js:33:  function draw(cases, library) {
app/frontend/switcher.js:42:    const lib = el("ul", { class: "cs-list", "data-testid": "library-list" });
app/frontend/switcher.js:43:    library.forEach((l) => lib.append(el("li", {}, el("button", { type: "button", class: "rv-btn cs-btn", "data-testid": "library-" + l.id, onclick: () => loadLibrary(l.id) },
app/frontend/switcher.js:45:    if (!library.length) lib.append(el("li", { class: "rv-empty" }, "The library is empty."));
app/frontend/switcher.js:48:    root.append(el("h2", { id: "cs-h", class: "cs-h" }, "Cases (local mode)"), list, el("h3", { class: "cs-h" }, "Synthetic library: one click loads and runs a case"), lib, msg || el("p", { class: "cs-msg rv-error", role: "status" }));
app/frontend/switcher.js:51:    const [a, b] = await Promise.all([get("/cases"), get("/library")]);
app/frontend/switcher.js:54:      root = el("section", { id: "case-switcher", class: "card cs", "data-testid": "case-switcher", "aria-labelledby": "cs-h" }, el("p", { class: "cs-msg rv-error", role: "status" }));
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:13:49.920Z

**tool call — Bash**
````
{
 "command": "git status --short | head -40; echo ---; git log --oneline -n 3 -- evals/library | cat; echo ---; cat app/frontend/switcher.js",
 "description": "Check working tree status and read the UI switcher file"
}
````

### User / tool · 2026-11-02T02:13:50.056Z

**tool result**
````
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
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_hook_guard_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M app/frontend/index.html
 M app/frontend/review.css
 M board/activity.jsonl
 M board/cards/T-036.md
 M board/cards/T-037.md
 M board/cards/T-038.md
 M board/cards/T-040.md
 M board/cards/T-045.md
 M board/cards/T-050.md
 M board/cards/T-051.md
 M board/cards/T-052.md
 M board/cards/T-053.md
 M board/cards/T-054.md
 M board/cards/T-056.md
 M board/cards/T-057.md
 M evals/reports/latest.json
 M memory/ORCHESTRATOR_DECISIONS.md
 M memory/SCOPE_CUTS.md
 M tests/fixtures/llm/06bbeeec2801064baeb024b1338ce8a0263644a7a2dca09efdaeed154ed50299.json
 M tests/fixtures/llm/07aab6f4f7a87ed2477b3cb9ebdb02449815ddf270c7f8aafdfa3c2338c9be19.json
 M tests/fixtures/llm/0cee28a9faf640b117982bccb05b874c1bc8b7359cd3ff5dc846f1ac8db9c8c9.json
 M tests/fixtures/llm/0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
---
a010dd4 feat(research): synthetic case library, 7 packets with sources and validator (T-052)
---
/* Case switcher (T-053 AC2, local mode only). Shown only when GET /api/cases answers 200 (404 in demo/public mode).
   Lists cases (open with one click) and the synthetic library (POST /cases {library:id}, then run). Text via ZL.el only. */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let root = null, lastToken = undefined, busy = false;

  async function get(path) {
    if (ZL.API_MODE === "mock") return ZL.mock.handle("GET", path);
    const res = await fetch("/api" + path); let body = null;
    try { body = await res.json(); } catch (_) { /* no body */ }
    return { status: res.status, body };
  }
  function say(msg, isError) { const p = root && root.querySelector(".cs-msg"); if (p) { p.textContent = msg || ""; p.setAttribute("role", isError ? "alert" : "status"); } }

  async function openCase(token) {
    const c = await ZL.api.getCase(token);
    history.replaceState(null, "", "#/case/" + encodeURIComponent(token));
    ZL.state.set({ token, created: c.status === "ingested" ? Object.assign({}, c, { record_count: (c.records || []).length }) : null, case: c, status: null });
    if (c.status === "running") ZL.pollRun();
  }
  async function guarded(fn) {
    if (busy) return; busy = true; say("");
    try { await fn(); } catch (e) { say((e && e.message) || "That did not work.", true); } finally { busy = false; }
  }
  const open = (token) => guarded(() => openCase(token));
  const loadLibrary = (id) => guarded(async () => {
    const resp = await ZL.api.createCase({ library: id });
    await openCase(resp.token);
    ZL.state.set({ status: { status: "running", progress: { label: "Starting…" } } });
    await ZL.api.run(resp.token, false); ZL.pollRun();
  });

  function draw(cases, library) {
    const cur = ZL.state.get().token;
    const list = el("ul", { class: "cs-list", "data-testid": "case-list" });
    if (!cases.length) list.append(el("li", { class: "rv-empty" }, "No cases yet."));
    cases.forEach((c) => {
      const k = c.counts || {};
      list.append(el("li", {}, el("button", { type: "button", class: "rv-btn rv-secondary cs-btn", "data-testid": "case-" + c.token, "aria-current": c.token === cur ? "true" : null, onclick: () => open(c.token) },
        (c.token === cur ? "Open now: " : "Open: ") + c.name, el("span", { class: "cs-meta" }, `${c.status} · ${c.record_count} records` + (k.pending != null ? ` · ${k.pending} pending` : "")))));
    });
    const lib = el("ul", { class: "cs-list", "data-testid": "library-list" });
    library.forEach((l) => lib.append(el("li", {}, el("button", { type: "button", class: "rv-btn cs-btn", "data-testid": "library-" + l.id, onclick: () => loadLibrary(l.id) },
      "Load: " + l.name, l.description ? el("span", { class: "cs-meta" }, l.description) : null))));
    if (!library.length) lib.append(el("li", { class: "rv-empty" }, "The library is empty."));
    const msg = root.querySelector(".cs-msg");
    clear(root);
    root.append(el("h2", { id: "cs-h", class: "cs-h" }, "Cases (local mode)"), list, el("h3", { class: "cs-h" }, "Synthetic library: one click loads and runs a case"), lib, msg || el("p", { class: "cs-msg rv-error", role: "status" }));
  }
  async function refresh() {
    const [a, b] = await Promise.all([get("/cases"), get("/library")]);
    if (a.status !== 200) { if (root) root.hidden = true; return; }
    if (!root) {
      root = el("section", { id: "case-switcher", class: "card cs", "data-testid": "case-switcher", "aria-labelledby": "cs-h" }, el("p", { class: "cs-msg rv-error", role: "status" }));
      const main = document.querySelector("main"); main.parentNode.insertBefore(root, main);
    }
    root.hidden = false;
    draw((a.body && a.body.cases) || [], (b.status === 200 && b.body && b.body.cases) || []);
  }
  document.addEventListener("DOMContentLoaded", () => {
    refresh().catch(() => {});
    ZL.state.subscribe((s) => { if (s.token !== lastToken) { lastToken = s.token; if (root) refresh().catch(() => {}); } });
  });
})();
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:13:54.556Z

**tool call — Bash**
````
{
 "command": "git diff -- app/frontend/index.html | head -40; echo ---; cat app/frontend/dom.js | head -60; echo ---; grep -n \"innerHTML\\|insertAdjacentHTML\\|outerHTML\\|document.write\\|eval(\\|new Function\" app/frontend/*.js | grep -v \"dev/\\|mock\" | head",
 "description": "Inspect uncommitted index.html diff, DOM helper, and unsafe sink grep"
}
````

### User / tool · 2026-11-02T02:13:54.669Z

**tool result**
````
diff --git a/app/frontend/index.html b/app/frontend/index.html
index e4430f1..aec51f2 100644
--- a/app/frontend/index.html
+++ b/app/frontend/index.html
@@ -48,6 +48,7 @@
 <script src="review.js"></script>
 <script src="flags.js"></script>
 <script src="charges.js"></script>
+<script src="switcher.js"></script>
 <script src="app.js"></script>
 </body>
 </html>
---
/* Shared DOM helpers (frontend-1 / T-042; also used by T-043). Data is only ever written with textContent / text nodes. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  // el("button", {class:"x", type:"button", onclick:fn, "data-testid":"y"}, "label", childNode, ...)
  ZL.el = function (tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === false || v == null) continue;
      if (k === "class") e.className = v;
      else if (k === "text") e.textContent = v;
      else if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v === true ? "" : String(v));
    }
    for (const c of kids.flat()) {
      if (c == null || c === false) continue;
      e.append(c.nodeType ? c : document.createTextNode(String(c)));
    }
    return e;
  };
  ZL.clear = (n) => { while (n.firstChild) n.removeChild(n.firstChild); return n; };
  ZL.$ = (s, r) => (r || document).querySelector(s);
  ZL.fmtDate = (iso) => {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
    if (!m) return iso || "undated";
    const mon = ["January","February","March","April","May","June","July","August","September","October","November","December"][+m[2] - 1];
    return `${mon} ${+m[3]}, ${m[1]}`;
  };
  ZL.money = (cents) => "$" + (cents / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
})();
---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:13:57.995Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider \"tests/unit/test_api_routes.py::test_case_list_and_library_exist_only_in_local_mode\" \"tests/unit/test_api_routes.py::test_cases_do_not_leak_decisions_between_each_other\" -v 2>&1 | tail -25",
 "description": "Run the two named T-053 pytest cases",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:13:59.491Z

**tool result**
````
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/arsis/zlayt-pm-project/.venv/bin/python
rootdir: /Users/arsis/zlayt-pm-project
plugins: anyio-4.16.0
collecting ... collected 2 items

tests/unit/test_api_routes.py::test_case_list_and_library_exist_only_in_local_mode PASSED [ 50%]
tests/unit/test_api_routes.py::test_cases_do_not_leak_decisions_between_each_other PASSED [100%]

============================== 2 passed in 1.11s ===============================
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:00.951Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py tests/e2e/test_api.py -q 2>&1 | tail -15; echo \"exit=$?\"",
 "description": "Run full API route and API e2e test files",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:14:08.215Z

**tool result**
````
...............................                                          [100%]
31 passed in 6.87s
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:13.241Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/local\" \"$S/demo\"; for p in 7871 7872; do (lsof -iTCP:$p -sTCP:LISTEN >/dev/null 2>&1 && echo \"$p busy\") || echo \"$p free\"; done; echo \"$S\"",
 "description": "Check candidate ports and prepare scratchpad dirs"
}
````

### User / tool · 2026-11-02T02:14:13.485Z

**tool result**
````
7871 busy
7872 free
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:14.645Z

**tool call — Bash**
````
{
 "command": "for p in 7873 7874 7875 7876; do (lsof -iTCP:$p -sTCP:LISTEN >/dev/null 2>&1 && echo \"$p busy\") || echo \"$p free\"; done",
 "description": "Find two free candidate ports"
}
````

### User / tool · 2026-11-02T02:14:15.026Z

**tool result**
````
7873 free
7874 free
7875 free
7876 free
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:18.282Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md"
}
````

### User / tool · 2026-11-02T02:14:18.295Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:18.491Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/project_hook_guard_review_patterns.md"
}
````

### User / tool · 2026-11-02T02:14:18.502Z

**tool result**
````
1	---
2	name: hook-guard-review-patterns
3	description: Recurring weak spots found reviewing the Zlayt PM git-guard/board-guard/check_secrets hooks (T-003/T-006 rounds 1-3); where to probe first next time
4	metadata:
5	  type: project
6	---
7	
8	Guards are string-analysis hooks (git_guard.py, board_guard.py, reviewer_write_guard.py, tools/check_secrets.py); the codebase is a moving target during review (worker edits the working tree live), so stamp md5/sha of the files you tested and re-run after any "changed on disk" notice. Threat model is D-023 (memory/ORCHESTRATOR_DECISIONS.md): accidents and lazy evasion are bugs; deliberate obfuscation (IFS, brace expansion, board.py copies, interpreter one-liners) is residual.
9	
10	Round 3 state (e3fbb08): r2 blockers (newline separators, `:+` refspec) fixed; remaining class of gaps = (1) git add of computed/glob sets (`./*`, `.*`, `$(git diff --name-only)`, `| xargs git add`), (2) reviewer redirect detection is token-based: `cmd>file` no-space, `>&`, `>|` pass, (3) global WRAPPER_OPTS_WITH_ARG swallows git after `sudo -n/-E`, `command -p`, `time -p`, (4) .claude/settings.json + tools/check_secrets.py removable, (5) history-moving ops (`checkout -B`, `reset origin/main`, `fetch -f`) allowed, (6) false positives: `find . -name x -delete`, `git reset HEAD file`, `git config --get core.hooksPath`, read-only reviewer git (branch/tag/stash list), quoted commit/note text containing bash/xargs plus a denied command, BSD `sed -i ''`. check_secrets: `git commit <path>` unseen by git-guard scan (native hook catches), hook install not drift-checked, placeholder FPs have no noqa, NUL-in-8000 skip.
11	
12	Reviewer-workflow gotchas (the live board-guard/git-guard apply to the reviewer): `cd <scratch> && cat > f` is denied (redirect checked pre-cd); `$VAR` redirect targets denied; `git config --get core.hooksPath` is denied by git-guard (config rule matches the key even for --get); backticks inside double quotes in a probe command really get analysed as commands; scratch-repo git via Bash is denied, so write probe scripts to artifacts/review-evidence/ with the Write tool and run them with python (subprocess git in /private/tmp scratch repos). Run probe scripts from the project ROOT: expand_vars() seeds $PWD from the hook process cwd, so results differ when launched from another dir.
13	
14	**How to apply:** start any re-review of these hooks by replaying artifacts/review-evidence/T-003-r3-probe-corpus.py (538-line r2 corpus; r3 = 345 DENY / 193 ALLOW), T-003-r3-probe-targeted.py, -targeted2.py, -legit.py (61 legit commands, must all allow), -rwg.py, T-003-r2-probe-direct.py / -board2.py, and T-006-r2-probe.py / -chain-probe.py / -fp-probe.py / T-006-r3-commit-paths-probe.py; diff against the r3 .out.txt files.
15	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:23.038Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; env -u ZLAYT_MODE -u ANTHROPIC_API_KEY -u LLM_BACKEND -u ENABLE_LIVE PYTHONDONTWRITEBYTECODE=1 DATA_DIR=\"$S/demo\" PORT=7873 HOST=127.0.0.1 .venv/bin/python -m app.main > \"$S/demo.log\" 2>&1 &\necho \"demo pid $!\"; cd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; env -u ANTHROPIC_API_KEY -u LLM_BACKEND -u ENABLE_LIVE ZLAYT_MODE=local PYTHONDONTWRITEBYTECODE=1 DATA_DIR=\"$S/local\" PORT=7874 HOST=127.0.0.1 .venv/bin/python -m app.main > \"$S/local.log\" 2>&1 &\necho \"local pid $!\"; sleep 4; curl -s -o /dev/null -w \"demo health %{http_code}\\n\" http://127.0.0.1:7873/api/health; curl -s -o /dev/null -w \"local health %{http_code}\\n\" http://127.0.0.1:7874/api/health",
 "description": "Start demo (no ZLAYT_MODE) and local servers on free ports",
 "timeout": 60000
}
````

### User / tool · 2026-11-02T02:14:27.200Z

**tool result**
````
demo pid 52647
local pid 52648
demo health 200
local health 200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:29.209Z

**tool call — Bash**
````
{
 "command": "cd /tmp 2>/dev/null; for port in 7873 7874; do echo \"== port $port\"; for path in /api/cases /api/library; do curl -s -i \"http://127.0.0.1:$port$path\" | sed -n '1p;/^content-type/Ip' ; curl -s \"http://127.0.0.1:$port$path\" | head -c 300; echo; done; done",
 "description": "Curl list and library routes on both servers",
 "timeout": 60000
}
````

### User / tool · 2026-11-02T02:14:29.372Z

**tool result**
````
== port 7873
HTTP/1.1 404 Not Found
content-type: application/json
{"error":{"code":"not_found","message":"Not found.","detail":{}}}
HTTP/1.1 404 Not Found
content-type: application/json
{"error":{"code":"not_found","message":"Not found.","detail":{}}}
== port 7874
HTTP/1.1 200 OK
content-type: application/json
{"cases":[]}
HTTP/1.1 200 OK
content-type: application/json
{"cases":[{"id":"case_lib01_er_only_then_gap","name":"case lib01 er only then gap","description":"Library L1 (mirrors S1). Rear-end collision, ED visit and a negative x-ray, then the first primary-care visit 44 days later with a new arm symptom and a patient-stated reason for the delay. The gap is f
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:32.333Z

**tool call — Bash**
````
{
 "command": "grep -n '@app\\.\\(get\\|post\\|put\\|patch\\|delete\\)' app/backend/api.py; grep -n \"def review\\b\\|def review_item\\|items/{\" app/backend/api.py | head",
 "description": "List all API routes defined in api.py"
}
````

### User / tool · 2026-11-02T02:14:32.424Z

**tool result**
````
189:    @app.get("/api/health")
195:    @app.get("/api/cases")
205:    @app.get("/api/library")
211:    @app.post("/api/cases", status_code=201)
227:    @app.post("/api/cases/pdf", status_code=201)
279:    @app.get("/api/cases/{token}")
288:    @app.delete("/api/cases/{token}", status_code=204)
312:    @app.post("/api/cases/{token}/run", status_code=202)
335:    @app.get("/api/cases/{token}/status")
354:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
366:    @app.get("/api/cases/{token}/items/{item_id}")
378:    @app.post("/api/cases/{token}/items/{item_id}/review")
388:    @app.get("/api/cases/{token}/export")
412:    @app.get("/api/cases/{token}/audit")
366:    @app.get("/api/cases/{token}/items/{item_id}")
378:    @app.post("/api/cases/{token}/items/{item_id}/review")
379:    async def review_item(token: str, item_id: str, request: Request):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:33.740Z

**tool call — Bash**
````
{
 "command": "sed -n 354,388p app/backend/api.py; echo ...; grep -n \"def get_item\\|def set_review\\|def review_item\\|def apply_review\\|WHERE id\\|case_id=?\" app/backend/review.py app/db/db.py | head -30",
 "description": "Read item review/get handlers and DB item scoping"
}
````

### User / tool · 2026-11-02T02:14:33.831Z

**tool result**
````
    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
    async def confirm_date(token: str, rid: str, request: Request):
        b = await body_of(request)
        if not isinstance(b.get("date"), str):
            raise ApiError(400, "bad_request", "Provide the chosen date.")
        c = conn()
        try:
            get_case(c, token)
            return review.confirm_date(c, token, rid, b["date"])
        finally:
            c.close()

    @app.get("/api/cases/{token}/items/{item_id}")
    def item(token: str, item_id: str):
        c = conn()
        try:
            get_case(c, token)
            try:
                return present.why_view(c, token, item_id)
            except (KeyError, IndexError):
                raise ApiError(404, "not_found", "No such item.") from None
        finally:
            c.close()

    @app.post("/api/cases/{token}/items/{item_id}/review")
    async def review_item(token: str, item_id: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
        finally:
            c.close()

    @app.get("/api/cases/{token}/export")
...
app/backend/review.py:41:def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
app/backend/review.py:142:    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
app/backend/review.py:150:    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
app/backend/review.py:168:    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
app/backend/review.py:198:            conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (old["id"], case_id))
app/backend/review.py:205:    have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
app/db/db.py:92:    conn.execute(f"UPDATE cases SET {sets} WHERE id=?", [_enc(v) for v in fields.values()] + [case_id])
app/db/db.py:96:    r = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
app/db/db.py:133:    q, a = f"SELECT * FROM {table} WHERE id=?", [item_id]
app/db/db.py:135:        q, a = q + " AND case_id=?", a + [case]
app/db/db.py:155:def get_item(conn, item_id: str, case: str = None) -> dict:
app/db/db.py:161:    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]
app/db/db.py:176:    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])
app/db/db.py:179:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
app/db/db.py:193:        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
app/db/db.py:204:def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
app/db/db.py:212:    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
app/db/db.py:228:    r = conn.execute("SELECT * FROM llm_calls WHERE id=?", (call_id,)).fetchone()
app/db/db.py:233:    q, a = "SELECT * FROM llm_calls WHERE case_id=?", [case_id]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:41.803Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json, time, urllib.request, urllib.error\nB = \"http://127.0.0.1:7874\"\ndef req(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(B + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(r, timeout=60) as resp:\n            raw = resp.read(); return resp.status, (json.loads(raw) if raw else None)\n    except urllib.error.HTTPError as e:\n        raw = e.read(); return e.code, (json.loads(raw) if raw else None)\nlib = req(\"GET\", \"/api/library\")[1][\"cases\"]\nprint(\"library ids:\", [x[\"id\"] for x in lib])\ns, a = req(\"POST\", \"/api/cases\", {\"sample\": True}); print(\"A sample create\", s, a[\"token\"][:8], a[\"status\"], a.get(\"demo_mode\"))\ns, r = req(\"POST\", \"/api/cases/%s/run\" % a[\"token\"], {}); print(\"A run\", s, r and r.get(\"status\"))\nfor _ in range(120):\n    st = req(\"GET\", \"/api/cases/%s/status\" % a[\"token\"])[1]\n    if st[\"status\"] in (\"ready\", \"failed\"): break\n    time.sleep(0.5)\nprint(\"A final\", st[\"status\"], st.get(\"error\"))\ns, b = req(\"POST\", \"/api/cases\", {\"library\": lib[0][\"id\"]}); print(\"B library create\", s, b.get(\"token\", \"\")[:8], b.get(\"status\"), b.get(\"name\"))\ns, r = req(\"POST\", \"/api/cases/%s/run\" % b[\"token\"], {}); print(\"B run\", s, r and r.get(\"status\"))\nfor _ in range(120):\n    stb = req(\"GET\", \"/api/cases/%s/status\" % b[\"token\"])[1]\n    if stb[\"status\"] in (\"ready\", \"failed\"): break\n    time.sleep(0.5)\nprint(\"B final\", stb[\"status\"], stb.get(\"error\"))\njson.dump({\"a\": a[\"token\"], \"b\": b[\"token\"]}, open(\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/tokens.json\", \"w\"))\nEOF",
 "description": "Create sample and library cases on local server and run both",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:14:43.216Z

**tool result**
````
library ids: ['case_lib01_er_only_then_gap', 'case_lib02_slip_fall_prior_knee', 'case_lib03_truck_rear_end_chiro', 'case_lib04_dog_bite_scar_revision', 'case_lib05_pedestrian_orif_hardware', 'case_lib06_lop_billed_vs_adjusted', 'case_lib07_parking_lot_fall_outside_records']
A sample create 201 jPZb3eOt ingested True
A run 202 running
A final ready None
B library create 201 OzuNMyqF ingested case lib01 er only then gap
B run 202 running
B final ready None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:48.582Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json, urllib.request, urllib.error\nB = \"http://127.0.0.1:7874\"\nT = json.load(open(\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/tokens.json\"))\na, b = T[\"a\"], T[\"b\"]\ndef req(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(B + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(r, timeout=60) as resp:\n            raw = resp.read(); return resp.status, (json.loads(raw) if raw else None)\n    except urllib.error.HTTPError as e:\n        raw = e.read(); return e.code, (json.loads(raw) if raw else None)\nea = req(\"GET\", f\"/api/cases/{a}\")[1]\nprint(\"A keys\", sorted(ea.keys())[:12])\nentries = ea.get(\"entries\") or []\nprint(\"A entries\", len(entries), \"first id\", entries[0][\"id\"] if entries else None)\nia = entries[0][\"id\"]\nprint(\"accept A item via A:\", req(\"POST\", f\"/api/cases/{a}/items/{ia}/review\", {\"action\": \"accept\"})[0])\nprint(\"cross: accept A item via B token:\", req(\"POST\", f\"/api/cases/{b}/items/{ia}/review\", {\"action\": \"accept\"}))\nprint(\"cross: GET A item via B token:\", req(\"GET\", f\"/api/cases/{b}/items/{ia}\")[0])\nlst = req(\"GET\", \"/api/cases\")[1][\"cases\"]\nfor c in lst:\n    print(\"list\", c[\"token\"][:8], c[\"name\"], c[\"status\"], c[\"record_count\"], c[\"counts\"], sorted(c.keys()))\nca = req(\"GET\", f\"/api/cases/{a}\")[1]; cb = req(\"GET\", f\"/api/cases/{b}\")[1]\nprint(\"A accepted entries:\", sum(1 for e in ca[\"entries\"] if e[\"review_status\"]==\"accepted\"), \" B accepted entries:\", sum(1 for e in cb[\"entries\"] if e[\"review_status\"]==\"accepted\"))\nprint(\"B decision via B list counts check, entries B:\", len(cb[\"entries\"]))\nEOF",
 "description": "Probe cross-case isolation of decisions via HTTP on local server",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:14:48.761Z

**tool result**
````
A keys ['amounts', 'backend', 'created_at', 'dates_to_confirm', 'demo_mode', 'entries', 'error', 'flags', 'injection', 'models', 'name', 'records']
A entries 9 first id e1
accept A item via A: 200
cross: accept A item via B token: (404, {'error': {'code': 'not_found', 'message': 'No such item.', 'detail': {}}})
cross: GET A item via B token: 404
list OzuNMyqF case lib01 er only then gap ready 6 {'pending': 4, 'accepted': 0, 'edited': 0, 'dismissed': 0, 'needs_review': 3} ['counts', 'created_at', 'name', 'record_count', 'source', 'status', 'token']
list jPZb3eOt Sample case ready 9 {'pending': 22, 'accepted': 1, 'edited': 0, 'dismissed': 0, 'needs_review': 7} ['counts', 'created_at', 'name', 'record_count', 'source', 'status', 'token']
A accepted entries: 1  B accepted entries: 0
B decision via B list counts check, entries B: 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:00.094Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; env -u ZLAYT_MODE LLM_BACKEND=anthropic-api ANTHROPIC_API_KEY=<redacted> ANTHROPIC_BASE_URL=http://127.0.0.1:9 PYTHONDONTWRITEBYTECODE=1 DATA_DIR=\"$S/live-demo\" PORT=7876 HOST=127.0.0.1 .venv/bin/python -m app.main > \"$S/live-demo.log\" 2>&1 &\nenv ZLAYT_MODE=local LLM_BACKEND=anthropic-api ANTHROPIC_API_KEY=<redacted> ANTHROPIC_BASE_URL=http://127.0.0.1:9 PYTHONDONTWRITEBYTECODE=1 DATA_DIR=\"$S/live-local\" PORT=7875 HOST=127.0.0.1 .venv/bin/python -m app.main > \"$S/live-local.log\" 2>&1 &\nsleep 4; curl -s http://127.0.0.1:7875/api/health | head -c 400; echo; curl -s http://127.0.0.1:7876/api/health | head -c 400; echo",
 "description": "Start two probe servers with anthropic-api backend and fake key, no ENABLE_LIVE",
 "timeout": 60000
}
````

### User / tool · 2026-11-02T02:15:04.244Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"anthropic-api","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"anthropic-api","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:07.651Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json, time, urllib.request, urllib.error\ndef mk(base):\n    def req(method, path, body=None):\n        data = json.dumps(body).encode() if body is not None else None\n        r = urllib.request.Request(base + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n        try:\n            with urllib.request.urlopen(r, timeout=120) as resp:\n                raw = resp.read(); return resp.status, (json.loads(raw) if raw else None)\n        except urllib.error.HTTPError as e:\n            raw = e.read(); return e.code, (json.loads(raw) if raw else None)\n    return req\ndef go(base, body, label):\n    req = mk(base)\n    s, c = req(\"POST\", \"/api/cases\", body); print(label, \"create\", s, c.get(\"status\") if c else None)\n    if s != 201: return\n    s, r = req(\"POST\", \"/api/cases/%s/run\" % c[\"token\"], {}); print(label, \"run\", s)\n    for _ in range(120):\n        st = req(\"GET\", \"/api/cases/%s/status\" % c[\"token\"])[1]\n        if st[\"status\"] in (\"ready\", \"failed\"): break\n        time.sleep(0.5)\n    print(label, \"final status\", st[\"status\"], \"error\", st.get(\"error\"))\n    au = req(\"GET\", \"/api/cases/%s/audit\" % c[\"token\"])[1]\n    calls = au.get(\"calls\", [])\n    print(label, \"llm_calls\", len(calls), \"backends\", sorted({x.get(\"backend\") for x in calls}), \"errors\", sorted({str(x.get(\"error\")) for x in calls})[:5])\ngo(\"http://127.0.0.1:7876\", {\"sample\": True}, \"DEMO(no ZLAYT_MODE) sample\")\ngo(\"http://127.0.0.1:7875\", {\"library\": \"case_lib01_er_only_then_gap\"}, \"LOCAL library lib01\")\nEOF",
 "description": "Run sample and library cases under anthropic-api backend with no ENABLE_LIVE",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T02:15:09.616Z

**tool result**
````
DEMO(no ZLAYT_MODE) sample create 201 ingested
DEMO(no ZLAYT_MODE) sample run 202
DEMO(no ZLAYT_MODE) sample final status ready error None
DEMO(no ZLAYT_MODE) sample llm_calls 66 backends ['anthropic-api'] errors ['None']
LOCAL library lib01 create 201 ingested
LOCAL library lib01 run 202
LOCAL library lib01 final status ready error None
LOCAL library lib01 llm_calls 45 backends ['anthropic-api'] errors ['BACKEND_FAILED']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:15.334Z

**tool call — Bash**
````
{
 "command": "grep -rn \"replay\\|demo\" app/backend/pipeline.py app/backend/api.py app/llm/*.py app/llm/backends/fixture.py | grep -v \"demo_mode=int\\|\\\"demo_mode\\\"\" | head -30; echo ---; sed -n 1,40p app/llm/backends/fixture.py",
 "description": "Find how demo mode replays cached LLM outputs"
}
````

### User / tool · 2026-11-02T02:15:15.453Z

**tool result**
````
app/llm/record.py:50:    Calls pipeline.judge_summary exactly as the eval runner does, so replay keys match. Returns the number of lines replayed."""
app/llm/record.py:84:        print(f"judge lines replayed: {record_judges()}")
app/backend/api.py:1:"""FastAPI routes (memory/contracts/api.md). Thin: parsing, the demo gate, error format; logic lives in ingest/store/review/present/export.
app/backend/api.py:99:    def demo_mode():
app/backend/api.py:197:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
app/backend/api.py:250:        if demo_mode() and digest(text) not in allowed_hashes():
app/backend/api.py:251:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:284:            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
app/backend/api.py:320:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
app/backend/api.py:321:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:322:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/llm/backends/fixture.py:1:"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
---
"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
import json
import os
import pathlib
import time

from app.llm._types import FixtureMiss, LLMError, LLMResult

DEFAULT_DIR = pathlib.Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "llm"


def fixture_dir() -> pathlib.Path:
    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
    if os.environ.get("LLM_FIXTURE_DIR"):
        return pathlib.Path(os.environ["LLM_FIXTURE_DIR"])
    name = os.environ.get("FIXTURE_SET", "").strip()
    return DEFAULT_DIR / name if name and name.isidentifier() else DEFAULT_DIR


def call(model: str, system: str, user: str, json_schema: dict, *, key: str) -> LLMResult:
    p = fixture_dir() / f"{key}.json"
    t0 = time.monotonic()
    if not p.is_file():
        raise FixtureMiss(key)
    try:
        d = json.loads(p.read_text())
        out = d["output"]
    except (ValueError, KeyError, OSError):
        raise LLMError(f"FIXTURE_CORRUPT {key}") from None
    return LLMResult(output=out, backend="fixture", model_resolved=model, latency_ms=int((time.monotonic() - t0) * 1000),
                     raw=json.dumps(out), recorded_from=d.get("recorded_from") or {})


def write(key: str, result: LLMResult, model: str) -> pathlib.Path:
    """Record mode: store a live result keyed by the prompt hash, with provenance."""
    d = fixture_dir()
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{key}.json"
    rec = {"output": result.output,
           "recorded_from": {"backend": result.backend, "model": result.model_resolved or model,
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:22.475Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I - \"$S\" <<'EOF'\nimport sqlite3, sys, os\nS = sys.argv[1]\nfor d in (\"live-demo\", \"live-local\"):\n    p = os.path.join(S, d, \"zlayt.sqlite\")\n    c = sqlite3.connect(p); c.row_factory = sqlite3.Row\n    print(\"==\", d)\n    rows = c.execute(\"SELECT backend, error, count(*) n, min(latency_ms) lat_min, max(latency_ms) lat_max, sum(cost_usd IS NOT NULL) costed FROM llm_calls GROUP BY backend, error\").fetchall()\n    for r in rows: print(dict(r))\n    print(\"cases:\", [dict(x) for x in c.execute(\"SELECT source, demo_mode, backend, status FROM cases\")])\nEOF\necho; grep -c . \"$S/live-demo.log\" \"$S/live-local.log\"; ls \"$S/live-demo\" \"$S/live-local\" 2>&1 | head",
 "description": "Inspect llm_calls rows in probe databases"
}
````

### User / tool · 2026-11-02T02:15:22.604Z

**tool result**
````
== live-demo
{'backend': 'anthropic-api', 'error': 'BACKEND_FAILED', 'n': 66, 'lat_min': 0, 'lat_max': 476, 'costed': 0}
cases: [{'source': 'sample', 'demo_mode': 1, 'backend': 'anthropic-api', 'status': 'ready'}]
== live-local
{'backend': 'anthropic-api', 'error': 'BACKEND_FAILED', 'n': 45, 'lat_min': 0, 'lat_max': 458, 'costed': 0}
cases: [{'source': 'paste', 'demo_mode': 1, 'backend': 'anthropic-api', 'status': 'ready'}]

/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/live-demo.log:66
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/live-local.log:45
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/live-demo:
zlayt.sqlite

/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/live-local:
zlayt.sqlite
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:42.683Z

**tool call — Bash**
````
{
 "command": "env -u ZLAYT_MODE ANTHROPIC_BASE_URL=http://127.0.0.1:7877 LLM_BACKEND=anthropic-api ANTHROPIC_API_KEY=<redacted> ENABLE_LIVE= PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I - <<'EOF'\nimport socket, threading, os, sys\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nhits = []\nsrv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); srv.bind((\"127.0.0.1\", 7877)); srv.listen(5); srv.settimeout(20)\ndef serve():\n    try:\n        while True:\n            c, _ = srv.accept(); hits.append(c.recv(65536)[:200]); c.sendall(b\"HTTP/1.1 401 Unauthorized\\r\\nContent-Type: application/json\\r\\nContent-Length: 2\\r\\nConnection: close\\r\\n\\r\\n{}\"); c.close()\n    except Exception: pass\nt = threading.Thread(target=serve, daemon=True); t.start()\nfrom app.llm import provider as P\nschema = {\"type\": \"object\", \"properties\": {\"x\": {\"type\": \"string\"}}, \"required\": [\"x\"], \"additionalProperties\": False}\nprint(\"ENABLE_LIVE env =\", repr(os.environ.get(\"ENABLE_LIVE\")), \"backend =\", P.backend_name())\ntry:\n    P.complete_with_meta(\"claude-sonnet-5-5\", \"sys\", \"synthetic user text\", schema)\n    print(\"returned\")\nexcept Exception as e:\n    print(\"raised\", type(e).__name__, str(e)[:80])\nprint(\"listener connections received:\", len(hits), \"first request line:\", (hits[0].split(b\"\\r\\n\")[0] if hits else None))\nEOF",
 "description": "Prove provider issues HTTP request with ENABLE_LIVE unset via local listener",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T02:15:43.518Z

**tool result**
````
ENABLE_LIVE env = '' backend = anthropic-api
raised LLMError BACKEND_FAILED anthropic-api TypeError
listener connections received: 0 first request line: None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:47.788Z

**tool call — Bash**
````
{
 "command": "env -u ZLAYT_MODE ANTHROPIC_BASE_URL=http://127.0.0.1:7877 ANTHROPIC_API_KEY=<redacted> PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I - <<'EOF'\nimport sys, traceback\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nimport anthropic\nprint(\"anthropic sdk\", anthropic.__version__)\nfrom app.llm.backends import anthropic_api as be\nschema = {\"type\": \"object\", \"properties\": {\"x\": {\"type\": \"string\"}}, \"required\": [\"x\"], \"additionalProperties\": False}\ncl = anthropic.Anthropic(api_key=\"sk-probe-not-a-real-key\", base_url=\"http://127.0.0.1:7877\", max_retries=0, timeout=5)\ntry:\n    cl.messages.create(model=\"claude-sonnet-5-5\", max_tokens=16, temperature=0, system=\"s\", messages=[{\"role\": \"user\", \"content\": \"u\"}],\n        tools=[{\"name\": \"emit\", \"description\": \"d\", \"input_schema\": schema}], tool_choice={\"type\": \"tool\", \"name\": \"emit\"})\nexcept Exception as e:\n    print(\"direct SDK exception:\", type(e).__name__, str(e)[:200])\n    traceback.print_exc(limit=-3)\nEOF",
 "description": "Call Anthropic SDK directly to see the underlying exception",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T02:15:48.639Z

**tool result**
````
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/anthropic/_utils/_utils.py", line 294, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
TypeError: Messages.create() got an unexpected keyword argument 'temperature'
anthropic sdk 2.3.0
direct SDK exception: TypeError Messages.create() got an unexpected keyword argument 'temperature'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:55.255Z

**tool call — Bash**
````
{
 "command": "env -u ZLAYT_MODE -u ENABLE_LIVE LLM_BACKEND=anthropic-api ANTHROPIC_API_KEY=<redacted> PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I - <<'EOF'\nimport sys, types\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nfrom app.llm.backends import anthropic_api as be\nfrom app.llm import provider as P\ncalls = []\nclass Msgs:\n    def create(self, **kw):\n        calls.append(kw[\"model\"])\n        blk = types.SimpleNamespace(type=\"tool_use\", input={\"x\": \"ok\"})\n        return types.SimpleNamespace(content=[blk], model=kw[\"model\"], usage=types.SimpleNamespace(input_tokens=1, output_tokens=1))\nclass Fake:\n    messages = Msgs()\nbe.make_client = lambda: Fake()          # no network: records what the SDK would be asked to do\nschema = {\"type\": \"object\", \"properties\": {\"x\": {\"type\": \"string\"}}, \"required\": [\"x\"], \"additionalProperties\": False}\nimport os\nprint(\"ENABLE_LIVE unset:\", \"ENABLE_LIVE\" not in os.environ, \"| backend:\", P.backend_name())\nout = P.complete(\"claude-sonnet-5-5\", \"sys\", \"synthetic\", schema)\nprint(\"provider returned:\", out, \"| SDK messages.create invocations:\", len(calls), calls)\nEOF",
 "description": "Show provider calls SDK messages.create with ENABLE_LIVE unset, using a stub client",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T02:15:55.382Z

**tool result**
````
ENABLE_LIVE unset: True | backend: anthropic-api
provider returned: {'x': 'ok'} | SDK messages.create invocations: 1 ['claude-sonnet-5-5']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:03.317Z

**tool call — Bash**
````
{
 "command": "ls requirements*.txt pyproject.toml Dockerfile 2>&1; cat requirements*.txt 2>/dev/null | head -30; echo ---; .venv/bin/python -I -c \"import importlib.metadata as m; print('anthropic', m.version('anthropic'))\"; echo ---; grep -rn \"ANTHROPIC_BASE_URL\\|temperature\" app/llm/backends/anthropic_api.py tests/unit/test_provider.py 2>/dev/null | head -5; echo ---; grep -rn \"ENABLE_LIVE\" spec memory/contracts memory/DECISIONS.md 2>/dev/null | head -8",
 "description": "Check dependency pins and ENABLE_LIVE spec wording"
}
````

### User / tool · 2026-11-02T02:16:03.495Z

**tool result**
````
ls: Dockerfile: No such file or directory
ls: pyproject.toml: No such file or directory
ls: requirements*.txt: No such file or directory
---
anthropic 2.3.0
---
app/llm/backends/anthropic_api.py:1:"""anthropic-api backend: Anthropic SDK, temperature 0, schema via a forced tool call. ADR-004. One attempt, no retry."""
app/llm/backends/anthropic_api.py:26:            model=model, max_tokens=MAX_TOKENS, temperature=0, system=system,
---
memory/DECISIONS.md:163:  - **The public build is demo-only.** Demo mode is on unless `ENABLE_LIVE=1` is set (and a key is present); the public Space never sets it. Demo mode uses the `fixture` backend over recorded responses shipped in the image; the real pipeline code runs and only the model answers are replayed. A "cached demo" badge is shown.
memory/contracts/api.md:43:`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every view and `ai_banner` on the review view; in live mode it also shows "Pasted text is deleted after `retention_hours` hours" with a Delete now button.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:06.967Z

**tool call — Bash**
````
{
 "command": "grep -rln \"anthropic-api\\|anthropic_api\" tests | head; echo ---; grep -rn \"ENABLE_LIVE\" tests | head -10; echo ---; grep -n \"library\\|lib\" tests/unit/test_api_routes.py | head -10; echo ---; grep -n \"def env\\|monkeypatch.setenv\\|LLM_BACKEND\" tests/unit/test_api_routes.py | head -10",
 "description": "Check whether tests cover the demo-mode live-backend gate"
}
````

### User / tool · 2026-11-02T02:16:07.101Z

**tool result**
````
tests/unit/test_provider.py
tests/unit/test_api_routes.py
tests/unit/test_provider_backends.py
---
tests/unit/test_pdf_upload.py:52:    monkeypatch.setenv("ENABLE_LIVE", "1")
tests/unit/test_pdf_upload.py:97:    monkeypatch.delenv("ENABLE_LIVE", raising=False)
tests/unit/test_api_routes.py:19:    monkeypatch.delenv("ENABLE_LIVE", raising=False)
tests/unit/test_api_routes.py:245:    monkeypatch.setenv("LLM_BACKEND", "anthropic-api"); monkeypatch.setenv("ENABLE_LIVE", "1"); monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
---
3:import pathlib
12:ROOT = pathlib.Path(__file__).resolve().parents[2]
278:def test_case_list_and_library_exist_only_in_local_mode(env, monkeypatch):
279:    """T-053 AC1: public/demo stays token-only (404); local mode lists cases and the library and loads a library case in one call."""
283:    assert c.get("/api/cases").status_code == 404 and c.get("/api/library").status_code == 404
284:    assert c.post("/api/cases", json={"library": "case_01_date_formats"}).status_code == 404
286:    lib = c.get("/api/library").json()["cases"]
287:    assert lib and "path" not in lib[0] and {"id", "name", "description"} <= set(lib[0])
288:    r = c.post("/api/cases", json={"library": lib[0]["id"]})
292:    assert "text" not in listed[0] and c.post("/api/cases", json={"library": "nope"}).status_code == 404
---
16:def env(tmp_path, monkeypatch):
17:    monkeypatch.setenv("LLM_BACKEND", "fixture")
221:    monkeypatch.setenv("LLM_BACKEND", "fixture")
245:    monkeypatch.setenv("LLM_BACKEND", "anthropic-api"); monkeypatch.setenv("ENABLE_LIVE", "1"); monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
249:    monkeypatch.setenv("PROVIDER_CAP_CONFIRMED", "1")
273:    monkeypatch.setenv("ZLAYT_MODE", "local")
285:    monkeypatch.setenv("ZLAYT_MODE", "local")
298:    monkeypatch.setenv("ZLAYT_MODE", "local")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:10.396Z

**tool call — Bash**
````
{
 "command": "curl -s -o /dev/null -w \"demo POST library %{http_code}\\n\" -H 'content-type: application/json' -d '{\"library\":\"case_lib01_er_only_then_gap\"}' http://127.0.0.1:7873/api/cases; curl -s -o /dev/null -w \"demo GET /api/cases/ %{http_code}\\n\" http://127.0.0.1:7873/api/cases/; curl -s -w \" %{http_code}\\n\" -H 'content-type: application/json' -d '{\"library\":\"../../etc/passwd\"}' http://127.0.0.1:7874/api/cases; curl -s -w \" %{http_code}\\n\" -H 'content-type: application/json' -d '{\"library\":\"case_lib01_er_only_then_gap\",\"name\":\"x\"}' http://127.0.0.1:7874/api/cases | head -c 200; echo; .venv/bin/python -I -c \"import importlib.util as u; print('playwright', bool(u.find_spec('playwright')))\"; which node npx chromium 2>/dev/null; ls ~/Library/Caches/ms-playwright 2>/dev/null | head -3",
 "description": "Probe demo 404, traversal-style library id, and check browser tooling",
 "timeout": 60000
}
````

### User / tool · 2026-11-02T02:16:10.566Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:12.402Z

**tool call — Bash**
````
{
 "command": "ps -axo pid,command | grep \"app.main\" | grep -v grep; for p in 7873 7874 7875 7876; do curl -s -o /dev/null -w \"$p %{http_code}\\n\" --max-time 5 http://127.0.0.1:$p/api/health; done",
 "description": "Check whether probe servers are still running"
}
````

### User / tool · 2026-11-02T02:16:12.581Z

**tool result**
````
53828 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
53829 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
7873 000
7874 000
7875 200
7876 200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:15.899Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -la \"$S\"; tail -n 5 \"$S/demo.log\"; echo ---; tail -n 5 \"$S/local.log\"",
 "description": "Inspect server logs for the ports that stopped responding"
}
````

### User / tool · 2026-11-02T02:16:16.043Z

**tool result**
````
total 1056
drwx------@ 164 arsis  wheel   5248 Nov  1 20:15 .
drwx------@   3 arsis  wheel     96 Nov  1 17:35 ..
-rw-r--r--@   1 arsis  wheel   2046 Nov  1 19:21 T-047-run1.json
-rw-r--r--@   1 arsis  wheel   3644 Nov  1 19:04 adr013.txt
-rw-r--r--@   1 arsis  wheel    438 Nov  1 20:15 boom_final.py
-rw-r--r--@   1 arsis  wheel    458 Nov  1 20:09 boom_server.py
drwxr-xr-x@  21 arsis  wheel    672 Nov  1 19:50 c
-rw-r--r--@   1 arsis  wheel   7451 Nov  1 18:17 cases.txt
-rw-r--r--@   1 arsis  wheel   1898 Nov  1 18:29 check.py
-rw-r--r--@   1 arsis  wheel    170 Nov  1 19:05 check_golden.out
-rw-r--r--@   1 arsis  wheel   1452 Nov  1 20:08 chk.py
-rw-r--r--@   1 arsis  wheel   1665 Nov  1 20:09 chk_mut.py
-rw-r--r--@   1 arsis  wheel   6003 Nov  1 19:58 cli1.err
-rw-r--r--@   1 arsis  wheel      0 Nov  1 19:58 cli1.txt
-rw-r--r--@   1 arsis  wheel   5746 Nov  1 19:58 cli2.err
-rw-r--r--@   1 arsis  wheel      0 Nov  1 19:58 cli2.txt
-rw-r--r--@   1 arsis  wheel   7030 Nov  1 19:59 cli_c1.err
-rw-r--r--@   1 arsis  wheel      0 Nov  1 19:59 cli_c1.txt
-rw-r--r--@   1 arsis  wheel   5829 Nov  1 20:00 cli_final.err
-rw-r--r--@   1 arsis  wheel   7173 Nov  1 20:00 cli_rep1.err
-rw-r--r--@   1 arsis  wheel   5791 Nov  1 20:00 cli_rep2.err
-rw-r--r--@   1 arsis  wheel   6139 Nov  1 20:00 cli_rep3.err
-rw-r--r--@   1 arsis  wheel    807 Nov  1 18:19 commitcases.txt
drwxr-xr-x@   6 arsis  wheel    192 Nov  1 18:20 copy
-rw-r--r--@   1 arsis  wheel    519 Nov  1 20:06 copy_untracked.py
-rwxr-xr-x@   1 arsis  wheel    491 Nov  1 18:19 cs.sh
drwxr-xr-x@   3 arsis  wheel     96 Nov  1 20:00 data
-rw-r--r--@   1 arsis  wheel   4623 Nov  1 19:51 dates.orig
drwxr-xr-x@   3 arsis  wheel     96 Nov  1 20:14 demo
-rw-r--r--@   1 arsis  wheel      0 Nov  1 20:14 demo.log
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 18:45 dl
-rw-r--r--@   1 arsis  wheel   1765 Nov  1 18:55 e1.py
-rw-r--r--@   1 arsis  wheel   5391 Nov  1 18:55 e2.py
-rw-r--r--@   1 arsis  wheel     74 Nov  1 18:37 ev.json
-rw-r--r--@   1 arsis  wheel   2393 Nov  1 18:42 ev.sh
-rw-r--r--@   1 arsis  wheel   1552 Nov  1 18:17 ex1.sh
-rw-r--r--@   1 arsis  wheel   3975 Nov  1 18:17 ex2.sh
-rw-r--r--@   1 arsis  wheel   2465 Nov  1 18:18 ex3.sh
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:13 exp-077
-rw-r--r--@   1 arsis  wheel    877 Nov  1 18:54 exp.py
-rw-r--r--@   1 arsis  wheel    774 Nov  1 18:55 exp2.py
-rw-r--r--@   1 arsis  wheel   1338 Nov  1 20:13 exp_077.py
drwxr-xr-x@  73 arsis  wheel   2336 Nov  1 18:35 fetch
drwxr-xr-x@   9 arsis  wheel    288 Nov  1 20:15 final-data
-rw-r--r--@   1 arsis  wheel   2541 Nov  1 18:37 guardprobe.py
-rw-r--r--@   1 arsis  wheel   2556 Nov  1 18:37 guardprobe.py.bak
drwxr-xr-x@   3 arsis  wheel     96 Nov  1 18:55 head
drwxr-xr-x@   8 arsis  wheel    256 Nov  1 19:01 hookcopy
-rw-r--r--@   1 arsis  wheel  11567 Nov  1 19:51 ingest.orig
lrwxr-xr-x@   1 arsis  wheel    243 Nov  1 18:20 link -> /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/copy
drwxr-xr-x@   3 arsis  wheel     96 Nov  1 20:16 live-demo
-rw-r--r--@   1 arsis  wheel   3933 Nov  1 20:15 live-demo.log
drwxr-xr-x@   3 arsis  wheel     96 Nov  1 20:16 live-local
-rw-r--r--@   1 arsis  wheel   2685 Nov  1 20:15 live-local.log
drwxr-xr-x@   3 arsis  wheel     96 Nov  1 20:14 local
-rw-r--r--@   1 arsis  wheel   2050 Nov  1 20:14 local.log
-rw-r--r--@   1 arsis  wheel    677 Nov  1 20:08 miss.py
-rw-r--r--@   1 arsis  wheel   1678 Nov  1 18:36 mkfix.py
-rw-r--r--@   1 arsis  wheel   1002 Nov  1 20:14 mkpdf.py
-rw-r--r--@   1 arsis  wheel  34991 Nov  1 18:25 mkreviews.py
drwxr-xr-x@  20 arsis  wheel    640 Nov  1 20:09 mut
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:10 mut-A
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:10 mut-B
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:10 mut-C
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:10 mut-D
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:10 mut-base
-rw-r--r--@   1 arsis  wheel   1236 Nov  1 20:09 mut.py
drwxr-xr-x@   6 arsis  wheel    192 Nov  1 19:56 mut1
drwxr-xr-x@   7 arsis  wheel    224 Nov  1 19:57 mut2
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:56 mut2_B0_pinned_baseline
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:56 mut2_G1_grounding_check_removed_in_extract
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:56 mut2_S1_judge_unavailable_fails_open_in_state
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:56 mut2_S2_judge1_error_becomes_supported
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:56 mut3_S2b_shared_judge_error_fails_open_to_supported
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:56 mut3_S3_j2_error_fails_open_to_agree_pipeline_only
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:59 mut4
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:54 mut_M0_baseline
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:54 mut_M1_sdk_internal_retries_2
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:54 mut_M2_cli_drops_strict_mcp
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:54 mut_M3_cli_timeout_600
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:54 mut_M4_cli_leaks_stderr_into_error
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:54 mut_M5_fixture_miss_retried
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:54 mut_M6_j2_error_becomes_agree
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:54 mut_M7_stray_subprocess_import_outside_backends
-rw-r--r--@   1 arsis  wheel   1950 Nov  1 19:54 mutate.py
-rw-r--r--@   1 arsis  wheel   1578 Nov  1 19:57 mutate2.py
-rw-r--r--@   1 arsis  wheel   1461 Nov  1 19:57 mutate3.py
-rw-r--r--@   1 arsis  wheel   2359 Nov  1 20:10 mutate_api.py
-rw-r--r--@   1 arsis  wheel   1509 Nov  1 20:02 mutate_run.py
-rw-r--r--@   1 arsis  wheel   2038 Nov  1 20:03 mutate_run2.py
-rw-r--r--@   1 arsis  wheel     63 Nov  1 20:09 mutrun.sh
drwxr-xr-x@   2 arsis  wheel     64 Nov  1 19:56 o1
drwx------@  14 arsis  wheel    448 Nov  1 18:22 o1.aIcW
drwxr-xr-x@   4 arsis  wheel    128 Nov  1 19:56 o2
drwx------@   5 arsis  wheel    160 Nov  1 18:22 o2.vHBZ
drwxr-xr-x@   7 arsis  wheel    224 Nov  1 18:22 old
drwxr-xr-x@   3 arsis  wheel     96 Nov  1 20:08 overlay-head
-rw-r--r--@   1 arsis  wheel   1040 Nov  1 19:50 p.py
-rw-r--r--@   1 arsis  wheel   3392 Nov  1 19:50 p2.py
-rw-r--r--@   1 arsis  wheel   1347 Nov  1 19:50 p3.py
-rw-r--r--@   1 arsis  wheel   3162 Nov  1 19:47 probe.py
-rw-r--r--@   1 arsis  wheel   1046 Nov  1 18:36 probe2.py
-rw-r--r--@   1 arsis  wheel   1028 Nov  1 18:35 probe2.py.bak
-rw-r--r--@   1 arsis  wheel    630 Nov  1 20:07 probe_run.py
drwxr-xr-x@   5 arsis  wheel    160 Nov  1 18:36 r2
-rw-r--r--@   1 arsis  wheel  11736 Nov  1 18:36 r2-cases.out
drwxr-xr-x@  28 arsis  wheel    896 Nov  1 18:53 r2src
drwxr-xr-x@  16 arsis  wheel    512 Nov  1 18:59 r3
-rw-r--r--@   1 arsis  wheel   5203 Nov  1 18:57 r3probe.py
drwxr-xr-x@   6 arsis  wheel    192 Nov  1 18:59 r3run
drwxr-xr-x@   3 arsis  wheel     96 Nov  1 18:52 r3src
-rw-r--r--@   1 arsis  wheel   2482 Nov  1 20:02 rec_all.log
-rwxr-xr-x@   1 arsis  wheel    263 Nov  1 19:57 rec_all.sh
-rw-r--r--@   1 arsis  wheel     31 Nov  1 20:05 rec_judges.log
-rw-r--r--@   1 arsis  wheel    109 Nov  1 19:56 rec_sample.log
drwxr-xr-x@   7 arsis  wheel    224 Nov  1 18:21 repo
drwxr-xr-x@   4 arsis  wheel    128 Nov  1 20:03 repro_stale
-rw-r--r--@   1 arsis  wheel  58116 Nov  1 19:58 req_mut.md
-rw-r--r--@   1 arsis  wheel    411 Nov  1 18:37 run_ro.py
-rw-r--r--@   1 arsis  wheel   1862 Nov  1 20:00 server.log
-rw-r--r--@   1 arsis  wheel  16482 Nov  1 20:00 server2.log
-rw-r--r--@   1 arsis  wheel  10562 Nov  1 19:59 server7867.log
-rw-r--r--@   1 arsis  wheel    833 Nov  1 18:28 show.py
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:54 snap
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:07 snap-077
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:14 snap-final
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:09 snap-h2
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:07 snap-head
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:55 snap2
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 19:56 snap3
drwxr-xr-x@  53 arsis  wheel   1696 Nov  1 18:34 src
drwx------@   8 arsis  wheel    256 Nov  1 18:19 srv.KdvV
-rw-r--r--@   1 arsis  wheel     38 Nov  1 18:42 srv.out
-rw-r--r--@   1 arsis  wheel    248 Nov  1 18:19 srvdir
-rw-r--r--@   1 arsis  wheel    338 Nov  1 18:30 strip.py
-rw-r--r--@   1 arsis  wheel    495 Nov  1 18:38 sync.py
drwxr-xr-x@   7 arsis  wheel    224 Nov  1 19:07 t015r4
-rw-r--r--@   1 arsis  wheel   3250 Nov  1 19:08 t028.out
drwxr-xr-x@   9 arsis  wheel    288 Nov  1 19:51 t030r2mut
drwxr-xr-x@   6 arsis  wheel    192 Nov  1 19:53 t033mut
-rw-r--r--@   1 arsis  wheel   2532 Nov  1 19:53 t033mut.py
drwxr-xr-x@   8 arsis  wheel    256 Nov  1 19:55 t035
drwxr-xr-x@   9 arsis  wheel    288 Nov  1 19:57 t038
drwxr-xr-x@  17 arsis  wheel    544 Nov  1 20:10 t038r3
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:06 t040-077
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:06 t040-head
drwxr-xr-x@   9 arsis  wheel    288 Nov  1 20:09 t040-live
drwxr-xr-x@   4 arsis  wheel    128 Nov  1 20:11 t043-239
-rw-r--r--@   1 arsis  wheel   4462 Nov  1 20:12 t043_r2_probe.py
-rw-r--r--@   1 arsis  wheel   2564 Nov  1 20:12 t043_r2_probe2.py
-rw-r--r--@   1 arsis  wheel    976 Nov  1 20:13 t043_r2_probe3.py
drwxr-xr-x@  19 arsis  wheel    608 Nov  1 20:15 t057
drwx------@  14 arsis  wheel    448 Nov  1 18:17 t1.xXug
drwx------@   5 arsis  wheel    160 Nov  1 18:17 t2.q4VB
drwx------@   5 arsis  wheel    160 Nov  1 18:17 t2b.IKsK
drwx------@  13 arsis  wheel    416 Nov  1 18:18 t3.ORDQ
drwx------@   5 arsis  wheel    160 Nov  1 18:23 t4.0u5g
-rw-r--r--@   1 arsis  wheel     33 Nov  1 20:00 tok.json
-rw-r--r--@   1 arsis  wheel     62 Nov  1 20:14 tokens.json
drwxr-xr-x@   3 arsis  wheel     96 Nov  1 18:30 tools
-rw-r--r--@   1 arsis  wheel  22388 Nov  1 20:00 view.json
-rw-r--r--@   1 arsis  wheel   1137 Nov  1 18:40 wprobe.py
-rw-r--r--@   1 arsis  wheel   6381 Nov  1 18:55 wt-golden.txt
-rw-r--r--@   1 arsis  wheel   2027 Nov  1 18:39 xss.py
---
llm call failed call_id=c36c3e7c22d3f step=flags attempt=1 prompt_hash=cee5696dde718e9b264a87e04675a120f2c81bbb04ad74f5ea7788c8aa22dd1b
llm call failed call_id=c331efe6fc8d2 step=flags attempt=1 prompt_hash=9a0c2aa23f83a2322d2cd972fd921da0417e125c3a25a5ee37c0bba06fce3c4f
llm call failed call_id=c5ddeff3324ed step=flags attempt=1 prompt_hash=a320ede9d535279fb882b00f9a4d07b7bde89ead126e48cfaa3f6154faaa8436
llm call failed call_id=cbc26b2ad02d3 step=flags attempt=1 prompt_hash=f2bc695f7cc75d1413d55821845da1fd11fe6bc87fc9a52082b82d1ae8c1917c
llm call failed call_id=c8e9c5034b277 step=flags attempt=1 prompt_hash=15676bbd3a5dfcc0ea008d7ce5df7d39df233a249a11548075e4595d1556399c
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:24.102Z

**tool call — Bash**
````
{
 "command": "for p in 7881 7882; do (lsof -iTCP:$p -sTCP:LISTEN >/dev/null 2>&1 && echo \"$p busy\") || echo \"$p free\"; done; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/r2demo\" \"$S/r2local\"; env -u ZLAYT_MODE -u ANTHROPIC_API_KEY -u LLM_BACKEND -u ENABLE_LIVE PYTHONDONTWRITEBYTECODE=1 DATA_DIR=\"$S/r2demo\" PORT=7881 HOST=127.0.0.1 .venv/bin/python -m app.main > \"$S/r2demo.log\" 2>&1 & DEMO=$!; env -u ANTHROPIC_API_KEY -u LLM_BACKEND -u ENABLE_LIVE ZLAYT_MODE=local PYTHONDONTWRITEBYTECODE=1 DATA_DIR=\"$S/r2local\" PORT=7882 HOST=127.0.0.1 .venv/bin/python -m app.main > \"$S/r2local.log\" 2>&1 & LOC=$!; echo \"pids demo=$DEMO local=$LOC\"; for i in $(seq 1 30); do curl -s -o /dev/null --max-time 2 http://127.0.0.1:7881/api/health && curl -s -o /dev/null --max-time 2 http://127.0.0.1:7882/api/health && break; sleep 1; done\necho \"== demo (7881, no ZLAYT_MODE)\"; for path in /api/cases /api/library; do curl -s -o /dev/null -w \"GET $path -> %{http_code}\\n\" --max-time 5 http://127.0.0.1:7881$path; done; curl -s -o /dev/null -w \"POST /api/cases library -> %{http_code}\\n\" --max-time 5 -H 'content-type: application/json' -d '{\"library\":\"case_lib01_er_only_then_gap\"}' http://127.0.0.1:7881/api/cases\necho \"== local (7882, ZLAYT_MODE=local)\"; for path in /api/cases /api/library; do curl -s -o /dev/null -w \"GET $path -> %{http_code}\\n\" --max-time 5 http://127.0.0.1:7882$path; done; curl -s -o /dev/null -w \"POST /api/cases library unknown -> %{http_code}\\n\" --max-time 5 -H 'content-type: application/json' -d '{\"library\":\"nope\"}' http://127.0.0.1:7882/api/cases\necho \"== traversal-ish library id on local\"; curl -s -w \" -> %{http_code}\\n\" --max-time 5 -H 'content-type: application/json' -d '{\"library\":\"../../../etc/passwd\"}' http://127.0.0.1:7882/api/cases\nkill $DEMO $LOC; sleep 1; for p in 7881 7882; do curl -s -o /dev/null -w \"after kill $p -> %{http_code}\\n\" --max-time 2 http://127.0.0.1:$p/api/health; done",
 "description": "Start demo and local servers, curl list and library routes, then kill",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T02:16:24.170Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to  %{http_code}\n)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:29.826Z

**tool call — Bash**
````
{
 "command": "for p in 7881 7882; do (lsof -iTCP:$p -sTCP:LISTEN >/dev/null 2>&1 && echo \"$p busy\") || echo \"$p free\"; done; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/r2demo\" \"$S/r2local\"; env -u ZLAYT_MODE -u ANTHROPIC_API_KEY -u LLM_BACKEND -u ENABLE_LIVE PYTHONDONTWRITEBYTECODE=1 DATA_DIR=\"$S/r2demo\" PORT=7881 HOST=127.0.0.1 .venv/bin/python -m app.main > \"$S/r2demo.log\" 2>&1 & DEMO=$!; env -u ANTHROPIC_API_KEY -u LLM_BACKEND -u ENABLE_LIVE ZLAYT_MODE=local PYTHONDONTWRITEBYTECODE=1 DATA_DIR=\"$S/r2local\" PORT=7882 HOST=127.0.0.1 .venv/bin/python -m app.main > \"$S/r2local.log\" 2>&1 & LOC=$!; echo \"pids demo=$DEMO local=$LOC\"; for i in $(seq 1 30); do curl -s -o /dev/null --max-time 2 http://127.0.0.1:7881/api/health && curl -s -o /dev/null --max-time 2 http://127.0.0.1:7882/api/health && break; sleep 1; done\necho \"== demo (7881, no ZLAYT_MODE)\"; for path in /api/cases /api/library; do curl -s -o /dev/null -w \"GET $path : %{http_code}\\n\" --max-time 5 http://127.0.0.1:7881$path; done; curl -s -o /dev/null -w \"POST /api/cases library : %{http_code}\\n\" --max-time 5 -H 'content-type: application/json' -d '{\"library\":\"case_lib01_er_only_then_gap\"}' http://127.0.0.1:7881/api/cases\necho \"== local (7882, ZLAYT_MODE=local)\"; for path in /api/cases /api/library; do curl -s -o /dev/null -w \"GET $path : %{http_code}\\n\" --max-time 5 http://127.0.0.1:7882$path; done; curl -s -o /dev/null -w \"POST /api/cases library unknown : %{http_code}\\n\" --max-time 5 -H 'content-type: application/json' -d '{\"library\":\"nope\"}' http://127.0.0.1:7882/api/cases\necho \"== traversal-ish library id on local\"; curl -s -w \" : %{http_code}\\n\" --max-time 5 -H 'content-type: application/json' -d '{\"library\":\"../../../etc/passwd\"}' http://127.0.0.1:7882/api/cases\nkill $DEMO $LOC; sleep 1; for p in 7881 7882; do curl -s -o /dev/null -w \"after kill $p : %{http_code}\\n\" --max-time 2 http://127.0.0.1:$p/api/health; done",
 "description": "Start demo and local servers, curl list and library routes, then kill",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T02:16:32.244Z

**tool result (error)**
````
Exit code 7
7881 free
7882 free
pids demo=56593 local=56594
== demo (7881, no ZLAYT_MODE)
GET /api/cases : 404
GET /api/library : 404
POST /api/cases library : 404
== local (7882, ZLAYT_MODE=local)
GET /api/cases : 200
GET /api/library : 200
POST /api/cases library unknown : 404
== traversal-ish library id on local
{"error":{"code":"not_found","message":"No such library case.","detail":{}}} : 404
/bin/bash: line 8: 56593 Terminated: 15          env -u ZLAYT_MODE -u ANTHROPIC_API_KEY -u LLM_BACKEND -u ENABLE_LIVE PYTHONDONTWRITEBYTECODE=1 DATA_DIR="$S/r2demo" PORT=7881 HOST=127.0.0.1 .venv/bin/python -m app.main > "$S/r2demo.log" 2>&1
/bin/bash: line 8: 56594 Terminated: 15          env -u ANTHROPIC_API_KEY -u LLM_BACKEND -u ENABLE_LIVE ZLAYT_MODE=local PYTHONDONTWRITEBYTECODE=1 DATA_DIR="$S/r2local" PORT=7882 HOST=127.0.0.1 .venv/bin/python -m app.main > "$S/r2local.log" 2>&1
after kill 7881 : 000
after kill 7882 : 000
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:48.087Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/ui-local\" \"$S/ui-demo\" && .venv/bin/python -I - \"$S\" <<'EOF'\nimport sys, os, subprocess, time, json, urllib.request, urllib.error\nS = sys.argv[1]; ROOT = \"/Users/arsis/zlayt-pm-project\"\nLT, DT = 7882, 7881\nGT = chr(60), chr(62)\ndef env(extra):\n    e = {k: v for k, v in os.environ.items() if k not in (\"ZLAYT_MODE\", \"ANTHROPIC_API_KEY\", \"LLM_BACKEND\", \"ENABLE_LIVE\")}\n    e.update(PYTHONDONTWRITEBYTECODE=\"1\", HOST=\"127.0.0.1\"); e.update(extra); return e\nprocs = []\ntry:\n    procs.append(subprocess.Popen([ROOT + \"/.venv/bin/python\", \"-m\", \"app.main\"], cwd=ROOT, env=env({\"ZLAYT_MODE\": \"local\", \"PORT\": str(LT), \"DATA_DIR\": S + \"/ui-local\"}), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))\n    procs.append(subprocess.Popen([ROOT + \"/.venv/bin/python\", \"-m\", \"app.main\"], cwd=ROOT, env=env({\"PORT\": str(DT), \"DATA_DIR\": S + \"/ui-demo\"}), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))\n    for port in (LT, DT):\n        for _ in range(40):\n            try:\n                urllib.request.urlopen(\"http://127.0.0.1:%d/api/health\" % port, timeout=2); break\n            except Exception: time.sleep(0.5)\n    def post(base, body):\n        r = urllib.request.Request(base + \"/api/cases\", data=json.dumps(body).encode(), method=\"POST\", headers={\"content-type\": \"application/json\"})\n        return json.loads(urllib.request.urlopen(r, timeout=60).read())\n    xss_name = GT[0] + \"img src=x onerror=alert(1)\" + GT[1]\n    c = post(\"http://127.0.0.1:%d\" % LT, {\"sample\": True, \"name\": xss_name})\n    print(\"xss case token:\", c[\"token\"][:6], \"stored name:\", c[\"name\"])\n    from playwright.sync_api import sync_playwright\n    with sync_playwright() as p:\n        b = p.chromium.launch()\n        for label, port in ((\"local\", LT), (\"demo\", DT)):\n            pg = b.new_page(); dialogs = []; errors = []\n            pg.on(\"dialog\", lambda d: (dialogs.append(d.message), d.dismiss()))\n            pg.on(\"pageerror\", lambda e: errors.append(str(e)[:120]))\n            resp = pg.goto(\"http://127.0.0.1:%d/\" % port); pg.wait_for_timeout(2500)\n            print(label, \"CSP header:\", (resp.headers.get(\"content-security-policy\") or \"\")[:60])\n            print(label, \"switcher count:\", pg.locator(\"[data-testid=case-switcher]\").count(), \"visible:\", pg.locator(\"[data-testid=case-switcher]\").is_visible() if pg.locator(\"[data-testid=case-switcher]\").count() else False)\n            if label == \"local\":\n                btn = pg.locator(\"[data-testid=case-%s]\" % c[\"token\"])\n                print(\"local xss button count:\", btn.count(), \"| textContent:\", btn.first.text_content()[:120] if btn.count() else None)\n                print(\"local xss button child <img> count:\", btn.first.locator(\"img\").count() if btn.count() else None)\n                print(\"local page img elements total:\", pg.locator(\"img\").count())\n                print(\"local library buttons:\", pg.locator(\"[data-testid=library-list] button\").count())\n                print(\"local lib01 button visible:\", pg.locator(\"[data-testid=library-case_lib01_er_only_then_gap]\").is_visible())\n                pg.screenshot(path=os.path.join(S, \"ui-local\", \"switcher-local.png\"), full_page=False)\n                print(\"local dialogs:\", dialogs, \"pageerrors:\", errors[:3])\n            else:\n                print(\"demo dialogs:\", dialogs, \"pageerrors:\", errors[:3])\n                pg.screenshot(path=os.path.join(S, \"ui-demo\", \"switcher-demo.png\"), full_page=False)\n            pg.close()\n        b.close()\nfinally:\n    for pr in procs: pr.terminate()\n    time.sleep(1)\n    print(\"servers terminated:\", all(pr.poll() is not None for pr in procs))\nEOF",
 "description": "Run Playwright UI checks for switcher presence, XSS-named case, and dialogs",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:16:55.493Z

**tool result**
````
xss case token: GqU_7n stored name: <img src=x onerror=alert(1)>
local CSP header: default-src 'none'; script-src 'self'; script-src-attr 'unsa
local switcher count: 1 visible: True
local xss button count: 1 | textContent: Open: <img src=x onerror=alert(1)>ingested · 9 records · 6 pending
local xss button child <img> count: 0
local page img elements total: 0
local library buttons: 7
local lib01 button visible: True
local dialogs: [] pageerrors: []
demo CSP header: default-src 'none'; script-src 'self'; script-src-attr 'unsa
demo switcher count: 0 visible: False
demo dialogs: [] pageerrors: []
servers terminated: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:31.147Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD; git status --short app/frontend/switcher.js app/frontend/index.html app/backend/api.py app/llm/provider.py app/llm/backends/anthropic_api.py; git ls-files .env | wc -l; git check-ignore -v .env; echo ---; grep -n \"ENABLE_LIVE\\|anthropic-api\" app/backend/api.py | head; echo ---; grep -n 'elif name in\\|if name == \"fixture\"' app/llm/provider.py; grep -n \"def call\\|ANTHROPIC_API_KEY\" app/llm/backends/anthropic_api.py; echo ---; grep -n \"host=\" app/main.py; echo ---; grep -n \"def allowed_hashes\" -A2 app/backend/api.py | head -4",
 "description": "Pin HEAD, check tracked status of changed files, and collect line references"
}
````

### User / tool · 2026-11-02T02:17:31.347Z

**tool result**
````
864676f
 M app/backend/api.py
       0
.gitignore:25:*.env	.env
---
91:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
92:        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
100:        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
329:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
---
88:    if name == "fixture":
90:    elif name in ("claude-cli", "anthropic-api"):
15:    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"), max_retries=0, timeout=TIMEOUT_S)
18:def call(model: str, system: str, user: str, json_schema: dict, *, key: str = "", client=None) -> LLMResult:
20:        if not os.environ.get("ANTHROPIC_API_KEY"):
---
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
---
87:    def allowed_hashes():
88-        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
89-    runs = {}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:34.870Z

**tool call — Bash**
````
{
 "command": "git log --oneline -n 6 | cat; echo ---; git diff --stat | tail -3; echo ---; git diff -- app/backend/api.py | head -80",
 "description": "Check recent commits and the uncommitted api.py diff"
}
````

### User / tool · 2026-11-02T02:17:35.040Z

**tool result**
````
864676f fix(db): delete old-schema database at rebuild instead of keeping a copy (T-050, T-040 security r2)
037cc89 chore(orchestrator): D-032/D-033; debt-close from in_review; T-036/T-038 closed
996f9b4 feat(frontend): local-mode case switcher and library loader (T-053 AC2)
5f8858f feat(db): log-only review actions not_duplicate, manual_entry; schema version rebuild (T-062)
dd545e3 feat(research): narrow lexicon self_report to explicit patient attribution (T-061)
099732b feat(backend): LLM split fallback for unsplit pastes, validated by code, flagged LLM_SPLIT (T-057, D-031)
---
 ...aee0fb0ea71d69a649ee254dd01d885b4b69bfda1e.json |   2 +-
 tests/unit/test_pdf_upload.py                      |  57 +++++++
 234 files changed, 746 insertions(+), 356 deletions(-)
---
diff --git a/app/backend/api.py b/app/backend/api.py
index 654383c..23449cc 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -4,6 +4,7 @@ Demo mode (D-008/D-020): only text whose normalised sha256 is a golden input is
 anything is stored. Never logs record text, tokens or prompts (run uvicorn with access_log off; see app/main.py).
 """
 import hashlib
+import asyncio
 import json
 import logging
 import os
@@ -16,6 +17,8 @@ from fastapi.exceptions import RequestValidationError
 from fastapi.responses import JSONResponse, Response
 from starlette.exceptions import HTTPException as StarletteHTTPException
 
+from starlette.concurrency import run_in_threadpool
+
 from app.backend import ingest, pdf_text, present, review, store
 from app.db import db as DB
 
@@ -227,6 +230,8 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
     @app.post("/api/cases/pdf", status_code=201)
     async def create_case_from_pdf(request: Request, name: str = None):
         """D-031: raw PDF bytes (Content-Type application/pdf). Text layer only; a scanned PDF is refused before anything is stored or run."""
+        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
+            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
         cl = request.headers.get("content-length")
         if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
             raise ApiError(413, "input_too_large", "The PDF is too large.")
@@ -235,8 +240,10 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             data += chunk
             if len(data) > pdf_text.MAX_PDF_BYTES:
                 raise ApiError(413, "input_too_large", "The PDF is too large.")
-        try:
-            got = pdf_text.extract(data)
+        try:       # parsing runs off the event loop (so /api/health stays responsive) under a time cap
+            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data), pdf_text.EXTRACT_TIMEOUT_S)
+        except asyncio.TimeoutError:
+            raise ApiError(400, "bad_request", _PDF_MESSAGES["pdf_unreadable"], {"reason": "pdf_timeout"}) from None
         except pdf_text.PdfError as e:
             raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
                            _PDF_MESSAGES[e.code], {"reason": e.code}) from None
@@ -363,6 +370,30 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         finally:
             c.close()
 
+    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
+    async def manual_entry(token: str, rid: str, request: Request):
+        """D-031: the reviewer writes the entry for a record the AI could not make one for. Quote = whole verbatim sentences (422 otherwise)."""
+        b = await body_of(request)
+        c = conn()
+        try:
+            get_case(c, token)
+            return review.manual_entry(c, token, rid, b, call=make_call(c, token))
+        finally:
+            c.close()
+
+    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
+    async def not_duplicate(token: str, item_id: str, request: Request):
+        """D-031: split one record back out of a merged entry. Body {record_id}."""
+        b = await body_of(request)
+        if not isinstance(b.get("record_id"), str):
+            raise ApiError(400, "bad_request", "Provide the record to split off.")
+        c = conn()
+        try:
+            get_case(c, token)
+            return review.not_duplicate(c, token, item_id, b["record_id"], call=make_call(c, token))
+        finally:
+            c.close()
+
     @app.get("/api/cases/{token}/items/{item_id}")
     def item(token: str, item_id: str):
         c = conn()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:40.055Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git diff --quiet 2c2eb1f HEAD -- app/llm/provider.py app/llm/backends/anthropic_api.py app/main.py && echo \"provider/anthropic_api/main unchanged since 2c2eb1f\"; git show HEAD:app/backend/api.py | grep -n \"def allowed_hashes\" -A1 | head -3; git show HEAD:app/backend/api.py | grep -c '@app.get(\"/api/cases\")'; git show --stat 996f9b4 | tail -8",
 "description": "Confirm provider and entrypoint unchanged since T-053 commit, and HEAD gate"
}
````

### User / tool · 2026-11-02T02:17:40.240Z

**tool result**
````
864676f
provider/anthropic_api/main unchanged since 2c2eb1f
84:    def allowed_hashes():
85-        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
1
    feat(frontend): local-mode case switcher and library loader (T-053 AC2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/frontend/index.html  |  1 +
 app/frontend/review.css  |  8 ++++++
 app/frontend/switcher.js | 64 ++++++++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 73 insertions(+)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:45.004Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I - \"$S\" <<'EOF'\nimport sys, re, glob, hashlib, sqlite3, os\nS = sys.argv[1]; R = \"/Users/arsis/zlayt-pm-project\"\nnorm = lambda s: re.sub(r\"\\s+\", \" \", s.replace(\"\\r\\n\", \"\\n\")).strip()\ngolden = {hashlib.sha256(norm(open(p).read()).encode()).hexdigest() for p in glob.glob(R + \"/evals/golden/*.txt\")}\nlib = sorted(glob.glob(R + \"/evals/library/*.txt\"))\nprint(\"library files:\", len(lib), \"| library texts whose normalized sha256 is a golden (recorded) input:\", sum(hashlib.sha256(norm(open(p).read()).encode()).hexdigest() in golden for p in lib))\nc = sqlite3.connect(os.path.join(S, \"local\", \"zlayt.sqlite\"))\nprint(\"local-probe llm_calls by backend/error:\", c.execute(\"SELECT backend, error, count(*) FROM llm_calls GROUP BY backend, error\").fetchall())\nprint(\"local-probe cases (source, demo_mode, status):\", c.execute(\"SELECT source, demo_mode, status FROM cases\").fetchall())\nEOF",
 "description": "Check library texts against golden recorded inputs and probe DB outcomes"
}
````

### User / tool · 2026-11-02T02:17:45.115Z

**tool result**
````
library files: 7 | library texts whose normalized sha256 is a golden (recorded) input: 0
local-probe llm_calls by backend/error: [('fixture', None, 39), ('fixture', 'FIXTURE_MISS 15676bbd3a5dfcc0ea008d7ce5df7d39df233a249a11548075e4595d1556399c', 1), ('fixture', 'FIXTURE_MISS 3571166930f3ee019a7d2d0b254863e710d259d1b5da4d458ca4eadae9cf7c6b', 1), ('fixture', 'FIXTURE_MISS 35f88fbe68632afb7e5f3efb286b5364006950e624594f057dca25d7ef3d2192', 1), ('fixture', 'FIXTURE_MISS 3a5c185e71a4fab40b3d4a735c2af0eb9d14eef489161f85fda8e8c0586c3048', 1), ('fixture', 'FIXTURE_MISS 4c7e35689e20a98dcb58088f3ca68e6233c027c6e55cf055bfe5ef9ef9bcf5ca', 1), ('fixture', 'FIXTURE_MISS 83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557', 1), ('fixture', 'FIXTURE_MISS 9a0c2aa23f83a2322d2cd972fd921da0417e125c3a25a5ee37c0bba06fce3c4f', 1), ('fixture', 'FIXTURE_MISS a320ede9d535279fb882b00f9a4d07b7bde89ead126e48cfaa3f6154faaa8436', 1), ('fixture', 'FIXTURE_MISS c34540e57c9499ee4f8143daf120f8481176c0dbae502290544711505ebae5ae', 1), ('fixture', 'FIXTURE_MISS c7afe5d6e22ac27e694269f801bf4472efa3dea6e7925b2afcb6baf74e85ac41', 1), ('fixture', 'FIXTURE_MISS cee5696dde718e9b264a87e04675a120f2c81bbb04ad74f5ea7788c8aa22dd1b', 1), ('fixture', 'FIXTURE_MISS d32270051a558dc270ee37faf3470cd58015a790d4d615c10ea470c4a547c389', 1), ('fixture', 'FIXTURE_MISS e9f5383b127e3b9f2dcf8a4cc966fcedb678286b3f335dd0b6e9b1f4f1b56f16', 1), ('fixture', 'FIXTURE_MISS f2bc695f7cc75d1413d55821845da1fd11fe6bc87fc9a52082b82d1ae8c1917c', 1), ('fixture', 'FIXTURE_MISS f65328e4891ae2019525628ff0f28ec0a9f39ee4b124806afe988a0e828aa539', 1)]
local-probe cases (source, demo_mode, status): [('sample', 1, 'ready'), ('paste', 1, 'ready')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:52.020Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I - \"$S\" <<'EOF'\nimport sys, sqlite3, os\nc = sqlite3.connect(os.path.join(sys.argv[1], \"local\", \"zlayt.sqlite\")); c.row_factory = sqlite3.Row\ntabs = [r[0] for r in c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")]\nprint(\"tables:\", tabs)\nfor t in (\"entries\", \"flags\", \"amounts\"):\n    if t in tabs:\n        cols = [r[1] for r in c.execute(f\"PRAGMA table_info({t})\")]\n        print(t, \"cols:\", cols)\n        vs = [x for x in cols if \"verif\" in x or \"grounded\" in x or \"status\" in x or \"judge\" in x]\n        for v in vs[:3]:\n            print(\"  \", t, v, c.execute(f\"SELECT {v} v, count(*) n FROM {t} GROUP BY {v}\").fetchall()[:6])\n        print(\"  \", t, \"case-split rows:\", c.execute(f\"SELECT case_id, count(*) n FROM {t} GROUP BY case_id\").fetchall())\nEOF",
 "description": "Inspect verification states for the library case in the probe DB"
}
````

### User / tool · 2026-11-02T02:17:52.125Z

**tool result**
````
tables: ['cases', 'records', 'entries', 'amounts', 'flags', 'llm_calls', 'review_events']
entries cols: ['id', 'case_id', 'record_ids_json', 'seq', 'date_iso', 'provider', 'summary', 'excerpt', 'excerpt_start', 'excerpt_end', 'state', 'state_reasons_json', 'review_status', 'edited_json', 'ladder_json', 'updated_at']
   entries review_status [<sqlite3.Row object at 0x1006a5960>, <sqlite3.Row object at 0x1006a5f90>]
   entries case-split rows: [<sqlite3.Row object at 0x1006a6140>]
flags cols: ['id', 'case_id', 'type', 'category', 'source_kind', 'title', 'explanation', 'computed_json', 'evidence_json', 'origin', 'reviewer_note', 'state', 'state_reasons_json', 'review_status', 'edited_json', 'ladder_json', 'updated_at']
   flags review_status [<sqlite3.Row object at 0x1006a6020>]
   flags case-split rows: [<sqlite3.Row object at 0x1006a5930>, <sqlite3.Row object at 0x1006a6080>]
amounts cols: ['id', 'case_id', 'record_ids_json', 'entry_id', 'text', 'value_cents', 'kind', 'excerpt', 'excerpt_start', 'excerpt_end', 'duplicate_note', 'state', 'state_reasons_json', 'review_status', 'edited_json', 'ladder_json', 'updated_at']
   amounts review_status [<sqlite3.Row object at 0x1006a6230>]
   amounts case-split rows: [<sqlite3.Row object at 0x1006a6140>, <sqlite3.Row object at 0x1006a6260>]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:55.536Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I - \"$S\" <<'EOF'\nimport sys, sqlite3, os\nc = sqlite3.connect(os.path.join(sys.argv[1], \"local\", \"zlayt.sqlite\"))\nfor cid, name, st in c.execute(\"SELECT id, name, status FROM cases\"):\n    print(\"case\", name, st)\n    print(\"  entries state:\", c.execute(\"SELECT state, count(*) FROM entries WHERE case_id=? GROUP BY state\", (cid,)).fetchall())\n    print(\"  flags state:\", c.execute(\"SELECT state, count(*) FROM flags WHERE case_id=? GROUP BY state\", (cid,)).fetchall())\n    print(\"  amounts state:\", c.execute(\"SELECT state, count(*) FROM amounts WHERE case_id=? GROUP BY state\", (cid,)).fetchall())\nEOF",
 "description": "Summarize grounding states per case in the probe DB"
}
````

### User / tool · 2026-11-02T02:17:55.644Z

**tool result**
````
case Sample case ready
  entries state: [('verified', 9)]
  flags state: [('needs_review', 5), ('verified', 5)]
  amounts state: [('needs_review', 2), ('verified', 2)]
case case lib01 er only then gap ready
  entries state: []
  flags state: [('needs_review', 1), ('verified', 1)]
  amounts state: [('needs_review', 2)]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:07.395Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-probe.py",
 "content": "# T-053 security probe (security-reviewer). No network, no writes outside a temp dir.\n# Run from the project root: .venv/bin/python -I artifacts/review-evidence/T-053-security-probe.py\nimport os\nimport pathlib\nimport sys\nimport tempfile\nimport types\n\nROOT = pathlib.Path(__file__).resolve().parents[2]\nsys.path.insert(0, str(ROOT))\nSCHEMA = {\"type\": \"object\", \"properties\": {\"x\": {\"type\": \"string\"}}, \"required\": [\"x\"], \"additionalProperties\": False}\n\n# Part 1: demo mode (ENABLE_LIVE unset, so /health says demo_mode true) with LLM_BACKEND=anthropic-api and a key.\n# The SDK client is stubbed so nothing leaves the machine; the question is whether the provider asks the SDK to call the API.\nos.environ.pop(\"ENABLE_LIVE\", None)\nos.environ.pop(\"ZLAYT_MODE\", None)\nos.environ[\"LLM_BACKEND\"] = \"anthropic-api\"\nos.environ[\"ANTHROPIC_API_KEY\"] = \"sk-probe-not-a-real-key\"\nfrom app.llm import provider as P  # noqa: E402\nfrom app.llm.backends import anthropic_api as be  # noqa: E402\n\nsdk_calls = []\n\n\nclass _Msgs:\n    def create(self, **kw):\n        sdk_calls.append(kw[\"model\"])\n        blk = types.SimpleNamespace(type=\"tool_use\", input={\"x\": \"ok\"})\n        return types.SimpleNamespace(content=[blk], model=kw[\"model\"], usage=types.SimpleNamespace(input_tokens=1, output_tokens=1))\n\n\nclass _Fake:\n    messages = _Msgs()\n\n\nbe.make_client = lambda: _Fake()\nout = P.complete(\"claude-sonnet-5-5\", \"sys\", \"synthetic text\", SCHEMA)\nprint(\"PART1 ENABLE_LIVE set:\", \"ENABLE_LIVE\" in os.environ, \"| backend:\", P.backend_name(),\n      \"| provider returned:\", out, \"| SDK messages.create invocations:\", len(sdk_calls))\n\n# Part 2: library texts through the demo gate, public (no ZLAYT_MODE) vs local.\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ.pop(\"ANTHROPIC_API_KEY\", None)\nfrom fastapi.testclient import TestClient  # noqa: E402\nfrom app.backend.api import create_app  # noqa: E402\n\nfor mode in (None, \"local\"):\n    if mode is None:\n        os.environ.pop(\"ZLAYT_MODE\", None)\n    else:\n        os.environ[\"ZLAYT_MODE\"] = mode\n    d = tempfile.mkdtemp(prefix=\"t053probe-\")\n    c = TestClient(create_app(db_path=os.path.join(d, \"p.sqlite\")))\n    health = c.get(\"/api/health\").json()\n    lst = c.get(\"/api/cases\").status_code\n    lib_post = c.post(\"/api/cases\", json={\"library\": \"case_lib01_er_only_then_gap\"})\n    print(\"PART2 ZLAYT_MODE=%s demo_mode=%s GET /api/cases=%d POST library=%d\" % (mode, health[\"demo_mode\"], lst, lib_post.status_code))\n"
}
````

### User / tool · 2026-11-02T02:18:07.502Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:09.042Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-053-security-probe.py 2>&1 | tail -20",
 "description": "Run the T-053 security probe script and show output",
 "timeout": 180000
}
````

### User / tool · 2026-11-02T02:18:09.659Z

**tool result**
````
c61e84f
PART1 ENABLE_LIVE set: False | backend: anthropic-api | provider returned: {'x': 'ok'} | SDK messages.create invocations: 1
PART2 ZLAYT_MODE=None demo_mode=True GET /api/cases=404 POST library=404
PART2 ZLAYT_MODE=local demo_mode=True GET /api/cases=200 POST library=201
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:12.491Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log --oneline -n 3 | cat && git diff --quiet 2c2eb1f HEAD -- app/llm/provider.py app/llm/backends/anthropic_api.py app/main.py && echo \"provider, anthropic_api, main.py unchanged 2c2eb1f..HEAD\" ; git show HEAD:app/backend/api.py | grep -n \"return app.state.recorded\" ; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py tests/e2e/test_api.py -q 2>&1 | tail -4",
 "description": "Pin HEAD, confirm gate code unchanged, and rerun route tests",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:18:20.405Z

**tool result**
````
c61e84f
c61e84f fix(db): bump schema version to 3, real v2 rebuild test (T-062 r2)
d548ccd feat(backend): manual entry for a rejected record and 'not a duplicate' split (T-056, D-031)
c143c4b docs(research): UI reference study and UI design brief draft (T-060 pass 1)
provider, anthropic_api, main.py unchanged 2c2eb1f..HEAD
88:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
...............................                                          [100%]
31 passed in 7.41s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:24.169Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/backend/api.py | grep -n 'def list_cases\\|def library\\|if not local_mode\\|ENABLE_LIVE\") == \"1\" and os.environ.get(\"PROVIDER\\|def live_enabled\\|def demo_mode\\|if demo_mode() and digest' ; git show HEAD:app/llm/provider.py | grep -n 'name == \"fixture\"\\|elif name in'; git show HEAD:app/llm/backends/anthropic_api.py | grep -n 'def call\\|ANTHROPIC_API_KEY'; git show HEAD:app/main.py | grep -n \"host=\"; git show HEAD:app/frontend/switcher.js | grep -n 'ZL.el\\|createTextNode\\|textContent' | head -3; git show HEAD:app/frontend/dom.js | grep -n \"createTextNode\"",
 "description": "Get line references at HEAD for the cited code"
}
````

### User / tool · 2026-11-02T02:18:24.363Z

**tool result**
````
59:def library_cases() -> list:
91:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
99:    def live_enabled():
102:    def demo_mode():
199:    def list_cases():
200:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
209:    def library():
210:        if not local_mode():
220:            if not local_mode():
257:        if demo_mode() and digest(text) not in allowed_hashes():
327:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
88:    if name == "fixture":
90:    elif name in ("claude-cli", "anthropic-api"):
15:    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"), max_retries=0, timeout=TIMEOUT_S)
18:def call(model: str, system: str, user: str, json_schema: dict, *, key: str = "", client=None) -> LLMResult:
20:        if not os.environ.get("ANTHROPIC_API_KEY"):
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
2:   Lists cases (open with one click) and the synthetic library (POST /cases {library:id}, then run). Text via ZL.el only. */
13:  function say(msg, isError) { const p = root && root.querySelector(".cs-msg"); if (p) { p.textContent = msg || ""; p.setAttribute("role", isError ? "alert" : "status"); } }
16:      e.append(c.nodeType ? c : document.createTextNode(String(c)));
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:30.627Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-ui-probe.py",
 "content": "# T-053 UI probe (security-reviewer): switcher presence per mode, XSS-named case rendered as text, no dialogs.\n# Starts two servers on 127.0.0.1 (local on 7882, public-style demo on 7881) with temp data dirs, then stops them.\n# Run from the project root: .venv/bin/python -I artifacts/review-evidence/T-053-security-ui-probe.py\nimport json\nimport os\nimport pathlib\nimport subprocess\nimport sys\nimport tempfile\nimport time\nimport urllib.request\n\nROOT = pathlib.Path(__file__).resolve().parents[2]\nEVID = ROOT / \"artifacts\" / \"review-evidence\"\nLT, DT = 7882, 7881\nLT_TAG = chr(60) + \"img src=x onerror=alert(1)\" + chr(62)  # the XSS probe string, spelled out so no literal angle brackets appear in this file\n\n\ndef env(extra):\n    e = {k: v for k, v in os.environ.items() if k not in (\"ZLAYT_MODE\", \"ANTHROPIC_API_KEY\", \"LLM_BACKEND\", \"ENABLE_LIVE\")}\n    e.update(PYTHONDONTWRITEBYTECODE=\"1\", HOST=\"127.0.0.1\")\n    e.update(extra)\n    return e\n\n\ndef post(base, body):\n    r = urllib.request.Request(base + \"/api/cases\", data=json.dumps(body).encode(), method=\"POST\", headers={\"content-type\": \"application/json\"})\n    return json.loads(urllib.request.urlopen(r, timeout=60).read())\n\n\ntmp = tempfile.mkdtemp(prefix=\"t053ui-\")\nprocs = []\ntry:\n    procs.append(subprocess.Popen([str(ROOT / \".venv/bin/python\"), \"-m\", \"app.main\"], cwd=str(ROOT),\n                                  env=env({\"ZLAYT_MODE\": \"local\", \"PORT\": str(LT), \"DATA_DIR\": tmp + \"/local\"}), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))\n    procs.append(subprocess.Popen([str(ROOT / \".venv/bin/python\"), \"-m\", \"app.main\"], cwd=str(ROOT),\n                                  env=env({\"PORT\": str(DT), \"DATA_DIR\": tmp + \"/demo\"}), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))\n    for port in (LT, DT):\n        for _ in range(60):\n            try:\n                urllib.request.urlopen(\"http://127.0.0.1:%d/api/health\" % port, timeout=2)\n                break\n            except Exception:\n                time.sleep(0.5)\n    case = post(\"http://127.0.0.1:%d\" % LT, {\"sample\": True, \"name\": LT_TAG})\n    print(\"case created, stored name:\", case[\"name\"])\n    from playwright.sync_api import sync_playwright\n    with sync_playwright() as p:\n        b = p.chromium.launch()\n        for label, port in ((\"local\", LT), (\"demo\", DT)):\n            pg = b.new_page()\n            dialogs, errors = [], []\n            pg.on(\"dialog\", lambda d: (dialogs.append(d.message), d.dismiss()))\n            pg.on(\"pageerror\", lambda e: errors.append(str(e)[:120]))\n            resp = pg.goto(\"http://127.0.0.1:%d/\" % port)\n            pg.wait_for_timeout(2500)\n            sw = pg.locator(\"[data-testid=case-switcher]\")\n            print(label, \"| CSP:\", (resp.headers.get(\"content-security-policy\") or \"\")[:40], \"| switcher count:\", sw.count(),\n                  \"| visible:\", sw.is_visible() if sw.count() else False)\n            if label == \"local\":\n                btn = pg.locator(\"[data-testid=case-%s]\" % case[\"token\"])\n                print(\"local | xss case button count:\", btn.count(), \"| text:\", btn.first.text_content()[:70] if btn.count() else None)\n                print(\"local | <img> elements inside that button:\", btn.first.locator(\"img\").count() if btn.count() else None,\n                      \"| <img> elements on page:\", pg.locator(\"img\").count())\n                print(\"local | library buttons:\", pg.locator(\"[data-testid=library-list] button\").count(),\n                      \"| lib01 visible:\", pg.locator(\"[data-testid=library-case_lib01_er_only_then_gap]\").is_visible())\n                pg.screenshot(path=str(EVID / \"T-053-security-switcher-local.png\"))\n            else:\n                pg.screenshot(path=str(EVID / \"T-053-security-switcher-demo.png\"))\n            print(label, \"| dialogs:\", dialogs, \"| page errors:\", errors[:3])\n            pg.close()\n        b.close()\nfinally:\n    for pr in procs:\n        pr.terminate()\n    time.sleep(1)\n    print(\"servers stopped:\", all(pr.poll() is not None for pr in procs))\n"
}
````

### User / tool · 2026-11-02T02:18:30.724Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-ui-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:32.148Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && .venv/bin/python -I artifacts/review-evidence/T-053-security-ui-probe.py 2>&1 | tail -20; ls -la artifacts/review-evidence/T-053-security-*.png",
 "description": "Run the UI probe and confirm screenshots were written",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:18:39.511Z

**tool result**
````
c61e84f
case created, stored name: <img src=x onerror=alert(1)>
local | CSP: default-src 'none'; script-src 'self'; s | switcher count: 1 | visible: True
local | xss case button count: 1 | text: Open: <img src=x onerror=alert(1)>ingested · 9 records · 6 pending
local | <img> elements inside that button: 0 | <img> elements on page: 0
local | library buttons: 7 | lib01 visible: True
local | dialogs: [] | page errors: []
demo | CSP: default-src 'none'; script-src 'self'; s | switcher count: 0 | visible: False
demo | dialogs: [] | page errors: []
servers stopped: True
-rw-r--r--@ 1 arsis  staff   43246 Nov  1 20:18 artifacts/review-evidence/T-053-security-switcher-demo.png
-rw-r--r--@ 1 arsis  staff  137235 Nov  1 20:18 artifacts/review-evidence/T-053-security-switcher-local.png
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:40.686Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-switcher-local.png"
}
````

### User / tool · 2026-11-02T02:18:40.695Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:09.536Z

**tool call — Bash**
````
{
 "command": "git show 2c2eb1f | grep -c -i \"sk-ant\\|sk-proj\\|api_key=\\|ANTHROPIC_API_KEY=<redacted> ; git show 996f9b4 | grep -c -i \"sk-ant\\|sk-proj\\|ANTHROPIC_API_KEY=<redacted> head -30 tools/check_secrets.py | grep -n '\"\"\"' -A4 | head -12; timeout 120 .venv/bin/python tools/check_secrets.py > /dev/null 2>&1; echo \"check_secrets exit=$?\"",
 "description": "Scan T-053 commits for key-shaped strings and run the secrets checker",
 "timeout": 180000
}
````

### User / tool · 2026-11-02T02:19:09.710Z

**tool result**
````
0
0
2:"""Secret scanner. `--staged` checks what is staged for commit (used by git-guard and the native pre-commit hook);
3-default scans tracked files. Exit 1 with a list of hits if a key-shaped string or an env file would enter git.
4-Never prints the secret itself.
5-
6-Round 2 (T-006 security review): NUL-separated file names (spaces/unicode safe), renames/copies included,
--
10:"""
11-from __future__ import annotations
12-import re
13-import subprocess
14-import sys
check_secrets exit=127
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:11.149Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python tools/check_secrets.py; echo \"check_secrets exit=$?\"",
 "description": "Run the repo secrets checker over tracked files",
 "timeout": 180000
}
````

### User / tool · 2026-11-02T02:19:11.657Z

**tool result**
````
check_secrets: ok (716 file(s) scanned)
check_secrets exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:14.292Z

**tool call — Bash**
````
{
 "command": "grep -o '\"persona\": \"[^\"]*\"' reviews/T-040-security.md reviews/T-051-privacy-compliance-r3.md | head -3; grep -o '\"model\": \"[^\"]*\"' reviews/T-040-security.md | head -2; grep -o '\"verdict\": \"[^\"]*\"' reviews/T-040-security.md; sed -n 1,12p reviews/T-040-security.md | cut -c1-200",
 "description": "Check format of an existing security review record"
}
````

### User / tool · 2026-11-02T02:19:14.428Z

**tool result**
````
reviews/T-051-privacy-compliance-r3.md:"persona": "privacy-compliance-reviewer"
reviews/T-040-security.md:"persona": "security-reviewer"
"model": "claude-sonnet-5-5"
"verdict": "fail"
# T-040 security review (security-reviewer, Tomás Rivas lens)

Commit under review: a7df086 (HEAD moved f861159 -> e274322 -> cd4bc60 during the review; api/review/store/main unchanged by those).
Verdict: **fail**. One blocker (single request locks the public demo out for everyone), two majors.

Verified clean: demo gate refuses unrecorded text with 409 and nothing stored (row counts 0/0/0/0/0/0/0 before and after, also after 400/413/400 errors); empty 400, oversize 413 (70k chars and a 100 M

Findings are in the JSON block. The export "router" (`export_routes.router`) is never included (`grep -rn include_router app` -> no hits); the same URL is served by an inline route in api.py:277, so t

```json
{"card": "T-040", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit a7df086 (app/backend/api.py, review.py, store.py, present.py, app/main.py); app run with LLM_BACKEND=fixture on :7961, DATA_DIR in scratchpad; case_01_date_formats + sample",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:40.061Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-probe.py",
 "old_string": "    print(\"PART2 ZLAYT_MODE=%s demo_mode=%s GET /api/cases=%d POST library=%d\" % (mode, health[\"demo_mode\"], lst, lib_post.status_code))\n",
 "new_string": "    print(\"PART2 ZLAYT_MODE=%s demo_mode=%s GET /api/cases=%d POST library=%d\" % (mode, health[\"demo_mode\"], lst, lib_post.status_code))\n\n# Part 3: are the library texts recorded inputs (normalised sha256 equal to an evals/golden text)?\nimport glob  # noqa: E402\nimport hashlib  # noqa: E402\nimport re  # noqa: E402\n\n\ndef _norm_hash(text):\n    return hashlib.sha256(re.sub(r\"\\s+\", \" \", text.replace(\"\\r\\n\", \"\\n\")).strip().encode()).hexdigest()\n\n\ngolden = {_norm_hash(open(p).read()) for p in glob.glob(str(ROOT / \"evals/golden/*.txt\"))}\nlib = sorted(glob.glob(str(ROOT / \"evals/library/*.txt\")))\nprint(\"PART3 library files:\", len(lib), \"| library texts equal to a golden recorded input:\", sum(_norm_hash(open(p).read()) in golden for p in lib))\n"
}
````

### User / tool · 2026-11-02T02:19:40.162Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-probe.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:41.673Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-053-security-probe.py 2>&1 | tail -8; .venv/bin/python -I -c \"import importlib.metadata as m; print('anthropic', m.version('anthropic'))\"; ls requirements*.txt pyproject.toml Makefile 2>&1 | head -3",
 "description": "Rerun the probe with the library-hash check and confirm SDK version and pin files",
 "timeout": 180000
}
````

### User / tool · 2026-11-02T02:19:42.235Z

**tool result**
````
c61e84f
PART1 ENABLE_LIVE set: False | backend: anthropic-api | provider returned: {'x': 'ok'} | SDK messages.create invocations: 1
PART2 ZLAYT_MODE=None demo_mode=True GET /api/cases=404 POST library=404
PART2 ZLAYT_MODE=local demo_mode=True GET /api/cases=200 POST library=201
PART3 library files: 7 | library texts equal to a golden recorded input: 0
anthropic 2.3.0
ls: Makefile: No such file or directory
ls: pyproject.toml: No such file or directory
ls: requirements*.txt: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:19:44.900Z

**tool call — Bash**
````
{
 "command": "for p in 7875 7876; do pid=$(lsof -tiTCP:$p -sTCP:LISTEN 2>/dev/null | head -1); if [ -n \"$pid\" ]; then echo \"port $p pid $pid: $(ps -o command= -p $pid | cut -c1-80)\"; kill $pid; fi; done; sleep 2; for p in 7875 7876 7881 7882; do curl -s -o /dev/null -w \"port $p : %{http_code}\\n\" --max-time 2 http://127.0.0.1:$p/api/health; done",
 "description": "Stop the leftover probe servers on ports 7875 and 7876",
 "timeout": 30000
}
````

### User / tool · 2026-11-02T02:19:47.214Z

**tool result (error)**
````
Exit code 7
port 7875 pid 53829: /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3
port 7876 pid 53828: /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3
port 7875 : 000
port 7876 : 000
port 7881 : 000
port 7882 : 000
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:20.867Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-053-security.md",
 "content": "# T-053 security review (security-reviewer, Tomás Rivas lens)\n\nCommits under review: 2c2eb1f (backend: api.py, present.py, tests) and 996f9b4 (frontend: switcher.js, index.html). HEAD moved during the review (2c2eb1f -> 864676f -> c61e84f); provider.py, anthropic_api.py and main.py are unchanged across 2c2eb1f..HEAD (`git diff --quiet 2c2eb1f HEAD -- app/llm/provider.py app/llm/backends/anthropic_api.py app/main.py` exit 0). Tests and servers ran against the working tree at c61e84f; api.py carried another agent's uncommitted PDF edits outside the T-053 paths.\n\nVerdict: **fail**. One blocker: demo mode sends live Anthropic SDK calls whenever `LLM_BACKEND=anthropic-api` and a key are set, with `ENABLE_LIVE` unset. The local-mode case list and library gate work as the card says: `/api/cases`, `/api/library` and `POST /api/cases {library}` return 404 without `ZLAYT_MODE=local`, library ids cannot traverse, decisions do not leak between cases, and the UI switcher is absent in demo mode and renders case names as text. Two majors: local demo admits unrecorded library texts (spec wording conflict with D-020), and the local list hands every case token to anything that can reach the server.\n\nVerified clean: route gating on both modes (curl, ports 7881 and 7882); traversal id `../../../etc/passwd` returns 404; GET /api/cases shows no `path` or record text; cross-case item access returns 404 both ways; XSS-named case `<img src=x onerror=alert(1)>` renders as literal text with zero `<img>` elements and zero dialogs (screenshot below); CSP header present on both servers; `tools/check_secrets.py` ok over 716 tracked files; no key-shaped strings in 2c2eb1f or 996f9b4; `.env` is untracked and gitignored (`.gitignore:25`).\n\nScreenshots: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-switcher-local.png` (local, switcher visible, XSS name shown as text), `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-switcher-demo.png` (demo, no switcher).\n\nRepro scripts: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-probe.py` (provider gate, route gate, library hash check) and `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-053-security-ui-probe.py` (Playwright).\n\n```json\n{\"card\": \"T-053\", \"persona\": \"security-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commits 2c2eb1f (app/backend/api.py, app/backend/present.py, tests/unit/test_api_routes.py) and 996f9b4 (app/frontend/switcher.js, app/frontend/index.html); HEAD c61e84f; app on 127.0.0.1 (ports 7881 no ZLAYT_MODE, 7882 ZLAYT_MODE=local, plus 7875/7876 probe servers with anthropic-api and a fake key, all stopped); sample case and library case lib01\",\n \"exercised\": [\n  \"python3 tools/board.py show T-053; read personas/security.md and my memory dir\",\n  \"git show 2c2eb1f -- app/backend/api.py app/backend/present.py tests/unit/test_api_routes.py; git show --stat 996f9b4; git log --oneline\",\n  \"git diff --quiet 2c2eb1f HEAD -- app/llm/provider.py app/llm/backends/anthropic_api.py app/main.py (exit 0, unchanged); git ls-files .env (0 lines); git check-ignore -v .env (.gitignore:25)\",\n  \"read app/frontend/switcher.js, app/frontend/dom.js, app/llm/provider.py, app/llm/audited.py, app/llm/backends/anthropic_api.py, app/main.py, memory/DECISIONS.md:163, memory/ORCHESTRATOR_DECISIONS.md D-008/D-020/D-031, spec/REQUIREMENTS.md R-CO-4, memory/contracts/api.md lines 27-28, 43, 441-442\",\n  \".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py::test_case_list_and_library_exist_only_in_local_mode tests/unit/test_api_routes.py::test_cases_do_not_leak_decisions_between_each_other -v -> 2 passed\",\n  \".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py tests/e2e/test_api.py -q -> 31 passed (HEAD c61e84f)\",\n  \"started app.main on 127.0.0.1:7881 (no ZLAYT_MODE) and 127.0.0.1:7882 (ZLAYT_MODE=local) with DATA_DIR in scratchpad; curl GET /api/cases, GET /api/library, POST /api/cases {library}: 404/404/404 on 7881, 200/200/404 on 7882 (unknown id 404); POST {library:'../../../etc/passwd'} on 7882 -> 404 'No such library case.'; both stopped (curl 000 afterwards)\",\n  \"local API probe on 127.0.0.1 (7874): created sample case A and library case B (lib01), ran both to ready; accept A item e1 via A -> 200; same accept via B token -> 404; GET A item via B token -> 404; GET /api/cases counts A accepted 1, B accepted 0\",\n  \"probe servers 7875 (ZLAYT_MODE=local) and 7876 (no ZLAYT_MODE) with LLM_BACKEND=anthropic-api, ANTHROPIC_API_KEY=<redacted> ANTHROPIC_BASE_URL=127.0.0.1:9; /api/health -> demo_mode true, live_enabled false; ran a sample case (7876) and a library case (7875); read llm_calls in their zlayt.sqlite: 66 rows (sample) and 45 rows (library), backend anthropic-api, cases.demo_mode=1; stopped\",\n  \".venv/bin/python -I artifacts/review-evidence/T-053-security-probe.py -> PART1 'ENABLE_LIVE set: False | backend: anthropic-api | provider returned: {x: ok} | SDK messages.create invocations: 1'; PART2 'ZLAYT_MODE=None demo_mode=True GET /api/cases=404 POST library=404' and 'ZLAYT_MODE=local demo_mode=True GET /api/cases=200 POST library=201'; PART3 'library files: 7 | library texts equal to a golden recorded input: 0'\",\n  \"direct anthropic SDK call with installed anthropic 2.3.0: TypeError Messages.create() got an unexpected keyword argument 'temperature'; importlib.metadata anthropic = 2.3.0\",\n  \".venv/bin/python -I artifacts/review-evidence/T-053-security-ui-probe.py (Playwright chromium, servers 7881/7882): local switcher count 1 visible True, library buttons 7, XSS-named case button text 'Open: <img src=x onerror=alert(1)>...', <img> count 0, dialogs [], page errors []; demo switcher count 0, dialogs [], page errors []; screenshots written\",\n  \".venv/bin/python tools/check_secrets.py -> 'check_secrets: ok (716 file(s) scanned)' exit 0\",\n  \"grep of 2c2eb1f and 996f9b4 diffs for sk-ant / sk-proj / ANTHROPIC_API_KEY= <redacted> 0 hits; ls requirements*.txt pyproject.toml Makefile -> none exist\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"public route gating (AC1, checklist 18)\": 5, \"live-call gating in demo mode (checklist 4)\": 1, \"output encoding of case names and library text (checklist 5)\": 5, \"CSP present and unchanged (checklist 6)\": 4, \"decision isolation between cases (AC3 API half)\": 5, \"library loader path safety (no traversal, no path leak)\": 5, \"secrets, logs and capability exposure (checklist 10-12)\": 3, \"dependency pinning (checklist 13)\": 2},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"Demo mode sends live Anthropic SDK calls when LLM_BACKEND=anthropic-api and a key is set, with ENABLE_LIVE unset (pre-existing gate hole; T-053 library route reaches it too)\",\n   \"evidence\": \"app/llm/provider.py:88-90 'if name == \\\"fixture\\\": ... elif name in (\\\"claude-cli\\\", \\\"anthropic-api\\\"):' has no ENABLE_LIVE or demo_mode check. app/llm/backends/anthropic_api.py:20-22 only checks ANTHROPIC_API_KEY, then calls client.messages.create. Repro: artifacts/review-evidence/T-053-security-probe.py PART1 output 'ENABLE_LIVE set: False | backend: anthropic-api | provider returned: {x: ok} | SDK messages.create invocations: 1'. Server repro: /api/health on the probe servers returned demo_mode true, live_enabled false; a sample case run (no ZLAYT_MODE) left 66 llm_calls rows with backend anthropic-api and cases.demo_mode=1; a library case left 45 rows (scratchpad live-demo/zlayt.sqlite and live-local/zlayt.sqlite). Spec: memory/DECISIONS.md:163 'Demo mode uses the fixture backend over recorded responses shipped in the image'; memory/ORCHESTRATOR_DECISIONS.md D-008 'live mode needs an explicit env opt-in'; memory/contracts/api.md:43 'live_enabled is true only when ENABLE_LIVE=1 and a key exist'. The gate lines are unchanged since 2c2eb1f (provider.py, anthropic_api.py, main.py). T-053 widens the reach: api.py:88 admits unrecorded library texts into demo runs (run gate api.py:327). Caveat: the installed anthropic SDK 2.3.0 rejects the 'temperature' kwarg, so in this environment the request fails before the network (rows show BACKEND_FAILED). That is accidental protection, not a gate.\",\n   \"why_it_matters\": \"Any deployment or shell that exports LLM_BACKEND=anthropic-api with a key turns every demo run into paid model calls with no opt-in. There is no per-IP limit and no in-code spend cap (D-020 defers to a provider-side limit), so a public link becomes denial of wallet. This violates D-008 and DECISIONS:163 directly.\",\n   \"fix\": \"In app/llm/provider.py complete_with_meta, refuse claude-cli and anthropic-api unless ENABLE_LIVE=1 and the key (or claude CLI) is present, raising LLMError('BACKEND_UNAVAILABLE live not enabled') before any SDK call. Demo mode must resolve to the fixture backend regardless of LLM_BACKEND. Optionally refuse to start with LLM_BACKEND=anthropic-api unless ENABLE_LIVE=1.\",\n   \"acceptance_test\": \"tests/unit/test_provider.py: set LLM_BACKEND=anthropic-api, ANTHROPIC_API_KEY=<redacted> ENABLE_LIVE unset; monkeypatch app.llm.backends.anthropic_api.make_client to a counting stub; assert P.complete(...) raises and the stub count is 0. tests/unit/test_api_routes.py: same env, POST /api/cases {sample:true} then POST /run, and POST {library:id} then POST /run (ZLAYT_MODE=local); assert stub count 0 and no llm_calls row with backend anthropic-api.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Local demo mode now admits seven unrecorded library texts through the demo gate; this conflicts with D-020/R-CO-4 wording and needs a ruling\",\n   \"evidence\": \"app/backend/api.py:88 'return app.state.recorded | ({digest(x[\\\"path\\\"].read_text()) for x in library_cases()} if local_mode() else set())' feeds the demo gate at api.py:257 and api.py:327. PART2 of T-053-security-probe.py: 'ZLAYT_MODE=local demo_mode=True ... POST library=201' vs 'ZLAYT_MODE=None demo_mode=True ... POST library=404' (public build unaffected). PART3: 'library files: 7 | library texts equal to a golden recorded input: 0'. Spec: spec/REQUIREMENTS.md:138 (R-CO-4) 'In demo mode POST /api/cases accepts only text whose normalized hash equals a recorded fixture; anything else is rejected and not stored'; memory/ORCHESTRATOR_DECISIONS.md:28 (D-020) 'Public build is demo-only ... accepts only text whose normalized hash equals a recorded fixture'. D-031 reinstates the library for local mode. The two decisions read differently for local demo mode, and the card notes say 'In local mode library texts pass the demo gate' without a ruling.\",\n   \"why_it_matters\": \"Non-recorded text now reaches the pipeline in demo mode. Today the default fixture backend replays it (fixture successes in the probe DB), but the same admission is what makes finding 1 reachable with text that was never recorded. The public build is not affected.\",\n   \"fix\": \"Chris rules on whether D-031 amends D-020 for local mode. If yes, amend D-020 in writing and require that library texts run only on recorded fixtures and never on a live backend (finding 1). If no, admit only texts whose hash is in app.state.recorded until T-052 records fixtures for each library text.\",\n   \"acceptance_test\": \"Local demo, unrecorded library text: POST returns 409 unless the amendment is recorded. If admitted, with LLM_BACKEND=anthropic-api and a counting stub, the run makes zero SDK calls and every llm_calls row has backend fixture.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Local-mode case list hands every case token to any caller that can reach the server; the bind address is configurable\",\n   \"evidence\": \"app/backend/api.py:195-203 GET /api/cases returns present.case_list. app/backend/present.py case_list writes '\\\"token\\\": cid' for every case. cid is secrets.token_urlsafe(16) (app/db/db.py:79) and the token is the only capability (get_case(c, token)). app/main.py:14 'host=os.environ.get(\\\"HOST\\\", \\\"127.0.0.1\\\")', so ZLAYT_MODE=local with HOST=0.0.0.0 publishes the list to the LAN. api.py:417 'full=os.environ.get(\\\"ZLAYT_MODE\\\") == \\\"local\\\"' then returns full prompts, responses and edits from the audit route. Verified on 127.0.0.1 only (curl and probe); the LAN bind is code-path evidence, not run.\",\n   \"why_it_matters\": \"Local mode has no authentication. Enumeration turns 128-bit capabilities into a list, and the case data is legal record text. A copy-paste of ZLAYT_MODE=local into a container or Space config would expose all of it.\",\n   \"fix\": \"Refuse to start when ZLAYT_MODE=local and HOST is not 127.0.0.1 or ::1 (or require an explicit ZLAYT_LOCAL_ALLOW_LAN=1 acknowledgement). Keep the list shape unchanged.\",\n   \"acceptance_test\": \"Start with ZLAYT_MODE=local HOST=0.0.0.0: process exits non-zero with a message and no listener. Start with ZLAYT_MODE=local HOST=127.0.0.1: GET /api/cases returns 200.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Live backend cannot be pinned or reproduced: no requirements or lock file, and the installed anthropic SDK rejects the kwarg the backend passes\",\n   \"evidence\": \"importlib.metadata: anthropic 2.3.0. Direct SDK call from the venv: 'TypeError: Messages.create() got an unexpected keyword argument temperature'. app/llm/backends/anthropic_api.py:26 passes temperature=0. 'ls requirements*.txt pyproject.toml Makefile' -> no such files. Dockerfile also absent (checklist 15 not verifiable from this card).\",\n   \"why_it_matters\": \"Checklist 13 (pinned dependencies, pip-audit) cannot be checked, and the live path only fails because of version drift. Whoever fixes finding 1 needs a known SDK version to test against.\",\n   \"fix\": \"Add requirements.txt with == pins for the SDK version the code targets, add pip-audit to a make test target, and add a unit test that inspects the pinned SDK's messages.create signature.\",\n   \"acceptance_test\": \"pip-audit -r requirements.txt exits 0 (or each finding is triaged); a test asserts 'temperature' is in inspect.signature(anthropic.resources.Messages.create).parameters.\"}\n ],\n \"whats_right\": [\n  \"Public and demo routes are gated: GET /api/cases, GET /api/library and POST /api/cases {library} return 404 without ZLAYT_MODE=local, and library ids are matched against the loader's own list (a traversal id returns 404 and no path is returned).\",\n  \"Case names and library text render through text nodes: the XSS-named case showed literal text, zero img elements and zero dialogs (artifacts/review-evidence/T-053-security-switcher-local.png), and the switcher is absent from the DOM in demo mode.\",\n  \"Decisions are isolated per case: accepting an item on case A returns 200, the same item via case B's token returns 404, and per-case counts stay separate (A accepted 1, B accepted 0).\"\n ],\n \"questions_for_chris\": [\n  \"Does D-031 (library loadable in local mode) amend D-020 (demo gate accepts only recorded fixture hashes) for local mode, or should library texts stay recorded-only until T-052 records them?\",\n  \"Is the public Space ever configured with LLM_BACKEND=anthropic-api and ANTHROPIC_API_KEY? That decides how exposed finding 1 is in practice; the code path is open either way.\",\n  \"Should local mode refuse a non-loopback HOST outright (finding 3), or do you want an explicit LAN override?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:20:21.050Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-053-security.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:24.507Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json, re\nt = open(\"/Users/arsis/zlayt-pm-project/reviews/T-053-security.md\").read()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", t, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"keys:\", sorted(d.keys()), \"| verdict:\", d[\"verdict\"], \"| expected by rule:\", exp, \"| severities:\", sev)\nEOF\npython3 tools/board.py validate 2>&1 | grep -i \"T-053\" | head -5; echo \"validate exit=${PIPESTATUS[0]}\"",
 "description": "Parse the review JSON and check the verdict rule and board validation",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T02:20:24.691Z

**tool result**
````
json blocks: 1
keys: ['card', 'exercised', 'findings', 'model', 'persona', 'questions_for_chris', 'scope', 'scores', 'verdict', 'whats_right'] | verdict: fail | expected by rule: fail | severities: ['blocker', 'major', 'major', 'minor']
validate exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:30.295Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/project_demo_live_gate.md",
 "content": "---\nname: demo-live-gate\ndescription: Demo mode does not stop live LLM calls in provider.py (LLM_BACKEND=anthropic-api + key + ENABLE_LIVE unset); check this gate first on any card touching runs, library or case creation\nmetadata:\n  type: project\n---\n\nThe live-call gate is only in the API layer. `app/llm/provider.py` (complete_with_meta, around lines 88-90) sends `claude-cli` and `anthropic-api` straight to the SDK with no ENABLE_LIVE or demo_mode check. `anthropic_api.call` only checks that a key exists. Reproduced at T-053 (HEAD c61e84f): demo_mode true, live_enabled false, and a sample run still produced llm_calls rows with backend anthropic-api. The gate code was unchanged from 2c2eb1f to c61e84f, so it predates T-053.\n\n**Why:** the spec says demo uses the fixture backend (memory/DECISIONS.md:163) and live needs an explicit ENABLE_LIVE opt-in (D-008). Filed as a T-053 blocker. T-053 also widened the demo gate to seven unrecorded library texts (api.py:88, D-020 vs D-031 conflict).\n\n**How to apply:** on any card touching runs, library loading, pasted text, or LLM_BACKEND, re-check provider.py for an ENABLE_LIVE/demo guard before reading the API gate as sufficient. Probe with a stub client (`be.make_client = lambda: Fake()`) and a counting `messages.create`, not a real key. Note the installed anthropic SDK (2.3.0) rejects the `temperature` kwarg, so a live-looking probe can fail before any network call; a stub is the reliable proof.\n\nRelated: [[feedback-round2-review-workflow]]\n"
}
````

### User / tool · 2026-11-02T02:20:30.399Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/project_demo_live_gate.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:34.379Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md",
 "content": "---\nname: round2-review-workflow\ndescription: Workflow gotchas for re-reviews and live-server probes (HEAD moves mid-review, board-guard flags '->' and '>' in command strings, background servers get killed, probe via files under artifacts/review-evidence)\nmetadata:\n  type: feedback\n---\n\nRound-2 re-reviews of a card: pin the commit you actually tested. Other agents commit to the same repo during a review. In T-053, HEAD moved 2c2eb1f -> 864676f -> c61e84f within one session. Run `git rev-parse --short HEAD` in the same call as the pytest run and quote both in the review. Check whether the code you cite changed between the commits (`git diff --quiet <card-commit> HEAD -- <files>`).\n\nThe git-guard PreToolUse hook rejects Bash commands that put `$(...)` substitutions in an `echo` or similar command position (\"unresolved variable or substitution in command position\"). Use one command per git query instead of nesting substitutions.\n\nThe board-guard PreToolUse hook also reads `>` inside quoted strings as a redirect. In T-053 it blocked `curl -w \"GET ... -> %{http_code}\"` and a `-w` format containing `>`. Keep arrows and `>` out of shell strings: write probe scripts with the Write tool into artifacts/review-evidence/ and run them with `.venv/bin/python -I <file>`, or put the probe on stdin with `.venv/bin/python -I - <<'EOF'`.\n\nOther agents on this machine kill or reuse listeners on the ports you pick (my 7873/7874 servers died between calls; 7875/7876 survived). Start servers with `subprocess.Popen` inside one Python probe and stop them in a `finally`, so a kill cannot strand them. Check `lsof -iTCP:<port> -sTCP:LISTEN` before choosing a port. `timeout` is not installed (macOS); run tools without it.\n\n**Why:** T-034 round 2 and T-053 (2026-11-01): the first `$()` echo was blocked, HEAD changed between runs, the `->` hook block cost a turn, and servers vanished between calls.\n**How to apply:** at the start of any probe session, check HEAD, check ports, write the probe as a file under artifacts/review-evidence/, and quote its output in the review.\n"
}
````

### User / tool · 2026-11-02T02:20:34.381Z

**tool result (error)**
````
<tool_use_error>File has been modified since read, either by the user or by a linter. Read it again before attempting to write it.</tool_use_error>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:35.237Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md"
}
````

### User / tool · 2026-11-02T02:20:35.255Z

**tool result**
````
1	---
2	name: round2-review-workflow
3	description: Workflow gotchas for round-2 re-reviews (HEAD moves several times per review, the :7860 server can predate HEAD, working tree is dirty, git-guard blocks $() in echo, probes without scratch files)
4	metadata:
5	  type: feedback
6	---
7	
8	Round-2 re-reviews of a card: pin the commit you actually tested. Other agents commit to the same repo during a review. T-034 r2: HEAD moved b1803c0 -> 250e7b6. T-040 r2 (2026-11-01): HEAD moved 7a450a1 -> 5650eae -> 099732b -> 996f9b4 -> 037cc89 within one review. Run `git rev-parse --short HEAD` in the same call as each pytest run and quote both in the review.
9	
10	The live server on :7860 can predate HEAD. Check `ps -o pid,lstart,command -ax | grep app.main` against `git log -1 --format='%h %ci'` for the commits in question. T-040 r2: pid 72588 started 20:05:05, before the 7a450a1 commit at 20:10:03, and `/api/health` returned 404 there. Probes against :7860 are not evidence for HEAD.
11	
12	The working tree is dirty too (T-040 r2: 245 uncommitted files). Pytest in the working tree is not HEAD evidence, and it can be flaky (test_api_routes gave 2 failed then 23 passed on the same HEAD). To pin, use `git archive <sha> | tar -x -C artifacts/review-evidence/<card>-r2/head_<sha>`, run pytest there with `-p no:cacheprovider`, and start a server from that copy on a spare port (for example 7961 or 7962) with DATA_DIR in artifacts/review-evidence. Kill it with `lsof -ti tcp:<port> | xargs kill`.
13	
14	The git-guard PreToolUse hook rejects Bash commands that put `$(...)` substitutions in an `echo` or similar command position ("unresolved variable or substitution in command position"). Use one command per git query instead of nesting substitutions.
15	
16	Probes can run as `.venv/bin/python - <<'EOF' ... EOF` on stdin, so no scratch file is written. Fault injection works by patching the module attribute and using `fastapi.testclient.TestClient(create())`, run from the archive directory. Large uploads: `python -c "...write('a'*N)" | curl --data-binary @-` gives a clean status and size_upload, while urllib can get a connection reset when the server rejects early.
17	
18	Persona scope: if a brief asks security-reviewer to write a record under another persona's name (e.g. staff-engineer-r2), do not write it. Report the facts and say the other persona's record needs its own run.
19	
20	**Why:** T-034 r2 (first `$()` echo blocked, HEAD changed between pytest and grep). T-040 r2 (four HEAD moves, a live server that predated HEAD, a dirty tree producing a flaky result).
21	**How to apply:** at the start of each round-2 review, record the HEAD sha and the server start time, pin an archive, and quote the sha with each test and probe output.
22	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:38.148Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md",
 "old_string": "Persona scope: if a brief asks security-reviewer",
 "new_string": "T-053 (2026-11-01) added two gotchas. The board-guard PreToolUse hook reads `>` inside quoted strings as a redirect; `curl -w \"GET ... -> %{http_code}\"` was blocked, so keep arrows and `>` out of shell strings and put probes in files under artifacts/review-evidence/ (Write tool, then `.venv/bin/python -I <file>`). Other agents on this machine also kill listeners between calls, so start probe servers with `subprocess.Popen` inside one Python run and stop them in a `finally`. Check `lsof -iTCP:<port> -sTCP:LISTEN` before choosing a port, and do not use `timeout` (not installed on macOS).\n\nPersona scope: if a brief asks security-reviewer"
}
````

### User / tool · 2026-11-02T02:20:38.241Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:38.924Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T02:20:38.939Z

**tool result**
````
1	- [Hook/guard review patterns](project_hook_guard_review_patterns.md) — recurring bypass classes in git-guard/board-guard/check_secrets and reviewer-workflow gotchas
2	- [Round-2 review workflow](feedback_round2_review_workflow.md) — HEAD moves mid-review, git-guard blocks $() in echo, probe via stdin not scratch files
3	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:40.527Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md",
 "old_string": "- [Round-2 review workflow](feedback_round2_review_workflow.md) — HEAD moves mid-review, git-guard blocks $() in echo, probe via stdin not scratch files\n",
 "new_string": "- [Round-2 review workflow](feedback_round2_review_workflow.md) — HEAD moves mid-review, board-guard flags > and -> in strings, servers get killed, probe via files\n- [Demo live-call gate](project_demo_live_gate.md) — provider.py ignores ENABLE_LIVE; demo mode can reach the live SDK; check before trusting the API gate\n"
}
````

### User / tool · 2026-11-02T02:20:40.644Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:42.578Z

T-053 security: fail. Blocker: demo mode reaches the live Anthropic SDK when `LLM_BACKEND=anthropic-api` and a key are set, with `ENABLE_LIVE` unset; majors: local demo admits unrecorded library texts (D-020 wording), and the local case list exposes every case token if `HOST` is non-loopback. Review: /Users/arsis/zlayt-pm-project/reviews/T-053-security.md
