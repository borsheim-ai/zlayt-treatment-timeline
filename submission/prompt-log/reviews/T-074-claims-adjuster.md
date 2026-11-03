# T-074 review: claims-adjuster-reviewer (spec sync to D-040 golden)

**Verdict: changes** (one major, no blocker). The two spec lines match the golden exactly and the spec-check tests pass. The spec still carries the cut requirement in R-FL-7, so the decision has not fully propagated.

Model: claude-haiku-5-5, per the brief and the runtime.

## What I checked

- **Lines 280 and 291 (pass).** `diff <(sed -n 280p spec/REQUIREMENTS.md) <(sed -n 58p evals/golden/sample.export.expected.txt)` and the same for 291/69 both exit 0. Commit 83b4353 changes only those two lines (2 insertions, 2 deletions).
- **Tests (pass).** The brief command passes: 62 live, 61 at HEAD archive. `test_eval_spec_check.py::test_real_spec_matches_golden` and the CLI spec-match test are included.
- **Propagation of D-040 into the spec (fails).** See F1 through F3.

## Findings

- **F1 major.** R-FL-7 (`spec/REQUIREMENTS.md:71`) still requires `source_kind = "patient_report"` and the UI text "Patient self-report". Its acceptance cell says "the label renders". The product now does the opposite (`app/backend/flags.py:61`; `tests/unit/test_flags_pass.py:95` asserts every flag is `source_kind == "record"`). The spec and the tests contradict each other. Major, not blocker, because D-040 is recorded and the product matches it. If the gate reads R-FL-7 literally, the product fails it and this becomes a blocker until the spec is amended.
- **F2 minor.** `spec/SAMPLE_CASE_TRUTHS.md:9` still labels the record 9 quote "(9 — patient self-report, not a physician's causation opinion)".
- **F3 minor.** `spec/REQUIREMENTS.md:371`, deviation row 4, says the golden uses `patient_self_report`. Its evidence command `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md` now returns no output, so the row is stale.
- **F4 minor.** Contract and design docs still show the cut label: `memory/contracts/api.md:184-186` (example f_pat_9 with "Patient self-report" title and explanation), and `docs/UI_DESIGN_BRIEF.md:132` (a "Patient self-report" chip row). `api.md:212` already records D-040, so the example is inconsistent with its own note.

```json
{"card": "T-074", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 83b4353 (spec/REQUIREMENTS.md lines 280, 291) checked against evals/golden/sample.export.expected.txt lines 58, 69; spec residue searched across spec/, memory/contracts/, docs/, evals/golden/; live tree /Users/arsis/zlayt-pm-project (dirty) and HEAD 83b4353 extracted with git archive",
 "exercised": [
  "read personas/claims-adjuster.md in full; memory/ORCHESTRATOR_DECISIONS.md D-040 and its Source column; board show T-074 (notes 02:49:08Z to 02:49:12Z, commits: [])",
  "git show --stat 83b4353; git show 83b4353 -- spec/REQUIREMENTS.md (2 lines changed, both suffix removals)",
  "diff <(sed -n 280p spec/REQUIREMENTS.md) <(sed -n 58p evals/golden/sample.export.expected.txt) -> identical (exit 0); diff <(sed -n 291p spec/REQUIREMENTS.md) <(sed -n 69p evals/golden/sample.export.expected.txt) -> identical (exit 0)",
  "sed -n 71p spec/REQUIREMENTS.md (R-FL-7 full text); sed -n 371p spec/REQUIREMENTS.md; sed -n 9p spec/SAMPLE_CASE_TRUTHS.md; grep -rn -i 'patient self|self-report|patient_report|self_report|chip' spec/ submission/ memory/ docs/",
  "grep -n 'patient_self_report|summary+excerpt' evals/golden/README.md -> no output; grep -n 'Causation rests on patient self-report' evals/golden/sample.expected.json -> line 625 (K3)",
  "read app/backend/flags.py:61 (source_kind record, D-040 comment) and tests/unit/test_flags_pass.py:95-100",
  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py -> 62 passed in 1.82s (live tree; includes an uncommitted T-070 test in test_eval_runner.py)",
  "same three files at git archive 83b4353 (artifacts/review-evidence/T-072-T-074-83b4353, removed afterwards) -> 61 passed",
  "board validate (read-only) -> 'ok (74 file(s))'",
  "evals.run --check-spec not run (writes evals/reports, outside my write paths); the spec-match behaviour is covered by test_eval_spec_check.py"
 ],
 "verdict": "changes",
 "scores": {"spec_lines_match_golden": 5, "decision_propagated_to_spec": 2, "tests_green_at_commit": 5, "spec_residue_cleanup": 2},
 "findings": [
  {"severity": "major",
   "title": "R-FL-7 still requires the cut 'Patient self-report' label; spec and product tests contradict",
   "evidence": "spec/REQUIREMENTS.md:71: | R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = \"patient_report\"` and the UI text \"Patient self-report\". It is never presented as a physician's opinion. | Sample record 9 flag has `source_kind == \"patient_report\"` and the label renders. Golden `must_not` M10 passes. | UT + E2E |. Product: app/backend/flags.py:61 `\"source_kind\": \"record\",   # D-040: no code or model labels who is speaking`; tests/unit/test_flags_pass.py:95 test_no_flag_carries_a_self_report_chip asserts all source_kind == \"record\" for records 7 and 9. memory/ORCHESTRATOR_DECISIONS.md D-040 says the writer mirrors product decisions into spec/REQUIREMENTS.md; R-FL-7 was not amended.",
   "why_it_matters": "The card's lines 280 and 291 are right, but the same D-040 cut leaves a written requirement that demands the label. An attorney or grader reading R-FL-7 would expect 'Patient self-report' in the UI and would find it absent. As written, the shipped product fails R-FL-7's acceptance cell. Major, not blocker, because the decision is recorded and the product matches it; the defect is the unamended spec. If the gate reads R-FL-7 literally, it is a blocker until amended.",
   "fix": "Spec sync by writer or orchestrator: rewrite R-FL-7 to D-040. Suggested text: 'No speaker label. Every excerpt is a verbatim record excerpt with its source label (D-040). A flag never presents a patient statement as a physician's opinion.' Acceptance cell: 'Flags carry source_kind = record; no speaker label in the UI; test_no_flag_carries_a_self_report_chip passes.'",
   "acceptance_test": "grep -n 'Patient self-report' spec/REQUIREMENTS.md returns no hits outside the decision log; R-FL-7's acceptance cell names test_no_flag_carries_a_self_report_chip; the spec-match test still passes."},
  {"severity": "minor",
   "title": "Case truth sheet labels the record 9 quote 'patient self-report'",
   "evidence": "spec/SAMPLE_CASE_TRUTHS.md:9: - **Causation-weakening language:** ... \"Patient states symptoms began after the January collision\" (9 — patient self-report, not a physician's causation opinion); ...",
   "why_it_matters": "The truth sheet is the case's reference. It still records the speaker label that D-040 cut. Not rendered anywhere, but it is the source the team grades against.",
   "fix": "Replace the parenthetical with the verbatim marker, e.g. (9 — verbatim 'Patient states ...').",
   "acceptance_test": "grep -n -i 'self-report' spec/SAMPLE_CASE_TRUTHS.md returns nothing."},
  {"severity": "minor",
   "title": "Deviation row 4 is stale: its evidence command now returns nothing",
   "evidence": "spec/REQUIREMENTS.md:371: | 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` ... | `grep -n \"patient_self_report\\|summary+excerpt\" evals/golden/README.md` | orchestrator (D-entry) |. Run: the grep on evals/golden/README.md returns no output.",
   "why_it_matters": "A deviation row that no longer reproduces misleads the next reviewer about what is still open.",
   "fix": "Close the row with a pointer to D-040, or update it to the current golden state.",
   "acceptance_test": "The row's stated evidence command either matches a current line or the row is marked closed."},
  {"severity": "minor",
   "title": "Contract example and design brief still show the cut chip and title",
   "evidence": "memory/contracts/api.md:184-186: { \"id\": \"f_pat_9\", \"type\": \"causation\", \"category\": \"patient_report\", \"source_kind\": \"record\", \"title\": \"Patient self-report\", \"explanation\": \"Patient self-report (not a physician's opinion) ...\"; api.md:212 already records D-040 ('No chip or label says who is speaking'). docs/UI_DESIGN_BRIEF.md:132: | `Patient self-report` | speech bubble | Patient self-report | `--text-muted` outline | only where code set `source_kind=patient_report` (T-061 narrows this) |.",
   "why_it_matters": "Two docs a builder would follow still specify the cut label. api.md:184-186 contradicts its own line 212. The design brief still lists a chip the product no longer has.",
   "fix": "Update the api.md example to the neutral title and explanation. Mark the design-brief row as cut under D-040. Owner: backend for api.md; orchestrator to route the design brief.",
   "acceptance_test": "grep -rn 'Patient self-report' memory/contracts docs/ returns no hits outside decision history."}
 ],
 "whats_right": [
  "Lines 280 and 291 are byte-identical to golden lines 58 and 69 (diff exit 0 both), and commit 83b4353 changes only those two lines.",
  "test_eval_spec_check.py and test_eval_runner.py pass at HEAD 83b4353 (61 passed across the three files) and on the live tree (62 passed).",
  "The orchestrator's self-performed edit is disclosed in the card note (02:49:12Z), so an independent check was possible and this review re-derived the result."
 ],
 "questions_for_chris": [
  "Should R-FL-7 be rewritten by the writer (product note owner) or by the orchestrator (spec is orchestrator-synced per T-074 notes)? Outside my lens; I only need the amendment to exist before the M3 gate.",
  "Board attribution (outside my lens, noted for the orchestrator): T-074 records the AC check under the architect role for an edit the orchestrator made, and commits is empty although 83b4353 exists."
 ]}
```
