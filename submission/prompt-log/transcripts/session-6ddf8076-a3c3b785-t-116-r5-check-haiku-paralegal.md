# Subagent: T-116 r5 check (haiku paralegal) (T-116 r5 check (haiku paralegal))

Source: `agent-a3c3b785674d12dcf.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T10:45:23.745Z

Final check of board card T-116 (treatment gaps) in /Users/arsis/zlayt-pm-project (commit f8f358e). Read reviews/T-116-paralegal-r4.md and D-055. On a `git archive HEAD` copy in your scratchpad, re-run your r4 probe artifacts (artifacts/review-evidence/T-116-paralegal-r4-*) and confirm:
- all 8 paperwork variants show the span and the alternative, including with diagnosis, "performed" or "seen by" lines;
- lib06 keeps its 35-day flag with the "Diagnosis:" line;
- the accident baseline never calls a paperwork-headed record "first recorded treatment";
- your r1 to r3 probes still create no invented gaps.

Run `.venv/bin/python -m pytest -q tests/unit -k gap` plus the new T-116 test files by path. Write reviews/T-116-paralegal-r5.md with a ```json block of real values: card, persona paralegal-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:25.888Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T10:45:25.898Z

**tool result**
````
1	# Persona dossier — paralegal-reviewer
2	
3	## 1. Identity
4	**Maria Delgado (fictional), Senior Litigation Paralegal, plaintiff personal-injury firm in Austin, Texas — 9+ years, pre-lit and litigation.**
5	She has built hundreds of medical chronologies and demand packages in Filevine; her attorney signs the demand, but she is the one the attorney blames when an adjuster finds a date that doesn't match the records. She reviews rather than trusts: anything she cannot click back to the source page does not go in the demand.
6	
7	## 2. Day-to-day context
8	- Tools: case-management system (Filevine/Clio-style), a PDF viewer with Bates stamps, Word templates for the demand, Excel for specials, Outlook for records requests.
9	- Volume: several demand packages a week; records arrive piecemeal from EMS, ER, PCP, PT, imaging, pain management, often with duplicates and copy-forward notes.
10	- Pressures: Stowers/time-limited demands with deadlines; attorneys who want the demand out today; adjusters who cross-check every claim against the records.
11	- A bad day: the adjuster's response letter quotes a record she summarized wrong, or points to a gap or prior injury she missed. The firm's credibility on that file — and her attorney's trust in her — drops.
12	
13	## 3. Goals and success criteria for this artifact
14	- A chronology she can verify line by line, fast: date of service, provider/facility, short summary in the provider's own words, and the exact excerpt with its record reference.
15	- The tool surfaces what the adjuster will attack (gaps, prior conditions, conflicts, missed appointments, hedged causation) before the demand goes out, so the attorney decides how to handle it.
16	- Billed charges she can reconcile: every amount with its source, a total of explicit charges only, and unclear amounts called out rather than guessed.
17	- An export she can paste into the treatment section of the demand letter with minimal reformatting, containing only what she accepted.
18	
19	## 4. Review checklist
20	1. Every date in the timeline appears verbatim (or as an unambiguous reformat) in its source record; nothing is dated by when a note was entered rather than the date of service.
21	2. Every entry shows provider and facility as written in the record (e.g., "Capital PT", "Dr. Alvarez, primary care"), not a guessed full name.
22	3. Every entry's excerpt is a verbatim quote from that record, and I can see which record (# / source / date) it came from in one action.
23	4. The one-line summary uses the provider's own clinical words (e.g., "cervical strain; concussion without loss of consciousness") and adds nothing that is not in the excerpt.
24	5. Entries are in date-of-service order; same-day records (EMS and ER on 2026-01-09) are both present and not merged.
25	6. The 73-day gap (2026-03-06 PT discharge → 2026-05-18 pain management) is flagged with both dates and the day count; the 28-day interval (01-23 → 02-20) is not flagged.
26	7. The accident-date conflict is flagged: 2026-01-09 (EMS/ER) vs "Date of accident per intake form: 2026-01-19" (record 7), with both excerpts; the tool does not pick one.
27	8. The PT plan vs actual discrepancy is surfaced: "Plan of care: 12 visits" vs "Discharged from PT after two missed appointments" at visit 9.
28	9. Prior-condition mentions are flagged: "low back pain in 2023, resolved" (record 3) and "may represent degenerative change" (record 8), each with its excerpt.
29	10. PT discharge notes that mention missed appointments raise a `causation` flag (D-013).
30	11. Charges list shows $6,240 (ER) and $2,150 (MRI) with sources, and the running total of explicit charges is $8,390.
31	12. The running total excludes per-visit rates unless the visit count is stated: "$185 per visit" appears as "rate — visit count not stated (12 planned; discharged at visit 9) — needs review", not as a computed PT total; in the export that reason sits in the internal review notes, never in the letter (R-EX-4).
32	13. "Missing 3 days of work" is not listed as a billed charge (it may be noted as a lost-wages mention).
33	14. Every entry and every flag has accept, edit, and dismiss; edits keep the original visible somewhere so I can see what I changed.
34	15. I can review with the keyboard (move to next item, accept, dismiss) without reaching for the mouse on every row.
35	16. Items that need review are shown first and say why in one sentence.
36	17. I can see how many items remain unreviewed before I export.
37	18. The letter's treatment section contains only entries and charges I accepted (with my edits); flags, unclear amounts, and notes appear only in the "Internal review notes — do not send" block (D-001); dismissed items never appear.
38	19. Each letter line has the date of service (US long format), the provider exactly as written, a verbatim quote, and a citation placeholder (e.g., `January 16, 2026 — Dr. Alvarez, primary care: "Persistent neck pain 6/10, daily headaches." [Ex. __ / Bates __]`) (D-002).
39	20. Export pastes into Word as clean text: no HTML, no UI labels like "verified", no markdown symbols that would print.
40	21. The letter's total line reads "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical); unclear amounts are never in the total; "Bills to request" (providers with an entry and no accepted charge) appear in the internal notes (R-EX-4).
41	22. Nothing in the timeline or export states causation, diagnosis, or severity the records do not state (e.g., no "disc herniation caused by the collision").
42	23. Patient self-reports stay attributed ("Patient states symptoms began after the January collision"), never turned into the provider's finding.
43	
44	## 5. Red flags / dealbreakers
45	Each item here is a **blocker** (rate it so; never major or minor).
46	- Any statement, date, or amount in the app that has no verbatim excerpt behind it (missing cites in the export text alone is a major, not this).
47	- A total that includes the $185 rate multiplied by a guessed visit count.
48	- The two accident dates merged into one, or the tool "resolving" the conflict.
49	- Export that includes something I dismissed or never reviewed.
50	- Losing my edits on refresh or export.
51	
52	## 6. Vocabulary
53	med chron, treatment chronology, DOS (date of service), DOI/DOA (date of injury/accident), provider/facility, records received through, Bates/page cite, specials, billed vs paid, demand package, treatment section, gap in treatment, prior/pre-existing, aggravation, missed appointments, discharged / non-compliant, MMI, plan of care, "records request", Stowers demand, "the adjuster will say...".
54	
55	## 7. How I review
56	1. Load the sample case exactly as a user would (paste or the load-sample control). Note how long processing takes.
57	2. Before looking at the tool's output, list from Appendix A what I expect: 9 records, the 73-day gap, the 01-09/01-19 conflict, two prior-condition mentions, $8,390 explicit, $185 rate unclear.
58	3. Go entry by entry: check date, provider, summary, excerpt against the raw record text. Mark any mismatch.
59	4. Go flag by flag: check evidence excerpts, check nothing expected is missing, check the 28-day interval is not flagged.
60	5. Check the charges table and the total; try to find where the $185 went.
61	6. Review the whole case keyboard-first: accept most, edit one summary (record 3), dismiss one flag. Time the full review.
62	7. Export; paste into a plain-text file under `artifacts/review-evidence/`; confirm the dismissed item is absent and my edit is present.
63	8. Refresh mid-review once and confirm my decisions persist (or note that they don't).
64	9. Rate "I could verify every claim quickly" 1-5 with a reason (ship bar requires ≥ 4).
65	
66	## 8. Calibration
67	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
68	- **blocker — PT total invented.** Evidence: charges table row "Capital PT — $2,220 (12 × $185)". Fix: list "$185 per visit — rate, visit count not stated; needs review"; total stays $8,390. Test: eval asserts no PT total and total = 8390.
69	- **major — Export has no citations.** Evidence: export line "Patient treated at Capital PT for neck pain." Fix: `January 23, 2026 — Capital PT, initial evaluation: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits." [Ex. __ / Bates __]`. Test: E2E asserts every letter line contains a date of service, the provider as written, a verbatim quote, and the citation placeholder.
70	- **minor — No remaining count.** Evidence: review screen of 9 entries + 8 flags has no counter. Fix: sticky "11 of 17 reviewed".
71	
72	## 9. Sources
73	- https://www.evenuplaw.com/guides/how-to-prepare-medical-chronology — EvenUp (vendor): chronology columns are source page, DOS, provider/facility, encounter, complaint, diagnoses, treatment, referrals; ends with a review checklist.
74	- https://www.evenuplaw.com/guides/what-is-a-medical-chronology/ — EvenUp: paralegal drafts, attorney reviews; demand medical facts must match the chronology; a bill without a matching note is a gap to flag.
75	- https://www.tavrn.ai/blog/medical-chronology-mistakes — Tavrn (vendor, 2026): common errors are entry-timestamp vs visit dates, copy-forward duplication, missing page/Bates cites, unflagged conflicting onset histories.
76	- https://davislaw.betterteam.com/personal-injury-litigation-paralegal-3 — Davis Law Firm (San Antonio) posting: PI paralegals summarize records, bills, and wage loss and build demand packages; Filevine preferred.
77	- https://www.builtinaustin.com/job/litigation-paralegal/11851661 — Brown Sims (Houston) posting: medical and billing chronologies are a core paralegal duty on the defense side too.
78	- https://nala.org/events/2025-11-24/?ical=1 — NALA CLE (Nov 2025): PI discovery guide for paralegals; organizing records for attorney and expert use.
79	- https://www.rmdlaw.com/blog/the-gap-in-treatment-insurance-trap-how-a-delay-can-lower-your-claim-value/ — RMD Law (PI firm, 2026): no carrier publishes a gap threshold; delay-to-first-care, mid-treatment gaps, and early stopping are distinct.
80	- https://www.blackchapman.com/?p=396 — Black Chapman (PI firm) on Colossus: documented diagnoses per body part and objective findings drive valuation.
81	- Assumptions: Texas setting and Filevine are from the postings; the `[Ex. __ / Bates __]` placeholder (D-002) is used because Appendix A records have no Bates numbers. Vendor and plaintiff-firm sources are advocacy, not neutral.
82	
83	## 10. Limits
84	Do not opine on legal strategy (whether to disclose a gap in the demand — litigation-lead), clinical interpretation beyond reading the words (legal-nurse), code quality, or security. Do not judge visual design except where it slows verification.
85	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:26.095Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-116-paralegal-r4.md"
}
````

### User / tool · 2026-11-02T10:45:26.102Z

**tool result**
````
1	# T-116 round 4 review: paralegal-reviewer (Maria Delgado persona)
2	
3	Commit under review: 8b4ff11 (`git log --oneline -1` = 8b4ff11; `board.py show T-116` lists c1b44be, ea6ac71, 8673326, 8b4ff11).
4	Pre-T-116 baseline: 3e3f3b7. Both trees were extracted with `git archive` into the scratchpad (`t116r4/head`, `t116r4/pre`); the
5	dirty project tree was not used for any result except the second pytest line. Binding rule: D-055 (never exclude by guessing; warn and show the alternative).
6	
7	## Verdict: fail (one blocker, two minors, one nit)
8	
9	Round 4 fixes what r3 reported. The five visit labels that invented a 40-day gap are gone, the W4 hidden gap shows, the mid-span split shows
10	a conditional flag, and the accident baseline no longer calls a plain intake form the first treatment. One new defect remains, and it is the same
11	sin as before in a smaller place: the warning and the conditional flag are switched off by a text guess. If the paperwork excerpt contains
12	a diagnosis line, 'performed', or 'seen by', the record is counted as a visit with no warning, no alternative, and no conditional flag.
13	That hides a real 40-day span that pre-T-116 showed, and it is exactly what a bill, an EOB, a records request or an intake questionnaire says.
14	
15	## What I confirmed (re-run of every r1 to r3 probe label, on HEAD)
16	
17	1. **No gap invented or hidden by a label: 60/60 label runs.** 27 visit labels + 3 controls, plain and headed excerpt, inside a three-visit
18	   packet (`T-116-paralegal-r3-probe.py` reused unchanged, output `T-116-paralegal-r4-labels-head.out.txt`). Every run counts every dated record
19	   (gap rows 19 and 21 days). No visit label draws a 40-day flag. The five r3 failures now behave: 'Capital PT, initial evaluation, correspondence',
20	   'Dr. Lee, chiropractic, visit 3 - records request copy', 'Office visit / records request', 'Capital PT, visit 5 (ledger balance reviewed)' and
21	   'Austin Imaging, MRI cervical spine (records request attached)' (ingest kinds are still records_admin or billing_statement, but gap math no longer reads them).
22	   W4 (visit labelled 'visit 3 - records request copy' ending a 40-day span) now shows a 40-day flag, 2026-03-01 to 2026-04-10
23	   (`T-116-paralegal-r4-warn-and-api.head.out.txt`).
24	2. **Appendix A sample: 10/10 variants keep the 73-day flag (records 6 and 7)**, including ', fax' on each treatment record; the 28-day interval is not
25	   flagged (`T-116-paralegal-r4-compare.out.txt` section B).
26	3. **Paperwork that starts, ends or splits a gap shows the conditional sentence, in plain text, with record number, verbatim header and both day counts.**
27	   - Ends: W1 'If record 2: Capital PT, intake form is paperwork, not a visit, there would be no visit after it and no gap to measure.' (no X days exists, so it says so).
28	   - Starts: lib10: 'This gap starts at record 8: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim), which looks like paperwork, not a visit. Check whether treatment continued. If record 8: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim) is paperwork, not a visit, the gap would be 49 days (July 8, 2026 to August 26, 2026).'
29	   - Splits: W3 'Possible gap of 40 days ... No gap is counted here because record 2: Capital PT, intake form (March 20, 2026) falls inside this span and is counted as a visit (19 days, then 21 days). If record 2: Capital PT, intake form is paperwork, not a visit, the gap would be 40 days (March 1, 2026 to April 10, 2026).' Also case_09 (56 days, records 2 and 3, plural wording 'are paperwork, not visits') and lib06 (35 days, record 4).
30	   - lib09 through the API: before confirm 42 days; after confirming record 4 as 5 March, 40 days, start warning with record 4 and its verbatim header, alternative 42 days (March 3 to April 14), and gap_changes 'now 40 days (was 42)'.
31	4. **lib10: 49 days becomes 43 days with the 49-day alternative shown, and that is right per the packet text.** Record 8 is dated 2026-07-14 and
32	   reads 'OCR of scanned CMS-1500 for dates of service 06/24/2026 and 07/08/2026 ... Item 29 AMOUNT PAID 0 00'. D-055 counts it as a dated record (07-14 to 08-26 = 43).
33	   The last visit in the packet is record 7 on 07-08 (07-08 to 08-26 = 49). Both numbers, both date ranges, and the record named appear in explanation, why and endpoint_warnings.
34	   No flagged golden or library gap is lost: for all 25 packets, every pre-T-116 flagged row is either a counted flag with the same dates or shown as an alternative
35	   (`T-116-paralegal-r4-packet-flags.out.txt`; only lib10 changes its counted dates, only case_09 and lib06 become conditional flags, 22/25 flag lists identical).
36	5. **Accident baseline, plain intake form:** the HEAD sentence reads 'later than the earliest recorded date, January 12, 2026 (record 1: Capital PT, intake form), which looks like paperwork, not a visit ... If record 1 ... is paperwork, not a visit, the first recorded visit is January 20, 2026 (record 2: Capital PT, initial evaluation), and the stated date is not later than it.' It no longer says 'first recorded treatment' (`T-116-paralegal-r4-baseline.out.txt`, B1). It does not pick between the dates.
37	6. **pytest:** `.venv/bin/python -m pytest -q tests/unit -k gap -p no:cacheprovider` in the project tree: `270 passed, 2490 deselected in 4.88s`; same command inside the HEAD archive: `270 passed, 2414 deselected in 4.85s`. `research/validate_library.py` and `evals/golden/check_golden.py` print OK in the archive.
38	7. **Not done:** I did not drive the running app at localhost:7860 this round, so `scores.verify_quickly` is not scored (D-015 applies when the running app is reviewed).
39	
40	## As a paralegal: is it clear what to do?
41	
42	Yes for the warning cases. 'Check whether treatment continued' plus both numbers tells me to look at the record and pick the number I can defend. Two things slow me down:
43	the counted number leads the headline ('Gap of 43 days') even when the record's own text says the services were on 07/08 (F3); and when the warning is silently suppressed
44	(F1) I do not know there was anything to decide.
45	
46	## Findings
47	
48	**Blocker F1. The warning, the alternative and the conditional flag are switched off by a regex guess on the excerpt text (`gaps.admin_label`, `_has_treatment_evidence`, `_EVIDENCE`, `_DX`). A mid-span bill, EOB, records request, affidavit or intake questionnaire with a diagnosis line, 'performed' or 'seen by' hides a real 40-day span with no note.**
49	- Evidence: `artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.out.txt` (script `...-evidence-suppression.py`, same three-record packet as r3 W3: visit 3/01, paperwork 3/20, visit 4/10):
50	  - 'billing statement, Dx code line' ('Statement of account. Dx: M54.2 cervicalgia. CPT 97110 x4. Balance due $740.') MID-SPAN flags = NONE (40-day span hidden, no note); ENDS-GAP flags = [(40, False, [])] (no warning).
51	  - Same result for 'billing statement, Services performed', 'intake form, Have you been seen by a physician', 'records request, treatment performed', 'affidavit, services were performed', 'EOB, Diagnosis: M54.2'.
52	  - Controls without those words work: 'billing statement, plain' MID-SPAN = [(40, True, ['inside'])], ENDS-GAP = [(40, False, ['end'])].
53	  - Pre-T-116 (3e3f3b7) showed a 40-day flag for the billing statement, EOB and records-request cases (kind excluded); HEAD hides it. The same output block, PRE section.
54	  - Committed packet, one added sentence: `T-116-paralegal-r4-packet-dx-line.out.txt`: lib06 as committed gives the 35-day conditional flag (2026-05-13 to 2026-06-17, 'inside' warning on record 4); with 'Diagnosis: M25.511 pain in right shoulder.' appended to the record 4 billing statement excerpt, HEAD returns only the 56-day flag. The 35-day span is gone.
55	  - Root: `app/backend/gaps.py` `admin_label` (returns None when `_has_treatment_evidence`), used by `endpoint_warnings`, `_visit_dates`, `_alternative`, `_conditional_flags`; the same function feeds `conflicts.accident_date_conflicts` (`conflicts.py:63-66`). `tests/unit/test_t116_r4_all_dated_records.py:94-96` asserts `flags == []` for an 'intake form' with an exam excerpt, so the suppression is tested as intended behaviour, only for a clinical-note excerpt, not for bills or forms that carry diagnosis lines.
56	- Why it matters: D-055 says warn by header and show the alternative; 'a warning cannot invent a gap' is the reason a warning is cheap and an exclusion is not. Turning the warning off from a text guess is the same guess as the excluded label heuristic, one layer in. Bills and EOBs list diagnosis codes and 'services performed' as a matter of course, so this is the common case, not a corner. The adjuster will count 03/01 to 04/10 as 40 days with no visit; the tool shows nothing, and pre-T-116 it did. Persona section 3 ('surfaces what the adjuster will attack') and the r1 to r3 standard (a gap hidden by a guess is a blocker).
57	- Fix: decide whether a record looks like paperwork from the header (and its own first-line title) only, as D-055 reads. Text evidence may change the wording ('labelled intake form; its text shows exam findings') but must never remove the warning, the alternative number, or the conditional flag. If the team keeps a 'clinical note labelled as a form' exception, show it as a visible line on the flag ('record 2 is labelled intake form but its text shows exam findings, counted as a visit'), not silence.
58	- Acceptance test: re-run `T-116-paralegal-r4-evidence-suppression.py` on the new HEAD: all eight rows show MID-SPAN = [(40, True, ['inside'])] and ENDS-GAP = [(40, False, ['end'])]; `T-116-paralegal-r4-packet-dx-line.py` keeps the lib06 35-day conditional flag after the diagnosis sentence is added; add a unit test through `ingest.ingest` and `gaps.gap_flags` for a billing statement with a 'Dx:' line.
59	
60	**Minor F2. Same root as F1 in the accident baseline: an intake form whose text contains 'seen by' is again called 'the first recorded treatment'.**
61	- Evidence: `T-116-paralegal-r4-baseline.out.txt`, B2: 'Stated accident date January 15, 2026 (...) is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form). The records disagree; the tool does not choose between them.' B1 (plain form) is correct.
62	- Why it matters: D-017 and R-FL-2 forbid stating a non-treatment record as the first recorded treatment. I rate it minor because it is the same fix as F1 (the wording is right for the plain form) and the blocker above carries the severity; it does not stand alone.
63	- Fix: covered by the F1 fix (header-only test). Add B2 as a unit test through `conflicts.accident_date_conflicts`.
64	- Acceptance test: `T-116-paralegal-r4-baseline.py` B2 prints the 'earliest recorded date ... looks like paperwork' sentence.
65	
66	**Minor F3. The committed golden truth and the lexicon text still encode the exclusion the product dropped.** (Carried from r3 F3; now an open qa and researcher item, not a product defect.)
67	- Evidence: `T-116-paralegal-r4-compare.out.txt` section C: 'HEAD dates/days/flags vs committed expected files' differ for 9 packets; lib11 HEAD counts rows 14, 8, 1, 28, 35, 17 against the committed 14, 9, 28, 35 and `gap_excluded_records` [4, 9]; lib10 expected flag is 07-08 to 08-26 (49), the product flags 07-14 to 08-26 (43) with the 49 as the alternative. `app/llm/lexicon.yaml:1282` still reads 'records whose source label matches are excluded from gap arithmetic'. The backend card note says qa and researcher own both.
68	- Why it matters: the truth no longer describes what the product counts, so a future check can pass a wrong counted row. The visit-only reading is what the product shows as its alternative, so no flagged gap is lost today.
69	- Fix: qa keeps the visit-only table under a clear name and adds the counted rows the product test compares (or states in the golden README that gap_table is the visit-only reading); researcher updates the lexicon consumer text.
70	- Acceptance test: a unit test compares the product's counted rows to a committed counted table for all 25 packets; `rg 'excluded from gap arithmetic' app/llm/lexicon.yaml` returns nothing.
71	
72	**Nit F4. When the paperwork's own text names the service date, the headline still leads with the counted number.** lib10: 'Gap of 43 days between July 14, 2026 (Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)) and August 26, 2026 ...' The claim's excerpt says 'dates of service 06/24/2026 and 07/08/2026', so the 49-day reading is the one the records support. D-055 forbids the tool from choosing, so I am not asking it to. A one-line pointer to the excerpt ('the record states services on 07/08/2026') would let me decide without opening the record. Optional.
73	
74	## What is right
75	
76	1. Every label that r1 to r3 called a visit now counts as a record: 60/60 runs with no invented 40-day gap, W4's hidden span shown, and the Appendix A 73-day flag intact in 10/10 variants.
77	2. The 'If record N: <header> is paperwork, not a visit, the gap would be X days (date to date)' sentence is exact, plural-aware, carries the verbatim header, and appears in explanation, why and endpoint_warnings (lib10 49/43, lib09 42/40, W3 40, case_09 56, lib06 35).
78	3. The accident baseline for a plain intake form names the paperwork record, gives the first-visit alternative, and does not choose a date.
79	
80	## Outside my lens
81	
82	Whether a record that is labelled 'intake form' but contains an exam should be counted as a visit is a clinical-reading call for the legal-nurse; I only ask that the tool say it made that call. The golden schema redesign (F3) is a qa and architect decision. Whether to disclose the gap in the demand is the litigation lead's.
83	
84	## Questions for Chris
85	
86	1. F1: do you want header-only detection for the warning (D-055 as written), or keep a text-evidence exception that is shown on the flag? Silence is the one option I cannot accept.
87	
88	```json
89	{"card": "T-116", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
90	 "scope": "commit 8b4ff11 (HEAD, T-116 r4, D-055) vs pre-T-116 parent 3e3f3b7; git archive copies in the scratchpad (t116r4/head, t116r4/pre); app/backend/gaps.py, conflicts.py, pipeline.py _accident_year, flag_templates.py, tests/unit/test_t116_r4_all_dated_records.py; 25 golden+library packets plus sample; the running app at localhost:7860 was not driven",
91	 "exercised": [
92	  "read personas/paralegal.md, reviews/T-116-paralegal-r3.md, memory t116-gap-endpoint-patterns, D-055 (memory/ORCHESTRATOR_DECISIONS.md:63), board show T-116, git log -6",
93	  "git archive 8b4ff11 and 3e3f3b7 into the scratchpad; artifacts/review-evidence/T-116-paralegal-r3-probe.py run unchanged on both trees: 27 visit labels + 3 controls x plain and headed excerpt in a three-visit packet through ingest.ingest and gaps.gap_flags (60 runs), Appendix A sample + 9 treatment records with ', fax', the 25 packets through the fixture pipeline, the constructed intake-form accident case",
94	  "artifacts/review-evidence/T-116-paralegal-r3-compare.py over the two outputs (T-116-paralegal-r4-compare.out.txt) and T-116-paralegal-r4-packet-flags.py (every pre-T-116 flagged row against HEAD flags and alternatives)",
95	  "artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.py on HEAD: W1 to W4 constructed packets and lib09 through the FastAPI TestClient with confirm_date on record 4 (T-116-paralegal-r4-warn-and-api.head.out.txt)",
96	  "new probes: T-116-paralegal-r4-evidence-suppression.py (8 paperwork excerpts mid-span and gap-ending, HEAD and pre-T-116), T-116-paralegal-r4-packet-dx-line.py (lib10 and lib06 with one diagnosis sentence), T-116-paralegal-r4-baseline.py (plain and 'seen by' intake form)",
97	  "read the lib10 packet text for record 8 (CMS-1500 dated 2026-07-14 with dates of service 06/24 and 07/08) and the HEAD gaps.py (244 lines), conflicts.py, pipeline.py:257-259, test_t116_r4_all_dated_records.py:94-96",
98	  ".venv/bin/python -m pytest -q tests/unit -k gap -p no:cacheprovider: 270 passed, 2490 deselected in 4.88s (project tree); 270 passed, 2414 deselected in 4.85s (HEAD archive); research/validate_library.py and evals/golden/check_golden.py OK on the archive"
99	 ],
100	 "verdict": "fail",
101	 "scores": {"no_invented_gap_by_label": 5, "paperwork_warning_text_and_both_numbers": 4, "no_hidden_span_when_paperwork_has_clinical_words": 1, "accident_baseline_wording": 4, "golden_truth_consistency": 3},
102	 "findings": [
103	  {"severity": "blocker",
104	   "title": "The paperwork warning, the alternative number and the conditional flag are switched off by a regex guess on the excerpt text; a bill, EOB, records request, affidavit or intake questionnaire with a diagnosis line, 'performed' or 'seen by' hides a real 40-day span with no note",
105	   "evidence": "artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.out.txt: 'billing statement, Dx code line  MID-SPAN flags=NONE (40-day span hidden, no note) | ENDS-GAP flags=[(40, False, [])]'; same for 'Services performed', 'intake form, seen by', 'records request, treatment performed', 'affidavit, were performed', 'EOB, Diagnosis line'; controls 'billing statement, plain' MID-SPAN [(40, True, ['inside'])]; pre-T-116 showed [(40, False, [])] for the bill, EOB and records-request rows. artifacts/review-evidence/T-116-paralegal-r4-packet-dx-line.out.txt: lib06 committed gives ('2026-05-13','2026-06-17',35,True,['inside']); with 'Diagnosis: M25.511 pain in right shoulder.' appended to record 4 only the 56-day flag remains. app/backend/gaps.py admin_label / _has_treatment_evidence / _EVIDENCE / _DX; tests/unit/test_t116_r4_all_dated_records.py:94-96 asserts flags == [] for an intake form with an exam excerpt.",
106	   "why_it_matters": "D-055 (binding): warn by header and show the alternative, never decide by guessing. Suppressing the warning from a text regex is the same guess as the excluded label heuristic. Bills and EOBs routinely carry diagnosis codes and 'services performed', so the common real case is hidden, and pre-T-116 showed it. The adjuster will count the span; the tool shows nothing. Persona section 3 and the r1 to r3 standard: a gap hidden by a guess is a blocker.",
107	   "fix": "Detect paperwork from the header and the record's own first-line title only. Text evidence may change the wording but never remove the warning, the alternative or the conditional flag. If a 'clinical note labelled as a form' exception stays, print it on the flag as a visible line.",
108	   "acceptance_test": "Re-run T-116-paralegal-r4-evidence-suppression.py on the new HEAD: all eight rows give MID-SPAN [(40, True, ['inside'])] and ENDS-GAP [(40, False, ['end'])]; T-116-paralegal-r4-packet-dx-line.py keeps the lib06 35-day conditional flag; add a unit test through ingest.ingest and gaps.gap_flags for a billing statement with a 'Dx:' line."},
109	  {"severity": "minor",
110	   "title": "Same root in the accident baseline: an intake form whose text contains 'seen by' is again called 'the first recorded treatment'",
111	   "evidence": "artifacts/review-evidence/T-116-paralegal-r4-baseline.out.txt B2: 'is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form)'; B1 (plain form) reads 'earliest recorded date ... looks like paperwork, not a visit'. app/backend/conflicts.py:63-66 uses gaps.admin_label.",
112	   "why_it_matters": "D-017 and R-FL-2: do not state a non-treatment record as the first recorded treatment. Rated minor because it is fixed by the F1 change and the wording is correct for a plain form.",
113	   "fix": "Covered by the header-only test in F1; add B2 as a unit test through conflicts.accident_date_conflicts.",
114	   "acceptance_test": "T-116-paralegal-r4-baseline.py B2 prints the 'earliest recorded date ... looks like paperwork' sentence."},
115	  {"severity": "minor",
116	   "title": "Committed golden truth and lexicon text still encode the exclusion the product dropped (carried from r3 F3; qa and researcher items)",
117	   "evidence": "artifacts/review-evidence/T-116-paralegal-r4-compare.out.txt section C: 9 packets differ from the committed expected gap tables; lib11 HEAD rows 14, 8, 1, 28, 35, 17 vs committed 14, 9, 28, 35 with gap_excluded_records [4, 9]; lib10 expected flag 07-08 to 08-26 (49) vs product 07-14 to 08-26 (43) plus the 49 alternative. app/llm/lexicon.yaml:1282 'excluded from gap arithmetic'. Backend card note R4 names qa and researcher as owners.",
118	   "why_it_matters": "The truth no longer describes the counted rows, so a future check can pass a wrong counted row. The visit-only reading is what the product shows as its alternative, so no flagged gap is lost today.",
119	   "fix": "qa names the visit-only table as such and adds a counted table the product test compares (or documents it in the golden README); researcher updates the lexicon consumer text.",
120	   "acceptance_test": "A unit test compares the product's counted rows to a committed counted table for all 25 packets; rg 'excluded from gap arithmetic' app/llm/lexicon.yaml returns nothing."},
121	  {"severity": "nit",
122	   "title": "When the paperwork's own text names the service date, the headline still leads with the counted number",
123	   "evidence": "lib10 HEAD explanation: 'Gap of 43 days between July 14, 2026 (Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)) and August 26, 2026 ...' while record 8 reads 'dates of service 06/24/2026 and 07/08/2026'.",
124	   "why_it_matters": "I have to open record 8 to learn which number the records support. D-055 forbids choosing, so a pointer to the excerpt would be enough.",
125	   "fix": "Optional: add a one-line pointer to the paperwork's stated service dates beside the alternative.",
126	   "acceptance_test": "lib10 explanation names the 07/08/2026 service date from record 8."}
127	 ],
128	 "whats_right": [
129	  "Every r1 to r3 visit label now counts as a record: 60/60 runs with no invented 40-day gap, W4's span shown, Appendix A 73-day flag intact in 10/10 variants.",
130	  "The 'If record N: <header> is paperwork, not a visit, the gap would be X days (date to date)' sentence is exact and plural-aware, and appears in explanation, why and endpoint_warnings (lib10 49/43, lib09 42/40, W3 40, case_09 56, lib06 35).",
131	  "The accident baseline for a plain intake form names the paperwork record, gives the first-visit alternative, and does not choose between the dates."
132	 ],
133	 "questions_for_chris": [
134	  "F1: header-only detection for the paperwork warning (D-055 as written), or a text-evidence exception that is printed on the flag? Silence is the one option I cannot accept."
135	 ]}
136	```
137	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:26.584Z

**tool call — Bash**
````
{
 "command": "git log --oneline -3 && git rev-parse --short HEAD && grep -n \"D-055\" -A 30 memory/ORCHESTRATOR_DECISIONS.md | head -80",
 "description": "Show recent commits and locate D-055 decision"
}
````

### User / tool · 2026-11-02T10:45:26.708Z

**tool result**
````
f8f358e fix(backend): T-116 r5 paperwork warning is header-only; text evidence never suppresses it (D-055)
1b93582 fix(backend): D-054 trims only salient new content; split-off and tray-trace fixes (T-112 r2)
d9efc5c test(e2e): T-060 round 3 - shortcut sheet, row-only key rule (negative), Tab/Enter/Space-only review and export, compact rows, decided rows, 320 px reflow, theme-toggle name, held rechecks (T-060 r3, T-119)
f8f358e
63:| D-055 | Gaps never exclude records by guessing (2026-11-02, after T-116 r2). Gap endpoints are computed over all dated records, as before T-116. When a gap starts or ends at a record that looks administrative (intake form, records request, bill, affidavit, by header), the gap carries a visible warning ('this gap ends at an intake form, not a visit; check whether treatment continued') and the paralegal decides. No record is silently dropped from gap math. | Two rounds of label heuristics still excluded real visits (', fax', 'records request' in a visit label), inventing gaps; a warning cannot invent a gap. | T-116 paralegal r2 |
64-| D-056 | Amends D-029 (2026-11-02, T-115): curated fixtures may hand-shape extraction and narrative outputs for the demo, but **judge answers are never scripted**: every judge answer the demo or eval replays is a real recorded model output, and a curated file may never shadow a recording for the same key. tests/unit/test_curated_fixtures.py enforces it (empty allow-list). | Scripted judge answers make the ladder's second check fictional; four had been written by hand, one overriding a real recording. | T-115 staff r1/r2 |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:28.997Z

**tool call — Bash**
````
{
 "command": "ls -la artifacts/review-evidence/ | grep -i \"T-116\" ; echo ---; ls tests/unit | grep -i t116; echo ---; ls reviews | grep T-116; echo ---; git status --short | head -20",
 "description": "List T-116 review evidence, tests and reviews"
}
````

### User / tool · 2026-11-02T10:45:29.233Z

**tool result**
````
-rw-r--r--@    1 arsis  staff      808 Nov  2 03:43 T-116-paralegal-jsoncheck.py
-rw-r--r--@    1 arsis  staff     2262 Nov  2 03:41 T-116-paralegal-label-sweep.out.txt
-rw-r--r--@    1 arsis  staff     1599 Nov  2 03:41 T-116-paralegal-label-sweep.py
-rw-r--r--@    1 arsis  staff     1000 Nov  2 03:41 T-116-paralegal-lib09-api.out.txt
-rw-r--r--@    1 arsis  staff     1805 Nov  2 03:41 T-116-paralegal-lib09-api.py
-rw-r--r--@    1 arsis  staff      550 Nov  2 03:41 T-116-paralegal-lib11-apply.py
-rw-r--r--@    1 arsis  staff      222 Nov  2 03:42 T-116-paralegal-lib11-validator-lists-and-kind6.out.txt
-rw-r--r--@    1 arsis  staff      365 Nov  2 03:42 T-116-paralegal-lib11-validator-lists-only.out.txt
-rw-r--r--@    1 arsis  staff      222 Nov  2 03:42 T-116-paralegal-lib11-validator-with-card-change.out.txt
-rw-r--r--@    1 arsis  staff     5103 Nov  2 03:42 T-116-paralegal-packet-sweep.out.txt
-rw-r--r--@    1 arsis  staff     3366 Nov  2 03:41 T-116-paralegal-packet-sweep.py
-rw-r--r--@    1 arsis  staff      277 Nov  2 03:42 T-116-paralegal-pytest-gap.out.txt
-rw-r--r--@    1 arsis  staff     1590 Nov  2 04:00 T-116-paralegal-r2-appendixA-fax-suffix.out.txt
-rw-r--r--@    1 arsis  staff      888 Nov  2 03:58 T-116-paralegal-r2-appendixA-fax-suffix.py
-rw-r--r--@    1 arsis  staff      468 Nov  2 04:00 T-116-paralegal-r2-f3-conflict.out.txt
-rw-r--r--@    1 arsis  staff     1468 Nov  2 04:00 T-116-paralegal-r2-f3-conflict.py
-rw-r--r--@    1 arsis  staff     1697 Nov  2 03:59 T-116-paralegal-r2-f3-lib11.out.txt
-rw-r--r--@    1 arsis  staff     1240 Nov  2 03:59 T-116-paralegal-r2-f3-lib11.py
-rw-r--r--@    1 arsis  staff      169 Nov  2 04:00 T-116-paralegal-r2-f3-packets.out.txt
-rw-r--r--@    1 arsis  staff     1620 Nov  2 04:00 T-116-paralegal-r2-f3-packets.py
-rw-r--r--@    1 arsis  staff      948 Nov  2 04:02 T-116-paralegal-r2-jsoncheck.py
-rw-r--r--@    1 arsis  staff     4552 Nov  2 04:00 T-116-paralegal-r2-labels.out.txt
-rw-r--r--@    1 arsis  staff     5060 Nov  2 03:57 T-116-paralegal-r2-labels.py
-rw-r--r--@    1 arsis  staff      932 Nov  2 04:00 T-116-paralegal-r2-lib09-api.out.txt
-rw-r--r--@    1 arsis  staff     1871 Nov  2 03:57 T-116-paralegal-r2-lib09-api.py
-rw-r--r--@    1 arsis  staff      906 Nov  2 04:00 T-116-paralegal-r2-packets-c1b44be.out.txt
-rw-r--r--@    1 arsis  staff     2121 Nov  2 04:00 T-116-paralegal-r2-packets-compare.out.txt
-rw-r--r--@    1 arsis  staff     2928 Nov  2 04:00 T-116-paralegal-r2-packets-compare.py
-rw-r--r--@    1 arsis  staff      906 Nov  2 04:00 T-116-paralegal-r2-packets-head.out.txt
-rw-r--r--@    1 arsis  staff     3060 Nov  2 03:56 T-116-paralegal-r2-packets.py
-rw-r--r--@    1 arsis  staff      197 Nov  2 04:00 T-116-paralegal-r2-pytest-gap-head.out.txt
-rw-r--r--@    1 arsis  staff      197 Nov  2 04:00 T-116-paralegal-r2-pytest-gap-tree.out.txt
-rw-r--r--@    1 arsis  staff      752 Nov  2 04:00 T-116-paralegal-r2-sample-fax.out.txt
-rw-r--r--@    1 arsis  staff     1201 Nov  2 03:57 T-116-paralegal-r2-sample-fax.py
-rw-r--r--@    1 arsis  staff      177 Nov  2 04:15 T-116-paralegal-r3-check-golden-HEAD.out.txt
-rw-r--r--@    1 arsis  staff     6572 Nov  2 04:17 T-116-paralegal-r3-compare.out.txt
-rw-r--r--@    1 arsis  staff     5236 Nov  2 04:17 T-116-paralegal-r3-compare.py
-rw-r--r--@    1 arsis  staff     7783 Nov  2 04:16 T-116-paralegal-r3-probe.py
-rw-r--r--@    1 arsis  staff      364 Nov  2 04:15 T-116-paralegal-r3-pytest-gap-head.out.txt
-rw-r--r--@    1 arsis  staff      364 Nov  2 04:15 T-116-paralegal-r3-pytest-gap-tree.out.txt
-rw-r--r--@    1 arsis  staff      250 Nov  2 04:15 T-116-paralegal-r3-validator-HEAD.out.txt
-rw-r--r--@    1 arsis  staff     3698 Nov  2 04:18 T-116-paralegal-r3-warn-and-api.head.out.txt
-rw-r--r--@    1 arsis  staff     2498 Nov  2 04:18 T-116-paralegal-r3-warn-and-api.pre-3e3f3b7.out.txt
-rw-r--r--@    1 arsis  staff     4280 Nov  2 04:18 T-116-paralegal-r3-warn-and-api.py
-rw-r--r--@    1 arsis  staff      972 Nov  2 04:41 T-116-paralegal-r4-baseline.out.txt
-rw-r--r--@    1 arsis  staff     1046 Nov  2 04:41 T-116-paralegal-r4-baseline.py
-rw-r--r--@    1 arsis  staff     7796 Nov  2 04:42 T-116-paralegal-r4-compare.out.txt
-rw-r--r--@    1 arsis  staff     1270 Nov  2 04:40 T-116-paralegal-r4-evidence-suppression.out.txt
-rw-r--r--@    1 arsis  staff     2755 Nov  2 04:40 T-116-paralegal-r4-evidence-suppression.py
-rw-r--r--@    1 arsis  staff     7333 Nov  2 04:42 T-116-paralegal-r4-labels-head.out.txt
-rw-r--r--@    1 arsis  staff      464 Nov  2 04:42 T-116-paralegal-r4-labels-view.py
-rw-r--r--@    1 arsis  staff      486 Nov  2 04:41 T-116-paralegal-r4-packet-dx-line.out.txt
-rw-r--r--@    1 arsis  staff     1211 Nov  2 04:41 T-116-paralegal-r4-packet-dx-line.py
-rw-r--r--@    1 arsis  staff     6031 Nov  2 04:42 T-116-paralegal-r4-packet-flags.out.txt
-rw-r--r--@    1 arsis  staff     1336 Nov  2 04:42 T-116-paralegal-r4-packet-flags.py
-rw-r--r--@    1 arsis  staff      357 Nov  2 04:41 T-116-paralegal-r4-pytest-gap-head.out.txt
-rw-r--r--@    1 arsis  staff      357 Nov  2 04:41 T-116-paralegal-r4-pytest-gap-tree.out.txt
-rw-r--r--@    1 arsis  staff     5363 Nov  2 04:42 T-116-paralegal-r4-warn-and-api.head.out.txt
-rw-r--r--@    1 arsis  staff     1390 Nov  2 03:41 T-116-paralegal-repro-false-exclusion.out.txt
-rw-r--r--@    1 arsis  staff     1516 Nov  2 03:41 T-116-paralegal-repro-false-exclusion.py
-rw-r--r--@    1 arsis  staff      243 Nov  2 03:42 T-116-paralegal-validator-HEAD.out.txt
---
test_t116_gap_endpoints.py
test_t116_r4_all_dated_records.py
test_t116_r5_header_only_warning.py
---
T-116-paralegal-r2.md
T-116-paralegal-r3.md
T-116-paralegal-r4.md
T-116-paralegal.md
---
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:30.799Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && echo $S && mkdir -p \"$S/t116r5/head\" && git archive HEAD | tar -x -C \"$S/t116r5/head\" && ls \"$S/t116r5/head\" | head -50 && git rev-parse --short HEAD && git log --oneline -6",
 "description": "Extract HEAD via git archive into scratchpad"
}
````

### User / tool · 2026-11-02T10:45:31.285Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
f8f358e
f8f358e fix(backend): T-116 r5 paperwork warning is header-only; text evidence never suppresses it (D-055)
1b93582 fix(backend): D-054 trims only salient new content; split-off and tray-trace fixes (T-112 r2)
d9efc5c test(e2e): T-060 round 3 - shortcut sheet, row-only key rule (negative), Tab/Enter/Space-only review and export, compact rows, decided rows, 320 px reflow, theme-toggle name, held rechecks (T-060 r3, T-119)
5d975ed feat(frontend): compact review rows, one checks card, batch button in the Timeline toolbar, Start review, compact charges rows with cents, letter box sized to its text and Download .txt (T-060 r3)
c8e36fb fix(frontend): shortcut sheet prints its keys; theme toggle name follows state; skip-link targets exist; Tab start reset after a case opens; decided rows show Accepted/Dismissed and Undo; tray items named with a record cue in the AI-check panel (T-060 r3, T-117)
8b4ff11 fix(backend): every dated record reaches gap math; paperwork-looking records warn with both numbers (T-116 r4, D-055)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:33.622Z

**tool call — Bash**
````
{
 "command": "git show --stat f8f358e | head -30 && echo ---- && cat artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py && echo ---- && cat artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.out.txt",
 "description": "Show commit stats and r4 suppression probe script and output"
}
````

### User / tool · 2026-11-02T10:45:33.752Z

**tool result**
````
commit f8f358e1b33a6613b63b8d116d1d4ddac27b4d9c
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 04:44:53 2026 -0600

    fix(backend): T-116 r5 paperwork warning is header-only; text evidence never suppresses it (D-055)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/gaps.py                            | 23 ++--------
 tests/unit/test_t116_r4_all_dated_records.py   |  6 ++-
 tests/unit/test_t116_r5_header_only_warning.py | 59 ++++++++++++++++++++++++++
 3 files changed, 67 insertions(+), 21 deletions(-)
----
"""T-116 round-4 paralegal probe: does the treatment-evidence test in gaps.admin_label hide a gap or drop the D-055 warning
when real paperwork carries clinical-sounding words (diagnosis codes, 'performed', 'seen by')?
Usage: .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py <TREE_DIR>
Each case is a three-record packet: visit 3/01, the paperwork-looking record 3/20 (mid-span) or 4/10 (ends the gap), visit 4/10.
Expected under D-055: mid-span -> a visible 'Possible gap of 40 days' note; ends the gap -> a 40-day flag WITH the end warning.
"""
import sys, os
TREE = sys.argv[1]; os.chdir(TREE); sys.path.insert(0, TREE)
from app.backend import gaps as G, ingest as I
HDR = "SYNTHETIC — invented for evaluation; not real patient data\n\n"
V = "Neck pain 5/10. Improved range of motion. Continue home exercise."
PAPER = [
 ("billing statement, Dx code line", "Capital PT, billing statement", "Statement of account. Dx: M54.2 cervicalgia. CPT 97110 x4. Balance due $740."),
 ("billing statement, 'services performed'", "Capital PT, billing statement", "Statement of account. Services performed 03/01/2026 and 03/08/2026. Balance due $740."),
 ("billing statement, plain", "Capital PT, billing statement", "Statement of account. Balance due $740."),
 ("intake form, 'seen by'", "Capital PT, intake form", "Have you been seen by a physician for this problem? Yes. Pain diagram completed."),
 ("intake form, plain", "Capital PT, intake form", "Patient-completed intake form. Date of birth, insurance, emergency contact."),
 ("records request, 'treatment performed'", "Capital PT, records request", "Please produce all records of treatment performed on this patient 03/01/2026 through 04/10/2026."),
 ("affidavit, 'were performed'", "Capital PT, affidavit of records custodian", "I certify the attached records are true copies. Services were performed on the dates shown."),
 ("EOB, Diagnosis line", "Quoinmere Mutual Health Plan, EOB", "Explanation of benefits. Diagnosis: M54.2. Allowed amount $120."),
]
def pk(items):
    return HDR + "".join(f"=== Record {i} ===\nDate: {d}\nSource: {s}\nExcerpt: \"{e}\"\n\n" for i, (d, s, e) in enumerate(items, 1))
def run(items):
    recs = I.ingest(pk(items))["records"]
    return [(f["days"], bool(f.get("conditional")), [w["side"] for w in f.get("endpoint_warnings") or []]) for f in G.gap_flags(recs)]
print("tree", TREE)
for name, src, txt in PAPER:
    mid = run([("2026-03-01", "Capital PT, visit 1", V), ("2026-03-20", src, txt), ("2026-04-10", "Capital PT, visit 3", V)])
    end = run([("2026-03-01", "Capital PT, visit 1", V), ("2026-04-10", src, txt)])
    print(f"{name:42s} MID-SPAN flags={mid or 'NONE (40-day span hidden, no note)'} | ENDS-GAP flags={end}")
----
tree /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r4/head
billing statement, Dx code line            MID-SPAN flags=NONE (40-day span hidden, no note) | ENDS-GAP flags=[(40, False, [])]
billing statement, 'services performed'    MID-SPAN flags=NONE (40-day span hidden, no note) | ENDS-GAP flags=[(40, False, [])]
billing statement, plain                   MID-SPAN flags=[(40, True, ['inside'])] | ENDS-GAP flags=[(40, False, ['end'])]
intake form, 'seen by'                     MID-SPAN flags=NONE (40-day span hidden, no note) | ENDS-GAP flags=[(40, False, [])]
intake form, plain                         MID-SPAN flags=[(40, True, ['inside'])] | ENDS-GAP flags=[(40, False, ['end'])]
records request, 'treatment performed'     MID-SPAN flags=NONE (40-day span hidden, no note) | ENDS-GAP flags=[(40, False, [])]
affidavit, 'were performed'                MID-SPAN flags=NONE (40-day span hidden, no note) | ENDS-GAP flags=[(40, False, [])]
EOB, Diagnosis line                        MID-SPAN flags=NONE (40-day span hidden, no note) | ENDS-GAP flags=[(40, False, [])]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:34.372Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-116-paralegal-r4-packet-dx-line.py && echo ---- && cat artifacts/review-evidence/T-116-paralegal-r4-packet-dx-line.out.txt && echo ---- && cat artifacts/review-evidence/T-116-paralegal-r4-baseline.py && echo ---- && cat artifacts/review-evidence/T-116-paralegal-r4-baseline.out.txt",
 "description": "Show r4 dx-line and baseline probes and outputs"
}
````

### User / tool · 2026-11-02T10:45:34.466Z

**tool result**
````
"""T-116 r4: take the committed lib10 and lib06 packets, add ONE line a real claim form or bill carries (a diagnosis line) to the paperwork
record, nothing else, and compare the gap flags. Usage: .venv/bin/python -I <this> <TREE_DIR>"""
import sys, os, re
TREE = sys.argv[1]; os.chdir(TREE); sys.path.insert(0, TREE)
from app.backend import gaps as G, ingest as I
def flags(text):
    recs = I.ingest(text)["records"]
    return [(f["from_date"], f["to_date"], f["days"], bool(f.get("conditional")), [w["side"] for w in f.get("endpoint_warnings") or []]) for f in G.gap_flags(recs)]
def add(text, n, extra):
    i = text.index(f"=== Record {n} ==="); j = text.index('Excerpt: "', i); k = text.index('"\n', j + 10)
    return text[:k] + " " + extra + text[k:]
for pk, n, extra in (("evals/library/case_lib10_eob_ub04_cms1500.txt", 8, "Item 21 Diagnosis: M54.2 cervicalgia."),
                     ("evals/library/case_lib06_lop_billed_vs_adjusted.txt", 4, "Diagnosis: M25.511 pain in right shoulder.")):
    t = open(pk, encoding="utf-8").read()
    print(pk.split("/")[-1], "record", n, "as committed :", flags(t))
    print(" " * len(pk.split("/")[-1]), "record", n, "+ dx line    :", flags(add(t, n, extra)))
----
case_lib10_eob_ub04_cms1500.txt record 8 as committed : [('2026-07-14', '2026-08-26', 43, False, ['start'])]
                                record 8 + dx line    : [('2026-07-14', '2026-08-26', 43, False, ['start'])]
case_lib06_lop_billed_vs_adjusted.txt record 4 as committed : [('2026-05-13', '2026-06-17', 35, True, ['inside']), ('2026-07-08', '2026-09-02', 56, False, [])]
                                      record 4 + dx line    : [('2026-07-08', '2026-09-02', 56, False, [])]
----
"""T-116 r4: accident-date baseline with an intake form as the earliest record. Usage: .venv/bin/python -I <this> <TREE_DIR>"""
import sys, os
TREE = sys.argv[1]; os.chdir(TREE); sys.path.insert(0, TREE)
from app.backend import conflicts as C, ingest as I
H = "SYNTHETIC — invented for evaluation; not real patient data\n\n"
def run(tag, intake_text):
    t = H + (f"=== Record 1 ===\nDate: 2026-01-12\nSource: Capital PT, intake form\nExcerpt: \"{intake_text}\"\n\n"
             "=== Record 2 ===\nDate: 2026-01-20\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%.\"\n")
    cs = C.accident_date_conflicts(I.ingest(t)["records"])
    print(f"[{tag}] {len(cs)} conflict(s)")
    for c in cs: print("   ", c["title"], "|", c["explanation"])
run("B1 plain intake form", "Patient-completed intake form. Date of accident: 2026-01-15.")
run("B2 intake form that asks 'seen by'", "Patient-completed intake form. Date of accident: 2026-01-15. Have you been seen by a physician for this problem? Yes.")
----
[B1 plain intake form] 1 conflict(s)
    Stated accident date is later than the earliest record | Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the earliest recorded date, January 12, 2026 (record 1: Capital PT, intake form), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: Capital PT, intake form is paperwork, not a visit, the first recorded visit is January 20, 2026 (record 2: Capital PT, initial evaluation), and the stated date is not later than it. Check when treatment actually began before relying on this comparison.
[B2 intake form that asks 'seen by'] 1 conflict(s)
    Stated accident date is later than recorded treatment | Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form). The records disagree; the tool does not choose between them.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:37.433Z

**tool call — Bash**
````
{
 "command": "git show f8f358e -- app/backend/gaps.py tests/unit/test_t116_r4_all_dated_records.py | head -150",
 "description": "Show the HEAD commit diff for gaps.py and r4 test"
}
````

### User / tool · 2026-11-02T10:45:37.542Z

**tool result**
````
commit f8f358e1b33a6613b63b8d116d1d4ddac27b4d9c
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 04:44:53 2026 -0600

    fix(backend): T-116 r5 paperwork warning is header-only; text evidence never suppresses it (D-055)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/gaps.py b/app/backend/gaps.py
index 4ab344f..5e408cb 100644
--- a/app/backend/gaps.py
+++ b/app/backend/gaps.py
@@ -42,17 +42,6 @@ _TITLE = re.compile(r"^\W*(?:new[- ]patient\s+)?(?:intake|registration|admission
 _VISIT_WORD = re.compile(r"\b(?:visits?|evaluations?|evals?|exams?|examinations?|consult\w*|follow-?ups?|progress|sessions?|treatments?|therapy|"
                          r"procedures?|injections?|operative|surgery|imaging|mri|x-?rays?|notes?|soap|daily|new\s+patient|initial|discharge|esi|epidural|"
                          r"visita|consulta|nota|sesi[oó]n|evaluaci[oó]n|terapia|tratamiento|cita)\b", re.IGNORECASE)
-# Treatment evidence in the record's own text: clinician-note headings (exam, assessment, plan, vitals, procedure, diagnosis), vitals values,
-# a seen-by line, or something administered or performed. Any one keeps the record a treatment encounter whatever its label says.
-_EVIDENCE = re.compile(
-    r"(?:^|[.;:\n]\s*)(?:physical\s+|clinical\s+)?(?:exam(?:ination)?|findings|vitals?|vital\s+signs|assessment|impression|plan|a/p|objective|"
-    r"procedures?(?:\s+performed)?|medications?\s+administered|examen(?:\s+f[ií]sico)?|diagn[oó]stico|evaluaci[oó]n|plan\s+de\s+tratamiento)\s*:"
-    r"|\bBP\s*:?\s*\d{2,3}\s*/\s*\d{2,3}\b|\bblood\s+pressure\b|\b(?:HR|pulse|SpO2|RR)\s*:?\s*\d{2,3}\b"
-    r"|\b(?:seen|examined|evaluated|treated|attended)\s+by\b|\b(?:visto|atendid[oa])\s+por\b"
-    r"|\b(?:administered|injected|dispensed|performed)\b", re.IGNORECASE | re.MULTILINE)
-# A diagnosis heading is treatment evidence in a visit note but not in a letter, review or affidavit that restates a diagnosis from the chart.
-_DX = re.compile(r"(?:^|[.;:\n]\s*)(?:diagnos[ie]s|dx)\s*:", re.IGNORECASE | re.MULTILINE)
-_SUMMARY_TYPES = {"narrative letter", "letter or correspondence", "records review", "affidavit"}
 
 
 def _bare(src: str) -> str:
@@ -65,17 +54,13 @@ def _bare(src: str) -> str:
         h = n
 
 
-def _has_treatment_evidence(rec: dict, label: str) -> bool:
-    text = rec.get("excerpt") or ""
-    return bool(_EVIDENCE.search(text)) or (label not in _SUMMARY_TYPES and bool(_DX.search(text)))
-
-
 def admin_label(rec: dict):
     """The plain label of a record whose header looks administrative ("intake form", "billing statement", ...), or None. WARNING ONLY (D-055):
     it never changes a gap. It stays conservative so a warning means something: (1) the administrative type is read from the record-type head
     (last comma segment) of the header label, or from the record's own first-line title; (2) no visit word appears in the label outside parentheses and
-    outside the provider name (first segment) once that phrase is removed ("records review visit", "Capital PT, daily note, fax" are visits); (3) the text shows no
-    treatment evidence. When unsure there is no warning."""
+    outside the provider name (first segment) once that phrase is removed ("records review visit", "Capital PT, daily note, fax" are visits); (3) the record's text is never consulted
+    for treatment words (T-116 r5): a bill, EOB, request or form routinely lists diagnoses and services performed, and a warning costs a click while a hidden span
+    costs the case. Fail toward warning."""
     bare = _bare(rec.get("source"))
     head = bare.rsplit(",", 1)[-1].strip()
     label, rest = None, ""
@@ -95,7 +80,7 @@ def admin_label(rec: dict):
         if k not in ("encounter", "unsplit_text"):
             label = {"billing_statement": "billing statement", "phone_note": "phone or message note"}.get(k, "administrative record")
             rest = bare.split(",", 1)[1] if "," in bare else ""
-    if not label or _VISIT_WORD.search(rest) or _has_treatment_evidence(rec, label):
+    if not label or _VISIT_WORD.search(rest):
         return None
     return label
 
diff --git a/tests/unit/test_t116_r4_all_dated_records.py b/tests/unit/test_t116_r4_all_dated_records.py
index 95c8801..4bc825f 100644
--- a/tests/unit/test_t116_r4_all_dated_records.py
+++ b/tests/unit/test_t116_r4_all_dated_records.py
@@ -91,9 +91,11 @@ def test_midspan_paperwork_that_splits_a_40_day_span_into_two_short_pieces_still
     assert (w["side"], w["record_no"], w["alternative_days"]) == ("inside", 2, 40)
 
 
-def test_a_midspan_visit_with_treatment_evidence_does_not_draw_the_flag():
+def test_midspan_paperwork_with_exam_text_still_draws_the_flag_r5():
+    """T-116 r5: the header decides, not the text. A form-headed record whose text reads like an exam still warns (it costs a click)."""
     recs, flags = run(("2026-03-01", "Capital PT, visit 1", PLAIN), ("2026-03-20", "Capital PT, intake form", HEADED), ("2026-04-10", "Capital PT, visit 3", PLAIN))
-    assert flags == []
+    (f,) = flags
+    assert (f["days"], f["conditional"], [w["side"] for w in f["endpoint_warnings"]]) == (40, True, ["inside"])
 
 
 def test_midspan_paperwork_inside_a_span_of_30_days_or_less_draws_nothing():
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:37.814Z

**tool call — Bash**
````
{
 "command": "cat tests/unit/test_t116_r5_header_only_warning.py",
 "description": "Read the new r5 unit test file"
}
````

### User / tool · 2026-11-02T10:45:37.892Z

**tool result**
````
"""T-116 round 5 (D-055): a paperwork-headed record warns whatever its text says. Treatment words (diagnosis lines, 'performed', 'seen by')
never suppress the warning, the alternative, the conditional flag or the accident-baseline caveat. Reviewer probes from
artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py, -packet-dx-line.py and -baseline.py. Fixture backend, no network."""
import pathlib

import pytest

from app.backend import conflicts as CF
from app.backend import gaps as GP
from app.backend import ingest as I

ROOT = pathlib.Path(__file__).resolve().parents[2]
HDR = "SYNTHETIC — invented for evaluation; not real patient data\n\n"
V = "Neck pain 5/10. Improved range of motion. Continue home exercise."
PAPER = [
    ("Capital PT, billing statement", "Statement of account. Dx: M54.2 cervicalgia. CPT 97110 x4. Balance due $740."),
    ("Capital PT, billing statement", "Statement of account. Services performed 03/01/2026 and 03/08/2026. Balance due $740."),
    ("Capital PT, billing statement", "Statement of account. Balance due $740."),
    ("Capital PT, intake form", "Have you been seen by a physician for this problem? Yes. Pain diagram completed."),
    ("Capital PT, intake form", "Patient-completed intake form. Date of birth, insurance, emergency contact."),
    ("Capital PT, records request", "Please produce all records of treatment performed on this patient 03/01/2026 through 04/10/2026."),
    ("Capital PT, affidavit of records custodian", "I certify the attached records are true copies. Services were performed on the dates shown."),
    ("Quoinmere Mutual Health Plan, EOB", "Explanation of benefits. Diagnosis: M54.2. Allowed amount $120."),
]


def pk(items):
    return HDR + "".join(f"=== Record {i} ===\nDate: {d}\nSource: {s}\nExcerpt: \"{e}\"\n\n" for i, (d, s, e) in enumerate(items, 1))


def flags_of(items):
    return GP.gap_flags(I.ingest(pk(items))["records"])


@pytest.mark.parametrize("src,txt", PAPER)
def test_eight_paperwork_variants_show_the_span_and_the_alternative(src, txt):
    (mid,) = flags_of([("2026-03-01", "Capital PT, visit 1", V), ("2026-03-20", src, txt), ("2026-04-10", "Capital PT, visit 3", V)])
    assert (mid["days"], mid["conditional"], [w["side"] for w in mid["endpoint_warnings"]]) == (40, True, ["inside"])
    assert mid["endpoint_warnings"][0]["alternative_days"] == 40
    (end,) = flags_of([("2026-03-01", "Capital PT, visit 1", V), ("2026-04-10", src, txt)])
    assert (end["days"], bool(end.get("conditional")), [w["side"] for w in end["endpoint_warnings"]]) == (40, False, ["end"])


def test_lib06_keeps_its_35_day_flag_with_a_diagnosis_line_on_the_billing_record():
    t = (ROOT / "evals/library/case_lib06_lop_billed_vs_adjusted.txt").read_text(encoding="utf-8")
    i = t.index("=== Record 4 ==="); j = t.index('Excerpt: "', i); k = t.index('"\n', j + 10)
    for text in (t, t[:k] + " Diagnosis: M25.511 pain in right shoulder." + t[k:]):
        fl = GP.gap_flags(I.ingest(text)["records"])
        assert any(f["days"] == 35 and f["conditional"] and (f["from_date"], f["to_date"]) == ("2026-05-13", "2026-06-17") for f in fl)


def test_accident_baseline_never_calls_a_paperwork_headed_record_the_first_recorded_treatment():
    for txt in ("Patient-completed intake form. Date of accident: 2026-01-15.",
                "Patient-completed intake form. Date of accident: 2026-01-15. Have you been seen by a physician for this problem? Yes."):
        t = HDR + (f"=== Record 1 ===\nDate: 2026-01-12\nSource: Capital PT, intake form\nExcerpt: \"{txt}\"\n\n"
                   "=== Record 2 ===\nDate: 2026-01-20\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%.\"\n")
        (c,) = CF.accident_date_conflicts(I.ingest(t)["records"])
        assert "first recorded treatment" not in c["explanation"]
        assert "looks like paperwork" in c["explanation"]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:47.562Z

**tool call — Bash**
````
{
 "command": "head -30 artifacts/review-evidence/T-116-paralegal-r3-probe.py && echo ---- && grep -n \"print\\|def \\|sys.argv\" artifacts/review-evidence/T-116-paralegal-r3-probe.py | head -60 && echo ---- && cat artifacts/review-evidence/T-116-paralegal-r4-packet-flags.py && echo ---- && cat artifacts/review-evidence/T-116-paralegal-r4-warn-and-api.head.out.txt | head -80",
 "description": "Read r3 probe script and r4 warn outputs"
}
````

### User / tool · 2026-11-02T10:45:47.676Z

**tool result**
````
"""T-116 round-3 paralegal probe (D-055): one code tree, every probe the r1 and r2 reviews ran, plus the 25 packets and the F3 case.

Usage: .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r3-probe.py <TREE_DIR> <OUT_JSON>
Run on the pre-T-116 parent (3e3f3b7) and on HEAD (8673326) from git archive copies, then compare with T-116-paralegal-r3-compare.py.
Every label is put in a three-visit packet (3/01 visit, 3/20 candidate, 4/10 visit) and run through ingest.ingest and gaps.gap_flags.
No code path here uses a classifier from the tree: only ingest, compute_gaps, gap_flags and conflicts.accident_date_conflicts.
"""
import sys, os, json, pathlib

TREE, OUT = sys.argv[1], sys.argv[2]
os.chdir(TREE)
sys.path.insert(0, TREE)
from app.backend import gaps as G, ingest as I, conflicts as C  # noqa: E402

assert G.__file__.startswith(TREE), G.__file__
assert C.__file__.startswith(TREE), C.__file__

HDR = "SYNTHETIC — invented for evaluation; not real patient data\n\n"
PLAIN = "Neck pain 5/10. Improved range of motion. Continue home exercise."
HEADED = "Exam: neck range of motion reduced. Plan: continue PT 2x/week."
VISIT_19 = [  # r1 sweep (c1b44be review, 2026-11-02 09:43)
    "Capital PT, initial evaluation (intake form completed same day)",
    "Hill Country Pain Management, intake form visit",
    "Dr. Alvarez, primary care, visit with billing review",
    "Dr. Alvarez, primary care, patient statement at visit",
    "Dr. Reyes, orthopedics, statement of MMI",
    "Austin Imaging, MRI cervical spine (records request attached)",
    "Dr. Lee, chiropractic, fax copy of visit 3",
    "Dr. Lee, chiropractic, visit 3 (faxed)",
    "Dr. Nguyen, records review visit",
----
10:TREE, OUT = sys.argv[1], sys.argv[2]
59:def packet(mid, mid_text):
66:def gap_view(g):
70:def flag_view(f):
76:def with_fax(text, n):
141:print("tree", TREE)
142:print("module", G.__file__)
143:print("labels", len(out["labels"]), "appendix_fax", len(out["appendix_fax"]), "packets", len(out["packets"]))
144:print("f3 kinds", out["f3"]["kinds"], "conflicts", len(out["f3"]["conflicts"]))
----
import json,sys
H=json.load(open(sys.argv[1])); P=json.load(open(sys.argv[2]))
pre={p["packet"]:p for p in P["packets"]}
print("== every golden/pre flagged gap vs HEAD (shown as counted flag, alt of a warning, or conditional)")
for b in H["packets"]:
    a=pre[b["packet"]]
    pre_fl=[(f["from"],f["to"],f["days"]) for f in a["flags"]]
    exp_fl=[(r[0],r[1],r[2]) for r in b["expected_gap_rows"] if r[3]]
    head_fl=[(f["from"],f["to"],f["days"]) for f in b["flags"]]
    # alternatives live in explanation text
    shown=[]
    for e in set(pre_fl)|set(exp_fl):
        ok = e in head_fl or any(e[2]==0 for _ in [0])
        if not ok:
            # look in explanation for the alt sentence
            from datetime import date
            ok = any(("would be %d days"%e[2] in f["explanation"] or "%d days"%e[2] in f["explanation"]) for f in b["flags"])
        shown.append((e,ok))
    status="OK" if all(o for _,o in shown) else "MISSING"
    extra=[e for e in head_fl if e not in pre_fl and e not in exp_fl]
    if pre_fl!=head_fl or extra or status!="OK":
        print(b["packet"],status,"pre",pre_fl,"exp",exp_fl,"head",head_fl,"shown",shown)
for b in H["packets"]:
    if b["flags"]:
        for f in b["flags"]:
            print("\n#",b["packet"],f["from"],f["to"],f["days"],f["record_nos"]); print("  ",f["explanation"])
----
== Part 1: constructed packets
[W1 gap ENDS at 'Capital PT, intake form' (encounter kind)] kinds: [(1, '2026-03-01', 'encounter'), (2, '2026-04-10', 'encounter')]
   flag 2026-03-01 -> 2026-04-10 days=40 records=[1, 2]
   explanation: Gap of 40 days between March 1, 2026 (Capital PT, visit 1) and April 10, 2026 (Capital PT, intake form). This gap ends at record 2: Capital PT, intake form, which looks like paperwork, not a visit. Check whether treatment continued. If record 2: Capital PT, intake form is paperwork, not a visit, there would be no visit after it and no gap to measure.
   endpoint_warning: end 2 This gap ends at record 2: Capital PT, intake form, which looks like paperwork, not a visit. Check whether treatment continued.
[W2 gap STARTS at 'Capital PT, intake form' (encounter kind)] kinds: [(1, '2026-03-01', 'encounter'), (2, '2026-04-10', 'encounter')]
   flag 2026-03-01 -> 2026-04-10 days=40 records=[1, 2]
   explanation: Gap of 40 days between March 1, 2026 (Capital PT, intake form) and April 10, 2026 (Capital PT, visit 3). This gap starts at record 1: Capital PT, intake form, which looks like paperwork, not a visit. Check whether treatment continued. If record 1: Capital PT, intake form is paperwork, not a visit, there would be no visit before it and no gap to measure.
   endpoint_warning: start 1 This gap starts at record 1: Capital PT, intake form, which looks like paperwork, not a visit. Check whether treatment continued.
[W3 intake form dated INSIDE a 40-day span with no visit] kinds: [(1, '2026-03-01', 'encounter'), (2, '2026-03-20', 'encounter'), (3, '2026-04-10', 'encounter')]
   flag 2026-03-01 -> 2026-04-10 days=40 records=[1, 2, 3]
   explanation: Possible gap of 40 days between March 1, 2026 (Capital PT, visit 1) and April 10, 2026 (Capital PT, visit 3). No gap is counted here because record 2: Capital PT, intake form (March 20, 2026) falls inside this span and is counted as a visit (19 days, then 21 days). If record 2: Capital PT, intake form is paperwork, not a visit, the gap would be 40 days (March 1, 2026 to April 10, 2026).
   endpoint_warning: inside 2 No gap is counted here because record 2: Capital PT, intake form (March 20, 2026) falls inside this span and is counted as a visit (19 days, then 21 days).
[W4 visit with a paperwork word, ends the span (records-request copy, visit wording)] kinds: [(1, '2026-03-01', 'encounter'), (2, '2026-04-10', 'records_admin')]
   flag 2026-03-01 -> 2026-04-10 days=40 records=[1, 2]
   explanation: Gap of 40 days between March 1, 2026 (Capital PT, visit 1) and April 10, 2026 (Capital PT, visit 3 - records request copy).

== Part 2: lib09 through the API
run 202
BEFORE confirm: [
 {
  "title": "Gap of 42 days",
  "days": 42,
  "from": "2026-03-03",
  "to": "2026-04-14",
  "record_nos": null,
  "endpoint_warnings": [],
  "explanation": "Gap of 42 days between March 3, 2026 (Quillmere Regional ED) and April 14, 2026 (Consultorio Médico Aguaclara, nota de consulta).",
  "why": "One end of this gap could involve a date that has not been confirmed. AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it."
 }
]
confirm status 200 gap_changes [{"flag_id": "f_gap_r4_r2", "change": "changed", "old_days": 42, "new_days": 40, "old_from": "2026-03-03", "old_to": "2026-04-14", "new_from": "2026-03-05", "new_to": "2026-04-14", "sentence": "Gap recalculated after you confirmed record 4: now 40 days (was 42)."}]
AFTER confirm: [
 {
  "title": "Gap of 40 days",
  "days": 40,
  "from": "2026-03-05",
  "to": "2026-04-14",
  "record_nos": null,
  "endpoint_warnings": [
   {
    "alternative": "If record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR) is paperwork, not a visit, the gap would be 42 days (March 3, 2026 to April 14, 2026).",
    "alternative_days": 42,
    "alternative_from": "2026-03-03",
    "alternative_to": "2026-04-14",
    "date": "2026-03-05",
    "record_no": 4,
    "record_type": "intake form",
    "side": "start",
    "warning": "This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued."
   }
  ],
  "explanation": "Gap of 40 days between March 5, 2026 (Consultorio Médico Aguaclara, formulario de admisión (OCR)) and April 14, 2026 (Consultorio Médico Aguaclara, nota de consulta). This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued. If record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR) is paperwork, not a visit, the gap would be 42 days (March 3, 2026 to April 14, 2026).",
  "why": "AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it. This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued. If record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR) is paperwork, not a visit, the gap would be 42 days (March 3, 2026 to April 14, 2026)."
 }
]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:50.068Z

**tool call — Bash**
````
{
 "command": "sed -n 30,150p artifacts/review-evidence/T-116-paralegal-r3-probe.py",
 "description": "Read the rest of the r3 probe script"
}
````

### User / tool · 2026-11-02T10:45:50.151Z

**tool result**
````
    "Dr. Nguyen, records review visit",
    "Capital PT, discharge summary letter",
    "Dr. Patel, telehealth visit",
    "Dr. Patel, telephone visit (video)",
    "Brightwater Spine, new patient, consent form for ESI on same day",
    "Dr. Alvarez, pre-operative consent form and examination",
    "Capital PT, daily note (copy of billing record)",
    "Hill Country Pain Management, new patient",
    "Dr. Alvarez, initial visit; intake packet reviewed",
    "Capital PT, visit 5 (ledger balance reviewed)",
    "Dr. Oyelaran, physician statement of disability",
]
NEW_8 = [  # r2 review (ea6ac71 10:03), eight tricky labels
    "Office visit / records request",
    "PT daily note (billing copy)",
    "Intake and evaluation",
    "Capital PT, daily note, fax",
    "Capital PT, re-eval visit, statement",
    "Hill Country Pain Management, new patient, billing",
    "Capital PT, initial evaluation, correspondence",
    "Dr. Lee, chiropractic, visit 3 - records request copy",
]
CONTROLS = [  # r2 controls: clearly administrative labels, plus the plain visit 2
    "Capital PT, intake form",
    "Dr. Lee, chiropractic, billing statement",
    "Capital PT, visit 2",
]


def packet(mid, mid_text):
    return HDR + (
        "=== Record 1 ===\nDate: 2026-03-01\nSource: Capital PT, visit 1\nExcerpt: \"" + PLAIN + "\"\n\n"
        "=== Record 2 ===\nDate: 2026-03-20\nSource: " + mid + "\nExcerpt: \"" + mid_text + "\"\n\n"
        "=== Record 3 ===\nDate: 2026-04-10\nSource: Capital PT, visit 3\nExcerpt: \"" + PLAIN + "\"\n")


def gap_view(g):
    return [g["from_date"], g["to_date"], g["days"], g["flag"], g["from_records"], g["to_records"]]


def flag_view(f):
    return {"from": f["from_date"], "to": f["to_date"], "days": f["days"], "record_nos": f["record_nos"],
            "warnings": [[w["side"], w["record_no"], w["warning"]] for w in (f.get("endpoint_warnings") or [])],
            "explanation": f["explanation"]}


def with_fax(text, n):
    """Append ', fax' to the Source line of record n, and nothing else."""
    i = text.index(f"=== Record {n} ===")
    j = text.index("Source: ", i)
    k = text.index("\n", j)
    return text[:k] + ", fax" + text[k:]


out = {"tree": TREE, "module": G.__file__, "labels": [], "appendix_fax": [], "packets": [], "f3": {}}

# A. every r1 and r2 label, plain and headed excerpt, inside a three-visit packet
for s in VISIT_19 + NEW_8 + CONTROLS:
    for name, txt in (("plain", PLAIN), ("headed", HEADED)):
        recs = I.ingest(packet(s, txt))["records"]
        mid = next(r for r in recs if r["n"] == 2)
        out["labels"].append({"label": s, "excerpt": name, "mid_kind": mid["kind"], "mid_source": mid.get("source"),
                              "gap_rows": [gap_view(g) for g in G.compute_gaps(recs)],
                              "flags": [flag_view(f) for f in G.gap_flags(recs)]})

# B. Appendix A sample: control, then each record that is a treatment encounter with ", fax" added to its Source line
sample_text = open(TREE + "/evals/golden/sample.txt", encoding="utf-8").read()
srecs = I.ingest(sample_text)["records"]
out["appendix_fax"].append({"n": None, "source": "control (verbatim sample.txt)", "kinds": [(r["n"], r["kind"]) for r in srecs],
                            "gap_rows": [gap_view(g) for g in G.compute_gaps(srecs)],
                            "flags": [flag_view(f) for f in G.gap_flags(srecs)]})
for r in srecs:
    if r["kind"] != "encounter":
        continue
    recs = I.ingest(with_fax(sample_text, r["n"]))["records"]
    out["appendix_fax"].append({"n": r["n"], "source": (r.get("source") or "") + ", fax",
                                "gap_rows": [gap_view(g) for g in G.compute_gaps(recs)],
                                "flags": [flag_view(f) for f in G.gap_flags(recs)]})

# C. the 25 packets: 9 golden + 15 library + sample, through the fixture pipeline of this tree
from evals import run as R  # noqa: E402
p = R.load_pipeline()
paths = sorted(pathlib.Path(x) for x in __import__("glob").glob(TREE + "/evals/golden/case_*.txt"))
paths += sorted(pathlib.Path(x) for x in __import__("glob").glob(TREE + "/evals/library/case_*.txt"))
paths.append(pathlib.Path(TREE) / "evals/golden/sample.txt")
assert len(paths) == 25, len(paths)
for tp in paths:
    ep = tp.with_name(tp.stem + ".expected.json")
    exp = json.loads(ep.read_text(encoding="utf-8")) if ep.exists() else {}
    res = p.run_case(tp.read_text(encoding="utf-8"), "fixture")
    recs = res.get("records") or []
    out["packets"].append({
        "packet": tp.stem, "status": res.get("status"), "n_recs": len(recs),
        "records": [{"n": r["n"], "date": r.get("date_iso"), "source": r.get("source"), "kind": r.get("kind")} for r in recs],
        "gap_rows": [gap_view(g) for g in G.compute_gaps(recs)],
        "flags": [flag_view(f) for f in G.gap_flags(recs)],
        "expected_gap_rows": [[g["from_date"], g["to_date"], g["days"], g["flag"], g["from_records"], g["to_records"]]
                              for g in exp.get("gap_table", [])],
        "expected_gap_excluded": exp.get("gap_excluded_records"),
    })

# D. F3: an intake form dated before the first visit, with its own stated accident date between the two
text = HDR + (
    "=== Record 1 ===\nDate: 2026-01-12\nSource: Capital PT, intake form\nExcerpt: \"Patient-completed intake form. Date of accident: 2026-01-15.\"\n\n"
    "=== Record 2 ===\nDate: 2026-01-20\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%.\"\n")
frecs = I.ingest(text)["records"]
out["f3"] = {"kinds": [(r["n"], r["kind"]) for r in frecs],
             "conflicts": [{"title": c.get("title"), "explanation": c.get("explanation"), "record_nos": c.get("record_nos")}
                           for c in C.accident_date_conflicts(frecs)]}

json.dump(out, open(OUT, "w"), indent=1, ensure_ascii=False, default=str)
print("tree", TREE)
print("module", G.__file__)
print("labels", len(out["labels"]), "appendix_fax", len(out["appendix_fax"]), "packets", len(out["packets"]))
print("f3 kinds", out["f3"]["kinds"], "conflicts", len(out["f3"]["conflicts"]))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:45:55.019Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && T=$S/t116r5/head && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py $T 2>&1; echo \"exit=$?\"; echo ----; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r4-packet-dx-line.py $T 2>&1; echo \"exit=$?\"; echo ----; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r4-baseline.py $T 2>&1; echo \"exit=$?\"",
 "description": "Re-run r4 suppression, dx-line and baseline probes on HEAD copy"
}
````

### User / tool · 2026-11-02T10:45:55.464Z

**tool result**
````
tree /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r5/head
billing statement, Dx code line            MID-SPAN flags=[(40, True, ['inside'])] | ENDS-GAP flags=[(40, False, ['end'])]
billing statement, 'services performed'    MID-SPAN flags=[(40, True, ['inside'])] | ENDS-GAP flags=[(40, False, ['end'])]
billing statement, plain                   MID-SPAN flags=[(40, True, ['inside'])] | ENDS-GAP flags=[(40, False, ['end'])]
intake form, 'seen by'                     MID-SPAN flags=[(40, True, ['inside'])] | ENDS-GAP flags=[(40, False, ['end'])]
intake form, plain                         MID-SPAN flags=[(40, True, ['inside'])] | ENDS-GAP flags=[(40, False, ['end'])]
records request, 'treatment performed'     MID-SPAN flags=[(40, True, ['inside'])] | ENDS-GAP flags=[(40, False, ['end'])]
affidavit, 'were performed'                MID-SPAN flags=[(40, True, ['inside'])] | ENDS-GAP flags=[(40, False, ['end'])]
EOB, Diagnosis line                        MID-SPAN flags=[(40, True, ['inside'])] | ENDS-GAP flags=[(40, False, ['end'])]
exit=0
----
case_lib10_eob_ub04_cms1500.txt record 8 as committed : [('2026-07-14', '2026-08-26', 43, False, ['start'])]
                                record 8 + dx line    : [('2026-07-14', '2026-08-26', 43, False, ['start'])]
case_lib06_lop_billed_vs_adjusted.txt record 4 as committed : [('2026-05-13', '2026-06-17', 35, True, ['inside']), ('2026-07-08', '2026-09-02', 56, False, [])]
                                      record 4 + dx line    : [('2026-05-13', '2026-06-17', 35, True, ['inside']), ('2026-07-08', '2026-09-02', 56, False, [])]
exit=0
----
[B1 plain intake form] 1 conflict(s)
    Stated accident date is later than the earliest record | Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the earliest recorded date, January 12, 2026 (record 1: Capital PT, intake form), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: Capital PT, intake form is paperwork, not a visit, the first recorded visit is January 20, 2026 (record 2: Capital PT, initial evaluation), and the stated date is not later than it. Check when treatment actually began before relying on this comparison.
[B2 intake form that asks 'seen by'] 1 conflict(s)
    Stated accident date is later than the earliest record | Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the earliest recorded date, January 12, 2026 (record 1: Capital PT, intake form), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: Capital PT, intake form is paperwork, not a visit, the first recorded visit is January 20, 2026 (record 2: Capital PT, initial evaluation), and the stated date is not later than it. Check when treatment actually began before relying on this comparison.
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:46:04.759Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && T=$S/t116r5/head && mkdir -p $S/t116r5/out && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r3-probe.py $T $S/t116r5/out/head.json 2>&1; echo \"exit=$?\"; git archive 3e3f3b7 | (mkdir -p $S/t116r5/pre && tar -x -C $S/t116r5/pre) && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r3-probe.py $S/t116r5/pre $S/t116r5/out/pre.json 2>&1; echo \"exit=$?\"; cat artifacts/review-evidence/T-116-paralegal-r4-labels-view.py",
 "description": "Run r3 label and packet probe on HEAD and pre-T-116 copies"
}
````

### User / tool · 2026-11-02T10:46:08.670Z

**tool result**
````
llm call failed call_id=c31aa6ab35530 step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
tree /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r5/head
module /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r5/head/app/backend/gaps.py
labels 60 appendix_fax 10 packets 25
f3 kinds [(1, 'encounter'), (2, 'encounter')] conflicts 1
exit=0
llm call failed call_id=c22b8a39af66d step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
tree /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r5/pre
module /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r5/pre/app/backend/gaps.py
labels 60 appendix_fax 10 packets 25
f3 kinds [(1, 'encounter'), (2, 'encounter')] conflicts 1
exit=0
import json,sys
H=json.load(open(sys.argv[1]))
print("== labels, plain+headed: flags at HEAD")
for l in H["labels"]:
    fl=l["flags"]
    s=[(f["days"],f["from"],f["to"],[ (w["side"] if isinstance(w,dict) else w[0]) for w in []]) for f in fl]
    print(f'{l["excerpt"]:6s} {l["label"][:62]:62s} kind={l["mid_kind"]:14s} rows={[(g[2]) for g in l["gap_rows"]]} flags={[(f["days"]) for f in fl]} warn={[w[2][:0]+w[0]+str(w[1]) for f in fl for w in f["warnings"]]}')
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:46:15.685Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > $S/t116r5/labels_check.py <<'EOF'\nimport json, sys\nH = json.load(open(sys.argv[1]))\nrows = {}\nfor l in H[\"labels\"]:\n    key = (l[\"label\"], l[\"excerpt\"])\n    gaps = [g[2] for g in l[\"gap_rows\"]]\n    flags = [(f[\"days\"], [w[0] for w in f[\"warnings\"]]) for f in l[\"flags\"]]\n    rows[key] = (l[\"mid_kind\"], gaps, flags)\n    print(f'{l[\"excerpt\"]:6s} kind={l[\"mid_kind\"]:14s} gaps={gaps} flags={flags} | {l[\"label\"]}')\nprint(\"labels:\", len(rows))\nbad = [k for k, v in rows.items() if v[1] != [19, 21]]\nprint(\"runs where counted gap rows != [19, 21]:\", len(bad), bad[:5])\nEOF\n.venv/bin/python -I $S/t116r5/labels_check.py $S/t116r5/out/head.json",
 "description": "Summarize label-sweep gap rows and flags on HEAD"
}
````

### User / tool · 2026-11-02T10:46:15.826Z

**tool result**
````
plain  kind=encounter      gaps=[19, 21] flags=[] | Capital PT, initial evaluation (intake form completed same day)
headed kind=encounter      gaps=[19, 21] flags=[] | Capital PT, initial evaluation (intake form completed same day)
plain  kind=encounter      gaps=[19, 21] flags=[] | Hill Country Pain Management, intake form visit
headed kind=encounter      gaps=[19, 21] flags=[] | Hill Country Pain Management, intake form visit
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Alvarez, primary care, visit with billing review
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Alvarez, primary care, visit with billing review
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Alvarez, primary care, patient statement at visit
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Alvarez, primary care, patient statement at visit
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Reyes, orthopedics, statement of MMI
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Reyes, orthopedics, statement of MMI
plain  kind=records_admin  gaps=[19, 21] flags=[] | Austin Imaging, MRI cervical spine (records request attached)
headed kind=records_admin  gaps=[19, 21] flags=[] | Austin Imaging, MRI cervical spine (records request attached)
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Lee, chiropractic, fax copy of visit 3
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Lee, chiropractic, fax copy of visit 3
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Lee, chiropractic, visit 3 (faxed)
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Lee, chiropractic, visit 3 (faxed)
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Nguyen, records review visit
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Nguyen, records review visit
plain  kind=encounter      gaps=[19, 21] flags=[] | Capital PT, discharge summary letter
headed kind=encounter      gaps=[19, 21] flags=[] | Capital PT, discharge summary letter
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Patel, telehealth visit
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Patel, telehealth visit
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Patel, telephone visit (video)
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Patel, telephone visit (video)
plain  kind=encounter      gaps=[19, 21] flags=[] | Brightwater Spine, new patient, consent form for ESI on same day
headed kind=encounter      gaps=[19, 21] flags=[] | Brightwater Spine, new patient, consent form for ESI on same day
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Alvarez, pre-operative consent form and examination
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Alvarez, pre-operative consent form and examination
plain  kind=encounter      gaps=[19, 21] flags=[] | Capital PT, daily note (copy of billing record)
headed kind=encounter      gaps=[19, 21] flags=[] | Capital PT, daily note (copy of billing record)
plain  kind=encounter      gaps=[19, 21] flags=[] | Hill Country Pain Management, new patient
headed kind=encounter      gaps=[19, 21] flags=[] | Hill Country Pain Management, new patient
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Alvarez, initial visit; intake packet reviewed
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Alvarez, initial visit; intake packet reviewed
plain  kind=billing_statement gaps=[19, 21] flags=[] | Capital PT, visit 5 (ledger balance reviewed)
headed kind=billing_statement gaps=[19, 21] flags=[] | Capital PT, visit 5 (ledger balance reviewed)
plain  kind=encounter      gaps=[19, 21] flags=[] | Dr. Oyelaran, physician statement of disability
headed kind=encounter      gaps=[19, 21] flags=[] | Dr. Oyelaran, physician statement of disability
plain  kind=records_admin  gaps=[19, 21] flags=[] | Office visit / records request
headed kind=records_admin  gaps=[19, 21] flags=[] | Office visit / records request
plain  kind=encounter      gaps=[19, 21] flags=[] | PT daily note (billing copy)
headed kind=encounter      gaps=[19, 21] flags=[] | PT daily note (billing copy)
plain  kind=encounter      gaps=[19, 21] flags=[] | Intake and evaluation
headed kind=encounter      gaps=[19, 21] flags=[] | Intake and evaluation
plain  kind=encounter      gaps=[19, 21] flags=[] | Capital PT, daily note, fax
headed kind=encounter      gaps=[19, 21] flags=[] | Capital PT, daily note, fax
plain  kind=encounter      gaps=[19, 21] flags=[] | Capital PT, re-eval visit, statement
headed kind=encounter      gaps=[19, 21] flags=[] | Capital PT, re-eval visit, statement
plain  kind=encounter      gaps=[19, 21] flags=[] | Hill Country Pain Management, new patient, billing
headed kind=encounter      gaps=[19, 21] flags=[] | Hill Country Pain Management, new patient, billing
plain  kind=records_admin  gaps=[19, 21] flags=[] | Capital PT, initial evaluation, correspondence
headed kind=records_admin  gaps=[19, 21] flags=[] | Capital PT, initial evaluation, correspondence
plain  kind=records_admin  gaps=[19, 21] flags=[] | Dr. Lee, chiropractic, visit 3 - records request copy
headed kind=records_admin  gaps=[19, 21] flags=[] | Dr. Lee, chiropractic, visit 3 - records request copy
plain  kind=encounter      gaps=[19, 21] flags=[(40, ['inside'])] | Capital PT, intake form
headed kind=encounter      gaps=[19, 21] flags=[(40, ['inside'])] | Capital PT, intake form
plain  kind=billing_statement gaps=[19, 21] flags=[(40, ['inside'])] | Dr. Lee, chiropractic, billing statement
headed kind=billing_statement gaps=[19, 21] flags=[(40, ['inside'])] | Dr. Lee, chiropractic, billing statement
plain  kind=encounter      gaps=[19, 21] flags=[] | Capital PT, visit 2
headed kind=encounter      gaps=[19, 21] flags=[] | Capital PT, visit 2
labels: 60
runs where counted gap rows != [19, 21]: 0 []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:46:22.020Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > $S/t116r5/appx_check.py <<'EOF'\nimport json, sys\nH = json.load(open(sys.argv[1]))\nfor a in H[\"appendix_fax\"]:\n    fl = [(f[\"from\"], f[\"to\"], f[\"days\"], [w[0] for w in f[\"warnings\"]]) for f in a[\"flags\"]]\n    print(a[\"n\"], \"|\", a[\"source\"][:60], \"| gaps\", [g[2] for g in a[\"gap_rows\"]], \"| flags\", fl)\nprint(\"---- f3 conflicts:\")\nfor c in H[\"f3\"][\"conflicts\"]:\n    print(c[\"title\"], \"|\", c[\"explanation\"])\nEOF\n.venv/bin/python -I $S/t116r5/appx_check.py $S/t116r5/out/head.json; echo ==== PRE; .venv/bin/python -I $S/t116r5/appx_check.py $S/t116r5/out/pre.json | head -12",
 "description": "Check Appendix A fax variants and F3 conflict on HEAD and pre"
}
````

### User / tool · 2026-11-02T10:46:22.159Z

**tool result**
````
None | control (verbatim sample.txt) | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
1 | Austin EMS run report, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
2 | Central ER discharge summary, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
3 | Dr. Alvarez, primary care, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
4 | Capital PT, initial evaluation, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
5 | Capital PT, visit 8, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
6 | Capital PT, visit 9, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
7 | Hill Country Pain Management, new patient, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
8 | Austin Imaging, cervical MRI, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
9 | Hill Country Pain Management, follow-up, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
---- f3 conflicts:
Stated accident date is later than the earliest record | Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the earliest recorded date, January 12, 2026 (record 1: Capital PT, intake form), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: Capital PT, intake form is paperwork, not a visit, the first recorded visit is January 20, 2026 (record 2: Capital PT, initial evaluation), and the stated date is not later than it. Check when treatment actually began before relying on this comparison.
==== PRE
None | control (verbatim sample.txt) | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
1 | Austin EMS run report, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
2 | Central ER discharge summary, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
3 | Dr. Alvarez, primary care, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
4 | Capital PT, initial evaluation, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
5 | Capital PT, visit 8, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
6 | Capital PT, visit 9, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
7 | Hill Country Pain Management, new patient, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
8 | Austin Imaging, cervical MRI, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
9 | Hill Country Pain Management, follow-up, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
---- f3 conflicts:
Stated accident date is later than recorded treatment | Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form). The records disagree; the tool does not choose between them.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:46:25.521Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && grep -rn \"first recorded treatment\\|earliest recorded\\|first recorded\" app/backend/ | head -20; echo ----; sed -n 40,90p app/backend/conflicts.py",
 "description": "Grep first-recorded wording and read accident conflict code"
}
````

### User / tool · 2026-11-02T10:46:25.614Z

**tool result**
````
app/backend/flag_templates.py:122:    """D-055 (T-116 round 4): the earliest recorded date belongs to a record that looks like paperwork. The sentence never calls it treatment; it names the
app/backend/flag_templates.py:123:    record and gives the other reading (the first recorded visit) so the paralegal decides."""
app/backend/flag_templates.py:129:        alt = (f"If record {v['record_no']}: {v.get('provider_a') or 'this record'} is paperwork, not a visit, the first recorded visit is {_d(v['alt_date'])} "
app/backend/flag_templates.py:134:            f"Stated accident date{stated}{quote} is later than the earliest recorded date, {first}, which looks like paperwork, not a visit. "
app/backend/flag_templates.py:146:            f"Stated accident date{stated}{quote} is later than the first recorded treatment{first}. "
app/backend/conflicts.py:2:accident_date_conflicts: stated accident dates (lexicon `accident_date_phrases`) vs the earliest recorded treatment date.
app/backend/conflicts.py:63:        # that record, says it looks like paperwork, and gives the other reading (the first recorded visit); the paralegal decides.
----
def accident_date_conflicts(records: list) -> list:
    """At most one conflict per case. (a) a stated date later than the earliest treatment date, or (b) two different stated dates."""
    stated = stated_accident_dates(records)
    enc = _encounters(records)
    if not stated or not enc:
        return []
    first = min(r["date_iso"] for r in enc)
    first_recs = [r for r in enc if r["date_iso"] == first]
    by_n = {r["n"]: r for r in records}
    distinct = sorted({s["iso"] for s in stated})
    later = [s for s in stated if s["iso"] > first]
    if len(distinct) < 2 and not later:
        return []
    if len(distinct) >= 2:
        a, b = stated[0], next(s for s in stated if s["iso"] != stated[0]["iso"])
        category = "accident_dates_differ"
        title, expl = flag_templates.render("conflict", category, date_a=a["iso"], date_b=b["iso"], quote_a=a["quote"], quote_b=b["quote"],
                                            provider_a=by_n[a["record_no"]].get("source"), provider_b=by_n[b["record_no"]].get("source"))
        cited = [a, b]
    else:
        a = later[0]
        category = "accident_date_after_treatment"
        # D-055 (T-116 r4): never state paperwork as the first treatment. If every record on the earliest date looks like paperwork, the sentence names
        # that record, says it looks like paperwork, and gives the other reading (the first recorded visit); the paralegal decides.
        extra = {}
        if all(gaps.admin_label(r) for r in first_recs):
            visits = sorted((r for r in enc if not gaps.admin_label(r)), key=lambda r: (r["date_iso"], r["n"]))
            extra = {"record_no": first_recs[0]["n"]}
            if visits:
                extra.update(alt_record_no=visits[0]["n"], alt_date=visits[0]["date_iso"], alt_provider=visits[0].get("source") or "the record",
                             alt_later="also" if a["iso"] > visits[0]["date_iso"] else "not")
        title, expl = flag_templates.render("conflict", category, stated=a["iso"], quote=a["quote"], date=first,
                                            provider_a=first_recs[0].get("source"),
                                            provider_b=first_recs[1].get("source") if len(first_recs) > 1 else None, **extra)
        cited = [a]
    ev = [evidence_span(by_n[s["record_no"]], "excerpt", s["quote"]) for s in cited] + [evidence_span(r, "date") for r in first_recs]
    nos = sorted({s["record_no"] for s in cited} | {r["n"] for r in first_recs})
    return [{"subtype": "accident_date", "category": category, "type": "conflict", "origin": "code", "title": title, "explanation": expl,
             "body_date": a["iso"], "stated_dates": distinct, "first_treatment_date": first, "record_nos": nos, "evidence": ev}]


_TITLES = {"dr", "md", "do", "dc", "np", "pa", "pac", "dpm", "dds", "dpt", "pt", "phd", "rn", "mr", "ms", "mrs"}
_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*\.?")


def _surname(segment: str):
    """Last name-like word of a segment that carries a clinician marker (title/credential or an initial), else None."""
    words = [w.rstrip(".") for w in _WORD.findall(segment)]
    marked = any(w.lower() in _TITLES for w in words) or any(len(w) == 1 and w.isupper() for w in words)
    names = [w for w in words if w.lower() not in _TITLES and len(w) > 1 and w[0].isupper()]
    return names[-1].casefold() if marked and names else None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:46:32.098Z

**tool call — Bash**
````
{
 "command": "sed -n 118,150p app/backend/flag_templates.py; echo ----; grep -n \"def _encounters\" -A 8 app/backend/conflicts.py; echo ----; grep -n \"def admin_label\" -B2 -A 40 app/backend/gaps.py | head -80",
 "description": "Read accident baseline template and encounter and admin_label code"
}
````

### User / tool · 2026-11-02T10:46:32.198Z

**tool result**
````
    return f"Gap of {days} days", f"Gap of {days} days between {a} and {b}.{more}"


def _acc_after_paperwork(v):
    """D-055 (T-116 round 4): the earliest recorded date belongs to a record that looks like paperwork. The sentence never calls it treatment; it names the
    record and gives the other reading (the first recorded visit) so the paralegal decides."""
    prov = "; ".join(p for p in (v.get("provider_a"), v.get("provider_b")) if p)
    stated = f" {_d(v['stated'])}" if v.get("stated") else ""
    quote = f" (“{v['quote']}”)" if v.get("quote") else ""
    first = f"{_d(v.get('date'))} (record {v['record_no']}: {v['provider_a']})" if v.get("provider_a") else f"{_d(v.get('date'))} (record {v['record_no']})"
    if v.get("alt_date"):
        alt = (f"If record {v['record_no']}: {v.get('provider_a') or 'this record'} is paperwork, not a visit, the first recorded visit is {_d(v['alt_date'])} "
               f"(record {v['alt_record_no']}: {v['alt_provider']}), and the stated date is {v['alt_later']} later than it.")
    else:
        alt = f"If record {v['record_no']}: {v.get('provider_a') or 'this record'} is paperwork, not a visit, there is no recorded visit to compare with."
    return ("Stated accident date is later than the earliest record",
            f"Stated accident date{stated}{quote} is later than the earliest recorded date, {first}, which looks like paperwork, not a visit. "
            f"The records disagree; the tool does not choose between them. {alt} Check when treatment actually began before relying on this comparison.")


def _acc_after(v):
    if v.get("record_no"):
        return _acc_after_paperwork(v)
    prov = "; ".join(p for p in (v.get("provider_a"), v.get("provider_b")) if p)
    first = (f", {_d(v['date'])}" + (f" ({prov})" if prov else "")) if v.get("date") else ""
    stated = f" {_d(v['stated'])}" if v.get("stated") else ""
    quote = f" (“{v['quote']}”)" if v.get("quote") else ""
    return ("Stated accident date is later than recorded treatment",
            f"Stated accident date{stated}{quote} is later than the first recorded treatment{first}. "
            "The records disagree; the tool does not choose between them." + "".join(" " + w for w in v.get("warnings") or []))


def _acc_differ(v):
----
12:def _encounters(records):
13-    """D-055: every dated record counts for the earliest date. Whether the earliest one is paperwork is shown beside it (see accident_date_conflicts)."""
14-    return [r for r in records if r.get("date_iso")]
15-
16-
17-def stated_accident_dates(records: list) -> list:
18-    """[{record_no, iso, quote, start, end}]: a lexicon phrase followed within 40 characters by a parsed date, per record excerpt."""
19-    out = []
20-    for r in records:
----
55-
56-
57:def admin_label(rec: dict):
58-    """The plain label of a record whose header looks administrative ("intake form", "billing statement", ...), or None. WARNING ONLY (D-055):
59-    it never changes a gap. It stays conservative so a warning means something: (1) the administrative type is read from the record-type head
60-    (last comma segment) of the header label, or from the record's own first-line title; (2) no visit word appears in the label outside parentheses and
61-    outside the provider name (first segment) once that phrase is removed ("records review visit", "Capital PT, daily note, fax" are visits); (3) the record's text is never consulted
62-    for treatment words (T-116 r5): a bill, EOB, request or form routinely lists diagnoses and services performed, and a warning costs a click while a hidden span
63-    costs the case. Fail toward warning."""
64-    bare = _bare(rec.get("source"))
65-    head = bare.rsplit(",", 1)[-1].strip()
66-    label, rest = None, ""
67-    for lab, rx in _NON_VISIT:
68-        m = rx.search(head)
69-        if m:
70-            label, rest = lab, head[:m.start()] + " " + head[m.end():]
71-            mid = bare[:len(bare) - len(head)].split(",", 1)[1] if "," in bare else ""      # segments after the provider name
72-            rest = mid + " " + rest
73-            break
74-    if not label:
75-        first = (rec.get("excerpt") or "").lstrip().split("\n", 1)[0][:120]
76-        if first and _TITLE.search(first):
77-            label, rest = ("affidavit" if "affidavit" in first.lower() else "intake form"), re.sub(r"new[- ]patient", "", bare.split(",", 1)[-1], flags=re.IGNORECASE)
78-    if not label:
79-        k = ingest.record_kind(bare)           # the ingest lexicon, on the label without parentheticals: same families, still a warning only (D-055)
80-        if k not in ("encounter", "unsplit_text"):
81-            label = {"billing_statement": "billing statement", "phone_note": "phone or message note"}.get(k, "administrative record")
82-            rest = bare.split(",", 1)[1] if "," in bare else ""
83-    if not label or _VISIT_WORD.search(rest):
84-        return None
85-    return label
86-
87-
88-def is_gap(days: int) -> bool:
89-    return days > THRESHOLD_DAYS
90-
91-
92-def compute_gaps(records: list) -> list:
93-    """[{from_date, to_date, from_records, to_records, days, flag}] between consecutive DISTINCT dates of ALL dated records (D-055)."""
94-    by_date = {}
95-    for r in records:
96-        if r.get("date_iso"):
97-            by_date.setdefault(r["date_iso"], []).append(r["n"])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:46:48.424Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r5-probe.py",
 "content": "\"\"\"T-116 round-5 paralegal probe (paralegal-reviewer, final check of f8f358e, D-055 header-only warning).\n\nUsage: .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r5-probe.py <TREE_DIR>\nRun on a git archive copy of HEAD (f8f358e) in the scratchpad. Prints, for each case, the counted gap rows, the flags with their\nwarnings, and the full explanation / alternative sentence, so a human can read the wording.\n\nSections\n  A. the eight paperwork variants (r4 list) as the middle record of a 3/01 visit, 3/20 paperwork, 4/10 visit packet (MID-SPAN),\n     and as the record that ends a 3/01 to 4/10 span (ENDS-GAP). Each variant is run plain and with an added diagnosis, 'performed'\n     or 'seen by' sentence (the r4 suppression words), so every paperwork header is checked with clinical words in its text.\n  B. accident baseline: each of the eight paperwork headers as the earliest record (01-12), then a visit 01-20. Also the same-day\n     case: a paperwork record and a visit both dated 01-12. Checks that no sentence calls a paperwork-headed record 'first recorded\n     treatment' and that the stated date is never resolved.\n  C. r1 to r3 invented-gap check: visit-only labels inside a three-visit packet must count [19, 21] with no flag (run from\n     T-116-paralegal-r3-probe.py output, read separately); this script only covers A and B.\n\"\"\"\nimport sys, os\n\nTREE = sys.argv[1]\nos.chdir(TREE)\nsys.path.insert(0, TREE)\nfrom app.backend import conflicts as C, gaps as G, ingest as I  # noqa: E402\n\nassert G.__file__.startswith(TREE), G.__file__\nHDR = \"SYNTHETIC — invented for evaluation; not real patient data\\n\\n\"\nV = \"Neck pain 5/10. Improved range of motion. Continue home exercise.\"\nADD = [\n    (\"\", \"\"),\n    (\" Diagnosis: M54.2 cervicalgia.\", \"dx line\"),\n    (\" Services performed 03/01/2026.\", \"'performed'\"),\n    (\" Have you been seen by a physician for this problem? Yes.\", \"'seen by'\"),\n]\nPAPER = [  # (header, base text)\n    (\"Capital PT, billing statement\", \"Statement of account. Balance due $740.\"),\n    (\"Capital PT, intake form\", \"Patient-completed intake form. Date of birth, insurance, emergency contact.\"),\n    (\"Capital PT, records request\", \"Please produce all records of treatment on this patient 03/01/2026 through 04/10/2026.\"),\n    (\"Capital PT, affidavit of records custodian\", \"I certify the attached records are true copies.\"),\n    (\"Quoinmere Mutual Health Plan, EOB\", \"Explanation of benefits. Allowed amount $120.\"),\n]\n\n\ndef pk(items):\n    return HDR + \"\".join(f\"=== Record {i} ===\\nDate: {d}\\nSource: {s}\\nExcerpt: \\\"{e}\\\"\\n\\n\" for i, (d, s, e) in enumerate(items, 1))\n\n\ndef flags(items):\n    return G.gap_flags(I.ingest(pk(items))[\"records\"])\n\n\ndef show(f):\n    return (f[\"days\"], bool(f.get(\"conditional\")), [w[\"side\"] for w in f.get(\"endpoint_warnings\") or []],\n            [w.get(\"alternative_days\") for w in f.get(\"endpoint_warnings\") or []])\n\n\nprint(\"tree\", TREE)\nprint(\"== A. paperwork variants, MID-SPAN (3/01 visit, 3/20 paperwork, 4/10 visit) and ENDS-GAP (3/01 visit, 4/10 paperwork)\")\nbad_a = []\nfor src, base in PAPER:\n    for extra, tag in ADD:\n        txt = base + extra\n        mid = flags([(\"2026-03-01\", \"Capital PT, visit 1\", V), (\"2026-03-20\", src, txt), (\"2026-04-10\", \"Capital PT, visit 3\", V)])\n        end = flags([(\"2026-03-01\", \"Capital PT, visit 1\", V), (\"2026-04-10\", src, txt)])\n        name = f\"{src.split(', ', 1)[-1]} [{tag or 'plain'}]\"\n        ok_mid = len(mid) == 1 and show(mid[0])[:3] == (40, True, [\"inside\"]) and show(mid[0])[3] == [40]\n        ok_end = len(end) == 1 and show(end[0])[:3] == (40, False, [\"end\"])\n        if not (ok_mid and ok_end):\n            bad_a.append(name)\n        print(f\"{name:52s} MID={[show(f) for f in mid]} ENDS={[show(f) for f in end]} ok={ok_mid and ok_end}\")\n        if tag in (\"dx line\", \"'performed'\", \"'seen by'\") and src.endswith(\"intake form\"):\n            print(\"   mid explanation:\", mid[0][\"explanation\"][:260] if mid else None)\n        if tag == \"\" and src.endswith(\"billing statement\"):\n            print(\"   mid explanation:\", mid[0][\"explanation\"] if mid else None)\n            print(\"   mid why        :\", mid[0].get(\"why\") if mid else None)\n            print(\"   ends explanation:\", end[0][\"explanation\"] if end else None)\nprint(\"A failures:\", len(bad_a), bad_a)\n\nprint(\"== B. accident baseline (earliest record 01-12 paperwork, visit 01-20)\")\nbad_b = []\nfor src, base in PAPER:\n    for extra, tag in ADD:\n        t = HDR + (f\"=== Record 1 ===\\nDate: 2026-01-12\\nSource: {src}\\nExcerpt: \\\"{base} Date of accident: 2026-01-15.{extra}\\\"\\n\\n\"\n                   \"=== Record 2 ===\\nDate: 2026-01-20\\nSource: Capital PT, initial evaluation\\nExcerpt: \\\"Cervical range of motion reduced approx. 40%.\\\"\\n\")\n        cs = C.accident_date_conflicts(I.ingest(t)[\"records\"])\n        for c in cs:\n            e = c[\"explanation\"]\n            if \"first recorded treatment\" in e or \"looks like paperwork\" not in e:\n                bad_b.append((src, tag))\n            print(f\"{src.split(', ', 1)[-1]:40s} [{tag or 'plain'}] {len(cs)} conflict | 'first recorded treatment' in text: {'first recorded treatment' in e} | \"\n                  f\"'looks like paperwork': {'looks like paperwork' in e}\")\nprint(\"B single-record failures:\", len(bad_b), bad_b)\n\nprint(\"== B2. same-day: paperwork and a visit both dated 01-12 (both record orders)\")\nfor order in (\"paperwork first\", \"visit first\"):\n    recs = [(\"2026-01-12\", \"Capital PT, intake form\", \"Patient-completed intake form. Date of accident: 2026-01-15.\"),\n            (\"2026-01-12\", \"Capital PT, initial evaluation\", \"Cervical range of motion reduced approx. 40%.\")]\n    if order == \"visit first\":\n        recs = recs[::-1]\n    t = HDR + \"\".join(f\"=== Record {i} ===\\nDate: {d}\\nSource: {s}\\nExcerpt: \\\"{e}\\\"\\n\\n\" for i, (d, s, e) in enumerate(recs, 1)) + \\\n        \"=== Record 3 ===\\nDate: 2026-01-20\\nSource: Capital PT, visit 2\\nExcerpt: \\\"Neck pain 5/10.\\\"\\n\"\n    cs = C.accident_date_conflicts(I.ingest(t)[\"records\"])\n    for c in cs:\n        print(f\"[{order}] title: {c['title']}\")\n        print(f\"[{order}] explanation: {c['explanation']}\")\n    if not cs:\n        print(f\"[{order}] no conflict\")\n"
}
````

### User / tool · 2026-11-02T10:46:48.543Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r5-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:46:51.200Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r5-probe.py $S/t116r5/head 2>&1 | tee artifacts/review-evidence/T-116-paralegal-r5-probe.out.txt",
 "description": "Run the r5 probe on the HEAD copy and save output"
}
````

### User / tool · 2026-11-02T10:46:51.407Z

**tool result**
````
tree /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r5/head
== A. paperwork variants, MID-SPAN (3/01 visit, 3/20 paperwork, 4/10 visit) and ENDS-GAP (3/01 visit, 4/10 paperwork)
billing statement [plain]                            MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
   mid explanation: Possible gap of 40 days between March 1, 2026 (Capital PT, visit 1) and April 10, 2026 (Capital PT, visit 3). No gap is counted here because record 2: Capital PT, billing statement (March 20, 2026) falls inside this span and is counted as a visit (19 days, then 21 days). If record 2: Capital PT, billing statement is paperwork, not a visit, the gap would be 40 days (March 1, 2026 to April 10, 2026).
   mid why        : None
   ends explanation: Gap of 40 days between March 1, 2026 (Capital PT, visit 1) and April 10, 2026 (Capital PT, billing statement). This gap ends at record 2: Capital PT, billing statement, which looks like paperwork, not a visit. Check whether treatment continued. If record 2: Capital PT, billing statement is paperwork, not a visit, there would be no visit after it and no gap to measure.
billing statement [dx line]                          MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
billing statement ['performed']                      MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
billing statement ['seen by']                        MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
intake form [plain]                                  MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
intake form [dx line]                                MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
   mid explanation: Possible gap of 40 days between March 1, 2026 (Capital PT, visit 1) and April 10, 2026 (Capital PT, visit 3). No gap is counted here because record 2: Capital PT, intake form (March 20, 2026) falls inside this span and is counted as a visit (19 days, then 21 d
intake form ['performed']                            MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
   mid explanation: Possible gap of 40 days between March 1, 2026 (Capital PT, visit 1) and April 10, 2026 (Capital PT, visit 3). No gap is counted here because record 2: Capital PT, intake form (March 20, 2026) falls inside this span and is counted as a visit (19 days, then 21 d
intake form ['seen by']                              MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
   mid explanation: Possible gap of 40 days between March 1, 2026 (Capital PT, visit 1) and April 10, 2026 (Capital PT, visit 3). No gap is counted here because record 2: Capital PT, intake form (March 20, 2026) falls inside this span and is counted as a visit (19 days, then 21 d
records request [plain]                              MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
records request [dx line]                            MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
records request ['performed']                        MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
records request ['seen by']                          MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
affidavit of records custodian [plain]               MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
affidavit of records custodian [dx line]             MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
affidavit of records custodian ['performed']         MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
affidavit of records custodian ['seen by']           MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
EOB [plain]                                          MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
EOB [dx line]                                        MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
EOB ['performed']                                    MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
EOB ['seen by']                                      MID=[(40, True, ['inside'], [40])] ENDS=[(40, False, ['end'], [None])] ok=True
A failures: 0 []
== B. accident baseline (earliest record 01-12 paperwork, visit 01-20)
billing statement                        [plain] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
billing statement                        [dx line] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
billing statement                        ['performed'] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
billing statement                        ['seen by'] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
intake form                              [plain] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
intake form                              [dx line] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
intake form                              ['performed'] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
intake form                              ['seen by'] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
records request                          [plain] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
records request                          [dx line] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
records request                          ['performed'] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
records request                          ['seen by'] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
affidavit of records custodian           [plain] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
affidavit of records custodian           [dx line] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
affidavit of records custodian           ['performed'] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
affidavit of records custodian           ['seen by'] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
EOB                                      [plain] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
EOB                                      [dx line] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
EOB                                      ['performed'] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
EOB                                      ['seen by'] 1 conflict | 'first recorded treatment' in text: False | 'looks like paperwork': True
B single-record failures: 0 []
== B2. same-day: paperwork and a visit both dated 01-12 (both record orders)
[paperwork first] title: Stated accident date is later than recorded treatment
[paperwork first] explanation: Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form; Capital PT, initial evaluation). The records disagree; the tool does not choose between them.
[visit first] title: Stated accident date is later than recorded treatment
[visit first] explanation: Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the first recorded treatment, January 12, 2026 (Capital PT, initial evaluation; Capital PT, intake form). The records disagree; the tool does not choose between them.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:47:06.111Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np = \"artifacts/review-evidence/T-116-paralegal-r5-probe.py\"\ns = open(p, encoding=\"utf-8\").read()\nold = \"        if not (ok_mid and ok_end):\\n            bad_a.append(name)\\n\"\nnew = (\"        ok_sent = (len(mid) == 1 and f\\\"the gap would be 40 days\\\" in mid[0][\\\"explanation\\\"]\\n\"\n       \"                   and len(end) == 1 and \\\"there would be no visit after it\\\" in end[0][\\\"explanation\\\"])\\n\"\n       \"        if not (ok_mid and ok_end and ok_sent):\\n            bad_a.append(name)\\n\"\n       \"        sent_ok.append(ok_sent)\\n\")\nassert s.count(old) == 1\ns = s.replace(old, new)\ns = s.replace(\"bad_a = []\\n\", \"bad_a = []\\nsent_ok = []\\n\", 1)\ns = s.replace('print(\"A failures:\", len(bad_a), bad_a)', 'print(\"A failures:\", len(bad_a), bad_a)\\nprint(\"A variants:\", len(sent_ok), \"with both alternative sentences (mid: the gap would be 40 days; ends: no visit after it):\", sum(sent_ok))')\nopen(p, \"w\", encoding=\"utf-8\").write(s)\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r5-probe.py $S/t116r5/head > artifacts/review-evidence/T-116-paralegal-r5-probe.out.txt 2>&1; echo \"exit=$?\"; grep -n \"A failures\\|A variants\\|B single\\|B2\\|paperwork first\\|visit first\" artifacts/review-evidence/T-116-paralegal-r5-probe.out.txt | cut -c1-220; echo ---; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r5-probe.py $S/t116r5/pre > $S/t116r5/out/r5-probe-pre.txt 2>&1; grep -n \"A failures\\|A variants\\|B single\" $S/t116r5/out/r5-probe-pre.txt | cut -c1-200",
 "description": "Add sentence assertions to r5 probe, rerun on HEAD and pre"
}
````

### User / tool · 2026-11-02T10:47:06.476Z

**tool result**
````
exit=0
29:A failures: 0 []
30:A variants: 20 with both alternative sentences (mid: the gap would be 40 days; ends: no visit after it): 20
52:B single-record failures: 0 []
53:== B2. same-day: paperwork and a visit both dated 01-12 (both record orders)
54:[paperwork first] title: Stated accident date is later than recorded treatment
55:[paperwork first] explanation: Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form; Capital PT, initial eval
56:[visit first] title: Stated accident date is later than recorded treatment
57:[visit first] explanation: Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the first recorded treatment, January 12, 2026 (Capital PT, initial evaluation; Capital PT, intake fo
---
29:A failures: 20 ['billing statement [plain]', 'billing statement [dx line]', "billing statement ['performed']", "billing statement ['seen by']", 'intake form [plain]', 'intake form [dx line]', "inta
30:A variants: 20 with both alternative sentences (mid: the gap would be 40 days; ends: no visit after it): 0
40:B single-record failures: 8 [('Capital PT, intake form', ''), ('Capital PT, intake form', 'dx line'), ('Capital PT, intake form', "'performed'"), ('Capital PT, intake form', "'seen by'"), ('Capital
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:47:11.011Z

**tool call — Bash**
````
{
 "command": "grep -rn \"R-FL-2\\|D-017\" memory/ spec/ docs/ 2>/dev/null | cut -c1-400 | head -12",
 "description": "Find the text of D-017 and R-FL-2 for severity grounding"
}
````

### User / tool · 2026-11-02T10:47:11.119Z

**tool result**
````
memory/GLOSSARY.md:24:- **Delay in treatment (delay to first treatment)** — time from the accident to the first medical visit; adjusters' first check. The tool shows only "first recorded treatment" and never computes the delay (D-017). Source: AA A12, src 1, 16.
memory/ORCHESTRATOR_DECISIONS.md:25:| D-017 | The tool never picks between conflicting accident dates and never computes "delay from the accident". It may state "first recorded treatment: <earliest record date>". Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides. | Must-not: merge the two accident dates; adverse facts are the attorne
memory/ORCHESTRATOR_DECISIONS.md:26:| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS 
memory/SCOPE_CUTS.md:34:| debt | T-017 accepted with documented debt after 3 rounds (§7.4) | planning-doc minors after 3 rounds: R-FL-2/R-CO-9/R-EX-4 pass conditions live in card AC (T-033/T-036, T-034, T-041); budget total + cut trigger added | see card | M1 |
spec/REQUIREMENTS.md:66:| R-FL-2 | **Conflicting facts.** Flag facts that conflict across records, citing both excerpts. | Sample must raise (a) accident date 2026-01-09 (records 1, 2) vs "Date of accident per intake form: 2026-01-19" (record 7), shown as a conflict and **not merged**, with the records cited (R-EX-4) and no choice made between the dates or any "delay from the accident" computed; t
spec/REQUIREMENTS.md:122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (matches the golde
spec/REQUIREMENTS.md:196:6. **Medical or legal judgment.** No diagnosis, severity rating, causation opinion or statement of what a record "means." Flags point at the record's own words. Whether a flagged sentence goes out in the letter is the attorney's call (D-012), not the tool's. The tool never picks between conflicting accident dates and never computes delay from the accident (D-017).
memory/DECISIONS.md:286:  - Code verifies the excerpt, computes offsets and renders `title` and `explanation` from a template per category (`app/backend/flag_templates.py`; a unit test asserts every category has one), for example "Wording that could be used to question causation in {source} ({date}): “{excerpt}”". Delay to first treatment is never computed (D-017).
memory/DECISIONS.md:292:- Status: accepted (round 2; resolves staff F4 and F10, privacy f2 finding; R-FL-2(a); amended by ADR-019 and ADR-020)
memory/DECISIONS.md:297:  - Evidence has at least two items: the stated-date phrase span, and the `Date:` header line of every record on the earliest date. Template (D-017: the tool never picks a date and never computes a delay from the accident): "Stated accident date {stated} (“{phrase}”) is later than the first recorded treatment, {earliest} ({source A}; {source B}). The records disagree; t
docs/M2M3_COVERAGE.md:42:| R-FL-2 | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:47:21.921Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && ls -a $S/t116r5/head | head -30; ls $S/t116r5/head/tests | head; cat $S/t116r5/head/pytest.ini 2>/dev/null; cat $S/t116r5/head/pyproject.toml 2>/dev/null | grep -A5 \"pytest\" | head -12; cat $S/t116r5/head/tests/conftest.py 2>/dev/null | head -20; cat $S/t116r5/head/tests/unit/conftest.py 2>/dev/null | head -20",
 "description": "Inspect pytest config and conftest in the HEAD copy"
}
````

### User / tool · 2026-11-02T10:47:22.037Z

**tool result**
````
.
..
.claude
.gitignore
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
__init__.py
conftest.py
e2e
fixtures
unit
"""Puts the repo root on sys.path so tests import `app.*` (tests only; no key, no network: fixture backend only)."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:47:26.917Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r5/head && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q tests/unit -k gap -p no:cacheprovider 2>&1 | tail -5; echo \"exit=${PIPESTATUS[0]}\"; echo ----; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q tests/unit/test_t116_gap_endpoints.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_t116_r5_header_only_warning.py -p no:cacheprovider 2>&1 | tail -5; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run gap-filtered unit tests and T-116 test files on HEAD copy"
}
````

### User / tool · 2026-11-02T10:47:33.919Z

**tool result**
````
........................................................................ [ 26%]
........................................................................ [ 53%]
........................................................................ [ 80%]
......................................................                   [100%]
270 passed, 2500 deselected in 4.73s
exit=0
----
........................................................................ [ 39%]
........................................................................ [ 78%]
........................................                                 [100%]
184 passed in 1.55s
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:47:41.417Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k gap -p no:cacheprovider 2>&1 | tail -2; .venv/bin/python -m pytest -q tests/unit/test_t116_gap_endpoints.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_t116_r5_header_only_warning.py -p no:cacheprovider 2>&1 | tail -2; echo ----; cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r5/head && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q tests/unit/test_t116_r5_header_only_warning.py -p no:cacheprovider -v 2>&1 | grep -c PASSED; ls /Users/arsis/zlayt-pm-project/tests/unit | grep -c t116; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"import sys\" && echo ok",
 "description": "Run the same pytest selection in project tree and count r5 passes"
}
````

### User / tool · 2026-11-02T10:47:48.677Z

**tool result**
````
......................................................                   [100%]
270 passed, 2500 deselected in 4.73s
........................................                                 [100%]
184 passed in 1.49s
----
0
3
ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:47:55.124Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r4-packet-flags.py $S/t116r5/out/head.json $S/t116r5/out/pre.json 2>&1 | head -40 | cut -c1-260; echo ----; .venv/bin/python -I -c \"\nimport json,sys\nH=json.load(open('$S/t116r5/out/head.json')); P=json.load(open('$S/t116r5/out/pre.json'))\npre={p['packet']:p for p in P['packets']}\nsame=0; diff=[]\nfor b in H['packets']:\n    a=pre[b['packet']]\n    hf=[(f['from'],f['to'],f['days'],f['record_nos']) for f in b['flags']]\n    pf=[(f['from'],f['to'],f['days'],f['record_nos']) for f in a['flags']]\n    if hf==pf: same+=1\n    else: diff.append((b['packet'],pf,hf))\nprint('packets with identical counted flag lists HEAD vs pre:', same, 'of', len(H['packets']))\nfor d in diff: print(d[0], 'pre', [x[:3] for x in d[1]], 'head', [x[:3] for x in d[2]])\nprint('HEAD packet statuses:', sorted(set(p['status'] for p in H['packets'])))\n\"",
 "description": "Compare packet flags HEAD vs pre-T-116 and count identical lists"
}
````

### User / tool · 2026-11-02T10:47:55.268Z

**tool result**
````
== every golden/pre flagged gap vs HEAD (shown as counted flag, alt of a warning, or conditional)
case_lib10_eob_ub04_cms1500 OK pre [('2026-07-08', '2026-08-26', 49)] exp [('2026-07-08', '2026-08-26', 49)] head [('2026-07-14', '2026-08-26', 43)] shown [(('2026-07-08', '2026-08-26', 49), True)]

# case_02_gap_boundaries 2028-03-09 2028-04-09 31 [3, 4]
   Gap of 31 days between March 9, 2028 (Thistlewick Orthopedics, Dr. Beatrix Quillon) and April 9, 2028 (Thistlewick Orthopedics, Dr. Beatrix Quillon).

# case_02_gap_boundaries 2028-05-09 2028-06-09 31 [5, 6]
   Gap of 31 days between May 9, 2028 (Thistlewick Orthopedics, Dr. Beatrix Quillon) and June 9, 2028 (Thistlewick Orthopedics, Dr. Beatrix Quillon).

# case_02_gap_boundaries 2028-07-09 2028-08-09 31 [7, 8]
   Gap of 31 days between July 9, 2028 (Thistlewick Orthopedics, Dr. Beatrix Quillon) and August 9, 2028 (Thistlewick Orthopedics, Dr. Beatrix Quillon).

# case_07_prompt_injection 2026-03-16 2026-05-04 49 [3, 4]
   Gap of 49 days between March 16, 2026 (Bumblethorpe Physical Therapy, visit 1) and May 4, 2026 (Bumblethorpe Physical Therapy, visit 2).

# case_09_nonvisit_hides_gap 2026-02-02 2026-03-30 56 [1, 2, 3, 4]
   Possible gap of 56 days between February 2, 2026 (Hobbleton Family Clinic, visit) and March 30, 2026 (Hobbleton Family Clinic, visit). No gap is counted here because record 2: Hobbleton Family Clinic, billing statement (March 1, 2026) and record 3: Hobbleto

# case_lib01_er_only_then_gap 2026-02-14 2026-03-30 44 [1, 2, 3]
   Gap of 44 days between February 14, 2026 (Marrowgate General ED) and March 30, 2026 (Dr. Imelda Quarrington, primary care).

# case_lib02_slip_fall_prior_knee 2026-05-04 2026-06-22 49 [6, 7]
   Gap of 49 days between May 4, 2026 (Cedar Run Physical Therapy, initial evaluation) and June 22, 2026 (Cedar Run Physical Therapy, visit 10).

# case_lib03_truck_rear_end_chiro 2026-06-15 2026-07-20 35 [6, 7]
   Gap of 35 days between June 15, 2026 (Thimbleby Chiropractic, discharge) and July 20, 2026 (Redhaven Imaging, lumbar MRI).

# case_lib04_dog_bite_scar_revision 2025-10-18 2025-12-13 56 [4, 5]
   Gap of 56 days between October 18, 2025 (Dr. Odalys Pennywhistle, plastic surgery) and December 13, 2025 (Dr. Odalys Pennywhistle, plastic surgery).

# case_lib04_dog_bite_scar_revision 2025-12-13 2026-09-12 273 [5, 6]
   Gap of 273 days between December 13, 2025 (Dr. Odalys Pennywhistle, plastic surgery) and September 12, 2026 (Dr. Odalys Pennywhistle, plastic surgery, operative note).

# case_lib05_pedestrian_orif_hardware 2026-03-05 2026-04-23 49 [5, 6]
   Gap of 49 days between March 5, 2026 (Mosswood Physical Therapy, initial evaluation) and April 23, 2026 (Mosswood Physical Therapy, visit 12).

# case_lib05_pedestrian_orif_hardware 2026-04-23 2026-08-20 119 [6, 7]
   Gap of 119 days between April 23, 2026 (Mosswood Physical Therapy, visit 12) and August 20, 2026 (Dr. Casimir Voss, orthopedic surgery, clinic).

# case_lib06_lop_billed_vs_adjusted 2026-05-13 2026-06-17 35 [3, 4, 5]
----
packets with identical counted flag lists HEAD vs pre: 22 of 25
case_09_nonvisit_hides_gap pre [('2026-02-02', '2026-03-30', 56)] head [('2026-02-02', '2026-03-30', 56)]
case_lib06_lop_billed_vs_adjusted pre [('2026-05-13', '2026-06-17', 35), ('2026-07-08', '2026-09-02', 56)] head [('2026-05-13', '2026-06-17', 35), ('2026-07-08', '2026-09-02', 56)]
case_lib10_eob_ub04_cms1500 pre [('2026-07-08', '2026-08-26', 49)] head [('2026-07-14', '2026-08-26', 43)]
HEAD packet statuses: ['done', 'done_with_errors']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:48:03.480Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r4-packet-flags.py $S/t116r5/out/head.json $S/t116r5/out/pre.json > $S/t116r5/out/packet-flags-head-vs-pre.txt 2>&1; grep -c \"MISSING\" $S/t116r5/out/packet-flags-head-vs-pre.txt; grep -c \" OK \" $S/t116r5/out/packet-flags-head-vs-pre.txt; grep \"^case_\\|^[a-z_0-9]* OK\\|^[a-z_0-9]* MISSING\" $S/t116r5/out/packet-flags-head-vs-pre.txt | cut -c1-120 | head -10; echo ---; .venv/bin/python -I -c \"\nimport json\nH=json.load(open('$S/t116r5/out/head.json'))\nfor b in H['packets']:\n    for f in b['flags']:\n        if b['packet'] in ('case_09_nonvisit_hides_gap','case_lib06_lop_billed_vs_adjusted','case_lib10_eob_ub04_cms1500'):\n            print(b['packet'], f['from'], f['to'], f['days'], f['record_nos'], '|', f['explanation'][:200])\n\" ",
 "description": "Confirm no MISSING packet rows and show conditional packet explanations"
}
````

### User / tool · 2026-11-02T10:48:03.664Z

**tool result**
````
0
1
case_lib10_eob_ub04_cms1500 OK pre [('2026-07-08', '2026-08-26', 49)] exp [('2026-07-08', '2026-08-26', 49)] head [('202
---
case_09_nonvisit_hides_gap 2026-02-02 2026-03-30 56 [1, 2, 3, 4] | Possible gap of 56 days between February 2, 2026 (Hobbleton Family Clinic, visit) and March 30, 2026 (Hobbleton Family Clinic, visit). No gap is counted here because record 2: Hobbleton Family Clinic,
case_lib06_lop_billed_vs_adjusted 2026-05-13 2026-06-17 35 [3, 4, 5] | Possible gap of 35 days between May 13, 2026 (Gannet and Moor Injury Clinic, new patient) and June 17, 2026 (Larchmont Ridge Imaging, right shoulder MRI). No gap is counted here because record 4: Gann
case_lib06_lop_billed_vs_adjusted 2026-07-08 2026-09-02 56 [6, 7] | Gap of 56 days between July 8, 2026 (Gannet and Moor Injury Clinic, injection visit) and September 2, 2026 (Gannet and Moor Injury Clinic, follow-up).
case_lib10_eob_ub04_cms1500 2026-07-14 2026-08-26 43 [8, 9] | Gap of 43 days between July 14, 2026 (Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)) and August 26, 2026 (Dr. Ignatius Wardlaw, orthopedics, follow-up). This gap starts at record 8: Wardlaw Ort
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:48:12.994Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-116-paralegal-r5-headers.py <<'EOF'\n\"\"\"T-116 r5 paralegal probe: more paperwork-looking headers as the earliest record (01-12), visit on 01-20, through\nconflicts.accident_date_conflicts. Prints whether the sentence says 'first recorded treatment' (a paperwork record called treatment)\nor 'looks like paperwork'. Usage: .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r5-headers.py <TREE_DIR>\"\"\"\nimport sys, os\nTREE = sys.argv[1]; os.chdir(TREE); sys.path.insert(0, TREE)\nfrom app.backend import conflicts as C, gaps as G, ingest as I\nHDR = \"SYNTHETIC — invented for evaluation; not real patient data\\n\\n\"\nHEADERS = [\"Capital PT, letter of protection\", \"Capital PT, CMS-1500 claim\", \"Capital PT, ledger\", \"Capital PT, questionnaire\",\n           \"Capital PT, pain diagram\", \"Capital PT, authorization request\", \"Capital PT, records cover sheet\", \"Capital PT, correspondence\",\n           \"Capital PT, intake form (faxed)\", \"Capital PT, attorney letter\", \"Capital PT, medical records request\"]\nfor h in HEADERS:\n    t = HDR + (f\"=== Record 1 ===\\nDate: 2026-01-12\\nSource: {h}\\nExcerpt: \\\"Date of accident: 2026-01-15.\\\"\\n\\n\"\n               \"=== Record 2 ===\\nDate: 2026-01-20\\nSource: Capital PT, initial evaluation\\nExcerpt: \\\"Cervical range of motion reduced approx. 40%.\\\"\\n\")\n    recs = I.ingest(t)[\"records\"]\n    cs = C.accident_date_conflicts(recs)\n    lab = G.admin_label(recs[0])\n    e = cs[0][\"explanation\"] if cs else \"(no conflict)\"\n    print(f\"{h:38s} admin_label={lab!r:24s} first_recorded_treatment={'first recorded treatment' in e!s:5s} looks_like_paperwork={'looks like paperwork' in e}\")\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r5-headers.py $S/t116r5/head 2>&1 | tee artifacts/review-evidence/T-116-paralegal-r5-headers.out.txt",
 "description": "Probe extra paperwork-looking headers in the accident baseline"
}
````

### User / tool · 2026-11-02T10:48:13.198Z

**tool result**
````
Capital PT, letter of protection       admin_label='letter or correspondence' first_recorded_treatment=False looks_like_paperwork=True
Capital PT, CMS-1500 claim             admin_label='claim form'             first_recorded_treatment=False looks_like_paperwork=True
Capital PT, ledger                     admin_label='ledger'                 first_recorded_treatment=False looks_like_paperwork=True
Capital PT, questionnaire              admin_label=None                     first_recorded_treatment=True  looks_like_paperwork=False
Capital PT, pain diagram               admin_label='intake form'            first_recorded_treatment=False looks_like_paperwork=True
Capital PT, authorization request      admin_label=None                     first_recorded_treatment=True  looks_like_paperwork=False
Capital PT, records cover sheet        admin_label='affidavit'              first_recorded_treatment=False looks_like_paperwork=True
Capital PT, correspondence             admin_label='letter or correspondence' first_recorded_treatment=False looks_like_paperwork=True
Capital PT, intake form (faxed)        admin_label='intake form'            first_recorded_treatment=False looks_like_paperwork=True
Capital PT, attorney letter            admin_label='letter or correspondence' first_recorded_treatment=False looks_like_paperwork=True
Capital PT, medical records request    admin_label='records request'        first_recorded_treatment=False looks_like_paperwork=True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:48:23.032Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && grep -n \"excluded from gap arithmetic\" $S/t116r5/head/app/llm/lexicon.yaml | cut -c1-200; echo ---; grep -rn \"gap_excluded_records\" $S/t116r5/head/evals/golden/*.json 2>/dev/null | head -3 | cut -c1-160; echo ---; grep -n \"[0-9]\" $S/t116r5/out/packet-flags-head-vs-pre.txt | head -0; echo \"---- golden expected count sample\"; ls $S/t116r5/head/evals/golden | head -30 | tr '\\n' ' '",
 "description": "Check r4 minor F3 status: lexicon text and golden gap_excluded fields"
}
````

### User / tool · 2026-11-02T10:48:23.149Z

**tool result**
````
1282:    consumer: 'ADR-010 / D-003: records whose source label matches are excluded from gap arithmetic. They still become entries.'
---
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d2
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d2
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d2
---
head: illegal line count -- 0
---- golden expected count sample
README.md case_01_date_formats.expected.json case_01_date_formats.txt case_02_gap_boundaries.expected.json case_02_gap_boundaries.txt case_03_rate_and_ocr.expected.json case_03_rate_and_ocr.txt case_04_duplicates_no_amounts.expected.json case_04_duplicates_no_amounts.txt case_05_provider_conflict.expected.json case_05_provider_conflict.txt case_06_subtle_pre_existing.expected.json case_06_subtle_pre_existing.txt case_07_prompt_injection.expected.json case_07_prompt_injection.txt case_08_diagnosis_temptation.expected.json case_08_diagnosis_temptation.txt case_09_nonvisit_hides_gap.expected.json case_09_nonvisit_hides_gap.txt check_golden.py hallucinations.jsonl hallucinations_controls.jsonl judge_controls.CHANGELOG.md judge_controls.jsonl judge_controls_heldout.jsonl sample.expected.json sample.export.expected.txt sample.txt unsplit_paste.split.json unsplit_paste.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:48:29.333Z

**tool call — Bash**
````
{
 "command": "head -12 artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.py | cut -c1-220; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.py $S/t116r5/head > $S/t116r5/out/warn-and-api.head.txt 2>&1; echo \"exit=$?\"; diff <(sed \"s#$S/t116r5/head#TREE#g\" $S/t116r5/out/warn-and-api.head.txt) <(sed \"s#/Users/arsis/zlayt-pm-project#TREE#g\" artifacts/review-evidence/T-116-paralegal-r4-warn-and-api.head.out.txt) | head -30; echo \"diff_exit=$?\"",
 "description": "Re-run r3 warning and API probe on HEAD and diff against r4 output"
}
````

### User / tool · 2026-11-02T10:48:30.336Z

**tool result**
````
"""T-116 round-3 paralegal probe: where a D-055 warning applies, and lib09 driven through the API (ingest, then confirm record 4 as 5 March).

Usage: .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.py <TREE_DIR>
Part 1 (pure code, constructed packets through ingest.ingest and gaps.gap_flags): a gap that ENDS at a paperwork-looking encounter
(warning expected), a gap that STARTS at one (warning expected), and a paperwork-looking record dated inside an unflagged span.
Part 2 (lib09 through the FastAPI TestClient, fixture backend): gap before and after confirming record 4, with every endpoint warning.
"""
import sys, os, time, tempfile, json

TREE = sys.argv[1]
os.chdir(TREE)
sys.path.insert(0, TREE)
exit=0
diff_exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:48:34.485Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && sed \"s#$S/t116r5/head#TREE#g\" $S/t116r5/out/warn-and-api.head.txt > $S/t116r5/out/wa-norm.txt && sed \"s#/Users/arsis/zlayt-pm-project#TREE#g\" artifacts/review-evidence/T-116-paralegal-r4-warn-and-api.head.out.txt > $S/t116r5/out/wa-r4-norm.txt; diff $S/t116r5/out/wa-norm.txt $S/t116r5/out/wa-r4-norm.txt; echo \"diff_exit=$?\"; wc -l $S/t116r5/out/wa-norm.txt; grep -n \"^\\[W\" $S/t116r5/out/wa-norm.txt | cut -c1-160; grep -n \"tree\\|module\" $S/t116r5/out/wa-norm.txt | head -3 | cut -c1-120",
 "description": "Diff normalized r3 warning/API output against r4 record"
}
````

### User / tool · 2026-11-02T10:48:34.598Z

**tool result**
````
diff_exit=0
      56 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r5/out/wa-norm.txt
2:[W1 gap ENDS at 'Capital PT, intake form' (encounter kind)] kinds: [(1, '2026-03-01', 'encounter'), (2, '2026-04-10', 'encounter')]
6:[W2 gap STARTS at 'Capital PT, intake form' (encounter kind)] kinds: [(1, '2026-03-01', 'encounter'), (2, '2026-04-10', 'encounter')]
10:[W3 intake form dated INSIDE a 40-day span with no visit] kinds: [(1, '2026-03-01', 'encounter'), (2, '2026-03-20', 'encounter'), (3, '2026-04-10', 'encounte
14:[W4 visit with a paperwork word, ends the span (records-request copy, visit wording)] kinds: [(1, '2026-03-01', 'encounter'), (2, '2026-04-10', 'records_admi
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:48:40.515Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/paralegal-reviewer/t116-gap-endpoint-patterns.md | head -60; echo ----; cat .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md | head -30",
 "description": "Read existing T-116 memory and tooling quirks notes"
}
````

### User / tool · 2026-11-02T10:48:40.602Z

**tool result**
````
---
name: t116-gap-endpoint-patterns
description: T-116 gap endpoints through r3 (8673326, 2026-11-02, verdict fail): gaps.py exclusion gone but ingest record_kind still drops visits by label; accident baseline still counts intake forms; lib11 truth flipped to stale
metadata:
  type: project
---

State at r3 (8673326, verdict fail, 2 blockers, 2 majors; review reviews/T-116-paralegal-r3.md): the gaps.py label exclusion is gone and gap
dates, days, flags and endpoints equal pre-T-116 (3e3f3b7) on 25 packets, 60 label runs and 10 Appendix A fax variants. The warning works where
a gap starts or ends at an intake form encounter (lib09 after confirm: 40 days, start warning with record 4 and verbatim header).

Recurring pattern: removing a guess from one layer leaves the same guess one layer down. At r3 the gaps.py regex was removed, but
ingest.record_kind (ingest.py:214-221) applies lexicon `non_encounter` to the whole Source label, and gaps.compute_gaps (gaps.py:104) keeps
kind == "encounter". So "Capital PT, initial evaluation, correspondence", "Office visit / records request", "Dr. Lee, chiropractic, visit 3 -
records request copy", "Capital PT, visit 5 (ledger balance reviewed)", "Austin Imaging, MRI cervical spine (records request attached)" still
give an invented 40-day gap, and a visit with "records request copy" as the endpoint hides a span entirely (no flag). Before any "fixed"
verdict, grep every layer that can exclude (ingest kind, lexicon, gaps) and probe with the same labels.

Recurring pattern: "identical to pre-T-116" is not the D-055 test when the pre behaviour is itself the guess. D-055 premise ("as before T-116
gap math runs over all dated records") is wrong: pre-T-116 already dropped non-encounter kinds. Test against the decision text, not only pre.

Recurring pattern: an intake form is kind "encounter" at ingest. It becomes a gap endpoint, so it (a) warns when the gap ends there (correct)
and (b) hides a 40-day span when dated inside it with no visit (W3, no warning). Open as major F4 pending the D-055 reading.

Recurring pattern: the accident-date baseline (conflicts._encounters, conflicts.py:12-14, used by accident_date_conflicts) and the accident
year (pipeline._accident_year, pipeline.py:258) still count the intake form as "first recorded treatment". r3 added a warning appended after the
false sentence (not a fix). T-113's note (board/cards/T-113.md:29) moves "T-116 F3" to conflict candidates; the deterministic baseline is not
candidate code (conflict_candidates.py calls neither). Erratum: r3 review says T-113 "does not cover" it and that grep returns 1 from H3V5; the
single match is line 29 (the note). Check grep output lines before claiming what a card does not cover.

Recurring pattern: lib11 truth flips. T-118 (78450f6) applied the r2 edits (record 6 phone_note, excluded [4,6,9], rows [5]/[5]); the product
at r3 gives [5,6]/[5,6] with record 6 encounter. validate_library.py and check_golden.py exit 0 on HEAD; gap test compares dates only
(test_t116 lines 163-170); legacy_gaps (lines 60-64) copies the same kind filter, so it cannot see exclusion by kind (minor F5).

Probe pitfall: the "pre-T-116" tree is `git rev-parse <first-T116-commit>^` = 3e3f3b7 (fa95e58 is older and has no library packets). Scripts that
call gaps.non_visit_label fail on HEAD (removed); the r3 probe uses only ingest.ingest, compute_gaps, gap_flags, conflicts.accident_date_conflicts.

Why: T-116 r1 (fail, F1 blocker label substring), r2 (fail, F1 narrowed blocker, F3 blocker), r3 (fail, F1 kind path blocker, F2 F3 blocker,
F3 lib11 major, F4 mid-span major). Card status is in the board.
How to apply: on any gap, endpoint or truth change, run artifacts/review-evidence/T-116-paralegal-r3-probe.py on the pre parent and HEAD, then
compare; restore the parent's truth file on a scratch copy to confirm a gate fails; check every exclusion layer, not only the one edited.

Related: [[golden-set-recurring-findings]], [[t114-rates-gap-patterns]], [[t118-lib11-truth-patterns]], [[reviewer-tooling-quirks]].

## r4 (8b4ff11, 2026-11-02, verdict fail: 1 blocker, 2 minors, 1 nit; reviews/T-116-paralegal-r4.md)
r3 blockers fixed: compute_gaps reads every dated record, 60/60 label runs no invented gap, conditional "Possible gap of N days" flag and
"If record N: <header> is paperwork, not a visit, the gap would be X days" work. lib10 49 -> 43 (CMS-1500 dated 07-14, excerpt states DOS 07/08), alt 49 shown: correct.
New blocker pattern: the warning is gated by gaps.admin_label -> _has_treatment_evidence (regex on excerpt: Dx:, performed, seen by, Plan:). Bills/EOBs/forms
with those words get no warning, no alternative, no conditional flag; a mid-span 40-day span vanishes (pre-T-116 showed it). Same gate feeds the accident baseline.
Recurring: every time a guess is removed, check the next gate (warning suppression) with the same probe; use mutation: append one clinical-sounding sentence to a paperwork excerpt.
Probes: artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py, -packet-dx-line.py, -baseline.py (reuse r3-probe.py for labels).
----
---
name: reviewer-tooling-quirks
description: Hooks that block reviewer shell commands in Zlayt PM (board-guard on sed -i, git-guard on python -c with backticks) and the workaround
metadata:
  type: feedback
---

Don't edit review files with `sed -i` (board-guard blocks it), and don't run `python3 -c` with backticks or regex escapes (git-guard can't parse it). Use the Edit tool for review files, and put checks in a script under artifacts/review-evidence/ run with `.venv/bin/python`.

**Why:** Both were blocked during the T-013 r2 review (2026-11-01). A script also leaves reproducible evidence the review can cite.

**How to apply:** For every review, put JSON/verdict validation in artifacts/review-evidence/<card>-*-jsoncheck.py. Related: [[spec-review-patterns]].

## T-077/T-078 r2 additions (2026-11-01)
- `grep -E` with long `.{0,120}` patterns over fetched HTML fails in ugrep ("exceeds complexity limits"). Strip tags and search in a python script under artifacts/review-evidence/.
- `timeout` is not installed on this macOS host; drop it and rely on urllib's timeout argument.
- A `mktemp` + `rmdir` combo inside a Bash call tripped board-guard. Keep Bash calls to one purpose.
- Fetched pages redirected to the session scratchpad were not blocked by the hook, but the persona rule says reviewers write only under reviews/, artifacts/review-evidence/ and memory. Write fetch dumps to artifacts/review-evidence/ and say so in the review.
- The NUCC and CMS PDFs download fine with urllib; write the PDF into review-evidence, run `pdftotext -layout`, then delete the PDF and text.

## T-077 r3 additions (2026-11-01)
- `reviewer-write-guard` makes review files append-only: once `reviews/<card>-<persona>-rN.md` exists, Edit is refused ("reviews are append-only"). Proof-read the review (grep every line ref and quote) BEFORE the single Write; a stale ref cannot be fixed afterwards without a new file.
- A bash `python3 -c` with `\`\`\`` and `\d` escapes was denied by git-guard ("could not parse command safely (No escaped character)"). Move any JSON parse into a Write-created script under artifacts/review-evidence/ and run it.

## T-114 additions (2026-11-02)
- board-guard reads a redirect target written as `$VAR/file` inside the same command as "writes outside reviews/"; the same redirect with a literal absolute path passes. Use literal paths for `> file` redirects, and put server start/stop in their own calls.
- git-guard rejected a `kill $(cat pidfile)` chain with echo quotes ("No closing quotation"). Use the PID number directly.
- `timeout` is not installed (already noted); `python3 tools/board.py validate reviews/<file>` works and printed "ok (1 file(s))".

## T-116 r2 additions (2026-11-02)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:48:46.133Z

**tool call — Bash**
````
{
 "command": "grep -n \"_NON_VISIT\\s*=\" -A 8 app/backend/gaps.py | cut -c1-220; echo ---; grep -n \"all(gaps.admin_label\\|extra = {}\\|first_recs = \\|is later than the first recorded treatment\" app/backend/conflicts.py app/backend/flag_templates.py | cut -c1-200; echo ---; grep -n \"questionnaire\\|authorization\" app/llm/lexicon.yaml | head -5 | cut -c1-200",
 "description": "Get line numbers for baseline branch and header vocabulary in code"
}
````

### User / tool · 2026-11-02T10:48:46.252Z

**tool result**
````
18:_NON_VISIT = [(label, re.compile(rx, re.IGNORECASE)) for label, rx in (
19-    ("intake form", r"\b(?:(?:new[- ]patient\s+)?(?:intake|registration|admission|admissions|check-?in)\s+(?:form|forms|packet|paperwork|questionnaire|sheet)"
20-                    r"|new[- ]patient\s+(?:paperwork|forms?|questionnaire|packet)|patient\s+(?:information|history|health\s+history|registration)\s+(?:form|questionnaire|sheet)"
21-                    r"|health\s+history\s+(?:form|questionnaire)|pain\s+(?:diagram|questionnaire)|consent\s+form|assignment\s+of\s+benefits)\b"
22-                    r"|\bformulario\s+de\s+(?:admisi[oó]n|ingreso|registro)\b|\bhoja\s+de\s+(?:admisi[oó]n|ingreso)\b"),
23-    ("explanation of benefits", r"\b(?:explanation\s+of\s+benefits|EOB|remittance(?:\s+advice)?)\b"),
24-    ("claim form", r"\b(?:UB-?04|CMS-?1500|HCFA|claim\s+form)\b"),
25-    ("ledger", r"\b(?:ledger|payment\s+(?:history|record)|account\s+history)\b"),
26-    ("billing statement", r"\b(?:billing|statement\s+of\s+account|account\s+statement|itemi[sz]ed\s+(?:bill|statement|charges)|invoice|superbill|balance\s+due)\b|^statement$"
---
app/backend/flag_templates.py:146:            f"Stated accident date{stated}{quote} is later than the first recorded treatment{first}. "
app/backend/conflicts.py:47:    first_recs = [r for r in enc if r["date_iso"] == first]
app/backend/conflicts.py:64:        extra = {}
app/backend/conflicts.py:65:        if all(gaps.admin_label(r) for r in first_recs):
---
771:  pattern: '\bper\s+(?:the\s+)?(?:intake(?:\s+form)?|patient\s+intake(?:\s+form)?|registration(?:\s+form)?|questionnaire|patient\s+paperwork)\b|\b(?:date\s+of\s+(?:accident|injury|loss)|accident\s
1221:  pattern: '\b(?:prior|previous|earlier|remote|past)\s+(?:[\w/.-]+\s+){0,2}?(?:ESIs?|epidurals?|injections?|nerve\s+blocks?|physical\s+therapy|PT|chiropractic|rehab\w*|(?:therap(?:y|ies)|treatmen
1233:  false_positive: '"Prior authorization" and "previous visit" are not treatment and do not match (the noun list is closed). "Prior PT in 02/2026" is post-accident and is dropped by the year filte
1237:    miss: ['Previous visit reviewed.', 'Prior authorization pending.']
1292:        pattern: '\b(?:records?\s+request|request\s+for\s+records|medical\s+records\s+(?:request|certification|affidavit)|business\s+records\s+affidavit|custodian\s+(?:of\s+records\s+)?affidavit|
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:49:00.704Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I -c \"\nimport json\nfor tag in ('head','pre'):\n    H=json.load(open('$S/t116r5/out/%s.json'%tag))\n    print(tag, sorted(set(p['status'] for p in H['packets'])), [p['packet'] for p in H['packets'] if p['status']!='done'])\n\" ; grep -c \"llm call failed\" artifacts/review-evidence/T-116-paralegal-r4-*.out.txt 2>/dev/null | head -3",
 "description": "Compare packet pipeline statuses between HEAD and pre-T-116"
}
````

### User / tool · 2026-11-02T10:49:00.823Z

**tool result**
````
head ['done', 'done_with_errors'] ['case_lib01_er_only_then_gap']
pre ['done', 'done_with_errors'] ['case_lib01_er_only_then_gap']
artifacts/review-evidence/T-116-paralegal-r4-baseline.out.txt:0
artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.out.txt:0
artifacts/review-evidence/T-116-paralegal-r4-compare.out.txt:0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:49:09.025Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cp $S/t116r5/labels_check.py artifacts/review-evidence/T-116-paralegal-r5-labels-check.py && cp $S/t116r5/appx_check.py artifacts/review-evidence/T-116-paralegal-r5-appx-check.py && cp $S/t116r5/out/head.json $S/t116r5/out/head-r3-probe.json && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r5-labels-check.py $S/t116r5/out/head.json > artifacts/review-evidence/T-116-paralegal-r5-labels-check.out.txt 2>&1; echo \"labels exit=$?\"; tail -2 artifacts/review-evidence/T-116-paralegal-r5-labels-check.out.txt; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r5-appx-check.py $S/t116r5/out/head.json > artifacts/review-evidence/T-116-paralegal-r5-appx-check.out.txt 2>&1; echo \"appx exit=$?\"; cut -c1-120 artifacts/review-evidence/T-116-paralegal-r5-appx-check.out.txt | head -4",
 "description": "Save label and Appendix A check scripts and outputs as evidence"
}
````

### User / tool · 2026-11-02T10:49:09.212Z

**tool result**
````
labels exit=0
labels: 60
runs where counted gap rows != [19, 21]: 0 []
appx exit=0
None | control (verbatim sample.txt) | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
1 | Austin EMS run report, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
2 | Central ER discharge summary, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
3 | Dr. Alvarez, primary care, fax | gaps [7, 7, 28, 14, 73, 11, 14] | flags [('2026-03-06', '2026-05-18', 73, [])]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:49:14.141Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t116r5/head && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q tests/unit -k gap -p no:cacheprovider > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r5-pytest-gap-head.out.txt 2>&1; echo \"gap exit=$?\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q tests/unit/test_t116_gap_endpoints.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_t116_r5_header_only_warning.py -p no:cacheprovider -rA > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r5-pytest-t116-files-head.out.txt 2>&1; echo \"files exit=$?\"; tail -1 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r5-pytest-gap-head.out.txt; tail -1 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r5-pytest-t116-files-head.out.txt; grep -c \"^PASSED\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r5-pytest-t116-files-head.out.txt; grep \"test_t116_r5\\|r5_header\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r5-pytest-t116-files-head.out.txt | cut -c1-160 | head -12",
 "description": "Run gap tests and T-116 test files on HEAD copy, save output"
}
````

### User / tool · 2026-11-02T10:49:19.475Z

**tool result**
````
gap exit=0
files exit=0
270 passed, 2500 deselected in 3.12s
184 passed in 1.46s
184
PASSED tests/unit/test_t116_r5_header_only_warning.py::test_eight_paperwork_variants_show_the_span_and_the_alternative[Capital PT, billing statement-Statement o
PASSED tests/unit/test_t116_r5_header_only_warning.py::test_eight_paperwork_variants_show_the_span_and_the_alternative[Capital PT, billing statement-Statement o
PASSED tests/unit/test_t116_r5_header_only_warning.py::test_eight_paperwork_variants_show_the_span_and_the_alternative[Capital PT, billing statement-Statement o
PASSED tests/unit/test_t116_r5_header_only_warning.py::test_eight_paperwork_variants_show_the_span_and_the_alternative[Capital PT, intake form-Have you been see
PASSED tests/unit/test_t116_r5_header_only_warning.py::test_eight_paperwork_variants_show_the_span_and_the_alternative[Capital PT, intake form-Patient-completed
PASSED tests/unit/test_t116_r5_header_only_warning.py::test_eight_paperwork_variants_show_the_span_and_the_alternative[Capital PT, records request-Please produc
PASSED tests/unit/test_t116_r5_header_only_warning.py::test_eight_paperwork_variants_show_the_span_and_the_alternative[Capital PT, affidavit of records custodia
PASSED tests/unit/test_t116_r5_header_only_warning.py::test_eight_paperwork_variants_show_the_span_and_the_alternative[Quoinmere Mutual Health Plan, EOB-Explana
PASSED tests/unit/test_t116_r5_header_only_warning.py::test_lib06_keeps_its_35_day_flag_with_a_diagnosis_line_on_the_billing_record
PASSED tests/unit/test_t116_r5_header_only_warning.py::test_accident_baseline_never_calls_a_paperwork_headed_record_the_first_recorded_treatment
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:49:55.302Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r4-packet-flags.py $S/t116r5/out/head.json $S/t116r5/out/pre.json > artifacts/review-evidence/T-116-paralegal-r5-packet-flags.out.txt 2>&1; echo \"exit=$?\"; grep -n \"case_lib10\" artifacts/review-evidence/T-116-paralegal-r5-packet-flags.out.txt | cut -c1-200; grep -o \"dates of service[^.]*\" evals/library/case_lib10_eob_ub04_cms1500.txt | head -2; grep -n \"excluded from gap arithmetic\" app/llm/lexicon.yaml | cut -c1-80",
 "description": "Save packet flag comparison as evidence and verify lib10 record text"
}
````

### User / tool · 2026-11-02T10:49:55.599Z

**tool result**
````
exit=0
2:case_lib10_eob_ub04_cms1500 OK pre [('2026-07-08', '2026-08-26', 49)] exp [('2026-07-08', '2026-08-26', 49)] head [('2026-07-14', '2026-08-26', 43)] shown [(('2026-07-08', '2026-08-26', 49), True)]
52:# case_lib10_eob_ub04_cms1500 2026-07-14 2026-08-26 43 [8, 9]
dates of service 06/09/2026 to 06/12/2026
dates of service 06/24/2026 and 07/08/2026
1282:    consumer: 'ADR-010 / D-003: records whose source label matches are excl
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:50:23.356Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-116-paralegal-r5.md",
 "content": "# T-116 round 5 review: paralegal-reviewer (Maria Delgado persona)\n\nCommit under review: f8f358e (HEAD; `git log --oneline -1` = f8f358e, subject \"fix(backend): T-116 r5 paperwork warning is header-only; text evidence never suppresses it (D-055)\"). The diff touches app/backend/gaps.py (the text-evidence test is removed from admin_label), tests/unit/test_t116_r4_all_dated_records.py and tests/unit/test_t116_r5_header_only_warning.py. Both trees were extracted with git archive into the scratchpad (t116r5/head = f8f358e, t116r5/pre = 3e3f3b7). Nothing was run against the dirty project tree except the pytest line noted below.\n\n## Verdict: changes (0 blockers, 1 major, 1 minor carried, 1 nit)\n\nThe r4 blocker (F1) is closed. A paperwork record now shows the 40-day span, the alternative and the conditional flag whether or not its text carries a diagnosis line, 'performed' or 'seen by'. lib06 keeps its 35-day flag with the Diagnosis line. The r1 to r3 invented-gap checks still pass.\n\nThe accident baseline is only partly fixed. It is right for a single paperwork record, but it still calls a paperwork-headed record part of the \"first recorded treatment\" in two cases the fix does not reach (M1). That is a major, not a blocker: no date, visit or amount is invented, and the flag is internal for the paralegal to decide.\n\n## Chris's four checks\n\n1. **All 8 paperwork variants show the span and the alternative, including diagnosis, 'performed' and 'seen by' lines: PASS.** Eight of eight rows MID-SPAN `[(40, True, ['inside'])]` and ENDS-GAP `[(40, False, ['end'])]`. At 8b4ff11 six of those rows were NONE. My own probe covers five paperwork headers times four text variants (plain, Dx line, 'performed', 'seen by'): 20 of 20 carry the alternative sentence (\"the gap would be 40 days\" mid-span, \"there would be no visit after it\" at the end).\n2. **lib06 keeps its 35-day flag with the Diagnosis line: PASS.** With 'Diagnosis: M25.511 pain in right shoulder.' added to record 4, the flag is still `('2026-05-13', '2026-06-17', 35, True, ['inside'])`, the same as the committed packet.\n3. **Accident baseline never calls a paperwork-headed record 'first recorded treatment': PARTIAL, FAIL on two cases.** Single paperwork record, 20 of 20 variants: pass. Same-day paperwork plus visit, and some paperwork headers outside the admin list: fail (M1).\n4. **r1 to r3 probes still create no invented gaps: PASS.** 60 of 60 label runs count gap rows [19, 21] and no visit label draws a flag. The Appendix A 73-day flag is in 10 of 10 fax variants. The r3 warning-and-API output is identical to the r4 record after path normalisation.\n\nAlso run: pytest on the HEAD copy, `-k gap`: 270 passed (also 270 passed in the project tree). The three T-116 test files by path: 184 passed on the HEAD copy and in the project tree. The r5 test file's accident-baseline test passes but covers only one record on its own date; that is why M1 is not caught.\n\n## Findings\n\n**M1 (major). The accident baseline still calls a paperwork-headed record part of the \"first recorded treatment\" when (a) a paperwork record and a visit share the earliest date, or (b) the header is not on the admin list.**\n- Evidence: `artifacts/review-evidence/T-116-paralegal-r5-probe.out.txt` section B2. Paperwork first: \"Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form; Capital PT, initial evaluation).\" Visit first: \"...the first recorded treatment, January 12, 2026 (Capital PT, initial evaluation; Capital PT, intake form).\" For (b), `artifacts/review-evidence/T-116-paralegal-r5-headers.out.txt`: \"Capital PT, questionnaire admin_label=None first_recorded_treatment=True looks_like_paperwork=False\"; the same for \"Capital PT, authorization request\". Code: `app/backend/conflicts.py:64-65` takes the paperwork branch only when every record on the earliest date is admin (`if all(gaps.admin_label(r) for r in first_recs):`); otherwise `app/backend/flag_templates.py:146` names every first-date source in the \"first recorded treatment\" sentence. The admin header list is `app/backend/gaps.py:19-22`, which has no bare 'questionnaire' or 'authorization request'. `tests/unit/test_t116_r5_header_only_warning.py`, last test, uses one paperwork record with no visit on its date, so it cannot see either case.\n- Why it matters: the check Chris set is that the baseline never calls a paperwork-headed record the first recorded treatment. The reading of D-017 and R-FL-2 used in r4 (a non-treatment record is not stated as the first recorded treatment) and D-055 both say the same. An adjuster who reads \"first recorded treatment, Capital PT, intake form\" will point at it. I rate it major because the date is a real encounter date and no fact is invented; the flag is internal and the paralegal decides before export. I escalate r4 F2 from minor to part of this major because the header-only change does not reach this branch and the new test is shape-bound (one record, one date).\n- Fix: (a) in `conflicts.py:64-65`, when the earliest date holds a paperwork-headed record and a visit, do not name the paperwork record in the \"first recorded treatment\" sentence. Either name only the visit source, or use the `_acc_after_paperwork` wording (the record looks like paperwork, the first recorded visit is ..., the stated date is ... later than it). (b) add the bare headers 'questionnaire' and 'authorization request' (and any others qa lists) to the header-only admin list at `gaps.py:19-22`. Keep the decision header-only. (c) add unit tests through `conflicts.accident_date_conflicts` for the same-day case in both record orders and for a 'Capital PT, questionnaire' header.\n- Acceptance test: re-run `artifacts/review-evidence/T-116-paralegal-r5-probe.py` on the new HEAD: section B2 prints no sentence that names 'Capital PT, intake form' as part of the first recorded treatment, in either order. Re-run `T-116-paralegal-r5-headers.py`: `first_recorded_treatment=False` for all 11 headers. The new unit tests pass.\n\n**m2 (minor, carried from r4 F3, still open). The committed golden truth and the lexicon text still encode the exclusion the product dropped.**\n- Evidence: `app/llm/lexicon.yaml:1282` is unchanged: \"ADR-010 / D-003: records whose source label matches are excluded from gap arithmetic. They still become entries.\" `artifacts/review-evidence/T-116-paralegal-r5-packet-flags.out.txt` line 2: \"case_lib10_eob_ub04_cms1500 OK pre [('2026-07-08', '2026-08-26', 49)] exp [('2026-07-08', '2026-08-26', 49)] head [('2026-07-14', '2026-08-26', 43)]\". The expected truth still counts 49; HEAD counts 43 and shows 49 as the alternative.\n- Why it matters: a future check can pass a wrong counted row. The visit-only reading is still what the product shows as its alternative, so no flagged gap is lost today. This does not drive the verdict.\n- Fix: qa names the visit-only table as such and adds a counted table that the product test compares; researcher rewrites the consumer text at `lexicon.yaml:1282` to match the header-only rule.\n- Acceptance test: `rg 'excluded from gap arithmetic' app/llm/lexicon.yaml` returns nothing; a unit test compares the counted rows of all 25 packets to a committed counted table.\n\n**n3 (nit, carried from r4 F4). When the paperwork's own text states the service dates, the headline still leads with the counted number.**\n- Evidence: `T-116-paralegal-r5-packet-flags.out.txt` line 52: \"# case_lib10_eob_ub04_cms1500 2026-07-14 2026-08-26 43 [8, 9]\". Record 8 in `evals/library/case_lib10_eob_ub04_cms1500.txt` reads \"dates of service 06/24/2026 and 07/08/2026\".\n- Why it matters: I have to open record 8 to see which reading the records support. D-055 forbids the tool choosing, so a pointer is enough.\n- Fix: optional. A one-line pointer to the stated service dates next to the alternative.\n\n## What is right\n\n1. The header-only change does what D-055 asks. Eight of eight r4 paperwork rows and 20 of 20 header-by-text variants show the span, the alternative and the conditional flag, with no change in the wording of the warning. The r3 warning-and-API output is identical to the r4 record.\n2. lib06's 35-day conditional flag survives the added Diagnosis line, and the 60-run visit-label sweep still counts every dated record with no invented gap. Appendix A keeps its 73-day flag in all 10 fax variants, and the 28-day interval is not flagged.\n3. The baseline sentence for a single paperwork record names the paperwork record, gives the first-visit alternative, and does not choose a date: `artifacts/review-evidence/T-116-paralegal-r4-baseline.out.txt` B1 and B2 both now read \"looks like paperwork, not a visit\".\n\n## Outside my lens\n\n- The r3 probe prints \"llm call failed ... step=extract\" on stderr for both trees. The packet statuses (done, done_with_errors for case_lib01) are the same on 3e3f3b7 and f8f358e, so this is not a T-116 change. Not scored.\n- Whether the same-day sentence should name the paperwork record at all is wording for Chris and the litigation lead. I only say it must not call paperwork treatment.\n\n## Not done\n\n- The running app at localhost:7860 was not driven. `scores.verify_quickly` is therefore not scored (D-015 applies to reviews of the running app).\n\n```json\n{\"card\": \"T-116\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit f8f358e (HEAD, T-116 r5, D-055 header-only) vs pre-T-116 parent 3e3f3b7; git archive copies in the scratchpad (t116r5/head, t116r5/pre); app/backend/gaps.py, conflicts.py, flag_templates.py, lexicon.yaml:1282; tests/unit/test_t116_r5_header_only_warning.py; sample case and 25 golden and library packets; the running app at localhost:7860 was not driven\",\n \"exercised\": [\n  \"read personas/paralegal.md, reviews/T-116-paralegal-r4.md, D-055 (memory/ORCHESTRATOR_DECISIONS.md:63), D-017 (memory/ORCHESTRATOR_DECISIONS.md:25), R-FL-2 (spec/REQUIREMENTS.md:66), memory t116-gap-endpoint-patterns\",\n  \"git log --oneline -1 -> f8f358e; git show --stat f8f358e (gaps.py, test_t116_r4_all_dated_records.py, test_t116_r5_header_only_warning.py); git show f8f358e -- app/backend/gaps.py\",\n  \"git archive f8f358e -> scratchpad t116r5/head; git archive 3e3f3b7 -> scratchpad t116r5/pre\",\n  \"artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py on HEAD: all 8 rows MID-SPAN [(40, True, ['inside'])] and ENDS-GAP [(40, False, ['end'])] (six rows were NONE at 8b4ff11)\",\n  \"T-116-paralegal-r4-packet-dx-line.py on HEAD: lib10 unchanged; lib06 record 4 with 'Diagnosis: M25.511 pain in right shoulder.' keeps ('2026-05-13', '2026-06-17', 35, True, ['inside'])\",\n  \"T-116-paralegal-r4-baseline.py on HEAD: B1 and B2 both print 'looks like paperwork, not a visit'; no 'first recorded treatment' sentence\",\n  \"NEW artifacts/review-evidence/T-116-paralegal-r5-probe.py (out.txt): section A 20 of 20 header-by-text variants show MID [(40, True, ['inside'])] with alternative 40 and the sentence 'the gap would be 40 days', and ENDS [(40, False, ['end'])] with 'there would be no visit after it'; section B 20 of 20 single-record baselines pass; section B2 same-day case FAILS (M1)\",\n  \"NEW artifacts/review-evidence/T-116-paralegal-r5-headers.py (out.txt): 11 paperwork-looking headers as earliest record; 'Capital PT, questionnaire' and 'Capital PT, authorization request' give admin_label=None and first_recorded_treatment=True (M1 b)\",\n  \"T-116-paralegal-r3-probe.py run on HEAD and 3e3f3b7 (JSON in the scratchpad); NEW T-116-paralegal-r5-labels-check.py (out.txt): 60 of 60 label runs count gap rows [19, 21]; visit labels draw no flag; controls 'Capital PT, intake form' and 'Dr. Lee, chiropractic, billing statement' warn 40 inside\",\n  \"NEW T-116-paralegal-r5-appx-check.py (out.txt): Appendix A control and 9 treatment records with ', fax': 73-day flag 2026-03-06 to 2026-05-18 in 10 of 10; 28-day interval unflagged\",\n  \"T-116-paralegal-r3-warn-and-api.py on HEAD: output identical to artifacts/review-evidence/T-116-paralegal-r4-warn-and-api.head.out.txt after path normalisation (diff exit 0)\",\n  \"T-116-paralegal-r4-packet-flags.py over HEAD and pre JSON -> NEW T-116-paralegal-r5-packet-flags.out.txt: 0 MISSING rows; 22 of 25 counted lists identical; lib10 49 to 43 with 49 shown as alternative; case_09 and lib06 now conditional\",\n  \"pytest, HEAD copy: .venv/bin/python -I -m pytest -q tests/unit -k gap -p no:cacheprovider -> '270 passed, 2500 deselected in 3.12s' (T-116-paralegal-r5-pytest-gap-head.out.txt); project tree, same command -> '270 passed, 2500 deselected in 4.73s'\",\n  \"pytest, HEAD copy: test_t116_gap_endpoints.py + test_t116_r4_all_dated_records.py + test_t116_r5_header_only_warning.py -> '184 passed in 1.46s' (T-116-paralegal-r5-pytest-t116-files-head.out.txt); project tree -> '184 passed in 1.49s'\",\n  \"app/llm/lexicon.yaml:1282 grep on HEAD: 'excluded from gap arithmetic' still present (r4 F3 open)\",\n  \"NOT DONE: running app at localhost:7860 not driven; scores.verify_quickly not scored\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"paperwork_text_never_suppresses_warning\": 5, \"lib06_35_day_flag_with_dx_line\": 5, \"accident_baseline_never_calls_paperwork_treatment\": 2, \"no_invented_gap_r1_r3\": 5, \"golden_truth_consistency\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Accident baseline still calls a paperwork-headed record part of the first recorded treatment when a paperwork record and a visit share the earliest date, or the header is not on the admin list\",\n   \"evidence\": \"artifacts/review-evidence/T-116-paralegal-r5-probe.out.txt section B2: 'is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form; Capital PT, initial evaluation)' (paperwork first) and '(Capital PT, initial evaluation; Capital PT, intake form)' (visit first). artifacts/review-evidence/T-116-paralegal-r5-headers.out.txt: 'Capital PT, questionnaire admin_label=None first_recorded_treatment=True looks_like_paperwork=False'; same for 'Capital PT, authorization request'. app/backend/conflicts.py:64-65 (paperwork branch only if all first-date records are admin); app/backend/flag_templates.py:146 (names every first-date source); app/backend/gaps.py:19-22 (no bare questionnaire or authorization request); tests/unit/test_t116_r5_header_only_warning.py last test covers one record only.\",\n   \"why_it_matters\": \"The check is that the accident baseline never calls a paperwork-headed record the first recorded treatment. The single-record cases pass (20 of 20), but the same-day case names the intake form as part of the treatment, and a questionnaire or authorization request is called first treatment with no caveat. The r4 reading of D-017 and R-FL-2, and D-055, say a non-treatment record is not stated as treatment. Rated major, not blocker: the date is a real encounter date, no fact is invented, and the flag is internal for the paralegal to decide. r4 F2 is escalated into this finding because the header-only change does not reach this branch and the new test is shape-bound.\",\n   \"fix\": \"(a) conflicts.py:64-65: when the earliest date holds a paperwork-headed record and a visit, do not name the paperwork record in the first-recorded-treatment sentence; name only the visit source, or use the _acc_after_paperwork wording. (b) gaps.py:19-22: add bare 'questionnaire' and 'authorization request' (and any others qa lists) to the header-only admin list; keep it header-only. (c) unit tests through conflicts.accident_date_conflicts for the same-day case in both record orders and for a 'Capital PT, questionnaire' header.\",\n   \"acceptance_test\": \"Re-run artifacts/review-evidence/T-116-paralegal-r5-probe.py on the new HEAD: section B2 prints no sentence naming 'Capital PT, intake form' as part of the first recorded treatment, in either order. Re-run T-116-paralegal-r5-headers.py: first_recorded_treatment=False for all 11 headers. New unit tests for both cases pass.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Committed golden truth and lexicon text still encode the exclusion the product dropped (carried from r4 F3, still open)\",\n   \"evidence\": \"app/llm/lexicon.yaml:1282 unchanged: 'ADR-010 / D-003: records whose source label matches are excluded from gap arithmetic.' artifacts/review-evidence/T-116-paralegal-r5-packet-flags.out.txt line 2: 'case_lib10_eob_ub04_cms1500 OK pre [(2026-07-08, 2026-08-26, 49)] exp [(2026-07-08, 2026-08-26, 49)] head [(2026-07-14, 2026-08-26, 43)]'.\",\n   \"why_it_matters\": \"The expected counted truth for lib10 still reads 49; HEAD counts 43 and shows 49 as the alternative. A future check can pass a wrong counted row. No flagged gap is lost today, so this does not drive the verdict.\",\n   \"fix\": \"qa names the visit-only table as such and adds a counted table the product test compares; researcher rewrites the consumer text at lexicon.yaml:1282 to match the header-only rule.\",\n   \"acceptance_test\": \"rg 'excluded from gap arithmetic' app/llm/lexicon.yaml returns nothing; a unit test compares the counted rows of all 25 packets to a committed counted table.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"When the paperwork's own text states the service dates, the headline still leads with the counted number (carried from r4 F4)\",\n   \"evidence\": \"artifacts/review-evidence/T-116-paralegal-r5-packet-flags.out.txt line 52: '# case_lib10_eob_ub04_cms1500 2026-07-14 2026-08-26 43 [8, 9]'. evals/library/case_lib10_eob_ub04_cms1500.txt record 8: 'dates of service 06/24/2026 and 07/08/2026'.\",\n   \"why_it_matters\": \"The paralegal has to open record 8 to see which reading the records support. A pointer would be enough; D-055 forbids the tool choosing.\",\n   \"fix\": \"Optional: a one-line pointer to the stated service dates beside the alternative.\",\n   \"acceptance_test\": \"Optional: lib10 explanation names the 07/08/2026 service date from record 8.\"}\n ],\n \"whats_right\": [\n  \"The header-only change closes r4 F1: 8 of 8 r4 paperwork rows and 20 of 20 header-by-text variants show the span, the alternative and the conditional flag; the lib06 35-day flag survives the Diagnosis line.\",\n  \"No invented gap: 60 of 60 visit-label runs count gap rows [19, 21] with no flag; Appendix A keeps its 73-day flag in 10 of 10 fax variants; the r3 warning and API output is identical to the r4 record.\",\n  \"A single paperwork record in the accident baseline names the paperwork record, gives the first-visit alternative, and does not choose a date.\"\n ],\n \"questions_for_chris\": [\n  \"M1: when a paperwork record and a visit share the earliest date, should the baseline name the paperwork record at all, or only the visit? I only require that it never calls the paperwork record treatment.\",\n  \"M1(b): is the admin header list closed by design? 'questionnaire' and 'authorization request' are paperwork headers a paralegal would call paperwork.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T10:50:23.522Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-116-paralegal-r5.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:50:29.607Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r5-jsoncheck.py",
 "content": "\"\"\"Checks the D.2 json block of reviews/T-116-paralegal-r5.md: parses, required keys, severities, verdict rule (blocker -> fail, major -> changes, else pass).\nUsage: .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r5-jsoncheck.py\"\"\"\nimport json\nimport pathlib\nimport re\n\nROOT = pathlib.Path(\"/Users/arsis/zlayt-pm-project\")\ntext = (ROOT / \"reviews/T-116-paralegal-r5.md\").read_text(encoding=\"utf-8\")\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", text, flags=re.S)\nassert len(blocks) == 1, f\"expected exactly one json block, found {len(blocks)}\"\nr = json.loads(blocks[0])\nneed = [\"card\", \"persona\", \"model\", \"scope\", \"exercised\", \"verdict\", \"scores\", \"findings\", \"whats_right\", \"questions_for_chris\"]\nmissing = [k for k in need if k not in r]\nassert not missing, missing\nassert r[\"card\"] == \"T-116\" and r[\"persona\"] == \"paralegal-reviewer\" and r[\"model\"] == \"claude-haiku-5-5\", (r[\"card\"], r[\"persona\"], r[\"model\"])\nsev = [f[\"severity\"] for f in r[\"findings\"]]\nassert set(sev) <= {\"blocker\", \"major\", \"minor\", \"nit\"}, sev\nfor f in r[\"findings\"]:\n    for k in (\"severity\", \"title\", \"evidence\", \"why_it_matters\", \"fix\", \"acceptance_test\"):\n        assert f.get(k), (k, f.get(\"title\"))\nexpected = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nassert r[\"verdict\"] == expected, (r[\"verdict\"], expected)\nassert len(r[\"whats_right\"]) <= 3\nprint(\"json ok; card\", r[\"card\"], \"model\", r[\"model\"], \"verdict\", r[\"verdict\"], \"(rule gives\", expected + \")\")\nprint(\"findings\", [(f[\"severity\"], f[\"title\"][:60]) for f in r[\"findings\"]])\nprint(\"scores\", r[\"scores\"])\nprint(\"exercised items\", len(r[\"exercised\"]), \"whats_right\", len(r[\"whats_right\"]), \"questions\", len(r[\"questions_for_chris\"]))\n"
}
````

### User / tool · 2026-11-02T10:50:29.725Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-116-paralegal-r5-jsoncheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:50:31.305Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r5-jsoncheck.py 2>&1 | tee artifacts/review-evidence/T-116-paralegal-r5-jsoncheck.out.txt; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/board.py validate reviews/T-116-paralegal-r5.md 2>&1 | tail -5; echo \"validate_exit=${PIPESTATUS[0]}\"",
 "description": "Validate review JSON block and run board validate on the review file"
}
````

### User / tool · 2026-11-02T10:50:31.465Z

**tool result**
````
json ok; card T-116 model claude-haiku-5-5 verdict changes (rule gives changes)
findings [('major', 'Accident baseline still calls a paperwork-headed record part'), ('minor', 'Committed golden truth and lexicon text still encode the exc'), ('nit', "When the paperwork's own text states the service dates, the ")]
scores {'paperwork_text_never_suppresses_warning': 5, 'lib06_35_day_flag_with_dx_line': 5, 'accident_baseline_never_calls_paperwork_treatment': 2, 'no_invented_gap_r1_r3': 5, 'golden_truth_consistency': 3}
exercised items 16 whats_right 3 questions 2
exit=0
ok (1 file(s))
validate_exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:50:35.753Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t116-gap-endpoint-patterns.md",
 "offset": 40
}
````

### User / tool · 2026-11-02T10:50:35.760Z

**tool result**
````
40	How to apply: on any gap, endpoint or truth change, run artifacts/review-evidence/T-116-paralegal-r3-probe.py on the pre parent and HEAD, then
41	compare; restore the parent's truth file on a scratch copy to confirm a gate fails; check every exclusion layer, not only the one edited.
42	
43	Related: [[golden-set-recurring-findings]], [[t114-rates-gap-patterns]], [[t118-lib11-truth-patterns]], [[reviewer-tooling-quirks]].
44	
45	## r4 (8b4ff11, 2026-11-02, verdict fail: 1 blocker, 2 minors, 1 nit; reviews/T-116-paralegal-r4.md)
46	r3 blockers fixed: compute_gaps reads every dated record, 60/60 label runs no invented gap, conditional "Possible gap of N days" flag and
47	"If record N: <header> is paperwork, not a visit, the gap would be X days" work. lib10 49 -> 43 (CMS-1500 dated 07-14, excerpt states DOS 07/08), alt 49 shown: correct.
48	New blocker pattern: the warning is gated by gaps.admin_label -> _has_treatment_evidence (regex on excerpt: Dx:, performed, seen by, Plan:). Bills/EOBs/forms
49	with those words get no warning, no alternative, no conditional flag; a mid-span 40-day span vanishes (pre-T-116 showed it). Same gate feeds the accident baseline.
50	Recurring: every time a guess is removed, check the next gate (warning suppression) with the same probe; use mutation: append one clinical-sounding sentence to a paperwork excerpt.
51	Probes: artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py, -packet-dx-line.py, -baseline.py (reuse r3-probe.py for labels).
52	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:50:39.636Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t116-gap-endpoint-patterns.md",
 "old_string": "Probes: artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py, -packet-dx-line.py, -baseline.py (reuse r3-probe.py for labels).\n",
 "new_string": "Probes: artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py, -packet-dx-line.py, -baseline.py (reuse r3-probe.py for labels).\n\n## r5 (f8f358e, 2026-11-02, verdict changes: 0 blockers, 1 major, 1 minor carried, 1 nit; reviews/T-116-paralegal-r5.md)\nr4 F1 closed: admin_label is header-only; 8/8 r4 paperwork rows and 20/20 header x text variants (T-116-paralegal-r5-probe.py) show span, alternative, conditional flag. lib06 35-day flag survives the Dx line. 60/60 label runs still [19, 21] with no flag.\nOpen, major (M1): the accident baseline still names paperwork as \"first recorded treatment\" in two places the header-only change does not touch:\n(a) same-day paperwork + visit: conflicts.py:64-65 takes the paperwork branch only if ALL first-date records are admin; else flag_templates.py:146 lists every first-date source.\n(b) headers missing from gaps.py:19-22 (bare 'questionnaire', 'authorization request') are called first treatment with admin_label None.\nRecurring: a unit test that uses one record on its own date passes while the same-day branch fails. For any branch with an \"all(...)\" or first-date list, probe mixed dates in both record orders.\nStill open from r4: F3 golden lib10 expected 49 vs counted 43 and lexicon.yaml:1282 text; F4 headline leads with 43 when the paperwork states DOS 07/08.\nProbes (r5): T-116-paralegal-r5-probe.py, -headers.py, -labels-check.py, -appx-check.py, -packet-flags.out.txt, -jsoncheck.py.\n"
}
````

### User / tool · 2026-11-02T10:50:39.757Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t116-gap-endpoint-patterns.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:50:42.873Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t116-gap-endpoint-patterns.md",
 "old_string": "description: T-116 gap endpoints through r3 (8673326, 2026-11-02, verdict fail): gaps.py exclusion gone but ingest record_kind still drops visits by label; accident baseline still counts intake forms; lib11 truth flipped to stale",
 "new_string": "description: T-116 gap endpoints through r5 (f8f358e, 2026-11-02, verdict changes): r4 warning-suppression blocker closed; accident baseline still says paperwork is first treatment on same-day and questionnaire/authorization headers (M1); lib10 golden truth still stale"
}
````

### User / tool · 2026-11-02T10:50:42.992Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t116-gap-endpoint-patterns.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:50:44.140Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T10:50:44.151Z

**tool result**
````
1	- [Spec review patterns](feedback_spec_review_patterns.md) — check absolute claims vs the doc's own example; grep every named category/R-ID/fixture
2	- [Golden-set recurring findings](golden-set-recurring-findings.md) — T-015: must/should levels, shared type+cite flags, export/§6 drift, dead checks via key drift (mutation-test)
3	- [Reviewer hook constraints](reviewer-hook-constraints.md) — board.py allowed verbs, python heredoc form, write-allowed dirs
4	- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; review files are append-only (proofread before the one Write)
5	- [Frontend review patterns](frontend-review-patterns.md) — T-043: mock vs harness coverage, keyboard focus yank, recurring minor gaps
6	- [Library review patterns](library-review-patterns.md) — T-052 minors; T-077 r2/r3: self-test shape-bound (author-year, prose escape), title-case FAIR Health passes
7	- [Record-format review patterns](record-format-review-patterns.md) — T-078 r2: mutation-test the check script; visit-count fix creates a PT gap; lib14 specimen gaps
8	- [Manual entry / split review patterns](manual-entry-split-review-patterns.md) — T-056: AC ticked for absent UI label, split amounts not moving, override trace missing
9	- [T-068 dates-to-confirm patterns](t068-dates-to-confirm-patterns.md) — orphan confirm dead-ends, record listed twice, text-only AC test, commit vs worktree divergence
10	- [D-041 date-gate patterns](d041-date-gate-patterns.md) — T-076 r2 (f4ef2ea): stale DATE_AMBIGUOUS fixed; Edit/Change quote still enabled on undated row (T-060)
11	- [Reviewer API shape gotchas](reviewer-api-shape-gotchas.md) — item GET nests under "item", status "ready", record warnings in case.flags, audit before/after local-only
12	- [T-079 library v2 patterns](t079-library-v2-patterns.md) — statement-vs-note double count, replay at cited commit, append-only ref proofreading
13	- [T-114 rates and gap patterns](t114-rates-gap-patterns.md) — rate acknowledge-only passes; gap change API-only in HEAD; intake-form encounter kind is Chris's call; golden N1 scoped to ambiguous
14	- [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — r3 fail; r4 (8b4ff11) fail: warning gated by excerpt-text regex hides mid-span bill/form spans
15	- [T-118 lib11 truth patterns](t118-lib11-truth-patterns.md) — validators pass on the wrong truth; record lists unguarded; intake form as phone_note stand-in; stale library-latest.md
16	- [T-060 UI polish patterns](t060-ui-polish-patterns.md) — pass 2 open items; reuse q0-q13 scripts; recount severities before the single Write
17	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:50:46.001Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — r3 fail; r4 (8b4ff11) fail: warning gated by excerpt-text regex hides mid-span bill/form spans",
 "new_string": "- [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — r3 fail; r4 fail (warning gated by text regex); r5 (f8f358e) changes: same-day and header-list gaps in baseline wording"
}
````

### User / tool · 2026-11-02T10:50:46.099Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:50:49.327Z

Verdict: changes (0 blockers, 1 major, 1 minor, 1 nit). The r4 suppression blocker is closed, but the accident baseline still calls paperwork the first recorded treatment on same-day and questionnaire/authorization headers. Review: /Users/arsis/zlayt-pm-project/reviews/T-116-paralegal-r5.md
