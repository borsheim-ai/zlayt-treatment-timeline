# T-179 staff-engineer review (commit f17c991)

Verdict: changes (0 blockers, 1 major, 4 minors).

The behaviour is right. D-066 is enforced in `review.set_review`, the batch refuses disputed items all-or-nothing, and the narrative is cut from the letter, the notes and the JSON export. The one major is about the proof, not the code. The only test of the D-067 default never runs its assertions, and flipping the gate to always-on leaves every test green.

## What I ran (all from `git archive f17c991`, never the shared tree)
- `tests/unit`: 5825 passed, 8 skipped in 350.16s. This matches the card's 5825.
- Mutants on a copy of the archive (`artifacts/review-evidence/T-179-r1/mutants.py`).
  - Killed: M2 (compare check off), M3 (batch allows disputed), M4 (compared not recorded), M6 (reasons fallback removed), M7 (verdict path removed).
  - **Survived**: M1 (narrative gate forced on, 9 passed) and M5 (amount `disagree` mapping removed, 145 passed).
- Probes: `probe.py`, `probe_narrative.py` and `probe_charge_order.py` in the same folder.
- `tests/e2e/test_held_quote_gate.py`: 7/7 solo (21s). Then 6 concurrent runs, and 4 concurrent runs with 24 busy loops at load average 39 on 12 cores: 10 of 10 runs passed, 70 tests, 25 to 35s each.

## The five checks
1. **422 COMPARE_REQUIRED and the confirm on the accept event: holds.** Without `compared:true` the response is 422, nothing is written and there are no accept events. With it the event carries `after.compared.at`, and `/audit` shows it. The probe also confirms the 422 for the reason-only and verdict-only cases.
2. **Batch refuses disputed items: holds.** A batch of `[e5, e4]` where e4 is disputed returns 422 `judge_disputed`, and the clean e5 stays pending (all or nothing). The disputed check runs ahead of `not_pending`, so an already-accepted disputed item is also refused.
3. **Narrative cannot reach the letter or the notes: correct in code, not proven by the committed test.**
   - `probe_narrative.py` drafts two real sentences and accepts the paragraph.
   - With the env var unset there is no `TREATMENT SUMMARY` in the letter, no `DRAFT TREATMENT` in the notes, and no sentence text anywhere in the `export_payload` JSON (keys: counts, generated_at, internal_notes_text, items, letter_text, token, warnings).
   - With `NARRATIVE_IN_LETTER=1` all three appear (the control).
   - `GET /api/cases/{tok}` has no `narrative` key.
   - The committed D-067 test proves none of this (F1).
4. **The 12 changed accept tests are not weakened.** Every edit adds `"compared": True`. `test_t134` gains a 422-then-200 pair, so it is stronger. `test_narrative.py` and one trace test get `NARRATIVE_IN_LETTER=1` so they still exercise the flagged-on path. The deleted e2e narrative-stepper test is replaced by a no-narrative-control check. One side effect: the blanket `compared:True` in `_accept_all` and similar helpers means those tests no longer cover accept-without-compare on charges (F3).
5. **`test_held_quote_gate` flake: load, not a data race, but unproven.** I could not reproduce it in 77 runs of the test body. Each pytest run starts a private server and DB. The waits are DOM-state waits (`expect` and `wait_for_function`), not time guesses. The `_held` helper asserts `second_check_pending` only after `data-review=accepted`, so the server has committed. The only bare sleep is `wait_for_timeout(300)` at line 93, and a native `<details>` toggles synchronously, so it is harmless. The likeliest cause is a fixed budget (Playwright's 5s `expect` default) under the suite's load. The card does not record which assertion timed out (F5).

## Findings
F1 (major): the D-067 default-off test cannot fail. F2 to F5 (minor): non-atomic record of `compared`, doc and code disagreement on error order and on `compared` for undisputed items, untested charge and amount paths, and the unrecorded flake.

```json
{"card": "T-179", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive f17c991 (app/backend/review.py, case_extras.py, export.py, present.py, memory/contracts/api.md, 25 changed files); tests/unit full, tests/e2e/test_held_quote_gate.py; no app URL (private test servers); sample case plus the D-059 NOTE case; guided UI is T-181 and was not graded",
 "exercised": [
  "python3 tools/board.py show T-179; read D-066 and D-067 in memory/ORCHESTRATOR_DECISIONS.md; read reviews/GATE-M3-round1-triage.md",
  "git show f17c991 (app/backend, memory/contracts/api.md, every changed test file)",
  "git archive f17c991 into the scratchpad T179_r1; .venv/bin/python -m pytest tests/unit -q -> 5825 passed, 8 skipped in 350.16s",
  "artifacts/review-evidence/T-179-r1/mutants.py: M1..M7 on archive copies (each mutant's occurrence count printed as 1 and changed=True before running); M1 and M5 survive, the others fail a test",
  "artifacts/review-evidence/T-179-r1/probe.py: undisputed accept with compared:true, fault injection on _record_compared, batch with an already-accepted disputed item, narrative draft and accept then the export JSON",
  "artifacts/review-evidence/T-179-r1/probe_narrative.py: two real drafted sentences accepted, build_export and export_payload with NARRATIVE_IN_LETTER unset and =1",
  "artifacts/review-evidence/T-179-r1/probe_charge_order.py: disputed flagged charge, which 422 comes first, both statements on one accept event",
  "E2E_REQUIRE_DB=1 pytest tests/e2e/test_held_quote_gate.py from the archive: 1 solo run, 6 concurrent runs, 4 concurrent runs under 24 busy loops (load average 39); 11 of 11 passed (output in held_load_*.txt and held_load2_*.txt)",
  "grep of app/backend for narrative, apply_review callers, JUDGE_ reason codes; read review.py 236-360, case_extras.py 33-60, export.py 125-160, export_routes.py, db.apply_review"
 ],
 "verdict": "changes",
 "scores": {"d066_enforcement": 4, "d067_cut_in_code": 5, "d067_test_strength": 2, "audit_trail": 3, "contract_doc_accuracy": 3, "changed_tests_not_weakened": 4},
 "findings": [
  {"severity": "major", "title": "The D-067 default-off test cannot fail: forcing the narrative gate on leaves all tests green",
   "evidence": "tests/unit/test_d067_narrative_cut.py:42 'if d.status_code == 200 and d.json()[\"narrative\"].get(\"sentences\"):' guards the accept step. Under FIXTURE_SET=curated the draft returns 0 sentences (probe.py printed 'draft 200 0', then 'accept 422'), so the narrative is never accepted. Line 46 asserts re.search(r'draft paragraph', notes, re.I), but the notes heading is 'DRAFT TREATMENT PARAGRAPH', which that pattern does not match. Mutant M1 (export.py narrative_in_letter returns True) -> 'tests/unit/test_d066_compare_confirm.py tests/unit/test_d067_narrative_cut.py: 9 passed'. test_narrative.py runs with NARRATIVE_IN_LETTER=1 (autouse), so it does not cover the default either. The production code is right (probe_narrative.py: env unset -> letter has no TREATMENT SUMMARY, notes have no DRAFT TREATMENT; env=1 -> both present), so this is a proof gap, not a leak.",
   "why_it_matters": "D-067 and AC 1 say the paragraph never reaches the letter. The only default-path test passes whether the gate exists or not, so a future edit that drops the gate or flips the default would ship an unevaluated paragraph with no quote and no Bates placeholder into a demand letter, which D-002 rules out.",
   "fix": "In test_d067_narrative_cut.py build a stored, ACCEPTED narrative with real sentences (as test_narrative.accepted_sample plus narr(GOOD) do) with NARRATIVE_IN_LETTER unset. Assert without any if-guard: no 'TREATMENT SUMMARY' in letter_text, no 'DRAFT TREATMENT' in internal_notes_text, and none of the sentence texts in json.dumps(export_payload). Add the =1 control in the same test so it proves the paragraph was there to be cut. Drop the status-code branch.",
   "acceptance_test": "Rerun mutants.py M1 (narrative_in_letter returns True): the new test fails. Unmutated: it passes with the sentences present under env=1."},
  {"severity": "minor", "title": "'compared' is written after the accept, outside any transaction; a failure leaves a disputed item accepted with no compare on record",
   "evidence": "app/backend/review.py:352-353 calls _record_compared after set_review returns; _record_compared (review.py:321) is a separate autocommit UPDATE on review_events. probe.py with _record_compared raising: 'status 500', 'e3 review_status accepted', 'e3 accept events [(accept, None)]'. The sibling _record_confirm (review.py:225-235) wraps its two writes in BEGIN/COMMIT and T-159 r2 takes the accept back if it fails.",
   "why_it_matters": "The whole point of D-066 is that the compare is on the record. In this window the item is in the letter and the audit shows no compare, and the paralegal sees a 500. A retry self-heals (a second accept event gets the stamp), so it is not silent, but the invariant is best-effort.",
   "fix": "Write after.compared inside the same DB.apply_review transaction (pass it into the event) or, as _record_confirm does, take the accept back when the stamp write fails.",
   "acceptance_test": "A unit test patches _record_compared to raise: the item is not left accepted (review_status back to pending) or the accept event already carries compared. It fails on f17c991."},
  {"severity": "minor", "title": "api.md states two behaviours the code does not have",
   "evidence": "memory/contracts/api.md:382 says 'the charge confirm (D-059) refuse first' and that compared 'is ignored ... for an item nobody disputed'. probe_charge_order.py on a disputed flagged charge: accept {} -> COMPARE_REQUIRED; {compared:true} -> CONFIRM_REQUIRED; {confirm} -> COMPARE_REQUIRED. So compare is checked before the confirm (review.py:252 sits before the amount branch). probe.py A: accept of undisputed e1 with compared:true -> 200 and the event stores [{'at': ...}], i.e. it is recorded, not ignored (review.py:352 stores whenever compared is True).",
   "why_it_matters": "A client written from the contract expects CONFIRM_REQUIRED first and no compared stamp on an undisputed accept. The audit would also show 'compared' on items nobody disputed, which overstates what she was asked to do.",
   "fix": "Either change the doc to the real order and drop the 'ignored' claim, or move compare_error after confirm_error and record compared only when judge_dispute(item) is set. Prefer the code change for the stamp, so only a real compare appears in the audit.",
   "acceptance_test": "Unit tests: (a) a disputed flagged charge with neither statement returns the order the doc names; (b) accept with compared:true on an undisputed entry writes no 'compared' key."},
  {"severity": "minor", "title": "Disputed charge and amount accepts, and the code-check-first order, have no direct test",
   "evidence": "Mutant M5 (review.py:304 'v = \"disagrees\" if v == \"disagree\" else v' -> 'v = v') -> '145 passed' across test_d066, test_d067, test_amounts_t140, test_t171_count_charge and test_t139_charge_text. Only entries are covered by test_d066_compare_confirm.py; the charge and amount tests were changed to always send compared:true, so none asserts 422 COMPARE_REQUIRED for an amount. api.md:382 also claims a failing code check stays CODE_CHECK_FAILED; no test sets a failing code check on a disputed entry. test_d066 batch test: 'if rej:' at the end makes the reason check conditional.",
   "why_it_matters": "The amount judge is the one that says 'disagree'; its mapping is the line D-066's note 'lib11 amounts all carry JUDGE_DISAGREES' relies on. Only the redundant reasons fallback keeps it working today.",
   "fix": "Add: a disputed amount with verdict 'disagree' and empty state_reasons -> 422 COMPARE_REQUIRED; a disputed entry whose summary fails a code check -> 422 CODE_CHECK_FAILED (not COMPARE_REQUIRED); make the batch test assert the rejected reasons unconditionally.",
   "acceptance_test": "Rerun mutants.py M5: a test fails."},
  {"severity": "minor", "title": "The held-quote flake is not diagnosed in the evidence, and the test has one bare sleep",
   "evidence": "Card AC 1 evidence: 'the 1 timeout, test_held_quote_gate, passes alone 7/7' with no assertion or line. tests/e2e/test_held_quote_gate.py:93 'panel.locator(\"summary\").first.click(); page.wait_for_timeout(300)'. I could not reproduce: held_load_*.txt and held_load2_*.txt, 10 concurrent runs at load average up to 39, all '7 passed'.",
   "why_it_matters": "'Passes alone' says nothing about whether a real race exists. My reading from the code is load against fixed budgets, not a race, but with the failing assertion unrecorded it stays a guess, and the next red run will be dismissed the same way.",
   "fix": "Replace the 300 ms sleep with an expect on the panel content, and set an explicit expect timeout (for example 15 s) on the case-rail waits. When a run times out again, record the assertion and line in the card note.",
   "acceptance_test": "grep -n 'wait_for_timeout' tests/e2e/test_held_quote_gate.py returns nothing; the file passes 10 of 10 under the load recipe in held_load2."}
 ],
 "whats_right": [
  "D-066 lives in the one choke point (set_review) and also in the batch validator, so a disputed accept is refused whichever route it takes; the all-or-nothing batch result was confirmed by probe.",
  "The D-067 gate sits in the export view, so the letter, the internal notes and the JSON payload (which is built from the same builder) all lose the paragraph together, and it works with real accepted sentences.",
  "The 12 edited accept tests only add compared:true; test_t134 gained a 422 assertion, so no assertion was lost."
 ],
 "questions_for_chris": []}
```
