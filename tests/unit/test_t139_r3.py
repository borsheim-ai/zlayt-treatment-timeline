"""T-139 round 3 (claims-adjuster r2): (1) amounts written in words, with other currency signs or ISO codes, or inside a patient's statement are caught by the charge-text
hold AND by the independent letter eval; plain clinical number words are not; (2) the held-out hint says the true reason for each held entry: a record with a charge
amount says its charges are under Billed charges, a record with none says its figures are not counted."""
import contextlib
import pathlib
import tempfile

import pytest

from app.backend import charge_text as CT
from app.backend import pipeline as PL
from app.backend import present
from evals import letter_check as LC
from tests.unit.test_t139_charge_text import _lib_client, _post

ROOT = pathlib.Path(__file__).resolve().parents[2]

MONEY = [
    "Charge per visit: one hundred eighty-five dollars.", "Estimated cost of revision: six thousand five hundred dollars.", "Patient owes two thousand dollars.",
    "Surgeon quoted 6,500 bucks for revision.", "a thousand bucks", "Charge per visit €185.", "Visit rate 185 €.", "Visit rate EUR 185.", "Visit rate 185.00 EUR.",
    "Visit rate £1,200.", "Visit rate ＄185.", "Visit rate MXN 1,300.", "Visit rate CAD 1,200.", "Visit rate 1.200,00 €.", "Visit rate USD 1,200.", "Consulta 400 pesos.",
    "Cuatrocientos dólares por sesión.",
    'Patient states "the ER bill was 3,915 and I cannot pay it."', "Patient reports she owes the chiropractor about 2,400.", 'Patient states "they charged me fifteen hundred for the MRI."',
    "Pt states the ambulance cost him 1,380.", 'Patient states: "I paid a 40 copay each visit."', "Patient states the ER billed her 6240.",
    "Patient states the injection will run about 1800 out of pocket.", "Patient states the MRI was 2,150.", "Patient states she spent 900 on prescriptions.",
    "Self-pay rate 185.", "Out-of-pocket 1,200.00.", "Lien amount 4,000.", "Total: 1,200.00.", "Amount: 1,200.00.", "Adjustment -1,250.00.", "Network discount 3,610.00.",
    "185 per visit.", "Medical specials total 8,390.", "Bill 3,915.", "Invoice total 1,567.05.", "Saldo: 2,900.00.", "Costo: 1,300.", "Fee 95.",
]
CLINICAL = [
    "Plan of care: twelve visits over two weeks.", "Pain 7/10; ibuprofen 600 mg; 35 mph; approx. 40%; 3 days of work.", "Patient states she took 1,000 mg of acetaminophen.",
    "Patient reports pain for 3 weeks; walked 1,500 steps.", "Patient states symptoms began 2019.", "BP 120/80, heart rate 120 bpm, respiratory rate 20.",
    "Total knee replacement in 2019.", "Total of 12 visits.", "Total body weight 180 lbs.", "Total ROM 150 degrees.", "Patient said she waited 45 minutes.",
    "Range of motion reduced by one hundred twenty degrees; twenty minutes of ultrasound; five minutes of heat; two sessions per week.",
    "Hundred percent compliant with home exercise; two hundred steps daily.", "Return in two weeks; twelve visits ordered; three days off work.",
    "UB-04 type of bill 0111, for statement period 06/09/2026 to 06/12/2026.", "Ambulance invoice, November 12, 2026.",
]


@pytest.mark.parametrize("text", MONEY)
def test_the_charge_text_hold_catches_it(text):
    assert CT.check("", text).get("excerpt"), text
    assert CT.check(text, "").get("summary"), text


@pytest.mark.parametrize("text", MONEY)
def test_the_letter_eval_catches_it_with_its_own_detector(text):
    assert LC.dollar_figures(text) or LC.other_currency(text) or LC.unmarked_money(text), text
    assert LC.violations("Plan of care.\nSource: \"" + text + "\"\n\nBILLED CHARGES\nBilled charges accepted from these records: $0.00"), text


@pytest.mark.parametrize("text", CLINICAL)
def test_plain_clinical_number_words_and_figures_are_not_money(text):
    assert CT.check(text, text) == {}, CT.currency_strings(text)
    assert not (LC.dollar_figures(text) or LC.other_currency(text) or LC.unmarked_money(text)), text


def test_the_letter_the_adjuster_found_is_flagged():
    letter = ("Plan of care: 12 visits at one hundred eighty-five dollars per visit.\nPT €4 per visit.\n\nBILLED CHARGES\nBilled charges accepted from these records: $0.00")
    out = LC.violations(letter)
    assert len(out) >= 2 and any("one hundred eighty-five dollars" in x for x in out) and any("€4" in x for x in out)


def test_the_eval_detector_is_the_shared_one(monkeypatch):
    """T-139 r4 replaced the round-3 design (a second detector in the eval) with ONE module; see test_t139_r4.py::test_the_three_callers_use_the_one_detector."""
    from app.backend import money
    assert LC.violations("Rate: one hundred eighty-five dollars per visit.")
    monkeypatch.setattr(money, "hits", lambda t: [])
    assert not LC.violations("Rate: one hundred eighty-five dollars per visit.")


def test_a_summary_edit_in_words_is_refused_with_the_charge_text_code_and_stores_nothing(tmp_path, monkeypatch):
    c, tok = _lib_client(tmp_path, monkeypatch, None)
    before = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == "e4")
    r = _post(c, tok, "e4", {"action": "edit", "edits": {"summary": "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits at one hundred eighty-five dollars per visit."}})
    body = r.json()
    assert r.status_code == 422 and "dollar amount" in str(body), body
    after = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == "e4")
    assert after["summary"] == before["summary"] and after["review_status"] == before["review_status"]


def test_a_summary_edit_whose_only_problem_is_the_amount_in_words_gets_the_charge_text_code(tmp_path, monkeypatch):
    """The quote already carries the words (so no D-034 token check fires first), and the reason is CHARGE_TEXT_IN_ENTRY."""
    c, tok = _lib_client(tmp_path, monkeypatch, None)
    e = next(x for x in c.get(f"/api/cases/{tok}").json()["entries"] if x["id"] == "e4")
    from app.backend import review as RV
    with pytest.raises(RV.ReviewError) as ei:
        RV._check_summary("e4", e["summary"] + " one hundred eighty-five dollars", e["excerpt"] + " It is one hundred eighty-five dollars per visit.", "x", "2026-01-01", (0, 1),
                          {"excerpt": e["excerpt"] + " It is one hundred eighty-five dollars per visit.", "n": 1, "id": "r1", "source": "x"}, lambda *a, **k: ({}, "c"))
    assert "CHARGE_TEXT_IN_ENTRY" in str(ei.value.detail) or "dollar amount" in str(ei.value)


# ---------------------------------------------------------------- 2. the held-out hint states the true reason
# The records whose figures are never charges whatever the amount classifier says (adjuster r2 heldout census): the hint must say they are not counted.
NOT_COUNTED = {("case_03_rate_and_ocr", "e2"), ("case_lib09_spanish_interpreter_espalda", "e7"), ("case_lib10_eob_ub04_cms1500", "e8"),
               ("case_lib14_handwritten_chiro_scans", "e7"), ("case_lib15_conclusory_letter_mist", "e9")}


def _held():
    """{(case, entry id): served entry view} for every held-out entry over the golden and library cases, through the same view code the API serves."""
    out, amts = {}, {}
    from app.backend import ingest as IN
    for p in sorted((ROOT / "evals" / "golden").glob("case_*.txt")) + sorted((ROOT / "evals" / "library").glob("case_*.txt")):
        text = p.read_text()
        with PL._Backend("fixture"), tempfile.TemporaryDirectory() as tmp:
            conn, cid, call = PL._scratch_call(tmp, IN.normalize_text(text))
            with contextlib.nullcontext():
                PL.run_pipeline(conn, cid, text, call=call)
            its = present.all_items(conn, cid)
            amts[p.stem] = its["amount"]
            for e in its["entry"]:
                if "CHARGE_TEXT_IN_ENTRY" in e["reasons"]:
                    out[(p.stem, e["id"])] = e
            conn.close()
    return out, amts


def _expected_state(e, amts):
    """What the served amounts of the entry's record say (the true cause), independent of the code under test."""
    rows = [a for a in amts if a["state"] != "rejected" and set(a["record_ids"]) & set(e["record_ids"])]
    ch = [a for a in rows if a["kind"] == "charge" and a["review_status"] != "dismissed"]
    if any(a["review_status"] in ("accepted", "edited") for a in ch):
        return "listed"
    if ch:
        return "pending"
    if any(a["kind"] == "charge" for a in rows):
        return "dismissed"
    return "not_totaled" if rows else "none"


WORDS = {"listed": "already listed under Billed charges", "pending": "once you accept them", "dismissed": "You dismissed this record's charge",
         "not_totaled": "read but not totaled", "none": "No amount was read from this record"}


def test_each_held_entry_says_the_true_reason():
    """T-139 r4 (adjuster r3): 6 of 11 held-out hints said 'No charge was read' for records whose amounts WERE read. Each hint now follows the served amounts."""
    held, amts = _held()
    assert NOT_COUNTED <= set(held) and len(held) >= 9
    seen = set()
    for k, e in held.items():
        st = _expected_state(e, amts[k[0]])
        seen.add(st)
        w = e["why"]
        assert WORDS[st] in w, (k, st, w)
        assert not any(WORDS[o] in w for o in WORDS if o != st), (k, st, w)
        assert "No charge was read" not in w, (k, w)
    assert "not_totaled" in seen
    for k in NOT_COUNTED:
        assert "read but not totaled" in held[k]["why"] or "No amount was read" in held[k]["why"], k


def test_the_422_message_follows_the_same_rule(tmp_path, monkeypatch):
    c, tok = _lib_client(tmp_path, monkeypatch, "case_lib10_eob_ub04_cms1500")
    r = _post(c, tok, "e8", {"action": "accept"})
    assert r.status_code == 422
    msg = str(r.json())
    assert "No charge was read" not in msg and ("read but not totaled" in msg or "No amount was read" in msg)


def test_a_record_with_a_charge_says_its_charges_are_under_billed_charges(tmp_path, monkeypatch):
    """lib01 e2 with narrowing switched off (so it is held): its record has the $3,915 charge amount, pending."""
    monkeypatch.setattr(CT, "narrow_excerpt", lambda excerpt: None)
    c, tok = _lib_client(tmp_path, monkeypatch, "case_lib01_er_only_then_gap")
    e2 = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == "e2")
    assert "CHARGE_TEXT_IN_ENTRY" in e2["reasons"] and "once you accept them" in e2["why"] and "under Billed charges" in e2["why"]
    assert "once you accept them" in c.get(f"/api/cases/{tok}/items/e2").json()["item"]["why"]
    r = _post(c, tok, "e2", {"action": "accept"})
    assert r.status_code == 422 and "once you accept them" in r.json()["error"]["message"]
    a1 = next(a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["kind"] == "charge")
    assert _post(c, tok, a1["id"], {"action": "accept"}).status_code == 200
    r = _post(c, tok, "e2", {"action": "accept"})
    assert "already listed under Billed charges" in r.json()["error"]["message"]
    assert "already listed under Billed charges" in next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["id"] == "e2")["why"]


def test_bill_state_rules():
    amt = lambda kind, rs, st="needs_review": {"kind": kind, "review_status": rs, "state": st}      # noqa: E731
    assert CT.bill_state([]) == "none"
    assert CT.bill_state([amt("rate", "pending")]) == "not_totaled"                   # read, but not a charge: nothing totaled
    assert CT.bill_state([amt("unclear", "pending"), amt("rate", "pending")]) == "not_totaled"
    assert CT.bill_state([amt("charge", "dismissed")]) == "dismissed"
    assert CT.bill_state([amt("charge", "pending", "rejected")]) == "none"
    assert CT.bill_state([amt("charge", "pending")]) == "pending"
    assert CT.bill_state([amt("charge", "accepted"), amt("charge", "pending")]) == "listed"
    assert "already listed under Billed charges" in CT.bill_sentence("listed") and "once you accept" in CT.bill_sentence("pending")
    assert "read but not totaled" in CT.bill_sentence("not_totaled") and "No charge was read" not in CT.bill_sentence("not_totaled")
    assert CT.bill_sentence(None) == ""


def test_a_figure_she_typed_gets_no_bill_sentence():
    """Adjuster r3 minor: the figure is only in a summary she edited and is not on the record, so where the record's charges are counted is beside the point."""
    state = CT.bill_state([{"kind": "unclear", "review_status": "pending", "state": "needs_review", "text": "$85.00", "excerpt": "Charge $85.00 for the office visit."}])
    typed, on_record = {"summary": ["\u20ac4"]}, {"summary": ["$85.00"]}
    assert CT.bill_sentence(state, typed) == "" and "read but not totaled" in CT.bill_sentence(state, on_record)
    assert "read but not totaled" in CT.bill_sentence(state, {"excerpt": ["\u20ac4"]})           # a figure in the quote is on the record by construction
    assert "read but not totaled" not in CT.message(typed, state) and "dollar amount" in CT.message(typed, state)
    assert "read but not totaled" in CT.hold_why({"excerpt": ["$85.00"]}, state)


# ---------------------------------------------------------------- adjuster r2 minor/nit folded in
@pytest.mark.parametrize("quote", ["Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. TOTAL\nCHARGE 49100.",
                                   "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Cost\nestimate 6,500."])
def test_narrowing_never_keeps_half_a_sentence_across_a_line_break(quote):
    n = CT.narrow_excerpt(quote)
    assert n is None or n["excerpt"].rstrip().endswith((".", "!", "?"))


def test_the_422_detail_lists_each_amount_once(tmp_path, monkeypatch):
    monkeypatch.setattr(CT, "narrow_excerpt", lambda excerpt: None)
    c, tok = _lib_client(tmp_path, monkeypatch, "case_lib06_lop_billed_vs_adjusted")
    r = _post(c, tok, "e4", {"action": "accept"})
    amts = r.json()["error"]["detail"]["amounts"]
    assert r.status_code == 422 and len(amts) == len(set(amts)) and amts
