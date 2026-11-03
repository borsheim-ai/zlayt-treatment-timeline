"""T-171 round 2 (adjuster fail; D-064 amended): the count action must not reopen the overcount paths.
(1) A line is countable only with a service description (CPT / HCPCS / revenue code or a service noun) and when it lacks only a date of service or the bill header.
    Insurer / payer words, allowed amounts, lifetime and running totals, on-account balances and 'amount charged' summaries are not countable, with a plain reason.
(2) An undated countable line that matches an accepted charge or another countable line on service + amount (any record) carries likely_duplicate and needs that
    confirm; `separate_charge` alone is never enough.
(3) The lib15 'amount unpaid ... to be paid' figure says balance, not payment.
The adjuster's pasted-ledger scenarios (artifacts/review-evidence/T-171-adjuster/probe_paste*.py) are restated here as data. Code only (the call factory is scripted)."""
import os
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import amounts as AM
from app.backend.api import create_app

SRC = "Fennimoor Spine Clinic, itemized ledger"
BASE = "Itemized ledger. New patient exam charge $250.00; x-ray charge $180.00; therapy visit charge $400.00."
TRUE = 83000


def nc(excerpt, fig, source=SRC, records=None, date_iso="2026-06-15"):
    a = next(x for x in AM.find_amounts(excerpt) if x["raw"] == fig)
    return AM.not_counted(excerpt, a["raw"], a["cents"], source, date_iso, a["start"], records, "unclear")


# ---------------------------------------------------------------- (1) the pure rule
@pytest.mark.parametrize("line,fig", [
    ("New patient exam charge $250.00.", "$250.00"),
    ("X-ray charge $180.00.", "$180.00"),
    ("Treatment visits 1 through 14 charge $2,310.00.", "$2,310.00"),
    ("CPT 97140 charge $150.00.", "$150.00"),
    ("Rev 0450 emergency room charge $1,640.00.", "$1,640.00"),
    ("HCPCS G0283 charge $60.00.", "$60.00"),
])
def test_an_itemized_service_line_missing_only_the_date_is_countable(line, fig):
    r = nc("Itemized ledger. " + line, fig)
    assert r["countable"] is True, r


@pytest.mark.parametrize("line,fig,word", [
    ("Aetna billed charge $1,100.00.", "$1,100.00", "insurer"),
    ("EOB amount billed $1,100.00.", "$1,100.00", "insurer"),
    ("TPA claim charge $1,100.00.", "$1,100.00", "insurer"),
    ("Plan billed charge $1,100.00.", "$1,100.00", "insurer"),
    ("Payer billed exam charge $1,100.00.", "$1,100.00", "insurer"),
    ("Cigna exam charge $1,100.00.", "$1,100.00", "insurer"),
    ("Allowed charge $600.00.", "$600.00", "allowed"),
    ("Allowed amount for the exam charge $600.00.", "$600.00", "insurer"),
    ("Lifetime charges at this clinic $1,100.00.", "$1,100.00", "lifetime"),
    ("Lifetime exam charges $1,100.00.", "$1,100.00", "lifetime"),
    ("Charges on account $1,100.00.", "$1,100.00", "account"),
    ("Exam charges on account $1,100.00.", "$1,100.00", "account"),
    ("Charge held under letter of protection $1,100.00.", "$1,100.00", "account"),
    ("Amount charged for all visits $1,100.00.", "$1,100.00", "amount charged"),
    ("Amount billed for all treatment visits $1,100.00.", "$1,100.00", "amount charged"),
    ("Charges for the above services came to $1,100.00.", "$1,100.00", "sums charges"),
    ("Charges for these exam and x-ray services came to $1,100.00.", "$1,100.00", "sums charges"),
    ("Total fees charged $1,100.00.", "$1,100.00", "total"),
    ("Amount billed $1,100.00.", "$1,100.00", "amount charged"),
    ("Medicare allowable exam charge $600.00.", "$600.00", "allowed"),
])
def test_insurer_allowed_lifetime_account_and_summary_wordings_are_not_countable_with_a_plain_reason(line, fig, word):
    r = nc(BASE + " " + line, fig)
    assert r["countable"] is False, r
    assert r["reason"] and word in r["reason"].lower(), r


@pytest.mark.parametrize("line", [
    "Charge $1,100.00.", "Charge for services $1,100.00.", "Charges $1,100.00.", "Billed $1,100.00.", "Fee charged $1,100.00.",
])
def test_a_line_with_no_service_description_is_not_countable_and_says_so(line):
    r = nc("Itemized ledger. " + line, "$1,100.00")
    assert r["countable"] is False and "names no service" in r["reason"], r


def test_a_code_alone_is_a_service_description():
    assert nc("Itemized ledger. 97140 charge $150.00.", "$150.00")["countable"] is True


def test_the_same_figure_says_balance_on_every_row_that_carries_it():
    # lib15's affidavit: 'Amount unpaid that the provider has a right to be paid: $2,660.00' is the balance, not a payment received
    ex = ("Affidavit concerning cost and necessity of services (CPRC 18.001). Total amount charged: $2,910.00. Amount paid: $250.00. "
          "Amount unpaid that the provider has a right to be paid: $2,660.00. The services were necessary and the charges reasonable.")
    r = nc(ex, "$2,660.00", source="Pennyroyal Records Retrieval, 18.001 affidavit")
    assert r["countable"] is False and r["reason"].startswith("Balance"), r
    r2 = nc("Itemized statement: exam charge $210.00. Balance due $2,660.00.", "$2,660.00")
    assert r2["reason"].startswith("Balance"), r2
    assert nc("Itemized statement: exam charge $210.00. Payment received $250.00 (med pay).", "$250.00")["reason"].startswith("Payment")


# ---------------------------------------------------------------- the API, with a scripted call factory
SCRIPT = {"extract": lambda u: dict(summary="Cervical strain.", excerpt="Dx: cervical strain."), "extract_es": lambda u: dict(summary="Cervical strain.", excerpt="Dx: cervical strain."),
          "j1": dict(verdict="supported", reason_code="NONE"), "j2": dict(verdict="agree", reason_code="NONE"), "j3": dict(verdict="benign", reason_code="NONE"),
          "j4": dict(verdict="agree", reason_code="NONE"), "conflicts": {"flags": []}, "flags": {"flags": []}}


def factory(conn, cid):
    def call(step, system, user, schema, *, item_id=None, validate=None):
        v = SCRIPT[step](user) if callable(SCRIPT[step]) else SCRIPT[step]
        return v, None
    return call


@pytest.fixture
def live(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    n = {"i": 0}

    def make(text):
        n["i"] += 1
        c = TestClient(create_app(str(tmp_path / f"r2_{n['i']}.sqlite"), call_factory=factory, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
        tok = c.post("/api/cases", json={"text": text}).json()["token"]
        assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
        for _ in range(400):
            s = c.get(f"/api/cases/{tok}/status").json()
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(0.05)
        assert s["status"] == "ready", s
        return c, tok
    return make


def doc(*recs):
    out = ["SYNTHETIC - invented for evaluation; not real patient data", ""]
    for i, (date, src, ex) in enumerate(recs, 1):
        out += [f"=== Record {i} ===", f"Date: {date}", f"Source: {src}", f'Excerpt: "{ex}"', ""]
    return "\n".join(out)


def single(extra):
    return doc(("2026-06-15", SRC, BASE + " " + extra))


def amounts(c, tok):
    return c.get(f"/api/cases/{tok}").json()["amounts"]


def post(c, tok, aid, **body):
    return c.post(f"/api/cases/{tok}/items/{aid}/review", json=body)


def accepted_cents(c, tok):
    return c.get(f"/api/cases/{tok}").json()["totals"]["accepted"]["cents"]


def count_all(c, tok):
    """Path A: the paralegal clicks 'Count this charge' with the named confirm only, on every amount that is not already a charge; then accepts what the code detected."""
    counted, refused = [], []
    for a in amounts(c, tok):
        if a["kind"] == "charge":
            continue
        r = post(c, tok, a["id"], action="count", confirm="separate_charge")
        (counted if r.status_code == 200 else refused).append((a["text"], r.status_code, (r.json().get("error") or {}).get("code")))
    for a in amounts(c, tok):
        if a["kind"] == "charge" and a["review_status"] != "accepted":
            r = post(c, tok, a["id"], action="accept")
            if r.status_code == 422:
                post(c, tok, a["id"], action="accept", confirm=r.json()["error"]["detail"].get("confirm_with"))
    return counted, refused


WORDS = {
    "total_sum_of_charges": "Sum of charges {x}.", "total_charges_to_date": "Charges to date {x}.", "total_grand": "Grand total charge {x}.", "total_billed": "Total billed {x}.",
    "total_fees": "Total fees charged {x}.", "total_in_words": "Charges for the above services came to {x}.", "total_amount_charged": "Amount charged for all visits {x}.",
    "balance_outstanding": "Outstanding charge {x}.", "balance_remaining": "Remaining charge {x}.", "balance_net": "Net charge after credits {x}.",
    "balance_pt_resp": "Patient responsibility charge {x}.", "balance_lop_hold": "Charge held under letter of protection {x}.", "ytd_cumulative": "Cumulative charges {x}.",
    "ytd_lifetime": "Lifetime charges at this clinic {x}.", "ytd_account": "Charges on account {x}.", "insurer_medpay": "Med pay charge {x}.",
    "insurer_plan_billed": "Plan billed charge {x}.", "ytd_plain": "Year to date charges {x}.", "insurer_aetna": "Aetna billed charge {x}.", "eob_in_ledger": "EOB amount billed {x}.",
    "tpa": "TPA claim charge {x}.", "pip": "PIP charge {x}.",
}
SCEN = {}
for _fig, _tag in (("$830.00", "match"), ("$1,100.00", "nonmatch")):
    for _k, _w in WORDS.items():
        SCEN[f"{_k}_{_tag}"] = (single(_w.format(x=_fig)), TRUE)
SCEN["insurer_allowed"] = (single("Allowed charge $600.00."), TRUE)
SCEN["pay_applied"] = (single("Insurance payment applied to charge $300.00."), TRUE)
SCEN["pay_copay"] = (single("Copay charge collected $50.00."), TRUE)
SCEN["rate_per_visit"] = (single("Charge per visit $200.00."), TRUE)
SCEN["est_future"] = (single("Estimated future charge $5,000.00."), TRUE)
SCEN["sum_charge_word_after"] = (single("The three charges above sum to $830.00."), TRUE)
SCEN["subtotal_page"] = (single("Page 1 subtotal charge $830.00."), TRUE)
SCEN["carried_forward"] = (single("Charge carried forward from prior page $830.00."), TRUE)
SCEN["restated_service"] = (single("New patient exam charge $250.00 (restated)."), TRUE)
SCEN["reprint_two_records"] = (doc(("2026-06-15", SRC, BASE), ("2026-06-30", SRC + " (reprint)", BASE)), TRUE)
SCEN["reprint_note_restates"] = (doc(("2026-06-15", SRC, BASE), ("2026-06-30", "Fennimoor Spine Clinic, discharge summary",
                                                                  "Discharged. New patient exam charge $250.00; x-ray charge $180.00; therapy visit charge $400.00.")), TRUE)
SCEN["dated_then_undated"] = (doc(("2026-04-16", "Clinic, billing statement", "Billing statement. 04/16/2026 manual therapy charge $150.00."),
                                  ("2026-05-01", "", "Manual therapy charge $150.00.")), 15000)
SCEN["dated_then_undated_nosource"] = (doc(("2026-04-16", "Clinic, billing statement", "Billing statement. 04/16/2026 manual therapy charge $150.00."),
                                           ("2026-05-01", "", "04/16/2026 manual therapy charge $150.00.")), 15000)
SCEN["note_total_no_header"] = (doc(("2026-06-15", "Fennimoor Spine Clinic, progress note", "Visit 3. Exam charge $250.00. Total charge to date for all visits $830.00.")), 25000)
SCEN["note_two_figs"] = (doc(("2026-06-15", "Clinic, progress note", "Exam charge $250.00 and x-ray charge $180.00, together a charge of $430.00.")), 43000)
SCEN["no_source_total"] = (doc(("2026-06-15", "", "Exam charge $250.00. X-ray charge $180.00. Charge total $430.00.")), 43000)
SCEN["no_source_balance"] = (doc(("2026-06-15", "", "Exam charge $250.00. Payment $100.00. Charge still owed $150.00.")), 25000)
SCEN["no_source_credit"] = (doc(("2026-06-15", "", "Exam charge $250.00. Charge reversed $250.00.")), 25000)      # the exam charge was billed; the reversal is a credit


@pytest.mark.parametrize("name", sorted(SCEN))
def test_pasted_ledger_scenario_never_totals_more_than_the_distinct_services_stated(live, name):
    text, truth = SCEN[name]
    c, tok = live(text)
    count_all(c, tok)
    for it in c.get(f"/api/cases/{tok}").json()["entries"]:
        post(c, tok, it["id"], action="accept")
    assert accepted_cents(c, tok) <= truth, (name, accepted_cents(c, tok), truth, [(a["text"], a["kind"], a["countable"], a["not_counted_reason"]) for a in amounts(c, tok)])


@pytest.mark.parametrize("name", sorted(k for k in SCEN if k.endswith("_nonmatch") or k in ("insurer_allowed", "pay_applied", "pay_copay", "rate_per_visit", "est_future")))
def test_the_extra_figure_is_not_countable_says_why_and_is_refused(live, name):
    text, _ = SCEN[name]
    c, tok = live(text)
    extra = [a for a in amounts(c, tok) if a["text"] not in ("$250.00", "$180.00", "$400.00")]
    assert extra, name
    for a in extra:
        assert a["countable"] is False and a["not_counted_reason"], (name, a["text"], a["not_counted_reason"])
        r = post(c, tok, a["id"], action="count", confirm="separate_charge")
        assert r.status_code == 422 and r.json()["error"]["code"] == "NOT_COUNTABLE", (name, a["text"], r.text)


# ---------------------------------------------------------------- (2) the undated duplicate
def _flag(r):
    assert r.status_code == 422, r.text
    e = r.json()["error"]
    assert e["code"] == "CONFIRM_REQUIRED", e
    return e["detail"]


def test_an_undated_repeat_of_an_accepted_dated_charge_needs_the_duplicate_confirm(live):
    text, _ = SCEN["dated_then_undated"]
    c, tok = live(text)
    am = amounts(c, tok)
    first = next(a for a in am if a["kind"] == "charge")
    twin = next(a for a in am if a["kind"] != "charge")
    assert post(c, tok, first["id"], action="accept").status_code == 200
    twin = next(a for a in amounts(c, tok) if a["id"] == twin["id"])
    assert twin["countable"] is True and twin["count_confirm"]["flag"] == "likely_duplicate" and twin["count_confirm"]["of"] == first["id"], twin
    d = _flag(post(c, tok, twin["id"], action="count", confirm="separate_charge"))
    assert d["flag"] == "likely_duplicate" and d["confirm_with"] == "likely_duplicate" and d["of"] == first["id"], d
    assert next(a for a in amounts(c, tok) if a["id"] == twin["id"])["kind"] == "unclear"
    assert accepted_cents(c, tok) == 15000
    ok = post(c, tok, twin["id"], action="count", confirm="separate_charge", confirm_flag="likely_duplicate")        # she says it is a separate visit
    assert ok.status_code == 200 and accepted_cents(c, tok) == 30000


@pytest.mark.parametrize("name", ["reprint_two_records", "reprint_note_restates", "restated_service"])
def test_a_reprint_or_restatement_without_dates_needs_the_duplicate_confirm_on_each_matching_line(live, name):
    text, truth = SCEN[name]
    c, tok = live(text)
    flagged = 0
    for a in amounts(c, tok):
        if a["kind"] == "charge" or not a["countable"]:
            continue
        if a["count_confirm"]:
            flagged += 1
            d = _flag(post(c, tok, a["id"], action="count", confirm="separate_charge"))
            assert d["flag"] == "likely_duplicate" and d["of"] and d["of"] != a["id"], d
    assert flagged >= (1 if name == "restated_service" else 3), (name, flagged)


def test_a_repeat_inside_one_record_is_flagged_on_both_lines_and_counting_one_then_the_other_asks_again(live):
    text, _ = SCEN["restated_service"]
    c, tok = live(text)
    twins = [a for a in amounts(c, tok) if a["text"] == "$250.00"]
    assert len(twins) == 2 and all(t["countable"] and t["count_confirm"]["flag"] == "likely_duplicate" for t in twins), twins
    assert post(c, tok, twins[0]["id"], action="count", confirm="separate_charge", confirm_flag="likely_duplicate").status_code == 200
    d = _flag(post(c, tok, twins[1]["id"], action="count", confirm="separate_charge"))
    assert d["flag"] == "likely_duplicate" and d["of"] == twins[0]["id"], d


def test_a_line_with_no_match_still_counts_with_only_the_named_confirm(live):
    text, _ = SCEN["no_source_total"]
    c, tok = live(text)
    ex = next(a for a in amounts(c, tok) if a["text"] == "$250.00")
    assert ex["countable"] is True and ex["count_confirm"] is None, ex
    assert post(c, tok, ex["id"], action="count", confirm="separate_charge").status_code == 200


def test_two_different_services_at_one_price_are_not_flagged(live):
    c, tok = live(doc(("2026-06-15", SRC, "Itemized ledger. Exam charge $200.00; x-ray charge $200.00.")))
    am = [a for a in amounts(c, tok) if a["countable"]]
    assert len(am) == 2 and all(a["count_confirm"] is None for a in am), am


def test_dated_lines_of_different_days_at_one_price_are_not_flagged(live):
    c, tok = live(doc(("2026-06-15", "", "04/16/2026 therapy visit charge $400.00. 05/16/2026 therapy visit charge $400.00.")))
    am = [a for a in amounts(c, tok) if a["countable"]]
    assert am and all(a["count_confirm"] is None for a in am), am


# ---------------------------------------------------------------- the library with Path A only
LIB = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "library")
LIBRARY = sorted(p[:-4] for p in os.listdir(LIB) if p.startswith("case_") and p.endswith(".txt"))


@pytest.fixture
def libclient(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.setenv("ZLAYT_MODE", "local")
    return TestClient(create_app(str(tmp_path / "r2lib.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


@pytest.mark.parametrize("case", LIBRARY)
def test_library_counting_with_only_the_named_confirm_stays_within_the_hand_total(libclient, case):
    import json
    exp = round(json.loads(open(os.path.join(LIB, f"{case}.expected.json")).read())["totals"]["explicit_charges_total"] * 100)
    c = libclient
    tok = c.post("/api/cases", json={"library": case}).json()["token"]
    c.post(f"/api/cases/{tok}/run", json={})
    for _ in range(400):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
            break
        time.sleep(0.05)
    count_all(c, tok)
    assert accepted_cents(c, tok) <= exp, (case, accepted_cents(c, tok), exp)


def test_lib11_still_counts_to_6000(libclient):
    c = libclient
    tok = c.post("/api/cases", json={"library": "case_lib11_priors_and_ledger"}).json()["token"]
    c.post(f"/api/cases/{tok}/run", json={})
    for _ in range(400):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
            break
        time.sleep(0.05)
    for fig in ("$250.00", "$180.00", "$2,310.00"):
        a = next(x for x in amounts(c, tok) if x["text"] == fig)
        assert a["countable"] is True and a["count_confirm"] is None, a
        assert post(c, tok, a["id"], action="count", confirm="separate_charge").status_code == 200
    for a in amounts(c, tok):
        if a["kind"] == "charge" and a["review_status"] != "accepted":
            post(c, tok, a["id"], action="accept")
    assert accepted_cents(c, tok) == 600000


@pytest.mark.parametrize("name", sorted(k for k in SCEN if k.endswith(("_match", "_nonmatch")) or k in (
    "insurer_allowed", "pay_applied", "pay_copay", "rate_per_visit", "est_future", "sum_charge_word_after", "subtotal_page", "carried_forward")))
def test_the_three_distinct_services_still_count_to_exactly_830_when_the_extra_line_is_refused(live, name):
    text, truth = SCEN[name]
    c, tok = live(text)
    counted, _ = count_all(c, tok)
    assert [t[0] for t in counted] == ["$250.00", "$180.00", "$400.00"], (name, counted)
    assert accepted_cents(c, tok) == truth == TRUE
