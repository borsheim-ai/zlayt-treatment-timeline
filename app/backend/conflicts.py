"""Structural conflicts raised by code, no LLM (ADR-014, D-017, D-025; R-FL-2, LLM_VS_CODE row 10).
accident_date_conflicts: stated accident dates (lexicon `accident_date_phrases`) vs the earliest recorded treatment date.
provider_conflicts: the same named clinician under different practice names. The tool never picks a date and never computes a delay."""
import re

from app.backend import dates, flag_templates, gaps, lexicon
from app.backend.ingest import evidence_span

PHRASE_TO_DATE_CHARS = 40

# T-141 r6 / D-061: one closed exemption. A stated accident date later than the earliest record is a conflict when a record dated before it has ANY accident or
# mechanism word (noun or verb: accident, collision, crash, MVC/MVA, rear-end(ed), struck, hit by, pedestrian, impact, injury...) that is not governed by an
# explicit "prior / previous / earlier" ("prior accident", "previously had an MVA") or by a negation of prior accidents ("no prior accidents", "denies previous
# MVA", "Prior accidents: No"). There is no date-distance exemption: "in October 2025", "last year", "years ago" and "in 2019" never exempt a word. A record with
# no such word at all (a routine or annual visit, paperwork) is an earlier visit; the case notes how many (accident_date_note). A false conflict is the safe
# direction (D-055, D-061). A governor reaches only the event noun it directly modifies, through determiners, adjectives and event words, and never across
# "the", a preposition, a verb or a label colon, so "No LOC after the accident" and "History: rear-ended" still refer to the accident.
_EVENT = re.compile(r"\b(?:collisions?|collided|crash\w*|MVAs?|MVCs?|MVIs?|rear[- ]?end\w*|struck|wreck\w*|accident\w*|incidents?|pedestrians?|motor\s+vehicle|vehicular|"
                    r"hits?\s+(?:by|from|at|to|and\s+run)|hits?\s+on\s+the|(?:was|were|got)\s+hit|(?:vehicle|car|truck|driver)\s+hit|hit\s+(?:them|him|us|me)|"
                    r"hit\s+(?:a|the|my|our)\s+(?:car|vehicle|truck|pole|tree|wall|guardrail|curb)|"
                    r"airbag\w*|seat\s?belt\w*|t-?bone\w*|side-?swip\w*|(?:run|ran)\s+over|run-over|"
                    r"fell|fall(?:ing)?\s+(?:from|off|down)|slip(?:ped)?\s+and\s+fall|whiplash|injur\w*(?!\s+prevention)|trauma\w*|impact(?:ed)?\s+(?:with|to|from|on\s+the)|impacts?(?!\s+(?:of|on)\b)|on\s+impact|impacted|LOC|loss\s+of\s+consciousness)\b", re.I)
_NEGATOR = {"no", "not", "denies", "denied", "denying", "without", "never", "negative", "neg", "none", "nor", "free"}
_HIST_WORD = {"prior", "previous", "earlier"}                                                         # D-061: only an explicit prior modifies the event noun (not "prior to")
_HIST_VERBS = {"had", "suffered", "been", "involved", "in", "was"}                                      # "previously had an MVA"; not "previously reported the MVA"
_FILLER = {"a", "an", "any", "all", "some", "other", "further", "known", "recent", "major", "minor", "serious", "significant", "new",
           "motor", "vehicle", "vehicular", "car", "auto", "traffic", "head", "neck", "back", "rear", "end"}      # words a negator or history word may reach through to the event noun
_LINKS = {"or", "and", "of", "for", "with"}                                                              # T-141 r6 (F1): a governor crosses these only to an injury word ('no prior accidents or injuries', 'previous accident with whiplash')
_INJURY = re.compile(r"whiplash|injur\w*|trauma\w*|LOC|loss\s+of\s+consciousness", re.I)                      # never an accident or mechanism: 'No injury or rear-ended' keeps the second event ungoverned
_PLURAL_REFERENT = {"this", "these", "the", "current", "currently", "latest", "recent", "last", "now", "today"}  # T-141 r6 (F3): a labelled plural list that points at the index event is not history
_HISTORY_LABEL = re.compile(r"(?:history|hx|pmh)(?:\s+\w+){0,2}:")                                       # "History per patient:" / "Hx:"
_PLURAL_EVENT = re.compile(r"(?:accidents|collisions|crashes|wrecks|MVAs|MVCs|MVIs)", re.I)         # T-141 r6: the lib11 PCP list ("History per patient: car accidents in 2019 and 2022"); a plural event under a history label is a list of past events
_CLAUSE_SPLIT = re.compile(r"[;,]|\s[-\u2013\u2014]\s|\s\(|\)")


def _governed(clause: str, m, plural_ok: bool = True) -> bool:
    """The event word is generic history when a negator or a history word governs it: walk back from it over determiners, adjectives, the nouns of a compound
    ('motor vehicle collision') and other event words; reaching a negator ('no prior accidents', 'denies any collision or injury') or a history word ('prior
    accident', 'previously had an MVA') ends the walk as history. Anything else ('the', a preposition, a verb, a noun, a label colon, 'prior to')
    ends it as a reference to the accident itself. T-141 r6 (F1): a governor carries across 'and', 'or', 'with', 'for', 'of' only to an injury word; a
    second accident or mechanism word after one is a new event, ungoverned."""
    toks = clause[:m.start()].split()
    crossed = False
    for i in range(len(toks) - 1, -1, -1):
        raw = toks[i]
        w = raw.strip(".:()\"'?[]").lower()
        if raw.endswith(":") or not w:                                                    # a label ("History:", "Allergies:") closes the scope
            return bool(raw.endswith(":") and _HISTORY_LABEL.fullmatch(" ".join(toks[:i + 1]).lower()) and _PLURAL_EVENT.fullmatch(m.group(0)) and plural_ok)
        if w in _NEGATOR or w in _HIST_WORD or (w in _HIST_VERBS and i and any(t.strip(".:()\"'?[]").lower() == "previously" for t in toks[max(0, i - 2):i])):
            return not crossed or bool(_INJURY.fullmatch(m.group(0)))
        if w in _LINKS:
            crossed = True
            continue
        if w in _FILLER or _EVENT.fullmatch(w):
            continue
        return False
    return False


_MONTH = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?"
_TWO_DIGIT_YEARS = re.compile(                                                        # a two-digit year in a date shape; the year is the one group that matched
    r"(?<![\d/.\-])(?:0?[1-9]|[12]\d|3[01])[/.\-](?:0?[1-9]|[12]\d|3[01])[/.\-](\d{2})(?!\d)"        # 1/3/26, 01/03/26, 1-3-26, 01.03.26
    r"|(?<![\d/.\-])(?:0?[1-9]|1[0-2])/(\d{2})(?!\d)"                                            # 1/26 (month/year)
    r"|\b" + _MONTH + r"\s+\d{1,2}(?:st|nd|rd|th)?,?\s+(\d{2})(?!\d)"                                # Jan 3, 26
    r"|\b\d{1,2}(?:st|nd|rd|th)?\s+" + _MONTH + r",?\s+(\d{2})(?!\d)",                                # 3rd Jan 26
    re.I)


def _plural_list_ok(unit: str, iso) -> bool:
    """T-141 r6 (F3): the plural-under-a-history-label exemption holds only when the whole sentence names no date on or after the stated accident date (a year
    counts at its year) and no referent word ('this one', 'the latest', 'current'): 'History per patient: accidents, this one on 01/03/2026' is the accident."""
    if any(w.strip(".,;:()\"'").lower() in _PLURAL_REFERENT for w in unit.split()):
        return False
    if not iso:
        return True
    if any(d["status"] == "parsed" and d["iso"] >= iso for d in dates.find_dates(unit)):
        return False
    if any(int(y) >= int(iso[:4]) for y in re.findall(r"\b((?:19|20)\d\d)\b", unit)):
        return False
    return not any(2000 + int(next(g for g in m if g)) >= int(iso[:4]) for m in _TWO_DIGIT_YEARS.findall(unit))     # T-141 r7 (F1): '1/3/26' reads as 2026


def _describes_event(rec: dict, iso=None) -> bool:
    """D-061: the record has ANY injury, mechanism or accident word not governed by an explicit prior/previous/earlier or a negation (judged per clause and per word)."""
    from app.backend import sentences
    text = rec.get("excerpt") or ""
    for a, b in sentences.stripped_spans(text):
        unit = text[a:b]
        plural_ok = _plural_list_ok(unit, iso)
        for d in dates.find_dates(unit):                                     # "January 9, 2026" is one date, not two clauses
            unit = unit[:d["start"]] + d["text"].replace(",", "\x01") + unit[d["end"]:]
        for clause in (c.replace("\x01", ",") for c in _CLAUSE_SPLIT.split(unit)):
            for m in _EVENT.finditer(clause):
                if not _governed(clause, m, plural_ok):
                    return True
    return False


def _event_records(s: dict, records: list) -> list:
    """Records dated before the stated date that describe the collision itself."""
    return [o for o in records if o.get("date_iso") and o["date_iso"] < s["iso"] and _describes_event(o, s["iso"])]


def _encounters(records):
    """D-055: every dated record counts for the earliest date. Whether the earliest one is paperwork is shown beside it (see accident_date_conflicts)."""
    return [r for r in records if r.get("date_iso")]


def stated_accident_dates(records: list) -> list:
    """[{record_no, iso, quote, start, end}]: a lexicon phrase followed within 40 characters by a parsed date, per record excerpt."""
    out = []
    for r in records:
        text = r.get("excerpt") or ""
        for e in lexicon.code_list("accident_date_phrases"):
            for m in e["regex"].finditer(text):
                for d in dates.find_dates(text[m.end():m.end() + PHRASE_TO_DATE_CHARS + 12]):
                    if d["start"] > PHRASE_TO_DATE_CHARS:
                        break
                    if d["status"] == "parsed":
                        end = m.end() + d["end"]
                        out.append({"record_no": r["n"], "iso": d["iso"], "quote": text[m.start():end], "start": m.start(), "end": end})
                    break
    seen, uniq = set(), []
    for s in sorted(out, key=lambda x: (x["record_no"], x["start"], -x["end"])):
        k = (s["record_no"], s["iso"])
        if k not in seen:
            seen.add(k)
            uniq.append(s)
    return uniq


def accident_date_conflicts(records: list) -> list:
    """At most one conflict per case. (a) a stated date later than the earliest treatment date, or (b) two different stated dates."""
    stated = stated_accident_dates(records)
    enc = _encounters(records)
    if not stated or not enc:
        return []
    first = min(r["date_iso"] for r in enc)
    by_n = {r["n"]: r for r in records}
    distinct = sorted({s["iso"] for s in stated})
    later = [s for s in stated if s["iso"] > first]
    if len(distinct) < 2:
        later = [s for s in later if _event_records(s, enc)]         # T-141 r2: an earlier visit that does not describe the collision is info, not a conflict
        if later:
            first = min(r["date_iso"] for r in _event_records(later[0], enc))      # compare with the earliest record that describes it
    first_recs = [r for r in enc if r["date_iso"] == first]
    if len(distinct) < 2 and not later:
        return []
    if len(distinct) >= 2:
        a, b = stated[0], next(s for s in stated if s["iso"] != stated[0]["iso"])
        category = "accident_dates_differ"
        title, expl = flag_templates.render("conflict", category, date_a=a["iso"], date_b=b["iso"], quote_a=a["quote"], quote_b=b["quote"],
                                            provider_a=by_n[a["record_no"]].get("source"), provider_b=by_n[b["record_no"]].get("source"))
        cited = [a, b]
    else:
        a = later[0]
        category = "accident_date_after_treatment"
        # D-055 (T-116 r4/T-123): never state paperwork as the first treatment. If ANY record on the earliest date looks like paperwork (alone, or
        # sharing the date with a visit, in either order), the sentence names that record, says it looks like paperwork, and gives the other reading
        # (the first recorded visit); the paralegal decides.
        extra = {}
        paper = [r for r in first_recs if gaps.admin_label(r)]
        if paper:
            visits = sorted((r for r in enc if not gaps.admin_label(r)), key=lambda r: (r["date_iso"], r["n"]))
            extra = {"record_no": paper[0]["n"]}
            if visits:
                extra.update(alt_record_no=visits[0]["n"], alt_date=visits[0]["date_iso"], alt_provider=visits[0].get("source") or "the record",
                             alt_later="also" if a["iso"] > visits[0]["date_iso"] else "not")
        ordered = paper + [r for r in first_recs if r not in paper]
        title, expl = flag_templates.render("conflict", category, stated=a["iso"], quote=a["quote"], date=first,
                                            provider_a=ordered[0].get("source"),
                                            provider_b=ordered[1].get("source") if len(ordered) > 1 else None, **extra)
        cited = [a]
    ev = [evidence_span(by_n[s["record_no"]], "excerpt", s["quote"]) for s in cited] + [evidence_span(r, "date") for r in first_recs]
    nos = sorted({s["record_no"] for s in cited} | {r["n"] for r in first_recs})
    return [{"subtype": "accident_date", "category": category, "type": "conflict", "origin": "code", "title": title, "explanation": expl,
             "body_date": a["iso"], "stated_dates": distinct, "first_treatment_date": first, "record_nos": nos, "evidence": ev}]


def accident_date_note(records: list):
    """T-141 r2: when one stated accident date is later than some records and no conflict is raised for it, how many records predate it.
    Info for the case's `checks.notes` (computed when the case is read, from the current dates); never a flag. None when there is nothing to say."""
    enc = _encounters(records)
    distinct = sorted({s["iso"] for s in stated_accident_dates(records)})
    if len(distinct) != 1 or not enc or accident_date_conflicts(records):
        return None
    iso = distinct[0]
    before = sorted((r for r in enc if r["date_iso"] < iso), key=lambda r: r["n"])
    if not before:
        return None
    n = len(before)
    lead = f"{n} record predates" if n == 1 else f"{n} records predate"
    return {"type": "accident_date", "code": "RECORDS_PREDATE_ACCIDENT", "count": n, "record_nos": [r["n"] for r in before], "stated_date": iso,
            "text": f"{lead} the stated accident date, {dates.long_date(iso)}. None was read as describing the collision itself, so no date conflict is raised; read them to check they are earlier care."}


_TITLES = {"dr", "md", "do", "dc", "np", "pa", "pac", "dpm", "dds", "dpt", "pt", "phd", "rn", "mr", "ms", "mrs"}
_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*\.?")


def _surname(segment: str):
    """Last name-like word of a segment that carries a clinician marker (title/credential or an initial), else None."""
    words = [w.rstrip(".") for w in _WORD.findall(segment)]
    marked = any(w.lower() in _TITLES for w in words) or any(len(w) == 1 and w.isupper() for w in words)
    names = [w for w in words if w.lower() not in _TITLES and len(w) > 1 and w[0].isupper()]
    return names[-1].casefold() if marked and names else None


def _norm(s):
    return " ".join((s or "").split()).casefold()


def parse_provider(label: str) -> dict:
    """{practice, person}: practice = the first comma segment when it is not itself a clinician; person = surname from any segment."""
    segs = [s.strip() for s in (label or "").split(",") if s.strip()]
    person = next((n for n in (_surname(s) for s in segs) if n), None)
    practice = _norm(segs[0]) if segs and _surname(segs[0]) is None else None
    return {"practice": practice, "person": person}


def provider_conflicts(records: list) -> list:
    """The same clinician surname under two different practice names (case_05: Wombleton vs Crumpet Lane). Header suffixes such as
    'new patient' / 'follow-up' and case or spacing variants are not conflicts (R-TL-9)."""
    by_person = {}
    for r in records:
        p = parse_provider(r.get("source"))
        if p["person"] and p["practice"]:
            by_person.setdefault(p["person"], {}).setdefault(p["practice"], []).append(r)
    out = []
    for person, practices in sorted(by_person.items()):
        if len(practices) < 2:
            continue
        groups = sorted(practices.values(), key=lambda rs: rs[0]["n"])
        a, b = groups[0][0], groups[1][0]
        title, expl = flag_templates.render("conflict", "provider_name_variant", provider_a=a["source"], provider_b=b["source"])
        recs = sorted((r for g in groups for r in g), key=lambda r: r["n"])
        out.append({"subtype": "provider_name", "category": "provider_name_variant", "type": "conflict", "origin": "code", "title": title,
                    "explanation": expl, "record_nos": [r["n"] for r in recs], "names": [r["source"] for r in recs],
                    "evidence": [evidence_span(r, "source") for r in recs]})
    return out
