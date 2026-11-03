"""Date-convention SUGGESTION for ambiguous numeric dates (T-088, D-042; code only, LLM_VS_CODE row 2). Never applied by itself.

An ambiguous record date such as 04/05/2026 has two code-proposed readings (MM/DD and DD/MM). This module looks at the OTHER numeric
dates in the same packet whose order is certain (one number above 12: 03/14/2026 is month first, 14/03/2026 is day first) and, when they
all agree, suggests that order with the reason stated in plain words and the dates it rests on. Mixed evidence or none: no suggestion.
The suggestion is a hint the UI pre-selects; the paralegal still confirms once through confirm_date (D-041), and confirm_date still only
accepts one of the code candidates. Nothing here writes to the database or changes a pipeline result."""
import re

_NUM_DATE = re.compile(r"(?<![\d/.\-])(\d{1,2})([/.\-])(\d{1,2})\2(\d{4}|\d{2})(?![\d/.\-]\d)(?!\d)")
MAX_EVIDENCE = 2
_LABEL = {"MDY": "MM/DD", "DMY": "DD/MM"}


def _order(a: int, b: int):
    """MDY / DMY when the numbers prove the order, else None (both <= 12, or neither a valid month)."""
    if a > 12 and 1 <= b <= 12:
        return "DMY"
    if b > 12 and 1 <= a <= 12:
        return "MDY"
    return None


def _evidence(records, raw_text):
    """Unambiguous numeric dates in the packet, in record order: [{record_id, raw, order}]. Reads each record's date label and its text."""
    out, seen = [], set()
    for r in records:
        block = raw_text[r["char_start"]:r["char_end"]]
        for m in _NUM_DATE.finditer(block):
            order = _order(int(m[1]), int(m[3]))
            key = (r["id"], m[0])
            if order and key not in seen:
                seen.add(key)
                out.append({"record_id": r["id"], "raw": m[0], "order": order})
    return out


def _example(ev):
    """'(Record 3: 03/14/2026)': names the record the date sits in, so the paralegal looks in the right place."""
    return f"(Record {str(ev['record_id']).lstrip('r')}: {ev['raw']})"


def suggest(rec: dict, records: list, raw_text: str):
    """Suggestion for one ambiguous record, or None. `rec` and `records` are record rows (id, date_raw, date_status, date_candidates,
    char_start, char_end). Returns {convention, label, iso, reason, evidence[]}; `iso` is None when the year is also ambiguous."""
    if rec.get("date_status") != "ambiguous":
        return None
    m = _NUM_DATE.fullmatch(" ".join(str(rec.get("date_raw") or "").split()))
    if not m or _order(int(m[1]), int(m[3])) is not None:
        return None
    ev = _evidence(records, raw_text)
    orders = {e["order"] for e in ev}
    if len(orders) != 1:
        return None                      # no evidence, or the packet mixes both orders: say nothing rather than guess
    order = next(iter(orders))
    a, b = int(m[1]), int(m[3])
    mo, d = (a, b) if order == "MDY" else (b, a)
    cands = [c for c in rec.get("date_candidates") or [] if int(c[5:7]) == mo and int(c[8:10]) == d]
    iso = cands[0] if len(cands) == 1 else None
    shown = ev[:MAX_EVIDENCE]
    n = len(ev)
    first = "month first" if order == "MDY" else "day first"
    reason = (f"Another date in this packet uses {first} {_example(shown[0])}" if n == 1 else
              f"{n} other dates in this packet use {first} " + " and ".join(_example(e) for e in shown))
    return {"convention": order, "label": _LABEL[order], "iso": iso, "reason": reason,
            "evidence": [{"record_id": e["record_id"], "raw": e["raw"]} for e in shown], "evidence_count": n, "auto_applied": False}
