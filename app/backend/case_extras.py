"""Batch accept of verified entries and per-case export config (D-031). Routes are added by api.create_app via add_routes().
Code only: nothing here asks a model anything, and the only review_status writer used is DB.apply_review (one event per item)."""
import re
import threading

from fastapi import Request

from app.backend import present, review, store
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


def _code_check_refusal(conn, case_id, item_id, row, cache):
    if "recs" not in cache:
        cache["recs"] = store.load_records(conn, case_id)
    err = review.code_check_error(item_id, review.entry_record(row, cache["recs"]), row)
    if not err:
        return None
    return {"id": item_id, "reason": "code_check_failed", "reason_code": err.detail["reason_code"], "why": err.message, "next_action": err.detail["next_action"]}


def _check(conn, case_id, ids, action):
    """[{id, reason}] for every id that may not be in this batch. Entries only; accept needs state verified and status pending."""
    bad, cache = [], {}
    for i in ids:
        try:
            kind, row = review._item(conn, case_id, i)
        except review.ReviewError:
            bad.append({"id": i, "reason": "not_found"})
            continue
        if kind == "amount" and row["kind"] == "charge":      # D-059: a charge is accepted one at a time, never in a batch
            bad.append({"id": i, "reason": "charge_in_batch"})
        elif kind != "entry":
            bad.append({"id": i, "reason": "not_an_entry"})
        elif action == "accept" and review.judge_dispute(row):      # D-066: a disputed summary is accepted alone, with her explicit compare
            bad.append({"id": i, "reason": "judge_disputed"})
        elif action == "accept" and review.date_unconfirmed(conn, case_id, kind, row):
            bad.append({"id": i, "reason": "date_unconfirmed"})
        elif action == "accept" and (err := _code_check_refusal(conn, case_id, i, row, cache)):     # D-051: same check as a single accept
            bad.append(err)
        elif action == "accept" and row["state"] != "verified":
            bad.append({"id": i, "reason": "not_verified"})
        elif action == "accept" and row["review_status"] != "pending":
            bad.append({"id": i, "reason": "not_pending"})
    return bad


def apply_batch(conn, case_id, body, now):
    """All or nothing. Validation covers every id before the first write; if a write still fails, the items already changed are put back."""
    action, ids = (body or {}).get("action"), (body or {}).get("item_ids")
    if action not in ("accept", "reset") or not isinstance(ids, list) or not ids or len(ids) > MAX_BATCH or \
            not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("bad_request")
    with _LOCK:
        bad = _check(conn, case_id, ids, action)
        if bad:
            raise BatchRefused(bad)
        done = []
        recs = store.load_records(conn, case_id) if action == "accept" else None
        try:
            for i in ids:
                review.batch_apply(conn, case_id, i, action, now, recs)
                done.append(i)
        except Exception:
            for i in reversed(done):          # compensate: each undo is itself an audited event
                review.batch_apply(conn, case_id, i, "reset", now)
            raise
    items = [{"id": i, "review_status": DB.get_item(conn, i, case_id)["review_status"]} for i in ids]
    return {"items": items, "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": []}


# ------------------------------------------------------------------ export config
def validate_config(b):
    """Returns the normalised config or raises ValueError. All keys optional; unknown keys refused."""
    if not isinstance(b, dict) or set(b) - set(EXPORT_KEYS):
        raise ValueError("invalid_edit")
    out = {}
    for k in ("exhibit", "bates_prefix"):
        v = b.get(k)
        if v is None or v == "":
            out[k] = None
        elif isinstance(v, str) and _LABEL.fullmatch(v):
            out[k] = v
        else:
            raise ValueError("invalid_edit")
    s = b.get("bates_start")
    if s is None:
        out["bates_start"] = None
    elif isinstance(s, int) and not isinstance(s, bool) and 0 <= s <= 99999999:
        out["bates_start"] = s
    else:
        raise ValueError("invalid_edit")
    return out


def get_config(conn, case_id) -> dict:
    cfg = (DB.get_case(conn, case_id).get("config") or {}).get("export") or {}
    return {k: cfg.get(k) for k in EXPORT_KEYS}


def put_config(conn, case_id, cfg):
    case = DB.get_case(conn, case_id)
    config = dict(case.get("config") or {})
    if cfg is None or not any(v is not None for v in cfg.values()):
        config.pop("export", None)
    else:
        config["export"] = cfg
    DB.update_case(conn, case_id, config_json=config or None)


def add_routes(app, *, conn, get_case, body_of, ApiError, now):
    @app.post("/api/cases/{token}/review/batch")
    async def review_batch(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            try:
                return apply_batch(c, token, b, now())
            except ValueError:
                raise ApiError(400, "bad_request", "Send an action (accept or reset) and a list of entry ids.") from None
            except BatchRefused as e:
                if any(r["reason"] == "charge_in_batch" for r in e.rejected):      # D-059
                    raise ApiError(422, "CHARGES_NOT_BATCHED", "Charges are accepted one at a time, so a charge cannot be part of a batch. Take the charge out and review it by itself; nothing was changed.",
                                   {"rejected": e.rejected}) from None
                if any(r["reason"] == "code_check_failed" for r in e.rejected):       # D-051
                    first = next(r for r in e.rejected if r["reason"] == "code_check_failed")
                    raise ApiError(422, "CODE_CHECK_FAILED", first["why"] + " Nothing was changed.", {"rejected": e.rejected}) from None
                if any(r["reason"] == "date_unconfirmed" for r in e.rejected):     # D-041: same code as a single accept
                    raise ApiError(422, "DATE_UNCONFIRMED", "Confirm the date of every undated entry first (Dates to confirm); nothing was changed.", {"rejected": e.rejected}) from None
                raise ApiError(422, "invalid_batch", "Only verified entries can be accepted together; nothing was changed.", {"rejected": e.rejected}) from None
        finally:
            c.close()

    @app.get("/api/cases/{token}/export_config")
    def export_config_get(token: str):
        c = conn()
        try:
            get_case(c, token)
            return get_config(c, token)
        finally:
            c.close()

    @app.put("/api/cases/{token}/export_config")
    async def export_config_put(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            try:
                cfg = validate_config(b)
            except ValueError:
                raise ApiError(422, "invalid_edit", "Exhibit and prefix: up to 20 letters, digits, space . _ -; first number 0 to 99999999.") from None
            put_config(c, token, cfg)
            return get_config(c, token)
        finally:
            c.close()

    @app.delete("/api/cases/{token}/export_config")
    def export_config_delete(token: str):
        c = conn()
        try:
            get_case(c, token)
            put_config(c, token, None)
            return get_config(c, token)
        finally:
            c.close()
