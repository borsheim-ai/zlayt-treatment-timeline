"""T-084 (D-042): guarded charge reclassification. Code wording check first, judge 2 second, 422 with a fixed reason otherwise; audited; survives a rerun."""
import pytest
from fastapi.testclient import TestClient
from app.backend import pipeline as PL, present, reclassify as RC, review as RV
from app.backend.api import create_app
from app.db import db as DB
from app.llm import audited as AU
from tests.unit._fakes import FakeCall, sample_script

TEXT = """=== Record 1 ===
Date: 2026-03-02
Source: Capital PT, visit 1
Excerpt: "Visit completed. Rate of $185 per visit."

=== Record 2 ===
Date: 2026-03-09
Source: Capital PT, visit 2
Excerpt: "Visit completed. Charge per visit $185."

=== Record 3 ===
Date: 2026-03-16
Source: Capital Imaging
Excerpt: "MRI performed. Charge: $310."

=== Record 4 ===
Date: 2026-03-23
Source: Capital PT, visit 4
Excerpt: "Visit completed. Not billed $90 per visit to this patient."

=== Record 5 ===
Date: 2026-03-30
Source: Capital PT, visit 5
Excerpt: "Visit completed. $185 was billed to the patient."

=== Record 6 ===
Date: 2026-04-06
Source: Capital PT, visit 6
Excerpt: "Visit completed. Billed $150 per visit."
"""
J2 = lambda v, code="NONE": {"j2": {"verdict": v, "reason_code": code}}     # noqa: E731


def seeded(tmp_path, judge="agree"):
    call = FakeCall(sample_script(extract=lambda u: dict(summary="Visit completed.", excerpt="Visit completed.")))
    conn = DB.connect(str(tmp_path / "rc.sqlite")); cid = DB.create_case(conn, TEXT, now=1.0)
    PL.run_pipeline(conn, cid, TEXT, call=call, now=lambda: 1.0)
    return conn, cid


def kinds(conn, cid):
    return {a["text"] + "@" + a["record_ids"][0]: a for a in DB.list_items(conn, cid, "amount")}


def aid(conn, cid, text, rec):
    return kinds(conn, cid)[f"{text}@{rec}"]["id"]


def events(conn, cid, item_id):
    return [e for e in DB.list_events(conn, cid, item_id) if (e.get("after") or {}).get("event") == "reclassify"]


def test_fixture_classes_are_what_the_tests_assume(tmp_path):
    conn, cid = seeded(tmp_path)
    k = kinds(conn, cid)
    assert (k["$185@r1"]["kind"], k["$185@r2"]["kind"], k["$310@r3"]["kind"], k["$90@r4"]["kind"]) == ("rate", "rate", "charge", "rate")
    assert (k["$185@r5"]["kind"], k["$150@r6"]["kind"]) == ("unclear", "rate")       # r5: charged wording, no rate cue; r2 and r6: wording AND a rate cue


# ---------------------------------------------------------------- charge -> not a charge
def test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    RV.apply_review(conn, cid, a, {"action": "accept"})
    r = RC.reclassify(conn, cid, a, {"to": "not_a_charge", "note": "This is a retainer, not a bill."}, call=None, now=5.0)
    assert r["amount"]["kind"] == "unclear" and r["item"]["review_status"] == "pending"          # her earlier accept was about the old meaning
    assert r["totals"]["accepted"]["cents"] == 0 and r["reclassified"] == {"from": "charge", "to": "unclear", "wording": None, "judge_verdict": None, "restored": False}
    [ev] = events(conn, cid, a)
    assert ev["before"]["kind"] == "charge" and ev["after"]["kind"] == "unclear" and ev["after"]["note"] == "This is a retainer, not a bill."
    row = DB.get_item(conn, a, cid)
    assert row["ladder"]["reclassification"]["by"] == "reviewer" and row["ladder"]["code_checks"]["classified_by"] == "reviewer:reclassified"
    assert any(e["action"] == "reset" for e in DB.list_events(conn, cid, a))                    # the reset is its own audited event


def test_same_direction_is_a_noop_without_an_event(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r1")
    r = RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    assert r["reclassified"] is None and not events(conn, cid, a)


def test_undoing_her_own_demotion_restores_the_code_class_without_a_judge(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    before = DB.get_item(conn, a, cid)["ladder"]["judge"]
    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)                                # no judge call available: still fine
    assert r["amount"]["kind"] == "charge" and r["reclassified"]["restored"] is True
    assert DB.get_item(conn, a, cid)["ladder"]["judge"] == before and len(events(conn, cid, a)) == 2


# ---------------------------------------------------------------- not a charge -> charge (guarded)
def test_rate_without_charge_wording_is_422_and_the_judge_is_never_asked(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r1")
    call = FakeCall(J2("agree"))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert (e.value.status, e.value.code, e.value.detail["reason"], e.value.detail["check"]) == (422, "reclassify_refused", "NO_CHARGE_WORDING", "code")
    assert call.log == [] and DB.get_item(conn, a, cid)["kind"] == "rate" and not events(conn, cid, a)


def test_negated_wording_does_not_count(tmp_path):
    conn, cid = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, aid(conn, cid, "$90", "r4"), {"to": "charge"}, call=FakeCall(J2("agree")))
    assert e.value.detail["reason"] == "NO_CHARGE_WORDING"


def test_figure_with_charge_wording_and_judge_agreement_becomes_a_pending_verified_charge(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r5")
    call = FakeCall(J2("agree"))
    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=call, now=7.0)
    assert call.steps() == ["j2"] and "CLASS: charge" in call.log[0]["user"]
    it = r["item"]
    assert r["amount"]["kind"] == "charge" and it["review_status"] == "pending" and it["state"] == "verified"
    assert r["totals"]["pending"]["cents"] == 31000 + 18500 and r["totals"]["accepted"]["cents"] == 0     # counted only after she accepts it
    row = DB.get_item(conn, a, cid)
    assert row["ladder"]["judge"]["verdict"] == "agree" and row["ladder"]["reclassification"]["wording"].lower() == "billed"
    [ev] = events(conn, cid, a)
    assert ev["after"]["judge_verdict"] == "agree" and ev["after"]["wording"].lower() == "billed" and ev["before"]["kind"] == "unclear"


@pytest.mark.parametrize("verdict,code,reason", [("disagree", "SHOULD_BE_RATE", "JUDGE_DISAGREES"), ("unsure", "TEXT_AMBIGUOUS", "JUDGE_UNSURE")])
def test_judge_objection_is_422_and_changes_nothing(tmp_path, verdict, code, reason):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r5")
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2(verdict, code)))
    assert (e.value.status, e.value.detail["reason"], e.value.detail["check"]) == (422, reason, "judge")
    assert e.value.detail["wording"].lower() == "billed" and DB.get_item(conn, a, cid)["kind"] == "unclear" and not events(conn, cid, a)


@pytest.mark.parametrize("call", [None, FakeCall(J2("agree", "BAD CODE")), lambda *a, **k: (_ for _ in ()).throw(AU.LLMFailed())])
def test_judge_that_cannot_answer_is_422_judge_unavailable(tmp_path, call):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r5")
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert e.value.detail["reason"] == "JUDGE_UNAVAILABLE" and DB.get_item(conn, a, cid)["kind"] == "unclear"


def test_unexpected_judge_bug_propagates(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r5")
    with pytest.raises(RuntimeError):
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=lambda *x, **k: (_ for _ in ()).throw(RuntimeError("bug")))
    assert DB.get_item(conn, a, cid)["kind"] == "unclear"


@pytest.mark.parametrize("rec,text", [("r2", "$185"), ("r6", "$150")])
def test_a_rate_sentence_that_also_says_charge_or_billed_is_refused_before_the_judge(tmp_path, rec, text):
    """Reviewer strings: "Charge per visit $185" and "Billed $150 per visit" state a rate; a rate cue is decisive."""
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, text, rec)
    call = FakeCall(J2("agree"))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert (e.value.status, e.value.detail["reason"], e.value.detail["check"]) == (422, "NO_CHARGE_WORDING", "code")
    assert call.log == [] and DB.get_item(conn, a, cid)["kind"] == "rate" and not events(conn, cid, a)
    assert DB.get_item(conn, a, cid)["state"] == "needs_review"


@pytest.mark.parametrize("sentence", [
    "Charge per visit $185.", "Billed $150 per visit.", "Billed $150 per session.", "Charged $40 per hour.", "Billed $40 per day.",
    "Charged $90 each.", "Each visit billed $90.", "Billed $90/visit.", "Billed $90 /session.", "Billed $90 x 3.", "Billed $90 \u00d7 4.",
    "Billed 3 x $90.", "Daily rate billed $400.", "Billed $185 a visit.", "Billed at a rate of $185.", "Billed $90 per-visit.", "Billed $90, per unit."])
def test_rate_cues_are_decisive(sentence):
    ex = "Visit done. " + sentence
    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;").split("/")[0]
    assert RC.charge_wording(ex, {"text": raw, "excerpt_start": None}) is None


UNIT_PRICE_SENTENCES = [        # T-084 r3 F2 (reviewer strings) + the brief's phrasings
    "Charged $150 an hour.", "Charged $75 a unit.", "Billed $120 an appointment.", "Billed $150 hourly.", "Charged $90 apiece.", "Billed $40 daily.",
    "Billed $200 a month.", "Billed unit price $90.", "Charged unit price of $90.", "Billed @ $90.", "Billed $90 @ each.", "Billed $90/visit.",
    "Billed at a rate of $90.", "Billed $90 weekly."]


@pytest.mark.parametrize("sentence", UNIT_PRICE_SENTENCES)
def test_every_unit_price_phrasing_is_refused_by_the_code_gate(sentence):
    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;").split("/")[0]
    assert RC.charge_wording("Visit done. " + sentence, {"text": raw, "excerpt_start": None}) is None


@pytest.mark.parametrize("sentence", UNIT_PRICE_SENTENCES + [
    "Charge per visit $185.", "Billed $150 per visit.", "Billed $150 for every visit.", "Billed $185 for the visit.", "Charged $310.", "Total billed $185.",
    "Billed $90 x 3.", "Amount due $90 on receipt.", "Charge: $310.", "Not billed $90 per visit to this patient."])
def test_classifier_rate_implies_the_wording_gate_refuses(sentence):
    """One rate test, two readers: whenever amounts.classify calls the figure a rate, charge_wording returns None."""
    from app.backend import amounts as AM
    ex = "Visit done. " + sentence
    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;").split("/")[0]
    a = next(x for x in AM.find_amounts(ex) if x["raw"].replace(" ", "") == raw)
    if AM.classify(ex, a) == "rate":
        assert RC.charge_wording(ex, {"text": a["raw"], "excerpt_start": None}) is None


@pytest.mark.parametrize("sentence", ["Charged $150 an hour.", "Charged $75 a unit.", "Billed $120 an appointment.", "Billed $150 hourly.", "Billed unit price $90."])
def test_unit_price_phrasings_are_refused_before_the_judge(tmp_path, sentence):
    conn, cid = seeded(tmp_path)
    text = TEXT.replace("Visit completed. $185 was billed to the patient.", "Visit completed. " + sentence)
    rerun(conn, cid, text)
    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;")
    a = aid(conn, cid, raw, "r5")
    call = FakeCall(J2("agree"))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert (e.value.status, e.value.detail["reason"], e.value.detail["check"]) == (422, "NO_CHARGE_WORDING", "code")
    assert call.log == [] and DB.get_item(conn, a, cid)["kind"] != "charge" and not events(conn, cid, a)


@pytest.mark.parametrize("sentence", ["Billed $185 for the visit.", "Total billed $185.", "Charged $310.", "Amount due $90 on receipt.", "The visit was billed at $185 in total."])
def test_plain_charge_statements_still_pass_the_wording_check(sentence):
    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;")
    assert RC.charge_wording("Visit done. " + sentence, {"text": raw, "excerpt_start": None}) is not None


RATE_R3 = TEXT.replace('Excerpt: "MRI performed. Charge: $310."', 'Excerpt: "MRI performed. Rate of $310 per visit."')


def rerun(conn, cid, text):
    call = FakeCall(sample_script(extract=lambda u: dict(summary="Visit completed.", excerpt="Visit completed.")))
    PL.run_pipeline(conn, cid, text, call=call, now=lambda: 3.0)


def test_restore_after_a_rerun_that_made_the_figure_a_rate_runs_both_checks_again(tmp_path):
    """Reviewer F1: demote $310, rerun with the code now calling it a rate, restore with no judge: 422, the figure stays out of the total."""
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    rerun(conn, cid, RATE_R3)
    row = DB.get_item(conn, a, cid)
    assert row["kind"] == "unclear" and row["ladder"]["reclassification"]["rerun"]["code_class"] == "rate"
    n = len(events(conn, cid, a))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)
    assert (e.value.status, e.value.detail["reason"]) == (422, "NO_CHARGE_WORDING")
    call = FakeCall(J2("agree"))
    with pytest.raises(RV.ReviewError):
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert call.log == []                                                                        # the code check stops it before the judge
    row = DB.get_item(conn, a, cid)
    assert row["kind"] == "unclear" and row["state"] == "needs_review" and len(events(conn, cid, a)) == n
    assert present.totals_view(conn, cid)["pending"]["cents"] == 0


def _class_only_flip(tmp_path, monkeypatch):
    """Demote $310, then rerun with the SAME text but the amount classifier now calling $310 a rate (a lexicon/classifier change). Excerpt unchanged."""
    from app.backend import amounts as AM
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    real = AM.classify
    monkeypatch.setattr(AM, "classify", lambda ex, am, *x, **k: "rate" if am.get("cents") == 31000 else real(ex, am, *x, **k))
    rerun(conn, cid, TEXT)
    monkeypatch.setattr(AM, "classify", real)
    row = DB.get_item(conn, a, cid)
    rr = row["ladder"]["reclassification"]["rerun"]
    assert rr["code_class"] == "rate" and rr["excerpt_sha"] == row["ladder"]["reclassification"]["excerpt_sha"]      # class changed, sentence did not
    return conn, cid, a


def test_restore_after_a_class_only_change_needs_the_judge_again(tmp_path, monkeypatch):
    """T84-3: restore must not skip the checks when only the rerun's code class changed (identical excerpt)."""
    conn, cid, a = _class_only_flip(tmp_path, monkeypatch)
    n = len(events(conn, cid, a))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)
    assert (e.value.status, e.value.detail["reason"]) == (422, "JUDGE_UNAVAILABLE")
    row = DB.get_item(conn, a, cid)
    assert row["kind"] == "unclear" and len(events(conn, cid, a)) == n and present.totals_view(conn, cid)["pending"]["cents"] == 0


def test_class_only_change_restore_with_a_judge_runs_the_judge_once_and_is_not_a_restore(tmp_path, monkeypatch):
    conn, cid, a = _class_only_flip(tmp_path, monkeypatch)
    call = FakeCall(J2("agree"))
    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert call.steps() == ["j2"] and r["reclassified"]["restored"] is False


def test_restore_after_a_rerun_that_changed_the_sentence_needs_the_judge_again(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    rerun(conn, cid, TEXT.replace("MRI performed. Charge: $310.", "MRI performed. Charge: $310 for the scan."))      # still a charge, different sentence
    assert DB.get_item(conn, a, cid)["ladder"]["reclassification"]["rerun"]["code_class"] == "charge"
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)
    assert e.value.detail["reason"] == "JUDGE_UNAVAILABLE" and DB.get_item(conn, a, cid)["kind"] == "unclear"
    call = FakeCall(J2("agree"))
    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert call.steps() == ["j2"] and r["reclassified"]["restored"] is False and r["amount"]["kind"] == "charge"


def test_restore_after_an_unchanged_rerun_still_needs_no_judge(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    rerun(conn, cid, TEXT)
    assert DB.get_item(conn, a, cid)["ladder"]["reclassification"]["rerun"]["code_class"] == "charge"
    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)
    assert r["reclassified"]["restored"] is True and r["amount"]["kind"] == "charge"


def test_a_promoted_charge_is_dropped_when_a_rerun_changes_its_sentence(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r5")
    RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2("agree")))
    rerun(conn, cid, TEXT)                                                                        # same sentence: her class is kept
    assert DB.get_item(conn, a, cid)["kind"] == "charge"
    rerun(conn, cid, TEXT.replace("$185 was billed to the patient.", "$185 was billed to the patient per visit."))
    assert DB.get_item(conn, a, cid)["kind"] != "charge"


# ---------------------------------------------------------------- structure
def test_bad_body_non_amount_and_rejected_item(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    for body in ({}, {"to": "rate"}, {"to": "charge", "note": 5}):
        with pytest.raises(RV.ReviewError) as e:
            RC.reclassify(conn, cid, a, body, call=None)
        assert e.value.status == 400
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, "e1", {"to": "charge"}, call=None)
    assert (e.value.status, e.value.code) == (422, "invalid_edit")
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, "a99", {"to": "charge"}, call=None)
    assert e.value.status == 404
    DB.update_item(conn, a, now=2.0, case=cid, state="rejected")
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    assert (e.value.status, e.value.code) == (409, "item_rejected")


def test_injection_tagged_record_and_missing_value_never_become_charges(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r2")
    DB.update_item(conn, a, now=2.0, case=cid, value_cents=None)
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2("agree")))
    assert e.value.detail["reason"] == "NO_VALUE"
    DB.update_item(conn, a, now=2.0, case=cid, value_cents=18500)
    conn.execute("UPDATE records SET injection_tag='ignore previous instructions' WHERE case_id=? AND id='r2'", (cid,))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2("agree")))
    assert e.value.detail["reason"] == "INJECTION_SUSPECTED"


def test_charge_wording_unit():
    ex = "Visit done. Billed $90 for the visit. Rate of $120 per visit. Not billed $50 per visit. Billed $70 per visit."
    row = lambda raw: {"text": raw, "excerpt_start": None}      # noqa: E731
    assert RC.charge_wording(ex, row("$90")).lower() == "billed"
    assert RC.charge_wording(ex, row("$70")) is None            # a rate cue beats the word "billed"
    assert RC.charge_wording(ex, row("$120")) is None
    assert RC.charge_wording(ex, row("$50")) is None
    assert RC.charge_wording("Amount due $40. Rate $40 per visit.", row("$40")) is None      # every occurrence of the figure needs its own wording


# ---------------------------------------------------------------- rerun and HTTP
def test_a_rerun_keeps_her_reclassification(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    call = FakeCall(sample_script(extract=lambda u: dict(summary="Visit completed.", excerpt="Visit completed.")))
    PL.run_pipeline(conn, cid, TEXT, call=call, now=lambda: 2.0)
    row = DB.get_item(conn, a, cid)
    assert row["kind"] == "unclear" and row["ladder"]["reclassification"]["by"] == "reviewer" and row["state"] == "needs_review"


def test_route(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    c = TestClient(create_app(str(tmp_path / "h.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/items/a1/reclassify", json={}).status_code == 400
    r = c.post(f"/api/cases/{tok}/items/a1/reclassify", json={"to": "not_a_charge"})
    assert r.status_code == 200 and r.json()["amount"]["kind"] == "unclear" and r.json()["reclassified"]["from"] == "charge"
    r = c.post(f"/api/cases/{tok}/items/a2/reclassify", json={"to": "charge"})              # "Charge per visit $185.": a rate, refused by the code check
    assert r.status_code == 422 and r.json()["error"]["code"] == "reclassify_refused" and r.json()["error"]["detail"]["reason"] == "NO_CHARGE_WORDING"
    assert c.post(f"/api/cases/{tok}/items/a99/reclassify", json={"to": "charge"}).status_code == 404
    ev = [e for e in c.get(f"/api/cases/{tok}/audit").json()["events"] if e["item_id"] == "a1"]
    assert [e["action"] for e in ev] == ["reclassify"]                # T-095: its own audit action (schema v4)


def test_judge_unavailable_refusal_names_the_error_class(tmp_path):
    conn, cid = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, aid(conn, cid, "$185", "r5"), {"to": "charge"}, call=lambda *a, **k: (_ for _ in ()).throw(AU.LLMFailed("down")))
    assert e.value.detail["reason"] == "JUDGE_UNAVAILABLE" and e.value.detail["error_class"] == "LLMFailed"
