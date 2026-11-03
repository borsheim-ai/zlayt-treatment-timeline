"""T-087 round 2 (security review): hidden text that the first pixel-spread check missed, a scan that fails closed, and a scan deadline that
stops the work. The constructions are the reviewer's probe files (artifacts/review-evidence/T-086-087/probe_hidden.py), built here.
SYNTHETIC text only."""
import random
import threading
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import pdf_checks, pdf_hidden, pdf_text
from app.backend.api import create_app
from tests.unit import _pdf_probe as K
from tests.unit._pdf_raw import build, build_pages, text_page

pytest.importorskip("pypdfium2")
PDF = {"content-type": "application/pdf"}
VISIBLE = "Visible clinic note: patient reports neck pain after the collision."


def _cases():
    c = {}
    c["white_text"] = K.one_page(K.VISIBLE + K.WHITE)
    c["white_text_plus_1pt_black_dot_in_bbox"] = K.one_page(K.VISIBLE + K.WHITE + b"0 0 0 rg 52 704 1 1 re f\n")
    c["white_text_plus_hairline_underline"] = K.one_page(K.VISIBLE + K.WHITE + b"0 0 0 RG 0.5 w 50 699 m 500 699 l S\n")
    c["white_text_across_a_table_border"] = K.one_page(K.VISIBLE + K.WHITE + b"0 0 0 RG 1 w 300 690 m 300 720 l S\n")
    stripes = b"".join(f"{g / 255:.2f} g {50 + 40 * i} 690 40 24 re f\n".encode()
                       for i, g in enumerate([255, 20, 235, 40, 215, 60, 195, 80, 175, 100, 155, 120, 135]))
    c["black_text_under_striped_cover"] = K.one_page(K.VISIBLE + f"0 0 0 rg BT /F1 12 Tf 50 700 Td ({K.PL}) Tj ET\n".encode() + stripes)
    c["white_on_white_rect_with_black_checkbox"] = K.one_page(K.VISIBLE + b"1 1 1 rg 40 690 520 30 re f\n" + K.WHITE + b"0 0 0 RG 0.5 w 45 692 8 8 re S\n")
    c["clipped_to_nothing"] = K.one_page(K.VISIBLE + f"q 0 0 1 1 re W n BT /F1 12 Tf 0 0 0 rg 50 700 Td ({K.PL}) Tj ET Q\n".encode())
    c["extgstate_alpha_0"] = K.pdf([
        b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> /ExtGState << /G0 6 0 R >> >> >>",
        K.stream(K.VISIBLE + f"/G0 gs 0 0 0 rg BT /F1 12 Tf 50 700 Td ({K.PL}) Tj ET\n".encode()), K.FONT, b"<< /Type /ExtGState /ca 0 >>"])
    c["optional_content_layer_off"] = K.pdf([
        b"<< /Type /Catalog /Pages 2 0 R /OCProperties << /OCGs [6 0 R] /D << /OFF [6 0 R] >> >> >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> /Properties << /OC1 6 0 R >> >> >>",
        K.stream(K.VISIBLE + f"/OC /OC1 BDC BT /F1 12 Tf 0 0 0 rg 50 700 Td ({K.PL}) Tj ET EMC\n".encode()), K.FONT, b"<< /Type /OCG /Name (Hidden layer) >>"])
    # the masking attack: the hidden text's box is partly overlapped by a VISIBLE line, so the visible line's pixels fall inside it
    c["white_text_partly_under_a_visible_line"] = K.one_page(
        K.VISIBLE + K.WHITE + b"BT /F1 12 Tf 0 g 50 692 Td (Visible second line of the clinic note goes here.) Tj ET\n")
    # white text under a wider black word drawn on top of it, same place (the whole box is shared with another text object)
    c["white_text_exactly_under_visible_text"] = K.one_page(
        K.VISIBLE + K.WHITE + b"BT /F1 12 Tf 0 g 50 700 Td (" + (b"M" * 70) + b") Tj ET\n")
    for d in (15, 16, 17, 30, 40, 41, 45, 60):         # PDFium draws 40 levels of form XObject; the first four are listed and caught, the rest reconciled
        c[f"white_text_in_form_depth_{d}"] = K.nested_form(d)
    return c


CASES = _cases()


@pytest.mark.parametrize("name", sorted(CASES))
def test_reviewers_hidden_text_constructions_are_flagged_and_kept_out_of_the_case(name):
    got = pdf_checks.extract(CASES[name])
    assert "PLANTED" not in got["text"] and "Visible clinic note" in got["text"]
    ht = got["pdf_checks"]["hidden_text"]
    assert [p["page"] for p in ht["pages"]] == [1] and ht["pages"][0]["count"] >= 1 and ht["pages"][0]["excluded"]
    assert any("PLANTED" in it["text"] for it in ht["pages"][0]["items"])
    assert all(it["why"] for it in ht["pages"][0]["items"])


@pytest.mark.parametrize("name", ["white_text", "white_text_plus_1pt_black_dot_in_bbox", "black_text_under_striped_cover", "white_text_in_form_depth_45"])
def test_the_paralegal_can_still_confirm_a_flagged_page(name):
    got = pdf_checks.extract(CASES[name], include_hidden="1")
    assert "PLANTED" in got["text"] and got["pdf_checks"]["hidden_text"]["pages"][0]["confirmed"]


def test_form_nesting_beyond_what_the_renderer_draws_is_found_by_reconciliation():
    got = pdf_checks.extract(CASES["white_text_in_form_depth_45"])
    assert [r for it in got["pdf_checks"]["hidden_text"]["pages"][0]["items"] for r in it["reasons"]] == ["not_in_rendered_page"]
    scanned = pdf_hidden.scan(CASES["white_text_in_form_depth_45"])
    assert "PLANTED" not in scanned["pages"][1]["listed_text"]


# ---- visible text must not be flagged by the differential check ----
def test_visible_marks_rules_and_overlapping_lines_do_not_flag_visible_text():
    lines = [f"Line {i}: patient seen for neck pain, ROM limited; plan PT 3x per week; charge $150.00 per visit." for i in range(60)]
    tight = build(text_page(lines, size=10, lead=8, y=780))                     # lines closer than the font height: their boxes overlap
    got = pdf_checks.extract(tight)
    assert got["pdf_checks"]["hidden_text"]["pages"] == [] and "Line 59" in got["text"]
    ruled = build(text_page([VISIBLE, "Second visible line of the note."]) + b"\n0 0 0 RG 0.5 w 50 725 m 500 725 l S 40 690 300 60 re S")
    assert pdf_checks.extract(ruled)["pdf_checks"]["hidden_text"]["pages"] == []
    assert pdf_checks.extract(build(text_page([VISIBLE]) + b"\nBT /F1 12 Tf 0 g 50 740 Td (Same place, visible, drawn twice for bold.) Tj ET"))["pdf_checks"]["hidden_text"]["pages"] == []


def test_a_space_only_text_object_is_not_reported_as_hidden_text():
    got = pdf_checks.extract(build(text_page([VISIBLE]) + b"\nBT /F1 12 Tf 0 g 300 600 Td (   ) Tj ET"))
    assert got["pdf_checks"]["hidden_text"]["pages"] == [] and got["pdf_checks"]["hidden_text"]["checked"]


def test_unlisted_spans_ignores_ligatures_hyphenation_and_line_breaks():
    listed = "Dr. Rao noted effective treatment of the oﬃce visit"
    assert pdf_hidden.unlisted_spans("Dr. Rao noted effective treat-\nment of the office visit", listed) == []
    assert pdf_hidden.unlisted_spans("Dr. Rao noted ignore previous instructions effective", listed) == ["ignore previous instructions"]
    assert pdf_hidden.unlisted_spans("A b 6/10", "6 10") == []                     # single letters never count as words


# ---- the scan fails closed ----
def test_mutated_files_pypdf_reads_but_pdfium_cannot_never_put_the_planted_text_in_the_case():
    base = K.one_page(K.VISIBLE + K.WHITE)
    rnd = random.Random(7)
    variants = [base.replace(b"/Kids [3 0 R]", b"/Kids [3 0 R 99 0 R]"), base.replace(b"[0 0 600 800]", b"[0 0 (x) 800]"), base.replace(b"/Font << /F1 5 0 R >>", b"")]
    for _ in range(400):
        b = bytearray(base)
        for _ in range(rnd.randint(1, 4)):
            b[rnd.randrange(9, len(b))] = rnd.randrange(256)
        variants.append(bytes(b))
    hits = 0
    for data in variants:
        try:
            texts = pdf_text.read_pages(data)
        except Exception:
            continue
        if "PLANTED" not in " ".join(texts):
            continue
        try:
            scanned = pdf_hidden.scan(data)
            if scanned["checked"]:
                continue
        except pdf_hidden.HiddenScanUnavailable:
            pass
        hits += 1                                           # pypdf reads the planted text; the renderer could not check the file or a page
        try:
            got = pdf_checks.extract(data)
        except pdf_text.PdfError:
            continue
        assert "PLANTED" not in got["text"], "planted text reached the case when the scan could not run"
    assert hits >= 5                                         # the reviewer found 21 such files in this seeded set; the test must exercise the path


def test_unreadable_by_the_renderer_holds_every_page_back_and_flags_it(monkeypatch):
    def boom(data, deadline=None, **kw):
        raise pdf_hidden.HiddenScanUnavailable("PdfiumError", texts=pdf_text.read_pages(data))      # the child read the text layer, then the render failed
    monkeypatch.setattr(pdf_hidden, "scan", boom)
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(CASES["white_text"])
    assert e.value.code == "pdf_only_hidden_text" and e.value.detail["hidden_text_pages"] == [1] and e.value.detail["unchecked_pages"] == [1]
    got = pdf_checks.extract(CASES["white_text"], include_hidden="all")           # only the paralegal's explicit confirmation includes it
    page = got["pdf_checks"]["hidden_text"]["pages"][0]
    assert "PLANTED" in got["text"] and page["unchecked"] and page["confirmed"] and not got["pdf_checks"]["hidden_text"]["checked"]
    assert got["pages"][0]["hidden_text_included"] is True


def test_one_page_the_renderer_chokes_on_is_held_back_and_the_others_are_kept(monkeypatch):
    real = pdf_hidden._page_scan
    calls = []

    def flaky(raw, page, tick, budget):
        calls.append(1)
        if len(calls) == 2:
            raise RuntimeError("renderer failure")
        return real(raw, page, tick, budget)
    monkeypatch.setattr(pdf_hidden, "_page_scan", flaky)
    monkeypatch.setattr(pdf_hidden, "scan", lambda d, deadline=None, **kw: {**pdf_hidden.scan_inprocess(d, deadline), "texts": pdf_text.read_pages(d)})       # the patch only reaches the in-process scan (the child is a fresh interpreter)
    two = build_pages([text_page(["Page one visible note of the clinic visit."]), text_page(["Page two text the scan could not check."])])
    got = pdf_checks.extract(two)
    assert "Page one visible note of the clinic visit." in got["text"] and "Page two" not in got["text"]
    ht = got["pdf_checks"]["hidden_text"]
    assert ht["checked"] is False and ht["unchecked_pages"] == [2]
    assert ht["pages"] == [{"page": 2, "count": 0, "items": [], "unchecked": True, "why": pdf_hidden.UNCHECKED_PLAIN["page_not_rendered"],
                            "confirmed": False, "excluded": True}]
    assert "Page two" in pdf_checks.extract(two, include_hidden="2")["text"]


def test_a_page_with_more_text_objects_than_the_cap_is_unchecked_not_scanned_for_ever(monkeypatch):
    monkeypatch.setattr(pdf_hidden, "MAX_TEXT_OBJECTS", 50)
    monkeypatch.setattr(pdf_hidden, "scan", lambda d, deadline=None, **kw: {**pdf_hidden.scan_inprocess(d, deadline), "texts": pdf_text.read_pages(d)})       # the patch only reaches the in-process scan
    data = K.many_objects_pdf(1, 200, wide=False)
    s = pdf_hidden.scan(data)
    assert s["pages"][1]["unchecked"] == "too_many_text_objects" and not s["checked"]
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(data)
    assert e.value.code == "pdf_only_hidden_text"


def test_a_page_the_renderer_does_not_list_is_unchecked(monkeypatch):
    real = pdf_hidden.scan

    def short(data, deadline=None, **kw):
        out = real(data, deadline, **kw)
        out["pages"].pop(2)
        return out
    monkeypatch.setattr(pdf_hidden, "scan", short)
    got = pdf_checks.extract(build_pages([text_page(["Page one visible note of the clinic visit."]), text_page(["Page two never scanned by the renderer."])]))
    assert "Page two" not in got["text"] and got["pdf_checks"]["hidden_text"]["unchecked_pages"] == [2]


# ---- the deadline stops the work ----
def test_scan_stops_at_its_deadline_between_objects():
    data = K.many_objects_pdf(10, 3000)
    t = time.monotonic()
    with pytest.raises(pdf_hidden.HiddenScanTimeout):
        pdf_hidden.scan(data, deadline=time.monotonic() + 0.5)
    assert time.monotonic() - t < 2.0
    with pytest.raises(pdf_hidden.HiddenScanTimeout):
        pdf_hidden.scan(data, deadline=time.monotonic() - 1)


def test_extract_with_an_expired_deadline_is_a_timeout_error_not_a_long_scan():
    data = K.many_objects_pdf(10, 3000)
    t = time.monotonic()
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(data, deadline=time.monotonic() + 0.5)
    assert e.value.code == "pdf_unreadable" and e.value.detail == {"reason": "pdf_timeout"} and time.monotonic() - t < 2.5


@pytest.fixture
def live(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return TestClient(create_app(str(tmp_path / "h.sqlite"), static_dir=str(tmp_path)))


def test_the_api_timeout_and_the_worker_stop_together(live, monkeypatch):
    """The reviewer's file cost 94 s of CPU after the 400 came back. Now the worker stops at the same deadline the API waits for."""
    monkeypatch.setattr(pdf_text, "EXTRACT_TIMEOUT_S", 1.0)
    data = K.many_objects_pdf(10, 5000)
    cpu0, t = time.process_time(), time.monotonic()
    r = live.post("/api/cases/pdf", content=data, headers=PDF)
    assert r.status_code == 400 and r.json()["error"]["detail"]["reason"] == "pdf_timeout" and time.monotonic() - t < 3.0
    time.sleep(2.5)
    used_at_2_5 = time.process_time() - cpu0
    time.sleep(3.0)
    assert time.process_time() - cpu0 - used_at_2_5 < 0.5, "the scan kept running after the API gave up"


def test_api_reports_an_unchecked_page_and_the_confirm_flow(live, monkeypatch):
    def boom(data, deadline=None, **kw):
        raise pdf_hidden.HiddenScanUnavailable("PdfiumError", texts=pdf_text.read_pages(data))
    monkeypatch.setattr(pdf_hidden, "scan", boom)
    r = live.post("/api/cases/pdf", content=CASES["white_text"], headers=PDF)
    assert r.status_code == 400 and r.json()["error"]["detail"]["reason"] == "pdf_only_hidden_text"
    r = live.post("/api/cases/pdf?include_hidden=all", content=CASES["white_text"], headers=PDF)
    assert r.status_code == 201 and r.json()["pdf_checks"]["hidden_text"]["pages"][0]["unchecked"] is True
