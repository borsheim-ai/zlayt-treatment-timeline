"""Draft treatment paragraph in firm voice (D-031, stretch from the spec). Generated from ACCEPTED entries only.

Ladder for every sentence: (a) code: cites an accepted entry; numbers, sides, negations and dates are in that entry's quote (D-006),
no dropped hedge / attribution / negation (D-022), no causation or adverse wording that the quote itself does not contain, no flag
content; (b) judge 1 over the sentence and the quote; (c) the paralegal accepts or dismisses the paragraph. A sentence that fails (a) or
(b) is removed and listed with a reason. The draft is internal (internal notes) until accepted; flags are never given to the model.
"""
import re

from pydantic import ValidationError

from app.backend import export, grounding, injection, judges, lexicon_scan, schemas, store
from app.db import db as DB
from app.llm import audited as AU, promptlib, provider as P

REASONS = {
    "NOT_AN_ACCEPTED_ENTRY": "The sentence cites an entry that is not accepted.",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The sentence has a number, side, negation or date that is not in the cited quote.",
    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, an attribution phrase or a negation that the cited quote has.",
    "CAUSATION_NOT_QUOTED": "The sentence uses cause or adverse wording that the cited quote does not contain.",
    "SEVERITY_NOT_QUOTED": "The sentence uses severity, outcome or recommendation wording that the cited quote does not contain.",
    "FLAG_CONTENT": "The sentence talks about gaps, conflicts or other review flags, which stay out of the paragraph.",
    "JUDGE_PARTIAL": "The second check found the sentence only partly supported by the cited quote.",
    "JUDGE_UNSUPPORTED": "The second check found the sentence not supported by the cited quote.",
    "JUDGE_UNAVAILABLE": "The second check was not available for this sentence.",
}
_CAUSE = re.compile(r"\b(?:caused?|causing|due to|result(?:ed|ing)? (?:of|from|in)|because of|as a result|attributable|secondary to|"
                    r"led to|stemm(?:ed|ing) from|aggravat\w+|exacerbat\w+|permanent|chronic|disabl\w+)\b", re.IGNORECASE)
_FLAGISH = re.compile(r"\b(?:gaps?|conflicts?|inconsisten\w+|discrepanc\w+|pre-?existing|prior (?:injur\w+|condition)|missed appointments?|"
                      r"non-?complian\w+|days without treatment)\b", re.IGNORECASE)
# Severity / outcome / recommendation wording the prompt forbids ("no adjectives of your own", "never add a diagnosis, severity, prognosis"):
# deterministic backstop so a sentence like "significant pain 4/10" or "and recommended surgery" never rests on judge 1 alone.
_SEVERITY = re.compile(r"\b(?:significan\w*|sever(?:e|ely|ity)|serious\w*|ongoing|worsen\w*|worse|deteriorat\w*|debilitat\w*|excruciat\w*|"
                       r"substantial\w*|catastroph\w*|prognos\w+|recommend\w*|surg\w+)\b", re.IGNORECASE)
_DATE_PHRASE = re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,\s*\d{4})?", re.IGNORECASE)


basis_hash = export.basis_hash


def accepted_entries(case: dict) -> list:
    """Entries the paralegal accepted (or edited and accepted) whose quote is still verbatim in the record, chronological."""
    v = export._View(case)
    return [dict(e, label=v.source(e["record_no"]), date_iso=v.date_of(e), cite=v.cite(e["record_no"])) for e in v.in_entries]


def prompt_user(entries: list, nonce: str) -> str:
    blocks = []
    for e in entries:
        blocks.append(f"ENTRY {e['id']} | {export._long_date(e['date_iso'])} | {e['label']}\nSUMMARY:\n{injection.wrap(e['summary'], nonce)}\n"
                      f"QUOTE:\n{injection.wrap(e['excerpt'], nonce)}")
    return "ACCEPTED ENTRIES:\n" + "\n\n".join(blocks) + "\nReturn the JSON object."


def check_sentence(text: str, entry: dict) -> list:
    """Code checks (a); returns reason codes, empty when the sentence may go to the judge."""
    quote = entry["excerpt"]
    reasons = []
    if grounding.new_tokens(text, quote, entry["label"], entry["date_iso"] or ""):
        reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
    if grounding.dropped_qualifiers(_DATE_PHRASE.sub("", text), quote):      # 'On May 29, 2026' must not count as the hedge word 'may'
        reasons.append("SUMMARY_DROPS_QUALIFIER")
    q = quote.casefold()
    caused = [m.group(0) for m in _CAUSE.finditer(text) if m.group(0).casefold() not in q]
    adverse = [text[h["start"]:h["end"]] for h in lexicon_scan.scan(text) if text[h["start"]:h["end"]].casefold() not in q]
    if caused or adverse:
        reasons.append("CAUSATION_NOT_QUOTED")
    if [m.group(0) for m in _FLAGISH.finditer(text) if m.group(0).casefold() not in q]:
        reasons.append("FLAG_CONTENT")
    if [m.group(0) for m in _SEVERITY.finditer(text) if m.group(0).casefold()[:6] not in q]:     # a shared 6-letter stem counts as quoted ("recommend" for "recommended")
        reasons.append("SEVERITY_NOT_QUOTED")
    return list(dict.fromkeys(reasons))


def draft(conn, case_id: str, *, call, now=0.0) -> dict:
    """Generate, check, judge and store the draft paragraph in the case config. Returns the stored narrative dict."""
    case = DB.get_case(conn, case_id)
    entries = [e for e in accepted_entries(store.export_case(conn, case_id)) if not e.get("translation_label")]    # D-042: the firm-voice paragraph is English-only; translated entries keep their own labelled lines
    by_id = {e["id"]: e for e in entries}
    base = {"status": "pending", "generated_at": store.iso(now), "sentences": [], "removed": [], "prompt_version": "narrative_v1",
            "basis": {i: basis_hash(e) for i, e in by_id.items()}}
    existing = (case.get("config") or {}).get("narrative")
    if not entries:
        base["error"] = "NO_ACCEPTED_ENTRIES"                  # the API answers 400 for this, so nothing is stored either
        return dict(existing, error=base["error"]) if existing else base
    prompt = promptlib.load("narrative_v1")
    nonce = promptlib.nonce(case["raw_text"], "narrative", ",".join(by_id))
    try:
        out, call_id = call("narrative", prompt.text, prompt_user(entries, nonce), schemas.NarrativeOutput.model_json_schema(), item_id="narrative")
        sents = schemas.NarrativeOutput.model_validate(out).sentences
    except (AU.LLMFailed, P.FixtureMiss, ValidationError, TypeError, ValueError):
        base["error"] = "LLM_FAILED_AFTER_RETRIES"
        return _keep_or_save(conn, case_id, case, existing, base)
    base["generator"] = {"model": judges.generator_model(), "prompt_version": prompt.name, "call_id": call_id}
    for k, s in enumerate(sents, 1):
        text, eid = s.text.strip(), s.entry_id
        item = {"id": f"ns{k}", "entry_id": eid, "text": text}
        e = by_id.get(eid)
        if e is None:
            base["removed"].append({**item, "reason": "NOT_AN_ACCEPTED_ENTRY"})
            continue
        reasons = check_sentence(text, e)
        item["code_checks"] = {"reasons": reasons}
        if reasons:
            base["removed"].append({**item, "reason": reasons[0], "reasons": reasons})
            continue
        # the date of service lives in the record header, not the quote: give the judge the header it may rely on
        verdict, jcall, jcode = judges.run_j1_meta(text, e["excerpt"], f"{e['label']} (date of service {export._long_date(e['date_iso'])})",
                                                   call=call, item_id=item["id"])
        lad = judges.to_ladder("j1", verdict)
        item["judge"] = {"model": judges.judge_model(), "prompt_version": "judge_faithfulness_v1", "call_id": jcall, "verdict": lad, "reason_code": jcode}
        if lad != "supported":
            base["removed"].append({**item, "reason": {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED"}.get(lad, "JUDGE_UNAVAILABLE")})
            continue
        item["cite"] = e["cite"]
        base["sentences"].append(item)
    for r in base["removed"]:
        r["message"] = REASONS.get(r["reason"], r["reason"])
    return _save(conn, case_id, case, base)


def _keep_or_save(conn, case_id, case, existing, failed):
    """A draft that failed before producing sentences must not wipe a paragraph the paralegal already has (possibly accepted):
    keep it untouched in the case and return it with the error alongside. With nothing stored yet, the failed draft is stored."""
    if existing and (existing.get("sentences") or existing.get("removed")):
        return dict(existing, error=failed["error"])
    return _save(conn, case_id, case, failed)


def _save(conn, case_id, case, nar):
    cfg = dict(case.get("config") or {})
    cfg["narrative"] = nar
    DB.update_case(conn, case_id, config_json=cfg)
    return nar


def get(conn, case_id: str):
    return ((DB.get_case(conn, case_id) or {}).get("config") or {}).get("narrative")


def review(conn, case_id: str, action: str, now=0.0) -> dict:
    """accept | dismiss | reset on the whole paragraph (the paralegal's rung of the ladder)."""
    case = DB.get_case(conn, case_id)
    nar = dict((case.get("config") or {}).get("narrative") or {})
    if not nar:
        raise KeyError("narrative")
    if action not in ("accept", "dismiss", "reset"):
        raise ValueError(action)
    if action == "accept" and not nar.get("sentences"):
        raise ValueError("EMPTY")
    nar["status"] = {"accept": "accepted", "dismiss": "dismissed", "reset": "pending"}[action]
    nar["reviewed_at"] = store.iso(now)
    return _save(conn, case_id, case, nar)


def for_export(nar: dict) -> dict:
    """The small dict export.build_export() reads."""
    return {"status": nar["status"], "sentences": [{"text": s["text"], "entry_id": s["entry_id"], "cite": s["cite"]} for s in nar.get("sentences", [])],
            "removed": [{"text": r["text"], "entry_id": r["entry_id"], "reason": r["reason"], "message": r.get("message") or REASONS.get(r["reason"], r["reason"])} for r in nar.get("removed", [])],
            "basis": nar.get("basis", {})}
