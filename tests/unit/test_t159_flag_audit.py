"""T-159 (D-059 audit trail of a flagged charge): the named confirm is in the review event (GET /audit, also in public mode), the item trace has a charge_flag step,
the flag sentence is plain words (no internal id, no token), and a repeat accept of a charge already accepted with its flag confirmed is a no-op."""
import re

import pytest
from fastapi.testclient import TestClient

from tests.unit.test_amounts_d059_api import NOTE, charges, make_env


@pytest.fixture
def promoted(tmp_path, monkeypatch):
    """NOTE: four unclear figures promoted to charges one by one; the second 04/16 manual therapy $150.00 (record 2) is a likely_duplicate of the one in record 1."""
    c, tok, _ = make_env(tmp_path, monkeypatch, NOTE)
    for a in [a for a in c.get(f"/api/cases/{tok}").json()["amounts"] if a["kind"] != "damages"]:
        assert c.post(f"/api/cases/{tok}/items/{a['id']}/reclassify", json={"to": "charge"}).status_code == 200
    f = next(a for a in charges(c, tok) if a["flag"])
    return c, tok, f


def review(c, tok, item, **body):
    return c.post(f"/api/cases/{tok}/items/{item}/review", json={"action": "accept", **body})


def accept_events(c, tok, item):
    return [e for e in c.get(f"/api/cases/{tok}/audit").json()["events"] if e["item_id"] == item and e["action"] == "accept"]


def steps(c, tok, item):
    return {s["id"]: s for s in c.get(f"/api/cases/{tok}/items/{item}/trace").json()["steps"]}


# ---------------------------------------------------------------- the sentence
def test_the_duplicate_sentence_names_the_other_line_not_its_id(promoted):
    c, tok, f = promoted
    msg = f["flag"]["message"]
    assert not re.search(r"\b[aeqf]\d+\b", msg), msg
    assert "04/16/2026 manual therapy invoiced $150.00." in msg and "record 1" in msg           # service, amount, date, record: the other charge's own line
    assert "Counting both would count one service twice." in msg
    assert f["flag"]["of"] and f["flag"]["of"] != f["id"]                                      # the id is still there for a client that wants to jump to it, not in the words


def test_confirm_required_carries_the_flags_own_sentence_without_the_token(promoted):
    c, tok, f = promoted
    r = review(c, tok, f["id"])
    err = r.json()["error"]
    assert r.status_code == 422 and err["code"] == "CONFIRM_REQUIRED"
    assert err["detail"]["message"] == f["flag"]["message"]
    assert "likely_duplicate" not in err["detail"]["message"] and "confirm" not in err["detail"]["message"].lower()
    assert not re.search(r"\b[aeqf]\d+\b", err["message"])


# ---------------------------------------------------------------- the review event
def test_the_accept_event_carries_the_named_confirm_in_public_mode(promoted, monkeypatch):
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    c, tok, f = promoted
    assert accept_events(c, tok, f["id"]) == []
    ok = review(c, tok, f["id"], confirm="likely_duplicate")
    assert ok.status_code == 200
    ev = accept_events(c, tok, f["id"])
    assert len(ev) == 1
    assert ev[0]["confirm"] == {"flag": "likely_duplicate", "name": "Likely duplicate", "confirmed_at": ok.json()["item"]["flag"]["confirmed_at"]}
    assert "before" not in ev[0] and "after" not in ev[0]                                       # metadata only: no text in public mode


def test_an_unflagged_accept_has_no_confirm_in_its_event(promoted):
    c, tok, f = promoted
    other = next(a for a in charges(c, tok) if not a["flag"])
    assert review(c, tok, other["id"]).status_code == 200
    ev = accept_events(c, tok, other["id"])
    assert len(ev) == 1 and "confirm" not in ev[0]


def test_local_mode_event_after_also_carries_the_confirm(promoted, monkeypatch):
    monkeypatch.setenv("ZLAYT_MODE", "local")
    c, tok, f = promoted
    review(c, tok, f["id"], confirm="likely_duplicate")
    ev = accept_events(c, tok, f["id"])[0]
    assert ev["confirm"]["flag"] == "likely_duplicate" and ev["after"]["confirm"] == ev["confirm"]


# ---------------------------------------------------------------- the repeat accept
def test_a_repeat_accept_of_a_confirmed_charge_writes_nothing(promoted):
    c, tok, f = promoted
    first = review(c, tok, f["id"], confirm="likely_duplicate").json()["item"]
    for body in ({}, {"confirm": "likely_duplicate"}, {"confirm": "likely_total"}):
        r = review(c, tok, f["id"], **body)
        assert r.status_code == 200 and r.json()["item"]["review_status"] == "accepted", body
        assert r.json()["item"]["flag"]["confirmed_at"] == first["flag"]["confirmed_at"]         # the first confirm stands
    assert len(accept_events(c, tok, f["id"])) == 1


def test_accept_again_after_a_reset_needs_the_confirm_again(promoted):
    c, tok, f = promoted
    review(c, tok, f["id"], confirm="likely_duplicate")
    assert c.post(f"/api/cases/{tok}/items/{f['id']}/review", json={"action": "reset"}).status_code == 200
    r = review(c, tok, f["id"])
    assert r.status_code == 422 and r.json()["error"]["code"] == "CONFIRM_REQUIRED"
    assert review(c, tok, f["id"], confirm="likely_duplicate").status_code == 200
    assert len(accept_events(c, tok, f["id"])) == 2


def test_each_accept_event_after_a_reset_carries_its_own_confirm(promoted):
    """r2 mutant: the confirm must land on the NEWEST accept event, so the first accept keeps its own and the second gets the second confirm."""
    c, tok, f = promoted
    first = review(c, tok, f["id"], confirm="likely_duplicate").json()["item"]["flag"]["confirmed_at"]
    assert c.post(f"/api/cases/{tok}/items/{f['id']}/review", json={"action": "reset"}).status_code == 200
    second = review(c, tok, f["id"], confirm="likely_duplicate").json()["item"]["flag"]["confirmed_at"]
    ev = sorted(accept_events(c, tok, f["id"]), key=lambda e: e["at"])
    assert [e["confirm"]["confirmed_at"] for e in ev] == [first, second]
    assert all(e["confirm"]["flag"] == "likely_duplicate" for e in ev)


def _db(tmp_path):
    from app.db import db as DB
    return DB.connect(str(tmp_path / "d059.sqlite"))


def test_an_accepted_flagged_charge_whose_confirm_has_no_timestamp_asks_for_the_confirm_again(promoted, tmp_path):
    """r2 mutant: the no-op needs the confirm to have happened (confirmed_at), not just the flag to exist on an accepted charge."""
    from app.db import db as DB
    c, tok, f = promoted
    review(c, tok, f["id"], confirm="likely_duplicate")
    conn = _db(tmp_path)
    cid = DB.get_case_by_token(conn, tok)["id"] if hasattr(DB, "get_case_by_token") else conn.execute("SELECT id FROM cases").fetchone()["id"]
    item = DB.get_item(conn, f["id"], cid)
    DB.update_item(conn, f["id"], now=9.0, case=cid, ladder={**item["ladder"], "confirm": {k: v for k, v in item["ladder"]["confirm"].items() if k != "confirmed_at"}})
    r = review(c, tok, f["id"])
    assert r.status_code == 422 and r.json()["error"]["code"] == "CONFIRM_REQUIRED"


# ---------------------------------------------------------------- one transaction
def test_a_failure_writing_the_confirm_leaves_no_half_confirmed_charge(promoted, monkeypatch):
    """r2: the item's confirm and the event's confirm are written in ONE transaction, so a failure on the second write rolls back the first (the item never shows a
    confirmed_at the event lacks), and the accept that preceded them is taken back: the charge is pending again and counts for nothing. A retry then works."""
    from app.backend import review as RV
    c, tok, f = promoted
    real = RV.json

    class Boom:
        def __getattr__(self, name):
            return getattr(real, name)

        def loads(self, *a, **k):
            raise RuntimeError("injected failure writing the event")
    monkeypatch.setattr(RV, "json", Boom())
    bad = TestClient(c.app, client=("127.0.0.1", 50000), raise_server_exceptions=False)
    totals_before = c.get(f"/api/cases/{tok}").json()["totals"]
    assert review(bad, tok, f["id"], confirm="likely_duplicate").status_code == 500
    monkeypatch.setattr(RV, "json", real)
    g = c.get(f"/api/cases/{tok}").json()
    now = next(a for a in g["amounts"] if a["id"] == f["id"])
    assert now["review_status"] == "pending" and not now["flag"].get("confirmed_at")
    assert g["totals"] == totals_before                                                      # never counted without its confirm
    assert review(c, tok, f["id"]).status_code == 422                                       # a bare accept is still refused
    ok = review(c, tok, f["id"], confirm="likely_duplicate")
    assert ok.status_code == 200 and ok.json()["item"]["flag"]["confirmed_at"]
    ev = sorted(accept_events(c, tok, f["id"]), key=lambda e: e["at"])
    assert ev[-1]["confirm"]["confirmed_at"] == ok.json()["item"]["flag"]["confirmed_at"]   # the accept that stands carries its own confirm
    assert [e["action"] for e in c.get(f"/api/cases/{tok}/audit").json()["events"] if e["item_id"] == f["id"] and e["action"] in ("accept", "reset")].count("reset") == 1      # the taken-back accept is in the trail


def test_the_trace_events_carry_the_confirm(promoted):
    c, tok, f = promoted
    at = review(c, tok, f["id"], confirm="likely_duplicate").json()["item"]["flag"]["confirmed_at"]
    ev = [e for e in steps(c, tok, f["id"])["human"]["evidence"]["events"] if e["action"] == "accept"]
    assert ev[0]["confirm"] == {"flag": "likely_duplicate", "name": "Likely duplicate", "confirmed_at": at}


def test_a_wrong_confirm_is_still_refused_before_the_first_accept(promoted):
    c, tok, f = promoted
    r = review(c, tok, f["id"], confirm="likely_total")
    assert r.status_code == 422 and r.json()["error"]["code"] == "CONFIRM_REQUIRED"
    assert accept_events(c, tok, f["id"]) == []


# ---------------------------------------------------------------- the trace
def test_trace_has_a_flag_step_pending_until_confirmed(promoted):
    c, tok, f = promoted
    st = steps(c, tok, f["id"])
    s = st["charge_flag"]
    assert s["label"] == "Flagged by the code: Likely duplicate" and s["kind"] == "code" and s["status"] == "pending"
    assert s["why"].startswith(f["flag"]["message"]) and "needs your named confirm" in s["why"]
    assert s["next_action"]["code"] == "CONFIRM_FLAG" and s["next_action"]["target"] == {"item_id": f["id"]}
    assert not re.search(r"\b[aeqf]\d+\b|likely_duplicate", s["why"])
    order = list(steps_in_order(c, tok, f["id"]))
    assert order.index("charge_flag") < order.index("total_inclusion") < order.index("human")


def steps_in_order(c, tok, item):
    return [s["id"] for s in c.get(f"/api/cases/{tok}/items/{item}/trace").json()["steps"]]


def test_trace_flag_step_passes_after_the_confirm_and_the_human_step_names_it(promoted):
    c, tok, f = promoted
    at = review(c, tok, f["id"], confirm="likely_duplicate").json()["item"]["flag"]["confirmed_at"]
    st = steps(c, tok, f["id"])
    s = st["charge_flag"]
    assert s["status"] == "pass" and s["evidence"]["values"] == {"flag": "likely_duplicate", "name": "Likely duplicate", "confirmed_at": at}
    assert "Likely duplicate" in s["why"] and s.get("next_action") in (None, {})
    h = st["human"]
    assert h["status"] == "pass" and "Likely duplicate" in h["why"] and "confirm" in h["why"].lower()
    assert st["total_inclusion"]["status"] == "pass"


def test_trace_flag_step_is_skipped_when_dismissed_and_absent_when_unflagged(promoted):
    c, tok, f = promoted
    other = next(a for a in charges(c, tok) if not a["flag"])
    assert "charge_flag" not in steps(c, tok, other["id"])
    assert c.post(f"/api/cases/{tok}/items/{f['id']}/review", json={"action": "dismiss"}).status_code == 200
    assert steps(c, tok, f["id"])["charge_flag"]["status"] == "skipped"
