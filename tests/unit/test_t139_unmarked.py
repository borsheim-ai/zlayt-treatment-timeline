"""T-139 round 2 (GATE-M2 claims-adjuster fail): money written WITHOUT a '$' (claim-form fields: 'TOTAL CHARGE 49100', 'AMOUNT PAID 0 00', CMS-1500 24F and UB-04
FL47 columns), 'Bills to request' lists only treating providers and facilities (never a law firm), and the held-out hint offers only actions that clear the hold.
Deterministic code only (fixture backend, no key)."""
import pytest
from fastapi.testclient import TestClient

from app.backend import charge_text as CT
from app.backend import export as X
from app.backend import why
from app.backend.api import create_app
from evals import letter_check as LC
from tests.unit.test_api_routes import wait_ready
from tests.unit.test_t139_charge_text import _accept_all, _entry, _post


# ---------------------------------------------------------------- 1. unmarked money: detected
@pytest.mark.parametrize("text", [
    "Item 28 TOTAL CHARGE 49100.",
    "Item 29 AMOUNT PAID 0 00.",
    "Item 28 TOTAL CHARGE 33000. Item 29 AMOUNT PAID 0 00.",
    "Line 1: 092126 to 092326, CPT 98941, 24F 25500, 24G 3.",
    "Item 24F lines: CPT 99204, 18500, 1 unit; CPT 20610, 21000, 1 unit; CPT 97110, 96 OO, 4 units.",
    "CPT 99204, 18500, 1 unit",
    "Charges: 3,915.00",
    "Charge per visit: 140.00",
    "Fee 140/visit",
    "Cost estimate 4,500",
    "Rev 0001 total charges 8,123.50.",
    "FL47 4920 00",
    "Balance due 2,166.00",
    "Amount billed 8,023.50; plan paid 3,530.80.",
    "Item 30: 12500",
    "Copay 40",
    "140.00 per visit",
])
def test_unmarked_money_is_currency(text):
    assert CT.has_currency(text), text
    assert CT.currency_strings(text), text


@pytest.mark.parametrize("text", [
    "Pain 5/10 on the left side, improving.",
    "Plan of care: 8/12 visits, 2x/week for 6 weeks.",
    "Discharged after 3 days of observation. Dx: left knee contusion.",
    "Date: 06/09/2026. Statement period 06/09/2026 to 06/12/2026.",
    "Ibuprofen 800 mg three times daily; Flexeril 10 mg at bedtime.",
    "Heart rate 88, BP 128/82, respiratory rate 16.",
    "Patient attended 12 visits; visit count 12 of 12.",
    "Cervical spine 3 views. CT head negative. MRI left knee ordered.",
    "Item 14 injury date 091426 qualifier 431. Item 31 signature date 110926.",
    "Rev 0120 room and board semi-private, FL46 3 days.",
    "Line 1: CPT 98941, 24G 3.",
    "Balance 42/56 on the Berg scale; balance 4 of 5.",
    "The charge nurse reviewed 2 charts. In charge of the unit.",
    "Estimated 30 minutes per session; estimated 120 minutes total.",
    "CPT 97110, 97112 and 97140 were performed.",
    "Paid 3 weeks of sick leave. Cost 2 visits.",
    "ROM reduced approx. 30%. Pain 7/10.",
])
def test_plain_clinical_numbers_are_not_currency(text):
    assert not CT.has_currency(text), (text, CT.currency_strings(text))


def test_dollar_figures_are_not_double_counted_with_their_label():
    assert CT.currency_strings("FL47 total charges $4,920.00") == ["$4,920.00"]
    assert CT.currency_strings("Rev 0450 ER, 1 unit, charge $2,105.00.") == ["$2,105.00"]
    assert CT.dollar_strings("Charge per visit $140 and total charge 49100") == ["$140"]       # the old '$'-only view the quote picker uses


def test_check_reports_unmarked_money_in_the_quote_and_the_summary():
    f = CT.check("Claim lists total charge 49100.", "Item 28 TOTAL CHARGE 49100.")
    assert "49100" in f["excerpt"][0] and "49100" in f["summary"][0]
    assert CT.check("Pain 3/10.", "Pain 3/10.") == {}


def test_narrowing_drops_claim_form_money_sentences_at_the_ends_only():
    exc = ("OCR of scanned CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, 18500, 1 unit; CPT 20610, 21000, 1 unit; "
           "CPT 97110, 96 OO, 4 units. Item 28 TOTAL CHARGE 49100. Item 29 AMOUNT PAID 0 00.")
    n = CT.narrow_excerpt(exc)
    assert n and n["excerpt"] == "OCR of scanned CMS-1500 for dates of service 06/24/2026 and 07/08/2026." and len(n["dropped"]) == 5     # the splitter breaks at the semicolons too
    mid = "OCR of scanned CMS-1500. Line 1: CPT 98941, 24F 25500, 24G 3. Item 28 TOTAL CHARGE 33000. Item 31 signature date 110926."
    assert CT.narrow_excerpt(mid) is None                                                # an amount in the middle: held out, never skipped


# ---------------------------------------------------------------- 1b. the letter check has its own detector
def test_letter_check_sees_unmarked_money_without_the_detector_it_audits(monkeypatch):
    monkeypatch.setattr(CT, "currency_strings", lambda text: [])                         # the detector under test is blind; the audit must still see it
    letter = ("TREATMENT CHRONOLOGY\n\nJuly 14, 2026 — Wardlaw Orthopedics, CMS-1500\n"
              'Claim lists total charge 49100; amount paid 0 00.\nSource [Ex. __ / Bates __]: "Item 28 TOTAL CHARGE 49100. Item 29 AMOUNT PAID 0 00."')
    bad = LC.violations(letter, ())
    assert bad and any("49100" in b or "0 00" in b for b in bad)


@pytest.mark.parametrize("line", ["Charges: 3,915.00", "Charge per visit: 140.00", "Cost estimate 4,500", "Fee 140/visit", "24F 25500", "FL47 4920 00", "amount paid 0 00"])
def test_letter_check_detector_catches_each_shape(line):
    assert LC.unmarked_money(line), line


@pytest.mark.parametrize("line", ["Pain 5/10.", "Plan of care: 8 visits.", "Discharged after 3 days of observation.", "Heart rate 88.", "CT head negative.", "Item 31 signature date 110926."])
def test_letter_check_detector_ignores_clinical_numbers(line):
    assert not LC.unmarked_money(line), line


def test_letter_check_passes_a_clean_letter_and_fails_the_money_field_letter():
    clean = "TREATMENT CHRONOLOGY\n\nPain 3/10, 8 visits planned. Discharged after 3 days.\n"
    assert LC.violations(clean, ()) == []
    assert LC.violations(clean + "Item 28 TOTAL CHARGE 33000.\n", ())


# ---------------------------------------------------------------- 1c. end to end: lib10 and lib14, every item accepted
def _lib_client(tmp_path, monkeypatch, lib):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    for k in ("FIXTURE_SET", "ANTHROPIC_API_KEY", "ENABLE_LIVE"):
        monkeypatch.delenv(k, raising=False)
    c = TestClient(create_app(str(tmp_path / "r2.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    tok = c.post("/api/cases", json={"library": lib}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    wait_ready(c, tok)
    return c, tok


@pytest.mark.parametrize("lib,figures", [
    ("case_lib10_eob_ub04_cms1500", ["TOTAL CHARGE", "AMOUNT PAID", "49100", "24F", "18500", "21000"]),
    ("case_lib14_handwritten_chiro_scans", ["TOTAL CHARGE", "AMOUNT PAID", "33000", "24F", "25500", "7500"]),
])
def test_claim_form_figures_never_reach_the_treatment_chronology(tmp_path, monkeypatch, lib, figures):
    c, tok = _lib_client(tmp_path, monkeypatch, lib)
    refused = _accept_all(c, tok)
    for style in ("standard", "oneline"):
        letter = c.get(f"/api/cases/{tok}/export?style={style}").json()["letter_text"]
        head = letter.split(X.CHARGES_TITLE)[0]
        for f in figures:
            assert f not in head, (style, f)
        assert LC.unmarked_money(letter) == [], LC.unmarked_money(letter)
    held = [i for i, r in refused.items() if r.status_code == 422 and r.json()["error"]["detail"]["reason_code"] == "CHARGE_TEXT_IN_ENTRY"]
    assert held, "the claim-form entry is held out (or narrowed to a clean quote), never accepted with its money fields"


def test_lib10_lib14_pass_the_letter_check():
    m = LC.measure([(n, t) for n, t in LC.cases() if n in ("case_lib10_eob_ub04_cms1500", "case_lib14_handwritten_chiro_scans")])
    assert m["value"] == 0, m["per_case"]


# ---------------------------------------------------------------- 2. Bills to request: treating providers and facilities only
def _bills_text(entries, records):
    out = X.build_export(dict(records=records, entries=entries, amounts=[], flags=[], pending_count=0, events=[]))
    return out["internal_notes_text"].split("BILLS TO REQUEST")[1].split("RECORDS NOT IN THE TREATMENT SECTION")[0]


def _rec(n, source, excerpt, date="2026-03-20"):
    return dict(n=n, source=source, date_iso=date, excerpt=excerpt)


@pytest.mark.parametrize("src,exc", [
    ("Pellingham and Rook PLLC, correspondence (letter of protection)", "Letter of protection to Fennimoor Spine Clinic. This firm represents the client for injuries."),
    ("Dunmore Law Offices, correspondence", "We represent the client. Please send records."),
    ("Attorney Hale, demand letter", "Our client was injured in a collision."),
    ("Quoinmere Mutual Health Plan, EOB", "Explanation of benefits. This is not a bill."),
    ("Pennyroy Records Retrieval, 18.001 affidavit", "Affidavit concerning cost and necessity of services."),
])
def test_bills_to_request_never_lists_a_law_firm_or_a_payer(src, exc):
    recs = [_rec(1, "Dr. Hesper Alderton, orthopedics", "Dx: left knee contusion."), _rec(2, src, exc, "2026-03-26")]
    ents = [_entry("Dx: left knee contusion.", "Dx: left knee contusion.", n=1, i="e1"),
            _entry("Letter on the client's injuries.", exc.split(".")[0] + ".", n=2, i="e2")]
    bills = _bills_text(ents, recs)
    assert "Dr. Hesper Alderton" in bills
    for bad in ("Pellingham", "PLLC", "Dunmore", "Hale", "Quoinmere", "Pennyroy"):
        assert bad not in bills, bills


def test_treating_providers_and_facilities_are_still_listed():
    recs = [_rec(1, "Ashgrove Fire-Rescue run report", "Transported to Marrowgate General ED."), _rec(2, "Marrowgate General ED", "Dx: cervical strain."),
            _rec(3, "Fennimoor Spine Clinic, PLLC, visit", "Cervical spasm noted.", "2026-03-27")]
    ents = [_entry("Transported to the ED.", "Transported to Marrowgate General ED.", n=1, i="e1"), _entry("Dx: cervical strain.", "Dx: cervical strain.", n=2, i="e2"),
            _entry("Cervical spasm noted.", "Cervical spasm noted.", n=3, i="e3")]
    bills = _bills_text(ents, recs)
    assert "Ashgrove Fire-Rescue" in bills and "Marrowgate General ED" in bills and "Fennimoor Spine Clinic" in bills


def test_lib11_bills_to_request_lists_the_treaters_not_the_firm(tmp_path, monkeypatch):
    c, tok = _lib_client(tmp_path, monkeypatch, "case_lib11_priors_and_ledger")
    _accept_all(c, tok)
    for style in ("standard", "oneline"):
        notes = c.get(f"/api/cases/{tok}/export?style={style}").json()["internal_notes_text"]
        bills = notes.split("BILLS TO REQUEST")[1].split("RECORDS NOT IN THE TREATMENT SECTION")[0]
        assert "Pellingham" not in bills and "PLLC" not in bills, bills
        assert "Alderton" in bills and "Ashgrove" in bills, bills


# ---------------------------------------------------------------- 3. the held-out hint offers only what clears the hold
def test_hint_texts_do_not_offer_a_summary_only_edit_when_the_quote_states_the_amount():
    w = why.why("CHARGE_TEXT_IN_ENTRY")
    assert "or edit the summary" not in w and "dismiss" in w.lower() and "Billed charges" not in w          # r3: the neutral text makes no claim about where charges are
    quote = CT.message({"excerpt": ["$250.00"], "summary": ["$250.00"]})
    assert "dismiss" in quote.lower() and "quote" in quote.lower()
    quote_only = CT.message({"excerpt": ["$250.00"]})
    assert "summary" in quote_only.lower() and "dismiss" in quote_only.lower()
    summ = CT.message({"summary": ["$250.00"]})
    assert "Edit the summary" in summ and "dismiss" in summ.lower()


def test_export_notes_for_a_held_out_bill_say_dismiss_and_where_the_charges_are():
    exc = "Itemized ledger, statement date 06/15/2026. Office visit $250.00; X-ray $180.00. Total charges $2,740.00."
    amts = [dict(id="a1", record_no=1, cents=25000, cls="charge", raw="$250.00", excerpt=exc, review_status="accepted"),
            dict(id="a2", record_no=1, cents=18000, cls="charge", raw="$180.00", excerpt=exc, review_status="accepted")]
    case = dict(records=[_rec(1, "Fennimoor Spine Clinic, itemized ledger", exc)], entries=[_entry("Itemized ledger with charges.", exc, status="pending")], amounts=amts, flags=[],
                pending_count=0, events=[])
    notes = X.build_export(case)["internal_notes_text"].split("RECORDS NOT IN THE TREATMENT SECTION")[1]
    assert "states a dollar amount" in notes and "or edit the summary" not in notes
    assert "dismiss" in notes.lower() and "Billed charges" in notes


def test_export_notes_for_a_held_out_clinical_entry_offer_quote_and_summary_together():
    case = dict(records=[_rec(1, "Marrowgate General ED", "Dx: cervical strain. ED charge: $3,915.")],
                entries=[_entry("Diagnosis of cervical strain; ED charge $3,915.", "Dx: cervical strain. ED charge: $3,915.", status="pending")], amounts=[], flags=[], pending_count=0, events=[])
    notes = X.build_export(case)["internal_notes_text"].split("RECORDS NOT IN THE TREATMENT SECTION")[1]
    assert "or edit the summary" not in notes and "dismiss" in notes.lower()


def _edit(c, tok, item, **body):
    return _post(c, tok, item, {"action": "edit", **body})


def test_each_remedy_the_hold_offers_actually_clears_it(tmp_path, monkeypatch):
    """lib11 e9 (a ledger whose quote states the amounts): the remedies in the hint are dismiss, or a new quote with a matching summary in one edit."""
    c, tok = _lib_client(tmp_path, monkeypatch, "case_lib11_priors_and_ledger")
    held = [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if "CHARGE_TEXT_IN_ENTRY" in e["reasons"]]
    assert held, "lib11 should keep a held-out ledger entry"
    e = held[0]
    r = _post(c, tok, e["id"], {"action": "accept"})
    assert r.status_code == 422
    msg = r.json()["error"]["message"]
    assert "dismiss" in msg.lower() and "or edit the summary" not in msg
    assert _post(c, tok, e["id"], {"action": "dismiss"}).status_code == 200            # the remedy named in the hint clears the hold
    again = next(x for x in c.get(f"/api/cases/{tok}").json()["entries"] if x["id"] == e["id"])
    assert again["review_status"] == "dismissed"


@pytest.mark.parametrize("body", [
    'Claim lists CPT 99204, 18500, 1 unit; CPT 20610, 21000, 1 unit; CPT 97110, 96 OO, 4 units; total charge 49100; amount paid 0 00.\n'
    'Source [Ex. __ / Bates __]: "Item 28 TOTAL CHARGE 49100. Item 29 AMOUNT PAID 0 00."',                                               # lib10, adjuster round 1
    'Line 1: 092126 to 092326, CPT 98941, 24F 25500, 24G 3. Line 2: 092126 to 092326, CPT 97014, 24F 7500, 24G 3. Item 28 total charge 33000.',    # lib14, adjuster round 1
])
def test_letter_check_fails_the_adjusters_round_one_letters(body):
    """Mutation: the lines the adjuster found in the lib10 and lib14 letters in round 1 are violations of the letter check."""
    letter = "TREATMENT CHRONOLOGY\n\nJuly 14, 2026 — Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)\n" + body + "\n"
    assert LC.violations(letter, [])
