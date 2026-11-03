"""T-086/T-087 over HTTP and through the pipeline: hidden text is kept out of the case until confirmed, OCR is opt-in and local, the page
image is served beside the OCR text, and every item on an OCR page is needs_review. SYNTHETIC text only."""
import base64
import shutil

import pytest
from fastapi.testclient import TestClient

from app.backend import pipeline as PL
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script
from tests.unit._pdf_raw import build, scanned_copy, text_page
from tests.unit.test_pdf_hidden import HIDDEN, VISIBLE, pdf_with
from tests.unit.test_pdf_ocr import LINES, scan_pdf

pytest.importorskip("pypdfium2")
PDF = {"content-type": "application/pdf"}
needs_tesseract = pytest.mark.skipif(not shutil.which("tesseract"), reason="tesseract is not installed")


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    db = str(tmp_path / "pc.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def test_upload_excludes_hidden_text_reports_it_and_shows_it_again_on_the_case(client):
    _, c = client
    r = c.post("/api/cases/pdf", content=pdf_with("white", "offpage"), headers=PDF)
    assert r.status_code == 201, r.text
    b = r.json()
    assert "PLANTED" not in " ".join(x["text"] for x in b["records"])
    ht = b["pdf_checks"]["hidden_text"]
    assert ht["pages"][0]["page"] == 1 and ht["pages"][0]["count"] == 2 and ht["pages"][0]["excluded"]
    view = c.get(f"/api/cases/{b['token']}").json()
    assert view["pdf_checks"]["hidden_text"]["pages"][0]["count"] == 2 and view["pdf_pages"][0]["page"] == 1
    assert all(x["ocr_derived"] is False for x in view["records"])


def test_confirming_the_page_includes_its_hidden_text(client):
    _, c = client
    r = c.post("/api/cases/pdf?include_hidden=1", content=pdf_with("white"), headers=PDF)
    assert r.status_code == 201
    b = r.json()
    assert "PLANTED white text" in " ".join(x["text"] for x in b["records"])
    assert b["pdf_checks"]["hidden_text"]["pages"][0]["confirmed"] is True


def test_a_pdf_with_nothing_hidden_has_an_empty_hidden_report(client):
    _, c = client
    b = c.post("/api/cases/pdf", content=build(text_page([VISIBLE])), headers=PDF).json()
    assert b["pdf_checks"]["hidden_text"]["checked"] is True and b["pdf_checks"]["hidden_text"]["pages"] == []


def test_scanned_pdf_without_the_ocr_option_is_refused_and_offers_ocr(client):
    db, c = client
    r = c.post("/api/cases/pdf", content=scan_pdf(), headers=PDF)
    e = r.json()["error"]
    assert r.status_code == 400 and e["detail"]["reason"] == "pdf_no_text_layer" and e["detail"]["scanned_pages"] == [1]
    assert "available" in e["detail"]["ocr"]
    assert DB.connect(db).execute("SELECT COUNT(*) FROM cases").fetchone()[0] == 0


def test_ocr_requested_without_tesseract_is_a_clear_400_and_stores_nothing(client, monkeypatch):
    from app.backend import pdf_ocr
    monkeypatch.setattr(pdf_ocr.shutil, "which", lambda name: None)
    db, c = client
    r = c.post("/api/cases/pdf?ocr=true", content=scan_pdf(), headers=PDF)
    e = r.json()["error"]
    assert r.status_code == 400 and e["detail"]["reason"] == "ocr_unavailable" and "brew install tesseract" in e["message"]
    assert DB.connect(db).execute("SELECT COUNT(*) FROM cases").fetchone()[0] == 0


@needs_tesseract
def test_ocr_upload_serves_the_page_image_beside_the_text_and_marks_records(client):
    _, c = client
    r = c.post("/api/cases/pdf?ocr=true", content=scan_pdf(), headers=PDF)
    assert r.status_code == 201, r.text
    b = r.json()
    assert b["pdf_checks"]["ocr"]["ran"] and b["pdf_checks"]["ocr"]["pages"] == [1]
    assert all(x["ocr_derived"] and x["page"] == 1 for x in b["records"])
    img = c.get(f"/api/cases/{b['token']}/pages/1/image")
    assert img.status_code == 200 and img.headers["content-type"] == "image/png" and img.content[:8] == b"\x89PNG\r\n\x1a\n"
    assert c.get(f"/api/cases/{b['token']}/pages/2/image").status_code == 404
    view = c.get(f"/api/cases/{b['token']}").json()
    assert view["pdf_pages"][0]["source"] == "ocr" and "page_images" not in view and "png_b64" not in str(view)
    assert c.get("/api/cases/nope/pages/1/image").status_code == 404


@needs_tesseract
def test_deleting_the_case_removes_the_stored_page_image(client):
    _, c = client
    t = c.post("/api/cases/pdf?ocr=true", content=scan_pdf(), headers=PDF).json()["token"]
    assert c.delete(f"/api/cases/{t}").status_code == 204
    assert c.get(f"/api/cases/{t}/pages/1/image").status_code == 404


def test_every_item_on_an_ocr_page_is_needs_review_after_a_full_run(tmp_path):
    raw = G.raw("sample")
    conn = DB.connect(str(tmp_path / "o.sqlite"))
    cfg = {"source_pdf": True, "pages": [{"page": 1, "start": 0, "end": len(raw), "source": "ocr"}]}
    cid = DB.create_case(conn, raw, now=1.0, config_json=cfg)
    out = PL.run_pipeline(conn, cid, raw, call=FakeCall(sample_script()), now=lambda: 1.0)
    items = out["entries"] + out["amounts"] + out["flags"]
    live = [i for i in items if i["state"] != "rejected"]
    assert live and all(i["state"] == "needs_review" and "OCR_DERIVED" in i["reasons"] for i in live)
    assert out["counts"]["verified"] == 0
    stored = [r for k in ("entry", "amount", "flag") for r in DB.list_items(conn, cid, k) if r["state"] != "rejected"]
    assert stored and all(r["state"] == "needs_review" and "OCR_DERIVED" in r["state_reasons"] for r in stored)


def test_a_text_layer_pdf_run_is_unchanged_by_the_ocr_marking(tmp_path):
    raw = G.raw("sample")
    conn = DB.connect(str(tmp_path / "n.sqlite"))
    cid = DB.create_case(conn, raw, now=1.0, config_json={"source_pdf": True, "pages": [{"page": 1, "start": 0, "end": len(raw)}]})
    out = PL.run_pipeline(conn, cid, raw, call=FakeCall(sample_script()), now=lambda: 1.0)
    assert out["counts"]["verified"] > 0 and not any("OCR_DERIVED" in i["reasons"] for i in out["entries"])


def test_requirements_pin_pypdfium2_exactly():
    import pathlib
    txt = (pathlib.Path(__file__).resolve().parents[2] / "requirements.txt").read_text()
    assert "pypdfium2==5.14.0" in txt.splitlines()
