"""Grounding verifier (R-TL-2, R-TL-8, R-TL-10, R-RV-9; ADR-005/012/016/017). Deterministic: a failing quote is never repaired.

normalize/locate: whitespace-normalised substring match with a normalised->raw index map, so offsets are absolute in the raw text.
check_excerpt: reason codes for a model/user excerpt against its record. check_summary: token and dropped-qualifier checks.
"""
import functools
import pathlib
import re

import yaml

_LEXICON = pathlib.Path(__file__).resolve().parents[1] / "llm" / "lexicon.yaml"
_WS = re.compile(r"\s+")


# ---------------------------------------------------------------- normalise / locate
def normalize(text: str) -> str:
    return _WS.sub(" ", text).strip()


def _norm_with_map(text: str):
    """(normalised, idx) where idx[k] is the raw offset of normalised char k."""
    out, idx, prev_space, started = [], [], False, False
    for i, ch in enumerate(text):
        if ch.isspace():
            if started:
                prev_space = True
            continue
        if prev_space:
            out.append(" ")
            idx.append(i - 1)
            prev_space = False
        out.append(ch)
        idx.append(i)
        started = True
    return "".join(out), idx


def locate_all(record_text: str, excerpt: str) -> list:
    """Every (start, end) raw span whose whitespace-normalised text equals the normalised excerpt."""
    ex = normalize(excerpt)
    if not ex:
        return []
    norm, idx = _norm_with_map(record_text)
    spans, pos = [], norm.find(ex)
    while pos != -1:
        spans.append((idx[pos], idx[pos + len(ex) - 1] + 1))
        pos = norm.find(ex, pos + 1)
    return spans


def locate(record_text: str, excerpt: str):
    """First (start, end) raw span of the excerpt in the record, or None (offset lookup failed: HIGHLIGHT_NOT_FOUND)."""
    spans = locate_all(record_text, excerpt)
    return spans[0] if spans else None


# ---------------------------------------------------------------- lexicon (hedge / attribution sets)
@functools.lru_cache(maxsize=1)
def _lexicon() -> dict:
    data = yaml.safe_load(_LEXICON.read_text())
    entries = data["entries"] if isinstance(data, dict) and "entries" in data else data
    hedges, selfrep = {}, {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        if "pattern" not in e:
            if e.get("hedge") or e.get("self_report"):
                raise ValueError(f"lexicon entry {e.get('id')} is a hedge/self_report entry without a pattern")
            continue
        if e.get("hedge"):
            hedges[e["id"]] = re.compile(e["pattern"], re.IGNORECASE)
        if e.get("self_report"):
            selfrep[e["id"]] = re.compile(e["pattern"], re.IGNORECASE)
    scope = (data.get("self_report_scope") or {}).get("exclude_sentence") if isinstance(data, dict) else None
    return {"hedge": hedges, "self_report": selfrep, "self_report_exclude": re.compile(scope, re.IGNORECASE) if scope else None}


def hedge_ids(text: str) -> set:
    return {i for i, rx in _lexicon()["hedge"].items() if rx.search(text)}


def is_hedge_unit(unit_text: str) -> bool:
    return bool(hedge_ids(unit_text))


# ---------------------------------------------------------------- excerpt check
def check_excerpt(record_text: str, excerpt: str) -> list:
    """[] when clean. Not verbatim -> ['GROUNDING_EXCERPT_NOT_VERBATIM'] (rejected, nothing else is evaluated)."""
    from app.backend import sentences as S
    spans = locate_all(record_text, excerpt)
    if not spans:
        return ["GROUNDING_EXCERPT_NOT_VERBATIM"]
    reasons = []
    units = S.stripped_spans(record_text)
    starts, ends = {a for a, _ in units}, {b for _, b in units}
    aligned = [sp for sp in spans if sp[0] in starts and sp[1] in ends]
    if not aligned:
        reasons.append("EXCERPT_NOT_WHOLE_SENTENCE")
    s, e = (aligned or spans)[0]
    # a hedge unit immediately after the last unit the excerpt touches must travel with it (R-TL-8, D-021)
    touched = [i for i, (a, b) in enumerate(units) if a < e and b > s]
    nxt = (touched[-1] + 1) if touched else len(units)
    if nxt < len(units):
        a, b = units[nxt]
        if is_hedge_unit(record_text[a:b]):
            reasons.append("EXCERPT_OMITS_QUALIFIER")
    return reasons


def check_amount(record_text: str, raw_amount: str) -> list:
    """An amount the model (or an edit) reports must appear in the record exactly as written (R-CH-1). Never auto-corrected:
    '$1,2OO' is found as written, the 'fixed' '$1,200' is not. A longer figure does not vouch for a shorter one ('$185' vs '$1,850')."""
    raw = (raw_amount or "").strip()
    if raw:
        for m in re.finditer(re.escape(raw), record_text):
            before = record_text[m.start() - 1] if m.start() else ""
            tail = record_text[m.end():m.end() + 2]
            if not before.isdigit() and not re.match(r"\d|[,.]\d", tail):
                return []
    return ["GROUNDING_AMOUNT_NOT_IN_TEXT"]


# ---------------------------------------------------------------- summary checks
_NUM = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")
# One source of truth for side and negation words (D-047, T-105 r2): app/llm/lexicon.yaml code_lists.added_qualifier (side, negation_word, negation_extra,
# negation_ruled_out, negation_contraction). The edit route, the generator's code check, the export gate and the Spanish helper all read it through the
# views below; no word list lives in code. Contractions (didn't, can't) count as a negation word of their own.
_MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
           "november", "december"]
_MONTH_RX = re.compile(r"\b(" + "|".join(m for m in _MONTHS if m != "may") + r")\b", re.IGNORECASE)


def _num_tokens(text: str) -> list:
    out = []
    for m in _NUM.finditer(text):
        t = m.group(0).replace(",", "")
        out.append(str(int(t)) if t.isdigit() else t)
    return out


def _allowed_numbers(excerpt: str, label: str, date_iso: str) -> set:
    allowed = set(_num_tokens(excerpt)) | set(_num_tokens(label))
    allowed |= {str(int(p)) for p in re.findall(r"\d+", date_iso or "")}
    return allowed


def side_neg_words(text: str, keep_order: bool = False):
    """The side and negation words in `text` (lower case): left, right, bilateral, no, not, none, never, without, denies, negative, absent, neither, nor, n't forms."""
    ws = [re.sub(r"\s+", " ", m.group(0)).lower() for m in view("side", "negation_word", "negation_extra", "negation_contraction").finditer(text.replace("\u2019", "'"))]
    return ws if keep_order else set(ws)


def _canon_neg(w: str) -> str:
    """didn't / wasn't / isn't are the word 'not' (so "Did not tolerate" and "Didn't tolerate" are the same statement)."""
    return "not" if w.endswith("n't") else w


def new_tokens(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
    """Numbers, dollar figures, dates (month names), side and negation words (side_neg_words) and attribution, hedge or approximation words
    (added_qualifier_tokens) in the summary that are in none of the
    excerpt, the source label or the parsed date. Digits are compared as digit runs, so a label digit can mask a changed
    score ('visit 8' vs 'pain 8/10'): that gap belongs to judge 1 (SE5)."""
    summary, excerpt = summary.replace("\u2019", "'"), excerpt.replace("\u2019", "'")        # a curly apostrophe (Word, PDF) is an apostrophe
    allowed = _allowed_numbers(excerpt, label, date_iso)
    out = [t for t in _num_tokens(summary) if t not in allowed]
    ex_words = {_canon_neg(w) for w in side_neg_words(excerpt)}
    neg_text = _aq()["inability"].sub(" ", summary) if _aq()["inability"].search(excerpt) else summary      # "cannot" / "could not" / "can't" say what "unable to" says
    out += [w for w in side_neg_words(neg_text, keep_order=True) if _canon_neg(w) not in ex_words]
    out += [w for w in added_qualifier_tokens(summary, excerpt) if w not in out]
    src = (excerpt + " " + label).lower()
    month = ""
    m = re.match(r"\d{4}-(\d{2})", date_iso or "")
    if m:
        month = _MONTHS[int(m.group(1)) - 1]
    out += [x.lower() for x in _MONTH_RX.findall(summary) if x.lower() not in src and x.lower() != month]
    return list(dict.fromkeys(out))


def has_hedge(text: str) -> bool:
    """A hedge anywhere in the text: the older hedge entries, the lexicon's hedge family, or the carried-only extras (cannot, suggest*)."""
    return bool(hedge_ids(text) or view("hedge", "hedge_carried").search(text))


def hedge_in_quote(text: str) -> bool:
    """A hedge in the QUOTE that a summary must carry (D-022): the older hedge entries or the lexicon's hedge family ('cannot' is an inability, not a hedge)."""
    return bool(hedge_ids(text) or aq("hedge").search(text))


def attribution_in_quote(text: str) -> bool:
    """The quote attributes the statement to someone ('Patient states', 'complained of', 'per patient', 'according to the patient'): a summary must carry it (D-022)."""
    return bool(aq("attribution").search(text))


def attribution_carried(text: str) -> bool:
    """Lenient, for the summary side: any attribution wording at all counts as carrying it (D-040: nothing labels who is speaking)."""
    return bool(view("attribution", "attribution_bare_verb", "attribution_word").search(text))


def approximation_hits(text: str) -> list:
    """Approximation words in the text; 'counseled about 3 exercises' (about as a preposition) is not one."""
    out = []
    for m in aq("approximation").finditer(text):
        w = _clean(m)
        if w.split()[0] in ("about", "around") and aq("approximation_preposition_context").search(text[max(0, m.start() - 40):m.start()]):
            continue
        out.append(w)
    return out


def negation_words(text: str) -> list:
    """The negation words in the text (lower case, in order); every contraction is the word 'not'."""
    return ["not" if w.endswith("n't") else w for w in (re.sub(r"\s+", " ", m.group(0)).lower() for m in
                                                        view("negation_word", "negation_contraction").finditer(text.replace("\u2019", "'")))]


def has_negation(text: str, *, extra: bool = False, ignore: tuple = ()) -> bool:
    """Any negation wording; extra=True also accepts the looser words (absence of, lacks, free of, nothing, unremarkable, ruled out).
    `ignore` lists words that do not count (the Spanish helper ignores 'no': in a Spanish quote it is the Spanish cue list's word)."""
    names = ("negation_word", "negation_contraction") + (("negation_extra", "negation_ruled_out") if extra else ())
    return any(m.group(0).lower() not in ignore for m in view(*names).finditer(text.replace("\u2019", "'")))


def is_negation_word(w: str) -> bool:
    return bool(view("negation_word", "negation_extra").fullmatch(w))


def lateral_words(text: str) -> set:
    return {m.group(0).lower() for m in aq("side").finditer(text)}


@functools.lru_cache(maxsize=1)
def _aq() -> dict:
    """The added-qualifier families from app/llm/lexicon.yaml code_lists.added_qualifier (T-105): the one source of the attribution, hedge,
    approximation and inability word lists, for this module and for spanish_text."""
    from app.backend import lexicon
    return {e["id"]: e["regex"] for e in lexicon.code_list("added_qualifier")}


def aq(name: str):
    return _aq()[name]


@functools.lru_cache(maxsize=None)
def view(*names: str):
    """One compiled regex over several lexicon families (alternation); a view of the lexicon, never a word list of its own."""
    return re.compile("|".join(f"(?:{aq(n).pattern})" for n in names), re.IGNORECASE)


def _clean(m) -> str:
    return re.sub(r"\s+", " ", m.group(0)).strip(" .;:\n").lower()


def added_qualifier_tokens(summary: str, excerpt: str, *, quote_has: dict = None) -> list:
    """Qualifier words the summary carries but the quote has no qualifier of that kind for (D-047, the reverse of dropped_qualifiers):
    an attribution (who said it), a hedge (how sure) or an approximation (how exact). The word lists are the lexicon's added_qualifier family (T-105). `quote_has` lets the Spanish
    path say that its own cue lists found a kind in the quote ({'attribution'|'hedge'|'approximation': bool}). Returns the summary's own words, lower
    case, in order; [] when the quote carries the kind. 'cannot' and 'unable to' are one statement; 'about' before a verb-object ('counseled about 3
    exercises') is a preposition, not an approximation."""
    qh = quote_has or {}
    summary, excerpt = summary.replace("\u2019", "'"), excerpt.replace("\u2019", "'")
    fam = _aq()
    out = []
    if not (qh.get("attribution") or attribution_carried(excerpt)):
        out += [_clean(m) for rx in (fam["attribution"], fam["attribution_bare_verb"]) for m in rx.finditer(summary)]
    if not (qh.get("hedge") or has_hedge(excerpt)):
        out += [m.group(0).lower() for m in fam["hedge"].finditer(summary)]
        for i in sorted(hedge_ids(summary)):
            m = _lexicon()["hedge"][i].search(summary)
            if m and m.group(0).lower() not in out:
                out.append(_clean(m))
        if not fam["inability"].search(excerpt):
            out += [_clean(m) for m in fam["inability_assertion"].finditer(summary)]
    if not (qh.get("approximation") or aq("approximation").search(excerpt)):
        out += approximation_hits(summary)
    return list(dict.fromkeys(w for w in out if w))


def dropped_qualifiers(summary: str, excerpt: str) -> list:
    """Qualifier kinds present in the excerpt and absent from the summary (D-022): hedge, self_report, negation, laterality, approx. The word lists are the
    lexicon's added_qualifier family (the same ones added_qualifier_tokens reads, T-105 r2), so a word the summary may not add is a word it may not drop."""
    out = []
    if hedge_in_quote(excerpt) and not has_hedge(summary):
        out.append("hedge")
    if attribution_in_quote(excerpt) and not attribution_carried(summary):   # D-022 qualifier carry only; D-040: nothing labels who is speaking
        out.append("self_report")
    ex_neg = set(negation_words(excerpt))
    sm_neg = set(negation_words(summary))
    same = aq("negation_interchangeable")          # no / not / none / never say the same thing
    if any(w not in sm_neg and not (same.fullmatch(w) and any(same.fullmatch(x) for x in sm_neg)) for w in ex_neg):
        out.append("negation")
    if lateral_words(excerpt) - lateral_words(summary):
        out.append("laterality")
    if approximation_hits(excerpt) and not approximation_hits(summary):
        out.append("approx")
    return out


def missing_qualifier_terms(summary: str, excerpt: str) -> list:
    """The words in the quote that carry a qualifier the summary dropped (D-022), for the 'Edit the summary to keep ...' sentence. English patterns only;
    a Spanish quote may return []. Display only: the pass/fail decision is dropped_qualifiers()."""
    kinds = set(dropped_qualifiers(summary, excerpt))
    found = []

    def add(m):
        w = re.sub(r"\s+", " ", m.group(0)).strip(" .").lower()
        if w and w not in found:
            found.append(w)
    if "hedge" in kinds:
        for rx in _lexicon()["hedge"].values():
            m = rx.search(excerpt)
            if m:
                add(m)
        if not found:
            m = aq("hedge").search(excerpt)
            if m:
                add(m)
    for kind, rx in (("self_report", aq("attribution")), ("negation", view("negation_word", "negation_contraction")), ("laterality", aq("side")),
                     ("approx", aq("approximation"))):
        if kind in kinds:
            sm = {w.lower() for w in (m.group(0) for m in rx.finditer(summary))}
            for m in rx.finditer(excerpt):
                if m.group(0).lower() not in sm:
                    add(m)
    return found[:4]


def check_summary(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
    reasons = []
    if new_tokens(summary, excerpt, label, date_iso):
        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
    if dropped_qualifiers(summary, excerpt):
        reasons.append("SUMMARY_DROPS_QUALIFIER")
    return reasons
