"""T-139 (GATE-M2 claims-adjuster blocker; D-019, R-CH-7, R-EX-8, D-051, D-054): no dollar amount reaches the carrier letter except in the BILLED CHARGES
section (accepted charges and the R-EX-8 total line). An entry whose summary or quote states an amount fails the code check CHARGE_TEXT_IN_ENTRY: it is
needs_review with a plain reason, cannot be accepted, and is held out of the letter until she picks a quote without the amount or edits the summary.
A dismissed charge is never listed under 'Bills to request'. Deterministic code only."""
import re

import pytest
from fastapi.testclient import TestClient

from app.backend import charge_text as CT
from app.backend import confidence, why
from app.backend import export as X
from app.backend.api import create_app
from tests.unit._hand_entry import enter_failed_records_by_hand
from tests.unit.test_api_routes import wait_ready as _wait_ready


def wait_ready(c, tok):
    """Wait for the run; lib01's record 3 has no recorded extract answer (T-165: failed / run_partial), so the record is entered by hand."""
    _wait_ready(c, tok, allow_failed=True)
    enter_failed_records_by_hand(c, tok)
    return _wait_ready(c, tok)


LIB01 = "case_lib01_er_only_then_gap"


# ---------------------------------------------------------------- the pure functions
@pytest.mark.parametrize("text,found", [
    ("ED charge: $3,915.", ["$3,915"]),
    ("Charge per visit $140.", ["$140"]),
    ("Statement: $1,2OO and $95.00", ["$1,2OO", "$95.00"]),
    ("Fee $ 95 per adjustment", ["$ 95"]),
    ("billed 140 dollars for the visit", ["140 dollars"]),
    ("Insurance adjustment: -$1,250.", ["$1,250"]),
])
def test_currency_strings_found(text, found):
    assert CT.currency_strings(text) == found


@pytest.mark.parametrize("text", ["Pain 7/10, ROM reduced approx. 30%.", "Plan of care: 8 visits, 2x/week for 6 weeks.", "Rx ibuprofen 600 mg. CT head negative.", "", None])
def test_no_currency_in_clinical_text(text):
    assert CT.currency_strings(text) == [] and not CT.has_currency(text)


def test_check_says_where():
    assert CT.check("Pain 3/10.", "Pain 3/10.") == {}
    assert CT.check("Pain 3/10; charge $140.", "Pain 3/10. Charge: $140.") == {"summary": ["$140"], "excerpt": ["$140"]}
    assert CT.check("Pain 3/10.", "Pain 3/10. Charge: $140.") == {"excerpt": ["$140"]}


def test_trim_removes_a_trailing_currency_clause_only():
    t = CT.trim_summary("Diagnosis of cervical strain; X-ray negative for fracture; follow up with primary care in 1 week; ED charge $3,915.")
    assert t["changed"] and t["text"] == "Diagnosis of cervical strain; X-ray negative for fracture; follow up with primary care in 1 week."
    assert t["removed"] == ["ED charge $3,915"]
    t = CT.trim_summary("Cervical range of motion reduced approx. 30%. Plan of care: 8 visits. Charge per visit $140.")
    assert t["text"] == "Cervical range of motion reduced approx. 30%. Plan of care: 8 visits."
    t = CT.trim_summary("Partial-thickness supraspinatus tear. MRI charge: $2,150.")
    assert t["text"] == "Partial-thickness supraspinatus tear."


def test_trim_never_edits_a_kept_clause_and_refuses_unsafe_cuts():
    for s in ("Pain 3/10, improving; home exercise program reviewed.",                  # nothing to trim
              "Charge $140; pain 3/10 with cervical spasm.",                            # the first clause is never removed
              "Cervical spasm; charge $140; plan 12 visits.",                           # a clause after the cut would depend on it (suffix rule)
              "Pain. Charge $140.",                                                     # the kept prefix needs 2 content words
              "Statement of charges: office visits $1,100; MRI referral fee $450. Balance: $1,550."):   # nothing safe is left
        t = CT.trim_summary(s)
        assert t["changed"] is False and t["text"] == s and t["removed"] == []


def test_codes_are_registered_and_have_a_plain_sentence():
    assert "CHARGE_TEXT_IN_ENTRY" in confidence.REASON_CODES
    assert "dollar" in why.why("CHARGE_TEXT_IN_ENTRY").lower() and "internal notes" in why.why("CHARGE_TEXT_IN_ENTRY").lower()
    state, reasons = confidence.compose_state({"code_reasons": ["CHARGE_TEXT_IN_ENTRY"], "judge": "supported"}, {})
    assert state == "needs_review" and reasons == ["CHARGE_TEXT_IN_ENTRY"]


# ---------------------------------------------------------------- export: held out, never printed
def _case(entries, amounts=(), records=None):
    records = records or [dict(n=1, source="Marrowgate General ED", date_iso="2026-02-14",
                               excerpt="Dx: cervical strain. Follow up in 1 week. ED charge: $3,915.")]
    return dict(records=records, entries=entries, amounts=list(amounts), flags=[], pending_count=0, events=[])


def _entry(summary, excerpt, status="accepted", n=1, i="e1"):
    return dict(id=i, record_no=n, summary=summary, excerpt=excerpt, review_status=status)


def _letter_money(letter):
    """Every currency string in the letter, outside the BILLED CHARGES section (the section lists accepted charges and the R-EX-8 total line)."""
    return CT.currency_strings(letter.split(X.CHARGES_TITLE)[0])


def test_accepted_entry_whose_quote_states_an_amount_blocks_the_export_and_names_the_line():
    """T-139 r4: an accepted entry with money is no longer dropped silently; the gate scans the final letter text and blocks, naming the line."""
    with pytest.raises(X.ExportBlocked) as ei:
        X.build_export(_case([_entry("Diagnosis of cervical strain; ED charge $3,915.", "Dx: cervical strain. Follow up in 1 week. ED charge: $3,915.")]))
    b = ei.value.items
    assert b and all(i["reason_code"] == "MONEY_IN_LETTER" for i in b) and ei.value.code == "export_blocked"
    assert any("$3,915" in e for i in b for e in i["expressions"]) and all(f"Line {i['line']} " in i["why"] for i in b)


def test_accepted_entry_whose_summary_states_an_amount_blocks_even_when_the_quote_is_clean():
    with pytest.raises(X.ExportBlocked) as ei:
        X.build_export(_case([_entry("Diagnosis of cervical strain; ED charge $3,915.", "Dx: cervical strain. Follow up in 1 week.")]))
    b = ei.value.items
    assert len(b) == 1 and b[0]["item_id"] == "e1" and b[0]["next_action"]["code"] == "EDIT_SUMMARY" and "3,915" in b[0]["why"]


def test_a_clean_entry_is_exported_unchanged():
    out = X.build_export(_case([_entry("Diagnosis of cervical strain.", "Dx: cervical strain.")]))
    assert "Diagnosis of cervical strain." in out["letter_text"] and out["counts"]["entries"] == 1


def test_oneline_style_is_gated_too():
    with pytest.raises(X.ExportBlocked):
        X.build_export(_case([_entry("Diagnosis of cervical strain.", "Follow up in 1 week. ED charge: $3,915.")]), style="oneline")


def test_a_pending_amount_entry_is_listed_with_its_reason():
    out = X.build_export(_case([_entry("Diagnosis of cervical strain; ED charge $3,915.", "Dx: cervical strain. Follow up in 1 week. ED charge: $3,915.", status="pending")]))
    assert "$" not in out["letter_text"]
    assert "states a dollar amount" in out["internal_notes_text"].split("RECORDS NOT IN THE TREATMENT SECTION")[1].split("EDITED ITEMS")[0]


def test_narrative_sentence_with_an_amount_never_reaches_the_letter():
    case = _case([_entry("Diagnosis of cervical strain.", "Dx: cervical strain.")])
    case["narrative"] = {"status": "accepted", "basis": {"e1": X.basis_hash(case["entries"][0])}, "removed": [],
                         "sentences": [{"text": "She was diagnosed with cervical strain and billed $3,915.", "entry_id": "e1", "cite": None}]}
    out = X.build_export(case)
    assert "$" not in out["letter_text"]


def _charge(i, cents, raw, excerpt, status="accepted", n=1):
    return dict(id=i, record_no=n, cents=cents, cls="charge", raw=raw, excerpt=excerpt, review_status=status)


def test_dismissed_charge_is_not_under_bills_to_request_and_not_quoted():
    entry = _entry("Diagnosis of cervical strain.", "Dx: cervical strain.")
    amt = _charge("a1", 391500, "$3,915", "ED charge: $3,915.", status="dismissed")
    out = X.build_export(_case([entry], [amt]))
    bills = out["internal_notes_text"].split("BILLS TO REQUEST")[1].split("RECORDS NOT IN THE TREATMENT SECTION")[0]
    assert "Marrowgate" not in bills
    assert "3,915" not in out["letter_text"] and X.CHARGES_TITLE not in out["letter_text"]


def test_a_provider_with_an_accepted_charge_and_nothing_dismissed_is_unchanged():
    entry = _entry("Diagnosis of cervical strain.", "Dx: cervical strain.")
    amt = _charge("a1", 391500, "$3,915", "ED charge: $3,915.")
    out = X.build_export(_case([entry], [amt]))
    assert "Billed charges accepted from these records: $3,915.00" in out["letter_text"]
    assert "Marrowgate" not in out["internal_notes_text"].split("BILLS TO REQUEST")[1].split("RECORDS NOT IN THE TREATMENT SECTION")[0]


def test_provider_still_listed_when_no_charge_was_stated_at_all():
    out = X.build_export(_case([_entry("Diagnosis of cervical strain.", "Dx: cervical strain.")]))
    assert "Marrowgate General ED" in out["internal_notes_text"].split("BILLS TO REQUEST")[1]


# ---------------------------------------------------------------- the review flow (lib01, recorded fixtures)
@pytest.fixture
def env(tmp_path, monkeypatch):
    # The held-out path on lib01's recorded e2/e4: narrowing (test_t139_narrow.py) would drop their trailing charge sentence, so it is switched off here to exercise
    # the hold-out, the 422 and the quote picker on entries narrowing cannot help (the same recorded model answers; their J1 answers are recorded too).
    monkeypatch.setattr(CT, "narrow_excerpt", lambda excerpt: None)
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("FIXTURE_SET", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    c = TestClient(create_app(str(tmp_path / "t139.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    tok = c.post("/api/cases", json={"library": LIB01}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    wait_ready(c, tok)
    return c, tok


def _post(c, tok, item, body):
    return c.post(f"/api/cases/{tok}/items/{item}/review", json=body)


def _accept_all(c, tok, skip=()):
    v = c.get(f"/api/cases/{tok}").json()
    refused = {}
    for kind in ("entries", "amounts", "flags"):
        for it in v[kind]:
            if it["id"] in skip:
                continue
            r = _post(c, tok, it["id"], {"action": "accept", "compared": True})      # D-066: she compared the disputed ones
            if r.status_code != 200:
                refused[it["id"]] = r
    return refused


def test_pipeline_marks_amount_entries_needs_review_with_a_plain_reason(env):
    c, tok = env
    ent = {e["id"]: e for e in c.get(f"/api/cases/{tok}").json()["entries"]}
    for i in ("e2", "e4"):
        assert ent[i]["state"] == "needs_review" and "CHARGE_TEXT_IN_ENTRY" in ent[i]["reasons"], ent[i]
        assert "internal notes" in ent[i]["why"].lower()
    assert ent["e1"]["state"] == "verified" and "CHARGE_TEXT_IN_ENTRY" not in ent["e1"]["reasons"]


def test_accept_is_refused_with_a_plain_message_naming_the_amount(env):
    c, tok = env
    r = _post(c, tok, "e2", {"action": "accept"})
    assert r.status_code == 422
    err = r.json()["error"]
    assert err["code"] == "CODE_CHECK_FAILED" and err["detail"]["reason_code"] == "CHARGE_TEXT_IN_ENTRY" and err["detail"]["item_id"] == "e2"
    assert "$3,915" in err["message"] and "letter" in err["message"].lower()
    refused = _accept_all(c, tok)
    assert set(refused) == {"e2", "e4"}


def test_lib01_letter_has_no_amount_outside_the_charges_section_and_no_per_visit_rate(env):
    c, tok = env
    _accept_all(c, tok)
    j = c.get(f"/api/cases/{tok}/export").json()
    for style in ("standard", "oneline"):
        letter = c.get(f"/api/cases/{tok}/export?style={style}").json()["letter_text"]
        assert _letter_money(letter) == [], letter
        assert "per visit" not in letter.lower() and "$140" not in letter
    assert j["counts"]["entries"] == 4                      # e1, e5, e6 and the hand-entered record 3 (wait_ready); e2 and e4 are held out
    notes = j["internal_notes_text"]
    assert "states a dollar amount, not exported" in notes


def test_dismissed_charge_lib01_end_to_end(env):
    c, tok = env
    _accept_all(c, tok)
    assert _post(c, tok, "a1", {"action": "dismiss"}).status_code == 200
    j = c.get(f"/api/cases/{tok}/export").json()
    assert "3,915" not in j["letter_text"] and X.CHARGES_TITLE not in j["letter_text"]
    bills = j["internal_notes_text"].split("BILLS TO REQUEST")[1].split("RECORDS NOT IN THE TREATMENT SECTION")[0]
    assert "Marrowgate" not in bills


def _sentences(c, tok, rec_id):
    rec = next(r for r in c.get(f"/api/cases/{tok}").json()["records"] if r["id"] == rec_id)
    return rec


def test_quote_picker_without_the_amount_clears_it_and_code_trims_the_summary_clause(env):
    c, tok = env
    v = c.get(f"/api/cases/{tok}").json()
    e2 = next(e for e in v["entries"] if e["id"] == "e2")
    new_quote = "Dx: cervical strain. X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Follow up with primary care in 1 week."
    r = _post(c, tok, "e2", {"action": "edit", "edits": {"excerpt": new_quote}})
    assert r.status_code == 200, r.json()
    item = r.json()["item"]
    assert "$" not in item["summary"] and item["summary"].endswith("1 week.")
    assert "CHARGE_TEXT_IN_ENTRY" not in item["reasons"]
    assert any(w["code"] == "CHARGE_CLAUSE_REMOVED" for w in r.json()["warnings"])
    # a human accept after comparing puts it in the letter, without the amount
    if item["state"] == "needs_review":
        assert _post(c, tok, "e2", {"action": "accept"}).status_code == 200
    _accept_all(c, tok)
    letter = c.get(f"/api/cases/{tok}/export").json()
    assert "Marrowgate General ED" in letter["letter_text"] and "ED charge" not in letter["letter_text"].split(X.CHARGES_TITLE)[0]
    assert "original" not in letter["letter_text"].lower()                # D-010: no edit marker in the letter
    assert "ED charge $3,915" in letter["internal_notes_text"]                # the notes keep the original wording
    assert e2["summary"].endswith("$3,915.")


def test_quote_picker_that_still_has_the_amount_is_refused(env):
    c, tok = env
    r = _post(c, tok, "e2", {"action": "edit", "edits": {"excerpt": "X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Follow up with primary care in 1 week. ED charge: $3,915."}})
    assert r.status_code == 422
    e = r.json()["error"]
    assert e["detail"].get("reason") == "CHARGE_TEXT_IN_ENTRY" or e["detail"].get("reason_code") == "CHARGE_TEXT_IN_ENTRY"
    assert "$3,915" in e["message"]


def test_summary_edit_that_keeps_the_amount_is_refused_and_one_without_it_is_not(env):
    c, tok = env
    bad = _post(c, tok, "e2", {"action": "edit", "edits": {"summary": "Diagnosis of cervical strain; cervical spine X-ray negative for fracture; ibuprofen 600 mg prescribed; follow up with primary care in 1 week; ED charge $3,915."}})
    assert bad.status_code == 422 and "$3,915" in bad.json()["error"]["message"]
    # the quote still states the amount, so a clean summary alone does not release the entry
    still = _post(c, tok, "e2", {"action": "edit", "edits": {"summary": "Diagnosis of cervical strain; cervical spine X-ray negative for fracture; ibuprofen 600 mg prescribed; follow up with primary care in 1 week."}})
    assert still.status_code == 422
    assert "quote" in still.json()["error"]["message"].lower()


def test_untrimmable_summary_with_a_clean_quote_asks_for_a_summary_edit(env):
    c, tok = env
    # e4's first clause carries the rate, so code cannot trim it (suffix rule); the paralegal must edit the summary
    quote = "Cervical range of motion reduced approx. 30%. Plan of care: 8 visits."
    r = _post(c, tok, "e4", {"action": "edit", "edits": {"excerpt": quote}})
    assert r.status_code == 200, r.json()           # trailing clause: code trims it
    r2 = _post(c, tok, "e4", {"action": "edit", "edits": {"summary": "Cervical range of motion reduced approx. 30%; charge per visit $140."}})
    assert r2.status_code == 422 and "summary" in r2.json()["error"]["message"].lower()


def test_trace_and_gate_still_work_with_the_new_reason(env):
    c, tok = env
    assert c.get(f"/api/cases/{tok}/trace").status_code == 200
    assert c.get(f"/api/cases/{tok}/items/e2/trace").status_code == 200
    assert re.search(r"dollar", c.get(f"/api/cases/{tok}").json()["entries"][1]["why"], re.I)


def _lib_client(tmp_path, monkeypatch, lib):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("FIXTURE_SET", raising=False)
    c = TestClient(create_app(str(tmp_path / "lib.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    tok = c.post("/api/cases", json={"library": lib}).json()["token"] if lib else c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    wait_ready(c, tok)
    return c, tok


@pytest.mark.parametrize("narrow", [False, True])
@pytest.mark.parametrize("lib,rates", [("case_lib01_er_only_then_gap", ["$140"]), ("case_lib03_truck_rear_end_chiro", ["$120"])])
def test_library_letters_carry_no_per_visit_rate_after_accepting_everything(tmp_path, monkeypatch, lib, rates, narrow):
    """The GATE-M2 blocker as reported: lib01 'Charge per visit $140' and lib03 '$120' reached the letter. Accept everything code allows, export both styles.
    narrow=False: narrowing off, the entries are held out. narrow=True (shipped): code drops the charge sentence and the entry stays in the letter without it."""
    if not narrow:
        monkeypatch.setattr(CT, "narrow_excerpt", lambda excerpt: None)
    c, tok = _lib_client(tmp_path, monkeypatch, lib)
    refused = _accept_all(c, tok)
    assert all(r.json()["error"]["code"] in ("CODE_CHECK_FAILED", "DATE_UNCONFIRMED") for r in refused.values())
    held = [r for r in refused.values() if r.json()["error"]["code"] == "CODE_CHECK_FAILED" and r.json()["error"]["detail"]["reason_code"] == "CHARGE_TEXT_IN_ENTRY"]
    assert bool(held) is (not narrow)
    for style in ("standard", "oneline"):
        j = c.get(f"/api/cases/{tok}/export?style={style}").json()
        letter = j["letter_text"]
        assert _letter_money(letter) == [], letter
        assert "per visit" not in letter.lower() and not any(r in letter for r in rates)
        assert "Request itemized" in j["internal_notes_text"] or "BILLS TO REQUEST" in j["internal_notes_text"]       # the rate itself stays available to the firm
    if narrow:
        ents = c.get(f"/api/cases/{tok}").json()["entries"]
        assert not [e for e in ents if CT.has_currency(e["summary"]) or CT.has_currency(e["excerpt"])]
        assert c.get(f"/api/cases/{tok}/export").json()["counts"]["entries"] >= len([e for e in ents if e["state"] != "rejected"]) - len(refused)


def test_narrowed_entries_keep_their_place_in_the_letter_without_the_charge_sentence(tmp_path, monkeypatch):
    """lib01 e2 (ED visit) and e4 (PT evaluation): the charge sentence is dropped by code, the rest of the quote is verbatim, judge 1 ran on the narrowed pair."""
    c, tok = _lib_client(tmp_path, monkeypatch, LIB01)
    ents = {e["id"]: e for e in c.get(f"/api/cases/{tok}").json()["entries"]}
    for i, kept_end in (("e2", "in 1 week."), ("e4", "Plan of care: 8 visits.")):
        e = ents[i]
        assert e["state"] == "verified" and "CHARGE_TEXT_IN_ENTRY" not in e["reasons"], e
        assert not CT.has_currency(e["excerpt"]) and not CT.has_currency(e["summary"]) and e["excerpt"].endswith(kept_end)
        lad = c.get(f"/api/cases/{tok}/items/{i}/trace").status_code
        assert lad == 200
    assert _accept_all(c, tok) == {}
    letter = c.get(f"/api/cases/{tok}/export").json()["letter_text"]
    assert "Plan of care: 8 visits." in letter and "Marrowgate General ED" in letter and _letter_money(letter) == []


def test_the_sample_keeps_all_nine_entries_in_the_letter_and_only_the_total_line_states_money(tmp_path, monkeypatch):
    c, tok = _lib_client(tmp_path, monkeypatch, None)
    assert _accept_all(c, tok) == {}
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    assert len([e for e in ents if e["state"] != "rejected"]) == 9
    j = c.get(f"/api/cases/{tok}/export").json()
    assert j["counts"]["entries"] == 9 and _letter_money(j["letter_text"]) == []
    for i in ("e2", "e4"):
        assert not CT.has_currency(next(e for e in ents if e["id"] == i)["excerpt"])
    assert "Billed charges accepted from these records: $8,390.00" in j["letter_text"]


def test_a_billing_statement_that_cannot_be_narrowed_is_still_held_out(tmp_path, monkeypatch):
    """lib06 e4: every sentence of the statement states an amount (and the summary needs it), so code cannot narrow it: held out as before."""
    c, tok = _lib_client(tmp_path, monkeypatch, "case_lib06_lop_billed_vs_adjusted")
    e4 = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == "e4")
    assert e4["state"] == "needs_review" and "CHARGE_TEXT_IN_ENTRY" in e4["reasons"] and "excerpt_narrowed" not in str(e4.get("ladder", ""))
    r = _post(c, tok, "e4", {"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["detail"]["reason_code"] == "CHARGE_TEXT_IN_ENTRY"
