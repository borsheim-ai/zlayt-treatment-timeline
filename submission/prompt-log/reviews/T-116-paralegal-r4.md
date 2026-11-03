# T-116 round 4 review: paralegal-reviewer (Maria Delgado persona)

Commit under review: 8b4ff11 (`git log --oneline -1` = 8b4ff11; `board.py show T-116` lists c1b44be, ea6ac71, 8673326, 8b4ff11).
Pre-T-116 baseline: 3e3f3b7. Both trees were extracted with `git archive` into the scratchpad (`t116r4/head`, `t116r4/pre`); the
dirty project tree was not used for any result except the second pytest line. Binding rule: D-055 (never exclude by guessing; warn and show the alternative).

## Verdict: fail (one blocker, two minors, one nit)

Round 4 fixes what r3 reported. The five visit labels that invented a 40-day gap are gone, the W4 hidden gap shows, the mid-span split shows
a conditional flag, and the accident baseline no longer calls a plain intake form the first treatment. One new defect remains, and it is the same
sin as before in a smaller place: the warning and the conditional flag are switched off by a text guess. If the paperwork excerpt contains
a diagnosis line, 'performed', or 'seen by', the record is counted as a visit with no warning, no alternative, and no conditional flag.
That hides a real 40-day span that pre-T-116 showed, and it is exactly what a bill, an EOB, a records request or an intake questionnaire says.

## What I confirmed (re-run of every r1 to r3 probe label, on HEAD)

1. **No gap invented or hidden by a label: 60/60 label runs.** 27 visit labels + 3 controls, plain and headed excerpt, inside a three-visit
   packet (`T-116-paralegal-r3-probe.py` reused unchanged, output `T-116-paralegal-r4-labels-head.out.txt`). Every run counts every dated record
   (gap rows 19 and 21 days). No visit label draws a 40-day flag. The five r3 failures now behave: 'Capital PT, initial evaluation, correspondence',
   'Dr. Lee, chiropractic, visit 3 - records request copy', 'Office visit / records request', 'Capital PT, visit 5 (ledger balance reviewed)' and
   'Austin Imaging, MRI cervical spine (records request attached)' (ingest kinds are still records_admin or billing_statement, but gap math no longer reads them).
   W4 (visit labelled 'visit 3 - records request copy' ending a 40-day span) now shows a 40-day flag, 2026-03-01 to 2026-04-10
   (`T-116-paralegal-r4-warn-and-api.head.out.txt`).
2. **Appendix A sample: 10/10 variants keep the 73-day flag (records 6 and 7)**, including ', fax' on each treatment record; the 28-day interval is not
   flagged (`T-116-paralegal-r4-compare.out.txt` section B).
3. **Paperwork that starts, ends or splits a gap shows the conditional sentence, in plain text, with record number, verbatim header and both day counts.**
   - Ends: W1 'If record 2: Capital PT, intake form is paperwork, not a visit, there would be no visit after it and no gap to measure.' (no X days exists, so it says so).
   - Starts: lib10: 'This gap starts at record 8: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim), which looks like paperwork, not a visit. Check whether treatment continued. If record 8: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim) is paperwork, not a visit, the gap would be 49 days (July 8, 2026 to August 26, 2026).'
   - Splits: W3 'Possible gap of 40 days ... No gap is counted here because record 2: Capital PT, intake form (March 20, 2026) falls inside this span and is counted as a visit (19 days, then 21 days). If record 2: Capital PT, intake form is paperwork, not a visit, the gap would be 40 days (March 1, 2026 to April 10, 2026).' Also case_09 (56 days, records 2 and 3, plural wording 'are paperwork, not visits') and lib06 (35 days, record 4).
   - lib09 through the API: before confirm 42 days; after confirming record 4 as 5 March, 40 days, start warning with record 4 and its verbatim header, alternative 42 days (March 3 to April 14), and gap_changes 'now 40 days (was 42)'.
4. **lib10: 49 days becomes 43 days with the 49-day alternative shown, and that is right per the packet text.** Record 8 is dated 2026-07-14 and
   reads 'OCR of scanned CMS-1500 for dates of service 06/24/2026 and 07/08/2026 ... Item 29 AMOUNT PAID 0 00'. D-055 counts it as a dated record (07-14 to 08-26 = 43).
   The last visit in the packet is record 7 on 07-08 (07-08 to 08-26 = 49). Both numbers, both date ranges, and the record named appear in explanation, why and endpoint_warnings.
   No flagged golden or library gap is lost: for all 25 packets, every pre-T-116 flagged row is either a counted flag with the same dates or shown as an alternative
   (`T-116-paralegal-r4-packet-flags.out.txt`; only lib10 changes its counted dates, only case_09 and lib06 become conditional flags, 22/25 flag lists identical).
5. **Accident baseline, plain intake form:** the HEAD sentence reads 'later than the earliest recorded date, January 12, 2026 (record 1: Capital PT, intake form), which looks like paperwork, not a visit ... If record 1 ... is paperwork, not a visit, the first recorded visit is January 20, 2026 (record 2: Capital PT, initial evaluation), and the stated date is not later than it.' It no longer says 'first recorded treatment' (`T-116-paralegal-r4-baseline.out.txt`, B1). It does not pick between the dates.
6. **pytest:** `.venv/bin/python -m pytest -q tests/unit -k gap -p no:cacheprovider` in the project tree: `270 passed, 2490 deselected in 4.88s`; same command inside the HEAD archive: `270 passed, 2414 deselected in 4.85s`. `research/validate_library.py` and `evals/golden/check_golden.py` print OK in the archive.
7. **Not done:** I did not drive the running app at localhost:7860 this round, so `scores.verify_quickly` is not scored (D-015 applies when the running app is reviewed).

## As a paralegal: is it clear what to do?

Yes for the warning cases. 'Check whether treatment continued' plus both numbers tells me to look at the record and pick the number I can defend. Two things slow me down:
the counted number leads the headline ('Gap of 43 days') even when the record's own text says the services were on 07/08 (F3); and when the warning is silently suppressed
(F1) I do not know there was anything to decide.

## Findings

**Blocker F1. The warning, the alternative and the conditional flag are switched off by a regex guess on the excerpt text (`gaps.admin_label`, `_has_treatment_evidence`, `_EVIDENCE`, `_DX`). A mid-span bill, EOB, records request, affidavit or intake questionnaire with a diagnosis line, 'performed' or 'seen by' hides a real 40-day span with no note.**
- Evidence: `artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.out.txt` (script `...-evidence-suppression.py`, same three-record packet as r3 W3: visit 3/01, paperwork 3/20, visit 4/10):
  - 'billing statement, Dx code line' ('Statement of account. Dx: M54.2 cervicalgia. CPT 97110 x4. Balance due $740.') MID-SPAN flags = NONE (40-day span hidden, no note); ENDS-GAP flags = [(40, False, [])] (no warning).
  - Same result for 'billing statement, Services performed', 'intake form, Have you been seen by a physician', 'records request, treatment performed', 'affidavit, services were performed', 'EOB, Diagnosis: M54.2'.
  - Controls without those words work: 'billing statement, plain' MID-SPAN = [(40, True, ['inside'])], ENDS-GAP = [(40, False, ['end'])].
  - Pre-T-116 (3e3f3b7) showed a 40-day flag for the billing statement, EOB and records-request cases (kind excluded); HEAD hides it. The same output block, PRE section.
  - Committed packet, one added sentence: `T-116-paralegal-r4-packet-dx-line.out.txt`: lib06 as committed gives the 35-day conditional flag (2026-05-13 to 2026-06-17, 'inside' warning on record 4); with 'Diagnosis: M25.511 pain in right shoulder.' appended to the record 4 billing statement excerpt, HEAD returns only the 56-day flag. The 35-day span is gone.
  - Root: `app/backend/gaps.py` `admin_label` (returns None when `_has_treatment_evidence`), used by `endpoint_warnings`, `_visit_dates`, `_alternative`, `_conditional_flags`; the same function feeds `conflicts.accident_date_conflicts` (`conflicts.py:63-66`). `tests/unit/test_t116_r4_all_dated_records.py:94-96` asserts `flags == []` for an 'intake form' with an exam excerpt, so the suppression is tested as intended behaviour, only for a clinical-note excerpt, not for bills or forms that carry diagnosis lines.
- Why it matters: D-055 says warn by header and show the alternative; 'a warning cannot invent a gap' is the reason a warning is cheap and an exclusion is not. Turning the warning off from a text guess is the same guess as the excluded label heuristic, one layer in. Bills and EOBs list diagnosis codes and 'services performed' as a matter of course, so this is the common case, not a corner. The adjuster will count 03/01 to 04/10 as 40 days with no visit; the tool shows nothing, and pre-T-116 it did. Persona section 3 ('surfaces what the adjuster will attack') and the r1 to r3 standard (a gap hidden by a guess is a blocker).
- Fix: decide whether a record looks like paperwork from the header (and its own first-line title) only, as D-055 reads. Text evidence may change the wording ('labelled intake form; its text shows exam findings') but must never remove the warning, the alternative number, or the conditional flag. If the team keeps a 'clinical note labelled as a form' exception, show it as a visible line on the flag ('record 2 is labelled intake form but its text shows exam findings, counted as a visit'), not silence.
- Acceptance test: re-run `T-116-paralegal-r4-evidence-suppression.py` on the new HEAD: all eight rows show MID-SPAN = [(40, True, ['inside'])] and ENDS-GAP = [(40, False, ['end'])]; `T-116-paralegal-r4-packet-dx-line.py` keeps the lib06 35-day conditional flag after the diagnosis sentence is added; add a unit test through `ingest.ingest` and `gaps.gap_flags` for a billing statement with a 'Dx:' line.

**Minor F2. Same root as F1 in the accident baseline: an intake form whose text contains 'seen by' is again called 'the first recorded treatment'.**
- Evidence: `T-116-paralegal-r4-baseline.out.txt`, B2: 'Stated accident date January 15, 2026 (...) is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form). The records disagree; the tool does not choose between them.' B1 (plain form) is correct.
- Why it matters: D-017 and R-FL-2 forbid stating a non-treatment record as the first recorded treatment. I rate it minor because it is the same fix as F1 (the wording is right for the plain form) and the blocker above carries the severity; it does not stand alone.
- Fix: covered by the F1 fix (header-only test). Add B2 as a unit test through `conflicts.accident_date_conflicts`.
- Acceptance test: `T-116-paralegal-r4-baseline.py` B2 prints the 'earliest recorded date ... looks like paperwork' sentence.

**Minor F3. The committed golden truth and the lexicon text still encode the exclusion the product dropped.** (Carried from r3 F3; now an open qa and researcher item, not a product defect.)
- Evidence: `T-116-paralegal-r4-compare.out.txt` section C: 'HEAD dates/days/flags vs committed expected files' differ for 9 packets; lib11 HEAD counts rows 14, 8, 1, 28, 35, 17 against the committed 14, 9, 28, 35 and `gap_excluded_records` [4, 9]; lib10 expected flag is 07-08 to 08-26 (49), the product flags 07-14 to 08-26 (43) with the 49 as the alternative. `app/llm/lexicon.yaml:1282` still reads 'records whose source label matches are excluded from gap arithmetic'. The backend card note says qa and researcher own both.
- Why it matters: the truth no longer describes what the product counts, so a future check can pass a wrong counted row. The visit-only reading is what the product shows as its alternative, so no flagged gap is lost today.
- Fix: qa keeps the visit-only table under a clear name and adds the counted rows the product test compares (or states in the golden README that gap_table is the visit-only reading); researcher updates the lexicon consumer text.
- Acceptance test: a unit test compares the product's counted rows to a committed counted table for all 25 packets; `rg 'excluded from gap arithmetic' app/llm/lexicon.yaml` returns nothing.

**Nit F4. When the paperwork's own text names the service date, the headline still leads with the counted number.** lib10: 'Gap of 43 days between July 14, 2026 (Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)) and August 26, 2026 ...' The claim's excerpt says 'dates of service 06/24/2026 and 07/08/2026', so the 49-day reading is the one the records support. D-055 forbids the tool from choosing, so I am not asking it to. A one-line pointer to the excerpt ('the record states services on 07/08/2026') would let me decide without opening the record. Optional.

## What is right

1. Every label that r1 to r3 called a visit now counts as a record: 60/60 runs with no invented 40-day gap, W4's hidden span shown, and the Appendix A 73-day flag intact in 10/10 variants.
2. The 'If record N: <header> is paperwork, not a visit, the gap would be X days (date to date)' sentence is exact, plural-aware, carries the verbatim header, and appears in explanation, why and endpoint_warnings (lib10 49/43, lib09 42/40, W3 40, case_09 56, lib06 35).
3. The accident baseline for a plain intake form names the paperwork record, gives the first-visit alternative, and does not choose a date.

## Outside my lens

Whether a record that is labelled 'intake form' but contains an exam should be counted as a visit is a clinical-reading call for the legal-nurse; I only ask that the tool say it made that call. The golden schema redesign (F3) is a qa and architect decision. Whether to disclose the gap in the demand is the litigation lead's.

## Questions for Chris

1. F1: do you want header-only detection for the warning (D-055 as written), or keep a text-evidence exception that is shown on the flag? Silence is the one option I cannot accept.

```json
{"card": "T-116", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 8b4ff11 (HEAD, T-116 r4, D-055) vs pre-T-116 parent 3e3f3b7; git archive copies in the scratchpad (t116r4/head, t116r4/pre); app/backend/gaps.py, conflicts.py, pipeline.py _accident_year, flag_templates.py, tests/unit/test_t116_r4_all_dated_records.py; 25 golden+library packets plus sample; the running app at localhost:7860 was not driven",
 "exercised": [
  "read personas/paralegal.md, reviews/T-116-paralegal-r3.md, memory t116-gap-endpoint-patterns, D-055 (memory/ORCHESTRATOR_DECISIONS.md:63), board show T-116, git log -6",
  "git archive 8b4ff11 and 3e3f3b7 into the scratchpad; artifacts/review-evidence/T-116-paralegal-r3-probe.py run unchanged on both trees: 27 visit labels + 3 controls x plain and headed excerpt in a three-visit packet through ingest.ingest and gaps.gap_flags (60 runs), Appendix A sample + 9 treatment records with ', fax', the 25 packets through the fixture pipeline, the constructed intake-form accident case",
  "artifacts/review-evidence/T-116-paralegal-r3-compare.py over the two outputs (T-116-paralegal-r4-compare.out.txt) and T-116-paralegal-r4-packet-flags.py (every pre-T-116 flagged row against HEAD flags and alternatives)",
  "artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.py on HEAD: W1 to W4 constructed packets and lib09 through the FastAPI TestClient with confirm_date on record 4 (T-116-paralegal-r4-warn-and-api.head.out.txt)",
  "new probes: T-116-paralegal-r4-evidence-suppression.py (8 paperwork excerpts mid-span and gap-ending, HEAD and pre-T-116), T-116-paralegal-r4-packet-dx-line.py (lib10 and lib06 with one diagnosis sentence), T-116-paralegal-r4-baseline.py (plain and 'seen by' intake form)",
  "read the lib10 packet text for record 8 (CMS-1500 dated 2026-07-14 with dates of service 06/24 and 07/08) and the HEAD gaps.py (244 lines), conflicts.py, pipeline.py:257-259, test_t116_r4_all_dated_records.py:94-96",
  ".venv/bin/python -m pytest -q tests/unit -k gap -p no:cacheprovider: 270 passed, 2490 deselected in 4.88s (project tree); 270 passed, 2414 deselected in 4.85s (HEAD archive); research/validate_library.py and evals/golden/check_golden.py OK on the archive"
 ],
 "verdict": "fail",
 "scores": {"no_invented_gap_by_label": 5, "paperwork_warning_text_and_both_numbers": 4, "no_hidden_span_when_paperwork_has_clinical_words": 1, "accident_baseline_wording": 4, "golden_truth_consistency": 3},
 "findings": [
  {"severity": "blocker",
   "title": "The paperwork warning, the alternative number and the conditional flag are switched off by a regex guess on the excerpt text; a bill, EOB, records request, affidavit or intake questionnaire with a diagnosis line, 'performed' or 'seen by' hides a real 40-day span with no note",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.out.txt: 'billing statement, Dx code line  MID-SPAN flags=NONE (40-day span hidden, no note) | ENDS-GAP flags=[(40, False, [])]'; same for 'Services performed', 'intake form, seen by', 'records request, treatment performed', 'affidavit, were performed', 'EOB, Diagnosis line'; controls 'billing statement, plain' MID-SPAN [(40, True, ['inside'])]; pre-T-116 showed [(40, False, [])] for the bill, EOB and records-request rows. artifacts/review-evidence/T-116-paralegal-r4-packet-dx-line.out.txt: lib06 committed gives ('2026-05-13','2026-06-17',35,True,['inside']); with 'Diagnosis: M25.511 pain in right shoulder.' appended to record 4 only the 56-day flag remains. app/backend/gaps.py admin_label / _has_treatment_evidence / _EVIDENCE / _DX; tests/unit/test_t116_r4_all_dated_records.py:94-96 asserts flags == [] for an intake form with an exam excerpt.",
   "why_it_matters": "D-055 (binding): warn by header and show the alternative, never decide by guessing. Suppressing the warning from a text regex is the same guess as the excluded label heuristic. Bills and EOBs routinely carry diagnosis codes and 'services performed', so the common real case is hidden, and pre-T-116 showed it. The adjuster will count the span; the tool shows nothing. Persona section 3 and the r1 to r3 standard: a gap hidden by a guess is a blocker.",
   "fix": "Detect paperwork from the header and the record's own first-line title only. Text evidence may change the wording but never remove the warning, the alternative or the conditional flag. If a 'clinical note labelled as a form' exception stays, print it on the flag as a visible line.",
   "acceptance_test": "Re-run T-116-paralegal-r4-evidence-suppression.py on the new HEAD: all eight rows give MID-SPAN [(40, True, ['inside'])] and ENDS-GAP [(40, False, ['end'])]; T-116-paralegal-r4-packet-dx-line.py keeps the lib06 35-day conditional flag; add a unit test through ingest.ingest and gaps.gap_flags for a billing statement with a 'Dx:' line."},
  {"severity": "minor",
   "title": "Same root in the accident baseline: an intake form whose text contains 'seen by' is again called 'the first recorded treatment'",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r4-baseline.out.txt B2: 'is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form)'; B1 (plain form) reads 'earliest recorded date ... looks like paperwork, not a visit'. app/backend/conflicts.py:63-66 uses gaps.admin_label.",
   "why_it_matters": "D-017 and R-FL-2: do not state a non-treatment record as the first recorded treatment. Rated minor because it is fixed by the F1 change and the wording is correct for a plain form.",
   "fix": "Covered by the header-only test in F1; add B2 as a unit test through conflicts.accident_date_conflicts.",
   "acceptance_test": "T-116-paralegal-r4-baseline.py B2 prints the 'earliest recorded date ... looks like paperwork' sentence."},
  {"severity": "minor",
   "title": "Committed golden truth and lexicon text still encode the exclusion the product dropped (carried from r3 F3; qa and researcher items)",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r4-compare.out.txt section C: 9 packets differ from the committed expected gap tables; lib11 HEAD rows 14, 8, 1, 28, 35, 17 vs committed 14, 9, 28, 35 with gap_excluded_records [4, 9]; lib10 expected flag 07-08 to 08-26 (49) vs product 07-14 to 08-26 (43) plus the 49 alternative. app/llm/lexicon.yaml:1282 'excluded from gap arithmetic'. Backend card note R4 names qa and researcher as owners.",
   "why_it_matters": "The truth no longer describes the counted rows, so a future check can pass a wrong counted row. The visit-only reading is what the product shows as its alternative, so no flagged gap is lost today.",
   "fix": "qa names the visit-only table as such and adds a counted table the product test compares (or documents it in the golden README); researcher updates the lexicon consumer text.",
   "acceptance_test": "A unit test compares the product's counted rows to a committed counted table for all 25 packets; rg 'excluded from gap arithmetic' app/llm/lexicon.yaml returns nothing."},
  {"severity": "nit",
   "title": "When the paperwork's own text names the service date, the headline still leads with the counted number",
   "evidence": "lib10 HEAD explanation: 'Gap of 43 days between July 14, 2026 (Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)) and August 26, 2026 ...' while record 8 reads 'dates of service 06/24/2026 and 07/08/2026'.",
   "why_it_matters": "I have to open record 8 to learn which number the records support. D-055 forbids choosing, so a pointer to the excerpt would be enough.",
   "fix": "Optional: add a one-line pointer to the paperwork's stated service dates beside the alternative.",
   "acceptance_test": "lib10 explanation names the 07/08/2026 service date from record 8."}
 ],
 "whats_right": [
  "Every r1 to r3 visit label now counts as a record: 60/60 runs with no invented 40-day gap, W4's span shown, Appendix A 73-day flag intact in 10/10 variants.",
  "The 'If record N: <header> is paperwork, not a visit, the gap would be X days (date to date)' sentence is exact and plural-aware, and appears in explanation, why and endpoint_warnings (lib10 49/43, lib09 42/40, W3 40, case_09 56, lib06 35).",
  "The accident baseline for a plain intake form names the paperwork record, gives the first-visit alternative, and does not choose between the dates."
 ],
 "questions_for_chris": [
  "F1: header-only detection for the paperwork warning (D-055 as written), or a text-evidence exception that is printed on the flag? Silence is the one option I cannot accept."
 ]}
```
