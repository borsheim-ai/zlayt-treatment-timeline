# T-083 r3 review: billing analysis, db08276 (staff-engineer-reviewer)

**Verdict: fail.** Two blockers stand. Blocker 3 from r1 and the r2 blocker are reopened in part: bare figures with no `$` and no cents still vanish, on three paths, and one path now vanishes with `complete: true`.

Answers to the brief, one line each:
- **No amount-bearing line disappears while complete is true: NOT MET.** Bare whole-number figures vanish with `complete: true` in an unlabelled prose row (P11), a dateless CMS-1500 line (P16) and a balance-forward row (P4). A second balance-forward row overwrites the first with `complete: true` (P2, P3). Finding 1 and finding 2.
- **Each amount parsed, unreconciled or excluded, with complete false whenever anything is unclear: NOT MET.** A labelled bare charge row is gone and complete is false (P13, P17). A dateless bare figure is omitted from its row's figures (P7). A line flagged BALANCE_STEP_MISMATCH leaves complete true (P2).
- **Fail-safe accounting test exists: YES, but it cannot see the class that broke.** `tests/unit/test_billing.py:664-667` runs 24 corpus cases, and the counter's token regex (`:578`) has no bare whole numbers. Finding 4.
- **Mutant M05 fails: YES.** Caught by `test_prose_unlabelled_figure_is_not_totaled_and_is_listed_unreconciled` and `test_prose_figure_with_no_billing_word_at_all_is_listed_and_the_total_is_unknown` (2 failed).
- **balance_forward field correct: PARTLY.** The value and cite are right for one table forward row (P1: 10000). It is not reconciled into the statement balance (finding 5), a second row is lost (finding 2), and a prose "Previous balance" is read as the statement's own balance (finding 5).
- **No-cents table row kept on its row as `unclear`, complete false, versus "unreconciled or excluded": NO, not as written.** My r2 acceptance line says "must each show an unreconciled entry or an excluded entry with the row excerpt, and complete false where a row was lost." Cases A and B (`Office visit`, CHARGES `$185` / `185`) show only an on-row `unclear` figure, complete false, and no unreconciled or excluded entry. C, E, F, H, I and J now pass that line. The on-row state does not lose a fact and is what the code's LINE_UNCLEAR path defines, so I rate the gap major, not blocker. Finding 3.

Pins and runs:
- The worktree billing files equal `git archive db08276` (`cmp` identical). HEAD is now `950d4a5`; `git diff --stat db08276 HEAD -- app/backend/billing.py tests/unit/test_billing.py` is empty, so the billing code is unchanged since db08276.
- `.venv/bin/python -m pytest -q tests/unit/test_billing.py` gives `105 passed` on the worktree and `105 passed` on the scratch pin with `-I`.
- Probe logs: `artifacts/review-evidence/T-083-r3/probes_r2_rerun_db08276.log` (r2 cases A-J), `probes_r3_db08276.log` (P1-P15), `probes_r3_bare_dateless_db08276.log` (P16-P18).
- Mutant logs: `artifacts/review-evidence/T-083-r3/mutants-r2-set-on-db08276.log` (the r2 set, where M01, M10 and M12 are NOT APPLIED because their anchors moved) and `mutants-r3-set-db08276.log` (the r2 set re-anchored, plus N01-N11 for the r3 branches).

## Findings

**1. blocker: bare figures (no `$`, no cents) vanish; three of the cases keep `complete: true`.**
Probes (`probes_r3_db08276.log`, `probes_r3_bare_dateless_db08276.log`), with the digit-bounded token check:
- P11: prose `Office visit 250.` with `Total charges $500.00.` gives `complete: true`, token `250` absent from every list, and only `LEDGER_TOTAL_MISMATCH` and `LEDGER_BALANCE_MISMATCH` raised.
- P16: a dateless CMS-1500 line `11 98941 AB 85 1 SYN-NPI-0001` gives `complete: true`, `billed` 8500 from the dated control line only, and `85` absent from every list.
- P4: `Balance forward  100` (no `$`) gives `balance_forward: null`, `complete: true`, `100` absent.
- P13 and P17: labelled bare charges `New patient exam charge 250.` and `Office visit charge 250` vanish; `complete: false`, but the row is in no list. Only the stated totals appear as orphans.

Code: the bare-number tokenizer only runs under a money column (`billing.py:157`, `:223` `figs = _tokens(ln, cols if m else None)`). Prose finds only `$` figures (`:312`) and decimal figures (`:338`), so a bare whole number is never seen (`:337` is only reached for seen tokens). The CMS tail needs a `$`, decimal or pipe box (`:405-408`). The balance-forward branch only proceeds `if toks:` (`:216-221`).

Why it matters: a bare charge is a fact the record prints. P11 and P16 break the brief's rule with `complete: true`, and P13 and P17 lose the row.

Fix: tokenise bare whole numbers in every money position (ledger rows, prose charges labelled as charges, CMS money boxes, balance-forward rows), not only under a money column. Each such figure goes to an unclear line or to unreconciled, with the row excerpt, and the provider goes complete false.

Acceptance test: new cases for P4, P11, P16, P13 and P17 assert the figure text in `unreconciled` or a line's `unclear`, and `complete is False`. Mutant N08 (bare tokens off) is caught by a fail-safe corpus entry as well as by the explicit tests (see finding 4).

**2. blocker: a second balance-forward row overwrites the first silently, with `complete: true`.**
Probes: P2 (two rows, 100.00 then 50.00 in one statement) gives `balance_forward` 5000, `complete: true`, and `100.00` absent from the output. P3 (one forward in each of two records of one provider, 100.00 and 30.00) gives `balance_forward` 10000, `complete: true`, and `30.00` absent.

Code: `billing.py:218` assigns `balfwd = {...}` with no conflict check, unlike `_put_stated` (`:161-168`), which lists the earlier figure as unparsed. `billing.py:718` takes `next(...)` over the provider's records, so the first record wins and the others vanish.

Fix: apply the `_put_stated` rule to balance-forward: a second, different forward is listed as an unparsed line in unreconciled, and the provider is `complete: false`. Across records, list each forward with its cite.

Acceptance test: a two-row statement asserts `100.00` is in `unreconciled` or a line's `unclear`, and `complete is False`. A two-record provider asserts both forwards are visible.

**3. major: no-cents figures stay on their row as `unclear`; the r2 acceptance line is not met for A, B and P15.**
Probes: A and B (`probes_r2_rerun_db08276.log`) show `billed None`, `unclear ['$185']` or `['185']`, provider `complete False`, `LINE_UNCLEAR` on the line flags, and an empty `unreconciled` and `excluded`. P15 (CMS-1500 `45` box, dated, no decimal) is the same shape: `LINE_UNCLEAR`, unclear `['45']`, not in unreconciled. The line is cited verbatim and no total includes it, so no fact is lost, and this is not a blocker. The contract text agrees with the code: `memory/contracts/api.md:701` says a no-cents figure "stays on its row as `unclear` text (`LINE_UNCLEAR`, provider `complete: false`)". My r2 acceptance line still requires an unreconciled or excluded entry with the row excerpt, and this path does not provide one.

Fix (either): add each no-cents figure to `unreconciled` as well, with the row excerpt, or record a decision that LINE_UNCLEAR on the row counts as listed and amend the r2 acceptance line. I have not amended my own line; that is an orchestrator or Chris decision (see questions).

Acceptance test: A and B and P15 each show the figure in `unreconciled` (or the amended criterion is recorded and the test follows it).

**4. major: the fail-safe accounting test is blind to the no-cents class and to cents-None placement.**
- `tests/unit/test_billing.py:578`: `_TOKEN` matches `$`, decimal and boxed tokens only; a bare whole number is never counted. `unaccounted` (`:600-612`) therefore cannot flag P4, P11, P16, P17 or the bare table figures.
- Mutants (`mutants-r3-set-db08276.log`): N08 (bare whole numbers not tokenised in table rows) is caught only by `test_table_charge_with_no_cents_..._[185]` and `test_table_rate_row_..._[185]`, not by `test_failsafe_every_amount_token_is_parsed_or_listed[table_bare_no_cents]`. N03 (a no-cents figure stored as `billed` with cents None, no `unclear`, complete true) is caught only by the explicit `[$185]` and `[185]` tests; the counter accepts it because it compares text, not cents (`:585-597`). N05 (dateless CMS line with no `$` box dropped) SURVIVED all 105 tests. N10 (balance-forward unparsed path off) SURVIVED all 105 tests.
- The corpus is 24 cases (`pytest --collect-only -k failsafe_every` prints `24/105 tests collected`), against the "over 25 inputs" in the handoff. It has no balance-forward case and no dateless bare CMS case.

The counter's own non-vacuity test (`:670-676`) is sound and was caught by N11.

Fix: extend `_TOKEN` to bare whole numbers in money positions; make the counter check cents (a figure whose cents is None must be in `unclear`, not `billed`); add corpus entries P4, P11, P16 and a balance-forward case; kill N03, N05 and N10 in the fail-safe test.

Acceptance test: N03, N05, N08 and N10 each fail `test_failsafe_every_amount_token_is_parsed_or_listed` for their own case, not only an explicit test.

**5. major: balance_forward is not reconciled, and prose "Previous balance" is read as the statement balance.**
- P1 (one forward row 100.00; running balances 310 and 440; BALANCE DUE 440.00 includes the forward): `balance_forward` 10000 is correct and cited, billed 34000 correctly excludes it, and the statement still raises `LEDGER_BALANCE_MISMATCH` (stated 44000, computed 34000). Code: `billing.py:697-700` computes `derived = billed - paid - adjustment` and does not use `balance_forward`. The running-balance step check does use it (`:652`), so the two checks disagree.
- P6 (prose `Previous balance $500.00.`, one charge, `Total charges $250.00.`): `_PROSE` (`:290`) matches "balance", the figure is put in `stated_totals.balance` at `:330-331`, `balance_forward` is null, `LEDGER_BALANCE_MISMATCH` fires, and complete is true.
- The contract (`memory/contracts/api.md:674`) says `balance_forward` is "shown, never a charge"; that holds. It does not say whether a printed BALANCE DUE includes the forward, so the check's convention is not written down.

Fix: decide the convention (question 1). Then compute the reconciliation with the forward where the convention says so, or raise an explicit "convention unclear" check instead of a mismatch. Route prose "previous balance" to `balance_forward` or to unparsed, never to the statement balance.

Acceptance test: P1 asserts no `LEDGER_BALANCE_MISMATCH` under the agreed convention and `balance_forward` 10000. P6 asserts the previous balance is not `stated_totals.balance`.

**6. minor: `complete` ignores line checks.** P2 line b1 carries `BALANCE_STEP_MISMATCH` and the provider reads `complete: true`. Code: `billing.py:719` uses `not unclear and not unparsed_all`, and `_unclear` (`:577-578`) looks only at `unclear` and `unparsed`. A step mismatch says "a column may have been read wrongly", which is an unclear reading. Fix: count step mismatches in `unclear` or in a separate `complete` input. Acceptance: P2 gives `complete: false`.

**7. minor: r2 minor 4 is reopened on the CMS fallback path.** The handoff says unreconciled lists "money tokens only". For a CMS line with no money token, `billing.py:408` uses `unclear=toks or [rest.group(1).strip()]`. P14 (`ten dollars` in the box) gives `figures: ["11     97010          A   ten dollars   1      SYN-NPI-0001"]`, the whole tail. Fix: list the row excerpt in the entry and no figure list, or list only money-like words. Acceptance: P14 asserts `figures` equals `[]` or `["ten dollars"]`, not the tail.

**8. minor: dateless table row omits a bare CHARGES figure from its figures list.** P7: `97014 E-stim unattended 35 165.00` gives `figures ['165.00']`. The row excerpt in `unreconciled` does contain `35`, so the fact is not lost, but the machine-readable list is incomplete. Code: `billing.py:223` passes `cols` only for dated rows. Fix: same as finding 1, applied to undated rows. Acceptance: P7 asserts `['35', '165.00']` (or the agreed text).

**9. nit: the kind label.** A charge line whose charge is unreadable is labelled `balance_only` (A and B line b2; `billing.py:661`). Label it `unclear`.

## Mutation results on db08276 (scratch copies, repo untouched)
- r2 set: M05 CAUGHT (2 failed). M02, M03, M04, M06-M09, M11, M13-M23 CAUGHT. M01, M10 and M12 NOT APPLIED (anchors moved); their r3 equivalents M01r3, M10r3 and M12r3 are CAUGHT.
- r3 set: N01, N02, N03 (by explicit tests only), N04, N06, N07, N08 (explicit tests only), N09 and N11 CAUGHT. N05 and N10 SURVIVED.

## What is right
- Money is integer cents throughout: no `float(`, `except` or `sleep(` in `billing.py`, `amounts.py` or `test_billing.py`. Unreadable figures get `cents: null`, not a rounded value.
- Rate cues hold in tables and prose: per-visit rows and sentences with `$` or bare figures are listed once in `excluded` and never totaled (probes G and H; M01r3, M03, M04, M06-M09 caught).
- The verifier is on the route and each check is tested (M16-M22 caught), and the prose charge gate is pinned (M05 caught).

```json
{"card": "T-083", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "db08276 (T-083 r3): app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md billing section (line 674, 701). Pinned with git archive db08276 into the reviewer scratchpad (pin-db08276); worktree billing files cmp-identical to the pin. HEAD is 950d4a5; billing files unchanged between db08276 and HEAD. No app URL; the billing route is exercised by its TestClient test and direct analyze() probes. Sample case: not on this path (billing is not in the sample CLI). Probe fixtures are synthetic.",
 "exercised": [
  "personas/staff-engineer.md read in full; reviews/T-083-staff-engineer-r2.md read in full (brief checks, finding 1 acceptance line); board/cards/T-083.md read (r3 notes, handoff); reviewer memory project_t083_billing_review_patterns.md read",
  "git log --oneline -5; git show --stat db08276 (billing.py, api.md, test_billing.py); git diff --stat db08276 HEAD -- app/backend/billing.py tests/unit/test_billing.py (empty) and the same against reclassify.py and api.md (changed by 950d4a5, not billing)",
  "git archive db08276 | tar -x into the scratchpad pin-db08276; cmp: billing.py and test_billing.py identical to the worktree",
  ".venv/bin/python -m pytest -q tests/unit/test_billing.py in the worktree: 105 passed; .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py on the pin: 105 passed; pytest --collect-only -k failsafe_every: 24 collected",
  "read billing.py at the pin in full (851 lines), tests/unit/test_billing.py fail-safe section (575-684) and helpers (1-30, 560-612), memory/contracts/api.md billing rules (674, 701)",
  "red-flag greps on billing.py, amounts.py, test_billing.py: float(, except, sleep(, retry: no matches",
  "artifacts/review-evidence/T-083-r3/probes_r2_rerun_script.py (copy of the r2 probe) in modes brief, table, prose, cms, noisy against the pin: artifacts/review-evidence/T-083-r3/probes_r2_rerun_db08276.log (cases A-J)",
  "artifacts/review-evidence/T-083-r3/probes_r3.py (new probes P1-P15, digit-bounded token check) against the pin: probes_r3_db08276.log; P16-P18: probes_r3_bare_dateless_db08276.log",
  "artifacts/review-evidence/T-083-r3/run_mutants_r3.py on scratch copies of the pin (repo untouched): mutants-r3-set-db08276.log (r2 set re-anchored plus N01-N11); mutants-r2-set-on-db08276.log (the r2 set as run first on the pin). M05 CAUGHT (2 failed)",
  "artifacts/review-evidence/T-083-r3/anchor_check.py (count of mutant anchors in the pin) and billing_db08276.py / test_billing_db08276.py (copies of the pinned files for the citations)",
  "not exercised: a live server or app URL; the sample CLI (python -m app.pipeline evals/golden/sample.txt), which billing is not on; the frontend billing panel (not built)"
 ],
 "verdict": "fail",
 "scores": {"integer_cents_no_llm": 5, "rate_guard": 5, "grounding_verifier": 4, "honest_failure_visible": 2, "fail_safe_accounting": 2, "test_quality": 2, "determinism_and_reproducibility": 5},
 "findings": [
  {"severity": "blocker",
   "title": "Bare figures (no $, no cents) vanish; in three cases the provider reads complete true",
   "evidence": "artifacts/review-evidence/T-083-r3/probes_r3_db08276.log P11 and probes_r3_bare_dateless_db08276.log P16, P4: token absent from every list while totals.complete is True. P13 and P17 (labelled bare charge 'New patient exam charge 250.' and 'Office visit charge 250'): row in no list, complete False. Code: billing.py:157 and :223 (bare tokens only under a money column, and only on dated rows), :312 and :338 (prose finds $ and decimal figures only), :337 (bad.append only for seen tokens), :405-408 (CMS needs a $, decimal or pipe box), :216-221 (balance-forward only 'if toks:'). Repro: artifacts/review-evidence/T-083-r3/probes_r3.py <pin> all.",
   "why_it_matters": "A figure the record prints disappears while the provider reads complete. That loses facts (D.2 blocker) and breaks the brief's rule. An unlabelled or dateless no-cents charge is the input class the r2 fixture never had.",
   "fix": "Tokenise bare whole numbers in every money position (ledger rows dated or not, prose charges, CMS money boxes, balance-forward rows), not only under a money column. Each figure goes to an unclear line or to unreconciled with the row excerpt, and the provider goes complete false.",
   "acceptance_test": "Cases P4, P11, P16, P13 and P17 each assert the figure text in unreconciled or a line's unclear and complete is False. Mutant N08 is caught by the fail-safe corpus entry as well as by the explicit tests."},
  {"severity": "blocker",
   "title": "A second balance-forward row overwrites the first silently; complete true",
   "evidence": "probes_r3_db08276.log P2: two forward rows (100.00 then 50.00) give balance_forward 5000, complete True, '100.00' absent. P3: forwards 100.00 (record 1) and 30.00 (record 2) give balance_forward 10000, complete True, '30.00' absent. Code: billing.py:218 balfwd = {...} with no conflict check (contrast _put_stated at :161-168, which lists the earlier figure); billing.py:718 next(... for n in rec_nos ...) takes the first record only.",
   "why_it_matters": "Two printed balance-forward figures for one provider are amount-bearing rows. One vanishes with complete true, so a paralegal reading the provider sees a clean statement.",
   "fix": "Apply the _put_stated rule to balance-forward: a second, different forward is listed as an unparsed line in unreconciled and the provider is complete false. Across records, list each forward with its cite; do not take the first.",
   "acceptance_test": "A two-row statement asserts 100.00 is in unreconciled or a line's unclear and complete is False. A two-record provider asserts both forwards are visible."},
  {"severity": "major",
   "title": "No-cents figures stay on their row as unclear; the r2 acceptance line is not met for A, B and P15",
   "evidence": "probes_r2_rerun_db08276.log, case A ('$185') and B ('185'): line b2 billed None, unclear ['$185'] / ['185'], complete False, LINE_UNCLEAR, unreconciled [] and excluded []. probes_r3_db08276.log P15: CMS '45' box, line b3 LINE_UNCLEAR, not in unreconciled. memory/contracts/api.md:701 says a no-cents ledger figure 'stays on its row as unclear text (LINE_UNCLEAR, provider complete: false)'. My r2 acceptance line: 'cases A, B, C, E, H, I and J must each show an unreconciled entry or an excluded entry with the row excerpt, and complete false where a row was lost.' C, E, F, H, I and J now pass; A, B and P15 do not.",
   "why_it_matters": "No fact is lost and complete is false, so this is not a blocker. But the on-row state is not in the unreconciled list the contract points the paralegal to, and my acceptance line says it must be. The gap is between the criterion and the contract text, and it has to be settled, not left.",
   "fix": "Either add each no-cents figure to unreconciled as well, with the row excerpt, or record a decision that LINE_UNCLEAR on the row counts as listed and amend the r2 acceptance line and api.md:701 together. The reviewer does not amend its own criterion.",
   "acceptance_test": "A, B and P15 each show the figure in unreconciled with the row excerpt, or the amended criterion is recorded in memory/DECISIONS.md and its test passes."},
  {"severity": "major",
   "title": "The fail-safe accounting test is blind to bare whole numbers and to cents-None placement",
   "evidence": "tests/unit/test_billing.py:578 _TOKEN has no bare whole numbers; :585-597 _items compares figure text, not cents; :600-612 unaccounted; :664-667 the parametrised test (24 cases). artifacts/review-evidence/T-083-r3/mutants-r3-set-db08276.log: N08 (bare numbers not tokenised) CAUGHT only by test_table_charge_..._[185] and test_table_rate_row_..._[185], not by test_failsafe_...[table_bare_no_cents]; N03 (no-cents figure stored as billed) CAUGHT only by the explicit [$185] and [185] tests; N05 (dateless CMS box with no $ dropped) SURVIVED 105 passed; N10 (balance-forward unparsed path off) SURVIVED 105 passed. No corpus case for balance-forward or dateless bare CMS.",
   "why_it_matters": "The accounting test is the card's named guard for silent drops, and it cannot see the class that failed in r2 and again in finding 1. A rewrite that drops bare figures would pass it.",
   "fix": "Extend _TOKEN to bare whole numbers in money positions. Make the counter check cents: a figure with cents None must sit in unclear, not in billed. Add corpus cases for P4, P11, P16 and a balance-forward row.",
   "acceptance_test": "N03, N05, N08 and N10 each fail test_failsafe_every_amount_token_is_parsed_or_listed for their own case, not only an explicit test."},
  {"severity": "major",
   "title": "balance_forward is not in the statement-balance reconciliation; prose 'Previous balance' is read as the statement balance",
   "evidence": "probes_r3_db08276.log P1: balance_forward 10000 (correct, cited), billed 34000, complete True, LEDGER_BALANCE_MISMATCH (stated 44000, computed 34000) on a self-consistent statement. billing.py:697-700 derived = billed - paid - adjustment (no balance_forward); :652 the running-balance step check does use it. P6: 'Previous balance $500.00.' via _PROSE at billing.py:290 goes to stated_totals.balance (:330-331); balance_forward null; LEDGER_BALANCE_MISMATCH; complete True. memory/contracts/api.md:674 says 'shown, never a charge' and does not state the BALANCE DUE convention.",
   "why_it_matters": "A correct ledger with a forward and a BALANCE DUE that includes it is flagged as not reconciling; the paralegal is told the statement is wrong when it is not. The field is right, the check built on it is wrong, and the convention is unwritten.",
   "fix": "Decide the convention (question 1). Then reconcile with the forward where the convention says so, or raise an explicit 'convention unclear' check instead of a mismatch. Route prose 'previous balance' to balance_forward or to unparsed, never to the statement balance.",
   "acceptance_test": "P1 asserts no LEDGER_BALANCE_MISMATCH under the agreed convention and balance_forward 10000. P6 asserts the previous balance is not stated_totals.balance."},
  {"severity": "minor",
   "title": "complete ignores line checks; BALANCE_STEP_MISMATCH leaves a provider complete",
   "evidence": "probes_r3_db08276.log P2: line b1 checks ['BALANCE_STEP_MISMATCH'], provider complete True. billing.py:719 complete = not unclear and not unparsed_all; billing.py:577-578 _unclear looks only at unclear and unparsed.",
   "why_it_matters": "The brief says complete is false whenever anything is unclear. A step mismatch says a column may have been read wrongly, which is an unclear reading.",
   "fix": "Count step mismatches as unclear for the complete flag, or add a separate input to complete.",
   "acceptance_test": "P2 gives complete False."},
  {"severity": "minor",
   "title": "r2 minor 4 reopened on the CMS fallback path: figures holds the whole line tail",
   "evidence": "billing.py:408 unclear=toks or [rest.group(1).strip()]. probes_r3_db08276.log P14: unreconciled figures ['11     97010          A   ten dollars   1      SYN-NPI-0001']. The card handoff says unreconciled lists 'money tokens only'.",
   "why_it_matters": "The NPI and procedure code appear as the figure. The handoff claim is wrong for this path.",
   "fix": "On the fallback, list no figure (the row excerpt is already in the entry) or only money-like words.",
   "acceptance_test": "P14 asserts figures is [] or ['ten dollars'], not the tail."},
  {"severity": "minor",
   "title": "Dateless table row omits a bare CHARGES figure from its figures list",
   "evidence": "probes_r3_db08276.log P7: '97014 E-stim unattended 35 165.00' gives unreconciled figures ['165.00']; the row excerpt contains '35'. billing.py:223 passes cols only for dated rows.",
   "why_it_matters": "The fact is still listed in the excerpt, but the machine-readable list is incomplete, and a figure read from the list would be wrong.",
   "fix": "Apply the finding 1 fix to undated rows.",
   "acceptance_test": "P7 asserts figures is ['35', '165.00'] (or the agreed text)."},
  {"severity": "nit",
   "title": "A charge line with an unreadable charge is labelled balance_only",
   "evidence": "probes_r2_rerun_db08276.log, case A and B line b2 kind balance_only; billing.py:661.",
   "why_it_matters": "A UI row reads as a balance, not as an unreadable charge.",
   "fix": "Label the kind unclear when the charge figure is unreadable.",
   "acceptance_test": "Case A line b2 kind is unclear."}
 ],
 "whats_right": [
  "Money is integer cents throughout: no float(, except or sleep( in billing.py, amounts.py or test_billing.py; unreadable figures carry cents null, not a rounded value.",
  "Rate cues hold in tables and prose: per-visit rows and sentences are listed once in excluded and never totaled (probes G and H; mutants M01r3, M03, M04, M06-M09 caught).",
  "The verifier is on the route and each check is tested (M16-M22 caught); the prose charge gate is pinned (M05 caught by two tests)."
 ],
 "questions_for_chris": [
  "Does a statement's printed BALANCE DUE include the balance-forward line (balance = forward + charges - payments - adjustments)? Finding 5 cannot be fixed without the answer.",
  "For a no-cents ledger figure kept on its row as LINE_UNCLEAR (finding 3): is that enough, or must each also appear in unreconciled? The r2 acceptance line says the latter; I have not amended it."
 ]}
```
