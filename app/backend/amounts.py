"""Dollar amounts: find, classify, dedupe (all code; ADR-011, R-CH-1/2/4/6, D-004/D-005, LLM_VS_CODE rows 6 and 7).
Money is whole cents (int). Noisy OCR figures keep their verbatim text with cents None and class unclear, never corrected.
There is no LLM classifier. A rate can never become a charge: classes are decided here and the paralegal can only accept or dismiss."""
import functools
import re

from app.backend import dates as _dates, injection, lexicon

# '$' + a whole numeric token (extra decimals are kept so to_cents can refuse them: never truncated).
# '$' + a figure. Letters that OCR confuses with digits (O o l I S B) are tolerated so noise is LISTED (unclear), not silently skipped.
_AMT = re.compile(r"\$\s?([0-9OolISB](?:[0-9OolISB,]*[0-9OolISB])?(?:\.[0-9OolISB]+)?)")
_VALID = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?\Z")
_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
_LEADER = re.compile(r"(?:\.[ ]?){3,}|\u2026+")


def mask_leaders(text: str) -> str:
    """The same text with every dotted leader ('.......', '. . . .', '\u2026') replaced by as many middle dots, so positions are unchanged: a leader is neither a sentence end
    nor a column gap nor a date's lookbehind (T-209 r2, T-202 r5: 'Date of service.......02/02/2026   Office visit 99213 ...... $275.00' is one itemized line). The classifier and the
    date resolver (service_date) both read leader-masked text."""
    return _LEADER.sub(lambda m: "\u00b7" * len(m.group(0)), text or "") if isinstance(text, str) else text


def _masked(fn):
    """Decorator for the readers whose first argument is a record's excerpt: they read it leader-masked."""
    @functools.wraps(fn)
    def wrapper(excerpt, *args, **kwargs):
        return fn(mask_leaders(excerpt), *args, **kwargs)
    return wrapper
# Rate = unit-rate phrasing only. 'Charge per invoice 4471: $400' is NOT a rate (per + a non-unit noun stays a charge or unclear).
_UNIT = r"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment|mile)s?"
# Spanish unit nouns (T-110 r2): "por sesión", "por visita", "cada ...". Accents are optional because pasted records often lose them.
_UNIT_ES = r"(?:sesi[o\u00f3]n|sesiones|visitas?|horas?|d[i\u00ed]as?|unidad(?:es)?|citas?|tratamientos?|procedimientos?)"
_RATE_WORD = re.compile(rf"\b(?:(?:per|each)[\s-]+{_UNIT}|rate\s+of|(?:por|cada)\s+{_UNIT_ES})\b|/\s*{_UNIT}\b|/\s*{_UNIT_ES}\b", re.IGNORECASE)
_RATE_AFTER = re.compile(rf"^\s*(?:(?:per|each|an?)[\s-]+{_UNIT}\b|(?:por|cada)\s+{_UNIT_ES}\b|/\s*{_UNIT}\b|each\b|cada\s+(?:una?|uno)\b|(?:hourly|daily|weekly|monthly|apiece)\b|an?\s+(?:month|week)\b)", re.IGNORECASE)
_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)      # the pre-D-060 listing rule (strict=False), used by billing.py only
_ESTIMATE = re.compile(r"\bestimat(?:e|ed|es)\b", re.IGNORECASE)
_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
# ONE rate-cue test for every code path that decides "is this figure a unit price?" (reclassify.py wording gate, billing.py ledger rows and
# sentences). A cue is decisive: "Charge per visit $185" and "Billed $150 per visit" state a rate, whatever else the text says (D-042, T-084 r2).
_RATE_CORE = (r"\bper\b|\beach\b|\bevery\b|\bcada\b|\bpor\s+(?:sesi[o\u00f3]n|sesiones|visitas?|horas?|d[i\u00ed]as?|unidad(?:es)?|citas?|tratamientos?|procedimientos?)\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
              r"|\ban?\s+(?:visit|session|hour|hr|day|treatment|appointment|unit|procedure|month|week)\b|\b(?:daily|hourly|weekly|monthly|session|visit|unit|flat)\s+(?:rate|fee|price|cost)\b|\brate\b"
              r"|\b(?:hourly|daily|weekly|monthly|apiece)\b|\bunit\s+(?:price|cost|charge)\b|@\s*\$"
              r"|\b\d+\s*[x\u00d7]\s*\$?\d")
_RATE_X_COUNT = r"(?<![\w$])[x\u00d7]\s*\d+\b"            # "x 14": a multiplier in a sentence, but plain unit notation ("Manual therapy x1") in a ledger row
RATE_CUE = re.compile(_RATE_CORE + "|" + _RATE_X_COUNT, re.IGNORECASE)
_RATE_CUE_ROW = re.compile(_RATE_CORE, re.IGNORECASE)


def has_rate_cue(text: str, unit_notation: bool = False) -> bool:
    """True when the text carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate, rate of ...). `unit_notation=True` is for a
    ledger row's description, where "x1" / "x2" is the unit count of a normal charge line and not a multiplier."""
    return bool((_RATE_CUE_ROW if unit_notation else RATE_CUE).search(text or ""))


# Spanish charge and balance cues (T-110 r3, D-050). The classifier does NOT use them: a Spanish figure stays `unclear` until the paralegal reads the
# original and reclassifies it, and only the reclassify guard (code cue + judge re-check) reads them. A rate cue above still beats a charge cue.
# PRECEDENCE (r3): a payment, balance, adjustment, copay or insurance word in the sentence beats every charge cue, in English and Spanish, because a
# statement of account lists payments and balances beside charges and a balance restates charges (counting it counts them twice).
CHARGE_CUE_ES = re.compile(r"\b(?:cargos?|honorarios)\b", re.IGNORECASE)
# 'estado de cuenta' names the document, never a charge. It counts only as statement context for a billed-service noun (consultas), never alone.
STATEMENT_CONTEXT_ES = re.compile(r"\bestado\s+de\s+cuenta\b", re.IGNORECASE)
_SERVICE_LINE_ES = re.compile(r"\bconsultas\b", re.IGNORECASE)
_NO_CHARGE_ES = re.compile(r"\bsin\s+(?:cargo|costo|cobro)s?\b|\bno\s+(?:se\s+)?(?:cobr[o\u00f3a]|factur\w*)\b|\bgratis\b|\bgratuit[oa]\b", re.IGNORECASE)
BALANCE_CUE = re.compile(
    r"\b(?:saldos?|balances?|pendientes?|adeudos?|"                                    # balance
    r"pagos?|pag[o\u00f3]|pagad[oa]s?|abonos?|copagos?|payments?|paid|copays?|"         # payment
    r"ajustes?|adjust(?:ment|ments|ed)?|cr[e\u00e9]ditos?|descuentos?|deducibles?|seguro|insurance|insurer|"   # adjustment / insurance
    r"contractual|write-?offs?)\b", re.IGNORECASE)


def charge_cue_es(text: str):
    """The Spanish charged-amount phrase in `text` (cargo, cargos, honorarios, or a statement-context 'consultas' line), or None. A payment, balance,
    adjustment, copay or insurance word (BALANCE_CUE) or a negation ('sin cargo', 'no facturado') in the same text returns None, whatever else it says."""
    t = text or ""
    if _NO_CHARGE_ES.search(t) or BALANCE_CUE.search(t):
        return None
    m = CHARGE_CUE_ES.search(t)
    if m:
        return m.group(0)
    ctx, svc = STATEMENT_CONTEXT_ES.search(t), _SERVICE_LINE_ES.search(t)
    return f"{ctx.group(0)}: {svc.group(0)}" if ctx and svc else None


_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)


def to_cents(figure: str):
    """'6,240' -> 624000, '95.5' -> 9550; None when the figure is not a clean number. Integer arithmetic only."""
    m = _VALID.match(figure)
    if not m:
        return None
    whole = figure.split(".")[0].replace(",", "")
    return int(whole) * 100 + int((m.group(1) or "").ljust(2, "0") or 0)


def find_amounts(excerpt: str) -> list:
    """[{raw, cents, start, end}] for every '$' figure, in text order. Doses, speeds, scores and day counts have no '$' and are never found."""
    out = []
    spans = [(h["start"], h["end"]) for h in injection.scan(excerpt or "")]
    for m in _AMT.finditer(excerpt or ""):
        figure = m.group(1)
        if not any(c.isdigit() for c in figure):
            continue
        injected = any(s <= m.start() and m.end() <= e for s, e in spans)   # a figure inside instruction-like text has no trusted value (D-005)
        out.append({"raw": m.group(0), "cents": None if injected else to_cents(figure), "start": m.start(), "end": m.end()})
    return out


def _label(excerpt: str, start: int) -> str:
    before = _BOUNDARY.split(excerpt[:start])[-1]
    clauses = [c for c in re.split(r"[,;]", before) if c.strip()]   # the amount's own clause: cues in a neighbouring clause do not count
    return " ".join((clauses[-1] if clauses else "").split()[-6:])


# T-140 / D-059: an amount that is a total, balance, payment, adjustment, credit, running figure, carried-forward figure, negative figure or an insurer's
# restatement is never a charge, so it never reaches the letter total. The word must be the amount's LABEL (the words just before the figure in its
# clause, the text just after it, the first cell of its table row, or its table column heading), not a word inside a service description:
# "Chiropractic adjustment charge $65", "Total body MRI charge" and "Balance training charge" are charges.
_KW = r"(?<![\w$])(?P<kw>%s)(?![\w])"
_NC_KINDS = (
    # (kind, words, trailing words allowed after the keyword, service-name guard applies, reason)
    ("total", r"sub[\s-]?totals?|grand\s+totals?|totals?|tot\.?", 4, True, "Total or subtotal line: it repeats the charges listed with it, so it is not totaled."),
    ("previous", r"(?:previous|prior|last|earlier)\s+(?:statements?|balance|bal\.?|bill|charges?|billed|amount)|carried\s+over|balance\s+(?:forward|fwd|brought|carried|from\s+(?:previous|prior))|"
                 r"bal\.?\s*(?:fwd|forward)|(?:brought|carried)\s+forward|carry[\s-]?(?:over|forward)|forwarded|previously\s+(?:billed|charged)|unpaid\s+prior", 4, False,
     "Previous statement or balance carried forward: charges already listed on an earlier statement, not a new charge."),
    ("balance", r"balances?|bal\.?|amount\s+(?:due|owed|owing)|amt\.?\s+due|(?:payment|now|total|balance|past)\s+due|due\s+now|owed|owing|outstanding|remaining|unpaid|"
                r"patient\s+resp(?:onsibility)?|pt\.?\s+resp\.?|(?:right\s+)?to\s+be\s+paid", 5, True, "Balance or amount due: worked out from charges, payments and adjustments, not a charge."),
    ("payment", r"paid|pd|payments?|pmts?|pymts?|co-?pay(?:ment)?s?|deposit", 5, False, "Payment: money received, not a charge."),
    ("reversal", r"reversal|reversed|void(?:ed)?|refund(?:ed)?|recoup\w*|remit(?:tance)?|(?:ins(?:urance)?\.?|payment|credit|med\s?pay|pip)\s+applied|med\s?pay|pip|written\s+off", 5, False,
     "Reversal, refund, void, recoupment or payment applied: money taken off the account, not a charge."),
    ("adjustment", r"adj\.?|adjust(?:ment|ments|ed)?|write[\s-]?offs?|w\s?/\s?o|credits?|discount\w*|contractual|courtesy", 5, True,
     "Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges."),
    ("running", r"year[\s-]*to[\s-]*date|ytd|cumulative|accumulated|running(?:\s+(?:balance|charges?))?|to[\s-]*date|aggregate|combined|all\s+charges|sum\s+of(?:\s+charges)?", 4, False,
     "Year-to-date or running figure: it adds up charges listed elsewhere, so it is not totaled."),
    ("statement", r"statement\s+(?:charges?|of\s+charges)|summary\s+of\s+charges|new\s+charges|(?:this|current)\s+statement|statement\s+amount|amount\s+of\s+(?:this\s+)?statement|billed\s+this\s+statement|period\s+charges", 3, False,
     "Statement-level figure: it adds up the charges listed on this statement, so it is not totaled."))
_NC_RX = [(k, re.compile((_KW % w) + r"(?:\s+[^\s$]+){0,%d}[\s:=(\-)|]*$" % n, re.IGNORECASE), guard, why) for k, w, n, guard, why in _NC_KINDS]
_CHARGE_NOUN = r"(?:charges?|charged|billed|fees?|cost)"
_CONT = frozenset("of for the this that statement account ledger amount billed all services service current new to date patient and".split())
_SERVICE_PRE = re.compile(r"\b(?:chiropractic|spinal|cervical|lumbar|thoracic|manipulative|osteopathic|joint|cmt)\s*$", re.IGNORECASE)
_SERVICE_TOTAL = re.compile(r"^\s+(?:body|knee|hip|shoulder|spine|joint|disc|ankle|wrist|elbow|er|emergency|hospital|abdominal|cervical|lumbar)\b", re.IGNORECASE)
_SERVICE_LINE = re.compile(r"\b(?:chiropractic|spinal|cervical|lumbar|thoracic)\s+adjustments?\s*$", re.IGNORECASE)
_UB_LINE = re.compile(r"\bFL\s?-?47\b", re.IGNORECASE)
_UB_TOTAL = re.compile(r"\brev(?:enue)?\s+(?:code\s+)?0001\b", re.IGNORECASE)      # UB-04 revenue code 0001 is the claim's total line
_CELL_SPLIT = re.compile(r"\t|\|| {2,}")
_CHARGE_COL = re.compile(r"^(?:charges?|billed(?:\s+charges?)?|amount\s+billed|billed\s+amount|charge\s+amount|fees?|amount|amt|price)$", re.IGNORECASE)
_RUN_SEP = re.compile(r"^[\s|/\\\-]*$")
# what stands AFTER a figure and names it: "$300.00 paid", "$2,740.00 total", "$2,166.00 balance due" (the words must end the clause)
_AFTER_KINDS = (
    ("total", r"(?:in\s+)?totals?|tot\.?", r""),
    ("balance", r"balance|due|owed|outstanding|remaining|unpaid|owing", r"(?:\s+(?:due|owed|remaining|outstanding|now))?"),
    ("payment", r"paid|received|payment", r"(?:\s+(?:on|by|from|to)\s+[\w/.-]+(?:\s+[\w/.-]+)?)?"),
    ("adjustment", r"adjustments?|credits?|write[\s-]?offs?|discounts?|adjusted|waived", r""),
    ("reversal", r"reversed|refunded|voided|applied|written\s+off", r""),
    # T-140 r3: running and carried-forward words AFTER the figure ("Charges $730.00 YTD", "$500.00 carried over", "$650.00 (all statements)")
    ("running", r"year[\s-]*to[\s-]*date|ytd|to[\s-]*date|in\s+all|combined|cumulative|so\s+far|(?:for\s+)?all\s+statements|(?:the\s+)?sum\s+of\s+the\s+above|since\s+[\w/.-]+(?:\s+[\w/.-]+)?", r""),
    ("previous", r"carried\s+(?:over|forward)|brought\s+forward|from\s+(?:the\s+)?(?:previous|prior|last|earlier)\s+statements?|previously\s+billed|last\s+statement|prior\s+period", r""))
_AFTER_RX = [(k, re.compile(r"^\s*\(?\s*(?:(?:was|is|were)\s+)?(?:%s)%s\s*\)?\s*(?:[.,;:)\]]|\n|$)" % (w, t), re.IGNORECASE)) for k, w, t in _AFTER_KINDS]
_WHY_OF = {k: why for k, _, _, _, why in _NC_KINDS}
_INSURER_SRC = re.compile(r"\b(?:EOB|explanation\s+of\s+benefits|remittance(?:\s+advice)?|ERA|payer|insurer|insurance|carrier|health\s+plan|mutual|casualty|indemnity|assurance|"
                          r"underwriters?|medicare|medicaid|tricare|blue\s+cross|claims?\s+(?:summary|history|payment|statement|detail)|"
                          r"med\s?pay|PIP|personal\s+injury\s+protection|benefits?\s+administrators?|TPA|third[\s-]party\s+administrators?)\b", re.IGNORECASE)
# the text arm: the excerpt opens as the insurer's own document, or states plan-side columns (T-140 r3). A provider bill that merely mentions an EOB is not one.
_INSURER_TXT = re.compile(r"^\W*.{0,40}?\b(?:EOB|explanation\s+of\s+benefits|remittance\s+advice)\b|\b(?:network\s+discount|plan\s+paid|allowed\s+amount|member\s+responsibility)\b", re.IGNORECASE | re.DOTALL)
_INSURER_WHY = "Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge."
_NEG_WHY = "Negative amount or credit (minus sign, parentheses or CR): money taken off the account, not a charge."
_ZERO_WHY = "Zero amount: nothing to total."


def _service_name(t: str, m, kind: str) -> bool:
    """True when the matched keyword sits inside a service description ('Chiropractic adjustment charge', 'Total body MRI charge', 'Balance training
    charge', 'Total of 12 visits billed'): a charge word follows after words that are not plain label words, or a service word touches the keyword."""
    if _SERVICE_PRE.search(t[:m.start('kw')]):
        return True
    after = t[m.end('kw'):]
    if kind == "total" and _SERVICE_TOTAL.match(after):
        return True
    n = re.match(r"((?:\s+\(?[^\s$:;]+\)?)*?)\s+%s\b" % _CHARGE_NOUN, after, re.IGNORECASE)
    return bool(n) and any(w.strip("()").lower() not in _CONT for w in n.group(1).split())


def label_reason(label: str):
    """(kind, reason) when the label text ends in a total, balance, payment, adjustment, running or carried-forward word, else None. A word earlier in
    the sentence than the last few label words, or inside a service name, does not count ('Total of 12 visits billed $2,150' labels a charge)."""
    t = (label or "").strip()
    if not t:
        return None
    if _UB_TOTAL.search(t):
        return _NC_KINDS[0][0], _NC_KINDS[0][4]
    for k, rx, guard, why in _NC_RX:
        if k == "total" and _UB_LINE.search(t):     # UB-04 field 47 is the 'Total Charges' COLUMN: each revenue-code line carries one, so the words name a column, not a total line
            continue
        m = rx.search(t)
        if m and not (guard and _service_name(t, m, k)):
            return k, why
    return None


def _label(excerpt: str, start: int) -> str:
    before = _BOUNDARY.split(excerpt[:start])[-1]
    clauses = [c for c in re.split(r"[,;]", before) if c.strip()]   # the amount's own clause: cues in a neighbouring clause do not count
    return " ".join((clauses[-1] if clauses else "").rstrip("\u00b7 \t").split()[-6:])          # a masked dotted leader between the label and the figure is not part of the label (T-202 r5)


def _column_label(excerpt: str, start: int) -> str:
    """Table heading above the figure: the nearest line above, up to a blank line, with no digits and the same number of cells as the figure's line
    (cells split at a tab, a bar or two or more spaces); data rows in between are skipped. '' when the text is not laid out as columns."""
    ls = excerpt.rfind("\n", 0, start) + 1
    le = excerpt.find("\n", start)
    row = excerpt[ls:len(excerpt) if le < 0 else le]
    cells = [(m.start(), m.end()) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", row)]
    idx = next((i for i, (a, b) in enumerate(cells) if a <= start - ls < b), None)
    if idx is None or len(cells) < 2:
        return ""
    for line in reversed(excerpt[:max(ls - 1, 0)].split("\n")[-40:]):
        if not line.strip():
            return ""
        if re.search(r"\d", line):
            continue
        heads = [h.strip() for h in _CELL_SPLIT.split(line) if h.strip()]
        return heads[idx] if len(heads) == len(cells) else ""
    return ""


def _run_label(excerpt: str, amounts: list, i: int):
    """(kind, reason) when figure i sits in a row of figures (only spaces, bars, slashes or dashes between them) whose label is a total, balance,
    payment... ('Total  $380  $77  $305'): every figure of that row takes the row's label."""
    lo = hi = i
    while lo > 0 and _RUN_SEP.match(excerpt[amounts[lo - 1]["end"]:amounts[lo]["start"]]):
        lo -= 1
    while hi + 1 < len(amounts) and _RUN_SEP.match(excerpt[amounts[hi]["end"]:amounts[hi + 1]["start"]]):
        hi += 1
    return label_reason(_label(excerpt, amounts[lo]["start"])) if hi > lo else None


def _sign_reason(excerpt: str, amount: dict):
    s, e = amount["start"], amount["end"]
    pre, post = excerpt[max(0, s - 3):s], excerpt[e:e + 14]
    neg = re.search(r"(?:^|[\s(:=|])[-−–]\s?$", pre) or re.search(r"\(\s?$", pre) and re.match(r"\s?\)", post) or re.match(r"-(?![\w$\d])", post)
    cr = re.match(r"\s?(?:CR\b|\(\s?(?:credit|CR)\s?\))", post, re.IGNORECASE)
    return ("credit", _NEG_WHY) if neg or cr else None


def _after_reason(excerpt: str, end: int):
    tail = excerpt[end:end + 70]
    return next(((k, _WHY_OF[k]) for k, rx in _AFTER_RX if rx.match(tail)), None)


_BILLED_COL = re.compile(r"\b(?:billed|charges?|charged|submitted)\b", re.IGNORECASE)
# a column only a payer fills in. 'Paid' and 'Payments' alone are NOT here: a provider's own ledger has a Payments column (D-062, adjuster r3 blocker 3)
_PAYER_COL = re.compile(r"\b(?:approved|allowed|covered|benefits?|eligible|plan\s+(?:paid|payment|pays?)|payer\s+paid|insurance\s+paid|ins\.?\s+paid|member\s+resp\w*|"
                        r"network|co-?insurance|deductible|payable)\b", re.IGNORECASE)


def _insurer_table(excerpt: str) -> bool:
    """D-062: a table whose heading line (no digits) has a billed/charges column beside a payer column (approved, allowed, covered, benefit, plan paid ...) is the
    payer's restatement of the provider's bill, whatever the document is called. A provider ledger's Payments / Adjustments / Balance columns are not payer columns."""
    return any(not re.search(r"\d", ln) and _BILLED_COL.search(ln) and _PAYER_COL.search(ln) for ln in (excerpt or "").split("\n"))


def is_insurer_document(source: str, excerpt: str) -> bool:
    return bool(_INSURER_SRC.search(source or "") or _INSURER_TXT.search(excerpt or "") or _insurer_table(excerpt))


@_masked
def non_charge_reason(excerpt: str, amount: dict, source: str = None):
    """(kind, reason) when code says this figure is not a charge (D-059): a negative sign, parentheses or CR; a zero; a total, balance, payment,
    adjustment, reversal, year-to-date, previous-statement or balance-forward LABEL (before the figure, after it, the row's first cell or the column
    heading); or an insurer document (EOB, remittance) restating the provider's bill. None for an ordinary figure."""
    amts = find_amounts(excerpt)
    i = next((n for n, a in enumerate(amts) if a["start"] == amount["start"]), None)
    found = (label_reason(_label(excerpt, amount["start"])) or label_reason(_column_label(excerpt, amount["start"]))
             or (i is not None and _run_label(excerpt, amts, i)) or _after_reason(excerpt, amount["end"]) or _sign_reason(excerpt, amount))
    if found:
        return found
    if amount.get("cents") == 0:
        return "zero", _ZERO_WHY
    return ("insurer", _INSURER_WHY) if is_insurer_document(source, excerpt) else None


def _non_charge(excerpt: str, amount: dict, source: str = None):
    return non_charge_reason(excerpt, amount, source)


# ---------------------------------------------------------------- D-060: charge candidates are default-deny
# An amount is a charge only when it sits on an itemized service line: a date of service, a service description (service noun, CPT, HCPCS or revenue code)
# and the amount on the same line or table row of a provider bill or ledger. In a dated encounter record (an ED note, an imaging report) the record's own date is
# the date of service and the sentence must say charge/billed beside a service (or a bare "Charge:" under a header that names the service). Everything else is
# `unclear` with its reason. Nothing here lists wording that is NOT a charge: wording that merely looks like a total cannot be outworded.
_MON = r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?"
_DOS_RX = re.compile(
    r"(?<![\w/.$-])(?:(?P<iy>\d{4})-(?P<im>\d{1,2})-(?P<id>\d{1,2})"
    r"|(?P<a>\d{1,2})[/.-](?P<b>\d{1,2})[/.-](?P<y>\d{4}|\d{2})"
    rf"|(?P<mon>{_MON})\.?\s+(?P<d2>\d{{1,2}})(?:st|nd|rd|th)?(?:,?\s+(?P<y2>\d{{4}}))?"
    rf"|(?P<d3>\d{{1,2}})(?:st|nd|rd|th)?[\s-]+(?:of\s+)?(?P<mon3>{_MON})\.?[\s-]*,?\s*(?P<y3>\d{{4}})"
    r"|(?P<a4>\d{1,2})/(?P<b4>\d{1,2}))(?![\w/]|\.\d)", re.IGNORECASE)
# a date that follows one of these words is a statement, billing, due or period date, never a date of service
_BAD_LEAD = re.compile(r"\b(?:statement|stmt|invoice|billing|billed|printed|issued|as\s+of|through|thru|until|ending|due|from|to|since|period|posted|paid|received|payment|balance)\b"
                       r"(?:\s+(?:date|dated|on))?\s*[:#]?\s*$", re.IGNORECASE)
_RANGE_JOIN = re.compile(r"^\s*(?:-|–|—|to|through|thru|until)\s*$", re.IGNORECASE)
_TAIL_LEAD = re.compile(r"^\s*[(,:–—-]?\s*(?:for|on|of|dos|date\s+of\s+service|service\s+date|dated|visit|service)\b|^\s*\(", re.IGNORECASE)
_DATE_LEAD = re.compile(r"(?:\bdos|date\s+of\s+service|service\s+date|dated?|\bon|\bfor|\bof|\bvisit|\()\s*[:#]?\s*$", re.IGNORECASE)
_SVC = re.compile(r"\b(?:office\s+visits?|visits?|exams?|examination|evals?|evaluations?|consult\w*|therap\w+|exercises?|treatments?|procedures?|injections?|surger\w+|mri|ct|"
                  r"cat\s+scan|x-?\s?rays?|radiograph\w*|ultrasound|imaging|radiolog\w+|labs?|laborator\w+|pharmacy|medications?|supplies|er|ed|emergency|room\s+and\s+board|"
                  r"ambulance|transport\w*|mileage|anesthesi\w+|cmt|chiropractic|manipulat\w+|modalit\w+|traction|stimulation|splint|brace|dme|nerve\s+block|epidural|biopsy|"
                  r"dressing|cast|admission|observation|inpatient|outpatient|follow[\s-]?up|assessment|screening|testing|session|urgent\s+care|care|train\w*|replacement|arthroplasty|repair|fusion|discectomy|"
                  r"laminectomy|fixation|reduction|suturing|sutures?|wound|closure|removal|infusion|dialysis|radiation|oxygen|nursing|icu|recovery|implant|hardware|orthotic|prosthe\w+|rehab\w*|"
                  r"massage|acupuncture|counsel\w*|ekg|ecg|emg|ncs|nerve\s+conduction|doppler|echo\w*|pathology|cultures?|blood|panel|urinalysis|vaccine|immuni[sz]\w+|occupational|speech)\b", re.IGNORECASE)
_PROVIDER_KIND = re.compile(r"\b(?:clinic|hospital|center|centre|medical|physicians?|practice|surgery|orthop\w+|neuro\w+|spine)\b", re.IGNORECASE)
_MOD = r"(?:-[A-Z0-9]{2})?"                # a CPT/HCPCS modifier ('97140-GP', 'CPT 97140-59')
_CODE_RX = re.compile(rf"\brev(?:enue)?\.?\s*(?:code\s*)?#?\s*0\d{{3}}\b|\b(?-i:[A-V]\d{{4}}){_MOD}(?![\w-])|\bCPT\s*[#:]?\s*\d{{5}}{_MOD}(?![\w-])|(?<![\w$#.,/-])\d{{5}}{_MOD}(?![\w.,/-])", re.IGNORECASE)


def norm_code(raw: str) -> str:
    """D-062: the bare code of a CPT, HCPCS or revenue code as written: label (CPT, HCPCS, Rev, Revenue code), '#', ':', spaces and a modifier removed, upper case.
    'CPT 97140-59', 'cpt#97140', '97140-GP' and '97140' are all '97140'; 'HCPCS: G0283' is 'G0283'; 'Rev. code #0450' is '0450'."""
    t = re.sub(r"[\s.#:]+", "", raw or "").upper()
    t = re.sub(r"^(?:CPT|HCPCS|REVENUE|REV|CODE)+", "", t)
    m = re.match(r"(\d{5}|[A-V]\d{4}|0\d{3})(?:-[A-Z0-9]{2})?$", t)
    return m.group(1) if m else t
_PERIOD_PHRASE = re.compile(r"(?:statement\s+period|billing\s+period|service\s+period|dates?\s+of\s+service|\bDOS\b|services?\s+(?:provided|rendered)|\brun\s+of|date\s+of\s+(?:the\s+)?run)\W{0,6}$", re.IGNORECASE)
_ADMIN_SRC = re.compile(r"\b(?:phone|telephone|tel\.?)\s+(?:note|call|encounter|message|contact)\b|\bportal\s+message\b|\bvoicemail\b|\bmessage\s+(?:note|log)\b|"
                        r"\b(?:records?\s+request|request\s+for\s+records|medical\s+records\s+(?:request|certification|affidavit)|business\s+records\s+affidavit|custodian\s+(?:of\s+records\s+)?affidavit|"
                        r"18\.001\s+affidavit|affidavit|authorization\s+form|HIPAA\s+authorization|correspondence|cover\s+letter|fax\s+cover|referral\s+(?:form|letter)|prior\s+authori[sz]ation|"
                        r"no-?\s?show\s+(?:notice|letter)|demand\s+letter)\b", re.IGNORECASE)
_BILLISH = re.compile(r"\b(?:statements?|bills?|billing|invoices?|ledgers?|account|itemi[sz]ed|ub-?04|hcfa|cms-?1500|claim\s+form)\b", re.IGNORECASE)
_BILL_OPEN = re.compile(r"^\W{0,3}(?:patient\s+)?(?:itemi[sz]ed|statement|invoice|ledger|billing|account\s+statement)\b", re.IGNORECASE)
_TOKEN_FILLER = frozenset("charge charges charged billed fee fees of on for the a an at to and unit units dos date service services statement rev cpt code invoiced total".split())
_NO_DATE_WHY = "The line states no date of service, so it is not an itemized service line and is not totaled."
NO_DATE_WHY = _NO_DATE_WHY           # T-200: the stored reason of a charge the paralegal counted because its line states no date of service
_NO_SVC_WHY = "The line names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized service line and is not totaled."
_NO_COL_WHY = "The figure is not under a charges column of the bill, so it is not an itemized service line and is not totaled."
_SECOND_WHY = ("A second amount on a service line is not the line's own charge (it can be a deductible, what the patient owes, a denied or paid amount, an adjustment, "
               "a balance or an unlabeled figure), so it is not totaled.")
_ADMIN_WHY = "A letter, request or note is not a provider bill, so its figures are not totaled."
_NOT_BILL_WHY = "This record is not a bill (it is a clinical note or summary) and the case holds a bill from the same provider, so charges are taken from the bill only and this amount is not totaled."
_UNKNOWN_WHY = "The record's document type is unknown (its header names no provider or kind), so it is not read as a bill and this amount is not totaled."


_GENERIC_WORDS = frozenset("""dr doctor md do dc dpt pt the and of at for in a an ed er emergency department hospital clinic center centre medical regional general community memorial
physical therapy imaging radiology urgent care health services chiropractic orthopedics orthopaedic pain management family practice institute group associates billing statement
ledger itemized itemised bill invoice account discharge summary note notes visit report records record patient new follow up initial evaluation treatment ems ambulance fire rescue
surgery surgical specialists specialist""".split())


def _provider_tokens(source) -> frozenset:
    """The distinctive words of the provider named in a record's header label (the words before the first comma, without generic words such as clinic, hospital,
    therapy, discharge summary): 'Brindlewood Physical Therapy, billing statement' and 'Brindlewood Physical Therapy, discharge summary' both give {'brindlewood'}."""
    return frozenset(w for w in re.findall(r"[a-z]+", (source or "").split(",")[0].casefold()) if len(w) > 2 and w not in _GENERIC_WORDS)


def _bill_yields_a_charge(r: dict) -> bool:
    """True when the bill record has at least one figure that is an itemized charge: only then does a note's charge sentence restate something the case already counts.
    A bill whose figures are all unreadable or unclear (OCR noise, no dates of service) restates nothing."""
    ex = r.get("excerpt") or ""
    return any(classify(ex, a, injection=bool(r.get("injection_tag")), source=r.get("source"), date_iso=r.get("date_iso")) == "charge" for a in find_amounts(ex))


def note_charge_block(records: list, rec: dict):
    """D-062: why a charge stated in this record may not be read as one, or None. Charges come from documents with a billing header (itemized statement, ledger,
    invoice, UB-04, CMS-1500). A record with no header at all is an unknown document and never yields one. A clinical note or discharge summary that states a charge
    restates the course of care and the provider's own bill, so it yields none once the case holds a bill from the SAME provider (a shared distinctive word in the header
    label; a note with no distinctive word is held against any bill) and that bill has at least one itemized charge of its own. A note with no bill from its provider in the case (the Appendix A sample has no bill at all) has
    only itself to read a stated charge from, so it is read under the encounter rule. Insurer documents never yield a charge (non_charge_reason). `records=None`: no
    case context, no block."""
    if records is None or billing_document(rec.get("source"), rec.get("excerpt")):
        return None
    if not (rec.get("source") or "").strip():
        return _UNKNOWN_WHY
    mine = _provider_tokens(rec.get("source"))
    for r in records:
        if r.get("duplicate_of") or not billing_document(r.get("source"), r.get("excerpt")) or is_insurer_document(r.get("source"), r.get("excerpt")):
            continue
        if (not mine or mine & _provider_tokens(r.get("source"))) and _bill_yields_a_charge(r):
            return _NOT_BILL_WHY
    return None




def _year_for(mo: int, d: int, ref_iso):
    if not ref_iso:
        return None
    y = int(ref_iso[:4])
    iso = _iso_or_none(y, mo, d)
    return _iso_or_none(y - 1, mo, d) if iso and iso > ref_iso else iso


def _iso_or_none(y, mo, d):
    import datetime
    try:
        return datetime.date(y, mo, d).isoformat()
    except ValueError:
        return None


def _dos_iso(m, ref_iso):
    """ISO date of one _DOS_RX match: month/day numerals read month first (US) unless the first number is over 12; a year-less date takes the year of the
    record's date (the latest such date not after it); None when the match is not a real calendar date."""
    g = m.groupdict()
    if g["iy"]:
        return _iso_or_none(int(g["iy"]), int(g["im"]), int(g["id"]))
    if g["a"]:
        a, b, y = int(g["a"]), int(g["b"]), int(g["y"])
        y = y if len(g["y"]) == 4 else (2000 + y if y <= _dates.PIVOT_YY else 1900 + y)
        return _iso_or_none(y, b, a) if a > 12 >= b else _iso_or_none(y, a, b)
    if g["mon"]:
        mo = _dates.MONTHS[g["mon"].lower()[:3]]
        return _iso_or_none(int(g["y2"]), mo, int(g["d2"])) if g["y2"] else _year_for(mo, int(g["d2"]), ref_iso)
    if g["mon3"]:
        return _iso_or_none(int(g["y3"]), _dates.MONTHS[g["mon3"].lower()[:3]], int(g["d3"]))
    return _year_for(int(g["a4"]), int(g["b4"]), ref_iso)


def _dates_in(text: str, ref_iso, tail: bool = False) -> list:
    """[(start, end, iso)] of the dates of service stated in `text`: real calendar dates, not led by a statement, billing, due, as-of or period word, and not an
    end of a range (a range is a period, not a date of service). `tail=True`: text after the figure, where only a date led by DOS / on / for / of counts."""
    found = []
    for m in _DOS_RX.finditer(text):
        iso = _dos_iso(m, ref_iso)
        if iso:
            found.append((m.start(), m.end(), iso))
    bad = set()
    for k, (s, e, _) in enumerate(found):
        lead = text[max(0, s - 30):s]
        if _BAD_LEAD.search(lead) or (tail and not _DATE_LEAD.search(lead)):
            bad.add(k)
        if k + 1 < len(found) and _RANGE_JOIN.match(text[e:found[k + 1][0]]):
            bad.update((k, k + 1))
    return [f for k, f in enumerate(found) if k not in bad]


def _segments(excerpt: str) -> list:
    out, pos = [], 0
    for m in _BOUNDARY.finditer(excerpt):
        out.append((pos, m.start()))
        pos = m.end()
    out.append((pos, len(excerpt)))
    return [(s, e) for s, e in out if e > s]


def _cells(line: str) -> list:
    return [m.group(0) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]


def billing_document(source, excerpt: str = "") -> bool:
    """A provider bill or ledger: the source label names one (lexicon billing_document, or a statement / bill / invoice / ledger / account word), or the
    excerpt opens as one ("Itemized statement: ...")."""
    return bool(_is_billing_source(source or "") or _BILLISH.search(source or "") or _BILL_OPEN.search(excerpt or ""))


def _record_period(before: str, ref_iso):
    """(first date, last date or None) of the date or period the record states for its services. D-071: the last date is the end of the range ('06/09/2026 to 06/12/2026'),
    None for a single date ('the run of 09/14/2026')."""
    ms = list(_DOS_RX.finditer(before))
    for k, m in enumerate(ms):
        iso = _dos_iso(m, ref_iso)
        if iso and _PERIOD_PHRASE.search(before[max(0, m.start() - 40):m.start()]):
            end = None
            if k + 1 < len(ms) and _RANGE_JOIN.match(before[m.end():ms[k + 1].start()]):
                end = _dos_iso(ms[k + 1], ref_iso)
            return iso, (end if end and end > iso else None)
    return None, None


def _record_period_dos(before: str, ref_iso):
    """A coded line (CPT, HCPCS, revenue code) with no date of its own takes the date or period the record states for its services ('statement period
    06/09/2026 to 06/12/2026', 'the run of 09/14/2026'): the first date of that period."""
    return _record_period(before, ref_iso)[0]


def _tokens(text: str, strip) -> tuple:
    """(word stems, codes) of a service description: dates, figures and charge words removed, words cut to four letters ('therapeutic' and 'ther' meet)."""
    for s, e in sorted(strip, reverse=True):
        text = text[:s] + " " + text[e:]
    codes = frozenset(norm_code(m.group(0)) for m in _CODE_RX.finditer(text))
    text = _CODE_RX.sub(" ", text)
    words = [w for w in re.findall(r"[a-z]+", text.casefold()) if w not in _TOKEN_FILLER and len(w) > 1]
    return frozenset(w[:4] for w in words[-6:]), codes


def _could_be_own_charge(excerpt: str, amount: dict, source: str = None) -> bool:
    """False for a figure that is a unit rate or carries a non-charge label (total, balance, payment, negative ...): it cannot be 'the line's own charge', so it does not make a
    later figure of the same line a second amount."""
    if amount.get("cents") is None:
        return False
    return not (_RATE_WORD.search(_label(excerpt, amount["start"])) or _RATE_AFTER.match(excerpt[amount["end"]:amount["end"] + 30]) or non_charge_reason(excerpt, amount, source))


@_masked
def charge_basis(excerpt: str, amount: dict, source: str = None, date_iso: str = None, note_block: str = None) -> dict:
    """D-060: {ok, reason, dos, tokens, codes} for one figure. `ok` is True only on an itemized service line (see the block comment above). `reason` is the plain
    sentence for the internal notes when it is not (None when the figure just has no charge wording). `dos` (ISO date, or the record's date for a note),
    `tokens` and `codes` describe the service and feed the duplicate match, whether or not `ok`. `note_block` (note_charge_block) is the reason a clinical note or
    unknown document yields no charge; it only applies to the encounter-record branch."""
    out = {"ok": False, "reason": None, "dos": None, "dos_end": None, "tokens": frozenset(), "codes": frozenset(), "svc": False}
    amts = find_amounts(excerpt or "")
    i = next((n for n, a in enumerate(amts) if a["start"] == amount["start"]), None)
    if i is None or amount.get("cents") is None:
        return out
    a = amts[i]
    segs = _segments(excerpt)
    ss, se = next(((s, e) for s, e in segs if s <= a["start"] < e), (0, len(excerpt)))
    sfigs = [j for j, x in enumerate(amts) if ss <= x["start"] < se]
    segtext = excerpt[ss:se]
    row = len(_cells(segtext)) >= 2
    strip_figs = [(x["start"] - ss, x["end"] - ss) for x in amts if ss <= x["start"] < se]
    if row:
        text, tail_text = segtext, ""
        ds = _dates_in(segtext, date_iso)
        dos = ds[0][2] if ds else None
        strip = strip_figs + [(s, e) for s, e, _ in ds]
    else:
        prev_end = ss                  # the whole sentence before the figure: a coded line's code or service name may stand before an earlier figure of the same line
        nxt = next((amts[j]["start"] for j in sfigs if j > i), se)
        before, tail_text = excerpt[prev_end:a["start"]], excerpt[a["end"]:nxt]
        ds = _dates_in(before, date_iso)
        dos = ds[-1][2] if ds else None
        strip = [(s, e) for s, e, _ in ds]
        if _TAIL_LEAD.match(tail_text) and not ds:
            td = _dates_in(tail_text, date_iso, tail=True)
            dos = td[0][2] if td else None
        text = before + (tail_text if _TAIL_LEAD.match(tail_text) else "")
        strip = strip + ([(len(before) + s, len(before) + e) for s, e, _ in _dates_in(tail_text, date_iso, tail=True)] if _TAIL_LEAD.match(tail_text) else [])
    text_nodate = text
    for s, e in sorted(strip, reverse=True):
        text_nodate = text_nodate[:s] + " " + text_nodate[e:]
    out["tokens"], out["codes"] = _tokens(text, strip)
    coded = bool(out["codes"])
    out["svc"] = bool(_SVC.search(text_nodate) or coded)          # D-064 r2: a service description (service noun, CPT / HCPCS / revenue code) stands in the line
    if billing_document(source, excerpt):
        if row:
            head = _column_label(excerpt, a["start"])
            if head and not _CHARGE_COL.match(head):
                out.update(reason=_NO_COL_WHY, dos=dos)
                return out
            if not head and len(sfigs) > 1 and sfigs[0] != i:
                out.update(reason=_NO_COL_WHY, dos=dos)
                return out
            # D-062 (staff r3): per figure, not per line. Under a charges-like heading, only the first such figure of the row is the line's own charge.
            if head and any(_CHARGE_COL.match(_column_label(excerpt, amts[j]["start"])) for j in sfigs if j < i):
                out.update(reason=_SECOND_WHY, dos=dos)
                return out
        else:
            earlier = [j for j in sfigs if j < i and _could_be_own_charge(excerpt, amts[j], source)]      # a rate or a labeled total before it ("FL44 rate $1,640.00 per day, ... FL47 total charges $4,920.00") is not the line's charge
            if earlier and not _dates_in(excerpt[amts[earlier[-1]]["end"]:a["start"]], date_iso):      # the line's own charge is its first figure; a later one needs a date of its own
                out.update(reason=_SECOND_WHY, dos=dos)
                return out
        if dos is None and coded:
            dos, out["dos_end"] = _record_period(excerpt[:se], date_iso)          # D-071: a period keeps its end date for the letter
        out["dos"] = dos
        if dos is None:
            out["reason"] = _NO_DATE_WHY
        elif not (_SVC.search(text_nodate) or coded):
            out["reason"] = _NO_SVC_WHY
        else:
            out["ok"] = True
        return out
    # a dated encounter record: the record's date is the date of service
    out["dos"] = dos or date_iso
    if _ADMIN_SRC.search(source or ""):
        out["reason"] = _ADMIN_WHY
        return out
    label = _label(excerpt, a["start"])
    out["svc"] = bool(_SVC.search(label) or _CODE_RX.search(label))
    if not _CHARGE_END.search(label):
        return out
    if note_block:
        out["reason"] = note_block
        return out
    if _SVC.search(label) or _CODE_RX.search(label):
        out["ok"] = True
        return out
    bare = re.findall(r"[a-z]+", label.casefold()) in (["charge"], ["charges"])          # exactly the bare word, as in "Charge: $2,150."
    if bare and (re.fullmatch(r"[\s.;,:)\]]*", tail_text) or _TAIL_LEAD.match(tail_text)) and (_SVC.search(source or "") or _PROVIDER_KIND.search(source or "")):
        out["tokens"] = frozenset(m.group(0).casefold()[:4] for m in _SVC.finditer(source or ""))
        out["ok"] = True
    else:
        out["reason"] = _NO_SVC_WHY.replace("The line names", "The sentence names").replace("an itemized service line", "an itemized charge")
    return out


@_masked
def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None, date_iso: str = None, strict: bool = True, note_block: str = None) -> str:
    """charge | rate | estimate | damages | unclear. First match wins (ADR-011): injection, unreadable, rate, estimate, damages,
    D-059 code rule (negative, zero, total/balance/payment/adjustment/running/carried-forward label, insurer restatement: unclear, never a charge),
    then D-060 default-deny: a charge only on an itemized service line (`charge_basis`), else unclear. `source` is the record's header label and `date_iso`
    its date; with no source the figure is read as an encounter note. `strict=False` is the billing LISTING's reading (billing.py shows a provider's lines and never
    totals): the D-059 rules still apply, but a figure is a charge by its wording alone (charge label, statement wording, Charges column), as before D-060.
    Nothing that feeds the letter total calls it with strict=False."""
    if injection or amount.get("cents") is None:
        return "unclear"
    label = _label(excerpt, amount["start"])
    after = excerpt[amount["end"]:amount["end"] + 30]
    if _RATE_WORD.search(label) or _RATE_AFTER.match(after):
        return "rate"
    if _ESTIMATE.search(label):
        return "estimate"
    if any(e["regex"].search(label) for e in lexicon.code_list("damages")):
        return "damages"
    if non_charge_reason(excerpt, amount, source):
        return "unclear"
    if strict:
        return "charge" if charge_basis(excerpt, amount, source, date_iso, note_block)["ok"] else "unclear"
    billing = source is None or _is_billing_source(source)
    if _STATEMENT.search(label) and billing:
        return "charge"
    if _CHARGE_END.search(label):
        return "charge"
    if billing and (_CHARGE_COL.match(_column_label(excerpt, amount["start"])) or _SERVICE_LINE.search(label)):
        return "charge"
    return "unclear"


def _likely_totals(rows: list) -> set:
    """Indexes (into `rows`, dicts with cls, cents) of charges that equal the sum of the OTHER charges of the same record, when there are at least two
    others: a total printed without a total word, or a coincidence. The check runs on one record's figures, never across records. It only FLAGS (D-059)."""
    ch = [i for i, a in enumerate(rows) if a["cls"] == "charge" and a.get("cents") and not a.get("injection")]
    total = sum(rows[j]["cents"] for j in ch)
    return {i for i in ch if len(ch) >= 3 and total - rows[i]["cents"] == rows[i]["cents"]}


def _usd(cents: int) -> str:
    return f"${cents // 100:,}.{cents % 100:02d}"


CONFIRM_NAMES = {"likely_duplicate": "Likely duplicate", "likely_total": "Likely total"}


@_masked
def charge_line(excerpt: str, start: int) -> str:
    """T-159: the sentence or table row of `excerpt` that holds the figure at `start`, whitespace collapsed and cut at 140 characters. It names a charge to the paralegal
    by what the record says (service, amount, date) and never by an internal id."""
    seg = next((excerpt[s:e] for s, e in _segments(excerpt or "") if s <= start < e), "")
    line = " ".join(seg.split())
    return line if len(line) <= 140 else line[:139].rstrip() + "\u2026"


def confirm_info(flag: str, of: str = None, detail: str = "") -> dict:
    """The flag a charge carries until the paralegal confirms it by name (D-059). `confirm_with` is the exact word the accept call must send. `of` is the other charge's
    id for a client that wants to jump to it; `detail` (already plain words, starting with what the other charge is) is what the sentence says. T-159: no id in the words."""
    msg = {"likely_duplicate": f"This looks like the same charge as {detail}Counting both would count one service twice.",
           "likely_total": "This amount equals the sum of the other charges in its record, so it may be a total and not a separate charge (it can also be a coincidence). "
                           "Counting it may count the same charges twice."}[flag]
    return {"flag": flag, "name": CONFIRM_NAMES[flag], "message": msg, "confirm_with": flag, "of": of}


@_masked
def not_totaled_reason(excerpt: str, raw: str, cents, source: str = None, date_iso: str = None, pos: int = None, records: list = None):
    """Why a figure in `excerpt` is not a charge (plain words for the internal notes): the D-059 code rules, then the D-060 default-deny reason. None for an
    ordinary charge or a figure with no stated reason. `pos` = the figure's own offset in `excerpt` (T-140 r3: two equal figures in one record are told apart
    by position, never by text search); without it the first figure with this text and value is read. `records` = the case's records (D-062: whether the case
    has bills decides whether a note yields a charge). Recomputed from the quote, so nothing extra is stored."""
    block = note_charge_block(records, {"source": source, "excerpt": excerpt})
    amts = find_amounts(excerpt or "")
    hit = [a for a in amts if a["start"] == pos] if pos is not None else []
    for a in hit or [a for a in amts if a["raw"] == raw and a["cents"] == cents][:1]:
        found = non_charge_reason(excerpt, a, source)
        if found:
            return found[1]
        return charge_basis(excerpt, a, source, date_iso, block)["reason"]
    return None


# ---------------------------------------------------------------- D-064: why an amount is not counted, and whether the paralegal may count it
_RATE_NC = "This figure is a rate, not a charge, so it is not added to the total."   # the same sentences as why.py, so the row and Why this status agree
_ESTIMATE_NC = "This figure is an estimate, not a billed charge, so it is not added to the total."
_DAMAGES_NC = "This figure is not a bill (for example a damages or settlement figure), so it is not added to the total."
_INJECTION_NC = "The record this figure comes from has instruction-like text, so the figure is not counted."
_NO_VALUE_NC = "The dollar value of this figure could not be read, so it is not counted."
_NO_WORDING_NC = "The sentence with this figure does not say it was charged or billed, so it is not counted."
_BALANCE_WORD_NC = "The line also names a payment, balance, adjustment or insurance amount, so it is not counted as a charge."
_NO_SVC_NC = ("The line names no service (a service name, or a CPT, HCPCS or revenue code), so it cannot be counted as one itemized service. "
              "Add the service to the line or leave it out of the total.")
_PAYER_NC = "The line names an insurer, plan or payer, so it is an insurance figure and not what the provider itself charged for a service. It is not counted."
_ALLOWED_NC = "An allowed amount is what an insurer agreed to pay, not what the provider billed, so it is not counted."
_LIFETIME_NC = "The line sums charges over many visits (a lifetime, running or overall total), so counting it would count the same charges twice. It is not counted."
_ACCOUNT_NC = "The line is an amount held or carried on the account, not one itemized service, so it is not counted."
_AMOUNT_CHARGED_NC = "The line summarizes the amount charged for several services (for all visits, for the above), not one itemized service, so it is not counted."
_DEMOTED_NC = "You took this line out of the total."
_STALE_NC = "This line looks like an itemized charge, but it is not counted right now."
# D-064 (b): held back only because the line lacks a detail D-060 needs. Everything else (a rule, an insurer, a note that restates a bill, a second figure on a line,
# a letter or request) stays uncountable: counting those would reopen the overcount paths D-059/D-062 closed.
COUNTABLE_WHY = frozenset({_NO_DATE_WHY, _UNKNOWN_WHY})
# D-064 r2 (adjuster): the label words that make a line a restatement or a summary, not one itemized service. They are checked in the figure's own sentence of a line
# that is otherwise countable; a miss here still stops at the service-description rule (a line needs a service noun or a code).
_NAMES_INSURER = (r"aetna|cigna|humana|united\s?health\w*|uhc|anthem|blue\s*(?:cross|shield)|bcbs\w*|medicare|medicaid|tricare|kaiser|geico|state\s+farm|allstate|progressive|"
                  r"liberty\s+mutual|farmers|nationwide|travelers|payers?|payors?|carriers?|tpa|eob|era|pip|med\s?pay|medpay|third[\s-]party|(?:health|insurance|benefit|group)\s+plan|"
                  r"plan\s+(?:billed|allowed|paid|charges?|amount|responsibility)|claims?\s+(?:charge|amount|total|summary)|"
                  # T-171 r3: any payer or insurer name, and the payer words, wherever they stand in the line (the r2 closed list was one name short each time)
                  r"insurers?|insurance|insured|underwriters?|hmo|ppo|epo|oscar|molina|usaa|wellcare|ambetter|centene|optum|sedgwick|zurich|chubb|hartford|esurance|safeco|amfam|"
                  r"american\s+family|amerigroup|health\s?net|coventry|multi\s?plan|first\s?health|gallagher\s+bassett|texas\s+mutual|sentry|mercury|the\s+general|"
                  r"workers['\u2019]?\s*(?:comp\w*|compensation)|(?<!care\s)(?<!treatment\s)(?<!plan\sof\s)plans?(?!\s+of\s+care)|reprice[ds]?|repricing|"
                  r"in[\s-]network|out[\s-]of[\s-]network|network\s+(?:rate|price|amount)|fee\s+schedule|usual\s+and\s+customary|ucr|negotiated|approved|eligible|covered|discounted|"
                  r"write[\s-]?offs?|written\s+off|contractual\w*")
_LINE_CUES = (
    (re.compile(r"\b(?:allowed|allowable)\b|\bcontract(?:ed|ual)?\s+(?:rate|amount|price)\b", re.IGNORECASE), _ALLOWED_NC),
    (re.compile(rf"\b(?:{_NAMES_INSURER})\b", re.IGNORECASE), _PAYER_NC),
    (re.compile(r"\b(?:lifetime|life[\s-]to[\s-]date|cumulative|year[\s-]to[\s-]date|ytd|to[\s-]date|total|totals|subtotal|sum|grand|combined|aggregate|overall|together|"
                r"altogether|came\s+to|comes\s+to|amounts?\s+to|add(?:s|ed)?\s+up|adds\s+up|running|gross|since\s+(?:the\s+)?(?:first|initial|start|beginning|\d)|so\s+far|thus\s+far|"
                r"through\s+(?:today|date)|up\s+to\s+(?:today|date)|episode\s+of\s+care|(?:whole|entire)\s+(?:course|episode|treatment|period)|charges\s+for\s+visits?\s+\d+|"
                r"(?:previous|prior|last)\s+statement|billed\s+amount)\b", re.IGNORECASE), _LIFETIME_NC),
    (re.compile(r"\bon\s+(?:the\s+)?account\b|\bheld\b|\bunder\s+(?:a\s+)?(?:letter\s+of\s+protection|lop)\b|\blop\b|\bcarried\b|\bforward(?:ed)?\b|\bbrought\b|"
                r"\bpending\s+(?:settlement|resolution)\b|\bescrow\b|\blien\b|\bcollections?\b|\bdeferred\b|\bon\s+hold\b|\b(?:to|with)\s+(?:the\s+)?attorney\b", re.IGNORECASE), _ACCOUNT_NC),
    (re.compile(r"\bamount\s+(?:charged|billed)\b|\b(?:charges?|billed|fees?|cost)\s+(?:for|of)\s+(?:all|the\s+above|the\s+(?:above|following)|these|those|every|each)\b|"
                r"\bfor\s+(?:all|every)\s+(?:visits?|dates?|services?|treatments?|care|sessions?)\b|\ball\s+(?:\w+\s+){0,2}(?:visits|services|dates|treatments|sessions|charges|fees)\b|"
                r"\bthe\s+above\b|\babove\s+(?:services|charges|visits)\b|\bpage\s+\d|\bthis\s+(?:page|statement|bill)\b", re.IGNORECASE), _AMOUNT_CHARGED_NC),
)


def _line_cue(sentence: str):
    """The plain reason for the first restatement / summary label word in the figure's own sentence (insurer, payer, allowed, lifetime or running total, on account,
    'amount charged' summary), or None."""
    return next((why for rx, why in _LINE_CUES if rx.search(sentence or "")), None)
SEPARATE_CHARGE = "separate_charge"
_NC_FIXED = {"rate": _RATE_NC, "estimate": _ESTIMATE_NC, "damages": _DAMAGES_NC}


@_masked
def not_counted(excerpt: str, raw: str, cents, source: str = None, date_iso: str = None, pos: int = None, records: list = None, kind: str = "unclear",
                injection: bool = False, demoted: bool = False) -> dict:
    """D-064: {reason, countable} for one amount, from the quote and the record alone (nothing stored). `reason` is a plain sentence (None for a charge, which is counted
    once she accepts it). `countable` is True only for a figure the code held back for a missing detail (no date of service, a document with no bill header), or one
    she took out of the total herself and the code still reads as an itemized line; never for a figure a rule excludes (total, balance, payment, adjustment, credit,
    year-to-date, insurer restatement, a negative or zero, a note restating the same provider's bill, a second amount on a line, a letter or request). Rates, estimates
    and work-loss mentions are not countable here (a rate becomes a charge only through the guarded reclassify route)."""
    if kind == "charge":
        return {"reason": None, "countable": False}
    if kind in _NC_FIXED:
        return {"reason": _NC_FIXED[kind], "countable": False}
    if injection:
        return {"reason": _INJECTION_NC, "countable": False}
    if cents is None:
        return {"reason": _NO_VALUE_NC, "countable": False}
    amts = find_amounts(excerpt or "")
    hit = [a for a in amts if a["start"] == pos] if pos is not None else []
    a = (hit or [x for x in amts if x["raw"] == raw and x["cents"] == cents][:1] or [None])[0]
    if a is None:
        return {"reason": _NO_WORDING_NC, "countable": False}
    found = non_charge_reason(excerpt, a, source)
    if found:
        return {"reason": found[1], "countable": False}
    basis = charge_basis(excerpt, a, source, date_iso, note_charge_block(records, {"source": source, "excerpt": excerpt}))
    sent = next((excerpt[x:y] for x, y in _own_sentences(excerpt) if x <= a["start"] < y), "")
    if basis["ok"]:
        if demoted:
            cue = _line_cue(sent)
            return {"reason": cue or _DEMOTED_NC, "countable": cue is None}
        return {"reason": _STALE_NC, "countable": False}
    why = basis["reason"] or _NO_WORDING_NC
    if why in COUNTABLE_WHY:             # the same wording gate the guarded reclassify uses: a charge word in the figure's own sentence, and no payment / balance / adjustment word
        if BALANCE_CUE.search(sent):
            return {"reason": _BALANCE_WORD_NC, "countable": False}
        if not _charged_wording(excerpt, sent, a):
            return {"reason": _NO_WORDING_NC, "countable": False}
        cue = _line_cue(sent)             # D-064 r2: a restatement or a summary (insurer, allowed, lifetime, on account, 'amount charged') is not one itemized service
        if cue:
            return {"reason": cue, "countable": False}
        if not basis["svc"]:              # D-064 r2: countable needs a service description and only a missing date of service or bill header
            return {"reason": _NO_SVC_NC, "countable": False}
    return {"reason": why, "countable": why in COUNTABLE_WHY}


_CHARGED_WORDING = re.compile(r"\b(?:charged|charges?|billed|invoiced|amount\s+due|balance\s+due|total\s+billed)\b", re.IGNORECASE)
_NEGATED_CHARGE = re.compile(r"\b(?:not|never|no|without|unbilled|uncharged)\s+(?:\w+\s+)?(?:charged|charges?|billed|invoiced)\b|\b(?:unbilled|uncharged)\b", re.IGNORECASE)


def _charged_wording(excerpt: str, sent: str, a: dict) -> bool:
    """The wording gate the guarded reclassify applies (reclassify.charge_wording), for one figure: charged-amount wording in its own sentence (English, or the Spanish cue),
    no payment / balance word, no negation, no rate cue, and the classifier does not read the figure as a rate."""
    m = _CHARGED_WORDING.search(sent)
    es = None if m else charge_cue_es(sent)
    if not (m or es) or (m and BALANCE_CUE.search(sent)) or _NEGATED_CHARGE.search(sent) or RATE_CUE.search(sent):
        return False
    return classify(excerpt, {"start": a["start"], "end": a["end"], "cents": 1}) != "rate"


def _own_sentences(excerpt: str) -> list:
    """[(start, end)] of the excerpt's sentences, the boundary rule classify and reclassify use."""
    out, pos = [], 0
    for m in _BOUNDARY.finditer(excerpt or ""):
        out.append((pos, m.start()))
        pos = m.end()
    out.append((pos, len(excerpt or "")))
    return out


def _is_billing_source(source: str) -> bool:
    return any(e["id"] == "billing_document" and e["regex"].search(source or "") for e in lexicon.code_list("non_encounter"))


def damages_mentions(excerpt: str) -> list:
    """Work-loss and similar mentions with no dollar value (lexicon `damages`): [{raw, cents: None, cls: 'damages', start, end}]."""
    out = []
    for e in lexicon.code_list("damages"):
        for m in e["regex"].finditer(excerpt or ""):
            end = m.end()
            t = _WORK_TAIL.match(excerpt, end)
            if t:
                end = t.end()
            if not any(o["start"] < end and m.start() < o["end"] for o in out):
                out.append({"raw": excerpt[m.start():end], "cents": None, "cls": "damages", "start": m.start(), "end": end})
    return sorted(out, key=lambda o: o["start"])


def _norm(s):
    return " ".join((s or "").split()).casefold()


def dedupe_amounts(amounts: list, separate=frozenset()) -> list:
    """Same date + normalised provider + record text (when given) + class + value merges into one amount citing every record (R-CH-6). Unreadable values never merge.
    Two figures of the SAME record never merge (D-059: two visits at the same price on one statement are two charges)."""
    out, index = [], {}
    for a in amounts:
        nos = sorted(a.get("record_nos") or [a["record_no"]])
        key = (a.get("date"), _norm(a.get("provider")), _norm(a.get("text")), a.get("cls"), a.get("cents")) if a.get("cents") is not None else None
        if set(nos) & set(separate):        # records the paralegal declared not-a-duplicate never merge (D-031)
            key = None
        if key in index and not set(nos) & set(out[index[key]]["record_nos"]):
            m = out[index[key]]
            m["record_nos"] = sorted(set(m["record_nos"]) | set(nos))
            m["duplicate_note"] = "Same amount, date and provider appears in records " + ", ".join(str(n) for n in m["record_nos"]) + "."
            continue
        row = {**a, "record_nos": nos, "duplicate_note": None}
        if key is not None and key not in index:
            index[key] = len(out)
        out.append(row)
    return out


def same_service(x: dict, y: dict) -> bool:
    """Two charge bases (`charge_basis` dicts) describe the same service on the same day: same date of service and, by their descriptions, the same service. Codes
    decide when both lines carry one; otherwise the shorter description's word stems must all appear in the other ('Manual therapy', 'Manual therapy (97140)' and
    'manual ther' meet; 'Manual therapy' and 'Therapeutic exercise' do not). The amount is compared by the caller."""
    if not x.get("dos") or x.get("dos") != y.get("dos"):
        return False
    if x["codes"] and y["codes"]:
        return bool(x["codes"] & y["codes"])
    a, b = x["tokens"], y["tokens"]
    return not a or not b or a <= b or b <= a


def _merge_same_service(out: list, separate) -> list:
    """D-060: a charge with the same normalized date of service, service and amount as an earlier charge of ANOTHER record (a statement re-listing a visit, in any
    date format) is the same charge: one amount that cites both records, as R-CH-6 merges identical amounts. Records the paralegal declared not-a-duplicate never
    merge (D-031). Two lines of the SAME record never merge."""
    kept = []
    for a in out:
        b = a.get("basis")
        hit = None
        if b and b["ok"] and a["cls"] == "charge" and a.get("cents") and not a.get("injection"):
            for f in kept:
                fb = f.get("basis")
                if (fb and fb["ok"] and f["cls"] == "charge" and f["cents"] == a["cents"] and not set(f["record_nos"]) & set(a["record_nos"])
                        and not (set(f["record_nos"]) | set(a["record_nos"])) & set(separate) and same_service(fb, b)):
                    hit = f
                    break
        if hit is None:
            kept.append(a)
            continue
        hit["record_nos"] = sorted(set(hit["record_nos"]) | set(a["record_nos"]))
        hit["duplicate_note"] = "Same service, date and amount appears in records " + ", ".join(str(n) for n in hit["record_nos"]) + "."
    return kept


def promotion_flag(target: dict, others: list):
    """The flag a charge gets when a paralegal PROMOTES a figure to a charge after extraction (T-140 r3), so the promoted line cannot skip the checks extraction
    gives a charge. `target` = {id, record_no, cents, basis}; `others` = the case's other live charges, each {id, record_no, cents, basis, [line]} (`line` = amounts.charge_line of the other charge, named in the sentence). A same-service duplicate of
    another record's charge is flagged likely_duplicate (merging would hide a line she chose to count); a figure equal to the sum of at least two other charges of
    its record is flagged likely_total. None when neither applies."""
    for o in others:
        if o["id"] != target["id"] and o["cents"] == target["cents"] and o["record_no"] != target["record_no"] and same_service(target["basis"], o["basis"]):
            where = f"\u201c{o['line']}\u201d in record {o['record_no']}" if o.get("line") else f"a line already listed in record {o['record_no']}"
            return confirm_info("likely_duplicate", o["id"], f"{where}: {_usd(target['cents'])}. ")
    same = [o for o in others if o["id"] != target["id"] and o["record_no"] == target["record_no"] and o.get("cents")]
    if len(same) >= 2 and sum(o["cents"] for o in same) == target["cents"]:
        return confirm_info("likely_total")
    return None


# T-171 r3: service words that name the same thing. The stems are `_tokens` stems (four letters). Pairs are symmetric and NOT transitive ('pt' is a patient, physical
# therapy or a physical-therapy visit, but 'patient' is not 'therapy'). A stem is also equivalent to another it is a prefix of ('vis' / 'visi'), three letters or more.
_STEM_ALIASES = {
    "pt": {"pati", "phys", "ther"}, "ov": {"offi", "visi"}, "mt": {"manu", "ther"}, "cmt": {"chir", "mani"}, "tx": {"trea"}, "ex": {"exer"}, "est": {"esta"},
    "us": {"ultr"}, "mri": {"magn"}, "ct": {"tomo", "comp"}, "estim": {"stim", "elec"}, "adj": {"adju"}, "inj": {"inje"}, "eval": {"exam", "asse"},
    "xray": {"ray", "rays", "radi"}, "ray": {"rays", "radi"}, "rays": {"radi"}, "ther": {"phys"},
}


def _stem_equiv(s: str, t: str) -> bool:
    if s == t or t in _STEM_ALIASES.get(s, ()) or s in _STEM_ALIASES.get(t, ()):
        return True
    short, long_ = sorted((s, t), key=len)
    return len(short) >= 3 and long_.startswith(short)


def _covers(a: frozenset, b: frozenset) -> bool:
    """Every service word of `a` has an equivalent in `b`."""
    return bool(a) and all(any(_stem_equiv(s, t) for t in b) for s in a)


def code_descriptions(bases: list) -> dict:
    """{code: service-word stems} from the case's own lines: a line that states a code AND a description teaches what that code is called here. Nothing is assumed about a code the case
    never describes."""
    out = {}
    for b in bases:
        if b and b.get("codes") and b.get("tokens"):
            for c in b["codes"]:
                out.setdefault(c, set()).update(b["tokens"])
    return out


def _same_service_any_day(x: dict, y: dict, desc: dict = None) -> bool:
    """D-064 r2/r3: two charge bases describe the same service when their codes meet (both coded), or their descriptions overlap after normalizing (word families, abbreviations:
    PT / physical therapy, pt / patient, xray / x-ray / radiograph; the shorter description's words must each have an equivalent in the other), or a code and a description meet
    by what the case itself says (`desc` = code_descriptions of the case). A code with no description anywhere in the case, against a described line, is a candidate (the
    paralegal is asked, not told). A date is compared only when BOTH lines state one: a line with no date of service may be the same visit as a dated one."""
    if x.get("dos") and y.get("dos") and x["dos"] != y["dos"]:
        return False
    if x["codes"] and y["codes"]:
        return bool(x["codes"] & y["codes"])
    desc = desc or {}
    toks = []
    for z in (x, y):
        t = set(z["tokens"])
        for c in z["codes"]:
            t |= desc.get(c, set())
        toks.append(frozenset(t))
    a, b = toks
    if a and b:
        return _covers(a, b) or _covers(b, a)
    coded, other = (x, y) if (x["codes"] and not a) else (y, x) if (y["codes"] and not b) else (None, None)
    return bool(coded and other["tokens"] and not other["codes"])         # a code nothing in the case describes, against a described line at the same amount


def count_flag(target: dict, others: list):
    """D-064 r2: the confirm a countable line needs before the paralegal counts it, from the case's other lines: `target` = {id, record_no, cents, basis}; `others` = every other
    live line of the case that is a charge or is itself countable, each {id, record_no, cents, basis, charge (bool), [line]}. likely_duplicate when ANOTHER line (any record, the same record
    too) has the same amount and the same service (normalized, see `_same_service_any_day`) and a compatible date (no date on one side, or the same date): an undated line cannot tell a
    repeat from a second visit, so the paralegal names it. A charge is matched before a countable line. Else the promoted-figure rule (a dated duplicate of another record's charge; a
    figure equal to the sum of its record's other charges: likely_total). None when neither applies. `separate_charge` alone is never enough for a line that matches."""
    if target["cents"] is None or not target.get("basis"):
        return None
    desc = code_descriptions([target["basis"]] + [o.get("basis") for o in others])
    cand = [o for o in others if o["id"] != target["id"] and o["cents"] == target["cents"] and o.get("basis") and _same_service_any_day(target["basis"], o["basis"], desc)]
    for o in sorted(cand, key=lambda o: not o.get("charge")):
        where = f"\u201c{o['line']}\u201d in record {o['record_no']}" if o.get("line") else f"a line already listed in record {o['record_no']}"
        return confirm_info("likely_duplicate", o["id"], f"{where}: {_usd(target['cents'])}. ")
    return promotion_flag(target, [o for o in others if o.get("charge")])


def extract_amounts(records: list, separate=frozenset()) -> list:
    """All amounts of a case from ingested records (needs n, excerpt; uses date_iso, source, injection_tag, text, char_start when present).
    Injection-tagged records yield class unclear for every amount (D-005). Duplicate records contribute once (the dedupe is per record).
    `separate` = record numbers the paralegal said are not duplicates: their amounts never merge with another record's and get ids ax<n>_<k>.
    D-060: a charge is a figure on an itemized service line only; the same service, date and amount in two records is one amount citing both.
    D-059: each row carries `confirm` (None, or the likely_total flag the paralegal must confirm by name before accepting it)."""
    rows = []
    for r in records:
        if r.get("duplicate_of"):
            continue
        base = (r.get("char_start") or 0) + (r["text"].find(r["excerpt"]) if r.get("text") and r["excerpt"] in r["text"] else 0)
        block = note_charge_block(records, r)
        found = [{**a, "cls": classify(r["excerpt"], a, injection=bool(r.get("injection_tag")), source=r.get("source"), date_iso=r.get("date_iso"), note_block=block)}
                 for a in find_amounts(r["excerpt"])]
        for a in found:
            a["basis"] = charge_basis(r["excerpt"], a, r.get("source"), r.get("date_iso"), block) if a["cls"] == "charge" else None
        totals = _likely_totals([{**a, "injection": bool(r.get("injection_tag"))} for a in found])      # a charge equal to the others may be a total: flag, never drop
        for i, a in enumerate(found):
            a["confirm"] = confirm_info("likely_total") if i in totals else None
        found += [{**d, "confirm": None, "basis": None} for d in damages_mentions(r["excerpt"])]
        for a in sorted(found, key=lambda x: x["start"]):
            rows.append({"record_no": r["n"], "text": r["excerpt"], "date": r.get("date_iso"), "provider": r.get("source"), "raw": a["raw"], "cents": a["cents"],
                         "cls": a["cls"], "start": base + a["start"], "end": base + a["end"], "lstart": a["start"], "injection": bool(r.get("injection_tag")),
                         "confirm": a["confirm"], "basis": a["basis"]})
    out = _merge_same_service(dedupe_amounts(rows, separate), separate)
    i, k = 0, {}
    for a in out:
        if a["record_no"] in separate:         # stable ids that do not shift the other amounts: a rerun lands on the same rows
            k[a["record_no"]] = k.get(a["record_no"], 0) + 1
            a["id"] = f"ax{a['record_no']}_{k[a['record_no']]}"
        else:
            i += 1
            a["id"] = f"a{i}"
    return out


_PLAN = re.compile(r"plan\s+of\s+care\s*:\s*(\d+)\s+visits?", re.IGNORECASE)
_VISIT = re.compile(r"\bvisit\s+(\d+)\b", re.IGNORECASE)


def _prefix(source):
    return _norm((source or "").split(",")[0])


def rate_note(records: list, record_no: int) -> dict:
    """Numbers for the rate note, code-derived (T-033 AC7): planned N from 'Plan of care: N visits' in a record with the same provider
    prefix (header label before the first comma); last_visit M = highest 'visit M' in such a header label. None when not found."""
    me = next(r for r in records if r["n"] == record_no)
    same = [r for r in records if _prefix(r.get("source")) == _prefix(me.get("source"))]
    planned = next((int(m.group(1)) for r in same for m in [_PLAN.search(r.get("excerpt") or "")] if m), None)
    visits = [int(m.group(1)) for r in same for m in [_VISIT.search(r.get("source") or "")] if m]
    return {"planned": planned, "last_visit": max(visits) if visits else None}
