"""T-087 round 4 (security review r3): the pypdf text read runs in the same killed child as the scan; at most two PDF jobs run at once and
the rest get a 429; an opaque Popup annotation over text counts as a cover; a parent-side RSS watch kills a scan child that grows past the
limit (macOS has no RLIMIT_AS). The constructions are the reviewer's probe files (probe_r3_textbomb.py 6 tj, probe_r3_minor.py
C_Popup_opaque_AP_cover, probe_r3_apbomb.py), rebuilt here. SYNTHETIC text only."""
import os
import subprocess
import threading
import time
import zlib

import pytest
from fastapi.testclient import TestClient

from app.backend import pdf_checks, pdf_hidden, pdf_text
from app.backend.api import create_app
from tests.unit import _pdf_probe as K
from tests.unit.test_pdf_hidden_r3 import COVER_AP, PLAIN, annot_pdf, held

pytest.importorskip("pypdfium2")
PDF = {"content-type": "application/pdf"}


def text_bomb(mb=6):
    """One page whose content stream inflates to `mb` MB of `(a) Tj` operators: about 10 KB on disk, 25 s of pypdf CPU and 300 MB at 6 MB."""
    body = b"BT /F1 12 Tf 10 10 Td\n" + b"(a) Tj\n" * (mb * 1024 * 1024 // 7) + b"ET\n"
    return K.one_page(body, flate=True)


def _children():
    out = subprocess.run(["pgrep", "-P", str(os.getpid())], capture_output=True, text=True).stdout.split()
    return [p for p in out if p]


def _rss_mb():
    return pdf_hidden._rss_bytes(os.getpid()) / 1024 ** 2


@pytest.fixture
def live(tmp_path, monkeypatch):
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return TestClient(create_app(str(tmp_path / "t.sqlite"), static_dir=str(tmp_path)))


# ---- Major 1: no PDF parsing in the API process ----
def test_the_text_bomb_is_ten_kb_on_disk():
    assert len(text_bomb()) < 20_000


def test_the_api_process_never_runs_the_pypdf_read(monkeypatch):
    def refuse(*a, **k):
        raise AssertionError("pypdf text read ran in the API process")
    monkeypatch.setattr(pdf_text, "read_pages", refuse)
    got = pdf_checks.extract(K.one_page(K.VISIBLE))
    assert "Visible clinic note" in got["text"]
    assert pdf_text.extract_text_layer(K.one_page(K.VISIBLE))["text"].startswith("Visible clinic note")


def test_text_bomb_is_a_400_at_the_deadline_and_cpu_and_rss_are_flat_afterwards(live, monkeypatch):
    monkeypatch.setattr(pdf_text, "EXTRACT_TIMEOUT_S", 3.0)
    data = text_bomb()
    rss0, cpu0, t = _rss_mb(), time.process_time(), time.monotonic()
    r = live.post("/api/cases/pdf", content=data, headers=PDF)
    assert r.status_code == 400 and r.json()["error"]["detail"]["reason"] == "pdf_timeout" and time.monotonic() - t < 6.0
    time.sleep(1.0)
    cpu1, rss1 = time.process_time(), _rss_mb()
    time.sleep(4.0)
    assert time.process_time() - cpu1 < 0.5, "the API process kept working after the 400"
    assert abs(_rss_mb() - rss1) < 20 and rss1 - rss0 < 100
    assert _children() == []
    assert cpu1 - cpu0 < 4.0                               # the parent itself did next to nothing; the work was in the killed child


def test_six_concurrent_text_bombs_two_run_four_are_busy_and_health_stays_fast(live, monkeypatch):
    monkeypatch.setattr(pdf_text, "EXTRACT_TIMEOUT_S", 4.0)
    data = text_bomb()
    results, health = [], []

    def post():
        results.append(live.post("/api/cases/pdf", content=data, headers=PDF))
    rss0 = _rss_mb()
    ts = [threading.Thread(target=post) for _ in range(6)]
    t0 = time.monotonic()
    for t in ts:
        t.start()
    while any(t.is_alive() for t in ts) and time.monotonic() - t0 < 15:
        s = time.monotonic()
        assert live.get("/api/health").status_code == 200
        health.append(time.monotonic() - s)
        time.sleep(0.1)
    for t in ts:
        t.join(15)
    codes = sorted(r.status_code for r in results)
    assert codes == [400, 400, 429, 429, 429, 429], codes
    busy = next(r for r in results if r.status_code == 429).json()["error"]
    assert busy["code"] == "busy" and busy["detail"]["reason"] == "pdf_busy"
    assert max(health) < 1.0, max(health)
    time.sleep(1.0)
    assert _children() == [] and _rss_mb() - rss0 < 100
    cpu = time.process_time()
    time.sleep(3.0)
    assert time.process_time() - cpu < 0.5
    assert live.post("/api/cases/pdf", content=K.one_page(K.VISIBLE), headers=PDF).status_code == 201      # the slots came back


def test_pdf_jobs_are_capped_at_two(monkeypatch):
    assert pdf_checks.MAX_PDF_JOBS == 2 and pdf_hidden.MAX_CHILDREN == 2
    monkeypatch.setattr(pdf_checks, "BUSY_WAIT_S", 0.05)
    held_slots = [pdf_checks._JOBS.acquire() for _ in range(2)]
    try:
        with pytest.raises(pdf_text.PdfError) as e:
            pdf_checks.extract(K.one_page(K.VISIBLE))
        assert e.value.code == "pdf_busy"
    finally:
        for _ in held_slots:
            pdf_checks._JOBS.release()
    assert "Visible" in pdf_checks.extract(K.one_page(K.VISIBLE))["text"]


def test_a_refusal_from_the_text_read_comes_back_as_the_same_error_code():
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(b"not a pdf at all")
    assert e.value.code == "pdf_unreadable"
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(b"%PDF-1.4\n" + b"x" * (pdf_text.MAX_PDF_BYTES + 1))
    assert e.value.code == "pdf_too_large"


# ---- Major 2: Popup ----
POPUP_BODY = b"<< /Type /Annot /Subtype /Popup /Rect [0 690 600 720] /F 4 /AP << /N 6 0 R >> >>"       # reviewer's C_Popup_opaque_AP_cover


def test_opaque_popup_over_text_holds_the_text_back_and_lists_the_page():
    text, page = held(annot_pdf(POPUP_BODY))
    assert "PLANTED" not in text and "Visible clinic note" in text
    assert page["page"] == 1 and page["excluded"] and any("covered_by_annotation" in i["reasons"] for i in page["items"])
    assert "PLANTED" in pdf_checks.extract(annot_pdf(POPUP_BODY), include_hidden="1")["text"]


def test_popup_with_a_parent_and_no_appearance_is_not_a_false_positive():
    body = b"<< /Type /Annot /Subtype /Popup /Parent 8 0 R /Rect [0 690 600 720] /F 4 /Open false >>"
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Contents 4 0 R /Annots [7 0 R 8 0 R] /Resources << /Font << /F1 5 0 R >> >> >>",
            K.stream(K.VISIBLE + PLAIN), K.FONT, COVER_AP, body,
            b"<< /Type /Annot /Subtype /Text /Popup 7 0 R /Rect [560 770 580 790] /F 28 /Contents (a comment) >>"]
    got = pdf_checks.extract(K.pdf(objs))
    assert "PLANTED" in got["text"] and got["pdf_checks"]["hidden_text"]["pages"] == []


def test_popup_with_no_appearance_over_text_is_not_held():
    body = b"<< /Type /Annot /Subtype /Popup /Rect [0 690 600 720] /F 4 >>"
    got = pdf_checks.extract(annot_pdf(body))
    assert "PLANTED" in got["text"] and got["pdf_checks"]["hidden_text"]["pages"] == []


# ---- Minor: parent-side RSS watch ----
def ap_bomb(mb):
    """A Stamp annotation whose appearance stream inflates to `mb` MB (pypdf never reads annotation appearances, PDFium decodes them)."""
    co = zlib.compressobj(9)
    parts = [co.compress(b"\x00" * (1024 * 1024)) for _ in range(mb)] + [co.flush()]
    z = b"".join(parts)
    ap = (f"<< /Type /XObject /Subtype /Form /BBox [0 0 600 30] /Filter /FlateDecode /Length {len(z)} >>\nstream\n").encode() + z + b"\nendstream"
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Contents 4 0 R /Annots [7 0 R] /Resources << /Font << /F1 5 0 R >> >> >>",
            K.stream(K.VISIBLE + PLAIN), K.FONT, ap,
            b"<< /Type /Annot /Subtype /Stamp /Rect [0 690 600 720] /F 4 /AP << /N 6 0 R >> >>"]
    return K.pdf(objs)


def test_rss_of_a_process_is_readable_and_missing_pid_is_zero():
    assert pdf_hidden._rss_bytes(os.getpid()) > 10 * 1024 ** 2
    assert pdf_hidden._rss_bytes(2 ** 22 - 3) == 0


def test_child_that_outgrows_the_rss_limit_is_killed_and_the_pages_are_unchecked(monkeypatch):
    monkeypatch.setattr(pdf_hidden, "CHILD_RSS_BYTES", 400 * 1024 ** 2)
    data = ap_bomb(1500)
    assert len(data) < 3 * 1024 ** 2
    t = time.monotonic()
    with pytest.raises(pdf_hidden.HiddenScanUnavailable) as e:
        pdf_hidden.scan(data, deadline=time.monotonic() + 30, with_text=True)
    assert str(e.value) == "memory" and e.value.texts is not None and "Visible clinic note" in e.value.texts[0]
    assert time.monotonic() - t < 20 and _children() == []
    with pytest.raises(pdf_text.PdfError) as pe:                    # extract keeps the page out of the case: nothing is included silently
        pdf_checks.extract(data)
    assert pe.value.code == "pdf_only_hidden_text" and pe.value.detail["unchecked_pages"] == [1]
    got = pdf_checks.extract(data, include_hidden="all")
    assert got["pdf_checks"]["hidden_text"]["pages"][0]["unchecked"] is True


def test_normal_files_stay_far_below_the_rss_limit():
    assert pdf_hidden.CHILD_RSS_BYTES >= 1024 ** 3
    pdf_hidden.scan(K.one_page(K.VISIBLE), with_text=True)
