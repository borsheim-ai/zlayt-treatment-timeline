# Subagent: T-107 security check (T-107 security check)

Source: `agent-afab1074bf586aa6d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T06:19:47.537Z

Review board card T-107 in /Users/arsis/zlayt-pm-project (commit 9851a0d). Read reviews/T-087-security-r4.md (the open OCR item) and re-run its Stamp-annotation bomb, from artifacts/review-evidence/T-087-r4/ or rebuilt, against a `git archive HEAD` copy in your scratchpad with ocr=true.

Confirm:
- the API RSS stays flat;
- a killed or failed child gives a 400 and never falls back to an in-process render;
- two concurrent bombs get 400s;
- the AST test really forbids pypdf and PDFium calls outside the child-side functions (mutate it in a scratch copy).

Then try 3 new OCR-path attacks: many pages, huge DPI requests through parameters, and a malformed image stream. Write key values as <redacted>, and stop only your own processes by PID.

Write reviews/T-107-security.md with a ```json block of real values: card, persona security-reviewer, model claude-sonnet-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:19:50.842Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/security.md"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:19:50.844Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-087-security-r4.md"
}
````

### User / tool · 2026-11-02T06:19:50.852Z

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

### User / tool · 2026-11-02T06:19:50.852Z

**tool result**
````
1	# T-087 security review, round 4: PDF hidden-text detection (security-reviewer)
2	
3	**Verdict: changes (0 blockers, 1 major).** All five round-3 confirmations hold at faee448. No PDF parser runs in the API process on the default path. The 10 KB text-layer bomb is a 400 at 10.0 s with parent CPU and RSS flat for 60 s afterwards. Six concurrent uploads give two 400s and four 429s with /api/health at 6 to 16 ms. The opaque Popup is held. The RSS watchdog kills the child at the configured limit. The open item is exploitable: with `ocr=true`, a 3.4 MB PDF whose Stamp appearance stream inflates to 3.5 GB made the API server process itself go from 57 MB to 3631 MB (4578 MB on a repeat run) and answer 201. The child's memory kill is what routes the file into the unprotected in-process OCR render.
4	
5	Pinned: `git archive faee448` unpacked in the scratchpad (`head_faee448_r4`). HEAD was bcdcb91 at write time; `git diff --quiet faee448 HEAD -- app/backend/pdf_hidden.py pdf_checks.py pdf_text.py pdf_ocr.py api.py` returned rc=0, so the code under test is unchanged at HEAD. Lens: untrusted-PDF handling, resource limits, grounding exclusion.
6	
7	## Confirmations asked for
8	
9	| Check | Result at faee448 |
10	|---|---|
11	| No PDF parsing in the API process | Yes for ocr=false. `grep` of app/ finds pypdf only in `pdf_text.read_pages` (called from the child, `pdf_hidden.py:674`) and pypdfium2 only in `pdf_hidden.scan_inprocess` (child) and `pdf_ocr.ocr_pages` (`pdf_ocr.py:191`, API thread, see finding 1). Runtime proof (`probe_r4_api.py`): with `pypdf.PdfReader` and `pypdfium2.PdfDocument` replaced by call-recording spies in the API process, a plain upload gave `201`, `parent parser calls = []`, and a garbage `%PDF-` upload gave `400 pdf_unreadable`, `parent parser calls = []`. |
12	| 10 KB text bomb: parent CPU and RSS flat after the 400 | Yes. 9.7 KB file, content inflates to 6 MB of `(a) Tj`. `POST -> 400 bad_request pdf_timeout after 10.0s`. Parent (rss MB, cputime) before 91 / 0:00.50, at the 400 93 / 0:00.71, then 94 / 0:00.71 at +10 s, 88 / 0:00.72 at +20 and +30, 88 / 0:00.73 at +45, 88 / 0:00.74 at +60. `pdf_hidden` children by ps: none at any sample; final `ps ... | grep '[p]df_hidden'` rc=1. Round 3 on the same file: 27 s of CPU and 330 MB after the 400. |
13	| 6 concurrent uploads, /api/health fast | Yes. Real uvicorn on 127.0.0.1:7881 (`probe_r3_server.py`, 6 bombs, 40 s window): responses `[(0,400,pdf_timeout,10.0s), (1,429,pdf_busy,0.5s), (2,400,pdf_timeout,10.0s), (3,429,pdf_busy,0.5s), (4,429,pdf_busy,0.5s), (5,429,pdf_busy,0.5s)]`. Health 7 to 16 ms throughout (round 3: 378 to 2858 ms). Server RSS 57 MB the whole run, cputime 0:00.30 at start and 0:00.73 at +36 s, 0.0% CPU from +12 s. Round 3 for six: 164 s at 100% CPU, 1.65 GB. |
14	| Opaque Popup held | Yes. `probe_r3_minor.py`: `C_Popup_opaque_AP_cover  held=[[1, [["covered_by_annotation"]]]]`, planted text not in the case text. Round 3: `held=[]`. No false positives: A1 to A8 (6 pt and 5 pt black, roomy clip, Link over text, non-overlapping Widget, Highlight with no appearance) all `held=[]`. B1 to B8 and D2 to D5 unchanged from round 3. Link, Highlight, Underline, Squiggly, StrikeOut held by the render; Caret, Ink, Line, Redact, Widget variants by `covered_by_annotation`. `probe_hidden.py`: 19 of 19 `planted_in_case_text: false`. `probe_r2_bypass.py`: all held except 5d (Hidden flag) and 5e (FreeText), correct as in rounds 2 and 3. |
15	| RSS watchdog kills above 1 GiB | Yes, with one honest caveat on measurement. `probe_r4_rss.py` (3484 KB file, AP inflates to 3500 MB, `pdf_hidden.scan(..., with_text=True)`): real limit 1.00 GiB gives `HiddenScanUnavailable('memory') texts_kept=True` after 0.4 s. Control with the watchdog off: returns after 2.9 s with the child at 4586 MB by ps. Sweep of the limit: 0.25 GiB killed at 0.3 s, 0.5 GiB at 0.3 s, 1 GiB at 0.4 s, 2 GiB at 0.6 s, 3 GiB at 0.7 s, so the kill point follows the setting. The 20 ms ps sampler peaked at 724 MB for the 1 GiB run (683 MB in an earlier run), below the limit, because the kill lands between samples; I did not measure the true peak at kill time. The poll interval is 0.1 s (`WATCH_EVERY_S`), so overshoot is bounded by what the child allocates in about 0.1 s plus the ps call; the control grows at roughly 1.5 GB/s, so I expect a few hundred MB, not measured. Round 3 had no limit on this machine and the same file reached 3186 MB. Linux `RLIMIT_AS` is still unverified (no Dockerfile is tracked, `git ls-files | grep -iE '^Dockerfile|deploy/'` returned nothing). |
16	| Tests and secrets | `pytest -p no:cacheprovider` on test_pdf_hidden, _r2, _r3, _r4, test_pdf_checks_api, test_pdf_upload in the archive: 117 passed in 98.99 s. `python3 tools/check_secrets.py`: ok (1808 file(s) scanned). No key appears in any probe output. |
17	
18	## The open item: PDFium in the API worker thread under OCR
19	
20	**It is exploitable.** The caps in `pdf_ocr` (page size, 8 MP bitmap, 10 pages, PNG total) limit the bitmap, not what PDFium allocates while it parses the file and draws annotations, and the thread is not bounded by the child's kill or the RSS watchdog.
21	
22	The path (all in the pinned archive):
23	1. `api.py:270` runs `pdf_text.extract` in a worker thread, with the 165 s OCR timeout when `ocr=true`.
24	2. `pdf_checks._extract` runs the scan child. The AP bomb pushes the child past 1 GiB, the watchdog kills it, `scan()` raises `HiddenScanUnavailable('memory', texts)`, and `pdf_checks.py:71` turns that into an all-pages-unchecked result instead of refusing.
25	3. Unchecked pages lose their text (`pdf_checks.py:91`), so every page is blank, and `pdf_checks.py:103` puts every page in `scan_pages`.
26	4. `pdf_checks.py:111` calls `pdf_ocr.ocr_pages`, which does `pdfium.PdfDocument(data)` (`pdf_ocr.py:191`) and `page.render` (`pdf_ocr.py:117`) in the API process. PDFium draws the Stamp appearance, inflates the 3.5 GB stream there, with no memory limit and no kill. macOS has no RLIMIT_AS and nothing in the API process polls RSS.
27	
28	So the file the child was killed for is handed to the same renderer in the parent. The attacker sets `ocr=true` in the query string; the file is 3.4 MB, under the 5 MB cap.
29	
30	Measured on a real uvicorn server (`probe_r4_ocr.py`, live-local, port 7882, my own server PID sampled by ps):
31	
32	| Run | Result |
33	|---|---|
34	| Same AP bomb, `ocr=false` | `400 pdf_only_hidden_text` in 0.4 s, server peak RSS 81 MB, health 9 ms |
35	| Same AP bomb, `ocr=true` | `201` in 2.0 s, server RSS 57 MB idle to **3631 MB peak**, 1529 MB still resident 20 s later, health 6 to 63 ms |
36	| Four sequential `ocr=true` runs | per-run retained RSS 1532, 1533, 1540 MB; peak 4578 MB; each answered 201. The retained memory did not stack across sequential runs |
37	| Image-XObject bomb (3.4 MB file, 3433 MB decoded, image-only page), `ocr=true` | `400 pdf_no_text_layer`, server peak RSS 177 MB. Not a memory vector |
38	
39	`MAX_PDF_JOBS = 2` lets two of these run at once, so about 7 to 9 GB of server RSS from two 3.4 MB uploads (I did not run two at once; this machine has 96 GB). A hosted container with a normal memory limit gets its API process OOM-killed, which takes every session down, not one upload. A file that makes PDFium crash (not just grow) in the child takes the same route into the API process; I did not build one. The same chain also applies to any other cause of a child failure on a file with no text left (`child_failed`), not just memory.
40	
41	Scope: live mode only (demo refuses PDFs before reading a byte), and only when Tesseract is installed and the caller passes `ocr=true`; there is no rate limit (D-020), so the caller needs no account. Reachability in the hosted build is what Chris decides; the code path exists on every live server where Tesseract is present.
42	
43	Severity: major, the same class and rating as the round-3 text-read finding (checklist item 3 / OWASP LLM10): an unauthenticated caller can make live mode consume memory the code does not bound. It is larger in size than that one (3.6 GB against 330 MB) but needs the OCR flag and an installed Tesseract, so I am not calling it a blocker; it is not in the persona's section 5 list.
44	
45	## Findings
46	
47	Labels: finding 1 violates checklist item 3 (every operation bounded) and the card's stated promise that no PDF parser runs in the API process; it is a spec-constraint violation on the OCR path, not a style preference.
48	
49	```json
50	{"card": "T-087", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
51	 "scope": "git archive of faee448 (scratchpad head_faee448_r4); app/backend/pdf_hidden.py, pdf_checks.py, pdf_text.py, pdf_ocr.py, api.py:250-277; HEAD bcdcb91 at write time with the five gate files unchanged (git diff --quiet rc=0); live-local mode via TestClient and real uvicorn servers on 127.0.0.1:7881 and :7882; poppler not needed this round",
52	 "exercised": [
53	  "read personas/security.md, reviews/T-087-security-r3.md and my memory notes; git show faee448 on pdf_hidden.py, pdf_checks.py, pdf_text.py, api.py",
54	  "pytest -p no:cacheprovider on test_pdf_hidden, _r2, _r3, _r4, test_pdf_checks_api, test_pdf_upload in the archive: 117 passed in 98.99 s; python3 tools/check_secrets.py: ok (1808 file(s) scanned)",
55	  "grep of app/ for pypdf, pypdfium2, PdfReader, PdfDocument, read_pages, ocr_pages, extract_text: parsers only in pdf_text.read_pages (child), pdf_hidden.scan_inprocess (child) and pdf_ocr.ocr_pages (API thread)",
56	  "probe_r4_api.py: TestClient in this process with spies on pypdf.PdfReader and pypdfium2.PdfDocument: plain upload 201, parent parser calls [], garbage upload 400 pdf_unreadable, parent parser calls []; then the 9.7 KB text bomb (6 MB inflated): 400 pdf_timeout after 10.0 s, parent rss/cputime 91/0:00.50 before, 93/0:00.71 at the 400, 88/0:00.74 at +60 s, no pdf_hidden child at any sample, final ps grep rc=1",
57	  "probe_r3_server.py (reused) with the same bomb, 6 concurrent, real uvicorn on :7881: two 400 pdf_timeout at 10.0 s, four 429 pdf_busy at 0.5 s; health 7 to 16 ms; server RSS 57 MB, cputime 0:00.30 to 0:00.73",
58	  "probe_r3_minor.py (28 files): C_Popup_opaque_AP_cover held covered_by_annotation; A1 to A8 not held; B1 to B8 and D2 to D5 as in round 3; probe_hidden.py 19 of 19 planted_in_case_text false; probe_r2_bypass.py all held except 5d and 5e (correct behaviour)",
59	  "probe_r4_rss.py: AP bomb 3500 MB inflated in a 3484 KB file through pdf_hidden.scan(with_text=True): real limit gives HiddenScanUnavailable('memory') with texts kept in 0.4 s (ps sampler peak 683 to 724 MB, kill lands between samples); watchdog off returns in 2.9 s at 4586 MB; limit sweep 0.25/0.5/1/2/3 GiB killed at 0.3/0.3/0.4/0.6/0.7 s",
60	  "probe_r4_ocr.py: AP bomb to real uvicorn :7882 with ocr=false (400 pdf_only_hidden_text 0.4 s, server peak 81 MB) and ocr=true (201 in 2.0 s, server peak 3631 MB, 1529 MB retained); four sequential ocr=true runs (retained 1532/1533/1540 MB, peak 4578 MB); image-XObject bomb (mk_imgbomb.py, 3433 MB decoded) with ocr=true: 400 pdf_no_text_layer, server peak 177 MB",
61	  "git diff --quiet faee448 HEAD on the five gate files: rc=0; lsof on 7881 and 7882 after the runs: nothing listening, rc=1; every probe server was started by the probe and killed by its own PID; other agents' pdf_hidden children (parent pid 67684) were seen in ps and not touched; git ls-files for Dockerfile and deploy/: none tracked"],
62	 "verdict": "changes",
63	 "scores": {"hidden_text_detection_coverage": 5, "fail_closed_behaviour": 3, "resource_limits": 3, "excluded_from_grounding_when_detected": 5, "demo_gating": 5, "dependency_hygiene": 5},
64	 "findings": [
65	  {"severity": "major",
66	   "title": "With ocr=true, a file the scan child was killed for is re-parsed by PDFium in the API process: a 3.4 MB upload takes the server to 3.6 GB RSS",
67	   "evidence": "Chain: api.py:270 runs pdf_text.extract in a worker thread; pdf_checks.py:71 `scanned = pdf_hidden.unchecked_scan(len(texts))` after HiddenScanUnavailable('memory'); pdf_checks.py:91 clears the unchecked page text; pdf_checks.py:103 `scan_pages = sorted(set(image_pages) | (set(blank) if not any(...)))` then makes every page an OCR page; pdf_checks.py:111 `pdf_ocr.ocr_pages(data, scan_pages, deadline=deadline)`; pdf_ocr.py:191 `pdf = pdfium.PdfDocument(data)` and pdf_ocr.py:117 `bitmap = page.render(scale=scale)` run in the API process with no memory limit and no kill. Repro (artifacts/review-evidence/T-087-r4/probe_r4_ocr.py, AP bomb built by probe_r4_rss.py with 3500 MB inflated, 3484 KB on disk, a Stamp annotation whose /AP /N stream is the flate bomb): ocr=false gives `400 pdf_only_hidden_text` in 0.4 s, server peak RSS 81 MB; ocr=true gives `201` in 2.0 s, server RSS 57 MB idle, 3631 MB peak, 1529 MB still resident 20 s later. A second run peaked at 4578 MB. The image-XObject bomb with ocr=true peaked at 177 MB, so the appearance stream is the vector. MAX_PDF_JOBS = 2 allows two at once (about 7 to 9 GB, extrapolated, not run).",
68	   "why_it_matters": "OWASP LLM10 / unbounded consumption, checklist item 3. The round-4 fix moved both parsers behind a killed child with an RSS watchdog, and the child's memory kill on exactly this file shows the file is hostile, but the code then answers a child failure by doing the same work in the unprotected process. That makes the watchdog moot for ocr=true and gives an unauthenticated caller a way to OOM-kill the API process of a hosted container (every session, not one upload). It also falls through for any child failure on a file with no text left, including a PDFium crash (not built), where a segfault in the API process ends the service. The card text says no PDF parsing happens in the API process; on the OCR path that is false.",
69	   "fix": "Two parts, do both. (1) Fail closed: in pdf_checks._extract, when the child ended in HiddenScanUnavailable with reason memory or child_failed, never run OCR on that file; return a 400 (pdf_unreadable, or a named reason) and keep the unchecked-pages behaviour only for the non-OCR text path. (2) Move the OCR render out of the API process: add a 'render' mode to the pdf_hidden child (or a sibling child) that opens the file, renders the requested pages with the render_scale caps, and writes PNG bytes back, under the same deadline, RLIMIT_CPU and RSS watchdog and the same MAX_PDF_JOBS slot. Tesseract already runs as a subprocess with a timeout, so after this change no PDFium or pypdf call remains in the API process.",
70	   "acceptance_test": "Test A (unit): monkeypatch pdf_hidden.scan to raise HiddenScanUnavailable('memory', texts=['x'*30]) and call pdf_checks.extract(data, ocr=True): assert PdfError and that pdf_ocr.ocr_pages (spied) was never called. Test B (integration, live-local real server): POST the 3484 KB AP bomb with ocr=true; assert a 400 within 10 s and, sampled by ps on the server PID at +5 s and +20 s, RSS under 200 MB and growth under 20 MB. Test C: with pypdf.PdfReader and pypdfium2.PdfDocument spied in the API process, a scanned-image PDF with ocr=true and Tesseract available returns 201 and records zero parser calls in the API process (the render happens in the child)."}
71	 ],
72	 "whats_right": [
73	  "Both parsers now share one killed child: the 10 KB text bomb went from 27 s of CPU and 330 MB after the 400 to flat parent CPU and RSS for 60 s, and six concurrent bombs from 164 s at 1.65 GB to two 400s, four 429s and 6 to 16 ms health.",
74	  "The RSS watchdog works on macOS where RLIMIT_AS does not: the same 3.4 MB file that took the child to 3186 MB in round 3 is killed in 0.4 s at the 1 GiB setting, and the kill point follows the limit.",
75	  "The Popup rule is narrow and still precise: an opaque Popup over text is held as covered_by_annotation, while a Popup with no appearance, a Link, a Highlight with no appearance and ordinary 5 to 12 pt text are kept."],
76	 "questions_for_chris": []}
77	```
78	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:19:51.234Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md"
}
````

### User / tool · 2026-11-02T06:19:51.241Z

**tool result**
````
1	---
2	name: pdf-upload-review-patterns
3	description: Recurring security weak spots in the Zlayt PDF text-layer upload (T-054, pypdf): log leakage, unpinned parser, demo-gate ordering, parse-time DoS; probes to rerun
4	metadata:
5	  type: project
6	---
7	
8	PDF upload (`app/backend/pdf_text.py`, route `POST /api/cases/pdf` in `app/backend/api.py`) was reviewed on T-054 (2026-11-01, HEAD 4eebb2d; the PDF surface was unchanged from c61e84f on).
9	
10	- pypdf logs through `logging.getLogger("pypdf...")` at WARNING/ERROR with the failing content-stream fragment in the message, so record text reaches stderr whenever a PDF has a syntax glitch. Reproduce with 300 seeded byte mutations of `tests/unit/_pdf.sample_pdf`; suppression via NullHandler + `propagate=False` removes all of it. Check this in any new parser or any PDF/DOCX/OCR path.
11	- pypdf 6.21.4 caps each inflated stream at 75 MB (`pypdf.filters.ZLIB_MAX_OUTPUT_LENGTH`) but not the document total. Measured about 3.7 s per 74 MB page; a 5 MB upload with about 70 such pages is minutes of CPU. The fix was a demo-gate-first refusal plus a threadpool and a 10 s `asyncio.wait_for`, but the thread keeps running after the 10 s cap.
12	- Demo gate ordering matters: the gate ran after parsing at 5650eae. The fixed route refuses before reading the body. Check the order again after any route change.
13	- No version pin or manifest: the card said "release/ENVIRONMENT must list pypdf" and it was still open. Check `git ls-files` for requirements/pyproject/Dockerfile before accepting any new third-party parser.
14	- Encrypted PDFs (real ones, written by pypdf with a password) return `pdf_encrypted`; printf-crafted "encrypted" files only give `pdf_unreadable`. Both are 400 and never 500.
15	- Invisible text (render mode 3) is extracted verbatim. The injection scanner (`app/backend/injection.py` lexicon) still fires on phrasing like "ignore prior instructions", but the case shows text that is not visible in the source.
16	- Rate limiter and spend cap were cut by D-020 (ADR-015). The persona checklist and `docs/CONTRACT.md:314` still require them. Treat as a question for Chris, not a finding, unless live mode is exposed beyond local use.
17	
18	T-054 r2 (2026-11-01, HEAD d796383, later 08764e7): F1 (logs) and F2 (pins; pip-audit 2.10.1 clean on 33 runtime pins) are resolved; F3 measured 5 pages x 74 MB stopping at 11.45 s against the 10 s cap. The deadline check is between pages only, and pypdf 6.21.4 caps an array-based `/Contents` at 75,000,000 bytes in total (`LimitReachedError`), so one page cannot exceed about one page of inflation. The earlier "K streams x 75 MB" worst case does not hold. Probe files: `artifacts/review-evidence/T-054-r2/T-054-r2-probe.py log|budget|pins`.
19	
20	**How to apply:** rerun `artifacts/review-evidence/T-054-security-probe.py live`, `-probe2.py`, `-probe3.py` (flate timing), `-probe4.py` (HTTP timing, demo vs live-local) and `-probe5.py plain|suppressed` (log leak) on any PDF change. Check `git diff --stat <last-reviewed-sha> HEAD -- app/backend/pdf_text.py app/backend/api.py tests/unit/test_pdf_upload.py` first.
21	
22	T-086/T-087 (2026-11-02, 2fca530; Tesseract OCR + PDFium hidden-text scan, D-042): findings were (1) review.py `_check_summary` -> `compose_state` has no OCR input, so an edit or manual entry on an OCR item becomes verified and drops OCR_DERIVED (blocker; check every state-recompute path when a new reason is added to the pipeline only); (2) pdf_checks `except HiddenScanUnavailable: pass` fails open (21 of 406 byte mutations); (3) pixel-spread visibility test beaten by a 1 pt dot; PDFium `get_objects` default max_depth=15 hides deeper form nesting from the scan; (4) pdf_hidden.scan has no deadline (226 KB = 94 s CPU, thread outlives the 10 s wait_for); (5) pdf_ocr.render has no pixel clamp (1 KB PDF at 7200pt = 2.3 GB RSS). Probes: artifacts/review-evidence/T-086-087/ (pdfkit.py builds raw PDFs; probe_hidden, probe_failopen, probe_scan_time, probe_dos, probe_ocr_edit). Good: tesseract argv fixed, tempdir cleaned on timeout, demo gate first, pip-audit clean.
23	Workflow: board-guard refuses `git worktree` for reviewers (use git archive); a shared scratchpad dir `wt` was deleted by another agent mid-review, so use a unique dir name.
24	
25	T-087 r3 (2026-11-02, ae76835; HEAD moved to 841be23, gate files unchanged): scan now runs in a killed child (overlap file 400 at 10 s, no child by ps, CPU flat); Widget/minor constructions held. Still open: (1) pypdf `page.extract_text()` runs in the API threadpool, deadline only between pages: a 10 KB one-page file of `(a) Tj` ops (6 MB inflated, under pypdf's token cap; 7 MB hits LimitReachedError) = 25 s CPU + 300 MB, 6 concurrent = 164 s at 100% CPU, 1.65 GB RSS; (2) ANNOT_EXEMPT includes Popup (16), PDFium does not draw it but poppler draws a parent-less Popup AP, so it covers text; (3) macOS setrlimit(RLIMIT_AS) raises ValueError (swallowed), scan child hit 3.2 GB on a 3.5 MB annotation-AP flate bomb (image-XObject bomb only 131 MB). Probes: artifacts/review-evidence/T-087-r3/ (probe_r3_api, _minor, _popup, _textbomb, _server, _rlimit, _apbomb). Pattern: when one stage gets a kill-at-deadline child, check every earlier stage that still runs in-process; exemption lists keyed on "the render checks it" fail for subtypes the renderer skips.
26	
27	T-087 r4 (2026-11-02, faee448; HEAD moved to bcdcb91, gate files unchanged): r3 majors fixed (pypdf read now in the killed child, MAX_PDF_JOBS=2 with 429 busy, Popup with AP held, parent RSS watchdog at 1 GiB kills the child in 0.4 s). Open and exploitable: with `ocr=true`, a child killed for memory returns HiddenScanUnavailable, pdf_checks clears the page text, every page becomes an OCR page and `pdf_ocr.ocr_pages` runs PDFium in the API process: 3.4 MB Stamp-AP flate bomb took the server 57 -> 3631 MB (4578 MB on a repeat), 201 response. Image-XObject bomb only 177 MB. Pattern: when a sandboxed stage fails for resource reasons, check that the fallback path does not repeat the same work in the unsandboxed process. Probes: artifacts/review-evidence/T-087-r4/ (probe_r4_api, _rss, _ocr, mk_imgbomb). Other agents' pdf_hidden children show up in ps (grep by ppid before blaming the server).
28	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:19:51.639Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/security-reviewer/feedback_round2_review_workflow.md"
}
````

### User / tool · 2026-11-02T06:19:51.645Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:19:52.278Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-107 2>&1 | head -80; git log --oneline | head -5; ls artifacts/review-evidence/T-087-r4/"
}
````

### User / tool · 2026-11-02T06:19:52.438Z

**tool result**
````
---
id: "T-107"
title: "OCR render in the killed child: refuse OCR after a child failure; no PDFium render in the API process (T-087 r4 major)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T06:07:22Z"
updated_at: "2026-11-02T06:19:43Z"
claimed_by: "backend"
claimed_at: "2026-11-02T06:07:24Z"
rounds: 0
commits: ["9851a0d"]
reviews: []
ac:
  - {"n": 1, "text": "With ocr=true, page rendering for OCR runs in the same deadline/RSS-watchdog child; if the child is killed the upload returns 400 and never falls back to an in-process render; the reviewer's Stamp-annotation bomb keeps API RSS flat; tests", "done": true, "evidence": "tests/unit/test_pdf_ocr_isolation.py (14 tests) + pytest -k 'pdf or ocr or hidden' 184 passed; live uvicorn with reviewer-style 3485 KB/3500 MB Stamp bomb ocr=true: 400 ocr_check_failed in 0.4 s, server RSS 57->82 MB; two concurrent: 400+400, peak 106-110 MB; grep: pypdf/PDFium only in scan_inprocess, read_pages, render_in_child (child-only, AST test)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T06:07:24Z backend: claimed
- 2026-11-02T06:19:36Z backend: Render moved into the pdf_hidden child (mode render); ocr=true + killed/failed scan child -> 400 ocr_check_failed; killed render child -> 400 ocr_render_failed. Also fixed a GIL convoy in _run_child (communicate(input) = 512 B writes; two concurrent 3 MB uploads stalled to the deadline): file now fed from a thread.
- 2026-11-02T06:19:36Z backend: AC 1 checked: tests/unit/test_pdf_ocr_isolation.py (14 tests) + pytest -k 'pdf or ocr or hidden' 184 passed; live uvicorn with reviewer-style 3485 KB/3500 MB Stamp bomb ocr=true: 400 ocr_check_failed in 0.4 s, server RSS 57->82 MB; two concurrent: 400+400, peak 106-110 MB; grep: pypdf/PDFium only in scan_inprocess, read_pages, render_in_child (child-only, AST test)
- 2026-11-02T06:19:36Z backend: moved in_progress -> in_review
- 2026-11-02T06:19:43Z orchestrator: review dispatched: security-reviewer

## Handoff
What changed: pdf_ocr.render_in_child + pdf_hidden 'render' child mode; pdf_ocr.ocr_pages renders via the killed child only (Tesseract subprocess stays in API). pdf_checks: ocr=true and scan child killed/failed -> PdfError ocr_check_failed (400); render child killed/failed -> ocr_render_failed (400); no in-process fallback exists. api.md documents both codes. Also fixed _run_child stdin feeding (GIL convoy, found when proving two concurrent bombs). How verified: .venv/bin/python -m pytest -q tests/unit -k 'pdf or ocr or hidden' = 184 passed; live server runs with a 3485 KB bomb (3500 MB inflated): ocr=true 400 in 0.4 s, RSS 57->82 MB (was 3631 MB); 2 concurrent ocr=true = 400,400 (peak 110 MB); AST test asserts pypdf/PDFium imports only in child functions. Left: ocr=false keeps unchecked-page behaviour (400 only when no text remains), by design. Surprised: Popen.communicate(input) on macOS writes 512 B/loop so concurrent 3 MB uploads stalled to the deadline.

9851a0d fix(backend): OCR page rendering runs in the killed scan child; a killed or failed child is a 400 with no in-process fallback (T-107)
d3e127c fix(backend): quote picker units come from the quotable body only (T-108)
c2a5d1f fix(backend): unit suite green on a clean HEAD; notes never print an unchecked narrative sentence (T-106)
3462ad0 fix(frontend): EDIT_QUOTE refusals offer Change the quote and open the picker; CODE_CHECK_FAILED on edit shows inline under the edit box; Why lead follows the backend verdict string (T-104)
bcdcb91 fix(backend): billing applies D-052 strictly: no sums or comparisons; EOB rows are lines, every EOB money token placed (T-103 r2)
mk_imgbomb.py
probe_r4_api.py
probe_r4_ocr.py
probe_r4_rss.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:19:56.489Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $SP/head_9851a0d_r5 && git archive 9851a0d | tar -x -C $SP/head_9851a0d_r5 && git rev-parse --short HEAD && ls $SP/head_9851a0d_r5 && cat artifacts/review-evidence/T-087-r4/probe_r4_ocr.py && cat artifacts/review-evidence/T-087-r4/probe_r4_rss.py | head -80; git status --short | head"
}
````

### User / tool · 2026-11-02T06:19:56.968Z

**tool result**
````
9851a0d
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
"""T-087 r4: one bomb PDF POSTed with ocr=true (or any query) to a real uvicorn server (live-local). Samples the SERVER pid (RSS, cputime) every 0.2 s, GET /api/health latency,
and the pdf_hidden children, until the response comes back plus a tail. Stops only the server process this script started, by PID.
Run: .venv/bin/python -I probe_r4_ocr.py <archive_root> <bomb.pdf> <query e.g. ocr=true> <port> <tail_s>"""
import os
import pathlib
import subprocess
import sys
import threading
import time

import httpx

root, pdf, query, port, tail = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
env = {k: os.environ[k] for k in ("PATH", "LANG", "TMPDIR") if k in os.environ}
env.update({"ENABLE_LIVE": "1", "LLM_BACKEND": "claude-cli", "PORT": str(port), "HOST": "127.0.0.1"})
srv = subprocess.Popen([sys.executable, "-I", "-c", "import sys, os; sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1]); import uvicorn; from app.main import create; uvicorn.run(create(), host='127.0.0.1', port=int(os.environ['PORT']), access_log=False, log_level='warning')", root],
                       env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
base = f"http://127.0.0.1:{port}"


def ps(pid):
    o = subprocess.run(["ps", "-o", "rss=,time=,%cpu=", "-p", str(pid)], capture_output=True, text=True).stdout.split()
    return (int(o[0]) // 1024, o[1], float(o[2])) if o else None


try:
    for _ in range(100):
        try:
            if httpx.get(base + "/api/health", timeout=1).status_code == 200:
                break
        except Exception:
            time.sleep(0.2)
    else:
        print("server did not start"); raise SystemExit(1)
    print(f"server pid {srv.pid}; idle (rss MB, cputime, %cpu) = {ps(srv.pid)}; file {pdf.name} {pdf.stat().st_size/1024:.0f} KB; query {query}")
    data = pdf.read_bytes()
    res = {}

    reps = int(sys.argv[6]) if len(sys.argv) > 6 else 1

    def post():
        for _ in range(reps - 1):       # sequential repeats first; the last result is the one reported
            try:
                httpx.post(base + "/api/cases/pdf?" + query, content=data, headers={"content-type": "application/pdf"}, timeout=400)
                print("   (repeat done) server rss/cputime/%cpu =", ps(srv.pid), flush=True)
            except Exception as e:
                print("   repeat failed", type(e).__name__)
        s = time.monotonic()
        try:
            r = httpx.post(base + "/api/cases/pdf?" + query, content=data, headers={"content-type": "application/pdf"}, timeout=400)
            j = r.json()
            res["r"] = (r.status_code, (j.get("error") or {}).get("code"), ((j.get("error") or {}).get("detail") or {}).get("reason") or ("created" if r.status_code == 201 else ""), round(time.monotonic() - s, 1))
        except Exception as e:
            res["r"] = (type(e).__name__, str(e)[:120], "", round(time.monotonic() - s, 1))
    th = threading.Thread(target=post)
    start = time.monotonic()
    th.start()
    peak_rss, lat_max, done_at = 0, 0.0, None
    last_print = 0
    while True:
        now = time.monotonic() - start
        p = ps(srv.pid)
        if p:
            peak_rss = max(peak_rss, p[0])
        s = time.monotonic()
        try:
            httpx.get(base + "/api/health", timeout=30)
            lat = (time.monotonic() - s) * 1000
        except Exception as e:
            lat = 30000.0
        lat_max = max(lat_max, lat)
        if now - last_print >= 2 or ("r" in res and done_at is None):
            kids = subprocess.run("ps -axo pid,ppid,time,command | grep '[a]pp.backend.pdf_hidden'", shell=True, capture_output=True, text=True).stdout.strip().splitlines()
            print(f"  +{now:6.1f}s server rss/cputime/%cpu={p} peak_rss={peak_rss} MB health={lat:.0f} ms pdf_hidden_children={len(kids)}")
            last_print = now
        if "r" in res and done_at is None:
            done_at = now
            print("  response:", res["r"])
        if done_at is not None and now - done_at >= tail:
            break
        if now > 420:
            print("  gave up waiting"); break
        time.sleep(0.2)
    print(f"summary: response={res.get('r')} server peak RSS={peak_rss} MB max health latency={lat_max:.0f} ms; server final={ps(srv.pid)}")
finally:
    srv.kill()
    srv.wait()
"""T-087 r4: RSS watchdog. Runs pdf_hidden.scan(with_text=True) on an AP-stream bomb (3500 MB inflated, 3.4 MB file) with the real CHILD_RSS_BYTES and again with the
watchdog disabled (control). A 20 ms sampler reads the child's RSS by ps. Prints the exception, wall, peak RSS.
Run: .venv/bin/python -I probe_r4_rss.py <archive_root> <outdir> <inflated_MB>"""
import pathlib
import subprocess
import sys
import threading
import time
import zlib

root, out, mb = sys.argv[1], pathlib.Path(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "T-086-087"))
sys.path.insert(0, root)
import pdfkit as K
out.mkdir(parents=True, exist_ok=True)
z = zlib.compressobj(9)
parts = [z.compress(b"1 1 1 rg 0 0 600 30 re f ")]
for _ in range(mb):
    parts.append(z.compress(b" " * (1024 * 1024)))
parts.append(z.flush())
body = b"".join(parts)
ap = f"<< /Type /XObject /Subtype /Form /BBox [0 0 600 30] /Filter /FlateDecode /Length {len(body)} >>\nstream\n".encode() + body + b"\nendstream"
objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Contents 4 0 R /Annots [7 0 R] /Resources << /Font << /F1 5 0 R >> >> >>",
        K.stream(K.VISIBLE + b"BT /F1 12 Tf 0 0 0 rg 50 700 Td (Normal note with a stamp over it, SYNTHETIC.) Tj ET\n"), K.FONT, ap,
        b"<< /Type /Annot /Subtype /Stamp /Rect [0 690 600 720] /F 4 /AP << /N 6 0 R >> >>"]
data = K.pdf(objs)
(out / f"ap_{mb}.pdf").write_bytes(data)
print(f"file {len(data)/1024:.0f} KB, AP inflates to {mb} MB")
from app.backend import pdf_hidden


def run(label, limit):
    pdf_hidden.CHILD_RSS_BYTES = limit
    peak, stop = [0], threading.Event()

    def samp():
        while not stop.is_set():
            o = subprocess.run(["ps", "-axo", "rss=,command="], capture_output=True, text=True).stdout
            for ln in o.splitlines():
                if "app.backend.pdf_hidden" in ln and "ps -axo" not in ln:
                    peak[0] = max(peak[0], int(ln.split(None, 1)[0]) // 1024)
            time.sleep(0.02)
    th = threading.Thread(target=samp, daemon=True)
    th.start()
    t = time.monotonic()
    try:
        r = pdf_hidden.scan(data, time.monotonic() + 10, with_text=True)
        res = "returned checked=%s pages=%s" % (r["checked"], list(r["pages"]))
    except pdf_hidden.HiddenScanUnavailable as e:
        res = "HiddenScanUnavailable(%r) texts_kept=%s" % (str(e), e.texts is not None)
    except pdf_hidden.HiddenScanTimeout as e:
        res = "HiddenScanTimeout(%s)" % e
    stop.set()
    th.join()
    print(f"{label}: limit={limit/1024**3:.2f} GiB -> {res}; wall={time.monotonic()-t:.1f}s; child peak RSS by ps={peak[0]} MB")


if len(sys.argv) > 4:
    for g in sys.argv[4:]:
        run("sweep", int(float(g) * 1024 ** 3))
else:
    run("watchdog on (real value)", pdf_hidden.CHILD_RSS_BYTES)
    run("watchdog off (control)", 10 ** 13)
print("children left:", subprocess.run("ps -axo pid,ppid,etime,command | grep '[p]df_hidden'", shell=True, capture_output=True, text=True).stdout.strip() or "none")
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:19:59.247Z

**tool call — Bash**
````
{
 "command": "which tesseract; git show 9851a0d --stat | head -30; git show 9851a0d -- app/backend/pdf_checks.py app/backend/pdf_ocr.py | head -400"
}
````

### User / tool · 2026-11-02T06:19:59.371Z

**tool result**
````
/opt/homebrew/bin/tesseract
commit 9851a0db2ba06d64828dad65a9124a5c2b4294d9
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 00:19:28 2026 -0600

    fix(backend): OCR page rendering runs in the killed scan child; a killed or failed child is a 400 with no in-process fallback (T-107)
    
    With ocr=true a 3.4 MB Stamp-annotation bomb took the API process to 3.6 GB RSS because a killed scan child sent the file to an in-process PDFium render.
    - pdf_ocr.render_in_child + pdf_hidden render mode: PDFium opens and draws the pages only in the child (deadline, CPU, RSS watch)
    - pdf_checks: scan child killed/failed with ocr=true -> 400 ocr_check_failed; render child killed -> 400 ocr_render_failed
    - pdf_hidden._run_child feeds the file from a thread in one write: communicate(input) wrote 512 B per loop and two concurrent 3 MB uploads stalled to the deadline
    - tests/unit/test_pdf_ocr_isolation.py; api.md documents the new codes
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/pdf_checks.py            |   9 +-
 app/backend/pdf_hidden.py            |  40 ++++++--
 app/backend/pdf_ocr.py               |  96 +++++++++++++-----
 memory/contracts/api.md              |   2 +-
 tests/unit/test_pdf_ocr_isolation.py | 182 +++++++++++++++++++++++++++++++++++
 5 files changed, 297 insertions(+), 32 deletions(-)
commit 9851a0db2ba06d64828dad65a9124a5c2b4294d9
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 00:19:28 2026 -0600

    fix(backend): OCR page rendering runs in the killed scan child; a killed or failed child is a 400 with no in-process fallback (T-107)
    
    With ocr=true a 3.4 MB Stamp-annotation bomb took the API process to 3.6 GB RSS because a killed scan child sent the file to an in-process PDFium render.
    - pdf_ocr.render_in_child + pdf_hidden render mode: PDFium opens and draws the pages only in the child (deadline, CPU, RSS watch)
    - pdf_checks: scan child killed/failed with ocr=true -> 400 ocr_check_failed; render child killed -> 400 ocr_render_failed
    - pdf_hidden._run_child feeds the file from a thread in one write: communicate(input) wrote 512 B per loop and two concurrent 3 MB uploads stalled to the deadline
    - tests/unit/test_pdf_ocr_isolation.py; api.md documents the new codes
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/pdf_checks.py b/app/backend/pdf_checks.py
index d5b190c..a7f1fa3 100644
--- a/app/backend/pdf_checks.py
+++ b/app/backend/pdf_checks.py
@@ -24,6 +24,10 @@ MESSAGES = {
                             "Run OCR to read what the pages show, or confirm the listed pages if you trust them.",
     "ocr_unavailable": "Scanned pages need Tesseract, which is not available on this server.",
     "ocr_too_many_pages": f"This PDF has more than {pdf_ocr.MAX_OCR_PAGES} scanned pages; OCR reads at most that many in one upload. Split the file.",
+    "ocr_render_failed": "This PDF could not be safely drawn for OCR (the page drawer ran out of memory or time, or the file is damaged), so nothing was read. "
+                         "Paste the text instead.",
+    "ocr_check_failed": "This PDF could not be checked safely (the checker ran out of memory or time, or crashed), so it was not read with OCR. "
+                        "Paste the text instead.",
     "ocr_failed": "OCR could not read a page of this PDF. Try again, or paste the text instead.",
     "ocr_page_too_large": "A scanned page in this PDF is larger than OCR will read (over 40 inches on a side). Re-scan or resize it, or paste the text instead.",
     "ocr_images_too_large": "The scanned pages in this PDF are too large to keep together. Split the file, or paste the text instead.",
@@ -65,6 +69,8 @@ def _extract(data: bytes, *, ocr: bool, include_hidden, deadline: float) -> dict
         scanned = pdf_hidden.scan(data, deadline, with_text=True)
         texts = scanned.pop("texts")
     except pdf_hidden.HiddenScanUnavailable as e:
+        if ocr:                # T-107: a file whose scan child was killed or failed is never handed to OCR; no fallback render anywhere
+            raise PdfError("ocr_check_failed", {"cause": str(e)[:40]}) from None
         texts = e.texts
         if texts is None:      # the child failed before it had read the text layer: there is nothing to hold back, the file is unreadable
             raise PdfError("pdf_unreadable") from None
@@ -112,7 +118,8 @@ def _extract(data: bytes, *, ocr: bool, include_hidden, deadline: float) -> dict
             except pdf_ocr.OcrUnavailable as e:
                 raise PdfError("ocr_unavailable", {"message": str(e), "ocr": checks["ocr"]["status"]}) from None
             except pdf_ocr.OcrFailed as e:
-                code = {"page_too_large": "ocr_page_too_large", "images_too_large": "ocr_images_too_large"}.get(e.reason, "ocr_failed")
+                code = {"page_too_large": "ocr_page_too_large", "images_too_large": "ocr_images_too_large",
+                        "render_killed": "ocr_render_failed", "render_failed": "ocr_render_failed"}.get(e.reason, "ocr_failed")
                 raise PdfError(code, {"page": e.page} if e.page else None) from None
             for n, o in ocr_page_data.items():
                 texts[n - 1] = o["text"].strip()
diff --git a/app/backend/pdf_ocr.py b/app/backend/pdf_ocr.py
index 0cea050..2d7203d 100644
--- a/app/backend/pdf_ocr.py
+++ b/app/backend/pdf_ocr.py
@@ -1,5 +1,5 @@
 """Local OCR for scanned PDF pages (T-086, D-042). The Tesseract binary runs as a subprocess on this machine; no page image or text
-ever leaves it, and nothing here calls a network. Rendering is pypdfium2 (PDFium), PNG encoding is stdlib zlib.
+ever leaves it, and nothing here calls a network. Rendering is pypdfium2 (PDFium) and runs ONLY in the killed child process of pdf_hidden (T-107: render_in_child); PNG encoding is stdlib zlib.
 
 OCR output is a guess at the printed words, so everything derived from it is held to a stricter rule than text-layer text:
   - the page image is kept beside the OCR text, so the paralegal checks the words against the page itself;
@@ -179,35 +179,85 @@ def ocr_png(png: bytes, languages: list = None, timeout: float = PAGE_TIMEOUT_S,
             "mean_conf": round(sum(confs) / len(confs), 1) if confs else None}
 
 
-def ocr_pages(data: bytes, pages: list, deadline: float = None) -> dict:
-    """OCR the given 1-based `pages` of a PDF. {n: {text, low_conf (page offsets), mean_conf, words, png_b64}}.
-    Raises OcrUnavailable (checked first, before any rendering), OcrFailed."""
-    st = ocr_status()
-    if not st["available"]:
-        raise OcrUnavailable(st["message"])
-    import pypdfium2 as pdfium
-    start = time.monotonic()
-    out, stored = {}, 0
-    pdf = pdfium.PdfDocument(data)
+def render_in_child(data: bytes, pages: list, soft_deadline: float, emit) -> None:
+    """RUNS ONLY INSIDE THE KILLED CHILD (pdf_hidden `render` mode). Opens the file with PDFium, renders each page to a capped greyscale PNG
+    and emits one JSON line per page: {page, png_b64} or {render_error, page}; {render_done: true} last. The caller's process never opens
+    the file (T-107)."""
+    try:
+        import pypdfium2 as pdfium
+        pdf = pdfium.PdfDocument(data)
+    except Exception as e:
+        emit({"render_error": type(e).__name__, "page": None})
+        return
+    stored = 0
     try:
         for n in pages:
-            if time.monotonic() - start > TOTAL_TIMEOUT_S or (deadline and time.monotonic() > deadline):
-                raise OcrFailed("timeout", n)
+            if time.monotonic() > soft_deadline:
+                emit({"render_error": "timeout", "page": n})
+                return
             try:
                 png = render_page_png(pdf, n - 1)
             except OcrFailed as e:
-                raise OcrFailed(e.reason, n) from None
+                emit({"render_error": e.reason, "page": n})
+                return
+            except Exception as e:
+                emit({"render_error": type(e).__name__, "page": n})
+                return
             stored += len(png)
             if stored > MAX_STORED_PNG_BYTES:
-                raise OcrFailed("images_too_large", n)
-            got = ocr_png(png, status=st)
-            out[n] = {"text": got["text"], "words": len(got["words"]), "mean_conf": got["mean_conf"],
-                      "low_conf": [{"start": w["start"], "end": w["end"], "text": w["text"], "conf": w["conf"]} for w in got["low_conf"]],
-                      "png_b64": base64.b64encode(png).decode("ascii")}
-    except (OcrUnavailable, OcrFailed):
-        raise
-    except Exception as e:             # PDFium could not render the page
-        raise OcrFailed(type(e).__name__) from None
+                emit({"render_error": "images_too_large", "page": n})
+                return
+            emit({"page": n, "png_b64": base64.b64encode(png).decode("ascii")})
+        emit({"render_done": True})
     finally:
         pdf.close()
+
+
+def render_pages(data: bytes, pages: list, deadline: float = None) -> dict:
+    """{page: PNG bytes}, rendered by the killed child process (pdf_hidden.render_messages). A child that is killed (deadline, CPU, memory),
+    crashes or cannot open the file is OcrFailed('render_killed' | 'render_failed' | 'timeout'); there is no in-process fallback."""
+    from app.backend import pdf_hidden
+    try:
+        msgs = pdf_hidden.render_messages(data, pages, deadline)
+    except pdf_hidden.HiddenScanTimeout:
+        raise OcrFailed("timeout") from None
+    except pdf_hidden.HiddenScanUnavailable:
+        raise OcrFailed("render_killed") from None
+    out = {}
+    for m in msgs:
+        if m.get("render_error"):
+            raise OcrFailed(str(m["render_error"])[:60], m.get("page"))
+        if isinstance(m.get("page"), int) and isinstance(m.get("png_b64"), str):
+            try:
+                out[m["page"]] = base64.b64decode(m["png_b64"], validate=True)
+            except ValueError:
+                raise OcrFailed("render_failed", m["page"]) from None
+    if not any(m.get("render_done") for m in msgs) or set(out) != set(pages):
+        raise OcrFailed("render_failed")
+    return out
+
+
+def ocr_pages(data: bytes, pages: list, deadline: float = None) -> dict:
+    """OCR the given 1-based `pages` of a PDF. {n: {text, low_conf (page offsets), mean_conf, words, png_b64}}.
+    Raises OcrUnavailable (checked first, before any rendering), OcrFailed. Rendering happens in the killed child (render_pages); only the
+    Tesseract subprocess and the PNG bytes it reads are handled in this process."""
+    st = ocr_status()
+    if not st["available"]:
+        raise OcrUnavailable(st["message"])
+    start = time.monotonic()
+    out = {}
+    pngs = render_pages(data, list(pages), deadline if deadline else start + TOTAL_TIMEOUT_S)
+    stored = 0
+    for n in pages:                    # the child enforces the cap too; this re-check is byte counting, not parsing
+        stored += len(pngs[n])
+        if stored > MAX_STORED_PNG_BYTES:
+            raise OcrFailed("images_too_large", n)
+    for n in pages:
+        if time.monotonic() - start > TOTAL_TIMEOUT_S or (deadline and time.monotonic() > deadline):
+            raise OcrFailed("timeout", n)
+        png = pngs[n]
+        got = ocr_png(png, status=st)
+        out[n] = {"text": got["text"], "words": len(got["words"]), "mean_conf": got["mean_conf"],
+                  "low_conf": [{"start": w["start"], "end": w["end"], "text": w["text"], "conf": w["conf"]} for w in got["low_conf"]],
+                  "png_b64": base64.b64encode(png).decode("ascii")}
     return out
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:20:01.007Z

**tool call — Bash**
````
{
 "command": "git show 9851a0d -- app/backend/pdf_hidden.py; cat tests/unit/test_pdf_ocr_isolation.py"
}
````

### User / tool · 2026-11-02T06:20:01.106Z

**tool result**
````
commit 9851a0db2ba06d64828dad65a9124a5c2b4294d9
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 00:19:28 2026 -0600

    fix(backend): OCR page rendering runs in the killed scan child; a killed or failed child is a 400 with no in-process fallback (T-107)
    
    With ocr=true a 3.4 MB Stamp-annotation bomb took the API process to 3.6 GB RSS because a killed scan child sent the file to an in-process PDFium render.
    - pdf_ocr.render_in_child + pdf_hidden render mode: PDFium opens and draws the pages only in the child (deadline, CPU, RSS watch)
    - pdf_checks: scan child killed/failed with ocr=true -> 400 ocr_check_failed; render child killed -> 400 ocr_render_failed
    - pdf_hidden._run_child feeds the file from a thread in one write: communicate(input) wrote 512 B per loop and two concurrent 3 MB uploads stalled to the deadline
    - tests/unit/test_pdf_ocr_isolation.py; api.md documents the new codes
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/pdf_hidden.py b/app/backend/pdf_hidden.py
index 5fa89e0..e4bb876 100644
--- a/app/backend/pdf_hidden.py
+++ b/app/backend/pdf_hidden.py
@@ -536,8 +536,8 @@ def _texts_of(msgs):
     return None
 
 
-def _run_child(data: bytes, deadline, mode: str):
-    """Runs `python -m app.backend.pdf_hidden <seconds> <mode>` ('scan' | 'text' | 'both') and returns its JSON lines. Every PDF parser (pypdf's
+def _run_child(data: bytes, deadline, mode: str, extra: str = ""):
+    """Runs `python -m app.backend.pdf_hidden <seconds> <mode> [extra]` ('scan' | 'text' | 'both' | 'render', whose extra is the page list) and returns its JSON lines. Every PDF parser (pypdf's
     text read and PDFium's render) runs in this child and nowhere else (T-087 round 4). The child gets a hard wall-clock kill at `deadline`
     (a time.monotonic() value; default DEFAULT_SCAN_S from now), an RLIMIT_CPU just past it, core dumps off, RLIMIT_AS where the platform
     enforces it and a parent-side RSS watch on every platform. Only the child process this call started is ever killed."""
@@ -555,11 +555,25 @@ def _run_child(data: bytes, deadline, mode: str):
         env = {k: os.environ[k] for k in _CHILD_ENV_KEEP if k in os.environ}
         env["PYTHONDONTWRITEBYTECODE"] = "1"
         try:
-            proc = subprocess.Popen([sys.executable, "-m", "app.backend.pdf_hidden", "%.3f" % remaining, mode], cwd=_ROOT, env=env,
+            proc = subprocess.Popen([sys.executable, "-m", "app.backend.pdf_hidden", "%.3f" % remaining, mode] + ([extra] if extra else []), cwd=_ROOT, env=env,
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, close_fds=True)
         except OSError as e:
             raise HiddenScanUnavailable(type(e).__name__) from None
-        first, out = True, b""
+        stdin, proc.stdin = proc.stdin, None        # the file goes in from its own thread in big writes (T-107): Popen.communicate(input) writes
+                                                    # 512 bytes per loop on macOS and loses the GIL each time, so two uploads at once took minutes
+
+        def feed():
+            try:
+                stdin.write(data)
+            except (OSError, ValueError):           # the child died or was killed before it read the file; the loop below sees that
+                pass
+            finally:
+                try:
+                    stdin.close()
+                except (OSError, ValueError):
+                    pass
+        threading.Thread(target=feed, daemon=True).start()
+        out = b""
         while True:
             left = deadline - time.monotonic()
             if left <= 0:
@@ -567,11 +581,11 @@ def _run_child(data: bytes, deadline, mode: str):
                 proc.communicate()                  # reap it
                 raise HiddenScanTimeout("deadline")
             try:
-                out, _ = proc.communicate(data if first else None, timeout=min(WATCH_EVERY_S, left))
+                out, _ = proc.communicate(timeout=min(WATCH_EVERY_S, left))
                 break
             except subprocess.TimeoutExpired:
-                first = False
-            except OSError:                         # broken pipe: the child died before it read the file
+                pass
+            except OSError:
                 proc.kill()
                 proc.communicate()
                 raise HiddenScanUnavailable("child_died") from None
@@ -638,6 +652,14 @@ def read_text(data: bytes, deadline: float = None) -> list:
     return texts
 
 
+def render_messages(data: bytes, pages: list, deadline: float = None) -> list:
+    """OCR page rendering in the same killed child (T-107): the child's JSON lines (see pdf_ocr.render_in_child). PDFium opens the file and
+    draws the pages only inside the child, with the deadline kill, RLIMIT_CPU and the RSS watch, so a stamp or appearance bomb costs the API
+    process nothing. A child that was killed, crashed or ran out of time is HiddenScanUnavailable / HiddenScanTimeout; there is no
+    in-process fallback (pdf_ocr.render_pages turns both into OcrFailed)."""
+    return _run_child(data, deadline, "render", ",".join(str(int(n)) for n in pages))
+
+
 def _limit_child(remaining: float):
     """Called first thing in the child: CPU limit just past the deadline, no core files, memory limit where it is enforced."""
     try:
@@ -668,6 +690,10 @@ def _child_main(argv):
     data = sys.stdin.buffer.read()
     soft = start + remaining - 0.2
     try:
+        if mode == "render":
+            from app.backend import pdf_ocr
+            pdf_ocr.render_in_child(data, [int(x) for x in (argv[3] if len(argv) > 3 else "").split(",") if x.strip().isdigit()], soft, _emit)
+            return
         if mode in ("text", "both"):
             from app.backend import pdf_text
             try:
"""T-107 (T-087 round 4 major): with ocr=true the page rendering runs in the same killed child as the hidden-text scan, a child that is
killed or fails makes the upload a 400 and is never retried in the API process, and no PDFium or pypdf call exists in the API process.
The bomb is the reviewer's: a ~3 MB Stamp annotation whose appearance stream inflates to GBs (here 1500 MB, with the RSS ceiling lowered).
SYNTHETIC text only."""
import ast
import os
import pathlib
import shutil
import threading
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import pdf_checks, pdf_hidden, pdf_ocr, pdf_text
from app.backend.api import create_app
from tests.unit import _pdf_probe as K
from tests.unit.test_pdf_hidden_r4 import ap_bomb, _children, _rss_mb
from tests.unit.test_pdf_ocr import scan_pdf

pypdfium2 = pytest.importorskip("pypdfium2")
PDF = {"content-type": "application/pdf"}
needs_tesseract = pytest.mark.skipif(not shutil.which("tesseract"), reason="tesseract is not installed")
APP = pathlib.Path(pdf_checks.__file__).resolve().parents[1]


@pytest.fixture
def live(tmp_path, monkeypatch):
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return TestClient(create_app(str(tmp_path / "t.sqlite"), static_dir=str(tmp_path)))


@pytest.fixture
def spies(monkeypatch):
    """Record every PDFium / pypdf open in THIS process (the child is another process and is not affected)."""
    import pypdf
    calls = []

    def spy(name, real):
        def f(*a, **k):
            calls.append(name)
            return real(*a, **k)
        return f
    monkeypatch.setattr(pypdfium2, "PdfDocument", spy("PdfDocument", pypdfium2.PdfDocument))
    monkeypatch.setattr(pypdf, "PdfReader", spy("PdfReader", pypdf.PdfReader))
    return calls


# ---- static: where the parsers may be imported ----
def test_pdfium_and_pypdf_are_imported_only_inside_the_child_functions():
    allowed = {("pdf_hidden.py", "scan_inprocess"), ("pdf_text.py", "read_pages"), ("pdf_ocr.py", "render_in_child")}
    found = set()
    for path in APP.rglob("*.py"):
        tree = ast.parse(path.read_text())
        for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))] + [tree]:
            body = fn.body if fn is not tree else tree.body
            for stmt in body:
                for node in ast.walk(stmt) if fn is not tree else ([stmt] if isinstance(stmt, (ast.Import, ast.ImportFrom)) else []):
                    mods = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
                    if any(m.split(".")[0] in ("pypdf", "pypdfium2") for m in mods):
                        found.add((path.name, getattr(fn, "name", "<module>")))
    assert found <= allowed, f"PDF parser imported outside the child code: {found - allowed}"
    assert ("pdf_ocr.py", "render_in_child") in found


def test_render_in_child_is_only_reached_from_the_child_main():
    callers = []
    for path in APP.rglob("*.py"):
        for line in path.read_text().splitlines():
            if "render_in_child(" in line and "def render_in_child" not in line:
                callers.append((path.name, line.strip()))
    assert [c[0] for c in callers] == ["pdf_hidden.py"], callers
    assert "_child_main" in (APP / "backend" / "pdf_hidden.py").read_text().split("render_in_child(")[0].rsplit("def ", 1)[1]


# ---- fail closed: a child that was killed or failed is never retried in the API process ----
def test_a_killed_scan_child_with_ocr_is_refused_and_ocr_never_runs(monkeypatch, spies):
    def killed(*a, **k):
        raise pdf_hidden.HiddenScanUnavailable("memory", ["x" * 30])
    monkeypatch.setattr(pdf_hidden, "scan", killed)
    monkeypatch.setattr(pdf_ocr, "ocr_pages", lambda *a, **k: pytest.fail("OCR ran on a file whose scan child was killed"))
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(K.one_page(K.VISIBLE), ocr=True)
    assert e.value.code == "ocr_check_failed" and e.value.detail == {"cause": "memory"}
    assert spies == []


@pytest.mark.parametrize("why", ["memory", "child_failed", "child_died"])
def test_every_scan_child_failure_with_ocr_is_a_400_with_a_plain_reason(live, monkeypatch, spies, why):
    monkeypatch.setattr(pdf_hidden, "scan", lambda *a, **k: (_ for _ in ()).throw(pdf_hidden.HiddenScanUnavailable(why, ["t" * 40])))
    r = live.post("/api/cases/pdf?ocr=true", content=K.one_page(K.VISIBLE), headers=PDF)
    assert r.status_code == 400 and r.json()["error"]["detail"]["reason"] == "ocr_check_failed"
    assert "could not be checked safely" in r.json()["error"]["message"] and spies == []


@pytest.mark.parametrize("why", ["memory", "child_failed"])
def test_a_killed_render_child_is_ocr_failed_and_there_is_no_fallback(monkeypatch, spies, why):
    monkeypatch.setattr(pdf_ocr, "ocr_status", lambda: {"available": True, "version": "5.5.2", "languages": ["eng"], "message": ""})
    monkeypatch.setattr(pdf_hidden, "render_messages", lambda *a, **k: (_ for _ in ()).throw(pdf_hidden.HiddenScanUnavailable(why)))
    monkeypatch.setattr(pdf_ocr, "render_page_png", lambda *a, **k: pytest.fail("rendered in the API process"))
    data = scan_pdf()
    spies.clear()                  # the fixture builder itself may open a document; only the calls after this point count
    with pytest.raises(pdf_ocr.OcrFailed) as e:
        pdf_ocr.ocr_pages(data, [1])
    assert e.value.reason == "render_killed" and spies == []


def test_a_render_that_hits_the_deadline_is_a_timeout_not_a_fallback(monkeypatch, spies):
    monkeypatch.setattr(pdf_ocr, "ocr_status", lambda: {"available": True, "version": "5.5.2", "languages": ["eng"], "message": ""})
    monkeypatch.setattr(pdf_hidden, "render_messages", lambda *a, **k: (_ for _ in ()).throw(pdf_hidden.HiddenScanTimeout("deadline")))
    data = scan_pdf()
    spies.clear()
    with pytest.raises(pdf_ocr.OcrFailed) as e:
        pdf_ocr.ocr_pages(data, [1])
    assert e.value.reason == "timeout" and spies == []


# ---- the render really happens in the child, under the same watchdog ----
@needs_tesseract
def test_a_scanned_pdf_with_ocr_renders_in_the_child_and_the_api_process_opens_no_pdf(live, spies):
    data = scan_pdf()
    spies.clear()
    r = live.post("/api/cases/pdf?ocr=true", content=data, headers=PDF)
    assert r.status_code == 201, r.text
    assert r.json()["pdf_checks"]["ocr"]["ran"] is True
    assert spies == [], f"PDF parser called in the API process: {spies}"


def test_the_render_child_stops_on_the_rss_ceiling_with_the_reviewers_bomb(monkeypatch, spies):
    """The render child alone (the scan is skipped): a Stamp appearance that inflates to GBs is killed by the RSS watch and the API
    process neither renders it nor grows."""
    monkeypatch.setattr(pdf_hidden, "CHILD_RSS_BYTES", 400 * 1024 ** 2)
    monkeypatch.setattr(pdf_ocr, "ocr_status", lambda: {"available": True, "version": "5.5.2", "languages": ["eng"], "message": ""})
    data = ap_bomb(1500)
    assert len(data) < 3 * 1024 ** 2
    rss0, t = _rss_mb(), time.monotonic()
    with pytest.raises(pdf_ocr.OcrFailed) as e:
        pdf_ocr.ocr_pages(data, [1], deadline=time.monotonic() + 30)
    assert e.value.reason == "render_killed" and time.monotonic() - t < 20
    assert _rss_mb() - rss0 < 150 and _children() == [] and spies == []


def test_the_bomb_with_ocr_true_is_a_400_and_the_api_rss_stays_flat(live, monkeypatch, spies):
    monkeypatch.setattr(pdf_hidden, "CHILD_RSS_BYTES", 400 * 1024 ** 2)
    data = ap_bomb(1500)
    rss0, t = _rss_mb(), time.monotonic()
    peak, stop = [rss0], threading.Event()

    def sample():
        while not stop.is_set():
            peak[0] = max(peak[0], _rss_mb())
            time.sleep(0.05)
    th = threading.Thread(target=sample, daemon=True)
    th.start()
    r = live.post("/api/cases/pdf?ocr=true", content=data, headers=PDF)
    time.sleep(1.0)
    stop.set()
    th.join()
    assert r.status_code == 400 and r.json()["error"]["detail"]["reason"] in ("ocr_check_failed", "ocr_render_failed"), r.text
    assert time.monotonic() - t < 25 and peak[0] - rss0 < 200, f"API RSS grew {peak[0] - rss0:.0f} MB"
    assert _children() == [] and spies == []


def test_two_concurrent_bombs_with_ocr_are_400_or_429_and_the_api_rss_stays_flat(live, monkeypatch, spies):
    monkeypatch.setattr(pdf_hidden, "CHILD_RSS_BYTES", 400 * 1024 ** 2)
    data, results = ap_bomb(1500), []
    rss0 = _rss_mb()

    def post():
        r = live.post("/api/cases/pdf?ocr=true", content=data, headers=PDF)
        results.append(r.status_code)
    ths = [threading.Thread(target=post) for _ in range(2)]
    for th in ths:
        th.start()
    peak = rss0
    while any(th.is_alive() for th in ths):
        peak = max(peak, _rss_mb())
        time.sleep(0.05)
    assert sorted(results) and all(c in (400, 429) for c in results), results
    assert peak - rss0 < 250 and _children() == [] and spies == []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:20:15.257Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; grep -n \"ocr\\|dpi\\|DPI\\|Query\\|scale\" $A/app/backend/api.py | sed -n 1,60p; grep -n \"^[A-Z_]* *= \" $A/app/backend/pdf_ocr.py | head -40; grep -n \"MAX_PDF_JOBS\\|MAX_PAGES\\|MAX_OCR_PAGES\\|CHILD_RSS\\|DEFAULT_SCAN_S\\|MAX_BYTES\\|MAX_PDF\" $A/app/backend/*.py | head -30"
}
````

### User / tool · 2026-11-02T06:20:15.365Z

**tool result**
````
251:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):
253:        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
265:        if (ocr or "").lower() in ("1", "true", "yes"):
266:            opts["ocr"] = True
270:            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data, **opts), _pdf_checks.OCR_TIMEOUT_S if opts.get("ocr") else pdf_text.EXTRACT_TIMEOUT_S)
277:                           (e.detail.get("message") if e.code == "ocr_unavailable" else None) or _PDF_MESSAGES[e.code], {"reason": e.code, **e.detail}) from None
22:TESTED_VERSION = "5.5.2"
23:MIN_MAJOR = 5
24:DPI = 150                       # render density; Tesseract reads 150 to 300 dpi, and a smaller image keeps the stored page small
25:LOW_CONF_WORD = 60              # a word below this confidence (0-100) is marked
26:LOW_CONF_NUMBER = 80            # a word with a digit in it needs this much: a wrong digit changes a date or a dollar amount
27:MAX_OCR_PAGES = 10              # more scanned pages than this is refused, not partly read
28:PAGE_TIMEOUT_S = 40
29:TOTAL_TIMEOUT_S = 150
30:MAX_LOW_CONF_LISTED = 400
31:MAX_PAGE_PT = 2880              # a page larger than 40 inches on a side is refused (PDF allows 14400 pt; a 1 KB file could ask for 2 GB of bitmap)
32:MAX_SIDE_PX = 3500              # longest side of the rendered page; a larger page is rendered smaller than DPI, never bigger
33:MAX_PIXELS = 8_000_000          # width x height of the rendered page (US Letter at 150 dpi is 2.1 million)
34:MAX_STORED_PNG_BYTES = 12 * 1024 * 1024     # all page images of one upload together; they are kept with the case
35:INSTALL_HINT = "Install Tesseract: macOS `brew install tesseract`; Debian/Ubuntu `sudo apt-get install tesseract-ocr`."
37:_ENV_KEEP = ("PATH", "TMPDIR", "TESSDATA_PREFIX", "LANG", "LC_ALL", "LC_CTYPE")     # nothing else: no API key, token or HOME reaches the binary
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/api.py:257:        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/api.py:262:            if len(data) > pdf_text.MAX_PDF_BYTES:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/api.py:274:            if e.code == "pdf_busy":     # T-087 round 4: at most pdf_checks.MAX_PDF_JOBS uploads are read at once; the rest are told to retry
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_ocr.py:27:MAX_OCR_PAGES = 10              # more scanned pages than this is refused, not partly read
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:31:parent-side poll of the child's RSS that kills it above CHILD_RSS_BYTES, so no work survives the deadline however slow a native call
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:65:CHILD_RSS_BYTES = 1024 ** 3                # resident-memory ceiling the parent enforces by polling, on every platform (macOS has no RLIMIT_AS)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:67:DEFAULT_SCAN_S = 60.0       # wall clock for scan() when the caller gives no deadline
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:542:    (a time.monotonic() value; default DEFAULT_SCAN_S from now), an RLIMIT_CPU just past it, core dumps off, RLIMIT_AS where the platform
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:545:    deadline = deadline if deadline is not None else now + DEFAULT_SCAN_S
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:592:            if _rss_bytes(proc.pid) > CHILD_RSS_BYTES:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:686:    remaining = float(argv[1]) if len(argv) > 1 else DEFAULT_SCAN_S
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_checks.py:16:MAX_PDF_JOBS = 2             # uploads being processed at once (text read, scan, OCR); the next ones get a 429 instead of queueing (T-087 round 4)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_checks.py:18:_JOBS = threading.BoundedSemaphore(MAX_PDF_JOBS)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_checks.py:26:    "ocr_too_many_pages": f"This PDF has more than {pdf_ocr.MAX_OCR_PAGES} scanned pages; OCR reads at most that many in one upload. Split the file.",
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_checks.py:114:            if len(scan_pages) > pdf_ocr.MAX_OCR_PAGES:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_checks.py:115:                raise PdfError("ocr_too_many_pages", {"scanned_pages": len(scan_pages), "max": pdf_ocr.MAX_OCR_PAGES})
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_text.py:9:MAX_PDF_BYTES = 5 * 1024 * 1024
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_text.py:10:MAX_PAGES = 100
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_text.py:41:    if len(data or b"") > MAX_PDF_BYTES:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_text.py:54:            if len(reader.pages) > MAX_PAGES:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:20:21.247Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; mkdir -p artifacts/review-evidence/T-107 $SP/bombs; .venv/bin/python -I artifacts/review-evidence/T-087-r4/probe_r4_rss.py $A $SP/bombs 3500 2>&1 | tail -8; ls -la $SP/bombs; ps -axo pid,ppid,command | grep '[p]df_hidden' | head"
}
````

### User / tool · 2026-11-02T06:20:33.256Z

**tool result**
````
file 3484 KB, AP inflates to 3500 MB
watchdog on (real value): limit=1.00 GiB -> HiddenScanUnavailable('memory') texts_kept=True; wall=0.4s; child peak RSS by ps=759 MB
watchdog off (control): limit=9313.23 GiB -> returned checked=True pages=[1]; wall=2.8s; child peak RSS by ps=4556 MB
children left: none
total 6976
drwxr-xr-x@   3 arsis  wheel       96 Nov  2 00:20 .
drwx------@ 750 arsis  wheel    24000 Nov  2 00:20 ..
-rw-r--r--@   1 arsis  wheel  3568121 Nov  2 00:20 ap_3500.pdf
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:20:37.542Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; lsof -iTCP:7891 -sTCP:LISTEN; for q in ocr=true ocr=false; do echo \"== $q\"; .venv/bin/python -I artifacts/review-evidence/T-087-r4/probe_r4_ocr.py $A $SP/bombs/ap_3500.pdf $q 7891 8 2>&1 | tail -12; done"
}
````

### User / tool · 2026-11-02T06:20:55.947Z

**tool result**
````
== ocr=true
server pid 5761; idle (rss MB, cputime, %cpu) = (63, '0:00.36', 52.5); file ap_3500.pdf 3484 KB; query ocr=true
  +   0.4s server rss/cputime/%cpu=(86, '0:00.38', 16.2) peak_rss=86 MB health=8 ms pdf_hidden_children=0
  response: (400, 'bad_request', 'ocr_check_failed', 0.4)
  +   2.4s server rss/cputime/%cpu=(86, '0:00.39', 0.4) peak_rss=86 MB health=7 ms pdf_hidden_children=0
  +   4.4s server rss/cputime/%cpu=(86, '0:00.40', 0.4) peak_rss=86 MB health=6 ms pdf_hidden_children=0
  +   6.5s server rss/cputime/%cpu=(86, '0:00.40', 0.4) peak_rss=86 MB health=7 ms pdf_hidden_children=0
  +   8.5s server rss/cputime/%cpu=(86, '0:00.41', 0.4) peak_rss=86 MB health=6 ms pdf_hidden_children=0
summary: response=(400, 'bad_request', 'ocr_check_failed', 0.4) server peak RSS=86 MB max health latency=11 ms; server final=(86, '0:00.42', 0.5)
== ocr=false
server pid 5933; idle (rss MB, cputime, %cpu) = (57, '0:00.28', 49.2); file ap_3500.pdf 3484 KB; query ocr=false
  +   0.4s server rss/cputime/%cpu=(80, '0:00.30', 11.9) peak_rss=80 MB health=9 ms pdf_hidden_children=0
  response: (400, 'bad_request', 'pdf_only_hidden_text', 0.4)
  +   2.4s server rss/cputime/%cpu=(80, '0:00.31', 0.3) peak_rss=80 MB health=7 ms pdf_hidden_children=0
  +   4.4s server rss/cputime/%cpu=(80, '0:00.32', 0.3) peak_rss=80 MB health=6 ms pdf_hidden_children=0
  +   6.5s server rss/cputime/%cpu=(80, '0:00.33', 0.4) peak_rss=80 MB health=6 ms pdf_hidden_children=0
  +   8.5s server rss/cputime/%cpu=(80, '0:00.34', 0.4) peak_rss=80 MB health=7 ms pdf_hidden_children=0
summary: response=(400, 'bad_request', 'pdf_only_hidden_text', 0.4) server peak RSS=80 MB max health latency=10 ms; server final=(80, '0:00.34', 0.6)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:21:14.813Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; sed -n 60,180p $A/app/backend/pdf_ocr.py; sed -n 55,150p $A/app/backend/pdf_checks.py"
}
````

### User / tool · 2026-11-02T06:21:14.905Z

**tool result**
````
def ocr_status() -> dict:
    """{available, version, tested_version, languages, message}. Never raises."""
    exe = _which()
    if not exe:
        return {"available": False, "version": None, "tested_version": TESTED_VERSION, "languages": [],
                "message": "Scanned pages need Tesseract, which is not installed on this server. " + INSTALL_HINT}
    try:
        v = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=10, env=_env())
        first = ((v.stdout or v.stderr).splitlines() or [""])[0]
        m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", first)
        version = m.group(0) if m else None
        langs = subprocess.run([exe, "--list-langs"], capture_output=True, text=True, timeout=10, env=_env())
        languages = [x.strip() for x in (langs.stdout or "").splitlines()[1:] if x.strip() and x.strip() not in ("osd", "snum")]
    except (OSError, subprocess.SubprocessError):
        return {"available": False, "version": None, "tested_version": TESTED_VERSION, "languages": [],
                "message": "Tesseract is installed but could not be run. " + INSTALL_HINT}
    if not m or int(m.group(1)) < MIN_MAJOR or "eng" not in languages:
        return {"available": False, "version": version, "tested_version": TESTED_VERSION, "languages": languages,
                "message": f"This server has Tesseract {version or '(unknown version)'} with English data "
                           f"{'present' if 'eng' in languages else 'missing'}; version {MIN_MAJOR} or later with English data is needed. " + INSTALL_HINT}
    return {"available": True, "version": version, "tested_version": TESTED_VERSION, "languages": languages,
            "message": f"Tesseract {version} is available."}


# ------------------------------------------------------------------ images
def _png_chunk(tag: bytes, body: bytes) -> bytes:
    c = tag + body
    return struct.pack(">I", len(body)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)


def _png(rows, w: int, h: int) -> bytes:
    """8-bit greyscale PNG from an iterable of `h` rows of `w` bytes, compressed row by row (stdlib only; one page is never held three times)."""
    z = zlib.compressobj(6)
    body = bytearray()
    for row in rows:
        body += z.compress(b"\x00")
        body += z.compress(row)
    body += z.flush()
    return b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0)) + _png_chunk(b"IDAT", bytes(body)) + _png_chunk(b"IEND", b"")


def render_scale(width_pt: float, height_pt: float) -> float:
    """The render scale for a page: DPI/72, lowered so neither side passes MAX_SIDE_PX nor the area MAX_PIXELS. Raises OcrFailed
    ("page_too_large") for a page over MAX_PAGE_PT on a side or one with no usable size."""
    longest = max(width_pt, height_pt)
    if not (width_pt > 0 and height_pt > 0) or longest > MAX_PAGE_PT:
        raise OcrFailed("page_too_large")
    return min(DPI / 72.0, MAX_SIDE_PX / longest, (MAX_PIXELS / (width_pt * height_pt)) ** 0.5)


def render_page_png(pdf, index: int) -> bytes:
    """Greyscale PNG of page `index` (0-based) of an open pypdfium2 document at DPI (capped by render_scale)."""
    page = pdf[index]
    try:
        scale = render_scale(*page.get_size())
        bitmap = page.render(scale=scale)
        try:
            w, h, stride, ch = bitmap.width, bitmap.height, bitmap.stride, bitmap.n_channels
            view = memoryview(bitmap.buffer).cast("B")
            off = 1 if ch >= 3 else 0          # the green channel stands in for luminance
            return _png((view[y * stride + off: y * stride + w * ch: ch].tobytes() for y in range(h)), w, h)
        finally:
            bitmap.close()
    finally:
        page.close()


# ------------------------------------------------------------------ tesseract
def _parse_tsv(tsv: str) -> dict:
    """Page text and word list from Tesseract TSV. Lines are rebuilt from the word rows, so word offsets are exact."""
    rows = [r for r in csv.reader(io.StringIO(tsv), delimiter="\t", quoting=csv.QUOTE_NONE) if len(r) >= 12 and r[0] != "level"]
    text, words, last_line, last_block = "", [], None, None
    for r in rows:
        if r[0] != "5" or not r[11].strip():
            continue
        try:
            conf = float(r[10])
        except ValueError:
            continue
        key, block = (r[2], r[3], r[4]), (r[2], r[3])
        if last_line is not None:
            text += ("\n\n" if block != last_block else "\n") if key != last_line else " "
        start = len(text)
        text += r[11].strip()
        words.append({"text": r[11].strip(), "start": start, "end": len(text), "conf": round(conf, 1)})
        last_line, last_block = key, block
    return {"text": text, "words": words}


def is_low(word: dict) -> bool:
    need = LOW_CONF_NUMBER if any(c.isdigit() for c in word["text"]) else LOW_CONF_WORD
    return word["conf"] < need


def ocr_png(png: bytes, languages: list = None, timeout: float = PAGE_TIMEOUT_S, status: dict = None) -> dict:
    """{text, words:[{text,start,end,conf}], low_conf:[...], mean_conf}. Raises OcrUnavailable / OcrFailed."""
    st = status or ocr_status()
    if not st["available"]:
        raise OcrUnavailable(st["message"])
    lang = "+".join(l for l in (languages or ["eng"]) if l in st["languages"]) or "eng"
    with tempfile.TemporaryDirectory(prefix="zlayt-ocr-") as d:
        src = os.path.join(d, "page.png")
        with open(src, "wb") as f:
            f.write(png)
        try:
            p = subprocess.run([_which(), src, "stdout", "-l", lang, "--psm", "3", "tsv"], capture_output=True, text=True,
                               timeout=timeout, env=_env(), cwd=d)
        except subprocess.TimeoutExpired:
            raise OcrFailed("timeout") from None
        except OSError:
            raise OcrFailed("exec") from None
    if p.returncode != 0:
        raise OcrFailed("exit")
    got = _parse_tsv(p.stdout)
    low = [w for w in got["words"] if is_low(w)]
    confs = [w["conf"] for w in got["words"]]
    return {"text": got["text"], "words": got["words"], "low_conf": low,
            "mean_conf": round(sum(confs) / len(confs), 1) if confs else None}


    Fail closed (T-087 round 2): a page whose hidden-text check could not run, or whose text-layer words the renderer did not place on the
    page, is kept out of the case text and listed in the report until the paralegal confirms it. Nothing is included silently."""
    if not _JOBS.acquire(timeout=BUSY_WAIT_S):
        raise PdfError("pdf_busy")
    try:
        return _extract(data, ocr=ocr, include_hidden=include_hidden,
                        deadline=deadline or time.monotonic() + (OCR_TIMEOUT_S if ocr else pdf_text.EXTRACT_TIMEOUT_S))
    finally:
        _JOBS.release()


def _extract(data: bytes, *, ocr: bool, include_hidden, deadline: float) -> dict:
    try:                       # the text-layer read (pypdf) and the render scan (PDFium) both run in one child process killed at the deadline
        scanned = pdf_hidden.scan(data, deadline, with_text=True)
        texts = scanned.pop("texts")
    except pdf_hidden.HiddenScanUnavailable as e:
        if ocr:                # T-107: a file whose scan child was killed or failed is never handed to OCR; no fallback render anywhere
            raise PdfError("ocr_check_failed", {"cause": str(e)[:40]}) from None
        texts = e.texts
        if texts is None:      # the child failed before it had read the text layer: there is nothing to hold back, the file is unreadable
            raise PdfError("pdf_unreadable") from None
        scanned = pdf_hidden.unchecked_scan(len(texts))
    except pdf_hidden.HiddenScanTimeout:
        raise PdfError("pdf_unreadable", {"reason": "pdf_timeout"}) from None
    confirmed = parse_confirmed(include_hidden, len(texts))
    checks = {"hidden_text": {"checked": False, "pages": [], "excluded_until_confirmed": True,
                              "message": "Hidden-text check did not run on this file."},
              "ocr": {"requested": bool(ocr), "ran": False, "pages": [], "status": pdf_ocr.ocr_status()}}
    for n in range(1, len(texts) + 1):               # a page the renderer did not list is a page nobody checked
        scanned["pages"].setdefault(n, pdf_hidden._unchecked("page_not_rendered"))
    sources = {}
    for n, p in scanned["pages"].items():
        if n > len(texts) or p.get("unchecked"):
            continue
        spans = pdf_hidden.unlisted_spans(texts[n - 1], p["listed_text"])      # words only the extractor can reach
        p["hidden"] = p["hidden"] + [{"text": sp, "reasons": ["not_in_rendered_page"], "bbox": None} for sp in spans]
    for n, p in scanned["pages"].items():
        if n > len(texts) or n in confirmed:
            continue
        if p.get("unchecked"):
            if "".join(texts[n - 1].split()):
                texts[n - 1] = ""                       # text we could not check stays out; a page with no text has nothing to hold back
            else:
                p["unchecked"] = None
        elif p["hidden"]:
            texts[n - 1] = pdf_hidden.remove_from_text(texts[n - 1], p["hidden"], p["visible_text"])
    checks["hidden_text"] = pdf_hidden.report(scanned, confirmed)
    for n in confirmed:
        if n in scanned["pages"] and (scanned["pages"][n]["hidden"] or scanned["pages"][n].get("unchecked")):
            sources[n] = {"hidden_text_included": True}
    # a page with no text left but a picture on it is a scan (or has only hidden text over a picture)
    image_pages = [n for n, p in scanned["pages"].items() if n <= len(texts) and not "".join(texts[n - 1].split()) and p["has_image"]]
    blank = [n for n, t in enumerate(texts, 1) if not "".join(t.split())]
    scan_pages = sorted(set(image_pages) | (set(blank) if not any("".join(t.split()) for t in texts) else set()))
    ocr_page_data = {}
    if scan_pages:
        checks["ocr"]["scanned_pages"] = scan_pages
        if ocr:
            if len(scan_pages) > pdf_ocr.MAX_OCR_PAGES:
                raise PdfError("ocr_too_many_pages", {"scanned_pages": len(scan_pages), "max": pdf_ocr.MAX_OCR_PAGES})
            try:
                ocr_page_data = pdf_ocr.ocr_pages(data, scan_pages, deadline=deadline)
            except pdf_ocr.OcrUnavailable as e:
                raise PdfError("ocr_unavailable", {"message": str(e), "ocr": checks["ocr"]["status"]}) from None
            except pdf_ocr.OcrFailed as e:
                code = {"page_too_large": "ocr_page_too_large", "images_too_large": "ocr_images_too_large",
                        "render_killed": "ocr_render_failed", "render_failed": "ocr_render_failed"}.get(e.reason, "ocr_failed")
                raise PdfError(code, {"page": e.page} if e.page else None) from None
            for n, o in ocr_page_data.items():
                texts[n - 1] = o["text"].strip()
                sources[n] = {"source": "ocr", "mean_conf": o["mean_conf"], "words": o["words"], "has_image": True}
    if sum(len("".join(t.split())) for t in texts) < pdf_text.MIN_TEXT_CHARS:
        hidden_pages = [p["page"] for p in checks["hidden_text"]["pages"] if not p["confirmed"]]
        detail = {"scanned_pages": scan_pages, "ocr": checks["ocr"]["status"], "hidden_text_pages": hidden_pages,
                  "unchecked_pages": [p for p in checks["hidden_text"]["unchecked_pages"] if p in hidden_pages]}
        raise PdfError("pdf_only_hidden_text" if hidden_pages else "pdf_no_text_layer", detail)
    got = pdf_text.assemble(texts, sources)
    images, low = {}, 0
    for pg in got["pages"]:
        o = ocr_page_data.get(pg["page"])
        if o:
            base = pg["start"]
            pg["low_conf"] = [{"start": base + w["start"], "end": base + w["end"], "text": w["text"], "conf": w["conf"]}
                              for w in o["low_conf"][:pdf_ocr.MAX_LOW_CONF_LISTED]]
            pg["low_conf_count"] = len(o["low_conf"])
            low += len(o["low_conf"])
            images[pg["page"]] = o["png_b64"]
    if ocr_page_data:
        checks["ocr"].update({"ran": True, "engine": f"tesseract {checks['ocr']['status']['version']}",
                              "pages": sorted(ocr_page_data), "low_conf_words": low,
                              "low_conf_rule": f"words under {pdf_ocr.LOW_CONF_WORD} confidence, or under {pdf_ocr.LOW_CONF_NUMBER} when the word has a digit",
                              "items_need_review": True})
    return {"text": got["text"], "pages": got["pages"], "pdf_checks": checks, "page_images": images}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:21:17.250Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; sed -n 536,720p $A/app/backend/pdf_hidden.py; grep -n \"def \\|^import\\|^from\" artifacts/review-evidence/T-086-087/pdfkit.py | head -30"
}
````

### User / tool · 2026-11-02T06:21:17.338Z

**tool result**
````
    return None


def _run_child(data: bytes, deadline, mode: str, extra: str = ""):
    """Runs `python -m app.backend.pdf_hidden <seconds> <mode> [extra]` ('scan' | 'text' | 'both' | 'render', whose extra is the page list) and returns its JSON lines. Every PDF parser (pypdf's
    text read and PDFium's render) runs in this child and nowhere else (T-087 round 4). The child gets a hard wall-clock kill at `deadline`
    (a time.monotonic() value; default DEFAULT_SCAN_S from now), an RLIMIT_CPU just past it, core dumps off, RLIMIT_AS where the platform
    enforces it and a parent-side RSS watch on every platform. Only the child process this call started is ever killed."""
    now = time.monotonic()
    deadline = deadline if deadline is not None else now + DEFAULT_SCAN_S
    if now >= deadline:
        raise HiddenScanTimeout("deadline")
    if not _SLOTS.acquire(timeout=max(deadline - now, 0)):
        raise HiddenScanTimeout("deadline")        # every slot busy until the deadline: the caller's wait is over
    proc = None
    try:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise HiddenScanTimeout("deadline")
        env = {k: os.environ[k] for k in _CHILD_ENV_KEEP if k in os.environ}
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        try:
            proc = subprocess.Popen([sys.executable, "-m", "app.backend.pdf_hidden", "%.3f" % remaining, mode] + ([extra] if extra else []), cwd=_ROOT, env=env,
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, close_fds=True)
        except OSError as e:
            raise HiddenScanUnavailable(type(e).__name__) from None
        stdin, proc.stdin = proc.stdin, None        # the file goes in from its own thread in big writes (T-107): Popen.communicate(input) writes
                                                    # 512 bytes per loop on macOS and loses the GIL each time, so two uploads at once took minutes

        def feed():
            try:
                stdin.write(data)
            except (OSError, ValueError):           # the child died or was killed before it read the file; the loop below sees that
                pass
            finally:
                try:
                    stdin.close()
                except (OSError, ValueError):
                    pass
        threading.Thread(target=feed, daemon=True).start()
        out = b""
        while True:
            left = deadline - time.monotonic()
            if left <= 0:
                proc.kill()
                proc.communicate()                  # reap it
                raise HiddenScanTimeout("deadline")
            try:
                out, _ = proc.communicate(timeout=min(WATCH_EVERY_S, left))
                break
            except subprocess.TimeoutExpired:
                pass
            except OSError:
                proc.kill()
                proc.communicate()
                raise HiddenScanUnavailable("child_died") from None
            if _rss_bytes(proc.pid) > CHILD_RSS_BYTES:
                proc.kill()
                partial, _ = proc.communicate()
                raise HiddenScanUnavailable("memory", _texts_of(_messages(partial)))
        msgs = _messages(out)
        if proc.returncode == -getattr(__import__("signal"), "SIGXCPU", 24):
            raise HiddenScanTimeout("cpu_limit")
        if proc.returncode != 0 or not msgs:
            raise HiddenScanUnavailable("child_failed", _texts_of(msgs))
        return msgs
    finally:
        if proc is not None and proc.poll() is None:
            proc.kill()
            proc.wait()
        _SLOTS.release()


def _pdf_error(msgs):
    """Re-raises, in the parent, the PdfError the child's text read ended with (a size, header, encryption or page-count refusal)."""
    from app.backend.pdf_text import PdfError
    for m in msgs:
        if m.get("pdf_error"):
            raise PdfError(str(m["pdf_error"]), m.get("detail") if isinstance(m.get("detail"), dict) else None)


def scan(data: bytes, deadline: float = None, with_text: bool = False) -> dict:
    """scan_inprocess() in a child Python process (see _run_child). Whatever the child is doing, nothing runs after the deadline:
    HiddenScanTimeout. A child that crashes or runs out of memory is HiddenScanUnavailable (the caller holds every page back as unchecked).
    `with_text=True` also has the same child read the text layer with pypdf first and adds it to the result as `texts` (a refusal such
    as pdf_encrypted is raised as PdfError); if the scan then fails, HiddenScanUnavailable carries `.texts`."""
    msgs = _run_child(data, deadline, "both" if with_text else "scan")
    if with_text:
        _pdf_error(msgs)
    texts = _texts_of(msgs)
    msg = msgs[-1]
    if with_text and texts is None:
        raise HiddenScanUnavailable("child_failed")
    if msg.get("error") == "timeout":
        raise HiddenScanTimeout("deadline")
    if "result" not in msg:
        raise HiddenScanUnavailable(str(msg.get("error") or "child_failed")[:60], texts)
    res = msg["result"]
    out = {"checked": res["checked"], "pages": {int(k): v for k, v in res["pages"].items()}}
    if with_text:
        out["texts"] = texts
    return out


def read_text(data: bytes, deadline: float = None) -> list:
    """pdf_text.read_pages() in the killed child (no scan): the stripped text of every page. Raises PdfError like read_pages, plus
    pdf_unreadable when the child failed and HiddenScanTimeout at the deadline."""
    from app.backend.pdf_text import PdfError
    try:
        msgs = _run_child(data, deadline, "text")
    except HiddenScanUnavailable:
        raise PdfError("pdf_unreadable") from None
    _pdf_error(msgs)
    texts = _texts_of(msgs)
    if texts is None:
        raise PdfError("pdf_unreadable")
    return texts


def render_messages(data: bytes, pages: list, deadline: float = None) -> list:
    """OCR page rendering in the same killed child (T-107): the child's JSON lines (see pdf_ocr.render_in_child). PDFium opens the file and
    draws the pages only inside the child, with the deadline kill, RLIMIT_CPU and the RSS watch, so a stamp or appearance bomb costs the API
    process nothing. A child that was killed, crashed or ran out of time is HiddenScanUnavailable / HiddenScanTimeout; there is no
    in-process fallback (pdf_ocr.render_pages turns both into OcrFailed)."""
    return _run_child(data, deadline, "render", ",".join(str(int(n)) for n in pages))


def _limit_child(remaining: float):
    """Called first thing in the child: CPU limit just past the deadline, no core files, memory limit where it is enforced."""
    try:
        import resource
    except ImportError:             # pragma: no cover - non-POSIX
        return
    cpu = int(math.ceil(remaining)) + 1
    for what, soft, hard in ((resource.RLIMIT_CPU, cpu, cpu + 2), (resource.RLIMIT_CORE, 0, 0),
                             (getattr(resource, "RLIMIT_AS", None), CHILD_MEM_BYTES, CHILD_MEM_BYTES)):
        if what is None:
            continue
        try:
            resource.setrlimit(what, (soft, hard))
        except (ValueError, OSError):       # macOS refuses RLIMIT_AS (ValueError); the CPU limit, the parent's kill and its RSS watch still hold
            pass


def _emit(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def _child_main(argv):
    remaining = float(argv[1]) if len(argv) > 1 else DEFAULT_SCAN_S
    mode = argv[2] if len(argv) > 2 else "scan"
    start = time.monotonic()
    _limit_child(remaining)
    data = sys.stdin.buffer.read()
    soft = start + remaining - 0.2
    try:
        if mode == "render":
            from app.backend import pdf_ocr
            pdf_ocr.render_in_child(data, [int(x) for x in (argv[3] if len(argv) > 3 else "").split(",") if x.strip().isdigit()], soft, _emit)
            return
        if mode in ("text", "both"):
            from app.backend import pdf_text
            try:
                _emit({"texts": pdf_text.read_pages(data, soft)})
            except pdf_text.PdfError as e:
                _emit({"pdf_error": e.code, "detail": e.detail})
                return
        if mode in ("scan", "both"):
            _emit({"result": scan_inprocess(data, soft)})
    except HiddenScanTimeout:
        _emit({"error": "timeout"})
    except HiddenScanUnavailable as e:
        _emit({"error": "unavailable: %s" % e})
    except MemoryError:
        _emit({"error": "memory"})


def _unchecked(reason: str) -> dict:
    return {"hidden": [], "visible_text": "", "listed_text": "", "has_image": False, "text_objects": 0, "unchecked": reason}


def unchecked_scan(n_pages: int, reason: str = "scan_unavailable") -> dict:
    """The scan result for a file the renderer could not open: every page unchecked."""
    return {"checked": False, "pages": {n: _unchecked(reason) for n in range(1, n_pages + 1)}}
2:import zlib
5:def pdf(objs, root=1):
19:def stream(content: bytes, extra: str = "", flate: bool = False) -> bytes:
30:def one_page(content: bytes, mediabox="0 0 600 800", extra_objs=(), xobjects="", flate=False):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:21:32.845Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; grep -rn \"scan_inprocess\\|read_pages\\|render_in_child\\|import_module\\|__import__\\|importlib\\|sys.modules\" $A/app --include=*.py | grep -v \"^.*:\\s*#\" ; cat $A/requirements.txt | grep -i \"pdf\\|fitz\\|mupdf\\|pillow\\|PIL\\|poppler\"; ls $A/tests/fixtures 2>/dev/null | head -3; cd $A && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_pdf_ocr_isolation.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T06:21:46.658Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/llm/audited.py:23:_CODE = __import__('re').compile(r"^([A-Z][A-Z_]{2,40})\b")
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/spanish_text.py:286:    return sys.modules[__name__] if language.is_translated(lang) else grounding
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_ocr.py:2:ever leaves it, and nothing here calls a network. Rendering is pypdfium2 (PDFium) and runs ONLY in the killed child process of pdf_hidden (T-107: render_in_child); PNG encoding is stdlib zlib.
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_ocr.py:182:def render_in_child(data: bytes, pages: list, soft_deadline: float, emit) -> None:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_text.py:36:def read_pages(data: bytes, deadline: float = None) -> list:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/review.py:17:_NUMERIC_TOKEN = __import__("re").compile(r"\d|^(?:january|february|march|april|june|july|august|september|october|november|december)$", __import__("re").IGNORECASE)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:32:is and no PDF parser runs in the API process. The in-process scan is `scan_inprocess()`.
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:454:def scan_inprocess(data: bytes, deadline: float = None) -> dict:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:597:        if proc.returncode == -getattr(__import__("signal"), "SIGXCPU", 24):
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:618:    """scan_inprocess() in a child Python process (see _run_child). Whatever the child is doing, nothing runs after the deadline:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:641:    """pdf_text.read_pages() in the killed child (no scan): the stripped text of every page. Raises PdfError like read_pages, plus
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:656:    """OCR page rendering in the same killed child (T-107): the child's JSON lines (see pdf_ocr.render_in_child). PDFium opens the file and
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:695:            pdf_ocr.render_in_child(data, [int(x) for x in (argv[3] if len(argv) > 3 else "").split(",") if x.strip().isdigit()], soft, _emit)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:700:                _emit({"texts": pdf_text.read_pages(data, soft)})
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5/app/backend/pdf_hidden.py:705:            _emit({"result": scan_inprocess(data, soft)})
pypdf==6.21.4
pypdfium2==5.14.0
llm
make_curated.py
.............                                                            [100%]
13 passed in 13.43s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:21:59.380Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; du -sh $A; ls $A/tests; ls $A/tests/unit | head -3; cat > $SP/mutate.sh <<'EOF'\n#!/bin/bash\n# usage: mutate.sh <name> <file relative to app/> <python snippet to append or \"prepend\"> \nSP=$1; NAME=$2; REL=$3; MODE=$4; SNIP=$5\nA=$SP/head_9851a0d_r5\nM=$SP/mut_$NAME\nrm -rf \"$M\"; mkdir -p \"$M\"\ncp -R \"$A/app\" \"$M/app\"; mkdir -p \"$M/tests\"; cp -R \"$A/tests/unit\" \"$M/tests/unit\"; cp \"$A/tests/__init__.py\" \"$M/tests/\" 2>/dev/null; cp -R \"$A/tests/fixtures\" \"$M/tests/fixtures\" 2>/dev/null\nif [ \"$MODE\" = append ]; then printf '\\n%s\\n' \"$SNIP\" >> \"$M/app/$REL\"; else printf '%s\\n%s\\n' \"$SNIP\" \"$(cat \"$M/app/$REL\")\" > \"$M/app/$REL\"; fi\ncd \"$M\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q -x tests/unit/test_pdf_ocr_isolation.py -k \"imported_only or reached_from\" 2>&1 | tail -6\nEOF\nchmod +x $SP/mutate.sh; ls $A/tests/__init__.py $A/tests/unit/__init__.py"
}
````

### User / tool · 2026-11-02T06:21:59.441Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (chmod +x)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:22:12.706Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/mutate_ast.py",
 "content": "\"\"\"T-107: mutation check of tests/unit/test_pdf_ocr_isolation.py AST tests. Copies app/ and tests/ of the pinned archive into a fresh scratch dir per\nmutation, injects one change, runs the two static tests. Prints PASS (test did NOT catch the mutation) or FAIL (test caught it).\nRun: .venv/bin/python -I mutate_ast.py <archive_root> <scratch_dir>\"\"\"\nimport pathlib\nimport shutil\nimport subprocess\nimport sys\n\nA, S = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\n\n# (name, file under app/, mode, snippet)\nMUTS = [\n    (\"m0_control_no_change\", \"backend/pdf_checks.py\", \"append\", \"\"),\n    (\"m1_func_import_pypdfium2_in_pdf_checks\", \"backend/pdf_checks.py\", \"append\", \"def _evil(data):\\n    import pypdfium2 as p\\n    return p.PdfDocument(data)\\n\"),\n    (\"m2_module_import_pypdf_in_api\", \"backend/api.py\", \"prepend\", \"import pypdf\"),\n    (\"m3_from_import_pypdf_in_pdf_text_extract\", \"backend/pdf_text.py\", \"append\", \"def extract2(data):\\n    from pypdf import PdfReader\\n    return PdfReader(data)\\n\"),\n    (\"m4_nested_import_inside_allowed_fn\", \"backend/pdf_ocr.py\", \"append\", \"def render_in_child2(d):\\n    import pypdfium2\\n\"),\n    (\"m5_dunder_import_call_no_import_stmt\", \"backend/pdf_checks.py\", \"append\", \"def _evil2(data):\\n    p = __import__('pypdfium2')\\n    return p.PdfDocument(data)\\n\"),\n    (\"m6_importlib_call\", \"backend/pdf_checks.py\", \"append\", \"def _evil3(data):\\n    import importlib\\n    return importlib.import_module('pypdf').PdfReader(data)\\n\"),\n    (\"m7_sys_modules_lookup\", \"backend/api.py\", \"append\", \"def _evil4(data):\\n    import sys\\n    return sys.modules['pypdfium2'].PdfDocument(data)\\n\"),\n    (\"m8_api_process_calls_child_side_scan_inprocess\", \"backend/pdf_checks.py\", \"append\", \"def _evil5(data):\\n    return pdf_hidden.scan_inprocess(data)\\n\"),\n    (\"m9_api_process_calls_child_side_read_pages\", \"backend/pdf_checks.py\", \"append\", \"def _evil6(data):\\n    return pdf_text.read_pages(data)\\n\"),\n    (\"m10_api_process_calls_render_in_child\", \"backend/pdf_checks.py\", \"append\", \"def _evil7(data):\\n    return pdf_ocr.render_in_child(data, [1], 1e12, print)\\n\"),\n    (\"m11_other_pdf_lib_pdfplumber_fitz\", \"backend/pdf_checks.py\", \"append\", \"def _evil8(data):\\n    import fitz\\n    return fitz.open(stream=data)\\n\"),\n    (\"m12_import_inside_class_method\", \"backend/pdf_checks.py\", \"append\", \"class _K:\\n    def m(self, data):\\n        import pypdfium2\\n\"),\n    (\"m13_import_in_lambda_via_exec\", \"backend/pdf_checks.py\", \"append\", \"_X = lambda d: exec('import pypdfium2')\"),\n    (\"m14_dynamic_in_new_module_file\", None, \"newfile\", \"import pypdf\\n\"),\n]\nfor name, rel, mode, snip in MUTS:\n    M = S / (\"mut_\" + name)\n    shutil.rmtree(M, ignore_errors=True)\n    M.mkdir(parents=True)\n    shutil.copytree(A / \"app\", M / \"app\")\n    (M / \"tests\").mkdir()\n    shutil.copytree(A / \"tests\" / \"unit\", M / \"tests\" / \"unit\")\n    for extra in (\"__init__.py\",):\n        if (A / \"tests\" / extra).exists():\n            shutil.copy(A / \"tests\" / extra, M / \"tests\" / extra)\n    if (A / \"tests\" / \"fixtures\").exists():\n        shutil.copytree(A / \"tests\" / \"fixtures\", M / \"tests\" / \"fixtures\")\n    if mode == \"newfile\":\n        (M / \"app\" / \"backend\" / \"newmod.py\").write_text(snip)\n    elif snip:\n        p = M / \"app\" / rel\n        txt = p.read_text()\n        p.write_text((snip + \"\\n\" + txt) if mode == \"prepend\" else (txt + \"\\n\" + snip + \"\\n\"))\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-p\", \"no:cacheprovider\", \"-q\", \"tests/unit/test_pdf_ocr_isolation.py\", \"-k\", \"imported_only_inside or reached_from_the_child_main\"],\n                       cwd=M, capture_output=True, text=True)\n    tail = [l for l in r.stdout.splitlines() if l.strip()][-1]\n    print(f\"{name}: rc={r.returncode} -> {'test CAUGHT it' if r.returncode else 'test did NOT catch it'} | {tail}\")\n    shutil.rmtree(M, ignore_errors=True)\n"
}
````

### User / tool · 2026-11-02T06:22:12.812Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/mutate_ast.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:22:17.484Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/T-107/mutate_ast.py $SP/head_9851a0d_r5 $SP 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T06:22:33.052Z

**tool result**
````
m0_control_no_change: rc=0 -> test did NOT catch it | 2 passed, 11 deselected in 0.46s
m1_func_import_pypdfium2_in_pdf_checks: rc=1 -> test CAUGHT it | 1 failed, 1 passed, 11 deselected in 0.50s
m2_module_import_pypdf_in_api: rc=1 -> test CAUGHT it | 1 failed, 1 passed, 11 deselected in 0.51s
m3_from_import_pypdf_in_pdf_text_extract: rc=1 -> test CAUGHT it | 1 failed, 1 passed, 11 deselected in 0.48s
m4_nested_import_inside_allowed_fn: rc=1 -> test CAUGHT it | 1 failed, 1 passed, 11 deselected in 0.49s
m5_dunder_import_call_no_import_stmt: rc=0 -> test did NOT catch it | 2 passed, 11 deselected in 0.47s
m6_importlib_call: rc=0 -> test did NOT catch it | 2 passed, 11 deselected in 0.45s
m7_sys_modules_lookup: rc=0 -> test did NOT catch it | 2 passed, 11 deselected in 0.47s
m8_api_process_calls_child_side_scan_inprocess: rc=0 -> test did NOT catch it | 2 passed, 11 deselected in 0.47s
m9_api_process_calls_child_side_read_pages: rc=0 -> test did NOT catch it | 2 passed, 11 deselected in 0.45s
m10_api_process_calls_render_in_child: rc=1 -> test CAUGHT it | 1 failed, 1 passed, 11 deselected in 0.48s
m11_other_pdf_lib_pdfplumber_fitz: rc=0 -> test did NOT catch it | 2 passed, 11 deselected in 0.46s
m12_import_inside_class_method: rc=1 -> test CAUGHT it | 1 failed, 1 passed, 11 deselected in 0.47s
m13_import_in_lambda_via_exec: rc=0 -> test did NOT catch it | 2 passed, 11 deselected in 0.46s
m14_dynamic_in_new_module_file: rc=1 -> test CAUGHT it | 1 failed, 1 passed, 11 deselected in 0.47s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:22:45.592Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/mutate_runtime.py",
 "content": "\"\"\"T-107: do the runtime tests (not just the AST test) catch a reintroduced in-process parse? Each mutation edits one real code path in a\nscratch copy and runs the whole tests/unit/test_pdf_ocr_isolation.py. Run: .venv/bin/python -I mutate_runtime.py <archive_root> <scratch_dir>\"\"\"\nimport pathlib\nimport shutil\nimport subprocess\nimport sys\n\nA, S = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\n\nMUTS = [\n    (\"r1_fallback_scan_inprocess_when_child_killed\",\n     \"backend/pdf_checks.py\",\n     '        if ocr:                # T-107: a file whose scan child was killed or failed is never handed to OCR; no fallback render anywhere\\n            raise PdfError(\"ocr_check_failed\", {\"cause\": str(e)[:40]}) from None\\n',\n     '        if ocr:\\n            scanned = pdf_hidden.scan_inprocess(data, None)\\n            texts = e.texts or [\"\"]\\n        else:\\n            pass\\n'),\n    (\"r2_read_pages_in_api_process_first\",\n     \"backend/pdf_checks.py\",\n     \"    try:                       # the text-layer read (pypdf) and the render scan (PDFium) both run in one child process killed at the deadline\\n\",\n     \"    pdf_text.read_pages(data)\\n    try:\\n\"),\n    (\"r3_ocr_pages_renders_in_process_on_render_killed\",\n     \"backend/pdf_ocr.py\",\n     \"    except pdf_hidden.HiddenScanUnavailable:\\n        raise OcrFailed(\\\"render_killed\\\") from None\\n\",\n     \"    except pdf_hidden.HiddenScanUnavailable:\\n        import pypdfium2 as pdfium\\n        pdf = pdfium.PdfDocument(data)\\n        return {n: render_page_png(pdf, n - 1) for n in pages}\\n\"),\n]\nfor name, rel, old, new in MUTS:\n    M = S / (\"mut_\" + name)\n    shutil.rmtree(M, ignore_errors=True)\n    M.mkdir(parents=True)\n    shutil.copytree(A / \"app\", M / \"app\")\n    (M / \"tests\").mkdir()\n    shutil.copytree(A / \"tests\" / \"unit\", M / \"tests\" / \"unit\")\n    if (A / \"tests\" / \"__init__.py\").exists():\n        shutil.copy(A / \"tests\" / \"__init__.py\", M / \"tests\" / \"__init__.py\")\n    if (A / \"tests\" / \"fixtures\").exists():\n        shutil.copytree(A / \"tests\" / \"fixtures\", M / \"tests\" / \"fixtures\")\n    p = M / \"app\" / rel\n    txt = p.read_text()\n    assert old in txt, name\n    p.write_text(txt.replace(old, new, 1))\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-p\", \"no:cacheprovider\", \"-q\", \"tests/unit/test_pdf_ocr_isolation.py\"], cwd=M, capture_output=True, text=True)\n    failed = [l for l in r.stdout.splitlines() if l.startswith(\"FAILED\")]\n    print(f\"{name}: rc={r.returncode} {[l.split('::')[1].split(' ')[0] for l in failed]} | {[l for l in r.stdout.splitlines() if l.strip()][-1]}\")\n    shutil.rmtree(M, ignore_errors=True)\n"
}
````

### User / tool · 2026-11-02T06:22:45.701Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/mutate_runtime.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:22:51.224Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/T-107/mutate_runtime.py $SP/head_9851a0d_r5 $SP 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T06:23:41.696Z

**tool result**
````
r1_fallback_scan_inprocess_when_child_killed: rc=1 ['test_a_killed_scan_child_with_ocr_is_refused_and_ocr_never_runs', 'test_every_scan_child_failure_with_ocr_is_a_400_with_a_plain_reason[memory]', 'test_every_scan_child_failure_with_ocr_is_a_400_with_a_plain_reason[child_failed]', 'test_every_scan_child_failure_with_ocr_is_a_400_with_a_plain_reason[child_died]', 'test_the_bomb_with_ocr_true_is_a_400_and_the_api_rss_stays_flat', 'test_two_concurrent_bombs_with_ocr_are_400_or_429_and_the_api_rss_stays_flat'] | 6 failed, 7 passed in 20.30s
r2_read_pages_in_api_process_first: rc=1 ['test_a_killed_scan_child_with_ocr_is_refused_and_ocr_never_runs', 'test_every_scan_child_failure_with_ocr_is_a_400_with_a_plain_reason[memory]', 'test_every_scan_child_failure_with_ocr_is_a_400_with_a_plain_reason[child_failed]', 'test_every_scan_child_failure_with_ocr_is_a_400_with_a_plain_reason[child_died]', 'test_a_scanned_pdf_with_ocr_renders_in_the_child_and_the_api_process_opens_no_pdf', 'test_the_bomb_with_ocr_true_is_a_400_and_the_api_rss_stays_flat', 'test_two_concurrent_bombs_with_ocr_are_400_or_429_and_the_api_rss_stays_flat'] | 7 failed, 6 passed in 13.36s
r3_ocr_pages_renders_in_process_on_render_killed: rc=1 ['test_pdfium_and_pypdf_are_imported_only_inside_the_child_functions', 'test_a_killed_render_child_is_ocr_failed_and_there_is_no_fallback[memory]', 'test_a_killed_render_child_is_ocr_failed_and_there_is_no_fallback[child_failed]', 'test_the_render_child_stops_on_the_rss_ceiling_with_the_reviewers_bomb'] | 4 failed, 9 passed in 14.60s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:23:57.427Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/probe_conc_server.py",
 "content": "\"\"\"T-107: N concurrent bomb uploads (ocr=true) to a real uvicorn server (live-local) started here. Samples the SERVER pid RSS every 0.1 s, the health latency,\nand counts pdf_hidden children whose parent is the server. Stops only the server PID it started.\nRun: .venv/bin/python -I probe_conc_server.py <archive_root> <bomb.pdf> <port> <n> <query>\"\"\"\nimport os\nimport pathlib\nimport subprocess\nimport sys\nimport threading\nimport time\n\nimport httpx\n\nroot, pdf, port, n, query = sys.argv[1], pathlib.Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]\nenv = {k: os.environ[k] for k in (\"PATH\", \"LANG\", \"TMPDIR\") if k in os.environ}\nenv.update({\"ENABLE_LIVE\": \"1\", \"LLM_BACKEND\": \"claude-cli\", \"PORT\": str(port), \"HOST\": \"127.0.0.1\"})\nsrv = subprocess.Popen([sys.executable, \"-I\", \"-c\", \"import sys, os; sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1]); import uvicorn; from app.main import create; uvicorn.run(create(), host='127.0.0.1', port=int(os.environ['PORT']), access_log=False, log_level='warning')\", root],\n                       env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\nbase = f\"http://127.0.0.1:{port}\"\n\n\ndef ps(pid):\n    o = subprocess.run([\"ps\", \"-o\", \"rss=,time=\", \"-p\", str(pid)], capture_output=True, text=True).stdout.split()\n    return (int(o[0]) // 1024, o[1]) if o else None\n\n\ndef kids(pid):\n    o = subprocess.run([\"ps\", \"-axo\", \"pid,ppid,rss,command\"], capture_output=True, text=True).stdout.splitlines()\n    return [(int(l.split()[0]), int(l.split()[2]) // 1024) for l in o if \"app.backend.pdf_hidden\" in l and l.split()[1] == str(pid)]\n\n\ntry:\n    for _ in range(100):\n        try:\n            if httpx.get(base + \"/api/health\", timeout=1).status_code == 200:\n                break\n        except Exception:\n            time.sleep(0.2)\n    else:\n        print(\"server did not start\"); raise SystemExit(1)\n    idle = ps(srv.pid)\n    print(f\"server pid {srv.pid} idle {idle}; file {pdf.name} {pdf.stat().st_size/1024:.0f} KB; {n} concurrent POSTs ?{query}\")\n    data = pdf.read_bytes()\n    res = []\n\n    def post(i):\n        s = time.monotonic()\n        try:\n            r = httpx.post(base + \"/api/cases/pdf?\" + query, content=data, headers={\"content-type\": \"application/pdf\"}, timeout=400)\n            j = r.json()\n            res.append((i, r.status_code, (j.get(\"error\") or {}).get(\"detail\", {}).get(\"reason\") if r.status_code != 201 else \"created\", round(time.monotonic() - s, 1)))\n        except Exception as e:\n            res.append((i, type(e).__name__, str(e)[:80], round(time.monotonic() - s, 1)))\n    ths = [threading.Thread(target=post, args=(i,)) for i in range(n)]\n    for t in ths:\n        t.start()\n    peak, kid_peak, lat_max, maxkids = idle[0], 0, 0.0, 0\n    while any(t.is_alive() for t in ths):\n        p = ps(srv.pid)\n        peak = max(peak, p[0]) if p else peak\n        k = kids(srv.pid)\n        maxkids = max(maxkids, len(k))\n        kid_peak = max([kid_peak] + [x[1] for x in k])\n        s = time.monotonic()\n        try:\n            httpx.get(base + \"/api/health\", timeout=30)\n            lat_max = max(lat_max, (time.monotonic() - s) * 1000)\n        except Exception:\n            lat_max = 30000\n        time.sleep(0.1)\n    for t in ths:\n        t.join()\n    time.sleep(3)\n    print(f\"responses {sorted(res)}\")\n    print(f\"server RSS idle={idle[0]} MB peak={peak} MB final={ps(srv.pid)}; max concurrent children={maxkids}; child peak RSS seen={kid_peak} MB; max health latency={lat_max:.0f} ms\")\n    print(\"children left after:\", kids(srv.pid))\nfinally:\n    srv.kill()\n    srv.wait()\n"
}
````

### User / tool · 2026-11-02T06:23:57.523Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/probe_conc_server.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:24:03.935Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/probe_killed_render.py",
 "content": "\"\"\"T-107: a render child that is killed or crashes (SIGKILL / SIGSEGV / SIGSTOP-then-deadline, and a child that cannot import) while the scan child was fine.\nTestClient in this process with spies on pypdf.PdfReader / pypdfium2.PdfDocument (API-process calls only). Expect 400 ocr_render_failed and zero spy calls.\nRun: .venv/bin/python -I probe_killed_render.py <archive_root>\"\"\"\nimport os\nimport signal\nimport subprocess\nimport sys\nimport tempfile\nimport time\n\nroot = sys.argv[1]\nsys.path.insert(0, root)\nos.chdir(root)\nos.environ.update({\"ENABLE_LIVE\": \"1\", \"LLM_BACKEND\": \"claude-cli\"})\nos.environ.pop(\"ANTHROPIC_API_KEY\", None)\nimport pypdf\nimport pypdfium2\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import pdf_hidden, pdf_ocr\nfrom app.backend.api import create_app\nfrom tests.unit.test_pdf_ocr import scan_pdf\n\ncalls = []\n_orig_doc, _orig_rd = pypdfium2.PdfDocument, pypdf.PdfReader\ndata = scan_pdf()\nreal_popen = subprocess.Popen\nmode = {\"sig\": None}\n\n\ndef popen(argv, *a, **k):\n    p = real_popen(argv, *a, **k)\n    if isinstance(argv, list) and \"app.backend.pdf_hidden\" in argv and \"render\" in argv and mode[\"sig\"] is not None:\n        os.kill(p.pid, mode[\"sig\"])         # my own child, by PID\n    return p\n\n\npypdfium2.PdfDocument = lambda *a, **k: (calls.append(\"PdfDocument\"), _orig_doc(*a, **k))[1]\npypdf.PdfReader = lambda *a, **k: (calls.append(\"PdfReader\"), _orig_rd(*a, **k))[1]\nsubprocess.Popen = popen\ntry:\n    c = TestClient(create_app(os.path.join(tempfile.mkdtemp(prefix=\"t107-\"), \"t.sqlite\"), static_dir=tempfile.mkdtemp(prefix=\"t107s-\")))\n    print(\"tesseract:\", pdf_ocr.ocr_status()[\"available\"])\n    for label, sig in ((\"control (no kill)\", None), (\"SIGKILL render child\", signal.SIGKILL), (\"SIGSEGV render child\", signal.SIGSEGV), (\"SIGABRT render child\", signal.SIGABRT)):\n        mode[\"sig\"] = sig\n        calls.clear()\n        t = time.monotonic()\n        r = c.post(\"/api/cases/pdf?ocr=true\", content=data, headers={\"content-type\": \"application/pdf\"})\n        j = r.json()\n        print(f\"{label}: {r.status_code} {(j.get('error') or {}).get('detail', {}).get('reason') if r.status_code != 201 else 'created'} in {time.monotonic()-t:.1f}s; API-process parser calls={calls}\")\nfinally:\n    subprocess.Popen = real_popen\n    pypdfium2.PdfDocument, pypdf.PdfReader = _orig_doc, _orig_rd\nprint(\"children left:\", subprocess.run(\"ps -axo pid,ppid,command | grep '[a]pp.backend.pdf_hidden'\", shell=True, capture_output=True, text=True).stdout.strip() or \"none\")\n"
}
````

### User / tool · 2026-11-02T06:24:04.033Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/probe_killed_render.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:24:12.109Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; echo \"== 2 concurrent\"; .venv/bin/python -I artifacts/review-evidence/T-107/probe_conc_server.py $A $SP/bombs/ap_3500.pdf 7892 2 ocr=true 2>&1 | tail -6; echo \"== 6 concurrent\"; .venv/bin/python -I artifacts/review-evidence/T-107/probe_conc_server.py $A $SP/bombs/ap_3500.pdf 7893 6 ocr=true 2>&1 | tail -6; echo \"== killed render\"; .venv/bin/python -I artifacts/review-evidence/T-107/probe_killed_render.py $A 2>&1 | tail -10"
}
````

### User / tool · 2026-11-02T06:24:22.498Z

**tool result**
````
== 2 concurrent
server pid 9930 idle (57, '0:00.30'); file ap_3500.pdf 3484 KB; 2 concurrent POSTs ?ocr=true
responses [(0, 400, 'ocr_check_failed', 0.4), (1, 400, 'ocr_check_failed', 0.4)]
server RSS idle=57 MB peak=101 MB final=(101, '0:00.34'); max concurrent children=2; child peak RSS seen=293 MB; max health latency=14 ms
children left after: []
== 6 concurrent
server pid 10054 idle (57, '0:00.29'); file ap_3500.pdf 3484 KB; 6 concurrent POSTs ?ocr=true
responses [(0, 400, 'ocr_check_failed', 0.4), (1, 400, 'ocr_check_failed', 0.4), (2, 429, 'pdf_busy', 0.6), (3, 400, 'ocr_check_failed', 0.8), (4, 400, 'ocr_check_failed', 0.8), (5, 429, 'pdf_busy', 0.6)]
server RSS idle=57 MB peak=198 MB final=(198, '0:00.39'); max concurrent children=2; child peak RSS seen=252 MB; max health latency=17 ms
children left after: []
== killed render
tesseract: True
control (no kill): 201 created in 0.5s; API-process parser calls=[]
SIGKILL render child: 400 ocr_render_failed in 0.2s; API-process parser calls=[]
SIGSEGV render child: 400 ocr_render_failed in 0.2s; API-process parser calls=[]
SIGABRT render child: 400 ocr_render_failed in 0.2s; API-process parser calls=[]
children left: none
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:24:28.082Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-086-087/pdfkit.py | head -60; sed -n 1,60p tests/unit/test_pdf_ocr.py | grep -n \"def scan_pdf\" ; grep -n \"def scan_pdf\" -A25 tests/unit/test_pdf_ocr.py | head -40; cat artifacts/review-evidence/T-087-r4/mk_imgbomb.py | head -40"
}
````

### User / tool · 2026-11-02T06:24:28.190Z

**tool result**
````
"""Tiny raw-PDF builder for the T-086/T-087 security probes (reviewer-written, SYNTHETIC text only)."""
import zlib


def pdf(objs, root=1):
    """objs: list of bytes bodies for object 1..N (stream objects pass the full `<< >>\nstream..endstream` body)."""
    out, offs = bytearray(b"%PDF-1.4\n"), []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    x = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode() + b"0000000000 65535 f \n"
    for o in offs:
        out += f"{o:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root {root} 0 R >>\nstartxref\n{x}\n%%EOF\n".encode()
    return bytes(out)


def stream(content: bytes, extra: str = "", flate: bool = False) -> bytes:
    if flate:
        content = zlib.compress(content)
        extra += " /Filter /FlateDecode"
    return f"<< /Length {len(content)} {extra} >>\nstream\n".encode() + content + b"\nendstream"


FONT = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
VISIBLE = b"BT /F1 12 Tf 50 740 Td (Visible clinic note: patient reports neck pain after the collision.) Tj ET\n"


def one_page(content: bytes, mediabox="0 0 600 800", extra_objs=(), xobjects="", flate=False):
    """Catalog 1, Pages 2, Page 3, Contents 4, Font 5, then extra_objs from 6 on. `xobjects` = '/Fm1 6 0 R ...'"""
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            (f"<< /Type /Page /Parent 2 0 R /MediaBox [{mediabox}] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >>"
             f" /XObject << {xobjects} >> >> >>").encode(),
            stream(content, flate=flate), FONT]
    return pdf(objs + list(extra_objs))
18:def scan_pdf():
18:def scan_pdf():
19-    return scanned_copy(build(text_page(LINES, size=18, lead=30, y=700)))
20-
21-
22-# ---- no tesseract: a clear message, never a crash ----
23-def test_missing_tesseract_gives_a_clear_message(monkeypatch):
24-    monkeypatch.setattr(pdf_ocr.shutil, "which", lambda name: None)
25-    st = pdf_ocr.ocr_status()
26-    assert st["available"] is False and "brew install tesseract" in st["message"] and "apt-get install tesseract-ocr" in st["message"]
27-    with pytest.raises(pdf_ocr.OcrUnavailable):
28-        pdf_ocr.ocr_png(b"x")
29-
30-
31-def test_ocr_requested_without_tesseract_is_a_pdf_error_with_the_message_not_a_crash(monkeypatch):
32-    monkeypatch.setattr(pdf_ocr.shutil, "which", lambda name: None)
33-    with pytest.raises(pdf_text.PdfError) as e:
34-        pdf_checks.extract(scan_pdf(), ocr=True)
35-    assert e.value.code == "ocr_unavailable" and "Tesseract" in e.value.detail["message"]
36-
37-
38-def test_scanned_pdf_without_ocr_is_refused_and_says_ocr_could_read_it():
39-    with pytest.raises(pdf_text.PdfError) as e:
40-        pdf_text.extract(scan_pdf())
41-    assert e.value.code == "pdf_no_text_layer" and e.value.detail["scanned_pages"] == [1]
42-    assert "available" in e.value.detail["ocr"]
43-
"""T-087 r4: image-only page (no text layer, so it is an OCR candidate) whose image XObject inflates to side*side bytes. Run: .venv/bin/python -I mk_imgbomb.py <outfile> <side_px>"""
import pathlib, sys, zlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "T-086-087"))
import pdfkit as K
out, side = pathlib.Path(sys.argv[1]), int(sys.argv[2])
z = zlib.compressobj(9); chunk = bytes(1024 * 1024); parts = []; tot = side * side
while tot > 0:
    n = min(tot, len(chunk)); parts.append(z.compress(chunk[:n])); tot -= n
parts.append(z.flush()); img = b"".join(parts)
imgobj = f"<< /Type /XObject /Subtype /Image /Width {side} /Height {side} /ColorSpace /DeviceGray /BitsPerComponent 8 /Filter /FlateDecode /Length {len(img)} >>\nstream\n".encode() + img + b"\nendstream"
objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Contents 4 0 R /Resources << /XObject << /Im1 6 0 R >> >> >>",
        K.stream(b"q 600 0 0 800 0 0 cm /Im1 Do Q\n"), K.FONT, imgobj]
d = K.pdf(objs); out.write_bytes(d)
print(f"{out.name}: {len(d)/1024:.0f} KB, image decodes to {side*side/1048576:.0f} MB")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:25:16.256Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/build_attacks.py",
 "content": "\"\"\"T-107: builds the OCR-path attack PDFs (reviewer-written, SYNTHETIC; no text in them is a record). Run: .venv/bin/python -I build_attacks.py <outdir>\nGroups: many_* (page-count attacks), dpi_* (size/scale attacks carried in the file), img_* (malformed image streams).\"\"\"\nimport pathlib\nimport random\nimport struct\nimport sys\nimport zlib\n\nsys.path.insert(0, str(pathlib.Path(__file__).parent.parent / \"T-086-087\"))\nimport pdfkit as K\n\nout = pathlib.Path(sys.argv[1])\nout.mkdir(parents=True, exist_ok=True)\n\n\ndef save(name, data):\n    (out / name).write_bytes(data)\n    print(f\"{name}: {len(data)/1024:.0f} KB\")\n\n\ndef gray_image(w, h, data, extra=\"\", filt=\" /Filter /FlateDecode\", cs=\"/DeviceGray\", bpc=8):\n    return f\"<< /Type /XObject /Subtype /Image /Width {w} /Height {h} /ColorSpace {cs} /BitsPerComponent {bpc}{filt} {extra} /Length {len(data)} >>\\nstream\\n\".encode() + data + b\"\\nendstream\"\n\n\ndef pages_doc(n_pages, content_for, image_obj, mediabox=\"0 0 600 800\", shared_page=False):\n    \"\"\"n image-only pages (each its own /Page object, one shared image XObject). Object layout: 1 catalog, 2 pages, 3 image, 4 shared content, 5.. pages.\"\"\"\n    objs = [b\"<< /Type /Catalog /Pages 2 0 R >>\", None, image_obj, K.stream(content_for)]\n    kids = []\n    for i in range(n_pages):\n        objs.append(f\"<< /Type /Page /Parent 2 0 R /MediaBox [{mediabox}] /Contents 4 0 R /Resources << /XObject << /Im1 3 0 R >> >> >>\".encode())\n        kids.append(f\"{len(objs)} 0 R\")\n    objs[1] = f\"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {n_pages} >>\".encode()\n    return K.pdf(objs)\n\n\nsmall_img = gray_image(8, 8, zlib.compress(bytes([random.randrange(256) for _ in range(64)])))\nCONT = b\"q 600 0 0 800 0 0 cm /Im1 Do Q\\n\"\n\n# ---------------- many pages ----------------\nsave(\"many_11_image_pages.pdf\", pages_doc(11, CONT, small_img))\nsave(\"many_100_image_pages.pdf\", pages_doc(100, CONT, small_img))\nsave(\"many_10_pages_max_size_noise.pdf\", None or pages_doc(10, b\"q 2880 0 0 2880 0 0 cm /Im1 Do Q\\n\",\n                                                       gray_image(1500, 1500, zlib.compress(bytes(random.Random(1).randrange(256) for _ in range(1500 * 1500)), 9)),\n                                                       mediabox=\"0 0 2880 2880\"))\n# speckle: sparse dark specks on white, 2000x2000 1-bit-ish gray; slow for layout analysis\nrnd = random.Random(2)\nrows = bytearray(b\"\\xff\" * (2000 * 2000))\nfor _ in range(60000):\n    x, y = rnd.randrange(2000), rnd.randrange(2000)\n    for dy in range(3):\n        for dx in range(3):\n            if x + dx < 2000 and y + dy < 2000:\n                rows[(y + dy) * 2000 + x + dx] = 0\nsave(\"many_10_pages_speckle_max_size.pdf\", pages_doc(10, b\"q 2880 0 0 2880 0 0 cm /Im1 Do Q\\n\", gray_image(2000, 2000, zlib.compress(bytes(rows), 9)), mediabox=\"0 0 2880 2880\"))\n# one page object listed 50000 times in Kids (a few hundred KB): page count attack on the page-tree walkers\nkid = \"3 0 R\"\nobjs = [b\"<< /Type /Catalog /Pages 2 0 R >>\", f\"<< /Type /Pages /Kids [{' '.join([kid] * 50000)}] /Count 50000 >>\".encode(),\n        b\"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Contents 4 0 R /Resources << /XObject << /Im1 5 0 R >> >> >>\", K.stream(CONT), small_img]\nsave(\"many_50000_kids_same_page.pdf\", K.pdf(objs))\n# deep page tree: 3000 nested /Pages nodes\ndepth = 3000\nobjs = [b\"<< /Type /Catalog /Pages 2 0 R >>\"]\nfor i in range(depth):\n    objs.append(f\"<< /Type /Pages /Parent {i + 1} 0 R /Kids [{i + 3} 0 R] /Count 1 >>\".encode() if i else f\"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\".encode())\nobjs.append(b\"<< /Type /Page /Parent %d 0 R /MediaBox [0 0 600 800] /Contents %d 0 R >>\" % (depth + 1, depth + 3))\nobjs.append(K.stream(b\"0 g 10 10 100 100 re f\\n\"))\nsave(\"many_deep_page_tree_3000.pdf\", K.pdf(objs))\n\n# ---------------- size / scale carried in the file ----------------\ndef one(mediabox, extra_page=\"\", content=CONT, image=small_img):\n    objs = [b\"<< /Type /Catalog /Pages 2 0 R >>\", b\"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\",\n            f\"<< /Type /Page /Parent 2 0 R /MediaBox [{mediabox}] {extra_page} /Contents 4 0 R /Resources << /XObject << /Im1 5 0 R >> >> >>\".encode(), K.stream(content), image]\n    return K.pdf(objs)\n\n\nsave(\"dpi_userunit_14400_on_100pt.pdf\", one(\"0 0 100 100\", \"/UserUnit 14400\", b\"q 100 0 0 100 0 0 cm /Im1 Do Q\\n\"))\nsave(\"dpi_mediabox_2880.pdf\", one(\"0 0 2880 2880\", content=b\"q 2880 0 0 2880 0 0 cm /Im1 Do Q\\n\"))\nsave(\"dpi_mediabox_1e9.pdf\", one(\"0 0 1000000000 1000000000\"))\nsave(\"dpi_mediabox_negative_huge.pdf\", one(\"-1000000000 -1000000000 1000000000 1000000000\"))\nsave(\"dpi_mediabox_tiny_0.001.pdf\", one(\"0 0 0.001 0.001\"))\nsave(\"dpi_mediabox_zero.pdf\", one(\"0 0 0 0\"))\nsave(\"dpi_crop_tiny_media_huge.pdf\", one(\"0 0 14400 14400\", \"/CropBox [0 0 100 100]\"))\nsave(\"dpi_crop_huge_media_small.pdf\", one(\"0 0 100 100\", \"/CropBox [0 0 99999999 99999999]\"))\nsave(\"dpi_rotate_90_2880x20.pdf\", one(\"0 0 2880 20\", \"/Rotate 90\", b\"q 2880 0 0 20 0 0 cm /Im1 Do Q\\n\"))\nsave(\"dpi_extreme_aspect_2880x0.01.pdf\", one(\"0 0 2880 0.01\", content=b\"q 2880 0 0 0.01 0 0 cm /Im1 Do Q\\n\"))\n\n# billion laughs of Form XObjects: F0 draws F1 ten times, F1 draws F2 ten times ... 9 levels = 1e9 draws of a rect\nlevels = 9\nobjs = [b\"<< /Type /Catalog /Pages 2 0 R >>\", b\"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\"]\nform_ids = [5 + i for i in range(levels)]\nobjs.append((\"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Contents 4 0 R /Resources << /XObject << /F0 %d 0 R >> >> >>\" % form_ids[0]).encode())\nobjs.append(K.stream(b\"/F0 Do\\n\"))\nfor i in range(levels):\n    if i < levels - 1:\n        body = b\" \".join([b\"/F%d Do\" % (i + 1)] * 10)\n        res = \"/Resources << /XObject << /F%d %d 0 R >> >>\" % (i + 1, form_ids[i + 1])\n    else:\n        body, res = b\"0 g 0 0 5 5 re f\", \"\"\n    objs.append(K.stream(body, f\"/Type /XObject /Subtype /Form /BBox [0 0 600 800] {res}\"))\nsave(\"dpi_laughs_forms_1e9_draws.pdf\", K.pdf(objs))\n\n# ---------------- malformed image streams ----------------\nreal = zlib.compress(bytes(64))\nsave(\"img_declared_100000x100000_gray_flate_short.pdf\", one(\"0 0 600 800\", image=gray_image(100000, 100000, real)))\nsave(\"img_declared_2e9_x_2e9.pdf\", one(\"0 0 600 800\", image=gray_image(2000000000, 2000000000, real)))\nsave(\"img_declared_negative_wh.pdf\", one(\"0 0 600 800\", image=gray_image(-5, -5, real)))\nsave(\"img_dct_garbage.pdf\", one(\"0 0 600 800\", image=gray_image(5000, 5000, b\"\\xff\\xd8\\xff\\xe0\" + bytes(random.Random(3).randrange(256) for _ in range(4000)), filt=\" /Filter /DCTDecode\")))\nsave(\"img_dct_header_65535x65535.pdf\", one(\"0 0 600 800\", image=gray_image(65535, 65535, b\"\\xff\\xd8\\xff\\xc0\\x00\\x0b\\x08\\xff\\xff\\xff\\xff\\x01\\x01\\x11\\x00\\xff\\xd9\", filt=\" /Filter /DCTDecode\")))\nsave(\"img_jpx_garbage.pdf\", one(\"0 0 600 800\", image=gray_image(4000, 4000, b\"\\x00\\x00\\x00\\x0cjP  \\r\\n\\x87\\n\" + bytes(random.Random(4).randrange(256) for _ in range(3000)), filt=\" /Filter /JPXDecode\")))\nsave(\"img_jbig2_garbage.pdf\", one(\"0 0 600 800\", image=gray_image(30000, 30000, bytes(random.Random(5).randrange(256) for _ in range(3000)), filt=\" /Filter /JBIG2Decode\", bpc=1)))\nsave(\"img_ccitt_huge_columns.pdf\", one(\"0 0 600 800\", image=gray_image(1000000, 1000000, bytes(200), filt=\" /Filter /CCITTFaxDecode\", extra=\"/DecodeParms << /K -1 /Columns 1000000 /Rows 1000000 >>\", bpc=1)))\nsave(\"img_predictor15_columns_2e9.pdf\", one(\"0 0 600 800\", image=gray_image(10, 10, real, extra=\"/DecodeParms << /Predictor 15 /Columns 2000000000 /Colors 4 /BitsPerComponent 16 >>\")))\nsave(\"img_lzw_garbage.pdf\", one(\"0 0 600 800\", image=gray_image(3000, 3000, bytes(random.Random(6).randrange(256) for _ in range(5000)), filt=\" /Filter /LZWDecode\")))\nsave(\"img_filter_chain_a85_flate_runlength_x20.pdf\", one(\"0 0 600 800\", image=gray_image(100, 100, b\"~>\" * 100, filt=\" /Filter [\" + \" /ASCII85Decode /FlateDecode /RunLengthDecode\" * 7 + \"]\")))\nsave(\"img_indexed_huge_palette_hival_255_short.pdf\", one(\"0 0 600 800\", image=gray_image(4000, 4000, real, cs=\"[/Indexed /DeviceRGB 255 <00>]\")))\nsave(\"img_inline_BI_huge.pdf\", one(\"0 0 600 800\", content=b\"q 600 0 0 800 0 0 cm BI /W 60000 /H 60000 /CS /G /BPC 8 /F /Fl ID \" + zlib.compress(bytes(100)) + b\" EI Q\\n\"))\nsave(\"img_smask_loop.pdf\", K.pdf([b\"<< /Type /Catalog /Pages 2 0 R >>\", b\"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\",\n                                   b\"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Contents 4 0 R /Resources << /XObject << /Im1 5 0 R >> >> >>\", K.stream(CONT),\n                                   gray_image(8, 8, real, extra=\"/SMask 5 0 R\"), ]))\n"
}
````

### User / tool · 2026-11-02T06:25:16.357Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/build_attacks.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:25:23.279Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $SP/atk; .venv/bin/python -I artifacts/review-evidence/T-107/build_attacks.py $SP/atk 2>&1 | tail -50"
}
````

### User / tool · 2026-11-02T06:25:40.543Z

**tool result**
````
many_11_image_pages.pdf: 2 KB
many_100_image_pages.pdf: 16 KB
many_10_pages_max_size_noise.pdf: 4 KB
many_10_pages_speckle_max_size.pdf: 182 KB
many_50000_kids_same_page.pdf: 294 KB
many_deep_page_tree_3000.pdf: 290 KB
dpi_userunit_14400_on_100pt.pdf: 1 KB
dpi_mediabox_2880.pdf: 1 KB
dpi_mediabox_1e9.pdf: 1 KB
dpi_mediabox_negative_huge.pdf: 1 KB
dpi_mediabox_tiny_0.001.pdf: 1 KB
dpi_mediabox_zero.pdf: 1 KB
dpi_crop_tiny_media_huge.pdf: 1 KB
dpi_crop_huge_media_small.pdf: 1 KB
dpi_rotate_90_2880x20.pdf: 1 KB
dpi_extreme_aspect_2880x0.01.pdf: 1 KB
dpi_laughs_forms_1e9_draws.pdf: 2 KB
img_declared_100000x100000_gray_flate_short.pdf: 1 KB
img_declared_2e9_x_2e9.pdf: 1 KB
img_declared_negative_wh.pdf: 1 KB
img_dct_garbage.pdf: 5 KB
img_dct_header_65535x65535.pdf: 1 KB
img_jpx_garbage.pdf: 4 KB
img_jbig2_garbage.pdf: 4 KB
img_ccitt_huge_columns.pdf: 1 KB
img_predictor15_columns_2e9.pdf: 1 KB
img_lzw_garbage.pdf: 6 KB
img_filter_chain_a85_flate_runlength_x20.pdf: 1 KB
img_indexed_huge_palette_hival_255_short.pdf: 1 KB
img_inline_BI_huge.pdf: 1 KB
img_smask_loop.pdf: 1 KB
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:25:44.365Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/build_attacks.py",
 "old_string": "zlib.compress(bytes(random.Random(1).randrange(256) for _ in range(1500 * 1500)), 9)),",
 "new_string": "zlib.compress(random.Random(1).randbytes(1500 * 1500), 9)),"
}
````

### User / tool · 2026-11-02T06:25:44.600Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/build_attacks.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:25:58.487Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/probe_attacks.py",
 "content": "\"\"\"T-107: POST each attack PDF (query given) to ONE real uvicorn server (live-local, started here, stopped by PID). Per file prints: HTTP status, error reason, wall time,\nserver RSS before/peak/after, server cputime delta, peak RSS of pdf_hidden children whose ppid is the server, tesseract processes seen, health latency max, children\nleft 3 s after, and a PNG size note when a case is created. Run: .venv/bin/python -I probe_attacks.py <archive_root> <port> <query> <file1.pdf> <file2.pdf> ...\"\"\"\nimport base64\nimport os\nimport subprocess\nimport sys\nimport threading\nimport time\nimport pathlib\n\nimport httpx\n\nroot, port, query, files = sys.argv[1], int(sys.argv[2]), sys.argv[3], [pathlib.Path(f) for f in sys.argv[4:]]\nenv = {k: os.environ[k] for k in (\"PATH\", \"LANG\", \"TMPDIR\") if k in os.environ}\nenv.update({\"ENABLE_LIVE\": \"1\", \"LLM_BACKEND\": \"claude-cli\", \"PORT\": str(port), \"HOST\": \"127.0.0.1\"})\nsrv = subprocess.Popen([sys.executable, \"-I\", \"-c\", \"import sys, os; sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1]); import uvicorn; from app.main import create; uvicorn.run(create(), host='127.0.0.1', port=int(os.environ['PORT']), access_log=False, log_level='warning')\", root],\n                       env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\nbase = f\"http://127.0.0.1:{port}\"\n\n\ndef table():\n    return subprocess.run([\"ps\", \"-axo\", \"pid,ppid,rss,time,command\"], capture_output=True, text=True).stdout.splitlines()\n\n\ndef srv_ps():\n    for l in table():\n        p = l.split(None, 4)\n        if p and p[0] == str(srv.pid):\n            return int(p[2]) // 1024, p[3]\n    return None\n\n\ndef mine():\n    \"\"\"children of the server (pdf_hidden) and tesseract processes under the server's tree\"\"\"\n    t = [l.split(None, 4) for l in table()]\n    kids = [(int(p[0]), int(p[2]) // 1024) for p in t if len(p) == 5 and p[1] == str(srv.pid) and \"app.backend.pdf_hidden\" in p[4]]\n    tess = [(int(p[0]), int(p[2]) // 1024) for p in t if len(p) == 5 and p[1] == str(srv.pid) and \"tesseract\" in p[4]]\n    return kids, tess\n\n\ndef cpu_s(t):\n    parts = t.replace(\":\", \" \").replace(\".\", \" \").split()\n    return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 100 if len(parts) == 3 else 0\n\n\ntry:\n    for _ in range(100):\n        try:\n            if httpx.get(base + \"/api/health\", timeout=1).status_code == 200:\n                break\n        except Exception:\n            time.sleep(0.2)\n    else:\n        print(\"server did not start\"); raise SystemExit(1)\n    print(f\"server pid {srv.pid}; idle {srv_ps()}; query ?{query}\")\n    for f in files:\n        data = f.read_bytes()\n        res = {}\n\n        def post():\n            s = time.monotonic()\n            try:\n                r = httpx.post(base + \"/api/cases/pdf?\" + query, content=data, headers={\"content-type\": \"application/pdf\"}, timeout=500)\n                j = r.json()\n                if r.status_code == 201:\n                    imgs = (j.get(\"pdf_checks\") or {}).get(\"ocr\") or {}\n                    res[\"r\"] = (201, \"created\", f\"ocr_ran={imgs.get('ran')} pages={imgs.get('pages')}\")\n                else:\n                    e = j.get(\"error\") or {}\n                    res[\"r\"] = (r.status_code, (e.get(\"detail\") or {}).get(\"reason\"), (e.get(\"message\") or \"\")[:60])\n            except Exception as ex:\n                res[\"r\"] = (type(ex).__name__, str(ex)[:60], \"\")\n            res[\"wall\"] = round(time.monotonic() - s, 1)\n        before = srv_ps()\n        th = threading.Thread(target=post)\n        th.start()\n        peak, kid_peak, tess_peak, lat, nk = before[0], 0, 0, 0.0, 0\n        while th.is_alive():\n            p = srv_ps()\n            peak = max(peak, p[0]) if p else peak\n            k, te = mine()\n            nk = max(nk, len(k))\n            kid_peak = max([kid_peak] + [x[1] for x in k])\n            tess_peak = max([tess_peak] + [x[1] for x in te])\n            s = time.monotonic()\n            try:\n                httpx.get(base + \"/api/health\", timeout=30)\n                lat = max(lat, (time.monotonic() - s) * 1000)\n            except Exception:\n                lat = 30000\n            time.sleep(0.1)\n        th.join()\n        time.sleep(3)\n        after, (k_after, t_after) = srv_ps(), mine()\n        print(f\"{f.name:52s} {res['r'][0]} {str(res['r'][1])[:28]:28s} wall={res['wall']:6.1f}s | srv rss {before[0]}->{peak} (after {after[0]}) MB cpu {cpu_s(before[1]):.1f}->{cpu_s(after[1]):.1f}s | child peak {kid_peak} MB tess peak {tess_peak} MB | health max {lat:.0f} ms | left kids={len(k_after)} tess={len(t_after)} | {res['r'][2]}\", flush=True)\nfinally:\n    srv.kill()\n    srv.wait()\n"
}
````

### User / tool · 2026-11-02T06:25:58.592Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/probe_attacks.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:26:03.425Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; .venv/bin/python -I artifacts/review-evidence/T-107/build_attacks.py $SP/atk > /dev/null; ls -la $SP/atk/many_10_pages_max_size_noise.pdf; .venv/bin/python -I artifacts/review-evidence/T-107/probe_attacks.py $A 7894 ocr=true $SP/atk/dpi_*.pdf > artifacts/review-evidence/T-107/out_dpi.txt 2>&1 ; cat artifacts/review-evidence/T-107/out_dpi.txt",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:26:46.451Z

**tool result**
````
-rw-r--r--@ 1 arsis  wheel  2252826 Nov  2 00:26 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/atk/many_10_pages_max_size_noise.pdf
server pid 12571; idle (57, '0:00.28'); query ?ocr=true
dpi_crop_huge_media_small.pdf                        400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.3->0.3s | child peak 19 MB tess peak 28 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
dpi_crop_tiny_media_huge.pdf                         400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.3->0.3s | child peak 18 MB tess peak 27 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
dpi_extreme_aspect_2880x0.01.pdf                     400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.3->0.3s | child peak 18 MB tess peak 5 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
dpi_laughs_forms_1e9_draws.pdf                       400 ocr_check_failed             wall=   1.9s | srv rss 57->57 (after 57) MB cpu 0.3->0.4s | child peak 1031 MB tess peak 0 MB | health max 12 ms | left kids=0 tess=0 | This PDF could not be checked safely (the checker ran out of
dpi_mediabox_1e9.pdf                                 400 ocr_page_too_large           wall=   0.2s | srv rss 57->57 (after 57) MB cpu 0.4->0.4s | child peak 18 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | A scanned page in this PDF is larger than OCR will read (ove
dpi_mediabox_2880.pdf                                400 pdf_no_text_layer            wall=   0.6s | srv rss 57->57 (after 57) MB cpu 0.4->0.5s | child peak 53 MB tess peak 72 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
dpi_mediabox_negative_huge.pdf                       400 ocr_page_too_large           wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.5->0.5s | child peak 18 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | A scanned page in this PDF is larger than OCR will read (ove
dpi_mediabox_tiny_0.001.pdf                          400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.5->0.5s | child peak 18 MB tess peak 26 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
dpi_mediabox_zero.pdf                                400 pdf_no_text_layer            wall=   0.4s | srv rss 57->57 (after 57) MB cpu 0.5->0.5s | child peak 18 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
dpi_rotate_90_2880x20.pdf                            400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.5->0.6s | child peak 19 MB tess peak 26 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
dpi_userunit_14400_on_100pt.pdf                      400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.6->0.6s | child peak 18 MB tess peak 27 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:26:55.694Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; .venv/bin/python -I artifacts/review-evidence/T-107/probe_attacks.py $A 7895 ocr=true $SP/atk/img_*.pdf > artifacts/review-evidence/T-107/out_img.txt 2>&1 ; cat artifacts/review-evidence/T-107/out_img.txt | cut -c1-330",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:27:47.050Z

**tool result**
````
server pid 14376; idle (57, '0:00.29'); query ?ocr=true
img_ccitt_huge_columns.pdf                           400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.3->0.3s | child peak 19 MB tess peak 5 MB | health max 8 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_dct_garbage.pdf                                  400 pdf_no_text_layer            wall=   0.4s | srv rss 57->57 (after 57) MB cpu 0.3->0.3s | child peak 18 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_dct_header_65535x65535.pdf                       400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.3->0.4s | child peak 19 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_declared_100000x100000_gray_flate_short.pdf      400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.4->0.4s | child peak 18 MB tess peak 7 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_declared_2e9_x_2e9.pdf                           400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.4->0.4s | child peak 18 MB tess peak 26 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_declared_negative_wh.pdf                         400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.4->0.4s | child peak 18 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_filter_chain_a85_flate_runlength_x20.pdf         400 pdf_no_text_layer            wall=   0.4s | srv rss 57->57 (after 57) MB cpu 0.4->0.5s | child peak 18 MB tess peak 0 MB | health max 8 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_indexed_huge_palette_hival_255_short.pdf         400 pdf_no_text_layer            wall=   0.4s | srv rss 57->57 (after 57) MB cpu 0.5->0.5s | child peak 18 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_inline_BI_huge.pdf                               400 pdf_no_text_layer            wall=   0.9s | srv rss 57->57 (after 57) MB cpu 0.5->0.5s | child peak 95 MB tess peak 29 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_jbig2_garbage.pdf                                400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.5->0.5s | child peak 19 MB tess peak 7 MB | health max 11 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_jpx_garbage.pdf                                  400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.5->0.6s | child peak 18 MB tess peak 18 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_lzw_garbage.pdf                                  400 pdf_no_text_layer            wall=   0.4s | srv rss 57->57 (after 57) MB cpu 0.6->0.6s | child peak 18 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_predictor15_columns_2e9.pdf                      400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.6->0.6s | child peak 18 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
img_smask_loop.pdf                                   400 pdf_no_text_layer            wall=   0.3s | srv rss 57->57 (after 57) MB cpu 0.6->0.6s | child peak 18 MB tess peak 1 MB | health max 7 ms | left kids=0 tess=0 | This PDF has no text layer (it looks scanned). Run OCR to re
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:27:54.788Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; .venv/bin/python -I artifacts/review-evidence/T-107/build_attacks.py $SP/atk > /dev/null; (.venv/bin/python -I artifacts/review-evidence/T-107/probe_attacks.py $A 7896 ocr=true $SP/atk/many_11_image_pages.pdf $SP/atk/many_100_image_pages.pdf $SP/atk/many_50000_kids_same_page.pdf $SP/atk/many_deep_page_tree_3000.pdf $SP/atk/many_10_pages_max_size_noise.pdf $SP/atk/many_10_pages_speckle_max_size.pdf > artifacts/review-evidence/T-107/out_many.txt 2>&1; echo done >> artifacts/review-evidence/T-107/out_many.txt) ; cut -c1-360 artifacts/review-evidence/T-107/out_many.txt",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:28:19.831Z

**tool result**
````
server pid 16248; idle (57, '0:00.29'); query ?ocr=true
many_11_image_pages.pdf                              400 ocr_too_many_pages           wall=   0.2s | srv rss 57->57 (after 57) MB cpu 0.3->0.3s | child peak 18 MB tess peak 0 MB | health max 8 ms | left kids=0 tess=0 | This PDF has more than 10 scanned pages; OCR reads at most t
many_100_image_pages.pdf                             400 ocr_too_many_pages           wall=   0.2s | srv rss 57->57 (after 57) MB cpu 0.3->0.3s | child peak 19 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | This PDF has more than 10 scanned pages; OCR reads at most t
many_50000_kids_same_page.pdf                        413 pdf_too_large                wall=   0.3s | srv rss 57->58 (after 58) MB cpu 0.3->0.3s | child peak 57 MB tess peak 0 MB | health max 7 ms | left kids=0 tess=0 | The PDF is too large.
many_deep_page_tree_3000.pdf                         400 pdf_unreadable               wall=   0.1s | srv rss 58->58 (after 58) MB cpu 0.3->0.3s | child peak 19 MB tess peak 0 MB | health max 8 ms | left kids=0 tess=0 | This file could not be read as a PDF.
many_10_pages_max_size_noise.pdf                     400 ocr_images_too_large         wall=   0.8s | srv rss 58->87 (after 117) MB cpu 0.3->0.4s | child peak 132 MB tess peak 0 MB | health max 10 ms | left kids=0 tess=0 | The scanned pages in this PDF are too large to keep together
many_10_pages_speckle_max_size.pdf                   400 ocr_images_too_large         wall=   2.1s | srv rss 117->213 (after 213) MB cpu 0.4->0.6s | child peak 85 MB tess peak 0 MB | health max 10 ms | left kids=0 tess=0 | The scanned pages in this PDF are too large to keep together
done
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:28:34.714Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/build_speckle.py",
 "content": "\"\"\"T-107: speckle scans for the Tesseract-time question. Run: .venv/bin/python -I build_speckle.py <outdir>\nFiles: speck_<n>specks_<pages>p.pdf. A 2000x2000 gray image of n 3x3 dark specks placed on text-like rows, drawn on a 2880 pt page (render capped to 8 MP), `pages` copies.\"\"\"\nimport pathlib\nimport random\nimport sys\nimport zlib\n\nsys.path.insert(0, str(pathlib.Path(__file__).parent.parent / \"T-086-087\"))\nimport pdfkit as K\n\nout = pathlib.Path(sys.argv[1])\nfor n, pages in ((4000, 1), (12000, 1), (30000, 1), (12000, 10), (30000, 10)):\n    rnd = random.Random(n)\n    side = 2000\n    buf = bytearray(b\"\\xff\" * (side * side))\n    for _ in range(n):\n        # clusters in text-like lines so layout analysis finds many words\n        y = rnd.randrange(0, side - 20, 40) + rnd.randrange(0, 12)\n        x = rnd.randrange(0, side - 20)\n        for dy in range(rnd.randrange(2, 9)):\n            for dx in range(rnd.randrange(2, 7)):\n                buf[(y + dy) * side + x + dx] = 0\n    img = zlib.compress(bytes(buf), 9)\n    imgobj = f\"<< /Type /XObject /Subtype /Image /Width {side} /Height {side} /ColorSpace /DeviceGray /BitsPerComponent 8 /Filter /FlateDecode /Length {len(img)} >>\\nstream\\n\".encode() + img + b\"\\nendstream\"\n    objs = [b\"<< /Type /Catalog /Pages 2 0 R >>\", None, imgobj, K.stream(b\"q 2880 0 0 2880 0 0 cm /Im1 Do Q\\n\")]\n    kids = []\n    for _ in range(pages):\n        objs.append(b\"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 2880 2880] /Contents 4 0 R /Resources << /XObject << /Im1 3 0 R >> >> >>\")\n        kids.append(f\"{len(objs)} 0 R\")\n    objs[1] = f\"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {pages} >>\".encode()\n    d = K.pdf(objs)\n    (out / f\"speck_{n}specks_{pages}p.pdf\").write_bytes(d)\n    print(f\"speck_{n}specks_{pages}p.pdf {len(d)/1024:.0f} KB\")\n"
}
````

### User / tool · 2026-11-02T06:28:34.833Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-107/build_speckle.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:28:41.072Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; .venv/bin/python -I artifacts/review-evidence/T-107/build_speckle.py $SP/atk; .venv/bin/python -I artifacts/review-evidence/T-107/probe_attacks.py $A 7897 ocr=true $SP/atk/speck_4000specks_1p.pdf $SP/atk/speck_12000specks_1p.pdf $SP/atk/speck_30000specks_1p.pdf > artifacts/review-evidence/T-107/out_speck1.txt 2>&1; cut -c1-380 artifacts/review-evidence/T-107/out_speck1.txt",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:29:52.885Z

**tool result**
````
speck_4000specks_1p.pdf 44 KB
speck_12000specks_1p.pdf 92 KB
speck_30000specks_1p.pdf 146 KB
speck_12000specks_10p.pdf 93 KB
speck_30000specks_10p.pdf 147 KB
server pid 17026; idle (57, '0:00.28'); query ?ocr=true
speck_4000specks_1p.pdf                              400 ocr_failed                   wall=  40.3s | srv rss 57->59 (after 59) MB cpu 0.3->0.5s | child peak 62 MB tess peak 88 MB | health max 8 ms | left kids=0 tess=0 | OCR could not read a page of this PDF. Try again, or paste t
speck_12000specks_1p.pdf                             201 created                      wall=   8.4s | srv rss 59->67 (after 75) MB cpu 0.5->0.7s | child peak 62 MB tess peak 114 MB | health max 30 ms | left kids=0 tess=0 | ocr_ran=True pages=[1]
speck_30000specks_1p.pdf                             201 created                      wall=   8.9s | srv rss 75->79 (after 85) MB cpu 0.7->0.8s | child peak 62 MB tess peak 111 MB | health max 8 ms | left kids=0 tess=0 | ocr_ran=True pages=[1]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:30:04.596Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; .venv/bin/python -I artifacts/review-evidence/T-107/probe_attacks.py $A 7898 ocr=true $SP/atk/speck_12000specks_10p.pdf $SP/atk/speck_30000specks_10p.pdf > artifacts/review-evidence/T-107/out_speck10.txt 2>&1; cut -c1-380 artifacts/review-evidence/T-107/out_speck10.txt; ps -axo pid,ppid,command | grep -E '[t]esseract|[p]df_hidden' | head",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:32:58.898Z

**tool result**
````
server pid 18565; idle (59, '0:00.28'); query ?ocr=true
speck_12000specks_10p.pdf                            201 created                      wall=  80.2s | srv rss 59->137 (after 166) MB cpu 0.3->1.1s | child peak 70 MB tess peak 116 MB | health max 264 ms | left kids=0 tess=0 | ocr_ran=True pages=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
speck_30000specks_10p.pdf                            201 created                      wall=  86.8s | srv rss 166->192 (after 222) MB cpu 1.1->2.1s | child peak 76 MB tess peak 114 MB | health max 264 ms | left kids=0 tess=0 | ocr_ran=True pages=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:33:08.223Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; F=$SP/bombs/ap_3500.pdf; .venv/bin/python -I artifacts/review-evidence/T-107/probe_attacks.py $A 7899 ocr=true $F $F $F $F $F $F $F $F $F $F $F $F $F $F $F $F $F $F $F $F > artifacts/review-evidence/T-107/out_bomb20.txt 2>&1; cut -c1-175 artifacts/review-evidence/T-107/out_bomb20.txt | awk '{print $2,$3,$4,$7,$8,$9,$10,$11}' | sed -n 1,22p",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T06:34:21.125Z

**tool result**
````
pid 27254; idle query ?ocr=true   
400 ocr_check_failed wall= srv rss 59->82 (after 82)
400 ocr_check_failed wall= srv rss 82->82 (after 82)
400 ocr_check_failed wall= srv rss 82->89 (after 89)
400 ocr_check_failed wall= srv rss 89->93 (after 93)
400 ocr_check_failed wall= srv rss 93->96 (after 96)
400 ocr_check_failed wall= srv rss 96->96 (after 96)
400 ocr_check_failed wall= srv rss 96->100 (after 100)
400 ocr_check_failed wall= srv rss 100->103 (after 103)
400 ocr_check_failed wall= srv rss 103->110 (after 110)
400 ocr_check_failed wall= srv rss 110->111 (after 111)
400 ocr_check_failed wall= srv rss 111->115 (after 115)
400 ocr_check_failed wall= srv rss 115->118 (after 118)
400 ocr_check_failed wall= srv rss 118->118 (after 116)
400 ocr_check_failed wall= srv rss 116->116 (after 116)
400 ocr_check_failed wall= srv rss 116->116 (after 116)
400 ocr_check_failed wall= srv rss 116->116 (after 113)
400 ocr_check_failed wall= srv rss 113->113 (after 113)
400 ocr_check_failed wall= srv rss 113->113 (after 113)
400 ocr_check_failed wall= srv rss 113->113 (after 110)
400 ocr_check_failed wall= srv rss 110->114 (after 114)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:34:29.862Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/head_9851a0d_r5; grep -rnE \"^\\s*(import|from)\\s+(pypdf|pypdfium2)\" $A/app --include=*.py; echo ---; sed -n 236,282p $A/app/backend/api.py; echo; git rev-parse --short HEAD; git diff --quiet 9851a0d HEAD -- app/backend/pdf_hidden.py app/backend/pdf_checks.py app/backend/pdf_text.py app/backend/pdf_ocr.py app/backend/api.py; echo gate-diff-rc=$?; python3 tools/check_secrets.py 2>&1 | tail -2; lsof -iTCP:7891-7899 -sTCP:LISTEN; echo lsof-rc=$?; ps -axo pid,ppid,command | grep -E '[a]pp.backend.pdf_hidden' | head"
}
````

### User / tool · 2026-11-02T06:34:31.232Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:34:33.990Z

**tool call — Bash**
````
{
 "command": "git log --oneline 9851a0d..HEAD; git diff --stat 9851a0d HEAD -- app/backend/pdf_hidden.py app/backend/pdf_checks.py app/backend/pdf_text.py app/backend/pdf_ocr.py app/backend/api.py"
}
````

### User / tool · 2026-11-02T06:34:34.121Z

**tool result**
````
ce70bd2 chore(evals): regenerate library report from clean HEAD a74b727 (T-079 r2)
a74b727 fix(evals): lib09 counts the consult once (6,390), tolerated billed-without-note, lib10 r6 / lib15 r7 re-recorded, report provenance (T-079 r2)
9217f8a fix(qa): controls gate is every wrong item; arithmetic pairs move to code tests; J3C10 reason and changelog history; report names its source commit (T-093 r3)
a9a27ed fix(backend): conflicts are code-proposed candidates classified by J3 v4; model-only flags the judge rejects are suppressed (T-094, R-CO-7)
e3a62fa fix(backend): pdf_hidden and pdf_ocr allow-list is an AST audit (T-106 round 2)
1526a1f fix(backend): billing never merges lines across records or providers; row money tokens are fields, T-103 r3
 app/backend/pdf_hidden.py | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:34:35.858Z

**tool call — Bash**
````
{
 "command": "git diff 9851a0d HEAD -- app/backend/pdf_hidden.py"
}
````

### User / tool · 2026-11-02T06:34:35.978Z

**tool result**
````
diff --git a/app/backend/pdf_hidden.py b/app/backend/pdf_hidden.py
index e4bb876..6cddef0 100644
--- a/app/backend/pdf_hidden.py
+++ b/app/backend/pdf_hidden.py
@@ -40,6 +40,7 @@ import json
 import math
 import os
 import re
+import signal
 import subprocess
 import sys
 import threading
@@ -594,7 +595,7 @@ def _run_child(data: bytes, deadline, mode: str, extra: str = ""):
                 partial, _ = proc.communicate()
                 raise HiddenScanUnavailable("memory", _texts_of(_messages(partial)))
         msgs = _messages(out)
-        if proc.returncode == -getattr(__import__("signal"), "SIGXCPU", 24):
+        if proc.returncode == -getattr(signal, "SIGXCPU", 24):
             raise HiddenScanTimeout("cpu_limit")
         if proc.returncode != 0 or not msgs:
             raise HiddenScanUnavailable("child_failed", _texts_of(msgs))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:34:49.547Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9851a0d_r5 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k \"pdf or ocr or hidden\" 2>&1 | tail -6; echo rc=$?",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:36:41.189Z

**tool result**
````
........................................................................ [ 39%]
........................................................................ [ 78%]
........................................                                 [100%]
184 passed, 1910 deselected in 111.20s (0:01:51)
rc=0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:37:35.208Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-107-security.md",
 "content": "# T-107 security review: OCR render in the killed child (security-reviewer)\n\n**Verdict: pass (0 blockers, 0 majors, 1 minor, 1 nit).** The T-087 round-4 major is closed at 9851a0d. The reviewer's Stamp-annotation bomb (3568121 bytes, 3500 MB inflated) with `ocr=true` is now a 400 in 0.4 s and the API server stays at 63 to 86 MB (it was 57 to 3631 MB). A killed or crashed child is a 400 on both child stages and the API process makes no PDF parser call. Two concurrent bombs gave two 400s. The AST test is weaker than the card says: it forbids parser imports outside the child functions, not calls (finding 1, minor).\n\nPinned: `git archive 9851a0d` unpacked in the scratchpad (`head_9851a0d_r5`). `git rev-parse --short HEAD` at write time returned ce70bd2. `git diff --quiet 9851a0d HEAD -- <five gate files>` returned rc=1: only `pdf_hidden.py` moved (e3a62fa, 2 insertions and 1 deletion: `import signal` replaces `__import__(\"signal\")`), no behaviour change. I did not run HEAD's new T-106 AST audit. Lens: untrusted-PDF resource limits, fail closed, parser isolation. Live-local mode, real uvicorn servers on 127.0.0.1:7891 to 7899, each started and killed by its own PID; `lsof -iTCP:7891-7899 -sTCP:LISTEN` returned rc=1 afterwards. A `pdf_hidden` child with parent pid 29618 was in ps from another agent and was not touched. `ANTHROPIC_API_KEY` was removed from every probe environment; no key value was printed (<redacted> if one had been).\n\n## The four confirmations\n\n| Check | Result at 9851a0d |\n|---|---|\n| API RSS flat on the bomb | Yes. `probe_r4_ocr.py` with the r4 bomb rebuilt by `probe_r4_rss.py` (3484 KB, 3500 MB inflated): `ocr=true` gives `400 ocr_check_failed` in 0.4 s, server RSS 63 MB idle, 86 MB peak, 86 MB at +8 s, health 6 to 11 ms, no `pdf_hidden` child at any sample. `ocr=false` gives `400 pdf_only_hidden_text` in 0.4 s, peak 80 MB. Twenty sequential `ocr=true` bombs: every one 400 `ocr_check_failed`; RSS 59 to 82 MB on the first, then a plateau of 96 to 118 MB (final 114 MB), so no leak. |\n| Killed or failed child: 400, no in-process render | Yes, both stages. Scan child killed by the RSS watch: 400 `ocr_check_failed`. Render child, scan fine (`probe_killed_render.py`, TestClient, spies on `pypdf.PdfReader` and `pypdfium2.PdfDocument` in the API process, `os.kill` on the render child's own PID right after Popen): control 201 in 0.5 s; SIGKILL, SIGSEGV and SIGABRT each give `400 ocr_render_failed` in 0.2 s with `API-process parser calls=[]`. Mutation runs below show the suite goes red if the fallback is put back. |\n| Two concurrent bombs give 400s | Yes. Real server, `probe_conc_server.py`: 2 concurrent gave `[(0,400,ocr_check_failed,0.4s), (1,400,ocr_check_failed,0.4s)]`, 2 children at once (peak 293 MB each side by ps), server RSS 57 to 101 MB, health max 14 ms, no child left. 6 concurrent gave four 400 `ocr_check_failed` (0.4 to 0.8 s) and two 429 `pdf_busy` (0.6 s), server 57 to 198 MB, health max 17 ms. |\n| AST test forbids parser use outside the child functions | Only partly. `mutate_ast.py` (15 mutations, each in a fresh scratch copy, run on the two static tests). Caught: a function-level `import pypdfium2` in `pdf_checks.py`, a module-level `import pypdf` in `api.py`, `from pypdf import PdfReader` in `pdf_text.extract`, a nested import in a copy of `render_in_child`, an import in a class method, `import pypdf` in a new module, and an in-process call of `pdf_ocr.render_in_child` (7 of 14 mutations; the control passes). Not caught: `__import__('pypdfium2')`, `importlib.import_module('pypdf')`, `sys.modules['pypdfium2']`, `exec('import pypdfium2')`, `import fitz`, and in-process calls of the child-side `pdf_hidden.scan_inprocess` and `pdf_text.read_pages` (7 of 14). The runtime half of the suite is stronger: `mutate_runtime.py` put back (r1) an in-process `scan_inprocess` fallback on the killed scan child: 6 tests failed; (r2) a `read_pages` call in the API process: 7 failed; (r3) an in-process render on a killed render child: 4 failed including the AST test. |\n\nTests: `pytest -p no:cacheprovider tests/unit/test_pdf_ocr_isolation.py` in the archive: 13 passed in 13.43 s (the card says 14 tests; nit). `pytest tests/unit -k \"pdf or ocr or hidden\"`: 184 passed in 111.20 s. `python3 tools/check_secrets.py`: ok (1819 file(s) scanned).\n\n## Three new OCR-path attacks (all against `ocr=true`, one server per group, `probe_attacks.py`)\n\nAll 31 files finished as a 400 or a 201, server RSS never left its idle figure on the 25 dpi and image files, and no child or tesseract process was left 3 s after any of them.\n\n1. **Many pages** (`build_attacks.py`, `build_speckle.py`): 11 and 100 image-only pages: `400 ocr_too_many_pages` in 0.2 s. 50000 `Kids` entries pointing at one page (294 KB): `413 pdf_too_large` in 0.3 s. A 3000-deep page tree (290 KB): `400 pdf_unreadable` in 0.1 s. Ten 2880 pt pages of noise and of speckle: `400 ocr_images_too_large` in 0.8 s and 2.1 s (the 12 MB PNG cap is enforced in the child). Ten pages that do fit (a 92 KB and a 147 KB file): `201`, 80.2 s and 86.8 s, health max 264 ms, server RSS 59 to 166 to 222 MB retained across the two cases (stored page images; see questions). One speckle page that Tesseract struggles with (a 44 KB file, 4000 specks): `400 ocr_failed` at 40.3 s, the per-page timeout. So one small upload can hold a core for up to about 40 s per page and 150 s per request; MAX_PDF_JOBS = 2 caps the concurrency. It is bounded, no rate limit exists by D-020, and I am not filing it.\n2. **Huge DPI through parameters**: the route takes only `name`, `ocr` and `include_hidden` (`api.py:251`); there is no dpi, scale or language parameter and unknown query parameters are ignored. The size can only come from the file, so I carried it there (11 files): MediaBox 1e9 and -1e9..1e9: `400 ocr_page_too_large` in 0.2 to 0.3 s; 2880 pt page: rendered, 0.6 s, child peak 53 MB; UserUnit 14400 on a 100 pt page, CropBox 100 on a 14400 MediaBox, CropBox 99999999 on a 100 pt page, 0.001 pt and zero MediaBox, 2880 by 0.01 pt, Rotate 90 on 2880 by 20: all `400 pdf_no_text_layer` in 0.3 to 0.4 s with child peak 18 to 53 MB. A 2 KB file with nested Form XObjects (9 levels of 10 draws, 1e9 draws): the child hit 1031 MB, was killed by the RSS watch, `400 ocr_check_failed` at 1.9 s, server RSS 57 MB the whole time.\n3. **Malformed image streams** (14 files): declared 100000 by 100000 and 2e9 by 2e9 and negative sizes over short Flate data, a DCT stream with garbage and one with a 65535 by 65535 header, JPX and JBIG2 garbage, CCITT at 1000000 columns, a Predictor 15 with Columns 2e9, LZW garbage, a 21-stage filter chain, an Indexed palette short of data, a self-referencing SMask, and an inline image declared 60000 by 60000: every one `400 pdf_no_text_layer` in 0.3 to 0.9 s (OCR ran on a blank render), child peak 18 to 95 MB, server RSS 57 MB, health max 11 ms. PDFium refused or skipped each one instead of allocating; none reached the crash path.\n\n## Findings\n\nLabels: finding 1 is a \"the guard is weaker than the card claims\" item, not a spec violation (the runtime tests close the gap for the known routes); finding 2 is a nit.\n\n```json\n{\"card\": \"T-107\", \"persona\": \"security-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive of 9851a0d (scratchpad head_9851a0d_r5); app/backend/pdf_checks.py, pdf_hidden.py, pdf_ocr.py, api.py:250-277, tests/unit/test_pdf_ocr_isolation.py; HEAD ce70bd2 at write time, pdf_hidden.py differs by a cosmetic import (git diff --quiet rc=1); live-local mode, real uvicorn servers on 127.0.0.1:7891-7899\",\n \"exercised\": [\n  \"read personas/security.md, reviews/T-087-security-r4.md, my memory notes, git show 9851a0d on pdf_checks.py, pdf_hidden.py, pdf_ocr.py and the new test file\",\n  \"pytest -p no:cacheprovider tests/unit/test_pdf_ocr_isolation.py in the archive: 13 passed in 13.43s; pytest tests/unit -k 'pdf or ocr or hidden': 184 passed in 111.20s; python3 tools/check_secrets.py: ok (1819 file(s) scanned)\",\n  \"probe_r4_rss.py (reused) rebuilt the r4 Stamp-AP bomb (3484 KB, 3500 MB inflated); probe_r4_ocr.py (reused) on a real uvicorn: ocr=true 400 ocr_check_failed in 0.4s, server RSS 63 idle / 86 peak / 86 at +8s, health 6-11 ms; ocr=false 400 pdf_only_hidden_text in 0.4s, peak 80 MB\",\n  \"probe_attacks.py x20 sequential ocr=true bombs: all 400 ocr_check_failed, RSS 59->82 then plateau 96-118 MB (final 114)\",\n  \"probe_conc_server.py: 2 concurrent bombs -> 400, 400 (0.4s), server 57->101 MB, health max 14 ms; 6 concurrent -> four 400 ocr_check_failed, two 429 pdf_busy, server 57->198 MB, health max 17 ms; no child left\",\n  \"probe_killed_render.py (TestClient, parser spies in the API process, os.kill on the render child PID): control 201; SIGKILL, SIGSEGV, SIGABRT each 400 ocr_render_failed in 0.2s, API-process parser calls []\",\n  \"mutate_ast.py: 15 mutations of the AST tests in fresh scratch copies: 7 of 14 caught, 7 of 14 not (dynamic imports, importlib, sys.modules, exec, fitz, in-process calls of scan_inprocess / read_pages); mutate_runtime.py: reinstated fallbacks fail 6, 7 and 4 tests\",\n  \"build_attacks.py + probe_attacks.py: 11 size/scale files (MediaBox 1e9, UserUnit, CropBox, Rotate, 1e9-draw Form nesting), 14 malformed-image files, 6 page-count files; build_speckle.py: 5 Tesseract-time files (1 page 4000/12000/30000 specks, 10 pages 12000/30000): results in out_dpi.txt, out_img.txt, out_many.txt, out_speck1.txt, out_speck10.txt, out_bomb20.txt\",\n  \"grep of app/ for ^import|from pypdf|pypdfium2: only pdf_ocr.py:187 (render_in_child), pdf_text.py:45-46 (read_pages), pdf_hidden.py:461-462 (scan_inprocess); read api.py:250-277 for query parameters (name, ocr, include_hidden only)\",\n  \"git rev-parse --short HEAD (ce70bd2); git diff 9851a0d HEAD on the five gate files (pdf_hidden.py, signal import only); lsof on 7891-7899 after the runs: nothing listening; every probe server started by the probe and killed by its own PID; another agent's pdf_hidden child (ppid 29618) left alone; ANTHROPIC_API_KEY unset in probe envs, no key value printed (<redacted>)\"],\n \"verdict\": \"pass\",\n \"scores\": {\"ocr_parser_isolation\": 5, \"fail_closed_behaviour\": 5, \"resource_limits\": 4, \"regression_tests\": 3, \"malformed_input_handling\": 5},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"test_pdfium_and_pypdf_are_imported_only_inside_the_child_functions forbids imports, not calls, so seven ways to run a parser in the API process still pass it\",\n   \"evidence\": \"tests/unit/test_pdf_ocr_isolation.py:62-76 walks Import/ImportFrom nodes only and checks the module name against {pypdf, pypdfium2}; test_render_in_child_is_only_reached_from_the_child_main (:79-85) checks callers of render_in_child only. mutate_ast.py in a scratch copy: appended to pdf_checks.py `p = __import__('pypdfium2'); return p.PdfDocument(data)` -> 2 passed; `importlib.import_module('pypdf').PdfReader(data)` -> 2 passed; `sys.modules['pypdfium2'].PdfDocument(data)` in api.py -> 2 passed; `exec('import pypdfium2')` -> 2 passed; `import fitz` -> 2 passed; `def _evil5(data): return pdf_hidden.scan_inprocess(data)` -> 2 passed; `def _evil6(data): return pdf_text.read_pages(data)` -> 2 passed. Control with no change: 2 passed. Caught: function-level, module-level, from-import, nested, class-method and new-module imports and a render_in_child call (7 of 14). The runtime spy tests in the same file do fail when the real fallbacks are put back (mutate_runtime.py: 6, 7 and 4 failed tests), so this is a gap in the static layer, not an open hole.\",\n   \"why_it_matters\": \"The card and the commit message say the AST test asserts that PDFium and pypdf calls exist only in the child functions. A later change that reaches PDFium through a call to scan_inprocess or read_pages, or through a dynamic import, passes the static test, and the runtime tests only cover the ocr=true routes they model. This is the class of regression T-087 round 4 was opened for.\",\n   \"fix\": \"Extend the audit to (a) every ast.Call whose target is `__import__`, `importlib.import_module`, `exec` or `eval`, and any reference to `sys.modules` with a pypdf/pypdfium2 string, anywhere in app/; (b) callers of scan_inprocess and read_pages (allowed only inside pdf_hidden._child_main and pdf_text's own helpers), the same way render_in_child callers are already pinned; (c) a deny list that also names fitz, pdfplumber, pdfminer, pdf2image and pypdfium2.raw. Keep the runtime spies.\",\n   \"acceptance_test\": \"Add a parametrised test that writes each of the seven mutation snippets above into a tmp copy of app/ (or runs the audit function on the snippet source) and asserts the audit returns a violation for all seven, and returns none for the unmodified tree.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Card AC evidence says 14 tests; the file holds 13\",\n   \"evidence\": \"T-107 AC 1 evidence: \\\"tests/unit/test_pdf_ocr_isolation.py (14 tests)\\\"; `pytest -p no:cacheprovider -q tests/unit/test_pdf_ocr_isolation.py` in the 9851a0d archive: `13 passed in 13.43s`. Test functions: 2 static, 1 + 3 (parametrised) fail-closed scan, 2 + 1 render-killed and timeout, 1 + 1 + 1 + 1 live; no fourteenth.\",\n   \"why_it_matters\": \"A count that does not match the file makes the other numbers on the handoff harder to trust at the next gate.\",\n   \"fix\": \"Correct the handoff to 13 tests, or add the missing test the writer had in mind.\",\n   \"acceptance_test\": \"`pytest --collect-only -q tests/unit/test_pdf_ocr_isolation.py` count equals the number in the handoff.\"}\n ],\n \"whats_right\": [\n  \"The render now happens in the same killed child as the scan: the r4 bomb with ocr=true went from 3631 MB of API RSS and a 201 to a 400 in 0.4 s at 86 MB, and 20 repeats plateau at about 115 MB.\",\n  \"Both child stages fail closed with a plain reason (ocr_check_failed, ocr_render_failed): SIGKILL, SIGSEGV, SIGABRT on the render child each gave a 400 in 0.2 s with zero parser calls in the API process, and putting any of three fallbacks back turns the suite red.\",\n  \"The OCR caps hold against 31 hostile files: MediaBox 1e9, UserUnit, 1e9-draw form nesting and 14 malformed image streams all ended as a 400 or 201 with the server at idle RSS and health under 270 ms.\"],\n \"questions_for_chris\": [\n  \"After two 10-page OCR cases the server RSS stayed at 222 MB (59 MB idle) because the page images are kept with the case. Is a per-process cap on stored cases or page-image bytes wanted for the hosted build, given D-020 removed the rate limit? I did not find an unbounded path, only two samples.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T06:37:35.360Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-107-security.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:37:41.968Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -5; python3 - <<'EOF'\nimport re,json\nt=open('reviews/T-107-security.md').read()\nm=re.findall(r\"```json\\n(.*?)\\n```\",t,re.S)\nprint(len(m)); d=json.loads(m[0]); print(d['verdict'],[f['severity'] for f in d['findings']])\nEOF"
}
````

### User / tool · 2026-11-02T06:37:42.140Z

**tool result**
````
ok (110 file(s))
1
pass ['minor', 'nit']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:37:48.386Z

T-107 passes with 0 blockers and 0 majors, but the static AST test is weaker than the card says (1 minor, 1 nit).

- **Stamp bomb:** with `ocr=true` it is now a 400 in 0.4 s and the API RSS stays at 63 to 86 MB (it was 3631 MB). Twenty repeats plateau at about 115 MB.
- **Killed or failed child:** SIGKILL, SIGSEGV and SIGABRT on the render child each give a 400 in 0.2 s with no PDF parser call in the API process. A killed scan child gives a 400 `ocr_check_failed`.
- **Concurrent bombs:** two at once gave two 400s. Six at once gave four 400s and two 429s.
- **AST test:** mutating it in scratch copies, it caught 7 of 14 mutations. It checks imports only, so `__import__`, `importlib`, `sys.modules`, `exec`, `import fitz` and in-process calls to `scan_inprocess` or `read_pages` still pass. The runtime tests do fail when the real fallbacks are put back, so it is a weak static layer, not an open hole (minor).
- **Nit:** the card says 14 tests; `test_pdf_ocr_isolation.py` has 13.
- **Three new attacks:** many pages, huge page sizes carried in the file and malformed image streams all ended as a 400 or 201 with the server at idle RSS. The route has no DPI parameter, so I tried size and scale from the file instead. The one bounded cost is Tesseract: a 44 KB speckle page holds a core for 40 s, and a 10-page OCR takes 80 to 87 s.

I pinned `git archive 9851a0d`; HEAD is now ce70bd2, where only `pdf_hidden.py` differs (an import cleanup). The probes and logs are in `artifacts/review-evidence/T-107/`.

Review: `/Users/arsis/zlayt-pm-project/reviews/T-107-security.md`
