---
name: wiring-review-patterns
description: T-030 r2 pattern: a round fix passes its unit tests at the function/table level but the producer path never calls it. Check callers and run the producer, not just pytest.
metadata:
  type: project
---

Recurring pattern (T-030 r2, 2026-11-01): the round-1 major "compose_state ignores endpoint_unverified" was fixed in the
boolean table (confidence.py:64) and tested there, and `check_amount` was added with tests. But the only producer of
ENDPOINT_NOT_VERIFIED (app/backend/gaps.py:37) never calls compose_state, and gap flags carry reasons with no `state` key.
`check_amount` had no production caller at all. Pytest was green on both, so the green summary hid the gap.

**Why:** a fix that is green only in its own unit test does not close the risk the original finding named (the gap flag
path). Same family as T-031 partial re-fixes (sibling writers), see [[project_db_review_patterns]].

**How to apply:**
- For every function or table row a round adds or changes, grep non-test callers (`grep -rn name --include=*.py . | grep -v tests/`).
  Zero production hits = not wired, regardless of pytest.
- Run the producer on a repro (e.g. gaps.gap_flags on synthetic records) and check the output shape, not only the unit tests.
- Scratch-copy mutation of the function (return []) and of the table row shows whether the tests are load-bearing; it does not
  show whether production reaches them.

Also: the dossier names claude-sonnet-5-5 as the expected model id, but the r2 run was executing as claude-haiku-5-5. Record
the model that actually ran in the JSON, and note the mismatch in the reply.
