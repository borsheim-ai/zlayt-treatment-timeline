---
name: flag-pass-review-patterns
description: T-036 flag-engine review (2026-11-01): recurring weak spots — vacuous guard tests, silent-empty on LLM failure, label inference, full-suite not run by worker
metadata:
  type: project
---

T-036 r0 (fail): sample flags all surface via lexicon floor and K1-K5 one-to-one holds, but:
- flag_templates.py title "No objective findings noted" for objective_negative (orchestrator said never display "objective");
  the guard test checks only the string "objective_negative" on a record with no hit, so it passes vacuously.
- run_conflict_pass swallows LLMFailed/FixtureMiss/ValidationError -> [] with status done, no warning; C2 (12 vs 9 visits)
  has no lexicon floor (plan_not_completed is strength low).
- Worker verified only its own 59 tests; full `pytest tests/unit` had 3 red test_pipeline J3 tests.
- source_kind patient_report inferred from lexicon self_report:true on intake_form_accident_date (record does not say patient wrote it).

**Why:** workers' evidence cites subset runs and tests that cannot fail; failure paths return empty instead of a visible marker.

**How to apply:** always run the FULL tests/unit, probe every flag_templates category title for banned words
(objective/subjective/failure to mitigate), and force LLMFailed/FixtureMiss on each LLM stage in the full pipeline (probe scripts in
artifacts/review-evidence/T-036-*.py). On re-review check the same four items. Related: [[lexicon-review-method]].
