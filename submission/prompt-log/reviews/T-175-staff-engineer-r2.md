# T-175 r2 review, staff-engineer-reviewer

Verdict: pass (0 blockers, 0 majors, 2 minors).

Scope. The round-2 backend commit is cb6740b (app/backend/api.py, app/backend/case_list.py, tests/unit/test_case_list_race.py, memory/contracts/api.md). HEAD moved during the review: it was 30c04e6 when I started, and da0c7fe landed at 12:27 with the overview UI half (app/frontend/overview.js, tests/e2e/conftest.py, tests/e2e/test_mvp_finish.py). I checked the backend on archives of 30c04e6 and cb6740b, which are identical for app/ and tests/unit/. I checked the UI on an archive of da0c7fe. The findings apply to HEAD da0c7fe.

Brief checks, all run on git archive copies, fixture backend, local mode, no network:
- A case whose summary fails twice: status_error true, record_count, counts, progress and hitl null, message "We couldn't load this case's status", export_ready false, next_action null, exactly one ERROR log line naming RuntimeError, and no record text at any log level. PASS (probe_r2, checks A1 to A9).
- A real error on an existing case's route stays 500 internal on GET case and GET trace. A missing token stays 404. Mutant A (every per-case error becomes 404) turns two tests red. PASS (probe_r2 B1 to B5; mutants_r2 A).
- The narrowed probe except logs one WARNING naming the exception class and no text, and the original 500 stands. PASS (probe_r2 C1, C2).
- The race test is fast by default: 8 passed in 9.85 s on the archive, 11.58 s while the full suite ran alongside. PASS.
- Full unit suite on the archive: 5683 passed, 8 skipped in 321.85 s, rc 0. The unit tree at da0c7fe is identical (diff -rq shows no tests/unit difference), so the count applies. I did not rerun the full suite at da0c7fe.

Round-1 findings: major 1 is closed (null rows on the API, and the UI renders the message at da0c7fe). Major 2 is closed (mutant A is red). Minor 3 is closed (AC 1 evidence now cites overview.js and the e2e test). The probe-log nit and the 40 s nit are closed.

Two minors remain, and neither changes a figure the paralegal sees:
- The one re-read that succeeds is silent. Checklist 8 says retries are logged.
- plain_row swallows a failure in run_progress and in case_title with no log line. Checklist 12 wants failures visible.

Not exercised: the e2e suite, including the new cases-status-error tests in test_mvp_finish.py; clicking the Try again button; RACE_FULL=1; and a repeat of the concurrent probe from r1. The r1 probe result stands for this backend because the backend diff is empty.

Evidence is under artifacts/review-evidence/T-175-r2-staff/ (unit_full_head.txt, probe_r2.out.txt, mutants_r2.out.txt, probe_retry_log_r2.out.txt, render_r2.json, overview_broken_row.png for 30c04e6, and at_da0c7fe/ for da0c7fe).

```json
{"card": "T-175", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 2: backend commit cb6740b (app/backend/api.py, app/backend/case_list.py, tests/unit/test_case_list_race.py, memory/contracts/api.md) at git archive 30c04e6 (identical to cb6740b for app/ and tests/unit/); frontend commit da0c7fe (app/frontend/overview.js) landed at HEAD during the review and checked on its own archive; local-mode app, fixture backend, no network; sample library case case_lib01_er_only_then_gap",
 "exercised": [
  "python3 tools/board.py show T-175 (read-only): status in_review, commits 4a097b6 and cb6740b, AC 1 evidence and r2 handoff read",
  "git rev-parse HEAD: 30c04e6 at start, da0c7fe later in the review (HEAD moved); git diff --stat cb6740b HEAD: 30c04e6 touched tests/e2e/test_multicase.py only; git diff --stat cb6740b da0c7fe: 4 files including app/frontend/overview.js",
  "git show cb6740b -- app/backend/api.py app/backend/case_list.py (full diff read); git show cb6740b:tests/unit/test_case_list_race.py (whole file read, 8 tests)",
  "git archive 30c04e6 and git archive cb6740b into scratch trees and diff -rq: only tests/e2e/test_multicase.py differs; git archive da0c7fe into a third scratch tree and diff -rq against 30c04e6: only app/frontend/overview.js, tests/e2e/conftest.py and tests/e2e/test_mvp_finish.py differ",
  "pytest tests/unit/test_case_list_race.py -q on the 30c04e6 archive: 8 passed in 9.85s (default 40 rounds)",
  "pytest tests/unit -q on the 30c04e6 archive: 5683 passed, 8 skipped in 321.85s (0:05:21), rc 0; output in artifacts/review-evidence/T-175-r2-staff/unit_full_head.txt",
  "artifacts/review-evidence/T-175-r2-staff/probe_r2.py run with python -I against the 30c04e6 archive: RESULT 15 passed, 0 failed (A1 to A9: status_error true, null figures, plain message, one ERROR line with RuntimeError, no record text at any level; B1 to B5: 500 internal on GET case and trace, no text in body or log, 'unhandled ValueError at api.py:354' and 'api.py:615', missing token 404; C1 to C2: probe failure logs one WARNING naming OSError, original 500 stands); output probe_r2.out.txt",
  "artifacts/review-evidence/T-175-r2-staff/mutants_r2.py against the 30c04e6 archive, one exact-string mutation per copy: M0 control 8 passed; A every per-case error to 404 KILLED (2 failed); B probe failure silent KILLED (1); C probe failure to 404 KILLED (1); D never 404 for a gone case KILLED (2); E single read, no retry KILLED (1); F status_error false KILLED (1); G counts zero not null KILLED (1); H ERROR downgraded to WARNING KILLED (1); I ERROR log carries exception text KILLED (1); output mutants_r2.out.txt",
  "artifacts/review-evidence/T-175-r2-staff/probe_retry_log_r2.py (python -I): a case whose summary fails once and then works lists with its full row, status_error false, and logs nothing at any level: RETRY_SILENT; output probe_retry_log_r2.out.txt",
  "artifacts/review-evidence/T-175-r2-staff/render_r2.py (python -I, uvicorn thread on 127.0.0.1:7871, headless Chromium via Playwright) against the 30c04e6 archive: broken row reads Entries None, Flags None, Amounts None, Analysis done, no message (page_has_status_error_message false); healthy twin reads Entries 0 of 6, Flags 0 of 2, Amounts 0 of 2; render_r2.json and overview_broken_row.png, the screenshot viewed",
  "same render against the da0c7fe archive on port 7872: broken row shows the message 'We couldn't load this case's status' and a Try again button, with no counts, bars, None or Analysis done; healthy row unchanged; page_has_status_error_message true; at_da0c7fe/render_run.out.txt, at_da0c7fe/render_r2.json and at_da0c7fe/overview_broken_row.png (screenshot viewed)",
  "grep -rn status_error app/frontend tests/e2e at 30c04e6: 0 matches; git log -S status_error -- app/frontend tests/e2e: da0c7fe only; git merge-base --is-ancestor da0c7fe HEAD: ancestor",
  "read memory/contracts/api.md lines 709-711 (the frontend-shows-the-message claim); app/frontend/overview.js lines 20-26 and 115 at 30c04e6 (bars fallback to zero and the None text); lines 97-98 and 118-119 at da0c7fe (the new status_error branch)",
  "line citations checked by grep in the da0c7fe archive: case_list.py except sites at 217, 222, 244, 259; api.py probe except at 175-176; test names at test_case_list_race.py:35, 54, 77, 106, 134, 200, 216, 241",
  "not run: tests/e2e (including cases-status-error tests in test_mvp_finish.py), the Try again click, RACE_FULL=1, the concurrent r1 probe"
 ],
 "verdict": "pass",
 "scores": {"race_fixed_under_load": 4, "honest_failure_signalling": 4, "test_sensitivity": 5, "log_privacy_and_diagnosability": 4, "evidence_accuracy": 5},
 "findings": [
  {"severity": "minor",
   "title": "The one re-read that succeeds is silent: a case whose summary failed once leaves no log line",
   "evidence": "app/backend/case_list.py:244-249 in the da0c7fe archive: except Exception as e: err = type(e).__name__; then if attempt == 1: time.sleep(RETRY_PAUSE) with no log call. Repro: .venv/bin/python -I artifacts/review-evidence/T-175-r2-staff/probe_retry_log_r2.py <archive> prints zlayt records during the retried read: [] and RETRY_SILENT.",
   "why_it_matters": "Checklist 8 says retries are capped, change conditions and are logged, and that no retry loop hides a failure. Here a real defect that fails on the first read and succeeds on the second produces no trace at all. The row is correct, but the defect is invisible in logs, and the 200 hides it from any alarm.",
   "fix": "Log once at WARNING when the first attempt fails, with the exception class only and no case text, for example: case list: a case's status failed once (RuntimeError); reading it again. Keep the second-failure ERROR line as it is.",
   "acceptance_test": "In test_list_retries_a_case_whose_summary_fails_once_and_shows_its_full_row, assert exactly one WARNING record on the zlayt.api logger that names RuntimeError and does not contain the exception text. probe_retry_log_r2.py then prints RETRY_LOGGED."},
  {"severity": "minor",
   "title": "plain_row swallows failures in run_progress and case_title with no log line",
   "evidence": "app/backend/case_list.py:216-218: try: stage, done = run_progress(case, stages) / except Exception: stage, done = None, 0. Lines 220-223: try: title = case_title(conn, case) / except Exception: title = readable_title(None, case['source'], case['created_at']). Neither branch calls log.",
   "why_it_matters": "Checklist 12 wants errors to reach an explicit status and to be visible. The row does carry status_error true, so the page is not misled. But when run_progress or case_title is the thing that failed, the log has only the summary line, so the cause is not findable from the log.",
   "fix": "In both except branches, log type(e).__name__ at WARNING with no case text, then keep the same fallback values.",
   "acceptance_test": "Monkeypatch case_list.run_progress to raise OSError with a secret string, then GET /api/cases on a case whose summary fails twice. Assert status_error true and exactly one WARNING naming OSError, with no secret text at any level."}
 ],
 "whats_right": [
  "A case whose summary fails twice is listed with status_error true, the plain message and null figures, and logs one ERROR line naming only the exception class; no record text appears at any level (probe_r2 A1 to A9).",
  "Nine of nine single-anchor backend mutants are red, including the every-error-404 mutant that round 1 found surviving; the unmutated control is green (mutants_r2.out.txt).",
  "The UI half landed in da0c7fe and the rendered page shows the server message and Try again on the broken row, with no counts, bars or None (at_da0c7fe/overview_broken_row.png)."
 ],
 "questions_for_chris": []}
```
