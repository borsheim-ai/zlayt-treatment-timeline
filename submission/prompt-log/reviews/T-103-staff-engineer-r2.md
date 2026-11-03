# T-103 staff-engineer review, r2 (commit bcdcb91)

Reviewer: staff-engineer-reviewer. Model: claude-haiku-5-5 (as dispatched). CLAUDE.md §6 and D-024 call for Sonnet on engineering reviewers; flagged, not changed (same as r1).

**Verdict: changes.** No blockers. One major carried from r1: a rate row's running balance is still only inside its verbatim excerpt, and the oracle passes it through a whole-row exemption. Three minors and one nit.

**Pin.** `git rev-parse HEAD` returned bcdcb919f1723f51579db03d9426443860a91680 at review start. HEAD later moved to c2a5d1f (T-106), with 3462ad0 (T-104) between. `git diff --stat bcdcb91 HEAD -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md` is empty, so the three reviewed files are identical at HEAD. Scripts and mutants ran on `git archive bcdcb91` in the scratchpad. Evidence: artifacts/review-evidence/T-103-r2/ (RUN_ORDER.txt lists every command).

**The four checks you asked for.**
1. Per-service sums and EOB-versus-ledger checks are gone: met. `grep -rn "LEDGER_EOB\|_sum(\|_tot(\|payer_reports\|BALANCE_STEP\|balance_convention\|stated_totals" app/ tests/unit/test_billing.py memory/contracts/api.md` on the archive returns only the absence assertions (test_billing.py:77, 132-133, 277, 795) and the "Removed by D-052" line (api.md:695). The one `_sum` hit is an unrelated function at app/backend/export.py:229. The r1 control (EOB 140.00 against ledger 130.00) now gives `checks: []` on the EOB row and no check anywhere (r1_reprobe_output.txt).
2. An EOB amount with no cents appears as a line or as unreconciled: met. "$140", "$130", "1O0.00", a bare "130" and "130.5" each produce an EOB line (class unclear, detail eob) with the text in `unclear` and `checks: [LINE_UNCLEAR]`. `unaccounted` is empty for each (r1_reprobe_output.txt).
3. The fail-safe accounting test covers EOB records and fails when a token is dropped: met for code-level drops (mutation_results_r2.txt, scratch copies). R01, the EOB unreadable figure's `unclear` list emptied at billing.py:531: 7 failed. R04, the first EOB column dropped at billing.py:529: 4 failed. R03, the EOB accounting pass off at billing.py:779: 2 failed. R05, R01 plus R03: 19 failed. The one survivor is R02, EOB unparsed rows dropped at billing.py:764 (`got = rows_ + unp_` to `got = rows_`), printed TOTAL row included: 179 passed. The accounting pass re-lists that TOTAL row's seven figures as an unreconciled eob row (r2_survivor_and_m2_check_output.txt), so nothing is lost. That is redundancy, not a gap. The in-test EOB fail-safe at test_billing.py:804 edits the analysed output, so it proves the oracle; the production-path proof is R01 and R04.
4. The route output has no total-like fields: met. route_keys_output.txt covers four responses (sample, case_03_rate_and_ocr, case_09_nonvisit_hides_gap, and a synthetic EOB $140 case). Each returns HTTP 200 with top-level keys `citation_failures, lines, rules, skipped_records, status, unreconciled`. No key path on any of them matches total, sum, complete, balance_convention, stated, providers, payer, ledger or matched. Per-line printed figures (`billed`, `paid`, `balance`, `eob.*`) remain. They are per line, not totals. The sample returns `none_found`, so it adds nothing beyond the top-level keys.

**Pytest.** `.venv/bin/python -m pytest -q tests/unit/test_billing.py` in the project worktree: 179 passed in 1.04s (pytest_billing_HEAD_bcdcb91.txt). The same command on the archive copy with `-I`: 179 passed in 0.93s (pytest_billing_archive_bcdcb91.txt). r1 recorded 157.

**Status of the r1 findings.**
- r1 B1 (EOB money token lost): resolved. See check 2.
- r1 B2 (per-service sums on payer checks): resolved. See check 1.
- r1 M1 (silent skip on an unreadable figure): resolved. The `continue` is gone. The same-service unreadable ledger row "130" now carries LINE_UNCLEAR on its own row (r1_reprobe_output.txt).
- r1 M2 (rate-row running balance only in the excerpt): open. Finding F1.
- r1 M3 (fail-safe cannot fail for EOB rows): resolved for EOB (R01 red). The rate whole-row exemption remains (F1).
- r1 M4 (docs versus code on balance checks): resolved. billing.py:5 says "no balance step check", and api.md:664 says "no running-balance step check".
- r1 m1 (detail carries two kinds): open, and `eob` is now another detail value. Finding F4.
- r1 nit (figure fields on extra lines): resolved. api.md:692 says they are never summed or compared by a client.

**Mutant coverage (r1 set re-run on the r2 code, mutation_results_r1_set_on_r2.txt).** M01 6 failed, M02 13, M03 8, M05 65, M07 16, M08 4. M04 and M06 report NOT APPLIED because their anchors moved. R07 (unreconciled list dropped, 78 failed) and R01 (EOB unclear dropped, 7 failed) are their equivalents on the r2 code.

**Not exercised.** The full tests/unit suite. The app over HTTP (TestClient only). The D-019 accepted total was not re-run; `git show --stat bcdcb91` lists only the three billing files, so totals.py, present.py and api.py are untouched. tests/unit/test_t093_eval_signature.py (unrelated, red at 841be23 per r1) was not re-run.

```json
{"card": "T-103", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git commit bcdcb91 (fix(backend): billing applies D-052 strictly, T-103 r2): app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md; scratch copy of git archive bcdcb91; project worktree (HEAD later c2a5d1f, billing files identical to bcdcb91); billing route via TestClient on evals/golden sample, case_03_rate_and_ocr, case_09_nonvisit_hides_gap and a synthetic EOB $140 case; no app URL exercised",
 "exercised": [
   "git rev-parse HEAD -> bcdcb919f1723f51579db03d9426443860a91680 at review start; git log later showed c2a5d1f (T-106) and 3462ad0 (T-104) above it",
   "git show --stat bcdcb91 -> app/backend/billing.py, memory/contracts/api.md, tests/unit/test_billing.py (3 files, 204 insertions, 138 deletions)",
   "git diff --stat bcdcb91 HEAD -- the three files -> empty; git status --short on the three files -> empty",
   "git diff 2dc5be2 bcdcb91 on the three files: every hunk read",
   ".venv/bin/python -m pytest -q tests/unit/test_billing.py in the project worktree -> 179 passed in 1.04s",
   "git archive bcdcb91 into a scratchpad copy; .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py on the copy -> 179 passed in 0.93s",
   "r1_reprobe.py on the copy (r1_reprobe_output.txt): EOB 97110 billed $140 against ledger 130.00; control 140.00; EOB figures $130, 1O0.00, bare 130, 130.5; same-service unreadable ledger row (bare 130) with EOB 130.00; rate row 'Charge per visit 185.00 999.00'; (class, detail) pairs over PROBES",
   "r2_survivor_and_m2_check.py on the copy and on mutant R02 (r2_survivor_and_m2_check_output.txt): the printed TOTAL row re-listed as an unreconciled eob row; rate line keys and figure",
   "route_keys.py (route_keys_output.txt): billing route via TestClient, fixture backend, ingest only, on evals/golden sample.txt, case_03_rate_and_ocr.txt, case_09_nonvisit_hides_gap.txt and a synthetic EOB $140 case; every key path searched for total-like names",
   "run_mutants_r2.py on scratch copies (mutation_results_r2.txt): R01 to R09 and T01, full file and -k 'eob or probe or property or bare or oracle' selections",
   "run_mutants.py from the r1 folder on the r2 copy (mutation_results_r1_set_on_r2.txt): M01 to M08; M04 and M06 not applied (anchors moved)",
   "pytest -k table_rate_no_cents on mutant T01 (T01_table_rate_no_cents_failure.txt): assert [('315.00', ...)] == []",
   "grep on the copy for LEDGER_EOB, _sum(, _tot(, payer_reports, BALANCE_STEP, balance_convention, stated_totals (grep_removed_names_bcdcb91.txt); grep of billing.py and the test module for float(, except, sleep(, random, and network or model imports",
   "read billing.py 166-182, 509-533, 558-565, 646-673, 690-727, 804-812 and the module docstring; test_billing.py helpers 73-115, oracle 565-611, PROBES 653-735, EOB tests 776-826, property test 1052-1103; memory/contracts/api.md 663-695; memory/ORCHESTRATOR_DECISIONS.md line 60 (D-052)"
 ],
 "verdict": "changes",
 "scores": {"fail_safe_completeness": 4, "decision_D052_conformance": 4, "honest_failure_no_silent_skip": 5, "api_doc_matches_code": 4, "money_integer_cents": 5, "no_llm_in_deterministic_path": 5, "test_mutation_catch": 4, "D019_total_unchanged": 5},
 "findings": [
   {"severity": "major",
    "title": "Rate-row running balance is still only inside its excerpt; the oracle's whole-row exemption is what passes it (r1 M2, not fixed at bcdcb91)",
    "evidence": "r1_reprobe_output.txt and r2_survivor_and_m2_check_output.txt: row 'Charge per visit 185.00 999.00' gives one line, class rate, figure 185.00, and no balance field; '999.00' occurs only in the excerpt. app/backend/billing.py:649 whole = [x['excerpt'].strip() for x in list(rates) + list(lop)] and tests/unit/test_billing.py:570 _WHOLE_ROW = ('rate', 'estimate', 'reduction', 'lien_amount', 'asserted_balance') are unchanged in bcdcb91. T01_table_rate_no_cents_failure.txt: with 'rate' removed from _WHOLE_ROW, table_rate_no_cents fails with assert [('315.00', ...)] == [].",
    "why_it_matters": "The running balance is a printed money token that a paralegal can only find inside the verbatim text. api.md:692 says a running balance is listed beside the lines, but on a rate row it is not a figure field of any line. The oracle accepts it only because the whole row is exempt. This is the r1 blind spot again, through the rate path, and it is the one r1 finding bcdcb91 leaves open.",
    "fix": "Carry the rate row's running balance as a figure of the rate line (an unclear figure with its text, or a separate cited line with class unclear), then remove 'rate' from _WHOLE_ROW. Update api.md:692 to name the field that carries it.",
    "acceptance_test": "For 'Charge per visit 185.00 999.00', '999.00' sits in a structured field of the output and not only in excerpt or cites; tests/unit/test_billing.py passes with 'rate' removed from _WHOLE_ROW; a mutant that drops that field turns the probe red."},
   {"severity": "minor",
    "title": "Comparisons remain under the strict reading of 'no sums or comparisons of any kind' (D-052 text itself does not name comparisons)",
    "evidence": "app/backend/billing.py:808 ... (l['billed']['cents'] or 0) < 0 sets detail 'reversal' (a sign test on a money figure). billing.py:696-698 _line_key includes billed, paid and adjustment cents; billing.py:701-717 _merge_duplicates merges a repeated line on equality of that key. billing.py:662 it[1] == key and billing.py:725-727 _listed_elsewhere compare figure text to decide whether a token is placed. None of these produces a sum, a total, a shown verdict or a disagreement check. memory/ORCHESTRATOR_DECISIONS.md:60 forbids totals and a complete badge and does not mention comparisons.",
    "why_it_matters": "The round's standard is no sums or comparisons of any kind. These are comparisons of money values (a sign test, equality on cents) and of token text. None of them violates the D-052 text, so this is minor here; it becomes major if Chris reads the standard as covering them.",
    "fix": "If the strict reading applies: classify reversal from the credit notation in the excerpt (parentheses or a trailing minus), and key duplicate merging on the record's own excerpt text, not on cents. If it does not apply: record the ruling under D-052 in memory/ORCHESTRATOR_DECISIONS.md so the next review does not re-raise it.",
    "acceptance_test": "Chris's ruling is recorded. If strict: no money comparison remains in billing.py, and a test pins 'reversal' from a parenthesised figure without a sign comparison."},
   {"severity": "minor",
    "title": "Stale comment and docstring wording name the removed provider-completeness state",
    "evidence": "app/backend/billing.py:563 '...the provider of such a line is complete: false.' (no complete field exists; tests/unit/test_billing.py:77 lists 'complete' in _GONE). billing.py:170 'the provider is incomplete'; billing.py:180 'the provider is incomplete, and the figure is not left only in a field nobody opens'.",
    "why_it_matters": "A reader who greps for 'complete: false' finds a comment about a flag that D-052 removed. 'Provider is incomplete' brings back the completeness state the decision retired. This is docs-versus-code drift of the kind r1 flagged.",
    "fix": "Reword the three comments to say the figure is listed on its own line and that no provider completeness is claimed.",
    "acceptance_test": "grep for 'complete: false' and 'provider is incomplete' in app/backend/billing.py returns nothing; the module docstring and api.md agree on the same wording."},
   {"severity": "minor",
    "title": "detail carries several kinds of thing (r1 m1, carried; 'eob' is now one more value)",
    "evidence": "r1_reprobe_output.txt, (class, detail) pairs over PROBES: (charge, reversal), (unclear, eob), (rate, rate), (unclear, asserted_balance), (unclear, stated_total_billed), (unclear, balance_forward), (unclear, None) and others. app/backend/billing.py:808-809 computes detail from form, sign, description and balance.",
    "why_it_matters": "A client has to branch on detail strings that mean different things: why a ledger row is listed, and what kind of extra line this is. The eob value adds a third meaning without a separate field.",
    "fix": "As r1 proposed: a closed kind list for what the line is, and a separate reason for why it is listed. Document both in api.md.",
    "acceptance_test": "Every line has a kind from a closed list, and a test pins that list."},
   {"severity": "nit",
    "title": "The in-test EOB fail-safe proves the oracle by editing the output, not the production path",
    "evidence": "tests/unit/test_billing.py:804 test_eob_fail_safe_names_a_figure_dropped_from_a_row... deletes keys from the analysed output (del _eob_line(out)['eob'][k]; _eob_line(out)['unclear'] = []) and asserts the oracle names them. The production-path proof is R01 and R04 in mutation_results_r2.txt.",
    "why_it_matters": "The test is correct as an oracle test, but it does not run a changed parser. The parametrized test at tests/unit/test_billing.py:781 does exercise the parser's unclear path and catches R01, which is why this is only a nit.",
    "fix": "Optional: add one test that patches the EOB parser's unclear list to empty and asserts the oracle names the figure.",
    "acceptance_test": "Optional; the mutant R01 stays red."}
 ],
 "whats_right": [
   "EOB money tokens sit on their rows: '$140', '1O0.00', bare '130' and '130.5' each stay as text on the EOB line, and the oracle names nothing unaccounted (r1_reprobe_output.txt).",
   "No sums, payer checks or ledger comparisons remain: the 140.00 control raises no check, and no total-like key appears in any of the four route responses (route_keys_output.txt, grep_removed_names_bcdcb91.txt).",
   "The EOB fail-safe is caught at the code level: R01, R03, R04 and R05 turn 7, 2, 4 and 19 tests red; the r1 M01, M02, M03, M05, M07 and M08 mutants stay red on the r2 code."
 ],
 "questions_for_chris": [
   "Does 'no sums or comparisons of any kind' (the standard for this round) cover the reversal sign test (billing.py:808), the duplicate-line equality on cents (billing.py:696-717) and the text identity in the accounting net (billing.py:662, 725-727)? I read D-052 as not covering them, so they are minor (F2). If the strict reading applies they are major.",
   "For F1: may a rate row's running balance stay as cited excerpt text only (the bcdcb91 reading), or must it be a figure field (the r1 proposal)? The answer decides whether F1 closes without a code change."
 ]}
```
