"""D-050 (T-085 round 4): nothing made from a record routed Spanish or LANGUAGE_UNCERTAIN is ever `verified`. Every item (entry, amount, flag)
is needs_review with AI_TRANSLATION ("AI translation — check against the original"), whatever the Spanish code checks and the translation
judge said; only the paralegal's accept is the gate. The rule is enforced once, in confidence.compose_state (ctx `translated`), and each path
that rewrites a state has to pass it: pipeline, rerun, rejudge, edit, manual entry, date confirmation, reclassify, batch accept, export."""
import pytest

from app.backend import confidence, flags as FL, generator, language, rejudge, review, spanish
from tests.unit._fakes import FakeCall
from tests.unit.test_spanish_records import (ES_NOTE, ES_QUOTE, ES_SUMMARY, MIXED, _es_script, _record, _wait, api, packet)   # noqa: F401  (api is a fixture)

LABEL = "AI translation — check against the original"
UNCERTAIN_LINE = "Cervicalgia post-traumatica."      # the reviewer's Italian line that cannot be told from Spanish


# ---------------------------------------------------------------- the one place
def test_compose_state_never_verifies_a_translated_item_whatever_the_ladder_says():
    perfect = {"grounding_failures": [], "schema_valid": True, "code_reasons": [], "judge": "supported"}
    assert confidence.compose_state(perfect, {}) == ("verified", [])
    assert confidence.compose_state(perfect, {"translated": True}) == ("needs_review", ["AI_TRANSLATION"])
    assert confidence.compose_state({}, {"translated": True}) == ("needs_review", ["AI_TRANSLATION"])
    state, reasons = confidence.compose_state({**perfect, "judge": "partially"}, {"translated": True})
    assert state == "needs_review" and reasons == ["JUDGE_PARTIAL", "AI_TRANSLATION"]       # the judge's failure is still shown
    state, reasons = confidence.compose_state({**perfect, "grounding_failures": ["GROUNDING_EXCERPT_NOT_VERBATIM"]}, {"translated": True})
    assert state == "rejected" and reasons[0] == "GROUNDING_EXCERPT_NOT_VERBATIM"            # rejection is not softened
    assert confidence.compose_state(perfect, {"translated": False}) == ("verified", [])


def test_the_reason_has_the_label_text():
    from app.backend import why
    assert "AI translation — check against the original" in why.why("AI_TRANSLATION")
    assert spanish.translation_info("es")["review_label"] == LABEL
    assert spanish.translation_info("uncertain", True)["review_label"] == LABEL


# ---------------------------------------------------------------- generator path: Spanish and uncertain
@pytest.mark.parametrize("lang_line", [None, UNCERTAIN_LINE])
def test_extract_and_judge_never_verify_spanish_or_uncertain(lang_line):
    if lang_line is None:
        rec, text, summary, quote = _record(), MIXED, ES_SUMMARY, ES_QUOTE
        assert language.record_lang(rec) == "es"
    else:
        text = packet(("2026-03-03", "Clinic A", "Left shoulder pain 7/10."), ("2026-03-04", "Clinic B", lang_line))
        rec = _record(text, 2)
        summary, quote = "Post-traumatic neck pain.", lang_line
    assert language.is_translated(language.record_lang(rec))
    call = FakeCall(_es_script(summary=summary, excerpt=quote))
    e = generator.extract_one(rec, [2], call=call, case_text=text)
    assert e["state"] == "needs_review" and "AI_TRANSLATION" in e["reasons"]
    e = generator.judge_entries([e], {2: rec}, call=call, case_text=text)[0]
    assert e["ladder"]["judge"]["verdict"] == "supported"
    assert e["state"] == "needs_review" and "AI_TRANSLATION" in e["reasons"] and e["state"] != "verified"
    assert LABEL in e["why"]


def test_an_english_record_keeps_its_normal_ladder():
    text = packet(("2026-03-03", "Clinic A", "Left shoulder pain 7/10."), ("2026-03-04", "Clinic B", ES_NOTE))
    rec = _record(text, 1)
    call = FakeCall({"extract": lambda u: dict(summary="Left shoulder pain 7/10.", excerpt="Left shoulder pain 7/10."),
                     "j1": dict(verdict="supported", reason_code="NONE")})
    e = generator.extract_one(rec, [1], call=call, case_text=text)
    e = generator.judge_entries([e], {1: rec}, call=call, case_text=text)[0]
    assert e["state"] == "verified" and e["reasons"] == []


# ---------------------------------------------------------------- flags and amounts
def test_a_flag_from_a_spanish_record_is_never_verified():
    rec = _record()
    f = FL._flag(rec, "causation", "speculative_language", "Posible desgarro del manguito rotador.", "lexicon", None, False, "both")
    f["_stage"]["judge"] = "supported"
    FL._compose(f)
    assert f["state"] == "needs_review" and "AI_TRANSLATION" in f["reasons"]
    en = _record(MIXED, 1)
    g = FL._flag(en, "causation", "speculative_language", "Left shoulder pain 7/10.", "lexicon", None, False, "both")
    g["_stage"]["judge"] = "supported"
    FL._compose(g)
    assert g["state"] == "verified"


# ---------------------------------------------------------------- the whole case through the API: pipeline, rerun, rejudge, accept, batch, export
def _items_of_record(view, rid="r2"):
    out = []
    for key in ("entries", "undated_entries", "amounts", "flags"):
        out += [i for i in view.get(key) or [] if rid in (i.get("record_ids") or [])]
    return out


def test_api_every_item_of_a_spanish_record_is_needs_review_after_run_and_rerun(api):
    c, seen, _ = api
    tok = c.post("/api/cases", json={"text": MIXED}).json()["token"]
    for _ in range(2):                                           # the run, then a rerun
        assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
        assert _wait(c, tok)["status"] == "ready"
        view = c.get(f"/api/cases/{tok}").json()
        items = _items_of_record(view)
        assert any(i in view["entries"] for i in items) and any(i in view["amounts"] for i in items), view.keys()      # an entry and the $650.00 charge
        for i in items:
            assert i["state"] != "verified", i["id"]
            if i["state"] != "rejected":
                assert "AI_TRANSLATION" in (i.get("state_reasons") or i.get("reasons") or []), i
        en = next(e for e in view["entries"] if "r1" in e["record_ids"])
        assert en["state"] == "verified"                       # English is untouched
    es = next(e for e in view["entries"] if "r2" in e["record_ids"])
    assert es["translation"]["review_label"] == LABEL and es["translation"]["label"] == "AI translation"


def test_api_batch_accept_refuses_the_translated_item_and_single_accept_is_the_gate(api):
    c, _, _ = api
    tok = c.post("/api/cases", json={"text": MIXED}).json()["token"]
    c.post(f"/api/cases/{tok}/run", json={})
    _wait(c, tok)
    view = c.get(f"/api/cases/{tok}").json()
    es = next(e for e in view["entries"] if "r2" in e["record_ids"])
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": [es["id"]]})
    assert r.status_code in (400, 409, 422) and "not_verified" in r.text
    assert c.get(f"/api/cases/{tok}").json()["entries"] and next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == es["id"])["review_status"] == "pending"
    # the paralegal's own accept still works, and the export gate asks for nothing more than it
    assert c.post(f"/api/cases/{tok}/items/{es['id']}/review", json={"action": "accept"}).status_code == 200
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 200 and ES_SUMMARY in ex.json()["letter_text"] and "[AI translation of the Spanish original; check before sending]" in ex.json()["letter_text"]
    after = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == es["id"])
    assert after["review_status"] == "accepted" and after["state"] == "needs_review"        # accepting does not rewrite the machine state


def test_api_edit_and_rejudge_of_a_translated_entry_stay_needs_review(api):
    c, _, _ = api
    tok = c.post("/api/cases", json={"text": MIXED}).json()["token"]
    c.post(f"/api/cases/{tok}/run", json={})
    _wait(c, tok)
    es = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if "r2" in e["record_ids"])
    ok = c.post(f"/api/cases/{tok}/items/{es['id']}/review",
                json={"action": "edit", "edits": {"summary": "Patient reports pain 6/10; denies loss of consciousness."}})
    assert ok.status_code == 200, ok.text
    item = ok.json()["item"]
    assert item["state"] == "needs_review" and "AI_TRANSLATION" in (item.get("state_reasons") or item.get("reasons") or [])
    r = c.post(f"/api/cases/{tok}/rejudge")                     # nothing unjudged: a no-op, and still nothing becomes verified
    assert r.status_code == 200
    again = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == es["id"])
    assert again["state"] == "needs_review"


# ---------------------------------------------------------------- rejudge and date confirmation recompute from the row
@pytest.mark.parametrize("row", [
    {"state_reasons": ["JUDGE_UNAVAILABLE", "AI_TRANSLATION"], "ladder": {"translation": {}}},
    {"state_reasons": ["JUDGE_UNAVAILABLE", "LANGUAGE_UNCERTAIN"], "ladder": {}},
    {"state_reasons": ["JUDGE_UNAVAILABLE"], "ladder": {"translation": {"source_language": "es"}}},          # a row that lost its reason code
    {"state_reasons": ["AI_TRANSLATION"], "ladder": None},                                                   # an amount or flag: no translation block
])
def test_rejudge_recompose_never_verifies_a_translation(row):
    state, reasons = rejudge.recompose(row, "supported")
    assert state == "needs_review" and "AI_TRANSLATION" in reasons and "JUDGE_UNAVAILABLE" not in reasons


def test_rejudge_recompose_still_verifies_an_english_item():
    assert rejudge.recompose({"state_reasons": ["JUDGE_UNAVAILABLE"], "ladder": {}}, "supported") == ("verified", [])


@pytest.mark.parametrize("item", [
    {"state": "needs_review", "state_reasons": ["DATE_AMBIGUOUS", "AI_TRANSLATION"], "ladder": {"translation": {}}},
    {"state": "needs_review", "state_reasons": ["DATE_AMBIGUOUS"], "ladder": {"translation": {}}},
])
def test_confirming_a_date_never_verifies_a_translated_entry(item):
    out = review._without_date_doubt(item)
    assert out["state"] == "needs_review" and "AI_TRANSLATION" in out["state_reasons_json"] and "DATE_AMBIGUOUS" not in out["state_reasons_json"]


def test_confirming_a_date_still_verifies_an_english_entry_whose_only_doubt_was_the_date():
    out = review._without_date_doubt({"state": "needs_review", "state_reasons": ["DATE_AMBIGUOUS"], "ladder": {}})
    assert out["state"] == "verified" and out["state_reasons_json"] == []


def test_api_reclassifying_a_charge_from_a_spanish_record_never_verifies_it(api):
    c, _, _ = api
    tok = c.post("/api/cases", json={"text": MIXED}).json()["token"]
    c.post(f"/api/cases/{tok}/run", json={})
    _wait(c, tok)
    amt = next(a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if "r2" in a["record_ids"])
    assert amt["state"] == "needs_review"
    r = c.post(f"/api/cases/{tok}/items/{amt['id']}/reclassify", json={"to": "not_a_charge"})      # (back to charge needs charge wording, which "Consulta:" lacks)
    assert r.status_code == 200, r.text
    now = next(a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["id"] == amt["id"])
    assert now["state"] == "needs_review" and "AI_TRANSLATION" in (now.get("state_reasons") or now.get("reasons") or []), now


def test_a_manual_entry_over_a_spanish_quote_is_never_verified(tmp_path):
    from app.backend import ingest, pipeline as PL, review
    from app.db import db as DB
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    cid = DB.create_case(conn, ingest.normalize_text(MIXED), now=1.0)
    script = {**_es_script(), "extract": lambda u: dict(summary="Left shoulder pain 7/10.", excerpt="Left shoulder pain 7/10."),
              "j1": dict(verdict="supported", reason_code="NONE"), "j2": dict(verdict="agree", reason_code="NONE"),
              "j3": dict(verdict="benign", reason_code="NONE"), "j4": dict(verdict="agree", reason_code="NONE"),
              "conflicts": {"flags": []}, "flags": {"flags": []}}
    script["extract_es"] = lambda u: dict(summary=ES_SUMMARY, excerpt="Refiere dolor 6/10 que no esta en el texto.")      # not verbatim: rejected, so no live entry
    PL.run_pipeline(conn, cid, MIXED, call=FakeCall(script), now=lambda: 1.0)
    out = review.manual_entry(conn, cid, "r2", {"summary": ES_SUMMARY, "excerpt": ES_QUOTE}, call=FakeCall(script), now=2.0)
    item = out["item"]
    assert item["translation"]["label"] == "Translation (edited by reviewer)"
    assert item["state"] == "needs_review" and "AI_TRANSLATION" in (item.get("state_reasons") or item.get("reasons") or [])
