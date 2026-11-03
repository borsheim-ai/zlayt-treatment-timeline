"""Read-side views in the shapes of memory/contracts/api.md, built from the DB. No writes."""
import json
import re

from app.backend import amounts as AM, conflict_candidates, confidence, date_convention, flag_templates as FT, generator, grounding, ingest, language, overlap, pdf_text, review, sentences, spanish, store, totals as T, uncovered, why
from app.db import db as DB
from app.llm import audited as AU

STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
OK_WHY = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."


def _why(reasons, judge=None, prep=False):
    out = []
    for c in reasons or []:
        try:
            out.append(why.why(c, None if "FIXTURE_MISS" in reasons else judge, prep))
        except KeyError:
            pass
    return " ".join(out) if out else OK_WHY


def _human(row):
    ed = row.get("edited") or {}
    return {"action": STATUS_ACTION.get(row["review_status"]), "edited_text": ed.get("summary") or ed.get("note"),
            "at": ed.get("at")}


def _ladder(row, prep=False):
    lad = dict(row.get("ladder") or {"item_id": row["id"]})
    if prep and isinstance(lad.get("translation"), dict):      # D-069: rebuilt from the prepared template, not rewritten
        lad["translation"] = {**lad["translation"], **_translation(row, True)}
    lad["item_id"] = row["id"]
    lad["state"] = row["state"]
    lad["human"] = _human(row)
    lad.pop("pre_edit", None)      # T-138: the undo snapshot is internal (api.md), never in a payload
    return lad


def rerun_available(row) -> bool:
    """T-157: whether "run the second check again" can get an answer for this item: no in demo / fixture mode (no live model), no after a rerun that got no answer, yes otherwise."""
    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
    return store.live_model_available() and not (last and last.get("verdict") == "unavailable")


def _common(row, prep=False):
    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge"), prep),
            "review_status": row["review_status"], "version": row.get("updated_at"), "edited": row.get("edited"), "ladder": _ladder(row, prep),
            "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message"),
            "rerun_available": rerun_available(row)}      # T-146 r3: set when a re-run disagreed with or failed on this decided item


def entry_view(row, recs, prep=False):
    r = recs.get((row["record_ids"] or [None])[0], {})
    ed = row.get("edited") or {}
    return {**_common(row, prep), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
            "provider": row["provider"], "summary": ed.get("summary", row["summary"]), "ai_drafted": "summary" not in ed and not (row.get("ladder") or {}).get("entered_by"),
            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
            "excerpt": ed.get("excerpt", row["excerpt"]), "excerpt_start": ed.get("excerpt_start", row["excerpt_start"]),
            "excerpt_end": ed.get("excerpt_end", row["excerpt_end"]), "duplicate_note": None, "translation": _translation(row, prep),
            "edit_to_check": review.edit_unconfirmed("entry", row)}      # T-134: reworded, still needs_review, not yet accepted: not in the letter


def _translation(row, prep=False):
    """D-042: set on an entry made from a Spanish record: its summary is an English translation, its quote the original Spanish."""
    t = (row.get("ladder") or {}).get("translation")
    return spanish.translation_info(t.get("source_language", "es"), "summary" in (row.get("edited") or {}) or bool(t.get("human_written")), prep) if t else None


def accept_effect(row) -> str:
    """What Accept does to an amount (T-114): `letter_total` (a charge: counted in the billed-charges total), `acknowledge` (a rate: noted in the internal notes only,
    never totaled, and no second AI check is needed), `internal_notes` (estimate, unclear: noted for the paralegal, never in the total)."""
    return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")


def amount_flag(row):
    """D-059: the flag a charge carries (likely_duplicate | likely_total) and whether accepting it now needs the confirm step. (None, False) for any other amount."""
    f = (row.get("ladder") or {}).get("confirm") if row["kind"] == "charge" else None
    return (None, False) if not f else ({k: f.get(k) for k in ("flag", "name", "message", "confirm_with", "of", "confirmed_at")}, row["review_status"] == "pending")


def not_counted_info(row, records):
    """D-064: {reason, countable} for one amount row. `records` = store.load_records(conn, case_id) (the case's records, with their body excerpt, source and date)."""
    rec = next((r for r in records or [] if r["id"] == (row["record_ids"] or [None])[0]), None)
    demoted = ((row.get("ladder") or {}).get("reclassification") or {}).get("to") == "unclear"
    return AM.not_counted(row["excerpt"], row["text"], row["value_cents"], (rec or {}).get("source"), (rec or {}).get("date_iso"), store.amount_pos(row, rec),
                          records, row["kind"], injection=bool(rec and rec.get("injection_tag")), demoted=demoted)


def _count_basis(b, rec, info):
    """In a document with no header the record's date stands in for a date of service; a line that states no date of its own then has none (dos None) for the duplicate match."""
    return {**b, "dos": None} if info["reason"] == AM._UNKNOWN_WHY and b.get("dos") == rec.get("date_iso") else b


class CountPool:
    """D-064 r2: the case's other lines a countable line is compared with (amounts.count_flag): every live charge and every countable amount, read once per list and only when a
    countable line asks."""
    def __init__(self, conn, case_id, records):
        self.conn, self.case_id, self.records, self._items = conn, case_id, records, None

    def items(self):
        if self._items is None:
            from app.backend import reclassify          # lazy: reclassify imports present
            recmap = {r["id"]: r for r in self.records or []}
            self._items = []
            for o in DB.list_items(self.conn, self.case_id, "amount"):
                orec = recmap.get((o["record_ids"] or [None])[0])
                if orec is None or o["state"] == "rejected" or o["review_status"] == "dismissed" or o["value_cents"] is None:
                    continue
                info = {"reason": None, "countable": True} if o["kind"] == "charge" else not_counted_info(o, self.records)
                if not info["countable"]:
                    continue
                b = reclassify._basis(o, orec)
                if b is None:
                    continue
                b = _count_basis(b, orec, info)
                sp = reclassify._figure_spans(o["excerpt"] or "", o, orec)
                self._items.append({"id": o["id"], "record_no": orec["n"], "cents": o["value_cents"], "basis": b, "charge": o["kind"] == "charge",
                                    "line": AM.charge_line(o["excerpt"], sp[0][0]) if sp else ""})
        return self._items


def count_flag_for(row, records, info, pool):
    """The likely_duplicate / likely_total confirm a countable amount needs before it is counted (amounts.count_flag), or None. Same function for the view and the count action."""
    if not info["countable"] or row["kind"] == "charge" or pool is None:
        return None
    from app.backend import reclassify
    rec = next((r for r in records or [] if r["id"] == (row["record_ids"] or [None])[0]), None)
    b = reclassify._basis(row, rec) if rec is not None else None
    if b is None:
        return None
    b = _count_basis(b, rec, info)
    return AM.count_flag({"id": row["id"], "record_no": rec["n"], "cents": row["value_cents"], "basis": b}, pool.items())


def amount_view(row, recs, records=None, pool=None, prep=False):
    flag, needs = amount_flag(row)
    nc = not_counted_info(row, records)
    cf = count_flag_for(row, records, nc, pool)
    counted = bool((row.get("ladder") or {}).get("counted"))
    c = _common(row, prep)
    srec = next((r for r in records or [] if r["id"] == (row["record_ids"] or [None])[0]), None)
    if counted and row["kind"] == "charge":      # D-064: counted by the paralegal with a named confirm; no AI said it was a charge
        c["why"] = ("You counted this line as a separate charge and confirmed it by name. The code found the figure in the record; no second check was asked about it." if prep else
                    "You counted this line as a separate charge and confirmed it by name. The code found the figure in the record; no AI check was asked about it.")
    if row["kind"] == "unclear" and nc["reason"]:      # D-064: the true per-line reason, not the generic 'could not be read or labelled' sentence
        c["why"] = c["why"].replace(why.why("AMOUNT_UNCLEAR"), nc["reason"]) if why.why("AMOUNT_UNCLEAR") in c["why"] else nc["reason"] + " " + c["why"]
    return {**c, "flag": flag, "confirm_required": needs, "record_ids": row["record_ids"], "entry_id": row["entry_id"], "text": row["text"], "value_cents": row["value_cents"],
            "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
            "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate" and not counted,
            "not_counted_reason": nc["reason"], "countable": nc["countable"],
            "service_date": store.charge_service_date(row, srec, store.amount_pos(row, srec)) if row["kind"] == "charge" else None,      # D-071: what the letter prints for this charge's date
            "count_confirm": {k: cf.get(k) for k in ("flag", "name", "message", "confirm_with", "of")} if cf else None}


def _computed(c):
    c = dict(c or {})
    if "from_date" in c:
        c.update({"from": c.pop("from_date"), "to": c.pop("to_date", None)})
        c.setdefault("threshold", 30)
        ids = c.get("record_ids") or []
        if ids:
            c["from_record"], c["to_record"] = ids[0], ids[-1]
    return c


def _evidence(evs, recs):
    by_n = {r["seq"]: r["id"] for r in recs.values()}
    return [{"record_id": e.get("record_id") or by_n.get(e.get("record_no")), "excerpt": e.get("excerpt") if e.get("excerpt") is not None else e.get("text"),
             "start": e.get("start"), "end": e.get("end")} for e in (evs or [])]


def _gap_why(row, base):
    """D-055: a gap's why also carries the code-built warning for each end that looks like paperwork (intake form, bill, ...), as stored by code."""
    ws = (row.get("computed") or {}).get("endpoint_warnings") or []
    ex = [x["warning"] for x in ws if x.get("warning")]
    alt = next((x["alternative"] for x in ws if x.get("alternative") and x["alternative"] not in ex), None)      # the other number, once (D-055 round 4)
    if alt:
        ex.append(alt)
    if row["type"] != "gap" or not ex:
        return base
    return " ".join(([] if base == OK_WHY else [base]) + ex)


def flag_view(row, recs, prep=False):
    c = _common(row, prep)
    c["why"] = _gap_why(row, c["why"])
    title, expl = FT.PREPARED_TEXT.get(row["category"]) if prep and row["category"] in FT.PREPARED_TEXT else (row["title"], row["explanation"])      # D-069
    if prep and (title, expl) == FT.UNRECOGNISED:
        title, expl = FT.UNRECOGNISED_PREPARED
    return {**c, "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": title,
            "explanation": expl, "computed": _computed(row["computed"]), "evidence": _evidence(row["evidence"], recs),
            "origin": row["origin"], "reviewer_note": row["reviewer_note"]}


def gap_change_index(events, current: dict):
    """T-127: which gap figures a confirm_date moved, kept with the case. `events` are the case's review events (oldest first); each `confirm_date` event's `after.gap_changes`
    holds what confirm_date reported (with record_seq and sentence). `current` maps gap flag id -> {days, from, to}. Returns ({flag_id: change} for gaps whose CURRENT figures
    are the ones that change produced, [removed changes whose gap is still gone]). A later change to the same gap replaces the earlier one; once the figures differ from the
    ones the change produced, nothing is claimed. Code over stored figures, never a model."""
    latest, gone = {}, {}
    for e in events:
        if e.get("action") != "confirm_date":
            continue
        for ch in (e.get("after") or {}).get("gap_changes") or []:
            fid = ch.get("flag_id")
            if ch.get("change") == "removed":
                latest.pop(fid, None)
                gone[fid] = ch
            else:
                gone.pop(fid, None)
                latest[fid] = ch
    kept = {}
    for fid, ch in latest.items():
        cur = current.get(fid)
        if cur and cur.get("days") == ch.get("new_days") and (ch.get("new_from") is None or cur.get("from") == ch["new_from"]) and (ch.get("new_to") is None or cur.get("to") == ch["new_to"]):
            kept[fid] = ch
    return kept, [ch for fid, ch in gone.items() if fid not in current]


def _with_gap_changes(conn, case_id, flags):
    """Adds `gap_change` (or None) to every gap flag view; returns (flags, gap_changes_removed)."""
    cur = {f["id"]: {"days": f["computed"].get("days"), "from": f["computed"].get("from"), "to": f["computed"].get("to")} for f in flags if f["type"] == "gap"}
    kept, removed = gap_change_index(DB.list_events(conn, case_id), cur)
    for f in flags:
        if f["type"] == "gap":
            f["gap_change"] = kept.get(f["id"])
    return flags, removed


_VIEW = {"entry": entry_view, "amount": amount_view, "flag": flag_view}
_ID_KIND = {"e": "entry", "a": "amount", "f": "flag"}


def _recs_by_id(conn, case_id):
    cfg = (DB.get_case(conn, case_id) or {}).get("config") or {}
    unsplit, pre = set(cfg.get("unsplit_records") or []), set(cfg.get("preamble_records") or [])      # T-129: stored by pipeline._store_record_marks
    out = {}
    for x in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
        r = DB._decode(x)
        r["unsplit"], r["preamble"] = r["id"] in unsplit, r["id"] in pre
        out[r["id"]] = r
    return out


def view_of(kind, row, conn, case_id, recs, records=None, pool=None, prov=None):
    """One item's view. An amount also needs the case's records (D-064); pass them (and one CountPool) when building a list so they are read once.
    `prov` (Prov) carries the case's calls so a list reads them once; the item's wording is chosen from it (D-069)."""
    prov = prov if prov is not None else Prov(conn, case_id)
    prep = prov.prepared(row)
    if kind == "amount":
        records = records if records is not None else store.load_records(conn, case_id)
        return amount_view(row, recs, records, pool if pool is not None else CountPool(conn, case_id, records), prep)
    return _VIEW[kind](row, recs, prep)


def item_view(conn, case_id, item_id):
    row = DB.get_item(conn, item_id, case_id)
    kind = _ID_KIND[item_id[0]]
    prov = Prov(conn, case_id)
    v = view_of(kind, row, conn, case_id, _recs_by_id(conn, case_id), prov=prov)
    v["kind"] = kind
    v["second_check_pending"] = item_id in second_check_pending_ids(conn, case_id)
    with_provenance(conn, case_id, [v], prov)
    if kind == "entry":
        review.hold_hints(conn, case_id, [v])      # T-139 r3: the held-out hint says where this record's figures are counted
    if kind == "flag":
        _with_gap_changes(conn, case_id, [v])
    return v


class Prov:
    """D-069: the provenance of the answers behind one case's items, read once. `prepared(row)` is the field every user-facing sentence about the item is keyed by: the item's first
    answer is a hand-checked fixture, or the case's answers are the prepared ones (so even a code-made item talks about 'the second check', never 'the second AI check')."""

    def __init__(self, conn, case_id, calls=None):
        self.calls = DB.list_llm_calls(conn, case_id) if calls is None else calls
        self.by_id = {c["id"]: c for c in self.calls}
        self.by_item = {}
        for c in self.calls:
            if c["role"] == "generator" and c.get("item_id"):
                self.by_item.setdefault(c["item_id"], []).append(c)
        self.case_prepared = models_for(conn, case_id, {"generator": "", "judge": ""}, self.calls)["generator_prepared"]

    def first_call(self, row):
        """The generator call behind the item: its ladder's call, else the item's last generator call, else (a flag) its record's flag call."""
        gen = (row.get("ladder") or {}).get("generator")
        call = self.by_id.get((gen or {}).get("call_id")) or next(iter(reversed(self.by_item.get(row["id"], []))), None)
        if call is None and str(row["id"]).startswith("f_") and row.get("origin") in FLAG_AI_ORIGINS:
            call = flag_generator_call(self.calls, row["id"], row.get("type"))      # T-177 r3: a flag's generator answer is its record's flag call (the ladder does not record it)
        return call

    def item_prepared(self, row) -> bool:
        call = self.first_call(row)
        return bool(call) and AU.is_prepared(call.get("recorded_from"))

    def prepared(self, row) -> bool:
        return self.case_prepared or self.item_prepared(row)


def with_provenance(conn, case_id, views, prov=None):
    """D-065: mark every item whose generator answer is a hand-checked fixture (the call's recorded_from.backend is 'curated') `prepared: true` and put the fixture's own model name
    ('hand-checked (qa)') on its ladder's generator, so no screen or payload names a model for an answer no model gave. Others get prepared false and keep their model id.
    D-069: sets only the provenance fields; every sentence was already built from the prepared templates (view_of), none is rewritten here."""
    prov = prov if prov is not None else Prov(conn, case_id)
    for v in views:
        gen = (v.get("ladder") or {}).get("generator")
        call = prov.first_call(v)      # a view carries the same id / ladder / type / origin the call lookup reads
        prepared = bool(call) and AU.is_prepared(call.get("recorded_from"))
        if str(v.get("id", "")).startswith("f_") and v.get("origin") in CODE_ONLY_FLAG_ORIGINS:
            prepared = False      # T-214: found only by code (the phrase list; the model's answer had nothing for it), so no curated answer is behind it
            v["origin_label"] = CODE_ONLY_FLAG_ORIGINS[v["origin"]]
        v["prepared"] = prepared
        if gen is not None:
            gen = v["ladder"]["generator"] = dict(gen, prepared=prepared)      # a copy: the stored row is never touched
            if prepared:
                gen["model"] = call["model"]


CODE_ONLY_FLAG_ORIGINS = {"lexicon": "Found by code (phrase list)", "code": "Found by code"}      # T-214 (D-065): a flag whose only source is code is never a "prepared answer"
FLAG_AI_ORIGINS = ("llm", "lexicon+llm", "lexicon")      # the record's flag call ran for these (the phrase-list-only ones too: the call found nothing for them)


def flag_generator_call(calls, item_id, ftype=None):
    """The generator call behind a flag that does not record one: the flags (or, for a conflict, conflicts) call made for its record (item f_r3_1 -> call item f_r3). Without a call of
    its own, the case's last such call when every one of them is the same kind; else None. A call that found no recorded answer is not an answer."""
    step = "conflicts" if ftype == "conflict" else "flags"
    gens = [c for c in calls if c["role"] == "generator" and c["step"] == step and not str(c.get("error") or "").startswith("FIXTURE_MISS")]
    base = re.sub(r"_\d+$", "", str(item_id))
    own = [c for c in gens if c.get("item_id") in (item_id, base)]
    if own:
        return own[-1]
    kinds = {AU.is_prepared(c.get("recorded_from")) for c in gens}
    return gens[-1] if gens and len(kinds) == 1 else None


PREPARED_MODEL = AU.PREPARED_MODEL      # what a prepared (curated) answer names as its maker; the same text the audit rows carry


def models_for(conn, case_id, base, calls=None):
    """D-065 (T-177 r2): the {generator, judge} model names a payload shows for THIS case. When every generator answer of the case is a hand-checked fixture, no model drafted it: the generator reads
    'hand-checked (qa)' and `generator_prepared` is true, so no screen names a model for an answer no model gave. A case with any recorded or live answer keeps the configured model; one with no usable answer follows the set in use."""
    calls = DB.list_llm_calls(conn, case_id) if calls is None else calls
    gens = [c for c in calls if c["role"] == "generator" and not str(c.get("error") or "").startswith("FIXTURE_MISS")]      # a call that found no answer is no model's work and no fixture's
    prepared = all(AU.is_prepared(c.get("recorded_from")) for c in gens) if gens else AU.answers_prepared()      # D-069: no usable answer (malformed, empty or missing counts as none) is decided by the set in use, never by a model label
    return dict(base, generator=PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)


def narrative_view(conn, case_id, nar):
    """D-065: the draft paragraph's generator answer, marked prepared (and named 'hand-checked (qa)') when it came from a curated fixture."""
    if not nar or not isinstance(nar.get("generator"), dict):
        return nar
    call = next((c for c in DB.list_llm_calls(conn, case_id) if c["id"] == nar["generator"].get("call_id")), None)
    prepared = bool(call) and AU.is_prepared(call.get("recorded_from"))
    return {**nar, "prepared": prepared, "generator": {**nar["generator"], "prepared": prepared, **({"model": call["model"]} if prepared else {})}}


def second_check_pending_ids(conn, case_id) -> set:
    """T-134 r4: the ids of live AI-made items whose second check has no answer (the same list the export gate's JUDGE_NOT_RUN reads), except a rate (accepting it only
    acknowledges it, no check needed). Lazy import: trace imports this module."""
    from app.backend import trace
    return {u["item_id"] for u in trace.unjudged_items(conn, case_id) if not trace.acknowledge_only(u["kind"], u["row"])}


def all_items(conn, case_id):
    recs = _recs_by_id(conn, case_id)
    records = store.load_records(conn, case_id)      # D-064: the amounts' not-counted reasons read the record body, source and date
    pool = CountPool(conn, case_id, records)
    prov = Prov(conn, case_id)
    out = {k: [view_of(k, r, conn, case_id, recs, records, pool, prov) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
    review.hold_hints(conn, case_id, out["entry"])      # T-139 r3
    with_provenance(conn, case_id, out["entry"] + out["amount"] + out["flag"], prov)
    pend = second_check_pending_ids(conn, case_id)
    for k in ("entry", "amount", "flag"):
        for v in out[k]:
            v["second_check_pending"] = v["id"] in pend
    out["gap_changes_removed"] = _with_gap_changes(conn, case_id, out["flag"])[1]
    return out


def totals_view(conn, case_id):
    am = [a for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
    t = T.totals([{"id": a["id"], "cents": a["value_cents"], "cls": a["kind"], "raw": a["text"], "review_status": a["review_status"]} for a in am])
    ch = [a for a in am if a["kind"] == "charge" and a["value_cents"] is not None]
    cnt = lambda sts: sum(1 for a in ch if a["review_status"] in sts)   # noqa: E731
    return {"accepted": {"cents": t["accepted_cents"], "count": cnt(("accepted", "edited")), "label": "Accepted charges"},
            "pending": {"cents": t["detected_pending_cents"], "count": cnt(("pending",)), "label": "Pending review"},
            "detected_not_a_total": {"cents": sum(a["value_cents"] for a in ch if a["review_status"] != "dismissed"),
                                     "count": sum(1 for a in ch if a["review_status"] != "dismissed"), "label": "Detected (not a total)"},
            "flagged_charges": [{"id": a["id"], "flag": amount_flag(a)[0]["flag"]} for a in am if amount_flag(a)[1]],      # D-059: flagged charges waiting for a named confirm
            "not_totaled": [{"id": a["id"], "kind": a["kind"], "text": a["text"]} for a in am
                            if a["kind"] != "charge" and a["review_status"] != "dismissed" and a["kind"] != "damages"],
            "possible_overlaps": overlap.view(conn, case_id)}      # T-110: a statement line that may include a separately stated charge; warns, never changes the total


def rejected_count(conn, case_id):
    """Entries and amounts in the could-not-verify tray (state rejected), without a placeholder the paralegal has since answered with a hand-entered entry (T-110 r2)."""
    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))
    return sum(1 for k in ("entry", "amount") for r in DB.list_items(conn, case_id, k) if r["state"] == "rejected" and r["id"] not in handled)


def review_view(conn, case_id):
    items = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, case_id, k)]
    handled = generator.resolved_placeholders([r for k, r in items if k == "entry"])
    items = [(k, r) for k, r in items if r["id"] not in handled and not FT.is_filtered(r.get("state_reasons"))]       # D-057: rule-filtered proposals need no action and are not counted
    live = [(k, r) for k, r in items if r["state"] != "rejected"]
    counts = {s: sum(1 for _, r in live if r["review_status"] == s) for s in ("pending", "accepted", "edited", "dismissed")}
    counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
    counts["edit_to_check"] = sum(1 for k, r in live if review.edit_unconfirmed(k, r))      # T-134: counted in `edited`, but open: not in the letter, not accepted
    rank = {"amount": 0, "entry": 1, "flag": 2}
    pend = sorted((x for x in live if x[1]["review_status"] == "pending"),
                  key=lambda x: (confidence.sort_key(x[1]["state"]), rank[x[0]], x[1].get("date_iso") or "", x[1]["id"]))
    return {"counts": counts, "queue": [r["id"] for _, r in pend],
            "ready_to_export": counts["pending"] == 0 and counts["edit_to_check"] == 0 and (counts["accepted"] + counts["edited"] - counts["edit_to_check"]) > 0}


def dates_to_confirm(conn, case_id):
    recs = list(_recs_by_id(conn, case_id).values())
    raw = DB.get_case(conn, case_id)["raw_text"]
    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"],
             "suggestion": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)
            for r in recs if r["date_status"] in ("ambiguous", "missing")]


def record_view(r, raw, with_sentences=True, pages=None):
    block = raw[r["char_start"]:r["char_end"]]
    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
         "date_status": r["date_status"], "date_candidates": r["date_candidates"] or [], "duplicate_of": r["duplicate_of"],
         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
         "char_end": r["char_end"], "text": block, "language": language.block_lang(block),
         "unsplit": bool(r.get("unsplit")), "preamble": bool(r.get("preamble"))}      # T-129: text outside any recognised record (D-027); a preamble sits above the first real record
    if pages:                                    # PDF source (D-031): the page where the record starts
        v["page"] = pdf_text.page_for(pages, r["char_start"])
        from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR
        v["ocr_derived"] = pdf_checks.is_ocr_span(pages, r["char_start"], r["char_end"])
    if with_sentences:
        base, body, why_none = quote_body(block)  # T-108: units come from the quotable body only, the same text the save route checks the quote against
        units = [] if why_none else quote_units(body, {**r, "excerpt": body})
        v["sentences"] = [{"text": body[a:b], "start": r["char_start"] + base + a, "end": r["char_start"] + base + b} for a, b in units]
        if why_none:
            v["sentences_reason"] = why_none           # no sentence is offered; the reason is plain words for the review screen
    return v


NO_UNITS_LAYOUT = ("No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, "
                   "so a quote cut from it could not be checked against the record. Read the record text instead.")
_LABEL_LINE = re.compile(r"^[ \t]*(?:Excerpt:|Date:|Source:|=== Record \d+ ===)", re.MULTILINE)


def quote_body(block):
    """(offset in block, text, reason) of the part of a record a quote can be cut from: the excerpt body, without the date/source/header
    lines, the `Excerpt:` label and the quote marks around a quoted block. The text is the string review.py / generator.py check a saved quote
    against (rec["excerpt"]), found at its true position in the block (searched from the end of the `Excerpt:` label, so a Source line that
    repeats the text is not mistaken for it), so every unit cut from it is a verbatim slice of the record text.
    A record whose excerpt still carries label or header lines (no Date/Source line, so the layout was not recognised) or whose body cannot be
    located gives (0, "", reason): no unit is offered, because a quote cut without the label would not be whole sentences of the text the
    save route checks against."""
    try:
        body = ingest.split_records(block)[0]["excerpt"]
    except ingest.IngestError:
        return 0, "", NO_UNITS_LAYOUT
    if not body or _LABEL_LINE.search(body):
        return 0, "", NO_UNITS_LAYOUT
    m = ingest._F_EXC.search(block)
    i = block.find(body, m.end() if m else 0)
    if i < 0:
        return 0, "", NO_UNITS_LAYOUT
    return i, body, None


def quote_units(body, rec):
    """Whole-sentence spans of `body` the quote picker offers. A sentence that a hedge sentence qualifies cannot be saved without it
    (EXCERPT_OMITS_QUALIFIER), so it is offered as ONE combined unit with the hedge sentence(s) that follow it: the same check the save
    routes run (language module for the record, Spanish hedge words included) decides, so every unit offered saves on its own."""
    check = spanish.module_for(language.record_lang(rec)).check_excerpt
    spans = sentences.stripped_spans(body)
    out, i = [], 0
    while i < len(spans):
        j = i
        while j + 1 < len(spans) and "EXCERPT_OMITS_QUALIFIER" in check(body, body[spans[i][0]:spans[j][1]]):
            j += 1
        out.append((spans[i][0], spans[j][1]))
        i = j + 1
    return out


def case_view(conn, case_id, *, backend, models, demo_mode):
    case = DB.get_case(conn, case_id)
    raw = case["raw_text"]
    recs = list(_recs_by_id(conn, case_id).values())
    its = all_items(conn, case_id)
    ents = its["entry"]
    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))      # T-110 r2: a record the paralegal entered by hand leaves the tray
    live_e = [e for e in ents if e["state"] != "rejected"]
    dated = sorted((e for e in live_e if e["date"] and (e["date_status"] in ("parsed", "confirmed", None))), key=lambda e: (e["date"], e["seq"] or 0))
    undated = [e for e in live_e if e not in dated]
    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
             "attempt": {"summary": x.get("summary"), "excerpt": x.get("excerpt")} if k == "entry" else {"text": x.get("text"), "excerpt": x.get("excerpt")},
             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected" and x["id"] not in handled]
    # D-053: a flag the judge rejected (a model-only flag J4 disagreed with, a code conflict candidate J3 called benign, a model-proposed conflict) is a tray
    # item of kind "flag": the model's attempt is the title and the quote(s); it is never in `flags`, the review queue or the letter.
    def _tray_flag(x):
        return {"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
                "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
                "flag": {"type": x["type"], "category": x["category"]},
                "attempt": {"summary": x.get("title"), "excerpt": " / ".join(e["excerpt"] for e in x["evidence"] if e.get("excerpt"))},
                "ladder": {"item_id": x["id"], "state": "rejected"}}
    rejected_flags = [x for x in its["flag"] if x["state"] == "rejected"]
    filtered = [x for x in rejected_flags if FT.is_filtered(x["reasons"])]
    tray += [_tray_flag(x) for x in rejected_flags if x not in filtered]
    # D-057: model proposals a code rule filtered out are a collapsed, counted group of their own (never in `tray`, `flags`, the queue or the letter)
    rules = []
    for cat in sorted({x["category"] for x in filtered}):
        ref, name, text = FT.FILTER_RULES.get(cat, ("", cat, ""))
        items = [_tray_flag(x) for x in filtered if x["category"] == cat]
        rules.append({"rule": cat, "ref": ref, "label": name, "explanation": text, "count": len(items), "items": items})
    tray_filtered = {"label": "Filtered by rule", "collapsed": True, "needs_action": False, "count": len(filtered), "rules": rules}
    err = json.loads(case["error"]) if case.get("error") else None
    injected = [r["id"] for r in recs if r["injection_tag"]]
    record_views = [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs]
    uncovered.attach(record_views, ents, quote_body)      # T-143: clinical sentences no entry quote covers (review aid; never in the letter or notes)
    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
            "records": record_views, "undated_entries": undated, "entries": dated,
            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete", store.load_records(conn, case_id, raw)), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
            "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
            "review": review_view(conn, case_id), "warnings": generator.hand_entered_warnings(DB.list_items(conn, case_id, "entry")), "error": err,
            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
            **{k: (case.get("config") or {})[k] for k in ("pdf_checks",) if (case.get("config") or {}).get(k)},     # T-086/T-087 (PDF cases only)
            **({"pdf_pages": (case.get("config") or {})["pages"]} if (case.get("config") or {}).get("pages") else {})}


def why_view(conn, case_id, item_id):
    item = item_view(conn, case_id, item_id)
    recs = _recs_by_id(conn, case_id)
    ids = list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])
    seen, src = set(), []
    for rid in ids:
        if rid in recs and rid not in seen:
            seen.add(rid)
            r = recs[rid]
            hs, he = item.get("excerpt_start"), item.get("excerpt_end")
            src.append({"record_id": rid, "char_start": r["char_start"], "char_end": r["char_end"], "highlight_start": hs, "highlight_end": he})
    calls = [_call(c) for c in DB.list_llm_calls(conn, case_id, item_id)]
    events = [{"action": e["action"], "at": store.iso(e["at"])} for e in DB.list_events(conn, case_id, item_id)]
    return {"item": item, "source": src, "calls": calls, "events": events}


def _call(c, full=False):
    rf = c.get("recorded_from")
    prep = AU.is_prepared(rf)
    miss = c["role"] == "generator" and not rf and not c["parsed_ok"] and AU.answers_prepared()      # T-177 r3: a curated set's missing or unusable answer asked no model either
    d = {"id": c["id"], "role": c["role"], "step": c["step"], "backend": c["backend"], "recorded_from": rf, "model": PREPARED_MODEL if miss else c["model"],
         "prompt_version": None if prep else c["prompt_version"], "prompt_sha256": None if prep else c["prompt_sha256"], "item_id": c["item_id"], "attempt": c["attempt"],
         "latency_ms": c["latency_ms"], "cost_usd": c["cost_usd"], "tokens_in": c["tokens_in"], "tokens_out": c["tokens_out"],
         "parsed_ok": bool(c["parsed_ok"]), "verdict": c["verdict"], "prepared": prep}      # D-065: a hand-checked fixture answer, not model output
    if full:
        d.update(system_text=c["system_text"], user_text=c["user_text"], response_raw=c["response_raw"], error=c["error"])
    return d


def audit_view(conn, case_id, full=False):
    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
    calls = DB.list_llm_calls(conn, case_id)
    by = {}
    for c in calls:
        by[c["backend"]] = by.get(c["backend"], 0) + 1
    return {"token": case_id, "calls": [_call(c, full) for c in calls],
            "events": [{"id": e["id"], "item_id": e["item_id"], "action": e["action"], "at": store.iso(e["at"]),
                        **({"confirm": e["after"]["confirm"]} if (e.get("after") or {}).get("confirm") else {}),      # T-159: the flag she confirmed by name (metadata, also in public mode)
                        **({"compared": e["after"]["compared"]} if (e.get("after") or {}).get("compared") else {}),      # T-179 / D-066: she said she compared it with the quote
                        **({"before": e["before"], "after": e["after"]} if full else {})}
                       for e in DB.list_events(conn, case_id)],
            "summary": {"calls": len(calls), "cost_usd": round(sum(c["cost_usd"] or 0 for c in calls), 6),
                        "latency_ms_total": sum(c["latency_ms"] or 0 for c in calls), "by_backend": by}}


def case_list(conn):
    """Local mode only (D-008/D-031): newest first. Metadata and counts, never record text."""
    out = []
    for r in conn.execute("SELECT id FROM cases ORDER BY created_at DESC, rowid DESC"):
        cid = r["id"]
        case = DB.get_case(conn, cid)
        counts = review_view(conn, cid)["counts"]
        out.append({"token": cid, "name": case["name"], "status": case["status"], "source": case["source"],
                    "record_count": conn.execute("SELECT count(*) FROM records WHERE case_id=?", (cid,)).fetchone()[0],
                    "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},
                    "created_at": store.iso(case["created_at"])})
    return out
