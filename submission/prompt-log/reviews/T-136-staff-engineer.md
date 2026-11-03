# T-136 staff-engineer review (frontend, 671f054)

Verdict: changes (0 blockers, 1 major, 2 minors).

Setup. I ran everything on `git archive 671f054` copies under my own scratch dir, on my own ports (7947 head, 7948-7951 mutants), with `LLM_BACKEND=fixture FIXTURE_SET=curated`. I stopped only those PIDs (89626, 72855, 72858, 72861, 72864; each checked with ps and lsof, ports confirmed closed). HEAD moved to 0c24f5f during the review, but the only app change after 671f054 is `app/backend/trace.py` (T-134 r2). No frontend or e2e file changed, so the verdict holds for HEAD.

Deterministic results.
- `tests/e2e/test_edit_to_check.py` with ZLAYT_DB set: `10 passed in 17.57s`.
- Full `tests/e2e` with ZLAYT_DB set and `ZLAYT_MODE=local`: `231 passed, 1 skipped in 317.04s`. My first run without local mode failed 6 library-case tests with `demo_mode_unsupported_input`. That was my server config, not the card.
- `tests/unit`: `3444 passed, 8 skipped in 193.63s`. The card says 3321; the count differs, but nothing failed.

Mutation checks (each on its own archive copy and server, new tests plus `test_polish_r5.py`).
- A, delete the `a` handler line (`review.js:423`) so `a` records the compare: caught. 3 of the new tests fail, and so does `test_polish_r5::test_nothing_left_message_does_not_come_while_an_edit_is_open`.
- B1, flags not grouped under Dismissed (`flags.js`): caught by `test_dismissed_flags_and_amounts_wait_under_dismissed_n`.
- B2, amounts not grouped under Dismissed (`charges.js`): caught by the same test.
- C, `ZL.editCount` ignores `review.counts.edit_to_check` (`dom.js:51`): survives, 10 of 10 pass (finding 2).
- D, a second `a` press records the compare: survives, 24 passed (finding 3).

Backend counts versus recomputation. In the code, `ZL.progressOf`, `export.js` and `timeline.js` all read `ZL.editCount`, which returns `review.counts.edit_to_check` and recounts items only when that field is absent (the mock API). The stepper reads the review step's `counts.edit_to_check` from the trace. I stubbed `review.counts.edit_to_check = 3` on a fresh sample case. The header then read "0 of 23 decided · 3 items need review, including 3 edits to check" and the strip read "3 edits to check". So the UI follows the backend value. No test proves it (finding 2).

ZLAYT_DB skip. The skip does hide the new tests in the default run. Nothing in the repo sets ZLAYT_DB for pytest. There is no Makefile, run.sh or CI. `docs/RUNBOOK.md` and `README.md` do not mention the e2e command or the variable. `tools/serve_app.sh:6` sets ZLAYT_DB only for the server process. With `env -u ZLAYT_DB`: `1 passed, 9 skipped`.

```json
{"card": "T-136", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 671f054 (app/frontend/{app,charges,dom,export,flags,mock,review,stepper,timeline}.js, tests/e2e/{conftest,test_edit_to_check,test_polish_r5}.py), git archive copies on ports 7947-7951, fixture backend FIXTURE_SET=curated; sample case; contract memory/contracts/api.md edit_to_check section",
 "exercised": [
  "python3 tools/board.py show T-136; read memory/contracts/api.md edit_to_check section (lines 353-361)",
  "git show 671f054 (full diff of app/ and tests/e2e); read tests/e2e/test_edit_to_check.py in full",
  "git archive 671f054 copy, own server on :7947 with ZLAYT_DB set: pytest tests/e2e/test_edit_to_check.py -> 10 passed in 17.57s",
  "full pytest tests/e2e on :7947 (ZLAYT_MODE=local, ZLAYT_DB set) -> 231 passed, 1 skipped in 317.04s (first run without local mode: 6 library-case tests failed demo_mode_unsupported_input, an environment error on my side)",
  "pytest tests/unit on the archive -> 3444 passed, 8 skipped in 193.63s",
  "mutant A (delete the a handler line review.js:423) on :7948: 4 failed (3 in test_edit_to_check, 1 in test_polish_r5)",
  "mutant B1 (flags not grouped under Dismissed) on :7949 and B2 (amounts not grouped) on :7950: each 1 failed (test_dismissed_flags_and_amounts_wait_under_dismissed_n)",
  "mutant C (ZL.editCount ignores review.counts.edit_to_check) on :7951: 10 passed (survives)",
  "mutant D (second a press records the compare) on :7948: test_edit_to_check + test_polish_r5 -> 24 passed, 1 skipped (survives)",
  "probe: Playwright route stub sets review.counts.edit_to_check=3 on a fresh sample case -> header 'including 3 edits to check', strip '3 edits to check'",
  "env -u ZLAYT_DB run of test_edit_to_check.py -> 1 passed, 9 skipped; same plus test_polish_r5 against mutant A -> test_nothing_left_message... still failed (caught without ZLAYT_DB)",
  "grep for ZLAYT_DB/e2e command in docs/RUNBOOK.md, README.md, memory/ENVIRONMENT.md, tools/, deploy/ (no Makefile, run.sh or CI exists); read tools/serve_app.sh",
  "git log 671f054..HEAD and git diff --stat 671f054 HEAD -- app tests/e2e (only app/backend/trace.py changed); grep of batch.js eligible() path (accept-verified batch cannot include a Needs review edit)"],
 "verdict": "changes",
 "scores": {"correctness_vs_contract": 4, "regression_strength_of_tests": 3, "determinism_and_reproducibility": 3, "uses_backend_counts": 4, "honest_failure": 4},
 "findings": [
  {"severity": "major",
   "title": "The tests for the card's main AC skip silently in the default e2e run; nothing sets ZLAYT_DB for pytest",
   "evidence": "tests/e2e/test_edit_to_check.py:28 `pytest.skip(\"needs ZLAYT_DB ...\")`. Repro: `cd <archive> && env -u ZLAYT_DB E2E_BASE_URL=http://127.0.0.1:<port> python -m pytest tests/e2e/test_edit_to_check.py -q -rs` -> `1 passed, 9 skipped` (9 SKIPPED lines at lines 78, 88, 99, 112, 130, 137, 153, 169, 179). tools/serve_app.sh:6 sets ZLAYT_DB only for the server process, not for pytest. `grep -n -i 'e2e\\|ZLAYT_DB' docs/RUNBOOK.md README.md memory/ENVIRONMENT.md` returns nothing, and there is no Makefile, run.sh or CI. Mutant A (a records the compare) still fails `test_polish_r5::test_nothing_left_message_does_not_come_while_an_edit_is_open` with ZLAYT_DB unset, so that one `a` regression is covered by default. The quote-only edit path that AC 1 is about (open row, 'I compared it with the quote', header and strip counts, EDIT_NOT_CONFIRMED gate warning, copy-confirm, Start review then a) has no default-run coverage.",
   "why_it_matters": "AC 1 says an excerpt-only edit shows as open with the compare control, with an e2e test. A plain `pytest tests/e2e` reports green while 9 of the 10 new tests did not run, and only `-rs` shows it. A regression in the quote-only path would then reach the gate with a green suite. The same skip pattern is already in test_code_check_refusal.py and test_change_the_quote.py, so the gap is larger than this card.",
   "fix": "Make the fixture find the server's DB itself (for example expose the file path in the test-mode /api/health, or default to the path tools/serve_app.sh uses and fail with a clear error if it is missing). Or add one documented e2e command that exports ZLAYT_DB (RUNBOOK or a script), and make the skip a failure when `E2E_REQUIRE_DB=1` is set so a run can say 0 skipped.",
   "acceptance_test": "The documented e2e command run on a fresh archive prints `10 passed` with 0 skipped for tests/e2e/test_edit_to_check.py; the same file with ZLAYT_DB unset and E2E_REQUIRE_DB=1 fails instead of skipping."},
  {"severity": "minor",
   "title": "test_header_and_strip_use_the_servers_edit_count does not prove the UI uses the server's count",
   "evidence": "tests/e2e/test_edit_to_check.py:88-96 compares the header to `_case(tok)['review']['counts']['edit_to_check']`, which is 1, the same number a recount of the item flags gives. Mutant C (app/frontend/dom.js:51 `return n != null ? n :` -> `return false ? n :`) leaves all 10 tests green. A route stub that sets review.counts.edit_to_check=3 makes the header read 'including 3 edits to check', so the shipped code does follow the server; the test does not prove it.",
   "why_it_matters": "The contract (api.md edit section) makes `review.counts.edit_to_check` the one count. Replacing it with a local recount, the thing T-136 removed, would pass. The test name overstates what it checks.",
   "fix": "Add a case that stubs GET /api/cases/{tok} so review.counts.edit_to_check differs from what the items show, and assert the header and strip follow the stub. Or rename the test to what it checks.",
   "acceptance_test": "With dom.js:51 changed to ignore review.counts, at least one test in tests/e2e/test_edit_to_check.py fails."},
  {"severity": "minor",
   "title": "The 'a never records the comparison' rule is proved for one key press only",
   "evidence": "tests/e2e/test_edit_to_check.py:153-164 and :169-174 press `a` once. Mutant D, `if (key === \"a\" && ZL.editToCheck(f.item)) { if (comparePrompt.has(id)) { RV.act(id, {action:\"accept\"}, {advance:true}); return; } askCompare(id); return; }` at app/frontend/review.js:423, gives `24 passed, 1 skipped` across test_edit_to_check.py and test_polish_r5.py.",
   "why_it_matters": "The handoff and code comment say `a` never records the compare (review.js:421-423). A second press, or key auto-repeat on a held key, would record a statement the paralegal has not made. The cheap implementation of 'ask first, then do it' passes every test.",
   "fix": "In test_one_a_press_does_not_record_the_comparison (or a sibling), press `a` twice, then assert data-review is still 'edited', the API's edit_to_check is still true, and the header count is unchanged.",
   "acceptance_test": "Mutant D fails at least one test in tests/e2e/test_edit_to_check.py."}
 ],
 "whats_right": [
  "ZL.editToCheck now reads the server's own item.edit_to_check (dom.js:49) and the count comes from review.counts.edit_to_check (dom.js:51); the UI follows a stubbed backend count.",
  "Mutants A (a records the compare) and B1/B2 (Dismissed grouping for flags and amounts) are each killed by the new tests; the a-key rule is also covered in the default run via test_polish_r5.",
  "Full e2e 231 passed/1 skipped and unit 3444 passed on a git-archive copy of the card commit; the batch Accept-verified path cannot include a Needs review edit."],
 "questions_for_chris": []}
```
