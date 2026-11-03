"""Date parsing by an explicit format list (code only). R-IN-3, R-TL-3, LLM_VS_CODE row 2.

parse_date(raw) -> {raw, status: parsed|ambiguous|missing, iso, candidates}. Nothing is ever guessed: a numeric date whose first two
numbers are both 1-12 and differ is `ambiguous` with both readings; anything unreadable or impossible is `missing`."""
import datetime as _dt
import re

from app.backend import spanish_text

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
    iso = spanish_text.parse_written_date(s)      # T-085: '14 de mayo de 2026', '14-ago-2026' (written months are never ambiguous)
    return _out(raw, "parsed", iso) if iso else _out(raw, "missing")


def days_between(a_iso: str, b_iso: str) -> int:
    """Calendar days from a to b (real calendar, leap years included)."""
    return (_dt.date.fromisoformat(b_iso) - _dt.date.fromisoformat(a_iso)).days


def confirm(parsed: dict, chosen_iso: str) -> dict:
    """confirm_date hook (R-IN-5): the paralegal may only choose one of the code-proposed readings. Returns the confirmed date dict."""
    if parsed.get("status") != "ambiguous" or chosen_iso not in parsed.get("candidates", []):
        raise ValueError("date_invalid")
    return {**parsed, "status": "confirmed", "iso": chosen_iso}


_MONTH_RE = "|".join(sorted((k for k in MONTHS), key=len, reverse=True))
_FIND = re.compile(
    r"\b\d{4}-\d{2}-\d{2}\b"
    r"|\b\d{1,2}[/-]\d{1,2}[/-](?:\d{4}|\d{2})\b"
    rf"|\b(?:{_MONTH_RE})[a-z]*\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}\b"
    rf"|\b\d{{1,2}}(?:st|nd|rd|th)?\s+(?:of\s+)?(?:{_MONTH_RE})[a-z]*\.?,?\s+\d{{4}}\b", re.IGNORECASE)


def find_dates(text: str) -> list:
    """Dates written inside free text, in listed formats only: [{start, end, text, **parse_date}] (used by the accident-date rule)."""
    out = []
    for m in _FIND.finditer(text or ""):
        out.append({"start": m.start(), "end": m.end(), "text": m.group(0), **parse_date(m.group(0))})
    return out


def long_date(iso: str) -> str:
    """'2026-03-06' -> 'March 6, 2026' (US long format, D-002). Anything that is not an ISO date is returned unchanged."""
    try:
        d = _dt.date.fromisoformat(iso)
    except (TypeError, ValueError):
        return str(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"
