# T-051 privacy-compliance review (Nadia Farouk)

Verdict: changes. The curated set itself is honest and synthetic: all 38 files carry a top-level `CURATED:` header ("Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029)") and `recorded_from.backend: "curated"`. The grounding replay passes. Three issues: AC1 is ticked done although byte-equality fails; nothing structural keeps the curated set out of eval runs; the "cached demo (curated responses)" label is not built yet (requirement for T-040/T-042, listed below, not a finding).

Requirement carried to T-040/T-042 (not a finding here): the badge at `app/frontend/app.js:11` reads only "cached demo". D-029 requires "cached demo (curated responses)". `/api/health` reports `backend: "fixture"` for both sets, so the UI cannot tell curated from recorded. Health needs a `fixture_set` field, and the export or audit view should show it too, so an attorney can see that the summaries were not model output.

```json
{"card": "T-051", "persona": "privacy-compliance-reviewer", "model": "claude-sonnet-5-5",
 "scope": "tests/fixtures/llm/curated/ (38 files), tests/fixtures/make_curated.py, app/llm/backends/fixture.py, evals/run.py, app/frontend/app.js, tests/e2e/test_api.py; board card T-051; D-029",
 "exercised": [
  "python3 tools/board.py show T-051 (AC1 done:true evidence 'x'; AC2 done:false; note says byte-equality NOT yet)",
  "grep D-029 in memory/ORCHESTRATOR_DECISIONS.md",
  "python3 loop over tests/fixtures/llm/curated/*.json: 38 files, every one has a top-level 'CURATED:' header and recorded_from.backend == 'curated'; output: '38 bad: []'",
  "grep -rniE for ssn/mrn/phone patterns in curated/: no hits",
  ".venv/bin/python tests/fixtures/make_curated.py --check: 'entries: 9 non-verified: []' (grounding replay passes) but 'letter equal: False | notes equal: False' with a diff in the BILLED CHARGES Source quote lines",
  ".venv/bin/python -m pytest tests/e2e/test_api.py -k deterministic_and_equals_golden -rs: SKIPPED, 'app server not running at http://localhost:7860'",
  "read app/llm/backends/fixture.py (only LLM_FIXTURE_DIR; no FIXTURE_SET), grep evals/run.py for fixture-set selection, app/frontend/app.js:11",
  "ls tests/fixtures/llm/recorded: does not exist"
 ],
 "verdict": "changes",
 "scores": {"synthetic_data_only": 5, "curated_labelling_in_files": 5, "grounding_parity": 4, "honesty_of_demo_label": 2, "separation_from_ship_bar_metrics": 3, "card_accuracy": 2},
 "findings": [
  {"severity": "major", "title": "AC1 ticked done although byte-equality with the golden export fails",
   "evidence": "board show T-051: AC1 'done: true, evidence: x'. The card note says 'Byte-equality NOT yet' and 'AC1/AC2 blocked'. make_curated.py --check prints 'letter equal: False | notes equal: False' with a diff: golden 'Source [Ex. __ / Bates __]: \"ER charges: $6,240.\"' vs got the whole record excerpt 'Dx: cervical strain; ... ER charges: $6,240.'. The same diff appears for the $2,150 MRI charge.",
   "why_it_matters": "The curated set exists so that the demo and E2E are deterministic and honest about being golden-conformant. A board that marks the byte-equality AC done with placeholder evidence overstates verified state, and a later reviewer could rely on it. The skipped e2e test also means no byte-equality run has been seen.",
   "fix": "Untick AC1 (or replace the evidence with the command and its output) until the export builder and FIXTURE_SET support land. Keep the card in review or blocked. Do not edit the golden to fit the output.",
   "acceptance_test": "FIXTURE_SET=curated LLM_BACKEND=fixture make run, then pytest tests/e2e/test_api.py::test_export_is_deterministic_and_equals_golden passes (not skipped). The AC1 evidence field quotes that output."},
  {"severity": "minor", "title": "No structural guard keeps the curated set out of eval and ship-bar runs, and the recorded/ split in D-029 does not exist yet",
   "evidence": "tests/fixtures/llm/recorded/ does not exist; recorded fixtures still sit in tests/fixtures/llm/*.json and curated is a subdirectory (38 files). app/llm/backends/fixture.py:13 selects the directory only through LLM_FIXTURE_DIR; there is no FIXTURE_SET. The evals/run.py grep finds no fixture-set selection or recording: report fields are only 'backend' and ship_bar. Today the root default means evals do not read curated/, and ship_bar blocks any non-live backend (evals/run.py:470-471), so no metric is contaminated now.",
   "why_it_matters": "D-029 says ship-bar metrics come only from live and recorded runs. That currently holds only by directory layout. If someone points LLM_FIXTURE_DIR at curated/ for evals, hallucination_catch_rate and the other fixture-computed metrics would be measured against hand-written answers and the report would not say so.",
   "fix": "Implement FIXTURE_SET (recorded|curated) in fixture.py with recorded as the default. Record fixture_set in the eval report and in /api/health. Make evals/run.py refuse, or mark every metric not_measured, when fixture_set is curated. Move the recordings to recorded/ as D-029 states.",
   "acceptance_test": "A unit test runs evals with FIXTURE_SET=curated and asserts the report carries fixture_set='curated', with ship_bar blocked or all metrics not_measured. Another test asserts the default set is recorded."}
 ],
 "whats_right": [
  "Every curated file carries a top-level CURATED header that says 'Not a model output' and names the ship-bar exclusion, and recorded_from.backend is 'curated', so provenance survives into the audit view.",
  "The curated set replays through the real fixture backend: 9 entries verified, flags verified, so it does not bypass the grounding verifier.",
  "The curated content derives from the fictional Appendix A golden case only; no identifier patterns found."
 ],
 "questions_for_chris": []}
```
