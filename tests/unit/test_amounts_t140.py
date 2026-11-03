"""T-140 (GATE-M2 blocker): a total, subtotal, balance, amount due, payment, adjustment, write-off or credit line is never class charge,
whatever the judge says; a charge equal to the sum of the other charges in its record is a likely total. Code only (LLM_VS_CODE rows 6/7)."""
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import amounts as AM, totals as TT
from app.backend.api import create_app

ROOT = pathlib.Path(__file__).resolve().parents[2]
LIB11 = ROOT / "evals" / "library" / "case_lib11_priors_and_ledger.txt"
LEDGER = ("Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; "
          "total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.")


def _rows(excerpt, source="Fennimoor Spine Clinic, itemized ledger"):
    return {a["raw"]: a for a in AM.extract_amounts([{"n": 1, "excerpt": excerpt, "source": source, "text": excerpt, "date_iso": "2026-06-15"}])}


def test_lib11_ledger_classes():
    """D-060: the three ledger lines state no date of service, so they are not itemized service lines: unclear, each with its reason (the paralegal can promote
    one after reading the record). Total, payment, adjustment and balance stay unclear by their own rules."""
    r = _rows(LEDGER)
    assert [r[k]["cls"] for k in ("$250.00", "$180.00", "$2,310.00")] == ["unclear"] * 3
    for k in ("$250.00", "$180.00", "$2,310.00"):
        assert "no date of service" in AM.not_totaled_reason(LEDGER, k, AM.to_cents(k.lstrip("$"))).lower()
    for k in ("$2,740.00", "$300.00", "$274.00", "$2,166.00"):
        assert r[k]["cls"] == "unclear", k
    assert TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": "accepted"} for a in r.values()])["accepted_cents"] == 0


def test_lib11_ledger_with_a_date_on_each_line_totals_its_three_charges():
    dated = LEDGER.replace("New patient exam charge", "06/01/2026 new patient exam charge").replace("x-ray charge", "06/01/2026 x-ray charge").replace(
        "treatment visits 1 through 14 charge", "06/02/2026 treatment visit charge")
    r = _rows(dated)
    assert [r[k]["cls"] for k in ("$250.00", "$180.00", "$2,310.00")] == ["charge"] * 3
    assert TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": "accepted"} for a in r.values()])["accepted_cents"] == 250_00 + 180_00 + 2310_00


@pytest.mark.parametrize("text,word", [
    ("Total $900.00", "total"), ("Subtotal: $900.00", "total"), ("Statement total $900.00", "total"), ("Balance due $900.00", "balance"),
    ("Balance: $900.00", "balance"), ("Amount due $900.00", "balance"), ("Patient paid $900.00", "payment"), ("Payment received $900.00", "payment"),
    ("Payments to date $900.00", "payment"), ("Adjustment -$900.00", "adjustment"), ("Insurance write-off $900.00", "adjustment"),
    ("Courtesy credit $900.00", "adjustment"), ("Contractual adjustment $900.00", "adjustment")])
def test_total_balance_payment_adjustment_labels_are_never_charges(text, word):
    a = next(iter(_rows("Statement of account: " + text + ".").values()))
    assert a["cls"] == "unclear"
    reason = AM.not_totaled_reason("Statement of account: " + text + ".", a["raw"], a["cents"])
    assert reason and word in reason.lower()


@pytest.mark.parametrize("text", ["Office visit charge $150.00", "ER charges: $6,240.", "MRI charge: $2,150.", "Total of 12 visits billed $2,150.00", "Office visit billed $400.00"])
def test_ordinary_charge_labels_stay_charges(text):
    text = "04/16/2026 " + text                  # D-060: an itemized line carries its date of service
    a = next(iter(_rows(text + ".", source="Clinic, billing statement").values()))
    assert a["cls"] == "charge"
    assert AM.not_totaled_reason(text + ".", a["raw"], a["cents"]) is None


def test_word_must_be_the_label_not_anywhere_in_the_sentence():
    ex = "Payment plan discussed; 04/16/2026 radiology charge $180.00. Balance of the visit unremarkable, 04/17/2026 office charge $95.00."
    r = _rows(ex, source="Clinic, billing statement")
    assert r["$180.00"]["cls"] == "charge" and r["$95.00"]["cls"] == "charge"


def test_column_label_of_a_table():
    ex = "Date  Description  Charges  Payments  Adjustments  Balance\n06/01/2026  Office visit  $500.00  $100.00  $50.00  $350.00"
    r = _rows(ex, source="Clinic, billing statement")
    assert AM.not_totaled_reason(ex, "$500.00", 50000) is None      # the Charges column is not a non-charge label
    assert [r[k]["cls"] for k in ("$100.00", "$50.00", "$350.00")] == ["unclear"] * 3
    assert "payment" in AM.not_totaled_reason(ex, "$100.00", 10000).lower() and "balance" in AM.not_totaled_reason(ex, "$350.00", 35000).lower()


def test_a_judge_cannot_make_a_total_a_charge():
    """The class is decided by code; extract_amounts has no judge input, and the reason is recomputed from the quote at export."""
    assert "judge" not in AM.classify.__code__.co_varnames and "verdict" not in AM.classify.__code__.co_varnames


def test_cross_check_flags_a_charge_equal_to_the_others():
    """D-059: a charge equal to the sum of the others of its record stays a charge and carries the likely_total flag (accepting it needs a named confirm)."""
    ex = "04/16/2026 office visit charge $100.00; 04/17/2026 therapy charge $250.00; 04/18/2026 imaging charge $300.00; 04/19/2026 exam charge $650.00."
    r = _rows(ex, source="Clinic, billing statement")
    assert [r[k]["cls"] for k in ("$100.00", "$250.00", "$300.00", "$650.00")] == ["charge"] * 4
    assert r["$650.00"]["confirm"]["flag"] == "likely_total" and "sum of the other charges" in r["$650.00"]["confirm"]["message"]


def test_cross_check_needs_two_other_charges_and_one_record():
    two = _rows("04/16/2026 office visit charge $100.00; 04/17/2026 therapy charge $200.00.", source="Clinic, billing statement")
    assert [a["cls"] for a in two.values()] == ["charge", "charge"] and [a["confirm"] for a in two.values()] == [None, None]
    recs = [{"n": 1, "excerpt": "04/16/2026 visit charge $100.00; 04/17/2026 visit charge $200.00.", "source": "Clinic, billing statement", "text": "x", "date_iso": "2026-01-01"},
            {"n": 2, "excerpt": "04/18/2026 imaging charge $300.00.", "source": "Clinic, billing statement", "text": "y", "date_iso": "2026-01-02"}]
    assert [a["confirm"] for a in AM.extract_amounts(recs)] == [None] * 3          # $300 is the sum, but of lines in another record


# ---- end to end: accept everything on lib11 and export
@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.setenv("ZLAYT_MODE", "local")
    return TestClient(create_app(str(tmp_path / "t140.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def test_lib11_accept_all_export_total_is_the_ed_charge_only(client):
    c = client
    tok = c.post("/api/cases", json={"library": LIB11.stem}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready", s
    g = c.get(f"/api/cases/{tok}").json()
    for it in g["entries"] + g["amounts"] + g["flags"]:
        c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "accept", "compared": True})      # D-066: a disputed item is accepted with her compare
    ex = c.get(f"/api/cases/{tok}/export").json()
    assert "letter_text" in ex, ex
    assert "Billed charges accepted from these records: $3,260.00" in ex["letter_text"].split("\n")       # D-060: the ledger lines carry no date of service
    assert ex["totals"]["charges_cents"] == 326000
    notes = ex["internal_notes_text"].split("AMOUNTS NOT TOTALED")[1].split("\n\n")[0]
    for fig in ("$250", "$180", "$2,310", "$2,740", "$300", "$274", "$2,166"):
        assert fig in notes, fig
    assert notes.count(AM._NO_DATE_WHY) == 3
    for fig, why in (("$2,740", AM._WHY_OF["total"]), ("$300", AM._WHY_OF["payment"]), ("$274", AM._WHY_OF["adjustment"]), ("$2,166", AM._WHY_OF["balance"])):
        assert f"Not totaled ({fig}" in notes and why in notes, fig              # the exact reason line of each figure (export.py), not the quote's own words
    assert "$2,740" not in ex["letter_text"] and "$2,166" not in ex["letter_text"]


# ---- the eval check: accept-all total of a library case vs its expected total (D-059: acceptable lines accepted one at a time, flagged lines not)
LIBRARY = sorted(p.stem for p in (ROOT / "evals" / "library").glob("case_*.txt"))


@pytest.mark.parametrize("case", LIBRARY)
def test_library_accept_all_total_equals_expected(case, monkeypatch):
    import json
    from evals import library_report as LR
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    from app import pipeline
    exp = json.loads((ROOT / "evals" / "library" / f"{case}.expected.json").read_text())
    row = LR.score(case, (ROOT / "evals" / "library" / f"{case}.txt").read_text(), exp, pipeline)
    assert row["accept_all_ok"], row["accept_all"]
    assert LR.accept_all_total_cents(pipeline.run_case((ROOT / "evals" / "library" / f"{case}.txt").read_text(), "fixture")) == LR.expected_accept_all_cents(exp)


@pytest.mark.parametrize("case,total", [("case_lib10_eob_ub04_cms1500", 812350)])
def test_library_expected_totals_are_the_hand_verified_ones(case, total):
    import json
    exp = json.loads((ROOT / "evals" / "library" / f"{case}.expected.json").read_text())
    assert round(exp["totals"]["explicit_charges_total"] * 100) == total and "accept_all_total" not in exp["totals"]


@pytest.mark.parametrize("case,explicit,accept_all", [("case_lib04_dog_bite_scar_revision", 8630, 4730), ("case_lib05_pedestrian_orif_hardware", 44570, 38420),
                                                      ("case_lib06_lop_billed_vs_adjusted", 6830, 5280), ("case_lib09_spanish_interpreter_espalda", 6390, 5090),
                                                      ("case_lib11_priors_and_ledger", 6000, 3260), ("case_lib12_records_review_credibility", 5790, 2780),
                                                      ("case_lib15_conclusory_letter_mist", 3295, 385)])
def test_library_undercounts_are_hand_verified_totals_carry_a_written_reason(case, explicit, accept_all):
    import json
    t = json.loads((ROOT / "evals" / "library" / f"{case}.expected.json").read_text())["totals"]
    assert t["explicit_charges_total"] == explicit and t["accept_all_total"] == accept_all and len(t["accept_all_reason"]) > 80 and "Hand-verified" in t["accept_all_reason"]


def test_library_check_catches_a_counted_total():
    """The check is not a tautology: a run whose ledger total were classed as a charge reports WRONG with both figures."""
    from evals import library_report as LR
    out = {"records": [{"n": 1, "source": "Clinic, billing statement", "date_iso": "2026-01-01", "excerpt": "Visit charge $100.00; total charges $100.00."}],
           "amounts": [{"id": "a1", "record_nos": [1], "cents": 10000, "kind": "charge", "raw": "$100.00", "excerpt": "Visit charge $100.00; total charges $100.00.", "state": "verified"},
                       {"id": "a2", "record_nos": [1], "cents": 10000, "kind": "charge", "raw": "$100.00", "excerpt": "Visit charge $100.00; total charges $100.00.", "state": "verified"}]}
    assert LR.accept_all_total_cents(out) == 20000      # both offered as charges -> the letter would print $200.00, not the expected $100.00



def test_library_accept_all_leaves_out_a_flagged_charge():
    """D-059: a charge with a likely-duplicate or likely-total flag cannot be accepted without a named confirm, so the accept-all total does not include it."""
    from evals import library_report as LR
    ex = "04/16/2026 manual therapy charge $150.00."
    base = {"record_nos": [1], "cents": 15000, "kind": "charge", "raw": "$150.00", "excerpt": ex, "state": "verified"}
    out = {"records": [{"n": 1, "source": "Clinic, billing statement", "date_iso": "2026-01-01", "excerpt": ex}],
           "amounts": [{"id": "a1", **base}, {"id": "a2", **base, "ladder": {"confirm": {"flag": "likely_duplicate"}}}]}
    assert LR.accept_all_total_cents(out) == 15000
