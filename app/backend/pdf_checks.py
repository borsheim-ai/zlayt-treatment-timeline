"""PDF intake checks, one pass (T-086 local OCR + T-087 hidden text; D-042). Deterministic code; the only external program is the
local Tesseract binary. `extract()` is what POST /api/cases/pdf calls; `mark_ocr_items()` is what the pipeline calls before it
stores items.

Order: read the text layer (pypdf) -> find text that is not visible when the page is rendered (pdf_hidden) and take it out of the
page text unless the paralegal confirmed that page -> pages left with no text are OCR'd locally only when the caller asked for OCR.
The case text is the result, so hidden text can never ground a quote and OCR words are quoted exactly as OCR read them."""
import threading
import time

from app.backend import pdf_hidden, pdf_ocr, pdf_text
from app.backend.pdf_text import PdfError

OCR_TIMEOUT_S = pdf_ocr.TOTAL_TIMEOUT_S + 15     # the API's wait when OCR was requested (the plain text path keeps pdf_text.EXTRACT_TIMEOUT_S)

MAX_PDF_JOBS = 2             # uploads being processed at once (text read, scan, OCR); the next ones get a 429 instead of queueing (T-087 round 4)
BUSY_WAIT_S = 0.5            # a slot freed by a job that has just timed out is given this long to come free before the answer is "busy"
_JOBS = threading.BoundedSemaphore(MAX_PDF_JOBS)

MESSAGES = {
    "pdf_busy": "The server is already reading other PDFs. Wait a moment and upload this one again.",
    "pdf_no_text_layer": "This PDF has no text layer (it looks scanned). Run OCR to read the scanned pages, or paste the text instead.",
    "pdf_only_hidden_text": "Every piece of text in this PDF's text layer is hidden when the page is shown, or could not be checked, so nothing was read. "
                            "Run OCR to read what the pages show, or confirm the listed pages if you trust them.",
    "ocr_unavailable": "Scanned pages need Tesseract, which is not available on this server.",
    "ocr_too_many_pages": f"This PDF has more than {pdf_ocr.MAX_OCR_PAGES} scanned pages; OCR reads at most that many in one upload. Split the file.",
    "ocr_render_failed": "This PDF could not be safely drawn for OCR (the page drawer ran out of memory or time, or the file is damaged), so nothing was read. "
                         "Paste the text instead.",
    "ocr_check_failed": "This PDF could not be checked safely (the checker ran out of memory or time, or crashed), so it was not read with OCR. "
                        "Paste the text instead.",
    "ocr_failed": "OCR could not read a page of this PDF. Try again, or paste the text instead.",
    "ocr_page_too_large": "A scanned page in this PDF is larger than OCR will read (over 40 inches on a side). Re-scan or resize it, or paste the text instead.",
    "ocr_images_too_large": "The scanned pages in this PDF are too large to keep together. Split the file, or paste the text instead.",
}


def parse_confirmed(value, pages: int):
    """Query value -> set of confirmed hidden-text pages. 'all' = every page; '2,5' = those pages; empty = none."""
    v = (value or "").strip().lower()
    if v == "all":
        return set(range(1, pages + 1))
    out = set()
    for part in v.split(","):
        part = part.strip()
        if part.isdigit():
            out.add(int(part))
    return out


def extract(data: bytes, *, ocr: bool = False, include_hidden=None, deadline: float = None) -> dict:
    """{text, pages: [{page, start, end, source?, ...}], pdf_checks: {...}, page_images: {n: base64 png}}.
    `include_hidden`: the raw query value for confirmed hidden-text pages (see parse_confirmed). `deadline`: a time.monotonic() value
    shared by every stage (default: the API's wait, EXTRACT_TIMEOUT_S, or OCR_TIMEOUT_S with OCR), so the work stops when the API has
    stopped waiting. Raises PdfError.

    Fail closed (T-087 round 2): a page whose hidden-text check could not run, or whose text-layer words the renderer did not place on the
    page, is kept out of the case text and listed in the report until the paralegal confirms it. Nothing is included silently."""
    if not _JOBS.acquire(timeout=BUSY_WAIT_S):
        raise PdfError("pdf_busy")
    try:
        return _extract(data, ocr=ocr, include_hidden=include_hidden,
                        deadline=deadline or time.monotonic() + (OCR_TIMEOUT_S if ocr else pdf_text.EXTRACT_TIMEOUT_S))
    finally:
        _JOBS.release()


def _extract(data: bytes, *, ocr: bool, include_hidden, deadline: float) -> dict:
    try:                       # the text-layer read (pypdf) and the render scan (PDFium) both run in one child process killed at the deadline
        scanned = pdf_hidden.scan(data, deadline, with_text=True)
        texts = scanned.pop("texts")
    except pdf_hidden.HiddenScanUnavailable as e:
        if ocr:                # T-107: a file whose scan child was killed or failed is never handed to OCR; no fallback render anywhere
            raise PdfError("ocr_check_failed", {"cause": str(e)[:40]}) from None
        texts = e.texts
        if texts is None:      # the child failed before it had read the text layer: there is nothing to hold back, the file is unreadable
            raise PdfError("pdf_unreadable") from None
        scanned = pdf_hidden.unchecked_scan(len(texts))
    except pdf_hidden.HiddenScanTimeout:
        raise PdfError("pdf_unreadable", {"reason": "pdf_timeout"}) from None
    confirmed = parse_confirmed(include_hidden, len(texts))
    checks = {"hidden_text": {"checked": False, "pages": [], "excluded_until_confirmed": True,
                              "message": "Hidden-text check did not run on this file."},
              "ocr": {"requested": bool(ocr), "ran": False, "pages": [], "status": pdf_ocr.ocr_status()}}
    for n in range(1, len(texts) + 1):               # a page the renderer did not list is a page nobody checked
        scanned["pages"].setdefault(n, pdf_hidden._unchecked("page_not_rendered"))
    sources = {}
    for n, p in scanned["pages"].items():
        if n > len(texts) or p.get("unchecked"):
            continue
        spans = pdf_hidden.unlisted_spans(texts[n - 1], p["listed_text"])      # words only the extractor can reach
        p["hidden"] = p["hidden"] + [{"text": sp, "reasons": ["not_in_rendered_page"], "bbox": None} for sp in spans]
    for n, p in scanned["pages"].items():
        if n > len(texts) or n in confirmed:
            continue
        if p.get("unchecked"):
            if "".join(texts[n - 1].split()):
                texts[n - 1] = ""                       # text we could not check stays out; a page with no text has nothing to hold back
            else:
                p["unchecked"] = None
        elif p["hidden"]:
            texts[n - 1] = pdf_hidden.remove_from_text(texts[n - 1], p["hidden"], p["visible_text"])
    checks["hidden_text"] = pdf_hidden.report(scanned, confirmed)
    for n in confirmed:
        if n in scanned["pages"] and (scanned["pages"][n]["hidden"] or scanned["pages"][n].get("unchecked")):
            sources[n] = {"hidden_text_included": True}
    # a page with no text left but a picture on it is a scan (or has only hidden text over a picture)
    image_pages = [n for n, p in scanned["pages"].items() if n <= len(texts) and not "".join(texts[n - 1].split()) and p["has_image"]]
    blank = [n for n, t in enumerate(texts, 1) if not "".join(t.split())]
    scan_pages = sorted(set(image_pages) | (set(blank) if not any("".join(t.split()) for t in texts) else set()))
    ocr_page_data = {}
    if scan_pages:
        checks["ocr"]["scanned_pages"] = scan_pages
        if ocr:
            if len(scan_pages) > pdf_ocr.MAX_OCR_PAGES:
                raise PdfError("ocr_too_many_pages", {"scanned_pages": len(scan_pages), "max": pdf_ocr.MAX_OCR_PAGES})
            try:
                ocr_page_data = pdf_ocr.ocr_pages(data, scan_pages, deadline=deadline)
            except pdf_ocr.OcrUnavailable as e:
                raise PdfError("ocr_unavailable", {"message": str(e), "ocr": checks["ocr"]["status"]}) from None
            except pdf_ocr.OcrFailed as e:
                code = {"page_too_large": "ocr_page_too_large", "images_too_large": "ocr_images_too_large",
                        "render_killed": "ocr_render_failed", "render_failed": "ocr_render_failed"}.get(e.reason, "ocr_failed")
                raise PdfError(code, {"page": e.page} if e.page else None) from None
            for n, o in ocr_page_data.items():
                texts[n - 1] = o["text"].strip()
                sources[n] = {"source": "ocr", "mean_conf": o["mean_conf"], "words": o["words"], "has_image": True}
    if sum(len("".join(t.split())) for t in texts) < pdf_text.MIN_TEXT_CHARS:
        hidden_pages = [p["page"] for p in checks["hidden_text"]["pages"] if not p["confirmed"]]
        detail = {"scanned_pages": scan_pages, "ocr": checks["ocr"]["status"], "hidden_text_pages": hidden_pages,
                  "unchecked_pages": [p for p in checks["hidden_text"]["unchecked_pages"] if p in hidden_pages]}
        raise PdfError("pdf_only_hidden_text" if hidden_pages else "pdf_no_text_layer", detail)
    got = pdf_text.assemble(texts, sources)
    images, low = {}, 0
    for pg in got["pages"]:
        o = ocr_page_data.get(pg["page"])
        if o:
            base = pg["start"]
            pg["low_conf"] = [{"start": base + w["start"], "end": base + w["end"], "text": w["text"], "conf": w["conf"]}
                              for w in o["low_conf"][:pdf_ocr.MAX_LOW_CONF_LISTED]]
            pg["low_conf_count"] = len(o["low_conf"])
            low += len(o["low_conf"])
            images[pg["page"]] = o["png_b64"]
    if ocr_page_data:
        checks["ocr"].update({"ran": True, "engine": f"tesseract {checks['ocr']['status']['version']}",
                              "pages": sorted(ocr_page_data), "low_conf_words": low,
                              "low_conf_rule": f"words under {pdf_ocr.LOW_CONF_WORD} confidence, or under {pdf_ocr.LOW_CONF_NUMBER} when the word has a digit",
                              "items_need_review": True})
    return {"text": got["text"], "pages": got["pages"], "pdf_checks": checks, "page_images": images}


def is_ocr_span(pages, start: int, end: int) -> bool:
    """True when [start, end) overlaps the text of an OCR page."""
    return any(p.get("source") == "ocr" and p["start"] < max(end, start + 1) and start < p["end"] for p in (pages or []))


def mark_ocr_items(items: list, recs: list, pages: list, why_text: str) -> int:
    """Every non-rejected item whose record lies on an OCR page becomes needs_review with reason OCR_DERIVED (never `verified`).
    Items carry `record_ids` ('r<n>'); `recs` are the ingest records ({n, char_start, char_end}). Mutates in place; returns the count."""
    if not any(p.get("source") == "ocr" for p in pages or []):
        return 0
    ocr_ids = {f"r{r['n']}" for r in recs if is_ocr_span(pages, r["char_start"], r["char_end"])}
    n = 0
    for it in items:
        if it.get("state") == "rejected" or not ocr_ids.intersection(it.get("record_ids") or []):
            continue
        reasons = list(it.get("reasons") or [])
        if "OCR_DERIVED" not in reasons:
            reasons.append("OCR_DERIVED")
            it["why"] = ((it.get("why") or "") + " " + why_text).strip()
        it["reasons"], it["state"] = reasons, "needs_review"
        if isinstance(it.get("ladder"), dict):
            it["ladder"]["state"] = "needs_review"
            it["ladder"].setdefault("code_checks", {})["ocr_derived"] = True
        n += 1
    return n

