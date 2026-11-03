# T-057 review, round 3: re-run record consistency after a failed or rejected re-split, staff-engineer-reviewer

Commit under review: 8bf99fb (pinned by `git archive` into artifacts/review-evidence/T-057-staff-engineer-r3/tree). HEAD at review time was b614b40, which contains 8bf99fb. The live working tree is dirty (145+ modified files, including app/backend/narrative.py and tests/fixtures), so the pinned tree is the control.

Verdict: **fail**. The round-2 blocker is closed for items that have not been decided. A new blocker on the same clause is open: items the paralegal already accepted are orphaned when a re-run replaces the stored records, on both the failed-split path and the successful-split path.

## Round-2 blocker: closed for pending items

- The probe prints `run2 stored [('r1', 0, 128)]`, `entry e1 record ['r1'] stored span (0, 128) ... True`, and `consistent`.
- The new tests `test_rerun_whose_split_fails_or_is_rejected_leaves_records_and_entries_consistent[call_fails|invalid_spans]` pass. The `ValueError` narrowing has its own test and passes.
- Mutant "remove record replacement" (`return` at the top of `_store_records`): 5 failed, 24 passed. The two new tests fail, as do the existing replace tests and the split audit test.
- Mutant "keep whatever is stored" (the round-2 behaviour, condition changed to `if stored:`): 4 failed, 25 passed. The probe prints `INCONSISTENT`.

## Round-3 blocker: accepted items orphaned by a re-run

The new tests only use pending entries, because each test runs the pipeline and never accepts anything. Run 2 deletes pending rows only (`_persist`, pipeline.py:169-174), so accepted entries from run 1 survive with the record ids of run 1. Those ids no longer exist in the records table after run 2.

- Failed re-split (`probe_accepted_orphan.py`): run 1 stored r1, r2, r3 and entries e1 to e3 were accepted. After run 2 the records table is `[('r1', 0, 128)]`, and the entries are `e1 ['r1'] accepted`, `e2 ['r2'] accepted`, `e3 ['r3'] accepted`. The probe reports `ORPHANED accepted entries ... ['e2', 'e3']`.
- Successful re-split with different boundaries (`probe_accepted_orphan_success.py`): run 2 stores `[('r1', 0, 85), ('r2', 86, 128)]`, and accepted `e3 ['r3']` is orphaned.
- Consequences I checked in code (pinned tree):
  - `app/backend/present.py:170-177` (`why_view`): `if rid in recs` silently drops the missing record, so the "why" panel for an accepted item shows `source: []` with no warning.
  - `app/backend/export_routes.py:38`: the export writes the dangling `record_ids` (fallback `r{record_no}`) for each entry.
  - `app/backend/api.py:348-354`: a re-run on a case with decided items is allowed when the client sends `confirm_rerun: true`. The path is reachable through the UI and API.
- Severity: rated **blocker** under CONTRACT D.2 "loses facts". The provenance of an accepted, exported item is lost, and it is lost silently. The round-2 acceptance criterion also requires that a failed re-split leave records and entries consistent, and it does not. A reviewer could argue for major because the excerpts are still verbatim input text. I did not downgrade it, because the link to the source record is what the paralegal verified against.

## Findings for the worker

1. blocker: accepted items from an earlier run are orphaned when the records are replaced, on both the failed and successful re-split paths. Fix options, pick one and state it in the handoff:
   a. Refuse the record replacement while any entry is decided and return 409 with a reason code, or
   b. Re-anchor decided items to the new record that contains their excerpt (verbatim substring check) and mark the item `needs_review` when no such record exists, or
   c. Keep the first accepted split and do not re-ask the model on a re-run that has decided items.
   Whichever is chosen, a test must cover a case with accepted items.
2. minor: the new round-3 tests do not cover accepted or edited items, so they pass while finding 1 is present. Add the accepted-item variant to `tests/unit/test_split_llm.py` (acceptance test below).

Acceptance test (for finding 1 and 2): accept every entry of run 1 (`DB.apply_review(conn, id, "accept", ...)`), then run 2 with (a) a failing split and (b) a successful split with different boundaries. After each run: every entry's `record_ids` resolve to a row in `records`, `excerpt in raw[char_start:char_end]` of that record, or the run refuses with a reason code. `probe_accepted_orphan.py` and `probe_accepted_orphan_success.py` must print no orphans.

## Commands and results

- `python3 -m pytest -q tests/unit/test_split_llm.py`: **not runnable**. System python3.12 has no pytest (`No module named pytest`). The venv was used instead.
- `.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider` in the pinned 8bf99fb tree: 29 passed in 0.52s.
- Same command in the live dirty working tree: 29 passed in 0.51s (not a clean control).
- Probe `artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py` on the pinned tree: `consistent`, exit 0.
- Mutant `artifacts/review-evidence/T-057-staff-engineer-r3/mut-no-replace` (record replacement removed): 5 failed, 24 passed.
- Mutant `artifacts/review-evidence/T-057-staff-engineer-r3/mut-keep-if-any`: 4 failed, 25 passed; probe prints `INCONSISTENT`.
- Grep: `grep -n "except" app/backend/pipeline.py` in the pinned tree shows the `_store_records` `except Exception: ROLLBACK; raise`, which re-raises. It is not a swallowed exception. No `float(`, `sleep(` in the changed files.

## Not exercised

Frontend rendering of the why panel and the export file (I read the code path, I did not click it). Live backend. `python -m app.pipeline evals/golden/sample.txt` (not in this card's brief). The 3-run live eval.

## Model note

This review was run as claude-haiku-5-5. The dossier expects claude-sonnet-5-5. The record below uses the model I ran as.

```json
{
 "card": "T-057",
 "persona": "staff-engineer-reviewer",
 "model": "claude-haiku-5-5",
 "scope": "commit 8bf99fb pinned; re-run record consistency after failed/rejected/successful re-split",
 "exercised": [
  "probe_rerun_fail2.py",
  "probe_accepted_orphan.py",
  "probe_accepted_orphan_success.py",
  "mutants mut-no-replace and mut-keep-if-any",
  "venv pytest tests/unit/test_split_llm.py (29 passed)"
 ],
 "verdict": "fail",
 "scores": {
  "round-2 blocker (pending items)": 4,
  "accepted-item provenance": 1
 },
 "findings": [
  {
   "severity": "blocker",
   "title": "Accepted items from an earlier run are orphaned when a re-run replaces the stored records (failed and successful re-split paths)",
   "evidence": "probe_accepted_orphan.py: ORPHANED accepted entries ['e2','e3']; probe_accepted_orphan_success.py: e3 ['r3'] orphaned; present.py:170-177 drops missing record silently; export_routes.py:38 writes dangling record_ids; api.py:348-354 allows re-run with confirm_rerun",
   "why_it_matters": "Provenance of an accepted, exported item is lost silently (D.2 loses facts).",
   "fix": "Refuse replacement while any entry is decided (409), or re-anchor decided items, or keep the first accepted split on re-run.",
   "acceptance_test": "Accept all run-1 entries, re-run with failing and with differently-bounded split; every entry's record_ids resolve and excerpt is in its record, or the run refuses with a reason code; both probes print no orphans."
  },
  {
   "severity": "minor",
   "title": "Round-3 tests cover only pending items",
   "evidence": "tests/unit/test_split_llm.py never accepts an entry before re-run",
   "why_it_matters": "Tests pass while the blocker is present.",
   "fix": "Add the accepted-item variant.",
   "acceptance_test": "As above."
  }
 ],
 "whats_right": [
  "Round-2 blocker closed for pending items; both mutants caught",
  "ValueError narrowed with its own test"
 ],
 "questions_for_chris": []
}
```


> Orchestrator note: the reviewer filled the JSON block with placeholders after misreading a redaction rule; the orchestrator rebuilt it from the prose above without changing any finding or verdict.
