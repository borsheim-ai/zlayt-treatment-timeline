"""Export assembly: letter_text and internal_notes_text from reviewed items. CODE ONLY (no LLM, no network).

Contract (ADR-009, D-001, D-012, D-017, D-019, LLM_VS_CODE rows 8 and 19; R-EX-1..R-EX-8):
    build_export(case) -> {"letter_text": str, "internal_notes_text": str, "counts": {...}}  (counts: R-EX-5, outside both blocks)

`case` is a plain dict (the route layer assembles it from the DB; tests build it from golden files):
    records: [{n, source, date_iso|None, excerpt, [could_not_process|status|reason]}]
    entries: [{id, record_no, summary, excerpt, review_status, [translation_label], [date_iso], [original_summary], [original_excerpt]}]
    amounts: [{id, record_no, cents|None, cls, raw, excerpt, review_status}]   cls: charge | rate | estimate | unclear | damages | ...
    flags:   [{id, type, subtype, evidence:[{record_no, field, excerpt}], review_status, [days, from_date, to_date], [note], [reason]}]
review_status in (accepted, edited) is "in"; dismissed/rejected is "out"; anything else is pending.

The letter builder takes NO flags argument: flag content cannot reach `letter_text` (R-EX-1). Output is deterministic
(R-EX-3): everything is sorted by (date, record number, id) and nothing reads a clock or a random source.
"""
from __future__ import annotations

import os
import re
from datetime import date

from app.backend import amounts, charge_text, language, money, service_date

LETTER_TITLE = "TREATMENT CHRONOLOGY"
CHARGES_TITLE = "BILLED CHARGES"
SUMMARY_TITLE = "TREATMENT SUMMARY"
NOTES_TITLE = "INTERNAL REVIEW NOTES — DO NOT SEND"


def narrative_in_letter() -> bool:
    """D-067: off by default. The paragraph needs its own eval and a verbatim quote plus [Ex. __ / Bates __] on each sentence (D-002) before it may reach a letter."""
    return os.environ.get("NARRATIVE_IN_LETTER") == "1"


SOURCE_PREFIX = "Source [Ex. __ / Bates __]: "
TOTAL_PREFIX = "Billed charges accepted from these records: "  # D-019: nothing may follow the amount, ever
AI_LINE = ("This chronology was drafted with AI assistance; every item in the treatment section was accepted "
           "by the paralegal. Items not reviewed: {n}.")
AI_LINE_PREPARED = ("This chronology was built from answers the team prepared for this demo and checked by a second check; every item in the treatment section was accepted "
                    "by the paralegal. Items not reviewed: {n}.")      # D-069: the notes of a prepared case never say an AI drafted it
FLAGGED_HEADING = ("FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or "
                   "dismiss the entry to remove it; hedge sentences cannot be removed)")

IN = ("accepted", "edited")
STYLES = ("standard", "oneline")      # T-121: "standard" (default) is the golden layout; "oneline" gives one line per entry
# T-121: the translation note is a bracketed, removable phrase at the end of the entry, keyed by the item's translation label (never a line prefix).
TRANSLATION_NOTE = {"AI translation": "[AI translation of the Spanish original; check before sending]",
                    "Prepared translation": "[Prepared translation of the Spanish original; check before sending]",
                    "Translation (edited by reviewer)": "[Translation of the Spanish original, edited by reviewer; check before sending]"}
NARRATIVE_CODE_REASONS = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "CAUSATION_NOT_QUOTED", "SEVERITY_NOT_QUOTED", "FLAG_CONTENT")
OUT = ("dismissed", "rejected")

_ABBREV = {"approx", "dr", "mr", "mrs", "ms", "vs", "e.g", "i.e", "etc", "st", "no", "jr", "sr"}
_TYPE_RANK = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
_CONFLICT_SUB = {"accident_date": "accident date", "treatment_plan": "PT plan", "treatment_plan_vs_actual": "PT plan",
                 "accident_dates_differ": "accident date", "accident_date_after_treatment": "accident date"}
_ACCIDENT_SUBS = ("accident_date", "accident_dates_differ", "accident_date_after_treatment")
_COLLISION_RE = re.compile(r"rear-ended|collision|accident|crash|\bMV[AC]\b|struck|hit by", re.I)
# Order inside a merged flag line (most adjuster-actionable first); both the lexicon subtypes and the closed category names.
_ORDER = ["hedged_imaging", "speculative_language", "noncompliance", "missed_care", "patient_reported_onset", "patient_report",
          "temporal_after_gap", "new_onset", "accident_date_inconsistency", "accident_date_provenance"]
_FUTURE_RE = re.compile(r"^\s*recommend", re.I)  # extend by card (R-EX-4 section 7)


# ---------------------------------------------------------------- small formatting helpers
def _long_date(iso):
    if not iso:
        return "date not stated"
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def _money(cents):
    return f"${cents // 100:,}.{cents % 100:02d}"


def _money_short(cents, raw=""):
    if cents is None:
        return raw
    return f"${cents // 100:,}" if cents % 100 == 0 else _money(cents)


def _norm(s):
    return " ".join((s or "").split())


def _cap(s):
    return s[:1].upper() + s[1:]


def _terminate(s):
    """End a note sentence with a period unless it already ends with a full stop."""
    return s if s.endswith('."') or s.endswith(".") else s + "."


def _sentence_spans(text):
    """[(start, end)] whole-sentence spans, split at '. ' (not after an abbreviation, not before a lowercase
    letter) and at line breaks. The terminal '.' stays inside the span."""
    spans, start, i, n = [], 0, 0, len(text)
    while i < n:
        c = text[i]
        if c == "\n":
            if text[start:i].strip():
                spans.append((start, i))
            start = i + 1
        elif c == "." and (i + 1 == n or text[i + 1].isspace()):
            word = re.search(r"([A-Za-z.]+)$", text[start:i])
            w = word.group(1).lower() if word else ""
            j = i + 1
            while j < n and text[j] == " ":
                j += 1
            nxt = text[j] if j < n else ""
            if w not in _ABBREV and not nxt.islower():
                spans.append((start, i + 1))
                start = j
                i = j - 1
        i += 1
    if text[start:].strip():
        spans.append((start, n))
    return spans


def _sentences(text):
    return [text[s:e] for s, e in _sentence_spans(text or "")]


# ---------------------------------------------------------------- case view
class _View:
    """Read-only index over the case dict. All ordering decisions live here."""

    def __init__(self, case):
        self.records = {r["n"]: r for r in case.get("records", [])}
        cfg = case.get("export_config") or {}
        self.export_config = cfg if any(cfg.get(k) is not None for k in ("exhibit", "bates_prefix", "bates_start")) else None
        self.entries = sorted(case.get("entries", []), key=lambda e: (self._date(e), e["record_no"], str(e.get("id"))))
        self.amounts = sorted(case.get("amounts", []), key=lambda a: (self._date(a), a["record_no"], str(a.get("id"))))
        self.flags = list(case.get("flags", []))
        self.narrative = case.get("narrative") if narrative_in_letter() else None      # D-067: the drafted paragraph is cut from the MVP; it never reaches the letter (or the notes) unless NARRATIVE_IN_LETTER=1
        self.overlaps = list(case.get("possible_overlaps") or [])
        self.prepared = bool(case.get("prepared"))      # D-069: the case's answers are the team's prepared ones, so no sentence of the notes says an AI drafted them

    def verbatim(self, item):
        """The quoted excerpt must still be a substring of its record (whitespace-normalized); else it never ships."""
        return _norm(item.get("excerpt")) in _norm(self.text(item["record_no"]))

    @staticmethod
    def states_amount(e):
        """T-139 (D-019, R-CH-7, R-EX-8): the entry's summary or quote states money (the one shared detector, app/backend/money.py). It is used for the notes' hold reason; the letter
        itself is checked as text by the export gate (letter_money_blockers)."""
        return money.has_money(e.get("summary")) or money.has_money(e.get("excerpt"))

    @property
    def in_entries(self):
        """D-041: an entry with no confirmed date never reaches the letter, even if it was accepted before this rule (it is listed in the
        internal notes as 'date not confirmed'). T-139 r4: an accepted entry whose summary or quote states money is NOT dropped silently; it stays in the letter text, where the
        export gate (letter_money_blockers) finds the money and blocks the export, naming the line."""
        return [e for e in self.entries if _status(e) == "in" and self.verbatim(e) and self.date_of(e)]

    @property
    def narrative_sentences(self):
        """Sentences of an ACCEPTED draft paragraph whose cited entry is still in the letter and unchanged since the draft."""
        n = self.narrative
        if not n or n.get("status") != "accepted":
            return []
        live = {e["id"]: e for e in self.in_entries}
        return [s for s in n.get("sentences", []) if s["entry_id"] in live and (n.get("basis") or {}).get(s["entry_id"]) == basis_hash(live[s["entry_id"]])
                and not charge_text.has_currency(s.get("text"))]

    @property
    def in_charges(self):
        """D-073 fallback: in the order of the record dates (the letter prints no service date)."""
        got = [a for a in self.amounts if a["cls"] == "charge" and a.get("cents") is not None and _status(a) == "in" and self.verbatim(a)]
        return sorted(got, key=lambda a: (self._date(a), a["record_no"], str(a.get("id"))))

    def _date(self, item):
        return self.date_of(item) or "9999-12-31"

    def date_of(self, item):
        return item.get("date_iso") or (self.records.get(item["record_no"]) or {}).get("date_iso")

    def source_prefix(self, n):
        """Citation prefix: 'Source [Ex. __ / Bates __]: ', or '..., p. N: ' when the record came from a PDF (D-031)."""
        pg = (self.records.get(n) or {}).get("page")
        head = SOURCE_PREFIX[:-2] if self.export_config is None else self._bracket(n)
        return head + (": " if pg is None else f", p. {pg}: ")

    def oneline_bracket(self, n):
        """'[Ex. 7 / Bates RIV-0001]' for the one-line style; a PDF page goes inside the bracket: '[Ex. __ / Bates __, p. 3]'."""
        pg = (self.records.get(n) or {}).get("page")
        head = SOURCE_PREFIX[len("Source "):-2] if self.export_config is None else self._bracket(n)[len("Source "):]
        return head if pg is None else head[:-1] + f", p. {pg}]"

    def _bracket(self, n):
        """'Source [Ex. 7 / Bates RIV-0001]' from the per-case export config; unset parts stay '__'. Bates = first number + record number - 1, 4 digits."""
        c = self.export_config
        ex = c.get("exhibit") or "__"
        prefix, start = c.get("bates_prefix"), c.get("bates_start")
        bates = "__" if prefix is None and start is None else f"{prefix or ''}{(1 if start is None else start) + n - 1:04d}"
        return f"Source [Ex. {ex} / Bates {bates}]"

    def source(self, n):
        return (self.records.get(n) or {}).get("source", "")

    def text(self, n):
        return (self.records.get(n) or {}).get("excerpt", "")

    def rec_date(self, n):
        return (self.records.get(n) or {}).get("date_iso")

    def charge_when(self, a):
        """D-073 fallback (T-202 round 6): the label before a charge's amount is ALWAYS the fillable blank, like the Bates placeholder, never a date: 'Fennimoor Spine Clinic, itemized ledger,
        date of service [__________] (record dated June 15, 2026)' (D-075: always the record's own date, never a bill/record classification). The code extracts no service date for
        the letter (SCOPE_CUTS row 28); the paralegal fills the blank from the quote. One string, the same one the case view carries (`store.charge_service_date`)."""
        n = a["record_no"]
        return f"{self.source(n)}, {service_date.not_stated_text(self.rec_date(n))}"

    def cite(self, n):
        return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"

    def cite_dated(self, n):
        return f"record {n} ({self.source(n)}, dated {_long_date(self.rec_date(n))})"

    def quote(self, n, ev, whole_sentence=False):
        """Quote evidence from record n. A directly following full stop is included when the evidence starts a
        sentence; whole_sentence expands mid-sentence evidence to its sentence. Always a substring of the record."""
        text = self.text(n)
        i = text.find(ev) if ev else -1
        if i < 0:
            return ev
        j = i + len(ev)
        if whole_sentence:
            hit = [(s, e) for s, e in _sentence_spans(text) if s <= i and j <= e]
            if hit:
                return text[hit[0][0]:hit[0][1]]
        starts_sentence = i == 0 or text[:i].rstrip(" ").endswith((".", "\n"))
        if starts_sentence and text[j:j + 1] == "." and not ev.endswith("."):
            return ev + "."
        return ev


def _foreign_money(text, pos, raw):
    """The money expressions of `text` that are not the charge's own figure (`raw` at offset `pos`; with no offset, a hit that contains `raw`). The one detector."""
    out = []
    for a, b, h, _ in money.hits(text):
        own = (a < pos + len(raw) and pos < b) if pos is not None else raw in h
        if own and not re.search(r"\d", h.replace(raw, "", 1)):
            continue
        out.append(h)
    return out


def _clauses(sentence):
    """Candidate clauses of a sentence, widest first: the pieces between ; and , (a comma inside a number is not a break), then each piece cut before a parenthesis."""
    spans = [(m.start(), m.end()) for m in re.finditer(r"(?:[^;,]|,(?=\d))+(?:[;,]|$)", sentence)]
    out = list(spans)
    for lo, hi in spans:
        k = sentence.find(" (", lo, hi)
        if k > lo:
            out.append((lo, k))
    return out


def _amount_quote(v, a):
    """The sentence of the amount's excerpt that holds the figure (a pipeline amount may carry the whole record excerpt). The figure is found by its own offset
    (`pos`, T-140 r3) so two equal figures of one record quote their own lines; without `pos` the first occurrence is used."""
    exc, raw = a.get("excerpt") or "", a.get("raw") or ""
    pos = a.get("pos")
    i = pos if isinstance(pos, int) and exc[pos:pos + len(raw)] == raw else (exc.find(raw) if raw else -1)
    base = 0
    if i >= 0:
        for st, en in _sentence_spans(exc):
            if st <= i < en:
                exc, base = exc[st:en], st
                break
    # T-139 r5 (D-019, R-EX-8; claims-adjuster r4): the quote line of an accepted charge states that charge only. ANY other money expression in the sentence (the one detector,
    # money.hits: a paid or adjusted figure, patient responsibility, wages, number words) is trimmed out by code: the shown text is then a clause of the sentence (or its start up to the charge's figure), still word
    # for word from the record. If no clause is free of other money the sentence stays and the export gate (letter_money_blockers) blocks, naming the charge line.
    rel = i - base
    if raw and _foreign_money(exc, rel if i >= 0 else None, raw):
        cands = _clauses(exc)
        if i >= 0:                                                  # last: the line up to the end of the charge's own figure (a ledger row 'date  service  $150.00  $0.00  $730.00')
            cands.append((exc.rfind("\n", 0, rel) + 1, rel + len(raw)))
        for lo, hi in cands:
            clause = exc[lo:hi]
            if (i >= 0 and lo <= rel and rel + len(raw) <= hi) or (i < 0 and raw in clause):
                if not _foreign_money(clause, rel - lo if i >= 0 else None, raw):
                    exc = clause.strip().rstrip(";,").strip()
                    break
    return v.quote(a["record_no"], exc)


def basis_hash(entry: dict) -> str:
    """What a narrative sentence was drafted from: if an entry's summary or quote changes afterwards, its sentences leave the letter."""
    import hashlib
    return hashlib.sha256(f"{entry['summary']}\x1f{entry['excerpt']}".encode("utf-8")).hexdigest()[:16]


def _status(item):
    s = item.get("review_status")
    return "in" if s in IN else "out" if s in OUT else "pending"


# ---------------------------------------------------------------- letter (takes no flags)
def build_letter(case: dict, style: str = None) -> str:
    """The treatment section. Deliberately has no flags parameter (R-EX-1): flag content cannot reach the letter."""
    return _letter(_View(case), style)


def _translation_note(e):
    """D-042/T-121: a translated entry says so in a bracketed phrase at the end of the entry, which the paralegal deletes after checking."""
    lab = e.get("translation_label")
    return " " + TRANSLATION_NOTE.get(lab, f"[{lab}; check before sending]") if lab else ""


def _translation_line(e) -> list:
    """Standard style: the note is its own bracket line at the end of the entry, under the Spanish quote, so it is not read as a comment on the quote."""
    return [_translation_note(e).strip()] if e.get("translation_label") else []


def _one_line(s):
    """Whitespace only: every run of spaces, tabs and line breaks becomes one space, so the one-line style stays one line. No word changes (T-121)."""
    return " ".join(str(s).split())


def _letter(v, style=None):
    if style not in (None, *STYLES):
        raise ValueError(f"unknown letter style {style!r}")
    out = [LETTER_TITLE, ""]
    for e in v.in_entries:
        n = e["record_no"]
        if style == "oneline":
            # a translated entry carries its English summary on the same line (the note below it would otherwise point at nothing)
            tr = f" — English: {_one_line(e['summary'])}" if e.get("translation_label") else ""
            out += [f'{_long_date(v.date_of(e))} — {_one_line(v.source(n))}: "{_one_line(e["excerpt"])}" {v.oneline_bracket(n)}{tr}{_translation_note(e)}']
        else:
            out += [f"{_long_date(v.date_of(e))} — {v.source(n)}", e["summary"], f'{v.source_prefix(n)}"{e["excerpt"]}"', *_translation_line(e), ""]
    if style == "oneline" and v.in_entries:
        out.append("")
    sents = v.narrative_sentences
    if sents:
        out += [SUMMARY_TITLE, ""] + [f"{x['text']} ({_cite_tail(v, x['entry_id'])})" for x in sents] + [""]
    charges = v.in_charges
    if charges:
        out += [CHARGES_TITLE, ""]
        for a in charges:
            n = a["record_no"]
            out += [f"{v.charge_when(a)}: {_money(a['cents'])}",
                    f'{v.source_prefix(n)}"{_amount_quote(v, a)}"']
        out += ["", TOTAL_PREFIX + _money(sum(a["cents"] for a in charges))]
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


# ---------------------------------------------------------------- internal notes
def _flag_label(f):
    t, sub = f.get("type"), f.get("subtype")
    if t == "gap":
        return "Gap"
    if t == "conflict":
        return "Conflict, " + _CONFLICT_SUB.get(sub, (sub or "other").replace("_", " "))
    if t == "pre_existing":
        return "Prior condition"
    if t == "causation":
        return "Causation language"
    if t == "record_warning":
        return "Record warning"
    return _cap((t or "flag").replace("_", " "))


def _excerpt_ev(f):
    return [x for x in f.get("evidence", []) if x.get("field", "excerpt") == "excerpt"]


def _flag_line(v, f):
    """One flag as a note sentence: '<label>: <body>'."""
    t = f.get("type")
    label = _flag_label(f)
    ev = f.get("evidence", [])
    if t == "gap":
        recs = list(dict.fromkeys(x["record_no"] for x in ev))
        days = f.get("days")
        if days is None and f.get("from_date") and f.get("to_date"):
            days = (date.fromisoformat(f["to_date"]) - date.fromisoformat(f["from_date"])).days
        span = f"{days} days, {_long_date(f.get('from_date'))} to {_long_date(f.get('to_date'))}"
        return _terminate(f"{label}: {span}: " + " to ".join(v.cite(n) for n in recs))
    if t == "conflict":
        order = list(dict.fromkeys(x["record_no"] for x in ev))
        by_rec = {n: [x for x in ev if x["record_no"] == n and x.get("field", "excerpt") == "excerpt"] for n in order}
        if f.get("subtype") == "accident_date":
            segs = []
            for k, n in enumerate(order):
                if by_rec[n]:
                    head = v.cite(n) if k == 0 else _cap(v.cite(n))
                    segs.append(_terminate(f'{head}: "{v.quote(n, by_rec[n][0]["excerpt"], whole_sentence=True)}"'))
                else:
                    coll = next((x for x in _sentences(v.text(n)) if _COLLISION_RE.search(x)), None)
                    if coll:
                        head = v.cite(n) if k == 0 else _cap(v.cite(n))
                        segs.append(_terminate(f'{head}: "{coll.strip()}"'))
                    else:
                        head = v.cite_dated(n)
                        segs.append(_terminate(head if k == 0 else _cap(head)))
            tail = "The tool does not choose between the dates."
            known = [r["date_iso"] for r in v.records.values() if r.get("date_iso")]
            if known:
                tail += f" First recorded treatment: {_long_date(min(known))}."
            return f"{label}: " + " ".join(segs + [tail])
        items = [f'{v.cite(n)} "{v.quote(n, by_rec[n][0]["excerpt"], whole_sentence=True)}"' if by_rec[n] else v.cite(n)
                 for n in order]
        return _terminate(f"{label}: " + "; ".join(items))
    items = []
    for x in _excerpt_ev(f) or ev:
        n = x["record_no"]
        s = f'{v.cite(n)} "{v.quote(n, x["excerpt"])}"' if x.get("field", "excerpt") == "excerpt" else v.cite(n)
        items.append(s)
    return f"{label}: " + "; ".join(items)


def _flag_block(v, flags):
    """One line per gap/conflict flag, one merged line per other type; types in fixed order (gap, conflict, prior, causation)."""
    keyed, merged = [], {}
    for idx, f in enumerate(flags):
        t = f.get("type")
        if t in ("gap", "conflict"):
            keyed.append((_TYPE_RANK[t], idx, [f]))
        elif t in merged:
            merged[t][2].append(f)
            merged[t][2].sort(key=lambda g: _ORDER.index(g.get("subtype")) if g.get("subtype") in _ORDER else 99)
        else:
            merged[t] = (_TYPE_RANK.get(t, 9), idx, [f])
            keyed.append(merged[t])
    lines = []
    for _, _, group in sorted(keyed, key=lambda k: (k[0], k[1])):
        if len(group) == 1:
            line = _flag_line(v, group[0])
        else:
            line = _terminate(f"{_flag_label(group[0])}: " + "; ".join(_flag_line(v, f).split(": ", 1)[1] for f in group))
        extra = [f"Reason: {f['reason']}" for f in group if f.get("reason")] + \
                [f"Reviewer note: {f['note']}" for f in group if f.get("note")]
        lines.append("- " + " ".join([_terminate(line)] + extra) if extra else "- " + _terminate(line))
    return lines or ["- none"]


def _flagged_language(v, flags):
    """R-EX-4(4): letter entries whose excerpt contains the evidence of a flag that is not dismissed (D-012)."""
    out = []
    live = sorted((f for f in flags if _status(f) != "out"), key=lambda f: _TYPE_RANK.get(f.get("type"), 9))
    for e in v.in_entries:
        n, exc = e["record_no"], e["excerpt"]
        spans, keep, hits = _sentence_spans(exc), set(), []
        for f in live:
            if f.get("type") == "gap" and n in {x["record_no"] for x in f.get("evidence", [])}:
                hits.append(_flag_label(f)) if _flag_label(f) not in hits else None   # a gap bounds these records' entries
            if f.get("type") == "conflict" and f.get("subtype") in _ACCIDENT_SUBS and not any(
                    x["record_no"] == n for x in _excerpt_ev(f)) and n in {x["record_no"] for x in f.get("evidence", [])}:
                coll = [k for k, (st, en) in enumerate(spans) if _COLLISION_RE.search(exc[st:en])]
                if coll:   # date-only evidence on a collision-day record: its collision sentence is the flagged language
                    keep.update(coll)
                    if _flag_label(f) not in hits:
                        hits.append(_flag_label(f))
            for x in _excerpt_ev(f):
                i = exc.find(x["excerpt"])
                if x["record_no"] != n or i < 0:
                    continue
                j = i + len(x["excerpt"])
                keep.update(k for k, (s, t) in enumerate(spans) if s < j and t > i)
                lab = _flag_label(f)
                if lab not in hits:
                    hits.append(lab)
        if hits:
            quote = " ".join(exc[spans[k][0]:spans[k][1]] for k in sorted(keep)) or exc
            out.append(f'- {_cap(v.cite(n))}: "{quote}" {_terminate(_cap("; ".join(hits[:1] + [h[:1].lower() + h[1:] for h in hits[1:]])))}')
    return out or ["- none"]


def _provider(src):
    return src.split(",", 1)[0].strip()


def _ledger_label(v, n):
    src = v.source(n)
    return "PT ledger" if re.search(r"\bPT\b|physical therapy", src, re.I) else f"ledger from {_provider(src)}"


def _plan_note(v, n):
    """'(12 planned; discharged at visit 9)' from the same provider's records, by pattern; '' when not derivable."""
    prov = _provider(v.source(n))
    planned = last = None
    for r in sorted(v.records.values(), key=lambda r: (r.get("date_iso") or "", r["n"])):
        if _provider(r.get("source", "")) != prov:
            continue
        m = re.search(r"plan of care:?\s*(\d+)\s+visits", r.get("excerpt", ""), re.I)
        if m and planned is None:
            planned = m.group(1)
        m2 = re.search(r"\bvisit\s+(\d+)\b", r.get("source", ""), re.I)
        if m2 and re.search(r"\bdischarged\b", r.get("excerpt", ""), re.I):
            last = m2.group(1)
    bits = ([f"{planned} planned"] if planned else []) + ([f"discharged at visit {last}"] if last else [])
    return f" ({'; '.join(bits)})" if bits else ""


def _not_totaled_why(v, a, n):
    """The code rule that keeps this figure out of the total (D-059, D-060), read at the figure's own offset."""
    rec = v.records.get(n) or {}
    return amounts.not_totaled_reason(a.get("excerpt"), a.get("raw"), a.get("cents"), rec.get("source"), rec.get("date_iso"), a.get("pos"), list(v.records.values()))


def _amounts_not_totaled(v):
    out = [f'- {_cap(v.cite(a["record_no"]))}: charge {_money(a["cents"])} not exported and not totaled: excerpt not found in record.'
           for a in v.amounts if a["cls"] == "charge" and a.get("cents") is not None and _status(a) == "in" and not v.verbatim(a)]
    for a in v.amounts:
        if a["cls"] in ("charge", "damages") or _status(a) != "in":
            continue
        n, cls = a["record_no"], a["cls"]
        q = f'"{_amount_quote(v, a)}"'
        m = _money_short(a.get("cents"), a.get("raw", ""))
        if cls == "rate":
            per = "/visit" if re.search(r"per visit", a["excerpt"], re.I) else ""
            body = f"Rate {m}{per}; visit count not stated{_plan_note(v, n)}. Request itemized {_ledger_label(v, n)}."
        elif cls == "estimate":
            body = f"Estimate {m}; not a billed charge. Request clean copy of bill."
        elif cls == "unclear" and language.translated_record(v.records.get(n)):
            body = f"Not classified as a charge ({a.get('raw') or m}); check the original quote."
        elif cls == "unclear" and _not_totaled_why(v, a, n):
            body = f"Not totaled ({a.get('raw') or m}): {_not_totaled_why(v, a, n)}"      # T-140
        elif cls == "unclear":
            body = f"Amount unclear ({a.get('raw') or m}). Request clean copy of bill."
        else:
            body = f"{_cap(cls.replace('_', ' '))} amount {m}; not totaled."
        out.append(f"- {_cap(v.cite(n))}: {q} {body}")
    return out or ["- none"]


def _overlaps(v):
    """T-110: a statement line that may already include a separately stated charge of the same kind. Internal notes only (D-019): the letter's total line never
    changes. Plain words, both records and both figures named; nothing is added, subtracted or compared here."""
    out = []
    for o in v.overlaps:
        s_no, c_no = o.get("statement_record_no"), o.get("covered_record_no")
        line = (f"- Possible overlap: {v.cite(s_no)} lists {o.get('statement_text')} on a statement line, and {v.cite(c_no)} separately states "
                f"{o.get('covered_text')}, both for {str(o.get('service') or 'the same service').replace('_', ' ')}. The statement line may already include that charge.")
        if o.get("both_in_total"):
            line += " Both figures are in the charges total, so this service may be counted twice. Check the records and dismiss one of the two."
        elif not o.get("date_known", True):
            line += " The date of the second record is not confirmed, so the statement's date range cannot rule it out. Check the records before relying on the total."
        else:
            line += " The total does not currently add both figures. Check the records before accepting both."
        out.append(line)
    return out


def _damages(v):
    out = [f'- {_cap(v.cite(a["record_no"]))}: "{_amount_quote(v, a)}"'
           for a in v.amounts if a["cls"] == "damages" and _status(a) == "in"]
    return out or ["- none"]


def _future(v):
    out = []
    for r in sorted(v.records.values(), key=lambda r: (r.get("date_iso") or "9999", r["n"])):
        for s in _sentences(r.get("excerpt", "")):
            if _FUTURE_RE.match(s) and "$" not in s:
                out.append(f'- {_cap(v.cite(r["n"]))}: "{s.strip()}" Request cost estimate.')
    return out or ["- none"]


# T-139 r2: 'Bills to request' lists treating providers and facilities only. A record from a law firm (the plaintiff's own LOP/demand letter), a payer's EOB or a records
# custodian is not a bill to request. Decided by the record's SOURCE label and by first-person firm wording in the record, never by a model.
_NOT_A_TREATER_SOURCE = re.compile(r"\b(?:LLP|L\.L\.P\.|law\s+(?:offices?|firms?|group)|attorneys?|counsel(?:ors?)?\s+at\s+law|esq\.?|legal|demand\s+letter|"
                                   r"(?:health|insurance|casualty|auto)\s+(?:plan|insurance|company)|mutual|insurer|insurance|claims|adjuster|EOB|explanation\s+of\s+benefits|"
                                   r"records?\s+(?:retrieval|custodian|service)s?|custodian\s+of\s+records)\b", re.IGNORECASE)
_FIRM_VOICE = re.compile(r"\b(?:this\s+firm\s+represents|we\s+represent|our\s+client|the\s+undersigned\s+(?:firm|counsel)|on\s+behalf\s+of\s+our\s+client)\b", re.IGNORECASE)


def _treating(v, n):
    """True when record `n` comes from a treating provider or facility (so its bill can be requested)."""
    src, text = v.source(n), (v.records.get(n) or {}).get("excerpt") or ""
    return not (_NOT_A_TREATER_SOURCE.search(src) or _FIRM_VOICE.search(text))


def _bills(v):
    paid = {_provider(v.source(a["record_no"])) for a in v.in_charges}
    dismissed = {_provider(v.source(a["record_no"])) for a in v.amounts if a["cls"] == "charge" and _status(a) == "out"}    # T-139: a dismissed charge is never asked for
    rated = {_provider(v.source(a["record_no"])) for a in v.amounts if a["cls"] == "rate" and _status(a) != "out"}
    names = []
    for e in v.in_entries:
        p = _provider(v.source(e["record_no"]))
        if p and _treating(v, e["record_no"]) and p not in paid and p not in dismissed and p not in names:
            names.append(p)
    if not names:
        return ["- none"]
    return ["- " + _terminate("; ".join(p + (" (itemized ledger)" if p in rated else "") for p in names))]


def _undated_charges(v):
    """T-202 r3 + D-073 fallback: one line per accepted charge (each prints the blank for its date of service): provider, amount, why, and the request for a dated itemized bill. [] when no
    charge is accepted (the heading is then left out)."""
    out = []
    for a in v.in_charges:
        why = (a.get("dos_note") or service_date.confirm_note("not_read", "")).split(" The letter prints")[0]
        out.append(f"- {_provider(v.source(a['record_no'])) or v.source(a['record_no'])}, {a['raw']}: {why} The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.")
    return out


def _held_amount_note(v, n, ents):
    """The RECORDS NOT IN THE TREATMENT SECTION reason for an entry held out because it states an amount (T-139 r2). It names only actions the review code accepts:
    dismiss the entry (always clears the hold); a quote without the amount WITH a matching summary in the same edit (a quote-only change is refused when the summary
    still has a token the new quote lacks); a summary edit alone only when the quote is already clean. A bill record is told where its charges are."""
    held = [e for e in ents if _status(e) != "out" and v.states_amount(e)]
    quote = any(money.has_money(e.get("excerpt")) for e in held)
    rows = [{"kind": a["cls"], "review_status": a.get("review_status"), "state": "rejected" if (_status(a) == "out" and a.get("review_status") != "dismissed") else "",
             "text": a.get("raw"), "excerpt": a.get("excerpt")} for a in v.amounts if a["record_no"] == n]
    state = charge_text.bill_state(rows)
    if state in ("listed", "pending", "dismissed", "not_totaled"):
        sentence = charge_text.bill_sentence(state)
        fix = sentence[0].lower() + sentence[1:].rstrip(".")
    elif quote:
        fix = "dismiss this entry, or pick a quote that does not state it and change the summary to match in the same edit"
    else:
        fix = "dismiss this entry, or edit the summary to remove it"
    return f"states a dollar amount, not exported ({fix})"


def _reconcile(v):
    in_letter = {e["record_no"] for e in v.in_entries}
    lines = []
    for r in sorted(v.records.values(), key=lambda r: (r.get("date_iso") or "9999", r["n"])):
        n = r["n"]
        if n in in_letter:
            continue
        ents = [e for e in v.entries if e["record_no"] == n]
        if r.get("could_not_process") or r.get("status") in ("failed", "could_not_process"):
            why = "could not process"
        elif any(_status(e) == "in" and not v.verbatim(e) for e in ents):
            why = "excerpt not found in record, not exported"
        elif any(_status(e) == "in" and not v.date_of(e) for e in ents):
            why = "date not confirmed, not exported"
        elif any(_status(e) != "out" and v.states_amount(e) for e in ents):
            why = _held_amount_note(v, n, ents)      # T-139
        elif any(e.get("edit_unconfirmed") for e in ents):
            why = "edited, not yet confirmed against the quote"      # T-134
        elif any(_status(e) == "pending" for e in ents):
            why = "not reviewed"
        elif any(e.get("review_status") == "rejected" for e in ents):
            why = "rejected"
        elif ents:
            why = "dismissed"
        else:
            why = r.get("reason") or "no entry"
        lines.append(f"- {_cap(v.cite(n))} — {why}")
    return lines or [f"- none ({len(v.records)} of {len(v.records)} records included)"]


def _was_edited(e):
    """T-069: an entry stays an edited item after the paralegal accepts it (accept keeps the edit payload and only flips the status),
    so edited-ness is the status OR a stored original that differs from the exported text. Out-of-letter entries are not listed."""
    if e.get("review_status") == "edited" or e.get("edit_unconfirmed"):
        return True
    if _status(e) != "in":
        return False
    return ((e.get("original_summary") is not None and e["original_summary"] != e["summary"])
            or (e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]))


_EDIT_REASON_PHRASE = {"JUDGE_UNAVAILABLE": "second check not available", "FIXTURE_MISS": "second check not available",
                       "JUDGE_PARTIAL": "the second check only partly supported it", "JUDGE_UNSUPPORTED": "the second check did not support it",
                       "JUDGE_UNSURE": "the second check was unsure", "JUDGE_DISAGREES": "the second check disagreed"}      # T-167: plain words, never the reason code


def _edit_unconfirmed_why(e) -> str:
    codes = list(e.get("edit_state_reasons") or [])
    return "; ".join(_EDIT_REASON_PHRASE.get(c, "still marked for review") for c in codes) or "still marked for review"


def _edit_unconfirmed_phrase(e) -> str:
    """T-134: an edit that is still needs_review is out of the letter until the paralegal accepts it; the notes say it was edited and why it is still open, never that she accepted it."""
    return f"edited; {_edit_unconfirmed_why(e)}; not yet confirmed against the quote, so it is not in the letter (accept it to put it there)"


def _edited(v):
    out = []
    for e in v.entries:
        if e.get("entered_by_reviewer") and _status(e) == "in":
            out.append(f'- {_cap(v.cite(e["record_no"]))}: entered by reviewer' + ("" if v.prepared else " (the AI did not draft this entry)") + f'; summary "{e["summary"]}"'
                       + ".")
        if not _was_edited(e):
            continue
        bits = []
        if e.get("original_summary") is not None and e["original_summary"] != e["summary"]:
            if e.get("original_summary_failed"):        # D-051: AI wording that failed a code check is not printed anywhere in the export
                bits.append(f'summary was {"prepared" if v.prepared else "AI"} wording removed (failed a check: {"; ".join(e["original_summary_failed"])}), now "{e["summary"]}"')
            else:
                bits.append(f'summary was "{e["original_summary"]}", now "{e["summary"]}"')
        if e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]:
            bits.append(f'excerpt was "{e["original_excerpt"]}", now "{e["excerpt"]}"')
        tail = (f" ({_edit_unconfirmed_phrase(e)})" if e.get("edit_unconfirmed") else
                f" (accepted by the paralegal after comparing it with the quote; {_edit_unconfirmed_why(e)})" if e.get("edit_state_reasons") and _status(e) == "in" else "")
        out.append(f"- {_cap(v.cite(e['record_no']))}: " + "; ".join(bits or ["edited"]) + "." + tail)
    return out or ["- none"]


def _pending(v):
    out = []
    for e in v.entries:
        if e.get("edit_unconfirmed") and not e.get("code_check_failed"):
            out.append(f'- Entry, {v.cite(e["record_no"])}: "{e["summary"]}" ({_edit_unconfirmed_phrase(e)})')
        elif _status(e) == "pending" and e.get("code_check_failed"):       # D-051: the wording fails a code check, so it is not printed anywhere in the export
            out.append(f'- Entry, {v.cite(e["record_no"])}: summary not shown, a code check on it fails (edit it to match the quote, or dismiss it)')
        elif _status(e) == "pending":
            out.append(f'- Entry, {v.cite(e["record_no"])}: "{e["summary"]}"' + (" [entered by reviewer]" if e.get("entered_by_reviewer") else ""))
    for a in v.amounts:
        if _status(a) == "pending":
            out.append(f'- Amount {_money_short(a.get("cents"), a.get("raw", ""))} ({a["cls"]}), {v.cite(a["record_no"])}: '
                       f'"{_amount_quote(v, a)}"')
    for f in v.flags:
        if _status(f) == "pending":
            out.append("- Flag, " + _flag_line(v, f))
    return out


def _cite_tail(v, entry_id):
    e = next(x for x in v.entries if x["id"] == entry_id)
    return f"{v.source(e['record_no'])}, {_long_date(v.date_of(e))}"


def _removed_why(r) -> str:
    """T-167: the plain sentence for a removed narrative sentence; the reason code is in the API field, not in the notes."""
    m = r.get("message")
    return m if m and not re.search(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\b", m) else "it failed a check"


def _draft_paragraph(v):
    n = v.narrative
    if not n:
        return []
    live = {e["id"]: e for e in v.in_entries}
    st = n.get("status", "pending")
    prep = getattr(v, "prepared", False)
    lines = ["", f"DRAFT TREATMENT PARAGRAPH ({'drafted' if prep else 'AI-drafted'} from accepted entries; each sentence cites one entry and passed code checks and the second check)"]
    lines.append({"pending": "- Not in the letter until you accept it.", "dismissed": "- Dismissed; not in the letter.",
                  "accepted": "- Accepted: included in the letter as TREATMENT SUMMARY."}.get(st, "- Not in the letter."))
    for s in n.get("sentences", []):
        e = live.get(s["entry_id"])
        stale = e is None or (n.get("basis") or {}).get(s["entry_id"]) != basis_hash(e)
        tag = "" if st != "accepted" or not stale else " [NOT in the letter: the cited entry changed or is no longer accepted]"
        lines.append(f'- {s["text"]} ({s.get("cite") or s["entry_id"]}){tag}')
    for r in n.get("removed", []):
        if r["reason"] in NARRATIVE_CODE_REASONS:       # D-051: wording that failed a code check is not printed anywhere in the export
            lines.append(f'- {"Prepared" if prep else "AI"} wording removed (failed a check: {_removed_why(r)}) ({r["entry_id"]}).')
        elif r["reason"] == "NOT_AN_ACCEPTED_ENTRY":     # T-106: no quote to check this sentence against, so its wording is never printed either
            lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r["entry_id"]}).')
        else:
            lines.append(f'- Removed: "{r["text"]}" ({r["entry_id"]}): {_removed_why(r)}')
    return lines


def _notes(v):
    accepted = [f for f in v.flags if _status(f) == "in"]
    dismissed = [f for f in v.flags if f.get("review_status") in OUT]
    pending = _pending(v)
    sec = [
        NOTES_TITLE, "",
        (AI_LINE_PREPARED if v.prepared else AI_LINE).format(n=len(pending)), "",
        "FLAGS ACCEPTED", *_flag_block(v, accepted), "",
        "FLAGS DISMISSED", *_flag_block(v, dismissed), "",
        FLAGGED_HEADING, *_flagged_language(v, v.flags), "",
        "AMOUNTS NOT TOTALED", *_amounts_not_totaled(v), "",
        *(["POSSIBLE OVERLAPS (check before relying on the charges total)", *_overlaps(v), ""] if v.overlaps else []),
        "DAMAGES MENTIONS (not charges)", *_damages(v), "",
        "FUTURE TREATMENT RECOMMENDED (no cost stated)", *_future(v), "",
        *(["CHARGES WITHOUT A CERTAIN DATE OF SERVICE", *_undated_charges(v), ""] if _undated_charges(v) else []),
        "BILLS TO REQUEST (entry in the letter, no accepted charge)", *_bills(v), "",
        "RECORDS NOT IN THE TREATMENT SECTION", *_reconcile(v), "",
        "EDITED ITEMS", *_edited(v), "",
        "PENDING ITEMS NOT INCLUDED", *(pending or ["- none"]),
        *_draft_paragraph(v),
    ]
    return "\n".join(sec)


def split_letter(letter_text: str):
    """(treatment lines, billed-charges lines) of a finished letter. The BILLED CHARGES section is the last header line (followed by a blank line) before the R-EX-8 total
    line, which is the last line of the letter; with no total line there is no charges section. Split by structure, never on the words appearing in a quote."""
    lines = (letter_text or "").split("\n")
    if lines and lines[-1].startswith(TOTAL_PREFIX):
        for k in range(len(lines) - 2, -1, -1):
            if lines[k] == CHARGES_TITLE and k + 1 < len(lines) and (lines[k + 1] == "" or lines[k + 1].startswith(TOTAL_PREFIX)):
                return lines[:k], lines[k:]
    return lines, []


_CHARGE_HEAD = re.compile(r"^(.*): (\$[\d,]+\.\d\d)$")


def _charge_groups(tail):
    """[(index of the header line, header, [quote lines])] of a BILLED CHARGES section: a header ends with ': $X.XX', the lines up to the next header (or the blank line before the
    total line) are that charge's quote."""
    groups = []
    for k, line in enumerate(tail):
        if k < 2 or line.startswith(TOTAL_PREFIX):
            continue
        if _CHARGE_HEAD.match(line):
            groups.append((k, line, []))
        elif groups and line != "":
            groups[-1][2].append(line)
    return groups


def _blocker(line_no, line, exprs, why, act, owner, kind):
    return {"item_id": owner["id"] if owner else None, "kind": kind if owner else "case", "reason_code": "MONEY_IN_LETTER", "line": line_no, "text": line,
            "expressions": exprs, "why": why, "next_action": act}


def _shown(line):
    line = line.strip()
    return line if len(line) <= 140 else line[:137] + "..."


def letter_money_blockers(letter_text: str, entries=(), charges=()) -> list:
    """T-139 r4/r5 (D-019, R-CH-7, R-EX-8): the export gate on the FINAL letter text. Any money expression outside the R-EX-8 total line and the accepted-charge lines is a
    blocker naming the line, whatever put it there (an AI summary, a quote, a paralegal's edit, a narrative sentence). Round 5: the BILLED CHARGES section is scanned too. A
    charge carries only its own amount: its header line is '<provider>, <date>: $X.XX', and on its quote lines the one figure equal to X is allowed; any other money
    expression (a paid or adjusted figure, patient responsibility, wages, a second charge) blocks. One shared detector (app/backend/money.py), the one the hold and the letter
    eval use. `entries` (the letter's in_entries) and `charges` (its in_charges, same order as the section) only let a blocker name the item to fix.
    [{item_id, kind, reason_code: MONEY_IN_LETTER, line (1-based), text, expressions, why, next_action}]"""
    head, tail = split_letter(letter_text)
    found = {}
    for i, line, expr in money.lines_with_money(head):
        found.setdefault(i, (line, []))[1].append(expr)
    out = []
    for i in sorted(found):
        line, exprs = found[i]
        owner = next((e for e in entries if any(_norm(x) in _norm(f"{e.get('summary')} {e.get('excerpt')}") for x in exprs)), None)
        in_summary = bool(owner) and any(_norm(x) in _norm(owner.get("summary")) for x in exprs)
        what = ", ".join(f"\u2018{x}\u2019" for x in exprs)
        why = (f"Line {i + 1} of the letter states an amount ({what}): \u201c{_shown(line)}\u201d. Amounts go only in the Billed charges section, never in a treatment entry.")
        act = ({"code": "EDIT_SUMMARY" if in_summary else "EDIT_QUOTE", "target": {"item_id": owner["id"]},
                "text": ("Edit the summary to remove the amount, or dismiss the entry." if in_summary else "Pick a quote that does not state the amount (and make the summary match), or dismiss the entry.")
                + " The export stays blocked until it passes."}
               if owner else {"code": "EDIT_SUMMARY", "text": "Remove the amount from the line named above, or dismiss the item it comes from. The export stays blocked until it passes."})
        out.append(_blocker(i + 1, line, exprs, why, act, owner, "entry"))
    base = len(head)
    groups = _charge_groups(tail)
    for g, (k, header, quotes) in enumerate(groups):
        owner = charges[g] if len(charges) == len(groups) else None
        figure = _CHARGE_HEAD.match(header).group(2)
        own_cents = amounts.to_cents(figure.lstrip("$"))
        bad, spent = [], False
        bad += [(k, header, h) for h in money.strings(_CHARGE_HEAD.match(header).group(1))]      # the header names a provider and a date: no money in it
        for q, qline in enumerate(quotes):
            for hit in money.hits(qline):
                text, kind = hit[2], hit[3]
                if not spent and kind in ("dollar", "sign") and amounts.to_cents(text.lstrip("$ ").strip()) == own_cents:
                    spent = True                                                                  # the charge's own figure, once
                    continue
                bad.append((k + 1 + q, qline, text))
        by_line = {}
        for n, line, h in bad:
            by_line.setdefault(n, (line, []))[1].append(h)
        for n in sorted(by_line):
            line, exprs = by_line[n]
            what = ", ".join(f"\u2018{x}\u2019" for x in exprs)
            why = (f"Line {base + n + 1} of the letter is a Billed charges line for {figure} and also states {what}: \u201c{_shown(line)}\u201d. A charge line carries its own amount only.")
            act = ({"code": "DISMISS_OR_ENTER_BY_HAND", "target": {"item_id": owner["id"]},
                    "text": "Dismiss this charge (its amount stays in the internal notes), or enter the charge by hand. The export stays blocked until it passes."}
                   if owner else {"code": "DISMISS_OR_ENTER_BY_HAND", "text": "Dismiss the charge named above, or enter it by hand. The export stays blocked until it passes."})
            out.append(_blocker(base + n + 1, line, exprs, why, act, owner, "amount"))
    return out


def money_blockers_for_case(case: dict) -> list:
    """The MONEY_IN_LETTER blockers of a case dict (T-139 r4). Both letter styles are scanned and merged (one blocker per offending entry and expression set, the first style's
    line number), so the answer does not depend on the style asked for, and the trace export gate (trace.export_blockers) and GET /export give the same answer."""
    v = _View(case)
    out, seen = [], set()
    for st in (None, "oneline"):
        for b in letter_money_blockers(_letter(v, st), v.in_entries, v.in_charges):
            key = (b["item_id"], tuple(_norm(x) for x in b["expressions"]))
            if key not in seen:
                seen.add(key)
                out.append(b)
    return out


class ExportBlocked(Exception):
    """The export refuses (D-044, D-045): a run in progress or failed, nothing accepted, or accepted AI-made items whose second check never ran. No override.
    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
    Pending items are not blockers: they stay out of the letter and the AI disclosure line counts them."""

    def __init__(self, items):
        self.items = list(items)
        super().__init__(self.items[0]["reason_code"] if self.items else "EXPORT_BLOCKED")

    @property
    def code(self) -> str:
        return "judge_not_run" if self.items and all(i.get("reason_code") == "JUDGE_NOT_RUN" for i in self.items) else "export_blocked"


class JudgeNotRun(ExportBlocked):
    """D-044 alias kept for callers that only care about the judge dimension."""


def build_export(case: dict, style: str = None, check_letter: bool = True) -> dict:
    """Pure function: reviewed items in, two text blocks out. Deterministic; no I/O; no flags reach the letter.
    Raises JudgeNotRun when the case lists accepted items whose judge never ran (`case["judge_not_run"]`, set by store.export_case). The run-state and nothing-accepted
    blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
    if case.get("judge_not_run"):
        raise JudgeNotRun(case["judge_not_run"])
    v = _View(case)
    letter = _letter(v, style)
    blockers = money_blockers_for_case(case) if check_letter else []      # T-139 r4: the final text, checked by the shared money detector; nothing is dropped silently
    if blockers:
        raise ExportBlocked(blockers)
    notes = _notes(v)
    in_letter = {e["record_no"] for e in v.in_entries}
    pend = _pending(v)
    counts = {  # R-EX-5 count line: shown by the UI outside both blocks, never inside them
        "entries": len(v.in_entries),
        "charges": len(v.in_charges),
        "flags_in_notes": sum(1 for f in v.flags if _status(f) == "in"),
        "records_in_letter": len(in_letter),
        "records_total": len(v.records),
        "pending": len(pend),
        "pending_flags": sum(1 for f in v.flags if _status(f) == "pending"),
    }
    return {"letter_text": letter, "internal_notes_text": notes, "counts": counts}
