"""POSSIBLE_OVERLAP: a statement line that may already include a separately stated charge (T-110, D-019). All code; no model, no arithmetic.

The case charge total adds STATED charges only (D-019). A billing statement line such as "consultas $1,300.00" can summarize a consult that another
record states on its own ("Consulta: $650.00"); counting both would add the consult twice. Code must not guess that they overlap (it cannot know the
statement's contents, and it must not subtract or merge anything), so it only WARNS: when a statement line and a separately stated charge name the
same kind of service (a small closed family table, English and Spanish) and the charge's date falls inside the statement's date range, the pair is
listed next to the total so the paralegal decides. The warning never changes the total and never compares the two figures.

Date range: two dates written in the statement text ("from X to Y", "X - Y", "del X al Y") are the stated range; otherwise the statement covers
everything up to its own record date (a statement summarizes what was billed before it was issued). A charge whose own date is not confirmed is
listed too (date_known false): the code cannot rule the overlap out.
"""
import re
import unicodedata

from app.backend import amounts as AM, dates

CODE = "POSSIBLE_OVERLAP"
_TAIL = (" The total adds each stated charge and does not merge them. Check whether the statement line already includes the separate charge; "
         "dismiss one of the two if it does.")
MESSAGES = {   # fixed sentences (never model text); the key is chosen by code
    "range": "Possible overlap: this statement line is for the same kind of service as a charge stated separately in another record, and that charge's date is inside the statement's stated date range." + _TAIL,
    "upto": "Possible overlap: this statement line is for the same kind of service as a charge stated separately in another record, dated on or before the statement." + _TAIL,
    "date": "Possible overlap: this statement line is for the same kind of service as a charge stated separately in another record whose date is not confirmed, so the date range cannot rule it out." + _TAIL,
}
MESSAGE = MESSAGES["upto"]

# Closed service-family table (English + Spanish, accents stripped, lower case). A family is the only thing two figures need to share.
_FAMILIES = (
    ("consult", r"\bconsult\w*|\boffice\s+visit\b|\bvisita\s+de\s+consultorio\b"),
    ("physical_therapy", r"\bphysical\s+therap\w*|\bphysiotherap\w*|\bterapia\s+fisica\b|\bfisioterapia\b|\bchiropract\w*|\bquiropract\w*|\bPT\b"),
    ("imaging", r"\bmri\b|\bresonancia\b|\bx-?\s?rays?\b|\bradiograf\w*|\brayos?\s+x\b|\bct\s+scan\b|\btomograf\w*|\bultrasound\b|\bultrasonido\b|\bimaging\b"),
    ("emergency", r"\bemergency\b|\bemergencia\b|\burgencias\b|\bED\b|\ber\b"),
    ("ambulance", r"\bambulance\b|\bambulancia\b|\bems\b"),
    ("injection", r"\binjection\w*|\binyeccion\w*|\bepidural\b"),
    ("surgery", r"\bsurg\w*|\bcirug\w*|\barthroscop\w*"),
    ("laboratory", r"\blab\b|\blabs\b|\blaborator\w*"),
)
_FAMILY_RX = tuple((name, re.compile(rx, re.IGNORECASE)) for name, rx in _FAMILIES)
# A statement summary line is not a service line: balances, totals, payments and adjustments never name a service to overlap.
_SUMMARY = re.compile(r"\b(?:balance|total|saldo|paid|payments?|pago|pagado|adjustments?|ajuste|due|adeudado|amount\s+due)\b", re.IGNORECASE)
_STATEMENT_SRC = re.compile(r"\bestado\s+de\s+cuenta\b|\bfactura\b|\bcuenta\s+de\s+gastos\b", re.IGNORECASE)
_RATE_ES = re.compile(r"\b(?:por|cada)\s+(?:sesion|visita|hora|dia|unidad|cita|tratamiento|procedimiento)\b|\bcosto\s+por\b|\btarifa\b|/\s*(?:sesion|visita)\b", re.IGNORECASE)
_RANGE_JOIN = re.compile(r"^\s*(?:to|through|thru|until|-|–|—|a|al|hasta)\s*$", re.IGNORECASE)


def _plain(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")


def families(label: str) -> set:
    """The service families named in an amount's own clause."""
    t = _plain(label)
    return {name for name, rx in _FAMILY_RX if rx.search(t)}


def is_statement_source(source: str) -> bool:
    return bool(AM._is_billing_source(source or "") or _STATEMENT_SRC.search(_plain(source)))


def stated_range(text: str):
    """(from_iso, to_iso) when the statement text states a range of two parsed dates joined by to/through/-/al/hasta; else None."""
    found = [d for d in dates.find_dates(text or "") if d.get("status") == "parsed" and d.get("iso")]
    for a, b in zip(found, found[1:]):
        if _RANGE_JOIN.match((text or "")[a["end"]:b["start"]]):
            lo, hi = sorted((a["iso"], b["iso"]))
            return lo, hi
    return None


def _clause_after(text: str, end: int) -> str:
    """The words right after a figure in its own clause (up to the next sentence or clause break), so a rate cue in the next sentence is not read as this figure's."""
    return re.split(r"[.;\n]", (text or "")[end:end + 40])[0]


def candidate(a: dict) -> bool:
    """A figure that can be a stated charge: a clean dollar value, not a rate/estimate/damages figure and not dismissed."""
    return (a.get("value_cents") is not None and a.get("kind") in ("charge", "unclear") and a.get("review_status") != "dismissed" and a.get("state") != "rejected"
            and not _is_rate_like(a))


def _is_rate_like(a: dict) -> bool:
    ctx = f"{a.get('label', '')} {a.get('after', '')}"
    return bool(AM.has_rate_cue(ctx) or _RATE_ES.search(_plain(ctx)))


def possible_overlaps(amounts: list) -> list:
    """`amounts`: [{id, record_id, kind, value_cents, text, review_status, state, label (the amount's own clause), after (30 chars after it),
    statement (bool: its record is a billing statement), record_date (ISO or None), record_excerpt}].
    Returns [{code, statement_amount_id, covered_amount_id, service, range, date_known, both_charges, both_in_total, message}] in a stable order.
    Two figures of one record never pair; a rate is never a party; the statement line is the summarizing side."""
    out = []
    lines = [a for a in amounts if a.get("statement") and candidate(a) and not _SUMMARY.search(_plain(a.get("label", "")))]
    others = [a for a in amounts if not a.get("statement") and candidate(a)]
    for s in lines:
        fam = families(s.get("label", ""))
        if not fam:
            continue
        rng = stated_range(s.get("record_excerpt", ""))
        end = rng[1] if rng else s.get("record_date")
        for c in others:
            if c["record_id"] == s["record_id"]:
                continue
            shared = fam & families(c.get("label", ""))
            if not shared:
                continue
            d = c.get("record_date")
            if d is None:                      # a date not confirmed cannot rule the overlap out; say so
                known = False
            else:
                known = True
                if (rng and not (rng[0] <= d <= rng[1])) or (not rng and end and d > end):
                    continue
            out.append({"code": CODE, "statement_amount_id": s["id"], "covered_amount_id": c["id"], "service": sorted(shared)[0],
                        "statement_record_id": s["record_id"], "covered_record_id": c["record_id"],
                        "statement_text": s.get("text"), "covered_text": c.get("text"),
                        "range": {"from": rng[0] if rng else None, "to": end, "stated": bool(rng)}, "date_known": known,
                        "both_charges": s["kind"] == "charge" and c["kind"] == "charge",
                        "both_in_total": s["kind"] == "charge" and c["kind"] == "charge"
                                         and s["review_status"] in ("accepted", "edited") and c["review_status"] in ("accepted", "edited"),
                        "message": MESSAGES["date"] if not known else MESSAGES["range"] if rng else MESSAGES["upto"]})
    return sorted(out, key=lambda o: (o["statement_amount_id"], o["covered_amount_id"]))


def view(conn, case_id: str) -> list:
    """The warnings for one stored case (reads amounts, records and the pasted text; no writes)."""
    from app.db import db as DB
    case = DB.get_case(conn, case_id)
    raw = case["raw_text"]
    recs = {r["id"]: DB._decode(r) for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,))}
    rows = []
    for a in DB.list_items(conn, case_id, "amount"):
        rec = recs.get((a["record_ids"] or [None])[0])
        if rec is None or a["excerpt_start"] is None:
            continue
        body = raw[rec["char_start"]:rec["char_end"]]
        rows.append({"id": a["id"], "record_id": rec["id"], "kind": a["kind"], "value_cents": a["value_cents"], "text": a["text"],
                     "review_status": a["review_status"], "state": a["state"],
                     "label": AM._label(raw, a["excerpt_start"]).replace("Excerpt:", "").strip(' "'), "after": _clause_after(raw, a["excerpt_end"]),
                     "statement": is_statement_source(rec.get("source_label")), "record_date": rec.get("date_iso") if rec.get("date_status") in ("parsed", "confirmed") else None,
                     "record_excerpt": body})
    return possible_overlaps(rows)
