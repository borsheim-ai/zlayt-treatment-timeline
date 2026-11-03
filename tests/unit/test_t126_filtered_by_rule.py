"""T-126 (D-057): a model proposal that a code rule filters out (D-032 objective_negative) is listed, not dropped: a collapsed, counted
'Filtered by rule' group in the case payload with the rule named. Never a flag, never in the review queue, timeline or letter; needs no action."""
import json

from app.backend import export, flag_templates as FT, flags as F, present, store, trace
from app.backend import pipeline as PL
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record

R = dict(n=1, source="EMS", excerpt="Cyclist struck by a car at low speed. X-ray negative for fracture. Ankle exam normal. Full cervical ROM.", date_iso="2026-06-01")


def test_a_model_objective_negative_proposal_is_a_filtered_item_not_a_silent_drop():
    llm = [dict(type="causation", category="objective_negative", excerpt="X-ray negative for fracture."),
           dict(type="causation", category="objective_negative", excerpt="X-ray negative for fracture."),          # duplicate: one item
           dict(type="causation", category="objective_negative", excerpt="Ankle exam normal.")]
    out = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": llm}}))
    assert len(out) == 2 and all(f["state"] == "rejected" and f["reasons"][0] == "FILTERED_BY_RULE" and f["origin"] == "llm" for f in out)
    assert [f["excerpt"] for f in out] == ["X-ray negative for fracture.", "Ankle exam normal."]
    assert not [f for f in out if f["state"] != "rejected"]


def test_filtered_items_come_after_every_other_tray_item_so_no_recorded_id_moves():
    llm = [dict(type="causation", category="objective_negative", excerpt="X-ray negative for fracture."),
           dict(type="causation", category="scene_facts", excerpt="Cyclist struck by a car at low speed."),
           dict(type="conflict", category="other_fact_mismatch", excerpt="Ankle exam normal.", excerpt_b="Full cervical ROM.")]
    out = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": llm}}))
    assert [f["reasons"][0] for f in out] == ["LLM_ONLY", "LLM_ONLY", "FILTERED_BY_RULE"]


def test_the_rule_filter_does_not_touch_a_phrase_list_flag_in_the_same_sentence():
    r = dict(R, excerpt="Patient reports prior neck pain. Ankle exam normal.")
    llm = [dict(type="causation", category="objective_negative", excerpt="Ankle exam normal.")]
    out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
    assert [f["category"] for f in out if f["state"] != "rejected"] and [f for f in out if f["reasons"][0] == "FILTERED_BY_RULE"]


def _view(tmp_path, extra):
    conn = DB.connect(str(tmp_path / "c.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=lambda user: {"flags": extra} if which_record(user) == [4] else {"flags": []})),
                    now=lambda: 1.0)
    return conn, cid, present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)


def test_case_payload_has_a_collapsed_counted_group_with_the_rule_named_and_nothing_else_changes(tmp_path):
    (tmp_path / "a").mkdir()
    _, _, base = _view(tmp_path / "a", [])
    extra = [dict(type="causation", category="objective_negative", excerpt="Plan of care: 12 visits."),
             dict(type="causation", category="objective_negative", excerpt="Discharged from PT after two missed appointments.")]
    (tmp_path / "b").mkdir()
    conn, cid, v = _view(tmp_path / "b", extra)
    g = v["tray_filtered"]
    assert g["label"] == "Filtered by rule" and g["collapsed"] is True and g["count"] == 2 and g["needs_action"] is False
    (rule,) = g["rules"]
    assert rule["rule"] == "objective_negative" and rule["ref"] == "D-032" and rule["count"] == 2 and "normal" in rule["label"].lower()
    ids = [i["id"] for i in rule["items"]]
    assert len(ids) == 2 and all(i["flag"]["category"] == "objective_negative" and i["attempt"]["excerpt"] for i in rule["items"])
    assert all(i["reasons"][0] == "FILTERED_BY_RULE" and i["why"] for i in rule["items"])
    # not in the flag list, the review queue, the ordinary tray, the counts that need action, or the letter
    assert not [f for f in v["flags"] if f["id"] in ids]
    assert not set(ids) & set(v["review"]["queue"]) and not [t for t in v["tray"] if t["id"] in ids]
    assert v["flags"] == base["flags"] and v["tray"] == base["tray"] and v["review"]["queue"] == base["review"]["queue"]
    assert base["tray_filtered"]["count"] == 0 and base["tray_filtered"]["rules"] == []
    ex = store.export_case(conn, cid)                      # the REAL stored case (the first version of this assertion built the export from an empty dict and could not fail)
    out = export.build_export(ex)
    assert not {f["id"] for f in ex["flags"]} & set(ids)
    assert "Plan of care: 12 visits." not in out["letter_text"] and not any(q in json.dumps(out) for q in ("12 visits.\"; filtered",))
    assert "filtered" not in out["internal_notes_text"].lower()


def test_no_model_proposal_is_dropped_silently_counts_match(tmp_path):
    extra = [dict(type="causation", category="objective_negative", excerpt="Plan of care: 12 visits.")]
    conn, cid, v = _view(tmp_path, extra)
    rows = [r for r in present.all_items(conn, cid)["flag"] if r["state"] == "rejected" and r["reasons"][0] == "FILTERED_BY_RULE"]
    assert len(rows) == 1 == v["tray_filtered"]["count"]


# ---- T-126 round 2 (reviews/T-126-staff-engineer.md) ---------------------------------------------------------------------------------------------------------
NOT_IN_RECORD = "Patient was discharged after a fall from the roof."
NOWHERE = "Another quote nobody wrote."
STORED = [dict(type="causation", category="objective_negative", excerpt="Plan of care: 12 visits."),                    # rule-filtered, verbatim
          dict(type="causation", category="objective_negative", excerpt=NOT_IN_RECORD),                                 # rule-filtered AND not in the record
          dict(type="causation", category="degenerative_language", excerpt=NOWHERE),                                    # model-only, not in the record: grounding-rejected tray flag
          dict(type="causation", category="scene_facts", excerpt="Discharged from PT after two missed appointments.")]   # model-only scene_facts: LLM_ONLY tray flag


def _stored(tmp_path):
    return _view(tmp_path, STORED)[:2]


def _tray_flag_ids(conn, cid):
    rows = [r for r in DB.list_items(conn, cid, "flag") if r["state"] == "rejected"]
    return {r["id"] for r in rows if FT.is_filtered(r.get("state_reasons"))}, {r["id"] for r in rows if not FT.is_filtered(r.get("state_reasons"))}


def test_the_grounding_failure_stays_on_a_filtered_item_and_the_why_says_so():
    llm = [dict(type="causation", category="objective_negative", excerpt="This sentence is not in the record at all.")]
    (f,) = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": llm}}))
    assert f["reasons"][0] == FT.FILTERED and "GROUNDING_EXCERPT_NOT_VERBATIM" in f["reasons"] and "JUDGE_UNAVAILABLE" not in f["reasons"]
    assert "not word for word in the record" in f["why"]
    (g,) = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": [dict(llm[0], excerpt="Ankle exam normal.")]}}))
    assert g["reasons"] == [FT.FILTERED] and "word for word" not in g["why"]                           # a verbatim one has no such note


def test_every_tray_flag_stays_out_of_the_export_pending_count_and_notes(tmp_path):
    conn, cid = _stored(tmp_path)
    filtered, other = _tray_flag_ids(conn, cid)
    assert len(filtered) == 2 and len(other) >= 2, (filtered, other)         # filtered x2; the grounding-rejected and the scene_facts flag
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    ex = store.export_case(conn, cid)
    assert not {f["id"] for f in ex["flags"]} & (filtered | other)
    assert ex["pending_count"] == v["review"]["counts"]["pending"]            # the notes count is the UI count (was 24 against 23)
    out = export.build_export(ex)
    for q in (NOT_IN_RECORD, NOWHERE):                                         # a quote that is not in the record is never printed
        assert q not in out["internal_notes_text"] and q not in out["letter_text"]
    assert f"Items not reviewed: {v['review']['counts']['pending']}" in out["internal_notes_text"]


def test_tray_flags_are_not_counted_by_the_review_counts_the_gate_or_the_judge_rows(tmp_path):
    conn, cid = _stored(tmp_path)
    filtered, other = _tray_flag_ids(conn, cid)
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    assert not filtered & {t["id"] for t in v["tray"]} and not (filtered | other) & set(v["review"]["queue"])
    all_rejected = [r["id"] for k in ("entry", "amount", "flag") for r in DB.list_items(conn, cid, k) if r["state"] == "rejected"]
    assert v["review"]["counts"]["rejected"] == len([i for i in all_rejected if i not in filtered]) > 0     # filtered ones are not in the rejected count either
    assert not filtered & {j["item_id"] for j in trace._judge_rows(trace._Cx(conn, cid, True))}
    assert sum(p["items"] for p in trace.judge_report(conn, cid)["judges"]) == len(trace._judge_rows(trace._Cx(conn, cid, False)))
    t = trace.case_trace(conn, cid)
    gate = next(s for s in t["steps"] if s["id"] == "export_gate")
    assert gate["counts"]["pending_items"] == v["review"]["counts"]["pending"]
    live = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, cid, k) if not FT.is_filtered(r.get("state_reasons"))
            and not (r.get("ladder") or {}).get("failure")]
    grounding_step = next(s for s in t["steps"] if s["id"] == "grounding")
    assert grounding_step["counts"]["items_checked"] == len(live)               # a rule-filtered proposal is not an item the checks ran over
    assert grounding_step["counts"]["rejected"] == sum(1 for _, r in live if r["state"] == "rejected")
    assert gate["counts"]["rejected_not_blocking"] == grounding_step["counts"]["rejected"]
    assert not any(i in json.dumps(t) for i in filtered)


def test_one_helper_names_the_marker():
    assert FT.is_filtered(["FILTERED_BY_RULE", "GROUNDING_EXCERPT_NOT_VERBATIM"]) and not FT.is_filtered(["LLM_ONLY", "FILTERED_BY_RULE"]) and not FT.is_filtered(None)
    import pathlib
    lits = sorted(p.name for p in pathlib.Path("app/backend").glob("*.py") if '"FILTERED_BY_RULE"' in p.read_text())
    assert lits == ["confidence.py", "flag_templates.py", "why.py"], lits       # the code list, the constant, the reason sentence: no copy in a reader


def test_same_quote_different_category_keeps_one_flag_and_names_the_other_category():
    r = dict(R, excerpt="Patient reports prior neck pain. Ankle exam normal.")
    llm = [dict(type="pre_existing", category="prior_condition", excerpt="prior neck pain"),
           dict(type="pre_existing", category="degenerative_language", excerpt="prior neck pain"),
           dict(type="pre_existing", category="prior_condition", excerpt="prior neck pain")]            # the same category again: nothing to say
    out = [f for f in F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}})) if f["type"] == "pre_existing"]
    assert len(out) == 1 and out[0]["ladder"]["code_checks"]["merged_categories"] == ["degenerative_language"]
    lone = [f for f in F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm[:1]}})) if f["type"] == "pre_existing"]
    assert "merged_categories" not in lone[0]["ladder"]["code_checks"]


def test_the_merge_shows_in_the_item_trace(tmp_path):
    llm = [dict(type="causation", category="causation_language", excerpt="Discharged from PT after two missed appointments."),
           dict(type="causation", category="mechanism_language", excerpt="Discharged from PT after two missed appointments.")]
    conn, cid, _v = _view(tmp_path, llm)
    rows = [r for r in DB.list_items(conn, cid, "flag") if (r.get("ladder") or {}).get("code_checks", {}).get("merged_categories")]
    assert rows, "the stored flag keeps the merged category"
    tr = trace.item_trace(conn, cid, rows[0]["id"]) if hasattr(trace, "item_trace") else None
    assert tr is not None and any(s["id"] == "proposals_merged" for s in tr["steps"])
