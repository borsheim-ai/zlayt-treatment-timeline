"""Billing as a cited line listing (T-083, D-042, D-052). CODE ONLY: no model is asked anything here.

What it does: every ledger line parses to billed / adjustment / paid / balance figures, each cited to its line (a verbatim excerpt of the
record) and classed charge, adjustment, payment, rate or unclear. NOTHING IS TOTALED OR COMPARED here: no sum of any kind, no
'complete' flag, no balance step check, no ledger-versus-EOB check (D-052; five review rounds kept finding ways a total could silently omit a
figure, and a listing cannot hide a missing line). The one total in the product is the case-level charge total of stated charges (D-019, totals.py), unchanged.
A rate (per visit, per unit, fee schedule, UB-04 line 44) is listed as class rate; an estimate, an LOP or lien amount, a printed total
(UB-04 line 0001, CMS-1500 Item 28, TOTAL CHARGES, BALANCE DUE) and a balance forward are listed as class unclear with a `detail`; an EOB service
row is a line of class unclear, detail `eob`, with its payer figures in `eob` (they restate the bill and are never added to it). A figure that cannot be read cleanly (OCR letters, odd decimals, a column that cannot be told
apart) is listed with cents None. A row that fits no layout is listed in `unreconciled`; a record the code could not parse is in
`skipped_records`. Billing returns only these three lists. The analysis is computed on read, never stored, and never reaches the letter. Money is whole cents (int).

POSITION, NOT TEXT (D-052, T-103 r4). No code here asks whether one figure equals, exceeds or differs from another, and none sums. A printed token is
identified by WHERE it sits in its record (`_at`, an offset range), never by its text: two equal figures in one excerpt are two tokens, and a token is
"already shown" only when an output field holds that same position. The sign of a charge is a flag read from its printed credit notation
(parentheses, trailing or leading minus), not a test on its value. The only remaining tests on numbers are layout (which header a column sits under,
whether two offset ranges overlap or one contains the other) and the grounding verifier's substring check of a figure's text against its excerpt.

MONEY TOKEN (D-049; the one definition the completeness pass uses). A money token is, in a billing record: (a) a number with a decimal point
(two decimals, or an odd decimal like 95.5, OCR letters tolerated), with or without '$'; (b) a '$' figure with no cents; or (c) a bare whole
number (no '$', no decimal) ONLY when it sits in an amount column (under a ledger CHARGES/PAYMENTS/ADJ/BALANCE header, a UB-04 money column, a
CMS-1500 charge box, an EOB money column, a balance-forward row, or as the figure of a labelled charge/total/balance sentence in prose). A bare whole number anywhere
else (a stray line outside every money column, a code, a count, a year) is NOT a money token and is not accounted for. Three more cases are not tokens: on a UB-04
revenue-code row, a whole number with a decimal or '$' figure to its right (the row's charges are its last figure, so it is the units count; the header's UNITS and
SERV DATE columns are read as well as the money ones); a procedure code that follows a money-shaped token in an EOB row's service slot; and a prose number that
directly follows another money figure with no word between. A lone number in a CMS-1500 box followed by another figure (a broken box) is not read as the box.
Every money token must be a listed line, an unreconciled line, or sit on its row as an 'unclear' figure: the final accounting pass lists whatever no parser placed.
On a rate, estimate or LOP/lien row, every OTHER money token printed on the row (a running balance, a second amount in the sentence, a printed total on that
row) is one of that entry's `other_figures`, wherever a parser first put it.
Repeated summary rows (a second TOTAL CHARGES, BALANCE DUE or balance forward, in one record or in several) are listed in full, never overwritten.
"""
import re

from app.backend import amounts as A, dates

# ------------------------------------------------------------------ fixed texts (closed list; the contract appendix mirrors it)
CHECKS = {
    "LINE_UNCLEAR": "A figure on this line could not be read cleanly. It is listed with its text and no value.",
    "NO_DATE_OF_SERVICE": "Charges on this statement carry no date of service; they are counted as stated but cannot be tied to a visit.",
    "ROW_NOT_PARSED": "This row carries a figure or a date but did not fit the form's layout, so it was not read into any column. It is listed here, not totaled; check the original.",
}
RULES = [
    "Every figure is listed with the line it was read from; nothing is totaled or compared here, and a missing figure is never hidden by a sum.",
    "A rate (per visit, per unit, fee schedule, UB-04 line 44) is listed as a rate, never a charge; a row or sentence that says per visit/session/hour/day, each or x N is a rate even beside the word charge.",
    "A running balance, a printed total and an EOB row's amounts are listed beside the lines and never added to them or checked against them.",
    "LOP, lien and attorney-reduction amounts are listed apart from the charges.",
    "A figure that cannot be read cleanly is listed with no value.",
    "A row that does not fit the layout is listed as unreconciled with its text; it is never dropped.",
    "This view is for review only. The letter's total line is still accepted charges only.",
]

# ------------------------------------------------------------------ money tokens
_D = r"[0-9OolISB]"           # letters OCR confuses with digits are tolerated so a noisy figure is LISTED (cents None), never silently skipped
_FIG = rf"\(?-?\$?(?:{_D}{{1,3}}(?:,{_D}{{3}})+|{_D}+)\.{_D}+\)?-?"
_NUM = re.compile(rf"(?<![\w/.])(?=[^\s]*[0-9]){_FIG}(?![\w/]|\.\d)")
_MONEY = re.compile(rf"(?<![\w/.])(?=[^\s]*[0-9])(?:{_FIG}|\(?-?\$\s?{_D}[0-9OolISB,]*\)?-?)(?![\w/]|\.\d)")      # a decimal figure, or a '$' figure with no cents
_BARE = re.compile(r"(?<![\w/.,$])\(?-?\d[\d,]*\)?-?(?![\w/]|[.,]\d)")                                            # a whole number: only read when it sits under a money column
_FIGX = rf"(?=[^\s]*[0-9])\(?-?\$?{_D}[0-9OolISB,]*(?:\.{_D}+)?\)?-?"                                                # a stated figure: cents optional (no cents -> listed, cents None)
_DATE = r"(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})"
_ROW = re.compile(rf"^\s*({_DATE})\s+(?:({_DATE})\s+)?(.*)$")
_VOID = re.compile(r"\b(?:void(?:ed)?|reverse[ds]?|reversal|rev\.?\s+chg)\b", re.IGNORECASE)
_NEGOTIATED = re.compile(r"\b(?:atty|attorney|lawyer)\s+(?:reduction|adj\w*|discount)|\breduced\s+to\b|\bsettlement\s+(?:reduction|discount)\b|\bin\s+full\s+satisfaction\b", re.IGNORECASE)
_BALFWD = re.compile(r"\bbal(?:ance)?\.?\s*(?:fwd|forward|brought\s+forward)\b|\bprevious\s+balance\b|\bprior\s+balance\b", re.IGNORECASE)
_COLS = {"billed": re.compile(r"\b(?:CHARGES?|BILLED)\b", re.IGNORECASE), "paid": re.compile(r"\b(?:PAYMENTS?|PMTS?|PAID)\b", re.IGNORECASE),
         "adjustment": re.compile(r"\b(?:ADJ(?:USTMENTS?|S)?)\b", re.IGNORECASE), "balance": re.compile(r"\b(?:BALANCE|BAL)\b", re.IGNORECASE),
         "rate": re.compile(r"\bRATE\b", re.IGNORECASE)}                    # a RATE column is a price list: its figures are listed as rates, never totaled
_DATECOLS = {"dos": re.compile(r"\b(?:DOS|SERVICE\s+DATE)\b", re.IGNORECASE), "posted": re.compile(r"\b(?:POSTED|POST\s+DATE)\b", re.IGNORECASE)}
TOL = 8        # characters a figure may sit away from its column header (left or right aligned) before the column is called unclear


def fmt(cents, credit=False):
    """'$1,234.50' from whole cents (the magnitude). A credit (parentheses, trailing or leading minus in the printed text) is a flag the parser read from
    the text, never a sign test on the value."""
    if cents is None:
        return None
    return ("-" if credit else "") + f"${abs(cents) // 100:,}.{abs(cents) % 100:02d}"


def _is_credit(token: str) -> bool:
    """Credit notation as printed: '(70.00)', '45.00-', '-45.00'. A syntax read of the text; no value is looked at."""
    return token.startswith(("(", "-")) or token.endswith(("-", ")"))


def parse_figure(token: str) -> dict:
    """'(70.00)' -> {cents: -7000}, '45.00-' -> -4500, '1,234.50' -> 123450. Credit notation (parentheses, trailing or leading minus) makes it
    negative. Exactly two decimals are required: '95.5' or '9.999' keep their text and cents None, never rounded."""
    neg = _is_credit(token)
    digits = re.sub(r"[()\-$]", "", token)
    cents = A.to_cents(digits) if re.fullmatch(r"[\d,]+\.\d\d", digits) else None
    return {"text": token, "cents": None if cents is None else (-cents if neg else cents), "usd": fmt(cents, neg)}


def _pf(m, base=0):
    """parse_figure of a regex match, with the match's position in the record's text (offsets `base` + span). The position is how a printed token
    is told apart from another with the same text; it is private and removed before the analysis is returned."""
    return {**parse_figure(m.group(0)), "_at": (base + m.start(), base + m.end())}


def _mag(f):
    """Payment/adjustment figures are reductions: credit notation and plain positives mean the same, so the magnitude is kept."""
    return {**f, "cents": None if f["cents"] is None else abs(f["cents"]), "usd": None if f["cents"] is None else fmt(abs(f["cents"]))}


def _norm(s):
    return " ".join(re.sub(r"[^a-z0-9]+", " ", (s or "").casefold().replace("(synthetic)", "")).split())


# ------------------------------------------------------------------ placement is by position
# A printed money token is identified by where it sits in its record's text, never by its text: `_at` is a (start, end) offset pair, `_row` the offsets of
# the row (excerpt) it was read from, `_unit` the offset where its line or sentence starts. Nothing in this module asks whether two figures are equal,
# larger or smaller; only whether two offset ranges overlap or one contains the other (is this token already shown? is it on that rate row?).
def _lap(a, b):
    return a[0] < b[1] and b[0] < a[1]


def _within(a, row):
    return row[0] <= a[0] and a[1] <= row[1]


def _offsets(lines):
    out, pos = [], 0
    for ln in lines:
        out.append(pos)
        pos += len(ln) + 1
    return out


def _row_span(base, text):
    """Offsets of the stripped text of a line that starts at `base`."""
    lead = len(text) - len(text.lstrip())
    return (base + lead, base + lead + len(text.strip()))


def _provider(rec: dict) -> str:
    src = (rec.get("source") or "").strip()
    name = re.split(r",|\s[-–—]\s", src, maxsplit=1)[0].strip()
    name = re.sub(r"\s+(?:itemized\s+)?(?:ledger|statement|billing|bill|claim|eob)\s*$", "", name, flags=re.IGNORECASE).strip()
    return name or "Unknown provider"


def _dos(raw):
    p = dates.parse_date(raw or "")
    return p["iso"] if p.get("status") == "parsed" else None


def _cite(rec, line):
    return {"record_no": rec["n"], "excerpt": line.strip()}


# ------------------------------------------------------------------ record forms
def form_of(rec: dict) -> str:
    """ledger_table | ledger_text | cms1500 | ub04 | eob | None, decided from the record's own words."""
    body = (rec.get("excerpt") or rec.get("text") or "")
    src = rec.get("source") or ""
    up = body.upper()
    if "EXPLANATION OF BENEFITS" in up or "THIS IS NOT A BILL" in up or re.search(r"\bEOB\b", src, re.IGNORECASE) or ("PLAN PAID" in up and "BILLED" in up):
        return "eob"
    if "UB-04" in up or "UB04" in up or "CMS-1450" in up or "47 TOTAL CHARGES" in up or re.search(r"\bUB-?04\b", src, re.IGNORECASE):
        return "ub04"
    if "TOTAL CHARGE" in up and "AMOUNT PAID" in up or "1500" in src or "HEALTH INSURANCE CLAIM FORM" in up:
        return "cms1500"
    if _header(body.split("\n"))[0] is not None:
        return "ledger_table"
    if "$" in body and (A._is_billing_source(src) or re.search(r"\bitemized\s+(?:ledger|statement)\b|\bledger\b", body, re.IGNORECASE)):
        return "ledger_text"
    return None


def _header(lines):
    """(index, {kind: (start, end)}) of the ledger column header, or (None, None). Needs billed and balance and one more column."""
    for i, ln in enumerate(lines):
        if _ROW.match(ln) or re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or "$" in ln or not re.search(r"\S\s{2,}\S", ln):
            continue          # a header is a spaced-out row of column names: a sentence with a '$' figure is prose
        cols = {}
        for kind, rx in _COLS.items():
            m = rx.search(ln)
            if m:
                cols[kind] = (m.start(), m.end())
        if "billed" in cols and "balance" in cols and len([k for k in cols if k != "rate"]) >= 3:
            return i, cols
    return None, None


def _column(token_span, cols):
    """The column whose header the figure sits under (left- or right-aligned), or None when two are equally near or none within TOL."""
    s, e = token_span
    d = sorted((min(abs(s - hs), abs(e - he)), kind) for kind, (hs, he) in cols.items())
    if d[0][0] > TOL or (len(d) > 1 and d[1][0] == d[0][0]):
        return None
    return d[0][1]


def _money_col(token_span, cols):
    """True when the figure sits under a money column (its nearest header is a money header, and not equally near another)."""
    k = _column(token_span, cols)
    return k is not None and k not in _NONMONEY


# ------------------------------------------------------------------ itemized ledger table
def _rate_entry(rec, fig, excerpt, why="A rate (per visit, per unit) is a price, not a charge.", kind="rate", row=None):
    """A rate, estimate or LOP-like entry. `fig` carries its position (`_at`); `row` is the offsets of the printed row (the excerpt) it was read from."""
    return {"record_no": rec["n"], "kind": kind, "why": why, "figure": fig, "excerpt": excerpt, "_at": fig["_at"], "_row": row or fig["_at"], "other_figures": []}


def _blank_dates(ln):
    return re.sub(_DATE, lambda m: " " * len(m.group(0)), ln)


_NONMONEY = ("units", "servdate")          # UB-04 header columns that are not money: a whole number nearest to one of these is a count or a date


def _tokens(ln, cols=None, all_bare=False):
    """Money-shaped tokens of a ledger line, in text order: decimals, '$' figures without cents and, only when `cols` is given, whole numbers that
    sit under a money column header (`all_bare`: every whole number on the line, for a balance-forward row). Dates are never tokens. Nothing here
    decides what a token means; every caller must place it or list it."""
    found = list(_MONEY.finditer(ln))
    if cols or all_bare:
        plain = _blank_dates(ln)
        found += [m for m in _BARE.finditer(plain) if (all_bare or _money_col(m.span(), cols)) and not any(m.start() < f.end() and f.start() < m.end() for f in found)]
    return sorted(found, key=lambda m: m.start())


def _put_stated(rec, stated, new, out):
    """Record the totals a statement prints. A second figure for the same total (equal or different) is never guessed between or silently
    absorbed: the earlier one is listed as an unparsed line (the paralegal sees it; no completeness is claimed), the later one is kept (D-049)."""
    for k, v in new.items():
        old = stated.get(k)
        if old:
            out.append({**_blank_line(rec, "ledger", old["cite"]["excerpt"], unparsed=True, unit=old["_unit"], unclear=[(old["text"], old["_at"])]), "superseded": True})      # not the kept total: it must not stand in for it
        stated[k] = v


def _stated_orphans(rec, lform, got, stated):
    """A printed total that could not be read (cents None), or that belongs to a statement with no readable line at all, is listed as an unparsed
    line with the total's own excerpt, so the figure is not left only in a field nobody opens. Totals on one printed line share one entry."""
    by_unit = {}
    for v in stated.values():
        if v["cents"] is None or not got:
            by_unit.setdefault(v["_unit"], (v["cite"]["excerpt"], []))[1].append((v["text"], v["_at"]))
    return [_blank_line(rec, lform, ex, unparsed=True, unit=u, unclear=pairs) for u, (ex, pairs) in by_unit.items()]


def _family(form):
    """Ledger tables and ledger prose are one family (a statement); each claim form is its own."""
    return "ledger" if (form or "ledger").startswith("ledger") else form


def _near(span, hdr):
    return min(abs(span[0] - hdr[0]), abs(span[1] - hdr[1]))


def _ledger_table(rec, lines):
    """(lines, stated totals, balance-forward rows [list], rate entries). A row whose description carries a rate cue and whose CHARGES figure was found (read
    or not) is a price, not a charge: it goes to the rate entries and into no total. Every other line that carries a figure and is not a clean
    dated row (above the header, below it, a total it cannot place) is emitted as an unparsed line (unclear, not totaled), never dropped."""
    hi, cols = _header(lines)
    offs = _offsets(lines)
    dcols = {k: (m.start(), m.end()) for k, rx in _DATECOLS.items() for m in [rx.search(lines[hi])] if m}
    out, stated, balfwd, rates = [], {}, [], []

    def unparsed(i, toks):
        out.append(_blank_line(rec, "ledger", lines[i], unparsed=True, unit=offs[i], unclear=[(t.group(0), (offs[i] + t.start(), offs[i] + t.end())) for t in toks]))

    for i in range(hi):                                # a figure above the column header is listed too
        if _tokens(lines[i]):
            unparsed(i, _tokens(lines[i]))
    for i in range(hi + 1, len(lines)):
        ln = lines[i]
        if re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or re.search(r"\bBALANCE\s+DUE\b", ln, re.IGNORECASE):
            new = _stated(rec, ln, offs[i])
            _put_stated(rec, stated, new, out)
            left = []
            for t in _tokens(ln):
                f, kind, at = parse_figure(t.group(0)), _column(t.span(), cols), (offs[i] + t.start(), offs[i] + t.end())
                if any(_lap(at, v["_at"]) for v in new.values()):
                    continue                                 # this token IS one of the totals just read from the line
                if kind in ("billed", "paid", "adjustment", "balance") and f["cents"] is not None and kind not in stated:
                    stated[kind] = {**(_mag(f) if kind in ("paid", "adjustment") else f), "cite": _cite(rec, ln), "_at": at, "_unit": offs[i]}      # a totals row printed under the columns
                else:
                    left.append(t)
            if left:
                unparsed(i, left)
            continue
        if _BALFWD.search(ln):
            toks = _tokens(ln, all_bare=True)
            if toks:
                bf = {**_pf(toks[-1], offs[i]), "cite": _cite(rec, ln), "_unit": offs[i]}
                if bf["cents"] is None or len(toks) > 1:
                    unparsed(i, toks if bf["cents"] is None else toks[:-1])
                if bf["cents"] is not None:
                    balfwd.append(bf)          # every forward row is kept; analyze() lists them all when a provider has more than one
            continue
        m = _ROW.match(ln)
        figs = _tokens(ln, cols)
        if not m:
            if figs:                                  # a figure on a line that is not a dated row: listed, not totaled (it moves to a rate or LOP entry's other figures when it sits on that row)
                unparsed(i, figs)
            continue
        head = ln[:figs[0].start()] if figs else ln
        row_m = _ROW.match(head + " ")
        parts = (row_m.group(3) if row_m else "").split(None, 1)
        code = parts[0] if parts and re.fullmatch(r"[A-Za-z0-9]{2,7}", parts[0]) and (len(parts) > 1 or not figs) else None
        desc = (parts[1] if code and len(parts) > 1 else " ".join(parts)).strip() if parts else ""
        dos, posted = m.group(1), m.group(2)
        if posted is None and len(dcols) == 2 and _near((m.start(1), m.end(1)), dcols["posted"]) < _near((m.start(1), m.end(1)), dcols["dos"]):
            dos, posted = None, m.group(1)            # the only date sits under POSTED: the DOS cell is blank, the posting date is not a service date
        line = _blank_line(rec, "ledger", ln, dos=dos, posted=posted, code=code, description=desc, unit=offs[i])
        ratey, row_rate = A.has_rate_cue(desc, unit_notation=True), False
        for fm in figs:
            kind = _column(fm.span(), cols)
            f = _pf(fm, offs[i])
            if kind == "billed" and ratey:           # a price, whether or not its cents could be read: listed once, never a line
                rates.append(_rate_entry(rec, f, ln.strip(), "This row says it is a per-visit/unit/rate figure: a rate is a price, not a charge. It is not totaled.", row=_row_span(offs[i], ln)))
                row_rate = True
            elif kind is None or f["cents"] is None:
                _add_unclear(line, f["text"], f["_at"])
            elif kind == "rate":
                rates.append(_rate_entry(rec, f, ln.strip(), "This figure sits in the RATE column: a rate is a price, not a charge.", row=_row_span(offs[i], ln)))
            elif line[kind] is not None:
                _add_unclear(line, f["text"], f["_at"])            # two figures in one column: not guessed
            else:
                line[kind] = _mag(f) if kind in ("paid", "adjustment") else f
                if kind == "billed":
                    line["_credit"] = _is_credit(f["text"])
        if row_rate:
            line["balance"] = None                    # the running balance of a price row is one of the rate entry's other figures
            if not (line["paid"] or line["adjustment"] or line["unclear"]):
                continue
        out.append(line)
    tail = hi + 1 if hi + 1 < len(lines) else None
    if tail is not None:
        _put_stated(rec, stated, {k: v for k, v in _stated(rec, "\n".join(lines[tail:]), offs[tail]).items() if k not in stated}, out)
    return out, stated, balfwd, rates


def _blank_line(rec, form, ln, dos=None, posted=None, code=None, description="", unparsed=False, unclear=None, unit=None):
    """A line with no figures yet. `unclear` is [(text, (start, end))]: the tokens listed on the row with their positions."""
    pairs = list(unclear or [])
    return {"record_no": rec["n"], "form": form, "dos": dos, "dos_iso": _dos(dos) if dos else None, "posted": posted, "code": code,
            "description": description, "billed": None, "adjustment": None, "paid": None, "balance": None, "unclear": [t for t, _ in pairs],
            "excerpt": ln.strip(), "unparsed": unparsed, "_uat": [p for _, p in pairs], "_unit": unit}


def _add_unclear(line, text, at):
    line["unclear"].append(text)
    line.setdefault("_uat", []).append(at)


_STATED = {"billed": re.compile(rf"TOTAL\s+CHARGES?\s*[:=]?\s*({_FIGX})", re.IGNORECASE),
           "paid": re.compile(rf"TOTAL\s+(?:PMTS?|PAYMENTS?)\s*[:=]?\s*({_FIGX})", re.IGNORECASE),
           "adjustment": re.compile(rf"TOTAL\s+ADJ\w*\s*[:=]?\s*({_FIGX})", re.IGNORECASE),
           "balance": re.compile(rf"(?:BALANCE\s+DUE|AMOUNT\s+DUE|TOTAL\s+BALANCE)\s*[:=]?\s*({_FIGX})", re.IGNORECASE)}


def _stated(rec, text, base=0):
    """Totals the statement prints itself. Returned with the line they were read from (and where they sit, from `base`, the offset of `text`); listed
    as printed, compared with nothing."""
    out = {}
    for kind, rx in _STATED.items():
        m = rx.search(text)
        if m:
            f = parse_figure(m.group(1))
            f = _mag(f) if kind in ("paid", "adjustment") else f
            a, b = text.rfind("\n", 0, m.start(1)) + 1, text.find("\n", m.end(1))
            ln = text[a:(b if b >= 0 else len(text))]
            out[kind] = {**f, "cite": _cite(rec, ln), "_at": (base + m.start(1), base + m.end(1)), "_unit": base + a}
    return out


# ------------------------------------------------------------------ ledger written as a sentence ("New patient exam charge $250.00; ...")
_PROSE = (("billed_total", re.compile(r"\btotal\s+(?:billed\s+)?charges?\b|\btotal\s+billed\b", re.IGNORECASE)),
          ("paid", re.compile(r"\bpayments?\b|\bpaid\b|\bpmts?\b", re.IGNORECASE)),
          ("adjustment", re.compile(r"\badjust\w*|\bdiscount\b|\bwrite-?off\b|\bcontractual\b|\bcourtesy\b|\bW/O\b", re.IGNORECASE)),
          ("balance", re.compile(r"\bbalance\b|\bamount\s+due\b", re.IGNORECASE)))


def _segments(text):
    """[(start, end)] of clauses: split at ; ! ? newline and a period that ends a sentence (not the decimal point of a figure)."""
    out, pos = [], 0
    for m in re.finditer(r"(?<=[;!?])\s+|\n|(?<=[a-zA-Z)\d])\.(?=\s+[A-Z])\s*", text):
        out.append((pos, m.start() + (1 if text[m.start()] == "." else 0)))
        pos = m.end()
    out.append((pos, len(text)))
    return [(s, e) for s, e in out if text[s:e].strip()]


def _ledger_text(rec, body):
    """(lines, stated totals, rate entries, balance-forward figures). A figure the classifier calls a rate, or a charge-worded figure whose sentence also carries a rate cue
    (per visit/session/hour/day, each, x N, daily rate), is a price: listed as a rate, never a line. An estimate is listed as excluded. Every other
    figure is either a charge (a line), a paid/adjustment/balance/total by its label, or an unparsed line with its text: an unlabelled figure is
    never totaled and never dropped."""
    lines, stated, rates, fwds = [], {}, [], []
    for s, e in _segments(body):
        seg = body[s:e]
        bad, spans = [], []
        for a in A.find_amounts(seg):
            spans.append((a["start"], a["end"]))
            at = (s + a["start"], s + a["end"])
            if a["cents"] is None:
                bad.append((a["raw"], at))                   # unreadable (OCR letters, odd decimals, injected text): listed with its text
                continue
            label = A._label(seg, a["start"])
            credit = seg[max(0, a["start"] - 1):a["start"]] == "-" or label.endswith("-")      # credit notation as printed: a flag read from the text
            raw = ("-" if credit else "") + a["raw"]
            fig = {"text": raw, "cents": -a["cents"] if credit else a["cents"], "usd": fmt(a["cents"], credit), "_at": at}
            kind = next((k for k, rx in _PROSE if rx.search(label)), None)
            cite = {**_cite(rec, seg), }
            cls = A.classify(seg, a, source=rec.get("source"), strict=False)
            row = _row_span(s, seg)
            if cls == "rate" or (kind is None and cls == "charge" and A.has_rate_cue(seg)):
                rates.append(_rate_entry(rec, fig, seg.strip(), row=row))
            elif kind == "billed_total":
                _put_stated(rec, stated, {"billed": {**fig, "cite": cite, "_unit": s}}, lines)
            elif kind in ("paid", "adjustment"):
                lines.append(_pline(rec, seg, kind, _mag(fig), s))
            elif kind == "balance" and _BALFWD.search(label):
                fwds.append({**fig, "cite": cite, "_unit": s})           # 'Previous balance' is where the account stood before these charges, not the statement's balance
            elif kind == "balance":
                _put_stated(rec, stated, {"balance": {**fig, "cite": cite, "_unit": s}}, lines)
            elif cls == "charge":
                lines.append(_pline(rec, seg, "billed", fig, s, credit))
            elif cls == "estimate":
                rates.append(_rate_entry(rec, fig, seg.strip(), "An estimate is not a charge. It is not totaled.", kind="estimate", row=row))
            else:
                bad.append((raw, at))                        # no label the code recognises: listed, not totaled, never guessed to be a charge
        for m in _NUM.finditer(seg):                         # a decimal figure with no '$'
            if not any(m.start() < e2 and s2 < m.end() for s2, e2 in spans):
                bad.append((m.group(0), (s + m.start(), s + m.end())))
        if bad:
            lines.append(_blank_line(rec, "ledger", seg, description=seg.strip(), unparsed=True, unclear=bad, unit=s))
    return lines, stated, rates, fwds


def _pline(rec, seg, kind, fig, unit, credit=False):
    line = _blank_line(rec, "ledger", seg, description=seg.strip(), unit=unit)
    line[kind] = fig
    if kind == "billed":
        line["_credit"] = credit
    return line


# ------------------------------------------------------------------ CMS-1500 service lines (24F is implied-cents)
_AMT = r"(?:\d+\.\d{2}(?![\d.])|[0-9O]+(?:\s*\|\s*[0-9O]{2}(?!\w)|[ ][0-9O]{2}(?![\d.O]))|[0-9O]+(?!\w)(?!\s*\|)(?!\s+(?:\(?-?\$|\(?-?[0-9OolISB,]*\d[0-9OolISB,]*\.[0-9OolISB])))"      # a printed decimal point is honoured; the usual box has none
_CDATE = r"(?:[0-9O]{6}|\d{1,2}/\d{1,2}/\d{2,4})"
_CMS = re.compile(rf"^\s*(?:24\.\s*)?({_CDATE})\s+({_CDATE})\s+(\d{{2}})\s+([A-Z0-9]{{5}})(?:\s+[A-Z0-9]{{1,4}})*?\s+({_AMT})\s+(\d+)(?:\s+(\S+))?\s*$")
_CMS_TOTAL = re.compile(rf"\bTOTAL\s+CHARGE\s+({_FIG}|{_AMT})")          # a printed figure with a decimal point first: '1,234.50' is one figure, not the '1' of a box
_CMS_PAID = re.compile(rf"\bAMOUNT\s+PAID\s+({_FIG}|{_AMT})")
_CMS_MONEY = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?|(?<![\w/.])[0-9OolISB,]*\d[0-9OolISB,]*\.[0-9OolISB]{2}(?![\d.\w])|(?<![\w/.])\d+\s*\|\s*[0-9O]{2}\b")      # a printed '$' figure, a decimal figure or a boxed 85 | 00


def box_amount(raw: str) -> dict:
    """A CMS-1500 money box has no decimal point: '85 | 00', '85 00' and '8500' are all $85.00. A printed decimal point is honoured.
    OCR letters (O for 0) keep the text, cents None."""
    raw = raw.strip()
    if "O" in raw.upper().replace("|", ""):
        return {"text": raw, "cents": None, "usd": None, "implied_decimal": True}
    if re.fullmatch(_FIG, raw):
        return {**parse_figure(raw), "implied_decimal": False}
    if "|" in raw:
        d, c = [x.strip() for x in raw.split("|")]
        cents = int(d) * 100 + int(c)
    elif re.fullmatch(r"\d+ \d\d", raw):
        d, c = raw.split(" ")
        cents = int(d) * 100 + int(c)
    elif re.fullmatch(r"\d{3,}", raw):
        cents = int(raw)
    else:
        return {"text": raw, "cents": None, "usd": None, "implied_decimal": True}
    return {"text": raw, "cents": cents, "usd": fmt(cents), "implied_decimal": True}


def _cms1500(rec, lines):
    out, stated = [], {}
    offs = _offsets(lines)
    for i, ln in enumerate(lines):
        m = _CMS.match(ln)
        if m:
            fig = {**box_amount(m.group(5)), "_at": (offs[i] + m.start(5), offs[i] + m.end(5))}
            line = {"record_no": rec["n"], "form": "cms1500", "dos": m.group(1) if m.group(1) == m.group(2) else f"{m.group(1)}-{m.group(2)}", "dos_iso": None,
                    "posted": None, "code": m.group(4), "description": f"units {m.group(6)}", "billed": None, "adjustment": None, "paid": None,
                    "balance": None, "unclear": [], "_uat": [], "_unit": offs[i], "excerpt": ln.strip(), "units": int(m.group(6))}
            if fig["cents"] is None:
                _add_unclear(line, fig["text"], fig["_at"])
            else:
                line["billed"] = fig
                line["_credit"] = _is_credit(fig["text"])
            out.append(line)
        else:
            hit = False
            for kind, rx in (("billed", _CMS_TOTAL), ("paid", _CMS_PAID)):
                t = rx.search(ln)
                if t:
                    hit = True
                    stated[kind] = {**box_amount(t.group(1)), "cite": _cite(rec, ln), "_at": (offs[i] + t.start(1), offs[i] + t.end(1)), "_unit": offs[i]}      # unreadable ones keep cents None and are listed by the caller
            if hit:
                continue
            toks = [(t.group(0).strip(), (offs[i] + t.start(), offs[i] + t.end())) for t in _CMS_MONEY.finditer(ln)]
            rest = re.match(rf"^\s*(?:24\.\s*)?{_CDATE}\s+(?:{_CDATE}\s+)?(.*)$", ln)
            if toks or (rest and re.search(r"\d", rest.group(1))):      # carries a money figure, or is dated and has digits, but did not fit the 24 layout: listed, never dropped
                out.append(_blank_line(rec, "cms1500", ln, unparsed=True, unit=offs[i], unclear=toks))      # the row excerpt is in the entry; only money tokens are figures
    return out, stated


# ------------------------------------------------------------------ UB-04 (FL 44 rate is never a charge; FL 47 is; 0001 is the total)
_UBROW = re.compile(r"^\s*(\d{4})\s+(\S.*?)(?:\s{2,}|$)")


def _ub_header(lines):
    hi = next((i for i, ln in enumerate(lines) if re.search(r"TOTAL\s+CHARGES", ln, re.IGNORECASE) and re.search(r"\bREV\b|SERV", ln)), None)
    if hi is None:
        return None, {}
    cols = {}
    for kind, rx in (("rate", r"HCPCS/RATE|RATE"), ("billed", r"TOTAL\s+CHARGES"), ("noncovered", r"NON-COVERED")):
        m = re.search(rx, lines[hi])
        if m:
            cols[kind] = (m.start(), m.end())
    return hi, cols


def _ub_all_cols(lines):
    """(index, columns) with the UB-04 header's non-money columns too (units, service date), so a whole number is told to sit under UNITS rather than
    under the money column it drifts toward when a description is long."""
    hi, cols = _ub_header(lines)
    if hi is None:
        return None, {}
    for kind, rx in (("units", r"\bUNITS\b"), ("servdate", r"SERV\s+DATE")):
        m = re.search(rx, lines[hi])
        if m:
            cols[kind] = (m.start(), m.end())
    return hi, cols


def _ub04(rec, lines):
    hi, cols = _ub_all_cols(lines)
    if hi is None:
        return [], {}, []
    offs = _offsets(lines)
    out, rates, stated = [], [], {}
    for i in range(hi + 1, len(lines)):
        ln = lines[i]
        m = _UBROW.match(ln)
        if not m:
            toks = [(t.group(0), (offs[i] + t.start(), offs[i] + t.end())) for t in _tokens(ln)]
            if toks:                                  # a figure on a line that is not a revenue-code row: listed, never dropped
                out.append(_blank_line(rec, "ub04", ln, unparsed=True, unit=offs[i], unclear=toks))
            continue
        figs = [(f, _column(f.span(), cols)) for f in _tokens(ln)]
        if m.group(1) == "0001":
            for f, k in figs:
                if k == "billed":
                    stated["billed"] = {**_pf(f, offs[i]), "cite": _cite(rec, ln), "_unit": offs[i]}
            continue
        line = {"record_no": rec["n"], "form": "ub04", "dos": None, "dos_iso": None, "posted": None, "code": m.group(1), "description": m.group(2).strip(),
                "billed": None, "adjustment": None, "paid": None, "balance": None, "unclear": [], "_uat": [], "_unit": offs[i], "excerpt": ln.strip(), "non_covered": None}
        sd = re.search(r"\b(\d{6})\b", ln[:figs[0][0].start()] if figs else ln)
        line["dos"] = sd.group(1) if sd else None
        row_rate = []
        for f, k in figs:
            p = _pf(f, offs[i])
            if p["cents"] is None or k is None or k in _NONMONEY:
                _add_unclear(line, p["text"], p["_at"])
            elif k == "rate":
                rates.append(_rate_entry(rec, p, ln.strip(), "UB-04 line 44 is a rate, not a charge.", row=_row_span(offs[i], ln)))
                row_rate.append(rates[-1])
            elif k == "noncovered":
                line["non_covered"] = p
            elif line["billed"] is None:
                line["billed"] = p
                line["_credit"] = _is_credit(p["text"])
            else:
                _add_unclear(line, p["text"], p["_at"])
        if row_rate:                                  # T-103 r4: the room row's FL 47 total (and a non-covered figure) are other figures of the FL 44 rate entry, listed once, as that entry's
            for key in ("billed", "non_covered"):
                if line[key] is not None:
                    _add_other(row_rate[0], line[key])
                    line[key] = None
            if not line["unclear"]:
                continue                              # nothing else on the row: no line of its own
        out.append(line)
    return out, stated, rates


# ------------------------------------------------------------------ EOB (payer figures; listed as lines, never added to charges or compared)
_EOBCOLS = (("billed", r"BILLED"), ("discount", r"DISCOUNT|NOT\s+COVERED"), ("allowed", r"ALLOWED"), ("deductible", r"DEDUCT\w*"), ("copay", r"COPAY"),
            ("coinsurance", r"COINS\w*"), ("plan_paid", r"PLAN\s+PAID"), ("patient_owes", r"YOU\s+MAY\s+OWE|PATIENT\s+RESP\w*"))
_EOBROW = re.compile(rf"^\s*({_DATE})\s+(\S+)\s+")


def _eob_header(lines):
    """(index, {column name: (start, end)}) of the EOB column header (BILLED and PLAN PAID on one line), or (None, None)."""
    hi = next((i for i, ln in enumerate(lines) if re.search(r"\bBILLED\b", ln) and re.search(r"PLAN\s+PAID", ln, re.IGNORECASE)), None)
    if hi is None:
        return None, None
    return hi, {k: (m.start(), m.end()) for k, rx in _EOBCOLS for m in [re.search(rx, lines[hi], re.IGNORECASE)] if m}


def _eob_tokens(ln, cols, service=None):
    """Money-shaped tokens of an EOB line: decimals, '$' figures with no cents and whole numbers under a money column. The service slot of a row, a
    procedure code that follows a money-shaped service slot (a five-character code before the row's first figure) and the number inside a reason code
    (PR-1, CO-45) are not money."""
    out = []
    slot_money = bool(service and (_MONEY.fullmatch(ln, service[0], service[1]) or _ACC_MONEY.fullmatch(ln, service[0], service[1])))
    for m in _tokens(ln, cols):
        if service and m.start() < service[1] and service[0] < m.end():
            continue
        if re.fullmatch(r"[\d,]+", m.group(0)) and re.search(r"[A-Za-z]-$", ln[:m.start()]):
            continue
        if slot_money and not out and re.fullmatch(r"(?:[A-Z]\d{4}|\d{5})", m.group(0)):
            continue                                  # the code of the service, pushed right by a money-shaped token in the service slot
        out.append(m)
    return out


def _eob(rec, lines):
    """(row lines, unparsed lines). Each service row (date, service code, figures) is one line of form eob: its figures are in `eob` (by column) when
    every figure was read and there is one per column; otherwise EVERY money token of the row is in `unclear` with its text, never dropped."""
    hi, cols = _eob_header(lines)
    offs = _offsets(lines)

    def unp(i, toks):
        return _blank_line(rec, "eob", lines[i], unparsed=True, unit=offs[i], unclear=[(t.group(0), (offs[i] + t.start(), offs[i] + t.end())) for t in toks])
    if hi is None:
        return [], [unp(i, _tokens(ln)) for i, ln in enumerate(lines) if _tokens(ln)]
    names = [k for _, k in sorted((s0, k) for k, (s0, _e) in cols.items())]
    out, unparsed = [], [unp(i, _tokens(lines[i])) for i in range(hi) if _tokens(lines[i])]
    for i in range(hi + 1, len(lines)):
        ln = lines[i]
        m = _EOBROW.match(ln)
        if not m:
            if _tokens(ln):                           # a printed EOB total row, or any figure outside a service row: listed, never dropped
                unparsed.append(unp(i, _tokens(ln)))
            continue
        toks = _eob_tokens(ln, cols, m.span(2))
        figs = [_pf(t, offs[i]) for t in toks]
        line = _blank_line(rec, "eob", ln, dos=m.group(1), code=m.group(2), unit=offs[i])
        line["eob"], line["eob_codes"] = {}, (ln[toks[-1].end():].strip() or None) if toks else None
        if len(figs) == len(names) and all(f["cents"] is not None for f in figs):
            line["eob"] = {k: _mag(f) for k, f in zip(names, figs)}
        else:
            for f in figs:
                _add_unclear(line, f["text"], f["_at"])
        out.append(line)
    return out, unparsed


# ------------------------------------------------------------------ LOP / lien amounts (listed, never totaled)
_LOP_SOURCE = re.compile(r"letter\s+of\s+protection|\bLOP\b|\blien\b|reduction\s+letter|assignment", re.IGNORECASE)
_LOP_LABEL = re.compile(r"\b(?:LOP|lien)\b[^,;]{0,25}\b(?:balance|amount)|\b(?:balance|amount)\b[^,;]{0,25}\b(?:LOP|lien)\b|\breduced\s+to\b|\baccept\w*\b[^.;]{0,50}\bsatisf\w+|"
                        r"\b(?:atty|attorney)\s+reduction\b|\bcurrent\s+balance\b|\bin\s+full\s+satisfaction\b", re.IGNORECASE)


def _lop_lien(rec):
    body = rec.get("excerpt") or rec.get("text") or ""
    doc = bool(_LOP_SOURCE.search(rec.get("source") or ""))
    out = []
    for s, e in _segments(body):
        seg = body[s:e]
        for a in A.find_amounts(seg):
            if a["cents"] is None:
                continue
            label = A._label(seg, a["start"])
            if not (doc or _LOP_LABEL.search(label) or _LOP_LABEL.search(seg)):
                continue
            kind = "reduction" if re.search(r"reduc|satisf", seg, re.IGNORECASE) else ("lien_amount" if re.search(r"\blien\b", seg, re.IGNORECASE) else "asserted_balance")
            at = (s + a["start"], s + a["end"])
            out.append({"record_no": rec["n"], "provider": _provider(rec), "kind": kind, "label": " ".join(label.split()) or None,
                        "figure": {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"]), "_at": at}, "excerpt": seg.strip(), "in_totals": False,
                        "_at": at, "_row": _row_span(s, seg), "other_figures": []})
    return out


# ------------------------------------------------------------------ D-049: the final accounting pass
# Every money-shaped token the record prints must end up in one of four places: a parsed figure (a line, a stated total, a balance forward), an
# unreconciled line, an excluded rate (or an LOP/lien amount, which is listed apart), or on its row as `unclear`. This pass reads the raw text with
# its OWN tokenizer, after every parser has run, and lists whatever no parser placed; no provider completeness is claimed. A rate or LOP entry's
# other money tokens (a running balance on a price row) become its `other_figures`.
_A = r"[0-9OolISB]"
_ACC_MONEY = re.compile(rf"\(?-?\$\s?{_A}[0-9OolISB,]*(?:\.{_A}+)?\)?-?(?![\w/])|(?<![\w/.$])\(?-?[0-9OolISB,]*[0-9][0-9OolISB,]*\.{_A}{{2}}\)?-?(?![\w/]|\.\d)")
_PROSE_BARE = re.compile(r"(?<![\w/.,$:#%-])\(?\d[\d,]*\)?(?![\w/%:-]|[.,]\d)")
_AFTER_UNIT = re.compile(r"\s*(?:visits?|units?|sessions?|days?|hours?|hrs?|minutes?|mins?|weeks?|months?|years?|yrs?|times|x\b|mg|ml|cc|of\b|per\b)", re.IGNORECASE)
_BEFORE_ID = re.compile(r"(?:\bx|\b(?:CPT|HCPCS|codes?|ICD(?:-10)?|invoice|inv|acct|account|claim|record|page|pg|ref|no|number|npi|id|mrn|fl|box|item|line|rev|ext|phone|tel|zip|visits|sessions|units|days|through|thru)|#)\s*[:#.]?\s*$", re.IGNORECASE)
_CODE5 = re.compile(r"\b(?:[A-Z]\d{4}|\d{5})\b")


_AFTER_FIGURE = re.compile(r"(?:\$\s?[\dOolISB][\dOolISB,]*(?:\.[\dOolISB]+)?|\d[\dOolISB,]*\.[\dOolISB]+)\)?-?\s+$")


def _prose_bare(u):
    """Whole numbers in a sentence that could be money: not part of a date, a time, a phone number, a code, a year, a count of visits/units/days, and
    not a number that directly follows another money figure with no word between (that is the tail of that figure's phrase, not a figure of its own)."""
    plain, out = _blank_dates(u), []
    for m in _PROSE_BARE.finditer(plain):
        digits = re.sub(r"\D", "", m.group(0))
        if _AFTER_UNIT.match(plain, m.end()) or _BEFORE_ID.search(plain[:m.start()]) or _AFTER_FIGURE.search(plain[:m.start()]):
            continue
        if re.fullmatch(r"(?:19|20|21)\d\d", digits) and "," not in m.group(0) or re.fullmatch(r"[79]\d{4}", digits):
            continue
        out.append(m)
    return out


def _cms_candidates(u):
    """A CMS-1500 line with a procedure code that fit no 24 layout (no dates, no units): the whole numbers after the code are its possible charge.
    The last one is the units box when there are two or more."""
    c = _CODE5.search(_blank_dates(u))
    if not c:
        return []
    nums = [m for m in re.finditer(r"(?<![\w/.-])\d+(?![\w/-])", _blank_dates(u)) if m.start() > c.end()]
    return nums[:-1] if len(nums) > 1 else nums


def _span_merge(found):
    """[(start, end, text)] with overlaps resolved in favour of the longer token."""
    out = []
    for a in sorted(found, key=lambda t: (t[0], -(t[1] - t[0]))):
        if not out or a[0] >= out[-1][1]:
            out.append(a)
    return out


def _unit_tokens(form, u, cols, below_header):
    found = [(m.start(), m.end(), m.group(0)) for m in _ACC_MONEY.finditer(u)]
    if form == "ledger_table":
        if below_header:
            found += [(m.start(), m.end(), m.group(0)) for m in _tokens(u, cols, all_bare=bool(_BALFWD.search(u)))]
        else:
            found += [(m.start(), m.end(), m.group(0)) for m in _tokens(u)]
    elif form == "ledger_text":
        found += [(m.start(), m.end(), m.group(0)) for m in _prose_bare(u)]
    elif form == "ub04":
        toks = _tokens(u, cols) if below_header else _tokens(u)
        if below_header and _UBROW.match(u):             # a revenue-code row: the charges are its last figure, so a whole number with a decimal figure to its right is a count (units), not money
            last_dec = max([m.start() for m in toks if re.search(r"[.$]", m.group(0))], default=-1)
            toks = [m for m in toks if re.search(r"[.$]", m.group(0)) or m.start() > last_dec]
        found += [(m.start(), m.end(), m.group(0)) for m in toks]
    elif form == "eob":
        row = _EOBROW.match(u)
        found += [(m.start(), m.end(), m.group(0)) for m in (_eob_tokens(u, cols, row.span(2) if row else None) if below_header else [])]
        found += [(m.start(), m.end(), m.group(0)) for m in _tokens(u)]            # decimals and '$' figures anywhere on the row, the service slot included
    elif form == "cms1500":
        found += [(m.start(), m.end(), m.group(0).strip()) for m in _CMS_MONEY.finditer(u)]
        found += [(m.start(), m.end(), m.group(0)) for m in _tokens(u)]                  # an odd decimal ('9.999') is a token too
        strict = _CMS.match(u)
        if strict:
            found.append((strict.start(5), strict.end(5), strict.group(5)))
        for rx in (_CMS_TOTAL, _CMS_PAID):
            t = rx.search(u)
            if t:
                found.append((t.start(1), t.end(1), t.group(1)))
        if not strict and not _CMS_TOTAL.search(u) and not _CMS_PAID.search(u):
            found += [(m.start(), m.end(), m.group(0)) for m in _cms_candidates(u)]
    return _span_merge(found)


def _placed(got, stated, bfs, holders):
    """[(start, end)] of every token of this record that some field of the output already shows: a parsed figure, a listed `unclear` token, a printed
    total, a balance forward, a rate or LOP entry's figure and its other figures. Read from the positions the parsers recorded."""
    spans = []
    for d in _walk([got, list(stated.values()), list(bfs), holders]):
        if "_at" in d:
            spans.append(d["_at"])
        spans += d.get("_uat") or []
    return spans


def _has_figure(l):
    return bool(l["billed"] or l["adjustment"] or l["paid"] or l["balance"] or l.get("non_covered") or l.get("eob"))


def _add_other(h, fig):
    """Put a token among an entry's other figures once: a token already there (same position) is not added again."""
    if not any(_lap(fig["_at"], f["_at"]) for f in h["other_figures"]):
        h["other_figures"].append(fig)


def _hold(got, stated, bfs, rates, lop):
    """(lines, rate/estimate entries, LOP entries) with one entry per printed row. The first figure of a rate, estimate or LOP/lien row is the entry; every
    OTHER money token printed on that row becomes one of its `other_figures`, wherever a parser first put it: a second amount in the sentence, a running
    balance the table parser left as an unclear figure, a printed total or balance on the same row. A token the entry already shows as its own figure is
    shown once. Positions decide all of this; no figure text is compared."""
    keep = []
    for h in sorted(list(rates) + list(lop), key=lambda h: h["_at"][0]):
        if any(_lap(h["_at"], k["_at"]) for k in keep):
            continue                                           # the same printed figure read as a rate and as an LOP amount: one entry
        host = next((k for k in keep if _within(h["_at"], k["_row"])), None)
        if host is not None:
            _add_other(host, {**parse_figure(h["figure"]["text"]), "_at": h["_at"]})          # read as the row prints it: a no-cents figure keeps its text and no value
        else:
            keep.append(h)
    out = []
    for l in got:
        had = bool(l["unclear"])
        pairs = []
        for t, sp in zip(l["unclear"], l.get("_uat") or []):
            h = next((k for k in keep if _within(sp, k["_row"])), None)
            if h is None:
                pairs.append((t, sp))
            elif not _lap(sp, h["_at"]):
                _add_other(h, {**parse_figure(t), "_at": sp})          # else: the entry's own figure, listed on its row too: shown once, as the entry
        l["unclear"], l["_uat"] = [t for t, _ in pairs], [sp for _, sp in pairs]
        if not (had and not pairs and (l.get("unparsed") or not _has_figure(l))):
            out.append(l)
    for h in keep:
        for k in [k for k, v in stated.items() if _within(v["_at"], h["_row"])]:
            v = stated.pop(k)
            if not _lap(v["_at"], h["_at"]):
                _add_other(h, {kk: v[kk] for kk in ("text", "cents", "usd", "_at")})
        for v in [v for v in bfs if _within(v["_at"], h["_row"])]:
            bfs.remove(v)
            if not _lap(v["_at"], h["_at"]):
                _add_other(h, {kk: v[kk] for kk in ("text", "cents", "usd", "_at")})
    is_rate = {id(x) for x in rates}
    return out, [h for h in keep if id(h) in is_rate], [h for h in keep if id(h) not in is_rate]


def _account(rec, form, body, ls, offs, got, stated, bfs, holders):
    """The tokens no parser placed, as unparsed lines (one per printed row; an unparsed line already on that row is extended). A token on a rate,
    estimate or LOP/lien row becomes that entry's other figure. `got` is mutated only by extending an existing line's `unclear`. A token is told from
    another with the same text by where it sits in the record."""
    placed = _placed(got, stated, bfs, holders)
    hi, cols = _header(ls) if form == "ledger_table" else _ub_all_cols(ls) if form == "ub04" else _eob_header(ls) if form == "eob" else (None, None)
    units = [(body[s:e], s, True) for s, e in _segments(body)] if form == "ledger_text" else [(u, offs[i], hi is not None and i > hi) for i, u in enumerate(ls)]
    lform = "ledger" if form.startswith("ledger") else form
    extra = []
    for u, base, below in units:
        us = u.strip()
        if not us:
            continue
        mine = next((l for l in got if l.get("unparsed") and l.get("_unit") == base), None)
        missing = []
        for a, b, text in _unit_tokens(form, u, cols, below):
            at = (base + a, base + b)
            if any(_lap(at, p) for p in placed):
                continue
            placed.append(at)
            host = next((h for h in holders if _within(at, h["_row"])), None)
            if host is not None:
                _add_other(host, {**parse_figure(text), "_at": at})
            elif not (mine and form == "cms1500" and re.fullmatch(r"\d+", text)):      # a bare whole number on a row already listed whole stays on that row's excerpt
                missing.append((text, at))
        if missing:
            if mine:
                for t, at in missing:
                    _add_unclear(mine, t, at)
            else:
                extra.append(_blank_line(rec, lform, us, description=us if form == "ledger_text" else "", unparsed=True, unit=base, unclear=missing))
    return extra


# ------------------------------------------------------------------ assembling
def _line_span(body, start, end):
    """Offsets of the whole printed line a figure sits on (a verbatim excerpt); a single-line paragraph gives the clause around it."""
    a, b = body.rfind("\n", 0, start) + 1, body.find("\n", end)
    b = len(body) if b < 0 else b
    if b - a > 240:
        for s, e in _segments(body):
            if s <= start < e:
                return _row_span(s, body[s:e])
    return _row_span(a, body[a:b])


def _checks_for_line(line):
    """ROW_NOT_PARSED for a row that fit no layout, LINE_UNCLEAR when a figure could not be read. Nothing is computed from the figures."""
    if line.get("unparsed"):
        return ["ROW_NOT_PARSED"]
    return ["LINE_UNCLEAR"] if line["unclear"] else []


def _own_cites(lines):
    """Every line cites only its own record. Nothing is merged or deduplicated across records or providers (T-103 r3): two providers' identical
    rows are two lines, and a re-sent statement is two lines, one per record. A byte-identical repeat of a whole record is dropped at ingest
    (`duplicate_of`), not here. Order is record number, then position in the record; a line's id is that order."""
    return [{**l, "record_nos": [l["record_no"]], "cites": [{"record_no": l["record_no"], "excerpt": l["excerpt"]}]} for l in lines]


def _billing_looking(rec, body):
    """A record that is a bill by its source label or its own words (invoice, total charges) and carries a decimal figure, but fits no known form."""
    src = rec.get("source") or ""
    return bool(_NUM.search(body) and (A._is_billing_source(src) or re.search(r"\binvoice\b|\bTOTAL\s+CHARGES?\b", body, re.IGNORECASE)))


def _strip_private(o):
    """The positions and flags the parsers keep for themselves (keys starting with an underscore) are not part of the response."""
    if isinstance(o, dict):
        return {k: _strip_private(v) for k, v in o.items() if not k.startswith("_")}
    if isinstance(o, list):
        return [_strip_private(v) for v in o]
    return o


def analyze(records: list) -> dict:
    """The whole analysis of a case from its ingested records (needs n, excerpt; uses text, source, duplicate_of). Pure; no I/O."""
    recs = [r for r in records if not r.get("duplicate_of")]
    lines, stated_by_rec, lop, excluded, balfwds, rec_form = [], {}, [], [], {}, {}
    skipped = []
    for r in recs:
        body = r.get("excerpt") or r.get("text") or ""
        ls = body.split("\n")
        offs = _offsets(ls)
        form = form_of(r)
        if r.get("injection_tag") and (form or _lop_lien(r)):      # a figure inside instruction-like text has no trusted value (D-005)
            skipped.append({"record_no": r["n"], "reason_code": "INJECTION_SUSPECTED"})
            continue
        rec_form[r["n"]] = form
        got, rates, st, bf = [], [], {}, []
        if form == "ledger_table":
            got, st, bf, rates = _ledger_table(r, ls)
        elif form == "ledger_text":
            got, st, rates, bf = _ledger_text(r, body)
        elif form == "cms1500":
            got, st = _cms1500(r, ls)
        elif form == "ub04":
            got, st, rates = _ub04(r, ls)
        elif form == "eob":
            rows_, unp_ = _eob(r, ls)
            got = rows_ + unp_
        elif _billing_looking(r, body):                  # a bill in a layout no parser here knows (an ambulance invoice, say): shown, not silently absent
            skipped.append({"record_no": r["n"], "reason_code": "UNRECOGNISED_BILLING_FORM"})
        stated_by_rec[r["n"]], balfwds[r["n"]] = st, bf
        if form in ("ledger_table", "ledger_text", "cms1500", "ub04"):
            got = got + _stated_orphans(r, "ledger" if form.startswith("ledger") else form, got, st)
        if form == "ledger_table":                       # a statement's fee-schedule line is a rate and carries no date of service
            for a in A.find_amounts(body):
                if a["cents"] is not None and A.classify(body, a, source=r.get("source"), strict=False) == "rate":
                    at = (a["start"], a["end"])
                    if not any(_lap(at, x["_at"]) for x in rates):                    # a figure a table row already gave as a rate is not listed again
                        row = _line_span(body, a["start"], a["end"])
                        rates.append(_rate_entry(r, {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"]), "_at": at}, body[row[0]:row[1]], row=row))
        got, rates, lop_here = _hold(got, st, bf, rates, _lop_lien(r))
        if form in ("ledger_table", "ledger_text", "cms1500", "ub04", "eob"):
            got = got + _account(r, form, body, ls, offs, got, st, bf, rates + lop_here)      # D-049: the last word on what was lost
        lines += got
        excluded += rates
        lop += lop_here
    fwd_by_prov = {}
    for r in recs:
        for bf in balfwds.get(r["n"]) or []:
            fwd_by_prov.setdefault(_norm(_provider(r)), []).append((r, bf))
    for found_fwd in fwd_by_prov.values():
        if len(found_fwd) > 1:                           # several balance-forward rows for one provider: every one is listed, none is picked (D-049)
            for r, bf in found_fwd:
                lines.append(_blank_line(r, "ledger", bf["cite"]["excerpt"], unparsed=True, unit=bf["_unit"], unclear=[(bf["text"], bf["_at"])]))
    stated_by_prov = {}
    for r in recs:                                       # a second statement's TOTAL CHARGES / BALANCE DUE (a summary row of one kind, same form family) is listed, never overwritten
        for k, v in (stated_by_rec.get(r["n"]) or {}).items():
            stated_by_prov.setdefault((_norm(_provider(r)), _family(rec_form.get(r["n"])), k), []).append((r, v))
    for found_st in stated_by_prov.values():
        if len(found_st) > 1:
            for r, v in found_st:
                lines.append(_blank_line(r, _family(rec_form.get(r["n"])), v["cite"]["excerpt"], unparsed=True, unit=v["_unit"], unclear=[(v["text"], v["_at"])]))
    by_n = {r["n"]: r for r in recs}
    for ln in lines:
        ln["provider"] = _provider(by_n[ln["record_no"]])
    lines = _own_cites(lines)
    for l in lines:
        l["checks"] = _checks_for_line(l)
    for l in lines:
        l["detail"] = "eob" if l["form"] == "eob" and not l.get("unparsed") else ("reversal" if l["billed"] and (l.get("_credit") or _VOID.search(l["description"] or "")) else
                       "balance_only" if l["balance"] and not (l["billed"] or l["paid"] or l["adjustment"] or l["unclear"]) else None)
        l["class"] = "charge" if l["billed"] else "payment" if l["paid"] else "adjustment" if l["adjustment"] else "unclear"
        l["negotiated"] = bool(l["adjustment"] and _NEGOTIATED.search(l["description"] or ""))
        l["unparsed"] = bool(l.get("unparsed"))
        if l["form"] == "ledger" and l["billed"] and not l["dos"]:
            l["checks"].append("NO_DATE_OF_SERVICE")
    parsed = [l for l in lines if not l["unparsed"]]
    unreconciled = [{"provider": l["provider"], "record_no": l["record_no"], "form": l["form"], "class": "unclear", "reason_code": "ROW_NOT_PARSED",
                     "message": CHECKS["ROW_NOT_PARSED"], "excerpt": l["excerpt"], "figures": l["unclear"]} for l in lines if l["unparsed"]]

    def extra(n, cls, detail, fig, excerpt, why, others=()):
        """A cited line that is not a ledger row: a rate, an estimate, an LOP/lien amount, a printed total or a balance forward."""
        f = rec_form.get(n)
        return {"class": cls, "detail": detail, "provider": _provider(by_n[n]), "record_no": n, "record_nos": [n], "form": _family(f) if f else None,
                "figure": fig, "other_figures": list(others), "why": why, "excerpt": excerpt, "cites": [{"record_no": n, "excerpt": excerpt}]}
    extras = [extra(x["record_no"], "rate" if x["kind"] == "rate" else "unclear", x["kind"], x["figure"], x["excerpt"], x["why"], x.get("other_figures", [])) for x in excluded]
    extras += [extra(x["record_no"], "unclear", x["kind"], x["figure"], x["excerpt"], "An LOP, lien or reduction amount is listed apart from the charges.", x.get("other_figures", [])) for x in lop]
    for r in recs:                                       # a printed total or a balance forward is a line too (each record's own, never merged), unless the same printed token is already listed with its row
        shown = _placed([l for l in lines if l["record_no"] == r["n"]], {}, [], [x for x in excluded + lop if x["record_no"] == r["n"]])
        for kind, v in list((stated_by_rec.get(r["n"]) or {}).items()) + [("balance_forward", bf) for bf in balfwds.get(r["n"]) or []]:
            if any(_lap(v["_at"], p) for p in shown):
                continue                                 # already listed with its row (unreconciled, a rate or an LOP amount)
            extras.append(extra(r["n"], "unclear", kind if kind == "balance_forward" else f"stated_total_{kind}", {k: v[k] for k in ("text", "cents", "usd", "_at")}, v["cite"]["excerpt"],
                                "A figure the statement prints itself. It is listed, never added to the lines."))      # one line per record, never merged with another record's
    listing = sorted(parsed + extras, key=lambda l: l["record_no"])
    for i, l in enumerate(listing, 1):
        l["id"] = f"b{i}"
    for i, u in enumerate(unreconciled, 1):
        u["id"] = f"u{i}"
    return _strip_private({"status": "listed" if (listing or unreconciled or skipped) else "none_found",
                           "lines": listing, "unreconciled": unreconciled, "skipped_records": skipped, "rules": RULES})


_FIG_KEYS = ("billed", "adjustment", "paid", "balance", "discount", "allowed", "deductible", "copay", "coinsurance", "plan_paid", "patient_owes", "non_covered")


def _figure_like(v):
    return isinstance(v, dict) and isinstance(v.get("text"), str) and "cents" in v


def _in(text, excerpt):
    return text in excerpt or text.lstrip("-") in excerpt


def _walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from _walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v)


def verify_citations(analysis: dict, records: list) -> list:
    """[] when every cited excerpt anywhere in the analysis is a verbatim substring of the record it names, and every figure text sits inside the
    excerpt it is cited to. The reference is the record's own text (the ingested block), never the excerpt being checked. Covers lines (EOB row figures
    included), cites and unreconciled rows. Returns [{ref, reason}]; `for_case` puts the list in the response as
    `citation_failures`."""
    text_of = {r["n"]: (r.get("text") or r.get("excerpt") or "") for r in records}
    bad = []
    for d in _walk({k: v for k, v in analysis.items() if k != "rules"}):
        ref = d.get("id") or d.get("code") or "?"
        if "excerpt" in d and "record_no" in d:
            if d["excerpt"] not in text_of.get(d["record_no"], ""):
                bad.append({"ref": ref, "reason": "excerpt_not_verbatim"})
            for k, v in d.items():
                if k in _FIG_KEYS and _figure_like(v) and not _in(v["text"], d["excerpt"]):
                    bad.append({"ref": ref, "reason": f"{k}_not_in_excerpt"})
            for k, v in (d.get("eob") or {}).items():
                if _figure_like(v) and not _in(v["text"], d["excerpt"]):
                    bad.append({"ref": ref, "reason": f"eob_{k}_not_in_excerpt"})
            if _figure_like(d.get("figure")) and not _in(d["figure"]["text"], d["excerpt"]):
                bad.append({"ref": ref, "reason": "figure_not_in_excerpt"})
            for v in d.get("other_figures") or []:
                if _figure_like(v) and not _in(v["text"], d["excerpt"]):
                    bad.append({"ref": ref, "reason": "other_figure_not_in_excerpt"})
    seen, out = set(), []
    for b in bad:
        k = (b["ref"], b["reason"])
        if k not in seen:
            seen.add(k)
            out.append(b)
    return out


def checked(analysis: dict, records: list) -> dict:
    """The analysis plus its citation check. A failure is shown (`citation_failures`, status `citation_failed`), never swallowed; nothing is dropped silently."""
    fails = verify_citations(analysis, records)
    analysis["citation_failures"] = fails
    if fails:
        analysis["status"] = "citation_failed"
    return analysis


def for_case(conn, case_id: str) -> dict:
    from app.backend import store      # imported here so unit tests of the pure functions need no database
    records = store.load_records(conn, case_id)
    return checked(analyze(records), records)


def add_routes(app, *, conn, get_case):
    @app.get("/api/cases/{token}/billing")
    def billing_get(token: str):
        c = conn()
        try:
            get_case(c, token)
            return {"billing": for_case(c, token)}
        finally:
            c.close()
