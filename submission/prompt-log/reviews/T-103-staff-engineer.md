# T-103 staff-engineer review, r1 (commit 2dc5be2)

Reviewer: staff-engineer-reviewer. Model: claude-haiku-5-5 (as dispatched). CLAUDE.md §6 and D-024 call for Sonnet on engineering reviewers; flagged, not changed.

**Verdict: fail.** Two blockers, three majors, two minors, one nit.

**Your two calls.**
- Per-service EOB-vs-ledger checks: keep the mismatch flags. They are reconciliations, not totals, and nothing from them reaches the letter. Reject what they carry: the per-service billed and paid sums (B2) and the silent skip when a figure is unreadable (B1, M1). Compare row by row.
- Rates, LOP amounts, printed totals and balance forwards as lines with `detail`: accepted. Probe results: rate gives class rate, detail rate; LOP gives unclear with detail reduction, asserted_balance or lien_amount; printed totals give unclear with detail stated_total_billed/paid/adjustment/balance; balance forward gives unclear with detail balance_forward; estimate gives unclear with detail estimate. Caveats are M2 and m2.

**Pin.** HEAD is 2dc5be2 (`git rev-parse HEAD`). `git show --stat 2dc5be2` lists app/backend/billing.py, tests/unit/test_billing.py and memory/contracts/api.md only. Those three files are clean in the working tree (`git status --short` shows nothing for them). Checks ran on `git archive 2dc5be2` and on the parent `git archive 841be23`.

**Brief checks.**
1. Route returns only cited lines, unreconciled rows, skipped records and payer reports: partly. Lines, unreconciled rows, skipped records and payer lines carry verbatim excerpts, and `verify_citations` returned [] on every probe and golden case I ran. Not met for EOB figures without a decimal point (B1).
2. No provider totals, complete flag or balance sums: `complete`, `providers`, `totals`, `stated_totals` and `balance_convention` are absent from the route output. Not met: payer checks carry per-service billed and paid sums (B2). The per-line BALANCE_STEP check remains (m1).
3. D-019 case total unchanged: met. `totals.py`, `present.py` and `api.py` are not touched by the commit. Accepting every charge and reading `present.totals_view` gives identical output at 2dc5be2 and 841be23: case_03 $335.00, case_09 $275.00, sample $8,390.00.
4. Fail-safe test under a scratch-copy drop: met for parser drops. M02, M03, M04 and M07 each turn the random-insertion property test red, and M01 (accounting net off) does too. Not met for EOB and payer rows: M06 (an EOB unreadable figure dropped) leaves 157 of 157 green (M3).
5. `test_fixture_runs_write_no_artifacts`: fails on the archive. It is unrelated to T-103. It lives in tests/unit/test_t093_eval_signature.py, imports evals.run, and fails the same way on the parent 841be23. The commit touches none of those files. It is a red at HEAD and needs its own card. I did not run the full tests/unit suite.
6. `.venv/bin/python -m pytest -q tests/unit/test_billing.py`: 157 passed in 1.06s on the project tree and in 1.06s on the archive copy.

**Strongest evidence.**
- Printed EOB billed '$140' against a ledger 130.00 for the same service and date: no LEDGER_EOB_BILLED_MISMATCH, and the oracle reports nothing unaccounted. The same probe with '140.00' raises the mismatch (artifacts/review-evidence/T-103-r1/eob_mismatch_output.txt). The route response for this case has no billed figure on the EOB row (artifacts/review-evidence/T-103-r1/route_eob140.json).
- The same route response carries `{'code': 'LEDGER_EOB_PAID_MISMATCH', 'service': '97140', 'ledger': {'cents': 0, 'usd': '$0.00'}, ...}`, a per-service paid sum that D-052 forbids showing.
- Mutation runs (artifacts/review-evidence/T-103-r1/mutation_results.txt): every drop of a table, CMS, unreconciled or rate token is caught; the EOB drop is not.

**Not exercised.** The full tests/unit suite; the frontend beyond a grep (no billing references); Spanish records; security depth (deferred to security-reviewer); UX copy. I did not run the app over HTTP on a port; the route was run through TestClient.

```json
{"card": "T-103", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git 2dc5be2 (HEAD at review time): app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md; scratch copies of git archive 2dc5be2 and parent 841be23; billing route via TestClient on evals/golden case_03_rate_and_ocr, case_09_nonvisit_hides_gap, sample and synthetic EOB probes; no app URL exercised",
 "exercised": [
   "git rev-parse HEAD -> 2dc5be21bd790d548ccdfce74c308aef88045ea9; git show --stat 2dc5be2 (3 files); git diff --name-only 841be23 2dc5be2 (billing.py, api.md, test_billing.py only)",
   "git status --short on app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md: clean",
   ".venv/bin/python -m pytest -q tests/unit/test_billing.py -> 157 passed in 1.06s (project tree and archive copy)",
   "test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts run on archive 2dc5be2 and parent 841be23: fails on both",
   "GET /api/cases/{token}/billing via TestClient (fixture backend, ingest only) on case_03, case_09, sample, and on synthetic EOB probe case_eob_140.txt",
   "D-019: accepted every charge via POST /api/cases/{token}/items/{id}/review, then present.totals_view, on case_03, case_09, sample at 2dc5be2 and 841be23: identical (accepted 33500, 27500, 839000 cents)",
   "read billing.py: analyze, _ledger_table, _ledger_text, _cms1500, _eob, _account, _checks_for_line, verify_citations, module docstring; read test_billing.py: helpers, PROBES, BARE_PROBES, unaccounted(), property test",
   "probe listings of T-083 PROBES (ledger, prose, CMS-1500, UB-04, rates, LOP, printed totals, balance forwards, EOB) via a loader of tests/unit/test_billing.py from the archive",
   "EOB probes: '$140' vs ledger 130.00 with '140.00' control; '$130' and '1O0.00' EOB figures; same-service second unreadable ledger row with EOB 130.00; rate row 'Charge per visit 185.00 999.00'; estimate row",
   "scratch-copy mutants M01-M08 (run_mutants.py, run_m04.py): full file and property/probe selections; results in artifacts/review-evidence/T-103-r1/mutation_results.txt",
   "grep billing.py and test_billing.py for float, except, sleep, retry, random; grep app/frontend for billing (no matches); memory/contracts/api.md lines 664, 692, 693; memory/ORCHESTRATOR_DECISIONS.md line 60 (D-052)",
   "evidence saved: artifacts/review-evidence/T-103-r1/ (RUN_ORDER.txt, mutation_results.txt, eob_mismatch_output.txt, route_eob140.json, pytest_billing_HEAD_2dc5be2.txt, probe scripts)"
 ],
 "verdict": "fail",
 "scores": {"fail_safe_completeness": 2, "decision_D052_conformance": 2, "honest_failure_no_silent_skip": 2, "api_doc_matches_code": 2, "money_integer_cents": 5, "no_llm_in_deterministic_path": 5, "test_mutation_catch": 3, "D019_total_unchanged": 5},
 "findings": [
   {"severity": "blocker", "title": "EOB money token lost from every structured field; the kept EOB-vs-ledger billed check silently skips; EOB records have no accounting pass",
    "evidence": "artifacts/review-evidence/T-103-r1/eob_mismatch_output.txt: EOB 97110 billed '$140' vs ledger 13000 cents -> 'EOB billed-mismatch checks for 97110: []' and 'oracle unaccounted: []'; control with '140.00' -> ['LEDGER_EOB_BILLED_MISMATCH']. route copy artifacts/review-evidence/T-103-r1/route_eob140.json: payer row 97110 has no billed key, unclear ['52.00','78.00']. Code: app/backend/billing.py:505 (_NUM is decimal-only), :511 row['unclear'], :859 'if not led or not el.get(billed): continue', :775-776 _account runs only for ledger_table, ledger_text, cms1500, ub04 (not eob). Test: tests/unit/test_billing.py:583 payer rows count as accounted (whole=True).",
    "why_it_matters": "D-049 (billing.py:13-18) and api.md:693 promise every money token is a line, an unreconciled row, an unclear figure on its row, or in skipped_records. '$140' is none of these. The EOB amount that disagrees with the ledger is not reported, and the fail-safe test cannot see it. A fact is lost and a check the worker kept silently does not run.",
    "fix": "(a) Run an accounting pass for form eob: add 'eob' to the form tuple at billing.py:775-776 with an EOB unit list (every $ figure, decimal or not, and every bare figure under a money column). (b) In _eob, when a service row's figures do not map to its columns, list each money token of the row as unclear, and raise a visible check when the billed or paid figure is unreadable instead of the continue at billing.py:859. (c) Stop whole=True for payer rows in tests/unit/test_billing.py:583 (see M3).",
    "acceptance_test": "New test: EOB 97110 billed '$140' against ledger 130.00 -> unaccounted() == [] AND the payer output carries a check for 97110 (LEDGER_EOB_BILLED_MISMATCH with 140, or an EOB-amount-unreadable check). Mutant M06 (drop the EOB unclear list) turns at least one test red."},
   {"severity": "blocker", "title": "Per-service ledger billed and paid sums are computed and shown on EOB payer checks (D-052)",
    "evidence": "artifacts/review-evidence/T-103-r1/route_eob140.json: payer_reports[0].checks = [{'code': 'LEDGER_EOB_PAID_MISMATCH', 'service': '97140', 'ledger': {'cents': 0, 'usd': '$0.00'}, 'eob': {'cents': 1600, ...}}]. Code: app/backend/billing.py:861 lb, lp = _sum(led, 'billed'), _sum(led, 'paid') or 0; :864 'ledger': _tot(lb); :866 'ledger': _tot(lp). Decision: memory/ORCHESTRATOR_DECISIONS.md:60 'no billed/paid/balance totals ... are computed or shown'. Spec: memory/contracts/api.md:664 'No provider totals, no billed/paid/balance sums'.",
    "why_it_matters": "A billed or paid sum is the mechanism D-052 retired (five review rounds found totals that silently omit figures). The output contradicts the binding decision and the API doc. A reader sees 'ledger $0.00' and takes it for the ledger's paid total. The sum is also partial: unreadable rows are left out of _sum (see M1).",
    "fix": "Remove the 'ledger' value from both checks. Cite the matching ledger rows by their own excerpt and their own figures. Compare row by row (each ledger row for that service and date against the EOB figure), so no sum is computed anywhere. Keep the check codes and the mismatch flag, which are consistent with D-052.",
    "acceptance_test": "Route output for any raised payer check contains no 'ledger' key holding a cents value; the check's cites list the ledger rows with their own excerpts. Test: assert 'ledger' not in each payer check, and that each cite excerpt is a ledger row."},
   {"severity": "major", "title": "Kept per-service check goes silent when one same-service ledger row is unreadable",
    "evidence": "artifacts/review-evidence/T-103-r1/eob_probe2.py (ledger 97110 on 06/10/26 twice: one 130.00 parsed, one bare '130' -> LINE_UNCLEAR; EOB 97110 130.00): output 'payer checks: [LEDGER_EOB_PAID_MISMATCH 97140]' with no BILLED mismatch. Code: app/backend/billing.py:859-861 sums only parsed billed figures (_sum drops None).",
    "why_it_matters": "A second charge for the same service and day that cannot be read is listed on its row but the reconciliation the worker kept reports nothing. The row is visible; the discrepancy is not raised.",
    "fix": "If any ledger row for that service and date has an unclear or unparsed figure, raise a visible check (for example SERVICE_NOT_RECONCILED with the row cites) instead of comparing a partial sum. Do this row by row, as in B2.",
    "acceptance_test": "Ledger 97110 on 06/10/26 with a bare '130' second row and EOB 130.00 -> a visible check for 97110 is raised; a mutant that drops unclear rows from the comparison turns a test red."},
   {"severity": "major", "title": "Rate-row running balance is listed only inside its excerpt; the oracle accepts it",
    "evidence": "app/backend/billing.py:271 line['balance'] = None  # the running balance of a price row is in the excluded entry's excerpt. Probe artifacts/review-evidence/T-103-r1/rate_balance.py on row 'Charge per visit 185.00 999.00': lines = [('rate','rate','185.00')]; '999.00' occurs only in the excerpt; tests/unit/test_billing.py unaccounted() == []. Spec: billing.py:13-18 'sit on its row as an unclear figure'.",
    "why_it_matters": "The balance is a money token. A paralegal finds it only in the verbatim text, not as a figure. This is the same blind spot as B1, via the whole-row rule for rate entries.",
    "fix": "Carry the balance on the rate entry as an unclear figure (class rate, detail rate, unclear ['999.00'] or a balance figure with cents). Then the oracle needs no whole-row exception for it.",
    "acceptance_test": "Row 'Charge per visit 185.00 999.00' -> '999.00' appears in a structured figure field of the rate entry, and unaccounted() == [] with the whole-row rule for rate entries removed."},
   {"severity": "major", "title": "Fail-safe test cannot fail for tokens dropped inside payer rows or whole-row entries",
    "evidence": "tests/unit/test_billing.py:567 _WHOLE_ROW; :583 items += [(x['excerpt'], set(), True) for e in out['payer_reports'] for x in e['lines']]. Mutant M06 (billing.py:511 row['unclear'] = []): 157 passed, 0 failed (artifacts/review-evidence/T-103-r1/mutation_results.txt). Card AC and api.md:693 say the test fails if a token is missing.",
    "why_it_matters": "The test's name and the card say it guards every money token, but for EOB rows it guards nothing. A regression in EOB figure handling would pass CI.",
    "fix": "Payer rows and whole-row entries claim only the figure texts they actually list. Add the '$140', '$130' and '1O0.00' EOB probes and the rate-balance probe to PROBES.",
    "acceptance_test": "Mutant M06 turns at least one test red; the new EOB probes pass the oracle only when their figures are placed in a structured field."},
   {"severity": "minor", "title": "Docs and code disagree on 'no balance reconciliation' (BALANCE_STEP_MISMATCH)",
    "evidence": "app/backend/billing.py:4-5 docstring 'no balance reconciliation (D-052...)'; billing.py:668-679 _checks_for_line emits BALANCE_STEP_MISMATCH from charge minus paid minus adjustment per line; memory/contracts/api.md:664 'no balance reconciliation' versus api.md:692 'BALANCE_STEP_MISMATCH on the line catches a wrongly read column'.",
    "why_it_matters": "A reader of the doc will assume no balance arithmetic happens. The step check is per-line arithmetic, not a total. Whether it is allowed under D-052 is Chris's ruling (questions_for_chris).",
    "fix": "Either reword the docstring and api.md to 'no balance sum and no cross-line reconciliation', or drop the check, once Chris rules.",
    "acceptance_test": "grep for 'no balance reconciliation' agrees with the code; a test pins the ruling."},
   {"severity": "minor", "title": "detail carries two different things (reason for ledger rows, kind for extra lines)",
    "evidence": "app/backend/billing.py:810 ledger rows set detail to reversal, balance_only or None; extra lines (billing.py:821 extra()) carry rate, estimate, reduction, lien_amount, asserted_balance, stated_total_<kind>, balance_forward. tests/unit/test_billing.py:567 _WHOLE_ROW keys on these strings.",
    "why_it_matters": "A client has to know which kind of detail it is reading. The oracle's leniency also depends on those strings.",
    "fix": "Split into a closed 'kind' list for what the line is and a 'reason' for why it is listed; document both in api.md.",
    "acceptance_test": "Every line has kind from a closed list; a test pins the list."},
   {"severity": "nit", "title": "Printed totals and balance forwards sit in lines with class unclear and a figure field, not billed",
    "evidence": "Probe output for table_balance_forward and sample_ledger: EXTRA class=unclear detail=stated_total_billed fig=445.00; EXTRA class=unclear detail=balance_forward fig=100.00.",
    "why_it_matters": "This matches the brief (printed totals as lines with detail). A consumer that sums the figure field would double count them.",
    "fix": "Say in api.md that figure fields on extra lines are never summed by the client.",
    "acceptance_test": "api.md states the rule; no test needed."}
 ],
 "whats_right": [
   "Money is whole cents throughout: no float in billing.py, fmt() is integer // and %, and the tests assert integer cents.",
   "The D-019 accepted case total is byte-identical at 2dc5be2 and 841be23 (case_03 $335.00, case_09 $275.00, sample $8,390.00); totals.py, present.py and api.py are untouched.",
   "Parser drops are caught: M02, M03, M04 and M07 each turn the random-insertion property test red, and the verifier stub (M08) turns four citation tests red."
 ],
 "questions_for_chris": [
   "Does D-052's 'no balance reconciliation' cover the per-line BALANCE_STEP_MISMATCH check (billing.py:668-679)? I read the check as allowed (no sum, no total, no complete flag), but api.md:664 says otherwise.",
   "May a per-service ledger sum be computed internally to decide whether to raise an EOB check, if it is never shown? I read D-052's 'computed or shown' as forbidding it; the row-by-row fix removes the need either way."
 ]}
```
