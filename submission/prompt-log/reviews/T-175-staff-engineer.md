# T-175 review, staff-engineer-reviewer (round 1), commit 4a097b6

Verdict: changes (0 blockers, 2 majors, 1 minor, 1 nit).

The race is fixed and the fix holds under load. On a `git archive 4a097b6` copy I ran the new test file 5 times (5 passed each time), four concurrent probe runs (about 4,480 requests, 0 responses of 500), and the full unit suite (5680 passed, 8 skipped, 0 failed). A real error on an existing case still answers 500 and is logged as class plus app file:line, with no record text.

Two things stop a pass:
- A persistent bug in `case_list.summary` now shows up as plausible zero-count rows with no marker and only a WARNING in the log.
- No test says a real error on a per-case route still answers 500. A mutant that turns every such error into 404 passes all 5 tests.

HEAD is now 82e5909. The commits after 4a097b6 are frontend and docs only. `git diff --stat 4a097b6 HEAD` on the three T-175 files prints nothing.

Labels: every finding below violates a checklist item or the persona's honest-failure criterion. None is a style preference.

```json
{"card": "T-175", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 4a097b6 (git archive copy): app/backend/api.py, app/backend/case_list.py, tests/unit/test_case_list_race.py; local-mode app, fixture backend, no network; HEAD at review time 82e5909 (later commits are frontend/docs only)",
 "exercised": [
  "python3 tools/board.py show T-175; git show 4a097b6 (full diff of api.py and case_list.py, whole of tests/unit/test_case_list_race.py); reviews/T-173-staff-engineer.md finding 2",
  "git archive 4a097b6 into two scratch dirs; tests/unit/test_case_list_race.py run 5 times: 5 passed in 40.49s, 40.98s, 42.36s, 44.13s, 46.49s",
  "FULL unit suite on the archive: pytest tests/unit -q -> '5680 passed, 8 skipped in 359.01s (0:05:59)' (worker ran only a subset)",
  "artifacts/review-evidence/T-175-r1-staff/probe_concurrent.py (my own): 2 creators, 2 runners, 3 readers over case/status/trace/export/audit/judges/narrative/item/item-trace plus review accept/dismiss, 1 renamer, 2 deleters, 2 listers, shared token pool, 6 library cases; seeds 1-4 (25 s then 3 x 45 s): 234, 1536, 1460, 1250 requests, '5xx: 0 []' every run; WARNING lines 28, 201, 189, 118 show the race is actually hit (list left-out and per-case 404 mapped from TypeError, AttributeError and IntegrityError)",
  "artifacts/review-evidence/T-175-r1-staff/probe_real_error.py: real ValueError on an existing case -> GET case 500 'internal', log 'unhandled ValueError at api.py:354'; GET trace 500, 'api.py:615'; secret string absent from body and log; same error on a missing token -> 404; summary() raising for every case -> list 200 with zero rows (finding 1)",
  "artifacts/review-evidence/T-175-r1-staff/mutants.py: 6 single-anchor mutants on scratch copies, race test file at RACE_ITERATIONS=30: M1 summaries reverted -> 3 failed; M2 never-404 -> 1 failed; M3 every per-case error -> 404 -> 5 passed (survives); M4 plain_row removed -> 1 failed; M5 log loses frame -> 1 failed; M6 probe error -> 404 -> 5 passed (survives)",
  "grep of app/frontend/overview.js and tests/e2e/test_multicase.py at 4a097b6 for the overview load-error message (finding 3)",
  "git rev-parse HEAD (82e5909) and git diff --stat 4a097b6 HEAD on the three T-175 files (empty); no server processes started, nothing left running"
 ],
 "verdict": "changes",
 "scores": {"race_fixed_under_load": 5, "honest_failure_signalling": 2, "test_sensitivity": 3, "log_privacy_and_diagnosability": 5, "evidence_accuracy": 3},
 "findings": [
  {"severity": "major",
   "title": "A persistent bug in case_list.summary is turned into plausible zero-count rows: the list answers 200, no 500 and no marker, only a WARNING",
   "evidence": "app/backend/case_list.py:233 `except Exception as e` around summary(), then plain_row (case_list.py:205) returns record_count 0 (case_list.py:216), all counts 0, next_action None, export_ready False, with the same keys as a full row. tests/unit/test_case_list_race.py:70-71 asserts exactly that shape. Repro: python -I artifacts/review-evidence/T-175-r1-staff/probe_real_error.py <archive> prints 'full row: record_count 6 counts {pending: 10, ... needs_review: 2}', then with case_list.summary raising TypeError for every case: 'list with summary() always raising (persistent bug): 200 rows 1 first row record_count 0 counts {pending: 0, ...} export_ready False keys differ from full: False' and 'row has any marker of partial data: []'. The only trace is log.warning at case_list.py:241 'listed with its status only'.",
   "why_it_matters": "The fix is written for a transient mid-write case, but the except is not limited to that. Any real defect in summary (bad JSON column, a code regression) now shows a fully processed case as 0 records, 0 pending, nothing to do. That is a wrong fact shown as a true one, not an unknown. It is a silent fallback of the kind the dossier calls out: the failure is hidden from the page and from any 5xx alarm and surfaces only as a WARNING line. The old behaviour (500) was at least visible. 'Not export-ready' is the safe direction, so this is not rated blocker.",
   "fix": "Keep the list alive but make the degraded row say so: give plain_row null counts and record_count (or an explicit `partial: true` / `refreshing` field the overview can render as 'updating'), and log a genuine non-race failure at ERROR. Narrow the except to the race signature: after the failure, re-read the case; if it is gone skip it; if it exists and summary fails twice in a row, let the failure be reported instead of fabricating zeros.",
   "acceptance_test": "A unit test makes case_list.summary raise for a case that exists and is not changing; the response either lists that case with null counts plus a partial marker the test checks, or reports the failure, and never returns record_count 0 / counts 0 as if they were real. A second test keeps the mid-write case (summary fails once, then works) listed with its full row on the next read."},
  {"severity": "major",
   "title": "No test pins that a real error on an existing case's route still answers 500; a mutant that makes every per-case error a 404 passes all 5 tests",
   "evidence": "Mutant M3 (app/backend/api.py:172 `if DB.get_case(c, parts[3]) is None:` replaced by `if True:`) -> 'M3 ... -> 5 passed'. The only 500 assertion is tests/unit/test_case_list_race.py:176, on GET /api/cases, which the new handler skips (the 404 branch needs a case id in the path). The per-case test (test_case_list_race.py:96) accepts 200, 202, 204, 404 or 409 and never checks which. M6 (the probe's swallowed error returning 404) also passes. Behaviour today is correct (probe_real_error.py: 'GET case, case_view raises: 500 internal', log 'unhandled ValueError at api.py:354'), but nothing keeps it so.",
   "why_it_matters": "The risk of this fix is exactly the new 404 mapping: it must fire only when the case is gone. If someone loosens the existence test, every server bug on a per-case route becomes a quiet 'No such case' and the 500 alarm and the app-frame log line go with it. Checklist 13: a test must fail when the guard breaks.",
   "fix": "Add a test in test_case_list_race.py: create a case, monkeypatch present.case_view (and trace.case_trace) to raise ValueError('SECRET-RECORD-TEXT'), call GET /api/cases/<token> and /trace on the existing case, assert 500, code 'internal', no secret in body, and a log line 'unhandled ValueError at api.py:<n>' without the secret. Tighten test_routes_answer_404... to assert 404 for the routes that read the case twice, instead of a five-code allowance.",
   "acceptance_test": "Mutants M3 and M6 (above) each turn at least one test red on a scratch copy, and M2 still does."},
  {"severity": "minor",
   "title": "Card evidence says the overview retry message is not built, but it is built and has an e2e test at the reviewed commit",
   "evidence": "T-175 AC 1 evidence: 'Frontend retry message NOT done: app/frontend not mine, needs frontend card'. At 4a097b6, app/frontend/overview.js:139 builds data-testid cases-load-error with a 'Try again' button (cases-retry) and overview.js:209 sets 'We could not load your cases. Check the connection and try again.'; tests/e2e/test_multicase.py:335 test_a_failed_list_load_shows_a_sentence_and_a_retry_button_in_the_same_place fulfils GET /api/cases with a 500 and asserts that text. (I read these in git show 4a097b6; I did not run the e2e.)",
   "why_it_matters": "The AC is marked done with an evidence line that contradicts the repo. The wrong note will lead to a duplicate frontend card, or to someone thinking a gap exists that does not.",
   "fix": "Correct the evidence/handoff to cite overview.js:139,209 and the existing e2e as the retry half of AC 1; open no new frontend card for it.",
   "acceptance_test": "`python3 tools/board.py show T-175` AC 1 evidence names overview.js and test_multicase.py and no longer says the retry message is missing."},
  {"severity": "nit",
   "title": "Probe error is swallowed without a log line; the new stress test adds about 40 s to the unit run",
   "evidence": "app/backend/api.py:175-176 `except Exception:` / `pass` around the existence probe in unexpected_response (checklist 12; falls through to the 500, so the failure is still visible, but the probe failure itself is not logged). tests/unit/test_case_list_race.py:100 stress test: 5 passed in 40-46 s per run.",
   "why_it_matters": "A broken DB during the probe leaves no hint why the 404 path was not taken. The 40 s cost is paid on every full unit run.",
   "fix": "Log type(e).__name__ at WARNING in the probe's except; consider RACE_ITERATIONS default 60 (M1 is already killed at 30 iterations).",
   "acceptance_test": "A test makes DB.get_case raise inside the probe and finds one log line naming the exception class and no text."}
 ],
 "whats_right": [
  "Root cause named correctly (id list read, then each case re-read) and fixed at both sites: the list tolerates a vanished case and per-case routes answer 404; 4 probe runs of about 4,480 mixed requests gave 0 responses of 500.",
  "The 500 path stays honest: probe shows 500 'internal' with the log line naming the exception class and api.py:line, and the secret string appears in neither body nor log.",
  "The new test file is sensitive to the race itself: reverting summaries (M1), the 404 mapping (M2), plain_row (M4) or the log frame (M5) each turn at least one test red."
 ],
 "questions_for_chris": []}
```
