# T-140 r2 — claims-adjuster-reviewer (Gary Pruitt, BI adjuster / defense adversary)

**Verdict: fail** (4 blockers, 0 majors, 1 minor). Commit a0e2639 (HEAD) via `git archive a0e2639` into my session scratchpad; own server on 127.0.0.1:7874 (`LLM_BACKEND=fixture`, `ZLAYT_MODE=local`, `ZLAYT_DB` in the scratchpad, PID 87476, stopped with `kill 87476`; `lsof -t -iTCP:7874` came back empty).

What r2 fixed, and I checked it: lib10 now prints $8,123.50 (was $16,147.00). Charges cannot go through a batch (`422 CHARGES_NOT_BATCHED`). A flagged charge is refused without its named confirm (`422 CONFIRM_REQUIRED`) and with a wrong word (422), and it is accepted only with `likely_duplicate`. My r1 SYNTHETIC ledger, accepted one at a time with the flagged duplicate left pending, now exports **$1,950.00**, which is the right figure. 92 of the 93 r1 label variants are no longer charges.

It still fails my question. My new SYNTHETIC ledger (`artifacts/review-evidence/T-140-adjuster-r2/attack_ledger.txt`) states $1,950.00 of distinct services: ED $1,000, PT eval $200, and five $150 PT visits (04/09, 04/16, 05/07, 06/10, 06/24). I accepted every charge one at a time and confirmed nothing flagged. The letter reads **"Billed charges stated in these records: $4,350.00"**. None of the $2,400 overstatement carried a flag:
- "Last statement $500.00." (+$500)
- "Charges $650.00 year to date." (+$650)
- the ledger row "06/30/2026  Account summary  $950.00 ..." (+$950)
- the 04/16 visit restated as "Apr 16, 2026 manual therapy charge $150.00." (+$150)
- the insurer's "Acme Mutual Insurance, payment history" row "04/09/2026  Ther exercise 97110  $150.00" (+$150)

With the one flagged line confirmed by name, the letter says $4,500.00.

The letter also cites the wrong sentence for same-price charges. Two different $150 visits in one statement both print the 04/09 sentence as their source, so on my desk the letter reads as a double count.

Deterministic checks first, on the a0e2639 tree:
- `pytest tests/unit/test_amounts_d059.py tests/unit/test_amounts_d059_api.py tests/unit/test_amounts_t140.py tests/unit/test_amounts.py tests/unit/test_billing.py tests/unit/test_export.py tests/unit/test_case_extras.py -q`: the first run gave `ERROR tests/unit/test_amounts_d059_api.py - FileNotFoundError: ... artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt` because that file is untracked (`git ls-files artifacts/review-evidence/T-140-adjuster/` is empty). After I copied it into the tree: `583 passed in 36.92s`.
- `LLM_BACKEND=fixture python -m evals.library_report`: the accept-all column reads `ok` for all 15 cases.

Library, each case run on my server. Entries, flags and every amount were accepted one at a time. No library case raised a flagged charge, so path A (no confirm) and path B (named confirm) give the same total:

| case | letter | records state | note |
|---|---|---|---|
| lib01 | $3,915.00 | $3,915 | ok |
| lib02 | $2,260.00 | $2,260 | ok |
| lib03 | $7,500.00 | $7,500 | ok |
| lib04 | $4,730.00 | $8,630 | under (surgeon fee unclear; known, in expected.json accept_all_reason) |
| lib05 | $38,420.00 | $44,570 | under (known) |
| lib06 | $6,380.00 | $6,830 | under (known) |
| lib07 | $2,620.00 | $2,620 | ok |
| lib08 | $11,240.00 | $11,240 | ok |
| lib09 | $5,090.00 | $6,390 | under (known) |
| lib10 | $8,123.50 | $8,123.50 | ok (fixed) |
| lib11 | $6,000.00 | $6,000 | ok |
| lib12 | $5,790.00 | $5,790 | ok |
| lib13 | $5,830.00 | $5,830 | ok |
| lib14 | $4,527.05 | $4,527.05 | ok |
| lib15 | $3,295.00 | $3,295 | ok |

No library letter goes over what its records state. The undercounts are the tracked fee-vocabulary issue, so they are noted here and not filed.

```json
{"card": "T-140", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commit a0e2639 (HEAD) via git archive into the session scratchpad; app on http://127.0.0.1:7874 (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, ZLAYT_DB in scratchpad); all 15 evals/library cases; SYNTHETIC ledgers artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt (r1) and artifacts/review-evidence/T-140-adjuster-r2/attack_ledger.txt (new); app/backend/amounts.py, review.py, present.py, export.py:_amount_quote",
 "exercised": [
  "python3 tools/board.py show T-140; read reviews/T-140-claims-adjuster.md, D-059 in memory/ORCHESTRATOR_DECISIONS.md, personas/claims-adjuster.md; git show --stat a0e2639; git show a0e2639 -- app/backend/review.py app/backend/present.py",
  "git archive a0e2639 into scratchpad/tree; pytest of 7 amount/export/billing/case_extras test files: first run 'ERROR tests/unit/test_amounts_d059_api.py - FileNotFoundError ... synthetic_ledger.txt' (file untracked: git ls-files artifacts/review-evidence/T-140-adjuster/ prints nothing); after copying it into the tree '583 passed in 36.92s'",
  "LLM_BACKEND=fixture python -m evals.library_report on the a0e2639 tree: accept-all total 'ok' for all 15 packets",
  "server: env HOST=127.0.0.1 PORT=7874 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=scratchpad/app.sqlite3 python -m app.main from the tree; /api/health backend=fixture demo_mode=true; PID 87476 stopped with kill, lsof -t -iTCP:7874 empty",
  "artifacts/review-evidence/T-140-adjuster-r2/probe_library_r2.py on all 15 library cases over HTTP: batch accept with a charge -> 422 CHARGES_NOT_BATCHED; entries/flags/amounts accepted one at a time; path A export and path B (wrong confirm then named confirm) export; output library_r2.txt; totals hand-checked against r1 table and lib10 records",
  "artifacts/review-evidence/T-140-adjuster-r2/probe_paste_r2.py (in-process TestClient on the tree, the worker's own D-059 API-test harness: claude-cli + ENABLE_LIVE + scripted call factory, no model runs) on the r1 ledger: batch 422 CHARGES_NOT_BATCHED, a13 422 CONFIRM_REQUIRED, wrong word 422, named 200; path A 'Billed charges stated in these records: $1,950.00', path B $2,100.00 (paste_r1_ledger_out.txt)",
  "same probe on the new attack_ledger.txt: path A $4,350.00, path B $4,500.00 vs $1,950.00 stated distinct services (paste_attack_out.txt)",
  "re-ran r1 probe_variants.py and probe_variants2.py on the tree: 1 leak each ('Statement charges')",
  "artifacts/review-evidence/T-140-adjuster-r2/probe_variants_r2.py: 44 restating labels through amounts.extract_amounts with a billing-statement source, figure not equal to the record's other charges: 26 class charge with no flag (variants_r2.txt)",
  "artifacts/review-evidence/T-140-adjuster-r2/probe_dup_nolabel_r2.py: same 04/16 line on a second statement in 11 forms (3 flagged, 8 missed) and 5 no-label figures (2 unclear, 3 table rows class charge with no flag) (dup_nolabel_r2.txt)",
  "GET /export of every library token: no repeated charge-quote line in any library letter (the mis-cite needs two same-price lines in one record)"
 ],
 "verdict": "fail",
 "scores": {"lib10_and_library_fix": 5, "batch_and_named_confirm_gate": 5, "letter_total_not_inflated_beyond_records": 1, "letter_charge_cites_match_the_charge": 1, "robustness_to_ledger_wording": 2},
 "findings": [
  {"severity": "blocker",
   "title": "Statement-level, year-to-date-after-figure, earlier-statement and summary-row figures are still class 'charge' with no flag and reach the letter total",
   "evidence": "paste_attack_out.txt path A (no confirms): 'LETTER: Source [Ex. __ / Bates __]: \"Last statement $500.00.\"', 'LETTER: Source [Ex. __ / Bates __]: \"Charges $650.00 year to date.\"', 'LETTER: Source [Ex. __ / Bates __]: \"06/30/2026  Account summary  $950.00  $90.00  $860.00\"' and 'LETTER: Billed charges stated in these records: $4,350.00' against $1,950.00 of distinct services in attack_ledger.txt. variants_r2.txt: 26 of 44 labels LEAK, including 'Statement charges', 'Statement amt', 'Statement:', 'Statement dated 06/01/2026:', 'Last statement', 'Charges from 05/01/2026 statement', 'Charges $730.00 year to date.', 'Charges $730.00 to date.', 'Charges $730.00 (all statements).', 'Amount billed since 04/02/2026:', 'Billed to insurance', 'Gross charges', 'Monthly charges', 'Earlier charges', 'Open charges'. dup_nolabel_r2.txt: ledger rows with description '—', '*' or 'Summary' in the Charges column: 'LEAK ... charge flag=None'. r1 probes: 'LEAK 'Statement charges $350.00' ... charge' (named in my r1 acceptance test). Causes: _STATEMENT (amounts.py:20, used at :268) still makes any label containing 'statement' or 'billed' a charge on a billing source; the 'previous' kind (amounts.py:107) needs the words previous/prior, so 'Last statement' and 'Charges from 05/01/2026 statement' pass; _AFTER_KINDS (amounts.py:133) has no year-to-date/to-date/running words, so 'Charges $650.00 year to date' is labelled by 'Charges' alone; a Charges-column row (amounts.py:130) is a charge whatever its description says.",
   "why_it_matters": "D-059 (2) lists year-to-date and previous statement as never-charge labels, and my r1 acceptance test said 'Statement charges' must not be a charge. On my desk, a demand stating $4,350 in billed charges where the itemized lines add to $1,950 is overstated by more than double, and I discount the whole specials package. The paralegal accepting one at a time sees the excerpt, but the tool offers these as unflagged charges with accept_effect letter_total. The confirm gate never fires because the cross-check only catches a figure equal to the same record's other charges.",
   "fix": "On a billing document, class a figure 'charge' only when its own line or row names a service (a service noun, CPT/HCPCS/revenue code) or a date of service. A figure whose label is a statement/period/account word (statement, last/earlier/open/gross/overall/monthly/account charges, billed since/to, summary), or that is followed by year to date / to date / since / all statements, is 'unclear' with a reason. Add year-to-date, to date, since <date>, in all and (all statements) to the after-figure kinds. Add 'last statement' and '<date> statement' to the previous kind. A ledger row whose description has no service word ('Account summary', a dash, '*', 'Summary') is not a charge even in the Charges column.",
   "acceptance_test": "Parametrized unit test over the 26 LEAK labels in variants_r2.txt and the 3 no-label rows in dup_nolabel_r2.txt (figure not equal to the record's other charges): none is class charge without a flag. HTTP test: attack_ledger.txt, every amount accepted one at a time without confirm, exports 'Billed charges stated in these records: $1,950.00'."},
  {"severity": "blocker",
   "title": "Likely-duplicate flag misses the same service line when the date is written another way or the description adds a code, so the visit is counted twice with no flag",
   "evidence": "paste_attack_out.txt: record 2 '04/16/2026 manual therapy charge $150.00.' and record 3 'Apr 16, 2026 manual therapy charge $150.00.' are both class charge with flag None and both in the letter ('LETTER: Source [Ex. __ / Bates __]: \"Apr 16, 2026 manual therapy charge $150.00.\"'). dup_nolabel_r2.txt: flagged only for '04/16/2026', '2026-04-16' and '4/16/26'. MISS for 'Apr 16, 2026', 'April 16, 2026', '16-Apr-2026', '04/16' (no year, statement dated 06/01/2026), 'Manual therapy charge $150.00 (DOS 04/16/2026).', '04/16/2026 manual therapy 97140 charge', '04/16/2026 manual ther charge', '04/16/2026 Manual Therapy (97140) charge'. Cause: _SVC_DATE (amounts.py:354) reads only m/d/y and ISO numerals; service_key (amounts.py:358) reads only the text before the figure and keys on the exact remaining words.",
   "why_it_matters": "D-059 (3) says a charge with the same date, description and amount on two statements is flagged. 'Apr 16, 2026' and '04/16/2026' are the same date. Provider statements re-list open charges, and many print month names or put the date of service after the amount. Each miss is an unflagged double count in the letter, and finding double counts is the first thing I do with a ledger.",
   "fix": "Parse the service date with the app's own date parser (month names, d-Mon-yyyy, m/d without a year resolved from the statement date) on the whole line or row, including text after the figure (DOS ...). Normalize the description (drop CPT/HCPCS codes and parentheses, compare word stems or a prefix match such as 'manual ther' and 'manual therapy') before the key, or key on (provider, service date, cents) and flag when the descriptions share a service word.",
   "acceptance_test": "Unit test: each of the 8 MISS forms in dup_nolabel_r2.txt on a second statement gets confirm.flag == 'likely_duplicate'. HTTP: the 04/16 line in attack_ledger.txt record 3 returns 422 CONFIRM_REQUIRED without confirm."},
  {"severity": "blocker",
   "title": "An insurer payment history not labelled EOB/remittance is not seen as an insurer document; its Billed column restates a provider charge as a new charge",
   "evidence": "paste_attack_out.txt: record 6 'Source: Acme Mutual Insurance, payment history' row '04/09/2026  Ther exercise 97110  $150.00  $90.00  $72.00' is a29 'charge accepted 15000 [r6] None' and in the letter ('LETTER: Acme Mutual Insurance, payment history, July 20, 2026: $150.00'), restating record 2's '04/09/2026 therapeutic exercise charge $150.00.'. Record 5 'Acme Mutual, explanation of benefits' with a 'Charges submitted' column is correctly unclear (a23..a28). Cause: _INSURER_SRC (amounts.py:141) matches EOB/explanation of benefits/remittance/ERA/payer/insurer/health plan only. 'Insurance', 'carrier', 'claim summary' and 'payment history' from an insurer are not insurer words, while 'payment history' makes the source a billing document (lexicon billing_document), so the Billed column (amounts.py:130) makes it a charge.",
   "why_it_matters": "D-059 (2) says an amount from an insurer document restating a provider charge is unclear. The EOB test passes only because the source says 'explanation of benefits'. A carrier's claim history labelled any other way adds the provider's bill a second time. A demand that counts my own company's payment history as a second bill is an easy discount for me.",
   "fix": "Widen insurer detection to the source and the excerpt: insurance/insurer/carrier/mutual/casualty/indemnity company names with claim/payment history/claim summary/allowed/paid-by-plan columns. A table that has both a Billed/Charges column and an Allowed or Paid column is an insurer restatement, so its figures are unclear with the insurer reason.",
   "acceptance_test": "Unit test: 'Acme Mutual Insurance, payment history' and 'Acme Mutual, claim summary' sources with Billed/Allowed/Paid columns give no class charge. HTTP: attack_ledger.txt record 6 adds nothing to the letter total."},
  {"severity": "blocker",
   "title": "Letter (and internal notes) cite the wrong sentence for a charge when its record states the same figure twice; two different visits print the same source line",
   "evidence": "paste_r1_ledger_out.txt path A, total correct at $1,950.00, but: 'Brindlewood Physical Therapy, patient statement, May 1, 2026: $150.00 / Source [Ex. __ / Bates __]: \"04/09/2026 therapeutic exercise charge $150.00\"' printed twice (the second is the 04/16 manual therapy charge). 'June 1, 2026: $150.00 / Source: \"04/16/2026 manual therapy charge $150.00.\"' is printed for the 05/07 exercise charge (a14) while the 04/16 duplicate a13 was pending. 'account ledger, July 1, 2026: $150.00 / Source: \"06/10/2026  Manual therapy  $150.00  $0.00  $730.00\"' is printed twice (the second is the 06/24 visit). paste_attack_out.txt shows the same pattern for 04/09, 'Apr 16', 06/10 and 'Ther exercise 97110'. Internal notes: 'Record 3 ... \"04/16/2026 manual therapy charge $150.00.\" Not totaled ($150.00): Reversal, refund, void...', when the reversal is 'Reversal of 05/07/2026 exercise charge -$150.00.' Cause: export.py:220-223 _amount_quote takes exc.find(raw), the first occurrence of the figure in the record, not the amount's own offset. The code dates from c9f272a/5f7ef96, but a0e2639's 'two figures of the SAME record never merge' (amounts.py dedupe_amounts) is what puts two same-price lines of one record into the letter. No library letter repeats a charge quote.",
   "why_it_matters": "Checklist 14: every line must carry a cite I can check. Here the cites are verbatim but belong to another service. Read cold, the letter documents the 04/09 and 06/10 visits twice and gives no source for 04/16, 05/07 and 06/24, so I would write back that the specials double-count. The internal notes tell the firm a real visit is a reversal.",
   "fix": "Quote from the amount's own offset (item excerpt_start/start minus the record's char_start), never from find(raw). Apply the same fix to not_totaled_reason, which matches on raw and cents.",
   "acceptance_test": "Export test: a statement with two different $150 lines, both accepted, prints two different Source lines, each holding its own service and date. Notes test: the reversal note quotes the reversal sentence."},
  {"severity": "minor",
   "title": "The D-059 API test reads an untracked reviewer evidence file, so it errors on a clean checkout of a0e2639 (engineering lane; noted for staff-engineer)",
   "evidence": "tests/unit/test_amounts_d059_api.py:11 LEDGER = (ROOT / 'artifacts' / 'review-evidence' / 'T-140-adjuster' / 'synthetic_ledger.txt').read_text(); on the git-archive tree: 'ERROR tests/unit/test_amounts_d059_api.py - FileNotFoundError'; git ls-files artifacts/review-evidence/T-140-adjuster/ prints nothing.",
   "why_it_matters": "The only end-to-end test of my ledger's $1,950.00 cannot run outside this working tree, so the guard against my r1 attack is not in the committed suite.",
   "fix": "Commit a qa-owned copy of the ledger under tests/fixtures (SYNTHETIC header kept) and read it from there.",
   "acceptance_test": "pytest tests/unit/test_amounts_d059_api.py passes on a fresh git archive of the commit."}
 ],
 "whats_right": [
  "lib10 now prints $8,123.50 and every library letter equals or (known fee cases) undercounts its records; no library letter is over",
  "Charges are never batched (422 CHARGES_NOT_BATCHED) and a flagged charge needs its exact confirm word; a wrong word is 422 and changes nothing",
  "My r1 ledger accepted one at a time exports $1,950.00, with every running, previous, credit, payment and YTD line explained in AMOUNTS NOT TOTALED"
 ],
 "questions_for_chris": []}
```
