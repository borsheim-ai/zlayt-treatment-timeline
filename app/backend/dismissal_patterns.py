"""Dismissal-pattern SUGGESTIONS for the single local profile (T-089, D-042; code only, LLM_VS_CODE row 12). Suggestions only.

The tool has one local profile: no accounts, no users, no auth. "Profile" means this machine's database, so the history is the set of flags
the paralegal has dismissed in it (read from the flags table; nothing new is stored, and deleting a case deletes its history). Outside
ZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.

When the same lexicon phrase (PHRASE_MIN dismissals) or the same category (CATEGORY_MIN) has been dismissed repeatedly, the review screen
may offer "You dismissed this kind of flag 4 times. Hide similar ones in this case?". This module only READS: suggest() never writes and
never changes a pipeline result, a flag's state or its review_status. The paralegal's click calls apply(), which dismisses the matching
PENDING flags in this case one by one through the normal review path (each a logged `dismiss` event with a reviewer note). Those
bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself.

Only lexicon-phrase flags of type pre_existing or causation are eligible. Gap and conflict flags, injection and date warnings, and flags
that code or the model found without a lexicon phrase are never suggested for hiding."""
from fastapi import Request

from app.backend import lexicon_scan, review
from app.db import db as DB

PHRASE_MIN = 3
CATEGORY_MIN = 5
ELIGIBLE_TYPES = ("pre_existing", "causation")
APPLIED_NOTE = "Hidden by dismissal-pattern suggestion (paralegal confirmed)."
_BAD = ("rejected",)


def _eligible(f) -> bool:
    return f["type"] in ELIGIBLE_TYPES and "lexicon" in (f.get("origin") or "")


def _phrase(f):
    """(lexicon entry id, matched phrase) for the flag, from its own evidence text, or (None, None). Same category only."""
    for ev in f.get("evidence") or []:
        hits = [h for h in lexicon_scan.scan(ev.get("text") or "") if h["category"] == f["category"]]
        if hits:
            h = min(hits, key=lambda x: x["start"])
            return h["id"], " ".join(h["text"].lower().split())
    return None, None


def _history(conn, case_id: str, local: bool) -> list:
    """Dismissed, eligible flags that were dismissed by the paralegal one at a time."""
    rows = conn.execute("SELECT * FROM flags WHERE review_status='dismissed'" + ("" if local else " AND case_id=?"), () if local else (case_id,)).fetchall()
    return [f for f in (DB._decode(r) for r in rows) if _eligible(f) and (f.get("reviewer_note") or "") != APPLIED_NOTE]


def _pending(conn, case_id: str) -> list:
    return [f for f in DB.list_items(conn, case_id, "flag") if f["review_status"] == "pending" and f["state"] not in _BAD and _eligible(f)]


def suggest(conn, case_id: str, *, local: bool = False) -> list:
    """Read-only. [{key, kind: phrase|category, label, dismissed_count, scope, flag_ids, message}], phrase suggestions first."""
    hist = _history(conn, case_id, local)
    phrase_n, cat_n = {}, {}
    for f in hist:
        pid, _ = _phrase(f)
        if pid:
            phrase_n[pid] = phrase_n.get(pid, 0) + 1
        cat_n[f["category"]] = cat_n.get(f["category"], 0) + 1
    out, covered = [], set()
    pend = [(f, *_phrase(f)) for f in _pending(conn, case_id)]
    scope = "all cases on this computer" if local else "this case"
    for pid in sorted({p for _, p, _ in pend if p and phrase_n.get(p, 0) >= PHRASE_MIN}):
        ids = [f["id"] for f, p, _ in pend if p == pid]
        label = next(t for _, p, t in pend if p == pid)
        out.append(_row(f"phrase:{pid}", "phrase", label, phrase_n[pid], scope, ids))
        covered.update(ids)
    for cat in sorted({f["category"] for f, _, _ in pend if cat_n.get(f["category"], 0) >= CATEGORY_MIN}):
        ids = [f["id"] for f, _, _ in pend if f["category"] == cat and f["id"] not in covered]
        if ids:
            out.append(_row(f"category:{cat}", "category", cat.replace("_", " "), cat_n[cat], scope, ids))
    return out


def _row(key, kind, label, n, scope, ids):
    return {"key": key, "kind": kind, "label": label, "dismissed_count": n, "scope": scope, "flag_ids": ids, "auto_applied": False,
            "message": f"You dismissed this kind of flag {n} times. Hide similar ones in this case?"}


def apply(conn, case_id: str, key: str, *, local: bool = False, now=None) -> dict:
    """The paralegal accepted the suggestion: dismiss the matching pending flags in THIS case through the normal review path.
    Raises KeyError when the key is not a current suggestion (nothing is written)."""
    s = next((x for x in suggest(conn, case_id, local=local) if x["key"] == key), None)
    if s is None:
        raise KeyError(key)
    for fid in s["flag_ids"]:
        review.apply_review(conn, case_id, fid, {"action": "dismiss", "note": APPLIED_NOTE}, now=now)
    return {"key": key, "dismissed_flag_ids": s["flag_ids"], "suggestions": suggest(conn, case_id, local=local)}


def add_routes(app, *, conn, get_case, body_of, ApiError, now, local_mode):
    @app.get("/api/cases/{token}/dismissal_suggestions")
    def dismissal_suggestions(token: str):
        c = conn()
        try:
            get_case(c, token)
            return {"suggestions": suggest(c, token, local=local_mode()), "min_phrase": PHRASE_MIN, "min_category": CATEGORY_MIN}
        finally:
            c.close()

    @app.post("/api/cases/{token}/dismissal_suggestions/apply")
    async def dismissal_suggestions_apply(token: str, request: Request):
        b = await body_of(request)
        if not isinstance(b.get("key"), str):
            raise ApiError(400, "bad_request", "Send the key of the suggestion to apply.")
        c = conn()
        try:
            get_case(c, token)
            try:
                return apply(c, token, b["key"], local=local_mode(), now=now)
            except KeyError:
                raise ApiError(404, "not_found", "That suggestion no longer applies.") from None
        finally:
            c.close()
