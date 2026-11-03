"""T-179 / D-067 (GATE-M3 product-manager + paralegal majors): the drafted treatment paragraph is cut from the MVP. No page offers it and it never reaches the letter.
The backend routes stay. With NARRATIVE_IN_LETTER unset, an ACCEPTED paragraph adds nothing to the letter or the notes."""
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.backend import export as X, narrative as N, store
from app.backend.api import create_app
from tests.unit.test_api_routes import run_case
from tests.unit.test_narrative import GOOD, accepted_sample, narr

FRONTEND = Path(__file__).resolve().parents[2] / "app" / "frontend"


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("FIXTURE_SET", "curated")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.delenv("NARRATIVE_IN_LETTER", raising=False)
    return TestClient(create_app(str(tmp_path / "d067.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def test_the_page_loads_no_narrative_script_and_has_no_narrative_control():
    html = (FRONTEND / "index.html").read_text()
    assert "narrative.js" not in html
    for f in FRONTEND.glob("*.js"):
        if f.name == "narrative.js":
            continue
        t = f.read_text()
        assert "btn-draft-narrative" not in t and "btn-accept-narrative" not in t, f.name
    assert "Draft treatment paragraph" not in html


def _accepted_paragraph(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    n = N.draft(conn, cid, call=narr(GOOD), now=2.0)
    assert [x["entry_id"] for x in n["sentences"]] == ["e1", "e5"]           # real sentences were drafted and kept
    N.review(conn, cid, "accept", now=3.0)
    assert store.export_case(conn, cid)["narrative"]["status"] == "accepted"
    return conn, cid


def test_an_accepted_paragraph_never_reaches_the_letter_the_notes_or_the_json(tmp_path, tmp_path_factory, monkeypatch):
    from app.backend.export_routes import export_payload
    conn, cid = _accepted_paragraph(tmp_path)
    texts = [s["text"] for s in GOOD]
    # control: with the gate on the stored, accepted paragraph IS in the letter, so the checks below can fail
    monkeypatch.setenv("NARRATIVE_IN_LETTER", "1")
    on = X.build_export(store.export_case(conn, cid))
    assert "TREATMENT SUMMARY" in on["letter_text"] and all(t in on["letter_text"] for t in texts)
    # default (unset): nothing of it anywhere, with no if-guard
    monkeypatch.delenv("NARRATIVE_IN_LETTER")
    ex = X.build_export(store.export_case(conn, cid))
    assert "TREATMENT SUMMARY" not in ex["letter_text"]
    assert "DRAFT TREATMENT" not in ex["internal_notes_text"] and "TREATMENT SUMMARY" not in ex["internal_notes_text"]
    blob = json.dumps(export_payload(cid, store.export_case(conn, cid)), default=str)
    assert not any(t in blob for t in texts) and "TREATMENT SUMMARY" not in blob and "DRAFT TREATMENT" not in blob
    # a pending (not yet accepted) paragraph is not in the notes either
    conn2, cid2 = accepted_sample(tmp_path_factory.mktemp("pending"))
    N.draft(conn2, cid2, call=narr(GOOD), now=2.0)
    ex2 = X.build_export(store.export_case(conn2, cid2))
    assert "DRAFT TREATMENT" not in ex2["internal_notes_text"] and not any(t in ex2["letter_text"] + ex2["internal_notes_text"] for t in texts)


def test_the_case_read_has_no_narrative_key(env):
    c = env
    tok = run_case(c)
    assert "narrative" not in c.get(f"/api/cases/{tok}").json()
