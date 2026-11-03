# T-134 staff-engineer-reviewer, round 4b (amends reviews/T-134-staff-engineer-r4.md)

Verdict unchanged: changes (one major, F1). This file replaces the r4 file's findings array and corrects three statements in the r4 body. The r4 file cannot be edited under the reviewer write guard, so this is the record to use.

Corrections to the r4 file:

1. Pin paragraph. The r4 file says the diff from 4f416a4 to 2db6ad2 "touches `present._why` (judge argument) and one api.md paragraph". It touches `present._why` and `present._common` (both pass the judge record) and two api.md hunks (the T-146 status paragraph near api.md:128 and the T-139 narrowing bullet near api.md:768). None of these is one of the five T-134 items.
2. "Only the AI's own quote passes" is overstated. `probe_b3.py` / `probe_b3.out` tried three candidates for e3 with the AI summary kept: the three-sentence record quote was refused (422, the attribution 'Patient reports' is not in the summary), the first sentence alone was refused (422, the summary's number '2' is not in the quote), and the first two sentences (the AI's own excerpt) were accepted (200). The loop stopped at the first accepted quote, so the second sentence alone was never run. I have not shown that no other valid quote exists on this sample. The conclusion that matters, that the 'second pick' test re-saves the same text, does not depend on this (probe B-setup: Q1 equals the AI excerpt after strip).
3. The F2 evidence and the 'second pick' row in the table are corrected by point 2 above; the other findings and the verdict are unchanged.

Evidence is under `artifacts/review-evidence/T-134/r4/`: `probe134r4.out` (sections A to D), `probe_b3.out`, `mutants.txt`, `unit_runs.txt`, and `leak138r2.out` (shared with T-138).

```json
{"card": "T-134", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive 4f416a4 (card commit; HEAD at start) and 2db6ad2 (HEAD at finish, same results): app/backend/trace.py, review.py, present.py, export_routes.py, tests/unit/test_t134_unconfirmed_edit.py, memory/contracts/api.md T-134 r4 paragraph; app/frontend/review.js and dom.js for the held-edit text; fixture backend; sample case evals/golden/sample.txt via TestClient; no served app, no browser",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-134-staff-engineer-r3.md, board show T-134 (7.4 note and card AC), the D-058 row in memory/ORCHESTRATOR_DECISIONS.md (api.md mirror)",
  "git show 4f416a4 (trace.py, present.py, export_routes.py, test file) in full; git diff 4f416a4 2db6ad2 on the in-scope files",
  ".venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py on git archive 4f416a4: 37 passed; same on 2db6ad2: 37 passed",
  "regression modules test_trace, test_export, test_export_edge, test_review_rules, test_api_routes on 4f416a4 with one pre-existing red test deselected: 266 passed, 1 deselected; the red test alone on 4f416a4 and on 68b8685: 1 failed (assert ['e2', 'e4'] == [])",
  "probe134r4.py on 4f416a4 (sections A, B, C, D) and on 2db6ad2: outputs identical",
  "probe_b3.py: three candidate quotes for e3 with the AI summary kept: 422, 422, 200 (the AI's own two sentences)",
  "mutate_r4.py on 4f416a4: N18, N19 (re-anchored), N21, N22, H2 and P1 all KILLED (mutants.txt)",
  "mutate_r3.py N19 on 4f416a4: SKIP (anchor count 0), so the r3 N19 mutant no longer applies",
  "frontend grep: review.js:182-183 and :191 ('stays blocked' / 'export stays blocked'); second_check_pending absent from app/frontend (0 lines); dom.js:55 ZL.secondCheckPending inference; review.js:320 toCheck = ZL.editToCheck; review.js:342-344 edit-check-hint",
  "backend grep: 'stays blocked' in app/backend (trace.py:447 only, inside _fix_action for _code_check_gated items, trace.py:432-435); judge_not_run_blockers trace.py:849-853",
  "pytest --collect-only -q on test_t134_unconfirmed_edit.py: 26 tests"
 ],
 "verdict": "changes",
 "scores": {"d058_wording_backend": 4, "d058_wording_ui": 2, "rerun_claim_currency": 4, "test_strength": 3, "field_and_docs": 3},
 "findings": [
  {"severity": "major",
   "title": "The open re-picked-quote card still says the export stays blocked while the gate passes: the r4 backend wording broke the frontend's server-text swap",
   "evidence": "app/frontend/review.js:182 AI_HELD = '...Accepting alone will not put it in the letter: the export stays blocked until the second check answers...'; review.js:342-344 shows it as edit-check-hint when ZL.secondCheckPending(item) (dom.js:55: ai_drafted and JUDGE_UNAVAILABLE and not a summary the paralegal wrote), and the card exists when item.edit_to_check (review.js:320). review.js:191 swaps in the server's human why only if /export stays blocked/ matches, and the r4 text no longer contains that phrase (trace.py:44). Repro: .venv/bin/python -I artifacts/review-evidence/T-134/r4/probe134r4.py <git archive 4f416a4>, section C: 'C gate ready True | export 200'; 'C item human why stays_blocked=False'; 'C item human why matches frontend loadItemWhy regex /export stays blocked/: False'. Same state, section D1: ai_drafted True, reasons ['JUDGE_UNAVAILABLE'], edit_to_check True. The fallback text therefore stays on the card.",
   "why_it_matters": "The 7.4 fix-up condition (3) was no 'export stays blocked' text when the gate passes. Before accept nothing is blocked (gate ready, export 200), and the paralegal reads this card. The backend text is now correct, but the sentence shown is the frontend fallback, which says the opposite. Fail-closed, so nothing wrong exports, but it is a false statement about the export state on the surface the paralegal reads, and it is the r3 minor the 7.4 note said must be gone. Not rated blocker: the conditional and the gate are right, and the wrong sentence is only shown before accept.",
   "fix": "Remove the regex swap at review.js:191 and show the server's why for the held card (the item trace human step, or the case gate warning EDIT_NOT_CONFIRMED) as given. Keep a fallback only in the conditional form ('If you accept it, the export will be blocked until...'), never the unconditional 'stays blocked'. Read item.second_check_pending instead of the dom.js:55 inference, which api.md (T-134 r4 paragraph) already says the UI does.",
   "acceptance_test": "A frontend unit test (or the existing tests/e2e suite) that renders an open quote re-pick under an AI summary with the gate ready and asserts the card's text has no 'stays blocked' and contains the server's human why. Re-introducing the old AI_HELD sentence or the regex must fail it."},
  {"severity": "minor",
   "title": "The 'second pick' test re-saves the identical quote text, so it does not show that a different re-picked quote clears the rerun record",
   "evidence": "tests/unit/test_t134_unconfirmed_edit.py:363 `edits: {'excerpt': QUOTE_ONLY.strip()}` with the comment 'another pick (a summary-safe variant of the quote)'. QUOTE_ONLY (line 257) equals the e3 AI excerpt in evals/golden/sample.txt:16 after strip (probe134r4.out B-setup: True). review.py:327 strips the excerpt, so the stored excerpt before and after the 'pick' is the same string (probe134r4.out B1 and B2 lines). probe_b3.out shows the three candidates tried, 422, 422, 200; the second sentence alone was not tried, so this is not a proof that no other valid quote exists.",
   "why_it_matters": "The handoff says 'my test uses a valid variant' and the orchestrator's 7.4 item 2 asks for a valid re-picked quote. The behaviour is right: review.py:357 drops ladder.rejudge on every edit, and B2 shows the claim clears on an identical re-save. Mutant P1 (the pop removed) is killed by two tests, so the protection holds; the test name and comment describe a different quote than the one tested.",
   "fix": "Correct the comment and the handoff to say it is an identical-text re-save. Add a test that stores a different excerpt for e3 (direct DB write of the excerpt, as the T-138 tests do with _set_ladder, or a second sample record), re-picks it, and asserts the rerun claim is gone and the 422 text says Run the second check again.",
   "acceptance_test": "Unit: rerun no-answer on stored excerpt X, then a valid pick Y != X: blocker why and the 422 message contain no 'ran again' and contain 'Run the second check again'. P1 (review.py:357 pop removed) must fail it."},
  {"severity": "minor",
   "title": "api.md says the UI reads second_check_pending and shows why as given; neither is true at HEAD, and the 'same list as the gate' claim is a superset",
   "evidence": "memory/contracts/api.md:368: 'The UI uses this field instead of inferring it from ladder.judge or reasons' and 'Show why as given.' app/frontend has no reference to second_check_pending (probe134r4.out D2: 'frontend review.js reads second_check_pending: False'; grep -rn second_check_pending app/frontend returns 0 lines). dom.js:55 still infers the state. The same paragraph says the field is 'the same list the JUDGE_NOT_RUN gate reads'; judge_not_run_blockers (trace.py:849-853) also requires accepted or edited and not edit_unconfirmed, so the field is a superset of the gate's list.",
   "why_it_matters": "A contract that says the UI does something it does not is what the next worker builds on (the T-136 follow-up is exactly that). The superset point decides whether a 'second check pending' badge on an unaccepted quote re-pick is a bug or intended.",
   "fix": "Reword api.md:368: the field is set on every view; the frontend reads it when the T-136 card lands (state the current behaviour as a TODO, not as fact). State that the field is the unjudged list minus rates, a superset of the gate's blocker list.",
   "acceptance_test": "Doc check: the T-134 r4 paragraph says the UI reads the field only once app/frontend reads it (grep count is 0 at HEAD); test_second_check_pending_is_an_explicit_item_field already covers the true case, and the superset is documented."},
  {"severity": "minor",
   "title": "OUT OF SCOPE (pre-existing, not from 4f416a4): tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted is red at HEAD",
   "evidence": "artifacts/review-evidence/T-134/r4/unit_runs.txt: on git archive 4f416a4 and on its parent 68b8685 the test fails with `assert ['e2', 'e4'] == []` (test_api_routes.py:170): the T-139 hold-out (CHARGE_TEXT_IN_ENTRY, commits 5f7ef96 and 184cbb7) holds e2 and e4, while the test expects nothing held out. The card handoff reports 6 unit failures and does not name this one.",
   "why_it_matters": "A red test on HEAD hides the next regression in the same module and makes the 'all green' claim on any card meaningless until it is fixed. It is not this card's defect and I do not rate it against T-134.",
   "fix": "Owner of T-139 to decide whether the expectation (nothing held out) or the hold-out is right, then update the other one; track it on a card.",
   "acceptance_test": "pytest tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted passes at HEAD."},
  {"severity": "nit",
   "title": "The card's AC evidence says 28 tests for test_t134_unconfirmed_edit.py; the file has 26",
   "evidence": "board show T-134 AC 1 evidence: 'tests/unit/test_t134_unconfirmed_edit.py (28 tests)'; .venv/bin/python -I -m pytest --collect-only -q tests/unit/test_t134_unconfirmed_edit.py: 26 tests collected (unit_runs.txt).",
   "why_it_matters": "Counts in the AC evidence should match what runs, so the next reviewer can trust them.",
   "fix": "Correct the count in the card's AC evidence.",
   "acceptance_test": "The collected count equals the number in the AC evidence."}
 ],
 "whats_right": [
  "One function (trace.judge_not_run_message) produces the gate headline and the 422 message, and the review step and item step now carry the conditional clause; probe B1 shows headline == 422 message and probe A shows no 'or the entry stays out' text.",
  "The rerun claim follows the current record: an edit drops ladder.rejudge (review.py:357), the identical re-save clears the claim (B2), and a new rerun brings it back (B3); N18, H2 and P1 die.",
  "second_check_pending is set on all 23 views of a fixture case and on the review response, with the same value as the GET case field (D0, D1); the mutants for each new branch (N19 re-anchored, N21, N22) fail at least one test."
 ],
 "questions_for_chris": []}
```
