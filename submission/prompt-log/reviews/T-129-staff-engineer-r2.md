# T-129 review, round 2 - staff-engineer-reviewer

Card: a non-library preamble must not become record 1; round 2 asks that GET case serves `unsplit` / `preamble` (matching api.md) and that a re-run after the numbering changed leaves no decided item on a shifted record number. Commit 1f0a164. I worked on a `git archive` of 2790918 in my scratchpad (`T128_9_r2b/repo`, with `m4/repo` as a mutation copy); `git diff 2790918 HEAD --stat -- app tests/unit memory/contracts` is empty at the end of the review (HEAD 5dfba88), so the code is HEAD's. Scripts are in `artifacts/review-evidence/T-128-129-r2/` (`t129_r2.py`, `mut_t129_r2.py`).

**Verdict: pass.** Both round-1 findings are fixed and verified through the real routes and the real re-ingest path. Two minors remain (tests narrower than the code; one ordering nit), neither changes behaviour today.

## 1. Deterministic checks
- `tests/unit` in the 2790918 archive: 3214 passed, 4 skipped, 0 failed. The three new tests in `tests/unit/test_ingest.py` pass.

## 2. GET case serves the fields (t129_r2.py part A, FastAPI TestClient on the real app, loopback peer)
`POST /api/cases` and `GET /api/cases/{token}` for three pastes return identical `(id, unsplit, preamble)` per record:
- cover sheet above two records: `[('r1', False, False), ('r2', False, False), ('r3', True, True)]` on both.
- two records only: `[('r1', False, False), ('r2', False, False)]`.
- a free note between two records: `[... ('r3', True, False)]`.
GET `warnings` is `[]` and POST has `UNSPLIT_TEXT`, which is what api.md now says (the warning is POST-only). The fields are in both api.md examples (memory/contracts/api.md, the POST and GET record examples) and the text at the `UNSPLIT_TEXT` warning code names both responses. `grep -rn "unsplit\|preamble" app/frontend` still prints nothing, so no label is shown yet; the handoff lists that as left, and it is a frontend card, not this one.

## 3. Re-run after the numbering changed (t129_r2.py part B, same sqlite file, ingest_case twice)
Stored under the old numbering (a dated cover as r1, visits r2 and r3), then I accepted the gap `f_gap_r1_r2`, accepted amount `a1` ($6,240, then on r2) and dismissed `a2` ($185). Re-ingest of the same paste with an undated cover sheet on top:
- records after: `r1 2026-01-09, r2 2026-03-20, r3 None`.
- every item that cites a record whose span changed is back to `pending`; `decided items left after shift: []`. Events keep the history: `a1 accept, a2 dismiss, f_gap_r1_r2 accept, a1 reset, a2 reset, f_gap_r1_r2 reset`.
- the stale `f_gap_r2_r3` row is gone, `f_date_r3` is new and pending.
So no accepted or dismissed item (flag or amount) points at a shifted number. The unit test covers only the flag; see finding 1.

## 4. Mutation of the tests (mut_t129_r2.py: 14 mutants of pipeline.py / present.py against test_ingest.py + test_api_routes.py + test_pipeline.py)
Killed (9): marks never stored; `unsplit` always False; `preamble` always False; `_recs_by_id` never sets preamble; reset is a no-op; moved set limited to vanished ids; no `computed.record_ids` fallback; `ingest_case` passes no `now`; marks early-return inverted.
Survived (5): reset only flags; reset skips amounts; reset only accepted items (dismissed and edited stay bound to the old number); no evidence-record fallback; `run_pipeline` passes the default `now` to `_store_records` (reset events then carry time 0.0).

```json
{"card": "T-129", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of 2790918 (HEAD 5dfba88, app/tests/contract identical) in scratchpad T128_9_r2b and m4; app/backend/pipeline.py _store_record_marks/_reset_reviewed_on/_store_records/_persist, app/backend/present.py _recs_by_id/record_view, tests/unit/test_ingest.py, memory/contracts/api.md; fixture/no model call, no network",
 "exercised": [
  "python3 tools/board.py show T-129; read reviews/T-129-staff-engineer.md; git show 1f0a164 (pipeline.py, present.py, api.md, test_ingest.py)",
  ".venv/bin/python -m pytest tests/unit -q in the 2790918 archive: 3214 passed, 4 skipped, 0 failed",
  "t129_r2.py part A: FastAPI TestClient on create_app (loopback peer), POST /api/cases then GET /api/cases/{token} for a cover-sheet paste, a plain paste and a mid-note paste; compared record fields and warnings",
  "t129_r2.py part B: case stored under the old numbering, gap accepted, amount accepted, amount dismissed, re-ingested on the same sqlite file with the cover sheet on top; listed item statuses, cited records and the event log",
  "mut_t129_r2.py: 14 mutants of pipeline.py / present.py against test_ingest.py, test_api_routes.py, test_pipeline.py (9 killed, 5 survived)",
  "grep of app/frontend for unsplit / preamble; read pipeline.py _store_records lines 150-215 including the BEGIN/COMMIT block and _persist"
 ],
 "verdict": "pass",
 "scores": {"numbering_stability": 5, "nothing_dropped_D027": 5, "api_exposes_preamble": 4, "contract_matches_code": 5, "test_strength": 3, "upgrade_safety": 4},
 "findings": [
  {"severity": "minor",
   "title": "The reset on a shifted record number is pinned for accepted flags only; amounts, entries, dismissed and edited decisions and the run_pipeline path have no test",
   "evidence": "`.venv/bin/python -I artifacts/review-evidence/T-128-129-r2/mut_t129_r2.py <archive>`: 'reset flags only' (pipeline.py _reset_reviewed_on `for kind in (\"entry\", \"amount\", \"flag\")` -> `(\"flag\",)`), 'reset amounts skipped', 'reset accepted only' (`it[\"review_status\"] != \"pending\"` -> `== \"accepted\"`), 'no evidence fallback' (_item_record_ids) and 'run_pipeline passes now=0.0' each leave 123 tests passed. tests/unit/test_ingest.py test_a_rerun_after_the_numbering_changed_resets_decisions_made_on_shifted_records accepts one gap flag and asserts flags only.",
   "why_it_matters": "The code is right today (part B shows an accepted amount and a dismissed amount reset), but an accepted amount or an edited entry bound to the wrong record is the export-relevant case and the one a later edit to this helper would break unnoticed. The card AC and the orchestrator's note name the accepted flag, which is why this is minor and not major.",
   "fix": "Extend the test: accept a gap flag, accept an amount and dismiss another, re-ingest with the cover on top, assert all three are pending and that the event log has the reset; add one run_pipeline-path assertion that the reset event has a non-zero timestamp.",
   "acceptance_test": "The five mutants above print KILLED in mut_t129_r2.py."},
  {"severity": "nit",
   "title": "_reset_reviewed_on commits its resets before the records transaction begins",
   "evidence": "app/backend/pipeline.py _store_records: `_reset_reviewed_on(conn, cid, {...}, now)` runs before `conn.execute(\"BEGIN\")`; if the DELETE/INSERT block raises and rolls back, the decisions were already reset while the records stay on the old numbering.",
   "why_it_matters": "Fails in the safe direction (items pending, exception propagates, event log intact) and needs a DB error to trigger, so it is only an ordering note.",
   "fix": "Move the reset inside the same transaction, or comment that reset-then-fail is intended.",
   "acceptance_test": "none needed"}
 ],
 "whats_right": [
  "GET case and POST case serve the same unsplit and preamble per record, and api.md names which response carries the UNSPLIT_TEXT warning (POST only).",
  "A re-ingest after the numbering changed resets every decided item that cites a moved record (flags and amounts), keeps the events, removes the stale row, and leaves an unchanged case alone (same-numbering test).",
  "Marks are stored in cases.config_json with no schema change and refreshed before the early return, so a model split that moves records updates them too (the inverted-early-return mutant is killed)."
 ],
 "questions_for_chris": []}
```
