# T-140 — claims-adjuster-reviewer (Gary Pruitt, BI adjuster / defense adversary)

**Verdict: fail** (4 blockers, 0 majors, 1 minor). Commit 78554d1 (HEAD), run from a `git archive HEAD` copy in my scratchpad: own server on 127.0.0.1:7873, `LLM_BACKEND=fixture`, `ZLAYT_MODE=local`, `ZLAYT_DB` in the scratchpad. The server was stopped by PID 88162 and the port check came back empty.

lib11 is fixed. If you accept everything, the letter reads "Billed charges stated in these records: $6,000.00". The internal notes give the reason each of $2,740 / $300 / $274 / $2,166 was left out. I checked that by hand: $3,260 + $250 + $180 + $2,310 = $6,000.

The fix depends on a closed list of label words, though, and a ledger that uses other ordinary wording still inflates the letter total:
- My SYNTHETIC two-statement ledger (`artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt`) puts **$2,600.00** in the letter. The records state $1,950.00 of distinct services. The overstatement comes from a "Year-to-date charges $1,100.00" running total that was counted as a charge, plus the 04/16 visit counted on both statements. Two real $150 lines also drop out because they merge with each other.
- Label sweep: of 28 running/statement-total labels, 15 are classed as a charge when the figure does not happen to equal the sum of the record's other lines. 9 of 15 prior-balance/carry-forward wordings are classed as a charge, and so are 4 of 22 credit/payment wordings.
- Across the library, lib10 (EOB) still prints **$16,147.00**. The records state $8,123.50.

For me, an inflated "billed charges" figure is the first thing I'd put in a response letter: if one number is wrong, I discount the whole package.

Deterministic checks first: `pytest tests/unit/test_amounts_t140.py tests/unit/test_amounts.py tests/unit/test_billing.py tests/unit/test_export.py -q` on the HEAD tree gave `457 passed in 5.89s`. `python -m evals.library_report` on the HEAD tree reported the accept-all column `WRONG $16,147.00 vs $8,123.50` for lib10 and WRONG for lib04/05/06/09. The other 10 cases were ok.

Library accept-all results, checked by hand against the records:

| case | letter | records | note |
|---|---|---|---|
| lib01 | $3,915 | $3,915 | ok |
| lib02 | $2,260 | $2,260 | ok |
| lib03 | $7,500 | $7,500 | ok |
| lib04 | $4,730 | $8,630 | under; surgeon fee left unclear |
| lib05 | $38,420 | $44,570 | under |
| lib06 | $6,380 | $6,830 | under; balance $1,550, adjustment $1,250 and amount due $1,150 correctly unclear |
| lib07 | $2,620 | $2,620 | ok |
| lib08 | $11,240 | $11,240 | ok |
| lib09 | $5,090 | $6,390 | under |
| lib10 | **$16,147.00** | $8,123.50 | **over: EOB "Amount billed $8,023.50" counted on top of the UB-04 lines** |
| lib11 | $6,000 | $6,000 | ok |
| lib12 | $5,790 | $5,790 | ok |
| lib13 | $5,830 | $5,830 | ok |
| lib14 | $4,527.05 | $4,527.05 | ok |
| lib15 | $3,295 | $3,295 | ok; the duplicate statement and the 18.001 affidavit restatement are not counted |

Where the synthetic paste ran: the paste through my HTTP server returned `409 demo_mode_unsupported_input` (fixture demo mode). I then ran the same paste through the real app in-process (TestClient on the HEAD tree). The only change was adding the paste's digest to `app.state.recorded`, the allow-list the server uses for library cases. With every item accepted, export returned `422 judge_not_run` because the fixture has no recorded judge answers. The letter line therefore comes from the real `export.build_export` via `evals.library_report.accept_all_total_cents`, which returned 260000. Amount classes are code-only, and the handoff says the judge cannot change them.

```json
{"card": "T-140", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 78554d1 (HEAD) via git archive into the session scratchpad; app on http://127.0.0.1:7873 (LLM_BACKEND=fixture, ZLAYT_MODE=local, ZLAYT_DB in scratchpad); all 15 evals/library cases accept-all + export; SYNTHETIC ledger artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt; app/backend/amounts.py diff",
 "exercised": [
  "python3 tools/board.py show T-140; git show HEAD -- app/backend/amounts.py",
  "git archive HEAD | tar -x into scratchpad/tree; server pid 88162 on :7873, /api/health backend=fixture demo_mode=true; stopped with kill 88162, lsof -t -iTCP:7873 empty",
  "pytest tests/unit/test_amounts_t140.py test_amounts.py test_billing.py test_export.py on HEAD tree: 457 passed in 5.89s",
  "python -m evals.library_report on HEAD tree: accept-all WRONG for lib04, lib05, lib06, lib09, lib10 ($16,147.00 vs $8,123.50); ok for the other 10",
  "artifacts/review-evidence/T-140-adjuster/probe_library.py: for each of the 15 library cases, POST /api/cases {library}, run, accept every entry/amount/flag, GET export, read the 'Billed charges stated in these records' line and amount classes (library_accept_all.txt); lib11 = $6,000.00 and the AMOUNTS NOT TOTALED notes give the reasons for $2,740/$300/$274/$2,166",
  "hand-recomputed every library total against the $ lines of evals/library/*.txt",
  "pasted SYNTHETIC ledger (running totals, Statement total, prior balance carried forward, 04/16 line on two statements, negative payments, columned ledger): HTTP paste refused 409 in demo mode; in-process TestClient with the digest allow-listed gave the amount classes, and export.build_export gave $2,600.00 (synthetic_paste_out.txt)",
  "artifacts/review-evidence/T-140-adjuster/probe_variants.py and probe_variants2.py: 93 ledger phrasings through amounts.extract_amounts + totals.totals with a billing-statement and a ledger source (variants_out.txt, variants2_out.txt)"
 ],
 "verdict": "fail",
 "scores": {"lib11_fix": 5, "letter_total_not_inflated_beyond_lib11": 1, "not_totaled_reasons_in_internal_notes": 4, "robustness_to_ledger_wording": 1},
 "findings": [
  {"severity": "blocker",
   "title": "Running-total, statement-total and carried-forward lines without the exact words total/balance/paid/adjustment are still classed 'charge' and added to the letter total",
   "evidence": "variants2_out.txt: with a figure that is not the sum of the record's lines, 15 of 28 labels are charge: 'Cumulative charges', 'Year-to-date charges', 'Accumulated charges', 'Sum of charges', 'All charges', 'Combined charges', 'Aggregate charges billed', 'Total, this statement:', 'This statement:', 'Statement amount', 'Amount of this statement', 'Current statement charges', 'New charges this statement', 'Statement charges', 'Billed this statement' -> 'charge   accept-all total $1,040.00' where the stated lines are $310.00. variants_out.txt: 'LEAK 'Previous statement $380.00' ... charge total $730.00' (lines $350.00), plus 'Carried forward charges', 'Prior charges', 'Previous charges', 'Carry-over from 05/01/2026 statement', 'Charges carried from prior statement', 'Prior statement charges', 'Previously billed', 'Unpaid prior charges'. End to end: synthetic_paste_out.txt 'a21 charge ... $1,100.00' ('Year-to-date charges $1,100.00') and 'library_report.accept_all_total_cents: 260000' = letter 'Billed charges stated in these records: $2,600.00' vs $1,950.00 of distinct services stated. Causes: the _NC_KINDS word list (amounts.py:103-108) has no running/cumulative/year-to-date/previous/prior/carried/forward/all/combined/statement words; _STATEMENT (amounts.py:20, used at :164) still turns any 'statement' or 'billed' label on a billing source into a charge; the comma split in _label leaves 'this statement:' as the label of 'Total, this statement: $X'; the cross-check (amounts.py:176) only catches a figure exactly equal to the sum of the same record's other charges, and a cumulative figure on statement 2 never is.",
   "why_it_matters": "This is the same defect class as the GATE-M2 blocker the card exists to close: a ledger summary line counted as a charge. On my desk a demand that states $2,600 in billed charges when the itemized lines add to $1,950 is overstated, and I would use it to discount the whole specials package. lib11 passes only because its total line happens to use the word 'total'.",
   "fix": "Invert the rule on billing documents: an amount is a charge only when its own line names a service, procedure, CPT/HCPCS/revenue code or date of service with a charge word. Statement-, period- and account-level figures (statement, previous/prior, carried/brought forward, cumulative, year-to-date, to date, all, combined, aggregate, sum) are 'unclear' with a reason. Drop 'statement' and 'billed' from the _STATEMENT charge rule, or limit it to a line with a service noun. Do the label check before the clause split, or across the comma.",
   "acceptance_test": "Parametrized unit test over these 28 + 15 phrasings (figure not equal to the sum of the other lines, billing-statement and ledger sources): none is class charge. HTTP test: the SYNTHETIC two-statement ledger in artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt (or a qa copy) accepted in full exports a total with no running, year-to-date or carried-forward figure in it."},
  {"severity": "blocker",
   "title": "Credits, reversals, voids, recoupments and med-pay applications written without a minus sign are added as positive charges",
   "evidence": "variants_out.txt: 'LEAK 'Reversal of exercise charge $100.00 CR' billing-statement: charge total $450.00', 'LEAK 'Med pay applied to visit charge $100.00' ... charge total $450.00', 'LEAK 'Void of 05/07 charge $100.00' ... charge total $450.00', 'LEAK 'Recoupment of billed $100.00' ... charge total $450.00' (stated charge lines: $350.00). The same wordings with '-$' stay unclear only because the '-' sits between the label and '$' and breaks _CHARGE_END's end anchor (amounts.py:21), not because of a credit rule. find_amounts drops the sign, so a credit counted as a charge is added, never netted. The payment pattern (amounts.py:106) has no 'pay'/'med pay'/'applied'; there is no reversal/void/refund/recoupment/CR word.",
   "why_it_matters": "A payment or credit counted as a billed charge inflates the specials and, worse, reads as money the plaintiff was charged twice. Texas paid-or-incurred discovery turns up exactly these ledger lines, and an adjuster who finds a credit summed as a charge has a ready attack on every number in the letter.",
   "fix": "Add reversal, void, refund, recoup(ment), 'CR' suffix, '(credit)', 'applied', 'med pay'/'PIP' to the non-charge kinds. A figure with a leading '-' or in parentheses '($X)' on a billing document is never a charge, whatever its label.",
   "acceptance_test": "Unit test: the 4 leaking wordings above plus '($100.00)' and '$100.00 CR' are unclear with a payment or adjustment reason; the accept-all total of the test statement stays $350.00."},
  {"severity": "blocker",
   "title": "lib10: EOB 'Amount billed $8,023.50' is counted on top of the UB-04 lines; the letter claims $16,147.00 against $8,123.50 in the records",
   "evidence": "library_accept_all.txt '## case_lib10_eob_ub04_cms1500 ... ['Billed charges stated in these records: $16,147.00']' with 'a7 charge verified accepted $8,023.50'; evals/library/case_lib10_eob_ub04_cms1500.txt line 31: 'Explanation of benefits ... This is not a bill. Amount billed $8,023.50'; expected.json explicit_charges_total 8123.5, A7 'EOB restates the provider charge ... not a second charge'. library_report on HEAD: 'case_lib10_eob_ub04_cms1500 | WRONG $16,147.00 vs $8,123.50'. Handoff: 'lib10: EOB Amount billed $8,023.50 still charge, M1 ... not touched'. No open card covers it: python3 tools/board.py list --status backlog/ready/in_progress shows none.",
   "why_it_matters": "The letter nearly doubles the billed specials. An EOB's 'amount billed' is the claim-level total of the provider's bill restated by the payer, the same 'restated total' the card's AC1 bars, on another document. I would cite the $8,023.50 EOB line and the $8,123.50 UB-04 total line to show the demand counted one hospital bill twice.",
   "fix": "On an EOB, remittance or other payer document (lexicon billing_document already matches 'explanation of benefits|EOB'), 'amount billed', 'billed charges', 'total billed' and 'provider charges' are restatements: class unclear with the reason 'Payer restates the provider's bill; not a second charge.' If a separate card owns it, open it as P0 before GATE-M2 reruns.",
   "acceptance_test": "Library accept-all for lib10 exports 'Billed charges stated in these records: $8,123.50'; library_report shows lib10 ok."},
  {"severity": "blocker",
   "title": "Duplicate service lines on two statements are counted twice; two distinct same-price lines in one statement collapse into one",
   "evidence": "variants_out.txt '## duplicate line on two statements': record 2 '04/16/2026 manual therapy charge $150.00' and record 3 '04/16/2026 manual therapy charge $150.00' -> 'a1 [2] $150.00 charge None' and 'a3 [3] $150.00 charge None', 'accept-all charge total 550.0 (distinct services stated: 150 + 120 + 130 = 400.00)'. '## two distinct same-price services inside ONE statement': 04/09 and 04/16 manual therapy $150.00 -> 'a1 [1] $150.00 charge Same amount, date and provider appears in records 1.', 'accept-all charge total 240.0 (stated: 150 + 150 + 90 = 390.00)'. Cause: dedupe key amounts.py:224 is (record date, provider, record text, class, cents). It has no service date, so the same visit on two statements never merges, and two visits in one record always do. Pre-existing; not in the 78554d1 diff.",
   "why_it_matters": "Re-listing open charges on the next statement is the normal format for a provider statement. Counting them again is the double-count I check for first, and the merge loses a stated charge. Both make the total wrong, and either one lets me say the demand's arithmetic doesn't match its bills.",
   "fix": "Dedupe charge lines by (provider, service date stated in the line, description, cents) across records. Never merge two lines of the same record that have different service dates or positions. When it does merge, the duplicate note names both records and the service date.",
   "acceptance_test": "Unit test with the two probe fixtures: cross-statement total 400.00 with one item citing records 2 and 3; same-statement total 390.00 with two $150 items."},
  {"severity": "minor",
   "title": "Accept-all under-counts on lib04, lib05, lib06, lib09 (fees left unclear); outside my adversary lens",
   "evidence": "library_report on HEAD: 'lib04 ... WRONG $4,730.00 vs $8,630.00', 'lib05 ... WRONG $38,420.00 vs $44,570.00', 'lib06 ... WRONG $6,380.00 vs $6,830.00', 'lib09 ... WRONG $5,090.00 vs $6,390.00' (e.g. lib04 'Surgeon fee: $3,900' class unclear).",
   "why_it_matters": "An understated total does not help me, but the letter's 'stated in these records' figure is still not what the records state. The handoff lists these cases as known. Context only.",
   "fix": "Track on its own card (fee/charge vocabulary), or record it in SCOPE_CUTS.",
   "acceptance_test": "library_report accept-all ok for these four, or a SCOPE_CUTS row naming them."}
 ],
 "whats_right": [
  "lib11 accept-all letter is $6,000.00 and the internal notes give each of $2,740/$300/$274/$2,166 a plain reason; no ledger figure reaches the letter",
  "The code rule beats the judge: lib11 $2,740/$300/$2,166 stay unclear with JUDGE_DISAGREES, and explicit Total/Statement total/Balance due/Payment/Adjustment/-$ lines are never charges",
  "lib15's duplicate statement and 18.001 affidavit restatement are not counted again ($3,295.00 correct)"
 ],
 "questions_for_chris": []}
```
