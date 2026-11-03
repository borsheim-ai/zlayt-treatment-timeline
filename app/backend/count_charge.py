"""Count an amount the code held back for a missing detail (D-064, GATE-M2 r2 paralegal major; amends D-059/D-060).

Two kinds of 'not counted' amount. (a) Rule-excluded (total, balance, payment, adjustment, credit, year-to-date, insurer restatement, a note restating the same
provider's bill, a second figure on a line ...): never countable. (b) Held back only because the line lacks something D-060 needs (no date of service, a document with no
bill header): the paralegal reads the line and counts it with the named confirm "separate_charge" ("I checked this is a separate charge for a service").
`POST /api/cases/{token}/items/{id}/review {"action": "count", "confirm": "separate_charge"}`:
  - the amount must be countable (amounts.not_counted, computed from the record, never from anything the client sends), else 422 NOT_COUNTABLE with the plain reason;
  - the named confirm is required, else 422 CONFIRM_REQUIRED and nothing changes;
  - a figure that would double another line (same service and amount, any record; a date only has to agree when both lines state one, so an UNDATED line matching an accepted charge
    or another countable line always matches) or equals the sum of its record's charges also needs that flag named in `confirm_flag`; `separate_charge` alone is never enough then;
  - then the amount becomes class `charge` and is accepted in one step; the letter total sums it like any accepted charge. Two audit events are written: the count
    (action `reclassify`, `after.event == "count"`, `after.confirm` = the flag she confirmed) and the accept (carries the confirm stamp of the flag the charge now holds).
No model is asked: the class is a code reading plus a human confirm (ladder steps a and c), so the item is human-decided like a hand-written entry and the second AI check is not required."""
from app.backend import amounts as AM, confidence, language, reclassify, review, store
from app.db import db as DB

CONFIRM = AM.SEPARATE_CHARGE
NAME = "Counted as a separate charge"
MESSAGE = ("You counted this line as a separate charge for a service. If you take the decision back, you confirm that again to count it. "
           "Counting a line that is not a separate charge would count the same money twice.")
REQUIRED = ("Count this line only if you checked that it is a separate charge for a service, and not a total or a repeat of another line. "
            f"Confirm that by name ({CONFIRM}) to count it.")


def _flag(confirmed_at=None) -> dict:
    return {"flag": CONFIRM, "name": NAME, "message": MESSAGE, "confirm_with": CONFIRM, "of": None, **({"confirmed_at": confirmed_at} if confirmed_at else {})}


def is_counted(row: dict) -> bool:
    """True for an amount the paralegal counted through this route (human-decided: no second AI check applies to it)."""
    return bool((row.get("ladder") or {}).get("counted"))


def _err(code: str, text: str, **detail):
    return review.ReviewError(422, code, {"reason_code": code, **detail}, text)


def count(conn, case_id: str, item_id: str, body: dict, *, now=None) -> dict:
    t = review._now(now)
    kind, row = review._item(conn, case_id, item_id)
    if kind != "amount":
        raise review._bad("Only a dollar figure can be counted as a charge.")
    if row["state"] == "rejected":
        raise review.ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    confirm = (body or {}).get("confirm")
    confirm_flag = (body or {}).get("confirm_flag")
    for v in (confirm, confirm_flag):
        if v is not None and not isinstance(v, str):
            raise review._bad("The confirm must be the name of the flag.")
    from app.backend import present          # lazy: present imports review
    records = store.load_records(conn, case_id)
    rec = next((r for r in records if r["id"] == (row["record_ids"] or [None])[0]), None)
    if row["kind"] == "charge":
        raise _err("NOT_COUNTABLE", "This amount is already a charge. Accept it to count it.", item_id=item_id, not_counted_reason=None)
    info = present.not_counted_info(row, records)
    if not info["countable"]:
        raise _err("NOT_COUNTABLE", f"This amount cannot be counted. {info['reason']}", item_id=item_id, not_counted_reason=info["reason"])
    if confirm != CONFIRM:
        raise _err("CONFIRM_REQUIRED", REQUIRED + ("" if confirm is None else " The confirm you sent does not name it."), item_id=item_id, flag=CONFIRM, name=NAME,
                   confirm_with=CONFIRM, of=None, message=REQUIRED, not_counted_reason=info["reason"])
    promo = present.count_flag_for(row, records, info, present.CountPool(conn, case_id, records))      # likely_duplicate / likely_total (D-064 r2: an undated repeat too); the same function the view uses
    if promo and confirm_flag != promo["confirm_with"]:
        raise _err("CONFIRM_REQUIRED", f"{promo['name']}: {promo['message']} It is not counted unless you also confirm that flag by name ({promo['confirm_with']}) as confirm_flag.",
                   item_id=item_id, flag=promo["flag"], name=promo["name"], confirm_with=promo["confirm_with"], of=promo.get("of"), message=promo["message"])
    old = dict(row)
    lad = dict(row.get("ladder") or {"item_id": item_id})
    prior = lad.get("reclassification") or {}
    cc = dict(lad.get("code_checks") or {})
    cc.update(classified_by="reviewer:counted")
    state, reasons = confidence.compose_state({"grounding_failures": [], "schema_valid": True, "code_reasons": [], "judge": None},
                                              {"injection": bool(rec and rec.get("injection_tag")), "amount_class": "charge",
                                               "ocr_derived": bool(rec and rec["id"] in review.ocr_record_ids(conn, case_id)), "translated": language.translated_record(rec)})
    stamp = {"flag": CONFIRM, "name": NAME, "confirmed_at": store.iso(t)}
    lad.update(judge=None, code_checks=cc, state=state, counted={"confirm": CONFIRM, "at": store.iso(t), "by": "reviewer", "not_counted_reason": info["reason"]},
               reclassification={"from": row["kind"], "to": "charge", "at": store.iso(t), "by": "reviewer", "original_kind": prior.get("original_kind", row["kind"]),
                                 "wording": None, "restored": False, "excerpt_sha": reclassify._sha(row["excerpt"]), "note": None,
                                 "previous_judge": lad.get("judge") if not prior.get("previous_judge") else prior.get("previous_judge")})
    lad["confirm"] = promo or _flag()                                     # a later reset needs this confirm again before the charge counts
    before = {"kind": row["kind"], "review_status": row["review_status"], "state": row["state"]}
    DB.update_item(conn, item_id, now=t, case=case_id, kind="charge", state=state, state_reasons_json=reasons, ladder=lad)
    try:
        if row["review_status"] != "pending":                              # an earlier decision was about the old meaning
            review.batch_apply(conn, case_id, item_id, "reset", t)
        reclassify._log(conn, case_id, item_id, before, {"event": "count", "kind": "charge", "review_status": "accepted", "confirm": stamp,
                                                         "not_counted_reason": info["reason"], "confirm_flag": promo["flag"] if promo else None}, t)
        review.set_review(conn, case_id, item_id, "accept", now=t, kind="amount", item=DB.get_item(conn, item_id, case_id), confirm=lad["confirm"]["confirm_with"])
    except Exception:
        DB.update_item(conn, item_id, now=t, case=case_id, kind=old["kind"], state=old["state"], state_reasons_json=old["state_reasons"], ladder=old.get("ladder") or {})
        raise
    return reclassify._result(conn, case_id, item_id, {"from": row["kind"], "to": "charge", "wording": None, "judge_verdict": None, "restored": False,
                                                       "counted": True, "confirm": CONFIRM}, [])
