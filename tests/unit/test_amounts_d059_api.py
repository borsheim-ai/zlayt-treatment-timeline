"""D-059 end to end: accept path (named confirm), no batch accept for charges, reclassify refusal, exported total of the adjuster's SYNTHETIC ledger."""
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEDGERS = {n: (ROOT / "tests" / "fixtures" / f"t140_synthetic_ledger_{n}.txt").read_text() for n in ("r1", "r2")}
LEDGER = LEDGERS["r1"]
SCRIPT = {"extract": lambda u: dict(summary="Cervical strain.", excerpt="Dx: cervical strain."), "j1": dict(verdict="supported", reason_code="NONE"),
          "j2": dict(verdict="agree", reason_code="NONE"), "j3": dict(verdict="benign", reason_code="NONE"), "j4": dict(verdict="agree", reason_code="NONE"),
          "conflicts": {"flags": []}, "flags": {"flags": []}}


def make_env(tmp_path, monkeypatch, text):
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")                     # leaves demo mode; the fake call factory means no model is ever started
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    judged = []

    def factory(conn, cid):
        def call(step, system, user, schema, *, item_id=None, validate=None):
            judged.append(step)
            v = SCRIPT[step](user) if callable(SCRIPT[step]) else SCRIPT[step]
            return v, None
        return call
    c = TestClient(create_app(str(tmp_path / "d059.sqlite"), call_factory=factory, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
    tok = c.post("/api/cases", json={"text": text}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(200):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.1)
    assert s["status"] == "ready", s
    return c, tok, judged


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_env(tmp_path, monkeypatch, LEDGER)


def charges(c, tok):
    return [a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["kind"] == "charge"]


def accept_every_amount_one_at_a_time(c, tok, confirm=None):
    g = c.get(f"/api/cases/{tok}").json()
    for it in g["entries"] + g["flags"]:
        c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "dismiss"})
    refused = []
    for a in g["amounts"]:
        if a["kind"] != "damages":
            r = c.post(f"/api/cases/{tok}/items/{a['id']}/review", json={"action": "accept"})
            if r.status_code != 200:
                refused.append(a["id"])
                if confirm:
                    assert c.post(f"/api/cases/{tok}/items/{a['id']}/review", json={"action": "accept", "confirm": confirm}).status_code == 200
    return refused


@pytest.mark.parametrize("name", ["r1", "r2"])
@pytest.mark.parametrize("confirm", [None, "likely_duplicate", "likely_total"])
def test_ledger_letter_total_is_1950_on_every_acceptance_path(tmp_path, monkeypatch, name, confirm):
    """D-060: both adjuster ledgers (SYNTHETIC) export $1,950.00 whether or not a confirm is offered: nothing in them needs one, and no restatement is a charge."""
    c, tok, _ = make_env(tmp_path, monkeypatch, LEDGERS[name])
    assert accept_every_amount_one_at_a_time(c, tok, confirm) == []
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 200, ex.json()
    assert "Billed charges accepted from these records: $1,950.00" in ex.json()["letter_text"].split("\n")
    assert ex.json()["totals"]["charges_cents"] == 195000
    if name == "r1":
        notes = ex.json()["internal_notes_text"]
        for reason in ("Year-to-date or running figure", "Previous statement or balance carried forward", "Reversal, refund, void", "Payment: money received", "Total or subtotal line"):
            assert reason in notes, reason


def test_each_charge_in_the_letter_quotes_its_own_line(tmp_path, monkeypatch):
    """T-140 r3: two different visits at the same price print two different Source lines (the figure's own offset, never the first equal figure)."""
    c, tok, _ = make_env(tmp_path, monkeypatch, LEDGERS["r1"])
    accept_every_amount_one_at_a_time(c, tok)
    letter = c.get(f"/api/cases/{tok}/export").json()["letter_text"]
    quotes = [ln for ln in letter.splitlines() if "$150.00" in ln and ln.lstrip().startswith("Source")]
    assert len(quotes) == len(set(quotes)) == 5, quotes
    for want in ("04/09/2026 therapeutic exercise charge $150.00", "04/16/2026 manual therapy charge $150.00", "05/07/2026 therapeutic exercise charge $150.00",
                 "06/10/2026  Manual therapy  $150.00", "06/24/2026  Manual therapy  $150.00"):
        assert any(want in q for q in quotes), want


def test_charges_are_never_batch_accepted(env):
    c, tok, _ = env
    ch = charges(c, tok)
    entry = c.get(f"/api/cases/{tok}").json()["entries"][0]["id"]
    for ids in ([ch[0]["id"]], [entry, ch[0]["id"]], [a["id"] for a in ch]):
        for action in ("accept", "reset"):
            r = c.post(f"/api/cases/{tok}/review/batch", json={"action": action, "item_ids": ids})
            assert r.status_code == 422 and r.json()["error"]["code"] == "CHARGES_NOT_BATCHED", (ids, r.json())
            assert "one at a time" in r.json()["error"]["message"] and "nothing was changed" in r.json()["error"]["message"].lower()
    assert all(a["review_status"] == "pending" for a in charges(c, tok))


def test_reclassify_cannot_promote_a_figure_a_rule_made_unclear(env):
    c, tok, judged = env
    g = c.get(f"/api/cases/{tok}").json()
    before = len(judged)
    tried = 0
    for a in g["amounts"]:
        if a["kind"] == "unclear" and a["text"] in ("$580.00", "$380.00", "$1,100.00", "$300.00", "$120.00", "$100.00", "$90.00"):
            r = c.post(f"/api/cases/{tok}/items/{a['id']}/reclassify", json={"to": "charge"})
            assert r.status_code == 422 and r.json()["error"]["code"] == "reclassify_refused", (a["text"], r.json())
            assert r.json()["error"]["detail"]["reason"] == "NOT_A_CHARGE_BY_RULE" and r.json()["error"]["detail"]["check"] == "code"
            assert r.json()["error"]["detail"]["rule_reason"] in r.json()["error"]["message"]
            tried += 1
    assert tried >= 6 and len(judged) == before                 # refused before any judge call


# ---------------------------------------------------------------- T-140 r3: a figure promoted to a charge gets the same flags and the same named confirm
NOTE = ("=== Record 1 ===\nDate: 2026-05-01\nSource: Brindlewood Physical Therapy, visit note\nExcerpt: \"04/09/2026 therapeutic exercise invoiced $150.00. "
        "04/16/2026 manual therapy invoiced $150.00.\"\n\n"
        "=== Record 2 ===\nDate: 2026-06-01\nSource: Brindlewood Physical Therapy, visit note\nExcerpt: \"04/16/2026 manual therapy invoiced $150.00. "
        "05/07/2026 evaluation invoiced $210.00.\"\n")


def test_a_promoted_duplicate_is_flagged_and_needs_the_named_confirm(tmp_path, monkeypatch):
    c, tok, _ = make_env(tmp_path, monkeypatch, NOTE)
    g = c.get(f"/api/cases/{tok}").json()
    amts = [a for a in g["amounts"] if a["kind"] != "damages"]
    assert [a["kind"] for a in amts] == ["unclear"] * 4                  # 'invoiced' is not a charge word in a visit note
    for a in amts:
        r = c.post(f"/api/cases/{tok}/items/{a['id']}/reclassify", json={"to": "charge"})
        assert r.status_code == 200, r.json()
    ch = charges(c, tok)
    flagged = [a for a in ch if a["flag"]]
    assert len(ch) == 4 and len(flagged) == 1
    f = flagged[0]
    assert f["flag"]["flag"] == "likely_duplicate" and f["confirm_required"] is True and f["flag"]["of"] != f["id"]
    assert f["flag"]["of"] in {a["id"] for a in ch}
    accept_every_amount_one_at_a_time(c, tok)                               # one at a time, no confirm: the flagged one is refused
    r = c.post(f"/api/cases/{tok}/items/{f['id']}/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "CONFIRM_REQUIRED" and r.json()["error"]["detail"]["flag"] == "likely_duplicate"
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 200, ex.json()
    assert "Billed charges accepted from these records: $510.00" in ex.json()["letter_text"].split("\n")          # the records state $510 of distinct services
    ok = c.post(f"/api/cases/{tok}/items/{f['id']}/review", json={"action": "accept", "confirm": "likely_duplicate"})
    assert ok.status_code == 200 and ok.json()["item"]["flag"]["confirmed_at"]
    assert c.get(f"/api/cases/{tok}").json()["totals"]["flagged_charges"] == []
    assert c.post(f"/api/cases/{tok}/items/{f['id']}/review", json={"action": "dismiss"}).status_code == 200      # a dismiss needs no confirm


def test_demoting_a_promoted_charge_clears_its_flag(tmp_path, monkeypatch):
    c, tok, _ = make_env(tmp_path, monkeypatch, NOTE)
    amts = [a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["kind"] != "damages"]
    for a in amts:
        c.post(f"/api/cases/{tok}/items/{a['id']}/reclassify", json={"to": "charge"})
    f = next(a for a in charges(c, tok) if a["flag"])
    assert c.post(f"/api/cases/{tok}/items/{f['id']}/reclassify", json={"to": "not_a_charge"}).status_code == 200
    got = next(a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["id"] == f["id"])
    assert got["kind"] == "unclear" and got["flag"] is None and got["confirm_required"] is False


def test_notes_quote_the_reversal_sentence_for_the_reversal_figure(tmp_path, monkeypatch):
    """T-140 r3: the internal note for the -$150.00 reversal quotes the reversal, not the earlier charge line that states the same figure."""
    c, tok, _ = make_env(tmp_path, monkeypatch, LEDGERS["r1"])
    accept_every_amount_one_at_a_time(c, tok)
    notes = c.get(f"/api/cases/{tok}/export").json()["internal_notes_text"].split("AMOUNTS NOT TOTALED")[1].split("\n\n")[0]
    line = next(ln for ln in notes.splitlines() if "Reversal of 05/07/2026" in ln)
    assert "Not totaled ($150.00)" in line and "Reversal, refund, void" in line
    assert not any('"05/07/2026 therapeutic exercise charge $150.00' in ln and "Not totaled" in ln for ln in notes.splitlines())
