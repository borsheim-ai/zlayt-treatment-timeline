---
name: t061-r3-clause-span-holes
description: T-061 r3 (a27b358, D-035 clause-level patient_report): comma/and/parenthesis family clause inherits chip via ';'-bounded span; closed verb list leaks 'thinks/told'; selfcheck PASS runs a rule production no longer uses
metadata:
  type: project
---

D-035 (memory/ORCHESTRATOR_DECISIONS.md:44) replaced the lexicon speaker lists with a code rule: the patient_report span runs from
a patient-subject clause ("Patient|Pt|The patient" + reporting verb) to the next ';' or sentence end. Production
(app/backend/grounding.py:189-213) no longer reads lexicon self_report entries or self_report_scope at all.

Round 3 (r3 review, reviews/T-061-claims-adjuster-r3.md) found the holes below. Re-check these on any later round before reusing this note.
- Comma, "and" or parenthesis joins a family/EMS clause into the patient span: "Patient states pain began after the collision, wife reports
  headaches." -> chip True. The span ignores commas; the mixed check only searches text outside the span.
- Closed reporting-verb list (grounding.py:183-186): "wife thinks", "his wife told the ER" -> chip True, even with a semicolon.
- research/lexicon_selfcheck.py still uses its own is_patient_statement, so the research PASS does not test production.
- Narrowings not in D-035 text: bare "C/O" and "Patient-reported" lose the chip (pinned in test_flags_pass.py NO_TAG); lexicon.yaml:764
  still says C/O is read as the patient.

**Why:** the r2 blocker (spouse clause inside a patient-subject sentence) was closed only for the semicolon form. Each round's
phrasings pass and the class leaks elsewhere. D-033 names this as a credibility error.

**How to apply:** probe every mixed sentence by (a) separator (`;`, `,`, `and`, parenthesis, sentence split), (b) verb outside the
list, (c) speaker word outside the lexicon. Use artifacts/review-evidence/T-061-r3-probe.py (run against a git archive of the commit).
Related: [[t061-speaker-scope-closed-list]], [[review-commit-not-worktree]], [[lexicon-review-method]].
