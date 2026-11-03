"""Cross-record conflict CANDIDATES, proposed by code (T-094, R-CO-7; LLM_VS_CODE row 11). Deterministic: no model, no app.llm import.
The model no longer searches the records for conflicts (open generation varied run to run). Code finds the pairs worth asking about, in a
fixed order, and a judge (J3, judge_conflict_v6) only classifies each pair: conflict or benign.

Rules:
- plan_vs_outcome: a stated plan of care (a visit count, or frequency x duration which code multiplies out) and a LATER record that shows the
  course ending early (missed appointments, no-show, discontinued). Arithmetic is code's: "2x/week for 6 weeks" is 12 visits, so it agrees
  with "Plan of care: 12 visits" and is never a conflict. Plans that agree make one plan (the explicit visit count is quoted).
- history_denial: a sentence that denies prior problems ("denies prior neck problems", "no previous accidents") and a sentence in ANOTHER record that
  the phrase list fires on as a prior condition or surgery, or that names an earlier accident or claim.
- Structured patterns, not free text: plan = visit count (digits or number words) in a sentence with a plan cue, or frequency x duration in weeks;
  early end = non-attendance, loss to follow-up, or an explicit stop, unless negated in the same sentence ("no missed appointments").
- Whose sentence it is (T-113): a sentence whose subject is another person (the other driver, a relative, a witness, "family history") is never half of a
  candidate; the judge would only be asked to say that one person's history is not another's. The subject is read inside the sentence's own semicolon clause
  (the splitter cuts at ';'). A paperwork record (intake form, bill, affidavit; gaps' header test) is not a clinical encounter and is never the plan or the
  outcome of a course (T-116 F3); a denial on an intake form is still the patient's own statement and is compared.
  Not covered (memory/SCOPE_CUTS.md): dosage, laterality, date and provider conflicts beyond the code rules, durations in months. One candidate per denial is judged at a time, in record order, and the first the judge confirms stands.
- A form field answered No counts as a denial (T-141): "Prior accidents? Yes [ ] No [X]." (OCR "No IX]") or "Prior injuries: None." Yes checked, no box
  checked or a question alone does not. An accident named by a year earlier than the denial record's year ("car accidents in 2019 and 2022") is a prior event.
Every quote is a whole sentence taken from the record text, so it is verbatim by construction."""
import re
from dataclasses import dataclass

from app.backend import gaps, lexicon_scan, sentences

_WORDS = {"one": 1, "once": 1, "two": 2, "twice": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
          "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "eighteen": 18, "twenty": 20, "twenty-four": 24}
_NW = "|".join(sorted(_WORDS, key=len, reverse=True))
_NUM = rf"(\d{{1,3}}|{_NW})"
# plan, count form: "<N> visits/sessions/treatments" in a sentence that carries a PLAN CUE (planned, authorized, recommended, "PT x 12", ...) and no completion
# word. "Completed 12 visits" is not a plan. Digits or number words ("Twelve visits authorized").
_VISITS = re.compile(rf"\b{_NUM}\s*(?:more\s+)?(?:visits?|sessions?|treatments?)\b", re.I)
_PLAN_CUE = re.compile(r"\b(?:plan(?:ned)?(?:\s+of\s+care)?|authori[sz]\w*|approv\w*|order\w*|certif\w*|recommend\w*|request\w*|prescrib\w*|referr?\w*|total|PT\s*x|therapy\s*x)\b", re.I)
_DONE = re.compile(r"\b(?:completed|attended|finished|received|had)\b", re.I)
# plan, frequency x duration: "2x/week for 6 weeks", "twice-weekly for six weeks", "three times per week x 4 wks". Code multiplies.
_FREQ = re.compile(rf"\b{_NUM}(?:\s*x|\s+times?)?\s*(?:[/-]|\s+per\s+|\s+a\s+|\s+each\s+)?\s*(?:week|wk|weekly)\w*\s*(?:for|x|over)\s*{_NUM}\s*(?:weeks?|wks?)\b", re.I)
# the course ended early: non-attendance, loss to follow-up, an explicit stop. "missing 3 days of work" and a plain "discharged home" do not match.
_CARE = r"(?:PT|physical\s+therapy|therapy|treatment|care|chiropractic|rehab\w*|visits?|appointments?|sessions?)"
_ENDED = re.compile(r"\b(?:missed\s+(?:\w+\s+){0,2}(?:appointments?|visits?|sessions?)|no[- ]?shows?|cancel(?:l)?ed\s+(?:\w+\s+){0,2}(?:appointments?|visits?|sessions?)"
                    r"|did\s+not\s+(?:attend|return)|failed\s+to\s+(?:attend|return)|stopped\s+(?:attending|going|coming)|no\s+longer\s+(?:attend\w*|coming|going)"
                    r"|lost\s+to\s+follow[- ]?up|self[- ]discharged|discontinued|non-?complian\w*"
                    rf"|(?:left|quit|ceased|stopped|withdrew\s+from|dropped\s+out\s+of)\s+(?:the\s+)?(?:\w+\s+)?{_CARE})\b", re.I)
_NEGATED_BEFORE = re.compile(r"\b(?:no|without|zero|never)\s+(?:\w+\s+)?$", re.I)      # "no missed appointments", "never missed a visit": a completed course, not an early end
_DENIAL = re.compile(r"\b(?:denies|denied|denying)\s+(?:any\s+)?(?:prior|previous|pre-?existing|earlier)\b|\bno\s+(?:prior|previous|pre-?existing)\s+(?:\w+\s+){0,3}"
                     r"(?:problems?|injur\w+|history|symptoms?|complaints?|pain|treatment|accidents?|collisions?|crash\w*|wrecks?|surger\w+|trauma|claims?)\b|\bno\s+history\s+of\b", re.I)
# T-141 (GATE-M2 lib11): a form field answered No is a denial too. The splitter cuts "Prior accidents? Yes [ ] No [X]." after the question mark, so a stem
# unit ("Prior accidents?" / "Previous injuries:") and the unit after it are read together. The answer is No only when the No box is checked and the Yes
# box is not ("No [X]", OCR "No IX]"), or the answer is a bare No / None. Yes checked, both boxes empty or a stem alone is never a denial.
_FORM_STEM = re.compile(r"^(?:any\s+)?(?:prior|previous|pre-?existing|earlier)\s+[A-Za-z][A-Za-z /-]{2,40}?\s*[?:]$", re.I)
_BOX = r"[\[(]?\s*(?:[Il1]\s*)?[xX\u2713\u2714]\s*[\])]"
_EMPTY_BOX = r"[\[(]\s*[\])]"
_FORM_NO = re.compile(rf"^(?:(?:yes\s*{_EMPTY_BOX}\s*)?no\s*{_BOX}(?:\s*yes\s*{_EMPTY_BOX})?|(?:no|none|negative)\b)\W*$", re.I)
_FORM_ONE = re.compile(r"^((?:any\s+)?(?:prior|previous|pre-?existing|earlier)\s+[A-Za-z][A-Za-z /-]{2,40}?)\s*[?:]\s*(?:no|none|negative)\W*$", re.I)
# an earlier accident named only by a year before the denial's year ("car accidents in 2019 and 2022"), not covered by _PRIOR_EVENT's 'prior' wording
_ACCIDENT_IN_YEAR = re.compile(r"\b(?:accidents?|collisions?|MVA|MVC|crash\w*|wrecks?)\b[^.;]{0,40}?\b(?:in|of|during)\s+((?:19|20)\d\d)\b", re.I)
_YEARS = re.compile(r"\b((?:19|20)\d\d)\b")
# a prior event the phrase list does not cover (an earlier accident or claim). A sentence that is itself a denial never counts.
_PRIOR_EVENT = re.compile(r"\b(?:prior|previous|earlier)\s+(?:\w+\s+){0,2}(?:accidents?|collisions?|MVA|MVC|crash\w*|wrecks?|injur\w+|claims?)\b", re.I)
_PRIOR_CATEGORIES = ("pre_existing", "prior_surgery")
# Whose sentence it is (T-113). A short closed list: a relative or another party as the SUBJECT at the start of the clause ("Her mother had ...",
# "The other driver reported ...", "Family history: ..."). If the clause then names the patient ("Mother reports patient had ..."), it is the patient's
# history reported by someone else and stays. A person this list does not name still reaches the judge, whose rule 2b is the backstop.
_RELATIVE = (r"(?:mother|father|mom|dad|parents?|sister|brother|sibling|husband|wife|spouse|son|daughter|child|children|grand(?:mother|father|parent)s?|"
             r"aunt|uncle|cousin|niece|nephew|partner|boyfriend|girlfriend|fianc\w+|in-laws?|step(?:mother|father|son|daughter))")
_PARTY = r"(?:(?:other|third|adverse)\s+(?:driver|party|motorist|person|vehicle\s+(?:driver|occupant)s?)|at-fault\s+driver|witness(?:es)?|bystanders?)"
_OTHER_SUBJECT = re.compile(rf"^\W*(?:family\s+history\b|(?:(?:the|her|his|their|patient'?s|pt'?s|client'?s|claimant'?s)\s+)*(?:{_RELATIVE}|{_PARTY})\b)", re.I)
# ('pt' is physical therapy as often as patient, so it is not read as the patient)
_PATIENT_WORD = re.compile(r"\b(?:patient|claimant|plaintiff|client)\b", re.I)


@dataclass(frozen=True)
class Quote:
    record_no: int
    text: str


def _num(s):
    return int(s) if s.isdigit() else _WORDS[s.lower()]


def _units(record):
    text = record.get("excerpt") or ""
    return [text[a:b].strip() for a, b in sentences.stripped_spans(text) if text[a:b].strip()]


def _denial_units(record) -> list:
    """Sentences of the record that deny prior problems: the T-094 phrases plus a form field answered No (T-141). A form denial is the stem unit and
    the answer unit joined as they stand in the record, so the quote is one contiguous piece of the text."""
    text = record.get("excerpt") or ""
    spans = [(a, b) for a, b in sentences.stripped_spans(text) if text[a:b].strip()]
    out = []
    for i, (a, b) in enumerate(spans):
        u = text[a:b].strip()
        if _DENIAL.search(u):
            out.append(u)
        elif _FORM_ONE.match(u):
            out.append(u)
        elif _FORM_STEM.match(u) and i + 1 < len(spans) and _FORM_NO.match(text[spans[i + 1][0]:spans[i + 1][1]].strip()):
            out.append(text[a:spans[i + 1][1]].strip())
    return out


_ACCIDENT_STEM = re.compile(r"^(?:any\s+)?(?:prior|previous|earlier)\s+(?:\w+\s+)?(?:accidents?|collisions?|crash\w*|wrecks?|MVA|MVC|claims?)\b", re.I)


def _earlier_year_accident(unit: str, denial_rec: dict) -> bool:
    """The sentence names an accident in a year earlier than the denial record's own year. Without a date for the denial it cannot be said, so no."""
    year = (denial_rec.get("date_iso") or "")[:4]
    if not year.isdigit() or _DENIAL.search(unit) or _FORM_STEM.match(unit):
        return False
    return any(int(m.group(1)) < int(year) for m in _ACCIDENT_IN_YEAR.finditer(unit))


def _other_person(unit: str) -> bool:
    """The clause is about someone other than the patient: another party or a relative is its subject, and the clause does not name the patient."""
    m = _OTHER_SUBJECT.match(unit)
    return bool(m) and not _PATIENT_WORD.search(unit[m.end():])


def _paperwork(rec: dict) -> bool:
    """T-116 F3: an intake form, bill or affidavit is not a clinical encounter. The header test is gaps' (conservative: a record with treatment evidence is a visit)."""
    return bool(gaps.admin_label(rec))


def _after(a, b) -> bool:
    """Record b is later than record a: by parsed date when both have one, else by record number."""
    da, db = a.get("date_iso"), b.get("date_iso")
    if da and db:
        return db > da or (db == da and b["n"] > a["n"])
    return b["n"] > a["n"]


def plans(records: list) -> list:
    """Every stated plan: {record_no, quote, visits, kind: 'count'|'freq', arithmetic}. Frequency x duration is multiplied by code."""
    out = []
    for r in records:
        if _paperwork(r):
            continue
        for u in _units(r):
            if _other_person(u):
                continue
            m = _VISITS.search(u)
            if m and _PLAN_CUE.search(u) and not _DONE.search(u):
                n = _num(m.group(1))
                out.append({"record_no": r["n"], "quote": u, "visits": n, "kind": "count", "arithmetic": f"{n} visits"})
                continue
            f = _FREQ.search(u)
            if f:
                per, weeks = _num(f.group(1)), _num(f.group(2))
                out.append({"record_no": r["n"], "quote": u, "visits": per * weeks, "kind": "freq", "arithmetic": f"{per} per week x {weeks} weeks = {per * weeks} visits"})
    return out


_COMPLETED = re.compile(r"\bgoals?\s+(?:met|achieved)\b|\b(?:completed|resolved)\b", re.I)       # "stopped PT, goals met" is a finished course


def _early_end(unit: str) -> bool:
    """The unit shows the course ending early. A match preceded by no/without/zero/never in the same unit ("no missed appointments") does not count,
    and neither does a unit that says the course was completed or its goals met."""
    return not _COMPLETED.search(unit) and any(not _NEGATED_BEFORE.search(unit[:m.start()]) for m in _ENDED.finditer(unit))


def _canonical_plan(ps: list, outcome_rec: dict, by_n: dict):
    """The plan an outcome is compared with: among plans in earlier records, an explicit visit count wins over frequency x duration, then the latest."""
    earlier = [p for p in ps if _after(by_n[p["record_no"]], outcome_rec)]
    if not earlier:
        return None
    order = lambda p: (p["kind"] == "count", (by_n[p["record_no"]].get("date_iso") or "", p["record_no"]))
    return max(earlier, key=order)


def plan_vs_outcome(records: list) -> list:
    by_n = {r["n"]: r for r in records}
    ps = plans(records)
    out = []
    for r in sorted(records, key=lambda r: (r.get("date_iso") or "", r["n"])):
        hit = None if _paperwork(r) else next((u for u in _units(r) if _early_end(u) and not _other_person(u)), None)
        if not hit:
            continue
        plan = _canonical_plan(ps, r, by_n)
        if not plan:
            continue
        stated = [p for p in ps if _after(by_n[p["record_no"]], r)]
        note = "; ".join(f"record {p['record_no']}: {p['arithmetic']}" for p in sorted(stated, key=lambda p: p["record_no"]))
        out.append({"rule": "plan_vs_outcome", "category": "treatment_plan_vs_actual", "group": f"plan:{plan['record_no']}:{r['n']}",
                    "a": Quote(plan["record_no"], plan["quote"]), "b": Quote(r["n"], hit), "arithmetic": note})
    return out


def history_denials(records: list) -> list:
    out = []
    for r in records:
        for u in _denial_units(r):
            if _other_person(u):
                continue
            priors = []
            for o in records:
                if o["n"] == r["n"]:
                    continue
                seen = set()
                for h in lexicon_scan.scan(o.get("excerpt") or ""):
                    if h["category"] in _PRIOR_CATEGORIES and (h["unit_start"], h["unit_end"]) not in seen:
                        seen.add((h["unit_start"], h["unit_end"]))
                        q = o["excerpt"][h["unit_start"]:h["unit_end"]].strip()
                        if not _other_person(q):
                            priors.append((o, q))
                for ou in _units(o):                                  # an earlier accident or claim, which the phrase list does not cover
                    if (_PRIOR_EVENT.search(ou) or _earlier_year_accident(ou, r)) and not _DENIAL.search(ou) and not _other_person(ou) and ou not in [q for po, q in priors if po is o]:
                        priors.append((o, ou))
            if _ACCIDENT_STEM.match(u) and not _DENIAL.search(u):        # a form field about accidents is answered by an accident, not by a problem-list line
                priors = [(o, q) for o, q in priors if _PRIOR_EVENT.search(q) or _earlier_year_accident(q, r)]
            priors.sort(key=lambda p: (p[0].get("date_iso") or "", p[0]["n"]))
            for o, q in priors:
                out.append({"rule": "history_denial", "category": "other_fact_mismatch", "group": f"denial:{r['n']}:{u}",
                            "a": Quote(r["n"], u), "b": Quote(o["n"], q), "arithmetic": None})
    return out


def candidates(records: list) -> list:
    """All candidates in a fixed order (rule, then record numbers). Same records in, same list out."""
    out = plan_vs_outcome(records) + history_denials(records)
    out.sort(key=lambda c: (c["rule"], c["a"].record_no, c["b"].record_no, c["a"].text, c["b"].text))
    return out


# T-142: what the code checks, for GET case `checks`, so the UI can say it honestly. The first two are the candidate rules in this module (a judge classifies each
# pair); accident_date and provider_name are the structural checks in conflicts.py (no model). Everything else is not looked for (memory/SCOPE_CUTS.md row 13).
CONFLICT_LABELS = {
    "plan_vs_early_end": "A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early",
    "denial_vs_history": "A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record",
    "accident_date": "A stated accident date against the dates of the records, or two different stated accident dates",
    "provider_name": "The same clinician named under two different practice names",
}
NOT_CHECKED = [
    {"type": "dosage", "label": "Medication doses that differ between records"},
    {"type": "laterality", "label": "Left versus right across records (checked only inside one summary)"},
    {"type": "diagnosis", "label": "A diagnosis that differs or is withdrawn between records"},
    {"type": "pain_score", "label": "Pain scores that differ on the same day"},
    {"type": "treatment_duration_months", "label": "Plans and outcomes measured in months"},
    {"type": "informant_history", "label": "Patient history reported by a relative"},
]


_PAIR_TYPES = ("plan_vs_early_end", "denial_vs_history")
_ENGLISH_RULE_TYPES = _PAIR_TYPES + ("accident_date",)       # these read English wording; provider_name compares header labels and is language-free
_LANG_WORD = {"es": "Spanish", "uncertain": "an unidentified language", "other": "an unsupported language"}


def run_summary(records: list, *, stage: str) -> dict:
    """What THIS case's check stage did, for GET case `checks` (stored in the case config by the pipeline): only what cannot be recomputed from the stored
    records. stage: 'pending' (ingested or running), 'ran', or 'skipped' (the run deadline passed before the conflict stage). {conflicts_stage,
    read_records, unread: {lang: [record nos]}}. `read_records` counts records the English rules can read; Spanish, uncertain and unsupported-language
    records are listed in `unread`. The dated-record count and the notes are NOT stored: `checks` computes them from the current dates (T-141 r3)."""
    unread = {}
    for r in records:
        lang = r.get("lang") or "en"
        if lang != "en":
            unread.setdefault(lang, []).append(r["n"])
    return {"conflicts_stage": stage, "read_records": sum(1 for r in records if (r.get("lang") or "en") == "en"),
            "unread": {k: sorted(v) for k, v in sorted(unread.items())}}


def checks(run: dict = None, state: str = "complete", records: list = None) -> dict:
    """GET case `checks`, computed from what this case actually ran (T-141 r2/r3). `run` is run_summary() as stored; `state` is 'complete', 'not_run'
    (created, not analysed) or 'failed'; `records` are the case's records as they are NOW (store.load_records): the dated-record count and `notes` come from
    them, so confirming a date refreshes both. A case with no stored summary reports every check as not run (NOT_RUN): nothing is claimed about it.
    {conflict_types: [what ran], labels: {type: sentence}, skipped: [{type, label, reason_code, reason, record_nos?}], not_checked: [{type, label}],
    notes: [..]}. A type is in `skipped` without `record_nos` when it did not run at all (and is then absent from conflict_types), and with `record_nos`
    when it ran but could not read those records (Spanish and the like)."""
    from app.backend import conflicts
    run = run or None
    stage = (run or {}).get("conflicts_stage")
    dated = sum(1 for r in records if r.get("date_iso")) if records is not None else None
    skipped = []

    def skip(t, code, reason, nos=None):
        skipped.append({"type": t, "label": CONFLICT_LABELS[t], "reason_code": code, "reason": reason, **({"record_nos": nos} if nos else {})})

    for t in CONFLICT_LABELS:
        if run is None:
            skip(t, "NOT_RUN", "This case was analysed before the record of what ran was kept, so nothing is claimed about this check. Run it again to check.")
        elif t in _PAIR_TYPES and stage != "ran":
            if stage == "skipped":
                skip(t, "STAGE_SKIPPED", "The run reached its time limit before the comparison between records. Run it again to check.")
            elif state == "failed":
                skip(t, "RUN_FAILED", "The run stopped before the comparison between records finished.")
            else:
                skip(t, "NOT_RUN", "The comparison between records has not run yet.")
        elif t == "accident_date" and dated == 0:
            skip(t, "NO_DATED_RECORD", "No record has a date the code could read, so there is nothing to compare a stated accident date with.")
        elif t in _ENGLISH_RULE_TYPES and run.get("unread"):
            unread = run["unread"]
            nos = sorted(n for v in unread.values() for n in v)
            langs = " and ".join(_LANG_WORD.get(k, k) for k in unread)
            if run.get("read_records") == 0:
                skip(t, "LANGUAGE", f"This check reads English wording and every record is in {langs}, so it could not find anything.")
            else:
                skip(t, "LANGUAGE_PARTIAL", f"This check reads English wording; the records in {langs} were not read.", nos)
    whole = {x["type"] for x in skipped if "record_nos" not in x}
    note = conflicts.accident_date_note(records) if records is not None and "accident_date" not in whole else None
    return {"conflict_types": [t for t in CONFLICT_LABELS if t not in whole], "labels": dict(CONFLICT_LABELS), "skipped": skipped,
            "not_checked": [dict(x) for x in NOT_CHECKED], "notes": [note] if note else []}
