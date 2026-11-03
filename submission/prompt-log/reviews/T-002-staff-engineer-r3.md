# T-002 staff-engineer-reviewer review, round 3 (final, §7.4)

**Verdict: pass (0 blockers, 0 majors, 4 minors, 2 nits).** `.venv/bin/python -m pytest tools/tests -q` -> `303 passed in 25.08s`.
Second server on 127.0.0.1:7822 with a temp `BOARD_ROOT` (killed afterwards; real repo status untouched by the POSTs). Probe: `artifacts/review-evidence/T-002-r3-probe.py`
(output `...-r3-probe.out.txt`); UI: `T-002-r3-ui.py` (output `...-r3-ui.out.txt`), screenshots `T-002-r3-<tab>-390.png`.

## Round-2 resolution
| r2 finding | status | evidence |
|---|---|---|
| 0 rebinding / Host | RESOLVED | run: `Host: evil.example` GET -> 421; `Host: evil.example:7822` + matching Origin POST -> 421; no Host (HTTP/1.0) -> 421; empty Host -> 421; `localhost.evil.example` -> 421; `[::1]:7822` and `[::1]` -> 421; `LOCALHOST:7822`, `127.0.0.1:7822`, tailnet name -> 200. Cross-origin POST still 403, text/plain 403, missing header 403, Origin null 403 |
| 2 POST error handling | PARTIAL | GET 500 now `{"error":"internal error"}` and logged to stderr (run). POST still maps every exception to 400 and does not log (finding 1) |
| 4 unpinned script / no SRI / no CSP | RESOLVED with a caveat | run: sha384 of cdnjs marked 12.0.2 and dompurify 3.1.6 recomputed with curl|openssl equals both `integrity=` values; both libs load under Playwright (`marked:true, dompurify:true`); CSP + nosniff headers present on every response. Caveat: finding 2 |
| 6 HEAD | RESOLVED | run: `HEAD /healthz` -> 405 (was 501) |
| 1 XSS, 3 overflow | still RESOLVED | run (390px): payload `<img onerror>`, `<script>`, `javascript:` link, `onclick` anchor -> `pwn:[null,null,null]`, 0 dialogs, 0 `[onerror]` nodes; scrollWidth 390 on Board, Milestones, Personas, Inbox, Activity, State against the real board data |

Console errors seen were a 404 for `/x` (an old `<img src=x>` probe note sitting inertly in the real inbox) and 500s from `/api/agents` on my near-empty fixture, which
exposed finding 3.

## Findings (see JSON)
All minor or nit; none blocks the card.

```json
{"card": "T-002", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git diff 9e759a2..e3fbb08 -- tools/board_server.py tools/board_ui.html tools/serve_board.sh tools/tests/test_board_server.py; second server http://127.0.0.1:7822 (temp BOARD_ROOT); real board at :7777 read-only; 390px",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -> 303 passed in 25.08s",
  "python3 artifacts/review-evidence/T-002-r3-probe.py 7822: 21 Host/Origin/Content-Type/header combinations incl. evil host, no Host, IPv6 literal, duplicate-style `localhost:7822, evil.example`, HEAD, CSP and nosniff headers",
  "curl | openssl dgst -sha384 on cdnjs marked 12.0.2 and dompurify 3.1.6 vs integrity= attributes in tools/board_ui.html",
  ".venv/bin/python artifacts/review-evidence/T-002-r3-ui.py (Playwright, 390x844): all six tabs on the real server and on the fixture, XSS payload via the Inbox form, dialogs, scrollWidth, console errors",
  "T-002-r3-404.py: failing requests per tab",
  "read tools/board_server.py _host_ok/_send/_post and the new tests"],
 "verdict": "pass",
 "scores": {"csrf_and_host_defense": 4, "xss_and_headers": 3, "error_handling": 3, "tests": 3},
 "findings": [
  {"severity": "minor", "title": "CSP keeps 'unsafe-inline' for scripts and allowlists all of cdnjs, so it does not back up DOMPurify",
   "evidence": "tools/board_server.py:29 `script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com`. Header observed in T-002-r3-probe.out.txt.",
   "why_it_matters": "DOMPurify is the only control against stored XSS. With 'unsafe-inline' any sanitizer bypass would still run inline handlers; any script hosted on cdnjs is also executable. The CSP does limit exfiltration (connect-src/img-src 'self', frame-ancestors, form-action), which is worth keeping.",
   "fix": "Move the inline script to a served file or use a per-response nonce, drop 'unsafe-inline' from script-src, and replace the inline onclick handlers with listeners.",
   "acceptance_test": "Playwright: CSP without 'unsafe-inline' in script-src, UI still renders all tabs, an injected inline handler raises a CSP violation."},
  {"severity": "minor", "title": "POST handler reports every exception as a 400 and logs nothing",
   "evidence": "tools/board_server.py:263 `except Exception as e:  # never drop the connection on bad input` -> `_send(400, {'error': f'bad request: {type(e).__name__}'})`. do_GET (same file) logs to stderr and returns 500.",
   "why_it_matters": "A full disk or permission error in atomic_write is shown to Chris as his own bad request and leaves no server-side trace (swallowed exception, persona checklist 12).",
   "fix": "Catch ValueError/JSONDecodeError/UnicodeDecodeError for 400; let other exceptions log and return 500 `internal error`, as do_GET does.",
   "acceptance_test": "test: monkeypatch atomic_write to raise OSError -> POST returns 500 and stderr contains the exception; malformed JSON still 400."},
  {"severity": "minor", "title": "UI does not check HTTP status; an API error crashes the tab render",
   "evidence": "tools/board_ui.html:109 `async function j(u,o){const r=await fetch(u,o);return r.json()}`. Fixture run: /api/agents 500 -> console `TypeError: a.map is not a function at renderPersonas`, tab shows nothing and no error message (T-002-r3-ui.out.txt, fixture errors).",
   "why_it_matters": "Failure is invisible to the user; the persona rule is honest failure with a visible state.",
   "fix": "In j(), throw on !r.ok (include the server's error text) and render it in the active panel/banner.",
   "acceptance_test": "Playwright with /api/agents stubbed to 500: panel shows an error message and no uncaught TypeError."},
  {"severity": "minor", "title": "test_csp_and_sri does not test the CSP",
   "evidence": "tools/tests/test_board_server.py:86-88 asserts only `html.count('integrity=\"sha384-') == 2`; no assertion on the Content-Security-Policy or X-Content-Type-Options header. Removing `_send`'s CSP line leaves the suite green.",
   "why_it_matters": "A test named for CSP that passes without it is a false assurance (checklist 13).",
   "fix": "Fetch a response from the fixture server and assert the header contains `frame-ancestors 'none'` and `connect-src 'self'`; also assert each integrity value is a 64-char sha384 base64.",
   "acceptance_test": "Deleting the CSP header line makes the test fail."},
  {"severity": "nit", "title": "Host parsing is by rsplit(':') with no port or format validation; IPv6 loopback is refused",
   "evidence": "tools/board_server.py:206 `(self.headers.get('Host') or '').rsplit(':', 1)[0].strip('[]').lower()`. Probe: `Host: localhost:7822, evil.example` -> 200; `[::1]:7822` -> 421.",
   "why_it_matters": "The first is not exploitable (browsers cannot send it) but shows the parse is loose; the second makes http://[::1]:7777 fail with 421 and no hint why.",
   "fix": "Parse with urllib/ipaddress, require a numeric port or none, and mention BOARD_ALLOWED_HOSTS in the 421 body.",
   "acceptance_test": "table test of Host values incl. `localhost:7822, evil` -> 421."},
  {"severity": "nit", "title": "A personal tailnet hostname is hard-coded as an allowed-host default",
   "evidence": "tools/board_server.py:27-28 default `BOARD_ALLOWED_HOSTS` includes <redacted-private>.",
   "why_it_matters": "Machine-specific value in committed code; if the hostname changes the UI fails closed with a 421.",
   "fix": "Default to localhost,127.0.0.1 and read the tailnet name from env or .env.example.",
   "acceptance_test": "server started with no env refuses the tailnet name."}
 ],
 "whats_right": [
  "Host allowlist runs before routing for both GET and POST, fails closed on missing/empty Host, and the rebinding case has a regression test that also asserts no inbox file was written.",
  "SRI hashes on both CDN scripts are correct (recomputed) and the page still renders every tab at 390px with no horizontal overflow.",
  "500 responses no longer echo exception text and the cause is logged server-side on GET."],
 "questions_for_chris": []}
```
