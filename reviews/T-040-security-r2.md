# T-040 round 2 review: security-reviewer (Tomás Rivas lens)

Verdict: pass (0 blockers, 0 majors, 5 minors, 2 nits). Every round-1 blocker and major is closed. The round-1 blocker is closed at HEAD by commits that are not 077e294 itself (see minor 2). Of the earlier round-2 notes, the PDF major and the moved-aside database finding are closed at c61e84f; the CSP inline-handler and dependency-manifest minors stay open.

Disclosure: an earlier `reviews/T-040-security-r2.md` (written 2026-11-02T02:17:03Z, verdict "changes", per the card notes) was overwritten by this review. That file was untracked, so it is not recoverable from git. This review re-checks its findings where they are still relevant, under "Prior round-2 notes" below. The orchestrator should decide whether that earlier file needs restoring from another source.

Scope: the reviewed commit is 077e294. The card has since gained ce191d9 (audit metadata-only unless local), 2c2eb1f (local-mode case list and library), 864676f (delete old-schema database), and the PDF route, and HEAD moved several times during this review. The final state checked is HEAD c61e84f, through a `git archive` snapshot with untracked fixtures copied in. Live servers ran with `LLM_BACKEND=fixture` and `DATA_DIR` in scratch, and were killed after.

Round-1 items, checked at c61e84f:
- Blocker (one request locks the demo out, global id collision): closed at HEAD. Two sample creates on the live server both returned 201 with distinct tokens. `test_two_cases_coexist_with_short_display_ids` passes. The pipeline `case=cid` lines are committed: `git show 0d040d3:app/backend/pipeline.py` has 2 matches and `git diff --stat app/backend/pipeline.py` is empty. So the dependency on backend-2's uncommitted WIP is discharged. At 077e294 those lines were absent (`git show 077e294:app/backend/pipeline.py | grep -c case=cid` gives 0). See minor 2.
- Major (failed create leaves an orphan row, bare 500): closed. `test_failed_create_stores_nothing_and_returns_clean_json` passes. Removing `DB.delete_case` makes it fail (mutation A). Live, a forced RuntimeError gave HTTP 500 `{"error":{"code":"internal","message":"Something went wrong.",...}}`. The server log held `create failed RuntimeError`, and the planted secret string appeared 0 times in it.
- Major (no Content-Security-Policy): closed. Live `/` carries `Content-Security-Policy: default-src 'none'; script-src 'self'; script-src-attr 'unsafe-hashes' 'sha256-95nb...'; style-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'`, plus `x-content-type-options: nosniff` and `referrer-policy: no-referrer`. I recomputed the sha256 of the one inline handler text `this.closest('dialog').close()` and it matches the hash in api.py. `index.html` has no inline `<style>` or `style=` attributes, so `style-src 'self'` breaks nothing. No `innerHTML`, `insertAdjacentHTML`, `outerHTML` or `document.write` in `app/frontend`.
- Minor (body buffered before the cap): the cap is present (api.py:25, 143, 148; 512 KB). A live 600 KB body returned 413. The test that names the behaviour does not pin it: see minor 1.
- Minor (PROVIDER_CAP_CONFIRMED not enforced): closed. `api.py:91-92` refuses to start live anthropic-api without the flag. `test_live_anthropic_needs_provider_cap_confirmation` passes.
- Minor (lazy purge only on create): closed. Purge runs from the `_headers` middleware at most once a minute. `test_expired_case_is_gone_without_any_create` passes.
- Nit (export router never included): still open. `export_routes.py:3` docstring says the factory includes the router; `git grep include_router` finds only that docstring.

Prior round-2 notes (from the card; re-checked where still relevant):
- Major, PDF upload parsed synchronously on the event loop before the demo gate, with no time or character budget: closed at c61e84f. The demo gate now runs before any byte is read (`api.py` PDF route, first lines: `if demo_mode(): raise ApiError(409, ...)`). Parsing runs in `run_in_threadpool` under `asyncio.wait_for(..., EXTRACT_TIMEOUT_S)` with a 10 s cap (`api.py:244`, `pdf_text.py:8`). The PDF tests that pin this are `test_demo_mode_refuses_before_any_parsing`, `test_oversize_pdf_is_refused_before_parsing`, `test_parsing_does_not_block_the_event_loop`, and `test_slow_extraction_hits_the_time_cap`. Live on c61e84f, a text-layer PDF in default (demo) mode returned HTTP 409 `demo_mode_unsupported_input`. Residual, now minor 3.
- Major, moved-aside schema file keeps pasted text past the 24 h purge: closed. `app/db/db.py:36-51` now deletes the old-schema file and its `-wal`, `-shm` and `-journal` siblings instead of moving them aside, and `secure_delete=ON` is set on connect. Commit 864676f says so. I checked this by reading the code; I did not exercise a schema-mismatch run live.
- Minor, CSP allows one inline event-handler attribute: still open. `app/frontend/index.html:34` still carries `onclick="this.closest('dialog').close()"`, and the CSP allows it by hash through `script-src-attr 'unsafe-hashes'`. The hash is exact, so the exception is narrow.
- Minor, no dependency manifest; pypdf unpinned: still open. `git ls-files | grep -i "requirements\|pyproject\|Pipfile\|lock"` returns only `spec/REQUIREMENTS.md`. pypdf is imported at `app/backend/pdf_text.py:26` with no pin anywhere. I could not run pip-audit against a manifest because there is none.

New minors and nits from this review:
- Minor 1, body-size test does not pin the cap it names. Mutations C and D below.
- Minor 2, commit 077e294 does not carry the id-collision fix its card note cites, and the proving test fails at that commit.
- Minor 3, PDF extraction has no character budget before `check_limits`, and the time cap leaves the worker running. Reachable only in local mode now (demo refuses first). Measured on the pre-threadpool code at dd545e3: a synthetic 4,686,528-byte, 100-page PDF extracted to 3,103,898 characters in 3.63 s on one thread, against a 60,000-character rule that is only applied afterwards.
- Nit 1, PDF route checks the `%PDF-` magic prefix but not Content-Type (the docstring says `application/pdf`).
- Nit 2, export router still unused (carried from round 1).

Test runs (exact commands and output):
- `.venv/bin/python -m pytest tests/unit/test_api_routes.py tests/unit/test_multicase.py tests/unit/test_review_rules.py -q 2>&1 | tail -2` on the worktree at run time: `55 passed in 6.33s`.
- Same three files plus `tests/unit/test_pdf_upload.py` on the dd545e3 snapshot: `66 passed in 7.30s`.
- Same four files on the c61e84f snapshot: `70 passed in 8.47s`.
- Reviewed commit 077e294 as committed (snapshot, untracked files copied in), same three files: `7 failed, 43 passed in 4.68s`. The LLM fixtures the tests load (`tests/fixtures/llm/*.json`) were added by 0d040d3, after 077e294, so the pipeline hits `FIXTURE_MISS`.
- 077e294 snapshot with HEAD's top-level fixture JSON overlaid: `2 failed, 48 passed in 5.08s`. The failures were `test_two_cases_coexist_with_short_display_ids` (minor 2) and `test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode`. The second is outside my lens; it passes at c61e84f.
- `.venv/bin/python tools/check_secrets.py` → `check_secrets: ok (716 file(s) scanned)`.

Mutation checks (scratch copy of the dd545e3 snapshot, not committed):
- A: remove `DB.delete_case` on the create-failure path → `test_failed_create_stores_nothing_and_returns_clean_json`: 1 failed.
- B: remove the CSP header line → `test_csp_and_nosniff_on_api_and_static`: 1 failed.
- C: disable the Content-Length precheck → `test_oversize_body_is_413_before_parsing`: 1 passed.
- D: disable both body caps → the same test: 1 passed.

Evidence: `artifacts/review-evidence/T-040-r2-mutate_api.py` (mutations), `T-040-r2-exp_077.py` (commit-state run), `T-040-r2-boom_final.py` (planted-exception server). The live outputs are quoted in the sections above.

Not exercised: rate limiting and a daily spend cap (neither exists here; the provider cap is the stated control and I did not verify it outside the repo); the Docker image (not present); `gitleaks` (not installed in this run; `tools/check_secrets.py` only); `pip-audit` (no manifest); the `ZLAYT_MODE=local` paths live; the PDF path with a real scanned or adversarial file.

```json
{"card": "T-040", "persona": "security-reviewer", "model": "claude-haiku-5-5",
 "scope": "reviewed commit 077e294 (app/backend/api.py, tests/unit/test_api_routes.py, tests/unit/test_multicase.py); card state at HEAD c61e84f incl. ce191d9, 2c2eb1f, 864676f and the PDF route; live checks on git-archive snapshots of dd545e3 and c61e84f with LLM_BACKEND=fixture and DATA_DIR in scratch (servers killed after); planted-exception server",
 "exercised": [
  ".venv/bin/python tools/board.py show T-040 (AC 1-6, notes including the earlier round-2 findings, handoff)",
  "git show 077e294 -- app/backend/api.py tests/unit/test_api_routes.py tests/unit/test_multicase.py (full r1 diff read)",
  ".venv/bin/python -m pytest tests/unit/test_api_routes.py tests/unit/test_multicase.py tests/unit/test_review_rules.py -q 2>&1 | tail -2 -> '55 passed in 6.33s' (worktree at run time)",
  "same three files + tests/unit/test_pdf_upload.py on git-archive snapshot of dd545e3 -> '66 passed in 7.30s'; on c61e84f -> '70 passed in 8.47s'",
  "git archive 077e294 snapshot, untracked files copied in, same three files -> '7 failed, 43 passed in 4.68s' (FIXTURE_MISS; top-level fixtures added by 0d040d3)",
  "077e294 snapshot + HEAD top-level tests/fixtures/llm/*.json overlaid (artifacts/review-evidence/T-040-r2-exp_077.py) -> '2 failed, 48 passed in 5.08s'; FAILED test_two_cases_coexist_with_short_display_ids and test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode",
  "git log -S 'case=cid' -- app/backend/pipeline.py -> 0d040d3; git show 077e294:app/backend/pipeline.py | grep -c case=cid -> 0; git show 0d040d3:app/backend/pipeline.py | grep -c case=cid -> 2; git diff --stat app/backend/pipeline.py -> empty",
  "CSP hash check: sha256 of \"this.closest('dialog').close()\" base64 = 95nblrfVsK8W4muMQZ2m4mrNYEqpgFiSJOd2xYMkbfU=, same as api.py CSP constant",
  "git grep -n 'Content-Security-Policy|PROVIDER_CAP_CONFIRMED|MAX_BODY_BYTES' c61e84f -- app/backend/api.py -> api.py:25, 91-92, 166",
  "live (dd545e3 snapshot, port 7963): curl -D on / -> CSP, referrer-policy no-referrer, x-content-type-options nosniff",
  "live (dd545e3): two POST /api/cases {sample:true} -> HTTP 201 each, distinct tokens; POST 600 KB body -> HTTP 413 input_too_large",
  "live (dd545e3): GET /api/cases and GET /api/library -> HTTP 404 not_found in default mode",
  "live (dd545e3): POST /api/cases/pdf with a text-layer PDF of unrecorded text -> HTTP 409 demo_mode_unsupported_input (before parsing in c61e84f); body 'hello' -> HTTP 400 pdf_unreadable",
  "live planted-exception server (port 7962, artifacts/review-evidence/T-040-r2-boom_final.py) on dd545e3: POST -> HTTP 500 {error.code internal, 'Something went wrong.'}; log 'create failed RuntimeError'; grep -c SECRET on log -> 0",
  "live (c61e84f snapshot, port 7964): POST /api/cases/pdf with unrecorded text, default mode -> HTTP 409 demo_mode_unsupported_input; GET /api/cases -> HTTP 404; GET / -> one content-security-policy header",
  "measurement (artifacts/review-evidence/T-040-r2-pdf_time.py): synthetic 4,686,528-byte 100-page PDF through pdf_text.extract at dd545e3 -> 3,103,898 chars, 3.63 s single thread",
  "mutation A (remove DB.delete_case on create failure) -> test_failed_create_stores_nothing_and_returns_clean_json: 1 failed",
  "mutation B (remove CSP header line) -> test_csp_and_nosniff_on_api_and_static: 1 failed",
  "mutation C (disable Content-Length precheck) -> test_oversize_body_is_413_before_parsing: 1 passed",
  "mutation D (disable both body caps) -> test_oversize_body_is_413_before_parsing: 1 passed",
  "tools/check_secrets.py -> 'check_secrets: ok (716 file(s) scanned)'",
  "grep innerHTML|insertAdjacentHTML|outerHTML|document.write in app/frontend: no hits; index.html: no inline <style> or style= attributes; index.html:34 onclick present at c61e84f",
  "git ls-files | grep -i 'requirements|pyproject|Pipfile|lock' -> spec/REQUIREMENTS.md only; grep pypdf at c61e84f -> app/backend/pdf_text.py:26 (no pin)",
  "git grep -n include_router c61e84f -- app -> export_routes.py:3 docstring only",
  "read api.py PDF route (c61e84f: demo gate, threadpool + wait_for at 244), pdf_text.py (EXTRACT_TIMEOUT_S, MAX_PAGES, extract), db.py connect (36-51), ingest.check_limits (MAX_CHARS 60000), list and audit routes"
 ],
 "verdict": "pass",
 "scores": {"input_limits_and_demo_gate": 5, "error_handling_no_leak": 5, "logging_hygiene": 5, "output_encoding_and_headers": 5, "availability_abuse_resistance": 4, "review_rules_integrity": 4},
 "findings": [
  {"severity": "minor",
   "title": "Body-size test does not pin the cap it names: removing both caps still passes",
   "evidence": "tests/unit/test_api_routes.py::test_oversize_body_is_413_before_parsing posts 600 KB and asserts 413 input_too_large. Mutation C (api.py Content-Length precheck disabled) -> '1 passed'. Mutation D (precheck and the streaming cap disabled) -> '1 passed'. The 413 comes from ingest.check_limits after the full body is read and parsed.",
   "why_it_matters": "Checklist item 1 is met (oversize is rejected before any LLM call). The round-1 point was cheap rejection before buffering, and nothing tests that. A refactor can drop the cap and CI stays green.",
   "fix": "Add a test that proves the cap itself: send more than 512 KB with no Content-Length (chunked) and assert 413 without reading past 512 KB plus one chunk (for example, a parser stub that fails if called, and a byte counter on the stream).",
   "acceptance_test": "Mutation D makes the new test fail; the existing 600 KB test stays."},
  {"severity": "minor",
   "title": "Commit 077e294 does not contain the id-collision fix its card note cites; the proving test fails at that commit",
   "evidence": "git show 077e294:app/backend/pipeline.py | grep -c 'case=cid' -> 0; git show 0d040d3:app/backend/pipeline.py | grep -c 'case=cid' -> 2. On a 077e294 snapshot with HEAD's fixture data: '2 failed, 48 passed', including FAILED tests/unit/test_api_routes.py::test_two_cases_coexist_with_short_display_ids. Card note 2026-11-02T02:02:55Z: 'Blocker ... fixed by T-050 6c3aeb1 - end-to-end verified in test_two_cases_coexist_with_short_display_ids; NOTE the pipeline.py case=cid lines are still uncommitted in backend-2's WIP'.",
   "why_it_matters": "The blocker is closed at HEAD: two sample creates both 201 with distinct tokens, and the test passes. But the closure claim named a commit that did not carry the pipeline half of the fix, so 077e294 alone is not a reproducible closure. Someone auditing the card would look at the wrong commit.",
   "fix": "In the card handoff, name 0d040d3 (pipeline case=cid) and 6c3aeb1 (T-050 composite keys) as the closing commits. Do not cite test_two_cases as proof for 077e294.",
   "acceptance_test": "git show <closing commit>:app/backend/pipeline.py contains case=cid, and test_two_cases_coexist_with_short_display_ids passes on that commit with the LLM fixtures present."},
  {"severity": "minor",
   "title": "PDF extraction has no character budget before the 60,000-character rule, and the time cap leaves the worker running",
   "evidence": "Measured at dd545e3 (pre-threadpool): synthetic 4,686,528-byte, 100-page PDF -> pdf_text.extract -> 3,103,898 characters in 3.63 s. At c61e84f the parse runs in run_in_threadpool with EXTRACT_TIMEOUT_S = 10.0 (api.py:244, pdf_text.py:8); pdf_text.py:8 comment says 'the worker thread is left to finish'. ingest.check_limits (MAX_CHARS = 60000, ingest.py:8) is applied only after extraction (api.py:254).",
   "why_it_matters": "Demo mode refuses PDFs before any parse, so the public link is not exposed. In local mode a large PDF still builds millions of characters before rejection, and a timed-out parse keeps a worker thread busy. This is an availability and memory gap for the local tool, not a public blocker.",
   "fix": "Stop extraction once the running character count exceeds ingest.MAX_CHARS (raise input_too_large at that point), and cap work per page; keep the thread cap in mind when many uploads time out.",
   "acceptance_test": "Unit: a PDF whose text exceeds MAX_CHARS returns 413 without building the full text (assert the extractor stops at the budget); a timed-out extract leaves no more than one live worker per request."},
  {"severity": "minor",
   "title": "No dependency manifest in the repo; pypdf (parses untrusted PDFs) is unpinned",
   "evidence": "git ls-files | grep -i 'requirements|pyproject|Pipfile|lock' -> spec/REQUIREMENTS.md only. pypdf is imported at app/backend/pdf_text.py:26 with no version anywhere in the repo. No pip-audit target exists.",
   "why_it_matters": "Checklist 13: dependencies must be pinned and audited. Without a manifest, neither can be checked, and the PDF parser is the riskiest dependency on the public surface.",
   "fix": "Add requirements.txt with == pins for every runtime package (fastapi, starlette, uvicorn, pypdf, anything else imported), plus a make or test target that runs pip-audit against it.",
   "acceptance_test": "pip-audit against the pinned file exits 0 or every finding is triaged in the card; grep finds pypdf== in the manifest."},
  {"severity": "minor",
   "title": "CSP allows one inline event-handler attribute through script-src-attr 'unsafe-hashes'",
   "evidence": "app/frontend/index.html:34 keeps onclick=\"this.closest('dialog').close()\"; api.py CSP constant allows it by sha256 (hash verified). Checklist 6 asks for no unsafe-inline where feasible.",
   "why_it_matters": "The hash is exact, so the exception is narrow. Still, it is the only inline script left, and moving it removes a CSP exception.",
   "fix": "Move the handler to app.js (addEventListener on the dialog Close button) and drop script-src-attr and its hash from the CSP.",
   "acceptance_test": "grep for onclick= in app/frontend returns nothing; the CSP header has no script-src-attr; the Close button still closes the dialog in Playwright."},
  {"severity": "nit",
   "title": "PDF route checks the %PDF- magic prefix but not Content-Type",
   "evidence": "pdf_text.py checks b'%PDF-' prefix; the route docstring says 'raw PDF bytes (Content-Type application/pdf)' but no header check exists.",
   "why_it_matters": "The magic check is a real type check; this is defence in depth (checklist 14 asks for an allowlist).",
   "fix": "Reject other Content-Type values with 415; keep the magic check.",
   "acceptance_test": "POST a valid PDF with content-type text/plain returns 415."},
  {"severity": "nit",
   "title": "Export router still never included; export served by an inline route (carried from round 1)",
   "evidence": "git grep -n include_router c61e84f -- app -> app/backend/export_routes.py:3 (docstring only).",
   "why_it_matters": "Dead router text can mislead a later reviewer into thinking a second export route exists.",
   "fix": "Delete the router and loader hook, or include the router and remove the inline route.",
   "acceptance_test": "grep finds exactly one definition of GET /api/cases/{token}/export."}
 ],
 "whats_right": [
  "The demo refuses before any byte of an upload is read or parsed (409 at c61e84f, pinned by test_demo_mode_refuses_before_any_parsing), and the parse runs off the event loop under a 10 s cap.",
  "Post-round-1 headers and error handling hold live: CSP with script-src 'self' and a hash for the one inline handler (hash verified), nosniff, no-referrer; a forced failure returns the standard JSON 500 and logs the exception type only.",
  "Local-only surfaces are closed by default: GET /api/cases and GET /api/library return 404 without ZLAYT_MODE=local, and the old-schema database is deleted rather than kept aside (864676f)."
 ],
 "questions_for_chris": ["Is the PDF upload meant to stay local-only for the public demo, as the current demo gate implies? If yes, the card should say so and the local-mode character budget (minor 3) becomes the only PDF work left."]}
```
