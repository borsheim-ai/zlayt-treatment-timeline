# T-054 r2 security review (security-reviewer, Tomás Rivas lens)

Verdict: **pass**. No blocker, no open major. The three r1 items that counted are resolved and verified: F1 (pypdf record text on stderr), F2 (unpinned parser) and F3 (extraction kept running past the cap). F4 is an accepted scope cut and is not a finding. Its SCOPE_CUTS row exists only in the uncommitted working tree, which I record as a minor (finding 4).

Model recorded as `claude-haiku-5-5`, the model this session runs as.

## Commit pinning

HEAD moved during the review: 37c0923 (the r1 fix, my starting point), then e83eb54, d796383, a27b358, bee1844, fa8a36e, 08764e7 (current). The reviewed code is `git archive d796383` at `artifacts/review-evidence/T-054-r2/head_d796383`. `git diff --stat d796383 HEAD -- app/backend/pdf_text.py app/backend/api.py tests/unit/test_pdf_upload.py requirements.txt` at 08764e7 shows only `app/backend/api.py` (15 insertions, 1 deletion). That change is a local-mode loopback guard (D-036, commit 08764e7) in the middleware and does not touch the PDF route. `pdf_text.py`, `test_pdf_upload.py` and `requirements.txt` are byte-identical from 37c0923 to 08764e7.

## Status of the r1 items

- **F1, pypdf writes record text to stderr (r1 major): resolved.** `app/backend/pdf_text.py:15-20` attaches a NullHandler to the `pypdf` logger, sets `propagate = False` and raises the level to CRITICAL+1. Probe run over the 300-mutation seed-54 corpus (`T-054-r2-probe.py log`): fix gives `stderr_lines=0 record_text_stderr_lines=0`; the control (same child, pypdf logger reset) gives `stderr_lines=616 record_text_stderr_lines=169`. The control shows the probe can detect the leak. Outcome counts are the same in both runs (ok 92, pdf_error 208, uncaught 0).
- **F2, dependency unpinned and unrecorded (r1 major): resolved, with minor residuals.** `requirements.txt:23` is `pypdf==6.21.4`. The file has 33 `==` pins and no unpinned lines. All 33 runtime pins match `.venv` `pip freeze` exactly (the only freeze-only names are the dev pins in `requirements-dev.txt`, which is expected). `pip-audit 2.10.1 -r requirements.txt --no-deps --disable-pip` printed "No known vulnerabilities found" and exited 0. Residuals are in finding 2.
- **F3, the time-capped parse keeps running (r1 minor): resolved in substance.** `pdf_text.py:50` checks the deadline between pages. Measured at the pinned code: a 5-page expansion with a 74 MB stream per page returns `pdf_unreadable` after 11.45 s against a 10 s cap (r1 measured 18.8 s for the same class of file, probe3 K). The overshoot is bounded to about one page. pypdf 6.21.4 also caps an array-based `/Contents` at 75,000,000 bytes in total (`LimitReachedError: Array-based stream has at least 148000001 > 75000000 output bytes`), so one page cannot cost more than about one page's worth of inflation. Residual in finding 3.
- **F4, invisible PDF text (r1 minor): accepted scope cut, not a finding.** See finding 4 for the record gap.

## Findings

Only minors. None are blockers or majors.

## What I did not change my mind about

Demo mode still refuses PDFs before reading or parsing (`api.py:233-234` at 37c0923, unchanged at 08764e7). Scanned and malformed inputs still return coded 4xx with no case row (`test_scanned_pdf_upload_is_refused_and_nothing_is_stored_or_called` and the other PDF tests pass at the pinned commit). Rate limit and daily spend cap remain waived by D-020 (r1 question still open, see questions).

## Exercised

Working directory `/Users/arsis/zlayt-pm-project` unless stated.

- `.venv/bin/python -m pytest tests/unit/test_pdf_upload.py -q 2>&1 | tail -2` at HEAD 37c0923 (working tree; the PDF files were clean against HEAD): `18 passed in 2.68s`.
- Same command in the pinned archive `artifacts/review-evidence/T-054-r2/head_d796383`, `-p no:cacheprovider`: `18 passed in 2.53s`.
- `git diff 4eebb2d 37c0923 -- app/backend/pdf_text.py tests/unit/test_pdf_upload.py requirements.txt requirements-dev.txt` (read the r1 diff).
- `.venv/bin/python -I artifacts/review-evidence/T-054-r2/T-054-r2-probe.py log`: fix and control output as quoted in F1.
- `.venv/bin/python -I artifacts/review-evidence/T-054-r2/T-054-r2-probe.py pins`: `pins=33 unpinned_lines=[]`; `requirements vs venv pip freeze mismatches: {...dev pins only...}`; PyPI release JSON for all 33 pins: vulnerabilities 0 for every name; httpx2 and httpcore2 metadata (see question 1).
- pip-audit in a scratch venv (`pip install pip-audit`, version 2.10.1): `pip-audit -r requirements.txt --no-deps --disable-pip`: "No known vulnerabilities found", exit 0.
- Inline timing (stdin heredoc, `PT.extract` in process, pinned `pdf_text.py` path printed): `pages=1 pdf_bytes=72512 outcome=pdf_no_text_layer elapsed_s=3.82`; `pages=5 pdf_bytes=361279 outcome=pdf_unreadable elapsed_s=11.45 cap_s=10.0`.
- Inline pypdf check at 74 MB, two and four streams in one page: `LimitReachedError Array-based stream has at least 148000001 > 75000000 output bytes`.
- `.venv/bin/python -I artifacts/review-evidence/T-054-r2/T-054-r2-probe.py budget`: k=1 74 MB `extract_s 3.93`; k=4 and k=8 gave `pdf_unreadable` at 0.1 s and 0.07 s. The k=4 cause is the 75 MB array cap above. I did not separately trace the k=8 exception (320 MB total, so it is consistent with the same cap).
- `.venv/bin/python tools/check_secrets.py`: `check_secrets: ok (998 file(s) scanned)`. The rc I captured was from `tail`, so I rely on the tool's own "ok" line.
- `git ls-files .env` empty; `which gitleaks` returned nothing (rc=1, gitleaks not installed).
- `git ls-files` for Makefile and Dockerfile: none. `grep -n pypdf memory/ENVIRONMENT.md`: no match.
- `git show HEAD:memory/SCOPE_CUTS.md | grep -n -i hidden`: no match at 08764e7 (rc=1). The row exists in the working tree only: `grep -n "^| 20 " memory/SCOPE_CUTS.md` shows `| 20 | PDF hidden/invisible text detection ... | M3 (T-054 F4) |`.
- Read `app/backend/pdf_text.py` (current), the PDF route in `app/backend/api.py` (r1 diff and 08764e7 diff).

**Not exercised:** gitleaks (not installed), a live uvicorn on :7860 (all HTTP runs were in-process), Playwright/UI (T-054 adds no UI), live LLM calls (none in the PDF path), the k=8 exception trace.

## Findings

```
finding 1 (resolved): F1 logs. Verified, see above. Test test_pypdf_writes_no_record_text_to_stderr_or_logs passes at the pinned commit.
finding 2 (minor): pip-audit is not wired into any test target, and pypdf is not recorded in memory/ENVIRONMENT.md.
   evidence: git ls-files shows no Makefile or Dockerfile; grep -n pypdf memory/ENVIRONMENT.md has no match; card T-054 still lists "release/ENVIRONMENT must list pypdf" as open (board/cards/T-054.md, r1 notes).
   why: the pins and the clean audit are good; the audit only runs when someone runs it by hand, so a future pin change can slip through.
   fix: when the M4 Makefile lands, add `pip-audit -r requirements.txt --no-deps --disable-pip` to the test target; record the pins in memory/ENVIRONMENT.md.
   acceptance: `make test` (or the test script) fails when pip-audit finds a vulnerability; `grep -c 'pypdf' memory/ENVIRONMENT.md` is at least 1.
finding 3 (minor): the cap test still uses a sleep stub; no test runs a real expansion.
   evidence: tests/unit/test_pdf_upload.py (test_slow_extraction_hits_the_time_cap, sleep stub, unchanged since r1); measured overshoot in the inline timing above.
   why: the F3 fix was verified by hand, not by the suite, so a regression to the between-pages check would not be caught.
   fix: add a test that builds a 5-page 74 MB expansion (pattern in the probe) and asserts extract() raises pdf_unreadable within EXTRACT_TIMEOUT_S + one page (about 15 s); mark it slow.
   acceptance: the test passes at HEAD and fails if pdf_text.py:50 is removed.
finding 4 (minor): the accepted scope cut for invisible PDF text is not committed.
   evidence: `git show HEAD:memory/SCOPE_CUTS.md | grep -n -i hidden` printed nothing (rc=1 at 08764e7); the row `| 20 | PDF hidden/invisible text detection ... | M3 (T-054 F4) |` is in the working tree only (`grep -n "^| 20 " memory/SCOPE_CUTS.md`).
   why: the cut is the reason F4 is not a finding; an uncommitted row does not survive a checkout.
   fix: orchestrator commits the SCOPE_CUTS row with the T-054 close.
   acceptance: `git show HEAD:memory/SCOPE_CUTS.md | grep -c "T-054 F4"` returns 1.
finding 5 (nit): warnings.catch_warnings() in extract() changes process-global warning filters from a worker thread.
   evidence: app/backend/pdf_text.py:41-42 (with warnings.catch_warnings(): warnings.simplefilter("ignore")).
   why: the context manager is not thread-safe, and the API runs extract in the threadpool; a concurrent warning can be hidden or restored in the wrong order. Not a leak, so nit.
   fix: filter the pypdf logger only (already silenced at import), or drop the context manager.
   acceptance: none required.
```

## Questions for Chris

1. `requirements.txt` pins `httpx2==2.16.0` and `httpcore2==2.16.0` as runtime dependencies. PyPI metadata shows the pydantic GitHub organisation (`https://github.com/pydantic/httpx2`), 22 releases, first upload 2026-05-11, and no known vulnerabilities. Which import needs them, and is that intended? (Both names are unfamiliar to me, so I checked the metadata rather than assume.)
2. D-020 cut the rate limit and daily spend cap, but the persona checklist, `docs/CONTRACT.md:314` and `MASTER_PROMPT.md:451` still require them for live mode. Does the cut stand for any `tailscale serve` exposure (`MASTER_PROMPT.md:227`)? (Carried from r1, unchanged.)

## Machine-readable record

```json
{"card": "T-054", "persona": "security-reviewer", "model": "claude-haiku-5-5",
 "scope": "T-054 r2 (fixes 37c0923). Reviewed code: git archive of HEAD d796383 at artifacts/review-evidence/T-054-r2/head_d796383 (HEAD moved to 08764e7; reviewed PDF files unchanged, api.py change at 08764e7 is the local-mode loopback guard, outside the PDF route). No app URL: HTTP not exercised; in-process probes only.",
 "exercised": [
  "pytest tests/unit/test_pdf_upload.py -q at HEAD 37c0923 (working tree): 18 passed in 2.68s",
  "pytest tests/unit/test_pdf_upload.py -q in pinned archive head_d796383: 18 passed in 2.53s",
  "git diff 4eebb2d 37c0923 for pdf_text.py, test_pdf_upload.py, requirements.txt, requirements-dev.txt",
  "artifacts/review-evidence/T-054-r2/T-054-r2-probe.py log: fix stderr_lines=0 record_text_stderr_lines=0 (ok 92, pdf_error 208, uncaught 0 of 300); control stderr_lines=616 record_text_stderr_lines=169",
  "artifacts/review-evidence/T-054-r2/T-054-r2-probe.py pins: pins=33 unpinned_lines=[]; freeze mismatches dev-only; PyPI vulnerabilities 0 for all 33; httpx2/httpcore2 metadata",
  "pip-audit 2.10.1 (scratch venv) -r requirements.txt --no-deps --disable-pip: No known vulnerabilities found, exit 0",
  "inline PT.extract timing: 1 page 74 MB 3.82 s; 5 pages 74 MB 11.45 s pdf_unreadable against 10 s cap",
  "inline pypdf 2 and 4 streams 74 MB in one page: LimitReachedError 148000001 > 75000000",
  "artifacts/review-evidence/T-054-r2/T-054-r2-probe.py budget: k=1 3.93 s; k=4, k=8 pdf_unreadable (cap)",
  "tools/check_secrets.py: check_secrets: ok (998 file(s) scanned)",
  "git ls-files .env empty; which gitleaks rc=1; git ls-files Makefile/Dockerfile none; grep pypdf memory/ENVIRONMENT.md none",
  "git show HEAD:memory/SCOPE_CUTS.md grep hidden: none; working-tree row 20 present",
  "git diff --stat d796383 HEAD over PDF surface: api.py only (local-mode guard)",
  "read app/backend/pdf_text.py, the PDF route in api.py, tests/unit/test_pdf_upload.py, requirements.txt, memory/SCOPE_CUTS.md",
  "not exercised: gitleaks (not installed), live uvicorn :7860, Playwright/UI, live LLM, k=8 exception trace"],
 "verdict": "pass",
 "scores": {"logs_exclude_record_text": 5, "dependency_pinned_and_recorded": 4, "parse_time_bounded": 4, "demo_mode_no_parse": 5, "size_limits_pdf": 4, "malformed_or_encrypted_4xx": 5, "scanned_refused_before_llm": 5, "secrets_clean": 5, "rate_limit_and_spend_cap": 3},
 "findings": [
  {"severity": "minor", "title": "pip-audit not in any test target; pypdf not recorded in ENVIRONMENT.md (F2 residual)",
   "evidence": "git ls-files: no Makefile or Dockerfile; grep -n pypdf memory/ENVIRONMENT.md: no match; board/cards/T-054.md r1 notes still list 'release/ENVIRONMENT must list pypdf' open",
   "why_it_matters": "A future pin change is only audited when someone runs pip-audit by hand.",
   "fix": "At the M4 Makefile, add pip-audit -r requirements.txt --no-deps --disable-pip to the test target; record pins in memory/ENVIRONMENT.md.",
   "acceptance_test": "The test target fails on a known vulnerability; grep -c pypdf memory/ENVIRONMENT.md >= 1."},
  {"severity": "minor", "title": "Time cap verified by hand only; the suite still uses a sleep stub (F3 residual)",
   "evidence": "tests/unit/test_pdf_upload.py test_slow_extraction_hits_the_time_cap (sleep stub); inline measurement 5 pages 74 MB pdf_unreadable at 11.45 s",
   "why_it_matters": "A regression to a between-pages check would pass the suite.",
   "fix": "Add a slow test with a real 5-page 74 MB expansion asserting pdf_unreadable within EXTRACT_TIMEOUT_S plus one page.",
   "acceptance_test": "Test passes at HEAD and fails if pdf_text.py:50 is removed."},
  {"severity": "minor", "title": "Accepted scope cut for invisible PDF text (F4) is uncommitted",
   "evidence": "git show HEAD:memory/SCOPE_CUTS.md | grep -n -i hidden: no match (rc=1 at 08764e7); working-tree row '| 20 | PDF hidden/invisible text detection ... | M3 (T-054 F4) |'",
   "why_it_matters": "The cut is the reason F4 is not a finding; an uncommitted row is lost on checkout.",
   "fix": "Commit the SCOPE_CUTS row with the T-054 close.",
   "acceptance_test": "git show HEAD:memory/SCOPE_CUTS.md | grep -c 'T-054 F4' returns 1."},
  {"severity": "nit", "title": "warnings.catch_warnings() in extract() modifies process-global filters from a worker thread",
   "evidence": "app/backend/pdf_text.py:41-42",
   "why_it_matters": "Not a leak; the context manager is not thread-safe under the threadpool.",
   "fix": "Rely on the pypdf logger silencing, or drop the context manager.",
   "acceptance_test": "none required"}
 ],
 "whats_right": [
  "The pypdf logger is cut off at import: 0 record-text stderr lines with the fix vs 169 with the control (T-054-r2-probe.py log).",
  "Parsing stops between pages at the 10 s cap: a 5-page 74 MB expansion returns in 11.45 s, down from 18.8 s at r1.",
  "requirements.txt pins pypdf==6.21.4 and the other 32 runtime packages; pip-audit reports no known vulnerabilities."
 ],
 "questions_for_chris": [
  "requirements.txt pins httpx2==2.16.0 and httpcore2==2.16.0 as runtime deps. PyPI metadata: pydantic GitHub org, 22 releases, first upload 2026-05-11. Which import needs them, and is that intended?",
  "D-020 cut the rate limit and daily spend cap, but the persona checklist, docs/CONTRACT.md:314 and MASTER_PROMPT.md:451 still require them for live mode. Does the cut stand for any tailscale serve exposure (MASTER_PROMPT.md:227)?"
 ]}
```
