"""THE money detector (T-139 round 4; D-019, R-CH-7, R-EX-8). CODE ONLY (no LLM, no network). One module, three callers, no divergence:

  - the charge-text hold      app/backend/charge_text.py  (an entry whose summary or quote states money is held out; the edit check refuses it)
  - the export gate           app/backend/export.py       (the final letter text: any money outside the R-EX-8 total line and the accepted-charge lines blocks the export)
  - the letter eval           evals/letter_check.py       (the audit over every golden and library case)

If this module is blind to a wording, all three are blind to it and the closed world below says so; if it holds a wording, all three hold it.

    hits(text)    -> [(start, end, text, kind)]   every money expression, in order of position, no two overlapping. kind:
                                                   dollar    '$' figure (also OCR-noisy '$1,2OO'), 'N dollars', 'USD N'
                                                   sign      another currency sign next to a figure ('EUR 185', '185 EUR', '1,200', full-width and small dollar signs)
                                                   spoken    amounts in words ('one hundred eighty-five dollars', 'billed at two thousand one hundred fifty')
                                                   unmarked  money without a sign: a money word or claim-form field and its figure ('TOTAL CHARGE 49100', 'Patient responsibility
                                                             1,200.00', 'Paid in full 2,150.00', '40 a visit', 'the 3,915 ER bill', CMS-1500 24F, UB-04 FL47)
                                                   statement a figure inside a patient's statement ('Patient states the ER bill was 3,915')
    strings(text) -> [text, ...]                  the same, as written
    has_money(text)
    dollar_strings(text)                          the dollar + sign + spoken kinds (the figures export may quote on a charge line)

A figure counts only when a money word, a currency sign or noun, or a claim-form field names it, so dates, pain scores, doses, visit counts and CPT/ICD codes are never money.

Closed world (scope cut 7c, written down): not detected are slang or shorthand ('6.5k', 'one eighty-five each', 'x 185'), a bare decimal with no money word ('Initial exam
185.00'), per-mile rates, and Spanish number words other than the hundreds. A record that states money only like that still reaches the carrier letter if the paralegal accepts it."""
import re

from app.backend import amounts

_ISO = r"(?:USD|EUR|GBP|CAD|MXN|AUD|CHF|JPY|INR|CNY|PHP|BRL|NZD|KRW|RUB)"
_NOUN = r"(?:dollars?|bucks?|pesos?|euros?|cents?|d[oó]lares)"
_WORDS = re.compile(r"\b\d[\d,]*(?:\.\d+)?\s*(?:" + _NOUN + r"|" + _ISO + r")\b|\b" + _ISO + r"\s*\d[\d,]*(?:\.\d+)?", re.IGNORECASE)
# Other currency signs ('€185', '185 €', '£1,200', '1.200,00 €', full-width '＄185', small '﹩185') .
_SIGN = re.compile(r"[€£¥₹₱₩₽₫₦＄﹩]\s?\d[\d,]*(?:\.\d+)?|\bRs\.?\s?\d[\d,]*(?:\.\d+)?|(?<![\w.,])\d[\d.,]*\d\s?[€£¥₹]|(?<![\w.,])\d\s?[€£¥₹]")
_NUMWORD = (r"(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|"
            r"fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|dos|tres|cuatro|cinco|diez|veinte|cien|ciento|cientos|mil)")
_NUMRUN = _NUMWORD + r"(?:(?:[\s-]+(?:and\s+)?)" + _NUMWORD + r")*"
_SPOKEN = re.compile(r"\b(?:an?\s+)?" + _NUMRUN + r"\s+" + _NOUN + r"\b|\b(?:\w+cientos|cuatrocientos|quinientos)\s+d[oó]lares\b", re.IGNORECASE)
_DIGIT = re.compile(r"\d")

_NUM = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:\s[0-9Oo]{2}(?!\w))?"                       # '49100', '3,915.00', '0 00', '96 OO'
_UNITS = (r"days?|visits?|units?|hours?|hrs?|minutes?|mins?|weeks?|wks?|months?|years?|yrs?|sessions?|treatments?|times|x|views?|sets?|reps?|mg|mcg|ml|cc|kg|lbs?|feet|ft|"
          r"steps?|miles?|mph|bpm|mmHg|degrees?|mm|cm|inch(?:es)?|charts?|pages?|items?")
_NOT_UNIT = r"(?!\s*(?:[-:/]\s*\d|\d|%|(?:" + _UNITS + r")\b))"
# After a money word the figure follows directly or after a short connector ('came to', 'amounts to', 'at', 'about').
_FILL = (r"(?:\s*[:=\-–]\s*|\s+)(?:(?:of|is|was|at|due|owed|each|came\s+to|comes\s+to|amounts?\s+to|totall?ed|about|around|approx\.?|approximately|roughly|"
         r"per\s+(?:visit|unit|session|day|treatment|adjustment))\s*[:=]?\s+)*-?")
# A label that names money by itself: any figure right after it is money ('Patient responsibility 6', 'Lost wages 1,800.00', 'Paid in full 3').
_STRONG = (r"\b(?:total\s+charges?|charges?|amount\s+(?:paid|billed|due|owed|charged|allowed)|balance\s+(?:due|owed|forward)|(?:outstanding|current|remaining)\s+balance|"
           r"co-?pay(?:ments?)?|co-?insurance|deductible|billed|invoice[d]?|fees?|saldo|costo|importe|net\s+due|med-?pay|"
           r"patient\s+responsibility|reimbursements?|paid\s+in\s+full|usual\s+and\s+customary|(?:lost\s+)?wages?(?:\s+loss)?|wage\s+loss|lost\s+(?:income|earnings)|dollars?)\b")
# A weaker word is money only when the figure is money-shaped (a thousands separator, cents, or 3+ digits).
_WEAK = (r"\b(?:costs?(?:\s+estimate)?|estimate[d]?|paid|settlement(?:\s+(?:offer|demand|amount))?|offer|demand|reduced\s+to|payments?|price|allowed|balance|write-?off|owed|owes?|"
         r"(?:invoice|medical|network|self-?pay|cash|visit|out-of-pocket|lien)\s+(?:totals?|amounts?|specials?|discounts?|adjustments?|rate|price|balance|bills?)|"
         r"self-?pay|out-of-pocket|lien|(?<!type of )bills?|discounts?|adjustments?|totals?|amounts?|specials?|"
         r"reimbursed|spent|refunds?|deposit|policy\s+limits?|cost\s+the\s+patient|lost)\b")
_MONEY_SHAPED = re.compile(r"\d{1,3}(?:,\d{3})+|\d+\.\d\d\b|\d{3,}|\d\s[0-9Oo]{2}\b")
_UNMARKED = [re.compile(_STRONG + _FILL + _NUM + _NOT_UNIT, re.IGNORECASE)]
_UNMARKED_WEAK = re.compile(_WEAK + _FILL + _NUM + _NOT_UNIT, re.IGNORECASE)

# A figure inside a patient's statement ('Patient states the ER bill was 3,915', 'she owes the chiropractor about 2,400', 'charged me fifteen hundred for the MRI').
_SAY = r"\b(?:states?|stated|reports?|reported|says?|said|claims?|claimed|told|alleges?)\b"
_FIG = r"(?:\d{1,3}(?:,\d{3})+|\d{2,})(?:\.\d+)?"
_STATEMENT = [
    re.compile(_SAY + r"[^.\n]{0,100}?\b(?:bills?|billed|owes?|owed|costs?|paid|pays?|spent|charged|co-?pay|price|out[\s-]of[\s-]pocket|run\s+about)\b[^.\n]{0,40}?"
               r"(?:(?<![\w/.,-])" + _FIG + _NOT_UNIT + r"|\b(?:\w+\s+)?(?:hundred|thousand)\b)", re.IGNORECASE),
    re.compile(_SAY + r"[^.\n]{0,80}?(?<![\w/.,-])(?:\d{1,3}(?:,\d{3})+(?:\.\d\d)?|\d+\.\d\d)" + _NOT_UNIT, re.IGNORECASE),
]
_SPOKEN_HUNDRED = re.compile(r"\b(?:hundred|thousand)\b", re.IGNORECASE)

# Round 4: a money verb or noun, then number words with no currency noun ('billed at two thousand one hundred fifty', 'quoted at fifteen hundred', 'owes twelve hundred').
_VERB = (r"\b(?:paid\s+in\s+full|patient\s+responsibility|usual\s+and\s+customary|(?:lost\s+)?wages?(?:\s+loss)?|wage\s+loss|co-?pay(?:ments?)?|co-?insurance|deductible|reimbursed|reimbursements?|"
         r"refunds?|deposit|spent|out[\s-]of[\s-]pocket|med-?pay|policy\s+limits?|net\s+due|allowed|write-?off|adjustments?|settled|settlement|"
         r"billed|quoted|charged|priced|invoiced|costs?|costing|paid|pays?|owes?|owed|charges?|fees?|price|estimated|estimate|bill|rate|balance|lien)\b"
         r"(?:\s+(?:at|of|for|to|is|was|about|around|roughly|approximately|approx\.?|came\s+to|comes\s+to|totall?ed|an?))*\s+")
_NOT_COUNT = r"(?!\s*(?:" + _UNITS + r"|claims?|bills?|invoices?|copies|doses?|tablets?|pills?|injections?|appointments?|referrals?|studies|exams?|scans?|x-?rays?)\b)"
_SPOKEN_AFTER = re.compile(_VERB + r"(" + _NUMRUN + r")(?!\w)" + _NOT_COUNT, re.IGNORECASE)
# 'lost eighteen hundred in wages': the number words come before the money label.
_SPOKEN_BEFORE = re.compile(r"\blost\s+(" + _NUMRUN + r")(?=\s+(?:in\s+|of\s+)?(?:wages?|income|earnings|pay)\b)", re.IGNORECASE)
# Round 4: 'N a visit' / 'N each visit' with any digit count ('12 visits at 40 a visit'); 'N per visit' with 2+ digits.
_PER_VISIT = re.compile(r"(?<![\w/.,-])(?:\d+(?:\.\d\d)?\s+(?:a|each)|\d{2,}(?:,\d{3})*(?:\.\d\d)?\s+per)\s+(?:visit|session|treatment|appointment)s?\b", re.IGNORECASE)
# Round 4: a money-shaped figure directly before bill / invoice / charge ('the 3,915 ER bill', '1,380 invoice'); 'charge nurse' is not a bill.
_BEFORE_BILL = re.compile(r"(?<![\w/.,-])(?:\d{1,3}(?:,\d{3})+(?:\.\d\d)?|\d+\.\d\d|\d{3,})(?!\s*(?:[-:/]\s*\d|%|(?:" + _UNITS + r")\b))"
                          r"(?:\s+[A-Za-z-]+){0,2}?\s+(?:bills?|invoices?|charges?(?!\s+nurse))\b", re.IGNORECASE)
_UNMARKED_FORM = [
    re.compile(r"\b24F\b[^.\n]{0,80}", re.IGNORECASE),                                                  # CMS-1500 item 24F is the charges column
    re.compile(r"\bFL\s?(?:47|48)\b\W{0,3}" + _NUM + _NOT_UNIT, re.IGNORECASE),                          # UB-04 total / non-covered charges
    re.compile(r"\bitem\s*(?:28|29|30)\b\W{0,3}" + _NUM + _NOT_UNIT, re.IGNORECASE),                     # CMS-1500 total charge, amount paid, balance
    re.compile(r"\b(?:CPT|HCPCS)\s*[A-Z]?\d{4,5}\s*,\s*[0-9Oo][0-9Oo ,.]*\s*,\s*\d+\s*units?\b", re.IGNORECASE),   # 'CPT 99204, 18500, 1 unit': code, charge, units
    re.compile(r"\b\d[\d,]*\.\d\d\s*(?:/|per\s+)\s*(?:visit|unit|session|day|treatment)s?\b", re.IGNORECASE),    # '140.00 per visit'
    re.compile(r"\b\d{3,}\s*/\s*(?:visit|unit|session)s?\b", re.IGNORECASE),                           # '140/visit'
    re.compile(r"\b\d[\d,]*\.\d\d\s+por\s+(?:sesi[o\u00f3]n|visita|consulta|d[i\u00ed]a)\b", re.IGNORECASE),     # Spanish '400.00 por sesi\u00f3n'
    re.compile(r"\brate\b" + _FILL + r"(?:\d{1,3}(?:,\d{3})+(?:\.\d\d)?|\d+\.\d\d)\b" + _NOT_UNIT, re.IGNORECASE),   # 'rate 140.00' (a heart or pulse rate has no cents)
    _PER_VISIT, _BEFORE_BILL,
]

# Amounts in words directly before a currency noun, by a token walk (catches runs the regex misses, e.g. 'and a thousand bucks').
_CURRENCY_NOUNS = {"dollar", "dollars", "buck", "bucks", "peso", "pesos", "euro", "euros", "cent", "cents", "dolar", "dolares", "dólar", "dólares"}
_NUMBER_WORDS = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty "
                    "sixty seventy eighty ninety hundred thousand million dos tres cuatro cinco seis siete ocho nueve diez veinte treinta cien ciento mil cuatrocientos "
                    "quinientos doscientos trescientos seiscientos setecientos ochocientos novecientos".split())
_WORD_TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*", re.UNICODE)


def _number_token(w: str) -> bool:
    parts = w.split("-")
    return all(p in _NUMBER_WORDS or p == "and" for p in parts) and any(p in _NUMBER_WORDS for p in parts)


def _token_walk(t: str) -> list:
    out = []
    toks = [(m.start(), m.end(), m.group(0).lower()) for m in _WORD_TOKEN.finditer(t)]
    for i, (a, b, w) in enumerate(toks):
        if w not in _CURRENCY_NOUNS:
            continue
        j = i
        while j > 0 and not t[toks[j - 1][1]:toks[j][0]].strip() and (_number_token(toks[j - 1][2]) or toks[j - 1][2] in {"and", "y", "a", "an"}):
            j -= 1
        while j < i and not _number_token(toks[j][2]):             # a run must start at a number word ('and' / 'a' alone is not an amount)
            j += 1
        if j < i:
            out.append((toks[j][0], b, t[toks[j][0]:b], "spoken"))
    return out


def _spoken_after(t: str) -> list:
    out = []
    for m in list(_SPOKEN_AFTER.finditer(t)) + list(_SPOKEN_BEFORE.finditer(t)):
        run = m.group(m.lastindex)
        if run.strip().lower() == "one":                           # a lone 'one' ('paid one') is a count, not an amount
            continue
        out.append((m.start(), m.end(), m.group(0), "spoken"))
    return out


def _marked(t: str) -> list:
    """The signed kinds, unsorted: dollar, sign, spoken."""
    hits = [(m.start(), m.end(), m.group(0), "dollar") for m in amounts._AMT.finditer(t) if _DIGIT.search(m.group(0))]
    hits += [(m.start(), m.end(), m.group(0), "dollar") for m in _WORDS.finditer(t)]
    hits += [(m.start(), m.end(), m.group(0), "sign") for m in _SIGN.finditer(t)]
    hits += [(m.start(), m.end(), m.group(0), "spoken") for m in _SPOKEN.finditer(t)]
    return hits + _token_walk(t) + _spoken_after(t)


def _unmarked(t: str) -> list:
    raw = []
    for rx in _UNMARKED + _UNMARKED_FORM:
        raw += [(m.start(), m.end(), m.group(0), "unmarked") for m in rx.finditer(t)]
    raw += [(m.start(), m.end(), m.group(0), "statement") for rx in _STATEMENT for m in rx.finditer(t)]
    raw += [(m.start(), m.end(), m.group(0), "unmarked") for m in _UNMARKED_WEAK.finditer(t) if _MONEY_SHAPED.search(m.group(0).split(None, 1)[-1] if " " in m.group(0) else "")]
    return raw


def _overlaps(a, b, spans) -> bool:
    return any(a < sb and sa < b for sa, sb, *_ in spans)


def hits(text) -> list:
    """Every money expression in `text` as (start, end, text, kind), in order of position, none overlapping another. The signed kinds win over the unmarked ones; of two
    overlapping hits the longer (then the first) is kept."""
    t = text or ""
    kept = []
    for a, b, s, k in sorted(_marked(t), key=lambda h: (-(h[1] - h[0]), h[0])):
        if not _overlaps(a, b, kept):
            kept.append((a, b, s, k))
    for a, b, s, k in sorted(_unmarked(t), key=lambda h: (h[0], -(h[1] - h[0]))):
        if not (_DIGIT.search(s) or _SPOKEN_HUNDRED.search(s)) or _overlaps(a, b, kept):
            continue
        kept.append((a, b, s.strip(), k))
    return sorted(kept)


def strings(text) -> list:
    """Every money expression in `text` as written, in order of position."""
    return [s for _, _, s, _ in hits(text)]


def has_money(text) -> bool:
    return bool(hits(text))


def of_kind(text, *kinds) -> list:
    """The money expressions of the given kinds ('dollar', 'sign', 'spoken', 'unmarked', 'statement'), in order of position."""
    return [s for _, _, s, k in hits(text) if k in kinds]


def dollar_strings(text) -> list:
    """The signed figures (dollar, sign, spoken kinds) as written: the figures export may quote on an accepted-charge line."""
    return of_kind(text, "dollar", "sign", "spoken")


def lines_with_money(lines, skip=()) -> list:
    """[(index, line, expression)]: for each money expression in the lines of a text, the 0-based index of the line it starts on, that line, and the expression.
    The lines in `skip` (indexes) are blanked first, so nothing in them counts. A money word and its figure split across a line break are still found."""
    skip = set(skip)
    body = "\n".join("" if i in skip else ln for i, ln in enumerate(lines))
    out = []
    for a, _, s, _ in hits(body):
        i = body.count("\n", 0, a)
        out.append((i, lines[i], s))
    return out
