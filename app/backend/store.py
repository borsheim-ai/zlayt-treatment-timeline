"""DB <-> unit-dict adapters shared by the API layer and the pipeline (T-040). Pure functions plus ingest persistence.

Item/record ids are the pipeline's own ("r6", "e5", "f_gap_r6_r7"); see the id-collision note on T-040.
"""
import json
import os
import threading
import time

from app.backend import ingest, pdf_text, spanish
from app.db import db as DB

# T-178 (GATE-M3 chaos blocker): a run is a thread of THIS process. When the process dies (crash, sleep, redeploy) the case row still says "running" and nothing would ever clear it.
LIVE_RUNS = set()                 # tokens whose run thread is alive in this process (api._run_thread adds and removes)
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


def interrupt_run(conn, token: str, now: float = None) -> bool:
    """Mark a case left `running` as failed with the honest `run_partial` message (T-146: the case reads failed, a re-run is allowed, nothing item-level is touched, so accepted
    and dismissed items stay exactly as they were and the re-run's `_persist` keeps them). False when the case is not running."""
    now = time.time() if now is None else now
    case = DB.get_case(conn, token)
    if case is None or case["status"] != "running":
        return False
    DB.update_case(conn, token, status="failed", run_finished_at=now,
                   error=json.dumps({"code": "run_partial", "interrupted": True, "message": INTERRUPTED_MESSAGE}))
    return True


def interrupt_orphaned_runs(conn, now: float = None) -> list:
    """At startup: every case still `running` and not running in this process was left by a process that stopped. Returns the tokens marked."""
    out = []
    for r in conn.execute("SELECT id FROM cases WHERE status='running'").fetchall():
        if not is_live_run(r[0]) and interrupt_run(conn, r[0], now):
            out.append(r[0])
    return out


def settle_stale_run(conn, case: dict, now: float = None) -> dict:
    """On read: a `running` case with no live thread in this process whose run started more than RUN_STALE_AFTER_S ago is an orphan too (a second process, a restart that
    skipped the startup sweep). Returns the case, re-read when it was changed."""
    now = time.time() if now is None else now
    if case and case["status"] == "running" and not is_live_run(case["id"]) and case.get("run_started_at") and now - case["run_started_at"] > RUN_STALE_AFTER_S:
        if interrupt_run(conn, case["id"], now):
            return DB.get_case(conn, case["id"])
    return case


def live_enabled() -> bool:
    """T-157 r2: the one definition of "live", used by api.demo_mode (its negation) and by rerun_available. ENABLE_LIVE=1 and something to call: the claude CLI, or an API key.
    Read per call so a test can change the environment."""
    from app.llm import provider
    return os.environ.get("ENABLE_LIVE") == "1" and (provider.backend_name() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))


def live_model_available() -> bool:
    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with."""
    from app.llm import provider
    return provider.backend_name() != "fixture" and live_enabled()


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
def amount_pos(item: dict, rec):
    """Where the amount's own figure sits in its excerpt (T-140 r3: quotes and reasons are taken from the figure's own offset, never from a text search that finds
    the first equal figure). None when the stored offsets do not point at the figure's text."""
    start, raw = item.get("excerpt_start"), item.get("text") or ""
    if rec is None or start is None or not raw:
        return None
    from app.backend import generator          # lazy: generator imports store
    i = start - generator.body_offset(rec)
    return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None


def charge_service_date(item: dict, rec, pos) -> dict:
    """D-071 + D-073 (extends T-200, T-202 round 5): what a charge line prints as its date, and why, for the letter AND the case view (Step 3 shows exactly this).
    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or the fillable blank 'date of service [__________] (record dated June 15, 2026)'
    when no service date is certain), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
    A date has exactly two sources (service_date.resolve): the date cell of the line's own row under a bill-table heading that names the date of service (a CMS-1500 24A From/To pair or a
    UB-04 statement-covers-period span included), or the record's own date when the source label names a DOCUMENT TYPE (visit, progress or office note, ER or ED record, discharge summary, PT
    or therapy note, run report, operative report ...; service_date.record_kind, app/backend/encounter_types.json) and the charge's sentence holds no other date or visit count. Prose is never
    read, a provider name is never a document type, and a bill, receipt, superbill, charge summary, administrative paper or record of unknown type never lends its date. A charge the paralegal
    counted for a missing date of service (D-064) is not stated, with no note (she counted it knowing). Code only."""
    from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
    rd = (rec or {}).get("date_iso")
    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
    none = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
    if counted_undated:
        r = dict(none)
    elif rec is None or pos is None or not item.get("excerpt"):
        r = dict(none)          # T-207 r2 F3: a figure the code cannot locate in its record is never looked at, so not even an encounter record lends its date: the blank prints
    else:
        r = SD.resolve(item["excerpt"], pos, rec.get("source"), rd)
    stated = r["state"] == "stated"
    note = None
    if not stated and not counted_undated:
        note = SD.confirm_note(r["reason"], r["raw"])
    return {"state": r["state"], "date_iso": r["first"], "end_iso": r["last"] if stated else None,
            "text": SD.display(r["first"], r["last"]) if stated else SD.printed_text(r, rd),
            "statement_date_iso": rd, "date_label": SD.date_label(), "reason": r["reason"], "confirm_note": note}


def charge_service_dates(item: dict, rec, pos) -> tuple:
    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
    d = charge_service_date(item, rec, pos)
    return d["date_iso"], d["end_iso"]


def export_case(conn, case_id: str, blockers: bool = True) -> dict:
    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
    case = DB.get_case(conn, case_id)
    recs = load_records(conn, case_id, case["raw_text"])
    n_of = {r["id"]: r["n"] for r in recs}
    rec_of = {r["id"]: r for r in recs}
    from app.backend import review as review_mod        # lazy: review imports store
    from app.backend import present                     # lazy: present imports store
    prep = present.models_for(conn, case_id, {"generator": "", "judge": ""})["generator_prepared"]      # D-069: the case's provenance chooses the wording of the export's notes and labels
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
            d["translation_label"] = spanish.translation_info("es", "summary" in ed or bool(lad["translation"].get("human_written")), prep)["label"]
        ents.append(d)
    amts = []
    for a in DB.list_items(conn, case_id, "amount"):
        if a["state"] == "rejected":
            continue
        r = rec_of.get((a["record_ids"] or [None])[0])
        d = dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
                 excerpt=a["excerpt"], review_status=a["review_status"], pos=amount_pos(a, r))
        if a["kind"] == "charge":
            sd = charge_service_date(a, r, d["pos"])
            d["dos_iso"], d["dos_end_iso"], d["dos_text"], d["dos_note"] = sd["date_iso"], sd["end_iso"], sd["text"], sd["confirm_note"]
        amts.append(d)
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
    out = dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events, prepared=prep)
    if blockers:                                        # trace.export_blockers calls this with blockers=False to build the letter it checks (T-139 r4)
        from app.backend import trace                   # lazy: trace imports store
        out["export_blockers"] = trace.export_blockers(conn, case_id, case=out)       # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
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
