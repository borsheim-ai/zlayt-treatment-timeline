# T-040 security review (security-reviewer, Tomás Rivas lens)

Commit under review: a7df086 (HEAD moved f861159 -> e274322 -> cd4bc60 during the review; api/review/store/main unchanged by those).
Verdict: **fail**. One blocker (single request locks the public demo out for everyone), two majors.

Verified clean: demo gate refuses unrecorded text with 409 and nothing stored (row counts 0/0/0/0/0/0/0 before and after, also after 400/413/400 errors); empty 400, oversize 413 (70k chars and a 100 MB body, no llm_calls rows); unknown token 404 on all 9 token routes; invalid-edit matrix 422 (entry provider/date/empty/non-string, charge amount/class/text); `+$9,000` returns 409 needs_confirm and confirm_warnings saves it as needs_review; confirm_date bad reading returns date_invalid 422 with candidates; decisions (e1 edited, e2 accepted, r8 date 2026-05-04) survive a process restart; `referrer-policy: no-referrer`, `x-content-type-options: nosniff`, `cache-control: no-store` on /api, also on 400/404; uvicorn log shows no case tokens or record text (only `llm call failed call_id/step/prompt_hash`); /docs and /openapi.json 404; no stack trace in any response body. Unit tests: `.venv/bin/python -m pytest tests/unit/test_review_rules.py tests/unit/test_api.py -q` -> `24 passed in 1.31s`; test_api_routes -> `14 passed`.

Findings are in the JSON block. The export "router" (`export_routes.router`) is never included (`grep -rn include_router app` -> no hits); the same URL is served by an inline route in api.py:277, so the endpoint works. Raw HTML in an edited summary (`Visit <b>x</b> +$9,000`) is stored and returned verbatim as JSON; safe only while the frontend uses textContent (grep of app/frontend for innerHTML/insertAdjacentHTML/outerHTML/document.write returned nothing).

```json
{"card": "T-040", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit a7df086 (app/backend/api.py, review.py, store.py, present.py, app/main.py); app run with LLM_BACKEND=fixture on :7961, DATA_DIR in scratchpad; case_01_date_formats + sample",
 "exercised": [
  "read personas/security.md, board show T-040, api.py, review.py, store.py, main.py, export_routes.py header, DECISIONS ADR-006",
  ".venv/bin/python -m pytest tests/unit/test_review_rules.py tests/unit/test_api.py -q -> 24 passed in 1.31s; tests/unit/test_api_routes.py -> 14 passed",
  "started python -m app.main LLM_BACKEND=fixture PORT=7961, killed after",
  "POST /api/cases with an <img onerror> non-recorded text -> 409 demo_mode_unsupported_input; sqlite row counts for cases/records/entries/amounts/flags/llm_calls/review_events all 0 before and after",
  "empty 400, 70k-char 413, 100 MB body 413 in 0.3 s, malformed JSON 400, JSON array 400, text:int 400; counts still 0",
  "unknown token on GET case/status/export/audit/items, DELETE, POST run/review/confirm_date -> 404 each",
  "posted case_01, ran pipeline (fixture), status ready; edit matrix (provider, date, empty, non-str, excerpt not in record, charge amount/class/text), 9,000 needs_confirm and confirm_warnings, confirm_date bad/non-str/non-ambiguous/missing/ok, accept, rerun without confirm_rerun -> 409",
  "killed and restarted the server; GET case showed e1 edited, e2 accepted, r8 date 2026-05-04",
  "second POST of the same golden text and two POST sample:true -> 500 Internal Server Error; sqlite showed 3 orphan 'ingested' cases",
  "curl -si headers on 400, 200 static and 404 static responses; /docs, /openapi.json, path traversal -> 404",
  "read server log for tokens/record text; grep logging/print in api/review/present/store/main; grep innerHTML in app/frontend; grep Content-Security-Policy, include_router, PROVIDER_CAP_CONFIRMED, rate-limit in app/"
 ],
 "verdict": "fail",
 "scores": {"input_limits_and_demo_gate": 5, "error_handling_no_leak": 3, "logging_hygiene": 5, "output_encoding_and_headers": 3, "availability_abuse_resistance": 1, "review_rules_integrity": 5},
 "findings": [
  {"severity": "blocker", "title": "One unauthenticated request locks the public demo out for every other visitor (global id collision -> 500)",
   "evidence": "After one successful POST /api/cases (case_01), POST /api/cases with the same golden text, and two with {\"sample\":true}, each returned `500 Internal Server Error`. server log: `sqlite3.IntegrityError: UNIQUE constraint failed: records.id` at app/backend/pipeline.py:104 via api.py:153. Backend's own card note admits it: 'unsuffixed global PKs (r1,e5,f_gap_r6_r7) so a SECOND case ... collides'. The public demo accepts only golden texts, so every visitor after the first (and the first visitor's own second attempt) gets a 500 until the 24 h purge or an explicit DELETE; an attacker can re-create a case after each purge to keep the lockout (denial of service, no auth, no rate limit needed).",
   "why_it_matters": "A public link whose second visitor gets a 500 is unusable for the reviewers it exists for, and it is a one-request availability attack on the whole app (OWASP LLM10 unbounded consumption / resource exhaustion class).",
   "fix": "Namespace record/item/flag ids per case (e.g. pk = case_id + ':' + local id, or a composite (case_id, id) key) in db/pipeline; keep the local ids in API payloads.",
   "acceptance_test": "Test: POST /api/cases twice with the sample (and once more after run on the first), all return 201 with different tokens; items of case A are 404 under case B's token; ids in each payload are unchanged."},
  {"severity": "major", "title": "Failed create leaves an orphan case row (raw text stored) and returns a bare 500; no generic error handler",
   "evidence": "api.py:152-156 only deletes the case on ingest.IngestError. In the run above, 3 failed POSTs left 3 rows: `SELECT status,count(*) FROM cases GROUP BY status` -> `[('ingested', 3), ('ready', 1)]`. The demo's promise (ADR-006/D-020) is that nothing of a refused request is stored; here a non-IngestError exception stores pasted text with no token ever returned to the caller, so it is only removed by the 24 h purge. The 500 body is plain 'Internal Server Error' (no trace leaked) but it is outside the documented JSON error format.",
   "why_it_matters": "Storage growth by unauthenticated callers, stored text the user cannot delete (no token returned), and error format drift.",
   "fix": "Wrap the whole ingest in try/except Exception: delete the case and re-raise as ApiError(500, 'internal', 'Something went wrong.'); add a catch-all exception handler returning the standard JSON error with no detail.",
   "acceptance_test": "Test: inject a pipeline whose ingest_case raises RuntimeError; assert 500 with error.code present, no traceback text in the body, and cases table has 0 rows."},
  {"severity": "major", "title": "No Content-Security-Policy on any response",
   "evidence": "`curl -si localhost:7961/` shows referrer-policy and x-content-type-options only; `grep -rn Content-Security-Policy app` -> no hits. The middleware at api.py:105-111 is where headers are set. All 14 <script> tags in app/frontend/index.html are external src files, so `script-src 'self'` is feasible.",
   "why_it_matters": "Checklist item 6; edited summaries and record text are attacker-controllable strings (api returns `Visit <b>x</b> +$9,000` verbatim), so CSP is the second layer behind textContent (OWASP LLM05 / XSS cheat sheet).",
   "fix": "Add `Content-Security-Policy: default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'` in the same middleware (adjust style-src if inline styles exist) plus X-Frame-Options or frame-ancestors.",
   "acceptance_test": "Test: GET / and GET /api/health both carry a CSP header without 'unsafe-inline' in script-src; Playwright page with a record containing <img src=x onerror=alert(1)> fires no dialog."},
  {"severity": "minor", "title": "Request body is fully buffered before the size limit is applied",
   "evidence": "api.py:114 `raw = await request.body()` then json.loads, then ingest.check_limits (api.py:140). A 100 MB body was read and parsed (413 after 0.3 s); there is no Content-Length precheck or streaming cap.",
   "why_it_matters": "Memory use grows with attacker body size; the documented 60,000-character limit is enforced after the allocation (checklist item 1 intent is cheap rejection).",
   "fix": "Reject when Content-Length exceeds a byte cap (e.g. 512 KB) with 413 before reading; also cap while streaming when the header is absent.",
   "acceptance_test": "Test: POST with a 5 MB body returns 413 input_too_large and the handler never calls request.body() fully (assert via a small ASGI middleware test or peak memory)."},
  {"severity": "minor", "title": "Spec'd live-mode guard PROVIDER_CAP_CONFIRMED is not enforced anywhere; lazy purge only on create",
   "evidence": "ADR-006: 'With anthropic-api the app refuses to start unless PROVIDER_CAP_CONFIRMED=1'. `grep -rn PROVIDER_CAP_CONFIRMED app tests --include=*.py` -> no hits; api.py:57-58 goes live on ENABLE_LIVE=1 plus a key. ADR-006 also says purge runs on every request; only api.py:148 (create_case) calls DB.purge_expired. This may belong to the config/release card; flagged because api.py is where the live gate sits.",
   "why_it_matters": "D-020 replaced the in-app limiter with this conscious provider-cap step; without it a local live run has no cap acknowledgement. Purge-on-create-only means expired data stays readable by token until someone creates a case.",
   "fix": "Fail fast in create_app when backend=='anthropic-api' and live is enabled and PROVIDER_CAP_CONFIRMED!='1'; call purge_expired in the `_headers` middleware or a dependency.",
   "acceptance_test": "Test: create_app with LLM_BACKEND=anthropic-api, ENABLE_LIVE=1, a key and no PROVIDER_CAP_CONFIRMED raises; a case older than 24 h returns 404 on GET without any POST in between."},
  {"severity": "nit", "title": "Export router never included; export served by an inline route",
   "evidence": "`grep -rn include_router app --include=*.py` -> only prose in export_routes.py docstring; api.py:277 defines its own GET /export and calls XR.export_payload.",
   "why_it_matters": "Dead router and set_case_loader invite a later duplicate-route or unauthenticated-variant mistake.",
   "fix": "Either include the router or delete it and the loader hook.",
   "acceptance_test": "grep shows exactly one definition of GET /api/cases/{token}/export."}
 ],
 "whats_right": [
  "Demo gate runs before any DB write and ingest limits run before any LLM call; row counts stayed zero across 409/400/413.",
  "Review layer is fail-closed: invalid edits 422, rejected items cannot be accepted or edited, ungrounded excerpt rejected, new numbers need explicit confirm and never become verified.",
  "access_log=False, token-free logs, generic JSON errors on 404/405/validation, docs/openapi disabled."
 ],
 "questions_for_chris": ["Is PROVIDER_CAP_CONFIRMED enforcement meant to land in this card or the config/release card?"]}
```
