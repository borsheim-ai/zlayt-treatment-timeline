# T-051 round 3 privacy-compliance review (Nadia Farouk persona)

Verdict: pass, judged strictly on the three T-051 acceptance criteria, as the orchestrator directed after triage of round 2.

Triage disposition of round 2 findings:
- F1 (AI attestation line, blocker): withdrawn for T-051 per triage. The line is scoped to the treatment section, which holds only accepted items in the letter, and it reports "Items not reviewed: N". I accept that scope. I keep one residual concern, recorded in questions_for_chris rather than as a finding: the sentence still names a human action ("accepted by the paralegal") that did not occur when N is greater than 0. Whoever owns the export text should decide whether the wording should say so.
- F2 (audit endpoint returns full LLM I/O and record text): routed to T-040 per triage. Not a T-051 finding.
- F3 (JSON export carries provenance and item ids), F4 (fixture_set not in health or eval report; recorded/ split absent; badge label), F5 (injection case not exercisable on the curated set): outside the three T-051 ACs. Carried as notes to T-040/T-042 and to the injection-control card; not counted in this verdict.

## Acceptance criteria

**AC1: tests/fixtures/llm/curated/ exists; LLM_BACKEND=fixture FIXTURE_SET=curated run on the sample gives an export byte-equal to evals/golden/sample.export.expected.txt.** Met.
- `tests/fixtures/llm/curated/` holds 38 JSON files.
- `.venv/bin/python tests/fixtures/make_curated.py --check` (exit 0): `entries: 9 non-verified: []` and `letter equal: True | notes equal: True`.
- The live server runs with `FIXTURE_SET=curated` (process env read from pid 72586). Its sample audit for case 7qKrI_PDigtMvygY6r0aXw shows 38 calls, 0 errors, all `fixture`, recorded_from backend `curated`.

**AC2: tests/e2e/test_api.py::test_export_is_deterministic_and_equals_golden passes on the curated set.** Met.
- `.venv/bin/python -m pytest tests/e2e/test_api.py -k golden -v -rs`: `test_export_is_deterministic_and_equals_golden PASSED`, `1 passed, 7 deselected`, no skip.
- `.venv/bin/python -m pytest tests/e2e/test_api.py -q 2>&1 | tail -3`: `8 passed in 2.30s`.
- The test accepts every entry, charge and flag through the live API, then asserts `letter_text` equals the golden LETTER block byte for byte and that two exports are identical. It is not a mock.

**AC3: every curated response file carries a CURATED header and passes the same grounding verifier and judges as live output.** Met.
- Header check (`python -I` over the 38 files): every file has a top-level `CURATED` key and `recorded_from.backend == "curated"`.
- Coverage: the sample replay used 38 distinct `prompt_sha256` keys. The curated directory has 38 files. Files unused: 0. Keys without a file: 0. So every file is replayed through the real pipeline.
- Verification: the replay goes through `PL.run_pipeline` (make_curated.py `check()`), and `entries: 9 non-verified: []` shows every entry reached `verified` through the grounding verifier and judge path.

## Other checks run this round
- Evals refusal: `FIXTURE_SET=curated .venv/bin/python -m evals.run --out <scratchpad>/evals-out` and `LLM_FIXTURE_DIR=tests/fixtures/llm/curated ...`: both exit 2 with the refusal message, no report written.
- Identifier grep over tests/fixtures: no hits.
- Board (read-only): `.venv/bin/python tools/board.py show T-051` before this round showed AC1 to AC3 `done: true`.

## Exercised
- `.venv/bin/python tests/fixtures/make_curated.py --check` (exit 0)
- `.venv/bin/python -m pytest tests/e2e/test_api.py -q 2>&1 | tail -3` and `-k golden -v -rs`
- `sed -n` of tests/e2e/test_api.py:29-36 (golden test body, via grep -A)
- `curl` GET /api/cases/7qKrI_PDigtMvygY6r0aXw/audit: 38 calls, 0 errors, 38 distinct prompt_sha256 keys vs 38 curated files
- `python -I` header check over tests/fixtures/llm/curated/*.json
- `FIXTURE_SET=curated` and `LLM_FIXTURE_DIR` evals refusal, exit 2
- Earlier round-2 exercises still stand (identifier grep, live health, injection 409, case_07 probe, export and audit reads) and are recorded in reviews/T-051-privacy-compliance-r2.md

```json
{"card": "T-051", "persona": "privacy-compliance-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 4e8f43d (tests/fixtures/llm/curated/* 38 files, tests/fixtures/make_curated.py); live app http://127.0.0.1:7860 with FIXTURE_SET=curated; tests/e2e/test_api.py; evals/run.py refusal; T-051 acceptance criteria 1-3 only",
 "exercised": [
  "tests/fixtures/make_curated.py --check -> entries 9 non-verified []; letter equal True; notes equal True (exit 0)",
  "pytest tests/e2e/test_api.py -q | tail -3 -> 8 passed in 2.30s",
  "pytest tests/e2e/test_api.py -k golden -v -rs -> test_export_is_deterministic_and_equals_golden PASSED",
  "read tests/e2e/test_api.py:29-36 (golden test asserts letter_text equals golden LETTER block)",
  "live audit GET /api/cases/7qKrI_PDigtMvygY6r0aXw/audit: 38 calls, 0 errors, 38 distinct prompt_sha256 equal to 38 curated files (0 unused)",
  "python -I header check over 38 curated JSON files: CURATED key present, recorded_from.backend curated",
  "FIXTURE_SET=curated and LLM_FIXTURE_DIR evals.run: exit 2, refusal message, no report written",
  "tools/board.py show T-051 (read-only) prior to this round"
 ],
 "verdict": "pass",
 "scores": {"ac1_curated_set_byte_equal_export": 5, "ac2_e2e_golden_test_passes": 5, "ac3_curated_header_and_verifier_parity": 5, "synthetic_data_only": 5, "evals_isolation": 5},
 "findings": [],
 "whats_right": [
  "All 38 curated files are replayed by the sample run (38 distinct prompt hashes, 0 unused), so the verifier and judges see every file.",
  "The golden e2e test runs against the live server and asserts byte equality of the letter, not a mock.",
  "evals.run refuses the curated set with exit 2 before writing any report."],
 "questions_for_chris": ["Residual concern from round 2 (not a T-051 finding, withdrawn by triage): the export's internal-notes sentence says every item was accepted by the paralegal while N items are pending (N=23 on a fresh sample case). The letter scope is accurate; the sentence still names a human action that did not happen when N is greater than 0. Should the wording change, or is the treatment-section scope enough?"]
}
```
