# T-139 — staff-engineer-reviewer (round 1: commits 5f7ef96, 184cbb7, ba82071)

**Verdict: fail** (2 blockers, 2 majors, 4 minors).

Scope: `git archive ba82071` and `git archive 2db6ad2` (HEAD moved to 2db6ad2 while I worked; 2db6ad2 is T-146 r2 and carries the missing `why.join`)
extracted into the session scratchpad (`T139_r1/tree`, `T139_r1/head`). The card has since moved to round 2 (4abec86) and a second dispatch is
pending; I did not review 4abec86, I only spot-checked it (see the end). Probe scripts and outputs are in `artifacts/review-evidence/T-139/`.

Deterministic results:
- `pytest tests/unit -q` on the ba82071 archive: **286 failed, 3488 passed, 8 skipped, 103 errors** (`AttributeError: module 'app.backend.why' has no attribute 'join'`, `generator.py:169`). `python -m app.pipeline evals/golden/sample.txt` crashes with the same error.
- Same suite on the 2db6ad2 archive: **3893 passed, 8 skipped**. `python -m evals.letter_check`: `{"value": 0, "cases": 25, "held_out_entries": 9}`. `evals.run --backend fixture` row `letter_currency_outside_charges ... | 0 |`.
- Held-out recorded entries: 9 (case_03 e2, case_09 e2, lib06 e4, lib09 e7, lib11 e9, lib12 e10, lib14 e8, lib15 e7 and e9), matching the handoff.

What I verified by the brief's list:
- **CHARGE_TEXT_IN_ENTRY** holds out an entry whose letter text carries a `$` figure (accept 422, export filter `in_entries`, `verify` reason). Mutants M7, M8, M10 killed.
- **narrow_excerpt** drops only start or end sentences. I replayed all 25 cases: 42 narrowed entries, 42 of 42 kept quotes are contiguous runs of the original's sentences and substrings of it. Mutants M1 (middle amount), M2 (stub guard), M3 (rung-1 re-run) killed.
- **Judge on the narrowed pair**: test and replay agree; 39 verified, one real `JUDGE_UNSUPPORTED` (lib10 e4).
- **41 new recordings**: all `claude-cli` / `claude-haiku-5-5`, timestamps 13:32:12 to 13:33:36 at 1 to 5 s intervals, one `unsupported` verdict among them; all 41 keys are read by the 25-case replay (probe_orphans.py); `test_curated_fixtures.py` passes. Provenance rests on the file metadata and on the replay, not on a call log I could check.
- **Letter**: 0 violations over 25 cases, but see F2 (blind to money without `$`), F6 (words, non-USD) and F7 (partition).
- **Bills to request**: dismissed charges are absent (M9 killed), but the plaintiff's law firm is still listed (F3).

```json
{"card": "T-139", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commits 5f7ef96, 184cbb7, ba82071 (git archive ba82071, and git archive 2db6ad2 because HEAD moved) in the session scratchpad; fixture backend, no network; sample + 9 golden + 15 library cases",
 "exercised": [
  "Read personas/staff-engineer.md, reviews/GATE-M2-claims-adjuster.md, board.py show T-139 (notes, handoff), D-019, D-044, D-054, D-056, D-058",
  "git show of 5f7ef96, 184cbb7, ba82071 (charge_text, generator, export, review, why, letter_check, run.py, tests)",
  "pytest tests/unit -q on git archive ba82071: 286 failed, 3488 passed, 8 skipped, 103 errors; python -m app.pipeline evals/golden/sample.txt crashes with AttributeError why.join",
  "pytest tests/unit -q on git archive 2db6ad2: 3893 passed, 8 skipped; python -m evals.letter_check: value 0, 25 cases, 9 held; python -m evals.run --backend fixture: letter row 0",
  "probe_narrowed.py: replay of 25 cases, 42 narrowed entries, substring + contiguous-sentence check, dropped sentences listed, odd-ending scan",
  "probe_orphans.py: 45 files added in 184cbb7, 41 judge keys read by the replay; metadata, timestamps and verdict spread of all 49 fixtures added by 5f7ef96 and 184cbb7",
  "tests/unit/test_curated_fixtures.py (passes in both full runs)",
  "mut.py with 16 mutants over charge_text, generator, export, review (M1 to M16) and M11 over 9 review/edit test files",
  "probe_cur.py: currency_strings and LC.violations on amounts in words, euro/pound/CAD, '$' mid-quote, OCR '$1,2OO', claim-form figures",
  "probe_letter.py and probe_bills.py: lib01, lib10, lib11, lib14 letters and internal notes, BILLS TO REQUEST for every case in both variants",
  "probe_part.py: LC.violations on a letter whose first quote contains the words BILLED CHARGES",
  "probe_edge.py: generator.extract_one on eight crafted records (hedge in the dropped sentence, semicolon clause, Dr. abbreviation, euro, words, negation)",
  "Spot-check of git archive 4abec86 (r2): detector and lib10/lib11/lib14 letters; not a review of r2"
 ],
 "verdict": "fail",
 "scores": {"deterministic_boundary": 3, "failure_visibility": 3, "test_strength": 4, "commit_integrity": 1, "eval_independence": 2},
 "findings": [
  {"severity": "blocker",
   "title": "The committed T-139 range cannot run a case: generator calls why.join, which is not in any T-139 commit",
   "evidence": "git archive ba82071 -> `python -m app.pipeline evals/golden/sample.txt` ends 'generator.py\", line 169, in compose: e[\"why\"] = why.join(reasons, lad.get(\"judge\")) ... AttributeError: module 'app.backend.why' has no attribute 'join''. `pytest tests/unit -q` on that archive: 286 failed, 3488 passed, 8 skipped, 103 errors (every test that runs the pipeline errors; first is tests/unit/test_amounts_t140.py::test_lib11_accept_all_export_total_is_6000, status 'failed' at stage 'extract'). `git log -S'why.join'` -> 184cbb7 added the call to generator.py; why.join itself arrived in 2db6ad2 (T-146 r2). Worker handoff counted 3887 passed from a dirty working tree.",
   "why_it_matters": "A swept-in hunk from another card's uncommitted work makes the delivered commits unusable: no extract, no letter, no CLI. The handoff's 'full unit 3887 pass' described the working tree, not the commits. It is repaired at 2db6ad2 only because a different card landed later.",
   "fix": "Re-state the T-139 range with the dependency: either add 2db6ad2 to the card's commits and record that T-139 requires it, or rebase the generator hunk so each commit passes alone. Re-run the T-139 tests and letter_check from a clean git archive of the final sha, not the working tree.",
   "acceptance_test": "`git archive <final sha> | tar -x -C <empty dir>`; there `pytest tests/unit -q` has 0 failed and 0 errors, and `python -m app.pipeline evals/golden/sample.txt` exits 0. Quote the counts in the handoff."},
  {"severity": "blocker",
   "title": "Claim-form money without a '$' reaches the carrier letter, and letter_check reports 0 over 25 cases",
   "evidence": "git archive 2db6ad2 (same code as ba82071), probe_letter.py case_lib10_eob_ub04_cms1500, letter_text: 'Claim lists CPT 99204, 18500, 1 unit; CPT 20610, 21000, 1 unit; CPT 97110, 96 OO, 4 units; total charge 49100; amount paid 0 00.' and 'Source ...: \"Item 24F lines: ... Item 28 TOTAL CHARGE 49100. Item 29 AMOUNT PAID 0 00.\"'. case_lib14_handwritten_chiro_scans, letter_text: 'Claim line 1: 092126 to 092326, CPT 98941, 24F 25500, 24G 3. ... Item 28 total charge 33000.' `python -m evals.letter_check` -> {\"value\": 0, \"cases\": 25}. Cause: charge_text.currency_strings (charge_text.py:19, amounts._AMT amounts.py:10) needs a '$', 'dollars' or 'USD'; probe_cur.py: 'TOTAL CHARGE 49100' -> [], 'AMOUNT PAID 0 00' -> [], 'FL47 total charges 4920' -> []. Same defect class the card exists to close (claims-adjuster GATE-M2 blocker; D-019, R-CH-7).",
   "why_it_matters": "A charge total, line charges and a paid amount ($491.00, $330.00) are in the carrier letter, outside the total line and not in BILLED CHARGES, while the eval gate that was added for exactly this says 0. AC 3 is green for the wrong reason. The cases are in the golden/library set the check walks, so the eval measured them and could not see them.",
   "fix": "Hold out (or narrow) entries whose quote or summary has a money field without '$': a money word (charge, charges, fee, cost, paid, balance, billed, rate, estimate, total) followed by a figure, CMS-1500 24F / Item 28-30, UB-04 FL47. Give letter_check its own detector, independent of the one the pipeline uses, so a shared blind spot cannot pass.",
   "acceptance_test": "UT: currency_strings or the new money check flags 'Item 28 TOTAL CHARGE 49100', 'AMOUNT PAID 0 00', '24F 25500', 'FL47 total charges 4920' and not 'Pain 7/10; ibuprofen 600 mg; 35 mph; approx. 40%; 3 days of work'. letter_check on lib10 and lib14 exits non-zero with the ba82071 code and 0 with the fix."},
  {"severity": "major",
   "title": "'Bills to request' still lists the plaintiff's own law firm (and a carrier) as a bill to request",
   "evidence": "probe_bills.py on 2db6ad2: case_lib11_priors_and_ledger -> 'BILLS TO REQUEST ... - Dr. Hesper Alderton; Ashgrove Fire-Rescue run report; Pellingham and Rook PLLC.' (record 4 is the firm's letter of protection, evals/library/case_lib11_priors_and_ledger.txt). case_lib12_records_review_credibility -> '... Marlowe Assurance Group.' (record 9 is the carrier's records-review letter). export._bills (export.py:510) only subtracts paid and dismissed providers. Card note 13:03:01Z (orchestrator): 'Bills to request must not list the plaintiff's own law firm (lib11); only treating providers/facilities.' No T-139 test covers it (grep 'law firm' tests/unit/test_t139*.py: none).",
   "why_it_matters": "The firm is told to request a bill from itself and from the adversary. It is internal notes only, so no fact reaches the carrier, but the list is the paralegal's to-do and the card named this case.",
   "fix": "List only providers whose entry is clinical: exclude correspondence, letter-of-protection and carrier/EOB sources by record kind or a closed source-pattern list.",
   "acceptance_test": "UT/E2E on lib11 and lib12: BILLS TO REQUEST contains no 'Pellingham and Rook PLLC' and no 'Marlowe Assurance Group' and still lists the treating providers without an accepted charge."},
  {"severity": "major",
   "title": "Code shortens the model's quote and strips summary clauses, and nothing shows it to the paralegal",
   "evidence": "grep -rn excerpt_narrowed app: written at generator.py:94 and read nowhere; app/backend/trace.py:355-364 renders only ladder.summary_trim. probe_narrowed.py: 42 entries had quotes shortened and 25 had summary clauses removed ('summary_removed': ['ED charge $3,915', ...]); an entry like sample e2 now quotes a different text than the generator returned. Handoff says 'trace/UI should show ladder.excerpt_narrowed (trace.py not mine; frontend)' and leaves it open. D-054 precedent: 'the removal is shown in the item trace'.",
   "why_it_matters": "Audit trail: a deterministic edit of LLM output on 42 of 241 entries leaves a record only in the ladder JSON. A reviewer debugging 'why does the quote end here' cannot find it in the trace the app serves. D-044/D-058 reasoning (the judge saw the narrowed pair) cannot be followed from the UI either.",
   "fix": "Add a code step to trace.py for entries with ladder.excerpt_narrowed: 'Code dropped the sentence(s) that state an amount', with the dropped sentences and the removed summary clauses, plus a test on the served trace.",
   "acceptance_test": "UT: for a narrowed entry, GET .../items/{id}/trace has a step whose detail contains the dropped sentence text; removing the trace step turns the test red."},
  {"severity": "minor",
   "title": "The edit-time charge check in review._check_summary has no test",
   "evidence": "Mutant M11 (muts2.json): replace `if found:` at review.py:284 with `if False:`; tests/unit/test_api_routes.py, test_lib09_t110.py, test_narrative.py, test_trace.py, test_manual_and_split.py, test_review_rules.py, test_t134_unconfirmed_edit.py, test_t138_undo_edit.py, test_t139_charge_text.py: 373 passed. The accept guard (M10) and the export filter (M8) are both killed, so no amount reaches the letter; the edit-time refusal and its message are unpinned.",
   "why_it_matters": "A later edit of that function can drop the edit-time 422 and no test notices; she would then find out only at accept.",
   "fix": "Add a test: PATCH edit that puts '$140' in the summary or the quote returns 422 invalid_edit with reason CHARGE_TEXT_IN_ENTRY and stores nothing.",
   "acceptance_test": "M11 is killed by a named test."},
  {"severity": "minor",
   "title": "letter_check splits the letter at the first occurrence of the words BILLED CHARGES, so a quote that contains them blinds the entry check",
   "evidence": "evals/letter_check.py:38 `letter.partition(CHARGES)`. probe_part.py: a letter whose first quote reads \"BILLED CHARGES are on the statement.\" and whose second entry says 'Charge per visit $185.' returns [] from LC.violations(letter, [18500]); the same letter with the quote in lower case returns two 'treatment text states $185' violations.",
   "why_it_matters": "An all-caps 'BILLED CHARGES' heading is plausible on a billing statement. The eval that is supposed to be independent of the pipeline's hold can be passed by the text it checks.",
   "fix": "Split on the section header line (a line equal to BILLED CHARGES at line start, after the last chronology entry), not on a substring.",
   "acceptance_test": "UT: the letter above returns the 'treatment text states $185' violation."},
  {"severity": "minor",
   "title": "Amounts written in words and non-USD currencies are not currency strings for the hold or for the eval",
   "evidence": "probe_cur.py on 2db6ad2: 'Charge per visit one hundred forty dollars.' -> [], 'fee of €140' -> [], 'fee of £120' -> [], 'fee of CAD 140' -> [], 'fee 140 euros' -> []. probe_edge.py: summary 'Pain 5/10; fee €140.' over quote 'Pain 5/10. Fee €140.' comes out state=verified, reasons=[] and would reach the letter. '$' mid-quote ('said it cost $400 out of pocket'), 'C$140', 'USD 140', '140 dollars', OCR '$1,2OO' are caught.",
   "why_it_matters": "The rule is no currency in the letter. The synthetic corpus does not contain these forms today, so letter_check is honest at 25 cases, but a record that spells an amount out passes the hold, the eval, and amounts.py extraction alike.",
   "fix": "Either extend the detector to number words followed by dollars/cents and to € £ ¥ CAD/EUR/GBP, or write the closed-world assumption (USD figures with a $) into docs/LLM_VS_CODE.md and SCOPE_CUTS.md.",
   "acceptance_test": "UT rows for the forms above; or a SCOPE_CUTS row naming them."},
  {"severity": "minor",
   "title": "A narrowed quote can be half a real sentence and end at ';' because the shared splitter treats ';' as a sentence end",
   "evidence": "probe_edge.py: record 'Plan: PT three times weekly; charge $95 per visit.' with summary 'Plan of care PT three times weekly.' -> state=verified, excerpt='Plan: PT three times weekly;', dropped=['charge $95 per visit.']. In the recorded corpus no kept quote ends outside . ! ? (probe_narrowed2 scan: 0 of 42), so this is a live-model risk, not a current one. narrow_excerpt docstring promises 'whole sentences'.",
   "why_it_matters": "The carrier letter would print a quote that stops mid-sentence at a semicolon. It is verbatim and the judge ran on it, but it is not a whole sentence as the card's wording requires.",
   "fix": "In narrow_excerpt, split on . ! ? only (or refuse to narrow when the kept run does not end in a sentence terminator).",
   "acceptance_test": "UT: narrow_excerpt('Plan: PT three times weekly; charge $95 per visit.') is None or keeps the whole sentence's currency clause out of the hold path."}
 ],
 "whats_right": [
  "narrow_excerpt is tight: 42 of 42 narrowed recorded quotes are contiguous, verbatim, whole-sentence runs with the dropped sentences kept in ladder for audit; mutants on the middle-amount rule, the stub guard and the rung-1 re-run are all killed.",
  "The 41 new judge answers are real claude-cli recordings (one is an honest 'unsupported'), all are read by the replay, and test_curated_fixtures.py stays green with an empty allow-list.",
  "Dismissed charges are absent from the letter and from Bills to request in all 25 cases, and mutants that remove the export filter, the accept guard or the dismissed-provider rule are killed."
 ],
 "questions_for_chris": []}
```

Note on round 2: a spot-check of `git archive 4abec86` shows `evals.letter_check` value 0 over 25 cases with 11 entries held, `currency_strings('TOTAL CHARGE 49100')` now returns a hit, and the lib14 claim-form text appears only in internal notes. That targets F2 and F3 but I did not review it; the pending round-2 dispatch should.

Errata (same reviewer, count corrections only; the file is write-once): in finding 4, "42 of 241 entries" should read "42 of 177 entries" (177 = entries across the 25-case replay), and "25 had summary clauses removed" should read "30 had summary clauses removed" (summary_removed non-empty, counted from probe_narrowed.py output). Severity and verdict are unchanged.
