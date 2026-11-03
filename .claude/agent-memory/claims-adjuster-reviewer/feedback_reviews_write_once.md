---
name: reviews-write-once
description: reviewer-write-guard makes reviews/<card>-<persona>.md append-only once written; get line citations and JSON right before the first write
metadata:
  type: feedback
---

The reviewer-write-guard hook blocks Edit on an existing file under reviews/ ("reviews are append-only — write a new file (e.g. -r2/-r3 suffix)").
On T-061 r3 I wrote the review, then found three wrong test line citations, and could not correct them in place.

**Why:** the guard enforces append-only history for review rounds, so a round file is final once written.

**How to apply:** before the first Write of a review file, grep every cited file:line and check it (use grep -n, not memory). Parse the
JSON block and check the verdict rule. Do not work around the guard with a shell write; if a citation is off after writing, say so in
the reply to the orchestrator and give the corrected line numbers.

Related: [[project_t061_r3_clause_span_holes]].
