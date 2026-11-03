"""Stages 1-3 for entries: extract (LLM generator), verify (code), judge_entries (LLM judge 1). R-TL-1, R-TL-2, R-TL-4, R-TL-9, R-TL-10.
The model supplies {summary, excerpt} only. Provider and date come from the record header (code, D-014); offsets come from code;
state is composed by code (confidence.compose_state). A failing quote is never repaired: it is rejected and stays out of the timeline.
`call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is supplied by the pipeline."""
import copy
import re
from concurrent.futures import ThreadPoolExecutor

from pydantic import ValidationError

from app.backend import charge_text, confidence, grounding, injection, judges, language, schemas, spanish, summary_trim, why
from app.llm import audited as AU, promptlib, provider as P

CONCURRENCY = 3
_EXC = re.compile(r"^Excerpt:[ \t]*\"?", re.MULTILINE)


def body_offset(record: dict) -> int:
    """Absolute offset (in the normalised case text) where record['excerpt'] starts."""
    block = record.get("text", "")
    m = _EXC.search(block)
    base = record.get("char_start", 0)
    if m and block[m.end():].startswith(record["excerpt"][:20]):
        return base + m.end()
    i = block.find(record["excerpt"])
    return base + (i if i >= 0 else 0)


def extract_prompt(record: dict, nonce: str) -> str:
    return (f"SOURCE LABEL (context only; do not copy):\n{injection.wrap(record['source'], nonce)}\n"
            f"RECORD TEXT:\n{injection.wrap(record['excerpt'], nonce)}\nReturn the JSON object.")


def _ctx(record: dict, **extra) -> dict:
    return {"injection": bool(record.get("injection_tag")), "date_status": record.get("date_status", "parsed"),
            "translated": language.translated_record(record), **extra}


def _entry_base(record: dict, group: list, case_text: str) -> dict:
    return {"id": f"e{record['n']}", "seq": record["n"], "record_id": record["id"], "record_ids": [f"r{n}" for n in group],
            "date": record.get("date_iso"), "date_status": record.get("date_status", "parsed"),
            "provider": record["source"], "ai_drafted": True, "review_status": "pending"}


def extract_one(record: dict, group: list, *, call, case_text: str = "") -> dict:
    """One generator call. Returns an entry dict (pre-judge) or {'failure': code, 'record_no': n} when no output exists."""
    lang = language.record_lang(record)
    if lang == "other":                                   # D-042: only English and Spanish are read; say so, never guess
        return {"failure": "UNSUPPORTED_LANGUAGE", "record_no": record["n"]}
    step, item = (spanish.EXTRACT_STEP if language.is_translated(lang) else "extract"), f"e{record['n']}"
    n = promptlib.nonce(case_text, step, item)
    prompt = promptlib.load(spanish.EXTRACT_PROMPT if language.is_translated(lang) else "extract_v1")
    try:
        out, call_id = call(step, prompt.text, extract_prompt(record, n), schemas.ExtractOutput.model_json_schema(), item_id=item)
    except P.FixtureMiss:
        return {"failure": "FIXTURE_MISS", "record_no": record["n"]}
    except AU.LLMFailed:
        return {"failure": "LLM_FAILED_AFTER_RETRIES", "record_no": record["n"]}
    e = _entry_base(record, group, case_text)
    e["ladder"] = {"item_id": e["id"], "generator": {"model": judges.generator_model(), "prompt_version": prompt.name,
                                                      "call_id": call_id, "output": out if isinstance(out, dict) else None},
                   "judge": None, "code_checks": {}, "human": {"action": None, "edited_text": None, "at": None}}
    if language.is_translated(lang):                      # the quote stays in the original language; the summary is a labelled AI translation (D-042)
        e["ladder"]["translation"] = spanish.translation_info(lang)
    try:
        o = schemas.ExtractOutput.model_validate(out)
    except (ValidationError, TypeError, ValueError):
        e.update(summary="", excerpt="", excerpt_start=None, excerpt_end=None, source_kind="record")
        return compose(e, record, grounding_failures=["SCHEMA_INVALID"], schema_valid=False)
    def shape(excerpt):
        """D-054: (summary after code trims clauses the quote does not support, trim record or None, nothing_left). Only AI summaries over a quote that is in the record."""
        if language.is_translated(lang) or grounding.locate(record["excerpt"], excerpt) is None:
            return o.summary, None, False
        t = summary_trim.trim(o.summary, excerpt, record.get("source") or "", record.get("date_iso") or "")
        if not t["changed"]:
            return o.summary, None, False
        info = {"rule": "D-054", "original_summary": o.summary, "removed": t["removed"], "notes": t["notes"], "kept_summary": t["text"] or None}
        return (t["text"] or o.summary), info, not t["text"]

    summary, trim_info, empty = shape(o.excerpt)
    if trim_info:
        e["ladder"]["summary_trim"] = trim_info
        if empty:                                   # nothing the quote supports is left: could-not-verify tray (D-053), never judged, never in the letter
            return {"failure": "SUMMARY_NOT_IN_QUOTE", "record_no": record["n"],
                    "detail": {"generator": e["ladder"]["generator"], "summary_trim": trim_info, "excerpt": o.excerpt}}
        # the judge and every later check see the trimmed summary
    excerpt = o.excerpt
    nar = _narrowed(e, record, o, summary, shape) if not language.is_translated(lang) and charge_text.check(summary, excerpt) else None
    if nar:                                         # T-139: the quote without its currency-bearing end sentences; judge 1 runs on THIS pair (D-044/D-058)
        summary, excerpt, trim_info = nar["summary"], nar["excerpt"], nar["trim"]
        e["ladder"].pop("summary_trim", None)
        if trim_info:
            e["ladder"]["summary_trim"] = trim_info
        e["ladder"]["excerpt_narrowed"] = {"rule": "T-139", "original_excerpt": o.excerpt, "dropped": nar["dropped"],
                                             "summary_removed": nar["summary_removed"], "original_summary": o.summary,
                                             "summary_before_charge_trim": nar["summary_before_charge_trim"]}
    return verify(e, record, summary, excerpt)


def _narrowed(e: dict, record: dict, o, summary: str, shape):
    """T-139 (D-019, R-CH-7): when the quote's currency-bearing sentences sit at its start or end, code drops them (charge_text.narrow_excerpt) so the entry can reach the
    letter. Applied only when ALL hold: the narrowed pair states no amount (the summary clause is trimmed by D-054 when the quote no longer supports it), some summary is
    left, and every rung-1 check re-run on the narrowed pair (generator.verify) raises no reason the original pair did not already raise. Otherwise None: the entry keeps its
    quote and is held out as CHARGE_TEXT_IN_ENTRY."""
    n = charge_text.narrow_excerpt(o.excerpt)
    if n is None or grounding.locate(record["excerpt"], n["excerpt"]) is None:
        return None
    s2, trim2, empty = shape(n["excerpt"])
    removed, before_charge_trim = [], s2
    if not empty and charge_text.has_currency(s2):          # D-054 keeps a clause that shares a word with the label ('ED charge $3,915'): remove a trailing amount clause (suffix rule)
        t = charge_text.trim_summary(s2)
        if t["changed"]:
            s2, removed = t["text"], t["removed"]
    if empty or charge_text.check(s2, n["excerpt"]):
        return None
    base = verify(copy.deepcopy(e), record, summary, o.excerpt)["_stage"]
    trial = verify(copy.deepcopy(e), record, s2, n["excerpt"])["_stage"]
    if trial["grounding_failures"] or "CHARGE_TEXT_IN_ENTRY" in trial["code_reasons"] or set(trial["code_reasons"]) - set(base["code_reasons"]):
        return None
    return {"summary": s2, "excerpt": n["excerpt"], "dropped": n["dropped"], "trim": trim2, "summary_removed": removed,
            "summary_before_charge_trim": before_charge_trim}


def verify(e: dict, record: dict, summary: str, excerpt: str) -> dict:
    """Stage 2 (code): grounding of the excerpt, summary token/qualifier checks, offsets. Never edits the model's text."""
    body = record["excerpt"]
    g = spanish.module_for(language.record_lang(record))     # English: grounding itself; Spanish: the same checks mapped onto Spanish words
    exc_reasons = g.check_excerpt(body, excerpt)
    failures = [c for c in exc_reasons if c in confidence.REJECTED_CODES]
    code_reasons = [c for c in exc_reasons if c not in confidence.REJECTED_CODES]
    if language.record_lang(record) == "uncertain":          # D-042: never verified when the language is not confidently English or Spanish
        code_reasons.append("LANGUAGE_UNCERTAIN")
    span = grounding.locate(body, excerpt)
    if not failures:
        code_reasons += g.check_summary(summary, excerpt, record["source"], record.get("date_iso") or "")
        if span is None:
            code_reasons.append("HIGHLIGHT_NOT_FOUND")
        if charge_text.check(summary, excerpt):         # T-139 (D-019, R-CH-7): an amount in an entry never reaches the carrier letter; held out until the paralegal re-quotes or edits
            code_reasons.append("CHARGE_TEXT_IN_ENTRY")
    base = body_offset(record)
    e.update(summary=summary, excerpt=excerpt,
             excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None,
             source_kind="record")
    cc = e["ladder"]["code_checks"]
    cc.update(excerpt_verbatim=not failures, excerpt_whole_sentence="EXCERPT_NOT_WHOLE_SENTENCE" not in code_reasons,
              qualifier_carried="EXCERPT_OMITS_QUALIFIER" not in code_reasons and "SUMMARY_DROPS_QUALIFIER" not in code_reasons,
              date_provider_from_header=True,
              summary_tokens_not_in_excerpt=g.new_tokens(summary, excerpt, record["source"], record.get("date_iso") or "") if not failures else [],
              highlight_found=span is not None)
    return compose(e, record, grounding_failures=failures, code_reasons=list(dict.fromkeys(code_reasons)))


def compose(e: dict, record: dict, *, grounding_failures=None, code_reasons=None, schema_valid=True, judge="__keep__", fixture_miss=False) -> dict:
    """Set e['state'], e['reasons'], e['why'] from e['_stage'] (private inputs; callers drop '_' keys when storing). Re-run after the judge."""
    lad = e["ladder"]
    st = e.setdefault("_stage", {})
    if grounding_failures is not None:
        st["grounding_failures"] = grounding_failures
    if code_reasons is not None:
        st["code_reasons"] = code_reasons
    st.setdefault("code_reasons", [])
    st.setdefault("grounding_failures", [])
    st["schema_valid"] = schema_valid and st.get("schema_valid", True)
    if judge != "__keep__":
        st["judge"] = judge
    st["fixture_miss"] = fixture_miss or st.get("fixture_miss", False)
    state, reasons = confidence.compose_state(
        {"grounding_failures": st["grounding_failures"], "schema_valid": st["schema_valid"], "code_reasons": st["code_reasons"],
         "judge": st.get("judge")}, _ctx(record, fixture_miss=st["fixture_miss"]))
    e["state"], e["reasons"] = state, reasons
    e["why"] = why.join(reasons, lad.get("judge")) if reasons else "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
    jd = (lad.get("judge") or {})
    if jd.get("verdict") in ("partially", "unsupported") and why.judge_detail(jd.get("reason_code")):
        e["why"] += " " + why.judge_detail(jd["reason_code"])
    lad["state"] = state
    return e


def _one(args):
    record, group, call, case_text = args
    return extract_one(record, group, call=call, case_text=case_text)


def failure_entry(record: dict, group: list, failure: str, detail: dict = None) -> dict:
    """A record the extract step produced NO usable output for (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, UNSUPPORTED_LANGUAGE, SUMMARY_NOT_IN_QUOTE) as a could-not-verify tray
    item: state rejected, the failure code as its reason, no summary or quote. It never reaches the timeline or the letter, and it never vanishes:
    the paralegal sees the record with the reason and can write the entry by hand (D-031). `ladder.failure` marks it as a placeholder."""
    e = _entry_base(record, group, "")
    e.update(ai_drafted=False, summary=None, excerpt=None, excerpt_start=None, excerpt_end=None, source_kind="record", state="rejected", reasons=[failure], why=why.why(failure))
    e["ladder"] = {"item_id": e["id"], "generator": None, "judge": None, "failure": failure, "code_checks": {}, "state": "rejected",
                   "human": {"action": None, "edited_text": None, "at": None}}
    if detail:                                          # SUMMARY_NOT_IN_QUOTE (D-054): keep the model's call and what code removed, so the tray item is auditable
        e["ladder"]["generator"] = detail.get("generator")
        e["ladder"]["summary_trim"] = detail.get("summary_trim")
    return e


def resolved_placeholders(entries: list) -> set:
    """Ids of could-not-verify placeholders (`ladder.failure`) whose record now has a live entry, which is the entry the paralegal wrote by hand (T-110 r2).
    Such a placeholder is handled: the tray, the rejected counts and the export's excluded count leave it out. The row itself stays (audit)."""
    live = {r for e in entries if e["state"] != "rejected" for r in (e["record_ids"] or [])}
    return {e["id"] for e in entries if (e.get("ladder") or {}).get("failure") and e["state"] == "rejected" and live & set(e["record_ids"] or [])}


def entered_by_hand(entries: list) -> set:
    """T-165: record ids ("r6") that have a live entry the paralegal wrote by hand (manual entry, D-031: `ladder.entered_by == "reviewer"`, not rejected)."""
    return {r for e in entries if e["state"] != "rejected" and (e.get("ladder") or {}).get("entered_by") == "reviewer" for r in (e["record_ids"] or [])}


def hand_entered_warnings(entries: list) -> list:
    """T-165: one named warning per could-not-verify placeholder whose record the paralegal has since entered by hand. The extract step failed for that record, but nothing is
    missing from the timeline any more, so it is information for the case (not a run failure): `{code: ENTERED_BY_HAND, record_no, item_id (the placeholder), message}`."""
    hand = entered_by_hand(entries)
    out = []
    for e in entries:
        rids = e["record_ids"] or []
        if e["state"] == "rejected" and (e.get("ladder") or {}).get("failure") and rids and rids[0] in hand:
            n = int(rids[0][1:])
            out.append({"code": "ENTERED_BY_HAND", "record_no": n, "item_id": e["id"],
                        "message": f"{'The prepared-answer step' if AU.answers_prepared() else 'The AI step'} could not write an entry for record {n}; you entered it by hand."})      # D-069: the set in use chooses the wording
    return sorted(out, key=lambda w: w["record_no"])


def extract_entries(records: list, groups: list, *, call, case_text: str = "", workers: int = CONCURRENCY):
    """Stages 1-2 over distinct records (only the first record of each duplicate group is sent). Returns
    (entries, rejected, failures). `entries` are chronological by (date, seq) and never contain a rejected item; `rejected` goes to the
    tray only (R-TL-2). `failures` = [{'record_no', 'failure'}] for records with no output (LLM_FAILED_AFTER_RETRIES / FIXTURE_MISS)."""
    by_n = {r["n"]: r for r in records}
    jobs = [(by_n[g[0]], g, call, case_text) for g in groups]
    with ThreadPoolExecutor(max_workers=max(1, min(workers, CONCURRENCY))) as ex:
        results = list(ex.map(_one, jobs))
    made = [r for r in results if "failure" not in r]
    failures = [r for r in results if "failure" in r]
    entries = sorted((e for e in made if e["state"] != "rejected"), key=lambda e: (e["date"] or "9999-99-99", e["seq"]))
    rejected = [e for e in made if e["state"] == "rejected"]
    return entries, rejected, failures


def judge_entries(entries: list, records_by_n: dict, *, call, case_text: str = "") -> list:
    """Stage 3: judge 1 on every non-rejected entry. Judge failure -> 'unavailable' (JUDGE_UNAVAILABLE). Recomposes state."""
    def work(e):
        if e["state"] == "rejected":
            return e, None, False
        rec = records_by_n[e["seq"]]
        n = promptlib.nonce(case_text, "j1", e["id"])
        try:
            return e, spanish.run_j1_meta(e["summary"], e["excerpt"], rec["source"], call=call, nonce=n, item_id=e["id"], lang=language.record_lang(rec)), False
        except P.FixtureMiss:
            return e, ("unavailable", None, "NONE"), True
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        results = list(ex.map(work, entries))
    for e, res, miss in results:
        if res is None:
            continue
        verdict, call_id, code = res
        e["ladder"]["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(records_by_n[e["seq"]])), "call_id": call_id,
                                "verdict": verdict, "reason_code": code}
        compose(e, records_by_n[e["seq"]], judge=verdict, fixture_miss=miss)
    return entries
