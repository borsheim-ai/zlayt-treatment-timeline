# Subagent: Backend: T-103 r2 strict listing (Backend: T-103 r2 strict listing)

Source: `agent-a79c4bfe221e4e191.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T06:02:09.701Z

You own board card T-103, round 2 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Read reviews/T-103-staff-engineer.md (2 blockers) and D-052. The orchestrator's call: apply D-052 strictly, with no sums or comparisons of any kind in billing.
1. Remove the per-service ledger sums and the EOB-versus-ledger paid and billed checks entirely. Billing returns only cited lines, unreconciled lines and skipped records. EOB rows are just lines, with class and detail.
2. An EOB amount with no cents must appear as a line, either unclear or as an unreconciled row with its excerpt. Extend the fail-safe accounting test to EOB records, with the reviewer's probes.

Delete the dead code. Update memory/contracts/api.md and the tests. Run `.venv/bin/python -m pytest -q tests/unit/test_billing.py`. Commit with the pathspec rule or a fresh temp index, and check that `git diff --cached --stat` lists only your files. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Never pkill. Then `board.py ac`, the handoff, and `move T-103 in_review --agent backend`. Reply in 1 line.

### User / tool · 2026-11-02T06:02:09.706Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:12.690Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-103-staff-engineer.md | head -150; grep -n \"D-052\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -40; ls app/backend; wc -l app/backend/billing.py tests/unit/test_billing.py"
}
````

### User / tool · 2026-11-02T06:02:12.788Z

**tool result**
````
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
60:| D-052 | Billing ships as a **cited line listing without provider totals** (2026-11-02, §7.4 as pre-declared on T-083). Each parsed billing line is shown with its verbatim excerpt and classification (charge, adjustment, payment, rate, unclear), and unreconciled lines are listed; no billed/paid/balance totals and no 'complete' badge are computed or shown. The existing case-level charge total (D-019, stated charges only) is unchanged. | Five review rounds kept finding ways a per-provider total could silently omit or overwrite a figure; a listing cannot hide a missing line. | T-083 staff r5 |
__init__.py
__pycache__
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
confidence.py
conflict_candidates.py
conflicts.py
credibility.py
date_convention.py
dates.py
dismissal_patterns.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judge_guard.py
judges.py
language.py
lexicon.py
lexicon_scan.py
narrative.py
pdf_checks.py
pdf_hidden.py
pdf_ocr.py
pdf_routes.py
pdf_text.py
pipeline.py
present.py
reclassify.py
rejudge.py
review.py
schemas.py
sentences.py
spanish.py
spanish_text.py
speaker.py
split_llm.py
store.py
totals.py
trace.py
why.py
     944 app/backend/billing.py
    1018 tests/unit/test_billing.py
    1962 total
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:14.988Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py"
}
````

### User / tool · 2026-11-02T06:02:15.124Z

**tool result**
````
1	"""Billing as a cited line listing (T-083, D-042, D-052). CODE ONLY: no model is asked anything here.
2	
3	What it does: every ledger line parses to billed / adjustment / paid / balance figures, each cited to its line (a verbatim excerpt of the
4	record) and classed charge, adjustment, payment, rate or unclear. NOTHING IS TOTALED here: no per-provider billed, paid or balance sum, no
5	'complete' flag, no balance reconciliation (D-052; five review rounds kept finding ways a total could silently omit a figure, and a listing
6	cannot hide a missing line). The one total in the product is the case-level charge total of stated charges (D-019, totals.py), unchanged.
7	A rate (per visit, per unit, fee schedule, UB-04 line 44) is listed as class rate; an estimate, an LOP or lien amount, a printed total
8	(UB-04 line 0001, CMS-1500 Item 28, TOTAL CHARGES, BALANCE DUE) and a balance forward are listed as class unclear with a `detail`; an EOB is a
9	payer report (its amounts restate the bill). A figure that cannot be read cleanly (OCR letters, odd decimals, a column that cannot be told
10	apart) is listed with cents None. A row that fits no layout is listed in `unreconciled`; a record the code could not parse is in
11	`skipped_records`. The analysis is computed on read, never stored, and never reaches the letter. Money is whole cents (int).
12	
13	MONEY TOKEN (D-049; the one definition the completeness pass uses). A money token is, in a billing record: (a) a number with a decimal point
14	(two decimals, or an odd decimal like 95.5, OCR letters tolerated), with or without '$'; (b) a '$' figure with no cents; or (c) a bare whole
15	number (no '$', no decimal) ONLY when it sits in an amount column (under a ledger CHARGES/PAYMENTS/ADJ/BALANCE header, a UB-04 money column, a
16	CMS-1500 charge box, a balance-forward row, or as the figure of a labelled charge/total/balance sentence in prose). A bare whole number anywhere
17	else (a stray line outside every money column, a code, a count, a year) is NOT a money token and is not accounted for. Every money token must be a
18	listed line, an unreconciled line, or sit on its row as an 'unclear' figure: the final accounting pass lists whatever no parser placed.
19	Repeated summary rows (a second TOTAL CHARGES, BALANCE DUE or balance forward, in one record or in several) are listed in full, never overwritten.
20	"""
21	import re
22	
23	from app.backend import amounts as A, dates
24	
25	# ------------------------------------------------------------------ fixed texts (closed list; the contract appendix mirrors it)
26	CHECKS = {
27	    "BALANCE_STEP_MISMATCH": "This line's running balance does not follow from the line before it, so a column may have been read wrongly.",
28	    "LINE_UNCLEAR": "A figure on this line could not be read cleanly. It is listed but not totaled.",
29	    "LEDGER_EOB_PAID_MISMATCH": "The ledger shows a different payment than the EOB for the same date and service. Neither is picked; paid versus incurred is a legal question.",
30	    "LEDGER_EOB_BILLED_MISMATCH": "The ledger's billed amount for this date and service differs from the amount billed on the EOB.",
31	    "NO_DATE_OF_SERVICE": "Charges on this statement carry no date of service; they are counted as stated but cannot be tied to a visit.",
32	    "ROW_NOT_PARSED": "This row carries a figure or a date but did not fit the form's layout, so it was not read into any column. It is listed here, not totaled; check the original.",
33	}
34	RULES = [
35	    "Every figure is listed with the line it was read from; nothing is totaled here, and a missing figure is never hidden by a sum.",
36	    "A rate (per visit, per unit, fee schedule, UB-04 line 44) is listed as a rate, never a charge; a row or sentence that says per visit/session/hour/day, each or x N is a rate even beside the word charge.",
37	    "A running balance, a printed total and an EOB's amount billed are listed or shown beside the lines and never added to them.",
38	    "LOP, lien and attorney-reduction amounts are listed apart from the charges.",
39	    "A figure that cannot be read cleanly is listed with no value.",
40	    "A row that does not fit the layout is listed as unreconciled with its text; it is never dropped.",
41	    "This view is for review only. The letter's total line is still accepted charges only.",
42	]
43	
44	# ------------------------------------------------------------------ money tokens
45	_D = r"[0-9OolISB]"           # letters OCR confuses with digits are tolerated so a noisy figure is LISTED (cents None), never silently skipped
46	_FIG = rf"\(?-?\$?(?:{_D}{{1,3}}(?:,{_D}{{3}})+|{_D}+)\.{_D}+\)?-?"
47	_NUM = re.compile(rf"(?<![\w/.])(?=[^\s]*[0-9]){_FIG}(?![\w/]|\.\d)")
48	_MONEY = re.compile(rf"(?<![\w/.])(?=[^\s]*[0-9])(?:{_FIG}|\(?-?\$\s?{_D}[0-9OolISB,]*\)?-?)(?![\w/]|\.\d)")      # a decimal figure, or a '$' figure with no cents
49	_BARE = re.compile(r"(?<![\w/.,$])\(?-?\d[\d,]*\)?-?(?![\w/]|[.,]\d)")                                            # a whole number: only read when it sits under a money column
50	_FIGX = rf"(?=[^\s]*[0-9])\(?-?\$?{_D}[0-9OolISB,]*(?:\.{_D}+)?\)?-?"                                                # a stated figure: cents optional (no cents -> listed, cents None)
51	_DATE = r"(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})"
52	_ROW = re.compile(rf"^\s*({_DATE})\s+(?:({_DATE})\s+)?(.*)$")
53	_VOID = re.compile(r"\b(?:void(?:ed)?|reverse[ds]?|reversal|rev\.?\s+chg)\b", re.IGNORECASE)
54	_NEGOTIATED = re.compile(r"\b(?:atty|attorney|lawyer)\s+(?:reduction|adj\w*|discount)|\breduced\s+to\b|\bsettlement\s+(?:reduction|discount)\b|\bin\s+full\s+satisfaction\b", re.IGNORECASE)
55	_BALFWD = re.compile(r"\bbal(?:ance)?\.?\s*(?:fwd|forward|brought\s+forward)\b|\bprevious\s+balance\b|\bprior\s+balance\b", re.IGNORECASE)
56	_COLS = {"billed": re.compile(r"\b(?:CHARGES?|BILLED)\b", re.IGNORECASE), "paid": re.compile(r"\b(?:PAYMENTS?|PMTS?|PAID)\b", re.IGNORECASE),
57	         "adjustment": re.compile(r"\b(?:ADJ(?:USTMENTS?|S)?)\b", re.IGNORECASE), "balance": re.compile(r"\b(?:BALANCE|BAL)\b", re.IGNORECASE),
58	         "rate": re.compile(r"\bRATE\b", re.IGNORECASE)}                    # a RATE column is a price list: its figures are listed as rates, never totaled
59	_DATECOLS = {"dos": re.compile(r"\b(?:DOS|SERVICE\s+DATE)\b", re.IGNORECASE), "posted": re.compile(r"\b(?:POSTED|POST\s+DATE)\b", re.IGNORECASE)}
60	TOL = 8        # characters a figure may sit away from its column header (left or right aligned) before the column is called unclear
61	
62	
63	def fmt(cents):
64	    if cents is None:
65	        return None
66	    return ("-" if cents < 0 else "") + f"${abs(cents) // 100:,}.{abs(cents) % 100:02d}"
67	
68	
69	def parse_figure(token: str) -> dict:
70	    """'(70.00)' -> {cents: -7000}, '45.00-' -> -4500, '1,234.50' -> 123450. Credit notation (parentheses, trailing or leading minus) makes it
71	    negative. Exactly two decimals are required: '95.5' or '9.999' keep their text and cents None, never rounded."""
72	    neg = token.startswith("(") or token.startswith("-") or token.endswith("-") or token.endswith(")")
73	    digits = re.sub(r"[()\-$]", "", token)
74	    cents = A.to_cents(digits) if re.fullmatch(r"[\d,]+\.\d\d", digits) else None
75	    return {"text": token, "cents": None if cents is None else (-cents if neg else cents), "usd": None if cents is None else fmt(-cents if neg else cents)}
76	
77	
78	def _mag(f):
79	    """Payment/adjustment figures are reductions: credit notation and plain positives mean the same, so the magnitude is kept. The running
80	    balance step check is what catches a column that was read the wrong way."""
81	    return {**f, "cents": None if f["cents"] is None else abs(f["cents"]), "usd": None if f["cents"] is None else fmt(abs(f["cents"]))}
82	
83	
84	def _norm(s):
85	    return " ".join(re.sub(r"[^a-z0-9]+", " ", (s or "").casefold().replace("(synthetic)", "")).split())
86	
87	
88	def _provider(rec: dict) -> str:
89	    src = (rec.get("source") or "").strip()
90	    name = re.split(r",|\s[-–—]\s", src, maxsplit=1)[0].strip()
91	    name = re.sub(r"\s+(?:itemized\s+)?(?:ledger|statement|billing|bill|claim|eob)\s*$", "", name, flags=re.IGNORECASE).strip()
92	    return name or "Unknown provider"
93	
94	
95	def _dos(raw):
96	    p = dates.parse_date(raw or "")
97	    return p["iso"] if p.get("status") == "parsed" else None
98	
99	
100	def _cite(rec, line):
101	    return {"record_no": rec["n"], "excerpt": line.strip()}
102	
103	
104	# ------------------------------------------------------------------ record forms
105	def form_of(rec: dict) -> str:
106	    """ledger_table | ledger_text | cms1500 | ub04 | eob | None, decided from the record's own words."""
107	    body = (rec.get("excerpt") or rec.get("text") or "")
108	    src = rec.get("source") or ""
109	    up = body.upper()
110	    if "EXPLANATION OF BENEFITS" in up or "THIS IS NOT A BILL" in up or re.search(r"\bEOB\b", src, re.IGNORECASE) or ("PLAN PAID" in up and "BILLED" in up):
111	        return "eob"
112	    if "UB-04" in up or "UB04" in up or "CMS-1450" in up or "47 TOTAL CHARGES" in up or re.search(r"\bUB-?04\b", src, re.IGNORECASE):
113	        return "ub04"
114	    if "TOTAL CHARGE" in up and "AMOUNT PAID" in up or "1500" in src or "HEALTH INSURANCE CLAIM FORM" in up:
115	        return "cms1500"
116	    if _header(body.split("\n"))[0] is not None:
117	        return "ledger_table"
118	    if "$" in body and (A._is_billing_source(src) or re.search(r"\bitemized\s+(?:ledger|statement)\b|\bledger\b", body, re.IGNORECASE)):
119	        return "ledger_text"
120	    return None
121	
122	
123	def _header(lines):
124	    """(index, {kind: (start, end)}) of the ledger column header, or (None, None). Needs billed and balance and one more column."""
125	    for i, ln in enumerate(lines):
126	        if _ROW.match(ln) or re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or "$" in ln or not re.search(r"\S\s{2,}\S", ln):
127	            continue          # a header is a spaced-out row of column names: a sentence with a '$' figure is prose
128	        cols = {}
129	        for kind, rx in _COLS.items():
130	            m = rx.search(ln)
131	            if m:
132	                cols[kind] = (m.start(), m.end())
133	        if "billed" in cols and "balance" in cols and len([k for k in cols if k != "rate"]) >= 3:
134	            return i, cols
135	    return None, None
136	
137	
138	def _column(token_span, cols):
139	    """The column whose header the figure sits under (left- or right-aligned), or None when two are equally near or none within TOL."""
140	    s, e = token_span
141	    d = sorted((min(abs(s - hs), abs(e - he)), kind) for kind, (hs, he) in cols.items())
142	    if d[0][0] > TOL or (len(d) > 1 and d[1][0] == d[0][0]):
143	        return None
144	    return d[0][1]
145	
146	
147	# ------------------------------------------------------------------ itemized ledger table
148	def _rate_entry(rec, fig, excerpt, why="A rate (per visit, per unit) is a price, not a charge.", kind="rate"):
149	    return {"record_no": rec["n"], "kind": kind, "why": why, "figure": fig, "excerpt": excerpt}
150	
151	
152	def _nt(text):
153	    """A figure's text with the money furniture removed, so '$65.00', '65.00' and '(65.00)' compare equal."""
154	    return re.sub(r"[$()\s-]", "", text or "")
155	
156	
157	def _blank_dates(ln):
158	    return re.sub(_DATE, lambda m: " " * len(m.group(0)), ln)
159	
160	
161	def _tokens(ln, cols=None, all_bare=False):
162	    """Money-shaped tokens of a ledger line, in text order: decimals, '$' figures without cents and, only when `cols` is given, whole numbers that
163	    sit under a money column header (`all_bare`: every whole number on the line, for a balance-forward row). Dates are never tokens. Nothing here
164	    decides what a token means; every caller must place it or list it."""
165	    found = list(_MONEY.finditer(ln))
166	    if cols or all_bare:
167	        plain = _blank_dates(ln)
168	        found += [m for m in _BARE.finditer(plain) if (all_bare or _column(m.span(), cols) is not None) and not any(m.start() < f.end() and f.start() < m.end() for f in found)]
169	    return sorted(found, key=lambda m: m.start())
170	
171	
172	def _put_stated(rec, stated, new, out):
173	    """Record the totals a statement prints. A second figure for the same total (equal or different) is never guessed between or silently
174	    absorbed: the earlier one is listed as an unparsed line (the paralegal sees it, the provider is incomplete), the later one is kept (D-049)."""
175	    for k, v in new.items():
176	        old = stated.get(k)
177	        if old:
178	            out.append(_blank_line(rec, "ledger", old["cite"]["excerpt"], unparsed=True, unclear=[old["text"]]))
179	        stated[k] = v
180	
181	
182	def _stated_orphans(rec, lform, got, stated):
183	    """A printed total that could not be read (cents None), or that belongs to a statement with no readable line at all, is listed as an unparsed
184	    line with the total's own excerpt: the provider is incomplete, and the figure is not left only in a field nobody opens."""
185	    by_ex = {}
186	    for v in stated.values():
187	        if v["cents"] is None or not got:
188	            by_ex.setdefault(v["cite"]["excerpt"], []).append(v["text"])
189	    return [_blank_line(rec, lform, ex, unparsed=True, unclear=texts) for ex, texts in by_ex.items()]
190	
191	
192	def _family(form):
193	    """Ledger tables and ledger prose are one family (a statement); each claim form is its own."""
194	    return "ledger" if (form or "ledger").startswith("ledger") else form
195	
196	
197	def _near(span, hdr):
198	    return min(abs(span[0] - hdr[0]), abs(span[1] - hdr[1]))
199	
200	
201	def _ledger_table(rec, lines):
202	    """(lines, stated totals, balance-forward rows [list], rate entries). A row whose description carries a rate cue and whose CHARGES figure was found (read
203	    or not) is a price, not a charge: it goes to the rate entries and into no total. Every other line that carries a figure and is not a clean
204	    dated row (above the header, below it, a total it cannot place) is emitted as an unparsed line (unclear, not totaled), never dropped."""
205	    hi, cols = _header(lines)
206	    dcols = {k: (m.start(), m.end()) for k, rx in _DATECOLS.items() for m in [rx.search(lines[hi])] if m}
207	    out, stated, balfwd, rates = [], {}, [], []
208	
209	    def unparsed(ln, toks):
210	        out.append(_blank_line(rec, "ledger", ln, unparsed=True, unclear=[parse_figure(t.group(0))["text"] for t in toks]))
211	
212	    for ln in lines[:hi]:                             # a figure above the column header is listed too
213	        if _tokens(ln):
214	            unparsed(ln, _tokens(ln))
215	    for ln in lines[hi + 1:]:
216	        if re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or re.search(r"\bBALANCE\s+DUE\b", ln, re.IGNORECASE):
217	            new = _stated(rec, ln)
218	            _put_stated(rec, stated, new, out)
219	            mine, left = {_nt(v["text"]) for v in new.values()}, []
220	            for t in _tokens(ln):
221	                f, kind = parse_figure(t.group(0)), _column(t.span(), cols)
222	                if _nt(t.group(0)) in mine:
223	                    continue
224	                if kind in ("billed", "paid", "adjustment", "balance") and f["cents"] is not None and kind not in stated:
225	                    stated[kind] = {**(_mag(f) if kind in ("paid", "adjustment") else f), "cite": _cite(rec, ln)}      # a totals row printed under the columns
226	                else:
227	                    left.append(t)
228	            if left:
229	                unparsed(ln, left)
230	            continue
231	        if _BALFWD.search(ln):
232	            toks = _tokens(ln, all_bare=True)
233	            if toks:
234	                bf = {**parse_figure(toks[-1].group(0)), "cite": _cite(rec, ln)}
235	                if bf["cents"] is None or len(toks) > 1:
236	                    unparsed(ln, toks if bf["cents"] is None else toks[:-1])
237	                if bf["cents"] is not None:
238	                    balfwd.append(bf)          # every forward row is kept; analyze() lists them all when a provider has more than one
239	            continue
240	        m = _ROW.match(ln)
241	        figs = _tokens(ln, cols)
242	        if not m:
243	            if figs:                                  # a figure on a line that is not a dated row: listed, not totaled (the caller may drop it if it is a rate or LOP line)
244	                unparsed(ln, figs)
245	            continue
246	        head = ln[:figs[0].start()] if figs else ln
247	        row_m = _ROW.match(head + " ")
248	        parts = (row_m.group(3) if row_m else "").split(None, 1)
249	        code = parts[0] if parts and re.fullmatch(r"[A-Za-z0-9]{2,7}", parts[0]) and (len(parts) > 1 or not figs) else None
250	        desc = (parts[1] if code and len(parts) > 1 else " ".join(parts)).strip() if parts else ""
251	        dos, posted = m.group(1), m.group(2)
252	        if posted is None and len(dcols) == 2 and _near((m.start(1), m.end(1)), dcols["posted"]) < _near((m.start(1), m.end(1)), dcols["dos"]):
253	            dos, posted = None, m.group(1)            # the only date sits under POSTED: the DOS cell is blank, the posting date is not a service date
254	        line = _blank_line(rec, "ledger", ln, dos=dos, posted=posted, code=code, description=desc)
255	        ratey, row_rate = A.has_rate_cue(desc, unit_notation=True), False
256	        for fm in figs:
257	            kind = _column(fm.span(), cols)
258	            f = parse_figure(fm.group(0))
259	            if kind == "billed" and ratey:           # a price, whether or not its cents could be read: listed once, never a line
260	                rates.append(_rate_entry(rec, f, ln.strip(), "This row says it is a per-visit/unit/rate figure: a rate is a price, not a charge. It is not totaled."))
261	                row_rate = True
262	            elif kind is None or f["cents"] is None:
263	                line["unclear"].append(f["text"])
264	            elif kind == "rate":
265	                rates.append(_rate_entry(rec, f, ln.strip(), "This figure sits in the RATE column: a rate is a price, not a charge."))
266	            elif line[kind] is not None:
267	                line["unclear"].append(f["text"])            # two figures in one column: not guessed
268	            else:
269	                line[kind] = _mag(f) if kind in ("paid", "adjustment") else f
270	        if row_rate:
271	            line["balance"] = None                    # the running balance of a price row is in the excluded entry's excerpt
272	            if not (line["paid"] or line["adjustment"] or line["unclear"]):
273	                continue
274	        out.append(line)
275	    _put_stated(rec, stated, {k: v for k, v in _stated(rec, "\n".join(lines[hi + 1:])).items() if k not in stated}, out)
276	    return out, stated, balfwd, rates
277	
278	
279	def _blank_line(rec, form, ln, dos=None, posted=None, code=None, description="", unparsed=False, unclear=None):
280	    return {"record_no": rec["n"], "form": form, "dos": dos, "dos_iso": _dos(dos) if dos else None, "posted": posted, "code": code,
281	            "description": description, "billed": None, "adjustment": None, "paid": None, "balance": None, "unclear": list(unclear or []),
282	            "excerpt": ln.strip(), "unparsed": unparsed}
283	
284	
285	_STATED = {"billed": re.compile(rf"TOTAL\s+CHARGES?\s*[:=]?\s*({_FIGX})", re.IGNORECASE),
286	           "paid": re.compile(rf"TOTAL\s+(?:PMTS?|PAYMENTS?)\s*[:=]?\s*({_FIGX})", re.IGNORECASE),
287	           "adjustment": re.compile(rf"TOTAL\s+ADJ\w*\s*[:=]?\s*({_FIGX})", re.IGNORECASE),
288	           "balance": re.compile(rf"(?:BALANCE\s+DUE|AMOUNT\s+DUE|TOTAL\s+BALANCE)\s*[:=]?\s*({_FIGX})", re.IGNORECASE)}
289	
290	
291	def _stated(rec, text):
292	    """Totals the statement prints itself. Returned with the line they were read from; compared with the parsed lines, never used instead."""
293	    out = {}
294	    for kind, rx in _STATED.items():
295	        m = rx.search(text)
296	        if m:
297	            f = parse_figure(m.group(1))
298	            f = _mag(f) if kind in ("paid", "adjustment") else f
299	            ln = next((x for x in text.split("\n") if m.group(0) in x), m.group(0))
300	            out[kind] = {**f, "cite": _cite(rec, ln)}
301	    return out
302	
303	
304	# ------------------------------------------------------------------ ledger written as a sentence ("New patient exam charge $250.00; ...")
305	_PROSE = (("billed_total", re.compile(r"\btotal\s+(?:billed\s+)?charges?\b|\btotal\s+billed\b", re.IGNORECASE)),
306	          ("paid", re.compile(r"\bpayments?\b|\bpaid\b|\bpmts?\b", re.IGNORECASE)),
307	          ("adjustment", re.compile(r"\badjust\w*|\bdiscount\b|\bwrite-?off\b|\bcontractual\b|\bcourtesy\b|\bW/O\b", re.IGNORECASE)),
308	          ("balance", re.compile(r"\bbalance\b|\bamount\s+due\b", re.IGNORECASE)))
309	
310	
311	def _segments(text):
312	    """[(start, end)] of clauses: split at ; ! ? newline and a period that ends a sentence (not the decimal point of a figure)."""
313	    out, pos = [], 0
314	    for m in re.finditer(r"(?<=[;!?])\s+|\n|(?<=[a-zA-Z)\d])\.(?=\s+[A-Z])\s*", text):
315	        out.append((pos, m.start() + (1 if text[m.start()] == "." else 0)))
316	        pos = m.end()
317	    out.append((pos, len(text)))
318	    return [(s, e) for s, e in out if text[s:e].strip()]
319	
320	
321	def _ledger_text(rec, body):
322	    """(lines, stated totals, rate entries, balance-forward figures). A figure the classifier calls a rate, or a charge-worded figure whose sentence also carries a rate cue
323	    (per visit/session/hour/day, each, x N, daily rate), is a price: listed as a rate, never a line. An estimate is listed as excluded. Every other
324	    figure is either a charge (a line), a paid/adjustment/balance/total by its label, or an unparsed line with its text: an unlabelled figure is
325	    never totaled and never dropped."""
326	    lines, stated, rates, fwds = [], {}, [], []
327	    for s, e in _segments(body):
328	        seg = body[s:e]
329	        bad, spans = [], []
330	        for a in A.find_amounts(seg):
331	            spans.append((a["start"], a["end"]))
332	            if a["cents"] is None:
333	                bad.append(a["raw"])                         # unreadable (OCR letters, odd decimals, injected text): listed with its text
334	                continue
335	            label = A._label(seg, a["start"])
336	            neg = seg[max(0, a["start"] - 1):a["start"]] == "-" or label.endswith("-")
337	            raw = ("-" if neg else "") + a["raw"]
338	            fig = {"text": raw, "cents": -a["cents"] if neg else a["cents"], "usd": fmt(-a["cents"] if neg else a["cents"])}
339	            kind = next((k for k, rx in _PROSE if rx.search(label)), None)
340	            cite = _cite(rec, seg)
341	            cls = A.classify(seg, a, source=rec.get("source"))
342	            if cls == "rate" or (kind is None and cls == "charge" and A.has_rate_cue(seg)):
343	                rates.append(_rate_entry(rec, {k: v for k, v in fig.items()}, seg.strip()))
344	            elif kind == "billed_total":
345	                _put_stated(rec, stated, {"billed": {**fig, "cite": cite}}, lines)
346	            elif kind in ("paid", "adjustment"):
347	                lines.append(_pline(rec, seg, kind, _mag(fig)))
348	            elif kind == "balance" and _BALFWD.search(label):
349	                fwds.append({**fig, "cite": cite})           # 'Previous balance' is where the account stood before these charges, not the statement's balance
350	            elif kind == "balance":
351	                _put_stated(rec, stated, {"balance": {**fig, "cite": cite}}, lines)
352	            elif cls == "charge":
353	                lines.append(_pline(rec, seg, "billed", fig))
354	            elif cls == "estimate":
355	                rates.append(_rate_entry(rec, fig, seg.strip(), "An estimate is not a charge. It is not totaled.", kind="estimate"))
356	            else:
357	                bad.append(raw)                              # no label the code recognises: listed, not totaled, never guessed to be a charge
358	        for m in _NUM.finditer(seg):                         # a decimal figure with no '$'
359	            if not any(m.start() < e2 and s2 < m.end() for s2, e2 in spans):
360	                bad.append(m.group(0))
361	        if bad:
362	            lines.append(_blank_line(rec, "ledger", seg, description=seg.strip(), unparsed=True, unclear=bad))
363	    return lines, stated, rates, fwds
364	
365	
366	def _pline(rec, seg, kind, fig):
367	    line = _blank_line(rec, "ledger", seg, description=seg.strip())
368	    line[kind] = fig
369	    return line
370	
371	
372	# ------------------------------------------------------------------ CMS-1500 service lines (24F is implied-cents)
373	_AMT = r"(?:\d+\.\d{2}(?![\d.])|[0-9O]+(?:\s*\|\s*[0-9O]{2}|[ ][0-9O]{2}(?![\d.O]))?)"      # a printed decimal point is honoured; the usual box has none
374	_CDATE = r"(?:[0-9O]{6}|\d{1,2}/\d{1,2}/\d{2,4})"
375	_CMS = re.compile(rf"^\s*(?:24\.\s*)?({_CDATE})\s+({_CDATE})\s+(\d{{2}})\s+([A-Z0-9]{{5}})(?:\s+[A-Z0-9]{{1,4}})*?\s+({_AMT})\s+(\d+)(?:\s+(\S+))?\s*$")
376	_CMS_TOTAL = re.compile(rf"\bTOTAL\s+CHARGE\s+({_AMT}|{_FIG})")
377	_CMS_PAID = re.compile(rf"\bAMOUNT\s+PAID\s+({_AMT}|{_FIG})")
378	_CMS_MONEY = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?|(?<![\w/.])[0-9OolISB,]*\d[0-9OolISB,]*\.[0-9OolISB]{2}(?![\d.\w])|(?<![\w/.])\d+\s*\|\s*[0-9O]{2}\b")      # a printed '$' figure, a decimal figure or a boxed 85 | 00
379	
380	
381	def box_amount(raw: str) -> dict:
382	    """A CMS-1500 money box has no decimal point: '85 | 00', '85 00' and '8500' are all $85.00. A printed decimal point is honoured.
383	    OCR letters (O for 0) keep the text, cents None."""
384	    raw = raw.strip()
385	    if "O" in raw.upper().replace("|", ""):
386	        return {"text": raw, "cents": None, "usd": None, "implied_decimal": True}
387	    if re.fullmatch(_FIG, raw):
388	        return {**parse_figure(raw), "implied_decimal": False}
389	    if "|" in raw:
390	        d, c = [x.strip() for x in raw.split("|")]
391	        cents = int(d) * 100 + int(c)
392	    elif re.fullmatch(r"\d+ \d\d", raw):
393	        d, c = raw.split(" ")
394	        cents = int(d) * 100 + int(c)
395	    elif re.fullmatch(r"\d{3,}", raw):
396	        cents = int(raw)
397	    else:
398	        return {"text": raw, "cents": None, "usd": None, "implied_decimal": True}
399	    return {"text": raw, "cents": cents, "usd": fmt(cents), "implied_decimal": True}
400	
401	
402	def _cms1500(rec, lines):
403	    out, stated = [], {}
404	    for ln in lines:
405	        m = _CMS.match(ln)
406	        if m:
407	            fig = box_amount(m.group(5))
408	            line = {"record_no": rec["n"], "form": "cms1500", "dos": m.group(1) if m.group(1) == m.group(2) else f"{m.group(1)}-{m.group(2)}", "dos_iso": None,
409	                    "posted": None, "code": m.group(4), "description": f"units {m.group(6)}", "billed": None, "adjustment": None, "paid": None,
410	                    "balance": None, "unclear": [], "excerpt": ln.strip(), "units": int(m.group(6))}
411	            if fig["cents"] is None:
412	                line["unclear"].append(fig["text"])
413	            else:
414	                line["billed"] = fig
415	            out.append(line)
416	        else:
417	            hit = False
418	            for kind, rx in (("billed", _CMS_TOTAL), ("paid", _CMS_PAID)):
419	                t = rx.search(ln)
420	                if t:
421	                    hit = True
422	                    stated[kind] = {**box_amount(t.group(1)), "cite": _cite(rec, ln)}      # unreadable ones keep cents None and are listed by the caller
423	            if hit:
424	                continue
425	            toks = [t.group(0).strip() for t in _CMS_MONEY.finditer(ln)]
426	            rest = re.match(rf"^\s*(?:24\.\s*)?{_CDATE}\s+(?:{_CDATE}\s+)?(.*)$", ln)
427	            if toks or (rest and re.search(r"\d", rest.group(1))):      # carries a money figure, or is dated and has digits, but did not fit the 24 layout: listed, never dropped
428	                out.append(_blank_line(rec, "cms1500", ln, unparsed=True, unclear=toks))      # the row excerpt is in the entry; only money tokens are figures
429	    return out, stated
430	
431	
432	# ------------------------------------------------------------------ UB-04 (FL 44 rate is never a charge; FL 47 is; 0001 is the total)
433	_UBROW = re.compile(r"^\s*(\d{4})\s+(\S.*?)(?:\s{2,}|$)")
434	
435	
436	def _ub_header(lines):
437	    hi = next((i for i, ln in enumerate(lines) if re.search(r"TOTAL\s+CHARGES", ln, re.IGNORECASE) and re.search(r"\bREV\b|SERV", ln)), None)
438	    if hi is None:
439	        return None, {}
440	    cols = {}
441	    for kind, rx in (("rate", r"HCPCS/RATE|RATE"), ("billed", r"TOTAL\s+CHARGES"), ("noncovered", r"NON-COVERED")):
442	        m = re.search(rx, lines[hi])
443	        if m:
444	            cols[kind] = (m.start(), m.end())
445	    return hi, cols
446	
447	
448	def _ub04(rec, lines):
449	    hi, cols = _ub_header(lines)
450	    if hi is None:
451	        return [], {}, []
452	    out, rates, stated = [], [], {}
453	    for ln in lines[hi + 1:]:
454	        m = _UBROW.match(ln)
455	        if not m:
456	            toks = [t.group(0) for t in _tokens(ln)]
457	            if toks:                                  # a figure on a line that is not a revenue-code row: listed, never dropped
458	                out.append(_blank_line(rec, "ub04", ln, unparsed=True, unclear=toks))
459	            continue
460	        figs = [(f, _column(f.span(), cols)) for f in _tokens(ln)]
461	        if m.group(1) == "0001":
462	            for f, k in figs:
463	                if k == "billed":
464	                    stated["billed"] = {**parse_figure(f.group(0)), "cite": _cite(rec, ln)}
465	            continue
466	        line = {"record_no": rec["n"], "form": "ub04", "dos": None, "dos_iso": None, "posted": None, "code": m.group(1), "description": m.group(2).strip(),
467	                "billed": None, "adjustment": None, "paid": None, "balance": None, "unclear": [], "excerpt": ln.strip(), "non_covered": None}
468	        sd = re.search(r"\b(\d{6})\b", ln[:figs[0][0].start()] if figs else ln)
469	        line["dos"] = sd.group(1) if sd else None
470	        for f, k in figs:
471	            p = parse_figure(f.group(0))
472	            if p["cents"] is None or k is None:
473	                line["unclear"].append(p["text"])
474	            elif k == "rate":
475	                rates.append({"record_no": rec["n"], "kind": "rate", "why": "UB-04 line 44 is a rate, not a charge.", "figure": p, "excerpt": ln.strip()})
476	            elif k == "noncovered":
477	                line["non_covered"] = p
478	            elif line["billed"] is None:
479	                line["billed"] = p
480	            else:
481	                line["unclear"].append(p["text"])
482	        out.append(line)
483	    return out, stated, rates
484	
485	
486	# ------------------------------------------------------------------ EOB (payer figures; never added to charges)
487	_EOBCOLS = (("billed", r"BILLED"), ("discount", r"DISCOUNT|NOT\s+COVERED"), ("allowed", r"ALLOWED"), ("deductible", r"DEDUCT\w*"), ("copay", r"COPAY"),
488	            ("coinsurance", r"COINS\w*"), ("plan_paid", r"PLAN\s+PAID"), ("patient_owes", r"YOU\s+MAY\s+OWE|PATIENT\s+RESP\w*"))
489	
490	
491	def _eob(rec, lines):
492	    hi = next((i for i, ln in enumerate(lines) if re.search(r"\bBILLED\b", ln) and re.search(r"PLAN\s+PAID", ln, re.IGNORECASE)), None)
493	    prov = next((re.sub(r"\s+", " ", m.group(1)).strip() for ln in lines for m in [re.match(r"\s*Provider\s*:\s*(.+?)\s*$", ln, re.IGNORECASE)] if m), None)
494	    if hi is None:
495	        return {"record_no": rec["n"], "provider": prov or _provider(rec), "lines": [], "unparsed": [_blank_line(rec, "eob", ln, unparsed=True, unclear=[t.group(0) for t in _tokens(ln)]) for ln in lines if _tokens(ln)]}
496	    order = sorted(((m.start(), k) for k, rx in _EOBCOLS for m in [re.search(rx, lines[hi], re.IGNORECASE)] if m))
497	    names = [k for _, k in order]
498	    out, unparsed = [], [_blank_line(rec, "eob", ln, unparsed=True, unclear=[t.group(0) for t in _tokens(ln)]) for ln in lines[:hi] if _tokens(ln)]
499	    for ln in lines[hi + 1:]:
500	        m = re.match(rf"^\s*({_DATE})\s+(\S+)\s+", ln)
501	        if not m:
502	            if _tokens(ln):                           # a printed EOB total row, or any figure outside a service row: listed, never dropped
503	                unparsed.append(_blank_line(rec, "eob", ln, unparsed=True, unclear=[t.group(0) for t in _tokens(ln)]))
504	            continue
505	        figs = [parse_figure(f.group(0)) for f in _NUM.finditer(ln)]
506	        row = {"record_no": rec["n"], "dos": m.group(1), "dos_iso": _dos(m.group(1)), "service": m.group(2), "excerpt": ln.strip(), "unclear": [],
507	               "codes": (ln[list(_NUM.finditer(ln))[-1].end():].strip() or None) if figs else None}
508	        if len(figs) == len(names) and all(f["cents"] is not None for f in figs):
509	            row.update({k: _mag(f) for k, f in zip(names, figs)})
510	        else:
511	            row["unclear"] = [f["text"] for f in figs]
512	        out.append(row)
513	    return {"record_no": rec["n"], "provider": prov or _provider(rec), "lines": out, "unparsed": unparsed}
514	
515	
516	# ------------------------------------------------------------------ LOP / lien amounts (listed, never totaled)
517	_LOP_SOURCE = re.compile(r"letter\s+of\s+protection|\bLOP\b|\blien\b|reduction\s+letter|assignment", re.IGNORECASE)
518	_LOP_LABEL = re.compile(r"\b(?:LOP|lien)\b[^,;]{0,25}\b(?:balance|amount)|\b(?:balance|amount)\b[^,;]{0,25}\b(?:LOP|lien)\b|\breduced\s+to\b|\baccept\w*\b[^.;]{0,50}\bsatisf\w+|"
519	                        r"\b(?:atty|attorney)\s+reduction\b|\bcurrent\s+balance\b|\bin\s+full\s+satisfaction\b", re.IGNORECASE)
520	
521	
522	def _lop_lien(rec):
523	    body = rec.get("excerpt") or rec.get("text") or ""
524	    doc = bool(_LOP_SOURCE.search(rec.get("source") or ""))
525	    out = []
526	    for s, e in _segments(body):
527	        seg = body[s:e]
528	        for a in A.find_amounts(seg):
529	            if a["cents"] is None:
530	                continue
531	            label = A._label(seg, a["start"])
532	            if not (doc or _LOP_LABEL.search(label) or _LOP_LABEL.search(seg)):
533	                continue
534	            kind = "reduction" if re.search(r"reduc|satisf", seg, re.IGNORECASE) else ("lien_amount" if re.search(r"\blien\b", seg, re.IGNORECASE) else "asserted_balance")
535	            out.append({"record_no": rec["n"], "provider": _provider(rec), "kind": kind, "label": " ".join(label.split()) or None,
536	                        "figure": {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"])}, "excerpt": seg.strip(), "in_totals": False})
537	    return out
538	
539	
540	# ------------------------------------------------------------------ D-049: the final accounting pass
541	# Every money-shaped token the record prints must end up in one of four places: a parsed figure (a line, a stated total, a balance forward), an
542	# unreconciled line, an excluded rate (or an LOP/lien amount, which is listed apart), or on its row as `unclear`. This pass reads the raw text with
543	# its OWN tokenizer, after every parser has run, and lists whatever no parser placed; the provider of such a line is complete: false.
544	_A = r"[0-9OolISB]"
545	_ACC_MONEY = re.compile(rf"\(?-?\$\s?{_A}[0-9OolISB,]*(?:\.{_A}+)?\)?-?(?![\w/])|(?<![\w/.$])\(?-?[0-9OolISB,]*[0-9][0-9OolISB,]*\.{_A}{{2}}\)?-?(?![\w/]|\.\d)")
546	_PROSE_BARE = re.compile(r"(?<![\w/.,$:#%-])\(?\d[\d,]*\)?(?![\w/%:-]|[.,]\d)")
547	_AFTER_UNIT = re.compile(r"\s*(?:visits?|units?|sessions?|days?|hours?|hrs?|minutes?|mins?|weeks?|months?|years?|yrs?|times|x\b|mg|ml|cc|of\b|per\b)", re.IGNORECASE)
548	_BEFORE_ID = re.compile(r"(?:\bx|\b(?:CPT|HCPCS|codes?|ICD(?:-10)?|invoice|inv|acct|account|claim|record|page|pg|ref|no|number|npi|id|mrn|fl|box|item|line|rev|ext|phone|tel|zip|visits|sessions|units|days|through|thru)|#)\s*[:#.]?\s*$", re.IGNORECASE)
549	_CODE5 = re.compile(r"\b(?:[A-Z]\d{4}|\d{5})\b")
550	
551	
552	def _prose_bare(u):
553	    """Whole numbers in a sentence that could be money: not part of a date, a time, a phone number, a code, a year, a count of visits/units/days."""
554	    plain, out = _blank_dates(u), []
555	    for m in _PROSE_BARE.finditer(plain):
556	        digits = re.sub(r"\D", "", m.group(0))
557	        if _AFTER_UNIT.match(plain, m.end()) or _BEFORE_ID.search(plain[:m.start()]):
558	            continue
559	        if re.fullmatch(r"(?:19|20|21)\d\d", digits) and "," not in m.group(0) or re.fullmatch(r"[79]\d{4}", digits):
560	            continue
561	        out.append(m)
562	    return out
563	
564	
565	def _cms_candidates(u):
566	    """A CMS-1500 line with a procedure code that fit no 24 layout (no dates, no units): the whole numbers after the code are its possible charge.
567	    The last one is the units box when there are two or more."""
568	    c = _CODE5.search(_blank_dates(u))
569	    if not c:
570	        return []
571	    nums = [m for m in re.finditer(r"(?<![\w/.-])\d+(?![\w/-])", _blank_dates(u)) if m.start() > c.end()]
572	    return nums[:-1] if len(nums) > 1 else nums
573	
574	
575	def _span_merge(found):
576	    """[(start, end, text)] with overlaps resolved in favour of the longer token."""
577	    out = []
578	    for a in sorted(found, key=lambda t: (t[0], -(t[1] - t[0]))):
579	        if not out or a[0] >= out[-1][1]:
580	            out.append(a)
581	    return out
582	
583	
584	def _unit_tokens(form, u, cols, below_header):
585	    found = [(m.start(), m.end(), m.group(0)) for m in _ACC_MONEY.finditer(u)]
586	    if form == "ledger_table":
587	        if below_header:
588	            found += [(m.start(), m.end(), m.group(0)) for m in _tokens(u, cols, all_bare=bool(_BALFWD.search(u)))]
589	        else:
590	            found += [(m.start(), m.end(), m.group(0)) for m in _tokens(u)]
591	    elif form == "ledger_text":
592	        found += [(m.start(), m.end(), m.group(0)) for m in _prose_bare(u)]
593	    elif form == "ub04":
594	        found += [(m.start(), m.end(), m.group(0)) for m in (_tokens(u, cols) if below_header else _tokens(u))]
595	    elif form == "cms1500":
596	        found += [(m.start(), m.end(), m.group(0).strip()) for m in _CMS_MONEY.finditer(u)]
597	        strict = _CMS.match(u)
598	        if strict:
599	            found.append((strict.start(5), strict.end(5), strict.group(5)))
600	        for rx in (_CMS_TOTAL, _CMS_PAID):
601	            t = rx.search(u)
602	            if t:
603	                found.append((t.start(1), t.end(1), t.group(1)))
604	        if not strict and not _CMS_TOTAL.search(u) and not _CMS_PAID.search(u):
605	            found += [(m.start(), m.end(), m.group(0)) for m in _cms_candidates(u)]
606	    return _span_merge(found)
607	
608	
609	def _account(rec, form, body, ls, got, stated, bfs, rates, lop):
610	    """The tokens no parser placed, as unparsed lines (one per printed row; an unparsed line already on that row is extended). `got` is mutated only
611	    by extending an existing line's `unclear`."""
612	    items = []
613	
614	    def add(ex, text):
615	        items.append([ex.strip(), _nt(text), False])
616	    for l in got:
617	        for k in _FIG_KEYS:
618	            if isinstance(l.get(k), dict) and "text" in l[k]:
619	                add(l["excerpt"], l[k]["text"])
620	        for t in l["unclear"]:
621	            add(l["excerpt"], t)
622	    for v in list(stated.values()) + list(bfs):
623	        add(v["cite"]["excerpt"], v["text"])
624	    whole = [x["excerpt"].strip() for x in list(rates) + list(lop)]      # an excluded rate / LOP entry carries its whole row (running balance included)
625	    hi, cols = _header(ls) if form == "ledger_table" else _ub_header(ls) if form == "ub04" else (None, None)
626	    units = [(body[s:e], True) for s, e in _segments(body)] if form == "ledger_text" else [(u, hi is not None and i > hi) for i, u in enumerate(ls)]
627	    lform = "ledger" if form.startswith("ledger") else form
628	    extra = []
629	    for u, below in units:
630	        us = u.strip()
631	        if not us:
632	            continue
633	        mine = next((l for l in got if l.get("unparsed") and l["excerpt"].strip() == us), None)
634	        missing = []
635	        for a, b, text in _unit_tokens(form, u, cols, below):
636	            key = _nt(text)
637	            hit = next((it for it in items if not it[2] and it[1] == key and (it[0] in us or us in it[0])), None)
638	            if hit:
639	                hit[2] = True
640	            elif any(w and (w in us or us in w) for w in whole):
641	                continue
642	            elif not (mine and form == "cms1500" and not _CMS_MONEY.search(text)):      # a bare number on a row already listed whole stays on that row's excerpt
643	                missing.append(text)
644	        if missing:
645	            if mine:
646	                mine["unclear"] += missing
647	            else:
648	                extra.append(_blank_line(rec, lform, us, description=us if form == "ledger_text" else "", unparsed=True, unclear=missing))
649	    return extra
650	
651	
652	# ------------------------------------------------------------------ assembling
653	def _line_around(body, start, end):
654	    """The whole printed line a figure sits on (a verbatim excerpt); a single-line paragraph gives the clause around it."""
655	    a, b = body.rfind("\n", 0, start) + 1, body.find("\n", end)
656	    line = body[a:(b if b >= 0 else len(body))]
657	    if len(line) > 240:
658	        for s, e in _segments(body):
659	            if s <= start < e:
660	                return body[s:e].strip()
661	    return line.strip()
662	
663	
664	def _cents(fig):
665	    return fig["cents"] if fig and fig["cents"] is not None else None
666	
667	
668	def _checks_for_line(line, prev_balance):
669	    """LINE_UNCLEAR when a figure could not be read; BALANCE_STEP_MISMATCH when this line's balance is not the previous balance plus its
670	    charge minus its payment and adjustment (only checked when every figure on the line was read)."""
671	    codes = []
672	    if line.get("unparsed"):
673	        codes.append("ROW_NOT_PARSED")
674	    elif line["unclear"]:
675	        codes.append("LINE_UNCLEAR")
676	    elif _cents(line.get("balance")) is not None and prev_balance is not None:
677	        delta = (_cents(line["billed"]) or 0) - (_cents(line["paid"]) or 0) - (_cents(line["adjustment"]) or 0)
678	        if line["balance"]["cents"] - prev_balance != delta:
679	            codes.append("BALANCE_STEP_MISMATCH")
680	    return codes
681	
682	
683	def _line_key(l):
684	    g = lambda k: (l[k] or {}).get("cents") if l.get(k) else None
685	    return (_norm(l.get("dos")), _norm(l.get("posted")), _norm(l.get("code")), _norm(l.get("description")), g("billed"), g("paid"), g("adjustment"), l.get("form"))
686	
687	
688	def _merge_duplicates(lines):
689	    """A line repeated in a later record (a re-sent statement, an attached copy) counts once and cites both. Repeats inside ONE record are real."""
690	    out, seen = [], {}
691	    for l in lines:
692	        key = _line_key(l)
693	        hit = next((o for o in seen.get(key, []) if l["record_no"] not in o["record_nos"] and l["record_no"] not in o["_taken"]), None)
694	        if hit and key[4:7] != (None, None, None):
695	            hit["record_nos"].append(l["record_no"])
696	            hit["cites"].append({"record_no": l["record_no"], "excerpt": l["excerpt"]})
697	            hit["_taken"].add(l["record_no"])
698	            continue
699	        l = {**l, "record_nos": [l["record_no"]], "cites": [{"record_no": l["record_no"], "excerpt": l["excerpt"]}], "_taken": set()}
700	        seen.setdefault(key, []).append(l)
701	        out.append(l)
702	    for l in out:
703	        l.pop("_taken")
704	    return out
705	
706	
707	def _listed_elsewhere(line, rates, lop):
708	    """True when every figure of an unparsed line is already listed with its row as a rate (excluded) or an LOP/lien amount, so listing it a second
709	    time as unreconciled would be noise. A figure on the same line that is NOT one of those keeps the line."""
710	    own = {_nt(t) for t in line["unclear"]}
711	    ex = line["excerpt"].strip()
712	    seen = {_nt(x["figure"]["text"]) for x in rates if x["excerpt"].strip() == ex}
713	    seen |= {_nt(x["figure"]["text"]) for x in lop if ex in x["excerpt"] or x["excerpt"] in ex}
714	    return bool(own) and own <= seen
715	
716	
717	def _sum(lines, kind):
718	    vals = [l[kind]["cents"] for l in lines if l.get(kind) and l[kind]["cents"] is not None]
719	    return sum(vals) if vals else None
720	
721	
722	def _tot(cents):
723	    return {"cents": cents, "usd": fmt(cents)}
724	
725	
726	def _billing_looking(rec, body):
727	    """A record that is a bill by its source label or its own words (invoice, total charges) and carries a decimal figure, but fits no known form."""
728	    src = rec.get("source") or ""
729	    return bool(_NUM.search(body) and (A._is_billing_source(src) or re.search(r"\binvoice\b|\bTOTAL\s+CHARGES?\b", body, re.IGNORECASE)))
730	
731	
732	def analyze(records: list) -> dict:
733	    """The whole analysis of a case from its ingested records (needs n, excerpt; uses text, source, duplicate_of). Pure; no I/O."""
734	    recs = [r for r in records if not r.get("duplicate_of")]
735	    lines, stated_by_rec, eobs, lop, excluded, balfwds, rec_form, checks = [], {}, [], [], [], {}, {}, []
736	    skipped = []
737	    for r in recs:
738	        body = r.get("excerpt") or r.get("text") or ""
739	        ls = body.split("\n")
740	        form = form_of(r)
741	        if r.get("injection_tag") and (form or _lop_lien(r)):      # a figure inside instruction-like text has no trusted value (D-005)
742	            skipped.append({"record_no": r["n"], "reason_code": "INJECTION_SUSPECTED"})
743	            continue
744	        rec_form[r["n"]] = form
745	        got, rates = [], []
746	        if form == "ledger_table":
747	            got, st, bf, rates = _ledger_table(r, ls)
748	            stated_by_rec[r["n"]], balfwds[r["n"]] = st, bf
749	        elif form == "ledger_text":
750	            got, st, rates, bf = _ledger_text(r, body)
751	            stated_by_rec[r["n"]], balfwds[r["n"]] = st, bf
752	        elif form == "cms1500":
753	            got, st = _cms1500(r, ls)
754	            stated_by_rec[r["n"]] = st
755	        elif form == "ub04":
756	            got, st, rates = _ub04(r, ls)
757	            stated_by_rec[r["n"]] = st
758	        elif form == "eob":
759	            eobs.append(_eob(r, ls))
760	            got = eobs[-1].pop("unparsed")
761	        elif _billing_looking(r, body):                  # a bill in a layout no parser here knows (an ambulance invoice, say): shown, not silently absent
762	            skipped.append({"record_no": r["n"], "reason_code": "UNRECOGNISED_BILLING_FORM"})
763	        if form in ("ledger_table", "ledger_text", "cms1500", "ub04"):
764	            got = got + _stated_orphans(r, "ledger" if form.startswith("ledger") else form, got, stated_by_rec.get(r["n"]) or {})
765	        if form == "ledger_table":                       # a statement's fee-schedule line is a rate and carries no date of service
766	            seen = {x["excerpt"] for x in rates}
767	            for a in A.find_amounts(body):
768	                if a["cents"] is not None and A.classify(body, a, source=r.get("source")) == "rate":
769	                    ex = _line_around(body, a["start"], a["end"])
770	                    if ex not in seen:                   # a rate row already listed once is not listed again for its second figure
771	                        seen.add(ex)
772	                        rates.append(_rate_entry(r, {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"])}, ex))
773	        lop_here = _lop_lien(r)
774	        got = [l for l in got if not (l.get("unparsed") and _listed_elsewhere(l, rates, lop_here))]
775	        if form in ("ledger_table", "ledger_text", "cms1500", "ub04"):
776	            got = got + _account(r, form, body, ls, got, stated_by_rec.get(r["n"]) or {}, balfwds.get(r["n"]) or [], rates, lop_here)      # D-049: the last word on what was lost
777	        lines += got
778	        excluded += rates
779	        lop += lop_here
780	    fwd_by_prov = {}
781	    for r in recs:
782	        for bf in balfwds.get(r["n"]) or []:
783	            fwd_by_prov.setdefault(_norm(_provider(r)), []).append((r, bf))
784	    for found_fwd in fwd_by_prov.values():
785	        if len(found_fwd) > 1:                           # several balance-forward rows for one provider: every one is listed, none is picked (D-049)
786	            for r, bf in found_fwd:
787	                lines.append(_blank_line(r, "ledger", bf["cite"]["excerpt"], unparsed=True, unclear=[bf["text"]]))
788	    stated_by_prov = {}
789	    for r in recs:                                       # a second statement's TOTAL CHARGES / BALANCE DUE (a summary row of one kind, same form family) is listed, never overwritten
790	        for k, v in (stated_by_rec.get(r["n"]) or {}).items():
791	            stated_by_prov.setdefault((_norm(_provider(r)), _family(rec_form.get(r["n"])), k), []).append((r, v))
792	    for found_st in stated_by_prov.values():
793	        found_st = list({(v["cents"], v["text"], v["cite"]["excerpt"].strip()): (r, v) for r, v in reversed(found_st)}.values())[::-1]      # a byte-identical copy of one statement is one row
794	        if len(found_st) > 1:
795	            for r, v in found_st:
796	                lines.append(_blank_line(r, _family(rec_form.get(r["n"])), v["cite"]["excerpt"], unparsed=True, unclear=[v["text"]]))
797	    by_n = {r["n"]: r for r in recs}
798	    for ln in lines:
799	        ln["provider"] = _provider(by_n[ln["record_no"]])
800	    lines = _merge_duplicates(lines)
801	    prev = {}                                            # running-balance steps follow the order printed within each record
802	    for l in lines:
803	        n = l["record_no"]
804	        bfs = balfwds.get(n) or []
805	        if n not in prev:
806	            prev[n] = bfs[0]["cents"] if len(bfs) == 1 else None
807	        l["checks"] = _checks_for_line(l, prev[n])
808	        prev[n] = l["balance"]["cents"] if l.get("balance") and l["balance"]["cents"] is not None else prev[n]
809	    for l in lines:
810	        l["detail"] = ("reversal" if (l["billed"] and (l["billed"]["cents"] or 0) < 0) or (l["billed"] and _VOID.search(l["description"] or "")) else
811	                       "balance_only" if l["balance"] and not (l["billed"] or l["paid"] or l["adjustment"] or l["unclear"]) else None)
812	        l["class"] = "charge" if l["billed"] else "payment" if l["paid"] else "adjustment" if l["adjustment"] else "unclear"
813	        l["negotiated"] = bool(l["adjustment"] and _NEGOTIATED.search(l["description"] or ""))
814	        l["unparsed"] = bool(l.get("unparsed"))
815	        if l["form"] == "ledger" and l["billed"] and not l["dos"]:
816	            l["checks"].append("NO_DATE_OF_SERVICE")
817	    parsed = [l for l in lines if not l["unparsed"]]
818	    unreconciled = [{"provider": l["provider"], "record_no": l["record_no"], "form": l["form"], "class": "unclear", "reason_code": "ROW_NOT_PARSED",
819	                     "message": CHECKS["ROW_NOT_PARSED"], "excerpt": l["excerpt"], "figures": l["unclear"]} for l in lines if l["unparsed"]]
820	
821	    def extra(n, cls, detail, fig, excerpt, why):
822	        """A cited line that is not a ledger row: a rate, an estimate, an LOP/lien amount, a printed total or a balance forward."""
823	        f = rec_form.get(n)
824	        return {"class": cls, "detail": detail, "provider": _provider(by_n[n]), "record_no": n, "record_nos": [n], "form": _family(f) if f else None,
825	                "figure": fig, "why": why, "excerpt": excerpt, "cites": [{"record_no": n, "excerpt": excerpt}]}
826	    extras = [extra(x["record_no"], "rate" if x["kind"] == "rate" else "unclear", x["kind"], x["figure"], x["excerpt"], x["why"]) for x in excluded]
827	    extras += [extra(x["record_no"], "unclear", x["kind"], x["figure"], x["excerpt"], "An LOP, lien or reduction amount is listed apart from the charges.") for x in lop]
828	    listed_apart = list(extras)
829	    shown, by_key = {(u["record_no"], u["excerpt"].strip(), t) for u in unreconciled for t in u["figures"]}, {}
830	    for r in recs:                                       # a printed total or a balance forward is a line too (a copy of one statement is one line citing both records)
831	        for kind, v in list((stated_by_rec.get(r["n"]) or {}).items()) + [("balance_forward", bf) for bf in balfwds.get(r["n"]) or []]:
832	            ex = v["cite"]["excerpt"]
833	            if (r["n"], ex.strip(), v["text"]) in shown or any(e["record_no"] == r["n"] and _nt(e["figure"]["text"]) == _nt(v["text"]) and (e["excerpt"] in ex or ex in e["excerpt"]) for e in listed_apart):
834	                continue                                 # already listed with its row (unreconciled, a rate or an LOP amount)
835	            key = (_norm(_provider(r)), kind, v["text"], ex.strip())
836	            if key in by_key:
837	                if r["n"] not in by_key[key]["record_nos"]:
838	                    by_key[key]["record_nos"].append(r["n"])
839	                    by_key[key]["cites"].append({"record_no": r["n"], "excerpt": ex})
840	                continue
841	            by_key[key] = extra(r["n"], "unclear", kind if kind == "balance_forward" else f"stated_total_{kind}", {k: v[k] for k in ("text", "cents", "usd")}, ex,
842	                                "A figure the statement prints itself. It is listed, never added to the lines.")
843	            extras.append(by_key[key])
844	    listing = sorted(parsed + extras, key=lambda l: l["record_no"])
845	    for i, l in enumerate(listing, 1):
846	        l["id"] = f"b{i}"
847	    for i, u in enumerate(unreconciled, 1):
848	        u["id"] = f"u{i}"
849	    # EOB cross-checks against the matching provider's ledger lines
850	    payer = []
851	    for e in eobs:
852	        match = next((l["provider"] for l in parsed if l["form"] == "ledger" and (_norm(l["provider"]) in _norm(e["provider"]) or _norm(e["provider"]) in _norm(l["provider"]))), None)
853	        ledger_ls = [l for l in parsed if l["form"] == "ledger" and l["provider"] == match]
854	        e["matched_provider"] = match
855	        e["not_added_note"] = "The EOB restates the provider's charge; its amounts are never added to the charges."
856	        e["checks"] = []
857	        for el in e["lines"] if match else []:
858	            led = [l for l in ledger_ls if _norm(l["code"]) == _norm(el["service"]) and ((l["dos_iso"] and l["dos_iso"] == el["dos_iso"]) or _norm(l["dos"]) == _norm(el["dos"]))]
859	            if not led or not el.get("billed"):
860	                continue
861	            lb, lp = _sum(led, "billed"), _sum(led, "paid") or 0
862	            cites = [{"record_no": el["record_no"], "excerpt": el["excerpt"]}] + [c for l in led for c in l["cites"]]
863	            if lb is not None and lb != el["billed"]["cents"]:
864	                e["checks"].append({"code": "LEDGER_EOB_BILLED_MISMATCH", "dos": el["dos"], "service": el["service"], "ledger": _tot(lb), "eob": el["billed"], "cites": cites})
865	            if el.get("plan_paid") and lp != el["plan_paid"]["cents"]:
866	                e["checks"].append({"code": "LEDGER_EOB_PAID_MISMATCH", "dos": el["dos"], "service": el["service"], "ledger": _tot(lp), "eob": el["plan_paid"], "cites": cites})
867	        for c in e["checks"]:
868	            c["message"] = CHECKS[c["code"]]
869	        payer.append(e)
870	    return {"status": "listed" if (listing or unreconciled or payer or skipped) else "none_found",
871	            "lines": listing, "unreconciled": unreconciled, "skipped_records": skipped, "payer_reports": payer, "rules": RULES}
872	
873	
874	_FIG_KEYS = ("billed", "adjustment", "paid", "balance", "discount", "allowed", "deductible", "copay", "coinsurance", "plan_paid", "patient_owes", "non_covered")
875	
876	
877	def _figure_like(v):
878	    return isinstance(v, dict) and isinstance(v.get("text"), str) and "cents" in v
879	
880	
881	def _in(text, excerpt):
882	    return text in excerpt or text.lstrip("-") in excerpt
883	
884	
885	def _walk(o):
886	    if isinstance(o, dict):
887	        yield o
888	        for v in o.values():
889	            yield from _walk(v)
890	    elif isinstance(o, list):
891	        for v in o:
892	            yield from _walk(v)
893	
894	
895	def verify_citations(analysis: dict, records: list) -> list:
896	    """[] when every cited excerpt anywhere in the analysis is a verbatim substring of the record it names, and every figure text sits inside the
897	    excerpt it is cited to. The reference is the record's own text (the ingested block), never the excerpt being checked. Covers lines, cites,
898	    unreconciled rows and payer-report lines and their check cites. Returns [{ref, reason}]; `for_case` puts the list in the response as
899	    `citation_failures`."""
900	    text_of = {r["n"]: (r.get("text") or r.get("excerpt") or "") for r in records}
901	    bad = []
902	    for d in _walk({k: v for k, v in analysis.items() if k != "rules"}):
903	        ref = d.get("id") or d.get("code") or "?"
904	        if "excerpt" in d and "record_no" in d:
905	            if d["excerpt"] not in text_of.get(d["record_no"], ""):
906	                bad.append({"ref": ref, "reason": "excerpt_not_verbatim"})
907	            for k, v in d.items():
908	                if k in _FIG_KEYS and _figure_like(v) and not _in(v["text"], d["excerpt"]):
909	                    bad.append({"ref": ref, "reason": f"{k}_not_in_excerpt"})
910	            if _figure_like(d.get("figure")) and not _in(d["figure"]["text"], d["excerpt"]):
911	                bad.append({"ref": ref, "reason": "figure_not_in_excerpt"})
912	    seen, out = set(), []
913	    for b in bad:
914	        k = (b["ref"], b["reason"])
915	        if k not in seen:
916	            seen.add(k)
917	            out.append(b)
918	    return out
919	
920	
921	def checked(analysis: dict, records: list) -> dict:
922	    """The analysis plus its citation check. A failure is shown (`citation_failures`, status `citation_failed`), never swallowed; nothing is dropped silently."""
923	    fails = verify_citations(analysis, records)
924	    analysis["citation_failures"] = fails
925	    if fails:
926	        analysis["status"] = "citation_failed"
927	    return analysis
928	
929	
930	def for_case(conn, case_id: str) -> dict:
931	    from app.backend import store      # imported here so unit tests of the pure functions need no database
932	    records = store.load_records(conn, case_id)
933	    return checked(analyze(records), records)
934	
935	
936	def add_routes(app, *, conn, get_case):
937	    @app.get("/api/cases/{token}/billing")
938	    def billing_get(token: str):
939	        c = conn()
940	        try:
941	            get_case(c, token)
942	            return {"billing": for_case(c, token)}
943	        finally:
944	            c.close()
945	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:37.050Z

**tool call — Bash**
````
{
 "command": "grep -rn \"payer_reports\\|LEDGER_EOB\\|not_added_note\\|matched_provider\" --include=* -r app memory/contracts tests evals tools docs spec 2>/dev/null | grep -v \"^app/backend/billing.py\" | grep -v pycache | head -40; git status --short | head; git log --oneline | head -3"
}
````

### User / tool · 2026-11-02T06:02:37.212Z

**tool result**
````
memory/contracts/api.md:685:  "payer_reports": [ { "record_no": 2, "provider": "Quoinmere Mutual Health Plan", "matched_provider": "Larkspur Hollow Physical Therapy",
memory/contracts/api.md:687:    "checks": [ {"code": "LEDGER_EOB_PAID_MISMATCH", "dos": "06/10/26", "service": "97140", "ledger": {"cents": 0, "usd": "$0.00"}, "eob": {"cents": 1600, ...}, "cites": [ {"record_no": 2, "excerpt": "..."}, {"record_no": 1, "excerpt": "..."} ], "message": "..."} ],
memory/contracts/api.md:688:    "not_added_note": "The EOB restates the provider's charge; its amounts are never added to the charges." } ],
memory/contracts/api.md:694:**Check codes (closed list, fixed message each):** `BALANCE_STEP_MISMATCH`, `LINE_UNCLEAR`, `LEDGER_EOB_PAID_MISMATCH`, `LEDGER_EOB_BILLED_MISMATCH`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). Removed by D-052: `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `CLAIM_TOTAL_MISMATCH`, `CLAIM_LEDGER_BILLED_MISMATCH`, and the response fields `providers`, `totals`, `complete`, `balance_convention`, `stated_totals`, `checks`, `line_flags`, `lop_lien`, `excluded`.
tests/unit/test_billing.py:85:    assert set(out) == {"status", "lines", "unreconciled", "skipped_records", "payer_reports", "rules"}
tests/unit/test_billing.py:268:    e = out["payer_reports"][0]
tests/unit/test_billing.py:269:    assert e["matched_provider"].startswith("Larkspur") and len(e["lines"]) == 3
tests/unit/test_billing.py:273:    assert mism == [("LEDGER_EOB_PAID_MISMATCH", "97140", 0, 1600)]       # billed agrees after the void is netted; the ledger posted no payment
tests/unit/test_billing.py:316:    assert set(b) == {"status", "lines", "unreconciled", "skipped_records", "payer_reports", "rules", "citation_failures"} and b["status"] == "listed"
tests/unit/test_billing.py:533:    assert broken(lambda o: o["payer_reports"][0]["lines"][0].update(excerpt="made up")) != []
tests/unit/test_billing.py:534:    assert broken(lambda o: o["payer_reports"][0]["checks"][0]["cites"][0].update(excerpt="made up")) != []
tests/unit/test_billing.py:583:    items += [(x["excerpt"], set(), True) for e in out["payer_reports"] for x in e["lines"]]      # a payer-report row stands for its whole row
tests/unit/test_billing.py:954:    assert out["skipped_records"] == [] and len(out["payer_reports"]) == 1
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
faee448 fix(backend): pypdf text read runs in the killed scan child; 2 PDF jobs at once, 429 busy; opaque Popup counts as a cover; RSS watchdog (T-087 r4)
1335f21 fix(backend): D-051 accept guard runs from one choke point (set_review) on accept, edit and batch; gate and trace recompute all code checks; notes withhold failing AI wording; AI-draft verdict says this summary (T-098 r3)
2dc5be2 feat(backend): billing ships as a cited line listing, no provider totals or complete flag (T-103, D-052)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:37.486Z

**tool call — Bash**
````
{
 "command": "grep -n \"eob\\|EOB\\|payer\" tests/unit/test_billing.py | head -80"
}
````

### User / tool · 2026-11-02T06:02:37.575Z

**tool result**
````
26:EOB = """SYNTHETIC RECORD - THIS IS NOT A BILL
85:    assert set(out) == {"status", "lines", "unreconciled", "skipped_records", "payer_reports", "rules"}
240:# ------------------------------------------------------------------ CMS-1500 (implied decimals), UB-04 (rate on the charge line), EOB
265:def test_eob_is_a_payer_report_and_a_ledger_eob_paid_mismatch_is_raised():
266:    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)])
267:    assert {l["record_no"] for l in out["lines"]} == {1}                     # the EOB's 235.00 billed is not a line of the ledger
268:    e = out["payer_reports"][0]
272:    mism = [(c["code"], c["service"], c["ledger"]["cents"], c["eob"]["cents"]) for c in e["checks"]]
273:    assert mism == [("LEDGER_EOB_PAID_MISMATCH", "97140", 0, 1600)]       # billed agrees after the void is netted; the ledger posted no payment
316:    assert set(b) == {"status", "lines", "unreconciled", "skipped_records", "payer_reports", "rules", "citation_failures"} and b["status"] == "listed"
525:    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB),
533:    assert broken(lambda o: o["payer_reports"][0]["lines"][0].update(excerpt="made up")) != []
534:    assert broken(lambda o: o["payer_reports"][0]["checks"][0]["cites"][0].update(excerpt="made up")) != []
583:    items += [(x["excerpt"], set(), True) for e in out["payer_reports"] for x in e["lines"]]      # a payer-report row stands for its whole row
680:    "r5_ledger_with_eob": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)],
952:def test_eob_is_a_payer_report_not_a_skip():
953:    out = one(PROBES["r5_ledger_with_eob"])
954:    assert out["skipped_records"] == [] and len(out["payer_reports"]) == 1
956:    assert u["form"] == "eob" and u["excerpt"].startswith("TOTAL") and u["figures"][0] == "235.00"      # the EOB's printed total row is listed, not dropped
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:39.902Z

**tool call — Bash**
````
{
 "command": "sed -n 1,100p tests/unit/test_billing.py; sed -n 255,320p tests/unit/test_billing.py; sed -n 515,700p tests/unit/test_billing.py; sed -n 940,1018p tests/unit/test_billing.py"
}
````

### User / tool · 2026-11-02T06:02:39.999Z

**tool result**
````
"""Billing analysis (T-083, D-042): code-only, every figure cited, nothing totaled that is not stated. SYNTHETIC ledgers from research/record-formats.md."""
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import billing as B
from app.backend import pipeline as PL
from app.backend.api import create_app
from app.db import db as DB

LEDGER = """SYNTHETIC RECORD
Larkspur Hollow Physical Therapy (SYNTHETIC)     ITEMIZED STATEMENT     Statement date: 07/31/2026
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Acct: SYN-PT-2207   Financial class: LOP
DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE
05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00
06/10/26  06/11/26  97110  Therapeutic exercise x2       130.00                         340.00
06/10/26  06/11/26  97140  Manual therapy x1              70.00                         410.00
06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00
06/10/26  06/30/26  97140  Manual therapy x1 VOID        (70.00)                        375.00
06/10/26  06/30/26  97140  Manual therapy x1              70.00                         445.00
07/15/26  07/15/26  ADJ    Courtesy discount                                 45.00-     400.00
                     TOTAL CHARGES 445.00  TOTAL PMTS 0.00  TOTAL ADJ (45.00)  BALANCE DUE 400.00
Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection."""

EOB = """SYNTHETIC RECORD - THIS IS NOT A BILL
Quoinmere Mutual Health Plan (SYNTHETIC)   Explanation of Benefits   Processed 07/22/2026
Member: Delphine Okonkwo-Vale (SYNTHETIC)  ID SYN-MBR-88231  Claim SYN-CLM-0091
Provider: Larkspur Hollow Physical Therapy (SYNTHETIC)
DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES
06/10/26  97110    130.00    52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45
06/10/26  97140     70.00    28.00     42.00    22.00    4.00    16.00      26.00     PR-1, PR-2, CO-45
06/10/26  97014     35.00    35.00      0.00     0.00    0.00     0.00       0.00     CO-97
TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00
CO-97: payment included in allowance for another service."""

CMS_CLEAN = """SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS
24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI
    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060326   060326   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060126   060326   11     97014              A      90 | 00       3      SYN-NPI-0001
    060126   060326   11     97010              A      45 | 00       3      SYN-NPI-0001
25. FED TAX ID  SYN-TIN-0001     28. TOTAL CHARGE  390 | 00     29. AMOUNT PAID  0 | 00
33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142"""

CMS_OCR = """SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS
24. 060126 060126 11 98941 AB 8500 1 SYN-NPI-0001
    060226 060226 11 98941 AB 85 00 1 SYN-NPI-0001
    O60326 060326 11 98941 AB 85|00 1 SYN-NPI-0001
    060126 060326 11 97014 A 9000 3 SYN-NPI-0001
    060126 060326 11 97010 A 45 OO 3 SYN-NPI-0001
28. TOTAL CHARGE 39000   29. AMOUNT PAID 0 00"""

UB_ROOM = """SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
1 Saltmarrow General Hospital (SYNTHETIC)   3a SYN-PCN-7730  3b SYN-IP-11902  4 0111
42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00
0450    EMERGENCY ROOM                               091526        1          1,975.00
0250    PHARMACY                                     091526       14            412.75
0300    LABORATORY                                   091526        6            688.00
0320    DX X-RAY                                     091526        2            540.00
0001    TOTAL                                        092226                   9,165.75
67 S42.201A   76 ATTENDING Dr. Rosamund Achterberg (SYNTHETIC)"""

PROSE = ("Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; "
         "total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.")

LOP = ("Letter of protection to Fennimoor Spine Clinic. The client's current balance is $4,860.00. Provider agrees to accept $3,100.00 in full satisfaction "
       "of the account. Please send an itemized statement.")


def rec(n, source, text, **kw):
    return {"n": n, "source": source, "excerpt": text, "text": text, **kw}


_GONE = {"complete", "balance_convention", "totals", "providers", "stated_totals", "stated_totals_repeated", "unreadable_providers",
         "stated_billed", "line_sum_billed", "line_flags", "negotiated_reductions", "balance_forwards"}


def one(records):
    """The analysis, with its citations verified and none of the removed total-shaped fields anywhere in it (D-052)."""
    out = B.analyze(records)
    assert B.verify_citations(out, records) == []
    assert set(out) == {"status", "lines", "unreconciled", "skipped_records", "payer_reports", "rules"}
    assert not [k for d in B._walk(out) for k in d if k in _GONE]
    return out


def rows(out, name):
    """The parsed ledger / claim-form rows of a provider (a row has billed / paid / adjustment / balance; an extra line has `figure`)."""
    return [l for l in out["lines"] if l["provider"].startswith(name) and "figure" not in l]


def detail(out, d):
    return [l for l in out["lines"] if l["detail"] == d]


def rates(out):
    return [l for l in out["lines"] if l["class"] == "rate"]


def test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total():
    out = one([rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM)])
    ls = rows(out, "Saltmarrow")
    assert [cents(l) for l in ls] == [555000, 197500, 41275, 68800, 54000]
    assert [(x["figure"]["cents"], x["detail"]) for x in rates(out)] == [(185000, "rate")]
    assert all(l["code"] != "0001" for l in ls) and detail(out, "stated_total_billed")[0]["figure"]["cents"] == 916575


def test_eob_is_a_payer_report_and_a_ledger_eob_paid_mismatch_is_raised():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)])
    assert {l["record_no"] for l in out["lines"]} == {1}                     # the EOB's 235.00 billed is not a line of the ledger
    e = out["payer_reports"][0]
    assert e["matched_provider"].startswith("Larkspur") and len(e["lines"]) == 3
    l140 = next(x for x in e["lines"] if x["service"] == "97140")
    assert l140["plan_paid"]["cents"] == 1600 and l140["codes"] == "PR-1, PR-2, CO-45"
    mism = [(c["code"], c["service"], c["ledger"]["cents"], c["eob"]["cents"]) for c in e["checks"]]
    assert mism == [("LEDGER_EOB_PAID_MISMATCH", "97140", 0, 1600)]       # billed agrees after the void is netted; the ledger posted no payment
    assert len(e["checks"][0]["cites"]) >= 3 and e["checks"][0]["cites"][0]["record_no"] == 2


def test_claim_form_and_ledger_for_one_provider_are_both_listed_each_with_its_form():
    r = [rec(1, "Brightwater Spine & Wellness, itemized ledger", "Itemized ledger, statement date 07/01/2026. Care charge $390.00. Total charges $390.00. Balance due $390.00."),
         rec(2, "Brightwater Spine & Wellness, CMS-1500", CMS_CLEAN)]
    ls = rows(one(r), "Brightwater")
    assert [(l["form"], cents(l)) for l in ls] == [("ledger", 39000)] + [("cms1500", c) for c in (8500, 8500, 8500, 9000, 4500)]


# ------------------------------------------------------------------ citations, API
def test_verify_citations_catches_an_uncited_line():
    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)]
    out = B.analyze(r)
    out["lines"][0]["cites"][0]["excerpt"] = "not in the record"
    assert B.verify_citations(out, r)[0]["reason"] == "excerpt_not_verbatim"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    return TestClient(create_app(str(tmp_path / "x.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 5000))


def _seed(client, text):
    conn = DB.connect(client.app.state.db_path)             # demo mode refuses unrecorded text over HTTP, so the case is seeded directly (code-only ingest)
    tok = DB.create_case(conn, text, now=time.time())
    PL.ingest_case(conn, tok, text, time.time())
    return conn, tok


def test_billing_route_returns_the_listing(client):
    text = ("=== Record 1 ===\nDate: 2026-06-15\nSource: Fennimoor Spine Clinic, itemized ledger\nExcerpt: \"" + PROSE + "\"\n\n"
            "=== Record 2 ===\nDate: 2026-03-26\nSource: Pellingham and Rook PLLC, correspondence (letter of protection)\nExcerpt: \"" + LOP + "\"\n")
    conn, tok = _seed(client, text)
    conn.close()
    r = client.get(f"/api/cases/{tok}/billing")
    assert r.status_code == 200
    b = r.json()["billing"]
    assert set(b) == {"status", "lines", "unreconciled", "skipped_records", "payer_reports", "rules", "citation_failures"} and b["status"] == "listed"
    assert [cents(l) for l in b["lines"] if l["class"] == "charge"] == [25000, 18000, 231000]
    assert [x["figure"]["cents"] for x in b["lines"] if x["detail"] in ("asserted_balance", "reduction")] == [486000, 310000]
    assert client.get("/api/cases/nope/billing").status_code == 404

# ------------------------------------------------------------------ the grounding verifier can fail on real output, and the API runs it
def test_verifier_reference_is_the_record_text_not_the_excerpt():
    r = [{"n": 1, "source": "Larkspur Hollow Physical Therapy, itemized statement", "excerpt": LEDGER, "text": "A"}]
    out = B.analyze(r)
    assert out["lines"] and B.verify_citations(out, r) != []                       # the excerpt is not in the record's own text
    ok = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)]
    assert B.verify_citations(B.analyze(ok), ok) == []


def test_verifier_covers_every_cite_bearing_field():
    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB),
         rec(3, "Medlark Clinic, itemized statement", "Itemized ledger, statement date 06/15/2026. Office visit $250.00. Total charges $250.00. Balance due $250.00.")]

    def broken(fn):
        out = B.analyze(r)
        fn(out)
        return B.verify_citations(out, r)
    pick = lambda o, d: next(l for l in o["lines"] if l["detail"] == d)
    assert broken(lambda o: o["payer_reports"][0]["lines"][0].update(excerpt="made up")) != []
    assert broken(lambda o: o["payer_reports"][0]["checks"][0]["cites"][0].update(excerpt="made up")) != []
    assert broken(lambda o: pick(o, "stated_total_billed").update(excerpt="made up")) != []
    assert broken(lambda o: pick(o, "stated_total_billed")["figure"].update(text="999.99")) != []          # a printed total must sit inside its own cite
    assert broken(lambda o: pick(o, "rate").update(excerpt="made up")) != []
    assert broken(lambda o: o["unreconciled"][0].update(excerpt="made up")) != []
    assert broken(lambda o: o["lines"][0]["billed"].update(text="999.99")) != []
    assert broken(lambda o: None) == []


def test_billing_route_returns_citation_failures_and_flags_the_status(client, monkeypatch):
    text = "=== Record 1 ===\nDate: 2026-06-15\nSource: Fennimoor Spine Clinic, itemized ledger\nExcerpt: \"" + PROSE + "\"\n"
    conn, tok = _seed(client, text)
    conn.close()
    clean = client.get(f"/api/cases/{tok}/billing").json()["billing"]
    assert clean["citation_failures"] == [] and clean["status"] == "listed"
    real = B.analyze

    def tampered(records):
        out = real(records)
        out["lines"][0]["cites"][0]["excerpt"] = "not in the record"
        return out
    monkeypatch.setattr(B, "analyze", tampered)
    bad = client.get(f"/api/cases/{tok}/billing").json()["billing"]
    assert bad["status"] == "citation_failed" and bad["citation_failures"][0]["reason"] == "excerpt_not_verbatim"


# ------------------------------------------------------------------ the oracle: no money-shaped token is silently missing
# Every '$' / decimal / boxed amount token a billing record prints must sit in a row the output shows: a listed line (parsed, rate, estimate, LOP,
# printed total, balance forward), an unreconciled row, or on its row as an unclear figure; or the whole record is in skipped_records.
import random
import re

_TOKEN = re.compile(r"\$\s?[\dOolISB][\dOolISB,]*(?:\.[\dOolISB]+)?|(?<![\w/.$])[\dO][\dO,]*\.[\dO]{2}(?!\w|\.\d)|(?<![\w/.])\d+\s*\|\s*\d\d\b")
_WHOLE_ROW = ("rate", "estimate", "reduction", "lien_amount", "asserted_balance")      # an excluded rate or LOP entry stands for its whole row


def _nt(t):
    return re.sub(r"[$()\s-]", "", t or "")


def _items(out):
    """(excerpt, figure texts, whole_row): every place the analysis shows a printed row."""
    items = []
    for l in out["lines"]:
        if "figure" in l:
            items.append((l["excerpt"], {_nt(l["figure"]["text"])}, l["detail"] in _WHOLE_ROW))
        else:
            items.append((l["excerpt"], {_nt(l[k]["text"]) for k in ("billed", "paid", "adjustment", "balance") if l.get(k) and l[k]["cents"] is not None} | {_nt(t) for t in l["unclear"]}, False))
    items += [(u["excerpt"], {_nt(f) for f in u["figures"]}, False) for u in out["unreconciled"]]
    items += [(x["excerpt"], set(), True) for e in out["payer_reports"] for x in e["lines"]]      # a payer-report row stands for its whole row
    return items


def unaccounted(records, out, bare=()):
    """The tokens printed in the input that no row of the output carries. `bare` names whole-number texts that are money in this input; each
    digit-bounded occurrence outside a longer token is counted as a token too. A figure whose cents is None counts only when it sits in `unclear`
    (a parsed slot with no value is not a placement). A record in skipped_records is accounted for as a whole."""
    items, missing, skipped = _items(out), [], {s["record_no"] for s in out["skipped_records"]}
    for r in records:
        if r["n"] in skipped:
            continue
        body = r["excerpt"]
        for s, e in B._segments(body):
            unit = body[s:e].strip()
            toks = list(_TOKEN.finditer(unit))
            for b in bare:
                toks += [m for m in re.finditer(r"(?<![\w/.,$])" + re.escape(b) + r"(?![\w/]|[.,]\d)", unit) if not any(m.start() < t.end() and t.start() < m.end() for t in toks)]
            for t in toks:
                hit = [(texts, whole) for ex, texts, whole in items if unit in ex or (ex in unit and t.group(0) in ex)]
                if not any(whole or _nt(t.group(0)) in texts for texts, whole in hit):
                    missing.append((t.group(0), unit))
    return missing


def cms(*lines, total=None):
    head = ("SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS\n"
            "24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI\n")
    return head + "\n".join(lines) + ("\n" + total if total else "") + "\n33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142"


CMS_SRC = "Brightwater Spine & Wellness, CMS-1500"
CMS_OK = "    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001"


def _ledger(*rows_, footer="          TOTAL CHARGES 130.00  BALANCE DUE 130.00"):
    return tbl(HEAD_TXT, [row("06/10/26", "06/11/26", "99202", "New patient exam", "130.00", "130.00"), *rows_], footer)


def _prose(*sentences, total="Total charges $250.00. Balance due $250.00."):
    return "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. " + " ".join(sentences) + " " + total


TOTALS_ROW = "TOTAL" + " " * 52 + "130.00" + " " * 26 + "130.00"          # right-aligned under CHARGES (ends col 63) and BALANCE (ends col 95)


def _fwd(*fwd_rows):
    t = tbl(HEAD_TXT, [row("06/10/26", "06/11/26", "97110", "Therapeutic exercise", "130.00", "230.00")], "          TOTAL CHARGES 130.00  BALANCE DUE 230.00")
    head, rest = t.split("\n", 1)
    return head + "\n" + "\n".join("          " + r_ for r_ in fwd_rows) + "\n" + rest


def _stmt(code, desc, charges, total, dos="06/01/26"):
    return tbl(HEAD_TXT, [row(dos, "06/02/26", code, desc, charges)], f"          TOTAL CHARGES {total}  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE {total}")


# the T-083 probe sets (r1 to r5 reviews, artifacts/review-evidence/T-083-*): each is run through the oracle
PROBES = {
    "sample_ledger": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)],
    "prose": [rec(1, "Fennimoor Spine Clinic, itemized ledger", PROSE)],
    "cms_clean": [rec(1, CMS_SRC, CMS_CLEAN)],
    "cms_no_28": [rec(1, CMS_SRC, CMS_NO_28)],
    "cms_printed_dollar": [rec(1, CMS_SRC, CMS_NO_28.replace("85.00         1", "$85.00        1") + "\n28. TOTAL CHARGE  260 | 00")],
    "cms_no_dates": [rec(1, CMS_SRC, cms(CMS_OK, "    11     98941              AB     85.00         1      SYN-NPI-0001"))],
    "cms_no_units": [rec(1, CMS_SRC, cms(CMS_OK, "    060226   060226   11     98941              AB     85.00      SYN-NPI-0001", total="28. TOTAL CHARGE  170 | 00     29. AMOUNT PAID  0 | 00"))],
    "cms_unreadable_total": [rec(1, CMS_SRC, cms(CMS_OK, total="28. TOTAL CHARGE  1O0 | 00     29. AMOUNT PAID  0 | 00"))],
    "ub04": [rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM)],
    "ub04_stray_figure": [rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM.replace("67 S42.201A", "   SURCHARGE NOTE        125.00\n67 S42.201A"))],
    "lop": [rec(1, "Letter of protection to Fennimoor Spine Clinic", LOP)],
    "table_dollar_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "$185", "315.00"), footer="          TOTAL CHARGES 315.00  BALANCE DUE 315.00"))],
    "table_bare_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "185", "315.00"), footer="          TOTAL CHARGES 315.00  BALANCE DUE 315.00"))],
    "table_rate_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Charge per visit", "185", "315.00")))],
    "table_rate_dollar_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Charge per visit", "$185", "315.00")))],
    "table_no_date": [rec(1, PT, _ledger(row("", "", "97014", "E-stim unattended", "35.00", "165.00"), footer="          TOTAL CHARGES 165.00  BALANCE DUE 165.00"))],
    "table_totals_under_columns": [rec(1, PT, _ledger(footer=TOTALS_ROW))],
    "table_total_no_cents": [rec(1, PT, _ledger(footer="          TOTAL CHARGES 130  BALANCE DUE 130.00"))],
    "table_figure_above_header": [rec(1, PT, "Previous statement balance $400.00\n" + _ledger())],
    "prose_unlabelled": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Office visit $250.00. Total charges $250.00. Balance due $250.00.")],
    "prose_balance_only": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Balance due $250.00.")],
    "prose_rate_only": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Charge per visit $185.00. Total charges $185.00. Balance due $185.00.")],
    "prose_ocr": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Physical therapy $2O0.00. Total charges $200.00. Balance due $200.00.")],
    "prose_no_dollar_sign": [rec(1, PT, _prose("Payment received 300.00."))],
    "prose_estimate": [rec(1, PT, _prose("Estimated cost of care $500.00."))],
    "prose_rates": [rec(1, PT, _prose(*PROSE_RATES))],
    "table_balance_forward": [rec(1, PT, _fwd("Balance forward  100.00"))],
    "table_two_balance_forwards": [rec(1, PT, _fwd("Balance forward  100.00", "Balance forward   50.00"))],
    "two_totals_disagree": [rec(1, PT, _prose(total="Total charges $250.00. Balance due $250.00. Total charges $310.00."))],
    "ledger_plus_claim": [rec(1, PT, _ledger()), rec(2, "Medlark Clinic, CMS-1500", cms("    060126   060126   11     98941              AB     85.00         1      SYN-NPI-0001"))],
    "r3_prose_previous_balance": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Previous balance $500.00. New patient exam charge $250.00. Total charges $250.00. Balance due $750.00.")],
    "r3_prose_previous_balance_no_due": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Previous balance $500.00. New patient exam charge $250.00. Total charges $250.00.")],
    "r3_dateless_row_dollar_no_cents": [rec(1, PT, _ledger(row("", "", "97014", "E-stim unattended", "$35", "165.00")))],
    "r3_cms_words_box": [rec(1, CMS_SRC, cms(CMS_OK, "    060426   060426   11     97010          A   ten dollars   1      SYN-NPI-0001"))],
    "r5_two_statements": [rec(1, PT, _stmt("97162", "PT eval", "210.00", "210.00")), rec(2, PT, _stmt("97110", "Therapeutic exercise", "130.00", "130.00", "06/10/26"))],
    "r5_second_claim_total": [rec(1, CMS_SRC, cms(CMS_OK, total="28. TOTAL CHARGE  85 | 00")),
                              rec(2, CMS_SRC, cms("    060226   060226   11     98941              AB     90 | 00       1      SYN-NPI-0001", total="28. TOTAL CHARGE  90 | 00"))],
    "r5_prose_two_totals": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Total charges $250.00. Total charges 99.00.")],
    "r5_prose_previous_balance_twice": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Previous balance $500.00. New patient exam charge $250.00. Previous balance $75.00. Total charges $250.00.")],
    "r5_ledger_with_eob": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)],
    "r5_skipped_ambulance": [rec(1, "Brightwater Ambulance invoice", "Brightwater Ambulance (SYNTHETIC) invoice\nALS transport 1234.00 mileage 1234.00 supplies 1234.00")],
    "r5_skipped_injection": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER, injection_tag=True)],
}
for _name, _extra in {"M2_second_total_charges": "\n          TOTAL CHARGES 99.00", "M3_second_total_bare": "\n          TOTAL CHARGES 99",
                      "M4_second_balance_due": "\n          BALANCE DUE 55.00", "M2b_second_total_equal": "\n          TOTAL CHARGES 210.00"}.items():
    PROBES[_name] = [rec(1, PT, _stmt("97162", "PT eval", "210.00", "210.00") + _extra)]

# whole numbers that are money in these inputs (D-049), with where each must end up
BARE_PROBES = {
    "P11_bare_prose_figure": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Office visit 250. Total charges $500.00.")], "250", True),
    "P12_dollar_no_cents_prose": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Office visit $250. Total charges $500.00.")], "$250", True),
    "P10_unlabelled_decimal_prose": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Office visit 250.00. Total charges $500.00.")], "250.00", True),
    "P13_bare_labelled_charge": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge 250. Total charges $250.00.")], "250", True),
    "P16_dateless_cms_bare": ([rec(1, CMS_SRC, cms(CMS_OK, "    11     98941              AB     85       1      SYN-NPI-0001"))], "85", True),
    "P16b_dateless_cms_dollar": ([rec(1, CMS_SRC, cms(CMS_OK, "    11     98941              AB     $85.00      1      SYN-NPI-0001"))], "$85.00", True),
    "P7_dateless_table_row_bare": ([rec(1, PT, _ledger(row("", "", "97014", "E-stim unattended", "35", "165.00")))], "35", True),
    "P4_balance_forward_bare": ([rec(1, PT, _fwd("Balance forward  100"))], "100", True),
    "P18_balance_forward_dollar_no_cents": ([rec(1, PT, _fwd("Balance forward  $100"))], "$100", True),
    "P15_dated_cms_bare_box": ([rec(1, CMS_SRC, cms(CMS_OK, "    060226   060226   11     98941              AB     45       1      SYN-NPI-0001"))], "45", False),
    "A_table_bare_charge": ([rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "185", "315.00")))], "185", False),
def test_repeated_prose_summary_is_unreconciled(name, token):
    assert token in figs(one(PROBES[name]))


# ---- skipped billing records
def test_unrecognised_billing_form_and_injection_are_skipped_never_none_found():
    out = one(PROBES["r5_skipped_ambulance"])
    assert [x["reason_code"] for x in out["skipped_records"]] == ["UNRECOGNISED_BILLING_FORM"] and out["status"] == "listed" and out["lines"] == []
    out = one(PROBES["r5_skipped_injection"])
    assert [x["reason_code"] for x in out["skipped_records"]] == ["INJECTION_SUSPECTED"] and out["status"] == "listed" and out["lines"] == []


def test_eob_is_a_payer_report_not_a_skip():
    out = one(PROBES["r5_ledger_with_eob"])
    assert out["skipped_records"] == [] and len(out["payer_reports"]) == 1
    (u,) = out["unreconciled"]
    assert u["form"] == "eob" and u["excerpt"].startswith("TOTAL") and u["figures"][0] == "235.00"      # the EOB's printed total row is listed, not dropped


# ---- the money-token definition (D-049): a bare whole number is a token only in an amount column
def test_bare_whole_number_on_a_stray_line_is_not_a_money_token_but_one_under_a_column_is():
    """Pins the definition in the module docstring. Fuzz class r4 finding 3: a stray '208' outside every column is not a token; the same number
    right-aligned under CHARGES is, and then it is listed."""
    base = _ledger()
    assert B._tokens("          208", B._header(base.split("\n"))[1]) == []
    assert "208" not in _texts(one([rec(1, PT, base + "\n          208")]))
    assert "208" in _texts(one([rec(1, PT, base + "\n" + " " * 61 + "208")]))
    assert "MONEY TOKEN" in B.__doc__ and "amount column" in B.__doc__


# ---- property: a random money token put anywhere in a billing record is a line, unreconciled, or its record is skipped
_BASES = {
    "table": lambda: _ledger(),
    "table_sample": lambda: LEDGER,
    "prose": lambda: PROSE,
    "cms": lambda: cms(CMS_OK, "    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001", total="28. TOTAL CHARGE  170 | 00     29. AMOUNT PAID  0 | 00"),
    "ub04": lambda: UB_ROOM,
}
_SRC = {"table": PT, "table_sample": PT, "prose": "Fennimoor Spine Clinic, itemized ledger", "cms": CMS_SRC, "ub04": "Saltmarrow General Hospital, UB-04"}
_TOKENS = ["$123.45", "123.45", "$77", "88", "(45.00)", "1,234.50", "45.00-", "$9,999", "2O0.00", "9.999", "310"]


def _insert(text, tok, rnd, base):
    """Put the token somewhere in the ledger. A whole number (no '$', no cents) is money only in an amount position (D-049): in a sentence for
    prose, right-aligned under a money column on a line of its own for a table or a UB-04. It is not put in a CMS-1500 (that form's boxes are tested by name)."""
    lines = text.split("\n")
    if re.fullmatch(r"\d+", tok):
        if base == "prose":
            return text.replace(". Balance due", f". Office visit {tok}. Balance due", 1) if rnd.random() < 0.5 else text + f" Visit fee {tok}."
        hdr, cols = B._header(lines) if base.startswith("table") else B._ub_header(lines)
        if hdr is None:
            return text
        kind = rnd.choice(sorted(k for k in cols if k != "rate"))
        lines.insert(rnd.randrange(hdr + 1, len(lines) + 1), " " * max(0, cols[kind][1] - len(tok)) + tok)
        return "\n".join(lines)
    mode = rnd.choice(["append_line", "own_line", "mid_line"])
    i = rnd.randrange(len(lines))
    if mode == "own_line":
        lines.insert(i, "          " + tok)
    elif mode == "append_line":
        lines[i] = lines[i] + "   " + tok
    else:
        cut = rnd.choice([m.end() for m in re.finditer(r"\s+", lines[i])] or [len(lines[i])])
        lines[i] = lines[i][:cut] + tok + " " + lines[i][cut:]
    return "\n".join(lines)


def test_property_a_random_money_token_is_never_silently_missing():
    rnd, n = random.Random(20261102), 0
    for _ in range(600):
        base, tok = rnd.choice(sorted(_BASES)), rnd.choice(_TOKENS)
        text = _insert(_BASES[base](), tok, rnd, base)
        recs = [rec(1, _SRC[base], text)]
        out = B.analyze(recs)
        assert B.verify_citations(out, recs) == [], (base, tok, text)
        missing = unaccounted(recs, out, bare=(tok,) if re.fullmatch(r"\d+", tok) else ())
        assert missing == [], (base, tok, missing, text)
        n += text != _BASES[base]()
    assert n > 400, n            # the token really was inserted in most draws
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:40.166Z

**tool call — Bash**
````
{
 "command": "sed -n 655,700p memory/contracts/api.md; grep -rn \"billing\" app/frontend --include=*.js --include=*.html -l | head"
}
````

### User / tool · 2026-11-02T06:02:40.255Z

**tool result**
````
Always `200` with one envelope:
- `{"status": "ok", "calibration": {...}, "message": null}`. `calibration` has exactly: `schema` (`evals.calibration/1`), `backend` (`fixture` or a live backend name), `case_count` (the sample size: golden cases pooled), `small_sample` (bool), `source_commit`, `generated_at`, `by_state` (`verified` and `needs_review`, each `{matched, total, cases[]}`), `by_type` (`entry`, `amount`, `flag`, each with the two states as `{matched, total, by_case: {case: [m, t]}}`), `not_scored` (`entry`, `amount`, `flag`, `total`) and `sentences` (`overall` and `by_type`, each state a string).
- `{"status": "missing", "calibration": null, "message": "..."}`: no file yet.
- `{"status": "invalid", "calibration": null, "message": "..."}`: the file is not a valid measurement (bad JSON or encoding, wrong schema, a count out of range, totals that do not add up, or a statement that does not quote its own `m/t`). The file's contents are never echoed; the reasons go to the server log.

Rules for the client: render `sentences.overall.verified` and `sentences.overall.needs_review` verbatim (they name the backend and the basis); never compute or show a percentage; hide the line when `calibration` is null. Nothing is invented: no default numbers appear in any state. `calibration` is served by `app/backend/calibration_route.py`; the route is registered in `create_app` and reads one fixed path.

## GET /api/cases/{token}/billing  (T-083, D-042, D-052)
Billing as a **cited line listing**. Code-only analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs. Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals`. **No provider totals, no billed/paid/balance sums, no `complete` flag, no balance reconciliation (D-052):** a listing cannot hide a missing line, a sum can. The only billing total in the product is the case-level charge total of stated charges (D-019, `totals`), unchanged. Unknown token: `404 not_found`.
```json
{ "billing": {
  "status": "listed",                         // listed | citation_failed | none_found. "listed" says only that something was found; it is not a completeness claim
  "citation_failures": [],                    // [{ref, reason}] from the grounding verifier, which the route always runs; non-empty makes status citation_failed
  "lines": [                                  // every figure the records print, in record order, each with a verbatim excerpt and its source record
    { "id": "b3", "class": "charge",          // charge | adjustment | payment | rate | unclear
      "detail": null,                         // null | "reversal" (negative or VOID charge) | "balance_only" | see the extra-line details below
      "provider": "Larkspur Hollow Physical Therapy", "record_no": 1, "record_nos": [1], "form": "ledger",    // form: ledger | cms1500 | ub04
      "dos": "06/10/26", "dos_iso": "2026-06-10", "posted": "06/11/26", "code": "97140", "description": "Manual therapy x1",
      "billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "adjustment": null, "paid": null, "balance": {"text": "410.00", "cents": 41000, "usd": "$410.00"},
      "unclear": [], "negotiated": false, "unparsed": false,
      "checks": [],                           // LINE_UNCLEAR | BALANCE_STEP_MISMATCH | NO_DATE_OF_SERVICE
      "excerpt": "06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00",   // the printed line, verbatim
      "cites": [ {"record_no": 1, "excerpt": "<same line>"} ] },                // a re-sent statement or attached copy is one line citing both records (record_nos, cites)
    { "id": "b8", "class": "rate", "detail": "rate", "provider": "...", "record_no": 1, "record_nos": [1], "form": "ledger",
      "figure": {"text": "$65.00", "cents": 6500, "usd": "$65.00"}, "why": "A rate (per visit, per unit) is a price, not a charge.",
      "excerpt": "Fee schedule: Therapeutic exercise $65.00 per unit.", "cites": [ {"record_no": 1, "excerpt": "<same>"} ] } ],
  "unreconciled": [ { "id": "u1", "provider": "...", "record_no": 1, "form": "cms1500", "class": "unclear", "reason_code": "ROW_NOT_PARSED", "message": "...",
    "excerpt": "<the row, verbatim>", "figures": ["$85.00"] } ],   // rows that carry a figure or a date but fit no layout; never dropped. `figures` holds only the money tokens, not the rest of the line
  "skipped_records": [ {"record_no": 4, "reason_code": "INJECTION_SUSPECTED"}, {"record_no": 5, "reason_code": "UNRECOGNISED_BILLING_FORM"} ],
  "payer_reports": [ { "record_no": 2, "provider": "Quoinmere Mutual Health Plan", "matched_provider": "Larkspur Hollow Physical Therapy",
    "lines": [ {"dos": "06/10/26", "service": "97140", "billed": {...}, "discount": {...}, "allowed": {...}, "deductible": {...}, "coinsurance": {...}, "plan_paid": {...}, "patient_owes": {...}, "codes": "PR-1, PR-2, CO-45", "excerpt": "...", "unclear": []} ],
    "checks": [ {"code": "LEDGER_EOB_PAID_MISMATCH", "dos": "06/10/26", "service": "97140", "ledger": {"cents": 0, "usd": "$0.00"}, "eob": {"cents": 1600, ...}, "cites": [ {"record_no": 2, "excerpt": "..."}, {"record_no": 1, "excerpt": "..."} ], "message": "..."} ],
    "not_added_note": "The EOB restates the provider's charge; its amounts are never added to the charges." } ],
  "rules": [ "Every figure is listed with the line it was read from; nothing is totaled here, ...", "..." ] } }
```
**Line classes.** `charge`, `adjustment`, `payment` come from the column or label the figure sits under (a line with several figures takes the first of charge, payment, adjustment); `rate` is a price, never a charge. `unclear` is everything else: a line whose figure could not be read, and the **extra lines** (they carry `figure` and `why` instead of the four figure fields), told apart by `detail`: `rate` (class rate), `estimate`, `lien_amount` | `asserted_balance` | `reduction` (LOP and lien amounts, listed apart from the charges), `stated_total_billed` | `stated_total_paid` | `stated_total_adjustment` | `stated_total_balance` (a total the statement prints: UB-04 line 0001, CMS-1500 Item 28 and Item 29, TOTAL CHARGES, BALANCE DUE; listed as printed, compared with nothing), `balance_forward`. A figure that is both an LOP amount and a printed balance is one line.
**Rules (tested).** Figures are whole cents; credit notation (`(70.00)`, `45.00-`, `-45.00`) makes a charge negative (`detail: reversal`) and is read as a reduction in the payment and adjustment columns (magnitude kept; `BALANCE_STEP_MISMATCH` on the line catches a wrongly read column). Ledger columns are assigned by position under the header (`CHARGES`, `PAYMENTS`, `ADJ`, `BALANCE`); two equally near columns or a figure far from every header is `unclear`, never guessed. `Bal fwd` is not a charge. A repeated line inside one record is listed twice. CMS-1500 money boxes have no decimal point: `85 | 00`, `85 00` and `8500` are all $85.00. UB-04: only FL 47 is a charge; the FL 44 figure on a room line is a `rate` and the `0001` line is a printed total. A fee-schedule or per-unit figure is a rate; a table row or a sentence that carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate; one shared test, `amounts.has_rate_cue`, also used by reclassify) is a rate even beside the word charge or billed, is listed once, and a `RATE` column's figures are rates too. A ledger-table figure with no cents (`$185`, `185`) under a money column stays on its row as `unclear` text (`LINE_UNCLEAR`); on a rate row it is a `rate` line with `cents: null`. A blank DOS cell stays blank (`dos: null`, `NO_DATE_OF_SERVICE`); the posting date is never read as the service date. A figure with OCR letters, other than two decimals, or inside an injection-tagged record has `cents: null` / the record is in `skipped_records`. A billing-looking record in no known layout is a `skipped_records` entry `UNRECOGNISED_BILLING_FORM`. EOB amounts are never lines of the ledger; a ledger-versus-EOB difference for the same date and service is raised as a check on the payer report and neither side is picked. Every cited excerpt anywhere in the response (lines, cites, unreconciled, payer lines, check cites) is checked against the record's own text, and every figure text against its excerpt, by `verify_citations`, which the route runs on every call; failures are returned as `citation_failures` and make the status `citation_failed`.
**Nothing is silently missing (D-049, tested).** After every parser has run, the code reads each billing record again with its own tokenizer and collects every money-shaped token: a `$` figure, a number with two decimals (OCR letters tolerated), and a whole number in an amount position (under a ledger or UB-04 money column, in a prose sentence, in a balance-forward row, in the box of a dateless CMS-1500 service line; dates, times, codes, years and counts of visits/units/days are not tokens; definition in the `app/backend/billing.py` docstring). Each token is a `lines` entry, an `unreconciled` row, an `unclear` figure on its row, or its whole record is in `skipped_records`. A token none of these holds is added to `unreconciled` as a `ROW_NOT_PARSED` row (one already on that row is extended). The test replays every money token of the T-083 probe sets (r1 to r5 reviews, `artifacts/review-evidence/T-083-*`) plus 600 random insertions and fails if one is missing. Repeated summary rows are never overwritten: two balance-forward rows, and a second TOTAL CHARGES / BALANCE DUE / paid / adjustment row (in one record, or in a second statement of the same provider and form family) are all listed (the earlier ones in `unreconciled`, the last as a line; a byte-identical copy of one statement is one line citing both records). A printed total on an EOB (its TOTAL row) is an `unreconciled` row of form `eob`.
**Check codes (closed list, fixed message each):** `BALANCE_STEP_MISMATCH`, `LINE_UNCLEAR`, `LEDGER_EOB_PAID_MISMATCH`, `LEDGER_EOB_BILLED_MISMATCH`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). Removed by D-052: `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `CLAIM_TOTAL_MISMATCH`, `CLAIM_LEDGER_BILLED_MISMATCH`, and the response fields `providers`, `totals`, `complete`, `balance_convention`, `stated_totals`, `checks`, `line_flags`, `lop_lien`, `excluded`.
**Ladder.** All steps are code (parse, cite, compare); there is no model step, so no judge. The human step is reading the view; none of it is exportable.

## Spanish-language records (T-085, D-042)

Languages: English and Spanish. Code detects the language of every record (`app/backend/language.py`, a stop-word and script scorer; no model). Text with no evidence for any language (numbers, codes) counts as English; anything with some non-English evidence never does (see *Uncertain language*). Short clinical Spanish lines (`RM cervical: protrusión discal C5-C6, posible estenosis foraminal derecha.`) are recognised from clinical vocabulary. Mixed English/Spanish text is supported.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:46.974Z

**tool call — Bash**
````
{
 "command": "grep -n \"BALANCE_STEP\\|checks\\b\\|\\\"checks\\\"\\|_checks_for_line\\|LINE_UNCLEAR\" tests/unit/test_billing.py | head -40; grep -rn \"BALANCE_STEP\\|billing\\.\\(checks\\|CHECKS\\)\\|billing import\" app tests evals docs spec memory --include=*.py --include=*.md --include=*.js --include=*.html -l | grep -v pycache"
}
````

### User / tool · 2026-11-02T06:02:47.082Z

**tool result**
````
107:def checks(out):
108:    return [c for l in out["lines"] for c in l.get("checks", [])]
139:    assert "BALANCE_STEP_MISMATCH" not in checks(out) and [l["excerpt"] for l in rates(out)] != []
160:    assert "BALANCE_STEP_MISMATCH" in checks(out)
166:    assert bad["billed"] is None and bad["unclear"] == ["13O.00"] and "LINE_UNCLEAR" in bad["checks"] and bad["class"] == "unclear"
272:    mism = [(c["code"], c["service"], c["ledger"]["cents"], c["eob"]["cents"]) for c in e["checks"]]
274:    assert len(e["checks"][0]["cites"]) >= 3 and e["checks"][0]["cites"][0]["record_no"] == 2
336:    assert set(checks(out)) == {"NO_DATE_OF_SERVICE"}
486:    assert l["dos"] is None and l["dos_iso"] is None and l["posted"] == "06/11/26" and "NO_DATE_OF_SERVICE" in l["checks"] and cents(l) == 3500
534:    assert broken(lambda o: o["payer_reports"][0]["checks"][0]["cites"][0].update(excerpt="made up")) != []
748:    assert bad["billed"] is None and bad["unclear"] == [fig] and bad["checks"] == ["LINE_UNCLEAR"] and bad["class"] == "unclear"
812:        assert out["unreconciled"] == [] and not [c for c in checks(out) if "BALANCE" in c and c != "BALANCE_STEP_MISMATCH"]
818:    assert checks(one([rec(1, PT, t)])) == ["BALANCE_STEP_MISMATCH"]
app/backend/billing.py
tests/unit/test_billing.py
memory/contracts/api.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:54.585Z

**tool call — Bash**
````
{
 "command": "sed -n 100,170p tests/unit/test_billing.py; sed -n 800,822p tests/unit/test_billing.py; grep -n \"^def test_\\|^def \\|^HEAD_TXT\\|^PT =\" tests/unit/test_billing.py | sed -n 1,200p | head -120"
}
````

### User / tool · 2026-11-02T06:02:54.681Z

**tool result**
````
    return [l for l in out["lines"] if l["class"] == "rate"]


def figs(out):
    return [f for u in out["unreconciled"] for f in u["figures"]]


def checks(out):
    return [c for l in out["lines"] for c in l.get("checks", [])]


def cents(l, k="billed"):
    return l[k]["cents"] if l.get(k) else None


# ------------------------------------------------------------------ itemized ledger
def test_ledger_lines_parse_to_four_figures_each_cited_and_classed():
    r = [rec(1, "Larkspur Hollow Physical Therapy (SYNTHETIC), itemized statement", LEDGER)]
    ls = rows(one(r), "Larkspur")
    assert [l["code"] for l in ls] == ["97162", "97110", "97140", "97014", "97140", "97140", "ADJ"]
    first = ls[0]
    assert (first["class"], cents(first), cents(first, "balance"), first["paid"], first["adjustment"]) == ("charge", 21000, 21000, None, None)
    assert first["dos"] == "05/27/26" and first["dos_iso"] == "2026-05-27" and first["posted"] == "05/28/26" and first["record_no"] == 1
    assert first["cites"] == [{"record_no": 1, "excerpt": first["excerpt"]}] and first["excerpt"] in LEDGER
    adj = ls[-1]
    assert adj["adjustment"]["cents"] == 4500 and adj["adjustment"]["text"] == "45.00-" and cents(adj, "balance") == 40000 and adj["class"] == "adjustment"


def test_no_per_provider_totals_no_complete_flag_no_balance_check_anywhere():
    """D-052: a listing, not a ledger reconciliation. Whatever the statement prints is a cited line; nothing is summed or compared with a sum."""
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Fennimoor Spine Clinic, itemized ledger", PROSE)])
    assert {l["provider"] for l in out["lines"]} == {"Larkspur Hollow Physical Therapy", "Fennimoor Spine Clinic"}
    assert {"LEDGER_TOTAL_MISMATCH", "LEDGER_BALANCE_MISMATCH", "CLAIM_TOTAL_MISMATCH", "CLAIM_LEDGER_BILLED_MISMATCH"}.isdisjoint(B.CHECKS)


def test_void_is_a_reversal_charge_line_and_the_running_balance_is_just_a_figure():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)])
    void = next(l for l in rows(out, "Larkspur") if "VOID" in l["description"])
    assert cents(void) == -7000 and void["class"] == "charge" and void["detail"] == "reversal"
    assert "BALANCE_STEP_MISMATCH" not in checks(out) and [l["excerpt"] for l in rates(out)] != []


def test_fee_schedule_rate_is_a_rate_line_and_never_a_charge():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)])
    assert [(x["figure"]["cents"], x["class"], x["detail"]) for x in rates(out)] == [(6500, "rate", "rate")]
    assert "Fee schedule" in rates(out)[0]["excerpt"]
    assert 6500 not in [cents(l) for l in rows(out, "Larkspur")]


def test_a_printed_total_is_a_cited_line_beside_the_rows_not_compared_with_them():
    bad = LEDGER.replace("TOTAL CHARGES 445.00", "TOTAL CHARGES 455.00")
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", bad)])
    (t,) = detail(out, "stated_total_billed")
    assert t["class"] == "unclear" and t["figure"]["cents"] == 45500 and "TOTAL CHARGES 455.00" in t["excerpt"]
    assert [cents(l) for l in rows(out, "Larkspur")][:2] == [21000, 13000] and out["unreconciled"] == []      # the rows are as printed; no verdict on the total


def test_running_balance_step_mismatch_is_flagged_on_the_line():
    bad = LEDGER.replace("410.00\n", "415.00\n", 1)
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", bad)])
    assert "BALANCE_STEP_MISMATCH" in checks(out)


def test_unreadable_figure_is_listed_with_no_value():
    txt = LEDGER.replace("130.00    ", "13O.00    ", 1)
    bad = next(l for l in rows(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", txt)]), "Larkspur") if l["code"] == "97110")
    assert bad["billed"] is None and bad["unclear"] == ["13O.00"] and "LINE_UNCLEAR" in bad["checks"] and bad["class"] == "unclear"


def test_extra_decimals_are_never_rounded():
    txt = LEDGER.replace("130.00", "130.005")
def test_prose_previous_balance_is_a_balance_forward_not_the_statement_balance():
    out = one(PROBES["r3_prose_previous_balance"])
    assert detail(out, "balance_forward")[0]["figure"]["cents"] == 50000 and detail(out, "stated_total_balance")[0]["figure"]["cents"] == 75000


def test_a_printed_balance_due_is_listed_as_printed_with_or_without_a_forward_and_no_verdict_is_given():
    """D-052: no balance reconciliation. Whatever BALANCE DUE a statement prints is a cited line, equal to the lines or not."""
    for due in ("440.00", "340.00", "500.00", "999.00"):
        t = tbl(HEAD_TXT, [row("06/01/26", "06/02/26", "97162", "PT eval", "210.00", "310.00"), row("06/10/26", "06/11/26", "97110", "Therapeutic exercise", "130.00", "440.00")],
                f"          TOTAL CHARGES 340.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE {due}").replace("\n06/01/26", "\n          Balance forward  100.00\n06/01/26", 1)
        out = one([rec(1, PT, t)])
        assert detail(out, "stated_total_balance")[0]["figure"]["text"] == due and detail(out, "balance_forward")[0]["figure"]["cents"] == 10000
        assert out["unreconciled"] == [] and not [c for c in checks(out) if "BALANCE" in c and c != "BALANCE_STEP_MISMATCH"]


def test_balance_step_mismatch_is_flagged_on_the_line_and_an_unreadable_charge_is_class_unclear():
    t = tbl(HEAD_TXT, [row("06/01/26", "06/02/26", "97162", "PT eval", "210.00", "210.00"), row("06/10/26", "06/11/26", "97110", "Therapeutic exercise", "130.00", "999.00")],
            "          TOTAL CHARGES 340.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 340.00")
    assert checks(one([rec(1, PT, t)])) == ["BALANCE_STEP_MISMATCH"]
    assert next(l for l in rows(one(BARE_PROBES["A_table_bare_charge"][0]), "Medlark") if l["code"] == "99213")["class"] == "unclear"


# ---- prose: an unlabelled figure is never a charge (pins the prose charge gate; reviewer mutant M05) and never dropped
73:def rec(n, source, text, **kw):
81:def one(records):
90:def rows(out, name):
95:def detail(out, d):
99:def rates(out):
103:def figs(out):
107:def checks(out):
111:def cents(l, k="billed"):
116:def test_ledger_lines_parse_to_four_figures_each_cited_and_classed():
128:def test_no_per_provider_totals_no_complete_flag_no_balance_check_anywhere():
135:def test_void_is_a_reversal_charge_line_and_the_running_balance_is_just_a_figure():
142:def test_fee_schedule_rate_is_a_rate_line_and_never_a_charge():
149:def test_a_printed_total_is_a_cited_line_beside_the_rows_not_compared_with_them():
157:def test_running_balance_step_mismatch_is_flagged_on_the_line():
163:def test_unreadable_figure_is_listed_with_no_value():
169:def test_extra_decimals_are_never_rounded():
174:def test_duplicate_statement_is_one_line_citing_both_records():
182:def test_two_identical_lines_inside_one_record_are_both_listed():
189:def test_balance_forward_is_a_cited_line_and_not_a_charge():
198:def test_payments_adjustments_in_their_own_columns_by_position():
211:def test_ledger_prose_statement_lists_charges_payment_adjustment_and_its_printed_figures():
220:def test_nothing_found_for_a_clinical_record():
226:def test_lop_and_lien_amounts_are_unclear_lines_apart_from_the_charges():
233:def test_atty_reduction_on_a_ledger_is_listed_as_an_lop_amount():
241:def test_cms1500_boxes_are_implied_cents_and_item_28_is_a_listed_total():
247:def test_cms1500_ocr_text_never_reads_8500_as_dollars():
257:def test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total():
265:def test_eob_is_a_payer_report_and_a_ledger_eob_paid_mismatch_is_raised():
277:def test_claim_form_and_ledger_for_one_provider_are_both_listed_each_with_its_form():
285:def test_verify_citations_catches_an_uncited_line():
293:def client(tmp_path, monkeypatch):
301:def _seed(client, text):
308:def test_billing_route_returns_the_listing(client):
322:def test_table_survives_ingest_with_the_quote_on_its_own_line_or_the_first_line(client):
334:def test_prose_charges_without_a_date_of_service_are_listed_and_flagged():
339:def test_injection_tagged_record_is_skipped_not_listed():
344:def test_duplicate_records_are_ignored_and_no_model_is_imported():
352:HEAD_TXT = "DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE"
355:def tbl(header, rows_, footer=""):
370:def row(dos, posted, code, desc, charges=None, balance=None, **kw):
380:PT = "Medlark Clinic, itemized statement"
384:def test_table_row_charge_per_visit_is_a_rate_line_listed_once(fig):
394:def test_every_rate_cue_in_a_table_row_wins_even_beside_charge(desc):
401:def test_unit_notation_x1_is_still_a_normal_charge_in_a_table_row():
410:def test_prose_rate_cue_beats_the_word_charge(sent):
417:def test_prose_rate_is_a_rate_even_when_the_printed_total_includes_it():
425:def test_one_rate_cue_function_is_shared_with_reclassify():
433:def test_rate_column_figures_are_listed_as_rates():
448:def test_cms1500_printed_decimal_is_read_not_dropped():
453:def test_cms1500_slash_dated_line_is_read():
458:def test_cms1500_line_that_does_not_fit_is_unreconciled_with_its_excerpt():
467:def test_ledger_row_with_no_date_is_unreconciled_and_its_total_is_a_line():
478:def test_a_fee_schedule_line_is_a_rate_not_an_unreconciled_row():
483:def test_blank_dos_cell_does_not_take_the_posted_date():
498:def test_a_bill_in_an_unrecognised_layout_is_skipped_visibly_not_none_found():
503:def test_a_clinical_note_with_a_dollar_amount_is_not_flagged_unrecognised():
508:def test_an_unreadable_provider_does_not_touch_another_providers_lines():
516:def test_verifier_reference_is_the_record_text_not_the_excerpt():
524:def test_verifier_covers_every_cite_bearing_field():
543:def test_billing_route_returns_citation_failures_and_flags_the_status(client, monkeypatch):
570:def _nt(t):
574:def _items(out):
587:def unaccounted(records, out, bare=()):
608:def cms(*lines, total=None):
618:def _ledger(*rows_, footer="          TOTAL CHARGES 130.00  BALANCE DUE 130.00"):
622:def _prose(*sentences, total="Total charges $250.00. Balance due $250.00."):
629:def _fwd(*fwd_rows):
635:def _stmt(code, desc, charges, total, dos="06/01/26"):
704:def _texts(out):
710:def test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped(name):
716:def test_bare_or_dateless_money_token_is_shown(name):
725:def test_oracle_is_not_vacuous():
745:def test_table_charge_with_no_cents_is_on_its_row_as_unclear(fig):
752:def test_table_rate_row_with_no_cents_is_a_rate_line_with_its_text(fig):
758:def test_table_payment_on_a_rate_row_is_kept_as_a_payment_line():
766:def test_table_totals_row_printed_under_the_columns_is_read_as_printed_totals():
771:def test_table_total_with_no_cents_is_unreconciled():
776:def test_table_figure_above_the_header_is_unreconciled():
781:def test_one_balance_forward_is_a_line_with_its_cite():
788:def test_two_balance_forward_rows_are_both_unreconciled_none_overwritten():
793:def test_balance_forward_in_two_records_of_one_provider_lists_both():
800:def test_prose_previous_balance_is_a_balance_forward_not_the_statement_balance():
805:def test_a_printed_balance_due_is_listed_as_printed_with_or_without_a_forward_and_no_verdict_is_given():
815:def test_balance_step_mismatch_is_flagged_on_the_line_and_an_unreadable_charge_is_class_unclear():
823:def test_prose_unlabelled_figure_is_unreconciled_not_a_charge():
830:def test_prose_figure_with_no_billing_word_is_unreconciled_and_its_total_is_a_line():
836:def test_prose_statement_with_only_a_printed_total_is_listed_not_none_found():
841:def test_prose_rate_only_statement_lists_the_rate_and_both_printed_totals():
846:def test_prose_unreadable_figure_is_listed_with_its_text():
850:def test_prose_decimal_figure_with_no_dollar_sign_is_unreconciled():
855:def test_prose_estimate_is_an_unclear_line_not_a_charge():
861:def test_two_different_printed_totals_are_both_listed_none_picked():
867:def test_cms1500_line_with_no_dates_is_unreconciled_with_only_its_figure():
873:def test_cms1500_line_with_no_units_lists_only_the_money_token_not_the_tail():
878:def test_cms1500_unreadable_total_is_unreconciled():
882:def test_an_unparsed_claim_line_is_unreconciled_beside_the_ledger_rows():
887:def test_ub04_line_with_a_figure_that_fits_no_revenue_row_is_unreconciled():
891:def test_dateless_cms_line_lists_only_its_money_token_and_a_worded_box_lists_none():
897:def test_dateless_table_row_lists_its_bare_charge_with_the_decimal():
902:def test_second_statement_total_never_overwrites_the_first():
907:def test_first_statement_total_is_visible_when_a_second_statement_follows():
913:def test_identical_copy_of_one_statement_is_one_line_citing_both_records():
919:def test_second_claim_form_total_is_listed_too():
924:def test_repeated_summary_row_in_one_record_is_listed_the_earlier_one_unreconciled(name, token):
929:def test_clean_statement_has_nothing_unreconciled():
933:def test_two_statements_each_with_a_forward_list_both_forwards():
940:def test_repeated_prose_summary_is_unreconciled(name, token):
945:def test_unrecognised_billing_form_and_injection_are_skipped_never_none_found():
952:def test_eob_is_a_payer_report_not_a_skip():
960:def test_bare_whole_number_on_a_stray_line_is_not_a_money_token_but_one_under_a_column_is():
982:def _insert(text, tok, rnd, base):
1007:def test_property_a_random_money_token_is_never_silently_missing():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:03:52.477Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/edit_billing.py <<'EOF'\nimport re\np = \"app/backend/billing.py\"\ns = open(p).read()\n\ndef sub(old, new, count=1):\n    global s\n    assert s.count(old) == count, (s.count(old), old[:70])\n    s = s.replace(old, new)\n\n# --- docstring\nsub(\"\"\"NOTHING IS TOTALED here: no per-provider billed, paid or balance sum, no\n'complete' flag, no balance reconciliation (D-052; five review rounds kept finding ways a total could silently omit a figure, and a listing\ncannot hide a missing line).\"\"\", \"\"\"NOTHING IS TOTALED OR COMPARED here: no sum of any kind, no\n'complete' flag, no balance step check, no ledger-versus-EOB check (D-052; five review rounds kept finding ways a total could silently omit a\nfigure, and a listing cannot hide a missing line).\"\"\")\nsub(\"\"\"balance forward are listed as class unclear with a `detail`; an EOB is a\npayer report (its amounts restate the bill).\"\"\", \"\"\"balance forward are listed as class unclear with a `detail`; an EOB service\nrow is a line of class unclear, detail `eob`, with its payer figures in `eob` (they restate the bill and are never added to it).\"\"\")\nsub(\"\"\"A row that fits no layout is listed in `unreconciled`; a record the code could not parse is in\n`skipped_records`.\"\"\", \"\"\"A row that fits no layout is listed in `unreconciled`; a record the code could not parse is in\n`skipped_records`. Billing returns only these three lists.\"\"\")\nsub(\"\"\"CMS-1500 charge box, a balance-forward row, or as the figure\"\"\", \"\"\"CMS-1500 charge box, an EOB money column, a balance-forward row, or as the figure\"\"\")\n\n# --- checks\nsub('''    \"BALANCE_STEP_MISMATCH\": \"This line's running balance does not follow from the line before it, so a column may have been read wrongly.\",\\n''', \"\")\nsub('''    \"LEDGER_EOB_PAID_MISMATCH\": \"The ledger shows a different payment than the EOB for the same date and service. Neither is picked; paid versus incurred is a legal question.\",\n    \"LEDGER_EOB_BILLED_MISMATCH\": \"The ledger's billed amount for this date and service differs from the amount billed on the EOB.\",\\n''', \"\")\nsub('''A figure on this line could not be read cleanly. It is listed but not totaled.\"''', '''A figure on this line could not be read cleanly. It is listed with its text and no value.\"''')\nsub('''    \"Every figure is listed with the line it was read from; nothing is totaled here, and a missing figure is never hidden by a sum.\",''',\n    '''    \"Every figure is listed with the line it was read from; nothing is totaled or compared here, and a missing figure is never hidden by a sum.\",''')\nsub('''    \"A running balance, a printed total and an EOB's amount billed are listed or shown beside the lines and never added to them.\",''',\n    '''    \"A running balance, a printed total and an EOB row's amounts are listed beside the lines and never added to them or checked against them.\",''')\n\n# --- _mag docstring\nsub(\"\"\"so the magnitude is kept. The running\n    balance step check is what catches a column that was read the wrong way.\"\"\", \"\"\"so the magnitude is kept.\"\"\")\n\n# --- EOB\na = s.index(\"# ------------------------------------------------------------------ EOB (payer figures; never added to charges)\")\nb = s.index(\"# ------------------------------------------------------------------ LOP / lien amounts\")\nnew_eob = '''# ------------------------------------------------------------------ EOB (payer figures; listed as lines, never added to charges or compared)\n_EOBCOLS = ((\"billed\", r\"BILLED\"), (\"discount\", r\"DISCOUNT|NOT\\\\s+COVERED\"), (\"allowed\", r\"ALLOWED\"), (\"deductible\", r\"DEDUCT\\\\w*\"), (\"copay\", r\"COPAY\"),\n            (\"coinsurance\", r\"COINS\\\\w*\"), (\"plan_paid\", r\"PLAN\\\\s+PAID\"), (\"patient_owes\", r\"YOU\\\\s+MAY\\\\s+OWE|PATIENT\\\\s+RESP\\\\w*\"))\n_EOBROW = re.compile(rf\"^\\\\s*({_DATE})\\\\s+(\\\\S+)\\\\s+\")\n\n\ndef _eob_header(lines):\n    \"\"\"(index, {column name: (start, end)}) of the EOB column header (BILLED and PLAN PAID on one line), or (None, None).\"\"\"\n    hi = next((i for i, ln in enumerate(lines) if re.search(r\"\\\\bBILLED\\\\b\", ln) and re.search(r\"PLAN\\\\s+PAID\", ln, re.IGNORECASE)), None)\n    if hi is None:\n        return None, None\n    return hi, {k: (m.start(), m.end()) for k, rx in _EOBCOLS for m in [re.search(rx, lines[hi], re.IGNORECASE)] if m}\n\n\ndef _eob_tokens(ln, cols, service=None):\n    \"\"\"Money-shaped tokens of an EOB line: decimals, '$' figures with no cents and whole numbers under a money column. The service code of a row and\n    the number inside a reason code (PR-1, CO-45) are not money.\"\"\"\n    out = []\n    for m in _tokens(ln, cols):\n        if service and m.start() < service[1] and service[0] < m.end():\n            continue\n        if re.fullmatch(r\"\\\\d+\", m.group(0)) and re.search(r\"[A-Za-z]-$\", ln[:m.start()]):\n            continue\n        out.append(m)\n    return out\n\n\ndef _eob(rec, lines):\n    \"\"\"(row lines, unparsed lines). Each service row (date, service code, figures) is one line of form eob: its figures are in `eob` (by column) when\n    every figure was read and there is one per column; otherwise EVERY money token of the row is in `unclear` with its text, never dropped.\"\"\"\n    hi, cols = _eob_header(lines)\n    unp = lambda ln, toks: _blank_line(rec, \"eob\", ln, unparsed=True, unclear=[t.group(0) for t in toks])\n    if hi is None:\n        return [], [unp(ln, _tokens(ln)) for ln in lines if _tokens(ln)]\n    names = [k for _, k in sorted((s0, k) for k, (s0, _e) in cols.items())]\n    out, unparsed = [], [unp(ln, _tokens(ln)) for ln in lines[:hi] if _tokens(ln)]\n    for ln in lines[hi + 1:]:\n        m = _EOBROW.match(ln)\n        if not m:\n            if _tokens(ln):                           # a printed EOB total row, or any figure outside a service row: listed, never dropped\n                unparsed.append(unp(ln, _tokens(ln)))\n            continue\n        toks = _eob_tokens(ln, cols, m.span(2))\n        figs = [parse_figure(t.group(0)) for t in toks]\n        line = _blank_line(rec, \"eob\", ln, dos=m.group(1), code=m.group(2))\n        line[\"eob\"], line[\"eob_codes\"] = {}, (ln[toks[-1].end():].strip() or None) if toks else None\n        if len(figs) == len(names) and all(f[\"cents\"] is not None for f in figs):\n            line[\"eob\"] = {k: _mag(f) for k, f in zip(names, figs)}\n        else:\n            line[\"unclear\"] = [f[\"text\"] for f in figs]\n        out.append(line)\n    return out, unparsed\n\n\n'''\ns = s[:a] + new_eob + s[b:]\n\n# --- _unit_tokens / _account: eob\nsub('''    elif form == \"ub04\":\n        found += [(m.start(), m.end(), m.group(0)) for m in (_tokens(u, cols) if below_header else _tokens(u))]''',\n    '''    elif form == \"ub04\":\n        found += [(m.start(), m.end(), m.group(0)) for m in (_tokens(u, cols) if below_header else _tokens(u))]\n    elif form == \"eob\":\n        row = _EOBROW.match(u)\n        found += [(m.start(), m.end(), m.group(0)) for m in (_eob_tokens(u, cols, row.span(2) if row else None) if below_header else _tokens(u))]''')\nsub('''            if isinstance(l.get(k), dict) and \"text\" in l[k]:\n                add(l[\"excerpt\"], l[k][\"text\"])\n''', '''            if isinstance(l.get(k), dict) and \"text\" in l[k]:\n                add(l[\"excerpt\"], l[k][\"text\"])\n        for f in (l.get(\"eob\") or {}).values():\n            add(l[\"excerpt\"], f[\"text\"])\n''')\nsub('''    hi, cols = _header(ls) if form == \"ledger_table\" else _ub_header(ls) if form == \"ub04\" else (None, None)''',\n    '''    hi, cols = _header(ls) if form == \"ledger_table\" else _ub_header(ls) if form == \"ub04\" else _eob_header(ls) if form == \"eob\" else (None, None)''')\n\n# --- remove balance step & sums\na = s.index(\"def _cents(fig):\")\nb = s.index(\"def _line_key(l):\")\ns = s[:a] + '''def _checks_for_line(line):\n    \"\"\"ROW_NOT_PARSED for a row that fit no layout, LINE_UNCLEAR when a figure could not be read. Nothing is computed from the figures.\"\"\"\n    if line.get(\"unparsed\"):\n        return [\"ROW_NOT_PARSED\"]\n    return [\"LINE_UNCLEAR\"] if line[\"unclear\"] else []\n\n\n''' + s[b:]\na = s.index(\"def _sum(lines, kind):\")\nb = s.index(\"def _billing_looking\")\ns = s[:a] + s[b:]\n\n# --- analyze\nsub(\"lines, stated_by_rec, eobs, lop, excluded, balfwds, rec_form, checks = [], {}, [], [], [], {}, {}, []\", \"lines, stated_by_rec, lop, excluded, balfwds, rec_form = [], {}, [], [], {}, {}\")\nsub('''            eobs.append(_eob(r, ls))\n            got = eobs[-1].pop(\"unparsed\")''', '''            rows_, unp_ = _eob(r, ls)\n            got = rows_ + unp_''')\nsub('''        if form in (\"ledger_table\", \"ledger_text\", \"cms1500\", \"ub04\"):\n            got = got + _account(''', '''        if form in (\"ledger_table\", \"ledger_text\", \"cms1500\", \"ub04\", \"eob\"):\n            got = got + _account(''')\na = s.index(\"    prev = {}  \")\nb = s.index(\"    for l in lines:\\n        l[\\\"detail\\\"]\")\ns = s[:a] + '''    for l in lines:\n        l[\"checks\"] = _checks_for_line(l)\n''' + s[b:]\nsub('''        l[\"detail\"] = (\"reversal\" if''', '''        l[\"detail\"] = \"eob\" if l[\"form\"] == \"eob\" and not l[\"unparsed\"] else (\"reversal\" if''')\na = s.index(\"    # EOB cross-checks against\")\nb = s.index(\"_FIG_KEYS = (\")\ns = s[:a] + '''    return {\"status\": \"listed\" if (listing or unreconciled or skipped) else \"none_found\",\n            \"lines\": listing, \"unreconciled\": unreconciled, \"skipped_records\": skipped, \"rules\": RULES}\n\n\n''' + s[b:]\n\n# --- verify: eob figures\nsub('''            if _figure_like(d.get(\"figure\")) and not _in(d[\"figure\"][\"text\"], d[\"excerpt\"]):''', '''            for k, v in (d.get(\"eob\") or {}).items():\n                if _figure_like(v) and not _in(v[\"text\"], d[\"excerpt\"]):\n                    bad.append({\"ref\": ref, \"reason\": f\"eob_{k}_not_in_excerpt\"})\n            if _figure_like(d.get(\"figure\")) and not _in(d[\"figure\"][\"text\"], d[\"excerpt\"]):''')\nsub(\"Covers lines, cites,\\n    unreconciled rows and payer-report lines and their check cites.\", \"Covers lines (EOB row figures\\n    included), cites and unreconciled rows.\")\nopen(p, \"w\").write(s)\nEOF\npython3 /private/tmp/claude-501/edit_billing.py && sed -n '/^def analyze/,/^_FIG_KEYS/p' app/backend/billing.py | tail -60"
}
````

### User / tool · 2026-11-02T06:03:52.613Z

**tool result**
````
    stated_by_prov = {}
    for r in recs:                                       # a second statement's TOTAL CHARGES / BALANCE DUE (a summary row of one kind, same form family) is listed, never overwritten
        for k, v in (stated_by_rec.get(r["n"]) or {}).items():
            stated_by_prov.setdefault((_norm(_provider(r)), _family(rec_form.get(r["n"])), k), []).append((r, v))
    for found_st in stated_by_prov.values():
        found_st = list({(v["cents"], v["text"], v["cite"]["excerpt"].strip()): (r, v) for r, v in reversed(found_st)}.values())[::-1]      # a byte-identical copy of one statement is one row
        if len(found_st) > 1:
            for r, v in found_st:
                lines.append(_blank_line(r, _family(rec_form.get(r["n"])), v["cite"]["excerpt"], unparsed=True, unclear=[v["text"]]))
    by_n = {r["n"]: r for r in recs}
    for ln in lines:
        ln["provider"] = _provider(by_n[ln["record_no"]])
    lines = _merge_duplicates(lines)
    for l in lines:
        l["checks"] = _checks_for_line(l)
    for l in lines:
        l["detail"] = "eob" if l["form"] == "eob" and not l["unparsed"] else ("reversal" if (l["billed"] and (l["billed"]["cents"] or 0) < 0) or (l["billed"] and _VOID.search(l["description"] or "")) else
                       "balance_only" if l["balance"] and not (l["billed"] or l["paid"] or l["adjustment"] or l["unclear"]) else None)
        l["class"] = "charge" if l["billed"] else "payment" if l["paid"] else "adjustment" if l["adjustment"] else "unclear"
        l["negotiated"] = bool(l["adjustment"] and _NEGOTIATED.search(l["description"] or ""))
        l["unparsed"] = bool(l.get("unparsed"))
        if l["form"] == "ledger" and l["billed"] and not l["dos"]:
            l["checks"].append("NO_DATE_OF_SERVICE")
    parsed = [l for l in lines if not l["unparsed"]]
    unreconciled = [{"provider": l["provider"], "record_no": l["record_no"], "form": l["form"], "class": "unclear", "reason_code": "ROW_NOT_PARSED",
                     "message": CHECKS["ROW_NOT_PARSED"], "excerpt": l["excerpt"], "figures": l["unclear"]} for l in lines if l["unparsed"]]

    def extra(n, cls, detail, fig, excerpt, why):
        """A cited line that is not a ledger row: a rate, an estimate, an LOP/lien amount, a printed total or a balance forward."""
        f = rec_form.get(n)
        return {"class": cls, "detail": detail, "provider": _provider(by_n[n]), "record_no": n, "record_nos": [n], "form": _family(f) if f else None,
                "figure": fig, "why": why, "excerpt": excerpt, "cites": [{"record_no": n, "excerpt": excerpt}]}
    extras = [extra(x["record_no"], "rate" if x["kind"] == "rate" else "unclear", x["kind"], x["figure"], x["excerpt"], x["why"]) for x in excluded]
    extras += [extra(x["record_no"], "unclear", x["kind"], x["figure"], x["excerpt"], "An LOP, lien or reduction amount is listed apart from the charges.") for x in lop]
    listed_apart = list(extras)
    shown, by_key = {(u["record_no"], u["excerpt"].strip(), t) for u in unreconciled for t in u["figures"]}, {}
    for r in recs:                                       # a printed total or a balance forward is a line too (a copy of one statement is one line citing both records)
        for kind, v in list((stated_by_rec.get(r["n"]) or {}).items()) + [("balance_forward", bf) for bf in balfwds.get(r["n"]) or []]:
            ex = v["cite"]["excerpt"]
            if (r["n"], ex.strip(), v["text"]) in shown or any(e["record_no"] == r["n"] and _nt(e["figure"]["text"]) == _nt(v["text"]) and (e["excerpt"] in ex or ex in e["excerpt"]) for e in listed_apart):
                continue                                 # already listed with its row (unreconciled, a rate or an LOP amount)
            key = (_norm(_provider(r)), kind, v["text"], ex.strip())
            if key in by_key:
                if r["n"] not in by_key[key]["record_nos"]:
                    by_key[key]["record_nos"].append(r["n"])
                    by_key[key]["cites"].append({"record_no": r["n"], "excerpt": ex})
                continue
            by_key[key] = extra(r["n"], "unclear", kind if kind == "balance_forward" else f"stated_total_{kind}", {k: v[k] for k in ("text", "cents", "usd")}, ex,
                                "A figure the statement prints itself. It is listed, never added to the lines.")
            extras.append(by_key[key])
    listing = sorted(parsed + extras, key=lambda l: l["record_no"])
    for i, l in enumerate(listing, 1):
        l["id"] = f"b{i}"
    for i, u in enumerate(unreconciled, 1):
        u["id"] = f"u{i}"
    return {"status": "listed" if (listing or unreconciled or skipped) else "none_found",
            "lines": listing, "unreconciled": unreconciled, "skipped_records": skipped, "rules": RULES}


_FIG_KEYS = ("billed", "adjustment", "paid", "balance", "discount", "allowed", "deductible", "copay", "coinsurance", "plan_paid", "patient_owes", "non_covered")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:03:58.605Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/backend/billing.py\"; s=open(p).read()\ns=s.replace('l[\"form\"] == \"eob\" and not l[\"unparsed\"] else','l[\"form\"] == \"eob\" and not l.get(\"unparsed\") else')\ns=s.replace(\"Returned with the line they were read from; compared with the parsed lines, never used instead.\",\"Returned with the line they were read from; listed as printed, compared with nothing.\")\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"compar\\|reconcil\\|_sum\\|_tot\\b\\|prev_balance\\|payer\" app/backend/billing.py"
}
````

### User / tool · 2026-11-02T06:03:58.710Z

**tool result**
````
9:row is a line of class unclear, detail `eob`, with its payer figures in `eob` (they restate the bill and are never added to it). A figure that cannot be read cleanly (OCR letters, odd decimals, a column that cannot be told
10:apart) is listed with cents None. A row that fits no layout is listed in `unreconciled`; a record the code could not parse is in
18:listed line, an unreconciled line, or sit on its row as an 'unclear' figure: the final accounting pass lists whatever no parser placed.
32:    "Every figure is listed with the line it was read from; nothing is totaled or compared here, and a missing figure is never hidden by a sum.",
37:    "A row that does not fit the layout is listed as unreconciled with its text; it is never dropped.",
149:    """A figure's text with the money furniture removed, so '$65.00', '65.00' and '(65.00)' compare equal."""
288:    """Totals the statement prints itself. Returned with the line they were read from; listed as printed, compared with nothing."""
482:# ------------------------------------------------------------------ EOB (payer figures; listed as lines, never added to charges or compared)
562:# unreconciled line, an excluded rate (or an LOP/lien amount, which is listed apart), or on its row as `unclear`. This pass reads the raw text with
722:    time as unreconciled would be noise. A figure on the same line that is NOT one of those keeps the line."""
816:    unreconciled = [{"provider": l["provider"], "record_no": l["record_no"], "form": l["form"], "class": "unclear", "reason_code": "ROW_NOT_PARSED",
827:    shown, by_key = {(u["record_no"], u["excerpt"].strip(), t) for u in unreconciled for t in u["figures"]}, {}
832:                continue                                 # already listed with its row (unreconciled, a rate or an LOP amount)
845:    for i, u in enumerate(unreconciled, 1):
847:    return {"status": "listed" if (listing or unreconciled or skipped) else "none_found",
848:            "lines": listing, "unreconciled": unreconciled, "skipped_records": skipped, "rules": RULES}
875:    included), cites and unreconciled rows. Returns [{ref, reason}]; `for_case` puts the list in the response as
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:04:06.125Z

**tool call — Bash**
````
{
 "command": "sed -n 700,745p tests/unit/test_billing.py; sed -n 352,380p tests/unit/test_billing.py"
}
````

### User / tool · 2026-11-02T06:04:06.208Z

**tool result**
````
    "A_table_bare_charge": ([rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "185", "315.00")))], "185", False),
}


def _texts(out):
    """Every figure text the analysis shows anywhere a paralegal can read it: unreconciled, rates and other extra lines, on-row unclear."""
    return {_nt(f) for f in figs(out)} | {_nt(l["figure"]["text"]) for l in out["lines"] if "figure" in l} | {_nt(x) for l in out["lines"] for x in l.get("unclear", [])}


@pytest.mark.parametrize("name", sorted(PROBES))
def test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped(name):
    recs = PROBES[name]
    assert unaccounted(recs, one(recs)) == [], name


@pytest.mark.parametrize("name", sorted(BARE_PROBES))
def test_bare_or_dateless_money_token_is_shown(name):
    recs, tok, in_unreconciled = BARE_PROBES[name]
    out = one(recs)
    assert _nt(tok) in _texts(out), name
    if in_unreconciled:
        assert _nt(tok) in {_nt(f) for f in figs(out)}, name
    assert unaccounted(recs, out, bare=(tok,) if tok[0] != "$" and "." not in tok else ()) == []


def test_oracle_is_not_vacuous():
    """Erase what the analysis shows and the oracle names every figure; keep it and the oracle is silent."""
    recs = PROBES["prose_unlabelled"]
    out = B.analyze(recs)
    assert unaccounted(recs, out) == []
    out["lines"], out["unreconciled"] = [], []
    assert [t for t, _u in unaccounted(recs, out)] == ["$250.00", "$250.00", "$250.00"]
    recs = BARE_PROBES["P11_bare_prose_figure"][0]
    out = B.analyze(recs)
    out["unreconciled"] = []
    assert [t for t, _u in unaccounted(recs, out, bare=("250",))] == ["250"]
    recs = BARE_PROBES["A_table_bare_charge"][0]
    out = B.analyze(recs)
    bad = next(l for l in out["lines"] if l.get("unclear"))
    bad["billed"], bad["unclear"] = {"text": "185", "cents": None, "usd": None}, []      # a parsed slot with no value is not a placement
    assert [t for t, _u in unaccounted(recs, out, bare=("185",))] == ["185"]


# ---- a figure with no cents is kept as text; a row that does not fit is listed; a printed total is a line
@pytest.mark.parametrize("fig", ["$185", "185"])
def test_table_charge_with_no_cents_is_on_its_row_as_unclear(fig):
HEAD_TXT = "DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE"


def tbl(header, rows_, footer=""):
    """A fixed-width ledger: text columns left-aligned under their header word, money columns right-aligned to the end of theirs."""
    import re as _re
    spans = {m.group(0): (m.start(), m.end()) for m in _re.finditer(r"\S+", header)}
    out = [header]
    for r_ in rows_:
        buf = [" "] * 130
        for name, text in r_.items():
            s, e = spans[name]
            start = s if name in ("DOS", "POSTED", "CODE", "DESCRIPTION") else e - len(text)
            buf[start:start + len(text)] = text
        out.append("".join(buf).rstrip())
    return "\n".join(out) + ("\n" + footer if footer else "")


def row(dos, posted, code, desc, charges=None, balance=None, **kw):
    r_ = {"DOS": dos, "POSTED": posted, "CODE": code, "DESCRIPTION": desc}
    if charges:
        r_["CHARGES"] = charges
    if balance:
        r_["BALANCE"] = balance
    r_.update(kw)
    return {k: v for k, v in r_.items() if v}


PT = "Medlark Clinic, itemized statement"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:04:35.283Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/unit/test_billing.py\"; s=open(p).read()\ndef sub(old,new,count=1):\n    global s\n    assert s.count(old)==count,(s.count(old),old[:80])\n    s=s.replace(old,new)\n\nsub('''\"\"\"Billing analysis (T-083, D-042): code-only, every figure cited, nothing totaled that is not stated.''','''\"\"\"Billing analysis (T-083, T-103, D-042, D-052): code-only, every figure cited, nothing totaled or compared.''')\nsub('''_GONE = {\"complete\",''','''_GONE = {\"payer_reports\", \"matched_provider\", \"not_added_note\", \"complete\",''')\nsub('''    assert set(out) == {\"status\", \"lines\", \"unreconciled\", \"skipped_records\", \"payer_reports\", \"rules\"}''','''    assert set(out) == {\"status\", \"lines\", \"unreconciled\", \"skipped_records\", \"rules\"}''')\nsub('''    assert set(b) == {\"status\", \"lines\", \"unreconciled\", \"skipped_records\", \"payer_reports\", \"rules\", \"citation_failures\"}''','''    assert set(b) == {\"status\", \"lines\", \"unreconciled\", \"skipped_records\", \"rules\", \"citation_failures\"}''')\n\nsub('''    assert {\"LEDGER_TOTAL_MISMATCH\", \"LEDGER_BALANCE_MISMATCH\", \"CLAIM_TOTAL_MISMATCH\", \"CLAIM_LEDGER_BILLED_MISMATCH\"}.isdisjoint(B.CHECKS)''',\n'''    assert {\"LEDGER_TOTAL_MISMATCH\", \"LEDGER_BALANCE_MISMATCH\", \"CLAIM_TOTAL_MISMATCH\", \"CLAIM_LEDGER_BILLED_MISMATCH\", \"BALANCE_STEP_MISMATCH\",\n            \"LEDGER_EOB_PAID_MISMATCH\", \"LEDGER_EOB_BILLED_MISMATCH\"}.isdisjoint(B.CHECKS)\n    assert set(B.CHECKS) == {\"LINE_UNCLEAR\", \"NO_DATE_OF_SERVICE\", \"ROW_NOT_PARSED\"}      # nothing in billing sums or compares figures''')\nsub('''    assert \"BALANCE_STEP_MISMATCH\" not in checks(out) and [l[\"excerpt\"] for l in rates(out)] != []''','''    assert checks(out) == [] and [l[\"excerpt\"] for l in rates(out)] != []''')\nsub('''def test_running_balance_step_mismatch_is_flagged_on_the_line():\n    bad = LEDGER.replace(\"410.00\\\\n\", \"415.00\\\\n\", 1)\n    out = one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", bad)])\n    assert \"BALANCE_STEP_MISMATCH\" in checks(out)''','''def test_a_running_balance_that_does_not_follow_is_listed_as_printed_with_no_verdict():\n    \"\"\"D-052 (strict): no arithmetic on a line either. A balance that is not the previous balance plus the charge is a figure, not a flag.\"\"\"\n    bad = LEDGER.replace(\"410.00\\\\n\", \"415.00\\\\n\", 1)\n    out = one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", bad)])\n    assert checks(out) == [] and \"415.00\" in {l[\"balance\"][\"text\"] for l in rows(out, \"Larkspur\") if l[\"balance\"]}''')\n\n# EOB main test\na=s.index(\"def test_eob_is_a_payer_report_and_a_ledger_eob_paid_mismatch_is_raised():\")\nb=s.index(\"def test_claim_form_and_ledger_for_one_provider\")\ns=s[:a]+'''def test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger():\n    out = one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER), rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", EOB)])\n    eob = [l for l in out[\"lines\"] if l[\"form\"] == \"eob\"]\n    assert [(l[\"code\"], l[\"class\"], l[\"detail\"], l[\"record_no\"]) for l in eob] == [(\"97110\", \"unclear\", \"eob\", 2), (\"97140\", \"unclear\", \"eob\", 2), (\"97014\", \"unclear\", \"eob\", 2)]\n    l140 = next(l for l in eob if l[\"code\"] == \"97140\")\n    assert l140[\"eob\"][\"plan_paid\"][\"cents\"] == 1600 and l140[\"eob\"][\"billed\"][\"cents\"] == 7000 and l140[\"eob_codes\"] == \"PR-1, PR-2, CO-45\"\n    assert l140[\"billed\"] is None and l140[\"paid\"] is None and l140[\"checks\"] == [] and l140[\"excerpt\"] in EOB     # an EOB row is never a charge or a payment\n    assert [cents(l) for l in rows(out, \"Larkspur\") if l[\"form\"] == \"ledger\"][:2] == [21000, 13000]\n    assert checks(out) == []            # the ledger shows no payment for 97140 and the EOB $16.00; nothing is compared, so nothing is raised\n    assert B.CHECKS.keys().isdisjoint({\"LEDGER_EOB_PAID_MISMATCH\", \"LEDGER_EOB_BILLED_MISMATCH\"})\n\n\n'''+s[b:]\n\n# verifier\nsub('''    assert broken(lambda o: o[\"payer_reports\"][0][\"lines\"][0].update(excerpt=\"made up\")) != []\n    assert broken(lambda o: o[\"payer_reports\"][0][\"checks\"][0][\"cites\"][0].update(excerpt=\"made up\")) != []''','''    assert broken(lambda o: pick(o, \"eob\").update(excerpt=\"made up\")) != []\n    assert broken(lambda o: pick(o, \"eob\")[\"eob\"][\"plan_paid\"].update(text=\"999.99\")) != []          # an EOB figure must sit inside its own row''')\n\n# oracle items\nsub('''            items.append((l[\"excerpt\"], {_nt(l[k][\"text\"]) for k in (\"billed\", \"paid\", \"adjustment\", \"balance\") if l.get(k) and l[k][\"cents\"] is not None} | {_nt(t) for t in l[\"unclear\"]}, False))''',\n'''            items.append((l[\"excerpt\"], {_nt(l[k][\"text\"]) for k in (\"billed\", \"paid\", \"adjustment\", \"balance\") if l.get(k) and l[k][\"cents\"] is not None} | {_nt(t) for t in l[\"unclear\"]}\n                          | {_nt(f[\"text\"]) for f in (l.get(\"eob\") or {}).values() if f[\"cents\"] is not None}, False))      # an EOB row claims only the figures it lists''')\nsub('''    items += [(x[\"excerpt\"], set(), True) for e in out[\"payer_reports\"] for x in e[\"lines\"]]      # a payer-report row stands for its whole row\\n''','')\n\n# balance tests\nsub('''        assert out[\"unreconciled\"] == [] and not [c for c in checks(out) if \"BALANCE\" in c and c != \"BALANCE_STEP_MISMATCH\"]''','''        assert out[\"unreconciled\"] == [] and checks(out) == []''')\nsub('''def test_balance_step_mismatch_is_flagged_on_the_line_and_an_unreadable_charge_is_class_unclear():''','''def test_a_balance_step_that_does_not_follow_raises_nothing_and_an_unreadable_charge_is_class_unclear():''')\nsub('''    assert checks(one([rec(1, PT, t)])) == [\"BALANCE_STEP_MISMATCH\"]''','''    assert checks(one([rec(1, PT, t)])) == []            # D-052: no arithmetic on a line; 999.00 is listed as printed''')\n\n# skip test\na=s.index(\"def test_eob_is_a_payer_report_not_a_skip():\")\nb=s.index(\"# ---- the money-token definition\")\ns=s[:a]+'''def test_eob_is_lines_not_a_skip():\n    out = one(PROBES[\"r5_ledger_with_eob\"])\n    assert out[\"skipped_records\"] == [] and len([l for l in out[\"lines\"] if l[\"form\"] == \"eob\"]) == 3\n    (u,) = out[\"unreconciled\"]\n    assert u[\"form\"] == \"eob\" and u[\"excerpt\"].startswith(\"TOTAL\") and u[\"figures\"][0] == \"235.00\"      # the EOB's printed total row is listed, not dropped\n\n\n'''+s[b:]\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_billing.py -x 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T06:04:36.113Z

**tool result**
````
...................F
=================================== FAILURES ===================================
_ test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger _

    def test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger():
        out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)])
        eob = [l for l in out["lines"] if l["form"] == "eob"]
        assert [(l["code"], l["class"], l["detail"], l["record_no"]) for l in eob] == [("97110", "unclear", "eob", 2), ("97140", "unclear", "eob", 2), ("97014", "unclear", "eob", 2)]
        l140 = next(l for l in eob if l["code"] == "97140")
>       assert l140["eob"]["plan_paid"]["cents"] == 1600 and l140["eob"]["billed"]["cents"] == 7000 and l140["eob_codes"] == "PR-1, PR-2, CO-45"
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'plan_paid'

tests/unit/test_billing.py:273: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_billing.py::test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 19 passed in 0.48s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:04:39.744Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport sys; sys.path.insert(0,\"tests/unit\")\nfrom app.backend import billing as B\nimport tests.unit.test_billing as T\nls=T.EOB.split(\"\\n\")\nprint(B._eob_header(ls))\nrows,unp=B._eob({\"n\":2,\"source\":\"x\"},ls)\nfor r in rows: print(r[\"eob\"],r[\"unclear\"],r[\"eob_codes\"])\nEOF"
}
````

### User / tool · 2026-11-02T06:04:40.181Z

**tool result**
````
(4, {'billed': (19, 25), 'discount': (28, 36), 'allowed': (38, 45), 'deductible': (47, 53), 'coinsurance': (55, 60), 'plan_paid': (63, 72), 'patient_owes': (74, 85)})
{} ['130.00', '52.00', '78.00', '78.00', '0.00', '0.00', '78.00', '1,'] CO-45
{} ['70.00', '28.00', '42.00', '22.00', '4.00', '16.00', '26.00', '1,'] PR-2, CO-45
{'billed': {'text': '35.00', 'cents': 3500, 'usd': '$35.00'}, 'discount': {'text': '35.00', 'cents': 3500, 'usd': '$35.00'}, 'allowed': {'text': '0.00', 'cents': 0, 'usd': '$0.00'}, 'deductible': {'text': '0.00', 'cents': 0, 'usd': '$0.00'}, 'coinsurance': {'text': '0.00', 'cents': 0, 'usd': '$0.00'}, 'plan_paid': {'text': '0.00', 'cents': 0, 'usd': '$0.00'}, 'patient_owes': {'text': '0.00', 'cents': 0, 'usd': '$0.00'}} [] CO-97
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:04:43.797Z

**tool call — Bash**
````
{
 "command": "sed -i 's/if re.fullmatch(r\"\\\\d+\", m.group(0)) and re.search(r\"\\[A-Za-z\\]-\\$\", ln\\[:m.start()\\])/if re.fullmatch(r\"[\\\\d,]+\", m.group(0)) and re.search(r\"[A-Za-z]-$\", ln[:m.start()])/' app/backend/billing.py && grep -n 'A-Za-z\\]-\\$' app/backend/billing.py; .venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T06:04:45.203Z

**tool result**
````
sed: 1: "app/backend/billing.py
": command a expects \ followed by text
>       assert broken(lambda o: pick(o, "eob")["eob"]["plan_paid"].update(text="999.99")) != []          # an EOB figure must sit inside its own row
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/unit/test_billing.py:537: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/unit/test_billing.py:533: in broken
    fn(out)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

o = {'status': 'listed', 'lines': [{'record_no': 1, 'form': 'ledger', 'dos': '05/27/26', 'dos_iso': '2026-05-27', ...}, {'...{'provider': 'Medlark Clinic', 'record_no': 3, 'form': 'ledger', 'class': 'unclear', ...}], 'skipped_records': [], ...}

>   assert broken(lambda o: pick(o, "eob")["eob"]["plan_paid"].update(text="999.99")) != []          # an EOB figure must sit inside its own row
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   KeyError: 'plan_paid'

tests/unit/test_billing.py:537: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_billing.py::test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger
FAILED tests/unit/test_billing.py::test_verifier_covers_every_cite_bearing_field
2 failed, 155 passed in 1.07s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:04:46.631Z

The sed failed (macOS); use Python.

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:04:47.996Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/backend/billing.py\"; s=open(p).read()\nold='''re.fullmatch(r\"\\\\d+\", m.group(0)) and re.search(r\"[A-Za-z]-$\", ln[:m.start()])'''\nassert old in s\ns=s.replace(old,'''re.fullmatch(r\"[\\\\d,]+\", m.group(0)) and re.search(r\"[A-Za-z]-$\", ln[:m.start()])''')\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T06:04:49.479Z

**tool result**
````
........................................................................ [ 45%]
........................................................................ [ 91%]
.............                                                            [100%]
157 passed in 1.11s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:08.872Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/unit/test_billing.py\"; s=open(p).read()\ndef sub(old,new,count=1):\n    global s\n    assert s.count(old)==count,(s.count(old),old[:80])\n    s=s.replace(old,new)\n\n# helpers + probes before PROBES comment\nsub('''# the T-083 probe sets''','''EOB_SRC = \"Quoinmere Mutual Health Plan, explanation of benefits\"\n_EOB_HEAD = EOB.split(\"\\\\n\")[:5]\n_EOB_COLS = \"DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES\"\n_EOB_TAIL = \"CO-97: payment included in allowance for another service.\"\n\n\ndef eob_text(*service_rows, total=\"TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00\"):\n    \"\"\"The sample EOB with the given service rows (a row is DOS, service, then the seven figure texts, then codes).\"\"\"\n    return \"\\\\n\".join([*_EOB_HEAD[:4], _EOB_COLS, *service_rows, *([total] if total else []), _EOB_TAIL])\n\n\ndef eob_row(billed=\"130.00\", plan_paid=\"16.00\", service=\"97110\", codes=\"PR-1, CO-45\", discount=\"52.00\", allowed=\"78.00\", deduct=\"22.00\", coins=\"4.00\", owes=\"26.00\"):\n    return f\"06/10/26  {service:<7} {billed:>7}   {discount:>7}   {allowed:>7}  {deduct:>7} {coins:>6}   {plan_paid:>8}   {owes:>9}     {codes}\"\n\n\n# the T-083 probe sets''')\nsub('''    \"r5_skipped_ambulance\":''','''    \"eob_sample\": [rec(1, EOB_SRC, EOB)],\n    \"eob_dollar_no_cents\": [rec(1, EOB_SRC, eob_text(eob_row(billed=\"$140\")))],                    # T-103 r1 B1: '$140' was lost from every field\n    \"eob_dollar_no_cents_paid\": [rec(1, EOB_SRC, eob_text(eob_row(plan_paid=\"$16\")))],\n    \"eob_ocr_letters\": [rec(1, EOB_SRC, eob_text(eob_row(billed=\"1O0.00\")))],\n    \"eob_bare_under_column\": [rec(1, EOB_SRC, eob_text(eob_row(billed=\"130\", plan_paid=\"16\")))],\n    \"eob_odd_decimals\": [rec(1, EOB_SRC, eob_text(eob_row(billed=\"130.5\", allowed=\"78.123\")))],\n    \"eob_missing_column\": [rec(1, EOB_SRC, eob_text(eob_row().replace(\"   26.00\", \"\")))],\n    \"eob_extra_figure\": [rec(1, EOB_SRC, eob_text(eob_row() + \"  104.00\"))],\n    \"eob_figure_above_header\": [rec(1, EOB_SRC, eob_text(eob_row()).replace(\"Provider:\", \"Billed to date $75.00\\\\nProvider:\"))],\n    \"eob_total_row_no_cents\": [rec(1, EOB_SRC, eob_text(eob_row(), total=\"TOTAL              $235   115.00\"))],\n    \"eob_ledger_conflict\": [rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER), rec(2, EOB_SRC, eob_text(eob_row(billed=\"$140\")))],\n    \"r5_skipped_ambulance\":''')\nsub('''    \"A_table_bare_charge\":''','''    \"eob_bare_charge\": ([rec(1, EOB_SRC, eob_text(eob_row(billed=\"130\")))], \"130\", False),\n    \"eob_bare_paid\": ([rec(1, EOB_SRC, eob_text(eob_row(plan_paid=\"16\")))], \"16\", False),\n    \"eob_bare_total_row\": ([rec(1, EOB_SRC, eob_text(eob_row(), total=\"TOTAL              235   115.00\"))], \"235\", True),\n    \"A_table_bare_charge\":''')\n\n# EOB tests after the oracle-not-vacuous test\nsub('''# ---- a figure with no cents is kept as text; a row that does not fit is listed; a printed total is a line''','''# ---- EOB rows (T-103 r2): every figure of a service row is a structured figure or sits on its row as unclear; nothing is compared with the ledger\ndef _eob_line(out, service=\"97110\"):\n    return next(l for l in out[\"lines\"] if l[\"form\"] == \"eob\" and l[\"code\"] == service)\n\n\n@pytest.mark.parametrize(\"fig\", [\"$140\", \"$130\", \"1O0.00\", \"130\", \"130.5\"])\ndef test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text(fig):\n    recs = [rec(1, EOB_SRC, eob_text(eob_row(billed=fig)))]\n    out = one(recs)\n    line = _eob_line(out)\n    assert fig in line[\"unclear\"] and line[\"eob\"] == {} and line[\"class\"] == \"unclear\" and line[\"detail\"] == \"eob\" and line[\"checks\"] == [\"LINE_UNCLEAR\"]\n    assert line[\"excerpt\"] in recs[0][\"text\"] and fig in line[\"excerpt\"]\n    assert unaccounted(recs, out, bare=(fig,) if re.fullmatch(r\"\\\\d+\", fig) else ()) == []\n\n\ndef test_eob_figure_that_disagrees_with_the_ledger_is_listed_and_nothing_is_raised():\n    \"\"\"r1 B1/B2/M1: '$140' against a ledger 130.00. No check, no ledger sum, no payer report: both rows are lines with their own excerpt.\"\"\"\n    out = one(PROBES[\"eob_ledger_conflict\"])\n    assert \"$140\" in _eob_line(out)[\"unclear\"] and checks(out) == [\"LINE_UNCLEAR\"]\n    assert next(l for l in out[\"lines\"] if l[\"code\"] == \"97110\" and l[\"form\"] == \"ledger\")[\"billed\"][\"cents\"] == 13000\n    assert not [k for d in B._walk(out) for k in d if k in (\"ledger\", \"payer_reports\", \"matched_provider\")]\n\n\ndef test_eob_row_reason_codes_and_service_code_are_not_money_tokens():\n    out = one([rec(1, EOB_SRC, EOB)])\n    assert [l[\"excerpt\"] for l in out[\"unreconciled\"]][0].startswith(\"TOTAL\") and len(out[\"unreconciled\"]) == 1\n    assert all(l[\"unclear\"] == [] for l in out[\"lines\"] if l[\"form\"] == \"eob\")\n\n\ndef test_eob_fail_safe_names_a_figure_dropped_from_a_row_and_stays_silent_when_it_is_kept():\n    \"\"\"The accounting test must be able to fail for EOB rows (r1 M3, mutant M06). Distinct figures, so each drop is visible to the set-based oracle.\"\"\"\n    row_ = eob_row(billed=\"130.00\", plan_paid=\"16.00\", discount=\"52.00\", allowed=\"78.00\", deduct=\"22.00\", coins=\"4.00\", owes=\"26.00\")\n    recs = [rec(1, EOB_SRC, eob_text(row_))]\n    assert unaccounted(recs, B.analyze(recs)) == []\n    for k in (\"billed\", \"discount\", \"allowed\", \"deductible\", \"coinsurance\", \"plan_paid\", \"patient_owes\"):\n        out = B.analyze(recs)\n        del _eob_line(out)[\"eob\"][k]\n        assert len(unaccounted(recs, out)) == 1, k\n    for fig in (\"$140\", \"1O0.00\"):\n        recs = [rec(1, EOB_SRC, eob_text(eob_row(billed=fig)))]\n        out = B.analyze(recs)\n        assert unaccounted(recs, out) == []\n        _eob_line(out)[\"unclear\"] = []                                  # mutant M06: the unclear list dropped\n        assert fig.replace(\"O\", \"O\") in {t for t, _u in unaccounted(recs, out)}, fig\n    recs = [rec(1, EOB_SRC, eob_text(eob_row(), total=\"TOTAL              $235   115.00\"))]\n    out = B.analyze(recs)\n    out[\"unreconciled\"] = []\n    assert {t for t, _u in unaccounted(recs, out)} == {\"$235\", \"115.00\"}\n\n\n# ---- a figure with no cents is kept as text; a row that does not fit is listed; a printed total is a line''')\n\n# property: eob base\nsub('''    \"ub04\": lambda: UB_ROOM,\n}''','''    \"ub04\": lambda: UB_ROOM,\n    \"eob\": lambda: EOB,\n    \"eob_rows\": lambda: eob_text(eob_row(), eob_row(service=\"97140\", billed=\"70.00\", plan_paid=\"16.00\")),\n}''')\nsub('''\"ub04\": \"Saltmarrow General Hospital, UB-04\"}''','''\"ub04\": \"Saltmarrow General Hospital, UB-04\",\n        \"eob\": EOB_SRC, \"eob_rows\": EOB_SRC}''')\nsub('''        hdr, cols = B._header(lines) if base.startswith(\"table\") else B._ub_header(lines)''','''        hdr, cols = B._header(lines) if base.startswith(\"table\") else B._eob_header(lines) if base.startswith(\"eob\") else B._ub_header(lines)''')\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T06:05:10.484Z

**tool result**
````
........................................................................ [ 40%]
........................................................................ [ 80%]
...................................                                      [100%]
179 passed in 1.25s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:15.881Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport subprocess, shutil\np=\"app/backend/billing.py\"; orig=open(p).read()\nmuts={\n \"M06_drop_unclear\":('line[\"unclear\"] = [f[\"text\"] for f in figs]','line[\"unclear\"] = []'),\n \"no_eob_account\":('\"cms1500\", \"ub04\", \"eob\"):\\n            got = got + _account','\"cms1500\", \"ub04\"):\\n            got = got + _account'),\n \"eob_numnum\":('toks = _eob_tokens(ln, cols, m.span(2))','toks = [t for t in _eob_tokens(ln, cols, m.span(2)) if \".\" in t.group(0)]'),\n \"eob_no_bare\":('(_eob_tokens(u, cols, row.span(2) if row else None) if below_header else _tokens(u))','_tokens(u)'),\n}\ntry:\n    for n,(a,b) in muts.items():\n        assert a in orig,n\n        open(p,\"w\").write(orig.replace(a,b))\n        r=subprocess.run([\".venv/bin/python\",\"-m\",\"pytest\",\"-q\",\"tests/unit/test_billing.py\"],capture_output=True,text=True)\n        print(n, r.stdout.strip().splitlines()[-1])\nfinally:\n    open(p,\"w\").write(orig)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -2"
}
````

### User / tool · 2026-11-02T06:05:22.223Z

**tool result**
````
M06_drop_unclear 7 failed, 172 passed in 1.19s
no_eob_account 2 failed, 177 passed in 0.71s
eob_numnum 5 failed, 174 passed in 1.25s
eob_no_bare 2 failed, 177 passed in 0.74s
...................................                                      [100%]
179 passed in 1.06s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:23.198Z

Mutants are all caught. Clean the silly replace, then update api.md.

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:40.184Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/unit/test_billing.py\"; s=open(p).read()\ns=s.replace('fig.replace(\"O\", \"O\") in','fig in'); open(p,\"w\").write(s)\n\np=\"memory/contracts/api.md\"; s=open(p).read()\ndef sub(old,new):\n    global s\n    assert s.count(old)==1,old[:70]\n    s=s.replace(old,new)\nsub(\"**No provider totals, no billed/paid/balance sums, no `complete` flag, no balance reconciliation (D-052):** a listing cannot hide a missing line, a sum can.\",\n    \"**No sums and no comparisons of any kind (D-052, applied strictly in T-103 r2):** no provider totals, no billed/paid/balance sums, no `complete` flag, no running-balance step check, no ledger-versus-EOB check. A listing cannot hide a missing line; a sum or a comparison can. The response has exactly `status`, `citation_failures`, `lines`, `unreconciled`, `skipped_records`, `rules`.\")\nsub(\"Code-only analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs.\",\"Code-only analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs (each EOB service row is a line).\")\nsub('''\"provider\": \"Larkspur Hollow Physical Therapy\", \"record_no\": 1, \"record_nos\": [1], \"form\": \"ledger\",    // form: ledger | cms1500 | ub04''','''\"provider\": \"Larkspur Hollow Physical Therapy\", \"record_no\": 1, \"record_nos\": [1], \"form\": \"ledger\",    // form: ledger | cms1500 | ub04 | eob''')\nsub('''\"detail\": null,                         // null | \"reversal\" (negative or VOID charge) | \"balance_only\" | see the extra-line details below''','''\"detail\": null,                         // null | \"reversal\" (negative or VOID charge) | \"balance_only\" | \"eob\" (an EOB service row) | see the extra-line details below''')\nsub('''      \"checks\": [],                           // LINE_UNCLEAR | BALANCE_STEP_MISMATCH | NO_DATE_OF_SERVICE''','''      \"checks\": [],                           // LINE_UNCLEAR | NO_DATE_OF_SERVICE (ROW_NOT_PARSED on an unreconciled row)''')\na=s.index('  \"payer_reports\": [ { \"record_no\": 2')\nb=s.index('  \"rules\": [ \"Every figure is listed')\ns=s[:a]+s[b:]\n# add EOB line example after rate example: find the end of rate example line\nsub('''\"excerpt\": \"Fee schedule: Therapeutic exercise $65.00 per unit.\", \"cites\": [ {\"record_no\": 1, \"excerpt\": \"<same>\"} ] } ],''','''\"excerpt\": \"Fee schedule: Therapeutic exercise $65.00 per unit.\", \"cites\": [ {\"record_no\": 1, \"excerpt\": \"<same>\"} ] },\n    { \"id\": \"b12\", \"class\": \"unclear\", \"detail\": \"eob\", \"provider\": \"Quoinmere Mutual Health Plan\", \"record_no\": 2, \"record_nos\": [2], \"form\": \"eob\",\n      \"dos\": \"06/10/26\", \"code\": \"97140\",                         // code = the EOB's service code; billed/paid/adjustment/balance are null on an EOB row\n      \"eob\": {\"billed\": {\"text\": \"70.00\", \"cents\": 7000, \"usd\": \"$70.00\"}, \"discount\": {...}, \"allowed\": {...}, \"deductible\": {...}, \"coinsurance\": {...}, \"plan_paid\": {...}, \"patient_owes\": {...}},\n      \"eob_codes\": \"PR-1, PR-2, CO-45\", \"unclear\": [], \"checks\": [],    // `eob` is {} and every money token of the row is in `unclear` (text, no value) when a figure could not be read or the row has the wrong number of figures\n      \"excerpt\": \"06/10/26  97140  70.00 ...\", \"cites\": [ {\"record_no\": 2, \"excerpt\": \"<same>\"} ] } ],''')\nsub(\"`unclear` is everything else: a line whose figure could not be read, and the **extra lines**\",\"`unclear` is everything else: a line whose figure could not be read, an **EOB service row** (`detail: eob`; its payer figures are in `eob`, never in `billed`/`paid`), and the **extra lines**\")\nsub(\"(a total the statement prints: UB-04 line 0001, CMS-1500 Item 28 and Item 29, TOTAL CHARGES, BALANCE DUE; listed as printed, compared with nothing), `balance_forward`.\",\"(a total the statement prints: UB-04 line 0001, CMS-1500 Item 28 and Item 29, TOTAL CHARGES, BALANCE DUE; listed as printed, compared with nothing), `balance_forward`. **Figure fields on an extra line, a running `balance`, and everything in `eob` are never summed or compared by a client.** The class is `unclear` because the code does not decide what such a figure means.\")\nsub(\"(magnitude kept; `BALANCE_STEP_MISMATCH` on the line catches a wrongly read column)\",\"(magnitude kept)\")\nsub(\"Ledger columns are assigned by position\",\"A running balance that does not follow from the line before it is listed as printed, with no flag. Ledger columns are assigned by position\")\nsub(\"EOB amounts are never lines of the ledger; a ledger-versus-EOB difference for the same date and service is raised as a check on the payer report and neither side is picked. Every cited excerpt anywhere in the response (lines, cites, unreconciled, payer lines, check cites) is checked against the record's own text, and every figure text against its excerpt,\",\"An EOB service row (date, service code, then one figure per header column: BILLED, DISCOUNT, ALLOWED, DEDUCT, COINS, PLAN PAID, YOU MAY OWE) is a line of form `eob`; it is never compared with the ledger, so a difference in billed or paid is simply two cited lines. A service code and the number in a reason code (`PR-1`, `CO-45`) are not money. Every cited excerpt anywhere in the response (lines, cites, unreconciled) is checked against the record's own text, and every figure text (including each `eob` figure) against its excerpt,\")\nsub(\"A printed total on an EOB (its TOTAL row) is an `unreconciled` row of form `eob`.\",\"An EOB money token is a `$` figure with or without cents, a decimal (OCR letters tolerated), or a whole number under one of the EOB money columns; a row whose figures do not map one-to-one to the columns (a `$140`, `1O0.00`, `130.5`, a bare `130`, a missing or extra figure) keeps every token on its row in `unclear`. A printed total on an EOB (its TOTAL row) is an `unreconciled` row of form `eob`. The test also deletes each EOB figure in turn and requires the oracle to name it.\")\nsub(\"**Check codes (closed list, fixed message each):** `BALANCE_STEP_MISMATCH`, `LINE_UNCLEAR`, `LEDGER_EOB_PAID_MISMATCH`, `LEDGER_EOB_BILLED_MISMATCH`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). Removed by D-052: `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `CLAIM_TOTAL_MISMATCH`, `CLAIM_LEDGER_BILLED_MISMATCH`, and the response fields `providers`, `totals`, `complete`, `balance_convention`, `stated_totals`, `checks`, `line_flags`, `lop_lien`, `excluded`.\",\n    \"**Check codes (closed list, fixed message each):** `LINE_UNCLEAR`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). None involves arithmetic. Removed by D-052: `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `CLAIM_TOTAL_MISMATCH`, `CLAIM_LEDGER_BILLED_MISMATCH`, `BALANCE_STEP_MISMATCH`, `LEDGER_EOB_PAID_MISMATCH`, `LEDGER_EOB_BILLED_MISMATCH`, and the response fields `payer_reports`, `providers`, `totals`, `complete`, `balance_convention`, `stated_totals`, `checks`, `line_flags`, `lop_lien`, `excluded`.\")\nsub(\"All steps are code (parse, cite, compare);\",\"All steps are code (parse, cite);\")\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"payer\\|MISMATCH\" memory/contracts/api.md | head; .venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -2; git status --short | grep -v agent-memory"
}
````

### User / tool · 2026-11-02T06:05:41.661Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:44.340Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/unreconciled rows, skipped records, EOB payer reports; no provider totals/unreconciled rows, skipped records (an EOB service row is a line); no sums or comparisons of any kind, no provider totals/' memory/contracts/api.md; grep -n \"payer_reports\\|_MISMATCH\\|payer report\" memory/contracts/api.md | cut -c1-200; .venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -2; git status --short | grep -v agent-memory"
}
````

### User / tool · 2026-11-02T06:05:45.798Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:48.528Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md; git diff -- memory/contracts/api.md | grep '^[-+]' | grep -v billing -i | grep -v \"^+++\\|^---\" | cut -c1-120 | head"
}
````

### User / tool · 2026-11-02T06:05:48.663Z

**tool result**
````
 app/backend/billing.py     | 170 ++++++++++++++++++++-------------------------
 memory/contracts/api.md    |  31 +++++----
 tests/unit/test_billing.py | 141 +++++++++++++++++++++++++++++--------
 3 files changed, 204 insertions(+), 138 deletions(-)
-      "detail": null,                         // null | "reversal" (negative or VOID charge) | "balance_only" | see the
-      "provider": "Larkspur Hollow Physical Therapy", "record_no": 1, "record_nos": [1], "form": "ledger",    // form: 
+      "detail": null,                         // null | "reversal" (negative or VOID charge) | "balance_only" | "eob" (
+      "provider": "Larkspur Hollow Physical Therapy", "record_no": 1, "record_nos": [1], "form": "ledger",    // form: 
-      "checks": [],                           // LINE_UNCLEAR | BALANCE_STEP_MISMATCH | NO_DATE_OF_SERVICE
+      "checks": [],                           // LINE_UNCLEAR | NO_DATE_OF_SERVICE (ROW_NOT_PARSED on an unreconciled r
-      "excerpt": "Fee schedule: Therapeutic exercise $65.00 per unit.", "cites": [ {"record_no": 1, "excerpt": "<same>"
+      "excerpt": "Fee schedule: Therapeutic exercise $65.00 per unit.", "cites": [ {"record_no": 1, "excerpt": "<same>"
+    { "id": "b12", "class": "unclear", "detail": "eob", "provider": "Quoinmere Mutual Health Plan", "record_no": 2, "re
+      "dos": "06/10/26", "code": "97140",                         // code = the EOB's service code; billed/paid/adjustm
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:49.766Z

Only my changes. Commit via a temp index.

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:52.166Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx_t103 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md && git diff --cached --stat && git commit -q -m \"fix(backend): billing applies D-052 strictly: no sums or comparisons; EOB rows are lines, every EOB money token placed (T-103 r2)\n\nRemoves per-service ledger sums, the EOB-vs-ledger paid/billed checks, payer_reports and the running-balance step check. EOB service rows are cited lines (class unclear, detail eob) with their figures in eob; an EOB amount with no cents or OCR letters stays on its row as unclear. The accounting pass and the fail-safe test now cover EOB records.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git rev-parse --short HEAD; unset GIT_INDEX_FILE; git show --stat --format=%h HEAD | tail -5"
}
````

### User / tool · 2026-11-02T06:05:52.251Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: export GIT_INDEX_FILE=/private/tmp/claude-501/idx_t103 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md && git diff -
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:54.243Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx_t103 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md && git diff --cached --stat"
}
````

### User / tool · 2026-11-02T06:05:54.456Z

**tool result**
````
 app/backend/billing.py     | 170 ++++++++++++++++++++-------------------------
 memory/contracts/api.md    |  31 +++++----
 tests/unit/test_billing.py | 141 +++++++++++++++++++++++++++++--------
 3 files changed, 204 insertions(+), 138 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:57.022Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx_t103 && git commit -q -m \"fix(backend): billing applies D-052 strictly: no sums or comparisons; EOB rows are lines, every EOB money token placed (T-103 r2)\n\nRemoves per-service ledger sums, the EOB-vs-ledger paid/billed checks, payer_reports and the running-balance step check. EOB service rows are cited lines (class unclear, detail eob) with their figures in eob; an EOB amount with no cents or OCR letters stays on its row as unclear. The accounting pass and the fail-safe test now cover EOB records.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git rev-parse --short HEAD && git show --stat --format=%h HEAD | tail -5"
}
````

### User / tool · 2026-11-02T06:05:57.535Z

**tool result**
````
check_secrets: ok (3 file(s) scanned staged)
bcdcb91

 app/backend/billing.py     | 170 ++++++++++++++++++++-------------------------
 memory/contracts/api.md    |  31 +++++----
 tests/unit/test_billing.py | 141 +++++++++++++++++++++++++++++--------
 3 files changed, 204 insertions(+), 138 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:04.993Z

**tool call — Bash**
````
{
 "command": "unset GIT_INDEX_FILE; git add app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md; git status --short | grep -E \"billing|api.md\"; B=\"python3 tools/board.py\"; $B show T-103 | grep -n \"AC\\|\\[ \\]\\|\\[x\\]\" | head -20"
}
````

### User / tool · 2026-11-02T06:06:05.175Z

**tool result**
````
?? .claude/agent-memory/staff-engineer-reviewer/project_t083_billing_review_patterns.md
26:- 2026-11-02T05:50:56Z backend: AC 1 checked: tests/unit/test_billing.py 157 passed: probe sets r1-r5 + 600 random insertions all appear as line/unreconciled/skipped; no totals/complete/balance fields (asserted in one()); api.md updated; commit 2dc5be2
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:06.427Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B show T-103 | head -25"
}
````

### User / tool · 2026-11-02T06:06:06.563Z

**tool result**
````
---
id: "T-103"
title: "Billing as a cited line listing (D-052): remove provider totals and complete badge; keep lines, classifications, unreconciled"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T05:42:05Z"
updated_at: "2026-11-02T06:02:05Z"
claimed_by: "backend"
claimed_at: "2026-11-02T06:02:05Z"
rounds: 1
commits: ["2dc5be2"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-103-staff-engineer.md", "at": "2026-11-02T06:02:05Z"}
ac:
  - {"n": 1, "text": "GET billing returns only cited lines (verbatim excerpt, class: charge/adjustment/payment/rate/unclear), unreconciled lines, and skipped records; no per-provider totals/complete/balance fields; api.md updated; tests: every money token from the T-083 probe set appears as a line, unreconciled or skipped", "done": true, "evidence": "tests/unit/test_billing.py 157 passed: probe sets r1-r5 + 600 random insertions all appear as line/unreconciled/skipped; no totals/complete/balance fields (asserted in one()); api.md updated; commit 2dc5be2"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T05:42:07Z backend: claimed
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:12.163Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B ac T-103 --check 1 --agent backend --evidence \"r2: tests/unit/test_billing.py 179 passed; response keys status/lines/unreconciled/skipped_records/rules only; EOB probes \\$140, \\$130, 1O0.00, bare 130 placed; 4 mutants (drop EOB unclear, no EOB accounting, decimal-only EOB tokens, no bare under column) each turn tests red; commit bcdcb91\" && $B commit T-103 --sha bcdcb91 --agent backend && $B handoff T-103 --agent backend --text \"What changed: D-052 applied strictly. Removed per-service ledger sums, LEDGER_EOB_PAID/BILLED_MISMATCH, payer_reports, _sum/_tot, and BALANCE_STEP_MISMATCH (a per-line comparison; reviewer question to Chris, I took the orchestrator's 'no comparisons of any kind'). EOB service rows are now lines (form eob, class unclear, detail eob, figures in eob{}, eob_codes); unreadable/no-cents/odd-decimal/bare/wrong-count figures keep every token in unclear. EOB records now run the D-049 accounting pass (eob header columns, service code and PR-1/CO-45 excluded). verify_citations checks eob figures. api.md updated. How verified: .venv/bin/python -m pytest -q tests/unit/test_billing.py -> 179 passed; new EOB probes in PROBES/BARE_PROBES, property test has eob bases, test deletes each EOB figure and requires the oracle to name it; 4 scratch mutants all red. What's left: nothing known; BALANCE_STEP removal is easy to restore if Chris rules it allowed. Surprise: the bare-number regex swallowed '1,' from 'PR-1,' as a money token on EOB rows.\" && $B move T-103 in_review --agent backend"
}
````

### User / tool · 2026-11-02T06:06:12.458Z

**tool result**
````
AC 1 checked: r2: tests/unit/test_billing.py 179 passed; response keys status/lines/unreconciled/skipped_records/rules only; EOB probes $140, $130, 1O0.00, bare 130 placed; 4 mutants (drop EOB unclear, no EOB accounting, decimal-only EOB tokens, no bare under column) each turn tests red; commit bcdcb91
T-103: commit bcdcb91 recorded
handoff written on T-103
T-103: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:14.418Z

T-103 round 2 is in review at commit bcdcb91, which touches only `app/backend/billing.py`, `tests/unit/test_billing.py` and `memory/contracts/api.md`. `pytest -q tests/unit/test_billing.py` gives 179 passed. Four scratch mutants of the EOB code, including the reviewer's M06, each turn tests red.

I also removed `BALANCE_STEP_MISMATCH`, since it is a per-line comparison and you said no comparisons of any kind. It is easy to restore if Chris rules it allowed.
