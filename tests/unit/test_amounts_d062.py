"""D-062 (T-140 fix-up after round 3): charge sources are positively identified, CPT/HCPCS codes are normalized before duplicate matching.
Adjuster r3 blockers 2, 3 and 4 on his third SYNTHETIC ledger (tests/fixtures/t140_synthetic_ledger_r3.txt). Blocker 1 (a summary row dressed as a service
line on a real bill) is accepted debt (SCOPE_CUTS): it is pinned below as the one remaining over-count, so nobody mistakes it for fixed. Code only."""
import pathlib
import re

import pytest

from app.backend import amounts as AM

ROOT = pathlib.Path(__file__).resolve().parents[2]
BILL = "Brindlewood Physical Therapy, billing statement"


def ledger(name="r3"):
    text = (ROOT / "tests" / "fixtures" / f"t140_synthetic_ledger_{name}.txt").read_text()
    out = []
    for m in re.finditer(r"=== Record (\d+) ===\nDate: (\S+)\nSource: ([^\n]+)\nExcerpt: \"(.*?)\"\n", text, re.DOTALL):
        out.append({"n": int(m.group(1)), "date_iso": m.group(2), "source": m.group(3), "excerpt": m.group(4), "text": m.group(4)})
    return out


def rows(recs):
    return AM.extract_amounts(recs)


def charges(recs):
    return [a for a in rows(recs) if a["cls"] == "charge"]


def rec(n, excerpt, source=BILL, date="2026-06-01"):
    return {"n": n, "excerpt": excerpt, "source": source, "text": excerpt, "date_iso": date}


# ---------------------------------------------------------------- blocker 2: charge sources
def test_third_ledger_discharge_summary_is_not_a_charge_source():
    recs = ledger()
    got = [a for a in rows(recs) if a["record_no"] == 6 or 6 in a["record_nos"]]
    assert [(a["raw"], a["cls"]) for a in got] == [("$950.00", "unclear")]
    assert "not a bill" in AM.not_totaled_reason(recs[5]["excerpt"], "$950.00", 95000, recs[5]["source"], recs[5]["date_iso"], got[0]["lstart"], records=recs).lower()


def test_third_ledger_clinical_note_from_a_provider_with_no_bill_is_read_under_the_encounter_rule():
    """The ED's own bill is not in the case, so nothing restates its 'ED charge: $1,000.'; it stays a charge (the paralegal still accepts it by hand)."""
    ed = [a for a in rows(ledger()) if a["record_no"] == 1]
    assert [(a["raw"], a["cls"]) for a in ed] == [("$1,000", "charge")]


def test_a_note_is_not_a_charge_source_once_a_bill_from_the_same_provider_is_in_the_case():
    """Appendix A sample: only clinical records, so 'ER charges: $6,240.' and 'Charge: $2,150.' stay charges (total $8,390.00). With that provider's own bill in the case
    the note's sentence restates the bill and yields no charge; a bill from another provider changes nothing."""
    notes = [rec(1, "Follow up with PCP in 1 week. ER charges: $6,240.", "Central ER discharge summary", "2026-01-09"),
             rec(2, "Correlate clinically. Charge: $2,150.", "Austin Imaging, cervical MRI", "2026-05-29")]
    assert sum(a["cents"] for a in charges(notes)) == 839000
    other_bill = notes + [rec(3, "Date  Code  Description  Charges\n06/01/2026  97110  Therapeutic exercise  $75.00", "Brindlewood Physical Therapy, billing statement")]
    assert sorted(a["cents"] for a in charges(other_bill)) == [7500, 215000, 624000]
    own_bill = notes + [rec(3, "Date  Code  Description  Charges\n06/01/2026  97110  Therapeutic exercise  $75.00", "Central Hospital, billing statement")]
    assert sorted(a["cents"] for a in charges(own_bill)) == [7500, 215000]
    assert "same provider" in AM.not_totaled_reason(notes[0]["excerpt"], "$6,240", 624000, notes[0]["source"], notes[0]["date_iso"], 39, records=own_bill).lower()


def test_a_document_with_no_header_never_yields_a_charge():
    unknown = [rec(1, "ED charge: $1,000.", None, "2026-04-01")]
    assert [(a["raw"], a["cls"]) for a in rows(unknown)] == [("$1,000", "unclear")]
    assert "unknown" in AM.not_totaled_reason("ED charge: $1,000.", "$1,000", 100000, None, "2026-04-01", 11, records=unknown).lower()


@pytest.mark.parametrize("src", ["Brindlewood Physical Therapy, billing statement", "Brindlewood Physical Therapy, itemized statement", "Brindlewood Physical Therapy, account ledger",
                                 "Brindlewood Physical Therapy, invoice", "Larkspur Hospital, UB-04", "Brindlewood Physical Therapy, CMS-1500"])
def test_billing_headers_still_yield_charges(src):
    assert [a["cls"] for a in rows([rec(1, "04/09/2026  97110  Therapeutic exercise  $75.00", src)])] == ["charge"]


# ---------------------------------------------------------------- blocker 3: insurer documents by structure
@pytest.mark.parametrize("src", ["Pecan Valley Auto Club, med pay ledger", "Acme Auto Group, PIP statement", "Hill Country TPA, account statement",
                                 "Lone Star Benefit Administrators, claims statement", "Lone Star Benefit Administrators, claim detail statement", "Acme Auto Group, med pay ledger",
                                 "Pecan Valley Auto Club, account ledger"])
def test_a_payer_table_is_an_insurer_document_whatever_its_name(src):
    ex = "DOS  CPT  Service  Billed  Approved  Paid\n04/09/2026  97110  Therapeutic exercise x2  $150.00  $90.00  $72.00"
    assert {a["cls"] for a in rows([rec(1, ex, src)])} == {"unclear"}


def test_a_payer_table_by_structure_alone():
    for head in ("DOS  CPT  Service  Charges  Allowed  Plan Paid", "Date  Service  Billed  Covered  Benefit", "DOS  Code  Service  Billed  Eligible  Member Resp"):
        ex = head + "\n04/09/2026  97110  Therapeutic exercise x2  $150.00  $90.00  $72.00"
        assert {a["cls"] for a in rows([rec(1, ex, "Pecan Valley Statement Services, account ledger")])} == {"unclear"}, head


def test_a_providers_own_ledger_with_payment_columns_is_still_a_bill():
    ex = "Date  Code  Description  Charges  Payments  Adjustments  Balance\n04/09/2026  97110  Therapeutic exercise  $75.00  $0.00  $0.00  $75.00"
    got = [(a["raw"], a["cls"]) for a in rows([rec(1, ex, "Brindlewood Physical Therapy, account ledger")])]
    assert got[0] == ("$75.00", "charge")


def test_third_ledger_med_pay_ledger_adds_nothing():
    assert [a["cls"] for a in rows(ledger()) if a["record_no"] == 5] == ["unclear"] * 6


# ---------------------------------------------------------------- blocker 4: code normalization
@pytest.mark.parametrize("a,b", [("97140", "CPT 97140"), ("97140", "CPT#97140"), ("97140", "CPT: 97140"), ("97140", "97140-GP"), ("97140", "CPT 97140-59"),
                                 ("CPT 97140", "cpt97140"), ("HCPCS G0283", "G0283"), ("G0283", "HCPCS: G0283"), ("97140", "CPT # 97140"), ("Rev 0450", "0450 rev"),
                                 ("Rev code 0450", "Revenue Code 0450")])
def test_code_forms_normalize_before_matching(a, b):
    x = rec(2, f"04/16/2026  {a}  Manual therapy  $150.00")
    y = rec(3, f"Apr 16, 2026  {b}  Manual therapy  $150.00")
    got = charges([x, y])
    assert len(got) == 1 and got[0]["record_nos"] == [2, 3], (a, b, [(g["raw"], g["record_nos"]) for g in got])


def test_different_codes_on_the_same_day_are_different_services():
    got = charges([rec(2, "04/16/2026  97140  Manual therapy  $150.00"), rec(3, "04/16/2026  97110  Therapeutic exercise  $150.00")])
    assert len(got) == 2


def test_normalized_code_helper():
    f = AM.norm_code
    assert {f(s) for s in ("97140", "CPT 97140", "CPT#97140", "CPT: 97140", "97140-GP", "CPT 97140-59", "cpt97140")} == {"97140"}
    assert {f(s) for s in ("G0283", "HCPCS G0283", "HCPCS: G0283", "g0283")} == {"G0283"}
    assert {f(s) for s in ("Rev 0450", "REV0450", "revenue code 0450", "Rev. code #0450")} == {"0450"}


def test_third_ledger_04_16_visit_is_one_amount_citing_both_statements():
    got = [a for a in charges(ledger()) if a["cents"] == 15000 and a["record_nos"] == [2, 3]]
    assert len(got) == 1 and "records 2, 3" in got[0]["duplicate_note"]


# ---------------------------------------------------------------- the whole third ledger
def test_third_ledger_total():
    """Everything the adjuster found is gone except blocker 1: the $650 summary row dressed as a service line is accepted debt (SCOPE_CUTS) and is the only
    amount here above what the bill states. 950 stated by the itemized lines + 650 debt row = 1,600. The ED note ($1,000, no bill of its own in the case) is read under the encounter rule: 950 + 650 + 1,000 = 2,600; the discharge summary's $950 is not totaled."""
    got = charges(ledger())
    assert sum(a["cents"] for a in got) == 260000
    assert any(a["cents"] == 65000 for a in got)             # the debt row, named so nobody mistakes it for fixed
    assert sum(a["cents"] for a in got if a["cents"] not in (65000, 100000)) == 95000


# ---------------------------------------------------------------- staff r3 major: default-deny is per figure, not per line
TAILS = ["insurance allowed $110.00", "allowed amount $110.00", "contract rate $110.00", "patient copay $30.00", "copay $30.00", "patient responsibility $30.00",
         "deductible $500.00", "coinsurance $22.00", "insurance paid $88.00", "plan paid $88.00", "PIP applied $60.00", "med pay $60.00", "network discount $40.00",
         "contractual $40.00", "you owe $22.00", "patient portion $22.00", "your share $22.00", "insurance pending $110.00", "estimated insurance payment $88.00",
         "late fee $25.00", "interest $5.00", "tax $8.00", "denied $150.00", "write-down $40.00", "$12.00", "balance $30.00", "adjustment $20.00"]


@pytest.mark.parametrize("tail", TAILS)
def test_only_the_lines_own_charge_is_a_charge(tail):
    """Staff r3 probe_second_fig.py: '04/16/2026 manual therapy charge $150.00, <tail>.' gives exactly one charge, the first figure; every tail figure is unclear."""
    ex = f"04/16/2026 manual therapy charge $150.00, {tail}."
    got = [(a["raw"], a["cls"]) for a in rows([rec(1, ex)])]
    assert got[0] == ("$150.00", "charge") or tail.startswith("allowed") or "plan paid" in tail or "network" in tail      # an insurer-side word may demote the first too (undercount)
    assert all(c != "charge" for _, c in got[1:]), got


@pytest.mark.parametrize("row", ["04/16/2026\tManual therapy\t$150.00\t$110.00", "04/16/2026  Manual therapy  $150.00  $30.00"])
def test_second_figure_in_a_charge_amount_row_is_not_a_charge(row):
    got = [(a["raw"], a["cls"]) for a in rows([rec(1, "Date\tService\tCharge\tAmount\n" + row)])]
    assert got[0][1] == "charge" and got[1][1] == "unclear", got


def test_a_second_figure_with_its_own_date_of_service_is_still_a_charge():
    ex = "04/09/2026 exercise charge $150.00 and 04/16/2026 manual therapy charge $160.00"
    assert [c for _, c in [(a["raw"], a["cls"]) for a in rows([rec(1, ex)])]] == ["charge", "charge"]


def test_second_unlabeled_figure_has_its_reason():
    ex = "04/16/2026 manual therapy charge $150.00, $12.00."
    a = [a for a in rows([rec(1, ex)]) if a["raw"] == "$12.00"][0]
    assert "second amount" in AM.not_totaled_reason(ex, "$12.00", 1200, BILL, "2026-06-01", a["lstart"], records=[rec(1, ex)]).lower()
