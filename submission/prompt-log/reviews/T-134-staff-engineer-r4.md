# T-134 staff-engineer-reviewer, round 4 (commit 4f416a4, section 7.4 bounded fix-up, scoped check)

Verdict: changes. No blocker. One major: the open re-picked-quote card in the UI still says "the export stays blocked" while the gate passes, because the r4 backend change broke the frontend's server-text swap. On the backend, the five scoped items hold: both D-058 wordings now say the conditional, the gate headline equals the 422 message, the rerun claim follows the current record, N18, N19 and H2 die, and `second_check_pending` is on every view. Three minors: the "second pick" test re-saves the identical quote, the api.md paragraph says the UI reads a field it does not read, and one red test on HEAD is outside this card.

Pin. `git rev-parse HEAD` at the start was 4f416a4 (the card commit, which contains the r4 change). It had moved to 2db6ad2 by the time I checked again (T-146 r2 and T-139 commits on top). I tested `git archive 4f416a4` and repeated the unit tests, the probe and the leak scan on a `git archive 2db6ad2`: 37 passed, probe output identical. The in-scope diff `4f416a4..2db6ad2` touches `present._why` (judge argument) and one api.md paragraph, not the items below.

I did not run a browser. The UI finding comes from the frontend code path plus the item fields the API returns for the same state (probe sections A and D1), not from a rendered screenshot.

## The five scoped items

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Two D-058 wordings (review step, gate headline) | Holds on the backend. The UI card still shows the old sentence (F1). | `probe134r4.out` A: review step "...accepting alone will not put it in the letter. If you accept it, the export will be blocked until..." and "or the entry stays out" absent. B1 and B2: headline equals the 422 message. |
| 2 | "Ran again" claim comes from the current quote's rejudge record; tested with a valid re-picked quote | Behaviour holds. The test does not re-pick a different quote (F2). | B0 no claim; B1 claim after a no-answer rerun; B2 identical re-save: `ladder.rejudge` None, no claim, Run the second check again; B3 new rerun: claim back. `probe_b3.out`: on this sample only the AI's own two-sentence quote is accepted with the AI summary kept. |
| 3 | No "export stays blocked" text when the gate passes | Holds in the backend text. Fails in the UI (F1). The one backend occurrence, trace.py:447, is attached only to accepted or edited items (trace.py:432-435), which the gate blocks. | `probe134r4.out` C: gate ready True, export 200, item human why and gate warning have no "stays blocked"; `review.js:182` still has it. |
| 4 | N18, N19, H2 killed | Killed. N19 needed a new anchor: the r3 anchor no longer exists on HEAD (`mutate_r3.py` prints `SKIP (anchor count 0)`), so I re-anchored it to the r4 `edit_warning` text. | `mutants.txt`: N18, N19, H2 KILLED; also N21, N22 and P1 KILLED. |
| 5 | `second_check_pending` present and documented | Present on all 23 views and on the review response. Documented, but the doc says the UI uses it, which is not true (F3). | `probe134r4.out` D0, D1; `review.js` has no reference (D2); `api.md:368`. |

Unit tests, both card files: `.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py` gives `37 passed` on 4f416a4 and on 2db6ad2 (26 + 11 collected). Regression modules (`test_trace`, `test_export`, `test_export_edge`, `test_review_rules`, `test_api_routes`) with one pre-existing red test deselected: `266 passed, 1 deselected`. That red test is F4.

Mutation: `mutate_r4.py` on the 4f416a4 archive, 6 T-134 mutants, each run on the 7 modules above: N18, N19 (re-anchored), N21, N22, H2 and P1 all KILLED. P1 (an edit no longer drops `ladder.rejudge`) is killed by two tests, including the identical re-save test, so the behaviour is protected even though the test describes it wrongly (F2).

## Findings

Full detail is in the JSON block. Short form:

- major, F1: the held-edit card text still says "the export stays blocked" while the gate passes (`review.js:182`, swap at `review.js:191`, shown at `review.js:342-344`).
- minor, F2: the "second pick" test re-saves the same text (`test_t134_unconfirmed_edit.py:363`), not a different quote.
- minor, F3: api.md:368 says the UI uses `second_check_pending` and shows `why` as given; neither is true at HEAD.
- minor, F4 (outside this card): `test_api_routes.py::test_export_equals_golden_when_everything_accepted` is red at 4f416a4 and at its parent 68b8685.
- nit, F5: the card's AC note says 28 tests for the T-134 file; collection gives 26.

## Evidence

Everything is under `artifacts/review-evidence/T-134/r4/`: `probe134r4.py` and `.out` (sections A to D), `probe_b3.py` and `.out`, `mutate_r4.py` and `mutants.txt`, `leak138r2.py` and `.out` (also used for T-138), `unit_runs.txt`.

```json
{"card": "T-134", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive 4f416a4 (card commit; HEAD at start) and 2db6ad2 (HEAD at finish, same results): app/backend/trace.py, review.py, present.py, export_routes.py, tests/unit/test_t134_unconfirmed_edit.py, memory/contracts/api.md T-134 r4 paragraph; app/frontend/review.js and dom.js for the held-edit text; fixture backend; sample case evals/golden/sample.txt via TestClient; no served app, no browser",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-134-staff-engineer-r3.md, board show T-134 (7.4 note and card AC), memory/ORCHESTRATOR_DECISIONS.md D-058 via api.md row",
  "git show 4f416a4 (trace.py, present.py, export_routes.py, test file) in full; git diff 4f416a4 2db6ad2 on the in-scope files",
  ".venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t138_undo_edit.py on git archive 4f416a4: 37 passed; same on 2db6ad2: 37 passed",
  "regression modules test_trace, test_export, test_export_edge, test_review_rules, test_api_routes on 4f416a4 with one pre-existing red test deselected: 266 passed, 1 deselected; the red test alone on 4f416a4 and on 68b8685: 1 failed (assert ['e2', 'e4'] == [])",
  "probe134r4.py on 4f416a4 (sections A, B, C, D) and on 2db6ad2: outputs identical (artifacts/review-evidence/T-134/r4/probe134r4.out)",
  "probe_b3.py: candidate quotes for e3 with the AI summary kept: two 422, the AI's own quote 200 (probe_b3.out)",
  "mutate_r4.py on 4f416a4: N18, N19 (re-anchored), N21, N22, H2, P1 all KILLED (mutants.txt; the T-138 mutants A1, T3, T9, L1 are in the same log)",
  "mutate_r3.py N19 on 4f416a4: SKIP (anchor count 0), so the r3 N19 mutant no longer applies",
  "frontend grep: review.js:182-183 and :191 'stays blocked' / 'export stays blocked'; second_check_pending absent from app/frontend; dom.js:55 ZL.secondCheckPending inference; review.js:320 toCheck = ZL.editToCheck; review.js:342-344 edit-check-hint",
  "backend grep: 'stays blocked' in app/backend (trace.py:447 only, _code_check_gated at trace.py:432-435); judge_not_run_blockers trace.py:849-853",
  "pytest --collect-only on test_t134_unconfirmed_edit.py: 26 tests"
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
   "evidence": "tests/unit/test_t134_unconfirmed_edit.py:363 `edits: {'excerpt': QUOTE_ONLY.strip()}` with the comment 'another pick (a summary-safe variant of the quote)'. QUOTE_ONLY (line 257) equals the e3 AI excerpt in evals/golden/sample.txt:16 after strip (probe134r4.out B-setup: True). review.py:327 strips the excerpt, so the stored excerpt before and after the 'pick' is the same string (B1 and B2 lines). On this sample no other quote passes while the AI summary is kept: probe_b3.out shows 422, 422 and only the AI's own two-sentence quote with 200.",
   "why_it_matters": "The handoff says 'my test uses a valid variant' and the 7.4 item 2 asks for a valid re-picked quote. The behaviour is right: review.py:357 drops ladder.rejudge on every edit, and B2 shows the claim clears on an identical re-save. Mutant P1 (the pop removed) is killed by two tests, so the protection holds; the test name and comment describe a different quote than the one tested.",
   "fix": "Correct the comment and the handoff to say it is an identical-text re-save. Add a test that stores a different excerpt for e3 (direct DB write of the excerpt, as the T-138 tests do with _set_ladder, or a second sample record), re-picks it, and asserts the rerun claim is gone and the 422 text says Run the second check again.",
   "acceptance_test": "Unit: rerun no-answer on stored excerpt X, then a valid pick Y != X: blocker why and the 422 message contain no 'ran again' and contain 'Run the second check again'. P1 (review.py:357 pop removed) must fail it."},
  {"severity": "minor",
   "title": "api.md says the UI reads second_check_pending and shows why as given; neither is true at HEAD, and the 'same list as the gate' claim is a superset",
   "evidence": "memory/contracts/api.md:368: 'The UI uses this field instead of inferring it from ladder.judge or reasons' and 'Show why as given.' app/frontend has no reference to second_check_pending (probe134r4.out D2: 'frontend review.js reads second_check_pending: False'; grep -rn second_check_pending app/frontend returns 0 lines). dom.js:55 still infers the state. The same paragraph says the field is 'the same list the JUDGE_NOT_RUN gate reads'; judge_not_run_blockers (trace.py:849-853) also requires accepted or edited and not edit_unconfirmed, so the field is a superset of the gate's list.",
   "why_it_matters": "A contract that says the UI does something it does not is what the next worker builds on (the T-136 follow-up is exactly that). The superset point decides whether a 'second check pending' badge on an unaccepted quote re-pick is a bug or intended.",
   "fix": "Reword api.md:368: the field is set on every view; the frontend reads it when the T-136 card lands (state the current behaviour as a TODO, not as fact). State that the field is the unjudged list minus rates, a superset of the gate's blocker list.",
   "acceptance_test": "Doc check: the T-134 r4 paragraph says the UI reads the field only once app/frontend reads it (grep count is 0 at HEAD); a unit test asserts second_check_pending is True for an unaccepted quote re-pick, which documents the superset (test_second_check_pending_is_an_explicit_item_field already covers the true case)."},
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
