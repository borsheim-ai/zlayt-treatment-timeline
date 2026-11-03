# T-134 staff-engineer-reviewer, round 2 (commit db1d8d5)

Verdict: changes. No blocker. The r1 major is fixed and the r1 minors are closed, but one sibling reader of the same "edited means accepted" rule was missed again: the judge report counts an open edit as "you accepted despite an objection".

Pin: `git rev-parse HEAD` at start was db1d8d5; it later moved to 0c24f5f, and `git diff --stat db1d8d5 HEAD -- app tests memory` is empty, so the code reviewed is the code at HEAD. Review copy: `git archive db1d8d5` (no .git, so the 8 skips versus the handoff's 1 are tests that skip on untracked fixtures; I did not chase them). Probes and outputs are in `artifacts/review-evidence/T-134/r2/`.

## What the brief asked

| Check | Result | Evidence |
|---|---|---|
| Item trace for an open edit says "Edited; waiting for your check" (`edit_to_check`); "Accepted" only after explicit accept or for a verified edit | holds | trace.py:248-250 (human step pending, EDIT_NOT_CONFIRMED, next_action DECIDE), trace.py:281-290 (verdict). `probe134c.py`: `ITEM TRACE verdict: {'code': 'edit_to_check', 'label': 'Edited; waiting for your check', 'blocks_export': False}`, human step pending, "not accepted until you compare it with the quote". After accept: `accepted` / "Accepted by you". |
| Re-run my 10 edit and accept sequences through trace, gate, notes, letter | 0 problems | `probe134r2.py` (r1 sequences S1-S9 plus quote-picker S10). After every step, for every entry: open edit has verdict `edit_to_check` and human step pending; no pending or dismissed item reads accepted; gate.ready equals export 200; open edit not in letter or items; `excluded.edit_not_confirmed`, gate warning and "Items not reviewed" agree. Output ends `TOTAL PROBLEMS 0` (`probe134r2.out`). `probe134g/d/e/c`: oneline and standard letter exclude the edit; RECORDS NOT IN THE TREATMENT SECTION says "edited, not yet confirmed against the quote"; OCR edit needs explicit accept and the notes keep OCR_DERIVED; stored wording failing a code check is still 422 CODE_CHECK_FAILED on accept and the item trace says `needs_attention`. |
| My 4 surviving mutants now die | yes | `mutate.py` on a scratch copy, tests = t134, trace, spanish, ocr_invariant, export, export_edge, review_rules, api_routes. M7 (present.py `edit_to_check == 0` clause) KILLED by `test_everything_else_decided_the_open_edit_alone_keeps_review_and_header_not_ready`; M12 (review step EDIT branch) KILLED by the same; M15 (header `n_pend + n_edit`) KILLED by the same; M16 (`edited` arm of judge_not_run_blockers) KILLED by `test_trace.py::test_an_edited_unjudged_entry_that_is_not_needs_review_still_blocks_as_accepted_would`. New-branch mutants N1 (human step), N2 (verdict), N4 (judges-step skip), N9, N10 also KILLED. |
| test_trace tests restored to full strength | yes | `test_an_edited_item_counts_as_accepted_for_the_judge_blocker` now has an unconditional `assert state == "needs_review"` and asserts the item enters the blocker list after accept (test_trace.py ~1004-1013); the exact list `[(edt, "SUMMARY_DROPS_QUALIFIER"), (None, "NOTHING_ACCEPTED")]` is asserted without the `if b["item_id"]` filter; the `edited` arm has its own test. The one remaining edit to the old test at `test_item_trace_shows_the_failing_code_step...` (human step now pending/EDIT_NOT_CONFIRMED) is correct under the new rule. |
| Case-checks banner | fixed for the reported case | `probe134`/`excerpt_only_curated.py` and the new test `test_judges_step_ignores_a_human_edit_whose_rerun_check_was_unavailable_under_the_curated_set`: with FIXTURE_SET=curated and a summary edit, judges step is not `fail`, `counts.unavailable == 0`, `/judges` `unresolved` has no e3. The skip is narrow: only human-authored wording AND verdict `unavailable` (trace.py:778-779); an AI summary with only its quote edited still counts as unjudged and the banner "Run the second check again" stays, which is correct because accepting it would be blocked by JUDGE_NOT_RUN (checked: `excerpt_only_curated.py` default and curated). |
| Unit suite | 3450 passed, 8 skipped, 190 s | `pytest tests/unit -q -p no:cacheprovider` in the archive copy. |

## Out-of-scope item: api.py route-order swap (billing/pdf_routes)

Not a bug. `routes_order.py` on the parent (5fb338d^) and db1d8d5: both build 34 routes, identical route sets (`cmp` of the sorted method/path lists), zero shadowed pairs (no earlier route of the same method matches a later route's path). The two swapped routes are `/api/cases/{token}/billing` and `/api/cases/{token}/pages/{n}/image`, which do not overlap. It is an unexplained hunk, harmless, so no finding beyond saying so; it still deserves a line in the card or a revert.

## Findings

One major (judge report), two minors (test gaps; undo-of-edit state, pre-existing and out of this card's scope).

```json
{"card": "T-134", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive db1d8d5 (HEAD at start; app/ and tests/ identical at 0c24f5f); app/backend/trace.py, review.py, present.py, api.py; tests/unit/test_t134_unconfirmed_edit.py, test_trace.py; parent 5fb338d^ for comparison; fixture backend, sample case evals/golden/sample.txt, FIXTURE_SET default and curated; no served app (backend routes through TestClient)",
 "exercised": [
  "read reviews/T-134-staff-engineer.md, board show T-134 with handoff, git show db1d8d5 in full (trace.py, api.md, two test files)",
  "pytest tests/unit -q on git archive db1d8d5: 3450 passed, 8 skipped",
  "probe134r2.py: 10 edit/accept/undo/dismiss sequences, per-item trace for every entry plus case trace, judge report, gate, export after each step: TOTAL PROBLEMS 0 (artifacts/review-evidence/T-134/r2/probe134r2.out)",
  "probe134c/d/e/g.py re-run on db1d8d5: item trace verdict, OCR edit, code-check-failing accept 422, oneline and standard letter, RECORDS NOT IN THE TREATMENT SECTION",
  "mutate.py: 12 mutants on a scratch copy (M7, M12, M15, M16, N1, N2, N3, N4, N5, N9, N10, N11): 9 killed, 3 survived (N3, N5, N11)",
  "objecting_judge.py: open edit whose re-check objected (partially): judge report human_overrides 1, item verdict edit_to_check, export 200 without the edit",
  "reset_judge.py and undo_accept.py on 5fb338d^, 5fb338d and db1d8d5: edit then undo then accept then export gives 422 JUDGE_NOT_RUN in all three",
  "excerpt_only_curated.py: quote-picker (excerpt-only) edit, default and curated sets, judges step and item verdict",
  "routes_order.py: route tables of parent and db1d8d5 equal, no shadowed route",
  "grep of every review_status in (accepted, edited) reader in app/backend/trace.py and app/frontend/judges.js"
 ],
 "verdict": "changes",
 "scores": {"export_honesty": 5, "gate_export_agreement": 5, "code_check_binding": 5, "test_strength": 4, "state_consistency_across_surfaces": 3},
 "findings": [
  {"severity": "major", "title": "Judge report counts an open edit as 'you accepted despite an objection'",
   "evidence": "app/backend/trace.py:865-866 in judge_report: `if row[\"review_status\"] in (\"accepted\", \"edited\"): overrides += 1`, with no review.edit_unconfirmed check. app/frontend/judges.js:164 renders it as the tile 'you accepted despite an objection'. Repro: python artifacts/review-evidence/T-134/r2/objecting_judge.py <archive of db1d8d5> (sample case, accept e1, edit e3, set e3's stored re-check verdict to partially, which is the JUDGE_PARTIAL warning path of review.py:6-7) prints `e3 edited needs_review edit_to_check True`, `totals {'items_judged': 20, 'supported': 19, 'unsupported': 1, 'unsure': 0, 'unavailable': 0, 'human_overrides': 1}`, `item verdict {'code': 'edit_to_check', ...}`, `export 200 e3 in letter: False`. Mutant N11 (exclude open edits from the count) SURVIVES 315 tests, and no test asserts human_overrides for an open edit either way.",
   "why_it_matters": "This is the r1 major in a different place and the same bug class as paralegal pass 4 M2: one surface says she accepted an item that the letter, the gate, the notes and now the item trace all say is still open. The judge panel is the audit view of where she went against the second AI check; it tells her, and anyone reading it later, that she accepted despite an objection when she has not accepted anything. The one-rule fix again covered the readers its author listed and not the sibling `(accepted, edited)` reader that I named in my r1 memory of this card.",
   "fix": "At trace.py:865 count an override only when the edit is decided: `if row[\"review_status\"] in (\"accepted\", \"edited\") and not review.edit_unconfirmed(r[\"kind\"], row): overrides += 1`. Then grep the other `(\"accepted\", \"edited\")` readers (trace.py:433 and :526 are fine: the first is meant to gate old data, the second is amounts, which have no edit) and note the grep result in the handoff.",
   "acceptance_test": "Unit test: edit an entry so the re-check objects (judge fixture partially or unsupported, or stored verdict set as in objecting_judge.py): GET /judges totals.human_overrides == 0 while edit_to_check is true; POST accept: human_overrides == 1. Mutant N11 above must make the test fail when the guard is removed."},
  {"severity": "minor", "title": "Two new branches and the judge-report scope of the human-edit skip have no killing test",
   "evidence": "mutate.py on db1d8d5: N3 (trace.py:285-286 `first_na` for an open edit replaced by None) SURVIVED `315 passed`; N5 (trace.py:778-779 skip widened from verdict == unavailable to any verdict on human-authored wording, which would hide an objection from the judges step and report) SURVIVED `315 passed`. test_t134_unconfirmed_edit.py asserts `h[\"next_action\"][\"code\"] == \"DECIDE\"` on the human step but never the item-level `next_action`, and no test sets a human-edited entry's verdict to partially or unsupported and checks it stays in /judges.",
   "why_it_matters": "N5 is the exact way the r2 judges-step fix could later over-hide: D-045b exempts her wording from the judge's blocking power, not from appearing in the report. N3 leaves the 'what to do next' hint for the open edit unproved, and the UI reads it.",
   "fix": "Assert t['next_action']['code'] == 'DECIDE' in test_item_trace_of_an_open_edit_does_not_say_accepted; add a test that an edited entry with an objecting stored verdict remains in /judges rejections and totals.unsupported (it can share its fixture with the human_overrides test above).",
   "acceptance_test": "Re-run mutants N3 and N5 in a scratch copy; each makes at least one test fail."},
  {"severity": "minor", "title": "OUT OF SCOPE (pre-existing at the parent): undoing an edit leaves the restored AI wording with the edit's 'unavailable' second check, and accept then hits JUDGE_NOT_RUN",
   "evidence": "artifacts/review-evidence/T-134/r2/undo_accept.py prints the same on 5fb338d^, 5fb338d and db1d8d5: `orig e3 ... pending verified`, `after reset pending needs_review ['JUDGE_UNAVAILABLE'] Persistent neck pain 6/10 and daily headaches; referred to p...` (the original AI wording, whose second check had said supported), `accept 200`, `export 422 [('e3', 'JUDGE_NOT_RUN')]`. reset_judge.py: judges step goes pass -> fail (unavailable 1) after reset.",
   "why_it_matters": "Reset restores the AI summary but keeps the judge result of the edited wording, so the original 'supported' verdict is lost and an item that was verified before the edit needs a manual re-run afterwards. It is a visible blocker with a RERUN_JUDGE action, not a silent fallback, and it was not introduced by T-134, so it is not rated higher and does not block this card.",
   "fix": "Either keep the original judge record when an edit is saved and restore it on reset, or clear the judge result and re-run it on reset. Needs a backend card; do not fold it into T-134.",
   "acceptance_test": "Edit e3, reset, accept: export is 200 on the sample case with the default fixture set (or the item shows a pending re-run, not a stale unavailable)."}
 ],
 "whats_right": [
  "The item trace now follows the same `review.edit_unconfirmed` rule as gate, export and notes: 10 sequences, every surface agreed, gate.ready equalled export-allowed each time.",
  "The r1 test weakening was undone properly: unconditional assert, exact blocker list, and a dedicated test for the `edited` arm (M16 now dies); M7, M12 and M15 each have a killing test.",
  "The judges-step fix is narrow (human wording and verdict unavailable only), reproduced under FIXTURE_SET=curated, and leaves the useful banner for an AI summary whose quote was edited."
 ],
 "questions_for_chris": []}
```
