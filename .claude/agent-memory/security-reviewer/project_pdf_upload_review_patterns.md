---
name: pdf-upload-review-patterns
description: Recurring security weak spots in the Zlayt PDF text-layer upload (T-054, pypdf): log leakage, unpinned parser, demo-gate ordering, parse-time DoS; probes to rerun
metadata:
  type: project
---

PDF upload (`app/backend/pdf_text.py`, route `POST /api/cases/pdf` in `app/backend/api.py`) was reviewed on T-054 (2026-11-01, HEAD 4eebb2d; the PDF surface was unchanged from c61e84f on).

- pypdf logs through `logging.getLogger("pypdf...")` at WARNING/ERROR with the failing content-stream fragment in the message, so record text reaches stderr whenever a PDF has a syntax glitch. Reproduce with 300 seeded byte mutations of `tests/unit/_pdf.sample_pdf`; suppression via NullHandler + `propagate=False` removes all of it. Check this in any new parser or any PDF/DOCX/OCR path.
- pypdf 6.21.4 caps each inflated stream at 75 MB (`pypdf.filters.ZLIB_MAX_OUTPUT_LENGTH`) but not the document total. Measured about 3.7 s per 74 MB page; a 5 MB upload with about 70 such pages is minutes of CPU. The fix was a demo-gate-first refusal plus a threadpool and a 10 s `asyncio.wait_for`, but the thread keeps running after the 10 s cap.
- Demo gate ordering matters: the gate ran after parsing at 5650eae. The fixed route refuses before reading the body. Check the order again after any route change.
- No version pin or manifest: the card said "release/ENVIRONMENT must list pypdf" and it was still open. Check `git ls-files` for requirements/pyproject/Dockerfile before accepting any new third-party parser.
- Encrypted PDFs (real ones, written by pypdf with a password) return `pdf_encrypted`; printf-crafted "encrypted" files only give `pdf_unreadable`. Both are 400 and never 500.
- Invisible text (render mode 3) is extracted verbatim. The injection scanner (`app/backend/injection.py` lexicon) still fires on phrasing like "ignore prior instructions", but the case shows text that is not visible in the source.
- Rate limiter and spend cap were cut by D-020 (ADR-015). The persona checklist and `docs/CONTRACT.md:314` still require them. Treat as a question for Chris, not a finding, unless live mode is exposed beyond local use.

T-054 r2 (2026-11-01, HEAD d796383, later 08764e7): F1 (logs) and F2 (pins; pip-audit 2.10.1 clean on 33 runtime pins) are resolved; F3 measured 5 pages x 74 MB stopping at 11.45 s against the 10 s cap. The deadline check is between pages only, and pypdf 6.21.4 caps an array-based `/Contents` at 75,000,000 bytes in total (`LimitReachedError`), so one page cannot exceed about one page of inflation. The earlier "K streams x 75 MB" worst case does not hold. Probe files: `artifacts/review-evidence/T-054-r2/T-054-r2-probe.py log|budget|pins`.

**How to apply:** rerun `artifacts/review-evidence/T-054-security-probe.py live`, `-probe2.py`, `-probe3.py` (flate timing), `-probe4.py` (HTTP timing, demo vs live-local) and `-probe5.py plain|suppressed` (log leak) on any PDF change. Check `git diff --stat <last-reviewed-sha> HEAD -- app/backend/pdf_text.py app/backend/api.py tests/unit/test_pdf_upload.py` first.
