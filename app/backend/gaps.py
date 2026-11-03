"""Treatment gaps, computed by code over code-parsed header dates (ADR-010, D-003, R-FL-1, row 9, D-055).
Entry state, review status and LLM output have no influence. Strictly more than 30 calendar days flags (30 is not a gap, 31 is).
Ambiguous or missing dates are never endpoints.
D-055 (T-116 rounds 3 and 4): the gap math NEVER guesses a record out. EVERY dated record is an endpoint, whatever ingest called it (the ingest
`kind` is a label guess and is not read here). When a paperwork-looking record (intake form, records request, bill or ledger, affidavit, records
review...) starts, ends or splits a gap, the gap carries a visible warning with BOTH numbers: the gap as counted, and the gap if that record is
paperwork, not a visit. A span over 30 days that such a record splits into pieces of 30 days or fewer shows as a conditional flag. The paralegal
decides. A warning cannot invent or hide a gap; an exclusion did, in two review rounds."""
import re

from app.backend import dates, flag_templates, ingest
from app.backend.ingest import evidence_span

THRESHOLD_DAYS = 30

# (label shown to the paralegal, header-label regex), first match wins. A bare "intake" (an intake evaluation or visit) is a treatment
# encounter and is deliberately NOT here; only the paperwork wording is ("intake form", "formulario de admision").
_NON_VISIT = [(label, re.compile(rx, re.IGNORECASE)) for label, rx in (
    ("intake form", r"\b(?:(?:new[- ]patient\s+)?(?:intake|registration|admission|admissions|check-?in)\s+(?:form|forms|packet|paperwork|questionnaire|sheet)"
                    r"|new[- ]patient\s+(?:paperwork|forms?|questionnaire|packet)|patient\s+(?:information|history|health\s+history|registration)\s+(?:form|questionnaire|sheet)"
                    r"|health\s+history\s+(?:form|questionnaire)|pain\s+(?:diagram|questionnaire)|consent\s+form|assignment\s+of\s+benefits|questionnaires?)\b"
                    r"|\bformulario\s+de\s+(?:admisi[oó]n|ingreso|registro)\b|\bhoja\s+de\s+(?:admisi[oó]n|ingreso)\b"),
    ("explanation of benefits", r"\b(?:explanation\s+of\s+benefits|EOB|remittance(?:\s+advice)?)\b"),
    ("claim form", r"\b(?:UB-?04|CMS-?1500|HCFA|claim\s+form)\b"),
    ("ledger", r"\b(?:ledger|payment\s+(?:history|record)|account\s+history)\b"),
    ("billing statement", r"\b(?:billing|statement\s+of\s+account|account\s+statement|itemi[sz]ed\s+(?:bill|statement|charges)|invoice|superbill|balance\s+due)\b|^statement$"
                          r"|\bestado\s+de\s+cuenta\b|\bfactura\b"),
    ("affidavit", r"\b(?:affidavit|custodian\s+of\s+records|records\s+custodian|certification\s+of\s+records|business\s+records|cover\s+(?:page|sheet))\b"),
    ("records request", r"\b(?:records?\s+request|request\s+for\s+records|records\s+retrieval|authorization\s+(?:form|request)|HIPAA\s+authorization)\b"),
    ("records review", r"\b(?:records?|chart|peer|utili[sz]ation)\s+review\b|\bIME\b|\bindependent\s+medical\s+(?:exam|examination|evaluation)\b"),
    ("narrative letter", r"\bnarrative\s+(?:letter|report)\b|\bmedical[- ]legal\s+(?:report|narrative)\b|\bsummary\s+letter\b|\bdemand\s+letter\b"),
    ("letter or correspondence", r"^fax$|\b(?:correspondence|letter(?:\s+of\s+protection)?|LOP|fax\s+cover(?:\s+sheet)?|referral\s+(?:form|letter)|prior\s+authori[sz]ation)\b"),
    ("phone or message note", r"\b(?:phone|telephone|tel\.?)\s+(?:note|call|encounter|message|contact)\b|\bportal\s+message\b|\bvoicemail\b|\bmessage\s+(?:note|log)\b"),
)]
# A document that names itself on its first line (an intake form whose Source label only says "new patient"). Anchored: a clinical note that
# merely mentions a form further in does not match.
_TITLE = re.compile(r"^\W*(?:new[- ]patient\s+)?(?:intake|registration|admission)\s+(?:form|packet|questionnaire)\b|^\W*(?:business\s+records\s+)?affidavit\b", re.IGNORECASE)


# Words that name a treatment visit in the record-type head. If one is left in the head after the administrative phrase is removed, the
# record is treated as a visit ("records review visit", "initial evaluation", "progress note"). English and Spanish.
_VISIT_WORD = re.compile(r"\b(?:visits?|evaluations?|evals?|exams?|examinations?|consult\w*|follow-?ups?|progress|sessions?|treatments?|therapy|"
                         r"procedures?|injections?|operative|surgery|imaging|mri|x-?rays?|notes?|soap|daily|new\s+patient|initial|discharge|esi|epidural|"
                         r"visita|consulta|nota|sesi[oó]n|evaluaci[oó]n|terapia|tratamiento|cita)\b", re.IGNORECASE)


def _bare(src: str) -> str:
    """The header label with every parenthetical dropped ("(OCR)", "(faxed)", "(intake form completed same day)")."""
    h = (src or "").strip()
    while True:
        n = re.sub(r"\s*\([^()]*\)", "", h)
        if n == h:
            return h.strip()
        h = n


def admin_label(rec: dict):
    """The plain label of a record whose header looks administrative ("intake form", "billing statement", ...), or None. WARNING ONLY (D-055):
    it never changes a gap. It stays conservative so a warning means something: (1) the administrative type is read from the record-type head
    (last comma segment) of the header label, or from the record's own first-line title; (2) no visit word appears in the label outside parentheses and
    outside the provider name (first segment) once that phrase is removed ("records review visit", "Capital PT, daily note, fax" are visits); (3) the record's text is never consulted
    for treatment words (T-116 r5): a bill, EOB, request or form routinely lists diagnoses and services performed, and a warning costs a click while a hidden span
    costs the case. Fail toward warning."""
    bare = _bare(rec.get("source"))
    head = bare.rsplit(",", 1)[-1].strip()
    label, rest = None, ""
    for lab, rx in _NON_VISIT:
        m = rx.search(head)
        if m:
            label, rest = lab, head[:m.start()] + " " + head[m.end():]
            mid = bare[:len(bare) - len(head)].split(",", 1)[1] if "," in bare else ""      # segments after the provider name
            rest = mid + " " + rest
            break
    if not label:
        first = (rec.get("excerpt") or "").lstrip().split("\n", 1)[0][:120]
        if first and _TITLE.search(first):
            label, rest = ("affidavit" if "affidavit" in first.lower() else "intake form"), re.sub(r"new[- ]patient", "", bare.split(",", 1)[-1], flags=re.IGNORECASE)
    if not label:
        k = ingest.record_kind(bare)           # the ingest lexicon, on the label without parentheticals: same families, still a warning only (D-055)
        if k not in ("encounter", "unsplit_text"):
            label = {"billing_statement": "billing statement", "phone_note": "phone or message note"}.get(k, "administrative record")
            rest = bare.split(",", 1)[1] if "," in bare else ""
    if not label or _VISIT_WORD.search(rest):
        return None
    return label


def is_gap(days: int) -> bool:
    return days > THRESHOLD_DAYS


def compute_gaps(records: list) -> list:
    """[{from_date, to_date, from_records, to_records, days, flag}] between consecutive DISTINCT dates of ALL dated records (D-055)."""
    by_date = {}
    for r in records:
        if r.get("date_iso"):
            by_date.setdefault(r["date_iso"], []).append(r["n"])
    ds = sorted(by_date)
    out = []
    for a, b in zip(ds, ds[1:]):
        n = dates.days_between(a, b)
        out.append({"from_date": a, "to_date": b, "from_records": sorted(by_date[a]), "to_records": sorted(by_date[b]),
                    "days": n, "flag": is_gap(n)})
    return out


def _reasons(gap: dict, records: list) -> list:
    """needs_review reasons: an undated/ambiguous record whose date could fall inside the span (ADR-010), or an injection-tagged endpoint."""
    reasons = []
    for r in records:
        if r.get("kind") == "unsplit_text" or r.get("date_iso"):
            continue
        cands = r.get("date_candidates") or []
        if not cands or any(gap["from_date"] <= c <= gap["to_date"] for c in cands):
            reasons.append("ENDPOINT_NOT_VERIFIED")
            break
    ends = set(gap["from_records"]) | set(gap["to_records"])
    if any(r.get("injection_tag") for r in records if r["n"] in ends):
        reasons.append("INJECTION_SUSPECTED")
    return reasons


def _visit_dates(records: list) -> list:
    """Sorted dates on which at least one dated record does NOT look like paperwork: the dates the alternative reading counts."""
    return sorted({r["date_iso"] for r in records if r.get("date_iso") and not admin_label(r)})


def _alternative(records: list, from_date: str, to_date: str) -> dict:
    """The gap that would exist if every paperwork-looking record around [from_date, to_date] were not a visit: from the nearest visit date at or
    before from_date to the nearest visit date at or after to_date. `dropped` = the paperwork-looking records strictly inside that span, in
    date order. days/from/to are None when one side has no visit at all."""
    vd = _visit_dates(records)
    lo = max((d for d in vd if d <= from_date), default=None)
    hi = min((d for d in vd if d >= to_date), default=None)
    dropped = sorted((r for r in records if r.get("date_iso") and admin_label(r) and (lo is None or r["date_iso"] > lo) and (hi is None or r["date_iso"] < hi)),
                     key=lambda r: (r["date_iso"], r["n"]))
    days = dates.days_between(lo, hi) if lo and hi else None
    return {"from": lo, "to": hi, "days": days, "dropped": dropped,
            "sentence": flag_templates.admin_alternative([(r["n"], r.get("source") or admin_label(r)) for r in dropped], days, lo, hi)}


def endpoint_warnings(gap: dict, records: list, a: int = None, b: int = None) -> list:
    """D-055: one warning per side of the gap whose endpoint records ALL look administrative (a visit on the same date anchors the side, so
    no warning). `a` and `b` are the records the flag cites for the start and the end. Each carries the alternative reading (the gap if the
    paperwork-looking records were not visits). Warnings only; the gap itself is not touched."""
    by_n = {r["n"]: r for r in records}
    a = a if a is not None else gap["from_records"][-1]
    b = b if b is not None else gap["to_records"][0]
    out = []
    for side, nos, cited, date in (("start", gap["from_records"], a, gap["from_date"]), ("end", gap["to_records"], b, gap["to_date"])):
        labs = [admin_label(by_n[n]) for n in nos if n in by_n]
        if labs and all(labs):
            r = by_n[cited]
            alt = _alternative(records, gap["from_date"], gap["to_date"])
            out.append({"side": side, "record_no": cited, "record_type": admin_label(r) or labs[0], "date": date,
                        "warning": flag_templates.admin_endpoint_warning(side, cited, r.get("source") or admin_label(r) or labs[0]),
                        "alternative": alt["sentence"], "alternative_days": alt["days"], "alternative_from": alt["from"], "alternative_to": alt["to"]})
    return out


def _strict_gaps(records: list) -> list:
    """Gaps over 30 days between consecutive VISIT dates (paperwork-looking records left out). Used only to find spans the counted math splits."""
    vd = _visit_dates(records)
    return [(x, y) for x, y in zip(vd, vd[1:]) if is_gap(dates.days_between(x, y))]


def _conditional_flags(records: list, counted: list) -> list:
    """A span over 30 days between two visit dates that paperwork-looking records split into counted pieces of 30 days or fewer: no counted gap
    exists, so show a flag that says so and gives both numbers (D-055). Skipped when a counted flagged gap already carries that alternative."""
    by_n = {r["n"]: r for r in records}
    shown = {(w["alternative_from"], w["alternative_to"]) for f in counted for w in f["endpoint_warnings"]}
    shown |= {(f["from_date"], f["to_date"]) for f in counted}
    out = []
    for lo, hi in _strict_gaps(records):
        if (lo, hi) in shown:
            continue
        inside = sorted((r for r in records if r.get("date_iso") and lo < r["date_iso"] < hi), key=lambda r: (r["date_iso"], r["n"]))
        if not inside:
            continue
        a = max(r["n"] for r in records if r.get("date_iso") == lo and not admin_label(r))
        b = min(r["n"] for r in records if r.get("date_iso") == hi and not admin_label(r))
        cuts = sorted({lo, hi} | {r["date_iso"] for r in inside})
        pieces = [dates.days_between(x, y) for x, y in zip(cuts, cuts[1:])]
        alt = _alternative(records, lo, hi)
        days = dates.days_between(lo, hi)
        split = flag_templates.admin_split_warning([(r["n"], r.get("source") or admin_label(r), r["date_iso"]) for r in inside], pieces)
        title, expl = flag_templates.render("gap", "gap_over_30", days=days, from_date=lo, to_date=hi, provider_a=by_n[a].get("source"),
                                            provider_b=by_n[b].get("source"), conditional=True, warnings=[split, alt["sentence"]])
        ev = [evidence_span(by_n[n], f) for n in (a, b) for f in ("date", "source")]
        w = [{"side": "inside", "record_no": r["n"], "record_type": admin_label(r), "date": r["date_iso"], "warning": split,
              "alternative": alt["sentence"], "alternative_days": alt["days"], "alternative_from": alt["from"], "alternative_to": alt["to"]} for r in inside]
        out.append({"id": f"f_gap_r{a}_r{b}", "type": "gap", "category": "gap_over_30", "origin": "code", "title": title, "explanation": expl,
                    "from_date": lo, "to_date": hi, "days": days, "conditional": True,
                    "record_nos": sorted({a, b} | {r["n"] for r in inside}), "evidence": ev,
                    "reasons": _reasons({"from_date": lo, "to_date": hi, "from_records": [a], "to_records": [b]}, records), "endpoint_warnings": w})
    return out


def gap_flags(records: list) -> list:
    """One flag per gap over 30 days, id keyed by the bounding record pair; text from flag_templates only."""
    by_n = {r["n"]: r for r in records}
    flags = []
    for g in compute_gaps(records):
        if not g["flag"]:
            continue
        a, b = g["from_records"][-1], g["to_records"][0]
        warns = endpoint_warnings(g, records, a, b)
        title, expl = flag_templates.render("gap", "gap_over_30", days=g["days"], from_date=g["from_date"], to_date=g["to_date"],
                                            provider_a=by_n[a].get("source"), provider_b=by_n[b].get("source"),
                                            warnings=[x["warning"] for x in warns] + ([warns[0]["alternative"]] if warns else []))
        ev = [evidence_span(by_n[n], f) for n in (a, b) for f in ("date", "source")]
        flags.append({"id": f"f_gap_r{a}_r{b}", "type": "gap", "category": "gap_over_30", "origin": "code", "title": title,
                      "explanation": expl, "from_date": g["from_date"], "to_date": g["to_date"], "days": g["days"],
                      "record_nos": sorted(set(g["from_records"]) | set(g["to_records"])), "evidence": ev, "reasons": _reasons(g, records),
                      "endpoint_warnings": warns})
    flags += _conditional_flags(records, flags)
    return sorted(flags, key=lambda f: (f["from_date"], f["to_date"], f["id"]))


def merge_flags(old: list, new: list) -> list:
    """Recompute after confirm_date: a flag whose record pair, dates and days are unchanged keeps its review status and note;
    a changed or new flag starts pending (ADR-002). Flags that no longer exist are dropped."""
    prev = {f["id"]: f for f in old}
    out = []
    for f in new:
        o = prev.get(f["id"])
        same = o and all(o.get(k) == f.get(k) for k in ("from_date", "to_date", "days"))
        out.append({**f, "review_status": o.get("review_status", "pending") if same else "pending", "note": o.get("note") if same else None})
    return out
