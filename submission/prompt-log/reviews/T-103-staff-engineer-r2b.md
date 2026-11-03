# T-103 staff-engineer review, r2b (commit bcdcb91): supersedes reviews/T-103-staff-engineer-r2.md

Reviewer: staff-engineer-reviewer. Model: claude-haiku-5-5. CLAUDE.md §6 and D-024 call for Sonnet on engineering reviewers; flagged, not changed (same as r1).

**Verdict: fail.** One blocker, found after the r2 file was written: identical rows from two different providers are merged into one line, so one provider's charge disappears from the listing. Record this file, not r2.

**Why r2 is superseded.** reviews/T-103-staff-engineer-r2.md gives verdict changes with no blocker. That verdict is wrong because of B1 below. Three statements in it also need correcting:
1. Exercised: "git diff 2dc5be2 bcdcb91 on the three files: every hunk read" was overstated when written. The api.md and test-file diffs were persisted and only partly shown. Both are now read in full. The commit's own api.md change is two hunks: the billing route-table row (line 36) and the billing section (lines 661-699). The other api.md hunks in the 2dc5be2..bcdcb91 range come from 1335f21 and faee448, other cards. test_billing.py: every hunk of the commit read; no new finding there.
2. F2 said the D-052 text does not name comparisons. That is true of memory/ORCHESTRATOR_DECISIONS.md:60 only. memory/contracts/api.md:664 says "No sums and no comparisons of any kind (D-052, applied strictly in T-103 r2)". F2 below is updated.
3. Check 1 said the one `_sum` hit is "an unrelated function". It is `def _summary_line` at app/backend/export.py:229, a prefix match of `def _sum`. Nothing is affected.

**B1 (blocker): two providers' identical rows merge into one line.** Probe: artifacts/review-evidence/T-103-r2/merge_cross_provider_probe.py; output merge_cross_provider_probe_output.txt. Record 1 is Larkspur Hollow Physical Therapy and record 2 is Medlark Clinic. Both carry the same row `06/10/26 06/11/26 97110 Therapeutic exercise 130.00 130.00`. The output has one charge line for 97110, provider Larkspur Hollow Physical Therapy, record_nos [1, 2], billed 13000. Medlark's record produces only its four printed-total lines; its 97110 charge has no line of its own.

Cause: app/backend/billing.py:696-698 `_line_key` has no provider. billing.py:701-717 `_merge_duplicates` merges a later-record line whose key matches (merge condition at 706-707). The provider is assigned at billing.py:802-803, before the merge at 804. The key is the same at the parent commit (`git show 2dc5be2:app/backend/billing.py`, lines 683-685), so this predates bcdcb91. The identical-copy test at tests/unit/test_billing.py:995-998 puts the same provider in both records, so no test can see it. Persona checklist item 19 requires the dedupe key to include source and provider.

Why it matters: D-052's reason for a listing is that a listing cannot hide a missing line (api.md:664). Here a second provider's charge is hidden inside another provider's line, and the line attributes the charge only to Larkspur. That loses a fact, which is a blocker under D.2.

Fix: include the provider in the merge key. Merge only the same provider's re-sent statement (byte-identical excerpt, same provider and form). Otherwise keep both lines.

Acceptance: a test with Larkspur and Medlark carrying the same row gives two 97110 charge lines, one per provider, each with its own record_no. The same-provider re-sent test (test_billing.py:995) still gives one line citing both records. A mutant that removes the provider from `_line_key` turns the new test red.

**The rest of r2, updated.**
- Checks 1-4 of r2 (sums and EOB checks gone; EOB tokens on their rows; R01/R03/R04/R05 red; no total-like route keys) still hold. The new probe does not change them.
- F1 (major, carried): the rate row's running balance is still only inside its excerpt, and the whole-row exemption passes it (billing.py:649, test_billing.py:570; T01_table_rate_no_cents_failure.txt).
- F2 (minor, updated): comparisons remain. The reversal sign test (billing.py:808) and the same-provider merge equality (billing.py:696-717) compare money values; the accounting net compares token text (billing.py:662, 725-727). memory/contracts/api.md:664 says "no sums and no comparisons of any kind", while api.md:693 describes the sign-based reversal rule. The contract conflicts with itself, so this needs Chris's ruling. If api.md:664 is read literally, F2 becomes major.
- F3, F4, F5 as in r2 (stale comments; detail kinds; in-test EOB proof).

**Pytest.** `.venv/bin/python -m pytest -q tests/unit/test_billing.py`: 179 passed in 1.04s in the project worktree (pytest_billing_HEAD_bcdcb91.txt). The same on the archive copy with `-I`: 179 passed in 0.93s (pytest_billing_archive_bcdcb91.txt). The suite passes because no test covers a cross-provider repeat.

**Not exercised.** The full tests/unit suite. The app over HTTP (TestClient only). The D-019 accepted total was not re-run; the commit does not touch totals.py, present.py or api.py. Other providers' identical rows in real statements (the probe is synthetic).

Evidence: artifacts/review-evidence/T-103-r2/ (RUN_ORDER.txt lists every command; the r2 file's evidence list still applies, plus merge_cross_provider_probe.py and its output).

```json
{"card": "T-103", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git commit bcdcb91 (fix(backend): billing applies D-052 strictly, T-103 r2): app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md; scratch copy of git archive bcdcb91; project worktree (HEAD later c2a5d1f, billing files identical to bcdcb91); billing route via TestClient on evals/golden sample, case_03_rate_and_ocr, case_09_nonvisit_hides_gap and a synthetic EOB $140 case; a synthetic two-provider probe; no app URL exercised. Supersedes reviews/T-103-staff-engineer-r2.md.",
 "exercised": [
   "git rev-parse HEAD -> bcdcb919f1723f51579db03d9426443860a91680 at review start; git log later showed c2a5d1f (T-106) and 3462ad0 (T-104) above it",
   "git show --stat bcdcb91 -> app/backend/billing.py, memory/contracts/api.md, tests/unit/test_billing.py (3 files, 204 insertions, 138 deletions); git show bcdcb91 -- memory/contracts/api.md -> two hunks (@@ -36,7 and @@ -661,38)",
   "git diff --stat bcdcb91 HEAD -- the three files -> empty; git status --short on the three files -> empty",
   "git diff 2dc5be2 bcdcb91 read in full for billing.py, memory/contracts/api.md and tests/unit/test_billing.py (saved to the scratchpad and read hunk by hunk)",
   ".venv/bin/python -m pytest -q tests/unit/test_billing.py in the project worktree -> 179 passed in 1.04s",
   "git archive bcdcb91 into a scratchpad copy; .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py on the copy -> 179 passed in 0.93s",
   "merge_cross_provider_probe.py on the copy (merge_cross_provider_probe_output.txt): two providers, identical 97110 row, 06/10/26, 130.00 -> one charge line, provider Larkspur, record_nos [1, 2]; same provider re-sent -> one line citing both records; _line_key fields",
   "git show 2dc5be2:app/backend/billing.py and bcdcb91 grep for _line_key and _merge_duplicates: key has no provider at both commits (lines 683-685 at 2dc5be2)",
   "read billing.py 696-717, 801-804 (provider assignment and merge order); tests/unit/test_billing.py 995-998 (identical-copy test uses one provider)",
   "r1_reprobe.py, route_keys.py, run_mutants_r2.py (R01 to R09, T01), run_mutants.py (r1 set), r2_survivor_and_m2_check.py, T01 failure detail: outputs in artifacts/review-evidence/T-103-r2/ (the r2 file's evidence list)",
   "grep on the copy for LEDGER_EOB, _sum(, _tot(, payer_reports, BALANCE_STEP, balance_convention, stated_totals; grep of billing.py and the test module for float(, except, sleep(, random, network or model imports",
   "memory/contracts/api.md 663-699 and memory/ORCHESTRATOR_DECISIONS.md:60 (D-052) read"
 ],
 "verdict": "fail",
 "scores": {"fail_safe_completeness": 3, "decision_D052_conformance": 3, "honest_failure_no_silent_skip": 3, "api_doc_matches_code": 3, "money_integer_cents": 5, "no_llm_in_deterministic_path": 5, "test_mutation_catch": 3, "D019_total_unchanged": 5},
 "findings": [
   {"severity": "blocker",
    "title": "Identical rows from two different providers are merged into one line: a second provider's charge disappears from the listing (pre-existing, in scope)",
    "evidence": "artifacts/review-evidence/T-103-r2/merge_cross_provider_probe_output.txt, case A: record 1 Larkspur Hollow Physical Therapy and record 2 Medlark Clinic, each with the row '06/10/26 06/11/26 97110 Therapeutic exercise 130.00 130.00'. One charge line for 97110: provider Larkspur Hollow Physical Therapy, record_nos [1, 2], billed 13000; Medlark's record gives only its four printed-total lines. Cause: app/backend/billing.py:696-698 _line_key has no provider; billing.py:701-717 _merge_duplicates merges a later-record line whose key matches (merge condition at 706-707); billing.py:802-803 assigns the provider before the merge at 804. Same key at 2dc5be2 (billing.py:683-685). tests/unit/test_billing.py:995-998 test_identical_copy_of_one_statement uses the same provider in both records.",
    "why_it_matters": "D-052's reason for a listing is that a listing cannot hide a missing line (memory/contracts/api.md:664). Here a second provider's charge is hidden inside another provider's line, and the line attributes the charge only to Larkspur. The fact that Medlark billed the service is lost from the listing. That is a loss of a fact under D.2. Persona checklist item 19 requires the dedupe key to include source and provider, and it does not.",
    "fix": "Include the provider in the merge key. Merge only a same provider re-sent statement (byte-identical excerpt, same provider and form, a second record). Otherwise keep both lines. Chris's answer to question 1 decides whether same-provider identical rows in two different statements also merge.",
    "acceptance_test": "A test with Larkspur and Medlark carrying the same 97110 row gives two charge lines for 97110, one per provider, each with its own record_no. The same-provider re-sent test (test_billing.py:995) still gives one line citing both records. A mutant that removes the provider from _line_key turns the new test red."},
   {"severity": "major",
    "title": "Rate-row running balance is still only inside its excerpt; the oracle's whole-row exemption is what passes it (r1 M2, not fixed at bcdcb91)",
    "evidence": "r1_reprobe_output.txt and r2_survivor_and_m2_check_output.txt: row 'Charge per visit 185.00 999.00' gives one line, class rate, figure 185.00, and no balance field; '999.00' occurs only in the excerpt. app/backend/billing.py:649 whole = [x['excerpt'].strip() for x in list(rates) + list(lop)] and tests/unit/test_billing.py:570 _WHOLE_ROW = ('rate', 'estimate', 'reduction', 'lien_amount', 'asserted_balance') are unchanged in bcdcb91. T01_table_rate_no_cents_failure.txt: with 'rate' removed from _WHOLE_ROW, table_rate_no_cents fails with assert [('315.00', ...)] == [].",
    "why_it_matters": "The running balance is a printed money token that a paralegal can only find inside the verbatim text. api.md:692 says a running balance is listed beside the lines, but on a rate row it is not a figure field of any line. The oracle accepts it only because the whole row is exempt. This is the r1 blind spot again, through the rate path.",
    "fix": "Carry the rate row's running balance as a figure of the rate line (an unclear figure with its text, or a separate cited line with class unclear), then remove 'rate' from _WHOLE_ROW. Update api.md:692 to name the field.",
    "acceptance_test": "For 'Charge per visit 185.00 999.00', '999.00' sits in a structured field of the output and not only in excerpt or cites; tests/unit/test_billing.py passes with 'rate' removed from _WHOLE_ROW; a mutant that drops that field turns the probe red."},
   {"severity": "minor",
    "title": "Comparisons remain: memory/contracts/api.md:664 says 'no sums and no comparisons of any kind', and the code still compares money values and token text",
    "evidence": "app/backend/billing.py:808 (l['billed']['cents'] or 0) < 0 sets detail 'reversal' (a sign test on a money figure); billing.py:696-717 equality on billed, paid and adjustment cents for the merge (see B1); billing.py:662 it[1] == key and billing.py:725-727 _listed_elsewhere compare token text to decide whether a token is placed. memory/contracts/api.md:664 'No sums and no comparisons of any kind (D-052, applied strictly in T-103 r2)'. api.md:693 describes the sign rule ('credit notation ... makes a charge negative (detail: reversal)'). memory/ORCHESTRATOR_DECISIONS.md:60 forbids totals and a complete badge and does not mention comparisons.",
    "why_it_matters": "The contract's own sentence is broader than the decision text, and the contract also describes the sign rule. None of the remaining comparisons produces a sum, a total, a shown verdict or a disagreement check. The merge comparison is the one that can hide a line, and B1 covers it. So this is minor pending Chris's ruling; if api.md:664 is read literally, F2 is major.",
    "fix": "Chris rules on api.md:664. If literal: classify reversal from the excerpt's credit notation (parentheses or a trailing minus) and reword the sentence to say which comparisons remain. If not literal: reword api.md:664 to name the comparisons that are forbidden (checks that can say two figures disagree).",
    "acceptance_test": "The ruling is recorded in memory/ORCHESTRATOR_DECISIONS.md under D-052 and api.md:664 matches the code. If literal: no money comparison remains in billing.py, and a test pins 'reversal' from a parenthesised figure."},
   {"severity": "minor",
    "title": "Stale comment and docstring wording name the removed provider-completeness state",
    "evidence": "app/backend/billing.py:563 '...the provider of such a line is complete: false.' (no complete field exists; tests/unit/test_billing.py:77 lists 'complete' in _GONE). billing.py:170 'the provider is incomplete'; billing.py:180 'the provider is incomplete, and the figure is not left only in a field nobody opens'.",
    "why_it_matters": "A reader who greps for 'complete: false' finds a comment about a flag that D-052 removed. 'Provider is incomplete' brings back the completeness state the decision retired.",
    "fix": "Reword the three comments to say the figure is listed on its own line and that no provider completeness is claimed.",
    "acceptance_test": "grep for 'complete: false' and 'provider is incomplete' in app/backend/billing.py returns nothing; the module docstring and api.md agree."},
   {"severity": "minor",
    "title": "detail carries several kinds of thing (r1 m1, carried; 'eob' is one more value)",
    "evidence": "r1_reprobe_output.txt, (class, detail) pairs over PROBES: (charge, reversal), (unclear, eob), (rate, rate), (unclear, asserted_balance), (unclear, stated_total_billed), (unclear, balance_forward), (unclear, None) and others. billing.py:808-809 computes detail from form, sign, description and balance.",
    "why_it_matters": "A client has to branch on detail strings that mean different things: why a ledger row is listed, and what kind of extra line this is.",
    "fix": "As r1 proposed: a closed kind list for what the line is, and a separate reason for why it is listed. Document both in api.md.",
    "acceptance_test": "Every line has a kind from a closed list, and a test pins that list."},
   {"severity": "nit",
    "title": "The in-test EOB fail-safe proves the oracle by editing the output, not the production path",
    "evidence": "tests/unit/test_billing.py:804 test_eob_fail_safe_names_a_figure_dropped_from_a_row... deletes keys from the analysed output and asserts the oracle names them. The production-path proof is R01 and R04 in mutation_results_r2.txt.",
    "why_it_matters": "The test is correct as an oracle test but does not run a changed parser. The parametrized test at tests/unit/test_billing.py:781 does exercise the parser's unclear path and catches R01, so this is only a nit.",
    "fix": "Optional: add one test that patches the EOB parser's unclear list to empty and asserts the oracle names the figure.",
    "acceptance_test": "Optional; mutant R01 stays red."}
 ],
 "whats_right": [
   "EOB money tokens sit on their rows: '$140', '1O0.00', bare '130' and '130.5' each stay as text on the EOB line, and the oracle names nothing unaccounted (r1_reprobe_output.txt).",
   "No sums, payer checks or ledger comparisons remain: the 140.00 control raises no check, and no total-like key appears in the four route responses (route_keys_output.txt, grep_removed_names_bcdcb91.txt).",
   "The EOB fail-safe is caught at the code level: R01, R03, R04 and R05 turn 7, 2, 4 and 19 tests red (mutation_results_r2.txt)."
 ],
 "questions_for_chris": [
   "Two identical rows for the same provider in two different statements (not a re-sent copy): one charge or two? memory/contracts/api.md:664 says a re-sent statement is one line; the code also merges any identical row from a later record. The fix for B1 depends on the answer.",
   "Does 'no sums and no comparisons of any kind' (memory/contracts/api.md:664) cover the reversal sign test (billing.py:808) and the same-provider merge equality? If yes, F2 becomes major.",
   "For F1: may a rate row's running balance stay as cited excerpt text only (the bcdcb91 reading), or must it be a figure field (the r1 proposal)?"
 ]}
```
