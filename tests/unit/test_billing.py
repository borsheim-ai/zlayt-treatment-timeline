"""Billing analysis (T-083, T-103, D-042, D-052): code-only, every figure cited, nothing totaled or compared. SYNTHETIC ledgers from research/record-formats.md."""
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import billing as B
from app.backend import pipeline as PL
from app.backend.api import create_app
from app.db import db as DB

LEDGER = """SYNTHETIC RECORD
Larkspur Hollow Physical Therapy (SYNTHETIC)     ITEMIZED STATEMENT     Statement date: 07/31/2026
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Acct: SYN-PT-2207   Financial class: LOP
DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE
05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00
06/10/26  06/11/26  97110  Therapeutic exercise x2       130.00                         340.00
06/10/26  06/11/26  97140  Manual therapy x1              70.00                         410.00
06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00
06/10/26  06/30/26  97140  Manual therapy x1 VOID        (70.00)                        375.00
06/10/26  06/30/26  97140  Manual therapy x1              70.00                         445.00
07/15/26  07/15/26  ADJ    Courtesy discount                                 45.00-     400.00
                     TOTAL CHARGES 445.00  TOTAL PMTS 0.00  TOTAL ADJ (45.00)  BALANCE DUE 400.00
Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection."""

EOB = """SYNTHETIC RECORD - THIS IS NOT A BILL
Quoinmere Mutual Health Plan (SYNTHETIC)   Explanation of Benefits   Processed 07/22/2026
Member: Delphine Okonkwo-Vale (SYNTHETIC)  ID SYN-MBR-88231  Claim SYN-CLM-0091
Provider: Larkspur Hollow Physical Therapy (SYNTHETIC)
DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES
06/10/26  97110    130.00    52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45
06/10/26  97140     70.00    28.00     42.00    22.00    4.00    16.00      26.00     PR-1, PR-2, CO-45
06/10/26  97014     35.00    35.00      0.00     0.00    0.00     0.00       0.00     CO-97
TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00
CO-97: payment included in allowance for another service."""

CMS_CLEAN = """SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS
24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI
    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060326   060326   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060126   060326   11     97014              A      90 | 00       3      SYN-NPI-0001
    060126   060326   11     97010              A      45 | 00       3      SYN-NPI-0001
25. FED TAX ID  SYN-TIN-0001     28. TOTAL CHARGE  390 | 00     29. AMOUNT PAID  0 | 00
33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142"""

CMS_OCR = """SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS
24. 060126 060126 11 98941 AB 8500 1 SYN-NPI-0001
    060226 060226 11 98941 AB 85 00 1 SYN-NPI-0001
    O60326 060326 11 98941 AB 85|00 1 SYN-NPI-0001
    060126 060326 11 97014 A 9000 3 SYN-NPI-0001
    060126 060326 11 97010 A 45 OO 3 SYN-NPI-0001
28. TOTAL CHARGE 39000   29. AMOUNT PAID 0 00"""

UB_ROOM = """SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
1 Saltmarrow General Hospital (SYNTHETIC)   3a SYN-PCN-7730  3b SYN-IP-11902  4 0111
42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00
0450    EMERGENCY ROOM                               091526        1          1,975.00
0250    PHARMACY                                     091526       14            412.75
0300    LABORATORY                                   091526        6            688.00
0320    DX X-RAY                                     091526        2            540.00
0001    TOTAL                                        092226                   9,165.75
67 S42.201A   76 ATTENDING Dr. Rosamund Achterberg (SYNTHETIC)"""

PROSE = ("Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; "
         "total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.")

LOP = ("Letter of protection to Fennimoor Spine Clinic. The client's current balance is $4,860.00. Provider agrees to accept $3,100.00 in full satisfaction "
       "of the account. Please send an itemized statement.")


def rec(n, source, text, **kw):
    return {"n": n, "source": source, "excerpt": text, "text": text, **kw}


_GONE = {"payer_reports", "matched_provider", "not_added_note", "complete", "balance_convention", "totals", "providers", "stated_totals", "stated_totals_repeated", "unreadable_providers",
         "stated_billed", "line_sum_billed", "line_flags", "negotiated_reductions", "balance_forwards"}


def one(records):
    """The analysis, with its citations verified and none of the removed total-shaped fields anywhere in it (D-052)."""
    out = B.analyze(records)
    assert B.verify_citations(out, records) == []
    assert set(out) == {"status", "lines", "unreconciled", "skipped_records", "rules"}
    assert not [k for d in B._walk(out) for k in d if k in _GONE]
    return out


def rows(out, name):
    """The parsed ledger / claim-form rows of a provider (a row has billed / paid / adjustment / balance; an extra line has `figure`)."""
    return [l for l in out["lines"] if l["provider"].startswith(name) and "figure" not in l]


def detail(out, d):
    return [l for l in out["lines"] if l["detail"] == d]


def rates(out):
    return [l for l in out["lines"] if l["class"] == "rate"]


def figs(out):
    return [f for u in out["unreconciled"] for f in u["figures"]]


def checks(out):
    return [c for l in out["lines"] for c in l.get("checks", [])]


def cents(l, k="billed"):
    return l[k]["cents"] if l.get(k) else None


# ------------------------------------------------------------------ itemized ledger
def test_ledger_lines_parse_to_four_figures_each_cited_and_classed():
    r = [rec(1, "Larkspur Hollow Physical Therapy (SYNTHETIC), itemized statement", LEDGER)]
    ls = rows(one(r), "Larkspur")
    assert [l["code"] for l in ls] == ["97162", "97110", "97140", "97014", "97140", "97140", "ADJ"]
    first = ls[0]
    assert (first["class"], cents(first), cents(first, "balance"), first["paid"], first["adjustment"]) == ("charge", 21000, 21000, None, None)
    assert first["dos"] == "05/27/26" and first["dos_iso"] == "2026-05-27" and first["posted"] == "05/28/26" and first["record_no"] == 1
    assert first["cites"] == [{"record_no": 1, "excerpt": first["excerpt"]}] and first["excerpt"] in LEDGER
    adj = ls[-1]
    assert adj["adjustment"]["cents"] == 4500 and adj["adjustment"]["text"] == "45.00-" and cents(adj, "balance") == 40000 and adj["class"] == "adjustment"


def test_no_per_provider_totals_no_complete_flag_no_balance_check_anywhere():
    """D-052: a listing, not a ledger reconciliation. Whatever the statement prints is a cited line; nothing is summed or compared with a sum."""
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Fennimoor Spine Clinic, itemized ledger", PROSE)])
    assert {l["provider"] for l in out["lines"]} == {"Larkspur Hollow Physical Therapy", "Fennimoor Spine Clinic"}
    assert {"LEDGER_TOTAL_MISMATCH", "LEDGER_BALANCE_MISMATCH", "CLAIM_TOTAL_MISMATCH", "CLAIM_LEDGER_BILLED_MISMATCH", "BALANCE_STEP_MISMATCH",
            "LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"}.isdisjoint(B.CHECKS)
    assert set(B.CHECKS) == {"LINE_UNCLEAR", "NO_DATE_OF_SERVICE", "ROW_NOT_PARSED"}      # nothing in billing sums or compares figures


def test_void_is_a_reversal_charge_line_and_the_running_balance_is_just_a_figure():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)])
    void = next(l for l in rows(out, "Larkspur") if "VOID" in l["description"])
    assert cents(void) == -7000 and void["class"] == "charge" and void["detail"] == "reversal"
    assert checks(out) == [] and [l["excerpt"] for l in rates(out)] != []


def test_fee_schedule_rate_is_a_rate_line_and_never_a_charge():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)])
    assert [(x["figure"]["cents"], x["class"], x["detail"]) for x in rates(out)] == [(6500, "rate", "rate")]
    assert "Fee schedule" in rates(out)[0]["excerpt"]
    assert 6500 not in [cents(l) for l in rows(out, "Larkspur")]


def test_a_printed_total_is_a_cited_line_beside_the_rows_not_compared_with_them():
    bad = LEDGER.replace("TOTAL CHARGES 445.00", "TOTAL CHARGES 455.00")
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", bad)])
    (t,) = detail(out, "stated_total_billed")
    assert t["class"] == "unclear" and t["figure"]["cents"] == 45500 and "TOTAL CHARGES 455.00" in t["excerpt"]
    assert [cents(l) for l in rows(out, "Larkspur")][:2] == [21000, 13000] and out["unreconciled"] == []      # the rows are as printed; no verdict on the total


def test_a_running_balance_that_does_not_follow_is_listed_as_printed_with_no_verdict():
    """D-052 (strict): no arithmetic on a line either. A balance that is not the previous balance plus the charge is a figure, not a flag."""
    bad = LEDGER.replace("410.00\n", "415.00\n", 1)
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", bad)])
    assert checks(out) == [] and "415.00" in {l["balance"]["text"] for l in rows(out, "Larkspur") if l["balance"]}


def test_unreadable_figure_is_listed_with_no_value():
    txt = LEDGER.replace("130.00    ", "13O.00    ", 1)
    bad = next(l for l in rows(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", txt)]), "Larkspur") if l["code"] == "97110")
    assert bad["billed"] is None and bad["unclear"] == ["13O.00"] and "LINE_UNCLEAR" in bad["checks"] and bad["class"] == "unclear"


def test_extra_decimals_are_never_rounded():
    txt = LEDGER.replace("130.00", "130.005")
    assert next(l for l in rows(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", txt)]), "Larkspur") if l["code"] == "97110")["billed"] is None


def test_a_re_sent_statement_is_two_sets_of_lines_one_per_record_never_merged():
    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Larkspur Hollow Physical Therapy, statement (copy)", LEDGER)]
    out = one(r)
    ls = rows(out, "Larkspur")
    assert len(ls) == 14 and all(len(l["record_nos"]) == 1 and l["record_nos"] == [l["record_no"]] and [c["record_no"] for c in l["cites"]] == l["record_nos"] for l in ls)
    assert [l["record_no"] for l in ls].count(1) == 7 and [l["record_no"] for l in ls].count(2) == 7
    assert sorted(t["record_nos"] for t in detail(out, "stated_total_billed")) == [[1], [2]] or not detail(out, "stated_total_billed")


def test_two_identical_lines_inside_one_record_are_both_listed():
    twice = LEDGER.replace("06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00",
                           "06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00\n"
                           "06/10/26  06/11/26  97014  E-stim unattended              35.00                         480.00")
    assert sum(1 for l in rows(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", twice)]), "Larkspur") if l["code"] == "97014") == 2


def test_balance_forward_is_a_cited_line_and_not_a_charge():
    txt = LEDGER.replace("05/27/26  05/28/26  97162", "Bal fwd                                                                          100.00\n05/27/26  05/28/26  97162", 1) \
                .replace("PT eval moderate complexity   210.00                         210.00", "PT eval moderate complexity   210.00                         310.00")
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", txt)])
    assert all("Bal" not in (l["description"] or "") for l in rows(out, "Larkspur"))
    (f,) = detail(out, "balance_forward")
    assert f["figure"]["cents"] == 10000 and f["class"] == "unclear" and "Bal fwd" in f["excerpt"]


def test_payments_adjustments_in_their_own_columns_by_position():
    txt = """DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE
03/01/26  03/02/26  99213  Office visit                  150.00                         150.00
03/15/26  03/15/26  PMT    Ins pmt - Ck #SYN-1043                    100.00             50.00
03/15/26  03/15/26  CO45   Contractual adj                                   20.00-      30.00
04/20/26  04/20/26  ATY    Atty reduction                                    10.00-      20.00
                     TOTAL CHARGES 150.00  TOTAL PMTS 100.00  TOTAL ADJ (30.00)  BALANCE DUE 20.00"""
    ls = rows(one([rec(1, "Medlark Clinic, statement", txt)]), "Medlark")
    assert [(l["class"], cents(l, {"charge": "billed", "payment": "paid", "adjustment": "adjustment"}[l["class"]])) for l in ls] == \
        [("charge", 15000), ("payment", 10000), ("adjustment", 2000), ("adjustment", 1000)]
    assert [l["negotiated"] for l in ls] == [False, False, False, True]


def test_ledger_prose_statement_lists_charges_payment_adjustment_and_its_printed_figures():
    out = one([rec(9, "Fennimoor Spine Clinic, itemized ledger", PROSE)])
    ls = rows(out, "Fennimoor")
    assert [(l["class"], cents(l)) for l in ls if l["class"] == "charge"] == [("charge", 25000), ("charge", 18000), ("charge", 231000)]
    assert [cents(l, "paid") for l in ls if l["class"] == "payment"] == [30000] and [cents(l, "adjustment") for l in ls if l["class"] == "adjustment"] == [27400]
    assert detail(out, "stated_total_billed")[0]["figure"]["cents"] == 274000 and detail(out, "stated_total_balance")[0]["figure"]["cents"] == 216600
    assert [l for l in out["lines"] if l["detail"] in ("lien_amount", "asserted_balance", "reduction")] == []      # "held under letter of protection" has no amount


def test_nothing_found_for_a_clinical_record():
    out = one([rec(1, "Dr. Lee, progress note", "Neck pain 5/10 after the collision. Plan: continue therapy.")])
    assert out["status"] == "none_found" and out["lines"] == [] and out["unreconciled"] == [] and out["skipped_records"] == []


# ------------------------------------------------------------------ LOP / lien amounts are listed apart
def test_lop_and_lien_amounts_are_unclear_lines_apart_from_the_charges():
    out = one([rec(1, "Fennimoor Spine Clinic, itemized ledger", PROSE), rec(2, "Pellingham and Rook PLLC, correspondence (letter of protection)", LOP)])
    lop = [l for l in out["lines"] if l["record_no"] == 2]
    assert [(x["figure"]["cents"], x["detail"], x["class"]) for x in lop] == [(486000, "asserted_balance", "unclear"), (310000, "reduction", "unclear")]
    assert [cents(l) for l in rows(out, "Fennimoor") if l["class"] == "charge"] == [25000, 18000, 231000]


def test_atty_reduction_on_a_ledger_is_listed_as_an_lop_amount():
    txt = "Itemized ledger. Therapy charge $1,000.00. Balance reduced to $600.00 in full satisfaction. Balance due $1,000.00."
    out = one([rec(1, "Medlark Clinic, itemized ledger", txt)])
    assert [x["figure"]["cents"] for x in out["lines"] if x["detail"] == "reduction"] == [60000]
    assert [cents(l) for l in rows(out, "Medlark")] == [100000]


# ------------------------------------------------------------------ CMS-1500 (implied decimals), UB-04 (rate on the charge line), EOB
def test_cms1500_boxes_are_implied_cents_and_item_28_is_a_listed_total():
    out = one([rec(1, "Brightwater Spine & Wellness, CMS-1500", CMS_CLEAN)])
    assert [cents(l) for l in rows(out, "Brightwater")] == [8500, 8500, 8500, 9000, 4500] and {l["form"] for l in out["lines"]} == {"cms1500"}
    assert detail(out, "stated_total_billed")[0]["figure"]["cents"] == 39000 and detail(out, "stated_total_paid")[0]["figure"]["cents"] == 0


def test_cms1500_ocr_text_never_reads_8500_as_dollars():
    out = one([rec(1, "Brightwater Spine & Wellness, CMS-1500 (OCR)", CMS_OCR)])
    ls = rows(out, "Brightwater")
    c = [cents(l) for l in ls]
    assert c[:2] == [8500, 8500] and c[3] == 9000                  # 8500 -> $85.00, 9000 -> $90.00
    assert c[4] is None and "45 OO" in ls[4]["unclear"]            # OCR letters: listed with no value
    assert c[2] == 8500                                            # O in the date does not matter
    assert detail(out, "stated_total_billed")[0]["figure"]["cents"] == 39000


def test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total():
    out = one([rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM)])
    ls = rows(out, "Saltmarrow")
    assert [cents(l) for l in ls] == [197500, 41275, 68800, 54000]            # T-103 r4: the room row's FL 47 total is not a line of its own ...
    assert [(x["figure"]["cents"], x["detail"]) for x in rates(out)] == [(185000, "rate")]
    assert [(f["text"], f["cents"]) for f in rates(out)[0]["other_figures"]] == [("5,550.00", 555000)]       # ... it is the FL 44 rate entry's other figure, listed once
    assert all(l["code"] != "0001" for l in ls) and detail(out, "stated_total_billed")[0]["figure"]["cents"] == 916575


def test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)])
    eob = [l for l in out["lines"] if l["form"] == "eob"]
    assert [(l["code"], l["class"], l["detail"], l["record_no"]) for l in eob] == [("97110", "unclear", "eob", 2), ("97140", "unclear", "eob", 2), ("97014", "unclear", "eob", 2)]
    l140 = next(l for l in eob if l["code"] == "97140")
    assert l140["eob"]["plan_paid"]["cents"] == 1600 and l140["eob"]["billed"]["cents"] == 7000 and l140["eob_codes"] == "PR-1, PR-2, CO-45"
    assert l140["billed"] is None and l140["paid"] is None and l140["checks"] == [] and l140["excerpt"] in EOB     # an EOB row is never a charge or a payment
    assert [cents(l) for l in rows(out, "Larkspur") if l["form"] == "ledger"][:2] == [21000, 13000]
    assert checks(out) == []            # the ledger shows no payment for 97140 and the EOB $16.00; nothing is compared, so nothing is raised
    assert B.CHECKS.keys().isdisjoint({"LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"})


def test_claim_form_and_ledger_for_one_provider_are_both_listed_each_with_its_form():
    r = [rec(1, "Brightwater Spine & Wellness, itemized ledger", "Itemized ledger, statement date 07/01/2026. Care charge $390.00. Total charges $390.00. Balance due $390.00."),
         rec(2, "Brightwater Spine & Wellness, CMS-1500", CMS_CLEAN)]
    ls = rows(one(r), "Brightwater")
    assert [(l["form"], cents(l)) for l in ls] == [("ledger", 39000)] + [("cms1500", c) for c in (8500, 8500, 8500, 9000, 4500)]


# ------------------------------------------------------------------ citations, API
def test_verify_citations_catches_an_uncited_line():
    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)]
    out = B.analyze(r)
    out["lines"][0]["cites"][0]["excerpt"] = "not in the record"
    assert B.verify_citations(out, r)[0]["reason"] == "excerpt_not_verbatim"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    return TestClient(create_app(str(tmp_path / "x.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 5000))


def _seed(client, text):
    conn = DB.connect(client.app.state.db_path)             # demo mode refuses unrecorded text over HTTP, so the case is seeded directly (code-only ingest)
    tok = DB.create_case(conn, text, now=time.time())
    PL.ingest_case(conn, tok, text, time.time())
    return conn, tok


def test_billing_route_returns_the_listing(client):
    text = ("=== Record 1 ===\nDate: 2026-06-15\nSource: Fennimoor Spine Clinic, itemized ledger\nExcerpt: \"" + PROSE + "\"\n\n"
            "=== Record 2 ===\nDate: 2026-03-26\nSource: Pellingham and Rook PLLC, correspondence (letter of protection)\nExcerpt: \"" + LOP + "\"\n")
    conn, tok = _seed(client, text)
    conn.close()
    r = client.get(f"/api/cases/{tok}/billing")
    assert r.status_code == 200
    b = r.json()["billing"]
    assert set(b) == {"status", "lines", "unreconciled", "skipped_records", "rules", "citation_failures"} and b["status"] == "listed"
    assert [cents(l) for l in b["lines"] if l["class"] == "charge"] == [25000, 18000, 231000]
    assert [x["figure"]["cents"] for x in b["lines"] if x["detail"] in ("asserted_balance", "reduction")] == [486000, 310000]
    assert client.get("/api/cases/nope/billing").status_code == 404


def test_table_survives_ingest_with_the_quote_on_its_own_line_or_the_first_line(client):
    from app.backend import store
    body = LEDGER.split("\n", 3)[3]
    for quoted in ('Excerpt: "' + body + '"', 'Excerpt: "\n' + body + '\n"'):
        text = "=== Record 1 ===\nDate: 2026-07-31\nSource: Larkspur Hollow Physical Therapy, itemized statement\n" + quoted + "\n"
        conn, tok = _seed(client, text)
        out = B.for_case(conn, tok)
        assert B.verify_citations(out, store.load_records(conn, tok)) == []
        conn.close()
        assert len(rows(out, "Larkspur")) == 7 and out["unreconciled"] == [] and out["citation_failures"] == []


def test_prose_charges_without_a_date_of_service_are_listed_and_flagged():
    out = one([rec(9, "Fennimoor Spine Clinic, itemized ledger", PROSE)])
    assert set(checks(out)) == {"NO_DATE_OF_SERVICE"}


def test_injection_tagged_record_is_skipped_not_listed():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER, injection_tag=True)])
    assert out["lines"] == [] and out["skipped_records"] == [{"record_no": 1, "reason_code": "INJECTION_SUSPECTED"}] and out["status"] == "listed"


def test_duplicate_records_are_ignored_and_no_model_is_imported():
    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER, duplicate_of=1)]
    assert rows(one(r), "Larkspur")[0]["record_nos"] == [1]
    import app.backend.billing as mod, inspect
    assert "app.llm" not in inspect.getsource(mod) and "call(" not in inspect.getsource(mod)


# ================================================================== rates, rows that do not fit, unknown layouts
HEAD_TXT = "DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE"


def tbl(header, rows_, footer=""):
    """A fixed-width ledger: text columns left-aligned under their header word, money columns right-aligned to the end of theirs."""
    import re as _re
    spans = {m.group(0): (m.start(), m.end()) for m in _re.finditer(r"\S+", header)}
    out = [header]
    for r_ in rows_:
        buf = [" "] * 130
        for name, text in r_.items():
            s, e = spans[name]
            start = s if name in ("DOS", "POSTED", "CODE", "DESCRIPTION") else e - len(text)
            buf[start:start + len(text)] = text
        out.append("".join(buf).rstrip())
    return "\n".join(out) + ("\n" + footer if footer else "")


def row(dos, posted, code, desc, charges=None, balance=None, **kw):
    r_ = {"DOS": dos, "POSTED": posted, "CODE": code, "DESCRIPTION": desc}
    if charges:
        r_["CHARGES"] = charges
    if balance:
        r_["BALANCE"] = balance
    r_.update(kw)
    return {k: v for k, v in r_.items() if v}


PT = "Medlark Clinic, itemized statement"


@pytest.mark.parametrize("fig", ["185.00", "$185.00"])
def test_table_row_charge_per_visit_is_a_rate_line_listed_once(fig):
    t = tbl(HEAD_TXT, [row("06/10/26", "06/11/26", "99202", "New patient exam", "130.00", "130.00"),
                       row("06/10/26", "06/11/26", "99213", "Charge per visit", fig, "315.00")],
            "          TOTAL CHARGES 130.00  BALANCE DUE 130.00")
    out = one([rec(1, PT, t)])
    assert [l["code"] for l in rows(out, "Medlark")] == ["99202"]
    assert [(x["figure"]["cents"], x["class"]) for x in rates(out)] == [(18500, "rate")] and "Charge per visit" in rates(out)[0]["excerpt"]      # once, never also a charge


@pytest.mark.parametrize("desc", ["Visit fee per session", "Rate each", "Hourly rate", "Charge /visit", "Daily rate"])
def test_every_rate_cue_in_a_table_row_wins_even_beside_charge(desc):
    t = tbl(HEAD_TXT, [row("06/10/26", "06/11/26", "99202", "New patient exam", "130.00", "130.00"), row("06/10/26", "06/11/26", "99213", desc, "185.00", "315.00")],
            "          TOTAL CHARGES 130.00  BALANCE DUE 130.00")
    out = one([rec(1, PT, t)])
    assert [l["code"] for l in rows(out, "Medlark")] == ["99202"] and [x["figure"]["cents"] for x in rates(out)] == [18500]


def test_unit_notation_x1_is_still_a_normal_charge_in_a_table_row():
    t = tbl(HEAD_TXT, [row("06/10/26", "06/11/26", "97140", "Manual therapy x1", "70.00", "70.00")], "          TOTAL CHARGES 70.00  BALANCE DUE 70.00")
    assert [cents(l) for l in rows(one([rec(1, PT, t)]), "Medlark")] == [7000]


PROSE_RATES = ["Charge per visit $185.00.", "Billed $150.00 per visit.", "Each session charge $95.00.", "Treatment charge $65.00 x 14.", "Daily rate charge $90.00."]


@pytest.mark.parametrize("sent", PROSE_RATES)
def test_prose_rate_cue_beats_the_word_charge(sent):
    txt = f"Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. {sent} Total charges $250.00. Balance due $250.00."
    out = one([rec(1, PT, txt)])
    assert [cents(l) for l in rows(out, "Medlark")] == [25000]
    assert len(rates(out)) == 1 and rates(out)[0]["detail"] == "rate" and sent.rstrip(".") in rates(out)[0]["excerpt"]


def test_prose_rate_is_a_rate_even_when_the_printed_total_includes_it():
    """The statement's own total was written to include the rate: the rate is still a rate line, and the total is listed as printed."""
    txt = "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Charge per visit $185.00. Total charges $435.00. Balance due $435.00."
    out = one([rec(1, PT, txt)])
    assert [cents(l) for l in rows(out, "Medlark")] == [25000] and [x["figure"]["cents"] for x in rates(out)] == [18500]
    assert detail(out, "stated_total_billed")[0]["figure"]["cents"] == 43500


def test_one_rate_cue_function_is_shared_with_reclassify():
    from app.backend import amounts as A, reclassify
    assert reclassify._RATE_CUE is A.RATE_CUE
    assert A.has_rate_cue("Charge per visit $185") and A.has_rate_cue("Billed $150 per visit") and A.has_rate_cue("charge $65 x 14")
    assert not A.has_rate_cue("Manual therapy x1", unit_notation=True) and A.has_rate_cue("Manual therapy x1")
    assert not A.has_rate_cue("New patient exam charge $250.00")


def test_rate_column_figures_are_listed_as_rates():
    head = "DOS       POSTED    CODE   DESCRIPTION            RATE      CHARGES   PAYMENTS   ADJ        BALANCE"
    t = tbl(head, [row("06/10/26", "06/11/26", "97110", "Ther exercise x2", "130.00", "130.00", RATE="65.00")], "          TOTAL CHARGES 130.00  BALANCE DUE 130.00")
    out = one([rec(1, PT, t)])
    assert [cents(l) for l in rows(out, "Medlark")] == [13000] and [(x["figure"]["cents"], x["class"]) for x in rates(out)] == [(6500, "rate")]


CMS_NO_28 = """SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS
24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI
    060126   060126   11     98941              AB     85.00         1      SYN-NPI-0001
    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060326   060326   11     97014              A      90 | 00       3      SYN-NPI-0001
33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142"""


def test_cms1500_printed_decimal_is_read_not_dropped():
    out = one([rec(1, "Brightwater Spine & Wellness, CMS-1500", CMS_NO_28)])
    assert [cents(l) for l in rows(out, "Brightwater")] == [8500, 8500, 9000] and out["unreconciled"] == []


def test_cms1500_slash_dated_line_is_read():
    ls = rows(one([rec(1, "Brightwater Spine & Wellness, CMS-1500", CMS_NO_28.replace("060126   060126", "06/01/26 06/01/26"))]), "Brightwater")
    assert [cents(l) for l in ls] == [8500, 8500, 9000] and ls[0]["dos"] == "06/01/26"


def test_cms1500_line_that_does_not_fit_is_unreconciled_with_its_excerpt():
    txt = CMS_NO_28.replace("85.00         1", "$85.00        1") + "\n28. TOTAL CHARGE  260 | 00     29. AMOUNT PAID  0 | 00"
    out = one([rec(1, "Brightwater Spine & Wellness, CMS-1500", txt)])
    assert [cents(l) for l in rows(out, "Brightwater")] == [8500, 9000] and out["status"] == "listed"
    (u,) = out["unreconciled"]
    assert u["reason_code"] == "ROW_NOT_PARSED" and u["class"] == "unclear" and u["excerpt"] in txt and "$85.00" in u["figures"][0] and u["record_no"] == 1
    assert detail(out, "stated_total_billed")[0]["figure"]["cents"] == 26000          # the printed total is a line too; nothing is added to it


def test_ledger_row_with_no_date_is_unreconciled_and_its_total_is_a_line():
    t = tbl(HEAD_TXT, [row("06/10/26", "06/11/26", "97110", "Therapeutic exercise x2", "130.00", "130.00"),
                       row("", "", "97014", "E-stim unattended", "35.00", "165.00")],
            "          TOTAL CHARGES 165.00  BALANCE DUE 165.00")
    out = one([rec(1, PT, t)])
    assert [cents(l) for l in rows(out, "Medlark")] == [13000]
    (u,) = out["unreconciled"]
    assert "E-stim unattended" in u["excerpt"] and u["figures"] == ["35.00", "165.00"]
    assert detail(out, "stated_total_billed")[0]["figure"]["cents"] == 16500


def test_a_fee_schedule_line_is_a_rate_not_an_unreconciled_row():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)])
    assert out["unreconciled"] == [] and len(rates(out)) == 1


def test_blank_dos_cell_does_not_take_the_posted_date():
    t = tbl(HEAD_TXT, [row("", "06/11/26", "97014", "E-stim unattended", "35.00", "35.00")], "          TOTAL CHARGES 35.00  BALANCE DUE 35.00")
    (l,) = rows(one([rec(1, PT, t)]), "Medlark")
    assert l["dos"] is None and l["dos_iso"] is None and l["posted"] == "06/11/26" and "NO_DATE_OF_SERVICE" in l["checks"] and cents(l) == 3500


AMBULANCE = """SYNTHETIC RECORD - AMBULANCE INVOICE - ALL IDENTIFIERS FICTITIOUS
Fernhollow County EMS Billing (SYNTHETIC)   TIN SYN-TIN-0440   Invoice SYN-INV-77310   Invoice date 05/29/2026
CODE      DESCRIPTION                          UNITS   RATE       CHARGE
A0427-SH  ALS emergency transport, Level 1      1      1,450.00   1,450.00
A0425-SH  Ground mileage, loaded                8.7       22.50     195.75
                                          TOTAL CHARGES          1,645.75
PAYMENTS 0.00   ADJUSTMENTS 0.00   BALANCE DUE 1,645.75"""


def test_a_bill_in_an_unrecognised_layout_is_skipped_visibly_not_none_found():
    out = one([rec(1, "Fernhollow County EMS Billing, ambulance invoice", AMBULANCE)])
    assert out["skipped_records"] == [{"record_no": 1, "reason_code": "UNRECOGNISED_BILLING_FORM"}] and out["status"] == "listed" and out["lines"] == []


def test_a_clinical_note_with_a_dollar_amount_is_not_flagged_unrecognised():
    out = one([rec(1, "Dr. Lee, progress note", "Patient reports paying $40.00 copay at the front desk.")])
    assert out["skipped_records"] == [] and out["status"] == "none_found"


def test_an_unreadable_provider_does_not_touch_another_providers_lines():
    t = tbl(HEAD_TXT, [row("06/10/26", "06/11/26", "97110", "Therapeutic exercise x2", "13O.00", "130.00")])
    out = one([rec(1, PT, t), rec(2, "Fennimoor Spine Clinic, itemized ledger", PROSE)])
    assert rows(out, "Medlark")[0]["billed"] is None and rows(out, "Medlark")[0]["unclear"] == ["13O.00"]
    assert [cents(l) for l in rows(out, "Fennimoor") if l["class"] == "charge"] == [25000, 18000, 231000]


# ------------------------------------------------------------------ the grounding verifier can fail on real output, and the API runs it
def test_verifier_reference_is_the_record_text_not_the_excerpt():
    r = [{"n": 1, "source": "Larkspur Hollow Physical Therapy, itemized statement", "excerpt": LEDGER, "text": "A"}]
    out = B.analyze(r)
    assert out["lines"] and B.verify_citations(out, r) != []                       # the excerpt is not in the record's own text
    ok = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)]
    assert B.verify_citations(B.analyze(ok), ok) == []


def test_verifier_covers_every_cite_bearing_field():
    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB),
         rec(3, "Medlark Clinic, itemized statement", "Itemized ledger, statement date 06/15/2026. Office visit $250.00. Total charges $250.00. Balance due $250.00.")]

    def broken(fn):
        out = B.analyze(r)
        fn(out)
        return B.verify_citations(out, r)
    pick = lambda o, d: next(l for l in o["lines"] if l["detail"] == d)
    assert broken(lambda o: pick(o, "eob").update(excerpt="made up")) != []
    assert broken(lambda o: pick(o, "eob")["eob"]["plan_paid"].update(text="999.99")) != []          # an EOB figure must sit inside its own row
    assert broken(lambda o: pick(o, "stated_total_billed").update(excerpt="made up")) != []
    assert broken(lambda o: pick(o, "stated_total_billed")["figure"].update(text="999.99")) != []          # a printed total must sit inside its own cite
    assert broken(lambda o: pick(o, "rate").update(excerpt="made up")) != []
    assert broken(lambda o: o["unreconciled"][0].update(excerpt="made up")) != []
    assert broken(lambda o: o["lines"][0]["billed"].update(text="999.99")) != []
    assert broken(lambda o: None) == []


def test_billing_route_returns_citation_failures_and_flags_the_status(client, monkeypatch):
    text = "=== Record 1 ===\nDate: 2026-06-15\nSource: Fennimoor Spine Clinic, itemized ledger\nExcerpt: \"" + PROSE + "\"\n"
    conn, tok = _seed(client, text)
    conn.close()
    clean = client.get(f"/api/cases/{tok}/billing").json()["billing"]
    assert clean["citation_failures"] == [] and clean["status"] == "listed"
    real = B.analyze

    def tampered(records):
        out = real(records)
        out["lines"][0]["cites"][0]["excerpt"] = "not in the record"
        return out
    monkeypatch.setattr(B, "analyze", tampered)
    bad = client.get(f"/api/cases/{tok}/billing").json()["billing"]
    assert bad["status"] == "citation_failed" and bad["citation_failures"][0]["reason"] == "excerpt_not_verbatim"


# ------------------------------------------------------------------ the oracle: no money-shaped token is silently missing
# Every '$' / decimal / boxed amount token a billing record prints must sit in a row the output shows: a listed line (parsed, rate, estimate, LOP,
# printed total, balance forward), an unreconciled row, or on its row as an unclear figure; or the whole record is in skipped_records.
import random
import re

_TOKEN = re.compile(r"\$\s?[\dOolISB][\dOolISB,]*(?:\.[\dOolISB]+)?|(?<![\w/.$])[\dO][\dO,]*\.[\dO]{2}(?!\w|\.\d)|(?<![\w/.])\d+\s*\|\s*\d\d\b")


def _nt(t):
    return re.sub(r"[$()\s-]", "", t or "")


def _items(out):
    """(excerpt, figure texts, False): every place the analysis shows a printed row. No row stands for "its whole text": a rate or LOP entry claims its
    own figure and its `other_figures` (a running balance on a price row), nothing else (T-103 r3)."""
    items = []
    for l in out["lines"]:
        if "figure" in l:
            items.append((l["excerpt"], {_nt(l["figure"]["text"])} | {_nt(f["text"]) for f in l["other_figures"]}, False))
        else:
            items.append((l["excerpt"], {_nt(l[k]["text"]) for k in ("billed", "paid", "adjustment", "balance") if l.get(k) and l[k]["cents"] is not None} | {_nt(t) for t in l["unclear"]}
                          | {_nt(f["text"]) for f in (l.get("eob") or {}).values() if f["cents"] is not None}, False))      # an EOB row claims only the figures it lists
    items += [(u["excerpt"], {_nt(f) for f in u["figures"]}, False) for u in out["unreconciled"]]
    return items


def unaccounted(records, out, bare=()):
    """The tokens printed in the input that no row of the output carries. `bare` names whole-number texts that are money in this input; each
    digit-bounded occurrence outside a longer token is counted as a token too. A figure whose cents is None counts only when it sits in `unclear`
    (a parsed slot with no value is not a placement). A record in skipped_records is accounted for as a whole."""
    items, missing, skipped = _items(out), [], {s["record_no"] for s in out["skipped_records"]}
    for r in records:
        if r["n"] in skipped:
            continue
        body = r["excerpt"]
        for s, e in B._segments(body):
            unit = body[s:e].strip()
            toks = list(_TOKEN.finditer(unit))
            for b in bare:
                toks += [m for m in re.finditer(r"(?<![\w/.,$])" + re.escape(b) + r"(?![\w/]|[.,]\d)", unit) if not any(m.start() < t.end() and t.start() < m.end() for t in toks)]
            for t in toks:
                hit = [(texts, whole) for ex, texts, whole in items if unit in ex or (ex in unit and t.group(0) in ex)]
                if not any(whole or _nt(t.group(0)) in texts for texts, whole in hit):
                    missing.append((t.group(0), unit))
    return missing


def cms(*lines, total=None):
    head = ("SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS\n"
            "24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI\n")
    return head + "\n".join(lines) + ("\n" + total if total else "") + "\n33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142"


CMS_SRC = "Brightwater Spine & Wellness, CMS-1500"
CMS_OK = "    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001"


def _ledger(*rows_, footer="          TOTAL CHARGES 130.00  BALANCE DUE 130.00"):
    return tbl(HEAD_TXT, [row("06/10/26", "06/11/26", "99202", "New patient exam", "130.00", "130.00"), *rows_], footer)


def _prose(*sentences, total="Total charges $250.00. Balance due $250.00."):
    return "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. " + " ".join(sentences) + " " + total


TOTALS_ROW = "TOTAL" + " " * 52 + "130.00" + " " * 26 + "130.00"          # right-aligned under CHARGES (ends col 63) and BALANCE (ends col 95)


def _fwd(*fwd_rows):
    t = tbl(HEAD_TXT, [row("06/10/26", "06/11/26", "97110", "Therapeutic exercise", "130.00", "230.00")], "          TOTAL CHARGES 130.00  BALANCE DUE 230.00")
    head, rest = t.split("\n", 1)
    return head + "\n" + "\n".join("          " + r_ for r_ in fwd_rows) + "\n" + rest


def _stmt(code, desc, charges, total, dos="06/01/26"):
    return tbl(HEAD_TXT, [row(dos, "06/02/26", code, desc, charges)], f"          TOTAL CHARGES {total}  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE {total}")


EOB_SRC = "Quoinmere Mutual Health Plan, explanation of benefits"
_EOB_HEAD = EOB.split("\n")[:5]
_EOB_COLS = "DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES"
_EOB_TAIL = "CO-97: payment included in allowance for another service."


def eob_text(*service_rows, total="TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00"):
    """The sample EOB with the given service rows (a row is DOS, service, then the seven figure texts, then codes)."""
    return "\n".join([*_EOB_HEAD[:4], _EOB_COLS, *service_rows, *([total] if total else []), _EOB_TAIL])


def eob_row(billed="130.00", plan_paid="16.00", service="97110", codes="PR-1, CO-45", discount="52.00", allowed="78.00", deduct="22.00", coins="4.00", owes="26.00"):
    return f"06/10/26  {service:<7} {billed:>7}   {discount:>7}   {allowed:>7}  {deduct:>7} {coins:>6}   {plan_paid:>8}   {owes:>9}     {codes}"


# the T-083 probe sets (r1 to r5 reviews, artifacts/review-evidence/T-083-*): each is run through the oracle
PROBES = {
    "sample_ledger": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)],
    "prose": [rec(1, "Fennimoor Spine Clinic, itemized ledger", PROSE)],
    "cms_clean": [rec(1, CMS_SRC, CMS_CLEAN)],
    "cms_no_28": [rec(1, CMS_SRC, CMS_NO_28)],
    "cms_printed_dollar": [rec(1, CMS_SRC, CMS_NO_28.replace("85.00         1", "$85.00        1") + "\n28. TOTAL CHARGE  260 | 00")],
    "cms_no_dates": [rec(1, CMS_SRC, cms(CMS_OK, "    11     98941              AB     85.00         1      SYN-NPI-0001"))],
    "cms_no_units": [rec(1, CMS_SRC, cms(CMS_OK, "    060226   060226   11     98941              AB     85.00      SYN-NPI-0001", total="28. TOTAL CHARGE  170 | 00     29. AMOUNT PAID  0 | 00"))],
    "cms_unreadable_total": [rec(1, CMS_SRC, cms(CMS_OK, total="28. TOTAL CHARGE  1O0 | 00     29. AMOUNT PAID  0 | 00"))],
    "ub04": [rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM)],
    "ub04_stray_figure": [rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM.replace("67 S42.201A", "   SURCHARGE NOTE        125.00\n67 S42.201A"))],
    "lop": [rec(1, "Letter of protection to Fennimoor Spine Clinic", LOP)],
    "table_dollar_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "$185", "315.00"), footer="          TOTAL CHARGES 315.00  BALANCE DUE 315.00"))],
    "table_bare_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "185", "315.00"), footer="          TOTAL CHARGES 315.00  BALANCE DUE 315.00"))],
    "table_rate_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Charge per visit", "185", "315.00")))],
    "table_rate_dollar_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Charge per visit", "$185", "315.00")))],
    "table_no_date": [rec(1, PT, _ledger(row("", "", "97014", "E-stim unattended", "35.00", "165.00"), footer="          TOTAL CHARGES 165.00  BALANCE DUE 165.00"))],
    "table_totals_under_columns": [rec(1, PT, _ledger(footer=TOTALS_ROW))],
    "table_total_no_cents": [rec(1, PT, _ledger(footer="          TOTAL CHARGES 130  BALANCE DUE 130.00"))],
    "table_figure_above_header": [rec(1, PT, "Previous statement balance $400.00\n" + _ledger())],
    "prose_unlabelled": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Office visit $250.00. Total charges $250.00. Balance due $250.00.")],
    "prose_balance_only": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Balance due $250.00.")],
    "prose_rate_only": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Charge per visit $185.00. Total charges $185.00. Balance due $185.00.")],
    "prose_ocr": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Physical therapy $2O0.00. Total charges $200.00. Balance due $200.00.")],
    "prose_no_dollar_sign": [rec(1, PT, _prose("Payment received 300.00."))],
    "prose_estimate": [rec(1, PT, _prose("Estimated cost of care $500.00."))],
    "prose_rates": [rec(1, PT, _prose(*PROSE_RATES))],
    "table_balance_forward": [rec(1, PT, _fwd("Balance forward  100.00"))],
    "table_two_balance_forwards": [rec(1, PT, _fwd("Balance forward  100.00", "Balance forward   50.00"))],
    "two_totals_disagree": [rec(1, PT, _prose(total="Total charges $250.00. Balance due $250.00. Total charges $310.00."))],
    "ledger_plus_claim": [rec(1, PT, _ledger()), rec(2, "Medlark Clinic, CMS-1500", cms("    060126   060126   11     98941              AB     85.00         1      SYN-NPI-0001"))],
    "r3_prose_previous_balance": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Previous balance $500.00. New patient exam charge $250.00. Total charges $250.00. Balance due $750.00.")],
    "r3_prose_previous_balance_no_due": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Previous balance $500.00. New patient exam charge $250.00. Total charges $250.00.")],
    "r3_dateless_row_dollar_no_cents": [rec(1, PT, _ledger(row("", "", "97014", "E-stim unattended", "$35", "165.00")))],
    "r3_cms_words_box": [rec(1, CMS_SRC, cms(CMS_OK, "    060426   060426   11     97010          A   ten dollars   1      SYN-NPI-0001"))],
    "r5_two_statements": [rec(1, PT, _stmt("97162", "PT eval", "210.00", "210.00")), rec(2, PT, _stmt("97110", "Therapeutic exercise", "130.00", "130.00", "06/10/26"))],
    "r5_second_claim_total": [rec(1, CMS_SRC, cms(CMS_OK, total="28. TOTAL CHARGE  85 | 00")),
                              rec(2, CMS_SRC, cms("    060226   060226   11     98941              AB     90 | 00       1      SYN-NPI-0001", total="28. TOTAL CHARGE  90 | 00"))],
    "r5_prose_two_totals": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Total charges $250.00. Total charges 99.00.")],
    "r5_prose_previous_balance_twice": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Previous balance $500.00. New patient exam charge $250.00. Previous balance $75.00. Total charges $250.00.")],
    "r5_ledger_with_eob": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)],
    "eob_sample": [rec(1, EOB_SRC, EOB)],
    "eob_dollar_no_cents": [rec(1, EOB_SRC, eob_text(eob_row(billed="$140")))],                    # T-103 r1 B1: '$140' was lost from every field
    "eob_dollar_no_cents_paid": [rec(1, EOB_SRC, eob_text(eob_row(plan_paid="$16")))],
    "eob_ocr_letters": [rec(1, EOB_SRC, eob_text(eob_row(billed="1O0.00")))],
    "eob_bare_under_column": [rec(1, EOB_SRC, eob_text(eob_row(billed="130", plan_paid="16")))],
    "eob_odd_decimals": [rec(1, EOB_SRC, eob_text(eob_row(billed="130.5", allowed="78.123")))],
    "eob_missing_column": [rec(1, EOB_SRC, eob_text(eob_row().replace("   26.00", "")))],
    "eob_extra_figure": [rec(1, EOB_SRC, eob_text(eob_row() + "  104.00"))],
    "eob_figure_above_header": [rec(1, EOB_SRC, eob_text(eob_row()).replace("Provider:", "Billed to date $75.00\nProvider:"))],
    "eob_total_row_no_cents": [rec(1, EOB_SRC, eob_text(eob_row(), total="TOTAL              $235   115.00"))],
    "eob_ledger_conflict": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, EOB_SRC, eob_text(eob_row(billed="$140")))],
    "r5_skipped_ambulance": [rec(1, "Brightwater Ambulance invoice", "Brightwater Ambulance (SYNTHETIC) invoice\nALS transport 1234.00 mileage 1234.00 supplies 1234.00")],
    "r5_skipped_injection": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER, injection_tag=True)],
}
for _name, _extra in {"M2_second_total_charges": "\n          TOTAL CHARGES 99.00", "M3_second_total_bare": "\n          TOTAL CHARGES 99",
                      "M4_second_balance_due": "\n          BALANCE DUE 55.00", "M2b_second_total_equal": "\n          TOTAL CHARGES 210.00"}.items():
    PROBES[_name] = [rec(1, PT, _stmt("97162", "PT eval", "210.00", "210.00") + _extra)]

# whole numbers that are money in these inputs (D-049), with where each must end up
BARE_PROBES = {
    "P11_bare_prose_figure": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Office visit 250. Total charges $500.00.")], "250", True),
    "P12_dollar_no_cents_prose": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Office visit $250. Total charges $500.00.")], "$250", True),
    "P10_unlabelled_decimal_prose": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Office visit 250.00. Total charges $500.00.")], "250.00", True),
    "P13_bare_labelled_charge": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge 250. Total charges $250.00.")], "250", True),
    "P16_dateless_cms_bare": ([rec(1, CMS_SRC, cms(CMS_OK, "    11     98941              AB     85       1      SYN-NPI-0001"))], "85", True),
    "P16b_dateless_cms_dollar": ([rec(1, CMS_SRC, cms(CMS_OK, "    11     98941              AB     $85.00      1      SYN-NPI-0001"))], "$85.00", True),
    "P7_dateless_table_row_bare": ([rec(1, PT, _ledger(row("", "", "97014", "E-stim unattended", "35", "165.00")))], "35", True),
    "P4_balance_forward_bare": ([rec(1, PT, _fwd("Balance forward  100"))], "100", True),
    "P18_balance_forward_dollar_no_cents": ([rec(1, PT, _fwd("Balance forward  $100"))], "$100", True),
    "P15_dated_cms_bare_box": ([rec(1, CMS_SRC, cms(CMS_OK, "    060226   060226   11     98941              AB     45       1      SYN-NPI-0001"))], "45", False),
    "eob_bare_charge": ([rec(1, EOB_SRC, eob_text(eob_row(billed="130")))], "130", False),
    "eob_bare_paid": ([rec(1, EOB_SRC, eob_text(eob_row(plan_paid="16")))], "16", False),
    "eob_bare_total_row": ([rec(1, EOB_SRC, eob_text(eob_row(), total="TOTAL              235   115.00"))], "235", True),
    "A_table_bare_charge": ([rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "185", "315.00")))], "185", False),
}


def _texts(out):
    """Every figure text the analysis shows anywhere a paralegal can read it: unreconciled, rates and other extra lines, on-row unclear."""
    return {_nt(f) for f in figs(out)} | {_nt(l["figure"]["text"]) for l in out["lines"] if "figure" in l} | {_nt(x) for l in out["lines"] for x in l.get("unclear", [])}


@pytest.mark.parametrize("name", sorted(PROBES))
def test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped(name):
    recs = PROBES[name]
    assert unaccounted(recs, one(recs)) == [], name


@pytest.mark.parametrize("name", sorted(BARE_PROBES))
def test_bare_or_dateless_money_token_is_shown(name):
    recs, tok, in_unreconciled = BARE_PROBES[name]
    out = one(recs)
    assert _nt(tok) in _texts(out), name
    if in_unreconciled:
        assert _nt(tok) in {_nt(f) for f in figs(out)}, name
    assert unaccounted(recs, out, bare=(tok,) if tok[0] != "$" and "." not in tok else ()) == []


def test_oracle_is_not_vacuous():
    """Erase what the analysis shows and the oracle names every figure; keep it and the oracle is silent."""
    recs = PROBES["prose_unlabelled"]
    out = B.analyze(recs)
    assert unaccounted(recs, out) == []
    out["lines"], out["unreconciled"] = [], []
    assert [t for t, _u in unaccounted(recs, out)] == ["$250.00", "$250.00", "$250.00"]
    recs = BARE_PROBES["P11_bare_prose_figure"][0]
    out = B.analyze(recs)
    out["unreconciled"] = []
    assert [t for t, _u in unaccounted(recs, out, bare=("250",))] == ["250"]
    recs = BARE_PROBES["A_table_bare_charge"][0]
    out = B.analyze(recs)
    bad = next(l for l in out["lines"] if l.get("unclear"))
    bad["billed"], bad["unclear"] = {"text": "185", "cents": None, "usd": None}, []      # a parsed slot with no value is not a placement
    assert [t for t, _u in unaccounted(recs, out, bare=("185",))] == ["185"]


# ---- EOB rows (T-103 r2): every figure of a service row is a structured figure or sits on its row as unclear; nothing is compared with the ledger
def _eob_line(out, service="97110"):
    return next(l for l in out["lines"] if l["form"] == "eob" and l["code"] == service)


@pytest.mark.parametrize("fig", ["$140", "$130", "1O0.00", "130", "130.5"])
def test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text(fig):
    recs = [rec(1, EOB_SRC, eob_text(eob_row(billed=fig)))]
    out = one(recs)
    line = _eob_line(out)
    assert fig in line["unclear"] and line["eob"] == {} and line["class"] == "unclear" and line["detail"] == "eob" and line["checks"] == ["LINE_UNCLEAR"]
    assert line["excerpt"] in recs[0]["text"] and fig in line["excerpt"]
    assert unaccounted(recs, out, bare=(fig,) if re.fullmatch(r"\d+", fig) else ()) == []


def test_eob_figure_that_disagrees_with_the_ledger_is_listed_and_nothing_is_raised():
    """r1 B1/B2/M1: '$140' against a ledger 130.00. No check, no ledger sum, no payer report: both rows are lines with their own excerpt."""
    out = one(PROBES["eob_ledger_conflict"])
    assert "$140" in _eob_line(out)["unclear"] and checks(out) == ["LINE_UNCLEAR"]
    assert next(l for l in out["lines"] if l["code"] == "97110" and l["form"] == "ledger")["billed"]["cents"] == 13000
    assert not [k for d in B._walk(out) for k in d if k in ("ledger", "payer_reports", "matched_provider")]


def test_eob_row_reason_codes_and_service_code_are_not_money_tokens():
    out = one([rec(1, EOB_SRC, EOB)])
    assert [l["excerpt"] for l in out["unreconciled"]][0].startswith("TOTAL") and len(out["unreconciled"]) == 1
    assert all(l["unclear"] == [] for l in out["lines"] if l["form"] == "eob")


def test_eob_fail_safe_names_a_figure_dropped_from_a_row_and_stays_silent_when_it_is_kept():
    """The accounting test must be able to fail for EOB rows (r1 M3, mutant M06). Distinct figures, so each drop is visible to the set-based oracle."""
    row_ = eob_row(billed="130.00", plan_paid="16.00", discount="52.00", allowed="78.00", deduct="22.00", coins="4.00", owes="26.00")
    recs = [rec(1, EOB_SRC, eob_text(row_))]
    assert unaccounted(recs, B.analyze(recs)) == []
    for k in ("billed", "discount", "allowed", "deductible", "coinsurance", "plan_paid", "patient_owes"):
        out = B.analyze(recs)
        del _eob_line(out)["eob"][k]
        assert len(unaccounted(recs, out)) == 1, k
    for fig in ("$140", "1O0.00"):
        recs = [rec(1, EOB_SRC, eob_text(eob_row(billed=fig)))]
        out = B.analyze(recs)
        assert unaccounted(recs, out) == []
        _eob_line(out)["unclear"] = []                                  # mutant M06: the unclear list dropped
        assert fig in {t for t, _u in unaccounted(recs, out)}, fig
    recs = [rec(1, EOB_SRC, eob_text(eob_row(), total="TOTAL              $235   115.00"))]
    out = B.analyze(recs)
    out["unreconciled"] = []
    assert {t for t, _u in unaccounted(recs, out)} == {"$235", "115.00"}


# ---- a figure with no cents is kept as text; a row that does not fit is listed; a printed total is a line
@pytest.mark.parametrize("fig", ["$185", "185"])
def test_table_charge_with_no_cents_is_on_its_row_as_unclear(fig):
    out = one([rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", fig, "315.00"), footer="          TOTAL CHARGES 315.00  BALANCE DUE 315.00"))])
    bad = next(l for l in rows(out, "Medlark") if l["code"] == "99213")
    assert bad["billed"] is None and bad["unclear"] == [fig] and bad["checks"] == ["LINE_UNCLEAR"] and bad["class"] == "unclear"


@pytest.mark.parametrize("fig", ["185", "$185"])
def test_table_rate_row_with_no_cents_is_a_rate_line_with_its_text(fig):
    out = one([rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Charge per visit", fig, "315.00")))])
    assert [(x["figure"]["text"], x["figure"]["cents"], x["class"]) for x in rates(out)] == [(fig, None, "rate")]
    assert "Charge per visit" in rates(out)[0]["excerpt"] and [l["code"] for l in rows(out, "Medlark")] == ["99202"]


def test_table_payment_on_a_rate_row_is_kept_as_a_payment_line():
    t = tbl(HEAD_TXT, [row("06/10/26", "06/11/26", "99202", "New patient exam", "130.00", "130.00"),
                       row("06/10/26", "06/11/26", "99213", "Charge per visit", "185.00", "130.00", PAYMENTS="55.00")], "          TOTAL CHARGES 130.00  BALANCE DUE 130.00")
    out = one([rec(1, PT, t)])
    assert [x["figure"]["cents"] for x in rates(out)] == [18500]
    assert [(l["class"], cents(l, "paid")) for l in rows(out, "Medlark") if l["class"] == "payment"] == [("payment", 5500)]


def test_table_totals_row_printed_under_the_columns_is_read_as_printed_totals():
    out = one([rec(1, PT, _ledger(footer=TOTALS_ROW))])
    assert detail(out, "stated_total_billed")[0]["figure"]["cents"] == 13000 and detail(out, "stated_total_balance")[0]["figure"]["cents"] == 13000 and out["unreconciled"] == []


def test_table_total_with_no_cents_is_unreconciled():
    (u,) = one([rec(1, PT, _ledger(footer="          TOTAL CHARGES 130  BALANCE DUE 130.00"))])["unreconciled"]
    assert u["figures"] == ["130"] and "TOTAL CHARGES 130" in u["excerpt"]


def test_table_figure_above_the_header_is_unreconciled():
    (u,) = one([rec(1, PT, "Previous statement balance $400.00\n" + _ledger())])["unreconciled"]
    assert u["figures"] == ["$400.00"]


def test_one_balance_forward_is_a_line_with_its_cite():
    out = one([rec(1, PT, _fwd("Balance forward  100.00"))])
    (f,) = detail(out, "balance_forward")
    assert f["figure"]["cents"] == 10000 and f["excerpt"] == "Balance forward  100.00" and out["unreconciled"] == []
    assert [cents(l) for l in rows(out, "Medlark")] == [13000]


def test_two_balance_forward_rows_are_both_unreconciled_none_overwritten():
    out = one([rec(1, PT, _fwd("Balance forward  100.00", "Balance forward   50.00"))])
    assert sorted(figs(out)) == ["100.00", "50.00"] and {u["excerpt"] for u in out["unreconciled"]} == {"Balance forward  100.00", "Balance forward   50.00"}


def test_balance_forward_in_two_records_of_one_provider_lists_both():
    r2 = tbl(HEAD_TXT, [row("06/20/26", "06/21/26", "97110", "Therapeutic exercise", "70.00", "100.00")], "          TOTAL CHARGES 70.00  BALANCE DUE 100.00")
    r2 = r2.replace("\n06/20/26", "\n          Balance forward   30.00\n06/20/26", 1)
    out = one([rec(1, PT, _fwd("Balance forward  100.00")), rec(2, PT, r2)])
    assert {"100.00", "30.00"} <= set(figs(out))


def test_prose_previous_balance_is_a_balance_forward_not_the_statement_balance():
    out = one(PROBES["r3_prose_previous_balance"])
    assert detail(out, "balance_forward")[0]["figure"]["cents"] == 50000 and detail(out, "stated_total_balance")[0]["figure"]["cents"] == 75000


def test_a_printed_balance_due_is_listed_as_printed_with_or_without_a_forward_and_no_verdict_is_given():
    """D-052: no balance reconciliation. Whatever BALANCE DUE a statement prints is a cited line, equal to the lines or not."""
    for due in ("440.00", "340.00", "500.00", "999.00"):
        t = tbl(HEAD_TXT, [row("06/01/26", "06/02/26", "97162", "PT eval", "210.00", "310.00"), row("06/10/26", "06/11/26", "97110", "Therapeutic exercise", "130.00", "440.00")],
                f"          TOTAL CHARGES 340.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE {due}").replace("\n06/01/26", "\n          Balance forward  100.00\n06/01/26", 1)
        out = one([rec(1, PT, t)])
        assert detail(out, "stated_total_balance")[0]["figure"]["text"] == due and detail(out, "balance_forward")[0]["figure"]["cents"] == 10000
        assert out["unreconciled"] == [] and checks(out) == []


def test_a_balance_step_that_does_not_follow_raises_nothing_and_an_unreadable_charge_is_class_unclear():
    t = tbl(HEAD_TXT, [row("06/01/26", "06/02/26", "97162", "PT eval", "210.00", "210.00"), row("06/10/26", "06/11/26", "97110", "Therapeutic exercise", "130.00", "999.00")],
            "          TOTAL CHARGES 340.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 340.00")
    assert checks(one([rec(1, PT, t)])) == []            # D-052: no arithmetic on a line; 999.00 is listed as printed
    assert next(l for l in rows(one(BARE_PROBES["A_table_bare_charge"][0]), "Medlark") if l["code"] == "99213")["class"] == "unclear"


# ---- prose: an unlabelled figure is never a charge (pins the prose charge gate; reviewer mutant M05) and never dropped
def test_prose_unlabelled_figure_is_unreconciled_not_a_charge():
    out = one([rec(1, PT, _prose("Standard fee $185.00."))])
    assert [cents(l) for l in rows(out, "Medlark")] == [25000]
    (u,) = out["unreconciled"]
    assert u["figures"] == ["$185.00"] and u["excerpt"] == "Standard fee $185.00." and u["reason_code"] == "ROW_NOT_PARSED"


def test_prose_figure_with_no_billing_word_is_unreconciled_and_its_total_is_a_line():
    out = one(PROBES["prose_unlabelled"])
    assert [cents(l) for l in rows(out, "Medlark")] == [] and [u["figures"] for u in out["unreconciled"]] == [["$250.00"]]
    assert detail(out, "stated_total_billed")[0]["figure"]["cents"] == 25000


def test_prose_statement_with_only_a_printed_total_is_listed_not_none_found():
    out = one(PROBES["prose_balance_only"])
    assert out["status"] == "listed" and out["unreconciled"][0]["figures"] == ["$250.00"] and "Balance due $250.00" in out["unreconciled"][0]["excerpt"]


def test_prose_rate_only_statement_lists_the_rate_and_both_printed_totals():
    out = one(PROBES["prose_rate_only"])
    assert [x["figure"]["cents"] for x in rates(out)] == [18500] and {u["figures"][0] for u in out["unreconciled"]} == {"$185.00"} and len(out["unreconciled"]) == 2


def test_prose_unreadable_figure_is_listed_with_its_text():
    assert [u["figures"] for u in one(PROBES["prose_ocr"])["unreconciled"]] == [["$2O0.00"]]


def test_prose_decimal_figure_with_no_dollar_sign_is_unreconciled():
    out = one(PROBES["prose_no_dollar_sign"])
    assert [u["figures"] for u in out["unreconciled"]] == [["300.00"]] and [cents(l) for l in rows(out, "Medlark")] == [25000]


def test_prose_estimate_is_an_unclear_line_not_a_charge():
    out = one(PROBES["prose_estimate"])
    assert [(x["detail"], x["class"], x["figure"]["cents"]) for x in out["lines"] if x["detail"] == "estimate"] == [("estimate", "unclear", 50000)]
    assert [cents(l) for l in rows(out, "Medlark")] == [25000] and out["unreconciled"] == []


def test_two_different_printed_totals_are_both_listed_none_picked():
    out = one(PROBES["two_totals_disagree"])
    assert [u["figures"] for u in out["unreconciled"]] == [["$250.00"]] and detail(out, "stated_total_billed")[0]["figure"]["cents"] == 31000


# ---- CMS-1500: a service line with no date, or no units, is listed with its money tokens only
def test_cms1500_line_with_no_dates_is_unreconciled_with_only_its_figure():
    out = one(PROBES["cms_no_dates"])
    (u,) = out["unreconciled"]
    assert u["figures"] == ["85.00"] and "98941" in u["excerpt"] and [cents(l) for l in rows(out, "Brightwater")] == [8500]


def test_cms1500_line_with_no_units_lists_only_the_money_token_not_the_tail():
    (u,) = one(PROBES["cms_no_units"])["unreconciled"]
    assert u["figures"] == ["85.00"]


def test_cms1500_unreadable_total_is_unreconciled():
    assert one(PROBES["cms_unreadable_total"])["unreconciled"][0]["figures"] == ["1O0 | 00"]


def test_an_unparsed_claim_line_is_unreconciled_beside_the_ledger_rows():
    out = one([rec(1, PT, _ledger()), rec(2, "Medlark Clinic, CMS-1500", cms("    11     98941              AB     85.00         1      SYN-NPI-0001"))])
    assert [cents(l) for l in rows(out, "Medlark")] == [13000] and out["unreconciled"][0]["record_no"] == 2


def test_ub04_line_with_a_figure_that_fits_no_revenue_row_is_unreconciled():
    assert [u["figures"] for u in one(PROBES["ub04_stray_figure"])["unreconciled"]] == [["125.00"]]


def test_dateless_cms_line_lists_only_its_money_token_and_a_worded_box_lists_none():
    assert [u["figures"] for u in one(BARE_PROBES["P16_dateless_cms_bare"][0])["unreconciled"]] == [["85"]]
    out = one(PROBES["r3_cms_words_box"])
    assert [u["figures"] for u in out["unreconciled"]] == [[]] and "ten dollars" not in " ".join(out["unreconciled"][0]["figures"])


def test_dateless_table_row_lists_its_bare_charge_with_the_decimal():
    assert [u["figures"] for u in one([rec(1, PT, _ledger(row("", "", "97014", "E-stim unattended", "35", "165.00")))])["unreconciled"]] == [["35", "165.00"]]


# ---- repeated summary rows are never overwritten (D-049)
def test_second_statement_total_never_overwrites_the_first():
    out = one(PROBES["r5_two_statements"])
    assert {"210.00", "130.00"} <= set(figs(out)) and [cents(l) for l in rows(out, "Medlark")] == [21000, 13000]


def test_first_statement_total_is_visible_when_a_second_statement_follows():
    r1 = _stmt("97162", "PT eval", "210.00", "340.00").replace("\n06/01/26", "\n          Balance forward  100.00\n06/01/26", 1)
    r2 = tbl(HEAD_TXT, [row("06/20/26", "06/21/26", "97110", "Therapy", "70.00", "70.00")], "          TOTAL CHARGES 70.00  BALANCE DUE 70.00")
    assert {"340.00", "70.00"} <= set(figs(one([rec(1, PT, r1), rec(2, PT, r2)])))


def test_identical_copy_of_one_statement_lists_each_records_totals_on_its_own():
    t = _stmt("97162", "PT eval", "210.00", "210.00")
    out = one([rec(1, PT, t), rec(2, PT, t)])
    assert all(len(x["record_nos"]) == 1 for x in out["lines"]) and {x["record_no"] for x in out["lines"]} == {1, 2}
    assert sorted(u["record_no"] for u in out["unreconciled"]) == [1, 1, 1, 1, 2, 2, 2, 2]      # each record's four printed totals, listed, none hidden behind the other record's


def test_second_claim_form_total_is_listed_too():
    assert len(one(PROBES["r5_second_claim_total"])["unreconciled"]) >= 2


@pytest.mark.parametrize("name,token", [("M2_second_total_charges", "99.00"), ("M3_second_total_bare", "99"), ("M4_second_balance_due", "55.00"), ("M2b_second_total_equal", "210.00")])
def test_repeated_summary_row_in_one_record_is_listed_the_earlier_one_unreconciled(name, token):
    out = one(PROBES[name])
    assert out["unreconciled"] and _nt(token) in _texts(out), name


def test_clean_statement_has_nothing_unreconciled():
    assert one([rec(1, PT, _stmt("97162", "PT eval", "210.00", "210.00"))])["unreconciled"] == []


def test_two_statements_each_with_a_forward_list_both_forwards():
    f1 = _stmt("97162", "PT eval", "210.00", "210.00").replace("\n06/01/26", "\n          Balance forward  40.00\n06/01/26", 1)
    f2 = _stmt("97110", "Therapy", "130.00", "130.00", "06/10/26").replace("\n06/10/26", "\n          Balance forward  60.00\n06/10/26", 1)
    assert {"40.00", "60.00"} <= set(figs(one([rec(1, PT, f1), rec(2, PT, f2)])))


@pytest.mark.parametrize("name,token", [("r5_prose_two_totals", "99.00"), ("r5_prose_previous_balance_twice", "$75.00")])
def test_repeated_prose_summary_is_unreconciled(name, token):
    assert token in figs(one(PROBES[name]))


# ---- skipped billing records
def test_unrecognised_billing_form_and_injection_are_skipped_never_none_found():
    out = one(PROBES["r5_skipped_ambulance"])
    assert [x["reason_code"] for x in out["skipped_records"]] == ["UNRECOGNISED_BILLING_FORM"] and out["status"] == "listed" and out["lines"] == []
    out = one(PROBES["r5_skipped_injection"])
    assert [x["reason_code"] for x in out["skipped_records"]] == ["INJECTION_SUSPECTED"] and out["status"] == "listed" and out["lines"] == []


def test_eob_is_lines_not_a_skip():
    out = one(PROBES["r5_ledger_with_eob"])
    assert out["skipped_records"] == [] and len([l for l in out["lines"] if l["form"] == "eob"]) == 3
    (u,) = out["unreconciled"]
    assert u["form"] == "eob" and u["excerpt"].startswith("TOTAL") and u["figures"][0] == "235.00"      # the EOB's printed total row is listed, not dropped


# ---- the money-token definition (D-049): a bare whole number is a token only in an amount column
def test_bare_whole_number_on_a_stray_line_is_not_a_money_token_but_one_under_a_column_is():
    """Pins the definition in the module docstring. Fuzz class r4 finding 3: a stray '208' outside every column is not a token; the same number
    right-aligned under CHARGES is, and then it is listed."""
    base = _ledger()
    assert B._tokens("          208", B._header(base.split("\n"))[1]) == []
    assert "208" not in _texts(one([rec(1, PT, base + "\n          208")]))
    assert "208" in _texts(one([rec(1, PT, base + "\n" + " " * 61 + "208")]))
    assert "MONEY TOKEN" in B.__doc__ and "amount column" in B.__doc__


# ---- property: a random money token put anywhere in a billing record is a line, unreconciled, or its record is skipped
_BASES = {
    "table": lambda: _ledger(),
    "table_sample": lambda: LEDGER,
    "prose": lambda: PROSE,
    "cms": lambda: cms(CMS_OK, "    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001", total="28. TOTAL CHARGE  170 | 00     29. AMOUNT PAID  0 | 00"),
    "ub04": lambda: UB_ROOM,
    "eob": lambda: EOB,
    "eob_rows": lambda: eob_text(eob_row(), eob_row(service="97140", billed="70.00", plan_paid="16.00")),
}
_SRC = {"table": PT, "table_sample": PT, "prose": "Fennimoor Spine Clinic, itemized ledger", "cms": CMS_SRC, "ub04": "Saltmarrow General Hospital, UB-04",
        "eob": EOB_SRC, "eob_rows": EOB_SRC}
_TOKENS = ["$123.45", "123.45", "$77", "88", "(45.00)", "1,234.50", "45.00-", "$9,999", "2O0.00", "9.999", "310"]


def _insert(text, tok, rnd, base):
    """Put the token somewhere in the ledger. A whole number (no '$', no cents) is money only in an amount position (D-049): in a sentence for
    prose, right-aligned under a money column on a line of its own for a table or a UB-04. It is not put in a CMS-1500 (that form's boxes are tested by name)."""
    lines = text.split("\n")
    if re.fullmatch(r"\d+", tok):
        if base == "prose":
            return text.replace(". Balance due", f". Office visit {tok}. Balance due", 1) if rnd.random() < 0.5 else text + f" Visit fee {tok}."
        hdr, cols = B._header(lines) if base.startswith("table") else B._eob_header(lines) if base.startswith("eob") else B._ub_header(lines)
        if hdr is None:
            return text
        kind = rnd.choice(sorted(k for k in cols if k != "rate"))
        lines.insert(rnd.randrange(hdr + 1, len(lines) + 1), " " * max(0, cols[kind][1] - len(tok)) + tok)
        return "\n".join(lines)
    mode = rnd.choice(["append_line", "own_line", "mid_line"])
    i = rnd.randrange(len(lines))
    if mode == "own_line":
        lines.insert(i, "          " + tok)
    elif mode == "append_line":
        lines[i] = lines[i] + "   " + tok
    else:
        cut = rnd.choice([m.end() for m in re.finditer(r"\s+", lines[i])] or [len(lines[i])])
        lines[i] = lines[i][:cut] + tok + " " + lines[i][cut:]
    return "\n".join(lines)


def test_property_a_random_money_token_is_never_silently_missing():
    rnd, n = random.Random(20261102), 0
    for _ in range(600):
        base, tok = rnd.choice(sorted(_BASES)), rnd.choice(_TOKENS)
        text = _insert(_BASES[base](), tok, rnd, base)
        recs = [rec(1, _SRC[base], text)]
        out = B.analyze(recs)
        assert B.verify_citations(out, recs) == [], (base, tok, text)
        bare = (tok,) if re.fullmatch(r"\d+", tok) else ()
        missing = unaccounted(recs, out, bare=bare)
        assert missing == [], (base, tok, missing, text)
        assert _out_counts(out) == _in_counts(recs, out, bare), (base, tok, text)      # T-103 r4: the exact per-record count, not only presence
        n += text != _BASES[base]()
    assert n > 400, n            # the token really was inserted in most draws


@pytest.mark.parametrize("seed", range(1, 6))
def test_property_a_exact_count_holds_for_other_seeds_too(seed):
    """The reviewer's generator again (same bases, tokens and insertion rule) with other seeds: 5 x 600 draws, citations verified, exact per-record count."""
    rnd = random.Random(seed)
    for _ in range(600):
        base, tok = rnd.choice(sorted(_BASES)), rnd.choice(_TOKENS)
        text = _insert(_BASES[base](), tok, rnd, base)
        recs = [rec(1, _SRC[base], text)]
        out = B.analyze(recs)
        bare = (tok,) if re.fullmatch(r"\d+", tok) else ()
        assert B.verify_citations(out, recs) == [] and unaccounted(recs, out, bare=bare) == [], (seed, base, tok, text)
        assert _out_counts(out) == _in_counts(recs, out, bare), (seed, base, tok, text)


# ------------------------------------------------------------------ T-103 r3: nothing merges across records or providers
_CROSS_ROW = row("06/10/26", "06/11/26", "97110", "Therapeutic exercise", "130.00", "130.00")
_CROSS_TXT = tbl(HEAD_TXT, [_CROSS_ROW], "          TOTAL CHARGES 130.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 130.00")


def test_identical_rows_from_two_providers_are_two_lines_one_per_provider():
    """The reviewer's probe (merge_cross_provider_probe.py): Larkspur and Medlark print the same 97110 row. Each charge is its own line."""
    recs = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", _CROSS_TXT), rec(2, "Medlark Clinic, itemized statement", _CROSS_TXT)]
    out = one(recs)
    charges = [l for l in out["lines"] if l.get("code") == "97110"]
    assert [(l["provider"], l["record_nos"], l["billed"]["cents"]) for l in charges] == [("Larkspur Hollow Physical Therapy", [1], 13000), ("Medlark Clinic", [2], 13000)]
    assert [c["record_no"] for l in charges for c in l["cites"]] == [1, 2]
    assert unaccounted(recs, out) == []


def test_identical_rows_from_one_provider_in_two_records_are_two_lines():
    """Even the same provider's re-sent row is not folded: each record's line cites only that record."""
    recs = [rec(1, PT, _CROSS_TXT), rec(2, PT, _CROSS_TXT)]
    charges = [l for l in one(recs)["lines"] if l.get("code") == "97110"]
    assert [l["record_nos"] for l in charges] == [[1], [2]]


def test_line_ids_are_unique_and_follow_record_then_position():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", _CROSS_TXT), rec(2, "Medlark Clinic, itemized statement", _CROSS_TXT)])
    ids = [l["id"] for l in out["lines"]]
    assert len(set(ids)) == len(ids) and [l["record_no"] for l in out["lines"]] == sorted(l["record_no"] for l in out["lines"])


def test_a_stated_total_printed_by_two_providers_is_one_line_each():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", _CROSS_TXT), rec(2, "Medlark Clinic, itemized statement", _CROSS_TXT)])
    tot = detail(out, "stated_total_billed")
    assert not tot or sorted(l["provider"] for l in tot) == ["Larkspur Hollow Physical Therapy", "Medlark Clinic"]
    assert sorted({u["provider"] for u in out["unreconciled"] if "TOTAL CHARGES" in u["excerpt"]} | {l["provider"] for l in tot}) == ["Larkspur Hollow Physical Therapy", "Medlark Clinic"]


# ---- a rate or LOP row's other money tokens are their own entries (T-103 r3)
def _rate_probe(balance="999.00"):
    return [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Charge per visit", "185.00", balance)))]


def test_rate_row_running_balance_is_a_structured_field_not_only_in_the_excerpt():
    out = one(_rate_probe())
    (r,) = [l for l in out["lines"] if l["class"] == "rate"]
    assert r["figure"]["text"] == "185.00" and [f["text"] for f in r["other_figures"]] == ["999.00"] and r["other_figures"][0]["cents"] == 99900
    assert "999.00" in r["excerpt"]


def test_rate_row_with_a_no_cents_balance_carries_it_as_an_other_figure_with_no_value():
    """T-103 r4: every other money token on a rate row is that entry's other figure, a no-cents one included (text, cents None); it is not also a line."""
    out = one(_rate_probe("$315"))
    (r,) = rates(out)
    assert [(f["text"], f["cents"]) for f in r["other_figures"]] == [("$315", None)]
    assert not [l for l in out["lines"] if l.get("unclear")]


def test_lop_row_other_money_token_is_a_structured_field():
    out = one([rec(1, "Letter of protection to Fennimoor Spine Clinic", LOP)])
    texts = [f["text"] for l in out["lines"] if "figure" in l for f in [l["figure"], *l["other_figures"]]]
    assert sorted(texts) == ["$3,100.00", "$4,860.00"]


def test_other_figure_must_sit_in_its_excerpt():
    recs = _rate_probe()
    out = B.analyze(recs)
    next(l for l in out["lines"] if l["class"] == "rate")["other_figures"][0]["text"] = "123.45"
    assert B.verify_citations(out, recs)[0]["reason"] == "other_figure_not_in_excerpt"


def test_dropping_the_other_figures_turns_the_oracle_red():
    recs = _rate_probe()
    out = B.analyze(recs)
    assert unaccounted(recs, out) == []
    next(l for l in out["lines"] if l["class"] == "rate")["other_figures"] = []
    assert [t for t, _u in unaccounted(recs, out)] == ["999.00"]


# ---- the fail-safe count: per record, the money tokens in the output equal the money tokens in the input
_COUNT_BARE = {"table_bare_no_cents": ("185",), "table_rate_no_cents": ("185",), "table_total_no_cents": ("130",), "M3_second_total_bare": ("99",), "eob_bare_under_column": ("130", "16")}


def _out_counts(out):
    """{record_no: Counter of normalised token texts}: every money token the output shows in a figure field (a parsed figure with no value counts only
    through `unclear`), never an excerpt."""
    from collections import Counter
    c = {}

    def put(n, text):
        c.setdefault(n, Counter())[_nt(text)] += 1
    for l in out["lines"]:
        if "figure" in l:
            for f in [l["figure"], *l["other_figures"]]:
                put(l["record_no"], f["text"])
            continue
        for k in ("billed", "paid", "adjustment", "balance"):
            if l.get(k) and l[k]["cents"] is not None:
                put(l["record_no"], l[k]["text"])
        for f in (l.get("eob") or {}).values():
            if f["cents"] is not None:
                put(l["record_no"], f["text"])
        for t in l["unclear"]:
            put(l["record_no"], t)
    for u in out["unreconciled"]:
        for f in u["figures"]:
            put(u["record_no"], f)
    return c


_COUNT_TOKEN = re.compile(r"\$\s?[\dOolISB][\dOolISB,]*(?:\.[\dOolISB]+)?|(?<![\w/.$])[\dOolISB,]*\d[\dOolISB,]*\.[\dOolISB]+(?!\w|\.\d)|(?<![\w/.])[\dO]+\s*\|\s*[\dO]{2}\b")      # liberal: odd decimals and OCR letters count


def _in_counts(records, out, bare=()):
    from collections import Counter
    skipped, c = {s["record_no"] for s in out["skipped_records"]}, {}
    for r in records:
        if r["n"] in skipped:
            continue
        cnt = Counter()
        for s_, e_ in B._segments(r["excerpt"]):
            unit = r["excerpt"][s_:e_].strip()
            toks = [m for m in _COUNT_TOKEN.finditer(unit)]
            for b in bare:
                toks += [m for m in re.finditer(r"(?<![\w/.,$])" + re.escape(b) + r"(?![\w/]|[.,]\d)", unit) if not any(m.start() < t.end() and t.start() < m.end() for t in toks)]
            for t in toks:
                cnt[_nt(t.group(0))] += 1
        if cnt:
            c[r["n"]] = cnt
    return c


# ---- T-103 r4: shapes the 600-draw generator found (and the reviewer's repro cases), each with its exact per-record count
_FOOTER = "          TOTAL CHARGES 130.00  BALANCE DUE 123.45 130.00"
PROBES.update({
    "r4_footer_equal_figure": [rec(1, PT, _ledger(footer=_FOOTER))],
    "r4_fee_schedule_unreadable_figure": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", _ledger() + "\nFee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection.   2O0.00")],
    "r4_rate_balance_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Charge per visit", "185.00", "$315")))],
    "r4_prose_rate_and_balance": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Charge per visit $185.00, balance $999.00. Total charges $185.00.")],
    "r4_lop_two_amounts": [rec(1, "Letter of protection to Fennimoor Spine Clinic", "Lien balance $4,860.00 reduced to $3,100.00 in full satisfaction.")],
    "r4_ub04_units_drift": [rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM.replace("PHARMACY                                     091526", "PHARMACY                                     1,234.50 091526"))],
    "r4_eob_money_in_service_slot": [rec(1, EOB_SRC, EOB.replace("06/10/26  97014", "06/10/26  123.45 97014"))],
    "r4_prose_number_after_figure": [rec(1, "Fennimoor Spine Clinic, itemized ledger", PROSE.replace("treatment visits 1 through 14", "treatment visits $9,999 1 through 14"))],
    "r4_cms_broken_box_fragments": [rec(1, CMS_SRC, cms(CMS_OK, total="28. TOTAL CHARGE  170 2O0.00 | 00     29. AMOUNT PAID  0 $77 | 00"))],
    "r4_cms_lone_odd_decimal": [rec(1, CMS_SRC, cms(CMS_OK, total="28. TOTAL CHARGE  85 | 00     29. AMOUNT PAID  0 | 00") + "\n          9.999")],
    "r4_cms_row_with_odd_decimal": [rec(1, CMS_SRC, cms(CMS_OK + "   9.999", total="28. TOTAL CHARGE  85 | 00     29. AMOUNT PAID  0 | 00"))],
})


def test_the_r4_probe_inputs_really_contain_their_shape():
    """A replace that matched nothing would leave a plain sample and test nothing."""
    assert PROBES["r4_ub04_units_drift"][0]["excerpt"] != UB_ROOM and "123.45 97014" in PROBES["r4_eob_money_in_service_slot"][0]["excerpt"]
    assert "$9,999 1 through" in PROBES["r4_prose_number_after_figure"][0]["excerpt"]


def test_a_units_count_nearer_the_units_header_than_a_money_header_is_not_money():
    """UB-04: a whole number is read against EVERY header, so a count that sits under UNITS (but within reach of TOTAL CHARGES) is not a charge. No decimal on the row,
    so the revenue-row rule does not apply; only the header columns decide."""
    ls = UB_ROOM.split("\n")
    i = next(k for k, ln in enumerate(ls) if ln.startswith("0450"))
    ls[i] = "0450    EMERGENCY ROOM".ljust(72) + "1" + " " * 5 + "1975"
    recs = [rec(1, "Saltmarrow General Hospital, UB-04", "\n".join(ls))]
    out = one(recs)
    assert _out_counts(out)[1]["1975"] == 1 and "1" not in _out_counts(out)[1]
    assert _out_counts(out) == _in_counts(recs, out, bare=("1975",))


def test_a_printed_total_that_shares_its_excerpt_with_an_equal_figure_is_still_its_own_line():
    """The reviewer's R1: 'TOTAL CHARGES 130.00  BALANCE DUE 123.45 130.00'. The stated total, the stated balance and the trailing 130.00 are three entries
    (positions tell them apart, not their text); 130.00 is printed 4 times in the record and shown 4 times."""
    recs = PROBES["r4_footer_equal_figure"]
    out = one(recs)
    assert [l["figure"]["text"] for l in out["lines"] if l.get("detail") in ("stated_total_billed", "stated_total_balance")] == ["130.00", "123.45"]
    assert [u["figures"] for u in out["unreconciled"]] == [["130.00"]]
    assert _out_counts(out) == _in_counts(recs, out) and _out_counts(out)[1]["130.00"] == 4


def test_a_rate_figure_is_not_also_listed_unreconciled_when_its_row_has_an_unreadable_figure():
    out = one(PROBES["r4_fee_schedule_unreadable_figure"])
    (r,) = [l for l in rates(out) if l["figure"]["text"] == "$65.00"]
    assert [f["text"] for f in r["other_figures"]] == ["2O0.00"] and not out["unreconciled"]


def test_prose_rate_sentence_carries_its_second_figure_and_it_is_not_also_a_line():
    out = one(PROBES["r4_prose_rate_and_balance"])
    (r,) = rates(out)
    assert r["figure"]["text"] == "$185.00" and [f["text"] for f in r["other_figures"]] == ["$999.00"]
    assert not detail(out, "stated_total_balance")


def test_lop_sentence_with_two_amounts_is_one_entry_with_the_second_as_an_other_figure():
    out = one(PROBES["r4_lop_two_amounts"])
    (e,) = [l for l in out["lines"] if "figure" in l]
    assert e["figure"]["text"] == "$4,860.00" and [f["text"] for f in e["other_figures"]] == ["$3,100.00"] and e["other_figures"][0]["cents"] == 310000


def test_a_figure_that_is_both_an_lop_amount_and_a_printed_balance_is_one_line():
    out = one([rec(1, "Letter of protection to Fennimoor Spine Clinic", "The client's current balance is $4,860.00.")])
    assert [l["figure"]["text"] for l in out["lines"] if "figure" in l] == ["$4,860.00"]


@pytest.mark.parametrize("name", sorted(PROBES))
def test_every_money_token_on_a_rate_estimate_or_lop_row_is_a_figure_of_that_entry(name):
    """The reviewer's literal rule for api.md: the row's tokens are the entry's figure plus its other_figures, counted. (The row's excerpt is the row.)"""
    from collections import Counter
    out = one(PROBES[name])
    for l in out["lines"]:
        if l["detail"] in ("rate", "estimate", "lien_amount", "asserted_balance", "reduction"):
            printed = Counter(_nt(m.group(0)) for m in _COUNT_TOKEN.finditer(l["excerpt"]))
            shown = Counter(_nt(f["text"]) for f in [l["figure"], *l["other_figures"]])
            for k in ("billed", "paid", "adjustment", "balance"):              # a UB-04 room row is also a charge line: its own figure is that line's, not the rate's
                shown += Counter(_nt(x[k]["text"]) for x in out["lines"] if "figure" not in x and x["excerpt"] == l["excerpt"] and x.get(k))
            assert not (printed - shown), (name, l["id"], l["excerpt"])


def test_no_money_value_or_text_is_compared_in_billing_code():
    """D-052 applied literally (T-103 r4): the listing code never asks whether one figure is equal to, larger than or smaller than another, never sums,
    and never normalises a figure's text to match it against another. Placement is by position; the sign of a figure is a flag read from its printed
    credit notation. Source scan of app/backend/billing.py (code lines only)."""
    import pathlib
    src = pathlib.Path(B.__file__).read_text(encoding="utf-8")
    code = [ln.split("  #")[0] for ln in src.split("\n") if not ln.strip().startswith("#")]
    banned = [r"cents\"?\]?\s*(?:<|>|<=|>=)\s*[-\d(]", r"\bsum\(", r"\b_nt\(", r"\bmax\([^)]*cents", r"\bmin\([^)]*cents", r"\[\"cents\"\]\s*(?:==|!=)", r"\[\"usd\"\]\s*(?:==|!=)",
              r"_nt\(", r"\bfloat\(", r"\bDecimal\("]
    hits = [(p, ln.strip()[:100]) for ln in code for p in banned if re.search(p, ln)]
    assert hits == [], hits


def test_the_sign_of_a_charge_is_the_printed_credit_notation_not_its_value():
    out = one([rec(1, PT, _ledger(row("06/10/26", "06/11/26", "97110", "Therapeutic exercise", "(70.00)", "60.00"), row("06/10/26", "06/11/26", "97140", "Manual therapy", "70.00", "130.00")))])
    assert [(l["code"], l["detail"], l["billed"]["usd"]) for l in rows(out, "Medlark") if l["code"] in ("97110", "97140") and l["billed"]] == [("97110", "reversal", "-$70.00"), ("97140", None, "$70.00")]


@pytest.mark.parametrize("name", sorted(PROBES))
def test_money_token_count_in_the_output_equals_the_count_in_the_input_per_record(name):
    recs = PROBES[name]
    out = one(recs)
    assert _out_counts(out) == _in_counts(recs, out, _COUNT_BARE.get(name, ())), name


def test_the_count_check_sees_a_listed_twice_and_a_dropped_token():
    recs = _rate_probe()
    out = B.analyze(recs)
    assert _out_counts(out) == _in_counts(recs, out)
    rate = next(l for l in out["lines"] if l["class"] == "rate")
    rate["other_figures"].append(dict(rate["other_figures"][0]))                  # listed twice
    assert _out_counts(out) != _in_counts(recs, out)
    rate["other_figures"] = []                                                    # dropped
    assert _out_counts(out) != _in_counts(recs, out)
