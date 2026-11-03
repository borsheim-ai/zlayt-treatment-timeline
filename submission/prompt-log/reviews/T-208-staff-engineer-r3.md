# T-208 staff-engineer review r3 (fix commit 8aa14e1)

**Verdict: pass.** No blocker, no major. The round-1 major (the translation label passes on an English letter) is fixed. Three round-1 minors and the nit are still open; they are minors, so they do not change the verdict. One new nit.

Reviewed sha: 8aa14e1, which is HEAD (`git rev-parse HEAD` printed `8aa14e1ecebed88c632204a914f252e26dea0c33`). Fix diff: `evals/letter_check.py` (+37 lines of the commit's added hunks) and `tests/unit/test_t208_ai_wording.py`. Nothing else changed.

Model: claude-sonnet-5-5.

Archive: `git archive 8aa14e1 | tar -x` into the scratchpad copy `.../scratchpad/T208_r3/clean`. Its file list equals `git ls-tree -r 8aa14e1` (3732 blobs; `diff` of the two sorted lists was empty). Note for the next reviewer: `python -I` ignores `PYTHONDONTWRITEBYTECODE`, so my first runs wrote 6 `__pycache__` dirs into the copy; I deleted them and used `-B` from then on. Evidence outputs, mutant maker (`mutate3.py`) and probe (`probe3.py`) are in `artifacts/review-evidence/T-208-r3/`.

## Brief results

1. **Major fixed.** The fix is `_label_with_quote` (`evals/letter_check.py`): the label is blanked only if the case has an "AI translation" entry (`letters_for` returns `translated_quotes`) and the label sits alone on the line under that quote (standard style) or after it on the same line (one-line style). Every other occurrence is scanned like any other "AI".
   - lib01 (English), the exact label under the TREATMENT heading (the round-1 repro): eval value 6, exit 1, all hits on `case_lib01_er_only_then_gap` (3 variants x 2 styles). Round 1 gave value 0.
   - lib01, the label in the accepted layout but under an English quote (standard: its own line under the Source line; one-line: after the quote): value 6, exit 1.
   - lib09 (has translated entries), an extra label under the English ED quote while the real label stays under the Spanish quote: value 6, exit 1, hits on lib09 only.
   - Clean tree, lib09: the label appears once per letter (6 letters: 3 variants x 2 styles), directly under the Spanish quote, `ai_hits 0` each (`s2_clean_lib09_label_lines.txt`, `s2b_lib09_letter.txt`). Passes with the label next to the translated quote.
   - Pure-function probe (11 cases, 0 differences): label before the quote, label plus trailing words, a blank line between quote and label, empty-string quote, and an empty quote list each fail; label under the translated quote (with and without a trailing newline, one-line style, two labels under two translated quotes) passes.
2. **`python -m evals.letter_check`** (via the `-I -B` launcher on the archive): `{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", ...}`, exit 0. Two runs give an identical first line; `FIXTURE_SET=curated` gives the same value.
3. **Matrix e2e**: `E2E_REQUIRE_DB=1 pytest tests/e2e/test_letter_matrix.py -q -rs` on the archive: 14 passed, 0 skipped. With the label put under the first quote of every letter (mutant `all_label_under_first_quote`): 11 failed, 3 passed, eval value 150. The matrix is unchanged by this commit and its cases are all English, so any label there fails.
4. **Unit**: `tests/unit/test_t208_ai_wording.py` on the archive: 16 passed. With `_label_with_quote` forced to return True: 3 failed (`test_mutant_label_on_an_english_letter_fails`, `test_label_away_from_the_translated_quote_fails`, `test_measure_fails_the_label_on_an_english_case_and_passes_it_on_a_translated_one`), so the binding tests do fail when the binding is removed.

Also checked: the fix adds no `except`, `float(`, `sleep(`, network or environment reads (read of the full `git show 8aa14e1 -- evals tests`).

## Round-1 findings, status

- Major 1 (allow-list not bound): **fixed**, as above.
- Minor 2 (eval report prints neither fixture set nor prepared count): **still open.** `main()` output keys are unchanged; `fixture_set` and `prepared_cases` are not in `evals/letter_check.py`. The card handoff says "Minors 2-5 not in this round's brief; still open".
- Minor 3 (pattern misses LLM, GPT, A.I., zero-width, fullwidth): **still open.** `probe3.py`: LLM, GPT-4, "A.I.", a zero-width space inside AI, fullwidth AI, Gemini and "chatbot" are all NOT FLAGGED (`s8_probe3_clean.txt`). `AI_WORDING` is unchanged. The AC names the regex literally, so the AC is met.
- Minor 4 (matrix covers 10 of 25 letters): **still open.** `CASES` in `tests/e2e/test_letter_matrix.py` is unchanged (diff vs 8aa14e1 is empty). With a label under an English quote on lib01, the matrix still passes 14 (`s7_matrix_lib01_label.txt`); only the eval catches it.
- Nit 5 (handoff said 12 unit tests, file had 13): moot; the new handoff says 16 and 16 reproduces. The old note stays in the append-only log.

## New nit

`letters_for` building `translated_quotes` has no unit test. Mutant `lc_no_translated_quotes` (always `[]`): unit 16 passed, but the eval fails with value 6 on lib09 (`s5_eval_lc_no_translated_quotes.txt`), so the gate still catches it. Not a verdict factor.

## Not run

The full `tests/unit` and e2e suites; only the T-208 files and the letter matrix were in scope. CRLF line endings: a label with CRLF fails closed (INFO line in `s8_probe3_clean.txt`); the product emits LF.

```json
{"card": "T-208", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "fix commit 8aa14e1 (= HEAD) on top of b96c08f: evals/letter_check.py, tests/unit/test_t208_ai_wording.py; git archive 8aa14e1 copy (3732 blobs, file list equals git ls-tree); fixture backend; sample, case_lib01, case_lib09",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-208-staff-engineer-r2.md (round-1 record), the T-208 reviewer memory note, board show T-208 (AC, notes, handoff)",
  "git show 8aa14e1 -- evals tests (full diff); git rev-parse HEAD = 8aa14e1ecebed88c632204a914f252e26dea0c33; added hunks contain no except, float(, sleep(, network or env reads",
  "git archive 8aa14e1 | tar -x into scratchpad T208_r3/clean; sorted file list equals git ls-tree -r --name-only 8aa14e1 (empty diff, 3732 blobs); removed 6 __pycache__ dirs written by my own -I runs and used -B afterwards",
  "brief: .venv/bin/python -I run_module.py <clean> evals.letter_check -> value 0, cases 25, exit 0; run twice, identical; FIXTURE_SET=curated same value (s1_eval.txt, s1_eval2.txt)",
  "clean lib09 letters via letters_for: label count 1 per letter in all 6 (variant x style), translated_quotes 3, ai_hits 0; label printed directly under the Spanish quote (s2_clean_lib09_label_lines.txt, s2b_lib09_letter.txt)",
  "mutate3.py mutants, each anchor asserted to match once: lib01_label_in_treatment -> eval value 6 exit 1 (s5_eval_lib01_label_in_treatment.txt); lib01_label_under_english_quote -> value 6 exit 1; lib09_extra_label_under_english_quote -> value 6 exit 1, hits on lib09 only; all_label_under_first_quote -> value 150, matrix e2e 11 failed 3 passed (s7_matrix_all_label.txt)",
  "check-removal mutants: lc_label_with_quote_true -> unit 3 failed 13 passed, eval value 0 (s6_unit_lc_label_with_quote_true.txt); lc_no_translated_quotes -> unit 16 passed, eval value 6 exit 1 (s6_unit_lc_no_translated_quotes.txt, s5_eval_lc_no_translated_quotes.txt)",
  "probe3.py on clean: 11 label-binding cases, 0 differences; pattern-gap probes LLM, GPT-4, A.I., zero-width, fullwidth, Gemini, chatbot all NOT FLAGGED (s8_probe3_clean.txt)",
  "unit: pytest tests/unit/test_t208_ai_wording.py -q on the archive -> 16 passed (s3_unit_clean.txt)",
  "matrix e2e: E2E_REQUIRE_DB=1 pytest tests/e2e/test_letter_matrix.py -q -rs on the archive -> 14 passed, 0 skipped (s4_matrix_clean.txt); with lib01_label_under_english_quote -> 14 passed (s7_matrix_lib01_label.txt)",
  "status of round-1 minors: grep of evals/letter_check.py for fixture_set and prepared_cases (absent); git diff --stat 8aa14e1 -- tests/e2e/test_letter_matrix.py (empty); CASES line at tests/e2e/test_letter_matrix.py:21",
  "self-check of this file with artifacts/review-evidence/T-208-r3/check_review.py and board.py validate (results below in the run log, not in this record)"],
 "verdict": "pass",
 "scores": {"ac_literal_met": 4, "allow_list_binding": 5, "mutation_resistance": 4, "determinism": 5, "evidence_accuracy": 5},
 "findings": [
  {"severity": "minor", "title": "Eval report still prints neither the fixture set nor the prepared-kind count (round-1 minor 2, open)",
   "evidence": "evals/letter_check.py main() output on 8aa14e1: {\"value\": 0, \"cases\": 25, \"held_out_entries\": 11, \"backend\": \"fixture\", \"r_ids\": [...]}; grep for fixture_set and prepared_cases in evals/letter_check.py finds nothing. Card handoff: 'Minors 2-5 not in this round's brief; still open'.",
   "why_it_matters": "With FIXTURE_SET unset all 25 cases run as recorded-kind; the card says 'sample prepared-kind' and the report cannot show which ran. The letter scan itself does not branch on kind, so this is an evidence-trail gap.",
   "fix": "Return fixture_set and prepared_cases from measure() and print them in main(), or name FIXTURE_SET=curated in the gate command.",
   "acceptance_test": "FIXTURE_SET=curated python -m evals.letter_check prints fixture_set curated and prepared_cases 1; unset prints recorded and 0."},
  {"severity": "minor", "title": "AI/model pattern still misses LLM, GPT, A.I., zero-width and fullwidth forms (round-1 minor 3, open)",
   "evidence": "artifacts/review-evidence/T-208-r3/s8_probe3_clean.txt: GAP-PROBE 'LLM', 'GPT-4', 'A.I.', 'zero-width in AI', 'fullwidth AI', 'Gemini', 'chatbot' all NOT FLAGGED. Pattern at evals/letter_check.py:91 is unchanged.",
   "why_it_matters": "The AC names the regex literally and the code matches it, so the AC is met; but a letter saying 'Drafted by an LLM' passes the eval, the unit suite and the matrix.",
   "fix": "Add LLM, GPT and A.I. to the pattern; NFKC-normalise and strip U+200B, U+200C, U+200D, U+2060, U+FEFF before the scan. Keep the AC regex as a subset.",
   "acceptance_test": "PLANTED in tests/unit/test_t208_ai_wording.py gains 'Drafted by an LLM.', 'Drafted with GPT-4.', 'Drafted by an A.I. tool.' and a zero-width-space AI; each fails the scan."},
  {"severity": "minor", "title": "E2E matrix still covers 10 of 25 letters; library letters including lib09 are guarded only by the eval (round-1 minor 4, open)",
   "evidence": "tests/e2e/test_letter_matrix.py:21 CASES = sample.txt + case_01..09 (unchanged by 8aa14e1). Mutant lib01_label_under_english_quote: matrix 14 passed (s7_matrix_lib01_label.txt) while the eval fails with value 6 (s5_eval_lib01_label_under_english_quote.txt).",
   "why_it_matters": "A regression reaching only library letters is caught by one command, the eval, which the e2e gate does not run.",
   "fix": "Add case_lib01 and case_lib09 to the matrix via evals.letter_check.cases(), or state in the test docstring that library letters are gated by the eval.",
   "acceptance_test": "The lib01_label_under_english_quote mutant makes the matrix test for case_lib01 fail under E2E_REQUIRE_DB=1."},
  {"severity": "nit", "title": "translated_quotes producer in letters_for has no unit test; only the eval covers it",
   "evidence": "Mutant lc_no_translated_quotes (translated_quotes always []): tests/unit/test_t208_ai_wording.py 16 passed (s6_unit_lc_no_translated_quotes.txt); the eval fails value 6 on lib09 (s5_eval_lc_no_translated_quotes.txt).",
   "why_it_matters": "The positive path (lib09 still passes with its label) is proven by the eval alone; the unit tests stub letters_for.",
   "fix": "Optional: a unit test that builds the lib09 case and asserts translated_quotes is non-empty and each quote appears in the letter beside the label.",
   "acceptance_test": "The lc_no_translated_quotes mutant fails at least one unit test."}
 ],
 "whats_right": [
  "The exemption is bound to the case's translated quotes and the label's position; 4 binding mutants (heading, English quote x2 styles, extra label on lib09) all fail the eval, and forcing the check to True fails 3 unit tests.",
  "lib09 still passes with its label directly under the Spanish quote in all 6 variant x style letters, and the eval output is identical across two runs.",
  "The new tests assert behaviour (hit lists and measure() value 0 versus 6), not internals; the matrix e2e (14 passed, 0 skipped) and a label-everywhere mutant (11 failed) agree."],
 "questions_for_chris": [
  "Should the carrier letter keep the bracketed '[AI translation of the Spanish original; check before sending]' label at all? The orchestrator kept it under D-042/D-050 while the card AC says no AI wording in any letter. This review rates the exemption's scope, not that product and legal call."]}
```

Corrections appended after writing: the first paragraph says 37 added lines in evals/letter_check.py; the commit adds 36 there (the count of 37 included the diff header). The last exercised entry says validator results are in a run log: check_review.py reported review ok and board.py validate reported ok (208 file(s)) after writing.
