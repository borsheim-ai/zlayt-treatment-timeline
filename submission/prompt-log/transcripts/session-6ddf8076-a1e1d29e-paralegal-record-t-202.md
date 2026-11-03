# Subagent: Paralegal record: T-202 (Paralegal record: T-202)

Source: `agent-a1e1d29e45ef0b108.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T14:59:47.400Z

You are the paralegal reviewer in /Users/arsis/zlayt-pm-project, starting from a fresh context. The board needs a paralegal record on T-202, whose last paralegal verdict, round 6, was fail. Since then, the D-073 all-blank fallback landed (b50952d), and the combined gate panel's paralegal review passed it: reviews/GATE-M3M4-paralegal.md.

Read the card, reviews/T-202-paralegal-r6.md and that gate review. Check quickly at HEAD:
- every charge line in the sample, case_09, lib10 and lib11 letters is the exact blank "date of service [__________] (record|statement dated X)";
- no line prints an extracted date;
- `python -m evals.letter_check` reports 0.

Run the letters from a `git archive HEAD` copy. Confirm the round-6 blockers, a wrong date from a visit note and a UB-04 period override, can no longer occur.

Write reviews/T-202-paralegal-r7.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:50.733Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-03T14:59:50.739Z

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

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:51.306Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-202 && echo ---- && git log --oneline -n 8 && echo ---- && git rev-parse HEAD && git status --short | head -30",
 "description": "Show T-202 card, recent commits, HEAD hash, and working tree status"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:51.534Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r6.md"
}
````

### User / tool · 2026-11-03T14:59:51.695Z

**tool result**
````
<outside-repo file omitted>
````

### User / tool · 2026-11-03T14:59:51.701Z

**tool result**
````
1	# T-202 round 6 (D-073 round-6 rules): paralegal review (Maria Delgado, senior PI litigation paralegal)
2	
3	**Verdict: fail.** The bar for this round: no charge line ever prints a wrong date of service. Round 6 does not meet it.
4	
5	**What round 6 fixed.** The round 5 findings are closed in the full pipeline:
6	- Provider names. "Austin MRI", "Open MRI of Austin", "Hobbleton Follow-Up Clinic", "Hobbleton X-Ray", "Hobbleton Hand Evaluation Center" and "Express Exam Urgent Care" bills now print the blank.
7	- The "Date of service: 02/02/2026  Account: 4471" line over a row, and the brief's "Date of service: X" line over a "Date posted" table, now print the blank.
8	- A "Visit date" column over a "Next visit" column prints the visit date, in either column order.
9	- Blank labels. On the 25-case corpus, all 74 blanks carry the right label: 16 "statement dated" lines, all on bills, and 58 "record dated" lines, all on ED, urgent-care, imaging, radiology or chiropractic records.
10	- The 5 dated corpus lines (the sample ER line and the four lib10 UB-04 lines) are correct. They are the same lines as on f9c0faf.
11	- The sample, case_09, lib14, lib10 and lib11 letters I generated in the UI are all correct.
12	
13	**What still prints a wrong date.** The second date source is the encounter record's own date. It is lent to any charge in an identified visit note whose own sentence holds none of the guard words: earlier, previous, prior, next, last, later, ago, former, subsequent, a month-year, or a visit count. Charges in a visit note for another time pass straight through:
14	- "Initial evaluation 97161 charge $250.00." in the visit-9 PT note prints March 6. Record 4 dates the initial evaluation January 23.
15	- "Patient went to urgent care yesterday, urgent care visit charge $310.00." prints January 16.
16	- "ER facility charge $6,240.00." in the PCP office visit note prints January 16.
17	- A late entry dated 01/20 "for the visit of 01/16/2026" prints January 20.
18	- The sample ER summary with "Arrived 01/09/2026 ... Discharged 01/10/2026" prints January 10.
19	
20	For every one of these, letter_check accepts the wrong line and rejects both the blank and the true date.
21	
22	One source (1) shape is also wrong. A UB-04 coded line that states its own "service date 02/05/2026" prints the statement period "February 9–12, 2026", with that quote directly under it.
23	
24	The ER overnight shape was already in my round 4 probe set (r4 T3). It printed January 10 in my round 5 run as well (r5 probe_r5.out:669), and I counted it as correct there. That was my miss.
25	
26	D-073 pre-declares the outcome: "If round 6 still prints a wrong date, the MVP letter prints the fillable blank on every charge line (no date extraction at all) and SCOPE_CUTS 28 covers it."
27	
28	**Usability (brief).** A letter of blanks works for a demand. Filling a date is the same job as filling the Bates placeholders. Now that the label reads "(record dated March 18, 2026)" on an ED record, I can fill most blanks from the date printed next to them. The internal notes still tell me to "fill it from the quote" when the quote has no date, while Step 3 says "Take the date from the matching visit note". A dated line from a visit note still has to be opened, because the eval protects a wrong one. `verify_quickly` is 3.
29	
30	**Scope.** I extracted `git archive 9655f1d` (tree 823f8e2e8d56) to the session scratchpad and served it in demo mode on 127.0.0.1:7986: fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local. /api/health returned demo_mode true and local_mode true. I stopped listener PID 94928 afterwards (lsof exit 1, curl 000).
31	
32	HEAD moved to 6be191f during the review. `git diff --stat 9655f1d HEAD -- app/backend app/llm app/frontend evals/letter_check.py` is empty.
33	
34	The adversarial texts ran in-process through `evals.letter_check.letters_for`, which is the export path, because demo mode refuses unrecorded text. Private values seen: 0. Per the brief, the Step 3 header ("statement dated" on record blanks) belongs to another card and is not graded here.
35	
36	```json
37	{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
38	 "scope": "commits b72acb9, 3654cf9, 756546b, 9655f1d (git archive 9655f1d, tree 823f8e2e8d56, extracted to the session scratchpad pr6_9655f1d/); served in demo mode (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local; /api/health demo_mode true, local_mode true) at http://127.0.0.1:7986; listener PID 94928 stopped (lsof exit 1, curl 000). Parent f9c0faf archive (pr6_f9c0faf/) run in-process for the corpus diff. HEAD moved to 6be191f during the review; git diff --stat 9655f1d HEAD -- app/backend app/llm app/frontend evals/letter_check.py is empty. Cases: sample, case_09 (POST /api/cases with the golden text, opened in the UI), lib14, lib10, lib11 in the UI; all 25 letter_check cases in-process; SYNTHETIC variants in-process (demo mode refuses unrecorded text). Step 3 header wording excluded per the brief (another card). Evidence: artifacts/review-evidence/T-202-paralegal-r6/. Private values seen: 0.",
39	 "exercised": [
40	  "Read personas/paralegal.md, D-073 and its round-6 rules (memory/ORCHESTRATOR_DECISIONS.md:97-100), memory/SCOPE_CUTS.md:113 (row 28), reviews/T-202-paralegal-r5.md, board.py show T-202 (r6 notes and the handoff with its 84-line corpus diff), service_date.py, store.charge_service_date and encounter_types.json at 9655f1d",
41	  "From the archive: pytest test_t202_r6_d073 + r5 + r4 + r3 + r2 layouts + test_t202_charge_service_dates + test_t200_undated_charge_label + test_export: '913 passed in 10.78s' (pytest-t202.out); python -m evals.letter_check: value 0 over 25 cases (letter_check.out)",
42	  "probe_r6.py: all 162 round 1-5 texts loaded by ast from my earlier probe files (r1 probe_dates/probe_dates2, r2, r3, r4 NEW, r5 NEW incl. the MRI/X-Ray/Follow-Up/Evaluation/Exam provider names, the key-value DOS line over a row, Visit Date/Next Visit Date) plus 31 round 6 shapes (A1-A20 charges in whole-phrase visit notes for another time, B1-B9 bill tables incl. the brief's 'Date of service: X' over 'Date posted' and 'Visit date' over 'Next visit', U1-U2 UB-04), through store.charge_service_date; every STATED result checked by hand (probe_r6.out)",
43	  "fullpipe_r6.py: 30 shapes (28 in fullpipe_r6.out, a15 and u1 in fullpipe_r6_a15_u1.out) through the full pipeline and letter (round 6 A-shapes, the r5 m1-m2/c1-c4 provider-name bills, t4/t4b key-value DOS lines, t5/t5b visit/next-visit tables, t1 control) with letter_check on each (fullpipe_r6.out, fullpipe_r6_a15_u1.out); fullpipe_lib10.py (an added charge in lib10 record 3 did not reach the letter: fullpipe_lib10.out)",
44	  "eval_teeth_r6.py: letter_check on the build's line vs the blank and the true date for A2, A5, A6b, A10; blank label on six records whose label or excerpt opening holds a money word (eval_teeth_r6.out)",
45	  "corpus_blanks.py on 9655f1d and f9c0faf: every BILLED CHARGES line of the 25 cases, all_accepted and counted (corpus_blanks_*.out, corpus_blanks.diff): 37 all_accepted lines, 32 blank and 5 dated on 9655f1d; the 5 dated lines are unchanged from f9c0faf; 74 blank labels checked against record type",
46	  "Playwright on the running archive (h.py + p01_cases.py): sample, case_09, lib14, lib10, lib11 keyboard-first through Steps 1-4, every Step 3 card logged and screenshotted, letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt, p01.out); drafting took 2.3-2.5 s per case"
47	 ],
48	 "verdict": "fail",
49	 "scores": {"verify_quickly": 3, "letter_dates_correct_on_corpus": 5, "adversarial_dates_correct": 3, "blank_label_correct": 4},
50	 "findings": [
51	  {"severity": "blocker",
52	   "title": "A visit note's own date is printed as the date of service of a charge the note itself places at another time (initial evaluation, first visit, yesterday, the ER, the day of the collision, February, a late entry, an overnight ER stay, a course total); letter_check accepts only the wrong line",
53	   "evidence": "fullpipe_r6.out (sample with one SYNTHETIC record added or record 6 replaced; full pipeline, every item accepted): a2 PT note 03/06 -> 'Capital PT, physical therapy note, March 6, 2026: $250.00 | Initial evaluation 97161 charge $250.00.' (record 4 dates the initial evaluation 2026-01-23); a3 'First visit charge $250.00.' -> March 6; a10 PCP note 01/16 -> 'Dr. Alvarez, office visit note, January 16, 2026: $310.00 | Patient went to urgent care yesterday, urgent care visit charge $310.00.'; a1 -> 'Dr. Alvarez, office visit note, January 16, 2026: $6,240.00 | ER facility charge $6,240.00.'; a16 'Original ER charge $6,240.00 reviewed with patient.' -> January 16; a11 'Ambulance transport on the day of the collision, charge $1,380.00.' -> January 16; a12 note 03/05 'February follow-up visit 99213 charge $150.00.' -> March 5; a20 MRI report 05/29 'ER x-ray charge $240.00.' -> May 29; a5 note dated 01/20 'Late entry for the visit of 01/16/2026. Office visit 99213 charge $150.00.' -> January 20; a6b the sample ER summary dated 01/10 with 'Arrived 01/09/2026 by EMS. Discharged 01/10/2026.' -> 'Central ER discharge summary, January 10, 2026: $6,240.00'; a7 'Physical therapy charges: $1,665.' -> March 6. Every one: 'date violations: []'. eval_teeth_r6.out (A2, A5, A6b, A10): the build's line -> []; the blank -> 'the line prints a blank above a source that gives its date'; the true date -> 'the line prints a date no source ties to it'. probe_r6.out: r4 T3 (my round 4 probe, same as a6b) prints January 10; it printed the same in my round 5 run (r5 probe_r5.out:669), and I did not flag it there. Cause: service_date.py:447 gives the record date unless the charge's own segment matches _MULTI (:374), _OTHER_TIME (:87; earlier, previous, prior, next, last, later, ago, former, subsequent) or a month-year; a previous sentence is never read (a5, a6b). evals/letter_check.py:264 uses the same word list, so it shares the blind spot. Controls print correctly: a17 ER record 'ER facility charge' -> January 9; a18 PT note 'Discharge visit 97110 charge $185.00.' -> March 6.",
54	   "why_it_matters": "This is the bar for this round, and §5 of my dossier: a date in the letter that the record contradicts. The adjuster will compare the PT initial-evaluation charge with the PT ledger and find January 23, not March 6. The ER overnight shape is common: an ER visit that crosses midnight, with its summary dated the discharge day. There it prints January 10 against an EMS run and accident date of January 9, which creates a date conflict that is not in the records. The quote printed under each line holds no date, so checking the quote does not catch it. The eval rejects both the blank and the true date, so a careful fix would be pushed back.",
55	   "fix": "Apply the outcome D-073 pre-declares for a round-6 failure: every charge line prints the fillable blank '(record dated X)' / '(statement dated X)', no date extraction, and SCOPE_CUTS 28 covers it. letter_check then accepts the blank and nothing else on every charge line. On the corpus this moves 5 of 37 lines (the sample ER line and the four lib10 UB-04 lines) to blanks with correct labels.",
56	   "acceptance_test": "fullpipe_r6.py a1, a2, a3, a5, a6b, a7, a10, a11, a12, a16, a20 and u1 each print '<source>, date of service [__________] (record dated ...)' or '(statement dated ...)'. letter_check reports a violation on 'Capital PT, physical therapy note, March 6, 2026: $250.00' and accepts the blank. The corpus has 0 dated charge lines and 74 blanks with unchanged labels."},
57	  {"severity": "blocker",
58	   "title": "A UB-04 statement period is printed over a coded line that states its own, different service date (rule 3: the UB-04 period gets the same several-dates guard)",
59	   "evidence": "fullpipe_r6_a15_u1.out u1 (case_09 record 2 replaced by 'Saltmarrow General Hospital, UB-04', excerpt 'UB-04. Statement covers period 02/09/2026 through 02/12/2026. Rev 0450 99285 emergency room, service date 02/05/2026, FL47 total charges $2,105.00.') -> 'Saltmarrow General Hospital, UB-04, February 9–12, 2026: $2,105.00 | Rev 0450 99285 emergency room, service date 02/05/2026, FL47 total charges $2,105.00.', date violations: []. probe_r6.out U1 gives the same at the resolver (06/05 line date, June 9–12 printed). Cause: service_date.py:427 blanks the span only for _OTHER_TIME words in the span's sentence; a second candidate date in the charge's own line is not checked.",
60	   "why_it_matters": "The head of the line says February 9–12 and the quote directly under it says 02/05. This bill contradicts itself, and the tool picks one reading silently. That is the case my dossier treats as a dealbreaker for the accident dates. The adjuster sees the mismatch on the face of the letter.",
61	   "fix": "Covered by the D-073 final step above. If source (1) is kept, a coded line whose own sentence holds any date gets the blank, the same guard as the encounter sentence.",
62	   "acceptance_test": "fullpipe_r6.py u1 prints 'Saltmarrow General Hospital, UB-04, date of service [__________] (statement dated March 1, 2026)'; letter_check flags 'February 9–12, 2026' for it."},
63	  {"severity": "major",
64	   "title": "The blank says '(statement dated X)' on clinical records whose excerpt opens with a money word or whose label carries one (rule 4)",
65	   "evidence": "eval_teeth_r6.out part 2: L1 'Central ER discharge summary', excerpt 'ER charges: $6,240. Dx: cervical strain. CT head negative.' -> kind=bill, '... date of service [__________] (statement dated January 9, 2026)'; L2 'Dr. Alvarez, office visit note', 'Copay collected $40. Persistent neck pain 6/10. ...' -> statement dated; L3 'Capital PT, physical therapy note', 'Payment plan discussed. ...' -> statement dated; L4 'Central ER, emergency department record, account 4471' -> statement dated. Cause: service_date.py:50-51 calls a record a bill when the first 40 characters of the excerpt (cut at the first colon or full stop) or the label match the financial list, before the whole document-type phrase is looked at. Corpus: 0 of 74 blanks mislabelled (corpus_blanks_9655f1d.out).",
66	   "why_it_matters": "If I fill the blank and keep the parenthetical, the letter tells the adjuster that an ER discharge summary is a statement. The record says no such thing, and it invites a request for a statement that does not exist. It is rated major, not blocker, because the date in parentheses is still the record's own date and no corpus line is affected. The same shape was a round 4 minor ('ER charges:' opening).",
67	   "fix": "Let a whole document-type phrase in the source label (discharge summary, office visit note, physical therapy note, emergency department record) outrank money words in the excerpt opening and in the rest of the label. Use the opening only when the label has no document-type phrase.",
68	   "acceptance_test": "eval_teeth_r6.py L1-L4 print '(record dated ...)'; L5 (no document type, opens 'Charges:') and L6 (billing statement) keep '(statement dated ...)'; the corpus labels are unchanged."},
69	  {"severity": "minor",
70	   "title": "Carried from rounds 3-5: the internal notes say 'fill it from the quote' for quotes with no date, while Step 3 says 'Take the date from the matching visit note'",
71	   "evidence": "ui-sample-notes.txt:36 '- Austin Imaging, $2,150: The line states no date of service the code can read ... fill it from the quote or request a dated itemized bill from the provider.' The quote is 'Charge: $2,150.' (ui-sample-letter.txt). ui-lib11-notes.txt:39-42 say the same for 'ED charge: $3,260.' and the Fennimoor ledger lines. p01.out [sample] s3 item=a4: 'Take the date from the matching visit note, or request a dated line-by-line bill, and fill the blank'.",
72	   "why_it_matters": "The notes and the screen give different instructions for the same line, and there is nothing in the quote to fill from.",
73	   "fix": "Use the Step 3 sentence (service_date.py _ASK_NONE) in the notes for the no-date reasons.",
74	   "acceptance_test": "No notes line says 'fill it from the quote' when the quote has no date."},
75	  {"severity": "minor",
76	   "title": "Carried from rounds 3-5: one single-date blank covers a 14-visit charge, and some quotes are only the figure",
77	   "evidence": "ui-lib11-letter.txt: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $2,310.00' over 'treatment visits 1 through 14 charge $2,310.00'. ui-lib14-letter.txt: 'Source [Ex. __ / Bates __]: \"charge $187.05.\"'; ui-sample-letter.txt: 'Source [Ex. __ / Bates __]: \"Charge: $2,150.\"'.",
78	   "why_it_matters": "A 14-visit charge needs a range. A bare-figure quote does not tell the adjuster what was billed.",
79	   "fix": "Print 'dates of service [__________]' when the quote counts visits. Quote the bill line from its code or description through the figure.",
80	   "acceptance_test": "The lib11 $2,310.00 line reads 'dates of service [__________]'. The lib14 $187.05 quote names its service."}
81	 ],
82	 "whats_right": [
83	  "Provider names no longer lend dates: Austin MRI, Open MRI of Austin, Follow-Up Clinic, X-Ray, Evaluation Center, Exam Urgent Care bills all print the blank with '(record dated ...)' (fullpipe_r6.out m1-m2, c1-c4).",
84	  "Real-table rule holds: 'Date of service: X' key-value lines over rows or a 'Date posted' table give the blank; 'Visit date' beside 'Next visit' prints the visit date in either column order (t4, t4b, t5, t5b, B1-B9).",
85	  "Corpus labels are right: 16 'statement dated' all on bills, 58 'record dated' all on ED/UC/imaging/chiro records; the 5 dated lines are correct and unchanged; sample total $8,390.00."
86	 ],
87	 "questions_for_chris": []}
88	```
89	
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:51.713Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/GATE-M3M4-paralegal.md"
}
````

### User / tool · 2026-11-03T14:59:51.719Z

**tool result**
````
1	# GATE-M3M4 paralegal review (Maria Delgado, senior PI paralegal)
2	
3	Pinned commit f6d5c19 (`git archive f6d5c19`, extracted to the session scratchpad). Rules applied: D-075 (blockers only) and the D-073 fallback.
4	Demo-mode server on port 7931 (`ZLAYT_MODE` unset, fixture backend, no `ENABLE_LIVE`, health `demo_mode:true`). The demo refuses lib10 and lib11 text
5	(409 `demo_mode_unsupported_input`, same as the public demo), so those two ran on a second archive server on port 7932 with `ZLAYT_MODE=local`
6	and the same fixtures. Both servers were stopped by PID afterward (curl on 7931 and 7932 returns 000, no listener). No private value was handled; none is quoted here.
7	
8	**Verdict: pass. No blockers.**
9	
10	## What I checked
11	
12	**Sample case, record to letter, timed.** Draft step 1.3 s. A scripted keyboard run (A to accept every item) reached the finished letter in 17.4 s total
13	(19 timeline items, 4 bill amounts). That is script speed, not human speed; the point is that nothing stalls.
14	- Records: 9 found, all dates read correctly (Jan 9 twice, Jan 16, Jan 23, Feb 20, Mar 6, May 18, May 29, Jun 12).
15	- Total: letter line reads `Billed charges accepted from these records: $8,390.00` (wording is D-062 / R-EX-8, not the older D-019 text). ER $6,240 plus MRI $2,150 = $8,390. Verified by hand.
16	- PT rate: `$185` is on the Step 3 "Never counted" list as a rate. No PT total anywhere in the letter. Internal notes say
17	  `Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.` "Missing 3 days of work" is not a charge and sits under Damages mentions.
18	- Gap: 73 days, March 6 to May 18, with both dates and both records. The 28-day interval (Jan 23 to Feb 20) is not flagged.
19	- Conflict: accident-date flag shows 2026-01-09 (EMS, ER) against "Date of accident per intake form: 2026-01-19" (record 7), "the tool does not choose between the dates". PT plan "12 visits" against "Discharged from PT after two missed appointments" is flagged. Both priors (record 3 low back 2023; record 8 degenerative wording) are flagged with excerpts.
20	- Every letter line has the long-format date, the provider as written, a summary, and a verbatim quote. I compared all 9 quotes with `evals/golden/sample.txt`. Each is an exact substring.
21	- Every charge line prints `date of service [__________] (record dated X)`, the D-073 fallback format. Two blanks plus `[Ex. __ / Bates __]` on each source line. After you fill them in, the letter is sendable.
22	- Letter downloaded as .txt: same text as the screen. No HTML, markdown, "verified" or other UI words. Flags, notes and "Bills to request" appear only in the internal block.
23	- Bates panel: Exhibit A, prefix RIV, start 1 turns record 2 into `[Ex. A / Bates RIV0002]`, MRI into RIV0008. Correct mapping.
24	- Edit, dismiss, pending, reload: I edited the record 3 summary, dismissed one flag, left one flag on "Decide later", and reloaded the page mid-review. The answer counter carried on from where I was. The letter holds my edited wording. Notes show EDITED ITEMS with the original and the new text, FLAGS DISMISSED with the dismissed flag, and PENDING ITEMS NOT INCLUDED with the undecided one. The letter was identical after a second reload.
25	
26	**case_09 (golden, demo server).** The billing statement entry came up with Yes unavailable (it holds a dollar figure), so I dismissed it; the $275 still counts from Step 3. Letter: 4 visit/phone entries and `Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00`; total $275.00. Notes: gap of 56 days, Feb 2 to Mar 30; the statement and phone note did not split the gap. The Feb 2 service date inside the statement sentence is not used for the letter date, so there is no wrong date.
27	
28	**lib10 (local server).** Letter charges are the four UB-04 line charges, $4,920.00, $2,105.00, $386.50 and $712.00, total `$8,123.50`. That equals the hand sum. Not in the total: the $1,640 rate, the 0001 repeat of $8,123.50, and every EOB figure; the CMS-1500 amounts are not in the total either. All of these are in the notes as not totaled (the CMS-1500 figures are the exception, see below). Charge lines print the blank with `(statement dated June 19, 2026)`.
29	
30	**lib11 (local server).** I ticked the two confirm boxes the app requires before the three ledger lines could be counted. Letter charges: ED $3,260.00, new patient exam $250.00, x-ray $180.00, visits 1 to 14 $2,310.00. Total `$6,000.00`, which matches `expected.json` and my hand sum. The $2,740 ledger total, the $300 payment, the -$274 adjustment and the $2,166 balance are in the notes, not in the total. Gap 35 days (Apr 24 to May 29). The 28-day interval (Mar 27 to Apr 24) is not flagged. The intake-form "Prior accidents: No" and the 2019/2022 history are both quoted in a conflict flag, and the tool does not say which is right.
31	
32	I read the letter lines for all four cases against the raw records. Every quote is a substring of its record. I found no wrong date, no wrong amount, and no total that disagrees with the hand sum.
33	
34	## Not blockers (D-075: for SCOPE_CUTS, not rated)
35	- lib10 notes say `Gap: 43 days, July 14, 2026 to August 26, 2026` from a CMS-1500 claim form. The review card carries the warning "looks like paperwork... the gap would be 49 days (July 8...)", but the notes line drops that sentence. This is the D-055 design, and earlier reviews (T-116 paralegal r4, GATE-M2 adjuster) already rated it minor or nit.
36	- lib10 letter has a chronology line `June 19, 2026 — ... UB-04 itemized bill` (the statement date) whose summary ends with the fragment "room". It is labelled a bill and its quote shows the 06/09 to 06/12 period.
37	- lib10: the card says the notes will name the CMS-1500 amounts so the paralegal can request the bill; after dismissing record 8 the notes list the record as dismissed but print none of its figures.
38	- lib10 EMS and lib11 EMS lines were disputed by the second check and accepted after I ticked "I read this line myself". The letter's Source quote then omits the sentence the summary uses ("struck at an intersection", "struck from behind"). The human gate worked as designed; widening the highlight would fix it.
39	
40	## Evidence (under artifacts/review-evidence/)
41	`GATE-M3M4-paralegal-sample-letter.txt`, `-sample-notes.txt`, `-sample-letter-bates.txt`, `-sample-cards.txt`, `-sample-bills.txt`, `-sample2.out` (timing), `-case09-letter.txt`, `-case09-notes.txt`, `-lib10-letter.txt`, `-lib10-notes.txt`, `-lib11-letter.txt`, `-lib11-notes.txt`, `-edit-letter.txt`, `-edit-notes.txt`, screenshots `GATE-M3M4-paralegal-0N-*.png`, probe scripts `GATE-M3M4-paralegal-*.py` and `gate_m3m4_lib.py`, server logs.
42	
43	```json
44	{"card": "GATE-M3M4", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
45	 "scope": "git archive f6d5c19; demo-mode app on :7931 (sample, case_09), local-mode archive server on :7932 (lib10, lib11, demo refuses them); D-075 blockers only, D-073 fallback",
46	 "exercised": [
47	  "git archive f6d5c19 into scratchpad; started demo server (ZLAYT_MODE unset, fixture backend) on 7931; /api/health showed demo_mode true",
48	  "Playwright: sample case from Open the sample case to the finished letter, keyboard A on every card, 17.4 s scripted total, draft step 1.3 s",
49	  "Read every Step 2 card and Step 3 amount for the sample against evals/golden/sample.txt and spec/SAMPLE_CASE_TRUTHS.md (total 8390, PT rate not totaled, gap 73, 28-day not flagged, 01-09 vs 01-19 conflict, plan vs discharge, two priors)",
50	  "Downloaded letter and notes as .txt, diffed against the screen text, grepped for HTML, markdown and UI words",
51	  "Set Bates panel (Ex A, prefix RIV, start 1) and checked the per-record mapping in the letter",
52	  "Edited the record 3 summary, dismissed one flag, left one flag undecided, reloaded mid-review and again at the letter; checked the letter and notes",
53	  "case_09 via POST /api/cases (golden text accepted) and the UI; letter and notes read against the raw record",
54	  "lib10 and lib11 on a local-mode archive server (demo returned 409 demo_mode_unsupported_input); drove all items, compare and separate boxes ticked where required; letters and notes read against the raw records and expected.json",
55	  "Hand arithmetic: 6240+2150=8390; 4920+2105+386.50+712=8123.50; 3260+250+180+2310=6000",
56	  "Stopped both servers by PID (53027, 59925); curl on 7931 and 7932 returns 000"
57	 ],
58	 "verdict": "pass",
59	 "scores": {"verify_quickly": 4, "totals_correct": 5, "dates_correct": 5, "letter_sendable_after_blanks": 5},
60	 "findings": [],
61	 "whats_right": [
62	  "Every charge line prints the same fillable blank with the statement or record date in parentheses, and no case printed a service date the records do not state.",
63	  "Totals match the hand sums on all four cases ($8,390, $275, $8,123.50, $6,000); the $185 rate, the 0001 repeat, EOB and ledger totals never enter a total.",
64	  "Edits, dismissals and undecided items survive reload and show up correctly in the notes (original kept, dismissed listed, pending excluded from the letter)."
65	 ],
66	 "questions_for_chris": []}
67	```
68	
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:54.745Z

**tool call — Bash**
````
{
 "command": "sed -n '1,400p' /Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/b9r69ctg6.txt | tail -n +30 | head -150",
 "description": "Read the rest of the persisted T-202 card output"
}
````

### User / tool · 2026-11-03T14:59:54.830Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:55.336Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git log --oneline -n 10 && git status --short | head -20 && git cat-file -t b50952d && git show --stat b50952d | head -40",
 "description": "Show HEAD, recent log, status and the b50952d commit stat"
}
````

### User / tool · 2026-11-03T14:59:55.545Z

**tool result**
````
a932fc9dcd627e0e5f92a234add6fc41b835a4f1
a932fc9 docs(writer): T-218 ship-bar row 5 and Part 2 cite the final suite at 43ce6eb; captions are burned in; PDFs re-rendered (1 and 4 pages)
c2dd104 fix(qa): T-184 demo.webm re-recorded at 43ce6eb (Step 3 MRI note shows the new wording), caption band below the app so Saved and Undo show; final green suite record
43ce6eb fix(backend): gate M3+M4 fix A part 2, no_date note no longer says the code reads dates; README reviews pointer
6371a28 fix(frontend): T-216 gate fix B: phone strip one row and out of the short-phone bar, Step 4 names date-of-service blanks, How page says demo second-check results were recorded; step3/step4/t211 expectations follow D-073
38655da feat(qa): T-184 burned-in captions in demo.webm (in-page caption band from the narration) + artifacts/demo.vtt; re-recorded 173 s
31122d7 docs(memory): SCOPE_CUTS row 28 states the D-073 all-blank fallback; row 29 gate non-blockers
ada93fc fix(submission): gate M3+M4 fix C, note and Part 2 state the D-073 date blank, current T-211/T-184/T-212 status, ship-bar row 5 pending re-run, video plan, snapshot-safe paths
db36531 feat(release): snapshot image allow-list keeps final screenshots, demo video and app/frontend images (T-217)
9ea3af8 docs(memory): commit decisions D-069..D-075, SCOPE_CUTS rows 24-28, lessons and progress (GATE-M3M4 PM blocker 3)
aa21b24 fix(backend): gate M3+M4 fix A, spec/api/LLM_VS_CODE/README match the D-073 blank; undated-charge notes section before BILLS TO REQUEST
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
commit
commit b50952dc6dc95d2befc463a67e55cf72bfd9b724
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Tue Nov 3 07:24:37 2026 -0600

    feat(backend): T-202 r7 D-073 fallback applied: the letter and Step 3 print the fillable blank on every charge line, no service date extracted; letter_check requires the blank form; reader kept as service_date.read (SCOPE_CUTS 28)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/export.py                           |  34 +-
 app/backend/service_date.py                     |  16 +-
 evals/golden/sample.export.expected.txt         |   3 +-
 evals/letter_check.py                           | 389 +------------------
 memory/contracts/api.md                         |   2 +-
 tests/e2e/guided/test_t205.py                   |  13 +-
 tests/e2e/test_charge_confirm.py                |   2 +-
 tests/unit/test_t200_undated_charge_label.py    |  13 +-
 tests/unit/test_t202_charge_service_dates.py    | 111 ------
 tests/unit/test_t202_r2_service_date_layouts.py | 360 ------------------
 tests/unit/test_t202_r3_allow_list.py           | 397 --------------------
 tests/unit/test_t202_r4_encounter.py            | 334 -----------------
 tests/unit/test_t202_r5_d073.py                 | 475 ------------------------
 tests/unit/test_t202_r6_d073.py                 | 423 ---------------------
 tests/unit/test_t202_r7_all_blank.py            |  78 ++++
 15 files changed, 136 insertions(+), 2514 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T14:59:59.126Z

**tool call — Bash**
````
{
 "command": "F=/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/b311qgbfb.txt; wc -l $F; grep -n \"Notes (append-only\" $F; awk 'NR>=1' $F | grep -n \"\" | sed -n '1,12p' | cut -c1-600; echo ....; grep -n \"^- 2026-11-03T1[4-9]\\|^- 2026-11-03T0[89]\\|^- 2026-11-03T2\\|^- 2026-11-03T1[0-3]\" $F | cut -c1-900 | tail -n 30; echo; git merge-base --is-ancestor b50952d HEAD && echo ANCESTOR_OK; git log --oneline b50952d..HEAD | wc -l; git log --oneline b50952d..HEAD",
 "description": "Extract recent card notes and check b50952d is an ancestor of HEAD"
}
````

### User / tool · 2026-11-03T14:59:59.178Z

**tool result (error)**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:02.738Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer && cat reviewer-hook-constraints.md feedback_reviewer_tooling_quirks.md t202-r5-d073-patterns.md 2>/dev/null | head -150; ls | head -80",
 "description": "Read reviewer hook constraint and tooling quirk memories"
}
````

### User / tool · 2026-11-03T15:00:02.824Z

**tool result**
````
---
name: reviewer-hook-constraints
description: Bash hooks that block reviewer commands in this repo (board.py --help, python -c containing backticks) and the workarounds
metadata:
  type: reference
---

- board-guard: reviewers may run only `tools/board.py validate|show|list|status`. `--help` is rejected.
- git-guard fails to parse `python3 -c "..."` when the code contains escaped backticks. Use a quoted heredoc (`python3 - <<'EOF'`) and build the fence as '`'*3.
- Write access is limited to reviews/ and artifacts/review-evidence/ (plus this memory dir). Probe scripts go in artifacts/review-evidence/.
- T-118 (2026-11-02): the Write tool is refused for the session scratchpad (reviewer-write-guard), and board-guard refuses `mkdir` there. A Bash `git archive | tar -x` into the scratchpad still worked. Put scripts and output dirs under artifacts/review-evidence/ and run archive copies from the scratchpad. Run them with `.venv/bin/python -I` and a runner that puts the archive root first on sys.path.

**How to apply:** use these forms directly to avoid wasted tool calls. Related: [[golden-set-recurring-findings]]
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
- `reviewer-write-guard` also refuses Write to the session scratchpad ("reviewers write only under reviews/ or artifacts/review-evidence/").
  Put probe copies, extracted archives and JSON checkers under artifacts/review-evidence/ (run with `.venv/bin/python -I`). `git archive`
  extraction into the scratchpad via Bash worked.
- The review file was refused a second write once it existed, so a wrong body sentence (I wrote "a scratchpad archive path that no longer
  exists" without checking it, and mislabeled a record) could not be fixed. Before the single Write: `ls` every path and grep every record
  label you quote.
- `bash python3 -c "... \`\`\` ..."` was denied again by git-guard. The JSON check now lives in artifacts/review-evidence/<card>-paralegal-r2-jsoncheck.py.

## T-114 r2 additions (2026-11-02)
- `nohup .venv/bin/python -m app.main ... &` then `kill $!` left the listener alive: the launcher PID exited, and the server
  (a child, re-parented to launchd, ppid 1) kept 7881 open and returned 200. Always `lsof -iTCP:<port> -sTCP:LISTEN -nP` after a
  kill, kill the listener PID too, and confirm `curl` returns 000. Name both PIDs in the review scope.
- reviewer-write-guard refused an Edit on reviews/T-114-paralegal-r2.md (append-only). A wrong scope PID could not be fixed; it went into the final reply.
  Before the single Write, check every PID, path and count with a command, not from memory.
- The board validator only checks files under reviews/. Pre-check a draft JSON with a script in artifacts/review-evidence/ (T-114-r2-paralegal-jsoncheck.py).

## T-116 r3 additions (2026-11-02)
- The r3 review was written once and then contained one wrong claim (a grep "returns 1 from the H3V5 line only" that was actually the line-29
  orchestrator note). Edit on the existing review was refused by `reviewer-write-guard`, so the erratum went into the final reply instead.
  Rule: before the single Write, run the exact grep again and quote its line numbers; do not describe a match you have not printed.
- `python3 -c` with `\`\`\`json` in the string was denied by git-guard again (parse error). The JSON check is `artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py`
  run with `.venv/bin/python -I <script> <review>`; it works for any review path.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider` keeps the dirty project tree free of new .pytest_cache and .pyc writes.

## T-120 r4 additions (2026-11-02)
- git-guard denies `git show "$c:$f"` and any git call with a shell variable in the subcommand or a `for` loop with `${var%%:*}` ("dynamic git subcommand is not allowed", "unresolved variable in command position"). Use literal git commands, or a script under artifacts/review-evidence/ run with `.venv/bin/python -I` (T-120-r4-archive-check.py does this).
- The Write tool and board-guard accept a `cp` of a finished draft from artifacts/review-evidence/ to reviews/<new file>; that let me proof a draft JSON with the jsoncheck and then publish the identical text in one step.
- `kill` by PID, then `lsof -iTCP:<port> -sTCP:LISTEN -nP` (exit 1 = closed) and `curl` 000, worked for four server pairs.

## T-120 r2 additions (2026-11-02)
- The guard refused Edit on reviews/T-120-paralegal-r2.md right after the single Write (the name has no -rN suffix, so it is treated as existing and append-only). Two wording slips were found after the Write: "lib02 and lib11 keep their prior flags" (I had not compared them to the pre-T-120 build) and "r2 handoff" (the line is the r2 backend note). They could not be fixed in the file; they went into the one-line reply.
- Before the Write, check each "keeps / still / unchanged" claim against a run you have actually done, not against memory of the build.

## T-060 pass 5 additions (2026-11-02)
- Playwright `new_page` with a fresh browser context is a fresh visit, not a reload; a same-page `pg.reload()` does restore the case. Probe a reload in the same page.
- Letter keys do nothing until an item is selected: after opening a case, click Start review (or a row edge) before j, a, d.
- Probe scripts that walk with j/a can stop early because `a` auto-advances within a kind; check the focus item after every key and reach skipped items with k or j, not by assumption.
- A ```json regex that captures a trailing colon in an evidence path reports a false "missing path"; the file exists. Strip `:` in the checker.
- Write the draft under artifacts/review-evidence/<card>-paralegal-pass5/, run the jsoncheck, then `cp` to reviews/ in one Bash call; board.py validate returned "ok (1 file(s))".
---
name: t202-r5-d073-patterns
description: T-202 r5 (f9c0faf, D-073 two-source fallback) fail: study/service words in encounter list (MRI, X-Ray, Follow-Up, Exam, Evaluation) let provider names lend statement dates; '(statement dated X)' on ED records; key-value DOS line read as column heading
metadata:
  type: project
---

Review file: reviews/T-202-paralegal-r5.md (f9c0faf). Verdict: fail, with 1 blocker, 2 majors and 3 minors.

**Fixed by D-073.** At the resolver, 114 of the 115 r1-r4 probes give the right date, a period that covers it, or the blank. The exception is r4 S7, a bill under the label "..., cervical MRI"; its "Amount due" is filed as a balance, so it never reaches the letter. In the corpus, 22 of 37 lines became blanks and no dated line changed. Dotted leaders now work on the case path.

**Blocker: the encounter list keeps service words.** It still holds service/study words (mri, x-ray, follow-up, evaluation, exam, visit), matched anywhere in Source. Provider names like "Austin MRI" or "Hobbleton Follow-Up Clinic" therefore lend their statement date. letter_check shares the table, so it rejects the blank. Same result on the parent; this is the r4 blocker 3 class.

**Majors**
- not_stated_text always writes "(statement dated X)". 19 of the 22 blanks sit on ED/UC records, and step3.js:37 says the date "is the statement date, not the service date".
- A "Date of service: X  Account: N" line sits right over an un-headed row and is read as the row's column heading (service_date.py:263), so the row's other date prints.

**Mechanics that worked**
- Fixture-backend letters_for drops amounts from unrecorded text that the classifier calls a balance or "names no service". Phrase probes as "<service> CPT <code>, charge $X" so they reach the letter.
- fullpipe_r5.py takes ONLY= and runs on any archive.
- Port 7985, PID 4950.

**Why:** each allow/deny list moves risk to a neighbouring shape. Next round:
- Probe provider names built from each remaining encounter word.
- Probe the blank's parenthetical against the record kind.

**How to apply:**
- Scripts are in artifacts/review-evidence/T-202-paralegal-r5/. probe_r5.py loads r2-r4 by ast (PROBES and the r4 NEW list).
- corpus_blanks.py diffs any two archives.

Related: [[t202-r4-encounter-patterns]], [[t200-undated-charge-label]].
MEMORY.md
d041-date-gate-patterns.md
feedback_reviewer_tooling_quirks.md
feedback_spec_review_patterns.md
frontend-review-patterns.md
gate-m2-r2-patterns.md
gate-m3-patterns.md
golden-set-recurring-findings.md
library-review-patterns.md
manual-entry-split-review-patterns.md
record-format-review-patterns.md
reviewer-api-shape-gotchas.md
reviewer-hook-constraints.md
reviewer-run-pitfalls-pass4.md
t060-pass4-state-patterns.md
t060-pass5-state-patterns.md
t060-ui-polish-patterns.md
t068-dates-to-confirm-patterns.md
t079-library-v2-patterns.md
t114-r3-gap-change-persistence.md
t114-rates-gap-patterns.md
t116-gap-endpoint-patterns.md
t118-lib11-truth-patterns.md
t120-123-patterns.md
t120-r2-patterns.md
t120-r3-patterns.md
t120-r4-patterns.md
t136-r2-t142-patterns.md
t149-r2-overview-patterns.md
t181-guided-ui-patterns.md
t181-r2-patterns.md
t200-undated-charge-label.md
t202-d071-service-date-patterns.md
t202-r2-non-service-date-patterns.md
t202-r3-allow-list-patterns.md
t202-r4-encounter-patterns.md
t202-r5-d073-patterns.md
t202-r6-encounter-other-time-patterns.md
t209-confirm-sentence-patterns.md
t209-r3-patterns.md
t209-r4-patterns.md
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:07.271Z

**tool call — Bash**
````
{
 "command": "ls reviews | grep -i \"T-202\" ; ls artifacts/review-evidence | grep -i \"T-202\" | head; git merge-base --is-ancestor b50952d HEAD && echo ANCESTOR_OK; git log --oneline b50952d..HEAD",
 "description": "List existing T-202 reviews and evidence, check b50952d ancestry"
}
````

### User / tool · 2026-11-03T15:00:07.519Z

**tool result**
````
T-202-gate-M3M4.md
T-202-paralegal-r2.md
T-202-paralegal-r3.md
T-202-paralegal-r4.md
T-202-paralegal-r5.md
T-202-paralegal-r6.md
T-202-paralegal.md
T-202-staff-engineer-r2.md
T-202-staff-engineer-r3.md
T-202-staff-engineer-r4.md
T-202-staff-engineer-r4b.md
T-202-staff-engineer-r5.md
T-202-staff-engineer.md
T-202-paralegal
T-202-paralegal-r2
T-202-paralegal-r3
T-202-paralegal-r4
T-202-paralegal-r5
T-202-paralegal-r6
T-202-staff
T-202-staff-r2
T-202-staff-r3
T-202-staff-r4
ANCESTOR_OK
a932fc9 docs(writer): T-218 ship-bar row 5 and Part 2 cite the final suite at 43ce6eb; captions are burned in; PDFs re-rendered (1 and 4 pages)
c2dd104 fix(qa): T-184 demo.webm re-recorded at 43ce6eb (Step 3 MRI note shows the new wording), caption band below the app so Saved and Undo show; final green suite record
43ce6eb fix(backend): gate M3+M4 fix A part 2, no_date note no longer says the code reads dates; README reviews pointer
6371a28 fix(frontend): T-216 gate fix B: phone strip one row and out of the short-phone bar, Step 4 names date-of-service blanks, How page says demo second-check results were recorded; step3/step4/t211 expectations follow D-073
38655da feat(qa): T-184 burned-in captions in demo.webm (in-page caption band from the narration) + artifacts/demo.vtt; re-recorded 173 s
31122d7 docs(memory): SCOPE_CUTS row 28 states the D-073 all-blank fallback; row 29 gate non-blockers
ada93fc fix(submission): gate M3+M4 fix C, note and Part 2 state the D-073 date blank, current T-211/T-184/T-212 status, ship-bar row 5 pending re-run, video plan, snapshot-safe paths
db36531 feat(release): snapshot image allow-list keeps final screenshots, demo video and app/frontend images (T-217)
9ea3af8 docs(memory): commit decisions D-069..D-075, SCOPE_CUTS rows 24-28, lessons and progress (GATE-M3M4 PM blocker 3)
aa21b24 fix(backend): gate M3+M4 fix A, spec/api/LLM_VS_CODE/README match the D-073 blank; undated-charge notes section before BILLS TO REQUEST
cc9386a test(qa): gate M3+M4 full-suite results on f6d5c19 (D-075)
5974034 feat(qa): T-184 re-capture at f6d5c19: letter charge blank, one-statement panel, Found by code tag; 72 shots, 174 s video, captions and narration updated
f6d5c19 feat(frontend): T-214 a flag only code found shows its origin label, not the Prepared answer tag; the how-checked panel says the same
d15c9ab fix(backend): flags found only by code are not prepared answers (T-214)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:08.230Z

**tool call — Bash**
````
{
 "command": "grep -n \"^- 2026-11-03T1[3-9]\\|^- 2026-11-03T0[89]\\|^- 2026-11-03T2\" /Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/b311qgbfb.txt | cut -c1-1200",
 "description": "Show the latest T-202 card notes from the persisted card output"
}
````

### User / tool · 2026-11-03T15:00:08.314Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:24.814Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-202-paralegal-r7/archive && git archive a932fc9 | tar -x -C artifacts/review-evidence/T-202-paralegal-r7/archive && ls artifacts/review-evidence/T-202-paralegal-r7/archive && cd artifacts/review-evidence/T-202-paralegal-r7/archive && git -C /Users/arsis/zlayt-pm-project rev-parse a932fc9^{tree} && grep -n \"D-073\" /Users/arsis/zlayt-pm-project/memory/ORCHESTRATOR_DECISIONS.md | head -20",
 "description": "Extract git archive of HEAD a932fc9 into review-evidence and find D-073"
}
````

### User / tool · 2026-11-03T15:00:26.078Z

**tool result**
````
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
app
artifacts
board
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
run.sh
spec
submission
tests
tools
5f74b7377e5fd55b9be2beb47090b9b0dfbc812d
97:## D-073 — Service dates: the pre-declared conservative fallback (§7.4 after T-202 r4)
99:- D-073 clarification (staff r4 question, decided per rule 1): an encounter record is identified only by a document-type word (visit/progress/office note, ED/ER record, discharge summary, PT/therapy note, ambulance run report, operative report); a provider name (clinic, ED, orthopedics, urgent care, imaging) is never enough. About 19 of 84 corpus charge lines then print the fillable blank; accepted.
100:- D-073 round-6 rules (§7.4, final; staff r5 + paralegal r5): (1) encounter_types.json holds whole document-type phrases only ("MRI report", "progress note", "emergency department record", "physical therapy note", "ambulance run report", "operative report", "discharge summary", "office visit note"); no single words (MRI, exam, evaluation, follow-up, new patient), because they occur in provider names; (2) a date-of-service column needs a real table: a header row naming at least two columns including the DOS column, and at least two data rows with a date in that column position; a lone "Date of service: X" line or a sentence mentioning DOS is not a heading; (3) several candidate dates, a month-year phrase or an "earlier/next/previous" phrase in the encounter sentence -> blank, each pinned by a test; the UB-04 period gets the same guard; (4) a blank on a non-bill record reads "(record dated X)", on a bill "(statement dated X)"; (5) the duplicate-promotion flag message never prints a prose date. The sample truths fix no charge dates, so sample lines may become blanks. If round 6 still prints a wrong date, the MVP letter prints the fillable blank on every charge line (no date extraction at all) and SCOPE_CUTS 28 covers it.
104:- D-073 fallback applied (T-202 r6 paralegal fail: a visit note lends its date to another visit's charge; a UB-04 period overrides a line's own date). Per the pre-declared rule the MVP letter prints the fillable blank "date of service [__________] (record|statement dated X)" on every charge line; no service date is extracted for the letter. Step 3 shows the same. SCOPE_CUTS 28 covers date extraction.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:30.836Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && wc -l app/backend/service_date.py app/backend/export.py evals/letter_check.py && git -C /Users/arsis/zlayt-pm-project show a932fc9:app/backend/service_date.py | head -120; ls /Users/arsis/zlayt-pm-project/.venv/bin/python",
 "description": "Read the head of service_date.py at HEAD and confirm venv python exists"
}
````

### User / tool · 2026-11-03T15:00:30.942Z

**tool result**
````
     462 app/backend/service_date.py
     927 app/backend/export.py
     314 evals/letter_check.py
    1703 total
"""The service date a charge line prints (D-073). FALLBACK APPLIED after round 6: `resolve` never returns a date. Every charge line prints the fillable blank and the paralegal fills it from the quote;
the two-source reader described below is kept as `read` (SCOPE_CUTS row 28) and is not called by the letter, the case view or the notes. Code only, no LLM (LLM_VS_CODE rows 2 and 3).

A charge line takes its date of service from EXACTLY TWO sources:
  (1) its own row's date cell in a REAL bill table: a header row of short labels (two or more) that names the date of service as a whole cell (DOS, date of service, service date, visit date, 24A ...),
      with at least two data rows that hold a date in that column and the same number of cells as the header; or the CMS-1500 24A 'From' / 'To' cells of such a table, or the UB-04
      'statement covers period FROM ... THROUGH ...' of one period, none of it about another statement; printed as a range. A 'Date of service: X' line, a key-value line or a sentence that mentions DOS is not a heading;
  (2) the record's own date, ONLY when the record is positively identified as an encounter record by a WHOLE document-type phrase in its source label (`record_kind`, the table
      app/backend/encounter_types.json: progress note, discharge summary, emergency department record, MRI report, ambulance run report, operative report ...; no single word, a provider's name is
      never enough), and the charge's own sentence holds at most that one date, no count of visits, no month-year phrase and no 'earlier / next / previous' phrase.
Prose is NOT read: 'DOS 01/09/2026', 'visit of', 'Treatment dates A to B', 'next visit date' ... inside a sentence never give a date (SCOPE_CUTS row 28). Every other line prints the fillable blank
'date of service [__________] (statement dated X)' on a bill, '(record dated X)' on any other record, and the Step 3 note; the paralegal fills it from the quote. The result of `resolve` is one of:
  - `stated`: a date or complete period from source (1), or the record's own date from source (2);
  - `not_stated` with reason `no_date` / `non_service_date`: the line has no date of source (1) or (2) (`non_service_date` names the one date the code saw but does not read);
  - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): a DOS-column cell the code cannot read with certainty;
    the note names the date as the column writes it.
Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
import datetime as _dt
import json
import pathlib
import re

from app.backend import amounts as AM

TYPES_PATH = pathlib.Path(__file__).with_name("encounter_types.json")          # D-071 amendment 2: the one declared table of record types (also read by evals/letter_check.py)
_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))


def _tokens(text: str) -> list:
    return re.findall(r"[^\W_]+", (text or "").lower())


def _phrase_rx(terms):
    return re.compile(r"(?<= )(?:" + "|".join(" ".join(re.escape(t) for t in _tokens(term)) for term in sorted(terms, key=len, reverse=True)) + r")(?= )")


_FIN, _ADMIN, _ENC = (_phrase_rx(_TYPES[k]) for k in ("financial", "administrative", "encounter"))
_OPEN = int(_TYPES["opening_chars"])


def _hit(rx, text) -> bool:
    return bool(rx.search(" " + " ".join(_tokens(text)) + " "))


def record_kind(source, excerpt: str = "") -> str:
    """'bill' | 'encounter' | 'other' (D-071 amendment 2). A bill is what amounts.billing_document says or what the declared table calls financial in the source label or the first
    characters of the excerpt, up to its first colon or full stop ('Receipt:', 'Charges:', 'Account summary:'); an administrative paper (phone note, letter, affidavit) is 'other'; an ENCOUNTER needs a positive
    identification by a DOCUMENT-TYPE word in the source label (visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, run report, operative report ...; D-073: a provider
    name such as Clinic, ED, Urgent Care, Imaging, Orthopedics is never enough). Anything else is of unknown type ('other'). Only an encounter lends its header date."""
    src, opening = source or "", re.split(r"[:.\n]", (excerpt or "")[:_OPEN])[0]
    if AM.billing_document(src, excerpt or "") or _hit(_FIN, src) or _hit(_FIN, opening):
        return "bill"
    if _hit(_ADMIN, src) or _hit(_ADMIN, opening):
        return "other"
    return "encounter" if _hit(_ENC, src) else "other"

_MON = AM._MON
_ORD = r"(?:st|nd|rd|th)?"
_DASH = "–—"
_TOK = re.compile(
    r"(?<![\w/$])(?:"
    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
    r"|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2}))"
    rf"|(?P<mper>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}\s*[-{_DASH}]\s*(?:(?:{_MON})\.?\s+)?\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
    rf"|(?P<mdy>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}(?:,?\s+\d{{4}}|,\s*\d{{2}}(?!\d))?)"
    rf"|(?P<dmy>\d{{1,2}}{_ORD}[\s-]+(?:of\s+)?(?:{_MON})\.?[\s-]*,?\s*\d{{4}})"
    r"|(?P<md>\d{1,2}/\d{1,2}(?!\s*(?:hrs?|hours?|units?|miles?|mins?|visits?|sessions?)\b))"
    r")(?![\w/]|\.\d)", re.IGNORECASE)
_JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
_LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
# ---- D-073: the only evidence that reads a date. A column heading over the date cell (below), the UB-04 'statement covers period' span, and nothing in a sentence.
_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(\u00b7]*$"          # a label, then spaces, a colon or a dotted leader (masked to middle dots, `_mask_leaders`), then the date
_WINDOW = 60                     # characters before a date that may hold the UB-04 span label and the leader after it
_mask_leaders = AM.mask_leaders          # the one helper: a dotted leader is neither a sentence end nor a column gap (T-209 r2)


_UB_SPAN = re.compile(r"\bstatement\s+(?:covers\s+)?period" + _LBL_END, re.IGNORECASE)       # UB-04 FL6 'Statement Covers Period FROM ... THROUGH ...': the span of the services of a coded line
_UB = re.compile(r"\bub-?04\b|\btype\s+of\s+bill\b|\bFL\s?\d{1,2}\b|\bUB\s?92\b", re.IGNORECASE)
# a column heading that names service (a CMS-1500 24A 'From'/'To' under 'Date(s) of Service', 'Service From', 'DOS' ...). A bare 'Date', 'Entry date', 'Transaction Date', 'Posted' ... does not.
_H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter\s+date|"
                    r"\b(?:service|svc)\s+(?:from|to|thru|through)\b|\b(?:from|to|thru|through)\s+(?:dos|service|svc)\b|\b24\s*-?a\b", re.IGNORECASE)
_H_CELL = re.compile(r"^(?:24\s*-?a\s*)?(?:dos|svc|date\(?s?\)?\s+of\s+(?:service|visit)(?:\s*\(dos\))?|(?:service|svc)\s+date|visit\s+date|encounter\s+date)(?:\s+(?:from|to|thru|through))?$"
                     r"|^(?:service|svc)\s+(?:from|to|thru|through)$|^(?:from|to|thru|through)\s+(?:dos|service|svc)$|^24\s*-?a$", re.IGNORECASE)      # a WHOLE heading cell that names the service
_ITEM_NO = re.compile(r"\b\d{1,2}[A-Za-z]\b|\bFL\s?\d{1,2}\b")          # a form item number ('24A', 'FL 6'): the only digit a heading cell may hold
# another time named in a sentence: an encounter note whose charge sentence says so lends nothing (D-073 round 6, rule 3); the same words guard a UB-04 statement period
_MONTH_YEAR = re.compile(rf"\b(?:{AM._MON})\.?,?\s+(?:of\s+)?(?:19|20)\d\d\b", re.IGNORECASE)          # 'October 2025', 'Oct. 2025' (the sentence split falls after 'Oct.', so the look-ahead below reads past it)
_OTHER_TIME = re.compile(r"\b(?:earlier|previous|previously|prior|next|last|later|ago|former|subsequent)\b|\bbalance\s+forward\b|"
                         rf"\b(?:{AM._MON})\.?,?\s+(?:of\s+)?(?:19|20)\d\d\b|(?<![\d/])\d{{1,2}}/(?:19|20)\d\d(?![\d/])", re.IGNORECASE)
_YEARS_BEFORE = 5                # a bill's service date more than this many years before its statement is doubtful

REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "implausible", "non_service_date", "no_date", "not_read")
WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)


def display(first, last=None) -> str:
    """'June 9, 2026' for one day; a period as a range: 'June 9–12, 2026', 'June 28–July 2, 2026', 'December 30, 2026–January 2, 2027' (D-071)."""
    def lng(iso):
        d = _dt.date.fromisoformat(iso)
        return f"{d.strftime('%B')} {d.day}, {d.year}"
    if not last or last == first:
        return lng(first)
    a, b = _dt.date.fromisoformat(first), _dt.date.fromisoformat(last)
    if (a.year, a.month) == (b.year, b.month):
        return f"{a.strftime('%B')} {a.day}–{b.day}, {a.year}"
    if a.year == b.year:
        return f"{a.strftime('%B')} {a.day}–{b.strftime('%B')} {b.day}, {a.year}"
    return f"{lng(first)}–{lng(last)}"


BLANK = "date of service [__________]"


def date_label(kind: str) -> str:
    """What the record's own date is called next to the blank (D-073 round 6, rule 4): a bill's is its 'statement' date; any other record's is the 'record' date."""
    return "statement" if kind == "bill" else "record"


def not_stated_text(statement_iso, kind: str = "bill") -> str:
    """The text the letter puts after the provider when no service date is certain (D-071 addendum): a fillable blank, like the Bates placeholder, never an inferred date. The
/Users/arsis/zlayt-pm-project/.venv/bin/python
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:32.323Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && sed -n '120,200p' app/backend/service_date.py",
 "description": "Read the rest of the not_stated_text and resolve path in service_date.py"
}
````

### User / tool · 2026-11-03T15:00:32.404Z

**tool result**
````
    """The text the letter puts after the provider when no service date is certain (D-071 addendum): a fillable blank, like the Bates placeholder, never an inferred date. The
    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)' on a bill, '(record dated June 15, 2026)' on any other record."""
    if statement_iso:
        return f"{BLANK} ({date_label(kind)} dated {display(statement_iso)})"
    return BLANK


def printed_text(res: dict, statement_iso, kind: str = "bill") -> str:
    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
    return not_stated_text(statement_iso, kind)


_WHY = {
    "ambiguous_numeric": "The date of service column of the bill reads {raw}, which can be read as month/day or day/month; the record does not settle which.",
    "two_digit_year": "The date of service column of the bill reads {raw}, which has a two-digit year; the code does not guess the century.",
    "no_year": "The date of service column of the bill reads {raw}, which states no year; the code does not borrow one from the statement.",
    "invalid": "The date of service column of the bill reads {raw}, which is not a complete date on the calendar.",
    "several_dates": "The date of service column of the bill holds more than one date ({raw}) and nothing says which one belongs to this charge.",
    "implausible": "The date of service column of the bill reads {raw}, but that date is after the statement it appears on or years before it.",
    "non_service_date": "The line shows {raw}, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service.",
    "no_date": "The letter does not take a date of service from the records.",
    "not_read": "The letter does not take a date of service from the records.",
}
_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated itemized bill, and fill the blank before you rely on it."


def confirm_note(reason, raw) -> str:
    """The Step 3 note and the internal-notes line for a charge whose service date is not certain: why, and what the letter does (D-071 amendment)."""
    return _WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") + (_ASK_WRITTEN if reason in WRITTEN else _ASK_NONE)


def _iso(y, mo, d):
    try:
        return _dt.date(y, mo, d).isoformat() if 1900 <= y <= 2100 else None
    except ValueError:
        return None


class _Tok:
    __slots__ = ("start", "end", "raw", "kind", "fixed", "ambiguous", "order", "flaw", "first", "last")

    def __init__(self, m):
        self.start, self.end, self.raw, self.kind = m.start(), m.end(), m.group(0), m.lastgroup
        self.fixed, self.ambiguous, self.order, self.flaw, self.first, self.last = None, None, None, None, None, None
        getattr(self, "_" + self.kind)(m.group(0))
        if self.flaw is None and not (self.fixed or self.ambiguous or self.first):
            self.flaw = "invalid"

    def _iso(self, s):
        y, mo, d = (int(x) for x in s.split("-"))
        self.fixed = _iso(y, mo, d)

    def _num(self, s):
        a, b, y = re.split(r"[/.-]", s)
        if len(y) == 2:
            self.flaw = "two_digit_year"
            return
        a, b, y = int(a), int(b), int(y)
        md, dm = _iso(y, a, b), _iso(y, b, a)
        if md and dm and md != dm:
            self.ambiguous = {"MD": md, "DM": dm}
        elif md or dm:
            self.fixed = md or dm
            self.order = None if (md and dm) else ("MD" if md else "DM")

    def _mdy(self, s):
        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}})|,\s*(\d{{2}}))?$", s, re.IGNORECASE)
        if m.group(4):
            self.flaw = "two_digit_year"
            return
        if not m.group(3):
            self.flaw = "no_year"
            return
        self.fixed = _iso(int(m.group(3)), _mon(m.group(1)), int(m.group(2)))

    def _dmy(self, s):
        m = re.match(rf"(\d{{1,2}}){_ORD}[\s-]+(?:of\s+)?({_MON})\.?[\s-]*,?\s*(\d{{4}})$", s, re.IGNORECASE)
        self.fixed = _iso(int(m.group(3)), _mon(m.group(2)), int(m.group(1)))

    def _md(self, s):
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:34.188Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && grep -n \"def \\|statement_iso\\|record_kind\\|def resolve\" app/backend/service_date.py | sed -n '1,200p' | tail -60; echo ----; sed -n '/^def resolve/,/^def [a-z_]*(/p' app/backend/service_date.py | head -80",
 "description": "Locate resolve and read/record-date functions in service_date.py"
}
````

### User / tool · 2026-11-03T15:00:34.292Z

**tool result**
````
8:  (2) the record's own date, ONLY when the record is positively identified as an encounter record by a WHOLE document-type phrase in its source label (`record_kind`, the table
30:def _tokens(text: str) -> list:
34:def _phrase_rx(terms):
42:def _hit(rx, text) -> bool:
46:def record_kind(source, excerpt: str = "") -> str:
96:def display(first, last=None) -> str:
98:    def lng(iso):
114:def date_label(kind: str) -> str:
119:def not_stated_text(statement_iso, kind: str = "bill") -> str:
122:    if statement_iso:
123:        return f"{BLANK} ({date_label(kind)} dated {display(statement_iso)})"
127:def printed_text(res: dict, statement_iso, kind: str = "bill") -> str:
129:    return not_stated_text(statement_iso, kind)
147:def confirm_note(reason, raw) -> str:
152:def _iso(y, mo, d):
162:    def __init__(self, m):
169:    def _iso(self, s):
173:    def _num(self, s):
186:    def _mdy(self, s):
196:    def _dmy(self, s):
200:    def _md(self, s):
203:    def _mper(self, s):
216:def _mon(name):
223:    def __init__(self, toks):
227:    def raw(self, text):
231:def _units(text: str) -> list:
245:def _certain(unit: _Unit, ref):
271:def _cells(line: str) -> list:
276:def _is_label(cell: str) -> bool:
282:def _pure_dates(cell: str) -> bool:
291:def _grid(excerpt: str, row_ls: int):
322:def _table_dates(excerpt, a_start):
341:def _plausible(first, last, ref) -> bool:
349:def _decide(units, text, ref):
368:def _apply(out: dict, res) -> dict:
380:def _sentence_at(text: str, pos: int) -> str:
387:def _from_to(pairs):
406:def resolve(excerpt: str, start: int, source, date_iso) -> dict:
416:def read(excerpt: str, start: int, source, date_iso) -> dict:
427:    kind = record_kind(source, excerpt)
----
def resolve(excerpt: str, start: int, source, date_iso) -> dict:
    """D-073 FALLBACK (T-202 round 6 failed on a visit note that lent its date to another visit's charge and a UB-04 period that overrode a line's own date): the letter and Step 3 NEVER
    carry a service date. Every charge line is `not_stated` and prints the fillable blank; the paralegal fills it from the quote. The reader below (`read`) stays for the day date extraction
    returns (SCOPE_CUTS row 28); a line it would have dated gets the reason `not_read`, any other keeps the reason it found."""
    out = read(excerpt, start, source, date_iso)
    if out["state"] == "stated":
        out.update(state="not_stated", first=None, last=None, reason="not_read", raw="", raws=[])
    return out


def read(excerpt: str, start: int, source, date_iso) -> dict:
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:36.621Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && grep -n \"charge_service_date\\|printed_text\\|not_stated_text\\|statement_iso\\|date_iso\" app/backend/*.py | head -60",
 "description": "Trace where charge_service_date and the date label are wired"
}
````

### User / tool · 2026-11-03T15:00:36.704Z

**tool result**
````
app/backend/amounts.py:357:    return any(classify(ex, a, injection=bool(r.get("injection_tag")), source=r.get("source"), date_iso=r.get("date_iso")) == "charge" for a in find_amounts(ex))
app/backend/amounts.py:492:def charge_basis(excerpt: str, amount: dict, source: str = None, date_iso: str = None, note_block: str = None) -> dict:
app/backend/amounts.py:511:        ds = _dates_in(segtext, date_iso)
app/backend/amounts.py:518:        ds = _dates_in(before, date_iso)
app/backend/amounts.py:522:            td = _dates_in(tail_text, date_iso, tail=True)
app/backend/amounts.py:525:        strip = strip + ([(len(before) + s, len(before) + e) for s, e, _ in _dates_in(tail_text, date_iso, tail=True)] if _TAIL_LEAD.match(tail_text) else [])
app/backend/amounts.py:547:            if earlier and not _dates_in(excerpt[amts[earlier[-1]]["end"]:a["start"]], date_iso):      # the line's own charge is its first figure; a later one needs a date of its own
app/backend/amounts.py:551:            dos, out["dos_end"] = _record_period(excerpt[:se], date_iso)          # D-071: a period keeps its end date for the letter
app/backend/amounts.py:561:    out["dos"] = dos or date_iso
app/backend/amounts.py:585:def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None, date_iso: str = None, strict: bool = True, note_block: str = None) -> str:
app/backend/amounts.py:588:    then D-060 default-deny: a charge only on an itemized service line (`charge_basis`), else unclear. `source` is the record's header label and `date_iso`
app/backend/amounts.py:605:        return "charge" if charge_basis(excerpt, amount, source, date_iso, note_block)["ok"] else "unclear"
app/backend/amounts.py:650:def not_totaled_reason(excerpt: str, raw: str, cents, source: str = None, date_iso: str = None, pos: int = None, records: list = None):
app/backend/amounts.py:662:        return charge_basis(excerpt, a, source, date_iso, block)["reason"]
app/backend/amounts.py:721:def not_counted(excerpt: str, raw: str, cents, source: str = None, date_iso: str = None, pos: int = None, records: list = None, kind: str = "unclear",
app/backend/amounts.py:744:    basis = charge_basis(excerpt, a, source, date_iso, note_charge_block(records, {"source": source, "excerpt": excerpt}))
app/backend/amounts.py:954:    """All amounts of a case from ingested records (needs n, excerpt; uses date_iso, source, injection_tag, text, char_start when present).
app/backend/amounts.py:965:        found = [{**a, "cls": classify(r["excerpt"], a, injection=bool(r.get("injection_tag")), source=r.get("source"), date_iso=r.get("date_iso"), note_block=block)}
app/backend/amounts.py:968:            a["basis"] = charge_basis(r["excerpt"], a, r.get("source"), r.get("date_iso"), block) if a["cls"] == "charge" else None
app/backend/amounts.py:974:            rows.append({"record_no": r["n"], "text": r["excerpt"], "date": r.get("date_iso"), "provider": r.get("source"), "raw": a["raw"], "cents": a["cents"],
app/backend/case_list.py:72:    for r in conn.execute("SELECT source_label, date_iso FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
app/backend/case_list.py:75:            day = datetime.date.fromisoformat(r["date_iso"]).strftime("%b %-d, %Y") if r["date_iso"] else None
app/backend/case_list.py:143:    recs = {r["id"]: (r["date_iso"], r["seq"]) for r in conn.execute("SELECT id, date_iso, seq FROM records WHERE case_id=?", (case_id,))}
app/backend/case_list.py:158:            date = date or (r.get("date_iso") if kind == "entry" else None)
app/backend/conflicts.py:101:    return [o for o in records if o.get("date_iso") and o["date_iso"] < s["iso"] and _describes_event(o, s["iso"])]
app/backend/conflicts.py:106:    return [r for r in records if r.get("date_iso")]
app/backend/conflicts.py:138:    first = min(r["date_iso"] for r in enc)
app/backend/conflicts.py:145:            first = min(r["date_iso"] for r in _event_records(later[0], enc))      # compare with the earliest record that describes it
app/backend/conflicts.py:146:    first_recs = [r for r in enc if r["date_iso"] == first]
app/backend/conflicts.py:164:            visits = sorted((r for r in enc if not gaps.admin_label(r)), key=lambda r: (r["date_iso"], r["n"]))
app/backend/conflicts.py:167:                extra.update(alt_record_no=visits[0]["n"], alt_date=visits[0]["date_iso"], alt_provider=visits[0].get("source") or "the record",
app/backend/conflicts.py:168:                             alt_later="also" if a["iso"] > visits[0]["date_iso"] else "not")
app/backend/conflicts.py:188:    before = sorted((r for r in enc if r["date_iso"] < iso), key=lambda r: r["n"])
app/backend/export.py:7:    records: [{n, source, date_iso|None, excerpt, [could_not_process|status|reason]}]
app/backend/export.py:8:    entries: [{id, record_no, summary, excerpt, review_status, [translation_label], [date_iso], [original_summary], [original_excerpt]}]
app/backend/export.py:179:        return item.get("date_iso") or (self.records.get(item["record_no"]) or {}).get("date_iso")
app/backend/export.py:208:        return (self.records.get(n) or {}).get("date_iso")
app/backend/export.py:213:        the letter (SCOPE_CUTS row 28); the paralegal fills the blank from the quote. One string, the same one the case view carries (`store.charge_service_date`)."""
app/backend/export.py:215:        return f"{self.source(n)}, {service_date.not_stated_text(self.rec_date(n), service_date.record_kind(self.source(n), self.text(n)))}"
app/backend/export.py:405:            known = [r["date_iso"] for r in v.records.values() if r.get("date_iso")]
app/backend/export.py:490:    for r in sorted(v.records.values(), key=lambda r: (r.get("date_iso") or "", r["n"])):
app/backend/export.py:506:    return amounts.not_totaled_reason(a.get("excerpt"), a.get("raw"), a.get("cents"), rec.get("source"), rec.get("date_iso"), a.get("pos"), list(v.records.values()))
app/backend/export.py:561:    for r in sorted(v.records.values(), key=lambda r: (r.get("date_iso") or "9999", r["n"])):
app/backend/export.py:628:    for r in sorted(v.records.values(), key=lambda r: (r.get("date_iso") or "9999", r["n"])):
app/backend/conflict_candidates.py:108:    year = (denial_rec.get("date_iso") or "")[:4]
app/backend/conflict_candidates.py:127:    da, db = a.get("date_iso"), b.get("date_iso")
app/backend/conflict_candidates.py:168:    order = lambda p: (p["kind"] == "count", (by_n[p["record_no"]].get("date_iso") or "", p["record_no"]))
app/backend/conflict_candidates.py:176:    for r in sorted(records, key=lambda r: (r.get("date_iso") or "", r["n"])):
app/backend/conflict_candidates.py:212:            priors.sort(key=lambda p: (p[0].get("date_iso") or "", p[0]["n"]))
app/backend/conflict_candidates.py:273:    dated = sum(1 for r in records if r.get("date_iso")) if records is not None else None
app/backend/gaps.py:96:        if r.get("date_iso"):
app/backend/gaps.py:97:            by_date.setdefault(r["date_iso"], []).append(r["n"])
app/backend/gaps.py:111:        if r.get("kind") == "unsplit_text" or r.get("date_iso"):
app/backend/gaps.py:125:    return sorted({r["date_iso"] for r in records if r.get("date_iso") and not admin_label(r)})
app/backend/gaps.py:135:    dropped = sorted((r for r in records if r.get("date_iso") and admin_label(r) and (lo is None or r["date_iso"] > lo) and (hi is None or r["date_iso"] < hi)),
app/backend/gaps.py:136:                     key=lambda r: (r["date_iso"], r["n"]))
app/backend/gaps.py:177:        inside = sorted((r for r in records if r.get("date_iso") and lo < r["date_iso"] < hi), key=lambda r: (r["date_iso"], r["n"]))
app/backend/gaps.py:180:        a = max(r["n"] for r in records if r.get("date_iso") == lo and not admin_label(r))
app/backend/gaps.py:181:        b = min(r["n"] for r in records if r.get("date_iso") == hi and not admin_label(r))
app/backend/gaps.py:182:        cuts = sorted({lo, hi} | {r["date_iso"] for r in inside})
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:38.087Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && sed -n '170,260p' app/backend/export.py",
 "description": "Read export.py charge-line text construction around the blank"
}
````

### User / tool · 2026-11-03T15:00:38.164Z

**tool result**
````
    def in_charges(self):
        """D-073 fallback: in the order of the record dates (the letter prints no service date)."""
        got = [a for a in self.amounts if a["cls"] == "charge" and a.get("cents") is not None and _status(a) == "in" and self.verbatim(a)]
        return sorted(got, key=lambda a: (self._date(a), a["record_no"], str(a.get("id"))))

    def _date(self, item):
        return self.date_of(item) or "9999-12-31"

    def date_of(self, item):
        return item.get("date_iso") or (self.records.get(item["record_no"]) or {}).get("date_iso")

    def source_prefix(self, n):
        """Citation prefix: 'Source [Ex. __ / Bates __]: ', or '..., p. N: ' when the record came from a PDF (D-031)."""
        pg = (self.records.get(n) or {}).get("page")
        head = SOURCE_PREFIX[:-2] if self.export_config is None else self._bracket(n)
        return head + (": " if pg is None else f", p. {pg}: ")

    def oneline_bracket(self, n):
        """'[Ex. 7 / Bates RIV-0001]' for the one-line style; a PDF page goes inside the bracket: '[Ex. __ / Bates __, p. 3]'."""
        pg = (self.records.get(n) or {}).get("page")
        head = SOURCE_PREFIX[len("Source "):-2] if self.export_config is None else self._bracket(n)[len("Source "):]
        return head if pg is None else head[:-1] + f", p. {pg}]"

    def _bracket(self, n):
        """'Source [Ex. 7 / Bates RIV-0001]' from the per-case export config; unset parts stay '__'. Bates = first number + record number - 1, 4 digits."""
        c = self.export_config
        ex = c.get("exhibit") or "__"
        prefix, start = c.get("bates_prefix"), c.get("bates_start")
        bates = "__" if prefix is None and start is None else f"{prefix or ''}{(1 if start is None else start) + n - 1:04d}"
        return f"Source [Ex. {ex} / Bates {bates}]"

    def source(self, n):
        return (self.records.get(n) or {}).get("source", "")

    def text(self, n):
        return (self.records.get(n) or {}).get("excerpt", "")

    def rec_date(self, n):
        return (self.records.get(n) or {}).get("date_iso")

    def charge_when(self, a):
        """D-073 fallback (T-202 round 6): the label before a charge's amount is ALWAYS the fillable blank, like the Bates placeholder, never a date: 'Fennimoor Spine Clinic, itemized ledger,
        date of service [__________] (statement dated June 15, 2026)' (a bill's own date is its statement date, any other record's its record date). The code extracts no service date for
        the letter (SCOPE_CUTS row 28); the paralegal fills the blank from the quote. One string, the same one the case view carries (`store.charge_service_date`)."""
        n = a["record_no"]
        return f"{self.source(n)}, {service_date.not_stated_text(self.rec_date(n), service_date.record_kind(self.source(n), self.text(n)))}"

    def cite(self, n):
        return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"

    def cite_dated(self, n):
        return f"record {n} ({self.source(n)}, dated {_long_date(self.rec_date(n))})"

    def quote(self, n, ev, whole_sentence=False):
        """Quote evidence from record n. A directly following full stop is included when the evidence starts a
        sentence; whole_sentence expands mid-sentence evidence to its sentence. Always a substring of the record."""
        text = self.text(n)
        i = text.find(ev) if ev else -1
        if i < 0:
            return ev
        j = i + len(ev)
        if whole_sentence:
            hit = [(s, e) for s, e in _sentence_spans(text) if s <= i and j <= e]
            if hit:
                return text[hit[0][0]:hit[0][1]]
        starts_sentence = i == 0 or text[:i].rstrip(" ").endswith((".", "\n"))
        if starts_sentence and text[j:j + 1] == "." and not ev.endswith("."):
            return ev + "."
        return ev


def _foreign_money(text, pos, raw):
    """The money expressions of `text` that are not the charge's own figure (`raw` at offset `pos`; with no offset, a hit that contains `raw`). The one detector."""
    out = []
    for a, b, h, _ in money.hits(text):
        own = (a < pos + len(raw) and pos < b) if pos is not None else raw in h
        if own and not re.search(r"\d", h.replace(raw, "", 1)):
            continue
        out.append(h)
    return out


def _clauses(sentence):
    """Candidate clauses of a sentence, widest first: the pieces between ; and , (a comma inside a number is not a break), then each piece cut before a parenthesis."""
    spans = [(m.start(), m.end()) for m in re.finditer(r"(?:[^;,]|,(?=\d))+(?:[;,]|$)", sentence)]
    out = list(spans)
    for lo, hi in spans:
        k = sentence.find(" (", lo, hi)
        if k > lo:
            out.append((lo, k))
    return out
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:41.456Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && sed -n '1,140p' evals/letter_check.py",
 "description": "Read evals/letter_check.py first half at HEAD"
}
````

### User / tool · 2026-11-03T15:00:41.532Z

**tool result**
````
"""Letter-level eval (T-139; D-019, R-CH-7, R-EX-8): no dollar amount reaches the carrier letter except in the BILLED CHARGES section.

For every golden case, the sample and every library packet, on the FIXTURE backend (recorded model answers; no network):
  run the pipeline on a scratch database, accept every item that code lets her accept (a refusal is counted, not hidden), export the letter in both styles;
  then a variant where every charge is dismissed.
Violations (all must be zero):
  - a currency string in the letter outside the BILLED CHARGES section (the treatment entries and the TREATMENT SUMMARY paragraph);
  - in the BILLED CHARGES section, a currency string that is not an accepted charge or the total line (R-EX-8: exactly 'Billed charges accepted from these records: $X');
  - after dismissing every charge: any currency string anywhere in the letter, or a provider whose charge was dismissed under BILLS TO REQUEST in the notes.
  - money written WITHOUT a '$' anywhere outside the accepted charge lines ('TOTAL CHARGE 49100', 'AMOUNT PAID 0 00', '24F 25500'): T-139 round 2.
T-139 round 4: the audit uses the SAME detector as the charge-text hold and the export gate (app/backend/money.py), so the three cannot diverge: a wording one holds, all hold.
The eval's independent value is the walk (every case, every style, charges dismissed) and the structure checks (charges section, total line, bills to request), not a
second regex. It also reports the export gate: a case whose letter the gate blocks is a violation.
D-071 / D-073 / T-202: a third variant counts every countable amount (the paralegal's D-064 "Count this charge", with the named confirms) after accepting everything, and every charge
line of every letter is checked (`charge_date_violations`, D-073 FALLBACK after round 6): the letter extracts no service date, so EVERY charge line must print the fillable blank in its exact
form, 'date of service [__________] (statement dated X)' on a bill or '(record dated X)' on any other record, X the record's own date. A printed date, period or any other form is a violation.
Pure check: `violations(letter, accepted_cents)`; the pipeline walk is `letters_for(text)`.

    python -m evals.letter_check            prints one line per case and exits 1 on any violation
"""
import contextlib
import json
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD, LIB = ROOT / "evals" / "golden", ROOT / "evals" / "library"
CHARGES, TOTAL = "BILLED CHARGES", "Billed charges accepted from these records: "
STYLES = (None, "oneline")

def dollar_figures(text: str) -> list:
    """Every '$'-marked figure (also 'N dollars', 'USD N') in `text`, in order of position (the shared detector, app/backend/money.py)."""
    from app.backend import money
    return money.of_kind(text, "dollar")


def other_currency(text: str) -> list:
    """Figures with another currency sign or code, amounts in words, and money in a patient's statement (the shared detector)."""
    from app.backend import money
    return money.of_kind(text, "sign", "spoken", "statement")


def unmarked_money(text: str) -> list:
    """Money written without a sign (a money word or claim-form field and its figure), outside any signed figure (the shared detector)."""
    from app.backend import money
    return money.of_kind(text, "unmarked")


def cases():
    """[(name, text)]: the sample, the golden cases and the library packets, in a fixed order."""
    names = [GOLD / "sample.txt"] + sorted(GOLD.glob("case_*.txt")) + sorted(LIB.glob("case_*.txt"))
    return [(p.stem, p.read_text()) for p in names]


def violations(letter: str, accepted_cents=(), expect_none: bool = False) -> list:
    """Currency strings the letter may not carry. `accepted_cents`: the accepted charges (the only amounts the BILLED CHARGES section may list).
    `expect_none`: nothing was accepted as a charge, so no currency string may appear anywhere."""
    from app.backend import amounts as AM, export
    out = []
    head_lines, tail_lines = export.split_letter(letter)               # by structure (the last BILLED CHARGES header line before the total line), never on the words in a quote
    head, tail = "\n".join(head_lines), "\n".join(tail_lines)
    out += [f"treatment text states {s}" for s in dollar_figures(head)]
    out += [f"treatment text states money in another form: {s}" for s in other_currency(head)]
    out += [f"treatment text states money without a $ sign: {s}" for s in unmarked_money(head)]
    if expect_none or not accepted_cents:
        out += [f"letter states {s} with no accepted charge" for s in dollar_figures(tail)]
        out += [f"letter states money without a $ sign: {s}" for s in unmarked_money(tail)]
        out += [f"letter states money in another form: {s}" for s in other_currency(tail)]
        return out
    allowed = {c for c in accepted_cents} | {sum(accepted_cents)}
    for line in tail.splitlines():
        for s in dollar_figures(line):
            cents = AM.to_cents(s.lstrip("$ ").strip())
            if cents is None or cents not in allowed:
                out.append(f"charges section states {s}, not an accepted charge or the total")
        out += [f"charges section states money without a $ sign: {s}" for s in unmarked_money(line)]
        out += [f"charges section states money in another form: {s}" for s in other_currency(line)]
    totals = [l for l in tail.splitlines() if l.startswith(TOTAL)]
    if len(totals) != 1 or not re.fullmatch(re.escape(TOTAL) + r"\$[\d,]+\.\d\d", totals[0]):
        out.append(f"total line is not exactly the template: {totals}")
    return out


# T-208 (T-201 review, D-065 / D-069): the carrier letter never names an AI or a model, whatever the case's provenance (prepared or live). One independent pattern, its own scan.
AI_WORDING = re.compile(r"\bAI\b|claude|sonnet|haiku|opus|\bmodel\b", re.I)
# The ONE allowed form (D-042 / D-050, T-121): the bracketed, removable translation label on an entry from a Spanish record whose English summary a model wrote. It is a safety label (check the
# original before sending), not provenance wording, and it is the only place the letter says 'AI'. Matched whole and verbatim (the string is copied here on purpose, not imported from the export).
# T-208 r2: the label is exempt ONLY where it belongs: the case must have a translated (non-English) source entry, and the label must sit directly with that entry's quote (standard style: alone on
# the line right under the quote line; one-line style: after the quote, on the same line). Anywhere else, in an English letter or away from the quote, it fails like any other 'AI'.
# If the product decides the letter must not say it at all, delete this one tuple entry.
ALLOWED_AI_LABELS = ("[AI translation of the Spanish original; check before sending]",)


def _oneline(s):
    return " ".join(str(s).split())


def _label_with_quote(letter: str, i: int, label: str, translated_quotes) -> bool:
    """True when the label starting at index i sits directly with the quote of a translated entry (see the comment on ALLOWED_AI_LABELS)."""
    before = letter[:i]
    line_start = before.rfind("\n") + 1
    after = letter[i + len(label):i + len(label) + 1]
    for q in translated_quotes:
        if not q:
            continue
        if line_start == i:      # standard style: the label is alone on its line, right under the quote line
            if after in ("", "\n") and before.endswith(f'"{q}"\n'):
                return True
        elif after in ("", "\n") and f'"{_oneline(q)}"' in before[line_start:]:      # one-line style: the quote is on this line, before the label
            return True
    return False


def ai_wording(letter: str, translated_quotes=()) -> list:
    """Every AI or model word in the letter ('AI', 'Claude', 'Sonnet', 'Haiku', 'Opus', 'model'), each with its line, so the audit shows where. The allowed translation label is not scanned when
    it sits directly with the quote of a translated entry (translated_quotes = that case's translated entries' quotes); with no translated quote given, nothing is exempt."""
    chars = list(letter)
    for ok in ALLOWED_AI_LABELS:
        for m in re.finditer(re.escape(ok), letter):
            if _label_with_quote(letter, m.start(), ok, translated_quotes):
                chars[m.start():m.end()] = [" "] * (m.end() - m.start())      # blank only the allowed occurrences (same length, so every other index stays valid)
    out = []
    for line, orig in zip("".join(chars).splitlines(), letter.splitlines()):
        out += [f"letter names AI or a model: {m.group(0)!r} in {orig.strip()[:80]!r}" for m in AI_WORDING.finditer(line)]
    return out


def _walk(conn, cid, dismiss_charges=False):
    """Accept (or dismiss) every item through the review code path. Returns (accepted charge cents, refused [(id, code)])."""
    from app.backend import review
    from app.db import db as DB
    refused, cents = [], []
    for kind in ("entry", "amount", "flag"):
        for it in DB.list_items(conn, cid, kind):
            if it["state"] == "rejected":
                continue
            dismiss = dismiss_charges and kind == "amount" and it["kind"] == "charge"
            try:
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:43.059Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && sed -n '140,314p' evals/letter_check.py",
 "description": "Read evals/letter_check.py second half at HEAD"
}
````

### User / tool · 2026-11-03T15:00:43.155Z

**tool result**
````
            try:
                review.apply_review(conn, cid, it["id"], {"action": "dismiss" if dismiss else "accept"})
            except review.ReviewError as e:
                refused.append((it["id"], e.code if e.code != "CODE_CHECK_FAILED" else (e.detail or {}).get("reason_code", e.code)))
                continue
            if kind == "amount" and it["kind"] == "charge" and not dismiss and it.get("value_cents") is not None:
                cents.append(it["value_cents"])
    return cents, refused


def _count_all(conn, cid):
    """D-064 count path: count every amount the code held back for a missing detail, naming the confirm (and the duplicate / total flag when the code asks for it); an uncountable one is
    skipped. Returns the cents of every accepted charge after that."""
    from app.backend import count_charge, review
    from app.db import db as DB
    for it in DB.list_items(conn, cid, "amount"):
        if it["state"] == "rejected" or it["kind"] == "charge":
            continue
        body = {"confirm": count_charge.CONFIRM}
        for _ in range(2):
            try:
                count_charge.count(conn, cid, it["id"], dict(body))
                break
            except review.ReviewError as e:
                want = (e.detail or {}).get("confirm_with")
                if e.code == "CONFIRM_REQUIRED" and want and want != count_charge.CONFIRM and "confirm_flag" not in body:
                    body["confirm_flag"] = want
                    continue
                break
    return [it["value_cents"] for it in DB.list_items(conn, cid, "amount")
            if it["kind"] == "charge" and it["review_status"] in ("accepted", "edited") and it.get("value_cents") is not None and it["state"] != "rejected"]


BLANK = "date of service [__________]"          # D-073 fallback: the ONLY printed form of a charge line's date


def charge_lines(letter: str) -> list:
    """[(header, quote)] of the BILLED CHARGES section, by structure (a header ends ': $X.XX'; the next line is its Source line)."""
    from app.backend import export
    _, tail = export.split_letter(letter)
    out = []
    for i, line in enumerate(tail):
        if re.search(r": \$[\d,]+\.\d\d$", line) and not line.startswith(TOTAL) and i + 1 < len(tail):
            q = tail[i + 1]
            out.append((line, q[q.index('"') + 1:q.rindex('"')] if '"' in q else q))
    return out


TYPES_PATH = ROOT / "app" / "backend" / "encounter_types.json"          # D-071 amendment 2: the ONE declared table of record types (production reads the same file)
_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))


def _words(text):
    return re.findall(r"[^\W_]+", (text or "").lower())


def _has_term(text_words, term):
    t = _words(term)
    return any(text_words[i:i + len(t)] == t for i in range(len(text_words) - len(t) + 1))


def _record_kind(source, excerpt=""):
    """'bill' | 'encounter' | 'other', read from the declared table with this file's own matcher: financial words in the source label or the opening of the excerpt (its first characters up to the first colon or full stop) make a bill,
    administrative words make 'other', and a record is an ENCOUNTER only when its source label names one (a visit, ER, clinic, therapy, imaging, ambulance-run note ...). Only an encounter
    lends the line its own date."""
    src_w, open_w = _words(source), _words(re.split(r"[:.\n]", (excerpt or "")[:int(_TYPES["opening_chars"])])[0])
    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["financial"]):
        return "bill"
    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["administrative"]):
        return "other"
    return "encounter" if any(_has_term(src_w, t) for t in _TYPES["encounter"]) else "other"


def charge_date_violations(letter: str, records) -> list:
    """D-073 FALLBACK (T-202 round 6): every charge line prints the fillable blank and nothing else for its date of service, in its exact form, anchored at both ends:
    '<source label>, date of service [__________] (statement dated June 15, 2026)' when the record is a bill, '(record dated June 15, 2026)' for any other record, and no parenthesis when the
    record has no date. A printed service date, a period, a blank in any other form, or a statement date that is not the record's own is a violation. `records`: the case's
    [{n, source, date_iso, excerpt}]; a line's record is the one whose excerpt holds the line's quote. The kind (bill or not) is read from the declared table with this file's own matcher."""
    from datetime import date
    norm = lambda t: " ".join(str(t).split())
    out = []
    for head, quote in charge_lines(letter):
        recs = [r for r in records if norm(quote) and norm(quote) in norm(r["excerpt"])]
        if not recs:
            out.append(f"charge line's quote is in no record: {head}")
            continue
        got = norm(re.sub(r": \$[\d,]+\.\d\d$", "", head))
        wants = []
        for r in recs:
            rd = r.get("date_iso")
            d = date.fromisoformat(rd) if rd else None
            wants.append(f"{norm(r.get('source') or '')}, {BLANK}" + (f" ({'statement' if _record_kind(r.get('source'), r['excerpt']) == 'bill' else 'record'} dated {d.strftime('%B')} {d.day}, {d.year})" if d else ""))
        if got not in wants:
            out.append(f"charge line does not print the blank date of service in its exact form (source label, then '{BLANK}', then the record's date called 'statement' on a bill and 'record' otherwise): {head}")
    return out


def letters_for(text: str, backend: str = "fixture") -> dict:
    """{'all_accepted': {...}, 'charges_dismissed': {...}}, each {'letters': {style: text}, 'notes': str, 'charge_cents': [...], 'refused': [(id, code)], 'gate': {style: [why...]}}."""
    from app.backend import export, ingest as IN, pipeline as PL, store
    from app.llm import provider as P
    out = {}
    for variant, dismiss in (("all_accepted", False), ("charges_dismissed", True), ("counted", False)):
        with PL._Backend(backend), tempfile.TemporaryDirectory() as tmp:
            conn, cid, call = PL._scratch_call(tmp, IN.normalize_text(text))
            with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
                PL.run_pipeline(conn, cid, text, call=call)
            cents, refused = _walk(conn, cid, dismiss)
            if variant == "counted":
                cents = _count_all(conn, cid)
            case = store.export_case(conn, cid)
            case["judge_not_run"] = []          # this check reads the letter text only; the second-check gate is a separate rule (D-044)
            built, gate = {}, {}
            for st in STYLES:
                key = st or "standard"
                try:
                    built[key] = export.build_export(case, st)
                except export.ExportBlocked as e:                  # T-139 r4: the export gate itself; a blocked letter is a violation, and the text is still audited below
                    gate[key] = [i["why"] for i in e.items]
                    built[key] = export.build_export(case, st, check_letter=False)
            src = {r["n"]: r["source"] for r in case["records"]}
            dismissed = sorted({src[a["record_no"]].split(",", 1)[0].strip() for a in case["amounts"] if a["cls"] == "charge" and a["review_status"] == "dismissed"})
            conn.close()
        out[variant] = {"letters": {k: v["letter_text"] for k, v in built.items()}, "notes": built["standard"]["internal_notes_text"],
                        "charge_cents": cents, "refused": refused, "records": case["records"], "dismissed_providers": dismissed, "gate": gate,
                        "prepared": bool(case.get("prepared")),
                        "translated_quotes": [e["excerpt"] for e in case["entries"] if e.get("translation_label") == "AI translation"]}      # T-208: the case kind, so a report can say how many prepared and live letters were scanned
    return out


def dismissed_in_bills(notes: str, providers) -> list:
    """Providers whose charge was dismissed that the notes still list under BILLS TO REQUEST."""
    sec = notes.split("BILLS TO REQUEST")[1].split("RECORDS NOT IN THE TREATMENT SECTION")[0] if "BILLS TO REQUEST" in notes else ""
    listed = [re.sub(r"\s*\(itemized ledger\)$", "", x.strip().rstrip(".")) for x in sec.split("\n", 2)[-1].lstrip("- ").split(";")]
    return [p for p in providers if p in listed]


def measure(case_list=None, backend: str = "fixture") -> dict:
    """The report block: {'value': total violations (0 = pass), 'cases': n, 'per_case': {...}, 'held_out_entries': n, 'r_ids': [...]}."""
    per_case, held = {}, 0
    for name, text in (case_list if case_list is not None else cases()):
        got = letters_for(text, backend)
        bad = []
        for style, letter in got["all_accepted"]["letters"].items():
            bad += [f"{style}: {v}" for v in violations(letter, got["all_accepted"]["charge_cents"])]
        for style, letter in got["charges_dismissed"]["letters"].items():
            bad += [f"{style} (charges dismissed): {v}" for v in violations(letter, (), expect_none=True)]
        for style, letter in got["counted"]["letters"].items():
            bad += [f"{style} (counted): {v}" for v in violations(letter, got["counted"]["charge_cents"])]
        for variant in ("all_accepted", "charges_dismissed", "counted"):      # T-208: no AI or model wording in any letter, of any kind of case
            for style, letter in got[variant]["letters"].items():
                bad += [f"{style} ({variant}): {v}" for v in ai_wording(letter, got[variant].get("translated_quotes", ()))]
        for variant in ("all_accepted", "counted"):
            for style, letter in got[variant]["letters"].items():
                bad += [f"{style} ({variant}): {v}" for v in charge_date_violations(letter, got[variant]["records"])]
        for variant in ("all_accepted", "charges_dismissed", "counted"):
            bad += [f"{style} ({variant}): the export gate blocked this letter: {w}" for style, whys in got[variant]["gate"].items() for w in whys]
        bad += [f"dismissed charge's provider {p} is under BILLS TO REQUEST" for p in dismissed_in_bills(got["charges_dismissed"]["notes"], got["charges_dismissed"]["dismissed_providers"])]
        held += sum(1 for _, code in got["all_accepted"]["refused"] if code == "CHARGE_TEXT_IN_ENTRY")
        if bad:
            per_case[name] = sorted(set(bad))
    return {"value": sum(len(v) for v in per_case.values()), "cases": len(case_list if case_list is not None else cases()), "per_case": per_case,
            "held_out_entries": held, "backend": backend, "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}


def main(argv=None) -> int:
    m = measure()
    print(json.dumps({k: v for k, v in m.items() if k != "per_case"}))
    for name, v in m["per_case"].items():
        print(f"  {name}: {v}")
    return 0 if m["value"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:00:54.753Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-202-paralegal-r6/ | head -80 && sed -n '1,60p' artifacts/review-evidence/T-202-paralegal-r6/fullpipe_r6.py",
 "description": "List round-6 evidence and read the full-pipeline probe script"
}
````

### User / tool · 2026-11-03T15:00:54.845Z

**tool result**
````
case_09-s3-00-a1.png
case_09-step2-done.png
case_09-step3-done.png
case_09-step4.png
corpus_blanks.diff
corpus_blanks.py
corpus_blanks_9655f1d.out
corpus_blanks_f9c0faf.out
db
draft-T-202-paralegal-r6.md
eval_teeth_r5.py
eval_teeth_r6.out
eval_teeth_r6.py
fullpipe_lib10.out
fullpipe_lib10.py
fullpipe_r5.py
fullpipe_r6.out
fullpipe_r6.py
fullpipe_r6_a15_u1.out
h.py
letter_check.out
letters_dump_r5.py
lib10-s3-00-a2.png
lib10-s3-01-a3.png
lib10-s3-02-a4.png
lib10-s3-03-a5.png
lib10-s3-04-a1.png
lib10-s3-05-a6.png
lib10-s3-06-a7.png
lib10-s3-07-a8.png
lib10-s3-08-a9.png
lib10-s3-09-a10.png
lib10-s3-10-a11.png
lib10-step2-done.png
lib10-step3-done.png
lib10-step4.png
lib11-s3-00-a1.png
lib11-s3-01-a2.png
lib11-s3-02-a3.png
lib11-s3-03-a4.png
lib11-s3-04-a5.png
lib11-s3-05-a6.png
lib11-s3-06-a7.png
lib11-s3-07-a8.png
lib11-step2-done.png
lib11-step3-done.png
lib11-step4.png
lib14-s3-00-a1.png
lib14-s3-01-a2.png
lib14-s3-02-a4.png
lib14-s3-03-a3.png
lib14-s3-04-a5.png
lib14-step2-done.png
lib14-step3-done.png
lib14-step4.png
p01.out
p01_cases.py
probe_r5.py
probe_r6.out
probe_r6.py
profile
pytest-t202.out
run.log
sample-s3-00-a1.png
sample-s3-01-a4.png
sample-s3-02-a2.png
sample-s3-03-a3.png
sample-step2-done.png
sample-step3-done.png
sample-step4.png
server.log
ui-case_09-letter-onscreen.txt
ui-case_09-letter.txt
ui-case_09-notes.txt
ui-lib10-letter-onscreen.txt
ui-lib10-letter.txt
ui-lib10-notes.txt
ui-lib11-letter-onscreen.txt
ui-lib11-letter.txt
ui-lib11-notes.txt
"""T-202 r6 paralegal: round 6 shapes through the FULL case pipeline and the letter (evals.letter_check.letters_for: fixture backend, every item accepted;
'counted' counts what the paralegal may count), on SYNTHETIC variants of the Appendix A sample: a record 10 is appended (the sample's own 9 records stay),
or record 6 / record 8 / case_09 record 2 is replaced. Prints every BILLED CHARGES line, letter_check.charge_date_violations, and the notes line for the probe figure.
Also re-runs the r5 provider-name, key-value-over-row and table shapes.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r6/fullpipe_r6.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
os.environ.setdefault("LLM_BACKEND", "fixture")
os.environ.setdefault("FIXTURE_SET", "curated")
import logging  # noqa: E402
logging.disable(logging.CRITICAL)
from evals import letter_check as LC  # noqa: E402

SAMPLE = open("evals/golden/sample.txt").read()
C09 = open("evals/golden/case_09_nonvisit_hides_gap.txt").read()
C09_R2 = 'Date: 2026-03-01\nSource: Hobbleton Family Clinic, billing statement\nExcerpt: "Statement for visit of 2026-02-02: $275."'
PT9 = 'Date: 2026-03-06\nSource: Capital PT, visit 9\nExcerpt: "Discharged from PT after two missed appointments. Pain 3/10."'
MRI8 = "correlate clinically. Charge: $2,150."
TAIL = 'Patient states symptoms began after the January collision."'


def add(src, ex, date):
    assert TAIL in SAMPLE
    return SAMPLE.replace(TAIL, TAIL + f'\n\n=== Record 10 ===\nDate: {date}\nSource: {src}\nExcerpt: "{ex}"')


def pt9(src, ex):
    assert PT9 in SAMPLE, "PT9"
    return SAMPLE.replace(PT9, f'Date: 2026-03-06\nSource: {src}\nExcerpt: "{ex}"')


def mri_bill(src, ex, date="2026-06-20"):
    s = SAMPLE.replace(MRI8, "correlate clinically.")
    return s.replace(TAIL, TAIL + f'\n\n=== Record 10 ===\nDate: {date}\nSource: {src}\nExcerpt: "{ex}"')


def c09(src, ex, date="2026-03-01"):
    assert C09_R2 in C09
    return C09.replace(C09_R2, f'Date: {date}\nSource: {src}\nExcerpt: "{ex}"')


PTN = "Capital PT, physical therapy note"
OVN = "Dr. Alvarez, office visit note"
D = "Discharged from PT after two missed appointments. Pain 3/10. "
CASES = {
    # round 6: whole-phrase encounter records whose charge is for another time (truth in brackets)
    "a1_pcp_note_er_charge [truth Jan 9]": ("6,240", add(OVN, "Persistent neck pain 6/10. Patient brought the Central ER bill. ER facility charge $6,240.00.", "2026-01-16")),
    "a2_pt_note_initial_eval [truth Jan 23]": ("250", pt9(PTN, D + "Initial evaluation 97161 charge $250.00.")),
    "a3_pt_note_first_visit [truth Jan 23]": ("250", pt9(PTN, D + "First visit charge $250.00.")),
    "a4_addendum_01_20 [truth Jan 16]": ("150", add("Dr. Alvarez, progress note addendum", "Addendum to the visit note. Office visit 99213 charge corrected to $150.00.", "2026-01-20")),
    "a5_late_entry_01_20 [truth Jan 16]": ("150", add(OVN, "Late entry for the visit of 01/16/2026. Office visit 99213 charge $150.00.", "2026-01-20")),
    "a6_inpatient_discharge_summary [truth Jun 9-12]": ("4,920", add("Saltmarrow General Hospital, discharge summary", "Admitted 06/09/2026 for observation after the collision. Discharged home in stable condition. Total hospital charges $4,920.00.", "2026-06-12")),
    "a6b_er_overnight_discharge_summary [truth Jan 9-10]": ("6,240", SAMPLE.replace('Date: 2026-01-09\nSource: Central ER discharge summary', 'Date: 2026-01-10\nSource: Central ER discharge summary', 1).replace("Follow up with PCP in 1 week.", "Arrived 01/09/2026 by EMS. Discharged 01/10/2026. Follow up with PCP in 1 week.")),
    "a7_pt_note_course_charges [truth Jan 23-Mar 6]": ("1,665", pt9(PTN, D + "Physical therapy charges: $1,665.")),
    "a10_pcp_note_yesterday_uc [truth Jan 15]": ("310", add(OVN, "Patient went to urgent care yesterday, urgent care visit charge $310.00.", "2026-01-16")),
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:01:01.717Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && ls evals/golden evals/library | head -80 && grep -rn \"route\\|@app\\.\\(get\\|post\\)\\|add_route\\|\\\"/api/\" app/backend/*.py | grep -i \"api/\" | head -30",
 "description": "List golden and library case files and API routes"
}
````

### User / tool · 2026-11-03T15:01:01.810Z

**tool result**
````
evals/golden:
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
case_09_nonvisit_hides_gap.expected.json
case_09_nonvisit_hides_gap.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
judge_controls.CHANGELOG.md
judge_controls.jsonl
judge_controls_heldout.jsonl
sample.expected.json
sample.export.expected.txt
sample.txt
unsplit_paste.split.json
unsplit_paste.txt

evals/library:
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
case_lib06_lop_billed_vs_adjusted.expected.json
case_lib06_lop_billed_vs_adjusted.txt
case_lib07_parking_lot_fall_outside_records.expected.json
case_lib07_parking_lot_fall_outside_records.txt
case_lib08_second_crash_mri_after.expected.json
case_lib08_second_crash_mri_after.txt
case_lib09_spanish_interpreter_espalda.expected.json
case_lib09_spanish_interpreter_espalda.txt
case_lib10_eob_ub04_cms1500.expected.json
case_lib10_eob_ub04_cms1500.txt
case_lib11_priors_and_ledger.expected.json
case_lib11_priors_and_ledger.txt
case_lib12_records_review_credibility.expected.json
case_lib12_records_review_credibility.txt
case_lib13_cloned_notes_cross_provider.expected.json
case_lib13_cloned_notes_cross_provider.txt
case_lib14_handwritten_chiro_scans.expected.json
case_lib14_handwritten_chiro_scans.txt
case_lib15_conclusory_letter_mist.expected.json
case_lib15_conclusory_letter_mist.txt
app/backend/calibration_route.py:201:    @app.get("/api/calibration")
app/backend/api.py:263:    @app.get("/api/health")
app/backend/api.py:270:    @app.get("/api/cases")
app/backend/api.py:280:    @app.get("/api/library")
app/backend/api.py:286:    @app.post("/api/cases", status_code=201)
app/backend/api.py:304:    @app.post("/api/cases/pdf", status_code=201)
app/backend/api.py:385:    @app.get("/api/cases/{token}")
app/backend/api.py:395:    @app.patch("/api/cases/{token}")
app/backend/api.py:411:    @app.delete("/api/cases/{token}", status_code=204)
app/backend/api.py:436:    @app.post("/api/cases/{token}/run", status_code=202)
app/backend/api.py:462:    @app.post("/api/cases/{token}/rejudge")
app/backend/api.py:484:    @app.get("/api/cases/{token}/status")
app/backend/api.py:502:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
app/backend/api.py:514:    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
app/backend/api.py:525:    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
app/backend/api.py:538:    @app.get("/api/cases/{token}/narrative")
app/backend/api.py:547:    @app.post("/api/cases/{token}/narrative")
app/backend/api.py:560:    @app.post("/api/cases/{token}/narrative/review")
app/backend/api.py:575:    @app.get("/api/cases/{token}/items/{item_id}")
app/backend/api.py:587:    @app.post("/api/cases/{token}/items/{item_id}/review")
app/backend/api.py:608:    @app.get("/api/cases/{token}/export")
app/backend/api.py:638:    @app.get("/api/cases/{token}/items/{item_id}/trace")
app/backend/api.py:651:    @app.get("/api/cases/{token}/trace")
app/backend/api.py:660:    @app.get("/api/cases/{token}/judges")
app/backend/api.py:669:    @app.get("/api/cases/{token}/audit")
app/backend/billing.py:1061:    @app.get("/api/cases/{token}/billing")
app/backend/case_extras.py:123:    @app.post("/api/cases/{token}/review/batch")
app/backend/case_extras.py:146:    @app.get("/api/cases/{token}/export_config")
app/backend/case_extras.py:155:    @app.put("/api/cases/{token}/export_config")
app/backend/case_extras.py:170:    @app.delete("/api/cases/{token}/export_config")
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:01:09.919Z

**tool call — Bash**
````
{
 "command": "head -c 900 evals/golden/case_09_nonvisit_hides_gap.txt; echo; echo ----; grep -n \"^Date:\\|^Source:\" evals/library/case_lib10_eob_ub04_cms1500.txt | head -30; echo ----; grep -n \"^Date:\" evals/library/case_lib11_priors_and_ledger.txt | head; grep -n \"^Date:\\|^Source\" evals/golden/sample.txt | head -30",
 "description": "Inspect the record header format of the four input cases"
}
````

### User / tool · 2026-11-03T15:01:10.026Z

**tool result**
````
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-02-02
Source: Hobbleton Family Clinic, visit
Excerpt: "Left wrist pain 4/10. Splint applied. Return in 2 weeks."

=== Record 2 ===
Date: 2026-03-01
Source: Hobbleton Family Clinic, billing statement
Excerpt: "Statement for visit of 2026-02-02: $275."

=== Record 3 ===
Date: 2026-03-12
Source: Hobbleton Family Clinic, phone note
Excerpt: "Patient called to request a work note. Work note provided."

=== Record 4 ===
Date: 2026-03-30
Source: Hobbleton Family Clinic, visit
Excerpt: "Left wrist pain 3/10. Splint removed."

=== Record 5 ===
Date: 2026-04-13
Source: Hobbleton Family Clinic, visit
Excerpt: "Pain 1/10. Released from care."


----
4:Date: 2026-06-09
5:Source: Rainhollow Fire-Rescue run report
9:Date: 2026-06-09
10:Source: Saltmarrow General Hospital ED
14:Date: 2026-06-12
15:Source: Saltmarrow General Hospital, discharge summary
19:Date: 2026-06-19
20:Source: Saltmarrow General Hospital, UB-04 itemized bill
24:Date: 2026-06-24
25:Source: Dr. Ignatius Wardlaw, orthopedics, new patient
29:Date: 2026-07-03
30:Source: Quoinmere Mutual Health Plan, EOB
34:Date: 2026-07-08
35:Source: Dr. Ignatius Wardlaw, orthopedics, follow-up
39:Date: 2026-07-14
40:Source: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)
44:Date: 2026-08-26
45:Source: Dr. Ignatius Wardlaw, orthopedics, follow-up
----
4:Date: 2026-03-04
9:Date: 2026-03-18
14:Date: 2026-03-18
19:Date: 2026-03-26
24:Date: 2026-03-27
29:Date: 3/27/26
34:Date: 2026-04-24
39:Date: 2026-05-29
44:Date: 2026-06-15
4:Date: 2026-01-09
5:Source: Austin EMS run report
9:Date: 2026-01-09
10:Source: Central ER discharge summary
14:Date: 2026-01-16
15:Source: Dr. Alvarez, primary care
19:Date: 2026-01-23
20:Source: Capital PT, initial evaluation
24:Date: 2026-02-20
25:Source: Capital PT, visit 8
29:Date: 2026-03-06
30:Source: Capital PT, visit 9
34:Date: 2026-05-18
35:Source: Hill Country Pain Management, new patient
39:Date: 2026-05-29
40:Source: Austin Imaging, cervical MRI
44:Date: 2026-06-12
45:Source: Hill Country Pain Management, follow-up
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:01:26.365Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.py",
 "content": "\"\"\"T-202 r7 paralegal check (run from a git archive copy, with -I):\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.py <archive_root>\n\nFor the sample, case_09, lib10 and lib11 inputs: runs the real pipeline and export path (evals.letter_check.letters_for, fixture backend,\nevery item accepted; 'counted' variant too), then checks every BILLED CHARGES line:\n  1. the line is EXACTLY '<source label>, date of service [__________] (statement|record dated <Month D, YYYY>)' (no other date-like text on the line);\n  2. the parenthetical date equals the record's own 'Date:' header in the INPUT text (parsed here from the raw text, not from the app);\n  3. the kind word is 'statement' only for a bill (letter_check's own kind reader), 'record' otherwise;\n  4. the number of charge lines equals the number of accepted charges;\n  5. no other line of the BILLED CHARGES section, and no line anywhere, prints a date-like string outside the quotes, except the total line and the headers.\nThen runs the teeth check: a mutated line with a wrong date of service, or a wrong record date, must be rejected by letter_check.charge_date_violations.\nPrints one JSON summary and a per-line table. Exit 0 if every check holds.\n\"\"\"\nimport json\nimport logging\nimport os\nimport re\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nos.environ.setdefault(\"LLM_BACKEND\", \"fixture\")\nos.environ.setdefault(\"FIXTURE_SET\", \"curated\")\nlogging.disable(logging.CRITICAL)\nfrom evals import letter_check as LC  # noqa: E402\n\nCASES = {\n    \"sample\": \"evals/golden/sample.txt\",\n    \"case_09\": \"evals/golden/case_09_nonvisit_hides_gap.txt\",\n    \"lib10\": \"evals/library/case_lib10_eob_ub04_cms1500.txt\",\n    \"lib11\": \"evals/library/case_lib11_priors_and_ledger.txt\",\n}\nMONTHS = [\"January\", \"February\", \"March\", \"April\", \"May\", \"June\", \"July\", \"August\", \"September\", \"October\", \"November\", \"December\"]\nLINE = re.compile(r\"^(?P<src>.+), date of service \\[__________\\] \\((?P<kind>statement|record) dated (?P<mon>[A-Z][a-z]+) (?P<day>\\d{1,2}), (?P<yr>\\d{4})\\)$\")\n# any date-like text: month names, numeric dates, ISO dates\nANY_DATE = re.compile(r\"\\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\\b|\\b\\d{1,2}/\\d{1,2}(?:/\\d{2,4})?\\b|\\b\\d{4}-\\d{2}-\\d{2}\\b|\\b\\d{1,2}[/.-]\\d{1,2}[/.-]\\d{2,4}\\b\")\n\n\ndef raw_headers(text):\n    \"\"\"{quote_text: (date_iso, source)} from the INPUT text: each record block's Date/Source/Excerpt, parsed by this script.\"\"\"\n    out = []\n    for block in re.split(r\"\\n=== Record \\d+ ===\\n\", text)[1:]:\n        m_date = re.search(r\"^Date:\\s*(\\S+)\", block, re.M)\n        m_src = re.search(r\"^Source:\\s*(.+)$\", block, re.M)\n        m_ex = re.search(r'^Excerpt:\\s*\"(.*)\"\\s*$', block, re.M | re.S)\n        if m_date and m_src and m_ex:\n            out.append({\"date_raw\": m_date.group(1), \"source\": m_src.group(1).strip(), \"excerpt\": m_ex.group(1)})\n    return out\n\n\ndef iso_from_raw(s):\n    \"\"\"'2026-03-27' or '3/27/26' (lib11 record 6 header) -> ISO. Only the two forms in the corpus.\"\"\"\n    m = re.fullmatch(r\"(\\d{4})-(\\d{2})-(\\d{2})\", s)\n    if m:\n        return s\n    m = re.fullmatch(r\"(\\d{1,2})/(\\d{1,2})/(\\d{2})\", s)\n    if m:\n        return f\"20{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}\"\n    raise ValueError(s)\n\n\ndef long_date(iso):\n    y, mo, d = (int(x) for x in iso.split(\"-\"))\n    return f\"{MONTHS[mo - 1]} {d}, {y}\"\n\n\ndef check_case(name, path, text):\n    res = LC.letters_for(text)\n    rows, problems = [], []\n    raws = raw_headers(text)\n    for variant in (\"all_accepted\", \"counted\"):\n        got = res[variant]\n        letter = got[\"letters\"][\"standard\"]\n        head_lines, tail_lines = _split(letter)\n        charge_heads = [l for l in tail_lines if re.search(r\": \\$[\\d,]+\\.\\d\\d$\", l) and not l.startswith(LC.TOTAL)]\n        n_acc = len(got[\"charge_cents\"])\n        if len(charge_heads) != n_acc:\n            problems.append(f\"{name}/{variant}: {len(charge_heads)} charge heads but {n_acc} accepted charges\")\n        for head in charge_heads:\n            # the Source/quote line sits right under the head\n            idx = tail_lines.index(head)\n            quote = tail_lines[idx + 1] if idx + 1 < len(tail_lines) else \"\"\n            body = re.sub(r\": \\$[\\d,]+\\.\\d\\d$\", \"\", head)\n            m = LINE.match(body)\n            ok_form = bool(m)\n            dates_on_line = ANY_DATE.findall(body)\n            # the parenthetical date is the only date on the line\n            if m and dates_on_line != [f\"{m.group('mon')}\"] and len(dates_on_line) != 1:\n                ok_form = False\n            # the record the quote came from, by the raw input text\n            qtext = quote[quote.index('\"') + 1:quote.rindex('\"')] if '\"' in quote else quote\n            hits = [r for r in raws if \" \".join(qtext.split()) in \" \".join(r[\"excerpt\"].split())]\n            rec_ok, kind_ok, src_ok = False, False, False\n            if hits and m:\n                r = hits[0]\n                iso = iso_from_raw(r[\"date_raw\"])\n                rec_ok = long_date(iso) == f\"{m.group('mon')} {m.group('day')}, {m.group('yr')}\"\n                kind = \"bill\" if LC._record_kind(r[\"source\"], r[\"excerpt\"]) == \"bill\" else \"other\"\n                kind_ok = (m.group(\"kind\") == \"statement\") == (kind == \"bill\")\n                src_ok = m.group(\"src\").strip() == r[\"source\"]\n            row = {\"case\": name, \"variant\": variant, \"head\": head, \"quote\": quote, \"form_exact\": ok_form, \"parenthetical_is_input_record_date\": rec_ok,\n                   \"kind_matches_record\": kind_ok, \"source_as_written\": src_ok, \"dates_on_line\": dates_on_line}\n            rows.append(row)\n            if not (ok_form and rec_ok and kind_ok and src_ok and hits):\n                problems.append(f\"{name}/{variant}: bad charge line: {head!r} quote={quote!r} row={row}\")\n        # no date-like text anywhere in the letter outside quotes, except the blank parenthetical and header dates\n        for line in letter.splitlines():\n            stripped = re.sub(r'\"[^\"]*\"', \"\", line)\n            stripped = LINE.sub(\"\", stripped) if False else stripped\n            if ANY_DATE.search(stripped) and not LINE.search(re.sub(r\": \\$[\\d,]+\\.\\d\\d$\", \"\", line)) and not line.startswith(LC.TOTAL):\n                problems.append(f\"{name}/{variant}: date-like text outside a charge line or quote: {line[:160]!r}\")\n        if got[\"gate\"]:\n            problems.append(f\"{name}/{variant}: export gate blocked: {got['gate']}\")\n    viol = {}\n    for variant in (\"all_accepted\", \"counted\"):\n        got = res[variant]\n        viol[variant] = LC.charge_date_violations(got[\"letters\"][\"standard\"], got[\"records\"])\n        if viol[variant]:\n            problems.append(f\"{name}/{variant}: letter_check.charge_date_violations: {viol[variant]}\")\n    return {\"case\": name, \"path\": path, \"charge_lines\": rows, \"violations\": viol, \"problems\": problems,\n            \"accepted_charges\": len(res[\"all_accepted\"][\"charge_cents\"])}\n\n\ndef _split(letter):\n    from app.backend import export\n    h, t = export.split_letter(letter)\n    return h, t\n\n\ndef teeth(name, text):\n    \"\"\"Mutants the check must reject: a wrong date of service in the blank slot, and a wrong record date in the parenthetical.\"\"\"\n    res = LC.letters_for(text)\n    letter = res[\"all_accepted\"][\"letters\"][\"standard\"]\n    records = res[\"all_accepted\"][\"records\"]\n    out = []\n    heads = [l for l in letter.splitlines() if \" [__________] (\" in l]\n    if not heads:\n        return [f\"{name}: no blank charge line to mutate\"]\n    h = heads[0]\n    bad_dos = h.replace(\"date of service [__________]\", \"date of service March 6, 2026\", 1)\n    bad_rec = re.sub(r\" dated [A-Z][a-z]+ \\d{1,2}, \\d{4}\\)\", \" dated January 1, 2030)\", h, count=1)\n    for label, mut in ((\"printed DOS\", bad_dos), (\"wrong record date\", bad_rec)):\n        m_letter = letter.replace(h, mut, 1)\n        v = LC.charge_date_violations(m_letter, records)\n        out.append({\"case\": name, \"mutant\": label, \"line\": mut, \"rejected\": bool(v), \"reasons\": len(v)})\n    return out\n\n\nif __name__ == \"__main__\":\n    summary = {\"archive\": root, \"cases\": [], \"teeth\": []}\n    for name, path in CASES.items():\n        text = open(os.path.join(root, path), encoding=\"utf-8\").read()\n        summary[\"cases\"].append(check_case(name, path, text))\n        summary[\"teeth\"] += teeth(name, text)\n    all_problems = [p for c in summary[\"cases\"] for p in c[\"problems\"]]\n    teeth_ok = all(t.get(\"rejected\") for t in summary[\"teeth\"] if isinstance(t, dict))\n    summary[\"charge_lines_checked\"] = sum(len(c[\"charge_lines\"]) for c in summary[\"cases\"])\n    summary[\"problems\"] = len(all_problems)\n    summary[\"teeth_all_rejected\"] = teeth_ok\n    print(json.dumps({k: v for k, v in summary.items() if k not in (\"cases\", \"teeth\")}))\n    for c in summary[\"cases\"]:\n        for r in c[\"charge_lines\"]:\n            print(f\"{c['case']} {r['variant']}: {r['head']}  | quote: {r['quote']}  | form={r['form_exact']} recdate={r['parenthetical_is_input_record_date']} kind={r['kind_matches_record']} src={r['source_as_written']}\")\n    for t in summary[\"teeth\"]:\n        print(\"TEETH\", json.dumps(t, ensure_ascii=False))\n    for p in all_problems:\n        print(\"PROBLEM\", p[:400])\n    sys.exit(0 if not all_problems and teeth_ok else 1)\n"
}
````

### User / tool · 2026-11-03T15:01:26.458Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:01:29.458Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.py artifacts/review-evidence/T-202-paralegal-r7/archive > artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.out 2>&1; echo EXIT=$?; cut -c1-400 artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.out | head -120",
 "description": "Run the charge-line check on the HEAD archive for four cases"
}
````

### User / tool · 2026-11-03T15:01:34.316Z

**tool result**
````
EXIT=1
{"archive": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive", "charge_lines_checked": 19, "problems": 78, "teeth_all_rejected": true}
sample all_accepted: Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00  | quote: Source [Ex. __ / Bates __]: "ER charges: $6,240."  | form=True recdate=True kind=True src=True
sample all_accepted: Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00  | quote: Source [Ex. __ / Bates __]: "Charge: $2,150."  | form=True recdate=True kind=True src=True
sample counted: Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00  | quote: Source [Ex. __ / Bates __]: "ER charges: $6,240."  | form=True recdate=True kind=True src=True
sample counted: Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00  | quote: Source [Ex. __ / Bates __]: "Charge: $2,150."  | form=True recdate=True kind=True src=True
case_09 all_accepted: Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00  | quote: Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."  | form=True recdate=True kind=True src=True
case_09 counted: Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00  | quote: Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."  | form=True recdate=True kind=True src=True
lib10 all_accepted: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $4,920.00  | quote: Source [Ex. __ / Bates __]: "FL47 total charges $4,920.00."  | form=True recdate=True kind=True src=True
lib10 all_accepted: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $2,105.00  | quote: Source [Ex. __ / Bates __]: "Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."  | form=True recdate=True kind=True src=True
lib10 all_accepted: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $386.50  | quote: Source [Ex. __ / Bates __]: "Rev 0250 pharmacy, 14 units, FL47 total charges $386.50."  | form=True recdate=True kind=True src=True
lib10 all_accepted: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $712.00  | quote: Source [Ex. __ / Bates __]: "Rev 0300 laboratory, 6 units, FL47 total charges $712.00."  | form=True recdate=True kind=True src=True
lib10 counted: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $4,920.00  | quote: Source [Ex. __ / Bates __]: "FL47 total charges $4,920.00."  | form=True recdate=True kind=True src=True
lib10 counted: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $2,105.00  | quote: Source [Ex. __ / Bates __]: "Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."  | form=True recdate=True kind=True src=True
lib10 counted: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $386.50  | quote: Source [Ex. __ / Bates __]: "Rev 0250 pharmacy, 14 units, FL47 total charges $386.50."  | form=True recdate=True kind=True src=True
lib10 counted: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $712.00  | quote: Source [Ex. __ / Bates __]: "Rev 0300 laboratory, 6 units, FL47 total charges $712.00."  | form=True recdate=True kind=True src=True
lib11 all_accepted: Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026): $3,260.00  | quote: Source [Ex. __ / Bates __]: "ED charge: $3,260."  | form=True recdate=True kind=True src=True
lib11 counted: Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026): $3,260.00  | quote: Source [Ex. __ / Bates __]: "ED charge: $3,260."  | form=True recdate=True kind=True src=True
lib11 counted: Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00  | quote: Source [Ex. __ / Bates __]: "New patient exam charge $250.00"  | form=True recdate=True kind=True src=True
lib11 counted: Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $180.00  | quote: Source [Ex. __ / Bates __]: "x-ray charge $180.00"  | form=True recdate=True kind=True src=True
lib11 counted: Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $2,310.00  | quote: Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"  | form=True recdate=True kind=True src=True
TEETH {"case": "sample", "mutant": "printed DOS", "line": "Central ER discharge summary, date of service March 6, 2026 (record dated January 9, 2026): $6,240.00", "rejected": true, "reasons": 1}
TEETH {"case": "sample", "mutant": "wrong record date", "line": "Central ER discharge summary, date of service [__________] (record dated January 1, 2030): $6,240.00", "rejected": true, "reasons": 1}
TEETH {"case": "case_09", "mutant": "printed DOS", "line": "Hobbleton Family Clinic, billing statement, date of service March 6, 2026 (statement dated March 1, 2026): $275.00", "rejected": true, "reasons": 1}
TEETH {"case": "case_09", "mutant": "wrong record date", "line": "Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated January 1, 2030): $275.00", "rejected": true, "reasons": 1}
TEETH {"case": "lib10", "mutant": "printed DOS", "line": "Saltmarrow General Hospital, UB-04 itemized bill, date of service March 6, 2026 (statement dated June 19, 2026): $4,920.00", "rejected": true, "reasons": 1}
TEETH {"case": "lib10", "mutant": "wrong record date", "line": "Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated January 1, 2030): $4,920.00", "rejected": true, "reasons": 1}
TEETH {"case": "lib11", "mutant": "printed DOS", "line": "Wexcombe Memorial ED, date of service March 6, 2026 (record dated March 18, 2026): $3,260.00", "rejected": true, "reasons": 1}
TEETH {"case": "lib11", "mutant": "wrong record date", "line": "Wexcombe Memorial ED, date of service [__________] (record dated January 1, 2030): $3,260.00", "rejected": true, "reasons": 1}
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'January 9, 2026 — Austin EMS run report'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'January 9, 2026 — Central ER discharge summary'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'January 16, 2026 — Dr. Alvarez, primary care'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'January 23, 2026 — Capital PT, initial evaluation'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'February 20, 2026 — Capital PT, visit 8'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'Pain 4/10, improving.'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'March 6, 2026 — Capital PT, visit 9'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'Discharged from physical therapy after two missed appointments; pain 3/10.'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'May 18, 2026 — Hill Country Pain Management, new patient'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'May 29, 2026 — Austin Imaging, cervical MRI'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'June 12, 2026 — Hill Country Pain Management, follow-up'
PROBLEM sample/all_accepted: date-like text outside a charge line or quote: 'Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'January 9, 2026 — Austin EMS run report'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'January 9, 2026 — Central ER discharge summary'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'January 16, 2026 — Dr. Alvarez, primary care'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'January 23, 2026 — Capital PT, initial evaluation'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'February 20, 2026 — Capital PT, visit 8'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'Pain 4/10, improving.'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'March 6, 2026 — Capital PT, visit 9'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'Discharged from physical therapy after two missed appointments; pain 3/10.'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'May 18, 2026 — Hill Country Pain Management, new patient'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'May 29, 2026 — Austin Imaging, cervical MRI'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'June 12, 2026 — Hill Country Pain Management, follow-up'
PROBLEM sample/counted: date-like text outside a charge line or quote: 'Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.'
PROBLEM case_09/all_accepted: date-like text outside a charge line or quote: 'February 2, 2026 — Hobbleton Family Clinic, visit'
PROBLEM case_09/all_accepted: date-like text outside a charge line or quote: 'Left wrist pain 4/10. Splint applied. Return in 2 weeks.'
PROBLEM case_09/all_accepted: date-like text outside a charge line or quote: 'March 12, 2026 — Hobbleton Family Clinic, phone note'
PROBLEM case_09/all_accepted: date-like text outside a charge line or quote: 'March 30, 2026 — Hobbleton Family Clinic, visit'
PROBLEM case_09/all_accepted: date-like text outside a charge line or quote: 'Left wrist pain 3/10. Splint removed.'
PROBLEM case_09/all_accepted: date-like text outside a charge line or quote: 'April 13, 2026 — Hobbleton Family Clinic, visit'
PROBLEM case_09/all_accepted: date-like text outside a charge line or quote: 'Pain 1/10. Released from care.'
PROBLEM case_09/counted: date-like text outside a charge line or quote: 'February 2, 2026 — Hobbleton Family Clinic, visit'
PROBLEM case_09/counted: date-like text outside a charge line or quote: 'Left wrist pain 4/10. Splint applied. Return in 2 weeks.'
PROBLEM case_09/counted: date-like text outside a charge line or quote: 'March 12, 2026 — Hobbleton Family Clinic, phone note'
PROBLEM case_09/counted: date-like text outside a charge line or quote: 'March 30, 2026 — Hobbleton Family Clinic, visit'
PROBLEM case_09/counted: date-like text outside a charge line or quote: 'Left wrist pain 3/10. Splint removed.'
PROBLEM case_09/counted: date-like text outside a charge line or quote: 'April 13, 2026 — Hobbleton Family Clinic, visit'
PROBLEM case_09/counted: date-like text outside a charge line or quote: 'Pain 1/10. Released from care.'
PROBLEM lib10/all_accepted: date-like text outside a charge line or quote: 'June 9, 2026 — Saltmarrow General Hospital ED'
PROBLEM lib10/all_accepted: date-like text outside a charge line or quote: 'June 12, 2026 — Saltmarrow General Hospital, discharge summary'
PROBLEM lib10/all_accepted: date-like text outside a charge line or quote: 'June 24, 2026 — Dr. Ignatius Wardlaw, orthopedics, new patient'
PROBLEM lib10/all_accepted: date-like text outside a charge line or quote: 'Left knee pain 5/10; MRI of the left knee ordered.'
PROBLEM lib10/all_accepted: date-like text outside a charge line or quote: 'July 3, 2026 — Quoinmere Mutual Health Plan, EOB'
PROBLEM lib10/all_accepted: date-like text outside a charge line or quote: 'July 8, 2026 — Dr. Ignatius Wardlaw, orthopedics, follow-up'
PROBLEM lib10/all_accepted: date-like text outside a charge line or quote: 'Left knee pain 3/10. Injection performed. Continue home exercises.'
PROBLEM lib10/all_accepted: date-like text outside a charge line or quote: 'August 26, 2026 — Dr. Ignatius Wardlaw, orthopedics, follow-up'
PROBLEM lib10/all_accepted: date-like text outside a charge line or quote: 'Left knee pain 2/10. Discharged from care.'
PROBLEM lib10/counted: date-like text outside a charge line or quote: 'June 9, 2026 — Saltmarrow General Hospital ED'
PROBLEM lib10/counted: date-like text outside a charge line or quote: 'June 12, 2026 — Saltmarrow General Hospital, discharge summary'
PROBLEM lib10/counted: date-like text outside a charge line or quote: 'June 24, 2026 — Dr. Ignatius Wardlaw, orthopedics, new patient'
PROBLEM lib10/counted: date-like text outside a charge line or quote: 'Left knee pain 5/10; MRI of the left knee ordered.'
PROBLEM lib10/counted: date-like text outside a charge line or quote: 'July 3, 2026 — Quoinmere Mutual Health Plan, EOB'
PROBLEM lib10/counted: date-like text outside a charge line or quote: 'July 8, 2026 — Dr. Ignatius Wardlaw, orthopedics, follow-up'
PROBLEM lib10/counted: date-like text outside a charge line or quote: 'Left knee pain 3/10. Injection performed. Continue home exercises.'
PROBLEM lib10/counted: date-like text outside a charge line or quote: 'August 26, 2026 — Dr. Ignatius Wardlaw, orthopedics, follow-up'
PROBLEM lib10/counted: date-like text outside a charge line or quote: 'Left knee pain 2/10. Discharged from care.'
PROBLEM lib11/all_accepted: date-like text outside a charge line or quote: 'March 18, 2026 — Wexcombe Memorial ED'
PROBLEM lib11/all_accepted: date-like text outside a charge line or quote: 'March 27, 2026 — Fennimoor Spine Clinic, new patient'
PROBLEM lib11/all_accepted: date-like text outside a charge line or quote: 'Neck pain 7/10 and low back pain 7/10; treating under a letter of protection; plan is chiropractic care three times weekly.'
PROBLEM lib11/all_accepted: date-like text outside a charge line or quote: 'March 27, 2026 — Fennimoor Spine Clinic, new patient intake form (OCR text)'
PROBLEM lib11/all_accepted: date-like text outside a charge line or quote: 'April 24, 2026 — Fennimoor Spine Clinic, visit 8'
PROBLEM lib11/all_accepted: date-like text outside a charge line or quote: 'Neck pain 5/10 and low back pain 6/10; manual therapy and exercises continued.'
PROBLEM lib11/all_accepted: date-like text outside a charge line or quote: 'May 29, 2026 — Fennimoor Spine Clinic, visit 14'
PROBLEM lib11/all_accepted: date-like text outside a charge line or quote: 'Neck pain 4/10, low back pain 5/10. Care continues.'
PROBLEM lib11/counted: date-like text outside a charge line or quote: 'March 18, 2026 — Wexcombe Memorial ED'
PROBLEM lib11/counted: date-like text outside a charge line or quote: 'March 27, 2026 — Fennimoor Spine Clinic, new patient'
PROBLEM lib11/counted: date-like text outside a charge line or quote: 'Neck pain 7/10 and low back pain 7/10; treating under a letter of protection; plan is chiropractic care three times weekly.'
PROBLEM lib11/counted: date-like text outside a charge line or quote: 'March 27, 2026 — Fennimoor Spine Clinic, new patient intake form (OCR text)'
PROBLEM lib11/counted: date-like text outside a charge line or quote: 'April 24, 2026 — Fennimoor Spine Clinic, visit 8'
PROBLEM lib11/counted: date-like text outside a charge line or quote: 'Neck pain 5/10 and low back pain 6/10; manual therapy and exercises continued.'
PROBLEM lib11/counted: date-like text outside a charge line or quote: 'May 29, 2026 — Fennimoor Spine Clinic, visit 14'
PROBLEM lib11/counted: date-like text outside a charge line or quote: 'Neck pain 4/10, low back pain 5/10. Care continues.'
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:01:40.463Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF' 2>&1 | head -5\nimport pathlib\np = pathlib.Path(\"artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.py\")\ns = p.read_text()\nold = '''        for line in letter.splitlines():\n            stripped = re.sub(r'\"[^\"]*\"', \"\", line)\n            stripped = LINE.sub(\"\", stripped) if False else stripped\n            if ANY_DATE.search(stripped) and not LINE.search(re.sub(r\": \\\\$[\\\\d,]+\\\\.\\\\d\\\\d$\", \"\", line)) and not line.startswith(LC.TOTAL):\n                problems.append(f\"{name}/{variant}: date-like text outside a charge line or quote: {line[:160]!r}\")'''\nnew = '''        # inside the BILLED CHARGES section only (the timeline above it is dated by design): no date-like text outside a quote, except the charge heads checked above\n        for line in tail_lines:\n            if re.search(r\": \\\\$[\\\\d,]+\\\\.\\\\d\\\\d$\", line) or line.startswith(LC.TOTAL):\n                continue\n            stripped = re.sub(r'\"[^\"]*\"', \"\", line)\n            if ANY_DATE.search(stripped):\n                problems.append(f\"{name}/{variant}: date-like text in the BILLED CHARGES section outside a quote: {line[:160]!r}\")'''\nassert s.count(old) == 1, s.count(old)\np.write_text(s.replace(old, new))\nprint(\"patched\")\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.py artifacts/review-evidence/T-202-paralegal-r7/archive > artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.out 2>&1; echo EXIT=$?; head -1 artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.out; grep -c \"form=True recdate=True kind=True src=True\" artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.out; grep \"PROBLEM\" artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.out | head; grep -c TEETH artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.out",
 "description": "Patch the outside-section check to the charges section only and rerun"
}
````

### User / tool · 2026-11-03T15:01:45.209Z

**tool result**
````
patched
EXIT=0
{"archive": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive", "charge_lines_checked": 19, "problems": 0, "teeth_all_rejected": true}
19
8
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:01:50.191Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/run_letter_check_r7.py",
 "content": "\"\"\"Runs `python -m evals.letter_check` against an archive root, with -I (no cwd or script-dir on sys.path; the archive root is inserted first).\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/run_letter_check_r7.py <archive_root>\nEquivalent to `cd <archive_root> && python -m evals.letter_check`; the exit code is letter_check's.\n\"\"\"\nimport os\nimport runpy\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nos.environ.setdefault(\"LLM_BACKEND\", \"fixture\")\nos.environ.setdefault(\"FIXTURE_SET\", \"curated\")\nsys.argv = [\"evals.letter_check\"]\nrunpy.run_module(\"evals.letter_check\", run_name=\"__main__\", alter_sys=True)\n"
}
````

### User / tool · 2026-11-03T15:01:50.281Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/run_letter_check_r7.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:01:52.111Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/run_letter_check_r7.py artifacts/review-evidence/T-202-paralegal-r7/archive > artifacts/review-evidence/T-202-paralegal-r7/letter_check.out 2>&1; echo EXIT=$?; cut -c1-300 artifacts/review-evidence/T-202-paralegal-r7/letter_check.out",
 "description": "Run python -m evals.letter_check equivalent on the HEAD archive"
}
````

### User / tool · 2026-11-03T15:02:03.171Z

**tool result**
````
EXIT=0
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:02:05.910Z

**tool call — Bash**
````
{
 "command": "sed -n '60,200p' artifacts/review-evidence/T-202-paralegal-r6/fullpipe_r6.py | head -120",
 "description": "Read the rest of the round-6 full-pipeline probe shapes and printing logic"
}
````

### User / tool · 2026-11-03T15:02:05.991Z

**tool result**
````
    "a10_pcp_note_yesterday_uc [truth Jan 15]": ("310", add(OVN, "Patient went to urgent care yesterday, urgent care visit charge $310.00.", "2026-01-16")),
    "a11_pcp_note_ambulance_collision_day [truth Jan 9]": ("1,380", add(OVN, "Ambulance transport on the day of the collision, charge $1,380.00.", "2026-01-16")),
    "a12_pcp_note_february_followup [truth Feb]": ("150", add(OVN, "February follow-up visit 99213 charge $150.00.", "2026-03-05")),
    "a13_nota_consulta_anterior [truth earlier]": ("150", add("Clinica del Sol, nota de consulta", "Dolor cervical 5/10. Cargo de la consulta anterior: $150.00.", "2026-03-05")),
    "a14_nota_consulta_2_feb [truth Feb 2]": ("150", add("Clinica del Sol, nota de consulta", "Dolor cervical 5/10. Cargo de la consulta del 2 de febrero de 2026: $150.00.", "2026-03-05")),
    "a16_pcp_note_original_er_charge [truth Jan 9]": ("6,240", add(OVN, "Original ER charge $6,240.00 reviewed with patient.", "2026-01-16")),
    "a17_control_er_record_own_charge [truth Jan 9]": ("6,240", add("Central ER, emergency department record", "Dx: cervical strain. ER facility charge $6,240.00.", "2026-01-09")),
    "a18_control_pt_note_discharge_visit [truth Mar 6]": ("185", pt9(PTN, D + "Discharge visit 97110 charge $185.00.")),
    "a20_mri_report_comparison_xray [truth Jan 9]": ("240", add("Austin Imaging, MRI report", "Comparison: ER cervical x-ray. ER x-ray charge $240.00.", "2026-05-29")),
    "a15_pt_note_dos_table_total [truth Jan 23-Mar 6 for the total]": ("435", pt9(PTN, "DOS         CPT    Charge\n01/23/2026  97161  $250.00\n03/06/2026  97110  $185.00\nTotal              $435.00")),
    "u1_ub04_line_date_outside_span [record contradicts itself: blank]": ("2,105", c09("Saltmarrow General Hospital, UB-04", "UB-04. Statement covers period 02/09/2026 through 02/12/2026. Rev 0450 99285 emergency room, service date 02/05/2026, FL47 total charges $2,105.00.")),
    # r5 shapes (blocker, major) re-run
    "m1_austin_mri_bill [truth May 29 or blank]": ("2,150", mri_bill("Austin MRI", "Date of service 05/29/2026. Cervical spine MRI, CPT 72141, charge $2,150.")),
    "m2_open_mri_bill [truth May 29 or blank]": ("2,150", mri_bill("Open MRI of Austin", "Cervical spine MRI without contrast performed 05/29/2026. MRI charge: $2,150.")),
    "c1_followup_clinic_bill [truth Feb 2 or blank]": ("275", c09("Hobbleton Follow-Up Clinic", "Date of service 2026-02-02. Office visit 99213 charge $275.")),
    "c2_xray_bill [truth Feb 2 or blank]": ("275", c09("Hobbleton X-Ray", "Wrist x-ray performed 2026-02-02. Wrist x-ray 3 views, CPT 73110, charge $275.")),
    "c3_evaluation_center_bill [truth Feb 2 or blank]": ("275", c09("Hobbleton Hand Evaluation Center", "Seen 2026-02-02. Hand evaluation 97165 charge $275.")),
    "c4_exam_urgent_care_bill [truth Feb 2 or blank]": ("275", c09("Express Exam Urgent Care", "Visit 2026-02-02. Urgent care visit 99213 charge $275.")),
    "t4_kv_dos_line_over_row [truth Feb 2 or blank]": ("275", c09("Hobbleton Family Clinic, billing statement", "Date of service: 02/02/2026     Account: 4471\n02/20/2026   Office visit 99213   $275.00")),
    "t4b_kv_dos_over_date_posted_table [truth Feb 2 or blank]": ("275", c09("Hobbleton Family Clinic, billing statement", "Date of service: 02/02/2026\nDate posted  Description         Charge\n02/20/2026   Office visit 99213  $275.00\n02/21/2026   X-ray 73110         $90.00")),
    "t5_visit_date_over_next_visit_table [truth Feb 2]": ("275", c09("Hobbleton Family Clinic, billing statement", "Visit date  Next visit  CPT    Charge\n02/02/2026  02/16/2026  99213  $275.00\n02/16/2026  03/02/2026  99213  $90.00")),
    "t5b_next_visit_first [truth Feb 2]": ("275", c09("Hobbleton Family Clinic, billing statement", "Next visit  Visit date  CPT    Charge\n02/16/2026  02/02/2026  99213  $275.00\n03/02/2026  02/16/2026  99213  $90.00")),
    "t1_control_dos_column_two_rows [truth Feb 2]": ("275", c09("Hobbleton Family Clinic, billing statement", "Posted      DOS         Description           Amount\n02/20/2026  02/02/2026  Office visit 99213    $275.00\n02/27/2026  02/16/2026  X-ray 73110           $90.00")),
}
only = os.environ.get("ONLY")
for name, (fig, text) in CASES.items():
    if only and not any(name.startswith(o) for o in only.split(",")):
        continue
    got = LC.letters_for(text)
    for variant in ("all_accepted", "counted"):
        v = got[variant]
        letter = v["letters"]["standard"]
        print(f"== {name} {variant}: cents={v['charge_cents']}")
        for h, q in LC.charge_lines(letter):
            if fig in h or fig in q:
                print("   ", h, "|", q)
        print("    date violations:", LC.charge_date_violations(letter, v["records"]))
        for line in v["notes"].splitlines():
            if fig in line:
                print("    notes:", line)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:02:08.506Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r6/fullpipe_r6.py artifacts/review-evidence/T-202-paralegal-r7/archive > artifacts/review-evidence/T-202-paralegal-r7/fullpipe_r6_shapes_at_a932fc9.out 2>&1; echo EXIT=$?; wc -l artifacts/review-evidence/T-202-paralegal-r7/fullpipe_r6_shapes_at_a932fc9.out; cut -c1-330 artifacts/review-evidence/T-202-paralegal-r7/fullpipe_r6_shapes_at_a932fc9.out | head -150",
 "description": "Run the round-6 adversarial shapes through the full pipeline on the HEAD archive"
}
````

### User / tool · 2026-11-03T15:02:18.350Z

**tool result**
````
EXIT=0
     264 artifacts/review-evidence/T-202-paralegal-r7/fullpipe_r6_shapes_at_a932fc9.out
== a1_pcp_note_er_charge [truth Jan 9] all_accepted: cents=[624000, 215000, 624000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | ER charges: $6,240.
    Dr. Alvarez, office visit note, date of service [__________] (record dated January 16, 2026): $6,240.00 | ER facility charge $6,240.00.
    date violations: []
    notes: - Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
    notes: - Dr. Alvarez, $6,240.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a1_pcp_note_er_charge [truth Jan 9] counted: cents=[624000, 215000, 624000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | ER charges: $6,240.
    Dr. Alvarez, office visit note, date of service [__________] (record dated January 16, 2026): $6,240.00 | ER facility charge $6,240.00.
    date violations: []
    notes: - Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
    notes: - Dr. Alvarez, $6,240.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a2_pt_note_initial_eval [truth Jan 23] all_accepted: cents=[624000, 25000, 215000]
    Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $250.00 | Initial evaluation 97161 charge $250.00.
    date violations: []
    notes: - Capital PT, $250.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a2_pt_note_initial_eval [truth Jan 23] counted: cents=[624000, 25000, 215000]
    Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $250.00 | Initial evaluation 97161 charge $250.00.
    date violations: []
    notes: - Capital PT, $250.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a3_pt_note_first_visit [truth Jan 23] all_accepted: cents=[624000, 25000, 215000]
    Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $250.00 | First visit charge $250.00.
    date violations: []
    notes: - Capital PT, $250.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a3_pt_note_first_visit [truth Jan 23] counted: cents=[624000, 25000, 215000]
    Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $250.00 | First visit charge $250.00.
    date violations: []
    notes: - Capital PT, $250.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a4_addendum_01_20 [truth Jan 16] all_accepted: cents=[624000, 215000]
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | Charge: $2,150.
    date violations: []
    notes: - Record 10 (Dr. Alvarez, progress note addendum, January 20, 2026): "Office visit 99213 charge corrected to $150.00." Amount unclear ($150.00). Request clean copy of bill.
    notes: - Austin Imaging, $2,150: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a4_addendum_01_20 [truth Jan 16] counted: cents=[624000, 215000]
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | Charge: $2,150.
    date violations: []
    notes: - Record 10 (Dr. Alvarez, progress note addendum, January 20, 2026): "Office visit 99213 charge corrected to $150.00." Amount unclear ($150.00). Request clean copy of bill.
    notes: - Austin Imaging, $2,150: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a5_late_entry_01_20 [truth Jan 16] all_accepted: cents=[624000, 215000, 15000]
    Dr. Alvarez, office visit note, date of service [__________] (record dated January 20, 2026): $150.00 | Office visit 99213 charge $150.00.
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | Charge: $2,150.
    date violations: []
    notes: - Dr. Alvarez, $150.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
    notes: - Austin Imaging, $2,150: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a5_late_entry_01_20 [truth Jan 16] counted: cents=[624000, 215000, 15000]
    Dr. Alvarez, office visit note, date of service [__________] (record dated January 20, 2026): $150.00 | Office visit 99213 charge $150.00.
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | Charge: $2,150.
    date violations: []
    notes: - Dr. Alvarez, $150.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
    notes: - Austin Imaging, $2,150: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a6_inpatient_discharge_summary [truth Jun 9-12] all_accepted: cents=[624000, 215000]
    date violations: []
    notes: - Record 10 (Saltmarrow General Hospital, discharge summary, June 12, 2026): "Total hospital charges $4,920.00." Not totaled ($4,920.00): The sentence names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized charge and is not totaled.
== a6_inpatient_discharge_summary [truth Jun 9-12] counted: cents=[624000, 215000]
    date violations: []
    notes: - Record 10 (Saltmarrow General Hospital, discharge summary, June 12, 2026): "Total hospital charges $4,920.00." Not totaled ($4,920.00): The sentence names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized charge and is not totaled.
== a6b_er_overnight_discharge_summary [truth Jan 9-10] all_accepted: cents=[624000, 215000]
    Central ER discharge summary, date of service [__________] (record dated January 10, 2026): $6,240.00 | ER charges: $6,240.
    date violations: []
    notes: - Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a6b_er_overnight_discharge_summary [truth Jan 9-10] counted: cents=[624000, 215000]
    Central ER discharge summary, date of service [__________] (record dated January 10, 2026): $6,240.00 | ER charges: $6,240.
    date violations: []
    notes: - Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a7_pt_note_course_charges [truth Jan 23-Mar 6] all_accepted: cents=[624000, 166500, 215000]
    Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $1,665.00 | Physical therapy charges: $1,665.
    date violations: []
    notes: - Capital PT, $1,665: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a7_pt_note_course_charges [truth Jan 23-Mar 6] counted: cents=[624000, 166500, 215000]
    Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $1,665.00 | Physical therapy charges: $1,665.
    date violations: []
    notes: - Capital PT, $1,665: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a10_pcp_note_yesterday_uc [truth Jan 15] all_accepted: cents=[624000, 215000, 31000]
    Dr. Alvarez, office visit note, date of service [__________] (record dated January 16, 2026): $310.00 | Patient went to urgent care yesterday, urgent care visit charge $310.00.
    date violations: []
    notes: - Dr. Alvarez, $310.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a10_pcp_note_yesterday_uc [truth Jan 15] counted: cents=[624000, 215000, 31000]
    Dr. Alvarez, office visit note, date of service [__________] (record dated January 16, 2026): $310.00 | Patient went to urgent care yesterday, urgent care visit charge $310.00.
    date violations: []
    notes: - Dr. Alvarez, $310.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a11_pcp_note_ambulance_collision_day [truth Jan 9] all_accepted: cents=[624000, 215000, 138000]
    Dr. Alvarez, office visit note, date of service [__________] (record dated January 16, 2026): $1,380.00 | Ambulance transport on the day of the collision, charge $1,380.00.
    date violations: []
    notes: - Dr. Alvarez, $1,380.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a11_pcp_note_ambulance_collision_day [truth Jan 9] counted: cents=[624000, 215000, 138000]
    Dr. Alvarez, office visit note, date of service [__________] (record dated January 16, 2026): $1,380.00 | Ambulance transport on the day of the collision, charge $1,380.00.
    date violations: []
    notes: - Dr. Alvarez, $1,380.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a12_pcp_note_february_followup [truth Feb] all_accepted: cents=[624000, 215000, 15000]
    Dr. Alvarez, office visit note, date of service [__________] (record dated March 5, 2026): $150.00 | February follow-up visit 99213 charge $150.00.
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | Charge: $2,150.
    date violations: []
    notes: - Dr. Alvarez, $150.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
    notes: - Austin Imaging, $2,150: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a12_pcp_note_february_followup [truth Feb] counted: cents=[624000, 215000, 15000]
    Dr. Alvarez, office visit note, date of service [__________] (record dated March 5, 2026): $150.00 | February follow-up visit 99213 charge $150.00.
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | Charge: $2,150.
    date violations: []
    notes: - Dr. Alvarez, $150.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
    notes: - Austin Imaging, $2,150: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a13_nota_consulta_anterior [truth earlier] all_accepted: cents=[624000, 215000]
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | Charge: $2,150.
    date violations: []
    notes: - Record 10 (Clinica del Sol, nota de consulta, March 5, 2026): "Cargo de la consulta anterior: $150.00." Not classified as a charge ($150.00); check the original quote.
    notes: - Austin Imaging, $2,150: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a13_nota_consulta_anterior [truth earlier] counted: cents=[624000, 215000]
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | Charge: $2,150.
    date violations: []
    notes: - Record 10 (Clinica del Sol, nota de consulta, March 5, 2026): "Cargo de la consulta anterior: $150.00." Not classified as a charge ($150.00); check the original quote.
    notes: - Austin Imaging, $2,150: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a14_nota_consulta_2_feb [truth Feb 2] all_accepted: cents=[624000, 215000]
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | Charge: $2,150.
    date violations: []
    notes: - Record 10 (Clinica del Sol, nota de consulta, March 5, 2026): "Cargo de la consulta del 2 de febrero de 2026: $150.00." Not classified as a charge ($150.00); check the original quote.
    notes: - Austin Imaging, $2,150: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a14_nota_consulta_2_feb [truth Feb 2] counted: cents=[624000, 215000]
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | Charge: $2,150.
    date violations: []
    notes: - Record 10 (Clinica del Sol, nota de consulta, March 5, 2026): "Cargo de la consulta del 2 de febrero de 2026: $150.00." Not classified as a charge ($150.00); check the original quote.
    notes: - Austin Imaging, $2,150: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a16_pcp_note_original_er_charge [truth Jan 9] all_accepted: cents=[624000, 215000, 624000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | ER charges: $6,240.
    Dr. Alvarez, office visit note, date of service [__________] (record dated January 16, 2026): $6,240.00 | Original ER charge $6,240.00 reviewed with patient.
    date violations: []
    notes: - Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
    notes: - Dr. Alvarez, $6,240.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a16_pcp_note_original_er_charge [truth Jan 9] counted: cents=[624000, 215000, 624000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | ER charges: $6,240.
    Dr. Alvarez, office visit note, date of service [__________] (record dated January 16, 2026): $6,240.00 | Original ER charge $6,240.00 reviewed with patient.
    date violations: []
    notes: - Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
    notes: - Dr. Alvarez, $6,240.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a17_control_er_record_own_charge [truth Jan 9] all_accepted: cents=[624000, 215000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | ER charges: $6,240.
    date violations: []
    notes: - Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a17_control_er_record_own_charge [truth Jan 9] counted: cents=[624000, 215000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | ER charges: $6,240.
    date violations: []
    notes: - Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a18_control_pt_note_discharge_visit [truth Mar 6] all_accepted: cents=[624000, 18500, 215000]
    Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $185.00 | Discharge visit 97110 charge $185.00.
    date violations: []
    notes: - Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned). Request itemized PT ledger.
    notes: - Capital PT, $185.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== a18_control_pt_note_discharge_visit [truth Mar 6] counted: cents=[624000, 18500, 215000]
    Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $185.00 | Discharge visit 97110 charge $185.00.
    date violations: []
    notes: - Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned). Request itemized PT ledger.
    notes: - Capital PT, $185.00: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:02:27.273Z

**tool call — Bash**
````
{
 "command": "sed -n '150,264p' artifacts/review-evidence/T-202-paralegal-r7/fullpipe_r6_shapes_at_a932fc9.out | grep -v \"^    notes: - .*: The letter does not take\" | cut -c1-330",
 "description": "Show the remaining round-6 shape results, dropping repeated notes lines"
}
````

### User / tool · 2026-11-03T15:02:27.390Z

**tool result**
````
== a20_mri_report_comparison_xray [truth Jan 9] all_accepted: cents=[624000, 215000, 24000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | ER charges: $6,240.
    Austin Imaging, MRI report, date of service [__________] (record dated May 29, 2026): $240.00 | ER x-ray charge $240.00.
    date violations: []
== a20_mri_report_comparison_xray [truth Jan 9] counted: cents=[624000, 215000, 24000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | ER charges: $6,240.
    Austin Imaging, MRI report, date of service [__________] (record dated May 29, 2026): $240.00 | ER x-ray charge $240.00.
    date violations: []
== a15_pt_note_dos_table_total [truth Jan 23-Mar 6 for the total] all_accepted: cents=[624000, 215000]
    date violations: []
    notes: - Record 6 (Capital PT, physical therapy note, March 6, 2026): "Total              $435.00" Not classified as a charge ($435.00); check the original quote.
== a15_pt_note_dos_table_total [truth Jan 23-Mar 6 for the total] counted: cents=[624000, 215000]
    date violations: []
    notes: - Record 6 (Capital PT, physical therapy note, March 6, 2026): "Total              $435.00" Not classified as a charge ($435.00); check the original quote.
== u1_ub04_line_date_outside_span [record contradicts itself: blank] all_accepted: cents=[210500]
    Saltmarrow General Hospital, UB-04, date of service [__________] (statement dated March 1, 2026): $2,105.00 | Rev 0450 99285 emergency room, service date 02/05/2026, FL47 total charges $2,105.00.
    date violations: []
== u1_ub04_line_date_outside_span [record contradicts itself: blank] counted: cents=[210500]
    Saltmarrow General Hospital, UB-04, date of service [__________] (statement dated March 1, 2026): $2,105.00 | Rev 0450 99285 emergency room, service date 02/05/2026, FL47 total charges $2,105.00.
    date violations: []
== m1_austin_mri_bill [truth May 29 or blank] all_accepted: cents=[624000, 215000]
    Austin MRI, date of service [__________] (record dated June 20, 2026): $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
    date violations: []
== m1_austin_mri_bill [truth May 29 or blank] counted: cents=[624000, 215000]
    Austin MRI, date of service [__________] (record dated June 20, 2026): $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
    date violations: []
== m2_open_mri_bill [truth May 29 or blank] all_accepted: cents=[624000, 215000]
    Open MRI of Austin, date of service [__________] (record dated June 20, 2026): $2,150.00 | MRI charge: $2,150.
    date violations: []
== m2_open_mri_bill [truth May 29 or blank] counted: cents=[624000, 215000]
    Open MRI of Austin, date of service [__________] (record dated June 20, 2026): $2,150.00 | MRI charge: $2,150.
    date violations: []
== c1_followup_clinic_bill [truth Feb 2 or blank] all_accepted: cents=[27500]
    Hobbleton Follow-Up Clinic, date of service [__________] (record dated March 1, 2026): $275.00 | Office visit 99213 charge $275.
    date violations: []
== c1_followup_clinic_bill [truth Feb 2 or blank] counted: cents=[27500]
    Hobbleton Follow-Up Clinic, date of service [__________] (record dated March 1, 2026): $275.00 | Office visit 99213 charge $275.
    date violations: []
== c2_xray_bill [truth Feb 2 or blank] all_accepted: cents=[27500]
    Hobbleton X-Ray, date of service [__________] (record dated March 1, 2026): $275.00 | Wrist x-ray 3 views, CPT 73110, charge $275.
    date violations: []
== c2_xray_bill [truth Feb 2 or blank] counted: cents=[27500]
    Hobbleton X-Ray, date of service [__________] (record dated March 1, 2026): $275.00 | Wrist x-ray 3 views, CPT 73110, charge $275.
    date violations: []
== c3_evaluation_center_bill [truth Feb 2 or blank] all_accepted: cents=[27500]
    Hobbleton Hand Evaluation Center, date of service [__________] (record dated March 1, 2026): $275.00 | Hand evaluation 97165 charge $275.
    date violations: []
== c3_evaluation_center_bill [truth Feb 2 or blank] counted: cents=[27500]
    Hobbleton Hand Evaluation Center, date of service [__________] (record dated March 1, 2026): $275.00 | Hand evaluation 97165 charge $275.
    date violations: []
== c4_exam_urgent_care_bill [truth Feb 2 or blank] all_accepted: cents=[27500]
    Express Exam Urgent Care, date of service [__________] (record dated March 1, 2026): $275.00 | Urgent care visit 99213 charge $275.
    date violations: []
== c4_exam_urgent_care_bill [truth Feb 2 or blank] counted: cents=[27500]
    Express Exam Urgent Care, date of service [__________] (record dated March 1, 2026): $275.00 | Urgent care visit 99213 charge $275.
    date violations: []
== t4_kv_dos_line_over_row [truth Feb 2 or blank] all_accepted: cents=[27500]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | 02/20/2026   Office visit 99213   $275.00
    date violations: []
    notes: - Hobbleton Family Clinic, $275.00: The line shows 02/20/2026, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemiz
== t4_kv_dos_line_over_row [truth Feb 2 or blank] counted: cents=[27500]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | 02/20/2026   Office visit 99213   $275.00
    date violations: []
    notes: - Hobbleton Family Clinic, $275.00: The line shows 02/20/2026, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemiz
== t4b_kv_dos_over_date_posted_table [truth Feb 2 or blank] all_accepted: cents=[27500, 9000]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | 02/20/2026   Office visit 99213  $275.00
    date violations: []
    notes: - Hobbleton Family Clinic, $275.00: The line shows 02/20/2026, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemiz
== t4b_kv_dos_over_date_posted_table [truth Feb 2 or blank] counted: cents=[27500, 9000]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | 02/20/2026   Office visit 99213  $275.00
    date violations: []
    notes: - Hobbleton Family Clinic, $275.00: The line shows 02/20/2026, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemiz
== t5_visit_date_over_next_visit_table [truth Feb 2] all_accepted: cents=[27500, 9000]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | 02/02/2026  02/16/2026  99213  $275.00
    date violations: []
== t5_visit_date_over_next_visit_table [truth Feb 2] counted: cents=[27500, 9000]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | 02/02/2026  02/16/2026  99213  $275.00
    date violations: []
== t5b_next_visit_first [truth Feb 2] all_accepted: cents=[27500, 9000]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | 02/16/2026  02/02/2026  99213  $275.00
    date violations: []
== t5b_next_visit_first [truth Feb 2] counted: cents=[27500, 9000]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | 02/16/2026  02/02/2026  99213  $275.00
    date violations: []
== t1_control_dos_column_two_rows [truth Feb 2] all_accepted: cents=[27500, 9000]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | 02/20/2026  02/02/2026  Office visit 99213    $275.00
    date violations: []
== t1_control_dos_column_two_rows [truth Feb 2] counted: cents=[27500, 9000]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | 02/20/2026  02/02/2026  Office visit 99213    $275.00
    date violations: []
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:02:36.493Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && sed -n '286,303p;436,461p;608,637p' app/backend/api.py | cut -c1-220",
 "description": "Read the create, run and export API routes at HEAD"
}
````

### User / tool · 2026-11-03T15:02:36.591Z

**tool result**
````
    @app.post("/api/cases", status_code=201)
    async def create_case(request: Request):
        b = await body_of(request)
        sample = b.get("sample") is True
        lib = None
        if isinstance(b.get("library"), str):
            if not local_mode():
                raise ApiError(404, "not_found", "Not found.")
            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
            if lib is None:
                raise ApiError(404, "not_found", "No such library case.")
        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
        if not isinstance(text, str):
            raise ApiError(400, "bad_request", "Provide text or sample: true.")
        typed = isinstance(b.get("title"), str)
        given = b.get("title") if typed else b.get("name")          # T-157: `title` is the name a paralegal types (refused when over 120 characters); `name` stays accepted (a long file name is cut)
        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample, strict_name=typed)

    @app.post("/api/cases/{token}/run", status_code=202)
    async def run_case(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            case = get_case(c, token)
            if case["status"] == "running" or token in runs:
                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
            if decided and b.get("confirm_rerun") is not True:
                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
            if (busy := limits.runs_busy(len(runs), local_mode())):  # T-183 r2: public demo runs at most DEMO_MAX_RUNS at once
                raise ApiError(429, "busy", busy, {"reason": "demo_busy"})
            now = time.time()
            store.run_started(token)
            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
            runs[token].start()
            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
        finally:
            c.close()

    @app.get("/api/cases/{token}/export")
    def export(token: str, style: str = None):
        from app.backend import export_routes as XR
        if style not in (None, *export_mod.STYLES):          # T-121: ?style=oneline | standard
            raise ApiError(422, "invalid_style", XR.invalid_style_message())
        c = conn()
        try:
            get_case(c, token)
            case = store.export_case(c, token)
            try:
                ex = XR.export_payload(token, case, style=style)
            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
            calls = DB.list_llm_calls(c, token)
            ok = ("accepted", "edited")
            tv = present.totals_view(c, token)
            ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
            ex["excluded"] = {"pending": case["pending_count"], "edit_not_confirmed": sum(1 for x in case["entries"] if x.get("edit_unconfirmed")),      # T-134: part of `pending`
                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
                              "rejected": present.rejected_count(c, token)}
            mm = present.models_for(c, token, config_models())
            ex["provenance"] = {"generator_model": mm["generator"], "judge_model": mm["judge"], "generator_prepared": mm["generator_prepared"], "backend": backend(),
                                "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"] and not AU.is_prepared(x.get("recorded_from"))}),
                                "edited_count": sum(1 for x in case["entries"] if x["review_status"] == "edited")}
            return ex
        finally:
            c.close()
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:02:40.997Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && grep -n \"uvicorn\\|PORT\\|port\" app/main.py | head -12; grep -n \"7860\\|python -m app\\|app.main\\|uvicorn\" docs/RUNBOOK.md | head -8; grep -n \"^demo\\|demo_mode()\" app/backend/*.py | head -3; grep -rn \"def demo_mode\" app | head -3",
 "description": "Find how the app server starts and how demo mode is detected"
}
````

### User / tool · 2026-11-03T15:02:41.112Z

**tool result**
````
3:A startup misconfiguration (live opt-in without PROVIDER_CAP_CONFIRMED=1, a port already in use, ...) prints one line naming the
5:import os
6:import sys
8:import uvicorn
10:from app.backend.api import create_app
14:    """uvicorn app.main:create --factory"""
24:    from app import config
25:    host, port = os.environ.get("HOST", "127.0.0.1"), int(os.environ.get("PORT", "7860"))
35:    if config.port_in_use(host, port):
36:        _fail(f"port {port} on {host} is already in use. Pick another with PORT=7870 (for example `PORT=7870 ./run.sh`).", 3)
37:    print(f"Serving on http://{host}:{port}  (Ctrl-C to stop)", flush=True)
38:    uvicorn.run(app, host=host, port=port, access_log=False, log_level="warning")
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
9:| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |
app/backend/api.py:127:    def demo_mode():
app/backend/api.py:266:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "local_mode": local_mode(), "answers": ans,
app/backend/api.py:308:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
app/backend/api.py:127:    def demo_mode():
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:02:48.238Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/serve_r7.py",
 "content": "\"\"\"Serves an archive root's app (app.main) for the T-202 r7 check. Run with -I:\n    PORT=7987 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/serve_r7.py <archive_root>\n\"\"\"\nimport os\nimport runpy\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nsys.argv = [\"app.main\"]\nrunpy.run_module(\"app.main\", run_name=\"__main__\", alter_sys=True)\n"
}
````

### User / tool · 2026-11-03T15:02:48.349Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/serve_r7.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:02:50.417Z

**tool call — Bash**
````
{
 "command": "(PORT=7987 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated nohup .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/serve_r7.py artifacts/review-evidence/T-202-paralegal-r7/archive > artifacts/review-evidence/T-202-paralegal-r7/server_7987.log 2>&1 &) ; sleep 6; curl -s http://127.0.0.1:7987/api/health | cut -c1-400; echo; lsof -iTCP:7987 -sTCP:LISTEN -nP",
 "description": "Start the HEAD archive app on port 7987 in local mode and check health"
}
````

### User / tool · 2026-11-03T15:02:56.615Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the

COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  84772 arsis    9u  IPv4 0xdc43e402f1188e33      0t0  TCP 127.0.0.1:7987 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:03:07.333Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/live_letters_r7.py",
 "content": "\"\"\"T-202 r7: drive the running HEAD archive app over HTTP (the same routes the UI calls), accept every item the code lets a reviewer accept,\nthen read the export's letter text and check each BILLED CHARGES line with the same exact-form rule as check_letters_r7.py.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/live_letters_r7.py http://127.0.0.1:7987 <out_dir>\nWrites <out_dir>/<case>-letter.txt and <out_dir>/<case>-items.json; prints a summary line per case.\n\"\"\"\nimport json\nimport os\nimport re\nimport sys\nimport time\nimport urllib.error\nimport urllib.request\n\nBASE = sys.argv[1].rstrip(\"/\")\nOUT = os.path.abspath(sys.argv[2])\nROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), \"archive\"))\nCASES = {\n    \"sample\": \"evals/golden/sample.txt\",\n    \"case_09\": \"evals/golden/case_09_nonvisit_hides_gap.txt\",\n    \"lib10\": \"evals/library/case_lib10_eob_ub04_cms1500.txt\",\n    \"lib11\": \"evals/library/case_lib11_priors_and_ledger.txt\",\n}\nLINE = re.compile(r\"^(?P<src>.+), date of service \\[__________\\] \\((?P<kind>statement|record) dated [A-Z][a-z]+ \\d{1,2}, \\d{4}\\)$\")\n\n\ndef call(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    req = urllib.request.Request(BASE + path, data=data, method=method, headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=60) as r:\n            raw = r.read().decode()\n            return r.status, (json.loads(raw) if raw else None)\n    except urllib.error.HTTPError as e:\n        raw = e.read().decode()\n        try:\n            return e.code, json.loads(raw)\n        except ValueError:\n            return e.code, raw\n\n\ndef walk_items(obj, found):\n    \"\"\"Collect {id, kind, review_status, ...} dicts from any list of items in the case JSON (kind in entry/amount/flag).\"\"\"\n    if isinstance(obj, dict):\n        if \"id\" in obj and obj.get(\"kind\") in (\"entry\", \"amount\", \"flag\", \"charge\") and \"review_status\" in obj:\n            found.append(obj)\n        for v in obj.values():\n            walk_items(v, found)\n    elif isinstance(obj, list):\n        for v in obj:\n            walk_items(v, found)\n    return found\n\n\ndef main():\n    os.makedirs(OUT, exist_ok=True)\n    summary = []\n    for name, rel in CASES.items():\n        text = open(os.path.join(ROOT, rel), encoding=\"utf-8\").read()\n        st, made = call(\"POST\", \"/api/cases\", {\"text\": text, \"title\": f\"r7 {name}\"})\n        if st != 201:\n            summary.append({\"case\": name, \"error\": f\"create {st}\", \"body\": str(made)[:300]})\n            continue\n        token = made.get(\"token\") or made.get(\"case\", {}).get(\"token\")\n        st, run = call(\"POST\", f\"/api/cases/{token}/run\", {})\n        if st != 202:\n            summary.append({\"case\": name, \"error\": f\"run {st}\", \"body\": str(run)[:300]})\n            continue\n        for _ in range(240):\n            st, s = call(\"GET\", f\"/api/cases/{token}/status\")\n            if isinstance(s, dict) and s.get(\"status\") not in (\"running\", None):\n                break\n            time.sleep(0.5)\n        st, case = call(\"GET\", f\"/api/cases/{token}\")\n        items = walk_items(case, [])\n        accepted, refused = 0, []\n        for it in items:\n            if it.get(\"review_status\") not in (\"pending\", None):\n                continue\n            st, r = call(\"POST\", f\"/api/cases/{token}/items/{it['id']}/review\", {\"action\": \"accept\"})\n            if st in (200, 201):\n                accepted += 1\n            else:\n                refused.append((it[\"id\"], it.get(\"kind\"), st, (r or {}).get(\"error\", {}).get(\"code\") if isinstance(r, dict) and isinstance(r.get(\"error\"), dict) else str(r)[:80]))\n        st, ex = call(\"GET\", f\"/api/cases/{token}/export\")\n        letter = ex.get(\"letter_text\") if isinstance(ex, dict) else None\n        if letter is None and isinstance(ex, dict):\n            letter = (ex.get(\"letter\") or {}).get(\"text\") if isinstance(ex.get(\"letter\"), dict) else ex.get(\"letter\")\n        if not isinstance(letter, str):\n            summary.append({\"case\": name, \"error\": f\"export {st}\", \"keys\": sorted(ex.keys()) if isinstance(ex, dict) else str(ex)[:200]})\n            continue\n        with open(os.path.join(OUT, f\"{name}-letter.txt\"), \"w\", encoding=\"utf-8\") as f:\n            f.write(letter)\n        with open(os.path.join(OUT, f\"{name}-items.json\"), \"w\", encoding=\"utf-8\") as f:\n            json.dump({\"accepted\": accepted, \"refused\": refused, \"items\": len(items)}, f, indent=1)\n        heads = [l for l in letter.splitlines() if re.search(r\": \\$[\\d,]+\\.\\d\\d$\", l) and not l.startswith(\"Billed charges\")]\n        bad = [h for h in heads if not LINE.match(re.sub(r\": \\$[\\d,]+\\.\\d\\d$\", \"\", h))]\n        total = [l for l in letter.splitlines() if l.startswith(\"Billed charges\")]\n        summary.append({\"case\": name, \"token\": token, \"items\": len(items), \"accepted\": accepted, \"refused\": len(refused), \"charge_lines\": len(heads),\n                        \"charge_lines_not_exact_blank\": bad, \"total_line\": total})\n    print(json.dumps(summary, indent=1, ensure_ascii=False))\n\n\nif __name__ == \"__main__\":\n    main()\n"
}
````

### User / tool · 2026-11-03T15:03:07.433Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/live_letters_r7.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:03:09.336Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/live_letters_r7.py http://127.0.0.1:7987 artifacts/review-evidence/T-202-paralegal-r7/live > artifacts/review-evidence/T-202-paralegal-r7/live_summary.out 2>&1; echo EXIT=$?; cut -c1-400 artifacts/review-evidence/T-202-paralegal-r7/live_summary.out | head -90",
 "description": "Drive the HEAD app over HTTP for four cases and check the exported letters"
}
````

### User / tool · 2026-11-03T15:03:11.970Z

**tool result**
````
EXIT=0
[
 {
  "case": "sample",
  "token": "DSJgqAWo8SysQZa1etn0vA",
  "items": 2,
  "accepted": 2,
  "refused": 0,
  "charge_lines": 2,
  "charge_lines_not_exact_blank": [],
  "total_line": [
   "Billed charges accepted from these records: $8,390.00"
  ]
 },
 {
  "case": "case_09",
  "token": "3lEEunfwvYCvGWODLPsyWg",
  "items": 1,
  "accepted": 1,
  "refused": 0,
  "charge_lines": 1,
  "charge_lines_not_exact_blank": [],
  "total_line": [
   "Billed charges accepted from these records: $275.00"
  ]
 },
 {
  "case": "lib10",
  "token": "7NUMmo3NAeUSxDBOXbpA8g",
  "items": 4,
  "accepted": 4,
  "refused": 0,
  "charge_lines": 4,
  "charge_lines_not_exact_blank": [],
  "total_line": [
   "Billed charges accepted from these records: $8,123.50"
  ]
 },
 {
  "case": "lib11",
  "token": "WViDrm5v6RWdz7yOujIH9A",
  "items": 1,
  "accepted": 1,
  "refused": 0,
  "charge_lines": 1,
  "charge_lines_not_exact_blank": [],
  "total_line": [
   "Billed charges accepted from these records: $3,260.00"
  ]
 }
]
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:03:17.331Z

**tool call — Bash**
````
{
 "command": "TOKEN=DSJgqAWo8SysQZa1etn0vA; curl -s http://127.0.0.1:7987/api/cases/$TOKEN > artifacts/review-evidence/T-202-paralegal-r7/live/sample-case.json; .venv/bin/python -I -c \"import json; d=json.load(open('artifacts/review-evidence/T-202-paralegal-r7/live/sample-case.json')); print(sorted(d.keys())); print({k: (type(v).__name__, len(v) if hasattr(v,'__len__') else v) for k,v in d.items()}); print(json.dumps((d.get('items') or [None])[0])[:600] if d.get('items') else 'no items key')\" 2>&1 | cut -c1-900",
 "description": "Inspect the case JSON shape from the live app"
}
````

### User / tool · 2026-11-03T15:03:17.476Z

**tool result**
````
['amounts', 'backend', 'checks', 'created_at', 'dates_to_confirm', 'demo_mode', 'entries', 'error', 'flags', 'gap_changes_removed', 'injection', 'models', 'name', 'next_action', 'records', 'review', 'status', 'title', 'token', 'totals', 'tray', 'tray_filtered', 'undated_entries', 'updated_at', 'warnings']
{'token': ('str', 22), 'name': ('str', 9), 'status': ('str', 5), 'demo_mode': ('bool', True), 'backend': ('str', 7), 'models': ('dict', 3), 'records': ('list', 9), 'undated_entries': ('list', 0), 'entries': ('list', 9), 'amounts': ('list', 4), 'totals': ('dict', 6), 'flags': ('list', 10), 'gap_changes_removed': ('list', 0), 'checks': ('dict', 5), 'tray': ('list', 0), 'tray_filtered': ('dict', 5), 'dates_to_confirm': ('list', 0), 'injection': ('dict', 2), 'review': ('dict', 3), 'warnings': ('list', 0), 'error': ('NoneType', None), 'created_at': ('str', 20), 'updated_at': ('str', 20), 'title': ('str', 9), 'next_action': ('dict', 3)}
no items key
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:03:20.024Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"import json; d=json.load(open('artifacts/review-evidence/T-202-paralegal-r7/live/sample-case.json')); print(json.dumps(d['entries'][0])[:500]); print(json.dumps(d['amounts'][0])[:500]); print(json.dumps(d['flags'][0])[:400])\" 2>&1 | cut -c1-700; curl -s -X POST -H 'Content-Type: application/json' -d '{\"action\":\"accept\"}' http://127.0.0.1:7987/api/cases/DSJgqAWo8SysQZa1etn0vA/items/nonexistent/review | cut -c1-200",
 "description": "Show one entry, amount and flag shape, and the review route response"
}
````

### User / tool · 2026-11-03T15:03:20.143Z

**tool result**
````
{"id": "e1", "state": "verified", "reasons": [], "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.", "review_status": "pending", "version": 1793718189.872724, "edited": null, "ladder": {"backend": "fixture", "code_checks": {"date_provider_from_header": true, "excerpt_verbatim": true, "excerpt_whole_sentence": true, "highlight_found": true, "qualifier_carried": true, "summary_tokens_not_in_excerpt": []}, "generator": {"call_id": "c5fd639d
{"id": "a1", "state": "verified", "reasons": [], "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.", "review_status": "accepted", "version": 1793718190.115125, "edited": null, "ladder": {"backend": "fixture", "code_checks": {"amount_in_text": true, "classified_by": "code:amounts"}, "generator": null, "human": {"action": "accept", "edited_text": null, "at": null}, "item_id": "a1", "judge": {"call_id": "cb6f9ebb81f01", "model": "claude-hai
{"id": "f_gap_r6_r7", "state": "verified", "reasons": [], "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.", "review_status": "pending", "version": 1793718189.872724, "edited": null, "ladder": {"backend": "fixture", "code_checks": {"computed_by": "code", "spans_match_input": true}, "generator": null, "human": {"action": null, "edited_text
{"error":{"code":"not_found","message":"No such item.","detail":{}}}
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:03:24.162Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport pathlib\np = pathlib.Path(\"artifacts/review-evidence/T-202-paralegal-r7/live_letters_r7.py\")\ns = p.read_text()\nold = '''        items = walk_items(case, [])'''\nnew = '''        items = list(case.get(\"entries\", [])) + list(case.get(\"amounts\", [])) + list(case.get(\"flags\", []))'''\nassert s.count(old) == 1\ns = s.replace(old, new)\nold2 = '''            if it.get(\"review_status\") not in (\"pending\", None):'''\nnew2 = '''            if it.get(\"review_status\") != \"pending\":'''\nassert s.count(old2) == 1\ns = s.replace(old2, new2)\np.write_text(s)\nprint(\"ok\")\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/live_letters_r7.py http://127.0.0.1:7987 artifacts/review-evidence/T-202-paralegal-r7/live > artifacts/review-evidence/T-202-paralegal-r7/live_summary.out 2>&1; echo EXIT=$?; cut -c1-300 artifacts/review-evidence/T-202-paralegal-r7/live_summary.out | grep -v \"^ *\\\"\\(token\\|items\\)\\\"\" | head -80; ls artifacts/review-evidence/T-202-paralegal-r7/live",
 "description": "Rerun the live check, accepting entries, amounts and flags, and summarize"
}
````

### User / tool · 2026-11-03T15:03:27.078Z

**tool result**
````
ok
EXIT=0
[
 {
  "case": "sample",
  "accepted": 23,
  "refused": 0,
  "charge_lines": 2,
  "charge_lines_not_exact_blank": [],
  "total_line": [
   "Billed charges accepted from these records: $8,390.00"
  ]
 },
 {
  "case": "case_09",
  "accepted": 6,
  "refused": 1,
  "charge_lines": 1,
  "charge_lines_not_exact_blank": [],
  "total_line": [
   "Billed charges accepted from these records: $275.00"
  ]
 },
 {
  "case": "lib10",
  "accepted": 15,
  "refused": 7,
  "charge_lines": 4,
  "charge_lines_not_exact_blank": [],
  "total_line": [
   "Billed charges accepted from these records: $8,123.50"
  ]
 },
 {
  "case": "lib11",
  "accepted": 19,
  "refused": 10,
  "charge_lines": 1,
  "charge_lines_not_exact_blank": [],
  "total_line": [
   "Billed charges accepted from these records: $3,260.00"
  ]
 }
]
case_09-items.json
case_09-letter.txt
lib10-items.json
lib10-letter.txt
lib11-items.json
lib11-letter.txt
sample-case.json
sample-items.json
sample-letter.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:03:30.782Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/live && grep -n -A1 \"BILLED CHARGES\\|date of service\" sample-letter.txt case_09-letter.txt lib10-letter.txt lib11-letter.txt | cut -c1-260",
 "description": "Show the live exported charge sections for the four cases"
}
````

### User / tool · 2026-11-03T15:03:30.872Z

**tool result**
````
case_09-letter.txt:19:BILLED CHARGES
case_09-letter.txt-20-
case_09-letter.txt:21:Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00
case_09-letter.txt-22-Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."
sample-letter.txt:39:BILLED CHARGES
sample-letter.txt-40-
sample-letter.txt:41:Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00
sample-letter.txt-42-Source [Ex. __ / Bates __]: "ER charges: $6,240."
sample-letter.txt:43:Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00
sample-letter.txt-44-Source [Ex. __ / Bates __]: "Charge: $2,150."
lib10-letter.txt:27:BILLED CHARGES
lib10-letter.txt-28-
lib10-letter.txt:29:Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $4,920.00
lib10-letter.txt-30-Source [Ex. __ / Bates __]: "FL47 total charges $4,920.00."
lib10-letter.txt:31:Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $2,105.00
lib10-letter.txt-32-Source [Ex. __ / Bates __]: "Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
lib10-letter.txt:33:Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $386.50
lib10-letter.txt-34-Source [Ex. __ / Bates __]: "Rev 0250 pharmacy, 14 units, FL47 total charges $386.50."
lib10-letter.txt:35:Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated June 19, 2026): $712.00
lib10-letter.txt-36-Source [Ex. __ / Bates __]: "Rev 0300 laboratory, 6 units, FL47 total charges $712.00."
lib11-letter.txt:23:BILLED CHARGES
lib11-letter.txt-24-
lib11-letter.txt:25:Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026): $3,260.00
lib11-letter.txt-26-Source [Ex. __ / Bates __]: "ED charge: $3,260."
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:04:12.868Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/archive && grep -n \"charge_when\\|cite_dated(\\|\\.cite(\\|date of service\\|not_stated_text\\|printed_text\" app/backend/*.py | cut -c1-230; echo ----; cd /Users/arsis/zlayt-pm-project && git diff --stat f6d5c19 a932fc9 -- app/backend/export.py app/backend/service_date.py evals/letter_check.py app/backend/amounts.py app/backend/store.py | tail -3; git log --oneline f6d5c19..a932fc9 -- app/backend evals | head; echo ----; grep -n \"D-062\" memory/ORCHESTRATOR_DECISIONS.md | cut -c1-260 | head -3",
 "description": "Find every path that prints a charge-line date and what changed since the gate pin"
}
````

### User / tool · 2026-11-03T15:04:13.017Z

**tool result**
````
app/backend/amounts.py:287:# An amount is a charge only when it sits on an itemized service line: a date of service, a service description (service noun, CPT, HCPCS or revenue code)
app/backend/amounts.py:289:# the date of service and the sentence must say charge/billed beside a service (or a bare "Charge:" under a header that names the service). Everything else is
app/backend/amounts.py:298:# a date that follows one of these words is a statement, billing, due or period date, never a date of service
app/backend/amounts.py:330:_NO_DATE_WHY = "The line states no date of service, so it is not an itemized service line and is not totaled."
app/backend/amounts.py:331:NO_DATE_WHY = _NO_DATE_WHY           # T-200: the stored reason of a charge the paralegal counted because its line states no date of service
app/backend/amounts.py:418:    end of a range (a range is a period, not a date of service). `tail=True`: text after the figure, where only a date led by DOS / on / for / of counts."""
app/backend/amounts.py:560:    # a dated encounter record: the record's date is the date of service
app/backend/amounts.py:724:    once she accepts it). `countable` is True only for a figure the code held back for a missing detail (no date of service, a document with no bill header), or one
app/backend/amounts.py:760:        if not basis["svc"]:              # D-064 r2: countable needs a service description and only a missing date of service or bill header
app/backend/amounts.py:833:    """Two charge bases (`charge_basis` dicts) describe the same service on the same day: same date of service and, by their descriptions, the same service. Codes
app/backend/amounts.py:845:    """D-060: a charge with the same normalized date of service, service and amount as an earlier charge of ANOTHER record (a statement re-listing a visit, in any
app/backend/amounts.py:918:    paralegal is asked, not told). A date is compared only when BOTH lines state one: a line with no date of service may be the same visit as a dated one."""
app/backend/export.py:210:    def charge_when(self, a):
app/backend/export.py:212:        date of service [__________] (statement dated June 15, 2026)' (a bill's own date is its statement date, any other record's its record date). The code extracts no service date for
app/backend/export.py:215:        return f"{self.source(n)}, {service_date.not_stated_text(self.rec_date(n), service_date.record_kind(self.source(n), self.text(n)))}"
app/backend/export.py:220:    def cite_dated(self, n):
app/backend/export.py:347:            out += [f"{v.charge_when(a)}: {_money(a['cents'])}",
app/backend/export.py:386:        return _terminate(f"{label}: {span}: " + " to ".join(v.cite(n) for n in recs))
app/backend/export.py:394:                    head = v.cite(n) if k == 0 else _cap(v.cite(n))
app/backend/export.py:399:                        head = v.cite(n) if k == 0 else _cap(v.cite(n))
app/backend/export.py:402:                        head = v.cite_dated(n)
app/backend/export.py:409:        items = [f'{v.cite(n)} "{v.quote(n, by_rec[n][0]["excerpt"], whole_sentence=True)}"' if by_rec[n] else v.cite(n)
app/backend/export.py:415:        s = f'{v.cite(n)} "{v.quote(n, x["excerpt"])}"' if x.get("field", "excerpt") == "excerpt" else v.cite(n)
app/backend/export.py:473:            out.append(f'- {_cap(v.cite(n))}: "{quote}" {_terminate(_cap("; ".join(hits[:1] + [h[:1].lower() + h[1:] for h in hits[1:]])))}')
app/backend/export.py:510:    out = [f'- {_cap(v.cite(a["record_no"]))}: charge {_money(a["cents"])} not exported and not totaled: excerpt not found in record.'
app/backend/export.py:531:        out.append(f"- {_cap(v.cite(n))}: {q} {body}")
app/backend/export.py:541:        line = (f"- Possible overlap: {v.cite(s_no)} lists {o.get('statement_text')} on a statement line, and {v.cite(c_no)} separately states "
app/backend/export.py:554:    out = [f'- {_cap(v.cite(a["record_no"]))}: "{_amount_quote(v, a)}"'
app/backend/export.py:564:                out.append(f'- {_cap(v.cite(r["n"]))}: "{s.strip()}" Request cost estimate.')
app/backend/export.py:597:    """T-202 r3 + D-073 fallback: one line per accepted charge (each prints the blank for its date of service): provider, amount, why, and the request for a dated itemized bill. [] when no
app/backend/export.py:602:        out.append(f"- {_provider(v.source(a['record_no'])) or v.source(a['record_no'])}, {a['raw']}: {why} The letter leaves a blank for the date of service; fill it from the quote or request a dated ite
app/backend/export.py:651:        lines.append(f"- {_cap(v.cite(n))} — {why}")
app/backend/export.py:685:            out.append(f'- {_cap(v.cite(e["record_no"]))}: entered by reviewer' + ("" if v.prepared else " (the AI did not draft this entry)") + f'; summary "{e["summary"]}"'
app/backend/export.py:699:        out.append(f"- {_cap(v.cite(e['record_no']))}: " + "; ".join(bits or ["edited"]) + "." + tail)
app/backend/export.py:707:            out.append(f'- Entry, {v.cite(e["record_no"])}: "{e["summary"]}" ({_edit_unconfirmed_phrase(e)})')
app/backend/export.py:709:            out.append(f'- Entry, {v.cite(e["record_no"])}: summary not shown, a code check on it fails (edit it to match the quote, or dismiss it)')
app/backend/export.py:711:            out.append(f'- Entry, {v.cite(e["record_no"])}: "{e["summary"]}"' + (" [entered by reviewer]" if e.get("entered_by_reviewer") else ""))
app/backend/export.py:714:            out.append(f'- Amount {_money_short(a.get("cents"), a.get("raw", ""))} ({a["cls"]}), {v.cite(a["record_no"])}: '
app/backend/billing.py:39:    "NO_DATE_OF_SERVICE": "Charges on this statement carry no date of service; they are counted as stated but cannot be tied to a visit.",
app/backend/billing.py:922:        if form == "ledger_table":                       # a statement's fee-schedule line is a rate and carries no date of service
app/backend/present.py:91:    """In a document with no header the record's date stands in for a date of service; a line that states no date of its own then has none (dos None) for the duplicate match."""
app/backend/count_charge.py:4:provider's bill, a second figure on a line ...): never countable. (b) Held back only because the line lacks something D-060 needs (no date of service, a document with no
app/backend/narrative.py:44:    return [dict(e, label=v.source(e["record_no"]), date_iso=v.date_of(e), cite=v.cite(e["record_no"])) for e in v.in_entries]
app/backend/narrative.py:107:        # the date of service lives in the record header, not the quote: give the judge the header it may rely on
app/backend/narrative.py:108:        verdict, jcall, jcode = judges.run_j1_meta(text, e["excerpt"], f"{e['label']} (date of service {export._long_date(e['date_iso'])})",
app/backend/service_date.py:4:A charge line takes its date of service from EXACTLY TWO sources:
app/backend/service_date.py:5:  (1) its own row's date cell in a REAL bill table: a header row of short labels (two or more) that names the date of service as a whole cell (DOS, date of service, service date, visit date, 24A ...),
app/backend/service_date.py:12:'date of service [__________] (statement dated X)' on a bill, '(record dated X)' on any other record, and the Step 3 note; the paralegal fills it from the quote. The result of `resolve` is one of:
app/backend/service_date.py:93:WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)
app/backend/service_date.py:111:BLANK = "date of service [__________]"
app/backend/service_date.py:119:def not_stated_text(statement_iso, kind: str = "bill") -> str:
app/backend/service_date.py:121:    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)' on a bill, '(record dated June 15, 2026)' on any other record."""
app/backend/service_date.py:127:def printed_text(res: dict, statement_iso, kind: str = "bill") -> str:
app/backend/service_date.py:129:    return not_stated_text(statement_iso, kind)
app/backend/service_date.py:133:    "ambiguous_numeric": "The date of service column of the bill reads {raw}, which can be read as month/day or day/month; the record does not settle which.",
app/backend/service_date.py:134:    "two_digit_year": "The date of service column of the bill reads {raw}, which has a two-digit year; the code does not guess the century.",
app/backend/service_date.py:135:    "no_year": "The date of service column of the bill reads {raw}, which states no year; the code does not borrow one from the statement.",
app/backend/service_date.py:136:    "invalid": "The date of service column of the bill reads {raw}, which is not a complete date on the calendar.",
app/backend/service_date.py:137:    "several_dates": "The date of service column of the bill holds more than one date ({raw}) and nothing says which one belongs to this charge.",
app/backend/service_date.py:138:    "implausible": "The date of service column of the bill reads {raw}, but that date is after the statement it appears on or years before it.",
app/backend/service_date.py:139:    "non_service_date": "The line shows {raw}, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of ser
app/backend/service_date.py:140:    "no_date": "The letter does not take a date of service from the records.",
app/backend/service_date.py:141:    "not_read": "The letter does not take a date of service from the records.",
app/backend/service_date.py:143:_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
app/backend/service_date.py:144:_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated itemized bill, and fill the b
app/backend/service_date.py:293:    with no digit (data rows and 'Date of service: X' lines in between are skipped), two or more cells, every one a short label, at least one naming the date of service as a whole cell
app/backend/service_date.py:432:    if pairs:                                                              # source (1): the date cell of its own row, under a heading cell of a real table that names the date of service
app/backend/store.py:120:    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or the fillable blank 'date of service [__________] (statement dated June 15, 
app/backend/store.py:122:    A date has exactly two sources (service_date.resolve): the date cell of the line's own row under a bill-table heading that names the date of service (a CMS-1500 24A From/To pair or a
app/backend/store.py:126:    counted for a missing date of service (D-064) is not stated, with no note (she counted it knowing). Code only."""
app/backend/store.py:143:            "text": SD.display(r["first"], r["last"]) if stated else SD.printed_text(r, rd, kind),
app/backend/store.py:148:    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
----
 app/backend/export.py       | 2 +-
 app/backend/service_date.py | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
43ce6eb fix(backend): gate M3+M4 fix A part 2, no_date note no longer says the code reads dates; README reviews pointer
aa21b24 fix(backend): gate M3+M4 fix A, spec/api/LLM_VS_CODE/README match the D-073 blank; undated-charge notes section before BILLS TO REQUEST
----
70:| D-062 | The letter total states what it is (2026-11-02, T-140 after 3 adversarial rounds). R-EX-8's line becomes `Billed charges accepted from these records: $X`, where X sums the charges the paralegal accepted one at a time, each listed above with its so
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:04:19.681Z

**tool call — Bash**
````
{
 "command": "head -12 artifacts/review-evidence/T-202-paralegal-r6/eval_teeth_r6.py | cut -c1-250; git diff f6d5c19 a932fc9 -- app/backend/export.py app/backend/service_date.py | grep \"^[-+]\" | cut -c1-200",
 "description": "Read the r6 teeth script usage and the diff since the gate pin"
}
````

### User / tool · 2026-11-03T15:04:19.784Z

**tool result**
````
"""T-202 r6 paralegal: (1) evals.letter_check.charge_date_violations on the line the 9655f1d build prints vs the blank and the true date, for the round 6 wrong-date shapes
(SYNTHETIC); (2) the blank's label ('record dated' vs 'statement dated') on clinical records whose label or excerpt opening holds a money word, via store.charge_service_date.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r6/eval_teeth_r6.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
from evals import letter_check as LC  # noqa: E402
from app.backend import amounts as AM, store, service_date as SD  # noqa: E402
--- a/app/backend/export.py
+++ b/app/backend/export.py
-        "BILLS TO REQUEST (entry in the letter, no accepted charge)", *_bills(v), "",
+        "BILLS TO REQUEST (entry in the letter, no accepted charge)", *_bills(v), "",
--- a/app/backend/service_date.py
+++ b/app/backend/service_date.py
-    "no_date": "The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note).",
+    "no_date": "The letter does not take a date of service from the records.",
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:04:21.901Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r6/eval_teeth_r6.py artifacts/review-evidence/T-202-paralegal-r7/archive > artifacts/review-evidence/T-202-paralegal-r7/eval_teeth_r6_at_a932fc9.out 2>&1; echo EXIT=$?; cut -c1-300 artifacts/review-evidence/T-202-paralegal-r7/eval_teeth_r6_at_a932fc9.out | head -60",
 "description": "Rerun the round-6 label and teeth script on the HEAD archive"
}
````

### User / tool · 2026-11-03T15:04:22.224Z

**tool result**
````
EXIT=0
# (1) letter_check on the build's line vs the alternatives
== A2 PT note 03/06, initial evaluation charge
   build  'Capital PT, physical therapy note, March 6, 2026: $250.00' -> ["charge line does not print the blank date of service in its exact form (source label, then 'date of service [__________]', then the record's date called 'statement' on a bill and 'record' otherwise): Capital PT, physical ther
   alt    'Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $250.00' -> []
   alt    'Capital PT, physical therapy note, January 23, 2026: $250.00' -> ["charge line does not print the blank date of service in its exact form (source label, then 'date of service [__________]', then the record's date called 'statement' on a bill and 'record' otherwise): Capital PT, physical t
== A5 late entry 01/20 for the 01/16 visit
   build  'Dr. Alvarez, office visit note, January 20, 2026: $150.00' -> ["charge line does not print the blank date of service in its exact form (source label, then 'date of service [__________]', then the record's date called 'statement' on a bill and 'record' otherwise): Dr. Alvarez, office visit
   alt    'Dr. Alvarez, office visit note, date of service [__________] (record dated January 20, 2026): $150.00' -> []
   alt    'Dr. Alvarez, office visit note, January 16, 2026: $150.00' -> ["charge line does not print the blank date of service in its exact form (source label, then 'date of service [__________]', then the record's date called 'statement' on a bill and 'record' otherwise): Dr. Alvarez, office visit
== A6b ER discharge summary dated 01/10, arrived 01/09
   build  'Central ER discharge summary, January 10, 2026: $6,240.00' -> ["charge line does not print the blank date of service in its exact form (source label, then 'date of service [__________]', then the record's date called 'statement' on a bill and 'record' otherwise): Central ER discharge summ
   alt    'Central ER discharge summary, date of service [__________] (record dated January 10, 2026): $6,240.00' -> []
   alt    'Central ER discharge summary, January 9–10, 2026: $6,240.00' -> ["charge line does not print the blank date of service in its exact form (source label, then 'date of service [__________]', then the record's date called 'statement' on a bill and 'record' otherwise): Central ER discharge 
== A10 PCP note 01/16, urgent care yesterday
   build  'Dr. Alvarez, office visit note, January 16, 2026: $310.00' -> ["charge line does not print the blank date of service in its exact form (source label, then 'date of service [__________]', then the record's date called 'statement' on a bill and 'record' otherwise): Dr. Alvarez, office visit
   alt    'Dr. Alvarez, office visit note, date of service [__________] (record dated January 16, 2026): $310.00' -> []
   alt    'Dr. Alvarez, office visit note, January 15, 2026: $310.00' -> ["charge line does not print the blank date of service in its exact form (source label, then 'date of service [__________]', then the record's date called 'statement' on a bill and 'record' otherwise): Dr. Alvarez, office visit
# (2) the blank's label by record
== L1 ER discharge summary that opens 'ER charges:': kind=bill $6,240 -> 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026)'
== L2 office visit note that opens with a copay: kind=bill $40 -> 'Dr. Alvarez, office visit note, date of service [__________] (statement dated January 16, 2026)'
== L2 office visit note that opens with a copay: kind=bill $150.00 -> 'Dr. Alvarez, office visit note, date of service [__________] (statement dated January 16, 2026)'
== L3 PT note that opens with a payment plan: kind=bill $185.00 -> 'Capital PT, physical therapy note, date of service [__________] (statement dated March 6, 2026)'
== L4 ER record whose label carries an account number: kind=bill $6,240.00 -> 'Central ER, emergency department record, account 4471, date of service [__________] (statement dated January 9, 2026)'
== L5 urgent care (no doc type) that opens 'Charges:': kind=bill $310.00 -> 'Quillfeather Urgent Care, date of service [__________] (statement dated February 3, 2026)'
== L6 control: billing statement: kind=bill $275.00 -> 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026)'
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:04:27.783Z

**tool call — Bash**
````
{
 "command": "grep -n \"L1\\|L2\\|L3\\|L4\" artifacts/review-evidence/T-202-paralegal-r6/eval_teeth_r6.py | cut -c1-400 | head -12; echo ----; grep -n -A3 \"Central ER discharge summary\" evals/golden/sample.txt | cut -c1-300",
 "description": "Show the r6 label probe inputs and the sample ER record text"
}
````

### User / tool · 2026-11-03T15:04:27.879Z

**tool result**
````
46:    ("L1 ER discharge summary that opens 'ER charges:'", "Central ER discharge summary", "2026-01-09", "ER charges: $6,240. Dx: cervical strain. CT head negative."),
47:    ("L2 office visit note that opens with a copay", OVN, "2026-01-16", "Copay collected $40. Persistent neck pain 6/10. Office visit 99213 charge $150.00."),
48:    ("L3 PT note that opens with a payment plan", PTN, "2026-03-06", "Payment plan discussed. Discharged from PT. Therapeutic exercise 97110 charge $185.00."),
49:    ("L4 ER record whose label carries an account number", "Central ER, emergency department record, account 4471", "2026-01-09", "Dx: cervical strain. ER facility charge $6,240.00."),
----
10:Source: Central ER discharge summary
11-Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."
12-
13-=== Record 3 ===
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:04:56.748Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/label_repro_r7.py",
 "content": "\"\"\"T-202 r7: round-6 major (D-073 rule 4) through the FULL pipeline at HEAD. SYNTHETIC variants of the sample:\n  V1: the ER record's excerpt opens with its money sentence ('ER charges: $6,240. Dx: ...'); the record is a discharge summary, not a statement.\n  V2: the PT visit-9 excerpt opens 'Payment plan discussed.' and carries its own charge sentence.\nExpected by D-073 rule 4: '(record dated X)' on both. Prints each charge line and letter_check's verdict.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/label_repro_r7.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nos.environ.setdefault(\"LLM_BACKEND\", \"fixture\")\nos.environ.setdefault(\"FIXTURE_SET\", \"curated\")\nimport logging  # noqa: E402\nlogging.disable(logging.CRITICAL)\nfrom evals import letter_check as LC  # noqa: E402\n\nSAMPLE = open(\"evals/golden/sample.txt\", encoding=\"utf-8\").read()\nER_OLD = \"Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.\"\nER_NEW = \"ER charges: $6,240. Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.\"\nPT_OLD = \"Discharged from PT after two missed appointments. Pain 3/10.\"\nPT_NEW = \"Payment plan discussed. Discharged from PT. Discharge visit 97110 charge $185.00.\"\nassert SAMPLE.count(ER_OLD) == 1, \"ER excerpt not found once\"\nassert SAMPLE.count(PT_OLD) == 1, \"PT excerpt not found once\"\nVARIANTS = {\n    \"V1_er_summary_opens_with_charges\": SAMPLE.replace(ER_OLD, ER_NEW),\n    \"V2_pt_note_opens_payment_plan\": SAMPLE.replace(PT_OLD, PT_NEW),\n}\nfor name, text in VARIANTS.items():\n    got = LC.letters_for(text)\n    v = got[\"all_accepted\"]\n    letter = v[\"letters\"][\"standard\"]\n    print(f\"== {name}: accepted charge cents={v['charge_cents']}\")\n    for head, quote in LC.charge_lines(letter):\n        print(\"   \", head, \"| quote:\", quote)\n    print(\"    letter_check.charge_date_violations:\", LC.charge_date_violations(letter, v[\"records\"]))\n"
}
````

### User / tool · 2026-11-03T15:04:56.851Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/label_repro_r7.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:04:59.406Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/label_repro_r7.py artifacts/review-evidence/T-202-paralegal-r7/archive > artifacts/review-evidence/T-202-paralegal-r7/label_repro_r7.out 2>&1; echo EXIT=$?; cut -c1-400 artifacts/review-evidence/T-202-paralegal-r7/label_repro_r7.out",
 "description": "Reproduce the D-073 rule 4 label mislabel through the full pipeline at HEAD"
}
````

### User / tool · 2026-11-03T15:05:00.675Z

**tool result**
````
EXIT=0
== V1_er_summary_opens_with_charges: accepted charge cents=[624000, 215000]
    Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240.00 | quote: ER charges: $6,240.
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | quote: Charge: $2,150.
    letter_check.charge_date_violations: []
== V2_pt_note_opens_payment_plan: accepted charge cents=[624000, 18500, 215000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | quote: ER charges: $6,240.
    Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $185.00 | quote: Discharge visit 97110 charge $185.00.
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | quote: Charge: $2,150.
    letter_check.charge_date_violations: []
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:05:22.785Z

**tool call — Bash**
````
{
 "command": "lsof -iTCP:7987 -sTCP:LISTEN -nP; kill 84772; sleep 2; lsof -iTCP:7987 -sTCP:LISTEN -nP; echo \"lsof_exit=$?\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7987/api/health; cd artifacts/review-evidence/T-202-paralegal-r7/archive && grep -n \"def record_kind\\|if AM.billing_document\\|def date_label\\|def not_stated_text\\|def resolve\\|def read\" app/backend/service_date.py; grep -n \"def charge_when\\|return f\\\"{self.source(n)}, {service_date\" app/backend/export.py; grep -n \"fill it from the quote\" app/backend/export.py | cut -c1-80; grep -n \"def _record_kind\\|def charge_date_violations\\|if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES\\[\\\"financial\\\"\\])\\|def charge_lines\" evals/letter_check.py; grep -n \"_OPEN\\|opening_chars\" app/backend/service_date.py | head -3",
 "description": "Stop the HEAD server by PID and collect exact file line references"
}
````

### User / tool · 2026-11-03T15:05:25.089Z

**tool result**
````
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  84772 arsis    9u  IPv4 0xdc43e402f1188e33      0t0  TCP 127.0.0.1:7987 (LISTEN)
lsof_exit=1
000
46:def record_kind(source, excerpt: str = "") -> str:
52:    if AM.billing_document(src, excerpt or "") or _hit(_FIN, src) or _hit(_FIN, opening):
114:def date_label(kind: str) -> str:
119:def not_stated_text(statement_iso, kind: str = "bill") -> str:
406:def resolve(excerpt: str, start: int, source, date_iso) -> dict:
416:def read(excerpt: str, start: int, source, date_iso) -> dict:
210:    def charge_when(self, a):
215:        return f"{self.source(n)}, {service_date.not_stated_text(self.rec_date(n), service_date.record_kind(self.source(n), self.text(n)))}"
602:        out.append(f"- {_provider(v.source(a['record_no'])) or v.source(a['r
176:def charge_lines(letter: str) -> list:
201:def _record_kind(source, excerpt=""):
206:    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["financial"]):
213:def charge_date_violations(letter: str, records) -> list:
39:_OPEN = int(_TYPES["opening_chars"])
51:    src, opening = source or "", re.split(r"[:.\n]", (excerpt or "")[:_OPEN])[0]
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:06:13.927Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/jsoncheck_r7.py",
 "content": "\"\"\"Checks a review file: exactly one fenced json block, parses, required keys present, verdict follows the rule (any blocker -> fail; else any major -> changes; else pass).\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/jsoncheck_r7.py <review.md>\n\"\"\"\nimport json\nimport sys\n\nFENCE = \"`\" * 3\ntext = open(sys.argv[1], encoding=\"utf-8\").read()\nblocks = []\nlines = text.splitlines()\ni = 0\nwhile i < len(lines):\n    if lines[i].strip() == FENCE + \"json\":\n        j = i + 1\n        body = []\n        while j < len(lines) and lines[j].strip() != FENCE:\n            body.append(lines[j])\n            j += 1\n        blocks.append(\"\\n\".join(body))\n        i = j\n    i += 1\nassert len(blocks) == 1, f\"expected exactly one json block, found {len(blocks)}\"\nd = json.loads(blocks[0])\nfor k in (\"card\", \"persona\", \"model\", \"scope\", \"exercised\", \"verdict\", \"scores\", \"findings\", \"whats_right\", \"questions_for_chris\"):\n    assert k in d, f\"missing {k}\"\nassert \"verify_quickly\" in d[\"scores\"], \"scores.verify_quickly missing\"\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nfor f in d[\"findings\"]:\n    for k in (\"severity\", \"title\", \"evidence\", \"why_it_matters\", \"fix\", \"acceptance_test\"):\n        assert f.get(k), f\"finding missing {k}: {f.get('title')}\"\n    assert f[\"severity\"] in (\"blocker\", \"major\", \"minor\", \"nit\")\nwant = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nassert d[\"verdict\"] == want, f\"verdict {d['verdict']} but rule gives {want}\"\nassert len(d[\"whats_right\"]) <= 3\nfor s in d[\"scores\"].values():\n    assert 1 <= s <= 5\nprint(\"ok\", d[\"verdict\"], {k: sev.count(k) for k in (\"blocker\", \"major\", \"minor\", \"nit\")}, \"model\", d[\"model\"])\n"
}
````

### User / tool · 2026-11-03T15:06:14.028Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/jsoncheck_r7.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:06:16.963Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git rev-parse a932fc9^{tree} && grep -n \"^- 2026-11-03T1[3-9]\" /Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/b311qgbfb.txt | wc -l && ls artifacts/review-evidence/T-202-paralegal-r7/ && grep -c \"\" artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.out",
 "description": "Confirm HEAD and tree hash still match the pin and list evidence files"
}
````

### User / tool · 2026-11-03T15:06:17.101Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:06:19.473Z

**tool call — Bash**
````
{
 "command": "git log --oneline a932fc9..HEAD && git diff --stat a932fc9 HEAD -- app/backend app/llm app/frontend evals/letter_check.py evals/golden tests | tail -5; echo \"---paths-changed:\"; git diff --name-only a932fc9 HEAD | head -40",
 "description": "Check what changed between the pinned commit and the moved HEAD"
}
````

### User / tool · 2026-11-03T15:06:19.612Z

**tool result**
````
be257c9 docs(release): drop OWNER placeholder clone step from README (T-212)
---paths-changed:
README.md
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:07:18.109Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md",
 "content": "# T-202 round 7 (D-073 all-blank fallback, b50952d): paralegal review (Maria Delgado, senior PI paralegal)\n\n**Verdict: fail.** The round-6 wrong-date blockers are closed at HEAD. No charge line prints a service date, and the UB-04 period and the visit-note dates can no longer reach the letter. One blocker remains: a clinical record's charge line is labelled \"statement dated\" when its excerpt opens with a money word. That breaks D-073 rule (4). I re-rate the round-6 major for that defect to blocker (finding 1 gives the reason). letter_check's value of 0 does not catch it, because the eval reads the record kind with the same rule.\n\n**Pin.** `git archive a932fc9` (tree 5f74b737), extracted to `artifacts/review-evidence/T-202-paralegal-r7/archive`. HEAD moved to be257c9 during the review. That commit changes README.md only, and the diff of app/backend, app/llm, app/frontend, evals and tests is empty between the two, so the results apply to be257c9 too.\n\n**What I checked, in brief.**\n- Charge lines: 19 in-process (sample, case_09, lib10, lib11; accepted-all and counted variants) and 8 live over HTTP. Every line is `<source>, date of service [__________] (statement|record dated <Month D, YYYY>)` with no other date on it. Each parenthetical date equals the record's own Date line in the input (check_letters_r7.out, live_summary.out).\n- `python -m evals.letter_check` equivalent, run with -I against the archive: value 0, 25 cases, exit 0 (letter_check.out).\n- Round-6 shapes (fullpipe_r6.py, run on the archive): every shape prints the blank and date violations are empty. The visit-note dates (initial evaluation, late entry, yesterday, ER charge in a PCP note, course total, collision day) and the UB-04 period override (u1) no longer print a date of service. Structurally, `service_date.resolve` never returns a stated date (service_date.py:406-413) and `export.charge_when` has no date path (export.py:210-215).\n- Teeth: a printed \"date of service March 6, 2026\" and a wrong record date are both rejected in all four cases (8 of 8 mutants).\n\n**Severity re-rate.** Round 6 rated the label defect (finding 1) major. The calibration rates a violation of a spec line as a blocker, and D-073 rule (4) is a spec line. The round-6 reason, that no corpus line is affected, is an impact argument and does not lower the class.\n\n**Verify-quickly score (3).** Each amount and each quote checks in one step. The date of service, though, is a manual lookup on every charge line, because 7 of the 8 live quotes carry no date. The record-kind word cannot be trusted without opening the record (finding 1).\n\n**Model.** This review ran on claude-haiku-5-5, the model I am running as. CLAUDE.md section 6 and my dossier expect claude-opus-5-5 for judgment reviews. See questions_for_chris.\n\n**Not exercised (outside this brief).** Timeline entries, the review screen and keyboard path, Step 3 UI text, and the 25-case corpus label count (round-6 corpus_blanks.py was not re-run). The gate review GATE-M3M4-paralegal.md was pinned at f6d5c19. It did not test the label shapes in finding 1, and it was signed claude-sonnet-5-5, so I did not rely on it for this card.\n\n```json\n{\"card\": \"T-202\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git archive a932fc9 (tree 5f74b7377e5fd55b9be2beb47090b9b0dfbc812d) extracted to artifacts/review-evidence/T-202-paralegal-r7/archive; HEAD moved to be257c9 (README.md only) during the review, and the app/backend, app/llm, app/frontend, evals and tests diff is empty; app served from that archive at http://127.0.0.1:7987 (ZLAYT_MODE=local, LLM_BACKEND=fixture, FIXTURE_SET=curated; /api/health demo_mode true, local_mode true), stopped by PID 84772 (lsof exit 1, curl 000). Cases: sample, case_09, lib10, lib11 (SYNTHETIC inputs from evals/golden and evals/library). Evidence: artifacts/review-evidence/T-202-paralegal-r7/.\",\n \"exercised\": [\n  \"Read personas/paralegal.md (live dossier), reviews/T-202-paralegal-r6.md (blockers, majors, minors), reviews/GATE-M3M4-paralegal.md, board.py show T-202 (round-6 findings and round-7 notes), memory/ORCHESTRATOR_DECISIONS.md:97-104 (D-073, rounds 6 rules and fallback)\",\n  \"git rev-parse HEAD: a932fc9 at the start, be257c9 at the end; git log --oneline a932fc9..HEAD: be257c9 docs(release) only; git diff --name-only a932fc9 HEAD: README.md; git diff --stat a932fc9 HEAD -- app/backend app/llm app/frontend evals tests: empty; git merge-base --is-ancestor b50952d HEAD: ancestor; git diff f6d5c19 a932fc9 -- app/backend/export.py app/backend/service_date.py: notes wording only\",\n  \"git archive a932fc9 | tar -x into artifacts/review-evidence/T-202-paralegal-r7/archive (tree 5f74b7377e5fd55b9be2beb47090b9b0dfbc812d)\",\n  \"run_letter_check_r7.py (python -m evals.letter_check, run with .venv/bin/python -I against the archive): {\\\"value\\\": 0, \\\"cases\\\": 25, \\\"held_out_entries\\\": 11, \\\"backend\\\": \\\"fixture\\\"}, exit 0 (letter_check.out)\",\n  \"check_letters_r7.py on the archive: sample, case_09, lib10, lib11 through evals.letter_check.letters_for (accepted-all and counted): 19 charge lines, each exact form, parenthetical date equal to the input Date header, kind and source as written; problems 0; 8 teeth mutants (printed DOS, wrong record date) all rejected (check_letters_r7.out)\",\n  \"serve_r7.py on 127.0.0.1:7987 from the archive; live_letters_r7.py over HTTP (POST /api/cases, POST run, GET status, accept every pending entry, amount and flag, GET export) for sample, case_09, lib10, lib11: 8 charge lines, all exact; totals $8,390.00, $275.00, $8,123.50, $3,260.00 (live_summary.out, live/*-letter.txt, live/sample-case.json). lib11 ledger items (10 refused, count confirm needed) not counted over HTTP; the counted variant in check_letters_r7.out covers them in-process\",\n  \"fullpipe_r6.py on the archive (the round-5 and round-6 shapes, through the full pipeline and letter_check; A1-A20, U1, M1-M2, C1-C4, T1-T5b): fullpipe_r6_shapes_at_a932fc9.out; every charge line prints the blank; date violations [] on each shape\",\n  \"eval_teeth_r6.py on the archive: eval_teeth_r6_at_a932fc9.out (part 1: build line rejected and blank accepted for A2, A5, A6b, A10; part 2: L1-L4 print 'statement dated' on clinical records)\",\n  \"label_repro_r7.py (SYNTHETIC variants through letters_for: V1 ER summary whose excerpt opens 'ER charges:', V2 PT visit whose excerpt opens 'Payment plan discussed'): label_repro_r7.out\",\n  \"jsoncheck_r7.py on this review (one json block, keys, verdict rule) before publishing\",\n  \"Not exercised: timeline entries, review screen and keyboard path, Step 3 UI, the 25-case corpus label count (corpus_blanks.py not re-run)\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 3, \"letter_dates_correct\": 5, \"adversarial_dates_correct\": 5, \"blank_label_correct\": 2},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"D-073 rule (4) broken: a clinical record's charge line says 'statement dated' when its excerpt opens with a money word (round-6 major, re-rated to blocker)\",\n   \"evidence\": \"label_repro_r7.out, V1: 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240.00 | quote: ER charges: $6,240.' V2: 'Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $185.00 | quote: Discharge visit 97110 charge $185.00.' Both: letter_check.charge_date_violations returns []. Cause: service_date.py:51-52 takes the excerpt's first 40 characters (cut at the first colon or full stop) and returns 'bill' when they hold a financial word (_hit(_FIN, opening)) before the document-type phrase in the source label is read. letter_check.py:206 repeats the same rule, so the eval agrees with the wrong label. eval_teeth_r6_at_a932fc9.out part 2: 'L1 ... -> (statement dated January 9, 2026)', 'L2 office visit note ... (statement dated January 16, 2026)', 'L3 PT note ... (statement dated March 6, 2026)', 'L4 ER record ... account 4471 ... (statement dated January 9, 2026)'. Rule: memory/ORCHESTRATOR_DECISIONS.md:100, D-073 round-6 rule (4): 'a blank on a non-bill record reads \\\"(record dated X)\\\", on a bill \\\"(statement dated X)\\\".' The sample is not affected: its ER excerpt opens 'Dx:' (evals/golden/sample.txt:11) and prints '(record dated January 9, 2026)' (live/sample-letter.txt:41).\",\n   \"why_it_matters\": \"The letter tells the adjuster that an ER discharge summary and a PT visit note are statements. The adjuster will ask for a statement that does not exist, and the paralegal gets a document type the record does not state. The date beside it is the record's own date, so no date is invented, but the document type is. This violates a binding spec line, and the calibration rates that as a blocker. Round 6 rated it major because no corpus line is affected; that argues about impact and does not change the class. The eval also cannot catch it (V1 and V2 pass letter_check), so the harness has a blind spot on the same rule.\",\n   \"fix\": \"service_date.record_kind (service_date.py:46-56): a whole document-type phrase in the source label (the encounter list in encounter_types.json) decides first; the excerpt opening decides only when the label has no document-type phrase, and a financial word in the label alone makes a bill only when the label names no document type. letter_check._record_kind (letter_check.py:201-210) must read the rule from the table on its own terms, not reuse the same opening test, so the eval can disagree with the app.\",\n   \"acceptance_test\": \"label_repro_r7.py V1 prints '(record dated January 9, 2026)' and V2 prints '(record dated March 6, 2026)'; eval_teeth_r6.py L1-L4 print 'record dated'; L5 (no document type, opens 'Charges:') and L6 (billing statement) keep 'statement dated'; a test in tests/ shows letter_check.charge_date_violations rejecting 'statement dated' on a discharge summary line and on a visit-note line.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from rounds 3-6 (still open): the internal notes say 'fill it from the quote' when the quote holds no date\",\n   \"evidence\": \"fullpipe_r6_shapes_at_a932fc9.out, notes line for the sample ER charge: '- Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.' The quote it points to is 'ER charges: $6,240.' (live/sample-letter.txt:42). The sentence is built at export.py:602; the Step 3 sentence for the same reason is service_date.py:144 (_ASK_NONE): 'Take the date from the matching visit note, or request a dated itemized bill'.\",\n   \"why_it_matters\": \"For the sample's charges the quote holds no date, so the notes tell the paralegal to fill a date the quote cannot give, while Step 3 tells her to take it from the visit note. Two instructions for one blank.\",\n   \"fix\": \"The notes use the Step 3 sentence (service_date._ASK_NONE) for the no-date reasons, and the words 'from the quote' stay only for the written-date reasons.\",\n   \"acceptance_test\": \"No notes line says 'fill it from the quote' when the quote holds no date: for the sample and lib10 charges, grep of the notes for 'from the quote' finds nothing.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from round 6 (still open): a 14-visit charge gets a single-date blank\",\n   \"evidence\": \"check_letters_r7.out, lib11 counted: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $2,310.00 | quote: treatment visits 1 through 14 charge $2,310.00'. The singular form is pinned by charge_date_violations (letter_check.py:213 onward).\",\n   \"why_it_matters\": \"One date blank over 14 visits asks the paralegal for one date for a range, and the quote gives none. The exact-form rule makes this a spec decision, not a code fix.\",\n   \"fix\": \"Decide in the spec: either allow 'dates of service [__________]' for a quote that counts visits (D-073 and letter_check's exact form change together), or keep the singular and say in the notes that the line covers 14 visits.\",\n   \"acceptance_test\": \"The lib11 $2,310.00 line prints the plural form, or its notes line says it covers 14 visits; the chosen form is recorded in D-073 and letter_check accepts only that form.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"New: a record date is printed beside a charge that the same note dates elsewhere\",\n   \"evidence\": \"fullpipe_r6_shapes_at_a932fc9.out, a5: 'Dr. Alvarez, office visit note, date of service [__________] (record dated January 20, 2026): $150.00 | Office visit 99213 charge $150.' (the same note's sentence reads 'Late entry for the visit of 01/16/2026.'). a2: 'Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $250.00 | Initial evaluation 97161 charge $250.' (record 4 dates the initial evaluation 2026-01-23).\",\n   \"why_it_matters\": \"The blank is correct and the record date is true. The printed date still sits beside a charge the record dates elsewhere. The round-6 brief says the paralegal fills blanks from the date printed next to them, which is how a wrong date gets into the demand. No excerpt makes it false, so this is minor, not a blocker.\",\n   \"fix\": \"Open question for the orchestrator (questions_for_chris 2): withhold the parenthetical when the charge's own sentence carries a time word (the round-6 rule (3) guard words), so a printed date appears only beside charges the record dates by its own header.\",\n   \"acceptance_test\": \"The chosen form is recorded in D-073, and a probe with 'Late entry for the visit of 01/16/2026. Office visit 99213 charge $150.00.' prints the chosen form in both the letter and the eval.\"}\n ],\n \"whats_right\": [\n  \"No service date is printed on any charge line at HEAD: 19 in-process and 8 live charge lines are the exact blank, the round-6 visit-note and UB-04 shapes print the blank, and letter_check reports 0 over 25 cases (letter_check.out, fullpipe_r6_shapes_at_a932fc9.out).\",\n  \"Each parenthetical date equals the record's own Date line in the input, and the totals match the accepted charges: $8,390.00, $275.00, $8,123.50 (check_letters_r7.out, live_summary.out).\",\n  \"The teeth check works: a printed service date and a wrong record date are rejected in all four cases (check_letters_r7.out, TEETH lines).\"\n ],\n \"questions_for_chris\": [\n  \"Model: this review ran on claude-haiku-5-5 (the model I am running as). CLAUDE.md section 6 and the dossier expect claude-opus-5-5 for judgment reviews. Should T-202 get an Opus re-run before it counts? The same question applies to reviews/GATE-M3M4-paralegal.md, which is signed claude-sonnet-5-5 and pinned f6d5c19, before aa21b24 and 43ce6eb.\",\n  \"Finding 4: should the record date be withheld beside a charge whose own sentence dates it elsewhere (late entry, initial evaluation, 'yesterday'), or does D-073 require it on every charge line?\",\n  \"Finding 3: keep the singular 'date of service' over a 14-visit quote, or allow 'dates of service [__________]' for count quotes?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-03T15:07:18.206Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:07:23.990Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md",
 "old_string": "- Round-6 shapes (fullpipe_r6.py, run on the archive): every shape prints the blank and date violations are empty.",
 "new_string": "- Round-6 shapes (fullpipe_r6.py, run on the archive): every charge line in those shapes prints the blank, and date violations are empty on each. Shapes that are not accepted as charges print no charge line."
}
````

### User / tool · 2026-11-03T15:07:24.100Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:07:26.805Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md",
 "old_string": "  \"fullpipe_r6.py on the archive (the round-5 and round-6 shapes, through the full pipeline and letter_check; A1-A20, U1, M1-M2, C1-C4, T1-T5b): fullpipe_r6_shapes_at_a932fc9.out; every charge line prints the blank; date violations [] on each shape\",",
 "new_string": "  \"fullpipe_r6.py on the archive (the round-5 and round-6 shapes in that file: visit-note A-shapes, UB-04 U-shape, provider-name M and C shapes, key-value and table T shapes; through the full pipeline and letter_check): fullpipe_r6_shapes_at_a932fc9.out; every charge line prints the blank; date violations [] on each shape; shapes not accepted as charges print no charge line\","
}
````

### User / tool · 2026-11-03T15:07:26.920Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:07:36.166Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md",
 "old_string": "git diff f6d5c19 a932fc9 -- app/backend/export.py app/backend/service_date.py: notes wording only\",",
 "new_string": "git diff f6d5c19 a932fc9 -- app/backend/export.py app/backend/service_date.py: two changed lines, one of them the service_date.py no_date reason text; no charge-line logic changed since the gate pin\","
}
````

### User / tool · 2026-11-03T15:07:36.268Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:07:40.316Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/jsoncheck_r7.py artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md; echo EXIT=$?; grep -n \"statement dated January 9, 2026): \\$6,240.00\\|statement dated March 6, 2026): \\$185.00\\|record dated January 20, 2026): \\$150.00\\|record dated March 6, 2026): \\$250.00\\|statement dated June 15, 2026): \\$2,310.00\" artifacts/review-evidence/T-202-paralegal-r7/label_repro_r7.out artifacts/review-evidence/T-202-paralegal-r7/fullpipe_r6_shapes_at_a932fc9.out artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.out | cut -c1-260; grep -n \"dated\" artifacts/review-evidence/T-202-paralegal-r7/eval_teeth_r6_at_a932fc9.out | grep \"^.*L[1-4] \" | cut -c1-200; sed -n '41,42p' artifacts/review-evidence/T-202-paralegal-r7/live/sample-letter.txt | cut -c1-200",
 "description": "Run the JSON check on the draft and proofread the quoted lines against outputs"
}
````

### User / tool · 2026-11-03T15:07:40.460Z

**tool result**
````
ok fail {'blocker': 1, 'major': 0, 'minor': 3, 'nit': 0} model claude-haiku-5-5
EXIT=0
19:== L1 ER discharge summary that opens 'ER charges:': kind=bill $6,240 -> 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026)'
20:== L2 office visit note that opens with a copay: kind=bill $40 -> 'Dr. Alvarez, office visit note, date of service [__________] (statement dated January 16, 2026)'
21:== L2 office visit note that opens with a copay: kind=bill $150.00 -> 'Dr. Alvarez, office visit note, date of service [__________] (statement dated January 16, 2026)'
22:== L3 PT note that opens with a payment plan: kind=bill $185.00 -> 'Capital PT, physical therapy note, date of service [__________] (statement dated March 6, 2026)'
23:== L4 ER record whose label carries an account number: kind=bill $6,240.00 -> 'Central ER, emergency department record, account 4471, date of service [__________] (statement dated January 9, 2026)'
Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240."
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:07:45.652Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7 && grep -F -c \"(statement dated January 9, 2026): \\$6,240.00\" label_repro_r7.out; grep -F -c \"(statement dated March 6, 2026): \\$185.00\" label_repro_r7.out; grep -F -c \"(record dated January 20, 2026): \\$150.00\" fullpipe_r6_shapes_at_a932fc9.out; grep -F -c \"(record dated March 6, 2026): \\$250.00\" fullpipe_r6_shapes_at_a932fc9.out; grep -F -c \"(statement dated June 15, 2026): \\$2,310.00\" check_letters_r7.out; grep -F -c \"Late entry for the visit of 01/16/2026\" fullpipe_r6_shapes_at_a932fc9.out; grep -F -c \"Dx: cervical strain\" /Users/arsis/zlayt-pm-project/evals/golden/sample.txt; grep -F \"Discharge visit 97110 charge \\$185.00\" label_repro_r7.out | head -1 | cut -c1-200",
 "description": "Confirm each quoted line in the draft appears verbatim in the evidence"
}
````

### User / tool · 2026-11-03T15:07:45.798Z

**tool result**
````
1
1
2
4
1
0
1
    Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $185.00 | quote: Discharge visit 97110 charge $185.00.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:07:48.543Z

**tool call — Bash**
````
{
 "command": "grep -n -F \"Late entry for the visit of 01/16/2026\" artifacts/review-evidence/T-202-paralegal-r6/fullpipe_r6.py | cut -c1-120",
 "description": "Locate the late-entry probe sentence in the round-6 probe script"
}
````

### User / tool · 2026-11-03T15:07:48.630Z

**tool result**
````
56:    "a5_late_entry_01_20 [truth Jan 16]": ("150", add(OVN, "Late entry for the visit of 01/16/2026. Office visit 9921
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:07:51.007Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md",
 "old_string": "(the same note's sentence reads 'Late entry for the visit of 01/16/2026.').",
 "new_string": "(the probe's source sentence, artifacts/review-evidence/T-202-paralegal-r6/fullpipe_r6.py:56, reads 'Late entry for the visit of 01/16/2026.')."
}
````

### User / tool · 2026-11-03T15:07:51.106Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:07:53.779Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/jsoncheck_r7.py artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md && cp artifacts/review-evidence/T-202-paralegal-r7/draft-T-202-paralegal-r7.md reviews/T-202-paralegal-r7.md && python3 tools/board.py validate reviews/T-202-paralegal-r7.md; echo EXIT=$?; ls -la reviews/T-202-paralegal-r7.md",
 "description": "Check the draft, publish it to reviews, and run the board validator"
}
````

### User / tool · 2026-11-03T15:07:53.954Z

**tool result**
````
ok fail {'blocker': 1, 'major': 0, 'minor': 3, 'nit': 0} model claude-haiku-5-5
ok (1 file(s))
EXIT=0
-rw-r--r--@ 1 arsis  staff  15419 Nov  3 09:07 reviews/T-202-paralegal-r7.md
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:08:04.710Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r7-label-kind-patterns.md",
 "content": "---\nname: t202-r7-label-kind-patterns\ndescription: T-202 r7 (a932fc9/be257c9, D-073 all-blank fallback) fail: DOS blank holds, but 'statement dated' still lands on clinical records whose excerpt opens with a money word; letter_check shares that rule so it passes it\nmetadata:\n  type: project\n---\n\nReview file: reviews/T-202-paralegal-r7.md (verdict fail; 1 blocker, 3 minors). Re-rated the r6 major (label kind) to blocker: calibration says a spec-line violation is a blocker; r6's \"no corpus line affected\" argued impact.\n\n**Holds at HEAD.** No charge line prints a DOS: service_date.resolve never returns stated (service_date.py:406-413), export.charge_when has no date path (export.py:210-215). Round-6 visit-note and UB-04 shapes print the blank. letter_check value 0 over 25 cases. Parenthetical record date equals the input Date header on every line checked.\n\n**Still broken.** record_kind (service_date.py:51-52) makes a record a bill when the first 40 characters of the excerpt hold a financial word, before the label's document-type phrase is read. letter_check.py:206 repeats the same rule, so the eval agrees with the wrong kind. Repro: label_repro_r7.py V1 (ER summary opening 'ER charges:') and V2 (PT visit opening 'Payment plan discussed').\n\n**Carried, still open:** notes say \"fill it from the quote\" for quotes with no date (export.py:602); lib11 14-visit line keeps singular \"date of service\" (exact form pinned in letter_check.charge_date_violations).\n\n**New minor:** a record date prints beside a charge its own note dates elsewhere (late entry 01/16 -> \"record dated January 20\"; initial evaluation -> \"record dated March 6\"). Blank is correct; the paralegal fills from the printed date.\n\n**Why:** the blank fallback removed the DOS failure class, but the label rule is a second classifier that the eval reuses. Any new check of label kind must read the rule independently or it cannot fail.\n\n**How to apply:** next round, mutation-test the label: a discharge-summary or visit-note line with 'statement dated' must be rejected by letter_check, and the eval's kind reader must not import the app's opening rule. Related: [[t202-r5-d073-patterns]], [[t202-r6-encounter-other-time-patterns]].\n"
}
````

### User / tool · 2026-11-03T15:08:04.800Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r7-label-kind-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:08:06.122Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer && tail -n 3 MEMORY.md",
 "description": "Read the last lines of the paralegal memory index"
}
````

### User / tool · 2026-11-03T15:08:06.207Z

**tool result**
````
- [T-209 r3 patterns](t209-r3-patterns.md) — 8521562 changes: one doubtful branch fills from highlight for 6 reasons; taller foot hides date line
- [T-209 r4 patterns](t209-r4-patterns.md) — 1b3c58a pass: generic sentence; note wording binding D-071 (question, not defect); longest note clips at 1366x768
- [T-209 confirm sentence](t209-confirm-sentence-patterns.md) — 88c73dd changes: static fill-from-highlighted-words vs no-date lines; dotted-leader DOS miss; append-only guard; r2 file
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:08:08.766Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-209 confirm sentence](t209-confirm-sentence-patterns.md) — 88c73dd changes: static fill-from-highlighted-words vs no-date lines; dotted-leader DOS miss; append-only guard; r2 file",
 "new_string": "- [T-209 confirm sentence](t209-confirm-sentence-patterns.md) — 88c73dd changes: static fill-from-highlighted-words vs no-date lines; dotted-leader DOS miss; append-only guard; r2 file\n- [T-202 r7 label-kind patterns](t202-r7-label-kind-patterns.md) — a932fc9/be257c9 fail: DOS blank holds; 'statement dated' on money-opening clinical records (blocker); eval shares the rule"
}
````

### User / tool · 2026-11-03T15:08:08.869Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:08:13.069Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md"
}
````

### User / tool · 2026-11-03T15:08:13.083Z

**tool result**
````
1	---
2	name: reviewer-hook-constraints
3	description: Bash hooks that block reviewer commands in this repo (board.py --help, python -c containing backticks) and the workarounds
4	metadata:
5	  type: reference
6	---
7	
8	- board-guard: reviewers may run only `tools/board.py validate|show|list|status`. `--help` is rejected.
9	- git-guard fails to parse `python3 -c "..."` when the code contains escaped backticks. Use a quoted heredoc (`python3 - <<'EOF'`) and build the fence as '`'*3.
10	- Write access is limited to reviews/ and artifacts/review-evidence/ (plus this memory dir). Probe scripts go in artifacts/review-evidence/.
11	- T-118 (2026-11-02): the Write tool is refused for the session scratchpad (reviewer-write-guard), and board-guard refuses `mkdir` there. A Bash `git archive | tar -x` into the scratchpad still worked. Put scripts and output dirs under artifacts/review-evidence/ and run archive copies from the scratchpad. Run them with `.venv/bin/python -I` and a runner that puts the archive root first on sys.path.
12	
13	**How to apply:** use these forms directly to avoid wasted tool calls. Related: [[golden-set-recurring-findings]]
14	
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:08:16.138Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md",
 "old_string": "**How to apply:** use these forms directly to avoid wasted tool calls. Related: [[golden-set-recurring-findings]]",
 "new_string": "- T-202 r7 (2026-11-03): `mkdir -p` and `git archive | tar -x -C <dir>` inside artifacts/review-evidence/ worked. `.venv/bin/python -I <runner> <archive_root>` where the runner does sys.path.insert and runpy.run_module('evals.letter_check') reproduces `python -m evals.letter_check` under -I. A single Bash call with a shell variable (`F=...; grep ... $F`) was refused by board-guard (\"redirect to =1\"); use literal paths.\n- T-202 r7: `cp <draft in artifacts/review-evidence/> reviews/<new>.md` then `python3 tools/board.py validate reviews/<new>.md` returned \"ok (1 file(s))\".\n- T-202 r7: HEAD moved during a review (a932fc9 to be257c9, README only). Pin the archive hash at the start and report the moved HEAD with its diff stat.\n\n**How to apply:** use these forms directly to avoid wasted tool calls. Related: [[golden-set-recurring-findings]]"
}
````

### User / tool · 2026-11-03T15:08:16.232Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-03T15:08:20.806Z

Verdict fail for T-202 r7 at `/Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r7.md`: the DOS blank holds at HEAD (letter_check 0), but the blocker is that a clinical record's charge line prints "statement dated" when its excerpt opens with a money word, and this review ran on claude-haiku-5-5 rather than the expected Opus.
