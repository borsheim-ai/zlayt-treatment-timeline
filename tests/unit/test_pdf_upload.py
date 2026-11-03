"""PDF text-layer upload (D-031, T-054): same records as paste, page-mapped citations, scanned PDFs refused with no LLM call."""
import re
import pytest
from fastapi.testclient import TestClient
from app.backend import export as X, ingest as I, pdf_text as PT
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._pdf import make_pdf, sample_pdf
from tests.unit.test_export import build_case


def _norm(s):
    return " ".join(s.split())


def test_text_pdf_of_the_sample_gives_the_same_nine_records_as_paste():
    """AC1: records, header dates, labels and excerpts equal the pasted sample; every excerpt is verbatim in the extracted text."""
    got = PT.extract(sample_pdf(G.raw("sample")))
    pdf, paste = I.ingest(got["text"]), I.ingest(G.raw("sample"))
    assert len(pdf["records"]) == 9 and pdf["split_method"] == "code" and not [w for w in pdf["warnings"] if w["code"] == "SPLIT_AMBIGUOUS"]
    for a, b in zip(pdf["records"], paste["records"]):
        assert (a["date_raw"], a["source"], _norm(a["excerpt"])) == (b["date_raw"], b["source"], _norm(b["excerpt"]))
        assert a["excerpt"] in got["text"]
    assert pdf["groups"] == paste["groups"]


def test_pages_map_records_to_page_numbers():
    got = PT.extract(sample_pdf(G.raw("sample"), split_after_record=5))
    recs = I.ingest(got["text"])["records"]
    assert [PT.page_for(got["pages"], r["char_start"]) for r in recs] == [1, 1, 1, 1, 1, 2, 2, 2, 2]
    assert PT.page_for([], 5) is None and got["text"][got["pages"][1]["start"]:].startswith("=== Record 6 ===")


@pytest.mark.parametrize("data,code", [
    (make_pdf([["x"]], image_only=True), "pdf_no_text_layer"),
    (make_pdf([["   "]]), "pdf_no_text_layer"),
    (b"not a pdf at all", "pdf_unreadable"),
    (b"%PDF-1.4\ngarbage", "pdf_unreadable"),
    (b"%PDF-" + b"0" * (PT.MAX_PDF_BYTES + 1), "pdf_too_large"),
])
def test_unusable_pdfs_are_refused_with_a_reason(data, code):
    """AC2: scanned / no-text / unreadable / oversize files raise a coded error; nothing is guessed or OCR'd."""
    with pytest.raises(PT.PdfError) as e:
        PT.extract(data)
    assert e.value.code == code


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")     # local live mode (arbitrary text allowed); this test never runs the pipeline
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    db = str(tmp_path / "pdf.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def test_scanned_pdf_upload_is_refused_and_nothing_is_stored_or_called(client, monkeypatch):
    """AC2 over HTTP: 400 with the plain message, no case row, zero model calls."""
    from app.llm import provider
    calls = []
    monkeypatch.setattr(provider, "complete_with_meta", lambda *a, **k: calls.append(1))
    db, c = client
    r = c.post("/api/cases/pdf", content=make_pdf([["x"]], image_only=True), headers={"content-type": "application/pdf"})
    assert r.status_code == 400 and r.json()["error"]["detail"]["reason"] == "pdf_no_text_layer"
    assert "no text layer" in r.json()["error"]["message"]
    assert DB.connect(db).execute("SELECT COUNT(*) FROM cases").fetchone()[0] == 0 and calls == []


def test_pdf_upload_creates_the_same_case_as_paste_with_pages(client):
    """AC1 over HTTP: 9 records, code split, page numbers on records."""
    _, c = client
    r = c.post("/api/cases/pdf?name=Sample%20PDF", content=sample_pdf(G.raw("sample")), headers={"content-type": "application/pdf"})
    assert r.status_code == 201, r.text
    b = r.json()
    assert b["record_count"] == 9 and b["split_method"] == "code" and [x["page"] for x in b["records"]] == [1, 1, 1, 1, 1, 2, 2, 2, 2]
    view = c.get(f"/api/cases/{b['token']}").json()
    assert [x["page"] for x in view["records"]][:6] == [1, 1, 1, 1, 1, 2]


def test_export_citations_carry_page_numbers_only_for_pdf_sources():
    """AC3: with a page on a record the citation reads 'Source [Ex. __ / Bates __], p. N:'; without, the golden prefix is unchanged."""
    case = build_case()
    plain = X.build_export(case)["letter_text"]
    assert not re.search(r", p\. \d", plain) and X.SOURCE_PREFIX in plain
    for r in case["records"]:
        r["page"] = 1 if r["n"] <= 5 else 2
    out = X.build_export(case)["letter_text"]
    assert 'Source [Ex. __ / Bates __], p. 2: "Discharged from PT after two missed appointments.' in out
    assert 'Source [Ex. __ / Bates __], p. 1: "Pain 4/10, improving."' in out
    assert out.replace(", p. 1", "").replace(", p. 2", "") == plain


def test_demo_mode_refuses_a_pdf_whose_text_is_not_recorded(tmp_path, monkeypatch):
    """D-020 still holds for PDFs: in the public demo only recorded text is accepted, and nothing is stored."""
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    c = TestClient(create_app(str(tmp_path / "d.sqlite"), static_dir=str(tmp_path)))
    r = c.post("/api/cases/pdf", content=make_pdf([["A pdf whose text is not one of the recorded demo cases, with enough characters."]]),
               headers={"content-type": "application/pdf"})
    assert r.status_code == 409 and r.json()["error"]["code"] == "demo_mode_unsupported_input"


# ---- T-040 security r2 follow-up: gate and size before parsing, parse off the event loop, time cap ----
def _boom(*a, **k):
    raise AssertionError("pdf_text.extract must not run")


def test_demo_mode_refuses_before_any_parsing(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.setattr(PT, "extract", _boom)
    c = TestClient(create_app(str(tmp_path / "d.sqlite"), static_dir=str(tmp_path)))
    r = c.post("/api/cases/pdf", content=sample_pdf(G.raw("sample")), headers={"content-type": "application/pdf"})
    assert r.status_code == 409 and r.json()["error"]["code"] == "demo_mode_unsupported_input"


def test_oversize_pdf_is_refused_before_parsing(client, monkeypatch):
    monkeypatch.setattr(PT, "extract", _boom)
    _, c = client
    r = c.post("/api/cases/pdf", content=b"%PDF-" + b"0" * (PT.MAX_PDF_BYTES + 1), headers={"content-type": "application/pdf"})
    assert r.status_code == 413 and r.json()["error"]["code"] == "input_too_large"


def test_parsing_does_not_block_the_event_loop(tmp_path, monkeypatch):
    """A slow extraction runs in the threadpool: /api/health answers while it is still parsing."""
    import threading
    import time
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")
    real = PT.extract

    def slow(data):
        time.sleep(1.5)
        return real(data)
    monkeypatch.setattr(PT, "extract", slow)
    with TestClient(create_app(str(tmp_path / "s.sqlite"), static_dir=str(tmp_path))) as c:
        res = {}
        t = threading.Thread(target=lambda: res.update(r=c.post("/api/cases/pdf", content=sample_pdf(G.raw("sample")),
                                                                headers={"content-type": "application/pdf"})))
        t.start()
        time.sleep(0.3)
        t0 = time.time()
        assert c.get("/api/health").status_code == 200
        assert time.time() - t0 < 0.8
        t.join()
        assert res["r"].status_code == 201


def test_slow_extraction_hits_the_time_cap(tmp_path, monkeypatch):
    import time
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.setattr(PT, "EXTRACT_TIMEOUT_S", 0.2)
    monkeypatch.setattr(PT, "extract", lambda d: time.sleep(1.0))
    with TestClient(create_app(str(tmp_path / "t.sqlite"), static_dir=str(tmp_path))) as c:
        r = c.post("/api/cases/pdf", content=sample_pdf(G.raw("sample")), headers={"content-type": "application/pdf"})
    assert r.status_code == 400 and r.json()["error"]["detail"]["reason"] == "pdf_timeout"


# ---- T-054 security review: pypdf must not write record text anywhere ----
SECRETS = ("rear-ended", "cyclobenzaprine", "Hill Country", "Jordan Rivera", "Capital PT", "concussion")


def _mutations(data: bytes, n=120, seed=54):
    import random
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        b = bytearray(data)
        kind = i % 4
        if kind == 0:                      # flip bytes
            for _ in range(rnd.randint(1, 12)):
                b[rnd.randrange(len(b))] = rnd.randrange(256)
        elif kind == 1:                    # truncate
            b = b[:rnd.randrange(60, len(b))]
        elif kind == 2:                    # delete a slice
            a = rnd.randrange(len(b) - 40)
            del b[a:a + rnd.randint(1, 40)]
        else:                              # break the xref/startxref offsets
            b = bytearray(bytes(b).replace(b"startxref", b"startxref\n9"))
            b[rnd.randrange(60, len(b))] = 0x28
        out.append(bytes(b))
    return out


def test_pypdf_writes_no_record_text_to_stderr_or_logs(capfd, caplog):
    import logging
    seen = []

    class H(logging.Handler):
        def emit(self, rec):
            seen.append(rec.getMessage())
    h = H(level=0)
    logging.getLogger("pypdf").addHandler(h)
    caplog.set_level(logging.DEBUG)
    try:
        ok = 0
        for m in _mutations(sample_pdf(G.raw("sample"))):
            try:
                PT.extract(m)
                ok += 1
            except PT.PdfError:
                pass
    finally:
        logging.getLogger("pypdf").removeHandler(h)
    cap = capfd.readouterr()
    blob = cap.out + cap.err + caplog.text + "\n".join(seen)
    assert not [s for s in SECRETS if s in blob], blob[:300]
    assert seen == [] and cap.err == "" and ok > 0


def test_upload_of_a_damaged_pdf_logs_no_record_text(client, capfd, caplog):
    _, c = client
    import logging
    caplog.set_level(logging.DEBUG)
    for m in _mutations(sample_pdf(G.raw("sample")), n=40, seed=7):
        r = c.post("/api/cases/pdf", content=m, headers={"content-type": "application/pdf"})
        assert r.status_code in (201, 400)
    cap = capfd.readouterr()
    blob = cap.out + cap.err + caplog.text
    assert not [s for s in SECRETS if s in blob], blob[:300]


def test_requirements_pin_pypdf_exactly():
    import pathlib
    txt = (pathlib.Path(__file__).resolve().parents[2] / "requirements.txt").read_text()
    assert [l for l in txt.splitlines() if l.startswith("pypdf==")] and not [l for l in txt.splitlines() if l and not l.startswith("#") and "==" not in l]
