# T-078 round 2: paralegal-reviewer (research/record-formats.md + research/record_formats_check.py, commit 327ce46)

**Verdict: pass.** All three round-1 majors are closed. The CMS-1500 grouping now follows the NUCC rule, both traps appear as specimens with stated truths, and the EMS report, ambulance invoice, CPRC 18.001 affidavit and narrative letter are present with sources and SYNTHETIC labels. The check script passes 85 of 85, and four planted faults each make it fail, so the pass is not vacuous. What is left is minor: one PT specimen has a 14-day gap that no note explains, two lib14 must-contain items have no specimen text, and the dates and fixtures need small alignments.

## Commands run and output

```
$ python3 research/record_formats_check.py
record_formats_check: 85/85 checks pass                                      exit 0
$ python3 research/record_formats_check.py -v   (saved: artifacts/review-evidence/T-078-paralegal-r2-checks-verbose.out)
85 'ok' lines, including: CMS-1500 97014 060126-060326 days = units [3 days, 3 units];
  every date marked on travel card; UB-04 room line 0120 rate x days = charge [1850.00 x 3 = 5550.00];
  UB-04 naive-sum figure stated in the note [20,181.50]; CMS-1500 OCR truths sum to Item 28 truth [390.00];
  ambulance A0425-SH units x rate = charge [8.7 x 22.50 = 195.75]; affidavit charged/paid/unpaid = ledger [445.00, 0.00, 400.00]
```

Mutation test (artifacts/review-evidence/T-078-paralegal-r2-mutation.py, output in T-078-paralegal-r2-mutation.out). Each planted fault is applied to a copy of the doc:

```
CONTROL (unmodified): 0 record_formats_check: 85/85 checks pass
M1 grouped 97014 spans 5 days, 3 units    -> FAIL CMS-1500 97014 060126-060526: days = units [5 days, 3 units]
M2 room rate 1,850.00 -> 1,805.00          -> FAIL UB-04 room line 0120: rate x days = charge [1805.00 x 3 = 5550.00]
M3 OCR truth 85.00 -> 58.00                -> FAIL CMS-1500 OCR truths sum to Item 28 truth [363.00]
M4 Spanish ambiguous date removed          -> FAIL Spanish specimen has an ambiguous day-first date with stated truth
```

NUCC 1500 manual v8.0 (artifacts/review-evidence/T-078-paralegal-r2-nucc.py, output in T-078-paralegal-r2-nucc.out): "Grouping is allowed only for services on consecutive days. The number of days must correspond to the number of units in 24G." and "Do not use dollar signs, commas, or a decimal point when reporting amounts." The doc's rule matches.

CMS Claims Processing Manual ch. 15 (artifacts/review-evidence/T-078-paralegal-r2-cms15.py, output in T-078-paralegal-r2-cms15.out): "round the total miles up to the nearest tenth of a mile", "S = Scene of accident or acute event", "each ambulance trip will require two lines of coding". The §16 claims match.

Hand checks: ledger 210 + 130 + 70 + 35 - 70 + 70 = 445, less 45 adjustment = 400. UB-04 naive sum 20,181.50 versus 9,165.75 billed. PT 38 timed minutes = 2 units (25 min) + 1 unit (13 min). PT 2x/wk x 6 wks = 12 planned visits. 05/27 to 08/04 = 69 days.

## Round-1 majors

1. **CMS-1500 follows NUCC grouping: closed.** Lines 4-5 of the clean form group 06/01 to 06/03 (three days, three units), and the travel card (lines 199-202) marks ES and H/C on all three dates. The round-1 five-day line is gone.
2. **Both traps are in the specimens: closed.** UB-04 specimen 2 (lines 450-466) has a room line with rate 1,850.00 and FL 46 = 3 days, and the note states the naive sum. OCR copy (lines 384-393) has 8500, 9000, 39000 with truths 85.00, 90.00, 390.00.
3. **EMS report, ambulance invoice, §18.001 affidavit and narrative letter: closed.** §15 (lines 703-756), §16 (760-799), §17 (803-854) and §18 (858-901) each have sources, a SYNTHETIC label on every specimen block, and a check in the script. The lib08-lib15 "formats used" references all point to sections that exist.

## Findings

1. **minor: the PT specimen now has an unexplained 14-day gap.** The round-1 fix made the 06/10 note "Visit 2 of 12" (line 144). That means no PT visit between the 05/27 evaluation and 06/10, on a 2x/wk plan (line 159), and no cancellation or no-show entry for those two weeks. The only cancellation (line 156, 06/12) says "Rescheduled 06/15/2026", and no 06/15 record exists in §3, §10 or §11. The doc's own trap at line 132 says cancellations "may state the reason for a gap". An adjuster asks about exactly this.
2. **minor: two lib14 must-contain items have no specimen text.** The v2 table (case-library-sources-v2.md:360) asks for "one handwritten date with no year" and "a page whose hidden text layer differs from the image". §14 specimen (lines 681-698) has only dated lines, and the hidden text layer is a table row (line 673). The no-year example is prose only (line 37).
3. **nit: lib09 fixture dates differ from the §13 specimen.** The v2 table (:355) asks for "03/06/2026" day-first and "14/05/2026". The §13 specimen has "17/05/2026" (line 632) and "07/06/2026" (line 641).
4. **nit: provenance dates are after the review date.** Line 9 "(2026-11-02, results in section 23)" and line 1073 "Name-collision search (2026-11-02)". The commit is 2026-11-01 21:42 -0600, so this is probably UTC. Same as T-077 F4.

Outside my lens: whether the NUBC accident-code family and the FL 45 creation-date convention are right. The doc labels both unverified, and I did not check them against the licensed manual. I did not re-run the name-collision search in §23.

```json
{"card": "T-078", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "research/record-formats.md and research/record_formats_check.py at commit 327ce46 (round 2); prior review reviews/T-078-paralegal.md; cross-read research/case-library-sources-v2.md 'Must contain' table; no app run (research card); no sample case",
 "exercised": [
  "Read personas/paralegal.md, reviews/T-078-paralegal.md, git show --stat 327ce46, research/record_formats_check.py (208 lines, full), research/record-formats.md §8-§23 in full and §1-§7 in part (traps and sections 3, 4, 10 checked directly)",
  "python3 research/record_formats_check.py -> 'record_formats_check: 85/85 checks pass', exit 0; -v run saved as artifacts/review-evidence/T-078-paralegal-r2-checks-verbose.out (85 ok lines)",
  "artifacts/review-evidence/T-078-paralegal-r2-mutation.py (+ .out): control passes; four planted faults in a copy each fail (M1 five-day span with 3 units; M2 room rate 1,805.00; M3 OCR truth 58.00; M4 ambiguous Spanish date removed)",
  "artifacts/review-evidence/T-078-paralegal-r2-nucc.py (+ .out): NUCC 1500 Manual v8.0 downloaded and text-extracted: 'Grouping is allowed only for services on consecutive days. The number of days must correspond to the number of units in 24G.' and 'Do not use dollar signs, commas, or a decimal point when reporting amounts.'",
  "artifacts/review-evidence/T-078-paralegal-r2-cms15.py (+ .out): CMS Claims Processing Manual ch. 15 checked for 'nearest tenth', 'S = Scene of accident or acute event', 'two lines of coding'",
  "Hand arithmetic: ledger 210+130+70+35-70+70 = 445 less 45 = 400; UB-04 room 1,850.00 x 3 = 5,550.00, naive sum 20,181.50 vs 9,165.75; PT 38 min = 2u + 1u; 2x/wk x 6 wks = 12; 05/27 to 08/04 = 69 days",
  "Not exercised: the §23 name-collision search; NUBC accident-code and creation-date conventions (doc marks them unverified; outside my lens); one fetch dump was written to the session scratchpad (outside the reviewer write paths, not a review artifact)"],
 "verdict": "pass",
 "scores": {"fields_and_wording_realism": 4, "extraction_traps_real": 5, "specimen_arithmetic": 5, "specimens_exercise_the_traps": 4, "coverage_for_t077_packets": 4},
 "findings": [
  {"severity": "minor", "title": "PT specimen: 14-day gap with no visits or cancellation note, and a 06/15 reschedule with no record",
   "evidence": "research/record-formats.md:144 'Daily Note Visit 2 of 12' (06/10/2026); :159 'Visit 1 was the 05/27/2026 evaluation; 2x/wk x 6 wks = 12 planned visits'; :156 '06/12/2026 Pt cancelled - no transportation. Rescheduled 06/15/2026.'; ledger lines 503-504 show only the 05/27 and 06/10 PT dates; no 06/15 entry in §3, §10 or §11.",
   "why_it_matters": "Round 1 flagged a visit count that did not match the ledger. The fix made the count match, but it now says there were no PT visits for 14 days on a 2x/wk plan, with no reason given. That is the gap-in-treatment and missed-appointment pattern an adjuster raises first, and the doc's own trap (line 132) says cancellations may state the reason. The 06/15 reschedule is never resolved.",
   "fix": "Add cancellation or no-show entries with reasons for 05/28 to 06/09 and a dated record for 06/15 (or a note that it did not occur), or label the 14-day interval DELIBERATE with its expected gap flag.",
   "acceptance_test": "record_formats_check.py asserts that each gap between dated PT visits has a cancellation or no-show note, or carries a DELIBERATE label, and that the 06/15 reschedule is resolved in the file."},
  {"severity": "minor", "title": "Two lib14 must-contain items have no specimen text",
   "evidence": "case-library-sources-v2.md:360 lib14 must contain 'one handwritten date with no year' and 'a page whose hidden text layer differs from the image'. research/record-formats.md §14 specimen (lines 681-698) has only dated lines ('Date of injury: 5/14/26', 'Signed 5/29/26'); the hidden text layer is a failure-mode table row (line 673) with no specimen; the no-year example is prose only (line 37).",
   "why_it_matters": "T-079 is told to take each packet's formats from this file. Two of lib14's required features have nothing to copy, so its expected JSON would assert features that no document in the file shows.",
   "fix": "Add to §14 a SYNTHETIC handwritten date with no year, and a SYNTHETIC page showing image text beside a hidden text layer that differs.",
   "acceptance_test": "A grep of §14 finds a specimen block with a date that has no year, and a block where the text layer line differs from the image line."},
  {"severity": "nit", "title": "lib09 fixture dates differ from the §13 specimen",
   "evidence": "case-library-sources-v2.md:355 lib09 must contain 'One date 03/06/2026 day-first (truth 3 June 2026) and one 14/05/2026'. research/record-formats.md:632 'Fecha: 17/05/2026' and :641 '(07/06/2026)'; neither 03/06/2026 nor 14/05/2026 appears in §13.",
   "why_it_matters": "The packet expectations and the format file disagree on the ambiguity fixture. Harmless if T-079 chooses its own dates; confusing if it copies §13.",
   "fix": "Align the lib09 row with the §13 dates, or state that the packet builder chooses its own day-first dates.",
   "acceptance_test": "Every date named in the lib09 row appears in §13, or the row says the dates are free choices."},
  {"severity": "nit", "title": "Provenance dates are after the review date and do not say which timezone",
   "evidence": "research/record-formats.md:9 'A web search ... (2026-11-02, results in section 23)'; :1073 'Name-collision search (2026-11-02)'. Commit 327ce46: 'Date: Sun Nov 1 21:42:39 2026 -0600'.",
   "why_it_matters": "Probably UTC, but a reader cannot tell. The same issue is in T-077 F4.",
   "fix": "State the timezone or use the local date.",
   "acceptance_test": "Each date in the doc matches the commit date in the stated timezone."}
 ],
 "whats_right": [
  "The NUCC grouping is now consistent: every grouped line has days = units and the travel card marks every date, and the rule text matches the NUCC v8.0 manual extracted for this review.",
  "Both traps are specimens with stated truths: a UB-04 room line (1,850.00 x 3 = 5,550.00, naive sum 20,181.50 stated) and an OCR copy with decimal-less amounts (8500, 9000, 39000) whose truths are 85.00, 90.00, 390.00.",
  "The 85 checks bite: four planted faults in a copy each make the matching check fail, so 85/85 is not vacuous."],
 "questions_for_chris": [
  "Were the 2026-11-02 dates in record-formats.md and case-library-sources-v2.md meant as UTC? (F4 in both reviews.)"]}
```
