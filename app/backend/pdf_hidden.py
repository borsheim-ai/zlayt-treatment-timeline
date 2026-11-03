"""Hidden-text detection for PDFs (T-087, D-042). Deterministic code, local only (pypdfium2 = PDFium, no network).

A PDF can carry text in its text layer that a reader never sees on the rendered page: white or background-coloured text, text drawn
off the page, text in a tiny font, text in the invisible render mode, text covered by a filled box. A paralegal copying from the
rendered page would never quote it, but the extractor reads it. Here every text object is checked against the page *as rendered*:

    invisible_render_mode  PDF text render mode 3 (neither filled nor stroked; this is how a hidden OCR layer is stored)
    transparent            fill opacity 0
    off_page               less than half of the text's box lies on the page
    tiny_font              effective font size under TINY_PT points
    blends_with_background a DIFFERENTIAL render: the page is drawn with every text object, and again with all text switched to the
                           invisible mode; if the two pictures agree under this text's box, drawing the text changes nothing a reader
                           can see (white on white, a cover drawn over it, a colour equal to the background). Marks, rules, dots
                           or stripes in the box cannot fool it, because they are in both pictures. Where another text object's box
                           overlaps this one, only the pixels outside that box are compared, and when too little is left the one
                           object is switched off alone and the two crops compared (an exact test, budgeted per page)
    could_not_verify       the check could not be made exactly (no box, too many overlapping objects): the text is held back
                           ("suspected") exactly like detected hidden text
    not_in_rendered_page   a word in the text layer that no text object the renderer placed on the page contains (for example text
                           nested deeper in form XObjects than the renderer draws); see unlisted_spans()
    covered_by_annotation  an annotation (a form field, stamp, box ...) that has an appearance and lies over the text's box. PDFium does
                           not draw a form field that the file's AcroForm does not list, though other viewers do, so the render cannot
                           show whether the field covers the text; any such text is suspected (fail toward excluding)
    clipped                a clipping path leaves less than CLIP_VISIBLE_MIN of the text's box showing (one glyph through a window)

A page that cannot be scanned at all (renderer error, more than MAX_TEXT_OBJECTS text objects) is *unchecked*: its text is kept out of
the case and the page is flagged, exactly like hidden text, until the paralegal confirms it. Nothing is ever included silently.
Hidden and unchecked text is removed from the case text until the paralegal confirms the page, so it can never ground a quote.
Isolation (T-087 rounds 3-4): `scan()` runs the whole scan, and with `with_text=True` the pypdf text-layer read too, in a child process
with a hard wall-clock kill at the deadline, an RLIMIT_CPU, RLIMIT_AS where the platform enforces it (Linux; macOS refuses it) and a
parent-side poll of the child's RSS that kills it above CHILD_RSS_BYTES, so no work survives the deadline however slow a native call
is and no PDF parser runs in the API process. The in-process scan is `scan_inprocess()`.
Limits (stated, not hidden): a clip path that leaves half or more of the text showing counts as visible; a rotated or skewed text box is
checked by its bounding box; a word that also appears in the visible text counts as listed (see unlisted_spans). Thresholds are
deliberately strict and fail toward excluding: text under TINY_PT, text whose colour is within DIFF_MIN levels of what is behind it, and
text clipped to under CLIP_VISIBLE_MIN of its box are all held back as suspected (a faint but real footnote costs the paralegal one click).
Text a reader can read only by changing the contrast or the zoom is not text they would quote."""
import ctypes
import json
import math
import os
import re
import signal
import subprocess
import sys
import threading
import time
import unicodedata

TINY_PT = 5.0               # effective font size below this is held back as suspected (round 3: was 3.0, and exactly 3.0 passed)
SCALE = 2.0                 # render scale for the pixel check (144 dpi on a 72-pt page)
MAX_SIDE_PX = 3200          # cap for oversized MediaBoxes
MAX_PIXELS = 6_000_000      # width x height cap for the two comparison renders (they are held in memory together)
DIFF_MIN = 96               # a pixel counts as changed by the text when any colour channel moves by at least this much (0-255); about 2.6:1 on white
                            # (round 3: was 48, which let grey-200 text on a light scan, 55 levels, through)
MIN_PIXELS = 3              # this many changed pixels under a text object = it is visible
MAX_DEPTH = 100             # form XObject nesting listed (PDFium parses 40 levels and draws no deeper)
MAX_TEXT_OBJECTS = 20000    # per page; more = the page is unchecked, not scanned for a long time
EXACT_MAX = 120             # single-object exact tests per DOCUMENT (each is two small renders); more = could_not_verify
NEAR_MAX = 200              # a box that more than this many other text boxes overlap is could_not_verify at once (no per-pixel work)
CLIP_VISIBLE_MIN = 0.5      # a clip that shows less than this share of the text box = suspected
MAX_ANNOTS = 500            # per page; more = the page is unchecked
ANNOT_EXEMPT = (2, 9, 10, 11, 12)          # Link, Highlight, Underline, Squiggly, StrikeOut: draw nothing opaque over text (the render checks markup)
POPUP = 16                                 # T-087 round 4: PDFium never draws a Popup, so the render cannot show an opaque one; only a Popup without an appearance is skipped
CHILD_MEM_BYTES = 3 * 1024 ** 3            # address-space limit for the scan child where the platform enforces it (Linux)
CHILD_RSS_BYTES = 1024 ** 3                # resident-memory ceiling the parent enforces by polling, on every platform (macOS has no RLIMIT_AS)
WATCH_EVERY_S = 0.1                        # how often the parent looks at the child's RSS and the clock
DEFAULT_SCAN_S = 60.0       # wall clock for scan() when the caller gives no deadline
MAX_CHILDREN = 2            # PDF child processes running at once in this server (round 4: was 4); pdf_checks refuses further uploads with a 429
OVERLAP_EXACT = 0.25        # if other text boxes cover more than this share of a box, compare by the exact test instead of the mask
MAX_HIDDEN_OBJECTS = 400    # per page; more hidden pieces than this and the page is unchecked (held back whole)
VISIBLE_REBUILD_MAX = 400   # a page with hidden text and more text objects than this has no rebuilt fallback text (it falls back to nothing)
CHECK_EVERY = 32            # deadline check every this many objects (and once per page and per render)
MAX_ITEMS_PER_PAGE = 50     # items listed per page in the report (the page still counts them all)
TEXT_CAP = 300              # characters of a hidden string kept in the report
INVISIBLE_MODE = 3

REASON_PLAIN = {
    "invisible_render_mode": "drawn in the PDF's invisible text mode",
    "transparent": "fully transparent",
    "off_page": "placed outside the page",
    "tiny_font": "set in a font too small to read",
    "blends_with_background": "not visible when the page is shown (the same colour as the page behind it, or covered)",
    "could_not_verify": "its visibility could not be confirmed, so it is held back as suspected hidden text",
    "not_in_rendered_page": "in the file's text but not placed on the page by the page renderer (for example nested deeper than the page draws)",
    "covered_by_annotation": "under a form field, stamp or other annotation that may cover it in some viewers, so it is held back as suspected hidden text",
    "clipped": "mostly cut off by a clipping window, so little or none of it shows",
}
UNCHECKED_PLAIN = {
    "scan_unavailable": "The page renderer could not open this file, so hidden text could not be checked.",
    "too_many_text_objects": "This page has more text pieces than the hidden-text check will examine.",
    "too_many_hidden_objects": "This page has an unusually large number of hidden text pieces, so it is held back whole.",
    "page_not_rendered": "The page renderer could not read this page, so hidden text could not be checked.",
    "too_many_annotations": "This page has more annotations than the hidden-text check will examine.",
}


class HiddenScanUnavailable(RuntimeError):
    """The renderer could not read the file; hidden text could not be checked (the caller holds every page back as unchecked).
    `texts` is the text layer when the child had already read it before it failed (None otherwise)."""

    def __init__(self, reason="", texts=None):
        super().__init__(reason)
        self.texts = texts


class HiddenScanTimeout(RuntimeError):
    """The shared deadline passed while scanning; the work stopped here."""


class _Unchecked(Exception):
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


# ------------------------------------------------------------------ PDFium helpers
def _text_of(raw, obj, textpage) -> str:
    n = raw.FPDFTextObj_GetText(obj, textpage, None, 0)
    if n <= 0:
        return ""
    buf = ctypes.create_string_buffer(n * 2 + 4)
    raw.FPDFTextObj_GetText(obj, textpage, ctypes.cast(buf, ctypes.POINTER(raw.FPDF_WCHAR)), n + 1)
    return buf.raw.decode("utf-16-le", "replace").split("\x00", 1)[0]


def _effective_size(raw, obj) -> float:
    size = ctypes.c_float(0)
    raw.FPDFTextObj_GetFontSize(obj, size)
    m = raw.FS_MATRIX()
    if raw.FPDFPageObj_GetMatrix(obj, m):
        scale = (abs(m.a * m.d - m.b * m.c)) ** 0.5
        if scale > 0:
            return size.value * scale
    return size.value


def _render(page, scale, crop=(0, 0, 0, 0)):
    """(bytes, stride, width, height, channels, posconv) of a render. The bytes are a copy, so the bitmap is closed at once."""
    bitmap = page.render(scale=scale, crop=crop)
    try:
        return bytes(bitmap.buffer), bitmap.stride, bitmap.width, bitmap.height, bitmap.n_channels, bitmap.get_posconv(page)
    finally:
        bitmap.close()


def _count_diff(a: bytes, b: bytes, ch: int, need: int) -> int:
    """Pixels where two equal-length RGB(A) byte rows differ by DIFF_MIN or more in a colour channel; stops counting at `need`."""
    n, c3 = 0, min(ch, 3)
    for i in range(0, len(a) - ch + 1, ch):
        if a[i:i + ch] != b[i:i + ch] and any(abs(a[i + k] - b[i + k]) >= DIFF_MIN for k in range(c3)):
            n += 1
            if n >= need:
                return n
    return n


def _free_intervals(lo, hi, masks):
    """[lo, hi) minus the union of the (start, end) masks."""
    out, cur = [], lo
    for s, e in sorted(masks):
        if e <= cur:
            continue
        if s > cur:
            out.append((cur, min(s, hi)))
        cur = max(cur, e)
        if cur >= hi:
            break
    if cur < hi:
        out.append((cur, hi))
    return [(a, b) for a, b in out if b > a]


def _px_rect(posconv, bbox, w, h, pad=1):
    x0, y0, x1, y1 = bbox
    pts = [posconv.to_bitmap(x, y) for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
    px0, px1 = int(math.floor(min(p[0] for p in pts))) - pad, int(math.ceil(max(p[0] for p in pts))) + pad
    py0, py1 = int(math.floor(min(p[1] for p in pts))) - pad, int(math.ceil(max(p[1] for p in pts))) + pad
    return max(px0, 0), max(py0, 0), min(px1, w), min(py1, h)


class _Grid:
    """Rectangles in pixel space, bucketed so 'which boxes touch this one' is not a quadratic scan."""
    CELL = 64

    def __init__(self):
        self.cells, self.rects = {}, []

    def add(self, rect):
        i = len(self.rects)
        self.rects.append(rect)
        x0, y0, x1, y1 = rect
        for cx in range(x0 // self.CELL, max(x1 - 1, x0) // self.CELL + 1):
            for cy in range(y0 // self.CELL, max(y1 - 1, y0) // self.CELL + 1):
                self.cells.setdefault((cx, cy), []).append(i)
        return i

    def touching(self, rect, skip):
        x0, y0, x1, y1 = rect
        seen = set()
        for cx in range(x0 // self.CELL, max(x1 - 1, x0) // self.CELL + 1):
            for cy in range(y0 // self.CELL, max(y1 - 1, y0) // self.CELL + 1):
                for i in self.cells.get((cx, cy), ()):
                    if i != skip and i not in seen:
                        r = self.rects[i]
                        if r[0] < x1 and x0 < r[2] and r[1] < y1 and y0 < r[3]:
                            seen.add(i)
        return [self.rects[i] for i in seen]


def _clipped_away(raw, obj, bbox) -> bool:
    """True when the object's clipping path (all its paths intersected, taken by bounding box) leaves under CLIP_VISIBLE_MIN of the
    text's box showing. No clip path = False. Any failure to read the path = False (the render test still applies)."""
    try:
        cp = raw.FPDFPageObj_GetClipPath(obj)
        n = raw.FPDFClipPath_CountPaths(cp) if cp else -1
        if n <= 0:
            return False
        bx0, by0, bx1, by1 = bbox
        cx0, cy0, cx1, cy1 = -1e12, -1e12, 1e12, 1e12
        for p in range(n):
            xs, ys = [], []
            for j in range(raw.FPDFClipPath_CountPathSegments(cp, p)):
                seg = raw.FPDFClipPath_GetPathSegment(cp, p, j)
                x, y = ctypes.c_float(), ctypes.c_float()
                if seg and raw.FPDFPathSegment_GetPoint(seg, x, y):
                    xs.append(x.value)
                    ys.append(y.value)
            if not xs:
                return True                                       # a clip path with no points shows nothing
            cx0, cy0, cx1, cy1 = max(cx0, min(xs)), max(cy0, min(ys)), min(cx1, max(xs)), min(cy1, max(ys))
        area = max((bx1 - bx0) * (by1 - by0), 1e-6)
        ix, iy = max(0.0, min(bx1, cx1) - max(bx0, cx0)), max(0.0, min(by1, cy1) - max(by0, cy0))
        return (ix * iy) / area < CLIP_VISIBLE_MIN
    except Exception:
        return False


def _annotation_cover(raw, page, items, tick):
    """Adds `covered_by_annotation` to every text object whose box overlaps an annotation that may be drawn over it. PDFium leaves out
    form fields (Widget annotations) that the file's AcroForm does not list, so the render comparison cannot see such a cover although
    other viewers draw it. Hidden and no-view annotations are not drawn by anyone and are skipped; links and text markup
    (highlight, underline, strike-out) are exempt (the render comparison checks markup). A Popup is skipped only when it has no appearance:
    PDFium never draws one, so for a Popup with an appearance the render cannot tell and the text is suspected like any other cover."""
    n = raw.FPDFPage_GetAnnotCount(page.raw)
    if n <= 0:
        return
    if n > MAX_ANNOTS:
        raise _Unchecked("too_many_annotations")
    rects = []
    for k in range(n):
        annot = raw.FPDFPage_GetAnnot(page.raw, k)
        if not annot:
            continue
        try:
            sub = raw.FPDFAnnot_GetSubtype(annot)
            if sub in ANNOT_EXEMPT:
                continue
            if sub == POPUP and not raw.FPDFAnnot_HasKey(annot, b"AP"):
                continue                    # a Popup with no appearance draws nothing; one with an appearance may be drawn opaque over the text
            if raw.FPDFAnnot_GetFlags(annot) & (raw.FPDF_ANNOT_FLAG_HIDDEN | raw.FPDF_ANNOT_FLAG_NOVIEW):
                continue
            r = raw.FS_RECTF()
            if raw.FPDFAnnot_GetRect(annot, r):
                rects.append((min(r.left, r.right), min(r.bottom, r.top), max(r.left, r.right), max(r.bottom, r.top)))
        finally:
            raw.FPDFPage_CloseAnnot(annot)
    if not rects:
        return
    for k, i in enumerate(items):
        if k % 256 == 0:
            tick()
        b = i["bbox"]
        if not b:
            continue
        for r in rects:
            if r[0] < b[2] and b[0] < r[2] and r[1] < b[3] and b[1] < r[3]:
                i["reasons"].append("covered_by_annotation")
                break


# ------------------------------------------------------------------ one page
def _page_scan(raw, page, tick, budget) -> dict:
    page_box = page.get_cropbox() or page.get_mediabox()
    pw, ph = page.get_size()
    if not (pw > 0 and ph > 0):
        raise _Unchecked("page_not_rendered")
    scale = min(SCALE, MAX_SIDE_PX / max(pw, ph), math.sqrt(MAX_PIXELS / (pw * ph)))
    textpage = page.get_textpage()
    try:
        objs, has_image, count = [], False, 0
        for obj in page.get_objects(filter=[raw.FPDF_PAGEOBJ_TEXT, raw.FPDF_PAGEOBJ_IMAGE], max_depth=MAX_DEPTH):
            if obj.type == raw.FPDF_PAGEOBJ_IMAGE:
                has_image = True
                continue
            count += 1
            if count > MAX_TEXT_OBJECTS:
                raise _Unchecked("too_many_text_objects")
            if count % CHECK_EVERY == 0:
                tick()
            objs.append(obj)
        items = []                              # {bbox, reasons, mode, obj}; the text of an object is fetched only when it is hidden (it costs
        for k, obj in enumerate(objs):          # a search of the whole page text each, which made a busy page take minutes)
            if k % CHECK_EVERY == 0:
                tick()
            bbox = obj.get_bounds()
            reasons = []
            mode = raw.FPDFTextObj_GetTextRenderMode(obj.raw)
            if mode == INVISIBLE_MODE:
                reasons.append("invisible_render_mode")
            r, g, b, a = (ctypes.c_uint() for _ in range(4))
            if raw.FPDFPageObj_GetFillColor(obj.raw, r, g, b, a) and a.value == 0:
                reasons.append("transparent")
            if bbox:
                bx0, by0, bx1, by1 = bbox
                area = max((bx1 - bx0) * (by1 - by0), 1e-6)
                ix = max(0.0, min(bx1, page_box[2]) - max(bx0, page_box[0]))
                iy = max(0.0, min(by1, page_box[3]) - max(by0, page_box[1]))
                if (ix * iy) / area < 0.5:
                    reasons.append("off_page")
            if _effective_size(raw, obj.raw) < TINY_PT:
                reasons.append("tiny_font")
            if bbox and _clipped_away(raw, obj.raw, bbox):
                reasons.append("clipped")
            items.append({"bbox": bbox, "reasons": reasons, "mode": mode, "obj": obj})
        if items:
            _annotation_cover(raw, page, items, tick)
            _differential(raw, page, scale, items, tick, budget)
        hidden, hidden_text = [], []
        if sum(1 for i in items if i["reasons"]) > MAX_HIDDEN_OBJECTS:     # reading each one's text is a search of the whole page; not worth it
            raise _Unchecked("too_many_hidden_objects")
        for k, i in enumerate(items):
            if i["reasons"]:
                if k % CHECK_EVERY == 0:
                    tick()
                i["text"] = _text_of(raw, i["obj"].raw, textpage).strip()
                if "".join(i["text"].split()):      # an object holding only spaces draws nothing and says nothing: not hidden text
                    hidden.append({"text": i["text"], "reasons": i["reasons"], "bbox": [round(v, 1) for v in i["bbox"]] if i["bbox"] else None})
                    hidden_text.append(i["text"])
        try:
            page_text = textpage.get_text_range()   # every text object on the page, hidden or not, in one call
        except Exception:
            page_text = ""
        visible = ""
        if hidden and len(items) <= VISIBLE_REBUILD_MAX:       # only used if a hidden string cannot be matched in the extractor's text
            visible = "\n".join(_text_of(raw, i["obj"].raw, textpage).strip() for i in items if not i["reasons"])
    finally:
        textpage.close()
    return {"hidden": hidden, "visible_text": visible, "listed_text": page_text + "\n" + "\n".join(hidden_text),
            "has_image": has_image, "text_objects": len(items)}


def _differential(raw, page, scale, items, tick, budget):
    """Adds `blends_with_background` / `could_not_verify` to the items whose drawing changes nothing on the page."""
    cand = [i for i in items if not ({"invisible_render_mode", "off_page"} & set(i["reasons"]))]
    if not cand:
        return
    for i in cand:
        i["cand"] = True
    tick()
    full = _render(page, scale)
    for i in items:                                    # every text object off: what the page looks like without any text
        raw.FPDFTextObj_SetTextRenderMode(i["obj"].raw, INVISIBLE_MODE)
    try:
        tick()
        bare = _render(page, scale)
    finally:
        for i in items:
            raw.FPDFTextObj_SetTextRenderMode(i["obj"].raw, i["mode"])
    fb, stride, w, h, ch, posconv = full
    nb = bare[0]
    grid, ids = _Grid(), {}
    for n, i in enumerate(items):
        if i["bbox"]:
            ids[n] = grid.add(_px_rect(posconv, i["bbox"], w, h))
    for n, i in enumerate(items):
        if n % CHECK_EVERY == 0:
            tick()
        if not i.get("cand"):
            continue
        if not i["bbox"] or n not in ids:
            i["reasons"].append("could_not_verify")
            continue
        rect = grid.rects[ids[n]]
        x0, y0, x1, y1 = rect
        if x1 - x0 < 1 or y1 - y0 < 1:
            i["reasons"].append("blends_with_background")       # the box lies outside the picture: nothing of it is drawn
            continue
        near = grid.touching(rect, ids[n])
        if len(near) > NEAR_MAX:                                 # a pile of overlapping text: no per-pixel work, hold it back
            i["reasons"].append("could_not_verify")
            continue
        verdict = _mask_verdict(fb, nb, stride, ch, rect, near, tick)
        if verdict is None:                                      # too much of the box is shared with other text: test this object alone
            if budget["exact"] <= 0:
                i["reasons"].append("could_not_verify")
                continue
            budget["exact"] -= 1
            verdict = _exact_verdict(raw, page, scale, i, tick)
        if not verdict:
            i["reasons"].append("blends_with_background")


def _mask_verdict(fb, nb, stride, ch, rect, near, tick):
    """True = the text changes pixels in its own box; False = it changes none; None = other text boxes cover too much to tell."""
    x0, y0, x1, y1 = rect
    area = (x1 - x0) * (y1 - y0)
    covered = 0
    for y in range(y0, y1):
        if y % 32 == 0:
            tick()
        m = [(max(r[0], x0), min(r[2], x1)) for r in near if r[1] <= y < r[3]]
        free = _free_intervals(x0, x1, m)
        covered += (x1 - x0) - sum(b - a for a, b in free)
    if area and covered / area > OVERLAP_EXACT:
        return None
    seen = 0
    for y in range(y0, y1):
        if y % 32 == 0:
            tick()
        a, b = fb[y * stride + x0 * ch: y * stride + x1 * ch], nb[y * stride + x0 * ch: y * stride + x1 * ch]
        if a == b:
            continue
        m = [(max(r[0], x0), min(r[2], x1)) for r in near if r[1] <= y < r[3]]
        for s, e in _free_intervals(x0, x1, m):
            seen += _count_diff(a[(s - x0) * ch:(e - x0) * ch], b[(s - x0) * ch:(e - x0) * ch], ch, MIN_PIXELS - seen)
            if seen >= MIN_PIXELS:
                return True
    return False


def _exact_verdict(raw, page, scale, item, tick) -> bool:
    """Draw a margin around the object with and without THIS object only (everything else as the file says) and compare."""
    x0, y0, x1, y1 = item["bbox"]
    left, bottom, right, top = page.get_cropbox() or page.get_mediabox()
    m = 2.0
    crop = (max(x0 - m - left, 0), max(y0 - m - bottom, 0), max(right - (x1 + m), 0), max(top - (y1 + m), 0))
    pw, ph = page.get_size()
    if crop[0] + crop[2] >= pw - 1 or crop[1] + crop[3] >= ph - 1:
        return False                                              # the margin box is off the page: nothing visible
    tick()
    with_it = _render(page, scale, crop)
    raw.FPDFTextObj_SetTextRenderMode(item["obj"].raw, INVISIBLE_MODE)
    try:
        tick()
        without = _render(page, scale, crop)
    finally:
        raw.FPDFTextObj_SetTextRenderMode(item["obj"].raw, item["mode"])
    if with_it[0] == without[0]:
        return False
    return _count_diff(with_it[0], without[0], with_it[4], MIN_PIXELS) >= MIN_PIXELS


# ------------------------------------------------------------------ the document
def scan_inprocess(data: bytes, deadline: float = None) -> dict:
    """{"checked": bool, "pages": {n: {hidden: [{text, reasons, bbox}], visible_text, listed_text, has_image, text_objects, unchecked?}}}.
    A page that could not be scanned has `unchecked: <reason>` and no text lists. `deadline` is a time.monotonic() value; the scan stops
    there (checked between pages, every CHECK_EVERY objects and before every render) with HiddenScanTimeout. A native render call cannot
    be interrupted, so callers on a server use scan(), which runs this in a child process that is killed at the deadline.
    Raises HiddenScanUnavailable when PDFium cannot open the file."""
    try:
        import pypdfium2 as pdfium
        import pypdfium2.raw as raw
    except ImportError as e:        # pragma: no cover - the dependency is pinned in requirements.txt
        raise HiddenScanUnavailable("pypdfium2 is not installed") from e

    def tick():
        if deadline is not None and time.monotonic() > deadline:
            raise HiddenScanTimeout("deadline")

    out, budget = {}, {"exact": EXACT_MAX}
    try:
        pdf = pdfium.PdfDocument(data)
        try:
            try:
                pdf.init_forms()        # before any page is loaded: lets PDFium draw the form fields the file's AcroForm lists
            except Exception:
                pass
            for i in range(len(pdf)):
                tick()
                try:
                    page = pdf[i]
                except Exception:
                    out[i + 1] = _unchecked("page_not_rendered")
                    continue
                try:
                    out[i + 1] = _page_scan(raw, page, tick, budget)
                except _Unchecked as u:
                    out[i + 1] = _unchecked(u.reason)
                except HiddenScanTimeout:
                    raise
                except Exception:                  # one page the renderer chokes on must not take the check off the others
                    out[i + 1] = _unchecked("page_not_rendered")
                finally:
                    page.close()
        finally:
            pdf.close()
    except (HiddenScanUnavailable, HiddenScanTimeout):
        raise
    except Exception as e:           # PDFium raises PdfiumError / ValueError / OSError on files it cannot read
        raise HiddenScanUnavailable(type(e).__name__) from None
    return {"checked": not any(p.get("unchecked") for p in out.values()), "pages": out}


# ------------------------------------------------------------------ the PDF parsers in a child process
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_SLOTS = threading.BoundedSemaphore(MAX_CHILDREN)
_CHILD_ENV_KEEP = ("PATH", "LANG", "LC_ALL", "LC_CTYPE", "TMPDIR")      # nothing else: no API key, token or HOME reaches the child


def _rss_bytes(pid: int) -> int:
    """Resident memory of a process we started, from ps (works on macOS and Linux); 0 when it cannot be read or has gone."""
    try:
        out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True, timeout=2).stdout.strip()
        return int(out.split()[0]) * 1024 if out else 0
    except (OSError, ValueError, IndexError, subprocess.SubprocessError):
        return 0


def _messages(out: bytes) -> list:
    """The JSON lines a child wrote (a killed child leaves a partial last line, which is ignored)."""
    msgs = []
    for line in (out or b"").split(b"\n"):
        try:
            m = json.loads(line.decode("utf-8")) if line.strip() else None
        except ValueError:
            m = None
        if isinstance(m, dict):
            msgs.append(m)
    return msgs


def _texts_of(msgs):
    for m in msgs:
        if isinstance(m.get("texts"), list):
            return m["texts"]
    return None


def _run_child(data: bytes, deadline, mode: str, extra: str = ""):
    """Runs `python -m app.backend.pdf_hidden <seconds> <mode> [extra]` ('scan' | 'text' | 'both' | 'render', whose extra is the page list) and returns its JSON lines. Every PDF parser (pypdf's
    text read and PDFium's render) runs in this child and nowhere else (T-087 round 4). The child gets a hard wall-clock kill at `deadline`
    (a time.monotonic() value; default DEFAULT_SCAN_S from now), an RLIMIT_CPU just past it, core dumps off, RLIMIT_AS where the platform
    enforces it and a parent-side RSS watch on every platform. Only the child process this call started is ever killed."""
    now = time.monotonic()
    deadline = deadline if deadline is not None else now + DEFAULT_SCAN_S
    if now >= deadline:
        raise HiddenScanTimeout("deadline")
    if not _SLOTS.acquire(timeout=max(deadline - now, 0)):
        raise HiddenScanTimeout("deadline")        # every slot busy until the deadline: the caller's wait is over
    proc = None
    try:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise HiddenScanTimeout("deadline")
        env = {k: os.environ[k] for k in _CHILD_ENV_KEEP if k in os.environ}
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        try:
            proc = subprocess.Popen([sys.executable, "-m", "app.backend.pdf_hidden", "%.3f" % remaining, mode] + ([extra] if extra else []), cwd=_ROOT, env=env,
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, close_fds=True)
        except OSError as e:
            raise HiddenScanUnavailable(type(e).__name__) from None
        stdin, proc.stdin = proc.stdin, None        # the file goes in from its own thread in big writes (T-107): Popen.communicate(input) writes
                                                    # 512 bytes per loop on macOS and loses the GIL each time, so two uploads at once took minutes

        def feed():
            try:
                stdin.write(data)
            except (OSError, ValueError):           # the child died or was killed before it read the file; the loop below sees that
                pass
            finally:
                try:
                    stdin.close()
                except (OSError, ValueError):
                    pass
        threading.Thread(target=feed, daemon=True).start()
        out = b""
        while True:
            left = deadline - time.monotonic()
            if left <= 0:
                proc.kill()
                proc.communicate()                  # reap it
                raise HiddenScanTimeout("deadline")
            try:
                out, _ = proc.communicate(timeout=min(WATCH_EVERY_S, left))
                break
            except subprocess.TimeoutExpired:
                pass
            except OSError:
                proc.kill()
                proc.communicate()
                raise HiddenScanUnavailable("child_died") from None
            if _rss_bytes(proc.pid) > CHILD_RSS_BYTES:
                proc.kill()
                partial, _ = proc.communicate()
                raise HiddenScanUnavailable("memory", _texts_of(_messages(partial)))
        msgs = _messages(out)
        if proc.returncode == -getattr(signal, "SIGXCPU", 24):
            raise HiddenScanTimeout("cpu_limit")
        if proc.returncode != 0 or not msgs:
            raise HiddenScanUnavailable("child_failed", _texts_of(msgs))
        return msgs
    finally:
        if proc is not None and proc.poll() is None:
            proc.kill()
            proc.wait()
        _SLOTS.release()


def _pdf_error(msgs):
    """Re-raises, in the parent, the PdfError the child's text read ended with (a size, header, encryption or page-count refusal)."""
    from app.backend.pdf_text import PdfError
    for m in msgs:
        if m.get("pdf_error"):
            raise PdfError(str(m["pdf_error"]), m.get("detail") if isinstance(m.get("detail"), dict) else None)


def scan(data: bytes, deadline: float = None, with_text: bool = False) -> dict:
    """scan_inprocess() in a child Python process (see _run_child). Whatever the child is doing, nothing runs after the deadline:
    HiddenScanTimeout. A child that crashes or runs out of memory is HiddenScanUnavailable (the caller holds every page back as unchecked).
    `with_text=True` also has the same child read the text layer with pypdf first and adds it to the result as `texts` (a refusal such
    as pdf_encrypted is raised as PdfError); if the scan then fails, HiddenScanUnavailable carries `.texts`."""
    msgs = _run_child(data, deadline, "both" if with_text else "scan")
    if with_text:
        _pdf_error(msgs)
    texts = _texts_of(msgs)
    msg = msgs[-1]
    if with_text and texts is None:
        raise HiddenScanUnavailable("child_failed")
    if msg.get("error") == "timeout":
        raise HiddenScanTimeout("deadline")
    if "result" not in msg:
        raise HiddenScanUnavailable(str(msg.get("error") or "child_failed")[:60], texts)
    res = msg["result"]
    out = {"checked": res["checked"], "pages": {int(k): v for k, v in res["pages"].items()}}
    if with_text:
        out["texts"] = texts
    return out


def read_text(data: bytes, deadline: float = None) -> list:
    """pdf_text.read_pages() in the killed child (no scan): the stripped text of every page. Raises PdfError like read_pages, plus
    pdf_unreadable when the child failed and HiddenScanTimeout at the deadline."""
    from app.backend.pdf_text import PdfError
    try:
        msgs = _run_child(data, deadline, "text")
    except HiddenScanUnavailable:
        raise PdfError("pdf_unreadable") from None
    _pdf_error(msgs)
    texts = _texts_of(msgs)
    if texts is None:
        raise PdfError("pdf_unreadable")
    return texts


def render_messages(data: bytes, pages: list, deadline: float = None) -> list:
    """OCR page rendering in the same killed child (T-107): the child's JSON lines (see pdf_ocr.render_in_child). PDFium opens the file and
    draws the pages only inside the child, with the deadline kill, RLIMIT_CPU and the RSS watch, so a stamp or appearance bomb costs the API
    process nothing. A child that was killed, crashed or ran out of time is HiddenScanUnavailable / HiddenScanTimeout; there is no
    in-process fallback (pdf_ocr.render_pages turns both into OcrFailed)."""
    return _run_child(data, deadline, "render", ",".join(str(int(n)) for n in pages))


def _limit_child(remaining: float):
    """Called first thing in the child: CPU limit just past the deadline, no core files, memory limit where it is enforced."""
    try:
        import resource
    except ImportError:             # pragma: no cover - non-POSIX
        return
    cpu = int(math.ceil(remaining)) + 1
    for what, soft, hard in ((resource.RLIMIT_CPU, cpu, cpu + 2), (resource.RLIMIT_CORE, 0, 0),
                             (getattr(resource, "RLIMIT_AS", None), CHILD_MEM_BYTES, CHILD_MEM_BYTES)):
        if what is None:
            continue
        try:
            resource.setrlimit(what, (soft, hard))
        except (ValueError, OSError):       # macOS refuses RLIMIT_AS (ValueError); the CPU limit, the parent's kill and its RSS watch still hold
            pass


def _emit(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def _child_main(argv):
    remaining = float(argv[1]) if len(argv) > 1 else DEFAULT_SCAN_S
    mode = argv[2] if len(argv) > 2 else "scan"
    start = time.monotonic()
    _limit_child(remaining)
    data = sys.stdin.buffer.read()
    soft = start + remaining - 0.2
    try:
        if mode == "render":
            from app.backend import pdf_ocr
            pdf_ocr.render_in_child(data, [int(x) for x in (argv[3] if len(argv) > 3 else "").split(",") if x.strip().isdigit()], soft, _emit)
            return
        if mode in ("text", "both"):
            from app.backend import pdf_text
            try:
                _emit({"texts": pdf_text.read_pages(data, soft)})
            except pdf_text.PdfError as e:
                _emit({"pdf_error": e.code, "detail": e.detail})
                return
        if mode in ("scan", "both"):
            _emit({"result": scan_inprocess(data, soft)})
    except HiddenScanTimeout:
        _emit({"error": "timeout"})
    except HiddenScanUnavailable as e:
        _emit({"error": "unavailable: %s" % e})
    except MemoryError:
        _emit({"error": "memory"})


def _unchecked(reason: str) -> dict:
    return {"hidden": [], "visible_text": "", "listed_text": "", "has_image": False, "text_objects": 0, "unchecked": reason}


def unchecked_scan(n_pages: int, reason: str = "scan_unavailable") -> dict:
    """The scan result for a file the renderer could not open: every page unchecked."""
    return {"checked": False, "pages": {n: _unchecked(reason) for n in range(1, n_pages + 1)}}


# ------------------------------------------------------------------ reconciling the two readers
_WORD = re.compile(r"[^\W_]+", re.UNICODE)


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s).casefold()


def unlisted_spans(page_text: str, listed_text: str) -> list:
    """Runs of words in the extractor's page text that no text object the renderer listed contains. The extractor (pypdf) and the renderer
    (PDFium) are two readers of one file; text only the extractor can reach (nested deeper than the renderer draws, in a part of the
    file it skips) is text a reader of the rendered page never sees. A word counts as listed when it occurs, case-folded, inside the
    renderer's text with spaces removed, so ligatures, hyphenation and line breaks do not cause false alarms; a single letter does not
    count as a word. Returns the unlisted runs as they appear in `page_text`, whitespace kept."""
    pool = "".join(_WORD.findall(_norm(listed_text)))
    spans, run = [], None
    for m in _WORD.finditer(page_text):
        w = _norm(m.group(0))
        if len(w) < 2 and not w.isdigit():
            continue
        if w in pool:
            if run is not None:
                spans.append(page_text[run[0]:run[1]])
                run = None
        else:
            run = (m.start(), m.end()) if run is None else (run[0], m.end())
    if run is not None:
        spans.append(page_text[run[0]:run[1]])
    return spans


def remove_from_text(page_text: str, hidden: list, visible_text: str) -> str:
    """The page's extracted text without the hidden strings. Each hidden string is removed once, matched ignoring whitespace; if any
    cannot be found in the extractor's text (the two libraries read the page differently), the page text is rebuilt from the visible
    text objects alone, so hidden text can never be left in by accident."""
    text = page_text
    for h in hidden:
        chars = [re.escape(c) for c in h["text"] if not c.isspace()]
        if not chars:
            continue
        m = re.search(r"\s*".join(chars), text)
        if not m:
            return visible_text.strip()
        a, b = m.start(), m.end()
        line_start = a == 0 or text[a - 1] == "\n"
        line_end = b >= len(text) or text[b] == "\n"
        if line_start and line_end and b < len(text):
            b += 1                     # the hidden string was a whole line: take its line break too
        text = text[:a] + text[b:]
    return text.strip()


def report(scanned: dict, confirmed: set) -> dict:
    """The per-page report stored with the case and returned to the UI. `confirmed` = page numbers whose hidden text the paralegal
    chose to include. A page that could not be checked is listed with `unchecked: true`, `count: 0` and a plain reason."""
    pages, unchecked = [], []
    for n, p in sorted(scanned["pages"].items()):
        if p.get("unchecked"):
            unchecked.append(n)
            pages.append({"page": n, "count": 0, "items": [], "unchecked": True, "why": UNCHECKED_PLAIN.get(p["unchecked"], UNCHECKED_PLAIN["page_not_rendered"]),
                          "confirmed": n in confirmed, "excluded": n not in confirmed})
            continue
        if not p["hidden"]:
            continue
        items = [{"text": h["text"][:TEXT_CAP], "truncated": len(h["text"]) > TEXT_CAP, "reasons": h["reasons"],
                  "why": ", ".join(REASON_PLAIN[r] for r in h["reasons"])} for h in p["hidden"][:MAX_ITEMS_PER_PAGE]]
        pages.append({"page": n, "count": len(p["hidden"]), "items": items, "unchecked": False, "confirmed": n in confirmed,
                      "excluded": n not in confirmed})
    return {"checked": not unchecked, "unchecked_pages": unchecked, "pages": pages, "excluded_until_confirmed": True}


if __name__ == "__main__":      # the scan child (`python -m app.backend.pdf_hidden <seconds>`); must stay the last statement in the file
    _child_main(sys.argv)
