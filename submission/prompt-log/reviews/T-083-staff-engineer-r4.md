# T-083 r4 review: final money-token accounting pass, 6bca71e (staff-engineer-reviewer)

**Verdict: fail.** One blocker stands: a second statement's TOTAL CHARGES overwrites the first, and the provider still reads complete: true. The r3 bare-figure blocker and the r3 second-forward blocker are closed for every probe in the brief.

Answers to the brief, one line each:
- Bare prose figures, dateless CMS rows and balance-forward rows (r3 P4, P7, P11, P13, P16, P17; r4 E8, E9): PASS. Each figure is listed or sits on its row as unclear, and the provider is complete: false.
- Second balance-forward row (r4 E2, E2b, E3, M6, M8): PASS. Every forward is in unreconciled and in balance_forwards; none is overwritten.
- Random money token in a ledger (seeded sweep, 360 insertions): PARTLY. 348 of 360 are accounted for or give complete: false with the record listed. The 12 that lose the figure with complete: true are bare or comma-grouped whole numbers on a stray ledger line outside any money column (finding 3, major pending a definition).
- Repeated summary rows all listed: NO for statement totals. Balance forwards are all listed; a second statement's TOTAL CHARGES overwrites the first (finding 1, blocker).
- Orchestrator decision on r3 F5 (BALANCE DUE consistent with or without the forward, and report which): NOT MET. r4 E1 and E5b print a BALANCE DUE that equals the total with the forward, and the code still raises LEDGER_BALANCE_MISMATCH with no convention reported (finding 2, major).
- EOB and skipped records: EOB records are NOT in skipped_records; they are in payer_reports (r4 S1). That is acceptable: EOB amounts are never added to charges and are cross-checked. skipped_records does list injection-skipped and unrecognised-form billing records, but totals.complete stays true for them (finding 4, major).
- `.venv/bin/python -m pytest -q tests/unit/test_billing.py`: 128 passed (worktree and HEAD pin).

Pins and runs:
- Pin: `git archive HEAD` extracted to the scratchpad as pin-HEAD2-r4 at 4c5f9bf (commit recorded in artifacts/review-evidence/T-083-r4/pin_commit.txt). Billing files (app/backend/billing.py, app/backend/amounts.py, tests/unit/test_billing.py) are identical at 6bca71e, f345bc8 and 4c5f9bf (`git diff --stat` empty). The worktree billing.py is cmp-identical to HEAD. The first probe pass ran on the f345bc8 pin; the explicit, multi and fuzz logs were re-run on the 4c5f9bf pin and are byte-identical.
- Logs in artifacts/review-evidence/T-083-r4/: probes_r4_explicit_HEAD2.log, probes_r4_multi_HEAD2.log, probes_r4_fuzz_HEAD2.log (the fuzz is seeded, random.Random(20261102)), probes_r4_skipped_HEAD.log and probes_r4_unrecognised_HEAD.log (f345bc8 pin; billing files identical), probes_r3_HEAD.log (the r3 P1 to P18 set), pytest_worktree.log and pytest_HEAD_pin.log. Scripts: probes_r4.py, probes_r4_skipped.py, probes_r3_rerun.py.
- Oracle: a token is accounted when its digit-bounded text sits in a figure field of the output (figure text, unclear list, unreconciled figures). A token not accounted must give totals.complete false and the record listed in unreconciled or skipped_records.

## Findings

**1. blocker: a second statement's TOTAL CHARGES (and BALANCE DUE) overwrites the first; the provider reads complete: true.**
Probe M5 (two consistent statements of one provider, TOTAL CHARGES 210.00 in record 1 and 130.00 in record 2; lines 210.00 and 130.00): the output has `stated_totals` = {billed: 13000, balance: 13000}, `totals.complete` True, and `unreconciled` empty. The printed 210.00 TOTAL CHARGES appears in no stated or unreconciled field. LEDGER_TOTAL_MISMATCH then compares the computed 34000 with the second statement's 13000, which misdirects the paralegal. Probe E3 (forward 100.00 and TOTAL CHARGES 340.00 in record 1, TOTAL CHARGES 70.00 in record 2) shows the same: the 340.00 total is absent; stated billed is 7000.
Code: app/backend/billing.py:822-825 `comp[kind] = stated.get(kind, [None])[-1]`. The comment at :822 says "the latest-in-file one is shown and all are listed", which is false for statement totals. The accounting pass at :610 (`for v in list(stated.values()) + list(bfs)`) treats each record's own stated totals as placed, so the overwritten total is counted as accounted and never shown.
Contract: memory/contracts/api.md:703 (HEAD) says "Repeated summary rows are never overwritten". D-049 (memory/ORCHESTRATOR_DECISIONS.md:57) says the same.
Repro: `.venv/bin/python -I artifacts/review-evidence/T-083-r4/probes_r4.py <pin> multi` (M5); `... explicit` (E3).
Why it matters: D-049 is binding and this violates it. A printed fact (a statement's total) is lost while the provider reads complete. Two monthly statements from one provider are an ordinary input. Only forwards got the no-overwrite rule; statement totals did not.
Fix: keep every printed statement total of a repeated kind across records, each with its cite. Put the later and earlier totals in unreconciled (or a listed statement-totals conflict) and set complete: false when a kind repeats across records. Compare the computed sum only against totals that cover the same lines, or raise an explicit conflict check. Remove the `[-1]` selection, and correct the comment at :822 and api.md:703 to match.
Acceptance test: fixture M5 asserts '210.00' is in unreconciled or in a listed per-statement total, and the provider is complete: false. Fixture E3 asserts '340.00' is visible in the output.

**2. major: the balance-forward convention (r3 F5, orchestrator decision) is not implemented.**
Probe E1 (BALANCE DUE 440.00 printed; billed 340.00; one forward 100.00): balance_forward is 10000 and correct, but the output has `LEDGER_BALANCE_MISMATCH` with stated 44000 and computed 34000. 44000 is billed plus the forward, so the printed balance is consistent with the forward and the output reports no convention. Probe E5b (prose: previous balance 500.00, charge 250.00, Balance due 750.00) gives the same mismatch: stated 75000, computed 25000, forward 50000.
Code: app/backend/billing.py:838 `derived = billed - (paid or 0) - ((adj or 0) + ...)`. The forward is never added, and no convention field exists in the output or api.md.
Why it matters: the decision says a printed BALANCE DUE is consistent with or without the forward and must say which. Today the paralegal is told a correct statement does not reconcile.
Fix: derive two values, without the forward (billed minus paid minus adjustment) and with it (that value plus the sum of balance_forwards). If the stated balance equals either, no mismatch; add `balance_convention` = "without_forward" or "with_forward" to the provider. Raise LEDGER_BALANCE_MISMATCH only when neither matches. Document the field in api.md. Two or more forwards: see question 1.
Acceptance test: E1 asserts no LEDGER_BALANCE_MISMATCH and balance_convention "with_forward". A fixture whose BALANCE DUE excludes the forward asserts "without_forward". A fixture matching neither asserts LEDGER_BALANCE_MISMATCH. E5b asserts the same.

**3. major (pending a definition): a bare whole number on a stray ledger line loses the figure with complete: true, 12 of 12 cases.**
Seeded sweep (artifacts/review-evidence/T-083-r4/probes_r4_fuzz_HEAD2.log): the 12 VIOLATION_LOST_COMPLETE_TRUE cases are all `table/stray_line/bare_whole`, `table/stray_line/comma_whole`, `table/stray_line_above_rows/bare_whole` and `.../comma_whole`. Examples: `table/stray_line/bare_whole/208`, `table/stray_line_above_rows/comma_whole/652`. Every $-prefixed, two-decimal, and column-aligned bare insertion across the table, prose and CMS families was accounted for or gave complete: false with the record listed (0 violations; 0 cents-None placements in complete providers).
Code: app/backend/billing.py:44 `_BARE` is "only read when it sits under a money column"; :156 `_tokens` reads bare numbers only with column spans; :533 `_ACC_MONEY` matches $-prefixed and two-decimal figures only. The property test (tests/unit/test_billing.py:972 `_insert`) places whole numbers only under a money column, so it cannot see this class.
Why it matters: the r3 blocker was exactly this class of silent loss. D-049's stated purpose is that silent loss is impossible "regardless of format". Under D-049's literal definition ("a no-cents figure in an amount column") a stray line is out of scope, so the code and the test follow the written rule. The brief's wording ("a random money token inserted into a ledger") is wider. I rate it major because the definition has to be settled, not because the code breaks its written rule.
Fix: if a bare whole number on a ledger line is money-shaped, add it to `_account` for ledger and UB-04 lines as ROW_NOT_PARSED with the row excerpt, and extend `_insert` to stray lines. If it is not, record the decision in memory/DECISIONS.md, state it in api.md:703 (already "in an amount position"), and have the test docstring say so. Upgrade to blocker if the orchestrator decides it is money-shaped.
Acceptance test: the 12 fuzz tags each either appear in an unreconciled or unclear list, or give complete: false with the record listed (`probes_r4.py <pin> fuzz` reports 0 lost-with-complete-true).

**4. major: totals.complete reads true when a billing record is skipped.**
Probe S2b (unrecognised billing form, source "Brightwater Ambulance invoice", three figures 1234.00, no $): `skipped_records` = UNRECOGNISED_BILLING_FORM, status partial_unclear, `totals.complete` True, `totals.billed` null, no provider. Probe S3 (a ledger with injection_tag set): `skipped_records` = INJECTION_SUSPECTED, status "none_found", `totals.complete` True.
Code: app/backend/billing.py:734 (injection skip), :753 (unrecognised skip), :905 status, :909 `"complete": not unreadable`. Skipped records are not counted in complete.
Why it matters: D-049 says a token that is not accounted for gives complete: false and the record is listed. The record is listed; complete is still true, and "none_found" says nothing was found when a billing record was skipped. On EOB: S1 (ledger plus the unit-test EOB) puts the EOB in payer_reports with matched_provider set, and skipped_records is empty. That is acceptable, so the brief's premise that EOB is in skipped_records is wrong.
Fix: set totals.complete to false whenever a billing-looking record is in skipped_records. Use status partial_unclear, not none_found, when an injection-skipped billing record exists.
Acceptance test: S2b and S3 each assert totals.complete False and status partial_unclear.

**Closed from r3 (checked, not findings):**
- r3 F1 (bare figures vanish): P4, P7, P11, P13, P14, P16, P17 now accounted with complete: false; P7 figures are ['35','165.00']; P14 figures are []. The stray-line class is finding 3.
- r3 F2 (second forward overwrites): E2, E2b, E3, M6, M8 list every forward; balance_forwards holds each.
- r3 F3 (no-cents on-row unclear): accepted by D-049 ("on-row unclear with complete: false is acceptable"). P15 and A/B give LINE_UNCLEAR with complete: false.
- r3 F6 (BALANCE_STEP_MISMATCH leaves complete true): S4 gives complete: false.
- r3 F8 (dateless table bare charge omitted): fixed (P7, E10).
- r3 F9 (unreadable charge labelled balance_only): fixed; the r2 A/B line kind is now "unclear" (probes_r3_HEAD.log and the r2 table run).
- r3 F4 (fail-safe counter blind to bare numbers): the property test now exists and uses bare numbers, but only in money columns (finding 3). I did not re-run the r3 mutants N05 and N10 in r4.

## What is right
- Money is integer cents. grep for `float(`, `except`, `sleep(` and `retry` in billing.py, amounts.py and test_billing.py returns no matches on the pin.
- Within one statement, a repeated balance forward or total is listed, not overwritten: E2, E2b, M2, M3, M4, M7, M8 all show the second figure in unreconciled with the row excerpt.
- The seeded sweep found no lost $-prefixed, two-decimal or column-aligned bare figure in 300 insertions across table, prose and CMS families (finding 3 is the only class).

```json
{"card": "T-083", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive HEAD = 4c5f9bf (billing files identical at 6bca71e, f345bc8, 4c5f9bf): app/backend/billing.py, app/backend/amounts.py, tests/unit/test_billing.py, memory/contracts/api.md line 703 at HEAD; decision D-049 and the r3 F5 decision from the T-083 card notes. No app URL: billing is exercised by direct analyze() probes on the pin. Sample CLI not on the billing path. Probe fixtures are synthetic (SYNTHETIC labels).",
 "exercised": [
  "personas/staff-engineer.md read in full; reviews/T-083-staff-engineer-r3.md read in full; reviewer memory project_t083_billing_review_patterns.md read; memory/ORCHESTRATOR_DECISIONS.md D-049 read; board/cards/T-083.md notes and handoff read",
  "git rev-parse --short HEAD (4c5f9bf); git log f345bc8..HEAD (one QA commit, no billing files); git diff --stat 6bca71e HEAD and f345bc8 HEAD over billing.py, amounts.py, test_billing.py, api.md (empty)",
  "git archive HEAD | tar -x into the scratchpad pin-HEAD2-r4; cmp of billing.py, test_billing.py, amounts.py against the 6bca71e archive and the worktree (identical)",
  ".venv/bin/python -m pytest -q tests/unit/test_billing.py in the worktree: 128 passed (artifacts/review-evidence/T-083-r4/pytest_worktree.log); .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py on the pin: 128 passed (pytest_HEAD_pin.log)",
  "red-flag greps: float(, except, sleep(, retry in billing.py, amounts.py, test_billing.py: no matches",
  "probes_r3_rerun.py (copy of the r3 P1 to P18 probes) on the f345bc8 pin: probes_r3_HEAD.log; r2 table probe (A, B) from artifacts/review-evidence/T-083-r3/probes_r2_rerun_script.py on the pin",
  "probes_r4.py modes explicit, multi, fuzz on pin-HEAD2-r4: probes_r4_explicit_HEAD2.log (E1 to E10), probes_r4_multi_HEAD2.log (M1 to M8), probes_r4_fuzz_HEAD2.log (360 seeded insertions, seed 20261102); the same modes on the f345bc8 pin gave byte-identical logs",
  "probes_r4_skipped.py and an inline unrecognised-form probe on the f345bc8 pin: probes_r4_skipped_HEAD.log (S1 EOB, S2 ledger-parsed invoice, S3 injection, S4 step mismatch), probes_r4_unrecognised_HEAD.log (S2b)",
  "read billing.py at the pin: _BARE :44, _tokens :156, _put_stated :167, _ACC_MONEY :533, _account :597 to :640, analyze() :724 to :912 (skipped appends :734 and :753, stated selection :822-825, derived balance :838, complete :859, status :905, totals.complete :909); tests/unit/test_billing.py _TOKENS :969, _insert :972, property test :1002; memory/contracts/api.md:703 at HEAD",
  "not exercised: the UB-04 family in the seeded sweep (the test file's property test covers it); r3 mutants N05 and N10 not re-run in r4; the frontend billing panel; the app URL; the sample CLI"
 ],
 "verdict": "fail",
 "scores": {"integer_cents_no_llm": 5, "bare_figure_accounting": 3, "repeated_summary_rows": 1, "balance_reconciliation": 2, "honest_failure_visible": 2, "test_quality": 3, "determinism_and_reproducibility": 5},
 "findings": [
  {"severity": "blocker",
   "title": "A second statement's TOTAL CHARGES (and BALANCE DUE) overwrites the first; the provider reads complete true",
   "evidence": "artifacts/review-evidence/T-083-r4/probes_r4_multi_HEAD2.log M5: stated_totals {'billed': 13000, 'balance': 13000}, totals.complete True, unreconciled empty; statement 1's TOTAL CHARGES 210.00 is in no stated or unreconciled field; checks LEDGER_TOTAL_MISMATCH compares 34000 with 13000. probes_r4_explicit_HEAD2.log E3: record 1 TOTAL CHARGES 340.00 absent, stated billed 7000. Code: app/backend/billing.py:822-825 comp[kind] = stated.get(kind, [None])[-1], with the comment at :822 'all are listed' (false for statement totals); :610 _account treats each record's own stated totals as placed. Contract: memory/contracts/api.md:703 'Repeated summary rows are never overwritten'; D-049 at memory/ORCHESTRATOR_DECISIONS.md:57. Repro: .venv/bin/python -I artifacts/review-evidence/T-083-r4/probes_r4.py <pin> multi",
   "why_it_matters": "D-049 is binding and this violates it: a printed statement total is lost while the provider reads complete, and the mismatch check compares against the wrong statement. Two monthly statements from one provider are an ordinary input. Only balance forwards got the no-overwrite rule.",
   "fix": "Keep every printed statement total of a repeated kind across records, each with its cite. List the earlier and later totals in unreconciled (or a listed statement-totals conflict) and set complete false when a kind repeats across records. Compare the computed sum only with totals that cover the same lines, or raise an explicit conflict check. Remove the [-1] selection; correct the comment at :822 and api.md:703 to match.",
   "acceptance_test": "Fixture M5 asserts '210.00' is in unreconciled or in a listed per-statement total and the provider is complete False. Fixture E3 asserts '340.00' is visible in the output."},
  {"severity": "major",
   "title": "Balance-forward convention (r3 F5, orchestrator decision) is not implemented",
   "evidence": "artifacts/review-evidence/T-083-r4/probes_r4_explicit_HEAD2.log E1: BALANCE DUE 440.00, billed 340.00, forward 100.00 gives balance_forward 10000 and LEDGER_BALANCE_MISMATCH with stated 44000, computed 34000 (44000 = billed plus forward). E5b: stated 75000 = billed 25000 plus forward 50000, same mismatch. Code: app/backend/billing.py:838 derived = billed - (paid or 0) - (adj ...), no forward, and no convention field in the output or api.md.",
   "why_it_matters": "The decision says a printed BALANCE DUE is consistent with or without the forward and must report which. Today a correct statement is reported as not reconciling.",
   "fix": "Compute the value without the forward and the value with it (plus the sum of balance_forwards). If the stated balance equals either, no mismatch; add balance_convention ('without_forward' or 'with_forward') to the provider and document it in api.md. Raise LEDGER_BALANCE_MISMATCH only when neither matches.",
   "acceptance_test": "E1 asserts no LEDGER_BALANCE_MISMATCH and balance_convention 'with_forward'. A fixture whose BALANCE DUE excludes the forward asserts 'without_forward'. A fixture matching neither asserts LEDGER_BALANCE_MISMATCH. E5b asserts the same as E1."},
  {"severity": "major",
   "title": "A bare whole number on a stray ledger line loses its figure with complete true (12 of 12 cases); pending a definition",
   "evidence": "artifacts/review-evidence/T-083-r4/probes_r4_fuzz_HEAD2.log: VIOLATION_LOST_COMPLETE_TRUE 12, all table/stray_line/bare_whole, table/stray_line/comma_whole, table/stray_line_above_rows/bare_whole and comma_whole (e.g. table/stray_line/bare_whole/208; table/stray_line_above_rows/comma_whole/652). $-prefixed, two-decimal and column-aligned bare insertions: 0 violations in 300 cases across table, prose and CMS families. Code: app/backend/billing.py:44 _BARE 'only read when it sits under a money column'; :156 _tokens; :533 _ACC_MONEY ($ and two-decimal only). tests/unit/test_billing.py:972 _insert places whole numbers only under a money column, so the property test cannot see this class. Repro: .venv/bin/python -I artifacts/review-evidence/T-083-r4/probes_r4.py <pin> fuzz",
   "why_it_matters": "This is the r3 blocker's class. D-049's purpose is that silent loss is impossible 'regardless of format'. Under D-049's literal definition (a no-cents figure in an amount column) a stray line is out of scope, so the code and the test follow the written rule. The brief's wording ('a random money token inserted into a ledger') is wider. Rated major because the definition must be settled, not because the code breaks its written rule.",
   "fix": "If a bare whole number on a ledger line is money-shaped: add it in _account for ledger and UB-04 lines as ROW_NOT_PARSED with the row excerpt, and extend _insert to stray lines. If not: record the decision in memory/DECISIONS.md, keep api.md:703 as 'in an amount position', and state it in the test docstring. Becomes a blocker if the orchestrator rules it money-shaped.",
   "acceptance_test": "Each of the 12 fuzz tags either appears in an unreconciled or unclear list or gives complete False with the record listed; probes_r4.py fuzz reports 0 lost-with-complete-true."},
  {"severity": "major",
   "title": "totals.complete reads true when a billing record is skipped (injection, unrecognised form)",
   "evidence": "artifacts/review-evidence/T-083-r4/probes_r4_unrecognised_HEAD.log S2b: skipped_records UNRECOGNISED_BILLING_FORM, status partial_unclear, totals.complete True, totals.billed null, no provider, three figures (1234.00) unlisted. probes_r4_skipped_HEAD.log S3: skipped_records INJECTION_SUSPECTED, status none_found, totals.complete True. Code: app/backend/billing.py:734 and :753 (skipped appends), :905 status, :909 totals complete = not unreadable (skipped records not counted). EOB (S1): in payer_reports with matched_provider, skipped_records empty; acceptable, but the brief's premise that EOB is in skipped_records is wrong.",
   "why_it_matters": "D-049: an unaccounted token gives complete false and the record is listed. The record is listed, but complete stays true, and status none_found says nothing was found when a billing record was skipped.",
   "fix": "Set totals.complete False whenever a billing-looking record is in skipped_records. Use status partial_unclear, not none_found, when an injection-skipped billing record exists.",
   "acceptance_test": "S2b and S3 each assert totals.complete False and status partial_unclear."}
 ],
 "whats_right": [
  "Money is integer cents: no float(, except, sleep( or retry in billing.py, amounts.py or test_billing.py on the HEAD pin.",
  "Within one statement a repeated balance forward or total is listed, not overwritten (E2, E2b, M2, M3, M4, M7, M8).",
  "The seeded sweep found no lost $-prefixed, two-decimal or column-aligned bare figure in 300 insertions across table, prose and CMS families."
 ],
 "questions_for_chris": [
  "Is a bare whole number on its own ledger line, outside any money column and with no $ or cents, a money-shaped token under D-049? The answer decides finding 3 (major or blocker).",
  "With two or more balance-forward rows, does the 'with forward' convention add the sum of all forwards? Finding 2 needs this for the multi-forward case.",
  "Should a skipped billing record (injection or unrecognised form) make the case's totals incomplete? I recommend yes (finding 4); the orchestrator should decide."
 ]}
```
