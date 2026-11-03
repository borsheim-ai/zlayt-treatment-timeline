# T-173 review: lib01 tray specs seeded with the pipeline's own placeholder, round 2

Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit under review: f814cf7 (tests/e2e/conftest.py only). Evidence was run on `git archive 489f1bc` (HEAD at review time, which contains f814cf7 and later commits that do not touch the helper or the three specs).

## Summary

The round-1 major is fixed at the data level. `tray_entry_for_record` now writes record 3's row through `generator.failure_entry` and `pipeline._row`. The 14 stored columns of the seeded row are identical to the row the real pipeline stores when record 3's extract answer is withheld (`fidelity_r2.json`: `diff_real_vs_seeded: {}`). The three specs pass with `E2E_REQUIRE_DB=1` on my own port, and their assertions are unchanged.

One gap remains and it is a major. The round-1 acceptance test also required the browser to show no attempt line for the seeded item (`item.get_by_test_id('tray-attempt').count() is 0`). That is true today (`tray_ui_r2.json`: `tray_attempt_count: 0`). No test enforces it. The helper checks only the API. With a one-line UI mutant that re-introduces the attempt line for an empty attempt, the browser shows "The model's attempt (not used): — “”" beside the placeholder reason, and all three specs still pass (`mutants/M6_attempt_line_for_empty_attempt.txt`, `mutants/M6_dom.json`).

Verdict: changes (one major, one nit, no blocker).

## What I exercised

- Read `personas/staff-engineer.md` in full, `reviews/T-173-staff-engineer.md` (round 1), and my T-173 memory note. Ran `python3 tools/board.py show T-173`.
- `git show f814cf7 -- tests/e2e/conftest.py` (full round-2 diff). `git merge-base --is-ancestor f814cf7 HEAD` returned true. `git diff d865d21 HEAD -- tests/e2e/test_polish_r5.py tests/e2e/test_suggestions.py` returned empty, so the spec files are unchanged from round 1 to HEAD. `git diff f814cf7 HEAD -- tests/e2e/conftest.py` changed one docstring line only, so the helper is unchanged since f814cf7. `git grep -n "tray-attempt" 489f1bc -- tests` showed no spec assertion on the tray item's attempt line.
- `git archive 489f1bc` extracted to `artifacts/review-evidence/T-173-r2-staff/copy-head`. A `git archive f814cf7` copy was made to `copy-f814cf7` but not run.
- Own server on 127.0.0.1:62617 from copy-head (`LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, `ZLAYT_DB=artifacts/review-evidence/T-173-r2-staff/e2e-head.sqlite3`). `.venv/bin/python -m pytest -p no:cacheprovider -v -rfE` on the three specs with `E2E_BASE_URL`, `ZLAYT_DB` and `E2E_REQUIRE_DB=1`: 3 passed (`run-3specs-head.txt`).
- `fidelity_r2.py`. Part A runs the real pipeline on lib01 in a scratch DB with the extract step for record 3 raising FixtureMiss, and reads the stored entries row. Part B calls `tests/e2e/conftest.tray_entry_for_record` (loaded from copy-head) against my server and reads the stored row and the API tray item. The 14 raw columns are compared with no differences. Output: `fidelity_r2.json`, `fidelity_r2.out`.
- `tray_ui_r2.py`: Chromium render of the seeded lib01 tray on my server. Result: 1 tray item, 0 `tray-attempt` elements, reason "The demo has no recorded AI answer for this step, so this item has not been checked." (`tray_ui_r2.json`, `tray_ui_r2.png`).
- `driver_r2.py` on `copy-mut` (a copy of copy-head). Each mutant ran against a fresh private server on a new loopback port, which the driver stopped afterward. Control: 3 passed. Results (specs red out of 3): M0 seed removed 3; M1 tray reason element removed 2; M2 tray items not appended 3; M3 reason doubled 1; M4 wrong data-tray-kind 1; M5 raw codes instead of sentence 1; M6 attempt line for empty attempt 0; M7 backend tray drops rejected 2 failed plus 1 error; M8 helper writes state only 2 failed plus 1 error; M9 manual reason replaced 1. `restore_check ok`. Output: `mutants/summary_r2.json`, `mutants/driver_r2.out`, per-run `mutants/*.txt`.
- `m6_dom.py`: applied M6 to `copy-mut/app/frontend/timeline.js:230`, rendered the seeded tray in Chromium. `tray_attempt_count: 1`, item text includes "The model's attempt (not used): — “”". Restored the file; `diff` against `git show 489f1bc:app/frontend/timeline.js` is empty.
- Not run, out of this round's scope: `pytest tests/unit`, the eval command, and the T-175 500 race (fixed by commit 4a097b6 at HEAD; not re-tested here).
- Stopped my server PID 20836 (SIGTERM). The driver's 11 server PIDs (`mutants/server_pids_started.json`) are gone. Port 62617 is free. Other listeners on the machine belong to other processes and were not touched.

## Findings

1. **Major, browser no-attempt rule unguarded.** The seeded row is correct. The API view is guarded by `conftest.py:226`. The browser rule from round 1 (`tray-attempt` count 0) has no test. Mutant M6 at `app/frontend/timeline.js:230` (`t.attempt && (t.attempt.summary || t.attempt.excerpt) ? el(` becomes `t.attempt ? el(`) keeps all three specs green, and the rendered DOM shows the attempt line for the placeholder (`mutants/M6_dom.json`). The specs assert neither `tray-attempt` absence nor its text (`test_polish_r5.py:176-182`, `test_suggestions.py:245-251`). Fix: add one new spec file (qa-owned, for example `tests/e2e/test_tray_seed_placeholder.py`). It seeds lib01 record 3 with `tray_entry_for_record`, opens the case, and asserts `tray-item` has `tray-attempt` count 0 and `tray-reason` count 1. Do not change the three existing specs. Acceptance: the new spec is green at HEAD on a `git archive` copy with `E2E_REQUIRE_DB=1`, and red when M6 is applied.

2. **Nit, backend stamp copied from the old row.** `tests/e2e/conftest.py:221` sets `f["ladder"]["backend"]` from the existing row. The pipeline stamps `P.backend_name()` on every item it stores (`app/backend/pipeline.py:570`). In this run both values were `fixture` (raw rows identical), so there is no visible effect. Fix: use `P.backend_name()` and import `provider` as `P` in the helper. Acceptance: after seeding, the stored `ladder_json.backend` equals `P.backend_name()` on a backend other than the default.

Round-1 items checked: the `next()` guard (conftest.py:208-211) and the module-level `sys.path` (conftest.py:106-108) are fixed. The round-1 minor (intermittent 500 on `GET /api/cases`) is outside this diff and is not re-opened here.

## Mutation results for the record

The helper guard is live: writing the round-1 state-only row (M8) turns the three specs red, so a future regression to the thin seed would be caught by the helper's own assert. Specs red for M0 to M7 and M9 are listed above; M6 is the only survivor.

```json
{"card": "T-173", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f814cf7 (tests/e2e/conftest.py, tree at HEAD 489f1bc): git archive copy at artifacts/review-evidence/T-173-r2-staff/copy-head; private server 127.0.0.1:62617 (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local); mutant copy copy-mut; sample case: library lib01 (case_lib01_er_only_then_gap), record 3",
 "exercised": [
  "python3 tools/board.py show T-173; personas/staff-engineer.md read in full; reviews/T-173-staff-engineer.md read (round 1)",
  "git show f814cf7 -- tests/e2e/conftest.py; git merge-base --is-ancestor f814cf7 HEAD (true); git diff d865d21 HEAD -- the two spec files (empty); git diff f814cf7 HEAD -- tests/e2e/conftest.py (docstring line only); git grep tray-attempt at 489f1bc (no spec asserts the attempt line)",
  "git archive 489f1bc extracted to artifacts/review-evidence/T-173-r2-staff/copy-head; git archive f814cf7 extracted to copy-f814cf7 (archived, not run)",
  ".venv/bin/python -m pytest -p no:cacheprovider -v -rfE on the three specs, E2E_BASE_URL on 127.0.0.1:62617, ZLAYT_DB=e2e-head.sqlite3, E2E_REQUIRE_DB=1: 3 passed (run-3specs-head.txt)",
  "fidelity_r2.py: real pipeline run on lib01 with record 3 extract forced to FixtureMiss (scratch DB) vs tests/e2e/conftest.tray_entry_for_record on the own server: 14 raw entries columns compared, zero differences (fidelity_r2.json, fidelity_r2.out)",
  "tray_ui_r2.py: Chromium render of the seeded lib01 tray: tray-item 1, tray-attempt 0, reason sentence shown (tray_ui_r2.json, tray_ui_r2.png)",
  "driver_r2.py on copy-mut: control 3 passed; M0 3 red; M1 2 red; M2 3 red; M3 1 red; M4 1 red; M5 1 red; M6 0 red; M7 2 failed + 1 error; M8 2 failed + 1 error; M9 1 red; restore_check ok (mutants/summary_r2.json, mutants/driver_r2.out, per-run .txt)",
  "m6_dom.py: M6 applied to copy-mut timeline.js:230, rendered: tray-attempt count 1, text 'The model's attempt (not used): — “”' (mutants/M6_dom.json); file restored, diff vs git show 489f1bc:app/frontend/timeline.js empty",
  "own server PID 20836 stopped; driver server PIDs (mutants/server_pids_started.json) confirmed gone; port 62617 free"
 ],
 "verdict": "changes",
 "scores": {"seed_fidelity_to_pipeline_placeholder": 5, "assertions_unchanged": 5, "helper_guard_live": 5, "tray_ui_mutation_sensitivity": 4, "browser_no_attempt_guard": 2, "spec_reproducibility": 5},
 "findings": [
  {"severity": "major",
   "title": "The browser no-attempt rule for the seeded placeholder is not tested; the attempt line can return and the three specs stay green",
   "evidence": "app/frontend/timeline.js:230 (t.attempt && (t.attempt.summary || t.attempt.excerpt) ? el(...)); mutant M6 sets it to t.attempt ? el( on copy-mut: mutants/M6_attempt_line_for_empty_attempt.txt shows 3 passed, rc 0; mutants/M6_dom.json shows tray_attempt_count 1 and item_text containing \"The model's attempt (not used): — “”\". Unmutated: tray_ui_r2.json shows tray_attempt_count 0. The helper checks the API only: tests/e2e/conftest.py:226 assert t and t[\"kind\"] == \"entry\" and t[\"reasons\"] == [\"FIXTURE_MISS\"] and t[\"attempt\"] == {\"summary\": None, \"excerpt\": None}. No spec asserts tray-attempt absence (tests/e2e/test_polish_r5.py:176-182; tests/e2e/test_suggestions.py:245-251).",
   "why_it_matters": "Round 1 named the contradictory attempt line as the symptom and its acceptance test required the browser check (tray-attempt count 0). The seed is now right, but nothing stops the rendered tray from showing a model attempt beside 'The demo has no recorded AI answer', which is the contradiction round 1 flagged. The regression would reach the spec suite unseen because the M0 to M9 set has no mutant for this render rule before this review.",
   "fix": "Add one new spec in a new qa-owned file (for example tests/e2e/test_tray_seed_placeholder.py). It seeds lib01 record 3 with tray_entry_for_record, opens the case, and asserts that the first rejected-tray tray-item has get_by_test_id('tray-attempt') count 0 and get_by_test_id('tray-reason') count 1. Do not edit the three existing specs (their assertions must stay unchanged).",
   "acceptance_test": "On a git archive of the fixed commit with E2E_REQUIRE_DB=1 and a private server, the new spec passes. With timeline.js:230 mutated to 't.attempt ? el(' (the M6 text in driver_r2.py), the new spec fails. The three existing specs still pass on the unmutated tree."},
  {"severity": "nit",
   "title": "Helper copies the backend stamp from the old row instead of the pipeline's backend_name()",
   "evidence": "tests/e2e/conftest.py:221 f[\"ladder\"][\"backend\"] = (old.get(\"ladder\") or {}).get(\"backend\"); the pipeline stamps P.backend_name() on every stored item at app/backend/pipeline.py:570. Raw rows in fidelity_r2.json compare equal (backend \"fixture\" on both sides).",
   "why_it_matters": "No effect in this run, because the case was run on the same backend that seeded it. The helper would silently store a null backend if the old row had none, which is not what the pipeline writes.",
   "fix": "Import provider as P in the helper and set f[\"ladder\"][\"backend\"] = P.backend_name().",
   "acceptance_test": "After tray_entry_for_record, the stored ladder_json.backend equals app.llm.provider.backend_name() in the same process."}
 ],
 "whats_right": [
  "The seeded row is the pipeline's own placeholder: the 14 raw entries columns for record 3 match the row the real pipeline stores for a withheld extract answer (zero differences in fidelity_r2.json).",
  "The helper guard is live: restoring the round-1 state-only write (M8) turns the three specs red, so a regression to the thin seed is caught.",
  "Assertions are unchanged: the three spec files are identical from d865d21 to HEAD, and all three pass with E2E_REQUIRE_DB=1 on a git archive copy at my own port."
 ],
 "questions_for_chris": []}
```
