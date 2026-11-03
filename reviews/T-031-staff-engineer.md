# T-031 review: staff-engineer (Marcus Lee lens)

Verdict: **changes**. Behaviour the AC names mostly works: I proved ladder round-trip, delete_case, 24h purge, secure_delete, originals kept and persistence myself (artifacts/review-evidence/T-031-ac_check.py and its .out). Three gaps: `update_item` is an unlogged side door around `apply_review`, `apply_review("edit")` accepts an empty edit, and the AC-named proof tests don't exist or don't prove what the AC says.

Labels: the three majors violate an AC or spec constraint (row 20 audit, honest failure, "proved by" tests). The minors are "I would do it differently".

```json
{"card": "T-031", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 39e458a: app/db/db.py, app/db/schema.sql; tests/unit/test_db.py; no app URL (library card); sample case n/a",
 "exercised": [
  "python3 tools/board.py show T-031",
  ".venv/bin/python -m pytest tests/unit/test_db.py -q -> 9 passed in 0.09s",
  "read app/db/db.py (227 lines), schema.sql (60 lines), tests/unit/test_db.py in full",
  ".venv/bin/python artifacts/review-evidence/T-031-ac_check.py (output in T-031-ac_check.out): ladder D.4+backend round trip on a new connection, llm_calls fields, secure_delete PRAGMA on two connections, raw-file byte check after delete_case, delete_case across all tables, purge at 24h-1 / 24h / 24h+1 with injected now, purge of a case with children under FK ON, apply_review before/after events, originals kept, SQL-injection probes, bypass probes",
  ".venv/bin/python artifacts/review-evidence/T-031-mutation.py: removed llm_calls from the delete list in-process; 4 of 9 tests fail (caught, though via FK error)",
  "grep -rn 'review_status' app --include=*.py: one UPDATE writer, db.py:160 in apply_review",
  "grep -rn 'sqlite3|logging|logger|print(' app: no logging or print in app/db; sqlite3 used only in db.py:29",
  "grep for callers of purge_expired/delete_case/apply_review/update_item outside db.py: none yet"],
 "verdict": "changes",
 "scores": {"determinism_injectable_time": 4, "audit_trail_completeness": 2, "honest_failure": 3, "test_proof_of_AC": 2, "sql_safety": 5, "privacy_deletion": 5},
 "findings": [
  {"severity": "major", "title": "AC-named proof tests do not exist; the tests that do exist do not prove AC4/AC3 as written",
   "evidence": "AC2 names tests/unit/test_db.py::test_ladder_roundtrip and AC5 names test_review_status_only_via_apply_review: `grep -n 'def test_' tests/unit/test_db.py` lists neither. AC4 names test_review_status_roundtrip; the file has test_review_status_round_trip (test_db.py:~46), which uses one `conn` fixture, so it never proves 'persist across a new connection' (R-RV-8), and never checks that originals are kept after an edit. No test touches secure_delete, apply_review's events, or an edit. Worker handoff admits: 'test_ladder_roundtrip not in qa file yet'; AC2/AC5 ticked on 'adhoc' evidence.",
   "why_it_matters": "The persistence, audit and secure-delete guarantees pass only because I ran a script today. Nothing in the suite fails if `PRAGMA secure_delete`, the before/after event, or edited_json/originals regress. AC ticked 'done' with evidence that is not the proof the AC specifies.",
   "fix": "Add (in qa's file via qa, or a db-owned test file the AC is amended to name): test_ladder_roundtrip (D.4 dict + backend, read on a second connection), test_review_status_only_via_apply_review (grep/AST over app/ for writers of review_status, plus the before/after event row), test_edit_keeps_original, test_secure_delete_on, and a new-connection variant of the review-status round trip. Correct the AC test names.",
   "acceptance_test": "`.venv/bin/python -m pytest tests/unit/test_db.py -q -k 'ladder_roundtrip or only_via_apply_review or keeps_original or secure_delete or new_connection'` selects and passes >= 5 tests; turning secure_delete off in connect() makes one fail."},
  {"severity": "major", "title": "update_item is an unlogged side door: edited_json and ids can change with no review event",
   "evidence": "db.py:141-152 (update_item) refuses only 'review_status'; every other column is writable. Repro: `DB.update_item(c, i, edited_json={'summary':'SNEAKY'})` -> `get_item(...)['edited']` = {'summary': 'SNEAKY'}, `len(list_events(c,cid))` = 0. `DB.update_item(c, i, id='e999')` succeeds and the item is then fetched under 'e999'. (T-031-ac_check.py, second run in transcript.)",
   "why_it_matters": "LLM_VS_CODE row 20 / AC5: every human action logs before/after. A human edit is edited_json; any caller can change it without an event, so the audit trail can be silently wrong. Letting the id be rewritten also breaks the audit link from llm_calls.item_id and review_events.item_id.",
   "fix": "Make update_item's column allowlist exclude edited_json, id, case_id (and ideally updated_at supplied by the caller); edited text only through apply_review.",
   "acceptance_test": "pytest: update_item(..., edited_json=...) and update_item(..., id=...) each raise ValueError; edited_json changes only via apply_review and always leaves a review_events row."},
  {"severity": "major", "title": "apply_review('edit') with no edited payload sets status 'edited' with a null edit",
   "evidence": "db.py:150-153 (`new_edited = (edited if edited is not None else before['edited']) if action == 'edit'`). Repro: `DB.apply_review(c, iid2, 'edit')` on a pending item -> status='edited', edited=None, no error, an event is logged. Same path via set_review_status(conn, id, 'edited').",
   "why_it_matters": "Status 'edited' claims a human changed the wording; nothing was recorded. Downstream export/UI would show or export an empty or original text as edited. It is a silent default, not a visible failure (checklist 7/12).",
   "fix": "Raise ValueError when action == 'edit' and no edited payload exists (neither argument nor an existing edit); set_review_status('edited') must require the payload.",
   "acceptance_test": "pytest: apply_review(c, id, 'edit') on a fresh item raises ValueError, status stays 'pending', no event row."},
  {"severity": "minor", "title": "Ladder JSON is stored unvalidated; D.4 fields are convention only",
   "evidence": "`DB.update_item(c, iid, ladder_json={'garbage': 1})` is accepted (ac_check.out: 'FAIL AC2 ladder validated against D.4 keys'). AC2 says the ladder record 'holds D.4 fields plus backend'; the db layer only round-trips opaque JSON.",
   "why_it_matters": "Records missing generator/judge/model/prompt_version can be stored and later look like audit evidence. I would accept this if the Pydantic schema lives in the audited wrapper, but no test pins that.",
   "fix": "Validate ladder_json on write against the schema model (or state in the AC that validation lives in app/llm/audited and test it there).",
   "acceptance_test": "pytest: writing a ladder missing 'generator' or 'backend' raises."},
  {"severity": "minor", "title": "Timestamps silently default to 0 and get_item/update_item names are asymmetric",
   "evidence": "db.py add_item/update_item/apply_review/add_llm_call take `now: float = 0`; add_item without now stores updated_at=0.0 (verified). llm_calls ordered by created_at (db.py list_llm_calls) so forgotten `now` mis-orders attempts. get_item returns 'ladder'/'edited' but update_item rejects them: `update_item(c, iid, ladder={...})` -> ValueError unknown entries fields ['ladder'].",
   "why_it_matters": "Silent epoch-0 timestamps corrupt the audit order and 24h purge basis; the naming asymmetry will trip the next caller (read-modify-write).",
   "fix": "Make `now` a required argument (as create_case already is); accept stripped names in update_item or document and test the asymmetry.",
   "acceptance_test": "pytest: add_llm_call without now raises TypeError; get_item -> update_item round trip works."},
  {"severity": "nit", "title": "apply_review-only is enforced by convention, not by the database",
   "evidence": "A raw `UPDATE entries SET review_status='accepted'` succeeds (ac_check.out 'FAIL AC5 DB-level enforcement'). schema.sql has no trigger. Not required by the AC; mention only because the grep test the AC asks for is the sole guard.",
   "why_it_matters": "A future raw SQL line passes every unit test.",
   "fix": "Optional trigger that rejects review_status changes without a paired review_events insert, or keep the grep test and make it part of CI.",
   "acceptance_test": "grep/AST test over app/ fails when a second review_status writer is added."}
 ],
 "whats_right": [
  "All SQL is parameterized; dynamic identifiers (table, column names) come from fixed maps or are checked against PRAGMA table_info, and hostile field names and text were stored or rejected without effect.",
  "delete_case covers all 7 tables in one transaction, secure_delete is set per connection in connect(), the raw file no longer contains the case text afterwards, and purge_expired(now) is injectable with a strict boundary (24h exactly keeps the case).",
  "apply_review is the sole review_status writer (single grep hit), runs in one transaction with a before/after review_events row, and originals stay in the item columns while edits go to edited_json; no logging or print anywhere in app/db, so no record text leaks."
 ],
 "questions_for_chris": []}
```
