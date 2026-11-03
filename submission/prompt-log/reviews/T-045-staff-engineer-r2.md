# T-045 staff-engineer review, round 2

Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commits under review: d7ea327 and 7c73294 (HEAD 7c73294 at review time). Verdict: **fail** (1 blocker, 0 majors, 2 nits).

## Result
The three round-1 majors are fixed in code, and the fixes hold under mutation:
- F1 (375 px): the check now bounds scrollWidth by 375 and fails on a 560 px body/html overflow mutant and on a 572 px timeline mutant.
- F2 (rejected item): accept and edit on a rejected item are refused by review.py:280. A unit test and an e2e test both fail when that guard is off, and neither skips under E2E_REQUIRE_DB=1.
- F3 (latest.json): check-fresh exits 0 on the clean clone, and board.py reads evals_ship_bar true from a pointer written by --record-latest. A fixture run leaves the live pointer byte-identical.

The record step behind F3 is not sound. --record-latest copies the `**ship_bar_met: X**` header line of the dated report and never recomputes the bar. Change that one line in a fixture report from False to True and --record-latest records `backend fixture, ship_bar_met True`. The board's Definition-of-Done check then reads True, and check-fresh still exits 0. T-038 AC4 says a fixture cannot satisfy ship_bar_met (R-CO-7). The code path allows exactly that state, so this is a blocker.

Everything below was run on a clean clone of 7c73294 with E2E_REQUIRE_DB=1. The full e2e suite was not re-run this round.

## Checks
- **375 px:** baseline `pytest tests/e2e/test_journey_modes.py` gave 3 passed. With `body, html { min-width: 560px; }` appended to styles.css, 1 failed: `sideways scroll on home: {'scroll': 560, 'body': 560, 'inner': 560, 'visual': 375}` at test_journey_modes.py:44. With `[data-testid="timeline"] { min-width: 572px; }`, 1 failed: `sideways scroll on timeline: {'scroll': 584, ...}`.
- **Rejected guard:** baseline `pytest tests/unit/test_t045_r2.py` gave 9 passed. With `if False and` on review.py:280, 3 failed (both parametrized accept/edit cases, and the dismiss/reset test). The e2e test `test_rejected_attempt_visible_but_not_exportable` passed with no skip on the baseline. With the guard off it failed at test_ladder_gate.py:49, where accept on a rejected item returned 200.
- **check-fresh:** `python -m evals.run --check-fresh` exit 0 at 7c73294.
- **--record-latest:** regenerated latest.json from 20261102T164038Z.md differs from the committed file only in recorded_at. The report's sha256 (03eafb83...) equals recorded_from.sha256. A control with the header set to False gives board evals_ship_bar False, and restoring the true report gives True, so board.py does read the file.
- **Fixture run:** `LLM_BACKEND=fixture python -m evals.run` exits 1 (ship_bar False, blockers as designed). latest.json's sha256 was a14045d4... before and after, and latest.fixture.json was written with backend fixture.
- **Full unit suite:** `E2E_REQUIRE_DB=1 pytest tests/unit -q` at 7c73294 gave 5704 passed, 2 skipped, exit 0.

## Findings
1. **Blocker:** `--record-latest` records a hand-flipped fixture report as ship_bar_met true (findings JSON, F-1).
2. **Nit:** the fixture blocker `4_no_invented_facts` gives no reason, because bar 4 includes three live-only clauses (F-2).
3. **Nit:** m3-sensors.md records 5698 unit passes, and the same commit gives 5704 (F-3).

## Evidence
artifacts/review-evidence/T-045-r2/exercise_log.txt, with the mutant and unit outputs next to it in the same directory. Scratch clones: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t045r2-clean and .../t045r2-bypass (the second one holds the tamper repro).

```json
{"card": "T-045", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commits d7ea327 and 7c73294 (HEAD 7c73294); diff of evals/run.py, tests/e2e/test_journey_modes.py, tests/e2e/test_ladder_gate.py, tests/unit/test_t045_r2.py, evals/reports/m3-sensors.md; clean clone at 7c73294 under the session scratchpad; no app URL (private e2e servers started by the suite); sample case and fixture curated set",
 "exercised": [
  "Read personas/staff-engineer.md, reviews/T-045-staff-engineer.md, board show T-045, git show d7ea327 (evals/run.py, test_journey_modes.py, test_ladder_gate.py) and 7c73294 (m3-sensors.md); read tests/unit/test_t045_r2.py and app/backend/review.py:276-282 at 7c73294.",
  "Clean clone detached at 7c73294 (git status empty). E2E_REQUIRE_DB=1 on every pytest run. Interpreter /Users/arsis/zlayt-pm-project/.venv/bin/python (Python 3.12.2).",
  "python -m evals.run --check-fresh in the clean clone: exit 0. python3 tools/board.py status --json: evals_ship_bar true.",
  "python -m evals.run --record-latest evals/reports/20261102T164038Z.md in the clone: latest.json equal to the committed pointer except recorded_at; sha256 of the report 03eafb83f90c3d46cf8b9bc009dbab0ef17fc7056d7ab4e453e12117036bb5e3 equals recorded_from.sha256.",
  "Control: copy of the live report with header set to False, then --record-latest: board evals_ship_bar False; restored, board True.",
  "LLM_BACKEND=fixture python -m evals.run in the clone: exit 1 (ship_bar False, by design). latest.json sha256 a14045d4f103a318fff28fd394a2444370143b59ad7bb6c707631db0b4e719fd before and after; latest.fixture.json written, backend fixture.",
  "pytest tests/e2e/test_journey_modes.py: baseline 3 passed; mutant body/html min-width 560px: 1 failed, sideways scroll on home {scroll 560, visual 375} at test_journey_modes.py:44; mutant timeline min-width 572px: 1 failed, sideways scroll on timeline scroll 584.",
  "pytest tests/unit/test_t045_r2.py: baseline 9 passed; review.py:280 guard disabled (if False and): 3 failed. pytest tests/e2e/test_ladder_gate.py -k rejected: baseline 1 passed, no skip; guard disabled: failed at test_ladder_gate.py:49 (accept returned 200 on a rejected item).",
  "Tamper repro in a second clone: header of fixture report 20261102T203245Z.md changed from False to True (grep confirmed), --record-latest exit 0 with ship_bar_met=True, latest.json backend fixture ship_bar_met True with three blockers still listed; board evals_ship_bar True; check-fresh exit 0. Control with the untouched report: ship_bar_met False, board False.",
  "Read evals/run.py: ship_bar at 913-928 (bar 4 spans 923-928), evaluate_report at 956 (not called by record_latest), record_latest at 1174, parse_report_md at 1153. Read board/cards/T-038.md AC4 (fixture cannot satisfy ship_bar_met, R-CO-7).",
  "Full unit suite at 7c73294: E2E_REQUIRE_DB=1 pytest tests/unit -q gave 5704 passed, 2 skipped, exit 0 (artifacts/review-evidence/T-045-r2/unit_full_head.out).",
  "Not exercised: full tests/e2e suite (the 412 claim was not re-run this round; only the three targeted spec files above); live claude-cli eval (cost, no run); 375 px check on screens the journey does not visit."
 ],
 "verdict": "fail",
 "scores": {"ship_bar_provenance": 2, "375px_check": 5, "rejected_item_guard_specs": 5, "fixture_run_protection": 5, "evidence_accuracy": 3, "unit_suite": 5},
 "findings": [
  {"severity": "blocker",
   "title": "--record-latest records a hand-edited fixture report as ship_bar_met true; the Definition-of-Done check then reads true",
   "evidence": "evals/run.py:1161 parse_report_md copies the header with the regex for ship_bar_met (True|False) and never recomputes it; evals/run.py:1174 record_latest writes that value; evals/run.py:956 evaluate_report exists but record_latest does not call it. Repro (clean clone, second clone under the session scratchpad): change only line 3 of evals/reports/20261102T203245Z.md from `**ship_bar_met: False**` to `**ship_bar_met: True**`, then `python -m evals.run --record-latest evals/reports/20261102T203245Z.md` prints `latest.json now points at 20261102T203245Z.md: backend=fixture ship_bar_met=True` and exits 0. Result: latest.json has backend fixture, ship_bar_met true, and three blockers still listed; `python3 tools/board.py status --json` gives evals_ship_bar true; `python -m evals.run --check-fresh` exits 0. Unit test tests/unit/test_t045_r2.py:61 (test_record_latest_a_false_report_records_false) only pins the False direction, so nothing catches this.",
   "why_it_matters": "T-038 AC4 (cited by T-045 AC6) says a fixture cannot satisfy ship_bar_met (R-CO-7). The gate is the one number that says the product passed its live bar, and this path lets a fixture run say it did. The sha256 in recorded_from proves the report did not change after recording; it does not prove the report came from the runner, and the runner's own write path (write_report) computes ship_bar, but record_latest bypasses that computation. Nobody needs to do this by accident for it to matter: any edit to the report before recording turns the pointer into a claim nothing checks. The brief asks that the pointer be provenance-backed and not hand-edited; the pointer is provenance-backed only for the file after recording.",
   "fix": "Make record_latest derive ship_bar_met instead of copying it. Have write_report persist the aggregate the runner computed (metrics, assertions, backend, spec_matches_golden, blockers) as a sidecar next to the dated .md, and have record_latest recompute with evaluate_report from that sidecar. Refuse (exit 2, nothing written) when the header disagrees with the recomputed value, when the sidecar is missing, or when the report's backend is not a live backend and the value is True. Keep the fixture-protection in write_report. Re-run the live eval or derive the aggregate for 20261102T164038Z.md, because that report has no sidecar.",
   "acceptance_test": "New unit test: copy a fixture report, set its header to True, call record_latest; expect exit 2, latest.json absent or unchanged. New unit test: a live report whose header says True but whose recomputed bar is False is refused. Repro above: after the flip, record-latest exits 2 and board evals_ship_bar stays false. Existing test_record_latest_a_false_report_records_false keeps passing."},
  {"severity": "nit",
   "title": "The fixture blocker 4_no_invented_facts does not say why; bar 4 includes live-only clauses",
   "evidence": "evals/run.py:923-928: bar 4 is one expression; lines 926-928 require unsupported_count_3run value 0 with runs 3, determinism_3run 1.0 with runs 3, and controls_ok(judge_controls). A fixture run cannot measure those. evals/reports/20261102T203245Z.md:6 lists `4_no_invented_facts` next to `backend=fixture: determinism_3run and unsupported_count_3run need a live backend`, with no link between them. Fixture hallucination_catch 40/40, judge_unavailable 0, must_not 0 (latest.fixture.json from the clone run).",
   "why_it_matters": "A reader of the fixture report sees a blocker on an invented-facts bar that the card's evidence says is clean. The explanation is in code, not in the report.",
   "fix": "Name the unmeasured clauses in the blocker text, or split bar 4 into the grounding part and the live-only part.",
   "acceptance_test": "Fixture report's blocker line names determinism_3run and unsupported_count_3run as the reason bar 4 fails."},
  {"severity": "nit",
   "title": "m3-sensors.md records 5698 unit passes; the same commit gives 5704",
   "evidence": "evals/reports/m3-sensors.md (7c73294): `E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/unit -q` = 5698 passed, 2 skipped. This review: `E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/unit -q` in the clean clone at 7c73294 = 5704 passed, 2 skipped in 397.77s (artifacts/review-evidence/T-045-r2/unit_full_head.out).",
   "why_it_matters": "The sensors file is the evidence the card cites. A count that does not reproduce at the same commit makes the rest of the table harder to trust.",
   "fix": "Re-run the unit suite at the commit the record names and paste its tail line; explain the 6-test difference if it is a fixture or environment effect.",
   "acceptance_test": "The count in m3-sensors.md equals the tail line of the pytest run at the named commit."}
 ],
 "whats_right": [
  "The 375 px check now compares against the 375 px viewport and fails on both a body/html and a timeline overflow mutant, with the measured numbers in the assertion message.",
  "The rejected-item guard has a unit test and an e2e test, neither skips under E2E_REQUIRE_DB=1, and both fail with the guard disabled.",
  "A fixture run never replaces a live latest.json: sha256 unchanged, and the fixture result goes to latest.fixture.json."
 ],
 "questions_for_chris": ["Re-running the live eval (about 40 min and model cost) to produce a sidecar for 20261102T164038Z.md: is that acceptable before the gate, or should the fix derive the aggregate from the runs/ case files instead?"]}
```
