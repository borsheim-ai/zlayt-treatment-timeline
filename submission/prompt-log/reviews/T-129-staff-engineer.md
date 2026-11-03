# T-129 review, round 1 - staff-engineer-reviewer

Card: a non-library preamble must not become record 1 (reviews/T-123-paralegal.md minor; D-027: nothing is dropped). Commit 3a74f75; HEAD at review time is 93de5f2 (`git diff 3a74f75 HEAD --stat -- app/backend/ingest.py` is empty). I worked on `git archive 93de5f2` (`repo/`) and on `git archive 3a74f75~1` (`parent/`) in scratchpad `T128_9_127_r1`. Scripts are in `artifacts/review-evidence/T-128-129-127-r1/`.

**Verdict: changes.** One major, one minor. Numbering is stable and nothing is dropped, and all 5 ingest mutants I ran are killed. But the contract line that says the preamble "has `preamble: true`" is not true of what the API serves, so the card's second option ("shown as a preamble") is unreachable and the preamble is still counted and displayed as an unlabelled record 3.

## 1. Deterministic checks
- `tests/unit/test_ingest.py` is part of the full unit run in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed.
- Old/new comparison over every `.txt` input under evals/, tests/, spec/, app/ (27 files, `cmp_ingest.py` loads the parent and HEAD `ingest.py` side by side): record numbers, sources and `unsplit` flags are identical for all 27. Golden and library packets and `unsplit_paste.txt` do not shift. The recorded-fixture suite passes, so no recorded call is keyed to a moved number.
- Record numbering of the 9 shapes in `ab.py` (HEAD vs parent): with a preamble above (`---` separated, blank-line separated, no separator, `=== Record N ===` style, "Re: Date:" text, two preambles), real records are r1, r2 and the preamble(s) are r3 (r4), `unsplit: true`, `preamble: true`. A note between records and trailing text are numbered after the real records, `preamble: false`. Parent numbered the preamble r1 in all of those. `ov129.py`: no overlapping record spans in 6 shapes.

## 2. What the API serves (api129.py, via `pipeline.ingest_case` and `present.record_view`)
`record_view` keys: char_end, char_start, date_candidates, date_iso, date_raw, date_status, duplicate_of, encounter, id, injection_tag, language, seq, source_label, text. No `unsplit`, no `preamble`. HEAD: `('r3', 3, 0, None, None, 'FAX COVER SHEET|To')` (unsplit and preamble print None). `GET /api/cases/{token}` returns `"warnings": []` (present.py case_view), so `UNSPLIT_TEXT` is only in the POST response. `grep -n "UNSPLIT\|unsplit\|preamble" app/frontend/*.js app/frontend/*.html` prints nothing. memory/contracts/api.md:76 says an unsplit record has `unsplit: true` and the one above the first real record `preamble: true`.

## 3. Upgrade behaviour (upg129.py)
A case created under the parent with a cover sheet, whose gap flag the paralegal accepted, then re-ingested by HEAD code on the same DB file:
`old: [('f_gap_r2_r3', 'accepted', 70), ('f_date_r1', 'pending', None)]` then `new: records r1 2026-01-09, r2 2026-03-20, r3 None; flags [('f_gap_r2_r3', 'accepted', 70, ['r2','r3']), ('f_gap_r1_r2', 'pending', 70, ['r1','r2']), ('f_date_r3', 'pending', None, ['r3'])]`. `_persist` (pipeline.py:186-208) keeps the accepted row by id, and it now cites r3 = the cover sheet.

```json
{"card": "T-129", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of 93de5f2 (ingest.py identical to 3a74f75) and 3a74f75~1 in scratchpad T128_9_127_r1; app/backend/ingest.py, tests/unit/test_ingest.py, app/backend/present.py record_view, app/backend/pipeline.py _store_records/_persist, memory/contracts/api.md:76; fixture/no backend, no network",
 "exercised": [
  "python3 tools/board.py show T-129; git diff 3a74f75~1 3a74f75; read app/backend/ingest.py in full",
  ".venv/bin/python -m pytest tests/unit -q in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed",
  "cmp_ingest.py: parent vs HEAD ingest over 27 .txt inputs under evals/, tests/, spec/, app/ (0 differ in record numbers/sources/unsplit)",
  "ab.py: 9 input shapes through parent and HEAD ingest (preamble with ---, blank line, no separator, header style; mid-note; trailing note; date-like preamble)",
  "ov129.py: 6 preamble shapes checked for overlapping record spans (none)",
  "api129.py: pipeline.ingest_case + present.record_view keys for a preamble case and a mid-note case (parent and HEAD)",
  "upg129.py: case created and gap flag accepted under the parent, re-ingested under HEAD on the same sqlite file",
  "mut.py: 5 mutants of ingest.py against tests/unit/test_ingest.py (sort off, preamble flag never set, preamble always true, first = block start, drop leftovers): all 5 killed",
  "grep of app/frontend for UNSPLIT/unsplit/preamble; grep of callers of ingest/split_records/_store_records"
 ],
 "verdict": "changes",
 "scores": {"numbering_stability": 5, "nothing_dropped_D027": 5, "api_exposes_preamble": 2, "contract_matches_code": 2, "test_strength": 4, "upgrade_safety": 3},
 "findings": [
  {"severity": "major",
   "title": "The preamble is still a counted record 3 and nothing the API serves says it is a preamble: api.md:76 promises `unsplit`/`preamble` fields on the record that GET case and POST case do not return",
   "evidence": "api129.py on HEAD: `record_view` keys are char_end, char_start, date_candidates, date_iso, date_raw, date_status, duplicate_of, encounter, id, injection_tag, language, seq, source_label, text; the cover sheet prints `('r3', 3, 0, None, None, 'FAX COVER SHEET|To')`. present.py case_view returns `\"warnings\": []`; `grep -rn \"UNSPLIT\\|unsplit\\|preamble\" app/frontend` prints nothing. memory/contracts/api.md:76: 'text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: ... the one above the first real record also has `preamble: true`'. Card AC 1: 'is not counted as a record (or is shown as a preamble, not a record)'. Handoff: 'Left: frontend may label preamble records.'",
   "why_it_matters": "The harm the paralegal reported (a cover sheet shifting 'record 1') is fixed. But AC 1 asks for one of two outcomes: the cover sheet is not counted (it is, as record 3, so a 2-record packet reports 3), or it is shown as a preamble (the UI cannot tell: the flag lives only in the in-memory ingest dict, which `_store_records` (pipeline.py:158) does not persist and `record_view` does not emit). The contract text is wrong for GET case, so a frontend following it finds no field. The stated 'frontend may label' follow-up cannot be built without a backend change.",
   "fix": "Persist `unsplit` and `preamble` on the records row (or derive them in `record_view` from `source_label == '' and date_raw == ''` plus position) and add both to `record_view`; carry the `UNSPLIT_TEXT` warning into GET case or document that it is POST-only. Then update api.md:76 to say which responses carry the fields. Frontend card to label it 'cover text, not a record'.",
   "acceptance_test": "tests/unit: create a case from a cover-sheet paste, then `GET /api/cases/{token}`: records[2] has `preamble: true` and `unsplit: true`, records[0..1] have both false, and a library packet (golden case_01) has all records false."},
  {"severity": "minor",
   "title": "A case stored before this commit and re-ingested after it keeps its accepted review on the old record numbers, so the accepted gap flag now cites the cover sheet",
   "evidence": "upg129.py: old (parent) `('f_gap_r2_r3', 'accepted', 70)`; after HEAD re-ingest on the same DB: `('f_gap_r2_r3', 'accepted', 70, ['r2','r3'])` alongside a new pending `('f_gap_r1_r2', 'pending', 70, ['r1','r2'])`, with r3 now the cover sheet. pipeline.py:150-166 (`_store_records` deletes and re-stores) and :186-208 (`_persist` keeps the old row's review_status by id; stale rows are removed only if pending).",
   "why_it_matters": "A reviewed item stays bound to a number that now means a different record; the accepted gap would still be listed for export. Exposure is bounded (cases purge after 24 h, `DB.RETENTION_SECONDS`, and only pastes with unsplit text are affected), so it is minor, but it is the numbering-stability question the brief asked and the card has no note, no migration and no test.",
   "fix": "Either re-run is allowed to drop a reviewed item whose record_ids no longer match the stored records, with a visible reset, or document in the card/DECISIONS that numbering changed and in-flight cases with unsplit text must be re-created (retention makes this a one-line note).",
   "acceptance_test": "Unit test: store a case with a preamble using the old numbering (records r1 preamble, r2, r3, accepted f_gap_r2_r3), re-run ingest_case with the new code, assert no accepted flag cites a record whose date differs from the one it was computed on, or that the item is reset to pending."}
 ],
 "whats_right": [
  "Numbering is stable on real data: 27 golden/library/spec inputs produce identical record numbers before and after, and the preamble cases keep r1, r2 for the real records in 6 shapes.",
  "D-027 is honoured: the preamble is kept verbatim as its own unsplit record, `UNSPLIT_TEXT` is raised for it, and no span overlaps another.",
  "The tests pin the behaviour (6 parametrized preambles plus 2 more): all 5 mutants I ran against ingest.py (sort, flag, first-field, always-preamble, dropped leftovers) fail at least one test."
 ],
 "questions_for_chris": []}
```
