"""Check traces (D-042): the validation ladder rendered as ordered steps, read from data already stored. No writes, no model call.

item_trace(conn, case_id, item_id, full)  one item (entry, amount, flag, narrative sentence): extracted, each code check by name, judge, human.
case_trace(conn, case_id, full)           the pipeline: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate.
judge_report(conn, case_id, full)         counts per judge, objections, unresolved, code-vs-judge disagreements.

Visibility is the /audit split (D-020/D-036): full=False (public/demo) returns metadata only; full=True (ZLAYT_MODE=local) adds the model's raw
answer for LLM steps and the before/after of human events. Prompt text is never in a trace. Judge "rationale" is the fixed sentence for the judge's
closed reason_code (D-028), written by code; the model never supplies prose. Every `why`, `label` and `next_action.text` here is a fixed string.
"""
import contextvars
import functools
import json

from app.backend import flag_templates as FT, generator, grounding, narrative, present, review, store, why
from app.backend import judges as J
from app.db import db as DB
from app.llm import audited as AU

PASS, FAIL, SKIPPED, PENDING = "pass", "fail", "skipped", "pending"

# D-069 (T-177 r4): the wording of a trace is chosen by provenance. `use_voice(prep)` is set once per trace by its entry point (the item's or the case's `prepared` field); every sentence that
# would name an AI, a model or a drafter is written twice, side by side (`pick(recorded, prepared)` or a *_PREPARED table). Nothing is produced by rewriting the AI sentence.
_PREP = contextvars.ContextVar("trace_prepared", default=False)


def scoped(fn):
    """Entry points that build a trace set the voice for their own call only; whatever a caller had set comes back when they return."""
    @functools.wraps(fn)
    def wrapper(*a, **k):
        tok = _PREP.set(_PREP.get())
        try:
            return fn(*a, **k)
        finally:
            _PREP.reset(tok)
    return wrapper


def use_voice(prep):
    _PREP.set(bool(prep))


def pick(recorded, prepared):
    return prepared if _PREP.get() else recorded


def second_check(label):
    """'Second AI check: ...' (or 'Second check: ...' for prepared answers)."""
    return pick("Second AI check", "Second check") + label
_JUDGE_PREFIX = (("judge_faithfulness", "j1"), ("judge_amount_class", "j2"), ("judge_conflict", "j3"), ("judge_flag", "j4"))
JUDGE_LABEL = {"j1": "Is the summary supported by the quote?", "j2": "Is this figure a charge, rate or estimate?",
               "j3": "Do these two quotes really conflict?", "j4": "Does this flag fit the quote?"}
JUDGE_PROMPT = {j: AU.PROMPT_OF_STEP[j] for j in ("j1", "j2", "j3", "j4")}     # current prompt version per judge (single source: audited.PROMPT_OF_STEP)


def judge_of_prompt(pv):
    """j1..j4 for a judge prompt name (any version), else None."""
    return next((j for pre, j in _JUDGE_PREFIX if str(pv or "").startswith(pre)), None)


_LADDER_VOCAB = {"supported", "partially", "unsupported", "disagrees", "unsure", "unavailable"}
_RAW_TO_LADDER = {"agree": "supported", "conflict": "supported", "disagree": "disagrees", "benign": "disagrees"}
_OBJECTION = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES", "unsure": "JUDGE_UNSURE"}
_J_OK = {"j1": "The second check found every statement in the summary in the quote.",
         "j2": "The second check agreed with the rule's reading of this figure.",
         "j3": "The second check agreed that the two quotes conflict.",
         "j4": "The second check agreed that the flag fits the quote."}
_J_NO_CODE = {"j1": "partially", "j2": "unsure", "j3": "unsure", "j4": "unsure"}

# Trace-only reason codes (case level and narrative); item reason codes come from confidence.REASON_CODES / why.py.
TRACE_WHY = {
    "PENDING_DECISION": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
    "DATE_UNCONFIRMED": "This entry's date is not confirmed, so it cannot be accepted into the letter yet.",
    "EDIT_NOT_CONFIRMED_ITEM": "You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.",
    "EDIT_NOT_CONFIRMED_ITEM_AI": "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.",
    "EDIT_NOT_CONFIRMED": "An edited entry is still marked Needs review; it stays out of the letter until you compare it with the quote and accept it.",
    "ITEMS_NOT_REVIEWED": "Some items have no decision yet; they will not be in the letter and the AI disclosure line counts them.",
    "RUN_IN_PROGRESS": "The AI run is still going.",
    "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
    "NOTHING_ACCEPTED": "Nothing is accepted or edited yet, so the letter would be empty.",
    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
    "JUDGE_NOT_RUN_RETRIED": "You accepted this item, but the second AI check ran again and still gave no answer. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it. It clears when the check answers, or when you edit the summary in your own words.",
    "CODE_CHECK_FAILED_AI": "This summary was drafted by the AI and a code check on it fails, so it cannot go into the letter until the summary matches the quote.",
    "CODE_CHECK_FAILED": "You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter.",
    "NOT_AN_ACCEPTED_ENTRY": narrative.REASONS["NOT_AN_ACCEPTED_ENTRY"],
    "CAUSATION_NOT_QUOTED": narrative.REASONS["CAUSATION_NOT_QUOTED"],
    "SEVERITY_NOT_QUOTED": narrative.REASONS["SEVERITY_NOT_QUOTED"],
    "FLAG_CONTENT": narrative.REASONS["FLAG_CONTENT"],
}
TRACE_WHY_PREPARED = {      # twins of the TRACE_WHY sentences that name an AI (D-069)
    "EDIT_NOT_CONFIRMED_ITEM_AI": "You changed the quote, but the summary is still the prepared wording and its second check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.",
    "ITEMS_NOT_REVIEWED": "Some items have no decision yet; they will not be in the letter and the disclosure line counts them.",
    "RUN_IN_PROGRESS": "The run is still going.",
    "JUDGE_NOT_RUN": "You accepted this item, but the second check never ran on it. Nothing prepared goes into the letter without that check, and accepting does not replace it.",
    "JUDGE_NOT_RUN_RETRIED": "You accepted this item, but the second check ran again and still gave no answer. Nothing prepared goes into the letter without that check, and accepting does not replace it. It clears when the check answers, or when you edit the summary in your own words.",
    "CODE_CHECK_FAILED_AI": "This summary is a prepared answer and a code check on it fails, so it cannot go into the letter until the summary matches the quote.",
    "CODE_CHECK_FAILED": "You wrote or edited this summary, so the second check is not needed, but the code checks on the summary still have to pass before it can go into the letter.",
}
_NEXT_PREPARED = {"RERUN": "Run the steps again.", "CONFIRM_RERUN": "Run the steps again; confirm that earlier decisions are kept."}
_NEXT = {   # code -> fixed sentence
    "DECIDE": "Accept, edit or dismiss this item.",
    "CONFIRM_DATE": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.",
    "EDIT_SUMMARY": "Edit the summary so it uses only the numbers, dates and words that are in the quote, and keeps the quote's qualifiers.",
    "EDIT_QUOTE": "Edit the quote so it starts and ends on whole sentences and keeps the hedge sentence that qualifies it.",
    "READ_RECORD": "Read the record yourself before relying on this item.",
    "COMPARE_BY_HAND": "Compare the item with the quote yourself. Edit it, accept it if you agree with it, or dismiss it.",
    "DISMISS_OR_ENTER_BY_HAND": "This item cannot be used. Dismiss it, or write the entry by hand from the record.",
    "RERUN": "Run the AI steps again.",
    "RERUN_JUDGE": "Run the second check again.",
    "SENTENCE_REMOVED": "This sentence was left out of the draft. If you want its facts in the paragraph, check the cited entry's quote and write them yourself.",
    "CONFIRM_RERUN": "Run the AI steps again; confirm that earlier decisions are kept.",
    "CONFIRM_FLAG": "Confirm the flag by name, or dismiss the charge",       # same words as the 422 CONFIRM_REQUIRED next_action (review.confirm_error)
}
_STEP_OF_REASON = {
    "GROUNDING_EXCERPT_NOT_VERBATIM": "excerpt_verbatim", "GROUNDING_AMOUNT_NOT_IN_TEXT": "found_in_text", "SCHEMA_INVALID": "extracted",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "summary_tokens", "SUMMARY_DROPS_QUALIFIER": "summary_qualifier", "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge",
    "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight", "DATE_AMBIGUOUS": "date_confirmed",
    "DATE_MISSING": "date_confirmed", "ENDPOINT_NOT_VERIFIED": "endpoints_confirmed", "LEXICON_ONLY": "agreement", "LLM_ONLY": "agreement",
    "INJECTION_SUSPECTED": "injection_scan", "OCR_DERIVED": "ocr_source", "LLM_FAILED_AFTER_RETRIES": "extracted", "SUMMARY_NOT_IN_QUOTE": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
    "AMOUNT_ESTIMATE": "amount_class", "AMOUNT_DAMAGES": "amount_class", "AMOUNT_UNCLEAR": "amount_class", "CONFLICT_CHECK_INCOMPLETE": "record_warning_check",
    "SPLIT_AMBIGUOUS": "record_warning_check", "LLM_SPLIT": "record_warning_check"}
_AMOUNT_CODE = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
_CODE_CHECK_REASONS = set(review.CODE_CHECK_REASONS)


def reason_text(code: str) -> str:
    if code in TRACE_WHY:
        return (TRACE_WHY_PREPARED.get(code) if _PREP.get() else None) or TRACE_WHY[code]
    try:
        return why.why(code, prep=_PREP.get())
    except KeyError:
        return code


def na(code: str, target: dict = None, options: list = None, text: str = None) -> dict:
    d = {"code": code, "text": text or (_NEXT_PREPARED.get(code) if _PREP.get() else None) or _NEXT[code]}
    if target:
        d["target"] = target
    if options:
        d["options"] = options
    return d


def step(sid, label, kind, status, why_text, *, reason=None, rule=None, evidence=None, next_action=None, blocks=False, **extra):
    return {"id": sid, "label": label, "kind": kind, "status": status, "why": why_text, "reason_code": reason, "rule": rule,
            "blocks_export": bool(blocks), "evidence": evidence or {}, "next_action": next_action, **extra}


def _ocr_steps(R, rid) -> list:
    """T-086: the step that holds an OCR-read item for review. Only present when the item carries OCR_DERIVED, so other cases are unchanged."""
    if "OCR_DERIVED" not in R:
        return []
    return [step("ocr_source", "Record was not read from a scanned page", "code", FAIL, reason_text("OCR_DERIVED"), reason="OCR_DERIVED", rule="D-042",
                 evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid}))]


def _number(steps):
    for i, s in enumerate(steps, 1):
        s["n"] = i
    return steps


def _progress(steps):
    done = sum(1 for s in steps if s["status"] != PENDING)
    return {"done": done, "total": len(steps), "label": f"{done} of {len(steps)} steps settled"}


# ------------------------------------------------------------------ shared context
_STEPS_OF = {}      # kind -> step builder; filled after the builders are defined


class UnknownItem(KeyError):
    """The item id is not in this case (the API maps exactly this to 404)."""


class _Cx:
    def __init__(self, conn, case_id, full):
        self.conn, self.case_id, self.full = conn, case_id, bool(full)
        self.case = DB.get_case(conn, case_id)
        self.recs = present._recs_by_id(conn, case_id)
        self._live_recs = None
        calls = DB.list_llm_calls(conn, case_id)
        self.call_by_id = {c["id"]: c for c in calls}
        self.calls_by_item = {}
        for c in calls:
            self.calls_by_item.setdefault(c["item_id"], []).append(c)
        self.events = {}
        for e in DB.list_events(conn, case_id):
            self.events.setdefault(e["item_id"], []).append(e)
        self.models = present.models_for(conn, case_id, {"generator": J.generator_model(), "judge": J.judge_model()}, calls)      # T-177 r2: a prepared case names no drafting model
        self.prep = bool(self.models.get("generator_prepared"))      # D-069: the case's own provenance; an item's wording is this OR its own first answer's
        self.answers_prepared = AU.answers_prepared()      # T-177 r3: the fixture set in use is the curated one, so a missing or unusable answer is a prepared-answer matter, never a model's
        self.ran = self.case.get("run_started_at") is not None
        self.running = self.case["status"] == "running"

    @property
    def live_recs(self):
        """store.load_records() dicts (they carry the record body, source and language the code checks need), loaded once per context."""
        if self._live_recs is None:
            self._live_recs = store.load_records(self.conn, self.case_id, self.case["raw_text"])
        return self._live_recs

    def call(self, call_id, item_id=None, step_name=None):
        if call_id and call_id in self.call_by_id:
            return self.call_by_id[call_id]
        if item_id and step_name:
            hits = [c for c in self.calls_by_item.get(item_id, []) if c["step"] == step_name]
            return hits[-1] if hits else None
        return None


def _span(cx, rid, start, end, text):
    return {"record_id": rid, "start": start, "end": end, "text": text}


PREPARED_LABEL = "Prepared answer"      # D-069: the D-065 wording minus its "standing in for the AI draft" tail (only the badge tooltip may say AI)
PREPARED_WHY = "Prepared answer (hand-checked by the team for the demo)"
CASE_PREPARED_LABEL = "Prepared summaries and quotes for each record"
NO_PREPARED_ANSWER = "There is no prepared answer for this record in the demo, so no entry was made."
_AGREE = ("Phrase list and AI agree", "Phrase list and prepared answers agree")      # (recorded, prepared)
PREPARED_FLAGS_LABEL = "Prepared answers did not include this flag"
PREPARED_FLAGS_MISSING = "There is no prepared answer for this record's flags in the demo, so only the phrase list looked at it."


_WHY_CODES = set(why.all_codes())


def _first_call(cx, row, kind):
    """The generator call behind an item (entry: its extract call; flag: its record's flags/conflicts call), or None."""
    lad = row.get("ladder") or {}
    if kind == "entry":
        return cx.call((lad.get("generator") or {}).get("call_id"), row["id"], "extract")
    if kind == "flag" and row.get("origin") in present.FLAG_AI_ORIGINS:
        return cx.call((lad.get("generator") or {}).get("call_id")) or present.flag_generator_call(list(cx.call_by_id.values()), row["id"], row.get("type"))
    return None


def prepared_item(cx, row, kind) -> bool:
    """D-065: the item's first answer is a hand-checked fixture, or it has none and the set in use is the curated one. Then no sentence about it may say an AI drafted or found it."""
    if kind == "entry" and (row.get("ladder") or {}).get("entered_by"):
        return False
    if kind not in ("entry", "flag") or (kind == "flag" and row.get("origin") not in present.FLAG_AI_ORIGINS):
        return False
    call = _first_call(cx, row, kind)
    return AU.is_prepared(call.get("recorded_from")) if call and call.get("recorded_from") else cx.answers_prepared      # a call that gave no answer has no provenance: the set in use decides


def _llm_evidence(cx, role, model, prompt_version, call):
    ev = {"model": {"id": (call or {}).get("model") or model, "role": role,
                    "independent_of_generator": None if role == "generator" else ((call or {}).get("model") or model) != cx.models["generator"],
                    "prepared": bool(call) and AU.is_prepared(call.get("recorded_from"))}}      # D-065: a hand-checked fixture answer, not model output
    ev["prompt_version"] = None if ev["model"]["prepared"] else ((call or {}).get("prompt_version") or prompt_version)      # a prepared answer was prompted by nothing (T-177 r3)
    if call:
        meta = present._call(call, cx.full)
        for k in ("prompt_sha256", "backend", "recorded_from", "latency_ms", "parsed_ok"):
            ev[k] = meta.get(k)
        ev["call_id"] = call["id"]
        if cx.full:
            ev["response_raw"] = meta.get("response_raw")
    return ev


def _norm_verdict(step_id, v):
    if v in _LADDER_VOCAB:
        return v
    return _RAW_TO_LADDER.get(v, "unsure")


def _judge_reason_code(jd, call):
    code = (jd or {}).get("reason_code")
    if code:
        return code
    if call and call.get("response_raw"):
        try:
            got = json.loads(call["response_raw"])
            if isinstance(got, dict) and isinstance(got.get("reason_code"), str):
                return got["reason_code"]
        except (ValueError, TypeError):
            pass
    return None


def _judge_step(cx, item_id, jd, jid, R, *, sid=None, label=None, rule="row 4"):
    """One LLM judge step from ladder.judge (or None). Statuses: pass (supported), fail (objected/unsure), skipped (did not answer), pending (not run yet)."""
    sid = sid or f"judge_{jid[1]}"
    label = label or second_check(f": {JUDGE_LABEL[jid].lower()}")
    label = label[0].upper() + label[1:]
    jd = jd or {}
    raw = jd.get("verdict")
    call = cx.call(jd.get("call_id"), item_id, jid)
    if raw is None and not call:
        if not cx.ran:
            return step(sid, label, "llm", PENDING, "The second check has not run yet.", rule=rule, evidence={"model": {"id": cx.models["judge"], "role": "judge", "independent_of_generator": cx.models["judge"] != cx.models["generator"]}, "prompt_version": JUDGE_PROMPT[jid]},
                        next_action=na("RERUN"))
        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence={"judge_verdict": "unavailable"},
                    next_action=na("RERUN_JUDGE", {"item_id": item_id}))
    verdict = _norm_verdict(jid, raw if raw is not None else (call or {}).get("verdict"))
    ev = _llm_evidence(cx, "judge", jd.get("model") or cx.models["judge"], jd.get("prompt_version") or JUDGE_PROMPT[jid], call)
    rc = _judge_reason_code(jd, call)
    ev.update(judge_verdict=verdict, judge_reason_code=rc)
    if verdict == "supported":
        ev["rationale"] = _J_OK[jid]
        return step(sid, label, "llm", PASS, _J_OK[jid], rule=rule, evidence=ev)
    if verdict == "unavailable":
        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence=ev, next_action=na("RERUN_JUDGE", {"item_id": item_id}))
    code = _OBJECTION[verdict]
    detail = why.judge_detail(rc)
    ev["rationale"] = detail or reason_text(code)
    return step(sid, label, "llm", FAIL, (reason_text(code) + (" " + detail if detail else "")).strip(), reason=code, rule=rule, evidence=ev,
                next_action=na("COMPARE_BY_HAND"))


def _human_step(cx, row, kind, *, blocks_ok=True, extra_pending_next=None):
    """The paralegal's rung. pending (live item) blocks export; rejected can only be dismissed; dismissed is skipped."""
    rs, rejected = row["review_status"], row["state"] == "rejected"
    evs = cx.events.get(row["id"], [])
    ev = {"action": present.STATUS_ACTION.get(rs), "at": ((row.get("edited") or {}).get("at") if rs == "edited" else None),
          "events": [{"action": e["action"], "at": store.iso(e["at"]), **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),
                      **({"before": e["before"], "after": e["after"]} if cx.full else {})} for e in evs]}
    if evs:
        ev["at"] = store.iso(evs[-1]["at"])
    if rs == "edited":
        ed = row.get("edited") or {}
        if cx.full:
            ev["edited_text"] = ed.get("summary") or ed.get("note")
    if review.edit_unconfirmed(kind, row):      # T-134 r2: her edit is saved but she has not accepted it; the trail must not say she did (same rule as the gate, the export and the notes)
        return step("human", "Your decision", "human", PENDING, reason_text("EDIT_NOT_CONFIRMED_ITEM_AI" if ai_summary_unchecked(kind, row) else "EDIT_NOT_CONFIRMED_ITEM"), reason="EDIT_NOT_CONFIRMED", rule="row 17", evidence=ev, blocks=False,
                    next_action=na("DECIDE", {"item_id": row["id"]}, ["accept", "edit", "dismiss"]))
    if rs in ("accepted", "edited"):
        cf = (row.get("ladder") or {}).get("confirm") if kind == "amount" and rs == "accepted" else None
        said = f"You accepted this item and confirmed the flag \u201c{cf['name']}\u201d by name." if cf and cf.get("confirmed_at") else "You accepted this item."      # T-159
        return step("human", "Your decision", "human", PASS, said if rs == "accepted" else "You edited this item and accepted it.", rule="row 17", evidence=ev)
    if rs == "dismissed":
        return step("human", "Your decision", "human", SKIPPED, "You dismissed this item; it stays out of the letter.", rule="row 17", evidence=ev)
    if rejected:
        return step("human", "Your decision", "human", PENDING, "This item could not be verified, so it cannot be accepted.", reason="PENDING_DECISION", rule="row 17", evidence=ev,
                    next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"]))
    return step("human", "Your decision", "human", PENDING, reason_text("PENDING_DECISION"), reason="PENDING_DECISION", rule="row 17", evidence=ev, blocks=blocks_ok,
                next_action=extra_pending_next or na("DECIDE", {"item_id": row["id"]}, ["accept", "edit", "dismiss"]))


def _skipped(sid, label, kind, code, rule=None, rule_text=None):
    msg = rule_text or {"GROUNDING_EXCERPT_NOT_VERBATIM": "Not run: the quote did not pass the word-for-word check.",
                        "GROUNDING_AMOUNT_NOT_IN_TEXT": "Not run: the amount is not in the record text.",
                        "SCHEMA_INVALID": pick("Not run: the AI answer was malformed.", "Not run: the prepared answer could not be used."),
                        "SUMMARY_NOT_IN_QUOTE": pick("Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check.",
                                                     "Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check."),
                        "LLM_FAILED_AFTER_RETRIES": pick("Not run: the AI gave no usable answer for this record.", "Not run: there is no prepared answer for this record."),
                        "FIXTURE_MISS": pick("Not run: the AI gave no usable answer for this record.", "Not run: there is no prepared answer for this record."),
                        "UNSUPPORTED_LANGUAGE": pick("Not run: the record is not in a language the AI reads.", "Not run: the record is not in a language the tool reads.")
                        }.get(code, "Not run because an earlier step rejected this item.")
    return step(sid, label, kind, SKIPPED, msg, reason=code, rule=rule)


def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
    """Assemble the item trace: numbering, progress, verdict, state_reasons mapped to the step that explains them."""
    _number(steps)
    ids = {s["id"] for s in steps}
    rs = row.get("review_status")
    live = row.get("state") != "rejected"
    first_na = next((s["next_action"] for s in steps if s["next_action"]), None)
    gated = [s for s in steps if s["kind"] == "code" and s["status"] == FAIL and s.get("blocks_export")]      # D-045(b): human wording whose code check fails
    open_edit = review.edit_unconfirmed(kind, row)            # T-134 r2: edited, still Needs review, not accepted
    if rs in ("accepted", "edited", "dismissed"):
        first_na = gated[0]["next_action"] if gated else (next((s["next_action"] for s in steps if s["id"] == "human"), None) if open_edit else None)     # the human already decided; step-level hints stay on the steps, except a failing code check on their own wording
    if gated:      # whose words: only the paralegal's own summary is "your wording"; an AI draft is "this summary"
        code, label = "needs_attention", ("Needs your attention: a check on your wording fails" if _paralegal_wording(kind, row) else "Needs your attention: a check on this summary fails")
    elif open_edit:
        code, label = "edit_to_check", "Edited; waiting for your check"
    elif rs in ("accepted", "edited"):
        code, label = "accepted", "Accepted by you"
    elif rs == "dismissed":
        code, label = "dismissed", "Dismissed by you"
    elif row.get("state") == "rejected":
        code, label = "rejected", "Rejected; kept out of the letter"
    elif any(s["status"] == FAIL for s in steps):
        code, label = "needs_attention", "Needs your attention"
    elif any(s["status"] == PENDING and s["kind"] == "llm" for s in steps):
        code, label = "waiting_for_run", pick("Waiting for the AI run", "Waiting for the run")
    elif row.get("state") == "needs_review":
        code, label = "needs_attention", "Needs your attention"
    else:
        code, label = "ready_for_decision", "Ready for your decision"
    blocks = (live and rs == "pending") if blocks_flag is None else blocks_flag
    blocks = blocks or bool(gated)
    judge_id = next((s["id"] for s in steps if s["id"].startswith("judge_")), None)
    fallback = next((s["id"] for s in steps if s["status"] == FAIL), steps[0]["id"] if steps else None)   # e.g. record-warning flags have one code step

    def step_of(c):
        if c.startswith("JUDGE_") or c == "FIXTURE_MISS":
            return judge_id or fallback
        return _STEP_OF_REASON.get(c) if _STEP_OF_REASON.get(c) in ids else fallback
    reasons = [{"code": c, "why": reason_text(c), "step_id": step_of(c)} for c in (row.get("state_reasons") or [])]
    return {"token": cx.case_id, "item_id": item_id, "kind": kind, "mode": "full" if cx.full else "metadata", "state": row.get("state"),
            "review_status": rs, "state_reasons": reasons, "verdict": {"code": code, "label": label, "blocks_export": bool(blocks)},
            "progress": _progress(steps), "next_action": first_na, "steps": steps}


# ------------------------------------------------------------------ entries
def _excerpt_ev(cx, rid, row):
    ed = row.get("edited") or {}
    return _span(cx, rid, ed.get("excerpt_start", row.get("excerpt_start")), ed.get("excerpt_end", row.get("excerpt_end")), ed.get("excerpt", row.get("excerpt")))


_NO_LETTER = "Amounts go only in the Billed charges section and the internal notes, never in the letter's treatment text (D-019, R-CH-7)."


def _q(items) -> str:
    return " ".join(f"\u2018{x}\u2019" for x in items)


def _narrow_steps(lad: dict, row: dict) -> list:
    """T-139: code steps for what generation did to the AI's text because it states an amount. Internal: the trace is not the letter, so the removed text is quoted as written.
    `excerpt_narrowed` = the AI's quote lost its end sentence(s); `charge_clause_removed` = the AI summary lost its trailing amount clause(s). Both are PASS: nothing
    is wrong, but the text no longer equals what the model returned, and the second AI check saw the shortened pair (D-044/D-058)."""
    nar = lad.get("excerpt_narrowed") or {}
    out = []
    if nar.get("dropped"):
        out.append(step("excerpt_narrowed", "Code removed quote sentences that state an amount", "code", PASS,
                        f"Code removed {_q(nar['dropped'])} from the quote the {pick('AI', 'prepared answer')} picked. Why: it states a dollar amount. {_NO_LETTER} What is left is whole, "
                        f"word-for-word sentences of the record, every code check ran again on it, and the {pick('second AI check', 'second check')} saw the shortened quote.",
                        rule="T-139", evidence={"removed": list(nar["dropped"]), "quote_before": nar.get("original_excerpt"), "quote_after": row.get("excerpt"),
                                                "summary_before": nar.get("original_summary"), "summary_after": row.get("summary")}))
    if nar.get("summary_removed"):
        out.append(step("charge_clause_removed", "Code removed a summary clause that states an amount", "code", PASS,
                        f"Code removed {_q(nar['summary_removed'])} from the end of the {pick('AI', 'prepared')} summary. Why: it states a dollar amount, and the shortened quote no longer carries it. "
                        f"{_NO_LETTER}",
                        rule="T-139", evidence={"removed": list(nar["summary_removed"]), "summary_before": nar.get("summary_before_charge_trim") or nar.get("original_summary"),
                                                "summary_after": row.get("summary"), "original_summary": nar.get("original_summary"),
                                                "quote_before": nar.get("original_excerpt"), "quote_after": row.get("excerpt")}))
    return out


def _edit_trim_steps(row: dict) -> list:
    """T-139: when she picked a quote without the amount and code removed the amount clause from the AI summary in the same edit (review._edit; `edited.code_trim`)."""
    ct = (row.get("edited") or {}).get("code_trim")
    if not ct or not ct.get("removed"):
        return []
    return [step("charge_clause_removed", "Code removed a summary clause that states an amount", "code", PASS,
                 f"Code removed {_q(ct['removed'])} from the end of the {pick('AI', 'prepared')} summary when you changed the quote. Why: the new quote does not state the amount, and "
                 f"{_NO_LETTER} Check the summary against the quote.",
                 rule="T-139", evidence={"removed": list(ct["removed"]), "summary_before": ct.get("summary_before"), "summary_after": ct.get("summary_after"),
                                         "quote_before": ct.get("quote_before"), "quote_after": ct.get("quote_after")})]


def _entry_steps(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    rid = (row.get("record_ids") or [None])[0]
    rec = cx.recs.get(rid, {})
    exc = _excerpt_ev(cx, rid, row)
    # D-051: all five code checks (and the highlight) are recomputed from the CURRENT summary and quote, as accept does, and also honour what was stored
    live = review.code_check_failures(review.entry_record(row, cx.live_recs), row)
    placeholder = lad.get("failure")                      # could-not-verify tray placeholder: the AI made no usable summary, so there is no quote to check (T-112 r2)
    verbatim_fail = not placeholder and ("GROUNDING_EXCERPT_NOT_VERBATIM" in R or cc.get("excerpt_verbatim") is False or "GROUNDING_EXCERPT_NOT_VERBATIM" in live)
    schema_fail = "SCHEMA_INVALID" in R
    stop = "SCHEMA_INVALID" if schema_fail else (placeholder or ("GROUNDING_EXCERPT_NOT_VERBATIM" if verbatim_fail else None))
    st = []
    # 1 extracted
    if lad.get("entered_by"):
        st.append(step("extracted", "You wrote this entry", "human", PASS, pick("You wrote this summary and picked the quote; no AI drafted it.", "You wrote this summary and picked the quote."), rule="row 4",
                       evidence={"excerpt": exc}))
    else:
        gen = lad.get("generator") or {}
        call = cx.call(gen.get("call_id"), row["id"], "extract")
        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "extract_v1", call)
        ev["excerpt"] = exc
        prep = ev["model"]["prepared"] or (not (call and call.get("recorded_from")) and cx.answers_prepared)      # D-065 (T-177 r3): a failed or missing prepared answer is still a prepared answer, never "AI drafted"
        if prep and not ev["model"]["prepared"]:
            ev = {"excerpt": exc}      # the call gave no answer: no model is named
        xlabel = PREPARED_LABEL if prep else "AI drafted a summary and picked a quote"      # `prep` here is the item's own first answer; `voice` is the item's or the case's
        if schema_fail:
            st.append(step("extracted", xlabel, "llm", FAIL, reason_text("SCHEMA_INVALID"), reason="SCHEMA_INVALID", rule="row 4",
                           evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        elif "LLM_FAILED_AFTER_RETRIES" in R:
            st.append(step("extracted", xlabel, "llm", FAIL, reason_text("LLM_FAILED_AFTER_RETRIES"), reason="LLM_FAILED_AFTER_RETRIES",
                           rule="row 4", evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        elif "SUMMARY_NOT_IN_QUOTE" in R:                     # D-054: code removed every clause; the notes say which
            ev["removed"] = (lad.get("summary_trim") or {}).get("removed") or []
            st.append(step("extracted", xlabel, "llm", FAIL,
                           " ".join((lad.get("summary_trim") or {}).get("notes") or []) + " " + reason_text("SUMMARY_NOT_IN_QUOTE"), reason="SUMMARY_NOT_IN_QUOTE",
                           rule="D-054", evidence=ev, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        elif placeholder:                                     # no usable answer for this record (FIXTURE_MISS, an unsupported language ...): never a passing model step, and no model is named
            code = placeholder if placeholder in _WHY_CODES else "LLM_FAILED_AFTER_RETRIES"
            st.append(step("extracted", xlabel, "llm", FAIL, NO_PREPARED_ANSWER if (prep and code == "FIXTURE_MISS") else reason_text(code), reason=code, rule="row 4",
                           evidence={"excerpt": exc}, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
        else:
            if ev["model"]["prepared"]:
                st.append(step("extracted", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
            else:
                st.append(step("extracted", "AI drafted a summary and picked a quote", "llm", PASS,
                               "The AI read this record and proposed a one-line summary and a quote.", rule="row 4", evidence=ev))
            trim = lad.get("summary_trim")
            if trim and trim.get("removed"):                  # D-054: shown, never silent. The judge saw the trimmed summary.
                st.append(step("summary_trimmed", "Code removed summary parts the quote does not support", "code", PASS, " ".join(trim.get("notes") or []),
                               rule="D-054", evidence={"removed": trim["removed"], "original_summary": trim.get("original_summary"), "kept_summary": trim.get("kept_summary")}))
            st.extend(_narrow_steps(lad, row))                # T-139: code shortened the AI's quote / removed an amount clause; shown, never silent, never in the letter
    st.extend(_edit_trim_steps(row))                          # T-139: the quote-picker edit removed the amount clause from the AI summary

    def code_step(sid, label, code, ok_text, rule, fail_na, evidence=None, failed=None):
        if stop:
            st.append(_skipped(sid, label, "code", stop, rule))
        elif failed if failed is not None else code in R:
            st.append(step(sid, label, "code", FAIL, reason_text(code), reason=code, rule=rule, evidence=evidence, next_action=fail_na))
        else:
            st.append(step(sid, label, "code", PASS, ok_text, rule=rule, evidence=evidence))
    # 2 grounding substring
    if schema_fail or placeholder:
        st.append(_skipped("excerpt_verbatim", "Quote is word for word in the record", "code", stop, "row 4"))
    elif verbatim_fail:
        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", FAIL, reason_text("GROUNDING_EXCERPT_NOT_VERBATIM"),
                       reason="GROUNDING_EXCERPT_NOT_VERBATIM", rule="row 4", evidence={"excerpt": exc}, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": rid})))
    else:
        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", PASS, "The quote was found in the record, character for character.",
                       rule="row 4", evidence={"excerpt": exc}))
    code_step("excerpt_whole_sentence", "Quote is made of whole sentences", "EXCERPT_NOT_WHOLE_SENTENCE", "The quote starts and ends on whole sentences.", "row 4",
              na("EDIT_QUOTE", {"item_id": row["id"]}), failed="EXCERPT_NOT_WHOLE_SENTENCE" in R or cc.get("excerpt_whole_sentence") is False or "EXCERPT_NOT_WHOLE_SENTENCE" in live)
    code_step("excerpt_hedge", "Quote keeps the hedge sentence that qualifies it", "EXCERPT_OMITS_QUALIFIER", "No hedge sentence that qualifies the quote is left out.", "row 4",
              na("EDIT_QUOTE", {"item_id": row["id"]}), failed="EXCERPT_OMITS_QUALIFIER" in R or "EXCERPT_OMITS_QUALIFIER" in live)
    toks = cc.get("summary_tokens_not_in_excerpt") or (live.get("SUMMARY_TOKEN_NOT_IN_EXCERPT") or {}).get("tokens") or []
    code_step("summary_tokens", "Numbers and dates in the summary are in the quote", "SUMMARY_TOKEN_NOT_IN_EXCERPT",
              "Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote.", "D-034", na("EDIT_SUMMARY", {"item_id": row["id"]}),
              evidence={"tokens": toks}, failed="SUMMARY_TOKEN_NOT_IN_EXCERPT" in R or bool(toks) or "SUMMARY_TOKEN_NOT_IN_EXCERPT" in live)
    code_step("summary_qualifier", "Summary keeps the quote's qualifiers", "SUMMARY_DROPS_QUALIFIER", "Every hedge, attribution, negation, side and approximation in the quote is in the summary.",
              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R or "SUMMARY_DROPS_QUALIFIER" in live)
    code_step("highlight", "Quote can be highlighted in the record", "HIGHLIGHT_NOT_FOUND", "The quote's position in the record was found, so it can be highlighted.", "row 4",
              na("READ_RECORD", {"record_id": rid}), failed="HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False or "HIGHLIGHT_NOT_FOUND" in live)
    # date confirmed (D-041)
    unconf = review.date_unconfirmed(cx.conn, cx.case_id, "entry", row)
    live_pending = row["state"] != "rejected" and row["review_status"] == "pending"
    dev = {"date": {"record_id": rid, "date_raw": rec.get("date_raw"), "date_iso": rec.get("date_iso"), "date_status": rec.get("date_status"),
                    "candidates": rec.get("date_candidates") or []}}
    if unconf:
        code = "DATE_AMBIGUOUS" if rec.get("date_status") == "ambiguous" else "DATE_MISSING"
        nxt = na("CONFIRM_DATE", {"record_id": rid, "view": "dates_to_confirm"}) if code == "DATE_AMBIGUOUS" else na("READ_RECORD", {"record_id": rid})
        st.append(step("date_confirmed", "Date of service is confirmed", "code", FAIL, reason_text(code), reason=code, rule="D-041", evidence=dev,
                       next_action=nxt, blocks=live_pending))
    else:
        st.append(step("date_confirmed", "Date of service is confirmed", "code", PASS, "The date comes from the record's own header and is parsed or confirmed.",
                       rule="D-041", evidence=dev))
    # injection scan
    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED"), reason="INJECTION_SUSPECTED", rule="row 16",
                       evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid})))
    else:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16"))
    st += _ocr_steps(R, rid)
    # judge 1
    if stop:
        st.append(_skipped("judge_1", second_check(": is the summary supported by the quote?"), "llm", stop, "row 4"))
    else:
        st.append(_judge_step(cx, row["id"], lad.get("judge"), "j1", R))
    nxt = None
    if unconf:
        nxt = na("CONFIRM_DATE", {"record_id": rid, "view": "dates_to_confirm"}) if rec.get("date_status") == "ambiguous" else na("READ_RECORD", {"record_id": rid})
    if _code_check_gated(row):        # D-045(b), D-051: a failing code check blocks the export (AI-made or human wording; only the judge is exempt for human wording) and says what to do
        for s in st:
            if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS:
                s["blocks_export"] = True
                s["next_action"] = _fix_action(row, s)
    st.append(_human_step(cx, row, "entry", extra_pending_next=nxt))
    return st


def _code_check_gated(row) -> bool:
    """An accepted or edited, live entry: its failing code checks block the export (D-051). Accept refuses such an item, so this is old data or a
    state reached some other way; the gate does not trust that the accept guard ran."""
    return row["state"] != "rejected" and row["review_status"] in ("accepted", "edited")


def _current_text(row):
    ed = row.get("edited") or {}
    return ed.get("summary", row.get("summary") or ""), ed.get("excerpt", row.get("excerpt") or "")


def _fix_action(row, stp) -> dict:
    """The paralegal's next move for a failed code step on their own wording: a fixed sentence plus the words from the quote (display only; code decided the failure)."""
    code, summ, exc = stp["reason_code"], *_current_text(row)
    target = {"item_id": row["id"]}
    tail = " The export stays blocked until it passes."
    if code == "SUMMARY_DROPS_QUALIFIER":
        terms = grounding.missing_qualifier_terms(summ, exc)
        what = ", ".join(f"\u2018{t}\u2019" for t in terms) if terms else "the quote's hedge, attribution, negation, side or approximation"
        return na("EDIT_SUMMARY", target, text=f"Edit the summary to keep {what}; the quote says it and your summary leaves it out." + tail)
    if code == "SUMMARY_TOKEN_NOT_IN_EXCERPT":
        toks = (stp.get("evidence") or {}).get("tokens") or []
        what = ", ".join(f"\u2018{t}\u2019" for t in toks) if toks else "the words that are not in the quote"
        return na("EDIT_SUMMARY", target, text=f"Edit the summary to remove {what}, or change the quote so it contains {'it' if len(toks) == 1 else 'them'}." + tail)
    if code in ("EXCERPT_NOT_WHOLE_SENTENCE", "EXCERPT_OMITS_QUALIFIER", "GROUNDING_EXCERPT_NOT_VERBATIM"):
        return na("EDIT_QUOTE", target, text=_NEXT["EDIT_QUOTE"] + tail)
    return na("READ_RECORD", {"record_id": (row.get("record_ids") or [None])[0]}, text="Read the record yourself, then fix the quote or dismiss this item." + tail)


@scoped
def code_check_blockers(conn, case_id: str, cx=None) -> list:
    """Export blockers (D-045(b), D-051): accepted or edited entries, AI-made or human, whose current summary or quote fails a code check.
    One blocker per item, reason_code = its first failing check; `failed_steps` lists every failing step. Same steps the item trace shows, so gate and trace agree."""
    cx = cx or _Cx(conn, case_id, False)
    use_voice(cx.prep)
    out = []
    for row in DB.list_items(conn, case_id, "entry"):
        if not _code_check_gated(row):
            continue
        use_voice(cx.prep or prepared_item(cx, row, "entry"))
        fails = [s for s in _entry_steps(cx, row) if s["kind"] == "code" and s["status"] == FAIL and s.get("reason_code") in _CODE_CHECK_REASONS]
        if not fails:
            continue
        f = fails[0]
        out.append({"item_id": row["id"], "kind": "entry", "reason_code": f["reason_code"], "step_id": f["id"], "failed_steps": [x["id"] for x in fails],
                    "why": f["why"] + " " + reason_text("CODE_CHECK_FAILED" if _paralegal_wording("entry", row) else "CODE_CHECK_FAILED_AI"), "next_action": _fix_action(row, f)})
    return out


# ------------------------------------------------------------------ amounts
def _charge_flag_step(row, cf, rs):
    """T-159 (D-059): the code's flag on a charge (likely duplicate / likely total) as a step of the trail: which flag, the flag's own plain sentence, and the confirm. Pending
    until she accepts it with the named confirm (a flag whose confirm was given and then reset needs it again); pass after, with the flag, its name and when she confirmed."""
    vals = {"flag": cf["flag"], "name": cf["name"]}
    label = f"Flagged by the code: {cf['name']}"
    if rs in ("accepted", "edited") and cf.get("confirmed_at"):
        at = cf["confirmed_at"]
        return step("charge_flag", label, "code", PASS, f"{cf['message']} You confirmed this flag by name ({cf['name']}) on {at[:10]}, so the charge is counted.",
                    rule="D-059", evidence={"values": {**vals, "confirmed_at": at}})
    if rs == "dismissed":
        return step("charge_flag", label, "code", SKIPPED, f"{cf['message']} You dismissed this charge, so it is not counted and needs no confirm.", rule="D-059", evidence={"values": vals})
    return step("charge_flag", label, "code", PENDING, f"{cf['message']} It needs your named confirm before it is counted: accept it and confirm \u201c{cf['name']}\u201d, or dismiss it.",
                reason="CONFIRM_REQUIRED", rule="D-059", evidence={"values": vals}, next_action=na("CONFIRM_FLAG", {"item_id": row["id"]}, ["accept", "dismiss"]))


def _amount_steps(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    rid = (row.get("record_ids") or [None])[0]
    rec = cx.recs.get(rid, {})
    kind = row["kind"]
    vals = {"text": row["text"], "value_cents": row["value_cents"], "kind": kind, "classified_by": cc.get("classified_by")}
    exc = _span(cx, rid, row.get("excerpt_start"), row.get("excerpt_end"), row.get("excerpt"))
    gfail = "GROUNDING_AMOUNT_NOT_IN_TEXT" in R or cc.get("amount_in_text") is False
    st = []
    if gfail:
        st.append(step("found_in_text", "Dollar figure is in the record text", "code", FAIL, reason_text("GROUNDING_AMOUNT_NOT_IN_TEXT"), reason="GROUNDING_AMOUNT_NOT_IN_TEXT",
                       rule="row 6", evidence={"excerpt": exc, "values": vals}, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"])))
        st.append(_skipped("amount_class", "Rule says what the figure is", "code", "GROUNDING_AMOUNT_NOT_IN_TEXT", "row 7"))
    else:
        st.append(step("found_in_text", "Dollar figure is in the record text", "code", PASS, pick("Code found this figure in the record by pattern; it is not a model's claim.", "Code found this figure in the record by pattern; it is not a claim from any answer."),
                       rule="row 6", evidence={"excerpt": exc, "values": vals}))
        if kind == "charge":
            st.append(step("amount_class", "Rule says what the figure is", "code", PASS,
                           "A billing phrase in the record labels this figure a charge, so it counts toward the total once you accept it.", rule="row 7", evidence={"values": vals}))
        elif kind == "unclear":
            st.append(step("amount_class", "Rule says what the figure is", "code", FAIL, reason_text("AMOUNT_UNCLEAR"), reason="AMOUNT_UNCLEAR", rule="row 7",
                           evidence={"values": vals}, next_action=na("READ_RECORD", {"record_id": rid})))
        else:
            code = _AMOUNT_CODE[kind]
            st.append(step("amount_class", "Rule says what the figure is", "code", PASS, reason_text(code), reason=code, rule="row 7", evidence={"values": vals}))
    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED") + " An amount from such a record cannot become a charge.",
                       reason="INJECTION_SUSPECTED", rule="row 16", evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid})))
    else:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16"))
    st += _ocr_steps(R, rid)
    if gfail:
        st.append(_skipped("judge_2", second_check(": is this figure a charge, rate or estimate?"), "llm", "GROUNDING_AMOUNT_NOT_IN_TEXT", "row 7"))
    elif kind == "damages":
        st.append(step("judge_2", second_check(": is this figure a charge, rate or estimate?"), "llm", SKIPPED, "Damages and other non-bill figures are not sent to the second check.",
                       reason="AMOUNT_DAMAGES", rule="row 7"))
    elif lad.get("counted"):          # D-064
        st.append(step("judge_2", second_check(": is this figure a charge, rate or estimate?"), "llm", SKIPPED,
                       pick("You counted this line as a separate charge and confirmed it by name, so no AI check is asked about it.",
                            "You counted this line as a separate charge and confirmed it by name, so no second check is asked about it."), rule="D-064"))
    else:
        js = _judge_step(cx, row["id"], lad.get("judge"), "j2", R, rule="row 7")
        if acknowledge_only("amount", row) and js["status"] == SKIPPED and (js.get("evidence") or {}).get("judge_verdict") == "unavailable":
            js["why"] = "The second check did not run. It is optional for a rate: accepting a rate only acknowledges it, and a rate never reaches the letter."   # T-114
        st.append(js)
    rs = row["review_status"]
    cf = lad.get("confirm") if kind == "charge" and not gfail and row["state"] != "rejected" else None
    if cf:
        st.append(_charge_flag_step(row, cf, rs))
    if kind != "charge" or gfail or row["state"] == "rejected":
        why_t = reason_text(_AMOUNT_CODE[kind]) if kind in _AMOUNT_CODE else "Not a billed charge, so it is not added to the total."
        st.append(step("total_inclusion", "Counted in the total", "code", SKIPPED, why_t, reason=_AMOUNT_CODE.get(kind), rule="row 8"))
    elif rs == "dismissed":
        st.append(step("total_inclusion", "Counted in the total", "code", SKIPPED, "Dismissed, so it is not in the total.", rule="row 8"))
    elif rs in ("accepted", "edited"):
        st.append(step("total_inclusion", "Counted in the total", "code", PASS, "Accepted, so this charge is in the billed-charges total (added by code).", rule="row 8", evidence={"values": vals}))
    else:
        st.append(step("total_inclusion", "Counted in the total", "code", PENDING, "Detected but not in the accepted total until you accept it.", reason="PENDING_DECISION", rule="row 8",
                       evidence={"values": vals}, next_action=na("DECIDE", {"item_id": row["id"]}, ["accept", "dismiss"])))
    st.append(_human_step(cx, row, "amount"))
    return st


# ------------------------------------------------------------------ flags
def _flag_steps_core(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    ftype, origin, cat = row["type"], row["origin"], row["category"]
    recs = cx.recs
    spans = [{"record_id": e["record_id"], "start": e["start"], "end": e["end"], "text": e["excerpt"]} for e in present._evidence(row.get("evidence"), recs)]
    rids = [s["record_id"] for s in spans if s["record_id"]]
    rid0 = rids[0] if rids else None
    st = []
    injected = any(recs.get(r, {}).get("injection_tag") for r in rids) or "INJECTION_SUSPECTED" in R

    def inj():
        if injected:
            return step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED"), reason="INJECTION_SUSPECTED", rule="row 16",
                        next_action=na("READ_RECORD", {"record_id": rid0}))
        return step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16")
    if ftype == "record_warning":
        code = {"injection_suspected": "INJECTION_SUSPECTED", "analysis_incomplete": "CONFLICT_CHECK_INCOMPLETE", "llm_split": "LLM_SPLIT", "date_ambiguous": "DATE_AMBIGUOUS"}.get(cat) \
            or next(iter(R), None)
        st.append(step("record_warning_check", "Code check on the record or the run", "code", FAIL, reason_text(code) if code else row["explanation"], reason=code,
                       rule="row 16" if cat == "injection_suspected" else "row 1", evidence={"values": {"category": cat}, "spans": spans},
                       next_action=na("CONFIRM_DATE", {"record_id": rid0, "view": "dates_to_confirm"}) if cat == "date_ambiguous"
                       else (na("READ_RECORD", {"record_id": rid0}) if rid0 else na("RERUN"))))
        st.append(_human_step(cx, row, "flag"))
        return st
    if origin == "code" and cc.get("candidate_rule"):
        # T-094: a conflict pair proposed by code and classified by the judge (J3). The model proposed nothing.
        comp = present._computed(row.get("computed"))
        arith = cc.get("arithmetic")
        st.append(step("paired_by_code", "Code paired these two quotes", "code", PASS,
                       "Software found a stated plan and a later record that shows it ended early" if cc["candidate_rule"] == "plan_vs_outcome"
                       else "Software found a denial of prior problems and another record that mentions an earlier problem",
                       rule="row 10", evidence={"values": {"rule": cc["candidate_rule"], "arithmetic": arith}, "spans": spans}))
        bad = row["state"] == "rejected" and "JUDGE_DISAGREES" not in R or cc.get("excerpt_verbatim") is False
        st.append(step("spans_match", "Cited text matches the record", "code", FAIL if bad else PASS,
                       reason_text("GROUNDING_EXCERPT_NOT_VERBATIM") if bad else "Both quotes are in the records, character for character.",
                       reason="GROUNDING_EXCERPT_NOT_VERBATIM" if bad else None, rule="row 4", evidence={"spans": spans}))
        st.append(inj())
        st.append(_judge_step(cx, row["id"], lad.get("judge"), "j3", R, rule="row 11"))
        st.append(_human_step(cx, row, "flag"))
        return st
    if origin == "code":
        comp = present._computed(row.get("computed"))
        vals = {k: comp[k] for k in ("from", "to", "days", "threshold", "stated_dates", "body_date", "first_treatment_date", "names", "subtype") if k in comp}
        st.append(step("computed", "Dates compared by code" if ftype == "gap" else "Stated and recorded dates compared by code", "code", PASS,
                       row["explanation"] or "Computed by code from the record dates.", rule="row 9" if ftype == "gap" else "row 10", evidence={"values": vals, "spans": spans}))
        bad = row["state"] == "rejected" or cc.get("spans_match_input") is False
        st.append(step("spans_match", "Cited text matches the record", "code", FAIL if bad else PASS,
                       reason_text("GROUNDING_EXCERPT_NOT_VERBATIM") if bad else "Every cited date line is in the record, character for character.",
                       reason="GROUNDING_EXCERPT_NOT_VERBATIM" if bad else None, rule="row 10", evidence={"spans": spans},
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"]) if bad else None))
        if "ENDPOINT_NOT_VERIFIED" in R:
            st.append(step("endpoints_confirmed", "Dates at both ends are confirmed", "code", FAIL, reason_text("ENDPOINT_NOT_VERIFIED"), reason="ENDPOINT_NOT_VERIFIED", rule="row 9",
                           next_action=na("CONFIRM_DATE", {"view": "dates_to_confirm"})))
        else:
            st.append(step("endpoints_confirmed", "Dates at both ends are confirmed", "code", PASS, "Both dates are parsed or confirmed.", rule="row 9"))
        st.append(inj())
        st += _ocr_steps(R, rid0)
        st.append(step("judge_not_needed", second_check(""), "llm", SKIPPED, "Not needed: this is arithmetic over dates in the record, which code does exactly.", rule="row 9"))
        st.append(_human_step(cx, row, "flag"))
        return st
    has_llm, has_lex = origin in ("llm", "lexicon+llm"), origin in ("lexicon", "lexicon+llm")
    if ftype == "conflict":
        pass                                  # a conflict is the AI's pair proposal (row 11): no phrase list, so no agreement step
    elif has_lex:
        st.append(step("proposed_by_phrase_list", "Phrase list found it", "code", PASS, "The researched phrase list found this wording in the record.", rule="row 12", evidence={"spans": spans}))
    else:
        st.append(step("proposed_by_phrase_list", "Phrase list found it", "code", SKIPPED, reason_text("LLM_ONLY"), reason="LLM_ONLY", rule="row 12"))
    prep = prepared_item(cx, row, "flag")      # D-065 (T-177 r3): the flag's first answer is its record's flag call, which a curated set makes a prepared answer
    if has_llm:
        gen = lad.get("generator") or {}
        step_name = "conflicts" if ftype == "conflict" else "flags"
        call = _first_call(cx, row, "flag")
        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or AU.PROMPT_OF_STEP.get(step_name), call)
        if ev["model"]["prepared"]:
            st.append(step("proposed_by_ai", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
        elif prep:      # no usable prepared answer for this record's flags: no model is named
            st.append(step("proposed_by_ai", PREPARED_FLAGS_LABEL, "llm", SKIPPED, PREPARED_FLAGS_MISSING, reason="FIXTURE_MISS", rule="D-065"))
        else:
            st.append(step("proposed_by_ai", "AI found it", "llm", PASS, "The AI proposed this flag as a category and a quote; it wrote no explanation.", rule="row 12", evidence=ev))
    elif prep:
        st.append(step("proposed_by_ai", PREPARED_FLAGS_LABEL, "llm", SKIPPED, reason_text("LEXICON_ONLY"), reason="LEXICON_ONLY", rule="D-065"))
    else:
        st.append(step("proposed_by_ai", "AI found it", "llm", SKIPPED, reason_text("LEXICON_ONLY"), reason="LEXICON_ONLY", rule="row 12"))
    if ftype == "conflict":
        pass
    elif has_llm and has_lex:
        st.append(step("agreement", _AGREE[1 if prep else 0], "code", PASS, pick("Both the phrase list and the AI found this flag.", "Both the phrase list and the prepared answers include this flag."), rule="row 12"))
    else:
        code = "LEXICON_ONLY" if origin == "lexicon" else "LLM_ONLY"
        if code in R:
            st.append(step("agreement", _AGREE[1 if prep else 0], "code", FAIL, reason_text(code), reason=code, rule="row 12", next_action=na("COMPARE_BY_HAND", {"item_id": row["id"]})))
        else:
            other = next((c for c in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS") if c in R), None)
            st.append(step("agreement", _AGREE[1 if prep else 0], "code", SKIPPED, reason_text(other) if other else "Only one source looked at this record, so there is nothing to compare.",
                           reason=other, rule="row 12"))
    if cat == "credibility_language":
        st.append(step("credibility_wording", "Credibility wording is not a clean negation", "code", PASS,
                       "The sentence uses a credibility term and is not a plain negation such as 'No Waddell signs', so it is flagged for you to see first.", rule="D-043"))
    vfail = "GROUNDING_EXCERPT_NOT_VERBATIM" in R or "SCHEMA_INVALID" in R or cc.get("excerpt_verbatim") is False
    if vfail:
        code = "SCHEMA_INVALID" if "SCHEMA_INVALID" in R else "GROUNDING_EXCERPT_NOT_VERBATIM"
        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", FAIL, reason_text(code), reason=code, rule="row 4", evidence={"spans": spans},
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"])))
        st.append(_skipped("highlight", "Quote can be highlighted in the record", "code", code, "row 4"))
    else:
        st.append(step("excerpt_verbatim", "Quote is word for word in the record", "code", PASS, "The quote was found in the record, character for character.", rule="row 4", evidence={"spans": spans}))
        if "HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False or any(s["start"] is None for s in spans):
            st.append(step("highlight", "Quote can be highlighted in the record", "code", FAIL, reason_text("HIGHLIGHT_NOT_FOUND"), reason="HIGHLIGHT_NOT_FOUND", rule="row 4",
                           next_action=na("READ_RECORD", {"record_id": rid0})))
        else:
            st.append(step("highlight", "Quote can be highlighted in the record", "code", PASS, "The quote's position in the record was found.", rule="row 4"))
    st.append(inj())
    st += _ocr_steps(R, rid0)
    jid = "j3" if ftype == "conflict" else "j4"
    if vfail:
        st.append(_skipped(f"judge_{jid[1]}", second_check(f": {JUDGE_LABEL[jid].lower()}"), "llm", "GROUNDING_EXCERPT_NOT_VERBATIM", "row 11" if jid == "j3" else "row 12"))
    elif not has_llm:
        st.append(step(f"judge_{jid[1]}", second_check(f": {JUDGE_LABEL[jid].lower()}"), "llm", SKIPPED,
                       pick("Not run: only the phrase list found this flag, so there is no AI answer to double-check; it stays marked for review.",
                            "Not run: only the phrase list found this flag, so there is no prepared answer to double-check; it stays marked for review."), reason="LEXICON_ONLY",
                       rule="row 11" if jid == "j3" else "row 12"))
    else:
        jd = lad.get("judge")
        pv = (jd or {}).get("prompt_version")
        jid = (judge_of_prompt(pv) or jid)
        st.append(_judge_step(cx, row["id"], jd, jid, R, rule="row 11" if jid == "j3" else "row 12"))
    st.append(_human_step(cx, row, "flag"))
    return st


# ------------------------------------------------------------------ narrative sentences
def _ntext(code):
    return narrative.REASONS.get(code) or reason_text(code)


def _narrative_trace(cx, item_id):
    nar = narrative.get(cx.conn, cx.case_id) or {}
    sent = next((s for s in nar.get("sentences", []) if s["id"] == item_id), None)
    rem = next((s for s in nar.get("removed", []) if s["id"] == item_id), None)
    s = sent or rem
    if s is None:
        raise UnknownItem(item_id)
    reason = (rem or {}).get("reason")
    rcodes = list((rem or {}).get("reasons") or []) if reason not in ("NOT_AN_ACCEPTED_ENTRY",) and not str(reason).startswith("JUDGE_") else []
    st = []
    gen = nar.get("generator") or {}
    call = cx.call(gen.get("call_id"))
    ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or "narrative_v1", call)
    ev["values"] = {"entry_id": s["entry_id"], "text": s["text"]}
    if ev["model"]["prepared"]:
        st.append(step("extracted", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
    else:
        st.append(step("extracted", "AI wrote this sentence from an accepted entry", "llm", PASS, "The AI wrote the sentence and named the one accepted entry it comes from.", rule="D-031", evidence=ev))
    cited_ok = reason != "NOT_AN_ACCEPTED_ENTRY"
    st.append(step("cites_accepted_entry", "Cites an accepted entry", "code", PASS if cited_ok else FAIL, "The sentence cites an entry you accepted." if cited_ok else TRACE_WHY["NOT_AN_ACCEPTED_ENTRY"],
                   reason=None if cited_ok else "NOT_AN_ACCEPTED_ENTRY", rule="D-031", evidence={"values": {"entry_id": s["entry_id"]}},
                   next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]}) if not cited_ok else None))
    if not cited_ok:
        st.append(_skipped("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", "NOT_AN_ACCEPTED_ENTRY", "D-006", "Not run: the cited entry is not accepted."))
    elif rcodes:
        st.append(step("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", FAIL, " ".join(_ntext(c) for c in rcodes),
                       reason=rcodes[0], rule="D-006", evidence={"reasons": rcodes}, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
    else:
        st.append(step("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", PASS,
                       "Every number, date and qualifier is in the cited quote, and the sentence adds no cause, severity or flag wording.", rule="D-006", evidence={"reasons": []}))
    if not cited_ok or rcodes:
        st.append(_skipped("judge_1", second_check(": is the summary supported by the quote?"), "llm", reason if not cited_ok else rcodes[0], "row 4"))
    else:
        jd = s.get("judge") or {}
        verdict = jd.get("verdict")
        jcall = cx.call(jd.get("call_id"), s["id"], "j1")
        ev = _llm_evidence(cx, "judge", jd.get("model") or cx.models["judge"], jd.get("prompt_version") or "judge_faithfulness_v1", jcall)
        if verdict:
            ev.update(judge_verdict=verdict, judge_reason_code=jd.get("reason_code"))
        if verdict == "supported":
            ev["rationale"] = _J_OK["j1"]
            st.append(step("judge_1", second_check(": is the sentence supported by the quote?"), "llm", PASS, _J_OK["j1"], rule="row 4", evidence=ev))
        elif verdict in ("partially", "unsupported"):
            detail = why.judge_detail(jd.get("reason_code"))
            ev["rationale"] = detail or narrative.REASONS[reason]
            st.append(step("judge_1", second_check(": is the sentence supported by the quote?"), "llm", FAIL, (narrative.REASONS.get(reason, "") + " " + detail).strip(),
                           reason=reason, rule="row 4", evidence=ev, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
        else:
            st.append(step("judge_1", second_check(": is the sentence supported by the quote?"), "llm", SKIPPED, narrative.REASONS["JUDGE_UNAVAILABLE"], reason="JUDGE_UNAVAILABLE", rule="row 4", evidence=ev, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
    status = nar.get("status") or "pending"
    if rem:
        st.append(step("human", "Your decision on the paragraph", "human", SKIPPED, "This sentence was removed from the draft, so it cannot be accepted.", rule="D-031"))
        code, label = "removed", "Removed from the draft"
    elif status == "accepted":
        st.append(step("human", "Your decision on the paragraph", "human", PASS, "You accepted the paragraph.", rule="D-031", evidence={"action": "accept", "at": nar.get("reviewed_at")}))
        code, label = "accepted", "Accepted by you"
    elif status == "dismissed":
        st.append(step("human", "Your decision on the paragraph", "human", SKIPPED, "You dismissed the paragraph.", rule="D-031", evidence={"action": "dismiss", "at": nar.get("reviewed_at")}))
        code, label = "dismissed", "Dismissed by you"
    else:
        st.append(step("human", "Your decision on the paragraph", "human", PENDING, "The paragraph stays in the internal notes until you accept it.", reason="PENDING_DECISION", rule="D-031",
                       next_action=na("DECIDE", {"view": "narrative"}, ["accept", "dismiss"])))
        code, label = "ready_for_decision", "Ready for your decision"
    _number(st)
    return {"token": cx.case_id, "item_id": item_id, "kind": "narrative_sentence", "mode": "full" if cx.full else "metadata", "state": None,
            "review_status": {"accepted": "accepted", "dismissed": "dismissed"}.get(status, "pending") if not rem else None,
            "state_reasons": [{"code": c, "why": _ntext(c),
                               "step_id": "cites_accepted_entry" if c == "NOT_AN_ACCEPTED_ENTRY" else ("sentence_checks" if c in rcodes else "judge_1")}
                              for c in ([reason] if rem and not rcodes else rcodes)],
            "verdict": {"code": code, "label": label, "blocks_export": False}, "progress": _progress(st),
            "next_action": next((x["next_action"] for x in st if x["next_action"]), None), "steps": st}


# ------------------------------------------------------------------ public: item trace
@scoped
def item_trace(conn, case_id: str, item_id: str, full: bool = False) -> dict:
    """UnknownItem for an id that is not in the case. Entry, amount, flag or narrative sentence (ns...). Any other error is a bug and propagates."""
    cx = _Cx(conn, case_id, full)
    use_voice(cx.prep)
    if item_id.startswith("ns"):
        return _narrative_trace(cx, item_id)
    kind = present._ID_KIND.get(item_id[:1])
    try:
        if kind is None:
            raise KeyError(item_id)
        row = DB.get_item(conn, item_id, case_id)
    except KeyError:
        raise UnknownItem(item_id) from None
    use_voice(cx.prep or prepared_item(cx, row, kind))      # D-069: the item's wording follows its own first answer, or the case's
    steps = _STEPS_OF[kind](cx, row)
    return _finish(cx, item_id, kind, row, steps)


def _flag_steps(cx, row):
    """_flag_steps_core plus, when the model proposed other categories for this same quote, a code step that names them (T-126 r2: a merge is not silent)."""
    st = _flag_steps_core(cx, row)
    merged = ((row.get("ladder") or {}).get("code_checks") or {}).get("merged_categories")
    if merged:
        st.insert(0, step("proposals_merged", "Same quote proposed more than once", "code", PASS,
                          pick("The AI", "A prepared answer") + " proposed this quote under more than one category (" + ", ".join(m.replace("_", " ") for m in merged) + " as well as " + row["category"].replace("_", " ")
                          + "); code kept one flag.", rule="row 11", evidence={"values": {"merged_categories": merged}}))
    return st


_STEPS_OF.update({"entry": _entry_steps, "amount": _amount_steps, "flag": _flag_steps})


# ------------------------------------------------------------------ judge report
def _judge_rows(cx):
    """[{item_id, kind, judge, verdict(ladder vocab), reason_code, row, jd}] for every item with a judge answer (or a recorded 'unavailable')."""
    out = []
    for kind in ("entry", "amount", "flag"):
        for row in DB.list_items(cx.conn, cx.case_id, kind):
            if kind == "flag" and FT.is_filtered(row.get("state_reasons")):      # D-057: never judged, never counted
                continue
            jd = (row.get("ladder") or {}).get("judge")
            if not jd or not jd.get("verdict"):
                out.extend(_judge_never_ran(cx, kind, row))
                continue
            jid = judge_of_prompt(jd.get("prompt_version")) or {"entry": "j1", "amount": "j2", "flag": "j4"}[kind]
            if _paralegal_wording(kind, row) and _norm_verdict(jid, jd["verdict"]) == "unavailable":
                continue                                        # T-134 r2 (D-045b): the edit route's re-check had no answer; her own wording needs none, so it is not a missing check
            call = cx.call(jd.get("call_id"), row["id"], jid)
            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": _norm_verdict(jid, jd["verdict"]),
                        "reason_code": _judge_reason_code(jd, call), "row": row, "jd": jd, "call": call})
    return out


def _judge_never_ran(cx, kind, row):
    """An item whose own trace says its judge step was skipped as unavailable (no stored verdict, run finished) counts as 'unavailable'.
    Decided from the item's steps so /judges can never disagree with the item traces (a gate never passes over a check that did not run)."""
    if not cx.ran or _paralegal_wording(kind, row):
        return []                                               # D-045(b): wording the paralegal wrote is not AI-made, so it has no second check to miss
    out = []
    for s in _STEPS_OF[kind](cx, row):
        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
                and (s.get("evidence") or {}).get("judge_verdict") == "unavailable":
            jid = "j" + s["id"].split("_")[1]
            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": "unavailable", "reason_code": None, "row": row, "jd": {}, "call": None})
    return out


def _paralegal_wording(kind, row) -> bool:
    """A manual entry or an entry whose summary the paralegal edited: human-authored (same rule as present.ai_drafted), exempt from the judge but still code-checked (D-034)."""
    return (kind == "entry" and bool((row.get("ladder") or {}).get("entered_by") or "summary" in (row.get("edited") or {}))
            or kind == "amount" and bool((row.get("ladder") or {}).get("counted")))          # D-064: a charge she counted with a named confirm is her decision, not an AI claim


def ai_summary_unchecked(kind, row) -> bool:
    """T-134 r3 (T-136 F-2): an open edit that left the AI's summary in place (a re-picked quote) and whose second check has no answer. Accepting it alone cannot clear D-044's
    block, so the words say so. A summary the paralegal wrote is exempt (D-045b)."""
    return (kind == "entry" and review.edit_unconfirmed(kind, row) and not _paralegal_wording(kind, row)
            and ((row.get("ladder") or {}).get("judge") or {}).get("verdict") in (None, "", "unavailable"))


def rerun_gave_no_answer(row) -> bool:
    """The last rerun of the second check (ladder.rejudge) came back unavailable."""
    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
    return bool(last) and last.get("verdict") == "unavailable"


def judge_not_run_message(n: int, retried: bool = False, prep=None) -> str:
    """The one sentence for n accepted AI-made items whose second check has no answer: the 422 `judge_not_run` message and the export-gate headline (T-134 r4).
    `prep` (D-069): the case's provenance; omitted, the voice of the trace being built."""
    s = f"{n} accepted item{'s have' if n != 1 else ' has'} not had the second {'' if (_PREP.get() if prep is None else prep) else 'AI '}check"
    if retried:       # the check was run again on the current wording and quote and gave no answer: say what clears it, not the action that was just tried
        return (f"{s}: it ran again and gave no answer, so the export is blocked. It clears when the check answers, or when you edit the summary in your own words.")
    return f"{s}, so the export is blocked. Run the second check again."


@scoped
def unjudged_items(conn, case_id: str) -> list:
    """Live (not rejected, not dismissed) AI-made entries, charges and flags whose second check never gave an answer (D-044).
    [{item_id, kind, judge, review_status, row}]. An entry whose wording the paralegal wrote (manual entry, edited summary) is not AI-made and is never listed. Nothing is listed before the run has started."""
    cx = _Cx(conn, case_id, False)
    use_voice(cx.prep)
    out = []
    for r in _judge_rows(cx):
        row = r["row"]
        if r["verdict"] != "unavailable" or row["state"] == "rejected" or row["review_status"] == "dismissed":
            continue
        if _paralegal_wording(r["kind"], row):
            continue                                            # the paralegal wrote this wording (manual entry or edited summary): not AI-made
        out.append({"item_id": r["item_id"], "kind": r["kind"], "judge": r["judge"], "review_status": row["review_status"], "row": row})
    return out


def acknowledge_only(kind: str, row: dict) -> bool:
    """T-114 (D-019/D-042): a figure classified `rate` is never a letter charge, so accepting it only acknowledges it (it is listed in the internal notes, never totaled).
    No second AI check is needed for that, so a missing one never blocks export. The one source for the amount view's `accept_effect` and the gate."""
    return kind == "amount" and row.get("kind") == "rate"


@scoped
def judge_not_run_blockers(conn, case_id: str) -> list:
    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one.
    A rate (`acknowledge_only`) is the one exception: accepting it only acknowledges it, nothing of it reaches the letter (T-114)."""
    use_voice(present.models_for(conn, case_id, {"generator": "", "judge": ""})["generator_prepared"])
    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id)
            if u["review_status"] in ("accepted", "edited") and not acknowledge_only(u["kind"], u["row"])
            and not review.edit_unconfirmed(u["kind"], u["row"])]          # T-134: an edit not yet accepted is not in the letter, so it blocks nothing


def _jnr_blocker(u):
    tried = rerun_gave_no_answer(u["row"])           # T-134 r3: the reason must match what happened after the action offered
    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": reason_text("JUDGE_NOT_RUN_RETRIED" if tried else "JUDGE_NOT_RUN"),
            "rerun_no_answer": tried, "prepared": _PREP.get(), "next_action": na("RERUN_JUDGE", {"item_id": u["item_id"], "judge": u["judge"]})}


@scoped
def judge_report(conn, case_id: str, full: bool = False) -> dict:
    cx = _Cx(conn, case_id, full)
    use_voice(cx.prep)
    rows = _judge_rows(cx)
    per = {j: {"id": j, "label": JUDGE_LABEL[j], "prompt_version": JUDGE_PROMPT[j], "models": set(), "items": 0, "supported": 0, "partially": 0, "unsupported": 0,
               "disagrees": 0, "unsure": 0, "unavailable": 0} for j in ("j1", "j2", "j3", "j4")}
    rejections, unresolved, disagreements, versions = [], [], [], set()
    overrides = 0
    for r in rows:
        p = per[r["judge"]]
        v = r["verdict"]
        p["items"] += 1
        p[v] += 1
        model = (r["call"] or {}).get("model") or r["jd"].get("model") or cx.models["judge"]
        pv = r["jd"].get("prompt_version") or (r["call"] or {}).get("prompt_version") or JUDGE_PROMPT[r["judge"]]
        p["models"].add(model)
        p["prompt_version"] = pv
        versions.add(pv)
        row = r["row"]
        base = {"item_id": r["item_id"], "kind": r["kind"], "judge": r["judge"], "verdict": v, "model": model, "prompt_version": pv,
                "call_id": r["jd"].get("call_id") or (r["call"] or {}).get("id"), "review_status": row["review_status"]}
        R = set(row.get("state_reasons") or [])
        if v in ("partially", "unsupported", "disagrees"):
            e = dict(base, reason_code=r["reason_code"], rationale=why.judge_detail(r["reason_code"]) or reason_text(_OBJECTION[v]), state_reason=_OBJECTION[v])
            if full and r["call"]:
                e["response_raw"] = r["call"].get("response_raw")
            rejections.append(e)
            if row["review_status"] in ("accepted", "edited") and not review.edit_unconfirmed(r["kind"], row):      # T-134 r3: an open edit is not an accept; "accepted despite an objection" needs her explicit accept
                overrides += 1
            if r["kind"] == "amount":
                says = (r["reason_code"] or "").replace("SHOULD_BE_", "").lower()
                disagreements.append({"item_id": r["item_id"], "kind": "amount", "type": "judge_objects", "code_says": row["kind"],
                                      "judge_says": f"{says} ({r['reason_code']})" if says and r["reason_code"] != "NONE" else "not a " + row["kind"],
                                      "resolution": "needs_review", "review_status": row["review_status"]})
            elif not (R & _CODE_CHECK_REASONS):
                disagreements.append({"item_id": r["item_id"], "kind": r["kind"], "type": "judge_objects", "code_says": "All code checks passed.",
                                      "judge_says": rationale_or(r["reason_code"], v), "resolution": "needs_review", "review_status": row["review_status"]})
        elif v in ("unsure", "unavailable"):
            unresolved.append(dict(base, state_reason="JUDGE_UNSURE" if v == "unsure" else ("FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"),
                                   **({"reason_code": r["reason_code"]} if v == "unsure" else {})))
        elif R & _CODE_CHECK_REASONS:            # judge supported but a code check raised a doubt
            disagreements.append({"item_id": r["item_id"], "kind": r["kind"], "type": "judge_agrees_code_flags",
                                  "code_says": " ".join(reason_text(c) for c in sorted(R & _CODE_CHECK_REASONS)), "judge_says": _J_OK[r["judge"]],
                                  "resolution": "needs_review", "review_status": row["review_status"]})
    for row in DB.list_items(conn, case_id, "flag"):
        R = set(row.get("state_reasons") or [])
        for c in ("LEXICON_ONLY", "LLM_ONLY"):
            if c in R:
                disagreements.append({"item_id": row["id"], "kind": "flag", "type": "sources_disagree",
                                      "code_says": "The phrase list found it." if c == "LEXICON_ONLY" else "The phrase list did not find it.",
                                      "judge_says": ((("The prepared answers did not include it." if c == "LEXICON_ONLY" else "The prepared answers included it.") if prepared_item(cx, row, "flag") or cx.prep
                                                     else ("The AI did not find it." if c == "LEXICON_ONLY" else "The AI found it."))),
                                      "resolution": "needs_review", "review_status": row["review_status"]})
    j = lambda *ks: sum(sum(p[k] for p in per.values()) for k in ks)      # noqa: E731
    judges_out = [dict(p, models=sorted(p["models"])) for p in per.values()]
    for p in judges_out:
        if not p["items"]:
            p["models"] = []
    answered = j("supported", "partially", "unsupported", "disagrees", "unsure")
    return {"token": case_id, "mode": "full" if cx.full else "metadata", "models": cx.models, "independent_models": cx.models["generator"] != cx.models["judge"],
            "totals": {"items_judged": answered, "supported": j("supported"), "unsupported": j("partially", "unsupported", "disagrees"), "unsure": j("unsure"),
                       "unavailable": j("unavailable"), "human_overrides": overrides},
            "judges": judges_out, "rejections": rejections, "unresolved": unresolved, "disagreements": disagreements, "prompt_versions": sorted(versions)}


def rationale_or(code, verdict):
    return why.judge_detail(code) or reason_text(_OBJECTION[verdict])


# ------------------------------------------------------------------ case trace
def _count_by(items, key):
    out = {}
    for i in items:
        out[i[key]] = out.get(i[key], 0) + 1
    return out


@scoped
def case_trace(conn, case_id: str, full: bool = False) -> dict:
    cx = _Cx(conn, case_id, full)
    use_voice(cx.prep)
    case = cx.case
    recs = list(cx.recs.values())
    ents = DB.list_items(conn, case_id, "entry")
    handled = generator.resolved_placeholders(ents)
    failed_ents = [x for x in ents if (x.get("ladder") or {}).get("failure") and x["id"] not in handled]       # tray placeholders for records the extract step made no output for (not drafted items: nothing to ground or judge)
    ents = [x for x in ents if not (x.get("ladder") or {}).get("failure")]      # (a hand-entered record's placeholder is dropped here too)
    amts = DB.list_items(conn, case_id, "amount")
    flgs = [x for x in DB.list_items(conn, case_id, "flag") if not FT.is_filtered(x.get("state_reasons"))]      # D-057: rule-filtered proposals are listed in the payload, not checked or counted here
    allitems = [("entry", x) for x in ents] + [("amount", x) for x in amts] + [("flag", x) for x in flgs]
    cfg = case.get("config") or {}
    rv = present.review_view(conn, case_id)
    jr = judge_report(conn, case_id, full)
    st = []
    # 1 ingest
    dup = sum(1 for r in recs if r["duplicate_of"])
    st.append(step("ingest", "Read the paste and split it into records", "code", PASS if recs else FAIL,
                   f"{len(recs)} records found." + (f" {dup} exact duplicate{'s' if dup != 1 else ''} merged into the record they repeat." if dup else ""), rule="row 1",
                   counts={"records": len(recs), "duplicates_merged": dup, "characters": len(case["raw_text"])}))
    # 2 split
    llm_split = any(f["category"] == "llm_split" for f in flgs)
    sf = cfg.get("split_failure")
    if sf:
        st.append(step("split", "Record boundaries", "code", FAIL, reason_text("SPLIT_AMBIGUOUS"), reason="SPLIT_AMBIGUOUS", rule="row 1", evidence={"values": {"failure": sf}},
                       counts={"method": "code", "llm_split": False}, next_action=na("READ_RECORD", {"view": "records"})))
    elif llm_split:
        st.append(step("split", "Record boundaries", "llm", FAIL, reason_text("LLM_SPLIT"), reason="LLM_SPLIT", rule="row 1", counts={"method": "llm", "llm_split": True},
                       next_action=na("READ_RECORD", {"view": "records"})))
    else:
        st.append(step("split", "Record boundaries", "code", PASS, "The record markers in the paste decided where each record starts and ends.", rule="row 1",
                       counts={"method": "code", "llm_split": False}))
    # 3 dates
    dc = _count_by([{"s": r["date_status"]} for r in recs], "s")
    bad = dc.get("ambiguous", 0) + dc.get("missing", 0)
    dcounts = {k: dc.get(k, 0) for k in ("parsed", "confirmed", "ambiguous", "missing")}
    if bad:
        code = "DATE_AMBIGUOUS" if dc.get("ambiguous") else "DATE_MISSING"
        st.append(step("dates", "Dates read by code", "code", FAIL, f"{bad} record date{'s are' if bad != 1 else ' is'} not confirmed. " + reason_text(code), reason=code, rule="row 2",
                       counts=dcounts, next_action=na("CONFIRM_DATE", {"view": "dates_to_confirm"})))
    else:
        st.append(step("dates", "Dates read by code", "code", PASS, "Every record date was read by code and is parsed or confirmed.", rule="row 2", counts=dcounts))
    # 4 extract
    firsts = [r for r in recs if not r["duplicate_of"]]
    have = {(e["record_ids"] or [None])[0] for e in ents}
    missing = [r["id"] for r in firsts if r["id"] not in have]
    ecounts = {"records_to_draft": len(firsts), "entries": len(ents), "rejected": sum(1 for e in ents if e["state"] == "rejected"), "records_without_entry": len(missing),
               **({"in_tray": len(failed_ents)} if failed_ents else {})}
    prep = bool(cx.models.get("generator_prepared"))      # T-177 r2 / D-065: the case's answers are hand-checked fixtures, so the step must not say an AI drafted them
    xlabel = CASE_PREPARED_LABEL if prep else "AI drafts a summary and a quote for each record"
    xev = {"evidence": {"model": {"id": present.PREPARED_MODEL, "role": "generator", "independent_of_generator": None, "prepared": True}}} if prep else {}
    if not cx.ran:
        st.append(step("extract", xlabel, "llm", PENDING, "The prepared answers have not been loaded yet." if prep else "The AI run has not started.", rule="row 4", counts=ecounts, next_action=na("RERUN"), **xev))
    elif missing:
        trimmed = {r for x in failed_ents if (x.get("ladder") or {}).get("failure") == "SUMMARY_NOT_IN_QUOTE" for r in (x["record_ids"] or [])}
        why_code = "SUMMARY_NOT_IN_QUOTE" if set(missing) <= trimmed else "LLM_FAILED_AFTER_RETRIES"      # D-054: say so when code removed the whole summary
        st.append(step("extract", xlabel, "llm", FAIL, f"{len(missing)} record{'s have' if len(missing) != 1 else ' has'} no {'prepared' if prep else 'AI-made'} entry. "
                       + reason_text(why_code), reason=why_code, rule="row 4", evidence=({"model": xev["evidence"]["model"], "values": {"record_ids": missing}} if prep else {"values": {"record_ids": missing}}), counts=ecounts,
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": missing[0]})))
    else:
        st.append(step("extract", xlabel, "llm", PASS, (f"The prepared answers (hand-checked by the team for the demo) cover all {len(firsts)} records." if prep else f"The AI drafted an entry for all {len(firsts)} records."), rule="row 4", counts=ecounts, **xev))
    # 5 grounding
    rej = [(k, x) for k, x in allitems if x["state"] == "rejected"]
    codes = {}
    for _, x in rej:
        for c in x.get("state_reasons") or []:
            if c in ("GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"):
                codes[c] = codes.get(c, 0) + 1
    gcounts = {"items_checked": len(allitems), "rejected": len(rej), "reasons": codes}
    if rej:
        first = next(iter(codes), None)
        st.append(step("grounding", "Every quote and amount is in the record", "code", FAIL, f"{len(rej)} item{'s were' if len(rej) != 1 else ' was'} rejected because the quote or amount is not in the record. "
                       "They stay in the tray and out of the letter.", reason=first, rule="row 4", counts=gcounts,
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"view": "tray"})))
    elif not allitems:
        st.append(step("grounding", "Every quote and amount is in the record", "code", PENDING, "There is nothing to check yet.", rule="row 4", counts=gcounts, next_action=na("RERUN")))
    else:
        st.append(step("grounding", "Every quote and amount is in the record", "code", PASS, f"All {len(allitems)} items cite text that is in the record, character for character.", rule="row 4", counts=gcounts))
    # 6 judges
    jlabel = "Second check on every prepared item" if prep else "Second AI check on every AI-made item"      # T-177 r2: the items are the team's prepared answers
    t = jr["totals"]
    jcounts = dict(t)
    objections = t["unsupported"] + t["unsure"]
    if not rows_any(jr) and not cx.ran:
        st.append(step("judges", jlabel, "llm", PENDING, "The second check has not run yet.", rule="row 4", counts=jcounts, next_action=na("RERUN")))
    elif t["unavailable"]:
        msg = f"{t['unavailable']} item{'s have' if t['unavailable'] != 1 else ' has'} not been double-checked. "
        if cx.running:
            st.append(step("judges", jlabel, "llm", PENDING, msg + "The run is still going.", reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts))
        else:
            st.append(step("judges", jlabel, "llm", FAIL, msg + reason_text("JUDGE_UNAVAILABLE"),
                           reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts, next_action=na("RERUN_JUDGE", {"view": "judges"})))
    elif objections:
        st.append(step("judges", jlabel, "llm", FAIL, f"The second check questioned {objections} of {t['items_judged']} items; they are marked for review.",
                       reason="JUDGE_UNSUPPORTED" if t["unsupported"] else "JUDGE_UNSURE", rule="row 4", counts=jcounts, next_action=na("COMPARE_BY_HAND", {"view": "judges"})))
    else:
        st.append(step("judges", jlabel, "llm", PASS, f"The second check agreed with all {t['items_judged']} items it checked.", rule="row 4", counts=jcounts))
    # 7 flags
    fc = {"total": len(flgs), "by_type": _count_by(flgs, "type"), "by_origin": _count_by(flgs, "origin")}
    if any(f["category"] == "analysis_incomplete" for f in flgs):
        st.append(step("flags", "Gaps, conflicts and wording flags", "code", FAIL, reason_text("CONFLICT_CHECK_INCOMPLETE"), reason="CONFLICT_CHECK_INCOMPLETE", rule="row 11", counts=fc,
                       next_action=na("RERUN")))
    elif not cx.ran:
        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PENDING, pick("Gaps and date conflicts are ready (code). The AI and phrase-list pass has not run.", "Gaps and date conflicts are ready (code). The prepared-answer and phrase-list pass has not run."), rule="row 9", counts=fc,
                       next_action=na("RERUN")))
    else:
        st.append(step("flags", "Gaps, conflicts and wording flags", "code", PASS, f"{len(flgs)} flag{'s' if len(flgs) != 1 else ''}: dates compared by code, wording found by the phrase list and {pick('the AI', 'the prepared answers')}.", rule="row 9", counts=fc))
    # 8 totals
    tv = present.totals_view(conn, case_id)
    pend_ch = tv["pending"]["count"]
    tcounts = {"accepted_cents": tv["accepted"]["cents"], "accepted_count": tv["accepted"]["count"], "pending_cents": tv["pending"]["cents"], "pending_charges": pend_ch,
               "not_totaled": len(tv["not_totaled"])}
    if not amts:
        st.append(step("totals", "Billed-charges total", "code", SKIPPED, "No dollar amounts were found.", rule="row 8", counts=tcounts))
    elif pend_ch:
        st.append(step("totals", "Billed-charges total", "code", PENDING, f"{pend_ch} detected charge{'s' if pend_ch != 1 else ''} not in the total until you accept {'them' if pend_ch != 1 else 'it'}. The total is added up by code from accepted charges only.",
                       reason="PENDING_DECISION", rule="row 8", counts=tcounts, next_action=na("DECIDE", {"view": "amounts"}, ["accept", "dismiss"])))
    else:
        st.append(step("totals", "Billed-charges total", "code", PASS, "The total is added up by code from the accepted charges.", rule="row 8", counts=tcounts))
    # 9 review
    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed", "edit_to_check")}
    if rc["pending"]:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{rc['pending']} item{'s are' if rc['pending'] != 1 else ' is'} waiting for your decision.", reason="PENDING_DECISION",
                       rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    elif rc["edit_to_check"]:           # T-134: her reworded entry is still marked Needs review; it is not decided until she accepts it
        n = rc["edit_to_check"]
        n_ai0 = sum(1 for k, x in allitems if ai_summary_unchecked(k, x))
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm "
                       f"{'them' if n != 1 else 'it'}). " + (ai_clause(n_ai0, n) if n_ai0 else f"Compare {'them' if n != 1 else 'it'} with the quote and accept, or the {'entries stay' if n != 1 else 'entry stays'} out of the letter."),
                       reason="EDIT_NOT_CONFIRMED", rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    else:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
    # 10 export gate
    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
    ccf = [b for b in blockers if b.get("step_id")]             # D-045(b): the paralegal's own wording fails a code check
    mil = [b for b in blockers if b["reason_code"] == "MONEY_IN_LETTER"]     # T-139 r4: a line of the final letter states an amount
    live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
    n_ai = sum(1 for k, x in allitems if ai_summary_unchecked(k, x))
    n_edit = rv["counts"].get("edit_to_check", 0)                # T-134: reworded, still Needs review, not accepted: not in the letter, so it warns like a pending item
    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
    ready = not blockers
    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"] - n_edit, "edit_not_confirmed": n_edit,
                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf), "money_in_letter": len(mil)}
    warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
                 "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])}] if n_pend else []
    if n_edit:
        warnings.append({"reason_code": "EDIT_NOT_CONFIRMED", "count": n_edit, "why": edit_warning(n_edit, n_ai), "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])})
    if ready:
        gate = step("export_gate", "Ready to export?", "code", PASS,
                    "At least one item is accepted and every accepted item has its checks, so the export can be built." + (" " + pending_warning(n_pend) if n_pend else "")
                    + (" " + edit_warning(n_edit, n_ai) if n_edit else ""),
                    rule="row 19", counts=gate_counts)
    else:
        first = blockers[0]
        text = (judge_not_run_message(len(jnr), all(b.get("rerun_no_answer") for b in jnr)) if jnr and first is jnr[0] else first["why"])
        gate = step("export_gate", "Ready to export?", "code", FAIL, text, reason=first["reason_code"], rule="row 19", counts=gate_counts, next_action=first["next_action"],
                    blocks=True)
    gate.update(ready=ready, blockers=blockers, warnings=warnings)
    st.append(gate)
    _number(st)
    verdict = ({"code": "running", "label": pick("The AI run is in progress", "The run is in progress")} if cx.running else {"code": "failed", "label": "The last run stopped"} if case["status"] == "failed"
               else {"code": "ready", "label": "Ready to export" + (f" ({n_pend + n_edit} not reviewed)" if n_pend + n_edit else "")} if ready
               else {"code": "needs_attention", "label": f"{len(ccf)} summar{'ies fail' if len(ccf) != 1 else 'y fails'} a check" if ccf and not jnr
                      else f"{len(jnr)} accepted item{'s' if len(jnr) != 1 else ''} not double-checked" if jnr
                      else f"{len(mil)} line{'s' if len(mil) != 1 else ''} of the letter state{'' if len(mil) != 1 else 's'} an amount" if mil else "Nothing is accepted yet"})
    return {"token": case_id, "mode": "full" if cx.full else "metadata", "status": case["status"], "verdict": verdict, "progress": _progress(st), "steps": st}


def pending_warning(n: int) -> str:
    return f"{n} item{'s are' if n != 1 else ' is'} not reviewed, so {'they' if n != 1 else 'it'} will not be in the letter; the {pick('AI ', '')}disclosure line will count {'them' if n != 1 else 'it'}."


def ai_clause(n_ai: int, n: int) -> str:
    """T-134 r4 (D-058): for open edits that keep the AI's summary with no second-check answer. Conditional, because before she accepts nothing is blocked (the gate passes and the
    entry is only left out); accept alone cannot clear D-044's block."""
    them = "them" if n_ai != 1 else "it"
    who = "It keeps" if n == n_ai == 1 else "They keep" if n == n_ai else f"{n_ai} of them keep" if n_ai != 1 else "1 of them keeps"
    return (f"{who} {pick("the AI's", "the prepared")} summary and the second check has no answer on the new quote, so accepting alone will not put {them} in the letter. "
            f"If you accept {them}, the export will be blocked until the second check answers (Run the second check again) or you edit the summary in your own words.")


def edit_warning(n: int, n_ai: int = 0) -> str:
    return edit_warning_base(n) + (" " + ai_clause(n_ai, n) if n_ai else "")


def edit_warning_base(n: int) -> str:
    return (f"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm {'them' if n != 1 else 'it'}), so {'they are' if n != 1 else 'it is'} "
            f"not in the letter and {'are' if n != 1 else 'is'} not counted as accepted until you compare {'them' if n != 1 else 'it'} with the quote and accept.")


def letter_money_blockers(conn, case_id: str, case=None) -> list:
    """MONEY_IN_LETTER blockers (T-139 r4, D-019, R-CH-7): the one money detector run on the final letter text, so the gate never reads ready while GET /export answers 422.
    `case` is the export case dict without blockers (store.export_case(blockers=False)) when the caller already has it."""
    from app.backend import export
    return export.money_blockers_for_case(case if case is not None else store.export_case(conn, case_id, blockers=False))


@scoped
def export_blockers(conn, case_id: str, cx=None, rv=None, case=None) -> list:
    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
    cx = cx or _Cx(conn, case_id, False)
    use_voice(cx.prep)
    rv = rv or present.review_view(conn, case_id)
    out = []
    if cx.running:
        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": reason_text("RUN_IN_PROGRESS"), "next_action": None})
    if cx.case["status"] == "failed":
        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": reason_text("RUN_FAILED"), "next_action": na("CONFIRM_RERUN")})
    out.extend(code_check_blockers(conn, case_id, cx))         # D-045(b): the paralegal's own wording is exempt from the judge, not from the code checks
    if rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0) > 0:
        out.extend(letter_money_blockers(conn, case_id, case))    # T-139 r4: money anywhere in the final letter text outside the Billed charges section; the same list GET /export refuses on
    if cx.ran and not cx.running:
        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
    if not (rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0)):       # T-134: an edit not yet accepted is not accepted
        out.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": reason_text("NOTHING_ACCEPTED"), "next_action": na("DECIDE", {"view": "queue"})})
    return out


def rows_any(jr):
    return bool(jr["totals"]["items_judged"] or jr["totals"]["unavailable"])
