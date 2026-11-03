"""T-114 (T-060 pass 1 F3/F4): a rate is acknowledged, never offered as a letter accept that later blocks export (D-019/D-042, accept needs no judge);
every acceptable item on every demo library packet has its judge fixture (no JUDGE_NOT_RUN dead end); confirm_date reports which gap figures moved.
Fixture backend, no network."""
import os
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import trace
from app.backend.api import create_app, library_cases
from app.db import db as DB

LIB09 = "case_lib09_spanish_interpreter_espalda"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    path = str(tmp_path / "t114.sqlite")
    return TestClient(create_app(path, static_dir=str(tmp_path)), client=("127.0.0.1", 50000)), path


def _load(c, lib_id):
    tok = c.post("/api/cases", json={"library": lib_id}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(480):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed", "done_with_errors"):
            break
        time.sleep(0.25)
    from tests.unit._hand_entry import enter_failed_records_by_hand
    enter_failed_records_by_hand(c, tok)      # T-165: lib01's record 3 has no recorded extract answer; the paralegal enters it by hand
    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready", lib_id
    return tok


def _gate(c, tok):
    return {s["id"]: s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"]}["export_gate"]


def _blank_judge(conn, tok, item_id):
    row = DB.get_item(conn, item_id, tok)
    lad = row["ladder"]
    lad["judge"] = None
    DB.update_item(conn, item_id, case=tok, state="needs_review", state_reasons_json=sorted(set(row["state_reasons"]) | {"JUDGE_UNAVAILABLE"}), ladder=lad)
    conn.execute("DELETE FROM llm_calls WHERE case_id=? AND item_id=? AND step IN ('j1','j2','j3','j4')", (tok, item_id))


# ------------------------------------------------------------ 1. a rate is acknowledged, not a letter accept
def test_a_rate_accepted_without_a_judge_does_not_block_export_but_a_charge_still_does(client):
    c, path = client
    tok = _load(c, LIB09)
    conn = DB.connect(path)
    amounts = {a["id"]: a for a in c.get(f"/api/cases/{tok}").json()["amounts"]}
    rates = [i for i, a in amounts.items() if a["kind"] == "rate"]
    charge = next(i for i, a in amounts.items() if a["kind"] == "charge")
    assert rates
    for i in rates:
        assert amounts[i]["accept_effect"] == "acknowledge" and amounts[i]["judge_required_for_export"] is False
    assert amounts[charge]["accept_effect"] == "letter_total" and amounts[charge]["judge_required_for_export"] is True
    for i in rates:
        _blank_judge(conn, tok, i)
    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
    for i in rates:
        assert c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept"}).status_code == 200
    g = _gate(c, tok)
    assert [b for b in g["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"] == [] and g["counts"]["judge_not_run"] == 0 and g["ready"] is True
    assert c.get(f"/api/cases/{tok}/export").status_code == 200
    tr = c.get(f"/api/cases/{tok}/items/{rates[0]}/trace").json()
    j2 = next(s for s in tr["steps"] if s["id"] == "judge_2")
    assert "optional for a rate" in j2["why"]
    # the same blank on an accepted charge is still a blocker (D-044 is unchanged for everything that can reach the letter)
    _blank_judge(conn, tok, charge)
    assert c.post(f"/api/cases/{tok}/items/{charge}/review", json={"action": "accept"}).status_code == 200
    got = [b["item_id"] for b in _gate(c, tok)["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
    assert got == [charge]
    assert c.get(f"/api/cases/{tok}/export").status_code == 422


def test_a_rate_is_never_in_the_letter_total_even_when_accepted(client):
    c, path = client
    tok = _load(c, LIB09)
    items = c.get(f"/api/cases/{tok}").json()
    for x in [*items["entries"], *items["amounts"]]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
    r = c.get(f"/api/cases/{tok}/export")
    assert r.status_code == 200
    letter = r.json()["letter_text"]
    assert "Billed charges accepted from these records: $5,090.00" in letter      # $2,940 + $2,150; the two $400.00 rate rows add nothing (D-019)


# ------------------------------------------------------------ 2. every acceptable item on every demo packet has its judge
@pytest.mark.parametrize("lib", [x["id"] for x in library_cases()])
def test_walking_every_acceptable_item_on_a_library_packet_never_hits_judge_not_run(client, lib):
    c, path = client
    tok = _load(c, lib)
    conn = DB.connect(path)
    for d in c.get(f"/api/cases/{tok}").json()["dates_to_confirm"]:
        if d.get("candidates"):
            c.post(f"/api/cases/{tok}/records/{d['record_id']}/confirm_date", json={"date": d["candidates"][0]})
    case = c.get(f"/api/cases/{tok}").json()
    accepted = []
    for x in [*case["entries"], *case["undated_entries"], *case["amounts"], *case["flags"]]:
        if c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"}).status_code == 200:
            accepted.append(x["id"])
    assert accepted, lib
    g = _gate(c, tok)
    jnr = [b["item_id"] for b in g["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
    assert jnr == [], f"{lib}: accepted but no judge fixture: {jnr}"
    # stricter than the gate: no accepted item (a rate included) is missing its judge answer, so the demo needs no 'run the second check' step
    missing = [u["item_id"] for u in trace.unjudged_items(conn, tok) if u["item_id"] in accepted]
    assert missing == [], f"{lib}: judge fixture missing for {missing}"


# ------------------------------------------------------------ 3. confirm_date reports which gap figures moved
def test_confirm_date_reports_the_gap_figures_that_changed(client):
    """lib09 record 4 (an intake form): reading it as 5 March moves the one gap from 42 to 40 days; the response says so, old to new."""
    c, path = client
    tok = _load(c, LIB09)
    assert [f["computed"]["days"] for f in c.get(f"/api/cases/{tok}").json()["flags"] if f["type"] == "gap"] == [42]
    out = c.post(f"/api/cases/{tok}/records/r4/confirm_date", json={"date": "2026-03-05"}).json()
    assert len(out["gap_changes"]) == 1
    ch = out["gap_changes"][0]
    assert (ch["change"], ch["old_days"], ch["new_days"]) == ("changed", 42, 40)
    assert (ch["old_from"], ch["old_to"], ch["new_from"], ch["new_to"]) == ("2026-03-03", "2026-04-14", "2026-03-05", "2026-04-14")
    assert ch["sentence"] == "Gap recalculated after you confirmed record 4: now 40 days (was 42)."
    assert ch["flag_id"] in out["gap_flags"]


def test_confirm_date_on_a_phone_note_changes_no_gap(client):
    """golden case_01 record 8 is a phone note (not an encounter): confirming its date moves no gap, so gap_changes is an empty list (not missing)."""
    c, path = client
    text = (pathlib.Path(__file__).resolve().parents[2] / "evals" / "golden" / "case_01_date_formats.txt").read_text()
    tok = c.post("/api/cases", json={"text": text}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(480):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    d = next(x for x in c.get(f"/api/cases/{tok}").json()["dates_to_confirm"] if x["candidates"])
    out = c.post(f"/api/cases/{tok}/records/{d['record_id']}/confirm_date", json={"date": d["candidates"][0]}).json()
    assert out["gap_changes"] == []


def test_gap_changes_pairs_a_moved_endpoint_into_one_change():
    from app.backend import review as RV
    old = {"f_a": {"flag_id": "f_a", "from": "2026-03-03", "to": "2026-04-14", "days": 42, "record_nos": [2, 3]}}
    new = {"f_b": {"flag_id": "f_b", "from": "2026-03-05", "to": "2026-04-14", "days": 40, "record_nos": [3, 4]}}
    got = RV._gap_changes(old, new)
    assert len(got) == 1 and got[0]["change"] == "changed" and (got[0]["old_days"], got[0]["new_days"]) == (42, 40)
    assert RV._gap_changes(old, old) == []
    assert RV._gap_changes(old, {})[0]["change"] == "removed" and RV._gap_changes({}, new)[0]["change"] == "added"
    assert "now 40 days (was 42)" in RV._gap_change_sentence(got[0], 4)
