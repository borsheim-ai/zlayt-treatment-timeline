# T-078 review: paralegal-reviewer (research/record-formats.md, commit 1193f8a)

**Verdict: changes.** The field lists, wording and traps read like what lands in a Texas PI file. The ED/PT/chiro/radiology/op-note/pharmacy/ledger/EOB/LOP specimens look right. The UB-04, ledger, EOB and CMS-1500 totals add up. The EOB arithmetic is clean, line by line. Three things need fixing before T-079 copies these specimens into packets. One CMS-1500 line breaks the NUCC rule the doc itself quotes. The two headline traps (UB-04 rate on the charge line, CMS-1500 amounts with no decimal) are described but not shown in the specimens. And T-077's proposed packets need formats this doc doesn't have.

## Arithmetic check (script and output saved)
`artifacts/review-evidence/T-078-paralegal-arith.py`, output in `artifacts/review-evidence/T-078-paralegal-arith.out`.
- UB-04: 2,410.00 + 3,185.00 + 96.00 + 38.50 = 5,729.50, correct. Ketorolac 30 mg IM = 2 units of J1885 (15 mg) = 96.00, consistent with the ED note.
- CMS-1500: 85 + 30 + 45 = 160, correct. **Line 3 fails the grouping rule** (finding 1).
- Ledger: 210 + 130 + 70 + 35 - 70 + 70 = 445, less 45 = 400, correct.
- EOB: every line balances (billed - discount = allowed; allowed - deductible - coinsurance = plan paid; deductible + coinsurance = "you may owe"). Totals 235 / 115 / 120 / 100 / 4 / 16 / 104 are right. The worked example in the typical-wording paragraph also checks.
- PT note: 35 timed minutes is 2 units under the 8-minute rule; the specimen bills 3 (finding 4).

## The three UB-04 details flagged as unverified (section 16)
I could not check these against the licensed NUBC manual. The RI Medicaid guide the researcher opened (I re-extracted it) does not address any of them. These verdicts come from my own working knowledge, so treat them as a paralegal's read.
1. **FL 44 holds an accommodation rate on inpatient room lines, HCPCS on outpatient lines: correct.** The RI guide says only "44 HCPC - Utilized for outpatient bills" and "46 Service Units ... hospital accommodation days", which is consistent. Rate times days equals FL 47 on those lines.
2. **Claim creation date in FL 45 on the 0001 total line: correct.** RI says "After the last Revenue Code, enter '0001' ... (PAPER CLAIMS ONLY)" but nothing on the date. The creation-date convention is real.
3. **Occurrence code 01 for the accident: right but too narrow.** Codes 01 to 06 are all accident-type (01 medical-coverage accident, 02 no-fault, 03 tort liability, 04 employment-related, 05 no medical/liability coverage, 06 crime victim). A PI hospital claim may carry 01 or 03. Extraction should treat any of them as an accident date, never a service date. The doc's wording implies 01 only (finding 6).

## Source spot-opens
NUCC 1500 manual v8.0 (the 24A grouping rule and "Do not use dollar signs, commas, or a decimal point" both match), RI UB-04 instructions, Noridian chiropractic page ("Daily notes must be specific to the date of service"; "exact spinal segment"), Noridian EOB examples, CMS "how to read your medical bill" (total charges, allowed, adjustments), arXiv 2511.13523 (Tesseract CER 0.189, WER 0.276, numeric accuracy 0.756), Jotform LOP packet (continuing lien, no collections). All matched the doc.

```json
{"card": "T-078", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "research/record-formats.md at commit 1193f8a; cross-read with T-077 v2 doc proposed packets, board cards T-078/T-079; no app run (research card)",
 "exercised": [
  "Read personas/paralegal.md, the whole record-formats doc, the T-077 doc, board.py show T-077/T-078/T-079, D-042",
  "Wrote and ran artifacts/review-evidence/T-078-paralegal-arith.py (output in T-078-paralegal-arith.out) to re-add the UB-04, CMS-1500, ledger and EOB specimens, test the PT unit rule and the 24A units rule, and the date-order cases",
  "Downloaded and text-extracted: NUCC 1500 manual v8.0 (lines 1202-1204 on 24F, 1351-1352 on 24A grouping), RI EOHHS UB-04 instructions (FL 4, 6, 12, 13, 42, 44-48)",
  "Opened: Noridian JF-B chiropractic documentation page, Noridian JF-A MSP EOB examples, CMS medical bill guide, arXiv 2511.13523 html, Jotform LOP packet",
  "Cross-read every specimen for internal consistency against the others (dates, visit counts, imaging types, units, payments)"],
 "verdict": "changes",
 "scores": {"fields_and_wording_realism": 4, "extraction_traps_real": 4, "specimen_arithmetic": 3, "specimens_exercise_the_traps": 2, "coverage_for_t077_packets": 2},
 "findings": [
  {"severity": "major", "title": "CMS-1500 line 3 violates the NUCC grouping rule the doc quotes, and the chiro travel card does not support it",
   "evidence": "record-formats.md line 358: '060126  060526  11  97010  A  45 | 00  3' means 06/01 to 06/05 = 5 calendar days, 3 units. Doc lines 28 and 338 state the rule: 'days must equal units'. NUCC manual v8.0 24A: 'Grouping is allowed only for services on consecutive days. The number of days must correspond to the number of units in 24G.' The line-363 note says 'groups three dates on one line with 3 units'. The travel card (lines 191-195) shows visits on 06/01, 06/03, 06/05 only (non-consecutive) and marks HP on 06/01 and 06/03 only, so hot/cold is documented 2 times, not 3. Script output: 'range 060126-060526 = 5 calendar days; units billed = 3; ... -> False'.",
   "why_it_matters": "This is the specimen meant to teach 'one line is not one visit'. As written, the truth is ambiguous: 5 days, 3 units, 2 documented. A fixture built from it has no derivable expected value. Real payers also reject this grouping, so a paralegal would flag the claim form, not trust it.",
   "fix": "Make line 3 consistent, e.g. 060126 060526 with 5 units at $15 = $75 and a travel card with HP on all 5 days (total becomes 190), or split into three single-date lines. If the mismatch is deliberate, label it 'DELIBERATE: units != days' and state the expected tool output.",
   "acceptance_test": "The script recomputes (To - From + 1) == units for every grouped line and checks the travel-card mark count equals units; both pass, or the specimen carries an explicit DELIBERATE label."},
  {"severity": "major", "title": "The two headline traps are in the prose but not in the specimens",
   "evidence": "(a) Section 15 maps UB-04 to 'FL 44 rate' and the handoff calls the rate-on-the-charge-line 'a ready-made D-042 rate-vs-charge trap', but the UB-04 specimen (lines 398-409) has no room-and-board line: FL 44 holds only HCPCS codes 99284, 72125, J1885 or is blank. There is no 0120/0110 line, no rate like 1850.00, no days in FL 46. (b) The CMS-1500 specimen is introduced as 'the OCR text a scanned form tends to produce' (line 348), yet every amount is `85 | 00`, `30 | 00`, `160 | 00`. The `15000` and `150 00` variants are only in the section 8 and section 14 prose.",
   "why_it_matters": "T-079 AC1 requires a rate-vs-charge trap packet. A builder who copies the specimens gets neither trap. A UB-04 where rate and charge share a line is the one place a naive total can go wrong by 3x. The decimal-less CMS-1500 amount is how $150 becomes $15,000.",
   "fix": "Add an inpatient UB-04 specimen with e.g. '0120 ROOM & BOARD SEMI-PVT  [FL44] 1,850.00  [FL45] 051526  [FL46] 3  [FL47] 5,550.00' and the 0001 total recomputed. Add a second CMS-1500 specimen in degraded OCR form, e.g. '8500', '30 00', '16000', plus the clean boxed form.",
   "acceptance_test": "Specimen check: UB-04 has a line where FL44 x FL46 == FL47; CMS-1500 has at least one amount string with no separator whose truth value is stated beside it."},
  {"severity": "major", "title": "Formats that the T-077 packets need are missing: EMS run report, ambulance invoice, 1.18.001 affidavit/cover page, treater narrative letter",
   "evidence": "T-077 proposals: lib08 starts with EMS and a second crash; lib14 'ambulance base + mileage invoice'; lib15 'EMS minor-damage and refused-transport wording' and an 'Accident caused all' letter plus billing-affidavit cover pages (P3). record-formats.md has no section for any of these (grep for 'run report', 'ambulance', 'affidavit' finds only passing mentions at lines 59, 173, 500). The ED specimen itself says 'Mode: EMS' with no EMS record. A pain-management/ESI procedure note and a work-status slip are also absent, though pain management is in the sample case.",
   "why_it_matters": "The AC list is met (12 named formats). But T-079 is told to build from 'the research patterns and formats', and three of its eight packets rest on documents this file cannot specify. The ambulance run sheet is the first record in nearly every MVC file, and the narrative letter and 18.001 affidavit are in almost every demand package.",
   "fix": "Add four short sections in the same shape (fields, wording, traps, SYNTHETIC specimen): EMS patient-care report, ambulance invoice (base + mileage), CPRC 18.001 business-records/billing affidavit with its cover page, treating-provider narrative letter. Optional: pain-management procedure note.",
   "acceptance_test": "Each lib08-lib15 row in the T-077 table can name the section in record-formats.md that specifies every document type it uses."},
  {"severity": "minor", "title": "PT specimen bills 3 timed units for 35 timed minutes, contradicting the 8-minute rule the doc cites",
   "evidence": "record-formats.md lines 142-145: '97110 23 min 2u; 97140 12 min 1u; Total timed 35 min'. The doc's own trap list (line 124) says 'Timed codes bill in 15-minute units under the 8-minute rule', and cites a bulletin where 40 minutes = 3 units. Script: 'PT timed minutes 35 -> CMS total timed units 2 | specimen bills 2u + 1u = 3'. The ledger (lines 446-447) repeats the 3 units ($130 + $70).",
   "why_it_matters": "Under the CMS total-time method this is a 1-unit over-bill. Commercial payers often use the AMA per-code method, where 3 is acceptable. The doc doesn't say which method the specimen follows, and an adjuster could treat it as an error.",
   "fix": "Either change minutes (e.g. 97110 25 min, 97140 13 min = 38 min = 3 units), or add a line 'units per AMA per-code method; CMS total-time method would give 2'.",
   "acceptance_test": "The script confirms units match total timed minutes under the stated method."},
  {"severity": "minor", "title": "The Delphine specimens do not agree with each other in several places",
   "evidence": "(1) Radiology COMPARISON 'Cervical radiographs 05/15/2026' (line 231), but the ED did and billed a CT cervical spine (lines 102, 404) and no radiographs. (2) Chiro 'Visit #9' on 06/03 (line 183) but the intake is signed 5/29/26 (line 624): nine visits in six days. (3) PT 'Visit 7 of 24' on 06/10 (line 138) but the ledger shows only the 05/27 eval and the 06/10 visit (lines 445-450). (4) Ledger 'Financial class: LOP', payments blank, TOTAL PMTS 0.00, while the EOB for the same 06/10 DOS shows plan paid $16.00 and $115.00 of CO-45/CO-97 reductions. (5) Op note 'not improved with 12 weeks of therapy' (line 280): 05/27 to 08/04 is 69 days, 9.9 weeks. (6) PT plan '3x/wk x 4 wks' against 24 planned visits.",
   "why_it_matters": "Items 4 and 5 are realistic traps (paid-or-incurred; therapy duration the adjuster will count), but nothing marks them as deliberate. If T-079 packages these as one case, the golden truth will contain unplanned conflicts and the tool will rightly flag them.",
   "fix": "Fix or annotate each as DELIBERATE with its expected flag. For (4) add a note that the packet tests ledger vs EOB mismatch and expects a billing-analysis flag.",
   "acceptance_test": "A short cross-check table lists every cross-specimen mismatch and marks it fixed or deliberate."},
  {"severity": "minor", "title": "UB-04 occurrence-code wording is too narrow, and two UB-04 conventions are stated as fact in the trap lists while still unverified",
   "evidence": "Section 16: 'occurrence code 01 for accident ... from my prior knowledge'. Section 9 specimen uses '31 OCCURRENCE CODE 01'. Section 1.1 (line 23) and section 9 traps state 'FL 45 on the total line is the claim creation date' without the caveat. RI guide (re-extracted) says 'See NUBC manual for specific codes' and does not mention creation date.",
   "why_it_matters": "PI claims may carry 01 or 03 depending on who is billed. A generator that always emits 01 under-tests accident-date detection. The creation-date convention is real, but a reader of section 1.1 would not know it is unsourced.",
   "fix": "Say 'accident codes 01 to 06; extraction treats any as an accident date'; vary the code across packets; add '(unverified)' next to the creation-date lines in sections 1.1 and 9.",
   "acceptance_test": "Section 9 names the code family; at least two UB-04 packets use different codes; unverified claims carry the marker in every place they appear."},
  {"severity": "minor", "title": "The Spanish specimen does not exercise the day-first trap, and 'no provider or payer name is real' is asserted without a check",
   "evidence": "Spanish note dates are 'Fecha: 17/05/2026' and '(24/05/2026)', both day > 12 and unambiguous; the trap table uses '03/06/2026 is 3 June', and section 15 says 'choose days <= 12 so the ambiguity is real'. The header says 'No person, provider, payer, address... is real', while section 16 says any resemblance of 'Quillfeather, Larkspur Hollow, Harrowgate & Vey' is 'unintended'. Names like 'Bluebonnet Mutual Health Plan', 'Clinica Familiar Los Almendros' and 'Dra. Ines Valcarcel' are common enough in Texas and Mexico that a collision is plausible. AC2 evidence mentions only a regex for SSN/phone patterns.",
   "why_it_matters": "A day-first date that cannot be misread tests nothing. The unsupported absolute 'none is real' is the kind of claim the data rule says we must not make without evidence.",
   "fix": "Change one Spanish date to e.g. 03/06/2026 with a stated truth; soften the header claim or run a name-collision search on every provider, payer, firm and clinician name and record the result.",
   "acceptance_test": "The Spanish specimen contains at least one date with day and month both <= 12 and states its truth; the doc records a collision search or drops the absolute claim."},
  {"severity": "nit", "title": "The doc says twelve formats but has thirteen sections; CMS-1500 PTR/MOD columns are ambiguous",
   "evidence": "Purpose paragraph: 'twelve document types'; sections 2 to 14 are thirteen (PT and chiro are separate); the handoff says 13. CMS-1500 specimen row '98941  AB  85 | 00' sits under the 'MOD' header, so 'AB' reads as a modifier rather than the diagnosis pointer (valid modifiers for chiro manipulation would be AT).",
   "why_it_matters": "Small, but an extractor test built on it can misattribute the field.",
   "fix": "Say thirteen; align the columns and add AT for 98941 if Medicare-style, or leave blank.",
   "acceptance_test": "Count in the intro matches the section count."}
 ],
 "whats_right": [
  "The cross-cutting trap list (service date vs creation/fax/received/statement dates, running balance, voids, one visit with several bills, rate vs charge wording) is what bites me in real files.",
  "The EOB, ledger, UB-04 and CMS-1500 totals re-add correctly, and the ED midnight-rollover line dates on the UB-04 (ER on 051426, CT and injection on 051526) match the ED note.",
  "Sources are honestly marked opened vs search summary, and the NUCC quotes ('no decimal point', 'consecutive days') match the manual."],
 "questions_for_chris": []}
```
