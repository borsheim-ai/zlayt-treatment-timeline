# Subagent: Backend: T-086 + T-087 PDF OCR/hidden (Backend: T-086 + T-087 PDF OCR/hidden)

Source: `agent-a8532fa632b8e39fc.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:16:34.788Z

You own board cards T-086 and T-087 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Run `board.py show` on each and read D-042 in memory/ORCHESTRATOR_DECISIONS.md, app/backend/pdf_text.py and the OCR-failure section of research/record-formats.md. Both cards are PDF work, so do them in one module set.

**T-087 — hidden-text detection:**
- Detect text that is present in the text layer but not visible when rendered: white or near-background text, off-page text, and tiny fonts. Use a pinned, permissively licensed local library such as pypdfium2, and add it to requirements.txt pinned, with no network.
- Flag it per page and exclude it from grounding until the paralegal confirms.
- Test with a synthetic PDF generated in the test.

**T-086 — local OCR:**
- Use the Tesseract binary through subprocess or pytesseract, pinned. A missing tesseract gives a clear message, never a crash.
- Scanned pages are OCR'd locally, and the page image is available beside the OCR text.
- Low-confidence words are marked.
- Every OCR-derived item is always needs_review.
- Tests skip cleanly if tesseract isn't installed; check `which tesseract`.
- Document the install line for the README in a card note (release owns README).

Add the contract to api.md, and note on the cards what the UI needs. Run pip-audit on any new dependency if it's available.

**Shared rules (8 workers are running in parallel):**
- Put the logic in new modules. In shared files (api.py, pipeline.py, api.md, requirements.txt), make the smallest possible edit, re-read the file right before editing, and never reformat.
- Don't touch flags.py or judges.py (T-094 is in them), evals/library, or evals/run.py.
- Commit only your own hunks. Use a temp index (`GIT_INDEX_FILE=$(mktemp) git read-tree HEAD`, then add your paths or patches) when a shared file has other workers' edits; otherwise `git add <paths>` then `git commit -m "..." -- <paths>` as separate commands. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".
- Run `.venv/bin/python -m pytest -q tests/unit`. If a failure is in someone else's area, name it and move on.
- Then `board.py ac`, the handoff, and `move <card> in_review --agent backend`, for each card. Reply in 2 lines.

### User / tool · 2026-11-02T04:16:34.792Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:36.923Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B show T-086; $B show T-087; grep -n \"D-042\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -40; which tesseract; ls app/backend; cat requirements.txt; .venv/bin/pip list 2>/dev/null | grep -i -E \"pdfium|pytesseract|pdfplumber|pypdf|pymupdf|reportlab|pillow|audit\""
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:37.458Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/pdf_text.py"
}
````

### User / tool · 2026-11-02T04:16:37.515Z

**tool result**
````
---
id: "T-086"
title: "Local OCR (Tesseract) for scanned PDFs with a verification step"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:16:04Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Scanned PDF pages OCR locally (no network); page image shown beside OCR text; low-confidence words marked; OCR-derived items always needs_review; missing tesseract gives a clear message; tests", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed

## Handoff (filled when moving to in_review)

---
id: "T-087"
title: "PDF hidden-text detection (render vs text layer)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:16:04Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Text present in the text layer but not visible when rendered (white text, off-page, tiny font) is flagged per page and excluded from grounding until the paralegal confirms; tests with a synthetic PDF", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed

## Handoff (filled when moving to in_review)

50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
51-| D-043 | Credibility flags fail toward flagging (2026-11-02, after T-067 r3): any sentence containing a credibility term flags, **unless** the whole sentence is one clause matching a short allow-list of clean negations ('No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Not tested/not performed.'). Anything with a second clause, contrast word or side qualifier flags. An extra flag costs one paralegal click; a missed one costs credibility at the adjuster. | Three rounds of clause-scoped negation each regressed a different word order. | T-067 claims-adjuster r3 |
52-| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
53-| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
/opt/homebrew/bin/tesseract
__init__.py
__pycache__
amounts.py
api.py
case_extras.py
confidence.py
conflict_candidates.py
conflicts.py
credibility.py
dates.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judges.py
lexicon.py
lexicon_scan.py
narrative.py
pdf_text.py
pipeline.py
present.py
rejudge.py
review.py
schemas.py
sentences.py
split_llm.py
store.py
totals.py
trace.py
why.py
# Runtime dependencies, exact versions from the working .venv (pip freeze minus test tools). Python 3.12.
# Test/dev tools are in requirements-dev.txt. Release adopts these pins; re-run pip-audit when they change.
annotated-doc==0.0.5
annotated-types==0.8.0
anthropic==2.3.0
anyio==4.16.0
certifi==2026.10.23
click==8.5.0
docstring_parser==0.18.0
fastapi==0.162.0
h11==0.16.0
httpcore==1.0.9
httpcore2==2.16.0
httptools==0.9.0
httpx==0.28.1
httpx2==2.16.0
idna==3.20
jiter==0.18.0
opentelemetry-api==1.45.2
packaging==26.3
pydantic==2.14.2
pydantic_core==2.50.2
pypdf==6.21.4
python-dotenv==1.2.4
python-multipart==0.0.33
PyYAML==6.0.3
sniffio==1.3.1
starlette==1.10.0
truststore==0.10.5
typing-inspection==0.4.4
typing_extensions==4.16.0
uvicorn==0.54.0
uvloop==0.23.0
watchfiles==1.3.0
websockets==17.4
pypdf             6.21.4
````

### User / tool · 2026-11-02T04:16:37.524Z

**tool result**
````
1	"""PDF text-layer extraction (D-031). Pure python (pypdf), no OCR: a PDF with no text layer is refused before anything is stored or any
2	model is called. The extracted text is the case text; `pages` maps character offsets of that text to page numbers so citations can
3	carry them. Deterministic code only."""
4	import io
5	import logging
6	import time
7	import warnings
8	
9	MAX_PDF_BYTES = 5 * 1024 * 1024
10	MAX_PAGES = 100
11	EXTRACT_TIMEOUT_S = 10.0     # the API stops waiting after this long (the worker thread is left to finish; page and size caps bound it)
12	MIN_TEXT_CHARS = 20          # fewer non-space characters than this in the whole file = no usable text layer
13	
14	
15	# pypdf logs fragments of the document it is parsing (record text) when a file is malformed; the app never logs record text, so the
16	# library's logger is cut off from every handler and its warnings are ignored during extraction.
17	_lg = logging.getLogger("pypdf")
18	_lg.addHandler(logging.NullHandler())
19	_lg.propagate = False
20	_lg.setLevel(logging.CRITICAL + 1)
21	
22	
23	class PdfError(ValueError):
24	    """str(e) is the API error code: pdf_no_text_layer | pdf_unreadable | pdf_too_large | pdf_encrypted."""
25	
26	    @property
27	    def code(self) -> str:
28	        return str(self)
29	
30	
31	def extract(data: bytes) -> dict:
32	    """{text, pages: [{page, start, end}]}. Page texts are stripped and joined with a blank line, so offsets index the text exactly."""
33	    if len(data or b"") > MAX_PDF_BYTES:
34	        raise PdfError("pdf_too_large")
35	    if not (data or b"").lstrip()[:5] == b"%PDF-":
36	        raise PdfError("pdf_unreadable")
37	    from pypdf import PdfReader
38	    from pypdf.errors import PyPdfError
39	    deadline = time.monotonic() + EXTRACT_TIMEOUT_S
40	    try:
41	        with warnings.catch_warnings():
42	            warnings.simplefilter("ignore")
43	            reader = PdfReader(io.BytesIO(data))
44	            if reader.is_encrypted:
45	                raise PdfError("pdf_encrypted")
46	            if len(reader.pages) > MAX_PAGES:
47	                raise PdfError("pdf_too_large")
48	            texts = []
49	            for page in reader.pages:
50	                if time.monotonic() > deadline:         # stop the worker thread between pages once the API has given up on it
51	                    raise PdfError("pdf_unreadable")
52	                texts.append((page.extract_text() or "").replace("\r\n", "\n").replace("\r", "\n").strip())
53	    except PdfError:
54	        raise
55	    except (PyPdfError, ValueError, KeyError, OSError, RecursionError, AssertionError, TypeError):
56	        raise PdfError("pdf_unreadable") from None
57	    if sum(len("".join(t.split())) for t in texts) < MIN_TEXT_CHARS:
58	        raise PdfError("pdf_no_text_layer")
59	    text, pages = "", []
60	    for i, t in enumerate(texts, 1):
61	        if not t:
62	            continue
63	        if text:
64	            text += "\n\n"
65	        pages.append({"page": i, "start": len(text), "end": len(text) + len(t)})
66	        text += t
67	    return {"text": text, "pages": pages}
68	
69	
70	def page_for(pages: list, offset: int):
71	    """Page number whose span holds `offset` (a gap between pages belongs to the earlier page); None when there is no page map."""
72	    if not pages or offset is None:
73	        return None
74	    hit = None
75	    for p in pages:
76	        if p["start"] <= offset:
77	            hit = p["page"]
78	    return hit
79	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:40.090Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"ocr\" research/record-formats.md | head -30; .venv/bin/pip list 2>/dev/null | grep -i -E \"pdfium|tesser|pillow|reportlab|fpdf|audit|pytest\"; .venv/bin/pip download pypdfium2==4.30.0 --no-deps -d /tmp/x 2>&1 | tail -2; tesseract --version 2>&1 | head -2; tesseract --list-langs; grep -n \"pdf_text\\|pdf\" app/backend/api.py | head -40; grep -n -i \"pdf\" memory/contracts/api.md | head -20"
}
````

### User / tool · 2026-11-02T04:16:41.432Z

**tool result**
````
5:tool's hard parts: dates, charges versus rates versus adjustments, totals lines, multiple authors, Spanish text and OCR noise.
52:line, so OCR reads `150 | 00` as `15000` or `150 00`. The shaded supplemental line *does* use a decimal point. Ledgers show credits as
179:- Travel-card checkmarks are OCR-hostile (see section 14); a missed checkmark loses a modality, a stray mark invents one.
350:- `150 | 00` OCRs as `15000` ($15,000) or `150 00`; the decimal is implied by the box, not printed.
356:- 10b "Auto accident? YES  Place (State) TX" is a useful corroborating checkbox and an OCR checkbox trap.
384:**Specimen (SYNTHETIC), the same claim as OCR text** (what a scanned copy returns; truth beside each money string):
386:SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS
395:every OCR-derived amount and date goes to review with the page image. A parser that reads `8500` as dollars bills $8,500 per adjustment.)
651:## 14. Scanned and handwritten intake forms (and OCR failure modes)
661:**OCR failure modes to reproduce.**
662:| Failure | Example (truth → OCR) | Consequence |
676:- *Compact Multimodal Language Models as Robust OCR Alternatives for Noisy Textual Clinical Reports* (arXiv 2511.13523): https://arxiv.org/html/2511.13523v1 — **opened**. Takeaway: on smartphone photos of printed clinical reports, Tesseract scored CER 0.189, WER 0.276 and numeric accuracy 0.756, worse than neural pipelines and small multimodal models; Tesseract struggled most with blur and shadows. (Cite by arXiv number; authors not recorded here.)
677:- Tesseract OCR mailing list, thread on reading "X" checkboxes: https://groups.google.com/g/tesseract-ocr/c/r9mVUg76iE0 — search summary; out-of-the-box quality is medium; form jargon needs training; one user got better results at 150 dpi than 600 dpi.
678:- ImageToTable blog, *Why AI reads handwriting but misses a ticked box*: https://imagetotable.ai/blog/how-ai-reads-handwritten-forms-checkboxes-to-excel — search summary (vendor); generic OCR has no character for a tick and skips or garbles it.
679:- Assumption: glyph confusions in the table are the standard OCR confusion set; I found no Tesseract-specific measurement of them.
681:**Specimen (SYNTHETIC)** — what the page shows, then what OCR returns:
689:[OCR TEXT as extracted]
699:(The chosen pain score and the prior-injury answer are not recoverable from the OCR text alone; the item needs the page image and review.)
1002:| Chiro note + travel card | Cloned notes; checkbox OCR | Travel card rows need review when OCR-derived |
1012:| Scanned intake | OCR glyphs, checkboxes, fax/stamp dates | OCR-derived items always need review; page image beside text |
1023:2. *Chiro under LOP*: intake form (scanned) + LOP + chiro daily notes with a travel card + CMS-1500 with a grouped date range (clean and OCR
1059:  Donis 2021 opinion, Ezel narrative template, arXiv OCR paper, Jotform LOP packet.
1068:- **OCR figures** come from one paper on smartphone photos of printed reports, not handwritten forms; handwriting is likely worse.
pytest            9.2.0
[notice] A new release of pip is available: 24.0 -> 26.2.2
[notice] To update, run: python3.12 -m pip install --upgrade pip
tesseract 5.5.2
 leptonica-1.87.0
List of available languages in "/opt/homebrew/share/tessdata/" (3):
eng
osd
snum
23:from app.backend import case_extras, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
38:_PDF_MESSAGES = {"pdf_no_text_layer": "This PDF has no text layer (it looks scanned). Scanned pages are not read; paste the text instead.",
39:                 "pdf_unreadable": "This file could not be read as a PDF.", "pdf_encrypted": "This PDF is password-protected and cannot be read.",
40:                 "pdf_too_large": "The PDF is too large."}
248:    @app.post("/api/cases/pdf", status_code=201)
249:    async def create_case_from_pdf(request: Request, name: str = None):
250:        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer only; a scanned PDF is refused before anything is stored or run."""
254:        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
259:            if len(data) > pdf_text.MAX_PDF_BYTES:
262:            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data), pdf_text.EXTRACT_TIMEOUT_S)
264:            raise ApiError(400, "bad_request", _PDF_MESSAGES["pdf_unreadable"], {"reason": "pdf_timeout"}) from None
265:        except pdf_text.PdfError as e:
266:            raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
268:        return make_case(got["text"], name, False, pdf_pages=got["pages"])
270:    def make_case(text, name, sample, pdf_pages=None):
284:                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages}} if pdf_pages else {}))
287:                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
71:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
73:## POST /api/cases/pdf (D-031)
74:Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
75:Errors: `400 bad_request` with `detail.reason` = `pdf_no_text_layer` (looks scanned: refused before anything is stored, no model call), `pdf_unreadable`, `pdf_encrypted`; `413 input_too_large` (`pdf_too_large`).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:45.767Z

**tool call — Bash**
````
{
 "command": ".venv/bin/pip install pypdfium2 2>&1 | tail -3; .venv/bin/pip list 2>/dev/null | grep -i -E \"pdfium|pillow|numpy\"; ls requirements*; sed -n 1,40p app/backend/ingest.py | head -50; sed -n 240,300p app/backend/api.py"
}
````

### User / tool · 2026-11-02T04:16:47.170Z

**tool result**
````
[notice] A new release of pip is available: 24.0 -> 26.2.2
[notice] To update, run: python3.12 -m pip install --upgrade pip
pypdfium2         5.14.0
requirements-dev.txt
requirements.txt
"""Stage 0 ingest (all code): split, header date/source, kind, duplicate merge, limits, injection tag, warnings.
R-IN-1, R-IN-3..5, R-TL-3, R-TL-7, R-TL-9, R-RV-6; LLM_VS_CODE rows 1, 2, 3, 16, 17. No model is called here: the D-031 split fallback takes an injected `splitter` callable.
Record text is never rewritten: every excerpt is a verbatim slice of the (newline-normalised) input."""
import re

from app.backend import dates, flag_templates, injection, lexicon

MAX_CHARS = 60000
MAX_RECORDS = 40

# The only text ever set aside as a non-record: the exact banner lines of the golden/sample files. Any other first line is kept as text.
BANNERS = ("SYNTHETIC — invented for evaluation; not real patient data",
           "SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data")

_HEADER = re.compile(r"^=== Record (\d+) ===[ \t]*$", re.MULTILINE)
_SEP = re.compile(r"^[ \t]*---+[ \t]*$", re.MULTILINE)
_DATE_LINE = re.compile(r"^Date:", re.MULTILINE)
_F_DATE = re.compile(r"^Date:[ \t]*(.*)$", re.MULTILINE)
_F_SRC = re.compile(r"^Source:[ \t]*(.*)$", re.MULTILINE)
_F_EXC = re.compile(r"^Excerpt:[ \t]*", re.MULTILINE)


class IngestError(ValueError):
    """Input refused before any processing; str(e) is the API error code ('bad_request' | 'input_too_large')."""

    @property
    def code(self) -> str:
        return str(self)


def normalize_text(raw: str) -> str:
    """CRLF and CR become LF; leading and trailing whitespace trimmed (api.md POST /api/cases)."""
    return (raw or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def check_limits(text: str, max_chars: int = MAX_CHARS) -> str:
    """Raise before anything else (and so before any LLM call): empty -> bad_request, oversize -> input_too_large."""
    t = normalize_text(text)
    if not t:
        raise IngestError("bad_request")
            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
            if lib is None:
                raise ApiError(404, "not_found", "No such library case.")
        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
        if not isinstance(text, str):
            raise ApiError(400, "bad_request", "Provide text or sample: true.")
        return make_case(text, b.get("name") if isinstance(b.get("name"), str) else (lib["name"] if lib else None), sample)

    @app.post("/api/cases/pdf", status_code=201)
    async def create_case_from_pdf(request: Request, name: str = None):
        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer only; a scanned PDF is refused before anything is stored or run."""
        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
            raise ApiError(413, "input_too_large", "The PDF is too large.")
        data = b""
        async for chunk in request.stream():
            data += chunk
            if len(data) > pdf_text.MAX_PDF_BYTES:
                raise ApiError(413, "input_too_large", "The PDF is too large.")
        try:       # parsing runs off the event loop (so /api/health stays responsive) under a time cap
            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data), pdf_text.EXTRACT_TIMEOUT_S)
        except asyncio.TimeoutError:
            raise ApiError(400, "bad_request", _PDF_MESSAGES["pdf_unreadable"], {"reason": "pdf_timeout"}) from None
        except pdf_text.PdfError as e:
            raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
                           _PDF_MESSAGES[e.code], {"reason": e.code}) from None
        return make_case(got["text"], name, False, pdf_pages=got["pages"])

    def make_case(text, name, sample, pdf_pages=None):
        try:
            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
        except ingest.IngestError as e:
            raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
        if demo_mode() and digest(text) not in allowed_hashes():
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        c = conn()
        try:
            now = time.time()
            DB.purge_expired(c, now)
            name = name if isinstance(name, str) else ("Sample case" if sample else None)
            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None,
                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages}} if pdf_pages else {}))
            try:
                ing = pipeline_mod().ingest_case(c, cid, text, now)
                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
                flags = DB.list_items(c, cid, "flag")
            except Exception as e:                       # nothing of a failed create stays stored (ADR-006): drop the case row and its parts
                DB.delete_case(c, cid)
                if isinstance(e, ingest.IngestError):
                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code) from None
                log.error("create failed %s", type(e).__name__)
                raise ApiError(500, "internal", "Something went wrong.") from None
            return {"token": cid, "name": DB.get_case(c, cid)["name"], "status": "ingested", "source": "sample" if sample else "paste",
                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
                    "dates_to_confirm": present.dates_to_confirm(c, cid),
                    "gap_flags": [f["id"] for f in flags if f["type"] == "gap"],
                    "record_warning_flags": [f["id"] for f in flags if f["type"] == "record_warning"],
                    "warnings": ing["warnings"]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:20.047Z

**tool call — Bash**
````
{
 "command": "grep -rn \"needs_review\" app/backend app/db app/llm --include=*.py | head -30; grep -n \"pages\" app/backend/present.py app/backend/review.py app/backend/export.py app/backend/pipeline.py | head -30; grep -rn \"pdf\" tests/unit/*.py -l; grep -n \"def create_case\\|config_json\" app/db/*.py | head"
}
````

### User / tool · 2026-11-02T04:17:20.159Z

**tool result**
````
app/backend/trace.py:267:    elif row.get("state") == "needs_review":
app/backend/trace.py:729:                                      "resolution": "needs_review", "review_status": row["review_status"]})
app/backend/trace.py:732:                                      "judge_says": rationale_or(r["reason_code"], v), "resolution": "needs_review", "review_status": row["review_status"]})
app/backend/trace.py:739:                                  "resolution": "needs_review", "review_status": row["review_status"]})
app/backend/trace.py:747:                                      "resolution": "needs_review", "review_status": row["review_status"]})
app/backend/rejudge.py:53:    return ("needs_review" if reasons else "verified"), reasons
app/backend/confidence.py:3:Precedence: rejected > needs_review > verified. Reason codes are a closed list (api.md appendix); an unknown code is a bug.
app/backend/confidence.py:14:STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}
app/backend/confidence.py:24:    """needs_review first, then verified, then rejected."""
app/backend/confidence.py:71:    return ("needs_review", doubts) if doubts else ("verified", [])
app/backend/flags.py:113:    (needs_review). Grounding of model quotes is checked separately (ground()); a tagged record adds INJECTION_SUSPECTED to every flag."""
app/backend/flags.py:180:            "origin": "code", "title": title, "explanation": expl, "review_status": "pending", "state": "needs_review",
app/backend/flags.py:239:    Policy for the answer: conflict -> flag (verified when the other checks hold); unsure / judge failed -> flag stays needs_review;
app/backend/flags.py:291:    A disagreement, unsure answer or failed judge call leaves the flag needs_review (JUDGE_DISAGREES / JUDGE_UNSURE / JUDGE_UNAVAILABLE),
app/backend/present.py:117:    counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
app/backend/present.py:216:                    "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},
app/backend/review.py:6:that cannot answer never blocks: the edit is saved as needs_review with JUDGE_UNAVAILABLE.
app/backend/review.py:206:    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
app/backend/review.py:209:    if state == "needs_review" and not reasons:
app/backend/pipeline.py:36:    """State of a flag made by code: evidence spans must equal the input text; injection / unconfirmed endpoints give needs_review."""
app/backend/pipeline.py:381:                       "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
app/backend/gaps.py:30:    """needs_review reasons: an undated/ambiguous encounter record whose date could fall inside the span (ADR-010), or an injection-tagged endpoint."""
app/backend/present.py:130:def record_view(r, raw, with_sentences=True, pages=None):
app/backend/present.py:136:    if pages:                                    # PDF source (D-031): the page where the record starts
app/backend/present.py:137:        v["page"] = pdf_text.page_for(pages, r["char_start"])
app/backend/present.py:158:            "records": [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs], "undated_entries": undated, "entries": dated,
tests/unit/_pdf.py
tests/unit/test_pdf_upload.py
app/db/db.py:78:def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:22.109Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p app/backend/confidence.py; cat tests/unit/_pdf.py; grep -n \"def test\\|no_text\" tests/unit/test_pdf_upload.py | head -40; sed -n 125,160p app/backend/present.py; sed -n 1,60p app/backend/injection.py | head -60; grep -n \"INJECTION_SUSPECTED\" app/backend/*.py | head"
}
````

### User / tool · 2026-11-02T04:17:22.219Z

**tool result**
````
"""compose_state(ladder, context) -> (state, reasons)  (ADR-005, R-TL-5, LLM_VS_CODE row 17). Pure and deterministic.

Precedence: rejected > needs_review > verified. Reason codes are a closed list (api.md appendix); an unknown code is a bug.
"""
REASON_CODES = (
    "GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE",
    "HIGHLIGHT_NOT_FOUND", "JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE",
    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
    "AMOUNT_ESTIMATE", "AMOUNT_DAMAGES", "AMOUNT_UNCLEAR", "LEXICON_ONLY", "LLM_ONLY", "SPLIT_AMBIGUOUS",
    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT",
)
REJECTED_CODES = frozenset({"GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"})
STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}

_JUDGE = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES",
          "unsure": "JUDGE_UNSURE", "unavailable": "JUDGE_UNAVAILABLE"}
_AMOUNT = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
_AGREE = {"lexicon_only": "LEXICON_ONLY", "llm_only": "LLM_ONLY"}
_DATE = {"ambiguous": "DATE_AMBIGUOUS", "missing": "DATE_MISSING"}


def sort_key(state: str) -> int:
    """needs_review first, then verified, then rejected."""
    return STATE_ORDER[state]


def _known(code: str) -> str:
    if code not in REASON_CODES:
        raise ValueError(f"unknown reason code: {code}")
    return code


def _lookup(table: dict, value, none_ok=()):
    if value is None or value in none_ok:
        return None
    if value not in table:
        raise ValueError(f"unknown value: {value}")
    return table[value]


_LADDER_KEYS = {"grounding_failures", "schema_valid", "code_reasons", "judge"}
_CTX_KEYS = {"injection", "date_status", "amount_class", "agreement", "fixture_miss", "split_ambiguous", "llm_failed",
             "endpoint_unverified", "llm_split"}


def compose_state(ladder: dict, context: dict = None):
    ctx = context or {}
    bad = (set(ladder) - _LADDER_KEYS) | (set(ctx) - _CTX_KEYS)
    if bad:      # a misspelled key must not fail open to 'verified'
        raise ValueError(f"unknown ladder/context keys: {sorted(bad)}")
    rejected, doubts = [], []
    for c in ladder.get("grounding_failures", []) or []:
        rejected.append(_known(c))
    if ladder.get("schema_valid", True) is False:
        rejected.append("SCHEMA_INVALID")
    for c in ladder.get("code_reasons", []) or []:
        (rejected if _known(c) in REJECTED_CODES else doubts).append(c)
    doubts.append(_lookup(_JUDGE, ladder.get("judge"), none_ok=("supported",)))
    doubts.append(_lookup(_DATE, ctx.get("date_status"), none_ok=("parsed", "confirmed")))
    doubts.append(_lookup(_AMOUNT, ctx.get("amount_class"), none_ok=("charge",)))
    doubts.append(_lookup(_AGREE, ctx.get("agreement"), none_ok=("both",)))
    for key, code in (("fixture_miss", "FIXTURE_MISS"), ("split_ambiguous", "SPLIT_AMBIGUOUS"), ("llm_split", "LLM_SPLIT"),
                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
        if ctx.get(key):
            doubts.append(code)
    rejected = list(dict.fromkeys(rejected))
    doubts = list(dict.fromkeys(d for d in doubts if d))
    if rejected:
        return "rejected", rejected + doubts       # the rejecting reasons come first; the item still shows every doubt
    return ("needs_review", doubts) if doubts else ("verified", [])
"""Minimal hand-built text PDFs for tests (no PDF library needed): one page per list entry, one text line per list item."""


def _esc(s: str) -> bytes:
    return s.encode("cp1252").replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def make_pdf(pages: list, image_only: bool = False) -> bytes:
    """pages: [[line, ...], ...]. image_only=True draws a rectangle instead of text (a stand-in for a scan: no text layer)."""
    objs = []
    n = len(pages)
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(n))
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode())
    for i, lines in enumerate(pages):
        page_no, content_no = 3 + 2 * i, 4 + 2 * i
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 2000 800] /Contents {content_no} 0 R "
                    f"/Resources << /Font << /F1 {3 + 2 * n} 0 R >> >> >>".encode())
        if image_only:
            stream = b"0.5 g 50 50 400 300 re f"
        else:
            parts = [b"BT /F1 8 Tf 9 TL 20 780 Td"]
            for ln in lines:
                parts.append(b"(" + _esc(ln) + b") Tj T*")
            parts.append(b"ET")
            stream = b"\n".join(parts)
        objs.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    out, offs = bytearray(b"%PDF-1.4\n"), []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    x = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode() + b"0000000000 65535 f \n"
    for o in offs:
        out += f"{o:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n".encode()
    return bytes(out)


def sample_pdf(raw: str, split_after_record: int = 5) -> bytes:
    """The golden sample as a 2-page text PDF: records up to `split_after_record` on page 1, the rest on page 2."""
    lines = raw.split("\n")
    cut = next(i for i, l in enumerate(lines) if l == f"=== Record {split_after_record + 1} ===")
    return make_pdf([lines[:cut], lines[cut:]])
17:def test_text_pdf_of_the_sample_gives_the_same_nine_records_as_paste():
28:def test_pages_map_records_to_page_numbers():
36:    (make_pdf([["x"]], image_only=True), "pdf_no_text_layer"),
37:    (make_pdf([["   "]]), "pdf_no_text_layer"),
42:def test_unusable_pdfs_are_refused_with_a_reason(data, code):
58:def test_scanned_pdf_upload_is_refused_and_nothing_is_stored_or_called(client, monkeypatch):
65:    assert r.status_code == 400 and r.json()["error"]["detail"]["reason"] == "pdf_no_text_layer"
70:def test_pdf_upload_creates_the_same_case_as_paste_with_pages(client):
81:def test_export_citations_carry_page_numbers_only_for_pdf_sources():
94:def test_demo_mode_refuses_a_pdf_whose_text_is_not_recorded(tmp_path, monkeypatch):
109:def test_demo_mode_refuses_before_any_parsing(tmp_path, monkeypatch):
118:def test_oversize_pdf_is_refused_before_parsing(client, monkeypatch):
125:def test_parsing_does_not_block_the_event_loop(tmp_path, monkeypatch):
150:def test_slow_extraction_hits_the_time_cap(tmp_path, monkeypatch):
187:def test_pypdf_writes_no_record_text_to_stderr_or_logs(capfd, caplog):
213:def test_upload_of_a_damaged_pdf_logs_no_record_text(client, capfd, caplog):
225:def test_requirements_pin_pypdf_exactly():
def dates_to_confirm(conn, case_id):
    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"]}
            for r in _recs_by_id(conn, case_id).values() if r["date_status"] in ("ambiguous", "missing")]


def record_view(r, raw, with_sentences=True, pages=None):
    block = raw[r["char_start"]:r["char_end"]]
    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
         "date_status": r["date_status"], "date_candidates": r["date_candidates"] or [], "duplicate_of": r["duplicate_of"],
         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
         "char_end": r["char_end"], "text": block}
    if pages:                                    # PDF source (D-031): the page where the record starts
        v["page"] = pdf_text.page_for(pages, r["char_start"])
    if with_sentences:
        v["sentences"] = [{"text": block[a:b], "start": r["char_start"] + a, "end": r["char_start"] + b} for a, b in sentences.stripped_spans(block)]
    return v


def case_view(conn, case_id, *, backend, models, demo_mode):
    case = DB.get_case(conn, case_id)
    raw = case["raw_text"]
    recs = list(_recs_by_id(conn, case_id).values())
    its = all_items(conn, case_id)
    ents = its["entry"]
    live_e = [e for e in ents if e["state"] != "rejected"]
    dated = sorted((e for e in live_e if e["date"] and (e["date_status"] in ("parsed", "confirmed", None))), key=lambda e: (e["date"], e["seq"] or 0))
    undated = [e for e in live_e if e not in dated]
    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
             "attempt": {"summary": x.get("summary"), "excerpt": x.get("excerpt")} if k == "entry" else {"text": x.get("text"), "excerpt": x.get("excerpt")},
             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected"]
    err = json.loads(case["error"]) if case.get("error") else None
    injected = [r["id"] for r in recs if r["injection_tag"]]
    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
            "records": [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs], "undated_entries": undated, "entries": dated,
            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "dates_to_confirm": dates_to_confirm(conn, case_id),
"""Advisory scan for instruction-like text in records (lexicon `injection`) and prompt delimiters. D-005, ADR-008.3, row 14.
A hit never strips or edits text; it tags the record. The scan is a floor, not a defence: the real controls are per-record
LLM passes, nonce delimiters and review."""
import re

from app.backend import lexicon


def scan(text: str) -> list:
    """[{id, phrase, start, end}] sorted by start; offsets index into `text`."""
    hits = []
    for e in lexicon.code_list("injection"):
        for m in e["regex"].finditer(text or ""):
            start, end = m.start(), m.end()
            while start < end and text[start] in ".\n \t":   # role_label includes its sentence/line lead-in
                start += 1
            hits.append({"id": e["id"], "phrase": text[start:end], "start": start, "end": end})
    return sorted(hits, key=lambda h: (h["start"], h["end"]))


_LOOKALIKE = re.compile(r"<(\s*/?\s*record-)", re.IGNORECASE)


def wrap(text: str, nonce: str) -> str:
    """Wrap record text in nonce delimiters; any `<record-` / `</record-` lookalike inside the text is neutralised in this prompt copy."""
    safe = _LOOKALIKE.sub(r"&lt;\1", text)
    return f"<record-{nonce}>\n{safe}\n</record-{nonce}>"
app/backend/confidence.py:11:    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT",
app/backend/confidence.py:64:                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
app/backend/flags.py:113:    (needs_review). Grounding of model quotes is checked separately (ground()); a tagged record adds INJECTION_SUSPECTED to every flag."""
app/backend/flags.py:181:            "reasons": ["INJECTION_SUSPECTED"], "why": why.why("INJECTION_SUSPECTED"), "excerpt": hits[0]["phrase"] if hits else "",
app/backend/gaps.py:41:        reasons.append("INJECTION_SUSPECTED")
app/backend/ingest.py:346:        w["reasons"] = {"injection_suspected": ["INJECTION_SUSPECTED"], "llm_split": ["LLM_SPLIT"]}.get(w["category"], [])
app/backend/pipeline.py:93:            warnings.append({"code": "INJECTION_SUSPECTED", "record_no": r["n"], "item_id": r["id"],
app/backend/trace.py:71:    "INJECTION_SUSPECTED": "injection_scan", "LLM_FAILED_AFTER_RETRIES": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
app/backend/trace.py:363:    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
app/backend/trace.py:364:        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED"), reason="INJECTION_SUSPECTED", rule="row 16",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:27.503Z

**tool call — Bash**
````
{
 "command": "git status --short | head -30; grep -n \"compose_state\\|injection\" app/backend/pipeline.py | head -40; grep -n \"INJECTION_SUSPECTED\" app/backend/why.py app/backend/trace.py memory/contracts/api.md | head; grep -rn \"REASON_CODES\" app tests --include=*.py | head"
}
````

### User / tool · 2026-11-02T04:17:27.633Z

**tool result**
````
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/pipeline.py
 M app/backend/review.py
 M app/backend/trace.py
 M app/frontend/api.js
 M app/frontend/export.js
 M app/frontend/judges.js
 M app/frontend/stepper.css
 M app/frontend/stepper.js
 M app/frontend/timeline.js
 M app/llm/audited.py
D  app/llm/prompts/conflicts_v1.md
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
36:    """State of a flag made by code: evidence spans must equal the input text; injection / unconfirmed endpoints give needs_review."""
38:    ctx = {"injection": any(rec_by_n[n].get("injection_tag") for n in nos if n in rec_by_n),
43:    return confidence.compose_state({"grounding_failures": ["GROUNDING_EXCERPT_NOT_VERBATIM"] if bad else [], "schema_valid": True,
75:        inj = w["category"] == "injection_suspected"
76:        ctx = {"llm_split": True} if w["category"] == "llm_split" else {"injection": inj, "date_status": None if inj else "ambiguous"}
77:        state, why_codes = confidence.compose_state({"code_reasons": []}, ctx)
92:        if r["injection_tag"]:
97:            "injection_records": ing["injection_records"]}
104:            "excerpt": r["excerpt"], "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending"}
158:                          date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
215:    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
226:    state, reasons = confidence.compose_state(
229:        {"injection": a["injection"], "amount_class": a["cls"]})
317:        llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
325:            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
367:                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
372:            "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
app/backend/why.py:28:    "INJECTION_SUSPECTED": "This record contains instruction-like text that may be trying to steer the AI; review it before relying on it.",
app/backend/trace.py:71:    "INJECTION_SUSPECTED": "injection_scan", "LLM_FAILED_AFTER_RETRIES": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
app/backend/trace.py:363:    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
app/backend/trace.py:364:        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED"), reason="INJECTION_SUSPECTED", rule="row 16",
app/backend/trace.py:408:    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
app/backend/trace.py:409:        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED") + " An amount from such a record cannot become a charge.",
app/backend/trace.py:410:                       reason="INJECTION_SUSPECTED", rule="row 16", evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid})))
app/backend/trace.py:446:    injected = any(recs.get(r, {}).get("injection_tag") for r in rids) or "INJECTION_SUSPECTED" in R
app/backend/trace.py:450:            return step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED"), reason="INJECTION_SUSPECTED", rule="row 16",
app/backend/trace.py:454:        code = {"injection_suspected": "INJECTION_SUSPECTED", "analysis_incomplete": "CONFLICT_CHECK_INCOMPLETE", "llm_split": "LLM_SPLIT", "date_ambiguous": "DATE_AMBIGUOUS"}.get(cat) \
app/backend/trace.py:39:# Trace-only reason codes (case level and narrative); item reason codes come from confidence.REASON_CODES / why.py.
app/backend/confidence.py:5:REASON_CODES = (
app/backend/confidence.py:29:    if code not in REASON_CODES:
app/backend/schemas.py:22:JUDGE_REASON_CODES = {"j1": _J1_CODES, "j2": _J2_CODES, "j3": _J3_CODES, "j4": _J4_CODES}
tests/unit/test_confidence.py:120:    """Row 18 / api.md appendix: confidence.REASON_CODES equals the closed list (22+ codes)."""
tests/unit/test_confidence.py:121:    assert set(C.REASON_CODES) == api_codes()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:31.959Z

**tool call — Bash**
````
{
 "command": "sed -n 340,385p app/backend/pipeline.py; grep -n \"^def \" app/db/db.py | head -60; sed -n 60,80p app/backend/trace.py; grep -n \"def reason_text\\|def why\" -A8 app/backend/trace.py app/backend/why.py | head -40; sed -n 110,135p tests/unit/test_confidence.py"
}
````

### User / tool · 2026-11-02T04:17:32.068Z

**tool result**
````
        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
        f["ladder"]["item_id"], f["ladder"]["backend"], f["ladder"]["state"] = f["id"], P.backend_name(), f["state"]
        f["ladder"]["code_checks"].setdefault("classified_by", "lexicon+llm")
        f.setdefault("review_status", "pending")
        f["origin"] = _ORIGIN.get(f["origin"], f["origin"])
        f.pop("record_no", None)
    flag_items = ing["flags"] + [_clean(f) for f in llm_flags if f["state"] != "rejected"]
    tray = [_clean(e) for e in rejected] + [_clean(f) for f in llm_flags if f["state"] == "rejected"]
    entries = [_clean(e) for e in entries]
    dated = sorted((e for e in entries if dated_cut(e)), key=lambda e: (e["date"], e["seq"]))
    undated = [e for e in entries if not dated_cut(e)]
    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
    flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
    final_amounts = [_clean(a) for a in final_amounts]
    damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
    now_t = clock()
    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
    _persist(conn, cid, "amount", final_amounts, now_t)
    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
    if timed_out:
        status = "timeout"
        err = {"code": "run_deadline", "message": "The run passed its time limit; finished items were kept."}
    else:
        status = "done_with_errors" if errors else "done"
        err = None
    DB.update_case(conn, cid, status="failed" if timed_out else "ready", stage="finalize", error=json.dumps(err) if err else None,
                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
    tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
    all_items = dated + undated + final_amounts + flag_items
    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
            "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
            "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
                       "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
                       "verified": sum(1 for i in all_items if i["state"] == "verified")}}


# ------------------------------------------------------------------ eval / API view
def case_view(out: dict) -> dict:
    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
    flags = []
    for f in out["flags"] + out["tray"]:
        if "summary" in f:
            continue
28:def init(path: str = ":memory:"):
36:def connect(path: str):
62:def _tok(prefix: str) -> str:
66:def _enc(v):
70:def _cols(conn, table):
74:def sha256(text: str) -> str:
78:def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
86:def update_case(conn, case_id: str, **fields) -> None:
95:def get_case(conn, case_id: str):
100:def _insert(conn, table, row):
108:def add_record(conn, case_id: str, **fields) -> str:
114:def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
127:def _find(conn, item_id, case=None):
144:def _decode(row) -> dict:
155:def get_item(conn, item_id: str, case: str = None) -> dict:
159:def list_items(conn, case_id: str, kind: str) -> list:
164:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
179:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
204:def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
211:def list_events(conn, case_id: str, item_id: str = None) -> list:
218:def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
227:def get_llm_call(conn, call_id: str):
232:def list_llm_calls(conn, case_id: str, item_id: str = None) -> list:
239:def delete_case(conn, case_id: str) -> None:
251:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
258:def table_counts(conn, case_id: str) -> dict:
    "DISMISS_OR_ENTER_BY_HAND": "This item cannot be used. Dismiss it, or write the entry by hand from the record.",
    "RERUN": "Run the AI steps again.",
    "RERUN_JUDGE": "Run the second check again.",
    "SENTENCE_REMOVED": "This sentence was left out of the draft. If you want its facts in the paragraph, check the cited entry's quote and write them yourself.",
    "CONFIRM_RERUN": "Run the AI steps again; confirm that earlier decisions are kept.",
}
_STEP_OF_REASON = {
    "GROUNDING_EXCERPT_NOT_VERBATIM": "excerpt_verbatim", "GROUNDING_AMOUNT_NOT_IN_TEXT": "found_in_text", "SCHEMA_INVALID": "extracted",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "summary_tokens", "SUMMARY_DROPS_QUALIFIER": "summary_qualifier", "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge",
    "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight", "DATE_AMBIGUOUS": "date_confirmed",
    "DATE_MISSING": "date_confirmed", "ENDPOINT_NOT_VERIFIED": "endpoints_confirmed", "LEXICON_ONLY": "agreement", "LLM_ONLY": "agreement",
    "INJECTION_SUSPECTED": "injection_scan", "LLM_FAILED_AFTER_RETRIES": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
    "AMOUNT_ESTIMATE": "amount_class", "AMOUNT_DAMAGES": "amount_class", "AMOUNT_UNCLEAR": "amount_class", "CONFLICT_CHECK_INCOMPLETE": "record_warning_check",
    "SPLIT_AMBIGUOUS": "record_warning_check", "LLM_SPLIT": "record_warning_check"}
_AMOUNT_CODE = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
_CODE_CHECK_REASONS = {"SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND"}


def reason_text(code: str) -> str:
    if code in TRACE_WHY:
        return TRACE_WHY[code]
app/backend/why.py:34:def why(code: str) -> str:
app/backend/why.py-35-    return _WHY[code]
app/backend/why.py-36-
app/backend/why.py-37-
app/backend/why.py-38-def all_codes() -> list:
app/backend/why.py-39-    return list(_WHY)
app/backend/why.py-40-
app/backend/why.py-41-
app/backend/why.py-42-# D-028: judge reason codes (closed lists) -> fixed sentence. Model prose never reaches the UI.
app/backend/trace.py:78:def reason_text(code: str) -> str:
app/backend/trace.py-79-    if code in TRACE_WHY:
app/backend/trace.py-80-        return TRACE_WHY[code]
app/backend/trace.py-81-    try:
app/backend/trace.py-82-        return why.why(code)
app/backend/trace.py-83-    except KeyError:
app/backend/trace.py-84-        return code
app/backend/trace.py-85-
app/backend/trace.py-86-
def api_codes():
    t = (pathlib.Path(__file__).resolve().parents[2] / "memory/contracts/api.md").read_text()
    app = t.split("## Appendix: reason codes")[1]
    codes = set()
    for line in app.splitlines():
        if line.startswith("| `"):
            codes |= set(re.findall(r"`([A-Z][A-Z_]+)`", line.split("|")[1]))
    return codes

def test_reason_codes_match_api_appendix():
    """Row 18 / api.md appendix: confidence.REASON_CODES equals the closed list (22+ codes)."""
    assert set(C.REASON_CODES) == api_codes()
    assert len(api_codes()) >= 22

@pytest.mark.parametrize("code", sorted(api_codes()))
def test_every_reason_code_has_a_why_template(code):
    """Row 18: every reason code has a fixed, non-empty, plain-language template (no braces left over, no model text)."""
    s = W.why(code)
    assert isinstance(s, str) and 15 < len(s) < 300 and "{" not in s and "}" not in s

def test_why_unknown_code_raises():
    """Row 18: unknown code -> KeyError (templates are a closed list)."""
    with pytest.raises(KeyError):
        W.why("NOT_A_CODE")

def test_why_is_deterministic():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:37.799Z

**tool call — Bash**
````
{
 "command": "sed -n 25,50p app/backend/pipeline.py; sed -n 215,240p app/backend/pipeline.py; sed -n 285,340p app/backend/pipeline.py; git diff --stat app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T04:17:37.915Z

**tool result**
````
def _clean(d: dict) -> dict:
    """Drop private '_' keys before an item is stored or returned."""
    return {k: v for k, v in d.items() if not k.startswith("_")}


def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
            "human": {"action": None, "edited_text": None, "at": None}, "state": state}


def _compose_code(rec_by_n: dict, nos: list, reasons: list, evidence: list, case_text: str) -> tuple:
    """State of a flag made by code: evidence spans must equal the input text; injection / unconfirmed endpoints give needs_review."""
    bad = [e for e in evidence if e.get("start") is not None and case_text[e["start"]:e["end"]] != e["text"]]
    ctx = {"injection": any(rec_by_n[n].get("injection_tag") for n in nos if n in rec_by_n),
           "endpoint_unverified": "ENDPOINT_NOT_VERIFIED" in reasons}
    dates = {rec_by_n[n].get("date_status") for n in nos if n in rec_by_n}
    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
        ctx["date_status"] = "ambiguous"
    return confidence.compose_state({"grounding_failures": ["GROUNDING_EXCERPT_NOT_VERBATIM"] if bad else [], "schema_valid": True,
                                     "code_reasons": []}, ctx)


# ------------------------------------------------------------------ stage 0
def run_ingest(raw_text: str, call=None, not_duplicates=(), splitter=None) -> dict:
    """Stage 0. Raises IngestError('bad_request' | 'input_too_large') before anything else. Zero model calls, except the D-031 split
    fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
    return ing


# ------------------------------------------------------------------ stages 4-6 helpers
def _finish_amount(a: dict, ing: dict, judged) -> dict:
    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
    by_n = {r["n"]: r for r in ing["records"]}
    a = dict(a)
    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
    verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
    state, reasons = confidence.compose_state(
        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
        {"injection": a["injection"], "amount_class": a["cls"]})
    a["state"], a["reasons"] = state, reasons
    a["why"] = " ".join(WHY.why(c) for c in reasons) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
    a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
                   "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
                              "verdict": judged["verdict"], "reason_code": judged.get("reason_code")} if judged else None)}
    return a


def _entry_for(entries: list, record_no: int):
    return next((e["id"] for e in entries if f"r{record_no}" in e["record_ids"]), None)

        nonlocal timed_out
        if timed_out or expired():
            timed_out = True
            return False
        set_stage(name)
        return True

    # 1-3: entries
    if guard("extract"):
        entries, rejected, failures = generator.extract_entries(recs, ing["groups"], call=call, case_text=text)
        for f in failures:
            errors.append(_err("LLM_FAILED_AFTER_RETRIES", "extract", f["record_no"], "FIXTURE_MISS" if f["failure"] == "FIXTURE_MISS" else None))
    if guard("verify"):
        pass                                    # grounding, token and qualifier checks ran inside extract_entries (code, same call per record)
    if guard("judge_entries") and entries:
        generator.judge_entries(entries, by_n, call=call, case_text=text)
    for e in entries + rejected:
        e["ladder"]["backend"] = P.backend_name()
        e.pop("_stage", None)
    # 4: amounts (J2 on every dollar amount)
    final_amounts = code_amounts
    if guard("amounts"):
        dollars = [a for a in ing["amounts"]]
        verdicts = judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars],
                                        call=call, case_text=text)
        final_amounts = [_finish_amount(a, ing, verdicts.get(a["id"])) for a in dollars] + [_finish_amount(a, ing, None) for a in ing["damages"]]
    for a in final_amounts:
        a["entry_id"] = _entry_for(entries, a["record_nos"][0])
    # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T-094). No model search, so the candidate set cannot vary.
    llm_flags = []
    distinct = [by_n[g[0]] for g in ing["groups"]]
    if guard("conflicts"):
        llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
    # 6: per-record flags (one call per distinct record) + J4
    if guard("flags"):
        year = _accident_year(recs)

        def one(r):
            if expired():                    # the deadline also applies inside the stage, record by record
                return r, None
            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
            per = list(ex.map(one, distinct))
        for r, fs in per:
            if fs is None or expired():
                timed_out = True
                continue
            fs = [f for f in fs if f["type"] != "record_warning"]          # stage 0 already made the record_warning flag
            for k, f in enumerate(fs, 1):
                f["id"] = f"f_r{r['n']}_{k}"
            llm_flags += FL.judge_flags(fs, call=call, case_text=text)
    # 7: finalize
    set_stage("finalize")
    for f in llm_flags:
        f.setdefault("record_nos", [f["record_no"]])
        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
 app/backend/pipeline.py | 13 +++----------
 1 file changed, 3 insertions(+), 10 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:41.927Z

**tool call — Bash**
````
{
 "command": "grep -n \"char_start\" app/backend/ingest.py | head -5; grep -n \"recs =\\|recs=\" app/backend/pipeline.py | head; grep -n \"record_nos\\|record_ids\" app/backend/pipeline.py | head -20; sed -n 20,35p app/backend/why.py; grep -n \"Appendix: reason codes\" -A12 memory/contracts/api.md | head -40"
}
````

### User / tool · 2026-11-02T04:17:42.049Z

**tool result**
````
139:            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit"))}
326:                                    "evidence": [{"field": "excerpt", "text": line, "start": r["char_start"] + at if at >= 0 else None,
327:                                                  "end": r["char_start"] + at + len(line) if at >= 0 else None}]})
355:    Offsets are absolute in the normalised input when the record carries `text` and `char_start`; otherwise they are None."""
356:    text, base = rec.get("text"), rec.get("char_start")
53:    recs = ing["records"]
272:    text, recs = ing["text"], ing["records"]
59:        nos = f["record_nos"]
64:                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": ev, "record_nos": nos,
65:                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "review_status": "pending",
80:                      "record_nos": [w["record_no"]], "record_ids": [r["id"]], "source_kind": "record", "review_status": "pending",
102:    return {"id": item_id or a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
169:        return {"record_ids_json": it["record_ids"], "seq": it["seq"], "date_iso": it.get("date"), "provider": it["provider"],
173:        return {"record_ids_json": it["record_ids"], "entry_id": it.get("entry_id"), "text": it["text"], "value_cents": it["cents"],
176:    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
177:                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids") if k in it}
239:    return next((e["id"] for e in entries if f"r{record_no}" in e["record_ids"]), None)
312:        a["entry_id"] = _entry_for(entries, a["record_nos"][0])
339:        f.setdefault("record_nos", [f["record_no"]])
340:        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
357:    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
469:    L += ["", "AMOUNTS"] + [f"  {a['text']} ({a['cls']}) record {','.join(str(n) for n in a['record_nos'])} [{a['state']}]" for a in out["amounts"]]
    "AMOUNT_RATE_NOT_TOTALED": "This figure is a rate, not a charge, so it is not added to the total.",
    "AMOUNT_ESTIMATE": "This figure is an estimate, not a billed charge, so it is not added to the total.",
    "AMOUNT_DAMAGES": "This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.",
    "AMOUNT_UNCLEAR": "This figure could not be read or labelled with confidence, so it is not added to the total.",
    "LEXICON_ONLY": "The phrase list found this flag but the AI did not; check that it applies.",
    "LLM_ONLY": "The AI found this flag but the phrase list did not; check that it applies.",
    "SPLIT_AMBIGUOUS": "It is not certain where this record begins and ends in the pasted text.",
    "LLM_SPLIT": "The AI, not the formatting, decided where this record begins and ends in the pasted text; check the boundaries against the paste.",
    "INJECTION_SUSPECTED": "This record contains instruction-like text that may be trying to steer the AI; review it before relying on it.",
    "CONFLICT_CHECK_INCOMPLETE": "The check for conflicts between records did not finish or had no recorded answer, so conflicts between records may be missing.",
    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
}


def why(code: str) -> str:
    return _WHY[code]
582:## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
583-| Code | State | Meaning |
584-|---|---|---|
585-| `GROUNDING_EXCERPT_NOT_VERBATIM` | rejected | model's excerpt is not word for word in the record |
586-| `GROUNDING_AMOUNT_NOT_IN_TEXT` | rejected | model reported an amount the record does not contain |
587-| `SCHEMA_INVALID` | rejected | model output failed schema validation after retries |
588-| `SUMMARY_TOKEN_NOT_IN_EXCERPT` | needs_review | a number, date, dollar figure or left/right/no/not/without in the summary (or an edit) is not in the quote |
589-| `SUMMARY_DROPS_QUALIFIER` | needs_review | the excerpt has a hedge, self-report marker, negation, laterality or "approx." that the summary leaves out (D-022) |
590-| `EXCERPT_OMITS_QUALIFIER` | needs_review | the record has a hedge sentence the excerpt leaves out |
591-| `EXCERPT_NOT_WHOLE_SENTENCE` | needs_review | the excerpt starts or ends mid-sentence |
592-| `HIGHLIGHT_NOT_FOUND` | needs_review | the quote cannot be located in the raw text for highlighting |
593-| `JUDGE_PARTIAL` / `JUDGE_UNSUPPORTED` | needs_review | judge 1 found the summary partly or not supported |
594-| `JUDGE_DISAGREES` / `JUDGE_UNSURE` | needs_review | judge 2, 3 or 4 disagreed or could not decide |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:45.228Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nimport pypdfium2 as p, pypdfium2.raw as r, inspect\nprint(p.version.PYPDFIUM_INFO if hasattr(p,'version') else '')\nprint([n for n in dir(r) if 'TextObj' in n or 'FillColor' in n or 'GetBounds' in n or 'PageObj_Get' in n])\nprint([n for n in dir(p.PdfPageObject) if not n.startswith('_')])\nprint([n for n in dir(p.PdfTextPage) if not n.startswith('_')])\nprint([n for n in dir(p.PdfBitmap) if not n.startswith('_')])\nE\n.venv/bin/pip show pypdfium2 | grep -i -E \"license|requires\""
}
````

### User / tool · 2026-11-02T04:17:45.941Z

**tool result**
````
5.14.0
['FPDFPageObj_CreateTextObj', 'FPDFPageObj_GetBounds', 'FPDFPageObj_GetClipPath', 'FPDFPageObj_GetDashArray', 'FPDFPageObj_GetDashCount', 'FPDFPageObj_GetDashPhase', 'FPDFPageObj_GetFillColor', 'FPDFPageObj_GetIsActive', 'FPDFPageObj_GetLineCap', 'FPDFPageObj_GetLineJoin', 'FPDFPageObj_GetMark', 'FPDFPageObj_GetMarkedContentID', 'FPDFPageObj_GetMatrix', 'FPDFPageObj_GetRenderedFillPattern', 'FPDFPageObj_GetRenderedStrokePattern', 'FPDFPageObj_GetRotatedBounds', 'FPDFPageObj_GetStrokeColor', 'FPDFPageObj_GetStrokeWidth', 'FPDFPageObj_GetType', 'FPDFPageObj_NewTextObj', 'FPDFPageObj_SetFillColor', 'FPDFTextObj_GetFont', 'FPDFTextObj_GetFontSize', 'FPDFTextObj_GetRenderedBitmap', 'FPDFTextObj_GetText', 'FPDFTextObj_GetTextRenderMode', 'FPDFTextObj_SetFontSize', 'FPDFTextObj_SetTextRenderMode', 'FPDFText_GetFillColor', 'FPDFText_GetTextObject']
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
AttributeError: module 'pypdfium2' has no attribute 'PdfPageObject'. Did you mean: 'PdfObject'?
License: BSD-3-Clause, Apache-2.0, dependency licenses
Requires:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:47.930Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nimport pypdfium2 as p, pypdfium2.raw as r, inspect\nprint([n for n in dir(p.PdfObject) if not n.startswith('_')])\nprint([n for n in dir(p.PdfTextPage) if not n.startswith('_')])\nprint([n for n in dir(p.PdfBitmap) if not n.startswith('_')])\nprint(inspect.signature(p.PdfPage.render))\nprint([n for n in dir(p.PdfPage) if not n.startswith('_')])\nE"
}
````

### User / tool · 2026-11-02T04:17:48.074Z

**tool result**
````
['close', 'get_bounds', 'get_matrix', 'get_quad_points', 'parent', 'set_matrix', 'transform']
['close', 'count_chars', 'count_rects', 'get_charbox', 'get_index', 'get_rect', 'get_text_bounded', 'get_text_range', 'get_textobj', 'parent', 'search']
['close', 'fill_rect', 'from_pil', 'from_raw', 'get_posconv', 'new_foreign', 'new_foreign_simple', 'new_native', 'parent', 'to_numpy', 'to_pil']
(self, scale=1, rotation=0, crop=(0, 0, 0, 0), may_draw_forms=True, bitmap_maker=<bound method PdfBitmap.new_native of <class 'pypdfium2._helpers.bitmap.PdfBitmap'>>, color_scheme=None, fill_to_stroke=False, **kwargs)
['close', 'flatten', 'gen_content', 'get_artbox', 'get_bbox', 'get_bleedbox', 'get_cropbox', 'get_height', 'get_mediabox', 'get_objects', 'get_rotation', 'get_size', 'get_textpage', 'get_trimbox', 'get_width', 'insert_obj', 'parent', 'remove_obj', 'render', 'set_artbox', 'set_bleedbox', 'set_cropbox', 'set_mediabox', 'set_rotation', 'set_trimbox']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:59.881Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/scratch && cd /Users/arsis/zlayt-pm-project && cat > /private/tmp/claude-501/scratch/proto.py <<'E'\nimport ctypes, sys\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nimport pypdfium2 as pdfium, pypdfium2.raw as raw\ndef build(content: bytes, mediabox=\"0 0 600 800\"):\n    objs = [b\"<< /Type /Catalog /Pages 2 0 R >>\", b\"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\",\n      f\"<< /Type /Page /Parent 2 0 R /MediaBox [{mediabox}] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\".encode(),\n      b\"<< /Length %d >>\\nstream\\n\" % len(content) + content + b\"\\nendstream\",\n      b\"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\"]\n    out = bytearray(b\"%PDF-1.4\\n\"); offs=[]\n    for i,o in enumerate(objs,1):\n        offs.append(len(out)); out += f\"{i} 0 obj\\n\".encode()+o+b\"\\nendobj\\n\"\n    x=len(out); out += f\"xref\\n0 {len(objs)+1}\\n\".encode()+b\"0000000000 65535 f \\n\"\n    for o in offs: out += f\"{o:010d} 00000 n \\n\".encode()\n    out += f\"trailer\\n<< /Size {len(objs)+1} /Root 1 0 R >>\\nstartxref\\n{x}\\n%%EOF\\n\".encode()\n    return bytes(out)\nc = b\"\"\"BT /F1 12 Tf 50 700 Td (Visible clinic note) Tj ET\nBT /F1 12 Tf 1 1 1 rg 50 650 Td (White hidden text) Tj ET\nBT /F1 12 Tf 0 g 900 650 Td (Offpage text) Tj ET\nBT /F1 1 Tf 0 g 50 600 Td (Tiny text) Tj ET\nBT /F1 12 Tf 3 Tr 0 g 50 550 Td (Invisible mode) Tj ET\n1 1 1 rg 40 490 300 40 re f\nBT /F1 12 Tf 0 g 50 500 Td (Covered by white box) Tj ET\n\"\"\"\npdf = pdfium.PdfDocument(build(c))\npage = pdf[0]\ntp = page.get_textpage()\nprint(page.get_mediabox(), page.get_size())\nfor o in page.get_objects(filter=[raw.FPDF_PAGEOBJ_TEXT]):\n    n = raw.FPDFTextObj_GetText(o.raw, tp.raw, None, 0)\n    buf = ctypes.create_string_buffer(n*2+2)\n    raw.FPDFTextObj_GetText(o.raw, tp.raw, ctypes.cast(buf, ctypes.POINTER(raw.FPDF_WCHAR)), n+1)\n    txt = buf.raw.decode(\"utf-16-le\").rstrip(\"\\x00\")\n    r_,g_,b_,a_ = [ctypes.c_uint() for _ in range(4)]\n    raw.FPDFPageObj_GetFillColor(o.raw, r_,g_,b_,a_)\n    print(repr(txt), o.get_bounds(), raw.FPDFTextObj_GetTextRenderMode(o.raw), (r_.value,g_.value,b_.value,a_.value))\n    fs = ctypes.c_float(); raw.FPDFTextObj_GetFontSize(o.raw, fs); print(fs.value)\nbm = page.render(scale=1)\nprint(bm.width, bm.height, bm.format, bm.stride, bm.n_channels)\nE\n.venv/bin/python /private/tmp/claude-501/scratch/proto.py"
}
````

### User / tool · 2026-11-02T04:18:00.179Z

**tool result**
````
(0.0, 0.0, 600.0, 800.0) (600.0, 800.0)
'Visible clinic note' (50.04800033569336, 699.8679809570312, 141.53598022460938, 708.5919799804688) 0 (0, 0, 0, 255)
12.0
'White hidden text ' (50.14400100708008, 649.8679809570312, 142.62799072265625, 658.5919799804688) 0 (255, 255, 255, 255)
12.0
'Offpage text' (900.5759887695312, 647.4920043945312, 965.2919921875, 658.7479858398438) 0 (0, 0, 0, 255)
12.0
'Tiny text' (50.02299880981445, 599.791015625, 53.77199935913086, 600.7160034179688) 0 (0, 0, 0, 255)
1.0
'Invisible mode' (51.11600112915039, 549.8679809570312, 126.20000457763672, 558.5919799804688) 3 (0, 0, 0, 255)
12.0
'Covered by white box' (50.599998474121094, 497.49200439453125, 165.29598999023438, 508.7359924316406) 3 (0, 0, 0, 255)
12.0
600 800 2 1800 3
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:29.470Z

**tool call — Bash**
````
{
 "command": "ls app/db; grep -n \"CREATE TABLE\" -A3 app/db/schema.sql | head -60; sed -n 78,100p app/db/db.py; grep -n \"tokens\\|def conn\\|DATA\\|data_dir\\|db_path\" app/backend/store.py | head"
}
````

### User / tool · 2026-11-02T04:18:29.578Z

**tool result**
````
__init__.py
__pycache__
db.py
schema.sql
4:CREATE TABLE IF NOT EXISTS cases (
5-  id TEXT PRIMARY KEY, name TEXT, source TEXT CHECK (source IN ('paste','sample')) DEFAULT 'paste',
6-  raw_text TEXT NOT NULL, text_sha256 TEXT,
7-  status TEXT NOT NULL DEFAULT 'ingested' CHECK (status IN ('ingested','running','ready','failed')),
--
11:CREATE TABLE IF NOT EXISTS records (
12-  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), seq INTEGER, char_start INTEGER, char_end INTEGER,
13-  date_header_start INTEGER, date_header_end INTEGER, source_header_start INTEGER, source_header_end INTEGER,
14-  source_label TEXT, date_raw TEXT, date_iso TEXT,
--
19:CREATE TABLE IF NOT EXISTS entries (
20-  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, seq INTEGER, date_iso TEXT,
21-  provider TEXT, summary TEXT, excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER,
22-  state TEXT, state_reasons_json TEXT,
--
27:CREATE TABLE IF NOT EXISTS amounts (
28-  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, entry_id TEXT,
29-  text TEXT, value_cents INTEGER, kind TEXT CHECK (kind IN ('charge','rate','estimate','damages','unclear')),
30-  excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER, duplicate_note TEXT,
--
36:CREATE TABLE IF NOT EXISTS flags (
37-  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id),
38-  type TEXT CHECK (type IN ('gap','conflict','pre_existing','causation','record_warning')),
39-  category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),
--
48:CREATE TABLE IF NOT EXISTS llm_calls (
49-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
50-  role TEXT CHECK (role IN ('generator','judge')), step TEXT, backend TEXT, model TEXT,
51-  prompt_version TEXT, prompt_sha256 TEXT, system_text TEXT, user_text TEXT, response_raw TEXT,
--
55:CREATE TABLE IF NOT EXISTS review_events (
56-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
57-  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry')),
58-  before_json TEXT, after_json TEXT, at REAL
def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
    cid = fields.pop("id", None) or secrets.token_urlsafe(16)
    row = {"id": cid, "name": name, "source": source, "raw_text": raw_text, "text_sha256": sha256(raw_text),
           "created_at": now, **fields}
    _insert(conn, "cases", row)
    return cid


def update_case(conn, case_id: str, **fields) -> None:
    ok = _cols(conn, "cases") - {"id", "created_at", "raw_text"}
    bad = set(fields) - ok
    if bad:
        raise ValueError(f"unknown case fields {sorted(bad)}")
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE cases SET {sets} WHERE id=?", [_enc(v) for v in fields.values()] + [case_id])


def get_case(conn, case_id: str):
    r = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
    return _decode(r) if r else None


def _insert(conn, table, row):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:32.635Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p app/backend/export_routes.py; grep -n \"export_routes\" app/backend/api.py; sed -n 144,155p app/db/db.py; sed -n 236,252p app/db/db.py; git log --oneline | head -5"
}
````

### User / tool · 2026-11-02T04:18:32.755Z

**tool result**
````
"""GET /api/cases/{token}/export: thin router around export.build_export (T-041). Code only.

The app factory (T-040) does `app.include_router(export_routes.router)` and registers the case loader once:
    export_routes.set_case_loader(fn)   # fn(token) -> case dict (see export.py docstring) or None for an unknown token
Items with review_status other than accepted/edited never reach either block (ADR-009, LLM_VS_CODE row 19).
"""
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.backend import export

router = APIRouter()
_loader = None


def set_case_loader(fn):
    global _loader
    _loader = fn


def _not_found():
    return JSONResponse(status_code=404, content={"error": {"code": "not_found", "message": "No case with that link.", "detail": {}}})


def export_payload(token: str, case: dict, now: datetime = None) -> dict:
    if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
        raise export.ExportBlocked(case["export_blockers"])
    out = export.build_export(case)
    now = now or datetime.now(timezone.utc)
    ok = ("accepted", "edited")
    return {
        "token": token,
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "letter_text": out["letter_text"],
        "internal_notes_text": out["internal_notes_text"],
        "counts": out["counts"],
        "items": {
            "entries": [{"id": e["id"], "record_ids": e.get("record_ids") or [f"r{e['record_no']}"],
500:        from app.backend import export_routes as XR
def _decode(row) -> dict:
    out = {}
    for k in row.keys():
        v = row[k]
        if k.endswith("_json"):
            out[k[:-5]] = json.loads(v) if v else None
        else:
            out[k] = v
    return out


def get_item(conn, item_id: str, case: str = None) -> dict:
    return [_decode(r) for r in conn.execute(q + " ORDER BY created_at, rowid", a)]


def delete_case(conn, case_id: str) -> None:
    """The one deletion path (ADR-006): every table, prompts included. DELETE endpoint and purge both call this."""
    conn.execute("BEGIN")
    try:
        for t in _CASE_TABLES:
            conn.execute(f"DELETE FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
    ids = [r["id"] for r in conn.execute("SELECT id FROM cases WHERE created_at < ?", (now - retention_seconds,))]
ea259cd docs: D-046 ship-bar item 4 gates on J3/J4 seeded controls
e491cad feat(evals): determinism signature covers every R-CO-7 field, per-run artifacts, J3/J4 seeded controls (T-093)
10d358e fix(backend): export gate ready equals export allowed; pending items warn, not block (D-045)
8d7548d fix(research): denylist covers every cited author surname; self-test extracts and checks them (T-077 r3)
f49c4c2 docs: D-045 scope of the judge export gate
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:20.174Z

**tool call — Bash**
````
{
 "command": "sed -n 30,70p app/backend/rejudge.py; sed -n 196,225p app/backend/review.py; grep -n \"_STEP_OF_REASON\" app/backend/trace.py"
}
````

### User / tool · 2026-11-02T04:19:20.265Z

**tool result**
````
                                  nonce=None if edited else nonce, item_id=item)           # an edit's judge ran without a case nonce (review._check_summary)
    if kind == "amount":
        return judges.run_j2_meta(row["excerpt"], row["text"], row["kind"], call=call, nonce=nonce, item_id=item)
    if jid == "j3":
        if not (comp.get("excerpt") and comp.get("excerpt_b")):
            return _UNAVAILABLE
        return judges.run_j3_meta(comp["excerpt"], comp["excerpt_b"], call=call, nonce=nonce, item_id=item, category=row["category"])
    if not comp.get("excerpt"):
        return _UNAVAILABLE
    return judges.run_j4_meta(comp["excerpt"], row["type"], row["category"], call=call, nonce=nonce, item_id=item)


def _safe_ask(t, case_text, call):
    try:
        return _ask(t["kind"], t["judge"], t["row"], case_text, call)
    except (P.FixtureMissing, AU.LLMFailed):
        return _UNAVAILABLE


def recompose(row: dict, ladder_verdict: str):
    """(state, reasons): the item's other doubts stay; its judge doubts are replaced by what the new answer says. Rejected items never get here."""
    keep = [c for c in (row.get("state_reasons") or []) if c not in _JUDGE_REASONS]
    reasons = keep + confidence.compose_state({"judge": ladder_verdict})[1]
    return ("needs_review" if reasons else "verified"), reasons


def rejudge(conn, case_id: str, call, now: float = None) -> dict:
    t = time.time() if now is None else now
    case = DB.get_case(conn, case_id)
    case_text = (case["raw_text"] or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    targets = trace.unjudged_items(conn, case_id)
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        answers = list(ex.map(lambda x: _safe_ask(x, case_text, call), targets))
    done, still = [], []
    for tg, (verdict, call_id, code) in zip(targets, answers):
        row, jid = tg["row"], tg["judge"]
        lad = dict(row.get("ladder") or {"item_id": row["id"]})
        ladder_verdict = judges.to_ladder(jid, verdict)
        attempt = {"at": t, "call_id": call_id, "verdict": ladder_verdict}
        lad["rejudge"] = list(lad.get("rejudge") or []) + [attempt]
        base = {"item_id": row["id"], "kind": tg["kind"], "judge": jid, "review_status": row["review_status"]}
    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t)
    from app.backend import present
    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
            "removed_flag_ids": removed, "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}


def _without_date_doubt(item: dict) -> dict:
    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
    state = item["state"]
    if state == "needs_review" and not reasons:
        state = "verified"
    out = {"state": state, "state_reasons_json": reasons}
    if isinstance(item.get("ladder"), dict):
        out["ladder"] = {**item["ladder"], "state": state}
    return out


def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t):
    after = {"date_chosen": date_iso, "date_raw": rec["date_raw"], "candidates": rec["date_candidates"], "record_id": rec["id"],
             "cleared_date_ambiguous": cleared}
    before = {"date_status": "ambiguous", "date_iso": rec.get("date_iso")}
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                 (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))


def _drop(conn, case_id, flag_id):
66:_STEP_OF_REASON = {
278:        return _STEP_OF_REASON.get(c) if _STEP_OF_REASON.get(c) in ids else fallback
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:28.004Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/pdf_text.py\"\ns=open(p).read()\ns=s.replace('''class PdfError(ValueError):\n    \"\"\"str(e) is the API error code: pdf_no_text_layer | pdf_unreadable | pdf_too_large | pdf_encrypted.\"\"\"\n\n    @property''','''class PdfError(ValueError):\n    \"\"\"str(e) is the API error code: pdf_no_text_layer | pdf_unreadable | pdf_too_large | pdf_encrypted (pdf_checks adds the OCR codes).\n    `detail` is extra, record-free context for the API error body (T-086/T-087).\"\"\"\n\n    def __init__(self, code, detail=None):\n        super().__init__(code)\n        self.detail = detail or {}\n\n    @property''')\ns=s.replace('''def extract(data: bytes) -> dict:\n    \"\"\"{text, pages: [{page, start, end}]}. Page texts are stripped and joined with a blank line, so offsets index the text exactly.\"\"\"\n    if len(data''','''def read_pages(data: bytes) -> list:\n    \"\"\"The stripped text-layer string of every page (may be empty). Validates size, header, encryption and page count.\"\"\"\n    if len(data''')\ns=s.replace('''    if sum(len(\"\".join(t.split())) for t in texts) < MIN_TEXT_CHARS:\n        raise PdfError(\"pdf_no_text_layer\")\n    text, pages = \"\", []\n    for i, t in enumerate(texts, 1):\n        if not t:\n            continue\n        if text:\n            text += \"\\\\n\\\\n\"\n        pages.append({\"page\": i, \"start\": len(text), \"end\": len(text) + len(t)})\n        text += t\n    return {\"text\": text, \"pages\": pages}\n''','''    return texts\n\n\ndef assemble(texts: list, sources: dict = None) -> dict:\n    \"\"\"{text, pages: [{page, start, end}]}. Page texts are stripped and joined with a blank line, so offsets index the text exactly.\n    `sources` maps a page number to extra keys for that page's entry (for example {\"source\": \"ocr\"}); empty pages are left out.\"\"\"\n    text, pages = \"\", []\n    for i, t in enumerate(texts, 1):\n        if not t:\n            continue\n        if text:\n            text += \"\\\\n\\\\n\"\n        pages.append({\"page\": i, \"start\": len(text), \"end\": len(text) + len(t), **(sources or {}).get(i, {})})\n        text += t\n    return {\"text\": text, \"pages\": pages}\n\n\ndef extract(data: bytes) -> dict:\n    \"\"\"{text, pages: [{page, start, end}]} from the text layer alone; a file with no usable text layer is refused.\"\"\"\n    texts = read_pages(data)\n    if sum(len(\"\".join(t.split())) for t in texts) < MIN_TEXT_CHARS:\n        raise PdfError(\"pdf_no_text_layer\")\n    return assemble(texts)\n''')\nopen(p,\"w\").write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_pdf_upload.py 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T04:19:29.152Z

**tool result**
````
ERROR tests/unit/test_pdf_upload.py::test_oversize_pdf_is_refused_before_parsing
ERROR tests/unit/test_pdf_upload.py::test_upload_of_a_damaged_pdf_logs_no_record_text
4 failed, 10 passed, 4 errors in 0.72s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:30.725Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_pdf_upload.py 2>&1 | grep -E \"Error|error|FAIL\" | head -12; git stash list | head -2"
}
````

### User / tool · 2026-11-02T04:19:30.780Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: subagents may not run git stash (it rewinds shared board/memory files of other agents)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:32.349Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_pdf_upload.py 2>&1 | grep -E \"^E \" | sort | uniq -c | head"
}
````

### User / tool · 2026-11-02T04:19:35.390Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:36.830Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_pdf_upload.py -x 2>&1 | tail -25"
}
````

### User / tool · 2026-11-02T04:19:40.034Z

**tool result**
````
..................                                                       [100%]
18 passed in 2.76s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:20:05.901Z

**tool call — Write**
````
{
 "path": "/Users/arsis/zlayt-pm-project/app/backend/pdf_hidden.py",
 "content": "\"\"\"Hidden-text detection for PDFs (T-087, D-042). Deterministic code, local only (pypdfium2 = PDFium, no network).\n\nA PDF can carry text in its text layer that a reader never sees on the rendered page: white or background-coloured text, text drawn\noff the page, text in a tiny font, text in the invisible render mode, text covered by a filled box. A paralegal copying from the\nrendered page would never quote it, but the extractor reads it. Here every text object is checked against the page *as rendered*:\n\n    invisible_render_mode  PDF text render mode 3 (neither filled nor stroked; this is how a hidden OCR layer is stored)\n    transparent            fill opacity 0\n    off_page               less than half of the text's box lies on the page\n    tiny_font              effective font size under TINY_PT points\n    blends_with_background the rendered pixels under the text's box are uniform (white on white, same colour as the fill, covered\n                           by a shape): the text cannot be told apart from its background\n\nHidden text is reported per page and removed from the case text until the paralegal confirms it, so it can never ground a quote.\nLimits (stated, not hidden): text that overlaps visible text of the same colour is judged visible; text hidden by a clip path alone\nis not detected; a rotated or skewed text box is checked by its bounding box.\"\"\"\nimport ctypes\nimport re\n\nTINY_PT = 3.0               # effective font size below this is not legible on any rendering\nSCALE = 2.0                 # render scale for the pixel check (144 dpi on a 72-pt page)\nMAX_SIDE_PX = 3200          # cap for oversized MediaBoxes\nFLAT_SPREAD = 48            # max-min of any colour channel under the text box below this = text not distinguishable from its background\nMAX_ITEMS_PER_PAGE = 50     # items listed per page in the report (the page still counts them all)\nTEXT_CAP = 300              # characters of a hidden string kept in the report\n\nREASON_PLAIN = {\n    \"invisible_render_mode\": \"drawn in the PDF's invisible text mode\",\n    \"transparent\": \"fully transparent\",\n    \"off_page\": \"placed outside the page\",\n    \"tiny_font\": \"set in a font too small to read\",\n    \"blends_with_background\": \"the same colour as the page behind it (not visible when the page is shown)\",\n}\n\n\nclass HiddenScanUnavailable(RuntimeError):\n    \"\"\"The renderer could not read the file; hidden text could not be checked (the caller reports the check as skipped).\"\"\"\n\n\ndef _text_of(raw, obj, textpage) -> str:\n    n = raw.FPDFTextObj_GetText(obj, textpage, None, 0)\n    if n <= 0:\n        return \"\"\n    buf = ctypes.create_string_buffer(n * 2 + 4)\n    raw.FPDFTextObj_GetText(obj, textpage, ctypes.cast(buf, ctypes.POINTER(raw.FPDF_WCHAR)), n + 1)\n    return buf.raw.decode(\"utf-16-le\", \"replace\").split(\"\\x00\", 1)[0]\n\n\ndef _effective_size(raw, obj) -> float:\n    size = ctypes.c_float(0)\n    raw.FPDFTextObj_GetFontSize(obj, size)\n    m = raw.FS_MATRIX()\n    if raw.FPDFPageObj_GetMatrix(obj, m):\n        scale = (abs(m.a * m.d - m.b * m.c)) ** 0.5\n        if scale > 0:\n            return size.value * scale\n    return size.value\n\n\ndef _rendered_rows(bitmap):\n    \"\"\"(buffer, stride, width, height, bytes_per_pixel) of the rendered page.\"\"\"\n    return bitmap.buffer, bitmap.stride, bitmap.width, bitmap.height, bitmap.n_channels\n\n\ndef _spread(bm, posconv, bbox) -> int:\n    \"\"\"Largest max-min of any colour channel over the rendered pixels under `bbox` (page coordinates). 255 when it cannot be sampled.\"\"\"\n    buf, stride, w, h, ch = bm\n    x0, y0, x1, y1 = bbox\n    pts = [posconv.to_bitmap(x, y) for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]\n    px0, px1 = int(min(p[0] for p in pts)) - 1, int(max(p[0] for p in pts)) + 2\n    py0, py1 = int(min(p[1] for p in pts)) - 1, int(max(p[1] for p in pts)) + 2\n    px0, px1, py0, py1 = max(px0, 0), min(px1, w), max(py0, 0), min(py1, h)\n    if px1 - px0 < 1 or py1 - py0 < 1:\n        return 255\n    worst = 0\n    for c in range(min(ch, 3)):\n        lo, hi = 255, 0\n        for y in range(py0, py1):\n            row = bytes(buf[y * stride + px0 * ch: y * stride + px1 * ch])[c::ch]\n            if row:\n                lo, hi = min(lo, min(row)), max(hi, max(row))\n        worst = max(worst, hi - lo)\n    return worst\n\n\ndef _page_scan(raw, pdfium, page) -> dict:\n    page_box = page.get_cropbox() or page.get_mediabox()\n    pw, ph = page.get_size()\n    scale = min(SCALE, MAX_SIDE_PX / max(pw, ph, 1))\n    bitmap = page.render(scale=scale)\n    bm = _rendered_rows(bitmap)\n    posconv = bitmap.get_posconv(page)\n    textpage = page.get_textpage()\n    visible, hidden, has_image, n_text = [], [], False, 0\n    try:\n        for obj in page.get_objects(filter=[raw.FPDF_PAGEOBJ_TEXT, raw.FPDF_PAGEOBJ_IMAGE]):\n            if obj.type == raw.FPDF_PAGEOBJ_IMAGE:\n                has_image = True\n                continue\n            text = _text_of(raw, obj.raw, textpage).strip()\n            if not \"\".join(text.split()):\n                continue\n            n_text += 1\n            bbox = obj.get_bounds()\n            reasons = []\n            if raw.FPDFTextObj_GetTextRenderMode(obj.raw) == 3:\n                reasons.append(\"invisible_render_mode\")\n            r, g, b, a = (ctypes.c_uint() for _ in range(4))\n            if raw.FPDFPageObj_GetFillColor(obj.raw, r, g, b, a) and a.value == 0:\n                reasons.append(\"transparent\")\n            if bbox:\n                bx0, by0, bx1, by1 = bbox\n                area = max((bx1 - bx0) * (by1 - by0), 1e-6)\n                ix = max(0.0, min(bx1, page_box[2]) - max(bx0, page_box[0]))\n                iy = max(0.0, min(by1, page_box[3]) - max(by0, page_box[1]))\n                if (ix * iy) / area < 0.5:\n                    reasons.append(\"off_page\")\n            if _effective_size(raw, obj.raw) < TINY_PT:\n                reasons.append(\"tiny_font\")\n            if bbox and \"off_page\" not in reasons and \"blends_with_background\" not in reasons and not reasons:\n                if _spread(bm, posconv, bbox) < FLAT_SPREAD:\n                    reasons.append(\"blends_with_background\")\n            elif bbox and reasons and \"off_page\" not in reasons and \"invisible_render_mode\" not in reasons:\n                if _spread(bm, posconv, bbox) < FLAT_SPREAD:\n                    reasons.append(\"blends_with_background\")\n            (hidden if reasons else visible).append({\"text\": text, \"reasons\": reasons, \"bbox\": [round(v, 1) for v in bbox] if bbox else None})\n    finally:\n        textpage.close()\n        bitmap.close()\n    return {\"hidden\": hidden, \"visible_text\": \"\\n\".join(v[\"text\"] for v in visible), \"has_image\": has_image, \"text_objects\": n_text}\n\n\ndef scan(data: bytes) -> dict:\n    \"\"\"{\"checked\": True, \"pages\": {n: {hidden: [{text, reasons, bbox}], visible_text, has_image, text_objects}}}.\n    Raises HiddenScanUnavailable when PDFium cannot open the file.\"\"\"\n    try:\n        import pypdfium2 as pdfium\n        import pypdfium2.raw as raw\n    except ImportError as e:        # pragma: no cover - the dependency is pinned in requirements.txt\n        raise HiddenScanUnavailable(\"pypdfium2 is not installed\") from e\n    out = {}\n    try:\n        pdf = pdfium.PdfDocument(data)\n        try:\n            for i in range(len(pdf)):\n                page = pdf[i]\n                try:\n                    out[i + 1] = _page_scan(raw, pdfium, page)\n                finally:\n                    page.close()\n        finally:\n            pdf.close()\n    except HiddenScanUnavailable:\n        raise\n    except Exception as e:           # PDFium raises PdfiumError / ValueError / OSError on files it cannot read\n        raise HiddenScanUnavailable(type(e).__name__) from None\n    return {\"checked\": True, \"pages\": out}\n\n\ndef remove_from_text(page_text: str, hidden: list, visible_text: str) -> str:\n    \"\"\"The page's extracted text without the hidden strings. Each hidden string is removed once, matched ignoring whitespace; if any\n    cannot be found in the extractor's text (the two libraries read the page differently), the page text is rebuilt from the visible\n    text objects alone, so hidden text can never be left in by accident.\"\"\"\n    text = page_text\n    for h in hidden:\n        chars = [re.escape(c) for c in h[\"text\"] if not c.isspace()]\n        if not chars:\n            continue\n        m = re.search(r\"\\s*\".join(chars), text)\n        if not m:\n            return visible_text.strip()\n        a, b = m.start(), m.end()\n        line_start = a == 0 or text[a - 1] == \"\\n\"\n        line_end = b >= len(text) or text[b] == \"\\n\"\n        if line_start and line_end and b < len(text):\n            b += 1                     # the hidden string was a whole line: take its line break too\n        text = text[:a] + text[b:]\n    return text.strip()\n\n\ndef report(scanned: dict, confirmed: set) -> dict:\n    \"\"\"The per-page report stored with the case and returned to the UI. `confirmed` = page numbers whose hidden text the paralegal\n    chose to include.\"\"\"\n    pages = []\n    for n, p in sorted(scanned[\"pages\"].items()):\n        if not p[\"hidden\"]:\n            continue\n        items = [{\"text\": h[\"text\"][:TEXT_CAP], \"truncated\": len(h[\"text\"]) > TEXT_CAP, \"reasons\": h[\"reasons\"],\n                  \"why\": \", \".join(REASON_PLAIN[r] for r in h[\"reasons\"])} for h in p[\"hidden\"][:MAX_ITEMS_PER_PAGE]]\n        pages.append({\"page\": n, \"count\": len(p[\"hidden\"]), \"items\": items, \"confirmed\": n in confirmed,\n                      \"excluded\": n not in confirmed})\n    return {\"checked\": True, \"pages\": pages, \"excluded_until_confirmed\": True}\n"
}
````

### User / tool · 2026-11-02T04:20:05.955Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/app/backend/pdf_hidden.py (file state is current in your context — no need to Read it back)

Note: Write's parameters are named `file_path` and `content`. `path` was read as `file_path`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:20:13.896Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/pdf_hidden.py\"\ns=open(p).read()\na=s.index('            if bbox and \"off_page\" not in reasons and \"blends')\nb=s.index('            (hidden if reasons')\ns=s[:a]+'''            if bbox and \"off_page\" not in reasons and \"invisible_render_mode\" not in reasons and _spread(bm, posconv, bbox) < FLAT_SPREAD:\n                reasons.append(\"blends_with_background\")\n'''+s[b:]\nopen(p,\"w\").write(s)\nE\ncat > /private/tmp/claude-501/scratch/proto2.py <<'E'\nimport sys; sys.path.insert(0,\"/Users/arsis/zlayt-pm-project\"); sys.path.insert(0,\"/private/tmp/claude-501/scratch\")\nfrom proto import build\nfrom app.backend import pdf_hidden\nc = b\"\"\"0 Tr\nBT /F1 12 Tf 0 g 50 700 Td (Visible clinic note) Tj ET\nBT /F1 12 Tf 1 1 1 rg 50 650 Td (White hidden text) Tj ET\nBT /F1 12 Tf 0 g 900 650 Td (Offpage text) Tj ET\nBT /F1 1 Tf 0 g 50 600 Td (Tiny text) Tj ET\nq 0.1 0 0 0.1 0 0 cm BT /F1 20 Tf 0 g 500 5400 Td (scaled tiny two pt) Tj ET Q\nq 0.1 0 0 0.1 0 0 cm BT /F1 120 Tf 0 g 500 5000 Td (scaled normal 12pt) Tj ET Q\nBT /F1 12 Tf 3 Tr 0 g 50 550 Td (Invisible mode) Tj ET\n0 Tr\n1 1 1 rg 40 490 300 40 re f\nBT /F1 12 Tf 0 g 50 500 Td (Covered by white box) Tj ET\n0.9 g\nBT /F1 12 Tf 0.95 g 50 450 Td (nearly white) Tj ET\nBT /F1 12 Tf 0 g 50 400 Td (...) Tj ET\n\"\"\"\nimport proto\nEOF=1\nE\nsed -i 's/^pdf = pdfium.PdfDocument(build(c))/if __name__ != \"__main__\": raise SystemExit\\npdf = pdfium.PdfDocument(build(c))/' /private/tmp/claude-501/scratch/proto.py\npython3 - <<'E'\n# make proto importable w/o side effects: only keep build()\ns=open(\"/private/tmp/claude-501/scratch/proto.py\").read()\ni=s.index(\"c = b\")\nopen(\"/private/tmp/claude-501/scratch/proto.py\",\"w\").write(s[:i])\nE\ncat >> /private/tmp/claude-501/scratch/proto2.py <<'E'\nr = pdf_hidden.scan(build(c))\nfor n,p in r[\"pages\"].items():\n    print(n, p[\"has_image\"], p[\"text_objects\"])\n    for h in p[\"hidden\"]: print(\"  H\", h[\"text\"], h[\"reasons\"])\n    print(\"  V\", repr(p[\"visible_text\"]))\nE\n.venv/bin/python /private/tmp/claude-501/scratch/proto2.py"
}
````

### User / tool · 2026-11-02T04:20:14.137Z

**tool result**
````
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/scratch/proto.py'
1 False 10
  H White hidden text ['blends_with_background']
  H Offpage text ['off_page']
  H Tiny text ['tiny_font']
  H scaled tiny two pt ['tiny_font']
  H Invisible mode ['invisible_render_mode']
  H nearly white ['blends_with_background']
  V 'Visible clinic note\nscaled normal 12pt\nCovered by white box\n...'
[This command modified 1 file you've previously read: app/backend/pdf_hidden.py. Call Read before editing.]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:20:37.376Z

**tool call — Write**
````
{
 "path": "/Users/arsis/zlayt-pm-project/app/backend/pdf_ocr.py",
 "content": "\"\"\"Local OCR for scanned PDF pages (T-086, D-042). The Tesseract binary runs as a subprocess on this machine; no page image or text\never leaves it, and nothing here calls a network. Rendering is pypdfium2 (PDFium), PNG encoding is stdlib zlib.\n\nOCR output is a guess at the printed words, so everything derived from it is held to a stricter rule than text-layer text:\n  - the page image is kept beside the OCR text, so the paralegal checks the words against the page itself;\n  - words Tesseract is unsure of are listed with their offsets (LOW_CONF_WORD / LOW_CONF_NUMBER below) and marked in the UI;\n  - every entry, amount and flag whose record lies on an OCR page is `needs_review` (reason OCR_DERIVED), whatever the model judges.\nThe OCR text is the case text for those pages, so quotes still have to match it word for word (the grounding verifier is unchanged).\nA missing Tesseract is a clear message (`ocr_status()`), never a crash. Tested with Tesseract 5.5.2; 5.x is accepted.\"\"\"\nimport base64\nimport csv\nimport io\nimport os\nimport re\nimport shutil\nimport struct\nimport subprocess\nimport tempfile\nimport time\nimport zlib\n\nTESTED_VERSION = \"5.5.2\"\nMIN_MAJOR = 5\nDPI = 150                       # render density; Tesseract reads 150 to 300 dpi, and a smaller image keeps the stored page small\nLOW_CONF_WORD = 60              # a word below this confidence (0-100) is marked\nLOW_CONF_NUMBER = 80            # a word with a digit in it needs this much: a wrong digit changes a date or a dollar amount\nMAX_OCR_PAGES = 10              # more scanned pages than this is refused, not partly read\nPAGE_TIMEOUT_S = 40\nTOTAL_TIMEOUT_S = 150\nMAX_LOW_CONF_LISTED = 400\nINSTALL_HINT = \"Install Tesseract: macOS `brew install tesseract`; Debian/Ubuntu `sudo apt-get install tesseract-ocr`.\"\n\n_ENV = {**os.environ, \"OMP_THREAD_LIMIT\": \"1\"}\n\n\nclass OcrUnavailable(RuntimeError):\n    \"\"\"Tesseract is missing or unusable; str(e) is a plain message for the user.\"\"\"\n\n\nclass OcrFailed(RuntimeError):\n    \"\"\"Tesseract ran and failed or timed out on a page.\"\"\"\n\n\ndef _which() -> str:\n    return shutil.which(\"tesseract\") or \"\"\n\n\ndef ocr_status() -> dict:\n    \"\"\"{available, version, tested_version, languages, message}. Never raises.\"\"\"\n    exe = _which()\n    if not exe:\n        return {\"available\": False, \"version\": None, \"tested_version\": TESTED_VERSION, \"languages\": [],\n                \"message\": \"Scanned pages need Tesseract, which is not installed on this server. \" + INSTALL_HINT}\n    try:\n        v = subprocess.run([exe, \"--version\"], capture_output=True, text=True, timeout=10, env=_ENV)\n        first = ((v.stdout or v.stderr).splitlines() or [\"\"])[0]\n        m = re.search(r\"(\\d+)\\.(\\d+)(?:\\.(\\d+))?\", first)\n        version = m.group(0) if m else None\n        langs = subprocess.run([exe, \"--list-langs\"], capture_output=True, text=True, timeout=10, env=_ENV)\n        languages = [x.strip() for x in (langs.stdout or \"\").splitlines()[1:] if x.strip() and x.strip() not in (\"osd\", \"snum\")]\n    except (OSError, subprocess.SubprocessError):\n        return {\"available\": False, \"version\": None, \"tested_version\": TESTED_VERSION, \"languages\": [],\n                \"message\": \"Tesseract is installed but could not be run. \" + INSTALL_HINT}\n    if not m or int(m.group(1)) < MIN_MAJOR or \"eng\" not in languages:\n        return {\"available\": False, \"version\": version, \"tested_version\": TESTED_VERSION, \"languages\": languages,\n                \"message\": f\"This server has Tesseract {version or '(unknown version)'} with English data \"\n                           f\"{'present' if 'eng' in languages else 'missing'}; version {MIN_MAJOR} or later with English data is needed. \" + INSTALL_HINT}\n    return {\"available\": True, \"version\": version, \"tested_version\": TESTED_VERSION, \"languages\": languages,\n            \"message\": f\"Tesseract {version} is available.\"}\n\n\n# ------------------------------------------------------------------ images\ndef _png(gray: bytes, w: int, h: int) -> bytes:\n    \"\"\"8-bit greyscale PNG from raw rows (stdlib only).\"\"\"\n    raw = b\"\".join(b\"\\x00\" + gray[y * w:(y + 1) * w] for y in range(h))\n\n    def chunk(tag, body):\n        c = tag + body\n        return struct.pack(\">I\", len(body)) + c + struct.pack(\">I\", zlib.crc32(c) & 0xFFFFFFFF)\n    return b\"\\x89PNG\\r\\n\\x1a\\n\" + chunk(b\"IHDR\", struct.pack(\">IIBBBBB\", w, h, 8, 0, 0, 0, 0)) + chunk(b\"IDAT\", zlib.compress(raw, 6)) + chunk(b\"IEND\", b\"\")\n\n\ndef render_page_png(pdf, index: int) -> bytes:\n    \"\"\"Greyscale PNG of page `index` (0-based) of an open pypdfium2 document at DPI.\"\"\"\n    page = pdf[index]\n    try:\n        bitmap = page.render(scale=DPI / 72.0)\n        try:\n            w, h, stride, ch = bitmap.width, bitmap.height, bitmap.stride, bitmap.n_channels\n            buf = bytes(bitmap.buffer)\n        finally:\n            bitmap.close()\n    finally:\n        page.close()\n    rows = []\n    for y in range(h):\n        row = buf[y * stride: y * stride + w * ch]\n        # BGR(x) -> grey by the green channel's neighbour mix: (B + 2G + R) / 4 without a per-pixel python loop\n        b, g, r = row[0::ch], row[1::ch], row[2::ch]\n        rows.append(bytes((x + 2 * y_ + z) >> 2 for x, y_, z in zip(b, g, r)) if ch >= 3 else row[0::ch])\n    return _png(b\"\".join(rows), w, h)\n\n\n# ------------------------------------------------------------------ tesseract\ndef _parse_tsv(tsv: str) -> dict:\n    \"\"\"Page text and word list from Tesseract TSV. Lines are rebuilt from the word rows, so word offsets are exact.\"\"\"\n    rows = [r for r in csv.reader(io.StringIO(tsv), delimiter=\"\\t\", quoting=csv.QUOTE_NONE) if len(r) >= 12 and r[0] != \"level\"]\n    text, words, last_line, last_block = \"\", [], None, None\n    for r in rows:\n        if r[0] != \"5\" or not r[11].strip():\n            continue\n        try:\n            conf = float(r[10])\n        except ValueError:\n            continue\n        key, block = (r[2], r[3], r[4]), (r[2], r[3])\n        if last_line is not None:\n            text += (\"\\n\\n\" if block != last_block else \"\\n\") if key != last_line else \" \"\n        start = len(text)\n        text += r[11].strip()\n        words.append({\"text\": r[11].strip(), \"start\": start, \"end\": len(text), \"conf\": round(conf, 1)})\n        last_line, last_block = key, block\n    return {\"text\": text, \"words\": words}\n\n\ndef is_low(word: dict) -> bool:\n    need = LOW_CONF_NUMBER if any(c.isdigit() for c in word[\"text\"]) else LOW_CONF_WORD\n    return word[\"conf\"] < need\n\n\ndef ocr_png(png: bytes, languages: list = None, timeout: float = PAGE_TIMEOUT_S) -> dict:\n    \"\"\"{text, words:[{text,start,end,conf}], low_conf:[...], mean_conf}. Raises OcrUnavailable / OcrFailed.\"\"\"\n    st = ocr_status()\n    if not st[\"available\"]:\n        raise OcrUnavailable(st[\"message\"])\n    lang = \"+\".join(l for l in (languages or [\"eng\"]) if l in st[\"languages\"]) or \"eng\"\n    with tempfile.TemporaryDirectory(prefix=\"zlayt-ocr-\") as d:\n        src = os.path.join(d, \"page.png\")\n        with open(src, \"wb\") as f:\n            f.write(png)\n        try:\n            p = subprocess.run([_which(), src, \"stdout\", \"-l\", lang, \"--psm\", \"3\", \"tsv\"], capture_output=True, text=True,\n                               timeout=timeout, env=_ENV, cwd=d)\n        except subprocess.TimeoutExpired:\n            raise OcrFailed(\"timeout\") from None\n        except OSError:\n            raise OcrFailed(\"exec\") from None\n    if p.returncode != 0:\n        raise OcrFailed(\"exit\")\n    got = _parse_tsv(p.stdout)\n    low = [w for w in got[\"words\"] if is_low(w)]\n    confs = [w[\"conf\"] for w in got[\"words\"]]\n    return {\"text\": got[\"text\"], \"words\": got[\"words\"], \"low_conf\": low,\n            \"mean_conf\": round(sum(confs) / len(confs), 1) if confs else None}\n\n\ndef ocr_pages(data: bytes, pages: list, deadline: float = None) -> dict:\n    \"\"\"OCR the given 1-based `pages` of a PDF. {n: {text, low_conf (page offsets), mean_conf, words, png_b64}}.\n    Raises OcrUnavailable (checked first, before any rendering), OcrFailed.\"\"\"\n    st = ocr_status()\n    if not st[\"available\"]:\n        raise OcrUnavailable(st[\"message\"])\n    import pypdfium2 as pdfium\n    start = time.monotonic()\n    out = {}\n    pdf = pdfium.PdfDocument(data)\n    try:\n        for n in pages:\n            if time.monotonic() - start > TOTAL_TIMEOUT_S or (deadline and time.monotonic() > deadline):\n                raise OcrFailed(\"timeout\")\n            png = render_page_png(pdf, n - 1)\n            got = ocr_png(png)\n            out[n] = {\"text\": got[\"text\"], \"words\": len(got[\"words\"]), \"mean_conf\": got[\"mean_conf\"],\n                      \"low_conf\": [{\"start\": w[\"start\"], \"end\": w[\"end\"], \"text\": w[\"text\"], \"conf\": w[\"conf\"]} for w in got[\"low_conf\"]],\n                      \"png_b64\": base64.b64encode(png).decode(\"ascii\")}\n    except (OcrUnavailable, OcrFailed):\n        raise\n    except Exception as e:             # PDFium could not render the page\n        raise OcrFailed(type(e).__name__) from None\n    finally:\n        pdf.close()\n    return out\n"
}
````

### User / tool · 2026-11-02T04:20:37.431Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/app/backend/pdf_ocr.py (file state is current in your context — no need to Read it back)

Note: Write's parameters are named `file_path` and `content`. `path` was read as `file_path`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:20:42.770Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/pdf_ocr.py\"\ns=open(p).read()\na=s.index(\"    rows = []\\n    for y in range(h):\")\nb=s.index(\"    return _png(b\\\"\\\".join(rows), w, h)\")\ns=s[:a]+'''    # the green channel stands in for luminance (a slice per row, no per-pixel loop)\n    rows = [buf[y * stride + (1 if ch >= 3 else 0): y * stride + w * ch: ch] for y in range(h)]\n'''+s[b:]\ns=s.replace('''def ocr_png(png: bytes, languages: list = None, timeout: float = PAGE_TIMEOUT_S) -> dict:\n    \"\"\"{text, words:[{text,start,end,conf}], low_conf:[...], mean_conf}. Raises OcrUnavailable / OcrFailed.\"\"\"\n    st = ocr_status()''','''def ocr_png(png: bytes, languages: list = None, timeout: float = PAGE_TIMEOUT_S, status: dict = None) -> dict:\n    \"\"\"{text, words:[{text,start,end,conf}], low_conf:[...], mean_conf}. Raises OcrUnavailable / OcrFailed.\"\"\"\n    st = status or ocr_status()''')\ns=s.replace(\"got = ocr_png(png)\",\"got = ocr_png(png, status=st)\")\nopen(p,\"w\").write(s)\nE"
}
````

### User / tool · 2026-11-02T04:20:42.891Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:02.360Z

**tool call — Write**
````
{
 "path": "/Users/arsis/zlayt-pm-project/app/backend/pdf_checks.py",
 "content": "\"\"\"PDF intake checks, one pass (T-086 local OCR + T-087 hidden text; D-042). Deterministic code; the only external program is the\nlocal Tesseract binary. `extract()` is what POST /api/cases/pdf calls; `mark_ocr_items()` is what the pipeline calls before it\nstores items.\n\nOrder: read the text layer (pypdf) -> find text that is not visible when the page is rendered (pdf_hidden) and take it out of the\npage text unless the paralegal confirmed that page -> pages left with no text are OCR'd locally only when the caller asked for OCR.\nThe case text is the result, so hidden text can never ground a quote and OCR words are quoted exactly as OCR read them.\"\"\"\nimport time\n\nfrom app.backend import pdf_hidden, pdf_ocr, pdf_text\nfrom app.backend.pdf_text import PdfError\n\nOCR_TIMEOUT_S = pdf_ocr.TOTAL_TIMEOUT_S + 15     # the API's wait when OCR was requested (the plain text path keeps pdf_text.EXTRACT_TIMEOUT_S)\n\nMESSAGES = {\n    \"pdf_no_text_layer\": \"This PDF has no text layer (it looks scanned). Run OCR to read the scanned pages, or paste the text instead.\",\n    \"pdf_only_hidden_text\": \"Every piece of text in this PDF's text layer is hidden when the page is shown, so nothing was read. \"\n                            \"Run OCR to read what the pages show, or confirm the hidden text if you trust it.\",\n    \"ocr_unavailable\": \"Scanned pages need Tesseract, which is not available on this server.\",\n    \"ocr_too_many_pages\": f\"This PDF has more than {pdf_ocr.MAX_OCR_PAGES} scanned pages; OCR reads at most that many in one upload. Split the file.\",\n    \"ocr_failed\": \"OCR could not read a page of this PDF. Try again, or paste the text instead.\",\n}\n\n\ndef parse_confirmed(value, pages: int):\n    \"\"\"Query value -> set of confirmed hidden-text pages. 'all' (or '1') = every page; '2,5' = those pages; empty = none.\"\"\"\n    v = (value or \"\").strip().lower()\n    if v in (\"all\", \"1\", \"true\", \"yes\"):\n        return set(range(1, pages + 1))\n    out = set()\n    for part in v.split(\",\"):\n        part = part.strip()\n        if part.isdigit():\n            out.add(int(part))\n    return out\n\n\ndef extract(data: bytes, *, ocr: bool = False, include_hidden=None) -> dict:\n    \"\"\"{text, pages: [{page, start, end, source?, ...}], pdf_checks: {...}, page_images: {n: base64 png}}.\n    `include_hidden`: the raw query value for confirmed hidden-text pages (see parse_confirmed). Raises PdfError.\"\"\"\n    texts = pdf_text.read_pages(data)\n    confirmed = parse_confirmed(include_hidden, len(texts))\n    checks = {\"hidden_text\": {\"checked\": False, \"pages\": [], \"excluded_until_confirmed\": True,\n                              \"message\": \"Hidden-text check did not run on this file.\"},\n              \"ocr\": {\"requested\": bool(ocr), \"ran\": False, \"pages\": [], \"status\": pdf_ocr.ocr_status()}}\n    scanned = None\n    try:\n        scanned = pdf_hidden.scan(data)\n    except pdf_hidden.HiddenScanUnavailable:\n        pass\n    sources, image_pages = {}, []\n    if scanned:\n        for n, p in scanned[\"pages\"].items():\n            if p[\"hidden\"] and n not in confirmed and n <= len(texts):\n                texts[n - 1] = pdf_hidden.remove_from_text(texts[n - 1], p[\"hidden\"], p[\"visible_text\"])\n        checks[\"hidden_text\"] = pdf_hidden.report(scanned, confirmed)\n        for n in confirmed:\n            if n in scanned[\"pages\"] and scanned[\"pages\"][n][\"hidden\"]:\n                sources[n] = {\"hidden_text_included\": True}\n        # a page with no text left but a picture on it is a scan (or has only hidden text over a picture)\n        image_pages = [n for n, p in scanned[\"pages\"].items() if not \"\".join(texts[n - 1].split()) and p[\"has_image\"]]\n    blank = [n for n, t in enumerate(texts, 1) if not \"\".join(t.split())]\n    scan_pages = sorted(set(image_pages) | (set(blank) if not any(\"\".join(t.split()) for t in texts) else set()))\n    ocr_page_data = {}\n    if scan_pages:\n        checks[\"ocr\"][\"scanned_pages\"] = scan_pages\n        if ocr:\n            if len(scan_pages) > pdf_ocr.MAX_OCR_PAGES:\n                raise PdfError(\"ocr_too_many_pages\", {\"scanned_pages\": len(scan_pages), \"max\": pdf_ocr.MAX_OCR_PAGES})\n            try:\n                ocr_page_data = pdf_ocr.ocr_pages(data, scan_pages)\n            except pdf_ocr.OcrUnavailable as e:\n                raise PdfError(\"ocr_unavailable\", {\"message\": str(e), \"ocr\": checks[\"ocr\"][\"status\"]}) from None\n            except pdf_ocr.OcrFailed:\n                raise PdfError(\"ocr_failed\") from None\n            for n, o in ocr_page_data.items():\n                texts[n - 1] = o[\"text\"].strip()\n                sources[n] = {\"source\": \"ocr\", \"mean_conf\": o[\"mean_conf\"], \"words\": o[\"words\"], \"has_image\": True}\n    if sum(len(\"\".join(t.split())) for t in texts) < pdf_text.MIN_TEXT_CHARS:\n        hidden_pages = [p[\"page\"] for p in checks[\"hidden_text\"][\"pages\"] if not p[\"confirmed\"]]\n        detail = {\"scanned_pages\": scan_pages, \"ocr\": checks[\"ocr\"][\"status\"], \"hidden_text_pages\": hidden_pages}\n        raise PdfError(\"pdf_only_hidden_text\" if hidden_pages else \"pdf_no_text_layer\", detail)\n    got = pdf_text.assemble(texts, sources)\n    images, low = {}, 0\n    for pg in got[\"pages\"]:\n        o = ocr_page_data.get(pg[\"page\"])\n        if o:\n            base = pg[\"start\"]\n            pg[\"low_conf\"] = [{\"start\": base + w[\"start\"], \"end\": base + w[\"end\"], \"text\": w[\"text\"], \"conf\": w[\"conf\"]}\n                              for w in o[\"low_conf\"][:pdf_ocr.MAX_LOW_CONF_LISTED]]\n            pg[\"low_conf_count\"] = len(o[\"low_conf\"])\n            low += len(o[\"low_conf\"])\n            images[pg[\"page\"]] = o[\"png_b64\"]\n    if ocr_page_data:\n        checks[\"ocr\"].update({\"ran\": True, \"engine\": f\"tesseract {checks['ocr']['status']['version']}\",\n                              \"pages\": sorted(ocr_page_data), \"low_conf_words\": low,\n                              \"low_conf_rule\": f\"words under {pdf_ocr.LOW_CONF_WORD} confidence, or under {pdf_ocr.LOW_CONF_NUMBER} when the word has a digit\",\n                              \"items_need_review\": True})\n    return {\"text\": got[\"text\"], \"pages\": got[\"pages\"], \"pdf_checks\": checks, \"page_images\": images}\n\n\ndef is_ocr_span(pages, start: int, end: int) -> bool:\n    \"\"\"True when [start, end) overlaps the text of an OCR page.\"\"\"\n    return any(p.get(\"source\") == \"ocr\" and p[\"start\"] < max(end, start + 1) and start < p[\"end\"] for p in (pages or []))\n\n\ndef mark_ocr_items(items: list, recs: list, pages: list, why_text: str) -> int:\n    \"\"\"Every non-rejected item whose record lies on an OCR page becomes needs_review with reason OCR_DERIVED (never `verified`).\n    Items carry `record_ids` ('r<n>'); `recs` are the ingest records ({n, char_start, char_end}). Mutates in place; returns the count.\"\"\"\n    if not any(p.get(\"source\") == \"ocr\" for p in pages or []):\n        return 0\n    ocr_ids = {f\"r{r['n']}\" for r in recs if is_ocr_span(pages, r[\"char_start\"], r[\"char_end\"])}\n    n = 0\n    for it in items:\n        if it.get(\"state\") == \"rejected\" or not ocr_ids.intersection(it.get(\"record_ids\") or []):\n            continue\n        reasons = list(it.get(\"reasons\") or [])\n        if \"OCR_DERIVED\" not in reasons:\n            reasons.append(\"OCR_DERIVED\")\n        it[\"reasons\"], it[\"state\"] = reasons, \"needs_review\"\n        it[\"why\"] = (it.get(\"why\") + \" \" if it.get(\"why\") and \"OCR_DERIVED\" not in (it.get(\"reasons\") or [])[:-1] else \"\") + why_text\n        if isinstance(it.get(\"ladder\"), dict):\n            it[\"ladder\"][\"state\"] = \"needs_review\"\n            it[\"ladder\"].setdefault(\"code_checks\", {})[\"ocr_derived\"] = True\n        n += 1\n    return n\n\n\ndef summary_for_case(config: dict) -> dict:\n    \"\"\"The pdf_checks block GET /api/cases/{token} returns (no images, no page text).\"\"\"\n    return (config or {}).get(\"pdf_checks\")\n"
}
````

### User / tool · 2026-11-02T04:21:02.417Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/app/backend/pdf_checks.py (file state is current in your context — no need to Read it back)

Note: Write's parameters are named `file_path` and `content`. `path` was read as `file_path`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:09.297Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/pdf_checks.py\"\ns=open(p).read()\na=s.index(\"        reasons = list(it.get\")\nb=s.index(\"        if isinstance(it.get(\\\"ladder\\\")\")\ns=s[:a]+'''        reasons = list(it.get(\"reasons\") or [])\n        if \"OCR_DERIVED\" not in reasons:\n            reasons.append(\"OCR_DERIVED\")\n            it[\"why\"] = ((it.get(\"why\") or \"\") + \" \" + why_text).strip()\n        it[\"reasons\"], it[\"state\"] = reasons, \"needs_review\"\n'''+s[b:]\ns=s[:s.index(\"\\n\\ndef summary_for_case\")]+\"\\n\"\ns=s.replace(\"import time\\n\\n\",\"\")\nopen(p,\"w\").write(s)\nE\ngrep -n \"def get_case\\|/api/cases/{token}\\\"\\|def case_or_404\\|def conn\\|404\" app/backend/api.py | head -20"
}
````

### User / tool · 2026-11-02T04:21:09.405Z

**tool result**
````
123:    def conn():
138:    def get_case(c, token):
141:            raise ApiError(404, "not_found", "No such case.")
155:        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
219:            raise ApiError(404, "not_found", "Not found.")
229:            raise ApiError(404, "not_found", "Not found.")
239:                raise ApiError(404, "not_found", "Not found.")
242:                raise ApiError(404, "not_found", "No such library case.")
304:    @app.get("/api/cases/{token}")
305:    def get_case_view(token: str):
313:    @app.delete("/api/cases/{token}", status_code=204)
468:                raise ApiError(404, "not_found", "No draft paragraph yet.") from None
482:                raise ApiError(404, "not_found", "No such item.") from None
537:                raise ApiError(404, "not_found", "No such item.") from None
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:11.069Z

**tool call — Bash**
````
{
 "command": "sed -n 118,150p app/backend/api.py; sed -n 300,330p app/backend/api.py; git diff --stat app/backend/api.py app/backend/present.py app/backend/confidence.py app/backend/why.py memory/contracts/api.md requirements.txt app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T04:21:11.186Z

**tool result**
````
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
        return DB.connect(app.state.db_path)

    def make_call(c, cid):
        if call_factory:
            return call_factory(c, cid)
        from app.llm import audited
        return audited.make_call(c, cid)

    def pipeline_mod():
        if pipeline is not None:
            return pipeline
        from app.backend import pipeline as PL
        return PL

    def get_case(c, token):
        case = DB.get_case(c, token)
        if case is None:
            raise ApiError(404, "not_found", "No such case.")
        return case

    # -------------------------------------------------- errors / headers
    @app.exception_handler(ApiError)
    async def _api_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(review.ReviewError)
    async def _review_error(_, e):
                    "warnings": ing["warnings"]}
        finally:
            c.close()

    @app.get("/api/cases/{token}")
    def get_case_view(token: str):
        c = conn()
        try:
            get_case(c, token)
            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
        finally:
            c.close()

    @app.delete("/api/cases/{token}", status_code=204)
    def delete_case(token: str):
        c = conn()
        try:
            get_case(c, token)
            DB.delete_case(c, token)
        finally:
            c.close()
        return Response(status_code=204)

    def _run_thread(token, raw):
        c = conn()
        try:
            mod = pipeline_mod()
            mod.run_pipeline(c, token, raw, call=make_call(c, token), now=time.time)
            if DB.get_case(c, token)["status"] == "running":
                DB.update_case(c, token, status="ready", stage="finalize", run_finished_at=time.time())
        except Exception as e:                                   # code only: no message text from the pipeline
 app/backend/api.py      |  5 ++++-
 app/backend/pipeline.py | 18 +++++++-----------
 app/backend/present.py  |  9 ++++++---
 memory/contracts/api.md | 29 +++++++++++++++++++++++++++++
 4 files changed, 46 insertions(+), 15 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:15.436Z

**tool call — Bash**
````
{
 "command": "grep -n \"monkeypatch\\|pdf_text\\.\" tests/unit/test_pdf_upload.py | head -30; grep -rn \"pdf_text.extract\\|pdf_text\\b\" tests --include=*.py -l"
}
````

### User / tool · 2026-11-02T04:21:15.529Z

**tool result**
````
50:def client(tmp_path, monkeypatch):
51:    monkeypatch.setenv("LLM_BACKEND", "claude-cli")     # local live mode (arbitrary text allowed); this test never runs the pipeline
52:    monkeypatch.setenv("ENABLE_LIVE", "1")
53:    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
58:def test_scanned_pdf_upload_is_refused_and_nothing_is_stored_or_called(client, monkeypatch):
62:    monkeypatch.setattr(provider, "complete_with_meta", lambda *a, **k: calls.append(1))
94:def test_demo_mode_refuses_a_pdf_whose_text_is_not_recorded(tmp_path, monkeypatch):
96:    monkeypatch.setenv("LLM_BACKEND", "fixture")
97:    monkeypatch.delenv("ENABLE_LIVE", raising=False)
106:    raise AssertionError("pdf_text.extract must not run")
109:def test_demo_mode_refuses_before_any_parsing(tmp_path, monkeypatch):
110:    monkeypatch.setenv("LLM_BACKEND", "fixture")
111:    monkeypatch.delenv("ENABLE_LIVE", raising=False)
112:    monkeypatch.setattr(PT, "extract", _boom)
118:def test_oversize_pdf_is_refused_before_parsing(client, monkeypatch):
119:    monkeypatch.setattr(PT, "extract", _boom)
125:def test_parsing_does_not_block_the_event_loop(tmp_path, monkeypatch):
129:    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
130:    monkeypatch.setenv("ENABLE_LIVE", "1")
136:    monkeypatch.setattr(PT, "extract", slow)
150:def test_slow_extraction_hits_the_time_cap(tmp_path, monkeypatch):
152:    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
153:    monkeypatch.setenv("ENABLE_LIVE", "1")
154:    monkeypatch.setattr(PT, "EXTRACT_TIMEOUT_S", 0.2)
155:    monkeypatch.setattr(PT, "extract", lambda d: time.sleep(1.0))
tests/unit/test_pdf_upload.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:27.414Z

**tool call — Bash**
````
{
 "command": "sed -n 100,160p tests/unit/test_pdf_upload.py"
}
````

### User / tool · 2026-11-02T04:21:27.497Z

**tool result**
````
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:38.387Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/pdf_text.py\"\ns=open(p).read()\ns=s.replace('''def extract(data: bytes) -> dict:\n    \"\"\"{text, pages: [{page, start, end}]} from the text layer alone; a file with no usable text layer is refused.\"\"\"\n    texts = read_pages(data)\n    if sum(len(\"\".join(t.split())) for t in texts) < MIN_TEXT_CHARS:\n        raise PdfError(\"pdf_no_text_layer\")\n    return assemble(texts)\n''','''def extract_text_layer(data: bytes) -> dict:\n    \"\"\"{text, pages: [{page, start, end}]} from the text layer alone (no hidden-text check, no OCR); no usable text layer is refused.\"\"\"\n    texts = read_pages(data)\n    if sum(len(\"\".join(t.split())) for t in texts) < MIN_TEXT_CHARS:\n        raise PdfError(\"pdf_no_text_layer\")\n    return assemble(texts)\n\n\ndef extract(data: bytes, **options) -> dict:\n    \"\"\"What POST /api/cases/pdf runs: the text layer minus text that is hidden when the page is shown (T-087), plus local OCR of scanned\n    pages when `ocr=True` (T-086). Options: ocr (bool), include_hidden ('all' | '2,5': pages whose hidden text the paralegal confirmed).\n    Result: {text, pages, pdf_checks, page_images}; see pdf_checks.extract.\"\"\"\n    from app.backend import pdf_checks\n    return pdf_checks.extract(data, **options)\n''')\ns=s.replace('''\"\"\"PDF text-layer extraction (D-031). Pure python (pypdf), no OCR: a PDF with no text layer is refused before anything is stored or any\nmodel is called.''','''\"\"\"PDF text-layer extraction (D-031). Pure python (pypdf) reads the text layer; hidden-text detection (pdf_hidden) and opt-in local OCR\n(pdf_ocr) are layered on by pdf_checks. A PDF with no usable text is refused before anything is stored or any model is called.''')\nopen(p,\"w\").write(s)\nE\nhead -5 app/backend/pdf_text.py"
}
````

### User / tool · 2026-11-02T04:21:38.486Z

**tool result**
````
"""PDF text-layer extraction (D-031). Pure python (pypdf) reads the text layer; hidden-text detection (pdf_hidden) and opt-in local OCR
(pdf_ocr) are layered on by pdf_checks. A PDF with no usable text is refused before anything is stored or any model is called. The extracted text is the case text; `pages` maps character offsets of that text to page numbers so citations can
carry them. Deterministic code only."""
import io
import logging
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:01.204Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/_pdf_raw.py <<'E'\n\"\"\"Hand-built PDFs for the hidden-text and OCR tests (T-086/T-087): raw content streams, and an image-only 'scan' made by rendering a\ntext PDF with pypdfium2 and embedding the pixels as an image with no text layer. All text is SYNTHETIC.\"\"\"\nimport zlib\n\n\ndef build(content: bytes, mediabox: str = \"0 0 600 800\", image: tuple = None) -> bytes:\n    \"\"\"One page. `image` = (gray_bytes, width, height): drawn full-page, no text layer unless `content` adds one.\"\"\"\n    objs = [b\"<< /Type /Catalog /Pages 2 0 R >>\", b\"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\",\n            (f\"<< /Type /Page /Parent 2 0 R /MediaBox [{mediabox}] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >>\"\n             + (\" /XObject << /Im1 6 0 R >>\" if image else \"\") + \" >> >>\").encode(),\n            b\"<< /Length %d >>\\nstream\\n\" % len(content) + content + b\"\\nendstream\",\n            b\"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\"]\n    if image:\n        gray, w, h = image\n        z = zlib.compress(gray)\n        objs.append(f\"<< /Type /XObject /Subtype /Image /Width {w} /Height {h} /ColorSpace /DeviceGray /BitsPerComponent 8 \"\n                    f\"/Filter /FlateDecode /Length {len(z)} >>\\nstream\\n\".encode() + z + b\"\\nendstream\")\n    out, offs = bytearray(b\"%PDF-1.4\\n\"), []\n    for i, o in enumerate(objs, 1):\n        offs.append(len(out))\n        out += f\"{i} 0 obj\\n\".encode() + o + b\"\\nendobj\\n\"\n    x = len(out)\n    out += f\"xref\\n0 {len(objs) + 1}\\n\".encode() + b\"0000000000 65535 f \\n\"\n    for o in offs:\n        out += f\"{o:010d} 00000 n \\n\".encode()\n    out += f\"trailer\\n<< /Size {len(objs) + 1} /Root 1 0 R >>\\nstartxref\\n{x}\\n%%EOF\\n\".encode()\n    return bytes(out)\n\n\ndef text_page(lines, size=14, x=50, y=740, lead=22) -> bytes:\n    parts = [b\"BT /F1 %d Tf %d TL %d %d Td\" % (size, lead, x, y)]\n    for ln in lines:\n        parts.append(b\"(\" + ln.replace(\"\\\\\", \"\\\\\\\\\").replace(\"(\", \"\\\\(\").replace(\")\", \"\\\\)\").encode(\"latin-1\") + b\") Tj T*\")\n    parts.append(b\"ET\")\n    return b\"\\n\".join(parts)\n\n\ndef scanned_copy(pdf_bytes: bytes, scale: float = 2.0) -> bytes:\n    \"\"\"An image-only PDF that looks like `pdf_bytes` page 1 when shown (no text layer).\"\"\"\n    import pypdfium2 as pdfium\n    page = pdfium.PdfDocument(pdf_bytes)[0]\n    bm = page.render(scale=scale)\n    w, h, stride, ch = bm.width, bm.height, bm.stride, bm.n_channels\n    buf = bytes(bm.buffer)\n    gray = b\"\".join(buf[y * stride + 1: y * stride + w * ch: ch] for y in range(h))\n    return build(b\"q 600 0 0 800 0 0 cm /Im1 Do Q\", image=(gray, w, h))\nE\ncat > tests/unit/test_pdf_hidden.py <<'E'\n\"\"\"T-087: text in the text layer that is not visible when the page is rendered is flagged per page and kept out of the case text\nuntil the paralegal confirms it. Synthetic PDFs are generated here (tests/unit/_pdf_raw.py).\"\"\"\nimport pytest\n\nfrom app.backend import pdf_checks, pdf_hidden, pdf_text\nfrom tests.unit._pdf_raw import build, text_page\n\npytest.importorskip(\"pypdfium2\")\n\nVISIBLE = \"SYNTHETIC visit 03/04/2023 Dr. Rao: neck pain 6/10, ibuprofen prescribed.\"\nHIDDEN = {\n    \"white\": (b\"BT /F1 12 Tf 1 1 1 rg 50 650 Td (PLANTED white text: patient was symptom free.) Tj ET\", \"blends_with_background\"),\n    \"offpage\": (b\"BT /F1 12 Tf 0 g 900 650 Td (PLANTED off page text.) Tj ET\", \"off_page\"),\n    \"tiny\": (b\"BT /F1 1 Tf 0 g 50 600 Td (PLANTED tiny text.) Tj ET\", \"tiny_font\"),\n    \"invisible\": (b\"BT /F1 12 Tf 3 Tr 0 g 50 550 Td (PLANTED invisible mode text.) Tj ET 0 Tr\", \"invisible_render_mode\"),\n    \"scaled_tiny\": (b\"q 0.1 0 0 0.1 0 0 cm BT /F1 20 Tf 0 g 500 5000 Td (PLANTED scaled tiny text.) Tj ET Q\", \"tiny_font\"),\n    \"covered\": (b\"BT /F1 12 Tf 0 g 50 500 Td (PLANTED covered text.) Tj ET\\n1 1 1 rg 40 490 300 40 re f\", \"blends_with_background\"),\n    \"near_white\": (b\"BT /F1 12 Tf 0.97 g 50 450 Td (PLANTED nearly white text.) Tj ET\", \"blends_with_background\"),\n}\n\n\ndef pdf_with(*keys, page_text=VISIBLE):\n    return build(text_page([page_text]) + b\"\\n\" + b\"\\n\".join(HIDDEN[k][0] for k in keys))\n\n\n@pytest.mark.parametrize(\"key\", sorted(HIDDEN))\ndef test_each_kind_of_hidden_text_is_flagged_with_its_reason(key):\n    scanned = pdf_hidden.scan(pdf_with(key))\n    hidden = scanned[\"pages\"][1][\"hidden\"]\n    assert len(hidden) == 1 and \"PLANTED\" in hidden[0][\"text\"]\n    assert HIDDEN[key][1] in hidden[0][\"reasons\"]\n\n\ndef test_visible_text_is_never_flagged():\n    scanned = pdf_hidden.scan(build(text_page([VISIBLE, \"Second visible line: ROM limited.\"])))\n    assert scanned[\"pages\"][1][\"hidden\"] == [] and scanned[\"pages\"][1][\"text_objects\"] >= 1\n\n\ndef test_small_but_legible_and_coloured_text_is_visible():\n    c = text_page([VISIBLE]) + b\"\\nBT /F1 7 Tf 0 0 0.6 rg 50 600 Td (Footnote in small blue type.) Tj ET\\nBT /F1 12 Tf 0.5 g 50 560 Td (Grey stamp.) Tj ET\"\n    assert pdf_hidden.scan(build(c))[\"pages\"][1][\"hidden\"] == []\n\n\ndef test_white_text_on_a_dark_box_is_visible():\n    c = b\"0 g 40 600 300 40 re f\\nBT /F1 14 Tf 1 g 50 612 Td (White on black label.) Tj ET\"\n    assert pdf_hidden.scan(build(c))[\"pages\"][1][\"hidden\"] == []\n\n\ndef test_hidden_text_is_excluded_from_the_case_text_and_reported_per_page():\n    got = pdf_checks.extract(pdf_with(\"white\", \"offpage\", \"tiny\"))\n    assert \"PLANTED\" not in got[\"text\"] and VISIBLE in got[\"text\"]\n    ht = got[\"pdf_checks\"][\"hidden_text\"]\n    assert ht[\"checked\"] and ht[\"excluded_until_confirmed\"] and [p[\"page\"] for p in ht[\"pages\"]] == [1]\n    page = ht[\"pages\"][0]\n    assert page[\"count\"] == 3 and page[\"excluded\"] and not page[\"confirmed\"]\n    assert {r for it in page[\"items\"] for r in it[\"reasons\"]} == {\"blends_with_background\", \"off_page\", \"tiny_font\"}\n    assert all(it[\"why\"] for it in page[\"items\"])\n\n\ndef test_paralegal_confirmation_includes_the_hidden_text_for_that_page_only():\n    two = build(text_page([VISIBLE]) + b\"\\n\" + HIDDEN[\"white\"][0])\n    got = pdf_checks.extract(two, include_hidden=\"1\")\n    assert \"PLANTED white text\" in got[\"text\"]\n    page = got[\"pdf_checks\"][\"hidden_text\"][\"pages\"][0]\n    assert page[\"confirmed\"] and not page[\"excluded\"]\n    assert got[\"pages\"][0][\"hidden_text_included\"] is True\n    assert \"PLANTED\" not in pdf_checks.extract(two, include_hidden=\"2\")[\"text\"]\n\n\ndef test_pdf_text_extract_applies_the_check_by_default():\n    assert \"PLANTED\" not in pdf_text.extract(pdf_with(\"white\"))[\"text\"]\n\n\ndef test_a_pdf_whose_only_text_is_hidden_is_refused_with_the_hidden_pages_named():\n    with pytest.raises(pdf_text.PdfError) as e:\n        pdf_checks.extract(build(HIDDEN[\"white\"][0] + b\"\\n\" + HIDDEN[\"offpage\"][0]))\n    assert e.value.code == \"pdf_only_hidden_text\" and e.value.detail[\"hidden_text_pages\"] == [1]\n\n\ndef test_removal_falls_back_to_the_visible_objects_when_the_strings_cannot_be_matched():\n    out = pdf_hidden.remove_from_text(\"Visible A\\nsomething the extractor spelled differently\",\n                                      [{\"text\": \"PLANTED\", \"reasons\": []}], \"Visible A\")\n    assert out == \"Visible A\"\n\n\ndef test_removal_takes_a_whole_hidden_line_with_its_line_break():\n    assert pdf_hidden.remove_from_text(\"line one\\nHIDDEN words\\nline three\", [{\"text\": \"HIDDEN words\", \"reasons\": []}], \"\") == \"line one\\nline three\"\n\n\ndef test_two_page_pdf_reports_only_the_page_with_hidden_text():\n    # page 2 is a copy of the builder's single page: build a 2-page file by hand\n    from tests.unit._pdf import make_pdf\n    base = make_pdf([[VISIBLE], [VISIBLE]])\n    got = pdf_checks.extract(base)\n    assert got[\"pdf_checks\"][\"hidden_text\"][\"pages\"] == []\nE\n.venv/bin/python -m pytest -q tests/unit/test_pdf_hidden.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:22:01.884Z

**tool result**
````
.................                                                        [100%]
17 passed in 0.33s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:09.518Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/_pdf_raw.py <<'E'\n\n\ndef build_pages(contents: list, mediabox: str = \"0 0 600 800\") -> bytes:\n    \"\"\"Several text pages: one content stream each (Helvetica as /F1).\"\"\"\n    n = len(contents)\n    kids = \" \".join(f\"{3 + 2 * i} 0 R\" for i in range(n))\n    objs = [b\"<< /Type /Catalog /Pages 2 0 R >>\", f\"<< /Type /Pages /Kids [{kids}] /Count {n} >>\".encode()]\n    for i, c in enumerate(contents):\n        objs.append(f\"<< /Type /Page /Parent 2 0 R /MediaBox [{mediabox}] /Contents {4 + 2 * i} 0 R \"\n                    f\"/Resources << /Font << /F1 {3 + 2 * n} 0 R >> >> >>\".encode())\n        objs.append(b\"<< /Length %d >>\\nstream\\n\" % len(c) + c + b\"\\nendstream\")\n    objs.append(b\"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\")\n    out, offs = bytearray(b\"%PDF-1.4\\n\"), []\n    for i, o in enumerate(objs, 1):\n        offs.append(len(out))\n        out += f\"{i} 0 obj\\n\".encode() + o + b\"\\nendobj\\n\"\n    x = len(out)\n    out += f\"xref\\n0 {len(objs) + 1}\\n\".encode() + b\"0000000000 65535 f \\n\"\n    for o in offs:\n        out += f\"{o:010d} 00000 n \\n\".encode()\n    out += f\"trailer\\n<< /Size {len(objs) + 1} /Root 1 0 R >>\\nstartxref\\n{x}\\n%%EOF\\n\".encode()\n    return bytes(out)\nE\npython3 - <<'E'\np=\"tests/unit/test_pdf_hidden.py\"\ns=open(p).read()\ni=s.index(\"def test_two_page_pdf\")\ns=s[:i]+'''def test_two_page_pdf_reports_only_the_page_with_hidden_text():\n    two = build_pages([text_page([VISIBLE]), text_page([\"Page two visible line.\"]) + b\"\\\\n\" + HIDDEN[\"white\"][0]])\n    got = pdf_checks.extract(two)\n    assert [p[\"page\"] for p in got[\"pdf_checks\"][\"hidden_text\"][\"pages\"]] == [2]\n    assert \"Page two visible line.\" in got[\"text\"] and \"PLANTED\" not in got[\"text\"]\n    assert \"PLANTED\" not in pdf_checks.extract(two, include_hidden=\"1\")[\"text\"]       # confirming page 1 does not include page 2\n    assert \"PLANTED\" in pdf_checks.extract(two, include_hidden=\"1,2\")[\"text\"]\n    assert \"PLANTED\" in pdf_checks.extract(two, include_hidden=\"all\")[\"text\"]\n'''\ns=s.replace(\"from tests.unit._pdf_raw import build, text_page\",\"from tests.unit._pdf_raw import build, build_pages, text_page\")\nopen(p,\"w\").write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_pdf_hidden.py 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T04:22:10.293Z

**tool result**
````
E           ble line.
E           PLANTED white text: patient was symptom free.
E         ? +++++++

tests/unit/test_pdf_hidden.py:95: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_pdf_hidden.py::test_two_page_pdf_reports_only_the_page_with_hidden_text
1 failed, 16 passed in 0.39s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:13.604Z

**tool call — Bash**
````
{
 "command": "sed -i 's/    if v in (\"all\", \"1\", \"true\", \"yes\"):/    if v == \"all\":/' app/backend/pdf_checks.py && sed -i \"s/'all' (or '1') = every page/'all' = every page/\" app/backend/pdf_checks.py && .venv/bin/python -m pytest -q tests/unit/test_pdf_hidden.py 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T04:22:13.697Z

**tool result (error)**
````
Exit code 1
sed: 1: "app/backend/pdf_checks.py
": command a expects \ followed by text
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:15.402Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/pdf_checks.py\"\ns=open(p).read()\ns=s.replace('    if v in (\"all\", \"1\", \"true\", \"yes\"):','    if v == \"all\":').replace(\"'all' (or '1') = every page\",\"'all' = every page\")\nopen(p,\"w\").write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_pdf_hidden.py 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T04:22:16.288Z

**tool result**
````
.................                                                        [100%]
17 passed in 0.43s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:17.059Z

Now OCR tests.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:34.689Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/test_pdf_ocr.py <<'E'\n\"\"\"T-086: local OCR of scanned PDF pages. Tests that need the Tesseract binary skip cleanly when it is not installed; the rest\n(missing-binary message, TSV parsing, low-confidence rule, needs_review marking) run everywhere. All text is SYNTHETIC.\"\"\"\nimport shutil\n\nimport pytest\n\nfrom app.backend import pdf_checks, pdf_ocr, pdf_text\nfrom tests.unit._pdf_raw import build, scanned_copy, text_page\n\npytest.importorskip(\"pypdfium2\")\nneeds_tesseract = pytest.mark.skipif(not shutil.which(\"tesseract\"), reason=\"tesseract is not installed\")\n\nLINES = [\"SYNTHETIC CLINIC NOTE\", \"Date: 03/04/2023\", \"Patient reports neck pain.\", \"Charge: $1,250.00 for MRI cervical spine.\"]\n\n\ndef scan_pdf():\n    return scanned_copy(build(text_page(LINES, size=18, lead=30, y=700)))\n\n\n# ---- no tesseract: a clear message, never a crash ----\ndef test_missing_tesseract_gives_a_clear_message(monkeypatch):\n    monkeypatch.setattr(pdf_ocr.shutil, \"which\", lambda name: None)\n    st = pdf_ocr.ocr_status()\n    assert st[\"available\"] is False and \"brew install tesseract\" in st[\"message\"] and \"apt-get install tesseract-ocr\" in st[\"message\"]\n    with pytest.raises(pdf_ocr.OcrUnavailable):\n        pdf_ocr.ocr_png(b\"x\")\n\n\ndef test_ocr_requested_without_tesseract_is_a_pdf_error_with_the_message_not_a_crash(monkeypatch):\n    monkeypatch.setattr(pdf_ocr.shutil, \"which\", lambda name: None)\n    with pytest.raises(pdf_text.PdfError) as e:\n        pdf_checks.extract(scan_pdf(), ocr=True)\n    assert e.value.code == \"ocr_unavailable\" and \"Tesseract\" in e.value.detail[\"message\"]\n\n\ndef test_scanned_pdf_without_ocr_is_refused_and_says_ocr_could_read_it():\n    with pytest.raises(pdf_text.PdfError) as e:\n        pdf_text.extract(scan_pdf())\n    assert e.value.code == \"pdf_no_text_layer\" and e.value.detail[\"scanned_pages\"] == [1]\n    assert \"available\" in e.value.detail[\"ocr\"]\n\n\n# ---- parsing and the low-confidence rule (no binary needed) ----\nTSV = (\"level\\tpage_num\\tblock_num\\tpar_num\\tline_num\\tword_num\\tleft\\ttop\\twidth\\theight\\tconf\\ttext\\n\"\n       \"1\\t1\\t0\\t0\\t0\\t0\\t0\\t0\\t100\\t100\\t-1\\t\\n\"\n       \"5\\t1\\t1\\t1\\t1\\t1\\t0\\t0\\t10\\t10\\t96.5\\tPatient\\n\"\n       \"5\\t1\\t1\\t1\\t1\\t2\\t0\\t0\\t10\\t10\\t41.0\\treports\\n\"\n       \"5\\t1\\t1\\t1\\t2\\t1\\t0\\t0\\t10\\t10\\t90.0\\tpain\\n\"\n       \"5\\t1\\t2\\t1\\t1\\t1\\t0\\t0\\t10\\t10\\t95.0\\t$1,250.00\\n\"\n       \"5\\t1\\t2\\t1\\t1\\t2\\t0\\t0\\t10\\t10\\t75.0\\t03/04/2023\\n\")\n\n\ndef test_tsv_rebuilds_lines_and_exact_word_offsets():\n    got = pdf_ocr._parse_tsv(TSV)\n    assert got[\"text\"] == \"Patient reports\\npain\\n\\n$1,250.00 03/04/2023\"\n    for w in got[\"words\"]:\n        assert got[\"text\"][w[\"start\"]:w[\"end\"]] == w[\"text\"]\n\n\ndef test_low_confidence_words_are_marked_numbers_need_more_confidence():\n    words = pdf_ocr._parse_tsv(TSV)[\"words\"]\n    low = [w[\"text\"] for w in words if pdf_ocr.is_low(w)]\n    assert low == [\"reports\", \"03/04/2023\"]            # 41 < 60; a date at 75 < 80 because it has digits; \"pain\" at 90 is fine\n\n\n# ---- OCR-derived items are always needs_review ----\ndef test_ocr_items_become_needs_review_with_the_reason_and_stay_that_way():\n    pages = [{\"page\": 1, \"start\": 0, \"end\": 50}, {\"page\": 2, \"start\": 52, \"end\": 100, \"source\": \"ocr\"}]\n    recs = [{\"n\": 1, \"char_start\": 0, \"char_end\": 40}, {\"n\": 2, \"char_start\": 52, \"char_end\": 90}]\n    items = [{\"id\": \"e1\", \"record_ids\": [\"r1\"], \"state\": \"verified\", \"reasons\": [], \"why\": \"\"},\n             {\"id\": \"e2\", \"record_ids\": [\"r2\"], \"state\": \"verified\", \"reasons\": [], \"why\": \"\", \"ladder\": {\"state\": \"verified\"}},\n             {\"id\": \"a2\", \"record_ids\": [\"r2\"], \"state\": \"rejected\", \"reasons\": [\"SCHEMA_INVALID\"], \"why\": \"x\"},\n             {\"id\": \"f2\", \"record_ids\": [\"r1\", \"r2\"], \"state\": \"needs_review\", \"reasons\": [\"LLM_ONLY\"], \"why\": \"ai only\"}]\n    assert pdf_checks.mark_ocr_items(items, recs, pages, \"Read by OCR.\") == 2\n    assert items[0][\"state\"] == \"verified\"\n    assert items[1][\"state\"] == \"needs_review\" and items[1][\"reasons\"] == [\"OCR_DERIVED\"] and items[1][\"ladder\"][\"state\"] == \"needs_review\"\n    assert items[2][\"state\"] == \"rejected\" and items[2][\"reasons\"] == [\"SCHEMA_INVALID\"]\n    assert items[3][\"reasons\"] == [\"LLM_ONLY\", \"OCR_DERIVED\"] and items[3][\"why\"] == \"ai only Read by OCR.\"\n    assert pdf_checks.mark_ocr_items(items, recs, pages, \"Read by OCR.\") == 2 and items[3][\"reasons\"].count(\"OCR_DERIVED\") == 1\n\n\ndef test_no_ocr_page_means_no_change():\n    items = [{\"id\": \"e\", \"record_ids\": [\"r1\"], \"state\": \"verified\", \"reasons\": []}]\n    assert pdf_checks.mark_ocr_items(items, [{\"n\": 1, \"char_start\": 0, \"char_end\": 9}], [{\"page\": 1, \"start\": 0, \"end\": 9}], \"x\") == 0\n    assert items[0][\"state\"] == \"verified\"\n\n\n# ---- the real binary ----\n@needs_tesseract\ndef test_status_reports_the_installed_version():\n    st = pdf_ocr.ocr_status()\n    assert st[\"available\"] and st[\"version\"] and \"eng\" in st[\"languages\"]\n\n\n@needs_tesseract\ndef test_scanned_page_is_ocrd_locally_with_page_image_low_conf_and_page_marked():\n    got = pdf_checks.extract(scan_pdf(), ocr=True)\n    assert \"neck pain\" in got[\"text\"] and \"03/04/2023\" in got[\"text\"]\n    pg = got[\"pages\"][0]\n    assert pg[\"source\"] == \"ocr\" and pg[\"has_image\"] and pg[\"mean_conf\"] > 60\n    assert got[\"page_images\"][1].startswith(\"iVBOR\")                           # base64 PNG beside the OCR text\n    for w in pg[\"low_conf\"]:\n        assert got[\"text\"][w[\"start\"]:w[\"end\"]] == w[\"text\"] and w[\"conf\"] < pdf_ocr.LOW_CONF_NUMBER\n    o = got[\"pdf_checks\"][\"ocr\"]\n    assert o[\"ran\"] and o[\"pages\"] == [1] and o[\"items_need_review\"] and o[\"engine\"].startswith(\"tesseract\")\n    assert o[\"low_conf_words\"] == pg[\"low_conf_count\"]\n\n\n@needs_tesseract\ndef test_garbled_scan_marks_low_confidence_words():\n    import random\n    rnd = random.Random(7)\n    base = scanned_copy(build(text_page(LINES, size=18, lead=30, y=700)))\n    # noise: flip a share of the pixels of the embedded image\n    import zlib\n    head, rest = base.split(b\"stream\\n\", 2)[0:1][0], base\n    st = pdf_ocr.ocr_status()\n    assert st[\"available\"]\n    got = pdf_checks.extract(base, ocr=True)\n    assert got[\"pages\"][0][\"source\"] == \"ocr\"\n    # degrade: render the page small (6 pt effective) so the engine is unsure\n    tiny = scanned_copy(build(text_page(LINES, size=5, lead=7, y=700)), scale=1.0)\n    g2 = pdf_checks.extract(tiny, ocr=True) if True else None\n    assert g2[\"pdf_checks\"][\"ocr\"][\"low_conf_words\"] >= 0\n\n\n@needs_tesseract\ndef test_too_many_scanned_pages_are_refused_not_partly_read(monkeypatch):\n    monkeypatch.setattr(pdf_ocr, \"MAX_OCR_PAGES\", 0)\n    with pytest.raises(pdf_text.PdfError) as e:\n        pdf_checks.extract(scan_pdf(), ocr=True)\n    assert e.value.code == \"ocr_too_many_pages\"\nE\n.venv/bin/python -m pytest -q tests/unit/test_pdf_ocr.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:22:36.069Z

**tool result**
````
...........                                                              [100%]
11 passed in 0.93s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:39.495Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nfrom tests.unit._pdf_raw import *\nfrom app.backend import pdf_checks\nL=[\"SYNTHETIC CLINIC NOTE\", \"Date: 03/04/2023\", \"Patient reports neck pain.\", \"Charge: $1,250.00 for MRI cervical spine.\"]\nfor sz,sc in ((18,2.0),(18,0.7),(9,0.7),(9,1.0),(7,0.6)):\n    d=scanned_copy(build(text_page(L,size=sz,lead=sz*1.6,y=700)),scale=sc)\n    g=pdf_checks.extract(d,ocr=True)\n    print(sz,sc,g[\"pages\"][0][\"mean_conf\"],g[\"pages\"][0][\"low_conf_count\"],repr(g[\"text\"][:100]), [w[\"text\"] for w in g[\"pages\"][0][\"low_conf\"]])\nE"
}
````

### User / tool · 2026-11-02T04:22:40.789Z

**tool result**
````
18 2.0 96.2 0 'SYNTHETIC CLINIC NOTE\n\nDate: 03/04/2023\n\nPatient reports neck pain.\n\nCharge: $1,250.00 for MRI cervi' []
18 0.7 93.5 0 'SYNTHETIC CLINIC NOTE\n\nDate: 03/04/2023\n\nPatient reports neck pain.\n\nCharge: $1,250.00 for MRI cervi' []
9 0.7 38.0 12 'SYNTHETIC CLINIC NOTE\nDate COS\nPalace repent reich, put,\n\n(Chaege: $1,250.00 for MR cervical spin.' ['CLINIC', 'Date', 'COS', 'Palace', 'repent', 'reich,', 'put,', '(Chaege:', '$1,250.00', 'MR', 'cervical', 'spin.']
9 1.0 93.4 0 'SYNTHETIC CLINIC NOTE\n\nDate: 03/04/2023\n\nPatient reports neck pain.\n\n(Charge: $1,250.00 for MRI cerv' []
7 0.6 35.0 14 'TENTH CLS MOTE\n\nBaie CELTS\n\nFaker rms by ord cae\n\n(habe 0 SRC MAP il' ['TENTH', 'CLS', 'Baie', 'CELTS', 'Faker', 'rms', 'by', 'ord', 'cae', '(habe', '0', 'SRC', 'MAP', 'il']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:44.768Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"tests/unit/test_pdf_ocr.py\"\ns=open(p).read()\na=s.index(\"@needs_tesseract\\ndef test_garbled_scan\")\nb=s.index(\"@needs_tesseract\\ndef test_too_many\")\ns=s[:a]+'''@needs_tesseract\ndef test_a_poor_scan_marks_its_unsure_words_and_a_clean_scan_marks_none():\n    clean = pdf_checks.extract(scan_pdf(), ocr=True)[\"pages\"][0]\n    assert clean[\"low_conf_count\"] == 0\n    poor = pdf_checks.extract(scanned_copy(build(text_page(LINES, size=9, lead=14, y=700)), scale=0.7), ocr=True)\n    pg = poor[\"pages\"][0]\n    assert pg[\"mean_conf\"] < 70 and pg[\"low_conf_count\"] >= 5\n    assert all(poor[\"text\"][w[\"start\"]:w[\"end\"]] == w[\"text\"] for w in pg[\"low_conf\"])\n    assert poor[\"pdf_checks\"][\"ocr\"][\"low_conf_words\"] == pg[\"low_conf_count\"]\n\n\n'''+s[b:]\nopen(p,\"w\").write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_pdf_ocr.py 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T04:22:46.117Z

**tool result**
````
...........                                                              [100%]
11 passed in 0.97s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:50.208Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport re\ndef edit(p, old, new, count=1):\n    s=open(p).read()\n    assert s.count(old)==count, (p, old, s.count(old))\n    open(p,\"w\").write(s.replace(old,new))\nedit(\"app/backend/confidence.py\", '\"INJECTION_SUSPECTED\", \"LLM_FAILED_AFTER_RETRIES\", \"CONFLICT_CHECK_INCOMPLETE\", \"LLM_SPLIT\",\\n)', '\"INJECTION_SUSPECTED\", \"LLM_FAILED_AFTER_RETRIES\", \"CONFLICT_CHECK_INCOMPLETE\", \"LLM_SPLIT\", \"OCR_DERIVED\",\\n)')\nE\ngit diff app/backend/confidence.py | head -20; git diff app/backend/why.py | head; grep -n \"LLM_SPLIT\\|INJECTION_SUSPECTED\" memory/contracts/api.md | tail -5"
}
````

### User / tool · 2026-11-02T04:22:50.362Z

**tool result**
````
diff --git a/app/backend/confidence.py b/app/backend/confidence.py
index 640a4e6..65460a9 100644
--- a/app/backend/confidence.py
+++ b/app/backend/confidence.py
@@ -8,7 +8,7 @@ REASON_CODES = (
     "HIGHLIGHT_NOT_FOUND", "JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE",
     "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
     "AMOUNT_ESTIMATE", "AMOUNT_DAMAGES", "AMOUNT_UNCLEAR", "LEXICON_ONLY", "LLM_ONLY", "SPLIT_AMBIGUOUS",
-    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT",
+    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT", "OCR_DERIVED",
 )
 REJECTED_CODES = frozenset({"GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"})
 STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}
73:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
218:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
533:- **entry (and a reviewer-written entry):** `extracted` (llm; a reviewer-written entry shows kind `human` and no model), `excerpt_verbatim` (code, `GROUNDING_EXCERPT_NOT_VERBATIM`), `excerpt_whole_sentence` (code, `EXCERPT_NOT_WHOLE_SENTENCE`), `excerpt_hedge` (code, `EXCERPT_OMITS_QUALIFIER`), `summary_tokens` (code, D-034, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `evidence.tokens`), `summary_qualifier` (code, D-022, `SUMMARY_DROPS_QUALIFIER`), `highlight` (code, `HIGHLIGHT_NOT_FOUND`), `date_confirmed` (code, D-041, `DATE_AMBIGUOUS`/`DATE_MISSING`, `blocks_export`), `injection_scan` (code, `INJECTION_SUSPECTED`), `judge_1` (llm), `human`. If the quote fails the word-for-word check or the AI output was malformed, the checks between `extracted` and `highlight` and `judge_1` are `skipped` with that code.
632:| `LLM_SPLIT` | needs_review | the record's boundaries were chosen by the model (code-validated), because the paste had no recognisable record markers |
633:| `INJECTION_SUSPECTED` | needs_review | the item's record (or a cross-record pass in this case) carries an instruction-like-text warning |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:55.160Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\ndef edit(p, old, new, count=1):\n    s=open(p).read()\n    assert s.count(old)==count, (p, old, s.count(old))\n    open(p,\"w\").write(s.replace(old,new))\nedit(\"app/backend/why.py\",'''    \"LLM_FAILED_AFTER_RETRIES\": \"The AI step failed on all three attempts, so this record has no AI-made entry.\",\n}''','''    \"LLM_FAILED_AFTER_RETRIES\": \"The AI step failed on all three attempts, so this record has no AI-made entry.\",\n    \"OCR_DERIVED\": \"This record was read from a scanned page by OCR, which can misread letters and digits. Check it against the page image.\",\n}''')\nedit(\"memory/contracts/api.md\",\"| `INJECTION_SUSPECTED` | needs_review | the item's record (or a cross-record pass in this case) carries an instruction-like-text warning |\\n\",\n\"| `INJECTION_SUSPECTED` | needs_review | the item's record (or a cross-record pass in this case) carries an instruction-like-text warning |\\n| `OCR_DERIVED` | needs_review | the item's record lies on a page read by OCR (T-086); always needs_review, added by code after the model steps, never cleared by a judge or a date confirmation |\\n\")\nE\nsed -n 340,372p app/backend/trace.py; git diff --stat app/backend/trace.py"
}
````

### User / tool · 2026-11-02T04:22:55.282Z

**tool result**
````
              na("EDIT_QUOTE", {"item_id": row["id"]}))
    toks = cc.get("summary_tokens_not_in_excerpt") or []
    code_step("summary_tokens", "Numbers and dates in the summary are in the quote", "SUMMARY_TOKEN_NOT_IN_EXCERPT",
              "Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote.", "D-034", na("EDIT_SUMMARY", {"item_id": row["id"]}),
              evidence={"tokens": toks}, failed="SUMMARY_TOKEN_NOT_IN_EXCERPT" in R or bool(toks))
    code_step("summary_qualifier", "Summary keeps the quote's qualifiers", "SUMMARY_DROPS_QUALIFIER", "Every hedge, attribution, negation, side and approximation in the quote is in the summary.",
              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R)
    code_step("highlight", "Quote can be highlighted in the record", "HIGHLIGHT_NOT_FOUND", "The quote's position in the record was found, so it can be highlighted.", "row 4",
              na("READ_RECORD", {"record_id": rid}), failed="HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False)
    # date confirmed (D-041)
    unconf = review.date_unconfirmed(cx.conn, cx.case_id, "entry", row)
    live_pending = row["state"] != "rejected" and row["review_status"] == "pending"
    dev = {"date": {"record_id": rid, "date_raw": rec.get("date_raw"), "date_iso": rec.get("date_iso"), "date_status": rec.get("date_status"),
                    "candidates": rec.get("date_candidates") or []}}
    if unconf:
        code = "DATE_AMBIGUOUS" if rec.get("date_status") == "ambiguous" else "DATE_MISSING"
        nxt = na("CONFIRM_DATE", {"record_id": rid, "view": "dates_to_confirm"}) if code == "DATE_AMBIGUOUS" else na("READ_RECORD", {"record_id": rid})
        st.append(step("date_confirmed", "Date of service is confirmed", "code", FAIL, reason_text(code), reason=code, rule="D-041", evidence=dev,
                       next_action=nxt, blocks=live_pending))
    else:
        st.append(step("date_confirmed", "Date of service is confirmed", "code", PASS, "The date comes from the record's own header and is parsed or confirmed.",
                       rule="D-041", evidence=dev))
    # injection scan
    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED"), reason="INJECTION_SUSPECTED", rule="row 16",
                       evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid})))
    else:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16"))
    # judge 1
    if stop:
        st.append(_skipped("judge_1", "Second AI check: is the summary supported by the quote?", "llm", stop, "row 4"))
    else:
        st.append(_judge_step(cx, row["id"], lad.get("judge"), "j1", R))
 app/backend/trace.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:00.920Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def step\\|^def _skipped\\|^def na\\|    def na\\|def code_step\" -A6 app/backend/trace.py | head -50; sed -n 404,412p app/backend/trace.py; sed -n 440,456p app/backend/trace.py; grep -n \"TRACE_WHY\" app/backend/trace.py | head -3"
}
````

### User / tool · 2026-11-02T04:23:01.063Z

**tool result**
````
87:def na(code: str, target: dict = None, options: list = None) -> dict:
88-    d = {"code": code, "text": _NEXT[code]}
89-    if target:
90-        d["target"] = target
91-    if options:
92-        d["options"] = options
93-    return d
--
96:def step(sid, label, kind, status, why_text, *, reason=None, rule=None, evidence=None, next_action=None, blocks=False, **extra):
97-    return {"id": sid, "label": label, "kind": kind, "status": status, "why": why_text, "reason_code": reason, "rule": rule,
98-            "blocks_export": bool(blocks), "evidence": evidence or {}, "next_action": next_action, **extra}
99-
100-
101-def _number(steps):
102-    for i, s in enumerate(steps, 1):
--
241:def _skipped(sid, label, kind, code, rule=None, rule_text=None):
242-    msg = rule_text or {"GROUNDING_EXCERPT_NOT_VERBATIM": "Not run: the quote did not pass the word-for-word check.",
243-                        "GROUNDING_AMOUNT_NOT_IN_TEXT": "Not run: the amount is not in the record text.",
244-                        "SCHEMA_INVALID": "Not run: the AI answer was malformed."}.get(code, "Not run because an earlier step rejected this item.")
245-    return step(sid, label, kind, SKIPPED, msg, reason=code, rule=rule)
246-
247-
--
321:    def code_step(sid, label, code, ok_text, rule, fail_na, evidence=None, failed=None):
322-        if stop:
323-            st.append(_skipped(sid, label, "code", stop, rule))
324-        elif failed if failed is not None else code in R:
325-            st.append(step(sid, label, "code", FAIL, reason_text(code), reason=code, rule=rule, evidence=evidence, next_action=fail_na))
326-        else:
327-            st.append(step(sid, label, "code", PASS, ok_text, rule=rule, evidence=evidence))
                           evidence={"values": vals}, next_action=na("READ_RECORD", {"record_id": rid})))
        else:
            code = _AMOUNT_CODE[kind]
            st.append(step("amount_class", "Rule says what the figure is", "code", PASS, reason_text(code), reason=code, rule="row 7", evidence={"values": vals}))
    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED") + " An amount from such a record cannot become a charge.",
                       reason="INJECTION_SUSPECTED", rule="row 16", evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid})))
    else:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16"))
    ftype, origin, cat = row["type"], row["origin"], row["category"]
    recs = cx.recs
    spans = [{"record_id": e["record_id"], "start": e["start"], "end": e["end"], "text": e["excerpt"]} for e in present._evidence(row.get("evidence"), recs)]
    rids = [s["record_id"] for s in spans if s["record_id"]]
    rid0 = rids[0] if rids else None
    st = []
    injected = any(recs.get(r, {}).get("injection_tag") for r in rids) or "INJECTION_SUSPECTED" in R

    def inj():
        if injected:
            return step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED"), reason="INJECTION_SUSPECTED", rule="row 16",
                        next_action=na("READ_RECORD", {"record_id": rid0}))
        return step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16")
    if ftype == "record_warning":
        code = {"injection_suspected": "INJECTION_SUSPECTED", "analysis_incomplete": "CONFLICT_CHECK_INCOMPLETE", "llm_split": "LLM_SPLIT", "date_ambiguous": "DATE_AMBIGUOUS"}.get(cat) \
            or next(iter(R), None)
        st.append(step("record_warning_check", "Code check on the record or the run", "code", FAIL, reason_text(code) if code else row["explanation"], reason=code,
40:TRACE_WHY = {
79:    if code in TRACE_WHY:
80:        return TRACE_WHY[code]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:03.588Z

**tool call — Bash**
````
{
 "command": "grep -n \"inj()\" app/backend/trace.py"
}
````

### User / tool · 2026-11-02T04:23:03.680Z

**tool result**
````
448:    def inj():
477:        st.append(inj())
524:    st.append(inj())
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:08.336Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/trace.py\"\ns=open(p).read()\ndef rep(old,new):\n    global s\n    assert s.count(old)==1,(old,s.count(old)); s=s.replace(old,new)\nrep('''def _number(steps):''','''def _ocr_steps(R, rid) -> list:\n    \"\"\"T-086: the step that holds an OCR-read item for review. Only present when the item carries OCR_DERIVED, so other cases are unchanged.\"\"\"\n    if \"OCR_DERIVED\" not in R:\n        return []\n    return [step(\"ocr_source\", \"Record was not read from a scanned page\", \"code\", FAIL, reason_text(\"OCR_DERIVED\"), reason=\"OCR_DERIVED\", rule=\"D-042\",\n                 evidence={\"values\": {\"record_id\": rid}}, next_action=na(\"READ_RECORD\", {\"record_id\": rid}))]\n\n\ndef _number(steps):''')\n# entry\nrep('''        st.append(step(\"injection_scan\", \"Record has no instruction-like text\", \"code\", PASS, \"The record has no instruction-like text.\", rule=\"row 16\"))\n    # judge 1''','''        st.append(step(\"injection_scan\", \"Record has no instruction-like text\", \"code\", PASS, \"The record has no instruction-like text.\", rule=\"row 16\"))\n    st += _ocr_steps(R, rid)\n    # judge 1''')\n# amount\nrep('''        st.append(step(\"injection_scan\", \"Record has no instruction-like text\", \"code\", PASS, \"The record has no instruction-like text.\", rule=\"row 16\"))\n    ftype, origin, cat''','''        st.append(step(\"injection_scan\", \"Record has no instruction-like text\", \"code\", PASS, \"The record has no instruction-like text.\", rule=\"row 16\"))\n    ftype, origin, cat''') if False else None\nopen(p,\"w\").write(s)\nE\nsed -n 412,425p app/backend/trace.py; sed -n 478,490p app/backend/trace.py; sed -n 528,536p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T04:23:08.464Z

**tool result**
````
            st.append(step("amount_class", "Rule says what the figure is", "code", FAIL, reason_text("AMOUNT_UNCLEAR"), reason="AMOUNT_UNCLEAR", rule="row 7",
                           evidence={"values": vals}, next_action=na("READ_RECORD", {"record_id": rid})))
        else:
            code = _AMOUNT_CODE[kind]
            st.append(step("amount_class", "Rule says what the figure is", "code", PASS, reason_text(code), reason=code, rule="row 7", evidence={"values": vals}))
    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED") + " An amount from such a record cannot become a charge.",
                       reason="INJECTION_SUSPECTED", rule="row 16", evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid})))
    else:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16"))
    if gfail:
        st.append(_skipped("judge_2", "Second AI check: is this figure a charge, rate or estimate?", "llm", "GROUNDING_AMOUNT_NOT_IN_TEXT", "row 7"))
    elif kind == "damages":
        st.append(step("judge_2", "Second AI check: is this figure a charge, rate or estimate?", "llm", SKIPPED, "Damages and other non-bill figures are not sent to the second check.",
                       reason_text("GROUNDING_EXCERPT_NOT_VERBATIM") if bad else "Every cited date line is in the record, character for character.",
                       reason="GROUNDING_EXCERPT_NOT_VERBATIM" if bad else None, rule="row 10", evidence={"spans": spans},
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"]) if bad else None))
        if "ENDPOINT_NOT_VERIFIED" in R:
            st.append(step("endpoints_confirmed", "Dates at both ends are confirmed", "code", FAIL, reason_text("ENDPOINT_NOT_VERIFIED"), reason="ENDPOINT_NOT_VERIFIED", rule="row 9",
                           next_action=na("CONFIRM_DATE", {"view": "dates_to_confirm"})))
        else:
            st.append(step("endpoints_confirmed", "Dates at both ends are confirmed", "code", PASS, "Both dates are parsed or confirmed.", rule="row 9"))
        st.append(inj())
        st.append(step("judge_not_needed", "Second AI check", "llm", SKIPPED, "Not needed: this is arithmetic over dates in the record, which code does exactly.", rule="row 9"))
        st.append(_human_step(cx, row, "flag"))
        return st
    has_llm, has_lex = origin in ("llm", "lexicon+llm"), origin in ("lexicon", "lexicon+llm")
        if "HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False or any(s["start"] is None for s in spans):
            st.append(step("highlight", "Quote can be highlighted in the record", "code", FAIL, reason_text("HIGHLIGHT_NOT_FOUND"), reason="HIGHLIGHT_NOT_FOUND", rule="row 4",
                           next_action=na("READ_RECORD", {"record_id": rid0})))
        else:
            st.append(step("highlight", "Quote can be highlighted in the record", "code", PASS, "The quote's position in the record was found.", rule="row 4"))
    st.append(inj())
    jid = "j3" if ftype == "conflict" else "j4"
    if vfail:
        st.append(_skipped(f"judge_{jid[1]}", f"Second AI check: {JUDGE_LABEL[jid].lower()}", "llm", "GROUNDING_EXCERPT_NOT_VERBATIM", "row 11" if jid == "j3" else "row 12"))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:12.024Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/trace.py\"\ns=open(p).read()\ndef rep(old,new):\n    global s\n    assert s.count(old)==1,(old[:60],s.count(old)); s=s.replace(old,new)\nrep('''        st.append(step(\"injection_scan\", \"Record has no instruction-like text\", \"code\", PASS, \"The record has no instruction-like text.\", rule=\"row 16\"))\n    if gfail:''','''        st.append(step(\"injection_scan\", \"Record has no instruction-like text\", \"code\", PASS, \"The record has no instruction-like text.\", rule=\"row 16\"))\n    st += _ocr_steps(R, rid)\n    if gfail:''')\nrep('''        st.append(inj())\n        st.append(step(\"judge_not_needed\"''','''        st.append(inj())\n        st += _ocr_steps(R, rid0)\n        st.append(step(\"judge_not_needed\"''')\nrep('''    st.append(inj())\n    jid = \"j3\" if ftype''','''    st.append(inj())\n    st += _ocr_steps(R, rid0)\n    jid = \"j3\" if ftype''')\nopen(p,\"w\").write(s)\nE\ngrep -n \"\\\"OCR_DERIVED\\\"\" app/backend/trace.py | head; sed -n 100,125p app/backend/trace.py | grep -n \"_STEP_OF_REASON\" ; grep -n \"INJECTION_SUSPECTED\\\": \\\"injection_scan\\\"\" app/backend/trace.py"
}
````

### User / tool · 2026-11-02T04:23:12.179Z

**tool result**
````
103:    if "OCR_DERIVED" not in R:
105:    return [step("ocr_source", "Record was not read from a scanned page", "code", FAIL, reason_text("OCR_DERIVED"), reason="OCR_DERIVED", rule="D-042",
71:    "INJECTION_SUSPECTED": "injection_scan", "LLM_FAILED_AFTER_RETRIES": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:15.602Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/trace.py\"\ns=open(p).read()\nold='\"INJECTION_SUSPECTED\": \"injection_scan\", \"LLM_FAILED_AFTER_RETRIES\": \"extracted\",'\nassert s.count(old)==1\ns=s.replace(old,'\"INJECTION_SUSPECTED\": \"injection_scan\", \"OCR_DERIVED\": \"ocr_source\", \"LLM_FAILED_AFTER_RETRIES\": \"extracted\",')\nopen(p,\"w\").write(s)\nE\ngit diff app/backend/pipeline.py | head -60; sed -n 322,340p app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T04:23:15.753Z

**tool result**
````
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index 2426a4d..c3a026c 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -1,7 +1,7 @@
 """Pipeline stages 0-7 (app/README-arch.md; ADR-007, ADR-010, ADR-011, ADR-013, ADR-014). `python -m app.pipeline <file>` prints the result.
 
 0 ingest (code, sync)  1 extract (LLM)  2 verify (code)  3 judge_entries (J1)  4 amounts (J2 on every amount)
-5 conflicts (one LLM pair pass + J3)  6 flags (one LLM pass per record + lexicon floor + J4)  7 finalize (code).
+5 conflicts (code proposes the pairs, J3 classifies each)  6 flags (one LLM pass per record + lexicon floor + J4)  7 finalize (code).
 Gaps, the accident-date conflict, provider-name conflicts, amounts and record warnings exist after stage 0 and never wait for a model.
 No code path here sets review_status: every item leaves a run `pending`. A model failure loses only that item and is reported in `errors`.
 `call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is the audited wrapper bound to a case (or a test fake)."""
@@ -12,7 +12,7 @@ import time
 from concurrent.futures import ThreadPoolExecutor
 
 from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
-                         judges, split_llm, totals as TT, why as WHY)
+                         judges, language, split_llm, totals as TT, why as WHY)
 from app.db import db as DB
 from app.llm import audited as AU, provider as P
 
@@ -50,7 +50,8 @@ def run_ingest(raw_text: str, call=None, not_duplicates=(), splitter=None) -> di
     fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
     ing = IN.ingest(raw_text, splitter=splitter or (split_llm.make_splitter(call) if call else None), not_duplicates=not_duplicates)
     text = IN.normalize_text(raw_text)
-    recs = ing["records"]
+    recs = language.annotate(ing["records"])           # D-042: en | es | other per record; raises UnsupportedLanguage when no record is readable
+    language.case_check(recs)
     by_n = {r["n"]: r for r in recs}
     backend = P.backend_name()
     flags = []
@@ -87,7 +88,7 @@ def run_ingest(raw_text: str, call=None, not_duplicates=(), splitter=None) -> di
     for a in AM.extract_amounts(recs, separate=sep):
         item = amount_item(a, by_n[a["record_no"]])
         (damages if a["cls"] == "damages" else amounts).append(item)
-    warnings = list(ing["warnings"])
+    warnings = list(ing["warnings"]) + language.record_warnings(recs)
     for r in recs:
         if r["injection_tag"]:
             warnings.append({"code": "INJECTION_SUSPECTED", "record_no": r["n"], "item_id": r["id"],
@@ -186,8 +187,11 @@ def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
     table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
     existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
     for it in items:
-        row = _row(kind, it)
         old = existing.get(it["id"])
+        if kind == "amount" and old is not None:        # T-084: a rerun keeps the class the paralegal gave a figure
+            from app.backend import reclassify as RC
+            it = RC.carry_over(old, it)
+        row = _row(kind, it)
         if old is None:
             DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
             continue
@@ -268,7 +272,11 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
         return clock() - t0 > deadline_s
 
     DB.update_case(conn, cid, status="running", stage="ingest", run_started_at=t0, error=None, backend=P.backend_name())
-    ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid), splitter=_frozen_splitter(conn, cid))
+    try:
    # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T-094). No model search, so the candidate set cannot vary.
    llm_flags = []
    distinct = [by_n[g[0]] for g in ing["groups"] if by_n[g[0]].get("lang") != "other"]     # unsupported-language records are skipped (warning + error)
    if guard("conflicts"):
        llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
    # 6: per-record flags (one call per distinct record) + J4
    if guard("flags"):
        year = _accident_year(recs)

        def one(r):
            if expired():                    # the deadline also applies inside the stage, record by record
                return r, None
            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
            per = list(ex.map(one, distinct))
        for r, fs in per:
            if fs is None or expired():
                timed_out = True
                continue
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:21.655Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/pipeline.py\"\ns=open(p).read()\nold='''    now_t = clock()\n    _persist(conn, cid, \"entry\",'''\nassert s.count(old)==1\nnew='''    from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said\n    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get(\"config\") or {}).get(\"pages\")), WHY.why(\"OCR_DERIVED\"))\n    now_t = clock()\n    _persist(conn, cid, \"entry\",'''\ns=s.replace(old,new)\nopen(p,\"w\").write(s)\nE\ngit diff app/backend/api.py app/backend/present.py | head -80"
}
````

### User / tool · 2026-11-02T04:23:21.789Z

**tool result**
````
diff --git a/app/backend/api.py b/app/backend/api.py
index 4edd585..1235998 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -20,7 +20,7 @@ from starlette.exceptions import HTTPException as StarletteHTTPException
 
 from starlette.concurrency import run_in_threadpool
 
-from app.backend import case_extras, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
+from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
 from app.db import db as DB
 
 MAX_BODY_BYTES = 512 * 1024      # cheap rejection before the 60,000-character rule: UTF-8 worst case plus JSON overhead
@@ -494,6 +494,11 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             c.close()
 
     case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
+    from app.backend import billing
+    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
+    from app.backend import reclassify
+    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
+    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
 
     @app.get("/api/cases/{token}/export")
     def export(token: str):
diff --git a/app/backend/present.py b/app/backend/present.py
index 01344f8..f9bc01f 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -1,7 +1,7 @@
 """Read-side views in the shapes of memory/contracts/api.md, built from the DB. No writes."""
 import json
 
-from app.backend import confidence, grounding, pdf_text, sentences, store, totals as T, why
+from app.backend import confidence, date_convention, grounding, pdf_text, sentences, store, totals as T, why
 from app.db import db as DB
 
 STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
@@ -123,8 +123,11 @@ def review_view(conn, case_id):
 
 
 def dates_to_confirm(conn, case_id):
-    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"]}
-            for r in _recs_by_id(conn, case_id).values() if r["date_status"] in ("ambiguous", "missing")]
+    recs = list(_recs_by_id(conn, case_id).values())
+    raw = DB.get_case(conn, case_id)["raw_text"]
+    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"],
+             "suggestion": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)
+            for r in recs if r["date_status"] in ("ambiguous", "missing")]
 
 
 def record_view(r, raw, with_sentences=True, pages=None):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:25.627Z

**tool call — Bash**
````
{
 "command": "sed -n 1,11p app/db/schema.sql"
}
````

### User / tool · 2026-11-02T04:23:25.711Z

**tool result**
````
-- T-050: item/record ids are short per-case ids (r1, e5, f_gap_r6_r7); uniqueness is (case_id, id), so many cases share one file.
-- ADR-002: seven tables, one SQLite file. All offsets are absolute into cases.raw_text. Money is integer cents.
-- *_json columns hold JSON text. Times are epoch seconds (REAL) supplied by the caller's injectable now().
CREATE TABLE IF NOT EXISTS cases (
  id TEXT PRIMARY KEY, name TEXT, source TEXT CHECK (source IN ('paste','sample')) DEFAULT 'paste',
  raw_text TEXT NOT NULL, text_sha256 TEXT,
  status TEXT NOT NULL DEFAULT 'ingested' CHECK (status IN ('ingested','running','ready','failed')),
  stage TEXT, error TEXT, backend TEXT, demo_mode INTEGER DEFAULT 0, config_json TEXT,
  injection_records_json TEXT, created_at REAL NOT NULL, run_started_at REAL, run_finished_at REAL
);
CREATE TABLE IF NOT EXISTS records (
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:30.672Z

**tool call — Bash**
````
{
 "command": "cat > app/backend/pdf_routes.py <<'E'\n\"\"\"GET /api/cases/{token}/pages/{n}/image (T-086): the scanned page beside its OCR text. The PNG was rendered at upload from the\nuser's own PDF and is stored with the case (config.page_images, base64), so it goes away with the case (DELETE or retention purge).\n`add_routes(app, conn=..., get_case=..., ApiError=...)`, the same shape as the other route modules.\"\"\"\nimport base64\nimport binascii\n\nfrom fastapi import Response\n\n\ndef add_routes(app, *, conn, get_case, ApiError):\n    @app.get(\"/api/cases/{token}/pages/{n}/image\")\n    def page_image(token: str, n: int):\n        c = conn()\n        try:\n            case = get_case(c, token)\n        finally:\n            c.close()\n        b64 = ((case.get(\"config\") or {}).get(\"page_images\") or {}).get(str(n))\n        if not b64:\n            raise ApiError(404, \"not_found\", \"No page image for that page.\")\n        try:\n            png = base64.b64decode(b64, validate=True)\n        except (binascii.Error, ValueError):\n            raise ApiError(404, \"not_found\", \"No page image for that page.\") from None\n        return Response(content=png, media_type=\"image/png\", headers={\"Cache-Control\": \"private, no-store\", \"X-Content-Type-Options\": \"nosniff\"})\nE\nsed -n 36,42p app/backend/api.py; sed -n 247,272p app/backend/api.py"
}
````

### User / tool · 2026-11-02T04:23:30.766Z

**tool result**
````
STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]
_ERR_STATUS = {"bad_request": 400, "input_too_large": 413}
_PDF_MESSAGES = {"pdf_no_text_layer": "This PDF has no text layer (it looks scanned). Scanned pages are not read; paste the text instead.",
                 "pdf_unreadable": "This file could not be read as a PDF.", "pdf_encrypted": "This PDF is password-protected and cannot be read.",
                 "pdf_too_large": "The PDF is too large."}



    @app.post("/api/cases/pdf", status_code=201)
    async def create_case_from_pdf(request: Request, name: str = None):
        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer only; a scanned PDF is refused before anything is stored or run."""
        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
            raise ApiError(413, "input_too_large", "The PDF is too large.")
        data = b""
        async for chunk in request.stream():
            data += chunk
            if len(data) > pdf_text.MAX_PDF_BYTES:
                raise ApiError(413, "input_too_large", "The PDF is too large.")
        try:       # parsing runs off the event loop (so /api/health stays responsive) under a time cap
            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data), pdf_text.EXTRACT_TIMEOUT_S)
        except asyncio.TimeoutError:
            raise ApiError(400, "bad_request", _PDF_MESSAGES["pdf_unreadable"], {"reason": "pdf_timeout"}) from None
        except pdf_text.PdfError as e:
            raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
                           _PDF_MESSAGES[e.code], {"reason": e.code}) from None
        return make_case(got["text"], name, False, pdf_pages=got["pages"])

    def make_case(text, name, sample, pdf_pages=None):
        try:
            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:35.122Z

**tool call — Bash**
````
{
 "command": "grep -rn \"Scanned pages are not read\\|looks scanned\" tests app/frontend memory/contracts | head; "
}
````

### User / tool · 2026-11-02T04:23:35.254Z

**tool result**
````
memory/contracts/api.md:77:Errors: `400 bad_request` with `detail.reason` = `pdf_no_text_layer` (looks scanned: refused before anything is stored, no model call), `pdf_unreadable`, `pdf_encrypted`; `413 input_too_large` (`pdf_too_large`).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:42.727Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/api.py\"\ns=open(p).read()\ndef rep(old,new):\n    global s\n    assert s.count(old)==1,(old[:70],s.count(old)); s=s.replace(old,new)\nrep('''                 \"pdf_too_large\": \"The PDF is too large.\"}\n''','''                 \"pdf_too_large\": \"The PDF is too large.\"}\nfrom app.backend import pdf_checks as _pdf_checks      # noqa: E402  (T-086/T-087)\n_PDF_MESSAGES.update(_pdf_checks.MESSAGES)\n''')\nrep('''    async def create_case_from_pdf(request: Request, name: str = None):\n        \"\"\"D-031: raw PDF bytes (Content-Type application/pdf). Text layer only; a scanned PDF is refused before anything is stored or run.\"\"\"''','''    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):\n        \"\"\"D-031: raw PDF bytes (Content-Type application/pdf). Text layer minus hidden text (T-087, `include_hidden`); a scanned PDF is\n        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086).\"\"\"''')\nrep('''        try:       # parsing runs off the event loop (so /api/health stays responsive) under a time cap\n            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data), pdf_text.EXTRACT_TIMEOUT_S)''','''        opts = {}\n        if (ocr or \"\").lower() in (\"1\", \"true\", \"yes\"):\n            opts[\"ocr\"] = True\n        if include_hidden:\n            opts[\"include_hidden\"] = include_hidden\n        try:       # parsing runs off the event loop (so /api/health stays responsive) under a time cap\n            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data, **opts), _pdf_checks.OCR_TIMEOUT_S if opts.get(\"ocr\") else pdf_text.EXTRACT_TIMEOUT_S)''')\nrep('''                           _PDF_MESSAGES[e.code], {\"reason\": e.code}) from None\n        return make_case(got[\"text\"], name, False, pdf_pages=got[\"pages\"])\n\n    def make_case(text, name, sample, pdf_pages=None):''','''                           (e.detail.get(\"message\") if e.code == \"ocr_unavailable\" else None) or _PDF_MESSAGES[e.code], {\"reason\": e.code, **e.detail}) from None\n        out = make_case(got[\"text\"], name, False, pdf_pages=got[\"pages\"], pdf_extra={\"pdf_checks\": got.get(\"pdf_checks\"), \"page_images\": got.get(\"page_images\") or None})\n        out[\"pdf_checks\"] = got.get(\"pdf_checks\")\n        return out\n\n    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None):''')\nrep('''**({\"config_json\": {\"source_pdf\": True, \"pages\": pdf_pages}} if pdf_pages else {}))''','''**({\"config_json\": {\"source_pdf\": True, \"pages\": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))''')\nrep('''    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083\n''','''    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083\n    from app.backend import pdf_routes\n    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text\n''')\nopen(p,\"w\").write(s)\nE\ngrep -n \"ApiError(413 if e.code\" -B1 -A3 app/backend/api.py"
}
````

### User / tool · 2026-11-02T04:23:42.873Z

**tool result**
````
273-        except pdf_text.PdfError as e:
274:            raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
275-                           (e.detail.get("message") if e.code == "ocr_unavailable" else None) or _PDF_MESSAGES[e.code], {"reason": e.code, **e.detail}) from None
276-        out = make_case(got["text"], name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None})
277-        out["pdf_checks"] = got.get("pdf_checks")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:47.298Z

**tool call — Bash**
````
{
 "command": "grep -n \"def record_view\" -A12 app/backend/present.py; grep -n \"return {\\\"token\\\": case_id, \\\"name\\\"\" -A14 app/backend/present.py"
}
````

### User / tool · 2026-11-02T04:23:47.408Z

**tool result**
````
133:def record_view(r, raw, with_sentences=True, pages=None):
134-    block = raw[r["char_start"]:r["char_end"]]
135-    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
136-         "date_status": r["date_status"], "date_candidates": r["date_candidates"] or [], "duplicate_of": r["duplicate_of"],
137-         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
138-         "char_end": r["char_end"], "text": block}
139-    if pages:                                    # PDF source (D-031): the page where the record starts
140-        v["page"] = pdf_text.page_for(pages, r["char_start"])
141-    if with_sentences:
142-        v["sentences"] = [{"text": block[a:b], "start": r["char_start"] + a, "end": r["char_start"] + b} for a, b in sentences.stripped_spans(block)]
143-    return v
144-
145-
160:    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
161-            "records": [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs], "undated_entries": undated, "entries": dated,
162-            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
163-            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "dates_to_confirm": dates_to_confirm(conn, case_id),
164-            "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
165-            "review": review_view(conn, case_id), "warnings": [], "error": err,
166-            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"])}
167-
168-
169-def why_view(conn, case_id, item_id):
170-    item = item_view(conn, case_id, item_id)
171-    recs = _recs_by_id(conn, case_id)
172-    ids = list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])
173-    seen, src = set(), []
174-    for rid in ids:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:55.523Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"app/backend/present.py\"\ns=open(p).read()\ndef rep(old,new):\n    global s\n    assert s.count(old)==1,(old[:70],s.count(old)); s=s.replace(old,new)\nrep('''        v[\"page\"] = pdf_text.page_for(pages, r[\"char_start\"])\n''','''        v[\"page\"] = pdf_text.page_for(pages, r[\"char_start\"])\n        from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR\n        v[\"ocr_derived\"] = pdf_checks.is_ocr_span(pages, r[\"char_start\"], r[\"char_end\"])\n''')\nrep('''            \"created_at\": store.iso(case[\"created_at\"]), \"updated_at\": store.iso(case.get(\"run_finished_at\") or case[\"created_at\"])}\n\n\ndef why_view''','''            \"created_at\": store.iso(case[\"created_at\"]), \"updated_at\": store.iso(case.get(\"run_finished_at\") or case[\"created_at\"]),\n            **{k: (case.get(\"config\") or {})[k] for k in (\"pdf_checks\",) if (case.get(\"config\") or {}).get(k)},     # T-086/T-087 (PDF cases only)\n            **({\"pdf_pages\": (case.get(\"config\") or {})[\"pages\"]} if (case.get(\"config\") or {}).get(\"pages\") else {})}\n\n\ndef why_view''')\nopen(p,\"w\").write(s)\nE\npython3 - <<'E'\np=\"/Users/arsis/zlayt-pm-project/requirements.txt\"\ns=open(p).read()\nprint(\"pypdf==\" in s)\nE\ncd /Users/arsis/zlayt-pm-project && git diff requirements.txt | head"
}
````

### User / tool · 2026-11-02T04:23:55.735Z

**tool result**
````
True
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:58.590Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"requirements.txt\"\ns=open(p).read()\nassert \"pypdfium2\" not in s and s.count(\"pypdf==6.21.4\\n\")==1\ns=s.replace(\"pypdf==6.21.4\\n\",\"pypdf==6.21.4\\npypdfium2==5.14.0\\n\")\nopen(p,\"w\").write(s)\nE\n.venv/bin/pip install pip-audit 2>&1 | tail -1; .venv/bin/pip-audit -r requirements.txt 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T04:24:15.178Z

**tool result**
````
[notice] To update, run: python3.12 -m pip install --upgrade pip
No known vulnerabilities found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:19.457Z

**tool call — Bash**
````
{
 "command": "grep -rln \"run_pipeline\" tests/unit | head; grep -n \"def test\" tests/unit/test_pipeline.py | head -5; sed -n 1,50p tests/unit/test_pipeline.py"
}
````

### User / tool · 2026-11-02T04:24:19.589Z

**tool result**
````
tests/unit/test_reclassify.py
tests/unit/test_t037_backend.py
tests/unit/test_dismissal_patterns.py
tests/unit/test_review_rules.py
tests/unit/test_conflict_candidates.py
tests/unit/test_narrative.py
tests/unit/test_multicase.py
tests/unit/_fakes.py
tests/unit/test_pipeline.py
tests/unit/test_split_llm.py
22:def test_stage_names_and_order():
26:def test_ingest_is_synchronous_code_with_gaps_and_no_llm():
34:def test_nine_entries_all_verified_with_code_set_provider_and_date(run):
43:def test_call_budget_about_forty(run):
49:def test_amounts_classified_by_code_and_totals(run):
"""Pipeline stages with a scripted fake `call` (no key, no network). app/README-arch.md stage list, R-IN-1, R-TL-1, R-FL-1, R-CH-*, ADR-007, LLM_VS_CODE rows 1-3, 9, 15."""
import pytest
from app.backend import pipeline as PL
from app.db import db as DB
from app.llm import audited as AU, provider as P
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, which_record, sample_script, run_sample, items_for

STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]

def script():
    return sample_script()

@pytest.fixture
def run(tmp_path):
    conn = DB.connect(str(tmp_path / "p.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    call = FakeCall(script())
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
    return out, call

def test_stage_names_and_order():
    """ADR-007 / README-arch: stages are exactly ingest, extract, verify, judge_entries, amounts, conflicts, flags, finalize."""
    assert list(PL.STAGES) == STAGES

def test_ingest_is_synchronous_code_with_gaps_and_no_llm():
    """Row 9 / arch: ingest returns records, dates, regex amounts and the gap flag without any LLM call."""
    out = PL.run_ingest(G.raw("sample"))
    assert len(out["records"]) == 9
    g = [f for f in out["flags"] if f["type"] == "gap"]
    assert [(f["from_date"], f["to_date"], f["days"]) for f in g] == [("2026-03-06", "2026-05-18", 73)]
    assert len(out["amounts"]) == 3

def test_nine_entries_all_verified_with_code_set_provider_and_date(run):
    """R-TL-1, R-TL-9: nine entries in date order; provider = header label and date = header date set by code; states verified."""
    out, _ = run
    ents = out["entries"]
    assert len(ents) == 9 and [e["date"] for e in ents] == sorted(e["date"] for e in ents)
    assert ents[3]["provider"] == "Capital PT, initial evaluation"
    assert ents[6]["date"] == "2026-05-18"
    assert all(e["state"] == "verified" and e["review_status"] == "pending" for e in ents)

def test_call_budget_about_forty(run):
    """ADR-003: about 40 calls on the sample (9 extract, 9 J1, 3 J2, conflicts, 9 flags, judges); never an unbounded loop."""
    _, call = run
    assert 30 <= len(call.log) <= 50
    assert call.steps().count("extract") == 9 and call.steps().count("flags") == 9 and call.steps().count("j1") == 9

def test_amounts_classified_by_code_and_totals(run):
    """R-CH-2/3: $6,240 and $2,150 charges, $185 rate (needs_review AMOUNT_RATE_NOT_TOTALED); nothing accepted yet so accepted total is 0."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:24.275Z

**tool call — Bash**
````
{
 "command": "sed -n 1,16p tests/unit/test_pdf_upload.py; sed -n 48,92p tests/unit/test_pdf_upload.py; sed -n 1,40p tests/unit/_fakes.py | head -60"
}
````

### User / tool · 2026-11-02T04:24:24.401Z

**tool result**
````
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

"""Scripted fake LLM `call` for pipeline/judge/flag tests. No key, no network (fixture-style, in memory)."""
import itertools, json, re
from tests.unit import _golden as G

_RUNS = itertools.count()

class FakeCall:
    """call(step, system, user, schema, *, item_id=None) -> (output, call_id). Records every prompt."""
    def __init__(self, script=None):
        self.script = script or {}
        self.log = []
    def __call__(self, step, system, user, schema, *, item_id=None):
        self.log.append(dict(step=step, system=system, user=user, item_id=item_id))
        out = self.script[step](user) if callable(self.script.get(step)) else self.script.get(step, {})
        if isinstance(out, Exception):
            raise out
        return out, f"call{len(self.log)}"
    def steps(self):
        return [l["step"] for l in self.log]
    def prompts(self, step):
        return [l["user"] for l in self.log if l["step"] == step]

def golden_summaries():
    """{record_no: (summary, quote)} from the golden letter block."""
    letter, _ = G.export_blocks()
    ex = G.expected("sample"); recs = {r["record_no"]: r for r in ex["records"]}
    from datetime import datetime
    out = {}
    for blk in letter.split("BILLED CHARGES")[0].strip().split("\n\n")[1:]:
        h, summ, src = blk.split("\n")
        m = re.match(r"([A-Z][a-z]+ \d+, \d{4}) — (.+)$", h)
        iso = datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        n = [k for k, r in recs.items() if r["source"] == m.group(2) and r["date"] == iso][0]
        out[n] = (summ, re.search(r'"(.+)"', src).group(1))
    return out

def which_record(user, case="sample"):
    """Record numbers whose excerpt appears in the prompt text."""
    return [r["n"] for r in G.records(case) if r["excerpt"] in user or r["excerpt"][:40] in user]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:25.390Z

Now the API integration tests.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:40.373Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/test_pdf_checks_api.py <<'E'\n\"\"\"T-086/T-087 over HTTP and through the pipeline: hidden text is kept out of the case until confirmed, OCR is opt-in and local, the page\nimage is served beside the OCR text, and every item on an OCR page is needs_review. SYNTHETIC text only.\"\"\"\nimport base64\nimport shutil\n\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import pipeline as PL\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit._fakes import FakeCall, sample_script\nfrom tests.unit._pdf_raw import build, scanned_copy, text_page\nfrom tests.unit.test_pdf_hidden import HIDDEN, VISIBLE, pdf_with\nfrom tests.unit.test_pdf_ocr import LINES, scan_pdf\n\npytest.importorskip(\"pypdfium2\")\nPDF = {\"content-type\": \"application/pdf\"}\nneeds_tesseract = pytest.mark.skipif(not shutil.which(\"tesseract\"), reason=\"tesseract is not installed\")\n\n\n@pytest.fixture\ndef client(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"claude-cli\")\n    monkeypatch.setenv(\"ENABLE_LIVE\", \"1\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    db = str(tmp_path / \"pc.sqlite\")\n    return db, TestClient(create_app(db, static_dir=str(tmp_path)))\n\n\ndef test_upload_excludes_hidden_text_reports_it_and_shows_it_again_on_the_case(client):\n    _, c = client\n    r = c.post(\"/api/cases/pdf\", content=pdf_with(\"white\", \"offpage\"), headers=PDF)\n    assert r.status_code == 201, r.text\n    b = r.json()\n    assert \"PLANTED\" not in \" \".join(x[\"text\"] for x in b[\"records\"])\n    ht = b[\"pdf_checks\"][\"hidden_text\"]\n    assert ht[\"pages\"][0][\"page\"] == 1 and ht[\"pages\"][0][\"count\"] == 2 and ht[\"pages\"][0][\"excluded\"]\n    view = c.get(f\"/api/cases/{b['token']}\").json()\n    assert view[\"pdf_checks\"][\"hidden_text\"][\"pages\"][0][\"count\"] == 2 and view[\"pdf_pages\"][0][\"page\"] == 1\n    assert all(x[\"ocr_derived\"] is False for x in view[\"records\"])\n\n\ndef test_confirming_the_page_includes_its_hidden_text(client):\n    _, c = client\n    r = c.post(\"/api/cases/pdf?include_hidden=1\", content=pdf_with(\"white\"), headers=PDF)\n    assert r.status_code == 201\n    b = r.json()\n    assert \"PLANTED white text\" in \" \".join(x[\"text\"] for x in b[\"records\"])\n    assert b[\"pdf_checks\"][\"hidden_text\"][\"pages\"][0][\"confirmed\"] is True\n\n\ndef test_a_pdf_with_nothing_hidden_has_an_empty_hidden_report(client):\n    _, c = client\n    b = c.post(\"/api/cases/pdf\", content=build(text_page([VISIBLE])), headers=PDF).json()\n    assert b[\"pdf_checks\"][\"hidden_text\"][\"checked\"] is True and b[\"pdf_checks\"][\"hidden_text\"][\"pages\"] == []\n\n\ndef test_scanned_pdf_without_the_ocr_option_is_refused_and_offers_ocr(client):\n    db, c = client\n    r = c.post(\"/api/cases/pdf\", content=scan_pdf(), headers=PDF)\n    e = r.json()[\"error\"]\n    assert r.status_code == 400 and e[\"detail\"][\"reason\"] == \"pdf_no_text_layer\" and e[\"detail\"][\"scanned_pages\"] == [1]\n    assert \"available\" in e[\"detail\"][\"ocr\"]\n    assert DB.connect(db).execute(\"SELECT COUNT(*) FROM cases\").fetchone()[0] == 0\n\n\ndef test_ocr_requested_without_tesseract_is_a_clear_400_and_stores_nothing(client, monkeypatch):\n    from app.backend import pdf_ocr\n    monkeypatch.setattr(pdf_ocr.shutil, \"which\", lambda name: None)\n    db, c = client\n    r = c.post(\"/api/cases/pdf?ocr=true\", content=scan_pdf(), headers=PDF)\n    e = r.json()[\"error\"]\n    assert r.status_code == 400 and e[\"detail\"][\"reason\"] == \"ocr_unavailable\" and \"brew install tesseract\" in e[\"message\"]\n    assert DB.connect(db).execute(\"SELECT COUNT(*) FROM cases\").fetchone()[0] == 0\n\n\n@needs_tesseract\ndef test_ocr_upload_serves_the_page_image_beside_the_text_and_marks_records(client):\n    _, c = client\n    r = c.post(\"/api/cases/pdf?ocr=true\", content=scan_pdf(), headers=PDF)\n    assert r.status_code == 201, r.text\n    b = r.json()\n    assert b[\"pdf_checks\"][\"ocr\"][\"ran\"] and b[\"pdf_checks\"][\"ocr\"][\"pages\"] == [1]\n    assert all(x[\"ocr_derived\"] and x[\"page\"] == 1 for x in b[\"records\"])\n    img = c.get(f\"/api/cases/{b['token']}/pages/1/image\")\n    assert img.status_code == 200 and img.headers[\"content-type\"] == \"image/png\" and img.content[:8] == b\"\\x89PNG\\r\\n\\x1a\\n\"\n    assert c.get(f\"/api/cases/{b['token']}/pages/2/image\").status_code == 404\n    view = c.get(f\"/api/cases/{b['token']}\").json()\n    assert view[\"pdf_pages\"][0][\"source\"] == \"ocr\" and \"page_images\" not in view and \"png_b64\" not in str(view)\n    assert c.get(\"/api/cases/nope/pages/1/image\").status_code == 404\n\n\n@needs_tesseract\ndef test_deleting_the_case_removes_the_stored_page_image(client):\n    _, c = client\n    t = c.post(\"/api/cases/pdf?ocr=true\", content=scan_pdf(), headers=PDF).json()[\"token\"]\n    assert c.delete(f\"/api/cases/{t}\").status_code == 204\n    assert c.get(f\"/api/cases/{t}/pages/1/image\").status_code == 404\n\n\ndef test_every_item_on_an_ocr_page_is_needs_review_after_a_full_run(tmp_path):\n    raw = G.raw(\"sample\")\n    conn = DB.connect(str(tmp_path / \"o.sqlite\"))\n    cfg = {\"source_pdf\": True, \"pages\": [{\"page\": 1, \"start\": 0, \"end\": len(raw), \"source\": \"ocr\"}]}\n    cid = DB.create_case(conn, raw, now=1.0, config_json=cfg)\n    out = PL.run_pipeline(conn, cid, raw, call=FakeCall(sample_script()), now=lambda: 1.0)\n    items = out[\"entries\"] + out[\"amounts\"] + out[\"flags\"]\n    live = [i for i in items if i[\"state\"] != \"rejected\"]\n    assert live and all(i[\"state\"] == \"needs_review\" and \"OCR_DERIVED\" in i[\"reasons\"] for i in live)\n    assert out[\"counts\"][\"verified\"] == 0\n    stored = [r for k in (\"entry\", \"amount\", \"flag\") for r in DB.list_items(conn, cid, k) if r[\"state\"] != \"rejected\"]\n    assert stored and all(r[\"state\"] == \"needs_review\" and \"OCR_DERIVED\" in r[\"state_reasons\"] for r in stored)\n\n\ndef test_a_text_layer_pdf_run_is_unchanged_by_the_ocr_marking(tmp_path):\n    raw = G.raw(\"sample\")\n    conn = DB.connect(str(tmp_path / \"n.sqlite\"))\n    cid = DB.create_case(conn, raw, now=1.0, config_json={\"source_pdf\": True, \"pages\": [{\"page\": 1, \"start\": 0, \"end\": len(raw)}]})\n    out = PL.run_pipeline(conn, cid, raw, call=FakeCall(sample_script()), now=lambda: 1.0)\n    assert out[\"counts\"][\"verified\"] > 0 and not any(\"OCR_DERIVED\" in i[\"reasons\"] for i in out[\"entries\"])\n\n\ndef test_requirements_pin_pypdfium2_exactly():\n    import pathlib\n    txt = (pathlib.Path(__file__).resolve().parents[2] / \"requirements.txt\").read_text()\n    assert \"pypdfium2==5.14.0\" in txt.splitlines()\nE\n.venv/bin/python -m pytest -q tests/unit/test_pdf_checks_api.py tests/unit/test_pdf_ocr.py tests/unit/test_pdf_hidden.py tests/unit/test_pdf_upload.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:24:48.569Z

**tool result**
````
........................................................                 [100%]
56 passed in 7.68s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:51.024Z

**tool call — Bash**
````
{
 "command": "(.venv/bin/python -m pytest -q tests/unit -x -q 2>&1 | tail -15); grep -n \"^def \" app/backend/trace.py | head -30"
}
````

### User / tool · 2026-11-02T04:25:19.096Z

**tool result**
````
        """T-034 AC5 / arch invariant: no anthropic SDK or subprocess import outside app/llm/backends."""
        import re
        app = pathlib.Path(__file__).resolve().parents[2] / "app"
        bad = [str(p.relative_to(app)) for p in app.rglob("*.py")
               if "llm/backends" not in p.as_posix() and re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", p.read_text(), re.M)]
>       assert bad == []
E       AssertionError: assert ['backend/pdf_ocr.py'] == []
E         
E         Left contains one more item: 'backend/pdf_ocr.py'
E         Use -v to get more diff

tests/unit/test_provider.py:121: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_provider.py::test_single_call_path - AssertionError: a...
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
25:def judge_of_prompt(pv):
78:def reason_text(code: str) -> str:
87:def na(code: str, target: dict = None, options: list = None) -> dict:
96:def step(sid, label, kind, status, why_text, *, reason=None, rule=None, evidence=None, next_action=None, blocks=False, **extra):
101:def _ocr_steps(R, rid) -> list:
109:def _number(steps):
115:def _progress(steps):
154:def _span(cx, rid, start, end, text):
158:def _llm_evidence(cx, role, model, prompt_version, call):
172:def _norm_verdict(step_id, v):
178:def _judge_reason_code(jd, call):
192:def _judge_step(cx, item_id, jd, jid, R, *, sid=None, label=None, rule="row 4"):
224:def _human_step(cx, row, kind, *, blocks_ok=True, extra_pending_next=None):
249:def _skipped(sid, label, kind, code, rule=None, rule_text=None):
256:def _finish(cx, item_id, kind, row, steps, *, blocks_flag=None):
294:def _excerpt_ev(cx, rid, row):
299:def _entry_steps(cx, row):
390:def _amount_steps(cx, row):
446:def _flag_steps(cx, row):
570:def _ntext(code):
574:def _narrative_trace(cx, item_id):
645:def item_trace(conn, case_id: str, item_id: str, full: bool = False) -> dict:
665:def _judge_rows(cx):
681:def _judge_never_ran(cx, kind, row):
695:def _paralegal_wording(kind, row) -> bool:
700:def unjudged_items(conn, case_id: str) -> list:
715:def judge_not_run_blockers(conn, case_id: str) -> list:
720:def _jnr_blocker(u):
725:def judge_report(conn, case_id: str, full: bool = False) -> dict:
788:def rationale_or(code, verdict):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:20.608Z

**tool call — Bash**
````
{
 "command": "grep -rn \"no anthropic SDK or subprocess import\" tests | head; grep -n \"subprocess\\|claude\\|anthropic\" app/backend/pdf_ocr.py"
}
````

### User / tool · 2026-11-02T04:25:20.724Z

**tool result**
````
tests/unit/test_provider.py:116:    """T-034 AC5 / arch invariant: no anthropic SDK or subprocess import outside app/llm/backends."""
1:"""Local OCR for scanned PDF pages (T-086, D-042). The Tesseract binary runs as a subprocess on this machine; no page image or text
17:import subprocess
55:        v = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=10, env=_ENV)
59:        langs = subprocess.run([exe, "--list-langs"], capture_output=True, text=True, timeout=10, env=_ENV)
61:    except (OSError, subprocess.SubprocessError):
138:            p = subprocess.run([_which(), src, "stdout", "-l", lang, "--psm", "3", "tsv"], capture_output=True, text=True,
140:        except subprocess.TimeoutExpired:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:22.654Z

**tool call — Bash**
````
{
 "command": "sed -n 112,124p tests/unit/test_provider.py; grep -rn \"single_call_path\" tests | head"
}
````

### User / tool · 2026-11-02T04:25:22.792Z

**tool result**
````
    assert root not in pathlib.Path(seen["cwd"]).resolve().parents and pathlib.Path(seen["cwd"]).resolve() != root
    assert 0 < seen["timeout"] <= 120 and "ANTHROPIC_API_KEY" not in seen["env"]

def test_single_call_path():
    """T-034 AC5 / arch invariant: no anthropic SDK or subprocess import outside app/llm/backends."""
    import re
    app = pathlib.Path(__file__).resolve().parents[2] / "app"
    bad = [str(p.relative_to(app)) for p in app.rglob("*.py")
           if "llm/backends" not in p.as_posix() and re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", p.read_text(), re.M)]
    assert bad == []

def test_no_text_in_logs(monkeypatch, caplog, capsys):
    """T-034 AC5 / arch invariant: backend failures never put the prompt, reply or SDK message in errors or logs."""
tests/unit/test_provider.py:115:def test_single_call_path():
tests/unit/test_provider_backends.py:153:def test_single_call_path():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:24.024Z

**tool call — Bash**
````
{
 "command": "sed -n 150,165p tests/unit/test_provider_backends.py"
}
````

### User / tool · 2026-11-02T04:25:24.115Z

**tool result**
````
    assert out == {"summary": "ok"} and row["backend"] == "fixture" and row["role"] == "judge" and row["parsed_ok"] == 1
    assert json.loads(row["recorded_from_json"] if "recorded_from_json" in row else json.dumps(row["recorded_from"]))["backend"] == "claude-cli"

def test_single_call_path():
    """T-034 AC5: no SDK or subprocess use outside app/llm/backends."""
    for p in (ROOT / "app").rglob("*.py"):
        if "backends" in p.parts and "llm" in p.parts:
            continue
        src = p.read_text()
        assert not re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", src, re.M), p

def test_no_text_in_logs(tmp_path, monkeypatch, caplog, capsys):
    """T-034 AC5: a failing live call logs neither prompt nor error text."""
    caplog.set_level("DEBUG")
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    def fake_run(a, **k): raise subprocess.TimeoutExpired("claude", 120)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:32.153Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"tests/unit/test_provider.py\"\ns=open(p).read()\nold='''    bad = [str(p.relative_to(app)) for p in app.rglob(\"*.py\")\n           if \"llm/backends\" not in p.as_posix() and re.search(r\"^\\\\s*(import|from)\\\\s+(anthropic|subprocess)\\\\b\", p.read_text(), re.M)]\n    assert bad == []'''\nnew='''    # The one allowed exception: app/backend/pdf_ocr.py runs the local Tesseract binary (T-086). That is OCR, not an LLM call; it may import\n    # subprocess but never the anthropic SDK, and test_pdf_ocr.py::test_pdf_ocr_only_runs_tesseract checks it never starts `claude`.\n    allow_subprocess = {\"backend/pdf_ocr.py\"}\n    bad = [str(p.relative_to(app)) for p in app.rglob(\"*.py\")\n           if \"llm/backends\" not in p.as_posix()\n           and re.search(r\"^\\\\s*(import|from)\\\\s+(anthropic|subprocess)\\\\b\", p.read_text(), re.M)\n           and not (str(p.relative_to(app)) in allow_subprocess and not re.search(r\"^\\\\s*(import|from)\\\\s+anthropic\\\\b\", p.read_text(), re.M))]\n    assert bad == []'''\nassert s.count(old)==1; open(p,\"w\").write(s.replace(old,new))\np=\"tests/unit/test_provider_backends.py\"\ns=open(p).read()\nold='''        if \"backends\" in p.parts and \"llm\" in p.parts:\n            continue\n        src = p.read_text()\n        assert not re.search(r\"^\\\\s*(import|from)\\\\s+(anthropic|subprocess)\\\\b\", src, re.M), p'''\nnew='''        if \"backends\" in p.parts and \"llm\" in p.parts:\n            continue\n        src = p.read_text()\n        if p.name == \"pdf_ocr.py\" and \"backend\" in p.parts:      # local Tesseract binary (T-086), not an LLM call; anthropic stays banned\n            assert not re.search(r\"^\\\\s*(import|from)\\\\s+anthropic\\\\b\", src, re.M), p\n            continue\n        assert not re.search(r\"^\\\\s*(import|from)\\\\s+(anthropic|subprocess)\\\\b\", src, re.M), p'''\nassert s.count(old)==1; open(p,\"w\").write(s.replace(old,new))\nE\ncat >> tests/unit/test_pdf_ocr.py <<'E'\n\n\ndef test_pdf_ocr_only_runs_tesseract():\n    \"\"\"The subprocess allow-list in test_provider.py covers pdf_ocr.py because it runs a local OCR binary, not an LLM: it never names\n    `claude` or the anthropic SDK, and every subprocess.run starts with the tesseract executable (or its --version / --list-langs probes).\"\"\"\n    import pathlib\n    import re\n    src = pathlib.Path(pdf_ocr.__file__).read_text()\n    code = \"\\n\".join(l for l in src.splitlines() if not l.lstrip().startswith((\"#\", '\"\"\"')))\n    assert not re.search(r\"claude|anthropic\", code, re.I)\n    calls = re.findall(r\"subprocess\\.run\\(\\[([^,\\]]+)\", src)\n    assert calls and all(c.strip() in (\"exe\", \"_which()\") for c in calls)\nE\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T04:26:13.363Z

**tool result**
````
........................................................................ [ 67%]
........................................................................ [ 73%]
........................................................................ [ 78%]
........................................................................ [ 84%]
........................................................................ [ 89%]
........................................................................ [ 95%]
.........................................................                [100%]
1281 passed in 39.75s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:26:15.465Z

**tool call — Bash**
````
{
 "command": "grep -n \"^## POST /api/cases/pdf\" -A6 memory/contracts/api.md | cut -c1-200"
}
````

### User / tool · 2026-11-02T04:26:15.578Z

**tool result**
````
77:## POST /api/cases/pdf (D-031)
78-Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the c
79-Errors: `400 bad_request` with `detail.reason` = `pdf_no_text_layer` (looks scanned: refused before anything is stored, no model call), `pdf_unreadable`, `pdf_encrypted`; `413 input_too_large` (`pd
80-
81-## POST /api/cases/{token}/review/batch (D-031)
82-Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "p
83-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:26:28.837Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np=\"memory/contracts/api.md\"\ns=open(p).read()\nmarker=\"\\n## POST /api/cases/{token}/review/batch (D-031)\"\nassert s.count(marker)==1\nadd='''\n### PDF hidden text and local OCR (T-087, T-086; D-042)\nQuery on `POST /api/cases/pdf`: `include_hidden` = `all` or a page list such as `2,5` (pages whose hidden text the paralegal confirmed; default none) and `ocr=true` (read scanned pages with local Tesseract; default off). Both are decided by re-posting the same file, which creates a new case (ingest is code only, so it costs no model call). Limits: OCR reads at most 10 scanned pages per upload, 150 s in all, nothing leaves the server.\n\n**Hidden text.** Every text object is checked against the page as rendered (pypdfium2). Reasons: `invisible_render_mode`, `transparent`, `off_page`, `tiny_font` (under 3 pt effective), `blends_with_background` (white or background-coloured text, or text covered by a shape: the rendered pixels under it are uniform). Hidden text is removed from the case text, so it can never ground a quote, until its page is confirmed. A file whose only text is hidden is refused with `detail.reason: \"pdf_only_hidden_text\"` and `detail.hidden_text_pages`.\n**OCR.** A page with no text left and a picture on it is \"scanned\". Without `ocr=true` the upload is refused as before (`pdf_no_text_layer`) with `detail.scanned_pages: [..]` and `detail.ocr` (the status object below) so the UI can offer \"Read scanned pages (OCR)\". With `ocr=true`: `400 ocr_unavailable` (Tesseract missing or too old; `message` is the plain install line, `detail.ocr` the status), `ocr_too_many_pages`, `ocr_failed`. OCR text is quoted exactly as OCR read it.\n\nResponse and `GET /api/cases/{token}` gain, for PDF cases only:\n```json\n\"pdf_checks\": {\n  \"hidden_text\": {\"checked\": true, \"excluded_until_confirmed\": true,\n    \"pages\": [{\"page\": 2, \"count\": 1, \"excluded\": true, \"confirmed\": false,\n               \"items\": [{\"text\": \"…\", \"truncated\": false, \"reasons\": [\"blends_with_background\"], \"why\": \"the same colour as the page behind it (not visible when the page is shown)\"}]}]},\n  \"ocr\": {\"requested\": true, \"ran\": true, \"scanned_pages\": [3], \"pages\": [3], \"engine\": \"tesseract 5.5.2\", \"low_conf_words\": 12, \"items_need_review\": true,\n          \"low_conf_rule\": \"words under 60 confidence, or under 80 when the word has a digit\",\n          \"status\": {\"available\": true, \"version\": \"5.5.2\", \"tested_version\": \"5.5.2\", \"languages\": [\"eng\"], \"message\": \"Tesseract 5.5.2 is available.\"}}},\n\"pdf_pages\": [{\"page\": 3, \"start\": 0, \"end\": 812, \"source\": \"ocr\", \"has_image\": true, \"mean_conf\": 91.2, \"words\": 120, \"low_conf_count\": 12,\n               \"low_conf\": [{\"start\": 40, \"end\": 47, \"text\": \"Chaege:\", \"conf\": 38.0}]}]\n```\n`checked: false` means the renderer could not open the file, so the hidden-text check did not run (show it as skipped). `pdf_pages[].start/end/low_conf[].start/end` are offsets into the case text; a page confirmed for hidden text carries `hidden_text_included: true`. Every record in a PDF case has `ocr_derived: true|false`.\n**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, date confirmation or rejudge clears it. Its trace gains a failing code step `ocr_source` (\"Record was not read from a scanned page\", rule D-042, next action `READ_RECORD`); nothing else about other items' traces changes.\n**`GET /api/cases/{token}/pages/{n}/image`** -> `image/png` (greyscale, 150 dpi) of an OCR'd page, stored with the case and deleted with it; `404 not_found` for a page that has none. The UI shows it beside the page's text.\n'''\ns=s.replace(marker, add+marker)\nopen(p,\"w\").write(s)\nE\ncat >> tests/unit/test_pdf_ocr.py <<'E'\n\n\ndef test_an_ocr_item_trace_has_the_ocr_source_step(tmp_path):\n    from app.backend import trace\n    from app.db import db as DB\n    from tests.unit import _golden as G\n    from tests.unit._fakes import FakeCall, sample_script\n    from app.backend import pipeline as PL\n    raw = G.raw(\"sample\")\n    conn = DB.connect(str(tmp_path / \"t.sqlite\"))\n    cid = DB.create_case(conn, raw, now=1.0, config_json={\"source_pdf\": True, \"pages\": [{\"page\": 1, \"start\": 0, \"end\": len(raw), \"source\": \"ocr\"}]})\n    out = PL.run_pipeline(conn, cid, raw, call=FakeCall(sample_script()), now=lambda: 1.0)\n    t = trace.item_trace(conn, cid, out[\"entries\"][0][\"id\"])\n    s = next(x for x in t[\"steps\"] if x[\"id\"] == \"ocr_source\")\n    assert s[\"status\"] == \"fail\" and s[\"reason_code\"] == \"OCR_DERIVED\" and s[\"next_action\"][\"code\"] == \"READ_RECORD\"\nE\n.venv/bin/python -m pytest -q tests/unit/test_pdf_ocr.py 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T04:26:30.696Z

**tool result**
````
.............                                                            [100%]
13 passed in 1.41s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:26:36.794Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit 2>&1 | tail -3; git status --short app/backend tests requirements.txt memory/contracts | grep -v \"^??\" ; git status --short | grep \"^??\" | grep -E \"pdf|_pdf\""
}
````

### User / tool · 2026-11-02T04:27:15.672Z

**tool result**
````
FAILED tests/unit/test_boundaries.py::test_no_llm_client_direct_or_transitive[conflicts]
FAILED tests/unit/test_boundaries.py::test_no_llm_client_direct_or_transitive[flag_templates]
5 failed, 1277 passed in 37.44s
 M app/backend/api.py
 M app/backend/confidence.py
D  app/backend/date_convention.py
 M app/backend/dates.py
D  app/backend/dismissal_patterns.py
 M app/backend/export.py
 M app/backend/flags.py
 M app/backend/generator.py
 M app/backend/judges.py
 M app/backend/narrative.py
 M app/backend/pdf_text.py
 M app/backend/pipeline.py
MM app/backend/present.py
 M app/backend/rejudge.py
 M app/backend/review.py
 M app/backend/sentences.py
 M app/backend/store.py
 M app/backend/trace.py
 M app/backend/why.py
 M memory/contracts/api.md
 M requirements.txt
M  tests/e2e/conftest.py
M  tests/e2e/test_ladder_gate.py
M  tests/e2e/test_local_mode.py
A  tests/e2e/test_rerun_judge.py
M  tests/e2e/test_stepper.py
 D tests/fixtures/llm/curated/1db15db3cba3733c5e00a8732ecddb694b45c2637be29b83e3bfa35576123f24.json
 D tests/fixtures/llm/curated/b8bf558be04cc588cd8da6cbb2e7678ce1d970a0dceeb367ddc03c19ccb87729.json
D  tests/unit/test_date_convention.py
D  tests/unit/test_dismissal_patterns.py
 M tests/unit/test_flags_injection.py
 M tests/unit/test_flags_pass.py
 M tests/unit/test_pipeline.py
 M tests/unit/test_provider.py
 M tests/unit/test_provider_backends.py
 M tests/unit/test_t075_determinism.py
 M tests/unit/test_t093_eval_signature.py
?? app/backend/pdf_checks.py
?? app/backend/pdf_hidden.py
?? app/backend/pdf_ocr.py
?? app/backend/pdf_routes.py
?? tests/unit/_pdf_raw.py
?? tests/unit/test_pdf_checks_api.py
?? tests/unit/test_pdf_hidden.py
?? tests/unit/test_pdf_ocr.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:17.643Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit 2>&1 | grep -E \"^FAILED|^E \" | head -12"
}
````

### User / tool · 2026-11-02T04:27:55.099Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:56.401Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit 2>&1 | tail -4"
}
````

### User / tool · 2026-11-02T04:28:31.738Z

**tool result**
````
FAILED tests/unit/test_trace.py::test_rejudge_only_touches_items_whose_judge_never_ran
FAILED tests/unit/test_trace.py::test_rejudge_failure_leaves_the_item_unjudged_and_the_gate_closed
FAILED tests/unit/test_trace.py::test_rejudge_objection_is_recorded_and_the_gate_opens_because_the_judge_ran
5 failed, 1277 passed in 34.11s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:28:34.998Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_boundaries.py 2>&1 | grep -E \"^(FAILED|E  )\" | head -12"
}
````

### User / tool · 2026-11-02T04:28:40.505Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:28:44.810Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_trace.py tests/unit/test_boundaries.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:28:50.640Z

**tool result**
````
........................................................................ [ 85%]
............                                                             [100%]
84 passed in 5.27s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:28:52.341Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit 2>&1 | tail -4"
}
````

### User / tool · 2026-11-02T04:29:30.089Z

**tool result**
````
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py:355: JSONDecodeError
=========================== short test summary info ============================
FAILED tests/unit/test_db.py::test_v3_to_v4_migrates_in_place_keeping_rows_and_converts_reclassify_edits
1 failed, 1285 passed in 36.64s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:29:36.104Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/scratch/commit.py <<'E'\nimport subprocess, re, os, tempfile, sys\nos.chdir(\"/Users/arsis/zlayt-pm-project\")\nidx = tempfile.mktemp()\nenv = {**os.environ, \"GIT_INDEX_FILE\": idx}\ndef git(*a, inp=None, check=True):\n    return subprocess.run([\"git\", *a], env=env, input=inp, capture_output=True, text=True, check=check)\ngit(\"read-tree\", \"HEAD\")\nKEY = re.compile(r\"pdf|ocr|OCR|pypdfium2|hidden\", re.I)\nshared = [\"app/backend/api.py\",\"app/backend/confidence.py\",\"app/backend/pipeline.py\",\"app/backend/present.py\",\"app/backend/trace.py\",\"app/backend/why.py\",\n          \"memory/contracts/api.md\",\"requirements.txt\",\"tests/unit/test_provider.py\",\"tests/unit/test_provider_backends.py\"]\nwhole = [\"app/backend/pdf_text.py\",\"app/backend/pdf_checks.py\",\"app/backend/pdf_hidden.py\",\"app/backend/pdf_ocr.py\",\"app/backend/pdf_routes.py\",\n         \"tests/unit/_pdf_raw.py\",\"tests/unit/test_pdf_checks_api.py\",\"tests/unit/test_pdf_hidden.py\",\"tests/unit/test_pdf_ocr.py\"]\ngit(\"add\", *whole)\nfor f in shared:\n    d = git(\"diff\", \"-U0\", \"HEAD\", \"--\", f).stdout   # working tree vs HEAD\n    head, *hunks = re.split(r\"(?m)^(?=@@ )\", d)\n    keep = [h for h in hunks if KEY.search(\"\\n\".join(l for l in h.splitlines() if l[:1] in \"+-\"))]\n    print(f, len(hunks), \"->\", len(keep))\n    for h in hunks:\n        if h not in keep: print(\"   skipped:\", [l[:90] for l in h.splitlines() if l[:1] in \"+-\"][:2])\n    if keep:\n        r = git(\"apply\", \"--cached\", \"--unidiff-zero\", \"-\", inp=head + \"\".join(keep), check=False)\n        if r.returncode: print(\"APPLY FAIL\", f, r.stderr)\nprint(git(\"diff\", \"--cached\", \"--stat\").stdout)\nopen(\"/private/tmp/claude-501/scratch/idx_path\",\"w\").write(idx)\nE\n.venv/bin/python /private/tmp/claude-501/scratch/commit.py"
}
````

### User / tool · 2026-11-02T04:29:36.656Z

**tool result**
````
app/backend/api.py 11 -> 9
   skipped: ['-_ERR_STATUS = {"bad_request": 400, "input_too_large": 413}', '+_ERR_STATUS = {"bad_request": 400, "input_too_large": 413, "unsupported_language": 400}']
   skipped: ['-                if isinstance(e, ingest.IngestError):', '-                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code) from None']
app/backend/confidence.py 1 -> 1
app/backend/pipeline.py 11 -> 1
   skipped: ['-5 conflicts (one LLM pair pass + J3)  6 flags (one LLM pass per record + lexicon floor + ', '+5 conflicts (code proposes the pairs, J3 classifies each)  6 flags (one LLM pass per reco']
   skipped: ['-                         judges, split_llm, totals as TT, why as WHY)', '+                         judges, language, split_llm, totals as TT, why as WHY)']
   skipped: ['-    recs = ing["records"]', '+    recs = language.annotate(ing["records"])           # D-042: en | es | other per recor']
   skipped: ['-    warnings = list(ing["warnings"])', '+    warnings = list(ing["warnings"]) + language.record_warnings(recs)']
   skipped: ['-    ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid), spli', '+    try:']
   skipped: ['-            errors.append(_err("LLM_FAILED_AFTER_RETRIES", "extract", f["record_no"], "FI', '+            errors.append(_err("UNSUPPORTED_LANGUAGE" if f["failure"] == "UNSUPPORTED_LAN']
   skipped: ['-    # 5: semantic conflicts (LLM) + J3', '+    # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T']
   skipped: ['-    distinct = [by_n[g[0]] for g in ing["groups"]]', '+    distinct = [by_n[g[0]] for g in ing["groups"] if by_n[g[0]].get("lang") != "other"]  ']
   skipped: ['-        pair = FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_r', '-        for i, f in enumerate(pair, 1):']
   skipped: ['+    try:', '+        language.case_check(language.annotate(IN.ingest(raw)["records"]))']
app/backend/present.py 5 -> 3
   skipped: ['-            "excerpt_end": ed.get("excerpt_end", row["excerpt_end"]), "duplicate_note": N', '+            "excerpt_end": ed.get("excerpt_end", row["excerpt_end"]), "duplicate_note": N']
   skipped: ['-         "char_end": r["char_end"], "text": block}', '+         "char_end": r["char_end"], "text": block, "language": language.block_lang(block)']
app/backend/trace.py 8 -> 6
   skipped: ['+    if origin == "code" and cc.get("candidate_rule"):', '+        # T-094: a conflict pair proposed by code and classified by the judge (J3). The m']
   skipped: ['-        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], g', '+        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], g']
app/backend/why.py 1 -> 1
memory/contracts/api.md 4 -> 3
   skipped: ['+| GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (bi']
requirements.txt 1 -> 1
tests/unit/test_provider.py 2 -> 1
   skipped: ['-           if "llm/backends" not in p.as_posix() and re.search(r"^\\s*(import|from)\\s+(ant', '+           if "llm/backends" not in p.as_posix()']
tests/unit/test_provider_backends.py 1 -> 1
 app/backend/api.py                   |  30 ++++--
 app/backend/confidence.py            |   2 +-
 app/backend/pdf_checks.py            | 125 +++++++++++++++++++++++
 app/backend/pdf_hidden.py            | 188 +++++++++++++++++++++++++++++++++++
 app/backend/pdf_ocr.py               | 178 +++++++++++++++++++++++++++++++++
 app/backend/pdf_routes.py            |  25 +++++
 app/backend/pdf_text.py              |  41 ++++++--
 app/backend/pipeline.py              |   2 +
 app/backend/present.py               |   8 +-
 app/backend/trace.py                 |  14 ++-
 app/backend/why.py                   |   1 +
 memory/contracts/api.md              |  59 +++++++++++
 requirements.txt                     |   1 +
 tests/unit/_pdf_raw.py               |  68 +++++++++++++
 tests/unit/test_pdf_checks_api.py    | 128 ++++++++++++++++++++++++
 tests/unit/test_pdf_hidden.py        |  97 ++++++++++++++++++
 tests/unit/test_pdf_ocr.py           | 152 ++++++++++++++++++++++++++++
 tests/unit/test_provider.py          |   3 +
 tests/unit/test_provider_backends.py |   3 +
 19 files changed, 1105 insertions(+), 20 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:29:42.382Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(cat /private/tmp/claude-501/scratch/idx_path) && git diff --cached -U0 -- app/backend/api.py app/backend/present.py app/backend/trace.py memory/contracts/api.md | grep -E \"^[+-]\" | cut -c1-170 | grep -v \"^+++\\|^---\"; git diff HEAD -- tests/unit/test_provider.py | grep \"^[+-]\" | cut -c1-150"
}
````

### User / tool · 2026-11-02T04:29:42.516Z

**tool result**
````
-from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
+from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
+from app.backend import pdf_checks as _pdf_checks      # noqa: E402  (T-086/T-087)
+_PDF_MESSAGES.update(_pdf_checks.MESSAGES)
-    async def create_case_from_pdf(request: Request, name: str = None):
-        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer only; a scanned PDF is refused before anything is stored or run."""
+    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):
+        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer minus hidden text (T-087, `include_hidden`); a scanned PDF is
+        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
+        opts = {}
+        if (ocr or "").lower() in ("1", "true", "yes"):
+            opts["ocr"] = True
+        if include_hidden:
+            opts["include_hidden"] = include_hidden
-            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data), pdf_text.EXTRACT_TIMEOUT_S)
+            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data, **opts), _pdf_checks.OCR_TIMEOUT_S if opts.get("ocr") else pdf_text.EXTRACT_TIMEOUT_S)
-                           _PDF_MESSAGES[e.code], {"reason": e.code}) from None
-        return make_case(got["text"], name, False, pdf_pages=got["pages"])
+                           (e.detail.get("message") if e.code == "ocr_unavailable" else None) or _PDF_MESSAGES[e.code], {"reason": e.code, **e.detail}) from None
+        out = make_case(got["text"], name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None})
+        out["pdf_checks"] = got.get("pdf_checks")
+        return out
-    def make_case(text, name, sample, pdf_pages=None):
+    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None):
-                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages}} if pdf_pages else {}))
+                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
+    from app.backend import billing
+    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
+    from app.backend import pdf_routes
+    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
-from app.backend import confidence, date_convention, grounding, pdf_text, sentences, store, totals as T, why
+from app.backend import confidence, date_convention, grounding, language, pdf_text, sentences, spanish, store, totals as T, why
+        from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR
+        v["ocr_derived"] = pdf_checks.is_ocr_span(pages, r["char_start"], r["char_end"])
-            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"])}
+            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
+            **{k: (case.get("config") or {})[k] for k in ("pdf_checks",) if (case.get("config") or {}).get(k)},     # T-086/T-087 (PDF cases only)
+            **({"pdf_pages": (case.get("config") or {})["pages"]} if (case.get("config") or {}).get("pages") else {})}
-    "INJECTION_SUSPECTED": "injection_scan", "LLM_FAILED_AFTER_RETRIES": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
+    "INJECTION_SUSPECTED": "injection_scan", "OCR_DERIVED": "ocr_source", "LLM_FAILED_AFTER_RETRIES": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
+def _ocr_steps(R, rid) -> list:
+    """T-086: the step that holds an OCR-read item for review. Only present when the item carries OCR_DERIVED, so other cases are unchanged."""
+    if "OCR_DERIVED" not in R:
+        return []
+    return [step("ocr_source", "Record was not read from a scanned page", "code", FAIL, reason_text("OCR_DERIVED"), reason="OCR_DERIVED", rule="D-042",
+                 evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid}))]
+
+
+    st += _ocr_steps(R, rid)
+    st += _ocr_steps(R, rid)
+        st += _ocr_steps(R, rid0)
+    st += _ocr_steps(R, rid0)
+### PDF hidden text and local OCR (T-087, T-086; D-042)
+Query on `POST /api/cases/pdf`: `include_hidden` = `all` or a page list such as `2,5` (pages whose hidden text the paralegal confirmed; default none) and `ocr=true` (rea
+
+**Hidden text.** Every text object is checked against the page as rendered (pypdfium2). Reasons: `invisible_render_mode`, `transparent`, `off_page`, `tiny_font` (under 3
+**OCR.** A page with no text left and a picture on it is "scanned". Without `ocr=true` the upload is refused as before (`pdf_no_text_layer`) with `detail.scanned_pages: 
+
+Response and `GET /api/cases/{token}` gain, for PDF cases only:
+```json
+"pdf_checks": {
+  "hidden_text": {"checked": true, "excluded_until_confirmed": true,
+    "pages": [{"page": 2, "count": 1, "excluded": true, "confirmed": false,
+               "items": [{"text": "…", "truncated": false, "reasons": ["blends_with_background"], "why": "the same colour as the page behind it (not visible when the p
+  "ocr": {"requested": true, "ran": true, "scanned_pages": [3], "pages": [3], "engine": "tesseract 5.5.2", "low_conf_words": 12, "items_need_review": true,
+          "low_conf_rule": "words under 60 confidence, or under 80 when the word has a digit",
+          "status": {"available": true, "version": "5.5.2", "tested_version": "5.5.2", "languages": ["eng"], "message": "Tesseract 5.5.2 is available."}}},
+"pdf_pages": [{"page": 3, "start": 0, "end": 812, "source": "ocr", "has_image": true, "mean_conf": 91.2, "words": 120, "low_conf_count": 12,
+               "low_conf": [{"start": 40, "end": 47, "text": "Chaege:", "conf": 38.0}]}]
+```
+`checked: false` means the renderer could not open the file, so the hidden-text check did not run (show it as skipped). `pdf_pages[].start/end/low_conf[].start/end` are 
+**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the mod
+**`GET /api/cases/{token}/pages/{n}/image`** -> `image/png` (greyscale, 150 dpi) of an OCR'd page, stored with the case and deleted with it; `404 not_found` for a page t
+
+## GET /api/cases/{token}/billing  (T-083, D-042)
+Code-only billing analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs. Computed on read from the records, never st
+```json
+{ "billing": {
+  "status": "analyzed",                         // analyzed | partial_unclear (some figure could not be read) | none_found
+  "providers": [ {
+    "provider": "Larkspur Hollow Physical Therapy", "record_nos": [1], "basis": "itemized_ledger",   // or "claim_form" when the provider has no ledger
+    "billed": {"cents": 44500, "usd": "$445.00"}, "adjustment": {"cents": 4500, "usd": "$45.00"}, "paid": {"cents": null, "usd": null},
+    "negotiated_reductions": {"cents": null, "usd": null},        // attorney reductions on the ledger, kept out of `adjustment`
+    "balance": {"text": "400.00", "cents": 40000, "usd": "$400.00", "cite": {"record_no": 1, "excerpt": "TOTAL CHARGES 445.00 ..."}},   // the statement's own figure, nu
+    "stated_totals": {"billed": {...}, "paid": {...}, "adjustment": {...}, "balance": {...}},        // each with a cite; only those the document prints
+    "complete": true, "unclear_lines": 0, "line_count": 7, "claim_lines_not_totaled": 0,
+    "checks": [ {"code": "LEDGER_TOTAL_MISMATCH", "field": "billed", "stated": {"cents": 45500, "usd": "$455.00", ...}, "computed": {"cents": 44500, "usd": "$445.00"}, "
+    "lines": [ {
+      "id": "b3", "kind": "charge",                              // charge | reversal | payment | adjustment | balance_only | unclear
+      "form": "ledger",                                          // ledger | cms1500 | ub04
+      "dos": "06/10/26", "dos_iso": "2026-06-10", "posted": "06/11/26", "code": "97140", "description": "Manual therapy x1",
+      "billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "adjustment": null, "paid": null, "balance": {"text": "410.00", "cents": 41000, "usd": "$410.00"},
+      "unclear": [], "negotiated": false, "checks": [],           // LINE_UNCLEAR | BALANCE_STEP_MISMATCH | NO_DATE_OF_SERVICE
+      "excerpt": "06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00",   // the printed line, verbatim
+      "record_nos": [1], "cites": [ {"record_no": 1, "excerpt": "<same line>"} ] } ] } ],
+  "payer_reports": [ { "record_no": 2, "provider": "Larkspur Hollow Physical Therapy", "matched_provider": "Larkspur Hollow Physical Therapy",
+    "lines": [ {"dos": "06/10/26", "service": "97140", "billed": {...}, "discount": {...}, "allowed": {...}, "deductible": {...}, "coinsurance": {...}, "plan_paid": {...
+    "checks": [ {"code": "LEDGER_EOB_PAID_MISMATCH", "dos": "06/10/26", "service": "97140", "ledger": {"cents": 0, "usd": "$0.00"}, "eob": {"cents": 1600, ...}, "cites":
+    "not_added_note": "The EOB restates the provider's charge; its amounts are never added to the charges." } ],
+  "lop_lien": [ {"id": "l1", "record_no": 2, "provider": "Pellingham and Rook PLLC", "kind": "asserted_balance", "label": "...", "figure": {"text": "$4,860.00", "cents":
+  "excluded": [ {"id": "x1", "record_no": 1, "provider": "...", "kind": "rate", "why": "...", "figure": {...}, "excerpt": "Fee schedule: Therapeutic exercise $65.00 per 
+  "skipped_records": [ {"record_no": 4, "reason_code": "INJECTION_SUSPECTED"} ],
+  "checks": [ /* every provider and payer check, flat */ ], "line_flags": [ {"code": "BALANCE_STEP_MISMATCH", "line_id": "b3", "provider": "...", "message": "...", "exce
+  "totals": { "billed": {"cents": 318500, "usd": "$3,185.00"}, "adjustment": {...}, "paid": {...}, "provider_count": 2, "not_for_letter": true },
+  "rules": [ "Only figures stated in the records are totaled; ...", "..." ] } }
+```
+**Rules (tested).** Figures are whole cents; credit notation (`(70.00)`, `45.00-`, `-45.00`) makes a charge negative (a void nets out) and is read as a reduction in the 
+**Check codes (closed list, fixed message each):** `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `BALANCE_STEP_MISMATCH`, `LINE_UNCLEAR`, `CLAIM_TOTAL_MISMATCH`, `
+**Ladder.** All steps are code (parse, cite, compare); there is no model step, so no judge. The human step is reading the view; none of it is exportable.
+
+| `OCR_DERIVED` | needs_review | the item's record lies on a page read by OCR (T-086); always needs_review, added by code after the model steps, never cleared by a judge
--- a/tests/unit/test_provider.py
+++ b/tests/unit/test_provider.py
+    # The one allowed exception: app/backend/pdf_ocr.py runs the local Tesseract binary (T-086). That is OCR, not an LLM call; it may import
+    # subprocess but never the anthropic SDK, and test_pdf_ocr.py::test_pdf_ocr_only_runs_tesseract checks it never starts `claude`.
+    allow_subprocess = {"backend/pdf_ocr.py"}
-           if "llm/backends" not in p.as_posix() and re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", p.read_text(), re.M)]
+           if "llm/backends" not in p.as_posix()
+           and re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", p.read_text(), re.M)
+           and not (str(p.relative_to(app)) in allow_subprocess and not re.search(r"^\s*(import|from)\s+anthropic\b", p.read_text(), re.M))]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:29:52.328Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/scratch/fix.py <<'E'\nimport subprocess, os\nos.chdir(\"/Users/arsis/zlayt-pm-project\")\nidx=open(\"/private/tmp/claude-501/scratch/idx_path\").read()\nenv={**os.environ,\"GIT_INDEX_FILE\":idx}\ndef g(*a,inp=None): return subprocess.run([\"git\",*a],env=env,input=inp,capture_output=True,text=True,check=True).stdout\ndef blob(f): return g(\"show\",\":\"+f)\ndef put(f,s):\n    h=g(\"hash-object\",\"-w\",\"--stdin\",inp=s).strip()\n    g(\"update-index\",\"--cacheinfo\",f\"100644,{h},{f}\")\n# api.py\ns=blob(\"app/backend/api.py\")\ns=s.replace(\"ingest, language, narrative\",\"ingest, narrative\",1)\ns=s.replace(\"    from app.backend import billing\\n    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083\\n\",\"\",1)\nput(\"app/backend/api.py\",s)\n# present.py\ns=blob(\"app/backend/present.py\")\ns=s.replace(\"grounding, language, pdf_text, sentences, spanish, store\",\"grounding, pdf_text, sentences, store\",1)\nput(\"app/backend/present.py\",s)\n# api.md: drop billing section\ns=blob(\"memory/contracts/api.md\")\na=s.index(\"\\n## GET /api/cases/{token}/billing\")\nb=s.index(\"\\n## \",a+5) if \"\\n## \" in s[a+5:] else None\nprint(\"billing section chars\",a,b)\nopen(\"/private/tmp/claude-501/scratch/billing_tail.txt\",\"w\").write(s[a:b][-200:] if b else s[a:][-300:])\nE\n.venv/bin/python /private/tmp/claude-501/scratch/fix.py; cat /private/tmp/claude-501/scratch/billing_tail.txt | tail -c 300"
}
````

### User / tool · 2026-11-02T04:29:52.578Z

**tool result**
````
billing section chars 77980 84701
s exportable.

`204`. Removes the case, records, items, calls and events. It is the same function the 24 h purge uses and deletes from every table by case id, including stored prompts (ADR-006).

---
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:29:57.530Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(cat /private/tmp/claude-501/scratch/idx_path) && git show :memory/contracts/api.md | python3 -c \"\nimport sys\ns=sys.stdin.read()\na=s.index('## GET /api/cases/{token}/billing')\nprint(repr(s[a-150:a]))\ne=s.index('none of it is exportable.')\nprint(repr(s[e:e+260]))\n\"; git show HEAD:memory/contracts/api.md | grep -n \"DELETE /api/cases/{token}\" "
}
````

### User / tool · 2026-11-02T04:29:57.659Z

**tool result**
````
'library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).\n\n## DELETE /api/cases/{token}\n'
'none of it is exportable.\n\n`204`. Removes the case, records, items, calls and events. It is the same function the 24 h purge uses and deletes from every table by case id, including stored prompts (ADR-006).\n\n---\n\n## Appendix: reason codes (closed list; one fix'
628:## DELETE /api/cases/{token}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:02.461Z

**tool call — Bash**
````
{
 "command": "cat >> /private/tmp/claude-501/scratch/fix.py <<'E'\na=s.index(\"## GET /api/cases/{token}/billing\")\nb=s.index(\"`204`. Removes the case\")\ns=s[:a]+s[b:]\nput(\"memory/contracts/api.md\",s)\n# test_provider.py: whole file diff vs HEAD is only mine (verified), take the working copy\nh=g(\"hash-object\",\"-w\",\"tests/unit/test_provider.py\").strip()\ng(\"update-index\",\"--cacheinfo\",f\"100644,{h},tests/unit/test_provider.py\")\nE\n.venv/bin/python /private/tmp/claude-501/scratch/fix.py >/dev/null; export GIT_INDEX_FILE=$(cat /private/tmp/claude-501/scratch/idx_path); git diff --cached --stat | cat; git diff --cached -U0 -- memory/contracts/api.md app/backend/api.py app/backend/present.py | grep -E \"^[+-]\" | grep -iE \"billing|language|spanish\" | head; git diff --cached -- tests/unit/test_provider.py | grep -c \"^[+-]\"; git diff --cached -U0 -- app/backend/pipeline.py app/backend/why.py app/backend/confidence.py requirements.txt tests/unit/test_provider_backends.py | grep \"^[+-]\" | cut -c1-140"
}
````

### User / tool · 2026-11-02T04:30:02.848Z

**tool result**
````
 app/backend/api.py                   |  26 +++--
 app/backend/confidence.py            |   2 +-
 app/backend/pdf_checks.py            | 125 +++++++++++++++++++++++
 app/backend/pdf_hidden.py            | 188 +++++++++++++++++++++++++++++++++++
 app/backend/pdf_ocr.py               | 178 +++++++++++++++++++++++++++++++++
 app/backend/pdf_routes.py            |  25 +++++
 app/backend/pdf_text.py              |  41 ++++++--
 app/backend/pipeline.py              |   2 +
 app/backend/present.py               |   6 +-
 app/backend/trace.py                 |  14 ++-
 app/backend/why.py                   |   1 +
 memory/contracts/api.md              |  23 +++++
 requirements.txt                     |   1 +
 tests/unit/_pdf_raw.py               |  68 +++++++++++++
 tests/unit/test_pdf_checks_api.py    | 128 ++++++++++++++++++++++++
 tests/unit/test_pdf_hidden.py        |  97 ++++++++++++++++++
 tests/unit/test_pdf_ocr.py           | 152 ++++++++++++++++++++++++++++
 tests/unit/test_provider.py          |   7 +-
 tests/unit/test_provider_backends.py |   3 +
 19 files changed, 1068 insertions(+), 19 deletions(-)
+          "status": {"available": true, "version": "5.5.2", "tested_version": "5.5.2", "languages": ["eng"], "message": "Tesseract 5.5.2 is available."}}},
9
--- a/app/backend/confidence.py
+++ b/app/backend/confidence.py
-    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT",
+    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT", "OCR_DERIVED",
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
+    from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
+    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.
--- a/app/backend/why.py
+++ b/app/backend/why.py
+    "OCR_DERIVED": "This record was read from a scanned page by OCR, which can misread letters and digits. Check it against the page image.
--- a/requirements.txt
+++ b/requirements.txt
+pypdfium2==5.14.0
--- a/tests/unit/test_provider_backends.py
+++ b/tests/unit/test_provider_backends.py
+        if p.name == "pdf_ocr.py" and "backend" in p.parts:      # local Tesseract binary (T-086), not an LLM call; anthropic stays banned
+            assert not re.search(r"^\s*(import|from)\s+anthropic\b", src, re.M), p
+            continue
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:06.842Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(cat /private/tmp/claude-501/scratch/idx_path) && D=/private/tmp/claude-501/scratch/stage && rm -rf $D && mkdir $D && git checkout-index -a --prefix=$D/ && cd $D && ln -s /Users/arsis/zlayt-pm-project/.venv .venv && .venv/bin/python -m pytest -q tests/unit/test_pdf_checks_api.py tests/unit/test_pdf_ocr.py tests/unit/test_pdf_hidden.py tests/unit/test_pdf_upload.py tests/unit/test_provider.py tests/unit/test_provider_backends.py tests/unit/test_confidence.py tests/unit/test_trace.py 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T04:30:08.446Z

**tool result**
````
ERROR tests/unit/test_pdf_checks_api.py
ERROR tests/unit/test_pdf_upload.py
ERROR tests/unit/test_trace.py
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
3 errors in 0.74s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:09.894Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/scratch/stage && .venv/bin/python -m pytest -q tests/unit/test_pdf_upload.py 2>&1 | grep -E \"^E \" | head -5"
}
````

### User / tool · 2026-11-02T04:30:10.563Z

**tool result**
````
E     File "/private/tmp/claude-501/scratch/stage/app/backend/present.py", line 149
E       case = DB.get_case(conn, case_id)
E                                        ^
E   IndentationError: unindent does not match any outer indentation level
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:12.411Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(cat /private/tmp/claude-501/scratch/idx_path) && git diff --cached -U2 -- app/backend/present.py"
}
````

### User / tool · 2026-11-02T04:30:12.517Z

**tool result**
````
/bin/bash: child setpgid (14766 to 14766): Operation not permitted
diff --git a/app/backend/present.py b/app/backend/present.py
index f9bc01f..6891cb6 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -145,4 +145,6 @@ def record_view(r, raw, with_sentences=True, pages=None):
 
 def case_view(conn, case_id, *, backend, models, demo_mode):
+        from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR
+        v["ocr_derived"] = pdf_checks.is_ocr_span(pages, r["char_start"], r["char_end"])
     case = DB.get_case(conn, case_id)
     raw = case["raw_text"]
@@ -164,5 +166,7 @@ def case_view(conn, case_id, *, backend, models, demo_mode):
             "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
             "review": review_view(conn, case_id), "warnings": [], "error": err,
-            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"])}
+            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
+            **{k: (case.get("config") or {})[k] for k in ("pdf_checks",) if (case.get("config") or {}).get(k)},     # T-086/T-087 (PDF cases only)
+            **({"pdf_pages": (case.get("config") or {})["pages"]} if (case.get("config") or {}).get("pages") else {})}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:20.729Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/scratch/fix2.py <<'E'\nimport subprocess, os\nos.chdir(\"/Users/arsis/zlayt-pm-project\")\nidx=open(\"/private/tmp/claude-501/scratch/idx_path\").read()\nenv={**os.environ,\"GIT_INDEX_FILE\":idx}\ndef g(*a,inp=None): return subprocess.run([\"git\",*a],env=env,input=inp,capture_output=True,text=True,check=True).stdout\ndef put(f,s):\n    h=g(\"hash-object\",\"-w\",\"--stdin\",inp=s).strip()\n    g(\"update-index\",\"--cacheinfo\",f\"100644,{h},{f}\")\ns=g(\"show\",\"HEAD:app/backend/present.py\")\ndef rep(old,new):\n    global s\n    assert s.count(old)==1,old[:50]; s=s.replace(old,new)\nrep('''        v[\"page\"] = pdf_text.page_for(pages, r[\"char_start\"])\n''','''        v[\"page\"] = pdf_text.page_for(pages, r[\"char_start\"])\n        from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR\n        v[\"ocr_derived\"] = pdf_checks.is_ocr_span(pages, r[\"char_start\"], r[\"char_end\"])\n''')\nrep('''            \"created_at\": store.iso(case[\"created_at\"]), \"updated_at\": store.iso(case.get(\"run_finished_at\") or case[\"created_at\"])}\n\n\ndef why_view''','''            \"created_at\": store.iso(case[\"created_at\"]), \"updated_at\": store.iso(case.get(\"run_finished_at\") or case[\"created_at\"]),\n            **{k: (case.get(\"config\") or {})[k] for k in (\"pdf_checks\",) if (case.get(\"config\") or {}).get(k)},     # T-086/T-087 (PDF cases only)\n            **({\"pdf_pages\": (case.get(\"config\") or {})[\"pages\"]} if (case.get(\"config\") or {}).get(\"pages\") else {})}\n\n\ndef why_view''')\nput(\"app/backend/present.py\",s)\nE\n.venv/bin/python /private/tmp/claude-501/scratch/fix2.py && export GIT_INDEX_FILE=$(cat /private/tmp/claude-501/scratch/idx_path) && D=/private/tmp/claude-501/scratch/stage && rm -rf $D && mkdir $D && git checkout-index -a --prefix=$D/ && cd $D && ln -s /Users/arsis/zlayt-pm-project/.venv .venv && .venv/bin/python -m pytest -q tests/unit 2>&1 | tail -6"
}
````

### User / tool · 2026-11-02T04:30:58.228Z

**tool result**
````
........................................................................ [ 76%]
........................................................................ [ 82%]
........................................................................ [ 88%]
........................................................................ [ 94%]
........................................................................ [100%]
1224 passed in 35.41s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:31:03.083Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(cat /private/tmp/claude-501/scratch/idx_path) && git commit -q -m \"feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)\n\nHidden text (white/background-coloured, off-page, tiny, invisible mode, covered) is found by comparing the text layer with the rendered page\n(pypdfium2 5.14.0 pinned), reported per page and kept out of the case text until the paralegal confirms the page. Scanned pages are OCR'd\nlocally on request (ocr=true) with the page image served beside the text, low-confidence words marked, and every item on an OCR page held at\nneeds_review (OCR_DERIVED). Missing tesseract gives a clear message. Tests skip cleanly without tesseract.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git log --oneline | head -1; unset GIT_INDEX_FILE; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T04:31:03.779Z

**tool result**
````
check_secrets: ok (28 file(s) scanned staged)
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
2fca530
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:31:05.125Z

Now the board work.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:31:16.747Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"\n$B ac T-087 --check 1 --agent backend --evidence \"tests/unit/test_pdf_hidden.py (17 tests: white, near-white, covered, off-page, tiny, scaled-tiny, invisible-mode flagged per page; visible/small-blue/white-on-black not flagged; excluded from case text until include_hidden confirms that page) + tests/unit/test_pdf_checks_api.py; pip-audit -r requirements.txt: no known vulnerabilities\"\n$B ac T-086 --check 1 --agent backend --evidence \"tests/unit/test_pdf_ocr.py + test_pdf_checks_api.py: real tesseract 5.5.2 OCR of a generated image-only PDF, page PNG served at GET /api/cases/{token}/pages/{n}/image, low_conf words marked, missing-tesseract -> clear 400 ocr_unavailable, OCR_DERIVED forces needs_review through a full pipeline run; tests skip when tesseract absent\"\n$B note T-086 --agent backend --text \"README install line (release owns README): macOS 'brew install tesseract'; Debian/Ubuntu 'sudo apt-get install tesseract-ocr' (English data; tested 5.5.2, 5.x accepted). Python dep pypdfium2==5.14.0 is in requirements.txt. UI needs: (1) on 400 pdf_no_text_layer with detail.scanned_pages and detail.ocr.available, offer 'Read scanned pages (OCR)' that re-posts the file with ?ocr=true; if detail.ocr.available is false show detail.ocr.message (install line). (2) Show GET /api/cases/{token}/pages/{n}/image beside the text of records with ocr_derived=true (record.page); mark pdf_pages[].low_conf spans (offsets into the case text). (3) Items carry reason OCR_DERIVED and a failing code step ocr_source in the stepper (next action READ_RECORD). (4) Contract: memory/contracts/api.md 'PDF hidden text and local OCR'. OCR is opt-in, max 10 scanned pages, 150s. Page images are stored base64 in cases.config_json (db could add a blob table later). Also: I edited tests/unit/test_provider.py and test_provider_backends.py to allow-list pdf_ocr.py for subprocess (local tesseract, not an LLM), with a test that pdf_ocr never names claude/anthropic. Commit 2fca530.\"\n$B note T-087 --agent backend --text \"UI needs: upload response and GET case carry pdf_checks.hidden_text {checked, pages[{page,count,items[{text,reasons,why}],excluded,confirmed}]}; render as a stepper step (checked=false => skipped). Hidden text is excluded from the case text; a 'Include hidden text on page N' action re-posts the file with ?include_hidden=N (or all), which creates a new case. A file whose only text is hidden is refused with detail.reason pdf_only_hidden_text and detail.hidden_text_pages. Limits: text hidden only by a clip path is not detected; text overlapping same-colour visible text counts as visible. Commit 2fca530. Also FYI for the billing owner: memory/contracts/api.md has the billing section inserted between the '## DELETE /api/cases/{token}' heading and its body.\"\n$B handoff T-087 --agent backend --text \"What changed: app/backend/pdf_hidden.py (pypdfium2 render vs text layer: invisible mode, transparent, off-page, tiny, background-coloured/covered), pdf_checks.py orchestration, pdf_text.extract now delegates; case text excludes hidden text until ?include_hidden confirms the page; api.md section. How verified: tests/unit/test_pdf_hidden.py + test_pdf_checks_api.py (synthetic PDFs built in the tests), full tests/unit green on the staged tree; pip-audit clean. Left: UI stepper step and confirm action (see notes). Surprised: PDF Tr state persists across BT/ET; a ledger of 'is it visible' is cheapest as a rendered-pixel spread check. Commit 2fca530.\"\n$B handoff T-086 --agent backend --text \"What changed: app/backend/pdf_ocr.py (tesseract subprocess, TSV parse, low-conf rule 60 / 80 for digit words, PNG page image), pdf_checks.py, pdf_routes.py (page image), OCR_DERIVED reason + ocr_source trace step, pipeline marks OCR-page items needs_review, api.md. How verified: tests/unit/test_pdf_ocr.py and test_pdf_checks_api.py with real tesseract 5.5.2 (skip if absent); full tests/unit green on the staged tree. Left: UI (see notes), README install line (release). Surprised: tesseract at 9pt/0.7 scale returns confident-looking garbage only partly flagged, so numbers get a stricter threshold. Commit 2fca530.\"\n$B commit T-086 --sha 2fca530 --agent backend; $B commit T-087 --sha 2fca530 --agent backend\n$B move T-086 in_review --agent backend; $B move T-087 in_review --agent backend"
}
````

### User / tool · 2026-11-02T04:31:17.381Z

**tool result**
````
AC 1 checked: tests/unit/test_pdf_hidden.py (17 tests: white, near-white, covered, off-page, tiny, scaled-tiny, invisible-mode flagged per page; visible/small-blue/white-on-black not flagged; excluded from case text until include_hidden confirms that page) + tests/unit/test_pdf_checks_api.py; pip-audit -r requirements.txt: no known vulnerabilities
AC 1 checked: tests/unit/test_pdf_ocr.py + test_pdf_checks_api.py: real tesseract 5.5.2 OCR of a generated image-only PDF, page PNG served at GET /api/cases/{token}/pages/{n}/image, low_conf words marked, missing-tesseract -> clear 400 ocr_unavailable, OCR_DERIVED forces needs_review through a full pipeline run; tests skip when tesseract absent
noted on T-086
noted on T-087
handoff written on T-087
handoff written on T-086
T-086: commit 2fca530 recorded
T-087: commit 2fca530 recorded
T-086: in_progress -> in_review
T-087: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:31:20.626Z

T-086 (local OCR) and T-087 (hidden-text detection) are both in `in_review`, in commit 2fca530. A full `tests/unit` run on a checkout of just that commit passes (1224 tests), and `pip-audit` on the pinned `pypdfium2==5.14.0` found nothing.

The mixed working tree had one `test_db.py` migration failure from another worker's in-flight db work, which I left alone.

- **Tests:** the OCR tests run against real Tesseract 5.5.2 and skip cleanly when it isn't installed.
- **Subprocess allow-list:** `pdf_ocr` is now allow-listed for subprocess in both `test_single_call_path` tests; anthropic imports stay banned. A new test checks that `pdf_ocr.py` never names `claude`.
- **Other worker's bug:** their billing section in `api.md` sits between the `## DELETE` heading and its body. I left it out of my commit and noted it on T-087.
- **UI and README:** the UI notes and the README install line are in the card notes.
