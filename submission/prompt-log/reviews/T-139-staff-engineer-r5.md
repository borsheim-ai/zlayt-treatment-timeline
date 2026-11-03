# T-139 — staff-engineer-reviewer, round 5 (last scoped check, commit ea988f8)

**Verdict: pass.** 0 blockers, 0 majors, 2 minors. Everything the brief asked for held on a clean `git archive HEAD` copy (HEAD `ea988f8`, checked with `git log --oneline`).

**Deterministic checks (archive tree, `.venv/bin/python`):**
- Full `pytest tests/unit -q -p no:cacheprovider`: **5047 passed, 8 skipped** (273 s). This is the final code, not the worker's number.
- `python -m evals.letter_check`: `{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture"}`.
- `tests/unit/test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte` passes (24 passed in the file). I also checked a live export of the sample (all accepted, fixture backend): its BILLED CHARGES section equals the golden byte for byte. The treatment lines differ from the golden only in fixture wording ("41-year-old male ..."), which comes from the fixture backend and not from this commit.
- `python -m app.pipeline evals/golden/sample.txt` run twice: output identical (`cmp`).

**The six word summaries (adjuster r4).** Live app on port 7893 (`LLM_BACKEND=fixture`, scratch DB), sample case, `new_edits_r5.txt`:
- 'ambulance copay of twenty', 'deductible of five hundred', 'patient spent fifteen hundred out of pocket', 'lost eighteen hundred in wages', 'patient responsibility twelve hundred', 'paid in full twenty-one fifty' each return **422** at edit time. The message names the expression, for example "(paid in full twenty-one fifty)". The three digit forms from r4 (coinsurance 430.00, reimbursed 1,412.50, MRI cost the patient 2,150) are also refused.
- Past the edit check: I stored the six directly in the DB. The trace gate went `ready:false` with `money_in_letter: 6`, six MONEY_IN_LETTER blockers naming line 4/8/12/20/28/32 and the entry. GET /export returned 422 `export_blocked` in all three styles, with six money blockers each. After restoring, gate ready and export 200 in all styles (`gate_words.json`: `ready_equals_allowed` true in all three states).

**'(ins paid $1,412.50)' and siblings (Billed charges section).** I rewrote record 8's sentence in a case dict built by `store.export_case` and ran the production gate, `build_export` in both styles, and `evals.letter_check.violations` (`cl.py`, `cl2.py`, `cl3.py`, 24 sentences):
- 'Charge: $2,150 (ins paid $1,412.50).' becomes the quote `"Charge: $2,150"`. The same trim happens for 'less $737.50 contractual adjustment', 'patient responsibility 1,200.00', 'paid in full 2,150.00', 'lost wages 1,800.00', 'allowed 1,412.50, write-off 737.50', the number-word variants, and 'Charge: $2,150 - paid 1,412.50'.
- 'Insurer paid $1,412.50 on a charge of $2,150.' and 'Ins paid $1,412.50 (charge: $2,150).' have no clean clause: the gate returns a MONEY_IN_LETTER blocker naming the charge line and both styles return 422.
- In every sentence the gate verdict and the export result agree (`agree_standard`, `agree_oneline` true), and the letter eval reports nothing on the exported letters.

**Mutation spot-check (scratch copies, not committed).** `groups = []` in `letter_money_blockers`: 7 tests in `test_t139_r5.py` fail. Disabling `_foreign_money` in `_amount_quote`: 14 fail. Dropping `_SPOKEN_BEFORE`: 3 fail. All three die.

**False-positive differential (HEAD vs HEAD~1 archives, `fp.py`).** Of 30 clinical or neutral phrases, only 'reimbursed two hundred', 'reimbursement twelve hundred', 'lost twelve hundred', 'Net due 737.50' gained a hit (all money), plus the contrived 'Lost 150 words'. 'Lost 15 lbs', 'Lost 200 ml', 'spent twenty minutes', 'allowed two visits' stay quiet.

**Scope cut 7c.** The row (slang, bare decimals, per-mile rates, accepted) still states what is not caught. The r5 forms are now covered, so the row's "amounts in words are caught" sentence is true for the labelled forms tested. Slang stays out of scope; I did not rate it.

```json
{"card": "T-139", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit ea988f8 (HEAD), git archive copy in session scratchpad t139r5/; app http://127.0.0.1:7893 (LLM_BACKEND=fixture, ZLAYT_MODE=local, scratch ZLAYT_DB); sample case; record-8 sentence variants through production functions on a store.export_case dict",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-139-claims-adjuster-r4.md, python3 tools/board.py show T-139 (r5 handoff and orchestrator last-fix note), memory/SCOPE_CUTS.md row 7c",
  "git log --oneline (HEAD ea988f8); git show HEAD -- app/backend/export.py app/backend/money.py read in full",
  "git archive HEAD into scratchpad t139r5/; pytest tests/unit -q -p no:cacheprovider -> 5047 passed, 8 skipped",
  "python -m evals.letter_check on the archive -> value 0, cases 25",
  "pytest tests/unit/test_export.py -> 24 passed (byte-for-byte golden test); live sample export vs evals/golden/sample.export.expected.txt: BILLED CHARGES section equal, treatment wording differs only by fixture backend",
  "python -m app.pipeline evals/golden/sample.txt twice, cmp -> identical",
  "started app on PORT 7893 from the archive tree; GET /api/health; claims-adjuster edit_attack_r4.py with new_edits.json (9 summary edits, accept all, trace gate, GET /export x3) -> new_edits_r5.txt: 9 x 422, exports 200 and clean",
  "g1.py (gate_vs_export with the six word summaries stored directly in the scratch DB): gate ready false, money_in_letter 6, three styles 422; restored -> ready, 200 -> gate_words.json",
  "cl.py, cl2.py, cl3.py: 24 charge-sentence variants incl. '(ins paid $1,412.50)' through money_blockers_for_case, build_export (standard + oneline), letter_check.violations -> charge_line*.json",
  "fp.py: 30 clinical/neutral phrases through money.strings on HEAD and HEAD~1 archives, diffed -> fp_head.txt, fp_prev.txt",
  "mutants on scratch copies (groups=[] ; _foreign_money disabled ; _SPOKEN_BEFORE dropped) run against test_t139_r5/r4/letter_eval: 7, 14 and 3 failures",
  "kill of the server (PID from lsof on 7893, confirmed the command line first); lsof re-check"],
 "verdict": "pass",
 "scores": {"determinism": 5, "honest_failure": 5, "test_strength": 4, "gate_eval_agreement": 4, "code_clarity": 4},
 "findings": [
  {"severity": "minor",
   "title": "A charge quote can be cut inside a parenthesis, leaving an unbalanced quote",
   "evidence": "artifacts/review-evidence/t139_staff_r5/charge_line2.json: record sentence 'Charge: $2,150 (paid by insurer, copay of twenty).' -> BILLED CHARGES line 'Source [Ex. __ / Bates __]: \"Charge: $2,150 (paid by insurer\"'. Cause: app/backend/export.py _clauses splits on ';' and ',' without regard to an open parenthesis, so the first candidate that is free of other money ends at the comma inside '(...)'.",
   "why_it_matters": "The text is still a verbatim substring of the record and carries no amount, so nothing false reaches the letter. But the carrier sees a quote that stops mid-parenthesis and states a payment fact ('paid by insurer') the trim was meant to remove, with no amount.",
   "fix": "In _clauses, do not break at ',' or ';' inside an open '(': drop a candidate that has an unmatched '(' and fall through to the next one (then to the 'cut before the parenthesis' candidate, which gives 'Charge: $2,150').",
   "acceptance_test": "UT: charge sentence 'Charge: $2,150 (paid by insurer, copay of twenty).' -> the quote line is 'Charge: $2,150' or the export blocks; no quote ends with an unmatched '('."},
  {"severity": "minor",
   "title": "The new Billed-charges gate rule has no case in the letter eval corpus, and the eval's section rule is still the pre-r5 one",
   "evidence": "Handoff: 'evals/letter_check section rule is the pre-r5 one (qa-owned, still agrees on corpus)'. python -m evals.letter_check -> {\"value\": 0, \"cases\": 25}; none of the 25 cases has a second money expression in a charge sentence, so the 0 does not exercise the r5 path. The r5 gate behaviour is pinned only by tests/unit/test_t139_r5.py (the mutants above die there, not in the eval).",
   "why_it_matters": "The card's own promise is one detector with no divergence between the gate and the eval. They share money.py, but the section structure is coded twice, and the eval cannot catch a regression of the charge-line trim because the corpus never reaches it. The eval is the check that runs on every prompt or model change.",
   "fix": "Add one corpus case (or a fixture record in an existing case) whose accepted charge sentence carries '(ins paid $X)' and assert letter_check reports 0 with the trimmed quote; give qa a card to move the eval's section rule to the same header/quote-line grouping as export._charge_groups, with a test that both reject the same synthetic letters.",
   "acceptance_test": "Mutant: `groups = []` in export.letter_money_blockers or disabling _foreign_money in _amount_quote makes python -m evals.letter_check report value > 0, not only the unit tests."}
 ],
 "whats_right": [
  "The gate and the export agree in every state tried (clean, six word summaries stored past the edit check, restored, 24 charge-sentence variants), and the MONEY_IN_LETTER blocker names the line, the entry or charge, and the expression.",
  "The charge-line trim stays word for word from the record ('Charge: $2,150'), and when no clean clause exists the export blocks instead of guessing.",
  "Three targeted mutants (charge-section scan, foreign-money trim, number words before a label) each fail 3 to 14 tests; the full unit suite is green on the final code (5047 passed)."],
 "questions_for_chris": []}
```
