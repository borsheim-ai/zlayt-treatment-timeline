"""T-177 round 3 (D-065, final): every backend-generated text for a PREPARED item says it is a prepared answer. Never 'AI drafted', 'AI found it', 'the AI's summary' or a model name.
Covers flag items (trace step + why + origin), failed prepared items (SUMMARY_NOT_IN_QUOTE, SCHEMA_INVALID), a missing curated answer (no model step), and /classic routing (D-068).
The recorded set keeps its AI wording."""
import json
import re
import shutil
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app

PREPARED_MODEL = "hand-checked (qa)"
ALLOWED = "\x00"       # D-069: nothing is allowed any more (the "standing in for the AI draft" tail was dropped); tests/unit/test_prepared_property.py is the full guard
AI_WORDS = re.compile(r"AI draft|AI found|AI proposed|AI-made|AI read|AI wrote|the AI's|the AI did not|claude-sonnet", re.I)
E1_KEY = "98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7"      # e1's curated generator answer


def _client(tmp_path, monkeypatch, fixture_set=None, fixture_dir=None, mode="local", static=None):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    if mode:
        monkeypatch.setenv("ZLAYT_MODE", mode)
    else:
        monkeypatch.delenv("ZLAYT_MODE", raising=False)
    for k in ("ANTHROPIC_API_KEY", "ENABLE_LIVE", "LLM_FIXTURE_DIR", "FIXTURE_SET"):
        monkeypatch.delenv(k, raising=False)
    if fixture_set:
        monkeypatch.setenv("FIXTURE_SET", fixture_set)
    if fixture_dir:
        monkeypatch.setenv("LLM_FIXTURE_DIR", str(fixture_dir))
    return TestClient(create_app(str(tmp_path / "p.sqlite"), static_dir=str(static or tmp_path)), client=("127.0.0.1", 50000))


def _run(c, partial=False):
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready" or (partial and (s.get("error") or {}).get("code") == "run_partial"), json.dumps(s)[:1500]      # a record with no usable answer is a partial run, kept
    return tok


@pytest.fixture
def curated(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, "curated")
    return c, _run(c)


@pytest.fixture
def recorded(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch)
    return c, _run(c)


def _ids(c, tok):
    case = c.get(f"/api/cases/{tok}").json()
    return [x["id"] for k in ("entries", "flags", "amounts") for x in case.get(k, [])] + [x["id"] for x in case.get("tray", []) if isinstance(x, dict) and x.get("id")]


def _hits(text):
    return AI_WORDS.findall(text.replace(ALLOWED, ""))


def _mutated_set(tmp_path, mode):
    """Copy the curated set (+ recorded fallback, as fixture.call does) into tmp/curated; break e1's generator answer."""
    import os
    root = tmp_path / "mut"
    d = root / "curated"
    d.mkdir(parents=True)
    src = os.path.join(os.path.dirname(__file__), "..", "fixtures", "llm")
    for f in os.listdir(src):
        if f.endswith(".json"):
            shutil.copy(os.path.join(src, f), d)
    for f in os.listdir(os.path.join(src, "curated")):
        if f.endswith(".json"):
            shutil.copy(os.path.join(src, "curated", f), d)
    p = d / f"{E1_KEY}.json"
    if mode == "missing":
        p.unlink()
    else:
        o = json.loads(p.read_text())
        if mode == "unsupported":
            o["output"]["summary"] = "Patient reported paralysis of the left leg and loss of bladder control."
        else:
            o["output"].pop("summary", None)
        p.write_text(json.dumps(o))
    return d


# ---- flags on the curated set
def test_curated_flag_traces_say_prepared_and_never_ai_found_it(curated):
    c, tok = curated
    case = c.get(f"/api/cases/{tok}").json()
    flags = [f for f in case["flags"] if f.get("origin") in ("llm", "lexicon+llm")]
    assert flags
    for f in flags:
        item = c.get(f"/api/cases/{tok}/items/{f['id']}").json()["item"]
        assert item["prepared"] is True, f["id"]
        st = next(s for s in c.get(f"/api/cases/{tok}/items/{f['id']}/trace").json()["steps"] if s["id"] == "proposed_by_ai")
        assert "Prepared answer" in st["label"] and st["evidence"]["model"]["prepared"] is True and st["evidence"]["model"]["id"] == PREPARED_MODEL, (f["id"], st)
        assert not _hits(json.dumps(st)), (f["id"], st)


def test_curated_whole_surface_has_no_ai_authorship_wording(curated):
    c, tok = curated
    bad = {}
    for path in (f"/api/cases/{tok}", f"/api/cases/{tok}/trace", f"/api/cases/{tok}/judges", f"/api/cases/{tok}/audit", "/api/health", f"/api/cases/{tok}/status"):
        h = _hits(json.dumps(c.get(path).json()))
        if h:
            bad[path] = h
    for iid in _ids(c, tok):
        for suffix in ("", "/trace"):
            r = c.get(f"/api/cases/{tok}/items/{iid}{suffix}")
            if r.status_code == 200:
                h = _hits(json.dumps(r.json()))
                if h:
                    bad[f"{iid}{suffix}"] = h
    assert not bad, bad


def test_curated_lexicon_only_flag_does_not_say_the_ai_looked(curated):
    c, tok = curated
    for f in c.get(f"/api/cases/{tok}").json()["flags"]:
        if f.get("origin") == "lexicon":
            st = next(s for s in c.get(f"/api/cases/{tok}/items/{f['id']}/trace").json()["steps"] if s["id"] == "proposed_by_ai")
            assert st["label"] != "AI found it" and "Prepared" in st["label"] and not _hits(st["why"]), st


def test_recorded_flags_keep_ai_found_it(recorded):
    c, tok = recorded
    fl = [f for f in c.get(f"/api/cases/{tok}").json()["flags"] if f.get("origin") in ("llm", "lexicon+llm")]
    assert fl
    for f in fl:
        st = next(s for s in c.get(f"/api/cases/{tok}/items/{f['id']}/trace").json()["steps"] if s["id"] == "proposed_by_ai")
        assert st["label"] == "AI found it" and st["evidence"]["model"]["prepared"] is False


# ---- failed or missing prepared answers
@pytest.mark.parametrize("mode", ["unsupported", "schema"])
def test_failed_prepared_item_trace_says_prepared(tmp_path, monkeypatch, mode):
    c = _client(tmp_path, monkeypatch, fixture_dir=_mutated_set(tmp_path, mode))
    tok = _run(c, partial=True)
    tr = c.get(f"/api/cases/{tok}/items/e1/trace").json()
    st = next(s for s in tr["steps"] if s["id"] == "extracted")
    assert st["status"] == "fail"
    if mode == "unsupported":
        assert st["evidence"]["model"]["prepared"] is True
    assert "AI drafted" not in st["label"] and "Prepared" in st["label"], st
    assert not _hits(json.dumps(st)), st
    assert not _hits(json.dumps(c.get(f"/api/cases/{tok}/items/e1").json()))


def test_missing_curated_answer_never_shows_a_model_step(tmp_path, monkeypatch):
    d = _mutated_set(tmp_path, "missing")
    (d.parent / "x").mkdir()
    # no recorded fallback exists for e1 because LLM_FIXTURE_DIR is set (fixture.call does not fall back then)
    c = _client(tmp_path, monkeypatch, fixture_dir=d)
    tok = _run(c, partial=True)
    item = c.get(f"/api/cases/{tok}/items/e1").json()["item"]
    assert item["state"] == "rejected" and "FIXTURE_MISS" in item["reasons"]
    st = next(s for s in c.get(f"/api/cases/{tok}/items/e1/trace").json()["steps"] if s["id"] == "extracted")
    assert st["status"] == "fail", st
    assert "claude-sonnet" not in json.dumps(st) and not _hits(json.dumps(st)) and "prepared" in st["label"].lower() and "no prepared answer" in st["why"].lower(), st
    assert not st["evidence"].get("model")
    assert not _hits(json.dumps(item))
    msg = c.get(f"/api/cases/{tok}/status").json().get("error", {}).get("message", "")
    assert msg and "The AI step" not in msg and not _hits(msg), msg      # the partial-run message on a curated set says nothing ran a model
    judges = c.get(f"/api/cases/{tok}/judges").json()
    assert judges["models"]["generator"] == PREPARED_MODEL and judges["models"]["generator_prepared"] is True
    ex = next(x for x in c.get(f"/api/cases/{tok}/trace").json()["steps"] if x["id"] == "extract")
    assert not _hits(json.dumps(ex)) and "claude-sonnet" not in json.dumps(ex), ex


def test_recorded_missing_answer_is_a_fail_step_not_a_pass(tmp_path, monkeypatch):
    d = tmp_path / "rec"
    d.mkdir()
    import os
    src = os.path.join(os.path.dirname(__file__), "..", "fixtures", "llm")
    for f in os.listdir(src):
        if f.endswith(".json") and f != f"{E1_KEY}.json":
            shutil.copy(os.path.join(src, f), d)
    c = _client(tmp_path, monkeypatch, fixture_dir=d)
    tok = _run(c, partial=True)
    st = next(s for s in c.get(f"/api/cases/{tok}/items/e1/trace").json()["steps"] if s["id"] == "extracted")
    assert st["status"] == "fail" and "The AI read this record" not in st["why"], st


# ---- /classic (D-068)
@pytest.fixture
def frontend(tmp_path):
    root = tmp_path / "fe"
    (root / "guided").mkdir(parents=True)
    (root / "guided" / "index.html").write_text("<html>guided</html>")
    (root / "index.html").write_text("<html>classic</html>")
    return root


def test_classic_redirects_to_the_guided_ui_in_demo_and_public_mode(tmp_path, monkeypatch, frontend):
    c = _client(tmp_path, monkeypatch, "curated", mode=None, static=frontend)
    for path in ("/classic", "/classic/", "/classic/index.html", "/classic/anything"):
        r = c.get(path, follow_redirects=False)
        assert r.status_code in (302, 307) and r.headers["location"] == "/", (path, r.status_code, r.headers)
    assert "guided" in c.get("/").text and "classic" not in c.get("/", follow_redirects=True).text.replace("guided", "")


def test_classic_stays_reachable_in_local_mode(tmp_path, monkeypatch, frontend):
    c = _client(tmp_path, monkeypatch, "curated", mode="local", static=frontend)
    r = c.get("/classic/", follow_redirects=False)
    assert r.status_code == 200 and "classic" in r.text
    assert c.get("/classic", follow_redirects=False).headers["location"] == "/classic/"


def test_classic_stays_reachable_in_dev_mode(tmp_path, monkeypatch, frontend):
    monkeypatch.setenv("ZLAYT_CLASSIC", "1")
    c = _client(tmp_path, monkeypatch, "curated", mode=None, static=frontend)
    assert c.get("/classic/", follow_redirects=False).status_code == 200


def test_classic_redirect_also_on_the_recorded_set(tmp_path, monkeypatch, frontend):
    c = _client(tmp_path, monkeypatch, None, mode=None, static=frontend)
    assert c.get("/classic/", follow_redirects=False).headers["location"] == "/"
