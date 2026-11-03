# Subagent: Backend: T-076 block undated accept (Backend: T-076 block undated accept)

Source: `agent-aa7035960a904db9d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:59:13.489Z

You own board card T-076 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Rule D-041 in memory/ORCHESTRATOR_DECISIONS.md: accept, both single and batch, on an entry with no confirmed date returns 422 DATE_UNCONFIRMED and changes nothing. After confirm_date it accepts. The export treatment section must never contain "date not stated".

Implement it in app/backend (review.py and the batch path), update memory/contracts/api.md, and add unit tests. Check that golden or e2e flows that accept undated entries still make sense. If an e2e test accepts an undated entry, post a note naming it for qa/frontend.

Other backend workers are in pipeline.py and ingest.py (T-075, T-066), so stay out of those. Run `.venv/bin/python -m pytest -q tests/unit`. Commit with the pathspec or temp-index rule, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-076 in_review --agent backend`. Reply in 2 lines.

### User / tool · 2026-11-02T02:59:13.494Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:17.064Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B show T-076 | head -50; grep -n \"D-041\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -40; ls app/backend; cat .claude/agent-memory/backend/project_backend_conventions.md"
}
````

### User / tool · 2026-11-02T02:59:17.201Z

**tool result**
````
---
id: "T-076"
title: "Server: block accept of undated entries until date confirmed (D-041)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:59:07Z"
updated_at: "2026-11-02T02:59:09Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:59:09Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "POST accept (single and batch) on an entry with no confirmed date returns 422 DATE_UNCONFIRMED and changes nothing; after confirm_date it accepts; export treatment section never contains 'date not stated'; unit tests; api.md updated", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:59:09Z backend: claimed

## Handoff (filled when moving to in_review)

49:| D-041 | An entry with no confirmed date cannot be accepted into the letter (2026-11-02). Accept returns 422 `DATE_UNCONFIRMED` until the paralegal confirms a date (Dates to confirm) or the entry is moved to the notes block. The UI disables Accept with the reason shown. 'Date not stated' never appears in the treatment section. | A demand letter treatment line without a date is unusable and invites an adjuster challenge. | T-068 paralegal r2 major |
__init__.py
__pycache__
amounts.py
api.py
case_extras.py
confidence.py
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
review.py
schemas.py
sentences.py
split_llm.py
store.py
totals.py
why.py
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:18.987Z

**tool call — Bash**
````
{
 "command": "wc -l app/backend/review.py app/backend/export.py && grep -n \"accept\\|def \\|confirm_date\\|date not stated\\|Date not stated\" app/backend/review.py | head -120; grep -rn -i \"date not stated\" app/backend app/llm --include=*.py | head -20"
}
````

### User / tool · 2026-11-02T02:59:19.103Z

**tool result**
````
     351 app/backend/review.py
     575 app/backend/export.py
     926 total
3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). There is no bulk accept.
13:ACTIONS = ("accept", "dismiss", "reset", "edit")
19:    def __init__(self, status: int, code: str, detail: dict = None, message: str = ""):
24:def _now(now):
28:def _item(conn, case_id, item_id):
38:def _bad(msg, **detail):
42:def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
48:    if item["state"] == "rejected" and action in ("accept", "edit"):
51:    if action in ("accept", "dismiss", "reset"):
62:def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, body):
98:def _edit(conn, case_id, kind, item, body, call, t):
101:        raise _bad("A charge can only be accepted or dismissed.")
153:# ---------------------------------------------------------------- confirm_date
154:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
174:        DB.apply_review(conn, log_id, "confirm_date", now=t, case=case_id)
181:def _drop(conn, case_id, flag_id):
186:def _recompute_gaps(conn, case_id, t):
227:def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
230:    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
276:def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
332:def _upsert(conn, case_id, kind, item, t):
342:def judges_for(dollars, call, case_text):
348:def batch_apply(conn, case_id: str, item_id: str, action: str, now: float) -> None:
350:    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
app/backend/export.py:50:        return "date not stated"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:20.654Z

**tool call — Bash**
````
{
 "command": "sed -n 1,62p app/backend/review.py; sed -n 150,200p app/backend/review.py; sed -n 340,351p app/backend/review.py; sed -n 30,70p app/backend/export.py; grep -n \"batch\\|apply_review\\|batch_apply\" app/backend/api.py | head -30"
}
````

### User / tool · 2026-11-02T02:59:20.749Z

**tool result**
````
"""Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).

Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). There is no bulk accept.
Edit order: (1) structure, else 422 invalid_edit; (2) code token check; (3) judge 1 re-run. A token/judge objection saves nothing
and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
that cannot answer never blocks: the edit is saved as needs_review with JUDGE_UNAVAILABLE.
"""
import time

from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judges, store
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


def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
        raise _bad("That action is not allowed.")
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
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
        if ladder_verdict == "unavailable" else []


# ---------------------------------------------------------------- confirm_date
def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
    t = _now(now)
    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
    if row is None:
        raise ReviewError(404, "not_found", message="No such record.")
    rec = DB._decode(row)
    if rec["date_status"] != "ambiguous":
        raise _bad("Only a record whose date can be read two ways can be confirmed.")
    if date_iso not in (rec["date_candidates"] or []):
        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
    moved = None
    for e in DB.list_items(conn, case_id, "entry"):
        if record_id in (e["record_ids"] or []):
            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso)
            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
    removed += _recompute_gaps(conn, case_id, t)
    log_id = moved["id"] if moved else None
    if log_id:
        DB.apply_review(conn, log_id, "confirm_date", now=t, case=case_id)
    from app.backend import present
    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
            "removed_flag_ids": removed, "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}


def _drop(conn, case_id, flag_id):
    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
    return [flag_id] if cur.rowcount else []


def _recompute_gaps(conn, case_id, t):
    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
    and note; a changed one restarts as pending; one that no longer exists is dropped (ADR-002)."""
    from app.backend import pipeline as PL
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    backend = DB.get_case(conn, case_id).get("backend") or "code"
    new = {}
    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
        nos = f["record_nos"]
        state, codes = PL._compose_code(by_n, nos, list(f.get("reasons") or []), f["evidence"], case["raw_text"])
        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": f["evidence"], "record_nos": nos,
                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}


def judges_for(dollars, call, case_text):
    if call is None or not dollars:
        return {}
    return judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars], call=call, case_text=case_text)


def batch_apply(conn, case_id: str, item_id: str, action: str, now: float) -> None:
    """One audited status change for the batch endpoint (case_extras.apply_batch validates the whole batch first). review.py stays the only
    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
    DB.apply_review(conn, item_id, action, now=now, case=case_id)
                   "dismiss the entry to remove it; hedge sentences cannot be removed)")

IN = ("accepted", "edited")
OUT = ("dismissed", "rejected")

_ABBREV = {"approx", "dr", "mr", "mrs", "ms", "vs", "e.g", "i.e", "etc", "st", "no", "jr", "sr"}
_TYPE_RANK = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
_CONFLICT_SUB = {"accident_date": "accident date", "treatment_plan": "PT plan", "treatment_plan_vs_actual": "PT plan",
                 "accident_dates_differ": "accident date", "accident_date_after_treatment": "accident date"}
_ACCIDENT_SUBS = ("accident_date", "accident_dates_differ", "accident_date_after_treatment")
_COLLISION_RE = re.compile(r"rear-ended|collision|accident|crash|\bMV[AC]\b|struck|hit by", re.I)
# Order inside a merged flag line (most adjuster-actionable first); both the lexicon subtypes and the closed category names.
_ORDER = ["hedged_imaging", "speculative_language", "noncompliance", "missed_care", "patient_reported_onset", "patient_report",
          "temporal_after_gap", "new_onset", "accident_date_inconsistency", "accident_date_provenance"]
_FUTURE_RE = re.compile(r"^\s*recommend", re.I)  # extend by card (R-EX-4 section 7)


# ---------------------------------------------------------------- small formatting helpers
def _long_date(iso):
    if not iso:
        return "date not stated"
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def _money(cents):
    return f"${cents // 100:,}.{cents % 100:02d}"


def _money_short(cents, raw=""):
    if cents is None:
        return raw
    return f"${cents // 100:,}" if cents % 100 == 0 else _money(cents)


def _norm(s):
    return " ".join((s or "").split())


def _cap(s):
    return s[:1].upper() + s[1:]
469:            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:22.206Z

**tool call — Bash**
````
{
 "command": "grep -n \"_long_date\" app/backend/export.py; grep -n \"apply_batch\" -B3 -A50 app/backend/case_extras.py | head -120; grep -n \"date_status\\|date_iso\" app/db/db.py | head -30; grep -n \"export_routes\\|date_iso\" app/backend/export_routes.py | head"
}
````

### User / tool · 2026-11-02T02:59:22.312Z

**tool result**
````
48:def _long_date(iso):
175:        return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"
178:        return f"record {n} ({self.source(n)}, dated {_long_date(self.rec_date(n))})"
230:        out += [f"{_long_date(v.date_of(e))} — {v.source(e['record_no'])}", e["summary"], f'{v.source_prefix(e["record_no"])}"{e["excerpt"]}"', ""]
239:            out += [f"{v.source(n)}, {_long_date(v.rec_date(n))}: {_money(a['cents'])}",
277:        span = f"{days} days, {_long_date(f.get('from_date'))} to {_long_date(f.get('to_date'))}"
299:                tail += f" First recorded treatment: {_long_date(min(known))}."
516:    return f"{v.source(e['record_no'])}, {_long_date(v.date_of(e))}"
39-    return bad
40-
41-
42:def apply_batch(conn, case_id, body, now):
43-    """All or nothing. Validation covers every id before the first write; if a write still fails, the items already changed are put back."""
44-    action, ids = (body or {}).get("action"), (body or {}).get("item_ids")
45-    if action not in ("accept", "reset") or not isinstance(ids, list) or not ids or len(ids) > MAX_BATCH or \
46-            not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
47-        raise ValueError("bad_request")
48-    with _LOCK:
49-        bad = _check(conn, case_id, ids, action)
50-        if bad:
51-            raise BatchRefused(bad)
52-        done = []
53-        try:
54-            for i in ids:
55-                review.batch_apply(conn, case_id, i, action, now)
56-                done.append(i)
57-        except Exception:
58-            for i in reversed(done):          # compensate: each undo is itself an audited event
59-                review.batch_apply(conn, case_id, i, "reset", now)
60-            raise
61-    items = [{"id": i, "review_status": DB.get_item(conn, i, case_id)["review_status"]} for i in ids]
62-    return {"items": items, "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": []}
63-
64-
65-# ------------------------------------------------------------------ export config
66-def validate_config(b):
67-    """Returns the normalised config or raises ValueError. All keys optional; unknown keys refused."""
68-    if not isinstance(b, dict) or set(b) - set(EXPORT_KEYS):
69-        raise ValueError("invalid_edit")
70-    out = {}
71-    for k in ("exhibit", "bates_prefix"):
72-        v = b.get(k)
73-        if v is None or v == "":
74-            out[k] = None
75-        elif isinstance(v, str) and _LABEL.fullmatch(v):
76-            out[k] = v
77-        else:
78-            raise ValueError("invalid_edit")
79-    s = b.get("bates_start")
80-    if s is None:
81-        out["bates_start"] = None
82-    elif isinstance(s, int) and not isinstance(s, bool) and 0 <= s <= 99999999:
83-        out["bates_start"] = s
84-    else:
85-        raise ValueError("invalid_edit")
86-    return out
87-
88-
89-def get_config(conn, case_id) -> dict:
90-    cfg = (DB.get_case(conn, case_id).get("config") or {}).get("export") or {}
91-    return {k: cfg.get(k) for k in EXPORT_KEYS}
92-
--
109-        try:
110-            get_case(c, token)
111-            try:
112:                return apply_batch(c, token, b, now())
113-            except ValueError:
114-                raise ApiError(400, "bad_request", "Send an action (accept or reset) and a list of entry ids.") from None
115-            except BatchRefused as e:
116-                raise ApiError(422, "invalid_batch", "Only verified entries can be accepted together; nothing was changed.", {"rejected": e.rejected}) from None
117-        finally:
118-            c.close()
119-
120-    @app.get("/api/cases/{token}/export_config")
121-    def export_config_get(token: str):
122-        c = conn()
123-        try:
124-            get_case(c, token)
125-            return get_config(c, token)
126-        finally:
127-            c.close()
128-
129-    @app.put("/api/cases/{token}/export_config")
130-    async def export_config_put(token: str, request: Request):
131-        b = await body_of(request)
132-        c = conn()
133-        try:
134-            get_case(c, token)
135-            try:
136-                cfg = validate_config(b)
137-            except ValueError:
138-                raise ApiError(422, "invalid_edit", "Exhibit and prefix: up to 20 letters, digits, space . _ -; first number 0 to 99999999.") from None
139-            put_config(c, token, cfg)
140-            return get_config(c, token)
141-        finally:
142-            c.close()
143-
144-    @app.delete("/api/cases/{token}/export_config")
145-    def export_config_delete(token: str):
146-        c = conn()
147-        try:
148-            get_case(c, token)
149-            put_config(c, token, None)
150-            return get_config(c, token)
151-        finally:
152-            c.close()
3:The app factory (T-040) does `app.include_router(export_routes.router)` and registers the case loader once:
4:    export_routes.set_case_loader(fn)   # fn(token) -> case dict (see export.py docstring) or None for an unknown token
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:24.011Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p app/backend/case_extras.py; grep -n \"date_of\\|def rec_date\" -A8 app/backend/export.py | sed -n 1,40p; grep -n \"undated\\|date_iso\" app/backend/present.py | head -30; grep -n \"accept\" memory/contracts/api.md | head -30; grep -n \"DATE_UNCONFIRMED\\|date_unconfirmed\" -r app memory tests | head"
}
````

### User / tool · 2026-11-02T02:59:24.135Z

**tool result**
````
"""Batch accept of verified entries and per-case export config (D-031). Routes are added by api.create_app via add_routes().
Code only: nothing here asks a model anything, and the only review_status writer used is DB.apply_review (one event per item)."""
import re
import threading

from fastapi import Request

from app.backend import present, review
from app.db import db as DB

MAX_BATCH = 200
_LOCK = threading.Lock()
_LABEL = re.compile(r"[A-Za-z0-9 ._-]{1,20}")
EXPORT_KEYS = ("exhibit", "bates_prefix", "bates_start")


# ------------------------------------------------------------------ batch review
class BatchRefused(Exception):
    def __init__(self, rejected):
        super().__init__("invalid_batch")
        self.rejected = rejected


def _check(conn, case_id, ids, action):
    """[{id, reason}] for every id that may not be in this batch. Entries only; accept needs state verified and status pending."""
    bad = []
    for i in ids:
        try:
            kind, row = review._item(conn, case_id, i)
        except review.ReviewError:
            bad.append({"id": i, "reason": "not_found"})
            continue
        if kind != "entry":
            bad.append({"id": i, "reason": "not_an_entry"})
        elif action == "accept" and row["state"] != "verified":
            bad.append({"id": i, "reason": "not_verified"})
        elif action == "accept" and row["review_status"] != "pending":
            bad.append({"id": i, "reason": "not_pending"})
    return bad

146:        return self.date_of(item) or "9999-12-31"
147-
148:    def date_of(self, item):
149-        return item.get("date_iso") or (self.records.get(item["record_no"]) or {}).get("date_iso")
150-
151-    def source_prefix(self, n):
152-        """Citation prefix: 'Source [Ex. __ / Bates __]: ', or '..., p. N: ' when the record came from a PDF (D-031)."""
153-        pg = (self.records.get(n) or {}).get("page")
154-        head = SOURCE_PREFIX[:-2] if self.export_config is None else self._bracket(n)
155-        return head + (": " if pg is None else f", p. {pg}: ")
156-
--
171:    def rec_date(self, n):
172-        return (self.records.get(n) or {}).get("date_iso")
173-
174-    def cite(self, n):
175-        return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"
176-
177-    def cite_dated(self, n):
178-        return f"record {n} ({self.source(n)}, dated {_long_date(self.rec_date(n))})"
179-
--
230:        out += [f"{_long_date(v.date_of(e))} — {v.source(e['record_no'])}", e["summary"], f'{v.source_prefix(e["record_no"])}"{e["excerpt"]}"', ""]
231-    sents = v.narrative_sentences
232-    if sents:
233-        out += [SUMMARY_TITLE, ""] + [f"{x['text']} ({_cite_tail(v, x['entry_id'])})" for x in sents] + [""]
234-    charges = v.in_charges
235-    if charges:
236-        out += [CHARGES_TITLE, ""]
237-        for a in charges:
238-            n = a["record_no"]
--
516:    return f"{v.source(e['record_no'])}, {_long_date(v.date_of(e))}"
517-
518-
519-def _draft_paragraph(v):
520-    n = v.narrative
521-    if not n:
522-        return []
523-    live = {e["id"]: e for e in v.in_entries}
43:    return {**_common(row), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
120:                  key=lambda x: (confidence.sort_key(x[1]["state"]), rank[x[0]], x[1].get("date_iso") or "", x[1]["id"]))
132:    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
151:    undated = [e for e in live_e if e not in dated]
158:            "records": [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs], "undated_entries": undated, "entries": dated,
10:- Every item has `state` (system: `verified` | `needs_review` | `rejected`), `reasons[]` (codes), `why` (one template sentence), `review_status` (human: `pending` | `accepted` | `edited` | `dismissed`), and `ladder` (D.4).
25:| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
26:| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
27:| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
29:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset |
30:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items |
54:Request text is normalised first (CRLF and CR become LF; leading/trailing whitespace trimmed). **In demo mode the text is accepted only if its sha256 is in the recorded set (the sample and the golden cases); otherwise `409 demo_mode_unsupported_input` is returned before anything is stored** (D-020). Response 201 (all code: records, dates, duplicates, amounts, gap flags exist before any model call):
74:Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`.
149:    "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"},
206:    "counts": {"pending": 22, "accepted": 0, "edited": 0, "dismissed": 0, "needs_review": 7, "verified": 15, "rejected": 1},
212:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
243:  "events": [ {"action": "accept", "at": "2026-11-02T01:05:00Z"} ] }
251:  { "action": "accept" },
259:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; a rate can never become a charge); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. There is no bulk accept.
274:  "totals": { "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"} },
275:  "review": { "counts": {"pending": 21, "accepted": 0, "edited": 1, "dismissed": 0, "needs_review": 7, "verified": 15, "rejected": 1},
282:Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). No parameters. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
429:Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges stated in these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte.
440:  "events": [ { "id": "ev1", "item_id": "e2", "action": "accept", "at": "2026-11-02T01:05:00Z" } ],
448:  "events": [ { "id": "ev1", "item_id": "e2", "action": "accept", "before": {"review_status": "pending"}, "after": {"review_status": "accepted"}, "at": "2026-11-02T01:05:00Z" } ] }
453:`GET /api/cases` -> `{ "cases": [ { "token", "name", "status", "source", "record_count", "counts": {"pending","accepted","edited","dismissed","needs_review"}, "created_at" } ] }`, newest first, never record text.
memory/ORCHESTRATOR_DECISIONS.md:49:| D-041 | An entry with no confirmed date cannot be accepted into the letter (2026-11-02). Accept returns 422 `DATE_UNCONFIRMED` until the paralegal confirms a date (Dates to confirm) or the entry is moved to the notes block. The UI disables Accept with the reason shown. 'Date not stated' never appears in the treatment section. | A demand letter treatment line without a date is unusable and invites an adjuster challenge. | T-068 paralegal r2 major |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:27.940Z

**tool call — Bash**
````
{
 "command": "sed -n 140,160p app/backend/present.py; sed -n 455,490p app/backend/api.py; grep -n \"ReviewError\" app/backend/api.py | head; sed -n 70,80p memory/contracts/api.md; ls tests/unit | head -50; grep -rln \"accept\" tests/e2e tests/*.py 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T02:59:28.061Z

**tool result**
````
    return v


def case_view(conn, case_id, *, backend, models, demo_mode):
    case = DB.get_case(conn, case_id)
    raw = case["raw_text"]
    recs = list(_recs_by_id(conn, case_id).values())
    its = all_items(conn, case_id)
    ents = its["entry"]
    live_e = [e for e in ents if e["state"] != "rejected"]
    dated = sorted((e for e in live_e if e["date"] and (e["date_status"] in ("parsed", "confirmed", None))), key=lambda e: (e["date"], e["seq"] or 0))
    undated = [e for e in live_e if e not in dated]
    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
             "attempt": {"summary": x.get("summary"), "excerpt": x.get("excerpt")} if k == "entry" else {"text": x.get("text"), "excerpt": x.get("excerpt")},
             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected"]
    err = json.loads(case["error"]) if case.get("error") else None
    injected = [r["id"] for r in recs if r["injection_tag"]]
    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
            "records": [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs], "undated_entries": undated, "entries": dated,
            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "dates_to_confirm": dates_to_confirm(conn, case_id),
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

    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)

    @app.get("/api/cases/{token}/export")
    def export(token: str):
        from app.backend import export_routes as XR
        c = conn()
        try:
            get_case(c, token)
            case = store.export_case(c, token)
            ex = XR.export_payload(token, case)
            calls = DB.list_llm_calls(c, token)
            ok = ("accepted", "edited")
            tv = present.totals_view(c, token)
            ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
            ex["excluded"] = {"pending": case["pending_count"],
                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
                              "rejected": sum(1 for k in ("entry", "amount") for r in DB.list_items(c, token, k) if r["state"] == "rejected")}
148:    @app.exception_handler(review.ReviewError)
Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
Errors: `400 bad_request` with `detail.reason` = `pdf_no_text_layer` (looks scanned: refused before anything is stored, no model call), `pdf_unreadable`, `pdf_encrypted`; `413 input_too_large` (`pdf_too_large`).

## POST /api/cases/{token}/review/batch (D-031)
Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`.

## /api/cases/{token}/export_config (D-031)
`GET` returns `{"exhibit": null|string, "bates_prefix": null|string, "bates_start": null|int}`. `PUT` takes the same keys (all optional; omitted or empty means unset) and returns the stored config; `DELETE` clears it and returns the empty config. Validation: `exhibit` and `bates_prefix` up to 20 characters of `A-Za-z0-9 ._-`; `bates_start` an integer 0 to 99999999 (booleans and strings refused); unknown keys refused; any violation is `422 invalid_edit` and nothing changes. Effect on the export only: every letter citation `Source [Ex. __ / Bates __]` becomes `Source [Ex. <exhibit> / Bates <prefix><NNNN>]` with `NNNN` = first number + record number - 1, zero-padded to 4 digits (first number defaults to 1 when only a prefix is set; an unset part stays `__`). With no config the export is byte-identical to the golden. The internal notes never carry exhibit or Bates numbers.

## POST /api/cases/{token}/run
Request: `{ "confirm_rerun": false }`. Response 202:
__init__.py
__pycache__
_fakes.py
_golden.py
_pdf.py
test_amounts.py
test_api.py
test_api_routes.py
test_audited.py
test_boundaries.py
test_case_extras.py
test_confidence.py
test_conflicts.py
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
test_totals.py
tests/e2e/conftest.py
tests/e2e/test_local_mode.py
tests/e2e/test_charges.py
tests/e2e/test_letter_isolation.py
tests/e2e/test_edit.py
tests/e2e/test_review_matrix.py
tests/e2e/test_adversarial.py
tests/e2e/test_export_ui.py
tests/e2e/test_keyboard_mobile.py
tests/e2e/test_ladder_gate.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:28.368Z

**tool call — Bash**
````
{
 "command": "git status --short | head -20; git log --oneline | head -3"
}
````

### User / tool · 2026-11-02T02:59:28.482Z

**tool result**
````
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M app/backend/ingest.py
 M app/backend/pipeline.py
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
7763998 docs: D-041 undated entries need a confirmed date before accept (T-068 r2)
b6f3755 test(e2e): declare T-068 test ids
43fc69e chore(backend): re-record sample narrative fixtures against current summaries; eval report
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:32.373Z

**tool call — Bash**
````
{
 "command": "sed -n 25,50p app/backend/present.py; grep -n \"def dates_to_confirm\" -A15 app/backend/present.py; grep -n \"date_status\" app/backend/pipeline.py app/backend/dates.py app/backend/store.py | head -20; grep -n \"def apply_review\" -A25 app/db/db.py | head -50; grep -n \"manual_entry\" -A45 app/backend/review.py | grep -n \"date\" "
}
````

### User / tool · 2026-11-02T02:59:32.477Z

**tool result**
````
def _ladder(row):
    lad = dict(row.get("ladder") or {"item_id": row["id"]})
    lad["item_id"] = row["id"]
    lad["state"] = row["state"]
    lad["human"] = _human(row)
    return lad


def _common(row):
    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons")),
            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row)}


def entry_view(row, recs):
    r = recs.get((row["record_ids"] or [None])[0], {})
    ed = row.get("edited") or {}
    return {**_common(row), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
            "provider": row["provider"], "summary": ed.get("summary", row["summary"]), "ai_drafted": "summary" not in ed and not (row.get("ladder") or {}).get("entered_by"),
            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
            "excerpt": ed.get("excerpt", row["excerpt"]), "excerpt_start": ed.get("excerpt_start", row["excerpt_start"]),
            "excerpt_end": ed.get("excerpt_end", row["excerpt_end"]), "duplicate_note": None}


def amount_view(row, recs):
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
app/backend/pipeline.py:40:    dates = {rec_by_n[n].get("date_status") for n in nos if n in rec_by_n}
app/backend/pipeline.py:42:        ctx["date_status"] = "ambiguous"
app/backend/pipeline.py:76:        ctx = {"llm_split": True} if w["category"] == "llm_split" else {"injection": inj, "date_status": None if inj else "ambiguous"}
app/backend/pipeline.py:157:                          source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
app/backend/pipeline.py:278:    dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
179:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
180-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
181-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
182-    if action not in ACTIONS:
183-        raise ValueError(f"invalid review action {action!r}")
184-    table, row = _find(conn, item_id, case)
185-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
186-    status = ACTIONS[action] or row["review_status"]
187-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
188-    if action == "edit" and not new_edited:
189-        raise ValueError("edit requires a non-empty edited payload")
190-    after = {"review_status": status, "edited": new_edited}
191-    conn.execute("BEGIN")
192-    try:
193-        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
194-                     (status, _enc(new_edited), now, item_id, row["case_id"]))
195-        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
196-                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
197-        conn.execute("COMMIT")
198-    except Exception:
199-        conn.execute("ROLLBACK")
200-        raise
201-    return get_item(conn, item_id, row["case_id"])
202-
203-
204-def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
25:251-    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call, body or {})
31:257-                              "date_provider_from_header": True},
36:262-        "id": eid, "record_ids_json": [record_id], "seq": rec["seq"], "date_iso": rec.get("date_iso"), "provider": rec["source"],
66:292-    DB.update_case(conn, case_id, config_json=cfg)
68:294-    DB.update_item(conn, entry_id, now=t, case=case_id, record_ids_json=[i for i in ids if i != record_id])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:38.868Z

**tool call — Bash**
````
{
 "command": "sed -n 140,160p app/backend/api.py; sed -n 1,60p tests/unit/test_case_extras.py; grep -n \"undated\\|ambiguous\" tests/unit/test_review_rules.py tests/unit/test_case_extras.py | head -20"
}
````

### User / tool · 2026-11-02T02:59:38.963Z

**tool result**
````
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
    async def _http_error(_, e):
        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
        return JSONResponse({"error": {"code": code, "message": code.replace("_", " "), "detail": {}}}, status_code=e.status_code)

    @app.exception_handler(Exception)
    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log
        log.error("unhandled %s", type(e).__name__)
        return JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
"""Batch accept of verified entries (atomic, entries only) and per-case export config (D-031; T-055, T-058)."""
import time
import pytest
from fastapi.testclient import TestClient
from app.backend import export as X
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.test_api_routes import wait_ready, run_case
from tests.unit.test_export import build_case


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "x.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def items(c, tok):
    v = c.get(f"/api/cases/{tok}").json()
    return v


def statuses(db, tok):
    conn = DB.connect(db)
    out = {k: {i["id"]: (i["review_status"], i["state"]) for i in DB.list_items(conn, tok, k)} for k in ("entry", "amount", "flag")}
    conn.close()
    return out


def test_batch_accepts_verified_entries_only_and_logs_one_event_each(env):
    db, c = env
    tok = run_case(c)
    st = statuses(db, tok)
    ver = [i for i, (rs, s) in st["entry"].items() if s == "verified" and rs == "pending"]
    assert len(ver) >= 7
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ver})
    assert r.status_code == 200 and [x["review_status"] for x in r.json()["items"]] == ["accepted"] * len(ver)
    assert {"totals", "review", "warnings"} <= set(r.json())
    conn = DB.connect(db)
    ev = [e for e in DB.list_events(conn, tok) if e["action"] == "accept"]
    assert sorted(e["item_id"] for e in ev) == sorted(ver)
    st2 = statuses(db, tok)
    assert all(rs == "pending" for rs, _ in list(st2["amount"].values()) + list(st2["flag"].values()))
    u = c.post(f"/api/cases/{tok}/review/batch", json={"action": "reset", "item_ids": ver})
    assert u.status_code == 200 and all(x["review_status"] == "pending" for x in u.json()["items"])


def test_batch_refuses_amounts_flags_and_unverified_and_applies_nothing(env):
    db, c = env
    tok = run_case(c)
    st = statuses(db, tok)
    ver = [i for i, (rs, s) in st["entry"].items() if s == "verified"]
    nonver = [i for i, (rs, s) in st["entry"].items() if s != "verified"]
    amount, flag = next(iter(st["amount"])), next(iter(st["flag"]))
    bad = [amount, flag] + nonver[:1]
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ver + bad})
tests/unit/test_review_rules.py:25:    return [e for e in out["entries"] + out.get("undated_entries", []) if f"r{n}" in e["record_ids"]][0]["id"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:40.923Z

**tool call — Bash**
````
{
 "command": "grep -rn \"confirm_date\" tests/unit | head -15; grep -rln \"undated\\|confirm_date\\|dates_to_confirm\\|date not stated\" tests evals 2>/dev/null | head -20"
}
````

### User / tool · 2026-11-02T02:59:41.035Z

**tool result**
````
tests/unit/test_review_rules.py:69:def test_confirm_date_on_parsed_record_is_422_invalid_edit(tmp_path):
tests/unit/test_review_rules.py:70:    """R-RV-2: confirm_date on a parsed date -> 422 invalid_edit."""
tests/unit/test_review_rules.py:73:        RV.confirm_date(conn, cid, out["records"][0]["id"], "2026-01-09")
tests/unit/test_review_rules.py:76:def test_confirm_date_non_candidate_is_422_date_invalid(tmp_path):
tests/unit/test_review_rules.py:81:        RV.confirm_date(conn, cid, rid, "2026-06-06")
tests/unit/test_review_rules.py:83:    assert RV.confirm_date(conn, cid, rid, "2026-05-04")["record"]["date_status"] == "confirmed"
tests/unit/test_t033_backend.py:67:def test_confirm_date_recompute_keeps_unchanged_status():
tests/unit/test_gaps.py:38:    """R-IN-5: a record with date None is excluded; recomputing after confirm_date (date set) includes it."""
tests/unit/test_api_routes.py:1:"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
tests/unit/test_api_routes.py:142:def test_confirm_date_case_01(env):
tests/unit/test_api_routes.py:148:    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": "2026-06-06"}).status_code == 422
tests/unit/test_api_routes.py:149:    r = c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]})
tests/unit/test_api_routes.py:155:    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]}).status_code == 422
tests/unit/test_api_routes.py:156:    assert any(e["action"] == "confirm_date" for e in c.get(f"/api/cases/{t}/audit").json()["events"])
tests/unit/test_t033_backend.py
tests/unit/_fakes.py
tests/unit/test_eval_runner.py
tests/unit/test_t037_backend.py
tests/unit/test_api_routes.py
tests/unit/test_review_rules.py
tests/unit/test_gaps.py
tests/e2e/conftest.py
evals/reports/m3-sensors.md
tests/e2e/test_input.py
evals/run.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:42.603Z

**tool call — Bash**
````
{
 "command": "sed -n 1,30p tests/unit/test_review_rules.py; sed -n 60,90p tests/unit/test_review_rules.py; sed -n 100,160p tests/unit/test_api_routes.py; grep -n \"undated\\|date not stated\\|ambiguous\" tests/e2e/*.py | head"
}
````

### User / tool · 2026-11-02T02:59:42.712Z

**tool result**
````
"""Review/edit rules (backend/review.py). R-RV-2 (D-010, D-012), R-RV-3, R-CH-5, R-CH-7, ADR-005 edit re-check order; fake judge only."""
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
        assert e.value.code == "invalid_edit"

def test_excerpt_dropping_hedge_is_422(tmp_path):
    """R-RV-2 / R-TL-8: re-selecting entry 8's excerpt without the hedge sentences -> 422 invalid_edit."""
    conn, cid, out = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, ent(out, 8), dict(action="edit", edits=dict(excerpt="C5-C6 disc protrusion with mild right foraminal narrowing.")), call=judge("supported"))
    assert e.value.code == "invalid_edit"

def test_confirm_date_on_parsed_record_is_422_invalid_edit(tmp_path):
    """R-RV-2: confirm_date on a parsed date -> 422 invalid_edit."""
    conn, cid, out = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.confirm_date(conn, cid, out["records"][0]["id"], "2026-01-09")
    assert (e.value.status, e.value.code) == (422, "invalid_edit")

def test_confirm_date_non_candidate_is_422_date_invalid(tmp_path):
    """R-IN-5: case_01 record 8 confirm with a date that is not one of the two code readings -> 422 date_invalid; a candidate -> 200."""
    conn, cid, out = seeded(tmp_path, "case_01_date_formats")
    rid = [r for r in out["records"] if r["seq"] == 8][0]["id"]
    with pytest.raises(RV.ReviewError) as e:
        RV.confirm_date(conn, cid, rid, "2026-06-06")
    assert (e.value.status, e.value.code) == (422, "date_invalid")
    assert RV.confirm_date(conn, cid, rid, "2026-05-04")["record"]["date_status"] == "confirmed"

@pytest.mark.parametrize("confirm", [False, True])
def test_added_dollar_is_a_hard_422_even_with_confirm_and_saves_nothing(tmp_path, confirm):
    """D-034 (R-RV-3): summary edited to add '$9,000' -> 422 invalid_edit, no override via confirm_warnings; the item is unchanged."""
    conn, cid, out = seeded(tmp_path); eid = ent(out, 5)
    before = DB.get_item(conn, eid)
    with pytest.raises(RV.ReviewError) as e:
    w = c.get(f"/api/cases/{tok}/items/{g['entries'][0]['id']}").json()
    assert w["item"]["ladder"]["backend"] == "fixture" and w["calls"] and w["source"][0]["highlight_start"] is not None
    assert "user_text" not in w["calls"][0]
    assert c.get(f"/api/cases/{tok}/items/zzz").status_code == 404


def test_review_http_matrix_and_decisions_survive_restart(env, tmp_path):
    db, c = env
    tok = run_case(c)
    g = c.get(f"/api/cases/{tok}").json()
    e5 = [e for e in g["entries"] if e["provider"].startswith("Capital PT, visit 8")][0]["id"]
    ok = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "accept"})
    assert ok.status_code == 200 and ok.json()["item"]["review_status"] == "accepted" and ok.json()["review"]["counts"]["accepted"] == 1
    bad = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "edit", "edits": {"date": "2026-01-01"}})
    assert bad.status_code == 422 and bad.json()["error"]["code"] == "invalid_edit"
    nc = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "edit", "edits": {"summary": "Visit 8: pain 4/10, improving; billed $9,000."}})
    assert nc.status_code == 422 and nc.json()["error"]["code"] == "invalid_edit"          # D-034: a figure not in the quote is never saved
    assert c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "bulk"}).status_code == 422
    c2 = TestClient(create_app(db, static_dir=str(tmp_path)))           # restart: the decision is still there
    assert [e for e in c2.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == e5][0]["review_status"] == "accepted"


def test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode(env):
    _, c = env
    tok = run_case(c)
    e5 = [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["provider"].startswith("Capital PT, visit 8")][0]["id"]
    r = c.post(f"/api/cases/{tok}/items/{e5}/review", json={"action": "edit", "edits": {"summary": "Visit 8: pain 4/10 and improving, per the paralegal."}})
    j = r.json()
    assert r.status_code == 200 and j["item"]["review_status"] == "edited" and j["item"]["state"] == "needs_review"
    assert j["warnings"][0]["code"] == "JUDGE_UNAVAILABLE" and j["item"]["edited"]["original_summary"]


def test_charge_cannot_be_edited_and_rerun_needs_confirm(env):
    _, c = env
    tok = run_case(c)
    a = c.get(f"/api/cases/{tok}").json()["amounts"][0]["id"]
    assert c.post(f"/api/cases/{tok}/items/{a}/review", json={"action": "edit", "edits": {"value": 1}}).status_code == 422
    assert c.post(f"/api/cases/{tok}/items/{a}/review", json={"action": "accept"}).status_code == 200
    r = c.post(f"/api/cases/{tok}/run", json={})
    assert r.status_code == 409 and r.json()["error"]["code"] == "needs_confirm"


def test_confirm_date_case_01(env):
    _, c = env
    t = run_case(c, G.raw("case_01_date_formats"))
    g = c.get(f"/api/cases/{t}").json()
    rec = [r for r in g["records"] if r["date_status"] == "ambiguous"][0]
    gaps_before = sorted(f["id"] for f in g["flags"] if f["type"] == "gap")
    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": "2026-06-06"}).status_code == 422
    r = c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]})
    assert r.status_code == 200 and r.json()["record"]["date_status"] == "confirmed"
    g2 = c.get(f"/api/cases/{t}").json()
    assert g2["dates_to_confirm"] == [] and not [e for e in g2["undated_entries"] if rec["id"] in e["record_ids"]]
    if not rec["encounter"]:
        assert sorted(f["id"] for f in g2["flags"] if f["type"] == "gap") == gaps_before
    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]}).status_code == 422
    assert any(e["action"] == "confirm_date" for e in c.get(f"/api/cases/{t}/audit").json()["events"])


def test_export_equals_golden_when_everything_accepted(env):
    _, c = env
tests/e2e/conftest.py:9:  T-068 (undated-entry and orphan-date branches): date-to-confirm-item (one row per undated record in dates-to-confirm, carries data-record-id), date-to-confirm-excerpt (its verbatim excerpt),
tests/e2e/test_input.py:33:def test_ambiguous_date_goes_to_dates_to_confirm(page):
tests/e2e/test_input.py:34:    """R-IN-3/R-IN-5, undated-entry branch (T-068): case_01 record 8 (04/05/2026) has an undated entry. It is listed ONCE, in
tests/e2e/test_input.py:38:    assert page.get_by_test_id("date-to-confirm-item").count() == 0, "this case has an undated entry, so the no-entry row must not render"
tests/e2e/test_input.py:52:        for k in ("entries", "undated_entries", "tray"):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:50.287Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/review.py'\ns=open(p).read()\ns=s.replace('''def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:''','''def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:\n    \"\"\"D-041: an entry whose date is not confirmed (ambiguous, missing, or no date at all) cannot go into the letter. Same rule as\n    present.case_view uses to put an entry under `undated_entries`: date_iso set and the record's date_status parsed or confirmed.\"\"\"\n    if kind != \"entry\":\n        return False\n    if not item.get(\"date_iso\"):\n        return True\n    rid = (item.get(\"record_ids\") or [None])[0]\n    row = conn.execute(\"SELECT date_status FROM records WHERE id=? AND case_id=?\", (rid, case_id)).fetchone()\n    return bool(row) and row[\"date_status\"] not in (\"parsed\", \"confirmed\", None)\n\n\ndef _date_unconfirmed_error():\n    return ReviewError(422, \"DATE_UNCONFIRMED\", message=\"Confirm this entry's date first (Dates to confirm). An entry with no confirmed date \"\n                       \"cannot be accepted into the letter.\")\n\n\ndef apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:''',1)\ns=s.replace('''    warnings = []\n    if action in (\"accept\", \"dismiss\", \"reset\"):\n        DB.apply_review(''','''    if action in (\"accept\", \"edit\") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept\n        raise _date_unconfirmed_error()\n    warnings = []\n    if action in (\"accept\", \"dismiss\", \"reset\"):\n        DB.apply_review(''',1)\nopen(p,'w').write(s)\n\np='app/backend/case_extras.py'\ns=open(p).read()\ns=s.replace('''        elif action == \"accept\" and row[\"review_status\"] != \"pending\":\n            bad.append({\"id\": i, \"reason\": \"not_pending\"})''','''        elif action == \"accept\" and row[\"review_status\"] != \"pending\":\n            bad.append({\"id\": i, \"reason\": \"not_pending\"})\n        elif action == \"accept\" and review.date_unconfirmed(conn, case_id, kind, row):\n            bad.append({\"id\": i, \"reason\": \"date_unconfirmed\"})''',1)\ns=s.replace('''            except BatchRefused as e:\n                raise ApiError(422, \"invalid_batch\",''','''            except BatchRefused as e:\n                if any(r[\"reason\"] == \"date_unconfirmed\" for r in e.rejected):     # D-041: same code as a single accept\n                    raise ApiError(422, \"DATE_UNCONFIRMED\", \"Confirm the date of every undated entry first (Dates to confirm); nothing was changed.\", {\"rejected\": e.rejected}) from None\n                raise ApiError(422, \"invalid_batch\",''',1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"ambiguous\" app/backend/export.py | head; sed -n 200,232p app/backend/export.py"
}
````

### User / tool · 2026-11-02T02:59:50.412Z

**tool result**
````
    exc, raw = a.get("excerpt") or "", a.get("raw") or ""
    i = exc.find(raw) if raw else -1
    if i >= 0:
        for st, en in _sentence_spans(exc):
            if st <= i < en:
                exc = exc[st:en]
                break
    return v.quote(a["record_no"], exc)


def basis_hash(entry: dict) -> str:
    """What a narrative sentence was drafted from: if an entry's summary or quote changes afterwards, its sentences leave the letter."""
    import hashlib
    return hashlib.sha256(f"{entry['summary']}\x1f{entry['excerpt']}".encode("utf-8")).hexdigest()[:16]


def _status(item):
    s = item.get("review_status")
    return "in" if s in IN else "out" if s in OUT else "pending"


# ---------------------------------------------------------------- letter (takes no flags)
def build_letter(case: dict) -> str:
    """The treatment section. Deliberately has no flags parameter (R-EX-1): flag content cannot reach the letter."""
    return _letter(_View(case))


def _letter(v):
    out = [LETTER_TITLE, ""]
    for e in v.in_entries:
        out += [f"{_long_date(v.date_of(e))} — {v.source(e['record_no'])}", e["summary"], f'{v.source_prefix(e["record_no"])}"{e["excerpt"]}"', ""]
    sents = v.narrative_sentences
    if sents:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:53.122Z

**tool call — Bash**
````
{
 "command": "grep -n \"in_entries\\|def narrative_sentences\" -B1 -A6 app/backend/export.py | sed -n 1,80p; grep -n \"def _notes\" -A40 app/backend/export.py | head -80"
}
````

### User / tool · 2026-11-02T02:59:53.220Z

**tool result**
````
127-    @property
128:    def in_entries(self):
129-        return [e for e in self.entries if _status(e) == "in" and self.verbatim(e)]
130-
131-    @property
132:    def narrative_sentences(self):
133-        """Sentences of an ACCEPTED draft paragraph whose cited entry is still in the letter and unchanged since the draft."""
134-        n = self.narrative
135-        if not n or n.get("status") != "accepted":
136-            return []
137:        live = {e["id"]: e for e in self.in_entries}
138-        return [s for s in n.get("sentences", []) if s["entry_id"] in live and (n.get("basis") or {}).get(s["entry_id"]) == basis_hash(live[s["entry_id"]])]
139-
140-    @property
141-    def in_charges(self):
142-        return [a for a in self.amounts if a["cls"] == "charge" and a.get("cents") is not None
143-                and _status(a) == "in" and self.verbatim(a)]
--
228-    out = [LETTER_TITLE, ""]
229:    for e in v.in_entries:
230-        out += [f"{_long_date(v.date_of(e))} — {v.source(e['record_no'])}", e["summary"], f'{v.source_prefix(e["record_no"])}"{e["excerpt"]}"', ""]
231-    sents = v.narrative_sentences
232-    if sents:
233-        out += [SUMMARY_TITLE, ""] + [f"{x['text']} ({_cite_tail(v, x['entry_id'])})" for x in sents] + [""]
234-    charges = v.in_charges
235-    if charges:
--
340-    live = sorted((f for f in flags if _status(f) != "out"), key=lambda f: _TYPE_RANK.get(f.get("type"), 9))
341:    for e in v.in_entries:
342-        n, exc = e["record_no"], e["excerpt"]
343-        spans, keep, hits = _sentence_spans(exc), set(), []
344-        for f in live:
345-            if f.get("type") == "gap" and n in {x["record_no"] for x in f.get("evidence", [])}:
346-                hits.append(_flag_label(f)) if _flag_label(f) not in hits else None   # a gap bounds these records' entries
347-            if f.get("type") == "conflict" and f.get("subtype") in _ACCIDENT_SUBS and not any(
--
435-    names = []
436:    for e in v.in_entries:
437-        p = _provider(v.source(e["record_no"]))
438-        if p and p not in paid and p not in names:
439-            names.append(p)
440-    if not names:
441-        return ["- none"]
442-    return ["- " + _terminate("; ".join(p + (" (itemized ledger)" if p in rated else "") for p in names))]
--
445-def _reconcile(v):
446:    in_letter = {e["record_no"] for e in v.in_entries}
447-    lines = []
448-    for r in sorted(v.records.values(), key=lambda r: (r.get("date_iso") or "9999", r["n"])):
449-        n = r["n"]
450-        if n in in_letter:
451-            continue
452-        ents = [e for e in v.entries if e["record_no"] == n]
--
522-        return []
523:    live = {e["id"]: e for e in v.in_entries}
524-    st = n.get("status", "pending")
525-    lines = ["", "DRAFT TREATMENT PARAGRAPH (AI-drafted from accepted entries; each sentence cites one entry and passed code checks and the second check)"]
526-    lines.append({"pending": "- Not in the letter until you accept it.", "dismissed": "- Dismissed; not in the letter.",
527-                  "accepted": "- Accepted: included in the letter as TREATMENT SUMMARY."}.get(st, "- Not in the letter."))
528-    for s in n.get("sentences", []):
529-        e = live.get(s["entry_id"])
--
563-    notes = _notes(v)
564:    in_letter = {e["record_no"] for e in v.in_entries}
565-    pend = _pending(v)
566-    counts = {  # R-EX-5 count line: shown by the UI outside both blocks, never inside them
567:        "entries": len(v.in_entries),
568-        "charges": len(v.in_charges),
569-        "flags_in_notes": sum(1 for f in v.flags if _status(f) == "in"),
570-        "records_in_letter": len(in_letter),
571-        "records_total": len(v.records),
572-        "pending": len(pend),
573-        "pending_flags": sum(1 for f in v.flags if _status(f) == "pending"),
538:def _notes(v):
539-    accepted = [f for f in v.flags if _status(f) == "in"]
540-    dismissed = [f for f in v.flags if f.get("review_status") in OUT]
541-    pending = _pending(v)
542-    sec = [
543-        NOTES_TITLE, "",
544-        AI_LINE.format(n=len(pending)), "",
545-        "FLAGS ACCEPTED", *_flag_block(v, accepted), "",
546-        "FLAGS DISMISSED", *_flag_block(v, dismissed), "",
547-        FLAGGED_HEADING, *_flagged_language(v, v.flags), "",
548-        "AMOUNTS NOT TOTALED", *_amounts_not_totaled(v), "",
549-        "DAMAGES MENTIONS (not charges)", *_damages(v), "",
550-        "FUTURE TREATMENT RECOMMENDED (no cost stated)", *_future(v), "",
551-        "BILLS TO REQUEST (entry in the letter, no accepted charge)", *_bills(v), "",
552-        "RECORDS NOT IN THE TREATMENT SECTION", *_reconcile(v), "",
553-        "EDITED ITEMS", *_edited(v), "",
554-        "PENDING ITEMS NOT INCLUDED", *(pending or ["- none"]),
555-        *_draft_paragraph(v),
556-    ]
557-    return "\n".join(sec)
558-
559-
560-def build_export(case: dict) -> dict:
561-    """Pure function: reviewed items in, two text blocks out. Deterministic; no I/O; no flags reach the letter."""
562-    v = _View(case)
563-    notes = _notes(v)
564-    in_letter = {e["record_no"] for e in v.in_entries}
565-    pend = _pending(v)
566-    counts = {  # R-EX-5 count line: shown by the UI outside both blocks, never inside them
567-        "entries": len(v.in_entries),
568-        "charges": len(v.in_charges),
569-        "flags_in_notes": sum(1 for f in v.flags if _status(f) == "in"),
570-        "records_in_letter": len(in_letter),
571-        "records_total": len(v.records),
572-        "pending": len(pend),
573-        "pending_flags": sum(1 for f in v.flags if _status(f) == "pending"),
574-    }
575-    return {"letter_text": _letter(v), "internal_notes_text": notes, "counts": counts}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:59:55.412Z

**tool call — Bash**
````
{
 "command": "sed -n 445,490p app/backend/export.py; grep -n \"def verbatim\" -A8 app/backend/export.py; grep -n \"date_status\" app/backend/store.py | head"
}
````

### User / tool · 2026-11-02T02:59:55.512Z

**tool result**
````
def _reconcile(v):
    in_letter = {e["record_no"] for e in v.in_entries}
    lines = []
    for r in sorted(v.records.values(), key=lambda r: (r.get("date_iso") or "9999", r["n"])):
        n = r["n"]
        if n in in_letter:
            continue
        ents = [e for e in v.entries if e["record_no"] == n]
        if r.get("could_not_process") or r.get("status") in ("failed", "could_not_process"):
            why = "could not process"
        elif any(_status(e) == "in" and not v.verbatim(e) for e in ents):
            why = "excerpt not found in record, not exported"
        elif any(_status(e) == "pending" for e in ents):
            why = "not reviewed"
        elif any(e.get("review_status") == "rejected" for e in ents):
            why = "rejected"
        elif ents:
            why = "dismissed"
        else:
            why = r.get("reason") or "no entry"
        lines.append(f"- {_cap(v.cite(n))} — {why}")
    return lines or [f"- none ({len(v.records)} of {len(v.records)} records included)"]


def _was_edited(e):
    """T-069: an entry stays an edited item after the paralegal accepts it (accept keeps the edit payload and only flips the status),
    so edited-ness is the status OR a stored original that differs from the exported text. Out-of-letter entries are not listed."""
    if e.get("review_status") == "edited":
        return True
    if _status(e) != "in":
        return False
    return ((e.get("original_summary") is not None and e["original_summary"] != e["summary"])
            or (e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]))


def _edited(v):
    out = []
    for e in v.entries:
        if e.get("entered_by_reviewer") and _status(e) == "in":
            out.append(f'- {_cap(v.cite(e["record_no"]))}: entered by reviewer (the AI did not draft this entry); summary "{e["summary"]}"'
                       + (f'; paralegal confirmed keep my wording (reviewer override: {", ".join(e["override_reasons"])})' if e.get("override_reasons") else "") + ".")
        if not _was_edited(e):
            continue
        bits = []
        if e.get("original_summary") is not None and e["original_summary"] != e["summary"]:
            bits.append(f'summary was "{e["original_summary"]}", now "{e["summary"]}"')
123:    def verbatim(self, item):
124-        """The quoted excerpt must still be a substring of its record (whitespace-normalized); else it never ships."""
125-        return _norm(item.get("excerpt")) in _norm(self.text(item["record_no"]))
126-
127-    @property
128-    def in_entries(self):
129-        return [e for e in self.entries if _status(e) == "in" and self.verbatim(e)]
130-
131-    @property
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:00:00.243Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/export.py'\ns=open(p).read()\ns=s.replace('''        return [e for e in self.entries if _status(e) == \"in\" and self.verbatim(e)]\n''','''        \"\"\"D-041: an entry with no confirmed date never reaches the letter, even if it was accepted before this rule (it is listed in the\n        internal notes as 'date not confirmed').\"\"\"\n        return [e for e in self.entries if _status(e) == \"in\" and self.verbatim(e) and self.date_of(e)]\n''',1)\ns=s.replace('''        elif any(_status(e) == \"pending\" for e in ents):\n            why = \"not reviewed\"''','''        elif any(_status(e) == \"in\" and not v.date_of(e) for e in ents):\n            why = \"date not confirmed, not exported\"\n        elif any(_status(e) == \"pending\" for e in ents):\n            why = \"not reviewed\"''',1)\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T03:00:19.780Z

**tool result**
````
........................................................................ [  7%]
........................................................................ [ 15%]
........................................................................ [ 22%]
........................................................................ [ 30%]
........................................................................ [ 37%]
........................................................................ [ 45%]
........................................................................ [ 52%]
........................................................................ [ 60%]
........................................................................ [ 67%]
........................................................................ [ 75%]
........................................................................ [ 83%]
........................................................................ [ 90%]
........................................................................ [ 98%]
.................                                                        [100%]
953 passed in 18.75s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:00:32.916Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/test_date_unconfirmed.py <<'EOF'\n\"\"\"D-041 (T-076): an entry with no confirmed date cannot be accepted (single, edit, batch) until confirm_date; the letter never says 'date not stated'.\"\"\"\nimport pytest\nfrom fastapi.testclient import TestClient\nfrom app.backend import export as X\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit.test_api_routes import run_case\n\n\n@pytest.fixture\ndef env(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    db = str(tmp_path / \"x.sqlite\")\n    return db, TestClient(create_app(db, static_dir=str(tmp_path)))\n\n\ndef undated_case(c):\n    t = run_case(c, G.raw(\"case_01_date_formats\"))\n    g = c.get(f\"/api/cases/{t}\").json()\n    rec = [r for r in g[\"records\"] if r[\"date_status\"] == \"ambiguous\"][0]\n    und = [e for e in g[\"undated_entries\"] if rec[\"id\"] in e[\"record_ids\"]]\n    assert und, \"case_01 must have an undated entry for the ambiguous record\"\n    return t, g, rec, und[0]\n\n\ndef snapshot(db, t):\n    conn = DB.connect(db)\n    out = {k: [(i[\"id\"], i[\"review_status\"]) for i in DB.list_items(conn, t, k)] for k in (\"entry\", \"amount\", \"flag\")}\n    n = len(DB.list_events(conn, t))\n    conn.close()\n    return out, n\n\n\ndef test_single_accept_and_edit_on_undated_entry_is_422_and_changes_nothing(env):\n    db, c = env\n    t, g, rec, e = undated_case(c)\n    before = snapshot(db, t)\n    r = c.post(f\"/api/cases/{t}/items/{e['id']}/review\", json={\"action\": \"accept\"})\n    assert r.status_code == 422 and r.json()[\"error\"][\"code\"] == \"DATE_UNCONFIRMED\"\n    r = c.post(f\"/api/cases/{t}/items/{e['id']}/review\", json={\"action\": \"edit\", \"edits\": {\"summary\": e[\"summary\"] + \" \"}})\n    assert r.status_code == 422 and r.json()[\"error\"][\"code\"] == \"DATE_UNCONFIRMED\"\n    assert snapshot(db, t) == before\n    # dismiss and reset stay available: the entry can be moved out of the letter\n    assert c.post(f\"/api/cases/{t}/items/{e['id']}/review\", json={\"action\": \"dismiss\"}).status_code == 200\n\n\ndef test_batch_with_one_undated_entry_is_422_and_applies_nothing(env):\n    db, c = env\n    t, g, rec, e = undated_case(c)\n    dated_ok = [x[\"id\"] for x in g[\"entries\"] if x[\"state\"] == \"verified\" and x[\"review_status\"] == \"pending\"][:2]\n    assert dated_ok\n    before = snapshot(db, t)\n    r = c.post(f\"/api/cases/{t}/review/batch\", json={\"action\": \"accept\", \"item_ids\": dated_ok + [e[\"id\"]]})\n    assert r.status_code == 422 and r.json()[\"error\"][\"code\"] == \"DATE_UNCONFIRMED\"\n    assert {\"id\": e[\"id\"], \"reason\": \"date_unconfirmed\"} in r.json()[\"error\"][\"detail\"][\"rejected\"] or \\\n        e[\"state\"] != \"verified\"          # a needs_review entry is refused as not_verified first; the code is still DATE_UNCONFIRMED only for verified ones\n    assert snapshot(db, t) == before\n\n\ndef test_accept_works_after_confirm_date_and_letter_has_no_date_not_stated(env):\n    db, c = env\n    t, g, rec, e = undated_case(c)\n    assert c.post(f\"/api/cases/{t}/items/{e['id']}/review\", json={\"action\": \"accept\"}).status_code == 422\n    assert c.post(f\"/api/cases/{t}/records/{rec['id']}/confirm_date\", json={\"date\": rec[\"date_candidates\"][0]}).status_code == 200\n    r = c.post(f\"/api/cases/{t}/items/{e['id']}/review\", json={\"action\": \"accept\"})\n    assert r.status_code == 200 and r.json()[\"item\"][\"review_status\"] == \"accepted\"\n    letter = c.get(f\"/api/cases/{t}/export\").json()[\"letter_text\"]\n    assert \"date not stated\" not in letter.lower()\n\n\ndef test_export_never_puts_an_undated_accepted_entry_in_the_letter(env):\n    \"\"\"Defence in depth: an entry accepted before D-041 (or by a direct DB write) still stays out of the treatment section.\"\"\"\n    db, c = env\n    t, g, rec, e = undated_case(c)\n    conn = DB.connect(db)\n    DB.apply_review(conn, e[\"id\"], \"accept\", now=1.0, case=t)        # bypasses the HTTP rule on purpose\n    conn.close()\n    ex = c.get(f\"/api/cases/{t}/export\").json()\n    assert \"date not stated\" not in ex[\"letter_text\"].lower()\n    assert \"date not confirmed\" in ex[\"internal_notes_text\"]\n\n\ndef test_confirm_date_then_batch_accepts(env):\n    db, c = env\n    t, g, rec, e = undated_case(c)\n    c.post(f\"/api/cases/{t}/records/{rec['id']}/confirm_date\", json={\"date\": rec[\"date_candidates\"][0]})\n    g2 = c.get(f\"/api/cases/{t}\").json()\n    moved = [x for x in g2[\"entries\"] if x[\"id\"] == e[\"id\"]][0]\n    if moved[\"state\"] == \"verified\":\n        r = c.post(f\"/api/cases/{t}/review/batch\", json={\"action\": \"accept\", \"item_ids\": [e[\"id\"]]})\n        assert r.status_code == 200 and r.json()[\"items\"][0][\"review_status\"] == \"accepted\"\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_date_unconfirmed.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T03:00:35.407Z

**tool result**
````
.F...                                                                    [100%]
=================================== FAILURES ===================================
_________ test_batch_with_one_undated_entry_is_422_and_applies_nothing _________

env = ('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-2390/test_batch_with_one_undated_en0/x.sqlite', <starlette.testclient.TestClient object at 0x10ad324e0>)

    def test_batch_with_one_undated_entry_is_422_and_applies_nothing(env):
        db, c = env
        t, g, rec, e = undated_case(c)
        dated_ok = [x["id"] for x in g["entries"] if x["state"] == "verified" and x["review_status"] == "pending"][:2]
        assert dated_ok
        before = snapshot(db, t)
        r = c.post(f"/api/cases/{t}/review/batch", json={"action": "accept", "item_ids": dated_ok + [e["id"]]})
>       assert r.status_code == 422 and r.json()["error"]["code"] == "DATE_UNCONFIRMED"
E       AssertionError: assert (422 == 422 and 'invalid_batch' == 'DATE_UNCONFIRMED'
E        +  where 422 = <Response [422 Unprocessable Content]>.status_code
E         
E         - DATE_UNCONFIRMED
E         + invalid_batch)

tests/unit/test_date_unconfirmed.py:57: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_date_unconfirmed.py::test_batch_with_one_undated_entry_is_422_and_applies_nothing
1 failed, 4 passed in 1.89s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:00:39.660Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/case_extras.py'\ns=open(p).read()\ndc='''        elif action == \"accept\" and review.date_unconfirmed(conn, case_id, kind, row):\n            bad.append({\"id\": i, \"reason\": \"date_unconfirmed\"})\n'''\ns=s.replace(dc,'',1)\ns=s.replace('''        elif action == \"accept\" and row[\"state\"] != \"verified\":''',dc+'''        elif action == \"accept\" and row[\"state\"] != \"verified\":''',1)\nopen(p,'w').write(s)\np='tests/unit/test_date_unconfirmed.py'\ns=open(p).read()\na=s.index('    assert {\"id\": e[\"id\"], \"reason\": \"date_unconfirmed\"}')\nb=s.index('    assert snapshot(db, t) == before', a)\ns=s[:a]+'    assert {\"id\": e[\"id\"], \"reason\": \"date_unconfirmed\"} in r.json()[\"error\"][\"detail\"][\"rejected\"]\\n'+s[b:]\nopen(p,'w').write(s)\nEOF\nsed -n 20,40p app/backend/case_extras.py; .venv/bin/python -m pytest -q tests/unit 2>&1 | tail -4"
}
````

### User / tool · 2026-11-02T03:01:03.455Z

**tool result**
````
        super().__init__("invalid_batch")
        self.rejected = rejected


def _check(conn, case_id, ids, action):
    """[{id, reason}] for every id that may not be in this batch. Entries only; accept needs state verified and status pending."""
    bad = []
    for i in ids:
        try:
            kind, row = review._item(conn, case_id, i)
        except review.ReviewError:
            bad.append({"id": i, "reason": "not_found"})
            continue
        if kind != "entry":
            bad.append({"id": i, "reason": "not_an_entry"})
        elif action == "accept" and review.date_unconfirmed(conn, case_id, kind, row):
            bad.append({"id": i, "reason": "date_unconfirmed"})
        elif action == "accept" and row["state"] != "verified":
            bad.append({"id": i, "reason": "not_verified"})
        elif action == "accept" and row["review_status"] != "pending":
            bad.append({"id": i, "reason": "not_pending"})
tests/unit/test_e2e_contract.py:31: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_data_attributes_declared - Asser...
1 failed, 961 passed in 22.84s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:05.036Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_e2e_contract.py 2>&1 | grep -E \"Error|assert\" | head; git stash list | head -1; git status --short tests app/frontend | head"
}
````

### User / tool · 2026-11-02T03:01:05.091Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: subagents may not run git stash (it rewinds shared board/memory files of other agents)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:06.695Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_e2e_contract.py 2>&1 | grep -E \"Error|assert|testid|missing\" | head"
}
````

### User / tool · 2026-11-02T03:01:07.069Z

**tool result**
````
>               assert a in c, (p.name, a)
E               AssertionError: ('test_input.py', 'data-entry-id')
E               assert 'data-entry-id' in 'E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fi...bugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).\n'
tests/unit/test_e2e_contract.py:31: AssertionError
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:09.549Z

**tool call — Bash**
````
{
 "command": "grep -n \"undated\\|case_01\\|date_formats\" tests/e2e/*.py evals/*.py evals/golden/* -l 2>/dev/null | head; grep -n \"accept\" tests/e2e/test_input.py | head; grep -rn \"undated\" tests/e2e/*.py | grep -i accept | head; grep -rn \"date not stated\" tests evals spec/REQUIREMENTS.md 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T03:01:09.682Z

**tool result**
````
tests/e2e/test_input.py
tests/e2e/conftest.py
evals/golden/README.md
evals/run.py
evals/golden/case_01_date_formats.expected.json
80:def test_undated_entry_cannot_be_accepted_until_date_confirmed(page):
82:    the keyboard shortcut and 'Accept all verified' do not accept it (the batch says how many it skipped); the letter never says 'date not stated';
87:    expect(row.get_by_test_id("btn-accept")).to_be_disabled()
88:    expect(row.get_by_test_id("accept-blocked-reason")).to_contain_text("Confirm the date first")
94:    page.get_by_test_id("btn-accept-verified").click()
102:    expect(entry.get_by_test_id("btn-accept")).to_be_enabled()
109:    entry.get_by_test_id("btn-accept").click()
tests/e2e/conftest.py:11:  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
tests/e2e/test_input.py:80:def test_undated_entry_cannot_be_accepted_until_date_confirmed(page):
tests/e2e/test_input.py:81:    """T-068 r3 / D-041: on an undated entry Accept is disabled with the visible reason 'Confirm the date first' and a link to the date choices;
tests/unit/test_date_unconfirmed.py:1:"""D-041 (T-076): an entry with no confirmed date cannot be accepted (single, edit, batch) until confirm_date; the letter never says 'date not stated'."""
tests/unit/test_date_unconfirmed.py:70:    assert "date not stated" not in letter.lower()
tests/unit/test_date_unconfirmed.py:81:    assert "date not stated" not in ex["letter_text"].lower()
tests/e2e/test_input.py:82:    the keyboard shortcut and 'Accept all verified' do not accept it (the batch says how many it skipped); the letter never says 'date not stated';
tests/e2e/test_input.py:98:    expect(page.get_by_test_id("export-letter")).not_to_contain_text("date not stated")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:11.748Z

**tool call — Bash**
````
{
 "command": "grep -n \"accept\" evals/run.py | head; grep -rn \"\\\"accept\\\"\\|'accept'\\|action.*accept\" tests/e2e/*.py | grep -v \"btn-accept\" | head; grep -rn \"undated_entries\\|case_01\" tests/e2e/*.py | grep -v test_input | head"
}
````

### User / tool · 2026-11-02T03:01:11.846Z

**tool result**
````
tests/e2e/test_api.py:33:        assert api("POST", f"/api/cases/{sample_case}/items/{it['id']}/review", {"action": "accept"})[0] == 200
tests/e2e/test_adversarial.py:47:            if a["state"] != "rejected": api("POST", f"/api/cases/{tok}/items/{a['id']}/review", {"action": "accept"})
tests/e2e/test_adversarial.py:49:            if e["state"] != "rejected": api("POST", f"/api/cases/{tok}/items/{e['id']}/review", {"action": "accept"})
tests/e2e/test_local_mode.py:53:    assert call(local, "POST", f"/api/cases/{toks[0]}/items/{ea['id']}/review", {"action": "accept"})[0] == 200
tests/e2e/test_letter_isolation.py:10:    st, _ = api("POST", f"/api/cases/{tok}/items/{it['id']}/review", {"action": "accept"})
tests/e2e/test_ladder_gate.py:27:    assert api("POST", f"/api/cases/{sample_case}/items/{rej[0]['id']}/review", {"action": "accept"})[0] == 409
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:13.248Z

**tool call — Bash**
````
{
 "command": "sed -n 36,56p tests/e2e/test_adversarial.py; sed -n 1,15p tests/e2e/test_letter_isolation.py; sed -n 25,36p tests/e2e/test_api.py"
}
````

### User / tool · 2026-11-02T03:01:13.335Z

**tool result**
````
    """R-RV-6 (D-005): case_07 injection text never reaches the total: accept every amount -> 'Billed charges stated in these records: $420.00'; $50,000 is not in the letter; no flag was resolved."""
    st, c = api("POST", "/api/cases", {"text": golden_text("case_07_prompt_injection.txt")}); assert st == 201
    tok = c["token"]
    try:
        assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
        for _ in range(180):
            if api("GET", f"/api/cases/{tok}/status")[1]["status"] in ("ready", "failed"): break
            time.sleep(1)
        d = api("GET", f"/api/cases/{tok}")[1]
        assert not [f for f in d["flags"] if f["review_status"] != "pending"]
        for a in d["amounts"]:
            if a["state"] != "rejected": api("POST", f"/api/cases/{tok}/items/{a['id']}/review", {"action": "accept"})
        for e in d["entries"]:
            if e["state"] != "rejected": api("POST", f"/api/cases/{tok}/items/{e['id']}/review", {"action": "accept"})
        t = api("GET", f"/api/cases/{tok}/export")[1]["letter_text"]
        assert "Billed charges stated in these records: $420.00" in t.split("\n") and "50,000" not in t
        assert any(w.get("category") == "injection_suspected" or "INJECTION" in str(w) for w in d.get("record_warning_flags", []) + d["flags"] + d.get("warnings", []))
    finally:
        api("DELETE", f"/api/cases/{tok}")
"""Letter isolation. R-EX-1 (no tool-authored flag content), D-019, D-012."""
import re
import pytest
from tests.e2e.conftest import api, open_case, golden_text, BASE


BAD = ["73 days", "AI assistance", "Conflict", "Causation", "Prior condition", "REVIEWER NOTE", "visit count", "supplemented", "rate", "Pending items", "of 9"]

def accept(tok, it):
    st, _ = api("POST", f"/api/cases/{tok}/items/{it['id']}/review", {"action": "accept"})
    assert st == 200 or it.get("state") == "rejected", (it["id"], st)

def test_letter_has_no_flag_or_note_content(sample_case):
    """R-EX-1: accept everything (each accept must return 200), add a reviewer note (200); letter is non-empty, has 9 dated headings and the accepted quotes; none of the forbidden strings."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
def test_empty_input_is_400():
    """R-IN-2: empty input -> 400 bad_request."""
    assert api("POST", "/api/cases", {"text": ""})[0] == 400

def test_export_is_deterministic_and_equals_golden(sample_case):
    """R-EX-6: accept all nine entries + both charges + all flags -> letter_text equals the golden LETTER block byte for byte; twice identical."""
    c = api("GET", f"/api/cases/{sample_case}")[1]
    for it in c["entries"] + [a for a in c["amounts"] if a["kind"] == "charge"] + c["flags"]:
        assert api("POST", f"/api/cases/{sample_case}/items/{it['id']}/review", {"action": "accept"})[0] == 200
    a = api("GET", f"/api/cases/{sample_case}/export")[1]; b = api("GET", f"/api/cases/{sample_case}/export")[1]
    golden = golden_text("sample.export.expected.txt").split("=== INTERNAL_NOTES_TEXT")[0].split("\n", 1)[1].rstrip("\n")
    assert a["letter_text"] == golden and a["letter_text"] == b["letter_text"] and a["internal_notes_text"] == b["internal_notes_text"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:20.731Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='memory/contracts/api.md'\ns=open(p).read()\nold=\"| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset |\"\nassert old in s\ns=s.replace(old,\"| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected` |\",1)\nold=\"Other malformed bodies: `400 bad_request`.\"\nassert s.count(old)==1\ns=s.replace(old,\"Other malformed bodies: `400 bad_request`. **D-041:** an entry with no confirmed date (see `undated_entries`) is refused for `accept` with reason `date_unconfirmed`; when any rejected id has that reason the response is `422 DATE_UNCONFIRMED` (instead of `invalid_batch`; same `detail.rejected` list, which still names every refused id and its reason), and nothing changes. After `confirm_date` the entry can be accepted singly or in a batch.\",1)\nold=\"Accepting is idempotent.\"\nassert old in s\ns=s.replace(old,\"Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so \\\"date not stated\\\" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as \\\"date not confirmed, not exported\\\".\",1)\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -3; git add app/backend/review.py app/backend/case_extras.py app/backend/export.py tests/unit/test_date_unconfirmed.py memory/contracts/api.md 2>&1"
}
````

### User / tool · 2026-11-02T03:01:43.204Z

**tool result**
````
........................................................................ [ 97%]
..........................                                               [100%]
962 passed in 21.72s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:45.919Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"feat(backend): block accept of undated entries until date confirmed (D-041, T-076)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/backend/review.py app/backend/case_extras.py app/backend/export.py tests/unit/test_date_unconfirmed.py memory/contracts/api.md && git log --oneline | head -1"
}
````

### User / tool · 2026-11-02T03:01:46.276Z

**tool result**
````
check_secrets: ok (5 file(s) scanned staged)
88a3393 feat(backend): block accept of undated entries until date confirmed (D-041, T-076)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:50.475Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B commit T-076 --sha 88a3393 --agent backend; $B note T-076 --agent backend --text \"e2e check: no e2e test accepts an undated entry (test_api/test_letter_isolation/test_adversarial/test_local_mode iterate dated entries only; test_input.py::test_undated_entry_cannot_be_accepted_until_date_confirmed already matches D-041). Unrelated: tests/unit/test_e2e_contract.py::test_data_attributes_declared fails in the shared tree because tests/e2e/test_input.py uses data-entry-id not declared in conftest (qa).\"; $B ac T-076 --check 1 --agent backend --evidence \"tests/unit/test_date_unconfirmed.py (5 tests) pass; full tests/unit 962 passed; api.md updated; commit 88a3393\"; $B handoff T-076 --agent backend --text \"What changed: review.date_unconfirmed() gates accept and edit (422 DATE_UNCONFIRMED, before any write); case_extras batch check adds reason date_unconfirmed and returns 422 DATE_UNCONFIRMED; export.in_entries excludes undated entries (notes line 'date not confirmed, not exported'); api.md updated. Verified: .venv/bin/python -m pytest -q tests/unit (962 pass; one test_e2e_contract failure seen once was from qa's concurrent edit, not mine, later passed). Left: nothing. Surprised: the undated entry is needs_review, so the date check runs before not_verified in the batch. Edit also blocked since it implies accept.\"; $B move T-076 in_review --agent backend"
}
````

### User / tool · 2026-11-02T03:01:50.840Z

**tool result**
````
T-076: commit 88a3393 recorded
noted on T-076
AC 1 checked: tests/unit/test_date_unconfirmed.py (5 tests) pass; full tests/unit 962 passed; api.md updated; commit 88a3393
handoff written on T-076
T-076: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:01:53.578Z

T-076 is in `in_review` (commit 88a3393, full `tests/unit` 962 passed). Single accept, edit (which implies accept) and batch accept on an entry with no confirmed date now return 422 `DATE_UNCONFIRMED` and change nothing. After `confirm_date` they succeed. `export.py` now keeps an undated entry out of the letter, so "date not stated" never appears in the treatment section, and `api.md` is updated.

No e2e test accepts an undated entry, so I posted no qa/frontend note naming one. `tests/e2e/test_input.py` already matches the rule. One unrelated failure showed up once: `test_e2e_contract.py::test_data_attributes_declared` flagged `data-entry-id` in `test_input.py` as undeclared in `conftest.py`. It passed on a later run, and I noted it on the card for qa.
