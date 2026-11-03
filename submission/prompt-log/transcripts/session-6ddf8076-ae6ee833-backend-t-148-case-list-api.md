# Subagent: Backend: T-148 case list API (Backend: T-148 case list API)

Source: `agent-ae6ee833fa92cddfe.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T13:25:11.005Z

You are a backend worker in /Users/arsis/zlayt-pm-project. Claim T-148 with `python3 tools/board.py claim T-148 --agent backend` and read it with `show`. It comes from Chris's request for multi-case management with an overview and a detail view.

**Build GET /api/cases.** It returns every case the local profile can see. For each case include:
- token, title (readable, not a file slug), created and updated times;
- run stage;
- progress: decided and total per kind (entries, flags, amounts);
- HITL call-outs: needs review, edits to check, the count in the could-not-verify tray, and gate blockers and warnings with their plain reasons;
- export_ready.

**Rules.**
- Compute it with the same functions GET case and the gate use, so nothing drifts. Add a test that compares the list summary against GET case and the gate for every library case.
- Local mode only, with no auth and no multi-user; that stays a scope cut.
- Keep it cheap: no LLM calls, and don't re-run the pipeline.
- Document it in memory/contracts/api.md.

**Files.** Other workers have uncommitted changes in shared files (api.py, present.py, store.py, api.md). Put the new logic in its own module, e.g. app/backend/case_list.py, and wire the route with a minimal touch. Commit only your hunks through a temp index (GIT_INDEX_FILE plus `git apply --cached` of your own patch) wherever a file has others' changes.

**Finish.** Write the tests first, then run the full unit suite. Failures from other workers' in-flight amounts and charge-text changes are not yours; note them. Write the handoff and move the card to in_review. Reply in 3 lines.

### User / tool · 2026-11-02T13:25:11.010Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:25:14.359Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-148 --agent backend; python3 tools/board.py show T-148; cat .claude/agent-memory/backend/project_backend_conventions.md; git status --short | head -40"
}
````

### User / tool · 2026-11-02T13:25:14.685Z

**tool result**
````
T-148 claimed by backend
---
id: "T-148"
title: "Multi-case API (Chris inbox 13:23Z): GET /api/cases summary list - per case title, created, run stage, progress (decided/total by kind), HITL call-outs (needs review, edits to check, could-not-verify tray, gate blockers/warnings with plain reasons), export ready"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T13:25:02Z"
updated_at: "2026-11-02T13:25:14Z"
claimed_by: "backend"
claimed_at: "2026-11-02T13:25:14Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "GET /api/cases returns every case the local profile can see, each with the summary fields, computed by the same code as GET case/gate (no drift: a test compares); local mode only, no auth/multi-user (scope cut kept); api.md", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:25:05Z orchestrator: assigned: backend
- 2026-11-02T13:25:14Z backend: claimed

## Handoff (filled when moving to in_review)

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
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/amounts.py
 M app/backend/confidence.py
 M app/backend/export.py
 M app/backend/generator.py
 M app/backend/pipeline.py
MM app/backend/present.py
 M app/backend/review.py
 M app/backend/why.py
 M app/frontend/dom.js
 M app/frontend/export.js
 M app/frontend/flags.js
 M app/frontend/review.css
 M app/frontend/review.js
 M app/frontend/stepper.js
 M app/frontend/timeline.js
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:25:16.961Z

**tool call — Bash**
````
{
 "command": "grep -n \"cases\\|def \\|@app\\|@router\" app/backend/api.py | head -150; wc -l app/backend/api.py app/backend/present.py app/backend/store.py; ls app/backend"
}
````

### User / tool · 2026-11-02T13:25:17.079Z

**tool result**
````
49:    def __init__(self, status, code, message="", detail=None):
54:def digest(text: str) -> str:
58:def recorded_hashes() -> set:
62:def library_cases() -> list:
79:def local_mode() -> bool:
83:def is_loopback_peer(request) -> bool:
93:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
100:    def allowed_hashes():
101:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
112:    def backend():
116:    def live_enabled():
119:    def demo_mode():
122:    def models():
125:    def conn():
128:    def make_call(c, cid):
134:    def pipeline_mod():
140:    def get_case(c, token):
147:    @app.exception_handler(ApiError)
148:    async def _api_error(_, e):
151:    @app.exception_handler(review.ReviewError)
152:    async def _review_error(_, e):
155:    @app.exception_handler(StarletteHTTPException)
156:    async def _http_error(_, e):
160:    @app.exception_handler(Exception)
161:    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log
165:    @app.exception_handler(RequestValidationError)
166:    async def _validation(_, e):
169:    @app.middleware("http")
170:    async def _headers(request, call_next):
171:        if request.url.path.startswith("/api") and time.time() - purged["at"] > 60:     # expired cases vanish even with no create
192:    async def body_of(request: Request) -> dict:
212:    @app.get("/api/health")
213:    def health():
218:    @app.get("/api/cases")
219:    def list_cases():
224:            return {"cases": present.case_list(c)}
228:    @app.get("/api/library")
229:    def library():
232:        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}
234:    @app.post("/api/cases", status_code=201)
235:    async def create_case(request: Request):
242:            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
250:    @app.post("/api/cases/pdf", status_code=201)
251:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):
255:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
282:    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None):
288:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
316:    @app.get("/api/cases/{token}")
317:    def get_case_view(token: str):
325:    @app.delete("/api/cases/{token}", status_code=204)
326:    def delete_case(token: str):
335:    def _run_thread(token, raw):
349:    @app.post("/api/cases/{token}/run", status_code=202)
350:    async def run_case(token: str, request: Request):
358:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
372:    @app.post("/api/cases/{token}/rejudge")
373:    async def rejudge_case(token: str):
383:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
394:    @app.get("/api/cases/{token}/status")
395:    def status(token: str):
413:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
414:    async def confirm_date(token: str, rid: str, request: Request):
425:    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
426:    async def manual_entry(token: str, rid: str, request: Request):
436:    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
437:    async def not_duplicate(token: str, item_id: str, request: Request):
449:    @app.get("/api/cases/{token}/narrative")
450:    def narrative_get(token: str):
458:    @app.post("/api/cases/{token}/narrative")
459:    def narrative_draft(token: str):
471:    @app.post("/api/cases/{token}/narrative/review")
472:    async def narrative_review(token: str, request: Request):
486:    @app.get("/api/cases/{token}/items/{item_id}")
487:    def item(token: str, item_id: str):
498:    @app.post("/api/cases/{token}/items/{item_id}/review")
499:    async def review_item(token: str, item_id: str, request: Request):
519:    @app.get("/api/cases/{token}/export")
520:    def export(token: str, style: str = None):
548:    @app.get("/api/cases/{token}/items/{item_id}/trace")
549:    def item_trace(token: str, item_id: str):
561:    @app.get("/api/cases/{token}/trace")
562:    def case_trace(token: str):
570:    @app.get("/api/cases/{token}/judges")
571:    def judge_report(token: str):
579:    @app.get("/api/cases/{token}/audit")
580:    def audit(token: str):
     592 app/backend/api.py
     377 app/backend/present.py
     101 app/backend/store.py
    1070 total
__init__.py
__pycache__
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
charge_text.py
confidence.py
conflict_candidates.py
conflicts.py
credibility.py
date_convention.py
dates.py
dismissal_patterns.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judge_guard.py
judges.py
language.py
lexicon.py
lexicon_scan.py
narrative.py
overlap.py
pdf_checks.py
pdf_hidden.py
pdf_ocr.py
pdf_routes.py
pdf_text.py
pipeline.py
present.py
reclassify.py
rejudge.py
review.py
schemas.py
sentences.py
spanish.py
spanish_text.py
speaker.py
split_llm.py
store.py
summary_trim.py
totals.py
trace.py
uncovered.py
why.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:25:19.776Z

**tool call — Bash**
````
{
 "command": "sed -n 210,232p app/backend/api.py; sed -n 310,335p app/backend/api.py; git diff HEAD --stat -- app/backend/api.py app/backend/present.py app/backend/store.py memory/contracts/api.md; grep -n \"case_list\" -r app tests memory | head; cat app/backend/store.py"
}
````

### User / tool · 2026-11-02T13:25:19.941Z

**tool result**
````
    # -------------------------------------------------- routes
    @app.get("/api/health")
    def health():
        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}

    @app.get("/api/cases")
    def list_cases():
        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
            raise ApiError(404, "not_found", "Not found.")
        c = conn()
        try:
            return {"cases": present.case_list(c)}
        finally:
            c.close()

    @app.get("/api/library")
    def library():
        if not local_mode():
            raise ApiError(404, "not_found", "Not found.")
        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}
                    "gap_flags": [f["id"] for f in flags if f["type"] == "gap"],
                    "record_warning_flags": [f["id"] for f in flags if f["type"] == "record_warning"],
                    "warnings": ing["warnings"]}
        finally:
            c.close()

    @app.get("/api/cases/{token}")
    def get_case_view(token: str):
        c = conn()
        try:
            get_case(c, token)
            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
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
 memory/contracts/api.md | 16 ++++++++++++++--
 1 file changed, 14 insertions(+), 2 deletions(-)
app/backend/present.py:366:def case_list(conn):
app/backend/api.py:224:            return {"cases": present.case_list(c)}
tests/unit/test_calibration_route.py:117:    "case_count_not_the_case_list": lambda d: d.update(case_count=500),
tests/unit/test_api_routes.py:285:def test_case_list_and_library_exist_only_in_local_mode(env, monkeypatch):
tests/e2e/test_local_mode.py:39:def test_case_list_and_library_exist_in_local_mode_only(local):
"""DB <-> unit-dict adapters shared by the API layer and the pipeline (T-040). Pure functions plus ingest persistence.

Item/record ids are the pipeline's own ("r6", "e5", "f_gap_r6_r7"); see the id-collision note on T-040.
"""
from app.backend import ingest, pdf_text, spanish
from app.db import db as DB


def iso(t) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(float(t or 0), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_records(conn, case_id: str, raw: str = None) -> list:
    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
    if raw is None:
        raw = DB.get_case(conn, case_id)["raw_text"]
    out = []
    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
        d = DB._decode(r)
        block = raw[d["char_start"]:d["char_end"]]
        try:
            body = ingest.split_records(block)[0]["excerpt"]
        except Exception:
            body = block
        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
                    "kind": "encounter" if d["encounter"] else "other", "date_candidates": d["date_candidates"] or []})
    return out


def _by_id(records):
    return {r["id"]: r for r in records}


# ---------------------------------------------------------------- unit dicts for export / totals
def export_case(conn, case_id: str) -> dict:
    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
    case = DB.get_case(conn, case_id)
    recs = load_records(conn, case_id, case["raw_text"])
    n_of = {r["id"]: r["n"] for r in recs}
    rec_of = {r["id"]: r for r in recs}
    from app.backend import review as review_mod        # lazy: review imports store
    ents = []
    for e in DB.list_items(conn, case_id, "entry"):
        if e["state"] == "rejected":
            continue
        ed = e.get("edited") or {}
        d = dict(id=e["id"], record_ids=e["record_ids"], record_no=n_of.get((e["record_ids"] or [None])[0], 0), summary=ed.get("summary", e["summary"]),
                 excerpt=ed.get("excerpt", e["excerpt"]), review_status=e["review_status"], date_iso=e["date_iso"])
        if "summary" in ed:
            d["original_summary"] = ed.get("original_summary", e["summary"])
            orig_fails = review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), dict(e, edited={"summary": d["original_summary"], "excerpt": ed.get("original_excerpt", e["excerpt"])}, state_reasons=[]))
            if orig_fails:          # the AI wording that was replaced failed a code check: the notes say so but never print it
                d["original_summary_failed"] = [review_mod.CHECK_PHRASE[c] for c in orig_fails]
        if "excerpt" in ed:
            d["original_excerpt"] = ed.get("original_excerpt", e["excerpt"])
        lad = e.get("ladder") or {}
        if review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), e):      # D-051: an unreviewed draft that fails a code check never has its wording printed
            d["code_check_failed"] = True
        if lad.get("entered_by"):
            d["entered_by_reviewer"] = True
        if e["state"] == "needs_review" and any(k in ed for k in ("summary", "excerpt")):
            d["edit_state_reasons"] = list(e.get("state_reasons") or [])          # T-134: why her edit is still marked for review; the notes keep it after she accepts
        if review_mod.edit_unconfirmed("entry", e):          # T-134: reworded and still needs_review: not decided. Out of the letter and counted as pending (D-045a); the notes name why.
            d["review_status"] = "pending"
            d["edit_unconfirmed"] = True
        if lad.get("translation"):          # D-042: the summary of a Spanish record is a translation; the letter says so
            d["translation_label"] = spanish.translation_info("es", "summary" in ed or bool(lad["translation"].get("human_written")))["label"]
        ents.append(d)
    amts = [dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
                 excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
    fl = []
    for f in DB.list_items(conn, case_id, "flag"):
        if f["state"] == "rejected":        # D-053/D-057: every tray flag (judge-rejected, not word for word, rule-filtered) is not an item to review, count or export; its quote may not be in the record
            continue
        c = f.get("computed") or {}
        ev = [dict(record_no=x.get("record_no") or n_of.get(x.get("record_id"), 0), field=x.get("field", "excerpt"),
                   excerpt=x.get("excerpt") or x.get("text")) for x in f.get("evidence") or []]
        fl.append(dict(id=f["id"], type=f["type"], subtype=c.get("subtype") or f["category"], evidence=ev, review_status=f["review_status"],
                       days=c.get("days"), from_date=c.get("from_date"), to_date=c.get("to_date"), note=f.get("reviewer_note")))
    events = []     # D-047: no 'keep my wording' event exists any more
    pending = sum(1 for x in ents + amts + fl if x["review_status"] == "pending")
    pages = (case.get("config") or {}).get("pages")
    records = [dict(n=r["n"], source=r["source"], date_iso=r["date_iso"], excerpt=r["excerpt"],
                    **({"page": pdf_text.page_for(pages, r["char_start"])} if pages else {})) for r in recs]
    nar = (case.get("config") or {}).get("narrative")
    out = dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events)
    from app.backend import trace                       # lazy: trace imports store
    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
    from app.backend import overlap                      # lazy: overlap imports amounts and dates only
    ov = overlap.view(conn, case_id)                      # T-110: statement line vs a separately stated charge of the same kind; code only, never changes a figure
    if ov:
        out["possible_overlaps"] = [dict(o, statement_record_no=n_of.get(o["statement_record_id"], 0), covered_record_no=n_of.get(o["covered_record_id"], 0)) for o in ov]
    ec = (case.get("config") or {}).get("export")
    if ec:
        out["export_config"] = ec
    if nar:
        out["narrative"] = {"status": nar["status"], "basis": nar.get("basis", {}), "removed": nar.get("removed", []),
                            "sentences": [{"text": x["text"], "entry_id": x["entry_id"], "cite": x.get("cite")} for x in nar.get("sentences", [])]}
    return out
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:25:23.236Z

**tool call — Bash**
````
{
 "command": "sed -n 255,377p app/backend/present.py; git diff HEAD -- app/backend/present.py | head -80; grep -n \"cases\" memory/contracts/api.md | head -30"
}
````

### User / tool · 2026-11-02T13:25:23.383Z

**tool result**
````
        return 0, "", NO_UNITS_LAYOUT
    m = ingest._F_EXC.search(block)
    i = block.find(body, m.end() if m else 0)
    if i < 0:
        return 0, "", NO_UNITS_LAYOUT
    return i, body, None


def quote_units(body, rec):
    """Whole-sentence spans of `body` the quote picker offers. A sentence that a hedge sentence qualifies cannot be saved without it
    (EXCERPT_OMITS_QUALIFIER), so it is offered as ONE combined unit with the hedge sentence(s) that follow it: the same check the save
    routes run (language module for the record, Spanish hedge words included) decides, so every unit offered saves on its own."""
    check = spanish.module_for(language.record_lang(rec)).check_excerpt
    spans = sentences.stripped_spans(body)
    out, i = [], 0
    while i < len(spans):
        j = i
        while j + 1 < len(spans) and "EXCERPT_OMITS_QUALIFIER" in check(body, body[spans[i][0]:spans[j][1]]):
            j += 1
        out.append((spans[i][0], spans[j][1]))
        i = j + 1
    return out


def case_view(conn, case_id, *, backend, models, demo_mode):
    case = DB.get_case(conn, case_id)
    raw = case["raw_text"]
    recs = list(_recs_by_id(conn, case_id).values())
    its = all_items(conn, case_id)
    ents = its["entry"]
    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))      # T-110 r2: a record the paralegal entered by hand leaves the tray
    live_e = [e for e in ents if e["state"] != "rejected"]
    dated = sorted((e for e in live_e if e["date"] and (e["date_status"] in ("parsed", "confirmed", None))), key=lambda e: (e["date"], e["seq"] or 0))
    undated = [e for e in live_e if e not in dated]
    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
             "attempt": {"summary": x.get("summary"), "excerpt": x.get("excerpt")} if k == "entry" else {"text": x.get("text"), "excerpt": x.get("excerpt")},
             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected" and x["id"] not in handled]
    # D-053: a flag the judge rejected (a model-only flag J4 disagreed with, a code conflict candidate J3 called benign, a model-proposed conflict) is a tray
    # item of kind "flag": the model's attempt is the title and the quote(s); it is never in `flags`, the review queue or the letter.
    def _tray_flag(x):
        return {"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
                "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
                "flag": {"type": x["type"], "category": x["category"]},
                "attempt": {"summary": x.get("title"), "excerpt": " / ".join(e["excerpt"] for e in x["evidence"] if e.get("excerpt"))},
                "ladder": {"item_id": x["id"], "state": "rejected"}}
    rejected_flags = [x for x in its["flag"] if x["state"] == "rejected"]
    filtered = [x for x in rejected_flags if FT.is_filtered(x["reasons"])]
    tray += [_tray_flag(x) for x in rejected_flags if x not in filtered]
    # D-057: model proposals a code rule filtered out are a collapsed, counted group of their own (never in `tray`, `flags`, the queue or the letter)
    rules = []
    for cat in sorted({x["category"] for x in filtered}):
        ref, name, text = FT.FILTER_RULES.get(cat, ("", cat, ""))
        items = [_tray_flag(x) for x in filtered if x["category"] == cat]
        rules.append({"rule": cat, "ref": ref, "label": name, "explanation": text, "count": len(items), "items": items})
    tray_filtered = {"label": "Filtered by rule", "collapsed": True, "needs_action": False, "count": len(filtered), "rules": rules}
    err = json.loads(case["error"]) if case.get("error") else None
    injected = [r["id"] for r in recs if r["injection_tag"]]
    record_views = [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs]
    uncovered.attach(record_views, ents, quote_body)      # T-143: clinical sentences no entry quote covers (review aid; never in the letter or notes)
    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
            "records": record_views, "undated_entries": undated, "entries": dated,
            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks(), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
            "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
            "review": review_view(conn, case_id), "warnings": [], "error": err,
            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
            **{k: (case.get("config") or {})[k] for k in ("pdf_checks",) if (case.get("config") or {}).get(k)},     # T-086/T-087 (PDF cases only)
            **({"pdf_pages": (case.get("config") or {})["pages"]} if (case.get("config") or {}).get("pages") else {})}


def why_view(conn, case_id, item_id):
    item = item_view(conn, case_id, item_id)
    recs = _recs_by_id(conn, case_id)
    ids = list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])
    seen, src = set(), []
    for rid in ids:
        if rid in recs and rid not in seen:
            seen.add(rid)
            r = recs[rid]
            hs, he = item.get("excerpt_start"), item.get("excerpt_end")
            src.append({"record_id": rid, "char_start": r["char_start"], "char_end": r["char_end"], "highlight_start": hs, "highlight_end": he})
    calls = [_call(c) for c in DB.list_llm_calls(conn, case_id, item_id)]
    events = [{"action": e["action"], "at": store.iso(e["at"])} for e in DB.list_events(conn, case_id, item_id)]
    return {"item": item, "source": src, "calls": calls, "events": events}


def _call(c, full=False):
    rf = c.get("recorded_from")
    d = {"id": c["id"], "role": c["role"], "step": c["step"], "backend": c["backend"], "recorded_from": rf, "model": c["model"],
         "prompt_version": c["prompt_version"], "prompt_sha256": c["prompt_sha256"], "item_id": c["item_id"], "attempt": c["attempt"],
         "latency_ms": c["latency_ms"], "cost_usd": c["cost_usd"], "tokens_in": c["tokens_in"], "tokens_out": c["tokens_out"],
         "parsed_ok": bool(c["parsed_ok"]), "verdict": c["verdict"]}
    if full:
        d.update(system_text=c["system_text"], user_text=c["user_text"], response_raw=c["response_raw"], error=c["error"])
    return d


def audit_view(conn, case_id, full=False):
    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
    calls = DB.list_llm_calls(conn, case_id)
    by = {}
    for c in calls:
        by[c["backend"]] = by.get(c["backend"], 0) + 1
    return {"token": case_id, "calls": [_call(c, full) for c in calls],
            "events": [{"id": e["id"], "item_id": e["item_id"], "action": e["action"], "at": store.iso(e["at"]),
                        **({"before": e["before"], "after": e["after"]} if full else {})}
                       for e in DB.list_events(conn, case_id)],
            "summary": {"calls": len(calls), "cost_usd": round(sum(c["cost_usd"] or 0 for c in calls), 6),
                        "latency_ms_total": sum(c["latency_ms"] or 0 for c in calls), "by_backend": by}}


def case_list(conn):
    """Local mode only (D-008/D-031): newest first. Metadata and counts, never record text."""
    out = []
    for r in conn.execute("SELECT id FROM cases ORDER BY created_at DESC, rowid DESC"):
        cid = r["id"]
        case = DB.get_case(conn, cid)
        counts = review_view(conn, cid)["counts"]
        out.append({"token": cid, "name": case["name"], "status": case["status"], "source": case["source"],
                    "record_count": conn.execute("SELECT count(*) FROM records WHERE case_id=?", (cid,)).fetchone()[0],
                    "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},
                    "created_at": store.iso(case["created_at"])})
    return out
18:| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
19:| GET | `/api/cases/{token}` | the whole case for the review screen |
20:| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
21:| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
22:| GET | `/api/cases/{token}/status` | stage and progress |
23:| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
24:| GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |
25:| POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |
26:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an unlocatable quote is a hard `422 invalid_edit` with `detail.reason` and `detail.tokens`/`detail.qualifiers`, no override; a judge objection saves the entry as `pending`/`needs_review` with a `warnings[]` code, no 409); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
27:| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
28:| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
29:| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
30:| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
31:| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
32:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/verbatim/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending "Edit the summary to match the quote." (a summary check) or "Change the quote to whole sentences of the record that keep the hedge sentence." (a quote check), `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}` (`EDIT_QUOTE` when the first failing check is on the quote: `GROUNDING_EXCERPT_NOT_VERBATIM`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`); the judge verdict does not matter. **T-098 r3: the same guard runs on every action that leaves an entry accepted or edited, from one function (`review.set_review`):** `accept`, `edit` (which implies accept, including a summary-only edit and a quote edit; the check runs on the wording the edit would leave, before any write, so a summary-only edit cannot clear a failing quote and never wipes a stored quote-level reason) and batch accept. `reset` and `dismiss` leave the item out of the letter and are never blocked |
33:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
34:| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
35:| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
36:| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `ns…` |
37:| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
38:| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
39:| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconciled rows, skipped records (an EOB service row is a line); no sums or comparisons of any kind, no provider totals or complete flag; internal view, never in the letter |
40:| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
56:`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every view and `ai_banner` on the review view; in live mode it also shows "Pasted text is deleted after `retention_hours` hours" with a Delete now button.
58:## POST /api/cases
63:Request text is normalised first (CRLF and CR become LF; leading/trailing whitespace trimmed). **In demo mode the text is accepted only if its sha256 is in the recorded set (the sample and the golden cases); otherwise `409 demo_mode_unsupported_input` is returned before anything is stored** (D-020). Response 201 (all code: records, dates, duplicates, amounts, gap flags exist before any model call):
76:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`. **Both fields are on every record of `POST /api/cases` and `GET /api/cases/{token}`** (`false` for a real record); the `UNSPLIT_TEXT` warning is in the POST response only. A re-run after a record number came to name different text resets the paralegal's decisions on items that cite it to `pending` (the review event keeps what they were) and removes the stale items), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
78:## POST /api/cases/pdf (D-031)
79:Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
83:Query on `POST /api/cases/pdf`: `include_hidden` = `all` or a page list such as `2,5` (pages whose hidden text the paralegal confirmed; default none) and `ocr=true` (read scanned pages with local Tesseract; default off). Both are decided by re-posting the same file, which creates a new case (ingest is code only, so it costs no model call). Limits: OCR reads at most 10 scanned pages per upload, 150 s in all, nothing leaves the server. A page larger than 40 inches on a side is refused (`ocr_page_too_large`, `detail.page`); a larger one under that is rendered smaller than 150 dpi (longest side at most 3500 px, area at most 8 million px); all page images of one upload together are capped at 12 MB (`ocr_images_too_large`). Tesseract runs with a scrubbed environment (no API key or token reaches it). One deadline (10 s, or 165 s with OCR) covers text reading, the hidden-text scan and OCR; when it passes the work stops and the response is `400 bad_request` with `detail.reason: "pdf_timeout"`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:25:27.190Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/backend/present.py | grep -n \"def case_list\"; grep -n \"def review_view\" -A45 app/backend/present.py; sed -n 394,412p app/backend/api.py; grep -n \"def export_blockers\" -B3 -A60 app/backend/trace.py"
}
````

### User / tool · 2026-11-02T13:25:27.321Z

**tool result**
````
366:def case_list(conn):
194:def review_view(conn, case_id):
195-    items = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, case_id, k)]
196-    handled = generator.resolved_placeholders([r for k, r in items if k == "entry"])
197-    items = [(k, r) for k, r in items if r["id"] not in handled and not FT.is_filtered(r.get("state_reasons"))]       # D-057: rule-filtered proposals need no action and are not counted
198-    live = [(k, r) for k, r in items if r["state"] != "rejected"]
199-    counts = {s: sum(1 for _, r in live if r["review_status"] == s) for s in ("pending", "accepted", "edited", "dismissed")}
200-    counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
201-    counts["edit_to_check"] = sum(1 for k, r in live if review.edit_unconfirmed(k, r))      # T-134: counted in `edited`, but open: not in the letter, not accepted
202-    rank = {"amount": 0, "entry": 1, "flag": 2}
203-    pend = sorted((x for x in live if x[1]["review_status"] == "pending"),
204-                  key=lambda x: (confidence.sort_key(x[1]["state"]), rank[x[0]], x[1].get("date_iso") or "", x[1]["id"]))
205-    return {"counts": counts, "queue": [r["id"] for _, r in pend],
206-            "ready_to_export": counts["pending"] == 0 and counts["edit_to_check"] == 0 and (counts["accepted"] + counts["edited"] - counts["edit_to_check"]) > 0}
207-
208-
209-def dates_to_confirm(conn, case_id):
210-    recs = list(_recs_by_id(conn, case_id).values())
211-    raw = DB.get_case(conn, case_id)["raw_text"]
212-    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"],
213-             "suggestion": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)
214-            for r in recs if r["date_status"] in ("ambiguous", "missing")]
215-
216-
217-def record_view(r, raw, with_sentences=True, pages=None):
218-    block = raw[r["char_start"]:r["char_end"]]
219-    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
220-         "date_status": r["date_status"], "date_candidates": r["date_candidates"] or [], "duplicate_of": r["duplicate_of"],
221-         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
222-         "char_end": r["char_end"], "text": block, "language": language.block_lang(block),
223-         "unsplit": bool(r.get("unsplit")), "preamble": bool(r.get("preamble"))}      # T-129: text outside any recognised record (D-027); a preamble sits above the first real record
224-    if pages:                                    # PDF source (D-031): the page where the record starts
225-        v["page"] = pdf_text.page_for(pages, r["char_start"])
226-        from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR
227-        v["ocr_derived"] = pdf_checks.is_ocr_span(pages, r["char_start"], r["char_end"])
228-    if with_sentences:
229-        base, body, why_none = quote_body(block)  # T-108: units come from the quotable body only, the same text the save route checks the quote against
230-        units = [] if why_none else quote_units(body, {**r, "excerpt": body})
231-        v["sentences"] = [{"text": body[a:b], "start": r["char_start"] + base + a, "end": r["char_start"] + base + b} for a, b in units]
232-        if why_none:
233-            v["sentences_reason"] = why_none           # no sentence is offered; the reason is plain words for the review screen
234-    return v
235-
236-
237-NO_UNITS_LAYOUT = ("No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, "
238-                   "so a quote cut from it could not be checked against the record. Read the record text instead.")
239-_LABEL_LINE = re.compile(r"^[ \t]*(?:Excerpt:|Date:|Source:|=== Record \d+ ===)", re.MULTILINE)
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
                    "progress": {"done": done, "total": len(stages), "label": f"Step {done + 1} of {len(stages)}: {stage}" if stage else ""},
                    "counts": {"entries": len(DB.list_items(c, token, "entry")), "amounts": len(DB.list_items(c, token, "amount")),
                               "flags": len(DB.list_items(c, token, "flag"))},
                    "error": json.loads(case["error"]) if case["error"] else None,
                    "elapsed_ms": int((end - case["run_started_at"]) * 1000) if case["run_started_at"] else 0}
        finally:
            c.close()

1105-            f"not in the letter and {'are' if n != 1 else 'is'} not counted as accepted until you compare {'them' if n != 1 else 'it'} with the quote and accept.")
1106-
1107-
1108:def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
1109-    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
1110-    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
1111-    cx = cx or _Cx(conn, case_id, False)
1112-    rv = rv or present.review_view(conn, case_id)
1113-    out = []
1114-    if cx.running:
1115-        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
1116-    if cx.case["status"] == "failed":
1117-        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
1118-    out.extend(code_check_blockers(conn, case_id, cx))         # D-045(b): the paralegal's own wording is exempt from the judge, not from the code checks
1119-    if cx.ran and not cx.running:
1120-        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
1121-    if not (rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0)):       # T-134: an edit not yet accepted is not accepted
1122-        out.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": TRACE_WHY["NOTHING_ACCEPTED"], "next_action": na("DECIDE", {"view": "queue"})})
1123-    return out
1124-
1125-
1126-def rows_any(jr):
1127-    return bool(jr["totals"]["items_judged"] or jr["totals"]["unavailable"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:25:27.767Z

**tool call — Bash**
````
{
 "command": "sed -n 519,548p app/backend/api.py; sed -n 62,80p app/backend/api.py; grep -n \"def edit_unconfirmed\" -A12 app/backend/review.py; grep -n \"name\" app/backend/api.py | sed -n 1,40p"
}
````

### User / tool · 2026-11-02T13:25:27.899Z

**tool result**
````
    @app.get("/api/cases/{token}/export")
    def export(token: str, style: str = None):
        from app.backend import export_routes as XR
        if style not in (None, *export_mod.STYLES):          # T-121: ?style=oneline | standard
            raise ApiError(422, "invalid_style", XR.invalid_style_message())
        c = conn()
        try:
            get_case(c, token)
            case = store.export_case(c, token)
            try:
                ex = XR.export_payload(token, case, style=style)
            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
            calls = DB.list_llm_calls(c, token)
            ok = ("accepted", "edited")
            tv = present.totals_view(c, token)
            ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
            ex["excluded"] = {"pending": case["pending_count"], "edit_not_confirmed": sum(1 for x in case["entries"] if x.get("edit_unconfirmed")),      # T-134: part of `pending`
                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
                              "rejected": present.rejected_count(c, token)}
            ex["provenance"] = {"generator_model": models()["generator"], "judge_model": models()["judge"], "backend": backend(),
                                "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
                                "edited_count": sum(1 for x in case["entries"] if x["review_status"] == "edited")}
            return ex
        finally:
            c.close()

    @app.get("/api/cases/{token}/items/{item_id}/trace")
def library_cases() -> list:
    """Synthetic case library (evals/library, same file format as evals/golden: <id>.txt + optional <id>.expected.json). Falls back to
    evals/golden until the library exists. [{id, name, description, path}]"""
    base = LIBRARY if any(LIBRARY.glob("*.txt")) else GOLDEN
    out = []
    for p in sorted(base.glob("*.txt")):
        meta = {}
        ej = p.with_name(p.stem + ".expected.json")
        if ej.exists():
            try:
                meta = json.loads(ej.read_text())
            except ValueError:
                meta = {}
        out.append({"id": p.stem, "name": meta.get("name") or p.stem.replace("_", " "), "description": (meta.get("description") or "")[:240], "path": p})
    return out


def local_mode() -> bool:
    return os.environ.get("ZLAYT_MODE") == "local"
81:def edit_unconfirmed(kind: str, item: dict) -> bool:
82-    """T-134 (D-045b, D-051): an ENTRY the paralegal reworded or re-quoted whose state is still needs_review (the second check did not run or did not agree, or another
83-    reason such as OCR or a translation keeps it open). Her edit saved it, but she has not yet said she compared it with the quote, so it has not been decided: it is
84-    not in the letter, not counted as accepted, and the notes do not say she accepted it. Her explicit accept (review_status accepted) ends it; that accept is bound
85-    by the code checks (set_review). One source for the item view, the review counts, the export and the gate."""
86-    return (kind == "entry" and item.get("review_status") == "edited" and item.get("state") == "needs_review"
87-            and any(k in (item.get("edited") or {}) for k in ("summary", "excerpt")))
88-
89-
90-def code_check_failures(rec, item: dict) -> dict:
91-    """{reason_code: detail} for every D-034/D-047/D-022 code check the entry's CURRENT summary and quote fail. Recomputed from the text (same
92-    functions the generator and the edit route use), plus any such reason already stored on the item, so old data cannot slip through.
93-    `rec` is a store.load_records() dict (None: only the stored reasons count)."""
64:    evals/golden until the library exists. [{id, name, description, path}]"""
69:        ej = p.with_name(p.stem + ".expected.json")
75:        out.append({"id": p.stem, "name": meta.get("name") or p.stem.replace("_", " "), "description": (meta.get("description") or "")[:240], "path": p})
95:    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
114:        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says
162:        log.error("unhandled %s", type(e).__name__)
184:            log.error("unhandled %s", type(e).__name__)
248:        return make_case(text, b.get("name") if isinstance(b.get("name"), str) else (lib["name"] if lib else None), sample)
251:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):
278:        out = make_case(got["text"], name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None})
282:    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None):
293:            name = name if isinstance(name, str) else ("Sample case" if sample else None)
294:            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None,
305:                log.error("create failed %s", type(e).__name__)
307:            return {"token": cid, "name": DB.get_case(c, cid)["name"], "status": "ingested", "source": "sample" if sample else "paste",
591:        app.mount("/", StaticFiles(directory=str(sd), html=True), name="frontend")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:25:31.114Z

**tool call — Bash**
````
{
 "command": "grep -n \"gate\\|warnings\" app/backend/trace.py | head -60; sed -n 561,570p app/backend/api.py; grep -n \"name\" app/db/db.py | head -20"
}
````

### User / tool · 2026-11-02T13:25:31.209Z

**tool result**
````
4:case_trace(conn, case_id, full)           the pipeline: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate.
250:    if review.edit_unconfirmed(kind, row):      # T-134 r2: her edit is saved but she has not accepted it; the trail must not say she did (same rule as the gate, the export and the notes)
282:    gated = [s for s in steps if s["kind"] == "code" and s["status"] == FAIL and s.get("blocks_export")]      # D-045(b): human wording whose code check fails
285:        first_na = gated[0]["next_action"] if gated else (next((s["next_action"] for s in steps if s["id"] == "human"), None) if open_edit else None)     # the human already decided; step-level hints stay on the steps, except a failing code check on their own wording
286:    if gated:      # whose words: only the paralegal's own summary is "your wording"; an AI draft is "this summary"
305:    blocks = blocks or bool(gated)
423:    if _code_check_gated(row):        # D-045(b), D-051: a failing code check blocks the export (AI-made or human wording; only the judge is exempt for human wording) and says what to do
432:def _code_check_gated(row) -> bool:
434:    state reached some other way; the gate does not trust that the accept guard ran."""
463:    One blocker per item, reason_code = its first failing check; `failed_steps` lists every failing step. Same steps the item trace shows, so gate and trace agree."""
467:        if not _code_check_gated(row):
738:    """UnknownItem for an id that is not in the case. Entry, amount, flag or narrative sentence (ns...). Any other error is a bug and propagates."""
790:    Decided from the item's steps so /judges can never disagree with the item traces (a gate never passes over a check that did not run)."""
837:    No second AI check is needed for that, so a missing one never blocks export. The one source for the amount view's `accept_effect` and the gate."""
1057:    # 10 export gate
1067:    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"] - n_edit, "edit_not_confirmed": n_edit,
1069:    warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
1072:        warnings.append({"reason_code": "EDIT_NOT_CONFIRMED", "count": n_edit, "why": edit_warning(n_edit, n_ai), "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])})
1074:        gate = step("export_gate", "Ready to export?", "code", PASS,
1077:                    rule="row 19", counts=gate_counts)
1082:        gate = step("export_gate", "Ready to export?", "code", FAIL, text, reason=first["reason_code"], rule="row 19", counts=gate_counts, next_action=first["next_action"],
1084:    gate.update(ready=ready, blockers=blockers, warnings=warnings)
1085:    st.append(gate)
1110:    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
    @app.get("/api/cases/{token}/trace")
    def case_trace(token: str):
        c = conn()
        try:
            get_case(c, token)
            return trace.case_trace(c, token, full=local_mode())
        finally:
            c.close()

    @app.get("/api/cases/{token}/judges")
4:- get_item() returns columns with `_json` decoded under the stripped name (ladder_json -> "ladder", edited_json -> "edited").
26:_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")
61:            conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='review_events'").fetchone():
107:    return {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
114:def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
116:    row = {"id": cid, "name": name, "source": source, "raw_text": raw_text, "text_sha256": sha256(raw_text),
151:    """Insert an entry/amount/flag. payload keys must be column names (dicts/lists JSON-encoded). New items are pending."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:25:33.075Z

**tool call — Bash**
````
{
 "command": "sed -n 1000,1100p app/backend/trace.py; grep -n \"def case_trace\" -A25 app/backend/trace.py | head -60; grep -n \"class _Cx\" -A30 app/backend/trace.py | head -50"
}
````

### User / tool · 2026-11-02T13:25:33.212Z

**tool result**
````
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"view": "tray"})))
    elif not allitems:
        st.append(step("grounding", "Every quote and amount is in the record", "code", PENDING, "There is nothing to check yet.", rule="row 4", counts=gcounts, next_action=na("RERUN")))
    else:
        st.append(step("grounding", "Every quote and amount is in the record", "code", PASS, f"All {len(allitems)} items cite text that is in the record, character for character.", rule="row 4", counts=gcounts))
    # 6 judges
    t = jr["totals"]
    jcounts = dict(t)
    objections = t["unsupported"] + t["unsure"]
    if not rows_any(jr) and not cx.ran:
        st.append(step("judges", "Second AI check on every AI-made item", "llm", PENDING, "The second check has not run yet.", rule="row 4", counts=jcounts, next_action=na("RERUN")))
    elif t["unavailable"]:
        msg = f"{t['unavailable']} item{'s have' if t['unavailable'] != 1 else ' has'} not been double-checked. "
        if cx.running:
            st.append(step("judges", "Second AI check on every AI-made item", "llm", PENDING, msg + "The run is still going.", reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts))
        else:
            st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, msg + reason_text("JUDGE_UNAVAILABLE"),
                           reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts, next_action=na("RERUN_JUDGE", {"view": "judges"})))
    elif objections:
        st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, f"The second check questioned {objections} of {t['items_judged']} items; they are marked for review.",
                       reason="JUDGE_UNSUPPORTED" if t["unsupported"] else "JUDGE_UNSURE", rule="row 4", counts=jcounts, next_action=na("COMPARE_BY_HAND", {"view": "judges"})))
    else:
        st.append(step("judges", "Second AI check on every AI-made item", "llm", PASS, f"The second check agreed with all {t['items_judged']} items it checked.", rule="row 4", counts=jcounts))
    # 7 flags
    fc = {"total": len(flgs), "by_type": _count_by(flgs, "type"), "by_origin": _count_by(flgs, "origin")}
    if any(f["category"] == "analysis_incomplete" for f in flgs):
        st.append(step("flags", "Gaps, conflicts and wording flags", "code", FAIL, reason_text("CONFLICT_CHECK_INCOMPLETE"), reason="CONFLICT_CHECK_INCOMPLETE", rule="row 11", counts=fc,
                       next_action=na("RERUN")))
    elif not cx.ran:
        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PENDING, "Gaps and date conflicts are ready (code). The AI and phrase-list pass has not run.", rule="row 9", counts=fc,
                       next_action=na("RERUN")))
    else:
        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PASS, f"{len(flgs)} flag{'s' if len(flgs) != 1 else ''}: dates compared by code, wording found by the phrase list and the AI.", rule="row 9", counts=fc))
    # 8 totals
    tv = present.totals_view(conn, case_id)
    pend_ch = tv["pending"]["count"]
    tcounts = {"accepted_cents": tv["accepted"]["cents"], "accepted_count": tv["accepted"]["count"], "pending_cents": tv["pending"]["cents"], "pending_charges": pend_ch,
               "not_totaled": len(tv["not_totaled"])}
    if not amts:
        st.append(step("totals", "Billed-charges total", "code", SKIPPED, "No dollar amounts were found.", rule="row 8", counts=tcounts))
    elif pend_ch:
        st.append(step("totals", "Billed-charges total", "code", PENDING, f"{pend_ch} detected charge{'s' if pend_ch != 1 else ''} not in the total until you accept {'them' if pend_ch != 1 else 'it'}. The total is added up by code from accepted charges only.",
                       reason="PENDING_DECISION", rule="row 8", counts=tcounts, next_action=na("DECIDE", {"view": "amounts"}, ["accept", "dismiss"])))
    else:
        st.append(step("totals", "Billed-charges total", "code", PASS, "The total is added up by code from the accepted charges.", rule="row 8", counts=tcounts))
    # 9 review
    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed", "edit_to_check")}
    if rc["pending"]:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{rc['pending']} item{'s are' if rc['pending'] != 1 else ' is'} waiting for your decision.", reason="PENDING_DECISION",
                       rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    elif rc["edit_to_check"]:           # T-134: her reworded entry is still marked Needs review; it is not decided until she accepts it
        n = rc["edit_to_check"]
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm "
                       f"{'them' if n != 1 else 'it'}). Compare {'them' if n != 1 else 'it'} with the quote and accept, or the {'entries stay' if n != 1 else 'entry stays'} out of the letter.",
                       reason="EDIT_NOT_CONFIRMED", rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    else:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
    # 10 export gate
    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
    ccf = [b for b in blockers if b.get("step_id")]             # D-045(b): the paralegal's own wording fails a code check
    live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
    n_ai = sum(1 for k, x in allitems if ai_summary_unchecked(k, x))
    n_edit = rv["counts"].get("edit_to_check", 0)                # T-134: reworded, still Needs review, not accepted: not in the letter, so it warns like a pending item
    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
    ready = not blockers
    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"] - n_edit, "edit_not_confirmed": n_edit,
                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf)}
    warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
                 "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])}] if n_pend else []
    if n_edit:
        warnings.append({"reason_code": "EDIT_NOT_CONFIRMED", "count": n_edit, "why": edit_warning(n_edit, n_ai), "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])})
    if ready:
        gate = step("export_gate", "Ready to export?", "code", PASS,
                    "At least one item is accepted and every accepted item has its checks, so the export can be built." + (" " + pending_warning(n_pend) if n_pend else "")
                    + (" " + edit_warning(n_edit, n_ai) if n_edit else ""),
                    rule="row 19", counts=gate_counts)
    else:
        first = blockers[0]
        text = (f"{len(jnr)} accepted item{'s have' if len(jnr) != 1 else ' has'} not been double-checked by the second AI check, so the export is blocked. Run the second check again."
                if jnr and first is jnr[0] else first["why"])
        gate = step("export_gate", "Ready to export?", "code", FAIL, text, reason=first["reason_code"], rule="row 19", counts=gate_counts, next_action=first["next_action"],
                    blocks=True)
    gate.update(ready=ready, blockers=blockers, warnings=warnings)
    st.append(gate)
    _number(st)
    verdict = ({"code": "running", "label": "The AI run is in progress"} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
               else {"code": "ready", "label": "Ready to export" + (f" ({n_pend + n_edit} not reviewed)" if n_pend + n_edit else "")} if ready
               else {"code": "needs_attention", "label": f"{len(ccf)} summar{'ies fail' if len(ccf) != 1 else 'y fails'} a check" if ccf and not jnr
                      else f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr else "Nothing is accepted yet"})
    return {"token": case_id, "mode": "full" if cx.full else "metadata", "status": case["status"], "verdict": verdict, "progress": _progress(st), "steps": st}


def pending_warning(n: int) -> str:
    return f"{n} item{'s are' if n != 1 else ' is'} not reviewed, so {'they' if n != 1 else 'it'} will not be in the letter; the AI disclosure line will count {'them' if n != 1 else 'it'}."


def edit_warning(n: int, n_ai: int = 0) -> str:
    return edit_warning_base(n) + (f" {n_ai} of {'them keep' if n != 1 else 'it keeps'} the AI's summary and the second check has no answer on the new quote, so accepting alone will not put "
                                    f"{'them' if n_ai != 1 else 'it'} in the letter; the export stays blocked until the check answers or you edit the summary yourself." if n_ai else "")
930:def case_trace(conn, case_id: str, full: bool = False) -> dict:
931-    cx = _Cx(conn, case_id, full)
932-    case = cx.case
933-    recs = list(cx.recs.values())
934-    ents = DB.list_items(conn, case_id, "entry")
935-    handled = generator.resolved_placeholders(ents)
936-    failed_ents = [x for x in ents if (x.get("ladder") or {}).get("failure") and x["id"] not in handled]       # tray placeholders for records the extract step made no output for (not drafted items: nothing to ground or judge)
937-    ents = [x for x in ents if not (x.get("ladder") or {}).get("failure")]      # (a hand-entered record's placeholder is dropped here too)
938-    amts = DB.list_items(conn, case_id, "amount")
939-    flgs = [x for x in DB.list_items(conn, case_id, "flag") if not FT.is_filtered(x.get("state_reasons"))]      # D-057: rule-filtered proposals are listed in the payload, not checked or counted here
940-    allitems = [("entry", x) for x in ents] + [("amount", x) for x in amts] + [("flag", x) for x in flgs]
941-    cfg = case.get("config") or {}
942-    rv = present.review_view(conn, case_id)
943-    jr = judge_report(conn, case_id, full)
944-    st = []
945-    # 1 ingest
946-    dup = sum(1 for r in recs if r["duplicate_of"])
947-    st.append(step("ingest", "Read the paste and split it into records", "code", PASS if recs else FAIL,
948-                   f"{len(recs)} records found." + (f" {dup} exact duplicate{'s' if dup != 1 else ''} merged into the record they repeat." if dup else ""), rule="row 1",
949-                   counts={"records": len(recs), "duplicates_merged": dup, "characters": len(case["raw_text"])}))
950-    # 2 split
951-    llm_split = any(f["category"] == "llm_split" for f in flgs)
952-    sf = cfg.get("split_failure")
953-    if sf:
954-        st.append(step("split", "Record boundaries", "code", FAIL, reason_text("SPLIT_AMBIGUOUS"), reason="SPLIT_AMBIGUOUS", rule="row 1", evidence={"values": {"failure": sf}},
955-                       counts={"method": "code", "llm_split": False}, next_action=na("READ_RECORD", {"view": "records"})))
134:class _Cx:
135-    def __init__(self, conn, case_id, full):
136-        self.conn, self.case_id, self.full = conn, case_id, bool(full)
137-        self.case = DB.get_case(conn, case_id)
138-        self.recs = present._recs_by_id(conn, case_id)
139-        self._live_recs = None
140-        calls = DB.list_llm_calls(conn, case_id)
141-        self.call_by_id = {c["id"]: c for c in calls}
142-        self.calls_by_item = {}
143-        for c in calls:
144-            self.calls_by_item.setdefault(c["item_id"], []).append(c)
145-        self.events = {}
146-        for e in DB.list_events(conn, case_id):
147-            self.events.setdefault(e["item_id"], []).append(e)
148-        self.models = {"generator": J.generator_model(), "judge": J.judge_model()}
149-        self.ran = self.case.get("run_started_at") is not None
150-        self.running = self.case["status"] == "running"
151-
152-    @property
153-    def live_recs(self):
154-        """store.load_records() dicts (they carry the record body, source and language the code checks need), loaded once per context."""
155-        if self._live_recs is None:
156-            self._live_recs = store.load_records(self.conn, self.case_id, self.case["raw_text"])
157-        return self._live_recs
158-
159-    def call(self, call_id, item_id=None, step_name=None):
160-        if call_id and call_id in self.call_by_id:
161-            return self.call_by_id[call_id]
162-        if item_id and step_name:
163-            hits = [c for c in self.calls_by_item.get(item_id, []) if c["step"] == step_name]
164-            return hits[-1] if hits else None
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:25:49.222Z

**tool call — Bash**
````
{
 "command": "ls evals/library | head -50; ls evals/library | wc -l; grep -n \"^STAGES\\|STAGES =\" -r app/backend/*.py | head; sed -n 80,140p app/backend/api.py; sed -n 280,300p tests/unit/test_api_routes.py; sed -n 1,60p tests/unit/test_api_routes.py; ls tests/unit | grep -i \"library\\|api\" "
}
````

### User / tool · 2026-11-02T13:25:49.378Z

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
case_lib06_lop_billed_vs_adjusted.expected.json
case_lib06_lop_billed_vs_adjusted.txt
case_lib07_parking_lot_fall_outside_records.expected.json
case_lib07_parking_lot_fall_outside_records.txt
case_lib08_second_crash_mri_after.expected.json
case_lib08_second_crash_mri_after.txt
case_lib09_spanish_interpreter_espalda.expected.json
case_lib09_spanish_interpreter_espalda.txt
case_lib10_eob_ub04_cms1500.expected.json
case_lib10_eob_ub04_cms1500.txt
case_lib11_priors_and_ledger.expected.json
case_lib11_priors_and_ledger.txt
case_lib12_records_review_credibility.expected.json
case_lib12_records_review_credibility.txt
case_lib13_cloned_notes_cross_provider.expected.json
case_lib13_cloned_notes_cross_provider.txt
case_lib14_handwritten_chiro_scans.expected.json
case_lib14_handwritten_chiro_scans.txt
case_lib15_conclusory_letter_mist.expected.json
case_lib15_conclusory_letter_mist.txt
      30
app/backend/api.py:36:STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]
app/backend/pipeline.py:19:STAGES = ("ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize")
    return os.environ.get("ZLAYT_MODE") == "local"


def is_loopback_peer(request) -> bool:
    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
    host = request.client.host if request.client else None
    try:
        ip = ipaddress.ip_address(host)
    except (TypeError, ValueError):
        return False
    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback


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
    DB.connect(db_path).close()
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
        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

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
    monkeypatch.setenv("ZLAYT_MODE", "local")
    full = c.get(f"/api/cases/{tok}/audit").json()
    assert full["calls"][0]["user_text"] and full["calls"][0]["system_text"] and "before" in full["events"][0]


def test_case_list_and_library_exist_only_in_local_mode(env, monkeypatch):
    """T-053 AC1: public/demo stays token-only (404); local mode lists cases and the library and loads a library case in one call."""
    _, c = env
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.get("/api/cases").status_code == 404 and c.get("/api/library").status_code == 404
    assert c.post("/api/cases", json={"library": "case_01_date_formats"}).status_code == 404
    monkeypatch.setenv("ZLAYT_MODE", "local")
    lib = c.get("/api/library").json()["cases"]
    assert lib and "path" not in lib[0] and {"id", "name", "description"} <= set(lib[0])
    r = c.post("/api/cases", json={"library": lib[0]["id"]})
    assert r.status_code == 201 and r.json()["token"] != tok
    listed = c.get("/api/cases").json()["cases"]
    assert [x["token"] for x in listed][:2] == [r.json()["token"], tok] and {"name", "status", "record_count", "counts", "created_at"} <= set(listed[0])
    assert "text" not in listed[0] and c.post("/api/cases", json={"library": "nope"}).status_code == 404

"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
import ast
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "api.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)


def wait_ready(c, tok):
    for _ in range(160):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready", s
    return s


def run_case(c, text=None):
    tok = c.post("/api/cases", json={"text": text} if text else {"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    wait_ready(c, tok)
    return tok


def test_health_shape(env):
    h = env[1].get("/api/health").json()
    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
    assert {"banner", "ai_banner", "models", "retention_hours", "sample_available", "synthetic_only"} <= set(h)


def test_create_sample_is_code_only_with_gap_flag(env):
    _, c = env
    r = c.post("/api/cases", json={"sample": True})
    b = r.json()
    assert r.status_code == 201 and b["record_count"] == 9 and len(b["gap_flags"]) == 1 and b["status"] == "ingested"
    assert b["records"][0]["text"].startswith("=== Record 1") and b["split_method"] == "code" and r.headers["referrer-policy"] == "no-referrer"
    assert c.get(f"/api/cases/{b['token']}/audit").json()["summary"]["calls"] == 0          # no model call at ingest


def test_error_format_and_unknown_token(env):
    _, c = env
    r = c.get("/api/cases/nope")
    e = r.json()["error"]
    assert r.status_code == 404 and e["code"] == "not_found" and set(e) == {"code", "message", "detail"}
test_api.py
test_api_routes.py
test_library_denylist.py
test_pdf_checks_api.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:26:11.339Z

**tool call — Bash**
````
{
 "command": "grep -n \"review_events\\|CREATE TABLE\" app/db/schema.sql | head -20; grep -n \"def list_events\" -A8 app/db/db.py; grep -n \"def get_case\" -A10 app/db/db.py; grep -n \"^def \\|^import\\|^from\" app/backend/present.py | head -50; grep -rn \"library\" tests/unit/*.py -l | head"
}
````

### User / tool · 2026-11-02T13:26:11.478Z

**tool result**
````
4:CREATE TABLE IF NOT EXISTS cases (
11:CREATE TABLE IF NOT EXISTS records (
19:CREATE TABLE IF NOT EXISTS entries (
27:CREATE TABLE IF NOT EXISTS amounts (
36:CREATE TABLE IF NOT EXISTS flags (
48:CREATE TABLE IF NOT EXISTS llm_calls (
55:CREATE TABLE IF NOT EXISTS review_events (
65:CREATE INDEX IF NOT EXISTS ix_events_case ON review_events(case_id);
257:def list_events(conn, case_id: str, item_id: str = None) -> list:
258-    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
259-    if item_id:
260-        q, a = q + " AND item_id=?", a + [item_id]
261-    return [_decode(r) for r in conn.execute(q + " ORDER BY at, rowid", a)]
262-
263-
264-def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
265-    """One row per attempt. `prompt` is the user text; prompt_sha256 covers system+user unless supplied."""
131:def get_case(conn, case_id: str):
132-    r = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
133-    return _decode(r) if r else None
134-
135-
136-def _insert(conn, table, row):
137-    bad = set(row) - _cols(conn, table)
138-    if bad:
139-        raise ValueError(f"unknown {table} fields {sorted(bad)}")
140-    conn.execute(f"INSERT INTO {table} ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
141-                 [_enc(v) for v in row.values()])
2:import json
3:import re
5:from app.backend import conflict_candidates, confidence, date_convention, flag_templates as FT, generator, grounding, ingest, language, overlap, pdf_text, review, sentences, spanish, store, totals as T, uncovered, why
6:from app.db import db as DB
12:def _why(reasons):
22:def _human(row):
28:def _ladder(row):
36:def _common(row):
41:def entry_view(row, recs):
52:def _translation(row):
58:def accept_effect(row) -> str:
64:def amount_view(row, recs):
70:def _computed(c):
81:def _evidence(evs, recs):
87:def _gap_why(row, base):
99:def flag_view(row, recs):
107:def gap_change_index(events, current: dict):
132:def _with_gap_changes(conn, case_id, flags):
146:def _recs_by_id(conn, case_id):
157:def item_view(conn, case_id, item_id):
167:def all_items(conn, case_id):
174:def totals_view(conn, case_id):
188:def rejected_count(conn, case_id):
194:def review_view(conn, case_id):
209:def dates_to_confirm(conn, case_id):
217:def record_view(r, raw, with_sentences=True, pages=None):
242:def quote_body(block):
263:def quote_units(body, rec):
279:def case_view(conn, case_id, *, backend, models, demo_mode):
325:def why_view(conn, case_id, item_id):
341:def _call(c, full=False):
352:def audit_view(conn, case_id, full=False):
366:def case_list(conn):
tests/unit/_pdf.py
tests/unit/test_amounts_t140.py
tests/unit/test_api_routes.py
tests/unit/test_conflict_candidates.py
tests/unit/test_library_denylist.py
tests/unit/test_ingest.py
tests/unit/test_language_routing_heldout.py
tests/unit/test_lib09_t110.py
tests/unit/test_t116_gap_endpoints.py
tests/unit/test_quote_units.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:26:15.908Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/unit/test_lib09_t110.py; sed -n 165,193p app/backend/present.py; git status --short tests | head"
}
````

### User / tool · 2026-11-02T13:26:16.040Z

**tool result**
````
"""T-110 on the lib09 Spanish packet (fixture backend, no network): where the 4/7 comes from, a record with no AI output never vanishes
(could-not-verify tray with its reason), and POSSIBLE_OVERLAP warns next to the charge total instead of guessing (D-019)."""
import json
import pathlib
import tempfile

import pytest

from app.backend import ingest as IN, overlap as OV, pipeline as PL, present, review as RV, totals as T, trace
from app.db import db as DB
from app.llm import provider as P
from evals import run as R
from tests.unit._fakes import FakeCall

LIB = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"
NAME = "case_lib09_spanish_interpreter_espalda"
TEXT = (LIB / f"{NAME}.txt").read_text()
EXPECTED = json.loads((LIB / f"{NAME}.expected.json").read_text())


@pytest.fixture(scope="module")
def lib09():
    return PL.run_case(TEXT, "fixture")


def _stored(wrap=None):
    """Run the fixture backend into a kept database; `wrap(call)` may replace the model call (to force a miss on one record)."""
    tmp = tempfile.TemporaryDirectory()
    with PL._Backend("fixture"):
        conn, cid, call = PL._scratch_call(tmp.name, IN.normalize_text(TEXT))
        PL.run_pipeline(conn, cid, TEXT, call=wrap(call) if wrap else call)
    return tmp, conn, cid


def _miss_on(*item_ids):
    def wrap(call):
        def c(step, system, user, schema, *, item_id=None):
            if item_id in item_ids:
                raise P.FixtureMiss("forced")
            return call(step, system, user, schema, item_id=item_id)
        return c
    return wrap


# ---------------------------------------------------------------- AC1: the 4/7
def test_every_lib09_record_has_an_entry_nothing_vanishes(lib09):
    """The '4/7' is the eval matcher, not a load failure: all seven records are entries (six dated, one date-to-confirm), no errors, nothing in the tray."""
    got = {n for e in lib09["entries"] + lib09["undated_entries"] for r in e["record_ids"] for n in [int(r[1:])]}
    assert got == set(range(1, 8)) and lib09["errors"] == [] and lib09["tray"] == [] and lib09["status"] == "done"
    assert len(lib09["entries"]) == 6 and [e["record_ids"] for e in lib09["undated_entries"]] == [["r4"]]


def test_spanish_records_are_held_for_review_not_verified(lib09):
    """D-050: records 2, 4 and 7 are Spanish, so their entries are needs_review with AI_TRANSLATION; the English ones are verified. The hold is not why the matcher misses."""
    by = {e["record_ids"][0]: e for e in lib09["entries"] + lib09["undated_entries"]}
    for r in ("r2", "r4", "r7"):
        assert by[r]["state"] == "needs_review" and "AI_TRANSLATION" in by[r]["reasons"]
    for r in ("r1", "r3", "r5", "r6"):
        assert by[r]["state"] == "verified" or by[r]["reasons"] == ["CHARGE_TEXT_IN_ENTRY"]      # T-139: an entry that states an amount is held for review, for that reason alone
        assert "AI_TRANSLATION" not in by[r]["reasons"]


def all_items(conn, case_id):
    recs = _recs_by_id(conn, case_id)
    out = {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
    out["gap_changes_removed"] = _with_gap_changes(conn, case_id, out["flag"])[1]
    return out


def totals_view(conn, case_id):
    am = [a for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
    t = T.totals([{"id": a["id"], "cents": a["value_cents"], "cls": a["kind"], "raw": a["text"], "review_status": a["review_status"]} for a in am])
    ch = [a for a in am if a["kind"] == "charge" and a["value_cents"] is not None]
    cnt = lambda sts: sum(1 for a in ch if a["review_status"] in sts)   # noqa: E731
    return {"accepted": {"cents": t["accepted_cents"], "count": cnt(("accepted", "edited")), "label": "Accepted charges"},
            "pending": {"cents": t["detected_pending_cents"], "count": cnt(("pending",)), "label": "Pending review"},
            "detected_not_a_total": {"cents": sum(a["value_cents"] for a in ch if a["review_status"] != "dismissed"),
                                     "count": sum(1 for a in ch if a["review_status"] != "dismissed"), "label": "Detected (not a total)"},
            "not_totaled": [{"id": a["id"], "kind": a["kind"], "text": a["text"]} for a in am
                            if a["kind"] != "charge" and a["review_status"] != "dismissed" and a["kind"] != "damages"],
            "possible_overlaps": overlap.view(conn, case_id)}      # T-110: a statement line that may include a separately stated charge; warns, never changes the total


def rejected_count(conn, case_id):
    """Entries and amounts in the could-not-verify tray (state rejected), without a placeholder the paralegal has since answered with a hand-entered entry (T-110 r2)."""
    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))
    return sum(1 for k in ("entry", "amount") for r in DB.list_items(conn, case_id, k) if r["state"] == "rejected" and r["id"] not in handled)


 M tests/e2e/conftest.py
 M tests/e2e/test_edit_to_check.py
 M tests/unit/test_api_routes.py
 M tests/unit/test_lib09_t110.py
 M tests/unit/test_narrative.py
 M tests/unit/test_t132_attribution_unit.py
 M tests/unit/test_trace.py
?? tests/e2e/test_conflict_coverage.py
?? tests/fixtures/llm/0cc7a873e16a2f0572848c8c047cc0aeb4d32e2b42dfc81274ea28ca63fa3b84.json
?? tests/fixtures/llm/11a811729af462550cae9432916cf92b314ef5912bdbf4fa459763a20caf03b7.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:26:25.775Z

**tool call — Write**
````
{
 "path": "/Users/arsis/zlayt-pm-project/app/backend/case_list.py",
 "content": "\"\"\"GET /api/cases (T-148): one summary per case for the local profile's overview screen. Local mode only (D-008/D-031); the route is a 404 otherwise.\n\nCode only: no model call, no pipeline run, no record text. Every number comes from the functions GET case, GET status and the export gate already use, so the\nlist cannot say something the case screen does not:\n  run             stage / progress   -> run_progress() (the /status route calls it too)\n  progress        decided / total    -> the item filter present.review_view applies (live = not rejected, no tray placeholder, no rule-filtered proposal)\n  hitl.needs_review / edits_to_check / could_not_verify -> present.review_view counts (the tray length GET case returns is the `rejected` count)\n  hitl.gate, export_ready -> the export_gate step of trace.case_trace (blockers and warnings with their plain `why`, the list GET /export refuses on)\ntests/unit/test_case_list.py compares each field with GET case, GET status, GET trace and GET export for every library case.\n\"\"\"\nimport re\n\nfrom app.backend import filters_shim as _unused  # noqa: F401  (placeholder removed below)\n"
}
````

### User / tool · 2026-11-02T13:26:25.836Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/app/backend/case_list.py (file state is current in your context — no need to Read it back)

Note: Write's parameters are named `file_path` and `content`. `path` was read as `file_path`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:26:40.210Z

**tool call — Write**
````
{
 "path": "/Users/arsis/zlayt-pm-project/app/backend/case_list.py",
 "content": "\"\"\"GET /api/cases (T-148): one summary per case for the local profile's overview screen. Local mode only (D-008/D-031); the route is a 404 otherwise.\n\nCode only: no model call, no pipeline run, no record text. Every number comes from the functions GET case, GET status and the export gate already use, so the\nlist cannot say something the case screen does not:\n  run                                        -> run_progress() (the /status route calls it too)\n  progress decided / total per kind          -> the item filter present.review_view applies (live = not rejected, no tray placeholder, no rule-filtered proposal)\n  hitl.needs_review, edits_to_check, tray    -> present.review_view counts (the tray length GET case returns is the `rejected` count)\n  hitl.gate, export_ready                    -> the export_gate step of trace.case_trace (blockers and warnings with their plain `why`; the list GET /export refuses on)\ntests/unit/test_case_list.py compares each field with GET case, /status, /trace and /export for every library case.\n\"\"\"\nimport datetime\nimport re\n\nfrom app.backend import flag_templates as FT, generator, present, review, store, trace\nfrom app.db import db as DB\n\nKINDS = ((\"entries\", \"entry\"), (\"flags\", \"flag\"), (\"amounts\", \"amount\"))\n_SLUG = re.compile(r\"^[\\w.\\-]+$\")\n_EXT = re.compile(r\"\\.(pdf|txt|docx?|rtf)$\", re.IGNORECASE)\n\n\ndef readable_title(name, source, created_at) -> str:\n    \"\"\"A name a paralegal would recognise. A file name or slug (\"smith_records-2024.pdf\") becomes words; no name at all becomes \"Untitled case\" with its date.\"\"\"\n    n = (name or \"\").strip()\n    if n and _SLUG.match(n) and not n.isalpha():          # one token with _ - . in it: a file name or slug, not a typed name\n        n = re.sub(r\"\\s+\", \" \", re.sub(r\"[_\\-]+\", \" \", _EXT.sub(\"\", n))).strip()\n        n = n[:1].upper() + n[1:]\n    if n:\n        return n\n    day = datetime.datetime.fromtimestamp(float(created_at or 0), datetime.timezone.utc).strftime(\"%b %-d\")\n    return (\"Sample case\" if source == \"sample\" else \"Untitled case\") + (f\", {day}\" if source != \"sample\" else \"\")\n\n\ndef run_progress(case: dict, stages) -> tuple:\n    \"\"\"(stage, steps_done) for a case row: what GET /status reports. A case that was only ingested is at the 'ingest' stage.\"\"\"\n    stage = case[\"stage\"] or (\"ingest\" if case[\"status\"] == \"ingested\" else None)\n    return stage, (list(stages).index(stage) if stage in stages else 0)\n\n\ndef _progress(conn, case_id) -> dict:\n    \"\"\"decided / total per kind over the items review_view counts. An edit still marked Needs review (T-134) is not decided.\"\"\"\n    items = {k: DB.list_items(conn, case_id, k) for _, k in KINDS}\n    handled = generator.resolved_placeholders(items[\"entry\"])\n    out = {}\n    for label, kind in KINDS:\n        live = [r for r in items[kind] if r[\"id\"] not in handled and not FT.is_filtered(r.get(\"state_reasons\")) and r[\"state\"] != \"rejected\"]\n        decided = sum(1 for r in live if r[\"review_status\"] in (\"accepted\", \"dismissed\", \"edited\") and not review.edit_unconfirmed(kind, r))\n        out[label] = {\"decided\": decided, \"total\": len(live)}\n    return out\n\n\ndef _gate(conn, case_id) -> dict:\n    step = next(s for s in trace.case_trace(conn, case_id, full=False)[\"steps\"] if s[\"id\"] == \"export_gate\")\n    keep = lambda xs, keys: [{k: x[k] for k in keys if k in x} for x in xs]      # noqa: E731\n    return {\"ready\": step[\"ready\"], \"blockers\": keep(step[\"blockers\"], (\"reason_code\", \"kind\", \"item_id\", \"why\")),\n            \"warnings\": keep(step[\"warnings\"], (\"reason_code\", \"count\", \"why\"))}\n\n\ndef summary(conn, case_id: str, stages) -> dict:\n    case = DB.get_case(conn, case_id)\n    rv = present.review_view(conn, case_id)\n    counts = rv[\"counts\"]\n    stage, done = run_progress(case, stages)\n    gate = _gate(conn, case_id)\n    last = conn.execute(\"SELECT max(at) FROM review_events WHERE case_id=?\", (case_id,)).fetchone()[0]\n    updated = case.get(\"run_finished_at\") or case[\"created_at\"]            # the same value GET case calls updated_at\n    return {\"token\": case_id, \"title\": readable_title(case[\"name\"], case[\"source\"], case[\"created_at\"]), \"name\": case[\"name\"],\n            \"source\": case[\"source\"], \"status\": case[\"status\"],\n            \"record_count\": conn.execute(\"SELECT count(*) FROM records WHERE case_id=?\", (case_id,)).fetchone()[0],\n            \"created_at\": store.iso(case[\"created_at\"]), \"updated_at\": store.iso(updated), \"last_activity_at\": store.iso(max(updated, last or 0)),\n            \"run\": {\"stage\": stage, \"steps_done\": done, \"steps_total\": len(stages), \"running\": case[\"status\"] == \"running\",\n                    \"error\": bool(case.get(\"error\"))},\n            \"progress\": _progress(conn, case_id),\n            \"counts\": {k: counts[k] for k in (\"pending\", \"accepted\", \"edited\", \"dismissed\", \"needs_review\")},      # kept from the first version of this route\n            \"hitl\": {\"pending\": counts[\"pending\"], \"needs_review\": counts[\"needs_review\"], \"edits_to_check\": counts[\"edit_to_check\"],\n                     \"could_not_verify\": counts[\"rejected\"], \"gate_blockers\": gate[\"blockers\"], \"gate_warnings\": gate[\"warnings\"]},\n            \"export_ready\": gate[\"ready\"]}\n\n\ndef summaries(conn, stages) -> list:\n    \"\"\"Every case, newest first (created, then insertion order).\"\"\"\n    return [summary(conn, r[\"id\"], stages) for r in conn.execute(\"SELECT id FROM cases ORDER BY created_at DESC, rowid DESC\")]\n"
}
````

### User / tool · 2026-11-02T13:26:40.288Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/backend/case_list.py has been updated successfully. (file state is current in your context — no need to Read it back)

Note: Write's parameters are named `file_path` and `content`. `path` was read as `file_path`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:26:41.870Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='app/backend/api.py'\ns=open(p).read()\ns=s.replace('return {\"cases\": present.case_list(c)}','return {\"cases\": case_list.summaries(c, STAGES)}')\ns=s.replace('''            stages = getattr(pipeline_mod(), \"STAGES\", None) or STAGES\n            stages = list(stages) if not callable(stages) else STAGES\n            done = stages.index(stage) if stage in stages else 0\n''','''            stages = getattr(pipeline_mod(), \"STAGES\", None) or STAGES\n            stages = list(stages) if not callable(stages) else STAGES\n            stage, done = case_list.run_progress(case, stages)\n''')\nopen(p,'w').write(s)\nEOF\nsed -n 1,35p app/backend/api.py | grep -n \"import\"; sed -n 394,402p app/backend/api.py"
}
````

### User / tool · 2026-11-02T13:26:42.001Z

**tool result**
````
6:import hashlib
7:import ipaddress
8:import asyncio
9:import json
10:import logging
11:import os
12:import pathlib
13:import threading
14:import time
16:from fastapi import FastAPI, Request
17:from fastapi.exceptions import RequestValidationError
18:from fastapi.responses import JSONResponse, Response
19:from starlette.exceptions import HTTPException as StarletteHTTPException
21:from starlette.concurrency import run_in_threadpool
23:from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
24:from app.db import db as DB
    @app.get("/api/cases/{token}/status")
    def status(token: str):
        c = conn()
        try:
            case = get_case(c, token)
            stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
            stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
            stages = list(stages) if not callable(stages) else STAGES
            stage, done = case_list.run_progress(case, stages)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:26:47.014Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/api.py'\ns=open(p).read()\ns=s.replace('''            stage = case[\"stage\"] or (\"ingest\" if case[\"status\"] == \"ingested\" else None)\n            stages = getattr(pipeline_mod(), \"STAGES\", None) or STAGES\n            stages = list(stages) if not callable(stages) else STAGES\n            stage, done''','''            stages = getattr(pipeline_mod(), \"STAGES\", None) or STAGES\n            stages = list(stages) if not callable(stages) else STAGES\n            stage, done''')\ns=s.replace('case_list.summaries(c, STAGES)','case_list.summaries(c, list(getattr(pipeline_mod(), \"STAGES\", None) or STAGES))')\ns=s.replace('from app.backend import case_extras, dismissal','from app.backend import case_extras, case_list, dismissal')\nopen(p,'w').write(s)\nEOF\ngit diff -- app/backend/api.py"
}
````

### User / tool · 2026-11-02T13:26:47.138Z

**tool result**
````
diff --git a/app/backend/api.py b/app/backend/api.py
index dfe1f24..c48b2a6 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -20,7 +20,7 @@ from starlette.exceptions import HTTPException as StarletteHTTPException
 
 from starlette.concurrency import run_in_threadpool
 
-from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
+from app.backend import case_extras, case_list, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
 from app.db import db as DB
 
 MAX_BODY_BYTES = 512 * 1024      # cheap rejection before the 60,000-character rule: UTF-8 worst case plus JSON overhead
@@ -221,7 +221,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             raise ApiError(404, "not_found", "Not found.")
         c = conn()
         try:
-            return {"cases": present.case_list(c)}
+            return {"cases": case_list.summaries(c, list(getattr(pipeline_mod(), "STAGES", None) or STAGES))}
         finally:
             c.close()
 
@@ -396,10 +396,9 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         c = conn()
         try:
             case = get_case(c, token)
-            stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
             stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
             stages = list(stages) if not callable(stages) else STAGES
-            done = stages.index(stage) if stage in stages else 0
+            stage, done = case_list.run_progress(case, stages)
             end = case["run_finished_at"] or time.time()
             return {"token": token, "status": case["status"], "stage": stage, "stages": stages,
                     "progress": {"done": done, "total": len(stages), "label": f"Step {done + 1} of {len(stages)}: {stage}" if stage else ""},
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:27:09.012Z

**tool call — Write**
````
{
 "path": "/Users/arsis/zlayt-pm-project/tests/unit/test_case_list.py",
 "content": "\"\"\"T-148: GET /api/cases summary list. Every field is compared with the route that owns it (GET case, /status, /trace, /export) for every library\ncase, so the overview can never say something the case screen does not. Fixture backend, no network; local mode only.\"\"\"\nimport pathlib\nimport time\n\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import case_list\nfrom app.backend.api import create_app\n\nLIB = pathlib.Path(__file__).resolve().parents[2] / \"evals\" / \"library\"\nLIB_IDS = sorted(p.stem for p in LIB.glob(\"*.txt\"))\n\n\n@pytest.fixture(scope=\"module\")\ndef local(tmp_path_factory):\n    import os\n    old = {k: os.environ.get(k) for k in (\"LLM_BACKEND\", \"ZLAYT_MODE\", \"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\")}\n    os.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\n    for k in (\"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\"):\n        os.environ.pop(k, None)\n    d = tmp_path_factory.mktemp(\"cl\")\n    c = TestClient(create_app(str(d / \"t.sqlite\"), static_dir=str(d)), client=(\"127.0.0.1\", 50000))\n    yield c\n    for k, v in old.items():\n        os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)\n\n\ndef _wait(c, tok):\n    for _ in range(240):\n        s = c.get(f\"/api/cases/{tok}/status\").json()\n        if s[\"status\"] in (\"ready\", \"failed\"):\n            return s\n        time.sleep(0.25)\n    raise AssertionError(s)\n\n\n@pytest.fixture(scope=\"module\")\ndef cases(local):\n    \"\"\"Every library case run to the end, plus one left at ingest, plus decisions made on the first run case (accept, edit, dismiss).\"\"\"\n    toks = {}\n    for lid in LIB_IDS:\n        r = local.post(\"/api/cases\", json={\"library\": lid})\n        assert r.status_code == 201, r.text\n        toks[lid] = r.json()[\"token\"]\n        assert local.post(f\"/api/cases/{toks[lid]}/run\", json={}).status_code == 202\n    for t in toks.values():\n        _wait(local, t)\n    first = toks[LIB_IDS[0]]\n    items = [i for k in (\"entries\", \"flags\", \"amounts\") for i in local.get(f\"/api/cases/{first}\").json()[k]]\n    for n, it in enumerate(items[:6]):\n        local.post(f\"/api/cases/{first}/items/{it['id']}/review\", json={\"action\": [\"accept\", \"dismiss\"][n % 2]})\n    toks[\"_ingested\"] = local.post(\"/api/cases\", json={\"text\": \"=== Record 1 ===\\nDate: 03/04/2024\\nSource: ER\\nExcerpt: Patient seen for neck pain.\\n\\n=== Record 2 ===\\nDate: 03/09/2024\\nSource: PT\\nExcerpt: Follow-up visit.\\n\", \"name\": \"smith_records-2024.txt\"}).json()[\"token\"]\n    return toks\n\n\ndef _by_token(local):\n    r = local.get(\"/api/cases\")\n    assert r.status_code == 200\n    return {x[\"token\"]: x for x in r.json()[\"cases\"]}\n\n\ndef test_list_covers_every_case_newest_first(local, cases):\n    got = local.get(\"/api/cases\").json()[\"cases\"]\n    assert {x[\"token\"] for x in got} == set(cases.values()) and len(got) == len(LIB_IDS) + 1\n    assert got[0][\"token\"] == cases[\"_ingested\"] and [x[\"created_at\"] for x in got] == sorted((x[\"created_at\"] for x in got), reverse=True)\n\n\ndef test_every_summary_field_matches_the_case_status_gate_and_export(local, cases):\n    listed = _by_token(local)\n    for lid, tok in cases.items():\n        s, case = listed[tok], local.get(f\"/api/cases/{tok}\").json()\n        st = local.get(f\"/api/cases/{tok}/status\").json()\n        tr = local.get(f\"/api/cases/{tok}/trace\").json()\n        gate = next(x for x in tr[\"steps\"] if x[\"id\"] == \"export_gate\")\n        # identity and times: the case screen's own values\n        assert s[\"name\"] == case[\"name\"] and s[\"status\"] == case[\"status\"] and s[\"created_at\"] == case[\"created_at\"] and s[\"updated_at\"] == case[\"updated_at\"], lid\n        assert s[\"record_count\"] == len(case[\"records\"]) and s[\"last_activity_at\"] >= s[\"updated_at\"], lid\n        # run stage: the status route\n        assert s[\"run\"][\"stage\"] == st[\"stage\"] and s[\"run\"][\"steps_done\"] == st[\"progress\"][\"done\"] and s[\"run\"][\"steps_total\"] == st[\"progress\"][\"total\"], lid\n        assert s[\"run\"][\"running\"] == (case[\"status\"] == \"running\"), lid\n        # review counts and the could-not-verify tray: the case screen\n        rc = case[\"review\"][\"counts\"]\n        h = s[\"hitl\"]\n        assert h[\"needs_review\"] == rc[\"needs_review\"] and h[\"edits_to_check\"] == rc[\"edit_to_check\"] and h[\"pending\"] == rc[\"pending\"], lid\n        assert h[\"could_not_verify\"] == len(case[\"tray\"]), lid\n        assert s[\"counts\"] == {k: rc[k] for k in (\"pending\", \"accepted\", \"edited\", \"dismissed\", \"needs_review\")}, lid\n        # progress per kind: totals are the live items GET case lists, decided never exceeds total, and the kinds add up to the review counts\n        live = {\"entries\": [e for e in case[\"entries\"] + case[\"undated_entries\"]], \"flags\": case[\"flags\"], \"amounts\": case[\"amounts\"]}\n        for kind, rows in live.items():\n            p = s[\"progress\"][kind]\n            assert p[\"total\"] == len(rows), (lid, kind)\n            assert p[\"decided\"] == sum(1 for r in rows if r[\"review_status\"] in (\"accepted\", \"dismissed\", \"edited\")) - (rc[\"edit_to_check\"] if kind == \"entries\" else 0), (lid, kind)\n        tot = sum(v[\"total\"] for v in s[\"progress\"].values())\n        dec = sum(v[\"decided\"] for v in s[\"progress\"].values())\n        assert tot - dec == rc[\"pending\"] + rc[\"edit_to_check\"], lid\n        # gate: blockers and warnings with their plain reasons, and export_ready is what GET /export allows\n        assert s[\"export_ready\"] is gate[\"ready\"] is (local.get(f\"/api/cases/{tok}/export\").status_code == 200), lid\n        assert [(b[\"reason_code\"], b[\"why\"]) for b in h[\"gate_blockers\"]] == [(b[\"reason_code\"], b[\"why\"]) for b in gate[\"blockers\"]], lid\n        assert [(w[\"reason_code\"], w[\"count\"], w[\"why\"]) for w in h[\"gate_warnings\"]] == [(w[\"reason_code\"], w[\"count\"], w[\"why\"]) for w in gate[\"warnings\"]], lid\n        assert all(b[\"why\"] for b in h[\"gate_blockers\"]) and all(w[\"why\"] for w in h[\"gate_warnings\"]), lid\n\n\ndef test_decisions_move_the_progress_and_the_ingested_case_is_not_ready(local, cases):\n    s = _by_token(local)\n    first = s[cases[LIB_IDS[0]]]\n    assert sum(v[\"decided\"] for v in first[\"progress\"].values()) >= 1 and first[\"last_activity_at\"] > first[\"updated_at\"] or first[\"last_activity_at\"] >= first[\"updated_at\"]\n    ing = s[cases[\"_ingested\"]]\n    assert ing[\"status\"] == \"ingested\" and ing[\"run\"][\"stage\"] == \"ingest\" and ing[\"export_ready\"] is False\n    assert [b[\"reason_code\"] for b in ing[\"hitl\"][\"gate_blockers\"]] == [\"NOTHING_ACCEPTED\"]\n\n\ndef test_title_is_readable_not_a_file_slug(local, cases):\n    s = _by_token(local)\n    assert s[cases[\"_ingested\"]][\"title\"] == \"Smith records 2024\"\n    for lid in LIB_IDS:\n        t = s[cases[lid]][\"title\"]\n        assert t and \"_\" not in t and not t.endswith((\".txt\", \".pdf\")), t\n    assert case_list.readable_title(\"records_final-v2.pdf\", \"paste\", 0) == \"Records final v2\"\n    assert case_list.readable_title(\"Smith v. Jones intake\", \"paste\", 0) == \"Smith v. Jones intake\"\n    assert case_list.readable_title(None, \"paste\", 1762000000) == \"Untitled case, Nov 1\"\n    assert case_list.readable_title(\"\", \"sample\", 0) == \"Sample case\"\n\n\ndef test_list_is_code_only_no_text_no_model_calls(local, cases):\n    import json\n    listed = local.get(\"/api/cases\").json()[\"cases\"]\n    raw = json.dumps(listed)\n    assert \"Excerpt:\" not in raw and \"raw_text\" not in raw\n    before = {t: local.get(f\"/api/cases/{t}/audit\").json()[\"summary\"][\"calls\"] for t in list(cases.values())[:3]}\n    local.get(\"/api/cases\")\n    assert before == {t: local.get(f\"/api/cases/{t}/audit\").json()[\"summary\"][\"calls\"] for t in before}\n\n\ndef test_list_is_404_outside_local_mode(local, monkeypatch):\n    monkeypatch.delenv(\"ZLAYT_MODE\")\n    assert local.get(\"/api/cases\").status_code == 404\n"
}
````

### User / tool · 2026-11-02T13:27:09.068Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/unit/test_case_list.py (file state is current in your context — no need to Read it back)

Note: Write's parameters are named `file_path` and `content`. `path` was read as `file_path`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:27:09.623Z

**tool call — Bash**
````
{
 "command": "time .venv/bin/python -m pytest tests/unit/test_case_list.py -x -q 2>&1 | tail -30",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T13:27:12.509Z

**tool result**
````
__________ ERROR at setup of test_list_covers_every_case_newest_first __________

local = <starlette.testclient.TestClient object at 0x108bd98b0>

    @pytest.fixture(scope="module")
    def cases(local):
        """Every library case run to the end, plus one left at ingest, plus decisions made on the first run case (accept, edit, dismiss)."""
        toks = {}
        for lid in LIB_IDS:
            r = local.post("/api/cases", json={"library": lid})
            assert r.status_code == 201, r.text
            toks[lid] = r.json()["token"]
            assert local.post(f"/api/cases/{toks[lid]}/run", json={}).status_code == 202
        for t in toks.values():
            _wait(local, t)
        first = toks[LIB_IDS[0]]
        items = [i for k in ("entries", "flags", "amounts") for i in local.get(f"/api/cases/{first}").json()[k]]
        for n, it in enumerate(items[:6]):
            local.post(f"/api/cases/{first}/items/{it['id']}/review", json={"action": ["accept", "dismiss"][n % 2]})
>       toks["_ingested"] = local.post("/api/cases", json={"text": "=== Record 1 ===\nDate: 03/04/2024\nSource: ER\nExcerpt: Patient seen for neck pain.\n\n=== Record 2 ===\nDate: 03/09/2024\nSource: PT\nExcerpt: Follow-up visit.\n", "name": "smith_records-2024.txt"}).json()["token"]
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_case_list.py:54: KeyError
------------------------------ Captured log setup ------------------------------
WARNING  zlayt.llm:audited.py:110 llm call failed call_id=cb2c8213ab358 step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
=========================== short test summary info ============================
ERROR tests/unit/test_case_list.py::test_list_covers_every_case_newest_first
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 error in 2.56s

real	0m2.803s
user	0m1.573s
sys	0m0.649s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:27:16.514Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_case_list.py'\ns=open(p).read()\na=s.index('    toks[\"_ingested\"]')\nb=s.index('    return toks')\ns=s[:a]+'''    text = (LIB / f\"{LIB_IDS[-1]}.txt\").read_text()               # an allowed (recorded) text, pasted under a file-slug name and never run\n    toks[\"_ingested\"] = local.post(\"/api/cases\", json={\"text\": text, \"name\": \"smith_records-2024.txt\"}).json()[\"token\"]\n'''+s[b:]\nopen(p,'w').write(s)\nEOF\ntime .venv/bin/python -m pytest tests/unit/test_case_list.py -x -q 2>&1 | tail -30",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T13:27:19.629Z

**tool result**
````
......                                                                   [100%]
6 passed in 2.79s

real	0m3.015s
user	0m2.180s
sys	0m0.674s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:27:26.247Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/dbg_cl.py <<'EOF'\nimport json, os, sys, time\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom tests.unit.test_case_list import LIB_IDS, _wait\nimport tempfile\nd = tempfile.mkdtemp()\nc = TestClient(create_app(d + \"/t.sqlite\", static_dir=d), client=(\"127.0.0.1\", 50000))\nfor l in LIB_IDS:\n    t = c.post(\"/api/cases\", json={\"library\": l}).json()[\"token\"]; c.post(f\"/api/cases/{t}/run\", json={})\nt0 = time.time()\nfor x in c.get(\"/api/cases\").json()[\"cases\"]:\n    _wait(c, x[\"token\"])\nt1 = time.time(); r = c.get(\"/api/cases\").json()[\"cases\"]; print(\"list secs\", time.time() - t1)\nfor x in r:\n    print(x[\"title\"][:30], x[\"status\"], x[\"run\"][\"stage\"], {k: tuple(v.values()) for k, v in x[\"progress\"].items()}, x[\"hitl\"][\"needs_review\"], x[\"hitl\"][\"could_not_verify\"], [b[\"reason_code\"] for b in x[\"hitl\"][\"gate_blockers\"]], [w[\"reason_code\"] for w in x[\"hitl\"][\"gate_warnings\"]], x[\"export_ready\"])\nprint(json.dumps(r[0], indent=1)[:2500])\nEOF\n.venv/bin/python /private/tmp/claude-501/dbg_cl.py 2>&1 | tail -60",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T13:27:28.594Z

**tool result**
````
 "token": "Ty4EuaCsY0DF6vls-a-YOg",
 "title": "case lib15 conclusory letter mist",
 "name": "case lib15 conclusory letter mist",
 "source": "paste",
 "status": "ready",
 "record_count": 9,
 "created_at": "2026-11-02T13:27:27Z",
 "updated_at": "2026-11-02T13:27:28Z",
 "last_activity_at": "2026-11-02T13:27:28Z",
 "run": {
  "stage": "finalize",
  "steps_done": 7,
  "steps_total": 8,
  "running": false,
  "error": false
 },
 "progress": {
  "entries": {
   "decided": 0,
   "total": 8
  },
  "flags": {
   "decided": 0,
   "total": 8
  },
  "amounts": {
   "decided": 0,
   "total": 11
  }
 },
 "counts": {
  "pending": 27,
  "accepted": 0,
  "edited": 0,
  "dismissed": 0,
  "needs_review": 14
 },
 "hitl": {
  "pending": 27,
  "needs_review": 14,
  "edits_to_check": 0,
  "could_not_verify": 1,
  "gate_blockers": [
   {
    "reason_code": "NOTHING_ACCEPTED",
    "kind": "case",
    "item_id": null,
    "why": "Nothing is accepted or edited yet, so the letter would be empty."
   }
  ],
  "gate_warnings": [
   {
    "reason_code": "ITEMS_NOT_REVIEWED",
    "count": 27,
    "why": "27 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them."
   }
  ]
 },
 "export_ready": false
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:27:33.680Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python /private/tmp/claude-501/dbg_cl.py 2>&1 | head -20",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T13:27:36.362Z

**tool result**
````
llm call failed call_id=ca30f489c1764 step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
list secs 0.05748891830444336
case lib15 conclusory letter m ready finalize {'entries': (0, 8), 'flags': (0, 8), 'amounts': (0, 11)} 14 1 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib14 handwritten chiro s ready finalize {'entries': (0, 8), 'flags': (0, 3), 'amounts': (0, 5)} 7 1 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib13 cloned notes cross  ready finalize {'entries': (0, 9), 'flags': (0, 2), 'amounts': (0, 3)} 4 0 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib12 records review cred ready finalize {'entries': (0, 10), 'flags': (0, 10), 'amounts': (0, 5)} 9 0 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib11 priors and ledger ready finalize {'entries': (0, 9), 'flags': (0, 12), 'amounts': (0, 8)} 15 2 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib10 eob ub04 cms1500 ready finalize {'entries': (0, 9), 'flags': (0, 2), 'amounts': (0, 11)} 9 0 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib09 spanish interpreter ready finalize {'entries': (0, 7), 'flags': (0, 5), 'amounts': (0, 7)} 15 0 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib08 second crash mri af ready finalize {'entries': (0, 12), 'flags': (0, 5), 'amounts': (0, 4)} 6 1 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib07 parking lot fall ou ready finalize {'entries': (0, 7), 'flags': (0, 6), 'amounts': (0, 2)} 4 2 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib06 lop billed vs adjus ready finalize {'entries': (0, 7), 'flags': (0, 5), 'amounts': (0, 7)} 9 1 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib05 pedestrian orif har ready finalize {'entries': (0, 8), 'flags': (0, 5), 'amounts': (0, 3)} 7 0 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib04 dog bite scar revis ready finalize {'entries': (0, 6), 'flags': (0, 2), 'amounts': (0, 3)} 5 0 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib03 truck rear end chir ready finalize {'entries': (0, 7), 'flags': (0, 4), 'amounts': (0, 3)} 7 0 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib02 slip fall prior kne ready finalize {'entries': (0, 7), 'flags': (0, 8), 'amounts': (0, 3)} 7 1 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
case lib01 er only then gap ready finalize {'entries': (0, 5), 'flags': (0, 2), 'amounts': (0, 2)} 4 1 ['NOTHING_ACCEPTED'] ['ITEMS_NOT_REVIEWED'] False
{
 "token": "0QMPwfi6eom_X0AttzSL-g",
 "title": "case lib15 conclusory letter mist",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:27:41.930Z

**tool call — Bash**
````
{
 "command": "cat >> /private/tmp/claude-501/dbg_cl.py <<'EOF'\nprint(\"----\")\ncl = c.get(\"/api/cases\").json()[\"cases\"]\nt = cl[-1][\"token\"]\ncase = c.get(f\"/api/cases/{t}\").json()\nents = case[\"entries\"]\ne = ents[0]\nprint(e[\"id\"], e[\"state\"], list(e.keys())[:30])\nr = c.post(f\"/api/cases/{t}/items/{e['id']}/review\", json={\"action\": \"edit\", \"summary\": \"Edited wording to check.\"})\nprint(r.status_code, r.text[:300])\nfor e in ents[1:]:\n    r = c.post(f\"/api/cases/{t}/items/{e['id']}/review\", json={\"action\": \"accept\"}); print(e[\"id\"], r.status_code, r.json().get(\"error\", {}).get(\"code\"))\nx = c.get(\"/api/cases\").json()[\"cases\"][-1]\nprint(x[\"progress\"], x[\"hitl\"], x[\"export_ready\"])\nEOF\n.venv/bin/python /private/tmp/claude-501/dbg_cl.py 2>&1 | sed -n '/----/,$p'",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T13:27:44.299Z

**tool result**
````
----
e1 verified ['id', 'state', 'reasons', 'why', 'review_status', 'edited', 'ladder', 'seq', 'record_ids', 'date', 'date_status', 'provider', 'summary', 'ai_drafted', 'entered_by_reviewer', 'entered_by', 'source_kind', 'excerpt', 'excerpt_start', 'excerpt_end', 'duplicate_note', 'translation', 'edit_to_check']
422 {"error":{"code":"invalid_edit","message":"Nothing to edit.","detail":{}}}
e2 422 CODE_CHECK_FAILED
e4 422 CODE_CHECK_FAILED
e5 200 None
e6 200 None
{'entries': {'decided': 2, 'total': 5}, 'flags': {'decided': 0, 'total': 2}, 'amounts': {'decided': 0, 'total': 2}} {'pending': 7, 'needs_review': 4, 'edits_to_check': 0, 'could_not_verify': 1, 'gate_blockers': [], 'gate_warnings': [{'reason_code': 'ITEMS_NOT_REVIEWED', 'count': 7, 'why': '7 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.'}]} True
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:27:47.235Z

**tool call — Bash**
````
{
 "command": "grep -n \"Nothing to edit\" -B12 app/backend/review.py | head -40"
}
````

### User / tool · 2026-11-02T13:27:47.318Z

**tool result**
````
298-                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed"), "ocr_derived": ocr_derived,
299-                                               "translated": language.translated_record(rec)})      # D-050: an edit or a manual entry over a Spanish quote is still never verified
300-    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
301-            "judge_error": judge_error, "state": state, "reasons": reasons}
302-
303-
304-# ---------------------------------------------------------------- edit
305-def _edit(conn, case_id, kind, item, body, call, t):
306-    edits = body.get("edits")
307-    if kind == "amount":
308-        raise _bad("A charge can only be accepted or dismissed.")
309-    if not isinstance(edits, dict) or not edits:
310:        raise _bad("Nothing to edit.")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:27:57.164Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_case_list.py'\ns=open(p).read()\ns=s.replace('''    text = (LIB''','''    second = local.get(f\"/api/cases/{toks[LIB_IDS[1]]}\").json()[\"entries\"][0]          # a reworded entry: saved, but the second check cannot confirm the new wording\n    local.post(f\"/api/cases/{toks[LIB_IDS[1]]}/items/{second['id']}/review\", json={\"action\": \"edit\", \"edits\": {\"summary\": second[\"summary\"].rstrip(\".\") + \" (reworded).\"}})\n    third = toks[LIB_IDS[2]]                                                                  # accept whatever the code checks allow: a case whose export gate opens\n    for k in (\"entries\", \"flags\", \"amounts\"):\n        for it in local.get(f\"/api/cases/{third}\").json()[k]:\n            local.post(f\"/api/cases/{third}/items/{it['id']}/review\", json={\"action\": \"accept\"})\n    text = (LIB''',1)\ns=s.replace('''def test_title_is_readable''','''def test_decided_cases_cover_ready_and_edit_to_check(local, cases):\n    s = _by_token(local)\n    third = s[cases[LIB_IDS[2]]]\n    assert third[\"export_ready\"] is True and third[\"hitl\"][\"gate_blockers\"] == [] and sum(v[\"decided\"] for v in third[\"progress\"].values()) > 0\n    assert s[cases[LIB_IDS[1]]][\"progress\"][\"entries\"][\"decided\"] <= s[cases[LIB_IDS[1]]][\"progress\"][\"entries\"][\"total\"]\n\n\ndef test_title_is_readable''')\ns=s.replace('''    for lid in LIB_IDS:\n        t = s[cases[lid]][\"title\"]\n        assert t and \"_\" not in t and not t.endswith((\".txt\", \".pdf\")), t\n''','''    for lid in LIB_IDS:\n        t = s[cases[lid]][\"title\"]\n        assert t and \"_\" not in t and not t.endswith((\".txt\", \".pdf\")) and not t.lower().startswith((\"case \", \"lib\")), t\n    assert s[cases[LIB_IDS[0]]][\"title\"] == \"Er only then gap\"\n''')\ns=s.replace('''    assert case_list.readable_title(\"records_final''','''    assert case_list.readable_title(\"case_01_date_formats\", \"paste\", 0) == \"Date formats\"\n    assert case_list.readable_title(\"records_final''')\nopen(p,'w').write(s)\n\np='app/backend/case_list.py'\ns=open(p).read()\ns=s.replace('''_EXT = ''','''_LIB_PREFIX = re.compile(r\"^case[ _](?:lib)?\\\\d+[ _]\", re.IGNORECASE)      # evals/library and evals/golden file names: case_lib01_..., case_01_...\n_EXT = ''')\ns=s.replace('''    n = (name or \"\").strip()\n''','''    n = _LIB_PREFIX.sub(\"\", (name or \"\").strip())\n''')\ns=s.replace('''    if n and _SLUG.match(n) and not n.isalpha():          # one token with _ - . in it: a file name or slug, not a typed name\n        n = re.sub(''','''    if n and (_SLUG.match(n) or n != (name or \"\").strip()) and not n.isalpha():          # one token with _ - . in it, or a library prefix: a file name or slug, not a typed name\n        n = re.sub(''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_case_list.py -x -q 2>&1 | tail -20",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T13:28:01.075Z

**tool result**
````
.......                                                                  [100%]
7 passed in 3.56s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:28:05.396Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/dbg2.py <<'EOF'\nimport sys; sys.path.insert(0,\"/Users/arsis/zlayt-pm-project\")\nimport pytest, tests.unit.test_case_list as T\nEOF\n.venv/bin/python -m pytest tests/unit/test_case_list.py -q -k decided_cases 2>&1 | tail -3; python3 - <<'EOF'\nimport re\np='/Users/arsis/zlayt-pm-project/tests/unit/test_case_list.py'\ns=open(p).read()\ns=s.replace('''    assert s[cases[LIB_IDS[1]]][\"progress\"][\"entries\"][\"decided\"] <= s[cases[LIB_IDS[1]]][\"progress\"][\"entries\"][\"total\"]''','''    print(\"EDIT\", s[cases[LIB_IDS[1]]][\"hitl\"], s[cases[LIB_IDS[1]]][\"progress\"])''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_case_list.py -q -s -k decided_cases 2>&1 | grep EDIT",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T13:28:11.250Z

**tool result**
````
.                                                                        [100%]
1 passed, 6 deselected in 2.46s
EDIT {'pending': 17, 'needs_review': 8, 'edits_to_check': 1, 'could_not_verify': 1, 'gate_blockers': [{'reason_code': 'NOTHING_ACCEPTED', 'kind': 'case', 'item_id': None, 'why': 'Nothing is accepted or edited yet, so the letter would be empty.'}], 'gate_warnings': [{'reason_code': 'ITEMS_NOT_REVIEWED', 'count': 17, 'why': '17 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.'}, {'reason_code': 'EDIT_NOT_CONFIRMED', 'count': 1, 'why': '1 edit is still marked Needs review (the second check did not confirm it), so it is not in the letter and is not counted as accepted until you compare it with the quote and accept.'}]} {'entries': {'decided': 0, 'total': 7}, 'flags': {'decided': 0, 'total': 8}, 'amounts': {'decided': 0, 'total': 3}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:28:12.421Z

Edit-to-check is exercised. Lock that into the test.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:28:14.141Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_case_list.py'\ns=open(p).read()\ns=s.replace('''    print(\"EDIT\", s[cases[LIB_IDS[1]]][\"hitl\"], s[cases[LIB_IDS[1]]][\"progress\"])''','''    second = s[cases[LIB_IDS[1]]]\n    assert second[\"hitl\"][\"edits_to_check\"] == 1 and second[\"progress\"][\"entries\"][\"decided\"] == 0          # a reworded entry is saved but not decided\n    assert \"EDIT_NOT_CONFIRMED\" in [w[\"reason_code\"] for w in second[\"hitl\"][\"gate_warnings\"]]''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider 2>&1 | tail -15",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T13:33:05.698Z

**tool result**
````
........................................................................ [ 75%]
........................................................................ [ 77%]
........................................................................ [ 79%]
........................................................................ [ 81%]
........................................................................ [ 83%]
........................................................................ [ 85%]
........................................................................ [ 87%]
........................................................................ [ 89%]
........................................................................ [ 91%]
........................................................................ [ 93%]
........................................................................ [ 94%]
........................................................................ [ 96%]
........................................................................ [ 98%]
................................................                         [100%]
3791 passed, 1 skipped in 289.85s (0:04:49)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:33:13.735Z

**tool call — Bash**
````
{
 "command": "grep -n \"^## \" memory/contracts/api.md | head -40"
}
````

### User / tool · 2026-11-02T13:33:13.813Z

**tool result**
````
5:## Conventions
14:## Endpoint index
45:## GET /api/health
58:## POST /api/cases
78:## POST /api/cases/pdf (D-031)
106:## POST /api/cases/{token}/review/batch (D-031)
110:## /api/cases/{token}/export_config (D-031)
113:## POST /api/cases/{token}/run
120:## GET /api/cases/{token}/status
130:## GET /api/cases/{token}
261:## POST /api/cases/{token}/records/{rid}/confirm_date
282:## Date-convention suggestion (T-088, D-042): `dates_to_confirm[].suggestion`
294:## Dismissal-pattern suggestions (T-089, D-042): `GET /api/cases/{token}/dismissal_suggestions`
309:## GET /api/cases/{token}/items/{item_id}  — "Why?"
327:## POST /api/cases/{token}/items/{item_id}/review
372:## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
398:## GET /api/cases/{token}/export
549:## GET /api/cases/{token}/audit
569:## Check traces (D-042): per-item stepper, case stepper, judge summary
674:## POST /api/cases/{token}/rejudge  (D-044)
684:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
690:## GET /api/calibration  (T-099, serves T-090 counts to T-096)
700:## GET /api/cases/{token}/billing  (T-083, D-042, D-052)
735:## Spanish-language records (T-085, D-042)
751:## Summary clause trimming (T-112, D-054)
754:## Dollar amounts in entries (T-139, D-019, R-CH-7, R-EX-8)
764:## DELETE /api/cases/{token}
769:## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:33:17.177Z

**tool call — Bash**
````
{
 "command": "sed -n 684,690p memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T13:33:17.272Z

**tool result**
````
## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays token-only and has no case list.
`GET /api/cases` -> `{ "cases": [ { "token", "name", "status", "source", "record_count", "counts": {"pending","accepted","edited","dismissed","needs_review"}, "created_at" } ] }`, newest first, never record text.
`GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
`POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).

## GET /api/calibration  (T-099, serves T-090 counts to T-096)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:33:29.057Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='memory/contracts/api.md'\ns=open(p).read()\nold=[l for l in s.split(\"\\n\") if l.startswith('`GET /api/cases` -> `{ \"cases\": [ { \"token\", \"name\"')][0]\nnew='''`GET /api/cases` (T-148, the overview screen) -> `{ \"cases\": [ summary ] }`, newest first (`created_at`, then insertion order); every case the single local profile can see. Code only: no model call, no pipeline run, no record text. Local mode only: no auth, no users, no sharing (scope cut kept). One `summary`:\n```\n{ \"token\": \"...\", \"title\": \"Er only then gap\", \"name\": \"case lib01 er only then gap\" | null, \"source\": \"paste|sample|library\", \"status\": \"ingested|running|ready|failed\",\n  \"record_count\": 9, \"created_at\": \"...Z\", \"updated_at\": \"...Z\", \"last_activity_at\": \"...Z\",\n  \"run\": { \"stage\": \"finalize\" | \"ingest\" | null, \"steps_done\": 7, \"steps_total\": 8, \"running\": false, \"error\": false },\n  \"progress\": { \"entries\": {\"decided\": 2, \"total\": 5}, \"flags\": {\"decided\": 0, \"total\": 2}, \"amounts\": {\"decided\": 0, \"total\": 2} },\n  \"counts\": { \"pending\", \"accepted\", \"edited\", \"dismissed\", \"needs_review\" },\n  \"hitl\": { \"pending\": 7, \"needs_review\": 4, \"edits_to_check\": 0, \"could_not_verify\": 1,\n            \"gate_blockers\": [ { \"reason_code\", \"kind\", \"item_id\", \"why\" } ], \"gate_warnings\": [ { \"reason_code\", \"count\", \"why\" } ] },\n  \"export_ready\": true }\n```\n`title` is what to show: the case name made readable (a file name or slug such as `smith_records-2024.pdf` becomes \"Smith records 2024\", the `case_lib01_` library prefix is dropped), or \"Untitled case, Nov 2\" / \"Sample case\" when it has no name; `name` is the stored value. `updated_at` is the same value as `GET /api/cases/{token}` (`run_finished_at`, else `created_at`); `last_activity_at` also counts the latest accept/edit/dismiss. `run` is `/status` (`stage`, `progress.done`, `progress.total`). `progress` counts the live items `review.counts` counts (not rejected, no answered tray placeholder, no rule-filtered proposal): `decided` = accepted, edited or dismissed, and a reworded entry still marked Needs review is NOT decided (T-134); `total - decided` over the three kinds = `hitl.pending + hitl.edits_to_check`. `hitl.needs_review` / `edits_to_check` / `pending` are `GET /api/cases/{token}` `review.counts` (`needs_review`, `edit_to_check`, `pending`); `could_not_verify` is the length of that case's `tray`. `gate_blockers` / `gate_warnings` are the `blockers` / `warnings` of the `export_gate` step of `GET /api/cases/{token}/trace` (same `reason_code` and plain `why`; the blockers are exactly what makes `GET .../export` answer 422), and `export_ready` is the gate's `ready`. A case with warnings only (items not reviewed, edits to check) is `export_ready: true`. `tests/unit/test_case_list.py` compares every field with those routes for every library case.'''\ns=s.replace(old,new)\nopen(p,'w').write(s)\nEOF\ngit diff HEAD --stat -- memory/contracts/api.md; git diff HEAD -- memory/contracts/api.md | grep '^@@'"
}
````

### User / tool · 2026-11-02T13:33:29.199Z

**tool result**
````
 memory/contracts/api.md | 13 ++++++++++++-
 1 file changed, 12 insertions(+), 1 deletion(-)
@@ -683,7 +683,18 @@ Run the second check again for the AI-made items whose judge never answered (the
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:33:36.816Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/\"source\": \"paste|sample|library\"/\"source\": \"paste|sample\"/' memory/contracts/api.md && git status --short app/backend/api.py app/backend/case_list.py tests/unit/test_case_list.py memory/contracts/api.md; git diff HEAD --stat -- app/backend/api.py; git log -1 --format=%h"
}
````

### User / tool · 2026-11-02T13:33:36.956Z

**tool result**
````
 M app/backend/api.py
 M memory/contracts/api.md
?? app/backend/case_list.py
?? tests/unit/test_case_list.py
 app/backend/api.py | 7 +++----
 1 file changed, 3 insertions(+), 4 deletions(-)
5de16d3
[This command modified 1 file you've previously read: memory/contracts/api.md. Call Read before editing.]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:33:41.053Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx_t148 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add app/backend/api.py app/backend/case_list.py tests/unit/test_case_list.py memory/contracts/api.md && git diff --cached --stat"
}
````

### User / tool · 2026-11-02T13:33:41.296Z

**tool result**
````
 app/backend/api.py           |   7 +-
 app/backend/case_list.py     |  83 +++++++++++++++++++++++
 memory/contracts/api.md      |  13 +++-
 tests/unit/test_case_list.py | 156 +++++++++++++++++++++++++++++++++++++++++++
 4 files changed, 254 insertions(+), 5 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:33:44.289Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx_t148 && git commit -q -m \"feat(backend): GET /api/cases summary list for the case overview (T-148)\n\nPer case: readable title, created/updated, run stage, decided/total per kind, HITL call-outs\n(needs review, edits to check, could-not-verify tray, gate blockers and warnings), export_ready.\nComputed from the functions GET case, /status and the export gate use; test compares all of them for every library case.\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log -1 --format=%h"
}
````

### User / tool · 2026-11-02T13:33:44.838Z

**tool result**
````
check_secrets: ok (4 file(s) scanned staged)
d19ae46
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:33:50.829Z

**tool call — Bash**
````
{
 "command": "unset GIT_INDEX_FILE; git reset -q -- app/backend/api.py app/backend/case_list.py tests/unit/test_case_list.py memory/contracts/api.md; git status --short app/backend/api.py app/backend/case_list.py tests/unit/test_case_list.py memory/contracts/api.md\nB=\"python3 tools/board.py\"\n$B ac T-148 --check 1 --agent backend --evidence \"tests/unit/test_case_list.py (7 tests): every summary field compared with GET case, /status, /trace export_gate and /export for all 15 library cases; full unit suite 3791 passed\"\n$B handoff T-148 --agent backend --text \"What changed: app/backend/case_list.py (new) builds GET /api/cases summaries (title, created/updated/last_activity, run stage, decided/total per kind, hitl needs_review/edits_to_check/could_not_verify/gate blockers+warnings, export_ready); api.py: route calls it, /status uses its run_progress (3 lines); api.md section. How verified: tests/unit/test_case_list.py vs GET case, /status, /trace, /export for all library cases (incl. an edit-to-check case and an export-ready case); full unit suite 3791 passed, 1 skipped. Cost: ~60 ms for 15 cases, no LLM, no pipeline. What's left: present.case_list is now dead code (present.py had staged hunks from others, left alone); old fields name/status/source/record_count/counts/created_at kept for the existing UI. Surprised me: GET /api/cases already existed as a thin list; commit d19ae46 via temp index.\"\n$B commit T-148 --sha d19ae46 --agent backend\n$B move T-148 in_review --agent backend"
}
````

### User / tool · 2026-11-02T13:33:51.177Z

**tool result**
````
AC 1 checked: tests/unit/test_case_list.py (7 tests): every summary field compared with GET case, /status, /trace export_gate and /export for all 15 library cases; full unit suite 3791 passed
handoff written on T-148
T-148: commit d19ae46 recorded
T-148: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:33:55.306Z

T-148 is in_review: `GET /api/cases` now returns the full per-case summary you listed, plus a `last_activity_at` field. The full unit suite passed (3791 passed, 1 skipped); nothing failed from the other workers' in-flight amounts or charge-text changes. Committed as d19ae46.

- **What changed:** the new module `app/backend/case_list.py` builds the summaries and `api.py` calls it. `/status` now reads the run stage from the same helper, and the contract is documented in `memory/contracts/api.md`. `GET /api/cases` already existed as a thin list, so I replaced its body and kept the old fields for the current UI.
- **How verified:** `tests/unit/test_case_list.py` compares every field with GET case, `/status`, the `/trace` export gate and `/export` for all 15 library cases. It also covers an edit-to-check case and an export-ready case. The list costs about 60 ms for 15 cases, with no model calls and no pipeline run.
- **Left over:** `present.case_list` is now dead code. I left it because `present.py` had staged changes from other workers.
