---
name: lexicon-review-method
description: How to review flag lexicons/phrase lists as the adjuster — self-check PASS on author examples hides recall gaps; probe off-sample phrasing, comma-scoped negation, intake checkboxes
metadata:
  type: feedback
---

A lexicon self-check that replays only the author's own examples + the 9 sample records will PASS while recall on real
adjuster phrasing is near zero (T-009 round 0: selfcheck PASS, my 63 probes OK=10 FN=38 FP=15).

**Why:** the second signal exists to catch what the LLM overlooks; testing it on the sample alone proves nothing.

**How to apply:** for any lexicon/flag change, re-run artifacts/review-evidence/T-009-adjuster-probes.py (import the repo
guard, never modify the repo; reviewer hook blocks writes outside reviews/ and artifacts/review-evidence/ — even scratchpad).
Always probe: (1) evals/golden/case_06_subtle_pre_existing records; (2) "No acute fracture, chronic degenerative changes"
(comma-scope negation); (3) intake checkboxes "Prior injuries: No."; (4) ROS denial lists >6 tokens; (5) "did not present
with"; (6) MIST/scene facts and "out of proportion". Also check flag_type names vs REQUIREMENTS/golden types (hedge category,
compliance→causation mapping). See [[research-attack-map-gaps]].
(7) For any exclusion regex (self_report_scope.exclude_sentence, T-061 r0): patient-subject sentences that contain a
family/EMS/witness word and a speech verb ("Patient states EMS noted a laceration."). A regex that matches a non-patient
name anywhere in the sentence passes every "exclude" example and still drops the patient's own statement.
(8) A lexicon change is not a product change: diff the commit for app/backend and run the parent-vs-HEAD FAILED list (T-061 r0:
selfcheck PASS, but the flag test went red and production still used the old word filter). See [[project-flag-source-kind-and-run-signal]].
