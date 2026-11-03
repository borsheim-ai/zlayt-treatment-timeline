---
name: db-review-patterns
description: T-031 (app/db) round-1/round-2 review patterns - partial re-fixes, regex guard blind spots, scratch-copy mutation method, hook gotchas for reviewers
metadata:
  type: project
---

Recurring patterns from the T-031 review (app/db/db.py, tests/unit/test_db.py; reviews reviews/T-031-staff-engineer.md and -r2.md).

- **A re-fix closes the named entry point, not the write class.** Round 2 locked `update_item` (db.py:137) but left `add_item` (db.py:90-101) accepting `edited_json` with no review event. When a finding says "X can be written with no event", grep every helper that reaches the same column (`grep -rn edited_json app`), not just the one named.
- **Source-regex guard tests have blind spots.** test_review_status_only_via_apply_review matches `review_status=?`, `SET review_status`, `review_status='...'`. It misses a multi-column `SET edited_json=?, review_status=:s`, and the test still passes while its docstring says the property holds. Probe such guards with an appended rogue line in a scratch copy before accepting them as proof.
- **"Raises on no payload" was true only for the fresh item.** `(edited or before["edited"])` lets a re-edit with no payload succeed and log an event. When a fix says "raises when X", probe the state variants (fresh, already-edited).
- **Mutation method that works:** copy app/ and tests/ to the scratchpad, `sed -i.bak` one guard, run `pytest tests/unit/test_db.py -q`, restore from .bak. Do not touch repo files.

Reviewer environment gotchas (seen on this card):
- The Bash git-guard hook denies commands containing backticks inside a `python -c "..."` string ("could not parse command safely"). Put scripts in a file and run the file.
- reviewer-write-guard blocks Write to the scratchpad. Scripts and probes must go under artifacts/review-evidence/.

Related: [[project_harness_review_patterns]], [[project_design_review_patterns]].
