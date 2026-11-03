"""Every flag title and explanation is rendered here, by code (D-007, ADR-013, R-FL-8, LLM_VS_CODE row 16).
render(flag_type, subtype, **vars) -> (title, explanation). The subtype is an ADR-013 category or one of its golden aliases.
Only a closed set of variables is accepted, and none is free LLM prose: dates (ISO), day counts, provider labels as written,
and verbatim record quotes. A missing variable drops its clause; braces never reach the output. No template characterizes,
infers causation, computes a delay from the accident (D-017) or labels anyone non-compliant."""
from app.backend.dates import long_date

ALLOWED_VARS = {"days", "from_date", "to_date", "date", "date_a", "date_b", "stated", "provider", "provider_a", "provider_b",
                "quote", "quote_a", "quote_b", "raw", "warnings", "conditional", "record_no", "alt_record_no", "alt_date", "alt_provider", "alt_later"}

# golden-file subtypes (evals/golden) -> ADR-013 category
ALIASES = {
    ("gap", "treatment_gap"): "gap_over_30",
    ("conflict", "accident_date"): "accident_date_after_treatment",
    ("conflict", "provider_name"): "provider_name_variant",
    ("conflict", "treatment_plan"): "treatment_plan_vs_actual",
    ("conflict", "history_inconsistency"): "other_fact_mismatch",
    ("pre_existing", "prior_injury_prior_treatment"): "pre_existing",
    ("pre_existing", "prior_condition_reported"): "pre_existing",
    ("pre_existing", "prior_other_region"): "pre_existing",
    ("pre_existing", "baseline_symptom"): "pre_existing",
    ("pre_existing", "prior_surgery_same_region"): "prior_surgery",
    ("causation", "hedged_imaging"): "speculative_language",
    ("causation", "noncompliance"): "missed_care",
    ("causation", "patient_reported_onset"): "patient_report",
    ("causation", "temporal_after_gap"): "new_onset",
    ("causation", "accident_date_inconsistency"): "accident_date_provenance",
}

TYPE_OF = {
    "gap_over_30": "gap",
    "accident_date_after_treatment": "conflict", "accident_dates_differ": "conflict", "provider_name_variant": "conflict",
    "treatment_plan_vs_actual": "conflict", "other_fact_mismatch": "conflict",
    "pre_existing": "pre_existing", "degenerative_language": "pre_existing", "prior_surgery": "pre_existing",
    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
    "scene_facts": "causation", "alternative_cause": "causation", "litigation_referral": "causation",
    "objective_negative": "causation", "accident_date_provenance": "causation", "credibility_language": "causation",
    "date_ambiguous": "record_warning", "injection_suspected": "record_warning", "analysis_incomplete": "record_warning", "llm_split": "record_warning",
}


def _d(iso):
    return long_date(iso) if iso else ""


def _who(v, key="provider"):
    p = v.get(key)
    return f"{p}" if p else "the record"


def _when(v, key="date"):
    return f" ({_d(v[key])})" if v.get(key) else ""


def _quote(v, key="quote"):
    return f": “{v[key]}”" if v.get(key) else ""


def _at(v, key="provider", dkey="date"):
    return f"{_who(v, key)}{_when(v, dkey)}"


def _single(title, lead):
    """One-record flag: '<lead> in <provider> (<date>): “quote”.'"""
    return lambda v: (title, f"{lead} in {_at(v)}{_quote(v)}.")


def _pair(title):
    def f(v):
        a = f"{_at(v, 'provider_a', 'date_a')}{_quote(v, 'quote_a')}"
        b = f"{_at(v, 'provider_b', 'date_b')}{_quote(v, 'quote_b')}"
        return title, f"{a}. {b}."
    return f


def admin_endpoint_warning(side: str, record_no: int, header: str) -> str:
    """D-055: shown on a gap that starts or ends at a record whose header looks like paperwork. `header` is the record's verbatim Source label."""
    verb = "ends" if side == "end" else "starts"
    return f"This gap {verb} at record {record_no}: {header}, which looks like paperwork, not a visit. Check whether treatment continued."


def _names(recs):
    """[(record_no, header), ...] -> 'record 2: Clinic, intake form' / 'record 2: A and record 3: B' / 'record 2: A, record 3: B and record 4: C'."""
    parts = [f"record {n}: {h}" for n, h in recs]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def admin_alternative(recs: list, days, from_date, to_date) -> str:
    """D-055: the other number. `recs` = [(record_no, verbatim header)] of the paperwork-looking records the counted math treats as visits.
    days/from_date/to_date = the gap if they were paperwork; days is None when one side has no visit at all."""
    one = len(recs) == 1
    lead = f"If {_names(recs)} {'is' if one else 'are'} paperwork, not {'a visit' if one else 'visits'}, "
    if days is None:
        it = "it" if one else "them"
        if from_date is None and to_date is None:
            return lead + "there would be no visit in the records and no gap to measure."
        return lead + f"there would be no visit {'before' if from_date is None else 'after'} {it} and no gap to measure."
    return lead + f"the gap would be {days} days ({_d(from_date)} to {_d(to_date)})."


def admin_split_warning(recs: list, pieces: list) -> str:
    """D-055: shown on the conditional flag for a span over 30 days that paperwork-looking records split into short counted pieces.
    `recs` = [(record_no, verbatim header, iso date)]; `pieces` = the counted day counts."""
    one = len(recs) == 1
    parts = [f"record {n}: {h} ({_d(d)})" for n, h, d in recs]
    where = parts[0] if one else ", ".join(parts[:-1]) + " and " + parts[-1]
    return (f"No gap is counted here because {where} {'falls' if one else 'fall'} inside this span and {'is' if one else 'are'} counted as "
            f"{'a visit' if one else 'visits'} ({', then '.join(f'{p} days' for p in pieces)}).")


def _gap(v):
    days = v.get("days")
    a = f"{_d(v.get('from_date'))}" + (f" ({v['provider_a']})" if v.get("provider_a") else "")
    b = f"{_d(v.get('to_date'))}" + (f" ({v['provider_b']})" if v.get("provider_b") else "")
    more = "".join(" " + w for w in v.get("warnings") or [])
    if v.get("conditional"):
        return f"Possible gap of {days} days", f"Possible gap of {days} days between {a} and {b}.{more}"
    return f"Gap of {days} days", f"Gap of {days} days between {a} and {b}.{more}"


def _acc_after_paperwork(v):
    """D-055 (T-116 round 4): the earliest recorded date belongs to a record that looks like paperwork. The sentence never calls it treatment; it names the
    record and gives the other reading (the first recorded visit) so the paralegal decides."""
    prov = "; ".join(p for p in (v.get("provider_a"), v.get("provider_b")) if p)
    stated = f" {_d(v['stated'])}" if v.get("stated") else ""
    quote = f" (“{v['quote']}”)" if v.get("quote") else ""
    first = f"{_d(v.get('date'))} (record {v['record_no']}: {v['provider_a']})" if v.get("provider_a") else f"{_d(v.get('date'))} (record {v['record_no']})"
    if v.get("alt_date"):
        alt = (f"If record {v['record_no']}: {v.get('provider_a') or 'this record'} is paperwork, not a visit, the first recorded visit is {_d(v['alt_date'])} "
               f"(record {v['alt_record_no']}: {v['alt_provider']}), and the stated date is {v['alt_later']} later than it.")
    else:
        alt = f"If record {v['record_no']}: {v.get('provider_a') or 'this record'} is paperwork, not a visit, there is no recorded visit to compare with."
    return ("Stated accident date is later than the earliest record",
            f"Stated accident date{stated}{quote} is later than the earliest recorded date, {first}, which looks like paperwork, not a visit. "
            f"The records disagree; the tool does not choose between them. {alt} Check when treatment actually began before relying on this comparison.")


def _acc_after(v):
    if v.get("record_no"):
        return _acc_after_paperwork(v)
    prov = "; ".join(p for p in (v.get("provider_a"), v.get("provider_b")) if p)
    first = (f", {_d(v['date'])}" + (f" ({prov})" if prov else "")) if v.get("date") else ""
    stated = f" {_d(v['stated'])}" if v.get("stated") else ""
    quote = f" (“{v['quote']}”)" if v.get("quote") else ""
    return ("Stated accident date is later than recorded treatment",
            f"Stated accident date{stated}{quote} is later than the first recorded treatment{first}. "
            "The records disagree; the tool does not choose between them." + "".join(" " + w for w in v.get("warnings") or []))


def _acc_differ(v):
    a = f"{_who(v, 'provider_a')} states {_d(v.get('date_a')) or 'a date'}" + (f" (“{v['quote_a']}”)" if v.get("quote_a") else "")
    b = f"{_who(v, 'provider_b')} states {_d(v.get('date_b')) or 'a date'}" + (f" (“{v['quote_b']}”)" if v.get("quote_b") else "")
    return "Two different stated accident dates", f"{a}; {b}. The tool does not choose between them."


def _provider_variant(v):
    a = f"{_who(v, 'provider_a')}" + (f" (“{v['quote_a']}”)" if v.get("quote_a") else "")
    b = f"{_who(v, 'provider_b')}" + (f" (“{v['quote_b']}”)" if v.get("quote_b") else "")
    return "Provider name differs between records", f"{a} and {b} may name the same provider."


def _date_amb(v):
    raw = f"The date “{v['raw']}” in " if v.get("raw") else "A date in "
    return "Date to confirm", f"{raw}{_who(v)} can be read more than one way; choose one reading."


def _inj(v):
    return ("Instruction-like text in a record",
            f"{_at(v)} contains instruction-like text{_quote(v)}. It is shown unchanged and everything from this record needs review.")


TEMPLATES = {
    "gap_over_30": _gap,
    "accident_date_after_treatment": _acc_after,
    "accident_dates_differ": _acc_differ,
    "provider_name_variant": _provider_variant,
    "treatment_plan_vs_actual": _pair("Treatment plan and what followed differ"),
    "other_fact_mismatch": _pair("Records differ on a fact"),
    "pre_existing": lambda v: ("Mention of a prior or pre-existing condition", f"{_at(v)} mentions a prior or pre-existing condition{_quote(v)}."),
    "degenerative_language": lambda v: ("Degenerative wording", f"{_at(v)} uses degenerative wording{_quote(v)}."),
    "prior_surgery": lambda v: ("Mention of prior surgery or repair", f"{_at(v)} mentions prior surgery or repair{_quote(v)}."),
    "speculative_language": lambda v: ("Hedged wording", f"Hedged wording in {_at(v)}{_quote(v)}."),
    "patient_report": lambda v: ("Reported onset", f"Onset wording reported in {_at(v)}{_quote(v)}."),
    "missed_care": lambda v: ("Missed or ended care", f"Wording about missed appointments or ending care in {_at(v)}{_quote(v)}."),
    "new_onset": lambda v: ("New-onset wording", f"New-onset wording in {_at(v)}{_quote(v)}."),
    "scene_facts": lambda v: ("Scene facts", f"Scene facts recorded by {_at(v)}{_quote(v)}."),
    "alternative_cause": lambda v: ("Mention of another injury or event", f"Mention of another injury or event in {_at(v)}{_quote(v)}."),
    "litigation_referral": lambda v: ("Attorney referral", f"Referral wording in {_at(v)}{_quote(v)}."),
    "objective_negative": lambda v: ("Normal or absent findings wording", f"Wording about normal or absent findings in {_at(v)}{_quote(v)}."),
    "credibility_language": lambda v: ("Credibility-related wording", f"Wording in {_at(v)} that uses a credibility term{_quote(v)}."),
    "accident_date_provenance": lambda v: ("Accident date source", f"Accident date as stated in {_at(v)}{_quote(v)}."),
    "date_ambiguous": _date_amb,
    "injection_suspected": _inj,
    "llm_split": lambda v: ("Record boundaries chosen by the AI", "This record was separated from the pasted text by the AI because the paste had no recognisable record markers. Check where it begins and ends."),
    "analysis_incomplete": lambda v: ("Cross-record check did not finish",
                                      "The check for conflicts between records did not finish, so conflicts between records may be missing from this list. Review the records side by side."),
}


# D-069: the (title, explanation) of a flag whose text would name the AI, for a flag whose first answer is a prepared one. Keyed by category; read-side views use it instead of the stored text.
PREPARED_TEXT = {"llm_split": ("Record boundaries chosen by a prepared answer",
                               "This record was separated from the pasted text by a prepared answer because the paste had no recognisable record markers. Check where it begins and ends.")}


UNRECOGNISED = ("Unrecognised flag category", "The model proposed a category that is not on the closed list.")
UNRECOGNISED_PREPARED = ("Unrecognised flag category", "A prepared answer proposed a category that is not on the closed list.")


def category_of(flag_type: str, subtype: str) -> str:
    """Resolve (type, subtype) to an ADR-013 category; KeyError if neither the category nor a golden alias (closed list)."""
    key = ALIASES.get((flag_type, subtype), subtype)
    if key not in TEMPLATES or TYPE_OF[key] != flag_type:
        raise KeyError(f"no flag template for {flag_type}/{subtype}")
    return key


def render(flag_type: str, subtype: str, **vars) -> tuple:
    extra = set(vars) - ALLOWED_VARS
    if extra:
        raise KeyError(f"unknown template variable(s): {sorted(extra)}")
    v = {k: x for k, x in vars.items() if x not in (None, "")}
    title, expl = TEMPLATES[category_of(flag_type, subtype)](v)
    return title, expl.replace(".”.", ".”")      # a quote that already ends in a period needs no second one


# D-057 (T-126): a model proposal that a code rule filters out is listed in a collapsed, counted "Filtered by rule" group, never dropped (D-053).
# category -> (decision, rule name shown, what the rule says). The group is derived from the flag's category; nothing extra is stored.
FILTER_RULES = {"objective_negative": ("D-032", "Normal or negative findings",
                                       "A normal or negative finding is context, not a flag, so the rule filtered it out. Nothing is needed from you.")}
FILTERED = "FILTERED_BY_RULE"


def is_filtered(reasons) -> bool:
    """T-126 r2: THE test for a rule-filtered proposal (its reason code comes first). Every reader uses this, never the literal."""
    return list(reasons or [])[:1] == [FILTERED]
