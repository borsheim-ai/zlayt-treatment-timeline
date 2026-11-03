"""T-171 (D-064, GATE-M2 r2 paralegal major): every amount that is not counted says why in a plain sentence and says whether the paralegal may count it
(`not_counted_reason`, `countable`). Rule-excluded amounts (total, balance, payment, adjustment/credit, year-to-date, insurer restatement, a note that restates
the same provider's bill, a second figure on a line) are never countable. An amount held back only for a missing detail (no date of service, a document with no
bill header) is countable: `POST .../review {action: "count", confirm: "separate_charge"}` makes it an accepted charge and writes an audit event naming the confirm.
lib11: counting the three ledger lines gives a letter total of $6,000.00. Code only."""
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import amounts as AM
from app.backend.api import create_app

ROOT = pathlib.Path(__file__).resolve().parents[2]
LIB11 = ROOT / "evals" / "library" / "case_lib11_priors_and_ledger.txt"
LEDGER = ("Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; "
          "total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.")
SRC = "Fennimoor Spine Clinic, itemized ledger"


def nc(excerpt, raw, source=SRC, records=None, date_iso="2026-06-15", kind="unclear"):
    a = next(x for x in AM.find_amounts(excerpt) if x["raw"] == raw)
    return AM.not_counted(excerpt, a["raw"], a["cents"], source, date_iso, a["start"], records, kind)


# ---------------------------------------------------------------- the pure rule
def test_ledger_lines_missing_a_date_are_countable_and_say_so():
    for fig in ("$250.00", "$180.00", "$2,310.00"):
        r = nc(LEDGER, fig)
        assert r["countable"] is True and "no date of service" in r["reason"].lower(), (fig, r)


def test_rule_excluded_ledger_figures_are_never_countable_and_say_why():
    want = {"$2,740.00": "repeats", "$300.00": "payment", "$274.00": "adjustment", "$2,166.00": "balance"}
    for fig, word in want.items():
        r = nc(LEDGER, fig)
        assert r["countable"] is False and word in r["reason"].lower(), (fig, r)


@pytest.mark.parametrize("excerpt,fig", [
    ("04/16/2026 office visit charge $100.00. Year-to-date charges $4,800.00.", "$4,800.00"),
    ("Itemized ledger. 04/16/2026 visit charge $100.00; credit memo $50.00.", "$50.00"),
    ("Itemized ledger. 04/16/2026 visit charge $100.00; refund (courtesy) $20.00.", "$20.00"),
    ("Itemized ledger. 04/16/2026 visit charge $100.00; previous balance $900.00.", "$900.00"),
    ("Itemized ledger. 04/16/2026 visit charge $100.00; balance forward $900.00.", "$900.00"),
])
def test_other_rule_labels_are_never_countable(excerpt, fig):
    r = nc(excerpt, fig)
    assert r["countable"] is False and r["reason"], r


def test_insurer_restatement_is_never_countable():
    ex = "Explanation of benefits. 04/16/2026 office visit amount billed $150.00. Plan paid $90.00."
    r = nc(ex, "$150.00", source="Great Plains Mutual, EOB")
    assert r["countable"] is False and "insurer" in r["reason"].lower(), r


def test_a_clinical_note_that_restates_the_same_providers_bill_is_not_countable():
    bill = {"n": 1, "source": "Brindlewood Physical Therapy, billing statement", "excerpt": "04/16/2026 manual therapy charge $150.00.", "text": "x", "date_iso": "2026-04-16"}
    note = {"n": 2, "source": "Brindlewood Physical Therapy, discharge summary", "excerpt": "Discharged. Manual therapy charge $150.00.", "text": "y", "date_iso": "2026-04-20"}
    r = nc(note["excerpt"], "$150.00", source=note["source"], records=[bill, note], date_iso="2026-04-20")
    assert r["countable"] is False and "bill" in r["reason"].lower(), r


def test_a_second_figure_on_a_service_line_is_not_countable():
    ex = "Itemized statement. 04/16/2026 office visit charge $150.00, deductible $500.00."
    r = nc(ex, "$500.00", source="Clinic, itemized statement")
    assert r["countable"] is False and r["reason"], r


def test_a_document_with_no_bill_header_stating_a_dated_charge_is_countable():
    ex = "04/16/2026 office visit charge $150.00."
    rec = {"n": 1, "source": "", "excerpt": ex, "text": ex, "date_iso": "2026-04-16"}
    r = nc(ex, "$150.00", source="", records=[rec], date_iso="2026-04-16")
    assert r["countable"] is True and "header" in r["reason"].lower(), r


@pytest.mark.parametrize("kind", ["rate", "estimate", "damages"])
def test_rates_estimates_and_damages_say_why_and_are_not_countable(kind):
    r = nc("Visit rate $185 per visit.", "$185", kind=kind)
    assert r["countable"] is False and r["reason"] and r["reason"][0].isupper() and r["reason"].endswith("."), r


def test_a_charge_has_no_reason_and_nothing_to_count():
    r = nc("04/16/2026 office visit charge $150.00.", "$150.00", source="Clinic, billing statement", kind="charge")
    assert r == {"reason": None, "countable": False}


# ---------------------------------------------------------------- the API
@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.setenv("ZLAYT_MODE", "local")
    return TestClient(create_app(str(tmp_path / "t171.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def run_case(c, **body):
    tok = c.post("/api/cases", json=body).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready", s
    return tok


@pytest.fixture
def lib11(client):
    tok = run_case(client, library=LIB11.stem)
    return client, tok


def by_text(c, tok):
    return {a["text"]: a for a in c.get(f"/api/cases/{tok}").json()["amounts"]}


def count(c, tok, aid, **body):
    return c.post(f"/api/cases/{tok}/items/{aid}/review", json={"action": "count", **body})


def test_every_amount_that_is_not_counted_carries_a_plain_reason_and_countable(lib11):
    c, tok = lib11
    am = by_text(c, tok)
    for a in am.values():
        if a["kind"] == "charge":
            assert a["not_counted_reason"] is None
        else:
            assert isinstance(a["countable"], bool) and a["not_counted_reason"] and a["not_counted_reason"].endswith("."), a
            assert "not a bill" not in a["not_counted_reason"] and "could not be read or labelled" not in a["not_counted_reason"]
            assert a["not_counted_reason"] in a["why"]                          # the screen's "why this status" gives the same sentence
    for fig in ("$250.00", "$180.00", "$2,310.00"):
        assert am[fig]["countable"] is True and "no date of service" in am[fig]["not_counted_reason"].lower(), fig
    for fig in ("$2,740.00", "$300.00", "$274.00", "$2,166.00"):
        assert am[fig]["countable"] is False, fig
    assert "repeats" in am["$2,740.00"]["not_counted_reason"]


def test_count_needs_the_named_confirm_and_changes_nothing_without_it(lib11):
    c, tok = lib11
    a = by_text(c, tok)["$250.00"]
    n_events = len(c.get(f"/api/cases/{tok}/audit").json()["events"])
    for body in ({}, {"confirm": "yes"}, {"confirm": "likely_duplicate"}, {"confirm": 5}):
        r = count(c, tok, a["id"], **body)
        assert r.status_code in (400, 422), body
        if r.status_code == 422 and body.get("confirm") != 5:
            err = r.json()["error"]
            assert err["code"] == "CONFIRM_REQUIRED" and err["detail"]["confirm_with"] == "separate_charge", err
            assert "separate charge" in err["message"].lower()
    after = by_text(c, tok)["$250.00"]
    assert after["kind"] == "unclear" and after["review_status"] == "pending"
    assert len(c.get(f"/api/cases/{tok}/audit").json()["events"]) == n_events


@pytest.mark.parametrize("fig", ["$2,740.00", "$300.00", "$274.00", "$2,166.00"])
def test_a_rule_excluded_amount_is_refused_422_with_its_reason(lib11, fig):
    c, tok = lib11
    a = by_text(c, tok)[fig]
    r = count(c, tok, a["id"], confirm="separate_charge")
    assert r.status_code == 422, r.text
    err = r.json()["error"]
    assert err["code"] == "NOT_COUNTABLE" and a["not_counted_reason"] in err["message"], err
    assert by_text(c, tok)[fig]["kind"] == "unclear"
    assert c.get(f"/api/cases/{tok}").json()["totals"]["accepted"]["cents"] == 0


def test_counting_the_three_ledger_lines_gives_the_letter_total_of_6000(lib11):
    c, tok = lib11
    am = by_text(c, tok)
    ed = next(a for a in am.values() if a["kind"] == "charge")                    # the $3,260 ED charge, accepted one at a time
    assert c.post(f"/api/cases/{tok}/items/{ed['id']}/review", json={"action": "accept"}).status_code == 200
    for fig in ("$250.00", "$180.00", "$2,310.00"):
        r = count(c, tok, am[fig]["id"], confirm="separate_charge")
        assert r.status_code == 200, r.text
        item = r.json()["item"]
        assert item["kind"] == "amount" and item["review_status"] == "accepted"
        assert r.json()["totals"]["accepted"]["count"] >= 1
    after = by_text(c, tok)
    assert [after[f]["kind"] for f in ("$250.00", "$180.00", "$2,310.00")] == ["charge"] * 3
    assert all(after[f]["review_status"] == "accepted" and after[f]["not_counted_reason"] is None for f in ("$250.00", "$180.00", "$2,310.00"))
    assert c.get(f"/api/cases/{tok}").json()["totals"]["accepted"]["cents"] == 600000
    for fig in ("$2,740.00", "$300.00", "$274.00", "$2,166.00"):                  # kept in the notes, one at a time, as before
        assert c.post(f"/api/cases/{tok}/items/{am[fig]['id']}/review", json={"action": "accept", "compared": True}).status_code == 200
    for it in c.get(f"/api/cases/{tok}").json()["entries"]:
        c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "accept"})
    ex = c.get(f"/api/cases/{tok}/export").json()
    assert "Billed charges accepted from these records: $6,000.00" in ex["letter_text"].split("\n"), ex["letter_text"][-400:]
    assert ex["totals"]["charges_cents"] == 600000
    for fig in ("$2,740", "$300.00", "$274", "$2,166"):
        assert fig not in ex["letter_text"], fig                                  # no overcount path reopened
    assert "Not totaled ($2,740" in ex["internal_notes_text"]
    assert "Not totaled ($250" not in ex["internal_notes_text"]


def test_counting_is_in_the_audit_trail_with_the_named_confirm(lib11):
    c, tok = lib11
    a = by_text(c, tok)["$180.00"]
    assert count(c, tok, a["id"], confirm="separate_charge").status_code == 200
    ev = [e for e in c.get(f"/api/cases/{tok}/audit").json()["events"] if e["item_id"] == a["id"]]
    confirms = [e["confirm"] for e in ev if e.get("confirm")]
    assert any(x["flag"] == "separate_charge" and x["confirmed_at"] for x in confirms), ev
    assert any(e["action"] == "accept" for e in ev)
    counted = [e for e in ev if (e.get("after") or {}).get("event") == "count"]
    assert counted and counted[0]["after"]["confirm"]["flag"] == "separate_charge" and counted[0]["before"]["kind"] == "unclear", ev


def test_counting_a_charge_that_is_already_a_charge_is_refused(lib11):
    c, tok = lib11
    ed = next(a for a in by_text(c, tok).values() if a["kind"] == "charge")
    r = count(c, tok, ed["id"], confirm="separate_charge")
    assert r.status_code == 422 and r.json()["error"]["code"] == "NOT_COUNTABLE"


def test_after_a_reset_the_counted_charge_needs_its_confirm_again(lib11):
    c, tok = lib11
    a = by_text(c, tok)["$250.00"]
    assert count(c, tok, a["id"], confirm="separate_charge").status_code == 200
    assert c.post(f"/api/cases/{tok}/items/{a['id']}/review", json={"action": "reset"}).status_code == 200
    r = c.post(f"/api/cases/{tok}/items/{a['id']}/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["detail"]["flag"] == "separate_charge", r.text
    assert c.post(f"/api/cases/{tok}/items/{a['id']}/review", json={"action": "accept", "confirm": "separate_charge"}).status_code == 200
    assert c.get(f"/api/cases/{tok}").json()["totals"]["accepted"]["cents"] == 25000


def test_a_dismissed_amount_stays_out_until_counted_and_reclassify_still_refuses_rule_amounts(lib11):
    c, tok = lib11
    am = by_text(c, tok)
    r = c.post(f"/api/cases/{tok}/items/{am['$2,740.00']['id']}/reclassify", json={"to": "charge"})
    assert r.status_code == 422 and r.json()["error"]["detail"]["reason"] == "NOT_A_CHARGE_BY_RULE"
    assert c.post(f"/api/cases/{tok}/items/{am['$300.00']['id']}/review", json={"action": "accept", "confirm": "separate_charge", "compared": True}).status_code == 200   # accept stays "keep in notes"; D-066: the second check disagreed
    assert by_text(c, tok)["$300.00"]["kind"] == "unclear"


SCRIPT = {"extract": lambda u: dict(summary="Manual therapy.", excerpt="Manual therapy."), "j1": dict(verdict="supported", reason_code="NONE"),
          "j2": dict(verdict="agree", reason_code="NONE"), "j3": dict(verdict="benign", reason_code="NONE"), "j4": dict(verdict="agree", reason_code="NONE"),
          "conflicts": {"flags": []}, "flags": {"flags": []}}


def live_env(tmp_path, monkeypatch, text):
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")                     # leaves demo mode; the fake call factory means no model is ever started
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    def factory(conn, cid):
        def call(step, system, user, schema, *, item_id=None, validate=None):
            v = SCRIPT[step](user) if callable(SCRIPT[step]) else SCRIPT[step]
            return v, None
        return call
    c = TestClient(create_app(str(tmp_path / "t171live.sqlite"), call_factory=factory, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    return c, run_case(c, text=text)


DUP = ("SYNTHETIC - invented for evaluation; not real patient data\n\n"
       "=== Record 1 ===\nDate: 2026-04-16\nSource: Clinic, billing statement\nExcerpt: \"Billing statement. 04/16/2026 manual therapy charge $150.00.\"\n\n"
       "=== Record 2 ===\nDate: 2026-05-01\nSource:\nExcerpt: \"04/16/2026 manual therapy charge $150.00.\"\n")


def test_counting_a_duplicate_of_another_charge_also_needs_that_flag_named(tmp_path, monkeypatch):
    c, tok = live_env(tmp_path, monkeypatch, DUP)
    am = c.get(f"/api/cases/{tok}").json()["amounts"]
    first = next(a for a in am if a["kind"] == "charge")
    twin = next(a for a in am if a["kind"] != "charge")
    assert twin["countable"] is True and "header" in twin["not_counted_reason"].lower(), am
    r = count(c, tok, twin["id"], confirm="separate_charge")
    assert r.status_code == 422, r.text
    err = r.json()["error"]
    assert err["code"] == "CONFIRM_REQUIRED" and err["detail"]["flag"] == "likely_duplicate" and err["detail"]["of"] == first["id"], err
    assert next(a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["id"] == twin["id"])["kind"] == "unclear"
    assert count(c, tok, twin["id"], confirm="separate_charge", confirm_flag="wrong").status_code == 422
    ok = count(c, tok, twin["id"], confirm="separate_charge", confirm_flag="likely_duplicate")
    assert ok.status_code == 200, ok.text
    ev = [e for e in c.get(f"/api/cases/{tok}/audit").json()["events"] if e["item_id"] == twin["id"]]
    assert any((e.get("after") or {}).get("event") == "count" and e["after"]["confirm"]["flag"] == "separate_charge" for e in ev)
    assert any(e.get("confirm", {}).get("flag") == "likely_duplicate" for e in ev), ev          # the accept event names the duplicate flag she confirmed


def test_a_counted_charge_needs_no_second_check_and_blocks_no_export(lib11, monkeypatch):
    c, tok = lib11
    a = by_text(c, tok)["$250.00"]
    assert count(c, tok, a["id"], confirm="separate_charge").status_code == 200
    v = next(x for x in c.get(f"/api/cases/{tok}").json()["amounts"] if x["id"] == a["id"])
    assert v["second_check_pending"] is False and v["judge_required_for_export"] is False and "counted this line" in v["why"]
    tr = c.get(f"/api/cases/{tok}/items/{a['id']}/trace")
    assert tr.status_code == 200, tr.text
    steps = {s["id"]: s for s in tr.json()["steps"]}
    assert steps["judge_2"]["status"] == "skipped" and "confirmed it by name" in steps["judge_2"]["why"]
    assert steps["total_inclusion"]["status"] == "pass" and steps["charge_flag"]["status"] == "pass"
    assert c.get(f"/api/cases/{tok}/judges").status_code == 200


def test_a_rerun_keeps_a_counted_charge(lib11):
    c, tok = lib11
    a = by_text(c, tok)["$2,310.00"]
    assert count(c, tok, a["id"], confirm="separate_charge").status_code == 200
    assert c.post(f"/api/cases/{tok}/run", json={"confirm_rerun": True}).status_code == 202
    for _ in range(240):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    after = by_text(c, tok)["$2,310.00"]
    assert after["kind"] == "charge" and after["review_status"] == "accepted", after


# ---------------------------------------------------------------- no overcount path: counting every countable amount never passes the hand-verified total
LIBRARY = sorted(p.stem for p in (ROOT / "evals" / "library").glob("case_*.txt"))


@pytest.mark.parametrize("case", LIBRARY)
def test_library_counting_every_countable_amount_never_exceeds_the_hand_verified_total(client, case):
    import json
    exp = json.loads((ROOT / "evals" / "library" / f"{case}.expected.json").read_text())["totals"]["explicit_charges_total"]
    tok = run_case(client, library=case)
    am = client.get(f"/api/cases/{tok}").json()["amounts"]
    total = sum(a["value_cents"] for a in am if a["kind"] == "charge") + sum(a["value_cents"] for a in am if a["countable"])
    assert total <= round(exp * 100), [(a["text"], a["not_counted_reason"]) for a in am if a["countable"]]
    for a in am:
        assert (a["kind"] == "charge") == (a["not_counted_reason"] is None), a["text"]


def test_a_spanish_saldo_and_a_line_with_a_payment_word_are_not_countable():
    ex = "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00."
    assert nc(ex, "$2,900.00", source="Fennimoor Spine Clinic, estado de cuenta")["countable"] is False
    ex2 = "Itemized ledger. Office exam charge $250.00, payment received $100.00."
    r = nc(ex2, "$250.00")
    assert r["countable"] is False and "payment" in r["reason"].lower(), r
    r = nc("Itemized ledger. Lab work $75.00.", "$75.00")          # no charge word in the line: not countable
    assert r["countable"] is False and "charged or billed" in r["reason"], r
