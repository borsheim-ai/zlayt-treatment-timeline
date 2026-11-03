# T-002 staff-engineer-reviewer review

**Verdict: fail (1 blocker, 2 majors, 3 minors, 1 nit).** The board renders and the read API is sound: all 12 GET routes return the right shape,
`/api/file` held against 30 traversal/absolute/symlink/case probes, the inbox form round-trips through `board.py inbox`, the tailnet URL answers, and
five of six tabs fit a 390px phone with no console errors. But the two state-changing POST endpoints (inbox, STOP) accept cross-site requests,
and the UI renders inbox/card/review text as unsanitized HTML, so a web page open in Chris's browser can plant an instruction the
orchestrator reads as Chris's own, and can run script on the board origin. Evidence: `artifacts/review-evidence/T-002-curl.txt`.

```json
{
 "card": "T-002",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git diff e37efb3..fbe5690 -- tools/board_server.py tools/board_ui.html tools/serve_board.sh (unchanged since); live server http://localhost:7777 (read-only GETs + rejected POSTs) and a second instance on :7799 with BOARD_ROOT=<tmp> for any write",
 "exercised": [
  "read board_server.py (263 lines), board_ui.html (150 lines), serve_board.sh, docs/RUNBOOK.md",
  "curl on :7777: /, /healthz, /api/status, /api/cards, /api/agents, /api/activity (limit=2, abc, -5, persona=), /api/milestones, /api/health, /api/inbox, /api/file, /api/stop (GET), unknown route",
  "30 /api/file probes: ../.env, .env, /.env, /etc/passwd, //etc/passwd, absolute path to the real .env, memory/../.env, %2e%2e, null byte, MEMORY/ and Memory/ case variants, directories, board/cards, tools/board.py, .claude/settings.json, CONTRACT.md via RUNBOOK.md/.. -> all 404 except allowlisted files",
  "symlinks inside an allowlisted dir (memory/link.md -> outside file, memory/hosts.md -> /etc/hosts) on the :7799 instance -> 404",
  "POST /api/inbox on :7777 with {}, empty, whitespace, invalid JSON, form-encoded empty, JSON array, {\"text\":5}, null, [\"a\"], 25KB; POST /api/stop with {} and confirm:'stop'; unknown POST route (verified board/inbox and board/STOP unchanged)",
  "on :7799: cross-origin form POST with forged Origin and Host headers to /api/inbox and text/plain POST to /api/stop -> both succeeded; lone-surrogate text; Content-Length abc and -1",
  "Browser pane: loaded the UI, opened Inbox and Activity tabs on :7799 and confirmed script execution (window.PWNED); on :7777 stepped through all 6 tabs at 390x844 and measured scrollWidth; read console (no errors)",
  "board.py inbox --ack against the :7799 tmp root printed the server-written note; curl to the tailnet URL /healthz -> 200",
  "/api/agents on :7777: 21 agents (13 reviewers), no per-file errors; checked screenshots exist (artifacts/screenshots/m0-board*.png)"
 ],
 "scores": {
  "security": 1,
  "correctness_read_api": 4,
  "error_handling": 2,
  "mobile_first": 3,
  "contract_fit": 4
 },
 "findings": [
  {
   "severity": "blocker",
   "title": "State-changing POSTs accept cross-site requests (no Origin/Host/Content-Type check): any web page can write an inbox instruction or create board/STOP",
   "evidence": "tools/board_server.py:224-249. do_POST accepts form-encoded bodies (:231) so a cross-origin <form> post is a CORS 'simple request' with no preflight, and never inspects Origin or Host. Repro on :7799 (T-002-curl.txt): `curl -X POST -H 'Origin: http://evil.example' -H 'Host: evil.example:7777' -H 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'text=...' localhost:7799/api/inbox` -> HTTP 200 {\"ok\": true, \"file\": \"board/inbox/<ts>.md\"}; `curl -X POST -H 'Origin: http://evil.example' -H 'Content-Type: text/plain' --data '{\"confirm\":\"STOP\"}' .../api/stop` -> 200 and board/STOP exists.",
   "why_it_matters": "Labelled: this is an 'unsafe' blocker, and it undercuts the contract's 'tailnet only' premise (§4.4: no auth because only tailnet peers can reach it). The server is also reachable from every page in Chris's own browser (localhost:7777, and via DNS rebinding with an attacker Host). RUNBOOK says an inbox note is 'treated exactly like' a direct instruction and the orchestrator runs in bypass-permissions mode, so a drive-by page can inject instructions into an agent with a shell. A forged STOP halts the run. The UI's confirm prompt is client-side only.",
   "fix": "On every POST: require Content-Type application/json (drop the form-encoded branch); reject if Origin is present and not in an allowlist (http://localhost:7777, http://127.0.0.1:7777, the tailnet origin from RUNBOOK); reject if Host is not in the same allowlist (403). Optionally add a per-process token header read from the served page. Keep GETs as is.",
   "acceptance_test": "curl with Origin: http://evil.example or Host: evil.example or Content-Type text/plain/form to /api/inbox and /api/stop returns 403 and writes nothing; the UI's own fetch (same origin, application/json) still returns 200."
  },
  {
   "severity": "major",
   "title": "Stored XSS: markdown rendered unsanitized, and esc() leaves the single quote unescaped inside inline onclick handlers",
   "evidence": "tools/board_ui.html:104 `const md=t=>...marked.parse(t||\"\")` (marked 12, no sanitizer) feeds innerHTML for inbox notes, card bodies, review files and state files. Repro: the inbox note `<img src=x onerror=\"window.PWNED=1\">` rendered as a live <img>; on opening the Inbox tab window.PWNED === 1. Second vector: esc() (:105) escapes & < > \" but not '; a `board.py log --card \"T-001');window.PWNED=1;('\"` event renders `onclick=\"openCard('T-001');window.PWNED=1;('');return false\"` (:140) and clicking it executed; same pattern at :127 (r.file), :137 (x.dossier unescaped, f.file) and :124 (c.id unescaped). Browser-confirmed on a fresh page load (T-002-curl.txt, Browser checks).",
   "why_it_matters": "Anything that can write to the repo or POST the inbox (see the blocker) runs script on the board origin, where it can read every /api route and POST STOP. Agents write free text into cards, notes and activity, so this is not only an outside-attacker issue.",
   "fix": "Sanitize marked output (vendor DOMPurify, or override marked's html renderer to escape raw HTML); replace inline onclick='...${x}...' with data-* attributes and addEventListener; make esc() escape ' as &#39;; add a Content-Security-Policy header (script-src 'self' plus the single CDN, no inline handlers).",
   "acceptance_test": "Inbox note with <img onerror> shows as inert text/markup; an activity event with card containing a single quote does not execute; document.querySelectorAll('[onclick]') is empty."
  },
  {
   "severity": "minor",
   "title": "POST handler has no error handling; non-string text, lone surrogates and bad Content-Length drop the connection instead of returning 400",
   "evidence": "tools/board_server.py:226 `int(self.headers.get('Content-Length') or 0)` (ValueError on 'abc'), :235 `(body.get('text') or '').strip()` (AttributeError on {\"text\":5} and [\"a\"]), :240 atomic_write of a lone surrogate (UnicodeEncodeError, traceback in server log). curl rc=52 (empty reply) for each; do_GET wraps everything in try/except (:196-222) but do_POST does not. Related: GET /api/activity?limit=abc -> 500 with the exception text (:206) and limit<=0 returns one row (:121-122).",
   "why_it_matters": "A malformed note should be a 400 with a reason. The UI's fetch().json() then throws and the sender sees nothing; the stack trace goes to board/.server.log only because log_message is silenced.",
   "fix": "Wrap do_POST like do_GET; coerce/validate text is a non-empty str (400 otherwise), Content-Length int >= 0 (400/411), encode with errors='replace' or reject surrogates; validate limit as int 1..2000 (400).",
   "acceptance_test": "curl the five bad payloads above -> 400 with a JSON error each; limit=abc -> 400."
  },
  {
   "severity": "minor",
   "title": "Activity tab overflows horizontally on a 390px phone (mobile-first AC4)",
   "evidence": "Browser pane at 390x844 on :7777: Board/Milestones/Personas/Inbox/State scrollWidth=390, Activity scrollWidth=752 (widest <li> 735px: the 'handoff T-001 What changed: tools/board.py (st...' entry). CSS: tools/board_ui.html:38-39 .feed li has no overflow-wrap (only .md has it, :44). The mobile screenshot artifacts/screenshots/m0-board-mobile.png covers only the Board tab.",
   "why_it_matters": "Chris steers from the phone (§4.4); the feed is the tab he reads to see what the team did, and it forces sideways page scroll.",
   "fix": "Add overflow-wrap:anywhere (and min-width:0) to .feed li; screenshot every tab at 390px, not just Board.",
   "acceptance_test": "At 390px every tab has document.documentElement.scrollWidth <= 390."
  },
  {
   "severity": "minor",
   "title": "Unpinned third-party script and no SRI",
   "evidence": "tools/board_ui.html:7 loads marked 12.0.2 from cdnjs without an integrity attribute; when the CDN is unreachable md() silently degrades to <pre> (:104).",
   "why_it_matters": "The board's only script dependency is fetched from a third party on every load and executes with the full API authority described in the XSS finding; the offline fallback shows raw markdown with no notice.",
   "fix": "Add integrity+crossorigin, or vendor marked into tools/ (stays 'no build step').",
   "acceptance_test": "The script tag carries an integrity hash, or no external script URLs remain in board_ui.html."
  },
  {
   "severity": "minor",
   "title": "Server writes no access or error log and returns exception text to clients",
   "evidence": "tools/board_server.py:180-181 log_message is a no-op; :221-222 returns str(e) (absolute paths) in a 500; the :7799 log shows tracebacks only for uncaught handler errors.",
   "why_it_matters": "When Chris reports 'the board is down' there is no request log, and the STOP/inbox POSTs (the only writes) leave no server-side record except the activity events.",
   "fix": "Log method, path, status to board/.server.log (no bodies); return a generic message with an error id.",
   "acceptance_test": "A POST appears in board/.server.log with status; a 500 body contains no filesystem path."
  },
  {
   "severity": "nit",
   "title": "HEAD is unsupported",
   "evidence": "`curl -I localhost:7777/` -> HTTP/1.0 501 Unsupported method ('HEAD'). board_server.py defines only do_GET/do_POST.",
   "why_it_matters": "Uptime checkers and `curl -I` report a healthy server as broken.",
   "fix": "Add do_HEAD that reuses do_GET headers.",
   "acceptance_test": "curl -I /healthz returns 200."
  }
 ],
 "whats_right": [
  "/api/file allowlist is fail-closed and held against every traversal, absolute-path, null-byte, case and symlink probe; the real .env is unreachable.",
  "Server binds 127.0.0.1 by default and tailnet exposure is by `tailscale serve`, not Funnel; the 443 clobber was disclosed and fixed.",
  "Per-tab rendering is robust: 21 cards, 21 agents, no console errors, and inbox POST -> board.py inbox round-trips."
 ],
 "questions_for_chris": [
  "Who else is on your tailnet (shared devices, invited users)? Every peer can POST /api/stop and /api/inbox with no auth."
 ],
 "verdict": "fail"
}
```
