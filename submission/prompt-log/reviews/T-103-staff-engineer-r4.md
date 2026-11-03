# T-103 staff-engineer review, r4 (commit 8a2b934)

Reviewer: staff-engineer-reviewer. Model: claude-haiku-5-5 (the id in the brief and the model this session runs as). CLAUDE.md §6 and D-024 name Sonnet for engineering reviewers; flagged, not changed (same as r1 to r3). This file follows reviews/T-103-staff-engineer-r3.md; it does not replace any earlier file.

**Verdict: changes.** No blocker. Two majors (findings 1 and 2, both carried from r3 and not fully closed) and three minors (3 to 5). The seeded exact count holds on every draw.

**The checks the brief asked for**

1. Random generator, exact per-record count: **pass.** The test module's own generator (`_BASES`, `_TOKENS`, `_insert`) was run over seed 20261102 and seeds 1 to 40, 600 draws each, 24,600 draws in total, on a `git archive 8a2b934` copy with `-I`. Failing draws: **0** by the module's helpers (the assertion test_property_a uses) and **0** by an independent count written for this review. Positive control: the same harness on the r3 commit (1526a1f, seed 20261102) reports 31 of 600, classed 18 BARE_OVERLIST, 10 DROP, 2 DOUBLE, 1 OTHER, which is the r3 result, so the harness can see the failure.
2. Other_figures gaps: **partly closed.** The r3 probe cases D (no-cents table balance), E (prose rate with two figures) and H (two LOP amounts in one sentence) now have an empty rule-break list, and the R1 footer (130.00 four times in, four out) and R2 (65.00 listed once) repros are fixed. One shape still breaks the literal rule on every UB-04 draw (finding 1).
3. No comparison codes: the removed codes are gone from `app/backend/billing.py`. `grep` finds `MISMATCH` only in the module docstring; the strings appear only in tests that assert they are absent (test_billing.py:132-133, 278) and in the removal list at api.md:698. Money-value comparisons are gone: the sign is a credit-notation flag (billing.py:403, 949). Offset comparisons remain for placement and for suppressing a printed total (finding 2).
4. `pytest -q tests/unit/test_billing.py`: **337 passed** in the worktree (HEAD 4a560d8, whose billing files equal 8a2b934) and **337 passed** on the archive copy of 8a2b934.

**Mutation evidence.** R4M1 (suppress every stated total, billing.py:970) turns 117 tests red. R4M2 (billing.py:790, the unclear-to-other_figures move on a rate row) and R4M3 (billing.py:798, the stated-total move on a rate row) each leave the suite green. R4M2 is reached: raising there turns 15 tests red. Removing its effect changes no output in the suite or in the 3,600-draw rule check. So either the branch is redundant or no test can tell it apart (finding 5).

**Status of the r3 findings**

- r3 F1 (other_figures literal gaps): open for the UB-04 room row (finding 1). Closed for probe cases D, E, H.
- r3 F2 (comparisons under D-052): money-value comparisons closed; offset comparisons open pending Chris's Q1 (finding 2).
- r3 F3 (printed total dropped when an equal figure shares its excerpt): closed. The R1 repro gives 130.00 four in, four out, and the 600-draw exact count fails 0 times.
- r3 F4 (rate figure also unreconciled): closed. R2 lists 65.00 once; 2O0.00 is an other figure of the rate line.
- r3 F5 (unit count or CPT code listed as unclear): closed for the random draws. Over-listing would show as a count mismatch, and there are 0 in 24,600.
- r3 F6 (live path folds a byte-identical same-date copy): open, unchanged (finding 3). Awaiting Chris's Q2.
- r3 F7 (detail carries a reason and a kind): open, unchanged (finding 4).

**A note on D-052's wording.** The phrase "no comparisons of any kind" is in api.md:667, and in the brief. The D-052 decision text (memory/ORCHESTRATOR_DECISIONS.md:60) does not use the word "comparison"; it forbids billed, paid and balance totals, a complete badge, and a comparison is not mentioned. I applied the stricter wording as the brief states it, and asked Chris (Q1).

**Exercised**

1. Read personas/staff-engineer.md; reviews/T-103-staff-engineer-r3.md in full; memory/ORCHESTRATOR_DECISIONS.md:60 (D-052); `python3 tools/board.py show T-103` (latest commit 8a2b934, AC 1 done, reviews r1 to r3 recorded, status in_review).
2. `git rev-parse --short HEAD` gave 4a560d8. `git diff --stat 8a2b934 HEAD -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md` printed nothing, so those files equal 8a2b934. `git diff --stat 1526a1f HEAD -- app/backend/ingest.py app/backend/totals.py` printed nothing; ingest and totals are unchanged since the r3 commit.
3. `git archive 8a2b934` extracted to the scratchpad (t103r4_archive). Positive-control archive `git archive 1526a1f` extracted to the scratchpad (t103r3_control_archive).
4. `artifacts/review-evidence/T-103-r4/random_count_seeds.py` on the 8a2b934 archive, all 41 seeds x 600 draws: `module_helper_exact_count_failing_draws=0`, `independent_exact_count_failing_draws=0` (random_count_seeds_8a2b934_output.txt). Same script on 1526a1f, seed 20261102: 31 failing draws (random_count_seeds_1526a1f_control_seed20261102_output.txt). The first version of my independent counter lacked the OCR-letter and CMS pipe forms and reported 5,561 false failures; I fixed it to the T-103 token forms before the run that counts.
5. `artifacts/review-evidence/T-103-r3/probe_r3.py` (-I) on the 8a2b934 archive: all 10 probes `count_equal_per_record=True`, `rate_lop_rule_breaks=[]` (probe_r3_8a2b934_output.json).
6. `artifacts/review-evidence/T-103-r3/repro_r3.py` on the 8a2b934 archive: R1 input 130.00 x4, output 130.00 x4, equal True; R2 65.00 listed once (repro_r3_8a2b934_output.txt). The "extra 2O0.00" line in R2 is the repro's own tokenizer, which does not read OCR letters; the module's count (which does) is equal on every draw.
7. `artifacts/review-evidence/T-103-r4/rate_rule_random.py` (literal api.md:695 rule over rate, estimate and LOP rows, 3,600 draws, seeds 20261102 and 1 to 5): 458 draws break, all base `ub04`, all the same token 5550.00 on rate line b6 (rate_rule_random_8a2b934_output.txt; rate_rule_by_base_8a2b934_output.txt). The same run on the R4M2 mutant gives the identical result (rate_rule_random_R4M3_mutant_output.txt; the file name is from the run order, its mutant is R4M2).
8. `artifacts/review-evidence/T-103-r4/ub04_rate_row_draw.py` on the 8a2b934 archive: b1 charge billed 5,550.00 and b6 rate figure 1,850.00 with other_figures [] for the same excerpt "0120 ROOM & BOARD SEMI-PVT 1,850.00 ... 5,550.00" (ub04_rate_row_draw6_8a2b934_output.txt).
9. `artifacts/review-evidence/T-103-r3/compare_scan.py` on billing.py at 8a2b934 (compare_scan_8a2b934_output.txt: 80 flagged lines, most of them regex literals, docstrings or layout; read each category). A targeted scan (money-word and comparison on one line; arithmetic, sum, float, Decimal) gave 54 lines, read by category. No `sum(`, `float(`, `Decimal(`, or money-valued `+=`. The only `+=` is an offset (billing.py:124).
10. `artifacts/review-evidence/T-103-r4/mut_r4.py` (scratch copies, never the repo): mutation_results_r4.txt (R4M1 117 failed; R4M2 337 passed; R4M3 337 passed). Raise-at-790 check, inline: 15 failed, 322 passed.
11. `artifacts/review-evidence/T-103-r3/live_dup_probe.py` on the 8a2b934 archive: dedupe groups [[1, 2]], billing record_nos [1], record 2 tokens in output 0 (live_dup_probe_8a2b934_output.txt). billing.py:884 filters `duplicate_of` records with no skipped_records entry; ingest.py:228-238 is unchanged.
12. `grep` for `float(`, `except`, LLM or model imports in billing.py: none. Test source scan present at test_billing.py:1336. Chris answers: no ruling on Q1 or Q2 found in submission/NEEDS_CHRIS.md or board/inbox (grep for T-103, placement, identical, DUPLICATE_OF).
13. Each citation in this file was checked with grep -n or sed -n on the 8a2b934 archive or the repo file it names (api.md lines 667, 695, 696; billing.py lines 113, 117, 403, 763, 776, 786, 789, 790, 797, 798, 801, 884, 949, 968 to 970; ingest.py 228 to 238; test_billing.py 55 to 64, 132, 133, 278, 1336).

**Not exercised.** The E2E tests and the full tests/unit suite (the brief named the billing module). The app over HTTP. The eval runner and the sample CLI (not in T-103). The case total (D-019): not touched by the commit, and totals.py is unchanged.

```json
{"card": "T-103", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git commit 8a2b934 (fix(backend): billing places tokens by position, not text; exact per-record count holds on 24000 generated records; other_figures filled, T-103 r4): app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md; git archive of 8a2b934 in the scratchpad (t103r4_archive); HEAD 4a560d8 with the three files unchanged since 8a2b934; ingest.py and totals.py unchanged since 1526a1f; no app URL; synthetic records only",
 "exercised": [
   "python3 tools/board.py show T-103 (latest commit 8a2b934; reviews r1 to r3; status in_review); personas/staff-engineer.md; reviews/T-103-staff-engineer-r3.md; memory/ORCHESTRATOR_DECISIONS.md:60 (D-052)",
   "git rev-parse --short HEAD -> 4a560d8; git diff --stat 8a2b934 HEAD on the three files -> empty; git diff --stat 1526a1f HEAD on ingest.py and totals.py -> empty",
   "git archive 8a2b934 into the scratchpad (t103r4_archive); git archive 1526a1f into the scratchpad (t103r3_control_archive) as a positive control",
   "artifacts/review-evidence/T-103-r4/random_count_seeds.py -I on the 8a2b934 archive, seeds 20261102 and 1-40, 600 draws each (24,600 draws): 0 failing draws by the module helpers and 0 by an independent count (random_count_seeds_8a2b934_output.txt); control on 1526a1f seed 20261102: 31 failing draws (random_count_seeds_1526a1f_control_seed20261102_output.txt)",
   "artifacts/review-evidence/T-103-r3/probe_r3.py -I on the 8a2b934 archive: 10 probes, count_equal_per_record true in all, rate_lop_rule_breaks [] in all (probe_r3_8a2b934_output.json)",
   "artifacts/review-evidence/T-103-r3/repro_r3.py -I on the 8a2b934 archive: R1 130.00 x4 in and out; R2 65.00 listed once (repro_r3_8a2b934_output.txt)",
   "artifacts/review-evidence/T-103-r4/rate_rule_random.py -I, literal api.md:695 rule over rate, estimate and LOP rows, 3,600 draws: 458 break, all ub04, token 5550.00 on rate line b6 (rate_rule_random_8a2b934_output.txt, rate_rule_by_base_8a2b934_output.txt)",
   "artifacts/review-evidence/T-103-r4/ub04_rate_row_draw.py -I: b1 charge 5,550.00 and b6 rate 1,850.00 with other_figures [] on the same UB-04 room row (ub04_rate_row_draw6_8a2b934_output.txt)",
   "artifacts/review-evidence/T-103-r3/compare_scan.py on billing.py at 8a2b934 (80 flagged lines, read by category; compare_scan_8a2b934_output.txt); targeted money-word and comparison scan, and sum, float, Decimal and += scan (54 and 18 lines, read)",
   "artifacts/review-evidence/T-103-r4/mut_r4.py on scratch copies: R4M1 117 failed; R4M2 337 passed; R4M3 337 passed (mutation_results_r4.txt); raise-at-billing.py:790 inline: 15 failed, 322 passed",
   "artifacts/review-evidence/T-103-r3/live_dup_probe.py -I on the 8a2b934 archive: dedupe groups [[1, 2]], record 2 tokens in output 0 (live_dup_probe_8a2b934_output.txt)",
   "python -m pytest -q tests/unit/test_billing.py: 337 passed in the worktree (pytest_billing_worktree_HEAD_4a560d8.txt) and 337 passed on the 8a2b934 archive with -I and no cache (pytest_billing_archive_8a2b934.txt)",
   "grep for float(, except, LLM and model imports in billing.py: none; grep for MISMATCH codes in billing.py, api.md and tests; test source scan at test_billing.py:1336; Chris answers searched in submission/NEEDS_CHRIS.md and board/inbox: none found",
   "grep -n on memory/contracts/api.md (lines 667, 695, 696), billing.py (113, 117, 403, 763, 776, 786, 789, 790, 797, 798, 801, 884, 949, 968 to 970) and ingest.py (228 to 238): each cited line checked"
 ],
 "verdict": "changes",
 "scores": {"exact_per_record_money_count": 5, "money_integer_cents_no_float": 5, "no_llm_in_deterministic_path": 5, "other_figures_contract_api_695": 2, "D052_no_comparisons": 3, "no_silent_loss_live_path": 3, "test_mutation_catch": 3, "D019_total_unchanged": 5},
 "findings": [
   {"severity": "major",
    "title": "UB-04 rate row: the row's own 5,550.00 total is a charge line, not in the rate entry's other_figures (r3 F1 carried; the r4 handoff says every other token on a rate row is an other figure)",
    "evidence": "artifacts/review-evidence/T-103-r4/ub04_rate_row_draw6_8a2b934_output.txt: b1 class charge billed 5,550.00 and b6 class rate figure 1,850.00 other_figures [] on the excerpt '0120 ROOM & BOARD SEMI-PVT 1,850.00 ... 5,550.00'. Repro: .venv/bin/python -I artifacts/review-evidence/T-103-r4/rate_rule_random.py <8a2b934 archive> 20261102,1,2,3,4,5 -> draws_with_rate_rule_break=458, all ub04 (rate_rule_by_base_8a2b934_output.txt). The UB-04 sample is test_billing.py:55-64. memory/contracts/api.md:695 says other_figures 'holds every OTHER money token printed on a rate, estimate or LOP/lien row ... a printed balance or total on that row'.",
    "why_it_matters": "No value is lost and no sum is made: 5,550.00 is on its own charge line, verbatim, and the per-record count holds. But the contract a client reads says the rate entry carries every other money token of its row, and this one does not. The literal rule fails on every UB-04 room row. A client that reads other_figures misses the row total. Both places cannot hold at once: the count test forbids listing the token twice, so the contract must either name this exception or the token must move to other_figures.",
    "fix": "Choose one and write it down: (a) api.md:695 says a token that the same row already lists as a charge line is not repeated in other_figures, and the rule is tested for that case; or (b) the rate entry takes the row total as an other figure and the charge line for that token is removed, keeping the count exact. Then fix the wording in api.md:695 to match.",
    "acceptance_test": "The literal rule script (rate_rule_random.py) reports 0 break draws on seeds 20261102 and 1-5, or api.md names the exception and a test asserts it. A mutant that removes the chosen rule turns a named test red."},
   {"severity": "major",
    "title": "Comparisons remain in listing code: placement and the suppression of a printed total are decided by comparing offsets (r3 F2 carried; open on Q1)",
    "evidence": "app/backend/billing.py:113 (return a[0] < b[1] and b[0] < a[1], the overlap test behind _lap) and :117 (containment, behind _within); :763 (if not any(_lap(fig['_at'], f['_at']) ...)); :776 (host = next(... _within(h['_at'], k['_row']) ...)); :786-789 (_within and _lap decide whether an unclear figure is an other figure); :797 and :801 (_lap decides whether a stated total or balance forward is an other figure); :968-970 (shown = _placed(...); if any(_lap(v['_at'], p) for p in shown): continue, so a printed stated total is not listed when its offsets overlap a placed token). compare_scan_8a2b934_output.txt lists these lines. memory/contracts/api.md:667 says 'No sums and no comparisons of any kind'. The D-052 decision text (memory/ORCHESTRATOR_DECISIONS.md:60) does not use the word 'comparison'. Q1 has no ruling in submission/NEEDS_CHRIS.md or board/inbox.",
    "why_it_matters": "Money values are no longer compared: the sign is a credit-notation flag (billing.py:403, 949), placement is by position, and no sum exists. What remains is a comparison of positions that decides which entry a token belongs to and whether a printed total is shown. Under the standard the brief states ('no sums or comparisons of any kind'), that is a comparison that decides output. Under the worker's documented reading (api.md:667: 'the only tests left on numbers are layout ... and offset overlap') it is allowed. The reading is Chris's to make, not the reviewer's or the worker's.",
    "fix": "Chris rules on Q1. If the literal reading stands: the parsers return the ids of the tokens they placed (the r3 fix), so the placement pass and the stated-total suppression compare nothing, and compare_scan shows no offset comparison in billing.py outside the verifier. If the placement reading stands: record it as a decision in memory/DECISIONS.md, reword api.md:667 to name offset overlap as the one allowed comparison, and keep the compare_scan allow-list in the test.",
    "acceptance_test": "After Q1: either compare_scan.py over billing.py lists only the verifier's substring checks, or api.md:667 names offset overlap and a DECISIONS entry records the ruling. A mutant that always suppresses a stated total turns 117 tests red (R4M1, mutation_results_r4.txt), so the suppression itself is covered."},
   {"severity": "minor",
    "title": "Live ingest folds a byte-identical same-date copy before billing sees it; record 2 has no count and no skipped entry (r3 F6 carried; awaiting Q2)",
    "evidence": "artifacts/review-evidence/T-103-r4/live_dup_probe_8a2b934_output.txt: dedupe groups [[1, 2]], billing record_nos [1], record 2 tokens in output 0. app/backend/ingest.py:228-238 (key = date, normalised source, normalised text; unchanged since 1526a1f). app/backend/billing.py:884 (recs = [r for r in records if not r.get('duplicate_of')]), with no skipped_records entry. memory/contracts/api.md:696 says 'a re-sent statement is two lines (one per record, ...)'.",
    "why_it_matters": "The rule that a re-sent statement is two lines is true for analyze() called directly, but not for the live path. A listing should say when a record is not shown; this one drops record 2 without a word. Checklist item 19 would accept one line here, so the behaviour may be right; the contract and the path do not say the same thing.",
    "fix": "Chris rules on Q2. If one set: name record 2 in skipped_records with reason DUPLICATE_OF and reword api.md:696 to say identical same-date copies are one set. If two sets: stop the ingest fold for billing and keep both records. Either way test the path through ingest.dedupe and then analyze.",
    "acceptance_test": "live_dup_probe.py: record 2 is either named in skipped_records with DUPLICATE_OF, or it has its own lines; the test runs through ingest.dedupe, not analyze() alone."},
   {"severity": "minor",
    "title": "detail carries both a reason for listing and a kind of line (r3 F7 carried, not changed in r4)",
    "evidence": "app/backend/billing.py:949 sets detail to eob, reversal, balance_only, rate, or None; the extra lines set detail to stated_total_billed, stated_total_balance, balance_forward and so on (billing.py:972 and the extra() calls at :965-966). The r4 handoff says 'detail kind/reason split (F7) untouched'.",
    "why_it_matters": "A client branches on strings that mean two different things: why a ledger row is listed, and what kind of line it is.",
    "fix": "As r1, r2b and r3 proposed: a closed kind list for what the line is, a separate reason for why it is listed, both documented in api.md.",
    "acceptance_test": "Every line has a kind from a closed list and a reason from a closed list; a test pins both lists."},
   {"severity": "minor",
    "title": "Two rate-row holder branches can be removed with the suite and the rule check unchanged (test-strength gap)",
    "evidence": "artifacts/review-evidence/T-103-r4/mutation_results_r4.txt: R4M2 (billing.py:790, the unclear-to-other_figures move) 337 passed; R4M3 (billing.py:798, the stated-total move) 337 passed. Raise-at-790 inline check: 15 failed, 322 passed, so the branch is reached. rate_rule_random_R4M3_mutant_output.txt (the R4M2 run's output file name keeps the earlier label) is identical to the baseline, so no output changes in 3,600 draws.",
    "why_it_matters": "Either the branch is redundant (the token is placed by another route in every shape tested) or the tests cannot tell. Both are a problem: dead code in the placement pass, and a contract rule with no guard on the path it names.",
    "fix": "Find a shape in which only the branch places the token, and assert its other_figures; or delete the branch and let the rule check and the exact count cover the case.",
    "acceptance_test": "Removing the chosen branch turns a named test red (mutant R4M2 or R4M3 in mutation_results_r4.txt)."}
 ],
 "whats_right": [
   "The exact per-record count holds on 24,600 generated draws across 41 seeds (0 failures by the module helper and by an independent count), and the same harness reproduces the r3 failure (31 of 600) on the r3 commit.",
   "Money values are no longer compared or summed: the sign is a credit-notation flag, the R1 footer and the R2 double are fixed, and no mismatch code or per-provider total remains in billing.py.",
   "The stated-total suppression is covered by a mutant (R4M1 turns 117 tests red), and the billing tests pass reproducibly (337 on both the worktree and the archive copy)."
 ],
 "questions_for_chris": [
   "Q1 (carried from r3, still open): does 'no comparisons of any kind' (api.md:667, and the brief) forbid comparing offsets to place a token and to suppress a printed total? D-052's own text (memory/ORCHESTRATOR_DECISIONS.md:60) does not mention comparisons. Finding 2 depends on the answer.",
   "Q2 (carried from r3, still open): a byte-identical copy dated the same day from the same source is folded at ingest (ingest.py:228-238). Do you want one set with record 2 named in skipped_records as DUPLICATE_OF, or two sets? Finding 3 depends on the answer.",
   "Q3 (new): for the UB-04 room row, should a row total that the row already lists as a charge line also appear in the rate entry's other_figures, or is that a documented exception? Finding 1 depends on the answer."
 ]}
```
