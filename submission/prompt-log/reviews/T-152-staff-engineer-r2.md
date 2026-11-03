# T-152 review, round 2 — staff-engineer-reviewer

Verdict: **pass** (0 blockers, 0 majors, 2 minors carried from round 1, 1 nit). The round-1 major (the unit suite cannot be collected from a clean checkout) is closed.

Pinned commit: 35d828056b967bfd98e8c38ce75610139dcb074f (T-140 round 3, which committed the ledgers), on a `git archive 35d8280` copy in the scratchpad (`T140_r3/head`). I also re-checked two later HEADs because HEAD moved during the review (6379c0b, c2913a6, then c8022fa).

## The claim: `pytest tests/unit` collects on a clean archive with 0 errors
- `git archive 35d8280` into an empty directory, `.venv/bin/python -m pytest tests/unit --collect-only -q -p no:cacheprovider`: `4380 tests collected in 3.11s`, no `ERROR`, no `Interrupted`. The archive has no `artifacts/review-evidence/T-140-adjuster` directory (`ls artifacts/review-evidence` -> `revert-audit.md` only), so nothing reads an untracked reviewer file. The ledgers are tracked: `git ls-files --error-unmatch tests/fixtures/t140_synthetic_ledger_r1.txt tests/fixtures/t140_synthetic_ledger_r2.txt tests/fixtures/t140_restating_labels.txt` lists all three.
- Full unit run on the same archive: `4372 passed, 8 skipped in 294.83s`, 0 failed.
- Golden gate: `pytest tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted tests/unit/test_export.py tests/unit/test_curated_fixtures.py` -> `31 passed`.

## HEAD moved, and one sibling commit broke collection for a while
- `6379c0b` (T-154 r2, frontend) committed `tests/e2e/conftest.py` with a line outside its docstring: `SyntaxError: unterminated string literal (detected at line 89)`. `tests/unit/test_e2e_private_server.py:7` imports `tests.e2e.conftest`, so on archives of 6379c0b and c2913a6 `pytest tests/unit --collect-only` reported `4559 tests collected, 1 error` (and `4595 tests collected, 1 error`), `Interrupted: 1 error during collection`.
- Fixed by `acad4f6 fix(e2e): T-154 r2 repair conftest.py` and guarded by `c8022fa tools: pre-commit also refuses any staged .py that does not parse`. On a fresh `git archive c8022fa`: `4597 tests collected in 3.15s`, 0 errors; `test_e2e_private_server.py`, `test_export.py`, `test_curated_fixtures.py` and the golden-named test give `33 passed`. I filed nothing for this: the break was another card's, it is repaired and now guarded, and T-152 needs no change.

## Findings carried from round 1 (card still has `commits: []`, nothing changed)
1. minor — the golden-named test does not compare to golden. `tests/unit/test_api_routes.py:159` `test_export_equals_golden_when_everything_accepted` still asserts `$8,390.00`, `charges_cents == 839000` and a non-empty notes string, with the comment that byte-equality runs elsewhere. The real golden gates are `tests/unit/test_export.py` and `tests/unit/test_curated_fixtures.py`, and both pass.
2. minor — AC 1 evidence count is stale. The card says `tests/unit 3900 passed 1 skipped` at 2db6ad2; my clean-archive counts are `3893 passed, 8 skipped` at 2db6ad2 (round 1) and `4372 passed, 8 skipped` at 35d8280 (now).
3. nit — the title blames T-139 narrowing; the verified cause of the earlier failure was `ba82071` (why.py had no `join`), as the handoff itself says.

```json
{"card": "T-152", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of 35d8280 in scratchpad T140_r3/head (clean unit collection and full unit run); later archives of 6379c0b, c2913a6 and c8022fa for collection only; tests/unit/test_api_routes.py, test_export.py, test_curated_fixtures.py, test_e2e_private_server.py; tests/fixtures/t140_*; tests/e2e/conftest.py",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-152-staff-engineer.md (round 1), python3 tools/board.py show T-152 (handoff and the orchestrator note about waiting for T-140 round 3)",
  "git archive 35d8280 into T140_r3/head; .venv/bin/python -m pytest tests/unit --collect-only -q -p no:cacheprovider (4380 collected, 0 errors); ls artifacts/review-evidence in the archive (no T-140-adjuster directory)",
  "git ls-files --error-unmatch on the three tests/fixtures/t140_* files (all tracked)",
  "full pytest tests/unit -q on the 35d8280 archive: 4372 passed, 8 skipped in 294.83s",
  "pytest test_api_routes.py::test_export_equals_golden_when_everything_accepted + test_export.py + test_curated_fixtures.py on 35d8280: 31 passed",
  "git archive 6379c0b and c2913a6: pytest tests/unit --collect-only gives 1 error (tests/e2e/conftest.py line 89 SyntaxError, imported by tests/unit/test_e2e_private_server.py:7); git show 6379c0b:tests/e2e/conftest.py parsed with ast to confirm the committed file is broken",
  "git log c2913a6..HEAD (acad4f6 repair, c8022fa parse guard); git archive c8022fa: collect-only 4597 collected, 0 errors; test_e2e_private_server.py + golden/export/curated tests 33 passed",
  "read tests/unit/test_api_routes.py:159-176 in the archive (golden-named test unchanged); evidence in artifacts/review-evidence/T-140-r3/ (collect_35d8280.txt, collect_c2913a6.txt, collect_c8022fa.txt, unit_full_35d8280_tail.txt)"],
 "verdict": "pass",
 "scores": {"claim_accuracy": 5, "reproducibility": 5, "golden_gate_honesty": 3, "evidence_accuracy": 3},
 "findings": [
  {"severity": "minor", "title": "The golden-named test still does not compare to the golden files (carried from round 1)",
   "evidence": "tests/unit/test_api_routes.py:159 def test_export_equals_golden_when_everything_accepted(env); its assertions check '$6,240' absence, 'Billed charges stated in these records: $8,390.00', charges_cents == 839000 and a non-empty internal_notes_text, with the comment 'golden byte-equality runs on the curated fixture set (D-029, qa T-051)'. The golden comparisons are tests/unit/test_export.py and tests/unit/test_curated_fixtures.py (31 passed together with this test on 35d8280).",
   "why_it_matters": "A reader of the card believes the API route output is compared with evals/golden. It is not; coverage exists elsewhere, so the cost is a misleading name and card evidence.",
   "fix": "Rename the test (for example test_export_accept_all_api_contract) or add a letter and notes comparison under FIXTURE_SET=curated; cite test_curated_fixtures as the golden gate in the card.",
   "acceptance_test": "grep -n 'def test_export_equals_golden' tests/unit/test_api_routes.py finds no test whose body never reads evals/golden, or the test reads it."},
  {"severity": "minor", "title": "AC 1 evidence count is not reproduced (carried from round 1)",
   "evidence": "python3 tools/board.py show T-152: AC 1 evidence 'tests/unit 3900 passed 1 skipped' at HEAD 2db6ad2. Clean-archive runs: 2db6ad2 -> 3893 passed, 8 skipped (round 1); 35d8280 -> 4372 passed, 8 skipped in 294.83s (this round).",
   "why_it_matters": "The acceptance record cites counts no clean tree gives.",
   "fix": "Restate AC 1 evidence with the command, the sha and the clean-archive counts (4380 collected, 4372 passed, 8 skipped at 35d8280).",
   "acceptance_test": "The counts in the card's AC 1 evidence equal the output of the quoted command on git archive of the quoted sha."}
 ],
 "whats_right": [
  "Collection is clean on a pure archive: the ledger fixtures are tracked and no test reads a reviewer directory, so the unit gate no longer depends on an untracked file.",
  "The sibling-commit syntax break (6379c0b) was repaired within two commits and c8022fa adds a pre-commit guard that refuses any staged .py that does not parse.",
  "The card's own claim holds: there was no golden drift at 2db6ad2 and the golden and export tests pass at 35d8280 and c8022fa."],
 "questions_for_chris": []}
```
