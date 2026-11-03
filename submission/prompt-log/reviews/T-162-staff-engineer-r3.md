# T-162 r3 review (staff-engineer-reviewer)

Verdict: **changes**. No blocker. One major: the round-2 dead-panel gap is closed for throws, but the no-console smoke still passes when a panel swallows its render error, because `manual` is asserted for mount only.

Reviewed sha: 9db2cec (HEAD at start and at end; `git diff --name-only 9db2cec HEAD -- app/frontend tests/e2e` lists 0 files). Everything below ran on `git archive 9db2cec` in a unique scratch dir, on my own ports 7896-7900, with `E2E_REQUIRE_DB=1`.

What holds:
- Round-2 repro closed. Throws at the batch callback (batch.js:97, M6), the manual callback (manual.js:65, M7) and the top of mountSection (review.js:497, M5) each turn `test_no_console_errors.py` red. Before, M6 left the spec at 2/2 green.
- All seven side panels mount at HEAD. Six draw content on both fixtures; `manual` mounts and draws nothing (see the finding).
- Round-2 minors are fixed: `to_have_count(1)` precedes both `to_be_hidden` checks, `timeline.js:77` calls `rerunMarker` unguarded, and `test_every_registered_panel_is_listed` greps the seven registrations.

Results at HEAD 9db2cec (port 7896, fixture backend, ZLAYT_MODE=local, curated set):
- `E2E_BASE_URL=http://127.0.0.1:7896 ZLAYT_DB=<scratch>/head/data/head.sqlite3 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_no_console_errors.py tests/e2e/test_rerun_note.py -v` gives `7 passed in 8.77s` (4/4 no_console_errors, 3/3 rerun_note).
- Panel probe (sample and library case): batch Accept-all bar in `.toolbar > .rv-batchbar` (1 on both); audit 87 chars; charges 1595 and 2490; export-settings 335; flags 5135 and 4040; narrative 266; manual 0 chars; `panel-error` 0; `pageerror` none.
- `tests/unit/test_e2e_contract.py`: 3 passed.

Mutants (each a copy of the archive with one edit; diffs in `artifacts/review-evidence/T-162-r3/mutants-r3.patch`):

| id | edit | port | result of `test_no_console_errors.py` |
|---|---|---|---|
| M5 | throw at top of mountSection (review.js:497) | 7900 | 3 failed, 1 passed; first failure :66 "side panel 'batch' did not mount" |
| M6 | throw at top of batch callback (batch.js:97) | 7897 | 3 failed, 1 passed; :68 batch bar 0 elements; :108 pageerror and window.onerror "zlUndefinedName is not defined" |
| M7 | throw at top of manual callback (manual.js:65) | 7898 | 3 failed, 1 passed; :71 "a side panel reported that it threw" |
| M8 | M7 plus review.js:503 `catch (err) { /* swallowed */ }` | 7899 | **4 passed in 5.65s** |

## Finding (major): a swallowed render error in `manual` passes the smoke

Evidence: M8 is the swallow mutant. Repro: `cd <scratch>/T162_r3/mut8 && E2E_BASE_URL=http://127.0.0.1:7899 ZLAYT_DB=<scratch>/T162_r3/mut8/data/mut8.sqlite3 E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_no_console_errors.py -v` gives `4 passed in 5.65s`. The probe on :7899 reports `panel manual mounted=1 chars=0`, `panel-error notices=0`, `page errors=[]`. The spec exempts manual from the content check at `tests/e2e/test_no_console_errors.py:69` (`elif name != "manual":`), so line 70 never runs for it. Line 71 counts `panel-error`, which the swallow removes. Neither `manual` check can see a throw that is caught and not reported. M7 (same throw, reported) is red at :71; M8 is green.

Why it matters: the brief and the spec's docstring (lines 1-3) say every side panel must draw content and that a swallowed error must fail. Neither holds for `manual`. On both fixtures `manual` draws nothing: `btn-manual-entry` 0, `missing-entry` 0, no `[data-panel=manual]` children. So the only signal for it is `panel-error`, and that is the signal a swallow removes. The product is correct at HEAD (the wrapper reports, so no swallow exists in product code). This is a guard gap, the same class as r2's major, and it is rated major, not blocker, for that reason.

Fix: (1) in `app/frontend/review.js:503` (frontend), set a marker on the section after `render(sec, c)` returns normally, for example `sec.setAttribute("data-rendered", "")`. (2) In `test_no_console_errors.py` (qa), assert `[data-panel="<name>"][data-rendered]` has count 1 for all seven names, including manual, before the `panel-error` check. Do not reach for a manual fixture: neither the sample nor the library case has a missing-entry or unclear card for it. Also correct the docstring at lines 1-3 if manual stays mount-only.

Acceptance test: on a git archive of the fixed commit, `E2E_REQUIRE_DB=1 pytest tests/e2e/test_no_console_errors.py`: (1) M8 is red at the new `data-rendered` assertion; (2) M5, M6 and M7 stay red; (3) unmodified HEAD stays 4/4 green. Not run by me: the swallow mutant on a content-bearing panel. I expect the content check to catch it, but that is untested.

Out of brief, not run: full `pytest tests/unit`; `tests/e2e/test_charge_confirm.py`.

Questions for Chris: carried from r2 and still open in the card handoff. Should a decided entry's note also appear in its "Why this status" dialog? The AC says "row and trace", and entries have no trace button at HEAD. The spec asserts the row only for entries.

```json
{
 "card": "T-162",
 "persona": "staff-engineer-reviewer",
 "model": "claude-haiku-5-5",
 "scope": "reviewed sha 9db2cec (HEAD at start and end; app/frontend and tests/e2e unchanged since 9db2cec); git archive 9db2cec in /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T162_r3/head; own servers :7896 (HEAD) and :7897-:7900 (mutants M6, M7, M8, M5); fixture backend, ZLAYT_MODE=local, FIXTURE_SET=curated; sample case and library case case_lib06_lop_billed_vs_adjusted; test_no_console_errors.py and test_rerun_note.py; decided fixture",
 "exercised": [
  "read personas/staff-engineer.md; reviews/T-162-staff-engineer-r2.md; python3 tools/board.py show T-162 (AC 1 evidence 9db2cec, handoff, notes, rounds 2)",
  "git rev-parse HEAD -> 9db2cec at start and end; git diff --name-only 9db2cec HEAD -- app/frontend tests/e2e -> 0 files",
  "git archive 9db2cec | tar -x into <scratch>/T162_r3/head; mutants mut5-mut8 are the same archive with one edit each, diffs in artifacts/review-evidence/T-162-r3/mutants-r3.patch",
  "HEAD server PORT=7896 HOST=127.0.0.1 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated: /api/health 200; listener PID 26487 (ps: python -m app.main, lsof 127.0.0.1:7896 LISTEN)",
  "E2E_BASE_URL=http://127.0.0.1:7896 ZLAYT_DB=<scratch>/T162_r3/head/data/head.sqlite3 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_no_console_errors.py tests/e2e/test_rerun_note.py -v -> 7 passed in 8.77s (4 no_console_errors incl. test_every_registered_panel_is_listed; 3 rerun_note)",
  "artifacts/review-evidence/T-162-r3/panels.py against :7896 (sample and library): mounted/chars per panel: batch 0 in section with the toolbar bar present; audit 87; charges 1595 and 2490; export-settings 335; flags 5135 and 4040; narrative 266; manual 0; panel-error 0; pageerror none",
  "artifacts/review-evidence/T-162-r3/manual_probe.py against :7896: btn-manual-entry 0, missing-entry 0, tray-item 0 (sample) and 1 (library), .toolbar > .rv-batchbar 1 on both",
  ".venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q (archive) -> 3 passed",
  "M6 (throw at top of batch callback, batch.js:97), PORT 7897, listener PID 27967 -> test_no_console_errors.py 3 failed, 1 passed; :68 batch bar 0 elements; :108 pageerror + window.onerror 'zlUndefinedName is not defined'",
  "M7 (throw at top of manual callback, manual.js:65), PORT 7898, listener PID 27976 -> 3 failed, 1 passed; :71 'a side panel reported that it threw'",
  "M5 (throw at top of mountSection, review.js:497), PORT 7900, listener PID 30187 -> 3 failed, 1 passed; first failure :66 \"side panel 'batch' did not mount its root element on the sample case\"",
  "M8 (M7 plus review.js:503 'catch (err) { /* swallowed */ }'), PORT 7899, listener PID 29389 -> 4 passed in 5.65s; probe: manual mounted=1 chars=0, panel-error 0, page errors []",
  "not run: swallow mutant on a content-bearing panel (expected red at its content check, untested); full pytest tests/unit; tests/e2e/test_charge_confirm.py",
  "servers stopped: PIDs 26487, 27967, 27976, 29389, 30187, each checked with ps and lsof before kill; ports 7896-7900 confirmed closed. One git-guard hook block on an rm with an unresolved expansion; no files were deleted, and mutant trees were rebuilt with git archive into new directories"
 ],
 "verdict": "changes",
 "scores": {
  "dead_panel_detection": 5,
  "swallowed_error_detection": 2,
  "all_panels_mount_at_head": 5,
  "all_panels_content_asserted": 3,
  "rerun_note_spec_at_head": 5,
  "r2_minors_fixed": 5,
  "evidence_reproduces_at_head": 5
 },
 "findings": [
  {
   "severity": "major",
   "title": "The no-console smoke still passes when a panel swallows its render error: manual asserts mount only, so neither its content nor its panel-error notice is checked",
   "evidence": "Mutant M8 (artifacts/review-evidence/T-162-r3/mutants-r3.patch: manual.js:66 throw plus review.js:503 'catch (err) { /* swallowed */ }') on PORT 7899: 'E2E_BASE_URL=http://127.0.0.1:7899 ZLAYT_DB=<scratch>/T162_r3/mut8/data/mut8.sqlite3 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_no_console_errors.py -v' -> '4 passed in 5.65s'. Probe: 'panel manual mounted=1 chars=0', 'panel-error notices=0', 'page errors=[]'. Spec: tests/e2e/test_no_console_errors.py:69 'elif name != \"manual\":' skips the content check at :70; :71 counts panel-error, which the swallow removes. Same throw with the reporting wrapper (M7, PORT 7898) is red at :71.",
   "why_it_matters": "The brief and the spec docstring (test_no_console_errors.py lines 1-3) say every side panel must draw content and that a swallowed error must fail the smoke. For manual neither holds: on both fixtures manual draws nothing (btn-manual-entry 0, missing-entry 0), so its only signal is panel-error, and a swallow removes that signal. The product is correct at HEAD (review.js:503 reports), so this is a guard gap, not a present defect, and is rated major by the same logic as the r2 finding.",
   "fix": "(frontend, review.js:503) after 'render(sec, c)' returns normally, set a marker on the section, e.g. sec.setAttribute('data-rendered', ''). (qa, test_no_console_errors.py) in _loads_clean, for all seven PANELS names, assert '[data-panel=\"<name>\"][data-rendered]' has count 1 before the panel-error check; update the docstring at lines 1-3 if manual stays mount-only. Do not try to get manual content from a fixture: neither sample nor library produces a missing-entry or unclear card for it.",
   "acceptance_test": "On a git archive of the fixed commit with E2E_REQUIRE_DB=1: (1) M8 turns test_no_console_errors.py red at the new data-rendered assertion; (2) M5, M6 and M7 stay red; (3) unmodified HEAD stays 4/4 green, and test_rerun_note.py stays 3/3."
  }
 ],
 "whats_right": [
  "Round-2 dead-panel gap is closed for throws: M6 (batch.js:97), M7 (manual.js:65) and M5 (review.js:497) each turn the smoke red; M5 names 'batch' at test_no_console_errors.py:66.",
  "All seven panels mount at HEAD on both fixtures and six draw content (batch Accept-all bar, audit 87, charges 1595/2490, export-settings 335, flags 5135/4040, narrative 266); 7/7 e2e green (4/4 smoke, 3/3 rerun_note).",
  "The r2 minors are fixed: to_have_count(1) precedes both to_be_hidden checks (test_rerun_note.py:75 and :84), timeline.js:77 calls rerunMarker unguarded, and test_every_registered_panel_is_listed greps the seven registrations."
 ],
 "questions_for_chris": [
  "Should a decided entry's note also appear in its 'Why this status' dialog? The AC says 'row and trace'; entries have no trace button at HEAD, and the spec asserts the row only for entries. Carried from r2; still open in the card handoff."
 ]
}
```
