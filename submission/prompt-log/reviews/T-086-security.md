# T-086 security review: local Tesseract OCR for scanned PDFs (security-reviewer, round 1)

**Verdict: fail (1 blocker, 1 major, 1 minor, 1 nit).**

Tested commit 2fca530 from a `git archive` copy in the scratchpad. `git worktree add` is refused for reviewers by board-guard, so I used the archive. The other agents' uncommitted edits were not in it. HEAD moved 02ff244, then bc12d44, then a850be0 while I worked. I re-ran the blocker probe and the hidden-text probe against a850be0 and got the same result. `git diff --stat 2fca530 HEAD` on the gate files shows `api.py`, `pipeline.py` and `review.py` changed (Spanish-record work). The `compose_state` call in `review.py` is unchanged.

Lens: the subprocess call, temp files, render limits, the OCR needs_review invariant, degradation, demo gating and the single-call-path allow-list. Clinical accuracy and OCR quality are outside my lens.

What passed (verified):
- **Subprocess call.** `pdf_ocr.py:138` uses a fixed argv list with no shell: `[tesseract, <tempdir>/page.png, "stdout", "-l", <lang>, "--psm", "3", "tsv"]`. The `-l` value is filtered against `--list-langs` output and defaults to `eng`. The path is server-generated and no user-controlled value reaches argv. Timeouts are 40 s per page and 150 s total. The cap is 10 OCR pages, enforced before any rendering (`pdf_checks.py:66`).
- **Temp files.** `tempfile.TemporaryDirectory` cleans up on success and on a forced timeout (`ocr_png(timeout=0.01)`). There were 0 leftover `zlayt-ocr-*` dirs and no tesseract process afterwards.
- **Missing tesseract.** It returns a clear 400 `ocr_unavailable` with the install line and stores nothing.
- **Demo gate.** `POST /api/cases/pdf`, `?ocr=true` and `?include_hidden=all` all return 409 `demo_mode_unsupported_input` before the body is read. The page-image route returns 404 for an unknown token.
- **Dependencies.** `pypdfium2==5.14.0` is pinned. `pip-audit 2.10.1 -r requirements.txt --no-deps --disable-pip` reports "No known vulnerabilities found".
- **Logs.** The new modules use no logger. Failures carry only exception class names. Malformed files produced 0 bytes on stderr.
- **Allow-list.** `test_single_call_path` allows `subprocess` only for `backend/pdf_ocr.py` and still bans the anthropic SDK there.
- **OCR text injection.** OCR text goes through the existing injection scanner. A scanned page reading "IGNORE ALL PREVIOUS INSTRUCTIONS" got `injection_tag=True` and `ocr_derived=True`.

Exercised: the 91 existing tests in the six PDF and provider test files, plus the probes under `artifacts/review-evidence/T-086-087/` (see JSON).

```json
{"card": "T-086", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 2fca530 (git archive copy in scratchpad); app/backend/pdf_ocr.py, pdf_checks.py, pdf_routes.py, review.py, pipeline.py:366; re-checked blocker and hidden-text probes at HEAD a850be0; local live mode and demo mode via TestClient; sample: generated image-only PDF and crafted PDFs",
 "exercised": [
  "read personas/security.md, board.py show T-086 and T-087, memory/ORCHESTRATOR_DECISIONS.md D-042, pdf_ocr.py, pdf_checks.py, pdf_routes.py, pdf_hidden.py, pdf_text.py, api.py PDF route, pipeline.py:366, review.py, rejudge.py, test_provider*.py allow-list",
  "pytest -p no:cacheprovider on tests/unit/test_pdf_hidden.py test_pdf_ocr.py test_pdf_checks_api.py test_pdf_upload.py test_provider.py test_provider_backends.py in the archive of 2fca530: 91 passed",
  "probe_dos.py malformed: truncated, garbage after header, header only, /Count 2000000000, page-tree loop, zero MediaBox, huge negative MediaBox, empty page tree: all clean 400 (pdf_unreadable, pdf_only_hidden_text, pdf_no_text_layer) or ok; 0 stderr bytes",
  "probe_dos.py bigpage with ocr=true: 600pt 62 MB RSS, 2500pt 315 MB RSS, 7200pt 2261 MB RSS in 3.8 s, from a 1 KB PDF",
  "probe_pngsize.py: 2.2 MB PDF with a noise image over a 3000pt page gives a 5.1 MB base64 PNG for one page, 460 MB RSS, 9.4 s",
  "probe_ocr_edit.py at 2fca530 and at a850be0: edit of an OCR-derived entry",
  "probe_ocr_injection.py: scanned page with injection text through POST /api/cases/pdf?ocr=true; temp dir cleanup after success and after forced timeout; pgrep tesseract",
  "probe_api.py: demo mode (no ENABLE_LIVE) refusal for plain, ?ocr=true, ?include_hidden=all; page image 404",
  "pip-audit 2.10.1 on requirements.txt (--no-deps --disable-pip): no known vulnerabilities; python3 tools/check_secrets.py: ok (1788 files)",
  "grep of logger/print use in the new modules and of hidden_text/page_images consumers in app/"],
 "verdict": "fail",
 "scores": {"subprocess_isolation": 5, "temp_file_cleanup": 5, "render_resource_limits": 2, "ocr_needs_review_invariant": 1, "missing_tesseract_degradation": 5, "demo_gating": 5, "dependency_hygiene": 5, "allow_list_narrowness": 4},
 "findings": [
  {"severity": "blocker",
   "title": "Editing an OCR-derived entry flips it to verified and drops OCR_DERIVED",
   "evidence": "review.py:107 (2fca530; moved to about :109 at a850be0): `_check_summary` ends with `confidence.compose_state({grounding_failures, code_reasons, judge}, {injection, date_status})`, which has no OCR input. `_edit` then writes `DB.update_item(... state=state, state_reasons_json=reasons ...)` (review.py:166). Reproduction: .venv/bin/python -I artifacts/review-evidence/T-086-087/probe_ocr_edit.py <archive> <tmp> (OCR page case, full pipeline with test fakes, then `RV.apply_review(... action=edit, edits={summary: ...}, call=judge supported)`). Output at 2fca530 and again at a850be0: `before edit : e1 needs_review ['OCR_DERIVED']` / `after edit  : verified None` / `stored row  : verified []`. manual_entry (review.py:309) uses the same `_check_summary` state with no OCR input, so a manual entry on an OCR record is `verified` too (read from code, not run).",
   "why_it_matters": "D-042 and the AC say OCR-derived items are ALWAYS needs_review. A one-word edit makes an item that came from a possibly misread digit or date show as verified, with the OCR reason gone from the stepper (the ocr_source step only appears while OCR_DERIVED is in the reasons). The 'verified' state is the product's claim that code, judge and human all checked. The paralegal's edit does not show that they compared the words with the page image. The existing test only covers the pipeline path, not the edit path.",
   "fix": "Make OCR_DERIVED a context input to compose_state (for example ctx key `ocr_derived`) and have `_check_summary`, `manual_entry` and `not_duplicate` compute it from `pdf_checks.is_ocr_span(case.config.pages, rec.char_start, rec.char_end)`. Alternatively carry forward any OCR_DERIVED already in `item.state_reasons`. Also assert it in rejudge.recompose, which today keeps it only because `keep` retains non-judge reasons.",
   "acceptance_test": "Unit test: seed an OCR-page case (as test_every_item_on_an_ocr_page_is_needs_review_after_a_full_run does), then `apply_review(action=edit)` with a supported judge, and `manual_entry` on a rejected OCR record. Assert state == needs_review and 'OCR_DERIVED' in state_reasons after each, and that the stepper ocr_source step is still FAIL."},
  {"severity": "major",
   "title": "OCR page render has no pixel or memory cap: a 1 KB PDF takes 2.3 GB, and the stored page image is unbounded",
   "evidence": "pdf_ocr.py:87 `page.render(scale=DPI / 72.0)` with no clamp on the MediaBox (compare pdf_hidden.py:22 and :89, which clamp to 3200 px). Page size is not limited (PDF allows 14400 pt). Then `bytes(bitmap.buffer)` (:90), a rows list (:96) and a zlib copy (:80) hold three or more full copies. probe_dos.py bigpage, ocr=true, 1 KB file: 600pt -> 62 MB RSS; 2500pt -> 315 MB; 7200pt (15000x15000 px) -> 2261 MB RSS, 3.8 s. At 14400pt (30000x30000 px) the same scaling gives roughly 9 GB (extrapolated, not run). The 150 s budget bounds time, not memory. Stored size: probe_pngsize.py, 2.2 MB PDF, noise image over a 3000pt page -> 5.1 MB base64 PNG for one page, 460 MB RSS; up to 10 such pages go into cases.config_json (api.py:276).",
   "why_it_matters": "OWASP LLM10 / unbounded consumption (checklist items 1 and 3). The card claims size and page caps. The page-count cap exists (10) but nothing bounds pixels per page, so one small upload can OOM-kill the process, including on a small container. It is gated to live mode only (demo refuses), but ENABLE_LIVE is the supported local and hosted live path.",
   "fix": "Clamp the render scale so max(width, height) in pixels is at most about 3500 (A4 or Letter at 150 dpi is 1754x1240; the pdf_hidden MAX_SIDE_PX pattern). Refuse (ocr_failed with a message) pages whose MediaBox exceeds a sane size such as 40 inches. Cap total stored page-image bytes per case (for example 10 MB) and fail with a clear message if exceeded. Build the greyscale PNG row by row instead of holding three copies.",
   "acceptance_test": "Test: a 1 KB PDF with an image page and MediaBox `0 0 14400 14400` plus ocr=true returns a 400 (page too large) or renders at a clamped size, and peak RSS stays under 300 MB (resource.getrusage in a child). Test: stored page_images total over the cap returns ocr_failed or ocr_too_large and stores nothing."},
  {"severity": "minor",
   "title": "Tesseract inherits the whole server environment, including any API key",
   "evidence": "pdf_ocr.py:33 `_ENV = {**os.environ, \"OMP_THREAD_LIMIT\": \"1\"}` is passed to all three subprocess.run calls (:55, :59, :138). The existing claude-cli backend strips ANTHROPIC_API_KEY from its child env (test_provider.py::test_cli_runs_outside_project_with_timeout_and_no_api_key). Tesseract needs only PATH, HOME or TMPDIR, TESSDATA_PREFIX and OMP_THREAD_LIMIT.",
   "why_it_matters": "Least privilege. A bug in tesseract or leptonica parsing an attacker-controlled image would run with the API key in its environment. This is low likelihood but cheap to remove, and the module is the only non-LLM subprocess on the public live path.",
   "fix": "Build `_ENV` from an allow-list: PATH, TMPDIR, TESSDATA_PREFIX, LANG, plus OMP_THREAD_LIMIT=1. Take it per call instead of at import so test monkeypatching works.",
   "acceptance_test": "Unit test: monkeypatch subprocess.run, set ANTHROPIC_API_KEY=<redacted> call ocr_png, and assert the env passed does not contain ANTHROPIC_API_KEY or any other `*_KEY` variable."},
  {"severity": "nit",
   "title": "The pdf_ocr subprocess allow-list test checks only the `subprocess.run([...])` form",
   "evidence": "test_pdf_ocr.py::test_pdf_ocr_only_runs_tesseract uses `re.findall(r\"subprocess\\.run\\(\\[([^,\\]]+)\", src)`. A later `subprocess.Popen(...)`, `shell=True` or `os.system` addition in pdf_ocr.py would pass test_single_call_path (which matches only import lines) and this test. The allow-list itself is narrow: one file, and the anthropic import is still banned there.",
   "why_it_matters": "The allow-list was added in the same commit as the code it protects. It is currently correct but would not catch drift.",
   "fix": "In the same test also assert that the source has no `shell=True`, `Popen`, `os.system` or `os.popen`, and that every `subprocess.run(` call has `timeout=`.",
   "acceptance_test": "Mutation: add `subprocess.Popen(['claude'])` or `shell=True` to pdf_ocr.py; the test fails."}
 ],
 "whats_right": [
  "The tesseract call is a fixed argv list with no shell, a server-generated path inside a TemporaryDirectory, a per-page and a total timeout, and a hard 10-page cap checked before rendering.",
  "Missing tesseract gives a clear 400 ocr_unavailable with the install line and stores nothing; demo mode refuses every PDF variant (plain, ocr, include_hidden) before reading the body.",
  "Temp dirs and processes are cleaned up on timeout, and pypdfium2 is pinned and pip-audit clean."],
 "questions_for_chris": ["D-042 says OCR-derived items always need review. I treated that as binding even after a paralegal edit, because the edit does not show the page image was compared. If you would rather let an edit clear it, the rule needs to say so in D-042 and the stepper should record who cleared it."]}
```
