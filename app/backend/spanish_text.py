"""Spanish-language records, code half (D-042, T-085): the quote is the original Spanish; the English summary is an AI translation.

Pure deterministic code: no model, no network, no app.llm import (tests/unit/test_spanish.py scans it).
The D-034 token checks need the English summary compared with a SPANISH quote, so this module maps the Spanish
words that carry the checked tokens (months, right/left, negations, hedges, who-said-it, approximations, number words, Spanish number
formats) onto the English tokens grounding.py already checks. It never edits text and never decides truth: a doubtful summary only
gets SUMMARY_TOKEN_NOT_IN_EXCERPT / SUMMARY_DROPS_QUALIFIER, which route it to the paralegal (fail toward flagging).

`module_for(lang)` returns `grounding` for English and this module for Spanish; both expose new_tokens, dropped_qualifiers and check_summary.
"""
import re
import unicodedata

from app.backend import grounding, language

LABEL = "AI translation"
LABEL_EDITED = "Translation (edited by reviewer)"
REVIEW_LABEL = "AI translation — check against the original"      # D-050: shown on every needs_review item from a Spanish or unidentified-language record
LABEL_PREPARED = "Prepared translation"      # D-069: the twins for an item whose first answer is a prepared one (no AI wrote it)
REVIEW_LABEL_PREPARED = "Prepared translation — check against the original"


def fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


# ---------------------------------------------------------------- vocabulary (folded: no accents, lower case)
MONTHS_ES = {"enero": "january", "febrero": "february", "marzo": "march", "abril": "april", "mayo": "may", "junio": "june", "julio": "july",
             "agosto": "august", "septiembre": "september", "setiembre": "september", "octubre": "october", "noviembre": "november",
             "diciembre": "december", "ene": "january", "feb": "february", "mar": "march", "abr": "april", "may": "may", "jun": "june",
             "jul": "july", "ago": "august", "sep": "september", "sept": "september", "set": "september", "oct": "october", "nov": "november",
             "dic": "december"}
_SIDES = {"derecho": "right", "derecha": "right", "derechos": "right", "derechas": "right", "dcho": "right", "dcha": "right", "der": "right",
          "izquierdo": "left", "izquierda": "left", "izquierdos": "left", "izquierdas": "left", "izq": "left", "izqdo": "left", "izqda": "left",
          "bilateral": "bilateral", "bilaterales": "bilateral"}
_NEG_CUES = frozenset("no sin niega niegan nego negativo negativa negativos negativas ningun ninguna ninguno ningunos ningunas nunca tampoco "
                      "ausencia ausente ausentes descarta descartan descartado descartada jamas carece carecen carente nada ni".split())
_HEDGE_CUES = frozenset("posible posibles posiblemente probable probables probablemente podria podrian pudiera pudieran sugiere sugieren "
                        "sugerente sugestivo sugestiva sospecha sospechoso parece parecen aparente aparentemente presunto presunta "
                        "correlacionar correlacion descartar quiza quizas impresiona eventual eventualmente incierto incierta inciertos inciertas dudoso dudosa "
                        "dudosos dudosas presuntamente presuntos presuntas indeterminado indeterminada indeterminados indeterminadas".split())
_HEDGE_PHRASES = re.compile(r"compatible\s+con|al\s+parecer|tal\s+vez|impresiona\s+como|no\s+concluyente|puede\s+(?:ser|representar|corresponder|tratarse)|"
                            r"cabe\s+la\s+posibilidad|correlaci[oó]n\s+cl[ií]nica|correlacionar\s+con", re.IGNORECASE)
_SELF_CUES = frozenset("refiere refirio refieren manifiesta manifesto manifiestan relata relato reporta reporto comenta comento dice dijo "
                       "acusa afirma menciono menciona informa niega niegan aqueja aquejan alega alegan senala senalan expresa expresan verbaliza "
                       "verbalizo califico califica calificaron calificado describio describe".split())
_SELF_PHRASES = re.compile(r"seg[uú]n\s+(?:el|la)\s+paciente|seg[uú]n\s+refiere|se\s+queja\s+de|paciente\s+indica|la\s+paciente\s+indica|"
                           r"motivo\s+de\s+consulta|a\s+decir\s+(?:del|de\s+la|de\s+los|de\s+las)\b", re.IGNORECASE)
_NEG_PHRASES = re.compile(r"libre\s+de|sin\s+evidencia", re.IGNORECASE)
# 'no se descarta' = NOT ruled out (a hedge); 'se descarta' / 'descartado' = ruled out (a negation). They point opposite ways, so each is
# checked on its own and neither may satisfy the other's rule.
_NOT_RULED_OUT = re.compile(r"\bno\s+(?:se\s+)?(?:(?:puede|pueden|pudo|ha|han|logra|esta|estan)\s+)?(?:ser\s+)?descart\w*|\bno\s+descart\w*|\bsin\s+descartar|"
                            r"\b(?:a|por)\s+descartar|\bdescartar\b|\baun\s+no\s+(?:se\s+)?(?:ha\s+)?descart\w*", re.IGNORECASE)
_RULED_OUT = re.compile(r"\bdescart(?:a|an|ado|ada|ados|adas|o)\b", re.IGNORECASE)
_EN_NOT_RULED_OUT = re.compile(r"\b(?:cannot|can't|can not|could not|not|unable to|no)\s+(?:yet\s+)?(?:be\s+)?(?:fully\s+|completely\s+|entirely\s+)?(?:ruled\s+out|excluded|"
                               r"rule\s+out|exclude|dismissed)\b|\bpossib\w+|\bmay\b|\bmight\b|\bcould\b|\bto\s+(?:be\s+)?(?:rule|ruled|exclude|excluded)\b|\brule\s+out\b|"
                               r"\bremains?\s+(?:a\s+)?(?:concern|possib\w+|open)\b|\bdifferential\b|\bperhaps\b|\bmaybe\b|\blikely\b|\bprobabl\w+", re.IGNORECASE)
_EN_RULED_OUT = re.compile(r"\b(?:ruled\s+out|excluded|rules?\s+out|dismissed|negative\s+for|no\s+(?:evidence|sign)s?\s+of|absent)\b", re.IGNORECASE)
_EN_SAYS_NOT_RULED_OUT = re.compile(r"\b(?:cannot|can't|can not|could not|not|unable to)\s+(?:yet\s+)?(?:be\s+)?(?:fully\s+|completely\s+|entirely\s+)?(?:ruled\s+out|excluded|dismissed)\b", re.IGNORECASE)
_APPROX_CUES = frozenset("aprox aproximadamente aproximado aproximada aproximados aproximadas alrededor estimado estimada estimados estimadas".split())
_APPROX_PHRASES = re.compile(r"cerca\s+de|m[aá]s\s+o\s+menos|\bunos\s+\d|\bunas\s+\d|~", re.IGNORECASE)
# The English side of the D-034 checks (negation, hedge, attribution, approximation, side words) is read from the lexicon through grounding's views
# (T-105 r2); this module keeps only the SPANISH cue lists above.

_UNITS = {"cero": 0, "un": 1, "uno": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
          "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16, "diecisiete": 17, "dieciocho": 18,
          "diecinueve": 19, "veinte": 20, "veintiuno": 21, "veintiun": 21, "veintiuna": 21, "veintidos": 22, "veintitres": 23,
          "veinticuatro": 24, "veinticinco": 25, "veintiseis": 26, "veintisiete": 27, "veintiocho": 28, "veintinueve": 29}
_TENS = {"treinta": 30, "cuarenta": 40, "cincuenta": 50, "sesenta": 60, "setenta": 70, "ochenta": 80, "noventa": 90}
_HUNDREDS = {"cien": 100, "ciento": 100}
_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def _words(text: str) -> list:
    return [fold(w) for w in _WORD.findall(text or "")]


# ---------------------------------------------------------------- numbers
_ES_THOUSANDS = re.compile(r"(?<![\d.,])\d{1,3}(?:\.\d{3})+(?:,\d+)?(?![\d])")
_ES_DECIMAL = re.compile(r"(?<![\d.,])\d+,\d{1,2}(?![\d])")


def _number_words(text: str) -> set:
    """Digit strings for spelled-out Spanish numbers ('tres' -> '3', 'treinta y cinco' -> '35' and '30', '5')."""
    ws = _words(text)
    out, i = set(), 0
    while i < len(ws):
        w = ws[i]
        if w in _UNITS:
            out.add(str(_UNITS[w]))
        elif w in _HUNDREDS:
            out.add(str(_HUNDREDS[w]))
        elif w in _TENS:
            out.add(str(_TENS[w]))
            if i + 2 < len(ws) and ws[i + 1] == "y" and ws[i + 2] in _UNITS and 1 <= _UNITS[ws[i + 2]] <= 9:
                out.add(str(_TENS[w] + _UNITS[ws[i + 2]]))
        i += 1
    return out


_WRITTEN = re.compile(r"^(?:[a-z]+,?\s+)?(\d{1,2})(?:\s+de\s+|\s*[-/.\s]\s*)([a-z]{3,10})\.?(?:\s+de\s+|\s*,?\s*[-/\s]\s*)(\d{4}|\d{2})$")


def parse_written_date(raw: str):
    """ISO date for a Spanish written date ('14 de mayo de 2026', 'jueves 14 de mayo de 2026', '14-may-26', '12-ago-2026'), else None.
    Day first, month spelled out, so it is never ambiguous. A two-digit year above 40 is left unread (could be 19yy or 20yy)."""
    import datetime as dt
    m = _WRITTEN.match(" ".join(fold(raw or "").split()))
    if not m or m.group(2) not in MONTHS_ES:
        return None
    y = int(m.group(3))
    if len(m.group(3)) == 2:
        if y > 40:
            return None
        y += 2000
    try:
        return dt.date(y, grounding._MONTHS.index(MONTHS_ES[m.group(2)]) + 1, int(m.group(1))).isoformat()
    except ValueError:
        return None


def _canonical_spanish_numbers(text: str) -> set:
    """Spanish-format figures as English digit strings: '1.250,00' -> '1250.00', '37,5' -> '37.5', '1.250' -> '1250'."""
    out = set()
    for m in _ES_THOUSANDS.finditer(text):
        out.add(m.group(0).replace(".", "").replace(",", "."))
    for m in _ES_DECIMAL.finditer(text):
        out.add(m.group(0).replace(",", "."))
    return {grounding._num_tokens(x)[0] if grounding._num_tokens(x) else x for x in out}


def _date_months(text: str, date_iso: str) -> set:
    """English month names the excerpt supports: written Spanish months, and the month of a numeric date read day-first (the Spanish
    convention; month-first only when the day-first reading is impossible). A numeric date is never read both ways."""
    ms = {MONTHS_ES[w] for w in _words(text) if w in MONTHS_ES}
    for m in re.finditer(r"(?<!\d)(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})(?!\d)", text):
        a, b = int(m.group(1)), int(m.group(2))
        mo = b if 1 <= b <= 12 and 1 <= a <= 31 else a if 1 <= a <= 12 else None
        if mo:
            ms.add(grounding._MONTHS[mo - 1])
    return ms


def _allowed_numbers(excerpt: str, label: str, date_iso: str) -> set:
    allowed = grounding._allowed_numbers(excerpt, label, date_iso)
    return allowed | _canonical_spanish_numbers(excerpt) | _number_words(excerpt)


def _cue_set(excerpt: str, cues, phrases=None) -> bool:
    return any(w in cues for w in _words(excerpt)) or bool(phrases and phrases.search(excerpt))


def allowed_english_words(excerpt: str) -> set:
    """left/right/no/not/without words the Spanish excerpt supports (plus those of any English words mixed into it). A Spanish negation cue also
    supports any English negation word (grounding.is_negation_word); that part is applied in new_tokens, not enumerated here."""
    ws = _words(excerpt)
    ok = grounding.side_neg_words(excerpt)
    ok |= {_SIDES[w] for w in ws if w in _SIDES}
    if "bilateral" in ok:
        ok.add("bilaterally")
    return ok


def _spanish_negation_cue(excerpt: str) -> bool:
    ws = _words(excerpt)
    return any(w in _NEG_CUES for w in ws) or bool(_NEG_PHRASES.search(fold(excerpt)) or _NOT_RULED_OUT.search(fold(excerpt)))


def check_excerpt(record_text: str, excerpt: str) -> list:
    """grounding.check_excerpt on the ORIGINAL Spanish text, plus the Spanish hedge rule: a hedge sentence right after the quote
    ('Compatible con contractura.') must travel with it (R-TL-8). The match itself is the same whitespace-normalised substring test."""
    from app.backend import sentences as S
    reasons = grounding.check_excerpt(record_text, excerpt)
    if "GROUNDING_EXCERPT_NOT_VERBATIM" in reasons or "EXCERPT_OMITS_QUALIFIER" in reasons:
        return reasons
    spans = grounding.locate_all(record_text, excerpt)
    units = S.stripped_spans(record_text)
    starts, ends = {a for a, _ in units}, {b for _, b in units}
    s, e = next((sp for sp in spans if sp[0] in starts and sp[1] in ends), spans[0])
    touched = [i for i, (a, b) in enumerate(units) if a < e and b > s]
    nxt = (touched[-1] + 1) if touched else len(units)
    if nxt < len(units) and is_hedge_unit(record_text[units[nxt][0]:units[nxt][1]]):
        reasons.append("EXCERPT_OMITS_QUALIFIER")
    return reasons


# ---------------------------------------------------------------- the D-034 checks, Spanish quote vs English summary
def new_tokens(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
    """Numbers, dollar figures, months and left/right/no/not/without in the English summary that the Spanish quote, the source label or
    the parsed date do not support. Same contract as grounding.new_tokens."""
    allowed = _allowed_numbers(excerpt, label, date_iso)
    out = [t for t in grounding._num_tokens(summary) if t not in allowed]
    ok = allowed_english_words(excerpt)
    neg_ok = _spanish_negation_cue(excerpt)
    out += [w for w in grounding.side_neg_words(summary, keep_order=True) if w not in ok and not (neg_ok and grounding.is_negation_word(w))]
    out += [w for w in added_qualifier_tokens(summary, excerpt) if w not in out]
    src = fold(excerpt + " " + label)
    months = _date_months(excerpt, date_iso) | {grounding._MONTHS[int(m.group(1)) - 1]
                                                for m in [re.match(r"\d{4}-(\d{2})", date_iso or "")] if m}
    months |= {MONTHS_ES[w] for w in _words(label) if w in MONTHS_ES}
    out += [x.lower() for x in grounding._MONTH_RX.findall(summary) if x.lower() not in months and x.lower() not in src]
    return list(dict.fromkeys(out))


def added_qualifier_tokens(summary: str, excerpt: str) -> list:
    """D-047 for a Spanish quote: attribution, hedge or approximation words in the English summary when the Spanish (or mixed English) quote has no qualifier
    of that kind. Same contract and the SAME word lists as grounding.added_qualifier_tokens (the lexicon's added_qualifier family, T-105); this module only
    adds the Spanish cue lists for the quote side."""
    folded = fold(excerpt)
    return grounding.added_qualifier_tokens(summary, excerpt, quote_has={
        "attribution": _cue_set(excerpt, _SELF_CUES, _SELF_PHRASES),
        "hedge": _cue_set(excerpt, _HEDGE_CUES, _HEDGE_PHRASES) or bool(_NOT_RULED_OUT.search(folded)),
        "approximation": _cue_set(excerpt, _APPROX_CUES, _APPROX_PHRASES)})


def _neg_hit(ws: list) -> bool:
    """A Spanish negation cue in the folded word list. 'sin embargo' (however), 'sin duda' (no doubt) and 'no obstante' are not negations."""
    for i, w in enumerate(ws):
        if w not in _NEG_CUES:
            continue
        nxt = ws[i + 1] if i + 1 < len(ws) else ""
        if (w == "sin" and nxt in ("embargo", "duda")) or (w == "no" and nxt == "obstante"):
            continue
        return True
    return False


def dropped_qualifiers(summary: str, excerpt: str) -> list:
    """Qualifier kinds in the Spanish quote that the English summary lost or turned round: hedge, self_report, negation, laterality, approx
    (D-022). 'No se descarta X' (X is not ruled out) is a hedge; 'Se descarta X' (X is ruled out) is a negation; a summary that says the
    opposite of the quote fails the one it contradicts."""
    out = []
    folded = fold(excerpt)
    not_ruled = bool(_NOT_RULED_OUT.search(folded))
    rest = _NOT_RULED_OUT.sub(" ", folded)                      # the quote with its 'not ruled out' phrases taken out
    ruled = bool(_RULED_OUT.search(rest))
    ex_words = _words(rest)
    hedge_q = _cue_set(rest, _HEDGE_CUES, _HEDGE_PHRASES) or bool(grounding.hedge_ids(excerpt) and not not_ruled)
    if hedge_q and not (grounding.has_hedge(summary)):
        out.append("hedge")
    if not_ruled:           # 'cannot be excluded' / 'possible' is right; 'ruled out' / 'excluded' says the opposite
        if not _EN_NOT_RULED_OUT.search(summary) or _EN_RULED_OUT.search(_EN_NOT_RULED_OUT.sub(" ", summary)):
            out.append("hedge")
    if (_cue_set(excerpt, _SELF_CUES, _SELF_PHRASES) or grounding.attribution_in_quote(excerpt)) and not grounding.attribution_carried(summary):
        out.append("self_report")
    neg_q = _neg_hit(ex_words) or bool(_NEG_PHRASES.search(folded))
    neg_q = neg_q or grounding.has_negation(excerpt, extra=True, ignore=("no",))     # 'no' is the Spanish cue list's word ("No se descarta")
    if neg_q and not grounding.has_negation(summary, extra=True):
        out.append("negation")
    if ruled and _EN_SAYS_NOT_RULED_OUT.search(summary):          # 'Se descarta fractura' read as 'fracture cannot be excluded'
        out.append("negation")
    sides = {_SIDES[w] for w in ex_words if w in _SIDES} | grounding.lateral_words(excerpt)
    if sides - grounding.lateral_words(summary):
        out.append("laterality")
    if (_cue_set(excerpt, _APPROX_CUES, _APPROX_PHRASES) or grounding.approximation_hits(excerpt)) and not (
            grounding.approximation_hits(summary) or grounding.aq("approximation_word").search(summary)):
        out.append("approx")
    return list(dict.fromkeys(out))


def check_summary(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
    reasons = []
    if new_tokens(summary, excerpt, label, date_iso):
        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
    if dropped_qualifiers(summary, excerpt):
        reasons.append("SUMMARY_DROPS_QUALIFIER")
    return reasons


def module_for(lang: str):
    """The module whose new_tokens / dropped_qualifiers / check_summary apply to a record of this language. Spanish and an uncertain
    language get this module; the English token checks are only for a record that is confidently English."""
    import sys
    return sys.modules[__name__] if language.is_translated(lang) else grounding


# ---------------------------------------------------------------- hedge unit (excerpt-end rule) for Spanish quotes
def is_hedge_unit(unit_text: str) -> bool:
    """A Spanish sentence that is only a hedge on the sentence before it ('Compatible con contractura muscular.'). Used with the
    English lexicon test by grounding.check_excerpt callers that know the record is Spanish."""
    return _cue_set(unit_text, _HEDGE_CUES, _HEDGE_PHRASES) or bool(_NOT_RULED_OUT.search(fold(unit_text)))




def translation_info(lang: str, edited: bool = False, prep: bool = False) -> dict:
    """The block entries carry (api.md): the UI shows `label` next to the summary. `prep` (D-069): the translation is a prepared answer's, so the labels say prepared, not AI."""
    return {"source_language": lang, "source_language_name": language.NAMES.get(lang, lang),
            "label": LABEL_EDITED if edited else (LABEL_PREPARED if prep else LABEL),
            "review_label": REVIEW_LABEL_PREPARED if prep else REVIEW_LABEL, "summary_is_translation": True, "quote_is_original": True}
