"""D-060 (T-140 round 3): a charge is default-deny. An amount is class `charge` only on an itemized service line of a provider bill or ledger (a date of service, a
service description and the amount on one line or row) or, in a dated encounter record, beside a service with a charge word. Everything else is `unclear` with its
reason. Duplicates match on normalized date of service + service + amount. Citations are taken from the figure's own offset. Code only (LLM_VS_CODE rows 6/7)."""
import pathlib

import pytest

from app.backend import amounts as AM

ROOT = pathlib.Path(__file__).resolve().parents[2]
BILL = "Brindlewood Physical Therapy, billing statement"
PREFIX = "Statement date 06/01/2026. 05/07/2026 exercise charge $150.00; 05/14/2026 manual therapy charge $160.00. "
LABELS = [ln for ln in (ROOT / "tests" / "fixtures" / "t140_restating_labels.txt").read_text().splitlines()[1:] if ln.strip()]


def rec(n, excerpt, source=BILL, date="2026-06-01"):
    return {"n": n, "excerpt": excerpt, "source": source, "text": excerpt, "date_iso": date}


def cls(excerpt, source=BILL, date="2026-06-01"):
    return [(a["raw"], a["cls"]) for a in AM.extract_amounts([rec(1, excerpt, source, date)])]


def why(excerpt, raw, source=BILL, date="2026-06-01"):
    a = next(a for a in AM.find_amounts(excerpt) if a["raw"] == raw)
    return AM.not_totaled_reason(excerpt, raw, a["cents"], source, date, a["start"])


# ---------------------------------------------------------------- default-deny on a provider bill
@pytest.mark.parametrize("source", [BILL, "Brindlewood Physical Therapy, patient statement", "Brindlewood Physical Therapy, account ledger",
                                    "Brindlewood Physical Therapy, visit 8"])
def test_no_restating_wording_becomes_a_charge(source):
    """180 statement-level, year-to-date, earlier-statement and summary wordings from the adjuster's and staff's probes: none is a charge, whatever the record's label."""
    leaks = []
    for lab in LABELS:
        ex = PREFIX + lab
        got = [(a["raw"], a["cls"]) for a in AM.extract_amounts([rec(1, ex, source)]) if a["start"] >= len(PREFIX)]
        if any(c == "charge" for _, c in got):
            leaks.append((lab, got))
    assert not leaks, leaks


def test_the_two_real_lines_before_the_labels_stay_charges():
    assert cls(PREFIX + "Statement charges $730.00.") == [("$150.00", "charge"), ("$160.00", "charge"), ("$730.00", "unclear")]


@pytest.mark.parametrize("ex,reason_part", [
    ("Last statement $500.00.", "earlier statement"), ("Charges $650.00 year to date.", "year-to-date"), ("Charges $730.00 YTD.", "year-to-date"),
    ("Charges $730.00 to date.", "year-to-date"), ("Charges $730.00 in all.", "year-to-date"), ("Charges $730.00 combined.", "year-to-date"),
    ("Charges: $730.00 (sum of the above).", "year-to-date"), ("Charges $730.00 (all statements).", "year-to-date"), ("Carried over charges $730.00.", "previous"),
    ("Charges $730.00 carried over.", "previous"), ("Statement charges $730.00.", "statement-level")])
def test_running_and_earlier_statement_words_after_the_figure_name_their_reason(ex, reason_part):
    """Staff r2: the label may come after the figure ('Charges $730.00 YTD'); default-deny and the after-figure rules both refuse it, with a reason."""
    text = "04/16/2026 physical therapy " + ex
    got = why(text, "$500.00" if "$500" in text else ("$650.00" if "$650" in text else "$730.00"))
    assert got and reason_part in got.lower(), (ex, got)
    assert cls(text)[-1][1] == "unclear"


def test_a_ledger_row_without_a_service_is_not_a_charge_even_in_the_charges_column():
    ex = ("Date  Description  Charges  Payments  Balance\n05/07/2026  Exercise  $150.00  $0.00  $150.00\n05/14/2026  Manual therapy  $160.00  $0.00  $310.00\n"
          "06/30/2026  Account summary  $950.00  $90.00  $860.00")
    assert [c for _, c in cls(ex, "Brindlewood Physical Therapy, account ledger")][:1] == ["charge"]
    got = dict(((r, c) for r, c in cls(ex, "Brindlewood Physical Therapy, account ledger")))
    assert got["$950.00"] == "unclear" and got["$160.00"] == "charge"
    assert "names no service" in why(ex, "$950.00", "Brindlewood Physical Therapy, account ledger")
    for desc in ("—", "*", "Summary", "Totals for period"):
        row = ex.replace("Account summary", desc)
        assert dict(cls(row, "Brindlewood Physical Therapy, account ledger"))["$950.00"] == "unclear", desc


def test_only_the_charges_column_of_a_ledger_row_is_a_candidate():
    ex = "Date  Description  Charges  Qty  Reference\n06/10/2026  Manual therapy  $150.00  $20.00  $730.00"
    got = dict(cls(ex, "Clinic, account ledger"))
    assert got == {"$150.00": "charge", "$20.00": "unclear", "$730.00": "unclear"}
    assert "charges column" in why(ex, "$20.00", "Clinic, account ledger")
    headerless = "06/10/2026  Manual therapy  $150.00  $20.00  $730.00"
    assert [c for _, c in cls(headerless, "Clinic, account ledger")] == ["charge", "unclear", "unclear"]      # no heading: only the first figure of a row


@pytest.mark.parametrize("ex", ["Manual therapy charge $150.00.", "Charge $150.00 for 04/16/2026.", "04/16/2026 charge $150.00.",
                                "Statement date 04/16/2026 manual therapy charge $150.00.", "As of 04/16/2026 manual therapy charge $150.00.",
                                "04/01/2026 - 04/30/2026 manual therapy charge $150.00.", "Manual therapy charge $150.00 through 04/30/2026.",
                                "Due 04/30/2026: manual therapy charge $150.00.", "04/31/2026 manual therapy charge $150.00."])
def test_a_line_needs_its_own_date_of_service_and_its_own_service(ex):
    assert dict(cls(ex))["$150.00"] == "unclear", ex


@pytest.mark.parametrize("ex", ["04/16/2026 manual therapy charge $150.00.", "Apr 16, 2026 manual therapy charge $150.00.", "16-Apr-2026 manual therapy charge $150.00.",
                                "Manual therapy charge $150.00 (DOS 04/16/2026).", "Manual therapy charge $150.00 for 04/16/2026.", "04/16 manual therapy charge $150.00.",
                                "2026-04-16 manual therapy 97140 $150.00.", "Facility charge $150.00 for 04/16/2026 manual therapy.", "Visit on April 16, 2026: manual therapy charge $150.00.",
                                "Statement for visit of 2026-04-16: $150.00."])
def test_an_itemized_line_in_any_date_form_is_a_charge(ex):
    assert dict(cls(ex))["$150.00"] == "charge", ex


def test_a_coded_line_takes_the_date_the_record_states_for_its_services():
    ub = "UB-04 itemized bill, statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
    assert dict(cls(ub, "Saltmarrow General Hospital, UB-04 itemized bill"))["$2,105.00"] == "charge"
    undated = "UB-04 itemized bill. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
    assert dict(cls(undated, "Saltmarrow General Hospital, UB-04 itemized bill"))["$2,105.00"] == "unclear"
    run = "Invoice for the run of 09/14/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00."
    assert dict(cls(run, "Tarnwick Fire-Rescue, ambulance invoice"))["$1,380.00"] == "charge"
    statement_date = "Invoice dated 09/20/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00."
    assert dict(cls(statement_date, "Tarnwick Fire-Rescue, ambulance invoice"))["$1,380.00"] == "unclear"      # an invoice date is not a date of service


def test_a_per_mile_figure_is_a_rate_and_its_extended_line_is_the_charge():
    ex = "Invoice for the run of 09/14/2026. A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05."
    assert cls(ex, "Tarnwick Fire-Rescue, ambulance invoice") == [("$21.50", "rate"), ("$187.05", "charge")]


# ---------------------------------------------------------------- dated encounter records (the sample, the library's ED and imaging notes)
@pytest.mark.parametrize("ex,src,want", [
    ("Follow up with PCP in 1 week. ER charges: $6,240.", "Central ER discharge summary", "charge"),
    ("Correlate clinically. Charge: $2,150.", "Austin Imaging, cervical MRI", "charge"),
    ("Visit charge: $410.", "Tamsin Valley Urgent Care", "charge"),
    ("Charge: $2,150.", "Dr. Smith, note", "unclear"),                                       # bare 'Charge:' needs a header that names the service
    ("Billed charges: $2,150.", "Austin Imaging, cervical MRI", "unclear"),                  # more than the bare word 'charge'
    ("Statement charges $730.00.", "Brindlewood Physical Therapy, visit 8", "unclear"),
    ("Charges $730.00 year to date.", "Brindlewood Physical Therapy, visit 8", "unclear"),
    ("Charges: $2,150. Total to date.", "Austin Imaging, cervical MRI", "charge"),            # the next sentence is its own
    ("Charge: $2,150 year to date.", "Austin Imaging, cervical MRI", "unclear"),
    ("MRI charge $1,000 for the whole course.", "Austin Imaging, cervical MRI", "charge"),
    ("Charges: $4,000.", "Pennyroyal Records Retrieval, 18.001 affidavit", "unclear"),         # a letter or affidavit is not a bill
    ("ED charge: $1,000.", None, "unclear")])           # D-062: a document with no header is unknown and never yields a charge
def test_encounter_record_charges(ex, src, want):
    assert dict(cls(ex, src, "2026-04-01"))[AM.find_amounts(ex)[0]["raw"]] == want


# ---------------------------------------------------------------- insurer restatements
@pytest.mark.parametrize("src", ["Acme Mutual Insurance, payment history", "Acme Mutual, claim summary", "Blue Cross, claims history", "Carrier ledger, Acme Casualty"])
def test_an_insurers_payment_history_is_not_a_second_bill(src):
    ex = "Date of service  Service  Billed  Allowed  Paid\n04/09/2026  Ther exercise 97110  $150.00  $90.00  $72.00"
    assert {c for _, c in cls(ex, src)} == {"unclear"}
    assert "insurer" in why(ex, "$150.00", src).lower()


def test_a_table_with_billed_and_allowed_columns_is_the_plans_restatement_whatever_its_label():
    ex = "Date of service  Service  Billed  Allowed  Paid\n04/09/2026  Ther exercise 97110  $150.00  $90.00  $72.00"
    assert {c for _, c in cls(ex, "Records page 4")} == {"unclear"}


def test_a_provider_bill_that_merely_mentions_an_eob_keeps_its_own_charge():
    ex = "04/16/2026 emergency room charge $730.00; the EOB reports the same $730.00 as billed."
    got = cls(ex, "Riverside Hospital, billing statement")
    assert got[0] == ("$730.00", "charge") and AM.not_totaled_reason(ex, "$730.00", 73000, "Riverside Hospital, billing statement", "2026-06-01", AM.find_amounts(ex)[0]["start"]) is None


def test_an_excerpt_that_opens_as_an_eob_is_an_insurer_document_under_any_label():
    ex = "EOB: amount billed $500.00."
    assert dict(cls(ex, "Clinic, billing statement"))["$500.00"] == "unclear"
    assert "insurer" in why(ex, "$500.00", "Clinic, billing statement").lower()


def test_negative_and_zero_figures_are_never_charges():
    assert dict(cls("04/16/2026 manual therapy charge $100.00-."))["$100.00"] == "unclear"        # trailing minus
    assert dict(cls("04/16/2026 manual therapy charge $0.00."))["$0.00"] == "unclear"
    assert "zero" in why("04/16/2026 manual therapy charge $0.00.", "$0.00").lower()


# ---------------------------------------------------------------- duplicates: normalized date of service + service + amount
def test_the_same_visit_on_two_statements_is_one_charge_in_any_date_form_and_it_cites_both_records():
    r2 = rec(2, "Statement date 05/01/2026. 04/16/2026 manual therapy charge $150.00.", date="2026-05-01")
    r3 = rec(3, "Statement date 06/01/2026. Apr 16, 2026 manual therapy charge $150.00.", date="2026-06-01")
    out = AM.extract_amounts([r2, r3])
    assert len(out) == 1 and out[0]["record_nos"] == [2, 3] and out[0]["cls"] == "charge" and out[0]["confirm"] is None


def test_a_restatement_in_an_insurer_table_adds_nothing():
    ex5 = "Date of service  Service  Charges submitted  Allowed  Paid\n04/09/2026  PT evaluation  $200.00  $120.00  $96.00"
    out = AM.extract_amounts([rec(1, "04/09/2026 PT evaluation charge $200.00."), rec(2, ex5, "Acme Mutual, explanation of benefits")])
    assert [(a["record_nos"], a["cls"]) for a in out if a["cents"] == 20000] == [([1], "charge"), ([2], "unclear")]


def test_a_charge_promotion_flag_names_the_duplicate_and_the_total():
    ex = "04/16/2026 manual therapy invoiced $150.00."
    b = AM.charge_basis(ex, {"start": ex.index("$"), "end": ex.index("$") + 7, "cents": 15000}, "Clinic, visit note", "2026-05-01")
    assert b["dos"] == "2026-04-16" and not b["ok"]
    other = {"id": "a1", "record_no": 1, "cents": 15000, "basis": b}
    t = {"id": "a2", "record_no": 2, "cents": 15000, "basis": b}
    f = AM.promotion_flag(t, [other])
    assert f["flag"] == "likely_duplicate" and f["of"] == "a1" and f["confirm_with"] == "likely_duplicate"
    assert AM.promotion_flag({**t, "record_no": 1}, [other]) is None                                  # same record: two lines, not a duplicate
    three = [{"id": f"x{i}", "record_no": 2, "cents": c, "basis": {**b, "dos": f"2026-04-{10 + i}"}} for i, c in enumerate((10000, 5000))]
    assert AM.promotion_flag({"id": "t", "record_no": 2, "cents": 15000, "basis": {**b, "dos": "2026-05-01"}}, three)["flag"] == "likely_total"


# ---------------------------------------------------------------- the reason and the quote come from the figure's own offset
def test_not_totaled_reason_reads_the_figure_at_its_own_offset():
    ex = "04/09/2026 manual therapy charge $150.00. Reversal of 05/07/2026 exercise charge $150.00."
    first, second = (a["start"] for a in AM.find_amounts(ex))
    assert AM.not_totaled_reason(ex, "$150.00", 15000, BILL, "2026-06-01", first) is None
    assert "reversal" in AM.not_totaled_reason(ex, "$150.00", 15000, BILL, "2026-06-01", second).lower()
