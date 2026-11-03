"""Lexicon floor scan (code). Port of the reference matcher in research/lexicon_selfcheck.py (D-018): clause-bounded negation guard,
field answers, year_filter, suppress_if_followed_by. Pure; no model. Hits with strength high/medium raise flags; low is context only."""
import bisect
import functools
import re

from app.backend import lexicon, sentences

TOKEN = re.compile(r"[\w'/-]+|[;,]")
SENT_END = re.compile(r"[.!?](?=\s|$)|\n")
YEAR = re.compile(r"\b(19|20)\d{2}\b")
RAISES = ("high", "medium")
# T-120 r3: "Hx obtained via patient's son, who interpreted" names who GAVE the history; it states no prior condition. We do not guess whether a
# sentence names a condition. We strip only the history-source ATTRIBUTION phrase after the history word (verb + via/from/per + a closed list of
# people and channels + an optional ", who interpreted") and look at what is left of the sentence: nothing left means the sentence was only
# attribution (no flag); anything left (", who reports neck pain", ": lumbar strain", a newline and more text) keeps the hit. An unknown source noun
# is simply not stripped, so it keeps the flag (safe direction).
_HISTORY_WORD = re.compile(r"(?:hx|h/o|phx|history)\Z", re.I)
_PERSON = (r"son|daughter|husband|wife|spouse|mother|father|brother|sister|sibling|aunt|uncle|cousin|grandmother|grandfather|niece|nephew|family|friend|caregiver|relative|guardian|parent|neighbor|"
           r"interpreter|translator|language\s+line|telephone|phone|video|ipad|tablet|staff|nurse|ems|paramedics?|medic|patient|pt|"
           r"chart\s+review|chart|(?:medical\s+)?records?|(?:dr|mr|mrs|ms)\.\s+[\w'-]+|(?-i:(?:Dr|Mr|Mrs|Ms)\s+[A-Z][\w'-]+)|doctor|physician")      # T-132: 'MS history' is a diagnosis, not 'Ms. History'
_PERSON_TAIL = r"(?:\s+(?:crew|line|service|team|staff|member|members|interpreter|translator|nurse))*"
_ONE_SOURCE = rf"(?:(?:the|a|an)\s+)?(?:(?:patient|pt)(?:'s|\u2019s)\s+)?(?:{_PERSON}){_PERSON_TAIL}\b"
_SOURCES = rf"{_ONE_SOURCE}(?:(?:,|\s+and|\s+or)\s+{_ONE_SOURCE})*"
_WHO_CORE = r"who\s+(?:was\s+)?(?:interpreted|translated|relayed|interpreting|translating|relaying)(?:\s+for\s+(?:the\s+)?(?:patient|pt|her|him|them|(?:dr|mr|mrs|ms)\.?\s+[\w'-]+))?"      # one pattern for the phrase tail and the chained clause
_WHO_INTERPRETED = rf"(?:,?\s+(?:and\s+)?{_WHO_CORE})?"
_HISTORY_SOURCE = re.compile(r"\s+(?:(?:was|is|were)\s+)?(?:obtained|taken|provided|given|gathered|collected|supplied|reported|relayed)\s+"
                             rf"(?:via|from|by|through|per|with)\s+{_SOURCES}{_WHO_INTERPRETED}", re.I)
_HISTORY_VIA = re.compile(rf"\s+(?:per|via)\s+{_SOURCES}{_WHO_INTERPRETED}", re.I)
_WORD = re.compile(r"\w")
_SENT_END = re.compile(r"[.!?](?:\s|$)")   # a newline does NOT end the sentence here: "Hx per interpreter\nLumbar strain 2019" keeps the flag


@functools.lru_cache(maxsize=4)
def _sentence_ends(text: str) -> tuple:
    """(starts, ends) of every SENT_END match in `text`, computed once per text (T-132 r4: _sentence_bounds ran a scan from 0 for every hit - quadratic on a long sentence)."""
    ms = list(SENT_END.finditer(text))
    return [m.start() for m in ms], [m.end() for m in ms]


def _sentence_bounds(text, start, end):
    """(start of the sentence that holds text[start:end], its end). Same result as scanning SENT_END from 0 up to `start`, then from `end` on; here two bisects on the cached match list."""
    starts, ends = _sentence_ends(text)
    i = bisect.bisect_right(ends, start)
    s = ends[i - 1] if i else 0
    if start > s and text[start - 1] in ".!?":                  # a sentence mark right before the hit ends the sentence there (the range scan ran up to `start`, where '$' matches)
        s = start
    j = bisect.bisect_left(starts, end)
    return s, (starts[j] if j < len(starts) else len(text))


def _norm(tokens):
    return " " + " ".join(t.lower() for t in tokens if t not in (",", ";")) + " "


def _strip_pseudo(s, pseudo):
    for p in pseudo:
        s = s.replace(" " + p.lower() + " ", " ")
    return s


def _has(s, phrases):
    return any((" " + p.lower() + " ") in s for p in phrases)


def _cut_at_terminator(tokens, terms):
    low = [t.lower() for t in tokens]
    multi = [t for t in terms if " " in t]
    for i in range(len(low) - 1, -1, -1):
        if low[i] in terms or any(" ".join(low[i:i + len(m.split())]) == m for m in multi):
            return tokens[i + 1:]
    return tokens


def negated(text, start, end, neg):
    """True if the hit text[start:end] is negated (clause-bounded NegEx-style guard)."""
    s0, s1 = _sentence_bounds(text, start, end)
    if neg.get("field_answer") and re.match(neg["field_answer"], text[end:], re.I):
        return True
    terms = [t.lower() for t in neg["clause_terminators"]]
    word_terms = [t for t in terms if t not in (",", ";")]
    pseudo, w = neg["pseudo_negations"], neg["window_tokens"]
    before = TOKEN.findall(text[max(s0, text.rfind(";", s0, start) + 1):start])      # only the clause after the last ';' matters; slicing there is the same tokens (T-132 r4: linear on a long ';' chain)
    segs, cur = [], []
    for t in before:
        if t == ",":
            segs.append(cur)
            cur = []
        else:
            cur.append(t)
    segs.append(cur)

    def seg_negates(seg):
        tail = _cut_at_terminator(seg, word_terms)[-w:]
        return _has(_strip_pseudo(_norm(tail), pseudo), neg["pre_cues"])

    if seg_negates(segs[-1]):
        return True
    hit_seg = [t.lower() for t in segs[-1]]
    if len(segs) > 1 and any(c in hit_seg for c in neg["list_coordinators"]):
        breakers = set(b.lower() for b in neg["list_breakers"])
        if not breakers & set(hit_seg):
            for seg in reversed(segs[:-1]):
                low = [t.lower() for t in seg]
                if _has(_strip_pseudo(_norm(seg), pseudo), neg["pre_cues"]):
                    return True
                if breakers & set(low) or any(t in word_terms for t in low):
                    break
    clause = []
    for tm in TOKEN.finditer(text, end, s1):                    # lazily: only the first `w` tokens of the clause are read (T-132 r4: not the whole rest of a long sentence per hit)
        t = tm.group(0)
        if t in (",", ";") or t.lower() in word_terms or len(clause) >= w:
            break
        clause.append(t)
    return _has(_strip_pseudo(_norm(clause[:w]), pseudo), neg["post_cues"])


@functools.lru_cache(maxsize=1)
def _entries() -> tuple:
    out = []
    for e in lexicon.load()["entries"]:
        sup = re.compile(e["suppress_if_followed_by"], re.I) if e.get("suppress_if_followed_by") else None
        out.append((e, re.compile(e["pattern"], re.I | re.M), sup))
    return tuple(out)


# T-132 r5 (orchestrator final narrowing, 2026-11-02): the extension stops at a hard line break only before (a) an ALL-CAPS label (_SECTION_HEADER), (b) a label from a CLOSED list of section and
# vitals names followed by a colon (SOAP letters S/O/A/P, Subjective, Objective, Assessment, Plan, Impression, Diagnosis/Dx, Rx, Meds, Medications, Allergies, BP, HR, RR, Temp, SpO2, Pulse, Weight)
# or (c) a bullet / numbered item (plus a blank line or a sentence end, handled elsewhere). A clinical phrase that ends in a colon ('Left wrist swollen:', 'Neck pain:') is the condition and
# never stops it: a quote that drops the condition is worse than one that runs long. A colon inside a line is a condition's word too. The colon must be followed by a space or the end ('Seen at 10:30').
_LINE_LABEL = re.compile(r"(?:(?-i:[SOAP])|(?:subjective|objective|assessment|plan|impression|diagnosis|dx|rx|meds|medications|allergies|bp|hr|rr|temp|spo2|pulse|weight)(?![\w'/-])):(?=\s|$)", re.I)
_LINE_BULLET = re.compile(r"(?:[-*\u2022\u00b7\u2013\u2014]|\d{1,2}[.)])\s")

def _is_source_sentence(text: str, end: int) -> bool:
    """T-120 r3: the history word ends at text[end]. Strip the attribution phrase that follows it and test what is left of the sentence: only
    punctuation or nothing means the sentence was only attribution ("Hx obtained via patient's son, who interpreted."). Any other text keeps the
    hit, whatever it says ("who reports neck pain", ": lumbar strain 2019", "(lumbar strain)", a second line)."""
    m = _HISTORY_SOURCE.match(text, end) or _HISTORY_VIA.match(text, end)
    if not m:
        return False
    q = _WORD.search(text, m.end())
    if q is None:
        return True
    s = _SENT_END.search(text, m.end(), q.start() + 1)         # a sentence end before the first word character after the phrase: nothing but punctuation is left (no scan to the end of a long sentence)
    return bool(s and s.start() < q.start())


_BLANK_LINE = re.compile(r"\n[ \t\r]*\n")
# A label on its own: 2+ capitals/digits/'#' and a colon ('PLAN:', 'BP:', 'HR:', 'PE:', 'CHIEF COMPLAINT:', 'TYLENOL #3:'). Structure, not a list of section names. DECISION: title-case labels
# ('Plan:', 'Dx:') are handled by the closed-list _LINE_LABEL at the start of a physical line (below), never inside a line.
_SECTION_HEADER = re.compile(r"[A-Z][A-Z0-9 /&#-]{1,}:")
_HISTORY_CLAUSE = re.compile(r"(?:hx|h/o|phx|history)\b", re.I)
_WHO_CLAUSE = re.compile(rf"(?:and\s+)?{_WHO_CORE}\b", re.I)


def _soft_wraps(text: str) -> str:
    """Same-length copy of `text` in which every SOFT line wrap is a space (so all offsets still map 1:1 to the original; a quote is always cut from the original).
    A newline is hard - kept - when it follows a sentence end (not the dot of Dr./Mrs./an initial), touches a blank line (also one with spaces, or CRLF), or is followed by a
    section label ('PLAN:', 'BP:'), a closed-list 'Label:' line ('Plan:', 'Rx:') or a bullet / numbered item."""
    out, n = list(text), len(text)
    for i, ch in enumerate(text):
        if ch != "\n":
            continue
        j = i + 1
        while j < n and text[j] in " \t\r":
            j += 1
        k = i - 1
        while k >= 0 and text[k] in " \t\r":
            k -= 1
        if j >= n or text[j] == "\n" or k < 0 or text[k] == "\n":
            continue
        e = k
        while e >= 0 and text[e] in "\"')]}":
            e -= 1
        if e >= 0 and text[e] in ".!?" and not (text[e] == "." and sentences._abbrev_before(text[max(0, e - 30):e + 1], min(e, 30))):
            continue
        if _SECTION_HEADER.match(text, j) or _LINE_LABEL.match(text, j) or _LINE_BULLET.match(text, j):
            continue
        out[i] = " "
    return "".join(out)


def _attribution_only(norm: str, unit: tuple) -> bool:
    """True when the clause is only a history-source attribution ('Hx per son;', 'who interpreted for the patient;'): no word is left once the phrase is removed."""
    seg = norm[unit[0]:unit[1]]
    m = _HISTORY_CLAUSE.match(seg)
    if m:
        att = _HISTORY_SOURCE.match(seg, m.end()) or _HISTORY_VIA.match(seg, m.end())
        return bool(att) and not re.search(r"\w", seg[att.end():])
    w = _WHO_CLAUSE.match(seg)
    return bool(w) and not re.search(r"\w", seg[w.end():])


class _Wrap:
    """The soft-wrap-normalised copy of a text, its units, and (T-132 r4, staff r3 minor 5) the chain ends computed ONCE, in one backward pass, so every hit looks its walk up in O(1)
    and the scan stays linear however long a run of attribution-only clauses is. chain_end[i] is the index of the unit where a walk that has just taken unit i stops: i itself at a sentence
    end, at the end of the text, at a hard line break or at a section label; otherwise the next unit if it has content, else the chain end of that unit."""

    def __init__(self, text: str):
        self.norm = _soft_wraps(text)
        self.units = sentences.stripped_spans(self.norm)
        self.starts = [a for a, _ in self.units]
        n, norm, units = len(self.units), self.norm, self.units
        self.chain_end = [0] * n
        for i in range(n - 1, -1, -1):
            end = units[i][1]
            if norm[end - 1] in ".!?" or i + 1 >= n or "\n" in norm[end:units[i + 1][0]] or _SECTION_HEADER.match(norm, units[i + 1][0]):
                self.chain_end[i] = i
            else:
                self.chain_end[i] = i + 1 if not _attribution_only(norm, units[i + 1]) else self.chain_end[i + 1]

    def unit_containing_end(self, pos: int):
        """Index of the unit with start < pos <= end, or None."""
        i = bisect.bisect_left(self.starts, pos) - 1
        return i if i >= 0 and pos <= self.units[i][1] else None


def _extend_attribution_unit(text: str, wrap: "_Wrap", end: int, unit: tuple):
    """T-132: the history word ends at text[end], inside `unit` (a one-line unit of the original text). `wrap.norm` is _soft_wraps(text) and `wrap.units` its units, so a line wrap
    is a space and a clause is never cut in the middle of a phrase, in the first clause or any later one. The quote is always cut from the ORIGINAL text.
    (a) the unit is completed to the end of the clause that holds the end of the attribution phrase ('Hx obtained\nvia patient's son;' is one clause);
    (b) when nothing but punctuation is left after the phrase, the quote would show who gave the history and not the condition: it extends over the following
        clauses of the SAME sentence - every further attribution-only clause ('Hx per EMS; who interpreted for the patient; Hx per son;' - no cap, one lookup) - up to and including
        the first clause with content. It never crosses a sentence end, a blank line, a hard line break before a section label, a closed-list 'Label:' line or a bullet, or a section label ('PLAN:', 'BP:').
    A unit that already names something is returned as it is (scan() then joins overlapping units of one flag type)."""
    norm = wrap.norm
    m = _HISTORY_SOURCE.match(norm, end) or _HISTORY_VIA.match(norm, end)
    if not m or _BLANK_LINE.search(text, end, m.end()):
        return unit
    i = wrap.unit_containing_end(m.end())
    if i is None:
        return unit
    cur = (unit[0], max(unit[1], wrap.units[i][1]))
    if re.search(r"\w", norm[m.end():cur[1]]):
        return cur
    return (cur[0], wrap.units[wrap.chain_end[i]][1])


def _hit_year(m):
    for g in ("year", "year2"):
        try:
            if m.group(g):
                return int(m.group(g))
        except IndexError:
            pass
    y = YEAR.search(m.group(0))
    return int(y.group(0)) if y else None


def _clause_after(text, end):
    m = re.search(r"[,;.\n]", text[end:])
    return text[end:end + m.start()] if m else text[end:]


def _join_overlapping(out: list) -> None:
    """T-132: units tile the text, so two hits of one flag type can only overlap through an extended unit ('Hx per EMS\\nHx via son; neck pain.': the first hit's unit runs on to the ';', the
    second hit's to 'neck pain.'). Overlapping units of one flag type become ONE span (the union), so there is one flag whose quote contains the condition and no condition-less fragment.
    Sort and sweep: linear after the sort. The text of each quote is still one contiguous slice of the record."""
    by_type = {}
    for h in out:
        by_type.setdefault(h["flag_type"], []).append(h)
    for hs in by_type.values():
        hs.sort(key=lambda h: (h["unit_start"], -h["unit_end"]))
        group, lo, hi = [], 0, 0
        for h in hs + [None]:
            if h is not None and group and h["unit_start"] < hi:
                hi = max(hi, h["unit_end"])
                group.append(h)
                continue
            for g in group:
                g["unit_start"], g["unit_end"] = lo, hi
            if h is not None:
                group, lo, hi = [h], h["unit_start"], h["unit_end"]


def scan(text: str, accident_year=None) -> list:
    """Firing hits as [{id, flag_type, category, strength, start, end, text, unit_start, unit_end}], file order. Unknown accident_year keeps
    year-filtered hits (the item is reviewed anyway)."""
    neg = lexicon.load()["negation"]
    units = sentences.stripped_spans(text)
    unit_starts = [a for a, _ in units]
    wrap = []                          # the _Wrap of the text, built once and only when a history hit needs it
    out = []
    for e, rx, sup in _entries():
        if e["strength"] not in RAISES:
            continue
        for m in rx.finditer(text):
            if e.get("negatable") and negated(text, m.start(), m.end(), neg):
                continue
            if e.get("year_filter") and accident_year:
                y = _hit_year(m)
                if y and y >= accident_year:
                    continue
            if sup and sup.search(_clause_after(text, m.end())):
                continue
            if e["flag_type"] == "pre_existing" and _HISTORY_WORD.match(m.group(0)) and _is_source_sentence(text, m.end()):
                continue
            k = bisect.bisect_right(unit_starts, m.start()) - 1
            u = units[k] if k >= 0 and m.start() < units[k][1] else (m.start(), m.end())
            if e["flag_type"] == "pre_existing" and _HISTORY_WORD.match(m.group(0)):
                if not wrap:
                    wrap.append(_Wrap(text))
                u = _extend_attribution_unit(text, wrap[0], m.end(), u)
            out.append({"id": e["id"], "flag_type": e["flag_type"], "category": e["category"], "strength": e["strength"],
                        "start": m.start(), "end": m.end(), "text": m.group(0), "unit_start": u[0], "unit_end": u[1]})
    _join_overlapping(out)
    return out
