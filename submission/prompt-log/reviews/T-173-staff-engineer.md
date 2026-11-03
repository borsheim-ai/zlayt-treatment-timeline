# T-173 review: lib01 tray specs seeded through the store (commit d865d21), round 1

Reviewer: staff-engineer-reviewer, model claude-haiku-5-5.

## Summary

The three specs pass on a `git archive d865d21` copy with `E2E_REQUIRE_DB=1` (3 passed). No assertion line changed. Each of eight mutations (the seed removed, six tray UI mutations, one backend tray filter) turns at least one of the three specs red, so the specs do watch the tray.

The seeding is not yet honest about what it reproduces. `tray_entry_for_record()` writes only `state` and `state_reasons_json`. The row keeps record 3's real T-168 summary and quote, its generator and judge ladder, and no failure marker. The browser then shows "The demo has no recorded AI answer for this step" next to "The model's attempt (not used): ...". A real missing answer never shows that second line. The docstring says the row is what a missing extract answer leaves; that is true for state and reason only. This is a major.

Verdict: changes (one major, one minor, one nit, no blocker).

## What I exercised

- `python3 tools/board.py show T-173`; `personas/staff-engineer.md` read in full.
- `git show d865d21` for the three test files (full diff); `git show d865d21 -- tests | grep -E '^[-+].*assert'` returned no lines, so no assertion changed.
- `git archive d865d21` extracted to `artifacts/review-evidence/T-173-r1-staff/copy`. Own private server on 127.0.0.1:55367 (`LLM_BACKEND=fixture`, `FIXTURE_SET=curated`, `ZLAYT_MODE=local`). Specs run with `E2E_BASE_URL`, `ZLAYT_DB` pointed at that server's file, and `E2E_REQUIRE_DB=1`: 3 passed (`artifacts/review-evidence/T-173-r1-staff/run-3specs-head.txt`).
- Mutation driver `artifacts/review-evidence/T-173-r1-staff/driver.py`; per-run output and `mutants/summary.json` in `mutants/`. Frontend mutants were checked as served by the server, then restored (`restore_check ok`).
- Fidelity probes against a diagnostic copy of HEAD (same code, plus tracebacks printed at `api.py:162` and `api.py:184`): `fidelity_probe.py` (stored row and API tray item) and `tray_ui_probe.py` (rendered tray in Chromium).
- `race_probe.py` (create, delete and list cases, 3 rounds), `m0_race_control.py` (seed removed, 3 rounds, unhandled-line count), and `cite_check.py` / `cite_lines.py` (every cited line read at d865d21).
- Own server PIDs stopped; port 55367 free afterwards.

Mutation results (spec outcomes in order: reason-once, entry-wording, no-sentences):

- M0 seed removed: FAIL, FAIL, FAIL.
- M1 tray reason element removed (`timeline.js:227`): FAIL, FAIL, PASS (test 3 does not use it).
- M2 tray items not appended (`timeline.js` `box.append(item)`): FAIL, FAIL, FAIL.
- M3 reason rendered twice: FAIL, PASS, PASS.
- M4 `data-tray-kind` set to flag: PASS, FAIL, PASS.
- M5 raw reason codes instead of sentence: FAIL, PASS, PASS.
- M6 manual-form reason replaced (`manual.js:55`): PASS, PASS, FAIL.
- M7 backend tray filter drops rejected (`present.py:397`): FAIL, FAIL, FAIL.

## Findings

See the JSON block. Finding 1 (major) is the blocker to the milestone: the seeded row must have the placeholder shape. Finding 2 (minor) is an intermittent server-side 500 on the case list that the spec flow reaches; it is outside this diff and does not fail the specs. Finding 3 (nit) is helper hygiene.

```json
{"card": "T-173", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit d865d21: tests/e2e/conftest.py, tests/e2e/test_polish_r5.py, tests/e2e/test_suggestions.py; git archive copy at artifacts/review-evidence/T-173-r1-staff/copy; private server 127.0.0.1:55367 (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local); diagnostic copy of HEAD with traceback printing in artifacts/review-evidence/T-173-r1-staff/diag; sample case: library lib01 (case_lib01_er_only_then_gap), record 3",
 "exercised": [
  "python3 tools/board.py show T-173 (AC, handoff and notes read); personas/staff-engineer.md read in full",
  "git show d865d21 full diff of tests/e2e/conftest.py, tests/e2e/test_polish_r5.py, tests/e2e/test_suggestions.py; grep of changed assert lines returned none",
  "git archive d865d21 extracted to artifacts/review-evidence/T-173-r1-staff/copy; .venv/bin/python -m pytest -v on the three named specs with E2E_BASE_URL, ZLAYT_DB and E2E_REQUIRE_DB=1: 3 passed (run-3specs-head.txt)",
  "driver.py: unmutated control plus M0 to M7 mutants, each restored after its run; outputs and summary.json in artifacts/review-evidence/T-173-r1-staff/mutants/",
  "fidelity_probe.py against the diagnostic copy: seeded tray item JSON (attempt present, ladder.failure None, summary and excerpt set)",
  "tray_ui_probe.py: Chromium render of the seeded lib01 tray: tray-attempt count 1 with text 'The model's attempt (not used): ...' beside 'The demo has no recorded AI answer for this step, so this item has not been checked.'",
  "race_probe.py: create, delete and list cases, 3 rounds: 0 list responses of 500",
  "m0_race_control.py: seed removed, 3 spec rounds on the diagnostic copy: 0 new unhandled lines per round (weak control: those rounds fail early on the tray wait)",
  "diagnostic server log (diag/server-diag.log): unhandled lines per round of the seeded specs 0, 2, 3; first traceback read through case_list.py, trace.py, present.py and overlap.py",
  "cite_check.py and cite_lines.py: every cited line number read at d865d21 with git show",
  "own server PIDs stopped (62857, 62859, 65848, 65849, 66269, 66531, 66533; the driver stopped its own servers); lsof shows nothing on 55367; no process left under artifacts/review-evidence/T-173-r1-staff"
 ],
 "verdict": "changes",
 "scores": {"assertions_unchanged": 5, "mutation_sensitivity": 5, "seed_fidelity_to_missing_answer": 2, "disclosure_in_docstring_and_card": 4, "spec_reproducibility": 4},
 "findings": [
  {"severity": "major",
   "title": "The seeded tray row is not the placeholder a missing answer leaves; the tray shows a contradictory attempt line",
   "evidence": "tests/e2e/conftest.py:208 (DB.update_item writes only state and state_reasons_json). Repro: fidelity_probe.py against the diagnostic copy prints the after-seed tray item with reasons ['FIXTURE_MISS'] and attempt.summary 'Neck pain 5/10 with new left arm tingling; ...', then 'ladder.failure = None | summary set = True | excerpt set = True'. The real placeholder sets summary=None and excerpt=None at app/backend/generator.py:189 and the ladder failure marker at app/backend/generator.py:190. tray_ui_probe.py prints 'tray-attempt count: 1' and the attempt line beside 'The demo has no recorded AI answer for this step, so this item has not been checked.' Builder: app/backend/present.py:396; renderer: app/frontend/timeline.js:230.",
   "why_it_matters": "Per the card title, record 3 was a pipeline-made tray item before T-168, so these specs used to cover the placeholder the pipeline writes. They now cover a hybrid row: the record's real T-168 summary and quote, a generator and judge ladder, no failure marker, and an on-screen line that says the model made an attempt on a record whose reason says no answer was recorded. The helper docstring (tests/e2e/conftest.py:197-199) and the commit message say the row is the state a missing extract answer leaves; that holds for state and reason only. Read from code and not executed: resolved_placeholders (app/backend/generator.py:198-202) keys on ladder.failure, so a hand-entered entry for record 3 would leave this seeded row in the tray, which a real placeholder does not do.",
   "fix": "In tray_entry_for_record, write the placeholder shape: entry summary, excerpt, excerpt_start and excerpt_end set to None, and ladder set to item_id, generator None, judge None, failure FIXTURE_MISS, code_checks {}, state rejected, human {action None, edited_text None, at None}; keep state_reasons_json FIXTURE_MISS. Alternatively call generator.failure_entry(record, group, 'FIXTURE_MISS') and write its fields with DB.update_item. Narrow the docstring to what is reproduced. Re-run the three specs and mutants M0 to M7.",
   "acceptance_test": "After tray_entry_for_record runs, GET /api/cases/<token> returns the entry tray item with attempt.summary and attempt.excerpt both null and ladder.failure equal to FIXTURE_MISS; in the browser item.get_by_test_id('tray-attempt').count() is 0. The three specs pass on a git archive of the fixed commit with E2E_REQUIRE_DB=1, and each of M0 to M7 still turns at least one spec red."},
  {"severity": "minor",
   "title": "Intermittent unhandled 500 on GET /api/cases during the spec flow (outside this diff; the specs still pass)",
   "evidence": "artifacts/review-evidence/T-173-r1-staff/diag/server-diag.log: unhandled lines per round of the three seeded specs were 0, 2, 3. First traceback: api.py:224 list_cases, then case_list.py:204 summaries, case_list.py:186 summary, case_list.py:125 _gate, trace.py:1111 case_trace, present.py:291 totals_view, overlap.py:129 (raw_text read from a case that is None). The handler logs only the exception type name (api.py:162 and api.py:184). Control: artifacts/review-evidence/T-173-r1-staff/m0_race_control.out shows 0 new lines in each of 3 no-seed rounds; race_probe.py, 3 rounds of create, delete and list, shows 0 list responses of 500.",
   "why_it_matters": "The three specs passed every round, so T-173's verdict does not turn on this. It is still a product defect that the spec flow reaches: a case removed between the id SELECT (case_list.py:204) and its read makes the whole case list return 500. The handler is built to log no traceback (api.py:162 comment), so the cause is invisible unless someone runs a diagnostic copy. I did not establish that the seed causes it: the traceback never reads entries, and the no-seed control is weak because those rounds fail early.",
   "fix": "File a backend card. summaries should tolerate a case removed mid-list: skip it, or read the id list and each case inside one transaction. The handler should log the exception class and the innermost app frame (file and line), never message text, which keeps the privacy rule api.py states.",
   "acceptance_test": "A unit test patches the case read to return None for one listed id and asserts GET /api/cases returns 200 without that case. A log test asserts the innermost app frame is named and no record text appears in the log line."},
  {"severity": "nit",
   "title": "Helper hygiene: unguarded next() and a sys.path insert on every call",
   "evidence": "tests/e2e/conftest.py:203 e = next(x for x in c['entries'] ...) has no default, so a missing record 3 entry raises a bare StopIteration. tests/e2e/conftest.py:204 sys.path.insert(0, ROOT) runs on every call, and the imports sit inside the function.",
   "why_it_matters": "A missing entry fails with no message naming the record. The per-call sys.path insert is harmless here but repeats on every call.",
   "fix": "Use next(..., None) and pytest.fail naming the record id; move the sys.path setup to module level, where ROOT is already defined.",
   "acceptance_test": "Calling tray_entry_for_record for a record id with no entry fails with a message that names the id."}
 ],
 "whats_right": [
  "Assertions are unchanged: the diff only adds a helper call and docstrings, and grep of changed assert lines at d865d21 returns nothing.",
  "The three specs fail when the tray breaks: 8 of 8 mutations (seed removed, six tray UI mutations, one backend tray filter) each turned at least one spec red.",
  "The helper writes through the store's case-scoped update_item and the tray is read from the real backend view and DOM, with the injection disclosed in the docstrings and the card."
 ],
 "questions_for_chris": [
  "Would you accept a fixture set in which record 3 has no recorded answer, so the real pipeline writes the placeholder and the DB write in tray_entry_for_record goes away? That is a fixture or backend card, not a test-only change, so I am asking, not conditioning T-173 on it."
 ]}
```
