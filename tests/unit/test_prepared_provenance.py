"""T-177 / D-065 (GATE-M3 PM blocker): a curated (hand-checked) fixture answer is never presented as model output.
Provenance comes from the fixture's own `recorded_from`. Curated -> prepared: true, model 'hand-checked (qa)' in the item, the trace and the audit rows;
the trace's generator step says it is a prepared answer. Recorded (and live) answers keep their real model ids and their AI labels."""
import json
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app

PREPARED_MODEL = "hand-checked (qa)"


def _client(tmp_path, monkeypatch, fixture_set):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.delenv("LLM_FIXTURE_DIR", raising=False)
    if fixture_set:
        monkeypatch.setenv("FIXTURE_SET", fixture_set)
    else:
        monkeypatch.delenv("FIXTURE_SET", raising=False)
    return TestClient(create_app(str(tmp_path / "p.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _run(c):
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready", s
    return tok


@pytest.fixture
def curated(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, "curated")
    return c, _run(c)


@pytest.fixture
def recorded(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, None)
    return c, _run(c)


def _generator_step(trace):
    return next(s for s in trace["steps"] if s["id"] == "extracted")


# ---- curated set
def test_curated_audit_rows_carry_the_prepared_model(curated):
    c, tok = curated
    calls = c.get(f"/api/cases/{tok}/audit").json()["calls"]
    gen = [x for x in calls if x["role"] == "generator"]
    assert len(gen) >= 9
    for x in gen:
        assert x["model"] == PREPARED_MODEL and x["prepared"] is True, x
    # D-056: judge answers are real recordings; they keep their real model id and are not prepared
    judges = [x for x in calls if x["role"] == "judge"]
    assert judges and all(x["prepared"] is False and x["model"] != PREPARED_MODEL for x in judges)


def test_curated_item_is_marked_prepared(curated):
    c, tok = curated
    case = c.get(f"/api/cases/{tok}").json()
    assert case["entries"]
    for e in case["entries"]:
        assert e["prepared"] is True, e["id"]
        assert e["ladder"]["generator"]["model"] == PREPARED_MODEL and e["ladder"]["generator"]["prepared"] is True
    item = c.get(f"/api/cases/{tok}/items/e1").json()["item"]
    assert item["prepared"] is True and item["ladder"]["generator"]["model"] == PREPARED_MODEL


def test_curated_trace_generator_step_names_a_prepared_answer(curated):
    c, tok = curated
    st = _generator_step(c.get(f"/api/cases/{tok}/items/e1/trace").json())
    ev = st["evidence"]
    assert ev["model"]["id"] == PREPARED_MODEL and ev["model"]["id"] != "claude-sonnet-5-5" and ev["model"]["prepared"] is True
    assert st["why"] == "Prepared answer (hand-checked by the team for the demo)"      # D-069: only the badge tooltip may say AI
    assert "AI read this record" not in json.dumps(st) and "AI drafted" not in st["label"]


def test_curated_health_says_prepared_and_the_banner_does_not_claim_ai(curated):
    c, tok = curated
    h = c.get("/api/health").json()
    assert h["answers"] == "prepared" and "prepared by our team" in h["ai_banner"] and "drafted by AI" not in h["ai_banner"]
    # T-177 r2 F3: the banner names the second AI check that runs on the same items, and does not say "checked by code" alone
    assert "second AI model" in h["ai_banner"] and "checked by code;" not in h["ai_banner"]
    # the second check is still an AI check (a real recorded answer) and keeps its model id
    tr = c.get(f"/api/cases/{tok}/items/e1/trace").json()
    j = next(s for s in tr["steps"] if s["id"] == "judge_1")
    assert j["evidence"]["model"]["id"] != PREPARED_MODEL and not j["evidence"]["model"].get("prepared")


# ---- recorded set: labels stay AI
def test_recorded_set_keeps_ai_labels_and_model_ids(recorded):
    c, tok = recorded
    h = c.get("/api/health").json()
    assert h["answers"] == "recorded" and "drafted by AI" in h["ai_banner"]
    calls = c.get(f"/api/cases/{tok}/audit").json()["calls"]
    assert calls and all(x["prepared"] is False and x["model"] != PREPARED_MODEL for x in calls)
    assert any(x["model"] == "claude-sonnet-5-5" for x in calls)
    case = c.get(f"/api/cases/{tok}").json()
    assert case["entries"] and all(e["prepared"] is False for e in case["entries"])
    e1 = case["entries"][0]
    assert e1["ladder"]["generator"]["model"] == "claude-sonnet-5-5" and e1["ladder"]["generator"].get("prepared") is False
    st = _generator_step(c.get(f"/api/cases/{tok}/items/{e1['id']}/trace").json())
    assert st["evidence"]["model"]["id"] == "claude-sonnet-5-5" and st["evidence"]["model"]["prepared"] is False
    assert st["why"] == "The AI read this record and proposed a one-line summary and a quote."


def test_live_backend_health_says_live(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, "curated")
    from app.backend import store
    monkeypatch.setattr(store, "live_enabled", lambda: True)
    assert c.get("/api/health").json()["answers"] == "live"


# ---- T-177 round 2 (staff-engineer F1): no payload names a model as the drafter of a prepared answer
def test_curated_models_never_name_a_drafting_model(curated):
    c, tok = curated
    h = c.get("/api/health").json()
    assert h["models"]["generator"] == PREPARED_MODEL and h["models"]["generator_prepared"] is True and h["models"]["judge"] == "claude-haiku-5-5"
    case = c.get(f"/api/cases/{tok}").json()
    assert case["models"]["generator"] == PREPARED_MODEL and case["models"]["generator_prepared"] is True and case["models"]["judge"] == "claude-haiku-5-5"
    j = c.get(f"/api/cases/{tok}/judges").json()
    assert j["models"]["generator"] == PREPARED_MODEL and j["models"]["generator_prepared"] is True and j["models"]["judge"] == "claude-haiku-5-5"
    assert j["independent_models"] is True and j["totals"]["items_judged"] > 0
    for path in (f"/api/cases/{tok}/judges", f"/api/cases/{tok}", f"/api/cases/{tok}/items/e1/trace", f"/api/cases/{tok}/audit", "/api/health"):
        body = json.dumps(c.get(path).json())
        assert '"generator": "claude-sonnet-5-5"' not in body and "generator_model\": \"claude-sonnet" not in body, path
    assert c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"}).status_code == 200
    r = c.get(f"/api/cases/{tok}/export")
    assert r.status_code == 200, r.text
    assert r.json()["provenance"]["generator_model"] == PREPARED_MODEL and r.json()["provenance"]["judge_model"] == "claude-haiku-5-5"


def test_curated_case_level_trace_does_not_say_an_ai_drafted(curated):
    c, tok = curated
    tr = c.get(f"/api/cases/{tok}/trace").json()
    ex = next(x for x in tr["steps"] if x["id"] == "extract")
    assert "AI drafts" not in ex["label"] and "AI drafted" not in ex["why"] and "prepared" in ex["label"].lower() and "prepared" in ex["why"].lower(), ex
    assert ex["evidence"]["model"]["id"] == PREPARED_MODEL and ex["evidence"]["model"]["prepared"] is True
    jd = next(x for x in tr["steps"] if x["id"] == "judges")
    assert "AI-made" not in jd["label"] and "AI" not in jd["label"] and "Second check" in jd["label"]      # D-069


def test_recorded_case_level_trace_keeps_the_ai_wording(recorded):
    c, tok = recorded
    ex = next(x for x in c.get(f"/api/cases/{tok}/trace").json()["steps"] if x["id"] == "extract")
    assert ex["label"] == "AI drafts a summary and a quote for each record" and ex["why"].startswith("The AI drafted an entry for all")
    assert not ex["evidence"]


def test_recorded_models_keep_the_drafting_model(recorded):
    c, tok = recorded
    j = c.get(f"/api/cases/{tok}/judges").json()
    assert j["models"]["generator"] == "claude-sonnet-5-5" and j["models"]["generator_prepared"] is False
    assert c.get(f"/api/cases/{tok}").json()["models"]["generator"] == "claude-sonnet-5-5"
    h = c.get("/api/health").json()
    assert h["models"]["generator"] == "claude-sonnet-5-5" and h["models"]["generator_prepared"] is False
