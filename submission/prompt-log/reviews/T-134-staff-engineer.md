# T-134 staff-engineer-reviewer, round 1 (commit 5fb338d)

Verdict: changes. No blocker. One major: the per-item trace still says "Accepted by you" for an edit that is still open.

Pin: I made `git archive` of 5fb338d (HEAD when I started; HEAD then moved to bea3984, but `git diff --stat 5fb338d HEAD -- app/backend/review.py trace.py store.py export.py` is empty, so the code under review is unchanged). Parent for comparison: `git archive 5fb338d^` = f939ccb. Probe scripts and outputs are in `artifacts/review-evidence/T-134/`.

## What the card asked, checked one by one

| Check | Result | Evidence |
|---|---|---|
| Edited entry still needs_review never reaches the letter, never counts accepted, notes do not say accepted | holds | `paralegal_view.py` (HTTP, served copy): letter has only record 1; `excluded {'pending': 22, 'edit_not_confirmed': 1}`; EDITED ITEMS says "edited; second check not available (JUDGE_UNAVAILABLE); not yet confirmed against the quote, so it is not in the letter". `probe134g.py`: also absent from `?style=oneline`; RECORDS NOT IN THE TREATMENT SECTION lists it "edited, not yet confirmed against the quote". |
| Explicit accept with wording that fails a code check is 422 | holds | `probe134e.py`: old data tampered to "9/10"; accept -> `422 CODE_CHECK_FAILED`; gate `ready False ['SUMMARY_TOKEN_NOT_IN_EXCERPT']`; export 422. A fresh edit with a bad figure is also 422 (probe134.py S9). Mutant M17 (accept skips the check) is killed. |
| gate.ready equals export-allowed | holds in every probed state | `probe134.py` checks `gate.ready == (export 200)` after every step of 9 sequences; 0 problems. |
| Spanish and OCR edits need an explicit accept | holds | Spanish: `test_api_spanish_case_end_to_end_label_edit_export` (passes). OCR: `probe134d.py` on an OCR case with a judge that answers "supported": after edit `edited needs_review ['OCR_DERIVED'] edit_to_check=True`, edited text not in letter; after accept it is in the letter and the notes keep "still marked for review (OCR_DERIVED)". |
| 8+ edit and accept sequences | 10 probed, 0 invariant breaks | edit; edit-undo; edit-undo-reedit; edit-accept-edit; edit-accept-undo; edit-dismiss; accept-edit; edit twice; two edits then accept one; quote-picker (summary+excerpt) edit; batch accept on an open edit is refused (not pending). |
| Unit suite | 3318 passed, 4 skipped, 182.8 s | `pytest tests/unit -q` in the archive copy (handoff said 3298; I did not find why the count differs). |

## The 5 changed existing tests

- `test_spanish_records.py:359-364`: correctly updated and stronger (asserts the edit is open, not in the letter, then explicit accept, then in the letter).
- `test_trace.py:~867` and `~1100`: correctly updated (they now assert NOTHING_ACCEPTED plus the warning, then accept, then ready and export 200).
- `test_trace.py:1004-1015` (`test_an_edited_item_counts_as_accepted_for_the_judge_blocker`): weakened. After the change the item is accepted before the final assertion, so the `edited` arm of `judge_not_run_blockers` (trace.py:821) is no longer exercised. Mutant M16 (arm reduced to `("accepted",)`) survives 269 tests. The docstring still says "status 'edited' blocks like 'accepted'". The new check is also behind an `if state == "needs_review":` so it can skip silently. See finding 3.
- `test_trace.py:1075`: loosened by `if b["item_id"]`, which hides any extra case-level blocker. See finding 3.

## Mutation spot-check (scratch copy, tests: t134, trace, spanish, ocr_invariant, export, export_edge, review_rules, api_routes)

Killed (13): M1 rule off, M2 status not flipped, M3 excerpt edits not covered (killed only by the changed test_trace test, not by the new file), M4 judge blocker on open edit, M5 warning dropped, M6 NOTHING_ACCEPTED counts open edit, M8 notes say accepted, M9 excluded count removed, M10 gate accepted count, M11 `_was_edited`, M13 reason lost after accept, M14 view flag false, M17 accept skips code check.
Survived (4): M7 `ready_to_export` ignores the open edit (present.py:206), M12 case-trace review step EDIT_NOT_CONFIRMED branch removed (trace.py:1025), M15 verdict label ignores the open edit (trace.py:1062), M16 above. M18 anchor matched twice, so it did not run.

## Paralegal view (served copy, port 7947, fixture backend curated, ZLAYT_MODE=local, scratch DB; listener PID 52680 checked with `ps` and `lsof`, then killed by that PID)

Steps: sample case, run, accept record 1, edit record 3 ("Persistent neck pain 6/10 with daily headaches noted."), export without accepting.
- Row (screenshot `artifacts/review-evidence/T-134/ui-after-edit.png`): "Needs review | Edited", a primary button "I compared it with the quote", and "Still marked Needs review ... Until then it counts as open." Header "1 of 23 decided", chip "1 edit to check", "Ready to export, 22 not reviewed". Honest.
- Letter: one entry (record 1). The edit is not there. Honest.
- Notes: "Items not reviewed: 22" counts the edit; EDITED ITEMS and PENDING ITEMS NOT INCLUDED both say second check not available and not in the letter. After pressing accept (API), the letter carries the edit and the notes say "accepted by the paralegal after comparing it with the quote; second check not available (JUDGE_UNAVAILABLE)". Honest.
- Not honest: "Why this status" for that row (item trace) says "Accepted by you" / "You edited this item and accepted it." (finding 1). And the case checks banner says "What you need to do: The second AI check did not run on 1 item. Run it again; accepted items it never checked cannot go in the letter." although nothing is accepted and the item is out of the letter (finding 4; same text at the parent f939ccb).

## Right already
- One rule (`review.edit_unconfirmed`) feeds the item view, counts, export, gate and notes; gate and export never disagreed in 10 sequences.
- Accept stays bound by the code checks (D-051) and a Spanish/OCR edit needs her explicit accept; the notes keep the reason code after she accepts.

```json
{"card": "T-134", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 5fb338d (app/backend review.py, store.py, export.py, present.py, trace.py, api.py; tests t134 + 4 changed tests); parent f939ccb for comparison; served copy http://127.0.0.1:7947 (fixture backend, curated, ZLAYT_MODE=local); sample case evals/golden/sample.txt",
 "exercised": [
  "read board show T-134, D-044, D-045, D-051, D-053, reviews/T-060-paralegal-pass4.md M2, git show 5fb338d in full",
  "pytest tests/unit -q on git archive 5fb338d: 3318 passed, 4 skipped",
  "probe134.py: 9 edit/accept/undo/dismiss sequences, invariant checks after each (artifacts/review-evidence/T-134/probe134.py)",
  "probe134c.py: quote-picker edit (summary+excerpt), excerpt-only 422s, item trace, batch accept route",
  "probe134d.py: OCR-derived entry edit with a supporting judge, export before and after accept",
  "probe134e.py: stored wording failing a code check: accept 422, gate vs export 422",
  "probe134g.py: standard and oneline export, RECORDS NOT IN THE TREATMENT SECTION, narrative route",
  "mutation runs M1-M17 on a scratch copy (13 killed, 4 survived)",
  "served the archive copy on port 7947, ran paralegal_view.py, steps134.py, shot134.py (Playwright screenshot), killed PID 52680",
  "judges_step134.py on f939ccb and 5fb338d: judges step FAIL with an open edit exists at the parent"
 ],
 "verdict": "changes",
 "scores": {"export_honesty": 4, "gate_export_agreement": 5, "code_check_binding": 5, "test_strength": 3, "state_consistency_across_surfaces": 3},
 "findings": [
  {"severity": "major", "title": "Item trace still says an open edit was accepted",
   "evidence": "app/backend/trace.py:247-248 returns step human PASS 'You edited this item and accepted it.' for review_status edited; trace.py:281-282 sets verdict {'code':'accepted','label':'Accepted by you'}. Neither calls review.edit_unconfirmed. Repro: artifacts/review-evidence/T-134/paralegal_view.py http://127.0.0.1:7947 prints \"ITEM TRACE verdict: {'code': 'accepted', 'label': 'Accepted by you', 'blocks_export': False}\" and \"[('human', 'pass', 'You edited this item and accepted it.')]\" right after the edit, while export excludes the entry and the gate warns EDIT_NOT_CONFIRMED. The frontend renders this verdict (app/frontend/stepper.js:411, 'Why this status').",
   "why_it_matters": "Paralegal pass 4 M2 was exactly this contradiction: the app says accepted while the row, the letter and the notes say it is open. T-134 fixed the letter, gate and notes but left the item's own audit trail claiming her acceptance, which is the text she (or opposing counsel) would read as the record of what she decided.",
   "fix": "In trace.py _human_step and the item verdict (lines 247 and 281), branch on review.edit_unconfirmed(kind, row): human step PENDING with 'You edited this item; it is not accepted until you compare it with the quote and accept', reason EDIT_NOT_CONFIRMED, next_action DECIDE; verdict code 'edit_to_check', label 'Edited; waiting for your check'. Keep the 'accepted' wording only for review_status accepted.",
   "acceptance_test": "Fixture case, edit e3 with no judge fixture, GET /items/e3/trace: verdict.code != 'accepted', 'Accepted' not in verdict.label, human step status 'pending'. After POST accept: verdict.code == 'accepted'. Mutant: revert the branch and the test fails."},
  {"severity": "minor", "title": "Three agreed surfaces have no test that fails when they break",
   "evidence": "Mutants M7 (present.py:206 drop the edit_to_check clause of ready_to_export), M12 (trace.py:1025 remove the EDIT_NOT_CONFIRMED review-step branch) and M15 (trace.py:1062 drop n_edit from the verdict label) all SURVIVE: '309 passed' for each across test_t134, test_trace, test_spanish_records, test_ocr_invariant, test_export, test_export_edge, test_review_rules, test_api_routes. tests/unit/test_t134_unconfirmed_edit.py only asserts ready_to_export False in a case that is already False because pending > 0 (line 55).",
   "why_it_matters": "The card's point is that several places agree. The review step text, the 'Ready to export (N not reviewed)' label the paralegal sees in the header, and the API field can regress without a red test.",
   "fix": "Add assertions: with every other item decided and one open edit, review.ready_to_export is False and the case-trace review step is pending with reason EDIT_NOT_CONFIRMED; verdict.label contains '(1 not reviewed)' when nothing else is pending.",
   "acceptance_test": "Re-run mutants M7, M12, M15 (reverse each edit above in a scratch copy); each makes at least one test fail."},
  {"severity": "minor", "title": "One existing test was weakened and one loosened",
   "evidence": "tests/unit/test_trace.py:1004-1015 test_an_edited_item_counts_as_accepted_for_the_judge_blocker now accepts the item before its last assertion, so the review_status 'edited' arm at trace.py:821 is untested: mutant M16 (arm changed to (\"accepted\",)) survives with '269 passed'. The new guard at line 1012 is `if ... state == \"needs_review\":`, which skips silently if the state differs, and the docstring (line 1005) still says \"status 'edited' blocks like 'accepted'\". tests/unit/test_trace.py:1075 adds `if b[\"item_id\"]`, which stops the list check from catching an extra case-level blocker. The new test file has no excerpt-only edit case; M3 is killed only by the changed test_trace test.",
   "why_it_matters": "A D-044 gate arm lost its proof when the test was bent to fit the new rule, and the guard can pass without running its assertions.",
   "fix": "Keep the old case and add a second one for an edited, unjudged, non-needs_review entry (or a flag note edit) that still blocks; make line 1012 an unconditional assert; assert the exact blocker list [(edt, 'SUMMARY_DROPS_QUALIFIER'), (None, 'NOTHING_ACCEPTED')] at line 1075; add a t134 test that an excerpt-only edited entry is edit_to_check.",
   "acceptance_test": "Mutants M16 and M3 each fail a test in test_t134_unconfirmed_edit.py or test_trace.py."},
  {"severity": "minor", "title": "Case-checks banner still tells her to re-run a check for an item that is out of the letter",
   "evidence": "Pre-existing at f939ccb (artifacts/review-evidence/T-134/judges_step134.py prints the same line for the parent and for 5fb338d): 'judges fail | 1 item has not been double-checked ...' with counts unavailable 1, after the edit, while gate is pass. Screenshot artifacts/review-evidence/T-134/ui-after-edit.png: 'What you need to do: The second AI check did not run on 1 item. Run it again; accepted items it never checked cannot go in the letter.' The unit test test_edited_summary_with_judge_unavailable_leaves_judges_step_and_gate_clean asserts unavailable == 0, which passes only with the default fixture set, not with FIXTURE_SET=curated.",
   "why_it_matters": "With T-134 the edit is not accepted and not in the letter, so the banner's reason ('accepted items') is false and it asks for a re-run that D-045(b) says a human edit does not need. Not introduced by this commit; it sits next to the M2 fix and the paralegal reads it in the same header.",
   "fix": "Exclude human-authored edits (D-045b) from the judges step unavailable count, or word the banner for the open-edit case; then run the test under FIXTURE_SET=curated too.",
   "acceptance_test": "FIXTURE_SET=curated, edit e3: case trace judges step is not 'fail' and its counts.unavailable == 0."},
  {"severity": "nit", "title": "Unrelated route-order swap in the same commit",
   "evidence": "app/backend/api.py:509-512 in the diff: billing.add_routes and pdf_routes.add_routes exchanged places; neither the card, the handoff nor the commit message mentions it.",
   "why_it_matters": "A behaviour change in route registration order hides inside a fix commit. The 3318-test suite is green, so I found no breakage; this is a process note.",
   "fix": "Say why in the handoff, or revert it.",
   "acceptance_test": "Handoff or commit message names the reason."}
 ],
 "whats_right": [
  "One rule (review.edit_unconfirmed) feeds the item view, counts, export, gate and notes; gate.ready equalled export-allowed in all 10 probed sequences.",
  "Accept stays bound by the D-051 code checks (422 CODE_CHECK_FAILED, nothing written), and Spanish and OCR edits need her explicit accept with the reason code kept in the notes.",
  "The letter, notes and row are honest in the paralegal run: the edit is out of the letter, counted in 'Items not reviewed', and the notes never say accepted."
 ],
 "questions_for_chris": []}
```
