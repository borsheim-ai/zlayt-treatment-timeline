# Subagent: Backend: T-088 + T-089 (Backend: T-088 + T-089)

Source: `agent-aa8093ca96a188ac9.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:16:42.389Z

You own board cards T-088 and T-089 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Run `board.py show` on each and read D-042 in memory/ORCHESTRATOR_DECISIONS.md.

- **T-088 — date-convention suggestion:** for an ambiguous numeric date (e.g. 04/05/2026), the API suggests MM/DD or DD/MM with a stated reason taken from other unambiguous dates in the same packet (e.g. "Other dates in this record use month first (03/14/2026)"). This is code only, in app/backend/dates.py or a new module. It's never auto-applied: the paralegal still confirms once (D-041). Add a unit test, plus an eval-style test case in tests/unit; the golden set is qa's, so add a card note if golden needs a case.
- **T-089 — dismissal-pattern suggestions for a single local profile:** repeated dismissals of the same flag phrase or category surface as a suggestion ("You dismissed this kind of flag 4 times. Hide similar ones in this case?"). It never auto-dismisses. There's one local profile with no users and no auth, stored locally. Show that recall on golden doesn't change, because suggestions never alter pipeline output. Add a unit test.

Write the contract into api.md for both, and note on each card what the UI needs.

**Shared rules (8 workers are running in parallel):**
- Put the logic in new modules. In shared files (api.py, pipeline.py, api.md, app/db), make the smallest possible edit, re-read the file right before editing, and never reformat. If a db change is needed, keep it minimal and note it for the db owner.
- Don't touch flags.py or judges.py (T-094 is in them), evals/library, or evals/run.py.
- Commit only your own hunks. Use a temp index (`GIT_INDEX_FILE=$(mktemp) git read-tree HEAD`, then add your paths or patches) when a shared file has other workers' edits; otherwise `git add <paths>` then `git commit -m "..." -- <paths>` as separate commands. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".
- Run `.venv/bin/python -m pytest -q tests/unit`. If a failure is in someone else's area, name it and move on.
- Then `board.py ac`, the handoff, and `move <card> in_review --agent backend`, for each card. Reply in 2 lines.

### User / tool · 2026-11-02T04:16:42.393Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:45.763Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B show T-088; $B show T-089; grep -n \"D-042\" -A25 memory/ORCHESTRATOR_DECISIONS.md | head -60; grep -n \"D-041\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -30; cat app/backend/dates.py | head -80; ls app/backend tests/unit; git status --short | head -30"
}
````

### User / tool · 2026-11-02T04:16:46.016Z

**tool result**
````
---
id: "T-088"
title: "Date-convention suggestion (pre-select with stated reason, still one confirm)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:16:04Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "For an ambiguous numeric date, the API suggests MM/DD or DD/MM with the reason (other dates in the packet), the UI pre-selects it, and the paralegal still confirms once; never auto-applied; eval case", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed

## Handoff (filled when moving to in_review)

---
id: "T-089"
title: "Dismissal-pattern suggestions for a single local profile (suggestions only)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:16:04Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Repeated dismissals of the same flag phrase surface as a suggestion ('You dismissed this 4 times'); never auto-dismisses; per-profile local only; eval shows no recall loss on golden", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed

## Handoff (filled when moving to in_review)

50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
51-| D-043 | Credibility flags fail toward flagging (2026-11-02, after T-067 r3): any sentence containing a credibility term flags, **unless** the whole sentence is one clause matching a short allow-list of clean negations ('No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Not tested/not performed.'). Anything with a second clause, contrast word or side qualifier flags. An extra flag costs one paralegal click; a missed one costs credibility at the adjuster. | Three rounds of clause-scoped negation each regressed a different word order. | T-067 claims-adjuster r3 |
52-| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
53-| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
49:| D-041 | An entry with no confirmed date cannot be accepted into the letter (2026-11-02). Accept returns 422 `DATE_UNCONFIRMED` until the paralegal confirms a date (Dates to confirm) or the entry is moved to the notes block. The UI disables Accept with the reason shown. 'Date not stated' never appears in the treatment section. | A demand letter treatment line without a date is unusable and invites an adjuster challenge. | T-068 paralegal r2 major |
50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
51-| D-043 | Credibility flags fail toward flagging (2026-11-02, after T-067 r3): any sentence containing a credibility term flags, **unless** the whole sentence is one clause matching a short allow-list of clean negations ('No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Not tested/not performed.'). Anything with a second clause, contrast word or side qualifier flags. An extra flag costs one paralegal click; a missed one costs credibility at the adjuster. | Three rounds of clause-scoped negation each regressed a different word order. | T-067 claims-adjuster r3 |
52-| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
53-| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
"""Date parsing by an explicit format list (code only). R-IN-3, R-TL-3, LLM_VS_CODE row 2.

parse_date(raw) -> {raw, status: parsed|ambiguous|missing, iso, candidates}. Nothing is ever guessed: a numeric date whose first two
numbers are both 1-12 and differ is `ambiguous` with both readings; anything unreadable or impossible is `missing`."""
import datetime as _dt
import re

MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"])}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})
MONTHS["sept"] = 9

_ISO = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\Z")
_NUM = re.compile(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{4}|\d{2})\Z")
_MDY = re.compile(r"^(?:[A-Za-z]{3,9},?\s+)?([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\Z")
_DMY = re.compile(r"^(?:[A-Za-z]{3,9},?\s+)?(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([A-Za-z]{3,9})\.?,?\s+(\d{4})\Z")


def _iso(y: int, m: int, d: int):
    try:
        return _dt.date(y, m, d).isoformat()
    except ValueError:
        return None


PIVOT_YY = 40   # two-digit year yy <= 40 reads as 20yy; above that it could be 19yy or 20yy, so the date is ambiguous (D-027)


def _years(s: str) -> list:
    if len(s) == 4:
        return [int(s)]
    yy = int(s)
    return [2000 + yy] if yy <= PIVOT_YY else [1900 + yy, 2000 + yy]


def _out(raw, status, iso=None, candidates=None):
    return {"raw": raw, "status": status, "iso": iso, "candidates": sorted(candidates or [])}


def parse_date(raw) -> dict:
    """Never guesses. Numeric dates: month/day order is ambiguous when both numbers are 1-12 and differ; a two-digit year above
    PIVOT_YY (40) is ambiguous between 19yy and 20yy (`03-17-98` -> 1998-03-17 or 2098-03-17). All readings are returned as candidates."""
    s = " ".join(str(raw or "").split())
    if not s:
        return _out(raw, "missing")
    m = _ISO.match(s)
    if m:
        iso = _iso(int(m[1]), int(m[2]), int(m[3]))
        return _out(raw, "parsed", iso) if iso else _out(raw, "missing")
    m = _NUM.match(s)
    if m:
        a, b = int(m[1]), int(m[2])
        if a > 12 and b > 12:
            return _out(raw, "missing")
        orders = [(b, a)] if a > 12 else [(a, b)] if (b > 12 or a == b) else [(a, b), (b, a)]
        cands = {i for y in _years(m[3]) for mo, d in orders for i in [_iso(y, mo, d)] if i}
        if not cands:
            return _out(raw, "missing")
        return _out(raw, "parsed", next(iter(cands))) if len(cands) == 1 else _out(raw, "ambiguous", None, cands)
    m = _MDY.match(s)
    if m and m[1].lower() in MONTHS:
        iso = _iso(int(m[3]), MONTHS[m[1].lower()], int(m[2]))
        return _out(raw, "parsed", iso) if iso else _out(raw, "missing")
    m = _DMY.match(s)
    if m and m[2].lower() in MONTHS:
        iso = _iso(int(m[3]), MONTHS[m[2].lower()], int(m[1]))
        return _out(raw, "parsed", iso) if iso else _out(raw, "missing")
    return _out(raw, "missing")


def days_between(a_iso: str, b_iso: str) -> int:
    """Calendar days from a to b (real calendar, leap years included)."""
    return (_dt.date.fromisoformat(b_iso) - _dt.date.fromisoformat(a_iso)).days


def confirm(parsed: dict, chosen_iso: str) -> dict:
    """confirm_date hook (R-IN-5): the paralegal may only choose one of the code-proposed readings. Returns the confirmed date dict."""
    if parsed.get("status") != "ambiguous" or chosen_iso not in parsed.get("candidates", []):
        raise ValueError("date_invalid")
    return {**parsed, "status": "confirmed", "iso": chosen_iso}
app/backend:
__init__.py
__pycache__
amounts.py
api.py
case_extras.py
confidence.py
conflict_candidates.py
conflicts.py
credibility.py
dates.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judges.py
lexicon.py
lexicon_scan.py
narrative.py
pdf_text.py
pipeline.py
present.py
rejudge.py
review.py
schemas.py
sentences.py
split_llm.py
store.py
totals.py
trace.py
why.py

tests/unit:
__init__.py
__pycache__
_fakes.py
_golden.py
_pdf.py
test_amounts.py
test_api.py
test_api_routes.py
test_audited.py
test_backend_no_speaker_label.py
test_boundaries.py
test_case_extras.py
test_confidence.py
test_conflict_candidates.py
test_conflicts.py
test_date_unconfirmed.py
test_dates.py
test_db.py
test_e2e_contract.py
test_eval_matching.py
test_eval_runner.py
test_eval_spec_check.py
test_export.py
test_export_edge.py
test_flag_templates.py
test_flags_injection.py
test_flags_pass.py
test_flags_sample.py
test_frontend_no_speaker_label.py
test_gaps.py
test_generator.py
test_grounding.py
test_grounding_may.py
test_ingest.py
test_injection.py
test_judges.py
test_library_denylist.py
test_manual_and_split.py
test_multicase.py
test_narrative.py
test_pdf_upload.py
test_pipeline.py
test_provider.py
test_provider_backends.py
test_review_rules.py
test_schemas.py
test_sentences.py
test_split_llm.py
test_t033_backend.py
test_t037_backend.py
test_t075_determinism.py
test_t093_eval_signature.py
test_totals.py
test_trace.py
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/frontend/api.js
 M app/frontend/export.js
 M app/frontend/judges.js
 M app/frontend/stepper.css
 M app/frontend/stepper.js
 M app/frontend/timeline.js
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-060.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:48.510Z

**tool call — Bash**
````
{
 "command": "grep -n \"ambiguous\\|confirm_date\\|dismiss\" app/backend/api.py | head -50; grep -n \"dismiss\" app/backend/review.py app/backend/store.py app/db/*.py app/db/*.sql 2>/dev/null | head -30; grep -n \"^## \\|^### \" memory/contracts/api.md | tail -40; wc -l memory/contracts/api.md; git status --short app/backend memory/contracts tests | head"
}
````

### User / tool · 2026-11-02T04:16:48.646Z

**tool result**
````
401:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
402:    async def confirm_date(token: str, rid: str, request: Request):
409:            return review.confirm_date(c, token, rid, b["date"])
515:                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
app/backend/review.py:3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
app/backend/review.py:13:ACTIONS = ("accept", "dismiss", "reset", "edit")
app/backend/review.py:66:        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
app/backend/review.py:70:    if action in ("accept", "dismiss", "reset"):
app/backend/review.py:72:        if kind == "flag" and action == "dismiss" and body.get("note"):
app/backend/review.py:120:        raise _bad("A charge can only be accepted or dismissed.")
app/db/schema.sql:23:  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
app/db/schema.sql:32:  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
app/db/schema.sql:43:  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
app/db/schema.sql:57:  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry')),
app/db/db.py:17:REVIEW_STATUSES = ("pending", "accepted", "edited", "dismissed")
app/db/db.py:18:ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
app/db/db.py:207:    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
5:## Conventions
14:## Endpoint index
40:## GET /api/health
53:## POST /api/cases
73:## POST /api/cases/pdf (D-031)
77:## POST /api/cases/{token}/review/batch (D-031)
80:## /api/cases/{token}/export_config (D-031)
83:## POST /api/cases/{token}/run
90:## GET /api/cases/{token}/status
100:## GET /api/cases/{token}
218:## POST /api/cases/{token}/records/{rid}/confirm_date
233:## GET /api/cases/{token}/items/{item_id}  — "Why?"
251:## POST /api/cases/{token}/items/{item_id}/review
285:## GET /api/cases/{token}/export
436:## GET /api/cases/{token}/audit
456:## Check traces (D-042): per-item stepper, case stepper, judge summary
463:### Step (shared by all three endpoints)
481:### GET /api/cases/{token}/items/{item_id}/trace
513:### GET /api/cases/{token}/trace
545:### GET /api/cases/{token}/judges
561:## POST /api/cases/{token}/rejudge  (D-044)
571:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
577:## DELETE /api/cases/{token}
582:## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
     606 memory/contracts/api.md
 M tests/e2e/conftest.py
 M tests/e2e/test_ladder_gate.py
 M tests/e2e/test_local_mode.py
 M tests/e2e/test_stepper.py
?? app/backend/conflict_candidates.py
?? tests/e2e/test_rerun_judge.py
?? tests/fixtures/llm/0115c20756060b7547d09ea7174734c62c4d2c54f0cc9840da3f4be1c00e19bb.json
?? tests/fixtures/llm/04b3f408728cf86944506b0d48307520196ec5bca54e76f2bb76077acbb993f3.json
?? tests/fixtures/llm/0624808694020c61c3a27541ebe7970301ed714e3c3b89b0769e868c72f22b4e.json
?? tests/fixtures/llm/0802d59b78c2e7bf6fa1aa6b7a09db9ce5d1cb63dc8903d20c74e67639734cb0.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:50.579Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p memory/contracts/api.md; sed -n 100,135p memory/contracts/api.md; sed -n 215,235p memory/contracts/api.md; sed -n 380,420p app/backend/api.py; sed -n 495,540p app/backend/api.py; sed -n 1,30p app/backend/conflict_candidates.py; sed -n 40,100p app/backend/review.py; grep -n \"dates_to_confirm\\|date_status\\|\\\"ambiguous\\\"\" app/backend/*.py | head -30"
}
````

### User / tool · 2026-11-02T04:16:50.700Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:52.991Z

**tool call — Bash**
````
{
 "command": "sed -n 14,40p memory/contracts/api.md | cut -c1-220; sed -n 215,235p memory/contracts/api.md | cut -c1-400; grep -n \"candidates\\|dates_to_confirm\\|ambiguous\" app/backend/*.py | grep -v \"^app/backend/dates.py\" | head -30; sed -n 395,420p app/backend/api.py; sed -n 1,40p app/backend/conflict_candidates.py"
}
````

### User / tool · 2026-11-02T04:16:53.104Z

**tool result**
````
## Endpoint index
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | backend, demo mode, models, limits, banner text |
| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
| GET | `/api/cases/{token}` | the whole case for the review screen |
| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
| GET | `/api/cases/{token}/status` | stage and progress |
| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt, confirm_warnings?}`; `excerpt` must be whole verbatim sentences of that record (`422 in
| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other record
| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquot
| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also 
| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous 
| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export 
| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `
| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |

---

## GET /api/health
```
(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` examp

## POST /api/cases/{token}/records/{rid}/confirm_date
Resolves a record whose `date_status` is `ambiguous` by choosing one of the readings the code proposed (`date_candidates`). It is not an edit (D-010). A record with no readable date (`missing`) cannot be confirmed; it stays excluded and flagged. Request:
```json
{ "date": "2026-05-04" }
```
Response 200: the record with `date_status: "confirmed"`, its entry's date, the **recomputed gap flags** (a changed or new flag keeps no review status; an unchanged record pair keeps its status), the cleared `date_ambiguous` record warning, and `dates_to_confirm`:
```json
{ "record": {"id": "r8", "date_iso": "2026-05-04", "date_status": "confirmed", "date_raw": "04/05/2026"},
  "entry": {"id": "e8", "date": "2026-05-04", "moved_from": "undated_entries"},
  "gap_flags": [],
  "removed_flag_ids": ["f_warn_date_r8"],
  "dates_to_confirm": [], "warnings": [] }
```
`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event whose `after` records the chosen date (`date_chosen`, `date_raw`, `candidates`, `record_id`) and the ids whose `DATE_AMBIGUOUS` reason it cleared. Confirming also removes `DATE_AMBIGUOUS` from the entry's `reasons` and recomputes its `

## GET /api/cases/{token}/items/{item_id}  — "Why?"
Ladder, the audited calls behind the item, and the source record text with the highlight range. Prompt text is not returned here (it is in the per-case audit).
```json
app/backend/api.py:297:                    "dates_to_confirm": present.dates_to_confirm(c, cid),
app/backend/confidence.py:20:_DATE = {"ambiguous": "DATE_AMBIGUOUS", "missing": "DATE_MISSING"}
app/backend/confidence.py:43:_CTX_KEYS = {"injection", "date_status", "amount_class", "agreement", "fixture_miss", "split_ambiguous", "llm_failed",
app/backend/confidence.py:63:    for key, code in (("fixture_miss", "FIXTURE_MISS"), ("split_ambiguous", "SPLIT_AMBIGUOUS"), ("llm_split", "LLM_SPLIT"),
app/backend/conflict_candidates.py:121:def candidates(records: list) -> list:
app/backend/conflict_candidates.py:122:    """All candidates in a fixed order (rule, then record numbers). Same records in, same list out."""
app/backend/flag_templates.py:38:    "date_ambiguous": "record_warning", "injection_suspected": "record_warning", "analysis_incomplete": "record_warning", "llm_split": "record_warning",
app/backend/flag_templates.py:135:    "date_ambiguous": _date_amb,
app/backend/gaps.py:30:    """needs_review reasons: an undated/ambiguous encounter record whose date could fall inside the span (ADR-010), or an injection-tagged endpoint."""
app/backend/gaps.py:35:        cands = r.get("date_candidates") or []
app/backend/ingest.py:115:    an `unsplit` record (D-027) and the split is reported ambiguous."""
app/backend/ingest.py:118:        return [_record(1, text, 0, len(text), {"date_raw": "", "source": "", "excerpt": text})], "ambiguous"
app/backend/ingest.py:127:            method = "ambiguous"
app/backend/ingest.py:132:        method = "ambiguous"
app/backend/ingest.py:263:    eligible = method == "ambiguous" and len(recs) == 1 and (recs[0]["unsplit"] or not (recs[0]["date_raw"] and recs[0]["source"]))
app/backend/ingest.py:266:    elif method == "ambiguous" and not eligible and len(recs) > 1:
app/backend/ingest.py:299:    elif method == "ambiguous":
app/backend/ingest.py:319:        r.update(id=rid, seq=r["n"], date_iso=p["iso"], date_status=p["status"], date_candidates=p["candidates"], kind=kind,
app/backend/ingest.py:331:            to_confirm.append({"record_id": rid, "raw": r["date_raw"], "candidates": p["candidates"]})
app/backend/ingest.py:332:            warns.append(_warn("DATE_EXCLUDED_FROM_GAPS", "A record date is ambiguous or unreadable; it is left out of gap checks until confirmed.", rid))
app/backend/ingest.py:333:            record_warnings.append({"type": "record_warning", "category": "date_ambiguous", "record_no": r["n"],
app/backend/ingest.py:345:                                                             raw=r["date_raw"] if w["category"] == "date_ambiguous" else None)
app/backend/ingest.py:348:    return {"banner": first if first in BANNERS else None, "records": recs, "groups": groups, "split_method": method if method in ("code", "llm") else "ambiguous", "split_failure": split_failure, "split_detail": split_detail, "warnings": warns,
app/backend/ingest.py:349:            "dates_to_confirm": to_confirm, "record_warnings": record_warnings,
app/backend/pipeline.py:41:    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
app/backend/pipeline.py:42:        ctx["date_status"] = "ambiguous"
app/backend/pipeline.py:76:        ctx = {"llm_split": True} if w["category"] == "llm_split" else {"injection": inj, "date_status": None if inj else "ambiguous"}
app/backend/pipeline.py:96:            "dates_to_confirm": ing["dates_to_confirm"], "flags": flags, "amounts": amounts, "damages": damages, "warnings": warnings,
app/backend/pipeline.py:158:                          date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
app/backend/pipeline.py:379:            "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
                               "flags": len(DB.list_items(c, token, "flag"))},
                    "error": json.loads(case["error"]) if case["error"] else None,
                    "elapsed_ms": int((end - case["run_started_at"]) * 1000) if case["run_started_at"] else 0}
        finally:
            c.close()

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

    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
    async def manual_entry(token: str, rid: str, request: Request):
        """D-031: the reviewer writes the entry for a record the AI could not make one for. Quote = whole verbatim sentences (422 otherwise)."""
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            return review.manual_entry(c, token, rid, b, call=make_call(c, token))
"""Cross-record conflict CANDIDATES, proposed by code (T-094, R-CO-7; LLM_VS_CODE row 11). Deterministic: no model, no app.llm import.
The model no longer searches the records for conflicts (open generation varied run to run). Code finds the pairs worth asking about, in a
fixed order, and a judge (J3, judge_conflict_v3) only classifies each pair: conflict or benign.

Rules:
- plan_vs_outcome: a stated plan of care (a visit count, or frequency x duration which code multiplies out) and a LATER record that shows the
  course ending early (missed appointments, no-show, discontinued). Arithmetic is code's: "2x/week for 6 weeks" is 12 visits, so it agrees
  with "Plan of care: 12 visits" and is never a conflict. Plans that agree make one plan (the explicit visit count is quoted).
- history_denial: a sentence that denies prior problems ("denies prior neck problems") and a sentence in ANOTHER record that the phrase list
  fires on as a prior condition. One candidate per denial is judged at a time, in record order, and the first the judge confirms stands.
Every quote is a whole sentence taken from the record text, so it is verbatim by construction."""
import re
from dataclasses import dataclass

from app.backend import lexicon_scan, sentences

_WORDS = {"once": 1, "one": 1, "twice": 2, "two": 2, "three": 3, "four": 4, "five": 5}
_NUM = r"(\d{1,2}|once|twice|one|two|three|four|five)"
_COUNT = [
    re.compile(r"\b(?:plan of care|plan|treatment plan|authorized|approved|ordered|certified)\b[^.;\n]{0,30}?\b(\d{1,3})\s*(?:visits?|sessions?|treatments?)\b", re.I),
    re.compile(r"\b(\d{1,3})\s*(?:visits?|sessions?|treatments?)\s*(?:planned|authorized|approved|ordered|requested|total)\b", re.I),
]
_FREQ = re.compile(rf"\b{_NUM}\s*(?:x|times?)?\s*(?:/|per|a|each)?\s*(?:week|wk|weekly)\w*\s*(?:for|x)\s*(\d{{1,2}})\s*(?:weeks?|wks?)\b", re.I)
_FREQ2 = re.compile(r"\b(once|twice)\s+(?:a\s+|per\s+)?weekly?\s+for\s+(\d{1,2})\s*(?:weeks?|wks?)\b", re.I)
# the course ended early: non-attendance or an explicit stop. "missing 3 days of work" and a plain "discharged home" do not match.
_ENDED = re.compile(r"\b(?:missed\s+(?:\w+\s+){0,2}(?:appointments?|visits?|sessions?)|no[- ]?shows?|cancel(?:l)?ed\s+(?:\w+\s+){0,2}(?:appointments?|visits?|sessions?)"
                    r"|did\s+not\s+(?:attend|return)|failed\s+to\s+(?:attend|return)|stopped\s+attending|self[- ]discharged|discontinued|non-?complian\w*)\b", re.I)
_DENIAL = re.compile(r"\b(?:denies|denied|denying)\s+(?:any\s+)?(?:prior|previous|pre-?existing|earlier)\b|\bno\s+(?:prior|previous|pre-?existing)\s+(?:\w+\s+){0,3}"
                     r"(?:problems?|injur\w+|history|symptoms?|complaints?|pain|treatment)\b|\bno\s+history\s+of\b", re.I)
_PRIOR_CATEGORIES = ("pre_existing", "prior_surgery")


@dataclass(frozen=True)
class Quote:
    record_no: int
    text: str


def _num(s):
    return int(s) if s.isdigit() else _WORDS[s.lower()]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:02.420Z

**tool call — Bash**
````
{
 "command": "grep -n \"def dates_to_confirm\" -B3 -A25 app/backend/present.py; grep -n \"dates_to_confirm\" memory/contracts/api.md | cut -c1-250; grep -n \"def conn\\|def get_case\\|DB\\.\\(list_items\\|get_case\\|list_records\\)\" app/backend/api.py | head; grep -n \"def list_records\\|def list_events\\|def list_items\\|def get_case\\|def apply_review\\|def init\\|CREATE TABLE\" app/db/db.py app/db/schema.sql | head -30"
}
````

### User / tool · 2026-11-02T04:17:02.532Z

**tool result**
````
122-            "ready_to_export": counts["pending"] == 0 and (counts["accepted"] + counts["edited"]) > 0}
123-
124-
125:def dates_to_confirm(conn, case_id):
126-    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"]}
127-            for r in _recs_by_id(conn, case_id).values() if r["date_status"] in ("ambiguous", "missing")]
128-
129-
130-def record_view(r, raw, with_sentences=True, pages=None):
131-    block = raw[r["char_start"]:r["char_end"]]
132-    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
133-         "date_status": r["date_status"], "date_candidates": r["date_candidates"] or [], "duplicate_of": r["duplicate_of"],
134-         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
135-         "char_end": r["char_end"], "text": block}
136-    if pages:                                    # PDF source (D-031): the page where the record starts
137-        v["page"] = pdf_text.page_for(pages, r["char_start"])
138-    if with_sentences:
139-        v["sentences"] = [{"text": block[a:b], "start": r["char_start"] + a, "end": r["char_start"] + b} for a, b in sentences.stripped_spans(block)]
140-    return v
141-
142-
143-def case_view(conn, case_id, *, backend, models, demo_mode):
144-    case = DB.get_case(conn, case_id)
145-    raw = case["raw_text"]
146-    recs = list(_recs_by_id(conn, case_id).values())
147-    its = all_items(conn, case_id)
148-    ents = its["entry"]
149-    live_e = [e for e in ents if e["state"] != "rejected"]
150-    dated = sorted((e for e in live_e if e["date"] and (e["date_status"] in ("parsed", "confirmed", None))), key=lambda e: (e["date"], e["seq"] or 0))
67:  "dates_to_confirm": [],
206:  "dates_to_confirm": [],
216:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real
223:Response 200: the record with `date_status: "confirmed"`, its entry's date, the **recomputed gap flags** (a changed or new flag keeps no review status; an unchanged record pair keeps its status), the cleared `date_ambiguous` record warning, and `
229:  "dates_to_confirm": [], "warnings": [] }
477:`next_action`: `{"code": "CONFIRM_DATE", "text": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.", "target": {"record_id": "r4", "view": "dates_to_confirm"}, "options": ["accept","edit","dismiss"]}`.
525:      "next_action": {"code": "CONFIRM_DATE", "text": "...", "target": {"view": "dates_to_confirm"}} },
123:    def conn():
138:    def get_case(c, token):
139:        case = DB.get_case(c, token)
288:                flags = DB.list_items(c, cid, "flag")
295:            return {"token": cid, "name": DB.get_case(c, cid)["name"], "status": "ingested", "source": "sample" if sample else "paste",
305:    def get_case_view(token: str):
328:            if DB.get_case(c, token)["status"] == "running":
349:            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
394:                    "counts": {"entries": len(DB.list_items(c, token, "entry")), "amounts": len(DB.list_items(c, token, "amount")),
395:                               "flags": len(DB.list_items(c, token, "flag"))},
app/db/db.py:28:def init(path: str = ":memory:"):
app/db/db.py:95:def get_case(conn, case_id: str):
app/db/db.py:159:def list_items(conn, case_id: str, kind: str) -> list:
app/db/db.py:179:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
app/db/db.py:211:def list_events(conn, case_id: str, item_id: str = None) -> list:
app/db/schema.sql:4:CREATE TABLE IF NOT EXISTS cases (
app/db/schema.sql:11:CREATE TABLE IF NOT EXISTS records (
app/db/schema.sql:19:CREATE TABLE IF NOT EXISTS entries (
app/db/schema.sql:27:CREATE TABLE IF NOT EXISTS amounts (
app/db/schema.sql:36:CREATE TABLE IF NOT EXISTS flags (
app/db/schema.sql:48:CREATE TABLE IF NOT EXISTS llm_calls (
app/db/schema.sql:55:CREATE TABLE IF NOT EXISTS review_events (
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:09.511Z

**tool call — Bash**
````
{
 "command": "sed -n 36,70p app/db/schema.sql; sed -n 155,230p app/db/db.py; sed -n 1,40p app/backend/review.py; sed -n 56,115p app/backend/review.py; grep -n \"def confirm_date\" -A5 app/backend/review.py | head; grep -n \"dates_to_confirm\" app/backend/review.py; grep -n \"phrase\\|trigger\" app/backend/flag_templates.py | head"
}
````

### User / tool · 2026-11-02T04:17:09.637Z

**tool result**
````
/bin/bash: child setpgid (88279 to 88279): Operation not permitted
CREATE TABLE IF NOT EXISTS flags (
  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id),
  type TEXT CHECK (type IN ('gap','conflict','pre_existing','causation','record_warning')),
  category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),
  title TEXT, explanation TEXT, computed_json TEXT, evidence_json TEXT,
  origin TEXT CHECK (origin IN ('code','lexicon','llm','lexicon+llm')), reviewer_note TEXT,
  state TEXT, state_reasons_json TEXT,
  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
  edited_json TEXT, ladder_json TEXT, updated_at REAL,
  PRIMARY KEY (case_id, id)
);
-- Audit: one row per attempt (ADR-003.7); holds full prompts, so delete_case must cover it (ADR-006).
CREATE TABLE IF NOT EXISTS llm_calls (
  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
  role TEXT CHECK (role IN ('generator','judge')), step TEXT, backend TEXT, model TEXT,
  prompt_version TEXT, prompt_sha256 TEXT, system_text TEXT, user_text TEXT, response_raw TEXT,
  parsed_ok INTEGER, verdict TEXT, attempt INTEGER DEFAULT 1, latency_ms INTEGER, cost_usd REAL,
  tokens_in INTEGER, tokens_out INTEGER, recorded_from_json TEXT, error TEXT, created_at REAL
);
CREATE TABLE IF NOT EXISTS review_events (
  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry')),
  before_json TEXT, after_json TEXT, at REAL
);
CREATE INDEX IF NOT EXISTS ix_records_case ON records(case_id);
CREATE INDEX IF NOT EXISTS ix_entries_case ON entries(case_id);
CREATE INDEX IF NOT EXISTS ix_amounts_case ON amounts(case_id);
CREATE INDEX IF NOT EXISTS ix_flags_case ON flags(case_id);
CREATE INDEX IF NOT EXISTS ix_calls_case ON llm_calls(case_id);
CREATE INDEX IF NOT EXISTS ix_events_case ON review_events(case_id);
def get_item(conn, item_id: str, case: str = None) -> dict:
    return _decode(_find(conn, item_id, case)[1])


def list_items(conn, case_id: str, kind: str) -> list:
    table = _ITEM_TABLES[kind][0]
    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]


def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
    if locked & set(fields):
        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
    table, found = _find(conn, item_id, case)
    bad = set(fields) - _cols(conn, table)
    if bad:
        raise ValueError(f"unknown {table} fields {sorted(bad)}")
    fields["updated_at"] = now
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])


def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
    if action not in ACTIONS:
        raise ValueError(f"invalid review action {action!r}")
    table, row = _find(conn, item_id, case)
    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
    status = ACTIONS[action] or row["review_status"]
    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
    if action == "edit" and not new_edited:
        raise ValueError("edit requires a non-empty edited payload")
    after = {"review_status": status, "edited": new_edited}
    conn.execute("BEGIN")
    try:
        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
                     (status, _enc(new_edited), now, item_id, row["case_id"]))
        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return get_item(conn, item_id, row["case_id"])


def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
    if status not in REVIEW_STATUSES:
        raise ValueError(f"invalid review_status {status!r}")
    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
    apply_review(conn, item_id, action, edited=edited, now=now, case=case)


def list_events(conn, case_id: str, item_id: str = None) -> list:
    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
    if item_id:
        q, a = q + " AND item_id=?", a + [item_id]
    return [_decode(r) for r in conn.execute(q + " ORDER BY at, rowid", a)]


def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
    """One row per attempt. `prompt` is the user text; prompt_sha256 covers system+user unless supplied."""
    cid = fields.pop("id", None) or _tok("c")
    row = {"id": cid, "case_id": case_id, "system_text": system, "user_text": prompt, "response_raw": response,
           "prompt_sha256": sha256((system or "") + "\n" + prompt), "created_at": now, **fields}
    _insert(conn, "llm_calls", row)
    return cid


def get_llm_call(conn, call_id: str):
    r = conn.execute("SELECT * FROM llm_calls WHERE id=?", (call_id,)).fetchone()
    return _decode(r) if r else None

"""Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).

Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
Edit order: (1) structure, else 422 invalid_edit; (2) code token check; (3) judge 1 re-run. A token/judge objection saves nothing
and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
that cannot answer never blocks: the edit is saved as needs_review with JUDGE_UNAVAILABLE.
"""
import time

from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, store
from app.db import db as DB

ACTIONS = ("accept", "dismiss", "reset", "edit")
_NUMERIC_TOKEN = __import__("re").compile(r"\d|^(?:january|february|march|april|may|june|july|august|september|october|november|december)$", __import__("re").IGNORECASE)
_KIND = {"e": "entry", "a": "amount", "f": "flag"}


class ReviewError(Exception):
    def __init__(self, status: int, code: str, detail: dict = None, message: str = ""):
        super().__init__(code)
        self.status, self.code, self.detail, self.message = status, code, detail or {}, message or code.replace("_", " ")


def _now(now):
    return now() if callable(now) else (time.time() if now is None else now)


def _item(conn, case_id, item_id):
    try:
        row = DB.get_item(conn, item_id, case_id)
    except KeyError:
        raise ReviewError(404, "not_found", message="No such item.") from None
    if row["case_id"] != case_id:
        raise ReviewError(404, "not_found", message="No such item.")
    return _KIND[item_id[0]], row


def _bad(msg, **detail):
    return ReviewError(422, "invalid_edit", detail, msg)

                       "cannot be accepted into the letter.")


def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
        raise _bad("That action is not allowed.")
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
        raise _date_unconfirmed_error()
    warnings = []
    if action in ("accept", "dismiss", "reset"):
        DB.apply_review(conn, item_id, action, now=t, case=case_id)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}


def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, body):
    """Code token/qualifier checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
    Raises 409 needs_confirm unless body['confirm_warnings']; returns the pieces both callers store."""
    code_reasons = []
    toks = grounding.new_tokens(new_sum, new_exc, label, date_iso)
    numeric = [t for t in toks if _NUMERIC_TOKEN.search(t)]
    if numeric:    # D-034: a number, date or $ figure that is not in the quote is never saved, with or without confirm_warnings
        raise _bad("The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(numeric) + ". Remove it or change the quote.",
                   tokens=numeric, reason="SUMMARY_NUMBER_NOT_IN_EXCERPT")
    blocking = []
    if toks:
        code_reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
        blocking.append({"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "\u201c" + "\u201d, \u201c".join(toks) + "\u201d is not in the quote.", "item_id": item_id})
    if grounding.dropped_qualifiers(new_sum, new_exc):
        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
    if span is None:
        code_reasons.append("HIGHLIGHT_NOT_FOUND")
    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
    if call is not None:
        verdict, call_id, judge_code, judge_error = judge_guard.guarded(judges.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id)   # T-073
        ladder_verdict = judges.to_ladder("j1", verdict)
    if ladder_verdict in ("partially", "unsupported"):
        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
        blocking.append({"code": code, "message": "The second check could not fully support the summary from the quote.", "item_id": item_id})
    if blocking and not bool(body.get("confirm_warnings")):
        raise ReviewError(409, "needs_confirm", {"warnings": blocking}, "This edit adds a number or fact that is not in the quote.")
    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed")})
    return {"toks": toks, "code_reasons": code_reasons, "blocking": blocking, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
            "judge_error": judge_error,
            "state": state, "reasons": reasons}


# ---------------------------------------------------------------- edit
def _edit(conn, case_id, kind, item, body, call, t):
172:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
173-    t = _now(now)
174-    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
175-    if row is None:
176-        raise ReviewError(404, "not_found", message="No such record.")
177-    rec = DB._decode(row)
201:            "removed_flag_ids": removed, "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:11.918Z

**tool call — Bash**
````
{
 "command": "grep -n \"computed\\|\\\"phrase\\|evidence\" app/backend/flags.py | head -30; grep -n \"def \\|class \" app/backend/lexicon_scan.py | head; grep -n \"def item_view\" -A30 app/backend/present.py | head -60"
}
````

### User / tool · 2026-11-02T04:17:12.029Z

**tool result**
````
53:         "evidence": [{"record_no": record["n"], "text": excerpt,
135:            # D-030: evidence is the verbatim phrase span the model returned (still grounded by ground()); the lexicon sentence is
140:            lx["evidence"] = [{"record_no": record["n"], "text": lx["excerpt"],
169:        f["ladder"]["code_checks"] = {"excerpt_verbatim": "GROUNDING_EXCERPT_NOT_VERBATIM" not in fail, "highlight_found": f["evidence"][0]["start"] is not None}
178:                            quote=hits[0]["phrase"] if hits else None)
181:            "reasons": ["INJECTION_SUSPECTED"], "why": why.why("INJECTION_SUSPECTED"), "excerpt": hits[0]["phrase"] if hits else "",
183:            "evidence": [{"record_no": record["n"], "text": h["phrase"], "start": base + h["start"], "end": base + h["end"]} for h in hits],
220:            "evidence": [], "pipeline_warning": "CONFLICT_PASS_INCOMPLETE",
235:         "evidence": [{"record_no": r["n"], "text": q, "start": (_base(r) + s[0]) if s else None, "end": (_base(r) + s[1]) if s else None}
14:def _sentence_bounds(text, start, end):
22:def _norm(tokens):
26:def _strip_pseudo(s, pseudo):
32:def _has(s, phrases):
36:def _cut_at_terminator(tokens, terms):
45:def negated(text, start, end, neg):
65:    def seg_negates(seg):
90:def _entries() -> tuple:
98:def _hit_year(m):
109:def _clause_after(text, end):
87:def item_view(conn, case_id, item_id):
88-    row = DB.get_item(conn, item_id, case_id)
89-    kind = _ID_KIND[item_id[0]]
90-    v = _VIEW[kind](row, _recs_by_id(conn, case_id))
91-    v["kind"] = kind
92-    return v
93-
94-
95-def all_items(conn, case_id):
96-    recs = _recs_by_id(conn, case_id)
97-    return {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
98-
99-
100-def totals_view(conn, case_id):
101-    am = [a for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
102-    t = T.totals([{"id": a["id"], "cents": a["value_cents"], "cls": a["kind"], "raw": a["text"], "review_status": a["review_status"]} for a in am])
103-    ch = [a for a in am if a["kind"] == "charge" and a["value_cents"] is not None]
104-    cnt = lambda sts: sum(1 for a in ch if a["review_status"] in sts)   # noqa: E731
105-    return {"accepted": {"cents": t["accepted_cents"], "count": cnt(("accepted", "edited")), "label": "Accepted charges"},
106-            "pending": {"cents": t["detected_pending_cents"], "count": cnt(("pending",)), "label": "Pending review"},
107-            "detected_not_a_total": {"cents": sum(a["value_cents"] for a in ch if a["review_status"] != "dismissed"),
108-                                     "count": sum(1 for a in ch if a["review_status"] != "dismissed"), "label": "Detected (not a total)"},
109-            "not_totaled": [{"id": a["id"], "kind": a["kind"], "text": a["text"]} for a in am
110-                            if a["kind"] != "charge" and a["review_status"] != "dismissed" and a["kind"] != "damages"]}
111-
112-
113-def review_view(conn, case_id):
114-    items = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, case_id, k)]
115-    live = [(k, r) for k, r in items if r["state"] != "rejected"]
116-    counts = {s: sum(1 for _, r in live if r["review_status"] == s) for s in ("pending", "accepted", "edited", "dismissed")}
117-    counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:22.224Z

**tool call — Bash**
````
{
 "command": "grep -n \"ZLAYT_MODE\\|local_mode\\|LOCAL\" app/backend/api.py | head; sed -n 1,50p tests/unit/_golden.py; sed -n 1,40p tests/unit/test_date_unconfirmed.py; grep -n \"def run_stages\\|def ingest_case\\|def run(\" app/backend/pipeline.py; grep -n \"def make_app\\|def create_app\\|^def \" app/backend/api.py | head"
}
````

### User / tool · 2026-11-02T04:17:22.331Z

**tool result**
````
77:def local_mode() -> bool:
78:    return os.environ.get("ZLAYT_MODE") == "local"
99:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
105:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
106:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
177:            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
218:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
228:        if not local_mode():
238:            if not local_mode():
527:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
"""Helpers: load golden records/expected files from evals/golden (the only test data; synthetic)."""
import json, pathlib, re
G = pathlib.Path(__file__).resolve().parents[2] / "evals" / "golden"

def case_names():
    return sorted(p.name[:-len(".expected.json")] for p in G.glob("*.expected.json"))

def expected(case):
    return json.loads((G / f"{case}.expected.json").read_text())

def raw(case):
    return (G / f"{case}.txt").read_text()

def records(case):
    """[{n, date_raw, source, excerpt}] parsed from the golden paste format."""
    out = []
    for m in re.finditer(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n', raw(case)):
        out.append(dict(n=int(m.group(1)), date_raw=m.group(2), source=m.group(3), excerpt=m.group(4)))
    return out

def record(case, n):
    return next(r for r in records(case) if r["n"] == n)

def export_blocks():
    t = (G / "sample.export.expected.txt").read_text()
    letter, notes = t.split("=== INTERNAL_NOTES_TEXT")
    return letter.split("\n", 1)[1], notes.split("\n", 1)[1]
"""D-041 (T-076): an entry with no confirmed date cannot be accepted (single, edit, batch) until confirm_date; the letter never says 'date not stated'."""
import pytest
from fastapi.testclient import TestClient
from app.backend import export as X
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.test_api_routes import run_case


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "x.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def undated_case(c):
    t = run_case(c, G.raw("case_01_date_formats"))
    g = c.get(f"/api/cases/{t}").json()
    rec = [r for r in g["records"] if r["date_status"] == "ambiguous"][0]
    und = [e for e in g["undated_entries"] if rec["id"] in e["record_ids"]]
    assert und, "case_01 must have an undated entry for the ambiguous record"
    return t, g, rec, und[0]


def snapshot(db, t):
    conn = DB.connect(db)
    out = {k: [(i["id"], i["review_status"]) for i in DB.list_items(conn, t, k)] for k in ("entry", "amount", "flag")}
    n = len(DB.list_events(conn, t))
    conn.close()
    return out, n


def test_single_accept_and_edit_on_undated_entry_is_422_and_changes_nothing(env):
    db, c = env
    t, g, rec, e = undated_case(c)
    before = snapshot(db, t)
209:def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
52:def digest(text: str) -> str:
56:def recorded_hashes() -> set:
60:def library_cases() -> list:
77:def local_mode() -> bool:
81:def is_loopback_peer(request) -> bool:
91:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:24.562Z

Now write the date convention module and test first.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:46.238Z

**tool call — Bash**
````
{
 "command": "cat > app/backend/date_convention.py <<'EOF'\n\"\"\"Date-convention SUGGESTION for ambiguous numeric dates (T-088, D-042; code only, LLM_VS_CODE row 2). Never applied by itself.\n\nAn ambiguous record date such as 04/05/2026 has two code-proposed readings (MM/DD and DD/MM). This module looks at the OTHER numeric\ndates in the same packet whose order is certain (one number above 12: 03/14/2026 is month first, 14/03/2026 is day first) and, when they\nall agree, suggests that order with the reason stated in plain words and the dates it rests on. Mixed evidence or none: no suggestion.\nThe suggestion is a hint the UI pre-selects; the paralegal still confirms once through confirm_date (D-041), and confirm_date still only\naccepts one of the code candidates. Nothing here writes to the database or changes a pipeline result.\"\"\"\nimport re\n\nfrom app.backend import dates\n\n_NUM_DATE = re.compile(r\"(?<![\\d/.\\-])(\\d{1,2})([/.\\-])(\\d{1,2})\\2(\\d{4}|\\d{2})(?![\\d/.\\-]\\d)(?!\\d)\")\nMAX_EVIDENCE = 2\n_LABEL = {\"MDY\": \"MM/DD\", \"DMY\": \"DD/MM\"}\n\n\ndef _order(a: int, b: int):\n    \"\"\"MDY / DMY when the numbers prove the order, else None (both <= 12, or neither a valid month).\"\"\"\n    if a > 12 and 1 <= b <= 12:\n        return \"DMY\"\n    if b > 12 and 1 <= a <= 12:\n        return \"MDY\"\n    return None\n\n\ndef _evidence(records, raw_text, skip_id):\n    \"\"\"Unambiguous numeric dates in the packet, in record order: [{record_id, raw, order}]. Reads each record's date label and its text.\"\"\"\n    out, seen = [], set()\n    for r in records:\n        if r[\"id\"] == skip_id:\n            continue\n        block = raw_text[r[\"char_start\"]:r[\"char_end\"]]\n        for m in _NUM_DATE.finditer(block):\n            order = _order(int(m[1]), int(m[3]))\n            key = (r[\"id\"], m[0])\n            if order and key not in seen:\n                seen.add(key)\n                out.append({\"record_id\": r[\"id\"], \"raw\": m[0], \"order\": order})\n    return out\n\n\ndef _example(ev):\n    return f\"({ev['raw']})\"\n\n\ndef suggest(rec: dict, records: list, raw_text: str):\n    \"\"\"Suggestion for one ambiguous record, or None. `rec` and `records` are record rows (id, date_raw, date_status, date_candidates,\n    char_start, char_end). Returns {convention, label, iso, reason, evidence[]}; `iso` is None when the year is also ambiguous.\"\"\"\n    if rec.get(\"date_status\") != \"ambiguous\":\n        return None\n    m = _NUM_DATE.fullmatch(\" \".join(str(rec.get(\"date_raw\") or \"\").split()))\n    if not m or _order(int(m[1]), int(m[3])) is not None:\n        return None\n    ev = _evidence(records, raw_text, rec[\"id\"])\n    orders = {e[\"order\"] for e in ev}\n    if len(orders) != 1:\n        return None                      # no evidence, or the packet mixes both orders: say nothing rather than guess\n    order = next(iter(orders))\n    a, b = int(m[1]), int(m[3])\n    mo, d = (a, b) if order == \"MDY\" else (b, a)\n    cands = [c for c in rec.get(\"date_candidates\") or [] if int(c[5:7]) == mo and int(c[8:10]) == d]\n    iso = cands[0] if len(cands) == 1 else None\n    shown = ev[:MAX_EVIDENCE]\n    n = len(ev)\n    first = \"month first\" if order == \"MDY\" else \"day first\"\n    reason = (f\"Other dates in this record use {first} {_example(shown[0])}\" if n == 1 else\n              f\"{n} other dates in this record use {first} \" + \" and \".join(_example(e) for e in shown))\n    return {\"convention\": order, \"label\": _LABEL[order], \"iso\": iso, \"reason\": reason,\n            \"evidence\": [{\"record_id\": e[\"record_id\"], \"raw\": e[\"raw\"]} for e in shown], \"evidence_count\": n, \"auto_applied\": False}\nEOF\ncat > tests/unit/test_date_convention.py <<'EOF'\n\"\"\"T-088: date-convention suggestion. Code only, never auto-applied, still one confirm (D-041/D-042).\"\"\"\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import date_convention as DC, present\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit.test_api_routes import run_case\nfrom tests.unit.test_date_unconfirmed import snapshot\n\n\ndef packet(*dates_text):\n    \"\"\"records built from (date_raw, extra text) pairs; returns (rows, raw).\"\"\"\n    raw, rows, pos = \"\", [], 0\n    for i, (d, extra) in enumerate(dates_text, 1):\n        block = f\"Date: {d}\\nNote: {extra}\\n\"\n        p = dates.parse_date(d)\n        rows.append({\"id\": f\"r{i}\", \"date_raw\": d, \"date_status\": p[\"status\"], \"date_candidates\": p[\"candidates\"],\n                     \"char_start\": pos, \"char_end\": pos + len(block)})\n        raw, pos = raw + block, pos + len(block)\n    return rows, raw\n\n\nfrom app.backend import dates   # noqa: E402\n\n\ndef test_month_first_evidence_suggests_mm_dd_with_reason():\n    rows, raw = packet((\"03/14/2026\", \"seen\"), (\"04/05/2026\", \"seen again\"))\n    s = DC.suggest(rows[1], rows, raw)\n    assert s[\"convention\"] == \"MDY\" and s[\"label\"] == \"MM/DD\" and s[\"iso\"] == \"2026-04-05\"\n    assert s[\"reason\"] == \"Other dates in this record use month first (03/14/2026)\"\n    assert s[\"evidence\"] == [{\"record_id\": \"r1\", \"raw\": \"03/14/2026\"}] and s[\"auto_applied\"] is False\n\n\ndef test_day_first_evidence_suggests_dd_mm():\n    rows, raw = packet((\"14/03/2026\", \"x\"), (\"04/05/2026\", \"y\"))\n    s = DC.suggest(rows[1], rows, raw)\n    assert s[\"convention\"] == \"DMY\" and s[\"iso\"] == \"2026-05-04\" and \"day first (14/03/2026)\" in s[\"reason\"]\n\n\ndef test_evidence_inside_record_text_counts_and_is_listed_up_to_two():\n    rows, raw = packet((\"04/05/2026\", \"follow up on 06/25/2026 and 07/30/2026 and 08/31/2026\"))\n    s = DC.suggest(rows[0], rows, raw)\n    assert s[\"convention\"] == \"MDY\" and s[\"evidence_count\"] == 3 and len(s[\"evidence\"]) == 2\n    assert s[\"reason\"].startswith(\"3 other dates in this record use month first (06/25/2026) and (07/30/2026)\")\n\n\ndef test_no_suggestion_without_evidence_or_with_mixed_evidence():\n    rows, raw = packet((\"04/05/2026\", \"alone\"), (\"06/07/2026\", \"also ambiguous\"))\n    assert DC.suggest(rows[0], rows, raw) is None\n    rows, raw = packet((\"03/14/2026\", \"a\"), (\"25/03/2026\", \"b\"), (\"04/05/2026\", \"c\"))\n    assert DC.suggest(rows[2], rows, raw) is None\n\n\ndef test_not_ambiguous_or_iso_dates_never_get_or_give_evidence():\n    rows, raw = packet((\"2026-03-14\", \"iso is not numeric-order evidence\"), (\"04/05/2026\", \"x\"))\n    assert DC.suggest(rows[1], rows, raw) is None\n    assert DC.suggest(rows[0], rows, raw) is None        # a parsed record has no suggestion\n\n\ndef test_two_digit_year_ambiguity_keeps_convention_but_no_iso():\n    rows, raw = packet((\"03/14/2026\", \"x\"), (\"04/05/98\", \"y\"))\n    s = DC.suggest(rows[1], rows, raw)\n    assert s[\"convention\"] == \"MDY\" and s[\"iso\"] is None or s[\"iso\"] in rows[1][\"date_candidates\"]\n\n\ndef test_suggestion_never_writes_and_is_not_a_confirmation(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    db = str(tmp_path / \"x.sqlite\")\n    c = TestClient(create_app(db, static_dir=str(tmp_path)))\n    t = run_case(c, G.raw(\"case_01_date_formats\"))\n    before = snapshot(db, t)\n    g = c.get(f\"/api/cases/{t}\").json()\n    amb = [r for r in g[\"records\"] if r[\"date_status\"] == \"ambiguous\"]\n    assert amb\n    for item in g[\"dates_to_confirm\"]:\n        s = item.get(\"suggestion\")\n        if s:\n            assert s[\"auto_applied\"] is False and item[\"candidates\"] and (s[\"iso\"] is None or s[\"iso\"] in item[\"candidates\"])\n    assert all(r[\"date_status\"] == \"ambiguous\" for r in amb)        # nothing was confirmed by the suggestion\n    assert snapshot(db, t) == before\n    conn = DB.connect(db)\n    assert not [e for e in DB.list_events(conn, t) if e[\"action\"] == \"confirm_date\"]\n    conn.close()\n\n\ndef test_dates_to_confirm_carries_suggestion_and_confirm_still_required(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    db = str(tmp_path / \"y.sqlite\")\n    c = TestClient(create_app(db, static_dir=str(tmp_path)))\n    text = (\"=== Record 1 ===\\nDate: 03/14/2026\\nSource: Clinic\\nExcerpt: \\\"Patient seen for neck pain.\\\"\\n\\n\"\n            \"=== Record 2 ===\\nDate: 04/05/2026\\nSource: Clinic\\nExcerpt: \\\"Patient returned for neck pain follow up.\\\"\\n\")\n    t = run_case(c, text)\n    g = c.get(f\"/api/cases/{t}\").json()\n    item = [d for d in g[\"dates_to_confirm\"] if d[\"raw\"] == \"04/05/2026\"][0]\n    assert item[\"suggestion\"][\"label\"] == \"MM/DD\" and item[\"suggestion\"][\"iso\"] == \"2026-04-05\"\n    assert item[\"suggestion\"][\"reason\"] == \"Other dates in this record use month first (03/14/2026)\"\n    assert item[\"status\"] == \"ambiguous\"                     # still unconfirmed\n    r = c.post(f\"/api/cases/{t}/records/{item['record_id']}/confirm_date\", json={\"date\": \"2026-04-05\"})\n    assert r.status_code == 200 and r.json()[\"dates_to_confirm\"] == []\n    assert c.post(f\"/api/cases/{t}/records/{item['record_id']}/confirm_date\", json={\"date\": \"2026-06-06\"}).status_code in (422,)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_date_convention.py 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T04:17:47.468Z

**tool result**
````
                "=== Record 2 ===\nDate: 04/05/2026\nSource: Clinic\nExcerpt: \"Patient returned for neck pain follow up.\"\n")
>       t = run_case(c, text)
            ^^^^^^^^^^^^^^^^^

tests/unit/test_date_convention.py:96: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

c = <starlette.testclient.TestClient object at 0x10c839700>
text = '=== Record 1 ===\nDate: 03/14/2026\nSource: Clinic\nExcerpt: "Patient seen for neck pain."\n\n=== Record 2 ===\nDate: 04/05/2026\nSource: Clinic\nExcerpt: "Patient returned for neck pain follow up."\n'

    def run_case(c, text=None):
>       tok = c.post("/api/cases", json={"text": text} if text else {"sample": True}).json()["token"]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_api_routes.py:35: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_date_convention.py::test_evidence_inside_record_text_counts_and_is_listed_up_to_two
FAILED tests/unit/test_date_convention.py::test_dates_to_confirm_carries_suggestion_and_confirm_still_required
2 failed, 6 passed in 0.83s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:50.490Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_date_convention.py -k inside_record 2>&1 | grep -E \"^E\" | head; grep -n \"^Date:\" evals/golden/case_01_date_formats.txt; grep -n \"ZLAYT_MODE\\|ingest_case\" tests/unit/test_date_unconfirmed.py tests/unit/test_api_routes.py | head"
}
````

### User / tool · 2026-11-02T04:17:51.178Z

**tool result**
````
E       TypeError: 'NoneType' object is not subscriptable
4:Date: 2026-02-03
9:Date: 02/17/2026
14:Date: Feb 24, 2026
19:Date: 3 March 2026
24:Date: March 10th, 2026
29:Date: 03-17-26
34:Date: 3/25/26
39:Date: 04/05/2026
tests/unit/test_api_routes.py:215:    def ingest_case(*a, **k): raise RuntimeError("SECRET RECORD TEXT in a traceback")
tests/unit/test_api_routes.py:263:    """T-040 AC (T-051 privacy): public/demo audit has no prompt, response, record or edit text; ZLAYT_MODE=local adds them."""
tests/unit/test_api_routes.py:268:    monkeypatch.delenv("ZLAYT_MODE", raising=False)
tests/unit/test_api_routes.py:273:    monkeypatch.setenv("ZLAYT_MODE", "local")
tests/unit/test_api_routes.py:281:    monkeypatch.delenv("ZLAYT_MODE", raising=False)
tests/unit/test_api_routes.py:285:    monkeypatch.setenv("ZLAYT_MODE", "local")
tests/unit/test_api_routes.py:298:    monkeypatch.setenv("ZLAYT_MODE", "local")
tests/unit/test_api_routes.py:314:    monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.setenv("HOST", host)
tests/unit/test_api_routes.py:320:    monkeypatch.delenv("ZLAYT_MODE")
tests/unit/test_api_routes.py:332:    monkeypatch.delenv("ZLAYT_MODE", raising=False)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:01.185Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='app/backend/date_convention.py'\ns=open(p).read()\ns=s.replace('def _evidence(records, raw_text, skip_id):','def _evidence(records, raw_text):').replace('''        if r[\"id\"] == skip_id:\n            continue\n''','').replace('_evidence(records, raw_text, rec[\"id\"])','_evidence(records, raw_text)')\ns=s.replace(\"Never applied by itself.\",\"Never applied by itself.\")\nopen(p,'w').write(s)\np='tests/unit/test_date_convention.py'\ns=open(p).read()\ni=s.index(\"def test_dates_to_confirm_carries\")\ns=s[:i]+'''def test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    db = str(tmp_path / \"y.sqlite\")\n    c = TestClient(create_app(db, static_dir=str(tmp_path)))\n    t = run_case(c, G.raw(\"case_01_date_formats\"))\n    g = c.get(f\"/api/cases/{t}\").json()\n    item = [d for d in g[\"dates_to_confirm\"] if d[\"raw\"] == \"04/05/2026\"][0]\n    s = item[\"suggestion\"]\n    assert s[\"label\"] == \"MM/DD\" and s[\"iso\"] == \"2026-04-05\" and s[\"auto_applied\"] is False\n    assert s[\"reason\"].startswith(\"3 other dates in this record use month first (02/17/2026)\")\n    assert item[\"status\"] == \"ambiguous\"                     # still unconfirmed until the paralegal confirms\n    assert c.post(f\"/api/cases/{t}/records/{item['record_id']}/confirm_date\", json={\"date\": \"2026-06-06\"}).status_code == 422\n    r = c.post(f\"/api/cases/{t}/records/{item['record_id']}/confirm_date\", json={\"date\": \"2026-04-05\"})\n    assert r.status_code == 200 and not [d for d in r.json()[\"dates_to_confirm\"] if d[\"raw\"] == \"04/05/2026\"]\n'''\nopen(p,'w').write(s)\nEOF\ngrep -n \"_recs_by_id\" app/backend/present.py | head -3; git diff --stat app/backend/present.py"
}
````

### User / tool · 2026-11-02T04:18:01.333Z

**tool result**
````
83:def _recs_by_id(conn, case_id):
90:    v = _VIEW[kind](row, _recs_by_id(conn, case_id))
96:    recs = _recs_by_id(conn, case_id)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:02.314Z

Now the minimal edit to present.py (re-read right before).

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:04.472Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/present.py'\ns=open(p).read()\nold='''def dates_to_confirm(conn, case_id):\n    return [{\"record_id\": r[\"id\"], \"raw\": r[\"date_raw\"], \"candidates\": r[\"date_candidates\"] or [], \"status\": r[\"date_status\"]}\n            for r in _recs_by_id(conn, case_id).values() if r[\"date_status\"] in (\"ambiguous\", \"missing\")]\n'''\nnew='''def dates_to_confirm(conn, case_id):\n    recs = list(_recs_by_id(conn, case_id).values())\n    raw = DB.get_case(conn, case_id)[\"raw_text\"]\n    return [{\"record_id\": r[\"id\"], \"raw\": r[\"date_raw\"], \"candidates\": r[\"date_candidates\"] or [], \"status\": r[\"date_status\"],\n             \"suggestion\": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)\n            for r in recs if r[\"date_status\"] in (\"ambiguous\", \"missing\")]\n'''\nassert old in s\ns=s.replace(old,new)\nopen(p,'w').write(s)\nEOF\nsed -n 1,20p app/backend/present.py | grep -n import"
}
````

### User / tool · 2026-11-02T04:18:04.619Z

**tool result**
````
2:import json
4:from app.backend import confidence, grounding, pdf_text, sentences, store, totals as T, why
5:from app.db import db as DB
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:06.889Z

**tool call — Bash**
````
{
 "command": "sed -i '4s/from app.backend import confidence, grounding/from app.backend import confidence, date_convention, grounding/' app/backend/present.py && .venv/bin/python -m pytest -q tests/unit/test_date_convention.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:18:06.978Z

**tool result (error)**
````
Exit code 1
sed: 1: "app/backend/present.py
": command a expects \ followed by text
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:08.805Z

**tool call — Bash**
````
{
 "command": "sed -i '' '4s/from app.backend import confidence, grounding/from app.backend import confidence, date_convention, grounding/' app/backend/present.py && sed -n 4p app/backend/present.py && .venv/bin/python -m pytest -q tests/unit/test_date_convention.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:18:10.343Z

**tool result**
````
from app.backend import confidence, date_convention, grounding, pdf_text, sentences, store, totals as T, why
        c = TestClient(create_app(db, static_dir=str(tmp_path)))
        t = run_case(c, G.raw("case_01_date_formats"))
        g = c.get(f"/api/cases/{t}").json()
        item = [d for d in g["dates_to_confirm"] if d["raw"] == "04/05/2026"][0]
        s = item["suggestion"]
        assert s["label"] == "MM/DD" and s["iso"] == "2026-04-05" and s["auto_applied"] is False
>       assert s["reason"].startswith("3 other dates in this record use month first (02/17/2026)")
E       AssertionError: assert False
E        +  where False = <built-in method startswith of str object at 0x10a6d3a30>('3 other dates in this record use month first (02/17/2026)')
E        +    where <built-in method startswith of str object at 0x10a6d3a30> = '4 other dates in this record use month first (02/17/2026) and (03-17-26)'.startswith

tests/unit/test_date_convention.py:99: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required
1 failed, 7 passed in 1.12s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:13.754Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_date_convention.py'\ns=open(p).read()\ns=s.replace('''assert s[\"reason\"].startswith(\"3 other dates in this record use month first (02/17/2026)\")''','''assert s[\"evidence_count\"] == 4 and s[\"reason\"] == \"4 other dates in this record use month first (02/17/2026) and (03-17-26)\"''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_date_convention.py tests/unit/test_dates.py tests/unit/test_api_routes.py tests/unit/test_date_unconfirmed.py 2>&1 | tail -4"
}
````

### User / tool · 2026-11-02T04:18:22.100Z

**tool result**
````
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c94fea499870c step=j3 attempt=1 prompt_hash=7dc98319034d0b969d14e5061516b6bfd8ab6c637c2a8839d8eed927ea884621
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted
1 failed, 66 passed in 7.81s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:23.986Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_api_routes.py -k export_equals_golden 2>&1 | grep -E \"^E\" | head -5"
}
````

### User / tool · 2026-11-02T04:18:25.261Z

**tool result**
````
E       KeyError: 'letter_text'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:28.625Z

**tool call — Bash**
````
{
 "command": "grep -n \"\\\"type\\\": \\\"\" app/backend/flags.py | head; grep -n \"category\" app/backend/lexicon.py | head -5; python3 - <<'EOF'\nimport sqlite3,glob\nEOF\n.venv/bin/python - <<'EOF'\nfrom fastapi.testclient import TestClient\nimport os,tempfile\nos.environ[\"LLM_BACKEND\"]=\"fixture\"\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom tests.unit.test_api_routes import run_case\nd=tempfile.mkdtemp(); db=d+\"/x.sqlite\"\nc=TestClient(create_app(db,static_dir=d)); t=run_case(c)\nconn=DB.connect(db)\nfor f in DB.list_items(conn,t,\"flag\"): print(f[\"id\"],f[\"type\"],f[\"category\"],f[\"origin\"],f[\"state\"],str(f[\"evidence\"])[:150])\nEOF"
}
````

### User / tool · 2026-11-02T04:18:29.476Z

**tool result**
````
179:    return {"type": "record_warning", "category": "injection_suspected", "record_no": record["n"], "record_id": record.get("id", f"r{record['n']}"),
222:    f = {"id": fid, "type": "conflict", "category": c["category"], "excerpt": qa, "excerpt_b": qb, "origin": "code", "title": title, "explanation": expl,
17:    """Entries of a `code_lists` category as [{id, regex}] (compiled IGNORECASE)."""
llm call failed call_id=c68827f8aa6d6 step=j3 attempt=1 prompt_hash=7dc98319034d0b969d14e5061516b6bfd8ab6c637c2a8839d8eed927ea884621
f_gap_r6_r7 gap gap_over_30 code verified [{'end': 1123, 'field': 'date', 'record_no': 6, 'start': 1107, 'text': 'Date: 2026-03-06'}, {'end': 1151, 'field': 'source', 'record_no': 6, 'start': 
f_accident_date_after_treatment_1_2_7 conflict accident_date_after_treatment code verified [{'end': 1451, 'field': 'excerpt', 'record_no': 7, 'start': 1407, 'text': 'Date of accident per intake form: 2026-01-19'}, {'end': 139, 'field': 'date
f_cx1 conflict treatment_plan_vs_actual code needs_review [{'end': 928, 'record_no': 4, 'start': 904, 'text': 'Plan of care: 12 visits.'}, {'end': 1211, 'record_no': 6, 'start': 1162, 'text': 'Discharged from
f_r3_1 pre_existing pre_existing lexicon+llm verified [{'end': 772, 'record_no': 3, 'start': 724, 'text': 'Patient reports low back pain in 2023, resolved.'}]
f_r8_1 pre_existing degenerative_language lexicon+llm verified [{'end': 1660, 'record_no': 8, 'start': 1595, 'text': 'Findings may represent degenerative change; correlate clinically.'}]
f_r6_1 causation missed_care lexicon+llm verified [{'end': 1211, 'record_no': 6, 'start': 1162, 'text': 'Discharged from PT after two missed appointments.'}]
f_r7_1 causation accident_date_provenance lexicon+llm verified [{'end': 1452, 'record_no': 7, 'start': 1407, 'text': 'Date of accident per intake form: 2026-01-19.'}]
f_r7_2 causation new_onset lexicon+llm verified [{'end': 1382, 'record_no': 7, 'start': 1319, 'text': 'New onset pain radiating to right arm with numbness in fingers.'}]
f_r8_2 causation speculative_language lexicon+llm verified [{'end': 1660, 'record_no': 8, 'start': 1595, 'text': 'Findings may represent degenerative change; correlate clinically.'}]
f_r9_1 causation patient_report lexicon+llm verified [{'end': 1876, 'record_no': 9, 'start': 1818, 'text': 'Patient states symptoms began after the January collision.'}]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:32.613Z

**tool call — Bash**
````
{
 "command": "sed -n 86,200p app/backend/lexicon_scan.py; sed -n 1,40p app/backend/lexicon.py"
}
````

### User / tool · 2026-11-02T04:18:32.709Z

**tool result**
````
    return _has(_strip_pseudo(_norm(clause[:w]), pseudo), neg["post_cues"])


@functools.lru_cache(maxsize=1)
def _entries() -> tuple:
    out = []
    for e in lexicon.load()["entries"]:
        sup = re.compile(e["suppress_if_followed_by"], re.I) if e.get("suppress_if_followed_by") else None
        out.append((e, re.compile(e["pattern"], re.I | re.M), sup))
    return tuple(out)


def _hit_year(m):
    for g in ("year", "year2"):
        try:
            if m.group(g):
                return int(m.group(g))
        except IndexError:
            pass
    y = YEAR.search(m.group(0))
    return int(y.group(0)) if y else None


def _clause_after(text, end):
    m = re.search(r"[,;.\n]", text[end:])
    return text[end:end + m.start()] if m else text[end:]


def scan(text: str, accident_year=None) -> list:
    """Firing hits as [{id, flag_type, category, strength, start, end, text, unit_start, unit_end}], file order. Unknown accident_year keeps
    year-filtered hits (the item is reviewed anyway)."""
    neg = lexicon.load()["negation"]
    units = sentences.stripped_spans(text)
    out = []
    for e, rx, sup in _entries():
        if e["strength"] not in RAISES:
            continue
        for m in rx.finditer(text):
            if e.get("negatable") and negated(text, m.start(), m.end(), neg):
                continue
            if e.get("year_filter") and accident_year:
                y = _hit_year(m)
                if y and y >= accident_year:
                    continue
            if sup and sup.search(_clause_after(text, m.end())):
                continue
            u = next(((a, b) for a, b in units if a <= m.start() < b), (m.start(), m.end()))
            out.append({"id": e["id"], "flag_type": e["flag_type"], "category": e["category"], "strength": e["strength"],
                        "start": m.start(), "end": m.end(), "text": m.group(0), "unit_start": u[0], "unit_end": u[1]})
    return out
"""Loader for app/llm/lexicon.yaml (read as a data file; no app.llm import, so deterministic modules stay LLM-free)."""
import functools
import pathlib
import re

import yaml

LEXICON_PATH = pathlib.Path(__file__).resolve().parents[1] / "llm" / "lexicon.yaml"


@functools.lru_cache(maxsize=1)
def load() -> dict:
    return yaml.safe_load(LEXICON_PATH.read_text(encoding="utf-8"))


def code_list(name: str) -> list:
    """Entries of a `code_lists` category as [{id, regex}] (compiled IGNORECASE)."""
    return list(_compiled(name))


@functools.lru_cache(maxsize=None)
def _compiled(name: str) -> tuple:
    entries = load()["code_lists"][name]["entries"]
    return tuple({"id": e["id"], "regex": re.compile(e["pattern"], re.IGNORECASE)} for e in entries)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:44.345Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def \" app/db/db.py | head -40; grep -n \"def make_call\\|def conn\\|def body_of\\|now\" app/backend/api.py | head -20; sed -n 2,30p tests/unit/test_review_rules.py"
}
````

### User / tool · 2026-11-02T04:18:44.450Z

**tool result**
````
28:def init(path: str = ":memory:"):
36:def connect(path: str):
62:def _tok(prefix: str) -> str:
66:def _enc(v):
70:def _cols(conn, table):
74:def sha256(text: str) -> str:
78:def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
86:def update_case(conn, case_id: str, **fields) -> None:
95:def get_case(conn, case_id: str):
100:def _insert(conn, table, row):
108:def add_record(conn, case_id: str, **fields) -> str:
114:def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
127:def _find(conn, item_id, case=None):
144:def _decode(row) -> dict:
155:def get_item(conn, item_id: str, case: str = None) -> dict:
159:def list_items(conn, case_id: str, kind: str) -> list:
164:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
179:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
204:def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
211:def list_events(conn, case_id: str, item_id: str = None) -> list:
218:def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
227:def get_llm_call(conn, call_id: str):
232:def list_llm_calls(conn, case_id: str, item_id: str = None) -> list:
239:def delete_case(conn, case_id: str) -> None:
251:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
258:def table_counts(conn, case_id: str) -> dict:
123:    def conn():
126:    def make_call(c, cid):
190:    async def body_of(request: Request) -> dict:
279:            now = time.time()
280:            DB.purge_expired(c, now)
282:            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None,
286:                ing = pipeline_mod().ingest_case(c, cid, text, now)
327:            mod.run_pipeline(c, token, raw, call=make_call(c, token), now=time.time)
352:            now = time.time()
353:            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
356:            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
376:                return await run_in_threadpool(lambda: RJ.rejudge(c, token, make_call(c, token), now=time.time()))
452:            nar = narrative.draft(c, token, call=make_call(c, token), now=time.time())
466:                return {"narrative": narrative.review(c, token, b.get("action"), now=time.time())}
496:    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
533:            except trace.UnknownItem:
import pytest
from app.backend import pipeline as PL, review as RV, export as X
from app.db import db as DB
from app.llm import audited as AU
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, which_record

def seeded(tmp_path, case="sample"):
    """Seeds a case through the pipeline with a case-aware fake (extract returns the first sentence unit of the cited record)."""
    from tests.unit._fakes import sample_script, which_record as wr
    if case == "sample":
        call = FakeCall(sample_script())
    else:
        def extract(u):
            n = wr(u, case)[0]; ex = G.record(case, n)["excerpt"]
            return dict(summary=ex.split(". ")[0].rstrip(".") + ".", excerpt=ex.split(". ")[0].rstrip(".") + ".")
        call = FakeCall(sample_script(extract=extract))
    conn = DB.connect(str(tmp_path / f"rv-{case}.sqlite")); cid = DB.create_case(conn, G.raw(case), now=1.0)
    out = PL.run_pipeline(conn, cid, G.raw(case), call=call, now=lambda: 1.0)
    return conn, cid, out

def ent(out, n):
    """Entry id citing record n (api.md: entries carry record_ids like 'r5')."""
    return [e for e in out["entries"] + out.get("undated_entries", []) if f"r{n}" in e["record_ids"]][0]["id"]
def amt(out, raw): return [a for a in out["amounts"] if a["raw"] == raw][0]["id"]
def judge(v): return FakeCall({"j1": {"verdict": v, "reason_code": "NONE"}})

@pytest.mark.parametrize("edits", [{"date": "2026-01-01"}, {"provider": "Someone Else"}, {"record": "r2"}, {"summary": "ok", "date": "2026-01-01"}])
def test_entry_immutable_fields_are_422(tmp_path, edits):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:46.297Z

**tool call — Bash**
````
{
 "command": "sed -n 108,126p app/db/db.py; grep -n \"_ITEM_TABLES\" -A6 app/db/db.py | head -12"
}
````

### User / tool · 2026-11-02T04:18:46.389Z

**tool result**
````
def add_record(conn, case_id: str, **fields) -> str:
    rid = fields.pop("id", None) or _tok("r")
    _insert(conn, "records", {"id": rid, "case_id": case_id, **fields})
    return rid


def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
    """Insert an entry/amount/flag. payload keys must be column names (dicts/lists JSON-encoded). New items are pending."""
    if kind not in _ITEM_TABLES:
        raise ValueError(f"unknown item kind {kind!r}")
    table, prefix = _ITEM_TABLES[kind]
    p = dict(payload)
    if {"review_status", "edited_json", "edited"} & set(p):
        raise ValueError("review_status and edits are written only by apply_review (with an event row)")
    iid = p.pop("id", None) or _tok(prefix)
    _insert(conn, table, {"id": iid, "case_id": case_id, "updated_at": now, **p})
    return iid


21:_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
22-_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
23-_PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
24-_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
25-_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")
26-
27-
--
116:    if kind not in _ITEM_TABLES:
117-        raise ValueError(f"unknown item kind {kind!r}")
118:    table, prefix = _ITEM_TABLES[kind]
119-    p = dict(payload)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:49.910Z

Write the module.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:03.605Z

**tool call — Bash**
````
{
 "command": "cat > app/backend/dismissal_patterns.py <<'EOF'\n\"\"\"Dismissal-pattern SUGGESTIONS for the single local profile (T-089, D-042; code only, LLM_VS_CODE row 12). Suggestions only.\n\nThe tool has one local profile: no accounts, no users, no auth. \"Profile\" means this machine's database, so the history is the set of flags\nthe paralegal has dismissed in it (read from the flags table; nothing new is stored, and deleting a case deletes its history). Outside\nZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.\n\nWhen the same lexicon phrase (PHRASE_MIN dismissals) or the same category (CATEGORY_MIN) has been dismissed repeatedly, the review screen\nmay offer \"You dismissed this kind of flag 4 times. Hide similar ones in this case?\". This module only READS: suggest() never writes and\nnever changes a pipeline result, a flag's state or its review_status. The paralegal's click calls apply(), which dismisses the matching\nPENDING flags in this case one by one through the normal review path (each a logged `dismiss` event with a reviewer note). Those\nbulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself.\n\nOnly lexicon-phrase flags of type pre_existing or causation are eligible. Gap and conflict flags, injection and date warnings, and flags\nthat code or the model found without a lexicon phrase are never suggested for hiding.\"\"\"\nfrom app.backend import lexicon_scan, review\n\nPHRASE_MIN = 3\nCATEGORY_MIN = 5\nELIGIBLE_TYPES = (\"pre_existing\", \"causation\")\nAPPLIED_NOTE = \"Hidden by dismissal-pattern suggestion (paralegal confirmed).\"\n_BAD = (\"rejected\",)\n\n\ndef _eligible(f) -> bool:\n    return f[\"type\"] in ELIGIBLE_TYPES and \"lexicon\" in (f.get(\"origin\") or \"\")\n\n\ndef _phrase(f):\n    \"\"\"(lexicon entry id, matched phrase) for the flag, from its own evidence text, or (None, None). Same category only.\"\"\"\n    for ev in f.get(\"evidence\") or []:\n        hits = [h for h in lexicon_scan.scan(ev.get(\"text\") or \"\") if h[\"category\"] == f[\"category\"]]\n        if hits:\n            h = min(hits, key=lambda x: x[\"start\"])\n            return h[\"id\"], \" \".join(h[\"text\"].lower().split())\n    return None, None\n\n\ndef _history(conn, case_id: str, local: bool) -> list:\n    \"\"\"Dismissed, eligible flags that were dismissed by the paralegal one at a time.\"\"\"\n    rows = conn.execute(\"SELECT * FROM flags WHERE review_status='dismissed'\" + (\"\" if local else \" AND case_id=?\"), () if local else (case_id,)).fetchall()\n    from app.db import db as DB\n    return [f for f in (DB._decode(r) for r in rows) if _eligible(f) and (f.get(\"reviewer_note\") or \"\") != APPLIED_NOTE]\n\n\ndef _pending(conn, case_id: str) -> list:\n    from app.db import db as DB\n    return [f for f in DB.list_items(conn, case_id, \"flag\") if f[\"review_status\"] == \"pending\" and f[\"state\"] not in _BAD and _eligible(f)]\n\n\ndef suggest(conn, case_id: str, *, local: bool = False) -> list:\n    \"\"\"Read-only. [{key, kind: phrase|category, label, dismissed_count, scope, flag_ids, message}], phrase suggestions first.\"\"\"\n    hist = _history(conn, case_id, local)\n    phrase_n, cat_n = {}, {}\n    for f in hist:\n        pid, _ = _phrase(f)\n        if pid:\n            phrase_n[pid] = phrase_n.get(pid, 0) + 1\n        cat_n[f[\"category\"]] = cat_n.get(f[\"category\"], 0) + 1\n    out, covered = [], set()\n    pend = [(f, *_phrase(f)) for f in _pending(conn, case_id)]\n    scope = \"all cases on this computer\" if local else \"this case\"\n    for pid in sorted({p for _, p, _ in pend if p and phrase_n.get(p, 0) >= PHRASE_MIN}):\n        ids = [f[\"id\"] for f, p, _ in pend if p == pid]\n        label = next(t for _, p, t in pend if p == pid)\n        out.append(_row(f\"phrase:{pid}\", \"phrase\", label, phrase_n[pid], scope, ids))\n        covered.update(ids)\n    for cat in sorted({f[\"category\"] for f, _, _ in pend if cat_n.get(f[\"category\"], 0) >= CATEGORY_MIN}):\n        ids = [f[\"id\"] for f, _, _ in pend if f[\"category\"] == cat and f[\"id\"] not in covered]\n        if ids:\n            out.append(_row(f\"category:{cat}\", \"category\", cat.replace(\"_\", \" \"), cat_n[cat], scope, ids))\n    return out\n\n\ndef _row(key, kind, label, n, scope, ids):\n    return {\"key\": key, \"kind\": kind, \"label\": label, \"dismissed_count\": n, \"scope\": scope, \"flag_ids\": ids, \"auto_applied\": False,\n            \"message\": f\"You dismissed this kind of flag {n} times. Hide similar ones in this case?\"}\n\n\ndef apply(conn, case_id: str, key: str, *, local: bool = False, now=None) -> dict:\n    \"\"\"The paralegal accepted the suggestion: dismiss the matching pending flags in THIS case through the normal review path.\n    Raises KeyError when the key is not a current suggestion (nothing is written).\"\"\"\n    s = next((x for x in suggest(conn, case_id, local=local) if x[\"key\"] == key), None)\n    if s is None:\n        raise KeyError(key)\n    for fid in s[\"flag_ids\"]:\n        review.apply_review(conn, case_id, fid, {\"action\": \"dismiss\", \"note\": APPLIED_NOTE}, now=now)\n    return {\"key\": key, \"dismissed_flag_ids\": s[\"flag_ids\"], \"suggestions\": suggest(conn, case_id, local=local)}\nEOF\npython3 - <<'EOF'\np='/Users/arsis/zlayt-pm-project/app/backend/dismissal_patterns.py'\ns=open(p).read()\ns=s.replace(\"from app.backend import lexicon_scan, review\\n\",\"from app.backend import lexicon_scan, review\\nfrom app.db import db as DB\\n\").replace(\"    from app.db import db as DB\\n\",\"\")\nopen(p,'w').write(s)\nEOF\nsed -n 460,500p app/backend/api.py | head -5; grep -n \"get_case_view\\|/trace\\\"\" app/backend/api.py | head"
}
````

### User / tool · 2026-11-02T04:19:03.726Z

**tool result**
````
    async def narrative_review(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
305:    def get_case_view(token: str):
525:    @app.get("/api/cases/{token}/items/{item_id}/trace")
538:    @app.get("/api/cases/{token}/trace")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:08.852Z

**tool call — Bash**
````
{
 "command": "sed -n 490,500p app/backend/api.py; grep -n \"def add_routes\" -A25 app/backend/case_extras.py | head -45; sed -n 85,92p app/backend/case_extras.py | head -3; grep -n \"ApiError\" app/backend/api.py | head -4"
}
````

### User / tool · 2026-11-02T04:19:08.957Z

**tool result**
````
        try:
            get_case(c, token)
            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
        finally:
            c.close()

    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)

    @app.get("/api/cases/{token}/export")
    def export(token: str):
        from app.backend import export_routes as XR
106:def add_routes(app, *, conn, get_case, body_of, ApiError, now):
107-    @app.post("/api/cases/{token}/review/batch")
108-    async def review_batch(token: str, request: Request):
109-        b = await body_of(request)
110-        c = conn()
111-        try:
112-            get_case(c, token)
113-            try:
114-                return apply_batch(c, token, b, now())
115-            except ValueError:
116-                raise ApiError(400, "bad_request", "Send an action (accept or reset) and a list of entry ids.") from None
117-            except BatchRefused as e:
118-                if any(r["reason"] == "date_unconfirmed" for r in e.rejected):     # D-041: same code as a single accept
119-                    raise ApiError(422, "DATE_UNCONFIRMED", "Confirm the date of every undated entry first (Dates to confirm); nothing was changed.", {"rejected": e.rejected}) from None
120-                raise ApiError(422, "invalid_batch", "Only verified entries can be accepted together; nothing was changed.", {"rejected": e.rejected}) from None
121-        finally:
122-            c.close()
123-
124-    @app.get("/api/cases/{token}/export_config")
125-    def export_config_get(token: str):
126-        c = conn()
127-        try:
128-            get_case(c, token)
129-            return get_config(c, token)
130-        finally:
131-            c.close()
        out["bates_start"] = s
    else:
        raise ValueError("invalid_edit")
46:class ApiError(Exception):
141:            raise ApiError(404, "not_found", "No such case.")
145:    @app.exception_handler(ApiError)
193:            raise ApiError(413, "input_too_large", "Input is too large.")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:13.837Z

**tool call — Bash**
````
{
 "command": "cat >> app/backend/dismissal_patterns.py <<'EOF'\n\n\ndef add_routes(app, *, conn, get_case, body_of, ApiError, now, local_mode):\n    @app.get(\"/api/cases/{token}/dismissal_suggestions\")\n    def dismissal_suggestions(token: str):\n        c = conn()\n        try:\n            get_case(c, token)\n            return {\"suggestions\": suggest(c, token, local=local_mode()), \"min_phrase\": PHRASE_MIN, \"min_category\": CATEGORY_MIN}\n        finally:\n            c.close()\n\n    @app.post(\"/api/cases/{token}/dismissal_suggestions/apply\")\n    async def dismissal_suggestions_apply(token: str, request: Request):\n        b = await body_of(request)\n        if not isinstance(b.get(\"key\"), str):\n            raise ApiError(400, \"bad_request\", \"Send the key of the suggestion to apply.\")\n        c = conn()\n        try:\n            get_case(c, token)\n            try:\n                return apply(c, token, b[\"key\"], local=local_mode(), now=now)\n            except KeyError:\n                raise ApiError(404, \"not_found\", \"That suggestion no longer applies.\") from None\n        finally:\n            c.close()\nEOF\nsed -i '' 's/^from app.backend import lexicon_scan, review$/from fastapi import Request\\n\\nfrom app.backend import lexicon_scan, review/' app/backend/dismissal_patterns.py\npython3 - <<'EOF'\np='/Users/arsis/zlayt-pm-project/app/backend/api.py'\ns=open(p).read()\nold=\"    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)\\n\"\nassert s.count(old)==1\ns=s.replace(old, old+\"    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089\\n\")\nopen(p,'w').write(s)\nEOF\ngrep -n \"^from app.backend import\\|^import\\|case_extras\" app/backend/api.py | head"
}
````

### User / tool · 2026-11-02T04:19:13.954Z

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
23:from app.backend import case_extras, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:31.533Z

**tool call — Bash**
````
{
 "command": "sed -i '' '23s/from app.backend import case_extras, export as export_mod,/from app.backend import case_extras, dismissal_patterns, export as export_mod,/' app/backend/api.py && sed -n 23p app/backend/api.py\ncat > tests/unit/test_dismissal_patterns.py <<'EOF'\n\"\"\"T-089: dismissal-pattern suggestions for the single local profile. Read-only suggestions; never auto-dismiss; no effect on pipeline output.\"\"\"\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import dismissal_patterns as DP, pipeline as PL\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit._fakes import FakeCall, sample_script\nfrom tests.unit.test_review_rules import seeded\n\nNEW_ONSET = \"New onset pain radiating to right arm with numbness in fingers.\"\n\n\ndef add_flag(conn, case, fid, *, category=\"new_onset\", text=NEW_ONSET, type_=\"causation\", origin=\"lexicon+llm\", status=None):\n    DB.add_item(conn, case, \"flag\", {\"id\": fid, \"type\": type_, \"category\": category, \"origin\": origin, \"title\": \"t\", \"explanation\": \"e\",\n                \"evidence_json\": [{\"record_no\": 1, \"text\": text, \"start\": 0, \"end\": len(text)}], \"state\": \"verified\", \"state_reasons_json\": []})\n    if status:\n        DB.apply_review(conn, fid, status, now=1.0, case=case)\n\n\ndef snapshot(conn, case):\n    return [(f[\"id\"], f[\"review_status\"], f[\"state\"]) for f in DB.list_items(conn, case, \"flag\")]\n\n\ndef test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss(tmp_path):\n    conn, cid, _ = seeded(tmp_path)\n    for i in range(3):\n        add_flag(conn, cid, f\"f_old{i}\", status=\"dismiss\")\n    before = snapshot(conn, cid)\n    s = DP.suggest(conn, cid)\n    assert len(s) == 1 and s[0][\"kind\"] == \"phrase\" and s[0][\"dismissed_count\"] == 3 and s[0][\"auto_applied\"] is False\n    assert s[0][\"message\"] == \"You dismissed this kind of flag 3 times. Hide similar ones in this case?\"\n    assert \"f_r7_2\" in s[0][\"flag_ids\"]                           # the sample's pending new_onset flag\n    assert snapshot(conn, cid) == before                          # suggest() wrote nothing; the flag is still pending\n    assert next(f for f in DB.list_items(conn, cid, \"flag\") if f[\"id\"] == \"f_r7_2\")[\"review_status\"] == \"pending\"\n\n\ndef test_two_dismissals_are_not_enough(tmp_path):\n    conn, cid, _ = seeded(tmp_path)\n    for i in range(2):\n        add_flag(conn, cid, f\"f_old{i}\", status=\"dismiss\")\n    assert DP.suggest(conn, cid) == []\n\n\ndef test_ineligible_flags_are_never_suggested(tmp_path):\n    conn, cid, _ = seeded(tmp_path)\n    for i in range(6):\n        add_flag(conn, cid, f\"f_g{i}\", category=\"gap_over_30\", type_=\"gap\", origin=\"code\", status=\"dismiss\")\n        add_flag(conn, cid, f\"f_i{i}\", category=\"injection_suspected\", type_=\"record_warning\", origin=\"code\", status=\"dismiss\")\n    assert DP.suggest(conn, cid) == []\n\n\ndef test_category_suggestion_after_five_dismissals_of_different_phrases(tmp_path):\n    conn, cid, _ = seeded(tmp_path)\n    texts = [\"Pain began after the collision.\", \"Symptoms began after the accident.\", \"Onset after the fall.\", \"New onset of numbness.\",\n             \"Developed pain after the accident.\"]\n    for i, t in enumerate(texts):\n        add_flag(conn, cid, f\"f_c{i}\", category=\"patient_report\", text=t, status=\"dismiss\")\n    s = DP.suggest(conn, cid)\n    assert [x[\"kind\"] for x in s] in ([\"category\"], [\"phrase\", \"category\"], [\"phrase\"]) or s == []\n    cats = [x for x in s if x[\"kind\"] == \"category\"]\n    for x in cats:\n        assert x[\"dismissed_count\"] >= DP.CATEGORY_MIN\n\n\ndef test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself(tmp_path):\n    conn, cid, _ = seeded(tmp_path)\n    for i in range(3):\n        add_flag(conn, cid, f\"f_old{i}\", status=\"dismiss\")\n    key = DP.suggest(conn, cid)[0][\"key\"]\n    n_events = len(DB.list_events(conn, cid))\n    out = DP.apply(conn, cid, key, now=2.0)\n    assert out[\"dismissed_flag_ids\"] == [\"f_r7_2\"] and out[\"suggestions\"] == []\n    f = next(x for x in DB.list_items(conn, cid, \"flag\") if x[\"id\"] == \"f_r7_2\")\n    assert f[\"review_status\"] == \"dismissed\" and f[\"reviewer_note\"] == DP.APPLIED_NOTE\n    assert len(DB.list_events(conn, cid)) == n_events + 1         # one logged dismiss event\n    # a bulk-hidden flag is not a new manual dismissal: the count stays 3, not 4\n    add_flag(conn, cid, \"f_new\")\n    assert DP.suggest(conn, cid)[0][\"dismissed_count\"] == 3\n    with pytest.raises(KeyError):\n        DP.apply(conn, cid, \"phrase:nope\")\n\n\ndef test_scope_is_this_case_unless_local_profile(tmp_path):\n    conn, cid, _ = seeded(tmp_path)\n    other = DB.create_case(conn, \"x\", now=1.0)\n    for i in range(3):\n        add_flag(conn, other, f\"f_o{i}\", status=\"dismiss\")\n    assert DP.suggest(conn, cid, local=False) == []\n    s = DP.suggest(conn, cid, local=True)\n    assert len(s) == 1 and s[0][\"scope\"] == \"all cases on this computer\"\n\n\ndef test_routes_and_demo_mode_isolation(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    monkeypatch.delenv(\"ZLAYT_MODE\", raising=False)\n    from tests.unit.test_api_routes import run_case\n    db = str(tmp_path / \"r.sqlite\")\n    c = TestClient(create_app(db, static_dir=str(tmp_path)))\n    t = run_case(c)\n    conn = DB.connect(db)\n    for i in range(3):\n        add_flag(conn, t, f\"f_old{i}\", status=\"dismiss\")\n    conn.close()\n    r = c.get(f\"/api/cases/{t}/dismissal_suggestions\")\n    assert r.status_code == 200 and r.json()[\"suggestions\"][0][\"dismissed_count\"] == 3\n    assert c.get(\"/api/cases/nope/dismissal_suggestions\").status_code == 404\n    assert c.post(f\"/api/cases/{t}/dismissal_suggestions/apply\", json={}).status_code == 400\n    assert c.post(f\"/api/cases/{t}/dismissal_suggestions/apply\", json={\"key\": \"phrase:zzz\"}).status_code == 404\n    key = r.json()[\"suggestions\"][0][\"key\"]\n    a = c.post(f\"/api/cases/{t}/dismissal_suggestions/apply\", json={\"key\": key})\n    assert a.status_code == 200 and a.json()[\"dismissed_flag_ids\"] and a.json()[\"suggestions\"] == []\n\n\n@pytest.mark.parametrize(\"case\", G.case_names()[:3] + [\"sample\"])\ndef test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged(tmp_path, case):\n    \"\"\"Same case through the pipeline with and without a dismissal history in the database: identical flags, entries and amounts.\"\"\"\n    def run(seed_history):\n        conn = DB.connect(str(tmp_path / f\"{case}-{seed_history}.sqlite\"))\n        if seed_history:\n            hist = DB.create_case(conn, \"history\", now=1.0)\n            for i in range(8):\n                add_flag(conn, hist, f\"f_h{i}\", status=\"dismiss\")\n        cid = DB.create_case(conn, G.raw(case), now=1.0)\n        PL.run_pipeline(conn, cid, G.raw(case), call=FakeCall(sample_script()), now=lambda: 1.0)\n        view = {k: [(i[\"id\"], i.get(\"category\"), i[\"state\"], i[\"review_status\"]) for i in DB.list_items(conn, cid, k)] for k in (\"entry\", \"amount\", \"flag\")}\n        DP.suggest(conn, cid, local=True)                          # computing suggestions after the run must not matter either\n        assert {k: [(i[\"id\"], i.get(\"category\"), i[\"state\"], i[\"review_status\"]) for i in DB.list_items(conn, cid, k)] for k in view} == view\n        return view\n    assert run(False) == run(True)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_dismissal_patterns.py tests/unit/test_date_convention.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:19:34.026Z

**tool result**
````
from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
           ^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/concurrent/futures/thread.py:58: in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app/backend/generator.py:118: in _one
    return extract_one(record, group, call=call, case_text=case_text)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
app/backend/generator.py:49: in extract_one
    out, call_id = call(step, prompt.text, extract_prompt(record, n), schemas.ExtractOutput.model_json_schema(), item_id=item)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/unit/_fakes.py:14: in __call__
    out = self.script[step](user) if callable(self.script.get(step)) else self.script.get(step, {})
          ^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

user = 'SOURCE LABEL (context only; do not copy):\n<record-c470791b07d9>\nGloamwood Chiropractic, initial evaluation\n</recor...ain 5/10. Treatment plan: 8 visits. Fee schedule: $95 per adjustment.\n</record-c470791b07d9>\nReturn the JSON object.'

    def extract(user):
>       n = which_record(user)[0]
            ^^^^^^^^^^^^^^^^^^^^^
E       IndexError: list index out of range

tests/unit/_fakes.py:46: IndexError
=========================== short test summary info ============================
FAILED tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_01_date_formats]
FAILED tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_02_gap_boundaries]
FAILED tests/unit/test_dismissal_patterns.py::test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged[case_03_rate_and_ocr]
3 failed, 16 passed in 2.10s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:38.068Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_dismissal_patterns.py'\ns=open(p).read()\ns=s.replace(\"from tests.unit._fakes import FakeCall, sample_script\\n\",\"from tests.unit._fakes import FakeCall, sample_script, which_record as wr\\n\")\ns=s.replace(\"        PL.run_pipeline(conn, cid, G.raw(case), call=FakeCall(sample_script()), now=lambda: 1.0)\\n\",'''        def extract(u):\n            ex = G.record(case, wr(u, case)[0])[\"excerpt\"].split(\". \")[0].rstrip(\".\") + \".\"\n            return dict(summary=ex, excerpt=ex)\n        PL.run_pipeline(conn, cid, G.raw(case), call=FakeCall(sample_script() if case == \"sample\" else sample_script(extract=extract)), now=lambda: 1.0)\n''')\ns=s.replace('G.case_names()[:3] + [\"sample\"]','G.case_names()')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_dismissal_patterns.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:19:40.327Z

**tool result**
````
.................                                                        [100%]
17 passed in 1.85s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:45.427Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_dismissal_patterns.py'\ns=open(p).read()\ni=s.index(\"    s = DP.suggest(conn, cid)\\n    assert [x[\\\"kind\\\"]\")\nj=s.index(\"def test_apply_dismisses\")\ns=s[:i]+'''    s = DP.suggest(conn, cid)\n    cats = [x for x in s if x[\"kind\"] == \"category\"]\n    assert len(cats) == 1 and cats[0][\"key\"] == \"category:patient_report\" and cats[0][\"dismissed_count\"] == 5\n    assert cats[0][\"flag_ids\"] == [\"f_r9_1\"] and cats[0][\"label\"] == \"patient report\"\n\n\n'''+s[j:]\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_dismissal_patterns.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:19:47.598Z

**tool result**
````
.................                                                        [100%]
17 passed in 1.74s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:48.435Z

Now the contract. Re-read api.md right before editing.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:20:01.293Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='memory/contracts/api.md'\ns=open(p).read()\n# 1. endpoint index rows (after confirm_date row)\nrow_anchor=\"| POST | `/api/cases/{token}/records/{rid}/entry` |\"\nassert s.count(row_anchor)==1\nnew_rows=(\"| GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |\\n\"\n          \"| POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |\\n\")\ns=s.replace(row_anchor,new_rows+row_anchor)\n# 2. sections before the \"GET items Why\" section\nanchor=\"## GET /api/cases/{token}/items/{item_id}  — \\\"Why?\\\"\"\nassert s.count(anchor)==1\nsec='''## Date-convention suggestion (T-088, D-042): `dates_to_confirm[].suggestion`\nEvery entry of `dates_to_confirm` (in `GET /api/cases/{token}` and in the `confirm_date` response) now has a `suggestion`: `null`, or a hint for an **ambiguous** numeric date. Code only (`app/backend/date_convention.py`). It looks at the other numeric dates in the packet whose order is certain (one number above 12: `03/14/2026` is month first, `14/03/2026` is day first), in each record's date label and text. It suggests only when all of that evidence agrees; no evidence, or evidence in both orders, gives `null`.\n```json\n{ \"record_id\": \"r8\", \"raw\": \"04/05/2026\", \"candidates\": [\"2026-04-05\", \"2026-05-04\"], \"status\": \"ambiguous\",\n  \"suggestion\": { \"convention\": \"MDY\", \"label\": \"MM/DD\", \"iso\": \"2026-04-05\",\n                  \"reason\": \"Other dates in this record use month first (03/14/2026)\",\n                  \"evidence\": [{\"record_id\": \"r3\", \"raw\": \"03/14/2026\"}], \"evidence_count\": 1, \"auto_applied\": false } }\n```\n`convention` is `MDY` or `DMY`. `iso` is the candidate that reading gives, always one of `candidates`, or `null` when the year is also ambiguous (two-digit year above 40). `reason` is plain words: one date reads \"Other dates in this record use month first (03/14/2026)\"; several read \"4 other dates in this record use month first (02/17/2026) and (03-17-26)\" (at most two examples in `evidence`, the total in `evidence_count`). `auto_applied` is always `false`.\n\nThe suggestion changes nothing: the record stays `ambiguous`, its entry stays in `undated_entries`, and Accept stays blocked (D-041, `DATE_UNCONFIRMED`) until the paralegal confirms through `confirm_date`, which still accepts only a code candidate (`422 date_invalid` otherwise). **UI:** pre-select the radio for `suggestion.iso` (when not null), show `reason` under it, keep the confirm button enabled only on an explicit click, and let the paralegal pick the other reading freely. Do not confirm on load.\n\n## Dismissal-pattern suggestions (T-089, D-042): `GET /api/cases/{token}/dismissal_suggestions`\nSuggestions only (`app/backend/dismissal_patterns.py`). The tool has one local profile and no accounts, so \"the profile\" is this machine's database: the history is the set of flags the paralegal dismissed one at a time. Under `ZLAYT_MODE=local` it counts every case in the database; otherwise only this case (a public/demo token never sees another case's dismissals). Nothing new is stored. Only lexicon-phrase flags of type `pre_existing` or `causation` can be suggested; gap and conflict flags, injection and date warnings are never offered for hiding.\nResponse 200:\n```json\n{ \"suggestions\": [\n    { \"key\": \"phrase:new_onset_001\", \"kind\": \"phrase\", \"label\": \"new onset\", \"dismissed_count\": 4, \"scope\": \"all cases on this computer\",\n      \"flag_ids\": [\"f_r7_2\"], \"auto_applied\": false,\n      \"message\": \"You dismissed this kind of flag 4 times. Hide similar ones in this case?\" } ],\n  \"min_phrase\": 3, \"min_category\": 5 }\n```\n`kind` is `phrase` (same lexicon phrase group dismissed at least `min_phrase` times) or `category` (same category at least `min_category` times, listing only flags a phrase suggestion does not already cover). `flag_ids` are this case's still-**pending** flags that match. The list is empty when nothing qualifies. This GET is read-only and changes no flag, state or pipeline result.\n\n### POST /api/cases/{token}/dismissal_suggestions/apply\nRequest `{\"key\": \"phrase:new_onset_001\"}`. This is the paralegal's click on \"Hide similar\": the server dismisses each matching pending flag in this case through the normal review path (one logged `dismiss` event per flag, `reviewer_note` \"Hidden by dismissal-pattern suggestion (paralegal confirmed).\"). They stay reversible with `reset`. Response 200: `{\"key\", \"dismissed_flag_ids\": [...], \"suggestions\": [...]}` (the refreshed list). `404 not_found` when the key is not a current suggestion (nothing written); `400 bad_request` without a `key`. Bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself. **UI:** show the `message` as a dismissible banner/chip on the flags list with two buttons (\"Hide similar\", \"Keep showing\"); \"Keep showing\" is client-side only. Never call `apply` without the click; never hide flags on load. Hidden flags remain in the Dismissed filter.\n\n'''\ns=s.replace(anchor,sec+anchor)\nopen(p,'w').write(s)\nEOF\ngit diff --stat memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T04:20:01.511Z

**tool result**
````
 memory/contracts/api.md | 29 +++++++++++++++++++++++++++++
 1 file changed, 29 insertions(+)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:20:03.678Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nfrom app.backend import lexicon_scan\nprint([(h[\"id\"],h[\"text\"]) for h in lexicon_scan.scan(\"New onset pain radiating to right arm\") ])\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T04:20:34.880Z

**tool result**
````
[('new_onset', 'New onset')]
FAILED tests/unit/test_pipeline.py::test_j3_error_or_unsure_makes_llm_conflicts_needs_review[j31]
FAILED tests/unit/test_pipeline.py::test_j3_conflict_verdict_keeps_semantic_conflict_and_code_conflict_is_unaffected
FAILED tests/unit/test_review_rules.py::test_any_judge_exception_on_edit_is_judge_unavailable_never_supported[exc1]
FAILED tests/unit/test_review_rules.py::test_any_judge_exception_on_edit_is_judge_unavailable_never_supported[exc2]
FAILED tests/unit/test_review_rules.py::test_any_judge_exception_on_edit_is_judge_unavailable_never_supported[exc3]
FAILED tests/unit/test_t075_determinism.py::test_conflict_order_and_duplicates_do_not_change_the_conflict_list
FAILED tests/unit/test_t075_determinism.py::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2
14 failed, 1159 passed in 29.84s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:20:36.768Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/phrase:new_onset_001/phrase:new_onset/g' memory/contracts/api.md && .venv/bin/python -m pytest -q tests/unit 2>&1 | grep FAILED | grep -v \"j3\\|j31\\|t075\\|judge_exception\\|conflict\" "
}
````

### User / tool · 2026-11-02T04:21:08.038Z

**tool result**
````
/bin/bash: child setpgid (92176 to 92176): Operation not permitted
        for exc, code in ((AU.LLMFailed("x"), "LLM_FAILED_AFTER_RETRIES"), (P.FixtureMiss("x"), "FIXTURE_MISS")):
FAILED tests/unit/test_api_routes.py::test_only_review_module_sets_review_status
FAILED tests/unit/test_flags_injection.py::test_cross_record_pass_carries_the_tag_while_any_record_is_tagged
FAILED tests/unit/test_provider.py::test_single_call_path - AssertionError: a...
FAILED tests/unit/test_provider_backends.py::test_single_call_path - Assertio...
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:09.649Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_api_routes.py::test_only_review_module_sets_review_status 2>&1 | grep -E \"^E|assert\" | head; grep -n \"def test_only_review_module_sets_review_status\" -A15 tests/unit/test_api_routes.py"
}
````

### User / tool · 2026-11-02T04:21:10.311Z

**tool result**
````
>           assert "DB.apply_review(" not in src and "set_review_status(" not in src, p.name
E           AssertionError: reclassify.py
E           assert ('DB.apply_review(' not in '"""Guarded ... c.close()\n'
E             
E             'DB.apply_review(' is contained here:
E               g
E                       DB.apply_review(conn, item_id, "reset", now=t, case=case_id)
E             ?         ++++++++++++++++
E                   _log(conn, case_id, item_id, before, {"event": "reclassify", "kind": new_kind, "review_status": "pending", "wording": wording,
E                                                         "judge_verdict": (jd or {}).get("verdict"), "judge_call_id": (jd or {}).get("call_id"), "restored": restored,...
181:def test_only_review_module_sets_review_status():
182-    """T-040 AC5: apply_review/set_review_status are called only from review.py (and the pipeline's own rerun reset); no bulk route."""
183-    for p in (ROOT / "app" / "backend").glob("*.py"):
184-        if p.name in ("review.py", "pipeline.py", "case_extras.py"):   # case_extras: batch accept of verified entries (D-031)
185-            continue
186-        src = p.read_text()
187-        assert "DB.apply_review(" not in src and "set_review_status(" not in src, p.name
188-    tree = ast.parse((ROOT / "app" / "backend" / "api.py").read_text())
189-    assert not [n for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and "accept_all" in n.value]
190-
191-
192-def test_no_text_in_logs(env, caplog, capsys):
193-    _, c = env
194-    caplog.set_level("DEBUG")
195-    run_case(c)
196-    out = capsys.readouterr()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:13.022Z

**tool call — Bash**
````
{
 "command": "git diff --stat app/backend/api.py app/backend/present.py memory/contracts/api.md; git diff app/backend/api.py app/backend/present.py | grep '^[+-]' | grep -v '^+++\\|^---' | cut -c1-140"
}
````

### User / tool · 2026-11-02T04:21:13.137Z

**tool result**
````
 app/backend/api.py      |  5 ++++-
 app/backend/present.py  |  9 ++++++---
 memory/contracts/api.md | 29 +++++++++++++++++++++++++++++
 3 files changed, 39 insertions(+), 4 deletions(-)
-from app.backend import case_extras, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
+from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
+    from app.backend import reclassify
+    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
+    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mo
-from app.backend import confidence, grounding, pdf_text, sentences, store, totals as T, why
+from app.backend import confidence, date_convention, grounding, pdf_text, sentences, store, totals as T, why
-    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"]}
-            for r in _recs_by_id(conn, case_id).values() if r["date_status"] in ("ambiguous", "missing")]
+    recs = list(_recs_by_id(conn, case_id).values())
+    raw = DB.get_case(conn, case_id)["raw_text"]
+    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"],
+             "suggestion": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)
+            for r in recs if r["date_status"] in ("ambiguous", "missing")]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:16.064Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(mktemp -u) && git read-tree HEAD && git show HEAD:app/backend/api.py > /private/tmp/claude-501/api_head.py 2>/dev/null || git show HEAD:app/backend/api.py > $TMPDIR/api_head.py; ls /private/tmp/claude-501/api_head.py 2>&1 | head -1"
}
````

### User / tool · 2026-11-02T04:21:16.275Z

**tool result**
````
/private/tmp/claude-501/api_head.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:19.849Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx_t088 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && python3 - <<'EOF'\np='/private/tmp/claude-501/api_head.py'\ns=open(p).read()\na=\"from app.backend import case_extras, export as export_mod,\"\nassert a in s\ns=s.replace(a,\"from app.backend import case_extras, dismissal_patterns, export as export_mod,\")\nold=\"    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)\\n\"\nassert s.count(old)==1\ns=s.replace(old, old+\"    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089\\n\")\nopen(p,'w').write(s)\nEOF\ngit diff HEAD --stat -- app/backend/present.py | tail -1\nH=$(git hash-object -w /private/tmp/claude-501/api_head.py) && git update-index --cacheinfo 100644,$H,app/backend/api.py\ngit add app/backend/date_convention.py app/backend/dismissal_patterns.py app/backend/present.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py memory/contracts/api.md\ngit diff --cached --stat"
}
````

### User / tool · 2026-11-02T04:21:20.186Z

**tool result**
````
 1 file changed, 6 insertions(+), 3 deletions(-)
 app/backend/api.py                    |   3 +-
 app/backend/date_convention.py        |  67 +++++++++++++++++
 app/backend/dismissal_patterns.py     | 114 +++++++++++++++++++++++++++++
 app/backend/present.py                |   9 ++-
 memory/contracts/api.md               |  29 ++++++++
 tests/unit/test_date_convention.py    | 103 ++++++++++++++++++++++++++
 tests/unit/test_dismissal_patterns.py | 134 ++++++++++++++++++++++++++++++++++
 7 files changed, 455 insertions(+), 4 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:22.677Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx_t088 && git commit -q -m \"feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)\n\nBoth are suggestions only: neither changes pipeline output or applies itself.\nContract in memory/contracts/api.md.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git log -1 --format=%h; unset GIT_INDEX_FILE; git status --short app/backend/api.py app/backend/present.py memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T04:21:23.120Z

**tool result**
````
check_secrets: ok (7 file(s) scanned staged)
f667f08
MM app/backend/api.py
MM app/backend/present.py
MM memory/contracts/api.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:36.731Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"\n$B note T-088 --agent backend --text \"UI needs: dates_to_confirm[].suggestion {convention, label, iso, reason, evidence, auto_applied:false} (contract in api.md). Pre-select the radio for suggestion.iso (when non-null), show reason beneath, still require an explicit confirm click (D-041); never confirm on load. Golden: evals/golden/case_01_date_formats should get a case asserting the 04/05/2026 record's suggestion is MM/DD with 4 evidence dates (qa owns golden; unit test tests/unit/test_date_convention.py covers it on that file today). No db change.\"\n$B ac T-088 --check 1 --agent backend --evidence \"tests/unit/test_date_convention.py (8 tests) pass: month-first/day-first/no-evidence/mixed evidence, golden case_01 suggestion, confirm still required, nothing written. UI pre-select is frontend's (see note)\"\n$B handoff T-088 --agent backend --text \"Changed: new app/backend/date_convention.py (code only); present.dates_to_confirm adds suggestion; contract section in memory/contracts/api.md. Verified: .venv/bin/python -m pytest tests/unit/test_date_convention.py (8 pass); full unit run has 14 failures all in T-094 J3/conflict, reclassify and provider tests, none from this card. Left: frontend pre-select; qa golden case. Surprised: ambiguous dates within the record text also count as evidence, but dates in ISO form do not. Commit f667f08.\"\n$B move T-088 in_review --agent backend\n$B commit T-088 --sha f667f08 --agent backend\n$B note T-089 --agent backend --text \"UI needs: GET /api/cases/{token}/dismissal_suggestions -> {suggestions:[{key,kind,label,dismissed_count,scope,flag_ids,message,auto_applied:false}]}; show message as a banner on the flags list with Hide similar (POST .../dismissal_suggestions/apply {key}) and Keep showing (client-side only). Never apply on load. Hidden flags stay in the Dismissed filter and are reversible via reset. Thresholds 3 (phrase) and 5 (category); only lexicon pre_existing/causation flags are eligible. History is read from the flags table (no db change); counts span all cases only under ZLAYT_MODE=local. Golden: no case needed; unit test proves identical pipeline output on every golden case with and without dismissal history.\"\n$B ac T-089 --check 1 --agent backend --evidence \"tests/unit/test_dismissal_patterns.py (17 pass): 3 dismissals -> suggestion, 2 -> none, apply only on click via review path, no self-reinforcement, ineligible types never offered, demo-mode isolation, pipeline output identical on all golden cases + sample with/without history (recall unchanged)\"\n$B handoff T-089 --agent backend --text \"Changed: new app/backend/dismissal_patterns.py (suggest read-only, apply = paralegal click via review.apply_review), 2 routes registered in api.py, contract in api.md. Verified: .venv/bin/python -m pytest tests/unit/test_dismissal_patterns.py (17 pass); recall unchanged shown by pipeline-output equality on every golden case. Left: frontend banner; optional db CHECK for a dismissal_suggestion event (not needed, reviewer_note marks bulk-hidden flags). Surprised: flags do not store the lexicon phrase, so the phrase is re-derived by lexicon_scan on the flag's evidence. Commit f667f08.\"\n$B move T-089 in_review --agent backend\n$B commit T-089 --sha f667f08 --agent backend 2>&1 | tail -2"
}
````

### User / tool · 2026-11-02T04:21:37.363Z

**tool result**
````
noted on T-088
AC 1 checked: tests/unit/test_date_convention.py (8 tests) pass: month-first/day-first/no-evidence/mixed evidence, golden case_01 suggestion, confirm still required, nothing written. UI pre-select is frontend's (see note)
handoff written on T-088
T-088: in_progress -> in_review
T-088: commit f667f08 recorded
noted on T-089
AC 1 checked: tests/unit/test_dismissal_patterns.py (17 pass): 3 dismissals -> suggestion, 2 -> none, apply only on click via review path, no self-reinforcement, ineligible types never offered, demo-mode isolation, pipeline output identical on all golden cases + sample with/without history (recall unchanged)
handoff written on T-089
T-089: in_progress -> in_review
T-089: commit f667f08 recorded
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:42.058Z

T-088 and T-089 are both in review, committed as f667f08. Both are suggestions only: neither changes pipeline output, and the paralegal still confirms.

- **T-088:** `dates_to_confirm[].suggestion` now carries MM/DD or DD/MM with a stated reason, e.g. "Other dates in this record use month first (03/14/2026)". It comes from unambiguous dates elsewhere in the packet, and `confirm_date` is unchanged. The 8 new tests pass, including golden `case_01`; golden needs a case for the 04/05/2026 suggestion, noted on the card for qa.
- **T-089:** `GET /api/cases/{token}/dismissal_suggestions` shows a pattern after 3 dismissals of the same phrase or 5 of the same category. The hide only happens when the paralegal clicks and calls `POST .../apply`. Pipeline output is identical on every golden case with and without a dismissal history, so recall is unchanged. The 17 new tests pass. Nothing new is stored, so there is no db change.
- **Contract and UI notes:** the contract for both is in `memory/contracts/api.md`, and the UI needs are noted on each card.
- **Wider unit run:** `tests/unit` has 14 failures, none in my code: T-094 J3/conflict tests, `reclassify.py` and provider tests.
- **Staged state:** I committed through a temp index. The real index still shows `api.py`, `present.py` and `api.md` as staged-modified, so anyone else committing those files should check what's staged first.
