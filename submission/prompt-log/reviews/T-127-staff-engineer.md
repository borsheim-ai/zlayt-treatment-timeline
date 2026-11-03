# T-127 review, round 1 - staff-engineer-reviewer

Card: keep the gap-change record on the gap flag (GET case returns `gap_change` on a gap flag whose figures moved after a confirm_date, and `gap_changes_removed[]`). Commit 93de5f2, which is HEAD at review time (`git log -1 --format=%H` prints 93de5f2e47a18f3eeff9edf8e6bc7b34fbb02dfb). I worked on `git archive 93de5f2` in scratchpad `T128_9_127_r1` (`repo/` for runs, `mut/` for mutants). Scripts are in `artifacts/review-evidence/T-128-129-127-r1/`.

**Verdict: pass.** No blocker or major. The record is stored in the `confirm_date` review event, read back by code only, and survives a fresh app on the same DB file. Two minors are test gaps; one nit is a contract omission.

## 1. Deterministic checks
- `tests/unit/test_t127_gap_change_kept.py`: 4 passed in the archive (part of the full run: 3057 collected, 3053 passed, 4 skipped, 0 failed).
- No model is called: `present.gap_change_index` is a loop over stored events; `review.py:353-359` fills `record_seq` and `sentence` from the recompute.

## 2. What I exercised on the real API (probe127.py, fixture backend, library case lib09)
- Before: `f_gap_r1_r2` 42 days, no `gap_change`. `POST .../records/r4/confirm_date {"date": "2026-03-05"}` returns `gap_changes [('f_gap_r4_r2', 'changed', 42, 40)]`. `GET case` then shows `('f_gap_r4_r2', 40, (42, 40, 4))` = old_days, new_days, record_seq, and `gap_changes_removed: []`.
- Accept, then `reset` (the undo) on the gap flag: both 200; `gap_change` still present after the reset, as api.md says ("stays through ... review actions"). `GET /items/{id}` and the review response wrap the item as `{"item": ...}` and carry the same `gap_change` sentence.
- Re-confirm of the same record: `422 invalid_edit` (a confirmed date is no longer ambiguous), no second event. There is no route that undoes a confirm_date, so there is no re-confirm path that could write a second change.
- Determinism: two GETs of the case are byte-equal (sorted JSON), and a fresh `create_app` on the same sqlite file returns the same JSON. `list_events` orders by `at, rowid` (db.py:261).
- The removed path end to end (probe127b.py, `pipeline.ingest_case` + `review.confirm_date` with no LLM, a 44-day gap split by an ambiguous 02/03/2026 record confirmed as 2026-02-03): `confirm_date` returns `removed f_gap_r1_r3`; `all_items` then lists `gap_changes_removed [('f_gap_r1_r3', 'A gap of 44 days no longer applies after you confirmed the date of record 2.')]`; the event holds `change: removed`.
- Non-gap flags carry no `gap_change` key; the contract says `gap_change: null` "otherwise", which is true only for gap flags.

## 3. Mutation of the tests (mut.py, 11 mutants of present.py/review.py against test_t127_gap_change_kept.py)
Killed (6): `record_seq` not stored; `gap_changes` not written into the event; removed list ignores current gaps; first event wins instead of latest; `gap_changes_removed` dropped from case_view; `gap_change` never set. Survived (5): drop the `days ==` check (equivalent: from/to imply days); drop both from/to checks; drop only the `new_to` check; skip `gone.pop` on re-add; skip `latest.pop` on removal. The last two do not change an observable result because the `fid not in current` and `cur ==` tests already guard them (equivalent). The from/to survivor is real: `idx.py` shows the code returns `{}` for a gap with the same 40 days but shifted dates, and the mutant would return the old change; no test sends that case.

```json
{"card": "T-127", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of 93de5f2 (HEAD) in scratchpad T128_9_127_r1; app/backend/present.py (gap_change_index, _with_gap_changes, item_view, all_items, case_view), app/backend/review.py (confirm_date, _log_confirm_date, _recompute_gaps), app/db/db.py list_events, memory/contracts/api.md:268, tests/unit/test_t127_gap_change_kept.py; fixture backend, no network",
 "exercised": [
  "python3 tools/board.py show T-127; git diff 93de5f2~1 93de5f2; read present.py, review.py:329-476, memory/contracts/api.md:262-270",
  ".venv/bin/python -m pytest tests/unit -q in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed",
  "probe127.py on the real API (fixture backend): confirm_date, GET case, accept + reset on the gap flag, GET item, re-confirm (422), second GET equality, fresh create_app on the same DB file",
  "probe127b.py: removed-gap path through pipeline.ingest_case + review.confirm_date + present.all_items (no LLM)",
  "idx.py: direct gap_change_index call with same days and shifted dates",
  "mut.py: 11 mutants of present.py/review.py against test_t127_gap_change_kept.py (6 killed, 5 survived, 4 of those equivalent)",
  "grep of callers of _recompute_gaps (review.py:354 and :579) and gap_change in app/backend"
 ],
 "verdict": "pass",
 "scores": {"stored_through_review_events": 5, "exposed_on_get_case": 5, "contract_matches_code": 4, "undo_and_reconfirm_paths": 5, "determinism": 5, "test_strength": 3},
 "findings": [
  {"severity": "minor",
   "title": "No test pins the from/to comparison in gap_change_index; removing it survives the suite",
   "evidence": "mut.py: replacing `(ch.get(\"new_from\") is None or cur.get(\"from\") == ch[\"new_from\"]) and (ch.get(\"new_to\") is None or cur.get(\"to\") == ch[\"new_to\"])` with nothing (present.py:126) -> 4 passed. idx.py: with an event new_days 40, new_from 2026-03-05, new_to 2026-04-14 and a current gap days 40 from 2026-03-10 to 2026-04-19, the code returns ({}, []); the mutant returns the stale change. The one `moved by something else` case in test_gap_change_goes_when_the_gaps_figures_move_again changes the days too (30), so the days check alone kills it.",
   "why_it_matters": "The contract says the change goes when the gap's figures differ from the ones it produced. A recompute that shifts both endpoints but keeps the length (not_duplicate calls `_recompute_gaps` at review.py:579 without recording a change) would then show 'now 40 days (was 42) after you confirmed record 4' on figures that are no longer those. It is a stale claim shown as fact.",
   "fix": "Add a case to test_gap_change_goes_when_the_gaps_figures_move_again with equal days and different from/to, asserting `changes == {}`.",
   "acceptance_test": "The mutant that removes the from/to comparison fails test_t127_gap_change_kept.py."},
  {"severity": "minor",
   "title": "The removed-gap path is tested only on hand-built events, never through confirm_date and GET case",
   "evidence": "tests/unit/test_t127_gap_change_kept.py::test_a_gap_that_no_longer_applies_is_listed_with_its_sentence_until_it_comes_back calls `present.gap_change_index` with a dict; no test drives `confirm_date` to a removal and then reads `GET /api/cases/{token}`. Mutant 'gap_changes_removed not in case_view' is killed only because test 1 asserts `== []`.",
   "why_it_matters": "I checked the path by hand (probe127b.py: 44-day gap, confirm, `gap_changes_removed` lists it with its sentence, and the event holds `change: removed`), and it works. Without a test, a later change to `_gap_changes` or the event shape could drop the removed list while every test stays green.",
   "fix": "Add the probe127b scenario as a unit test through `review.confirm_date` and `present.all_items` (no LLM needed), asserting the sentence, then confirming a second record that recreates the gap and asserting the list empties.",
   "acceptance_test": "Mutating `_log_confirm_date` to write `gap_changes: []` fails a removed-path test, not only the changed-path test."},
  {"severity": "nit",
   "title": "api.md names GET case only; GET item and the review response also carry gap_change, and non-gap flags have no key",
   "evidence": "probe127.py: `GET /items/{id}` returns {'item': ...} with gap_change sentence 'Gap recalculated after you confirmed record 4: now 40 days (was 42).'; present.py:149-157 item_view adds it for kind == 'flag' gaps; api.md:268 says 'a gap flag in `flags[]` ... otherwise `gap_change: null`' and 'Both are always present' while non-gap flags have no `gap_change` key.",
   "why_it_matters": "A frontend reading the contract would not know the item and review responses are consistent with GET case, and 'always present' is true only for gap flags.",
   "fix": "One sentence in api.md:268: 'On gap flags only; also in GET /items/{id} and the review response `item`.'",
   "acceptance_test": "grep -n 'gap_change' memory/contracts/api.md shows the item/review mention."}
 ],
 "whats_right": [
  "The change is derived, not duplicated: stored once in the confirm_date audit event (no schema change) and shown only while the gap's current figures match, so a later move cannot leave a stale claim in the common case.",
  "Deterministic and restart-safe: two GETs and a fresh app on the same sqlite file return identical JSON; accept and reset on the gap flag keep the change.",
  "The removed-gap case works end to end with its sentence, and a second confirm of the same record is refused with 422 invalid_edit without writing a second event."
 ],
 "questions_for_chris": []}
```
