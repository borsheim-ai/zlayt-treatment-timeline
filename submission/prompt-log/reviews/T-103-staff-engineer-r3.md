# T-103 staff-engineer review, r3 (commit 1526a1f)

Reviewer: staff-engineer-reviewer. Model: claude-haiku-5-5 (the id in the brief). CLAUDE.md §6 and D-024 name Sonnet for engineering reviewers; flagged, not changed (same as r1 and r2b).

**Verdict: changes.** No blocker. Three majors (findings 1 to 3), three minors (4 to 6), and one carried minor (7). This file follows reviews/T-103-staff-engineer-r2b.md; it does not replace any earlier file.

**The three checks the brief asked for**

1. Nothing merges across records or providers: pass on the analysis path. Larkspur and Medlark with the same 97110 row give two lines, each citing only its own record (probe A). One provider with the same row in two records gives two lines (probe B). The same rate row in two records keeps each record's own running balance (probe I). The live ingest path is the exception; see finding 6.
2. Every money token on a rate or LOP row is in other_figures: fail for three shapes (finding 1). The table running balance (probe C) passes.
3. Per record, output money tokens equal input, and one drop fails a test: pass for the fixed probe set (all 10 probes equal per record; 245 tests pass) and for the drop mutants (all 7 turn the suite red; M1 and M2 each turn 8 tests red). Fail for generated records: 31 of 600 draws from the test module's own generator differ per record (findings 3 to 5). The exact-count claim holds for the fixed probes only.

**The D-052 ruling.** Applied as the brief states it: no comparisons of any kind. The code still compares money values and token text in five places (finding 2). The r2b F2 minor is now at the severity r2b gave its literal reading (major).

**Verdict basis.** The majors are: a contract mismatch on other_figures (1), comparisons left after the ruling (2), and one printed total dropped when an equal figure shares its excerpt (3). None invents a value or makes a token unreachable: the verbatim excerpt still carries each figure, and no sum or verdict is computed, so none is a blocker under D.2.

**Findings**

- 1 (major): rate or LOP rows with a second money token that is not in other_figures. probe_r3_output.json cases D, E and H.
- 2 (major): comparisons remain under the D-052 ruling. compare_scan_output.txt.
- 3 (major): a printed total is dropped when an equal figure sits in the same excerpt. repro_r3_output.txt case R1; random_count_classify_output.txt.
- 4 (minor): a rate figure is also listed unreconciled when its sentence has one unreadable figure. repro_r3_output.txt case R2.
- 5 (minor): a unit count or a money-shaped EOB code is listed as an unclear figure. random_count_detail_output.txt draws 32, 34, 165.
- 6 (minor): on the live path a byte-identical same-date copy is one set, which contradicts api.md:693. live_dup_probe_output.txt.
- 7 (minor, carried from r2b F4): detail still carries a reason and a kind.

**Mutation evidence.** mut_r3.py ran the unmodified copy (245 passed) and seven mutants on scratch copies. Each mutant went red: M1 (drop the other_figures placement) 8 failed; M2 (drop other_figures in extra lines) 8 failed; M3 (drop stated-total lines) 103 failed; M4 (drop the last listed line) 172 failed; M5 (dedupe by excerpt across records) 5 failed; M6 (a superseded total counts as shown) 4 failed, including the count test for M2b; M7 (suppress every stated total) 171 failed. The unmodified archive copy was not edited.

**Exercised**

1. Read personas/staff-engineer.md, reviews/T-103-staff-engineer-r2b.md, memory/ORCHESTRATOR_DECISIONS.md:60 (D-052), memory/contracts/api.md:664-694, and my T-103 memory notes.
2. `git rev-parse HEAD` gave 1526a1f at review start and a9a27ed later (other cards). `git show --stat 1526a1f` lists the three files (198 insertions, 60 deletions). `git diff 9851a0d 1526a1f` read for billing.py and memory/contracts/api.md in full, and the test file's new hunks at lines 1094 to 1249. `git diff --stat 1526a1f HEAD -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md` printed nothing, so the three files are unchanged since 1526a1f.
3. `.venv/bin/python -m pytest -q tests/unit/test_billing.py` in the worktree: "245 passed in 1.08s" (first run), "245 passed in 1.26s" (saved as artifacts/review-evidence/T-103-r3/pytest_billing_worktree_1526a1f.txt).
4. `git archive 1526a1f` into the scratchpad (t103r3_archive); `.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py` on the copy: "245 passed in 1.13s" (pytest_billing_archive_1526a1f.txt).
5. artifacts/review-evidence/T-103-r3/probe_r3.py run with -I on the archive: ten probes (A two providers, B same provider twice, C table rate with running balance, D rate balance without cents, E prose rate with two figures, F and G LOP letters, H LOP sentence with two amounts, I identical rate in two records, J LOP plus rate). Its own tokenizer, per-record exact count, and literal other_figures rule. Output in probe_r3_output.json.
6. artifacts/review-evidence/T-103-r3/repro_r3.py: cases R1 (footer with a trailing 130.00), R1 control, R2 (fee-schedule sentence with an unreadable figure), R3 (table rate balance). Output in repro_r3_output.txt.
7. artifacts/review-evidence/T-103-r3/live_dup_probe.py: ingest.dedupe then billing.analyze on two byte-identical same-date records. Output in live_dup_probe_output.txt.
8. random_count_probe.py, random_count_classify.py and random_count_detail.py: the test module's own 600-draw generator (seed 20261102) run with exact per-record counts. Outputs saved; 31 draws differ.
9. mut_r3.py with the seven mutants above; output in mutation_results_r3.txt.
10. compare_scan.py over app/backend/billing.py at 1526a1f; output in compare_scan_output.txt.
11. Read billing.py at 1526a1f: _tokens (157), _account (633-678), _own_cites (700-704), _listed_elsewhere (707-714), analyze (723-837), verify_citations (861-890). Read ingest.py dedupe (228-238).
12. grep of billing.py and tests/unit/test_billing.py for float(, except, sleep(, random and network or model imports: no float(, no except, no sleep( in billing.py; the test file imports random only for the seeded generator, and passes a time value only to ingest (lines 307-308), not to the billing functions.
13. Each line citation in this file was checked with grep -n on the file it names.

**Not exercised.** The full tests/unit suite and the E2E tests (the brief named the billing module). The app over HTTP: only the TestClient tests in the unit module. The eval runner and the sample CLI (not part of T-103). The case total (D-019): the commit does not touch totals.py, and its stat lists only the three files.

```json
{"card": "T-103", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git commit 1526a1f (fix(backend): billing never merges lines across records or providers; row money tokens are fields, T-103 r3): app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md; git archive of 1526a1f in the scratchpad; worktree HEAD a9a27ed with the three files unchanged since 1526a1f; app/backend/ingest.py dedupe read for the live path; no app URL; synthetic records only",
 "exercised": [
   "read personas/staff-engineer.md, reviews/T-103-staff-engineer-r2b.md, memory/ORCHESTRATOR_DECISIONS.md:60, memory/contracts/api.md:664-694",
   "git rev-parse HEAD: 1526a1f at start, a9a27ed later; git show --stat 1526a1f: 3 files, 198 insertions, 60 deletions; git diff 9851a0d 1526a1f read for billing.py and api.md; git diff --stat 1526a1f HEAD on the three files: empty",
   ".venv/bin/python -m pytest -q tests/unit/test_billing.py in the worktree: 245 passed in 1.08s (repeat: 245 passed in 1.26s, pytest_billing_worktree_1526a1f.txt)",
   "git archive 1526a1f into the scratchpad; .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py on the copy: 245 passed in 1.13s (pytest_billing_archive_1526a1f.txt)",
   "artifacts/review-evidence/T-103-r3/probe_r3.py with -I on the archive: 10 probes A to J; per-record exact count equal in all 10; literal other_figures rule breaks in D, E, H (probe_r3_output.json)",
   "artifacts/review-evidence/T-103-r3/repro_r3.py: R1 footer with trailing 130.00 drops one 130.00, R1 control equal, R2 rate figure listed twice, R3 running balance in other_figures (repro_r3_output.txt)",
   "artifacts/review-evidence/T-103-r3/live_dup_probe.py: ingest.dedupe groups [[1, 2]], billing record_nos [1], record 2 has 0 output tokens (live_dup_probe_output.txt)",
   "random_count_probe.py, random_count_classify.py, random_count_detail.py: the test module's 600-draw generator with exact per-record counts: 31 draws differ (18 bare-count, 10 drop, 2 double, 1 other); outputs saved",
   "mut_r3.py: baseline 245 passed; M1 8 failed, M2 8 failed, M3 103 failed, M4 172 failed, M5 5 failed, M6 4 failed, M7 171 failed (mutation_results_r3.txt; mutants on scratch copies)",
   "compare_scan.py over billing.py at 1526a1f (compare_scan_output.txt)",
   "read billing.py 157-165, 633-714, 723-837, 861-890 and ingest.py 228-238 at 1526a1f; read test_billing.py 1094-1249",
   "grep for float(, except, sleep(, random, network and model imports in billing.py and test_billing.py: none in billing.py code; random only as a seeded generator in the test",
   "grep -n on memory/contracts/api.md, app/backend/billing.py and tests/unit/test_billing.py for every cited line"
 ],
 "verdict": "changes",
 "scores": {"fail_safe_completeness": 3, "decision_D052_conformance": 3, "honest_failure_no_silent_skip": 3, "api_doc_matches_code": 2, "money_integer_cents": 5, "no_llm_in_deterministic_path": 5, "test_mutation_catch": 3, "D019_total_unchanged": 5},
 "findings": [
   {"severity": "major",
    "title": "Rate and LOP rows: some other money tokens are not in other_figures, which api.md:692 and the T-103 handoff both say they are",
    "evidence": "artifacts/review-evidence/T-103-r3/probe_r3_output.json, case D_table_rate_balance_no_cents: '$315' on the rate row is an unclear line b1 and unreconciled u1; rate b2 has other_figures []. Case E_prose_rate_two_figures: 'Charge per visit $185.00, balance $999.00.' gives rate b1 ($185.00) with other_figures [], and $999.00 appears only as unreconciled u1. Case H_lop_two_amounts_one_sentence: 'Lien balance $4,860.00 reduced to $3,100.00 in full satisfaction.' gives two LOP lines, each with other_figures []. Cause: billing.py:666 matches each token against items first, and items hold each rate/LOP entry's own figure (billing.py:651) and each unclear figure of the record's rows (billing.py:646-647); the holder branch at billing.py:669-670 therefore never sees those tokens. Test pins the D shape: tests/unit/test_billing.py:1155-1157 asserts '$315' is an unclear line of its own.",
    "why_it_matters": "api.md:692 says other_figures holds every OTHER money token on a rate, estimate or LOP/lien row, and the handoff says the same. The tokens are not lost (the per-record count holds), so this is a contract mismatch, not a dropped fact. A client that reads other_figures misses them, and the probe's literal rule fails on these three shapes. The existing count test cannot see the difference, because the same token is shown somewhere.",
    "fix": "Let the holder branch claim a token that sits inside a rate or LOP entry's excerpt before the record's own items match it, and make the second LOP amount in one sentence an other_figures entry of the first LOP entry. For the no-cents balance, either put it in other_figures with cents null or change api.md:692 and test_billing.py:1155 to say a no-cents balance is an unclear line of its own. Reword api.md:692 to match whichever is chosen.",
    "acceptance_test": "probe_r3.py reports an empty rate_lop_rule_breaks list for D, E and H. A new test asserts the other_figures contents for the prose rate sentence and the two-amount LOP sentence. Removing the holder branch at billing.py:669-670 turns those tests red."},
   {"severity": "major",
    "title": "D-052 ruling (no comparisons of any kind) is not met: money values and token text are still compared in listing code",
    "evidence": "artifacts/review-evidence/T-103-r3/compare_scan_output.txt. billing.py:794 (l['billed']['cents'] or 0) < 0 sets detail 'reversal', which is shown. billing.py:332 seg[...] == '-' sets the sign of a figure. billing.py:712-714 (_listed_elsewhere, set compare of figure texts) decides whether an unparsed row is dropped at billing.py:765. billing.py:761 'if ex not in seen' skips a second fee-schedule rate listing. billing.py:813-828: shown counts keyed by (record, excerpt, text) and the apart match on figure text and excerpt suppress a printed total. billing.py:666-670 text equality decides token placement. memory/contracts/api.md:664 reads 'No sums and no comparisons of any kind'.",
    "why_it_matters": "The ruling says no comparisons of any kind. The r2b file said that if api.md:664 is read literally, F2 is major; the ruling now makes it literal. No fact is lost in the probes (the count holds), and no sum, total or verdict is computed, so this is major and not a blocker. The suppression comparisons at billing.py:813-828 are the same mechanism behind finding 3.",
    "fix": "Take the sign of a figure from the credit-notation parse as a flag, not from '< 0' (billing.py:794 and 332). Let each parser return the ids of the tokens it placed, so the placement pass and the stated-total suppression compare nothing (billing.py:666-670 and 813-828). Remove the set compare at 712-714 and the skip at 761 in favour of parser-returned placement. See questions_for_chris Q1 for placement matching.",
    "acceptance_test": "compare_scan.py reports no operator or membership line on a money or figure text in the listing code, or each remaining line is named in api.md as placement. A mutant that flips the credit flag turns the reversal test red."},
   {"severity": "major",
    "title": "A printed total is dropped when an equal figure shares its excerpt; the per-record exact count fails on 31 of 600 generated records",
    "evidence": "artifacts/review-evidence/T-103-r3/repro_r3_output.txt case R1: 'TOTAL CHARGES 130.00  BALANCE DUE 123.45 130.00' under a 130.00 row. Input 130.00 x4, output 130.00 x3; the stated total billed 130.00 is not a line (lines b1, b2 and unreconciled u1 only). Cause: billing.py:813-816 counts unlisted figures per (record, excerpt, text); billing.py:822-825 suppresses the stated total because the trailing 130.00 uses the same key. The control 'BALANCE DUE 130.00' passes (R1-control). artifacts/review-evidence/T-103-r3/random_count_classify_output.txt: 10 DROP entries, 7 of them the 130.00 footer (draws 61, 151, 155, 229, 253, 393, 419); 3 are 9.999 values, which the module does not count as money (two decimals), so they are not counted here. The oracle at tests/unit/test_billing.py:591-609 is presence-only, and the exact count (tests/unit/test_billing.py:1234-1238) runs only over the fixed PROBES.",
    "why_it_matters": "The handoff says the same collision class was fixed for 210.00 (found and fixed a dropped balance-due 210.00 collision). It was fixed for that shape only: a second printed occurrence of an equal total in one excerpt is still lost from the structured fields. The verbatim excerpt still carries the text, so nothing is invented, but the brief's per-record exact-count rule fails and the oracle cannot see multiplicity.",
    "fix": "Stop suppressing by text. A stated total is always its own line, and each unlisted token is listed at its own position, so the same text in one excerpt is two entries. Add the R1 shape to PROBES. Move the exact count into the random loop of test_property_a_random_money_token_is_never_silently_missing.",
    "acceptance_test": "repro_r3.py case R1: output count equals input (130.00 x4). The exact count passes for 600 draws of the generator at test_billing.py:1094-1105. Removing the suppression at billing.py:823-825 turns the R1 case red."},
   {"severity": "minor",
    "title": "A rate figure is also listed as unreconciled when its sentence has one unreadable figure",
    "evidence": "artifacts/review-evidence/T-103-r3/repro_r3_output.txt case R2: 'Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection.   2O0.00' gives rate b2 ($65.00) and unreconciled u1 with figures ['$65.00', '2O0.00']. Same double in random_count_classify_output.txt draws 116 and 244. Cause: billing.py:707-714 _listed_elsewhere is all-or-nothing (every figure of the row must already be a rate figure), and billing.py:765 keeps the row.",
    "why_it_matters": "Over-listing, not loss. A reader sees the same $65.00 twice with two different labels (rate and unreconciled).",
    "fix": "Remove the rate's own figures from the unparsed row's unclear list and keep only the tokens that are not already listed, instead of the all-or-nothing test at billing.py:714.",
    "acceptance_test": "repro_r3.py case R2: 65.00 appears once; u1 figures are ['2O0.00']."},
   {"severity": "minor",
    "title": "A unit count and a CPT code become unclear figures; a money-shaped token in an EOB code slot is read as the code",
    "evidence": "artifacts/review-evidence/T-103-r3/random_count_detail_output.txt. Draw 32: '14' from 'treatment visits 1 through $123.45 14' is listed in unreconciled u1. Draw 34: the UB-04 UNITS value '3' is other_figures of the ROOM rate b6 after the description was lengthened. Draw 165: the EOB row's code field is '123.45' (b3 code) and the CPT 97014 is an unclear figure of b3. random_count_classify_output.txt: 18 BARE_OVERLIST and 1 OTHER over 600 draws. parse_figure('3') returns cents None and usd None (checked inline), so no money value is invented; the entries carry text only. Column test: billing.py:157 _tokens; EOB row regex billing.py:485 _EOBROW and _eob_tokens at billing.py:496.",
    "why_it_matters": "A count or a service code shown as a money figure is the regex-catches-a-non-money-number pattern. It is minor because no value or sum follows, and cents is null on each entry.",
    "fix": "A bare figure is money only under a money header within TOL of its column (billing.py:157). In an EOB row, the service code slot is a code and is never read as money. Re-check the alignment after the description is lengthened.",
    "acceptance_test": "draws 32, 34 and 165 give output counts equal to input counts. Each shape is added to PROBES with the exact count."},
   {"severity": "minor",
    "title": "On the live path a byte-identical same-date copy is one set, which contradicts api.md:693 and the test that pins two sets",
    "evidence": "artifacts/review-evidence/T-103-r3/live_dup_probe_output.txt: ingest.dedupe gives groups [[1, 2]] (app/backend/ingest.py:228-238; key at ingest.py:233 is date, normalised source and normalised text). Billing lines have record_nos [1]; record 2 has 0 output tokens and no skipped_records entry, because billing.py:725 drops records with duplicate_of. memory/contracts/api.md:693 says 'a re-sent statement is two lines (one per record...)'. tests/unit/test_billing.py:1123-1127 calls analyze() directly, so it never runs the ingest rule.",
    "why_it_matters": "A byte-identical copy with the same date and source is folded silently, so record 2 has no count and no visible skip. Checklist item 19 asks for duplicates to be counted once, so the behaviour may be right; the contract and the test name describe something else. A listing should say when a record is not shown.",
    "fix": "Decide (questions_for_chris Q2). Either name record 2 in skipped_records with reason DUPLICATE_OF and reword api.md:693 to say identical same-date copies are one set, or keep two sets and stop the ingest fold for billing. Either way, test the path through ingest.dedupe and then analyze.",
    "acceptance_test": "live_dup_probe.py: record 2 is named in skipped_records (or the contract says otherwise and the test runs through ingest.dedupe)."},
   {"severity": "minor",
    "title": "detail still carries a reason and a kind (r2b F4, carried, not changed in r3)",
    "evidence": "app/backend/billing.py:794-796 sets detail to eob, reversal, balance_only or None for ledger rows; billing.py:829 sets stated_total_* and balance_forward kinds for extra lines. The r3 handoff says 'detail kinds untouched'.",
    "why_it_matters": "A client has to branch on strings that mean different things: why a ledger row is listed, and what kind of extra line it is.",
    "fix": "As r1 and r2b proposed: a closed kind list for what the line is, and a separate reason for why it is listed. Document both in api.md.",
    "acceptance_test": "Every line has a kind from a closed list, and a test pins that list."}
 ],
 "whats_right": [
   "Identical rows from two providers, and one provider's identical rows in two records, are two lines each citing only its own record (probe_r3_output.json A and B; test_billing.py:1113-1127). B1 from r2b is closed.",
   "Rate and LOP running balances are structured: probe C and repro R3 put 999.00 in other_figures, and the 'rate' whole-row exemption is gone; M1 and M2 each turn 8 tests red.",
   "All seven drop and suppression mutants turn the suite red (mutation_results_r3.txt), and the baseline is 245 passed; no float, bare except, sleep or network call in billing.py or the test module."
 ],
 "questions_for_chris": [
   "Q1: The D-049 placement pass has to match each printed token to an output entry (billing.py:666-670). I read 'no comparisons of any kind' (D-052) as covering verdicts, sums and sign tests, not placement matching. Confirm that reading, or say how placement should work without comparing text. Finding 2 depends on the answer.",
   "Q2: A byte-identical copy dated the same day from the same source is folded at ingest (ingest.py:228-238), so billing shows one set. api.md:693 says a re-sent statement is two lines. Which do you want: one set, with record 2 named in skipped_records as DUPLICATE_OF, or two sets? Finding 6 depends on the answer."
 ]}
```
