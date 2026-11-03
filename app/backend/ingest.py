"""Stage 0 ingest (all code): split, header date/source, kind, duplicate merge, limits, injection tag, warnings.
R-IN-1, R-IN-3..5, R-TL-3, R-TL-7, R-TL-9, R-RV-6; LLM_VS_CODE rows 1, 2, 3, 16, 17. No model is called here: the D-031 split fallback takes an injected `splitter` callable.
Record text is never rewritten: every excerpt is a verbatim slice of the (newline-normalised) input."""
import re
import unicodedata

from app.backend import dates, flag_templates, injection, lexicon

MAX_CHARS = 60000
MAX_RECORDS = 40

# The only text ever set aside as a non-record: the exact banner lines of the golden/sample files. Any other first line is kept as text.
BANNERS = ("SYNTHETIC — invented for evaluation; not real patient data",
           "SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data")

_HEADER = re.compile(r"^=== Record (\d+) ===[ \t]*$", re.MULTILINE)
_SEP = re.compile(r"^[ \t]*---+[ \t]*$", re.MULTILINE)
_DATE_LINE = re.compile(r"^Date:", re.MULTILINE)
_F_DATE = re.compile(r"^Date:[ \t]*(.*)$", re.MULTILINE)
_F_SRC = re.compile(r"^Source:[ \t]*(.*)$", re.MULTILINE)
_F_EXC = re.compile(r"^Excerpt:[ \t]*", re.MULTILINE)


class IngestError(ValueError):
    """Input refused before any processing; str(e) is the API error code ('bad_request' | 'input_too_large')."""

    @property
    def code(self) -> str:
        return str(self)


_LONE_SURROGATE = re.compile("[\ud800-\udfff]")


def replace_lone_surrogates(raw: str) -> str:
    return _LONE_SURROGATE.sub("\ufffd", raw)


def clean_chars(raw: str) -> str:
    """T-178 (GATE-M3 chaos): characters that are not text. A lone UTF-16 surrogate (half an emoji; it cannot be encoded, so it used to be a 500) becomes U+FFFD, and every
    format character (Unicode category Cf: zero-width space/joiner, word joiner, BOM, bidi marks, soft hyphen, tag characters) is removed, so a paste of only invisible
    characters is empty. What is left is the text the paralegal can see; it is what is stored, hashed and quoted."""
    return "".join(ch for ch in replace_lone_surrogates(raw) if unicodedata.category(ch) != "Cf")


def normalize_text(raw: str) -> str:
    """CRLF and CR become LF; format characters removed and lone surrogates replaced (clean_chars); leading and trailing whitespace trimmed (api.md POST /api/cases)."""
    return clean_chars(raw or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def check_limits(text: str, max_chars: int = MAX_CHARS) -> str:
    """Raise before anything else (and so before any LLM call): empty -> bad_request, oversize -> input_too_large."""
    t = normalize_text(text)
    if not t:
        raise IngestError("bad_request")
    if len(t) > max_chars:
        raise IngestError("input_too_large")
    return t


def _spans(text: str):
    """Candidate block (start, end) spans and the method that found them; None when nothing is confident."""
    heads = [m.start() for m in _HEADER.finditer(text)]
    if heads:
        return list(zip(heads, heads[1:] + [len(text)]))
    if _SEP.search(text):
        cuts = [0] + [x for m in _SEP.finditer(text) for x in (m.start(), m.end())] + [len(text)]
        return [(cuts[i], cuts[i + 1]) for i in range(0, len(cuts), 2)]
    starts = [m.start() for m in _DATE_LINE.finditer(text)]
    if starts and (_F_SRC.search(text) or _F_EXC.search(text)):
        return list(zip(starts, starts[1:] + [len(text)]))
    return None


def _excerpt_extent(rest: str):
    """(excerpt, consumed_chars) for the text after 'Excerpt:'. A quoted excerpt ends at the first line that ends with a quote;
    anything after it is NOT part of the excerpt (it surfaces as unsplit text). Unquoted or unterminated: the rest of the block."""
    if rest.startswith('"'):
        i = 0
        while True:
            j = rest.find("\n", i)
            seg = rest[i:len(rest) if j < 0 else j].rstrip()
            if seg.endswith('"') and i + len(seg) > 1:
                return rest[1:i + len(seg) - 1], i + len(seg)
            if j < 0:
                break
            i = j + 1
    return rest.strip(), len(rest.rstrip())


def _scan_block(text: str, a: int, b: int):
    """Parse one block. Returns (fields | None, covered spans). Covered spans are absolute; whatever lies outside them is leftover."""
    block = text[a:b]
    cov, f = [], {"date_raw": "", "source": "", "excerpt": "", "complete": False}
    h = _HEADER.match(block)
    if h:
        cov.append((a, a + h.end()))
    found = 0
    for key, pat in (("date_raw", _F_DATE), ("source", _F_SRC)):
        m = pat.search(block)
        if m:
            f[key] = m.group(1).strip()
            cov.append((a + m.start(), a + m.end()))
            found += 1
    e = _F_EXC.search(block)
    if e:
        exc, used = _excerpt_extent(block[e.end():])
        f["excerpt"] = exc
        cov.append((a + e.start(), a + e.end() + used))
        found += 1
    f["complete"] = found == 3
    return (f if found else None), cov


def _leftovers(text: str, cov: list):
    """Non-blank segments of `text` not inside any covered span, as (start, end); an exact golden banner line (BANNERS) on line 1 is exempt."""
    out, pos = [], 0
    for s, e in sorted(cov) + [(len(text), len(text))]:
        if s > pos:
            seg = text[pos:s]
            if seg.strip():
                lead = len(seg) - len(seg.lstrip())
                out.append((pos + lead, pos + len(seg.rstrip())))
        pos = max(pos, e)
    return [(s, e) for s, e in out if not (s == 0 and text[s:e] in BANNERS)]


def _split(text: str):
    """(records, method). Every non-blank character of the input ends up inside some record; text outside a recognised block becomes
    an `unsplit` record (D-027) and the split is reported ambiguous."""
    spans = _spans(text)
    if not spans:
        return [_record(1, text, 0, len(text), {"date_raw": "", "source": "", "excerpt": text})], "ambiguous"
    items, method = [], "code"
    cov_all = [] if _HEADER.search(text) else [(m.start(), m.end()) for m in _SEP.finditer(text)]   # separator lines carry no content
    for a, b in spans:
        f, cov = _scan_block(text, a, b)
        cov_all += cov
        if f is None:
            continue
        if not f["complete"]:
            method = "ambiguous"
        end = max(e for _, e in cov)
        f["first"] = min(x for x, _ in cov)             # where the block's own fields start (a block can begin with a preamble line)
        items.append((a, end, f))
    for s, e in _leftovers(text, cov_all):
        items.append((s, e, {"date_raw": "", "source": "", "excerpt": text[s:e], "unsplit": True}))
        method = "ambiguous"
    # T-129: record numbers are the paralegal's citations, so they count only the real records, in paste order. Unsplit text (a preamble, a note between separators) is kept
    # (D-027: nothing is dropped) but numbered AFTER the real records, so a fax cover sheet on top never shifts "record 1" to "record 2". Text above the first real record
    # is marked `preamble`.
    items.sort(key=lambda t: (bool(t[2].get("unsplit")), t[0]))
    first_real = min((f["first"] for _a, _e, f in items if not f.get("unsplit")), default=None)
    for _a, e, f in items:
        if f.get("unsplit") and first_real is not None and e <= first_real:
            f["preamble"] = True
    return [_record(i + 1, text[a:e], a, e, f) for i, (a, e, f) in enumerate(items)], method


def _record(n: int, block: str, start: int, end: int, p: dict) -> dict:
    return {"n": n, "date_raw": p["date_raw"], "source": p["source"], "excerpt": p["excerpt"],
            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit")), "preamble": bool(p.get("preamble"))}


class SplitFailed(Exception):
    """The model could not give a split (call failed, no recorded answer, unusable output). `code` is a reason code; never model text."""
    def __init__(self, code: str, replayed: bool = False):
        super().__init__(code)
        self.code = code
        self.replayed = replayed           # True: the reason was stored by an earlier run; no call was made, so it is not a new failure


def validate_split(text: str, spans, max_records: int = None) -> list:
    """Code check on the model's record boundaries (D-031). `spans` = [(start, end)]. Valid only if they cover `text` exactly
    (first start 0, each end == next start, last end == len(text)), every start falls on a line start, and there are at least two.
    Returns the list of (start, end) or raises ValueError; the caller then keeps the single unsplit record."""
    sp = [(int(a), int(b)) for a, b in spans]
    if max_records is not None and len(sp) > max_records:
        raise ValueError("SPLIT_TOO_MANY")
    if len(sp) < 2 or sp[0][0] != 0 or sp[-1][1] != len(text):
        raise ValueError("SPLIT_NOT_COVERING")
    for i, (a, b) in enumerate(sp):
        if not a < b or (i and a != sp[i - 1][1]):
            raise ValueError("SPLIT_NOT_CONTIGUOUS")
        if a and text[a - 1] != "\n":
            raise ValueError("SPLIT_NOT_ON_LINE_START")
        if not text[a:b].strip():
            raise ValueError("SPLIT_EMPTY_RECORD")
    return sp


def numbered(text: str) -> str:
    """The text with an '@OFFSET| ' label on every line, so the model can name boundaries without counting characters."""
    out, pos = [], 0
    for line in text.split("\n"):
        out.append(f"@{pos}| {line}")
        pos += len(line) + 1
    return "\n".join(out)


def _llm_records(text: str, spans: list) -> list:
    """Records from validated spans. Fields come from code only (labelled lines, or a first line that parses as a date)."""
    out = []
    for a, b in spans:
        s0 = a + (len(text[a:b]) - len(text[a:b].lstrip()))
        first_line = text[s0:b].split("\n", 1)[0].rstrip()
        if s0 == 0 and first_line in BANNERS:       # the golden banner line belongs to no record
            s0 += len(first_line)
            s0 += len(text[s0:b]) - len(text[s0:b].lstrip())
        e0 = a + len(text[a:b].rstrip())
        if s0 >= e0:
            continue
        f, _cov = _scan_block(text, s0, e0)
        f = f or {"date_raw": "", "source": "", "excerpt": "", "complete": False}
        if not f["excerpt"]:
            f["excerpt"] = text[s0:e0].strip()
        if not f["date_raw"]:
            first = text[s0:e0].split("\n", 1)[0].strip()
            left, _, right = re.split(r"(\s+[\u2014\u2013|-]\s+)", first, maxsplit=1)[:3] if re.search(r"\s+[\u2014\u2013|-]\s+", first) else (first, "", "")
            if dates.parse_date(left.strip())["status"] == "parsed":     # 'May 4, 2026 - Pottsworth Emergency Department' or a bare date line
                f["date_raw"] = left.strip()
                if right.strip() and not f["source"]:
                    f["source"] = right.strip()
                    f["excerpt"] = text[s0:e0].split("\n", 1)[1].strip() if "\n" in text[s0:e0] else f["excerpt"]
        out.append(_record(len(out) + 1, text[s0:e0], s0, e0, f))
    return out


def split_records(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS) -> list:
    text = check_limits(raw_text, max_chars)
    recs, _ = _split(text)
    if len(recs) > max_records:
        raise IngestError("input_too_large")
    return recs


def record_kind(source: str, excerpt: str = "") -> str:
    """encounter | billing_statement | phone_note (| records_admin), decided by the lexicon `non_encounter` list on the header label only (D-003)."""
    if not (source or "").strip():
        return "unsplit_text"
    for e in lexicon.code_list("non_encounter"):
        if e["regex"].search(source or ""):
            return {"billing_document": "billing_statement", "phone_or_message": "phone_note"}.get(e["id"], "records_admin")
    return "encounter"


def _norm(s: str) -> str:
    return " ".join((s or "").split()).casefold()


def dedupe(records: list) -> list:
    """Groups of record numbers (in file order): same date + same normalised provider label + same normalised text merge (R-TL-7)."""
    groups, order = {}, []
    for r in records:
        p = dates.parse_date(r["date_raw"])
        key = (p["iso"] or _norm(r["date_raw"]), _norm(r["source"]), _norm(r["excerpt"]))
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(r["n"])
    return [sorted(groups[k]) for k in order]


_PHI = [re.compile(p, re.IGNORECASE) for p in (
    r"\b\d{3}-\d{2}-\d{4}\b",                                  # SSN
    r"(?<!\d)(?:\(\d{3}\)\s?|\d{3}[-.\s])\d{3}[-.\s]\d{4}\b",  # phone
    r"\bMRN\s*[:#]?\s*[A-Z0-9-]{5,}")]                         # MRN


def _warn(code: str, message: str, item_id=None) -> dict:
    return {"code": code, "message": message, "item_id": item_id}


def warnings(raw_text: str) -> list:
    return ingest(raw_text)["warnings"]


def ingest(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS, splitter=None, not_duplicates=(), prep=False) -> dict:
    """Everything stage 0 knows. Zero model calls unless `splitter(text) -> [(start, end)] | None` is given AND the code split found one
    unsplit block (D-031); its answer is accepted only if validate_split passes, else the single record stays.
    `not_duplicates`: record ids ('r2') the paralegal said are NOT duplicates of the record they matched; they stay separate (D-031).
    `prep` (D-069): the split answer is a prepared one, so the warnings say so instead of naming an AI.
    Raises IngestError('bad_request'|'input_too_large') first."""
    text = check_limits(raw_text, max_chars)
    recs, method = _split(text)
    llm_split, split_failure, split_detail, split_call_id = False, None, None, None
    eligible = method == "ambiguous" and len(recs) == 1 and (recs[0]["unsplit"] or not (recs[0]["date_raw"] and recs[0]["source"]))
    if eligible and not splitter:
        split_failure = "NO_MODEL"         # an unsplit paste with no model or fixture to propose boundaries: say so, never pass silently
    elif method == "ambiguous" and not eligible and len(recs) > 1:
        split_failure = "NOT_ATTEMPTED"    # several records plus an unsplit tail: the model is only asked about a single block, so say that
        # (one labelled but incomplete record gets no reason: SPLIT_AMBIGUOUS already describes it, and "several records" would be false)
    if splitter and eligible:
        try:
            got = splitter(text)
        except SplitFailed as e:           # the model did not answer: keep the one record and say why (never swallowed silently)
            got, split_failure, split_detail = None, e.code, None if e.replayed else e.code
            if e.code == "FIXTURE_MISS":   # no recorded answer is the same user-facing state as no model; the detail stays for the run's error entry
                split_failure = "NO_MODEL"
        if got is not None:
            spans, split_call_id = got if isinstance(got, tuple) else (got, None)
            try:
                checked = validate_split(text, spans or [], max_records)
            except ValueError as e:        # the code check refused the proposal: keep the one record, with the reason code
                split_failure = str(e) if str(e).startswith("SPLIT_") else "SPLIT_INVALID"
            else:
                recs, method, llm_split = _llm_records(text, checked), "llm", True
    if len(recs) > max_records:
        raise IngestError("input_too_large")
    groups = dedupe(recs)
    if not_duplicates:
        nd = {int(str(i)[1:]) for i in not_duplicates if str(i)[1:].isdigit()}
        out = []
        for grp in groups:
            out.append([grp[0]] + [n for n in grp[1:] if n not in nd])
            out += [[n] for n in grp[1:] if n in nd]
        groups = out
        groups.sort(key=lambda g: g[0])
    first_of = {n: g[0] for g in groups for n in g}
    warns, to_confirm, record_warnings = [], [], []
    if llm_split:
        warns.append(_warn("LLM_SPLIT", f"The pasted text had no recognisable record markers; {'a prepared answer' if prep else 'the AI'} proposed the record boundaries and code checked them. Check the split."))
    elif method == "ambiguous":
        warns.append(_warn("SPLIT_AMBIGUOUS", "Record boundaries could not be found with confidence; check the split."))
        if split_failure:
            if split_failure == "NOT_ATTEMPTED":
                msg = f"The paste has several records and some text outside them; {'only a single unsplit block can be split by a prepared answer' if prep else 'the AI is only asked to split a single unsplit block'}, so that text stays its own record (NOT_ATTEMPTED)."
            elif split_failure == "NO_MODEL":
                msg = "No prepared answer was available to propose record boundaries; the paste stays one record." if prep else "No model was available to propose record boundaries; the paste stays one record."
            else:
                msg = ("The prepared record boundaries" if prep else "The AI's proposed record boundaries") + " were not used (" + split_failure + "); the paste stays one record."
            warns.append(_warn("SPLIT_REJECTED", msg))
    if any(len(g) > 1 for g in groups):
        warns.append(_warn("DUPLICATE_MERGED", "Identical records were merged into one entry that cites all of them."))
    if any(p.search(text) for p in _PHI):
        warns.append(_warn("PHI_PATTERN", "Text looks like it contains an SSN, phone number or MRN. This tool is for synthetic data only."))
    for r in recs:
        p = dates.parse_date(r["date_raw"])
        kind = record_kind(r["source"], r["excerpt"])
        hits = [{**h, "field": "excerpt"} for h in injection.scan(r["excerpt"])] + \
               [{**h, "field": "source"} for h in injection.scan(r["source"])]
        rid = f"r{r['n']}"
        r.update(id=rid, seq=r["n"], date_iso=p["iso"], date_status=p["status"], date_candidates=p["candidates"], kind=kind,
                 encounter=kind == "encounter", duplicate_of=None if first_of[r["n"]] == r["n"] else f"r{first_of[r['n']]}",
                 injection_tag=bool(hits), injection_hits=hits)
        if llm_split:
            line = r["excerpt"].split("\n", 1)[0][:160]
            at = r["text"].find(line)
            record_warnings.append({"type": "record_warning", "category": "llm_split", "record_no": r["n"], "call_id": split_call_id,
                                    "evidence": [{"field": "excerpt", "text": line, "start": r["char_start"] + at if at >= 0 else None,
                                                  "end": r["char_start"] + at + len(line) if at >= 0 else None}]})
        if r["unsplit"]:
            warns.append(_warn("UNSPLIT_TEXT", "Text outside any recognised record was kept as its own record; check it and add separators if it belongs to one.", rid))
        if p["status"] != "parsed":
            to_confirm.append({"record_id": rid, "raw": r["date_raw"], "candidates": p["candidates"]})
            warns.append(_warn("DATE_EXCLUDED_FROM_GAPS", "A record date is ambiguous or unreadable; it is left out of gap checks until confirmed.", rid))
            record_warnings.append({"type": "record_warning", "category": "date_ambiguous", "record_no": r["n"],
                                    "evidence": [{"field": "date", "text": r["date_raw"]}]})
        if hits:   # one flag per tagged record; evidence = every matched phrase (offsets into the excerpt)
            record_warnings.append({"type": "record_warning", "category": "injection_suspected", "record_no": r["n"],
                                    "evidence": [{"field": h["field"], "text": h["phrase"], "start": h["start"], "end": h["end"]} for h in hits]})
    by_n = {r["n"]: r for r in recs}
    for w in record_warnings:       # title/explanation come from flag_templates only (R-FL-8)
        r = by_n[w["record_no"]]
        ev = w["evidence"][0]["text"]
        w["id"] = f"f_{ {'injection_suspected': 'inj', 'llm_split': 'split'}.get(w['category'], 'date') }_r{r['n']}"
        w["title"], w["explanation"] = flag_templates.render("record_warning", w["category"], provider=r["source"] or None,
                                                             date=r["date_iso"], quote=ev if w["category"] == "injection_suspected" else None,
                                                             raw=r["date_raw"] if w["category"] == "date_ambiguous" else None)
        w["reasons"] = {"injection_suspected": ["INJECTION_SUSPECTED"], "llm_split": ["LLM_SPLIT"]}.get(w["category"], [])
    first = text.split("\n", 1)[0].rstrip()
    return {"banner": first if first in BANNERS else None, "records": recs, "groups": groups, "split_method": method if method in ("code", "llm") else "ambiguous", "split_failure": split_failure, "split_detail": split_detail, "warnings": warns,
            "dates_to_confirm": to_confirm, "record_warnings": record_warnings,
            "injection_records": [r["id"] for r in recs if r["injection_tag"]]}


def evidence_span(rec: dict, field: str, needle: str = None) -> dict:
    """Evidence item for a record: field 'date' | 'source' (the header line) or 'excerpt' (`needle`, a verbatim substring of the record).
    Offsets are absolute in the normalised input when the record carries `text` and `char_start`; otherwise they are None."""
    text, base = rec.get("text"), rec.get("char_start")
    out = {"record_no": rec["n"], "field": field, "text": needle, "start": None, "end": None}
    if field in ("date", "source"):
        pat = _F_DATE if field == "date" else _F_SRC
        m = pat.search(text) if text else None
        out["text"] = m.group(0) if m else (rec.get("date_iso") if field == "date" else rec.get("source"))
        if m and base is not None:
            out["start"], out["end"] = base + m.start(), base + m.end()
    elif text and base is not None and needle:
        i = text.find(needle)
        if i >= 0:
            out["start"], out["end"] = base + i, base + i + len(needle)
    return out
