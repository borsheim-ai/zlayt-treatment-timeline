"""LLM flag engines with the lexicon as the floor (ADR-008, ADR-013; R-FL-3..5, R-FL-7, R-FL-8; LLM_VS_CODE rows 11-13, 16).
Per-record pre_existing/causation pass (one call per record, so an injected record cannot suppress another record's flags) merged
with the code lexicon scan; one cross-record pass for semantic conflicts (accident-date and provider-name conflicts are code, conflicts.py).
The model returns only type, category and quoted text; titles and explanations are code templates. Flags never get a review_status
other than 'pending'. `call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is supplied by the pipeline."""
from pydantic import ValidationError

import re

from app.backend import conflict_candidates as CC, sentences, confidence, credibility, flag_templates as FT, generator, grounding, injection, judges, language, lexicon_scan, schemas, why
from app.llm import audited as AU, promptlib, provider as P

_PER_RECORD_TYPES = ("pre_existing", "causation")
# D-032: normal/negative findings are context only and never become flags (from either signal); a scene_facts flag needs a phrase-list
# hit on a specific adjuster phrase, never just a model's reading of a mechanism description.
_CONTEXT_ONLY = ("objective_negative",)
_NEEDS_LEXICON = ("scene_facts",)
# D-038 (narrows D-032): defense credibility phrases are the exception to "normal/negative is context only". They are what an adjuster quotes
# against the claimant, so the paralegal must see them first. Detected by credibility.scan (family match + negation), raised under their own
# category, never folded into a hedge flag. The lexicon's objective_negative hits (incl. the same phrases) stay context only.
CREDIBILITY_CATEGORY = credibility.CATEGORY
FILTER_RULES, FILTERED = FT.FILTER_RULES, FT.FILTERED       # D-057 (T-126): data lives in flag_templates so present.py can read it without importing the engines
JUDGE_PROMPT = {j: AU.PROMPT_OF_STEP[j] for j in ("j3", "j4")}


# ------------------------------------------------------------------ helpers
def _base(record: dict) -> int:
    return generator.body_offset(record) if record.get("text") else 0


def _render(f: dict, record: dict):
    try:
        f["title"], f["explanation"] = FT.render(f["type"], f["category"], provider=record.get("source"), date=record.get("date_iso"),
                                                 quote=f.get("excerpt"))
    except KeyError:    # a category outside the closed list: ground() rejects it; no model text is used as a title
        f["title"], f["explanation"] = FT.UNRECOGNISED


def _compose(f: dict) -> dict:
    st = f["_stage"]
    ladder = {"grounding_failures": st["grounding_failures"], "schema_valid": True, "code_reasons": [], "judge": st.get("judge")}
    ctx = {"injection": st["injection"], "agreement": st.get("agreement"), "fixture_miss": st.get("fixture_miss", False),
           "llm_failed": st.get("llm_failed", False), "translated": st.get("translated", False)}      # D-050
    f["state"], f["reasons"] = confidence.compose_state(ladder, ctx)
    f["why"] = why.join(f["reasons"], (f.get("ladder") or {}).get("judge")) if f["reasons"] else "Found by the phrase list and the model, and the second check agreed."
    return f


def _flag(record: dict, ftype: str, category: str, excerpt: str, origin: str, span, tagged: bool, agreement) -> dict:
    base = _base(record)
    f = {"type": ftype, "category": category, "excerpt": excerpt, "origin": origin, "record_no": record["n"],
         "record_id": record.get("id", f"r{record['n']}"), "review_status": "pending",
         "source_kind": "record",   # D-040: no code or model labels who is speaking
         "evidence": [{"record_no": record["n"], "text": excerpt,
                       "start": base + span[0] if span else None, "end": base + span[1] if span else None}],
         "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {}},
         "_stage": {"grounding_failures": [], "injection": tagged, "agreement": agreement, "translated": language.translated_record(record),
                    # model-involved flags are not verified until judge 4 has agreed ("unavailable" = not double-checked yet)
                    "judge": "unavailable" if origin != "lexicon" else None}}
    _render(f, record)
    return _compose(f)


# ------------------------------------------------------------------ lexicon floor
def _hedge_run(text: str, units: list, a: int, b: int):
    """A hedge unit travels with the adjacent hedge units (R-TL-8): the flag quotes the whole run, never half a hedge."""
    if not grounding.is_hedge_unit(text[a:b]):
        return a, b
    i = next(k for k, (x, y) in enumerate(units) if (x, y) == (a, b)) if (a, b) in units else None
    if i is None:
        return a, b
    lo = hi = i
    while lo > 0 and grounding.is_hedge_unit(text[units[lo - 1][0]:units[lo - 1][1]]):
        lo -= 1
    while hi + 1 < len(units) and grounding.is_hedge_unit(text[units[hi + 1][0]:units[hi + 1][1]]):
        hi += 1
    return units[lo][0], units[hi][1]


def lexicon_flags(record: dict, accident_year=None) -> list:
    """Flags from the phrase list alone: excerpt = the whole sentence unit that contains the hit; one flag per (unit, type)."""
    text = record["excerpt"]
    units = sentences.stripped_spans(text)
    seen, out = {}, []
    hits = []
    for h in lexicon_scan.scan(text, accident_year):
        if h["category"] not in _CONTEXT_ONLY:
            hits.append(h)
    hits += credibility.scan(text)
    prior_units = {(h["unit_start"], h["unit_end"]) for h in hits if h["flag_type"] == "pre_existing"}
    # a sentence that already carries a prior-condition flag does not also raise an "alternative cause" flag (same fact, one flag)
    hits = [h for h in hits if not (h["category"] == "alternative_cause" and (h["unit_start"], h["unit_end"]) in prior_units)]
    for h in hits:
        # a credibility hit's span is already its whole period sentence (D-043): it never pulls a neighbouring hedge sentence into the quote
        a, b = (h["unit_start"], h["unit_end"]) if h["category"] == CREDIBILITY_CATEGORY else _hedge_run(text, units, h["unit_start"], h["unit_end"])
        key = (a, b, h["flag_type"], CREDIBILITY_CATEGORY if h["category"] == CREDIBILITY_CATEGORY else None)   # D-038: never folded into a hedge flag
        if key in seen:
            seen[key]["lexicon_ids"].append(h["id"])
            continue
        f = _flag(record, h["flag_type"], h["category"], text[a:b], "lexicon", (a, b), False, "lexicon_only")
        f["lexicon_ids"] = [h["id"]]
        f["_span"] = (a, b)
        seen[key] = f
        out.append(f)
    return out


# ------------------------------------------------------------------ merge
def _overlap(a, b) -> bool:
    return bool(a and b and a[0] < b[1] and b[0] < a[1])


def _note_merged(f: dict, lf: dict) -> None:
    """Other categories the model proposed for the same quote (collapsed into this flag) go in the audit trail: ladder.code_checks.merged_categories."""
    extra = sorted(c for c in lf.get("_merged", []) if c and c != f["category"])
    if extra:
        f["ladder"] = dict(f["ladder"], code_checks=dict(f["ladder"].get("code_checks") or {}, merged_categories=extra))


def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False, *, llm_failed: bool = False, fixture_miss: bool = False) -> list:
    """Combine model flags and lexicon flags. Same type with overlapping spans -> origin 'both'; one side only -> LEXICON_ONLY / LLM_ONLY
    (needs_review). Grounding of model quotes is checked separately (ground()); a tagged record adds INJECTION_SUSPECTED to every flag."""
    body, out, used = record["excerpt"], [], set()
    uniq, seen, filtered, fseen = [], {}, [], set()
    for lf in llm_flags:
        if lf.get("category") in _CONTEXT_ONLY:       # D-032 + D-057: never a flag, but listed (collapsed, counted) rather than dropped
            k = (lf["type"], lf["category"], grounding.normalize(lf["excerpt"]))
            if k not in fseen:
                fseen.add(k)
                filtered.append(lf)
            continue
        k = (lf["type"], grounding.normalize(lf["excerpt"]))
        if k not in seen:
            seen[k] = lf
            uniq.append(lf)
        elif lf.get("category") != seen[k].get("category") and lf.get("category") not in seen[k].setdefault("_merged", []):
            seen[k]["_merged"].append(lf.get("category"))       # T-126 r2 / D-053: a second category on the same quote is not silently lost; the kept flag's code_checks names it
    # R-CO-7: the model's flag order must not decide ids or which model flag a lexicon flag pairs with. Sort by position in the record,
    # then type, category and text (code decides what code can decide).
    uniq.sort(key=lambda lf: ((grounding.locate(body, lf["excerpt"]) or (10 ** 9, 0))[0], lf["type"], lf["category"], grounding.normalize(lf["excerpt"])))
    llm_spans = [grounding.locate(body, lf["excerpt"]) for lf in uniq]
    for lx in lex_flags:
        lx = dict(lx)
        lx["_stage"] = dict(lx["_stage"], injection=tagged)
        match = next((i for i, lf in enumerate(uniq) if i not in used and lf["type"] == lx["type"] and _overlap(llm_spans[i], lx.get("_span"))), None)
        if match is not None:
            used.add(match)
            lx["origin"], lx["_stage"]["agreement"], lx["_stage"]["judge"] = "both", "both", "unavailable"
            lx["ladder"] = dict(lx["ladder"], judge=None)
            _note_merged(lx, uniq[match])
            # D-030: evidence is the verbatim phrase span the model returned (still grounded by ground()); the lexicon sentence is
            # only the fallback quote for phrase-list-only flags. A credibility flag is the exception (D-043, T-092): its excerpt is the whole
            # period sentence, so a model clause never replaces it (the positive half of a mixed sentence must stay in the quote).
            if lx["category"] != CREDIBILITY_CATEGORY:
                lx["excerpt"] = uniq[match]["excerpt"]
                sp = llm_spans[match]
                base = _base(record)
                lx["evidence"] = [{"record_no": record["n"], "text": lx["excerpt"],
                                   "start": base + sp[0] if sp else None, "end": base + sp[1] if sp else None}]
                lx["_span"] = sp or lx.get("_span")
            _render(lx, record)
        else:
            lx["origin"], lx["_stage"]["agreement"] = "lexicon", "lexicon_only"
            lx["_stage"]["llm_failed"], lx["_stage"]["fixture_miss"] = llm_failed, fixture_miss
            if llm_failed or fixture_miss:
                lx["_stage"]["agreement"] = None
        out.append(_compose(lx))
    for i, lf in enumerate(uniq):
        if i in used:
            continue
        f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", llm_spans[i], tagged, "llm_only")
        _note_merged(f, lf)
        if lf.get("category") in _NEEDS_LEXICON:
            f["_tray"] = "LLM_ONLY"      # D-032 + D-053: a scene_facts flag needs a phrase-list hit; the model's alone is shown in the tray, never dropped
        out.append(f)
    for lf in filtered:
        f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", grounding.locate(body, lf["excerpt"]), tagged, "llm_only")
        f["_tray"] = FILTERED
        f["_last"] = True       # after every other tray item, so no recorded judge prompt (it carries the flag id) changes
        out.append(f)
    for f in out:
        f["_stage"]["injection"] = tagged
        _compose(f)
    return out


def _model_conflicts(proposed: list, record: dict, tagged: bool) -> list:
    """A conflict the model proposed in the per-record pass (T-113, D-053; T-109 r2): only a code candidate (run_conflict_pass) can be a conflict flag, so the
    model's is a could-not-verify tray item (LLM_ONLY) with its own quotes and the fixed template title. It is not judged and never reaches the letter."""
    out, seen = [], set()
    for lf in proposed:
        k = (grounding.normalize(lf["excerpt"]), grounding.normalize(lf.get("excerpt_b") or ""), lf["category"])
        if k in seen:
            continue
        seen.add(k)
        f = _flag(record, "conflict", lf["category"], lf["excerpt"], "llm", grounding.locate(record["excerpt"], lf["excerpt"]), tagged, "llm_only")
        if lf.get("excerpt_b"):
            f["excerpt_b"] = lf["excerpt_b"]
            sb = grounding.locate(record["excerpt"], lf["excerpt_b"])
            f["evidence"].append({"record_no": record["n"], "text": lf["excerpt_b"],
                                  "start": _base(record) + sb[0] if sb else None, "end": _base(record) + sb[1] if sb else None})
            try:
                f["title"], f["explanation"] = FT.render("conflict", lf["category"], provider_a=record.get("source"), date_a=record.get("date_iso"),
                                                         quote_a=lf["excerpt"], quote_b=lf["excerpt_b"])
            except KeyError:
                pass        # a category outside the closed list: ground() marks it SCHEMA_INVALID (visible, not dropped); no model text is used as a title
        f["_tray"] = "LLM_ONLY"
        out.append(f)
    return out


def ground(flags: list, record: dict) -> list:
    """Rung 1 on model flags: quote must be verbatim in its record (else rejected, never repaired); category must belong to the type."""
    for f in flags:
        fail = []
        if grounding.locate(record["excerpt"], f["excerpt"]) is None:
            fail.append("GROUNDING_EXCERPT_NOT_VERBATIM")
        elif f["origin"] == "llm" and FT.TYPE_OF.get(f["category"]) != f["type"]:
            fail.append("SCHEMA_INVALID")
        f["_stage"]["grounding_failures"] = fail
        f["ladder"]["code_checks"] = {**{k: v for k, v in (f["ladder"].get("code_checks") or {}).items() if k == "merged_categories"},
                                      "excerpt_verbatim": "GROUNDING_EXCERPT_NOT_VERBATIM" not in fail, "highlight_found": f["evidence"][0]["start"] is not None}
        _compose(f)
    return flags


def _record_warning(record: dict) -> dict:
    hits = injection.scan(record["excerpt"])
    base = _base(record)
    title, expl = FT.render("record_warning", "injection_suspected", provider=record.get("source"), date=record.get("date_iso"),
                            quote=hits[0]["phrase"] if hits else None)
    return {"type": "record_warning", "category": "injection_suspected", "record_no": record["n"], "record_id": record.get("id", f"r{record['n']}"),
            "origin": "code", "title": title, "explanation": expl, "review_status": "pending", "state": "needs_review",
            "reasons": ["INJECTION_SUSPECTED"] + (["AI_TRANSLATION"] if language.translated_record(record) else []),      # D-050
            "why": why.why("INJECTION_SUSPECTED"), "excerpt": hits[0]["phrase"] if hits else "",
            "source_kind": "record",
            "evidence": [{"record_no": record["n"], "text": h["phrase"], "start": base + h["start"], "end": base + h["end"]} for h in hits],
            "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {"classified_by": "code:injection_scan"}}}


# ------------------------------------------------------------------ per-record pass
def run_flag_pass(record: dict, *, call, tagged: bool = False, accident_year=None, case_text: str = "") -> list:
    """One model call for this record only, merged with the lexicon floor. A failed or missed model call leaves the lexicon flags in place."""
    item = f"f_r{record['n']}"
    n = promptlib.nonce(case_text, "flags", item)
    prompt = promptlib.load("flags_v1")
    user = f"{injection.wrap(record['excerpt'], n)}\nReturn the JSON object."
    llm, conflicts, failed, miss = [], [], False, False
    try:
        out, _cid = call("flags", prompt.text, user, schemas.FlagPass.model_json_schema(), item_id=item)
        try:
            proposed = [f.model_dump() for f in schemas.FlagPass.model_validate(out).flags]
            llm = [f for f in proposed if f["type"] in _PER_RECORD_TYPES]
            conflicts = [f for f in proposed if f["type"] == "conflict"]
        except (ValidationError, TypeError, ValueError):
            failed = True
    except P.FixtureMiss:
        miss = True
    except AU.LLMFailed:
        failed = True
    flags = merge(llm, lexicon_flags(record, accident_year), record, tagged, llm_failed=failed, fixture_miss=miss)
    # tray items go LAST: a flag's id (f_r<n>_<k>) is its position in this list and is part of the judge's prompt, so inserting an item that used to be
    # dropped must not renumber the flags after it (recorded judge answers are keyed on that prompt)
    last = [f for f in flags if f.pop("_last", False)]
    flags = [f for f in flags if "_tray" not in f] + [f for f in flags if "_tray" in f and f not in last] + _model_conflicts(conflicts, record, tagged) + last
    ground(flags, record)
    for f in flags:
        code = f.pop("_tray", None)
        if code:
            _to_tray(f, code)       # after ground(), which recomposes the state; a rung-1 failure keeps its own reason after the tray code
    if tagged:
        flags.append(_record_warning(record))
    return flags


# ------------------------------------------------------------------ cross-record conflict pass
def _candidate_flag(c: dict, by_n: dict, any_tagged: bool, fid: str) -> dict:
    """A conflict flag built from a code candidate: both quotes are whole sentences cut from the record text, so rung 1 holds by construction
    (it is still checked, not assumed). Title and explanation come from the code template."""
    ra, rb = by_n[c["a"].record_no], by_n[c["b"].record_no]
    qa, qb = c["a"].text, c["b"].text
    sa, sb = grounding.locate(ra["excerpt"], qa), grounding.locate(rb["excerpt"], qb)
    fail = [] if (sa and sb) else ["GROUNDING_EXCERPT_NOT_VERBATIM"]
    title, expl = FT.render("conflict", c["category"], provider_a=ra.get("source"), date_a=ra.get("date_iso"), quote_a=qa,
                            provider_b=rb.get("source"), date_b=rb.get("date_iso"), quote_b=qb)
    f = {"id": fid, "type": "conflict", "category": c["category"], "excerpt": qa, "excerpt_b": qb, "origin": "code", "title": title, "explanation": expl,
         "record_no": ra["n"], "record_id": ra.get("id", f"r{ra['n']}"), "review_status": "pending", "source_kind": "record",
         "evidence": [{"record_no": r["n"], "text": q, "start": (_base(r) + s[0]) if s else None, "end": (_base(r) + s[1]) if s else None}
                      for r, q, s in ((ra, qa, sa), (rb, qb, sb))],
         "ladder": {"item_id": None, "generator": None, "judge": None,
                    "code_checks": {"classified_by": "code:conflict_candidate+j3", "candidate_rule": c["rule"], "arithmetic": c.get("arithmetic"),
                                    "excerpt_verbatim": not fail}},
         "_stage": {"grounding_failures": fail, "injection": any_tagged, "agreement": None, "judge": "unavailable",
                    "translated": language.translated_record(ra) or language.translated_record(rb)}, "_group": c["group"]}
    f["record_nos"] = sorted({ra["n"], rb["n"]})
    return _compose(f)


def run_conflict_pass(records: list, *, call, any_tagged: bool = False, case_text: str = "") -> list:
    """Conflicts between records (T-094, R-CO-7). CODE proposes the candidate pairs (conflict_candidates.py: a stated plan against a later early end,
    a denial of prior problems against a prior-condition sentence; frequency x duration is multiplied out, so '2x/week for 6 weeks' agrees with
    '12 visits' and is never asked about). The model's only job is the classification of each candidate, by J3 (judge_conflict_v6). There is no
    open-ended search call, so the set of candidates cannot vary between runs.
    Policy for the answer: conflict -> flag (verified when the other checks hold); unsure / judge failed -> flag stays needs_review;
    benign -> the could-not-verify tray (state rejected, JUDGE_DISAGREES), shown to the paralegal, never exported. For a denial, candidates are
    judged one at a time in record order and the first confirmed conflict stands (later ones are not asked)."""
    by_n = {r["n"]: r for r in records}
    cands = CC.candidates(records)
    flags, settled = [], set()
    for i, c in enumerate(cands, 1):
        f = _candidate_flag(c, by_n, any_tagged, f"f_cx{i}")
        flags.append(f)
        if c["group"] in settled and c["rule"] == "history_denial":
            f["_skip"] = True
            continue
        if f["state"] == "rejected":
            continue
        _judge_one(f, i - 1, call=call, case_text=case_text)
        if c["rule"] == "history_denial" and f["state"] != "rejected" and f["ladder"]["judge"]["verdict"] == "conflict":
            settled.add(c["group"])
    return [{k: v for k, v in f.items() if k not in ("_skip", "_group")} for f in flags if not f.get("_skip")]


# ------------------------------------------------------------------ rung 2 for flags (J3 / J4)
def _judge_one(f: dict, i: int, *, call, case_text: str = "") -> None:
    item = f.get("id") or f"f{i}"
    nonce = promptlib.nonce(case_text, "j3" if f["type"] == "conflict" else "j4", item)
    try:
        if f["type"] == "conflict":
            if not f.get("excerpt_b"):
                return
            v, cid, reason = judges.run_j3_meta(f["excerpt"], f["excerpt_b"], call=call, nonce=nonce, item_id=item, category=f["category"])
            step, pv = "j3", JUDGE_PROMPT["j3"]
        elif f["origin"] in ("llm", "both"):
            v, cid, reason = judges.run_j4_meta(f["excerpt"], f["type"], f["category"], call=call, nonce=nonce, item_id=item)
            step, pv = "j4", JUDGE_PROMPT["j4"]
        else:
            return
    except P.FixtureMiss:
        f["_stage"]["fixture_miss"] = True
        step = "j3" if f["type"] == "conflict" else "j4"
        v, cid, reason, pv = "unavailable", None, "NONE", JUDGE_PROMPT[step]
    f["ladder"]["judge"] = {"model": judges.judge_model(), "prompt_version": pv, "call_id": cid, "verdict": v, "reason_code": reason}
    f["_stage"]["judge"] = judges.to_ladder(step, v)
    _compose(f)
    # What the independent judge rejects (T-094, D-053): nothing is dropped. The item leaves the flag list and goes to the could-not-verify tray
    # with the judge's reason (visible in the API and UI, never a flag, never in the letter):
    # - a code-proposed conflict candidate judged benign (J3);
    # - a model-only flag (no phrase-list hit, no second source) judged not a flag (J4). Judge unsure or unavailable keeps any flag visible.
    if f["state"] != "rejected" and ((step == "j3" and v == "benign" and f.get("origin") == "code") or
                                      (step == "j4" and v == "disagree" and f.get("origin") == "llm")):
        _to_tray(f, "JUDGE_DISAGREES", reason)


def _to_tray(f: dict, code: str, judge_reason=None) -> None:
    """Move a flag to the could-not-verify tray: state rejected, the reason code first, a fixed sentence (plus the judge's fixed detail sentence)."""
    f["state"] = "rejected"
    if code == FILTERED:
        f["_stage"]["judge"] = None
        f["reasons"] = [FILTERED] + [r for r in f["reasons"] if r not in (FILTERED, "JUDGE_UNAVAILABLE", "LLM_ONLY")]       # keeps a grounding failure / injection reason (T-126 r2)
        f["why"] = why.why(FILTERED) + ("" if "GROUNDING_EXCERPT_NOT_VERBATIM" not in f["reasons"] else " " + why.why("GROUNDING_EXCERPT_NOT_VERBATIM"))
        return
    if code == "LLM_ONLY":
        # never sent to a judge by design (model-only, not code-confirmed): it carries its real reason, not the compose default "judge unavailable"
        # (T-122: the eval counted case_05's f_r1_1 as a judge that did not run)
        f["_stage"]["judge"] = None
        f["reasons"] = [r for r in f["reasons"] if r != "JUDGE_UNAVAILABLE"]
    f["reasons"] = [code] + [r for r in f["reasons"] if r != code]
    detail = why.judge_detail(judge_reason) if judge_reason else ""
    f["why"] = why.why(code) + (" " + detail if detail else "")
    if code == "LLM_ONLY" and f.get("type") == "conflict":
        f["why"] = why.MODEL_CONFLICT       # T-113 r2 F5: a conflict is never a phrase-list item; say why it is in the tray


def judge_flags(flags: list, *, call, case_text: str = "") -> list:
    """J4 on every model-involved pre_existing/causation flag. Lexicon-only flags have no judge.
    An unsure answer or failed judge call leaves the flag needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a disagreement on a flag that is both
    phrase-list and model leaves it needs_review (JUDGE_DISAGREES); a model-only flag J4 rejects goes to the tray (D-053, see _judge_one).
    A model-proposed CONFLICT is never a flag: only a code candidate (run_conflict_pass) can make one, so the model's goes to the tray (D-053)."""
    for i, f in enumerate(flags):
        if f["type"] == "record_warning" or f["state"] == "rejected":
            continue
        if f["type"] == "conflict" and f.get("origin") == "llm":
            _to_tray(f, "LLM_ONLY")
            continue
        _judge_one(f, i, call=call, case_text=case_text)
    return flags
