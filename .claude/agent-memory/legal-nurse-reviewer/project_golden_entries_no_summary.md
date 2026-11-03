---
name: golden-entries-lack-summary-requirements
description: T-015 golden required_terms are scored on summary+excerpt, so summary omissions (LOC qualifier, hedge, patient states) still pass; recheck on re-review
metadata:
  type: project
---

Round 1 (commit 47520a8): entries had no summary requirements. Round 2 (commit 3c5eb7c, 2026-11-01) added `required_terms` and `source_kind`, but the README scores required_terms on **summary+excerpt**. The excerpt already contains each term, so a summary that drops "without loss of consciousness", "may represent" or "patient states" still passes. R-TL-4 (judge #1) checks additions only, never omissions. Still a major in round 2. source_kind=patient_self_report is entry-level and covers exam findings and Dx (case_08 E1 tenderness, case_06 E3 ROM). Also a major.

**Why:** Omission of a qualifier is a persona dealbreaker. Fields that look like a fix can be satisfied by the excerpt alone.

**How to apply:** On any T-015/evals re-review, probe required_terms with a summary-only omission (script: artifacts/review-evidence/T-015-r2-nurse-probe.py). Check whether a summary-only field exists. Related: [[probe-must-not-regexes]]
