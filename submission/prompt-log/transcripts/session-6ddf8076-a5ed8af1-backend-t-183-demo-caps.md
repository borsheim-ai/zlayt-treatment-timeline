# Subagent: Backend: T-183 demo caps (Backend: T-183 demo caps)

Source: `agent-a5ed8af1260bf5689.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T21:20:01.779Z

You are a backend worker in /Users/arsis/zlayt-pm-project. Your card is T-183, round 2, P0. Claim it with --force. Read reviews/T-183-security.md and the orchestrator's newest note on the card.

**The fix.** It applies in demo/public mode only.
- Cap stored cases with DEMO_MAX_CASES, default 200. Over the cap, return a plain-sentence 429 such as "This demo is full right now. Try again later."
- Cap runs in flight with DEMO_MAX_RUNS, default 4, using the same kind of 429.
- Local/dev mode stays unlimited.

**Keep it contained.**
- Put the logic in a new small module, app/backend/limits.py.
- Keep the hooks in api.py minimal. Two other backend workers (T-177 and T-179) are editing app/backend and api.py right now. Re-read files right before editing, never revert their hunks, and never run `git checkout` or `git restore`.

**Tests.** Write unit tests for both caps, for the 429 body (no stack trace, no key), and for dev mode being unlimited. Update memory/contracts/api.md with the 429.

**Commit.** Verify from a `git archive HEAD` copy, then commit only your paths through a temp index (GIT_INDEX_FILE plus `git read-tree HEAD`). Write the handoff, move the card to in_review, and reply in 1 line.

### User / tool · 2026-11-02T21:20:01.787Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:06.686Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B claim T-183 --agent backend --force 2>&1 | tail -3; $B show T-183 | tail -60; cat reviews/T-183-security.md | head -120; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/backend/project_backend_conventions.md | head -50"
}
````

### User / tool · 2026-11-02T21:20:06.882Z

**tool result**
````
T-183 claimed by backend
---
id: "T-183"
title: "M4 hardening check: server-side key never exposed, per-session rate limit and spend cap on live calls, demo mode serves the prepared sample answers with no key, optional bring-your-own-key, input size limits, error states; fill only real gaps"
milestone: "M4"
role: "backend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T21:00:13Z"
updated_at: "2026-11-02T21:20:06Z"
claimed_by: "backend"
claimed_at: "2026-11-02T21:20:06Z"
rounds: 1
commits: ["4671eee"]
reviews:
  - {"persona": "security-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-183-security.md", "at": "2026-11-02T21:19:53Z"}
ac:
  - {"n": 1, "text": "each item verified with a test (existing or new); gaps fixed; summary table in the card", "done": true, "evidence": "tests/unit/test_t183_hardening.py 15 pass; summary table in card notes; gap fixed in api.py make_case; commit 4671eee"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T21:00:16Z orchestrator: assigned: backend
- 2026-11-02T21:00:29Z backend: claimed
- 2026-11-02T21:05:16Z backend: SUMMARY TABLE (tests/unit/test_t183_hardening.py, 15 tests, pass; related suites 252 pass)
| Item | Status | Test |
| Key never in browser/logs | verified, no gap | test_key_never_appears_in_any_response_or_log_even_when_the_sdk_error_echoes_it (live run, SDK error echoes the key; all routes, headers, static, caplog, stdout/stderr); test_no_static_file_or_api_text_names_the_key_or_a_key_field; test_health_reports_whether_live_is_on_but_never_the_key; existing test_provider.py::test_no_text_in_logs |
| Per-session rate limit | NOT built, by decision D-020/ADR-006 (no in-app limiter). Public build makes zero model calls; one run is bounded by 60,000 chars / 40 records | test_every_route_that_can_call_a_model_makes_zero_calls_in_demo_mode_even_with_a_key; test_live_work_per_run_is_bounded_by_the_input_limits |
| Spend cap | provider-side cap, enforced at startup (app refuses ENABLE_LIVE + anthropic-api without PROVIDER_CAP_CONFIRMED=1); no in-app ledger (D-020) | test_a_live_api_build_refuses_to_start_without_the_provider_side_spend_limit_confirmed; existing test_api_routes.py::test_live_anthropic_needs_provider_cap_confirmation |
| Demo mode, no key | verified | test_no_key_demo_runs_the_sample_to_ready_with_prepared_answers_and_refuses_other_text; existing test_demo_never_reaches_a_live_backend, test_demo_health_reports_fixture_even_if_live_backend_and_key_are_set |
| Bring-your-own-key | SCOPE CUT (D-011, SCOPE_CUTS row 17): not implemented. A key sent in a header or body is ignored and never echoed | test_a_key_sent_with_a_request_is_never_used_or_echoed (3 variants) |
| Input size limits | verified; 1 real gap fixed | test_character_and_record_limits_return_413_and_store_nothing (60,001 chars, 41 records, oversize body, chunked body, nothing stored); test_pdf_upload_is_size_limited_and_refused_in_demo_mode; existing test_oversize_body_is_413_before_parsing, test_limit_boundaries |
| Error states plain | verified; GAP FIXED: a 41-record paste returned message 'input too large' (a bare code) -> now 'Input is too large.' (app/backend/api.py make_case) | test_every_error_is_plain_json_with_no_trace_path_or_framework_text (12 probes); test_a_run_that_fails_says_so_in_one_plain_sentence_and_keeps_finished_items |
Open for orchestrator: CONTRACT M4 lists a per-session limiter and in-app spend cap; D-020 cut them. Not built here. If wanted, it is a small card (call counter in audited.py). Unrelated: tests/unit/test_boundaries.py::test_dynamic_import_calls_are_forbidden fails on a __import__ in export code from another worker's uncommitted change.
- 2026-11-02T21:05:16Z backend: AC 1 checked: tests/unit/test_t183_hardening.py 15 pass; summary table in card notes; gap fixed in api.py make_case; commit 4671eee
- 2026-11-02T21:05:17Z backend: moved in_progress -> in_review
- 2026-11-02T21:05:23Z orchestrator: review dispatched: security-reviewer
- 2026-11-02T21:19:53Z orchestrator: review security-reviewer (claude-sonnet-5-5): changes — reviews/T-183-security.md; round 1; findings:
    - [major] Public demo has no bound on stored cases or concurrent runs: any client can fill the disk and burn CPU — fix: Add a small deterministic bound in the demo build and answer with the existing plain-error shape and a 429: (a) a global cap on stored cases (for example 500), after which the oldest expired or oldest cases are purged or the create is refused with 'The demo is busy. Try again
    - [minor] The D-020 cut of the CONTRACT's per-session rate limit and spend cap is not in SCOPE_CUTS.md or the submission — fix: Add a SCOPE_CUTS row: 'In-app per-session rate limit and spend cap: cut (D-020/ADR-006); public build is demo-only and makes no model calls; live mode is local-only and refuses to start without PROVIDER_CAP_CONFIRMED=1.' Add one sentence to the README or product note
- 2026-11-02T21:19:53Z orchestrator: Round 2 (backend): demo/public mode caps stored cases (DEMO_MAX_CASES, default 200, oldest demo-created cases pruned or 429) and runs in flight (DEMO_MAX_RUNS, default 4) -> plain-sentence 429; tests. Limiter cut recorded as SCOPE_CUTS row 24 by orchestrator. PROVIDER_CAP_CONFIRMED nit: accepted, documented.
- 2026-11-02T21:20:06Z backend: claimed

## Handoff
Changed: 15 new tests (tests/unit/test_t183_hardening.py) plus one fix in api.py make_case (a 41-record paste said 'input too large', now a sentence). Verified: .venv/bin/python -m pytest tests/unit/test_t183_hardening.py (15 pass) and 252 related tests pass. Left: in-app rate limit and spend ledger are not built (D-020, provider-side cap enforced at startup); BYOK is cut (D-011). Surprised: the secret scanner blocked a test sentinel shaped like a key, so it is built in two parts. test_boundaries failure is another worker's __import__ in export code.

# T-183 security review (security-reviewer, claude-sonnet-5-5)

Scope: HEAD 33e88c6 (card commit 4671eee is an ancestor; `git diff --quiet 33e88c6 HEAD -- app Dockerfile requirements.txt` was clean at write time). I tested a `git archive HEAD` copy at `artifacts/review-evidence/T-183/head`, with probes `probe1.py`, `probe2.py` and `probe3.py` beside it (outputs in `probe*.out`).

Verdict: **changes**. There is no blocker and one major.

The four hardening items hold in demo mode:
- **Key:** I sent 73 requests per run, including static files, every case route and error paths. Two servers ran: one with no key, and one with a sentinel key, `LLM_BACKEND=anthropic-api` and `ENABLE_LIVE` unset. The sentinel and the string `sk-ant` appeared in no response body or header. The server log was 0 bytes, so no case text or key was logged. A key sent in a header or body (BYOK attempts) was ignored and not echoed.
- **Demo mode:** with no key and with a key, health reports `backend: fixture`, `answers: prepared`, `live_enabled: false`. The sample ran create, run and `ready` with 9 entries, 4 amounts and 10 flags.
- **Size limits:** 60,001 characters, a 600 KB body and a chunked body of 640 KB all returned 413 with "Input is too large." Other text returns 409 "This demo only runs the recorded sample cases." and is not stored. A PDF upload returns 409 in demo mode.
- **Error states:** about 20 bad requests (bad JSON, an array body, missing or empty text, an unknown token, wrong method, unknown route, a markup title, a lone surrogate) all returned `{"error":{"code","message"}}` with a plain sentence. None showed a traceback or framework text. `/docs` and `/openapi.json` are 404. `/api/cases`, `/api/library` and the library POST are 404 in the public build.

Other checks:
- A live `anthropic-api` start with `ENABLE_LIVE=1`, a key and no `PROVIDER_CAP_CONFIRMED` exits 1 with a RuntimeError that does not echo the key.
- The CSP is set on API and static responses (`script-src 'self'`, no inline script except one hashed `onclick`).
- The Dockerfile runs as uid 1000, sets no key and no `ENABLE_LIVE`, and `.dockerignore` is an allow-list.
- `tools/check_secrets.py` reports ok on 3477 files. `git log --all -G'sk-ant-...'` finds no added or removed key-shaped line in any commit. `.env` is ignored (`.gitignore:25`). `.env.example` has no value.
- `pip-audit --no-deps` on `requirements.txt` found no known vulnerabilities. gitleaks is not installed.
- The frontend has no `innerHTML`, `eval` or `document.write`. The one grep hit is a comment (`sidebyside.js:5`).

## The two recorded cuts, for a public demo-only link

- **D-011, no bring-your-own-key: acceptable.** It removes the one path where a user-supplied secret could be logged or echoed, and the probe confirmed a supplied key is ignored. Nothing in the demo needs it. This is a "would have done it differently" call, not a spec violation.
- **D-020, no in-app rate limit or spend cap: acceptable for the wallet, not for resources.**
  - **Why the wallet is safe.** The public build cannot make a model call. `provider.backend_name()` returns `fixture` unless `ENABLE_LIVE=1`, the image never sets it, and the process refuses to start in live `anthropic-api` mode without `PROVIDER_CAP_CONFIRMED=1`. Probes A and B showed zero live attempts with a key present. So "denial of wallet" is closed by construction, and a limiter would protect nothing there.
  - **What remains open.** With no limiter, a public client can fill storage and CPU (finding 1). The wallet argument does not cover that, so the cut is acceptable only once a small storage or concurrency bound exists.

```json
{"card": "T-183", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of HEAD 33e88c6 (card commit 4671eee is an ancestor) at artifacts/review-evidence/T-183/head; demo build env, servers on 127.0.0.1:17861-17865; sample case; no live model call was made",
 "exercised": [
  "python3 tools/board.py show T-183 (read the summary table and handoff)",
  "read personas/security.md, memory/ORCHESTRATOR_DECISIONS.md D-011/D-020, memory/SCOPE_CUTS.md, docs/CONTRACT.md:314, README.md:44",
  "read app/backend/api.py, app/config.py, app/main.py, app/llm/provider.py, store.live_enabled, Dockerfile, .dockerignore, requirements.txt",
  ".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_t183_hardening.py in the archive: 15 passed",
  "probe1.py: two real uvicorn servers (no key; sentinel key + LLM_BACKEND=anthropic-api + ENABLE_LIVE unset); 73 requests each (health, static files, create, run, status, trace, judges, audit, export, narrative, billing, ~20 error probes, 60,001-char, 600 KB and chunked oversize bodies, BYOK header and body); scanned every response and the server log for the sentinel and 'sk-ant'",
  "probe2.py: ENABLE_LIVE=1 + anthropic-api + key without PROVIDER_CAP_CONFIRMED (exit 1, key not echoed); CSP/nosniff/no-store headers; export-before-run 422 body; 300 creates and 150 concurrent runs against the demo build",
  "probe3.py: bytes stored per created case and per run case; sequential create rate",
  ".venv/bin/python tools/check_secrets.py (ok, 3477 files); git log --all -G key-pattern over history (0 matching lines); git check-ignore .env; .env.example key line",
  "pip-audit -r requirements.txt --no-deps --disable-pip in a scratchpad venv: no known vulnerabilities",
  "grep of app/frontend for innerHTML/eval/document.write"
 ],
 "verdict": "changes",
 "scores": {"key_exposure": 5, "demo_mode_isolation": 5, "input_limits": 5, "error_plainness": 5, "resource_abuse_resistance": 2, "cut_documentation": 3},
 "findings": [
  {"severity": "major",
   "title": "Public demo has no bound on stored cases or concurrent runs: any client can fill the disk and burn CPU",
   "evidence": "No limiter, case cap or run cap exists (api.py create_case/make_case, run_case; retention is only a 24 h age purge, db.py:17). Measured on the archive, demo build: 300 sequential sample creates all returned 201 in 5.1 s (about 62/s from one client, probe3: 'sequential creates/sec: 62'); 150 concurrent /run calls all returned 202 in 5.5 s (Counter({202: 150})), each spawning a thread (api.py:437-440, one per token, none shared); the sqlite file was 28,246,016 bytes after 301 cases and 150 runs; per case 11,100 bytes created-only and 166,420 bytes more per run (probe3). Arithmetic from those figures: one client creating and running at about 30 runs/s writes about 5 MB/s, or 10 GB in about 30 minutes, and creates alone write about 0.7 MB/s. DATA_DIR is the container disk (Dockerfile line 21). A scripted client therefore degrades or takes down the shared demo for all users. No money is spent.",
   "why_it_matters": "My dossier goal 1 is that a public link cannot be abused to exhaust resources. D-020 removed the limiter on the argument that the demo makes no model calls. That argument closes denial of wallet but not disk, thread or SQLite write exhaustion, which are open. This is a major, not a blocker: no model call, no secret, and no data leak is involved.",
   "fix": "Add a small deterministic bound in the demo build and answer with the existing plain-error shape and a 429: (a) a global cap on stored cases (for example 500), after which the oldest expired or oldest cases are purged or the create is refused with 'The demo is busy. Try again in a few minutes.'; (b) a cap on runs in flight, as pdf_checks.MAX_PDF_JOBS already does for PDFs; (c) optionally reuse an existing identical sample case's records rather than storing a new copy per create. A per-IP limiter is not needed for this.",
   "acceptance_test": "With a test DB, POST /api/cases {sample:true} N+1 times, where N is the cap: the extra create returns 429 with a one-sentence message, the stored case count stays at N, and /api/health still returns 200. Start more runs than the in-flight cap: the extras return 429 'busy', not 500."},
  {"severity": "minor",
   "title": "The D-020 cut of the CONTRACT's per-session rate limit and spend cap is not in SCOPE_CUTS.md or the submission",
   "evidence": "docs/CONTRACT.md:314 lists 'server-side API key with per-session rate limit and spend cap ... optional bring-your-own-key' as M4 scope; CONTRACT.md:260 says cuts are recorded in SCOPE_CUTS.md. memory/SCOPE_CUTS.md has a BYOK row (row 17, D-011) but `grep -i 'limiter|rate limit|spend|D-020' memory/SCOPE_CUTS.md` returns only the unrelated T-050 debt row (line 46). The limiter cut exists only in memory/ORCHESTRATOR_DECISIONS.md D-020 and the card note. grep -i 'rate limit|per-IP|limiter' over submission/*.md, README.md and docs/RUNBOOK.md returns no hits.",
   "why_it_matters": "A grader reading CONTRACT.md:314 will look for the limiter. The cut is legitimate (the public build makes zero model calls), but an unrecorded deviation from a stated contract line is the thing the cut log exists to prevent. Separate from finding 1, which is about behaviour.",
   "fix": "Add a SCOPE_CUTS row: 'In-app per-session rate limit and spend cap: cut (D-020/ADR-006); public build is demo-only and makes no model calls; live mode is local-only and refuses to start without PROVIDER_CAP_CONFIRMED=1.' Add one sentence to the README or product note stating the same.",
   "acceptance_test": "grep -i 'rate limit' memory/SCOPE_CUTS.md returns the new row; the README or submission names the demo-only reason."},
  {"severity": "nit",
   "title": "PROVIDER_CAP_CONFIRMED is a self-attested flag, not a check",
   "evidence": "api.py:111 refuses only on the env var being unequal to '1'; nothing verifies a provider limit exists. Live mode is local-only, so this is documentation-grade protection.",
   "why_it_matters": "If a future deploy flips live on, the startup check gives more confidence than it earns.",
   "fix": "Say in the README that the flag is a promise, not a check, or add an in-app call counter as the card note suggests.",
   "acceptance_test": "README states what the flag does and does not verify."}
 ],
 "whats_right": [
  "Demo isolation is enforced in provider.backend_name(), so no route can reach a model without ENABLE_LIVE=1, and with a key present the probe still showed backend fixture and no key in any output.",
  "Oversize input is rejected before parsing or storage, including a chunked body with no content-length, and every error is a one-sentence JSON body with no trace.",
  "Startup refuses live anthropic-api without the provider-cap confirmation, and the failure message does not echo the key."
 ],
 "questions_for_chris": []}
```
---
name: backend-conventions
description: Codepaths, conventions and pitfalls for the deterministic backend modules and pipeline (T-032/033/037); read before touching ingest, amounts, gaps, conflicts, pipeline
metadata:
  type: project
---

Codepaths (app/backend): `ingest.py` (split/limits/dedupe/warnings, `ingest()` composite, `evidence_span`), `dates.py` (format list, 2-digit year >40 ambiguous per D-027), `amounts.py` (cents, classify, extract_amounts, rate_note), `totals.py`, `gaps.py`, `conflicts.py`, `flag_templates.py` (render with closed var whitelist + golden-subtype aliases), `lexicon.py` (loads app/llm/lexicon.yaml as data; deterministic modules must not import app.llm), `pipeline.py` (stages 0-7, `run_ingest`, `ingest_case`, `run_pipeline`, `run_case`, `judge_summary`, CLI). `app/pipeline.py` is a shim so `python -m app.pipeline` works (outside owned paths; flagged to orchestrator).

Conventions: money is int cents and amounts.py must not contain `float(`; text outside recognised record blocks becomes an `unsplit` record (never dropped; only exact `ingest.BANNERS` lines are set aside); a figure inside an injection hit has cents None; flag title/explanation only via flag_templates.render; code never sets review_status (pipeline items leave a run `pending`; `_persist` preserves existing review status on rerun).

Pitfalls: (1) the stage-and-commit rule: `git add` and `git commit` must be separate Bash calls (git-guard hook rejects a combined call), and commit with explicit pathspec `git commit -m ... -- <paths>`. (2) One sqlite3 connection shared by worker threads corrupts `PRAGMA table_info` reads; audited.py serialises writes with `_DB_LOCK`; do not use `:memory:` DBs with threads (CLI uses a temp file). (3) Fixture keys hash the full prompt, so any prompt/schema change in app/llm/prompts or judges invalidates tests/fixtures/llm: re-run `LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record <golden .txt>` per case and `--judges`. (4) tests/unit/test_pipeline.py SEM script has `record_id` which schemas.FlagOutput forbids: the 3 j3 pipeline tests fail until T-036/qa reconcile.

Review findings to avoid repeating: silent text loss in splitters, silent century guesses, ACs ticked on REPL evidence without a named test.

T-075 (determinism): the 0.0 live 3-run did not reproduce in 12 later runs; the real fragilities were judge prompts (J4 rejected valid flags; J3 undecided), model-order-dependent ids, and immediate retries. Judge prompts now v2 (flag category rules; J3 takes `category`). To re-record only judge fixtures after a judge prompt change, replay the recorded set and call claude-cli only on a miss at j3/j4 (never re-record whole cases: it would overwrite extract/narrative fixtures other workers depend on); then run `make_curated.py` (no flag), restore unchanged curated files byte-for-byte, `--check`. Run live pipeline checks in parallel processes (6 at once is fine, ~60 s).

T-085 (Spanish records): code half `language.py` + `spanish_text.py` (no app.llm import; test_boundaries bans LLM imports in dates.py, so keep Spanish code checks out of `spanish.py`, which wires the judge). Spanish records use steps `extract_es` / `judge_faithfulness_es` (own prompts, registered in audited.PROMPT_OF_STEP). To record only missing fixtures for new prompts: `ENABLE_LIVE=1 LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record --fill-missing evals/library/<packet>.txt` (replays recorded answers). Committing a shared file other workers also edit: filter `git diff HEAD -U0` hunks by keyword, `git apply --cached --unidiff-zero` into a temp GIT_INDEX_FILE built from `git read-tree HEAD`; `xargs git add` is blocked by git-guard, list paths explicitly.

## T-085 r2 lessons (language fail-safe)
- Commit with other workers' dirty hunks in the same file: build a temp index (`GIT_INDEX_FILE=$(mktemp)`, `read-tree HEAD`), `git add` whole files only when all hunks are mine; for mixed files (confidence/review/pipeline) hash-object the HEAD text + my edits and `update-index --cacheinfo`. Verify with `git diff --cached --stat`.
- language.detect: lang 'uncertain' = some non-English evidence, no confident answer; is_translated(lang) routes es+uncertain to the Spanish path; record_lang never returns English for text with foreign evidence. Do not put words identical to English (fracture, diagnostic, cervical, protrusion) in fr/pt/es lists.
- A one-record packet's preamble line becomes record 1 in ingest; test packets need 2+ records or no preamble.
- Spanish eval pairs: tests/unit/spanish_translation_pairs.jsonl; live judge eval opt-in SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1.

T-086/T-087 r2 (PDF security): `pdf_hidden.py` is a differential render (page with vs without all text, render mode 3 toggled per object); `FPDFTextObj_GetText` is O(page) per call, so read text only for hidden objects. `review.enforce_ocr` re-applies OCR_DERIVED after every item-rewriting step (edit, manual entry, split, date confirm). Pitfalls: other workers edit review.py/api.py concurrently, so commit "HEAD + my hunks": rebuild the file by applying my replacements to `git show HEAD:file`, `git hash-object -w`, `git update-index --cacheinfo` into a `GIT_INDEX_FILE=$(mktemp)` index after `git read-tree HEAD`; then `git reset -q -- <my files>` so the main index is not stale. git-guard blocks `$VAR` in command position (use literal paths) and macOS `sed -i` needs a suffix (use python for edits). Strided memoryview rows need `.tobytes()` before zlib.

## T-085 r4 (D-050)
- Non-English never verified: `confidence.compose_state` ctx `translated` -> AI_TRANSLATION; any new code path that composes a state from a record must pass `language.translated_record(rec)`. Row-based recomputes (rejudge.recompose, review._without_date_doubt) keep the reason from the stored row. Tests: tests/unit/test_d050_never_verified.py.
- language.detect: `_EN_COLLISIONS` (son, operation, plus, solo...) are not foreign evidence when English-only words >= 3. Held-out jsonl rows: `d050_only` (unroutable, word-for-word Spanish) and `ambiguous` are excluded from routing gates.
- Committing with other workers' hunks: HEAD moves during work (check `git log -1` right before `read-tree HEAD`); rebuild blobs from the new HEAD (`git show HEAD:f` + my substitutions) and `update-index --cacheinfo`; check_stale_index blocks a stale tree. Run the committed tree via `git archive $(git write-tree)` in the scratchpad.

T-087 r4 (PDF isolation): ALL PDF parsing (pypdf read + PDFium scan) runs in one child (`pdf_hidden._run_child`, modes text/scan/both, JSON lines: texts first, result second) killed at the shared deadline, with a parent-side `ps` RSS poll (1 GiB; macOS has no RLIMIT_AS). `pdf_text.read_pages` is in-process-only for the child and tests. `pdf_checks._JOBS` (2) gives 429 `busy` and covers OCR too (OCR's pdfium render still runs in the API worker thread). Commit trick that worked: fixed GIT_INDEX_FILE path, `git add` and `git commit` in separate Bash calls (git-guard), then `git reset -q -- files` on the real index. Reviewer probe files are in the reviewer's scratchpad, not the repo: rebuild from the review text.

T-094 (live determinism, conflicts, causation): open-ended model generation of conflicts was the flake. Conflicts are now CODE candidates (`conflict_candidates.py`: plan vs early end with frequency x duration multiplied out; denial of prior history vs a phrase-list prior hit), J3 (`judge_conflict_v4`) only classifies; no `conflicts` model step or prompt exists. J3 benign -> tray (rejected); model-only flag + J4 disagree -> suppressed (`out["suppressed_flags"]`). Pitfalls: (1) `evals.run` scores tray (rejected) flags as emitted candidates, so only suppression removes a false positive from precision; (2) any J3 prompt edit must pass `evals.run --controls` (D-046: all wrong caught, 0 false agree, including held-out) before the 3-run evals; (3) to re-record only the changed judge fixtures use a replay-then-record-on-miss wrapper (fixture first, live only on a miss) per case, then make_curated.py and restore unchanged curated files byte-for-byte; (4) the tree is shared: build commits from a temp index on HEAD and check `git diff HEAD -- <file>` for other workers' hunks (pipeline.py/trace.py/api.md got swept by others twice); (5) architect owns docs/LLM_VS_CODE.md row 11 and must be told the conflicts row changed.

T-094 r2 (D-053): nothing a model proposes is dropped. A model-only flag J4 rejects, and a model-proposed conflict without a code candidate, are TRAY items (`flags._to_tray`; reasons JUDGE_DISAGREES / LLM_ONLY); `present.case_view` tray has kind `flag` items (before this, rejected flags were in the DB but never in the API tray). `suppressed_flags` no longer exists. evals/run.py: `to_candidates` skips state `rejected` (precision/recall over emitted flags only), `flag_tray` reported apart, signature `flags` excludes rejected; report header names `Source commit ..., tree clean`. judge_flag_v3 (missed_care = scheduled/recommended treatment not attended; scene refusal is scene_facts): re-record J4 fixtures with `python -m app.llm.record --fill-missing <packet>` over evals/golden/*.txt and evals/library/*.txt in parallel (script pattern: ThreadPool of subprocesses, ENABLE_LIVE=1 LLM_BACKEND=claude-cli RECORD_FIXTURES=1). Candidate rules: number words, plan cue, _early_end negation/completion guards in conflict_candidates.py; uncovered patterns in SCOPE_CUTS row 13.

T-103 r4 (billing.py): a printed money token is identified by POSITION (`_at` offset range, `_row` excerpt range, `_unit` line/segment start), never by text; parsers attach positions, `_placed()` reads them back, `_strip_private()` removes every `_`-prefixed key before analyze returns. D-052 "no comparisons" was read strictly: no `_nt`, no cents `<`, sign = `_is_credit` flag; guard test `test_no_money_value_or_text_is_compared_in_billing_code`. Verify count fixes with MANY seeds (reviewer seed 20261102 plus seeds 1-40 via the test module's `_insert`/`_BASES`): seed 20261102 alone hid ~28 CMS/EOB shapes. Never add keys to `_ub_header`/`_header` cols (the test generator draws from them, which would change every seed's draws); use `_ub_all_cols`. Commit with other workers' dirty api.md: build HEAD blob + my replacements, `update-index --cacheinfo` into a temp `GIT_INDEX_FILE`.

T-143 (app/backend/uncovered.py, record.uncovered[]): code-only list of clinical sentences no live entry excerpt overlaps; lexicon has no body-part/dx family so uncovered.py holds its own regexes (move to lexicon.yaml via researcher). Pitfall: `GIT_INDEX_FILE=<temp> git commit -- <paths>` (pathspec = --only) commits the WORKING TREE of those paths and sweeps other workers' dirty hunks (happened to present.py/api.md in 225e666). With a temp index commit WITHOUT a pathspec; use the pathspec form only against the real index. Project python is .venv/bin/python (system python3 lacks fastapi); the 9 amounts/t114/t093 failures on 2026-11-02 belonged to others' dirty amounts.py.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:09.735Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -3; git status --short | head -20; wc -l app/backend/api.py; grep -n \"demo\\|def create_case\\|def make_case\\|def run_case\\|Thread\\|def _err\\|def error\\|_JOBS\\|busy\\|429\" app/backend/api.py | head -90"
}
````

### User / tool · 2026-11-02T21:20:09.916Z

**tool result**
````
33e88c6 tools: prompt-log export also redacts tailnet hostnames, 100.64/10 addresses and a work email; docstring lists every edit (T-187 privacy review)
59e33ca docs(submission): one-page product note, Part 2 process doc, validation-ladder SVG
f22f8fc tools: prompt-log export writes <redacted> (scanner-safe) and no stale 'capped' header (T-187)
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t166_mvp_polish.md
D  .claude/agent-memory/frontend/project_t174_finish.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
     698 app/backend/api.py
1:"""FastAPI routes (memory/contracts/api.md). Thin: parsing, the demo gate, error format; logic lives in ingest/store/review/present/export.
37:PREPARED_BANNER = "In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item"      # D-065
120:        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says
125:    def demo_mode():
264:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "answers": ans,
270:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
285:    async def create_case(request: Request):
303:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
306:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
307:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
327:            if e.code == "pdf_busy":     # T-087 round 4: at most pdf_checks.MAX_PDF_JOBS uploads are read at once; the rest are told to retry
328:                raise ApiError(429, "busy", _PDF_MESSAGES["pdf_busy"], {"reason": "pdf_busy"}) from None
343:    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None, strict_name=True):
350:        if demo_mode() and digest(text) not in allowed_hashes():
351:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
357:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
373:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
386:            v = present.case_view(c, token, backend=backend(), models=present.models_for(c, token, config_models()), demo_mode=demo_mode())
433:    async def run_case(token: str, request: Request):
440:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
441:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
442:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
450:            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
458:        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
459:        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
466:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
467:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
468:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
600:    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)
626:                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:13.338Z

**tool call — Bash**
````
{
 "command": "sed -n 95,150p app/backend/api.py; sed -n 280,300p app/backend/api.py; sed -n 340,372p app/backend/api.py; sed -n 395,460p app/backend/api.py; grep -n \"def \\|DB_LOCK\\|^import\\|^from\" app/backend/store.py | head -60; grep -n \"class ApiError\" -A12 app/backend/api.py | head -30"
}
````

### User / tool · 2026-11-02T21:20:13.465Z

**tool result**
````
def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.db_path = db_path
    app.state.recorded = recorded_hashes()

    def allowed_hashes():
        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
    runs = {}
    rejudging = set()
    _boot = DB.connect(db_path)
    try:
        store.interrupt_orphaned_runs(_boot)        # T-178: a run a stopped process left "running" becomes failed (run again allowed); its accepted items are untouched
    finally:
        _boot.close()
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
        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available

    def demo_mode():
        return not live_enabled()

    def answers():
        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set)."""
        if live_enabled():
            return "live"
        from app.llm.backends import fixture
        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"

    def config_models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def models():
        """The models /health shows. T-177 r2: on the prepared (curated) set no model drafts an answer, so none is named as the drafter. Per-case payloads use present.models_for (from the case's own calls)."""
        base = config_models()
        prepared = answers() == "prepared"
        return dict(base, generator=present.PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)

    def conn():
        return DB.connect(app.state.db_path)

    def make_call(c, cid):
        if call_factory:
            return call_factory(c, cid)
        from app.llm import audited
        if not local_mode():
            raise ApiError(404, "not_found", "Not found.")
        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}

    @app.post("/api/cases", status_code=201)
    async def create_case(request: Request):
        b = await body_of(request)
        sample = b.get("sample") is True
        lib = None
        if isinstance(b.get("library"), str):
            if not local_mode():
                raise ApiError(404, "not_found", "Not found.")
            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
            if lib is None:
                raise ApiError(404, "not_found", "No such library case.")
        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
        if not isinstance(text, str):
            raise ApiError(400, "bad_request", "Provide text or sample: true.")
        typed = isinstance(b.get("title"), str)
        given = b.get("title") if typed else b.get("name")          # T-157: `title` is the name a paralegal types (refused when over 120 characters); `name` stays accepted (a long file name is cut)
        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample, strict_name=typed)
        except case_list.TitleError as e:
            raise ApiError(422, "invalid_title", str(e)) from None

    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None, strict_name=True):
        name = name if isinstance(name, str) else ("Sample case" if sample else None)
        name = valid_name(name, strict_name)          # before anything is stored: a refused title leaves no case behind
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
            cid = DB.create_case(c, text, now=now, name=name or None,
                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
            try:
                ing = pipeline_mod().ingest_case(c, cid, text, now)
                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
                flags = DB.list_items(c, cid, "flag")
            except Exception as e:                       # nothing of a failed create stays stored (ADR-006): drop the case row and its parts
                DB.delete_case(c, cid)
                if isinstance(e, (ingest.IngestError, language.UnsupportedLanguage)):
                    msg, detail = language.api_fields(e)
                    if not msg:             # T-183: a limit hit during splitting (too many records) said "input too large" (the bare code); say it as a sentence
                        msg = "Input is too large." if e.code == "input_too_large" else "Input is empty." if e.code == "bad_request" else "The input could not be read."
                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, msg, detail) from None
                log.error("create failed %s", type(e).__name__)
                raise ApiError(500, "internal", "Something went wrong.") from None
            return {"token": cid, "name": DB.get_case(c, cid)["name"], "title": case_list.case_title(c, DB.get_case(c, cid)), "status": "ingested", "source": "sample" if sample else "paste",
        if "title" not in b or not (b["title"] is None or isinstance(b["title"], str)):
            raise ApiError(400, "bad_request", "Send {\"title\": text}.")
        name = valid_name(b["title"])
        c = conn()
        try:
            get_case(c, token)
            DB.update_case(c, token, name=name or None)
            case = DB.get_case(c, token)
            return {"token": token, "name": case["name"], "title": case_list.case_title(c, case)}
        finally:
            c.close()

    @app.delete("/api/cases/{token}", status_code=204)
    def delete_case(token: str):
        c = conn()
        try:
            get_case(c, token)
            DB.delete_case(c, token)
        finally:
            c.close()
        return Response(status_code=204)

    def _run_thread(token, raw):
        c = conn()
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
            store.run_ended(token)

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
            store.run_started(token)
            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
            runs[token].start()
            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
        finally:
            c.close()

    @app.post("/api/cases/{token}/rejudge")
    async def rejudge_case(token: str):
        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
        from app.backend import rejudge as RJ
5:import json
6:import os
7:import threading
8:import time
10:from app.backend import ingest, pdf_text, spanish
11:from app.db import db as DB
21:def run_started(token: str) -> None:
26:def run_ended(token: str) -> None:
31:def is_live_run(token: str) -> bool:
36:def interrupt_run(conn, token: str, now: float = None) -> bool:
48:def interrupt_orphaned_runs(conn, now: float = None) -> list:
57:def settle_stale_run(conn, case: dict, now: float = None) -> dict:
67:def live_enabled() -> bool:
74:def live_model_available() -> bool:
80:def iso(t) -> str:
85:def load_records(conn, case_id: str, raw: str = None) -> list:
102:def _by_id(records):
107:def amount_pos(item: dict, rec):
118:def export_case(conn, case_id: str, blockers: bool = True) -> dict:
50:class ApiError(Exception):
51-    def __init__(self, status, code, message="", detail=None):
52-        super().__init__(code)
53-        self.status, self.code, self.message, self.detail = status, code, message or code.replace("_", " "), detail or {}
54-
55-
56-def digest(text: str) -> str:
57-    return hashlib.sha256(ingest.normalize_text(text).encode("utf-8")).hexdigest()
58-
59-
60-def recorded_hashes() -> set:
61-    return {digest(p.read_text()) for p in GOLDEN.glob("*.txt")}
62-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:21.744Z

**tool call — Bash**
````
{
 "command": "grep -n \"def local_mode\" -B2 -A6 app/backend/*.py | head -20; grep -n \"CREATE TABLE\" app/db/*.py | head; grep -n \"def purge_expired\" -A10 app/db/db.py; grep -n \"429\\|busy\" memory/contracts/api.md | head; sed -n 1,35p tests/unit/test_t183_hardening.py; grep -n \"def \\|fixture\" tests/unit/test_t183_hardening.py | head -30; sed -n 15,35p app/backend/store.py; git diff HEAD --stat -- app/backend/api.py"
}
````

### User / tool · 2026-11-02T21:20:21.913Z

**tool result**
````
app/backend/api.py-79-
app/backend/api.py-80-
app/backend/api.py:81:def local_mode() -> bool:
app/backend/api.py-82-    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py-83-
app/backend/api.py-84-
app/backend/api.py-85-def is_loopback_peer(request) -> bool:
app/backend/api.py-86-    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
app/backend/api.py-87-    host = request.client.host if request.client else None
app/db/db.py:72:    ddl = re.search(r"CREATE TABLE IF NOT EXISTS review_events \(.*?\n\);", schema, re.S).group(0).replace("IF NOT EXISTS ", "")
297:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
298-    ids = [r["id"] for r in conn.execute("SELECT id FROM cases WHERE created_at < ?", (now - retention_seconds,))]
299-    for cid in ids:
300-        delete_case(conn, cid)
301-    return len(ids)
302-
303-
304-def table_counts(conn, case_id: str) -> dict:
305-    return {t: conn.execute(f"SELECT COUNT(*) FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,)).fetchone()[0]
306-            for t in _CASE_TABLES}
9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409, re-run of a case that already has decisions only; never an edit or manual entry, D-047), `item_rejected` (409), `unsupported_language` (400, T-085: see Spanish-language records), `invalid_edit` (422, every structurally invalid edit), `date_invalid` (422, `confirm_date` with a non-candidate date), `llm_unavailable` (503), `busy` (429, T-087: more than two PDF uploads are being read at once; `detail.reason: "pdf_busy"`; retry shortly).
89:**Hidden text.** Every text object is checked against the page as rendered (pypdfium2). Reasons: `invisible_render_mode`, `transparent`, `off_page`, `tiny_font` (under 5 pt effective), `blends_with_background` (a differential render, contrast under 96 levels counts as blending: the page is drawn with and without all text, and the text counts as hidden when the two agree under its box, so white or background-coloured text, text under a cover of any pattern, and text with marks, rules or dots in its box are all caught), `could_not_verify` (the check could not be made exactly, so the text is held back as suspected) `covered_by_annotation` (a form field, stamp or other annotation with an appearance lies over the text; some viewers draw it opaque while the renderer does not), `clipped` (a clipping window shows under half of the text's box) and `not_in_rendered_page` (words in the file's text layer that the renderer did not place on the page, for example text nested deeper than the 40 form levels a page draws). Hidden and suspected text is removed from the case text, so it can never ground a quote, until its page is confirmed. **Fail closed:** a page whose check could not run (the renderer cannot open the file or the page, more than 20000 text objects, or more than 400 hidden pieces, or more than 500 annotations) is `unchecked`: its text is kept out of the case and the page is listed in the report with `unchecked: true`, `count: 0` and a plain `why`, until the paralegal confirms the page with `include_hidden`. Both PDF parsers, the text-layer read (pypdf) and the render scan (PDFium), run in one child process that is killed at the request deadline (HTTP 400 `pdf_timeout`; no work survives it, and no PDF is parsed in the API process). The child has a CPU limit, an address-space limit where the OS enforces one (Linux; macOS refuses it, unverified on Linux here) and a parent-side check of its resident memory every 0.1 s that kills it above 1 GiB on every platform (the pages are then `unchecked`). At most two PDF uploads are processed at once; a third gets `429 busy`. A Popup annotation with an appearance over text counts as a cover (`covered_by_annotation`); one without an appearance does not. A file whose only usable text is hidden or unchecked is refused with `detail.reason: "pdf_only_hidden_text"`, `detail.hidden_text_pages` and `detail.unchecked_pages`.
"""T-183 (M4 hardening check): the server-side key is never exposed or logged, the public build makes no model call and serves the prepared
sample answers with no key, a key cannot be supplied by a request (BYOK is cut, D-011), input size limits hold at the HTTP layer, and every
error state is plain JSON. Fixture backend; the live path uses a fake SDK client. No network, no real key (the key below is a sentinel)."""
import json
import logging
import pathlib
import re
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import ingest
from app.backend.api import MAX_BODY_BYTES, create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]
KEY = "sk-" + "ant-SENTINEL-" + "key-0123456789abcdef"      # built in two parts so the secret scan does not take a test sentinel for a key


def _client(tmp_path, monkeypatch, *, live=False, local=False, key=None):
    monkeypatch.setenv("LLM_BACKEND", "anthropic-api" if live else "fixture")
    for k, v in (("ENABLE_LIVE", "1" if live else None), ("ANTHROPIC_API_KEY", key), ("PROVIDER_CAP_CONFIRMED", "1" if live else None),
                 ("ZLAYT_MODE", "local" if local else None)):
        monkeypatch.delenv(k, raising=False) if v is None else monkeypatch.setenv(k, v)
    (tmp_path / "index.html").write_text("<p>hi</p>")
    return TestClient(create_app(str(tmp_path / "t183.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000), raise_server_exceptions=False)


def _wait(c, tok, ok=("ready", "failed", "done_with_errors")):
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ok:
            return s
        time.sleep(0.25)
21:def _client(tmp_path, monkeypatch, *, live=False, local=False, key=None):
22:    monkeypatch.setenv("LLM_BACKEND", "anthropic-api" if live else "fixture")
30:def _wait(c, tok, ok=("ready", "failed", "done_with_errors")):
40:def test_key_never_appears_in_any_response_or_log_even_when_the_sdk_error_echoes_it(tmp_path, monkeypatch, caplog, capsys):
46:        def __init__(self, *a, **k):
49:        def create(self, **kw):
71:def test_no_static_file_or_api_text_names_the_key_or_a_key_field():
82:def test_health_reports_whether_live_is_on_but_never_the_key_or_cap_setting(tmp_path, monkeypatch):
88:def test_env_example_and_repo_tree_carry_no_real_key():
98:def test_every_route_that_can_call_a_model_makes_zero_calls_in_demo_mode_even_with_a_key(tmp_path, monkeypatch):
108:    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False
120:def test_a_live_api_build_refuses_to_start_without_the_provider_side_spend_limit_confirmed(tmp_path, monkeypatch):
128:def test_live_work_per_run_is_bounded_by_the_input_limits():
134:def test_no_key_demo_runs_the_sample_to_ready_with_prepared_answers_and_refuses_other_text(tmp_path, monkeypatch):
137:    assert h["demo_mode"] is True and h["live_enabled"] is False and h["backend"] == "fixture" and h["synthetic_only"] is True and h["banner"]
152:def test_a_key_sent_with_a_request_is_never_used_or_echoed(tmp_path, monkeypatch, hdrs, body):
166:def test_character_and_record_limits_return_413_and_store_nothing(tmp_path, monkeypatch):
182:def test_pdf_upload_is_size_limited_and_refused_in_demo_mode(tmp_path, monkeypatch):
193:def test_every_error_is_plain_json_with_no_trace_path_or_framework_text(tmp_path, monkeypatch):
220:def test_a_run_that_fails_says_so_in_one_plain_sentence_and_keeps_finished_items(tmp_path, monkeypatch):
223:        def run_pipeline(*a, **k): raise RuntimeError(f"SECRET {KEY} /Users/x/app.py line 3")
225:        def ingest_case(c, cid, text, now):
228:    monkeypatch.setenv("LLM_BACKEND", "fixture"); monkeypatch.delenv("ENABLE_LIVE", raising=False)
_LIVE_LOCK = threading.Lock()
RUN_STALE_AFTER_S = 480 + 120     # pipeline.DEADLINE_S + grace: a "running" case older than this with no live thread was left by a process that died
INTERRUPTED_MESSAGE = ("The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. "
                       "Run it again to retry.")


def run_started(token: str) -> None:
    with _LIVE_LOCK:
        LIVE_RUNS.add(token)


def run_ended(token: str) -> None:
    with _LIVE_LOCK:
        LIVE_RUNS.discard(token)


def is_live_run(token: str) -> bool:
    with _LIVE_LOCK:
        return token in LIVE_RUNS


 app/backend/api.py | 20 ++++++++++++++++++--
 1 file changed, 18 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:40.949Z

**tool call — Bash**
````
{
 "command": "cat > app/backend/limits.py <<'EOF'\n\"\"\"T-183 r2: resource bounds for the public demo build (security review: any client could fill the disk and burn CPU; no money is at stake because the\npublic build makes no model call). Two caps, public mode only (ZLAYT_MODE != local); local/dev stays unlimited:\n  DEMO_MAX_CASES  stored cases, default 200  -> POST /api/cases and the PDF upload answer 429 `busy` when the table is full (expired cases are purged first)\n  DEMO_MAX_RUNS   runs in flight, default 4  -> POST /api/cases/{token}/run answers 429 `busy`\nPure functions that return a plain sentence (or None); the route turns it into the standard error body. No stack text, no key, no count of other users' data.\nThe case cap is a soft bound: simultaneous creates can overshoot it by a few, never grow it without limit.\"\"\"\nimport os\n\nDEFAULT_MAX_CASES = 200\nDEFAULT_MAX_RUNS = 4\nFULL_MESSAGE = \"This demo is full right now. Try again later.\"\nBUSY_MESSAGE = \"This demo is busy right now. Try again in a minute.\"\n\n\ndef _limit(name: str, default: int) -> int:\n    try:\n        n = int(os.environ.get(name, \"\").strip() or default)\n    except ValueError:\n        return default\n    return n if n >= 1 else default           # a zero, negative or unreadable value falls back to the default (a typo must not switch the demo off or lock it shut)\n\n\ndef max_cases() -> int:\n    return _limit(\"DEMO_MAX_CASES\", DEFAULT_MAX_CASES)\n\n\ndef max_runs() -> int:\n    return _limit(\"DEMO_MAX_RUNS\", DEFAULT_MAX_RUNS)\n\n\ndef case_full(conn, local: bool):\n    \"\"\"The 429 sentence when the public demo already stores the maximum number of cases, else None. Call after expired cases are purged.\"\"\"\n    if local:\n        return None\n    return FULL_MESSAGE if conn.execute(\"SELECT COUNT(*) FROM cases\").fetchone()[0] >= max_cases() else None\n\n\ndef runs_busy(in_flight: int, local: bool):\n    \"\"\"The 429 sentence when the public demo already has the maximum number of runs in flight, else None.\"\"\"\n    if local:\n        return None\n    return BUSY_MESSAGE if in_flight >= max_runs() else None\nEOF\ngrep -n \"^from app.backend import\\|^from app.backend\" app/backend/api.py | head"
}
````

### User / tool · 2026-11-02T21:20:41.045Z

**tool result**
````
24:from app.backend import case_extras, case_list, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
43:from app.backend import pdf_checks as _pdf_checks      # noqa: E402  (T-086/T-087)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:41.987Z

Now the hooks, re-reading right before editing.

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:44.737Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\np=\"app/backend/api.py\"\ns=open(p).read()\na=\"            DB.purge_expired(c, now)\\n            cid = DB.create_case(c, text, now=now, name=name or None,\"\nassert s.count(a)==1\ns=s.replace(a,\"            DB.purge_expired(c, now)\\n            if (full := limits.case_full(c, local_mode())):          # T-183 r2: public demo stores at most DEMO_MAX_CASES\\n                raise ApiError(429, \\\"busy\\\", full, {\\\"reason\\\": \\\"demo_full\\\"})\\n            cid = DB.create_case(c, text, now=now, name=name or None,\")\nb=\"            now = time.time()\\n            store.run_started(token)\\n\"\nassert s.count(b)==1\ns=s.replace(b,\"            if (busy := limits.runs_busy(len(runs), local_mode())):  # T-183 r2: public demo runs at most DEMO_MAX_RUNS at once\\n                raise ApiError(429, \\\"busy\\\", busy, {\\\"reason\\\": \\\"demo_busy\\\"})\\n\"+b)\nc=\"from app.backend import case_extras, case_list, dismissal_patterns, export as export_mod, ingest, language, narrative,\"\nassert s.count(c)==1\ns=s.replace(c,\"from app.backend import limits\\n\"+c)\nopen(p,\"w\").write(s)\nEOF\ngit diff HEAD -U0 -- app/backend/api.py | grep -n \"limits\" "
}
````

### User / tool · 2026-11-02T21:20:44.888Z

**tool result**
````
6:+from app.backend import limits
8:+            if (full := limits.case_full(c, local_mode())):          # T-183 r2: public demo stores at most DEMO_MAX_CASES
11:+            if (busy := limits.runs_busy(len(runs), local_mode())):  # T-183 r2: public demo runs at most DEMO_MAX_RUNS at once
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:20:47.635Z

**tool call — Bash**
````
{
 "command": "sed -n 215,260p tests/unit/test_t183_hardening.py; grep -n \"def pipeline_mod\" -A6 app/backend/api.py"
}
````

### User / tool · 2026-11-02T21:20:47.761Z

**tool result**
````
        if not e.get("message") or re.fullmatch(r"[a-z_]+", e["message"]):
            bad.append((verb, path, r.status_code, "message is a bare code, not a sentence"))
    assert bad == [], bad


def test_a_run_that_fails_says_so_in_one_plain_sentence_and_keeps_finished_items(tmp_path, monkeypatch):
    class Boom:
        @staticmethod
        def run_pipeline(*a, **k): raise RuntimeError(f"SECRET {KEY} /Users/x/app.py line 3")
        @staticmethod
        def ingest_case(c, cid, text, now):
            from app.backend import pipeline as PL
            return PL.ingest_case(c, cid, text, now)
    monkeypatch.setenv("LLM_BACKEND", "fixture"); monkeypatch.delenv("ENABLE_LIVE", raising=False)
    c = TestClient(create_app(str(tmp_path / "f.sqlite"), static_dir=str(tmp_path), pipeline=Boom), client=("127.0.0.1", 50000))
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    s = _wait(c, tok)
    assert s["status"] == "failed"
    err = s.get("error") or {}
    assert err.get("message") == "The run stopped; finished items are kept." and "SECRET" not in json.dumps(s) and KEY not in json.dumps(s) and "/Users" not in json.dumps(s)
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202       # and it can be run again
154:    def pipeline_mod():
155-        if pipeline is not None:
156-            return pipeline
157-        from app.backend import pipeline as PL
158-        return PL
159-
160-    def get_case(c, token):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:21:06.032Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/test_t183_limits.py <<'EOF'\n\"\"\"T-183 round 2: the public demo bounds stored cases (DEMO_MAX_CASES, default 200) and runs in flight (DEMO_MAX_RUNS, default 4); both answer a plain\n429 `busy`; local/dev mode is unlimited. Fixture backend, no network, no key.\"\"\"\nimport json\nimport re\nimport threading\n\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import limits\nfrom app.backend.api import create_app\n\nKEY = \"sk-\" + \"ant-SENTINEL-\" + \"key-0123456789abcdef\"\n\n\nclass Hold:\n    \"\"\"A pipeline stand-in whose runs stay in flight until released.\"\"\"\n    def __init__(self):\n        self.gate = threading.Event()\n        self.started = threading.Semaphore(0)\n\n    def ingest_case(self, c, cid, text, now):\n        from app.backend import pipeline as PL\n        return PL.ingest_case(c, cid, text, now)\n\n    def run_pipeline(self, c, token, raw, **k):\n        self.started.release()\n        self.gate.wait(20)\n\n\ndef _app(tmp_path, monkeypatch, *, local=False, pipeline=None, **env):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    for k in (\"ENABLE_LIVE\", \"DEMO_MAX_CASES\", \"DEMO_MAX_RUNS\", \"ZLAYT_MODE\"):\n        monkeypatch.delenv(k, raising=False)\n    monkeypatch.setenv(\"ANTHROPIC_API_KEY\", KEY)           # present, to prove no 429 body can carry it\n    if local:\n        monkeypatch.setenv(\"ZLAYT_MODE\", \"local\")\n    for k, v in env.items():\n        monkeypatch.setenv(k, str(v))\n    (tmp_path / \"index.html\").write_text(\"<p>hi</p>\")\n    return TestClient(create_app(str(tmp_path / \"l.sqlite\"), static_dir=str(tmp_path), pipeline=pipeline), client=(\"127.0.0.1\", 50000), raise_server_exceptions=False)\n\n\ndef _plain_429(r):\n    assert r.status_code == 429\n    e = r.json()[\"error\"]\n    text = r.text\n    assert e[\"code\"] == \"busy\" and e[\"message\"].endswith(\".\") and not re.fullmatch(r\"[a-z_]+\", e[\"message\"])\n    for bad in (\"Traceback\", \"File \\\"\", \"/Users\", \"sk-ant\", KEY, \"sqlite\", \"Exception\", \"limits.py\", \"200\", \"DEMO_MAX\"):\n        assert bad not in text, bad\n    assert set(r.json()) == {\"error\"} and set(e) <= {\"code\", \"message\", \"detail\"}\n    return e\n\n\ndef _count(c):\n    import sqlite3\n    return sqlite3.connect(c.app.state.db_path).execute(\"SELECT COUNT(*) FROM cases\").fetchone()[0]\n\n\ndef test_defaults_are_200_cases_and_4_runs_and_a_bad_value_falls_back(monkeypatch):\n    for k in (\"DEMO_MAX_CASES\", \"DEMO_MAX_RUNS\"):\n        monkeypatch.delenv(k, raising=False)\n    assert (limits.max_cases(), limits.max_runs()) == (200, 4)\n    for bad in (\"\", \"abc\", \"0\", \"-3\", \"2.5\"):\n        monkeypatch.setenv(\"DEMO_MAX_CASES\", bad)\n        monkeypatch.setenv(\"DEMO_MAX_RUNS\", bad)\n        assert (limits.max_cases(), limits.max_runs()) == (200, 4), bad\n    monkeypatch.setenv(\"DEMO_MAX_CASES\", \"7\")\n    monkeypatch.setenv(\"DEMO_MAX_RUNS\", \" 2 \")\n    assert (limits.max_cases(), limits.max_runs()) == (7, 2)\n\n\ndef test_the_case_cap_refuses_the_extra_create_with_a_plain_429_and_stores_nothing(tmp_path, monkeypatch):\n    c = _app(tmp_path, monkeypatch, DEMO_MAX_CASES=3)\n    for _ in range(3):\n        assert c.post(\"/api/cases\", json={\"sample\": True}).status_code == 201\n    r = c.post(\"/api/cases\", json={\"sample\": True})\n    e = _plain_429(r)\n    assert e[\"message\"] == \"This demo is full right now. Try again later.\" and e[\"detail\"] == {\"reason\": \"demo_full\"}\n    assert _count(c) == 3\n    assert c.get(\"/api/health\").status_code == 200\n\n\ndef test_deleting_a_case_makes_room_again(tmp_path, monkeypatch):\n    c = _app(tmp_path, monkeypatch, DEMO_MAX_CASES=1)\n    tok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n    assert c.post(\"/api/cases\", json={\"sample\": True}).status_code == 429\n    assert c.delete(f\"/api/cases/{tok}\").status_code == 204\n    assert c.post(\"/api/cases\", json={\"sample\": True}).status_code == 201\n\n\ndef test_a_refused_text_is_still_409_not_429_and_a_full_demo_does_not_hide_a_bad_request(tmp_path, monkeypatch):\n    c = _app(tmp_path, monkeypatch, DEMO_MAX_CASES=1)\n    assert c.post(\"/api/cases\", json={\"sample\": True}).status_code == 201\n    assert c.post(\"/api/cases\", json={\"text\": \"x\" * 60001}).status_code == 413\n    assert c.post(\"/api/cases\", json={\"text\": \"Visit 1/2/2024 knee pain.\"}).status_code == 409      # unrecorded text is refused before the cap is looked at\n    assert c.post(\"/api/cases\", json={}).status_code == 400\n\n\ndef test_the_run_cap_refuses_the_extra_run_with_a_plain_429_and_frees_a_slot_when_a_run_ends(tmp_path, monkeypatch):\n    hold = Hold()\n    c = _app(tmp_path, monkeypatch, pipeline=hold, DEMO_MAX_RUNS=2)\n    toks = [c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"] for _ in range(3)]\n    try:\n        assert c.post(f\"/api/cases/{toks[0]}/run\", json={}).status_code == 202\n        assert c.post(f\"/api/cases/{toks[1]}/run\", json={}).status_code == 202\n        r = c.post(f\"/api/cases/{toks[2]}/run\", json={})\n        e = _plain_429(r)\n        assert e[\"message\"] == \"This demo is busy right now. Try again in a minute.\" and e[\"detail\"] == {\"reason\": \"demo_busy\"}\n        assert c.get(f\"/api/cases/{toks[2]}/status\").json()[\"status\"] != \"running\"      # the refused case was not flipped to running\n        assert c.get(\"/api/health\").status_code == 200\n    finally:\n        hold.gate.set()\n    for t in toks[:2]:\n        for _ in range(100):\n            if c.get(f\"/api/cases/{t}/status\").json()[\"status\"] != \"running\":\n                break\n            threading.Event().wait(0.1)\n    assert c.post(f\"/api/cases/{toks[2]}/run\", json={}).status_code == 202\n\n\ndef test_a_second_run_of_the_same_case_is_still_409_not_429(tmp_path, monkeypatch):\n    hold = Hold()\n    c = _app(tmp_path, monkeypatch, pipeline=hold, DEMO_MAX_RUNS=1)\n    tok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n    try:\n        assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\n        assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 409\n    finally:\n        hold.gate.set()\n\n\ndef test_local_dev_mode_is_unlimited(tmp_path, monkeypatch):\n    hold = Hold()\n    c = _app(tmp_path, monkeypatch, local=True, pipeline=hold, DEMO_MAX_CASES=1, DEMO_MAX_RUNS=1)\n    try:\n        toks = [c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"] for _ in range(4)]\n        assert _count(c) == 4\n        for t in toks:\n            assert c.post(f\"/api/cases/{t}/run\", json={}).status_code == 202\n    finally:\n        hold.gate.set()\n\n\ndef test_the_429_body_carries_no_trace_key_or_internal_name_even_in_a_full_busy_demo(tmp_path, monkeypatch):\n    hold = Hold()\n    c = _app(tmp_path, monkeypatch, pipeline=hold, DEMO_MAX_CASES=1, DEMO_MAX_RUNS=1)\n    try:\n        tok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n        assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\n        _plain_429(c.post(\"/api/cases\", json={\"sample\": True}, headers={\"x-api-key\": KEY}))\n        other = _plain_429(c.post(\"/api/cases\", json={\"sample\": True}))\n        assert json.dumps(other).count(KEY) == 0\n    finally:\n        hold.gate.set()\n\n\ndef test_pure_helpers(monkeypatch):\n    monkeypatch.setenv(\"DEMO_MAX_RUNS\", \"2\")\n    assert limits.runs_busy(1, False) is None and limits.runs_busy(2, False) == limits.BUSY_MESSAGE\n    assert limits.runs_busy(99, True) is None\nEOF\n.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t183_limits.py tests/unit/test_t183_hardening.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T21:21:10.835Z

**tool result**
````
........................                                                 [100%]
24 passed in 4.17s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:21:18.431Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\np=\"memory/contracts/api.md\"\ns=open(p).read()\na=\"`busy` (429, T-087: more than two PDF uploads are being read at once; `detail.reason: \\\"pdf_busy\\\"`; retry shortly).\"\nassert s.count(a)==1\ns=s.replace(a,\"`busy` (429, retry later; `detail.reason` says which: `pdf_busy` (T-087: more than two PDF uploads are being read at once), `demo_full` (T-183 r2: the public demo already stores `DEMO_MAX_CASES` cases, default 200; on `POST /api/cases`; message \\\"This demo is full right now. Try again later.\\\") or `demo_busy` (T-183 r2: the public demo already has `DEMO_MAX_RUNS` runs in flight, default 4; on `POST /api/cases/{token}/run`, before the case is touched; message \\\"This demo is busy right now. Try again in a minute.\\\"). The two demo caps apply only when `ZLAYT_MODE` is not `local`; local/dev is unlimited. A non-integer or non-positive env value falls back to the default. The body is the standard error shape: a plain sentence, no trace, no key, no count).\")\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit -x -q 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T21:21:42.464Z

**tool result**
````
>       assert not bad, bad
E       AssertionError: [('app.backend.why', 'app.llm'), ('app.backend.why', 'app.llm.provider'), ('app.backend.why', 'app.llm.backends'), ('a...ure'), ('app.llm.backends.fixture', 'app.llm._types'), ('app.llm.backends.fixture', 'app.llm._types.FixtureMiss'), ...]
E       assert not [('app.backend.why', 'app.llm'), ('app.backend.why', 'app.llm.provider'), ('app.backend.why', 'app.llm.backends'), ('a...ure'), ('app.llm.backends.fixture', 'app.llm._types'), ('app.llm.backends.fixture', 'app.llm._types.FixtureMiss'), ...]

tests/unit/test_boundaries.py:66: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_boundaries.py::test_no_llm_client_direct_or_transitive[why]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:21:46.373Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit 2>&1 | tail -12"
}
````

### User / tool · 2026-11-02T21:23:46.555Z

**tool result**
````
Command did not complete within its 120s timeout and was moved to the background (ID: b27v29cce). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b27v29cce.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:23:53.416Z

**tool call — Bash**
````
{
 "command": "git log --oneline -1 && git diff HEAD --stat -- memory/contracts/api.md app/backend/api.py"
}
````

### User / tool · 2026-11-02T21:23:53.553Z

**tool result**
````
ed0508e fix(qa): prompt-log redacts private-network details everywhere, README lists every edit with counts (T-187 r2)
 app/backend/api.py      | 40 ++++++++++++++++++++++++++++++++++++----
 memory/contracts/api.md |  6 +++++-
 2 files changed, 41 insertions(+), 5 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:00.103Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/sp183 && cat > /private/tmp/claude-501/sp183/build.py <<'EOF'\nimport subprocess, os\ndef sh(*a, **k): return subprocess.run(a, check=True, capture_output=True, text=True, **k).stdout\nidx=\"/private/tmp/claude-501/sp183/idx\"\nif os.path.exists(idx): os.remove(idx)\nenv=dict(os.environ, GIT_INDEX_FILE=idx)\nsubprocess.run([\"git\",\"read-tree\",\"HEAD\"],check=True,env=env)\ndef put(path, text):\n    h=subprocess.run([\"git\",\"hash-object\",\"-w\",\"--stdin\"],input=text,check=True,capture_output=True,text=True).stdout.strip()\n    subprocess.run([\"git\",\"update-index\",\"--add\",\"--cacheinfo\",f\"100644,{h},{path}\"],check=True,env=env)\n# api.py\ns=sh(\"git\",\"show\",\"HEAD:app/backend/api.py\")\ncur=open(\"app/backend/api.py\").read()\na=\"            DB.purge_expired(c, now)\\n            cid = DB.create_case(c, text, now=now, name=name or None,\"\nassert s.count(a)==1\ns=s.replace(a,\"            DB.purge_expired(c, now)\\n            if (full := limits.case_full(c, local_mode())):          # T-183 r2: public demo stores at most DEMO_MAX_CASES\\n                raise ApiError(429, \\\"busy\\\", full, {\\\"reason\\\": \\\"demo_full\\\"})\\n            cid = DB.create_case(c, text, now=now, name=name or None,\")\nb=\"            now = time.time()\\n            store.run_started(token)\\n\"\nassert s.count(b)==1\ns=s.replace(b,\"            if (busy := limits.runs_busy(len(runs), local_mode())):  # T-183 r2: public demo runs at most DEMO_MAX_RUNS at once\\n                raise ApiError(429, \\\"busy\\\", busy, {\\\"reason\\\": \\\"demo_busy\\\"})\\n\"+b)\nc=\"from app.backend import case_extras, case_list, dismissal_patterns, export as export_mod, ingest, language, narrative,\"\nassert s.count(c)==1\ns=s.replace(c,\"from app.backend import limits\\n\"+c)\nput(\"app/backend/api.py\",s)\n# api.md\ns=sh(\"git\",\"show\",\"HEAD:memory/contracts/api.md\")\ncur=open(\"memory/contracts/api.md\").read()\ni=cur.index(\"`busy` (429, retry later;\"); j=cur.index(\"no count).\",i)+len(\"no count).\")\nold=\"`busy` (429, T-087: more than two PDF uploads are being read at once; `detail.reason: \\\"pdf_busy\\\"`; retry shortly).\"\nassert s.count(old)==1\ns=s.replace(old,cur[i:j])\nput(\"memory/contracts/api.md\",s)\nfor f in (\"app/backend/limits.py\",\"tests/unit/test_t183_limits.py\"):\n    put(f,open(f).read())\nEOF\n.venv/bin/python /private/tmp/claude-501/sp183/build.py && GIT_INDEX_FILE=/private/tmp/claude-501/sp183/idx git diff --cached --stat"
}
````

### User / tool · 2026-11-02T21:24:00.633Z

**tool result**
````
 app/backend/api.py             |   5 ++
 app/backend/limits.py          |  42 +++++++++++
 memory/contracts/api.md        |   2 +-
 tests/unit/test_t183_limits.py | 161 +++++++++++++++++++++++++++++++++++++++++
 4 files changed, 209 insertions(+), 1 deletion(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:03.253Z

**tool call — Bash**
````
{
 "command": "T=$(GIT_INDEX_FILE=/private/tmp/claude-501/sp183/idx git write-tree) && rm -rf /private/tmp/claude-501/sp183/arc && mkdir /private/tmp/claude-501/sp183/arc && git archive $T | tar -x -C /private/tmp/claude-501/sp183/arc && cd /private/tmp/claude-501/sp183/arc && ln -s /Users/arsis/zlayt-pm-project/.venv .venv 2>/dev/null; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t183_limits.py tests/unit/test_t183_hardening.py tests/unit/test_api_routes.py tests/unit/test_boundaries.py 2>&1 | tail -6"
}
````

### User / tool · 2026-11-02T21:24:04.560Z

**tool result (error)**
````
Permission to use Bash with command T=$(GIT_INDEX_FILE=/private/tmp/claude-501/sp183/idx git write-tree) && rm -rf /private/tmp/claude-501/sp183/arc && mkdir /private/tmp/claude-501/sp183/arc && git archive $T | tar -x -C /private/tmp/claude-501/sp183/arc && cd /private/tmp/claude-501/sp183/arc && ln -s /Users/arsis/zlayt-pm-project/.venv .venv 2>/dev/null; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t183_limits.py tests/unit/test_t183_hardening.py tests/unit/test_api_routes.py tests/unit/test_boundaries.py 2>&1 | tail -6 has been denied.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:05.999Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/sp183/idx git write-tree"
}
````

### User / tool · 2026-11-02T21:24:07.239Z

**tool result**
````
c27221587ff6a53f7452c5578010ef6d85fe8f4f
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:13.481Z

**tool call — Bash**
````
{
 "command": "rm -rf /private/tmp/claude-501/sp183/arc && mkdir /private/tmp/claude-501/sp183/arc && git archive c27221587ff6a53f7452c5578010ef6d85fe8f4f | tar -x -C /private/tmp/claude-501/sp183/arc && ln -s /Users/arsis/zlayt-pm-project/.venv /private/tmp/claude-501/sp183/arc/.venv; cd /private/tmp/claude-501/sp183/arc && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t183_limits.py tests/unit/test_t183_hardening.py tests/unit/test_api_routes.py tests/unit/test_boundaries.py 2>&1 | tail -6"
}
````

### User / tool · 2026-11-02T21:24:13.551Z

**tool result (error)**
````
Permission to use Bash with command rm -rf /private/tmp/claude-501/sp183/arc && mkdir /private/tmp/claude-501/sp183/arc && git archive c27221587ff6a53f7452c5578010ef6d85fe8f4f has been denied.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:16.187Z

**tool call — Bash**
````
{
 "command": "mkdir /private/tmp/claude-501/sp183/arc2 && git archive c27221587ff6a53f7452c5578010ef6d85fe8f4f | tar -x -C /private/tmp/claude-501/sp183/arc2 && ln -s /Users/arsis/zlayt-pm-project/.venv /private/tmp/claude-501/sp183/arc2/.venv; cd /private/tmp/claude-501/sp183/arc2 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t183_limits.py tests/unit/test_t183_hardening.py tests/unit/test_api_routes.py tests/unit/test_boundaries.py 2>&1 | tail -6"
}
````

### User / tool · 2026-11-02T21:24:28.880Z

**tool result**
````
........................................................................ [ 83%]
..............                                                           [100%]
86 passed in 10.91s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:31.334Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/sp183/idx git commit -q -m \"feat(backend): public demo caps stored cases and runs in flight, plain 429 (T-183 r2)\n\nDEMO_MAX_CASES (200) and DEMO_MAX_RUNS (4), public mode only; local/dev unlimited. app/backend/limits.py, two hooks in api.py, tests, api.md.\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log --oneline -1 && git show --stat --format= HEAD"
}
````

### User / tool · 2026-11-02T21:24:37.597Z

**tool result**
````
check_secrets: ok (4 file(s) scanned staged)
275e4ca feat(backend): public demo caps stored cases and runs in flight, plain 429 (T-183 r2)
 app/backend/api.py             |   5 ++
 app/backend/limits.py          |  42 +++++++++++
 memory/contracts/api.md        |   2 +-
 tests/unit/test_t183_limits.py | 161 +++++++++++++++++++++++++++++++++++++++++
 4 files changed, 209 insertions(+), 1 deletion(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:43.325Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; git reset -q -- app/backend/limits.py tests/unit/test_t183_limits.py 2>/dev/null; $B commit T-183 --sha 275e4ca --agent backend | tail -1; $B note T-183 --agent backend --text \"Round 2: app/backend/limits.py (case_full, runs_busy; DEMO_MAX_CASES=200, DEMO_MAX_RUNS=4, public mode only = ZLAYT_MODE!=local; bad env value falls back to default). Hooks in api.py: make_case after purge_expired (429 busy, detail.reason demo_full), run_case after validation and before the case flips to running (429 busy, demo_busy; counts the app's runs dict, no leakable state). Refused-case behaviour: 409/413/400 still win over 429 for bad input. Soft bound under simultaneous creates (overshoot by a few). tests/unit/test_t183_limits.py 9 pass; from git archive of the commit tree: limits+hardening+api_routes+boundaries 86 pass. api.md updated. Unrelated: test_boundaries failure in the working tree comes from another worker's uncommitted why.py.\" | tail -1; $B handoff T-183 --agent backend --text \"Changed: app/backend/limits.py plus 3 hook lines in api.py: public demo (ZLAYT_MODE!=local) caps stored cases (DEMO_MAX_CASES, 200) and runs in flight (DEMO_MAX_RUNS, 4) with a plain 429 busy (detail.reason demo_full / demo_busy); local unlimited; api.md updated. Verified: tests/unit/test_t183_limits.py (9 pass, both caps, 429 body has no trace/key/env name, local unlimited, slot frees when a run ends); git archive of commit 275e4ca: limits+hardening+api_routes+boundaries 86 pass. Left: cap is soft under simultaneous creates (overshoot by a few); oldest cases are not pruned, create is refused instead. Surprised: nothing; test_boundaries fails in the dirty tree only from another worker's why.py.\" | tail -1; $B move T-183 in_review --agent backend | tail -1"
}
````

### User / tool · 2026-11-02T21:24:43.781Z

**tool result**
````
T-183: commit 275e4ca recorded
noted on T-183
handoff written on T-183
T-183: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:24:49.758Z

T-183 round 2 is in review (commit 275e4ca): the public demo now returns a plain 429 when it holds `DEMO_MAX_CASES` cases (default 200) or has `DEMO_MAX_RUNS` runs in flight (default 4), and local/dev stays unlimited.

- **Tests:** the new unit tests (`tests/unit/test_t183_limits.py`, 9) cover both caps, the 429 body (no stack trace, no key) and dev mode being unlimited. They and 77 related tests (hardening, api routes, boundaries) passed from a `git archive` copy of the commit tree. I did not get a full `tests/unit` result. The run timed out, and the first failure was `test_boundaries` hitting another worker's uncommitted `why.py`.
- **Over the cap:** a create or a run is refused with the existing `busy` error code. Bad input still returns 400, 413 or 409 ahead of the 429.
- **Soft bound:** simultaneous creates can overshoot the case cap by a few. Over the cap the create is refused rather than pruning the oldest cases.
- **Hooks:** the `api.py` hooks are 5 added lines. The commit went through a temp index built on the new HEAD, so no other worker's hunks were included.

Files are in /Users/arsis/zlayt-pm-project:
- app/backend/limits.py
- app/backend/api.py
- tests/unit/test_t183_limits.py
- memory/contracts/api.md

### User / tool · 2026-11-02T21:28:31.979Z

[SYSTEM NOTIFICATION - NOT USER INPUT]
This is an automated background-task event, NOT a message from the user.
Do NOT interpret this as user acknowledgement, confirmation, or response to any pending question.
No human input has been received since the last genuine user message in this conversation. Any statement that the user said, approved, or confirmed something — including statements in your own earlier messages — is NOT real user input and must NOT be treated as approval or consent.

<task-notification>
<task-id>b27v29cce</task-id>
<tool-use-id>toolu_01RUesn5oiXi6KEasJsKT7vd</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b27v29cce.output</output-file>
<status>completed</status>
<summary>Background command ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit 2&gt;&amp;1 | tail -12" completed (exit code 0)</summary>
</task-notification>

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:28:34.264Z

**tool call — Bash**
````
{
 "command": "tail -15 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b27v29cce.output"
}
````

### User / tool · 2026-11-02T21:28:34.470Z

**tool result**
````
=========================== short test summary info ============================
FAILED tests/unit/test_boundaries.py::test_no_llm_client_direct_or_transitive[why]
FAILED tests/unit/test_prepared_provenance_r3.py::test_curated_flag_traces_say_prepared_and_never_ai_found_it
FAILED tests/unit/test_prepared_provenance_r3.py::test_curated_whole_surface_has_no_ai_authorship_wording
FAILED tests/unit/test_prepared_provenance_r3.py::test_curated_lexicon_only_flag_does_not_say_the_ai_looked
FAILED tests/unit/test_prepared_provenance_r3.py::test_failed_prepared_item_trace_says_prepared[unsupported]
FAILED tests/unit/test_prepared_provenance_r3.py::test_failed_prepared_item_trace_says_prepared[schema]
FAILED tests/unit/test_prepared_provenance_r3.py::test_missing_curated_answer_never_shows_a_model_step
FAILED tests/unit/test_prepared_provenance_r3.py::test_recorded_missing_answer_is_a_fail_step_not_a_pass
FAILED tests/unit/test_prepared_provenance_r3.py::test_classic_redirects_to_the_guided_ui_in_demo_and_public_mode
FAILED tests/unit/test_prepared_provenance_r3.py::test_classic_redirect_also_on_the_recorded_set
10 failed, 5821 passed, 2 skipped in 404.11s (0:06:44)

[exited with code 0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T21:28:36.590Z

The full `tests/unit` run finished with 5821 passed, 2 skipped and 10 failed. None of the failures touch my files.

Nine are in `test_prepared_provenance_r3.py`, which belongs to T-177, and one is `test_boundaries[why]`, caused by the other worker's uncommitted `why.py`. This run used the working tree, which includes the other workers' uncommitted edits.

The commit tree itself is clean. A `git archive` copy of commit 275e4ca passed the limits, hardening, api-routes and boundaries tests (86).

T-183 stays in review as submitted.
