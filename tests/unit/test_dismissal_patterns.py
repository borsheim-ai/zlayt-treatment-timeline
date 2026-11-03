"""T-089: dismissal-pattern suggestions for the single local profile. Read-only suggestions; never auto-dismiss; no effect on pipeline output."""
import pytest
from fastapi.testclient import TestClient

from app.backend import dismissal_patterns as DP, pipeline as PL
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record as wr
from tests.unit.test_review_rules import seeded

NEW_ONSET = "New onset pain radiating to right arm with numbness in fingers."


def add_flag(conn, case, fid, *, category="new_onset", text=NEW_ONSET, type_="causation", origin="lexicon+llm", status=None):
    DB.add_item(conn, case, "flag", {"id": fid, "type": type_, "category": category, "origin": origin, "title": "t", "explanation": "e",
                "evidence_json": [{"record_no": 1, "text": text, "start": 0, "end": len(text)}], "state": "verified", "state_reasons_json": []})
    if status:
        DB.apply_review(conn, fid, status, now=1.0, case=case)


def snapshot(conn, case):
    return [(f["id"], f["review_status"], f["state"]) for f in DB.list_items(conn, case, "flag")]


def test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(3):
        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    before = snapshot(conn, cid)
    s = DP.suggest(conn, cid)
    assert len(s) == 1 and s[0]["kind"] == "phrase" and s[0]["dismissed_count"] == 3 and s[0]["auto_applied"] is False
    assert s[0]["message"] == "You dismissed this kind of flag 3 times. Hide similar ones in this case?"
    assert "f_r7_2" in s[0]["flag_ids"]                           # the sample's pending new_onset flag
    assert snapshot(conn, cid) == before                          # suggest() wrote nothing; the flag is still pending
    assert next(f for f in DB.list_items(conn, cid, "flag") if f["id"] == "f_r7_2")["review_status"] == "pending"


def test_two_dismissals_are_not_enough(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(2):
        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    assert DP.suggest(conn, cid) == []


def test_ineligible_flags_are_never_suggested(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(6):
        add_flag(conn, cid, f"f_g{i}", category="gap_over_30", type_="gap", origin="code", status="dismiss")
        add_flag(conn, cid, f"f_i{i}", category="injection_suspected", type_="record_warning", origin="code", status="dismiss")
    assert DP.suggest(conn, cid) == []


def test_category_suggestion_after_five_dismissals_of_different_phrases(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    texts = ["Pain began after the collision.", "Symptoms began after the accident.", "Onset after the fall.", "New onset of numbness.",
             "Developed pain after the accident."]
    for i, t in enumerate(texts):
        add_flag(conn, cid, f"f_c{i}", category="patient_report", text=t, status="dismiss")
    s = DP.suggest(conn, cid)
    cats = [x for x in s if x["kind"] == "category"]
    assert len(cats) == 1 and cats[0]["key"] == "category:patient_report" and cats[0]["dismissed_count"] == 5
    assert cats[0]["flag_ids"] == ["f_r9_1"] and cats[0]["label"] == "patient report"


def test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(3):
        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    key = DP.suggest(conn, cid)[0]["key"]
    n_events = len(DB.list_events(conn, cid))
    out = DP.apply(conn, cid, key, now=2.0)
    assert out["dismissed_flag_ids"] == ["f_r7_2"] and out["suggestions"] == []
    f = next(x for x in DB.list_items(conn, cid, "flag") if x["id"] == "f_r7_2")
    assert f["review_status"] == "dismissed" and f["reviewer_note"] == DP.APPLIED_NOTE
    assert len(DB.list_events(conn, cid)) == n_events + 1         # one logged dismiss event
    # a bulk-hidden flag is not a new manual dismissal: the count stays 3, not 4
    add_flag(conn, cid, "f_new")
    assert DP.suggest(conn, cid)[0]["dismissed_count"] == 3
    with pytest.raises(KeyError):
        DP.apply(conn, cid, "phrase:nope")


def test_scope_is_this_case_unless_local_profile(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    other = DB.create_case(conn, "x", now=1.0)
    for i in range(3):
        add_flag(conn, other, f"f_o{i}", status="dismiss")
    assert DP.suggest(conn, cid, local=False) == []
    s = DP.suggest(conn, cid, local=True)
    assert len(s) == 1 and s[0]["scope"] == "all cases on this computer"


def _client(tmp_path, monkeypatch, name, mode=None):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    if mode:
        monkeypatch.setenv("ZLAYT_MODE", mode)
    else:
        monkeypatch.delenv("ZLAYT_MODE", raising=False)
    db = str(tmp_path / name)
    return TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000)), db


def test_routes_apply_and_errors(tmp_path, monkeypatch):
    from tests.unit.test_api_routes import run_case
    c, db = _client(tmp_path, monkeypatch, "r.sqlite")
    t = run_case(c)
    conn = DB.connect(db)
    for i in range(3):
        add_flag(conn, t, f"f_old{i}", status="dismiss")
    conn.close()
    r = c.get(f"/api/cases/{t}/dismissal_suggestions")
    assert r.status_code == 200 and r.json()["suggestions"][0]["dismissed_count"] == 3
    assert c.get("/api/cases/nope/dismissal_suggestions").status_code == 404
    assert c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={}).status_code == 400
    assert c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={"key": "phrase:zzz"}).status_code == 404
    key = r.json()["suggestions"][0]["key"]
    a = c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={"key": key})
    assert a.status_code == 200 and a.json()["dismissed_flag_ids"] and a.json()["suggestions"] == []


def _two_cases(c, db):
    """Case A holds three dismissals of a phrase; case B (a different token) holds only the pending match."""
    from tests.unit.test_api_routes import run_case
    a, b = run_case(c), run_case(c)
    assert a != b
    conn = DB.connect(db)
    for i in range(3):
        add_flag(conn, a, f"f_a_old{i}", status="dismiss")
    add_flag(conn, b, "f_b_pending")
    conn.close()
    return a, b


def test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route(tmp_path, monkeypatch):
    """Demo/public mode: case B sees nothing from case A; apply refuses; a forced-local route (mutant) fails this test."""
    c, db = _client(tmp_path, monkeypatch, "pub.sqlite")
    a, b = _two_cases(c, db)
    assert c.get(f"/api/cases/{b}/dismissal_suggestions").json()["suggestions"] == []
    assert c.post(f"/api/cases/{b}/dismissal_suggestions/apply", json={"key": "phrase:new_onset"}).status_code == 404
    pend = lambda: [f for f in DB.list_items(DB.connect(db), b, "flag") if f["id"] == "f_b_pending"][0]["review_status"]   # noqa: E731
    assert pend() == "pending"                                       # nothing was hidden in B by A's history
    own = c.get(f"/api/cases/{a}/dismissal_suggestions").json()["suggestions"]       # A's own history still counts for A, scoped to A
    assert len(own) == 1 and own[0]["scope"] == "this case" and "f_b_pending" not in own[0]["flag_ids"]


def test_local_mode_counts_the_machine_profile_through_the_route(tmp_path, monkeypatch):
    c, db = _client(tmp_path, monkeypatch, "loc.sqlite", mode="local")
    a, b = _two_cases(c, db)
    s = c.get(f"/api/cases/{b}/dismissal_suggestions").json()["suggestions"]
    assert len(s) == 1 and s[0]["scope"] == "all cases on this computer" and s[0]["dismissed_count"] == 3 and "f_b_pending" in s[0]["flag_ids"]


@pytest.mark.parametrize("case", G.case_names())
def test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged(tmp_path, case):
    """Same case through the pipeline with and without a dismissal history in the database: identical flags, entries and amounts.
    The history is built from the case's OWN flags (same type, category, origin and quoted phrase, 8 dismissals each), so a pipeline that
    let history filter flags would change this case's output; a case with no eligible flag also gets the generic new_onset history."""
    def run(history_from):
        conn = DB.connect(str(tmp_path / f"{case}-{bool(history_from)}.sqlite"))
        if history_from is not None:
            hist = DB.create_case(conn, "history", now=1.0)
            for n, f in enumerate(history_from * 8 or [None]):
                if f is None:
                    add_flag(conn, hist, f"f_h{n}", status="dismiss")
                else:
                    add_flag(conn, hist, f"f_h{n}", category=f["category"], text=f["evidence"][0]["text"], type_=f["type"], origin=f["origin"], status="dismiss")
        cid = DB.create_case(conn, G.raw(case), now=1.0)
        def extract(u):
            ex = G.record(case, wr(u, case)[0])["excerpt"].split(". ")[0].rstrip(".") + "."
            return dict(summary=ex, excerpt=ex)
        PL.run_pipeline(conn, cid, G.raw(case), call=FakeCall(sample_script() if case == "sample" else sample_script(extract=extract)), now=lambda: 1.0)
        view = {k: [(i["id"], i.get("category"), i["state"], i["review_status"]) for i in DB.list_items(conn, cid, k)] for k in ("entry", "amount", "flag")}
        DP.suggest(conn, cid, local=True)                          # computing suggestions after the run must not matter either
        assert {k: [(i["id"], i.get("category"), i["state"], i["review_status"]) for i in DB.list_items(conn, cid, k)] for k in view} == view
        flags = [f for f in DB.list_items(conn, cid, "flag") if DP._eligible(f) and f.get("evidence")]
        return view, flags
    base, flags = run(None)
    seeded_view, _ = run(flags)
    assert base == seeded_view
    assert base == run([])[0]


def test_eligibility_rules_are_each_enforced_on_their_own(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(6):
        add_flag(conn, cid, f"f_gl{i}", category="gap_over_30", type_="gap", origin="lexicon+llm", status="dismiss")      # right origin, wrong type
        add_flag(conn, cid, f"f_rw{i}", category="new_onset", type_="record_warning", origin="lexicon+llm", status="dismiss")
        add_flag(conn, cid, f"f_llm{i}", category="new_onset", type_="pre_existing", origin="llm", status="dismiss")          # right type, no lexicon
    assert DP.suggest(conn, cid) == []
    add_flag(conn, cid, "f_ok", type_="pre_existing", origin="lexicon", status=None)
    assert DP.suggest(conn, cid) == []                              # ineligible history never counts toward an eligible pending flag


def test_category_threshold_is_exactly_five(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    texts = ["Pain began after the collision.", "Symptoms began after the accident.", "Onset after the fall.", "New onset of numbness."]
    for i, t in enumerate(texts):
        add_flag(conn, cid, f"f_c{i}", category="patient_report", text=t, status="dismiss")
    assert [x for x in DP.suggest(conn, cid) if x["kind"] == "category"] == []             # 4 is not enough
    add_flag(conn, cid, "f_c4", category="patient_report", text="Developed pain after the accident.", status="dismiss")
    assert [x["dismissed_count"] for x in DP.suggest(conn, cid) if x["kind"] == "category"] == [5]
