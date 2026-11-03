"""T-107 (T-087 round 4 major): with ocr=true the page rendering runs in the same killed child as the hidden-text scan, a child that is
killed or fails makes the upload a 400 and is never retried in the API process, and no PDFium or pypdf call exists in the API process.
The bomb is the reviewer's: a ~3 MB Stamp annotation whose appearance stream inflates to GBs (here 1500 MB, with the RSS ceiling lowered).
SYNTHETIC text only."""
import ast
import os
import pathlib
import shutil
import threading
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import pdf_checks, pdf_hidden, pdf_ocr, pdf_text
from app.backend.api import create_app
from tests.unit import _pdf_probe as K
from tests.unit.test_pdf_hidden_r4 import ap_bomb, _children, _rss_mb
from tests.unit.test_pdf_ocr import scan_pdf

pypdfium2 = pytest.importorskip("pypdfium2")
PDF = {"content-type": "application/pdf"}
needs_tesseract = pytest.mark.skipif(not shutil.which("tesseract"), reason="tesseract is not installed")
APP = pathlib.Path(pdf_checks.__file__).resolve().parents[1]


@pytest.fixture
def live(tmp_path, monkeypatch):
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return TestClient(create_app(str(tmp_path / "t.sqlite"), static_dir=str(tmp_path)))


@pytest.fixture
def spies(monkeypatch):
    """Record every PDFium / pypdf open in THIS process (the child is another process and is not affected)."""
    import pypdf
    calls = []

    def spy(name, real):
        def f(*a, **k):
            calls.append(name)
            return real(*a, **k)
        return f
    monkeypatch.setattr(pypdfium2, "PdfDocument", spy("PdfDocument", pypdfium2.PdfDocument))
    monkeypatch.setattr(pypdf, "PdfReader", spy("PdfReader", pypdf.PdfReader))
    return calls


# ---- static: where the parsers may be imported ----
def test_pdfium_and_pypdf_are_imported_only_inside_the_child_functions():
    allowed = {("pdf_hidden.py", "scan_inprocess"), ("pdf_text.py", "read_pages"), ("pdf_ocr.py", "render_in_child")}
    found = set()
    for path in APP.rglob("*.py"):
        tree = ast.parse(path.read_text())
        for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))] + [tree]:
            body = fn.body if fn is not tree else tree.body
            for stmt in body:
                for node in ast.walk(stmt) if fn is not tree else ([stmt] if isinstance(stmt, (ast.Import, ast.ImportFrom)) else []):
                    mods = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
                    if any(m.split(".")[0] in ("pypdf", "pypdfium2") for m in mods):
                        found.add((path.name, getattr(fn, "name", "<module>")))
    assert found <= allowed, f"PDF parser imported outside the child code: {found - allowed}"
    assert ("pdf_ocr.py", "render_in_child") in found


def test_render_in_child_is_only_reached_from_the_child_main():
    callers = []
    for path in APP.rglob("*.py"):
        for line in path.read_text().splitlines():
            if "render_in_child(" in line and "def render_in_child" not in line:
                callers.append((path.name, line.strip()))
    assert [c[0] for c in callers] == ["pdf_hidden.py"], callers
    assert "_child_main" in (APP / "backend" / "pdf_hidden.py").read_text().split("render_in_child(")[0].rsplit("def ", 1)[1]


# ---- fail closed: a child that was killed or failed is never retried in the API process ----
def test_a_killed_scan_child_with_ocr_is_refused_and_ocr_never_runs(monkeypatch, spies):
    def killed(*a, **k):
        raise pdf_hidden.HiddenScanUnavailable("memory", ["x" * 30])
    monkeypatch.setattr(pdf_hidden, "scan", killed)
    monkeypatch.setattr(pdf_ocr, "ocr_pages", lambda *a, **k: pytest.fail("OCR ran on a file whose scan child was killed"))
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(K.one_page(K.VISIBLE), ocr=True)
    assert e.value.code == "ocr_check_failed" and e.value.detail == {"cause": "memory"}
    assert spies == []


@pytest.mark.parametrize("why", ["memory", "child_failed", "child_died"])
def test_every_scan_child_failure_with_ocr_is_a_400_with_a_plain_reason(live, monkeypatch, spies, why):
    monkeypatch.setattr(pdf_hidden, "scan", lambda *a, **k: (_ for _ in ()).throw(pdf_hidden.HiddenScanUnavailable(why, ["t" * 40])))
    r = live.post("/api/cases/pdf?ocr=true", content=K.one_page(K.VISIBLE), headers=PDF)
    assert r.status_code == 400 and r.json()["error"]["detail"]["reason"] == "ocr_check_failed"
    assert "could not be checked safely" in r.json()["error"]["message"] and spies == []


@pytest.mark.parametrize("why", ["memory", "child_failed"])
def test_a_killed_render_child_is_ocr_failed_and_there_is_no_fallback(monkeypatch, spies, why):
    monkeypatch.setattr(pdf_ocr, "ocr_status", lambda: {"available": True, "version": "5.5.2", "languages": ["eng"], "message": ""})
    monkeypatch.setattr(pdf_hidden, "render_messages", lambda *a, **k: (_ for _ in ()).throw(pdf_hidden.HiddenScanUnavailable(why)))
    monkeypatch.setattr(pdf_ocr, "render_page_png", lambda *a, **k: pytest.fail("rendered in the API process"))
    data = scan_pdf()
    spies.clear()                  # the fixture builder itself may open a document; only the calls after this point count
    with pytest.raises(pdf_ocr.OcrFailed) as e:
        pdf_ocr.ocr_pages(data, [1])
    assert e.value.reason == "render_killed" and spies == []


def test_a_render_that_hits_the_deadline_is_a_timeout_not_a_fallback(monkeypatch, spies):
    monkeypatch.setattr(pdf_ocr, "ocr_status", lambda: {"available": True, "version": "5.5.2", "languages": ["eng"], "message": ""})
    monkeypatch.setattr(pdf_hidden, "render_messages", lambda *a, **k: (_ for _ in ()).throw(pdf_hidden.HiddenScanTimeout("deadline")))
    data = scan_pdf()
    spies.clear()
    with pytest.raises(pdf_ocr.OcrFailed) as e:
        pdf_ocr.ocr_pages(data, [1])
    assert e.value.reason == "timeout" and spies == []


# ---- the render really happens in the child, under the same watchdog ----
@needs_tesseract
def test_a_scanned_pdf_with_ocr_renders_in_the_child_and_the_api_process_opens_no_pdf(live, spies):
    data = scan_pdf()
    spies.clear()
    r = live.post("/api/cases/pdf?ocr=true", content=data, headers=PDF)
    assert r.status_code == 201, r.text
    assert r.json()["pdf_checks"]["ocr"]["ran"] is True
    assert spies == [], f"PDF parser called in the API process: {spies}"


def test_the_render_child_stops_on_the_rss_ceiling_with_the_reviewers_bomb(monkeypatch, spies):
    """The render child alone (the scan is skipped): a Stamp appearance that inflates to GBs is killed by the RSS watch and the API
    process neither renders it nor grows."""
    monkeypatch.setattr(pdf_hidden, "CHILD_RSS_BYTES", 400 * 1024 ** 2)
    monkeypatch.setattr(pdf_ocr, "ocr_status", lambda: {"available": True, "version": "5.5.2", "languages": ["eng"], "message": ""})
    data = ap_bomb(1500)
    assert len(data) < 3 * 1024 ** 2
    rss0, t = _rss_mb(), time.monotonic()
    with pytest.raises(pdf_ocr.OcrFailed) as e:
        pdf_ocr.ocr_pages(data, [1], deadline=time.monotonic() + 30)
    assert e.value.reason == "render_killed" and time.monotonic() - t < 20
    assert _rss_mb() - rss0 < 150 and _children() == [] and spies == []


def test_the_bomb_with_ocr_true_is_a_400_and_the_api_rss_stays_flat(live, monkeypatch, spies):
    monkeypatch.setattr(pdf_hidden, "CHILD_RSS_BYTES", 400 * 1024 ** 2)
    data = ap_bomb(1500)
    rss0, t = _rss_mb(), time.monotonic()
    peak, stop = [rss0], threading.Event()

    def sample():
        while not stop.is_set():
            peak[0] = max(peak[0], _rss_mb())
            time.sleep(0.05)
    th = threading.Thread(target=sample, daemon=True)
    th.start()
    r = live.post("/api/cases/pdf?ocr=true", content=data, headers=PDF)
    time.sleep(1.0)
    stop.set()
    th.join()
    assert r.status_code == 400 and r.json()["error"]["detail"]["reason"] in ("ocr_check_failed", "ocr_render_failed"), r.text
    assert time.monotonic() - t < 25 and peak[0] - rss0 < 200, f"API RSS grew {peak[0] - rss0:.0f} MB"
    assert _children() == [] and spies == []


def test_two_concurrent_bombs_with_ocr_are_400_or_429_and_the_api_rss_stays_flat(live, monkeypatch, spies):
    monkeypatch.setattr(pdf_hidden, "CHILD_RSS_BYTES", 400 * 1024 ** 2)
    data, results = ap_bomb(1500), []
    rss0 = _rss_mb()

    def post():
        r = live.post("/api/cases/pdf?ocr=true", content=data, headers=PDF)
        results.append(r.status_code)
    ths = [threading.Thread(target=post) for _ in range(2)]
    for th in ths:
        th.start()
    peak = rss0
    while any(th.is_alive() for th in ths):
        peak = max(peak, _rss_mb())
        time.sleep(0.05)
    assert sorted(results) and all(c in (400, 429) for c in results), results
    assert peak - rss0 < 250 and _children() == [] and spies == []
