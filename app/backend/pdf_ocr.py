"""Local OCR for scanned PDF pages (T-086, D-042). The Tesseract binary runs as a subprocess on this machine; no page image or text
ever leaves it, and nothing here calls a network. Rendering is pypdfium2 (PDFium) and runs ONLY in the killed child process of pdf_hidden (T-107: render_in_child); PNG encoding is stdlib zlib.

OCR output is a guess at the printed words, so everything derived from it is held to a stricter rule than text-layer text:
  - the page image is kept beside the OCR text, so the paralegal checks the words against the page itself;
  - words Tesseract is unsure of are listed with their offsets (LOW_CONF_WORD / LOW_CONF_NUMBER below) and marked in the UI;
  - every entry, amount and flag whose record lies on an OCR page is `needs_review` (reason OCR_DERIVED), whatever the model judges.
The OCR text is the case text for those pages, so quotes still have to match it word for word (the grounding verifier is unchanged).
A missing Tesseract is a clear message (`ocr_status()`), never a crash. Tested with Tesseract 5.5.2; 5.x is accepted."""
import base64
import csv
import io
import os
import re
import shutil
import struct
import subprocess
import tempfile
import time
import zlib

TESTED_VERSION = "5.5.2"
MIN_MAJOR = 5
DPI = 150                       # render density; Tesseract reads 150 to 300 dpi, and a smaller image keeps the stored page small
LOW_CONF_WORD = 60              # a word below this confidence (0-100) is marked
LOW_CONF_NUMBER = 80            # a word with a digit in it needs this much: a wrong digit changes a date or a dollar amount
MAX_OCR_PAGES = 10              # more scanned pages than this is refused, not partly read
PAGE_TIMEOUT_S = 40
TOTAL_TIMEOUT_S = 150
MAX_LOW_CONF_LISTED = 400
MAX_PAGE_PT = 2880              # a page larger than 40 inches on a side is refused (PDF allows 14400 pt; a 1 KB file could ask for 2 GB of bitmap)
MAX_SIDE_PX = 3500              # longest side of the rendered page; a larger page is rendered smaller than DPI, never bigger
MAX_PIXELS = 8_000_000          # width x height of the rendered page (US Letter at 150 dpi is 2.1 million)
MAX_STORED_PNG_BYTES = 12 * 1024 * 1024     # all page images of one upload together; they are kept with the case
INSTALL_HINT = "Install Tesseract: macOS `brew install tesseract`; Debian/Ubuntu `sudo apt-get install tesseract-ocr`."

_ENV_KEEP = ("PATH", "TMPDIR", "TESSDATA_PREFIX", "LANG", "LC_ALL", "LC_CTYPE")     # nothing else: no API key, token or HOME reaches the binary


def _env() -> dict:
    """The environment tesseract runs with: an allow-list taken from the server's at call time, plus one thread (T-086 round 2)."""
    return {**{k: os.environ[k] for k in _ENV_KEEP if k in os.environ}, "OMP_THREAD_LIMIT": "1"}


class OcrUnavailable(RuntimeError):
    """Tesseract is missing or unusable; str(e) is a plain message for the user."""


class OcrFailed(RuntimeError):
    """Tesseract ran and failed or timed out on a page, or a page was refused. `reason`: timeout | exec | exit | page_too_large |
    images_too_large | <exception class>; `page` is the 1-based page when known."""

    def __init__(self, reason, page=None):
        super().__init__(reason)
        self.reason, self.page = reason, page


def _which() -> str:
    return shutil.which("tesseract") or ""


def ocr_status() -> dict:
    """{available, version, tested_version, languages, message}. Never raises."""
    exe = _which()
    if not exe:
        return {"available": False, "version": None, "tested_version": TESTED_VERSION, "languages": [],
                "message": "Scanned pages need Tesseract, which is not installed on this server. " + INSTALL_HINT}
    try:
        v = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=10, env=_env())
        first = ((v.stdout or v.stderr).splitlines() or [""])[0]
        m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", first)
        version = m.group(0) if m else None
        langs = subprocess.run([exe, "--list-langs"], capture_output=True, text=True, timeout=10, env=_env())
        languages = [x.strip() for x in (langs.stdout or "").splitlines()[1:] if x.strip() and x.strip() not in ("osd", "snum")]
    except (OSError, subprocess.SubprocessError):
        return {"available": False, "version": None, "tested_version": TESTED_VERSION, "languages": [],
                "message": "Tesseract is installed but could not be run. " + INSTALL_HINT}
    if not m or int(m.group(1)) < MIN_MAJOR or "eng" not in languages:
        return {"available": False, "version": version, "tested_version": TESTED_VERSION, "languages": languages,
                "message": f"This server has Tesseract {version or '(unknown version)'} with English data "
                           f"{'present' if 'eng' in languages else 'missing'}; version {MIN_MAJOR} or later with English data is needed. " + INSTALL_HINT}
    return {"available": True, "version": version, "tested_version": TESTED_VERSION, "languages": languages,
            "message": f"Tesseract {version} is available."}


# ------------------------------------------------------------------ images
def _png_chunk(tag: bytes, body: bytes) -> bytes:
    c = tag + body
    return struct.pack(">I", len(body)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)


def _png(rows, w: int, h: int) -> bytes:
    """8-bit greyscale PNG from an iterable of `h` rows of `w` bytes, compressed row by row (stdlib only; one page is never held three times)."""
    z = zlib.compressobj(6)
    body = bytearray()
    for row in rows:
        body += z.compress(b"\x00")
        body += z.compress(row)
    body += z.flush()
    return b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0)) + _png_chunk(b"IDAT", bytes(body)) + _png_chunk(b"IEND", b"")


def render_scale(width_pt: float, height_pt: float) -> float:
    """The render scale for a page: DPI/72, lowered so neither side passes MAX_SIDE_PX nor the area MAX_PIXELS. Raises OcrFailed
    ("page_too_large") for a page over MAX_PAGE_PT on a side or one with no usable size."""
    longest = max(width_pt, height_pt)
    if not (width_pt > 0 and height_pt > 0) or longest > MAX_PAGE_PT:
        raise OcrFailed("page_too_large")
    return min(DPI / 72.0, MAX_SIDE_PX / longest, (MAX_PIXELS / (width_pt * height_pt)) ** 0.5)


def render_page_png(pdf, index: int) -> bytes:
    """Greyscale PNG of page `index` (0-based) of an open pypdfium2 document at DPI (capped by render_scale)."""
    page = pdf[index]
    try:
        scale = render_scale(*page.get_size())
        bitmap = page.render(scale=scale)
        try:
            w, h, stride, ch = bitmap.width, bitmap.height, bitmap.stride, bitmap.n_channels
            view = memoryview(bitmap.buffer).cast("B")
            off = 1 if ch >= 3 else 0          # the green channel stands in for luminance
            return _png((view[y * stride + off: y * stride + w * ch: ch].tobytes() for y in range(h)), w, h)
        finally:
            bitmap.close()
    finally:
        page.close()


# ------------------------------------------------------------------ tesseract
def _parse_tsv(tsv: str) -> dict:
    """Page text and word list from Tesseract TSV. Lines are rebuilt from the word rows, so word offsets are exact."""
    rows = [r for r in csv.reader(io.StringIO(tsv), delimiter="\t", quoting=csv.QUOTE_NONE) if len(r) >= 12 and r[0] != "level"]
    text, words, last_line, last_block = "", [], None, None
    for r in rows:
        if r[0] != "5" or not r[11].strip():
            continue
        try:
            conf = float(r[10])
        except ValueError:
            continue
        key, block = (r[2], r[3], r[4]), (r[2], r[3])
        if last_line is not None:
            text += ("\n\n" if block != last_block else "\n") if key != last_line else " "
        start = len(text)
        text += r[11].strip()
        words.append({"text": r[11].strip(), "start": start, "end": len(text), "conf": round(conf, 1)})
        last_line, last_block = key, block
    return {"text": text, "words": words}


def is_low(word: dict) -> bool:
    need = LOW_CONF_NUMBER if any(c.isdigit() for c in word["text"]) else LOW_CONF_WORD
    return word["conf"] < need


def ocr_png(png: bytes, languages: list = None, timeout: float = PAGE_TIMEOUT_S, status: dict = None) -> dict:
    """{text, words:[{text,start,end,conf}], low_conf:[...], mean_conf}. Raises OcrUnavailable / OcrFailed."""
    st = status or ocr_status()
    if not st["available"]:
        raise OcrUnavailable(st["message"])
    lang = "+".join(l for l in (languages or ["eng"]) if l in st["languages"]) or "eng"
    with tempfile.TemporaryDirectory(prefix="zlayt-ocr-") as d:
        src = os.path.join(d, "page.png")
        with open(src, "wb") as f:
            f.write(png)
        try:
            p = subprocess.run([_which(), src, "stdout", "-l", lang, "--psm", "3", "tsv"], capture_output=True, text=True,
                               timeout=timeout, env=_env(), cwd=d)
        except subprocess.TimeoutExpired:
            raise OcrFailed("timeout") from None
        except OSError:
            raise OcrFailed("exec") from None
    if p.returncode != 0:
        raise OcrFailed("exit")
    got = _parse_tsv(p.stdout)
    low = [w for w in got["words"] if is_low(w)]
    confs = [w["conf"] for w in got["words"]]
    return {"text": got["text"], "words": got["words"], "low_conf": low,
            "mean_conf": round(sum(confs) / len(confs), 1) if confs else None}


def render_in_child(data: bytes, pages: list, soft_deadline: float, emit) -> None:
    """RUNS ONLY INSIDE THE KILLED CHILD (pdf_hidden `render` mode). Opens the file with PDFium, renders each page to a capped greyscale PNG
    and emits one JSON line per page: {page, png_b64} or {render_error, page}; {render_done: true} last. The caller's process never opens
    the file (T-107)."""
    try:
        import pypdfium2 as pdfium
        pdf = pdfium.PdfDocument(data)
    except Exception as e:
        emit({"render_error": type(e).__name__, "page": None})
        return
    stored = 0
    try:
        for n in pages:
            if time.monotonic() > soft_deadline:
                emit({"render_error": "timeout", "page": n})
                return
            try:
                png = render_page_png(pdf, n - 1)
            except OcrFailed as e:
                emit({"render_error": e.reason, "page": n})
                return
            except Exception as e:
                emit({"render_error": type(e).__name__, "page": n})
                return
            stored += len(png)
            if stored > MAX_STORED_PNG_BYTES:
                emit({"render_error": "images_too_large", "page": n})
                return
            emit({"page": n, "png_b64": base64.b64encode(png).decode("ascii")})
        emit({"render_done": True})
    finally:
        pdf.close()


def render_pages(data: bytes, pages: list, deadline: float = None) -> dict:
    """{page: PNG bytes}, rendered by the killed child process (pdf_hidden.render_messages). A child that is killed (deadline, CPU, memory),
    crashes or cannot open the file is OcrFailed('render_killed' | 'render_failed' | 'timeout'); there is no in-process fallback."""
    from app.backend import pdf_hidden
    try:
        msgs = pdf_hidden.render_messages(data, pages, deadline)
    except pdf_hidden.HiddenScanTimeout:
        raise OcrFailed("timeout") from None
    except pdf_hidden.HiddenScanUnavailable:
        raise OcrFailed("render_killed") from None
    out = {}
    for m in msgs:
        if m.get("render_error"):
            raise OcrFailed(str(m["render_error"])[:60], m.get("page"))
        if isinstance(m.get("page"), int) and isinstance(m.get("png_b64"), str):
            try:
                out[m["page"]] = base64.b64decode(m["png_b64"], validate=True)
            except ValueError:
                raise OcrFailed("render_failed", m["page"]) from None
    if not any(m.get("render_done") for m in msgs) or set(out) != set(pages):
        raise OcrFailed("render_failed")
    return out


def ocr_pages(data: bytes, pages: list, deadline: float = None) -> dict:
    """OCR the given 1-based `pages` of a PDF. {n: {text, low_conf (page offsets), mean_conf, words, png_b64}}.
    Raises OcrUnavailable (checked first, before any rendering), OcrFailed. Rendering happens in the killed child (render_pages); only the
    Tesseract subprocess and the PNG bytes it reads are handled in this process."""
    st = ocr_status()
    if not st["available"]:
        raise OcrUnavailable(st["message"])
    start = time.monotonic()
    out = {}
    pngs = render_pages(data, list(pages), deadline if deadline else start + TOTAL_TIMEOUT_S)
    stored = 0
    for n in pages:                    # the child enforces the cap too; this re-check is byte counting, not parsing
        stored += len(pngs[n])
        if stored > MAX_STORED_PNG_BYTES:
            raise OcrFailed("images_too_large", n)
    for n in pages:
        if time.monotonic() - start > TOTAL_TIMEOUT_S or (deadline and time.monotonic() > deadline):
            raise OcrFailed("timeout", n)
        png = pngs[n]
        got = ocr_png(png, status=st)
        out[n] = {"text": got["text"], "words": len(got["words"]), "mean_conf": got["mean_conf"],
                  "low_conf": [{"start": w["start"], "end": w["end"], "text": w["text"], "conf": w["conf"]} for w in got["low_conf"]],
                  "png_b64": base64.b64encode(png).decode("ascii")}
    return out
