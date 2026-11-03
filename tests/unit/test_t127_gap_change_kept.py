"""T-127 (T-114 r3): the gap-change record lives with the case, not in one browser. A gap flag whose figures moved in confirm_date carries `gap_change` in
GET /api/cases/{token} until that gap's figures change again; a gap that no longer applies is listed in `gap_changes_removed[]` with its sentence. Fixture backend."""
import pytest

from app.backend import present
from app.db import db as DB
from tests.unit.test_t114_rates_and_demo_judges import LIB09, _load, client  # noqa: F401  (fixture)


def _gap(case):
    return next(f for f in case["flags"] if f["type"] == "gap")


def test_the_changed_gap_flag_carries_gap_change_in_get_case_and_it_survives_a_new_connection(client):
    c, path = client
    tok = _load(c, LIB09)
    assert "gap_change" not in _gap(c.get(f"/api/cases/{tok}").json()) or _gap(c.get(f"/api/cases/{tok}").json())["gap_change"] is None
    out = c.post(f"/api/cases/{tok}/records/r4/confirm_date", json={"date": "2026-03-05"}).json()
    want = out["gap_changes"][0]
    for _ in range(2):                                              # a fresh GET (and, below, a fresh app on the same file) gives the same record
        g = _gap(c.get(f"/api/cases/{tok}").json())
        gc = g["gap_change"]
        assert gc["flag_id"] == g["id"] == want["flag_id"] and gc["change"] == "changed" and gc["record_seq"] == 4
        assert (gc["old_days"], gc["new_days"], gc["old_from"], gc["old_to"], gc["new_from"], gc["new_to"]) == (42, 40, "2026-03-03", "2026-04-14", "2026-03-05", "2026-04-14")
        assert gc["sentence"] == "Gap recalculated after you confirmed record 4: now 40 days (was 42)." == want["sentence"]
        assert "gap_change" not in g["computed"]
    from fastapi.testclient import TestClient
    from app.backend.api import create_app
    c2 = TestClient(create_app(path, static_dir="."), client=("127.0.0.1", 50000))
    assert _gap(c2.get(f"/api/cases/{tok}").json())["gap_change"]["new_days"] == 40
    assert c2.get(f"/api/cases/{tok}").json()["gap_changes_removed"] == []
    # reviewing the gap does not lose it
    acc = c.post(f"/api/cases/{tok}/items/{_gap(c.get(f'/api/cases/{tok}').json())['id']}/review", json={"action": "accept"})
    assert acc.status_code == 200 and _gap(c.get(f"/api/cases/{tok}").json())["gap_change"]["new_days"] == 40


def test_gap_change_goes_when_the_gaps_figures_move_again():
    """The kept record matches only the gap's CURRENT figures: a later recompute that moves them again replaces it (the latest event wins; a stale one is never shown)."""
    ev = [{"action": "confirm_date", "after": {"gap_changes": [{"flag_id": "f_gap_r4_r5", "change": "changed", "old_days": 42, "new_days": 40, "old_from": "a", "old_to": "b",
                                                                 "new_from": "2026-03-05", "new_to": "2026-04-14", "record_seq": 4, "sentence": "s1"}]}},
          {"action": "confirm_date", "after": {"gap_changes": [{"flag_id": "f_gap_r4_r5", "change": "changed", "old_days": 40, "new_days": 35, "old_from": "2026-03-05", "old_to": "2026-04-14",
                                                                 "new_from": "2026-03-10", "new_to": "2026-04-14", "record_seq": 6, "sentence": "s2"}]}}]
    cur = {"f_gap_r4_r5": {"days": 35, "from": "2026-03-10", "to": "2026-04-14"}}
    changes, removed = present.gap_change_index(ev, cur)
    assert changes["f_gap_r4_r5"]["sentence"] == "s2" and removed == []
    changes, removed = present.gap_change_index(ev, {"f_gap_r4_r5": {"days": 30, "from": "2026-03-15", "to": "2026-04-14"}})        # moved by something else since: no stale claim
    assert changes == {} and removed == []


def test_a_gap_that_no_longer_applies_is_listed_with_its_sentence_until_it_comes_back():
    ev = [{"action": "confirm_date", "after": {"gap_changes": [{"flag_id": "f_gap_r2_r3", "change": "removed", "old_days": 31, "new_days": None, "old_from": "2026-01-01",
                                                                 "old_to": "2026-02-01", "new_from": None, "new_to": None, "record_seq": 3, "sentence": "A gap of 31 days no longer applies after you confirmed the date of record 3."}]}}]
    changes, removed = present.gap_change_index(ev, {})
    assert changes == {} and [r["sentence"] for r in removed] == ["A gap of 31 days no longer applies after you confirmed the date of record 3."]
    assert removed[0]["flag_id"] == "f_gap_r2_r3" and removed[0]["old_days"] == 31
    _c, removed = present.gap_change_index(ev, {"f_gap_r2_r3": {"days": 31, "from": "2026-01-01", "to": "2026-02-01"}})        # the same gap exists again
    assert removed == []


def test_confirm_date_writes_the_change_into_its_audit_event(client):
    c, path = client
    tok = _load(c, LIB09)
    c.post(f"/api/cases/{tok}/records/r4/confirm_date", json={"date": "2026-03-05"})
    conn = DB.connect(path)
    ev = [e for e in DB.list_events(conn, tok) if e["action"] == "confirm_date"]
    assert ev and ev[-1]["after"]["gap_changes"][0]["record_seq"] == 4 and ev[-1]["after"]["gap_changes"][0]["new_days"] == 40
