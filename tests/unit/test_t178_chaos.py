"""T-178 (GATE-M3 chaos tester): an interrupted run, a stale second tab, invisible-only pastes and lone surrogates. Fixture backend, no key, no network."""
import json
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import ingest, store
from app.backend.api import create_app
from app.db import db as DB
from tests.unit.test_api_routes import wait_ready

LOCAL = ("127.0.0.1", 50000)
ZW = ["​", "‌", "‍", "⁠", "﻿", "‎", "‏", "­", "‮", "\U000e0041"]


def make(tmp_path, monkeypatch, live=False, db=None):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    if live:                                   # arbitrary text reaches code-only ingest; the backend stays fixture: no network, no model call
        monkeypatch.setenv("ENABLE_LIVE", "1")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "dummy-not-a-key")
    db = db or str(tmp_path / "t178.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=LOCAL, raise_server_exceptions=False)


def send(c, method, path, obj):
    """A browser's JSON.stringify writes a lone surrogate as the escape \\ud83d; json.dumps (ensure_ascii) does the same. The test client's own json= cannot encode one."""
    return c.request(method, path, content=json.dumps(obj).encode(), headers={"content-type": "application/json"})


def counts(db):
    c = DB.connect(db)
    try:
        return c.execute("SELECT count(*) FROM cases").fetchone()[0], c.execute("SELECT count(*) FROM llm_calls").fetchone()[0]
    finally:
        c.close()


# ------------------------------------------------------------------ 3. paste text
@pytest.mark.parametrize("text", ["​" * 3, *ZW, "".join(ZW), " ​ \n\t⁠﻿ ", "​ ‍ ", "\r\n​\r"])
def test_invisible_only_text_is_empty(text):
    with pytest.raises(ingest.IngestError) as e:
        ingest.check_limits(text)
    assert e.value.code == "bad_request"
    with pytest.raises(ingest.IngestError) as e:
        ingest.check_limits(text, max_chars=0)            # empty is decided before the size limit, even a limit of zero
    assert e.value.code == "bad_request"


def test_invisible_characters_do_not_count_toward_the_limit():
    padded = ("ab" + "​" * 10) * (ingest.MAX_CHARS // 2)         # 60,000 visible characters, 660,000 with the padding
    assert len(ingest.check_limits(padded)) == ingest.MAX_CHARS
    with pytest.raises(ingest.IngestError) as e:
        ingest.check_limits("a" * (ingest.MAX_CHARS + 1))
    assert e.value.code == "input_too_large"


def test_text_is_cleaned_not_only_checked():
    assert ingest.check_limits("Date:​ 2026-01-02⁠\r\nSource:﻿ X ‮") == "Date: 2026-01-02\nSource: X"
    assert ingest.normalize_text("a\ud83db") == "a�b"
    assert ingest.normalize_text("😀") == "\U0001f600"                    # a real pair stays an emoji
    assert ingest.normalize_text("\ud83d") == "�"                               # a lone surrogate alone is (visible) text, not empty


def test_pdf_page_text_is_cleaned_with_offsets_that_still_index_the_text():
    from app.backend import pdf_text
    got = pdf_text.assemble(["Page one­ text​ here.", "", "Page ⁠two."])
    assert got["text"] == "Page one text here.\n\nPage two."
    assert [got["text"][p["start"]:p["end"]] for p in got["pages"]] == ["Page one text here.", "Page two."]


@pytest.mark.parametrize("live", [False, True])
@pytest.mark.parametrize("text", ["​​​", "⁠﻿‍", " ​ \t", "﻿"])
def test_invisible_only_paste_is_400_and_spends_nothing(tmp_path, monkeypatch, live, text):
    db, c = make(tmp_path, monkeypatch, live=live)
    r = c.post("/api/cases", json={"text": text})
    assert r.status_code == 400 and r.json()["error"]["code"] == "bad_request" and r.json()["error"]["message"] == "Input is empty."
    assert counts(db) == (0, 0)


# ------------------------------------------------------------------ 4. no 500 for any paste
WEIRD = ["\ud83d", "a\ud83db", "\ude00\ud83d", "\x00", "a\x00b", "￾￿", "\U0010ffff", "é" * 5000, "‮" * 100 + "x", "\x1b[31mred", "\x0c\x0b",
         "\U000e0041\U000e0042 hidden tag text", "=== Record 1 ===\nDate: ​2026-01-02\nSource: Test\nExcerpt: \"Pain.\"", "  ", "\U0001f600" * 20000]


@pytest.mark.parametrize("live", [False, True])
@pytest.mark.parametrize("text", WEIRD)
def test_no_paste_returns_a_500(tmp_path, monkeypatch, live, text):
    db, c = make(tmp_path, monkeypatch, live=live)
    r = send(c, "POST", "/api/cases", {"text": text})
    assert r.status_code in (201, 400, 409, 413), (live, r.status_code, r.text[:200])
    if r.status_code == 201:
        assert c.get(f"/api/cases/{r.json()['token']}").status_code == 200
        raw = DB.connect(db).execute("SELECT raw_text FROM cases").fetchone()[0]
        raw.encode("utf-8")                                           # what is stored can always be encoded
        assert not any(ch in raw for ch in ZW)


SAMPLE = "=== Record 1 ===\nDate: 2026-01-02\nSource: Test Clinic\nExcerpt: \"Patient reports neck pain.\""


def test_lone_surrogate_in_titles_and_edit_bodies_is_not_a_500(tmp_path, monkeypatch):
    db, c = make(tmp_path, monkeypatch, live=True)
    r = send(c, "POST", "/api/cases", {"text": SAMPLE, "title": "Smith \ud83d case"})
    assert r.status_code == 201, r.text
    tok = r.json()["token"]
    assert c.get(f"/api/cases/{tok}").json()["title"] == "Smith � case"
    assert send(c, "PATCH", f"/api/cases/{tok}", {"title": "x\ude00y"}).status_code < 500
    assert send(c, "POST", f"/api/cases/{tok}/items/e1/review", {"action": "edit", "edits": {"summary": "a\ud83d"}}).status_code < 500
    assert send(c, "POST", "/api/cases", {"text": SAMPLE, "title": "\ud83d" * 3}).status_code < 500


def test_json_body_surrogates_are_replaced_at_the_door(tmp_path, monkeypatch):
    db, c = make(tmp_path, monkeypatch, live=True)
    body = json.dumps({"text": SAMPLE.replace("Test Clinic", "Clinic @@")}).replace("@@", "\\ud83d")        # the escape \ud83d is how a client sends half an emoji
    r = c.post("/api/cases", content=body.encode(), headers={"content-type": "application/json"})
    assert r.status_code == 201
    assert "Clinic �" in DB.connect(db).execute("SELECT raw_text FROM cases").fetchone()[0]


# ------------------------------------------------------------------ 1. interrupted runs
def seeded(tmp_path, monkeypatch):
    db, c = make(tmp_path, monkeypatch)
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    wait_ready(c, tok)
    return db, c, tok


def test_restart_marks_a_stranded_run_failed_and_keeps_accepted_items(tmp_path, monkeypatch):
    db, c, tok = seeded(tmp_path, monkeypatch)
    case = c.get(f"/api/cases/{tok}").json()
    accepted = [x["id"] for x in case["entries"][:3]]
    for i in accepted:
        assert c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept"}).status_code == 200
    conn = DB.connect(db)
    DB.update_case(conn, tok, status="running", stage="extract", error=None, run_started_at=time.time(), run_finished_at=None)   # what a SIGKILL mid re-run leaves
    conn.close()
    assert store.is_live_run(tok) is False

    _, c2 = make(tmp_path, monkeypatch, db=db)                        # the restarted server, same DB
    s = c2.get(f"/api/cases/{tok}/status").json()
    assert s["status"] == "failed" and s["error"]["code"] == "run_partial" and s["error"]["interrupted"] is True
    assert "interrupted" in s["error"]["message"] and "Run it again" in s["error"]["message"] and "decision" in s["error"]["message"]
    ex = c2.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 422 and ex.json()["error"]["detail"]["blockers"][0]["reason_code"] == "RUN_FAILED"       # not RUN_IN_PROGRESS: there is a way out
    assert c2.post(f"/api/cases/{tok}/run", json={}).json()["error"]["code"] == "needs_confirm"
    assert c2.post(f"/api/cases/{tok}/run", json={"confirm_rerun": True}).status_code == 202
    wait_ready(c2, tok)
    after = c2.get(f"/api/cases/{tok}").json()
    assert {x["id"] for x in after["entries"] if x["review_status"] == "accepted"} >= set(accepted)
    assert c2.get(f"/api/cases/{tok}/export").status_code == 200


def test_first_run_stranded_by_a_restart_can_be_run_again(tmp_path, monkeypatch):
    db, c = make(tmp_path, monkeypatch)
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    conn = DB.connect(db)
    DB.update_case(conn, tok, status="running", stage="extract", run_started_at=time.time())
    conn.close()
    _, c2 = make(tmp_path, monkeypatch, db=db)
    assert c2.get(f"/api/cases/{tok}/status").json()["status"] == "failed"
    assert c2.post(f"/api/cases/{tok}/run", json={}).status_code == 202          # nothing decided: no confirm needed
    wait_ready(c2, tok)


def test_a_run_that_is_really_running_is_not_interrupted(tmp_path, monkeypatch):
    db, c = make(tmp_path, monkeypatch)
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    conn = DB.connect(db)
    DB.update_case(conn, tok, status="running", stage="extract", run_started_at=time.time())
    store.run_started(tok)
    try:
        _, c2 = make(tmp_path, monkeypatch, db=db)                    # another app in the same process: the thread is alive
        assert c2.get(f"/api/cases/{tok}/status").json()["status"] == "running"
    finally:
        store.run_ended(tok)
        conn.close()


def test_a_stale_running_case_with_no_thread_settles_on_read_but_a_fresh_one_does_not(tmp_path, monkeypatch):
    db, c = make(tmp_path, monkeypatch)
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    conn = DB.connect(db)
    DB.update_case(conn, tok, status="running", stage="extract", run_started_at=time.time() - 60)
    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "running"
    DB.update_case(conn, tok, status="running", stage="extract", run_started_at=time.time() - store.RUN_STALE_AFTER_S - 5)
    s = c.get(f"/api/cases/{tok}/status").json()
    assert s["status"] == "failed" and s["error"]["interrupted"] is True
    conn.close()


def test_interrupt_run_ignores_a_case_that_is_not_running(tmp_path, monkeypatch):
    db, c, tok = seeded(tmp_path, monkeypatch)
    conn = DB.connect(db)
    assert store.interrupt_run(conn, tok) is False and DB.get_case(conn, tok)["status"] == "ready"
    conn.close()


# ------------------------------------------------------------------ 2. stale second tab
def test_stale_tab_cannot_override_a_newer_decision(tmp_path, monkeypatch):
    db, c, tok = seeded(tmp_path, monkeypatch)
    item = c.get(f"/api/cases/{tok}").json()["entries"][3]
    iid, seen = item["id"], {"version": item["version"], "expected_status": item["review_status"]}
    assert isinstance(seen["version"], float) and seen["expected_status"] == "pending"
    r1 = c.post(f"/api/cases/{tok}/items/{iid}/review", json={"action": "dismiss", **seen})        # tab 1
    assert r1.status_code == 200 and r1.json()["item"]["review_status"] == "dismissed" and r1.json()["item"]["version"] != seen["version"]
    r2 = c.post(f"/api/cases/{tok}/items/{iid}/review", json={"action": "accept", **seen})          # tab 2, still showing the old version
    e = r2.json()["error"]
    assert r2.status_code == 409 and e["code"] == "stale_item" and e["message"] == "This item changed in another tab; reload to see it."
    assert e["detail"]["review_status"] == "dismissed"
    now = c.get(f"/api/cases/{tok}").json()
    assert next(x for x in now["entries"] if x["id"] == iid)["review_status"] == "dismissed"
    conn = DB.connect(db)
    assert [x["action"] for x in DB.list_events(conn, tok, iid)] == ["dismiss"]                     # the refused write left no event
    conn.close()


def test_either_signal_alone_detects_staleness_and_the_fresh_version_succeeds(tmp_path, monkeypatch):
    db, c, tok = seeded(tmp_path, monkeypatch)
    it = c.get(f"/api/cases/{tok}").json()["entries"][2]
    iid = it["id"]
    c.post(f"/api/cases/{tok}/items/{iid}/review", json={"action": "accept"})                       # another tab, no check sent: old clients still work
    assert c.post(f"/api/cases/{tok}/items/{iid}/review", json={"action": "dismiss", "version": it["version"]}).status_code == 409
    assert c.post(f"/api/cases/{tok}/items/{iid}/review", json={"action": "dismiss", "expected_status": "pending"}).status_code == 409
    fresh = c.get(f"/api/cases/{tok}/items/{iid}").json()["item"]
    ok = c.post(f"/api/cases/{tok}/items/{iid}/review", json={"action": "dismiss", "version": fresh["version"], "expected_status": fresh["review_status"]})
    assert ok.status_code == 200 and ok.json()["item"]["review_status"] == "dismissed"


def test_a_repeat_of_the_same_decision_from_a_stale_tab_is_harmless(tmp_path, monkeypatch):
    db, c, tok = seeded(tmp_path, monkeypatch)
    it = c.get(f"/api/cases/{tok}").json()["entries"][1]
    body = {"action": "accept", "version": it["version"], "expected_status": "pending"}
    assert c.post(f"/api/cases/{tok}/items/{it['id']}/review", json=body).status_code == 200
    assert c.post(f"/api/cases/{tok}/items/{it['id']}/review", json=body).status_code == 200      # same outcome: nothing to protect


def test_stale_edit_is_refused_and_bad_check_values_are_a_422(tmp_path, monkeypatch):
    db, c, tok = seeded(tmp_path, monkeypatch)
    it = c.get(f"/api/cases/{tok}").json()["entries"][4]
    c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "dismiss"})
    r = c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "edit", "edits": {"summary": it["summary"]}, "expected_status": "pending"})
    assert r.status_code == 409 and r.json()["error"]["code"] == "stale_item"
    assert c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "reset", "version": "x"}).status_code == 422
    assert c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "reset", "expected_status": "maybe"}).status_code == 422
    assert c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "reset", "version": True}).status_code == 422


def test_every_item_view_carries_a_version(tmp_path, monkeypatch):
    db, c, tok = seeded(tmp_path, monkeypatch)
    case = c.get(f"/api/cases/{tok}").json()
    for k in ("entries", "amounts", "flags"):
        assert case[k] and all(isinstance(x["version"], float) for x in case[k]), k
