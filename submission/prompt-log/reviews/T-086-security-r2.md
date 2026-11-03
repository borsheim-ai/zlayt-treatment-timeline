# T-086 security review, round 2: local Tesseract OCR for scanned PDFs (security-reviewer)

**Verdict: pass (0 blockers, 0 majors, 0 minors, 2 nits).** All three round-1 findings that bind this card are fixed. The round-1 blocker (edit flips an OCR item to verified) is closed on every path I could reach. The pixel caps stop the 7200 pt page. Tesseract's environment holds no secret.

Pinned: `git archive 950d4a5` unpacked in the scratchpad (`head_950d4a5`). HEAD moved to e63e564 while I worked. `git diff --quiet 950d4a5 HEAD` on pdf_hidden.py, pdf_ocr.py, pdf_checks.py, pdf_text.py, confidence.py and reclassify.py returned rc=0, so those files are unchanged. review.py did change (24c18a7, D-047 hard 422 on edits). I re-ran test_ocr_invariant.py, test_pdf_hidden_r2.py, test_pdf_ocr_limits.py (53 passed) and the all-paths probe against a fresh archive of e63e564: `VIOLATIONS: none`.

Lens: subprocess and environment, render limits, the OCR needs_review invariant. OCR quality is outside my lens. T-087 is reviewed in `reviews/T-087-security-r2.md`.

## Round-1 findings, re-tested

| Round-1 finding | Result at 950d4a5 |
|---|---|
| blocker: edit makes an OCR item verified and drops OCR_DERIVED | Fixed. `probe_ocr_edit.py` now prints `after edit  : needs_review ['OCR_DERIVED']` and the same for the stored row (round 1: `verified None`). |
| major: no pixel or memory cap on the OCR render | Fixed. See the numbers below. |
| minor: tesseract inherits the full server environment | Fixed. Child env holds only PATH, TMPDIR, LC_CTYPE, OMP_THREAD_LIMIT (plus PWD, SHLVL, `_` that the shell wrapper adds). |
| nit: allow-list test checks only the `subprocess.run([` form | Not changed. Carried as a nit. |

## What I ran

- **OCR_DERIVED on every state-rewriting path** (`probe_r2_ocr_paths.py`, OCR-only and half-text/half-OCR cases): after the pipeline, after edit, accept, dismiss and reset, after rejudge, after `not_duplicate` (case_04, 4 live items then 5), after `reclassify` charge and not-a-charge both ways (11 items), and after `confirm_date` (case_01, 9 items), every live item on an OCR page was `needs_review` with `OCR_DERIVED`. Manual entry is covered by `test_manual_entry_on_an_ocr_record_is_needs_review_with_the_ocr_reason` (passes); my probe did not call `manual_entry` itself. The code now computes the flag in `_check_summary` (review.py `ocr_derived=` argument) and then runs `enforce_ocr` after edit, manual entry, confirm_date and not_duplicate, and `reclassify.py` passes `ocr_derived` into `compose_state`. I read the enforcement as belt and braces: two independent mechanisms.
- **Pixel caps** (`probe_dos.py bigpage`, a 1 KB PDF with a gray image page, `ocr=True`): 600 pt, 2500 pt and 2880 pt reach the OCR step (47, 65 and 66 MB peak RSS; the image is blank so the result is `pdf_no_text_layer`). 2881 pt, 7200 pt and 14400 pt return `ocr_page_too_large` in 0.1 s at 42 MB. Round 1 measured 2261 MB for 7200 pt.
- **Worst case inside the caps** (`probe_pngsize.py 2880 4000`, 15.6 MB noise PDF called directly): one page, 1.6 s, 198 MB RSS, 9.4 MB base64 PNG. Through `pdf_checks.extract(ocr=True)` (`probe_r2_pngcap.py 10`, 3.8 MB file, noise over 40-inch pages): `ocr_images_too_large` at page 3, 2.1 s, 165 MB RSS, nothing stored.
- **Environment** (`probe_r2_env.py`): a wrapper named `tesseract` first on PATH dumps its environment, then execs the real 5.5.2. I set dummy `ANTHROPIC_API_KEY=<redacted>`, `OPENAI_API_KEY=<redacted>`, `GITHUB_TOKEN=<redacted>`, `AWS_SECRET_ACCESS_KEY=<redacted>`, `ENABLE_LIVE=1` and `HOME` in the parent. Child env names: `LC_CTYPE, OMP_THREAD_LIMIT, PATH, PWD, SHLVL, TMPDIR, _`. "secret-like or HOME names in child env: none".
- `pytest -p no:cacheprovider` on test_pdf_hidden.py, test_pdf_hidden_r2.py, test_pdf_ocr.py, test_pdf_ocr_limits.py, test_ocr_invariant.py, test_pdf_checks_api.py, test_pdf_upload.py, test_provider.py, test_provider_backends.py at 950d4a5: 144 passed.
- `python3 tools/check_secrets.py`: ok (1801 files).

```json
{"card": "T-086", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of 950d4a5 (scratchpad head_950d4a5); app/backend/pdf_ocr.py, pdf_checks.py, review.py, reclassify.py, confidence.py; re-checked at HEAD e63e564 (pdf files unchanged, review.py changed, invariant re-run); local OCR via tesseract 5.5.2; sample: golden sample, case_01, case_04, reclassify bill text, crafted big-page and noise PDFs",
 "exercised": [
  "read personas/security.md, reviews/T-086-security.md, reviews/T-087-security.md, board.py show T-087, git show 950d4a5 for pdf_ocr.py, review.py, confidence.py, reclassify.py, pdf_text.py",
  "pytest -p no:cacheprovider on 9 PDF, OCR and provider test files at 950d4a5: 144 passed; test_ocr_invariant, test_pdf_hidden_r2, test_pdf_ocr_limits at e63e564: 53 passed",
  "probe_ocr_edit.py at 950d4a5: after edit needs_review ['OCR_DERIVED'], stored row the same",
  "probe_r2_ocr_paths.py at 950d4a5 and at e63e564: edit, accept, dismiss, reset, rejudge, not_duplicate, reclassify both ways, confirm_date, OCR-only and mixed pages; VIOLATIONS none",
  "probe_dos.py bigpage 600/2500/2880/2881/7200/14400 pt with ocr=True: 2881 pt and above refused ocr_page_too_large in 0.1 s at 42 MB RSS",
  "probe_pngsize.py 2880 pt noise: 198 MB RSS, 9.4 MB base64 PNG, 1.6 s; probe_r2_pngcap.py 10 pages: ocr_images_too_large at page 3, 165 MB RSS, 2.1 s",
  "probe_r2_env.py: wrapper tesseract dumped the child environment with dummy keys set in the parent (values <redacted>); no key-like name present",
  "python3 tools/check_secrets.py: ok (1801 files)"],
 "verdict": "pass",
 "scores": {"subprocess_isolation": 5, "temp_file_cleanup": 5, "render_resource_limits": 5, "ocr_needs_review_invariant": 5, "missing_tesseract_degradation": 5, "demo_gating": 5, "dependency_hygiene": 5, "allow_list_narrowness": 4},
 "findings": [
  {"severity": "nit",
   "title": "The pdf_ocr subprocess allow-list test still checks only the `subprocess.run([...])` form (carried from round 1)",
   "evidence": "tests/unit/test_pdf_ocr.py:136 `calls = re.findall(r\"subprocess\\.run\\(\\[([^,\\]]+)\", src)`. Unchanged since 2fca530. A later `subprocess.Popen(...)`, `shell=True` or `os.system` in pdf_ocr.py would pass it and test_single_call_path (which matches import lines only).",
   "why_it_matters": "The guard is correct today but would not catch drift in the one module that runs a non-LLM subprocess on the live path.",
   "fix": "In the same test also assert no `shell=True`, `Popen`, `os.system` or `os.popen` in the source, and that every `subprocess.run(` call has `timeout=`.",
   "acceptance_test": "Mutation: add `subprocess.Popen(['claude'])` or `shell=True` to pdf_ocr.py; the test fails."},
  {"severity": "nit",
   "title": "The stored-image cap counts raw PNG bytes (12 MiB) but the case keeps them base64, about 16 MiB per case",
   "evidence": "pdf_ocr.py:34 `MAX_STORED_PNG_BYTES = 12 * 1024 * 1024` is compared with `len(png)` (pdf_ocr.py:201), then `base64.b64encode(png)` (pdf_ocr.py:206) goes into config via api.py:276 `page_images`. Measured: one 2880 pt noise page gave 9.4 MB base64 (probe_pngsize.py).",
   "why_it_matters": "The cap is real and the bound is fine for a local or demo case, but the comment says 12 MiB while the database row can reach 16 MiB, and a hosted instance multiplies it by the number of retained cases.",
   "fix": "Count the base64 length, or lower the constant to 9 MiB so the stored size matches the stated one.",
   "acceptance_test": "Unit test: pages whose PNGs total 11 MiB are refused when the cap is stated as the stored size."}
 ],
 "whats_right": [
  "OCR_DERIVED is now enforced twice (compose_state context and enforce_ocr after each step), and the unit tests cover edit, second edit, accept, no-judge edit, manual entry, rejudge and a text-only control.",
  "The render clamp has three limits (40-inch page refusal, 3500 px side, 8 MP area) plus a 12 MiB stored-image cap; the 7200 pt page is refused in 0.1 s at 42 MB.",
  "Tesseract's environment is an allow-list taken at call time; a wrapper dump with dummy keys set shows no secret-like name."],
 "questions_for_chris": []}
```
