# T-015 Eval golden set, round 3 (final): legal-nurse checklist

**Scope note:** the **paralegal-reviewer** agent (Opus 5.5) wrote this review at the orchestrator's request (D.6 brief, round 3). It is judged strictly against the legal-nurse r2 findings in `reviews/T-015-legal-nurse-r2.md`, not against the paralegal checklist. Clinical judgment beyond those findings is outside this agent's lens.

**Verdict: changes** (0 blockers, 1 major, 3 minors).

| r2 finding | r3 status | Evidence |
|---|---|---|
| M1 required_terms on summary+excerpt | **Fixed** | README.md:72 'a **summary** that by itself satisfies every `required_terms` item'. The nurse probe's 4 omission summaries (E1/E2/E8/E9) give `pass_on_summary_only=False`, so they now fail. E2/E8/E9 carry any-of qualifier alternatives. All 9 export summaries pass on the summary alone (probe C). check_golden.py:189-193 grounds every term in the record. |
| M2 patient-attributed causation allowed | **Fixed in substance** | 'Patient states her neck pain is due to the collision.' moved to bad_examples (sample.expected.json:806). M10 bad_examples include 'Patient states the collision caused his symptoms.' H35-H37 `temporal_to_causal` were added and REQ_CAT requires the category. Residual (minor): the literal r2 acceptance grep still finds a good_example with 'due to the collision' (:813). |
| M3 source_kind on whole mixed entries | **Data fixed, checks dead** | Entry-level source_kind is gone. 6 per-sentence spans use `patient_report`, and all are subjective (probe B objective_hit=False). But they are stored under `spans` while README and check_golden.py read `self_report_spans`, so the r2 acceptance test (the checker asserts span verbatim and no objective content) never runs. A mutation passes. K3 flag lacks R-FL-7 `source_kind`. |
| minor: regex leaks (30 of 50) | **27 of 30 closed** | Re-run: `('r2','LEAK'),3`. 'Diagnosed with cervical strain and concussion; CT head negative.' is now caught by summary-only required_terms (D-022). Still leaking: 'Findings may represent degenerative disc disease.' and 'Cervical disc disease at C5-C6.' |
| minor: controls S08/S10 | **Fixed** | S08 'The patient has seen a chiropractor ...' (no sex); S10 'pain radiating to the right arm'; check_golden.py:596 rejects invented pronouns |
| minor: missing judge items | **Fixed** | H38/H39 approximation_dropped, H40 abbreviation_misexpanded ('PT' -> 'prothrombin time'), SE5 kind judge_masked 'Visit 8: pain 8/10, improving.' -> needs_review |
| nit: case_01 'fracture' | **Fixed** | case_01 E1 required_terms ['ankle', 'negative for fracture'] |

Commands run: `python3 evals/golden/check_golden.py` → `golden OK: ... 57 must_nots ..., 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase) ...` EXIT=0. `.venv/bin/python -I artifacts/review-evidence/T-015-r2-nurse-probe.py` → `T-015-r3-rerun-of-r2-nurse-probe.out.txt`. `T-015-r3-paralegal-probe.py` (sections B, C, F) and `T-015-r3-paralegal-mutation.py` on a scratch copy.

```json
{"card": "T-015", "persona": "legal-nurse-reviewer", "model": "claude-opus-5-5",
 "scope": "round 3 (final), commit f8c1948 (git diff 3c5eb7c..f8c1948 -- evals/golden), judged strictly against reviews/T-015-legal-nurse-r2.md findings; written by the paralegal-reviewer agent against the legal-nurse checklist at orchestrator request. Files: README.md, sample.expected.json, case_01/06/08 expected.json, hallucinations.jsonl (40), hallucinations_controls.jsonl (10), sample.export.expected.txt summaries, check_golden.py; decisions D-021, D-022; spec R-FL-7, R-TL-10. No app (pre-code card).",
 "exercised": [
  "python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered' EXIT=0",
  ".venv/bin/python -I artifacts/review-evidence/T-015-r2-nurse-probe.py against f8c1948 -> T-015-r3-rerun-of-r2-nurse-probe.out.txt: COUNTS r1 OK 36, n/a 2; r2 OK 45, LEAK 3, FALSEPOS 2; omission probe pass_on_summary_only=False for E1/E2/E8/E9",
  "T-015-r3-paralegal-probe.py section B (span key inventory, objective-content regex on each span), C (export summaries vs required_terms and span attribution, summary alone), F (M2 examples, hallucination categories, S08/S10, M10, seeded edits, case_01 E1)",
  "T-015-r3-paralegal-mutation.py on a scratchpad copy: objective span under 'spans' -> exit 0; under 'self_report_spans' -> exit 1",
  "read sample.expected.json M2 bad/good examples (:795-815) and K3 (:638); README.md:40 and :72"
 ],
 "verdict": "changes",
 "scores": {"clinical_fidelity_of_reference_wording": 4, "appendix_c_must_not_check_reliability": 4, "hallucination_set_genuineness": 5, "hallucination_failure_mode_coverage": 5, "controls_faithfulness": 5, "objective_vs_subjective_coverage": 3, "summary_omission_measurement": 4},
 "findings": [
  {"severity": "major", "title": "r2 M3 acceptance test still fails: per-sentence self-report spans are correct but sit under key 'spans', so check_golden.py never validates them and a runner built from the README never scores them",
   "evidence": "README.md:40 and check_golden.py:195, :455 read 'self_report_spans'; the JSON uses '\"spans\"' (sample.expected.json:109, :272; case_01_date_formats.expected.json:175; case_06_subtle_pre_existing.expected.json:74, :120, :157). Probe B: 'self_report_spans items = 0; spans items = 6'. Mutation: sample E1 span 'Alert and oriented', source_kind 'WRONG', under 'spans' -> check_golden exit=0. Under 'self_report_spans' -> exit=1 'span contains objective/assessment content'. case_01 E8, case_06 E3 and case_06 E5 attribution appear in no required_terms (probe B attribution_also_in_required_terms=False).",
   "why_it_matters": "The r2 point was that the subjective/objective split must be encoded exactly and checked. The encoding is now right, but the check that would catch a future regression (an exam finding tagged as patient report) is dead. The eval also can't fail a summary that states 'History: occasional stiffness at baseline' or 'old shoulder problem is acting up again' as the provider's finding.",
   "fix": "Rename 'spans' to 'self_report_spans' in the six entries (or align README and checker the other way). Make check_golden.py reject unknown entry keys.",
   "acceptance_test": "The objective-span mutation under the JSON's key makes check_golden.py exit 1. A summary for case_06 E5 without 'patient notes/reports/states/per patient' is not found."},
  {"severity": "minor", "title": "K3 flag has no source_kind 'patient_report' (R-FL-7 value name) and keeps subtype 'patient_self_report'",
   "evidence": "sample.expected.json:638 '\"subtype\": \"patient_self_report\"'; probe: K3 source_kind=None. R-FL-7: 'Sample record 9 flag has source_kind == \"patient_report\"'. The r2 M3 fix asked to 'Use R-FL-7's value name'.",
   "why_it_matters": "The one flag that rests on the patient's own statement is the one R-FL-7 asserts on. Without the field, the runner can't check that the flag is never presented as a physician's opinion.",
   "fix": "Add 'source_kind': 'patient_report' to K3 and rename the subtype.",
   "acceptance_test": "K3.source_kind == 'patient_report'; grep 'patient_self_report' evals/golden/ returns nothing."},
  {"severity": "minor", "title": "r2 M2 literal acceptance grep still matches a good_example, and two M2 good_examples are tool commentary on causation rather than the record's words",
   "evidence": "`grep -n 'due to the collision' evals/golden/sample.expected.json` -> :806 (bad_example, correct) and :813 good_example 'Patient states symptoms began after the collision; no physician states they are due to the collision.' :812 good_example '... per patient report; no physician causation opinion is stated.'",
   "why_it_matters": "The substance of r2 M2 is fixed. But a good example that comments on what no physician said is a judgment about the record set, not a faithful summary. It also drops 'January' from the record's 'January collision'.",
   "fix": "Replace both with record-words examples, e.g. 'Per patient, symptoms began after the January collision.'",
   "acceptance_test": "No M2 good_example contains 'due to' or 'no physician'."},
  {"severity": "minor", "title": "Two regex-floor leaks from r2 remain: 'degenerative disc disease' under a hedge, and 'disc disease' without 'degenerative'",
   "evidence": "T-015-r3-rerun-of-r2-nurse-probe.out.txt: 'r2 V LEAK M3 M8 Findings may represent degenerative disc disease. -> {}' and 'r2 V LEAK M1 M8 M3 Cervical disc disease at C5-C6. -> {}'. (The third leak, the dropped LOC qualifier, is now caught by summary-only required_terms.)",
   "why_it_matters": "The record says 'degenerative change'. 'Degenerative disc disease' and 'disc disease' are diagnoses the radiologist did not make, and a hedge does not make a new diagnosis faithful. Judge #1 is the only backstop.",
   "fix": "Add a sample regex for '\\bdisc disease\\b|\\bDDD\\b' with no hedge exemption (the record never uses the term).",
   "acceptance_test": "Both probe strings become bad_examples that fire; 'Findings may represent degenerative change' stays a good example."}
 ],
 "whats_right": [
  "D-022 is implemented for entries: required_terms are summary-only with any-of qualifier alternatives, so dropping 'without loss of consciousness', the MRI hedge or 'patient states' now fails, and all 9 export summaries pass.",
  "The hallucination set (40) and controls (10) now cover temporal-to-causal, approximation dropped, abbreviation mis-expansion and the masked pain-score swap (SE5), and the controls no longer invent sex or drop 'radiating'.",
  "Every self-report span is a verbatim subjective sentence (C/O, patient states, denies, history, patient notes), and none carries an exam finding or assessment."
 ],
 "questions_for_chris": []}
```
