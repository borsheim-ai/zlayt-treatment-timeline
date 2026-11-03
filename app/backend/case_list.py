"""GET /api/cases (T-148): one summary per case for the local profile's overview screen. Local mode only (D-008/D-031); the route is a 404 otherwise.

Code only: no model call, no pipeline run, no record text. Every number comes from the functions GET case, GET status and the export gate already use, so the
list cannot say something the case screen does not:
  run                                        -> run_progress() (the /status route calls it too)
  progress decided / total per kind          -> the item filter present.review_view applies (live = not rejected, no tray placeholder, no rule-filtered proposal)
  hitl.needs_review, edits_to_check, tray    -> present.review_view counts (the tray length GET case returns is the `rejected` count)
  hitl.gate, export_ready                    -> the export_gate step of trace.case_trace (blockers and warnings with their plain `why`; the list GET /export refuses on)
tests/unit/test_case_list.py compares each field with GET case, /status, /trace and /export for every library case.
"""
import datetime
import logging
import re
import time

from app.backend import flag_templates as FT, generator, present, review, store, trace
from app.db import db as DB

log = logging.getLogger("zlayt.api")
RETRY_PAUSE = 0.05            # seconds before the one re-read of a case whose summary failed

KINDS = (("entries", "entry"), ("flags", "flag"), ("amounts", "amount"))
_SLUG = re.compile(r"^[\w.\-]+$")
_LIB_PREFIX = re.compile(r"^case[ _](?:lib)?\d+[ _]", re.IGNORECASE)      # evals/library and evals/golden file names: case_lib01_..., case_01_...
_EXT = re.compile(r"\.(pdf|txt|docx?|rtf)$", re.IGNORECASE)


MAX_TITLE = 120
_WS = re.compile(r"[\t\n\r\x0b\x0c\x85\u2028\u2029]+")
_CTRL = re.compile(r"[\x00-\x1f\x7f-\x9f\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]")      # control, zero-width and bidi-override characters: removed
_TAG = re.compile(r"<[^<>]*>")


class TitleError(ValueError):
    """T-157 r2: a typed title that cannot be stored. str(e) is the plain message the API returns (422 invalid_title); it never repeats the rejected text."""


def _tidy(value) -> str:
    """Control and bidi characters removed, line breaks and tabs turned into spaces, runs of white space collapsed. '' for anything that is not text."""
    if not isinstance(value, str):
        return ""
    return re.sub(r" +", " ", _CTRL.sub("", _WS.sub(" ", value))).strip()


def validate_title(value) -> str:
    """T-157 r2: a title the paralegal typed (create, PATCH). Control characters stripped, white space collapsed; '' when nothing is left (clears the name).
    Raises TitleError for markup (any < or >: a title is plain text, never HTML) and for more than 120 characters. Nothing is escaped or rewritten: it is refused, so what is
    stored is exactly what was typed."""
    t = _tidy(value)
    if "<" in t or ">" in t:
        raise TitleError("A case title is plain text. Remove the angle brackets and try again.")
    if len(t) > MAX_TITLE:
        raise TitleError(f"A case title can be at most {MAX_TITLE} characters. Shorten it and try again.")
    return t


def plain_title(value) -> str:
    """T-157 r2: text from a record (a Source line) shown as a title: complete tags dropped, a lone angle bracket removed on its own (the words after it stay), tidied, at most 120 characters. Never refused: it is not typed."""
    return _tidy(re.sub(r"[<>]", "", _TAG.sub(" ", _tidy(value))))[:MAX_TITLE].strip()


def clean_title(value) -> str:
    """The stored name of a case from a field that may hold a file name (`name`, the PDF's name): validated like a typed title, except that a long file name is cut to
    120 characters, not refused. Markup is still refused."""
    t = _tidy(value)
    return validate_title(t if ("<" in t or ">" in t) else t[:MAX_TITLE])


def derived_title(conn, case_id) -> str:
    """T-157: the title of a case nobody named, from its first record header: the provider (Source line) and that record's date, "Marrowgate General ED, Feb 14, 2026".
    None when no record has either."""
    for r in conn.execute("SELECT source_label, date_iso FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
        label = plain_title(r["source_label"])[:60].strip()
        try:
            day = datetime.date.fromisoformat(r["date_iso"]).strftime("%b %-d, %Y") if r["date_iso"] else None
        except ValueError:
            day = None
        if label:
            return f"{label}, {day}" if day else label
        if day:
            return f"Records from {day}"
    return None


def readable_name(name) -> str:
    """A stored name made readable: a file name or slug ("smith_records-2024.pdf", "case_lib01_er_only") becomes words, a typed name keeps its words, markup is dropped.
    '' when nothing is left ("case_01_", ".txt")."""
    typed = plain_title(name)
    n = _LIB_PREFIX.sub("", typed)
    if n and (_SLUG.match(n) or n != typed) and not n.isalpha():          # one token with _ - . in it, or a library prefix: a file name or slug, not a typed name
        n = re.sub(r"\s+", " ", re.sub(r"[_\-]+", " ", _EXT.sub("", n))).strip()
        n = n[:1].upper() + n[1:]
    return n


def readable_title(name, source, created_at) -> str:
    """A name a paralegal would recognise; no name at all becomes "Records added Nov 1" (T-157: never "Untitled case"; `case_title` prefers the first record header over that fallback)."""
    n = readable_name(name)
    if n:
        return n
    day = datetime.datetime.fromtimestamp(float(created_at or 0), datetime.timezone.utc).strftime("%b %-d")
    return "Sample case" if source == "sample" else f"Records added {day}"


def case_title(conn, case: dict) -> str:
    """What to show for a case: its name made readable; else (no name, or one that is empty after cleanup) the first record header (provider and date); else the date it was added.
    Never "Untitled case", never markup."""
    return readable_name(case["name"]) or derived_title(conn, case["id"]) or readable_title(None, case["source"], case["created_at"])


def run_progress(case: dict, stages) -> tuple:
    """(stage, steps_done) for a case row: what GET /status reports. A case that was only ingested is at the 'ingest' stage."""
    stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
    return stage, (list(stages).index(stage) if stage in stages else 0)


def _progress(conn, case_id) -> dict:
    """decided / total per kind over the items review_view counts. An edit still marked Needs review (T-134) is not decided."""
    items = {k: DB.list_items(conn, case_id, k) for _, k in KINDS}
    handled = generator.resolved_placeholders(items["entry"])
    out = {}
    for label, kind in KINDS:
        live = [r for r in items[kind] if r["id"] not in handled and not FT.is_filtered(r.get("state_reasons")) and r["state"] != "rejected"]
        decided = sum(1 for r in live if r["review_status"] in ("accepted", "dismissed", "edited") and not review.edit_unconfirmed(kind, r))
        out[label] = {"decided": decided, "total": len(live)}
    return out


def _gate(conn, case_id) -> dict:
    step = next(s for s in trace.case_trace(conn, case_id, full=False)["steps"] if s["id"] == "export_gate")
    keep = lambda xs, keys: [{k: x[k] for k in keys if k in x} for x in xs]      # noqa: E731
    return {"ready": step["ready"], "blockers": keep(step["blockers"], ("reason_code", "kind", "item_id", "why")),
            "warnings": keep(step["warnings"], ("reason_code", "count", "why"))}


_RANK = {"entry": 0, "flag": 1, "amount": 2}


def needs_review_order(conn, case_id) -> list:
    """T-157: the live items that still wait for the paralegal and that the AI could not verify (state needs_review; pending, or an edit not yet confirmed), in timeline order:
    the date of the record each item cites (earliest, for a flag that cites several), then that record's position, then entry before flag before amount, then id. Undated last.
    [{id, kind, date, seq, rank, row}]. Same item filter as `_progress`."""
    recs = {r["id"]: (r["date_iso"], r["seq"]) for r in conn.execute("SELECT id, date_iso, seq FROM records WHERE case_id=?", (case_id,))}
    by_seq = {seq: rid for rid, (_, seq) in recs.items()}
    items = {k: DB.list_items(conn, case_id, k) for _, k in KINDS}
    handled = generator.resolved_placeholders(items["entry"])
    out = []
    for kind, rows in items.items():
        for r in rows:
            if r["id"] in handled or FT.is_filtered(r.get("state_reasons")) or r["state"] != "needs_review":
                continue
            if not (r["review_status"] == "pending" or review.edit_unconfirmed(kind, r)):
                continue
            ids = list(r.get("record_ids") or []) if kind != "flag" else \
                [e.get("record_id") or by_seq.get(e.get("record_no")) for e in r.get("evidence") or []] or list((r.get("computed") or {}).get("record_ids") or [])
            known = sorted((recs[i] for i in ids if i in recs), key=lambda x: (x[0] is None, x[0] or "", x[1] or 0))
            date, seq = known[0] if known else (None, None)
            date = date or (r.get("date_iso") if kind == "entry" else None)
            out.append({"id": r["id"], "kind": kind, "date": date, "seq": seq, "rank": _RANK[kind], "row": r})
    return sorted(out, key=lambda x: (x["date"] is None, x["date"] or "", x["seq"] or 0, x["rank"], x["id"]))


def next_action(conn, case_id, case: dict = None, blockers: list = None):
    """T-157: the single first thing to do in a case, {item_id, kind, reason}, or None when nothing is waiting. Code only, deterministic:
      1. the first export-gate blocker, in gate order (a run in progress or failed, a code-check failure, an accepted item whose second check never answered). Its `kind` is the
         blocker's (`case` for a blocker that names no item, `item_id` null) and `reason` its plain `why`. NOTHING_ACCEPTED yields to step 2 when an item waits (deciding it clears it);
      2. else the first needs-review item in timeline order (`needs_review_order`): `kind` entry | flag | amount, `reason` the item's own plain `why`;
      3. else NOTHING_ACCEPTED when nothing is accepted; else None.
    A case that was only ingested has no items yet: {item_id: null, kind: "run"}. `blockers` may be passed when the caller already read the gate."""
    case = case or DB.get_case(conn, case_id)
    if case["status"] == "ingested":
        return {"item_id": None, "kind": "run", "reason": "Run the case to draft the timeline. Nothing is waiting for you until then."}
    blockers = _gate(conn, case_id)["blockers"] if blockers is None else blockers
    first = next((b for b in blockers if b["reason_code"] != "NOTHING_ACCEPTED"), None)
    if first:
        return {"item_id": first.get("item_id"), "kind": first["kind"], "reason": first["why"]}
    waiting = needs_review_order(conn, case_id)
    if waiting:
        w = waiting[0]
        return {"item_id": w["id"], "kind": w["kind"], "reason": present.item_view(conn, case_id, w["id"])["why"]}
    if blockers:
        return {"item_id": blockers[0].get("item_id"), "kind": blockers[0]["kind"], "reason": blockers[0]["why"]}
    return None


def summary(conn, case_id: str, stages) -> dict:
    case = DB.get_case(conn, case_id)
    rv = present.review_view(conn, case_id)
    counts = rv["counts"]
    stage, done = run_progress(case, stages)
    gate = _gate(conn, case_id)
    last = conn.execute("SELECT max(at) FROM review_events WHERE case_id=?", (case_id,)).fetchone()[0]
    updated = case.get("run_finished_at") or case["created_at"]            # the same value GET case calls updated_at
    return {"token": case_id, "title": case_title(conn, case), "name": case["name"],
            "source": case["source"], "status": case["status"],
            "record_count": conn.execute("SELECT count(*) FROM records WHERE case_id=?", (case_id,)).fetchone()[0],
            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(updated), "last_activity_at": store.iso(max(updated, last or 0)),
            "run": {"stage": stage, "steps_done": done, "steps_total": len(stages), "running": case["status"] == "running",
                    "error": bool(case.get("error"))},
            "progress": _progress(conn, case_id),
            "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},      # kept from the first version of this route
            "hitl": {"pending": counts["pending"], "needs_review": counts["needs_review"], "needs_review_open": len(needs_review_order(conn, case_id)), "edits_to_check": counts["edit_to_check"],
                     "could_not_verify": counts["rejected"], "gate_blockers": gate["blockers"], "gate_warnings": gate["warnings"]},
            "export_ready": gate["ready"], "next_action": next_action(conn, case_id, case, gate["blockers"]),
            "status_error": False, "status_error_message": None}


STATUS_ERROR_MESSAGE = "We couldn't load this case's status"


def plain_row(conn, case: dict, stages) -> dict:
    """T-175 r2: the row for a case that exists but whose status could not be computed (summary failed twice in a row, so this is a bug and not a write in flight). Same keys as
    `summary`, but it says so: `status_error: true` + `status_error_message`, and every figure is null (record_count, counts, progress, hitl) so no zero is shown as if it were real.
    Nothing is claimed about export readiness (`export_ready` false, `next_action` null); the row carries only what the case row itself holds (token, title, status, times)."""
    try:
        stage, done = run_progress(case, stages)
    except Exception:
        stage, done = None, 0
    updated = case.get("run_finished_at") or case["created_at"]
    try:
        title = case_title(conn, case)
    except Exception:
        title = readable_title(None, case["source"], case["created_at"])
    return {"token": case["id"], "title": title, "name": case["name"], "source": case["source"], "status": case["status"],
            "record_count": None, "created_at": store.iso(case["created_at"]), "updated_at": store.iso(updated), "last_activity_at": store.iso(updated),
            "run": {"stage": stage, "steps_done": done, "steps_total": len(stages), "running": case["status"] == "running", "error": bool(case.get("error"))},
            "progress": None, "counts": None, "hitl": None,
            "export_ready": False, "next_action": None, "status_error": True, "status_error_message": STATUS_ERROR_MESSAGE}


def summaries(conn, stages) -> list:
    """Every case, newest first (created, then insertion order). T-175: the id list and each case are read at different moments, so a case can be deleted (DELETE, the purge)
    or be mid-write (a run, a review) in between. A case that is gone is left out. A case whose summary fails is read again once, after a short pause: if that works it is the
    full row (a write was in flight). If it fails again the case exists and the failure is a bug: the row is listed with `status_error: true` (see `plain_row`) and logged at ERROR.
    Everything is logged by exception class only (no text from the case), and the list itself never fails for one case."""
    out = []
    for r in conn.execute("SELECT id FROM cases ORDER BY created_at DESC, rowid DESC").fetchall():
        err = None
        for attempt in (1, 2):
            try:
                out.append(summary(conn, r["id"], stages))
                err = None
                break
            except Exception as e:
                err = type(e).__name__
                if DB.get_case(conn, r["id"]) is None:
                    break
                if attempt == 1:
                    time.sleep(RETRY_PAUSE)
        if err is None:
            continue
        case = DB.get_case(conn, r["id"])
        if case is None:
            log.warning("case list: a case was deleted while the list was read (%s); left out", err)
            continue
        try:
            out.append(plain_row(conn, case, stages))
            log.error("case list: a case's status could not be computed twice in a row (%s); listed with status_error", err)
        except Exception:
            log.error("case list: a case could not be listed at all (%s); left out", err)
    return out
