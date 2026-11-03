# T-140 r3 — claims-adjuster-reviewer (Gary Pruitt, BI adjuster / defense adversary)

**Verdict: fail** (4 blockers, 1 major, 1 nit). Commit 35d8280 (HEAD), taken with `git archive HEAD` into my session scratchpad. I ran my own server on 127.0.0.1:7875 (`LLM_BACKEND=fixture`, `FIXTURE_SET=curated`, `ZLAYT_MODE=local`, `ZLAYT_DB` in the scratchpad), PID 87124. I stopped it with `kill 87124`, and `lsof -nP -t -iTCP:7875 -sTCP:LISTEN` then printed nothing (exit 1).

**What r3 fixed, and I checked it.** My r1 and r2 SYNTHETIC ledgers now export **"Billed charges stated in these records: $1,950.00"** on path A (one at a time, no confirm) and on path B (named confirms). Both totals are correct. A batch that includes a charge is refused with `422 CHARGES_NOT_BATCHED`. Two identical units on one statement stay two charges. A later statement that restates both units in another date format ("4/9/26 97110 Ther ex") merges one-for-one. No library case goes over what its records state. The sample case gives $8,390.00, with $185 kept as a rate and the missed work kept as damages.

**It still fails against default-deny.** My third ledger (`artifacts/review-evidence/T-140-adjuster-r3/default_deny_ledger.txt`, SYNTHETIC) states $1,950.00 of distinct services:
- ED $1,000
- PT evaluation $200
- two $75 units on 04/09
- manual therapy $150 on each of 04/16, 06/10 and 06/24
- therapeutic exercise $150 on 05/07

I accepted every charge one at a time. On both paths the letter reads **"Billed charges stated in these records: $3,850.00"**. Nothing in the $1,900 overstatement was flagged:
- **+$650**, a summary row dressed as a service line on the June statement: "05/31/2026  97110  Physical therapy, April-May  $650.00". It equals 200+75+75+150+150, which records 2 and 3 already list.
- **+$950**, the discharge summary's "Physical therapy charges: $950.00.". This is every PT charge in records 2 to 4 again.
- **+$150**, a med pay ledger from an auto carrier: "04/09/2026  97110  Therapeutic exercise x2  $150.00  $90.00  $72.00". The carrier rolled up the two $75 units that are already counted.
- **+$150**, the 04/16 visit restated as "Apr 16, 2026  CPT 97140  Manual therapy  $150.00". It did not merge with "04/16/2026  97140  Manual therapy  $150.00" because the "CPT " prefix changes the code key.

**What should have merged did merge:**
- the two 04/09 units (records r2 and r4, kept as two)
- the 06/10 visit (r4 and r5)

Default-deny limits what a charge line looks like. It cannot tell a summary row, an insurer's restatement or a course-of-care sentence from an itemized line, because all three have a date, a service and an amount. The cross-check that would catch a sum (`_likely_totals`) only looks inside one record. Insurer detection is still a closed word list.

**Library (all 15 cases, on my server, every amount accepted one at a time; no case raised a flagged charge, so path A equals path B):** lib01 $3,915.00, lib02 $2,260.00, lib03 $7,500.00, lib07 $2,620.00, lib08 $11,240.00, lib10 $8,123.50, lib13 $5,830.00 and lib14 $4,527.05 match their records. The rest are undercounts, which are accepted, so I note them and do not file them:

| case | letter | records state |
|---|---|---|
| lib04 | $4,730.00 | $8,630 |
| lib05 | $38,420.00 | $44,570 |
| lib06 | $5,280.00 | $6,830 (was $6,380 at r2) |
| lib09 | $5,090.00 | $6,390 |
| lib11 | $3,260.00 | $6,000 (was $6,000 at r2) |
| lib12 | $2,780.00 | $5,790 (was $5,790) |
| lib15 | $385.00 | $3,295 (was $3,295) |

The reasons are written in each expected.json `accept_all_reason`.

Outside my lens: the pasted English ledger was routed to an `extract_es` step (my first harness run failed with `KeyError: 'extract_es'`). That is for the staff-engineer reviewer.

```json
{"card": "T-140", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 35d8280 (HEAD) via git archive HEAD into the session scratchpad; app on http://127.0.0.1:7875 (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, ZLAYT_DB in scratchpad); sample case; all 15 evals/library cases; SYNTHETIC ledgers artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt (r1), artifacts/review-evidence/T-140-adjuster-r2/attack_ledger.txt (r2), artifacts/review-evidence/T-140-adjuster-r3/default_deny_ledger.txt (new); app/backend/amounts.py (charge_basis, same_service, _merge_same_service, _likely_totals, is_insurer_document)",
 "exercised": [
  "read personas/claims-adjuster.md, D-059 and D-060 in memory/ORCHESTRATOR_DECISIONS.md, reviews/T-140-claims-adjuster-r2.md, python3 tools/board.py show T-140 (incl. orchestrator merge note 2026-11-02T14:48:14Z: same-statement identical lines never merge); git show HEAD -- app/backend/amounts.py",
  "git rev-parse HEAD -> 35d828056b967bfd98e8c38ce75610139dcb074f; git archive HEAD into scratchpad/tree3",
  "pytest tests/unit/test_amounts_d060.py test_amounts_d059_api.py test_amounts_d059.py test_amounts_t140.py test_amounts.py test_billing.py test_export.py on the tree: '656 passed in 16.60s'",
  "server: env HOST=127.0.0.1 PORT=7875 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=scratchpad/db3/app.sqlite3 python -m app.main; /api/health backend=fixture demo_mode=true; PID 87124, stopped with kill 87124; lsof -nP -t -iTCP:7875 -sTCP:LISTEN printed nothing",
  "probe_paste_r2.py (in-process TestClient on the tree, the worker's scripted call-factory harness, every amount accepted one at a time; path A no confirm, path B named confirms) on the r1 and r2 ledgers: both $1,950.00 on both paths; batch with a charge 422 CHARGES_NOT_BATCHED (artifacts/review-evidence/T-140-adjuster-r3/paste_r1_r2_ledgers_out.txt)",
  "artifacts/review-evidence/T-140-adjuster-r3/probe_paste_r3.py (same harness plus the extract_es step) on default_deny_ledger.txt: path A and path B both 'Billed charges stated in these records: $3,850.00' vs $1,950.00 stated (paste_default_deny_out.txt); debug_run_r3.py showed the first run's failure was KeyError 'extract_es' in the harness",
  "artifacts/review-evidence/T-140-adjuster-r3/probe_variants_r3.py through amounts.extract_amounts: 9 summary-row forms, 3 summary sentences, 7 insurer source labels, 3 same-day-unit cases, 13 code-less restatements, 4 coded restatements, 3 note summaries (variants_r3.txt)",
  "code-form probe: '97140' vs 'CPT 97140' / 'CPT#97140' not merged; 'CPT: 97140', 'HCPCS G0283', '97140GP' merged (code_forms_r3.txt)",
  "probe_library_r2.py against http://127.0.0.1:7875 on all 15 library cases: batch 422, entries/flags/amounts one at a time, path A and path B totals (library_r3.txt); compared to the records-state totals in my r2 review table and the expected.json accept_all_reason text",
  "sample case over HTTP: path A and path B 'Billed charges stated in these records: $8,390.00'; $185 class rate; 'missing 3 days of work' class damages (sample_r3.txt)"
 ],
 "verdict": "fail",
 "scores": {"letter_total_not_overstated": 2, "restatements_merged_or_flagged": 2, "same_statement_units_kept_separate": 5, "library_no_overcount": 5, "charge_lines_cite_own_source": 4},
 "findings": [
  {"severity": "blocker", "title": "A summary row dressed as a service line (date + CPT + a total) is counted as a charge, with no flag",
   "evidence": "artifacts/review-evidence/T-140-adjuster-r3/paste_default_deny_out.txt path A and path B: 'LETTER: Brindlewood Physical Therapy, billing statement, June 1, 2026: $650.00' / 'Source [Ex. __ / Bates __]: \"05/31/2026  97110  Physical therapy, April-May  $650.00\"'. The $650 equals 200 + 75 + 75 + 150 + 150, which records 2 and 3 already list. variants_r3.txt: 9 of 9 row forms ('Therapeutic exercise (5 visits)', 'PT services this period', 'Physical therapy summary', 'Therapy, 04/02/2026-05/31/2026', ...) and 2 of 3 sentence forms give 'charges $1,300.00 vs records $650.00 -> OVER'. app/backend/amounts.py:500 _likely_totals only compares the charges of one record.",
   "why_it_matters": "This is the overstated special I would cite: a statement-period summary counted on top of the visits it adds up. D-060 says account summaries are unclear, but the shape rule cannot see this one, and the D-059 likely-total flag cannot see across statements.",
   "fix": "Run the likely-total check across records. A charge that equals the sum of at least two other charges of the same provider (the source label before the comma), dated on or before its own date of service, gets the likely_total flag and needs the named confirm. Keep the in-record check.",
   "acceptance_test": "default_deny_ledger.txt: the $650.00 row carries flag likely_total; accepting every amount one at a time with no confirm gives a letter total of at most $1,950.00; the 9 summary-row forms in probe_variants_r3.py are flagged or unclear."},
  {"severity": "blocker", "title": "A course-of-care charge sentence in a discharge summary is counted on top of the itemized bill",
   "evidence": "paste_default_deny_out.txt: 'LETTER: Brindlewood Physical Therapy, discharge summary, July 2, 2026: $950.00' / 'Source [Ex. __ / Bates __]: \"Physical therapy charges: $950.00.\"'. $950 is every PT charge in records 2 to 4. variants_r3.txt: 'note summary: Manual therapy charges: $300.00.: charges $600.00 vs records $300.00 -> OVER'. The path is the encounter-note branch, app/backend/amounts.py:449-459 (a service noun plus a charge word is enough). D-060 limits charges to an itemized service line 'in a provider bill or ledger'.",
   "why_it_matters": "A narrative note that restates the whole bill doubles the PT specials in the letter. Any bill review would catch it, and the whole package would be discounted for it.",
   "fix": "Apply the cross-record likely-total check (finding 1) to encounter-note charges too. Also, when the same provider's itemized bill lines are in the case, give a note-level 'X charges: $N' the likely_total or likely_duplicate flag with the named confirm. The note sentence is never counted silently.",
   "acceptance_test": "default_deny_ledger.txt record 6 $950.00 is flagged (or unclear with a reason in internal notes); path A total at most $1,950.00; sample case still $8,390.00."},
  {"severity": "blocker", "title": "An insurer document whose name is not on the insurer word list is read as a provider bill; its rolled-up row is counted",
   "evidence": "paste_default_deny_out.txt: 'LETTER: Pecan Valley Auto Club, med pay ledger, July 20, 2026: $150.00' / 'Source [Ex. __ / Bates __]: \"04/09/2026  97110  Therapeutic exercise x2  $150.00  $90.00  $72.00\"'. The provider's two $75 units for that day are already counted. The table header is 'DOS  CPT  Service  Billed  Approved  Paid'. variants_r3.txt: '== insurer: Lone Star Benefit Administrators, claims statement: charges $450.00 vs records $300.00 -> OVER'. The same OVER result appears for 'claim detail statement', 'Acme Auto Group, med pay ledger', 'Acme Auto Group, PIP statement' and 'Hill Country TPA, account statement'. Only 'Health Plan' and 'Mutual' are caught. app/backend/amounts.py:144 _INSURER_SRC is a word list; :232 _insurer_table needs an 'Allowed' header.",
   "why_it_matters": "D-060 says insurer documents are unclear. In a Texas auto file, a med pay or PIP ledger is exactly what lands in the packet, and its billed column restates the provider's bill. A rolled-up unit line does not merge with the provider's unit lines, so it is counted twice.",
   "fix": "Decide by structure as well as by name. A table row that carries a billed figure together with a payer figure (column headed approved, allowed, paid, benefit, covered, plan or payment, on the same row) is a payer restatement: unclear, with the insurer reason. Also add med pay, PIP, personal injury protection, benefit(s) administrator, TPA and claims statement to the insurer words.",
   "acceptance_test": "The 7 insurer labels in probe_variants_r3.py give no charge from record 2. default_deny_ledger.txt record 5 gives no charge. The worker's lib10 ($8,123.50) and both earlier ledgers ($1,950.00) are unchanged."},
  {"severity": "blocker", "title": "The same visit restated with a 'CPT ' prefix is counted twice: the code key differs and codes decide alone",
   "evidence": "paste_default_deny_out.txt prints both 'Source [Ex. __ / Bates __]: \"04/16/2026  97140  Manual therapy  $150.00\"' and 'Source [Ex. __ / Bates __]: \"Apr 16, 2026  CPT 97140  Manual therapy  $150.00\"' at $150.00 each. code_forms_r3.txt: \"'97140' vs 'CPT 97140' -> [('charge', [1]), ('charge', [2])]\" and \"'97140' vs 'CPT#97140' -> [('charge', [1]), ('charge', [2])]\", while 'CPT: 97140' merges. app/backend/amounts.py:386 keys the code as the whole match with spaces removed ('CPT97140'), and :586 same_service returns the code comparison with no fallback when both lines are coded.",
   "why_it_matters": "This is the case D-060 says must merge: same provider, same date of service, same code, same amount, on a later statement. The letter double-counts it with no flag.",
   "fix": "Normalize a code to the bare code: strip the CPT/HCPCS/Rev label, '#', ':' and modifiers. If two coded lines do not share a code, fall back to the description tokens before you decide they are different services.",
   "acceptance_test": "Unit test: '97140' merges with 'CPT 97140', 'CPT#97140', 'CPT: 97140', '97140-GP' and 'CPT 97140-59' on the same date and amount in another record. default_deny_ledger.txt 04/16 is one amount citing r2 and r3."},
  {"severity": "major", "title": "Same provider, date of service and amount on two statements with different descriptions: no merge and no flag, counted twice",
   "evidence": "variants_r3.txt: '== restated without code on stmt 1: 04/16/2026  PT visit  $150.00: charges $300.00 vs records $150.00 -> OVER' with both amounts flag=None. D-059's extraction-time likely_duplicate flag was replaced by the D-060 merge (amounts.py:592 _merge_same_service), so a near-match now falls between the two: it is neither merged nor flagged.",
   "why_it_matters": "A same-day, same-amount line from the same provider on two statements is the first thing my bill review asks about. The tool cannot know whether it is one visit or two services, but it must not hide the question.",
   "fix": "When provider, date of service and amount match across records and same_service is false, flag the later one likely_duplicate with the named confirm. Never merge it.",
   "acceptance_test": "probe_variants_r3.py 'PT visit' restatement: the second $150 carries likely_duplicate; path A (no confirm) total is $150.00."},
  {"severity": "nit", "title": "Two identical units on one statement print two identical Source lines with no unit or line marker",
   "evidence": "paste_default_deny_out.txt: 'Source [Ex. __ / Bates __]: \"04/09/2026  97110  Therapeutic exercise  $75.00\"' printed twice under 'Brindlewood Physical Therapy, billing statement, May 1, 2026: $75.00'.",
   "why_it_matters": "Both quotes are verbatim, and the two units are real. On my desk, though, two identical source lines read as a double bill until the paralegal fills in distinct Bates or line references.",
   "fix": "Optional: add 'line 2 of 4' (code-derived row position) to the Source line when a record has identical lines.",
   "acceptance_test": "Two identical rows in one record print Source lines that differ by a line marker."}
 ],
 "whats_right": [
  "Both earlier SYNTHETIC ledgers export $1,950.00 on path A and path B; a batch with a charge is refused 422 CHARGES_NOT_BATCHED.",
  "Two identical $75 units on one statement stay two charges, and a later restatement of both ('4/9/26 97110 Ther ex') merges one-for-one (r2+r4).",
  "No library case overcounts (lib10 $8,123.50, lib11 $3,260.00 under its $6,000); sample $8,390.00 with $185 kept as a rate."
 ],
 "questions_for_chris": [
  "D-060 limits charges to an itemized line 'in a provider bill or ledger', but the worker also counts a dated encounter note's 'X charges: $N' (the sample's 'Charge: $2,150' needs it). Should a note-level charge be counted silently when the same provider's itemized bill is in the packet, or always need a named confirm?"
 ]}
```
