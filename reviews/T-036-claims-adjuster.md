# T-036 LLM flag passes — claims-adjuster review (Gary Pruitt)

Verdict: **fail** (1 blocker, 3 major, 2 minor, 1 nit).

On the sample the lexicon floor does surface every flag I would use: 73-day gap, accident-date conflict (one flag, both sides shown, no choice made, no delay figure), prior LBP 2023 (rec 3), "may represent degenerative" (rec 8, as both `degenerative_language` and `speculative_language`), missed appointments (rec 6), new onset (rec 7), wrong intake date (rec 7, separate flag), and patient-states causation (rec 9, `patient_report`). K1–K5 + P1/P2 match one-to-one. Case_07 record 2's prior-ACL flag survives an obedient model and the full pipeline run. Judge #3/#4 error, unsure and disagree all land in `needs_review`. The 12-visits-vs-discharge conflict (C2) exists only if the model supplies it.

What I could attack:
- **The `objective_negative` title.** Its user-visible title is "No objective findings noted", which is false for a sentence like "Cervical ROM full, no spasm noted."
- **C2 can vanish silently.** If the conflict pass fails or returns an unexpected shape, C2 disappears and the run reports `status done` with no error or warning.
- **The suite is red.** `tests/unit/test_pipeline.py` has 3 failures that the handoff did not mention.
- **K5 is labelled "Patient self-report".** Nothing in record 7 says the patient wrote the intake form.

AC6 and AC8 are open on the board (`done: false`), deferred by the backend. I did not rate them.

```json
{"card": "T-036", "persona": "claims-adjuster-reviewer", "model": "claude-sonnet-5-5",
 "scope": "app/backend/flags.py, lexicon_scan.py, flag_templates.py, judges.py, pipeline.py (flag/conflict stages), app/llm/prompts/flags_v1.md, tests/unit/test_flags_sample.py, test_flags_injection.py, test_flags_pass.py, test_pipeline.py; card commit 199785f; sample case + case_06/07/08 golden; no live app (fixture/scripted LLM only)",
 "exercised": [
  "python3 tools/board.py show T-036",
  ".venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_schemas.py -q -> 50 passed",
  ".venv/bin/python -m pytest tests/unit -q -> 3 failed, 694 passed (FAILED tests/unit/test_pipeline.py::test_j3_error_or_unsure_makes_llm_conflicts_needs_review[j30], [j31], test_j3_conflict_verdict_keeps_semantic_conflict_and_code_conflict_is_unaffected)",
  ".venv/bin/python -m pytest tests/unit/test_flags_pass.py tests/unit/test_conflicts.py tests/unit/test_judges.py -q -> 40 passed",
  "artifacts/review-evidence/T-036-adjuster-probe.py on sample, case_06, case_07, case_08: per-record flags with the model returning nothing (outputs in T-036-sample-probe.txt, T-036-cases-probe.txt)",
  "artifacts/review-evidence/T-036-adjuster-probe2.py: J4 agree/disagree/unsure/error; LLM_ONLY; off-list category, prose field, non-verbatim quote, wrong type/category; conflict pass + J3 variants (T-036-probe2.txt)",
  "artifacts/review-evidence/T-036-probe3.py: full pipeline on sample with the conflict stage LLMFailed / FixtureMiss / plan-vs-actual scripted (T-036-probe3.txt)",
  "full pipeline on case_07 with an obedient model (T-036-case07-pipeline.txt): f_r2_1 prior_surgery 'History: prior ACL repair of the same knee in 2019.' present",
  "ad hoc lexicon probes for objective_negative / scene_facts / litigation_referral wording",
  "read flags.py, flag_templates.py, lexicon.yaml entries intake_form_accident_date and plan_not_completed, grounding.has_self_report, frontend/flags.js:63 and timeline.js tray, pipeline.py:255-295"
 ],
 "verdict": "fail",
 "scores": {"surfaces_every_attack_item_on_sample": 4, "no_invented_or_overstated_text": 2, "one_to_one_K1_K5": 5, "injection_isolation": 5, "judge_failure_handling": 4, "code_only_flag_text": 3, "test_honesty": 2},
 "findings": [
  {"severity": "blocker",
   "title": "objective_negative flags display the title 'No objective findings noted' - the word 'objective' is user-visible and false for the sentence it quotes",
   "evidence": "flag_templates.py:132 `\"objective_negative\": lambda v: (\"No objective findings noted\", ...)`. Probe: lexicon_flags on 'Cervical ROM full, no spasm noted.' -> category objective_negative, title 'No objective findings noted', explanation 'Wording about absent or normal findings in Dr X (March 1, 2026): “Cervical ROM full, no spasm noted.”.' Also 'No objective findings. Pain 4/10.' -> same title. The T-036 card note (2026-11-02T01:44:48Z) says: 'category objective_negative is internal; UI/flag templates must never display it as objective.' The handoff confirms: \"titles say 'No objective findings noted'\". The guarding test (test_flags_pass.py:80-83) only asserts the string 'objective_negative' is absent, and runs on record 2, which has no hit, so it passes vacuously.",
   "why_it_matters": "The tool states, in its own voice, that no objective findings were noted, when the quoted record documents an objective finding (full ROM, no spasm). Cervical ROM is a measured finding. That is an invented, overstated finding and my own 'subjective-only / objective findings' label supplied by the tool (checklist 9, 18). It breaks the orchestrator's explicit constraint.",
   "fix": "Retitle with neutral wording that quotes the record and uses no 'objective' or 'subjective' vocabulary, e.g. title 'Normal or absent findings wording', explanation 'Wording about normal or absent findings in <provider> (<date>): “<quote>”.' Keep the category key internal.",
   "acceptance_test": "Unit test that renders every category in flag_templates.TEMPLATES and, for every golden case and for lexicon hits on 'Cervical ROM full, no spasm noted.' and 'No objective findings.', asserts re.search(r'objective|subjective', title + explanation, re.I) is None."},
  {"severity": "major",
   "title": "C2 (12 planned visits vs discharge at visit 9) disappears silently when the conflict pass fails or returns an unexpected shape; run still says status done",
   "evidence": "flags.py:189-192 `except P.FixtureMiss: return []` and `except (AU.LLMFailed, ValidationError, TypeError, ValueError): return []`. Probe3 (pipeline on sample, conflicts=LLMFailed): `status done errors [] warnings []`, flags = gap, accident-date conflict, 7 lexicon flags, no f_cx*; identical for FixtureMiss. Same with the old record_id-shaped output in test_pipeline.py:168-169 -> run_conflict_pass(...) == []. The lexicon entry plan_not_completed ('Plan of care: 12 visits.') is strength low and produces no flag (probe: rec 4 -> no flags). The per-record pass degrades visibly (lexicon floor + LLM_FAILED_AFTER_RETRIES); the conflict pass has no floor and no marker.",
   "why_it_matters": "R-FL-2(b) is a sample 'must raise'. An outage is indistinguishable from 'no conflict found'. The attorney never sees that the plan-vs-actual comparison did not run, so a weakness I would attack is hidden without any signal.",
   "fix": "When the conflict pass errors, misses the fixture or fails schema, emit a visible needs_review item (a record_warning or conflict-group notice drawn from a code template) and a pipeline warning. Do not return an empty list silently. Optionally add a code floor for plan-count vs discharge.",
   "acceptance_test": "Pipeline test: conflicts=LLMFailed / FixtureMiss / schema-invalid -> out['warnings'] or a flag with a LLM_FAILED_AFTER_RETRIES-style reason is present; the result is not status done with zero signal."},
  {"severity": "major",
   "title": "Full unit suite is red: 3 test_pipeline.py failures that the handoff did not report; they are the only pipeline-level tests of AC5/AC9 judge #3 behaviour",
   "evidence": ".venv/bin/python -m pytest tests/unit -q -> `3 failed, 694 passed`; FAILED tests/unit/test_pipeline.py::test_j3_error_or_unsure_makes_llm_conflicts_needs_review[j30], [j31], test_j3_conflict_verdict_keeps_semantic_conflict_and_code_conflict_is_unaffected, each `assert ([])`. Cause: SEM fixture (test_pipeline.py:168-169) emits conflict flags with an extra `record_id` field and a single `excerpt`, which the new FlagPass schema rejects, so run_conflict_pass returns []. Handoff says 'Verified: 59 flag/boundary tests pass.' AC9 evidence cites judges.py paths, not this test.",
   "why_it_matters": "The J3 error and unsure handling is the AC the brief asks me to check, and its end-to-end test is failing. 'Done' evidence rests on unit-level tests alone. The failure is also swallowed with no signal (see the previous finding).",
   "fix": "Update the SEM fixture to the new two-quote shape (excerpt + excerpt_b), or make the pipeline contract explicit; run the full tests/unit before handoff.",
   "acceptance_test": ".venv/bin/python -m pytest tests/unit -q reports 0 failed, including the three test_pipeline.py J3 tests."},
  {"severity": "major",
   "title": "K5 (intake-form accident date) is labelled source_kind patient_report ('Patient self-report' chip), but record 7 does not say the patient supplied the intake form",
   "evidence": "Pipeline sample run: flag f_r7_1 (accident_date_provenance) `source_kind == 'patient_report'`; frontend/flags.js:63 renders chip 'Patient self-report' whenever source_kind is patient_report and the title is not 'Patient self-report'. Cause: lexicon.yaml `intake_form_accident_date` has `self_report: true`; grounding.has_self_report('Date of accident per EMS report.') also returns True. Record 7 text: 'Date of accident per intake form: 2026-01-19.' - no author stated. Golden K5 carries no source_kind.",
   "why_it_matters": "R-FL-7 reserves the label for wording that rests on the patient's own statement. Attributing an unattributed intake line to the patient is a fact the record does not state (checklist 10, 19). A chip on an EMS-sourced date would be plainly wrong.",
   "fix": "Set patient_report only on explicit patient-attribution markers (C/O, Patient states/reports, per patient). Remove self_report from intake_form_accident_date, and tighten the generic 'per ...' pattern so it cannot match 'per EMS report'.",
   "acceptance_test": "Unit test: source_kind of the record-7 intake flag == 'record'; of 'Date of accident per EMS report.' == 'record'; of rec 9 and rec 3 flags == 'patient_report'."},
  {"severity": "minor",
   "title": "An LLM conflict with only one quote is accepted and rendered as a two-sided conflict with garbled text",
   "evidence": "Probe: conflicts output {type conflict, category treatment_plan_vs_actual, excerpt 'Plan of care: 12 visits.'} (no excerpt_b) -> title 'Treatment plan and what followed differ', explanation 'Capital PT, initial evaluation (January 23, 2026): “Plan of care: 12 visits.”. the record.', state needs_review JUDGE_UNAVAILABLE (J3 skipped at flags.py:238-239).",
   "why_it_matters": "The title asserts a difference but cites one side; it reads as an unfinished sentence ('the record.'), and no judge checked it.",
   "fix": "Require excerpt_b for conflict flags (reject as SCHEMA_INVALID otherwise), or render a single-quote variant that does not claim a difference.",
   "acceptance_test": "Test: conflict without excerpt_b is rejected or renders no 'differ' title and no 'the record.' fragment."},
  {"severity": "minor",
   "title": "Two code templates characterise causation instead of only quoting",
   "evidence": "flag_templates.py:125 'Wording that could be used to question causation in ...' (speculative_language); flag_templates.py:130 'Wording suggesting another cause in ...' (alternative_cause), shown on case_06 rec 2 'Has been seeing a chiropractor off and on since a lifting injury several years ago.'",
   "why_it_matters": "R-FL-4: 'The tool quotes the wording; it never rules on causation.' A template that predicts how the quote will be used, or says it suggests another cause, is the tool arguing my side. It also differs from the neutral 'Mention of a prior or pre-existing condition' style.",
   "fix": "Use neutral labels such as 'Hedged wording in <provider> (<date>): “...”' and 'Mention of another injury or event in ...'.",
   "acceptance_test": "Templates test forbids 'question', 'suggest', 'could be used' and 'cause' in title + explanation."},
  {"severity": "nit",
   "title": "Double terminal punctuation in every template explanation",
   "evidence": "'... mentions a prior or pre-existing condition: “Patient reports low back pain in 2023, resolved.”.' (probe output, rec 3)",
   "why_it_matters": "A quote that already ends in a period is followed by a second one; it looks careless in a document that goes to counsel.",
   "fix": "Strip the trailing period inside the quote or omit the template period after a closing quote.",
   "acceptance_test": "Rendered explanations contain no '.”.' sequence."}
 ],
 "whats_right": [
  "Per-record isolation holds: 9 calls, one nonce block each, and case_07's prior-ACL flag survives an obedient model both at unit level and in the full pipeline.",
  "Flag text is code-only: an extra prose field in model output voids the model pass and leaves the lexicon flags, a non-verbatim quote is rejected, and an off-list category (accident_dates_differ, failure_to_mitigate) never reaches a title.",
  "J4/J3 disagree, unsure and error each yield needs_review (JUDGE_DISAGREES / JUDGE_UNSURE / JUDGE_UNAVAILABLE), and LEXICON_ONLY / LLM_ONLY are set correctly."
 ],
 "questions_for_chris": [
  "Should an LLM-unavailable conflict stage block the review (status not done) or only warn? I rated a silent pass as the problem either way."
 ]}
```
