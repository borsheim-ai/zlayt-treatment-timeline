"""T-086: local OCR of scanned PDF pages. Tests that need the Tesseract binary skip cleanly when it is not installed; the rest
(missing-binary message, TSV parsing, low-confidence rule, needs_review marking) run everywhere. All text is SYNTHETIC."""
import pathlib
import shutil

import pytest

from app.backend import pdf_checks, pdf_ocr, pdf_text
from tests.unit._pdf_raw import build, scanned_copy, text_page
from tests.unit.spawn_audit import audit, spawn_keys

pytest.importorskip("pypdfium2")
needs_tesseract = pytest.mark.skipif(not shutil.which("tesseract"), reason="tesseract is not installed")

LINES = ["SYNTHETIC CLINIC NOTE", "Date: 03/04/2023", "Patient reports neck pain.", "Charge: $1,250.00 for MRI cervical spine."]


def scan_pdf():
    return scanned_copy(build(text_page(LINES, size=18, lead=30, y=700)))


# ---- no tesseract: a clear message, never a crash ----
def test_missing_tesseract_gives_a_clear_message(monkeypatch):
    monkeypatch.setattr(pdf_ocr.shutil, "which", lambda name: None)
    st = pdf_ocr.ocr_status()
    assert st["available"] is False and "brew install tesseract" in st["message"] and "apt-get install tesseract-ocr" in st["message"]
    with pytest.raises(pdf_ocr.OcrUnavailable):
        pdf_ocr.ocr_png(b"x")


def test_ocr_requested_without_tesseract_is_a_pdf_error_with_the_message_not_a_crash(monkeypatch):
    monkeypatch.setattr(pdf_ocr.shutil, "which", lambda name: None)
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(scan_pdf(), ocr=True)
    assert e.value.code == "ocr_unavailable" and "Tesseract" in e.value.detail["message"]


def test_scanned_pdf_without_ocr_is_refused_and_says_ocr_could_read_it():
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_text.extract(scan_pdf())
    assert e.value.code == "pdf_no_text_layer" and e.value.detail["scanned_pages"] == [1]
    assert "available" in e.value.detail["ocr"]


# ---- parsing and the low-confidence rule (no binary needed) ----
TSV = ("level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"
       "1\t1\t0\t0\t0\t0\t0\t0\t100\t100\t-1\t\n"
       "5\t1\t1\t1\t1\t1\t0\t0\t10\t10\t96.5\tPatient\n"
       "5\t1\t1\t1\t1\t2\t0\t0\t10\t10\t41.0\treports\n"
       "5\t1\t1\t1\t2\t1\t0\t0\t10\t10\t90.0\tpain\n"
       "5\t1\t2\t1\t1\t1\t0\t0\t10\t10\t95.0\t$1,250.00\n"
       "5\t1\t2\t1\t1\t2\t0\t0\t10\t10\t75.0\t03/04/2023\n")


def test_tsv_rebuilds_lines_and_exact_word_offsets():
    got = pdf_ocr._parse_tsv(TSV)
    assert got["text"] == "Patient reports\npain\n\n$1,250.00 03/04/2023"
    for w in got["words"]:
        assert got["text"][w["start"]:w["end"]] == w["text"]


def test_low_confidence_words_are_marked_numbers_need_more_confidence():
    words = pdf_ocr._parse_tsv(TSV)["words"]
    low = [w["text"] for w in words if pdf_ocr.is_low(w)]
    assert low == ["reports", "03/04/2023"]            # 41 < 60; a date at 75 < 80 because it has digits; "pain" at 90 is fine


# ---- OCR-derived items are always needs_review ----
def test_ocr_items_become_needs_review_with_the_reason_and_stay_that_way():
    pages = [{"page": 1, "start": 0, "end": 50}, {"page": 2, "start": 52, "end": 100, "source": "ocr"}]
    recs = [{"n": 1, "char_start": 0, "char_end": 40}, {"n": 2, "char_start": 52, "char_end": 90}]
    items = [{"id": "e1", "record_ids": ["r1"], "state": "verified", "reasons": [], "why": ""},
             {"id": "e2", "record_ids": ["r2"], "state": "verified", "reasons": [], "why": "", "ladder": {"state": "verified"}},
             {"id": "a2", "record_ids": ["r2"], "state": "rejected", "reasons": ["SCHEMA_INVALID"], "why": "x"},
             {"id": "f2", "record_ids": ["r1", "r2"], "state": "needs_review", "reasons": ["LLM_ONLY"], "why": "ai only"}]
    assert pdf_checks.mark_ocr_items(items, recs, pages, "Read by OCR.") == 2
    assert items[0]["state"] == "verified"
    assert items[1]["state"] == "needs_review" and items[1]["reasons"] == ["OCR_DERIVED"] and items[1]["ladder"]["state"] == "needs_review"
    assert items[2]["state"] == "rejected" and items[2]["reasons"] == ["SCHEMA_INVALID"]
    assert items[3]["reasons"] == ["LLM_ONLY", "OCR_DERIVED"] and items[3]["why"] == "ai only Read by OCR."
    assert pdf_checks.mark_ocr_items(items, recs, pages, "Read by OCR.") == 2 and items[3]["reasons"].count("OCR_DERIVED") == 1


def test_no_ocr_page_means_no_change():
    items = [{"id": "e", "record_ids": ["r1"], "state": "verified", "reasons": []}]
    assert pdf_checks.mark_ocr_items(items, [{"n": 1, "char_start": 0, "char_end": 9}], [{"page": 1, "start": 0, "end": 9}], "x") == 0
    assert items[0]["state"] == "verified"


# ---- the real binary ----
@needs_tesseract
def test_status_reports_the_installed_version():
    st = pdf_ocr.ocr_status()
    assert st["available"] and st["version"] and "eng" in st["languages"]


@needs_tesseract
def test_scanned_page_is_ocrd_locally_with_page_image_low_conf_and_page_marked():
    got = pdf_checks.extract(scan_pdf(), ocr=True)
    assert "neck pain" in got["text"] and "03/04/2023" in got["text"]
    pg = got["pages"][0]
    assert pg["source"] == "ocr" and pg["has_image"] and pg["mean_conf"] > 60
    assert got["page_images"][1].startswith("iVBOR")                           # base64 PNG beside the OCR text
    for w in pg["low_conf"]:
        assert got["text"][w["start"]:w["end"]] == w["text"] and w["conf"] < pdf_ocr.LOW_CONF_NUMBER
    o = got["pdf_checks"]["ocr"]
    assert o["ran"] and o["pages"] == [1] and o["items_need_review"] and o["engine"].startswith("tesseract")
    assert o["low_conf_words"] == pg["low_conf_count"]


@needs_tesseract
def test_a_poor_scan_marks_its_unsure_words_and_a_clean_scan_marks_none():
    clean = pdf_checks.extract(scan_pdf(), ocr=True)["pages"][0]
    assert clean["low_conf_count"] == 0
    poor = pdf_checks.extract(scanned_copy(build(text_page(LINES, size=9, lead=14, y=700)), scale=0.7), ocr=True)
    pg = poor["pages"][0]
    assert pg["mean_conf"] < 70 and pg["low_conf_count"] >= 5
    assert all(poor["text"][w["start"]:w["end"]] == w["text"] for w in pg["low_conf"])
    assert poor["pdf_checks"]["ocr"]["low_conf_words"] == pg["low_conf_count"]


@needs_tesseract
def test_too_many_scanned_pages_are_refused_not_partly_read(monkeypatch):
    monkeypatch.setattr(pdf_ocr, "MAX_OCR_PAGES", 0)
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(scan_pdf(), ocr=True)
    assert e.value.code == "ocr_too_many_pages"


def test_pdf_ocr_only_runs_tesseract():
    """pdf_ocr.py runs a local OCR binary, never an LLM (T-086). The AST audit in spawn_audit.py enforces it: no claude, anthropic or
    app.llm reference; every spawn starts the Tesseract path from _which(), and `exe` is only ever bound to _which()."""
    src = pathlib.Path(pdf_ocr.__file__).read_text()
    assert audit(src, "pdf_ocr") == []
    assert spawn_keys(src) == ["expr:exe", "expr:exe", "expr:_which()"]


OCR_BYPASSES = {
    "exe_rebound": "exe = 'curl'\n",
    "ps_probe": "import subprocess\nsubprocess.run(['ps', '-A'])\n",
    "interpreter_probe": "import subprocess, sys\nsubprocess.run([sys.executable, '-m', 'app.backend.pdf_ocr'])\n",
    "claude_program": "import subprocess\nsubprocess.run(['claude', '-p', 'x'])\n",
    "from_import_alias": "from subprocess import check_output as co\nco(['/usr/bin/curl', 'x'])\n",
    "llm_import": "from app.llm import provider\n",
}


@pytest.mark.parametrize("snippet", list(OCR_BYPASSES.values()), ids=list(OCR_BYPASSES))
def test_pdf_ocr_audit_rejects_bypass(snippet):
    src = pathlib.Path(pdf_ocr.__file__).read_text() + "\n" + snippet
    assert audit(src, "pdf_ocr"), "the audit let this through"


def test_an_ocr_item_trace_has_the_ocr_source_step(tmp_path):
    from app.backend import trace
    from app.db import db as DB
    from tests.unit import _golden as G
    from tests.unit._fakes import FakeCall, sample_script
    from app.backend import pipeline as PL
    raw = G.raw("sample")
    conn = DB.connect(str(tmp_path / "t.sqlite"))
    cid = DB.create_case(conn, raw, now=1.0, config_json={"source_pdf": True, "pages": [{"page": 1, "start": 0, "end": len(raw), "source": "ocr"}]})
    out = PL.run_pipeline(conn, cid, raw, call=FakeCall(sample_script()), now=lambda: 1.0)
    t = trace.item_trace(conn, cid, out["entries"][0]["id"])
    s = next(x for x in t["steps"] if x["id"] == "ocr_source")
    assert s["status"] == "fail" and s["reason_code"] == "OCR_DERIVED" and s["next_action"]["code"] == "READ_RECORD"
