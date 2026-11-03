"""PDF text-layer extraction (D-031). Pure python (pypdf) reads the text layer; hidden-text detection (pdf_hidden) and opt-in local OCR
(pdf_ocr) are layered on by pdf_checks. A PDF with no usable text is refused before anything is stored or any model is called. The extracted text is the case text; `pages` maps character offsets of that text to page numbers so citations can
carry them. Deterministic code only."""
import io
import logging
import time
import warnings

MAX_PDF_BYTES = 5 * 1024 * 1024
MAX_PAGES = 100
EXTRACT_TIMEOUT_S = 10.0     # the API stops waiting after this long; the child process doing the work is killed at the same moment
MIN_TEXT_CHARS = 20          # fewer non-space characters than this in the whole file = no usable text layer


# pypdf logs fragments of the document it is parsing (record text) when a file is malformed; the app never logs record text, so the
# library's logger is cut off from every handler and its warnings are ignored during extraction.
_lg = logging.getLogger("pypdf")
_lg.addHandler(logging.NullHandler())
_lg.propagate = False
_lg.setLevel(logging.CRITICAL + 1)


class PdfError(ValueError):
    """str(e) is the API error code: pdf_no_text_layer | pdf_unreadable | pdf_too_large | pdf_encrypted (pdf_checks adds the OCR codes).
    `detail` is extra, record-free context for the API error body (T-086/T-087)."""

    def __init__(self, code, detail=None):
        super().__init__(code)
        self.detail = detail or {}

    @property
    def code(self) -> str:
        return str(self)


def read_pages(data: bytes, deadline: float = None) -> list:
    """The stripped text-layer string of every page (may be empty). Validates size, header, encryption and page count.
    `deadline` (time.monotonic() value) is shared with the later stages of one upload; default EXTRACT_TIMEOUT_S from now.
    THIS PARSES THE FILE IN THE CALLING PROCESS. The server never calls it directly (T-087 round 4: one page can cost minutes of CPU
    that no thread can cancel); it runs inside the killed child of pdf_hidden (`pdf_hidden.scan(..., with_text=True)` / `read_text`)."""
    if len(data or b"") > MAX_PDF_BYTES:
        raise PdfError("pdf_too_large")
    if not (data or b"").lstrip()[:5] == b"%PDF-":
        raise PdfError("pdf_unreadable")
    from pypdf import PdfReader
    from pypdf.errors import PyPdfError
    deadline = deadline or time.monotonic() + EXTRACT_TIMEOUT_S
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            reader = PdfReader(io.BytesIO(data))
            if reader.is_encrypted:
                raise PdfError("pdf_encrypted")
            if len(reader.pages) > MAX_PAGES:
                raise PdfError("pdf_too_large")
            texts = []
            for page in reader.pages:
                if time.monotonic() > deadline:         # stop the worker thread between pages once the API has given up on it
                    raise PdfError("pdf_unreadable", {"reason": "pdf_timeout"})
                texts.append((page.extract_text() or "").replace("\r\n", "\n").replace("\r", "\n").strip())
    except PdfError:
        raise
    except (PyPdfError, ValueError, KeyError, OSError, RecursionError, AssertionError, TypeError):
        raise PdfError("pdf_unreadable") from None
    return texts


def assemble(texts: list, sources: dict = None) -> dict:
    """{text, pages: [{page, start, end}]}. Page texts are stripped and joined with a blank line, so offsets index the text exactly.
    `sources` maps a page number to extra keys for that page's entry (for example {"source": "ocr"}); empty pages are left out."""
    from app.backend import ingest          # lazy: T-178 format characters leave the page text here, so the offsets below index the cleaned case text
    text, pages = "", []
    for i, t in enumerate(texts, 1):
        t = ingest.clean_chars(t).strip()
        if not t:
            continue
        if text:
            text += "\n\n"
        pages.append({"page": i, "start": len(text), "end": len(text) + len(t), **(sources or {}).get(i, {})})
        text += t
    return {"text": text, "pages": pages}


def extract_text_layer(data: bytes) -> dict:
    """{text, pages: [{page, start, end}]} from the text layer alone (no hidden-text check, no OCR); no usable text layer is refused."""
    from app.backend import pdf_hidden
    try:
        texts = pdf_hidden.read_text(data, time.monotonic() + EXTRACT_TIMEOUT_S)       # in the killed child, never in this process
    except pdf_hidden.HiddenScanTimeout:
        raise PdfError("pdf_unreadable", {"reason": "pdf_timeout"}) from None
    if sum(len("".join(t.split())) for t in texts) < MIN_TEXT_CHARS:
        raise PdfError("pdf_no_text_layer")
    return assemble(texts)


def extract(data: bytes, **options) -> dict:
    """What POST /api/cases/pdf runs: the text layer minus text that is hidden when the page is shown (T-087), plus local OCR of scanned
    pages when `ocr=True` (T-086). Options: ocr (bool), include_hidden ('all' | '2,5': pages whose hidden text the paralegal confirmed).
    Result: {text, pages, pdf_checks, page_images}; see pdf_checks.extract."""
    from app.backend import pdf_checks
    return pdf_checks.extract(data, **options)


def page_for(pages: list, offset: int):
    """Page number whose span holds `offset` (a gap between pages belongs to the earlier page); None when there is no page map."""
    if not pages or offset is None:
        return None
    hit = None
    for p in pages:
        if p["start"] <= offset:
            hit = p["page"]
    return hit
