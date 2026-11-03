# T-031 round-2 review: staff-engineer (Marcus Lee lens)

Verdict: **changes**. The three round-1 majors are each partly closed. `update_item` now refuses `edited_json`, `id`, `case_id`, `updated_at` and `review_status` (verified by script and mutation). `apply_review('edit')` with no payload raises on a fresh item (verified). The two AC-named tests now exist (`test_ladder_roundtrip`, `test_review_status_only_via_apply_review`). Three things keep this from a pass:

1. The AC5 grep guard passes when a second `review_status` writer is added in a multi-column `SET` with a named parameter (probe G1). Its docstring claims the property holds, so the test asserts something the test itself does not enforce.
2. `add_item` still accepts `edited_json` at creation and writes no review event. This is the round-1 side door, one entry point over.
3. `apply_review('edit')` with no payload on an already-edited item succeeds silently and logs an `edit` event that changes nothing.

Labels: findings 1 and 2 are "present but weak / not closed" against the T-031 AC5 and row 20 audit requirement, so major. Finding 3 is "I would do it differently", so minor. Nothing here is a §5 red flag (no float money, no LLM call, no silent fallback, no network in tests).

Scope note: no production code outside `app/db/db.py` calls `add_item`, `update_item`, `apply_review` or `set_review_status` yet (grep below), so findings 1 to 3 are latent, not reachable from the app today.

```json
{"card": "T-031", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f8d73d0 (round 2 of T-031): app/db/db.py, tests/unit/test_db.py; round-1 review reviews/T-031-staff-engineer.md; no app URL (library card); sample case n/a",
 "exercised": [
  "git show --stat f8d73d0 -> 2 files changed, 84 insertions(+), 8 deletions(-); app/db/db.py and tests/unit/test_db.py",
  ".venv/bin/python -m pytest tests/unit/test_db.py -q -> '16 passed in 0.13s' (exit 0)",
  "grep -rn 'test_ladder_roundtrip\\|test_review_status_only_via_apply_review' --include=*.py . -> tests/unit/test_db.py:77 and :123",
  "grep -n 'def test_' tests/unit/test_db.py -> 13 test functions incl. test_review_status_round_trip_new_connection:69, test_ladder_roundtrip:77, test_secure_delete_is_on:120, test_review_status_only_via_apply_review:123",
  "read tests/unit/test_db.py:60-133 and app/db/db.py:24-37, 90-101, 134-178 in full",
  "artifacts/review-evidence/T-031-r2-check.py -> artifacts/review-evidence/T-031-r2-check.out: 10/10 checks passed. update_item(edited_json=), update_item(review_status=), update_item(id=) each raise ValueError with 0 review_events and state unchanged; apply_review(iid,'edit') no payload, apply_review(iid,'edit',edited={}) and set_review_status(iid,'edited') each raise 'edit requires a non-empty edited payload' with status pending and 0 events; positive edit with payload and update_item(state=...) still work",
  "mutation in a scratch copy of app/ and tests/ (repo files untouched): M1 PRAGMA secure_delete=OFF -> test_secure_delete_is_on fails (1 failed, 15 passed); M2 edit-payload check disabled -> test_edit_without_payload_raises fails; M3 edited_json removed from locked set -> test_update_item_cannot_write_edits_status_or_ids fails; M4 restored -> 16 passed",
  "bypass probe G1 in scratch copy: appended 'UPDATE entries SET edited_json=?, review_status=:s WHERE id=:i' outside apply_review -> pytest -k only_via_apply_review: '1 passed' (guard missed it)",
  "bypass probe G2 in scratch copy: appended plain 'UPDATE entries SET review_status=? WHERE id=?' -> test fails with 'assert (2 == 1)' (guard caught it)",
  "probe add_item(..., {'summary':'orig','edited_json':{'summary':'BORN EDITED'}}) -> review_status='pending' edited={'summary': 'BORN EDITED'} events=0",
  "probe apply_review(iid,'edit',edited={'summary':'first'}) then apply_review(iid,'edit') -> accepted silently; events=2 last_action='edit' after={'edited': {'summary': 'first'}, 'review_status': 'edited'}",
  "grep -rn 'add_item(\\|update_item(\\|apply_review(\\|set_review_status(' app tests -> callers only in db.py:178 and tests/unit/test_db.py; no app/ caller outside db.py",
  "grep -rn 'edited_json' app --include=*.py -> db.py:4,137,151,155,163 only"],
 "verdict": "changes",
 "scores": {"determinism_injectable_time": 4, "audit_trail_completeness": 3, "honest_failure": 4, "test_proof_of_AC": 3, "sql_safety": 5, "privacy_deletion": 5},
 "findings": [
  {"severity": "major", "title": "AC5 grep guard passes on a rogue review_status writer in a multi-column SET",
   "evidence": "tests/unit/test_db.py:129 regex r\"review_status\\s*=\\s*\\?|SET\\s+review_status|review_status\\s*=\\s*['\\\"]\" misses 'SET edited_json=?, review_status=:s'. Repro (scratch copy, repo untouched): append `conn.execute(\"UPDATE entries SET edited_json=?, review_status=:s WHERE id=:i\", (\"{}\", \"accepted\", item_id))` to app/db/db.py, run `.venv/bin/python -m pytest tests/unit/test_db.py -q -k only_via_apply_review` -> '1 passed, 15 deselected'. Same test with a plain `UPDATE entries SET review_status=? WHERE id=?` appended -> 'assert (2 == 1)', 1 failed.",
   "why_it_matters": "AC5 says only the events helper writes review_status and names this test as the proof. The test's own docstring ('the only statement that SETs review_status is inside apply_review') is false under the bypass, and the test still passes. A future line in the common multi-column form would change review_status with no review_events row, which is the audit gap row 20 forbids, and nothing would fail.",
   "fix": "Replace the regex with an AST or SQL-aware check: collect every string literal in app/ that contains UPDATE/INSERT ... review_status (any position in SET list, named or positional params) and every assignment to a key 'review_status' in dict literals passed to execute; assert the only hit is inside apply_review. Keep the existing string check as well.",
   "acceptance_test": "pytest: a test that copies db.py, appends the two rogue forms above (plain and multi-column, named and positional), and asserts each one fails the guard; the unmodified tree passes. Quoted in the test file so the guard cannot silently weaken."},
  {"severity": "major", "title": "add_item still accepts edited_json and writes an edit with no review event (round-1 side door, one entry point over)",
   "evidence": "app/db/db.py:90-101: add_item rejects only the 'review_status' key (line 96-97); `_insert` accepts any column, so 'edited_json' passes. Repro: add_item(c, cid, 'entry', {'summary':'orig','edited_json':{'summary':'BORN EDITED'}}) -> review_status='pending', edited={'summary': 'BORN EDITED'}, list_events(...) = 0 (probe output above). The round-2 fix closed update_item only (db.py:137 locked set).",
   "why_it_matters": "Round-1 major 2 was 'edited_json can change with no review event'. It is still true at creation: an item can be born carrying a human-style edit with no before/after row. No app/ caller does this today (grep above), so the exposure is latent, but the audit guarantee in AC5 and row 20 is only as strong as the weakest writer, and this one is open.",
   "fix": "Reject 'edited_json' (and 'id' if caller-chosen ids are not wanted) in add_item's payload, the same way review_status is rejected. Creation of an edit goes through apply_review only.",
   "acceptance_test": "pytest: add_item(conn, cid, 'entry', {'edited_json': {...}}) raises ValueError and inserts no row; add_item(... {'review_status': 'accepted'}) still raises; get_item after a normal add_item returns edited None."},
  {"severity": "minor", "title": "apply_review('edit') with no payload on an already-edited item succeeds and logs a no-op 'edit' event",
   "evidence": "app/db/db.py:157 `new_edited = (edited or before[\"edited\"]) if action == \"edit\" ...` and db.py:158 `if action == \"edit\" and not new_edited:` only raises when no prior edit exists. Probe: apply_review(iid,'edit',edited={'summary':'first'}) then apply_review(iid,'edit') -> accepted; review_events=2; last action='edit', after={'edited': {'summary': 'first'}, 'review_status': 'edited'}.",
   "why_it_matters": "The round-2 claim is 'apply_review(edit) with no payload raises'. That holds for a fresh item only. On a re-edit the audit trail records a human 'edit' that carried no new text, which reads as a change when none happened. Honest failure says it should raise.",
   "fix": "Require a non-empty `edited` argument for action 'edit' regardless of prior state; `(edited or before)` should not be used for 'edit'.",
   "acceptance_test": "pytest: edit once with payload, then apply_review(iid,'edit') raises ValueError and the event count stays at 1."},
  {"severity": "minor", "title": "Carry-over from round 1: ladder JSON unvalidated; timestamps default to 0; update_item/get_item name asymmetry",
   "evidence": "app/db/db.py:90 add_item, :134 update_item, :149 apply_review, :188 add_llm_call all take `now: float = 0`; the round-2 commit message and card state these defaults are unchanged. Ladder validation still lives in the audited wrapper, not pinned by a test here.",
   "why_it_matters": "Silent epoch-0 timestamps corrupt the audit order (llm_calls ordered by created_at) and the 24h purge basis. Records missing D.4 keys can be stored as audit evidence if the wrapper is bypassed.",
   "fix": "Make `now` required on these four helpers (create_case already is); test that add_llm_call without now raises TypeError. Pin ladder validation in app/llm/audited with a test, or validate on write here.",
   "acceptance_test": "pytest: add_llm_call(...) without now raises TypeError; a ladder missing 'generator' is rejected at the layer that owns it."}
 ],
 "whats_right": [
  "update_item's locked set (db.py:137) now blocks edited_json, edited, id, case_id, updated_at and review_status; mutation M3 proves test_update_item_cannot_write_edits_status_or_ids pins it.",
  "The two AC-named tests exist and pass (test_db.py:77 and :123); test_review_status_round_trip_new_connection (:69) proves persistence on a second connection, and mutation M1 proves the secure_delete test fails when the PRAGMA is off.",
  "apply_review's edit check runs before BEGIN and before any write, so a refused edit leaves status pending and no event row (probe: 0 events, status pending)."
 ],
 "questions_for_chris": []}
```
