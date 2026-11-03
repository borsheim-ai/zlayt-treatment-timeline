"""D-059 (T-140 round 2): code rules that make an amount `unclear`, flags that need a named confirm, expected totals. Code only (LLM_VS_CODE rows 6/7).
The SYNTHETIC ledger is the claims adjuster's (artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt)."""
import pathlib

import pytest

from app.backend import amounts as AM, ingest, totals as TT

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEDGER = ROOT / "tests" / "fixtures" / "t140_synthetic_ledger_r1.txt"
BILL = "Clinic, billing statement"


def rec(n, excerpt, source=BILL, date="2026-05-01"):
    return {"n": n, "excerpt": excerpt, "source": source, "text": excerpt, "date_iso": date}


def rows(excerpt, source=BILL):
    return {a["raw"]: a for a in AM.extract_amounts([rec(1, excerpt, source)])}


def classes(excerpt, source=BILL):
    return [(a["raw"], a["cls"]) for a in AM.extract_amounts([rec(1, excerpt, source)])]


# ---------------------------------------------------------------- 1. code rules: each is `unclear`, with its reason in the internal notes
NOT_CHARGES = [
    # year to date / running / cumulative
    ("Year-to-date charges $1,100.00", "year-to-date"), ("YTD charges $1,100.00", "year-to-date"), ("Charges year to date $1,100.00", "year-to-date"),
    ("Cumulative charges $500.00", "year-to-date"), ("Accumulated charges $500.00", "year-to-date"), ("Running total $350.00", "total"),
    ("Aggregate charges billed $500.00", "year-to-date"), ("Combined charges $500.00", "year-to-date"), ("All charges $500.00", "year-to-date"),
    ("Sum of charges $500.00", "year-to-date"),
    # previous statement / balance forward
    ("Previous statement $380.00", "previous statement"), ("Prior statement charges $380.00", "previous statement"),
    ("Prior balance carried forward $380.00", "previous statement"), ("Balance forward $380.00", "previous statement"),
    ("Balance brought forward $380.00", "previous statement"), ("Carry-over from 05/01/2026 statement $380.00", "previous statement"),
    ("Previously billed $380.00", "previous statement"), ("Bal fwd $380.00", "previous statement"), ("Unpaid prior charges $380.00", "previous statement"),
    # negative, parentheses, CR
    ("Office visit charge -$100.00", "negative"), ("Office visit charge ($100.00)", "negative"), ("Office visit charge $100.00 CR", "negative"),
    ("Office visit charge $100.00 (credit)", "credit"), ("Manual therapy charge - $100.00", "negative"),
    ("Reversal of 05/07/2026 exercise charge $100.00", "reversal"), ("Void of 05/07 charge $100.00", "reversal"), ("Recoupment of billed $100.00", "reversal"),
    ("Med pay applied to visit charge $100.00", "reversal"), ("Insurance remit applied to evaluation charge $100.00", "reversal"), ("Refund $100.00", "reversal"),
    # statement-level, total, balance, payment, adjustment wordings (staff round 1)
    ("Total, this statement: $380.00", "total"), ("New charges $300.00", "statement-level"), ("Statement amount $300.00", "statement-level"),
    ("Statement total (14 visits): $2,740.00", "total"), ("Totals: $2,740.00", "total"), ("Tot $2,740.00", "total"), ("$2,740.00 total", "total"),
    ("Write off $500.00", "adjustment"), ("W/O $500.00", "adjustment"), ("Adj: $274.00", "adjustment"), ("$274.00 adjustment", "adjustment"),
    ("$300.00 paid", "payment"), ("Ins pd $300.00", "payment"), ("Payment received 06/01/2026 $300.00", "payment"),
    ("$2,166.00 balance due", "balance"), ("Account balance as of 06/15/2026 is $2,166.00", "balance"), ("Bal $2,166.00", "balance"),
    ("Patient responsibility $882.70", "balance"), ("Previous bal $380.00", "previous statement")]


@pytest.mark.parametrize("text,word", NOT_CHARGES)
def test_each_d059_rule_makes_the_amount_unclear_and_names_the_reason(text, word):
    ex = "Statement: " + text + "."
    a = next(iter(rows(ex).values()))
    assert a["cls"] == "unclear", text
    why = AM.not_totaled_reason(ex, a["raw"], a["cents"])
    assert why and word in why.lower(), (text, why)


REAL_CHARGES = ["Chiropractic adjustment charge $65.00", "Adjustment (chiropractic) charge $65.00", "Chiropractic adjustment $65.00", "Total body MRI charge $1,800.00",
                "Balance training exercise charge $45.00", "Balance and gait training charge $45.00", "Total ER charge $6,240.00", "Credit evaluation consult charge $95.00",
                "Total knee replacement charge $9,000.00", "Office visit charge $150.00", "Total of 12 visits billed $2,150.00", "ER charges: $6,240.",
                "Visit due to injury charge $120.00"]


@pytest.mark.parametrize("text", REAL_CHARGES)
def test_a_cue_word_inside_a_service_description_stays_a_charge(text):
    ex = "04/16/2026 " + text + "."          # D-060: an itemized line carries its date of service
    a = next(iter(rows(ex).values()))
    assert a["cls"] == "charge", text
    assert AM.not_totaled_reason(ex, a["raw"], a["cents"]) is None


def test_label_words_in_another_clause_or_sentence_do_not_count():
    ex = "Payment plan discussed; 04/16/2026 radiology charge $180.00. Balance of the visit unremarkable, 04/17/2026 office charge $95.00."
    assert classes(ex) == [("$180.00", "charge"), ("$95.00", "charge")]


# ---------------------------------------------------------------- table rows and columns
@pytest.mark.parametrize("sep", ["\t", " | ", "  "])
def test_a_table_total_row_makes_every_figure_on_the_row_a_non_charge(sep):
    head = "04/16/2026 office visit charge $150.00; 04/17/2026 therapy charge $230.00.\n"
    ex = head + "Total" + sep + "$380.00" + sep + "$77.00" + sep + "$305.00"
    assert classes(ex) == [("$150.00", "charge"), ("$230.00", "charge"), ("$380.00", "unclear"), ("$77.00", "unclear"), ("$305.00", "unclear")]


@pytest.mark.parametrize("line", ["Total / Paid / Balance: $380.00 / $77.00 / $303.00", "| Total | $380.00 | $77.00 | $303.00 |", "TOTAL  $380.00  $77.00  $305.00",
                                  "Balance  $305.00  $0.00", "Payments  $77.00  $20.00"])
def test_row_label_covers_the_whole_row(line):
    assert {c for _, c in classes("Ledger:\n" + line)} == {"unclear"}


def test_a_charges_column_under_a_header_with_several_data_rows():
    ex = ("Date  Description  Charges  Payments  Balance\n06/10/2026  Manual therapy  $150.00  $20.00  $730.00\n06/17/2026  Ins pmt  $0.00  $90.00  $640.00\n"
          "06/24/2026  Manual therapy  $150.00  $0.00  $790.00\nTotal  $300.00  $110.00  $790.00")
    got = classes(ex, "Clinic, account ledger")
    assert [c for r, c in got][:2] == ["charge", "unclear"]
    charges = [r for r, c in got if c == "charge"]
    assert charges == ["$150.00", "$150.00"], got              # row 2 and 3 payments and balances come from the header, not the row above; zeros and the total row are not charges


def test_ub04_fl47_column_stays_a_charge_and_rev_0001_is_a_total():
    fl47 = "UB-04 itemized bill, statement period 06/09/2026 to 06/12/2026. Rev 0450 Emergency room FL47 Total Charges $1,200.00."
    r1 = rows(fl47, "Hospital, UB-04 itemized bill")
    assert r1["$1,200.00"]["cls"] == "charge"
    rev1 = "UB-04 itemized bill. Rev 0001 Total Charges $1,200.00."
    r2 = rows(rev1, "Hospital, UB-04 itemized bill")
    assert r2["$1,200.00"]["cls"] == "unclear"
    assert "total" in AM.not_totaled_reason(rev1, "$1,200.00", 120000).lower()
    bare = "UB-04 itemized bill. Rev 0001 charges billed $8,123.50."                 # the revenue code alone marks the claim's total line, whatever the words
    assert rows(bare, "Hospital, UB-04 itemized bill")["$8,123.50"]["cls"] == "unclear"


# ---------------------------------------------------------------- insurer document
@pytest.mark.parametrize("src,text", [("Quoinmere Mutual Health Plan, EOB", "Amount billed $8,023.50"), ("Acme Mutual, remittance advice", "Provider charges $500.00"),
                                      ("Acme Mutual, explanation of benefits", "Amount billed $500.00"), ("Acme Mutual, EOB", "Billed charges $500.00")])
def test_an_insurer_document_restating_a_provider_charge_is_unclear(src, text):
    a = next(iter(rows("Statement: " + text + ".", src).values()))
    assert a["cls"] == "unclear"
    assert "insurer" in AM.not_totaled_reason("Statement: " + text + ".", a["raw"], a["cents"], src).lower()


def test_the_same_words_on_a_provider_bill_need_a_service_line_to_be_a_charge():
    bill = "Saltmarrow General Hospital, UB-04 itemized bill"
    assert rows("Amount billed $8,023.50.", bill)["$8,023.50"]["cls"] == "unclear"                       # D-060: a bill's summary line is not an itemized service line
    assert rows("06/10/2026 emergency room, amount billed $8,023.50.", bill)["$8,023.50"]["cls"] == "charge"


# ---------------------------------------------------------------- flags that need a named confirm
def test_likely_total_stays_a_charge_but_carries_the_flag():
    ex = "04/16/2026 office visit charge $100.00; 04/17/2026 therapy charge $250.00; 04/18/2026 imaging charge $300.00; 04/19/2026 exam charge $650.00."
    r = rows(ex)
    assert [r[k]["cls"] for k in ("$100.00", "$250.00", "$300.00", "$650.00")] == ["charge"] * 4
    assert r["$650.00"]["confirm"]["flag"] == "likely_total" and r["$650.00"]["confirm"]["confirm_with"] == "likely_total"
    assert all(r[k]["confirm"] is None for k in ("$100.00", "$250.00", "$300.00"))


def test_likely_total_needs_two_other_charges_in_one_record():
    two = "04/16/2026 visit charge $100.00; 04/17/2026 visit charge $100.00."
    assert [a["confirm"] for a in AM.extract_amounts([rec(1, two)])] == [None, None]                    # [100, 100]: the guard is >= 2 others, so no flag
    assert [a["confirm"] for a in AM.extract_amounts([rec(1, "04/16/2026 visit charge $100.00; 04/17/2026 visit charge $200.00.")])] == [None, None]
    split = AM.extract_amounts([rec(1, "04/16/2026 visit charge $100.00; 04/17/2026 visit charge $200.00."), rec(2, "04/18/2026 imaging charge $300.00.")])
    assert [a["confirm"] for a in split] == [None, None, None]       # the sum is across records: no flag
    coincidence = AM.extract_amounts([rec(1, "04/16/2026 visit charge $100.00; 04/17/2026 visit charge $100.00; 04/18/2026 x-ray charge $200.00.")])
    assert [a["confirm"] and a["confirm"]["flag"] for a in coincidence] == [None, None, "likely_total"]      # a coincidence is flagged, never dropped


def test_same_service_on_two_statements_is_one_charge_citing_both_records():
    """D-060: the same normalized date of service + service + amount in another record is the same charge. Not flagged and not counted twice."""
    r2 = rec(2, "Statement 05/01. 04/16/2026 manual therapy charge $150.00; 04/09/2026 therapeutic exercise charge $150.00.", date="2026-05-01")
    r3 = rec(3, "Statement 06/01. 04/16/2026 manual therapy charge $150.00. 05/07/2026 therapeutic exercise charge $150.00.", date="2026-06-01")
    out = AM.extract_amounts([r2, r3])
    assert [(a["record_nos"], a["confirm"], a["cls"]) for a in out] == [([2, 3], None, "charge"), ([2], None, "charge"), ([3], None, "charge")]
    assert out[0]["duplicate_note"] == "Same service, date and amount appears in records 2, 3."


@pytest.mark.parametrize("second", [
    "Apr 16, 2026 manual therapy charge $150.00.", "April 16, 2026 manual therapy charge $150.00.", "16-Apr-2026 manual therapy charge $150.00.",
    "16 April 2026 manual therapy charge $150.00.", "2026-04-16 manual therapy charge $150.00.", "04/16/26 manual therapy charge $150.00.",
    "04/16 manual therapy charge $150.00.", "Manual therapy charge $150.00 (DOS 04/16/2026).", "Manual therapy charge $150.00 for 04/16/2026.",
    "04/16/2026 manual therapy 97140 charge $150.00.", "04/16/2026 Manual Therapy (97140) charge $150.00.",
    "Visit on April 16, 2026: manual therapy charge $150.00."])
def test_the_same_visit_written_another_way_is_the_same_charge(second):
    out = AM.extract_amounts([rec(2, "04/16/2026 manual therapy charge $150.00."), rec(3, second, date="2026-06-01")])
    assert [a["record_nos"] for a in out] == [[2, 3]], second


def test_a_different_date_service_or_amount_is_not_the_same_charge():
    base = "04/16/2026 manual therapy charge $150.00."
    for other in ("04/17/2026 manual therapy charge $150.00.", "04/16/2026 therapeutic exercise charge $150.00.", "04/16/2026 manual therapy charge $160.00.",
                  "04/16/2025 manual therapy charge $150.00."):
        out = AM.extract_amounts([rec(2, base), rec(3, other, date="2026-06-01")])
        assert [a["record_nos"] for a in out] == [[2], [3]], other


def test_two_same_price_lines_of_one_statement_are_two_charges():
    out = AM.extract_amounts([rec(1, "04/09/2026 manual therapy charge $150.00. 04/16/2026 manual therapy charge $150.00. 04/23/2026 imaging charge $90.00.")])
    assert [(a["cents"], a["confirm"]) for a in out] == [(15000, None), (15000, None), (9000, None)]
    same_day = AM.extract_amounts([rec(1, "04/16/2026 manual therapy charge $150.00. 04/16/2026 manual therapy charge $150.00.")])
    assert len(same_day) == 2                                   # one record: never merged


def test_not_a_duplicate_records_never_merge():
    r2, r3 = rec(2, "04/16/2026 manual therapy charge $150.00."), rec(3, "04/16/2026 manual therapy charge $150.00.", date="2026-06-01")
    assert len(AM.extract_amounts([r2, r3])) == 1
    assert [a["record_nos"] for a in AM.extract_amounts([r2, r3], separate={3})] == [[2], [3]]


# ---------------------------------------------------------------- the adjuster's ledgers (tests/fixtures, SYNTHETIC)
def _ledger_records(path):
    return [{**r, "date_iso": r.get("date_iso")} for r in ingest.ingest(path.read_text())["records"]]


@pytest.mark.parametrize("name", ["t140_synthetic_ledger_r1.txt", "t140_synthetic_ledger_r2.txt"])
def test_adjusters_ledgers_total_1950_when_every_charge_is_accepted_one_by_one(name):
    out = AM.extract_amounts(_ledger_records(ROOT / "tests" / "fixtures" / name))
    ch = [a for a in out if a["cls"] == "charge"]
    assert [a["confirm"] for a in ch] == [None] * len(ch)                    # nothing needs a confirm: every acceptance path gives the same total
    t = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": "accepted"} for a in ch])
    assert t["accepted_cents"] == 195000, [(a["record_nos"], a["raw"], a["cls"]) for a in out]
    assert t["letter_line"] == "Billed charges accepted from these records: $1,950.00"
    assert sorted((a["record_nos"][0], a["raw"]) for a in ch) == [(1, "$1,000"), (2, "$150.00"), (2, "$150.00"), (2, "$200.00"), (3, "$150.00"), (4, "$150.00"), (4, "$150.00")]


def test_adjusters_r1_ledger_lines_that_are_not_charges_are_listed_with_their_reason():
    out = AM.extract_amounts(_ledger_records(ROOT / "tests" / "fixtures" / "t140_synthetic_ledger_r1.txt"))
    unclear = {(a["record_nos"][0], a["raw"]) for a in out if a["cls"] == "unclear"}
    for key in [(2, "$380.00"), (2, "$500.00"), (2, "$120.00"), (3, "$380.00"), (3, "$100.00"), (3, "$300.00"), (3, "$580.00"), (4, "$1,100.00"), (4, "$730.00"), (4, "$90.00")]:
        assert key in unclear, key


@pytest.mark.parametrize("text", ["Statement: total billed $310.00.", "Ledger. Amount due: $2,166.00.", "Grand total billed $5,000.00.", "Total charges $2,740.00.", "Statement: office visit charge $100.00 CR."])
def test_reclassify_rule_check_refuses_totals_the_wording_gate_would_pass(text):
    from app.backend import reclassify as RC
    a = AM.find_amounts(text)[0]
    row = {"text": a["raw"], "value_cents": a["cents"], "excerpt_start": None}
    assert RC.charge_wording(text, row) or "CR" in text                                     # the old gate alone lets the wording through
    assert RC._rule_reason(text, row, {"source": BILL})
