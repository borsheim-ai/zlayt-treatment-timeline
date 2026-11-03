"""Defense credibility wording (D-038, D-043), code only. A family match over the lexicon's credibility terms (Waddell, symptom magnification, pain behavior,
non-physiologic/non-organic, out of proportion, inconsistent/not-consistent/sub-maximal effort, malingering, secondary gain), not one fixed phrase.
D-043: fail toward flagging. Any sentence containing a credibility term flags, unless the WHOLE sentence is one clause that matches the short allow-list
of clean negations below. A comma, semicolon, line break, contrast word, side qualifier or any extra words means it flags. The sentence runs to . ? ! or end of text (';' and line breaks are clause separators); the flag excerpt is that whole sentence. No clause or segment logic."""
import re

from app.backend import sentences

CATEGORY = "credibility_language"
_SEP = r"[\s-]*"
_COUNT = r"\d+\s*(?:/|of|out\s+of)\s*\d+"
_APOS = r"(?:['\u2019]s)?"
_WADDELL = (r"(?P<count>" + _COUNT + r"\s+)\bWaddell" + _APOS + r"\b(?:\s+(?:signs?|testing|tests?|criteria|scores?|findings?|positive|negative)\b)?"
            r"|\b(?:positive|negative)\s+Waddell" + _APOS + r"\b(?:\s+(?:signs?|testing|tests?|criteria|scores?|findings?)\b)?"
            r"|\bWaddell" + _APOS + r"[\s-]+(?:signs?|testing|tests?|criteria|scores?|findings?|positive|negative|\d+(?:\s*(?:/|of|out\s+of)\s*\d+)?)\b")
# T-111 r2: a bare positive count ("3/5 positive") is a Waddell result only when the sentence right before it is a Waddell sentence in the same record.
_BARE_COUNT = re.compile(r"\b\d+\s*(?:/|of|out\s+of)\s*5\s+positive\b", re.I)
_PATTERNS = (
    re.compile(_WADDELL, re.I),
    re.compile(r"\bsymptom" + _SEP + r"magnif\w*|\bmagnif(?:y|ying|ies|ied|ication)\s+(?:of\s+)?(?:the\s+|her\s+|his\s+|their\s+)?(?:symptoms?|pain|complaints?)\b", re.I),
    re.compile(r"\bnon" + _SEP + r"organic\s+(?:\w+\s+){0,2}?(?:signs?|findings?|pain)\b", re.I),
    re.compile(r"\bnon" + _SEP + r"physiologic\w*", re.I),
    re.compile(r"\bout\s+of\s+proportion\b", re.I),
    re.compile(r"\b(?:in|non)consistent\s+(?:\w+\s+)?effort\b|\bsub" + _SEP + r"maximal\s+(?:\w+\s+)?effort\b|\b(?:poor|variable)\s+effort\b", re.I),
    # reversed order: "effort is/was/displayed was inconsistent / not consistent".
    re.compile(r"\beffort\s+(?:\w+\s+){0,4}?(?:inconsistent|not\s+(?:consistent|reliable|maximal|full)|sub" + _SEP + r"maximal|variable)\b|\beffort\s+(?:was|is|were|appeared|seemed)\s+(?:\w+\s+)?poor\b", re.I),
    re.compile(r"\bpain\s+behaviou?rs?\b", re.I),
    re.compile(r"\bmalinger\w*|\bsecondary\s+gain\b|\bexaggerat\w*", re.I),
)
# D-043 allow-list (case and trailing punctuation vary), matched against the WHOLE normalized sentence:
# 'No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Waddell signs not tested / not performed.'
# T-111 adds the single-clause 'Waddell testing not performed.' / 'Waddell testing not done.' and 'Not tested.' (D-043 'Not tested/not performed').
# No colon, no 'was/were', no other noun (tests, criteria, findings), no 'Waddell signs not done', no spaced '0 / 5': those flag (T-067 r5 C01-C10).
_CLEAN = re.compile(r"^(?:" + "|".join((
    r"no waddell signs",
    r"waddell signs negative",
    r"0/5 waddell signs",
    r"effort consistent", r"good effort", r"full effort",
    r"waddell signs not (?:tested|performed)",
    r"waddell testing not (?:performed|done)",
    r"not tested",
)) + r")$")
_END = re.compile(r"[.?!][\"')\]}]*$")


def _clean_negation(sentence: str) -> bool:
    return bool(_CLEAN.match(re.sub(r"\s+", " ", sentence.strip().lower()).rstrip(".!? ")))


def sentence_spans(text: str) -> list:
    """Full sentences for credibility flags (D-043, T-067 r5): a sentence ends at . ? ! or end of text. ';' and line breaks only
    separate clauses inside it, so the shared unit splitter's units are merged until one ends in a real terminator."""
    out, cur = [], None
    for a, b in sentences.stripped_spans(text):
        cur = (a, b) if cur is None else (cur[0], b)
        if _END.search(text[cur[0]:cur[1]]):
            out.append(cur)
            cur = None
    if cur is not None:
        out.append(cur)
    return out


def scan(text: str) -> list:
    """Firing credibility hits as [{id, flag_type, category, start, end, text, unit_start, unit_end}], file order, one per span.
    A term in a sentence that is not wholly an allow-listed clean negation always fires (D-043)."""
    units = sentence_spans(text)
    out, seen = [], set()
    for rx in _PATTERNS:
        for m in rx.finditer(text):
            if (m.start(), m.end()) in seen:
                continue
            u = next(((a, b) for a, b in units if a <= m.start() < b), (m.start(), m.end()))
            if _clean_negation(text[u[0]:u[1]]):
                continue
            seen.add((m.start(), m.end()))
            out.append({"id": "credibility_language", "flag_type": "causation", "category": CATEGORY, "strength": "high",
                        "start": m.start(), "end": m.end(), "text": m.group(0), "unit_start": u[0], "unit_end": u[1]})
    rx = _PATTERNS[0]
    for i in range(1, len(units)):
        a, b = units[i]
        m = _BARE_COUNT.search(text, a, b)
        if not m or (m.start(), m.end()) in seen or not rx.search(text, units[i - 1][0], units[i - 1][1]):
            continue
        seen.add((m.start(), m.end()))
        out.append({"id": "credibility_language", "flag_type": "causation", "category": CATEGORY, "strength": "high",
                    "start": m.start(), "end": m.end(), "text": m.group(0), "unit_start": a, "unit_end": b})
    return sorted(out, key=lambda h: h["start"])
