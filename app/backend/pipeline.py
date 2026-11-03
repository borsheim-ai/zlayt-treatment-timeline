"""Pipeline stages 0-7 (app/README-arch.md; ADR-007, ADR-010, ADR-011, ADR-013, ADR-014). `python -m app.pipeline <file>` prints the result.

0 ingest (code, sync)  1 extract (LLM)  2 verify (code)  3 judge_entries (J1)  4 amounts (J2 on every amount)
5 conflicts (code proposes the pairs, J3 classifies each)  6 flags (one LLM pass per record + lexicon floor + J4)  7 finalize (code).
Gaps, the accident-date conflict, provider-name conflicts, amounts and record warnings exist after stage 0 and never wait for a model.
No code path here sets review_status: every item leaves a run `pending`. A model failure loses only that item and is reported in `errors`.
`call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is the audited wrapper bound to a case (or a test fake)."""
import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from app.backend import (amounts as AM, confidence, conflict_candidates as CC, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
                         judges, language, split_llm, totals as TT, why as WHY)
from app.db import db as DB
from app.llm import audited as AU, provider as P

STAGES = ("ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize")
DEADLINE_S = 480
CONCURRENCY = 3
_ORIGIN = {"both": "lexicon+llm"}


def _clean(d: dict) -> dict:
    """Drop private '_' keys before an item is stored or returned."""
    return {k: v for k, v in d.items() if not k.startswith("_")}


def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
            "human": {"action": None, "edited_text": None, "at": None}, "state": state}


def _compose_code(rec_by_n: dict, nos: list, reasons: list, evidence: list, case_text: str) -> tuple:
    """State of a flag made by code: evidence spans must equal the input text; injection / unconfirmed endpoints give needs_review."""
    bad = [e for e in evidence if e.get("start") is not None and case_text[e["start"]:e["end"]] != e["text"]]
    ctx = {"injection": any(rec_by_n[n].get("injection_tag") for n in nos if n in rec_by_n),
           "endpoint_unverified": "ENDPOINT_NOT_VERIFIED" in reasons,
           "translated": any(language.translated_record(rec_by_n[n]) for n in nos if n in rec_by_n)}      # D-050
    dates = {rec_by_n[n].get("date_status") for n in nos if n in rec_by_n}
    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
        ctx["date_status"] = "ambiguous"
    return confidence.compose_state({"grounding_failures": ["GROUNDING_EXCERPT_NOT_VERBATIM"] if bad else [], "schema_valid": True,
                                     "code_reasons": []}, ctx)


# ------------------------------------------------------------------ stage 0
def run_ingest(raw_text: str, call=None, not_duplicates=(), splitter=None) -> dict:
    """Stage 0. Raises IngestError('bad_request' | 'input_too_large') before anything else. Zero model calls, except the D-031 split
    fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
    ing = IN.ingest(raw_text, splitter=splitter or (split_llm.make_splitter(call) if call else None), not_duplicates=not_duplicates, prep=AU.answers_prepared())      # D-069
    text = IN.normalize_text(raw_text)
    recs = language.annotate(ing["records"])           # D-042: en | es | other per record; raises UnsupportedLanguage when no record is readable
    language.case_check(recs)
    by_n = {r["n"]: r for r in recs}
    backend = P.backend_name()
    flags = []
    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
    for f in code:
        nos = f["record_nos"]
        ev = f["evidence"]
        reasons = list(f.get("reasons") or [])
        state, why_codes = _compose_code(by_n, nos, reasons, ev, text)
        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": ev, "record_nos": nos,
                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "review_status": "pending",
                "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes) or
                "Computed by code from the record dates and text; every cited span matches the input."}
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names", "endpoint_warnings", "conditional"):
            if k in f:
                item[k] = f[k]
        item["ladder"] = _ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
        flags.append(item)
    for w in ing["record_warnings"]:
        r = by_n[w["record_no"]]
        inj = w["category"] == "injection_suspected"
        ctx = {"llm_split": True} if w["category"] == "llm_split" else {"injection": inj, "date_status": None if inj else "ambiguous"}
        ctx["translated"] = language.translated_record(r)      # D-050
        state, why_codes = confidence.compose_state({"code_reasons": []}, ctx)
        flags.append({"id": w["id"], "type": "record_warning", "category": w["category"], "origin": "code", "title": w["title"],
                      "explanation": w["explanation"], "evidence": [{"record_no": w["record_no"], **e} for e in w["evidence"]],
                      "record_nos": [w["record_no"]], "record_ids": [r["id"]], "source_kind": "record", "review_status": "pending",
                      "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes),
                      "ladder": _ladder(w["id"], backend, {"computed_by": "code"}, state)})
        if w["category"] == "llm_split":      # trace the flag to the audited split call (prompt version, model, call id)
            flags[-1]["ladder"]["generator"] = {"model": judges.generator_model(), "prompt_version": "split_v1", "call_id": w.get("call_id")}
    amounts, damages = [], []
    sep = {int(str(i)[1:]) for i in not_duplicates if str(i)[1:].isdigit()}
    for a in AM.extract_amounts(recs, separate=sep):
        item = amount_item(a, by_n[a["record_no"]])
        (damages if a["cls"] == "damages" else amounts).append(item)
    warnings = list(ing["warnings"]) + language.record_warnings(recs, AU.answers_prepared())
    for r in recs:
        if r["injection_tag"]:
            warnings.append({"code": "INJECTION_SUSPECTED", "record_no": r["n"], "item_id": r["id"],
                             "message": "This record contains instruction-like text; it is shown unchanged and everything from it needs review."})
    return {"text": text, "records": recs, "groups": ing["groups"], "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "split_detail": ing.get("split_detail"), "banner": ing["banner"],
            "dates_to_confirm": ing["dates_to_confirm"], "flags": flags, "amounts": amounts, "damages": damages, "warnings": warnings,
            "injection_records": ing["injection_records"]}


def amount_item(a: dict, r: dict, item_id: str = None) -> dict:
    """The pipeline's amount item from an amounts.extract_amounts row and its record."""
    return {"id": item_id or a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
            "cents": a["cents"], "value_cents": a["cents"], "cls": a["cls"], "kind": a["cls"], "start": a["start"], "end": a["end"],
            "excerpt": r["excerpt"], "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending",
            "confirm": a.get("confirm")}


def _not_duplicates(conn, cid: str) -> list:
    return list(((DB.get_case(conn, cid) or {}).get("config") or {}).get("not_duplicates", []))


def _frozen_splitter(conn, cid: str):
    """D-039: once any entry, amount or flag of the case is accepted, edited or dismissed, the stored records are frozen. Returns None
    while everything is still pending (the model may re-split). Otherwise returns a splitter that replays the stored record spans with
    no model call, so decided items keep their record ids and excerpts; with fewer than two stored records it answers None (nothing to
    replay; the code split decides, which is deterministic and equals what is stored)."""
    if not any(i["review_status"] != "pending" for k in ("entry", "amount", "flag") for i in DB.list_items(conn, cid, k)):
        return None
    starts = [r[0] for r in conn.execute("SELECT char_start FROM records WHERE case_id=? ORDER BY seq", (cid,))]
    split_call = next((c["id"] for c in reversed(DB.list_llm_calls(conn, cid, "split")) if c.get("parsed_ok")), None)

    reason = ((DB.get_case(conn, cid) or {}).get("config") or {}).get("split_failure")

    def replay(text: str):             # stored spans are trimmed; the split contract is contiguous starts that cover the text
        if len(starts) <= 1 and reason:
            raise IN.SplitFailed(reason, replayed=True)
        cuts = [0] + starts[1:] + [len(text)]
        return (list(zip(cuts, cuts[1:])), split_call) if len(starts) > 1 else None
    return replay


def _store_split_failure(conn, cid: str, reason) -> None:
    """Keep the split-rejection reason in the case config so a later re-run that replays frozen records can show it again (D-039)."""
    cfg = dict((DB.get_case(conn, cid) or {}).get("config") or {})
    if cfg.get("split_failure") == reason:
        return
    if reason:
        cfg["split_failure"] = reason
    else:
        cfg.pop("split_failure", None)
    DB.update_case(conn, cid, config_json=cfg or None)


def _store_record_marks(conn, cid: str, ing: dict) -> None:
    """T-129: which stored records are unsplit text (D-027) and which of those is a preamble, kept in the case config so GET case serves them (record_view)."""
    marks = {"unsplit_records": [r["id"] for r in ing["records"] if r.get("unsplit")], "preamble_records": [r["id"] for r in ing["records"] if r.get("preamble")]}
    cfg = dict((DB.get_case(conn, cid) or {}).get("config") or {})
    if all(cfg.get(k, []) == v for k, v in marks.items()):
        return
    for k, v in marks.items():
        if v:
            cfg[k] = v
        else:
            cfg.pop(k, None)
    DB.update_case(conn, cid, config_json=cfg or None)


def _store_run_checks(conn, cid: str, recs: list, stage: str) -> None:
    """T-141 r2: what the conflict checks did on THIS case (language routing, whether the pair stage ran), kept in the case config so GET case `checks`
    is computed from the run, not a constant. stage: 'pending' (ingested, or the run has started), 'ran', 'skipped' (deadline before the stage)."""
    cfg = dict((DB.get_case(conn, cid) or {}).get("config") or {})
    cfg["run_checks"] = CC.run_summary(recs, stage=stage)
    DB.update_case(conn, cid, config_json=cfg)


def _item_record_ids(item: dict) -> list:
    return list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])


def _reset_reviewed_on(conn, cid: str, moved: set, now: float) -> None:
    """T-129 r2: a record number now names different text (a re-run after the numbering changed, or a model split that moved). A decision the paralegal made on an item
    that cites such a record was made on other text, so it goes back to pending (the review event keeps what it was); the run then rebuilds or removes the item."""
    if not moved:
        return
    for kind in ("entry", "amount", "flag"):
        for it in DB.list_items(conn, cid, kind):
            if it["review_status"] != "pending" and moved & set(_item_record_ids(it)):
                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)


def _store_records(conn, cid: str, ing: dict, now: float = 0.0) -> None:
    """Make the stored records equal this run's records. Same ids and spans -> nothing to do. Anything else (a model split that moved,
    or a re-run whose split failed or was rejected and so fell back to the code split) -> delete and re-store in the same transaction,
    before any entry, flag or amount of this run is written, so the records table and the run's items never disagree."""
    _store_record_marks(conn, cid, ing)
    stored = [(r[0], r[1], r[2]) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
    if stored == [(r["id"], r["char_start"], r["char_end"]) for r in ing["records"]]:
        return
    new_spans = {r["id"]: (r["char_start"], r["char_end"]) for r in ing["records"]}
    _reset_reviewed_on(conn, cid, {i for i, a, b in stored if new_spans.get(i) != (a, b)}, now)
    conn.execute("BEGIN")                      # autocommit connection: one explicit transaction, all or nothing
    try:
        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
        for r in ing["records"]:
            d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
            DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
                          date_header_start=d["start"], date_header_end=d["end"], source_header_start=s["start"], source_header_end=s["end"],
                          source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
                          date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
                          encounter=int(r["encounter"]))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _row(kind: str, it: dict) -> dict:
    ladder = _clean(it.get("ladder") or {})
    if kind == "entry":
        return {"record_ids_json": it["record_ids"], "seq": it["seq"], "date_iso": it.get("date"), "provider": it["provider"],
                "summary": it.get("summary"), "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"),
                "excerpt_end": it.get("excerpt_end"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
    if kind == "amount":
        return {"record_ids_json": it["record_ids"], "entry_id": it.get("entry_id"), "text": it["text"], "value_cents": it["cents"],
                "kind": it["cls"], "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"), "excerpt_end": it.get("excerpt_end"),
                "duplicate_note": it.get("duplicate_note"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids", "endpoint_warnings", "conditional") if k in it}
    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
            "explanation": it["explanation"], "computed_json": computed, "evidence_json": it.get("evidence", []),
            "origin": _ORIGIN.get(it["origin"], it["origin"]), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}


JUDGE_NOT_RUN = "JUDGE_NOT_RUN"


def _mark_judge_not_run(entries: list, by_n: dict) -> None:
    """T-145: an AI entry that has no judge-1 answer (the run hit its deadline before or during the stage) is recorded as judge `unavailable` with reason_code
    JUDGE_NOT_RUN and recomposed, so it is `needs_review` (JUDGE_UNAVAILABLE, whose sentence names JUDGE_NOT_RUN), never `verified`, and batch accept (state == verified) refuses it.
    Missing is not a pass: compose treats a judge of None as 'nothing to doubt', so the absence is made explicit here."""
    for e in entries:
        if e["state"] == "rejected" or (e["ladder"].get("judge") or {}).get("verdict"):
            continue
        e["ladder"]["judge"] = {"model": None, "prompt_version": None, "call_id": None, "verdict": "unavailable", "reason_code": JUDGE_NOT_RUN}
        generator.compose(e, by_n[e["seq"]], judge="unavailable")


_STUB_REASONS = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"}      # an entry rejected for one of these has no output at all: a stub
_FLAG_FAIL = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS"}      # a flag made while the flag step failed carries one of these (it is the lexicon floor, nothing the model checked)
_RANK = {"verified": 0, "needs_review": 1, "rejected": 2}
_EXTRACT_STEP = "writing the entries"


def _failure(kind: str, it: dict):
    """T-146 r3: what failed in the NEW row `it` alone, as the step's name, or None: an entry that is a failure stub (the AI step gave nothing), a flag made while the flag
    step failed, or an item whose second check was asked and gave no answer."""
    if kind == "entry" and it.get("state") == "rejected" and set(it.get("reasons") or []) & _STUB_REASONS:
        return _EXTRACT_STEP
    if kind == "flag" and set(it.get("reasons") or []) & _FLAG_FAIL:
        return "finding the flags"
    return "the second check" if ((it.get("ladder") or {}).get("judge") or {}).get("verdict") == "unavailable" else None


def _degrades(kind: str, old: dict, it: dict):
    """T-146 r2/r3: would storing `it` over the stored row `old` replace output with a failure, or take back a second-check answer? Returns the step's name or None.
    (entry) the AI step gave nothing where the stored row has a summary and a quote; (flag) the flag step failed and the stored row was not made from a failure;
    (any AI-made item) the second check gave no answer where the stored row had one. A failure is never allowed to erase earlier work."""
    cause = _failure(kind, it)
    if cause == _EXTRACT_STEP:
        return cause if old.get("summary") and old.get("excerpt") else None
    if cause == "finding the flags":
        return None if set(old.get("state_reasons") or []) & _FLAG_FAIL else cause
    return cause if ((old.get("ladder") or {}).get("judge") or {}).get("verdict") not in (None, "unavailable") else None


def _evidence_texts(row: dict) -> set:
    return {e.get("text") or e.get("excerpt") for e in (row.get("evidence") or [])}


_POSITIVE = {"agree", "supported", "conflict"}      # a second-check answer that backs the item (judge 1 supported, 2 and 4 agree, 3 conflict confirmed); anything else is not a backing answer


def _checks_worse(old: dict, it: dict) -> bool:
    """T-146 r4: did the whole ladder of checks get worse INSIDE the same state? (a) a reason code the stored row did not have; (b) the second-check answer moved from a
    backing one to anything else; (c) a code check that was true is now false, or the list of summary tokens the quote does not support went from empty to non-empty.
    Equal rank is not equal checks: the stored answer is the audit record the paralegal decided on."""
    if set(it.get("reasons") or []) - set(old.get("state_reasons") or []):
        return True
    ol, nl = old.get("ladder") or {}, it.get("ladder") or {}
    ov, nv = (ol.get("judge") or {}).get("verdict"), (nl.get("judge") or {}).get("verdict")
    if ov in _POSITIVE and nv is not None and nv not in _POSITIVE:
        return True
    oc, nc = ol.get("code_checks") or {}, nl.get("code_checks") or {}
    return any(v is True and nc.get(k) is False for k, v in oc.items()) or (not oc.get("summary_tokens_not_in_excerpt") and bool(nc.get("summary_tokens_not_in_excerpt")))


def _disagrees(kind: str, old: dict, it: dict) -> bool:
    """T-146 r3: does the NEW row `it` lower or change what the stored row `old` says? True when its state is worse (verified -> needs_review -> rejected) or its content
    differs (entry: summary, quote, date; amount: text, value, class; flag: type, category, evidence quotes), or its checks are worse inside the same state (`_checks_worse`: a new
    reason, a backing second-check answer turned negative, a code check turned false). A better state with the same content is not a disagreement.
    A stored row that is itself in the tray (rejected) has nothing to lower. A flag whose computed numbers changed is the existing reset path (the decision was about
    other numbers), so it is not judged here."""
    if _RANK.get(it["state"], 1) > _RANK.get(old["state"], 1) and old["state"] != "rejected":
        return True
    if old["state"] == "rejected":
        return False
    if kind == "flag":
        oc = old.get("computed") or {}
        if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
            return False
    if _checks_worse(old, it):
        return True
    if kind == "entry":
        return (old.get("summary"), old.get("excerpt"), old.get("date_iso")) != (it.get("summary"), it.get("excerpt"), it.get("date"))
    if kind == "amount":
        return (old.get("text"), old.get("value_cents"), old.get("kind")) != (it.get("text"), it.get("cents"), it.get("cls"))
    return (old.get("type"), old.get("category"), _evidence_texts(old)) != (it.get("type"), it.get("category"), {e.get("text") for e in it.get("evidence", [])})


def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bool = False, prune: bool = True, empty_ids: list = None) -> tuple:
    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed.
    `additive` (T-146, a run that stopped at its deadline): only items with no stored row are added. A stopped run is partial, so it must not delete, downgrade or
    overwrite what an earlier complete run stored (its judged states, its flags) or what the paralegal decided.
    One rule for every stage (T-146 r3): a re-run never lowers or replaces a decided item (accepted, dismissed, edited). When the new row fails (`_degrades`) or lowers
    or changes it (`_disagrees`), the stored row is kept as it is and `ladder.rerun_note` says so (shown on the item). A row that is not decided is kept the same way,
    without a note, when the new row is a failure over stored output (a stub, a flag made while the flag step failed, a lost second-check answer).
    Returns (kept, nothing_to_keep): `kept` is [(stored row, step, 'failed' | 'disagreed')]; `nothing_to_keep` is [(step)] for new rows that are failures with no stored
    output to fall back on. `prune=False`: the stale-pending delete is skipped (a failed flag step cannot tell which flags are stale).
    `empty_ids` (T-165): when given, the id of each `nothing_to_keep` row is appended in step (the caller names the records). A hand-entered pending entry (`ladder.entered_by`
    reviewer) is never a stale row (T-165 r2, `_keep_hand_entry`): a re-run must not sweep the paralegal's work; when the AI now also has an entry for the record it gets a rerun_note."""
    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
    kept, empty = [], []
    for it in items:
        old = existing.get(it["id"])
        if additive and old is not None:
            continue
        if old is not None and kind == "amount":        # T-084: a rerun keeps the class the paralegal gave a figure
            from app.backend import reclassify as RC
            it = RC.carry_over(old, it)
        decided = old is not None and old["review_status"] != "pending"
        cause = _degrades(kind, old, it) if old is not None else None
        how = "failed" if cause else None
        if decided and not cause and _disagrees(kind, old, it):
            cause, how = "a different result", "disagreed"
        if cause:
            kept.append((old, cause, how))
            if decided:
                msg = (f"The re-run could not redo this item ({cause}). Your decision and the earlier result were kept." if how == "failed" else
                       "The re-run gave a different result for this item (its summary, quote or checks no longer match what you decided on). Your decision and the earlier result were kept; the new result was not applied.")
                DB.update_item(conn, it["id"], now=now, case=cid, ladder={**(old.get("ladder") or {}), "rerun_note": {"kind": how, "step": cause, "message": msg, "at": now}})
            continue
        fail = _failure(kind, it)
        if fail:
            empty.append(fail)
            if empty_ids is not None:
                empty_ids.append(it["id"])
        row = _row(kind, it)
        if old is None:
            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
            continue
        DB.update_item(conn, it["id"], now=now, case=cid, **row)
        if kind == "flag" and old["review_status"] != "pending":
            oc = old.get("computed") or {}
            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
            else:
                it["review_status"] = old["review_status"]
        elif old["review_status"] != "pending":
            it["review_status"] = old["review_status"]
    if additive:
        return kept, empty
    keep = {i["id"] for i in items}
    live = {}      # record id -> id of the AI entry that came out for it on this run
    for i in items:
        if kind == "entry" and i.get("state") != "rejected":
            for r in (i.get("record_ids") or []):
                live.setdefault(r, i["id"])
    for oid, old in existing.items():
        if oid not in keep and old["review_status"] == "pending":
            if kind == "entry" and (old.get("ladder") or {}).get("entered_by") == "reviewer":
                _keep_hand_entry(conn, old, live, cid, now)      # T-165 r2: the paralegal's own entry is never swept, whether or not the AI now has one
                continue
            if not prune:
                kept.append((old, "finding the flags", "failed"))
                continue
            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
    return kept, empty


def _keep_hand_entry(conn, old: dict, live: dict, cid: str, now: float) -> None:
    """T-165 r2: a pending hand-entered entry survives every re-run untouched. When the AI now also has an entry for the record, `ladder.rerun_note` (kind `ai_entry`) says so and
    she chooses (T-146 keep-and-note); the note is dropped again when a later run has no AI entry for it."""
    ladder = dict(old.get("ladder") or {})
    ai = next((live[r] for r in (old["record_ids"] or []) if r in live), None)
    note = ladder.get("rerun_note")
    if ai:
        no = str(old["record_ids"][0]).lstrip("r")
        msg = f"{'The prepared-answer step' if AU.answers_prepared() else 'The AI step'} now has an entry for record {no} ({ai}) as well. Your entry was kept; keep whichever is right and dismiss the other."
        if (note or {}).get("message") != msg:
            DB.update_item(conn, old["id"], now=now, case=cid, ladder={**ladder, "rerun_note": {"kind": "ai_entry", "step": "writing the entries", "message": msg, "ai_entry": ai, "at": now}})
    elif (note or {}).get("kind") == "ai_entry":
        ladder.pop("rerun_note")
        DB.update_item(conn, old["id"], now=now, case=cid, ladder=ladder)


def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
    _store_records(conn, cid, ing, now)
    _store_run_checks(conn, cid, ing["records"], "pending")
    _persist(conn, cid, "flag", ing["flags"], now)
    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
    return ing


# ------------------------------------------------------------------ stages 4-6 helpers
def _finish_amount(a: dict, ing: dict, judged) -> dict:
    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
    by_n = {r["n"]: r for r in ing["records"]}
    a = dict(a)
    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
    verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
    state, reasons = confidence.compose_state(
        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
        {"injection": a["injection"], "amount_class": a["cls"], "translated": any(language.translated_record(by_n.get(n)) for n in a["record_nos"])})      # D-050
    a["state"], a["reasons"] = state, reasons
    a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
                   "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
                              "verdict": judged["verdict"], "reason_code": judged.get("reason_code")} if judged else None),
                   **({"confirm": a["confirm"]} if a.get("confirm") else {})}      # D-059: the flag the paralegal must confirm by name before accepting this charge
    a["why"] = WHY.join(reasons, a["ladder"]["judge"]) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
    return a


def _entry_for(entries: list, record_no: int):
    return next((e["id"] for e in entries if f"r{record_no}" in e["record_ids"]), None)


def _err(code, stage, record_no=None, cause=None) -> dict:
    d = {"code": code, "stage": stage}
    if record_no is not None:
        d["record_no"] = record_no
    if cause:
        d["cause"] = cause
    return d


def _accident_year(recs: list):
    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso"))      # D-055: a year hint from every dated record; the ingest kind is a label guess and is not read
    return int(ds[0][:4]) if ds else None


def _items(n: int) -> str:
    return f"{n} item{'s' if n != 1 else ''}"


def _partial_error(kept: list, empty: list, down: tuple = (), records: list = ()):
    """T-146 r3: the case's honest message for a re-run that kept earlier work or had a step fail with nothing to fall back on (code `run_partial`), or None.
    It names how many items and which steps, and says exactly what was kept. `down` (T-161 r2): steps that failed without leaving any row to count (the flag step on
    records with no phrase-list hit makes no flag at all), named without a count. `records` (T-165): the record numbers whose extract step failed with nothing to keep; the message names
    them and the error carries them (`records`, plus `extract_only` when that is the whole failure, so a hand entry can clear it)."""
    failed, differed = [k for k in kept if k[2] == "failed"], [k for k in kept if k[2] == "disagreed"]
    step = "The prepared-answer step" if AU.answers_prepared() else "The AI step"      # D-069: the set in use chooses the wording; nothing is rewritten afterwards
    parts = []
    if failed:
        parts.append(f"{step} failed for {_items(len(failed))} ({' and '.join(sorted({c for _, c, _ in failed}))}) on this run. Their earlier results and every "
                     "decision of yours were kept unchanged.")
    if differed:
        parts.append(f"The re-run gave a different result for {_items(len(differed))} you had already decided; your decision and the earlier result were kept, "
                     "and each item carries a note.")
    if empty:
        parts.append(f"{step} also failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) with no earlier result to keep." if kept else
                     f"{step} failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) on this run, and there is no earlier result to keep.")
    if down:
        parts.append(f"{step} ({' and '.join(sorted(down))}) failed on this run, so nothing from it could be used.")
    if records:
        parts.append(f"No entry was made for record{'s' if len(records) != 1 else ''} {_nos(records)}.")
    msg = " ".join(parts + ["Run it again to retry."])
    err = {"code": "run_partial", "message": msg} if parts else None
    if err and records:
        err["records"] = list(records)
        if not kept and not down and set(empty) == {_EXTRACT_STEP}:
            err["extract_only"] = True
    return err


def _nos(ns: list) -> str:
    ns = [str(n) for n in ns]
    return ns[0] if len(ns) == 1 else ", ".join(ns[:-1]) + " and " + ns[-1]


def refresh_extract_error(conn, cid: str) -> None:
    """T-165: after the paralegal enters a record by hand, a case that failed ONLY because the extract step failed for named records stops counting the ones now entered:
    it reads ready (no error, no RUN_FAILED) when none is left, and names the rest otherwise. A failure with any other cause (a second check, the flag step, a kept earlier result) is left as
    it is; it needs a re-run."""
    case = DB.get_case(conn, cid)
    err = json.loads(case["error"]) if case.get("error") else None
    if case["status"] != "failed" or not err or err.get("code") != "run_partial" or not err.get("extract_only"):
        return
    hand = generator.entered_by_hand(DB.list_items(conn, cid, "entry"))
    left = [n for n in err["records"] if f"r{n}" not in hand]
    if left == err["records"]:
        return
    new = _partial_error([], [_EXTRACT_STEP] * len(left), records=left) if left else None
    DB.update_case(conn, cid, status="failed" if new else "ready", error=json.dumps(new) if new else None)


def _noting(raw_call, failed_steps: list):
    """T-146 r2: the same `call`, remembering the steps whose call failed (the AI layer gave up, or a fixture was missing). The failure still propagates to the
    caller's own handling; this only lets the run say which steps were down."""
    def call(step, system, user, schema, *, item_id=None):
        try:
            return raw_call(step, system, user, schema, item_id=item_id)
        except (AU.LLMFailed, P.FixtureMiss):
            failed_steps.append(step)
            raise
    return call


def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
    clock = now if callable(now) else (lambda: time.time() if now is None else now)
    t0 = clock()
    call = _noting(call or AU.make_call(conn, cid, now=clock), failed_steps := [])
    errors, stage_done = [], []

    def set_stage(name):
        if on_stage:
            on_stage(name)
        DB.update_case(conn, cid, status="running", stage=name)

    def expired():
        return clock() - t0 > deadline_s

    DB.update_case(conn, cid, status="running", stage="ingest", run_started_at=t0, error=None, backend=P.backend_name())
    try:
        ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid), splitter=_frozen_splitter(conn, cid))
    except language.UnsupportedLanguage:               # D-042: a clear failure, never a run that guesses; the case is not left 'running'
        DB.update_case(conn, cid, status="failed", error=json.dumps({"code": "unsupported_language", "message": "The records are not in English or Spanish."}))
        raise
    text, recs = ing["text"], ing["records"]
    by_n = {r["n"]: r for r in recs}
    _store_split_failure(conn, cid, ing.get("split_failure"))
    if ing.get("split_detail") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
        errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_detail"] == "FIXTURE_MISS" else None))
    _store_records(conn, cid, ing, clock())
    _store_run_checks(conn, cid, recs, "pending")           # a run that dies before the conflict stage leaves 'pending' (GET case: RUN_FAILED)
    dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
    entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
    code_amounts = [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]]
    status = "done"
    timed_out = False

    def guard(name):
        nonlocal timed_out
        if timed_out or expired():
            timed_out = True
            return False
        set_stage(name)
        return True

    # 1-3: entries
    if guard("extract"):
        entries, rejected, failures = generator.extract_entries(recs, ing["groups"], call=call, case_text=text)
        for f in failures:
            rejected.append(generator.failure_entry(by_n[f["record_no"]], next(g for g in ing["groups"] if g[0] == f["record_no"]), f["failure"], f.get("detail")))   # never vanishes: tray item with the reason
            if f["failure"] != "SUMMARY_NOT_IN_QUOTE":      # D-054: a tray item, not an error (the model answered; code removed what the quote does not support)
                errors.append(_err("UNSUPPORTED_LANGUAGE" if f["failure"] == "UNSUPPORTED_LANGUAGE" else "LLM_FAILED_AFTER_RETRIES", "extract", f["record_no"],
                                   "FIXTURE_MISS" if f["failure"] == "FIXTURE_MISS" else None))
    if guard("verify"):
        pass                                    # grounding, token and qualifier checks ran inside extract_entries (code, same call per record)
    if guard("judge_entries") and entries:
        generator.judge_entries(entries, by_n, call=call, case_text=text)
    _mark_judge_not_run(entries, by_n)           # T-145: judge 1 did not run (deadline) -> never 'verified'
    for e in entries + rejected:
        e["ladder"]["backend"] = P.backend_name()
        e.pop("_stage", None)
    # 4: amounts (J2 on every dollar amount)
    final_amounts = code_amounts
    if guard("amounts"):
        dollars = [a for a in ing["amounts"]]
        verdicts = judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars],
                                        call=call, case_text=text)
        final_amounts = [_finish_amount(a, ing, verdicts.get(a["id"])) for a in dollars] + [_finish_amount(a, ing, None) for a in ing["damages"]]
    for a in final_amounts:
        a["entry_id"] = _entry_for(entries, a["record_nos"][0])
    # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T-094). No model search, so the candidate set cannot vary.
    llm_flags = []
    distinct = [by_n[g[0]] for g in ing["groups"] if by_n[g[0]].get("lang") != "other"]     # unsupported-language records are skipped (warning + error)
    conflicts_ran = guard("conflicts")
    if conflicts_ran:
        llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
    # 6: per-record flags (one call per distinct record) + J4
    if guard("flags"):
        year = _accident_year(recs)

        def one(r):
            if expired():                    # the deadline also applies inside the stage, record by record
                return r, None
            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
            per = list(ex.map(one, distinct))
        for r, fs in per:
            if fs is None or expired():
                timed_out = True
                continue
            fs = [f for f in fs if f["type"] != "record_warning"]          # stage 0 already made the record_warning flag
            for k, f in enumerate(fs, 1):
                f["id"] = f"f_r{r['n']}_{k}"
            llm_flags += FL.judge_flags(fs, call=call, case_text=text)
    # 7: finalize
    set_stage("finalize")
    for f in llm_flags:
        f.setdefault("record_nos", [f["record_no"]])
        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
        f["ladder"]["item_id"], f["ladder"]["backend"], f["ladder"]["state"] = f["id"], P.backend_name(), f["state"]
        f["ladder"]["code_checks"].setdefault("classified_by", "lexicon+llm")
        f.setdefault("review_status", "pending")
        f["origin"] = _ORIGIN.get(f["origin"], f["origin"])
        f.pop("record_no", None)
    flag_items = ing["flags"] + [_clean(f) for f in llm_flags if f["state"] != "rejected"]
    tray = [_clean(e) for e in rejected] + [_clean(f) for f in llm_flags if f["state"] == "rejected"]
    entries = [_clean(e) for e in entries]
    dated = sorted((e for e in entries if dated_cut(e)), key=lambda e: (e["date"], e["seq"]))
    undated = [e for e in entries if not dated_cut(e)]
    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
    flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
    final_amounts = [_clean(a) for a in final_amounts]
    damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
    from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
    now_t = clock()
    by_hand = generator.entered_by_hand(DB.list_items(conn, cid, "entry"))      # T-165: records the paralegal already entered by hand
    empty_eids = []
    kept_e, empty_e = _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out, empty_ids=empty_eids)
    stub_rid = {e["id"]: e["record_ids"][0] for e in tray if e.get("record_ids")}
    no_entry = sorted(int(stub_rid[i][1:]) for s, i in zip(empty_e, empty_eids) if s == _EXTRACT_STEP and stub_rid.get(i) not in by_hand)      # extract failed, nothing earlier kept, not entered by hand
    empty_e = [s for s, i in zip(empty_e, empty_eids) if not (s == _EXTRACT_STEP and stub_rid.get(i) in by_hand)]
    for a in final_amounts:                     # an amount stays linked to the entry whose record failed this time (that entry's stored row was kept)
        if not a.get("entry_id"):
            a["entry_id"] = next((o["id"] for o, _, _ in kept_e if f"r{a['record_nos'][0]}" in (o["record_ids"] or [])), None)
    kept_a, empty_a = _persist(conn, cid, "amount", final_amounts, now_t, additive=timed_out)
    kept_f, empty_f = _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t, additive=timed_out,
                               prune="flags" not in failed_steps)      # conflicts are code candidates + judge 3: a down judge leaves them in the run, only the flag step can lose a stored flag
    kept, empty = kept_e + kept_a + kept_f, empty_e + empty_a + empty_f
    _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
    if timed_out:
        status = "timeout"
        err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    else:
        status = "done_with_errors" if errors else "done"
        # T-161: a first run with a judge or the flag step down fails like a re-run. The flag step is read from the steps that were down (a note with no phrase-list hit has no flag row to carry the failure).
        # T-165: an extract failure fails the case on a first run too, however many other records came out, and the records are named; a record the paralegal entered by hand is not one of them.
        named = {c for _, c, _ in kept} | set(empty)
        down = ("finding the flags",) if "flags" in failed_steps and "finding the flags" not in named else ()
        err = _partial_error(kept, empty, down, no_entry)
    DB.update_case(conn, cid, status="failed" if (timed_out or err) else "ready", stage="finalize", error=json.dumps(err) if err else None,
                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
    tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
    all_items = dated + undated + final_amounts + flag_items
    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot,
            "warnings": ing["warnings"] + generator.hand_entered_warnings(DB.list_items(conn, cid, "entry")),
            "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
            "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
                       "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
                       "verified": sum(1 for i in all_items if i["state"] == "verified")}}


# ------------------------------------------------------------------ eval / API view
def case_view(out: dict) -> dict:
    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
    flags = []
    for f in out["flags"] + out["tray"]:
        if "summary" in f:
            continue
        g = dict(f)
        g["evidence"] = [{**e, "record_id": f"r{e['record_no']}", "excerpt": e.get("text")} for e in f.get("evidence", [])]
        if f["type"] == "gap":
            g["computed"] = {"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}
        flags.append(g)
    return {"records": out["records"], "entries": out["entries"], "undated_entries": out["undated_entries"],
            "amounts": [{**a, "value_cents": a["cents"], "kind": a["cls"]} for a in out["amounts"] + out["damages"]],
            "totals": out["totals"], "flags": flags, "tray": [t for t in out["tray"] if "summary" in t], "warnings": out["warnings"],
            "dates_to_confirm": out["dates_to_confirm"], "status": out["status"], "errors": out["errors"],
            "backend": P.backend_name(), "models": {"generator": judges.generator_model(), "judge": judges.judge_model()}}


class _Backend:
    """Temporarily select the LLM backend for one call (eval runner passes it explicitly)."""

    def __init__(self, name):
        self.name, self.old = name, None

    def __enter__(self):
        import os
        self.old = os.environ.get("LLM_BACKEND")
        if self.name:
            os.environ["LLM_BACKEND"] = self.name

    def __exit__(self, *a):
        import os
        if self.old is None:
            os.environ.pop("LLM_BACKEND", None)
        else:
            os.environ["LLM_BACKEND"] = self.old


def _scratch_call(tmp, text):
    import os
    conn = DB.connect(os.path.join(tmp, "scratch.sqlite"))
    cid = DB.create_case(conn, text, now=0.0)
    return conn, cid, AU.make_call(conn, cid)


def run_case(text: str, backend: str = None) -> dict:
    """Full pipeline over `text` on a scratch database; returns case_view(). Used by evals; nothing is kept."""
    import contextlib
    import tempfile
    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
        conn, cid, call = _scratch_call(tmp, IN.normalize_text(text))
        with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
            out = run_pipeline(conn, cid, text, call=call)
        view = case_view(out)
        conn.close()
        return view


def judge_summary(summary: str, excerpt: str, label: str, backend: str = None) -> str:
    """Judge 1 on one (summary, excerpt, label): 'supported' | 'partially' | 'unsupported' | 'unavailable'. A missing fixture or a failed call
    is 'unavailable', never a pass."""
    import contextlib
    import tempfile
    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
        conn, cid, call = _scratch_call(tmp, excerpt)
        with (P.record_fragment_context(excerpt) if P._recording() else contextlib.nullcontext()):
            v = judges.run_j1(summary, excerpt, label, call=call)
        conn.close()
        return v


# ------------------------------------------------------------------ CLI
def _usd(c):
    return TT.usd(c)


def format_report(out: dict) -> str:
    from app.backend.dates import long_date
    L = [f"Status: {out['status']}   backend: {P.backend_name()}   records: {len(out['records'])}   entries: {len(out['entries'])}"
         f"   flags: {len(out['flags'])}   amounts: {len(out['amounts'])}", "", "TIMELINE"]
    for e in out["entries"]:
        L.append(f"  {long_date(e['date'])} - {e['provider']} [{e['state']}]\n      {e['summary']}")
    for e in out["undated_entries"]:
        L.append(f"  (date to confirm) {e['provider']} [{e['state']}]\n      {e['summary']}")
    for title, types in (("GAPS", ("gap",)), ("CONFLICTS", ("conflict",)), ("PRE-EXISTING", ("pre_existing",)), ("CAUSATION LANGUAGE", ("causation",)),
                         ("RECORD WARNINGS", ("record_warning",))):
        fs = [f for f in out["flags"] if f["type"] in types]
        if fs:
            L += ["", title] + [f"  [{f['state']}] {f['title']} - {f['explanation']}" for f in fs]
    L += ["", "AMOUNTS"] + [f"  {a['text']} ({a['cls']}) record {','.join(str(n) for n in a['record_nos'])} [{a['state']}]" for a in out["amounts"]]
    t = out["totals"]
    L.append(f"  Charges detected, pending review (not a total): {_usd(t['detected_pending_cents'])}; accepted so far: {_usd(t['accepted_cents'])}")
    if out["errors"]:
        L += ["", "ERRORS"] + [f"  {e['code']} at {e['stage']}" + (f" record {e['record_no']}" if "record_no" in e else "") for e in out["errors"]]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m app.pipeline", description="Run the treatment-timeline pipeline on a text file (synthetic data only).")
    ap.add_argument("file")
    ap.add_argument("--db", default=None, help="SQLite file (default: a temporary file deleted on exit; the audit log lives there)")
    ap.add_argument("--json", action="store_true", help="print the full result as JSON")
    a = ap.parse_args(sys.argv[1:] if argv is None else argv)
    raw = open(a.file, encoding="utf-8").read()
    try:
        IN.check_limits(raw)
    except IN.IngestError as e:
        print(f"refused: {e.code}", file=sys.stderr)
        return 1
    try:
        language.case_check(language.annotate(IN.ingest(raw)["records"]))
    except language.UnsupportedLanguage as e:
        print(f"refused: {e.code} ({', '.join(e.names)})", file=sys.stderr)
        return 1
    import os
    import tempfile
    with tempfile.TemporaryDirectory() as d:          # a file, not :memory: (worker threads share the connection)
        conn = DB.connect(a.db or os.path.join(d, "cli.sqlite"))
        cid = DB.create_case(conn, IN.normalize_text(raw), now=time.time())
        out = run_pipeline(conn, cid, raw)
        conn.close()
    print(json.dumps(out, indent=1, default=str) if a.json else format_report(out))
    return 0 if out["status"] in ("done", "done_with_errors") else 1


if __name__ == "__main__":
    sys.exit(main())
