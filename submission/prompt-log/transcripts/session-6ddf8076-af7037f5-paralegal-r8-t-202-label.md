# Subagent: Paralegal r8: T-202 label (Paralegal r8: T-202 label)

Source: `agent-af7037f5c257e317b.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T15:13:19.867Z

You are the paralegal reviewer in /Users/arsis/zlayt-pm-project, starting from a fresh context. Re-check T-202 at commit cd7fd27; read reviews/T-202-paralegal-r7.md (its blocker).

In a `git archive cd7fd27` copy in demo mode on your own port, and also in local mode for lib10 and lib11 (stop your PIDs afterward):
- every charge line in the sample, case_09, lib10 and lib11 letters reads exactly "date of service [__________] (record dated X)";
- X is the record's own date;
- no "statement dated" appears anywhere in the letter or Step 3;
- `python -m evals.letter_check` reports 0.

Re-run your r7 probe (an ER record whose excerpt opens with "ER charges:"). Write reviews/T-202-paralegal-r8.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:20.944Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-03T15:13:20.953Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:21.299Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r7.md"
}
````

### User / tool · 2026-11-03T15:13:21.306Z

**tool result**
````
1	# T-202 round 7 (D-073 all-blank fallback, b50952d): paralegal review (Maria Delgado, senior PI paralegal)
2	
3	**Verdict: fail.** The round-6 wrong-date blockers are closed at HEAD. No charge line prints a service date, and the UB-04 period and the visit-note dates can no longer reach the letter. One blocker remains: a clinical record's charge line is labelled "statement dated" when its excerpt opens with a money word. That breaks D-073 rule (4). I re-rate the round-6 major for that defect to blocker (finding 1 gives the reason). letter_check's value of 0 does not catch it, because the eval reads the record kind with the same rule.
4	
5	**Pin.** `git archive a932fc9` (tree 5f74b737), extracted to `artifacts/review-evidence/T-202-paralegal-r7/archive`. HEAD moved to be257c9 during the review. That commit changes README.md only, and the diff of app/backend, app/llm, app/frontend, evals and tests is empty between the two, so the results apply to be257c9 too.
6	
7	**What I checked, in brief.**
8	- Charge lines: 19 in-process (sample, case_09, lib10, lib11; accepted-all and counted variants) and 8 live over HTTP. Every line is `<source>, date of service [__________] (statement|record dated <Month D, YYYY>)` with no other date on it. Each parenthetical date equals the record's own Date line in the input (check_letters_r7.out, live_summary.out).
9	- `python -m evals.letter_check` equivalent, run with -I against the archive: value 0, 25 cases, exit 0 (letter_check.out).
10	- Round-6 shapes (fullpipe_r6.py, run on the archive): every charge line in those shapes prints the blank, and date violations are empty on each. Shapes that are not accepted as charges print no charge line. The visit-note dates (initial evaluation, late entry, yesterday, ER charge in a PCP note, course total, collision day) and the UB-04 period override (u1) no longer print a date of service. Structurally, `service_date.resolve` never returns a stated date (service_date.py:406-413) and `export.charge_when` has no date path (export.py:210-215).
11	- Teeth: a printed "date of service March 6, 2026" and a wrong record date are both rejected in all four cases (8 of 8 mutants).
12	
13	**Severity re-rate.** Round 6 rated the label defect (finding 1) major. The calibration rates a violation of a spec line as a blocker, and D-073 rule (4) is a spec line. The round-6 reason, that no corpus line is affected, is an impact argument and does not lower the class.
14	
15	**Verify-quickly score (3).** Each amount and each quote checks in one step. The date of service, though, is a manual lookup on every charge line, because 7 of the 8 live quotes carry no date. The record-kind word cannot be trusted without opening the record (finding 1).
16	
17	**Model.** This review ran on claude-haiku-5-5, the model I am running as. CLAUDE.md section 6 and my dossier expect claude-opus-5-5 for judgment reviews. See questions_for_chris.
18	
19	**Not exercised (outside this brief).** Timeline entries, the review screen and keyboard path, Step 3 UI text, and the 25-case corpus label count (round-6 corpus_blanks.py was not re-run). The gate review GATE-M3M4-paralegal.md was pinned at f6d5c19. It did not test the label shapes in finding 1, and it was signed claude-sonnet-5-5, so I did not rely on it for this card.
20	
21	```json
22	{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
23	 "scope": "git archive a932fc9 (tree 5f74b7377e5fd55b9be2beb47090b9b0dfbc812d) extracted to artifacts/review-evidence/T-202-paralegal-r7/archive; HEAD moved to be257c9 (README.md only) during the review, and the app/backend, app/llm, app/frontend, evals and tests diff is empty; app served from that archive at http://127.0.0.1:7987 (ZLAYT_MODE=local, LLM_BACKEND=fixture, FIXTURE_SET=curated; /api/health demo_mode true, local_mode true), stopped by PID 84772 (lsof exit 1, curl 000). Cases: sample, case_09, lib10, lib11 (SYNTHETIC inputs from evals/golden and evals/library). Evidence: artifacts/review-evidence/T-202-paralegal-r7/.",
24	 "exercised": [
25	  "Read personas/paralegal.md (live dossier), reviews/T-202-paralegal-r6.md (blockers, majors, minors), reviews/GATE-M3M4-paralegal.md, board.py show T-202 (round-6 findings and round-7 notes), memory/ORCHESTRATOR_DECISIONS.md:97-104 (D-073, rounds 6 rules and fallback)",
26	  "git rev-parse HEAD: a932fc9 at the start, be257c9 at the end; git log --oneline a932fc9..HEAD: be257c9 docs(release) only; git diff --name-only a932fc9 HEAD: README.md; git diff --stat a932fc9 HEAD -- app/backend app/llm app/frontend evals tests: empty; git merge-base --is-ancestor b50952d HEAD: ancestor; git diff f6d5c19 a932fc9 -- app/backend/export.py app/backend/service_date.py: two changed lines, one of them the service_date.py no_date reason text; no charge-line logic changed since the gate pin",
27	  "git archive a932fc9 | tar -x into artifacts/review-evidence/T-202-paralegal-r7/archive (tree 5f74b7377e5fd55b9be2beb47090b9b0dfbc812d)",
28	  "run_letter_check_r7.py (python -m evals.letter_check, run with .venv/bin/python -I against the archive): {\"value\": 0, \"cases\": 25, \"held_out_entries\": 11, \"backend\": \"fixture\"}, exit 0 (letter_check.out)",
29	  "check_letters_r7.py on the archive: sample, case_09, lib10, lib11 through evals.letter_check.letters_for (accepted-all and counted): 19 charge lines, each exact form, parenthetical date equal to the input Date header, kind and source as written; problems 0; 8 teeth mutants (printed DOS, wrong record date) all rejected (check_letters_r7.out)",
30	  "serve_r7.py on 127.0.0.1:7987 from the archive; live_letters_r7.py over HTTP (POST /api/cases, POST run, GET status, accept every pending entry, amount and flag, GET export) for sample, case_09, lib10, lib11: 8 charge lines, all exact; totals $8,390.00, $275.00, $8,123.50, $3,260.00 (live_summary.out, live/*-letter.txt, live/sample-case.json). lib11 ledger items (10 refused, count confirm needed) not counted over HTTP; the counted variant in check_letters_r7.out covers them in-process",
31	  "fullpipe_r6.py on the archive (the round-5 and round-6 shapes in that file: visit-note A-shapes, UB-04 U-shape, provider-name M and C shapes, key-value and table T shapes; through the full pipeline and letter_check): fullpipe_r6_shapes_at_a932fc9.out; every charge line prints the blank; date violations [] on each shape; shapes not accepted as charges print no charge line",
32	  "eval_teeth_r6.py on the archive: eval_teeth_r6_at_a932fc9.out (part 1: build line rejected and blank accepted for A2, A5, A6b, A10; part 2: L1-L4 print 'statement dated' on clinical records)",
33	  "label_repro_r7.py (SYNTHETIC variants through letters_for: V1 ER summary whose excerpt opens 'ER charges:', V2 PT visit whose excerpt opens 'Payment plan discussed'): label_repro_r7.out",
34	  "jsoncheck_r7.py on this review (one json block, keys, verdict rule) before publishing",
35	  "Not exercised: timeline entries, review screen and keyboard path, Step 3 UI, the 25-case corpus label count (corpus_blanks.py not re-run)"
36	 ],
37	 "verdict": "fail",
38	 "scores": {"verify_quickly": 3, "letter_dates_correct": 5, "adversarial_dates_correct": 5, "blank_label_correct": 2},
39	 "findings": [
40	  {"severity": "blocker",
41	   "title": "D-073 rule (4) broken: a clinical record's charge line says 'statement dated' when its excerpt opens with a money word (round-6 major, re-rated to blocker)",
42	   "evidence": "label_repro_r7.out, V1: 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240.00 | quote: ER charges: $6,240.' V2: 'Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $185.00 | quote: Discharge visit 97110 charge $185.00.' Both: letter_check.charge_date_violations returns []. Cause: service_date.py:51-52 takes the excerpt's first 40 characters (cut at the first colon or full stop) and returns 'bill' when they hold a financial word (_hit(_FIN, opening)) before the document-type phrase in the source label is read. letter_check.py:206 repeats the same rule, so the eval agrees with the wrong label. eval_teeth_r6_at_a932fc9.out part 2: 'L1 ... -> (statement dated January 9, 2026)', 'L2 office visit note ... (statement dated January 16, 2026)', 'L3 PT note ... (statement dated March 6, 2026)', 'L4 ER record ... account 4471 ... (statement dated January 9, 2026)'. Rule: memory/ORCHESTRATOR_DECISIONS.md:100, D-073 round-6 rule (4): 'a blank on a non-bill record reads \"(record dated X)\", on a bill \"(statement dated X)\".' The sample is not affected: its ER excerpt opens 'Dx:' (evals/golden/sample.txt:11) and prints '(record dated January 9, 2026)' (live/sample-letter.txt:41).",
43	   "why_it_matters": "The letter tells the adjuster that an ER discharge summary and a PT visit note are statements. The adjuster will ask for a statement that does not exist, and the paralegal gets a document type the record does not state. The date beside it is the record's own date, so no date is invented, but the document type is. This violates a binding spec line, and the calibration rates that as a blocker. Round 6 rated it major because no corpus line is affected; that argues about impact and does not change the class. The eval also cannot catch it (V1 and V2 pass letter_check), so the harness has a blind spot on the same rule.",
44	   "fix": "service_date.record_kind (service_date.py:46-56): a whole document-type phrase in the source label (the encounter list in encounter_types.json) decides first; the excerpt opening decides only when the label has no document-type phrase, and a financial word in the label alone makes a bill only when the label names no document type. letter_check._record_kind (letter_check.py:201-210) must read the rule from the table on its own terms, not reuse the same opening test, so the eval can disagree with the app.",
45	   "acceptance_test": "label_repro_r7.py V1 prints '(record dated January 9, 2026)' and V2 prints '(record dated March 6, 2026)'; eval_teeth_r6.py L1-L4 print 'record dated'; L5 (no document type, opens 'Charges:') and L6 (billing statement) keep 'statement dated'; a test in tests/ shows letter_check.charge_date_violations rejecting 'statement dated' on a discharge summary line and on a visit-note line."},
46	  {"severity": "minor",
47	   "title": "Carried from rounds 3-6 (still open): the internal notes say 'fill it from the quote' when the quote holds no date",
48	   "evidence": "fullpipe_r6_shapes_at_a932fc9.out, notes line for the sample ER charge: '- Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.' The quote it points to is 'ER charges: $6,240.' (live/sample-letter.txt:42). The sentence is built at export.py:602; the Step 3 sentence for the same reason is service_date.py:144 (_ASK_NONE): 'Take the date from the matching visit note, or request a dated itemized bill'.",
49	   "why_it_matters": "For the sample's charges the quote holds no date, so the notes tell the paralegal to fill a date the quote cannot give, while Step 3 tells her to take it from the visit note. Two instructions for one blank.",
50	   "fix": "The notes use the Step 3 sentence (service_date._ASK_NONE) for the no-date reasons, and the words 'from the quote' stay only for the written-date reasons.",
51	   "acceptance_test": "No notes line says 'fill it from the quote' when the quote holds no date: for the sample and lib10 charges, grep of the notes for 'from the quote' finds nothing."},
52	  {"severity": "minor",
53	   "title": "Carried from round 6 (still open): a 14-visit charge gets a single-date blank",
54	   "evidence": "check_letters_r7.out, lib11 counted: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $2,310.00 | quote: treatment visits 1 through 14 charge $2,310.00'. The singular form is pinned by charge_date_violations (letter_check.py:213 onward).",
55	   "why_it_matters": "One date blank over 14 visits asks the paralegal for one date for a range, and the quote gives none. The exact-form rule makes this a spec decision, not a code fix.",
56	   "fix": "Decide in the spec: either allow 'dates of service [__________]' for a quote that counts visits (D-073 and letter_check's exact form change together), or keep the singular and say in the notes that the line covers 14 visits.",
57	   "acceptance_test": "The lib11 $2,310.00 line prints the plural form, or its notes line says it covers 14 visits; the chosen form is recorded in D-073 and letter_check accepts only that form."},
58	  {"severity": "minor",
59	   "title": "New: a record date is printed beside a charge that the same note dates elsewhere",
60	   "evidence": "fullpipe_r6_shapes_at_a932fc9.out, a5: 'Dr. Alvarez, office visit note, date of service [__________] (record dated January 20, 2026): $150.00 | Office visit 99213 charge $150.' (the probe's source sentence, artifacts/review-evidence/T-202-paralegal-r6/fullpipe_r6.py:56, reads 'Late entry for the visit of 01/16/2026.'). a2: 'Capital PT, physical therapy note, date of service [__________] (record dated March 6, 2026): $250.00 | Initial evaluation 97161 charge $250.' (record 4 dates the initial evaluation 2026-01-23).",
61	   "why_it_matters": "The blank is correct and the record date is true. The printed date still sits beside a charge the record dates elsewhere. The round-6 brief says the paralegal fills blanks from the date printed next to them, which is how a wrong date gets into the demand. No excerpt makes it false, so this is minor, not a blocker.",
62	   "fix": "Open question for the orchestrator (questions_for_chris 2): withhold the parenthetical when the charge's own sentence carries a time word (the round-6 rule (3) guard words), so a printed date appears only beside charges the record dates by its own header.",
63	   "acceptance_test": "The chosen form is recorded in D-073, and a probe with 'Late entry for the visit of 01/16/2026. Office visit 99213 charge $150.00.' prints the chosen form in both the letter and the eval."}
64	 ],
65	 "whats_right": [
66	  "No service date is printed on any charge line at HEAD: 19 in-process and 8 live charge lines are the exact blank, the round-6 visit-note and UB-04 shapes print the blank, and letter_check reports 0 over 25 cases (letter_check.out, fullpipe_r6_shapes_at_a932fc9.out).",
67	  "Each parenthetical date equals the record's own Date line in the input, and the totals match the accepted charges: $8,390.00, $275.00, $8,123.50 (check_letters_r7.out, live_summary.out).",
68	  "The teeth check works: a printed service date and a wrong record date are rejected in all four cases (check_letters_r7.out, TEETH lines)."
69	 ],
70	 "questions_for_chris": [
71	  "Model: this review ran on claude-haiku-5-5 (the model I am running as). CLAUDE.md section 6 and the dossier expect claude-opus-5-5 for judgment reviews. Should T-202 get an Opus re-run before it counts? The same question applies to reviews/GATE-M3M4-paralegal.md, which is signed claude-sonnet-5-5 and pinned f6d5c19, before aa21b24 and 43ce6eb.",
72	  "Finding 4: should the record date be withheld beside a charge whose own sentence dates it elsewhere (late entry, initial evaluation, 'yesterday'), or does D-073 require it on every charge line?",
73	  "Finding 3: keep the singular 'date of service' over a 14-visit quote, or allow 'dates of service [__________]' for count quotes?"
74	 ]}
75	```
76	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:21.729Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r7-label-kind-patterns.md"
}
````

### User / tool · 2026-11-03T15:13:21.735Z

**tool result**
````
1	---
2	name: t202-r7-label-kind-patterns
3	description: T-202 r7 (a932fc9/be257c9, D-073 all-blank fallback) fail: DOS blank holds, but 'statement dated' still lands on clinical records whose excerpt opens with a money word; letter_check shares that rule so it passes it
4	metadata:
5	  type: project
6	---
7	
8	Review file: reviews/T-202-paralegal-r7.md (verdict fail; 1 blocker, 3 minors). Re-rated the r6 major (label kind) to blocker: calibration says a spec-line violation is a blocker; r6's "no corpus line affected" argued impact.
9	
10	**Holds at HEAD.** No charge line prints a DOS: service_date.resolve never returns stated (service_date.py:406-413), export.charge_when has no date path (export.py:210-215). Round-6 visit-note and UB-04 shapes print the blank. letter_check value 0 over 25 cases. Parenthetical record date equals the input Date header on every line checked.
11	
12	**Still broken.** record_kind (service_date.py:51-52) makes a record a bill when the first 40 characters of the excerpt hold a financial word, before the label's document-type phrase is read. letter_check.py:206 repeats the same rule, so the eval agrees with the wrong kind. Repro: label_repro_r7.py V1 (ER summary opening 'ER charges:') and V2 (PT visit opening 'Payment plan discussed').
13	
14	**Carried, still open:** notes say "fill it from the quote" for quotes with no date (export.py:602); lib11 14-visit line keeps singular "date of service" (exact form pinned in letter_check.charge_date_violations).
15	
16	**New minor:** a record date prints beside a charge its own note dates elsewhere (late entry 01/16 -> "record dated January 20"; initial evaluation -> "record dated March 6"). Blank is correct; the paralegal fills from the printed date.
17	
18	**Why:** the blank fallback removed the DOS failure class, but the label rule is a second classifier that the eval reuses. Any new check of label kind must read the rule independently or it cannot fail.
19	
20	**How to apply:** next round, mutation-test the label: a discharge-summary or visit-note line with 'statement dated' must be rejected by letter_check, and the eval's kind reader must not import the app's opening rule. Related: [[t202-r5-d073-patterns]], [[t202-r6-encounter-other-time-patterns]].
21	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:22.119Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md"
}
````

### User / tool · 2026-11-03T15:13:22.126Z

**tool result**
````
1	---
2	name: reviewer-run-pitfalls-pass4
3	description: T-060/T-114 pass-4 run pitfalls: HEAD moves mid-review (pin by hash, run both if brief says HEAD and card names a commit); venv path relative from subdirs (exit 127); sed -i blocked again; Playwright selectors for case list, disclosure, confirm-date radios; reload restores the case
4	metadata:
5	  type: reference
6	---
7	
8	- HEAD moved during the review: 433ac1c became f7829c1 while I worked (other agents commit). Record the hash you archived with `git rev-parse --short HEAD` at the start AND `git archive <hash>`. When the brief says HEAD and the card names a commit (e293daa), run both and say which commit each finding applies to. Check `git diff --stat <card-commit> HEAD -- app/frontend` (empty = same UI).
9	- Server launch: `env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch db> PORT=<p> HOST=127.0.0.1 .venv/bin/python -I artifacts/review-evidence/<card>-paralegal-pass4-serve.py <archive_root>` (runpy, puts the archive root first on sys.path). Background launch: the launcher task exits 0 while the listener lives; get the listener PID with `lsof -iTCP:<p> -sTCP:LISTEN -nP`, kill by number, confirm curl = 000. Port 7860 is the live dev app; never touch it.
10	- `.venv/bin/python` is relative: from artifacts/review-evidence/<card>/ it exits 127. Run from repo root.
11	- `sed -i` is refused by board-guard again (pass 4). Use the Edit tool on scripts and memory; check `grep -c` after.
12	- Playwright selectors (e293daa/HEAD): case list buttons are `[data-testid=case-<token>]`; library entries `[data-testid=library-case_lib09_spanish_interpreter_espalda]` sit inside a collapsed disclosure: click `summary:has-text('synthetic library')` first. The lib09 names repeat ("Spanish-language records, back pain") and differ only by token: never pick by name. Date step: `button:has-text('1 date to confirm')`; radios via `get_by_label("March 5, 2026")`; confirm `get_by_role("button", name="Confirm date")`; there is NO `form[data-testid=confirm-date]` in this build. Gap notice `[data-testid=gap-change-note]`; dismiss it `[data-testid=btn-dismiss-gap-note]`. Dismissed entries group `[data-testid=dismissed-summary]`. Export `[data-testid=btn-export]`, letter `[data-testid=export-letter]` (a PRE, read innerText not value), copy `[data-testid=btn-copy-letter]`, download `[data-testid=btn-download-letter]`.
13	- Keyboard: `a` on a flag or amount acts on it; `d` on a flag dismisses without a reason prompt; `e` opens the textarea only when focus is on the row, and Ctrl+Enter saves.
14	- Reload restores the last case view (no paste page), so a probe that expects the paste box after reload will time out. Use the case list or continue on the restored case.
15	- Output discipline: write every probe's output with `> file` in the same call; console-only numbers do not count as evidence when the review quotes them.
16	- Review files are write-once: proofread every line reference with grep before the single Write (api.md:341 D-045b checked; the erratum route is the final reply).
17	
18	Why: all of these cost a probe rerun or an unfixable review line during the T-060/T-114 pass-4 run.
19	How to apply: start each Playwright run with `curl` on the port, confirm the archive hash, and keep one helper module per card. Related: [[reviewer-tooling-quirks]], [[reviewer-api-shape-gotchas]], [[t060-pass4-state-patterns]], [[t114-r3-gap-change-persistence]].
20	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:23.713Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log --oneline -5 && python3 tools/board.py show T-202 | tail -40 && ls artifacts/review-evidence/T-202-paralegal-r7/ && ls memory/ORCHESTRATOR_DECISIONS.md && sed -n 95,110p memory/ORCHESTRATOR_DECISIONS.md"
}
````

### User / tool · 2026-11-03T15:13:23.922Z

**tool result**
````
cd7fd27
cd7fd27 feat(backend): D-075 charge blank always reads (record dated X); drop statement variant (T-202)
be257c9 docs(release): drop OWNER placeholder clone step from README (T-212)
a932fc9 docs(writer): T-218 ship-bar row 5 and Part 2 cite the final suite at 43ce6eb; captions are burned in; PDFs re-rendered (1 and 4 pages)
c2dd104 fix(qa): T-184 demo.webm re-recorded at 43ce6eb (Step 3 MRI note shows the new wording), caption band below the app so Saved and Undo show; final green suite record
43ce6eb fix(backend): gate M3+M4 fix A part 2, no_date note no longer says the code reads dates; README reviews pointer
    - [major] The blank says '(statement dated X)' on records that are not statements (19 of 22 corpus blanks are ED, urgent-care, imaging or radiology records), and Step 3 says the date 'is the statement date, not the service date' when it is the visit's own date — fix: Word the parenthetical by record kind. For a bill: '(statement dated X)'. For any other record: '(record dated X)'. Make step3.j
    - [major] A 'Date of service: X  Account: N' line directly over an un-headed row is read as that row's column heading, so the row's other date prints as the date of service; letter_check enforces it — fix: A heading line must not contain a date. A line that holds a date with a 'Date of service' label is a labeled value, not a column heading. When such a line sits over a row whose own date diff
    - [minor] A several-visit total inside an identified visit note, with no 'visits'/'to date' word, prints the note's date (allowed by D-073 rule 2) — fix: When an encounter note's charge exceeds a per-visit rate stated elsewhere in the case for the same provider, print the blank. Or add 'course', 'plan of care' and 'episode' to the several-visits words.
    - [minor] Carried from rounds 3 and 4: the notes still say 'fill it from the quote' for quotes with no date (Step 3 now says 'take the date from the matching visit note'), and one single-date blank covers 'visits 1 through 14' — fix: Use the Step 3 wording in the notes too. Print 'dates of service [__________]' when the quote counts visits.
    - [minor] Carried from rounds 1-4: some charge quotes name neither the service nor the date; with dotted leaders the quote is now the bare figure — fix: Quote the bill line from its code or description through the figure. With leaders, quote the whole leader line.
- 2026-11-03T02:57:45Z orchestrator: assigned: backend
- 2026-11-03T02:57:45Z orchestrator: Paralegal r5: corpus dates all correct; blocker = single encounter words (MRI, X-Ray, Follow-Up, Evaluation, Exam) match provider names. Round 6 plan (after staff r5): encounter_types.json holds whole document-type phrases only (no single words); non-bill blanks say 'record dated X' not 'statement dated'; a 'Date of service: X' line is a label, a column heading needs a table with >=2 dated rows.
- 2026-11-03T03:09:35Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): fail — reviews/T-202-staff-engineer-r5.md
- 2026-11-03T03:09:35Z backend: moved changes_requested -> in_progress
- 2026-11-03T03:26:33Z backend: r6 (D-073 round-6 rules 1-5) in progress: tests/unit/test_t202_r6_d073.py written first (78 failed, 43 passed on f9c0faf code); production + letter_check (own scanner) now implement whole-phrase encounter table, real-table rule (header row, 2 dated rows, equal cell counts), several-dates/month-year/earlier-next-previous guard incl. UB-04, record dated vs statement dated (API field service_date.date_label), promotion flag without date. Corpus: 84 lines -> 26 unchanged, 38 statement->record label only, 20 date->blank (10 distinct MRI/visit lines incl. the sample MRI). qa-owned golden evals/golden/sample.export.expected.txt edited (MRI line + one notes section). Mutant run + git-archive verification next.
- 2026-11-03T04:19:30Z backend: r6 progress (not blocked): rules 1-5 + T-207 pins committed b72acb9, 3654cf9, 756546b; archive 756546b verified (unit 6814 passed 12 skipped 0 failed, guided e2e 156 passed, letter_check 0/25). Running the last 4 old staff mutants (L5, L6, L9, N8 survive) and writing the handoff.
- 2026-11-03T04:33:34Z backend: AC 1 checked: r6 (D-073 round 6) 9655f1d from git archive (tree 823f8e2e8d56): unit 6815 passed 12 skipped 0 failed (4 shards); guided e2e 156 passed; python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r6_d073.py 152 tests (78 red on f9c0faf first); 100 own mutants: 99 killed, 1 equivalent
- 2026-11-03T04:33:34Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2-3, T-207). Row 2 replace the two-source sentence with: 'A charge line's date of service has two sources only. (1) The date cell of its own row in a REAL bill table: a header row of short labels (<= 4 words, no colon) with a whole-cell service heading (DOS, date(s) of service, service date, svc date, visit date, date of visit, encounter date, service/svc from/to/thru, from/to service/dos/svc, 24A, or a bare From/To under a 24A line), at least two data rows below it with the same number of cells and a date-only cell in the service column(s); or the one UB-04 statement (covers) period of a coded line whose sentence has no previous/prior/next/last/earlier/balance forward. A Date of service: X line, a key-value line or a sentence is never a heading. (2) The record dates own date, only for a source label holding a whole document-type phrase from encounter_types.json (no single word) and only when the charge sentence holds at most that one date, no visit count (visits, sessions, to date, 2 x, visit 1-9), no month-year and no earlier/previous/prior/next/last/later/ago phrase.' Row 3: blank reads (statement dated X) on a bill and (record dated X) on any other record; API service_date.date_label. Pins (tests/unit/test_t202_r6_d073.py): whole phrase test_every_encounter_term_is_a_whole_document_type_phrase + test_a_word_that_also_names_a_service_or_a_provider_never_makes_a_visit_note; real table test_a_heading_over_one_data_row_is_not_a_table, test_a_key_value_line_or_a_sentence_naming_dos_is_not_a_column_heading, test_a_heading_cell_that_names_the_service_is_read_in_a_real_table, test_a_heading_cell_that_does_not_name_the_service_gives_the_blank, test_a_header_row_must_be_all_short_labels, test_every_service_column_must_hold_a_date_in_the_data_rows, test_two_dates_in_one_dos_cell_give_the_blank_not_the_first, test_two_dos_columns_with_different_dates_give_the_blank_not_the_first, test_a_pipe_delimited_table_is_a_table; other time test_another_time_in_the_encounter_sentence_gives_the_blank, test_a_charge_for_more_than_one_visit_in_an_encounter_gives_the_blank, test_a_visit_range_is_a_charge_for_more_than_one_visit, test_ub04_*; opening window test_the_opening_of_the_excerpt_is_its_first_40_characters_cut_at_a_colon_or_full_stop, test_the_check_reads_the_opening_length_from_the_shared_table, test_an_administrative_opening_of_the_excerpt_makes_the_record_other; notes test_the_confirm_note_for_all_six_written_reasons_asks_to_confirm_from_the_quote; label test_a_blank_on_a_record_that_is_not_a_bill_says_record_dated, test_a_blank_on_a_bill_says_statement_dated; flag test_the_duplicate_promotion_flag_message_prints_no_date.
- 2026-11-03T04:33:34Z backend: FOR ORCHESTRATOR, frontend card needed: Step 3 (app/frontend/guided/step3.js stmtOnly/recLabel/dateLine) still words the record date as 'statement dated' for a blank on an ED/imaging record; use amounts[].service_date.date_label ('statement'|'record', new in api.md) instead. test_t206 ED service-date-text assertion was changed to '(record dated ...)'; its src-head assertion still says statement until that card lands.
- 2026-11-03T04:33:48Z backend: moved in_progress -> in_review
- 2026-11-03T04:33:58Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-03T13:13:03Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-202-paralegal-r6.md; round 6; findings:
    - [blocker] A visit note's own date is printed as the date of service of a charge the note itself places at another time (initial evaluation, first visit, yesterday, the ER, the day of the collision, February, a late entry, an overnight ER stay, a course total); letter_check accepts only the wrong line — fix: Apply the outcome D-073 pre-declares for a round-6 failure: every charge line prints 
    - [blocker] A UB-04 statement period is printed over a coded line that states its own, different service date (rule 3: the UB-04 period gets the same several-dates guard) — fix: Covered by the D-073 final step above. If source (1) is kept, a coded line whose own sentence holds any date gets the blank, the same guard as the encounter sentence.
    - [major] The blank says '(statement dated X)' on clinical records whose excerpt opens with a money word or whose label carries one (rule 4) — fix: Let a whole document-type phrase in the source label (discharge summary, office visit note, physical therapy note, emergency department record) outrank money words in the excerpt opening and in the rest of the label. Use the opening only when the l
    - [minor] Carried from rounds 3-5: the internal notes say 'fill it from the quote' for quotes with no date, while Step 3 says 'Take the date from the matching visit note' — fix: Use the Step 3 sentence (service_date.py _ASK_NONE) in the notes for the no-date reasons.
    - [minor] Carried from rounds 3-5: one single-date blank covers a 14-visit charge, and some quotes are only the figure — fix: Print 'dates of service [__________]' when the quote counts visits. Quote the bill line from its code or description through the figure.
- 2026-11-03T13:13:03Z backend: moved changes_requested -> in_progress
- 2026-11-03T13:26:01Z backend: AC 1 checked: r7 D-073 fallback b50952d, git archive, targeted per D-075: letter_check value 0 over 25 cases (blank form required on every charge line); 105 passed (t200, r7_all_blank 11, export x3, letter_eval, e2e test_charge_confirm 12, guided t205+t206 22); make_curated --check and check_golden OK; full unit/e2e left to QA gate
- 2026-11-03T13:26:01Z backend: moved in_progress -> in_review
- 2026-11-03T13:26:27Z orchestrator: review dispatched: paralegal-reviewer + staff-engineer-reviewer (queued: combined M3+M4 gate panel, D-075)
- 2026-11-03T14:51:23Z orchestrator: review dispatched: staff-engineer-reviewer (per-card record from the GATE-M3M4 panel, running)
- 2026-11-03T14:59:35Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): pass — reviews/T-202-gate-M3M4.md
- 2026-11-03T15:08:26Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): fail — reviews/T-202-paralegal-r7.md; round 7; findings:
    - [blocker] D-073 rule (4) broken: a clinical record's charge line says 'statement dated' when its excerpt opens with a money word (round-6 major, re-rated to blocker) — fix: service_date.record_kind (service_date.py:46-56): a whole document-type phrase in the source label (the encounter list in encounter_types.json) decides first; the excerpt opening decides only when the label has no documen
    - [minor] Carried from rounds 3-6 (still open): the internal notes say 'fill it from the quote' when the quote holds no date — fix: The notes use the Step 3 sentence (service_date._ASK_NONE) for the no-date reasons, and the words 'from the quote' stay only for the written-date reasons.
    - [minor] Carried from round 6 (still open): a 14-visit charge gets a single-date blank — fix: Decide in the spec: either allow 'dates of service [__________]' for a quote that counts visits (D-073 and letter_check's exact form change together), or keep the singular and say in the notes that the line covers 14 visits.
    - [minor] New: a record date is printed beside a charge that the same note dates elsewhere — fix: Open question for the orchestrator (questions_for_chris 2): withhold the parenthetical when the charge's own sentence carries a time word (the round-6 rule (3) guard words), so a printed date appears only beside charges the record dates by its own header.
- 2026-11-03T15:08:26Z backend: moved changes_requested -> in_progress
- 2026-11-03T15:13:05Z backend: D-075 done: date_label always record; export/store/letter_check/api.md/step3.js/tests updated; letter_check 0 violations; check-spec true (archive copy); 124 unit + 110 guided e2e + test_round2 pass. SCOPE_CUTS row 28 and docs/LLM_VS_CODE.md still mention '(statement dated X)' (not my paths).
- 2026-11-03T15:13:05Z backend: moved in_progress -> in_review

## Handoff
What changed: charge blank is always 'date of service [__________] (record dated X)'; statement/bill classification removed (service_date.date_label, store, export, letter_check dead classifier, step3.js copy, api.md, tests). How verified: from git archive overlay, letter_check 0 violations, --check-spec true, unit date/export/letter files 124 pass, guided step3/t205/t206/amounts 110 pass, round2 23 pass. Left: SCOPE_CUTS row 28 + docs/LLM_VS_CODE.md rows 3/47 still say statement dated (orchestrator/architect). Sample golden and REQUIREMENTS §6 already read record dated; unchanged. Surprise: none.

archive
check_letters_r7.out
check_letters_r7.py
draft-T-202-paralegal-r7.md
eval_teeth_r6_at_a932fc9.out
fullpipe_r6_shapes_at_a932fc9.out
jsoncheck_r7.py
label_repro_r7.out
label_repro_r7.py
letter_check.out
live
live_letters_r7.py
live_summary.out
run_letter_check_r7.py
serve_r7.py
server_7987.log
memory/ORCHESTRATOR_DECISIONS.md
- D-071 amendment 2 note (T-202 r4): inside bills only, "visit of", "the run of", "rendered on" and "service period" also count as service labels (case_09 and lib14 need them); outside bills they do not. Accepted.

## D-073 — Service dates: the pre-declared conservative fallback (§7.4 after T-202 r4)
Four rounds of date recognition kept finding new prose patterns that print a wrong date of service (r4: a visit note citing an earlier "DOS", a therapy "Treatment dates A to B" range collapsing to B, an unknown source lending its statement date). Binding for the MVP: a charge line prints a service date from exactly two sources, (1) the date cell of its own row in a bill table whose column header names the date of service (or the CMS-1500 24A/UB-04 from-through period, printed as a range), or (2) the encounter record's own date when the charge sits inside a positively identified encounter record (encounter_types.json). Prose labels are no longer read for charge dates at all; every other line prints the fillable blank "date of service [__________] (statement dated X)" with the Step 3 confirm note. letter_check applies the same two-source rule independently. Wider date recognition is SCOPE_CUTS row 28. Expected effect: some corpus lines that printed a correct prose-labelled date now print the blank, which is honest and is shown in the handoff diff.
- D-073 clarification (staff r4 question, decided per rule 1): an encounter record is identified only by a document-type word (visit/progress/office note, ED/ER record, discharge summary, PT/therapy note, ambulance run report, operative report); a provider name (clinic, ED, orthopedics, urgent care, imaging) is never enough. About 19 of 84 corpus charge lines then print the fillable blank; accepted.
- D-073 round-6 rules (§7.4, final; staff r5 + paralegal r5): (1) encounter_types.json holds whole document-type phrases only ("MRI report", "progress note", "emergency department record", "physical therapy note", "ambulance run report", "operative report", "discharge summary", "office visit note"); no single words (MRI, exam, evaluation, follow-up, new patient), because they occur in provider names; (2) a date-of-service column needs a real table: a header row naming at least two columns including the DOS column, and at least two data rows with a date in that column position; a lone "Date of service: X" line or a sentence mentioning DOS is not a heading; (3) several candidate dates, a month-year phrase or an "earlier/next/previous" phrase in the encounter sentence -> blank, each pinned by a test; the UB-04 period gets the same guard; (4) a blank on a non-bill record reads "(record dated X)", on a bill "(statement dated X)"; (5) the duplicate-promotion flag message never prints a prose date. The sample truths fix no charge dates, so sample lines may become blanks. If round 6 still prints a wrong date, the MVP letter prints the fillable blank on every charge line (no date extraction at all) and SCOPE_CUTS 28 covers it.

## D-074 — The deliverable is the demo plus the repo (Chris, 2026-11-03)
Chris will hand Zlayt only the running demo and the repo. So: (1) README.md is the front door: what it is, a two-command setup that works from a fresh clone, a 3-minute guided walk of the demo, and where the LLM-as-judge and the human-in-the-loop live (code, prompts, evals, decisions), with the validation-ladder diagram; (2) the app itself exposes and explains the ladder: each item shows its code check, the second AI check (judge) verdict and reason, and the human decision, and a plain "How each answer is checked" page is reachable from every screen; (3) the submission packet (checklist, product note, Part 2, prompt log) stays in submission/ and is linked from the README; (4) after T-184/T-188 an independent reviewer double-checks the assets and the packet.
- D-073 fallback applied (T-202 r6 paralegal fail: a visit note lends its date to another visit's charge; a UB-04 period overrides a line's own date). Per the pre-declared rule the MVP letter prints the fillable blank "date of service [__________] (record|statement dated X)" on every charge line; no service date is extracted for the letter. Step 3 shows the same. SCOPE_CUTS 28 covers date extraction.

## D-075 — Ship freeze: how we finish fast (Chris, 2026-11-03: "speed all this work up")
Where the time went: serial review→fix rounds per card (T-202 took six), every worker running the full e2e suite (10-20 min each), per-card reviews plus gate panels re-checking the same things, and polish findings reopening cards. Binding until submission:
1. Fix only what makes the demo wrong, crash, leak or mislead (fact errors, provenance, privacy, broken setup). Every other finding (major or minor UX/test-rigor/wording) goes straight to SCOPE_CUTS as accepted debt; no new rounds for it.
2. No more per-card review rounds. The open cards (T-202 fallback, T-207, T-211, T-213, T-184, T-188, T-212) are reviewed once, together, by ONE combined M3+M4 gate panel on one pinned commit, run in parallel (staff, UX, paralegal, privacy, installer, PM; Sonnet except PM). That panel is also Chris's double-check of the assets and packet. One blockers-only fix round, then gate.
3. Workers run targeted tests only; QA runs the full unit + e2e suite once on the gate commit.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:25.945Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-202-paralegal-r8 && mkdir -p $D/archive && git archive cd7fd27 | tar -x -C $D/archive && git rev-parse cd7fd27^{tree} && cd artifacts/review-evidence/T-202-paralegal-r7 && cat check_letters_r7.py run_letter_check_r7.py serve_r7.py label_repro_r7.py live_letters_r7.py"
}
````

### User / tool · 2026-11-03T15:13:27.117Z

**tool result**
````
487a191a8b26728bd84e4bc0c4c1b48e77b5a67b
"""T-202 r7 paralegal check (run from a git archive copy, with -I):
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.py <archive_root>

For the sample, case_09, lib10 and lib11 inputs: runs the real pipeline and export path (evals.letter_check.letters_for, fixture backend,
every item accepted; 'counted' variant too), then checks every BILLED CHARGES line:
  1. the line is EXACTLY '<source label>, date of service [__________] (statement|record dated <Month D, YYYY>)' (no other date-like text on the line);
  2. the parenthetical date equals the record's own 'Date:' header in the INPUT text (parsed here from the raw text, not from the app);
  3. the kind word is 'statement' only for a bill (letter_check's own kind reader), 'record' otherwise;
  4. the number of charge lines equals the number of accepted charges;
  5. no other line of the BILLED CHARGES section, and no line anywhere, prints a date-like string outside the quotes, except the total line and the headers.
Then runs the teeth check: a mutated line with a wrong date of service, or a wrong record date, must be rejected by letter_check.charge_date_violations.
Prints one JSON summary and a per-line table. Exit 0 if every check holds.
"""
import json
import logging
import os
import re
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
os.environ.setdefault("LLM_BACKEND", "fixture")
os.environ.setdefault("FIXTURE_SET", "curated")
logging.disable(logging.CRITICAL)
from evals import letter_check as LC  # noqa: E402

CASES = {
    "sample": "evals/golden/sample.txt",
    "case_09": "evals/golden/case_09_nonvisit_hides_gap.txt",
    "lib10": "evals/library/case_lib10_eob_ub04_cms1500.txt",
    "lib11": "evals/library/case_lib11_priors_and_ledger.txt",
}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
LINE = re.compile(r"^(?P<src>.+), date of service \[__________\] \((?P<kind>statement|record) dated (?P<mon>[A-Z][a-z]+) (?P<day>\d{1,2}), (?P<yr>\d{4})\)$")
# any date-like text: month names, numeric dates, ISO dates
ANY_DATE = re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\b|\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b|\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}\b")


def raw_headers(text):
    """{quote_text: (date_iso, source)} from the INPUT text: each record block's Date/Source/Excerpt, parsed by this script."""
    out = []
    for block in re.split(r"\n=== Record \d+ ===\n", text)[1:]:
        m_date = re.search(r"^Date:\s*(\S+)", block, re.M)
        m_src = re.search(r"^Source:\s*(.+)$", block, re.M)
        m_ex = re.search(r'^Excerpt:\s*"(.*)"\s*$', block, re.M | re.S)
        if m_date and m_src and m_ex:
            out.append({"date_raw": m_date.group(1), "source": m_src.group(1).strip(), "excerpt": m_ex.group(1)})
    return out


def iso_from_raw(s):
    """'2026-03-27' or '3/27/26' (lib11 record 6 header) -> ISO. Only the two forms in the corpus."""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return s
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2})", s)
    if m:
        return f"20{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    raise ValueError(s)


def long_date(iso):
    y, mo, d = (int(x) for x in iso.split("-"))
    return f"{MONTHS[mo - 1]} {d}, {y}"


def check_case(name, path, text):
    res = LC.letters_for(text)
    rows, problems = [], []
    raws = raw_headers(text)
    for variant in ("all_accepted", "counted"):
        got = res[variant]
        letter = got["letters"]["standard"]
        head_lines, tail_lines = _split(letter)
        charge_heads = [l for l in tail_lines if re.search(r": \$[\d,]+\.\d\d$", l) and not l.startswith(LC.TOTAL)]
        n_acc = len(got["charge_cents"])
        if len(charge_heads) != n_acc:
            problems.append(f"{name}/{variant}: {len(charge_heads)} charge heads but {n_acc} accepted charges")
        for head in charge_heads:
            # the Source/quote line sits right under the head
            idx = tail_lines.index(head)
            quote = tail_lines[idx + 1] if idx + 1 < len(tail_lines) else ""
            body = re.sub(r": \$[\d,]+\.\d\d$", "", head)
            m = LINE.match(body)
            ok_form = bool(m)
            dates_on_line = ANY_DATE.findall(body)
            # the parenthetical date is the only date on the line
            if m and dates_on_line != [f"{m.group('mon')}"] and len(dates_on_line) != 1:
                ok_form = False
            # the record the quote came from, by the raw input text
            qtext = quote[quote.index('"') + 1:quote.rindex('"')] if '"' in quote else quote
            hits = [r for r in raws if " ".join(qtext.split()) in " ".join(r["excerpt"].split())]
            rec_ok, kind_ok, src_ok = False, False, False
            if hits and m:
                r = hits[0]
                iso = iso_from_raw(r["date_raw"])
                rec_ok = long_date(iso) == f"{m.group('mon')} {m.group('day')}, {m.group('yr')}"
                kind = "bill" if LC._record_kind(r["source"], r["excerpt"]) == "bill" else "other"
                kind_ok = (m.group("kind") == "statement") == (kind == "bill")
                src_ok = m.group("src").strip() == r["source"]
            row = {"case": name, "variant": variant, "head": head, "quote": quote, "form_exact": ok_form, "parenthetical_is_input_record_date": rec_ok,
                   "kind_matches_record": kind_ok, "source_as_written": src_ok, "dates_on_line": dates_on_line}
            rows.append(row)
            if not (ok_form and rec_ok and kind_ok and src_ok and hits):
                problems.append(f"{name}/{variant}: bad charge line: {head!r} quote={quote!r} row={row}")
        # no date-like text anywhere in the letter outside quotes, except the blank parenthetical and header dates
        # inside the BILLED CHARGES section only (the timeline above it is dated by design): no date-like text outside a quote, except the charge heads checked above
        for line in tail_lines:
            if re.search(r": \$[\d,]+\.\d\d$", line) or line.startswith(LC.TOTAL):
                continue
            stripped = re.sub(r'"[^"]*"', "", line)
            if ANY_DATE.search(stripped):
                problems.append(f"{name}/{variant}: date-like text in the BILLED CHARGES section outside a quote: {line[:160]!r}")
        if got["gate"]:
            problems.append(f"{name}/{variant}: export gate blocked: {got['gate']}")
    viol = {}
    for variant in ("all_accepted", "counted"):
        got = res[variant]
        viol[variant] = LC.charge_date_violations(got["letters"]["standard"], got["records"])
        if viol[variant]:
            problems.append(f"{name}/{variant}: letter_check.charge_date_violations: {viol[variant]}")
    return {"case": name, "path": path, "charge_lines": rows, "violations": viol, "problems": problems,
            "accepted_charges": len(res["all_accepted"]["charge_cents"])}


def _split(letter):
    from app.backend import export
    h, t = export.split_letter(letter)
    return h, t


def teeth(name, text):
    """Mutants the check must reject: a wrong date of service in the blank slot, and a wrong record date in the parenthetical."""
    res = LC.letters_for(text)
    letter = res["all_accepted"]["letters"]["standard"]
    records = res["all_accepted"]["records"]
    out = []
    heads = [l for l in letter.splitlines() if " [__________] (" in l]
    if not heads:
        return [f"{name}: no blank charge line to mutate"]
    h = heads[0]
    bad_dos = h.replace("date of service [__________]", "date of service March 6, 2026", 1)
    bad_rec = re.sub(r" dated [A-Z][a-z]+ \d{1,2}, \d{4}\)", " dated January 1, 2030)", h, count=1)
    for label, mut in (("printed DOS", bad_dos), ("wrong record date", bad_rec)):
        m_letter = letter.replace(h, mut, 1)
        v = LC.charge_date_violations(m_letter, records)
        out.append({"case": name, "mutant": label, "line": mut, "rejected": bool(v), "reasons": len(v)})
    return out


if __name__ == "__main__":
    summary = {"archive": root, "cases": [], "teeth": []}
    for name, path in CASES.items():
        text = open(os.path.join(root, path), encoding="utf-8").read()
        summary["cases"].append(check_case(name, path, text))
        summary["teeth"] += teeth(name, text)
    all_problems = [p for c in summary["cases"] for p in c["problems"]]
    teeth_ok = all(t.get("rejected") for t in summary["teeth"] if isinstance(t, dict))
    summary["charge_lines_checked"] = sum(len(c["charge_lines"]) for c in summary["cases"])
    summary["problems"] = len(all_problems)
    summary["teeth_all_rejected"] = teeth_ok
    print(json.dumps({k: v for k, v in summary.items() if k not in ("cases", "teeth")}))
    for c in summary["cases"]:
        for r in c["charge_lines"]:
            print(f"{c['case']} {r['variant']}: {r['head']}  | quote: {r['quote']}  | form={r['form_exact']} recdate={r['parenthetical_is_input_record_date']} kind={r['kind_matches_record']} src={r['source_as_written']}")
    for t in summary["teeth"]:
        print("TEETH", json.dumps(t, ensure_ascii=False))
    for p in all_problems:
        print("PROBLEM", p[:400])
    sys.exit(0 if not all_problems and teeth_ok else 1)
"""Runs `python -m evals.letter_check` against an archive root, with -I (no cwd or script-dir on sys.path; the archive root is inserted first).
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/run_letter_check_r7.py <archive_root>
Equivalent to `cd <archive_root> && python -m evals.letter_check`; the exit code is letter_check's.
"""
import os
import runpy
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
os.environ.setdefault("LLM_BACKEND", "fixture")
os.environ.setdefault("FIXTURE_SET", "curated")
sys.argv = ["evals.letter_check"]
runpy.run_module("evals.letter_check", run_name="__main__", alter_sys=True)
"""Serves an archive root's app (app.main) for the T-202 r7 check. Run with -I:
    PORT=7987 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/serve_r7.py <archive_root>
"""
import os
import runpy
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
sys.argv = ["app.main"]
runpy.run_module("app.main", run_name="__main__", alter_sys=True)
"""T-202 r7: round-6 major (D-073 rule 4) through the FULL pipeline at HEAD. SYNTHETIC variants of the sample:
  V1: the ER record's excerpt opens with its money sentence ('ER charges: $6,240. Dx: ...'); the record is a discharge summary, not a statement.
  V2: the PT visit-9 excerpt opens 'Payment plan discussed.' and carries its own charge sentence.
Expected by D-073 rule 4: '(record dated X)' on both. Prints each charge line and letter_check's verdict.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/label_repro_r7.py <archive_root>
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

SAMPLE = open("evals/golden/sample.txt", encoding="utf-8").read()
ER_OLD = "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."
ER_NEW = "ER charges: $6,240. Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
PT_OLD = "Discharged from PT after two missed appointments. Pain 3/10."
PT_NEW = "Payment plan discussed. Discharged from PT. Discharge visit 97110 charge $185.00."
assert SAMPLE.count(ER_OLD) == 1, "ER excerpt not found once"
assert SAMPLE.count(PT_OLD) == 1, "PT excerpt not found once"
VARIANTS = {
    "V1_er_summary_opens_with_charges": SAMPLE.replace(ER_OLD, ER_NEW),
    "V2_pt_note_opens_payment_plan": SAMPLE.replace(PT_OLD, PT_NEW),
}
for name, text in VARIANTS.items():
    got = LC.letters_for(text)
    v = got["all_accepted"]
    letter = v["letters"]["standard"]
    print(f"== {name}: accepted charge cents={v['charge_cents']}")
    for head, quote in LC.charge_lines(letter):
        print("   ", head, "| quote:", quote)
    print("    letter_check.charge_date_violations:", LC.charge_date_violations(letter, v["records"]))
"""T-202 r7: drive the running HEAD archive app over HTTP (the same routes the UI calls), accept every item the code lets a reviewer accept,
then read the export's letter text and check each BILLED CHARGES line with the same exact-form rule as check_letters_r7.py.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r7/live_letters_r7.py http://127.0.0.1:7987 <out_dir>
Writes <out_dir>/<case>-letter.txt and <out_dir>/<case>-items.json; prints a summary line per case.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE = sys.argv[1].rstrip("/")
OUT = os.path.abspath(sys.argv[2])
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "archive"))
CASES = {
    "sample": "evals/golden/sample.txt",
    "case_09": "evals/golden/case_09_nonvisit_hides_gap.txt",
    "lib10": "evals/library/case_lib10_eob_ub04_cms1500.txt",
    "lib11": "evals/library/case_lib11_priors_and_ledger.txt",
}
LINE = re.compile(r"^(?P<src>.+), date of service \[__________\] \((?P<kind>statement|record) dated [A-Z][a-z]+ \d{1,2}, \d{4}\)$")


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, raw


def walk_items(obj, found):
    """Collect {id, kind, review_status, ...} dicts from any list of items in the case JSON (kind in entry/amount/flag)."""
    if isinstance(obj, dict):
        if "id" in obj and obj.get("kind") in ("entry", "amount", "flag", "charge") and "review_status" in obj:
            found.append(obj)
        for v in obj.values():
            walk_items(v, found)
    elif isinstance(obj, list):
        for v in obj:
            walk_items(v, found)
    return found


def main():
    os.makedirs(OUT, exist_ok=True)
    summary = []
    for name, rel in CASES.items():
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        st, made = call("POST", "/api/cases", {"text": text, "title": f"r7 {name}"})
        if st != 201:
            summary.append({"case": name, "error": f"create {st}", "body": str(made)[:300]})
            continue
        token = made.get("token") or made.get("case", {}).get("token")
        st, run = call("POST", f"/api/cases/{token}/run", {})
        if st != 202:
            summary.append({"case": name, "error": f"run {st}", "body": str(run)[:300]})
            continue
        for _ in range(240):
            st, s = call("GET", f"/api/cases/{token}/status")
            if isinstance(s, dict) and s.get("status") not in ("running", None):
                break
            time.sleep(0.5)
        st, case = call("GET", f"/api/cases/{token}")
        items = list(case.get("entries", [])) + list(case.get("amounts", [])) + list(case.get("flags", []))
        accepted, refused = 0, []
        for it in items:
            if it.get("review_status") != "pending":
                continue
            st, r = call("POST", f"/api/cases/{token}/items/{it['id']}/review", {"action": "accept"})
            if st in (200, 201):
                accepted += 1
            else:
                refused.append((it["id"], it.get("kind"), st, (r or {}).get("error", {}).get("code") if isinstance(r, dict) and isinstance(r.get("error"), dict) else str(r)[:80]))
        st, ex = call("GET", f"/api/cases/{token}/export")
        letter = ex.get("letter_text") if isinstance(ex, dict) else None
        if letter is None and isinstance(ex, dict):
            letter = (ex.get("letter") or {}).get("text") if isinstance(ex.get("letter"), dict) else ex.get("letter")
        if not isinstance(letter, str):
            summary.append({"case": name, "error": f"export {st}", "keys": sorted(ex.keys()) if isinstance(ex, dict) else str(ex)[:200]})
            continue
        with open(os.path.join(OUT, f"{name}-letter.txt"), "w", encoding="utf-8") as f:
            f.write(letter)
        with open(os.path.join(OUT, f"{name}-items.json"), "w", encoding="utf-8") as f:
            json.dump({"accepted": accepted, "refused": refused, "items": len(items)}, f, indent=1)
        heads = [l for l in letter.splitlines() if re.search(r": \$[\d,]+\.\d\d$", l) and not l.startswith("Billed charges")]
        bad = [h for h in heads if not LINE.match(re.sub(r": \$[\d,]+\.\d\d$", "", h))]
        total = [l for l in letter.splitlines() if l.startswith("Billed charges")]
        summary.append({"case": name, "token": token, "items": len(items), "accepted": accepted, "refused": len(refused), "charge_lines": len(heads),
                        "charge_lines_not_exact_blank": bad, "total_line": total})
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:30.272Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8/archive && grep -rn \"ZLAYT_MODE\" app/config.py app/main.py | head -20; grep -n \"demo\" docs/RUNBOOK.md | head -20; ls; grep -n \"paste\\|409\" app/backend/routes*.py 2>/dev/null | head -20; ls app/backend | head -50"
}
````

### User / tool · 2026-11-03T15:13:30.377Z

**tool result**
````
app/config.py:35:        "local_mode": os.environ.get("ZLAYT_MODE") == "local",
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
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
__init__.py
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
case_list.py
charge_text.py
confidence.py
conflict_candidates.py
conflicts.py
count_charge.py
credibility.py
date_convention.py
dates.py
dismissal_patterns.py
encounter_types.json
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
limits.py
money.py
narrative.py
overlap.py
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
service_date.py
spanish.py
spanish_text.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:31.876Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8/archive && sed -n 20,60p app/config.py; grep -n \"demo_mode\\|local_mode\" -r app/backend/*.py | head -20; cat ../../T-202-paralegal-r7/server_7987.log | head -5; ls ../../T-202-paralegal-r7/live"
}
````

### User / tool · 2026-11-03T15:13:31.971Z

**tool result**
````
    backend = provider.backend_name()
    warnings = []
    if os.environ.get("ENABLE_LIVE") == "1" and not live:
        warnings.append("ENABLE_LIVE=1 but there is nothing to call (no ANTHROPIC_API_KEY, backend is not claude-cli): serving demo mode.")
    if os.environ.get("LLM_BACKEND") not in (None, "", "fixture") and os.environ.get("ENABLE_LIVE") != "1":
        warnings.append("LLM_BACKEND is set but ENABLE_LIVE is not 1: the fixture backend is used (no model call is possible).")
    if live and backend == "anthropic-api" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        warnings.append("Live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a spend limit at the provider first); the server will refuse to start.")
    return {
        "mode": "live" if live else "demo",
        "backend": backend,
        "fixture_set": os.environ.get("FIXTURE_SET", DEFAULTS["FIXTURE_SET"]) if backend == "fixture" else None,
        "host": os.environ.get("HOST", DEFAULTS["HOST"]),
        "port": int(os.environ.get("PORT", DEFAULTS["PORT"])),
        "anthropic_api_key": "set" if key_set else "not set",
        "local_mode": os.environ.get("ZLAYT_MODE") == "local",
        "warnings": warnings,
    }


def preflight() -> str | None:
    """One-line reason the server cannot start in the configured mode, or None. Called by app.main before create_app so a misconfigured
    live opt-in prints one line naming the variable instead of a traceback. The cap/host rules themselves stay in create_app (it still raises)."""
    from app.llm import provider
    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        return "live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)"
    if provider.backend_name() == "claude-cli" and importlib.util.find_spec("app.llm.backends.claude_cli") is None:
        return ("LLM_BACKEND=claude-cli is not available in this build (the Docker image does not ship the CLI backend, CONTRACT section 10): "
                "use LLM_BACKEND=anthropic-api, or unset ENABLE_LIVE for demo mode.")
    return None


def port_in_use(host: str, port: int) -> bool:
    """True when something is already listening on host:port (same SO_REUSEADDR setting uvicorn binds with)."""
    with socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
        except OSError:
            return True
    return False
app/backend/api.py:83:def local_mode() -> bool:
app/backend/api.py:105:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
app/backend/api.py:115:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
app/backend/api.py:127:    def demo_mode():
app/backend/api.py:221:            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
app/backend/api.py:266:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "local_mode": local_mode(), "answers": ans,
app/backend/api.py:272:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
app/backend/api.py:282:        if not local_mode():
app/backend/api.py:292:            if not local_mode():
app/backend/api.py:308:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
app/backend/api.py:309:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:352:        if demo_mode() and digest(text) not in allowed_hashes():
app/backend/api.py:353:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:358:            if (full := limits.case_full(c, local_mode())):          # T-183 r2: public demo stores at most DEMO_MAX_CASES
app/backend/api.py:361:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
app/backend/api.py:377:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
app/backend/api.py:390:            v = present.case_view(c, token, backend=backend(), models=present.models_for(c, token, config_models()), demo_mode=demo_mode())
app/backend/api.py:444:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
app/backend/api.py:445:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:446:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
Serving on http://127.0.0.1:7987  (Ctrl-C to stop)
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

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:36.988Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-202-paralegal-r8 && mkdir -p $E/live_demo $E/live_local && cp artifacts/review-evidence/T-202-paralegal-r7/serve_r7.py $E/serve_r8.py && cp artifacts/review-evidence/T-202-paralegal-r7/live_letters_r7.py $E/live_letters_r8.py && cp artifacts/review-evidence/T-202-paralegal-r7/label_repro_r7.py $E/label_repro_r8.py && cp artifacts/review-evidence/T-202-paralegal-r7/check_letters_r7.py $E/check_letters_r8.py && cp artifacts/review-evidence/T-202-paralegal-r7/run_letter_check_r7.py $E/run_letter_check_r8.py\nlsof -iTCP:7991 -iTCP:7992 -sTCP:LISTEN -nP; echo lsof=$?\n(env PORT=7991 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$PWD/$E/demo.db .venv/bin/python -I $E/serve_r8.py $E/archive > $E/server_7991.log 2>&1 &) \n(env PORT=7992 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$PWD/$E/local.db .venv/bin/python -I $E/serve_r8.py $E/archive > $E/server_7992.log 2>&1 &)\nsleep 6; curl -s localhost:7991/api/health | head -c 300; echo; curl -s localhost:7992/api/health | head -c 300; echo; lsof -iTCP:7991 -iTCP:7992 -sTCP:LISTEN -nP"
}
````

### User / tool · 2026-11-03T15:13:43.301Z

**tool result**
````
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  44861 arsis    9u  IPv4 0x603e54d72f21f3ff      0t0  TCP 127.0.0.1:7991 (LISTEN)
lsof=1
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":tr
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":tr
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  44861 arsis    9u  IPv4 0x603e54d72f21f3ff      0t0  TCP 127.0.0.1:7991 (LISTEN)
Python  93175 arsis    9u  IPv4 0xf5f37c43b4e99ab0      0t0  TCP 127.0.0.1:7992 (LISTEN)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:46.492Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-202-paralegal-r8 && cat $E/server_7991.log | tail -3; lsof -iTCP:7993 -sTCP:LISTEN -nP; echo lsof7993=$?\n(env PORT=7993 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$PWD/$E/demo.db .venv/bin/python -I $E/serve_r8.py $E/archive > $E/server_7993.log 2>&1 &)\nsleep 5; curl -s localhost:7993/api/health | head -c 200; echo; lsof -iTCP:7993 -sTCP:LISTEN -nP; ps -p 93175 -o pid,command | cut -c1-200"
}
````

### User / tool · 2026-11-03T15:13:51.751Z

**tool result**
````
error: port 7991 on 127.0.0.1 is already in use. Pick another with PORT=7870 (for example `PORT=7870 ./run.sh`).
lsof7993=1
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":false,"answers":"prepared","live_enable
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  93310 arsis    9u  IPv4 0xe33f2967dcc41db9      0t0  TCP 127.0.0.1:7993 (LISTEN)
  PID COMMAND
93175 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -I artifacts/review-evidence/T-202-paralegal-r8/serve_r8.py artifac
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:53.938Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8 && grep -n \"statement\" live_letters_r8.py check_letters_r8.py label_repro_r8.py"
}
````

### User / tool · 2026-11-03T15:13:54.021Z

**tool result**
````
live_letters_r8.py:23:LINE = re.compile(r"^(?P<src>.+), date of service \[__________\] \((?P<kind>statement|record) dated [A-Z][a-z]+ \d{1,2}, \d{4}\)$")
label_repro_r8.py:2:  V1: the ER record's excerpt opens with its money sentence ('ER charges: $6,240. Dx: ...'); the record is a discharge summary, not a statement.
check_letters_r8.py:6:  1. the line is EXACTLY '<source label>, date of service [__________] (statement|record dated <Month D, YYYY>)' (no other date-like text on the line);
check_letters_r8.py:8:  3. the kind word is 'statement' only for a bill (letter_check's own kind reader), 'record' otherwise;
check_letters_r8.py:35:LINE = re.compile(r"^(?P<src>.+), date of service \[__________\] \((?P<kind>statement|record) dated (?P<mon>[A-Z][a-z]+) (?P<day>\d{1,2}), (?P<yr>\d{4})\)$")
check_letters_r8.py:100:                kind_ok = (m.group("kind") == "statement") == (kind == "bill")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:00.939Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8 && python3 - <<'EOF'\nimport re\np='live_letters_r8.py'; s=open(p).read()\ns=s.replace(\"(?P<kind>statement|record) dated\",\"(?P<kind>record) dated\")\ns=s.replace('\"sample\": \"evals/golden/sample.txt\",\\n    \"case_09\"','\"sample\": \"evals/golden/sample.txt\",\\n    \"case_09\"')\n# add statement checks and case json dump, CASES from argv\ns=s.replace(\"\"\"        with open(os.path.join(OUT, f\"{name}-letter.txt\"), \"w\", encoding=\"utf-8\") as f:\n            f.write(letter)\"\"\",\"\"\"        with open(os.path.join(OUT, f\"{name}-letter.txt\"), \"w\", encoding=\"utf-8\") as f:\n            f.write(letter)\n        cj = json.dumps(case, ensure_ascii=False)\n        exj = json.dumps(ex, ensure_ascii=False)\n        with open(os.path.join(OUT, f\"{name}-case.json\"), \"w\", encoding=\"utf-8\") as f:\n            f.write(cj)\"\"\")\ns=s.replace(\"\"\"\\\"charge_lines_not_exact_blank\\\": bad,\"\"\",\"\"\"\\\"charge_lines_not_exact_blank\\\": bad, \\\"statement_in_letter\\\": letter.lower().count(\"statement dated\"), \\\"statement_in_case_json\\\": cj.lower().count(\"statement dated\"), \\\"statement_in_export_json\\\": exj.lower().count(\"statement dated\"),\"\"\")\ns=s.replace(\"\"\"CASES = {\"\"\",\"\"\"ONLY = os.environ.get(\"ONLY\")\nCASES = {\"\"\")\ns=s.replace(\"\"\"def call(method\"\"\",\"\"\"if ONLY:\n    CASES = {k: v for k, v in CASES.items() if k in ONLY.split(\",\")}\n\n\ndef call(method\"\"\",1)\nopen(p,'w').write(s)\np='check_letters_r8.py'; s=open(p).read()\ns=s.replace(\"(?P<kind>statement|record) dated\",\"(?P<kind>record) dated\")\ns=s.replace(\"\"\"kind_ok = (m.group(\"kind\") == \"statement\") == (kind == \"bill\")\"\"\",\"\"\"kind_ok = m.group(\"kind\") == \"record\" and \"statement\" not in head.lower()\"\"\")\nopen(p,'w').write(s)\nEOF\ngrep -n \"statement\" live_letters_r8.py check_letters_r8.py | head; grep -n \"_record_kind\\|kind\" check_letters_r8.py | head -20"
}
````

### User / tool · 2026-11-03T15:14:01.056Z

**tool result**
````
live_letters_r8.py:108:                        "charge_lines_not_exact_blank": bad, "statement_in_letter": letter.lower().count("statement dated"), "statement_in_case_json": cj.lower().count("statement dated"), "statement_in_export_json": exj.lower().count("statement dated"), "total_line": total})
check_letters_r8.py:6:  1. the line is EXACTLY '<source label>, date of service [__________] (statement|record dated <Month D, YYYY>)' (no other date-like text on the line);
check_letters_r8.py:8:  3. the kind word is 'statement' only for a bill (letter_check's own kind reader), 'record' otherwise;
check_letters_r8.py:100:                kind_ok = m.group("kind") == "record" and "statement" not in head.lower()
8:  3. the kind word is 'statement' only for a bill (letter_check's own kind reader), 'record' otherwise;
35:LINE = re.compile(r"^(?P<src>.+), date of service \[__________\] \((?P<kind>record) dated (?P<mon>[A-Z][a-z]+) (?P<day>\d{1,2}), (?P<yr>\d{4})\)$")
94:            rec_ok, kind_ok, src_ok = False, False, False
99:                kind = "bill" if LC._record_kind(r["source"], r["excerpt"]) == "bill" else "other"
100:                kind_ok = m.group("kind") == "record" and "statement" not in head.lower()
103:                   "kind_matches_record": kind_ok, "source_as_written": src_ok, "dates_on_line": dates_on_line}
105:            if not (ok_form and rec_ok and kind_ok and src_ok and hits):
166:            print(f"{c['case']} {r['variant']}: {r['head']}  | quote: {r['quote']}  | form={r['form_exact']} recdate={r['parenthetical_is_input_record_date']} kind={r['kind_matches_record']} src={r['source_as_written']}")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:05.327Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8 && python3 - <<'EOF'\np='check_letters_r8.py'; s=open(p).read()\ns=s.replace('''kind = \"bill\" if LC._record_kind(r[\"source\"], r[\"excerpt\"]) == \"bill\" else \"other\"\\n''','''kind = \"n/a\"\\n''')\ns=s.replace('''        if got[\"gate\"]:''','''        if \"statement dated\" in letter.lower() or \"statement\" in \" \".join(tail_lines[:0]).lower():\n            problems.append(f\"{name}/{variant}: 'statement dated' appears in the letter\")\n        if got[\"gate\"]:''',1)\nopen(p,'w').write(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && E=artifacts/review-evidence/T-202-paralegal-r8\n.venv/bin/python -I $E/run_letter_check_r8.py $E/archive > $E/letter_check.out 2>&1; echo exit=$?; cat $E/letter_check.out | tail -5\n.venv/bin/python -I $E/check_letters_r8.py $E/archive > $E/check_letters_r8.out 2>&1; echo exit=$?; head -c 600 $E/check_letters_r8.out; grep -c \"form=True recdate=True kind=True src=True\" $E/check_letters_r8.out; grep -c \"^TEETH\" $E/check_letters_r8.out; grep \"TEETH\\|PROBLEM\" $E/check_letters_r8.out | cut -c1-300"
}
````

### User / tool · 2026-11-03T15:14:20.835Z

**tool result**
````
exit=0
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
exit=1
{"archive": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8/archive", "charge_lines_checked": 19, "problems": 2, "teeth_all_rejected": true}
sample all_accepted: Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00  | quote: Source [Ex. __ / Bates __]: "ER charges: $6,240."  | form=True recdate=True kind=True src=True
sample all_accepted: Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00  | quote: Source [Ex. __ / Bates __]: "Charge: $2,150."  | form=True recdate=True kin17
8
TEETH {"case": "sample", "mutant": "printed DOS", "line": "Central ER discharge summary, date of service March 6, 2026 (record dated January 9, 2026): $6,240.00", "rejected": true, "reasons": 1}
TEETH {"case": "sample", "mutant": "wrong record date", "line": "Central ER discharge summary, date of service [__________] (record dated January 1, 2030): $6,240.00", "rejected": true, "reasons": 1}
TEETH {"case": "case_09", "mutant": "printed DOS", "line": "Hobbleton Family Clinic, billing statement, date of service March 6, 2026 (record dated March 1, 2026): $275.00", "rejected": true, "reasons": 1}
TEETH {"case": "case_09", "mutant": "wrong record date", "line": "Hobbleton Family Clinic, billing statement, date of service [__________] (record dated January 1, 2030): $275.00", "rejected": true, "reasons": 1}
TEETH {"case": "lib10", "mutant": "printed DOS", "line": "Saltmarrow General Hospital, UB-04 itemized bill, date of service March 6, 2026 (record dated June 19, 2026): $4,920.00", "rejected": true, "reasons": 1}
TEETH {"case": "lib10", "mutant": "wrong record date", "line": "Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (record dated January 1, 2030): $4,920.00", "rejected": true, "reasons": 1}
TEETH {"case": "lib11", "mutant": "printed DOS", "line": "Wexcombe Memorial ED, date of service March 6, 2026 (record dated March 18, 2026): $3,260.00", "rejected": true, "reasons": 1}
TEETH {"case": "lib11", "mutant": "wrong record date", "line": "Wexcombe Memorial ED, date of service [__________] (record dated January 1, 2030): $3,260.00", "rejected": true, "reasons": 1}
PROBLEM case_09/all_accepted: bad charge line: 'Hobbleton Family Clinic, billing statement, date of service [__________] (record dated March 1, 2026): $275.00' quote='Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."' row={'case': 'case_09', 'variant': 'all_accepted', 'head': 'H
PROBLEM case_09/counted: bad charge line: 'Hobbleton Family Clinic, billing statement, date of service [__________] (record dated March 1, 2026): $275.00' quote='Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."' row={'case': 'case_09', 'variant': 'counted', 'head': 'Hobbleton F
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:24.744Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-202-paralegal-r8 && python3 - <<'EOF'\np='artifacts/review-evidence/T-202-paralegal-r8/check_letters_r8.py'; s=open(p).read()\ns=s.replace('\"statement\" not in head.lower()','\"statement dated\" not in head.lower()')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -I $E/check_letters_r8.py $E/archive > $E/check_letters_r8.out 2>&1; echo exit=$?; head -1 $E/check_letters_r8.out; grep -c \"form=True recdate=True kind=True src=True\" $E/check_letters_r8.out; grep -c \"PROBLEM\" $E/check_letters_r8.out; grep -ci \"statement dated\" $E/check_letters_r8.out\nONLY=sample,case_09 .venv/bin/python -I $E/live_letters_r8.py http://127.0.0.1:7993 $E/live_demo > $E/live_demo_summary.out 2>&1; echo exit=$?; cat $E/live_demo_summary.out\n.venv/bin/python -I $E/live_letters_r8.py http://127.0.0.1:7992 $E/live_local > $E/live_local_summary.out 2>&1; echo exit=$?; cat $E/live_local_summary.out"
}
````

### User / tool · 2026-11-03T15:14:33.728Z

**tool result**
````
exit=0
{"archive": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8/archive", "charge_lines_checked": 19, "problems": 0, "teeth_all_rejected": true}
19
0
0
exit=0
[
 {
  "case": "sample",
  "token": "lqfL69hSQO5lfj5wLy7Cow",
  "items": 23,
  "accepted": 23,
  "refused": 0,
  "charge_lines": 2,
  "charge_lines_not_exact_blank": [],
  "statement_in_letter": 0,
  "statement_in_case_json": 0,
  "statement_in_export_json": 0,
  "total_line": [
   "Billed charges accepted from these records: $8,390.00"
  ]
 },
 {
  "case": "case_09",
  "token": "8NeboLcXEu9Uj1F1oht1ZQ",
  "items": 7,
  "accepted": 6,
  "refused": 1,
  "charge_lines": 1,
  "charge_lines_not_exact_blank": [],
  "statement_in_letter": 0,
  "statement_in_case_json": 0,
  "statement_in_export_json": 0,
  "total_line": [
   "Billed charges accepted from these records: $275.00"
  ]
 }
]
exit=0
[
 {
  "case": "sample",
  "token": "OgoN66h8zzI-4ysnYrkzjw",
  "items": 23,
  "accepted": 23,
  "refused": 0,
  "charge_lines": 2,
  "charge_lines_not_exact_blank": [],
  "statement_in_letter": 0,
  "statement_in_case_json": 0,
  "statement_in_export_json": 0,
  "total_line": [
   "Billed charges accepted from these records: $8,390.00"
  ]
 },
 {
  "case": "case_09",
  "token": "6t7gThHRGw0F1qaMH_Ye9g",
  "items": 7,
  "accepted": 6,
  "refused": 1,
  "charge_lines": 1,
  "charge_lines_not_exact_blank": [],
  "statement_in_letter": 0,
  "statement_in_case_json": 0,
  "statement_in_export_json": 0,
  "total_line": [
   "Billed charges accepted from these records: $275.00"
  ]
 },
 {
  "case": "lib10",
  "token": "nEB2T6iB2yUMVP5gORqzzQ",
  "items": 22,
  "accepted": 15,
  "refused": 7,
  "charge_lines": 4,
  "charge_lines_not_exact_blank": [],
  "statement_in_letter": 0,
  "statement_in_case_json": 0,
  "statement_in_export_json": 0,
  "total_line": [
   "Billed charges accepted from these records: $8,123.50"
  ]
 },
 {
  "case": "lib11",
  "token": "KxK9zEcBLvDoMUGRQHjetw",
  "items": 29,
  "accepted": 19,
  "refused": 10,
  "charge_lines": 1,
  "charge_lines_not_exact_blank": [],
  "statement_in_letter": 0,
  "statement_in_case_json": 0,
  "statement_in_export_json": 0,
  "total_line": [
   "Billed charges accepted from these records: $3,260.00"
  ]
 }
]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:37.174Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-202-paralegal-r8 && grep -rn \"Billed charges\" $E/archive/evals/golden/sample.export.expected.txt $E/archive/spec/REQUIREMENTS.md $E/archive/memory/ORCHESTRATOR_DECISIONS.md | cut -c1-250 | head; for c in demo:sample demo:case_09 local:sample local:case_09 local:lib10 local:lib11; do d=${c%%:*}; n=${c##*:}; echo \"== $c\"; grep -E \": \\\\\\$[0-9,]+\\.[0-9]{2}$\" $E/live_$d/$n-letter.txt | grep -v \"^Billed\"; done"
}
````

### User / tool · 2026-11-03T15:14:37.309Z

**tool result**
````
artifacts/review-evidence/T-202-paralegal-r8/archive/evals/golden/sample.export.expected.txt:47:Billed charges accepted from these records: $8,390.00
artifacts/review-evidence/T-202-paralegal-r8/archive/memory/ORCHESTRATOR_DECISIONS.md:12:| D-004 | *(Partly superseded: guarded charge reclassification reinstated by D-042 (T-084); totals replaced by a cited line listing, D-052.)* Amounts: code extra
artifacts/review-evidence/T-202-paralegal-r8/archive/memory/ORCHESTRATOR_DECISIONS.md:27:| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**,
artifacts/review-evidence/T-202-paralegal-r8/archive/memory/ORCHESTRATOR_DECISIONS.md:70:| D-062 | The letter total states what it is (2026-11-02, T-140 after 3 adversarial rounds). R-EX-8's line becomes `Billed charges accepted from these records: $
artifacts/review-evidence/T-202-paralegal-r8/archive/spec/REQUIREMENTS.md:74:### 1.4 Billed charges
artifacts/review-evidence/T-202-paralegal-r8/archive/spec/REQUIREMENTS.md:126:| R-EX-8 | **The total line is exactly** `Billed charges accepted from these records: $X` (D-019, wording per D-062), where X is the sum of accepted `charge` amounts, forma
artifacts/review-evidence/T-202-paralegal-r8/archive/spec/REQUIREMENTS.md:265:Billed charges accepted from these records: $8,390.00
== demo:sample
Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00
Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00
== demo:case_09
Hobbleton Family Clinic, billing statement, date of service [__________] (record dated March 1, 2026): $275.00
== local:sample
Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00
Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00
== local:case_09
Hobbleton Family Clinic, billing statement, date of service [__________] (record dated March 1, 2026): $275.00
== local:lib10
Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (record dated June 19, 2026): $4,920.00
Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (record dated June 19, 2026): $2,105.00
Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (record dated June 19, 2026): $386.50
Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (record dated June 19, 2026): $712.00
== local:lib11
Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026): $3,260.00
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:41.342Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8/archive && python3 - <<'EOF'\nimport re\nfor f,keys in [(\"evals/golden/sample.txt\",[\"ER charges: $6,240\",\"Charge: $2,150\"]),(\"evals/golden/case_09_nonvisit_hides_gap.txt\",[\"$275\"]),(\"evals/library/case_lib10_eob_ub04_cms1500.txt\",[\"$4,920\",\"$2,105\",\"$386.50\",\"$712\"]),(\"evals/library/case_lib11_priors_and_ledger.txt\",[\"$3,260\"])]:\n    t=open(f).read()\n    for b in re.split(r\"\\n=== Record \\d+ ===\\n\",t)[1:]:\n        for k in keys:\n            if k in b:\n                print(f.split('/')[-1][:22], k, re.search(r\"^Date:\\s*(\\S+)\",b,re.M).group(1), '|', re.search(r\"^Source:\\s*(.+)$\",b,re.M).group(1))\nEOF"
}
````

### User / tool · 2026-11-03T15:14:41.441Z

**tool result**
````
sample.txt ER charges: $6,240 2026-01-09 | Central ER discharge summary
sample.txt Charge: $2,150 2026-05-29 | Austin Imaging, cervical MRI
case_09_nonvisit_hides $275 2026-03-01 | Hobbleton Family Clinic, billing statement
case_lib10_eob_ub04_cm $4,920 2026-06-19 | Saltmarrow General Hospital, UB-04 itemized bill
case_lib10_eob_ub04_cm $2,105 2026-06-19 | Saltmarrow General Hospital, UB-04 itemized bill
case_lib10_eob_ub04_cm $386.50 2026-06-19 | Saltmarrow General Hospital, UB-04 itemized bill
case_lib10_eob_ub04_cm $712 2026-06-19 | Saltmarrow General Hospital, UB-04 itemized bill
case_lib11_priors_and_ $3,260 2026-03-18 | Wexcombe Memorial ED
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:44.710Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-202-paralegal-r8 && .venv/bin/python -I $E/label_repro_r8.py $E/archive > $E/label_repro_r8.out 2>&1; cat $E/label_repro_r8.out; grep -rIn \"statement dated\" $E/archive/app $E/archive/evals/*.py | cut -c1-200; ls artifacts/review-evidence/*/*step3* artifacts/review-evidence/*/*.py 2>/dev/null | grep -i \"step\\|pw\\|play\" | head"
}
````

### User / tool · 2026-11-03T15:14:46.114Z

**tool result**
````
== V1_er_summary_opens_with_charges: accepted charge cents=[624000, 215000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | quote: ER charges: $6,240.
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | quote: Charge: $2,150.
    letter_check.charge_date_violations: []
== V2_pt_note_opens_payment_plan: accepted charge cents=[624000, 18500, 215000]
    Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00 | quote: ER charges: $6,240.
    Capital PT, visit 9, date of service [__________] (record dated March 6, 2026): $185.00 | quote: Discharge visit 97110 charge $185.00.
    Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00 | quote: Charge: $2,150.
    letter_check.charge_date_violations: []
artifacts/review-evidence/GATE-M3M4-verify-staff/step3-end.png
artifacts/review-evidence/T-060-pass1/p4-stepper.py
artifacts/review-evidence/T-060-pass1/p5-stepper-open.py
artifacts/review-evidence/T-134/judges_step134.py
artifacts/review-evidence/T-134/steps134.py
artifacts/review-evidence/T-168/probe_r2_lenient_and_steps.py
artifacts/review-evidence/T-181-paralegal-r2/05-step3-done.png
artifacts/review-evidence/T-181-paralegal-r2/lib-step3-done.png
artifacts/review-evidence/T-181-paralegal/19-step3-done.png
artifacts/review-evidence/T-181-paralegal/32-lib-step3-done.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:49.250Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-181-paralegal-r2/ | head -30; grep -n \"step3\\|Step 3\\|data-testid\" artifacts/review-evidence/T-181-paralegal-r2/*.py | head -40"
}
````

### User / tool · 2026-11-03T15:14:49.340Z

**tool result**
````
01-home.png
02-step1.png
03-after-draft.png
04-step2-done.png
05-step3-done.png
06-step4.png
07-bates-blank.png
08-bates-typed-preview.png
09-bates-saved.png
draft-T-181-paralegal-r2.md
h.py
letter-clipboard.txt
letter-download.txt
letter-with-bates.txt
lib-s2-00-e1.png
lib-s2-05-e2.png
lib-s2-08-e4.png
lib-s2-19-e9.png
lib-s3-00-a1.png
lib-s3-01-a2.png
lib-s3-02-a3.png
lib-s3-03-a4.png
lib-s3-04-a5.png
lib-s3-05-a6.png
lib-s3-06-a7.png
lib-s3-07-a8.png
lib-step2-done.png
lib-step3-done.png
lib-step4.png
lib11-letter.txt
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:4:pg.wait_for_selector("[data-testid=view][data-ready]")
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:5:pg.click("[data-testid=btn-continue]")
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:6:pg.wait_for_selector("[data-testid=letter-text]", timeout=15000)
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:8:panel = pg.locator("[data-testid=cfg-panel]")
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:12:pg.click("[data-testid=cfg-exhibit]")
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:14:log("PREVIEW after exhibit only:", pg.inner_text("[data-testid=cfg-preview]"))
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:15:pg.click("[data-testid=cfg-bates-prefix]")
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:17:log("PREVIEW after prefix:", pg.inner_text("[data-testid=cfg-preview]"))
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:18:pg.click("[data-testid=cfg-bates-start]")
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:20:log("PREVIEW after start 101:", pg.inner_text("[data-testid=cfg-preview]"))
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:23:pg.click("[data-testid=btn-save-cfg]")
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:25:log("cfg-error:", pg.inner_text("[data-testid=cfg-error]") if pg.query_selector("[data-testid=cfg-error]") else None)
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:26:txt = pg.inner_text("[data-testid=letter-text]")
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:34:pg.wait_for_selector("[data-testid=letter-text]", timeout=15000)
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:36:log("after reload has RIVERA0101:", "RIVERA0101" in pg.inner_text("[data-testid=letter-text]"))
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:37:log("after reload PREVIEW:", pg.inner_text("[data-testid=cfg-preview]"))
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:40:    pg.fill(f"[data-testid={t}]", "")
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:41:pg.click("[data-testid=btn-save-cfg]")
artifacts/review-evidence/T-181-paralegal-r2/r02_bates.py:43:log("after clearing: letter has [Ex. __ / Bates __]:", "[Ex. __ / Bates __]" in pg.inner_text("[data-testid=letter-text]"), "| PREVIEW:", pg.inner_text("[data-testid=cfg-preview]"))
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:2:Step 3 ledger lines (dispute direction, date column), Step 4 letter lines for the counted undated ledger amounts.
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:8:pg.wait_for_selector("[data-testid=view][data-ready]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:9:pg.click("[data-testid=tile-library]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:11:pg.check("[data-testid=library-case_lib11_priors_and_ledger]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:12:pg.click("[data-testid=btn-read]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:13:pg.wait_for_selector("[data-testid=btn-draft]", timeout=20000)
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:16:pg.click("[data-testid=btn-draft]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:24:    pg.wait_for_selector("[data-testid=view][data-ready]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:38:    outs = pg.evaluate("() => Array.from(document.querySelectorAll('[data-testid=outside-word]')).map(m => m.innerText)")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:39:    note = pg.evaluate("() => { const u = document.querySelector('[data-testid=outside-note]'); return u ? u.innerText : null }")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:40:    unc = pg.evaluate("() => { const u = document.querySelector('[data-testid=uncovered]'); return u ? u.innerText.replace(/\\n/g, ' / ') : null }")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:41:    yes = pg.query_selector("[data-testid=answer-yes]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:43:    cmp_box = pg.query_selector("[data-testid=check-compare]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:58:        log("  after A on refused: focus", pg.evaluate("() => document.activeElement.getAttribute('data-testid') || document.activeElement.tagName"),
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:67:pg.click("[data-testid=btn-next-step]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:68:pg.wait_for_selector("[data-testid=view][data-ready]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:76:    boxes = [b.get_attribute("data-testid") for b in pg.query_selector_all("input[type=checkbox]") if b.is_visible()]
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:92:shot("lib-step3-done", full=True)
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:95:pg.wait_for_selector("[data-testid=letter-text]", timeout=15000)
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:98:    pg.click("[data-testid=btn-download-letter]")
artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py:101:    pg.click("[data-testid=btn-download-notes]")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:49.962Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8/archive && ls app/frontend app/frontend/guided | head -40; grep -n \"record dated\\|dateLine\\|recLabel\\|stmtOnly\" app/frontend/guided/step3.js | head -20"
}
````

### User / tool · 2026-11-03T15:14:50.054Z

**tool result**
````
app/frontend:
api.js
app.js
audit.js
batch.js
charges.js
dev
dom.js
excerpt.js
export.js
exportcfg.js
flags.js
guided
index.html
input.js
judges.js
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
overview.css
overview.js
review.css
review.js
sections.js
sidebyside.css
sidebyside.js
source.js
state.js
stepper.css
stepper.js
styles.css
suggestions.css
suggestions.js
switcher.js
timeline.js
tokens.css
uncovered.css
uncovered.js
20:  const stmtOnly = (sd) => !!sd && !!sd.statement_date_iso && !(sd.state === "stated" && sd.date_iso === sd.statement_date_iso && !sd.end_iso);      // a bill's date, not the day of the service
23:  const stmtDated = (item, sd, rec) => stmtOnly(sd) || (!sd && !!item && (kindOf(item) === "count" || BILL_DOC.test((rec && rec.source_label) || "")));
24:  /* D-075 (T-202 r7): the record's own date is always called "record dated"; the app never classifies a source as a bill or a clinical record. */
27:  const recLabel = (r, st) => `Record ${r.seq} · ${r.source_label || "Record"} · ${recDate(r, st)}`;
33:  const dateLine = (sd) => h("p", { class: "svc-date gap-top", "data-testid": "service-date", "data-state": sd.state },
35:    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · ${dateWord(sd)} dated ${R.longDate(sd.statement_date_iso)}`) : null);
39:    const paren = /\(record dated/.test((sd && sd.text) || ""), stmt = paren ? " The date in parentheses is the record date, not the service date." : "";
48:    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, stmtDated(item, sd, r) && dateWord(sd)) : null }));
49:    const src = { head: many ? "Records " + recs.slice(0, -1).map((r) => r.seq).join(", ") + " and " + recs[recs.length - 1].seq : rec ? recLabel(rec, st) : "", nodes: srcNodes };
68:        body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), sd ? dateLine(sd) : null, h("p", { class: "explain muted gap-top" }, "Written in the record as ", h("b", {}, item.text || ""), "."), note],
128:      return d && /^reviewer:counted/.test(by || "") ? `No date of service (record dated ${d})` : d;          // a ledger line she counted states no date of service
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:52.022Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2 && cat h.py | head -40; sed -n 1,25p r03_lib11.py; sed -n 60,95p r03_lib11.py"
}
````

### User / tool · 2026-11-03T15:14:52.109Z

**tool result**
````
"""T-181 paralegal review helper: persistent Chromium profile on the archive app (9ab8cae r2, demo mode, port 7941).

Usage: .venv/bin/python -I artifacts/review-evidence/T-181-paralegal/h.py <step-script.py>
The step script gets `pg` (page), `shot(name)`, `dump(label)`, `log(...)`, `BASE`, `OUT` in its globals.
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7941")
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
PROFILE = os.path.join(OUT, os.environ.get("T181_PROFILE", "profile"))
LOG = os.path.join(OUT, "run.log")


def main(script):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE, headless=True, viewport={"width": 1440, "height": 900})
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        errors = []
        pg.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        pg.on("response", lambda r: errors.append(f"http {r.status} {r.request.method} {r.url}") if r.status >= 400 else None)
        logf = open(LOG, "a")

        def log(*a):
            s = " ".join(str(x) for x in a)
            print(s)
            logf.write(s + "\n")
            logf.flush()

        def shot(name, full=False):
            path = os.path.join(OUT, name + ".png")
            pg.screenshot(path=path, full_page=full)
            log("[shot]", path)

        def dump(label=""):
            pg.wait_for_timeout(250)
            t = pg.evaluate("() => document.body.innerText")
"""T-181 r2: lib11 (priors and ledger) on the local-mode copy. Step 2 disputed lines (grey box label, underlined outside words),
Step 3 ledger lines (dispute direction, date column), Step 4 letter lines for the counted undated ledger amounts.
Run: T181_BASE=http://127.0.0.1:7942 T181_PROFILE=profile-local .venv/bin/python -I .../h.py .../r03_lib11.py
"""
import re
T0 = time.time()
pg.goto(BASE + "/new")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.click("[data-testid=tile-library]")
pg.wait_for_timeout(300)
pg.check("[data-testid=library-case_lib11_priors_and_ledger]")
pg.click("[data-testid=btn-read]")
pg.wait_for_selector("[data-testid=btn-draft]", timeout=20000)
pg.wait_for_timeout(300)
dump("lib11 records")
pg.click("[data-testid=btn-draft]")
for i in range(80):
    pg.wait_for_timeout(250)
    if pg.query_selector("text=Go to step 2") or "/timeline" in pg.url:
        break
log("draft took", round(time.time() - T0, 1), "s")
if "/timeline" not in pg.url:
    pg.get_by_text("Go to step 2").first.click()
    pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(500)
        pg.keyboard.press("d")
    else:
        pg.keyboard.press("a")
    pg.wait_for_timeout(450)
dump("lib11 step 2 done")
shot("lib-step2-done", full=True)

pg.click("[data-testid=btn-next-step]")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(500)
n = 0
for step in range(15):
    i = iid()
    if not i or "/bills" not in pg.url:
        break
    right = pg.evaluate("() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }")
    boxes = [b.get_attribute("data-testid") for b in pg.query_selector_all("input[type=checkbox]") if b.is_visible()]
    log(f"######## bills {n} item={i} boxes={boxes}")
    log("CARD:", right.replace("\n", " / "))
    shot(f"lib-s3-{n:02d}-{i}")
    n += 1
    if boxes:
        pg.keyboard.press("a"); pg.wait_for_timeout(200)
        for _ in boxes:
            pg.keyboard.press("Space"); pg.wait_for_timeout(200)
            pg.keyboard.press("a"); pg.wait_for_timeout(300)
            if iid() != i:
                break
    else:
        pg.keyboard.press("a")
    pg.wait_for_timeout(450)
dump("lib11 step 3 done")
shot("lib-step3-done", full=True)

pg.get_by_text("Go to step 4").first.click()
pg.wait_for_selector("[data-testid=letter-text]", timeout=15000)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:54.795Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && sed -n 1,12p T-181-paralegal-r2/r02_bates.py; ls T-181-paralegal-r2/*.py T-181-paralegal/*.py | head; grep -n \"tile-sample\\|btn-sample\\|goto\" T-181-paralegal/*.py | head"
}
````

### User / tool · 2026-11-03T15:14:54.902Z

**tool result**
````
"""T-181 r2: Step 4 Bates panel wording, live preview, save, letter cites, reload. Sample case (the one finished by r01)."""
import re
pg.goto(BASE + "/")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.click("[data-testid=btn-continue]")
pg.wait_for_selector("[data-testid=letter-text]", timeout=15000)
pg.wait_for_timeout(600)
panel = pg.locator("[data-testid=cfg-panel]")
panel.scroll_into_view_if_needed()
log("PANEL (blank):\n" + panel.inner_text())
shot("07-bates-blank")
pg.click("[data-testid=cfg-exhibit]")
T-181-paralegal-r2/h.py
T-181-paralegal-r2/r01_sample_e2e.py
T-181-paralegal-r2/r02_bates.py
T-181-paralegal-r2/r03_lib11.py
T-181-paralegal/api_e1.py
T-181-paralegal/check_letter.py
T-181-paralegal/h.py
T-181-paralegal/s01_home.py
T-181-paralegal/s02_open_sample.py
T-181-paralegal/s03_draft.py
T-181-paralegal/s01_home.py:2:pg.goto(BASE + "/")
T-181-paralegal/s03_draft.py:1:pg.goto(BASE + "/")
T-181-paralegal/s02_open_sample.py:2:pg.goto(BASE + "/")
T-181-paralegal/s04_step2_first.py:1:pg.goto(BASE + "/")
T-181-paralegal/s07_step2_finish.py:17:pg.goto(BASE + "/")
T-181-paralegal/s05_catalogue.py:2:pg.goto(BASE + "/")
T-181-paralegal/s06_step2_pass.py:21:pg.goto(BASE + "/")
T-181-paralegal/s08_step3_catalogue.py:2:pg.goto(BASE + "/")
T-181-paralegal/s11_new_case.py:1:pg.goto(BASE + "/")
T-181-paralegal/s09_step3_pass_and_letter.py:17:pg.goto(BASE + "/")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:14:56.151Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2 && cat r01_sample_e2e.py | head -80; sed -n 40,80p h.py"
}
````

### User / tool · 2026-11-03T15:14:56.234Z

**tool result**
````
"""T-181 r2: sample case end to end, timed, keyboard-first. Home -> Open the sample -> Draft -> Step 2 -> Step 3 -> Step 4 -> downloads.
Run: T181_BASE=http://127.0.0.1:7941 .venv/bin/python -I artifacts/review-evidence/T-181-paralegal-r2/h.py artifacts/review-evidence/T-181-paralegal-r2/r01_sample_e2e.py
"""
import re, json
T0 = time.time()
C = {"keys": 0, "clicks": 0}
ctx.grant_permissions(["clipboard-read", "clipboard-write"], origin=BASE)

def T():
    return round(time.time() - T0, 1)

def item_id():
    m = re.search(r"item=([^&]+)", pg.url)
    return m.group(1) if m else None

def info(label):
    pg.wait_for_timeout(300)
    title = pg.evaluate("() => (document.querySelector('.titlebar') || {innerText:''}).innerText").replace("\n", " | ")
    acts = pg.evaluate("() => (document.querySelector('.actions') || {innerText:''}).innerText").replace("\n", " | ")
    ae = pg.evaluate("() => { const a = document.activeElement; return a ? a.tagName + '[' + (a.getAttribute('data-testid')||'') + ']' : null }")
    log(f"[{T()}s] {label} item={item_id()} | {title[-60:]} | ACT: {acts[:220]} | focus {ae}")

def card(n):
    iid = item_id()
    right = pg.evaluate("() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }")
    src = pg.evaluate("() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[0].innerText.split('\\n').slice(0,2).join(' | ') : '' }")
    marks = pg.evaluate("() => Array.from(document.querySelectorAll('mark')).map(m => m.innerText)")
    outs = pg.evaluate("() => Array.from(document.querySelectorAll('[data-testid=outside-word]')).map(m => m.innerText)")
    unc = pg.evaluate("() => { const u = document.querySelector('[data-testid=uncovered]'); return u ? u.innerText : null }")
    log(f"######## {n} item={iid} t={T()}s")
    log("SRC:", src)
    log("CARD:", right.replace("\n", " / "))
    log("MARKS:", marks)
    log("OUTSIDE-WORDS:", outs, "| UNCOVERED:", unc)
    shot(f"s2-{n:02d}-{iid}")

def key(k, label=None):
    C["keys"] += 1
    pg.keyboard.press(k)
    info(label or k)

def tab_to(prefix):
    for i in range(8):
        pg.keyboard.press("Tab"); C["keys"] += 1
        ae = pg.evaluate("() => (document.activeElement.innerText||'').trim()")
        if ae.startswith(prefix):
            return True
    log("could not tab to", prefix)
    return False

# ---- Home -> Open the sample case
pg.goto(BASE + "/")
pg.wait_for_selector("[data-testid=view][data-ready]")
dump("home first visit")
shot("01-home")
pg.get_by_role("button", name="Open the sample case").click(); C["clicks"] += 1
pg.wait_for_selector("[data-testid=btn-draft]", timeout=20000)
pg.wait_for_timeout(300)
log(f"[{T()}s] step 1 shown")
dump("step 1 records")
shot("02-step1")
TD = time.time()
pg.click("[data-testid=btn-draft]"); C["clicks"] += 1
for i in range(120):
    pg.wait_for_timeout(250)
    if pg.query_selector("text=Go to step 2") or "/timeline" in pg.url:
        break
log(f"[{T()}s] draft took {round(time.time()-TD,1)}s")
dump("after draft")
shot("03-after-draft")
if "/timeline" not in pg.url:
    pg.get_by_text("Go to step 2").first.click(); C["clicks"] += 1
    pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(400)
if not item_id():
    btn = pg.query_selector("text=Start") or pg.query_selector("[data-testid=btn-first-undecided]")
    if btn:
        btn.click(); C["clicks"] += 1
        pg.wait_for_timeout(400)
info("step 2 first item")
            t = pg.evaluate("() => document.body.innerText")
            log(f"===== {label} url={pg.url}")
            log(t)
            log("=====")
            return t

        g = {"pg": pg, "shot": shot, "dump": dump, "log": log, "BASE": BASE, "OUT": OUT, "time": time, "ctx": ctx}
        log(f"### run {os.path.basename(script)} at {time.strftime('%H:%M:%S')}")
        try:
            exec(compile(open(script).read(), script, "exec"), g)
        finally:
            if errors:
                log("ERRORS:\n  " + "\n  ".join(errors))
            ctx.close()
            logf.close()


if __name__ == "__main__":
    main(sys.argv[1])
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:15:09.633Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8/ui_step3_r8.py",
 "content": "\"\"\"T-202 r8: drive the real UI (Chromium) through Step 1 -> 4 on an archive app and collect every visible text on Step 3 (/bills) and the Step 4 letter.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r8/ui_step3_r8.py <base_url> <case: sample|lib10|lib11|case09> <out_prefix>\nWrites <out_prefix>-step3.txt (every Step 3 card text), <out_prefix>-letter.txt (Step 4 letter), <out_prefix>-step3.png.\nPrints counts of 'statement dated' / 'statement date' / 'record dated' and the charge lines.\n\"\"\"\nimport re\nimport sys\nimport time\nfrom playwright.sync_api import sync_playwright\n\nbase, case, prefix = sys.argv[1].rstrip(\"/\"), sys.argv[2], sys.argv[3]\nLIB = {\"lib10\": \"case_lib10_eob_ub04_cms1500\", \"lib11\": \"case_lib11_priors_and_ledger\"}\n\n\ndef iid(pg):\n    m = re.search(r\"item=([^&]+)\", pg.url)\n    return m.group(1) if m else None\n\n\nwith sync_playwright() as p:\n    b = p.chromium.launch(headless=True)\n    pg = b.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    errs = []\n    pg.on(\"pageerror\", lambda e: errs.append(str(e)))\n    pg.goto(base + \"/\")\n    pg.wait_for_selector(\"[data-testid=view][data-ready]\")\n    if case == \"sample\":\n        pg.get_by_role(\"button\", name=\"Open the sample case\").click()\n    else:\n        pg.goto(base + \"/new\")\n        pg.wait_for_selector(\"[data-testid=view][data-ready]\")\n        pg.click(\"[data-testid=tile-library]\")\n        pg.wait_for_timeout(300)\n        pg.check(f\"[data-testid=library-{LIB[case]}]\")\n        pg.click(\"[data-testid=btn-read]\")\n    pg.wait_for_selector(\"[data-testid=btn-draft]\", timeout=20000)\n    pg.click(\"[data-testid=btn-draft]\")\n    for _ in range(160):\n        pg.wait_for_timeout(250)\n        if pg.query_selector(\"text=Go to step 2\") or \"/timeline\" in pg.url:\n            break\n    if \"/timeline\" not in pg.url:\n        pg.get_by_text(\"Go to step 2\").first.click()\n        pg.wait_for_selector(\"[data-testid=view][data-ready]\")\n    pg.wait_for_timeout(500)\n    if not iid(pg):\n        btn = pg.query_selector(\"text=Start\") or pg.query_selector(\"[data-testid=btn-first-undecided]\")\n        if btn:\n            btn.click()\n            pg.wait_for_timeout(400)\n    for _ in range(80):\n        if \"/timeline\" not in pg.url or not iid(pg):\n            break\n        pg.keyboard.press(\"a\")\n        pg.wait_for_timeout(350)\n    if pg.query_selector(\"[data-testid=btn-next-step]\"):\n        pg.click(\"[data-testid=btn-next-step]\")\n        pg.wait_for_selector(\"[data-testid=view][data-ready]\")\n        pg.wait_for_timeout(500)\n    texts = []\n    for n in range(40):\n        if \"/bills\" not in pg.url or not iid(pg):\n            break\n        body = pg.evaluate(\"() => document.body.innerText\")\n        texts.append(f\"##### step3 item {iid(pg)} url={pg.url}\\n{body}\")\n        if n == 0:\n            pg.screenshot(path=prefix + \"-step3.png\", full_page=True)\n        cur = iid(pg)\n        boxes = [x for x in pg.query_selector_all(\"input[type=checkbox]\") if x.is_visible()]\n        if boxes:\n            pg.keyboard.press(\"a\")\n            pg.wait_for_timeout(200)\n            for _ in boxes:\n                pg.keyboard.press(\"Space\")\n                pg.wait_for_timeout(200)\n                pg.keyboard.press(\"a\")\n                pg.wait_for_timeout(300)\n                if iid(pg) != cur:\n                    break\n        else:\n            pg.keyboard.press(\"a\")\n        pg.wait_for_timeout(450)\n    texts.append(\"##### step3 end\\n\" + pg.evaluate(\"() => document.body.innerText\"))\n    open(prefix + \"-step3.txt\", \"w\").write(\"\\n\".join(texts))\n    nxt = pg.get_by_text(\"Go to step 4\")\n    if nxt.count():\n        nxt.first.click()\n        pg.wait_for_selector(\"[data-testid=letter-text]\", timeout=15000)\n        pg.wait_for_timeout(500)\n        letter = pg.inner_text(\"[data-testid=letter-text]\")\n        open(prefix + \"-letter.txt\", \"w\").write(letter)\n        full = pg.evaluate(\"() => document.body.innerText\")\n        open(prefix + \"-step4page.txt\", \"w\").write(full)\n    else:\n        letter, full = \"\", \"\"\n    s3 = \"\\n\".join(texts)\n    print(case, \"url\", pg.url)\n    print(\"step3 'statement dated':\", len(re.findall(r\"statement dated\", s3, re.I)), \"| 'statement date':\", len(re.findall(r\"statement date\", s3, re.I)),\n          \"| 'record dated':\", len(re.findall(r\"record dated\", s3, re.I)))\n    print(\"step4 page 'statement dated':\", len(re.findall(r\"statement dated\", full, re.I)), \"| letter 'statement dated':\", len(re.findall(r\"statement dated\", letter, re.I)))\n    for l in letter.splitlines():\n        if re.search(r\": \\$[\\d,]+\\.\\d\\d$\", l) and not l.startswith(\"Billed\"):\n            print(\"CHARGE LINE:\", l)\n    print(\"pageerrors:\", errs)\n    b.close()\n"
}
````

### User / tool · 2026-11-03T15:15:09.732Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8/ui_step3_r8.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:15:12.118Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-202-paralegal-r8 && .venv/bin/python -I $E/ui_step3_r8.py http://127.0.0.1:7993 sample $E/ui_demo_sample > $E/ui_demo_sample.out 2>&1; cat $E/ui_demo_sample.out | tail -12\n.venv/bin/python -I $E/ui_step3_r8.py http://127.0.0.1:7992 lib10 $E/ui_local_lib10 > $E/ui_local_lib10.out 2>&1; tail -10 $E/ui_local_lib10.out\n.venv/bin/python -I $E/ui_step3_r8.py http://127.0.0.1:7992 lib11 $E/ui_local_lib11 > $E/ui_local_lib11.out 2>&1; tail -10 $E/ui_local_lib11.out"
}
````

### User / tool · 2026-11-03T15:16:26.959Z

**tool result**
````
sample url http://127.0.0.1:7993/case/UfzsdWH4_z1qvIVcbbySLg/letter
step3 'statement dated': 0 | 'statement date': 0 | 'record dated': 8
step4 page 'statement dated': 0 | letter 'statement dated': 0
CHARGE LINE: Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00
CHARGE LINE: Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00
pageerrors: []
lib10 url http://127.0.0.1:7992/case/H9oq98Dm4DOoNNHMbzq6lg/timeline?item=e1
step3 'statement dated': 0 | 'statement date': 0 | 'record dated': 0
step4 page 'statement dated': 0 | letter 'statement dated': 0
pageerrors: []
lib11 url http://127.0.0.1:7992/case/MD1I7Ca6Ik-LbeWct-Sc4A/timeline?item=e1
step3 'statement dated': 0 | 'statement date': 0 | 'record dated': 0
step4 page 'statement dated': 0 | letter 'statement dated': 0
pageerrors: []
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:16:32.614Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-202-paralegal-r8 && sed -n 40,70p artifacts/review-evidence/T-181-paralegal-r2/r03_lib11.py | head -30; python3 - <<'EOF'\np='/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8/ui_step3_r8.py'; s=open(p).read()\ns=s.replace('''        pg.keyboard.press(\"a\")\n        pg.wait_for_timeout(350)\n    if pg.query_selector(\"[data-testid=btn-next-step]\")''','''        before = iid(pg)\n        pg.keyboard.press(\"a\")\n        pg.wait_for_timeout(350)\n        if iid(pg) == before and \"/timeline\" in pg.url:\n            pg.keyboard.press(\"d\")\n            pg.wait_for_timeout(350)\n    if pg.query_selector(\"[data-testid=btn-next-step]\")''')\nopen(p,'w').write(s)\nEOF"
}
````

### User / tool · 2026-11-03T15:16:32.720Z

**tool result**
````
    unc = pg.evaluate("() => { const u = document.querySelector('[data-testid=uncovered]'); return u ? u.innerText.replace(/\\n/g, ' / ') : null }")
    yes = pg.query_selector("[data-testid=answer-yes]")
    yd = yes.is_disabled() if yes else None
    cmp_box = pg.query_selector("[data-testid=check-compare]")
    log(f"######## {n} item={i} yes_disabled={yd} compare_box={bool(cmp_box)}")
    log("CARD:", right.replace("\n", " / "))
    log("MARKS:", marks)
    log("OUTSIDE-WORDS:", outs, "| NOTE:", note)
    log("UNCOVERED:", unc)
    if cmp_box or yd:
        shot(f"lib-s2-{n:02d}-{i}")
    n += 1
    if cmp_box:
        pg.keyboard.press("a"); pg.wait_for_timeout(200)
        pg.keyboard.press("Space"); pg.wait_for_timeout(200)
        pg.keyboard.press("a")
    elif yd:
        pg.keyboard.press("a"); pg.wait_for_timeout(250)
        log("  after A on refused: focus", pg.evaluate("() => document.activeElement.getAttribute('data-testid') || document.activeElement.tagName"),
            "| msg:", pg.evaluate("() => (document.querySelector('.actions') || {innerText:''}).innerText").replace("\n", " | ")[-200:])
        pg.keyboard.press("d")
    else:
        pg.keyboard.press("a")
    pg.wait_for_timeout(450)
dump("lib11 step 2 done")
shot("lib-step2-done", full=True)

pg.click("[data-testid=btn-next-step]")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(500)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:16:35.402Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-202-paralegal-r8 && for c in lib10 lib11; do .venv/bin/python -I $E/ui_step3_r8.py http://127.0.0.1:7992 $c $E/ui_local_$c > $E/ui_local_$c.out 2>&1; tail -9 $E/ui_local_$c.out; done"
}
````

### User / tool · 2026-11-03T15:17:13.775Z

**tool result**
````
lib10 url http://127.0.0.1:7992/case/eW7Mp2Rk6bGlCB5I4NwRUQ/letter
step3 'statement dated': 0 | 'statement date': 0 | 'record dated': 30
step4 page 'statement dated': 0 | letter 'statement dated': 0
CHARGE LINE: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (record dated June 19, 2026): $4,920.00
CHARGE LINE: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (record dated June 19, 2026): $2,105.00
CHARGE LINE: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (record dated June 19, 2026): $386.50
CHARGE LINE: Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (record dated June 19, 2026): $712.00
pageerrors: []
lib11 url http://127.0.0.1:7992/case/UuBKxN7zF-mQL7LTFJExpg/letter
step3 'statement dated': 0 | 'statement date': 7 | 'record dated': 21
step4 page 'statement dated': 0 | letter 'statement dated': 0
CHARGE LINE: Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026): $3,260.00
CHARGE LINE: Fennimoor Spine Clinic, itemized ledger, date of service [__________] (record dated June 15, 2026): $250.00
CHARGE LINE: Fennimoor Spine Clinic, itemized ledger, date of service [__________] (record dated June 15, 2026): $180.00
CHARGE LINE: Fennimoor Spine Clinic, itemized ledger, date of service [__________] (record dated June 15, 2026): $2,310.00
pageerrors: []
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:17:15.690Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8 && grep -n -i \"statement date\" ui_local_lib11-step3.txt | cut -c1-300; grep -n -i \"statement\" ui_local_lib11-step3.txt | grep -vi \"statement date\" | cut -c1-200 | head"
}
````

### User / tool · 2026-11-03T15:17:15.787Z

**tool result**
````
110:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under lette
181:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under lette
252:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under lette
323:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under lette
392:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under lette
461:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under lette
529:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under lette
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:17:18.263Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8 && grep -n -i \"record dated\" ui_demo_sample-step3.txt | sort -u -k2 | cut -c1-330 | head -6; grep -n -i \"record dated\" ui_local_lib11-step3.txt | cut -d: -f2- | sort | uniq -c | cut -c1-330"
}
````

### User / tool · 2026-11-03T15:17:18.360Z

**tool result**
````
319:$2,150.00	Austin Imaging, cervical MRI	date of service [__________] (record dated May 29, 2026)	Change
318:$6,240.00	Central ER discharge summary	date of service [__________] (record dated January 9, 2026)	Change
35:Record 2 · Central ER discharge summary · record dated January 9, 2026
106:Record 8 · Austin Imaging, cervical MRI · record dated May 29, 2026
52:Central ER discharge summary · record dated January 9, 2026
123:Austin Imaging, cervical MRI · record dated May 29, 2026
   1 $180.00	Fennimoor Spine Clinic, itemized ledger	date of service [__________] (record dated June 15, 2026)	Change
   1 $2,310.00	Fennimoor Spine Clinic, itemized ledger	date of service [__________] (record dated June 15, 2026)	Change
   1 $250.00	Fennimoor Spine Clinic, itemized ledger	date of service [__________] (record dated June 15, 2026)	Change
   1 $3,260.00	Wexcombe Memorial ED	date of service [__________] (record dated March 18, 2026)	Change
   7 Fennimoor Spine Clinic, itemized ledger · record dated June 15, 2026
   1 Record 3 · Wexcombe Memorial ED · record dated March 18, 2026
   7 Record 9 · Fennimoor Spine Clinic, itemized ledger · record dated June 15, 2026
   1 Wexcombe Memorial ED · record dated March 18, 2026
   1 date of service [__________] (record dated March 18, 2026)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:17:25.777Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-202-paralegal-r8 && cat > $E/teeth_statement_r8.py <<'EOF'\n\"\"\"T-202 r8: letter_check must reject '(statement dated X)' on any charge line (D-075: always 'record dated'). Run with -I: <archive_root>\"\"\"\nimport os, sys, logging\nroot = os.path.abspath(sys.argv[1]); sys.path.insert(0, root); os.chdir(root)\nos.environ.setdefault(\"LLM_BACKEND\", \"fixture\"); os.environ.setdefault(\"FIXTURE_SET\", \"curated\"); logging.disable(logging.CRITICAL)\nfrom evals import letter_check as LC\nfor name, path in [(\"sample\",\"evals/golden/sample.txt\"),(\"case_09\",\"evals/golden/case_09_nonvisit_hides_gap.txt\"),(\"lib10\",\"evals/library/case_lib10_eob_ub04_cms1500.txt\"),(\"lib11\",\"evals/library/case_lib11_priors_and_ledger.txt\")]:\n    res = LC.letters_for(open(path, encoding=\"utf-8\").read())[\"all_accepted\"]\n    letter = res[\"letters\"][\"standard\"]\n    base = LC.charge_date_violations(letter, res[\"records\"])\n    mut = letter.replace(\"(record dated\", \"(statement dated\", 1)\n    v = LC.charge_date_violations(mut, res[\"records\"])\n    print(f\"{name}: unmutated violations={base}; mutant 'statement dated' rejected={bool(v)} ({len(v)})\")\nEOF\n.venv/bin/python -I $E/teeth_statement_r8.py $E/archive > $E/teeth_statement_r8.out 2>&1; cat $E/teeth_statement_r8.out"
}
````

### User / tool · 2026-11-03T15:17:28.258Z

**tool result**
````
sample: unmutated violations=[]; mutant 'statement dated' rejected=True (1)
case_09: unmutated violations=[]; mutant 'statement dated' rejected=True (1)
lib10: unmutated violations=[]; mutant 'statement dated' rejected=True (1)
lib11: unmutated violations=[]; mutant 'statement dated' rejected=True (1)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:17:32.009Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8 && grep -n \"from the quote\" live_*/*-letter.txt | cut -c1-260; grep -n \"treatment visits 1 through 14\" live_local/lib11-letter.txt | cut -c1-260; grep -n -i \"statement\" live_local/lib11-letter.txt live_demo/sample-letter.txt | cut -c1-200; grep -n \"28\\b\" ../../../memory/SCOPE_CUTS.md | head -3; cd /Users/arsis/zlayt-pm-project; git diff --stat cd7fd27 HEAD | tail -2; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-03T15:17:32.164Z

**tool result**
````
26:| debt | T-014 accepted with documented debt after 3 rounds (§7.4) | 5 consistency majors, 0 blockers after 3 rounds; split to T-028 which T-017 depends on | see card | M1 |
33:| debt | T-028 accepted with documented debt after 2 rounds (§7.4) | remaining major (golden export byte test) is T-041 AC2 and T-038 spec-vs-golden check; minors (README-arch v1 names, confirm_date warning) carried to M2 backend cards | see card | M1 |
78:| debt | T-112 accepted with documented debt after 3 rounds (§7.4) | 3 rounds; the D-054 trimmer is vocabulary-bound, so it misses some abbreviations (fresh probes: 12/43 faithful pairs over-trimmed to the tray, 9/30 unsupported clauses kept). Both directions are safe: over-trim is visible in the tray and the human recovers it; kept clauses still face judge 1 and the human. On 188 recorded outputs the trim never fires on English. | Fragments and surviving mutants: T-128. Full coverage would need an LLM-free clinical abbreviation resource; ~1-2 days. | M3 (T-128) |
 memory/SCOPE_CUTS.md             | 2 +-
 5 files changed, 6 insertions(+), 3 deletions(-)
304ba58
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:17:34.551Z

**tool call — Bash**
````
{
 "command": "git diff --name-only cd7fd27 HEAD; git diff --stat cd7fd27 HEAD -- app evals tests | tail -1; grep -n \"2,310\\|Fennimoor\" artifacts/review-evidence/T-202-paralegal-r8/live_local/lib11-letter.txt | cut -c1-300"
}
````

### User / tool · 2026-11-03T15:17:34.670Z

**tool result**
````
docs/LLM_VS_CODE.md
memory/LESSONS.md
memory/ORCHESTRATOR_DECISIONS.md
memory/PROGRESS.md
memory/SCOPE_CUTS.md
7:March 27, 2026 — Fennimoor Spine Clinic, new patient
11:March 27, 2026 — Fennimoor Spine Clinic, new patient intake form (OCR text)
15:April 24, 2026 — Fennimoor Spine Clinic, visit 8
19:May 29, 2026 — Fennimoor Spine Clinic, visit 14
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:17:37.943Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8 && grep -n \"2,310\\|from the quote\\|Internal review\" ui_local_lib11-letter.txt | cut -c1-330; grep -n \"from the quote\" ui_*-letter.txt | wc -l; grep -c \"from the quote\" ui_demo_sample-step3.txt; grep -n \"Take the date\\|fill it\" ui_demo_sample-letter.txt | cut -c1-250 | head -3"
}
````

### User / tool · 2026-11-03T15:17:38.051Z

**tool result**
````
31:Fennimoor Spine Clinic, itemized ledger, date of service [__________] (record dated June 15, 2026): $2,310.00
32:Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"
       0
0
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:17:40.627Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r8 && grep -n -i \"date of service\\|quote\" live_demo/sample-letter.txt | cut -c1-300"
}
````

### User / tool · 2026-11-03T15:17:40.711Z

**tool result**
````
41:Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00
43:Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:17:45.494Z

**tool call — Bash**
````
{
 "command": "kill 93175 93310; sleep 2; lsof -iTCP:7992 -iTCP:7993 -sTCP:LISTEN -nP; echo lsof=$?; curl -s -o /dev/null -w \"%{http_code}\\n\" localhost:7992/api/health; curl -s -o /dev/null -w \"%{http_code}\\n\" localhost:7993/api/health; cd /Users/arsis/zlayt-pm-project; git rev-parse --short HEAD; git rev-parse cd7fd27^{tree}; grep -c \"\" artifacts/review-evidence/T-202-paralegal-r8/check_letters_r8.out; head -1 artifacts/review-evidence/T-202-paralegal-r8/letter_check.out"
}
````

### User / tool · 2026-11-03T15:17:47.709Z

**tool result**
````
lsof=1
000
000
304ba58
487a191a8b26728bd84e4bc0c4c1b48e77b5a67b
28
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:18:15.182Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r8.md",
 "content": "# T-202 round 8 (D-075, cd7fd27): paralegal review (Maria Delgado, senior PI paralegal)\n\n**Verdict: pass.** The round-7 blocker is closed. Every charge line in the sample, case_09, lib10 and lib11 letters reads exactly `<source as written>, date of service [__________] (record dated <Month D, YYYY>)`. Each date is the record's own Date header in the input. \"statement dated\" appears nowhere in a letter, in the Step 3 screens or in the app code. `python -m evals.letter_check` reports 0 over 25 cases. My r7 probe (an ER discharge summary whose excerpt opens \"ER charges:\") now prints \"(record dated January 9, 2026)\". The kind classifier I blocked in r7 is gone, so there is no label rule left to get wrong. One minor carried from r7 remains (finding 1).\n\n**Pin.** `git archive cd7fd27` (tree 487a191a8b26) extracted to `artifacts/review-evidence/T-202-paralegal-r8/archive`. HEAD moved to 304ba58 during the review. `git diff --name-only cd7fd27 HEAD` lists only docs/LLM_VS_CODE.md and memory/*.md, and `git diff --stat cd7fd27 HEAD -- app evals tests` is empty, so the results apply to HEAD.\n\n**Servers.** Demo mode on 127.0.0.1:7993 (health: local_mode false), PID 93310. Local mode on 127.0.0.1:7992 (local_mode true), PID 93175. Both were killed, and lsof exit 1 with curl 000 on each port. Port 7991 was already held by another process before I started, so I did not use or touch it.\n\n**Checks.**\n- Charge lines over HTTP: 3 in demo mode (sample 2, case_09 1) and 8 in local mode (sample 2, case_09 1, lib10 4, lib11 1). All match the exact blank form. \"statement dated\" count in the letter, the case JSON and the export JSON is 0 for every case. Totals: $8,390.00, $275.00, $8,123.50, $3,260.00.\n- Charge lines in the UI, through Step 1 to Step 4 (Chromium, keyboard accept): sample (demo), lib10 and lib11 (local). Letter lines are exact. Step 3 shows `date of service [__________] (record dated ...)` on each charge row. \"statement dated\" count is 0 in Step 3 and Step 4. The 7 \"statement date\" hits in lib11 Step 3 are the record's own quoted words: `Itemized ledger, statement date 06/15/2026`.\n- Record dates, checked by a parse of the INPUT text by my script: sample ER 2026-01-09, MRI 2026-05-29; case_09 2026-03-01; lib10 2026-06-19 on all 4 lines; lib11 ED 2026-03-18. 19 in-process charge lines (accepted-all and counted variants): form exact, date equal to the input header, source as written, 0 problems.\n- Teeth: a printed \"date of service March 6, 2026\" and a wrong record date are rejected in all four cases (8 of 8). A \"(statement dated X)\" mutant is rejected by `letter_check.charge_date_violations` in all four cases (4 of 4).\n- r7 probe `label_repro_r8.py`: V1 (ER summary opening \"ER charges: $6,240.\") prints \"(record dated January 9, 2026)\". V2 (PT visit opening \"Payment plan discussed.\", quote \"Discharge visit 97110 charge $185.00.\") prints \"(record dated March 6, 2026)\". `charge_date_violations` is [] on both.\n\n**Verify-quickly score (4).** Each amount and its quote check in one step. The date in parentheses is the record's own date and matches the header. The date of service is a blank the paralegal fills herself, which is honest. It is a manual lookup on every charge, so I do not score 5.\n\n**Model.** This review ran on claude-sonnet-5-5, the model I am running as. My definition expects claude-opus-5-5 for judgment reviews. See questions_for_chris.\n\n**Not exercised.** The case_09 Step 3 UI screens (the demo offers only the sample case in the UI; case_09 was checked through the HTTP API and the in-process letter, including the case JSON). Timeline entries beyond reaching Step 3, and the full 25-case corpus label count. The lib11 ledger lines were counted in the UI (the 3 Fennimoor lines are in the UI letter) and in-process, not over HTTP.\n\n```json\n{\"card\": \"T-202\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive cd7fd27 (tree 487a191a8b26728bd84e4bc0c4c1b48e77b5a67b) extracted to artifacts/review-evidence/T-202-paralegal-r8/archive; HEAD moved to 304ba58 (docs and memory only, app/evals/tests diff empty); demo-mode app at http://127.0.0.1:7993 (PID 93310) and local-mode app at http://127.0.0.1:7992 (PID 93175), LLM_BACKEND=fixture FIXTURE_SET=curated; both stopped (lsof exit 1, curl 000). Cases: sample, case_09, lib10, lib11 (SYNTHETIC inputs from evals/golden and evals/library). Evidence: artifacts/review-evidence/T-202-paralegal-r8/.\",\n \"exercised\": [\n  \"Read personas/paralegal.md (live dossier), reviews/T-202-paralegal-r7.md (blocker), my memory notes for r7 and run pitfalls, board.py show T-202 (r7 findings and the D-075 handoff), memory/ORCHESTRATOR_DECISIONS.md D-073 and D-075\",\n  \"git rev-parse --short HEAD: cd7fd27 at the start, 304ba58 at the end; git diff --name-only cd7fd27 HEAD: docs/LLM_VS_CODE.md, memory/LESSONS.md, memory/ORCHESTRATOR_DECISIONS.md, memory/PROGRESS.md, memory/SCOPE_CUTS.md; git diff --stat cd7fd27 HEAD -- app evals tests: empty\",\n  \"git archive cd7fd27 | tar -x into artifacts/review-evidence/T-202-paralegal-r8/archive (tree 487a191a8b26728bd84e4bc0c4c1b48e77b5a67b)\",\n  \"run_letter_check_r8.py (python -m evals.letter_check, with -I against the archive): {\\\"value\\\": 0, \\\"cases\\\": 25, \\\"held_out_entries\\\": 11, \\\"backend\\\": \\\"fixture\\\"}, exit 0 (letter_check.out)\",\n  \"check_letters_r8.py on the archive (sample, case_09, lib10, lib11 through evals.letter_check.letters_for, accepted-all and counted): 19 charge lines, each exact form with kind 'record', parenthetical date equal to the input Date header (parsed by this script from the raw text), source as written, 'statement dated' absent from every letter; problems 0; exit 0; 8 teeth mutants (printed DOS, wrong record date) all rejected (check_letters_r8.out)\",\n  \"teeth_statement_r8.py: a '(record dated' to '(statement dated' mutant is rejected by letter_check.charge_date_violations in all four cases (teeth_statement_r8.out)\",\n  \"Demo-mode server on 127.0.0.1:7993 and local-mode server on 127.0.0.1:7992 from the archive (serve_r8.py with -I); live_letters_r8.py over HTTP (create, run, status, accept every pending entry, amount and flag, GET export): demo sample and case_09, local sample, case_09, lib10 and lib11; every charge line is the exact blank; statement-dated counts 0 in letter, case JSON and export JSON (live_demo_summary.out, live_local_summary.out, live_demo/, live_local/)\",\n  \"ui_step3_r8.py in Chromium through the real UI (Open the sample case or library tile, Draft, Step 2 keyboard accept, Step 3, Step 4): demo sample, local lib10, local lib11; Step 3 and Step 4 'statement dated' counts 0; Step 3 rows read 'date of service [__________] (record dated ...)'; letter charge lines exact (ui_demo_sample.out, ui_local_lib10.out, ui_local_lib11.out, *-step3.txt, *-letter.txt, ui_demo_sample-step3.png and the other -step3.png files)\",\n  \"label_repro_r8.py (the r7 probe: V1 ER summary opening 'ER charges:', V2 PT visit opening 'Payment plan discussed'): both print '(record dated ...)' and charge_date_violations is [] (label_repro_r8.out)\",\n  \"grep -rIn 'statement dated' on archive/app and archive/evals/*.py: no hits\",\n  \"Not exercised: case_09 Step 3 UI, timeline entries beyond reaching Step 3, the 25-case corpus label count, lib11 ledger lines over HTTP\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"verify_quickly\": 4, \"letter_dates_correct\": 5, \"blank_label_correct\": 5, \"adversarial_dates_correct\": 5},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from rounds 6-7: a 14-visit ledger charge still prints a single 'date of service' blank\",\n   \"evidence\": \"ui_local_lib11-letter.txt:31-32: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (record dated June 15, 2026): $2,310.00' with quote 'treatment visits 1 through 14 charge $2,310.00'. check_letters_r8.out holds the same line for the counted lib11 variant.\",\n   \"why_it_matters\": \"One date blank over 14 visits asks the paralegal for one date for a range, and the quote gives none. The exact form is pinned in letter_check, so this is a spec choice, not a defect in the code. It does not print a wrong fact. Under D-075 item 1 this is accepted debt for SCOPE_CUTS, so I rate it minor and do not ask for a round.\",\n   \"fix\": \"Record the choice in SCOPE_CUTS: either allow 'dates of service [__________]' for a quote that counts visits (D-073 and letter_check change together), or note in the internal review notes that the line covers 14 visits.\",\n   \"acceptance_test\": \"The lib11 $2,310.00 line prints the plural form, or its notes line says it covers 14 visits; letter_check accepts only the chosen form.\"}\n ],\n \"whats_right\": [\n  \"Every charge line is the same exact blank with the record's own date, equal to the input Date header on all 19 in-process and 11 live lines, and 'statement dated' appears nowhere in a letter, Step 3 or the app code.\",\n  \"The r7 label blocker is gone for good: removing the bill-versus-record classifier means no wording rule can misname a discharge summary, and letter_check rejects a '(statement dated X)' mutant in all four cases.\",\n  \"Totals still match the accepted charges ($8,390.00, $275.00, $8,123.50, $3,260.00), and the blank never prints a service date, so no date of service is invented.\"\n ],\n \"questions_for_chris\": [\n  \"Model: this review ran on claude-sonnet-5-5, the model I am running as. CLAUDE.md section 6 and my dossier expect claude-opus-5-5 for judgment reviews. Does the T-202 close-out need an Opus re-run?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-03T15:18:15.320Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r8.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:18:17.124Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re,json\nt=open('reviews/T-202-paralegal-r8.md').read()\nb=re.findall(r\"```json\\n(.*?)\\n```\",t,re.S); print(len(b)); d=json.loads(b[0]); print(d['verdict'],[f['severity'] for f in d['findings']])\nEOF\npython3 tools/board.py validate 2>&1 | tail -3; ls artifacts/review-evidence/T-202-paralegal-r8/live_local | head -3"
}
````

### User / tool · 2026-11-03T15:18:17.307Z

**tool result**
````
1
pass ['minor']
ok (218 file(s))
case_09-case.json
case_09-items.json
case_09-letter.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:18:19.598Z

Pass: in cd7fd27 every charge line in the sample, case_09, lib10 and lib11 letters reads "date of service [__________] (record dated X)" with X equal to the record's own date, "statement dated" appears nowhere, letter_check reports 0 over 25 cases, and my r7 probe now prints "record dated". The one finding is a minor carry-over (the 14-visit ledger line keeps a single date blank). My two servers are stopped. The review is in `/Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r8.md` (ran as claude-sonnet-5-5, not the expected Opus).
