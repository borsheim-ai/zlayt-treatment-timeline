"""T-086 round 2 (security review): OCR render limits (pixels, memory, stored bytes), the scrubbed tesseract environment, and a tighter
subprocess allow-list check. SYNTHETIC files only; the tests that would need the Tesseract binary mock it."""
import pathlib
import re
import subprocess
import sys

import pytest

from app.backend import pdf_checks, pdf_ocr, pdf_text
from tests.unit._pdf_raw import build

pytest.importorskip("pypdfium2")
ROOT = pathlib.Path(__file__).resolve().parents[2]
READY = {"available": True, "version": "5.5.2", "tested_version": "5.5.2", "languages": ["eng"], "message": "ok"}


def _big_blank(side_pt):
    return build(b"0.5 g 10 10 100 100 re f", mediabox=f"0 0 {side_pt} {side_pt}")


def _fake_tesseract(monkeypatch):
    monkeypatch.setattr(pdf_ocr, "ocr_status", lambda: READY)
    monkeypatch.setattr(pdf_ocr, "ocr_png", lambda png, **k: {"text": "SYNTHETIC page text for the test.", "words": [], "low_conf": [], "mean_conf": 90.0})


def test_render_scale_caps_both_sides_and_area():
    assert pdf_ocr.render_scale(612, 792) == pytest.approx(150 / 72)                     # US Letter is rendered at the full DPI
    s = pdf_ocr.render_scale(2800, 2800)
    assert 2800 * s <= pdf_ocr.MAX_SIDE_PX and (2800 * s) ** 2 <= pdf_ocr.MAX_PIXELS * 1.01
    for bad in ((14400, 14400), (3000, 100), (0, 0), (-5, 10)):
        with pytest.raises(pdf_ocr.OcrFailed) as e:
            pdf_ocr.render_scale(*bad)
        assert e.value.reason == "page_too_large"


def test_a_14400_pt_page_is_refused_with_a_clear_code_and_page_number(monkeypatch):
    _fake_tesseract(monkeypatch)
    data = _big_blank(14400)
    assert len(data) < 2000                                                              # the reviewer's 1 KB bomb
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(data, ocr=True)
    assert e.value.code == "ocr_page_too_large" and e.value.detail == {"page": 1}
    assert "40 inches" in pdf_checks.MESSAGES["ocr_page_too_large"]


def test_a_page_just_under_the_limit_is_rendered_smaller_not_refused(monkeypatch):
    _fake_tesseract(monkeypatch)
    got = pdf_checks.extract(_big_blank(2800), ocr=True)
    assert got["pdf_checks"]["ocr"]["ran"] and 1 in got["page_images"]


def test_stored_page_images_are_capped_in_total(monkeypatch):
    _fake_tesseract(monkeypatch)
    monkeypatch.setattr(pdf_ocr, "MAX_STORED_PNG_BYTES", 100)
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(_big_blank(600), ocr=True)
    assert e.value.code == "ocr_images_too_large" and e.value.detail == {"page": 1}


def test_rendering_a_large_allowed_page_stays_under_a_memory_cap():
    """A page at the largest allowed size (2800 pt = 38.9 in) renders in a child process; its peak RSS stays small (the unbounded render took 2.3 GB)."""
    code = (
        "import resource, sys\n"
        "sys.path.insert(0, %r)\n"
        "import pypdfium2 as p\n"
        "from app.backend import pdf_ocr\n"
        "from tests.unit.test_pdf_ocr_limits import _big_blank\n"
        "png = pdf_ocr.render_page_png(p.PdfDocument(_big_blank(2800)), 0)\n"
        "print(len(png), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)\n" % str(ROOT))
    out = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=120, cwd=str(ROOT))
    assert out.returncode == 0, out.stderr[-400:]
    size, rss = (int(x) for x in out.stdout.split())
    rss_mb = rss / (1024 * 1024) if sys.platform == "darwin" else rss / 1024
    assert rss_mb < 300 and size < pdf_ocr.MAX_STORED_PNG_BYTES


def test_png_is_valid_and_streamed_row_by_row():
    rows = [bytes([i % 256]) * 7 for i in range(5)]
    png = pdf_ocr._png(iter(rows), 7, 5)
    assert png[:8] == b"\x89PNG\r\n\x1a\n" and png.endswith(b"IEND\xaeB`\x82")
    import zlib
    idat = png[png.index(b"IDAT") + 4:png.index(b"IEND") - 8]
    assert zlib.decompress(idat) == b"".join(b"\x00" + r for r in rows)


# ---- the tesseract environment ----
def test_tesseract_runs_with_a_scrubbed_environment(monkeypatch):
    for k, v in {"ANTHROPIC_API_KEY": "test-value", "OPENAI_API_KEY": "x", "GITHUB_TOKEN": "y", "AWS_SECRET_ACCESS_KEY": "z", "HOME": "/home/x",
                 "TESSDATA_PREFIX": "/tessdata", "PATH": "/usr/bin"}.items():
        monkeypatch.setenv(k, v)
    seen = []

    def fake_run(argv, **kw):
        seen.append(kw["env"])
        return subprocess.CompletedProcess(argv, 0, stdout="level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n", stderr="")
    monkeypatch.setattr(pdf_ocr.subprocess, "run", fake_run)
    monkeypatch.setattr(pdf_ocr, "_which", lambda: "/usr/bin/tesseract")
    pdf_ocr.ocr_png(b"x", status=READY)
    assert seen and all(set(e) <= set(pdf_ocr._ENV_KEEP) | {"OMP_THREAD_LIMIT"} for e in seen)
    assert seen[0]["TESSDATA_PREFIX"] == "/tessdata" and seen[0]["OMP_THREAD_LIMIT"] == "1"
    assert not any(k.endswith(("_KEY", "_TOKEN")) or "SECRET" in k or k == "HOME" for k in seen[0])
    monkeypatch.setattr(pdf_ocr.shutil, "which", lambda n: "/usr/bin/tesseract")
    seen.clear()
    pdf_ocr.ocr_status()
    assert seen and all("ANTHROPIC_API_KEY" not in e for e in seen)


def test_pdf_ocr_has_no_other_way_to_start_a_process():
    src = pathlib.Path(pdf_ocr.__file__).read_text()
    code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith(("#", '"""')))
    assert not re.search(r"shell\s*=\s*True|Popen|os\.system|os\.popen|os\.exec|os\.spawn|pty\.", code)
    calls = [m.start() for m in re.finditer(r"subprocess\.run\(", code)]
    assert calls and all("timeout=" in code[i:code.index("\n", code.index(")", i))] + code[i:i + 400] for i in calls)
