# GATE-M3 staff-engineer review

Reviewer: staff-engineer-reviewer (Marcus Lee). Model claude-sonnet-5-5. Commit under review: d0b04bc (T-045 commits 4510dc2, d0b04bc). Verdict: **changes** (0 blockers, 3 majors).

## Result
Verdict **changes**: 0 blockers, 3 majors, 1 minor, 3 nits. No red-flag item (silent fallback, LLM deciding export or totals, float money, real-API tests, secrets) was found in the files I read. T-045's specs and the M3 UI-backend contract are mostly sound; three pieces of evidence are not.

## T-045 specs (card review in reviews/T-045-staff-engineer.md)
Both suites reproduce at d0b04bc (e2e 411/2 skipped, unit 5689/2 skipped, secrets scan ok). Mutation results: 16 effective mutants, 13 killed, 3 survived. Majors: the 375 px sideways-scroll assertion cannot fail under is_mobile (F1); no test runs the rejected-item accept/edit guard and m3-sensors.md says one does (F2); latest.json is a stale fixture pointer (F3).

## --check-fresh severity
Major. The dated live report is valid (hashes at :143 and :151 equal the d0b04bc files; no prompt or lexicon commit since 312efe6), but check-fresh exits 1 and tools/board.py:421 reads ship_bar_met False from the pointer, so the Definition-of-Done check fails, and every fixture eval re-breaks it. One commit plus a fixture-vs-live pointer split fixes it.

## M3 UI-backend contract pass
No behavioural drift found. All 34 backend routes are in the contract; no documented route is missing; all 16 raised error codes are documented; the UI's export count line reads the names the backend serves. Live sample: /health and /status match their examples exactly. Documentation drift only (F4): export counts example names, a removed kept_my_wording field, and a Conventions line that contradicts the case-list endpoint.

## Stale AC text vs current rules
Sound in each case (D-045, D-062, R-EX-4). Nit F5 asks the owner to reword R-CO-2.

```json
{
 "card": "GATE-M3",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "commit d0b04bc (T-045: 4510dc2, d0b04bc; diff 3ddfdc6..d0b04bc); git archive and git clone copies; private fixture server (ZLAYT_MODE=local, FIXTURE_SET=curated) on a free port per run; sample case plus case_01..09 and library cases lib01/lib06; memory/contracts/api.md vs app/backend, app/frontend",
 "exercised": [
  "Read personas/staff-engineer.md, evals/reports/m3-sensors.md, python3 tools/board.py show T-045, the diff 3ddfdc6..d0b04bc (8 files), and the five new spec files in full (test_journey_modes, test_adversarial_ui, test_letter_matrix, test_ladder_gate additions, test_two_cases_side_by_side).",
  "git archive d0b04bc into a scratch dir; E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e -q -rsx on a private server and port (the suite starts its own): 411 passed, 2 skipped in 601.18s; skips tests/e2e/test_ladder_gate.py:37 and tests/e2e/test_multicase.py:775.",
  "git clone checked out at d0b04bc; E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/unit -q: 5689 passed, 2 skipped in 489.68s (clone, so the git-dependent guards run). tools/check_secrets.py in the clone: ok (2328 files).",
  "Mutation spot-checks on archive copies via artifacts/review-evidence/GATE-M3-staff/mutants.py (16 effective mutants run): 13 KILLED: dismissed_exports, pending_exports, flag_line_always_in_letter, flag_note_always_in_letter, flag_note_after_total, count_line_in_letter, gap_days_in_letter, decision_leaks_across_cases, key_d_accepts, accept_button_short_375, size_limit_off (by the API test), rate_in_total_pinned (by test_letter_isolation), sideways_scroll_375_wide (by a tap timeout); 3 SURVIVED: sideways_scroll_375, rate_in_total (new matrix and adversarial_ui alone: letter total became $8,575.00, only the older test_letter_isolation catches it), accept_rejected_allowed (6 files and full unit). Four of my first mutants (flag_title_in_letter, flag_note_in_letter, flag_note_in_letter_v2, flag_title_always_in_letter) were no-ops or artifacts because export flags carry no title or reviewer_note key; I replaced them with flag_line/flag_note mutants and do not count them.",
  "Reran test_journey_modes, test_adversarial_ui, test_letter_matrix, test_two_cases_side_by_side three times under load: 25 passed each time.",
  "python -m evals.run --check-fresh in the archive (exit 1, two hash lines); python3 tools/board.py status --json (evals_ship_bar False); sha256 of lexicon.yaml and judge_conflict_v6.md at d0b04bc against evals/reports/20261102T164038Z.md:143,151 (equal); git log 312efe6..d0b04bc -- app/llm/lexicon.yaml app/llm/prompts (empty). Scripts and probe outputs: artifacts/review-evidence/GATE-M3-staff/.",
  "HEAD moved from d0b04bc to 0c4284f (docs-only, D-065) during the review; every finding is for d0b04bc and none of the files cited changed in that commit.",
  "Contract pass over memory/contracts/api.md: routes_drift.py (34 backend routes vs index), error_codes_drift.py (16 raised codes), shape_drift.py (live sample case on a fixture server: health, status, case, review, export, item views against the examples), grep of frontend fetches (app/frontend/api.js, review.js, switcher.js) and of removed-API remnants (needs_confirm only remains for run, as documented)."
 ],
 "verdict": "changes",
 "scores": {
  "letter_isolation_specs": 5,
  "journey_specs_keyboard_375": 3,
  "ladder_gate_coverage": 2,
  "evidence_integrity": 2,
  "contract_drift": 4
 },
 "findings": [
  {
   "severity": "major",
   "title": "The 375 px 'no sideways scroll' assertion cannot fail under is_mobile emulation",
   "evidence": "tests/e2e/test_journey_modes.py:36-38 (_no_sideways_scroll: scrollWidth <= innerWidth + 1) is called at :136, :140, :152, :155, :162 in a context built at :134 with is_mobile=True. Probe artifacts/review-evidence/GATE-M3-staff/probe_375.py on a d0b04bc archive with 'body, html { min-width: 560px; }' appended to app/frontend/styles.css: is_mobile context {inner: 560, scroll: 560, vv: 375}; a plain 375 px context {inner: 375, scroll: 560}. Mutant sideways_scroll_375 (timeline min-width 560px at <= 420 px): test_whole_journey_on_a_375_px_phone '1 passed in 26.37s' (SURVIVED). Mutant sideways_scroll_375_wide (body/html min-width 560px) failed only on 'Locator.tap: Timeout 30000ms exceeded', not on the scroll assertion.",
   "why_it_matters": "Chromium's mobile emulation widens window.innerWidth to the content width, so the check compares the page with itself and passes for any overflow. A layout that makes a phone pan sideways (visual viewport stays 375) passes the 375 px journey, whose claim 'no sideways scroll' is repeated in the test docstring and in m3-sensors.md (AC3 row: 'no sideways scroll on four screens'). The 44 px tap-size half of the spec is real (mutant accept_button_short_375 was killed at :144).",
   "fix": "Compare scrollWidth with the constant 375 (or window.visualViewport.width) instead of window.innerWidth, or take the overflow measurement in a non-mobile 375 px context; keep is_mobile for tap and touch.",
   "acceptance_test": "With 'body, html { min-width: 560px; }' appended to app/frontend/styles.css, test_whole_journey_on_a_375_px_phone fails with 'sideways scroll on home'; with the shipped CSS it passes."
  },
  {
   "severity": "major",
   "title": "No test runs the rule 'a rejected item cannot be accepted or edited'; the sensors file says a unit test covers it",
   "evidence": "app/backend/review.py:280 raises 409 item_rejected for accept/edit on state 'rejected'. The only test is tests/e2e/test_ladder_gate.py:33-38, which calls pytest.skip at :37; my e2e run printed 'SKIPPED [1] tests/e2e/test_ladder_gate.py:37: no rejected item in the sample fixture run'. evals/reports/m3-sensors.md:8 says 'the 409 is unit-covered', but grep -rn item_rejected tests finds unit hits only in tests/unit/test_reclassify.py:343, which is the reclassify route (reclassify.py:122), a different raise. Mutant accept_rejected_allowed (condition changed to 'if False and ...' at review.py:280): 6 targeted files 336 passed, 1 skipped; whole tests/unit in a git-archive copy (no .git, so 8 skips instead of 2) 5683 passed, exit 0 (SURVIVED).",
   "why_it_matters": "This is the ladder rung 'a rejected (ungrounded or failed) item can only be dismissed or reset' (ADR-005), and the card cites a unit test for it that does not exist, so the evidence for T-045 AC5's gate is wrong. Someone can delete the guard and every sensor stays green.",
   "fix": "Add a unit test: set an item to state 'rejected' with DB.update_item, then apply_review accept and edit each raise ReviewError(409, 'item_rejected') while dismiss and reset succeed. Seed a rejected item through needs_db() in the e2e test so it runs instead of skipping. Correct the m3-sensors.md sentence.",
   "acceptance_test": "With review.py:280 disabled the new unit test fails; under E2E_REQUIRE_DB=1 the ladder-gate e2e test is not skipped."
  },
  {
   "severity": "major",
   "title": "Committed latest.json is a fixture run: ship_bar_met False, --check-fresh exits 1, the Definition-of-Done check reads False",
   "evidence": "evals/reports/latest.json at d0b04bc: backend fixture, ship_bar_met False, generated_at 2026-11-02T14:39:59Z (last changed by 78450f6). 'python -m evals.run --check-fresh' in the d0b04bc archive printed 'check-fresh: app/llm/lexicon.yaml changed since the report' and 'check-fresh: app/llm/prompts/judge_conflict_v6.md changed since the report', exit 1. 'python3 tools/board.py status --json' shows done_checks.evals_ship_bar False; tools/board.py:421 reads ship_bar_met from latest.json. The live evidence itself is sound: evals/reports/20261102T164038Z.md:143 and :151 list judge_conflict_v6 8a09702a5c12... and lexicon.yaml fbefe801fb3d..., which equal the sha256 of those two files at d0b04bc, and 'git log 312efe6..d0b04bc -- app/llm/lexicon.yaml app/llm/prompts' is empty.",
   "why_it_matters": "The dated report is right and the pointer is wrong, but two machine consumers read the pointer: the staleness guard and the Definition-of-Done ship-bar check. Every fixture eval overwrites latest.json by design, so the gate re-run, a 'make eval' or a reviewer's run puts it back to False after any fix. T-045 AC4 and AC6 say the live command yields ship_bar_met true, and the repo cannot show that from its own pointer. Severity: major, not blocker (no code, prompt or number is wrong; one commit fixes it), not minor (the DoD check fails on it and nothing stops it recurring).",
   "fix": "Commit the live run's latest.json (restore it from the 164038Z run, or run the live eval once at the gate commit and commit its latest.json), and make a fixture run write latest.fixture.json or refuse to replace a live latest.json.",
   "acceptance_test": "After a fixture 'python -m evals.run', 'python -m evals.run --check-fresh' still exits 0 and 'board.py status --json' shows evals_ship_bar true; a unit test pins that a fixture run does not replace a live latest.json."
  },
  {
   "severity": "minor",
   "title": "Three examples in memory/contracts/api.md disagree with what the backend serves and the UI reads (documentation drift; backend and UI agree with each other)",
   "evidence": "api.md:528-529 documents export counts.entries_in_letter and counts.charges_in_letter; GET /export serves counts.entries, charges, flags_in_notes, records_in_letter, records_total, pending, pending_flags (app/backend/export.py:886-894) and the UI reads c.entries and c.charges (app/frontend/export.js:9); pending and pending_flags are not documented. api.md:359 still shows edited.kept_my_wording in the review 200 example, but D-047 removed keep-my-wording and grep kept_my_wording app/backend finds nothing. api.md:7 says 'There is no case-list endpoint' while the index at :41 lists GET /api/cases (local mode). Checked with artifacts/review-evidence/GATE-M3-staff/routes_drift.py (all 34 backend routes are in the contract text; no documented route is missing), error_codes_drift.py (16 raised codes, none absent from the contract) and shape_drift.py (live sample case: GET /health and /status match their examples exactly; GET case serves 58 paths the example block lacks, e.g. title, next_action, checks, entries[].edit_to_check, which the prose sections describe).",
   "why_it_matters": "A future client written from the examples would read counts.entries_in_letter (undefined) and expect kept_my_wording. Today nothing reads either, so it is a doc defect, not a behaviour one.",
   "fix": "Update the export counts example, drop kept_my_wording from the review example, and correct the Conventions line to 'case list only in local mode'.",
   "acceptance_test": "A contract test that compares the sample export's counts keys with the example block in api.md passes; grep -n 'kept_my_wording\\|entries_in_letter' memory/contracts/api.md returns nothing."
  },
  {
   "severity": "nit",
   "title": "R-CO-2 and T-045 AC5 still say 'absent from both export blocks'; the spec tests rightly follow R-EX-4 (reason checked and sound)",
   "evidence": "spec/REQUIREMENTS.md:136 (R-CO-2 row) says 'an LLM-derived item with no human action is absent from both export blocks'. The same file lists 'pending items' as a notes section at :12 and shows the 'PENDING ITEMS NOT INCLUDED' heading at :311 (R-EX-4), and D-045(a) says pending items never reach the letter. tests/e2e/test_ladder_gate.py (new test from line 46) requires the pending summary to be absent from the letter and from FLAGS ACCEPTED, FLAGS DISMISSED, EDITED ITEMS, and present only under PENDING ITEMS NOT INCLUDED. Mutants dismissed_exports and pending_exports were killed (ladder gate and matrix).",
   "why_it_matters": "The test is right and the older sentence is stale, so the next reader will think the test is weaker than the requirement. The D-062 total wording and the D-045 'edit alone does not open the export' changes are also sound: the edit test asserts 422 after the edit and 200 after the accept.",
   "fix": "Have the owner reword R-CO-2 and the AC to 'absent from the letter and from every notes section that reports accepted content; listed only under PENDING ITEMS NOT INCLUDED'.",
   "acceptance_test": "grep -n 'absent from both export blocks' spec/REQUIREMENTS.md returns nothing."
  },
  {
   "severity": "nit",
   "title": "Fixed 80/120/150 ms waits in the keyboard and tap loops",
   "evidence": "tests/e2e/test_journey_modes.py:83 (wait_for_timeout(80) after k), :92 (120 after a), :151 (150 after tap). I ran the four new spec files three times in a row while a unit suite was running: '25 passed in 34.52s', '25 passed in 32.92s', '25 passed in 34.12s'. Not flaky today.",
   "why_it_matters": "Fixed sleeps are how a spec turns flaky on a slower machine; a state wait would be exact.",
   "fix": "Replace each wait with expect(...).to_have_attribute('data-review', ...) or a wait on the pending count.",
   "acceptance_test": "grep -c wait_for_timeout tests/e2e/test_journey_modes.py prints 0 and the file still passes 3 runs in a row."
  },
  {
   "severity": "nit",
   "title": "The browser oversize case passes through the demo-mode refusal, so on its own it does not prove the size bound",
   "evidence": "tests/e2e/test_adversarial_ui.py:40 pastes 'x' * (max_chars + 5). With ingest.check_limits disabled (mutant size_limit_off, ingest.py check_limits 'if False and len(t) > max_chars') the demo refusal (409 unrecorded text) still ends in a clear alert, so this case passes. tests/e2e/test_adversarial.py::test_oversize_input_413 failed with 'assert (409 == 413)', so the bound is covered at the API.",
   "why_it_matters": "Small: coverage exists one layer down; the browser case just reads as stronger than it is.",
   "fix": "Say in the docstring that the size bound is proved by test_oversize_input_413, or add a library-mode case that is oversize but recorded.",
   "acceptance_test": "Docstring names the covering test."
  }
 ],
 "whats_right": [
  "Every letter-leak mutant I planted (flag line, reviewer note before and after the total, count line, '73 days', pending or dismissed items exported) is killed by the letter specs together, and the matrix's planted-leak self-test shows its leak check is not vacuous.",
  "Keyboard journey has a working control (pointer-click counter reads 0 on keys, 1 on a mouse click); mutants 'd accepts' and 'review UPDATE without case_id' were killed by the keyboard and two-case specs.",
  "Both suites reproduce at d0b04bc exactly as the sensors file says (unit 5689 passed/2 skipped in a git clone; e2e 411 passed/2 skipped), and the live eval hashes equal HEAD's prompts and lexicon."
 ],
 "questions_for_chris": []
}
```
