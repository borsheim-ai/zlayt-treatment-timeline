"""T-134 (paralegal pass 4 M2; D-045b, D-051): an edited entry that is still needs_review has not been decided.
It is not in the letter, not counted as accepted, listed by the gate as EDIT_NOT_CONFIRMED (a warning: it is not in the letter, so it blocks nothing),
and the notes never say the paralegal accepted it. Her explicit Accept (after comparing with the quote) is still bound by the code checks (422)."""
import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from app.db import db as DB
from tests.unit.test_api_routes import run_case

EDIT = "Persistent neck pain 6/10 with daily headaches noted."


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "t134.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _gate(c, tok):
    return next(s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"] if s["id"] == "export_gate")


def _setup(c, accept=("e1",)):
    tok = run_case(c)
    for i in accept:
        assert c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept"}).status_code == 200
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"summary": EDIT}})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "edited" and r.json()["item"]["state"] == "needs_review"
    return tok, r.json()


def test_edit_with_no_second_check_is_not_in_the_letter_and_not_counted_accepted(env):
    _, c = env
    tok, r = _setup(c)
    assert r["item"]["edit_to_check"] is True
    assert r["review"]["counts"]["edit_to_check"] == 1
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 200
    j = ex.json()
    assert EDIT not in j["letter_text"] and "daily headaches" not in j["letter_text"]
    assert "e3" not in [e["id"] for e in j["items"]["entries"]]
    assert j["counts"]["entries"] == 1 and j["counts"]["pending"] >= 1
    assert j["excluded"]["edit_not_confirmed"] == 1
    assert j["provenance"]["edited_count"] == 0
    notes = j["internal_notes_text"]
    assert "edited; second check not available" in notes and "JUDGE_UNAVAILABLE" not in notes      # T-167: the code stays in the API fields, not the notes
    assert "not yet confirmed" in notes
    before_edited = notes.split("EDITED ITEMS")[1].split("PENDING ITEMS NOT INCLUDED")[0]
    assert "not in the letter" in before_edited and EDIT in before_edited
    assert "Items not reviewed: 0" not in notes


def test_gate_names_the_unconfirmed_edit_as_a_warning_and_agrees_with_the_export(env):
    _, c = env
    tok, _ = _setup(c)
    g = _gate(c, tok)
    assert g["ready"] is True and g["blockers"] == []          # not in the letter, so it does not block (the same rule as a pending item, D-045a)
    w = {x["reason_code"]: x for x in g["warnings"]}
    assert w["EDIT_NOT_CONFIRMED"]["count"] == 1 and "second check" in w["EDIT_NOT_CONFIRMED"]["why"]
    assert g["counts"]["edit_not_confirmed"] == 1 and g["counts"]["accepted"] == 1
    assert c.get(f"/api/cases/{tok}/export").status_code == 200       # ready == export allowed


def test_only_an_unconfirmed_edit_accepted_means_nothing_accepted(env):
    _, c = env
    tok, r = _setup(c, accept=())
    assert r["review"]["ready_to_export"] is False
    g = _gate(c, tok)
    assert g["ready"] is False and [b["reason_code"] for b in g["blockers"]] == ["NOTHING_ACCEPTED"]
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 422 and ex.json()["error"]["detail"]["blockers"][0]["reason_code"] == "NOTHING_ACCEPTED"


def test_explicit_accept_after_comparing_moves_it_into_the_letter_and_the_notes_keep_the_reason(env):
    _, c = env
    tok, _ = _setup(c)
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "accepted" and r.json()["item"]["edit_to_check"] is False
    assert r.json()["review"]["counts"]["edit_to_check"] == 0
    j = c.get(f"/api/cases/{tok}/export").json()
    assert EDIT in j["letter_text"] and "e3" in [e["id"] for e in j["items"]["entries"]]
    assert "EDIT_NOT_CONFIRMED" not in [w["reason_code"] for w in _gate(c, tok)["warnings"]]
    notes = j["internal_notes_text"]
    assert "second check not available" in notes.split("EDITED ITEMS")[1].split("PENDING ITEMS NOT INCLUDED")[0]


def test_accept_after_comparing_is_a_422_when_the_stored_wording_fails_a_code_check(env):
    db, c = env
    tok, _ = _setup(c)
    conn = DB.connect(db)
    row = DB.get_item(conn, "e3", tok)
    ed = dict(row["edited"], summary="Persistent neck pain 9/10 with daily headaches noted.")      # old data: a figure the quote does not carry
    DB.apply_review(conn, "e3", "edit", edited=ed, now=1.0, case=tok)       # straight into the DB: the edit route would refuse it
    conn.close()
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "CODE_CHECK_FAILED"
    assert [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == "e3"][0]["review_status"] == "edited"      # nothing was written
    g = _gate(c, tok)
    assert g["ready"] is False and any(b["reason_code"] == "SUMMARY_TOKEN_NOT_IN_EXCERPT" for b in g["blockers"])      # D-051: the gate still blocks it


def test_a_verified_edit_is_unaffected(env):
    """An edit the second check supports is state verified: in the letter at once, no warning."""
    _, c = env
    tok = run_case(c)
    r = c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
    assert r.status_code == 200 and r.json()["item"]["edit_to_check"] is False
    assert "EDIT_NOT_CONFIRMED" not in [w["reason_code"] for w in _gate(c, tok)["warnings"]]


# ------------------------------------------------------------------ round 2 (staff-engineer findings 1-4)
def _item_trace(c, tok, iid):
    t = c.get(f"/api/cases/{tok}/items/{iid}/trace").json()
    return t, {s["id"]: s for s in t["steps"]}


def _dismiss_all_but(c, db, tok, keep):
    """Dismiss every live pending item except `keep`, so the only open thing is the edit."""
    conn = DB.connect(db)
    ids = [r["id"] for k in ("entry", "amount", "flag") for r in DB.list_items(conn, tok, k) if r["state"] != "rejected" and r["review_status"] == "pending" and r["id"] not in keep]
    conn.close()
    for i in ids:
        assert c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "dismiss"}).status_code == 200


def test_item_trace_of_an_open_edit_does_not_say_accepted(env):
    """Finding 1: the 'Why this status' trail must not claim her acceptance of an edit that is still open."""
    _, c = env
    tok, _ = _setup(c)
    t, s = _item_trace(c, tok, "e3")
    assert t["verdict"]["code"] == "edit_to_check" and "accepted" not in t["verdict"]["label"].lower()
    assert t["verdict"]["label"] == "Edited; waiting for your check" and t["verdict"]["blocks_export"] is False
    h = s["human"]
    assert h["status"] == "pending" and h["reason_code"] == "EDIT_NOT_CONFIRMED" and h["next_action"]["code"] == "DECIDE"
    assert "accepted it" not in h["why"] and "not accepted" in h["why"] and "compare" in h["why"]
    assert h["blocks_export"] is False
    # her explicit accept ends it, and only then does the trail say accepted
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
    t, s = _item_trace(c, tok, "e3")
    assert t["verdict"]["code"] == "accepted" and t["verdict"]["label"] == "Accepted by you" and s["human"]["status"] == "pass"


def test_item_trace_of_an_open_excerpt_only_edit_is_also_not_accepted(env):
    db, c = env
    tok, _ = _setup(c)
    conn = DB.connect(db)
    row = DB.get_item(conn, "e5", tok)
    DB.apply_review(conn, "e5", "edit", edited={"excerpt": row["excerpt"], "original_excerpt": row["excerpt"], "at": "2026-11-02T00:00:00Z"}, now=1.0, case=tok)
    DB.update_item(conn, "e5", case=tok, state="needs_review", state_reasons_json=["JUDGE_UNAVAILABLE"])
    conn.close()
    e5 = [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == "e5"][0]
    assert e5["review_status"] == "edited" and e5["edit_to_check"] is True       # an excerpt-only edit is open too
    t, s = _item_trace(c, tok, "e5")
    assert t["verdict"]["code"] == "edit_to_check" and s["human"]["status"] == "pending"
    assert c.get(f"/api/cases/{tok}/export").json()["excluded"]["edit_not_confirmed"] == 2


def test_a_verified_edit_trail_still_says_accepted(env):
    """An edit whose state is not needs_review is decided by the edit (D-045b): the trail keeps its 'edited and accepted' wording."""
    db, c = env
    tok, _ = _setup(c)
    conn = DB.connect(db)
    DB.update_item(conn, "e3", case=tok, state="verified", state_reasons_json=[])
    conn.close()
    t, s = _item_trace(c, tok, "e3")
    assert t["verdict"]["code"] == "accepted" and s["human"]["status"] == "pass" and "accepted" in s["human"]["why"]


def test_everything_else_decided_the_open_edit_alone_keeps_review_and_header_not_ready(env):
    """Findings 2 (M7, M12, M15): with nothing else pending, the open edit still holds ready_to_export, the review step and the header label."""
    db, c = env
    tok, r = _setup(c)
    _dismiss_all_but(c, db, tok, {"e1", "e3"})
    rv = c.get(f"/api/cases/{tok}").json()["review"]
    assert rv["counts"]["pending"] == 0 and rv["counts"]["edit_to_check"] == 1
    assert rv["ready_to_export"] is False                                          # M7: one accepted entry, one open edit: not "decided"
    ct = c.get(f"/api/cases/{tok}/trace").json()
    review = next(s for s in ct["steps"] if s["id"] == "review")
    assert review["status"] == "pending" and review["reason_code"] == "EDIT_NOT_CONFIRMED"      # M12
    assert ct["verdict"] == {"code": "ready", "label": "Ready to export (1 not reviewed)"}      # M15: the gate passes, the header still counts the open edit
    assert c.get(f"/api/cases/{tok}/export").status_code == 200
    c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"})
    rv = c.get(f"/api/cases/{tok}").json()["review"]
    assert rv["ready_to_export"] is True
    assert next(s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"] if s["id"] == "review")["status"] == "pass"


def test_judges_step_ignores_a_human_edit_whose_rerun_check_was_unavailable_under_the_curated_set(env, monkeypatch, tmp_path):
    """Finding 4: under FIXTURE_SET=curated the edit route's second check has no fixture; her own wording needs none (D-045b), so the case
    checks banner must not ask her to re-run it for an item that is out of the letter."""
    monkeypatch.setenv("FIXTURE_SET", "curated")
    db = str(tmp_path / "cur.sqlite")
    c = TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    tok = run_case(c)
    assert c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"}).status_code == 200
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"summary": EDIT}})
    assert r.status_code == 200 and r.json()["item"]["edit_to_check"] is True
    ct = c.get(f"/api/cases/{tok}/trace").json()
    j = next(s for s in ct["steps"] if s["id"] == "judges")
    assert j["status"] != "fail" and j["counts"]["unavailable"] == 0
    jr = c.get(f"/api/cases/{tok}/judges").json()
    assert jr["totals"]["unavailable"] == 0 and "e3" not in [u["item_id"] for u in jr["unresolved"]]


# ---- T-134 round 3 (staff-engineer r2): the judge report, the item next_action, and the narrow judges-step skip

def _object(db, tok, iid, verdict="partially", code="PARTIAL", reasons=("JUDGE_PARTIAL",)):
    """Store an objecting second-check result on the item, as the edit route does when the re-check disagrees with her new wording."""
    conn = DB.connect(db)
    row = DB.get_item(conn, iid, tok)
    lad = dict(row["ladder"])
    lad["judge"] = dict(lad["judge"], verdict=verdict, reason_code=code)
    DB.update_item(conn, iid, case=tok, ladder=lad, state="needs_review", state_reasons_json=list(reasons))
    conn.close()


def test_judge_report_does_not_count_an_open_edit_as_accepted_despite_an_objection(env):
    """Reviewer r2 major: 'you accepted despite an objection' (human_overrides) is her explicit accept; an edit she has not accepted is not one.
    The objection itself stays in the report either way (D-045b: her wording is exempt from blocking, not from being reported)."""
    db, c = env
    tok, _ = _setup(c)
    _object(db, tok, "e3")
    rep = c.get(f"/api/cases/{tok}/judges").json()
    assert rep["totals"]["human_overrides"] == 0
    assert "e3" in [r["item_id"] for r in rep["rejections"]] and rep["totals"]["unsupported"] == 1       # still reported, still counted as an objection
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 422      # D-066: the second check objected, so accepting needs her compare
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept", "compared": True}).status_code == 200
    rep = c.get(f"/api/cases/{tok}/judges").json()
    assert rep["totals"]["human_overrides"] == 1 and "e3" in [r["item_id"] for r in rep["rejections"]]       # accepted despite the objection: now it counts


def test_judges_step_keeps_a_human_edit_whose_recheck_objected(env):
    """Reviewer r2 N5: the skip is for an UNAVAILABLE re-check only. An objecting verdict on her wording stays in the case checks step."""
    db, c = env
    tok, _ = _setup(c)
    _object(db, tok, "e3")
    j = next(s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"] if s["id"] == "judges")
    assert j["status"] != "pass"                                              # the objection is still on the case-level step
    rep = c.get(f"/api/cases/{tok}/judges").json()
    assert [r["verdict"] for r in rep["rejections"] if r["item_id"] == "e3"] == ["partially"]


def test_item_next_action_of_an_open_edit_is_decide(env):
    """Reviewer r2 N3: the UI reads the item-level next_action; for an open edit it is DECIDE (accept or dismiss), not nothing."""
    _, c = env
    tok, _ = _setup(c)
    t, _s = _item_trace(c, tok, "e3")
    assert t["next_action"] and t["next_action"]["code"] == "DECIDE"


# ---- T-134 round 3, T-136 paralegal F-2: a re-picked quote under AI wording whose second check has no answer
# D-044 stands (nothing AI-written reaches the letter without the second check), so the words must not promise what accept alone cannot do.

QUOTE_ONLY = "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. "     # e3's own quote re-picked (same sentences; the summary stays the AI's)


def _quote_pick(c, tok):
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"excerpt": QUOTE_ONLY}})
    assert r.status_code == 200 and r.json()["item"]["edit_to_check"] is True, r.text
    return r


def test_open_quote_edit_with_ai_summary_and_no_second_check_says_accept_alone_will_not_put_it_in_the_letter(env):
    _, c = env
    tok = run_case(c)
    assert c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"}).status_code == 200
    _quote_pick(c, tok)
    t, s = _item_trace(c, tok, "e3")
    why = s["human"]["why"]
    assert "second" in why and "check" in why and "accepting alone" in why.lower()
    g = _gate(c, tok)
    w = next(x for x in g["warnings"] if x["reason_code"] == "EDIT_NOT_CONFIRMED")
    assert "second" in w["why"] and "check" in w["why"] and "accept" in w["why"]


def test_open_edit_of_her_own_wording_keeps_the_plain_compare_and_accept_text(env):
    """Her own summary is exempt from the second check (D-045b), so compare-and-accept is the whole step for it."""
    _, c = env
    tok, _ = _setup(c)
    t, s = _item_trace(c, tok, "e3")
    assert "accepting alone" not in s["human"]["why"].lower()
    w = next(x for x in _gate(c, tok)["warnings"] if x["reason_code"] == "EDIT_NOT_CONFIRMED")
    assert "second AI check" not in w["why"]


def test_accepted_quote_edit_blocks_with_a_reason_that_says_the_rerun_was_tried_and_gave_no_answer(env):
    """After accept the block is D-044's (unchanged). Before a rerun the text offers the rerun; after a rerun that still has no answer it says so
    and names what does clear it (the check answering, or her own wording)."""
    _, c = env
    tok = run_case(c)
    _quote_pick(c, tok)
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 422 and ex.json()["error"]["code"] == "judge_not_run" and "Run the second check again" in ex.json()["error"]["message"]
    b = next(x for x in _gate(c, tok)["blockers"] if x["item_id"] == "e3")
    assert "tried again" not in b["why"]
    r = c.post(f"/api/cases/{tok}/rejudge")
    assert r.status_code == 200 and [x["item_id"] for x in r.json()["still_unavailable"]] == ["e3"]
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 422
    msg = ex.json()["error"]["message"]
    assert "ran again" in msg and "no answer" in msg and "edit the summary" in msg
    b = next(x for x in _gate(c, tok)["blockers"] if x["item_id"] == "e3")
    assert "ran again" in b["why"] and "no answer" in b["why"]
    # the way out is real: her own summary wording is exempt (D-045b) and passes the code checks
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"summary": "Persistent neck pain 6/10, daily headaches."}})
    assert r.status_code == 200
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
    assert c.get(f"/api/cases/{tok}/export").status_code == 200


# ---- T-134 round 4 (staff-engineer r3 bounded fix-up, section 7.4): every renderer of the re-picked-quote state, a rerun claim tied to the CURRENT quote, an explicit item field
def _rejudge_no_answer(c, tok):
    r = c.post(f"/api/cases/{tok}/rejudge")
    assert r.status_code == 200 and "e3" in [x["item_id"] for x in r.json()["still_unavailable"]]


def test_review_step_of_a_quote_pick_under_the_ai_summary_says_accepting_alone_will_not_put_it_in_the_letter(env):
    """r3 finding 1a: with everything else decided, the review step is the text she reads last; it must not promise that accept puts the entry in the letter."""
    db, c = env
    tok = run_case(c)
    _quote_pick(c, tok)
    _dismiss_all_but(c, db, tok, keep={"e3"})
    step = next(s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"] if s["id"] == "review")
    assert step["status"] == "pending" and step["reason_code"] == "EDIT_NOT_CONFIRMED"
    assert "accepting alone will not put it in the letter" in step["why"].lower()
    assert "or the entry stays out of the letter" not in step["why"]


def test_review_step_of_her_own_wording_keeps_the_plain_compare_and_accept_text(env):
    db, c = env
    tok, _ = _setup(c, accept=())
    _dismiss_all_but(c, db, tok, keep={"e3"})
    step = next(s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"] if s["id"] == "review")
    assert "accept, or the entry stays out of the letter" in step["why"] and "accepting alone" not in step["why"].lower()


def test_gate_headline_after_a_rerun_with_no_answer_is_the_same_sentence_as_the_422_and_does_not_repeat_the_action(env):
    """r3 finding 1b: one function says it (headline, 422 message), so they cannot drift."""
    _, c = env
    tok = run_case(c)
    _quote_pick(c, tok)
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
    g0 = _gate(c, tok)
    assert g0["why"].endswith("Run the second check again.") and "ran again" not in g0["why"]
    _rejudge_no_answer(c, tok)
    g = _gate(c, tok)
    msg = c.get(f"/api/cases/{tok}/export").json()["error"]["message"]
    assert g["why"] == msg and "ran again" in g["why"] and not g["why"].endswith("Run the second check again.")
    assert g["blockers"][0]["rerun_no_answer"] is True


def test_rerun_claim_is_about_the_current_quote_a_second_pick_clears_it(env):
    """r3 finding 2: the rerun ran on the first quote; after she picks another quote nobody has run the check on it, so no text may say it ran again."""
    db, c = env
    tok = run_case(c)
    _quote_pick(c, tok)
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
    _rejudge_no_answer(c, tok)
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"excerpt": QUOTE_ONLY.strip()}}).status_code == 200      # another pick (a summary-safe variant of the quote)
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
    conn = DB.connect(db)
    assert not (DB.get_item(conn, "e3", tok)["ladder"] or {}).get("rejudge")          # the attempts belonged to the old quote
    conn.close()
    b = next(x for x in _gate(c, tok)["blockers"] if x["item_id"] == "e3")
    assert b["rerun_no_answer"] is False and "ran again" not in b["why"]
    msg = c.get(f"/api/cases/{tok}/export").json()["error"]["message"]
    assert "ran again" not in msg and "Run the second check again" in msg
    assert "ran again" not in _gate(c, tok)["why"]
    _rejudge_no_answer(c, tok)                                                          # now it has run on this quote
    assert "ran again" in c.get(f"/api/cases/{tok}/export").json()["error"]["message"]


def test_rerun_gave_no_answer_reads_the_last_attempt_only():
    from app.backend import trace
    row = lambda *vs: {"ladder": {"rejudge": [{"verdict": v} for v in vs]}}      # noqa: E731
    assert trace.rerun_gave_no_answer(row("supported", "unavailable")) is True
    assert trace.rerun_gave_no_answer(row("unavailable", "supported")) is False
    assert trace.rerun_gave_no_answer(row("supported")) is False
    assert trace.rerun_gave_no_answer(row("unavailable")) is True
    assert trace.rerun_gave_no_answer(row()) is False and trace.rerun_gave_no_answer({}) is False and trace.rerun_gave_no_answer({"ladder": None}) is False


def test_no_text_says_the_export_stays_blocked_while_the_gate_passes(env):
    """r3 finding 3: before she accepts, nothing is blocked; the conditional is what is true."""
    _, c = env
    tok = run_case(c)
    assert c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"}).status_code == 200
    _quote_pick(c, tok)
    g = _gate(c, tok)
    assert g["ready"] is True and c.get(f"/api/cases/{tok}/export").status_code == 200
    w = next(x for x in g["warnings"] if x["reason_code"] == "EDIT_NOT_CONFIRMED")
    for text in (w["why"], g["why"], _item_trace(c, tok, "e3")[1]["human"]["why"]):
        assert "stays blocked" not in text and "stay blocked" not in text and "1 of it" not in text
        assert "If you accept it, the export will be blocked until the second check answers" in text and "in your own words" in text
    assert "It keeps the AI's summary" in w["why"]


def test_warning_for_her_own_wording_has_no_ai_clause(env):
    _, c = env
    tok, _ = _setup(c)
    w = next(x for x in _gate(c, tok)["warnings"] if x["reason_code"] == "EDIT_NOT_CONFIRMED")
    assert "If you accept it" not in w["why"] and "AI's summary" not in w["why"]


def test_second_check_pending_is_an_explicit_item_field(env):
    """The UI reads second_check_pending instead of guessing from judge/ladder fields: true exactly when the item is AI-made, live and its second check has no answer."""
    db, c = env
    tok = run_case(c)
    case = c.get(f"/api/cases/{tok}").json()
    every = case["entries"] + case.get("undated_entries", []) + case["amounts"] + case["flags"]
    assert every and all(isinstance(i["second_check_pending"], bool) for i in every)
    from app.backend import trace
    conn = DB.connect(db)
    unjudged = {u["item_id"] for u in trace.unjudged_items(conn, tok) if not trace.acknowledge_only(u["kind"], u["row"])}
    conn.close()
    assert {i["id"] for i in every if i["second_check_pending"]} == unjudged
    assert next(i for i in every if i["id"] == "e3")["second_check_pending"] is False
    r = _quote_pick(c, tok).json()
    assert r["item"]["second_check_pending"] is True                                     # the re-picked quote has no answer
    assert next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == "e3")["second_check_pending"] is True
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"summary": EDIT}})
    assert r.status_code == 200 and r.json()["item"]["second_check_pending"] is False    # her own wording needs no second check (D-045b)
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "reset"}).json()["item"]["second_check_pending"] is False
    assert c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "dismiss"}).json()["item"]["second_check_pending"] is False


def test_second_check_pending_clears_when_the_check_answers(env, monkeypatch):
    from app.backend import rejudge as RJ
    _, c = env
    tok = run_case(c)
    _quote_pick(c, tok)
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
    monkeypatch.setattr(RJ, "_safe_ask", lambda t, case_text, call: ("supported", "c_patched", "NONE"))
    assert c.post(f"/api/cases/{tok}/rejudge").status_code == 200
    e3 = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == "e3")
    assert e3["second_check_pending"] is False and c.get(f"/api/cases/{tok}/export").status_code == 200
