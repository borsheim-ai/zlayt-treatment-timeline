# T-179 staff-engineer review, round 2 (commit 619f283)

Verdict: pass (0 blockers, 0 majors, 3 minors).

The round-1 major is fixed and I proved it by mutation. The D-067 test now builds a stored, accepted two-sentence paragraph, has an `=1` control, and asserts with no if-guard. Forcing `narrative_in_letter()` to `return True` fails `test_an_accepted_paragraph_never_reaches_the_letter_the_notes_or_the_json` at test_d067_narrative_cut.py:58. The round-1 survivor M5 (amount `disagree` mapping removed) is now killed by two tests. The api.md order claims now match the code and are pinned by mutants.

Two things are not as the handoff and api.md state. The `compared` stamp is still a second commit after the accept commit. The "taken back" repair is a compensation, not a transaction. A concurrent reader sees the accepted item with no stamp. The api.md sentence "a disputed item is never accepted without the compare on record" is false for a reader in that window and for a process crash. The held-quote sleep from F5 is unchanged; the card said it was out of scope. All three are minors.

## What I ran (all from `git archive 619f283` in the scratchpad `T179_r2`, never the shared tree)
- `tests/unit`: 5830 passed, 8 skipped in 338.47s. This matches the handoff. Output: `artifacts/review-evidence/T-179-r2/unit_full.txt`.
- e2e with `E2E_REQUIRE_DB=1`, 29 spec files that touch accept, batch, review, charges, the letter or the stepper:
  - Group A (review_matrix, ladder_gate, charge_confirm, count_charge, edit_to_check, rerun_judge, code_check_refusal, held_quote_gate, letter_isolation, charges, api, edit): 130 passed in 211.77s.
  - Group B (stepper, suggestions, uncovered_ui, letter_matrix, mvp_finish, mvp_polish, polish_r3/r4/r5, keyboard_mobile, rerun_note, export_ui, change_the_quote, conflict_skipped, no_console_errors, multicase, journey_modes): 225 passed, 1 skipped in 323.14s. The skips in these files are data or mode dependent (`pytest.skip` for "library cases need ZLAYT_MODE=local" and "this backend verified the edit"); I did not identify which one fired.
  - Outputs: `e2e_a.txt`, `e2e_b.txt`. `test_held_quote_gate.py` passed inside group A, 1 run.
- Mutants on 12 archive copies, `artifacts/review-evidence/T-179-r2/mutants.py`, results in `mutants_out.txt`. Each mutant printed `occurrences=1 changed=True` before running.
  - Killed: M1 (D-067 gate forced on, 1 failed), M2 (gate on unless "0", 1 failed), M3 (compare check off, 6 failed), M4 (batch allows disputed, 1 failed), M5 (`v = v`, 2 failed), M6 (stamp written for an undisputed item, 1 failed), M7 (stamp never written, 6 failed), M8 (no take-back on stamp failure, 1 failed), M10 (compare before the code checks, 1 failed), M11 (confirm before compare, 1 failed), M12 (batch reason renamed, 1 failed).
  - **Survived**: M9 (`"edited": "edit"` removed from the take-back map), 14 passed.
  - My first M11 used the wrong key (`item.get("flag")`), so it was a no-op and survived; I fixed it to `ladder.confirm` and the rerun was killed. Both runs are in `mutants_out.txt`.
- `probe_window.py` (reader on a second connection inside the stamp call, stamp failure plus take-back failure, process kill between the two commits) and `probe_edited_takeback.py` (stamp failure on a disputed edited entry, with and without M9).
- Read: `git show 619f283` for review.py, api.md and both test files; `app/db/db.py:215-237` (`apply_review` commits at line 233); `review.py:260-282`, `:333-345`; `memory/ORCHESTRATOR_DECISIONS.md` D-066 and D-067.

## Round-1 findings, checked
- **F1 (major) D-067 test cannot fail: fixed.** The test drafts and accepts real sentences (`entry_id` e1 and e5), proves with `=1` that they are in the letter, then asserts absence from letter, notes and the export JSON with the env var removed. M1 and M2 both fail it.
- **F2 (minor) non-atomic stamp: improved, not fixed.** See finding 1 below.
- **F3 (minor) api.md order and "ignored": fixed.** The doc says code checks, then COMPARE_REQUIRED, then CONFIRM_REQUIRED; the stamp is written only for a disputed item. `test_a_disputed_flagged_charge_needs_both_statements_compare_first` pins the order (M11 killed) and `test_the_code_checks_refuse_before_the_compare` pins code-checks-first (M10 killed). The undisputed `compared:true` test (M6 killed) pins "no key written". The doc sentence about the stamp being "written together with the accept" is the part that is not true (finding 1).
- **F4 (minor) charge, amount and code-check tests: fixed.** The disputed amount with verdict `disagree` and no reasons returns 422 COMPARE_REQUIRED (M5 killed, M7 killed). The batch test now reads `rej == {"e2": "judge_disputed", "e3": "judge_disputed"}` with no `if`. M12 kills it.
- **F5 (minor) held-quote sleep: not addressed.** `tests/e2e/test_held_quote_gate.py:93` still has `page.wait_for_timeout(300)`, and the commit touches no e2e file. The handoff states this. Carried as finding 3.

## Findings
1. The compared stamp is a compensation, not a transaction, and the doc says otherwise (minor). `DB.apply_review` commits the accept at db.py:233, then `_record_compared` opens its own BEGIN/COMMIT (review.py:333-345). The probe shows what a second connection sees in between: `status accepted, events [('accept', None)]`. With the stamp failing and the take-back also failing: HTTP 500 and the item stays `accepted` with `[('accept', None)]`. With the process killed inside the stamp: exit 9, item `accepted`, no stamp, and nothing ever reconciles it. api.md:382 says "if the stamp cannot be written the accept is taken back ... so a disputed item is never accepted without the compare on record". That holds only for a stamp exception that is followed by a successful take-back.
2. The "edited" take-back path has no test (minor). M9 leaves 14 passed. The probe shows the difference: on a disputed edited entry with a failing stamp, HEAD returns the item to `edited` and M9 leaves it `accepted`. The `"edited": "edit"` entry is new in 619f283.
3. Held-quote e2e keeps a bare 300 ms sleep and an unrecorded flake (minor, carried from round 1). Still at test_held_quote_gate.py:93.

Separate "violates a constraint" from preference: findings 1 to 3 are not spec-constraint violations. D-066 says the confirm "is stored on the review event" and does not require a single transaction; round 1 named the take-back as an acceptable fix. Finding 1 is minor because the doc claims more than the code delivers and a real transaction is cheap. Findings 2 and 3 are test-proof gaps.

```json
{"card": "T-179", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 619f283 (app/backend/review.py, memory/contracts/api.md, tests/unit/test_d066_compare_confirm.py, tests/unit/test_d067_narrative_cut.py; app/db/db.py read for the transaction boundary); tests/unit full, 29 tests/e2e spec files; no app URL (private test servers); round-1 review reviews/T-179-staff-engineer.md",
 "exercised": [
  "python3 tools/board.py show T-179; read reviews/T-179-staff-engineer.md, the card handoff, the r1 memory notes, personas/staff-engineer.md, D-066 and D-067",
  "git show 619f283 -- app/backend/review.py memory/contracts/api.md tests/ (every changed line)",
  "git archive 619f283 into the scratchpad T179_r2; .venv/bin/python -m pytest tests/unit -q -> 5830 passed, 8 skipped in 338.47s (artifacts/review-evidence/T-179-r2/unit_full.txt)",
  "E2E_REQUIRE_DB=1 pytest from the archive: group A 12 files, 130 passed in 211.77s (e2e_a.txt); group B 17 files, 225 passed, 1 skipped in 323.14s (e2e_b.txt); test_held_quote_gate.py inside group A",
  "artifacts/review-evidence/T-179-r2/mutants.py: M1..M12 on archive copies, each mutant printed occurrences=1 changed=True; M1-M8, M10, M11 (second attempt), M12 killed, M9 survived; first M11 was a no-op and is recorded as such (mutants_out.txt)",
  "artifacts/review-evidence/T-179-r2/probe_window.py: second-connection snapshot between accept commit and stamp commit; stamp failure plus take-back failure; process kill inside the stamp",
  "artifacts/review-evidence/T-179-r2/probe_edited_takeback.py on the HEAD archive and on the M9 mutant copy",
  "read app/db/db.py:215-237 (apply_review commits at 233), review.py:260-282 and 333-345, api.md:382; grep wait_for_timeout in the archive's test_held_quote_gate.py"
 ],
 "verdict": "pass",
 "scores": {"d066_enforcement": 4, "d067_cut_in_code": 5, "d067_test_strength": 5, "audit_trail_atomicity": 3, "contract_doc_accuracy": 4, "changed_tests_not_weakened": 5},
 "findings": [
  {"severity": "minor", "title": "The compared stamp is a second commit with a compensating take-back, so the doc claim 'never accepted without the compare on record' is false for a concurrent reader and for a crash",
   "evidence": "app/db/db.py:233 apply_review COMMITs the accept; app/backend/review.py:260-265 then calls _record_compared (review.py:333-345, its own BEGIN/COMMIT) and _take_back on failure. probe_window.py A: a second connection inside the stamp call sees \"accepted\", events [('accept', None)]. B: stamp raises and the take-back's apply_review raises -> status 500, e3 review_status accepted, events [('accept', None)]. C: process killed inside the stamp (exit 9) -> e4 review_status accepted, events [('accept', None)], never reconciled. memory/contracts/api.md:382: 'if the stamp cannot be written the accept is taken back ... so a disputed item is never accepted without the compare on record'.",
   "why_it_matters": "D-066 puts the compare on the review event so the audit can show a human compared a disputed summary. In the window, and after a crash or a failed take-back, a disputed item sits accepted, countable and exportable, with no compare on record, and the doc tells a client that cannot happen. A compensating repair also fails exactly when the DB is failing, which is when it is needed.",
   "fix": "Write after.compared in the same transaction as the accept: let DB.apply_review take an optional dict that is merged into the after_json it already inserts (the single INSERT at db.py:231-232), so the status UPDATE and the stamp commit together. Then drop _record_compared and the take-back for compared. If that is not wanted, change the api.md sentence to say the stamp is written right after the accept and is repaired best-effort, and say what a reader can see in between.",
   "acceptance_test": "Unit test: patch the stamp path to raise and assert the item is pending and has zero accept events (with the stamp inside apply_review it cannot be accepted without it). A second-connection snapshot taken inside the call never sees an accepted disputed item whose accept event lacks compared. Re-run probe_window.py: A, B and C show no accepted item without a stamp."},
  {"severity": "minor", "title": "The edited-status take-back has no test: removing it leaves all 14 D-066/D-067 tests green",
   "evidence": "review.py:280 '{\"pending\": \"reset\", \"dismissed\": \"dismiss\", \"edited\": \"edit\"}'. Mutant M9 (drop the 'edited' entry) -> '14 passed' (mutants_out.txt). probe_edited_takeback.py: disputed edited entry, stamp raises -> HEAD 'http 500 after take-back: edited'; M9 'http 500 after take-back: accepted'.",
   "why_it_matters": "The 'edited' mapping is new in 619f283. Without a test, a refactor of _take_back can leave an edited disputed item accepted with no compare on record and nothing fails. test_a_failed_compared_stamp_takes_the_accept_back covers only the pending case.",
   "fix": "Parametrize test_a_failed_compared_stamp_takes_the_accept_back over the starting status: pending, dismissed, and edited (edit e2 to clean wording first, then dispute it, then accept with compared:true under the failing stamp) and assert the status returns to the starting one.",
   "acceptance_test": "Rerun mutants.py M9: a test fails."},
  {"severity": "minor", "title": "Round-1 F5 not addressed: test_held_quote_gate.py keeps a bare 300 ms sleep and the flake assertion is still unrecorded",
   "evidence": "tests/e2e/test_held_quote_gate.py:93 'panel.locator(\"summary\").first.click(); page.wait_for_timeout(300)' in the 619f283 archive. 'git diff --stat f17c991 619f283 -- tests/e2e' lists no changed file under tests/e2e other than the guided specs that belong to another card. The handoff says F5 is frontend or qa owned and not touched. The test passed in group A (130 passed).",
   "why_it_matters": "A fixed sleep on a UI toggle is the pattern that fails under load, and the card note still does not record which assertion timed out in the 430-test run, so the next red run is dismissed the same way. It is a test-owner item, not a backend regression.",
   "fix": "Replace the sleep with an expect on the panel content, set an explicit expect timeout on the case-rail waits, and open a qa card for it if it is not in this card's scope. Record the failing assertion and line next time it times out.",
   "acceptance_test": "grep -n 'wait_for_timeout' tests/e2e/test_held_quote_gate.py returns nothing and the file passes in the load recipe from reviews/T-179-staff-engineer.md."}
 ],
 "whats_right": [
  "The D-067 test now builds real accepted sentences, proves them present with a flag-on control, and fails under two different gate mutants (M1, M2).",
  "The new D-066 tests pin the refusal order from both sides: M10 (compare before code checks) and M11 (confirm before compare) are each killed, and M5 and the batch reason are now killed too.",
  "The compared stamp is written only for a real compare on a disputed item (M6 killed), so the audit no longer overstates what she was asked to do."
 ],
 "questions_for_chris": []}
```
