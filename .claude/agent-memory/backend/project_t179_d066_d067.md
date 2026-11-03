---
name: t179-d066-d067-compare-and-narrative-cut
description: T-179 backend: D-066 COMPARE_REQUIRED lives in set_review after the code checks; D-067 narrative gate is NARRATIVE_IN_LETTER; blanket-accept tests need compared:true; temp-index commit pitfalls
metadata:
  type: project
---

D-066: `review.judge_dispute(item)` (ladder.judge.verdict partially/unsupported/disagrees, amount judge says "disagree", or a JUDGE_PARTIAL/UNSUPPORTED/DISAGREES reason) + `compare_error` are enforced inside `set_review(..., compared=)` AFTER the D-051 code checks, so a failing code check stays CODE_CHECK_FAILED (test_trace d051 tests pin this). Stored as `after.compared={at}` on the accept event (`_record_compared`), shown in audit events. Batch refuses with reason `judge_disputed` (case_extras._check). `count` clears the judge so it is not disputed.

**Why:** the repo has many tests that "accept everything"; with D-066 any disputed item (lib11 amounts all carry JUDGE_DISAGREES) needs `"compared": True` in the test body. Fix the test, not the rule.

D-067: `export.narrative_in_letter()` reads `NARRATIVE_IN_LETTER=1` (normal `import os`; `__import__` trips tests/unit/test_boundaries.py). Tests of the narrative's export lines (test_narrative.py autouse fixture, test_trace d051_r3) set it via monkeypatch.

Commit pitfalls: HEAD moves under you (other workers commit present.py/api.md); rebuild the temp-index blob from the CURRENT HEAD, never from an old archive. A leftover directory named like your temp index file breaks `git read-tree` ("unable to map index file") — use a fresh filename. `rm` with `$VAR` is blocked by git-guard; use literal paths. Verification archive must be re-cut after HEAD moves.
