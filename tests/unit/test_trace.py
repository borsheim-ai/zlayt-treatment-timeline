"""D-042 check traces (T-080): per-item stepper, case stepper with export gate, judge summary, and the full/metadata visibility split.
Fixture backend, no key. One recorded sample run is built once; each test works on its own copy of the database."""
import json
import pathlib
import sqlite3
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import trace, why
from app.backend.api import create_app
from app.db import db as DB

STATUSES = {"pass", "fail", "skipped", "pending"}
KINDS = {"code", "llm", "human"}
NEXT_CODES = {"DECIDE", "CONFIRM_DATE", "EDIT_SUMMARY", "EDIT_QUOTE", "READ_RECORD", "COMPARE_BY_HAND", "DISMISS_OR_ENTER_BY_HAND", "RERUN", "SENTENCE_REMOVED", "CONFIRM_RERUN", "RERUN_JUDGE"}
FULL_ONLY_KEYS = {"response_raw", "before", "after", "edited_text"}


def _without_amount_entries(db, tok):
    """T-139: the recorded sample's e2 and e4 quote an amount ('ER charges: $6,240.', 'Charge per visit $185.'), so the pipeline holds them (CHARGE_TEXT_IN_ENTRY).
    These tests exercise the check traces, not that hold (tests/unit/test_t139_charge_text.py does), so the shared case is shaped as a run whose answer had no amount
    sentence: the quote ends before it and code trims the summary clause, exactly what the paralegal's re-quote produces. Judge result and the rest of the ladder are as recorded."""
    from app.backend import charge_text
    conn = DB.connect(db)
    for e in DB.list_items(conn, tok, "entry"):
        if "CHARGE_TEXT_IN_ENTRY" not in (e.get("state_reasons") or []):
            continue
        exc = e["excerpt"]
        cut = min(i for i in (exc.find(x) for x in charge_text.currency_strings(exc)) if i >= 0)
        new_exc = exc[:exc.rfind(". ", 0, cut) + 1]
        lad = e["ladder"]
        lad["state"] = "verified"
        DB.update_item(conn, e["id"], case=tok, excerpt=new_exc, excerpt_end=e["excerpt_start"] + len(new_exc), summary=charge_text.trim_summary(e["summary"])["text"],
                       state="verified", state_reasons_json=[], ladder=lad)
    conn.close()


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    import os
    d = tmp_path_factory.mktemp("trace")
    old = {k: os.environ.get(k) for k in ("LLM_BACKEND", "ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY")}
    os.environ["LLM_BACKEND"] = "fixture"
    for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        os.environ.pop(k, None)
    db = str(d / "base.sqlite")
    c = TestClient(create_app(db, static_dir=str(d)), client=("127.0.0.1", 50000))
    pre = c.post("/api/cases", json={"sample": True}).json()["token"]          # an ingested case that never ran
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready"
    _without_amount_entries(db, tok)
    yield {"dir": d, "db": db, "tok": tok, "pre": pre}
    for k, v in old.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


@pytest.fixture
def env(base, tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    path = str(tmp_path / "copy.sqlite")
    src = sqlite3.connect(base["db"])
    dst = sqlite3.connect(path)
    src.backup(dst)
    src.close()
    dst.close()
    conn = DB.connect(path)
    c = TestClient(create_app(path, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    return c, conn, base["tok"], base["pre"]


def steps_of(t):
    return {s["id"]: s for s in t["steps"]}


def walk(o, keys):
    """Every dict key anywhere in o that is in `keys`."""
    found = set()
    if isinstance(o, dict):
        for k, v in o.items():
            if k in keys:
                found.add(k)
            found |= walk(v, keys)
    elif isinstance(o, list):
        for v in o:
            found |= walk(v, keys)
    return found


def all_keys(o, skip=()):
    """Every dict key in o, not looking inside the values of keys in `skip`."""
    out = set()
    if isinstance(o, dict):
        for k, v in o.items():
            out.add(k)
            if k not in skip:
                out |= all_keys(v, skip)
    elif isinstance(o, list):
        for v in o:
            out |= all_keys(v, skip)
    return out


def check_step_shape(s):
    assert {"id", "n", "label", "kind", "status", "why", "reason_code", "rule", "blocks_export", "evidence", "next_action"} <= set(s)
    assert s["kind"] in KINDS and s["status"] in STATUSES and s["why"] and s["label"]
    if s["status"] in ("fail", "pending"):
        assert s["next_action"] and s["next_action"]["code"] in NEXT_CODES and s["next_action"]["text"], s["id"]
    else:
        assert s["next_action"] is None
    if s["reason_code"]:
        assert trace.reason_text(s["reason_code"]) != s["reason_code"] or s["reason_code"] in trace.narrative.REASONS, s["reason_code"]


# ------------------------------------------------------------------ AC1: per-item ladder
def test_every_item_has_an_ordered_well_formed_trace(env):
    c, conn, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    ids = [x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k]]
    assert len(ids) >= 20
    for iid in ids:
        r = c.get(f"/api/cases/{tok}/items/{iid}/trace")
        assert r.status_code == 200, iid
        t = r.json()
        assert t["item_id"] == iid and t["mode"] == "metadata" and t["kind"] in ("entry", "amount", "flag")
        assert [s["n"] for s in t["steps"]] == list(range(1, len(t["steps"]) + 1))
        assert t["steps"][-1]["id"] == "human" and t["steps"][-1]["kind"] == "human"
        for s in t["steps"]:
            check_step_shape(s)
        assert t["progress"]["total"] == len(t["steps"]) and t["progress"]["done"] == sum(1 for s in t["steps"] if s["status"] != "pending")
        for rs in t["state_reasons"]:
            assert rs["why"] and rs["code"]


def test_entry_trace_names_each_code_check_and_the_judge(env):
    c, _, tok, _ = env
    t = c.get(f"/api/cases/{tok}/items/e2/trace").json()
    assert [s["id"] for s in t["steps"]] == ["extracted", "excerpt_narrowed", "charge_clause_removed", "excerpt_verbatim", "excerpt_whole_sentence", "excerpt_hedge", "summary_tokens", "summary_qualifier",
                                            "highlight", "date_confirmed", "injection_scan", "judge_1", "human"]
    s = steps_of(t)
    assert s["extracted"]["kind"] == "llm" and s["extracted"]["evidence"]["model"]["id"] and s["extracted"]["evidence"]["prompt_version"] == "extract_v1"
    assert s["extracted"]["evidence"]["call_id"] and s["extracted"]["evidence"]["excerpt"]["text"]
    assert s["summary_tokens"]["rule"] == "D-034" and s["summary_qualifier"]["rule"] == "D-022" and s["date_confirmed"]["rule"] == "D-041"
    j = s["judge_1"]
    assert j["kind"] == "llm" and j["status"] == "pass" and j["evidence"]["model"]["independent_of_generator"] is True
    assert j["evidence"]["prompt_version"] == "judge_faithfulness_v1" and j["evidence"]["judge_verdict"] == "supported" and j["evidence"]["rationale"]
    assert s["human"]["status"] == "pending" and s["human"]["blocks_export"] is True and s["human"]["next_action"]["code"] == "DECIDE"
    assert t["verdict"] == {"code": "ready_for_decision", "label": "Ready for your decision", "blocks_export": True}


def test_judge_objection_is_a_fail_with_fixed_rationale(env):
    c, conn, tok, _ = env
    e = DB.get_item(conn, "e2", tok)
    lad = e["ladder"]
    lad["judge"].update(verdict="partially", reason_code="DROPS_QUALIFIER")
    DB.update_item(conn, "e2", case=tok, state="needs_review", state_reasons_json=["JUDGE_PARTIAL"], ladder=lad)
    t = c.get(f"/api/cases/{tok}/items/e2/trace").json()
    j = steps_of(t)["judge_1"]
    assert j["status"] == "fail" and j["reason_code"] == "JUDGE_PARTIAL" and j["evidence"]["judge_reason_code"] == "DROPS_QUALIFIER"
    assert j["evidence"]["rationale"] == why.judge_detail("DROPS_QUALIFIER") and why.judge_detail("DROPS_QUALIFIER") in j["why"]
    assert j["next_action"]["code"] == "COMPARE_BY_HAND"
    assert t["verdict"]["code"] == "needs_attention" and t["state_reasons"] == [{"code": "JUDGE_PARTIAL", "why": why.why("JUDGE_PARTIAL"), "step_id": "judge_1"}]
    assert t["next_action"]["code"] == "COMPARE_BY_HAND"


def test_rejected_entry_skips_later_checks_and_points_to_manual_entry(env):
    c, conn, tok, _ = env
    e = DB.get_item(conn, "e3", tok)
    lad = e["ladder"]
    lad["code_checks"]["excerpt_verbatim"] = False
    DB.update_item(conn, "e3", case=tok, state="rejected", state_reasons_json=["GROUNDING_EXCERPT_NOT_VERBATIM"], ladder=lad)
    t = c.get(f"/api/cases/{tok}/items/e3/trace").json()
    s = steps_of(t)
    assert s["excerpt_verbatim"]["status"] == "fail" and s["excerpt_verbatim"]["reason_code"] == "GROUNDING_EXCERPT_NOT_VERBATIM"
    for sid in ("excerpt_whole_sentence", "excerpt_hedge", "summary_tokens", "summary_qualifier", "highlight", "judge_1"):
        assert s[sid]["status"] == "skipped" and s[sid]["reason_code"] == "GROUNDING_EXCERPT_NOT_VERBATIM", sid
    assert s["human"]["status"] == "pending" and s["human"]["blocks_export"] is False and s["human"]["next_action"]["code"] == "DISMISS_OR_ENTER_BY_HAND"
    assert t["verdict"] == {"code": "rejected", "label": "Rejected; kept out of the letter", "blocks_export": False}


def test_token_and_qualifier_failures_name_the_rule(env):
    c, conn, tok, _ = env
    e = DB.get_item(conn, "e4", tok)
    lad = e["ladder"]
    lad["code_checks"]["summary_tokens_not_in_excerpt"] = ["9,000"]
    DB.update_item(conn, "e4", case=tok, state="needs_review", state_reasons_json=["SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER"], ladder=lad)
    s = steps_of(c.get(f"/api/cases/{tok}/items/e4/trace").json())
    assert s["summary_tokens"]["status"] == "fail" and s["summary_tokens"]["evidence"]["tokens"] == ["9,000"] and s["summary_tokens"]["next_action"]["code"] == "EDIT_SUMMARY"
    assert s["summary_qualifier"]["status"] == "fail" and s["summary_qualifier"]["reason_code"] == "SUMMARY_DROPS_QUALIFIER"
    assert s["excerpt_verbatim"]["status"] == "pass"


def test_unconfirmed_date_fails_and_blocks_accept_d041(env):
    c, conn, tok, _ = env
    rid = DB.get_item(conn, "e5", tok)["record_ids"][0]
    conn.execute("UPDATE records SET date_status='ambiguous', date_candidates_json=? WHERE id=? AND case_id=?", (json.dumps(["2026-04-05", "2026-05-04"]), rid, tok))
    t = c.get(f"/api/cases/{tok}/items/e5/trace").json()
    d = steps_of(t)["date_confirmed"]
    assert d["status"] == "fail" and d["reason_code"] == "DATE_AMBIGUOUS" and d["blocks_export"] is True
    assert d["next_action"]["code"] == "CONFIRM_DATE" and d["next_action"]["target"]["record_id"] == rid
    assert d["evidence"]["date"]["candidates"] == ["2026-04-05", "2026-05-04"]
    assert steps_of(t)["human"]["next_action"]["code"] == "CONFIRM_DATE"
    assert c.post(f"/api/cases/{tok}/items/e5/review", json={"action": "accept"}).json()["error"]["code"] == "DATE_UNCONFIRMED"   # the trace and the rule agree


def test_unavailable_judge_is_skipped_with_reason(env):
    c, conn, tok, _ = env
    e = DB.get_item(conn, "e6", tok)
    lad = e["ladder"]
    lad["judge"] = {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": None, "verdict": "unavailable", "reason_code": "NONE"}
    DB.update_item(conn, "e6", case=tok, state="needs_review", state_reasons_json=["JUDGE_UNAVAILABLE"], ladder=lad)
    t = c.get(f"/api/cases/{tok}/items/e6/trace").json()
    j = steps_of(t)["judge_1"]
    assert j["status"] == "skipped" and j["reason_code"] == "JUDGE_UNAVAILABLE" and j["next_action"]["code"] == "RERUN_JUDGE"
    assert t["verdict"]["code"] == "needs_attention"


def test_amount_steps_and_rate_is_never_totaled(env):
    c, _, tok, _ = env
    amounts = c.get(f"/api/cases/{tok}").json()["amounts"]
    charge = next(a for a in amounts if a["kind"] == "charge")
    rate = next(a for a in amounts if a["kind"] == "rate")
    t = c.get(f"/api/cases/{tok}/items/{charge['id']}/trace").json()
    assert [s["id"] for s in t["steps"]] == ["found_in_text", "amount_class", "injection_scan", "judge_2", "total_inclusion", "human"]
    s = steps_of(t)
    assert s["found_in_text"]["evidence"]["values"]["value_cents"] == charge["value_cents"] and s["amount_class"]["status"] == "pass"
    assert s["total_inclusion"]["status"] == "pending"
    c.post(f"/api/cases/{tok}/items/{charge['id']}/review", json={"action": "accept"})
    s = steps_of(c.get(f"/api/cases/{tok}/items/{charge['id']}/trace").json())
    assert s["total_inclusion"]["status"] == "pass" and s["human"]["status"] == "pass"
    r = steps_of(c.get(f"/api/cases/{tok}/items/{rate['id']}/trace").json())
    assert r["amount_class"]["reason_code"] == "AMOUNT_RATE_NOT_TOTALED" and r["total_inclusion"]["status"] == "skipped"


def test_amount_judge_reason_is_read_from_the_audited_call_when_not_stored(env):
    """Amounts stored before ladder.judge.reason_code existed: the closed code comes from the call's answer, still a fixed sentence."""
    c, conn, tok, _ = env
    a = next(x for x in c.get(f"/api/cases/{tok}").json()["amounts"] if x["kind"] == "charge")
    row = DB.get_item(conn, a["id"], tok)
    lad = row["ladder"]
    cid = lad["judge"]["call_id"]
    lad["judge"].pop("reason_code", None)
    lad["judge"]["verdict"] = "disagree"
    DB.update_item(conn, a["id"], case=tok, state="needs_review", state_reasons_json=["JUDGE_DISAGREES"], ladder=lad)
    conn.execute("UPDATE llm_calls SET response_raw=? WHERE id=?", (json.dumps({"verdict": "disagree", "reason_code": "SHOULD_BE_RATE"}), cid))
    j = steps_of(c.get(f"/api/cases/{tok}/items/{a['id']}/trace").json())["judge_2"]
    assert j["status"] == "fail" and j["evidence"]["judge_reason_code"] == "SHOULD_BE_RATE" and j["evidence"]["rationale"] == why.judge_detail("SHOULD_BE_RATE")
    rep = c.get(f"/api/cases/{tok}/judges").json()
    d = next(x for x in rep["disagreements"] if x["item_id"] == a["id"])
    assert d["type"] == "judge_objects" and d["code_says"] == "charge" and "SHOULD_BE_RATE" in d["judge_says"]


def test_code_made_flags_need_no_judge(env):
    c, _, tok, _ = env
    t = c.get(f"/api/cases/{tok}/items/f_gap_r6_r7/trace").json()
    assert [s["id"] for s in t["steps"]] == ["computed", "spans_match", "endpoints_confirmed", "injection_scan", "judge_not_needed", "human"]
    s = steps_of(t)
    assert s["computed"]["evidence"]["values"]["days"] == 73 and s["judge_not_needed"]["status"] == "skipped" and s["computed"]["kind"] == "code"


def test_ai_and_phrase_list_flags_show_agreement_and_judge(env):
    c, _, tok, _ = env
    flags = c.get(f"/api/cases/{tok}").json()["flags"]
    both = next(f for f in flags if f["origin"] == "lexicon+llm")
    s = steps_of(c.get(f"/api/cases/{tok}/items/{both['id']}/trace").json())
    assert s["proposed_by_phrase_list"]["status"] == "pass" and s["proposed_by_ai"]["status"] == "pass" and s["agreement"]["status"] == "pass"
    assert s["judge_4"]["kind"] == "llm" and s["judge_4"]["status"] == "pass"


def test_lexicon_only_flag_is_agreement_fail_and_judge_skipped(env):
    c, conn, tok, _ = env
    f = next(x for x in c.get(f"/api/cases/{tok}").json()["flags"] if x["origin"] == "lexicon+llm")
    row = DB.get_item(conn, f["id"], tok)
    lad = row["ladder"]
    lad["judge"] = None
    DB.update_item(conn, f["id"], case=tok, origin="lexicon", state="needs_review", state_reasons_json=["LEXICON_ONLY"], ladder=lad)
    s = steps_of(c.get(f"/api/cases/{tok}/items/{f['id']}/trace").json())
    assert s["proposed_by_ai"]["status"] == "skipped" and s["proposed_by_ai"]["reason_code"] == "LEXICON_ONLY"
    assert s["agreement"]["status"] == "fail" and s["agreement"]["reason_code"] == "LEXICON_ONLY"
    assert s["judge_4"]["status"] == "skipped" and s["judge_4"]["reason_code"] == "LEXICON_ONLY"


def test_unknown_item_and_case_are_404(env):
    c, _, tok, _ = env
    assert c.get(f"/api/cases/{tok}/items/e999/trace").status_code == 404
    assert c.get(f"/api/cases/{tok}/items/zzz/trace").status_code == 404
    assert c.get("/api/cases/nope/trace").status_code == 404 and c.get("/api/cases/nope/judges").status_code == 404
    assert c.get(f"/api/cases/{tok}/items/ns1/trace").status_code == 404


def test_unrun_case_waits_for_the_ai(env):
    c, _, _, pre = env
    ct = c.get(f"/api/cases/{pre}/trace").json()
    s = steps_of(ct)
    assert s["extract"]["status"] == "pending" and s["extract"]["next_action"]["code"] == "RERUN" and s["judges"]["status"] == "pending"
    amt = c.get(f"/api/cases/{pre}").json()["amounts"][0]
    t = c.get(f"/api/cases/{pre}/items/{amt['id']}/trace").json()
    assert steps_of(t)["judge_2"]["status"] == "pending" and t["verdict"]["code"] == "waiting_for_run"


# ------------------------------------------------------------------ narrative sentences
def test_narrative_sentence_traces(env):
    c, conn, tok, _ = env
    nar = {"status": "pending", "generator": {"model": "claude-sonnet-5-5", "prompt_version": "narrative_v1", "call_id": None},
           "sentences": [{"id": "ns1", "entry_id": "e1", "text": "Jordan was seen.", "code_checks": {"reasons": []},
                          "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": None, "verdict": "supported", "reason_code": "NONE"}}],
           "removed": [{"id": "ns2", "entry_id": "e2", "text": "It caused chronic pain.", "code_checks": {"reasons": ["CAUSATION_NOT_QUOTED"]}, "reason": "CAUSATION_NOT_QUOTED",
                        "reasons": ["CAUSATION_NOT_QUOTED"]},
                       {"id": "ns3", "entry_id": "e3", "text": "A thing.", "code_checks": {"reasons": []}, "reason": "JUDGE_PARTIAL",
                        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": None, "verdict": "partially", "reason_code": "NUMBER_MISMATCH"}}]}
    case = DB.get_case(conn, tok)
    cfg = dict(case.get("config") or {})
    cfg["narrative"] = nar
    DB.update_case(conn, tok, config_json=cfg)
    k = steps_of(c.get(f"/api/cases/{tok}/items/ns1/trace").json())
    assert [s for s in k] == ["extracted", "cites_accepted_entry", "sentence_checks", "judge_1", "human"] and k["judge_1"]["status"] == "pass" and k["human"]["status"] == "pending"
    t2 = c.get(f"/api/cases/{tok}/items/ns2/trace").json()
    s2 = steps_of(t2)
    assert t2["kind"] == "narrative_sentence" and t2["verdict"]["code"] == "removed" and s2["sentence_checks"]["status"] == "fail"
    assert s2["sentence_checks"]["reason_code"] == "CAUSATION_NOT_QUOTED" and s2["judge_1"]["status"] == "skipped" and s2["human"]["status"] == "skipped"
    s3 = steps_of(c.get(f"/api/cases/{tok}/items/ns3/trace").json())
    assert s3["sentence_checks"]["status"] == "pass" and s3["judge_1"]["status"] == "fail" and s3["judge_1"]["reason_code"] == "JUDGE_PARTIAL"
    assert s3["judge_1"]["evidence"]["rationale"] == why.judge_detail("NUMBER_MISMATCH")
    for t in (t2,):
        for s in t["steps"]:
            check_step_shape(s)


# ------------------------------------------------------------------ AC2: case trace and export gate
def test_case_trace_steps_and_counts(env):
    c, _, tok, _ = env
    ct = c.get(f"/api/cases/{tok}/trace").json()
    assert [s["id"] for s in ct["steps"]] == ["ingest", "split", "dates", "extract", "grounding", "judges", "flags", "totals", "review", "export_gate"]
    for s in ct["steps"]:
        check_step_shape(s)
        assert isinstance(s["counts"], dict)
    s = steps_of(ct)
    assert s["ingest"]["counts"]["records"] == 9 and s["extract"]["counts"] == {"records_to_draft": 9, "entries": 9, "rejected": 0, "records_without_entry": 0}
    assert s["judges"]["counts"]["items_judged"] == 20 and s["flags"]["counts"]["by_type"]["gap"] == 1 and s["review"]["counts"]["pending"] == 23
    assert s["totals"]["counts"]["pending_cents"] == 839000 and s["totals"]["status"] == "pending"
    assert ct["progress"]["total"] == 10


def test_pending_live_items_are_a_warning_not_a_blocker_d045(env):
    c, conn, tok, _ = env
    e = DB.get_item(conn, "e3", tok)
    DB.update_item(conn, "e3", case=tok, state="rejected", state_reasons_json=["GROUNDING_EXCERPT_NOT_VERBATIM"], ladder=e["ladder"])
    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
    c.post(f"/api/cases/{tok}/items/e2/review", json={"action": "dismiss"})
    case = c.get(f"/api/cases/{tok}").json()
    gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
    expected = {x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k] if x["review_status"] == "pending"}
    assert expected == set(case["review"]["queue"])
    assert "e3" not in expected and "e1" not in expected and "e2" not in expected and expected
    assert gate["blockers"] == [] and gate["ready"] is True and gate["status"] == "pass" and gate["counts"]["rejected_not_blocking"] == 1
    assert gate["counts"]["pending_items"] == len(expected) and gate["counts"]["blocking"] == 0
    w, = gate["warnings"]
    assert w["reason_code"] == "ITEMS_NOT_REVIEWED" and w["count"] == len(expected) and w["next_action"]["code"] == "DECIDE"
    assert "will not be in the letter" in w["why"] and "AI disclosure line will count" in w["why"]
    assert c.get(f"/api/cases/{tok}/export").status_code == 200
    notes = c.get(f"/api/cases/{tok}/export").json()["internal_notes_text"]
    assert f"Items not reviewed: {len(expected)}" in notes
    assert c.get(f"/api/cases/{tok}/trace").json()["verdict"]["code"] == "ready"


def test_export_gate_date_unconfirmed_blocker(env):
    c, conn, tok, _ = env
    rid = DB.get_item(conn, "e5", tok)["record_ids"][0]
    conn.execute("UPDATE records SET date_status='ambiguous', date_candidates_json=? WHERE id=? AND case_id=?", (json.dumps(["2026-04-05", "2026-05-04"]), rid, tok))
    gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
    assert all(x["item_id"] != "e5" for x in gate["blockers"]) and gate["counts"]["date_unconfirmed"] == 1       # D-045(a): pending, so it warns; accepting it is refused (D-041)
    assert [x["reason_code"] for x in gate["blockers"]] == ["NOTHING_ACCEPTED"] and gate["warnings"][0]["count"] >= 1
    assert steps_of(c.get(f"/api/cases/{tok}/trace").json())["dates"]["status"] == "fail"


def test_export_gate_ready_matches_review_view(env):
    c, _, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        assert c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"}).status_code == 200
    ct = c.get(f"/api/cases/{tok}/trace").json()
    gate = steps_of(ct)["export_gate"]
    assert gate["ready"] is True and gate["blockers"] == [] and gate["status"] == "pass" and ct["verdict"]["code"] == "ready"
    assert c.get(f"/api/cases/{tok}").json()["review"]["ready_to_export"] is True


def test_export_gate_nothing_accepted(env):
    c, _, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "dismiss"})
    gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
    assert gate["ready"] is False and [b["reason_code"] for b in gate["blockers"]] == ["NOTHING_ACCEPTED"]


def test_run_in_progress_blocks_the_gate(env):
    c, conn, tok, _ = env
    DB.update_case(conn, tok, status="running")
    ct = c.get(f"/api/cases/{tok}/trace").json()
    gate = steps_of(ct)["export_gate"]
    assert gate["ready"] is False and "RUN_IN_PROGRESS" in [b["reason_code"] for b in gate["blockers"]] and ct["verdict"]["code"] == "running"


# ------------------------------------------------------------------ judge summary
def test_judge_summary_counts_and_objections(env):
    c, conn, tok, _ = env
    rep = c.get(f"/api/cases/{tok}/judges").json()
    assert rep["totals"] == {"items_judged": 20, "supported": 20, "unsupported": 0, "unsure": 0, "unavailable": 0, "human_overrides": 0}
    assert rep["models"]["judge"] == "claude-haiku-5-5" and rep["independent_models"] is True
    assert {j["id"] for j in rep["judges"]} == {"j1", "j2", "j3", "j4"} and rep["rejections"] == [] and rep["unresolved"] == []
    assert "judge_faithfulness_v1" in rep["prompt_versions"]
    e = DB.get_item(conn, "e2", tok)
    lad = e["ladder"]
    lad["judge"].update(verdict="unsupported", reason_code="ADDS_DIAGNOSIS")
    DB.update_item(conn, "e2", case=tok, state="needs_review", state_reasons_json=["JUDGE_UNSUPPORTED"], ladder=lad)
    e6 = DB.get_item(conn, "e6", tok)
    l6 = e6["ladder"]
    l6["judge"] = {"model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": None, "verdict": "unavailable", "reason_code": "NONE"}
    DB.update_item(conn, "e6", case=tok, state="needs_review", state_reasons_json=["JUDGE_UNAVAILABLE"], ladder=l6)
    c.post(f"/api/cases/{tok}/items/e2/review", json={"action": "accept", "compared": True})      # D-066: the second check disputed it, so her accept says she compared
    rep = c.get(f"/api/cases/{tok}/judges").json()
    assert rep["totals"]["unsupported"] == 1 and rep["totals"]["unavailable"] == 1 and rep["totals"]["items_judged"] == 19 and rep["totals"]["human_overrides"] == 1
    r = rep["rejections"][0]
    assert r["item_id"] == "e2" and r["judge"] == "j1" and r["verdict"] == "unsupported" and r["reason_code"] == "ADDS_DIAGNOSIS" and r["rationale"] == why.judge_detail("ADDS_DIAGNOSIS")
    assert r["model"] == "claude-haiku-5-5" and r["prompt_version"] == "judge_faithfulness_v1" and r["state_reason"] == "JUDGE_UNSUPPORTED" and r["review_status"] == "accepted"
    assert rep["unresolved"][0]["item_id"] == "e6" and rep["unresolved"][0]["verdict"] == "unavailable"
    assert any(d["item_id"] == "e2" and d["type"] == "judge_objects" and d["code_says"] == "All code checks passed." for d in rep["disagreements"])
    ct = steps_of(c.get(f"/api/cases/{tok}/trace").json())["judges"]
    assert ct["status"] == "fail" and ct["reason_code"] == "JUDGE_UNAVAILABLE" and ct["counts"]["unavailable"] == 1


def test_code_flags_doubt_judge_agrees_and_sources_disagree(env):
    c, conn, tok, _ = env
    e = DB.get_item(conn, "e4", tok)
    DB.update_item(conn, "e4", case=tok, state="needs_review", state_reasons_json=["SUMMARY_DROPS_QUALIFIER"], ladder=e["ladder"])
    f = next(x for x in c.get(f"/api/cases/{tok}").json()["flags"] if x["origin"] == "lexicon+llm")
    DB.update_item(conn, f["id"], case=tok, state="needs_review", state_reasons_json=["LLM_ONLY"])
    types = {(d["item_id"], d["type"]) for d in c.get(f"/api/cases/{tok}/judges").json()["disagreements"]}
    assert ("e4", "judge_agrees_code_flags") in types and (f["id"], "sources_disagree") in types


# ------------------------------------------------------------------ visibility split (D-020 / D-036)
def test_metadata_mode_has_no_raw_answers_or_edit_text_and_local_mode_only_adds_them(env, monkeypatch):
    c, _, tok, _ = env
    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
    fid = next(x["id"] for x in c.get(f"/api/cases/{tok}").json()["flags"] if x["origin"] != "code")
    assert c.post(f"/api/cases/{tok}/items/{fid}/review", json={"action": "edit", "edits": {"note": "Ask the client about 2023."}}).status_code == 200
    urls = [f"/api/cases/{tok}/items/{i}/trace" for i in ("e1", "e2", "a1", fid, "f_gap_r6_r7")] + [f"/api/cases/{tok}/trace", f"/api/cases/{tok}/judges"]
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    pub = {u: c.get(u).json() for u in urls}
    monkeypatch.setenv("ZLAYT_MODE", "local")
    loc = {u: c.get(u).json() for u in urls}
    for u in urls:
        assert pub[u]["mode"] == "metadata" and loc[u]["mode"] == "full"
        assert not walk(pub[u], FULL_ONLY_KEYS | {"system_text", "user_text"}), u
        assert not walk(loc[u], {"system_text", "user_text"}), u                      # prompts never travel in a trace
        assert all_keys(loc[u], FULL_ONLY_KEYS) - all_keys(pub[u]) <= FULL_ONLY_KEYS | {"mode"}, u    # full adds only the full-only keys
    assert "Ask the client about 2023." not in json.dumps(pub[urls[3]]) and "Ask the client about 2023." in json.dumps(loc[urls[3]])
    assert walk(loc[urls[0]], {"before", "after"}) == {"before", "after"} and walk(loc[urls[0]], {"response_raw"}) == {"response_raw"}
    assert "<<<RECORD" not in json.dumps(loc[urls[0]]) and "You read one medical record" not in json.dumps(loc[urls[0]])
    human = steps_of(pub[urls[0]])["human"]["evidence"]
    assert human["action"] == "accept" and human["at"] and [e["action"] for e in human["events"]] == ["accept"]


def test_judge_report_rejection_response_raw_is_full_mode_only(env, monkeypatch):
    c, conn, tok, _ = env
    e = DB.get_item(conn, "e2", tok)
    lad = e["ladder"]
    lad["judge"].update(verdict="partially", reason_code="DROPS_QUALIFIER")
    DB.update_item(conn, "e2", case=tok, state="needs_review", state_reasons_json=["JUDGE_PARTIAL"], ladder=lad)
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    assert "response_raw" not in c.get(f"/api/cases/{tok}/judges").json()["rejections"][0]
    monkeypatch.setenv("ZLAYT_MODE", "local")
    assert "response_raw" in c.get(f"/api/cases/{tok}/judges").json()["rejections"][0]


def test_every_emitted_reason_code_has_a_fixed_sentence(env):
    c, conn, tok, pre = env
    codes = set()
    for t in (tok, pre):
        ct = c.get(f"/api/cases/{t}/trace").json()
        for s in ct["steps"]:
            codes.add(s["reason_code"])
            codes |= {b["reason_code"] for b in s.get("blockers", [])}
        for k in ("entries", "amounts", "flags"):
            for x in c.get(f"/api/cases/{t}").json()[k]:
                it = c.get(f"/api/cases/{t}/items/{x['id']}/trace").json()
                codes |= {s["reason_code"] for s in it["steps"]} | {r["code"] for r in it["state_reasons"]}
    for code in codes - {None}:
        assert trace.reason_text(code) != code, code


def test_judge_reason_code_is_persisted_on_new_runs(env):
    """The run keeps the judge's closed reason code with the verdict (no db change: it lives in ladder_json)."""
    _, conn, tok, _ = env
    for kind in ("entry", "amount"):
        judged = [r for r in DB.list_items(conn, tok, kind) if (r["ladder"] or {}).get("judge")]
        assert judged and all("reason_code" in r["ladder"]["judge"] for r in judged), kind


# ------------------------------------------------------------------ round 2 (staff-engineer review): a gate never passes over a failure or a check that did not run
def _blank_judges(conn, tok):
    """Make the judge stage 'never ran' on every entry and every non-damages amount (the run deadline case in pipeline.py)."""
    n = 0
    for kind in ("entry", "amount"):
        for row in DB.list_items(conn, tok, kind):
            if row["state"] == "rejected" or (kind == "amount" and row["kind"] == "damages"):
                continue
            if kind == "entry" and row["id"] in ("e2", "e4"):       # T-139: shaped by _without_amount_entries, so no recorded second-check answer exists for their text; they keep the recorded verdict
                continue
            lad = row["ladder"]
            if not lad.get("judge"):
                continue
            lad["judge"] = None
            DB.update_item(conn, row["id"], case=tok, state="needs_review", state_reasons_json=sorted(set(row["state_reasons"]) | {"JUDGE_UNAVAILABLE"}), ladder=lad)
            conn.execute("DELETE FROM llm_calls WHERE case_id=? AND item_id=? AND step IN ('j1','j2','j3','j4')", (tok, row["id"]))     # no audited judge call either
            n += 1
    return n


def test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step(env):
    c, conn, tok, _ = env
    before = c.get(f"/api/cases/{tok}/judges").json()["totals"]
    n = _blank_judges(conn, tok)
    assert n >= 5
    rep = c.get(f"/api/cases/{tok}/judges").json()
    case = c.get(f"/api/cases/{tok}").json()
    skipped = 0
    for x in [*case["entries"], *case["undated_entries"], *case["amounts"], *case["flags"]]:
        t = c.get(f"/api/cases/{tok}/items/{x['id']}/trace").json()
        skipped += sum(1 for s in t["steps"] if s["id"].startswith("judge_") and s["status"] == "skipped" and s["reason_code"] == "JUDGE_UNAVAILABLE")
    assert skipped == n == rep["totals"]["unavailable"]                       # item traces and /judges reconcile
    assert rep["totals"]["items_judged"] == before["items_judged"] - n
    assert len(rep["unresolved"]) == n and {u["state_reason"] for u in rep["unresolved"]} == {"JUDGE_UNAVAILABLE"}
    assert sum(j["unavailable"] for j in rep["judges"]) == n
    j = steps_of(c.get(f"/api/cases/{tok}/trace").json())["judges"]
    assert j["status"] == "fail" and j["reason_code"] == "JUDGE_UNAVAILABLE" and j["counts"]["unavailable"] == n and "agreed" not in j["why"]
    assert str(n) in j["why"] and j["next_action"]["code"] == "RERUN_JUDGE"


def test_judges_step_is_pending_not_pass_while_the_run_is_going_and_judges_are_missing(env):
    c, conn, tok, _ = env
    n = _blank_judges(conn, tok)
    DB.update_case(conn, tok, status="running")
    j = steps_of(c.get(f"/api/cases/{tok}/trace").json())["judges"]
    assert j["status"] == "pending" and j["counts"]["unavailable"] == n and "agreed" not in j["why"]


def _gate_states(c, conn, tok):
    """Yield (name) after putting the case into each state we can build; the caller checks the invariant."""
    case = c.get(f"/api/cases/{tok}").json()
    ids = [x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k]]
    yield "pending items"
    DB.update_case(conn, tok, status="running")
    yield "running with pending items"
    DB.update_case(conn, tok, status="ready")
    for i in ids:
        c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "dismiss"})
    yield "everything dismissed"
    DB.update_case(conn, tok, status="failed")
    yield "failed, everything dismissed"
    DB.update_case(conn, tok, status="ready")
    # accept every item still reviewable
    for i in ids:
        c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept"})
    yield "all accepted"
    DB.update_case(conn, tok, status="running")
    yield "all accepted, running"
    DB.update_case(conn, tok, status="failed")
    yield "all accepted, failed"


def test_gate_ready_equals_no_blockers_in_every_case_state(env):
    c, conn, tok, pre = env
    seen = {}
    for name in _gate_states(c, conn, tok):
        gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
        assert gate["ready"] == (len(gate["blockers"]) == 0), name
        assert gate["status"] == ("pass" if gate["ready"] else "fail"), name
        if not gate["ready"]:
            assert gate["next_action"] is not None or "running" in name, name
        seen[name] = gate
    assert seen["all accepted"]["ready"] is True
    for name in ("all accepted, failed", "failed, everything dismissed"):
        assert seen[name]["ready"] is False and "RUN_FAILED" in [b["reason_code"] for b in seen[name]["blockers"]], name
    assert seen["all accepted, running"]["ready"] is False and "RUN_IN_PROGRESS" in [b["reason_code"] for b in seen["all accepted, running"]["blockers"]]
    g = steps_of(c.get(f"/api/cases/{pre}/trace").json())["export_gate"]            # a case that never ran
    assert g["ready"] == (g["blockers"] == []) and g["status"] == ("pass" if g["ready"] else "fail")


def test_failed_run_with_everything_accepted_is_not_ready_and_verdict_failed(env):
    c, conn, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
    DB.update_case(conn, tok, status="failed")
    ct = c.get(f"/api/cases/{tok}/trace").json()
    gate = steps_of(ct)["export_gate"]
    assert ct["verdict"]["code"] == "failed" and gate["ready"] is False and gate["status"] == "fail" and gate["reason_code"] == "RUN_FAILED"
    assert [b["reason_code"] for b in gate["blockers"]] == ["RUN_FAILED"] and gate["next_action"]["code"] == "CONFIRM_RERUN"


def test_all_accepted_but_run_in_progress_is_not_ready(env):
    c, conn, tok, _ = env
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
    DB.update_case(conn, tok, status="running")
    gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
    assert gate["ready"] is False and gate["status"] == "fail" and [b["reason_code"] for b in gate["blockers"]] == ["RUN_IN_PROGRESS"]


def _add_record_warning(conn, tok, category, rid_from="e1"):
    src = conn.execute("SELECT * FROM flags WHERE case_id=? LIMIT 1", (tok,)).fetchone()
    row = {k: src[k] for k in src.keys() if k not in ("review_status", "edited_json", "updated_at")}
    ent = DB.get_item(conn, rid_from, tok)
    row.update(id=f"f_{category}_t", type="record_warning", category=category, origin="code", state="needs_review", ladder_json=json.dumps({}),
               state_reasons_json=json.dumps({"date_ambiguous": ["DATE_AMBIGUOUS"], "injection_suspected": ["INJECTION_SUSPECTED"]}[category]),
               evidence_json=json.dumps([{"record_id": ent["record_ids"][0], "excerpt": "x", "start": 0, "end": 1}]))
    DB.add_item(conn, tok, "flag", row)
    return row["id"]


def test_record_warning_flags_point_at_the_right_action_and_a_real_step(env):
    c, conn, tok, _ = env
    for cat, action in (("date_ambiguous", "CONFIRM_DATE"), ("injection_suspected", "READ_RECORD")):
        fid = _add_record_warning(conn, tok, cat)
        t = c.get(f"/api/cases/{tok}/items/{fid}/trace").json()
        s = steps_of(t)
        assert s["record_warning_check"]["next_action"]["code"] == action, cat
        assert t["state_reasons"] and all(r["step_id"] in s for r in t["state_reasons"]), cat


def test_decided_items_have_no_top_level_next_action_but_steps_keep_theirs(env):
    c, conn, tok, _ = env
    pend = c.get(f"/api/cases/{tok}/items/e2/trace").json()
    # force a failing code check, then decide
    e = DB.get_item(conn, "e2", tok)
    DB.update_item(conn, "e2", case=tok, state="needs_review", state_reasons_json=["SUMMARY_DROPS_QUALIFIER"], ladder=e["ladder"])
    t = c.get(f"/api/cases/{tok}/items/e2/trace").json()
    assert t["next_action"] is not None and pend is not None
    for action in ("accept", "dismiss"):
        # D-051: the API refuses accept while a code check fails; old data is simulated by writing the decision directly
        DB.apply_review(conn, "e2", action, now=1.0, case=tok) if action == "accept" else c.post(f"/api/cases/{tok}/items/e2/review", json={"action": action})
        t = c.get(f"/api/cases/{tok}/items/e2/trace").json()
        if action == "accept":       # D-051: an accepted item whose code check fails keeps the fix as its next action (and blocks the export)
            assert t["next_action"]["code"] == "EDIT_SUMMARY" and t["verdict"]["blocks_export"] is True
        else:
            assert t["next_action"] is None
        assert any(s["status"] == "fail" and s["next_action"] for s in t["steps"]) or action == "dismiss"


def test_dismissed_item_human_step_is_skipped_not_pass(env):
    c, _, tok, _ = env
    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "dismiss"})
    h = steps_of(c.get(f"/api/cases/{tok}/items/e1/trace").json())["human"]
    assert h["status"] == "skipped"
    c.post(f"/api/cases/{tok}/items/e2/review", json={"action": "accept"})
    assert steps_of(c.get(f"/api/cases/{tok}/items/e2/trace").json())["human"]["status"] == "pass"


def test_internal_table_bug_is_a_500_not_a_404(env, monkeypatch):
    c, _, tok, _ = env
    amt = c.get(f"/api/cases/{tok}").json()["amounts"][0]["id"]
    assert c.get(f"/api/cases/{tok}/items/{amt}/trace").status_code == 200
    monkeypatch.delitem(trace._NEXT, "DECIDE")
    quiet = TestClient(c.app, client=("127.0.0.1", 50000), raise_server_exceptions=False)
    r = quiet.get(f"/api/cases/{tok}/items/{amt}/trace")
    assert r.status_code == 500 and r.json()["error"]["code"] != "not_found"
    assert quiet.get(f"/api/cases/{tok}/items/e999/trace").status_code == 404           # unknown ids are still 404


def test_amount_judge_objection_counts_in_totals_unsupported(env):
    c, conn, tok, _ = env
    a = next(x for x in DB.list_items(conn, tok, "amount") if x["kind"] != "damages" and (x["ladder"] or {}).get("judge"))
    lad = a["ladder"]
    lad["judge"].update(verdict="disagrees", reason_code="SHOULD_BE_RATE")
    DB.update_item(conn, a["id"], case=tok, state="needs_review", state_reasons_json=["JUDGE_DISAGREES"], ladder=lad)
    rep = c.get(f"/api/cases/{tok}/judges").json()
    assert rep["totals"]["unsupported"] == 1 and rep["judges"][1]["disagrees"] == 1 and len(rep["rejections"]) == 1


def test_zlayt_db_env_var_picks_the_database_file(tmp_path, monkeypatch):
    target = tmp_path / "chosen" / "x.sqlite"
    monkeypatch.setenv("ZLAYT_DB", str(target))
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "ignored"))
    app = create_app(static_dir=str(tmp_path))
    assert app.state.db_path == str(target) and target.exists() and not (tmp_path / "ignored").exists()


# ------------------------------------------------------------------ round 3 (D-044): an AI-made item whose judge never ran blocks export even when accepted; no override
def _accept_all(c, tok):
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})


def _blank_and_accept(c, conn, tok):
    n = _blank_judges(conn, tok)
    _accept_all(c, tok)
    return n


def _gate(c, tok):
    return steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]


def _jnr(gate):
    return [b for b in gate["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]


def test_accepted_items_whose_judge_never_ran_are_gate_blockers_with_a_next_action(env):
    c, conn, tok, _ = env
    n = _blank_and_accept(c, conn, tok)
    gate = _gate(c, tok)
    got = _jnr(gate)
    accepted_blanked = {r["id"] for k in ("entry", "amount") for r in DB.list_items(conn, tok, k)
                        if r["review_status"] in ("accepted", "edited") and "JUDGE_UNAVAILABLE" in r["state_reasons"]
                        and not trace.acknowledge_only(k, r)}      # T-114: an accepted rate only acknowledges, it never needs a judge
    assert len(got) >= 5 and n >= len(got)
    assert {b["item_id"] for b in got} == accepted_blanked
    for b in got:
        assert b["kind"] in ("entry", "amount", "flag") and b["why"] and "second AI check never ran" in b["why"]
        assert b["next_action"]["code"] == "RERUN_JUDGE" and b["next_action"]["text"] == "Run the second check again."
        assert b["next_action"]["target"]["item_id"] == b["item_id"]
    assert gate["ready"] is False and gate["status"] == "fail" and gate["counts"]["judge_not_run"] == len(got)
    assert gate["next_action"]["code"] == "RERUN_JUDGE" and "Run the second check again" in gate["why"]
    ct = c.get(f"/api/cases/{tok}/trace").json()
    assert ct["verdict"]["code"] == "needs_attention" and "not double-checked" in ct["verdict"]["label"]


def test_export_refuses_422_for_the_same_items_the_gate_lists(env):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    ids = sorted(b["item_id"] for b in _jnr(_gate(c, tok)))
    r = c.get(f"/api/cases/{tok}/export")
    assert r.status_code == 422 and r.json()["error"]["code"] == "judge_not_run"
    det = r.json()["error"]["detail"]["blockers"]
    assert sorted(b["item_id"] for b in det) == ids and {b["reason_code"] for b in det} == {"JUDGE_NOT_RUN"}
    assert "letter_text" not in r.text and "second AI check" in r.json()["error"]["message"]


def test_no_override_accepting_again_editing_or_comparing_by_hand_does_not_clear_it(env):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    before = sorted(b["item_id"] for b in _jnr(_gate(c, tok)))
    for i in before:
        c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept", "confirm_judge_unavailable": True, "override": True})
    assert sorted(b["item_id"] for b in _jnr(_gate(c, tok))) == before
    assert c.get(f"/api/cases/{tok}/export").status_code == 422


def test_dismissing_or_resetting_an_unjudged_item_clears_its_blocker(env):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    ids = sorted(b["item_id"] for b in _jnr(_gate(c, tok)))
    c.post(f"/api/cases/{tok}/items/{ids[0]}/review", json={"action": "dismiss"})
    assert ids[0] not in [b["item_id"] for b in _jnr(_gate(c, tok))]
    c.post(f"/api/cases/{tok}/items/{ids[1]}/review", json={"action": "reset"})
    g = _gate(c, tok)
    assert ids[1] not in [b["item_id"] for b in _jnr(g)]
    assert all(b["item_id"] != ids[1] for b in g["blockers"]) and g["counts"]["pending_items"] >= 1                         # now it is pending: a warning, not a blocker


def test_pending_unjudged_items_are_not_judge_blockers_yet(env):
    c, conn, tok, _ = env
    _blank_judges(conn, tok)
    g = _gate(c, tok)
    assert _jnr(g) == [] and g["counts"]["judge_not_run"] == 0 and g["ready"] is False


def test_reviewer_written_entry_is_not_ai_made_so_it_never_needs_the_judge(env):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    eid = sorted(b["item_id"] for b in _jnr(_gate(c, tok)) if b["kind"] == "entry")[0]
    e = DB.get_item(conn, eid, tok)
    lad = e["ladder"]
    lad["entered_by"] = "reviewer"
    DB.update_item(conn, eid, case=tok, ladder=lad)
    assert eid not in [b["item_id"] for b in _jnr(_gate(c, tok))]


def test_entry_with_a_summary_the_paralegal_wrote_is_not_ai_made(env):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    eid = sorted(b["item_id"] for b in _jnr(_gate(c, tok)) if b["kind"] == "entry")[0]
    DB.apply_review(conn, eid, "edit", edited={"summary": "Neck pain, seen in clinic.", "original_summary": "x", "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
    assert eid not in [b["item_id"] for b in _jnr(_gate(c, tok))]


def _accept_all_but(c, tok, keep_pending):
    case = c.get(f"/api/cases/{tok}").json()
    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
        if x["id"] not in keep_pending:
            c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})


def test_gate_ready_equals_export_allowed_in_every_state_d045(env):
    """The invariant: gate.ready == (GET /export is not 4xx) == (gate.blockers == []), whatever the state. Pending items warn, never block."""
    c, conn, tok, _ = env
    seen = {}

    def check(name):
        g = _gate(c, tok)
        ex = c.get(f"/api/cases/{tok}/export")
        assert g["ready"] == (g["blockers"] == []), name
        assert g["ready"] == (ex.status_code < 400), (name, ex.status_code, [b["reason_code"] for b in g["blockers"]])
        assert g["status"] == ("pass" if g["ready"] else "fail"), name
        assert bool(_jnr(g)) == (ex.status_code == 422 and ex.json()["error"]["detail"]["blockers"] != [] and any(b["reason_code"] == "JUDGE_NOT_RUN" for b in ex.json()["error"]["detail"]["blockers"])), name
        if ex.status_code >= 400:
            assert [b["reason_code"] for b in ex.json()["error"]["detail"]["blockers"]] == [b["reason_code"] for b in g["blockers"]], name     # the same list
        seen[name] = (g, ex)

    check("nothing decided yet (pending only)")
    case = c.get(f"/api/cases/{tok}").json()
    all_ids = [x["id"] for x in [*case["entries"], *case["amounts"], *case["flags"]]]
    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
    check("one accepted, rest pending")
    _accept_all_but(c, tok, keep_pending={all_ids[-1]})
    check("all accepted but one")
    n = _blank_judges(conn, tok)
    assert n
    check("accepted, judge not run")
    assert c.post(f"/api/cases/{tok}/rejudge").status_code == 200
    check("judges answered, one pending")
    DB.update_case(conn, tok, status="failed")
    check("run failed")
    DB.update_case(conn, tok, status="running")
    check("run in progress")
    DB.update_case(conn, tok, status="ready")
    _accept_all(c, tok)
    check("all clear")
    for i in all_ids:
        c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "dismiss"})
    check("everything dismissed")

    g, ex = seen["nothing decided yet (pending only)"]
    assert [b["reason_code"] for b in g["blockers"]] == ["NOTHING_ACCEPTED"] and ex.status_code == 422
    g, ex = seen["one accepted, rest pending"]
    assert g["ready"] is True and ex.status_code == 200 and g["warnings"][0]["count"] > 0 and "Items not reviewed" in ex.json()["internal_notes_text"]
    g, ex = seen["all accepted but one"]
    assert g["ready"] is True and g["counts"]["pending_items"] == 1 and "Items not reviewed: 1" in ex.json()["internal_notes_text"]
    g, ex = seen["accepted, judge not run"]
    assert g["ready"] is False and {b["reason_code"] for b in g["blockers"]} == {"JUDGE_NOT_RUN"} and ex.json()["error"]["code"] == "judge_not_run"
    assert seen["judges answered, one pending"][0]["ready"] is True
    g, ex = seen["run failed"]
    assert [b["reason_code"] for b in g["blockers"]] == ["RUN_FAILED"] and ex.json()["error"]["code"] == "export_blocked"
    assert "RUN_IN_PROGRESS" in [b["reason_code"] for b in seen["run in progress"][0]["blockers"]]
    g, ex = seen["all clear"]
    assert g["ready"] is True and g["warnings"] == [] and ex.status_code == 200
    assert seen["everything dismissed"][0]["ready"] is False


def test_paralegal_edited_summary_is_not_counted_unchecked_in_judges_d045b(env):
    c, conn, tok, _ = env
    _blank_judges(conn, tok)
    case = c.get(f"/api/cases/{tok}").json()
    ent = [x["id"] for x in case["entries"]]
    target = ent[0]
    DB.apply_review(conn, target, "edit", edited={"summary": "Neck pain, seen in clinic.", "original_summary": "x", "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
    rep = c.get(f"/api/cases/{tok}/judges").json()
    assert target not in [u["item_id"] for u in rep["unresolved"]]
    assert rep["totals"]["unavailable"] == len(trace.unjudged_items(conn, tok)) and target not in [u["item_id"] for u in trace.unjudged_items(conn, tok)]


def test_edited_summary_with_judge_unavailable_leaves_judges_step_and_gate_clean_d045b(env):
    c, conn, tok, _ = env
    # every judge answered except one entry the paralegal then rewrites; dismiss the rest so only that item is live
    case = c.get(f"/api/cases/{tok}").json()
    target = case["entries"][0]["id"]
    row = DB.get_item(conn, target, tok)
    lad = row["ladder"]
    lad["judge"] = None
    DB.update_item(conn, target, case=tok, state="needs_review", state_reasons_json=sorted(set(row["state_reasons"]) | {"JUDGE_UNAVAILABLE"}), ladder=lad)
    conn.execute("DELETE FROM llm_calls WHERE case_id=? AND item_id=? AND step IN ('j1','j2','j3','j4')", (tok, target))
    before = steps_of(c.get(f"/api/cases/{tok}/trace").json())["judges"]
    assert before["status"] == "fail"
    DB.apply_review(conn, target, "edit", edited={"summary": row["summary"] + " Reviewed.", "original_summary": "x", "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
    ct = c.get(f"/api/cases/{tok}/trace").json()
    assert steps_of(ct)["judges"]["status"] != "fail" and steps_of(ct)["judges"]["counts"]["unavailable"] == 0
    g = steps_of(ct)["export_gate"]
    # T-134: her edit is still Needs review, so it is open: not accepted, not in the letter. Nothing else is accepted here, so the gate says so; no judge blocker.
    assert [b["reason_code"] for b in g["blockers"]] == ["NOTHING_ACCEPTED"] and "EDIT_NOT_CONFIRMED" in [w["reason_code"] for w in g["warnings"]]
    assert c.post(f"/api/cases/{tok}/items/{target}/review", json={"action": "accept"}).status_code == 200      # her explicit accept after comparing it with the quote
    ct = c.get(f"/api/cases/{tok}/trace").json()
    g = steps_of(ct)["export_gate"]
    assert g["ready"] is True and ct["verdict"]["code"] == "ready" and c.get(f"/api/cases/{tok}/export").status_code == 200


# ------------------------------------------------------------------ the rejudge route
def test_rejudge_in_demo_mode_replays_recorded_answers_and_clears_the_gate(env, monkeypatch):
    c, conn, tok, _ = env
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")          # demo mode (no ENABLE_LIVE) must still use the recorded answers only
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    _blank_and_accept(c, conn, tok)
    todo = sorted(b["item_id"] for b in _jnr(_gate(c, tok)))
    calls_before = len(DB.list_llm_calls(conn, tok))
    r = c.post(f"/api/cases/{tok}/rejudge")
    assert r.status_code == 200, r.text
    out = r.json()
    assert out["asked"] >= len(todo) and sorted(x["item_id"] for x in out["rejudged"] if x["item_id"] in todo) == todo and out["still_unavailable"] == []
    assert out["export_gate"]["ready"] is True and out["export_gate"]["blockers"] == []
    new = DB.list_llm_calls(conn, tok)[calls_before:]
    assert len(new) == out["asked"] and {x["backend"] for x in new} == {"fixture"} and {x["role"] for x in new} == {"judge"}      # audited, fixture only
    assert {x["item_id"] for x in new} >= set(todo)
    assert c.get(f"/api/cases/{tok}/export").status_code == 200
    j = c.get(f"/api/cases/{tok}/judges").json()["totals"]
    assert j["unavailable"] == 0
    e = DB.get_item(conn, todo[0], tok)
    assert e["review_status"] == "accepted" and e["ladder"]["judge"]["verdict"] != "unavailable" and e["ladder"]["rejudge"][-1]["verdict"] != "unavailable"
    assert "JUDGE_UNAVAILABLE" not in e["state_reasons"] and "FIXTURE_MISS" not in e["state_reasons"]


def test_rejudge_with_nothing_to_do_asks_nothing(env):
    c, conn, tok, _ = env
    before = len(DB.list_llm_calls(conn, tok))
    r = c.post(f"/api/cases/{tok}/rejudge")
    assert r.status_code == 200 and r.json()["asked"] == 0 and r.json()["rejudged"] == []
    assert len(DB.list_llm_calls(conn, tok)) == before


def test_rejudge_only_touches_items_whose_judge_never_ran(env):
    c, conn, tok, _ = env
    n = _blank_judges(conn, tok)
    keep = {r["id"]: json.dumps(r["ladder"], sort_keys=True) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, tok, k)
            if (r["ladder"] or {}).get("judge")}
    r = c.post(f"/api/cases/{tok}/rejudge").json()
    assert r["asked"] == n
    for k in ("entry", "amount", "flag"):
        for row in DB.list_items(conn, tok, k):
            if row["id"] in keep:
                assert json.dumps(row["ladder"], sort_keys=True) == keep[row["id"]], row["id"]


def _fake_factory(verdicts, seen=None):
    """call_factory whose judge answers come from `verdicts` {step: output | Exception}; every call is recorded in `seen`."""
    from app.llm import audited as AU

    def factory(conn, cid):
        def call(step, system, user, schema, *, item_id=None, validate=None):
            if seen is not None:
                seen.append((step, item_id))
            v = verdicts[step]
            if isinstance(v, Exception):
                raise v
            return v, None
        return call
    return factory


def test_rejudge_failure_leaves_the_item_unjudged_and_the_gate_closed(env, tmp_path):
    from app.llm import audited as AU
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    todo = sorted(b["item_id"] for b in _jnr(_gate(c, tok)))
    app = create_app(str(tmp_path / "copy.sqlite"), call_factory=_fake_factory({s: AU.LLMFailed("x") for s in ("j1", "j2", "j3", "j4")}), static_dir=str(tmp_path))
    c2 = TestClient(app, client=("127.0.0.1", 50000))
    r = c2.post(f"/api/cases/{tok}/rejudge")
    rates = sorted(x["id"] for x in DB.list_items(conn, tok, "amount") if x["kind"] == "rate" and x["state"] != "rejected")      # T-114: still re-asked, but never a blocker
    assert r.status_code == 200 and r.json()["rejudged"] == [] and sorted(x["item_id"] for x in r.json()["still_unavailable"]) == sorted(todo + rates)
    assert r.json()["export_gate"]["ready"] is False and sorted(b["item_id"] for b in r.json()["export_gate"]["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN") == todo
    assert c2.get(f"/api/cases/{tok}/export").status_code == 422
    e = DB.get_item(conn, todo[0], tok)
    assert e["review_status"] == "accepted" and len(e["ladder"]["rejudge"]) == 1 and e["ladder"]["rejudge"][0]["verdict"] == "unavailable"


def test_rejudge_objection_is_recorded_and_the_gate_opens_because_the_judge_ran(env, tmp_path):
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    todo = sorted(b["item_id"] for b in _jnr(_gate(c, tok)))
    seen = []
    ans = {"j1": {"verdict": "unsupported", "reason_code": "NUMBER_MISMATCH"}, "j2": {"verdict": "disagree", "reason_code": "SHOULD_BE_RATE"},
           "j3": {"verdict": "unsure", "reason_code": "NONE"}, "j4": {"verdict": "unsure", "reason_code": "NONE"}}
    c2 = TestClient(create_app(str(tmp_path / "copy.sqlite"), call_factory=_fake_factory(ans, seen), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    r = c2.post(f"/api/cases/{tok}/rejudge").json()
    assert sorted(x["item_id"] for x in r["rejudged"] if x["item_id"] in todo) == todo and r["still_unavailable"] == []
    assert len(seen) == r["asked"] and {i for _, i in seen} >= set(todo)
    ent = next(x for x in r["rejudged"] if x["kind"] == "entry")
    assert ent["state"] == "needs_review" and "JUDGE_UNSUPPORTED" in ent["state_reasons"] and "JUDGE_UNAVAILABLE" not in ent["state_reasons"]
    amt = next(x for x in r["rejudged"] if x["kind"] == "amount")
    assert "JUDGE_DISAGREES" in amt["state_reasons"] and amt["review_status"] == "accepted"
    assert r["export_gate"]["ready"] is True and c2.get(f"/api/cases/{tok}/export").status_code == 200       # the paralegal accepted knowing the judge objected
    rep = c2.get(f"/api/cases/{tok}/judges").json()
    assert rep["totals"]["human_overrides"] >= 2 and rep["totals"]["unavailable"] == 0


def test_rejudge_is_refused_in_the_cases_the_run_route_refuses(env, tmp_path):
    c, conn, tok, _ = env
    assert c.post("/api/cases/nope/rejudge").status_code == 404
    DB.update_case(conn, tok, status="running")
    r = c.post(f"/api/cases/{tok}/rejudge")
    assert r.status_code == 409 and r.json()["error"]["code"] == "run_in_progress"
    DB.update_case(conn, tok, status="ready")
    conn.execute("UPDATE cases SET raw_text=? WHERE id=?", ("SYNTHETIC. 01/02/2024 Clinic note: seen for neck pain.", tok))      # a case whose text was never recorded
    r = c.post(f"/api/cases/{tok}/rejudge")
    assert r.status_code == 409 and r.json()["error"]["code"] == "demo_mode_unsupported_input"            # demo mode: recorded cases only


def test_rejected_amount_and_flag_are_dismiss_only_and_never_block_the_gate(env):
    c, conn, tok, _ = env
    amt = next(x for x in DB.list_items(conn, tok, "amount") if x["kind"] == "charge")
    flg = next(x for x in DB.list_items(conn, tok, "flag") if x["type"] in ("pre_existing", "causation", "conflict"))
    g0 = _gate(c, tok)
    DB.update_item(conn, amt["id"], case=tok, state="rejected", state_reasons_json=["GROUNDING_AMOUNT_NOT_IN_TEXT"], ladder=amt["ladder"])
    DB.update_item(conn, flg["id"], case=tok, state="rejected", state_reasons_json=["GROUNDING_EXCERPT_NOT_VERBATIM"], ladder=flg["ladder"])
    for i in (amt["id"], flg["id"]):
        t = c.get(f"/api/cases/{tok}/items/{i}/trace").json()
        h = steps_of(t)["human"]
        assert t["verdict"]["code"] == "rejected" and t["verdict"]["blocks_export"] is False
        assert h["status"] == "pending" and h["next_action"]["code"] == "DISMISS_OR_ENTER_BY_HAND" and h["blocks_export"] is False
    g = _gate(c, tok)
    assert amt["id"] not in [b["item_id"] for b in g["blockers"]] and flg["id"] not in [b["item_id"] for b in g["blockers"]]
    assert g["counts"]["rejected_not_blocking"] == g0["counts"]["rejected_not_blocking"] + 2


def test_an_edited_item_counts_as_accepted_for_the_judge_blocker(env):
    """status 'edited' blocks like 'accepted' once it is decided (the quote is still AI-chosen when only the quote was edited).
    T-134: an edit still marked Needs review is not decided: it blocks nothing until she accepts it."""
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    eid = sorted(b["item_id"] for b in _jnr(_gate(c, tok)) if b["kind"] == "entry")[0]
    e = DB.get_item(conn, eid, tok)
    DB.apply_review(conn, eid, "edit", edited={"excerpt": e["excerpt"], "original_excerpt": e["excerpt"], "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
    assert DB.get_item(conn, eid, tok)["review_status"] == "edited"
    assert DB.get_item(conn, eid, tok)["state"] == "needs_review"
    assert eid not in [b["item_id"] for b in _jnr(_gate(c, tok))]
    assert c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "accept"}).status_code == 200
    assert eid in [b["item_id"] for b in _jnr(_gate(c, tok))]


def test_an_edited_unjudged_entry_that_is_not_needs_review_still_blocks_as_accepted_would(env):
    """The `edited` arm of judge_not_run_blockers (T-134 r2): an edit that is not open (state not needs_review) is decided by the edit, so its missing second check blocks."""
    c, conn, tok, _ = env
    _blank_and_accept(c, conn, tok)
    eid = sorted(b["item_id"] for b in _jnr(_gate(c, tok)) if b["kind"] == "entry")[0]
    e = DB.get_item(conn, eid, tok)
    DB.apply_review(conn, eid, "edit", edited={"excerpt": e["excerpt"], "original_excerpt": e["excerpt"], "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
    DB.update_item(conn, eid, case=tok, state="verified", state_reasons_json=[])
    row = DB.get_item(conn, eid, tok)
    assert row["review_status"] == "edited" and row["state"] == "verified"
    assert eid in [b["item_id"] for b in _jnr(_gate(c, tok))]


def test_rejudge_writes_one_rejudge_event_per_asked_item_and_leaves_review_status_alone(env, monkeypatch):
    """T-095: review_events.action 'rejudge', one row per item the second check was asked about; the paralegal's status is untouched."""
    c, conn, tok, _ = env
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    _blank_and_accept(c, conn, tok)
    before = {r["id"]: r["review_status"] for k in ("entry", "amount", "flag") for r in DB.list_items(conn, tok, k)}
    seen_before = len(DB.list_events(conn, tok))
    out = c.post(f"/api/cases/{tok}/rejudge").json()
    ev = [e for e in DB.list_events(conn, tok) if e["action"] == "rejudge"]
    assert out["asked"] > 0 and len(ev) == out["asked"] and len(DB.list_events(conn, tok)) == seen_before + out["asked"]
    assert sorted(e["item_id"] for e in ev) == sorted(x["item_id"] for x in out["rejudged"] + out["still_unavailable"])
    assert all(e["after"]["event"] == "rejudge" and e["after"]["verdict"] and e["before"]["review_status"] == "accepted" for e in ev)
    assert {r["id"]: r["review_status"] for k in ("entry", "amount", "flag") for r in DB.list_items(conn, tok, k)} == before


# ---- D-045(b) / T-098: a human-edited summary is exempt from the judge, never from the code checks (reviewer case: reviews/T-097-ux-designer.md B1)
REVIEWER_EDIT = "Paralegal wording for the mixed-case check."          # the T-097 walk's edit: drops the quote's qualifier


def _edit_entry(c, tok, eid, summary):
    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "edit", "edits": {"summary": summary}})
    assert r.status_code == 200, r.text
    return r


def _mixed(c, tok, conn):
    """The reviewer's walk: accept one entry, edit another so it drops a qualifier, dismiss the first. Returns the edited id."""
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    acc, edt = ents[0]["id"], ents[1]["id"]
    assert c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "accept"}).status_code == 200
    r = c.post(f"/api/cases/{tok}/items/{edt}/review", json={"action": "edit", "edits": {"summary": REVIEWER_EDIT}})
    assert r.status_code == 422 and r.json()["error"]["detail"]["reason"] == "SUMMARY_DROPS_QUALIFIER"     # D-047: the route refuses it, so the gate case below is legacy/hand-written data
    orig = DB.get_item(conn, edt, tok)
    DB.apply_review(conn, edt, "edit", edited={"summary": REVIEWER_EDIT, "original_summary": orig["summary"], "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)   # bypass the route: the gate is the second line of defence
    lad = orig.get("ladder") or {"item_id": edt}
    lad.setdefault("code_checks", {}).update(qualifier_carried=False)
    DB.update_item(conn, edt, now=9e9, case=tok, state="needs_review", state_reasons_json=["SUMMARY_DROPS_QUALIFIER"], ladder=lad)
    c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "dismiss"})
    return edt


def _ccf(gate):
    return [b for b in gate["blockers"] if b.get("step_id")]


def test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098(env):
    c, conn, tok, _ = env
    edt = _mixed(c, tok, conn)
    g = _gate(c, tok)
    got = _ccf(g)
    assert [b["item_id"] for b in got] == [edt] and got[0]["reason_code"] == "SUMMARY_DROPS_QUALIFIER" and got[0]["step_id"] == "summary_qualifier"
    assert g["ready"] is False and g["status"] == "fail" and g["counts"]["code_check_failed"] == 1 and g["reason_code"] == "SUMMARY_DROPS_QUALIFIER"
    assert "second AI check is not needed" in got[0]["why"] and g["next_action"]["code"] == "EDIT_SUMMARY"
    r = c.get(f"/api/cases/{tok}/export")
    assert r.status_code == 422 and "letter_text" not in r.text and REVIEWER_EDIT not in r.text
    det = r.json()["error"]["detail"]["blockers"]
    assert [(b["item_id"], b["reason_code"]) for b in det] == [(edt, "SUMMARY_DROPS_QUALIFIER"), (None, "NOTHING_ACCEPTED")]      # T-134: the open edit is not accepted either
    assert r.json()["error"]["code"] == "export_blocked" and "export is blocked" in r.json()["error"]["message"]
    ct = c.get(f"/api/cases/{tok}/trace").json()
    assert ct["verdict"]["code"] == "needs_attention" and "fails a check" in ct["verdict"]["label"]


def test_item_trace_shows_the_failing_code_step_with_the_next_action_t098(env):
    c, conn, tok, _ = env
    edt = _mixed(c, tok, conn)
    t = c.get(f"/api/cases/{tok}/items/{edt}/trace").json()
    s = steps_of(t)
    q = s["summary_qualifier"]
    assert q["status"] == "fail" and q["blocks_export"] is True and q["reason_code"] == "SUMMARY_DROPS_QUALIFIER"
    na = q["next_action"]
    assert na["code"] == "EDIT_SUMMARY" and na["text"].startswith("Edit the summary to keep ") and "‘" in na["text"] and "export stays blocked" in na["text"]
    assert t["verdict"]["blocks_export"] is True and t["verdict"]["code"] == "needs_attention" and t["next_action"] == na
    assert s["human"]["status"] == "pending" and s["human"]["reason_code"] == "EDIT_NOT_CONFIRMED"      # T-134: the edit is open, so the trail does not call it a decision; the code check is what blocks
    for sid in ("summary_tokens", "excerpt_verbatim", "highlight"):
        assert s[sid]["blocks_export"] is False


def test_fixing_the_summary_clears_the_blocker_and_the_gate_agrees_with_export_t098(env):
    c, conn, tok, _ = env
    edt = _mixed(c, tok, conn)
    assert c.get(f"/api/cases/{tok}/export").status_code == 422
    quote = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == edt)["excerpt"]
    _edit_entry(c, tok, edt, quote)      # the quote verbatim keeps every qualifier
    g = _gate(c, tok)
    assert _ccf(g) == [] and [b["reason_code"] for b in g["blockers"]] == ["NOTHING_ACCEPTED"]       # T-134: the fixed edit is still Needs review (no second check), so not accepted yet
    assert c.post(f"/api/cases/{tok}/items/{edt}/review", json={"action": "accept"}).status_code == 200
    g = _gate(c, tok)
    assert _ccf(g) == [] and g["ready"] is True
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 200 and g["ready"] == (ex.status_code < 400)
    assert steps_of(c.get(f"/api/cases/{tok}/items/{edt}/trace").json())["summary_qualifier"]["status"] == "pass"


def test_dismissing_the_failing_edited_item_clears_the_blocker_t098(env):
    c, conn, tok, _ = env
    edt = _mixed(c, tok, conn)
    c.post(f"/api/cases/{tok}/items/{edt}/review", json={"action": "dismiss"})
    assert _ccf(_gate(c, tok)) == []


def test_clean_accepted_ai_drafts_are_not_code_check_blockers_d051(env):
    c, conn, tok, _ = env
    _accept_all(c, tok)
    assert _ccf(_gate(c, tok)) == []


def test_gate_ready_equals_export_allowed_with_a_failing_edit_t098(env):
    c, conn, tok, _ = env
    _mixed(c, tok, conn)
    for name in ("failing edit", "failing edit and run failed"):
        if name.endswith("run failed"):
            DB.update_case(conn, tok, status="failed")
        g = _gate(c, tok)
        ex = c.get(f"/api/cases/{tok}/export")
        assert g["ready"] == (g["blockers"] == []) == (ex.status_code < 400), name
        assert [b["reason_code"] for b in ex.json()["error"]["detail"]["blockers"]] == [b["reason_code"] for b in g["blockers"]], name


def test_missing_qualifier_terms_name_the_words_to_keep_t098():
    from app.backend import grounding
    assert grounding.missing_qualifier_terms("MRI of the cervical spine was done.", "MRI suggests possible disc herniation.")
    got = grounding.missing_qualifier_terms("Fracture seen.", "Possible left wrist fracture.")
    assert "possible" in got and "left" in got
    assert grounding.missing_qualifier_terms("Possible left wrist fracture.", "Possible left wrist fracture.") == []


# ---- D-051 / T-098 r2: the code rung binds accept for every item, AI-made or human (reviewer F1: an AI draft 'Pain 5/10' over a quote without 5/10)
def _ai_draft_with_invented_number(c, conn, tok, *, judge="supported", stored_reason=True, eid=None):
    """An AI-made entry whose summary says 'Pain 5/10' over a quote that does not. State, reasons and judge verdict set like the generator + judge would."""
    eid = eid or c.get(f"/api/cases/{tok}").json()["entries"][0]["id"]
    row = DB.get_item(conn, eid, tok)
    assert "5/10" not in row["excerpt"] and "ladder" in row and not row["ladder"].get("entered_by")
    lad = row["ladder"]
    lad["judge"] = {**(lad.get("judge") or {}), "verdict": judge}
    DB.update_item(conn, eid, now=9e9, case=tok, summary="Pain 5/10", ladder=lad,
                   state="needs_review" if stored_reason else "verified", state_reasons_json=["SUMMARY_TOKEN_NOT_IN_EXCERPT"] if stored_reason else [])
    return eid


@pytest.mark.parametrize("judge", ["supported", "unsupported", "disagrees"])
def test_accepting_an_ai_draft_with_an_invented_number_is_422_and_the_export_never_has_it_d051(env, judge):
    c, conn, tok, _ = env
    eid = _ai_draft_with_invented_number(c, conn, tok, judge=judge)
    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "accept"})
    err = r.json()["error"]
    assert r.status_code == 422 and err["code"] == "CODE_CHECK_FAILED"
    assert "not in the quote: 5." in err["message"] and err["message"].endswith("Edit the summary to match the quote.")
    assert err["detail"]["next_action"]["text"] == "Edit the summary to match the quote" and err["detail"]["next_action"]["code"] == "EDIT_SUMMARY"
    assert err["detail"]["reason_code"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and err["detail"]["step_id"] == "summary_tokens" and err["detail"]["tokens"] == ["5"]
    assert DB.get_item(conn, eid, tok)["review_status"] == "pending"           # nothing was written
    for x in c.get(f"/api/cases/{tok}").json()["entries"]:                      # accept everything else the paralegal can; the letter must not carry the figure
        if x["id"] != eid:
            c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
    ex = c.get(f"/api/cases/{tok}/export")
    assert "5/10" not in ex.text


def test_accept_recomputes_from_the_current_text_not_only_the_stored_reasons_d051(env):
    c, conn, tok, _ = env
    eid = _ai_draft_with_invented_number(c, conn, tok, stored_reason=False)    # state 'verified', no stored reason: only the live check can catch it
    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "CODE_CHECK_FAILED"


def test_accept_refuses_a_dropped_qualifier_on_an_ai_draft_and_a_clean_draft_still_accepts_d051(env):
    c, conn, tok, _ = env
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    eid = ents[1]["id"]
    DB.update_item(conn, eid, now=9e9, case=tok, summary=REVIEWER_EDIT, state="needs_review", state_reasons_json=["SUMMARY_DROPS_QUALIFIER"])
    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["detail"]["reason_code"] == "SUMMARY_DROPS_QUALIFIER" and "Edit the summary to match the quote." in r.json()["error"]["message"]
    assert c.post(f"/api/cases/{tok}/items/{ents[0]['id']}/review", json={"action": "accept"}).status_code == 200      # golden drafts pass the code checks


def test_batch_accept_refuses_the_whole_batch_for_one_failing_summary_d051(env):
    c, conn, tok, _ = env
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    bad = _ai_draft_with_invented_number(c, conn, tok, stored_reason=False, eid=ents[0]["id"])
    ids = [bad, ents[1]["id"], ents[2]["id"]]
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ids})
    err = r.json()["error"]
    assert r.status_code == 422 and err["code"] == "CODE_CHECK_FAILED" and err["message"].endswith("Nothing was changed.") and "not in the quote: 5." in err["message"]
    rej = [x for x in err["detail"]["rejected"] if x["reason"] == "code_check_failed"]
    assert [x["id"] for x in rej] == [bad] and rej[0]["next_action"]["text"] == "Edit the summary to match the quote" and rej[0]["reason_code"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT"
    assert all(DB.get_item(conn, i, tok)["review_status"] == "pending" for i in ids)       # all or nothing


def test_gate_blocks_an_accepted_ai_draft_that_fails_a_code_check_and_export_is_422_d051(env):
    """Old data / any other route: the accept guard is not trusted. The gate lists the item, the trace shows the failing step, GET export is 422."""
    c, conn, tok, _ = env
    eid = _ai_draft_with_invented_number(c, conn, tok, judge="supported")
    DB.apply_review(conn, eid, "accept", now=9e9, case=tok)                                 # bypass the route
    for x in c.get(f"/api/cases/{tok}").json()["entries"]:
        if x["id"] != eid:
            c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
    g = _gate(c, tok)
    got = _ccf(g)
    assert [b["item_id"] for b in got] == [eid] and got[0]["reason_code"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and got[0]["step_id"] == "summary_tokens"
    assert "drafted by the AI" in got[0]["why"] and "‘5’" in got[0]["next_action"]["text"] and "second AI check is not needed" not in got[0]["why"]
    ex = c.get(f"/api/cases/{tok}/export")
    assert g["ready"] is False and ex.status_code == 422 and "letter_text" not in ex.text and "Pain 5/10" not in ex.text
    t = c.get(f"/api/cases/{tok}/items/{eid}/trace").json()
    s = steps_of(t)["summary_tokens"]
    assert s["status"] == "fail" and s["blocks_export"] is True and s["next_action"]["code"] == "EDIT_SUMMARY"
    assert t["verdict"]["blocks_export"] is True and t["next_action"] == s["next_action"]


def test_pending_ai_draft_trace_shows_the_failing_code_step_even_with_stored_data_clean_d051(env):
    c, conn, tok, _ = env
    eid = _ai_draft_with_invented_number(c, conn, tok, stored_reason=False)
    s = steps_of(c.get(f"/api/cases/{tok}/items/{eid}/trace").json())["summary_tokens"]
    assert s["status"] == "fail" and s["evidence"]["tokens"] == ["5"]


def test_a_non_code_check_reason_on_an_accepted_entry_is_not_a_code_check_blocker_t098_f4(env):
    c, conn, tok, _ = env
    eid = c.get(f"/api/cases/{tok}").json()["entries"][0]["id"]
    DB.update_item(conn, eid, now=9e9, case=tok, state="needs_review", state_reasons_json=["INJECTION_SUSPECTED", "OCR_DERIVED"])
    DB.apply_review(conn, eid, "accept", now=9e9, case=tok)
    assert eid not in [b["item_id"] for b in _ccf(_gate(c, tok))]


def test_gate_and_export_recompute_the_code_checks_and_ignore_a_stale_stored_pass_t097_r2_b1(env):
    """An edited summary that drops a qualifier, written straight to edited_json with every stored check result left as 'pass': the gate and the export
    recompute from the current text, so GET /export is 422 export_blocked naming the item (reviews/T-097-ux-designer-r2.md B1)."""
    c, conn, tok, _ = env
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    acc, edt = ents[0]["id"], ents[1]["id"]
    orig = DB.get_item(conn, edt, tok)
    lad = orig["ladder"]
    lad.setdefault("code_checks", {}).update(qualifier_carried=True, summary_tokens_not_in_excerpt=[], excerpt_whole_sentence=True, highlight_found=True)
    DB.update_item(conn, edt, now=9e9, case=tok, state="verified", state_reasons_json=[], ladder=lad)          # stale: every stored result says pass
    DB.apply_review(conn, edt, "edit", edited={"summary": REVIEWER_EDIT, "original_summary": orig["summary"], "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)
    c.post(f"/api/cases/{tok}/items/{acc}/review", json={"action": "accept"})
    g = _gate(c, tok)
    assert g["ready"] is False and [(b["item_id"], b["reason_code"]) for b in _ccf(g)] == [(edt, "SUMMARY_DROPS_QUALIFIER")]
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 422 and ex.json()["error"]["code"] == "export_blocked" and REVIEWER_EDIT not in ex.text.replace(g["blockers"][0]["why"], "")
    assert [(b["item_id"], b["reason_code"]) for b in ex.json()["error"]["detail"]["blockers"]] == [(edt, "SUMMARY_DROPS_QUALIFIER")]
    assert steps_of(c.get(f"/api/cases/{tok}/items/{edt}/trace").json())["summary_qualifier"]["status"] == "fail"


# ---- D-051 / T-098 r3: ONE choke point (review.set_review) for every decision that leaves an entry accepted or edited; the gate and the trace recompute all five checks
HEDGE_Q = "C5-C6 disc protrusion with mild right foraminal narrowing."                               # e8's quote without the hedge sentence that follows it in the record
HEDGE_FULL = "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."


def _e8_ai_draft_with_short_quote(c, conn, tok, stored=True):
    """The reviewer's live case (T-098-staff-engineer-r2 F1): the AI quoted e8 and left out the hedge sentence that follows it."""
    row = DB.get_item(conn, "e8", tok)
    assert HEDGE_FULL in row["excerpt"] or row["excerpt"].startswith(HEDGE_Q)
    DB.update_item(conn, "e8", now=9e9, case=tok, excerpt=HEDGE_Q, summary="Disc protrusion at C5-C6 with mild right foraminal narrowing.",
                   state="needs_review", state_reasons_json=["EXCERPT_OMITS_QUALIFIER"] if stored else [])
    return "e8"


def test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3(env):
    c, conn, tok, _ = env
    eid = _e8_ai_draft_with_short_quote(c, conn, tok)
    for body in ({"action": "accept"}, {"action": "edit", "edits": {"summary": "Disc protrusion at C5-C6 with mild right foraminal narrowing."}}):
        r = c.post(f"/api/cases/{tok}/items/{eid}/review", json=body)
        err = r.json()["error"]
        assert r.status_code == 422 and err["code"] == "CODE_CHECK_FAILED", body
        assert err["detail"]["reason_code"] == "EXCERPT_OMITS_QUALIFIER" and err["detail"]["step_id"] == "excerpt_hedge"
        assert err["detail"]["next_action"]["code"] == "EDIT_QUOTE" and "Change the quote" in err["message"] and "Edit the summary" not in err["message"]
        row = DB.get_item(conn, eid, tok)
        assert row["review_status"] == "pending" and row["edited"] is None and "EXCERPT_OMITS_QUALIFIER" in row["state_reasons"]     # nothing written, reason not wiped
    ok = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "edit", "edits": {"excerpt": HEDGE_FULL, "summary": "Disc protrusion at C5-C6 with mild right foraminal narrowing; findings may represent degenerative change."}})
    assert ok.status_code == 200, ok.text                                                           # changing the QUOTE is the fix
    assert DB.get_item(conn, eid, tok)["review_status"] == "edited"


def test_reset_of_a_failing_entry_is_allowed_and_keeps_the_stored_reason_d051_r3(env):
    c, conn, tok, _ = env
    eid = _e8_ai_draft_with_short_quote(c, conn, tok)
    DB.apply_review(conn, eid, "accept", now=9e9, case=tok)                                          # old data: accepted before the guard
    r = c.post(f"/api/cases/{tok}/items/{eid}/review", json={"action": "reset"})
    assert r.status_code == 200
    row = DB.get_item(conn, eid, tok)
    assert row["review_status"] == "pending" and "EXCERPT_OMITS_QUALIFIER" in row["state_reasons"]


def test_set_review_is_the_choke_point_for_accept_edit_and_batch_d051_r3(env):
    from app.backend import review as REV
    c, conn, tok, _ = env
    eid = _e8_ai_draft_with_short_quote(c, conn, tok)
    for action, kw in (("accept", {}), ("edit", {"edited": {"summary": "x y", "at": "t"}})):
        with pytest.raises(REV.ReviewError) as ei:
            REV.set_review(conn, tok, eid, action, now=9e9, **kw)
        assert ei.value.status == 422 and ei.value.code == "CODE_CHECK_FAILED"
    with pytest.raises(REV.ReviewError):
        REV.batch_apply(conn, tok, eid, "accept", 9e9)
    assert DB.get_item(conn, eid, tok)["review_status"] == "pending"
    REV.batch_apply(conn, tok, eid, "reset", 9e9)                                                    # the way out is never blocked
    assert not [e for e in DB.list_events(conn, tok, eid) if e["action"] in ("accept", "edit")]


QUOTE_AND_SUMMARY_CASES = [      # (name, excerpt, summary, expected reason, failing trace step); every stored check result is left as a pass
    ("hedge sentence dropped", HEDGE_Q, "Disc protrusion at C5-C6 with mild right foraminal narrowing.", "EXCERPT_OMITS_QUALIFIER", "excerpt_hedge"),
    ("quote starts mid-sentence", "disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.",
     "Disc protrusion with mild right foraminal narrowing; findings may represent degenerative change.", "EXCERPT_NOT_WHOLE_SENTENCE", "excerpt_whole_sentence"),
    ("quote is not in the record", "Patient reports the collision was the cause of the disc protrusion.", "Patient reports the collision was the cause of the disc protrusion.",
     "GROUNDING_EXCERPT_NOT_VERBATIM", "excerpt_verbatim"),
    ("number not in the quote", HEDGE_FULL, "Disc protrusion with pain 5/10, findings may represent degenerative change.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "summary_tokens"),
    ("qualifier dropped", HEDGE_FULL, "Disc protrusion at C5-C6 with mild right foraminal narrowing.", "SUMMARY_DROPS_QUALIFIER", "summary_qualifier"),
]


@pytest.mark.parametrize("name,excerpt,summary,reason,step_id", QUOTE_AND_SUMMARY_CASES, ids=[x[0] for x in QUOTE_AND_SUMMARY_CASES])
def test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3(env, name, excerpt, summary, reason, step_id):
    """The reviewer's F2: every stored result says pass, the text fails one check. Accept refuses; a forced accept is a gate blocker, GET /export is 422
    and the item trace shows that step failing with blocks_export. Mutant M11 (the quote checks off) fails the first three cases."""
    c, conn, tok, _ = env
    row = DB.get_item(conn, "e8", tok)
    lad = row["ladder"]
    lad["code_checks"] = {k: (True if k != "summary_tokens_not_in_excerpt" else []) for k in (lad.get("code_checks") or {})}
    lad["judge"] = {"model": "fixture", "prompt_version": "judge", "call_id": None, "verdict": "supported", "reason_code": "NONE"}
    DB.update_item(conn, "e8", now=9e9, case=tok, summary=summary, excerpt=excerpt, state="verified", state_reasons_json=[], ladder=lad)
    r = c.post(f"/api/cases/{tok}/items/e8/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["detail"]["reason_code"] == reason
    DB.apply_review(conn, "e8", "accept", now=9e9, case=tok)                                         # old data / any route that skips the guard
    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
    g = _gate(c, tok)
    assert g["ready"] is False and [(b["item_id"], b["reason_code"]) for b in _ccf(g)] == [("e8", reason)]
    assert c.get(f"/api/cases/{tok}/export").status_code == 422
    stp = steps_of(c.get(f"/api/cases/{tok}/items/e8/trace").json())[step_id]
    assert stp["status"] == "fail" and stp["blocks_export"] is True and stp["reason_code"] == reason


def test_internal_notes_never_print_ai_wording_that_failed_a_check_d051_r3(env, monkeypatch):
    """EDITED ITEMS 'summary was' and the narrative 'Removed' line say the AI wording was removed, not what it said."""
    monkeypatch.setenv("NARRATIVE_IN_LETTER", "1")      # D-067: the narrative is out of the notes by default; this test is about the flagged-on path
    c, conn, tok, _ = env
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    eid = ents[0]["id"]
    row = DB.get_item(conn, eid, tok)
    DB.apply_review(conn, eid, "edit", edited={"summary": row["summary"], "original_summary": "Pain 5/10 on the left.", "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)
    DB.update_item(conn, eid, now=9e9, case=tok, state="verified", state_reasons_json=[])
    for x in ents[1:]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
    case = DB.get_case(conn, tok)
    cfg = dict(case.get("config") or {})
    cfg["narrative"] = {"status": "pending", "sentences": [], "basis": {}, "removed": [
        {"id": "ns1", "entry_id": eid, "text": "Pain 77/10 invented.", "reason": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "The sentence has a number, side, negation or date that is not in the cited quote."},
        {"id": "ns2", "entry_id": eid, "text": "Second check said no.", "reason": "JUDGE_UNSUPPORTED", "message": "x"}]}
    DB.update_case(conn, tok, config_json=cfg)
    j = c.get(f"/api/cases/{tok}/export").json()
    notes = j["internal_notes_text"]
    assert "5/10" not in j["letter_text"] + notes and "77/10" not in j["letter_text"] + notes
    assert "summary was AI wording removed (failed a check:" in notes and "a number or word in it is not in the quote" in notes
    assert "- AI wording removed (failed a check: The sentence has a number" in notes
    assert 'Removed: "Second check said no."' in notes                                              # a judge removal is not a code failure: the sentence stays visible


def test_verdict_says_this_summary_for_an_ai_draft_and_your_wording_only_for_the_paralegals_t097_r3_f1(env):
    c, conn, tok, _ = env
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    ai, human = ents[0]["id"], ents[1]["id"]
    DB.update_item(conn, ai, now=9e9, case=tok, summary="Pain 5/10", state="verified", state_reasons_json=[])
    DB.apply_review(conn, ai, "accept", now=9e9, case=tok)                                            # an accepted AI draft that fails a check (old data)
    orig = DB.get_item(conn, human, tok)
    DB.apply_review(conn, human, "edit", edited={"summary": REVIEWER_EDIT, "original_summary": orig["summary"], "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)
    v = {i: c.get(f"/api/cases/{tok}/items/{i}/trace").json()["verdict"] for i in (ai, human)}
    assert v[ai]["label"] == "Needs your attention: a check on this summary fails" and "wording" not in v[ai]["label"]
    assert v[human]["label"] == "Needs your attention: a check on your wording fails"
    assert v[ai]["code"] == v[human]["code"] == "needs_attention" and v[ai]["blocks_export"] and v[human]["blocks_export"]


def test_highlight_not_found_is_recomputed_live_by_accept_gate_and_trace_t106(env, monkeypatch):
    """T-098 r3 F2: HIGHLIGHT_NOT_FOUND has no route with a verbatim quote today (locate and check_excerpt use one matcher), so the live recompute is
    defence in depth. Pin it by making locate fail while every stored result says pass: accept refuses, a forced accept is a gate blocker, export is
    422 and the item trace fails the `highlight` step. Mutants: the highlight term off in trace._entry_steps, or the check off in review.code_check_failures."""
    from app.backend import grounding
    c, conn, tok, _ = env
    row = DB.get_item(conn, "e8", tok)
    lad = row["ladder"]
    lad["code_checks"] = {k: (True if k != "summary_tokens_not_in_excerpt" else []) for k in (lad.get("code_checks") or {})}
    lad["judge"] = {"model": "fixture", "prompt_version": "judge", "call_id": None, "verdict": "supported", "reason_code": "NONE"}
    DB.update_item(conn, "e8", now=9e9, case=tok, state="verified", state_reasons_json=[], ladder=lad)
    assert steps_of(c.get(f"/api/cases/{tok}/items/e8/trace").json())["highlight"]["status"] == "pass"      # control: fine while locate works
    monkeypatch.setattr(grounding, "locate", lambda *a, **k: None)
    r = c.post(f"/api/cases/{tok}/items/e8/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["detail"]["reason_code"] == "HIGHLIGHT_NOT_FOUND"
    DB.apply_review(conn, "e8", "accept", now=9e9, case=tok)                                         # old data / any route that skips the guard
    g = _gate(c, tok)
    assert ("e8", "HIGHLIGHT_NOT_FOUND") in [(b["item_id"], b["reason_code"]) for b in _ccf(g)] and g["ready"] is False
    assert c.get(f"/api/cases/{tok}/export").status_code == 422
    stp = steps_of(c.get(f"/api/cases/{tok}/items/e8/trace").json())["highlight"]
    assert stp["status"] == "fail" and stp["blocks_export"] is True and stp["reason_code"] == "HIGHLIGHT_NOT_FOUND"
