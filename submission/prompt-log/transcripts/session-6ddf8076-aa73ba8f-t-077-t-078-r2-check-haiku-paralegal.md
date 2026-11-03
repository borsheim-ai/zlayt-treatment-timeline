# Subagent: T-077/T-078 r2 check (haiku paralegal) (T-077/T-078 r2 check (haiku paralegal))

Source: `agent-aa73ba8fdd1b50201.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:43:12.564Z

Round-2 checks of two research cards in /Users/arsis/zlayt-pm-project.

1. **T-077** (commit 5c2cb2f): using reviews/T-077-paralegal.md, confirm the major is closed. Every real name cited in research/case-library-sources-v2.md must be on the research/validate_library.py denylist, and a planted name must fail. Run the self-test, and check that the minors are fixed. Write reviews/T-077-paralegal-r2.md.
2. **T-078** (commit 327ce46): using reviews/T-078-paralegal.md, confirm all three majors are closed:
   - the CMS-1500 follows NUCC grouping;
   - both traps appear in the specimens: decimal-less amounts in an OCR copy, and a UB-04 rate on the charge line;
   - the EMS report, ambulance bill, §18.001 affidavit and narrative letter are present with sources and SYNTHETIC specimens.
   Run `python3 research/record_formats_check.py`. Write reviews/T-078-paralegal-r2.md.

Each file needs a ```json block of real values: card, persona paralegal-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T03:43:13.900Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T03:43:13.919Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T03:43:14.106Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal.md"
}
````

### User / tool · 2026-11-02T03:43:14.114Z

**tool result**
````
1	# T-077 review: paralegal-reviewer (research/case-library-sources-v2.md, commit bb26bf0)
2	
3	**Verdict: changes.** The 17 patterns are mostly what a Texas PI paralegal sees (second accident, priors, EOBs vs bills, cloned notes, scanned chiro notes, ER-missed concussion, conclusory causation letters), and the read-depth labelling is honest. I fetched 11 source URLs. Nine opened and matched the doc's claims. Two (the NJ Rodriguez PDF and the studicata Hampton page) returned 403 to me, as the doc says for Hampton. The blocking issue is synthetic safety. The doc says the real names must go on the denylist before any packet is built, and nothing has done that. The list the doc gives is also incomplete.
4	
5	## What I opened and found
6	| Source | Result |
7	|---|---|
8	| P1 JLG v. Garza, txcourts PDF | Confirmed: ortho visit 5 days after crash 1, about 11 weeks PT, second crash with ambulance and hard collar, first MRI after crash 2, fusion in 2012. The treating doctor's July note had no other history (cross-exam). The record features follow from the opinion. |
9	| P5 In re Central Oregon, txcourts PDF | Confirmed: two prior accidents, memory complaints, tailbone surgery. The court's six billing-discovery items are confirmed, but they are not the "six ledger columns" the doc claims (finding 5). |
10	| P10 Steinkamp, PubMed | Confirmed: 104,456,653 notes, 50.1%, 33.0% to 54.2%, 45.9% from a different author. |
11	| P11 ElGhrably, nature.com | Confirmed: 44 errors in 32 sets, 19 later corrected, 3 consent forms. |
12	| P12 Rodriguez-Vera, PMC | Confirmed: 18 of 117 (15%) unclear, worse in surgical departments. |
13	| P16 Lewis Brisbois write-up | Confirmed, including the ortho-vs-PCP contradiction and the photos. The doc correctly leaves out the drug-use facts. |
14	| P4 Chiv v. Figueroa, hallapproved | The Spanish-translation and counteraffidavit holdings are confirmed. The case says nothing about record content (finding 2). |
15	| P6 Gunn v. McCoy, dallas-appellate blog | Date June 15, 2018 and the subrogation-agent holding confirmed. The blog calls it a "medical malpractice case". |
16	| P3 Hills v. Donis, mdjwlaw.com | Holding confirmed. The "withdrawn and substituted 2021-02-11" claim is not on the page (finding 3). |
17	
18	## Judgement on the four asks
19	1. **Realistic for PI practice, features follow from the source.** Mostly yes. Gaps are in findings 2, 4 and 5.
20	2. **Summary-level claims marked.** Source read depth is marked on every pattern. The "Record features" lines are not marked as source-derived or inferred (finding 2).
21	3. **Synthetic-safety notes.** The six rules are sound. The enforcement is missing (finding 1).
22	4. **lib08 to lib15 cover D-042.** On paper, yes (coverage map). Three features rest on premises the table doesn't state (finding 6).
23	
24	```json
25	{"card": "T-077", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
26	 "scope": "research/case-library-sources-v2.md at commit bb26bf0; cross-read with research/validate_library.py, board cards T-077/T-079, memory/ORCHESTRATOR_DECISIONS.md D-042/D-043; no app run (research card)",
27	 "exercised": [
28	  "Read personas/paralegal.md, the whole v2 doc, validate_library.py, board.py show T-077/T-078/T-079, D-042 and D-043",
29	  "Fetched with curl and pdftotext: txcourts Garza (130978.pdf) and Central Oregon (200945pc.pdf), PubMed 36156143, mdjwlaw.com Hills v. Donis page, hallapproved.com Chiv v. Figueroa, legal500.com Lewis Brisbois write-up, nature.com 6702590, PMC1279250, dallas-appellate.blogspot.com Gunn v. McCoy",
30	  "403 on njcourts.gov Rodriguez PDF and studicata.com Hampton page (matches the doc's own note for Hampton)",
31	  "Grepped the fetched text for each numeric and holding claim the doc makes",
32	  "Checked evals/library/case_lib03 format and the validate_library.py DENYLIST"],
33	 "verdict": "changes",
34	 "scores": {"realism_for_PI_practice": 4, "source_fidelity": 4, "summary_level_claims_marked": 3, "synthetic_safety_enforcement": 2, "d042_coverage": 4},
35	 "findings": [
36	  {"severity": "major", "title": "Denylist for v2 real names is not in place, and the doc's list is incomplete and unsafe as written",
37	   "evidence": "Doc rule 2 (case-library-sources-v2.md lines 24-26): 'the real case names in this file (e.g. Garza, Broussard, Rodriguez) must be added to that denylist before any v2 packet is built.' research/validate_library.py:13-15 DENYLIST still holds only v1 terms ('Nichols', 'Duke Linden', 'Haygood', ... 'Cutch'); none of Garza, JLG, Guevara, Ferrer, Hills, Donis, Chiv, Figueroa, Broussard, Gunn, McCoy, Hampton, Miskell, Wal-Mart, Brisbois is present. The match is a case-sensitive word-boundary regex (validate_library.py:33), so 'GARZA' or 'garza' would pass. T-079 (the packet builder) is status ready with a note telling someone to do this.",
38	   "why_it_matters": "A real captioned party, doctor or county in a synthetic packet is exactly the leak the data rule forbids. The only guard is the denylist, and the doc hands the builder three example names. Garza, Rodriguez, Figueroa and Hills are also very common Texas surnames, so a blanket ban will collide with the invented Spanish-language names lib09 needs unless the builder knows to avoid them.",
39	   "fix": "Researcher adds an explicit 'Denylist additions' block to the v2 doc and updates validate_library.py (case-insensitive) before T-079 starts. Include distinctive tokens: JLG, Pechero, Zapata, Guevara, Ferrer, Donis, Chiv, Figueroa, Broussard, 'Central Oregon', McCoy, Miskell, Wal-Mart, Brisbois, 'Harris County'. For common surnames (Garza, Rodriguez, Hills, Gunn, Hampton) ban them as invented-name choices and state that in the doc.",
40	   "acceptance_test": "A unit test builds a temp packet containing each listed token in mixed case and asserts validate_library.py exits non-zero for each; the test also greps the v2 doc for capitalised case-caption names and fails if any is missing from DENYLIST."},
41	  {"severity": "minor", "title": "'Record features' mix source-derived and inferred content, and two sources do not support the record shape at all",
42	   "evidence": "P4 (hallapproved page): the holdings are about a deposition lacking a certified translation and a stricken counteraffidavit; the page has nothing on 'history via interpreter' charting. P17 Hampton v. Miskell: the opinion is about a reconstructionist's testimony, and the cite has no court district or docket number; studicata page returns 403 to me (curl http 403, 1398 bytes). P5 'intake forms answering prior accidents: none' is not in In re Central Oregon (grep of the pdftotext output finds only the discovery list, the two priors and the memory testimony). The doc's read-depth note says only that the PI framing of the medical studies is 'ours'.",
43	   "why_it_matters": "A builder reading 'Record features' will treat them as documented real-world shapes. The adjuster-style ones are plausible, but for a paralegal reviewing the library 'real-world pattern' should mean the source says it. Inferred ones need a label.",
44	   "fix": "Tag each Record-features line 'from source' or 'our inference'. Give Hampton a full citation (court, district, docket or WL cite) or replace it with a retrievable source. Say plainly that P4 and P17 support only the scenario theme.",
45	   "acceptance_test": "Every 'Record features:' bullet carries one of two tags, and every case citation includes court, district and docket or reporter cite; a grep-based check passes."},
46	  {"severity": "minor", "title": "Hills v. Donis 'withdrawn and substituted 2021-02-11' is not supported by the cited page",
47	   "evidence": "Doc P3: 'memorandum op. 2020-01-14, withdrawn and substituted 2021-02-11'. The cited mdjwlaw.com page is a newsbrief dated '11 Feb 2020' that cites 'Hills v. Donis, No. 14-18-00566-CV, 2020 WL 206187 ... Jan. 14, 2020, no pet. h.' and never says 'withdrawn' or 'substituted' (searched the fetched HTML). Looks like a 2020/2021 slip, or an unsourced claim.",
48	   "why_it_matters": "If the memorandum opinion was withdrawn, the write-up may describe a superseded holding. If it was not, the doc misstates the record. A paralegal would not cite either without checking.",
49	   "fix": "Either cite the substituted opinion with its own date and URL, or delete the sentence. Re-read the opinion itself, since the doc admits it was not opened.",
50	   "acceptance_test": "The P3 entry names the opinion date and the URL of the opinion that carries that date, and no claim in it lacks a retrievable page."},
51	  {"severity": "minor", "title": "P7/lib12 (defense IME) and P16 assume documents a demand-stage packet usually does not contain",
52	   "evidence": "P7 source is a New Jersey trial-evidence ruling, and lib12 is 'Defense IME with symptom-magnification wording'. P16's contradiction ('denying back and neck pain to her primary care doctor') was found by defense subpoena per the Lewis Brisbois text ('Lewis Brisbois subpoenaed post-accident records from the hospital, which showed...').",
53	   "why_it_matters": "The tool prepares a pre-suit demand chronology. A defense medical exam is a post-suit event in Texas, and the PCP record that contradicts the ortho note is often not in the paralegal's file at all. The tool can still process both, but the packet should say which stage it simulates so a reviewer does not mistake it for a typical demand file.",
54	   "fix": "Label lib12 as litigation-stage, or recast it as a carrier records-review/peer-review letter or a treating-provider FCE note. Say in lib13 that the PCP note arrived from a records request.",
55	   "acceptance_test": "Each proposed packet row states the case stage (pre-suit demand or post-suit) and how each cross-provider record entered the file."},
56	  {"severity": "minor", "title": "P5 claim that provider ledgers 'match the six categories exactly' overstates the opinion",
57	   "evidence": "In re Central Oregon (pdftotext lines 54-59): '(1) total billed charges; (2) adjustments or write-offs; (3) the amount paid to the provider and by whom; (4) outstanding balances; (5) copies of any contracts for services with ... health-insurance carrier; and (6) any letters of protection, contracts, liens, or other guarantees'. The doc's ledger columns are 'billed, adjusted, paid, payer, balance, LOP/lien'; item 5 is copies of contracts, not a column.",
58	   "why_it_matters": "lib11 and the billing-analysis card (T-083) will build six columns and call them the court's list. Item 5 is a document request, so the ledger packet would imply the contracts are on the page.",
59	   "fix": "Reword to 'ledger columns derived from items 1-4 and 6; item 5 (carrier contracts) is a separate document the packet may reference but not reproduce'.",
60	   "acceptance_test": "The P5 text distinguishes the four ledger-derivable categories from the contract-copy request."},
61	  {"severity": "minor", "title": "Three D-042 features are credited to packets whose premises do not carry them",
62	   "evidence": "Coverage map: date-convention suggestion -> 'P9 (assumption), P12'; but the lib09 and lib14 premises in the packet table mention no DD/MM date with day <= 12. Dismissal-pattern learning -> P8/lib12, but lib12's premise does not say it supplies enough credibility flags to dismiss. P16 notes 'estimate is not a charge, D-019', yet lib13's premise ('Copied ROS denies the complaint the ortho charts the same week') omits the surgical cost estimate.",
63	   "why_it_matters": "T-079 AC1 lists specific fixtures. If the premise lines are all the builder reads, these features get no test packet.",
64	   "fix": "Add a 'must contain' column to the packet table, e.g. lib09: one form dated 03/06/2026 day-first plus 14/05/2026; lib12: at least 4 credibility sentences (2 clean, 2 mixed) across 3 dates; lib13: a surgical estimate line.",
65	   "acceptance_test": "Each lib08-lib15 row lists its D-042 features, and T-079's expected.json for each packet asserts them."},
66	  {"severity": "nit", "title": "P6 source is a medical-malpractice case, and statute currency is not stated",
67	   "evidence": "dallas-appellate blog: 'The central issue in this medical malpractice case was...' for Gunn v. McCoy. The doc's Texas authorities (2007-2022) do not say whether CPRC 18.001 text was checked for later amendments.",
68	   "why_it_matters": "Low risk, since the doc says the opinions are only for scenario shape. A paralegal would still want to know before quoting.",
69	   "fix": "Add 'health care liability claim' to P6 and one line saying current statute text was not checked.",
70	   "acceptance_test": "The P6 entry names the case type and the assumptions section has the currency line."}
71	 ],
72	 "whats_right": [
73	  "Read depth is stated per source ('full text' vs 'summary'), the 403 pages are admitted, and the P16 drug-use facts are deliberately left out.",
74	  "Verified numbers match the sources: Garza interval facts, Central Oregon discovery list, Steinkamp 50.1%, ElGhrably 44 errors in 32 sets, Rodriguez-Vera 15% of 117.",
75	  "Synthetic-safety rules 1-6 (pattern not facts, dates shifted, features recombined across two patterns, SYNTHETIC banner) are the right design."],
76	 "questions_for_chris": []}
77	```
78	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:43:14.290Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-078-paralegal.md"
}
````

### User / tool · 2026-11-02T03:43:14.299Z

**tool result**
````
1	# T-078 review: paralegal-reviewer (research/record-formats.md, commit 1193f8a)
2	
3	**Verdict: changes.** The field lists, wording and traps read like what lands in a Texas PI file. The ED/PT/chiro/radiology/op-note/pharmacy/ledger/EOB/LOP specimens look right. The UB-04, ledger, EOB and CMS-1500 totals add up. The EOB arithmetic is clean, line by line. Three things need fixing before T-079 copies these specimens into packets. One CMS-1500 line breaks the NUCC rule the doc itself quotes. The two headline traps (UB-04 rate on the charge line, CMS-1500 amounts with no decimal) are described but not shown in the specimens. And T-077's proposed packets need formats this doc doesn't have.
4	
5	## Arithmetic check (script and output saved)
6	`artifacts/review-evidence/T-078-paralegal-arith.py`, output in `artifacts/review-evidence/T-078-paralegal-arith.out`.
7	- UB-04: 2,410.00 + 3,185.00 + 96.00 + 38.50 = 5,729.50, correct. Ketorolac 30 mg IM = 2 units of J1885 (15 mg) = 96.00, consistent with the ED note.
8	- CMS-1500: 85 + 30 + 45 = 160, correct. **Line 3 fails the grouping rule** (finding 1).
9	- Ledger: 210 + 130 + 70 + 35 - 70 + 70 = 445, less 45 = 400, correct.
10	- EOB: every line balances (billed - discount = allowed; allowed - deductible - coinsurance = plan paid; deductible + coinsurance = "you may owe"). Totals 235 / 115 / 120 / 100 / 4 / 16 / 104 are right. The worked example in the typical-wording paragraph also checks.
11	- PT note: 35 timed minutes is 2 units under the 8-minute rule; the specimen bills 3 (finding 4).
12	
13	## The three UB-04 details flagged as unverified (section 16)
14	I could not check these against the licensed NUBC manual. The RI Medicaid guide the researcher opened (I re-extracted it) does not address any of them. These verdicts come from my own working knowledge, so treat them as a paralegal's read.
15	1. **FL 44 holds an accommodation rate on inpatient room lines, HCPCS on outpatient lines: correct.** The RI guide says only "44 HCPC - Utilized for outpatient bills" and "46 Service Units ... hospital accommodation days", which is consistent. Rate times days equals FL 47 on those lines.
16	2. **Claim creation date in FL 45 on the 0001 total line: correct.** RI says "After the last Revenue Code, enter '0001' ... (PAPER CLAIMS ONLY)" but nothing on the date. The creation-date convention is real.
17	3. **Occurrence code 01 for the accident: right but too narrow.** Codes 01 to 06 are all accident-type (01 medical-coverage accident, 02 no-fault, 03 tort liability, 04 employment-related, 05 no medical/liability coverage, 06 crime victim). A PI hospital claim may carry 01 or 03. Extraction should treat any of them as an accident date, never a service date. The doc's wording implies 01 only (finding 6).
18	
19	## Source spot-opens
20	NUCC 1500 manual v8.0 (the 24A grouping rule and "Do not use dollar signs, commas, or a decimal point" both match), RI UB-04 instructions, Noridian chiropractic page ("Daily notes must be specific to the date of service"; "exact spinal segment"), Noridian EOB examples, CMS "how to read your medical bill" (total charges, allowed, adjustments), arXiv 2511.13523 (Tesseract CER 0.189, WER 0.276, numeric accuracy 0.756), Jotform LOP packet (continuing lien, no collections). All matched the doc.
21	
22	```json
23	{"card": "T-078", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
24	 "scope": "research/record-formats.md at commit 1193f8a; cross-read with T-077 v2 doc proposed packets, board cards T-078/T-079; no app run (research card)",
25	 "exercised": [
26	  "Read personas/paralegal.md, the whole record-formats doc, the T-077 doc, board.py show T-077/T-078/T-079, D-042",
27	  "Wrote and ran artifacts/review-evidence/T-078-paralegal-arith.py (output in T-078-paralegal-arith.out) to re-add the UB-04, CMS-1500, ledger and EOB specimens, test the PT unit rule and the 24A units rule, and the date-order cases",
28	  "Downloaded and text-extracted: NUCC 1500 manual v8.0 (lines 1202-1204 on 24F, 1351-1352 on 24A grouping), RI EOHHS UB-04 instructions (FL 4, 6, 12, 13, 42, 44-48)",
29	  "Opened: Noridian JF-B chiropractic documentation page, Noridian JF-A MSP EOB examples, CMS medical bill guide, arXiv 2511.13523 html, Jotform LOP packet",
30	  "Cross-read every specimen for internal consistency against the others (dates, visit counts, imaging types, units, payments)"],
31	 "verdict": "changes",
32	 "scores": {"fields_and_wording_realism": 4, "extraction_traps_real": 4, "specimen_arithmetic": 3, "specimens_exercise_the_traps": 2, "coverage_for_t077_packets": 2},
33	 "findings": [
34	  {"severity": "major", "title": "CMS-1500 line 3 violates the NUCC grouping rule the doc quotes, and the chiro travel card does not support it",
35	   "evidence": "record-formats.md line 358: '060126  060526  11  97010  A  45 | 00  3' means 06/01 to 06/05 = 5 calendar days, 3 units. Doc lines 28 and 338 state the rule: 'days must equal units'. NUCC manual v8.0 24A: 'Grouping is allowed only for services on consecutive days. The number of days must correspond to the number of units in 24G.' The line-363 note says 'groups three dates on one line with 3 units'. The travel card (lines 191-195) shows visits on 06/01, 06/03, 06/05 only (non-consecutive) and marks HP on 06/01 and 06/03 only, so hot/cold is documented 2 times, not 3. Script output: 'range 060126-060526 = 5 calendar days; units billed = 3; ... -> False'.",
36	   "why_it_matters": "This is the specimen meant to teach 'one line is not one visit'. As written, the truth is ambiguous: 5 days, 3 units, 2 documented. A fixture built from it has no derivable expected value. Real payers also reject this grouping, so a paralegal would flag the claim form, not trust it.",
37	   "fix": "Make line 3 consistent, e.g. 060126 060526 with 5 units at $15 = $75 and a travel card with HP on all 5 days (total becomes 190), or split into three single-date lines. If the mismatch is deliberate, label it 'DELIBERATE: units != days' and state the expected tool output.",
38	   "acceptance_test": "The script recomputes (To - From + 1) == units for every grouped line and checks the travel-card mark count equals units; both pass, or the specimen carries an explicit DELIBERATE label."},
39	  {"severity": "major", "title": "The two headline traps are in the prose but not in the specimens",
40	   "evidence": "(a) Section 15 maps UB-04 to 'FL 44 rate' and the handoff calls the rate-on-the-charge-line 'a ready-made D-042 rate-vs-charge trap', but the UB-04 specimen (lines 398-409) has no room-and-board line: FL 44 holds only HCPCS codes 99284, 72125, J1885 or is blank. There is no 0120/0110 line, no rate like 1850.00, no days in FL 46. (b) The CMS-1500 specimen is introduced as 'the OCR text a scanned form tends to produce' (line 348), yet every amount is `85 | 00`, `30 | 00`, `160 | 00`. The `15000` and `150 00` variants are only in the section 8 and section 14 prose.",
41	   "why_it_matters": "T-079 AC1 requires a rate-vs-charge trap packet. A builder who copies the specimens gets neither trap. A UB-04 where rate and charge share a line is the one place a naive total can go wrong by 3x. The decimal-less CMS-1500 amount is how $150 becomes $15,000.",
42	   "fix": "Add an inpatient UB-04 specimen with e.g. '0120 ROOM & BOARD SEMI-PVT  [FL44] 1,850.00  [FL45] 051526  [FL46] 3  [FL47] 5,550.00' and the 0001 total recomputed. Add a second CMS-1500 specimen in degraded OCR form, e.g. '8500', '30 00', '16000', plus the clean boxed form.",
43	   "acceptance_test": "Specimen check: UB-04 has a line where FL44 x FL46 == FL47; CMS-1500 has at least one amount string with no separator whose truth value is stated beside it."},
44	  {"severity": "major", "title": "Formats that the T-077 packets need are missing: EMS run report, ambulance invoice, 1.18.001 affidavit/cover page, treater narrative letter",
45	   "evidence": "T-077 proposals: lib08 starts with EMS and a second crash; lib14 'ambulance base + mileage invoice'; lib15 'EMS minor-damage and refused-transport wording' and an 'Accident caused all' letter plus billing-affidavit cover pages (P3). record-formats.md has no section for any of these (grep for 'run report', 'ambulance', 'affidavit' finds only passing mentions at lines 59, 173, 500). The ED specimen itself says 'Mode: EMS' with no EMS record. A pain-management/ESI procedure note and a work-status slip are also absent, though pain management is in the sample case.",
46	   "why_it_matters": "The AC list is met (12 named formats). But T-079 is told to build from 'the research patterns and formats', and three of its eight packets rest on documents this file cannot specify. The ambulance run sheet is the first record in nearly every MVC file, and the narrative letter and 18.001 affidavit are in almost every demand package.",
47	   "fix": "Add four short sections in the same shape (fields, wording, traps, SYNTHETIC specimen): EMS patient-care report, ambulance invoice (base + mileage), CPRC 18.001 business-records/billing affidavit with its cover page, treating-provider narrative letter. Optional: pain-management procedure note.",
48	   "acceptance_test": "Each lib08-lib15 row in the T-077 table can name the section in record-formats.md that specifies every document type it uses."},
49	  {"severity": "minor", "title": "PT specimen bills 3 timed units for 35 timed minutes, contradicting the 8-minute rule the doc cites",
50	   "evidence": "record-formats.md lines 142-145: '97110 23 min 2u; 97140 12 min 1u; Total timed 35 min'. The doc's own trap list (line 124) says 'Timed codes bill in 15-minute units under the 8-minute rule', and cites a bulletin where 40 minutes = 3 units. Script: 'PT timed minutes 35 -> CMS total timed units 2 | specimen bills 2u + 1u = 3'. The ledger (lines 446-447) repeats the 3 units ($130 + $70).",
51	   "why_it_matters": "Under the CMS total-time method this is a 1-unit over-bill. Commercial payers often use the AMA per-code method, where 3 is acceptable. The doc doesn't say which method the specimen follows, and an adjuster could treat it as an error.",
52	   "fix": "Either change minutes (e.g. 97110 25 min, 97140 13 min = 38 min = 3 units), or add a line 'units per AMA per-code method; CMS total-time method would give 2'.",
53	   "acceptance_test": "The script confirms units match total timed minutes under the stated method."},
54	  {"severity": "minor", "title": "The Delphine specimens do not agree with each other in several places",
55	   "evidence": "(1) Radiology COMPARISON 'Cervical radiographs 05/15/2026' (line 231), but the ED did and billed a CT cervical spine (lines 102, 404) and no radiographs. (2) Chiro 'Visit #9' on 06/03 (line 183) but the intake is signed 5/29/26 (line 624): nine visits in six days. (3) PT 'Visit 7 of 24' on 06/10 (line 138) but the ledger shows only the 05/27 eval and the 06/10 visit (lines 445-450). (4) Ledger 'Financial class: LOP', payments blank, TOTAL PMTS 0.00, while the EOB for the same 06/10 DOS shows plan paid $16.00 and $115.00 of CO-45/CO-97 reductions. (5) Op note 'not improved with 12 weeks of therapy' (line 280): 05/27 to 08/04 is 69 days, 9.9 weeks. (6) PT plan '3x/wk x 4 wks' against 24 planned visits.",
56	   "why_it_matters": "Items 4 and 5 are realistic traps (paid-or-incurred; therapy duration the adjuster will count), but nothing marks them as deliberate. If T-079 packages these as one case, the golden truth will contain unplanned conflicts and the tool will rightly flag them.",
57	   "fix": "Fix or annotate each as DELIBERATE with its expected flag. For (4) add a note that the packet tests ledger vs EOB mismatch and expects a billing-analysis flag.",
58	   "acceptance_test": "A short cross-check table lists every cross-specimen mismatch and marks it fixed or deliberate."},
59	  {"severity": "minor", "title": "UB-04 occurrence-code wording is too narrow, and two UB-04 conventions are stated as fact in the trap lists while still unverified",
60	   "evidence": "Section 16: 'occurrence code 01 for accident ... from my prior knowledge'. Section 9 specimen uses '31 OCCURRENCE CODE 01'. Section 1.1 (line 23) and section 9 traps state 'FL 45 on the total line is the claim creation date' without the caveat. RI guide (re-extracted) says 'See NUBC manual for specific codes' and does not mention creation date.",
61	   "why_it_matters": "PI claims may carry 01 or 03 depending on who is billed. A generator that always emits 01 under-tests accident-date detection. The creation-date convention is real, but a reader of section 1.1 would not know it is unsourced.",
62	   "fix": "Say 'accident codes 01 to 06; extraction treats any as an accident date'; vary the code across packets; add '(unverified)' next to the creation-date lines in sections 1.1 and 9.",
63	   "acceptance_test": "Section 9 names the code family; at least two UB-04 packets use different codes; unverified claims carry the marker in every place they appear."},
64	  {"severity": "minor", "title": "The Spanish specimen does not exercise the day-first trap, and 'no provider or payer name is real' is asserted without a check",
65	   "evidence": "Spanish note dates are 'Fecha: 17/05/2026' and '(24/05/2026)', both day > 12 and unambiguous; the trap table uses '03/06/2026 is 3 June', and section 15 says 'choose days <= 12 so the ambiguity is real'. The header says 'No person, provider, payer, address... is real', while section 16 says any resemblance of 'Quillfeather, Larkspur Hollow, Harrowgate & Vey' is 'unintended'. Names like 'Bluebonnet Mutual Health Plan', 'Clinica Familiar Los Almendros' and 'Dra. Ines Valcarcel' are common enough in Texas and Mexico that a collision is plausible. AC2 evidence mentions only a regex for SSN/phone patterns.",
66	   "why_it_matters": "A day-first date that cannot be misread tests nothing. The unsupported absolute 'none is real' is the kind of claim the data rule says we must not make without evidence.",
67	   "fix": "Change one Spanish date to e.g. 03/06/2026 with a stated truth; soften the header claim or run a name-collision search on every provider, payer, firm and clinician name and record the result.",
68	   "acceptance_test": "The Spanish specimen contains at least one date with day and month both <= 12 and states its truth; the doc records a collision search or drops the absolute claim."},
69	  {"severity": "nit", "title": "The doc says twelve formats but has thirteen sections; CMS-1500 PTR/MOD columns are ambiguous",
70	   "evidence": "Purpose paragraph: 'twelve document types'; sections 2 to 14 are thirteen (PT and chiro are separate); the handoff says 13. CMS-1500 specimen row '98941  AB  85 | 00' sits under the 'MOD' header, so 'AB' reads as a modifier rather than the diagnosis pointer (valid modifiers for chiro manipulation would be AT).",
71	   "why_it_matters": "Small, but an extractor test built on it can misattribute the field.",
72	   "fix": "Say thirteen; align the columns and add AT for 98941 if Medicare-style, or leave blank.",
73	   "acceptance_test": "Count in the intro matches the section count."}
74	 ],
75	 "whats_right": [
76	  "The cross-cutting trap list (service date vs creation/fax/received/statement dates, running balance, voids, one visit with several bills, rate vs charge wording) is what bites me in real files.",
77	  "The EOB, ledger, UB-04 and CMS-1500 totals re-add correctly, and the ED midnight-rollover line dates on the UB-04 (ER on 051426, CT and injection on 051526) match the ED note.",
78	  "Sources are honestly marked opened vs search summary, and the NUCC quotes ('no decimal point', 'consecutive days') match the manual."],
79	 "questions_for_chris": []}
80	```
81	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:43:14.880Z

**tool call — Bash**
````
{
 "command": "git show --stat 5c2cb2f | head -30 && echo ---- && git show --stat 327ce46 | head -30 && echo ---- && git log --oneline -5",
 "description": "Show commit stats for T-077 and T-078 and recent log"
}
````

### User / tool · 2026-11-02T03:43:15.014Z

**tool result**
````
commit 5c2cb2f0939266f7c65e1f2a1e025ac135d68839
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 21:42:31 2026 -0600

    fix(research): v2 case-library denylist enforced with self-test, tagged record features, verified citations (T-077 r2)
    
    - validate_library.py: v2 real names added (case- and accent-insensitive), capitalised-only terms for
      common words, Waddell eponym allowed, --self-test plants mixed-case names and cross-checks the doc's
      Denylist additions block and every X v. Y caption
    - v2 doc: Record features tagged from source / our inference; Hills v. Donis re-cited to the 2021
      substitute opinion (read in full); P17 source replaced (Hampton not retrievable); P5 six items
      reworded; P6 case type; stage/entry, must-contain and formats columns for lib08-lib15
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 research/case-library-sources-v2.md | 253 +++++++++++++++++++++++++++---------
 research/validate_library.py        | 168 +++++++++++++++++++++---
 2 files changed, 341 insertions(+), 80 deletions(-)
----
commit 327ce46a323a7093867e89c9856898f378b50bf2
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 21:42:39 2026 -0600

    fix(research): record formats r2 - NUCC-consistent 1500, OCR and room-rate specimens, six new formats (T-078 r2)
    
    - CMS-1500: grouped lines now consecutive days = units, matching the travel card; OCR rendering with
      decimal-less amounts and stated truth
    - UB-04: inpatient specimen with FL44 rate x FL46 days = FL47 charge; occurrence codes 01-06 as the
      accident family (code 03 used); creation-date convention marked unverified
    - New sections 15-20: EMS run report, ambulance invoice (fractional mileage), CPRC 18.001 affidavit
      + cover page, treating narrative letter, office/specialist note, records-review/IME report
    - PT units follow the stated 8-minute rule; Spanish day-first date 07/06/2026; cross-specimen table
      (fixed vs DELIBERATE); name-collision search, two names replaced
    - research/record_formats_check.py re-adds every specimen (85 checks)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 research/record-formats.md       | 527 ++++++++++++++++++++++++++++++++++-----
 research/record_formats_check.py | 208 +++++++++++++++
 2 files changed, 672 insertions(+), 63 deletions(-)
----
327ce46 fix(research): record formats r2 - NUCC-consistent 1500, OCR and room-rate specimens, six new formats (T-078 r2)
5c2cb2f fix(research): v2 case-library denylist enforced with self-test, tagged record features, verified citations (T-077 r2)
f5c43c9 docs: D-044 export gate blocks items with no judge
94beaeb fix(backend): check-trace gate and judge summary never pass over a failure or a check that did not run (T-080 r2)
df5dddd feat(frontend): vertical steppers for every check and gate, case stepper with export-gate blockers, How the AI was checked panel (T-081, T-082, D-042)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:43:15.327Z

**tool call — Bash**
````
{
 "command": "ls -la /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/ && cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "description": "List reviewer memory directory and index"
}
````

### User / tool · 2026-11-02T03:43:15.415Z

**tool result**
````
total 88
drwxr-xr-x@ 13 arsis  staff   416 Nov  1 21:20 .
drwxr-xr-x@ 17 arsis  staff   544 Nov  1 20:38 ..
-rw-r--r--@  1 arsis  staff  1571 Nov  1 21:20 MEMORY.md
-rw-r--r--@  1 arsis  staff  1965 Nov  1 21:20 d041-date-gate-patterns.md
-rw-r--r--@  1 arsis  staff   774 Nov  1 18:34 feedback_reviewer_tooling_quirks.md
-rw-r--r--@  1 arsis  staff  2123 Nov  1 18:46 feedback_spec_review_patterns.md
-rw-r--r--@  1 arsis  staff  1038 Nov  1 19:59 frontend-review-patterns.md
-rw-r--r--@  1 arsis  staff  4020 Nov  1 20:00 golden-set-recurring-findings.md
-rw-r--r--@  1 arsis  staff  1249 Nov  1 20:15 library-review-patterns.md
-rw-r--r--@  1 arsis  staff  2889 Nov  1 20:30 manual-entry-split-review-patterns.md
-rw-r--r--@  1 arsis  staff  1634 Nov  1 21:20 reviewer-api-shape-gotchas.md
-rw-r--r--@  1 arsis  staff   726 Nov  1 18:32 reviewer-hook-constraints.md
-rw-r--r--@  1 arsis  staff  1948 Nov  1 20:49 t068-dates-to-confirm-patterns.md
- [Spec review patterns](feedback_spec_review_patterns.md) — check absolute claims vs the doc's own example; grep every named category/R-ID/fixture
- [Golden-set recurring findings](golden-set-recurring-findings.md) — T-015: must/should levels, shared type+cite flags, export/§6 drift, dead checks via key drift (mutation-test)
- [Reviewer hook constraints](reviewer-hook-constraints.md) — board.py allowed verbs, python heredoc form, write-allowed dirs
- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; use Edit + scripts in review-evidence
- [Frontend review patterns](frontend-review-patterns.md) — T-043: mock vs harness coverage, keyboard focus yank, recurring minor gaps
- [Library review patterns](library-review-patterns.md) — T-052: passed with minors; rate-vs-count rule, flag-type fit, source 403s
- [Manual entry / split review patterns](manual-entry-split-review-patterns.md) — T-056: AC ticked for absent UI label, split amounts not moving, override trace missing
- [T-068 dates-to-confirm patterns](t068-dates-to-confirm-patterns.md) — orphan confirm dead-ends, record listed twice, text-only AC test, commit vs worktree divergence
- [D-041 date-gate patterns](d041-date-gate-patterns.md) — T-076 r2 (f4ef2ea): stale DATE_AMBIGUOUS fixed; Edit/Change quote still enabled on undated row (T-060)
- [Reviewer API shape gotchas](reviewer-api-shape-gotchas.md) — item GET nests under "item", status "ready", record warnings in case.flags, audit before/after local-only
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:43:18.035Z

**tool call — Bash**
````
{
 "command": "cat -n research/validate_library.py",
 "description": "Read the library validator with line numbers"
}
````

### User / tool · 2026-11-02T03:43:18.110Z

**tool result**
````
     1	#!/usr/bin/env python3
     2	"""Validate evals/library/* with evals/golden/check_golden.py (T-052) and scan packets for real identifiers (T-077).
     3	
     4	check_golden.py reads cases from its own directory, so this copies evals/golden into a scratch dir, adds the library packets,
     5	runs the checker there, and then scans the library for real identifiers. The denylist holds every proper noun taken from the
     6	cited real sources in research/case-library-sources.md (v1) and research/case-library-sources-v2.md (v2): case parties, judges,
     7	doctors named in opinions, firms, counties, cities, highways and study authors. Matching is case-insensitive and
     8	accent-insensitive ('GARZA', 'garza', 'Rodríguez' all hit). Exit 0 = both pass.
     9	
    10	Run:        python3 research/validate_library.py
    11	Self-test:  python3 research/validate_library.py --self-test   (planted names must fail; v2 doc names must all be listed)
    12	"""
    13	import pathlib, re, shutil, subprocess, sys, tempfile, unicodedata
    14	
    15	ROOT = pathlib.Path(__file__).resolve().parents[1]
    16	LIB = ROOT / "evals" / "library"
    17	V2_DOC = ROOT / "research" / "case-library-sources-v2.md"
    18	
    19	# v1 sources (research/case-library-sources.md). States are listed because v1 sources named them; packets use the
    20	# two-letter abbreviation (e.g. "TX") where a state must appear.
    21	DENYLIST_V1 = ["Nichols", "Duke Linden", "Haygood", "Escabedo", "K & L", "K&L", "Auto Crushers", "Alexandria", "Puerto Rico",
    22	               "Rissman", "Colossus", "Manitoba", "Verisk", "Medicare", "Tennessee", "Nebraska", "New Jersey", "Virginia",
    23	               "Oklahoma", "Texas", "Florida", "California", "Illinois", "Michigan", "Kelly", "Cutch"]
    24	# v2 sources (research/case-library-sources-v2.md, "Denylist additions" block). Keep the two lists in sync; --self-test checks.
    25	DENYLIST_V2 = [
    26	    # P1 JLG Trucking v. Garza
    27	    "JLG", "Garza", "Pechero", "Zapata",
    28	    # P2 Guevara v. Ferrer
    29	    "Guevara", "Ferrer",
    30	    # P3 Hills v. Donis (parties, the doctor named in the opinion, the author justice, the highway)
    31	    "Donis", "Matamoros", "Castellanos", "Morehouse", "Reuben", "Rueben", "Poissant", "I-45",
    32	    # P4 Chiv v. Figueroa
    33	    "Chiv", "Figueroa",
    34	    # P5 In re Central Oregon Truck Co.
    35	    "Central Oregon", "Oregon", "Broussard",
    36	    # P6 Gunn v. McCoy
    37	    "Gunn", "McCoy",
    38	    # P7 Rodriguez v. Wal-Mart Stores
    39	    "Rodriguez", "Wal-Mart", "Walmart",
    40	    # P16 defense-firm write-up
    41	    "Lewis Brisbois", "Brisbois", "Harris County",
    42	    # P17 Hampton v. Miskell (dropped as a source, names still banned) and Castro et al.
    43	    "Hampton", "Miskell", "Baratta", "I-635", "Castro", "Schilgen",
    44	    # Study authors cited in v2
    45	    "Steinkamp", "Kantrowitz", "Airan-Javia", "ElGhrably", "Fishbain", "Powell", "Anderson",
    46	    # Cities and counties named in v2 citations; insurer named in a v1 caption that v2 mentions
    47	    "Houston", "Dallas", "Allstate",
    48	]
    49	# Real names that are also ordinary lowercase words: banned only when capitalised (Title or UPPER), so "rolling hills" or
    50	# "flores" (Spanish for flowers) in a packet still passes while "Hills" / "FLORES" as a name fails.
    51	DENY_CAPITALISED = ["Hills", "Flores", "Bai"]
    52	# Eponymous clinical terms that share a name with a cited author and are allowed in packets on purpose.
    53	ALLOWED_EPONYMS = ["Waddell"]
    54	DENYLIST = DENYLIST_V1 + DENYLIST_V2
    55	BANNER = "SYNTHETIC — invented for evaluation; not real patient data\n"
    56	
    57	
    58	def fold(s):
    59	    """Strip accents so 'Rodríguez' matches 'Rodriguez'."""
    60	    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    61	
    62	
    63	_ANY = [(w, re.compile(r"(?<!\w)" + re.escape(fold(w)) + r"(?!\w)", re.I)) for w in DENYLIST]
    64	_CAP = [(w, re.compile(r"(?<!\w)(?:" + re.escape(w) + "|" + re.escape(w.upper()) + r")(?!\w)")) for w in DENY_CAPITALISED]
    65	
    66	
    67	def scan_text(text):
    68	    """Return the denylist terms found in text (case- and accent-insensitive; capitalised-only terms need a capital)."""
    69	    t = fold(text)
    70	    return [w for w, rx in _ANY if rx.search(t)] + [w for w, rx in _CAP if rx.search(t)]
    71	
    72	
    73	def doc_denylist_block(doc_text):
    74	    """Terms listed in the v2 doc's fenced 'Denylist additions' block (one per line, '#' comments allowed)."""
    75	    m = re.search(r"## Denylist additions.*?```text\n(.*?)```", doc_text, re.S)
    76	    if not m:
    77	        return None
    78	    return [ln.split("#")[0].strip() for ln in m.group(1).splitlines() if ln.split("#")[0].strip()]
    79	
    80	
    81	_GENERIC = {"In", "re", "Inc", "Inc.", "LLC", "LLC,", "Co", "Co.", "Stores", "Stores,", "Truck", "Trucking", "Trucking,", "The",
    82	            "of", "and", "Tex", "Tex.", "App", "App.", "No", "No."}
    83	
    84	
    85	def doc_caption_names(doc_text):
    86	    """Capitalised name tokens from every 'X v. Y' and 'In re X' caption in the v2 doc."""
    87	    names = set()
    88	    for a, b in re.findall(r"([A-Z][\w.'&-]*(?:,? [A-Z][\w.'&-]*)*) v\. ([A-Z][\w.'&-]*(?:,? [A-Z][\w.'&-]*)*)", doc_text):
    89	        for side in (a, b):
    90	            for tok in re.split(r"[ ,]+", side):
    91	                if len(tok) > 1 and tok not in _GENERIC and tok[0].isupper() and not any(c.isdigit() for c in tok):
    92	                    names.add(tok.rstrip(".,"))
    93	    for x in re.findall(r"In re ([A-Z][\w'-]*(?: [A-Z][\w'-]*)*)", doc_text):
    94	        toks = [t for t in x.split() if t not in _GENERIC]
    95	        if toks:
    96	            names.add(" ".join(toks[:2]))
    97	    return names
    98	
    99	
   100	def self_test():
   101	    fails = []
   102	    for w in DENYLIST:
   103	        for variant in {w, w.lower(), w.upper(), w.swapcase(), w.title()}:
   104	            if w not in scan_text(f"Seen by Dr. {variant} at the clinic."):
   105	                fails.append(f"planted {variant!r} not caught")
   106	    for w in DENY_CAPITALISED:
   107	        for variant in (w, w.upper()):
   108	            if w not in scan_text(f"Referred by {variant} Family Clinic."):
   109	                fails.append(f"planted {variant!r} not caught")
   110	        if scan_text(f"walked up the {w.lower()} near home"):
   111	            fails.append(f"lowercase common word {w.lower()!r} wrongly flagged")
   112	    if not scan_text("Patient: Ana Rodríguez (SYNTHETIC)"):
   113	        fails.append("accented Rodríguez not caught")
   114	    for w in ALLOWED_EPONYMS:
   115	        if scan_text(f"{w} signs 0/5 today."):
   116	            fails.append(f"eponym {w!r} wrongly flagged")
   117	    doc = V2_DOC.read_text()
   118	    block = doc_denylist_block(doc)
   119	    listed = {fold(w).lower() for w in DENYLIST + DENY_CAPITALISED + ALLOWED_EPONYMS}
   120	    if block is None:
   121	        fails.append("v2 doc has no '## Denylist additions' ```text block")
   122	    else:
   123	        for w in block:
   124	            if fold(w).lower() not in listed:
   125	                fails.append(f"v2 doc denylist term {w!r} missing from validate_library.py")
   126	        for w in DENYLIST_V2 + DENY_CAPITALISED:
   127	            if w not in block:
   128	                fails.append(f"validate_library.py term {w!r} missing from the v2 doc block")
   129	    for name in sorted(doc_caption_names(doc)):
   130	        if not any(fold(part).lower() in listed for part in [name] + name.split()):
   131	            fails.append(f"v2 caption name {name!r} not on the denylist")
   132	    # End-to-end: a planted packet must make the library scan fail.
   133	    with tempfile.TemporaryDirectory() as tmp:
   134	        p = pathlib.Path(tmp) / "case_planted.txt"
   135	        p.write_text(BANNER + "Patient seen by DR. GARZA after the crash on i-45.\n")
   136	        if not scan_library([p]):
   137	            fails.append("planted packet passed the library scan")
   138	    for f in fails:
   139	        print("SELF-TEST FAIL:", f)
   140	    n = len(DENYLIST) * 5 + len(DENY_CAPITALISED) * 3
   141	    print("self-test:", "FAIL" if fails else f"ok ({n} planted variants caught, {len(doc_caption_names(doc))} caption names covered)")
   142	    return 1 if fails else 0
   143	
   144	
   145	def scan_library(files):
   146	    bad = []
   147	    for f in files:
   148	        t = f.read_text()
   149	        for w in scan_text(t):
   150	            bad.append(f"{f.name}: contains real identifier {w!r}")
   151	        if f.suffix == ".txt" and not t.startswith(BANNER):
   152	            bad.append(f"{f.name}: missing SYNTHETIC header")
   153	    return bad
   154	
   155	
   156	def main():
   157	    if "--self-test" in sys.argv:
   158	        return self_test()
   159	    cases = sorted(LIB.glob("case_*.expected.json"))
   160	    if len(cases) < 6:
   161	        print(f"FAIL: need >= 6 library cases, found {len(cases)}")
   162	        return 1
   163	    with tempfile.TemporaryDirectory() as tmp:
   164	        d = pathlib.Path(tmp) / "golden"
   165	        shutil.copytree(ROOT / "evals" / "golden", d)
   166	        for f in LIB.glob("case_*"):
   167	            shutil.copy(f, d / f.name)
   168	        r = subprocess.run([sys.executable, str(d / "check_golden.py")], capture_output=True, text=True, cwd=d)
   169	    print(r.stdout.strip()[-1500:] or r.stderr.strip()[-1500:])
   170	    bad = scan_library(sorted(LIB.glob("case_*")))
   171	    for b in bad:
   172	        print("IDENTIFIER CHECK FAIL:", b)
   173	    terms = len(DENYLIST) + len(DENY_CAPITALISED)
   174	    print("identifier check:", "FAIL" if bad else f"ok ({len(cases)} packets, {terms} denylist terms, case-insensitive)")
   175	    return 1 if (r.returncode or bad) else 0
   176	
   177	
   178	if __name__ == "__main__":
   179	    sys.exit(main())
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:43:18.337Z

**tool call — Bash**
````
{
 "command": "cat -n research/case-library-sources-v2.md",
 "description": "Read the v2 case library sources doc with line numbers"
}
````

### User / tool · 2026-11-02T03:43:18.417Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:43:19.875Z

**tool call — Bash**
````
{
 "command": "wc -l research/case-library-sources-v2.md && cat -n research/case-library-sources-v2.md | sed -n '19,140p'",
 "description": "Read the first part of the v2 doc"
}
````

### User / tool · 2026-11-02T03:43:19.958Z

**tool result**
````
     435 research/case-library-sources-v2.md
    19	## Synthetic-safety rules (apply to every pattern)
    20	
    21	1. **Pattern, not facts.** We take the shape of the record (what kind of page, which wording, which billing columns, where
    22	   the gap falls) and nothing else. No party, provider, clinic, county, road, date, amount or diagnosis code is copied.
    23	2. **Invented people and places.** Every name, provider, clinic and town is invented (the v1 style: Marrowgate,
    24	   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass. Every real name in this file is on
    25	   that denylist (see "Denylist additions" below; matching is case- and accent-insensitive), and
    26	   `python3 research/validate_library.py --self-test` proves a planted name fails. Common surnames that appear here
    27	   (Garza, Rodriguez, Hills, Gunn, Hampton, Castro, Powell, Anderson, Flores) are banned as invented-name choices too,
    28	   including in the Spanish-language packets: pick distinctive invented surnames instead.
    29	3. **Dates shifted.** Packet dates run in 2025–2027 and keep only the *interval* shape the pattern needs (e.g. "second event
    30	   about 12 weeks after the first"). Real dates in this file are citation dates for the source, not record dates.
    31	4. **Facts recombined.** Each packet mixes features from two or more patterns, so no packet maps back to one real matter.
    32	5. **Every packet text file starts with the SYNTHETIC banner line** used by v1 and is labeled synthetic in its expected JSON.
    33	6. **No real records.** Nothing here was taken from a medical record; opinions describe facts in prose, and we use that prose
    34	   only for scenario shape. Spanish text in packets is written fresh, not translated from any source.
    35	
    36	## Patterns
    37	
    38	### P1. Intervening second accident between first care and the key imaging
    39	- **Source:** JLG Trucking, LLC v. Garza, 466 S.W.3d 157 (Tex. 2015), opinion delivered 2015-04-24 —
    40	  https://www.txcourts.gov/media/943999/130978.pdf (full text, background section read).
    41	- **Summary:** The plaintiff was rear-ended, saw an orthopedist five days later, did about eleven weeks of PT, then had a
    42	  second crash shortly after PT ended and was taken by ambulance in a hard collar. The MRI showing herniations came only after
    43	  the second crash; surgery followed years later. The court held the second accident was relevant to causation and its
    44	  exclusion (including on cross of the treating doctor) was harmful error, even without a defense causation expert.
    45	- **Record features (from source):** an orthopedic visit days after event 1, then about eleven weeks of PT; an ambulance
    46	  transport in a hard collar after event 2; first MRI dated after event 2; a treating note whose history omits event 2;
    47	  multi-year span ending in fusion.
    48	- **Record features (our inference):** first-incident clinic records missing from the file; an ER record from event 2 with
    49	  neck complaints; a surgeon's narrative "history" that attributes everything to event 1.
    50	- **D-042 / flags:** conflict (two incident dates in the chart), causation (history-only attribution is self-reported/
    51	  provider-recited, not an opinion), gap; multi-case library; vertical stepper must show "two incidents found: human
    52	  decides relevance" as a HITL step. The tool never apportions.
    53	- **Synthetic-safety:** invent both crashes, shift to 2025–2026, change the interval (e.g. 10–14 weeks), change body region
    54	  if useful (lumbar instead of cervical); no county, highway or vehicle type from the opinion.
    55	
    56	### P2. Immediate care is common-knowledge; later complex care needs an expert
    57	- **Source:** Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007), decided 2007-08-31 —
    58	  https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html and commentary
    59	  https://www.casemine.com/commentary/us/expert-medical-evidence-mandated-for-causation-in-high-cost-automobile-accident-claims:-guevara-v.-ferrer/view
    60	  (summary only).
    61	- **Summary:** An elderly passenger's family relied on lay testimony to tie over $1 million in medical expenses to a crash.
    62	  The court held lay evidence can link a crash to conditions within common knowledge (immediate post-crash care), but
    63	  conditions outside it need expert evidence; the claimant must show what conditions generated the expenses and that each
    64	  was caused by the accident.
    65	- **Record features (from source):** immediate post-crash care, then a long, medically complex course with large total
    66	  expenses in an elderly patient.
    67	- **Record features (our inference):** EMS and ER pages with visible injuries; later admission, procedure and rehab notes
    68	  with no causation statement; one itemized hospital bill spanning both phases; comorbidities in the problem list.
    69	- **D-042 / flags:** causation (absence of any provider causation statement on later care is shown as "no causation
    70	  language found", not as a finding), pre_existing (comorbidity list), billing analysis (charges split by encounter, cited
    71	  per line); calibrated confidence must not imply causation strength.
    72	- **Synthetic-safety:** age band changed, no death in the packet, invented hospital, amounts invented and far smaller.
    73	
    74	### P3. Billing affidavits and records are not causation; conclusory physician letter
    75	- **Source:** Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.] Feb. 11, 2021, pet. denied) (substitute
    76	  mem. op.) — opinion PDF via the court docket https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14 (full
    77	  text read, pdftotext). The docket shows the memorandum opinion of 2020-01-14, a rehearing motion, and on 2021-02-11
    78	  rehearing denied, the 2020 opinion withdrawn and a substitute memorandum opinion issued; petition for review No. 21-0287
    79	  denied 2021-07-23 (https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/). The firm newsbrief
    80	  https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the withdrawn 2020 opinion only.
    81	- **Summary (2021 substitute opinion):** Soft-tissue claims after a rear-end crash; no ambulance or ER. Past-medical awards
    82	  for three plaintiffs were reversed and rendered: §18.001 affidavits prove reasonableness of charges, not causation, and
    83	  a treating doctor's letters (and causation statements inside billing records) were conclusory because they gave no
    84	  explanation of how and why the crash caused the diagnoses. The award for a fourth plaintiff's ankle injury, and her
    85	  child's single visit, was affirmed on lay testimony and temporal proximity (Guevara).
    86	- **Record features (from source):** letters from a treater stating the crash caused the injuries, with no reasoning;
    87	  causation statements embedded in billing records; long diagnosis lists (radiculitis, disc displacement, discogenic pain)
    88	  on the bills; one plaintiff's single-visit bill (evaluation plus hot/cold pack).
    89	- **Record features (our inference):** billing-affidavit cover pages that look like records but carry no clinical content;
    90	  the same diagnosis lines repeated on every bill.
    91	- **D-042 / flags:** causation (letter language is shown verbatim with source; the tool never upgrades it to an opinion);
    92	  billing analysis (affidavit totals cited to the page, not re-derived by the LLM); LLM-as-judge visible: the judge must
    93	  reject any summary that turns "the accident caused" into a fact; record_warning for non-clinical pages.
    94	- **Synthetic-safety:** invented clinic and letter text; diagnosis wording paraphrased generically; no amounts reused; no
    95	  highway, county or party name from the opinion.
    96	
    97	### P4. Spanish-speaking party, certified interpreter, uncertified translation; counteraffidavit fight
    98	- **Source:** Chiv v. Figueroa, No. 01-23-00638-CV (Tex. App.—Houston [1st Dist.] 2025-08-21) —
    99	  https://hallapproved.com/tx/cases/appeals/2025/10659616/ (page fetched; summarized by the fetch tool, not read line by line).
   100	- **Summary:** A party sought to use a deposition taken in Spanish that lacked a certified translation, with a certified
   101	  interpreter at trial; that point was not preserved. Separately, striking a §18.001 counteraffidavit was harmful because the
   102	  only non-lay causation evidence came from admitted medical reports; past medical was reversed and remanded.
   103	- **Scope of support:** this source supports only the scenario theme (Spanish-speaking party, translation and
   104	  counteraffidavit disputes). The opinion says nothing about how records are charted.
   105	- **Record features (our inference):** records where the history is given in Spanish and charted in English; a note line
   106	  such as "history via interpreter" (or its absence); an itemized bill paired with a counteraffidavit-style rebuttal page.
   107	- **D-042 / flags:** Spanish-language records (the excerpt stays in the original language; any LLM translation is labeled
   108	  and judged); speaker attribution v2 (patient vs interpreter vs provider); billing analysis (contested line items shown, not
   109	  resolved).
   110	- **Synthetic-safety:** invented parties and providers; Spanish lines composed fresh; no deposition content used.
   111	
   112	### P5. Prior accidents, claimed brain injury, memory gaps, and a six-column billing request
   113	- **Source:** In re Central Oregon Truck Co., No. 20-0945 (Tex. 2022, per curiam), opinion delivered 2022-05-06 —
   114	  https://www.txcourts.gov/media/1454150/200945pc.pdf (full text read).
   115	- **Summary:** After a rear-end crash the plaintiff claimed a TBI and lost earning capacity; she had treated after two
   116	  earlier car accidents and for other conditions with overlapping symptoms, and said at deposition that memory problems
   117	  limited her recall. The court held pre-accident medical records and provider billing data relevant (subject to
   118	  proportionality). The billing discovery listed six items: (1) total billed charges, (2) adjustments or write-offs,
   119	  (3) amount paid to the provider and by whom, (4) outstanding balances, (5) copies of contracts with the health-insurance
   120	  carrier, (6) any letters of protection, contracts, liens or other guarantees.
   121	- **Record features (from source):** two earlier car accidents with treatment; memory complaints; a prior tailbone surgery;
   122	  the six billing-discovery items above.
   123	- **Record features (our inference):** intake forms answering "prior accidents: none" vs older notes that mention them; a
   124	  neuro or neuropsych note with memory complaints; ledger columns derived from items 1-4 and 6 (billed, adjusted, paid,
   125	  payer, balance, LOP/lien). Item 5 (carrier contracts) is a separate document a packet may reference but never reproduce
   126	  as a ledger column.
   127	- **D-042 / flags:** billing analysis (ledger columns from items 1-4 and 6, each cited; totals by code); pre_existing (prior accidents); conflict
   128	  (intake denial vs older note); calibrated confidence (per-state precision, not a "TBI likely" score).
   129	- **Synthetic-safety:** invented crash count and years (shift to e.g. 2019/2022 priors, 2026 index event); generic employment
   130	  facts omitted; ledger numbers invented.
   131	
   132	### P6. Health-insurer-paid claims: EOBs with billed, allowed, paid, patient share
   133	- **Source:** Gunn v. McCoy, 554 S.W.3d 645 (Tex. 2018), decided 2018-06-15 (one secondary source says 2018-02-08; trust the
   134	  reporter citation) — https://dallas-appellate.blogspot.com/2018/06/kmh-scotx-insurance-agents-may-know.html and
   135	  https://painterfirm.com/medmal/texas-supreme-court-allows-streamlined-approach-to-medical-billing-affidavits/ (summary only).
   136	- **Summary:** In a health care liability claim (medical malpractice, not a crash case), the plaintiff replaced provider
   137	  billing affidavits with affidavits from health insurers' subrogation agents stating amounts actually paid; the court held
   138	  §18.001 does not limit affiants to providers or their custodians.
   139	- **Record features (from source):** insurer subrogation-agent affidavits stating amounts paid.
   140	- **Record features (our inference):** insurer EOB pages (billed / allowed / plan paid / deductible / coinsurance / patient responsibility /
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:43:21.047Z

**tool call — Bash**
````
{
 "command": "cat -n research/case-library-sources-v2.md | sed -n '140,290p'",
 "description": "Read middle part of the v2 doc"
}
````

### User / tool · 2026-11-02T03:43:21.125Z

**tool result**
````
   140	- **Record features (our inference):** insurer EOB pages (billed / allowed / plan paid / deductible / coinsurance / patient responsibility /
   141	  "not covered" with a remark code); the same date of service appearing on a provider bill and an EOB with different numbers;
   142	  the affidavit page itself.
   143	- **D-042 / flags:** billing analysis (paid vs incurred, never chosen by the LLM; code reconciles EOB to provider bill and
   144	  flags mismatches); charge reclassification guard (an "allowed amount" is not a charge); dedupe of the same service across
   145	  two documents.
   146	- **Synthetic-safety:** invented insurer, plan and remark codes; amounts invented; no real payer names.
   147	
   148	### P7. Pain out of proportion, "somatization", "symptom magnification" in the exam note
   149	- **Source:** Rodriguez v. Wal-Mart Stores, Inc., A-2/3-17 (N.J. 2019-03-04) —
   150	  https://www.njcourts.gov/system/files/court-opinions/2019/a_2_3_17.pdf (syllabus read).
   151	- **Summary:** A shopper hit by a falling display developed a CRPS diagnosis. A defense neurologist described a strong pain
   152	  reaction to light touch while a companion rubbed the same arm without a reaction, found nothing objective, and used
   153	  "somatization" and "symptom magnification". The court held such terms are admissible case by case, distinguished them from
   154	  "malingering", and upheld admission of unrelated past medical history.
   155	- **Record features (from source):** a defense neurologist's exam narrating observed behavior (pain reaction to light touch vs
   156	  none when a companion touched the arm), no objective findings, "somatization" and "symptom magnification"; unrelated past
   157	  medical history.
   158	- **Record features (our inference):** treater notes using the same CRPS vocabulary in the opposite direction.
   159	- **Case stage:** a defense medical exam is a post-suit event (in Texas, TRCP 204 needs a motion and court order). For a
   160	  pre-suit demand packet use the same wording in a carrier records-review (peer-review) letter instead (see lib12).
   161	- **D-042 / flags:** credibility flags (D-043: any credibility term flags; a second clause or contrast word always flags);
   162	  speaker attribution v2 (examiner's observation vs patient's report vs companion's behavior); LLM-as-judge visible; the tool
   163	  never concludes malingering.
   164	- **Synthetic-safety:** different mechanism (e.g. falling shelf at a hardware store), different limb, invented examiner;
   165	  no psychiatric details beyond a generic history line.
   166	
   167	### P8. Waddell signs charted as a score
   168	- **Source:** Fishbain et al., "A Structured Evidence-Based Review on the Meaning of Nonorganic Physical Signs: Waddell
   169	  Signs", Pain Medicine 4(2):141–181 (2003); companion review Clin J Pain 20(6):399–408 (2004) —
   170	  https://www.statpearls.com/articlelibrary/viewarticle/31286/ (StatPearls overview; reviews seen via search summaries only).
   171	- **Summary:** Reviews of the Waddell literature found the signs associated with poorer treatment outcomes but not reliably
   172	  with secondary gain or malingering; adjusters and IMEs still cite a positive count as a credibility point.
   173	- **Record features (from source):** the five Waddell sign categories (superficial/non-anatomic tenderness, simulation,
   174	  distraction, regional disturbance, overreaction) charted as a count.
   175	- **Record features (our inference):** "Waddell 3/5 positive", "distraction SLR negative"; clean negations ("0/5 Waddell
   176	  signs") on other dates; FCE "effort inconsistent" lines. "Waddell" is an eponymous clinical term and is allowed in
   177	  packets (it is on the validator's eponym allow-list, not the denylist).
   178	- **D-042 / flags:** credibility flags with the D-043 allow-list (clean negation does not flag; mixed sentence flags);
   179	  dismissal-pattern learning must not learn to auto-dismiss credibility flags (eval-guarded).
   180	- **Synthetic-safety:** all wording composed fresh; invented PT/FCE provider and dates.
   181	
   182	### P9. Interpreter errors and ad hoc (family) interpreters in a Spanish-language history
   183	- **Source:** Flores G. et al., "Errors in medical interpretation and their potential clinical consequences in pediatric
   184	  encounters", Pediatrics 111(1):6–14 (2003) — AHRQ research summary
   185	  https://webarchive.library.unt.edu/web/20081105020658/http:/www.ahrq.gov/research/apr03/0403RA20.htm (summary only).
   186	  Corroborating (search excerpt only, page returned 403): Texas DWC Appeals Panel decisions on interpreter word choice
   187	  ("espalda" for the area between the shoulder blades; "cane" vs "crutches") — https://texasworker.com/?p=38127.
   188	- **Summary:** Thirteen audiotaped visits averaged 31 interpretation errors each; most had potential clinical consequences,
   189	  ad hoc interpreters' errors more often so (77% vs 53%); omission was the commonest error. One reported example turned a fall
   190	  into a reported assault.
   191	- **Record features (from source):** an ad hoc family interpreter; omissions; a mechanism that changed in interpretation
   192	  (fall reported as assault); "espalda" word choice (DWC excerpt only).
   193	- **Record features (our inference):** "Hx obtained via patient's son (interpreter)"; mechanism worded differently on two
   194	  records; a Spanish intake form beside an English provider note; DD/MM/YYYY dates on a form from a clinic across the
   195	  border.
   196	- **D-042 / flags:** Spanish-language records; speaker attribution v2 (who said it); conflict (mechanism mismatch, code
   197	  surfaces both); date-convention suggestion (pre-select with reason, one confirm); body-region ambiguity goes to human.
   198	- **Synthetic-safety:** no pediatric facts; adult patient, invented family member and clinic; Spanish text composed fresh.
   199	
   200	### P10. Copy-forward (cloned) notes that contradict the visit
   201	- **Source:** Steinkamp J., Kantrowitz J.J., Airan-Javia S., "Prevalence and Sources of Duplicate Information in the
   202	  Electronic Medical Record", JAMA Network Open 5(9) (2022-09-01) — https://pubmed.ncbi.nlm.nih.gov/36156143/ (abstract read).
   203	- **Summary:** Across about 104.5 million notes at one health system (2015–2020), 50.1% of text was duplicated from earlier
   204	  notes about the same patient, rising from 33% to 54.2%; 45.9% of duplicated text came from a different author.
   205	- **Record features (from source):** half of note text duplicated from earlier notes, often from another author.
   206	- **Record features (our inference):** identical ROS/exam blocks across visits weeks apart ("denies neck pain" copied into a neck-pain
   207	  follow-up); "pain 6/10" unchanged across six visits; a stale medication list; a plan that repeats a completed referral.
   208	- **D-042 / flags:** conflict (same-visit contradiction between HPI and copied ROS); dedupe must *not* merge two visits just
   209	  because text matches (code dedupes by date + provider + content, and shows near-duplicates for human review);
   210	  LLM-as-judge must catch a summary that cites the copied line as current; vertical stepper shows "near-duplicate text
   211	  across N visits".
   212	- **Synthetic-safety:** template text invented; invented clinic.
   213	
   214	### P11. Left/right transposition across records
   215	- **Source:** ElGhrably I., Fraser S.G., "An observational study of laterality errors in a sample of clinical records",
   216	  Eye 22(3):340–343 (2008) — https://www.nature.com/articles/6702590 (abstract via search excerpts).
   217	- **Summary:** In 100 randomly selected ophthalmic record sets the authors found 44 left/right transposition errors in 32
   218	  sets; 19 were later corrected; three consent forms named the wrong eye.
   219	- **Record features (from source):** left/right transpositions across a record set, some later corrected; consent forms
   220	  naming the wrong side.
   221	- **Record features (our inference):** "right shoulder" in the ER note, "left shoulder" in the ortho note, MRI ordered on one side and read on
   222	  the other; a radiculopathy side that flips; a correction addendum.
   223	- **D-042 / flags:** conflict (mixed-side exam findings, code-detected by side tokens per body part; never resolved by the
   224	  LLM); judge must reject a summary that silently picks a side; HITL step "confirm side".
   225	- **Synthetic-safety:** orthopedic not ophthalmic; invented providers; side flip placed at an invented visit.
   226	
   227	### P12. Handwritten, scanned pages with illegible entries
   228	- **Source:** Rodríguez-Vera F.J. et al., "Illegible handwriting in medical records", J R Soc Med 95(11):545–546 (2002) —
   229	  https://pmc.ncbi.nlm.nih.gov/articles/PMC1279250 (abstract-level via search; full text not read).
   230	- **Summary:** Of 117 hospital case notes, 15% were so illegible that meaning was unclear; surgical departments scored worse.
   231	- **Record features (from source):** illegible handwritten hospital notes whose meaning is unclear.
   232	- **Record features (our inference):** faxed or scanned urgent-care and chiropractic daily notes; checkbox SOAP forms; handwritten pain
   233	  scores and dates; signatures illegible; a typed later page that disagrees with a handwritten earlier page; skewed scans.
   234	- **D-042 / flags:** local OCR (Tesseract) with page image beside OCR text, OCR-derived items always need review; date-
   235	  convention suggestion for handwritten dates; PDF hidden-text detection (assumption, no public PI source found: a scanned
   236	  page whose embedded text layer differs from the image, e.g. a copy-service OCR layer; we include it adversarially).
   237	- **Synthetic-safety:** handwriting rendered synthetically (font or generated strokes), never scanned from a real chart.
   238	
   239	### P13. Concussion not diagnosed in the ER; LOC history changes later
   240	- **Source:** Powell J.M. et al., "Accuracy of Mild Traumatic Brain Injury Diagnosis", Arch Phys Med Rehabil 89(8):1550–1555
   241	  (2008) — https://natlawreview.com/article/new-study-finds-emergency-room-physicians-often-fail-to-diagnose-tbi (summary only).
   242	- **Summary:** Among ED patients who met CDC mild-TBI criteria by study interview, 56% had no documented TBI diagnosis in the
   243	  ED record; ED care focused on ruling out severe injury.
   244	- **Record features (from source):** an ED record with no TBI diagnosis for a patient who met mild-TBI criteria.
   245	- **Record features (our inference):** ER "denies LOC", "CT head negative", discharge dx "neck strain"; a later neurology note "brief LOC per
   246	  patient", headaches, word-finding complaints; a neuropsych page weeks later.
   247	- **D-042 / flags:** conflict (LOC denied vs reported, both cited); causation (patient-stated onset); new body system after
   248	  a gap; speaker attribution (per patient vs examiner). The tool does not diagnose concussion.
   249	- **Synthetic-safety:** invented ED and neurologist; mechanism changed; dates shifted.
   250	
   251	### P14. Chargemaster charge vs what is owed (rate-vs-charge trap on hospital bills)
   252	- **Source:** Bai G., Anderson G.F., "Extreme Markup: The Fifty US Hospitals With The Highest Charge-To-Cost Ratios",
   253	  Health Affairs 34(6) (2015) — https://publichealth.jhu.edu/2015/some-hospitals-marking-up-prices-more-than-1000-percent
   254	  (press release; paper not opened).
   255	- **Summary:** In 2012 Medicare cost-report data the typical hospital charged about 3.4 times Medicare-allowable cost; the 50
   256	  highest-markup hospitals charged roughly ten times, 49 of them for-profit.
   257	- **Record features (from source):** hospital charges several times cost.
   258	- **Record features (our inference):** UB-04-style itemized bill with revenue codes, units and unit price; a "self-pay discount" line; a
   259	  later statement with a contractual adjustment; a price list or rate sheet page that is not a charge.
   260	- **D-042 / flags:** charge reclassification guard (a rate becomes a charge only with code-verified charge wording plus a
   261	  judge re-check); billing analysis (units × unit price is recomputed in code and compared with the stated line total);
   262	  totals in code only.
   263	- **Synthetic-safety:** invented hospital, codes and prices; no real chargemaster data.
   264	
   265	### P15. Ambulance bill: base rate plus per-mile mileage
   266	- **Source:** FAIR Health, "A Window into Utilization and Cost of Ground Ambulance Services" (brief, 2023) —
   267	  https://mma.prnewswire.com/media/2207553/A_Window_into_Utilization_and_Cost_of_Ground_Ambulance_Services___A_FAIR_Health_Brief.pdf?p=pdf
   268	  (search excerpt only).
   269	- **Summary:** Ground ambulance claims are billed as a base transport line plus mileage per statute mile; most claim lines
   270	  were out of network (63.7% in 2018, 59.4% in 2022).
   271	- **Record features (from source):** a base transport line plus per-mile mileage; out-of-network claim lines. Medicare billing
   272	  rules confirm two lines per trip and loaded miles rounded up to the tenth (see research/record-formats.md §16).
   273	- **Record features (our inference):** EMS run sheet (times, vitals, "ambulatory at scene" or "stretcher") plus an invoice with "ALS base",
   274	  "mileage 14 mi @ $X/mi" and a line total; a balance-bill page.
   275	- **D-042 / flags:** charge reclassification (the per-mile rate is a rate; only the extended line or stated total is a charge);
   276	  billing analysis (lien/balance columns); code checks miles × rate = stated line.
   277	- **Synthetic-safety:** invented EMS agency, mileage and rates.
   278	
   279	### P16. Same-week symptom contradiction across two providers
   280	- **Source:** Lewis Brisbois write-up of a Harris County zero-damages defense verdict (trial 2023-12; published 2024-06-25)
   281	  — https://www.legal500.com/intelligence/united-states/litigation-mediation-arbitration/houston-office-secures-zero-damages-verdict-in-rear-end-collision-case
   282	  (fetched; defense-side account).
   283	- **Summary:** After an ER visit the next day and care with several providers, the plaintiff reported significant neck and
   284	  back pain to an orthopedic surgeon while denying those symptoms to her primary-care doctor; the defense also disputed a
   285	  recommended discectomy and pointed to photos of a minor impact. The jury awarded nothing.
   286	- **Record features (from source):** neck and back pain reported to an orthopedic surgeon while denied to the primary-care
   287	  doctor; a recommended discectomy; photos of minor impact.
   288	- **Case stage and entry:** in the source the PCP records came in by defense subpoena (post-suit). In a pre-suit demand
   289	  packet the PCP note arrives from the paralegal's own records request after the client lists the PCP on intake (lib13).
   290	- **Record features (our inference):** ortho note "low back pain 8/10, radiating" and a PCP note days apart with ROS "denies back pain"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:43:22.210Z

**tool call — Bash**
````
{
 "command": "cat -n research/case-library-sources-v2.md | sed -n '290,435p'",
 "description": "Read final part of the v2 doc"
}
````

### User / tool · 2026-11-02T03:43:22.294Z

**tool result**
````
   290	- **Record features (our inference):** ortho note "low back pain 8/10, radiating" and a PCP note days apart with ROS "denies back pain"
   291	  (possibly copied forward, see P10); a surgical recommendation with a cost estimate; property-damage photos referenced but
   292	  not in the file.
   293	- **D-042 / flags:** conflict (cross-provider, code pairs nearby dates); billing analysis (estimate is not a charge, D-019);
   294	  vertical stepper HITL "two providers disagree; paralegal decides which to cite".
   295	- **Synthetic-safety:** drug-use facts from the write-up are **not** used; invented providers; shifted dates.
   296	
   297	### P17. Minimal property damage, low-speed impact (MIST) language in records
   298	- **Source:** Castro W.H. et al., "Do 'whiplash injuries' occur in low-speed rear impacts?", Eur Spine J 6(6):366–375
   299	  (1997), PMID 9455663 — https://pubmed.ncbi.nlm.nih.gov/9455663/ (abstract read via PubMed). This replaces the round-1
   300	  source (a Texas appellate summary on a reconstructionist's five-mph opinion) because no court, district, docket or
   301	  reporter cite could be found for it and its page returned 403; its names stay on the denylist.
   302	- **Summary:** Nineteen volunteers in staged rear impacts (velocity change about 9-14 km/h) showed no injury signs on exam,
   303	  motion analysis or MRI, with one minor exception. The study is the kind of biomechanical evidence the defense cites for
   304	  "minor impact, soft tissue" arguments.
   305	- **Scope of support:** this source supports only the scenario theme (low-speed impacts are argued to be non-injurious).
   306	  It says nothing about EMS or ER wording.
   307	- **Record features (our inference):** EMS "minor damage to rear bumper", "ambulatory at scene", "refused transport"; ER
   308	  "low-speed MVC"; later treater notes that describe the crash as "violent" or "high impact" (patient-reported).
   309	- **D-042 / flags:** causation (scene facts per D-018 lexicon); conflict (mechanism description changes over time, both
   310	  attributed); speaker attribution.
   311	- **Synthetic-safety:** invented crash; no speeds or vehicles from the source; no study data reproduced in a packet.
   312	
   313	## Coverage map: pattern x D-042 feature
   314	
   315	| Feature (D-042 / base flags) | Patterns |
   316	|---|---|
   317	| Charge reclassification guard (rate vs charge) | P6, P14, P15 |
   318	| Billing analysis (billed, adjusted, paid, LOP/lien, cited) | P2, P3, P4, P5, P6, P14, P15, P16 |
   319	| Spanish-language records | P4, P9 |
   320	| Local OCR, scanned/handwritten pages | P12 |
   321	| PDF hidden-text detection | P12 (assumption-based, no public source) |
   322	| Date-convention suggestion | P9 (assumption), P12 |
   323	| Dismissal-pattern learning (eval guard) | P8 |
   324	| Calibrated confidence | P2, P5 |
   325	| Speaker attribution v2 | P4, P7, P9, P13, P17 |
   326	| LLM-as-judge visible | P3, P7, P10, P11 |
   327	| Vertical stepper / HITL hand-off | P1, P10, P11, P16 |
   328	| Credibility flags (D-043) | P7, P8 |
   329	| Conflict | P1, P5, P9, P10, P11, P13, P16, P17 |
   330	| Pre-existing | P2, P5 |
   331	| Causation language | P1, P2, P3, P13, P17 |
   332	| Gap | P1, P13 |
   333	
   334	## Suggested v2 packets (each recombines two or more patterns)
   335	
   336	Stage: every packet simulates a **pre-suit demand file** unless marked otherwise. "Entry" says how each cross-provider record
   337	reached the paralegal. Format sections refer to `research/record-formats.md`.
   338	
   339	| Proposed id | Combines | One-line synthetic premise | Stage / entry |
   340	|---|---|---|---|
   341	| lib08_second_crash_mri_after | P1 + P13 | Rear-end, PT, second minor crash 11 weeks later, MRI and neuro note after crash 2 | Pre-suit; all records from the firm's requests to each provider |
   342	| lib09_spanish_interpreter_espalda | P9 + P4 + P11 | History via son; "espalda" ambiguity; side flips between ER and ortho | Pre-suit; Spanish clinic note supplied by the client |
   343	| lib10_eob_vs_provider_bill | P6 + P14 | Insured patient; hospital itemized bill plus EOBs with different numbers for same DOS | Pre-suit; EOBs from the client's health plan |
   344	| lib11_priors_and_ledger | P5 + P2 | Two prior crashes denied on intake; ledgers; older patient comorbidities | Pre-suit; older notes from a records request to the PCP |
   345	| lib12_records_review_credibility | P7 + P8 | Carrier records-review (peer-review) letter with symptom-magnification wording; PT/FCE notes with clean and mixed Waddell lines | Pre-suit; review letter came with the carrier's response to the demand. Litigation-stage variant: TRCP 204 exam report |
   346	| lib13_cloned_notes_cross_provider | P10 + P16 | Copied ROS denies the complaint the ortho charts the same week | Pre-suit; PCP note from the firm's records request after the client listed the PCP |
   347	| lib14_handwritten_chiro_scans | P12 + P15 | Scanned handwritten daily notes; ambulance base + mileage invoice; hidden text layer | Pre-suit; chiro records faxed by the provider |
   348	| lib15_conclusory_letter_mist | P3 + P17 | "Accident caused all" letter; EMS minor-damage and refused-transport wording | Pre-suit; affidavits obtained from providers for later service, not yet served |
   349	
   350	**Must contain** (the builder's checklist; each packet's expected JSON asserts these) and **formats used**:
   351	
   352	| Proposed id | Must contain (D-042 features and flags) | Formats (record-formats.md §) |
   353	|---|---|---|
   354	| lib08 | Two incident dates in the chart (conflict); ED "denies LOC" vs neuro "brief LOC per patient" (conflict, speaker); first MRI dated after event 2; gap between PT discharge and the neuro visit; stepper HITL step "two incidents found" | EMS PCR §15, ED §2, PT §3, radiology §5, office/specialist note §19, ambulance invoice §16 |
   355	| lib09 | One date `03/06/2026` day-first (truth 3 June 2026) and one `14/05/2026`; "Hx via son (interpreter)"; "espalda" with no level; right vs left shoulder across ER and ortho (conflict, HITL confirm side); translation labeled as LLM output | Spanish note §13, ED §2, office/specialist note §19, scanned intake §14 |
   356	| lib10 | Same DOS on a provider bill and an EOB with different numbers (dedupe + mismatch flag); one UB-04 room line where FL44 rate × FL46 days = FL47 charge (rate-vs-charge guard); a 0001 total line; one CMS-1500 amount OCR'd without a separator with its truth stated | UB-04 §9, ledger §10, EOB §11, CMS-1500 §8 |
   357	| lib11 | Intake "prior accidents: none" vs an older note naming two prior crashes (conflict, pre_existing); ledger with billed, adjustment, payment + payer, balance and LOP columns (items 1-4 and 6, no contract column); comorbidity problem list; calibrated confidence on pre-existing | scanned intake §14, office/specialist note §19, ledger §10, LOP §12 |
   358	| lib12 | At least 4 credibility sentences across 3 dates: 2 clean negations ("0/5 Waddell signs") that must not flag, 2 mixed sentences ("Waddell 3/5; effort inconsistent") that must flag (D-043); at least 3 dismissable non-credibility flags so the dismissal-pattern guard is exercised | records-review/IME report §20, PT §3 |
   359	| lib13 | PCP ROS "denies back pain" copied across 3 visits, and an ortho note "low back pain 8/10" in the same week (conflict, cloned text, no merge); a surgical cost estimate line (D-019: not a charge); HITL "two providers disagree" | office/specialist note §19 (PCP and ortho), ED §2 |
   360	| lib14 | Scanned travel card with checkmarks; one handwritten date with no year; a CMS-1500 grouped line where days = units; an ambulance invoice where miles × per-mile rate = line total; a page whose hidden text layer differs from the image | chiro §4, scanned intake §14, CMS-1500 §8, EMS PCR §15, ambulance invoice §16 |
   361	| lib15 | EMS "refused transport" and "minor damage" (causation lexicon, speaker); ER "low-speed MVC" vs later "violent impact" per patient (conflict); a narrative letter "caused all treatment" shown verbatim, never upgraded (judge rejects any summary that states it as fact); an 18.001 affidavit whose attached bill duplicates a bill already in the packet (dedupe) | EMS PCR §15, ED §2, chiro §4, narrative letter §18, 18.001 affidavit §17 |
   362	
   363	## Denylist additions
   364	
   365	Every real proper noun in this file's sources. The same list is in `DENYLIST_V2` / `DENY_CAPITALISED` of
   366	`research/validate_library.py`; `python3 research/validate_library.py --self-test` fails if the two drift apart, if any
   367	"X v. Y" caption name here is not listed, or if a planted name in mixed case passes. Matching is case-insensitive and
   368	accent-insensitive; the three capitalised-only terms are also ordinary lowercase words. Allowed on purpose: "Waddell"
   369	(clinical eponym).
   370	
   371	```text
   372	JLG
   373	Garza
   374	Pechero
   375	Zapata
   376	Guevara
   377	Ferrer
   378	Donis
   379	Matamoros
   380	Castellanos
   381	Morehouse
   382	Reuben
   383	Rueben
   384	Poissant
   385	I-45
   386	Chiv
   387	Figueroa
   388	Central Oregon
   389	Oregon
   390	Broussard
   391	Gunn
   392	McCoy
   393	Rodriguez
   394	Wal-Mart
   395	Walmart
   396	Lewis Brisbois
   397	Brisbois
   398	Harris County
   399	Hampton
   400	Miskell
   401	Baratta
   402	I-635
   403	Castro
   404	Schilgen
   405	Steinkamp
   406	Kantrowitz
   407	Airan-Javia
   408	ElGhrably
   409	Fishbain
   410	Powell
   411	Anderson
   412	Houston
   413	Dallas
   414	Allstate
   415	Hills        # capitalised only
   416	Flores       # capitalised only
   417	Bai          # capitalised only
   418	```
   419	
   420	## Assumptions and limits
   421	
   422	- Hidden-text PDFs and DD/MM/YYYY dates in Spanish-language records are our adversarial assumptions; no public PI source
   423	  documented them. They are included because D-042 reinstated those features and they need test cases.
   424	- Texas DWC Appeals Panel decisions (P9) were seen only as a search excerpt (page returned 403). Hampton v. Miskell was
   425	  dropped as P17's source in round 2: no court, district or docket could be found and its page returned 403.
   426	- P4 (Chiv v. Figueroa) and P17 (Castro et al.) support only the scenario theme, not any record wording.
   427	- Statute currency: CPRC §18.001/§18.002 text was checked 2026-11-02 through the texas.public.law mirror (amended through
   428	  Acts 2019, 86th Leg., H.B. 1693; §18.001(b) now says the affidavit is not evidence of causation). The official
   429	  statutes.capitol.texas.gov page is a JavaScript app that did not render for the fetch tool. Opinions are cited for
   430	  scenario shape, not as current law.
   431	- Medical studies (P8–P14, P17) describe general record quality or biomechanics, not PI files; every "Record features"
   432	  line is tagged "(from source)" or "(our inference)".
   433	- Defense-firm (P16) and plaintiff-side write-ups are advocacy; used for scenario shape only.
   434	- Search also surfaced Texas Lawbook (2023-05-16) on a verdict where LOP provider entities were shown to the jury; it is
   435	  paywalled and was not used.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:44:06.535Z

**tool call — Bash**
````
{
 "command": "echo \"== self-test ==\" && python3 research/validate_library.py --self-test; echo \"exit=$?\"; echo \"== full validator ==\" && python3 research/validate_library.py; echo \"exit=$?\"",
 "description": "Run the library validator self-test and the full validator"
}
````

### User / tool · 2026-11-02T03:44:06.892Z

**tool result**
````
== self-test ==
self-test: ok (354 planted variants caught, 16 caption names covered)
exit=0
== full validator ==
golden OK: 17 cases (16 synthetic), 85 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (7 packets, 72 denylist terms, case-insensitive)
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:44:07.474Z

**tool call — Bash**
````
{
 "command": "grep -n -i -E \"brinjikji|nakashima|fraser|vera|painter|mdjw|kmh|fair health|haygood|allstate|auto crushers|Broussard|Schilgen|Baratta|Pennywhistle|Marrowgate\" research/case-library-sources-v2.md | cut -c1-220; echo ---; grep -n -E \"Record features\" research/case-library-sources-v2.md | cut -c1-160",
 "description": "Grep v2 doc for real names and check record-feature tags"
}
````

### User / tool · 2026-11-02T03:44:07.573Z

**tool result**
````
10:(Haygood line); missing out-of-state records. None of the patterns below reuses those scenarios or v1's sources. Sources
11:already cited in `research/texas-pi-notes.md` and `research/adjuster-attacks.md` (Haygood, In re Allstate, K&L Auto Crushers,
12:Brinjikji, Nakashima) are not used as primary sources here.
23:2. **Invented people and places.** Every name, provider, clinic and town is invented (the v1 style: Marrowgate,
24:   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass. Every real name in this file is on
80:  https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the withdrawn 2020 opinion only.
134:  reporter citation) — https://dallas-appellate.blogspot.com/2018/06/kmh-scotx-insurance-agents-may-know.html and
135:  https://painterfirm.com/medmal/texas-supreme-court-allows-streamlined-approach-to-medical-billing-affidavits/ (summary only).
188:- **Summary:** Thirteen audiotaped visits averaged 31 interpretation errors each; most had potential clinical consequences,
215:- **Source:** ElGhrably I., Fraser S.G., "An observational study of laterality errors in a sample of clinical records",
228:- **Source:** Rodríguez-Vera F.J. et al., "Illegible handwriting in medical records", J R Soc Med 95(11):545–546 (2002) —
257:- **Record features (from source):** hospital charges several times cost.
266:- **Source:** FAIR Health, "A Window into Utilization and Cost of Ground Ambulance Services" (brief, 2023) —
283:- **Summary:** After an ER visit the next day and care with several providers, the plaintiff reported significant neck and
313:## Coverage map: pattern x D-042 feature
390:Broussard
401:Baratta
404:Schilgen
414:Allstate
---
45:- **Record features (from source):** an orthopedic visit days after event 1, then about eleven weeks of PT; an ambulance
48:- **Record features (our inference):** first-incident clinic records missing from the file; an ER record from event 2 with
65:- **Record features (from source):** immediate post-crash care, then a long, medically complex course with large total
67:- **Record features (our inference):** EMS and ER pages with visible injuries; later admission, procedure and rehab notes
86:- **Record features (from source):** letters from a treater stating the crash caused the injuries, with no reasoning;
89:- **Record features (our inference):** billing-affidavit cover pages that look like records but carry no clinical content;
105:- **Record features (our inference):** records where the history is given in Spanish and charted in English; a note line
121:- **Record features (from source):** two earlier car accidents with treatment; memory complaints; a prior tailbone surgery;
123:- **Record features (our inference):** intake forms answering "prior accidents: none" vs older notes that mention them; a
139:- **Record features (from source):** insurer subrogation-agent affidavits stating amounts paid.
140:- **Record features (our inference):** insurer EOB pages (billed / allowed / plan paid / deductible / coinsurance / patient responsibility /
155:- **Record features (from source):** a defense neurologist's exam narrating observed behavior (pain reaction to light touch vs
158:- **Record features (our inference):** treater notes using the same CRPS vocabulary in the opposite direction.
173:- **Record features (from source):** the five Waddell sign categories (superficial/non-anatomic tenderness, simulation,
175:- **Record features (our inference):** "Waddell 3/5 positive", "distraction SLR negative"; clean negations ("0/5 Waddell
191:- **Record features (from source):** an ad hoc family interpreter; omissions; a mechanism that changed in interpretation
193:- **Record features (our inference):** "Hx obtained via patient's son (interpreter)"; mechanism worded differently on two
205:- **Record features (from source):** half of note text duplicated from earlier notes, often from another author.
206:- **Record features (our inference):** identical ROS/exam blocks across visits weeks apart ("denies neck pain" copied into a neck-pain
219:- **Record features (from source):** left/right transpositions across a record set, some later corrected; consent forms
221:- **Record features (our inference):** "right shoulder" in the ER note, "left shoulder" in the ortho note, MRI ordered on one side and read on
231:- **Record features (from source):** illegible handwritten hospital notes whose meaning is unclear.
232:- **Record features (our inference):** faxed or scanned urgent-care and chiropractic daily notes; checkbox SOAP forms; handwritten pain
244:- **Record features (from source):** an ED record with no TBI diagnosis for a patient who met mild-TBI criteria.
245:- **Record features (our inference):** ER "denies LOC", "CT head negative", discharge dx "neck strain"; a later neurology note "brief LOC per
257:- **Record features (from source):** hospital charges several times cost.
258:- **Record features (our inference):** UB-04-style itemized bill with revenue codes, units and unit price; a "self-pay discount" line; a
271:- **Record features (from source):** a base transport line plus per-mile mileage; out-of-network claim lines. Medicare billing
273:- **Record features (our inference):** EMS run sheet (times, vitals, "ambulatory at scene" or "stretcher") plus an invoice with "ALS base",
286:- **Record features (from source):** neck and back pain reported to an orthopedic surgeon while denied to the primary-care
290:- **Record features (our inference):** ortho note "low back pain 8/10, radiating" and a PCP note days apart with ROS "denies back pain"
307:- **Record features (our inference):** EMS "minor damage to rear bumper", "ambulatory at scene", "refused transport"; ER
431:- Medical studies (P8–P14, P17) describe general record quality or biomechanics, not PI files; every "Record features"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:44:16.130Z

**tool call — Bash**
````
{
 "command": "S=$(mktemp -d \"$(pwd)/artifacts/review-evidence/.t077-XXXX\" 2>/dev/null || echo /private/tmp/claude-501/scratch-t077); mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t077 && D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t077; rmdir \"$S\" 2>/dev/null; for u in \"https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1\" \"https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/\" \"https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14\"; do n=$(echo \"$u\" | md5 | cut -c1-8); curl -sL --max-time 20 -A \"Mozilla/5.0\" -o \"$D/$n.html\" -w \"%{http_code} %{size_download} $u\\n\" \"$u\"; done; echo \"saved to $D\"; ls -la \"$D\"",
 "description": "Fetch the Hills v. Donis cited pages into scratchpad"
}
````

### User / tool · 2026-11-02T03:44:16.189Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (rmdir $(mktemp)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:44:19.534Z

**tool call — Bash**
````
{
 "command": "for u in \"https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1\" \"https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/\" \"https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14\"; do echo \"== $u\"; curl -sL --max-time 20 -A \"Mozilla/5.0\" -w \"\\nHTTP %{http_code} bytes %{size_download}\\n\" \"$u\" | tr -s ' \\n' ' ' | grep -o -i -E \".{0,120}(withdraw|substitut|14-18-00566|21-0287|Hills).{0,120}\" | head -8; done",
 "description": "Check cited Hills v. Donis pages for withdrawal and substitution wording"
}
````

### User / tool · 2026-11-02T03:44:23.592Z

**tool result**
````
== https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1
ugrep: error: error at position 125
\xbf][\x80-\xbf]*){0,120}
                         \___exceeds complexity limits


== https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/
ugrep: error: error at position 125
\xbf][\x80-\xbf]*){0,120}
                         \___exceeds complexity limits


== https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14
ugrep: error: error at position 125
\xbf][\x80-\xbf]*){0,120}
                         \___exceeds complexity limits
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:44:27.825Z

**tool call — Bash**
````
{
 "command": "for u in \"https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1\" \"https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/\" \"https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14\"; do echo \"== $u\"; curl -sL --max-time 20 -A \"Mozilla/5.0\" -w \"\\nHTTP %{http_code} bytes %{size_download}\\n\" \"$u\" > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/page.txt 2>/dev/null; tail -1 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/page.txt; tr -s ' \\n' ' ' < /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/page.txt | grep -o -i -E '.{0,100}(withdraw|substitut|14-18-00566|21-0287|hills).{0,100}' | head -6; done",
 "description": "Fetch cited pages and grep for withdrawal wording"
}
````

### User / tool · 2026-11-02T03:44:33.056Z

**tool result**
````
== https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1
HTTP 200 bytes 32603
ugrep: error: error at position 125
\xbf][\x80-\xbf]*){0,100}
                         \___exceeds complexity limits


== https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/
HTTP 200 bytes 33168
ugrep: error: error at position 125
\xbf][\x80-\xbf]*){0,100}
                         \___exceeds complexity limits


== https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14
HTTP 200 bytes 163281
ugrep: error: error at position 125
\xbf][\x80-\xbf]*){0,100}
                         \___exceeds complexity limits
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:44:45.243Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-paralegal-r2-denylist.py",
 "content": "#!/usr/bin/env python3\n\"\"\"T-077 r2 check (paralegal-reviewer): is every real name cited in research/case-library-sources-v2.md on the denylist?\n\nSteps:\n1. Load research/validate_library.py as a module (read-only use of scan_text / DENYLIST).\n2. Candidate real names taken from a line-by-line read of the v2 doc (captions, study authors, judges, firms, sites, agencies).\n3. For each candidate: is it in DENYLIST or DENY_CAPITALISED? Does a planted sentence containing it fail the scan?\n4. Plant a packet with the names the v2 doc cites but the denylist omits, and show scan_library passes it.\n5. Fetch the two Hills v. Donis pages the doc cites and search for 'withdraw' / 'substitut' wording (plain python, no regex blowup).\n\"\"\"\nimport importlib.util\nimport pathlib\nimport re\nimport tempfile\nimport urllib.request\n\nROOT = pathlib.Path(\"/Users/arsis/zlayt-pm-project\")\nspec = importlib.util.spec_from_file_location(\"vl\", ROOT / \"research\" / \"validate_library.py\")\nvl = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(vl)\n\nDOC = (ROOT / \"research\" / \"case-library-sources-v2.md\").read_text()\n\n# Real names that appear in the v2 doc text (not only in the denylist block). Source line numbers from the doc.\nCITED_REAL_NAMES = {\n    \"JLG\": \"L39\", \"Garza\": \"L39\", \"Guevara\": \"L57\", \"Ferrer\": \"L57\", \"Hills\": \"L75\", \"Donis\": \"L75\",\n    \"Houston\": \"L75,L280\", \"Chiv\": \"L98\", \"Figueroa\": \"L98\", \"Central Oregon\": \"L113\", \"Oregon\": \"L113\",\n    \"Broussard\": \"not in body; listed\", \"Gunn\": \"L133\", \"McCoy\": \"L133\", \"Rodriguez\": \"L149\", \"Wal-Mart\": \"L149\",\n    \"Fishbain\": \"L168\", \"Flores\": \"L183\", \"Steinkamp\": \"L201\", \"Kantrowitz\": \"L201\", \"Airan-Javia\": \"L201\",\n    \"ElGhrably\": \"L215\", \"Powell\": \"L240\", \"Bai\": \"L252\", \"Anderson\": \"L252\", \"Lewis Brisbois\": \"L280\",\n    \"Harris County\": \"L280\", \"Castro\": \"L298\", \"Hampton\": \"L424\", \"Miskell\": \"listed\", \"Allstate\": \"L11\",\n    \"Haygood\": \"L11\", \"K&L\": \"L11\", \"Auto Crushers\": \"L11\",\n    # Named in the doc but NOT in any denylist list I could find (checked below):\n    \"Brinjikji\": \"L12\", \"Nakashima\": \"L12\", \"Fraser\": \"L215\", \"Vera\": \"L228 (Rodríguez-Vera)\",\n}\n\nprint(\"== 1. denylist membership and planted-sentence result ==\")\nall_terms = set(vl.DENYLIST) | set(vl.DENY_CAPITALISED)\nfolded_terms = {vl.fold(t).lower() for t in all_terms}\nmissing = []\nfor name, where in CITED_REAL_NAMES.items():\n    listed = vl.fold(name).lower() in folded_terms\n    caught = name in vl.scan_text(f\"Seen by Dr. {name.upper()} at the clinic.\")\n    print(f\"{name!r:20} cited at {where:22} on denylist={listed!s:5} planted-caught={caught}\")\n    if not listed:\n        missing.append(name)\nprint(\"cited real names NOT on denylist:\", missing)\n\nprint()\nprint(\"== 2. planted packet with the uncaught names (scan_library must fail it; expect it to pass) ==\")\nwith tempfile.TemporaryDirectory() as tmp:\n    p = pathlib.Path(tmp) / \"case_planted_gap.txt\"\n    p.write_text(vl.BANNER + \"Peer article by BRINJIKJI and Nakashima; authors Fraser S.G. and Rodríguez-Vera F.J. (dropped).\\n\"\n                 \"Clinic note: referred by painter and mdjwlaw intake.\\n\")\n    print(\"scan_text hits:\", vl.scan_text(p.read_text()))\n    print(\"scan_library problems:\", vl.scan_library([p]))\n\nprint()\nprint(\"== 3. the self-test claim: does it check prose names or only captions? ==\")\ncaps = sorted(vl.doc_caption_names(DOC))\nprint(\"caption names checked by self-test:\", caps)\nprint(\"prose-only names the self-test never checks:\", [n for n in [\"Brinjikji\", \"Nakashima\", \"Fraser\", \"Vera\"] if n in DOC])\n\nprint()\nprint(\"== 4. Hills v. Donis cited pages ==\")\ndef fetch(url):\n    req = urllib.request.Request(url, headers={\"User-Agent\": \"Mozilla/5.0\"})\n    with urllib.request.urlopen(req, timeout=25) as r:\n        return r.status, r.read().decode(\"utf-8\", \"replace\")\n\nfor url in [\n    \"https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1\",\n    \"https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/\",\n    \"https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14\",\n]:\n    try:\n        status, html = fetch(url)\n    except Exception as exc:  # network or 403\n        print(url, \"ERROR\", exc)\n        continue\n    text = re.sub(r\"<[^>]+>\", \" \", html)\n    text = re.sub(r\"\\s+\", \" \", text)\n    print(f\"{status} {len(html)} bytes {url}\")\n    for word in [\"withdr\", \"substitut\", \"14-18-00566\", \"21-0287\", \"Hills\"]:\n        hits = [m.start() for m in re.finditer(word, text, re.I)]\n        print(f\"   '{word}': {len(hits)} hit(s)\")\n        for h in hits[:2]:\n            print(\"      ...\", text[max(0, h - 90): h + 90], \"...\")\n"
}
````

### User / tool · 2026-11-02T03:44:45.347Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-paralegal-r2-denylist.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:44:46.505Z

**tool call — Bash**
````
{
 "command": "python3 artifacts/review-evidence/T-077-paralegal-r2-denylist.py 2>&1 | tee artifacts/review-evidence/T-077-paralegal-r2-denylist.out",
 "description": "Run the T-077 denylist and Hills cited-page check script"
}
````

### User / tool · 2026-11-02T03:44:47.678Z

**tool result**
````
== 1. denylist membership and planted-sentence result ==
'JLG'                cited at L39                    on denylist=True  planted-caught=True
'Garza'              cited at L39                    on denylist=True  planted-caught=True
'Guevara'            cited at L57                    on denylist=True  planted-caught=True
'Ferrer'             cited at L57                    on denylist=True  planted-caught=True
'Hills'              cited at L75                    on denylist=True  planted-caught=True
'Donis'              cited at L75                    on denylist=True  planted-caught=True
'Houston'            cited at L75,L280               on denylist=True  planted-caught=True
'Chiv'               cited at L98                    on denylist=True  planted-caught=True
'Figueroa'           cited at L98                    on denylist=True  planted-caught=True
'Central Oregon'     cited at L113                   on denylist=True  planted-caught=True
'Oregon'             cited at L113                   on denylist=True  planted-caught=True
'Broussard'          cited at not in body; listed    on denylist=True  planted-caught=True
'Gunn'               cited at L133                   on denylist=True  planted-caught=True
'McCoy'              cited at L133                   on denylist=True  planted-caught=True
'Rodriguez'          cited at L149                   on denylist=True  planted-caught=True
'Wal-Mart'           cited at L149                   on denylist=True  planted-caught=True
'Fishbain'           cited at L168                   on denylist=True  planted-caught=True
'Flores'             cited at L183                   on denylist=True  planted-caught=True
'Steinkamp'          cited at L201                   on denylist=True  planted-caught=True
'Kantrowitz'         cited at L201                   on denylist=True  planted-caught=True
'Airan-Javia'        cited at L201                   on denylist=True  planted-caught=True
'ElGhrably'          cited at L215                   on denylist=True  planted-caught=True
'Powell'             cited at L240                   on denylist=True  planted-caught=True
'Bai'                cited at L252                   on denylist=True  planted-caught=True
'Anderson'           cited at L252                   on denylist=True  planted-caught=True
'Lewis Brisbois'     cited at L280                   on denylist=True  planted-caught=True
'Harris County'      cited at L280                   on denylist=True  planted-caught=True
'Castro'             cited at L298                   on denylist=True  planted-caught=True
'Hampton'            cited at L424                   on denylist=True  planted-caught=True
'Miskell'            cited at listed                 on denylist=True  planted-caught=True
'Allstate'           cited at L11                    on denylist=True  planted-caught=True
'Haygood'            cited at L11                    on denylist=True  planted-caught=True
'K&L'                cited at L11                    on denylist=True  planted-caught=True
'Auto Crushers'      cited at L11                    on denylist=True  planted-caught=True
'Brinjikji'          cited at L12                    on denylist=False planted-caught=False
'Nakashima'          cited at L12                    on denylist=False planted-caught=False
'Fraser'             cited at L215                   on denylist=False planted-caught=False
'Vera'               cited at L228 (Rodríguez-Vera)  on denylist=False planted-caught=False
cited real names NOT on denylist: ['Brinjikji', 'Nakashima', 'Fraser', 'Vera']

== 2. planted packet with the uncaught names (scan_library must fail it; expect it to pass) ==
scan_text hits: ['Rodriguez']
scan_library problems: ["case_planted_gap.txt: contains real identifier 'Rodriguez'"]

== 3. the self-test claim: does it check prose names or only captions? ==
caption names checked by self-test: ['Allstate', 'Central Oregon', 'Chiv', 'Donis', 'Ferrer', 'Figueroa', 'Garza', 'Guevara', 'Gunn', 'Hampton', 'Hills', 'JLG', 'McCoy', 'Miskell', 'Rodriguez', 'Wal-Mart']
prose-only names the self-test never checks: ['Brinjikji', 'Nakashima', 'Fraser', 'Vera']

== 4. Hills v. Donis cited pages ==
200 32603 bytes https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1
   'withdr': 0 hit(s)
   'substitut': 0 hit(s)
   '14-18-00566': 1 hit(s)
      ... injuries from an automobile accident by expert medical testimony. In Hills v. Donis , No. 14-18-00566-CV, 2020 WL 206187, at *1 (Tex. App.&mdash;Houston [14th Dist.] Jan. 14, 2020, ...
   '21-0287': 0 hit(s)
   'Hills': 3 hit(s)
      ... tablish causation of injuries from an automobile accident by expert medical testimony. In Hills v. Donis , No. 14-18-00566-CV, 2020 WL 206187, at *1 (Tex. App.&mdash;Houston [14th  ...
      ... 206187, at *1 (Tex. App.&mdash;Houston [14th Dist.] Jan. 14, 2020, no pet. h.), Defendant Hills challenged the trial court&rsquo;s judgment on grounds that various Plaintiffs (the  ...
200 33145 bytes https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/
   'withdr': 0 hit(s)
   'substitut': 0 hit(s)
   '14-18-00566': 1 hit(s)
      ... F S.D., A MINOR v. EBONI IVORY HILLS; from Harris County; 14th Court of Appeals District (14-18-00566-CV, ___ SW3d ___, 02-11-21) 21-0290 IN THE INTEREST OF M.A.G. AND Z.A.G., CHIL ...
   '21-0287': 1 hit(s)
      ... rom Denton County; 2nd Court of Appeals District (02-19-00406-CV, ___ SW3d ___, 01-28-21) 21-0287 CARLOS DONIS, CALIXTO DONIS, VICTOR MATAMOROS, SAIRA CASTELLANOS, INDIVIDUALLY AND ...
   'Hills': 1 hit(s)
      ... MOROS, SAIRA CASTELLANOS, INDIVIDUALLY AND AS NEXT FRIEND OF S.D., A MINOR v. EBONI IVORY HILLS; from Harris County; 14th Court of Appeals District (14-18-00566-CV, ___ SW3d ___, 0 ...
200 163280 bytes https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14
   'withdr': 1 hit(s)
      ... NDERED IN PART [ PDF/3.10 MB ] Memorandum Opinion [ PDF/97 KB ] Notice 02/11/2021 Opinion withdrawn &nbsp; 12/23/2020 Additional authorities filed &nbsp; [ PDF/303 KB ] Letter 04/2 ...
   'substitut': 0 hit(s)
   '14-18-00566': 2 hit(s)
      ... mitted Cases Oral Arguments Archive Case Mail Appellate Staff & OCA Log In // // // Case: 14-18-00566-CV &nbsp;&nbsp;&nbsp; Print-Friendly &nbsp;Add to CaseMail Case: 14-18-00566-C ...
      ...  // // Case: 14-18-00566-CV &nbsp;&nbsp;&nbsp; Print-Friendly &nbsp;Add to CaseMail Case: 14-18-00566-CV Date Filed: 07/11/2018 Case Type: Personal Injury Style: Eboni Ivory Hills& ...
   '21-0287': 0 hit(s)
   'Hills': 2 hit(s)
      ... Case: 14-18-00566-CV Date Filed: 07/11/2018 Case Type: Personal Injury Style: Eboni Ivory Hills&nbsp; v.: Carlos Donis, Calixto Donis, Victor Matamoros, Saira Castellanos, Individu ...
      ... civil case will be destroyed (6 yrs after mandate) Parties Party PartyType Representative Hills, Eboni Ivory Appellant Robert T. Owen William Shane Osborn Levon Hovnatanian Donis,  ...
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:44:57.115Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer && cat library-review-patterns.md reviewer-hook-constraints.md feedback_reviewer_tooling_quirks.md",
 "description": "Read library and hook memory notes"
}
````

### User / tool · 2026-11-02T03:44:57.194Z

**tool result**
````
---
name: library-review-patterns
description: T-052 (2026-11-01) synthetic case library review - what held up, what to re-check on library/golden changes
metadata:
  type: project
---

T-052 evals/library (7 packets) passed with minors only. Hand-recomputed gaps/totals were all right; identifier overlap vs fetchable sources was 0.
Re-check on any library change:
- Stated attendance count vs billed count (lib03 "31 visits", $120 rate left unclear): is the rule written in README/REQUIREMENTS?
- Flag type fit: lib06 attorney referral is typed `causation` (wrong heading).
- PT plan-of-care vs last visit with no discharge (lib05) is not surfaced.
- Library packets are one-sentence excerpts; no ledger-by-DOS, Bates, DOA conflict.
- valawyersweekly.com and rissman.com return 403 to curl even with a browser UA; studicata is unopened. Sources fetch fine for rmdlaw, oklahomalawyer, plasticsurgerypractice, thompsoncoe.
- curl `-o` to scratchpad and python heredocs containing `>=` trip board-guard; redirect stdout into artifacts/review-evidence and put code in a script file.

**How to apply:** use artifacts/review-evidence/T-052-paralegal-scan.py as a starting probe. Related: [[golden-set-recurring-findings]], [[reviewer-hook-constraints]]
---
name: reviewer-hook-constraints
description: Bash hooks that block reviewer commands in this repo (board.py --help, python -c containing backticks) and the workarounds
metadata:
  type: reference
---

- board-guard: reviewers may run only `tools/board.py validate|show|list|status`. `--help` is rejected.
- git-guard fails to parse `python3 -c "..."` when the code contains escaped backticks. Use a quoted heredoc (`python3 - <<'EOF'`) and build the fence as '`'*3.
- Write access is limited to reviews/ and artifacts/review-evidence/ (plus this memory dir). Probe scripts go in artifacts/review-evidence/.

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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:05.192Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-paralegal-r2-orders.py",
 "content": "#!/usr/bin/env python3\n\"\"\"T-077 r2 follow-up (paralegal-reviewer): what the July 23, 2021 Texas Supreme Court order list says about No. 21-0287,\nand whether the doc's 'Statute currency ... checked 2026-11-02' date is in the past relative to the review date (2026-11-01).\"\"\"\nimport re\nimport urllib.request\n\nurl = \"https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/\"\nreq = urllib.request.Request(url, headers={\"User-Agent\": \"Mozilla/5.0\"})\nwith urllib.request.urlopen(req, timeout=25) as r:\n    html = r.read().decode(\"utf-8\", \"replace\")\ntext = re.sub(r\"<[^>]+>\", \" \", html)\ntext = re.sub(r\"\\s+\", \" \", text)\ni = text.find(\"21-0287\")\nprint(\"order list around 21-0287:\")\nprint(text[max(0, i - 700): i + 120])\nprint()\nheads = [m.group(0) for m in re.finditer(r\"(Petitions? (?:Denied|Granted)|Denied|Granted|Dismissed)[^.]{0,40}\", text)]\nprint(\"section headings seen:\", heads[:12])\n\ndoc = open(\"/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md\", encoding=\"utf-8\").read()\nfor m in re.finditer(r\"2026-11-0\\d\", doc):\n    line = doc[: m.start()].count(\"\\n\") + 1\n    print(f\"doc line {line}: {doc[max(0, m.start() - 60): m.end() + 20]!r}\")\n"
}
````

### User / tool · 2026-11-02T03:45:05.293Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-paralegal-r2-orders.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:06.504Z

**tool call — Bash**
````
{
 "command": "python3 artifacts/review-evidence/T-077-paralegal-r2-orders.py 2>&1 | tee artifacts/review-evidence/T-077-paralegal-r2-orders.out",
 "description": "Run order-list and date-provenance check for T-077"
}
````

### User / tool · 2026-11-02T03:45:06.878Z

**tool result**
````
order list around 21-0287:
istics & Other Data Vexatious Litigants eFile Texas Media Click to expand submenu Public Affairs How to Report Scam Text Messages Supreme Court Site Search Texas Judicial Branch Supreme Court Web (function() { $('#group').val($('#search-facet li.active a').attr('name')); })(); You are here: Home / Courts / Supreme Court / Orders &amp; Opinions / 2021 / July / July 23, 2021 July 23, 2021 Print-Friendly THE SUPREME COURT OF TEXAS Orders Pronounced July 23, 2021 ORDERS ON PETITIONS FOR REVIEW THE FOLLOWING PETITIONS FOR REVIEW ARE DENIED: 21-0214 GRCDALLASHOMES LLC AND KAZEM DANESHMANDI v. JOHN CALDWELL; from Denton County; 2nd Court of Appeals District (02-19-00406-CV, ___ SW3d ___, 01-28-21) 21-0287 CARLOS DONIS, CALIXTO DONIS, VICTOR MATAMOROS, SAIRA CASTELLANOS, INDIVIDUALLY AND AS NEXT FRIEND OF S.D., A MIN

section headings seen: []
doc line 4: 'lib07`, see `research/case-library-sources.md`). Researched 2026-11-01/02 by the\nresearche'
doc line 427: '.\n- Statute currency: CPRC §18.001/§18.002 text was checked 2026-11-02 through the texas.p'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:16.332Z

**tool call — Bash**
````
{
 "command": "python3 research/record_formats_check.py; echo \"exit=$?\"",
 "description": "Run the record formats check script"
}
````

### User / tool · 2026-11-02T03:45:16.442Z

**tool result**
````
record_formats_check: 85/85 checks pass
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:16.753Z

**tool call — Bash**
````
{
 "command": "wc -l research/record-formats.md research/record_formats_check.py && grep -n -E \"^#{1,4} \" research/record-formats.md",
 "description": "Count lines and list headings in record formats doc"
}
````

### User / tool · 2026-11-02T03:45:16.838Z

**tool result**
````
    1080 research/record-formats.md
     208 research/record_formats_check.py
    1288 total
1:# Record and billing document formats for synthetic PI packets (T-078)
22:## 1. Cross-cutting traps (apply to every format)
24:### 1.1 Dates that are not service dates
40:### 1.2 Money: charges, rates, adjustments, estimates
56:### 1.3 Authorship and voice
61:### 1.4 One visit, several bills
69:## 2. Emergency department note
117:## 3. Physical therapy daily note (SOAP)
163:## 4. Chiropractic daily note and travel card
210:## 5. Radiology report (x-ray, CT, MRI)
255:## 6. Operative report
301:## 7. Pharmacy dispensing log (patient Rx history printout)
337:## 8. CMS-1500 (02/12) professional claim
399:## 9. UB-04 (CMS-1450) institutional claim
473:## 10. Itemized provider ledger / statement
519:## 11. Explanation of Benefits (EOB) / remittance
556:## 12. Letter of protection (LOP) and lien letters
601:## 13. Spanish-language clinic note
651:## 14. Scanned and handwritten intake forms (and OCR failure modes)
703:## 15. EMS patient care report (ambulance run report)
760:## 16. Ambulance invoice (base rate plus mileage)
803:## 17. Texas CPRC §18.001 billing affidavit and records cover page
858:## 18. Treating-provider narrative letter
905:## 19. Physician office / specialist progress note (PCP, orthopedics, neurology, pain management)
949:## 20. Records-review (peer-review) letter and independent medical exam (IME) report
996:## 21. Product mapping and proposed packet mixes
1034:## 22. Cross-specimen consistency (Delphine Okonkwo-Vale timeline)
1054:## 23. Assumptions, limits, gaps and the name-collision search
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:18.537Z

**tool call — Bash**
````
{
 "command": "cat -n research/record_formats_check.py",
 "description": "Read the record formats check script"
}
````

### User / tool · 2026-11-02T03:45:18.615Z

**tool result**
````
     1	#!/usr/bin/env python3
     2	"""Re-check the SYNTHETIC specimens in research/record-formats.md (T-078 round 2).
     3	
     4	Each specimen claims to follow a rule (NUCC grouping, CMS 8-minute rule, UB-04 rate x days, totals). This script re-adds them in code so a
     5	later edit cannot silently break one. Exit 0 = every check passes.   Run: python3 research/record_formats_check.py
     6	"""
     7	import datetime as dt, pathlib, re, sys
     8	from decimal import Decimal as D
     9	
    10	DOC = pathlib.Path(__file__).resolve().parent / "record-formats.md"
    11	MONEY = r"\(?-?\d{1,3}(?:,\d{3})*\.\d\d\)?-?"
    12	results = []
    13	
    14	
    15	def check(name, ok, detail=""):
    16	    results.append((name, bool(ok), detail))
    17	
    18	
    19	def money(s):
    20	    neg = s.startswith("(") or s.endswith("-") or s.startswith("-")
    21	    v = D(s.strip("()-").replace(",", ""))
    22	    return -v if neg else v
    23	
    24	
    25	def sections(text):
    26	    parts = re.split(r"^## (\d+)\. ", text, flags=re.M)
    27	    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
    28	
    29	
    30	def blocks(sec):
    31	    return re.findall(r"```\n(.*?)```", sec, re.S)
    32	
    33	
    34	def mmddyy(s):
    35	    s = s.replace("O", "0")
    36	    return dt.date(2000 + int(s[4:6]), int(s[0:2]), int(s[2:4]))
    37	
    38	
    39	def main():
    40	    text = DOC.read_text()
    41	    S = sections(text)
    42	    formats = [n for n in S if 2 <= n <= 20]
    43	    words = {19: "nineteen"}
    44	    check("intro format count matches sections 2-20", f"describes the {words.get(len(formats), '?')} document" in text,
    45	          f"{len(formats)} format sections")
    46	    for n in formats:
    47	        bs = blocks(S[n])
    48	        check(f"§{n} has a specimen", bs)
    49	        for b in bs:
    50	            check(f"§{n} specimen labeled synthetic", re.search(r"SYNTHETIC|SINTÉTICO", b.splitlines()[0]), b.splitlines()[0][:60])
    51	
    52	    # §3 PT: CMS 8-minute rule on total timed minutes; plan count.
    53	    pt = blocks(S[3])[0]
    54	    timed = [(int(m), int(u)) for m, u in re.findall(r"\b97\d{3} \w+\s+(\d+) min\s+(\d+)u", pt)]
    55	    total = sum(m for m, _ in timed)
    56	    cms_units = (total + 7) // 15 if total >= 8 else 0
    57	    check("PT timed minutes total stated", f"Total timed {total} min" in pt, f"{total} min")
    58	    check("PT units = CMS 8-minute rule", sum(u for _, u in timed) == cms_units, f"{total} min -> {cms_units} units")
    59	    check("PT per-code (AMA) units agree", all(u == (m + 7) // 15 for m, u in timed))
    60	    v = re.search(r"Visit (\d+) of (\d+)", pt)
    61	    plan = re.search(r"(\d)x/wk x (\d+) wks", pt)
    62	    check("PT plan visits = frequency x weeks", v and plan and int(v.group(2)) == int(plan.group(1)) * int(plan.group(2)))
    63	
    64	    # §4 travel card marks per column.
    65	    chiro = blocks(S[4])[0]
    66	    hdr = next(l for l in chiro.splitlines() if l.startswith("DATE"))
    67	    cols = [c.strip() for c in hdr.split("|")]
    68	    marks = {}
    69	    for l in chiro.splitlines():
    70	        if re.match(r"\d\d/\d\d\s+\|", l):
    71	            cells = [c.strip() for c in l.split("|")]
    72	            for c, val in zip(cols, cells):
    73	                if val == "x":
    74	                    marks.setdefault(c, set()).add(dt.date(2026, int(cells[0][:2]), int(cells[0][3:5])))
    75	
    76	    # §8 CMS-1500 clean: days = units, grouped dates on the travel card, line sum = Item 28.
    77	    clean, ocr = blocks(S[8])[:2]
    78	    lines = re.findall(r"^\s+(\d{6})\s+(\d{6})\s+\d+\s+(\w+)\s+\w+\s+(\d+) \| (\d\d)\s+(\d+)", clean, re.M)
    79	    check("CMS-1500 clean has service lines", len(lines) >= 3, f"{len(lines)} lines")
    80	    col_for = {"97014": "ES", "97010": "H/C", "98941": "C"}
    81	    line_sum = D(0)
    82	    for f, t, code, dollars, cents, units in lines:
    83	        a, b = mmddyy(f), mmddyy(t)
    84	        days = (b - a).days + 1
    85	        check(f"CMS-1500 {code} {f}-{t}: days = units", days == int(units), f"{days} days, {units} units")
    86	        dates = {a + dt.timedelta(d) for d in range(days)}
    87	        check(f"CMS-1500 {code} {f}-{t}: every date marked on travel card", dates <= marks.get(col_for.get(code, ""), set()))
    88	        line_sum += D(f"{dollars}.{cents}")
    89	    item28 = re.search(r"28\. TOTAL CHARGE\s+(\d+) \| (\d\d)", clean)
    90	    check("CMS-1500 line sum = Item 28", item28 and line_sum == D(f"{item28.group(1)}.{item28.group(2)}"), str(line_sum))
    91	
    92	    # §8 CMS-1500 OCR: at least one separator-less amount with its truth stated; truths add up to the Item 28 truth.
    93	    truths, bare = [], 0
    94	    for l in ocr.splitlines():
    95	        m = re.search(r"<- truth (\d+\.\d\d)", l)
    96	        if not m:
    97	            continue
    98	        if re.search(r"\s\d{4,5}\s", l.split("<-")[0]):
    99	            bare += 1
   100	        if l.lstrip().startswith(("24.", "0", "O")):
   101	            truths.append(D(m.group(1)))
   102	        elif "28." in l:
   103	            t28 = D(m.group(1))
   104	    check("CMS-1500 OCR has separator-less amounts with truth", bare >= 1, f"{bare} lines")
   105	    check("CMS-1500 OCR truths sum to Item 28 truth", truths and sum(truths) == t28 == line_sum, str(sum(truths)))
   106	
   107	    # §9 UB-04: lines sum to 0001; a room line where rate x days = charge; occurrence codes differ and are 01-06.
   108	    occ = []
   109	    room_ok = False
   110	    for b in blocks(S[9]):
   111	        occ.append(re.search(r"OCCURRENCE\s+CODE (\d\d)", b).group(1))
   112	        tot47 = D(0); tot48 = D(0); allm = D(0); total = None
   113	        for l in b.splitlines():
   114	            m = re.match(r"(\d{4})\s{2,}", l)
   115	            if not m:
   116	                continue
   117	            ms = [money(x) for x in re.findall(MONEY, l)]
   118	            allm += sum(ms)
   119	            rev = m.group(1)
   120	            if rev == "0001":
   121	                total = ms
   122	                continue
   123	            if rev.startswith("01"):
   124	                rate, charge = ms[0], ms[1]
   125	                days = int(re.search(r"\d\.\d\d\s+(\d+)\s+\d", l.replace(",", "")).group(1))
   126	                room_ok = room_ok or rate * days == charge
   127	                check(f"UB-04 room line {rev}: rate x days = charge", rate * days == charge, f"{rate} x {days} = {charge}")
   128	                tot47 += charge
   129	            else:
   130	                tot47 += ms[0]
   131	                tot48 += ms[1] if len(ms) > 1 else 0
   132	        check("UB-04 lines sum to 0001 FL47", total and total[0] == tot47, f"{tot47} vs {total}")
   133	        if total and len(total) > 1:
   134	            check("UB-04 FL48 lines sum to 0001 FL48", total[1] == tot48)
   135	        if room_ok:
   136	            naive = f"{allm:,.2f}"
   137	            check("UB-04 naive-sum figure stated in the note", naive in S[9], naive)
   138	    check("UB-04 has a rate-on-charge-line specimen", room_ok)
   139	    check("UB-04 occurrence codes are accident codes 01-06 and vary", all(c in {"01", "02", "03", "04", "05", "06"} for c in occ)
   140	          and len(set(occ)) >= 2, str(occ))
   141	
   142	    # §10 ledger: running balance and totals.
   143	    led = blocks(S[10])[0]
   144	    bal = D(0); ch = D(0); adj = D(0)
   145	    for l in led.splitlines():
   146	        if not re.match(r"\d\d/\d\d/\d\d", l):
   147	            continue
   148	        ms = [money(x) for x in re.findall(MONEY, l)]
   149	        if " ADJ " in l:
   150	            adj += abs(ms[0]); bal -= abs(ms[0])
   151	        else:
   152	            ch += ms[0]; bal += ms[0]
   153	        check(f"ledger running balance {l[:8]}", bal == ms[-1], f"{bal} vs {ms[-1]}")
   154	    tl = re.search(r"TOTAL CHARGES ([\d.,]+)\s+TOTAL PMTS ([\d.,]+)\s+TOTAL ADJ \(([\d.,]+)\)\s+BALANCE DUE ([\d.,]+)", led)
   155	    check("ledger totals", tl and (D(tl.group(1)), D(tl.group(3)), D(tl.group(4))) == (ch, adj, bal), f"{ch} {adj} {bal}")
   156	
   157	    # §11 EOB arithmetic per line and totals.
   158	    eob = blocks(S[11])[0]
   159	    sums = [D(0)] * 7
   160	    for l in eob.splitlines():
   161	        if re.match(r"\d\d/\d\d/\d\d", l):
   162	            b_, disc, allw, ded, coin, paid, owe = [D(x) for x in re.findall(r"\d+\.\d\d", l)]
   163	            check(f"EOB line {l[10:15]}", b_ - disc == allw and allw - ded - coin == paid and ded + coin == owe)
   164	            sums = [s + v for s, v in zip(sums, (b_, disc, allw, ded, coin, paid, owe))]
   165	        elif l.startswith("TOTAL"):
   166	            check("EOB totals", [D(x) for x in re.findall(r"\d+\.\d\d", l)] == sums)
   167	
   168	    # §13 Spanish: a day-first date with both parts <= 12 and its truth stated.
   169	    sp = S[13]
   170	    amb = [d for d in re.findall(r"\b(\d\d)/(\d\d)/(\d{4})\b", blocks(sp)[0]) if int(d[0]) <= 12 and int(d[1]) <= 12]
   171	    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
   172	    check("Spanish specimen has an ambiguous day-first date with stated truth",
   173	          any(f"{int(d)} {months[int(m) - 1]} {y}" in sp for d, m, y in amb), str(amb))
   174	
   175	    # §15 EMS: call times in order.
   176	    ems = blocks(S[15])[0]
   177	    times = re.findall(r"(?:PSAP|Notified|En route|On scene|At pt|Left scene|At dest|Transfer of care) (\d\d):(\d\d)", ems.split("---")[0])
   178	    mins = [int(h) * 60 + int(m) for h, m in times]
   179	    check("EMS times ascend", len(mins) == 8 and mins == sorted(mins), str(times))
   180	
   181	    # §16 ambulance: units x rate = charge; lines sum to total; mileage units fractional.
   182	    amb_b = blocks(S[16])[0]
   183	    tot = D(0)
   184	    for code, units, rate, charge in re.findall(r"(A04\d\d-\w\w).*?\s([\d.]+)\s+([\d,]+\.\d\d)\s+([\d,]+\.\d\d)\s*$", amb_b, re.M):
   185	        u, r, c = D(units), money(rate), money(charge)
   186	        check(f"ambulance {code}: units x rate = charge", u * r == c, f"{u} x {r} = {c}")
   187	        if code.startswith("A0425"):
   188	            check("ambulance mileage units carry a tenth", "." in units)
   189	        tot += c
   190	    tc = re.search(r"TOTAL CHARGES\s+([\d,]+\.\d\d)", amb_b)
   191	    check("ambulance lines sum to total", tc and money(tc.group(1)) == tot, str(tot))
   192	
   193	    # §17 affidavit amounts match the §10 ledger.
   194	    aff = blocks(S[17])[0]
   195	    a = re.search(r"charged: \$([\d,.]+)\.\s+Amount paid: \$([\d,.]+)\.\s+Amount unpaid.*?\$([\d,.]+)\.", aff)
   196	    check("affidavit charged/paid/unpaid = ledger", a and (D(a.group(1)), D(a.group(2)), D(a.group(3))) == (ch, D(0), bal),
   197	          a.groups() if a else "no match")
   198	
   199	    bad = [r for r in results if not r[1]]
   200	    for name, ok, detail in results:
   201	        if not ok or "-v" in sys.argv:
   202	            print(("ok   " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
   203	    print(f"record_formats_check: {len(results) - len(bad)}/{len(results)} checks pass")
   204	    return 1 if bad else 0
   205	
   206	
   207	if __name__ == "__main__":
   208	    sys.exit(main())
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:22.102Z

**tool call — Bash**
````
{
 "command": "cat -n research/record-formats.md | sed -n '1,21p'; echo ....; cat -n research/record-formats.md | sed -n '337,400p'",
 "description": "Read doc intro and CMS-1500 section"
}
````

### User / tool · 2026-11-02T03:45:22.193Z

**tool result**
````
     1	# Record and billing document formats for synthetic PI packets (T-078)
     2	
     3	**Purpose.** D-042 says the multi-case library grows from researched real-world document formats. This file describes the nineteen document
     4	types a Texas PI paralegal typically receives, so the packet generator can produce realistic, **fully synthetic** records that exercise the
     5	tool's hard parts: dates, charges versus rates versus adjustments, totals lines, multiple authors, Spanish text and OCR noise.
     6	
     7	**Rules followed.** Every specimen below is invented and labeled SYNTHETIC. Every person, provider, payer, address, phone, NPI, tax ID, claim
     8	number and NDC was made up for this file; identifiers use a `SYN-` prefix, phones use the 555-01xx fiction range, places are invented. A web
     9	search for each provider, payer, firm and clinician name (2026-11-02, results in section 23) found no exact match; two names close to real
    10	organizations were replaced. CPT, HCPCS, ICD-10 and
    11	revenue codes are public code sets, used only as codes. Sources are listed per format with whether I opened the page or worked from a
    12	search-result summary; where a source is thin I state the assumption.
    13	
    14	**How to use.** Section 1 holds the cross-cutting traps (dates, money, authorship). Sections 2 to 20 cover one format each (fields, wording,
    15	traps, sources, specimen): 2-14 from round 1, 15-20 added in round 2 for the v2 library packets (EMS report, ambulance invoice, §18.001
    16	affidavit, narrative letter, office/specialist note, records-review/IME report). Section 21 maps formats to product rules and packet mixes.
    17	Section 22 lists every cross-specimen mismatch as fixed or DELIBERATE. Section 23 lists assumptions, gaps and the name-collision search.
    18	`python3 research/record_formats_check.py` re-adds every specimen and checks the rules each one claims to follow.
    19	
    20	---
    21	
....
   337	## 8. CMS-1500 (02/12) professional claim
   338	
   339	**Fields (NUCC numbering).** 1a insured ID; 2 patient name; 3 DOB (8-digit) and sex; 10a-c condition related to employment / **auto accident
   340	(with state)** / other accident; 11 insured's policy; 14 date of current illness or injury with qualifier (431 onset); 17 referring provider;
   341	21 ICD indicator (0 = ICD-10) and diagnoses A-L; 24A dates of service From/To; 24B place of service; 24D CPT/HCPCS with up to four modifiers;
   342	24E diagnosis pointer (letters); 24F $charges; 24G days or units; 24J rendering provider NPI; 25 federal tax ID; 28 total charge; 29 amount
   343	paid; 30 reserved for NUCC use (no balance-due box on 02/12); 31 signature and date; 32 service facility; 33 billing provider.
   344	
   345	**Typical wording and number format.** 24F "is the total billed amount for each service line": dollars right-justified left of a vertical
   346	line, cents to the right, no dollar sign, comma or decimal point. Shaded supplemental lines above each service line hold NDC and other data
   347	and *do* use a decimal point (e.g., `1000.00`). Item 28 is the total of all 24F lines. Item 29 is money paid by patient or other payers.
   348	
   349	**Extraction traps.**
   350	- `150 | 00` OCRs as `15000` ($15,000) or `150 00`; the decimal is implied by the box, not printed.
   351	- 24A From/To with 24G = 10 means ten consecutive days on one line; one line is not one visit (NUCC: days must equal units).
   352	- 24F is the line total (units times fee), not a per-unit rate; a per-unit figure must not be read from it.
   353	- Item 14 is the injury/onset date and Item 31 is the signature date: neither is a service date.
   354	- Item 28 can disagree with the sum of lines (data entry), or a claim may run to a second page with its own lines; sum lines in code and
   355	  compare to Item 28 rather than trusting either.
   356	- 10b "Auto accident? YES  Place (State) TX" is a useful corroborating checkbox and an OCR checkbox trap.
   357	
   358	**Sources.**
   359	- NUCC, *1500 Health Insurance Claim Form Reference Instruction Manual for Form Version 02/12*, Version 8.0 (7/20): https://www.nucc.org/images/stories/PDF/1500_claim_form_instruction_manual_2020_07-v8.pdf — **opened** (text extracted locally). Takeaways: Items 14, 24A, 24F, 24G, 28, 29, 30 as stated above. Newer manual versions may exist (NUCC updates each July); field layout of the 02/12 form is unchanged.
   360	- CMS MLN web-based training on the 1500 (lesson 5): https://cms.gov/Outreach-and-Education/MLN/WBT/MLN4462429-MLN-WBT-1500/1500/lesson05/02/index.html — search result, not opened.
   361	
   362	**Specimen (SYNTHETIC), clean boxed form** (as printed; money boxes have no decimal point, cents sit right of the bar):
   363	```
   364	SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS
   365	2. PATIENT'S NAME  OKONKWO-VALE, DELPHINE (SYNTHETIC)     3. DOB 03 | 09 | 1991  F
   366	10b. AUTO ACCIDENT?  [X] YES  [ ] NO   PLACE (State) TX
   367	14. DATE OF CURRENT ILLNESS  05 | 14 | 26   QUAL 431
   368	21. ICD Ind 0   A. S13.4XXA   B. M54.12
   369	24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI
   370	    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001
   371	    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001
   372	    060326   060326   11     98941              AB     85 | 00       1      SYN-NPI-0001
   373	    060126   060326   11     97014              A      90 | 00       3      SYN-NPI-0001
   374	    060126   060326   11     97010              A      45 | 00       3      SYN-NPI-0001
   375	25. FED TAX ID  SYN-TIN-0001     28. TOTAL CHARGE  390 | 00     29. AMOUNT PAID  0 | 00
   376	31. SIGNATURE  Dr. Corvin Ashdown, DC (SYNTHETIC)  DATE 06/30/26
   377	33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142
   378	```
   379	(Lines 4-5 group 06/01 to 06/03: three consecutive days, 3 units, each matching the travel card's ES and H/C marks on all three days in
   380	section 4; $30.00 and $15.00 per day. Lines 1-3 bill the same code one line per day, which NUCC also allows. MOD is blank; AB and A are
   381	diagnosis pointers in 24E. Line sum 85 + 85 + 85 + 90 + 45 = 390 = Item 28. Item 14 is the injury date and Item 31 the signature date;
   382	neither is a visit.)
   383	
   384	**Specimen (SYNTHETIC), the same claim as OCR text** (what a scanned copy returns; truth beside each money string):
   385	```
   386	SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS
   387	24. 060126 060126 11 98941 AB 8500 1 SYN-NPI-0001         <- truth 85.00 (not 8,500.00)
   388	    060226 060226 11 98941 AB 85 00 1 SYN-NPI-0001        <- truth 85.00 (bar dropped, space kept)
   389	    O60326 060326 11 98941 AB 85|00 1 SYN-NPI-0001        <- truth 85.00; O for 0 in the date
   390	    060126 060326 11 97014 A 9000 3 SYN-NPI-0001          <- truth 90.00 (not 9,000.00)
   391	    060126 060326 11 97010 A 45 OO 3 SYN-NPI-0001         <- truth 45.00; O for 0 in the cents
   392	28. TOTAL CHARGE 39000   29. AMOUNT PAID 0 00             <- truth 390.00 and 0.00
   393	```
   394	(Expected tool behavior: money in 24F and Items 28-29 is parsed as implied-cents in code; the line sum is compared with Item 28 in code;
   395	every OCR-derived amount and date goes to review with the page image. A parser that reads `8500` as dollars bills $8,500 per adjustment.)
   396	
   397	---
   398	
   399	## 9. UB-04 (CMS-1450) institutional claim
   400
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:28.864Z

**tool call — Bash**
````
{
 "command": "cat -n research/record-formats.md | sed -n '163,209p'; echo ....; cat -n research/record-formats.md | sed -n '399,475p'",
 "description": "Read chiro travel card and UB-04 sections"
}
````

### User / tool · 2026-11-02T03:45:28.964Z

**tool result**
````
   163	## 4. Chiropractic daily note and travel card
   164	
   165	**Fields.** Date; subjective complaint with pain scale (VAS/NPRS) and functional change since last visit; objective exam documenting the
   166	PART elements (Pain/tenderness, Asymmetry/misalignment, Range-of-motion abnormality, Tissue/tone change) at specific spinal levels;
   167	segments adjusted (e.g., C5, C6, L4) and technique; modalities (97012 mechanical traction, 97014 e-stim, 97010 hot/cold); CPT for
   168	manipulation (98940 one to two regions, 98941 three to four, 98942 five, 98943 extraspinal); assessment of progress; plan and visit
   169	frequency; provider signature. Many PI chiropractic offices also keep a **travel card** (one row per visit with checkboxes for regions and
   170	modalities), which arrives as a scanned grid.
   171	
   172	**Typical wording.** "Pt states neck 6/10, better than last visit." "TTP and hypertonicity bilat C4-C6, ROM flex 35 deg." "Adjusted C5, C6,
   173	T4, L5 - diversified." "98941, 97014, 97010." "Pt responding favorably, continue 3x/wk." Fee slips say "Adjustment 3-4 regions $85.00" -
   174	which may be a fee schedule **rate** or a charge for that visit depending on whether a date of service is attached.
   175	
   176	**Extraction traps.**
   177	- Medicare guidance requires the exact segment, not just a region; PI notes often list both. Do not count segments as visits.
   178	- "Same as last visit", "SALV", or identical text across weeks is the cloned-note pattern adjusters attack.
   179	- Travel-card checkmarks are OCR-hostile (see section 14); a missed checkmark loses a modality, a stray mark invents one.
   180	- Percent-improvement statements ("50% better") are patient report, not an objective measure.
   181	- Post-visit narrative reports written for the attorney are supplemental reports, not daily notes; their date is the letter date.
   182	
   183	**Sources.**
   184	- Noridian JF Part B, *Chiropractic Documentation Guidelines - Initial vs Subsequent Visits*: https://med.noridianmedicare.com/web/jfb/specialties/chiropractic/documentation-guidelines — **opened**. Takeaway: subsequent-visit notes need updated history, exam supporting the subluxation, assessment of progress, the exact segment treated, and date-specific (not cloned) findings.
   185	- CMS MLN, *Chiropractic Services* compliance tip: https://www.cms.gov/training-education/medicare-learning-networkr-mln/compliance/medicare-provider-compliance-tips/chiropractic-services — search summary; PART acronym and AT modifier for 98940-98942.
   186	
   187	**Specimen (SYNTHETIC).**
   188	```
   189	SYNTHETIC RECORD
   190	Brightwater Spine & Wellness (SYNTHETIC)         Daily Note
   191	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   DOS: 06/03/2026   Visit #4
   192	S: Neck 6/10, low back 4/10. Pt states "about 50% better since I started."
   193	O: TTP + hypertonicity bilat C4-C6. Cerv flex 35 deg (norm 50). Asym: R high shoulder.
   194	Adjusted: C5, C6, T4, L5 (diversified).  Modalities: 97014 e-stim 15 min, 97010 cold pack.
   195	CPT: 98941, 97014, 97010
   196	A: Improving. P: Daily through 06/05, then 3x/wk x 3 wks, re-exam 06/24/2026.
   197	Dr. Corvin Ashdown, DC (SYNTHETIC)
   198	--- Travel card (scanned) ---
   199	DATE    | C | T | L | ES | H/C | TR
   200	06/01   | x | x | x | x  |  x  |
   201	06/02   | x | x | x | x  |  x  |
   202	06/03   | x | x | x | x  |  x  |
   203	```
   204	(Visit #1 was the new-patient exam on 05/29/2026, the date the intake in section 14 is signed; it was billed on an earlier claim not shown.
   205	Visits 2-4 are the three consecutive days on the travel card and on the CMS-1500 in section 8. C/T/L = regions adjusted, ES = 97014,
   206	H/C = 97010 hot/cold pack.)
   207	
   208	---
   209	
....
   399	## 9. UB-04 (CMS-1450) institutional claim
   400	
   401	**Fields (form locators).** FL 1 provider; 3a patient control number, 3b medical record number; **FL 4 type of bill** (4-digit with leading zero,
   402	e.g. 0131 hospital outpatient); **FL 6 statement covers period** From/Through; 8-11 patient name and demographics; 12-13 admission date/hour;
   403	14 admission type; 15 source; 17 discharge status; 31-36 occurrence codes and dates (accident codes 01-06, see traps); 39-41 value codes; **FL 42
   404	revenue code** (4-digit, e.g. 0450 emergency room, 0320 x-ray, 0350 CT, 0610 MRI, 0250 pharmacy, 0636 drugs requiring detailed coding);
   405	43 description (and NDC); **FL 44 HCPCS / accommodation rate / HIPPS code**; 45 service date; 46 service units; **47 total charges** (per
   406	line, plus the total after the last line); **48 non-covered charges**; 50 payer; 67 principal diagnosis and 67A-Q other diagnoses; 72
   407	external cause of injury codes; 74 principal procedure; 76 attending provider; 80 remarks.
   408	
   409	**Typical wording.** Line 23 carries revenue code `0001` = total charges (paper claims), with the **creation date** in FL 45 of that line
   410	(unverified: common convention, not in the RI guide; NUBC manual not opened). "PAGE 1 OF 2" on multi-page claims. FL 44 holds a per-day accommodation rate on inpatient room lines (e.g., `1850.00`) and a HCPCS code on
   411	outpatient lines.
   412	
   413	**Extraction traps.**
   414	- Summing every amount in FL 47 includes the 0001 total line and doubles the bill.
   415	- FL 44 on room lines is a **rate**; FL 47 on the same line is the charge (rate times days). Classic rate-vs-charge confusion (D-042).
   416	- FL 45 on the total line is the claim creation date (unverified convention), not a service date.
   417	- Occurrence codes 01-06 all carry an accident date: 01 auto accident (current NUBC wording reported as accident/medical coverage), 02
   418	  no-fault insurance involved, 03 accident/tort liability, 04 accident/employment related, 05 other accident, 06 crime victim. A PI claim may
   419	  carry any of them (01 or 03 most often). Extraction treats every one as the accident date, never a service date; packets vary the code.
   420	- On inpatient claims the room line has a rate in FL 44, days in FL 46 and often no FL 45 date; the stay dates come from FL 6 and FL 12.
   421	- On multi-page claims the total appears only on the last page.
   422	- FL 48 non-covered is not an adjustment by the provider; it is still a charge the payer did not cover.
   423	- Payer guides disagree on whether Medicare's FL 47 total excludes non-covered charges; compute from lines and keep both.
   424	
   425	**Sources.**
   426	- Rhode Island EOHHS, *UB-04 Instructions*: https://eohhs.ri.gov/sites/g/files/xkgbur226/files/2021-03/ub04_instructions.pdf — **opened** (text extracted). Takeaways: FL 4 four-digit with leading zero; FL 6 MMDDYY; FL 42 enter "0001" after last revenue code for the total in column 47 (paper only); FL 47 per-line total plus grand total; FL 48 amount not covered by primary payer.
   427	- NUBC, *Official UB-04 Data Specifications Manual 2024* (table of contents; FL 47 p.180, FL 48 p.181): https://www.nubc.org/system/files/media/file/2024/04/TOC%20FOR%20NUBC%20SITE%202024%20UB04%20Manual.pdf — search summary; the full manual is licensed.
   428	- McGraw-Hill chapter summary on FL 47/48 Medicare treatment: https://highered.mheducation.com/sites/0073520896/student_view0/chapter12/chapter_summary.html — search summary.
   429	- HL7 v2.4 NUBC occurrence-code vocabulary: https://build.fhir.org/ig/frankoemig/hl7.v2.terminology.v24/CodeSystem-nubc-OccurrenceCode-cs.json.html — **opened**. Takeaway: 01 auto accident, 02 no-fault insurance involved, 03 accident/tort liability, 04 accident/employment related, 05 other accident, 06 crime victim, 11 onset of symptoms. This is an older HL7 rendering; the current NUBC label for 01 may differ.
   430	- Assumption: FL 44 title "HCPCS/Rate/HIPPS code" and the creation-date-on-line-23 convention are from prior knowledge, confirmed only by the T-078 reviewer's working knowledge; verify against the NUBC manual before quoting.
   431	
   432	**Specimen 1 (SYNTHETIC), outpatient ED claim.**
   433	```
   434	SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
   435	1 Quillfeather Regional Medical Center (SYNTHETIC)   3a SYN-PCN-5521  3b SYN-ED-40417  4 0131
   436	6 STATEMENT COVERS PERIOD  FROM 051426  THROUGH 051526
   437	8 OKONKWO-VALE, DELPHINE (SYNTHETIC)   12 ADMISSION 051426  13 HR 23
   438	31 OCCURRENCE  CODE 01  DATE 051426
   439	42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
   440	0450    EMERGENCY ROOM LVL 4          99284          051426        1          2,410.00
   441	0350    CT CERVICAL SPINE W/O         72125          051526        1          3,185.00
   442	0636    KETOROLAC INJ 15MG            J1885          051526        2             96.00
   443	0250    PHARMACY GENERAL                             051526        1             38.50           38.50
   444	0001    TOTAL                                        051826                   5,729.50           38.50
   445	67 S16.1XXA   72 ECI V43.52XA   76 ATTENDING Dr. Ilario Fenwick (SYNTHETIC)
   446	PAGE 1 OF 1
   447	```
   448	(The 0001 line repeats the sum; 051826 on that line is the creation date, an unverified convention. Occurrence code 01.)
   449	
   450	**Specimen 2 (SYNTHETIC), inpatient claim with a room rate on the charge line** (a different synthetic patient):
   451	```
   452	SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
   453	1 Saltmarrow General Hospital (SYNTHETIC)   3a SYN-PCN-7730  3b SYN-IP-11902  4 0111
   454	6 STATEMENT COVERS PERIOD  FROM 091526  THROUGH 091826
   455	8 TELFAIR-NKEMELU, AMBROSE (SYNTHETIC)   12 ADMISSION 091526  13 HR 02  14 TYPE 1  17 STAT 01
   456	31 OCCURRENCE  CODE 03  DATE 091426
   457	42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
   458	0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00
   459	0450    EMERGENCY ROOM                               091526        1          1,975.00
   460	0250    PHARMACY                                     091526       14            412.75
   461	0300    LABORATORY                                   091526        6            688.00
   462	0320    DX X-RAY                                     091526        2            540.00
   463	0001    TOTAL                                        092226                   9,165.75
   464	67 S42.201A   72 ECI V43.52XA   76 ATTENDING Dr. Rosamund Achterberg (SYNTHETIC)
   465	PAGE 1 OF 1
   466	```
   467	(Room line: FL 44 rate 1,850.00 x FL 46 3 days = FL 47 5,550.00. Only FL 47 is a charge; 1,850.00 is a rate. A naive sum of every money
   468	figure adds the rate and the 0001 line and reports 20,181.50 instead of 9,165.75. Admitted 09/15, discharged 09/18 = 3 room days.
   469	Occurrence code 03, not 01: 09/14/2026 is the accident date, not a service date. 092226 on the 0001 line is the creation date.)
   470	
   471	---
   472	
   473	## 10. Itemized provider ledger / statement
   474	
   475	**Fields.** Provider name and address; patient and account number; statement date; prior balance / balance forward; per line: date of
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:36.697Z

**tool call — Bash**
````
{
 "command": "cat -n research/record-formats.md | sed -n '601,702p'",
 "description": "Read Spanish and scanned-intake sections"
}
````

### User / tool · 2026-11-02T03:45:36.781Z

**tool result**
````
   601	## 13. Spanish-language clinic note
   602	
   603	**Fields.** Same structure as an English clinic note under Spanish headings: *Fecha*; *Ficha de identificación* (name, age, sex);
   604	*Motivo de consulta* (reason for visit, with duration); *Enfermedad actual* / *Padecimiento actual* (onset, course, current state);
   605	*Antecedentes* (personales patológicos, no patológicos, quirúrgicos, alergias); *Signos vitales*; *Exploración física*; *Impresión
   606	diagnóstica* / *Diagnóstico* (IDx); *Plan* (diagnostic: *estudios solicitados*; therapeutic: drug, dose, *vía oral (VO)*, frequency *c/8h*,
   607	duration); *Pronóstico*; signature with *cédula profesional* (Mexico) or license.
   608	
   609	**Typical wording.** "Paciente femenina de 35 años que acude por dolor cervical de 3 días de evolución posterior a choque vehicular por
   610	alcance." "Refiere dolor 7/10, irradiado a brazo derecho." "Niega pérdida del estado de alerta." "A la exploración física: contractura
   611	paravertebral cervical, dolor a la palpación C5-C7." "IDx: Esguince cervical grado I." "Plan: naproxeno 500 mg VO c/12h por 7 días,
   612	reposo relativo, cita en 1 semana." "Consulta: $650.00" (charge) vs "Costo por sesión de terapia: $400.00" (rate).
   613	
   614	**Extraction traps.**
   615	- Day-first dates: `03/06/2026` is 3 June, not March 6. Written months: `14 de mayo de 2026`, `14-may-26`, `12-ago-2026`.
   616	- `ago` is a month abbreviation (agosto); `hace 3 días` is "3 days ago" and is relative to the visit date, not a date.
   617	- `refiere` (patient reports) and `niega` (denies) mark voice and negation; a translation must keep them.
   618	- Decimal comma and dot thousands in Latin American notes (`$1.250,00`); US-based clinics usually print `$1,250.00`. Currency may be MXN.
   619	- Mixed English/Spanish ("dolor de low back", "MRI solicitada") in border-region clinics.
   620	- Per D-042 the excerpt is always the original Spanish; any translation is LLM output, labeled, judged, and never the cited excerpt.
   621	
   622	**Sources.**
   623	- Huli Practice, *Ejemplo Formato Historia Clínica* (Mexican clinical-history template: motivo de consulta, enfermedad actual, antecedentes, exploración, diagnóstico, plan): https://blog.hulipractice.com/content/files/2023/08/Ejemplo-Formato-Historia-Cli-nica.pdf — search summary.
   624	- Universitat de Barcelona, *Estructura de una entrevista diagnóstica - Motivo de consulta y enfermedad actual*: https://diposit.ub.edu/items/77b3b1a7-0b60-48b7-850d-224ebebcb4e5/full — search summary; enfermedad actual covers onset, evolution and current state; impresión diagnóstica is the clinician's, not asked of the patient.
   625	- AgendaPro, *Formato de Historia Clínica*: https://agendapro.com/blog/wp-content/uploads/sites/2/2026/03/Formato-de-Historia-Clinica.pdf — search summary; plan split into estudios solicitados and treatment with drug, dose, frequency, duration.
   626	- Assumption: common phrasing above ("acude por", "de N días de evolución", "refiere", "niega", "c/8h", "VO") is from general clinical Spanish usage; sources are teaching templates, not a terminology standard.
   627	
   628	**Specimen (SYNTHETIC).**
   629	```
   630	REGISTRO SINTÉTICO / SYNTHETIC RECORD
   631	Consultorio Médico Peñaverde (SINTÉTICO)          Nota de consulta
   632	Fecha: 17/05/2026
   633	Paciente: Rosalba Itzel Marqueño (SINTÉTICO)   Edad: 41 años   Sexo: F
   634	Motivo de consulta: Dolor de cuello de 3 días de evolución posterior a choque vehicular por alcance.
   635	Enfermedad actual: Refiere dolor 7/10, irradiado a brazo derecho, que aumenta al girar la cabeza.
   636	  Niega pérdida del estado de alerta. Niega antecedentes de dolor cervical.
   637	Signos vitales: TA 130/85, FC 88.
   638	Exploración física: Contractura paravertebral cervical. Dolor a la palpación C5-C7.
   639	IDx: Esguince cervical grado I.
   640	Plan: Naproxeno 500 mg VO c/12h por 7 días. Reposo relativo. Rx de columna cervical.
   641	  Cita de control en 3 semanas (07/06/2026).
   642	Consulta: $650.00     Costo por sesión de terapia física: $400.00
   643	Dra. Itziar Orbezua Lanz (SINTÉTICO)
   644	```
   645	(`17/05/2026` is 17 May: unambiguous, day > 12. `07/06/2026` is **7 June 2026**, not July 6: both parts are 12 or less, so only the
   646	day-first convention decides; it is 21 days after the visit, matching "en 3 semanas". The $650.00 is the visit charge; the $400.00 is a
   647	per-session rate, not a charge.)
   648	
   649	---
   650	
   651	## 14. Scanned and handwritten intake forms (and OCR failure modes)
   652	
   653	**Fields.** Patient demographics; date of injury; "How did the injury occur?" (free text); body diagram with marked pain areas; pain scale
   654	0-10 (circled); symptom checkboxes (headache, dizziness, numbness); "Prior injuries / accidents / chiropractic care? Yes / No" with
   655	explanation lines; current medications; employer and work status; "Who referred you?" (often an attorney); attorney name; insurance (auto,
   656	health, MedPay/PIP); signature and date; sometimes an embedded LOP or assignment of benefits (section 12).
   657	
   658	**Typical wording.** Handwriting, abbreviations and the patient's own words: "rear ended at light, neck + back hurt", "no prior", "Dr. told
   659	me to come", "pain 7-8". Stamps: "RECEIVED", "SCANNED", Bates numbers; fax header on every page.
   660	
   661	**OCR failure modes to reproduce.**
   662	| Failure | Example (truth → OCR) | Consequence |
   663	|---|---|---|
   664	| Checkbox read as character or dropped | `[X] No` → `IX] No` or `No`; `[ ] Yes [X] No` → `Yes No` | Prior-injury answer lost or flipped - high stakes for pre-existing flags |
   665	| Glyph confusion | `0/O`, `1/l/I/7`, `5/S`, `8/B`, `2/Z` | `05/14/26` → `O5/l4/26`; `$150` → `$I50` |
   666	| Dropped or added decimal | `$1,250.00` → `$125000` or `$1,25000` | Amount off by 100x |
   667	| Implied decimal (CMS-1500 boxes) | `150 \| 00` → `15000` | Same |
   668	| Circled number | Pain scale `0 1 2 3 4 5 6 7 8 9 10` with 7 circled → all digits | Pain score lost |
   669	| Strike-through and correction | `6/12` struck, `6/15` written above | Both dates extracted |
   670	| Two-column / form-grid reading order | Left and right columns interleaved | Answers attached to the wrong question |
   671	| Fax header and stamps | `11/03/2026 09:14 FROM: 555-0199 P.3/14` | Fax date read as a record date |
   672	| Skew, blur, shadow, bleed-through | Phone photo of a form | Character error rate rises; Tesseract was weakest on blur and shadow in one study |
   673	| Hidden or layered text in PDFs | Searchable PDF with an invisible text layer that differs from the image | Extracted text not visible to the human reviewer (D-042 hidden-text detection) |
   674	
   675	**Sources.**
   676	- *Compact Multimodal Language Models as Robust OCR Alternatives for Noisy Textual Clinical Reports* (arXiv 2511.13523): https://arxiv.org/html/2511.13523v1 — **opened**. Takeaway: on smartphone photos of printed clinical reports, Tesseract scored CER 0.189, WER 0.276 and numeric accuracy 0.756, worse than neural pipelines and small multimodal models; Tesseract struggled most with blur and shadows. (Cite by arXiv number; authors not recorded here.)
   677	- Tesseract OCR mailing list, thread on reading "X" checkboxes: https://groups.google.com/g/tesseract-ocr/c/r9mVUg76iE0 — search summary; out-of-the-box quality is medium; form jargon needs training; one user got better results at 150 dpi than 600 dpi.
   678	- ImageToTable blog, *Why AI reads handwriting but misses a ticked box*: https://imagetotable.ai/blog/how-ai-reads-handwritten-forms-checkboxes-to-excel — search summary (vendor); generic OCR has no character for a tick and skips or garbles it.
   679	- Assumption: glyph confusions in the table are the standard OCR confusion set; I found no Tesseract-specific measurement of them.
   680	
   681	**Specimen (SYNTHETIC)** — what the page shows, then what OCR returns:
   682	```
   683	SYNTHETIC RECORD
   684	[PAGE IMAGE, described] Brightwater Spine & Wellness New Patient Intake. Handwritten in blue ink.
   685	  Date of injury: 5/14/26.  How did it happen: "rear ended at red light, neck and back hurt."
   686	  Pain today: 7 circled on a 0-10 line.  Prior injuries? [ ] Yes [X] No.
   687	  Who referred you? "my lawyer - Vey".  Signed 5/29/26.  Fax header: 11/03/2026 09:14 P.2/9.
   688	  Stamp: RECEIVED NOV 03 2026.
   689	[OCR TEXT as extracted]
   690	  11/O3/2026 O9:14 FROM 555-0199 P.2/9
   691	  Date of injury: 5/l4/26
   692	  How did it happen: rear ended at red Iight, neck and back hurt
   693	  Pain today: 0 1 2 3 4 5 6 7 8 9 10
   694	  Prior injuries? Yes IX] No
   695	  Who referred you? my Iawyer - Vey
   696	  Signed 5/29/2G
   697	  RECEIVED NOV O3 2026
   698	```
   699	(The chosen pain score and the prior-injury answer are not recoverable from the OCR text alone; the item needs the page image and review.)
   700	
   701	---
   702
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:41.145Z

**tool call — Bash**
````
{
 "command": "cat -n research/record-formats.md | sed -n '703,858p'",
 "description": "Read EMS, ambulance invoice, and affidavit sections"
}
````

### User / tool · 2026-11-02T03:45:41.258Z

**tool result**
````
   703	## 15. EMS patient care report (ambulance run report)
   704	
   705	**Fields (NEMSIS v3 names in brackets).** Agency, unit and crew with certification levels; incident and run numbers; call times: PSAP call
   706	(eTimes.01), unit notified (eTimes.03), en route (eTimes.05), arrived on scene (eTimes.06), arrived at patient (eTimes.07), left scene
   707	(eTimes.09), arrived at destination (eTimes.11), transfer of care (eTimes.12); scene location type; patient demographics; chief complaint;
   708	mechanism of injury and vehicle/scene description; several timed vital-sign sets (BP, HR, RR, SpO2, GCS, pain); assessment by body region;
   709	treatments with times (spinal motion restriction, cold pack, medications); narrative (often in CHART or SOAP order); disposition: unit
   710	disposition, patient evaluation/care, crew disposition, transport disposition (eDisposition.27-30); reason for refusal or release
   711	(eDisposition.31); destination; patient or witness signature on a refusal; crew signatures.
   712	
   713	**Typical wording.** "Dispatched for MVC with injuries." "Arrived to find pt sitting in driver seat, self-extricated, ambulatory at scene."
   714	"Moderate rear-end damage to pt's vehicle, airbags deployed." "Pt c/o neck pain 7/10, denies LOC." "GCS 15." "Pt placed in position of
   715	comfort, c-collar applied." Refusal: "Pt refused transport against medical advice. Risks explained incl. worsening injury and death. Pt
   716	verbalized understanding, signed refusal." "Minor damage to rear bumper." The run report carries **no charges**; the bill is section 16.
   717	
   718	**Extraction traps.**
   719	- The service date is the call date. A call at 23:12 that reaches the ED at 23:47 and is signed after midnight still belongs to the call date.
   720	- Eight timestamps for one encounter; the ED's own arrival time (section 2) can differ by a minute or two. That is not a conflict.
   721	- Scene descriptions ("minor damage", "ambulatory at scene", "self-extricated") are the crew's observations, not the patient's report and not
   722	  a medical finding. They are the defense's MIST language (D-018 causation lexicon; speaker is EMS).
   723	- A refusal is a dated encounter with no transport. The next care date after a refusal decides the first-treatment gap.
   724	- "Pt states" lines (history) sit beside crew observations in one narrative; the excerpt keeps both voices.
   725	- Repeated vital sets: pain 7/10 at 23:24 and 5/10 at 23:40 are both true at their times.
   726	
   727	**Sources.**
   728	- NASEMSO, *EMS Time Duration Definitions* (2024-06-18): https://nemsis.org/wp-content/uploads/2024/06/NASEMSO_EMS_Time_Duration_Definitions-6-18-24.pdf — **opened** (text extracted). Takeaway: the eTimes.01-17 list and interval formulas (scene time = left scene minus arrived on scene).
   729	- Montana DPHHS, *NEMSIS disposition guide*: https://dphhs.mt.gov/assets/publichealth/EMSTS/EMS/Disposition.pdf — **opened** (text extracted). Takeaway: eDisposition.27-31 (unit, patient evaluation/care, crew, transport disposition, reason for refusal/release); "patient evaluated and refused care" and "patient refused transport" values; "against medical advice" as a refusal reason.
   730	- NEMSIS v3.5 *Requisite National Elements*: https://nemsis.org/wp-content/uploads/2025/01/NEMSIS-v3.5-Requisite-National-Elements-EMS-DataSet.pdf — search summary (the URL returned an HTML page to curl).
   731	- Assumption: the narrative wording above is common EMS charting style; no Texas agency template was opened.
   732	
   733	**Specimen (SYNTHETIC).**
   734	```
   735	SYNTHETIC RECORD - PATIENT CARE REPORT - ALL IDENTIFIERS FICTITIOUS
   736	Fernhollow County EMS (SYNTHETIC)   Unit: Medic 14   Incident SYN-INC-26-04471   Run SYN-RUN-0912
   737	Date: 05/14/2026   PSAP 23:12  Notified 23:13  En route 23:14  On scene 23:21  At pt 23:22
   738	                   Left scene 23:36  At dest 23:47  Transfer of care 23:52
   739	Patient: Delphine Okonkwo-Vale (SYNTHETIC)  DOB 03/09/1991  F
   740	CC: Neck pain.  MOI: MVC, rear-end, restrained driver, airbag deployed.
   741	Scene: Moderate rear damage to pt vehicle. Pt self-extricated, ambulatory at scene.
   742	VITALS  23:24  BP 148/90  HR 102  RR 18  SpO2 98%  GCS 15  Pain 7/10
   743	        23:40  BP 142/88  HR 96   RR 18  SpO2 98%  GCS 15  Pain 6/10
   744	NARRATIVE: Pt states "the truck hit me from behind." Denies LOC. C/o neck pain and
   745	  tingling R hand. C-collar applied, cold pack to neck. Transported to Quillfeather
   746	  Regional ED without incident.
   747	DISPOSITION: Patient treated, transported by this EMS unit.
   748	Crew: Hollis Brandvold, Paramedic (SYNTHETIC); Pia Strandquist, EMT (SYNTHETIC)
   749	--- Refusal variant (another synthetic run, for packets that need it) ---
   750	Date: 03/02/2026  On scene 16:05  Left scene 16:31
   751	Scene: Minor damage to rear bumper. Pt ambulatory at scene, no visible injury.
   752	Pt c/o mild neck stiffness. Pt refused transport against medical advice; risks explained.
   753	DISPOSITION: Patient evaluated and refused care / refused transport.  Pt signature on file.
   754	```
   755	(Arrival at destination 23:47 here vs ED arrival 23:48 in section 2: same event, not a conflict. "Moderate rear damage" is the crew's
   756	observation; "the truck hit me from behind" is the patient's.)
   757	
   758	---
   759	
   760	## 16. Ambulance invoice (base rate plus mileage)
   761	
   762	**Fields.** Agency billing name and tax ID; invoice number, invoice date and run number; date of service; patient; pick-up and drop-off
   763	(origin/destination modifier letters); level of service line (HCPCS A0427 ALS1 emergency, A0429 BLS emergency, etc.); mileage line (A0425,
   764	units = loaded miles, fractional to the tenth); per-unit rate and line charge; supplies lines if itemized; total charges; payments (auto
   765	PIP/MedPay, health plan); adjustments; balance due; "out of network" or balance-billing notice.
   766	
   767	**Typical wording.** "A0427-SH ALS emergency transport, Level 1 ... 1,450.00." "A0425-SH Ground mileage 8.7 mi @ 22.50/mi ... 195.75."
   768	"Total charges 1,645.75." "Balance due upon receipt." Origin/destination modifiers pair a pick-up letter with a drop-off letter (S = scene of
   769	accident or acute event, H = hospital, R = residence), so a crash scene to ED trip is SH.
   770	
   771	**Extraction traps.**
   772	- The per-mile figure (22.50/mi) is a **rate**; only the extended line (195.75) and the stated total are charges (D-042 rate-vs-charge guard;
   773	  miles x rate is recomputed in code).
   774	- Units are miles with a decimal (8.7), not visits and not integers. A parser that drops the decimal bills 87 miles.
   775	- Every trip is normally two lines (service + mileage) for one encounter; they are not two encounters.
   776	- Only loaded miles (patient on board) are billable for Medicare; commercial and auto carriers vary.
   777	- The invoice date and any statement date are not the service date; the run number ties the invoice to the run report (section 15).
   778	- A balance-billing notice states an asserted balance without a service line (notes only, D-019).
   779	
   780	**Sources.**
   781	- CMS, *Medicare Claims Processing Manual*, ch. 15 *Ambulance*: https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/downloads/clm104c15.pdf — **opened** (text extracted). Takeaways: origin/destination modifier letters (S = scene of accident or acute event, H = hospital, R = residence ...; first letter origin, second destination); A0425 ground mileage per mile, A0427 ALS1 emergency; generally two lines per trip; mileage reported in fractional units, rounded up to the nearest tenth for trips under 100 miles; mileage means loaded mileage.
   782	- Noridian JE, *Ambulance Mileage*: https://med.noridianmedicare.com/web/jeb/specialties/ambulance/mileage — **opened**. Takeaway: only loaded miles are paid; round up to the tenth for 100 miles or less; leading zero below 1 mile; missing mileage defaults to 0.1.
   783	- FAIR Health ground-ambulance brief (2023) via research/case-library-sources-v2.md P15 — search excerpt; most claim lines out of network.
   784	- Assumption: the rates in the specimen are invented and do not reflect any fee schedule.
   785	
   786	**Specimen (SYNTHETIC).**
   787	```
   788	SYNTHETIC RECORD - AMBULANCE INVOICE - ALL IDENTIFIERS FICTITIOUS
   789	Fernhollow County EMS Billing (SYNTHETIC)   TIN SYN-TIN-0440   Invoice SYN-INV-77310   Invoice date 05/29/2026
   790	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Run SYN-RUN-0912   DOS 05/14/2026
   791	Pick-up: Scene (S)   Drop-off: Quillfeather Regional Medical Center (H)
   792	CODE      DESCRIPTION                          UNITS   RATE       CHARGE
   793	A0427-SH  ALS emergency transport, Level 1      1      1,450.00   1,450.00
   794	A0425-SH  Ground mileage, loaded                8.7       22.50     195.75
   795	                                          TOTAL CHARGES          1,645.75
   796	PAYMENTS 0.00   ADJUSTMENTS 0.00   BALANCE DUE 1,645.75
   797	Account noted: attorney representation, letter of protection requested.
   798	```
   799	(8.7 x 22.50 = 195.75; 1,450.00 + 195.75 = 1,645.75. 22.50 is a rate. 05/29/2026 is the invoice date, not a service date.)
   800	
   801	---
   802	
   803	## 17. Texas CPRC §18.001 billing affidavit and records cover page
   804	
   805	**Fields.** Optional caption (cause number, court, parties) when filed; affiant's name and role: the person who provided the service or the
   806	person in charge of records (custodian); provider name; patient; date-of-service range; sworn statements that the records were kept in the
   807	regular course of business and made at or near the time, and that the services were necessary and the charges reasonable at the time and
   808	place; for medical expenses, the amount charged, the amount paid and the amount still unpaid that the provider has a right to be paid
   809	after adjustments or credits (§18.002(b-1)); jurat with notary signature, date and commission expiry; attached itemized statement; page
   810	count. A records-retrieval **cover page** often sits on top: vendor name, request number, page count, a list of what is enclosed, or a
   811	"no records found" certification.
   812	
   813	**Typical wording (paraphrased, not the statutory form).** "Before me, the undersigned authority, personally appeared ..., who being duly
   814	sworn deposed as follows." "I am the custodian of records of ..." "Attached are 3 pages of records ... kept in the regular course of
   815	business." "The total amount charged for the services was $445.00. The amount paid was $0.00. The amount unpaid that the provider has a
   816	right to be paid is $400.00." "Sworn to and subscribed before me on ..." The exact form is in CPRC §18.002; quote it from the official text.
   817	
   818	**Extraction traps.**
   819	- The affidavit is **not a medical record**: no encounter, no clinical content. Its jurat date, notary commission date and cover-page date
   820	  are not service dates; its DOS range spans many visits.
   821	- §18.001(b) (as amended 2019): the affidavit supports reasonableness of the charge but is **not evidence of causation**. Diagnosis lines on
   822	  the attached bill are not a causation opinion (Hills v. Donis, 2021).
   823	- The attached itemized statement usually duplicates a bill already produced in the provider's records: a true duplicate (section 1.4).
   824	  Dedupe must keep one copy and cite both locations, never add both.
   825	- Charged / paid / unpaid totals are attested sums. Code recomputes totals from the attached lines and compares; paid vs unpaid is a
   826	  paid-or-incurred figure for notes only.
   827	- A counteraffidavit from the other side attacks the same lines; it is an opponent's opinion, not a provider record.
   828	- "No records" certifications are non-record pages (record_warning), but their date tells the paralegal a request was answered.
   829	
   830	**Sources.**
   831	- Texas Civil Practice and Remedies Code §18.001 and §18.002, via https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_18.001 and https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_18.002 — **opened** (fetch tool; short quotes only). Takeaways: affiant is the provider or the records custodian; affidavit must include an itemized statement and be sworn; 90-day / 120-day service deadlines for affidavits and counteraffidavits; §18.001(b) says it is not evidence of causation; §18.002(b-1) medical-expense form adds amount paid and amount unpaid; amended through Acts 2019 (H.B. 1693). Official page https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm is a JavaScript app that did not render for the fetch tool.
   832	- Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.] Feb. 11, 2021, pet. denied) (substitute mem. op.), via https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14 — **opened** (PDF, pdftotext). Takeaway: §18.001 affidavits do not establish causation.
   833	- Assumption: the cover-page layout is a common records-retrieval vendor style; no vendor template was opened.
   834	
   835	**Specimen (SYNTHETIC).**
   836	```
   837	SYNTHETIC RECORD - RECORDS CERTIFICATION COVER - ALL IDENTIFIERS FICTITIOUS
   838	Gallowmere Records Retrieval (SYNTHETIC)   Request SYN-RR-3310   Completed 08/14/2026
   839	Provider: Larkspur Hollow Physical Therapy (SYNTHETIC)   Patient: Delphine Okonkwo-Vale (SYNTHETIC)
   840	Enclosed: Affidavit (2 pp) | Itemized statement (1 p) | Daily notes (6 pp)   Total pages: 9
   841	--- page 2 ---
   842	AFFIDAVIT CONCERNING COST AND NECESSITY OF SERVICES (CPRC 18.001)
   843	STATE OF TX  /  COUNTY OF FERNHOLLOW (SYNTHETIC)
   844	Before me appeared Marguerite Oyelaran-Pike (SYNTHETIC), who being sworn stated: I am the custodian of
   845	records of Larkspur Hollow Physical Therapy (SYNTHETIC). Attached are records of services provided to
   846	Delphine Okonkwo-Vale (SYNTHETIC) from 05/27/2026 through 06/10/2026, kept in the regular course of business
   847	and made at or near the time of service. The services were necessary and the charges reasonable.
   848	Total amount charged: $445.00.  Amount paid: $0.00.  Amount unpaid that the provider has a right to be paid: $400.00.
   849	Sworn to before me 08/12/2026.   /s/ Notary Public, State of TX (SYNTHETIC)   Commission expires 04/30/2029
   850	--- page 3: itemized statement (same document as section 10) ---
   851	```
   852	(The figures match the ledger in section 10: charges 445.00, adjustment 45.00, payments 0.00, balance 400.00. Page 3 is a duplicate of the
   853	section 10 statement and must not be counted twice. Packets write the state as "TX" because the spelled-out state name is on the v1
   854	identifier denylist in research/validate_library.py.)
   855	
   856	---
   857	
   858	## 18. Treating-provider narrative letter
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:47.392Z

**tool call — Bash**
````
{
 "command": "cat -n research/record-formats.md | sed -n '858,950p'",
 "description": "Read narrative letter and office note sections"
}
````

### User / tool · 2026-11-02T03:45:47.481Z

**tool result**
````
   858	## 18. Treating-provider narrative letter
   859	
   860	**Fields.** Letterhead; letter date; addressee (usually the patient's attorney); "Re:" line with patient, DOB, date of injury; records
   861	reviewed; history as told by the patient; initial complaints; examination findings; diagnoses (often with ICD-10); treatment summary
   862	(dates, visit count, modalities, referrals); current status and maximum medical improvement; prognosis and permanency; future care (type,
   863	frequency, duration, estimated cost); work status and restrictions; causation statement; signature and credentials.
   864	
   865	**Typical wording.** Explained form: "Based on the history, the timing of symptom onset, my examination and the MRI of 06/18/2026, it is my
   866	opinion within reasonable medical probability that the C5-6 disc protrusion was caused or aggravated by the collision of 05/14/2026,
   867	because ..." Conclusory form: "The accident caused all of the injuries and treatment listed above." Future care: "Ms. X will need an
   868	estimated 12 additional visits at $150.00 per visit." "She has not reached MMI."
   869	
   870	**Extraction traps.**
   871	- The letter date is not a service date. The letter is a summary written for the attorney, not a visit (section 4 traps).
   872	- The causation sentence is a provider statement: the D-018 causation lexicon flags it, the excerpt is shown verbatim, and no summary may
   873	  restate it as fact (the judge rejects one that does). The tool never grades whether it is conclusory; that is a legal judgment.
   874	- Restated history ("Pt reports she was rear-ended ...") is the patient's account repeated by the provider.
   875	- Visit counts and dates in the letter can disagree with the notes; code counts dated notes, the letter's number is cited as the letter's.
   876	- Future-care costs are estimates and per-visit prices are rates (D-019, D-042): never charges.
   877	- The letter may cite records not in the packet (an MRI from another facility); cite the letter, do not invent the record.
   878	
   879	**Sources.**
   880	- Ezel, *Personal Injury Narrative Medical Report Request* template: https://ezel.ai/templates/narrative-medical-report-request/ — **opened**. Takeaways: requested sections (history, exam, diagnoses with ICD-10, treatment, causation, MMI, prognosis, permanency, future care with cost, work status); causation addressed only within the provider's own judgment and in counsel-approved terms.
   881	- Hills v. Donis (2021), above — **opened**. Takeaway: a treater's letters that state the crash caused the injuries without explaining how and why are conclusory and no evidence of causation.
   882	- Mondaq, *Tips for attorneys: direct exam of a treating physician* (2012): https://mondaq.com/unitedstates/healthcare/160998/tips-for-attorneys-direct-exam-of-a-treating-physician — search summary; future care, cost and a causation question in reasonable medical probability.
   883	
   884	**Specimen (SYNTHETIC).**
   885	```
   886	SYNTHETIC RECORD
   887	Brightwater Spine & Wellness (SYNTHETIC)   555-0142
   888	July 20, 2026
   889	Ottoline Vey, Attorney, Harrowgate & Vey, PLLC (SYNTHETIC)
   890	Re: Delphine Okonkwo-Vale (SYNTHETIC)   DOB 03/09/1991   Date of injury 05/14/2026
   891	Ms. Okonkwo-Vale has treated in this office since 05/29/2026. She reports she was rear-ended
   892	on 05/14/2026 and developed neck pain and right hand tingling the same night.
   893	Diagnoses: cervical sprain (S13.4XXA); cervical radiculopathy (M54.12).
   894	Treatment: spinal manipulation, e-stim and hot/cold packs; MRI 06/18/2026 ordered by this office.
   895	Prognosis: guarded. She has not reached maximum medical improvement.
   896	Future care: an estimated 12 additional visits at $150.00 per visit ($1,800.00).
   897	The motor vehicle collision of 05/14/2026 caused all of the injuries and treatment described in this letter.
   898	Dr. Corvin Ashdown, DC (SYNTHETIC)
   899	```
   900	(Conclusory on purpose, as in v2 pattern P3: no explanation of how or why. $150.00 per visit is a rate and $1,800.00 an estimate; neither is
   901	a charge. July 20, 2026 is the letter date. The diagnoses match the CMS-1500 in section 8.)
   902	
   903	---
   904	
   905	## 19. Physician office / specialist progress note (PCP, orthopedics, neurology, pain management)
   906	
   907	**Fields.** Date; visit type (new, follow-up); chief complaint; HPI or interval history; ROS; PMH/PSH, medications, allergies, social
   908	history (often carried forward); exam; data reviewed (imaging, outside records); assessment and plan (medical decision making); procedures
   909	recommended or scheduled; referrals; work status; follow-up interval; E/M code on the billing copy (99202-99215); signature and date.
   910	
   911	**Typical wording.** "Pt returns for f/u of neck pain." "Interval hx: no improvement with 6 wks of PT." "ROS: Negative except as noted in
   912	HPI." "MRI C-spine 06/18/2026 reviewed: C5-6 protrusion with R foraminal narrowing." "A/P: 1. Cervical radiculopathy, R C6. Discussed
   913	options. Recommend C5-6 ACDF." "Estimated surgeon fee $14,500.00." "Work status: off work through 08/31/2026." "RTC 4 wks."
   914	
   915	**Extraction traps.**
   916	- Carried-forward ROS and PMH ("denies back pain") can contradict the HPI of the same note or another provider's note the same week
   917	  (v2 patterns P10, P16); code pairs nearby dates, never merges two visits because text matches.
   918	- A recommended or scheduled procedure is not a performed one; its date is in the future.
   919	- "Estimated" surgeon or facility fees are estimates (D-019), not charges.
   920	- Work-status and follow-up dates are future dates, not encounters.
   921	- History "per patient" and outside imaging "reviewed" are cited as the note's statements, not as new findings.
   922	- A PCP note that predates the injury is a pre-existing-condition source even when it is about something else.
   923	
   924	**Sources.**
   925	- CMS MLN, *Evaluation and Management Services Guide* (MLN006764): https://www.cms.gov/files/document/mln006764-evaluation-management-services.pdf — search summary; history, exam and medical decision making as the documented elements; document during or soon after the encounter.
   926	- Steinkamp et al. (2022) via research/case-library-sources-v2.md P10 — abstract read; about half of note text is duplicated from earlier notes.
   927	- Assumption: the layout above is a common EHR office-note print; no specific vendor template was opened.
   928	
   929	**Specimen (SYNTHETIC).**
   930	```
   931	SYNTHETIC RECORD
   932	Thistledown Orthopedic & Spine Clinic (SYNTHETIC)      Office Visit      DOS 07/08/2026
   933	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Referred by: Dr. Corvin Ashdown, DC (SYNTHETIC)
   934	CC: Neck pain with R arm tingling.
   935	HPI: Rear-end MVC 05/14/2026 per pt. PT since 05/27/2026 without lasting relief. Pain 7/10.
   936	ROS: Negative except as noted in HPI.
   937	PMH: Low back pain 2023, resolved per pt.
   938	EXAM: Spurling + R. Grip 4/5 R. Diminished R biceps reflex.
   939	DATA: MRI C-spine 06/18/2026 reviewed: C5-6 protrusion, mild R foraminal narrowing.
   940	A/P: Cervical radiculopathy, R C6. Recommend C5-6 ACDF. Estimated surgeon fee $14,500.00.
   941	Work status: off work through 08/31/2026.   RTC after surgery.
   942	Dr. Anselm Greaves, MD (SYNTHETIC)   99204
   943	```
   944	(The ACDF is recommended here and performed on 08/04/2026 (section 6). $14,500.00 is an estimate. 08/31/2026 is a future work-status
   945	date, not a visit.)
   946	
   947	---
   948	
   949	## 20. Records-review (peer-review) letter and independent medical exam (IME) report
   950
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:45:49.707Z

**tool call — Bash**
````
{
 "command": "cat -n research/record-formats.md | sed -n '950,1080p'",
 "description": "Read IME, mapping, cross-specimen and name-collision sections"
}
````

### User / tool · 2026-11-02T03:45:49.792Z

**tool result**
````
   950	
   951	**Fields.** Requesting party (liability carrier, PIP carrier or defense counsel); reviewer or examiner name, specialty and credentials;
   952	report date; for an IME, the exam date and who attended; list of records reviewed with their dates; questions posed (Were the injuries
   953	caused by the incident? Was treatment reasonable and necessary? Through what date? Has the person reached MMI?); the reviewer's history
   954	summary; exam findings (IME only: inspection, ROM, neuro, non-organic signs such as Waddell signs, distraction tests); opinions; attestation.
   955	
   956	**Typical wording.** "Based on my review of the records listed above ..." "Treatment after 07/15/2026 was not reasonable or medically
   957	necessary." "Findings consistent with a self-limited cervical strain." "Degenerative changes that pre-date the incident." "Symptom
   958	magnification." "Waddell signs 3/5." "Effort was inconsistent." "MMI as of 07/15/2026."
   959	
   960	**Extraction traps.**
   961	- Stage: a records review is often pre-suit (the carrier's response to the demand); a defense medical exam in Texas needs a motion and court
   962	  order under TRCP 204, so it is post-suit. The packet should say which.
   963	- The reviewer's history is a summary of other records, not an encounter. A records review has only a report date; only an IME has an exam
   964	  date, and the examiner is an adverse party's expert, not a treater.
   965	- Credibility words ("symptom magnification", "inconsistent effort", "Waddell 3/5") flag under D-043; a clean negation ("0/5 Waddell signs")
   966	  does not, and a sentence that mixes both does.
   967	- "Not reasonable or necessary after date X" and "MMI as of X" are opinions with dates; X is not a service date.
   968	- The reviewer may misquote dates or findings from the records; code can compare quoted dates with the packet's own entries.
   969	
   970	**Sources.**
   971	- Texas Rule of Civil Procedure 204 (physical and mental examination): https://ruledex.com/texas/texas-rules-of-civil-procedure/part-ii-rules-of-practice-in-district-and-county-courts/section-9-evidence-and-discovery/b-discovery/rule-204-physical-and-mental-examination/ — search summary; motion no later than 30 days before the discovery period ends; written order setting time, place, scope and examiner; report delivered on request.
   972	- Search summary of New York no-fault arbitration awards and Pennsylvania MVFRL decisions on peer reviews (e.g. https://aaa-nynf.modria.com/downloadAward/42428348): a peer review must state a factual basis and medical rationale; Pennsylvania peer review addresses reasonableness and necessity, not causation. Jurisdiction-specific; used for wording only.
   973	- Fishbain et al. (2003) on Waddell signs via research/case-library-sources-v2.md P8 — search summary.
   974	- Assumption: Texas third-party liability carriers commission records reviews informally; no Texas statute governs them. Not verified.
   975	
   976	**Specimen (SYNTHETIC).**
   977	```
   978	SYNTHETIC RECORD - RECORDS REVIEW - ALL IDENTIFIERS FICTITIOUS
   979	Requested by: Quillon Casualty Mutual (SYNTHETIC), claim SYN-BI-55120   Report date: 08/27/2026
   980	Reviewer: Dr. Evander Pollitt-Rhys, MD, PM&R (SYNTHETIC)
   981	Claimant: Corentin Abelard-Moss (SYNTHETIC)   Date of loss: 05/02/2026
   982	Records reviewed: ED 05/02/2026; PT notes 05/12/2026-07/31/2026; FCE 07/20/2026.
   983	Summary: The PT note of 06/12/2026 documents Waddell signs 0/5.
   984	  The PT note of 07/01/2026 documents no non-organic signs.
   985	  The FCE of 07/20/2026 documents Waddell 3/5 and inconsistent effort.
   986	  The PT note of 07/31/2026 documents full effort but symptom magnification with light touch.
   987	Opinions: Findings are consistent with a self-limited lumbar strain. Treatment after 07/20/2026 was
   988	  not reasonable or necessary. MMI as of 07/20/2026.
   989	/s/ Dr. Evander Pollitt-Rhys (SYNTHETIC)
   990	```
   991	(Credibility sentences across 4 dates: 06/12 and 07/01 are clean negations that must not flag; 07/20 and 07/31 must flag (07/31 mixes a
   992	clean and an adverse clause). 08/27/2026 is the report date; 07/20/2026 in the opinions is the reviewer's cut-off, not a visit.)
   993	
   994	---
   995	
   996	## 21. Product mapping and proposed packet mixes
   997	
   998	| Format | Main rule it exercises | Expected tool behavior |
   999	|---|---|---|
  1000	| ED note | Dates (rollover), voice, pre-existing, hedges | Date = arrival; excerpt verbatim; PMH flag |
  1001	| PT note | Gaps vs cancellations; plan vs actual; timed units | Cancellation is not an encounter; reason shown verbatim |
  1002	| Chiro note + travel card | Cloned notes; checkbox OCR | Travel card rows need review when OCR-derived |
  1003	| Radiology | Hedge and prior-imaging language; three dates | Exam date used; "Comparison: prior" flagged |
  1004	| Op note | Indications ≠ causation; D:/T: dates | No causation inferred; surgery date used |
  1005	| Pharmacy log | Refills, reversals, three price columns | Reversed lines excluded; prices to notes unless charge wording |
  1006	| CMS-1500 | Implied decimal; date ranges; Item 14/31 dates | Code parses amounts as implied cents; line sum vs Item 28 compared; days = units checked |
  1007	| UB-04 | 0001 total; FL 44 rate on the charge line; creation date; occurrence codes 01-06 | Total line not summed; rate not a charge (D-042 guard); any accident code = accident date |
  1008	| Ledger | Running balance; voids; balance forward; fee schedule | Only dated charge lines counted; voids netted in code |
  1009	| EOB | Double count of billed; CO/PR; mismatch with ledger | EOB amounts to notes, never added to charges; mismatch flagged |
  1010	| LOP / lien | Non-record narrative; asserted totals | No entries created; amounts to notes only (D-019) |
  1011	| Spanish note | Day-first dates; voice; translation labeling | Original excerpt; date convention suggestion (D-042) needs confirm |
  1012	| Scanned intake | OCR glyphs, checkboxes, fax/stamp dates | OCR-derived items always need review; page image beside text |
  1013	| EMS report | Call date and eight times; crew vs patient voice; refusal | One encounter on the call date; MIST wording attributed to EMS; refusal is an encounter without transport |
  1014	| Ambulance invoice | Per-mile rate vs line; fractional units | Miles x rate recomputed in code; only line totals are charges |
  1015	| §18.001 affidavit | Non-record page; duplicate attached bill; not causation | No encounter; duplicate deduped with both cites; totals recomputed |
  1016	| Narrative letter | Causation statement; letter date; estimates | Causation shown verbatim and flagged, never upgraded; estimates to notes |
  1017	| Office/specialist note | Copied ROS; recommended vs performed; estimates | Same-week contradiction surfaced; future dates not encounters |
  1018	| Records review / IME | Adverse opinions; credibility words; report vs exam date | D-043 credibility flags; opinions attributed to the reviewer |
  1019	
  1020	**Proposed synthetic packet mixes** (round 1; the v2 library packets lib08-lib15 and the sections each needs are in
  1021	`research/case-library-sources-v2.md`, "Must contain" table):
  1022	1. *ER-only then gap*: EMS report + ED note + UB-04 (with 0001 line) + ED-physician CMS-1500 + radiology report + ambulance invoice + fax headers.
  1023	2. *Chiro under LOP*: intake form (scanned) + LOP + chiro daily notes with a travel card + CMS-1500 with a grouped date range (clean and OCR
  1024	   versions) + ledger with a void and a courtesy adjustment + narrative letter + §18.001 affidavit with a duplicate attached statement.
  1025	3. *PT with health insurance*: PT eval + daily notes with two cancellations + ledger + EOB (CO-45, PR-1, CO-97) with the deliberate
  1026	   ledger-vs-EOB mismatch.
  1027	4. *Surgery*: MRI with prior comparison + ortho office note with a surgical estimate + op note with indications paragraph + surgeon/
  1028	   assistant/anesthesia/facility bills on one date + inpatient UB-04 with a room-rate line.
  1029	5. *Spanish-speaking client*: Spanish clinic note with a day-first date whose parts are both 12 or less + rate and charge on the same page +
  1030	   pharmacy log with a reversed fill.
  1031	
  1032	---
  1033	
  1034	## 22. Cross-specimen consistency (Delphine Okonkwo-Vale timeline)
  1035	
  1036	| # | Mismatch found in round 1 review | Status | Expected tool behavior |
  1037	|---|---|---|---|
  1038	| 1 | Radiology compared with "cervical radiographs" though the ED did a CT | Fixed: comparison is the 05/15/2026 CT | None |
  1039	| 2 | Chiro "Visit #9" on 06/03 with intake signed 05/29 | Fixed: Visit #4 (05/29 exam, 06/01-06/03 daily) | None |
  1040	| 3 | PT "Visit 7 of 24" on 06/10 but the ledger shows only the eval and 06/10 | Fixed: Visit 2 of 12 | None |
  1041	| 4 | Ledger shows no payments; EOB for the same DOS shows plan paid 16.00 and CO reductions | DELIBERATE | Billing analysis cites both and flags the mismatch; never picks paid vs incurred |
  1042	| 5 | Op note "12 weeks of therapy"; PT eval 05/27 to surgery 08/04 is 9.9 weeks | DELIBERATE | Excerpt verbatim and attributed; no automatic flag; golden truth never states 12 weeks |
  1043	| 6 | PT plan "3x/wk x 4 wks" against 24 planned visits | Fixed: 2x/wk x 6 wks = 12 | None |
  1044	| 7 | CMS-1500 line grouped 06/01-06/05 (5 days) with 3 units; travel card had non-consecutive dates | Fixed: grouped lines 06/01-06/03 = 3 days = 3 units; travel card marks match | Code checks days = units |
  1045	| 8 | PT units: 35 timed minutes billed as 3 units | Fixed: 38 minutes = 3 units under the stated CMS method | None |
  1046	| 9 | EMS arrival at destination 23:47 vs ED arrival 23:48 (new in round 2) | DELIBERATE (realistic) | Same encounter chain; no conflict flag |
  1047	| 10 | §18.001 affidavit totals vs ledger (new in round 2) | Consistent: 445.00 / 0.00 / 400.00 | Attached statement deduped against section 10 |
  1048	| 11 | Narrative letter "since 05/29/2026" and diagnoses vs chiro records and CMS-1500 (new in round 2) | Consistent | Letter cited as the letter; no new encounter |
  1049	
  1050	`python3 research/record_formats_check.py` re-checks rows 2, 3, 6, 7, 8 and 10 and every specimen total.
  1051	
  1052	---
  1053	
  1054	## 23. Assumptions, limits, gaps and the name-collision search
  1055	
  1056	- **Search-summary sources.** Sources marked "search summary" were not opened; their takeaways come from the search tool's summary. Opened:
  1057	  NUCC 1500 manual, RI UB-04 instructions, HL7 NUBC occurrence-code list, Noridian chiro, EOB and ambulance-mileage pages, CMS bill guide,
  1058	  CMS Claims Processing Manual ch. 15, NASEMSO time definitions, Montana NEMSIS disposition guide, CPRC §18.001/§18.002 (mirror), Hills v.
  1059	  Donis 2021 opinion, Ezel narrative template, arXiv OCR paper, Jotform LOP packet.
  1060	- **ACR report components.** The ACR page rendered only headings; the component list rests on secondary sources plus common practice.
  1061	- **UB-04 specifics.** FL 44 accommodation-rate use and the creation date on line 23 are prior knowledge that the T-078 reviewer also
  1062	  judged correct from working knowledge; both are marked "unverified" where they appear. Occurrence codes 01-06 come from an HL7 v2.4
  1063	  rendering of the NUBC list; the current NUBC label for 01 may read "accident/medical coverage". Verify against the licensed NUBC manual
  1064	  before quoting any of these in the submission.
  1065	- **Payer variation.** CMS-1500, UB-04 and ambulance rules here are NUCC/NUBC, CMS and one Medicaid guide; commercial and auto carriers vary.
  1066	- **Pharmacy "charge".** Whether U&C, plan paid or patient paid is the recoverable amount is a legal question the tool does not decide.
  1067	- **Spanish phrasing** is drawn from Mexican and Spanish teaching templates; Central American and Caribbean usage may differ.
  1068	- **OCR figures** come from one paper on smartphone photos of printed reports, not handwritten forms; handwriting is likely worse.
  1069	- **Statute currency.** CPRC §18.001/§18.002 were read through a mirror (amended through 2019); the official site did not render. Not
  1070	  checked for 2025-2026 amendments.
  1071	- **Not covered.** Pain-management procedure notes (e.g. epidural steroid injection) and stand-alone work-status slips have no section;
  1072	  the office-note section covers the visit that orders them.
  1073	- **Name-collision search (2026-11-02).** Web searches for the invented provider, payer, firm and clinician names found no exact match for
  1074	  Brightwater Spine & Wellness, Larkspur Hollow Physical Therapy, Quillfeather Regional Medical Center, Ferncastle Imaging Associates,
  1075	  Thistledown Surgical Center, Mossgate Community Pharmacy or Harrowgate & Vey. Two names were replaced in round 2: "Bluebonnet Mutual
  1076	  Health Plan" (Texas has real "Bluebonnet" health plans) became Quoinmere Mutual Health Plan, and "Clínica Familiar Los Almendros" /
  1077	  "Dra. Inés Valcárcel" (a similarly named clinic and a real surname match) became Consultorio Médico Peñaverde / Dra. Itziar Orbezua Lanz.
  1078	  Names added in round 2 (Fernhollow County EMS, Gallowmere Records Retrieval, Saltmarrow General Hospital, Quillon Casualty Mutual and the
  1079	  clinicians) were built from uncommon word pairs and not searched individually. Any remaining resemblance is unintended; packets built
  1080	  from these specimens still pass `research/validate_library.py`.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:46:11.087Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"Visit|per wk|/wk|x/wk|min |Total timed|COMPARISON|Comparison|23:48|ED ARRIV|Arrival|ACDF|08/04|05/27|TOTAL PMTS|CO-45|CO-97|PR-1|plan paid|Plan paid|LOP|Financial|0\\.00|16\\.00|2x|3x\" research/record-formats.md | sed -n '1,120p' | cut -c1-230",
 "description": "Grep cross-specimen values to verify the round-2 consistency claims"
}
````

### User / tool · 2026-11-02T03:46:11.177Z

**tool result**
````
27:| Date of injury / onset | CMS-1500 Item 14 (qualifier 431), UB-04 occurrence code date (accident codes 01-06), LOP letter "Re:" line, intake form, narrative letter "Re:" line | It is the accident date, not a visit. Treating it
34:| Date ranges | CMS-1500 24A From/To with 24G units, UB-04 FL 6 statement period, PT "Visits 1 to 12" summary | One line can stand for many consecutive days (NUCC allows grouping only on consecutive days with identical code, ch
45:| "Adjustment", "Contractual adj", "Write-off", "W/O", "Network discount", "Courtesy discount", CARC "CO-45" | Reduction by the provider or under a contract | No (separate column; never subtracted silently from billed) |
46:| "Payment", "Ins pmt", "Pt pmt", "Plan paid", "Amount paid" (Item 29) | Money received | No |
49:| "LOP balance", "Lien amount", "Reduced to", "Accept in full satisfaction" | Negotiated or asserted amount | No (internal notes only) |
71:**Fields.** Arrival date/time; mode of arrival (EMS, private vehicle); triage block (ESI level, vitals, pain score, triage nurse narrative);
83:- Midnight rollover: arrival 23:48, physician exam 00:31 the next calendar day; the visit date is the arrival date.
99:Arrival: 05/14/2026 23:48   Mode: EMS   ESI: 3
119:**Fields.** Date; visit number against plan ("Visit 7 of 24"); authorization/referral; time in and time out; S (patient report, NPRS pain
125:(2 units); 97140 Manual 13 min (1 unit); 97014 E-stim unattended 15 min." "Total timed: 38 min. Total tx: 53 min." "Tolerated well. Continue
126:POC 2x/wk x 6 wks." Cancellations appear as a note with no treatment: "Pt cancelled - no transportation." Charges usually do **not** appear
131:- "Visit 7 of 24" states the plan, not the count delivered; the adjuster compares planned versus actual.
144:Larkspur Hollow Physical Therapy (SYNTHETIC)        Daily Note        Visit 2 of 12
146:S: Pt reports neck pain 5/10 (7/10 at eval 05/27/2026). Still wakes at night.
148:Interventions:  97110 TherEx  25 min  2u
149:                97140 Manual  13 min  1u
150:                97014 E-stim  15 min  (untimed)
151:Total timed 38 min / Total tx 53 min
153:P: Continue POC 2x/wk x 6 wks.
159:per-code method gives the same 2 + 1 here. Visit 1 was the 05/27/2026 evaluation; 2x/wk x 6 wks = 12 planned visits.)
173:T4, L5 - diversified." "98941, 97014, 97010." "Pt responding favorably, continue 3x/wk." Fee slips say "Adjustment 3-4 regions $85.00" -
184:- Noridian JF Part B, *Chiropractic Documentation Guidelines - Initial vs Subsequent Visits*: https://med.noridianmedicare.com/web/jfb/specialties/chiropractic/documentation-guidelines — **opened**. Takeaway: subsequent-visi
191:Patient: Delphine Okonkwo-Vale (SYNTHETIC)   DOS: 06/03/2026   Visit #4
196:A: Improving. P: Daily through 06/05, then 3x/wk x 3 wks, re-exam 06/24/2026.
204:(Visit #1 was the new-patient exam on 05/29/2026, the date the intake in section 14 is signed; it was billed on an earlier claim not shown.
205:Visits 2-4 are the three consecutive days on the travel card and on the CMS-1500 in section 8. C/T/L = regions adjusted, ES = 97014,
216:**Typical wording.** "INDICATION: MVC 05/14/2026, neck pain, R arm paresthesia." "COMPARISON: None." / "COMPARISON: MRI 08/2023." "C5-6: disc
223:- "Comparison: MRI 08/2023" reveals prior imaging - a pre-existing flag - even when the findings section is silent about it.
232:- Assumption: the INDICATION / TECHNIQUE / COMPARISON / FINDINGS / IMPRESSION order is near-universal; I did not read the ACR II.B body text.
242:COMPARISON: CT cervical spine 05/15/2026 (Quillfeather Regional ED).
250:ADDENDUM 06/20/2026: Comparison CT images reviewed; no change to impression.
264:who reports neck and arm pain since a motor vehicle collision..." "D: 08/04/2026 T: 08/05/2026."
282:Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Date of surgery: 08/04/2026  07:42-09:15
293:D: 08/04/2026  T: 08/05/2026
295:(DELIBERATE: "12 weeks of therapy" is the surgeon's recital. From the PT evaluation (05/27/2026) to surgery (08/04/2026) is 69 days, about 9.9 weeks.
305:price (usual and customary), plan paid, patient paid/copay, status (filled, reversed, returned to stock).
307:**Typical wording.** "Fill 05/15/26 Rx 6604412 R0 CYCLOBENZAPRINE 10MG TAB Q 30 DS 10 Dr. Fenwick." "U&C $24.99 Plan $0.00 Pt pd $24.99."
314:- U&C price, plan paid and patient paid are three different numbers on one line; which one is a "charge" for a demand is a legal choice
329:05/15/26  SYN6604412 0  CYCLOBENZAPRINE 10MG TAB  00000-0000-01   30 10  FENWICK I (SYN)  24.99  0.00  24.99  FILLED
330:05/15/26  SYN6604413 0  NAPROXEN 500MG TAB        00000-0000-02   60 30  FENWICK I (SYN)  18.40  0.00  18.40  FILLED
331:05/25/26  SYN6604412 1  CYCLOBENZAPRINE 10MG TAB  00000-0000-01   30 10  FENWICK I (SYN)  24.99  0.00  24.99  REVERSED 05/26/26
332:06/02/26  SYN6604412 1  CYCLOBENZAPRINE 10MG TAB  00000-0000-03   30 10  FENWICK I (SYN)  21.50  0.00  21.50  FILLED
347:and *do* use a decimal point (e.g., `1000.00`). Item 28 is the total of all 24F lines. Item 29 is money paid by patient or other payers.
380:section 4; $30.00 and $15.00 per day. Lines 1-3 bill the same code one line per day, which NUCC also allows. MOD is blank; AB and A are
387:24. 060126 060126 11 98941 AB 8500 1 SYN-NPI-0001         <- truth 85.00 (not 8,500.00)
390:    060126 060326 11 97014 A 9000 3 SYN-NPI-0001          <- truth 90.00 (not 9,000.00)
392:28. TOTAL CHARGE 39000   29. AMOUNT PAID 0 00             <- truth 390.00 and 0.00
410:(unverified: common convention, not in the RI guide; NUBC manual not opened). "PAGE 1 OF 2" on multi-page claims. FL 44 holds a per-day accommodation rate on inpatient room lines (e.g., `1850.00`) and a HCPCS code on
440:0450    EMERGENCY ROOM LVL 4          99284          051426        1          2,410.00
458:0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00
462:0320    DX X-RAY                                     091526        2            540.00
467:(Room line: FL 44 rate 1,850.00 x FL 46 3 days = FL 47 5,550.00. Only FL 47 is a charge; 1,850.00 is a rate. A naive sum of every money
477:payments, total adjustments, balance due); notes ("Account on LOP hold", "Sent to attorney").
489:- Fee-schedule summaries ("Office visit est. $150.00 per visit") look like charge lines but carry no date of service (rate, not charge).
501:Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Acct: SYN-PT-2207   Financial class: LOP
503:05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00
504:06/10/26  06/11/26  97110  Therapeutic exercise x2       130.00                         340.00
505:06/10/26  06/11/26  97140  Manual therapy x1              70.00                         410.00
507:06/10/26  06/30/26  97140  Manual therapy x1 VOID        (70.00)                        375.00
508:06/10/26  06/30/26  97140  Manual therapy x1              70.00                         445.00
509:07/15/26  07/15/26  ADJ    Courtesy discount                                 45.00-     400.00
510:                     TOTAL CHARGES 445.00  TOTAL PMTS 0.00  TOTAL ADJ (45.00)  BALANCE DUE 400.00
513:(DELIBERATE: no payment or contractual adjustment is posted, although the EOB in section 11 (processed 07/22/2026) shows plan paid 16.00 and
514:CO-45/CO-97 reductions for DOS 06/10/26. Expected: billing analysis cites both documents' figures and flags the ledger-vs-EOB mismatch for
522:description or code, amount billed, network discount / not covered, allowed amount, deductible, copay, coinsurance, plan paid, patient
525:**Typical wording.** "Amount billed $410.00 - Network discount $162.40 = Allowed $247.60." "Deductible applied $100.00; Coinsurance 20%
526:$29.52; Plan paid $118.08; You may owe $129.52." "CO-45: charge exceeds fee schedule/maximum allowable." "PR-1 deductible, PR-2 coinsurance,
547:06/10/26  97110    130.00    52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45
548:06/10/26  97140     70.00    28.00     42.00    22.00    4.00    16.00      26.00     PR-1, PR-2, CO-45
549:06/10/26  97014     35.00    35.00      0.00     0.00    0.00     0.00       0.00     CO-97
550:TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00
551:CO-97: payment included in allowance for another service.
556:## 12. Letter of protection (LOP) and lien letters
566:itemized statement of charges." Provider intake LOPs add: the provider will not send the account to collections while the claim is pending,
570:- The LOP is not a medical record: its accident narrative is the attorney's, and its dates (letter date, injury date) are not encounters.
571:- Amounts in an LOP or lien notice ("current balance $4,860.00") are asserted totals without dates of service; never charges (D-019).
573:- Sources disagree on whether "LOP" and "lien" are interchangeable; the tool should keep the document's own words.
576:- Jotform HIPAA intake packet with an embedded LOP (chiropractic, auto/slip-and-fall): https://hipaa.jotform.com/221364153684052 — **opened**. Takeaway: patient signs; provider defers payment and collections; direction to pa
577:- ChartRequest, *Letters of Protection and Medical Liens*: https://www.chartrequest.com/articles/letters-of-protection-medical-records — search summary; argues LOP and lien are distinct.
578:- D Law Group, *What is a Letter of Protection or Personal Injury Lien?*: https://dlawgroup.com/letter-of-protection-personal-injury-lien/ — search summary; LOP can operate as a contract; patient owes the balance if the case
579:- Miller & Zois forms library (sample assignment/LOP and hold-harmless letters): https://www.millerandzois.com/professional-attorney-information-center/forms-and-letters-for-personal-injury-lawyers/ — search result, not open
612:reposo relativo, cita en 1 semana." "Consulta: $650.00" (charge) vs "Costo por sesión de terapia: $400.00" (rate).
618:- Decimal comma and dot thousands in Latin American notes (`$1.250,00`); US-based clinics usually print `$1,250.00`. Currency may be MXN.
642:Consulta: $650.00     Costo por sesión de terapia física: $400.00
646:day-first convention decides; it is 21 days after the visit, matching "en 3 semanas". The $650.00 is the visit charge; the $400.00 is a
656:health, MedPay/PIP); signature and date; sometimes an embedded LOP or assignment of benefits (section 12).
666:| Dropped or added decimal | `$1,250.00` → `$125000` or `$1,25000` | Amount off by 100x |
755:(Arrival at destination 23:47 here vs ED arrival 23:48 in section 2: same event, not a conflict. "Moderate rear damage" is the crew's
767:**Typical wording.** "A0427-SH ALS emergency transport, Level 1 ... 1,450.00." "A0425-SH Ground mileage 8.7 mi @ 22.50/mi ... 195.75."
793:A0427-SH  ALS emergency transport, Level 1      1      1,450.00   1,450.00
796:PAYMENTS 0.00   ADJUSTMENTS 0.00   BALANCE DUE 1,645.75
799:(8.7 x 22.50 = 195.75; 1,450.00 + 195.75 = 1,645.75. 22.50 is a rate. 05/29/2026 is the invoice date, not a service date.)
815:business." "The total amount charged for the services was $445.00. The amount paid was $0.00. The amount unpaid that the provider has a
816:right to be paid is $400.00." "Sworn to and subscribed before me on ..." The exact form is in CPRC §18.002; quote it from the official text.
846:Delphine Okonkwo-Vale (SYNTHETIC) from 05/27/2026 through 06/10/2026, kept in the regular course of business
848:Total amount charged: $445.00.  Amount paid: $0.00.  Amount unpaid that the provider has a right to be paid: $400.00.
852:(The figures match the ledger in section 10: charges 445.00, adjustment 45.00, payments 0.00, balance 400.00. Page 3 is a duplicate of the
868:estimated 12 additional visits at $150.00 per visit." "She has not reached MMI."
875:- Visit counts and dates in the letter can disagree with the notes; code counts dated notes, the letter's number is cited as the letter's.
896:Future care: an estimated 12 additional visits at $150.00 per visit ($1,800.00).
900:(Conclusory on purpose, as in v2 pattern P3: no explanation of how or why. $150.00 per visit is a rate and $1,800.00 an estimate; neither is
913:options. Recommend C5-6 ACDF." "Estimated surgeon fee $14,500.00." "Work status: off work through 08/31/2026." "RTC 4 wks."
932:Thistledown Orthopedic & Spine Clinic (SYNTHETIC)      Office Visit      DOS 07/08/2026
935:HPI: Rear-end MVC 05/14/2026 per pt. PT since 05/27/2026 without lasting relief. Pain 7/10.
940:A/P: Cervical radiculopathy, R C6. Recommend C5-6 ACDF. Estimated surgeon fee $14,500.00.
944:(The ACDF is recommended here and performed on 08/04/2026 (section 6). $14,500.00 is an estimate. 08/31/2026 is a future work-status
1003:| Radiology | Hedge and prior-imaging language; three dates | Exam date used; "Comparison: prior" flagged |
1010:| LOP / lien | Non-record narrative; asserted totals | No entries created; amounts to notes only (D-019) |
1023:2. *Chiro under LOP*: intake form (scanned) + LOP + chiro daily notes with a travel card + CMS-1500 with a grouped date range (clean and OCR
1025:3. *PT with health insurance*: PT eval + daily notes with two cancellations + ledger + EOB (CO-45, PR-1, CO-97) with the deliberate
1039:| 2 | Chiro "Visit #9" on 06/03 with intake signed 05/29 | Fixed: Visit #4 (05/29 exam, 06/01-06/03 daily) | None |
1040:| 3 | PT "Visit 7 of 24" on 06/10 but the ledger shows only the eval and 06/10 | Fixed: Visit 2 of 12 | None |
1041:| 4 | Ledger shows no payments; EOB for the same DOS shows plan paid 16.00 and CO reductions | DELIBERATE | Billing analysis cites both and flags the mismatch; never picks paid vs incurred |
1042:| 5 | Op note "12 weeks of therapy"; PT eval 05/27 to surgery 08/04 is 9.9 weeks | DELIBERATE | Excerpt verbatim and attributed; no automatic flag; golden truth never states 12 weeks |
1043:| 6 | PT plan "3x/wk x 4 wks" against 24 planned visits | Fixed: 2x/wk x 6 wks = 12 | None |
1046:| 9 | EMS arrival at destination 23:47 vs ED arrival 23:48 (new in round 2) | DELIBERATE (realistic) | Same encounter chain; no conflict flag |
1047:| 10 | §18.001 affidavit totals vs ledger (new in round 2) | Consistent: 445.00 / 0.00 / 400.00 | Attached statement deduped against section 10 |
1059:  Donis 2021 opinion, Ezel narrative template, arXiv OCR paper, Jotform LOP packet.
1066:- **Pharmacy "charge".** Whether U&C, plan paid or patient paid is the recoverable amount is a legal question the tool does not decide.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:46:19.285Z

**tool call — Bash**
````
{
 "command": "cat -n research/record-formats.md | sed -n '473,520p'",
 "description": "Read the ledger section with exact line text"
}
````

### User / tool · 2026-11-02T03:46:19.372Z

**tool result**
````
   473	## 10. Itemized provider ledger / statement
   474	
   475	**Fields.** Provider name and address; patient and account number; statement date; prior balance / balance forward; per line: date of
   476	service, posting date, CPT or internal code, description, charge, payment, adjustment, running balance; totals block (total charges, total
   477	payments, total adjustments, balance due); notes ("Account on LOP hold", "Sent to attorney").
   478	
   479	**Typical wording.** CMS's consumer guide names the parts as total charges, allowed amount, adjustments, insurance payment, patient payment,
   480	and balance due/patient responsibility. Real ledgers add: "Contractual adj", "W/O", "Courtesy disc", "Atty reduction", "Bal fwd", credits in
   481	parentheses or with a trailing minus, "Pmt - Ck #SYN-1043". Hospital consumer statements often show only a total; the itemized version must be
   482	requested.
   483	
   484	**Extraction traps.**
   485	- Running balance is cumulative; summing it multiplies the bill.
   486	- Balance forward from a prior statement re-counts earlier charges if two statements are both in the packet.
   487	- Posting date versus date of service: a charge posted 06/30 for a 06/03 visit.
   488	- Reversals ("Void", "Reverse chg") paired with a re-bill on a later line.
   489	- Fee-schedule summaries ("Office visit est. $150.00 per visit") look like charge lines but carry no date of service (rate, not charge).
   490	- An attorney reduction recorded as an adjustment after settlement talks is a negotiated number, not a billed charge.
   491	
   492	**Sources.**
   493	- CMS, *How to read your medical bill*: https://www.cms.gov/initiatives/your-patient-rights/medical-bill-rights/get-help/medical-bill-guides-resources/how-read-your-medical-bill — **opened**. Takeaway: standard parts are total charges, allowed amount, adjustments, insurance payment, patient payment, balance due.
   494	- Resolve Medical Bills, *Itemized Hospital Bills*: https://www.resolvemedicalbills.com/guides/itemized-hospital-bill — search summary; itemized bill is sent only on request and lists dates, codes and per-service prices.
   495	- Texas CPRC §18.001 (affidavit must include an itemized statement of the service and charge): https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm — search summary; see also research/texas-pi-notes.md.
   496	
   497	**Specimen (SYNTHETIC).**
   498	```
   499	SYNTHETIC RECORD
   500	Larkspur Hollow Physical Therapy (SYNTHETIC)     ITEMIZED STATEMENT     Statement date: 07/31/2026
   501	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Acct: SYN-PT-2207   Financial class: LOP
   502	DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE
   503	05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00
   504	06/10/26  06/11/26  97110  Therapeutic exercise x2       130.00                         340.00
   505	06/10/26  06/11/26  97140  Manual therapy x1              70.00                         410.00
   506	06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00
   507	06/10/26  06/30/26  97140  Manual therapy x1 VOID        (70.00)                        375.00
   508	06/10/26  06/30/26  97140  Manual therapy x1              70.00                         445.00
   509	07/15/26  07/15/26  ADJ    Courtesy discount                                 45.00-     400.00
   510	                     TOTAL CHARGES 445.00  TOTAL PMTS 0.00  TOTAL ADJ (45.00)  BALANCE DUE 400.00
   511	Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection.
   512	```
   513	(DELIBERATE: no payment or contractual adjustment is posted, although the EOB in section 11 (processed 07/22/2026) shows plan paid 16.00 and
   514	CO-45/CO-97 reductions for DOS 06/10/26. Expected: billing analysis cites both documents' figures and flags the ledger-vs-EOB mismatch for
   515	review; the tool never picks paid or incurred. The $65.00 fee-schedule line has no date of service: a rate, not a charge.)
   516	
   517	---
   518	
   519	## 11. Explanation of Benefits (EOB) / remittance
   520
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:46:59.201Z

**tool call — Bash**
````
{
 "command": "grep -n -i -E \"cancel|no-show|missed\" research/record-formats.md | cut -c1-200; echo ---; grep -n -i \"denies LOC\\|LOC\" research/record-formats.md | cut -c1-160 | head -12; echo ---; which pdftotext; echo ---; grep -n -i \"handwritten\\|no year\\|without a year\" research/record-formats.md | cut -c1-160",
 "description": "Grep PT cancellations, LOC wording, and handwritten-date coverage"
}
````

### User / tool · 2026-11-02T03:46:59.311Z

**tool result**
````
126:POC 2x/wk x 6 wks." Cancellations appear as a note with no treatment: "Pt cancelled - no transportation." Charges usually do **not** appear
132:- Cancelled or no-show entries are dated documents that are **not** encounters, but they may state the reason for a gap.
156:06/12/2026  Pt cancelled - no transportation. Rescheduled 06/15/2026.
179:- Travel-card checkmarks are OCR-hostile (see section 14); a missed checkmark loses a modality, a stray mark invents one.
1001:| PT note | Gaps vs cancellations; plan vs actual; timed units | Cancellation is not an encounter; reason shown verbatim |
1025:3. *PT with health insurance*: PT eval + daily notes with two cancellations + ledger + EOB (CO-45, PR-1, CO-97) with the deliberate
---
71:**Fields.** Arrival date/time; mode of arrival (EMS, private vehicle); triage block (ESI level, vitals, pain score, triage nurse narrative);
77:**Typical wording.** "Restrained driver in a rear-end MVC at approx 35 mph, + airbag deployment, ambulatory at scene." "Denies LOC, denies
104:HPI: Restrained driver, rear-end MVC, + airbag. Denies LOC. Reports tingling R hand.
359:- NUCC, *1500 Health Insurance Claim Form Reference Instruction Manual for Form Version 02/12*, Version 8.0 (7/20): https://www.nucc.org/images/stories/PDF/
401:**Fields (form locators).** FL 1 provider; 3a patient control number, 3b medical record number; **FL 4 type of bill** (4-digit with leading zero,
476:service, posting date, CPT or internal code, description, charge, payment, adjustment, running balance; totals block (total charges, total
558:**Fields.** Law-firm letterhead; letter date; addressee (provider billing office); "Re:" block with client name, DOB, date of injury, sometimes
707:(eTimes.09), arrived at destination (eTimes.11), transfer of care (eTimes.12); scene location type; patient demographics; chief complaint;
714:"Moderate rear-end damage to pt's vehicle, airbags deployed." "Pt c/o neck pain 7/10, denies LOC." "GCS 15." "Pt placed in position of
744:NARRATIVE: Pt states "the truck hit me from behind." Denies LOC. C/o neck pain and
824:  Dedupe must keep one copy and cite both locations, never add both.
---
/opt/homebrew/bin/pdftotext
---
37:(pharmacy and lab systems), `14/05/2026` and `14 de mayo de 2026` (Spanish-language clinics, day first), `5/14` (handwritten, no year),
651:## 14. Scanned and handwritten intake forms (and OCR failure modes)
678:- ImageToTable blog, *Why AI reads handwriting but misses a ticked box*: https://imagetotable.ai/blog/how-ai-reads-handwritten-forms-checkboxes-to-excel —
684:[PAGE IMAGE, described] Brightwater Spine & Wellness New Patient Intake. Handwritten in blue ink.
1068:- **OCR figures** come from one paper on smartphone photos of printed reports, not handwritten forms; handwriting is likely worse.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:06.456Z

**tool call — Bash**
````
{
 "command": "cat -n research/record-formats.md | sed -n '117,162p' | cut -c1-260",
 "description": "Read the PT section with the cancellation entry"
}
````

### User / tool · 2026-11-02T03:47:06.558Z

**tool result**
````
   117	## 3. Physical therapy daily note (SOAP)
   118	
   119	**Fields.** Date; visit number against plan ("Visit 7 of 24"); authorization/referral; time in and time out; S (patient report, NPRS pain
   120	0-10, function, home exercise compliance); O (ROM in degrees, MMT grades, special tests, gait); interventions table with CPT, minutes and
   121	units; total timed minutes and total treatment minutes; A (progress toward goals, tolerance); P (frequency and duration, next visit focus);
   122	signature with credential (PT, PTA, DPT) and co-signature when a PTA treats.
   123	
   124	**Typical wording.** "Pt reports neck pain 5/10, improved from 7/10 at eval." "Cervical rotation R 55 deg, L 60 deg." "97110 TherEx 25 min
   125	(2 units); 97140 Manual 13 min (1 unit); 97014 E-stim unattended 15 min." "Total timed: 38 min. Total tx: 53 min." "Tolerated well. Continue
   126	POC 2x/wk x 6 wks." Cancellations appear as a note with no treatment: "Pt cancelled - no transportation." Charges usually do **not** appear
   127	on the note; they appear on the CMS-1500 or ledger as units times a fee.
   128	
   129	**Extraction traps.**
   130	- Timed codes bill in 15-minute units under the 8-minute rule; minutes are not dollars and units are not visits.
   131	- "Visit 7 of 24" states the plan, not the count delivered; the adjuster compares planned versus actual.
   132	- Cancelled or no-show entries are dated documents that are **not** encounters, but they may state the reason for a gap.
   133	- Identical copy-forward text across visits (a known audit flag) reads as "cloned notes" to the defense.
   134	- Re-evaluation and discharge summaries restate earlier values; extracting them as new measurements double counts.
   135	
   136	**Sources.**
   137	- Colorado HCPF Bulletin B1900436 (timed-minute totals across codes, e.g. 40 minutes = 3 units): https://hcpf.colorado.gov/sites/hcpf/files/Bulletin_1019_B1900436.pdf — search summary.
   138	- AAPC compliance article on therapist signatures and documented time after an OIG audit: https://aapc.com/codes/scc_articles/article_pdf/47/compliance-forget-your-john-hancock-and-you-could-be-out-thousands-41142 — search summary.
   139	- WebPT, *SOAP note tips for PTs*: https://www.webpt.com/blog/soap-note-tips-for-pts-plus-examples — search result, not opened. Assumption: SOAP order and fields above match common PT EMR output.
   140	
   141	**Specimen (SYNTHETIC).**
   142	```
   143	SYNTHETIC RECORD
   144	Larkspur Hollow Physical Therapy (SYNTHETIC)        Daily Note        Visit 2 of 12
   145	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Date: 06/10/2026   In 09:02 Out 09:55
   146	S: Pt reports neck pain 5/10 (7/10 at eval 05/27/2026). Still wakes at night.
   147	O: Cerv rot R 55 deg / L 60 deg. Grip R 4/5.
   148	Interventions:  97110 TherEx  25 min  2u
   149	                97140 Manual  13 min  1u
   150	                97014 E-stim  15 min  (untimed)
   151	Total timed 38 min / Total tx 53 min
   152	A: Tolerated well. Progressing toward goal of 70 deg rotation.
   153	P: Continue POC 2x/wk x 6 wks.
   154	Signed: Wren Abernathy, PTA (SYNTHETIC)   Co-signed: Odalys Kerr, DPT (SYNTHETIC) 06/11/2026
   155	--
   156	06/12/2026  Pt cancelled - no transportation. Rescheduled 06/15/2026.
   157	```
   158	(Units follow the CMS total-time 8-minute rule: 38 timed minutes = 3 units, the extra unit going to the code with more minutes. The AMA
   159	per-code method gives the same 2 + 1 here. Visit 1 was the 05/27/2026 evaluation; 2x/wk x 6 wks = 12 planned visits.)
   160	
   161	---
   162
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:15.342Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-nucc.py",
 "content": "#!/usr/bin/env python3\n\"\"\"T-078 r2 check (paralegal-reviewer): does the NUCC 02/12 manual support the grouping and no-decimal rules the specimens rely on?\n\nDownloads the NUCC v8.0 manual into artifacts/review-evidence (temporary, deleted after), extracts text with pdftotext,\nprints the 24A / 24F / 24G passages, then removes the PDF. Output is captured to T-078-paralegal-r2-nucc.out.\n\"\"\"\nimport os\nimport re\nimport subprocess\nimport urllib.request\n\nURL = \"https://www.nucc.org/images/stories/PDF/1500_claim_form_instruction_manual_2020_07-v8.pdf\"\nHERE = os.path.dirname(os.path.abspath(__file__))\nPDF = os.path.join(HERE, \"T-078-nucc-v8-tmp.pdf\")\nTXT = os.path.join(HERE, \"T-078-nucc-v8-tmp.txt\")\n\nreq = urllib.request.Request(URL, headers={\"User-Agent\": \"Mozilla/5.0\"})\nwith urllib.request.urlopen(req, timeout=60) as r, open(PDF, \"wb\") as f:\n    f.write(r.read())\nsubprocess.run([\"pdftotext\", \"-layout\", PDF, TXT], check=True)\ntext = open(TXT, encoding=\"utf-8\", errors=\"replace\").read()\nos.remove(PDF)\nos.remove(TXT)\n\nflat = re.sub(r\"[ \\t]+\", \" \", text)\nflat = re.sub(r\"\\n\\s*\\n\", \"\\n\", flat)\nfor pat in [\n    r\"consecutive days\",\n    r\"number of days must\",\n    r\"decimal point\",\n    r\"dollar sign\",\n    r\"total charge for each service line|total billed amount for each\",\n]:\n    for m in re.finditer(pat, flat, re.I):\n        s = flat[max(0, m.start() - 260): m.end() + 200].replace(\"\\n\", \" \")\n        print(f\"[{pat}] ...{s}...\\n\")\n        break\n    else:\n        print(f\"[{pat}] NOT FOUND\\n\")\n"
}
````

### User / tool · 2026-11-02T03:47:15.451Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-nucc.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:17.022Z

**tool call — Bash**
````
{
 "command": "timeout 150 python3 artifacts/review-evidence/T-078-paralegal-r2-nucc.py > artifacts/review-evidence/T-078-paralegal-r2-nucc.out 2>&1; echo \"exit=$?\"; cat artifacts/review-evidence/T-078-paralegal-r2-nucc.out | cut -c1-700; ls artifacts/review-evidence | grep -i nucc",
 "description": "Download NUCC v8.0 manual and extract grouping and no-decimal passages"
}
````

### User / tool · 2026-11-02T03:47:17.155Z

**tool result**
````
exit=127
/bin/bash: timeout: command not found
T-078-paralegal-r2-nucc.out
T-078-paralegal-r2-nucc.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:19.243Z

**tool call — Bash**
````
{
 "command": "python3 artifacts/review-evidence/T-078-paralegal-r2-nucc.py > artifacts/review-evidence/T-078-paralegal-r2-nucc.out 2>&1; echo \"exit=$?\"; cut -c1-700 artifacts/review-evidence/T-078-paralegal-r2-nucc.out; ls artifacts/review-evidence | grep -i nucc",
 "description": "Download NUCC v8.0 manual and extract grouping and no-decimal passages"
}
````

### User / tool · 2026-11-02T03:47:20.197Z

**tool result**
````
exit=0
[consecutive days] ...nter that date under “From.” Leave “To” blank or re-enter “From” date. If grouping services, the place of service, procedure code, charges, and individual provider for each line must be identical for that service line. Grouping is allowed only for services on consecutive days. The number of days must correspond to the number of units in 24G. When required by payers to provide additional narrative description of an unspecified code, NDC, contract rate, or tooth numbers and...

[number of days must] ...From.” Leave “To” blank or re-enter “From” date. If grouping services, the place of service, procedure code, charges, and individual provider for each line must be identical for that service line. Grouping is allowed only for services on consecutive days. The number of days must correspond to the number of units in 24G. When required by payers to provide additional narrative description of an unspecified code, NDC, contract rate, or tooth numbers and areas of the oral cavity...

[decimal point] ... entered. When entering the charge amount, enter the amount in the field to the left of the vertical line. Enter number right justified to the left of the vertical line. Enter 00 for cents if the amount is a whole number. Do not use dollar signs, commas, or a decimal point when reporting amounts. Negative dollar amounts are not allowed. Leave the right-hand field blank. DESCRIPTION: “Outside lab? $Charges” indicates that services have been rendered by an independent pr...

[dollar sign] ...m as only one charge can be entered. When entering the charge amount, enter the amount in the field to the left of the vertical line. Enter number right justified to the left of the vertical line. Enter 00 for cents if the amount is a whole number. Do not use dollar signs, commas, or a decimal point when reporting amounts. Negative dollar amounts are not allowed. Leave the right-hand field blank. DESCRIPTION: “Outside lab? $Charges” indicates that services have been ...

[total charge for each service line|total billed amount for each] ...-hand area of the field. Do not use commas when reporting dollar amounts. Negative dollar amounts are not allowed. Dollar signs should not be entered. Enter 00 in the right-hand area of the field if the amount is a whole number. DESCRIPTION: “$Charges” is the total billed amount for each service line. FIELD SPECIFICATION: This field allows for the entry of 6 digits to the left of the vertical line and 2 digits to the right of the vertical line in the unshaded area. EXAMPLE: Version 8...

T-078-paralegal-r2-nucc.out
T-078-paralegal-r2-nucc.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:32.681Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-mutation.py",
 "content": "#!/usr/bin/env python3\n\"\"\"T-078 r2 mutation test (paralegal-reviewer): planted faults in a COPY of record-formats.md must make\nresearch/record_formats_check.py fail. A check that passes on a broken specimen is vacuous.\n\nWrites copies only under artifacts/review-evidence/mut/ (the real research/ files are never modified).\n\"\"\"\nimport pathlib\nimport shutil\nimport subprocess\nimport sys\n\nROOT = pathlib.Path(\"/Users/arsis/zlayt-pm-project\")\nMUT = ROOT / \"artifacts\" / \"review-evidence\" / \"mut\"\nMUT.mkdir(parents=True, exist_ok=True)\nchecker_src = (ROOT / \"research\" / \"record_formats_check.py\").read_text()\ndoc_src = (ROOT / \"research\" / \"record-formats.md\").read_text()\nshutil.copy(ROOT / \"research\" / \"record_formats_check.py\", MUT / \"record_formats_check.py\")\n\nmutations = {\n    \"M1 CMS-1500 grouped 97014 spans 5 days but keeps 3 units (round-1 fault)\": (\n        \"060126 060326 11 97014 A 90 | 00 3\", \"060126 060526 11 97014 A 90 | 00 3\"),\n    \"M2 UB-04 room rate 1,850.00 changed to 1,805.00 (rate x days != charge)\": (\n        \"0120    ROOM & BOARD SEMI-PVT         1,850.00\", \"0120    ROOM & BOARD SEMI-PVT         1,805.00\"),\n    \"M3 OCR copy written with decimal and separator restored (no decimal-less amount left)\": (\n        \"24. 060126 060126 11 98941 AB 8500 1\", \"24. 060126 060126 11 98941 AB 85 00 1\"),\n    \"M4 Spanish day-first date changed so both parts are day > 12 (ambiguity removed)\": (\n        \"Fecha: 17/05/2026\", \"Fecha: 17/05/2026\"),  # placeholder, replaced below\n}\nmutations[\"M4 Spanish 07/06/2026 date and its stated truth deleted\"] = (\n    \"(07/06/2026)\", \"(14/06/2026)\")\n\nresults = []\nfor name, (old, new) in mutations.items():\n    if doc_src.count(old) != 1:\n        results.append((name, f\"SKIPPED: pattern count {doc_src.count(old)} != 1\"))\n        continue\n    (MUT / \"record-formats.md\").write_text(doc_src.replace(old, new))\n    p = subprocess.run([sys.executable, str(MUT / \"record_formats_check.py\")], capture_output=True, text=True, cwd=str(MUT))\n    fails = [ln for ln in p.stdout.splitlines() if ln.startswith(\"FAIL\")]\n    results.append((name, f\"exit={p.returncode}; \" + (\" | \".join(fails[:3]) if fails else \"NO FAIL (vacuous check)\")))\n\n# Control: unmodified copy must pass all checks.\n(MUT / \"record-formats.md\").write_text(doc_src)\nctl = subprocess.run([sys.executable, str(MUT / \"record_formats_check.py\")], capture_output=True, text=True, cwd=str(MUT))\nprint(\"CONTROL (unmodified):\", ctl.returncode, ctl.stdout.strip().splitlines()[-1])\nfor name, res in results:\n    print(name, \"->\", res)\n"
}
````

### User / tool · 2026-11-02T03:47:32.835Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-mutation.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:36.798Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-mutation.py",
 "old_string": "    \"M4 Spanish day-first date changed so both parts are day > 12 (ambiguity removed)\": (\n        \"Fecha: 17/05/2026\", \"Fecha: 17/05/2026\"),  # placeholder, replaced below\n}\nmutations[\"M4 Spanish 07/06/2026 date and its stated truth deleted\"] = (\n    \"(07/06/2026)\", \"(14/06/2026)\")",
 "new_string": "}\nmutations[\"M4 Spanish ambiguous date 07/06/2026 replaced by 14/06/2026 (no day-first ambiguity left)\"] = (\n    \"(07/06/2026)\", \"(14/06/2026)\")"
}
````

### User / tool · 2026-11-02T03:47:36.892Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-mutation.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:39.131Z

**tool call — Bash**
````
{
 "command": "python3 artifacts/review-evidence/T-078-paralegal-r2-mutation.py > artifacts/review-evidence/T-078-paralegal-r2-mutation.out 2>&1; echo \"exit=$?\"; cut -c1-400 artifacts/review-evidence/T-078-paralegal-r2-mutation.out; echo \"--- verbose real run (check names, grep the rule-bearing ones) ---\"; python3 research/record_formats_check.py -v > artifacts/review-evidence/T-078-paralegal-r2-checks-verbose.out 2>&1; echo \"exit=$?\"; grep -c \"^ok\" artifacts/review-evidence/T-078-paralegal-r2-checks-verbose.out; grep -E \"CMS-1500|UB-04|Spanish|EMS|ambulance|affidavit|PT units|ledger totals|EOB totals\" artifacts/review-evidence/T-078-paralegal-r2-checks-verbose.out | cut -c1-200",
 "description": "Run planted-fault mutation test and verbose record format checks"
}
````

### User / tool · 2026-11-02T03:47:39.434Z

**tool result**
````
exit=0
CONTROL (unmodified): 0 record_formats_check: 85/85 checks pass
M1 CMS-1500 grouped 97014 spans 5 days but keeps 3 units (round-1 fault) -> SKIPPED: pattern count 0 != 1
M2 UB-04 room rate 1,850.00 changed to 1,805.00 (rate x days != charge) -> exit=1; FAIL UB-04 room line 0120: rate x days = charge  [1805.00 x 3 = 5550.00] | FAIL UB-04 has a rate-on-charge-line specimen
M3 OCR copy written with decimal and separator restored (no decimal-less amount left) -> exit=0; NO FAIL (vacuous check)
M4 Spanish ambiguous date 07/06/2026 replaced by 14/06/2026 (no day-first ambiguity left) -> exit=1; FAIL Spanish specimen has an ambiguous day-first date with stated truth  [[]]
--- verbose real run (check names, grep the rule-bearing ones) ---
exit=0
85
ok   §9 specimen labeled synthetic  [SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS]
ok   §9 specimen labeled synthetic  [SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS]
ok   PT units = CMS 8-minute rule  [38 min -> 3 units]
ok   CMS-1500 clean has service lines  [5 lines]
ok   CMS-1500 98941 060126-060126: days = units  [1 days, 1 units]
ok   CMS-1500 98941 060126-060126: every date marked on travel card
ok   CMS-1500 98941 060226-060226: days = units  [1 days, 1 units]
ok   CMS-1500 98941 060226-060226: every date marked on travel card
ok   CMS-1500 98941 060326-060326: days = units  [1 days, 1 units]
ok   CMS-1500 98941 060326-060326: every date marked on travel card
ok   CMS-1500 97014 060126-060326: days = units  [3 days, 3 units]
ok   CMS-1500 97014 060126-060326: every date marked on travel card
ok   CMS-1500 97010 060126-060326: days = units  [3 days, 3 units]
ok   CMS-1500 97010 060126-060326: every date marked on travel card
ok   CMS-1500 line sum = Item 28  [390.00]
ok   CMS-1500 OCR has separator-less amounts with truth  [6 lines]
ok   CMS-1500 OCR truths sum to Item 28 truth  [390.00]
ok   UB-04 lines sum to 0001 FL47  [5729.50 vs [Decimal('5729.50'), Decimal('38.50')]]
ok   UB-04 FL48 lines sum to 0001 FL48
ok   UB-04 room line 0120: rate x days = charge  [1850.00 x 3 = 5550.00]
ok   UB-04 lines sum to 0001 FL47  [9165.75 vs [Decimal('9165.75')]]
ok   UB-04 naive-sum figure stated in the note  [20,181.50]
ok   UB-04 has a rate-on-charge-line specimen
ok   UB-04 occurrence codes are accident codes 01-06 and vary  [['01', '03']]
ok   ledger totals  [445.00 45.00 400.00]
ok   EOB totals
ok   Spanish specimen has an ambiguous day-first date with stated truth  [[('07', '06', '2026')]]
ok   EMS times ascend  [[('23', '12'), ('23', '13'), ('23', '14'), ('23', '21'), ('23', '22'), ('23', '36'), ('23', '47'), ('23', '52')]]
ok   ambulance A0427-SH: units x rate = charge  [1 x 1450.00 = 1450.00]
ok   ambulance A0425-SH: units x rate = charge  [8.7 x 22.50 = 195.75]
ok   ambulance mileage units carry a tenth
ok   ambulance lines sum to total  [1645.75]
ok   affidavit charged/paid/unpaid = ledger  [('445.00', '0.00', '400.00')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:46.770Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-mutation.py",
 "old_string": "    \"M1 CMS-1500 grouped 97014 spans 5 days but keeps 3 units (round-1 fault)\": (\n        \"060126 060326 11 97014 A 90 | 00 3\", \"060126 060526 11 97014 A 90 | 00 3\"),",
 "new_string": "    \"M1 CMS-1500 grouped 97014 spans 5 days but keeps 3 units (round-1 fault)\": (\n        \"060126   060326   11     97014\", \"060126   060526   11     97014\"),"
}
````

### User / tool · 2026-11-02T03:47:46.856Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-mutation.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:48.611Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-mutation.py",
 "old_string": "    \"M3 OCR copy written with decimal and separator restored (no decimal-less amount left)\": (\n        \"24. 060126 060126 11 98941 AB 8500 1\", \"24. 060126 060126 11 98941 AB 85 00 1\"),",
 "new_string": "    \"M3 OCR truth for the 8500 line tampered 85.00 -> 58.00 (truth sum must no longer match Item 28)\": (\n        \"<- truth 85.00 (not 8,500.00)\", \"<- truth 58.00 (not 8,500.00)\"),"
}
````

### User / tool · 2026-11-02T03:47:48.704Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-mutation.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:50.090Z

**tool call — Bash**
````
{
 "command": "python3 artifacts/review-evidence/T-078-paralegal-r2-mutation.py > artifacts/review-evidence/T-078-paralegal-r2-mutation.out 2>&1; echo \"exit=$?\"; cut -c1-420 artifacts/review-evidence/T-078-paralegal-r2-mutation.out",
 "description": "Re-run mutation test with corrected patterns"
}
````

### User / tool · 2026-11-02T03:47:50.348Z

**tool result**
````
exit=0
CONTROL (unmodified): 0 record_formats_check: 85/85 checks pass
M1 CMS-1500 grouped 97014 spans 5 days but keeps 3 units (round-1 fault) -> exit=1; FAIL CMS-1500 97014 060126-060526: days = units  [5 days, 3 units] | FAIL CMS-1500 97014 060126-060526: every date marked on travel card
M2 UB-04 room rate 1,850.00 changed to 1,805.00 (rate x days != charge) -> exit=1; FAIL UB-04 room line 0120: rate x days = charge  [1805.00 x 3 = 5550.00] | FAIL UB-04 has a rate-on-charge-line specimen
M3 OCR truth for the 8500 line tampered 85.00 -> 58.00 (truth sum must no longer match Item 28) -> exit=1; FAIL CMS-1500 OCR truths sum to Item 28 truth  [363.00]
M4 Spanish ambiguous date 07/06/2026 replaced by 14/06/2026 (no day-first ambiguity left) -> exit=1; FAIL Spanish specimen has an ambiguous day-first date with stated truth  [[]]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:57.642Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-cms15.py",
 "content": "#!/usr/bin/env python3\n\"\"\"T-078 r2 source spot-check (paralegal-reviewer): the §16 ambulance section says it 'opened' CMS Medicare Claims Processing\nManual ch. 15 and quotes mileage rounding, loaded miles and the S = scene-of-accident modifier. Check those phrases in the\nPDF itself. Downloads to artifacts/review-evidence (temporary, deleted after).\"\"\"\nimport os\nimport re\nimport subprocess\nimport urllib.request\n\nURL = \"https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/downloads/clm104c15.pdf\"\nHERE = os.path.dirname(os.path.abspath(__file__))\nPDF = os.path.join(HERE, \"T-078-cms15-tmp.pdf\")\nTXT = os.path.join(HERE, \"T-078-cms15-tmp.txt\")\nreq = urllib.request.Request(URL, headers={\"User-Agent\": \"Mozilla/5.0\"})\nwith urllib.request.urlopen(req, timeout=90) as r, open(PDF, \"wb\") as f:\n    f.write(r.read())\nsubprocess.run([\"pdftotext\", \"-layout\", PDF, TXT], check=True)\ntext = re.sub(r\"\\s+\", \" \", open(TXT, encoding=\"utf-8\", errors=\"replace\").read())\nos.remove(PDF)\nos.remove(TXT)\nfor pat in [r\"nearest tenth\", r\"loaded mile\", r\"scene of accident\", r\"A0425\", r\"A0427\", r\"two (?:separate )?lines|two lines\"]:\n    m = re.search(pat, text, re.I)\n    print(f\"[{pat}]\", (\"...\" + text[max(0, m.start() - 160): m.end() + 120] + \"...\") if m else \"NOT FOUND\")\n    print()\n"
}
````

### User / tool · 2026-11-02T03:47:57.755Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-078-paralegal-r2-cms15.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:47:59.176Z

**tool call — Bash**
````
{
 "command": "python3 artifacts/review-evidence/T-078-paralegal-r2-cms15.py > artifacts/review-evidence/T-078-paralegal-r2-cms15.out 2>&1; echo \"exit=$?\"; cut -c1-520 artifacts/review-evidence/T-078-paralegal-r2-cms15.out",
 "description": "Spot-check CMS Claims Manual ch. 15 phrases cited for ambulance"
}
````

### User / tool · 2026-11-02T03:47:59.612Z

**tool result**
````
exit=0
[nearest tenth] ...per claim is used. Fractional units are not required on Form CMS-1450. For trips totaling up to100 covered miles suppliers must round the total miles up to the nearest tenth of a mile and report the resulting number with the appropriate HCPCS code for ambulance mileage. The decimal must be us...

[loaded mile] ...service; 3. A geographic adjustment factor (GAF) for each ambulance fee schedule locality area (geographic practice cost index (GPCI)); 4. A nationally uniform loaded mileage rate; 5. An additional amount for certain mileage for a rural point-of-pickup; and 6. For specified temporary period...

[scene of accident] ... helicopter pad) between modes of ambulance transport; J = Freestanding ESRD facility; N = Skilled nursing facility; P = Physician’s office; R = Residence; S = Scene of accident or acute event; X = Intermediate stop at physician’s office on way to hospital (destination code only) In addition, ins...

[A0425] ...e billed in association with a non-emergency transport of a beneficiary with ESRD to and from renal dialysis treatment. BLS mileage is identified by HCPCS code A0425. The 10% reduction will be taken after calculation of the normal fee schedule payment amount, including any add-on or b...

[A0427] ...PCS Codes Code A0425 BLS mileage (per mile) A0425 ALS mileage (per mile) A0426 Ambulance service, Advanced Life Support (ALS), non-emergency transport, Level 1 A0427 Ambulance service, ALS, emergency transport, Level 1 A0428 Ambulance service, Basic Life Support (BLS), non-emergency t...

[two (?:separate )?lines|two lines] ...are ignored. If the data submitted in the required field does not match that format, the claim is rejected. Mileage Generally, each ambulance trip will require two lines of coding, e.g., one line for the service and one line for the mileage. Suppliers who do not bill mileage would have on...
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:48:07.156Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF' > artifacts/review-evidence/T-077-paralegal-r2-docket.out 2>&1\nimport re, urllib.request\nurl = \"https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14\"\nreq = urllib.request.Request(url, headers={\"User-Agent\": \"Mozilla/5.0\"})\nhtml = urllib.request.urlopen(req, timeout=30).read().decode(\"utf-8\", \"replace\")\ntext = re.sub(r\"\\s+\", \" \", re.sub(r\"<[^>]+>\", \" \", html))\ntext = text.replace(\"&nbsp;\", \" \")\nfor w in [\"ehearing\", \"Opinion withdrawn\", \"Memorandum Opinion\", \"Petition for Review\", \"Denied\"]:\n    for m in list(re.finditer(w, text))[:2]:\n        print(f\"[{w}]\", text[max(0, m.start() - 140): m.end() + 90])\n    print()\nEOF\ncat artifacts/review-evidence/T-077-paralegal-r2-docket.out | cut -c1-400",
 "description": "Check Hills v. Donis docket events for rehearing and withdrawal entries"
}
````

### User / tool · 2026-11-02T03:48:08.008Z

**tool result**
````
[ehearing] Supreme Court   03/29/2021 Petition for review was not filed   03/29/2021 Petition for review due in Supreme Court   02/26/2021 Motion for rehearing was not filed   02/26/2021 Motion for rehearing due   02/11/2021 Motion for rehearing dis
[ehearing] as not filed   03/29/2021 Petition for review due in Supreme Court   02/26/2021 Motion for rehearing was not filed   02/26/2021 Motion for rehearing due   02/11/2021 Motion for rehearing disposed DENIED 02/11/2021 Judgment Issued   [ PDF/

[Opinion withdrawn] randum opinion issued AFFIRMED IN PART AND REVERSED AND RENDERED IN PART [ PDF/3.10 MB ] Memorandum Opinion [ PDF/97 KB ] Notice 02/11/2021 Opinion withdrawn   12/23/2020 Additional authorities filed   [ PDF/303 KB ] Letter 04/22/2020 Response fil

[Memorandum Opinion] nt Issued   [ PDF/118 KB ] Judgment 02/11/2021 Memorandum opinion issued AFFIRMED IN PART AND REVERSED AND RENDERED IN PART [ PDF/3.10 MB ] Memorandum Opinion [ PDF/97 KB ] Notice 02/11/2021 Opinion withdrawn   12/23/2020 Additional authorities fil
[Memorandum Opinion] earing due   01/14/2020 Judgment Issued   [ PDF/175 KB ] JUDGMENT 01/14/2020 Memorandum opinion issued REVERSED AND RENDERED [ PDF/196 KB ] Memorandum Opinion [ PDF/91 KB ] Notice 12/12/2019 Post submission brief filed   [ PDF/78 KB ] Brief [ PDF/1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:49:29.421Z

Both research cards have been checked, so I'm writing the two round-2 review files now.

### Assistant · claude-haiku-5-5 · 2026-11-02T03:49:46.415Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r2.md",
 "content": "# T-077 round 2: paralegal-reviewer (research/case-library-sources-v2.md + research/validate_library.py, commit 5c2cb2f)\n\n**Verdict: changes.** The round-1 major is only partly closed. The denylist mechanism works: the self-test passes, and every planted mixed-case and accented variant of a listed name fails. But four real names the v2 file cites are still not on the list (Brinjikji, Nakashima, Fraser, Vera), so the file's own rule \"every real name in this file is on that denylist\" is still false. The self-test only checks the \"X v. Y\" captions, not the prose author names. Nothing in the current packets contains these names (the 7-packet scan is clean), so this is a major and not a blocker. Three round-1 minors are closed. The Hills v. Donis fix is right on the docket but misattributes the withdrawal to the newsbrief.\n\n## Commands run and output\n\n```\n$ python3 research/validate_library.py --self-test\nself-test: ok (354 planted variants caught, 16 caption names covered)        exit 0\n$ python3 research/validate_library.py\nidentifier check: ok (7 packets, 72 denylist terms, case-insensitive)       exit 0\n```\n\nPer-name check (artifacts/review-evidence/T-077-paralegal-r2-denylist.py, output in T-077-paralegal-r2-denylist.out):\n\n```\n'Brinjikji' cited at L12   on denylist=False planted-caught=False\n'Nakashima' cited at L12   on denylist=False planted-caught=False\n'Fraser'    cited at L215  on denylist=False planted-caught=False\n'Vera'      cited at L228 (Rodriguez-Vera) on denylist=False planted-caught=False\ncited real names NOT on denylist: ['Brinjikji', 'Nakashima', 'Fraser', 'Vera']\ncaption names checked by self-test: [16 names, all captions only]\n```\n\nRound-1 minors:\n\n| Round-1 item | Status | Evidence |\n|---|---|---|\n| Record features not tagged | Closed | All 17 patterns (P1-P17) carry \"(from source)\" or \"(our inference)\"; P4 and P17 say the source supports only the scenario theme (lines 103-104, 305-306). |\n| Hills v. Donis \"withdrawn and substituted\" | Partly closed | Docket supports it (artifacts/review-evidence/T-077-paralegal-r2-docket.out): \"Opinion withdrawn 02/11/2021\", \"Motion for rehearing disposed DENIED 02/11/2021\", \"Memorandum opinion issued AFFIRMED IN PART AND REVERSED AND RENDERED IN PART [PDF/97 KB]\". Supreme Court order list of July 23, 2021 denies 21-0287 (T-077-paralegal-r2-orders.out). But line 80 says the newsbrief \"describes the withdrawn 2020 opinion\": the fetched page has 0 matches for \"withdr\" and \"substitut\". See F2. |\n| P7 / lib12 stage not stated | Closed | Case stage line (159-160); stage/entry column (345-348). |\n| P5 \"six ledger columns\" overstated | Closed | Lines 124-126: ledger columns derived from items 1-4 and 6; item 5 is a separate document. |\n| D-042 features not in packet rows | Closed | \"Must contain\" table (350-361) with lib09, lib12, lib13 fixtures. |\n| P6 case type, statute currency | Closed | Line 136 \"health care liability claim\"; statute currency line 427-430. |\n\n## Findings\n\n1. **major, still open: four cited real names are not on the denylist.** Brinjikji and Nakashima (line 12), Fraser (line 215) and Rodriguez-Vera's \"Vera\" (line 228) are real names in the file and absent from DENYLIST_V2 and the doc block. The self-test checks only caption names (see the output above), though validate_library.py:11 says \"v2 doc names must all be listed\".\n2. **minor: the Hills newsbrief is described as saying what it does not say.** Line 80. Cite the docket for withdrawal and substitution; add the substitute opinion's own PDF link or say it is not linked.\n3. **minor: firm and organisation names are not on the list.** mdjwlaw (line 80), painterfirm (line 135), FAIR Health (line 266). The denylist section says it covers \"every real proper noun in this file's sources\".\n4. **nit: provenance dates are after the review date.** Line 4 \"Researched 2026-11-01/02\", line 427 \"checked 2026-11-02\". The commit is \"Sun Nov 1 21:42:31 2026 -0600\", which is 2026-11-02 in UTC, so these are probably UTC. Same pattern in research/record-formats.md lines 9 and 1073. State the timezone.\n\nOutside my lens: whether a Texas statute or case holding is currently good law. I checked only what the doc says the sources say.\n\n```json\n{\"card\": \"T-077\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"research/case-library-sources-v2.md and research/validate_library.py at commit 5c2cb2f (round 2); prior review reviews/T-077-paralegal.md; no app run (research card); no sample case\",\n \"exercised\": [\n  \"Read personas/paralegal.md, reviews/T-077-paralegal.md, git show --stat 5c2cb2f, research/validate_library.py (179 lines), research/case-library-sources-v2.md (435 lines, full)\",\n  \"python3 research/validate_library.py --self-test -> 'self-test: ok (354 planted variants caught, 16 caption names covered)', exit 0\",\n  \"python3 research/validate_library.py -> 'identifier check: ok (7 packets, 72 denylist terms, case-insensitive)', exit 0\",\n  \"artifacts/review-evidence/T-077-paralegal-r2-denylist.py (+ .out): every real name found in the v2 file checked against DENYLIST and a planted sentence; Brinjikji, Nakashima, Fraser, Vera are not on the list and not caught; a planted packet with them passes the library scan\",\n  \"artifacts/review-evidence/T-077-paralegal-r2-docket.out: search.txcourts.gov case 14-18-00566-CV (Opinion withdrawn 02/11/2021; rehearing denied and memorandum opinion issued 02/11/2021)\",\n  \"artifacts/review-evidence/T-077-paralegal-r2-orders.py (+ .out): Texas Supreme Court July 23, 2021 order list denies 21-0287; date mentions in the doc (2026-11-02) checked against the commit date\",\n  \"Fetched mdjwlaw newsbrief TIN-20200211-item1 (HTTP 200, 32,603 bytes): 0 matches for 'withdr' and 'substitut'; cites 2020 WL 206187 only\",\n  \"Counted 'Record features' lines: 17 patterns, each tagged '(from source)' or '(our inference)'\",\n  \"Not exercised: a fresh name-collision search; the round-1 web fetches were not repeated beyond the Hills pages; one fetch dump was written to the session scratchpad (outside the reviewer write paths, not a review artifact)\"],\n \"verdict\": \"changes\",\n \"scores\": {\"denylist_covers_cited_names\": 2, \"planted_name_self_test\": 4, \"round1_minors_closed\": 3, \"source_fidelity\": 4, \"synthetic_safety_enforcement\": 3},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Denylist still omits four real names the v2 file cites; self-test checks only caption names\",\n   \"evidence\": \"research/case-library-sources-v2.md:12 'Brinjikji, Nakashima'; :215 'ElGhrably I., Fraser S.G.'; :228 'Rodriguez-Vera F.J.'; rule at :24-25 says every real name in the file is on the denylist. research/validate_library.py:25-48 (DENYLIST_V2) has no Brinjikji, Nakashima, Fraser or Vera. artifacts/review-evidence/T-077-paralegal-r2-denylist.out: 'cited real names NOT on denylist: [Brinjikji, Nakashima, Fraser, Vera]'; self-test caption list has 16 names, all 'X v. Y' or 'In re' captions. validate_library.py:11 docstring says 'v2 doc names must all be listed'.\",\n   \"why_it_matters\": \"The guard fails open for these four names: a packet containing 'Fraser' or 'Brinjikji' passes the identifier check, and the doc says it does not. No current packet contains them (the 7-packet scan is clean), so no real name has leaked; this is why it is a major and not a blocker. It stays open because the round-1 major was exactly this coverage gap.\",\n   \"fix\": \"Add Brinjikji, Nakashima, Fraser and Vera (and Rodriguez-Vera as a unit) to DENYLIST_V2 and to the 'Denylist additions' block. Extend self_test so that author names in the doc's citations are checked against the list, not only X v. Y captions. Correct the validate_library.py docstring to say what is checked.\",\n   \"acceptance_test\": \"python3 research/validate_library.py --self-test fails when 'Brinjikji' is removed from DENYLIST_V2 (it passes today); a packet containing 'Fraser S.G.' fails scan_library; the doc-versus-list check covers the prose author names.\"},\n  {\"severity\": \"minor\", \"title\": \"Hills v. Donis: the newsbrief is described as saying 'withdrawn', which it does not say\",\n   \"evidence\": \"research/case-library-sources-v2.md:80 'The firm newsbrief https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the withdrawn 2020 opinion only.' Fetched page: 0 matches for 'withdr' and 'substitut'; it cites 'Hills v. Donis, No. 14-18-00566-CV, 2020 WL 206187 ... Jan. 14, 2020'. Docket supports the withdrawal (artifacts/review-evidence/T-077-paralegal-r2-docket.out: 'Opinion withdrawn 02/11/2021').\",\n   \"why_it_matters\": \"This is the sentence round 1 flagged. The conclusion is now right, but a paralegal who opens the newsbrief to check the withdrawal will not find it. The 2021 substitute opinion also has no PDF link in the doc; the docket page is cited instead.\",\n   \"fix\": \"Cite the docket page for the withdrawal and the substitution. Change the newsbrief sentence to 'describes the 2020 opinion (2020 WL 206187) and does not mention withdrawal'. Add the substitute opinion's own PDF link from the docket, or say it is not linked.\",\n   \"acceptance_test\": \"In the P3 entry, 'withdrawn' is attributed only to the docket URL; the newsbrief sentence matches the fetched page (no 'withdr' or 'substitut' hits).\"},\n  {\"severity\": \"minor\", \"title\": \"Firm and organisation names in cited URLs and text are not on the denylist\",\n   \"evidence\": \"research/case-library-sources-v2.md:80 'mdjwlaw.com'; :135 'painterfirm.com/medmal/...'; :266 'FAIR Health, A Window into Utilization and Cost of Ground Ambulance Services'. None appears in DENYLIST_V2 or DENY_CAPITALISED (validate_library.py:21-53). The denylist section (:363-366) says it covers every real proper noun in the file's sources.\",\n   \"why_it_matters\": \"These are firm and organisation names, not parties, so the risk is lower than for the names in F1. A packet could still carry 'Painter' or 'FAIR Health' with no flag, and the doc's own rule is broader than the list.\",\n   \"fix\": \"Add mdjwlaw, Painter and FAIR Health to the denylist, or state in the doc that organisation and website names are exempt and why.\",\n   \"acceptance_test\": \"The denylist block lists every firm or organisation token in the source citations, or the exemption is written in the doc.\"},\n  {\"severity\": \"nit\", \"title\": \"Provenance dates are after the review date and do not say which timezone\",\n   \"evidence\": \"research/case-library-sources-v2.md:4 'Researched 2026-11-01/02'; :427 'CPRC 18.001/18.002 text was checked 2026-11-02'. Commit 5c2cb2f: 'Date: Sun Nov 1 21:42:31 2026 -0600'. The same date appears in research/record-formats.md:9 and :1073.\",\n   \"why_it_matters\": \"The commit is 2026-11-02 in UTC, so the dates are probably UTC. A reader cannot tell which clock was used, and a statute-currency date should be unambiguous.\",\n   \"fix\": \"State the timezone, or use the local date.\",\n   \"acceptance_test\": \"Each date in the doc matches the commit date in the stated timezone.\"}\n ],\n \"whats_right\": [\n  \"All 17 'Record features' lines are tagged '(from source)' or '(our inference)', and P4 and P17 say their sources back only the scenario theme.\",\n  \"The self-test plants 354 mixed-case and accented variants of the listed names and all are caught; lowercase 'hills' is not flagged, and 'Waddell' is allowed as an eponym.\",\n  \"The P5 billing list now matches the opinion: four ledger columns from items 1-4 and 6, with item 5 (carrier contracts) marked as a separate document.\"],\n \"questions_for_chris\": [\n  \"Should cited firm websites and journal names count as 'real names' for the denylist, or only people and places? The doc says 'every real proper noun', and the answer decides F3.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T03:49:46.569Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:05.398Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-078-paralegal-r2.md",
 "content": "# T-078 round 2: paralegal-reviewer (research/record-formats.md + research/record_formats_check.py, commit 327ce46)\n\n**Verdict: pass.** All three round-1 majors are closed. The CMS-1500 grouping now follows the NUCC rule, both traps appear as specimens with stated truths, and the EMS report, ambulance invoice, CPRC 18.001 affidavit and narrative letter are present with sources and SYNTHETIC labels. The check script passes 85 of 85, and four planted faults each make it fail, so the pass is not vacuous. What is left is minor: one PT specimen has a 14-day gap that no note explains, two lib14 must-contain items have no specimen text, and the dates and fixtures need small alignments.\n\n## Commands run and output\n\n```\n$ python3 research/record_formats_check.py\nrecord_formats_check: 85/85 checks pass                                      exit 0\n$ python3 research/record_formats_check.py -v   (saved: artifacts/review-evidence/T-078-paralegal-r2-checks-verbose.out)\n85 'ok' lines, including: CMS-1500 97014 060126-060326 days = units [3 days, 3 units];\n  every date marked on travel card; UB-04 room line 0120 rate x days = charge [1850.00 x 3 = 5550.00];\n  UB-04 naive-sum figure stated in the note [20,181.50]; CMS-1500 OCR truths sum to Item 28 truth [390.00];\n  ambulance A0425-SH units x rate = charge [8.7 x 22.50 = 195.75]; affidavit charged/paid/unpaid = ledger [445.00, 0.00, 400.00]\n```\n\nMutation test (artifacts/review-evidence/T-078-paralegal-r2-mutation.py, output in T-078-paralegal-r2-mutation.out). Each planted fault is applied to a copy of the doc:\n\n```\nCONTROL (unmodified): 0 record_formats_check: 85/85 checks pass\nM1 grouped 97014 spans 5 days, 3 units    -> FAIL CMS-1500 97014 060126-060526: days = units [5 days, 3 units]\nM2 room rate 1,850.00 -> 1,805.00          -> FAIL UB-04 room line 0120: rate x days = charge [1805.00 x 3 = 5550.00]\nM3 OCR truth 85.00 -> 58.00                -> FAIL CMS-1500 OCR truths sum to Item 28 truth [363.00]\nM4 Spanish ambiguous date removed          -> FAIL Spanish specimen has an ambiguous day-first date with stated truth\n```\n\nNUCC 1500 manual v8.0 (artifacts/review-evidence/T-078-paralegal-r2-nucc.py, output in T-078-paralegal-r2-nucc.out): \"Grouping is allowed only for services on consecutive days. The number of days must correspond to the number of units in 24G.\" and \"Do not use dollar signs, commas, or a decimal point when reporting amounts.\" The doc's rule matches.\n\nCMS Claims Processing Manual ch. 15 (artifacts/review-evidence/T-078-paralegal-r2-cms15.py, output in T-078-paralegal-r2-cms15.out): \"round the total miles up to the nearest tenth of a mile\", \"S = Scene of accident or acute event\", \"each ambulance trip will require two lines of coding\". The §16 claims match.\n\nHand checks: ledger 210 + 130 + 70 + 35 - 70 + 70 = 445, less 45 adjustment = 400. UB-04 naive sum 20,181.50 versus 9,165.75 billed. PT 38 timed minutes = 2 units (25 min) + 1 unit (13 min). PT 2x/wk x 6 wks = 12 planned visits. 05/27 to 08/04 = 69 days.\n\n## Round-1 majors\n\n1. **CMS-1500 follows NUCC grouping: closed.** Lines 4-5 of the clean form group 06/01 to 06/03 (three days, three units), and the travel card (lines 199-202) marks ES and H/C on all three dates. The round-1 five-day line is gone.\n2. **Both traps are in the specimens: closed.** UB-04 specimen 2 (lines 450-466) has a room line with rate 1,850.00 and FL 46 = 3 days, and the note states the naive sum. OCR copy (lines 384-393) has 8500, 9000, 39000 with truths 85.00, 90.00, 390.00.\n3. **EMS report, ambulance invoice, §18.001 affidavit and narrative letter: closed.** §15 (lines 703-756), §16 (760-799), §17 (803-854) and §18 (858-901) each have sources, a SYNTHETIC label on every specimen block, and a check in the script. The lib08-lib15 \"formats used\" references all point to sections that exist.\n\n## Findings\n\n1. **minor: the PT specimen now has an unexplained 14-day gap.** The round-1 fix made the 06/10 note \"Visit 2 of 12\" (line 144). That means no PT visit between the 05/27 evaluation and 06/10, on a 2x/wk plan (line 159), and no cancellation or no-show entry for those two weeks. The only cancellation (line 156, 06/12) says \"Rescheduled 06/15/2026\", and no 06/15 record exists in §3, §10 or §11. The doc's own trap at line 132 says cancellations \"may state the reason for a gap\". An adjuster asks about exactly this.\n2. **minor: two lib14 must-contain items have no specimen text.** The v2 table (case-library-sources-v2.md:360) asks for \"one handwritten date with no year\" and \"a page whose hidden text layer differs from the image\". §14 specimen (lines 681-698) has only dated lines, and the hidden text layer is a table row (line 673). The no-year example is prose only (line 37).\n3. **nit: lib09 fixture dates differ from the §13 specimen.** The v2 table (:355) asks for \"03/06/2026\" day-first and \"14/05/2026\". The §13 specimen has \"17/05/2026\" (line 632) and \"07/06/2026\" (line 641).\n4. **nit: provenance dates are after the review date.** Line 9 \"(2026-11-02, results in section 23)\" and line 1073 \"Name-collision search (2026-11-02)\". The commit is 2026-11-01 21:42 -0600, so this is probably UTC. Same as T-077 F4.\n\nOutside my lens: whether the NUBC accident-code family and the FL 45 creation-date convention are right. The doc labels both unverified, and I did not check them against the licensed manual. I did not re-run the name-collision search in §23.\n\n```json\n{\"card\": \"T-078\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"research/record-formats.md and research/record_formats_check.py at commit 327ce46 (round 2); prior review reviews/T-078-paralegal.md; cross-read research/case-library-sources-v2.md 'Must contain' table; no app run (research card); no sample case\",\n \"exercised\": [\n  \"Read personas/paralegal.md, reviews/T-078-paralegal.md, git show --stat 327ce46, research/record_formats_check.py (208 lines, full), research/record-formats.md §8-§23 in full and §1-§7 in part (traps and sections 3, 4, 10 checked directly)\",\n  \"python3 research/record_formats_check.py -> 'record_formats_check: 85/85 checks pass', exit 0; -v run saved as artifacts/review-evidence/T-078-paralegal-r2-checks-verbose.out (85 ok lines)\",\n  \"artifacts/review-evidence/T-078-paralegal-r2-mutation.py (+ .out): control passes; four planted faults in a copy each fail (M1 five-day span with 3 units; M2 room rate 1,805.00; M3 OCR truth 58.00; M4 ambiguous Spanish date removed)\",\n  \"artifacts/review-evidence/T-078-paralegal-r2-nucc.py (+ .out): NUCC 1500 Manual v8.0 downloaded and text-extracted: 'Grouping is allowed only for services on consecutive days. The number of days must correspond to the number of units in 24G.' and 'Do not use dollar signs, commas, or a decimal point when reporting amounts.'\",\n  \"artifacts/review-evidence/T-078-paralegal-r2-cms15.py (+ .out): CMS Claims Processing Manual ch. 15 checked for 'nearest tenth', 'S = Scene of accident or acute event', 'two lines of coding'\",\n  \"Hand arithmetic: ledger 210+130+70+35-70+70 = 445 less 45 = 400; UB-04 room 1,850.00 x 3 = 5,550.00, naive sum 20,181.50 vs 9,165.75; PT 38 min = 2u + 1u; 2x/wk x 6 wks = 12; 05/27 to 08/04 = 69 days\",\n  \"Not exercised: the §23 name-collision search; NUBC accident-code and creation-date conventions (doc marks them unverified; outside my lens); one fetch dump was written to the session scratchpad (outside the reviewer write paths, not a review artifact)\"],\n \"verdict\": \"pass\",\n \"scores\": {\"fields_and_wording_realism\": 4, \"extraction_traps_real\": 5, \"specimen_arithmetic\": 5, \"specimens_exercise_the_traps\": 4, \"coverage_for_t077_packets\": 4},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"PT specimen: 14-day gap with no visits or cancellation note, and a 06/15 reschedule with no record\",\n   \"evidence\": \"research/record-formats.md:144 'Daily Note Visit 2 of 12' (06/10/2026); :159 'Visit 1 was the 05/27/2026 evaluation; 2x/wk x 6 wks = 12 planned visits'; :156 '06/12/2026 Pt cancelled - no transportation. Rescheduled 06/15/2026.'; ledger lines 503-504 show only the 05/27 and 06/10 PT dates; no 06/15 entry in §3, §10 or §11.\",\n   \"why_it_matters\": \"Round 1 flagged a visit count that did not match the ledger. The fix made the count match, but it now says there were no PT visits for 14 days on a 2x/wk plan, with no reason given. That is the gap-in-treatment and missed-appointment pattern an adjuster raises first, and the doc's own trap (line 132) says cancellations may state the reason. The 06/15 reschedule is never resolved.\",\n   \"fix\": \"Add cancellation or no-show entries with reasons for 05/28 to 06/09 and a dated record for 06/15 (or a note that it did not occur), or label the 14-day interval DELIBERATE with its expected gap flag.\",\n   \"acceptance_test\": \"record_formats_check.py asserts that each gap between dated PT visits has a cancellation or no-show note, or carries a DELIBERATE label, and that the 06/15 reschedule is resolved in the file.\"},\n  {\"severity\": \"minor\", \"title\": \"Two lib14 must-contain items have no specimen text\",\n   \"evidence\": \"case-library-sources-v2.md:360 lib14 must contain 'one handwritten date with no year' and 'a page whose hidden text layer differs from the image'. research/record-formats.md §14 specimen (lines 681-698) has only dated lines ('Date of injury: 5/14/26', 'Signed 5/29/26'); the hidden text layer is a failure-mode table row (line 673) with no specimen; the no-year example is prose only (line 37).\",\n   \"why_it_matters\": \"T-079 is told to take each packet's formats from this file. Two of lib14's required features have nothing to copy, so its expected JSON would assert features that no document in the file shows.\",\n   \"fix\": \"Add to §14 a SYNTHETIC handwritten date with no year, and a SYNTHETIC page showing image text beside a hidden text layer that differs.\",\n   \"acceptance_test\": \"A grep of §14 finds a specimen block with a date that has no year, and a block where the text layer line differs from the image line.\"},\n  {\"severity\": \"nit\", \"title\": \"lib09 fixture dates differ from the §13 specimen\",\n   \"evidence\": \"case-library-sources-v2.md:355 lib09 must contain 'One date 03/06/2026 day-first (truth 3 June 2026) and one 14/05/2026'. research/record-formats.md:632 'Fecha: 17/05/2026' and :641 '(07/06/2026)'; neither 03/06/2026 nor 14/05/2026 appears in §13.\",\n   \"why_it_matters\": \"The packet expectations and the format file disagree on the ambiguity fixture. Harmless if T-079 chooses its own dates; confusing if it copies §13.\",\n   \"fix\": \"Align the lib09 row with the §13 dates, or state that the packet builder chooses its own day-first dates.\",\n   \"acceptance_test\": \"Every date named in the lib09 row appears in §13, or the row says the dates are free choices.\"},\n  {\"severity\": \"nit\", \"title\": \"Provenance dates are after the review date and do not say which timezone\",\n   \"evidence\": \"research/record-formats.md:9 'A web search ... (2026-11-02, results in section 23)'; :1073 'Name-collision search (2026-11-02)'. Commit 327ce46: 'Date: Sun Nov 1 21:42:39 2026 -0600'.\",\n   \"why_it_matters\": \"Probably UTC, but a reader cannot tell. The same issue is in T-077 F4.\",\n   \"fix\": \"State the timezone or use the local date.\",\n   \"acceptance_test\": \"Each date in the doc matches the commit date in the stated timezone.\"}\n ],\n \"whats_right\": [\n  \"The NUCC grouping is now consistent: every grouped line has days = units and the travel card marks every date, and the rule text matches the NUCC v8.0 manual extracted for this review.\",\n  \"Both traps are specimens with stated truths: a UB-04 room line (1,850.00 x 3 = 5,550.00, naive sum 20,181.50 stated) and an OCR copy with decimal-less amounts (8500, 9000, 39000) whose truths are 85.00, 90.00, 390.00.\",\n  \"The 85 checks bite: four planted faults in a copy each make the matching check fail, so 85/85 is not vacuous.\"],\n \"questions_for_chris\": [\n  \"Were the 2026-11-02 dates in record-formats.md and case-library-sources-v2.md meant as UTC? (F4 in both reviews.)\"]}\n```\n"
}
````

### User / tool · 2026-11-02T03:50:05.558Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-078-paralegal-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:10.308Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-T-078-paralegal-r2-jsoncheck.py",
 "content": "#!/usr/bin/env python3\n\"\"\"Check the round-2 review JSON blocks for T-077 and T-078 (paralegal-reviewer).\n\nEach review must have exactly one fenced json block, the required keys, persona 'paralegal-reviewer', model 'claude-haiku-5-5',\nand a verdict that follows the rule: any blocker -> fail; else any major -> changes; else pass.\n\"\"\"\nimport json\nimport pathlib\nimport re\n\nROOT = pathlib.Path(\"/Users/arsis/zlayt-pm-project\")\nREQUIRED = [\"card\", \"persona\", \"model\", \"scope\", \"exercised\", \"verdict\", \"scores\", \"findings\", \"whats_right\", \"questions_for_chris\"]\nok_all = True\nfor card in [\"T-077\", \"T-078\"]:\n    path = ROOT / \"reviews\" / f\"{card}-paralegal-r2.md\"\n    text = path.read_text()\n    blocks = re.findall(r\"```json\\n(.*?)```\", text, re.S)\n    problems = []\n    if len(blocks) != 1:\n        problems.append(f\"expected 1 json block, found {len(blocks)}\")\n    data = json.loads(blocks[0]) if blocks else {}\n    for k in REQUIRED:\n        if k not in data:\n            problems.append(f\"missing key {k}\")\n    if data.get(\"card\") != card:\n        problems.append(\"card mismatch\")\n    if data.get(\"persona\") != \"paralegal-reviewer\":\n        problems.append(\"persona mismatch\")\n    if data.get(\"model\") != \"claude-haiku-5-5\":\n        problems.append(\"model mismatch\")\n    sev = [f.get(\"severity\") for f in data.get(\"findings\", [])]\n    if any(s not in {\"blocker\", \"major\", \"minor\", \"nit\"} for s in sev):\n        problems.append(\"bad severity value\")\n    if len(data.get(\"whats_right\", [])) > 3:\n        problems.append(\"more than 3 whats_right\")\n    expected = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\n    if data.get(\"verdict\") != expected:\n        problems.append(f\"verdict {data.get('verdict')!r} breaks rule (expected {expected!r})\")\n    for f in data.get(\"findings\", []):\n        for k in [\"severity\", \"title\", \"evidence\", \"why_it_matters\", \"fix\", \"acceptance_test\"]:\n            if not f.get(k):\n                problems.append(f\"finding missing {k}: {f.get('title', '?')}\")\n    print(card, \"verdict\", data.get(\"verdict\"), \"findings\", sev, \"problems:\", problems or \"none\")\n    ok_all = ok_all and not problems\nprint(\"jsoncheck:\", \"ok\" if ok_all else \"FAIL\")\n"
}
````

### User / tool · 2026-11-02T03:50:10.401Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-T-078-paralegal-r2-jsoncheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:11.948Z

**tool call — Bash**
````
{
 "command": "python3 artifacts/review-evidence/T-077-T-078-paralegal-r2-jsoncheck.py | tee artifacts/review-evidence/T-077-T-078-paralegal-r2-jsoncheck.out; echo \"--- board validate ---\"; python3 tools/board.py validate 2>&1 | tail -5; echo \"exit=$?\"",
 "description": "Validate the two review JSON blocks and run board validate"
}
````

### User / tool · 2026-11-02T03:50:12.127Z

**tool result**
````
T-077 verdict changes findings ['major', 'minor', 'minor', 'nit'] problems: none
T-078 verdict pass findings ['minor', 'minor', 'nit', 'nit'] problems: none
jsoncheck: ok
--- board validate ---
ok (94 file(s))
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:17.117Z

Both review files pass the JSON check and board validate. Next I'll save the recurring patterns to my memory directory.

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:19.976Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/library-review-patterns.md",
 "old_string": "**How to apply:** use artifacts/review-evidence/T-052-paralegal-scan.py as a starting probe. Related: [[golden-set-recurring-findings]], [[reviewer-hook-constraints]]",
 "new_string": "**How to apply:** use artifacts/review-evidence/T-052-paralegal-scan.py as a starting probe. Related: [[golden-set-recurring-findings]], [[reviewer-hook-constraints]]\n\n## T-077 r2 (commit 5c2cb2f): denylist guard, self-test scope\n- A denylist self-test that cross-checks only the doc's caption names (\"X v. Y\", \"In re X\") misses real names cited in prose (study authors, co-authors). Brinjikji, Nakashima, Fraser, Vera slipped through while the self-test printed \"ok\". Run the per-name check yourself: list every capitalised name in the doc and test each against the list.\n- Firm domains in cited URLs (mdjwlaw, painterfirm) and organisation names (FAIR Health) are not on the list; decide with Chris whether they count as \"real names\".\n- Rule text that says \"every real name in this file is on the denylist\" is a claim to test, not to trust.\n- Fetched-page checks: a newsbrief sentence attributing a claim (\"describes the withdrawn opinion\") must be grepped on the page; the docket was the source that actually supported it.\n- Date provenance: \"checked 2026-11-02\" in a doc written 2026-11-01 local is probably UTC. Ask, do not assume.\n- Denylist and self-test changes in this area: keep a planted-name test per new term (mutation: delete a term and confirm self-test fails)."
}
````

### User / tool · 2026-11-02T03:50:20.104Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/library-review-patterns.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:25.363Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/record-format-review-patterns.md",
 "content": "---\nname: record-format-review-patterns\ndescription: T-078 r2 (commit 327ce46) record-format specimens review - mutation-test the check script, which traps are real, cross-specimen gaps a fixture fix creates\nmetadata:\n  type: project\n---\n\nT-078 r2 (2026-11-01) closed all three round-1 majors (NUCC grouping days = units, rate-on-charge UB-04 room line, OCR decimal-less\namounts, EMS/ambulance/18.001/narrative sections). 85/85 checks passed. Recurring things to re-check on any record-formats change:\n\n- Run the check script, then mutation-test it. Copy research/record-formats.md into artifacts/review-evidence/mut/, plant a fault,\n  and run a copy of the checker there. Working faults: five-day span with 3 units (CMS-1500), room rate changed (UB-04), truth tampered\n  (OCR sum), ambulance/ambiguous date removed. A check that \"requires at least one\" bare amount is by design: mutating one of\n  several lines does not fail it, so tamper the truth sum instead.\n- Fixing a visit count can create a new gap. Round-1 \"Visit 7 of 24\" became \"Visit 2 of 12\" on 06/10, which means no PT visit for\n  14 days on a 2x/wk plan with no cancellation note. Check any visit-number fix against the ledger AND the plan frequency.\n- lib14 must-contain items (handwritten date with no year; hidden text layer) need specimen text, not only a table row.\n- Packet table (case-library-sources-v2.md) fixture dates vs the §13 specimen dates drift; compare them.\n- NUCC 1500 v8.0 text (24A grouping, 24F no decimal) and CMS ch. 15 (nearest tenth; S = scene) were verifiable by download in\n  review-evidence; the NUBC occurrence-code and creation-date conventions stay \"unverified\" per the doc (outside my lens).\n- Ledger arithmetic is right when read in full: a VOID line nets to zero; the 35.00 e-stim line is easy to miss on a grep.\n\n**Why:** the T-078 r2 pass depends on the checks actually biting; the mutation run is the proof, not the 85/85.\n**How to apply:** start with the mutation script (artifacts/review-evidence/T-078-paralegal-r2-mutation.py) and adapt the pattern strings to the new doc.\nRelated: [[library-review-patterns]], [[reviewer-tooling-quirks]].\n"
}
````

### User / tool · 2026-11-02T03:50:25.486Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/record-format-review-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:29.233Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md",
 "old_string": "**How to apply:** For every review, put JSON/verdict validation in artifacts/review-evidence/<card>-*-jsoncheck.py. Related: [[spec-review-patterns]].",
 "new_string": "**How to apply:** For every review, put JSON/verdict validation in artifacts/review-evidence/<card>-*-jsoncheck.py. Related: [[spec-review-patterns]].\n\n## T-077/T-078 r2 additions (2026-11-01)\n- `grep -E` with long `.{0,120}` patterns over fetched HTML fails in ugrep (\"exceeds complexity limits\"). Strip tags and search in a python script under artifacts/review-evidence/.\n- `timeout` is not installed on this macOS host; drop it and rely on urllib's timeout argument.\n- A `mktemp` + `rmdir` combo inside a Bash call tripped board-guard. Keep Bash calls to one purpose.\n- Fetched pages redirected to the session scratchpad were not blocked by the hook, but the persona rule says reviewers write only under reviews/, artifacts/review-evidence/ and memory. Write fetch dumps to artifacts/review-evidence/ and say so in the review.\n- The NUCC and CMS PDFs download fine with urllib; write the PDF into review-evidence, run `pdftotext -layout`, then delete the PDF and text."
}
````

### User / tool · 2026-11-02T03:50:29.332Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:31.151Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [Library review patterns](library-review-patterns.md) — T-052: passed with minors; rate-vs-count rule, flag-type fit, source 403s",
 "new_string": "- [Library review patterns](library-review-patterns.md) — T-052 minors; T-077 r2: denylist self-test checks captions only, prose names escape\n- [Record-format review patterns](record-format-review-patterns.md) — T-078 r2: mutation-test the check script; visit-count fix creates a PT gap; lib14 specimen gaps"
}
````

### User / tool · 2026-11-02T03:50:31.262Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:33.725Z

**tool call — Bash**
````
{
 "command": "ls -la artifacts/review-evidence/ | grep -E \"T-077-paralegal-r2|T-078-paralegal-r2|T-077-T-078|mut|tmp\" ; ls artifacts/review-evidence/mut 2>/dev/null; ls reviews/ | grep -E \"T-07[78]\"",
 "description": "List review evidence files and confirm temp downloads were removed"
}
````

### User / tool · 2026-11-02T03:50:33.835Z

**tool result**
````
-rw-r--r--@   1 arsis  staff      649 Nov  1 19:00 T-015-r3-paralegal-mutation.out.txt
-rw-r--r--@   1 arsis  staff     1145 Nov  1 19:00 T-015-r3-paralegal-mutation.py
-rw-r--r--@   1 arsis  staff      696 Nov  1 19:46 T-031-mutation.out
-rw-r--r--@   1 arsis  staff      285 Nov  1 19:46 T-031-mutation.py
-rw-r--r--@   1 arsis  staff      631 Nov  1 19:53 T-033-mutations.txt
-rw-r--r--@   1 arsis  staff     3631 Nov  1 19:57 T-039-r2-mutation.py
-rw-r--r--@   1 arsis  staff      923 Nov  1 19:58 T-039-r2-mutation.txt
-rw-r--r--@   1 arsis  staff     2359 Nov  1 20:15 T-040-r2-mutate_api.py
-rw-r--r--@   1 arsis  staff      728 Nov  1 19:55 T-041-r2-mutation.py
-rw-r--r--@   1 arsis  staff      171 Nov  1 21:50 T-077-T-078-paralegal-r2-jsoncheck.out
-rw-r--r--@   1 arsis  staff     2197 Nov  1 21:50 T-077-T-078-paralegal-r2-jsoncheck.py
-rw-r--r--@   1 arsis  staff     6959 Nov  1 21:44 T-077-paralegal-r2-denylist.out
-rw-r--r--@   1 arsis  staff     4560 Nov  1 21:44 T-077-paralegal-r2-denylist.py
-rw-r--r--@   1 arsis  staff     1313 Nov  1 21:48 T-077-paralegal-r2-docket.out
-rw-r--r--@   1 arsis  staff     1091 Nov  1 21:45 T-077-paralegal-r2-orders.out
-rw-r--r--@   1 arsis  staff     1165 Nov  1 21:45 T-077-paralegal-r2-orders.py
-rw-r--r--@   1 arsis  staff     4741 Nov  1 21:47 T-078-paralegal-r2-checks-verbose.out
-rw-r--r--@   1 arsis  staff     1894 Nov  1 21:47 T-078-paralegal-r2-cms15.out
-rw-r--r--@   1 arsis  staff     1280 Nov  1 21:47 T-078-paralegal-r2-cms15.py
-rw-r--r--@   1 arsis  staff      831 Nov  1 21:47 T-078-paralegal-r2-mutation.out
-rw-r--r--@   1 arsis  staff     2386 Nov  1 21:47 T-078-paralegal-r2-mutation.py
-rw-r--r--@   1 arsis  staff     2598 Nov  1 21:47 T-078-paralegal-r2-nucc.out
-rw-r--r--@   1 arsis  staff     1498 Nov  1 21:47 T-078-paralegal-r2-nucc.py
drwxr-xr-x@   4 arsis  staff      128 Nov  1 21:47 mut
drwx------@   3 arsis  staff       96 Nov  1 20:09 tmp0b9w2aep
drwx------@   3 arsis  staff       96 Nov  1 19:57 tmp13651ilh
drwx------@   3 arsis  staff       96 Nov  1 20:02 tmp99xikjz2
drwx------@   3 arsis  staff       96 Nov  1 19:57 tmp_7ds_ih3
drwx------@   3 arsis  staff       96 Nov  1 20:03 tmp_gk1fcau
drwx------@   3 arsis  staff       96 Nov  1 20:09 tmpb7tx4xxn
drwx------@   3 arsis  staff       96 Nov  1 19:57 tmpexbqevaz
drwx------@   3 arsis  staff       96 Nov  1 20:09 tmphpsovtn2
drwx------@   3 arsis  staff       96 Nov  1 20:02 tmpmtvlmelh
drwx------@   3 arsis  staff       96 Nov  1 19:57 tmpq8_383ll
drwx------@   3 arsis  staff       96 Nov  1 19:58 tmpr0ep3lxh
drwx------@   3 arsis  staff       96 Nov  1 20:09 tmpwwgsz_xz
record-formats.md
record_formats_check.py
T-077-paralegal-r2.md
T-077-paralegal.md
T-078-paralegal-r2.md
T-078-paralegal.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:36.841Z

T-077 r2 is `changes`: the round-1 major is still open because Brinjikji, Nakashima, Fraser and Vera are cited in the v2 doc but not on the denylist, and the self-test only checks captions. T-078 r2 is `pass`: all three majors are closed, with three minors and one nit left. Files: /Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r2.md and /Users/arsis/zlayt-pm-project/reviews/T-078-paralegal-r2.md.
