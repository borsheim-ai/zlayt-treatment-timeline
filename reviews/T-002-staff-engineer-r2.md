# T-002 staff-engineer-reviewer review, round 2

**Verdict: changes (0 blockers, 1 major, 3 minors, 1 nit).** The round-1 blocker (cross-site form POST) and major (stored XSS) are fixed and I could not
re-break them: foreign-Origin, form-encoded, text/plain and missing-header POSTs get 403 and write nothing, and a hostile inbox note renders inert in a real
browser at 390px. What remains is a Host-header gap (DNS rebinding passes the new check because it compares Origin to the attacker-supplied Host),
which fails the round-1 acceptance line "Host: evil.example ... returns 403", plus the unchanged SRI/500-text/HEAD items.

Ran against a second server on :7811 with a temp BOARD_ROOT copy; the real board and :7777 were not written to.
Evidence: `artifacts/review-evidence/T-002-r2-csrf-curl.txt`, screenshots `artifacts/review-evidence/T-002-r2-*-390.png`.

```json
{
 "card": "T-002",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git diff fbe5690..9e759a2 -- tools/board_server.py tools/board_ui.html tools/tests/test_board_server.py; second server on :7811 with BOARD_ROOT=<scratchpad copy>; Playwright at 390x844",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -> 251 passed in 18.51s",
  "started tools/board_server.py --port 7811 with a temp BOARD_ROOT; stopped it afterwards (curl :7811 -> 000)",
  "curl POST /api/inbox: form-encoded + foreign Origin + foreign Host; JSON + foreign Origin without X-Board-Client; text/plain with header; JSON + header + foreign Origin; JSON + header + Host and Origin both evil.example:7811; POST /api/stop form + foreign Origin",
  "curl bad payloads: {\"text\":5}, [\"a\"], Content-Length: abc, lone surrogate, /api/activity?limit=abc, HEAD /healthz, /api/file?path=../../etc/passwd",
  "Python Playwright (chromium, 390x844): loaded the UI, confirmed window.marked and window.DOMPurify both loaded, posted a note containing <img src=x onerror=alert(1)>, <script>, a javascript: link and an onclick anchor through the UI's own #send handler; recorded dialogs, window.PWN* and [onerror],[onclick] counts; visited Board, Milestones, Personas, Inbox, Activity, State and recorded document scrollWidth and body text length",
  "read the server log board/.server.log in the temp root (requests are logged); grep for integrity=/Content-Security-Policy and str(e) in tools/",
  "read the full diff of board_server.py and board_ui.html"
 ],
 "verdict": "changes",
 "scores": {"correctness": 4, "error_handling": 3, "security_posture": 3, "test_quality": 4, "mobile_layout": 5},
 "findings": [
  {
   "severity": "major",
   "title": "Host header is not validated, so a DNS-rebinding page passes the CSRF check and can write inbox notes or create STOP (round-1 blocker, partially resolved)",
   "evidence": "tools/board_server.py _csrf_ok: `origin, host = self.headers.get(\"Origin\"), self.headers.get(\"Host\") or \"\"` then `if origin and urlparse(origin).netloc.lower() != host.lower(): return \"cross-origin request refused\"`. Repro on :7811: `curl -X POST -H 'Origin: http://evil.example:7811' -H 'Host: evil.example:7811' -H 'Content-Type: application/json' -H 'X-Board-Client: 1' -d '{\"text\":\"REBIND\"}' localhost:7811/api/inbox` -> `{\"ok\": true, \"file\": \"board/inbox/20261102T003913265556Z.md\"} [http 200]`, and the file exists; the inbox tab later rendered '<p>REBIND</p>'. GET with `Host: evil.example:7811` also answers 200 (full read access to cards, reviews and state). Round-1 acceptance: 'curl with ... Host: evil.example ... returns 403 and writes nothing' is not met.",
   "why_it_matters": "The orchestrator treats board/inbox notes as Chris's instructions. After a rebinding attack the attacker page is same-origin with the server (Origin == Host == attacker name), so the JSON type, custom header and Origin==Host checks all pass. The round-1 fix asked for a Host allowlist; only the Origin half was implemented.",
   "fix": "Reject any request (GET and POST) whose Host is not in an allowlist built from the bind address and port plus the tailnet names parsed from docs/RUNBOOK.md (localhost:PORT, 127.0.0.1:PORT, the tailnet host); return 403 'bad host'. Keep the Origin==Host check on top.",
   "acceptance_test": "pytest in test_board_server.py: POST and GET with Host: evil.example:PORT (and a matching Origin) return 403 and write nothing; Host: localhost:PORT with the UI's headers still returns 200."
  },
  {
   "severity": "minor",
   "title": "Two unpinned CDN scripts, no SRI, no CSP; DOMPurify, now the only XSS control, is loaded this way (round-1 finding 4, not resolved and enlarged)",
   "evidence": "grep -n 'integrity\\|Content-Security' tools/board_ui.html tools/board_server.py -> no matches. tools/board_ui.html:7-8 load marked 12.0.2 and dompurify 3.1.6 from cdnjs without integrity or crossorigin. board_ui.html md(): `(window.marked&&window.DOMPurify)?DOMPurify.sanitize(marked.parse(t||\"\")):\"<pre>\"+esc(t)+\"</pre>\"`.",
   "why_it_matters": "A compromised or swapped CDN file runs with full access to the board API and the POST endpoints. The version in the URL helps, but nothing verifies the bytes. The graceful fallback to escaped text is good; the supply-chain gap is the issue.",
   "fix": "Add integrity=sha384-... and crossorigin=anonymous to both script tags, or vendor both files under tools/ and serve them from the board server (still no build step). Optionally send a Content-Security-Policy: script-src 'self' (+ the CDN host) from _send.",
   "acceptance_test": "grep shows integrity= on both script tags (or no external script URLs remain); a tampered file is blocked by the browser."
  },
  {
   "severity": "minor",
   "title": "Every POST exception is reported as 400 'bad request', and GET 500s still return str(e) with local paths (round-1 findings 2 and 5, half fixed)",
   "evidence": "tools/board_server.py do_POST: `except Exception as e: return self._send(400, {\"error\": f\"bad request: {type(e).__name__}\"})`, so a disk-full or permission OSError in atomic_write would be reported to the client as a 400; verified on :7811 that 'Content-Length: abc' -> `{\"error\": \"bad request: ValueError\"}` [400] and a lone surrogate -> `bad request: UnicodeEncodeError` [400] (correct), but nothing separates those from server faults. board_server.py:227 (do_GET) is unchanged: `return self._send(500, {\"error\": str(e)})`.",
   "why_it_matters": "Server faults masquerading as client errors hide real failures from the operator and the UI; str(e) in the 500 can carry absolute filesystem paths.",
   "fix": "Catch (ValueError, json.JSONDecodeError, UnicodeError, KeyError) -> 400; everything else -> 500 with a generic message and an error id, and log the traceback to board/.server.log.",
   "acceptance_test": "pytest: monkeypatch B.atomic_write to raise OSError -> POST returns 500 with no path in the body; malformed JSON still returns 400."
  },
  {
   "severity": "minor",
   "title": "New CSRF/XSS controls have regression tests for the main paths but none for Host, DOM injection, or the data-* handlers",
   "evidence": "git diff fbe5690..9e759a2 --stat: tools/tests/test_board_server.py +69 lines; it posts with foreign Origin/form/text types. No test sends a foreign Host, and no test loads board_ui.html in a browser; the XSS fix (DOMPurify + data-card/data-file delegation, board_ui.html:~137) is verified only by my manual Playwright run (artifacts/review-evidence/T-002-r2-xss.json).",
   "why_it_matters": "The Host gap above shipped because the tests only mirrored the implemented checks. The delegated click handler replaced every inline onclick; a regression there would silently break card/file links.",
   "fix": "Add the Host test from the finding above and a Playwright smoke (skipped when chromium is absent): post the <img onerror> note, assert no dialog, then click a card and a dossier link and assert the dialog opens.",
   "acceptance_test": "pytest includes a foreign-Host case and a browser smoke that fails if DOMPurify is removed from md()."
  },
  {
   "severity": "nit",
   "title": "HEAD is still unsupported (round-1 finding 6)",
   "evidence": "curl -I localhost:7811/healthz -> `HTTP/1.0 501 Unsupported method ('HEAD')`.",
   "why_it_matters": "Uptime probes and some proxies use HEAD.",
   "fix": "Add do_HEAD that returns do_GET's headers without a body.",
   "acceptance_test": "curl -I /healthz returns 200."
  }
 ],
 "whats_right": [
  "Stored XSS is closed in a real browser: <img onerror>, <script>, javascript: href and onclick all neutralized (0 dialogs, PWN* undefined), inline handlers replaced by data-* delegation, esc() now escapes the single quote, and md() falls back to escaped text if either library is missing.",
  "The CSRF trio (application/json only, X-Board-Client header that forces a preflight, Origin==Host) shuts the cross-site form/text/plain vectors; every one returned 403 and wrote nothing.",
  "All six tabs measure scrollWidth 390 at 390px, including Activity (was 752) and Personas with 14k characters of content."
 ],
 "questions_for_chris": []
}
```
