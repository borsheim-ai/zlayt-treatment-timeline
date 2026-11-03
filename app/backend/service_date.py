"""The service date a charge line prints (D-073). FALLBACK APPLIED after round 6: `resolve` never returns a date. Every charge line prints the fillable blank and the paralegal fills it from the quote;
the two-source reader described below is kept as `read` (SCOPE_CUTS row 28) and is not called by the letter, the case view or the notes. Code only, no LLM (LLM_VS_CODE rows 2 and 3).

A charge line takes its date of service from EXACTLY TWO sources:
  (1) its own row's date cell in a REAL bill table: a header row of short labels (two or more) that names the date of service as a whole cell (DOS, date of service, service date, visit date, 24A ...),
      with at least two data rows that hold a date in that column and the same number of cells as the header; or the CMS-1500 24A 'From' / 'To' cells of such a table, or the UB-04
      'statement covers period FROM ... THROUGH ...' of one period, none of it about another statement; printed as a range. A 'Date of service: X' line, a key-value line or a sentence that mentions DOS is not a heading;
  (2) the record's own date, ONLY when the record is positively identified as an encounter record by a WHOLE document-type phrase in its source label (`record_kind`, the table
      app/backend/encounter_types.json: progress note, discharge summary, emergency department record, MRI report, ambulance run report, operative report ...; no single word, a provider's name is
      never enough), and the charge's own sentence holds at most that one date, no count of visits, no month-year phrase and no 'earlier / next / previous' phrase.
Prose is NOT read: 'DOS 01/09/2026', 'visit of', 'Treatment dates A to B', 'next visit date' ... inside a sentence never give a date (SCOPE_CUTS row 28). Every other line prints the fillable blank
'date of service [__________] (record dated X)' and the Step 3 note; the paralegal fills it from the quote. The result of `resolve` is one of:
  - `stated`: a date or complete period from source (1), or the record's own date from source (2);
  - `not_stated` with reason `no_date` / `non_service_date`: the line has no date of source (1) or (2) (`non_service_date` names the one date the code saw but does not read);
  - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): a DOS-column cell the code cannot read with certainty;
    the note names the date as the column writes it.
Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
import datetime as _dt
import json
import pathlib
import re

from app.backend import amounts as AM

TYPES_PATH = pathlib.Path(__file__).with_name("encounter_types.json")          # D-071 amendment 2: the one declared table of record types (also read by evals/letter_check.py)
_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))


def _tokens(text: str) -> list:
    return re.findall(r"[^\W_]+", (text or "").lower())


def _phrase_rx(terms):
    return re.compile(r"(?<= )(?:" + "|".join(" ".join(re.escape(t) for t in _tokens(term)) for term in sorted(terms, key=len, reverse=True)) + r")(?= )")


_FIN, _ADMIN, _ENC = (_phrase_rx(_TYPES[k]) for k in ("financial", "administrative", "encounter"))
_OPEN = int(_TYPES["opening_chars"])


def _hit(rx, text) -> bool:
    return bool(rx.search(" " + " ".join(_tokens(text)) + " "))


def record_kind(source, excerpt: str = "") -> str:
    """'bill' | 'encounter' | 'other' (D-071 amendment 2). A bill is what amounts.billing_document says or what the declared table calls financial in the source label or the first
    characters of the excerpt, up to its first colon or full stop ('Receipt:', 'Charges:', 'Account summary:'); an administrative paper (phone note, letter, affidavit) is 'other'; an ENCOUNTER needs a positive
    identification by a DOCUMENT-TYPE word in the source label (visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, run report, operative report ...; D-073: a provider
    name such as Clinic, ED, Urgent Care, Imaging, Orthopedics is never enough). Anything else is of unknown type ('other'). Only an encounter lends its header date."""
    src, opening = source or "", re.split(r"[:.\n]", (excerpt or "")[:_OPEN])[0]
    if AM.billing_document(src, excerpt or "") or _hit(_FIN, src) or _hit(_FIN, opening):
        return "bill"
    if _hit(_ADMIN, src) or _hit(_ADMIN, opening):
        return "other"
    return "encounter" if _hit(_ENC, src) else "other"

_MON = AM._MON
_ORD = r"(?:st|nd|rd|th)?"
_DASH = "–—"
_TOK = re.compile(
    r"(?<![\w/$])(?:"
    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
    r"|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2}))"
    rf"|(?P<mper>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}\s*[-{_DASH}]\s*(?:(?:{_MON})\.?\s+)?\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
    rf"|(?P<mdy>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}(?:,?\s+\d{{4}}|,\s*\d{{2}}(?!\d))?)"
    rf"|(?P<dmy>\d{{1,2}}{_ORD}[\s-]+(?:of\s+)?(?:{_MON})\.?[\s-]*,?\s*\d{{4}})"
    r"|(?P<md>\d{1,2}/\d{1,2}(?!\s*(?:hrs?|hours?|units?|miles?|mins?|visits?|sessions?)\b))"
    r")(?![\w/]|\.\d)", re.IGNORECASE)
_JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
_LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
# ---- D-073: the only evidence that reads a date. A column heading over the date cell (below), the UB-04 'statement covers period' span, and nothing in a sentence.
_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(\u00b7]*$"          # a label, then spaces, a colon or a dotted leader (masked to middle dots, `_mask_leaders`), then the date
_WINDOW = 60                     # characters before a date that may hold the UB-04 span label and the leader after it
_mask_leaders = AM.mask_leaders          # the one helper: a dotted leader is neither a sentence end nor a column gap (T-209 r2)


_UB_SPAN = re.compile(r"\bstatement\s+(?:covers\s+)?period" + _LBL_END, re.IGNORECASE)       # UB-04 FL6 'Statement Covers Period FROM ... THROUGH ...': the span of the services of a coded line
_UB = re.compile(r"\bub-?04\b|\btype\s+of\s+bill\b|\bFL\s?\d{1,2}\b|\bUB\s?92\b", re.IGNORECASE)
# a column heading that names service (a CMS-1500 24A 'From'/'To' under 'Date(s) of Service', 'Service From', 'DOS' ...). A bare 'Date', 'Entry date', 'Transaction Date', 'Posted' ... does not.
_H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter\s+date|"
                    r"\b(?:service|svc)\s+(?:from|to|thru|through)\b|\b(?:from|to|thru|through)\s+(?:dos|service|svc)\b|\b24\s*-?a\b", re.IGNORECASE)
_H_CELL = re.compile(r"^(?:24\s*-?a\s*)?(?:dos|svc|date\(?s?\)?\s+of\s+(?:service|visit)(?:\s*\(dos\))?|(?:service|svc)\s+date|visit\s+date|encounter\s+date)(?:\s+(?:from|to|thru|through))?$"
                     r"|^(?:service|svc)\s+(?:from|to|thru|through)$|^(?:from|to|thru|through)\s+(?:dos|service|svc)$|^24\s*-?a$", re.IGNORECASE)      # a WHOLE heading cell that names the service
_ITEM_NO = re.compile(r"\b\d{1,2}[A-Za-z]\b|\bFL\s?\d{1,2}\b")          # a form item number ('24A', 'FL 6'): the only digit a heading cell may hold
# another time named in a sentence: an encounter note whose charge sentence says so lends nothing (D-073 round 6, rule 3); the same words guard a UB-04 statement period
_MONTH_YEAR = re.compile(rf"\b(?:{AM._MON})\.?,?\s+(?:of\s+)?(?:19|20)\d\d\b", re.IGNORECASE)          # 'October 2025', 'Oct. 2025' (the sentence split falls after 'Oct.', so the look-ahead below reads past it)
_OTHER_TIME = re.compile(r"\b(?:earlier|previous|previously|prior|next|last|later|ago|former|subsequent)\b|\bbalance\s+forward\b|"
                         rf"\b(?:{AM._MON})\.?,?\s+(?:of\s+)?(?:19|20)\d\d\b|(?<![\d/])\d{{1,2}}/(?:19|20)\d\d(?![\d/])", re.IGNORECASE)
_YEARS_BEFORE = 5                # a bill's service date more than this many years before its statement is doubtful

REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "implausible", "non_service_date", "no_date", "not_read")
WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)


def display(first, last=None) -> str:
    """'June 9, 2026' for one day; a period as a range: 'June 9–12, 2026', 'June 28–July 2, 2026', 'December 30, 2026–January 2, 2027' (D-071)."""
    def lng(iso):
        d = _dt.date.fromisoformat(iso)
        return f"{d.strftime('%B')} {d.day}, {d.year}"
    if not last or last == first:
        return lng(first)
    a, b = _dt.date.fromisoformat(first), _dt.date.fromisoformat(last)
    if (a.year, a.month) == (b.year, b.month):
        return f"{a.strftime('%B')} {a.day}–{b.day}, {a.year}"
    if a.year == b.year:
        return f"{a.strftime('%B')} {a.day}–{b.strftime('%B')} {b.day}, {a.year}"
    return f"{lng(first)}–{lng(last)}"


BLANK = "date of service [__________]"


def date_label(kind=None) -> str:
    """What the record's own date is called next to the blank (D-075): always 'record'. The text never classifies the source as a bill or a clinical record; one neutral label cannot be wrong. `kind` is ignored."""
    return "record"


def not_stated_text(statement_iso, kind=None) -> str:
    """The text the letter puts after the provider when no service date is certain (D-071 addendum, D-075): a fillable blank, like the Bates placeholder, never an inferred date. The
    paralegal fills it from the quote. 'date of service [__________] (record dated June 15, 2026)', the bare blank when the record has no date. `kind` is ignored."""
    if statement_iso:
        return f"{BLANK} ({date_label()} dated {display(statement_iso)})"
    return BLANK


def printed_text(res: dict, statement_iso, kind=None) -> str:
    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
    return not_stated_text(statement_iso)


_WHY = {
    "ambiguous_numeric": "The date of service column of the bill reads {raw}, which can be read as month/day or day/month; the record does not settle which.",
    "two_digit_year": "The date of service column of the bill reads {raw}, which has a two-digit year; the code does not guess the century.",
    "no_year": "The date of service column of the bill reads {raw}, which states no year; the code does not borrow one from the statement.",
    "invalid": "The date of service column of the bill reads {raw}, which is not a complete date on the calendar.",
    "several_dates": "The date of service column of the bill holds more than one date ({raw}) and nothing says which one belongs to this charge.",
    "implausible": "The date of service column of the bill reads {raw}, but that date is after the statement it appears on or years before it.",
    "non_service_date": "The line shows {raw}, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service.",
    "no_date": "The letter does not take a date of service from the records.",
    "not_read": "The letter does not take a date of service from the records.",
}
_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated itemized bill, and fill the blank before you rely on it."


def confirm_note(reason, raw) -> str:
    """The Step 3 note and the internal-notes line for a charge whose service date is not certain: why, and what the letter does (D-071 amendment)."""
    return _WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") + (_ASK_WRITTEN if reason in WRITTEN else _ASK_NONE)


def _iso(y, mo, d):
    try:
        return _dt.date(y, mo, d).isoformat() if 1900 <= y <= 2100 else None
    except ValueError:
        return None


class _Tok:
    __slots__ = ("start", "end", "raw", "kind", "fixed", "ambiguous", "order", "flaw", "first", "last")

    def __init__(self, m):
        self.start, self.end, self.raw, self.kind = m.start(), m.end(), m.group(0), m.lastgroup
        self.fixed, self.ambiguous, self.order, self.flaw, self.first, self.last = None, None, None, None, None, None
        getattr(self, "_" + self.kind)(m.group(0))
        if self.flaw is None and not (self.fixed or self.ambiguous or self.first):
            self.flaw = "invalid"

    def _iso(self, s):
        y, mo, d = (int(x) for x in s.split("-"))
        self.fixed = _iso(y, mo, d)

    def _num(self, s):
        a, b, y = re.split(r"[/.-]", s)
        if len(y) == 2:
            self.flaw = "two_digit_year"
            return
        a, b, y = int(a), int(b), int(y)
        md, dm = _iso(y, a, b), _iso(y, b, a)
        if md and dm and md != dm:
            self.ambiguous = {"MD": md, "DM": dm}
        elif md or dm:
            self.fixed = md or dm
            self.order = None if (md and dm) else ("MD" if md else "DM")

    def _mdy(self, s):
        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}})|,\s*(\d{{2}}))?$", s, re.IGNORECASE)
        if m.group(4):
            self.flaw = "two_digit_year"
            return
        if not m.group(3):
            self.flaw = "no_year"
            return
        self.fixed = _iso(int(m.group(3)), _mon(m.group(1)), int(m.group(2)))

    def _dmy(self, s):
        m = re.match(rf"(\d{{1,2}}){_ORD}[\s-]+(?:of\s+)?({_MON})\.?[\s-]*,?\s*(\d{{4}})$", s, re.IGNORECASE)
        self.fixed = _iso(int(m.group(3)), _mon(m.group(2)), int(m.group(1)))

    def _md(self, s):
        self.flaw = "no_year"

    def _mper(self, s):
        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}\s*[-{_DASH}]\s*(?:({_MON})\.?\s+)?(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}}))?$", s, re.IGNORECASE)
        if not m.group(5):
            self.flaw = "no_year"
            return
        y, m1 = int(m.group(5)), _mon(m.group(1))
        a, b = _iso(y, m1, int(m.group(2))), _iso(y, _mon(m.group(3)) if m.group(3) else m1, int(m.group(4)))
        if a and b and b > a:
            self.first, self.last = a, b
        else:
            self.flaw = "invalid"


def _mon(name):
    from app.backend import dates
    return dates.MONTHS[name.lower()[:3]]


class _Unit:
    """One candidate: a single date or a period (two tokens joined by a range word, or a month-name period)."""
    def __init__(self, toks):
        self.toks = toks
        self.start, self.end = toks[0].start, toks[-1].end

    def raw(self, text):
        return text[self.start:self.end]


def _units(text: str) -> list:
    toks = [_Tok(m) for m in _TOK.finditer(text)]
    out, k = [], 0
    while k < len(toks):
        t = toks[k]
        if k + 1 < len(toks) and t.kind != "mper" and toks[k + 1].kind != "mper" and _JOIN.match(text[t.end:toks[k + 1].start]):
            out.append(_Unit([t, toks[k + 1]]))
            k += 2
        else:
            out.append(_Unit([t]))
            k += 1
    return out


def _certain(unit: _Unit, ref):
    """('ok', first, last or None) or ('bad', reason): the one reading of a unit, or why it has none."""
    for t in unit.toks:
        if t.flaw:
            return "bad", t.flaw
    if len(unit.toks) == 1 and unit.toks[0].first:
        return "ok", unit.toks[0].first, unit.toks[0].last
    determined = {t.order for t in unit.toks if t.order}
    amb = [t for t in unit.toks if t.ambiguous]
    if len(determined) > 1:
        return "bad", "ambiguous_numeric"
    if determined:
        order = next(iter(determined))
    elif amb:
        feasible = [o for o in ("MD", "DM") if not ref or all(t.ambiguous[o] <= ref for t in amb)]          # a service is not after the statement that bills it
        if len(feasible) != 1:
            return "bad", "ambiguous_numeric"
        order = feasible[0]
    else:
        order = None
    isos = [t.ambiguous[order] if t.ambiguous else t.fixed for t in unit.toks]
    if len(isos) == 2 and isos[1] <= isos[0]:
        return "bad", "invalid"
    return "ok", isos[0], (isos[1] if len(isos) == 2 else None)


def _cells(line: str) -> list:
    """[(start column, text)] of a table line: runs of words split at a tab, a pipe or two spaces."""
    return [(m.start(), m.group(0)) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]


def _is_label(cell: str) -> bool:
    """A heading cell is a short label: at most four words and no colon (a 'Key: value' pair). The heading line itself holds no digit but a form item number such as 24A (`_grid` skips any other line)."""
    t = cell.strip()
    return bool(t) and ":" not in t and len(_ITEM_NO.sub("", t).split()) <= 4


def _pure_dates(cell: str) -> bool:
    """True when the cell holds a date, a period or a list of dates and nothing else (a 'Next visit 05/29/2026' cell is not a date cell)."""
    units = _units(cell)
    if not units:
        return False
    gaps = [cell[:units[0].start]] + [cell[a.end:b.start] for a, b in zip(units, units[1:])] + [cell[units[-1].end:]]
    return all(not g.strip() or _LIST.match(g) or _JOIN.match(g) for g in gaps)


def _grid(excerpt: str, row_ls: int):
    """The real table over the row that starts at `row_ls`: (heads [(start column, text)], service columns [index]) or None (D-073 round 6, rule 2). A table needs a HEADER ROW: the nearest line above the row
    with no digit (data rows and 'Date of service: X' lines in between are skipped), two or more cells, every one a short label, at least one naming the date of service as a whole cell
    (a bare From / To cell under a line that names the service, like a CMS-1500 '24A DATE(S) OF SERVICE', takes that line's words), the same number of cells as the row, and at least TWO data rows
    below it (up to a blank line) with the heading's cell count and a pure date cell in every service column. A key-value line, a sentence or a lone row is never a heading."""
    lines = excerpt.split("\n")
    r = excerpt.count("\n", 0, row_ls)
    k = r - 1
    while k >= 0 and r - k <= 40 and lines[k].strip() and re.search(r"\d", _ITEM_NO.sub("", lines[k])):
        k -= 1
    if k < 0 or r - k > 40 or not lines[k].strip():
        return None
    heads = _cells(lines[k])
    if len(heads) < 2 or not all(_is_label(t) for _, t in heads):
        return None
    over = lines[k - 1].strip() if k >= 1 else ""
    if over and _H_SVC.search(over) and not _H_SVC.search(lines[k]):
        heads = [(c, f"{over} {t}" if re.fullmatch(r"(?i)from|to|thru|through", t.strip()) else t) for c, t in heads]
    svc = [i for i, (_, t) in enumerate(heads) if _H_CELL.match(" ".join(t.split()))]
    if not svc:
        return None
    n = 0
    for line in lines[k + 1:k + 61]:
        if not line.strip():
            break
        cells = _cells(line)
        if len(cells) == len(heads) and all(_pure_dates(cells[i][1]) for i in svc):
            n += 1
    return (heads, svc) if n >= 2 else None


def _table_dates(excerpt, a_start):
    """([(unit, heading)], row text) of the line that holds the figure at `a_start`: the dates of the whole line (a sentence end such as ';' inside a cell does not cut it), each with the service column
    heading over its cell when the line is a row of a real table and the date is the whole text of a service cell ('' for any other date)."""
    row_ls = excerpt.rfind("\n", 0, a_start) + 1
    rl_end = excerpt.find("\n", a_start)
    row_text = excerpt[row_ls:len(excerpt) if rl_end < 0 else rl_end]
    row_cells = _cells(row_text)
    grid = _grid(excerpt, row_ls)
    out = []
    for u in _units(row_text):
        head = ""
        if grid and len(row_cells) == len(grid[0]):
            idx = next((i for i, (c, t) in enumerate(row_cells) if c <= u.start < c + len(t)), None)
            if idx in grid[1] and _pure_dates(row_cells[idx][1]):
                head = grid[0][idx][1]
        out.append((u, head))
    return out, row_text


def _plausible(first, last, ref) -> bool:
    """A service date is not after the record it appears in and not years before it."""
    if not ref:
        return True
    r = _dt.date.fromisoformat(ref)
    return (last or first) <= ref and _dt.date.fromisoformat(first) >= r - _dt.timedelta(days=366 * _YEARS_BEFORE)


def _decide(units, text, ref):
    """('ok', first, last) for one certain labeled unit (or several that read the same); ('bad', reason, [raw, ...]) otherwise."""
    reads = [(u, _certain(u, ref)) for u in units]
    raws = [" ".join(u.raw(text).split()) for u in units]
    if len(units) > 1:
        same = {(r[1], r[2]) for _, r in reads if r[0] == "ok"}
        if not (len(same) == 1 and all(r[0] == "ok" for _, r in reads)):
            return "bad", "several_dates", raws
        first, last = next(iter(same))
    else:
        r = reads[0][1]
        if r[0] != "ok":
            return "bad", r[1], raws
        first, last = r[1], r[2]
    if not _plausible(first, last, ref):          # in every record: a service date is not after the record's own date and not years before it (a prior treatment's DOS is not this charge's)
        return "bad", "implausible", raws
    return "ok", first, last


def _apply(out: dict, res) -> dict:
    if res[0] == "ok":
        out.update(state="stated", first=res[1], last=res[2], reason=None, raw="", raws=[])
    else:
        out.update(reason=res[1], raw=", ".join(res[2]), raws=list(res[2]))
    return out


_MULTI = re.compile(r"\b(?:visits|sessions|treatments|appointments|encounters)\b|\bto[ -]date\b|\bvisits?\s+\d+\s*(?:-|\u2013|\u2014|to|through|thru)\s*\d+|"
                    r"\b(?:[2-9]|\d{2,}|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*(?:x|times)\b", re.IGNORECASE)          # a charge for more than one visit


def _sentence_at(text: str, pos: int) -> str:
    """The sentence (or line) of `text` that holds position `pos`: the text between the nearest sentence ends around it."""
    lo = max([0] + [m.end() for m in re.finditer(r"(?<=[.;!?])\s+|\n", text[:pos])])
    m = re.compile(r"(?<=[.;!?])\s+|\n").search(text, pos)
    return text[lo:m.start() if m else len(text)]


def _from_to(pairs):
    """The units of a table row's service-date cells: a CMS-1500 24A 'From' cell followed by its 'To' / 'Thru' cell is one period (the same day twice is that day)."""
    out, k = [], 0
    while k < len(pairs):
        u, head = pairs[k]
        if not head:          # only a date under a service heading cell of a real table carries one (`_table_dates`)
            k += 1
            continue
        nxt = pairs[k + 1] if k + 1 < len(pairs) else None
        if nxt and re.search(r"\bfrom\b", head, re.IGNORECASE) and re.search(r"\b(?:to|thru|through)\b", nxt[1] or "", re.IGNORECASE):
            same = u.toks[-1].raw.strip() == nxt[0].toks[0].raw.strip()
            out.append(u if same else _Unit(u.toks + nxt[0].toks))
            k += 2
            continue
        out.append(u)
        k += 1
    return out


def resolve(excerpt: str, start: int, source, date_iso) -> dict:
    """D-073 FALLBACK (T-202 round 6 failed on a visit note that lent its date to another visit's charge and a UB-04 period that overrode a line's own date): the letter and Step 3 NEVER
    carry a service date. Every charge line is `not_stated` and prints the fillable blank; the paralegal fills it from the quote. The reader below (`read`) stays for the day date extraction
    returns (SCOPE_CUTS row 28); a line it would have dated gets the reason `not_read`, any other keeps the reason it found."""
    out = read(excerpt, start, source, date_iso)
    if out["state"] == "stated":
        out.update(state="not_stated", first=None, last=None, reason="not_read", raw="", raws=[])
    return out


def read(excerpt: str, start: int, source, date_iso) -> dict:
    """{state: 'stated'|'not_stated', first, last (None for one day), reason (None when stated, else one of REASONS), raw (the date text the reason is about), raws ([the dates as written])} for
    the figure at `start` of `excerpt`, in a record with header `source` and date `date_iso`. Exactly two sources give a date (module doc, D-073)."""
    out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
    excerpt = _mask_leaders(excerpt)
    amts = AM.find_amounts(excerpt or "")
    i = next((n for n, a in enumerate(amts) if a["start"] == start), None)
    if i is None:
        return out
    a = amts[i]
    ss, se = next(((s, e) for s, e in AM._segments(excerpt) if s <= a["start"] < e), (0, len(excerpt)))
    kind = record_kind(source, excerpt)
    seg = excerpt[ss:se]
    units = _units(seg)
    others = [u.raw(seg) for u in units]                                   # the dates of the line that no source reads
    pairs, row_text = _table_dates(excerpt, a["start"])
    if pairs:                                                              # source (1): the date cell of its own row, under a heading cell of a real table that names the date of service
        lab = _from_to(pairs)
        if lab:
            return _apply(out, _decide(lab, row_text, date_iso))
    if kind == "bill" and AM._CODE_RX.search(seg[:a["start"] - ss]) and (_UB.search(source or "") or _UB.search(excerpt or "")):
        prefix = excerpt[:se]                                              # source (1), UB-04 FL6: a coded line takes the span its 'statement covers period FROM ... THROUGH ...' states
        span = [u for u in _units(prefix) if _UB_SPAN.search(prefix[max(0, u.start - _WINDOW):u.start])]
        if span and any(_OTHER_TIME.search(_sentence_at(prefix, u.start)) for u in span):
            out.update(reason="non_service_date", raw=span[0].raw(prefix))      # a previous / next / prior period, or a balance forward, in the period's sentence: not this charge's span
            return out
        if span:
            return _apply(out, _decide(span, prefix, date_iso))
    if kind != "encounter":                                                # a bill, an administrative paper or a record of unknown type never lends its header date
        if others:
            out.update(reason="non_service_date", raw=others[0])
        return out
    if not date_iso:
        return out
    # source (2): the date of an identified encounter record is the visit's, unless the charge's own sentence names another time, charges more than one visit or holds several dates
    if len(units) > 1:
        out.update(reason="non_service_date", raw=units[0].raw(seg))                # several candidate dates: even the same day twice is not one certain date
        return out
    for u in units:
        r = _certain(u, date_iso)
        if not (r[0] == "ok" and r[1] == date_iso and not r[2]):
            out.update(reason="non_service_date", raw=u.raw(seg))
            return out
    if _MULTI.search(seg) or _OTHER_TIME.search(seg) or _MONTH_YEAR.search(excerpt[ss:se + 8]):
        return out
    out.update(state="stated", first=date_iso, last=None, reason=None, raw="", raws=[])
    return out
