# T-087 security review, round 2: PDF hidden-text detection (security-reviewer)

**Verdict: changes (0 blockers, 2 majors, 1 minor).** All three round-1 majors are fixed for the files I used in round 1: 19 of 19 constructions are held back, a scan failure is fail-closed with pages listed, and the 226 KB slow file now stops at the deadline. Two new constructions still get through. A 2 KB file makes the scan run 127.6 s against a 10 s deadline, and a Widget annotation drawn over the text hides it from a reader but not from the scan.

Pinned: `git archive 950d4a5` unpacked in the scratchpad (`head_950d4a5`). HEAD moved to e63e564 while I worked. `git diff --quiet 950d4a5 HEAD` on pdf_hidden.py, pdf_checks.py, pdf_text.py, pdf_ocr.py, confidence.py and reclassify.py returned rc=0, so the code under test is unchanged at HEAD. The Widget bypass and the deadline probe are on files that did not move.

Lens: untrusted-PDF handling, grounding exclusion, resource limits. Whether a 48-level contrast threshold suits paralegals is a UX call I note but do not grade.

## Round-1 findings, re-tested

| Round-1 finding | Result at 950d4a5 |
|---|---|
| major: scan unavailable fails open | Fixed. 406 mutations, 16 where pypdf reads the plant and PDFium cannot scan (round 1: 21): 16 of 16 refused `pdf_only_hidden_text`, 0 planted in case text. A two-page file with the scan forced unavailable: refused, `unchecked_pages: [1, 2]`. One page forced to fail: page 1 kept, page 2 dropped, `checked: False`, `unchecked_pages: [2]`, listed as `(2, True, True)` (page, unchecked, excluded). Confirming `include_hidden=2` includes only page 2 text. |
| major: 9 of 19 constructions leak | Fixed. `probe_hidden.py`: all 19 print `planted_in_case_text: false` (white, dot, hairline, table border, striped cover, off-page, tiny, mode 3, form depth 1/5/14/15/16/17/30, OCG off, alpha 0, clip-to-nothing, checkbox). |
| major: no scan deadline | Fixed for the round-1 file (226 KB, 10 pages x 5000 wide objects): `POST -> 400 pdf_timeout after 10.0s`, process CPU 10.2 s and flat for 60 s (round 1: 69.7 s). Not fixed in general: see finding 1. |

## New bypass ideas (all through `pdf_checks.extract`, files in the scratchpad `r2o/bp`)

| Idea | File | Result |
|---|---|---|
| Image XObject over text | 1a opaque white image; 1b image with an SMask hole; 1c image at alpha 0.9 | Held (refused `pdf_only_hidden_text`). Caveat: these images cover the page's visible line as well, so the whole page was held. 4a below covers only the plant and shows the separation. |
| Clipping path | 2a clip to a 3 pt slit that falls in a word gap; 2b clip to a 7 pt window over the first glyph | 2a held. **2b leaks**: the planted string is in the case text. poppler counts 72 dark pixels in the band and PDFium 71, so a reader sees the letter "P". |
| Render mode 7 with a clip | 3a mode 7 plus a decoy mark in a word gap; 3b mode 7 alone; 3c mode 7 with a fill through the clip; 3d one-dot mode-7 clip, then black planted text | All held. 3d: poppler and PDFium both show 6 dark pixels (the dot), so PDFium implements the text clip. No bypass. |
| White text layer under a scanned image | 4a white plant under a full-width scan image; 4b white plant over a grey-200 scan image | 4a held. **4b leaks** (white on 200 grey is 55 levels, DIFF_MIN is 48). |
| Annotation appearance stream | 5a Square, 5c Stamp, 5b Widget, each with an opaque white AP over the plant | 5a and 5c held. **5b leaks**: poppler 0 dark pixels (covered), PDFium 4478 (not drawn). |

Two probes flagged `BYPASS` but are correct behaviour: 5d (annotation with the Hidden flag does not cover the text) and 5e (a FreeText annotation: the plant is plain visible text, and the annotation's `/Contents` never reaches the case text). I did not check 5d against poppler.

```json
{"card": "T-087", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of 950d4a5 (scratchpad head_950d4a5); app/backend/pdf_hidden.py, pdf_checks.py, pdf_text.py; HEAD e63e564 checked for drift (pdf files unchanged); 19 round-1 PDFs, 406 mutated PDFs, 16 new bypass PDFs, overlap-DoS PDFs; local live mode via TestClient; poppler pdftoppm as the independent viewer",
 "exercised": [
  "read personas/security.md, reviews/T-086-security.md, reviews/T-087-security.md, board.py show T-087 (card AC and limits note), pdf_hidden.py in full, pdf_checks.py in full",
  "pytest -p no:cacheprovider on test_pdf_hidden.py, test_pdf_hidden_r2.py, test_pdf_ocr.py, test_pdf_ocr_limits.py, test_ocr_invariant.py, test_pdf_checks_api.py, test_pdf_upload.py, test_provider.py, test_provider_backends.py at 950d4a5: 144 passed",
  "probe_hidden.py at 950d4a5: 19 of 19 planted_in_case_text false",
  "probe_r2_failopen.py: 406 mutations, 16 where pypdf reads the plant and the scan cannot run; 16 refused pdf_only_hidden_text, 0 planted in case text",
  "probe_r2_failclosed.py: scan unavailable on a 2-page file -> refused with unchecked_pages [1, 2]; page 2 forced to fail -> page 1 kept, page 2 excluded and listed; include_hidden=2 includes page 2 only",
  "probe_scan_time.py 10 5000 wide at 950d4a5: scan 7.9 s (round 1: 94.0 s); probe_api.py timing on the 226 KB file: 400 pdf_timeout at 10.0 s, process CPU flat at 10.2 s for 60 s",
  "probe_r2_deadline.py: scan(deadline=now+10) on 1 page of overlapping large text objects: 1000 objects at 400 pt -> HiddenScanTimeout after 25.2 s; 5000 at 400 pt -> 127.6 s; 5000 at 40 pt -> 14.4 s; cProfile of the 1000-object file: _exact_verdict 31 calls 20.0 s, 64 page.render calls 20.3 s, _mask_verdict 32 calls 7.1 s",
  "probe_api.py timing on the 2 KB 5000-object file: POST -> 400 pdf_timeout after 10.0 s, process CPU 19.4 s at +10 s, 29.4 at +20, 39.4 at +30, 49.2 at +40, 59.1 at +50, 68.9 s at +60",
  "probe_r2_bypass.py: 16 crafted PDFs (image over text x3, clip x2, mode 7 x3, white under scan x4, annotation x5)",
  "probe_r2_viewers.py: poppler pdftoppm vs PDFium dark-pixel counts in the planted row band for 5b (poppler 0, PDFium 4478), 5a (0, 0), 3d (6, 6), 3a (0, 0), 2b (72, 71), 4b (0, 0), 4c (0, 0), 4d (217, 279)",
  "probe_r2_failclosed.py section 3: pdf.init_forms() before render for the Widget file: dark pixels 4478 without and 4478 with init_forms, so init_forms alone does not draw it",
  "python3 tools/check_secrets.py: ok (1801 files)"],
 "verdict": "changes",
 "scores": {"hidden_text_detection_coverage": 4, "fail_closed_behaviour": 5, "resource_limits": 2, "excluded_from_grounding_when_detected": 5, "demo_gating": 5, "dependency_hygiene": 5},
 "findings": [
  {"severity": "major",
   "title": "The scan deadline is checked every 32 objects, so a 2 KB PDF keeps the worker running for minutes after the 400",
   "evidence": "pdf_hidden.py:267-269 ticks only when `n % CHECK_EVERY == 0` (CHECK_EVERY = 32); pdf_hidden.py:316 `_exact_verdict` makes two native `page.render` calls per object with no tick, and `exact_left = EXACT_MAX` (120) is reset per page (pdf_hidden.py:266); `_mask_verdict` (pdf_hidden.py:292-300) is a Python loop over rows times neighbouring boxes with no tick. probe_r2_deadline.py, scan(deadline=now+10): 1000 overlapping 400 pt text objects (1 KB) -> HiddenScanTimeout after 25.2 s; 5000 (2 KB) -> 127.6 s; 5000 at 40 pt -> 14.4 s. Through the API (probe_api.py timing, the 2 KB file): `POST 2KB -> 400 pdf_timeout after 10.0s wall`, then process CPU 19.4 s at +10, 39.4 at +30, 68.9 s at +60 after the response. cProfile (1000 objects): 64 page.render calls = 20.3 s of 27.6 s. The 100-page limit and the 20000-object cap multiply this (not run).",
   "why_it_matters": "OWASP LLM10 / unbounded consumption (checklist item 3 says every call has a timeout). The round-1 fix handles the 226 KB file, but a file 100 times smaller defeats it with the same symptom: the API answers 400 and the worker burns a core. Repeated uploads stack CPU-bound threads in the default threadpool. Live mode only (demo refuses PDFs), but live mode is the supported hosted path. The card's AC and handoff say the worker stops at the deadline; that is true only when the work is many cheap steps.",
   "fix": "Tick before every `_render` and every `_exact_verdict` call and every 64 rows of `_mask_verdict`; give the exact-test budget to the whole document, not each page; when more than N text boxes overlap a box (for example 200), skip straight to could_not_verify instead of testing it. A native render cannot be interrupted, so for a hard bound run `pdf_hidden.scan` in a child process that the parent kills at the deadline.",
   "acceptance_test": "Test: build 5000 overlapping 400 pt text objects (probe_r2_deadline.py 5000 400) and call scan(deadline=now+10): it raises HiddenScanTimeout within 15 s. API test: the same file returns 400 pdf_timeout and process CPU time is flat within 2 s of the response (time.process_time sampled at +5 s and +15 s differs by less than 1 s)."},
  {"severity": "major",
   "title": "A Widget annotation drawn over the text hides it from a reader but not from the scan",
   "evidence": "probe_r2_bypass.py file 5b_widget_annot_AP_opaque_cover: `<< /Type /Annot /Subtype /Widget /FT /Tx /Rect [0 690 600 720] /F 4 /AP << /N 6 0 R >> >>` over black planted text. Result: `{\"PLANTED_in_case_text\": true, ... \"held_back\": []}`. probe_r2_viewers.py: dark pixels in the planted row band, poppler = 0 (the AP covers the text), PDFium as the scan renders it = 4478 (cover not drawn). The same cover as a Square (5a) or Stamp (5c) annotation is held (`blends_with_background`). Adding `pdf.init_forms()` before render did not change the 4478 (probe_r2_failclosed.py section 3), so the fix is not that one line. pdf_hidden.py has no annotation handling (grep for annot returns only prose matches).",
   "why_it_matters": "This is the round-1 cover construction again by a different route: the planted text reaches the case text, can ground a quote, and goes to the model, while a paralegal in a conforming viewer sees a blank box. The control promises that text a reader cannot see is held until confirmed. Widget covers are easy to build and they are the one annotation type PDFium skips without a form environment.",
   "fix": "Enumerate annotations per page (`raw.FPDFPage_GetAnnotCount`, or `/Annots` through pypdf) and, for any annotation with an appearance stream whose `/Rect` overlaps a text object's box and that PDFium did not draw (Widget, or any subtype PDFium skips), mark those text objects `could_not_verify` so they are held and listed. Simplest safe rule: a page with any Widget annotation overlapping text is unchecked until confirmed.",
   "acceptance_test": "Add 5b as a test next to the 19: the planted text is held for its page and excluded from the case text, and the page is listed. Also add a Widget annotation that does not overlap any text and assert the page is not held (no false positives on real forms)."},
  {"severity": "minor",
   "title": "Visibility is a pixel count and a contrast step, not legibility: a one-glyph window, 48-level contrast and 3.0 pt text pass as visible",
   "evidence": "probe_r2_bypass.py, all with the 80-character plant included in the case text: 2b clip to a 7 pt window over the first glyph (poppler 72 dark px, PDFium 71: a reader sees one letter); 4b white text over a grey-200 scan image (difference 55 against DIFF_MIN = 48, pdf_hidden.py:34); 4c text colour 0.81 grey on white (difference 48); 4d black text at 3 pt (`_effective_size(...) < TINY_PT` with TINY_PT = 3.0, so exactly 3.0 passes). Module docstring discloses 'text hidden by a clip path alone is not detected'; the contrast and size cutoffs are stated as constants but not as bypasses.",
   "why_it_matters": "These are label-versus-design differences, not spec violations (clip is a disclosed limit): an attacker who wants the text in the case text can stay just inside each threshold. The effect is bounded because such text is faint, tiny or mostly clipped, and the injection scanner still runs, but the control's promise is about what a reader cannot see.",
   "fix": "State all four limits in the docstring and in the card's limits note. Optionally add a `low_legibility` reason for text under 5 pt or with a contrast step under 80 levels, and a clip rule that holds text whose visible fraction is under, say, 20 percent of its glyph area. This is a calibration call with a false-positive cost on real footnotes, so I leave the numbers to the owner.",
   "acceptance_test": "Tests for 2b, 4b, 4c and 4d assert either that the plant is held and listed, or that the limits note names each construction; the test file records which choice was made."}
 ],
 "whats_right": [
  "The differential render closes all 19 round-1 constructions (19 of 19 planted_in_case_text false), including the dot, hairline, striped cover and form depth 15 to 30 that beat the old pixel-spread test.",
  "Fail-closed is real and granular: a failed scan or a failed page is excluded, listed with `unchecked`, and only the confirmed page comes back with include_hidden; 16 of 16 pypdf-readable corrupt files are refused.",
  "PDFium implements the mode-7 text clip (3d: 6 dark pixels in both PDFium and poppler), and the new Square and Stamp annotation covers are held."],
 "questions_for_chris": []}
```

Correction (appended; reviews are append-only): in finding 3 the DIFF_MIN constant is at pdf_hidden.py:37 and TINY_PT at pdf_hidden.py:33, not :34 as written. The findings and numbers are unchanged.
