"""Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).

Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
Edit order: (1) structure, else 422 invalid_edit; (2) code checks (D-034/D-047): a number, date or $ figure, a side/negation word (left, right,
no, not, without) that is not in the quote, a qualifier of the quote that the summary drops, or a highlight that cannot be found is a hard 422
invalid_edit and nothing is saved; there is no confirm or override path (no 409). (3) judge 1 re-run: it never blocks a human-written edit
(D-045b); an objection or an unavailable judge saves the edit as needs_review and is returned in warnings[] (JUDGE_PARTIAL, JUDGE_UNSUPPORTED,
JUDGE_UNAVAILABLE).
"""
import copy
import json
import time

from app.backend import amounts as AM, charge_text, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store, why
from app.db import db as DB
from app.llm import audited as AU

ACTIONS = ("accept", "dismiss", "reset", "edit", "count")      # count (D-064): an amount held back for a missing detail becomes an accepted charge, see count_charge.py
# "may" is not here: grounding never reports the month May as a token, so a "may" token is the hedge word
_NUMERIC_TOKEN = __import__("re").compile(r"\d|^(?:january|february|march|april|june|july|august|september|october|november|december)$", __import__("re").IGNORECASE)
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


def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
    """D-041: an entry whose date is not confirmed (ambiguous, missing, or no date at all) cannot go into the letter. Same rule as
    present.case_view uses to put an entry under `undated_entries`: date_iso set and the record's date_status parsed or confirmed."""
    if kind != "entry":
        return False
    if not item.get("date_iso"):
        return True
    rid = (item.get("record_ids") or [None])[0]
    row = conn.execute("SELECT date_status FROM records WHERE id=? AND case_id=?", (rid, case_id)).fetchone()
    return bool(row) and row["date_status"] not in ("parsed", "confirmed", None)


def _date_unconfirmed_error():
    return ReviewError(422, "DATE_UNCONFIRMED", message="Confirm this entry's date first (Dates to confirm). An entry with no confirmed date "
                       "cannot be accepted into the letter.")


# D-051: the code rung binds accept for every item, AI-made or human. These are the code checks on an entry's current wording.
CODE_CHECK_REASONS = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "GROUNDING_EXCERPT_NOT_VERBATIM", "EXCERPT_NOT_WHOLE_SENTENCE", "EXCERPT_OMITS_QUALIFIER",
                      "HIGHLIGHT_NOT_FOUND")
CODE_CHECK_STEP = {"SUMMARY_TOKEN_NOT_IN_EXCERPT": "summary_tokens", "SUMMARY_DROPS_QUALIFIER": "summary_qualifier", "GROUNDING_EXCERPT_NOT_VERBATIM": "excerpt_verbatim",
                   "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge", "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight"}
QUOTE_LEVEL_REASONS = ("GROUNDING_EXCERPT_NOT_VERBATIM", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND")   # only a change to the QUOTE clears these
EDIT_SUMMARY_TEXT = "Edit the summary to match the quote"
EDIT_QUOTE_TEXT = "Change the quote to whole sentences of the record that keep the hedge sentence"
# plain words for "AI wording removed (failed a check: ...)" in the internal notes
CHECK_PHRASE = {"SUMMARY_TOKEN_NOT_IN_EXCERPT": "a number or word in it is not in the quote", "SUMMARY_DROPS_QUALIFIER": "it drops a qualifier the quote has",
                "GROUNDING_EXCERPT_NOT_VERBATIM": "the quote is not word for word in the record", "EXCERPT_OMITS_QUALIFIER": "the quote leaves out a hedge sentence",
                "EXCERPT_NOT_WHOLE_SENTENCE": "the quote is not whole sentences", "HIGHLIGHT_NOT_FOUND": "the quote cannot be found in the record"}


def current_text(item: dict):
    ed = item.get("edited") or {}
    return ed.get("summary", item.get("summary") or ""), ed.get("excerpt", item.get("excerpt") or "")


def edit_unconfirmed(kind: str, item: dict) -> bool:
    """T-134 (D-045b, D-051): an ENTRY the paralegal reworded or re-quoted whose state is still needs_review (the second check did not run or did not agree, or another
    reason such as OCR or a translation keeps it open). Her edit saved it, but she has not yet said she compared it with the quote, so it has not been decided: it is
    not in the letter, not counted as accepted, and the notes do not say she accepted it. Her explicit accept (review_status accepted) ends it; that accept is bound
    by the code checks (set_review). One source for the item view, the review counts, the export and the gate."""
    return (kind == "entry" and item.get("review_status") == "edited" and item.get("state") == "needs_review"
            and any(k in (item.get("edited") or {}) for k in ("summary", "excerpt")))


def code_check_failures(rec, item: dict) -> dict:
    """{reason_code: detail} for every D-034/D-047/D-022 code check the entry's CURRENT summary and quote fail. Recomputed from the text (same
    functions the generator and the edit route use), plus any such reason already stored on the item, so old data cannot slip through.
    `rec` is a store.load_records() dict (None: only the stored reasons count)."""
    out = {}
    summ, exc = current_text(item)
    if rec is not None:
        g = spanish.module_for(language.record_lang(rec))
        toks = g.new_tokens(summ, exc, rec.get("source") or item.get("provider") or "", rec.get("date_iso") or item.get("date_iso") or "")
        if toks:
            out["SUMMARY_TOKEN_NOT_IN_EXCERPT"] = {"tokens": toks}
        dropped = g.dropped_qualifiers(summ, exc)
        if dropped:
            out["SUMMARY_DROPS_QUALIFIER"] = {"qualifiers": list(dropped)}
        for c in g.check_excerpt(rec["excerpt"], exc):             # the quote against its record: word for word, whole sentences, keeps the hedge sentence
            if c in ("GROUNDING_EXCERPT_NOT_VERBATIM", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE"):
                out[c] = {}
        if grounding.locate(rec["excerpt"], exc) is None and "GROUNDING_EXCERPT_NOT_VERBATIM" not in out:
            out["HIGHLIGHT_NOT_FOUND"] = {}
    for c in item.get("state_reasons") or []:
        if c in CODE_CHECK_REASONS:
            out.setdefault(c, {})
    return {c: out[c] for c in CODE_CHECK_REASONS if c in out}


def code_check_message(fails: dict) -> str:
    """Plain words for the first failing check, then the next step."""
    c = next(iter(fails))
    d = fails[c]
    if c == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and d.get("tokens"):
        toks = d["tokens"]
        if any(_NUMERIC_TOKEN.search(t) for t in toks):
            what = "The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(toks) + "."
        else:
            what = "The summary says " + _quoted_words(toks) + ", which the quote does not say."
    elif c == "SUMMARY_DROPS_QUALIFIER" and d.get("qualifiers"):
        what = "The quote carries " + "; ".join(_QUALIFIER_WORDS.get(k, k) for k in d["qualifiers"]) + " that the summary leaves out."
    elif c == "GROUNDING_EXCERPT_NOT_VERBATIM":
        what = "The quote is not word for word in the record."
    elif c == "EXCERPT_OMITS_QUALIFIER":
        what = "The quote leaves out a hedge sentence that qualifies it."
    elif c == "EXCERPT_NOT_WHOLE_SENTENCE":
        what = "The quote does not start and end on whole sentences."
    elif c == "HIGHLIGHT_NOT_FOUND":
        what = "The quote cannot be found in the record, so it cannot be highlighted."
    else:
        what = "The summary does not match the quote."
    return f"{what} {EDIT_QUOTE_TEXT if c in QUOTE_LEVEL_REASONS else EDIT_SUMMARY_TEXT}."


def code_check_detail(item_id: str, fails: dict) -> dict:
    first = next(iter(fails))
    return {"item_id": item_id, "reason_code": first, "step_id": CODE_CHECK_STEP[first], "failed_steps": [CODE_CHECK_STEP[c] for c in fails],
            "tokens": (fails.get("SUMMARY_TOKEN_NOT_IN_EXCERPT") or {}).get("tokens", []),
            "next_action": ({"code": "EDIT_QUOTE", "text": EDIT_QUOTE_TEXT, "target": {"item_id": item_id}} if first in QUOTE_LEVEL_REASONS
                            else {"code": "EDIT_SUMMARY", "text": EDIT_SUMMARY_TEXT, "target": {"item_id": item_id}})}


def code_check_error(item_id: str, rec, item: dict):
    """A 422 ReviewError (code CODE_CHECK_FAILED) if the entry's current wording fails a code check, else None. Accept never goes past it (D-051)."""
    fails = code_check_failures(rec, item)
    if not fails:
        return None
    return ReviewError(422, "CODE_CHECK_FAILED", code_check_detail(item_id, fails), code_check_message(fails))


def bill_state_for(conn, case_id: str, record_ids) -> str:
    """T-139 r3: charge_text.bill_state of the amount items on these records (where the figures of a held entry are counted). One query."""
    ids = set(record_ids or [])
    return charge_text.bill_state([a for a in DB.list_items(conn, case_id, "amount") if ids & set(a.get("record_ids") or [])])


def charge_text_error(item_id: str, item: dict, state_fn=None):
    """T-139 (D-019, R-CH-7): a 422 CODE_CHECK_FAILED naming CHARGE_TEXT_IN_ENTRY when the entry's CURRENT summary or quote states a dollar amount, else None.
    Same shape as the D-051 code checks, so the UI that handles them handles this one. Code only (app/backend/charge_text.py)."""
    summ, exc = current_text(item)
    found = charge_text.check(summ, exc)
    if not found:
        return None
    code = charge_text.next_action_code(found)
    text = EDIT_QUOTE_TEXT if code == "EDIT_QUOTE" else EDIT_SUMMARY_TEXT
    detail = {"item_id": item_id, "reason_code": "CHARGE_TEXT_IN_ENTRY", "step_id": "charge_text", "failed_steps": ["charge_text"], "tokens": [],
              "amounts": list(dict.fromkeys(found.get("excerpt", []) + found.get("summary", []))),
              "next_action": {"code": code, "text": "Pick a quote that does not state the amount" if code == "EDIT_QUOTE" else text, "target": {"item_id": item_id}}}
    return ReviewError(422, "CODE_CHECK_FAILED", detail, charge_text.message(found, state_fn() if state_fn else None))


def hold_hints(conn, case_id: str, entry_views: list) -> None:
    """T-139 r3: the `why` of an entry held for CHARGE_TEXT_IN_ENTRY says where THIS record's figures are counted (charge_text.hold_why), never that a bill's charges are
    listed when none is. Edits the views in place; only entries whose reasons carry the code are touched."""
    held = [v for v in entry_views if "CHARGE_TEXT_IN_ENTRY" in (v.get("reasons") or [])]
    if not held:
        return
    amts = DB.list_items(conn, case_id, "amount")
    static = why.why("CHARGE_TEXT_IN_ENTRY")
    for v in held:
        ids = set(v.get("record_ids") or [])
        found = charge_text.check(v.get("summary"), v.get("excerpt")) or {"summary": ["amount"]}
        new = charge_text.hold_why(found, charge_text.bill_state([a for a in amts if ids & set(a.get("record_ids") or [])]))
        v["why"] = v["why"].replace(static, new) if static in v["why"] else v["why"]


def entry_record(item: dict, recs: list):
    rid = (item.get("record_ids") or [None])[0]
    return next((r for r in recs if r["id"] == rid), None)


def confirm_error(item_id: str, item: dict, confirm):
    """D-059: a charge that carries a likely_duplicate or likely_total flag is accepted only when the call names that flag (`confirm`). A 422 CONFIRM_REQUIRED
    with the flag and the exact word to send, else None. Code only: the flag was set by amounts.py, not by a model, and a judge answer does not clear it."""
    f = (item.get("ladder") or {}).get("confirm")
    if item.get("kind") != "charge" or not f or confirm == f["confirm_with"]:
        return None
    detail = {"item_id": item_id, "reason_code": "CONFIRM_REQUIRED", "flag": f["flag"], "name": f["name"], "confirm_with": f["confirm_with"], "of": f.get("of"),
              "message": f["message"],      # T-159: the flag's own sentence, without the "confirm by name" tail, so a client never strips the token out of the error message
              "next_action": {"code": "CONFIRM_FLAG", "text": "Confirm the flag by name, or dismiss the charge", "target": {"item_id": item_id}}}
    wrong = "" if confirm is None else " The confirm you sent does not name this flag."
    return ReviewError(422, "CONFIRM_REQUIRED", detail, f"{f['name']}: {f['message']} It is not counted unless you confirm that flag by name ({f['confirm_with']}).{wrong}")


def confirmed_accept(item: dict) -> bool:
    """T-159: a charge that is accepted and whose flag has been confirmed by name. A repeat accept of it changes nothing, so it writes nothing."""
    f = (item.get("ladder") or {}).get("confirm")
    return item.get("kind") == "charge" and bool(f) and bool(f.get("confirmed_at")) and item.get("review_status") == "accepted"      # item["kind"] = the amount's class


def _record_confirm(conn, case_id: str, item_id: str, item: dict, t) -> None:
    """The named confirm is kept on the item (ladder.confirm.confirmed_at) and in the accept event that carried it (after.confirm = {flag, name, confirmed_at}),
    so GET /audit shows who confirmed which flag and when without reading the item (T-159, D-059). Both writes are ONE transaction: a failure on either leaves neither."""
    f = (item.get("ladder") or {}).get("confirm")
    if item.get("kind") == "charge" and f:
        stamp = {"flag": f["flag"], "name": f["name"], "confirmed_at": store.iso(t)}
        conn.execute("BEGIN")
        try:
            DB.update_item(conn, item_id, now=t, case=case_id, ladder={**item["ladder"], "confirm": {**f, "confirmed_at": stamp["confirmed_at"]}})
            ev = conn.execute("SELECT id, after_json FROM review_events WHERE case_id=? AND item_id=? AND action='accept' ORDER BY at DESC, rowid DESC LIMIT 1", (case_id, item_id)).fetchone()
            if ev:
                after = json.loads(ev["after_json"]) if ev["after_json"] else {}
                conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "confirm": stamp}), ev["id"]))
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise


def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None, compared=None) -> dict:
    """THE one place a review decision is written (DB.apply_review is called from here for accept, edit, dismiss, reset and the batch).
    D-051: whenever the decision leaves an ENTRY accepted or edited (so in the letter), the code checks are recomputed from the wording that
    decision would leave (`edited` replaces the current text; stored code reasons are dropped because the new text is what counts) and a
    failure is a 422 CODE_CHECK_FAILED before anything is written. The judge verdict, the stored state and who wrote the wording do not matter."""
    if kind is None or item is None:
        kind, item = _item(conn, case_id, item_id)
    if kind == "entry" and DB.ACTIONS.get(action) in ("accepted", "edited"):
        cand = dict(item)
        if edited is not None:
            cand["edited"] = edited
            cand["state_reasons"] = [c for c in item.get("state_reasons") or [] if c not in CODE_CHECK_REASONS]
        err = code_check_error(item_id, entry_record(cand, recs if recs is not None else store.load_records(conn, case_id)), cand) or charge_text_error(item_id, cand, lambda: bill_state_for(conn, case_id, item.get("record_ids")))
        if err:
            raise err
    if action == "accept" and (err := compare_error(item_id, item, compared, conn, case_id)):      # D-066: after the code checks (they refuse first), before any write
        raise err
    if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
        if confirmed_accept(item):
            return item                                     # T-159: already accepted with its flag confirmed; a repeat accept writes no second decision
        err = confirm_error(item_id, item, confirm)         # D-059
        if err:
            raise err
    out = DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)
    if action == "accept" and compared is True and judge_dispute(item):
        try:
            _record_compared(conn, case_id, item_id, now)       # D-066 r2: only a real compare is stamped; a failed stamp takes the accept back, so nothing disputed is accepted without it on record
        except Exception:
            _take_back(conn, case_id, item_id, item, now)
            raise
        out = DB.get_item(conn, item_id, case_id)
    if kind == "amount" and DB.ACTIONS.get(action) == "accepted":
        try:
            _record_confirm(conn, case_id, item_id, item, now)
        except Exception:
            _take_back(conn, case_id, item_id, item, now)      # T-159 r2: take the accept back, so no charge counts without its confirm on record
            raise
        out = DB.get_item(conn, item_id, case_id)
    return out


def _take_back(conn, case_id: str, item_id: str, item: dict, now) -> None:
    """Undo an accept whose stamp (compare or confirm) could not be written: back to the status the item had before."""
    back = {"pending": "reset", "dismissed": "dismiss", "edited": "edit"}.get(item.get("review_status"))
    if back:
        DB.apply_review(conn, item_id, back, now=now, case=case_id)


STALE_MESSAGE = "This item changed in another tab; reload to see it."
_TARGET_STATUS = {"accept": "accepted", "dismiss": "dismissed", "reset": "pending"}


def check_fresh(item: dict, body: dict, action: str) -> None:
    """T-178 (GATE-M3 chaos): a decision made from a stale screen must not silently override a newer one. The client sends what it last saw of the item: `version` (the item's
    `version` field, its last-change time) and/or `expected_status` (its `review_status`). If either differs from the stored row the write is refused with 409 `stale_item`
    and nothing changes. Neither sent = no check (older clients). A re-assertion that would leave the item exactly as it is (accept on an accepted item, dismiss on a
    dismissed one, reset on a pending one) is harmless and is let through."""
    ver, exp = (body or {}).get("version"), (body or {}).get("expected_status")
    if ver is None and exp is None:
        return
    if exp is not None and exp not in ("pending", "accepted", "edited", "dismissed"):
        raise _bad("The expected_status must be one of pending, accepted, edited or dismissed.")
    if ver is not None and (isinstance(ver, bool) or not isinstance(ver, (int, float))):
        raise _bad("The version must be the number the item was last shown with.")
    stale = (exp is not None and exp != item["review_status"]) or (ver is not None and abs(float(ver) - float(item.get("updated_at") or 0)) > 1e-6)
    if stale and _TARGET_STATUS.get(action) != item["review_status"]:
        raise ReviewError(409, "stale_item", {"item_id": item["id"], "review_status": item["review_status"], "version": item.get("updated_at")}, STALE_MESSAGE)


_DISPUTED = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES"}
_DISPUTE_SENTENCE = {"partially": "The second AI check found this only partly supported by the quote.", "unsupported": "The second AI check found this not supported by the quote.",
                     "disagrees": "The second AI check disagreed with the first result for this item."}
_DISPUTE_SENTENCE_PREPARED = {"partially": "A second check found this only partly supported by the quote.", "unsupported": "A second check found this not supported by the quote.",      # D-069
                              "disagrees": "A second check disagreed with the first result for this item."}


def judge_dispute(item: dict):
    """D-066: the second check's objection to this item, as its ladder verdict (partially | unsupported | disagrees), else None. The verdict on the item's ladder or any of the
    three JUDGE_* reasons counts; unsure and unavailable are not an objection. Code only."""
    j = (item.get("ladder") or {}).get("judge")
    v = j.get("verdict") if isinstance(j, dict) else None
    v = "disagrees" if v == "disagree" else v        # the amount-class judge says "disagree"
    if v in _DISPUTED:
        return v
    reasons = item.get("state_reasons") or []
    return next((k for k, code in _DISPUTED.items() if code in reasons), None)


def compare_error(item_id: str, item: dict, compared, conn=None, case_id=None):
    """D-066: accepting an item the second check disputed needs the explicit statement that she compared it with the quote (`compared: true`). 422 COMPARE_REQUIRED without it."""
    v = judge_dispute(item)
    if not v or compared is True or item.get("review_status") == "accepted":
        return None
    prep = False
    if conn is not None:
        from app.backend import present          # lazy: present imports review
        prep = present.Prov(conn, case_id).prepared(item)      # D-069: the sentence follows the item's provenance
    return ReviewError(422, "COMPARE_REQUIRED", {"item_id": item_id, "reason_code": "COMPARE_REQUIRED", "verdict": v,
                       "next_action": {"code": "COMPARE_WITH_QUOTE", "text": "Read it against the quote, then say you compared it", "target": {"item_id": item_id}}},
                       (_DISPUTE_SENTENCE_PREPARED if prep else _DISPUTE_SENTENCE)[v] + " Read it against the quote, then say you compared it before you accept it.")


def _record_compared(conn, case_id: str, item_id: str, t) -> None:
    """D-066: her statement is kept in the accept event that carried it (after.compared = {at}), so the audit shows it."""
    ev = conn.execute("SELECT id, after_json FROM review_events WHERE case_id=? AND item_id=? AND action='accept' ORDER BY at DESC, rowid DESC LIMIT 1", (case_id, item_id)).fetchone()
    if ev:
        after = json.loads(ev["after_json"]) if ev["after_json"] else {}
        conn.execute("BEGIN")
        try:
            conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "compared": {"at": store.iso(t)}}), ev["id"]))
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise


def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
        raise _bad("That action is not allowed.")
    check_fresh(item, body, action)
    if action == "count":
        from app.backend import count_charge          # lazy: count_charge imports review
        return count_charge.count(conn, case_id, item_id, body, now=t)
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
        raise _date_unconfirmed_error()
    warnings = []
    if action in ("accept", "dismiss", "reset"):
        confirm = body.get("confirm")
        if confirm is not None and not isinstance(confirm, str):
            raise _bad("The confirm must be the name of the flag.")
        compared = body.get("compared")
        if compared is not None and not isinstance(compared, bool):
            raise _bad("The compared flag must be true or false.")
        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm, compared=compared)
        if action == "reset":
            restore_pre_edit(conn, case_id, item_id, kind, item, t)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}


def ocr_record_ids(conn, case_id: str) -> set:
    """Ids of the records whose text lies on an OCR-read page of this case (empty for a text case). T-086, D-042."""
    from app.backend import pdf_checks
    pages = (DB.get_case(conn, case_id).get("config") or {}).get("pages")
    if not any(p.get("source") == "ocr" for p in pages or []):
        return set()
    return {r[0] for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=?", (case_id,))
            if pdf_checks.is_ocr_span(pages, r[1], r[2])}


def enforce_ocr(conn, case_id: str, t) -> int:
    """T-086/D-042 invariant, applied after every step that rewrites an item's state (edit, manual entry, not-a-duplicate, date confirm,
    reclassify): an item whose record is on an OCR-read page is needs_review with OCR_DERIVED (rejected items stay rejected). A human edit
    does not show the page image was compared, so it never clears this. Idempotent; returns how many items it had to fix."""
    ids = ocr_record_ids(conn, case_id)
    if not ids:
        return 0
    n = 0
    for kind in ("entry", "amount", "flag"):
        for it in DB.list_items(conn, case_id, kind):
            if it["state"] == "rejected" or not ids.intersection(it.get("record_ids") or []):
                continue
            reasons = list(it.get("state_reasons") or [])
            if it["state"] == "needs_review" and "OCR_DERIVED" in reasons:
                continue
            if "OCR_DERIVED" not in reasons:
                reasons.append("OCR_DERIVED")
            out = {"state": "needs_review", "state_reasons_json": reasons}
            if isinstance(it.get("ladder"), dict):
                out["ladder"] = {**it["ladder"], "state": "needs_review"}
            DB.update_item(conn, it["id"], now=t, case=case_id, **out)
            n += 1
    return n


_QUALIFIER_WORDS = {"hedge": "a hedge (such as may, possible or appears)", "self_report": "a phrase that says whose account the quote gives", "negation": "a negation (such as no, not or denies)",
                    "laterality": "a side (left or right)", "approx": "an approximation (such as approximately)"}


def _quoted_words(toks) -> str:
    q = ["\u201c" + t + "\u201d" for t in toks]
    return q[0] if len(q) == 1 else ", ".join(q[:-1]) + " and " + q[-1]


def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, ocr_derived=False, bill_state=None, prep=False):
    """Code checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
    D-034/D-047: a number/date/$ figure, a side or negation word that is not in the quote, a qualifier the summary drops, or a highlight that
    cannot be found raises a hard 422 invalid_edit before anything is stored or any judge call is made. No confirm or override exists.
    The judge never blocks (D-045b): its objection is returned in `warnings` and the item is stored as needs_review."""
    code_reasons = []
    lang = language.record_lang(rec)                        # D-042: a Spanish record's English summary is checked against the Spanish quote
    g = spanish.module_for(lang)
    toks = g.new_tokens(new_sum, new_exc, label, date_iso)
    numeric = [t for t in toks if _NUMERIC_TOKEN.search(t)]
    if numeric:
        raise _bad("The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(numeric) + ". Remove it or change the quote.",
                   tokens=numeric, reason="SUMMARY_NUMBER_NOT_IN_EXCERPT")
    if toks:
        words = _quoted_words(toks)
        raise _bad(f"The summary says {words}, which the quote does not say. Remove it or change the quote.", tokens=toks, reason="SUMMARY_TOKEN_NOT_IN_EXCERPT")
    dropped = g.dropped_qualifiers(new_sum, new_exc)
    if dropped:
        what = "; ".join(_QUALIFIER_WORDS.get(k, k) for k in dropped)
        raise _bad(f"The quote carries {what} that the summary leaves out. Put it back in the summary.", qualifiers=list(dropped), reason="SUMMARY_DROPS_QUALIFIER")
    found = charge_text.check(new_sum, new_exc)             # T-139 (D-019, R-CH-7): an amount in the summary or the quote never reaches the letter
    if found:
        raise _bad(charge_text.message(found, bill_state() if callable(bill_state) else bill_state), amounts=list(dict.fromkeys(found.get("excerpt", []) + found.get("summary", []))), reason="CHARGE_TEXT_IN_ENTRY")
    if span is None:
        raise _bad("The quoted sentences cannot be found in the record, so they cannot be highlighted. Change the quote.", reason="HIGHLIGHT_NOT_FOUND")
    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
    if call is not None:
        verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
        ladder_verdict = judges.to_ladder("j1", verdict)
    warnings = []
    if ladder_verdict in ("partially", "unsupported"):
        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
        warnings.append({"code": code, "message": "The second check could not fully support the summary from the quote; the item stays marked for review.", "item_id": item_id})
    elif ladder_verdict == "unavailable":
        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": why.unavailable_sentence({"verdict": "unavailable", "reason_code": judge_code, "error_class": judge_error}, prep) + " Until you do, the item stays marked for review.", "item_id": item_id})
    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed"), "ocr_derived": ocr_derived,
                                               "translated": language.translated_record(rec)})      # D-050: an edit or a manual entry over a Spanish quote is still never verified
    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
            "judge_error": judge_error, "state": state, "reasons": reasons}


# ---------------------------------------------------------------- edit
def _edit(conn, case_id, kind, item, body, call, t):
    edits = body.get("edits")
    if kind == "amount":
        raise _bad("A charge can only be accepted or dismissed.")
    if not isinstance(edits, dict) or not edits:
        raise _bad("Nothing to edit.")
    if kind == "flag":
        if set(edits) != {"note"} or not isinstance(edits["note"], str) or not edits["note"].strip():
            raise _bad("Only a note can be added to a flag.")
        set_review(conn, case_id, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, kind="flag", item=item)
        DB.update_item(conn, item["id"], now=t, case=case_id, reviewer_note=edits["note"].strip()[:2000])
        return []
    if not set(edits) <= {"summary", "excerpt"} or not all(isinstance(v, str) and v.strip() for v in edits.values()):
        raise _bad("Only the summary or the quoted sentences of an entry can be edited.")
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    rec = next((r for r in recs if r["id"] == (item["record_ids"] or [None])[0]), None)
    if rec is None:
        raise _bad("The entry's source record is missing.")
    prev = item.get("edited") or {}
    cur_sum, cur_exc = prev.get("summary", item["summary"]), prev.get("excerpt", item["excerpt"])
    new_sum, new_exc = edits.get("summary", cur_sum).strip(), edits.get("excerpt", cur_exc).strip()
    trimmed = None
    summary_before_trim = new_sum
    if "summary" not in edits and charge_text.has_currency(new_sum) and not charge_text.has_currency(new_exc):
        tr = charge_text.trim_summary(new_sum)          # T-139: the quote she picked no longer states the amount; code removes the trailing amount clause (D-054 suffix rule)
        if tr["changed"] and not charge_text.has_currency(tr["text"]):
            new_sum, trimmed = tr["text"], tr
    span = None
    if "excerpt" in edits:
        problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], new_exc)
        if problems:
            raise _bad("The quote must be whole sentences of the same record, in order, with any hedge sentence that qualifies them.", reasons=problems)
    span = grounding.locate(rec["excerpt"], new_exc)
    base = generator.body_offset(rec)
    label, date_iso = item["provider"] or "", item["date_iso"] or ""
    from app.backend import present          # lazy: present imports review
    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call, prep=present.Prov(conn, case_id).prepared(item),      # D-069 r5: the warning follows the item's provenance
                         ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []),
                         bill_state=lambda: bill_state_for(conn, case_id, item.get("record_ids")))
    toks, code_reasons, ladder_verdict, call_id, state, reasons = (
        chk["toks"], chk["code_reasons"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
    edited = dict(prev)
    edited.update(at=store.iso(t))
    edited.pop("code_trim", None)           # T-139 r3: the trace shows the removal only while the wording it made is still the wording (a later hand edit or quote change clears it)
    if trimmed:
        edited["code_trim"] = {"rule": "T-139", "removed": list(trimmed["removed"]), "summary_before": summary_before_trim, "summary_after": new_sum,
                               "quote_before": cur_exc, "quote_after": new_exc}
    if "summary" in edits or "summary" in prev or trimmed:
        edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
    if "excerpt" in edits or "excerpt" in prev:
        edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
    set_review(conn, case_id, item["id"], "edit", edited=edited, now=t, kind="entry", item=item, recs=recs)     # D-051: edit implies accept; refused before any write
    lad = item.get("ladder") or {"item_id": item["id"]}
    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
        lad["pre_edit"] = {"judge": copy.deepcopy(lad.get("judge")), "code_checks": copy.deepcopy(lad.get("code_checks")), "rejudge": copy.deepcopy(lad.get("rejudge")),
                           "state": item["state"], "state_reasons": list(item.get("state_reasons") or []), "lad_state": lad.get("state")}      # deep copies: the edit updates code_checks in place below
    lad.pop("rejudge", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none
    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
    lad["state"] = state
    lad["pre_edit"]["after"] = {"state": state, "state_reasons": list(reasons)}      # what the latest edit left, to tell later on whether anything else has changed the state since
    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
    enforce_ocr(conn, case_id, t)
    if trimmed:
        chk["warnings"].append({"code": "CHARGE_CLAUSE_REMOVED", "item_id": item["id"], "removed": trimmed["removed"],
                                "message": "Code removed the clause that stated a dollar amount from the summary (" + "; ".join(trimmed["removed"])
                                           + "). Amounts go only in the internal notes. Check the summary against the quote."})
    return chk["warnings"]


def restore_pre_edit(conn, case_id: str, item_id: str, kind: str, item: dict, t) -> bool:
    """T-138: undoing an edit puts the AI wording back WITH the second-check result and code-check record it had before the edit, so accept works as it did.
    The state and reasons come back too, unless something else has rewritten them since the edit (a date confirm, a rejudge): then only the judge result and
    code checks return and the state is left as it is. No snapshot (an edit saved before this change): nothing happens, as before. Returns True when restored."""
    lad = dict(item.get("ladder") or {})
    snap = lad.pop("pre_edit", None)
    if kind != "entry" or not snap:
        return False
    if snap.get("judge") is not None:
        lad["judge"] = snap["judge"]
    else:
        lad.pop("judge", None)
    if snap.get("code_checks") is not None:
        lad["code_checks"] = snap["code_checks"]
    if snap.get("rejudge"):
        lad["rejudge"] = snap["rejudge"]
    else:
        lad.pop("rejudge", None)
    fields = {}
    after = snap.get("after") or {}
    if after and item["state"] == after.get("state") and sorted(item.get("state_reasons") or []) == sorted(after.get("state_reasons") or []):
        fields = {"state": snap["state"], "state_reasons_json": list(snap["state_reasons"])}
        if snap.get("lad_state") is not None:
            lad["state"] = snap["lad_state"]
    DB.update_item(conn, item_id, now=t, case=case_id, ladder=lad, **fields)
    enforce_ocr(conn, case_id, t)
    return True


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
    moved, cleared = None, []
    for e in DB.list_items(conn, case_id, "entry"):
        if record_id in (e["record_ids"] or []):
            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso, **_without_date_doubt(e))
            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
                cleared.append(e["id"])
            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
    for a in DB.list_items(conn, case_id, "amount"):
        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
            DB.update_item(conn, a["id"], now=t, case=case_id, **_without_date_doubt(a))
            cleared.append(a["id"])
    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
    gap_changes = []
    removed += _recompute_gaps(conn, case_id, t, gap_changes)
    for ch in gap_changes:
        ch["record_seq"] = rec["seq"]
        ch["sentence"] = _gap_change_sentence(ch, rec["seq"])
    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t, gap_changes)
    enforce_ocr(conn, case_id, t)
    from app.backend import present
    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
            "removed_flag_ids": removed, "gap_changes": gap_changes,
            "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}


def _without_date_doubt(item: dict) -> dict:
    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
    if (item.get("ladder") or {}).get("translation") is not None and "AI_TRANSLATION" not in reasons:      # D-050: confirming a date never verifies a translation
        reasons.append("AI_TRANSLATION")
    state = item["state"]
    if state == "needs_review" and not reasons:
        state = "verified"
    out = {"state": state, "state_reasons_json": reasons}
    if isinstance(item.get("ladder"), dict):
        out["ladder"] = {**item["ladder"], "state": state}
    return out


def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t, gap_changes=()):
    after = {"date_chosen": date_iso, "date_raw": rec["date_raw"], "candidates": rec["date_candidates"], "record_id": rec["id"],
             "cleared_date_ambiguous": cleared, "gap_changes": list(gap_changes)}       # T-127: the change is kept with the case; GET case reads it back (present.gap_change_index)
    before = {"date_status": "ambiguous", "date_iso": rec.get("date_iso")}
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                 (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))


def _drop(conn, case_id, flag_id):
    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
    return [flag_id] if cur.rowcount else []


def _gap_figures(flag: dict) -> dict:
    c = flag.get("computed") or {}
    return {"flag_id": flag["id"], "from": c.get("from_date"), "to": c.get("to_date"), "days": c.get("days"), "record_nos": list(c.get("record_nos") or [])}


def _gap_changes(old: dict, new: dict) -> list:
    """Which gap figures a recompute changed (T-114). `old`/`new` map flag id -> _gap_figures. A gap whose id survives and whose figures moved is `changed`; an
    old gap that vanished and a new one that shares a record number with it are ONE `changed` entry (an endpoint moved); the rest are `removed` / `added`.
    Each: {flag_id, change, old_days, new_days, old_from, old_to, new_from, new_to}; the side that does not exist is null. Code over the figures, never a model."""
    rows = []
    fresh = [n for i, n in new.items() if i not in old]
    for i, n in new.items():
        o = old.get(i)
        if o is not None and any(o[k] != n[k] for k in ("from", "to", "days")):
            rows.append(("changed", o, n))
    for i, o in old.items():
        if i in new:
            continue
        mate = next((n for n in fresh if set(n["record_nos"]) & set(o["record_nos"])), None)
        if mate is not None:
            fresh.remove(mate)
        rows.append(("changed" if mate else "removed", o, mate))
    rows += [("added", None, n) for n in fresh]
    nul = {"flag_id": None, "from": None, "to": None, "days": None}
    return [{"flag_id": (n or o)["flag_id"], "change": ch, "old_days": (o or nul)["days"], "new_days": (n or nul)["days"],
             "old_from": (o or nul)["from"], "old_to": (o or nul)["to"], "new_from": (n or nul)["from"], "new_to": (n or nul)["to"]} for ch, o, n in rows]


def _gap_change_sentence(ch: dict, seq) -> str:
    """The plain-words line the UI can announce. The numbers come from the figures in the entry, not from a model."""
    if ch["change"] == "removed":
        return f"A gap of {ch['old_days']} days no longer applies after you confirmed the date of record {seq}."
    if ch["change"] == "added":
        return f"A gap of {ch['new_days']} days now applies after you confirmed the date of record {seq}."
    return f"Gap recalculated after you confirmed record {seq}: now {ch['new_days']} days (was {ch['old_days']})."


def _recompute_gaps(conn, case_id, t, changes=None):
    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
    and note; a changed one restarts as pending; one that no longer exists is dropped (ADR-002). `changes` (a list) receives the gap figures that moved (T-114)."""
    from app.backend import pipeline as PL
    before = {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}
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
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names", "endpoint_warnings", "conditional"):
            if k in f:
                item[k] = f[k]
        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
        new[item["id"]] = item
    removed = []
    for old in DB.list_items(conn, case_id, "flag"):
        if old["origin"] != "code" or old["type"] not in ("gap", "conflict"):
            continue
        item = new.get(old["id"])
        if item is None:
            conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (old["id"], case_id))
            removed.append(old["id"])
            continue
        oc = old.get("computed") or {}
        DB.update_item(conn, old["id"], now=t, case=case_id, **PL._row("flag", item))
        if old["review_status"] != "pending" and any(oc.get(k) != item.get(k) for k in ("from_date", "to_date", "days", "stated_dates", "first_treatment_date")):
            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
    have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
    for iid, item in new.items():
        if iid not in have:
            DB.add_item(conn, case_id, "flag", {"id": iid, **PL._row("flag", item)}, now=t)
    if changes is not None:
        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
    return removed


# ---------------------------------------------------------------- manual entry (D-031, T-056)
def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
    t = _now(now)
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    rec = next((r for r in recs if r["id"] == record_id), None)
    if rec is None:
        raise ReviewError(404, "not_found", message="No such record.")
    if rec.get("duplicate_of"):
        raise _bad("This record is merged into another; enter the entry on the record it duplicates.")
    live = [e for e in DB.list_items(conn, case_id, "entry") if record_id in (e["record_ids"] or []) and e["state"] != "rejected"]
    if live:
        raise _bad("This record already has an entry; edit that entry instead.")
    summary, excerpt = (body or {}).get("summary"), (body or {}).get("excerpt")
    if not all(isinstance(v, str) and v.strip() for v in (summary, excerpt)):
        raise _bad("Provide a summary and the quoted sentences.")
    summary, excerpt = summary.strip(), excerpt.strip()
    problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], excerpt)
    if problems:
        raise _bad("The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.", reasons=problems)
    span = grounding.locate(rec["excerpt"], excerpt)
    eid = f"e{rec['seq']}_m"
    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call, prep=AU.answers_prepared(),      # D-069 r5: the set in use decides the wording
                         ocr_derived=record_id in ocr_record_ids(conn, case_id), bill_state=lambda: bill_state_for(conn, case_id, [record_id]))
    base = generator.body_offset(rec)
    ladder = {"item_id": eid, "generator": None, "entered_by": "reviewer",
              "judge": {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
                        "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})},
              "code_checks": {"excerpt_verbatim": True, "excerpt_whole_sentence": True, "summary_tokens_not_in_excerpt": chk["toks"],
                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
                              "date_provider_from_header": True},
              "human": {"action": None, "edited_text": None, "at": None}, "state": chk["state"]}
    if language.is_translated(language.record_lang(rec)):      # the reviewer wrote this English summary of a Spanish (or unidentified-language) quote: labelled as the reviewer's translation (D-042)
        ladder["translation"] = {**spanish.translation_info(language.record_lang(rec), True), "human_written": True}
    DB.add_item(conn, case_id, "entry", {
        "id": eid, "record_ids_json": [record_id], "seq": rec["seq"], "date_iso": rec.get("date_iso"), "provider": rec["source"],
        "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
        "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
    enforce_ocr(conn, case_id, t)
    from app.backend import pipeline as PL
    PL.refresh_extract_error(conn, case_id)      # T-165: a case that failed only because this record had no entry no longer fails
    from app.backend import present
    return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": chk["warnings"]}


# ---------------------------------------------------------------- 'not a duplicate' (D-031, T-056)
def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
    """Undo one merge: the merged entry keeps its other records; `record_id` gets an entry of its own (generator + judge 1 over that record),
    its amounts come back, gap flags are recomputed, and the decision is remembered in the case config so a rerun keeps it. Logged as a
    `not_duplicate` event on the original entry."""
    from app.backend import pipeline as PL
    from app.llm import provider as P
    t = _now(now)
    kind, ent = _item(conn, case_id, entry_id)
    if kind != "entry":
        raise _bad("Only a merged entry can be split.")
    ids = list(ent["record_ids"] or [])
    if record_id not in ids or ids.index(record_id) == 0 or len(ids) < 2:
        raise _bad("That record is not one of the duplicates merged into this entry.")
    case = DB.get_case(conn, case_id)
    cfg = dict(case.get("config") or {})
    cfg["not_duplicates"] = sorted(set(cfg.get("not_duplicates", [])) | {record_id})
    DB.update_case(conn, case_id, config_json=cfg)
    conn.execute("UPDATE records SET duplicate_of=NULL WHERE id=? AND case_id=?", (record_id, case_id))
    DB.update_item(conn, entry_id, now=t, case=case_id, record_ids_json=[i for i in ids if i != record_id])
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    rec = next(r for r in recs if r["id"] == record_id)
    warns = []
    # the split-off record's own entry (code-checked, then judge 1; a failure leaves it visibly without an entry)
    if call is not None:
        e = generator.extract_one(rec, [rec["n"]], call=call, case_text=case["raw_text"])
        if "failure" in e:                              # never vanishes: a could-not-verify tray item with the reason, as the pipeline does (T-112 r2)
            f = generator.failure_entry(rec, [rec["n"]], e["failure"], e.get("detail"))
            f["ladder"]["backend"] = P.backend_name()
            _upsert(conn, case_id, "entry", PL._clean(f), t)
            prep = AU.answers_prepared()      # D-069: the set in use decides the wording of a message written now
            msg = (f"The record was split off. Code removed every part of {"the prepared summary" if prep else "the AI's summary"} that its quote does not support, so it is in the could-not-verify tray; "
                   "write its entry by hand." if e["failure"] == "SUMMARY_NOT_IN_QUOTE"
                   else f"The record was split off, but {'no prepared answer was usable for' if prep else 'the AI could not draft'} its entry; it is in the could-not-verify tray. Enter it by hand.")
            warns.append({"code": e["failure"], "message": msg, "item_id": f["id"]})
        else:
            if e["state"] != "rejected":
                generator.judge_entries([e], by_n, call=call, case_text=case["raw_text"])
            e["ladder"]["backend"] = P.backend_name()
            e.pop("_stage", None)
            _upsert(conn, case_id, "entry", PL._clean(e), t)
    else:
        warns.append({"code": "LLM_UNAVAILABLE", "message": "The record was split off; its entry has not been drafted yet.", "item_id": None})
    # its amounts come back as their own items (new ids; existing amounts keep theirs and their review status)
    sep = {int(str(i)[1:]) for i in cfg["not_duplicates"] if str(i)[1:].isdigit()}
    rows = [a for a in AM.extract_amounts(recs, separate=sep) if a["record_no"] == rec["n"]]
    new_items = [PL.amount_item(a, rec) for a in rows]
    ing = {"records": recs, "text": case["raw_text"]}
    for a in DB.list_items(conn, case_id, "amount"):
        if record_id in (a["record_ids"] or []):
            DB.update_item(conn, a["id"], now=t, case=case_id, record_ids_json=[i for i in a["record_ids"] if i != record_id], duplicate_note=None)
    dollars = [a for a in new_items if a["cls"] != "damages"]
    verdicts = judges_for(dollars, call, case["raw_text"])
    for a in new_items:
        _upsert(conn, case_id, "amount", PL._finish_amount(a, ing, verdicts.get(a["id"])), t)
    _recompute_gaps(conn, case_id, t)
    DB.apply_review(conn, entry_id, "not_duplicate", now=t, case=case_id)
    enforce_ocr(conn, case_id, t)
    from app.backend import present
    split_id = f"e{rec['n']}" if any(e["id"] == f"e{rec['n']}" for e in DB.list_items(conn, case_id, "entry")) else None
    return {"entry_ids": [entry_id] + ([split_id] if split_id else []), "item": present.item_view(conn, case_id, entry_id),
            "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": warns}


def _upsert(conn, case_id, kind, item, t):
    """Add or refresh ONE item without PL._persist's removal of other pending rows."""
    from app.backend import pipeline as PL
    row = PL._row(kind, item)
    if any(i["id"] == item["id"] for i in DB.list_items(conn, case_id, kind)):
        DB.update_item(conn, item["id"], now=t, case=case_id, **row)
    else:
        DB.add_item(conn, case_id, kind, {"id": item["id"], **row}, now=t)


def judges_for(dollars, call, case_text):
    if call is None or not dollars:
        return {}
    return judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars], call=call, case_text=case_text)


def batch_apply(conn, case_id: str, item_id: str, action: str, now: float, recs: list = None) -> None:
    """One audited status change for the batch endpoint (case_extras.apply_batch validates the whole batch first). review.py stays the only
    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
    set_review(conn, case_id, item_id, action, now=now, recs=recs)
