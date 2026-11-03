"""T-143 (GATE-M2 legal-nurse major 2, round 2): sentences of a record that no entry excerpt covers. Deterministic code only; no model is read or called.

An entry quotes the sentences its summary rests on. A record sentence the quote leaves out (a pain score, a chief complaint, a baseline-history line, a
patient-stated mechanism, an exam finding, a medication, an interpreter line) vanishes from the letter with no trace, and the letter then looks complete.
`record.uncovered[]` on GET case lists those sentences so the paralegal sees them: each item is the verbatim sentence with its start and end offsets
(offsets into the case text, the same frame as `record.sentences[]`). It is a review aid only: never part of the letter or the internal notes, it changes
no item, state or count.

Rule (round 3, final): EVERY sentence (the shared splitter, sentences.stripped_spans, over the quotable body of the record) that overlaps no live entry's
excerpt is listed, except a line skipped only when BOTH hold: (a) an anchored administrative pattern matches the WHOLE line (`re.fullmatch`, no open tail: a
signature line with a name-shaped tail, a header field with an explicit label, a page / fax / print stamp, a billing line, a closed legal / cost shape), and
(b) the line has no clinical kind (number / pain score, body part, diagnosis or procedure term, negation, patient statement, mechanism). A bare word never removes
a line, and neither does a label that merely starts like a header: "Adjustment to C5-6 performed.", "Date of onset: 01/16/2026.", "Source of history: patient's
son." and "Letter of protection issued; patient states neck pain began after collision." are all listed. One narrow relaxation: a line that ends in a currency
amount and carries a charge cue ("MRI charge: $2,150.") is a line-item charge; its procedure / body-part / count words are the item's label, so only a pain score,
a negation, a patient statement or a mechanism keeps it listed (the amounts engine already carries those figures; listing them would repeat the notes).
Cost and legal sentences without a dollar sign ("No payments posted.", "Letter of protection requested.") are skipped only on the closed shapes in _ADMIN_FULL.
A form answer carries its question: a checkbox or short answer ("Si [ ] No [X].") whose previous sentence ends in "?" is listed as one item with that
question. A duplicate record is skipped (its original carries the entry).

`kinds` is only a hint for the reader (number / body_part / term / negation, possibly empty); it never decides whether a sentence is listed. The hint word
lists below are this module's own because the lexicon has no body-part / diagnosis family yet; they are the one place to move to app/llm/lexicon.yaml
when a researcher adds that family (a card, not an edit here) and nothing depends on their completeness any more.
"""
import re

from app.backend import grounding, sentences

# ---------------------------------------------------------------- administrative lines: anchored whole-line patterns (fullmatch) AND no clinical kind
_I = re.IGNORECASE
_CRED = r"(?:MD|DO|PA-?C|NP|RN|DC|DPT|PT)"
_CAP = r"(?-i:[A-Z][\w'’-]*\.?)"                                   # a capitalized name token or an initial ("Ortiz", "J.")
_PERSON = rf"(?:(?:dr|mr|mrs|ms)\.?\s+)?{_CAP}(?:\s+(?:{_CAP}|de|la|van|von)){{0,4}}(?:,\s*{_CRED}\.?)?"
_PERSON_CRED = rf"(?:(?:dr|mr|mrs|ms)\.?\s+)?{_CAP}(?:\s+(?:{_CAP}|de|la|van|von)){{0,4}},\s*{_CRED}\.?"      # a bare name line needs a credential ("J. Smith, MD")
_ORG = rf"{_CAP}(?:\s+{_CAP}){{0,5}}"
_DATEISH = r"[\dIlOGZ/.\-]{6,12}"
_LOP = r"(?:a\s+)?(?:letter\s+of\s+protection|lop|lien)"
_LOP_STATE = r"(?:requested|issued|on\s+file|in\s+place|signed|provided|received|noted|pending|attached|executed|filed)"
_AMOUNT = r"\(?-?[−-]?\s?\$\s?[\d,]+(?:\.\d+)?\)?"
_ADMIN_FULL = [re.compile(p, _I) for p in (
    # signature / attestation lines: a name-shaped value only
    rf"(?:electronically\s+|e-)?(?:signed|dictated|transcribed|authenticated|firmado)\s*(?:by|por|:)\s*{_PERSON}\.?",
    r"(?:signature|firma)(?:\s+(?:of|de)(?:\s+(?:la|el))?\s+[a-z]{1,15})?\s*:\s*(?:illegible|none|n/a|on\s+file|_+|" + _PERSON + r")\.?",
    rf"{_PERSON_CRED}",
    rf"(?:signed|sworn|dated)\s+{_DATEISH}\.?",
    rf"date\s+(?:written|signed|dictated)\s*:?\s*(?:{_DATEISH})?\.?",
    # header fields: an explicit label, a colon, a plain short value
    r"(?:date\s+of\s+(?:service|birth|visit|report|fax|print)|service\s+date|dob|patient\s+name|name|mrn|account(?:\s+(?:no|number|#))?|fax|phone|tel|npi|facility|"
    r"source|fecha(?:\s+de\s+(?:servicio|nacimiento))?|nombre|tel[eé]fono)\s*[#:]\s*[\w ,'()/#@\-]{0,60}\.?",
    # page / fax / print stamps and dividers
    r"(?:page|p[aá]gina|pg\.?)\s*\d+(?:\s*(?:of|de|/)\s*\d+)?\.?",
    r"(?:faxed|fax\s+received|printed|received|impreso)\s+(?:on\s+|at\s+)?[\d/:\-.\s]+(?:[ap]\.?m\.?)?\.?",
    r"[\W_]*",
    # billing lines (a currency-amount line is _CHARGE_LINE below)
    r"invoice\s+for\s+[\w ,./\-]{0,60}\.?",
    r"(?=[A-Za-z0-9 ,.:#/\-]*\bcpt\b)[A-Za-z0-9 ,.:#/\-]{0,100}",                                                                      # a CPT / form-code line (no brackets or verbs)
    r"(?:contractual\s+)?(?:adjustment|write-?off|discount|ajuste)\b[^\n]{0,60}[-−(]\s?\$?\d[\d,]*\.\d{2}\)?\.?",             # a negative decimal amount, not "C5-6"
    r"(?:itemized\s+)?ledger(?:\s*,?\s*statement\s+date\s*:?\s*[\d/\-.]+)?\.?",
    r"statement\s+date\s*:?\s*[\d/\-.]+\.?",
    r"(?:total\s+charges?|amount\s+(?:paid|due|billed)|(?:balance|saldo)(?:\s+(?:due|forward|remaining|pendiente))?|invoice(?:\s+(?:no|number|#)\s*[\w\-]*)?)\s*[:.]?\s*[$\d,.\s()\-]*\.?",
    r"(?:item\s+\d+[a-z]?|line\s+\d+)\s*:?\s*[\w ,.#/\-]{0,60}?\b(?:total\s+charge|amount\s+paid|signature\s+date|cpt)\b[\w ,.#/\-]{0,80}",
    r"(?:costo|tarifa|cargos?|factura|estado\s+de\s+cuenta)\b[\w ,:$./\-]{0,80}",
    # legal / cost boilerplate without a dollar sign: closed shapes only
    rf"{_LOP}(?:\s+{_LOP_STATE})?(?:\s+(?:to|from|by|with|for)\s+{_ORG})?\.?",
    r"(?:(?:treatment|care|services?|visits?)\s+(?:is|are|was|were)\s+(?:being\s+)?(?:provided|rendered|billed)\s+)?(?:under|on|pursuant\s+to|by)\s+(?:a\s+)?letter\s+of\s+protection\.?",
    r"no\s+(?:payments?|charges?)\s+(?:posted|received|made|recorded)\.?",
    r"(?:the\s+)?(?:cost|fees?|charges?|bill|payments?)\s+(?:of|for)\s+[\w ]{1,50}?\s+(?:was|were|is|are|has\s+been|have\s+been)\s+(?:covered|paid|waived|owed|outstanding|deferred|unpaid)\.?",
    r"(?:paid|payment)\s+(?:for|of)\s+[\w ]{1,50}?\s+(?:out\s+of\s+pocket|in\s+full|by\s+(?:the\s+)?(?:patient|insurance|cash|check))\.?",
    r"(?:patient|pt)\s+(?:paid|owes|owed)\s+(?:the\s+)?(?:clinic|provider|hospital|practice|office|facility)(?:\s+for\s+(?:the\s+)?(?:care|treatment|services?|visits?))?\.?",
)]
# A line that ends in a currency amount ("MRI charge: $2,150.", "Total charges $1,567.05.") is a line-item charge: the procedure or body-part words in it are the item's
# label, not a clinical statement, so only a pain score, a negation, a patient statement or a mechanism keeps it listed. It needs a charge cue word to count.
_CHARGE_LINE = re.compile(rf"[\w ,.:#/&()\-]{{0,80}}?(?:{_AMOUNT}[^$\n]{{0,25}}?){{1,4}}(?:\s+(?:per|each)\s+\w+)?\.?", _I)
_CHARGE_CUE = re.compile(r"\b(?:charges?|fees?|costs?|billed|billing|rate|price|total|statement|invoice|paid|payments?|balance|due|owed|adjustment|discount|write-?off|"
                         r"costo|tarifa|cargos?|factura|saldo|ajuste|per|each)\b|:\s*" + _AMOUNT + r"\.?\s*$", _I)
_PAIN_SCORE = re.compile(r"(?<![\d/])\d{1,2}\s*/\s*10(?![\d/])")
_NO_PAYMENT = re.compile(r"no\s+(?:payments?|charges?)\s+(?:posted|received|made|recorded)\.?", _I)


def is_administrative(sentence: str) -> bool:
    """True only when BOTH hold: (a) an anchored administrative pattern matches the WHOLE line (`fullmatch`, no open tail), and (b) the line has no clinical kind
    (number / pain score, body part, diagnosis or procedure term, negation, patient statement, mechanism). Every other line is listed."""
    s = sentence.strip()
    kinds = None
    if _CHARGE_LINE.fullmatch(s) and _CHARGE_CUE.search(s):
        kinds = [k for k in clinical_kinds(s) if k not in ("body_part", "term", "number")] + (["number"] if _PAIN_SCORE.search(s) else [])
    elif any(p.fullmatch(s) for p in _ADMIN_FULL):
        kinds = clinical_kinds(s)
        if _NO_PAYMENT.fullmatch(s):
            kinds = [k for k in kinds if k != "negation"]    # "No payments posted." is a ledger statement, not a clinical denial
    return kinds is not None and not kinds


# ---------------------------------------------------------------- clinical content
_NUMBER_UNITS = (r"mg|mcg|ml|mm|cm|mph|lbs?|kg|bpm|mmhg|%|°|degrees?|weeks?|wks?|days?|months?|visits?|sessions?|reps?|"
                 r"semanas?|d[ií]as?|meses|sesiones|grados|pulgadas|inches")
_NUMBER = re.compile(rf"(?<![\d/])\d{{1,2}}\s*/\s*10(?![\d/])|(?<![\d/])\d+(?:\.\d+)?\s*/\s*5(?![\d/])|(?<![\w/-])\d+(?:\.\d+)?\s*(?:{_NUMBER_UNITS})(?![A-Za-z])", re.IGNORECASE)

_BODY = re.compile(
    r"\b(?:neck|back|head|shoulders?|arms?|forearms?|elbows?|wrists?|hands?|fingers?|thumbs?|hips?|legs?|thighs?|knees?|ankles?|feet|foot|toes?|chest|ribs?|"
    r"abdomen|abdominal|spine|spinal|cervical|thoracic|lumbar|sacral|sacrum|coccyx|jaw|skull|scalp|face|groin|pelvis|pelvic|rotator|"
    r"cuello|espalda|cabeza|hombros?|brazos?|codos?|mu[nñ]ecas?|manos?|dedos?|caderas?|piernas?|rodillas?|tobillos?|pies?|pecho|costillas?|"
    r"abdomen|columna|lumbar|cervical|mand[ií]bula|pelvis)\b", re.IGNORECASE)

_CLINICAL_TERM = re.compile(
    r"\b(?:pain|ache|aching|stiffness|soreness|sore|tenderness|tender|numbness|tingling|weakness|swelling|bruising|spasms?|headaches?|dizziness|nausea|"
    r"fatigue|radiating|radiates|burning|"
    r"strain|sprain|fractures?|concussion|contusion|laceration|whiplash|herniation|herniated|protrusion|bulge|stenosis|radiculopathy|"
    r"dislocation|tear|arthritis|degenerative|diagnos\w+|dx|"
    r"mri|ct|x-?ray|ultrasound|emg|injections?|surgery|surgical|fusion|therapy|physical\s+therapy|chiropractic|medications?|prescribed|rx|"
    r"dolor|rigidez|entumecimiento|hormigueo|debilidad|hinchaz[oó]n|esguince|fractura|contusi[oó]n|conmoci[oó]n|hernia|"
    r"resonancia|radiograf[ií]a|inyecci[oó]n|cirug[ií]a|fisioterapia|terapia|medicamentos?)\b", re.IGNORECASE)

_STATEMENT = re.compile(
    r"\b(?:patient|pt|pacient[ea]|she|he|they|el\s+paciente|la\s+paciente)\s+(?:states?|stated|reports?|reported|says|said|denies|denied|complains?|complained|describes|described|"
    r"refiere|dice|reporta|niega|relata)\b|\bper\s+(?:the\s+)?(?:patient|pt|paciente)\b|\baccording\s+to\s+(?:the\s+)?patient\b|\brefiere\b", re.IGNORECASE)
_MECHANISM = re.compile(
    r"\b(?:collision|crash(?:ed)?|struck|rear-?ended|mvc|mva|accident(?:e)?s?|fell|fall|slipped|tripped|hit\s+by|impact|onset|began|started|choque|atropell\w*|ca[i\u00ed]da)\b",
    re.IGNORECASE)

_NEGATION_ES = re.compile(r"\b(?:niega|niegan|sin|ning[uú]n[ao]?|negativo)\b", re.IGNORECASE)


def clinical_kinds(sentence: str) -> list:
    """Hint only: which kinds of clinical content the sentence carries, in a fixed order: number, body_part, term, negation, statement, mechanism (empty = none)."""
    kinds = []
    if _NUMBER.search(sentence):
        kinds.append("number")
    if _BODY.search(sentence):
        kinds.append("body_part")
    if _CLINICAL_TERM.search(sentence):
        kinds.append("term")
    if grounding.has_negation(sentence, extra=True) or _NEGATION_ES.search(sentence):
        kinds.append("negation")
    if _STATEMENT.search(sentence):
        kinds.append("statement")
    if _MECHANISM.search(sentence):
        kinds.append("mechanism")
    return kinds


# ---------------------------------------------------------------- coverage
_ANSWER = re.compile(r"(?:s[i\u00ed]|no|yes|n/a|[\[(][^\]\n)]{0,3}[\])])\b|[\[(][^\]\n)]{0,3}[\])]", _I)


def _overlaps(a: int, b: int, spans: list) -> bool:
    return any(a < e and s < b for s, e in spans)


def for_record(body: str, base: int, excerpts: list) -> list:
    """Uncovered sentences of one record. `body` is the quotable body (present.quote_body), `base` its offset in the case text,
    `excerpts` the live entries' quotes for this record. [{text, start, end, kinds}] in record order."""
    covered = [sp for ex in excerpts if ex for sp in grounding.locate_all(body, ex)]
    spans = sentences.stripped_spans(body)
    out = []
    for i, (a, b) in enumerate(spans):
        text = body[a:b]
        if _overlaps(a, b, covered) or is_administrative(text):
            continue
        if i and _ANSWER.match(text) and body[spans[i - 1][0]:spans[i - 1][1]].endswith("?"):
            qa = spans[i - 1][0]                      # a form answer carries its question (contiguous verbatim slice)
            if out and out[-1]["start"] == base + qa:
                out.pop()                             # the question was listed on its own: one item instead of two
            a = qa
            text = body[a:b]
        out.append({"text": text, "start": base + a, "end": base + b, "kinds": clinical_kinds(text)})
    return out


def attach(record_views: list, entries: list, quote_body) -> None:
    """Add `uncovered` to every record view (in place). `entries` are the entry views (a rejected one covers nothing: it is a tray item, not an entry);
    `quote_body` is present.quote_body. A record with no locatable quotable body, and a duplicate, get []."""
    live = [e for e in entries if e.get("state") != "rejected"]
    for rv in record_views:
        rv["uncovered"] = []
        if rv.get("duplicate_of"):
            continue
        base, body, why_none = quote_body(rv["text"])
        if why_none or not body:
            continue
        quotes = [e.get("excerpt") for e in live if rv["id"] in (e.get("record_ids") or [])]
        rv["uncovered"] = [{**u, "start": rv["char_start"] + u["start"], "end": rv["char_start"] + u["end"]}
                           for u in for_record(body, base, quotes)]
