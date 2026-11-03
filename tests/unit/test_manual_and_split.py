"""T-056 (D-031): manual entry for a rejected record (whole verbatim sentences, 422 otherwise, never auto-accepted) and 'not a duplicate' split."""
import pytest
from app.backend import export as X, pipeline as PL, review as RV, store
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, sample_script, which_record
from tests.unit.test_review_rules import judge


def sample_with_rejected_5(tmp_path):
    sums = golden_summaries()

    def extract(u):
        n = which_record(u)[0]
        if n == 5:     # a quote that is not in the record: grounding rejects it, so record 5 has no usable entry
            return dict(summary="Pain improving.", excerpt="Pain is much better today.")
        return dict(summary=sums[n][0], excerpt=sums[n][1])
    call = FakeCall(sample_script(extract=extract))
    conn = DB.connect(str(tmp_path / "m.sqlite")); cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
    return conn, cid


def test_record_5_has_no_live_entry(tmp_path):
    conn, cid = sample_with_rejected_5(tmp_path)
    assert not [e for e in DB.list_items(conn, cid, "entry") if "r5" in e["record_ids"] and e["state"] != "rejected"]


@pytest.mark.parametrize("excerpt", ["Pain 4/10, impr", "improving.", "Patient reports missing 3 days", "Something else entirely."])
def test_manual_entry_requires_whole_verbatim_sentences(tmp_path, excerpt):
    conn, cid = sample_with_rejected_5(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.manual_entry(conn, cid, "r5", {"summary": "Pain 4/10.", "excerpt": excerpt}, call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit")
    assert not [x for x in DB.list_items(conn, cid, "entry") if x["id"].endswith("_m")]


def test_manual_entry_is_pending_labelled_logged_and_exports_only_after_accept(tmp_path):
    conn, cid = sample_with_rejected_5(tmp_path)
    r = RV.manual_entry(conn, cid, "r5", {"summary": "Pain 4/10, improving.", "excerpt": "Pain 4/10, improving."}, call=judge("supported"))
    it = r["item"]
    assert it["id"] == "e5_m" and it["review_status"] == "pending" and it["entered_by_reviewer"] and not it["ai_drafted"]
    assert it["date"] == "2026-02-20" and it["provider"] == "Capital PT, visit 8"          # from the header, not from the writer
    assert any(ev["action"] == "manual_entry" and ev["item_id"] == "e5_m" for ev in DB.list_events(conn, cid))
    before = X.build_export(store.export_case(conn, cid))
    assert "February 20, 2026" not in before["letter_text"]                              # never auto-accepted
    RV.apply_review(conn, cid, "e5_m", {"action": "accept"}, call=judge("supported"))
    after = X.build_export(store.export_case(conn, cid))
    assert "February 20, 2026 — Capital PT, visit 8" in after["letter_text"] and "entered by reviewer" not in after["letter_text"]
    assert "entered by reviewer" in after["internal_notes_text"].split("EDITED ITEMS")[1].split("PENDING ITEMS")[0]


@pytest.mark.parametrize("confirm", [False, True])
def test_manual_entry_summary_with_new_number_is_a_hard_422(tmp_path, confirm):
    """D-034: no override for a number absent from the quote."""
    conn, cid = sample_with_rejected_5(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.manual_entry(conn, cid, "r5", {"summary": "Pain 9/10.", "excerpt": "Pain 4/10, improving.", "confirm_warnings": confirm}, call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit")
    assert not [x for x in DB.list_items(conn, cid, "entry") if x["id"].endswith("_m")]


@pytest.mark.parametrize("confirm", [False, True])
@pytest.mark.parametrize("summary", ["No pain, improving.", "Left-sided pain, improving.", "Pain improving without medication.", "Pain not improving."])
def test_manual_entry_side_or_negation_not_in_quote_is_a_hard_422_d047(tmp_path, summary, confirm):
    """D-047: a side/negation word absent from the quote is refused with no override; nothing is stored, no judge call, no event."""
    conn, cid = sample_with_rejected_5(tmp_path)
    events = DB.list_events(conn, cid)
    calls = []
    def spy(*a, **k):
        calls.append(1); return judge("supported")(*a, **k)
    with pytest.raises(RV.ReviewError) as e:
        RV.manual_entry(conn, cid, "r5", {"summary": summary, "excerpt": "Pain 4/10, improving.", "confirm_warnings": confirm}, call=spy)
    assert (e.value.status, e.value.code) == (422, "invalid_edit") and e.value.detail["reason"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and e.value.detail["tokens"]
    assert not [x for x in DB.list_items(conn, cid, "entry") if x["id"].endswith("_m")]
    assert DB.list_events(conn, cid) == events and calls == []


def test_manual_entry_judge_objection_saves_pending_with_warning_and_no_override_note(tmp_path):
    conn, cid = sample_with_rejected_5(tmp_path)
    body = {"summary": "Pain improving, treatment effective.", "excerpt": "Pain 4/10, improving."}
    r = RV.manual_entry(conn, cid, "r5", body, call=judge("unsupported"))             # D-047: no 409; the judge never blocks a human-written entry
    assert "JUDGE_UNSUPPORTED" in [w["code"] for w in r["warnings"]] and r["item"]["state"] == "needs_review"
    assert not [x for x in DB.list_events(conn, cid) if x["action"] == "keep_my_wording"]
    assert r["item"]["entered_by"] == "reviewer"
    notes = X.build_export(store.export_case(conn, cid))["internal_notes_text"]
    pend = notes.split("PENDING ITEMS NOT INCLUDED")[1]
    assert "[entered by reviewer]" in pend                                            # label before accept
    RV.apply_review(conn, cid, "e5_m", {"action": "accept", "compared": True})      # D-066: the judge objected
    sec = X.build_export(store.export_case(conn, cid))["internal_notes_text"].split("EDITED ITEMS")[1].split("PENDING ITEMS")[0]
    assert "entered by reviewer" in sec and "keep my wording" not in sec and "override" not in sec


def test_manual_entry_refused_when_record_has_a_live_entry(tmp_path):
    conn, cid = sample_with_rejected_5(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.manual_entry(conn, cid, "r1", {"summary": "x.", "excerpt": "Alert and oriented."}, call=judge("supported"))
    assert e.value.status == 422


# ---------------------------------------------------------------- not a duplicate
CASE = "case_04_duplicates_no_amounts"


def seeded_case4(tmp_path):
    def extract(u):
        n = which_record(u, CASE)[0]
        s = G.record(CASE, n)["excerpt"].split(". ")[0].rstrip(".") + "."
        return dict(summary=s, excerpt=s)
    call = FakeCall(sample_script(extract=extract))
    conn = DB.connect(str(tmp_path / "d.sqlite")); cid = DB.create_case(conn, G.raw(CASE), now=1.0)
    PL.run_pipeline(conn, cid, G.raw(CASE), call=call, now=lambda: 1.0)
    return conn, cid, call


def test_not_a_duplicate_splits_the_pair_with_an_event(tmp_path):
    conn, cid, call = seeded_case4(tmp_path)
    merged = next(e for e in DB.list_items(conn, cid, "entry") if "r2" in e["record_ids"])
    assert merged["record_ids"] == ["r1", "r2"] and len(DB.list_items(conn, cid, "entry")) == 4
    r = RV.not_duplicate(conn, cid, merged["id"], "r2", call=call)
    ents = {e["id"]: e for e in DB.list_items(conn, cid, "entry")}
    assert len(ents) == 5 and ents[merged["id"]]["record_ids"] == ["r1"] and ents["e2"]["record_ids"] == ["r2"]
    assert r["entry_ids"] == [merged["id"], "e2"]
    assert [ev for ev in DB.list_events(conn, cid) if ev["action"] == "not_duplicate" and ev["item_id"] == merged["id"]]
    assert DB.get_case(conn, cid)["config"]["not_duplicates"] == ["r2"]
    assert conn.execute("SELECT duplicate_of FROM records WHERE id='r2' AND case_id=?", (cid,)).fetchone()[0] is None


def test_split_survives_a_rerun(tmp_path):
    conn, cid, call = seeded_case4(tmp_path)
    RV.not_duplicate(conn, cid, "e1", "r2", call=call)
    PL.run_pipeline(conn, cid, G.raw(CASE), call=call, now=lambda: 2.0)
    assert sorted(e["id"] for e in DB.list_items(conn, cid, "entry")) == ["e1", "e2", "e3", "e5", "e6"]


@pytest.mark.parametrize("rid", ["r1", "r5", "r99"])
def test_not_a_duplicate_only_for_a_merged_non_primary_record(tmp_path, rid):
    conn, cid, call = seeded_case4(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.not_duplicate(conn, cid, "e1", rid, call=call)
    assert e.value.status == 422


# ---------------------------------------------------------------- HTTP
def test_routes_exist_and_validate(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from app.backend.api import create_app
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    c = TestClient(create_app(str(tmp_path / "h.sqlite"), static_dir=str(tmp_path)))
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    r = c.post(f"/api/cases/{tok}/records/r5/entry", json={"summary": "Pain 4/10.", "excerpt": "Pain 4/10, impr"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_edit"
    assert c.post(f"/api/cases/{tok}/records/r99/entry", json={"summary": "x", "excerpt": "y"}).status_code == 404
    assert c.post(f"/api/cases/{tok}/items/e1/not_duplicate", json={}).status_code == 400
    assert c.post(f"/api/cases/{tok}/items/e1/not_duplicate", json={"record_id": "r1"}).status_code in (404, 422)


# ---------------------------------------------------------------- the duplicate's charge follows the split (T-056 review B2)
TWO = """=== Record 1 ===
Date: 2026-03-02
Source: Capital Imaging
Excerpt: "Cervical MRI performed. Charge: $310."

=== Record 2 ===
Date: 2026-03-02
Source: Capital Imaging
Excerpt: "Cervical MRI performed. Charge: $310."
"""


def seeded_two(tmp_path):
    call = FakeCall(sample_script(extract=lambda u: dict(summary="Cervical MRI performed.", excerpt="Cervical MRI performed.")))
    conn = DB.connect(str(tmp_path / "t.sqlite")); cid = DB.create_case(conn, TWO, now=1.0)
    PL.run_pipeline(conn, cid, TWO, call=call, now=lambda: 1.0)
    return conn, cid, call


def amounts(conn, cid):
    return sorted((a["id"], tuple(a["record_ids"]), a["value_cents"], a["review_status"]) for a in DB.list_items(conn, cid, "amount"))


def test_duplicate_charge_moves_to_the_split_record_and_survives_rerun(tmp_path):
    conn, cid, call = seeded_two(tmp_path)
    assert amounts(conn, cid) == [("a1", ("r1",), 31000, "pending")]            # the duplicate contributes nothing while merged
    RV.not_duplicate(conn, cid, "e1", "r2", call=call)
    assert amounts(conn, cid) == [("a1", ("r1",), 31000, "pending"), ("ax2_1", ("r2",), 31000, "pending")]
    for aid in ("a1", "ax2_1"):
        RV.apply_review(conn, cid, aid, {"action": "accept"})
    for e in DB.list_items(conn, cid, "entry"):
        RV.apply_review(conn, cid, e["id"], {"action": "accept"})
    assert "Billed charges accepted from these records: $620.00" in X.build_export(store.export_case(conn, cid))["letter_text"].split("\n")
    PL.run_pipeline(conn, cid, TWO, call=call, now=lambda: 2.0)                       # rerun keeps both, with their review status
    assert amounts(conn, cid) == [("a1", ("r1",), 31000, "accepted"), ("ax2_1", ("r2",), 31000, "accepted")]
    assert "Billed charges accepted from these records: $620.00" in X.build_export(store.export_case(conn, cid))["letter_text"].split("\n")


@pytest.mark.parametrize("confirm", [False, True])
@pytest.mark.parametrize("summary", ["Patient reports pain 4/10, improving.", "Pain 4/10, possibly improving.", "Pain approximately 4/10, improving.",
                                     "Pain 4/10, likely improving.", "Pain about 4/10, improving.", "Patient denies radiating symptoms, pain 4/10.", "Bilateral pain 4/10, improving."])
def test_manual_entry_added_qualifier_or_wide_negation_not_in_quote_is_a_hard_422_d047(tmp_path, summary, confirm):
    conn, cid = sample_with_rejected_5(tmp_path)
    events, calls = DB.list_events(conn, cid), []
    def spy(*a, **k):
        calls.append(1); return judge("supported")(*a, **k)
    with pytest.raises(RV.ReviewError) as e:
        RV.manual_entry(conn, cid, "r5", {"summary": summary, "excerpt": "Pain 4/10, improving.", "confirm_warnings": confirm}, call=spy)
    assert (e.value.status, e.value.code) == (422, "invalid_edit") and e.value.detail["reason"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and e.value.detail["tokens"]
    assert not [x for x in DB.list_items(conn, cid, "entry") if x["id"].endswith("_m")]
    assert DB.list_events(conn, cid) == events and calls == []
