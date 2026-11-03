# T-159 staff-engineer review, round 2 (confirm and its event in one transaction)

Reviewed commit c0e2b86 on a `git archive` copy taken at that commit. HEAD later moved to 67be38d; `git diff c0e2b86 HEAD --stat` for app/backend/{review,trace,pipeline,flags}.py, app/db and tests/unit/test_t159_flag_audit.py is empty, so none of this card's files changed.

Verdict: **pass**. No blocker, no major. The round-1 minor (three autocommit statements) is fixed for a single fault, and both surviving mutants now die. Two minors remain: the take-back is best-effort, not atomic (a double fault leaves a flagged charge accepted, counted and exported without its confirm), and the dismissed-prior take-back is unpinned. AC1 is T-163's and is not judged here.

Is the compensation safe? For a single failure, yes. `_record_confirm` (review.py:218-235) now writes the item confirm and the event confirm inside one BEGIN/COMMIT/ROLLBACK, so a failure on either leaves neither. `set_review` (review.py:259-267) then takes the accept back with a `reset` (prior pending) or `dismiss` (prior dismissed) and re-raises, so the caller sees a 500 and the trail shows accept then reset. Amounts have no edit action, so those two priors are the only ones. It is not safe against a second fault (finding 1), because the accept is committed by `DB.apply_review` before the confirm write starts and only then taken back. The worker says so in the handoff.

What I exercised (archive copy of c0e2b86, `.venv/bin/python`):
- `pytest tests/unit -q`: 4880 passed, 8 skipped (281 s).
- Probes (TestClient, `make_env` and the `promoted` fixture from test_t159_flag_audit.py):
  - prior pending, event write fails: pending again, no confirmed_at, totals unchanged, bare accept 422, retry with confirm works, one `reset` in /audit (the card's own test, re-run).
  - prior dismissed, event write fails: item ends `dismissed`, confirmed_at None. Correct.
  - item write (`DB.update_item`) raises inside the transaction: item pending, events show reclassify, accept, reset; no confirm anywhere.
  - compensation itself fails (the second `DB.apply_review` call raises, after the event write failed): 500; item stays `accepted`, confirmed_at None, `totals.accepted` 15000 count 1; bare accept then 422 CONFIRM_REQUIRED; trace `charge_flag` pending with next_action CONFIRM_FLAG; after accepting the entries, GET /export returns 200 and the letter lists `$150.00` for the flagged duplicate.
  - prior accepted with the confirm's timestamp stripped, event write fails: stays accepted, unconfirmed, counted (the state before this card, unchanged).
- Mutants of app/backend/review.py against test_t159_flag_audit.py + test_amounts_d059_api.py (27 tests): ASC order on the newest accept event: killed. Drop the `confirmed_at` clause: killed. Real no-transaction (BEGIN, COMMIT, ROLLBACK replaced by `pass`): killed. ROLLBACK replaced by COMMIT: killed. No compensation: killed. Swallow the failure (return instead of raise): killed. Compensation always `reset` regardless of prior status: survived (finding 2).
- Read `git show c0e2b86` for review.py, trace.py and the new tests in full.

Labels: finding 1 is a robustness gap against a spec constraint (D-059) that needs two faults; I rate it minor because the single-fault path is closed and the fix is cheap, not because the fix is inconvenient. Finding 2 is a missing test.

```json
{"card": "T-159", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit c0e2b86 (app/backend/review.py, trace.py, tests/unit/test_t159_flag_audit.py) in a git archive copy; HEAD later 67be38d with none of these files changed; synthetic NOTE from test_amounts_d059_api.py; no app server",
 "exercised": ["python3 tools/board.py show T-159 and T-161; read reviews/T-159-staff-engineer.md", "git archive c0e2b86 copy: pytest tests/unit -q -> 4880 passed, 8 skipped", "git show c0e2b86 (review.py, trace.py, tests) in full; git diff c0e2b86 HEAD --stat on this card's files: empty", "TestClient probes: prior pending, prior dismissed, item-write failure, compensation failure (export 200 and trace), prior accepted without confirmed_at", "7 mutants of review.py against test_t159_flag_audit.py + test_amounts_d059_api.py: 6 killed, 1 survived (always-reset compensation)", "grep of callers of set_review and _record_confirm; read db.apply_review and update_item for transaction handling"],
 "verdict": "pass",
 "scores": {"atomic_confirm_write": 4, "compensation_safety": 3, "mutant_kills": 4, "failure_visibility": 5, "trace_confirm": 5},
 "findings": [
  {"severity": "minor", "title": "The take-back is best-effort: if it fails, or the process dies between the two commits, a flagged charge stays accepted, counted and exported without its confirm",
   "evidence": "app/backend/review.py:257 DB.apply_review commits the accept; review.py:261-267 _record_confirm then the take-back, each a separate transaction. Repro (archive, promoted fixture): event write raises (json.loads patched) and the second DB.apply_review call raises -> POST accept confirm=likely_duplicate returns 500; GET case shows review_status accepted, flag.confirmed_at None, totals.accepted {'cents': 15000, 'count': 1}; trace charge_flag status pending with next_action CONFIRM_FLAG; after accepting the entries GET /export returns 200 and letter_text contains 'Brindlewood Physical Therapy, visit note, June 1, 2026: $150.00' for the likely_duplicate charge. A bare accept then returns 422 CONFIRM_REQUIRED, so a retry repairs it.",
   "why_it_matters": "D-059 says a flagged charge is not counted unless confirmed by name. Under a double fault, or a kill between the two commits, the invariant holds only until someone retries; meanwhile totals and the letter carry the duplicate. The 500 is visible, but the state that follows is not flagged at export time.",
   "fix": "Either give DB.apply_review an optional extra for after_json and the item ladder so status, item confirm and event are one transaction (db owner), or make the export gate and totals refuse an accepted charge whose ladder.confirm has no confirmed_at (trace.py already shows it as pending CONFIRM_FLAG, so the read side knows).",
   "acceptance_test": "Inject the double fault as above: either the charge is pending/dismissed afterwards, or GET /export returns 422 with a CONFIRM_FLAG blocker naming the charge until it is confirmed or dismissed."},
  {"severity": "minor", "title": "Mutant survives: the take-back of a previously dismissed charge always resets instead of dismissing",
   "evidence": "replace the dict at review.py:263 {\"pending\": \"reset\", \"dismissed\": \"dismiss\"}.get(item.get(\"review_status\")) with \"reset\" -> 27 passed (test_t159_flag_audit.py + test_amounts_d059_api.py). tests/unit/test_t159_flag_audit.py:133 test_a_failure_writing_the_confirm_leaves_no_half_confirmed_charge starts only from pending. My probe of the dismissed prior ends 'dismissed', so the code is right; no test pins it.",
   "why_it_matters": "A dismissed charge whose accept fails would reappear as pending under that regression, undoing the paralegal's earlier decision without a word.",
   "fix": "Add a variant of the failure-injection test that dismisses the charge first and asserts review_status == 'dismissed' after the 500.",
   "acceptance_test": "The always-reset mutant fails that test; HEAD passes it."},
  {"severity": "nit", "title": "The take-back's own failure is not caught, so the caller sees only the second exception",
   "evidence": "review.py:263-266: DB.apply_review(conn, item_id, back, ...) inside the except block is not guarded; if it raises, the original exception survives only as __context__ and nothing logs that the accept was left standing.",
   "why_it_matters": "A person debugging the 500 sees the take-back error, not that a counted charge remains.",
   "fix": "Wrap the take-back, log both errors with the item id, and re-raise the original.",
   "acceptance_test": "Compensation-failure probe: the log line names the item and says the accept stands."}
 ],
 "whats_right": ["the item confirm and the event confirm share one BEGIN/COMMIT with ROLLBACK on error; the real no-transaction mutant and the ROLLBACK-to-COMMIT mutant are both killed", "both round-1 survivors (newest-event ordering, confirmed_at required for the no-op) now die, with tests that assert behaviour (event confirm values, 422 on the stripped state)", "failures stay loud: every injected fault returns 500, the taken-back accept shows up as an accept then reset in /audit, and a retry with the confirm works"],
 "questions_for_chris": []}
```
