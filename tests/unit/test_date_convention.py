"""T-088: date-convention suggestion. Code only, never auto-applied, still one confirm (D-041/D-042)."""
import pytest
from fastapi.testclient import TestClient

from app.backend import date_convention as DC, present
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.test_api_routes import run_case
from tests.unit.test_date_unconfirmed import snapshot


def packet(*dates_text):
    """records built from (date_raw, extra text) pairs; returns (rows, raw)."""
    raw, rows, pos = "", [], 0
    for i, (d, extra) in enumerate(dates_text, 1):
        block = f"Date: {d}\nNote: {extra}\n"
        p = dates.parse_date(d)
        rows.append({"id": f"r{i}", "date_raw": d, "date_status": p["status"], "date_candidates": p["candidates"],
                     "char_start": pos, "char_end": pos + len(block)})
        raw, pos = raw + block, pos + len(block)
    return rows, raw


from app.backend import dates   # noqa: E402


def test_month_first_evidence_suggests_mm_dd_with_reason():
    rows, raw = packet(("03/14/2026", "seen"), ("04/05/2026", "seen again"))
    s = DC.suggest(rows[1], rows, raw)
    assert s["convention"] == "MDY" and s["label"] == "MM/DD" and s["iso"] == "2026-04-05"
    assert s["reason"] == "Another date in this packet uses month first (Record 1: 03/14/2026)"
    assert s["evidence"] == [{"record_id": "r1", "raw": "03/14/2026"}] and s["auto_applied"] is False


def test_day_first_evidence_suggests_dd_mm():
    rows, raw = packet(("14/03/2026", "x"), ("04/05/2026", "y"))
    s = DC.suggest(rows[1], rows, raw)
    assert s["convention"] == "DMY" and s["iso"] == "2026-05-04" and "day first (Record 1: 14/03/2026)" in s["reason"]


def test_evidence_inside_record_text_counts_and_is_listed_up_to_two():
    rows, raw = packet(("04/05/2026", "follow up on 06/25/2026 and 07/30/2026 and 08/31/2026"))
    s = DC.suggest(rows[0], rows, raw)
    assert s["convention"] == "MDY" and s["evidence_count"] == 3 and len(s["evidence"]) == 2
    assert s["reason"].startswith("3 other dates in this packet use month first (Record 1: 06/25/2026) and (Record 1: 07/30/2026)")


def test_no_suggestion_without_evidence_or_with_mixed_evidence():
    rows, raw = packet(("04/05/2026", "alone"), ("06/07/2026", "also ambiguous"))
    assert DC.suggest(rows[0], rows, raw) is None
    rows, raw = packet(("03/14/2026", "a"), ("25/03/2026", "b"), ("04/05/2026", "c"))
    assert DC.suggest(rows[2], rows, raw) is None


def test_not_ambiguous_or_iso_dates_never_get_or_give_evidence():
    rows, raw = packet(("2026-03-14", "iso is not numeric-order evidence"), ("04/05/2026", "x"))
    assert DC.suggest(rows[1], rows, raw) is None
    assert DC.suggest(rows[0], rows, raw) is None        # a parsed record has no suggestion


def test_two_digit_year_ambiguity_keeps_convention_but_no_iso():
    rows, raw = packet(("03/14/2026", "x"), ("04/05/98", "y"))
    s = DC.suggest(rows[1], rows, raw)
    assert s["convention"] == "MDY" and (s["iso"] is None or s["iso"] in rows[1]["date_candidates"])


def test_suggestion_never_writes_and_is_not_a_confirmation(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    db = str(tmp_path / "x.sqlite")
    c = TestClient(create_app(db, static_dir=str(tmp_path)))
    t = run_case(c, G.raw("case_01_date_formats"))
    before = snapshot(db, t)
    g = c.get(f"/api/cases/{t}").json()
    amb = [r for r in g["records"] if r["date_status"] == "ambiguous"]
    assert amb
    for item in g["dates_to_confirm"]:
        s = item.get("suggestion")
        if s:
            assert s["auto_applied"] is False and item["candidates"] and (s["iso"] is None or s["iso"] in item["candidates"])
    assert all(r["date_status"] == "ambiguous" for r in amb)        # nothing was confirmed by the suggestion
    assert snapshot(db, t) == before
    conn = DB.connect(db)
    assert not [e for e in DB.list_events(conn, t) if e["action"] == "confirm_date"]
    conn.close()


def test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    db = str(tmp_path / "y.sqlite")
    c = TestClient(create_app(db, static_dir=str(tmp_path)))
    t = run_case(c, G.raw("case_01_date_formats"))
    g = c.get(f"/api/cases/{t}").json()
    item = [d for d in g["dates_to_confirm"] if d["raw"] == "04/05/2026"][0]
    s = item["suggestion"]
    assert s["label"] == "MM/DD" and s["iso"] == "2026-04-05" and s["auto_applied"] is False
    assert s["evidence_count"] == 4 and s["reason"] == "4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)"
    assert item["status"] == "ambiguous"                     # still unconfirmed until the paralegal confirms
    assert c.post(f"/api/cases/{t}/records/{item['record_id']}/confirm_date", json={"date": "2026-06-06"}).status_code == 422
    r = c.post(f"/api/cases/{t}/records/{item['record_id']}/confirm_date", json={"date": "2026-04-05"})
    assert r.status_code == 200 and not [d for d in r.json()["dates_to_confirm"] if d["raw"] == "04/05/2026"]


def test_reason_names_the_record_each_date_sits_in_never_this_record(tmp_path, monkeypatch):
    """T-088 round 2: evidence dates in other records must not be described as 'in this record' (golden case_01, record 8)."""
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    c = TestClient(create_app(str(tmp_path / "z.sqlite"), static_dir=str(tmp_path)))
    t = run_case(c, G.raw("case_01_date_formats"))
    g = c.get(f"/api/cases/{t}").json()
    item = [d for d in g["dates_to_confirm"] if d["raw"] == "04/05/2026"][0]
    s = item["suggestion"]
    assert item["record_id"] == "r8" and "this record" not in s["reason"]
    assert s["reason"].count("Record ") == len(s["evidence"]) == 2
    for e in s["evidence"]:
        assert e["record_id"] != "r8" and f"(Record {e['record_id'][1:]}: {e['raw']})" in s["reason"]
    # packet: month-first date in record 1, ambiguous date in record 2 -> the reason points at record 1
    rows, raw = packet(("03/14/2026", "seen"), ("04/05/2026", "seen again"))
    r = DC.suggest(rows[1], rows, raw)["reason"]
    assert "Record 1" in r and "this record" not in r and "Record 2" not in r
