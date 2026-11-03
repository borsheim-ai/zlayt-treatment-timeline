# Subagent: Researcher: T-077/T-078 round 2 (Researcher: T-077/T-078 round 2)

Source: `agent-ac16ec6c1a6e28601.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:27:12.456Z

You own board cards T-077 and T-078, round 2 (claimed by "researcher") in /Users/arsis/zlayt-pm-project. Read reviews/T-077-paralegal.md and reviews/T-078-paralegal.md.

**T-077 major:** add every real case or party name cited in research/case-library-sources-v2.md to the denylist in research/validate_library.py, with a test or self-check showing a planted name fails validation. Fix the minors too.

**T-078 majors:**
1. Fix CMS-1500 specimen line 3 to follow the NUCC grouping rule (the days/units mismatch).
2. Make both headline traps appear in the specimens: CMS-1500 amounts with no decimal point, and a UB-04 rate on the same line as the charge.
3. Add the missing formats that lib08, lib14 and lib15 need: an EMS run report, an ambulance bill, a Texas CPRC §18.001 billing affidavit, and a treating-doctor narrative letter. Each needs fields, wording, traps, a source URL, and a SYNTHETIC specimen.

Also apply the reviewer's correction on occurrence codes (01–06 are all accident codes), and fix the minors.

Commit with the pathspec rule, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". For each card run `board.py ac`, the handoff, and `move in_review --agent researcher`. Reply in 2 lines.

### User / tool · 2026-11-02T03:27:12.461Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-opus-5-5 · 2026-11-02T03:27:14.491Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-077-paralegal.md reviews/T-078-paralegal.md && python3 tools/board.py show T-077 | tail -40 && python3 tools/board.py show T-078 | tail -40",
 "description": "Read both reviews and card states"
}
````

### User / tool · 2026-11-02T03:27:14.704Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:27:14.911Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/record-formats-key-traps.md"
}
````

### User / tool · 2026-11-02T03:27:14.921Z

**tool result**
````
1	---
2	name: record-formats-key-traps
3	description: Highest-value extraction traps found in T-078 record-format research (CMS-1500 implied decimal, UB-04 0001 total and FL44 rate, non-service dates) for packet generation and lexicon work
4	metadata:
5	  type: project
6	---
7	
8	research/record-formats.md (T-078, 2026-11-02) is the reference for synthetic packet formats under D-042. Traps worth reusing in evals/reviews:
9	- CMS-1500 24F/28 amounts print with no decimal point (`150 | 00`), so OCR gives 15000; 24A From/To + 24G units = several days on one line; Item 14 = injury date, Item 31 = signature date.
10	- UB-04: line 23 rev code 0001 is the total (do not sum it); FL 44 holds a per-day rate on room lines next to the FL 47 charge (D-042 rate-vs-charge guard).
11	- One ED visit = facility UB-04 + ED physician 1500 + radiologist 1500 (not duplicates); EOB "amount billed" restates the bill (double count risk).
12	- Spanish notes: day-first dates; `ago` = agosto; `refiere`/`niega` carry voice/negation.
13	**Why:** these drive realistic adversarial packets and reviewer checks.
14	**How to apply:** when building library cases, lexicon entries, or reviewing billing/OCR cards, start from §1 and §15 of that file. Unverified-from-memory items are listed in its §16.
15	
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:27:16.802Z

**tool call — Bash**
````
{
 "command": "cat /Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/bc87yuitt.txt | head -400",
 "description": "Read full review output"
}
````

### User / tool · 2026-11-02T03:27:16.903Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:27:18.385Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal.md"
}
````

### User / tool · 2026-11-02T03:27:18.395Z

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

### Assistant · claude-opus-5-5 · 2026-11-02T03:27:18.782Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-078-paralegal.md"
}
````

### User / tool · 2026-11-02T03:27:18.796Z

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

### Assistant · claude-opus-5-5 · 2026-11-02T03:27:21.310Z

**tool call — Bash**
````
{
 "command": "cat research/validate_library.py && wc -l research/case-library-sources-v2.md research/record-formats.md && ls research tests | head -80 && git status --short | head -30 && git log --oneline -5",
 "description": "Inspect validator, docs, git state"
}
````

### User / tool · 2026-11-02T03:27:21.437Z

**tool result**
````
#!/usr/bin/env python3
"""Validate evals/library/* with evals/golden/check_golden.py (T-052).

check_golden.py reads cases from its own directory, so this copies evals/golden into a scratch dir, adds the library packets,
runs the checker there, and then scans the library for real identifiers (denylist taken from the sources in
research/case-library-sources.md). Exit 0 = both pass.   Run: python3 research/validate_library.py
"""
import pathlib, re, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIB = ROOT / "evals" / "library"
# Proper nouns that appear in the cited real sources (case names, parties, places, vendors). None may appear in a packet.
DENYLIST = ["Nichols", "Duke Linden", "Haygood", "Escabedo", "K & L", "K&L", "Auto Crushers", "Alexandria", "Puerto Rico", "Rissman",
            "Colossus", "Manitoba", "Verisk", "Medicare", "Tennessee", "Nebraska", "New Jersey", "Virginia", "Oklahoma", "Texas",
            "Florida", "California", "Illinois", "Michigan", "Kelly", "Cutch"]


def main():
    cases = sorted(LIB.glob("case_*.expected.json"))
    if len(cases) < 6:
        print(f"FAIL: need >= 6 library cases, found {len(cases)}")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp) / "golden"
        shutil.copytree(ROOT / "evals" / "golden", d)
        for f in LIB.glob("case_*"):
            shutil.copy(f, d / f.name)
        r = subprocess.run([sys.executable, str(d / "check_golden.py")], capture_output=True, text=True, cwd=d)
    print(r.stdout.strip()[-1500:] or r.stderr.strip()[-1500:])
    bad = []
    for f in LIB.glob("case_*"):
        t = f.read_text()
        for w in DENYLIST:
            if re.search(r"\b" + re.escape(w) + r"\b", t):
                bad.append(f"{f.name}: contains real identifier {w!r}")
        if f.suffix == ".txt" and not t.startswith("SYNTHETIC — invented for evaluation; not real patient data\n"):
            bad.append(f"{f.name}: missing SYNTHETIC header")
    for b in bad:
        print("IDENTIFIER CHECK FAIL:", b)
    print("identifier check:", "FAIL" if bad else f"ok ({len(cases)} packets, {len(DENYLIST)} denylist terms)")
    return 1 if (r.returncode or bad) else 0


if __name__ == "__main__":
    sys.exit(main())
     308 research/case-library-sources-v2.md
     679 research/record-formats.md
     987 total
research:
ASSUMPTIONS-proposed.md
__pycache__
adjuster-attacks.md
case-library-sources-v2.md
case-library-sources.md
chronology-practice.md
lexicon_selfcheck.py
library_build.py
office-view-references.md
phi-and-ai-supervision.md
record-formats.md
texas-pi-notes.md
ui-references.md
validate_library.py

tests:
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M app/backend/flags.py
 M app/backend/judges.py
 M app/frontend/api.js
 M app/frontend/charges.js
 M app/frontend/flags.js
 M app/frontend/index.html
 M app/frontend/timeline.js
 M app/llm/audited.py
 M artifacts/screenshots/office-floors-mobile-all.png
 M artifacts/screenshots/office-floors-mobile-board.png
 M artifacts/screenshots/office-floors-mobile-default.png
 M artifacts/screenshots/office-floors-mobile-floor0.png
 M artifacts/screenshots/office-floors-mobile-floor1.png
 M artifacts/screenshots/office-floors-mobile-floor2.png
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-060.md
e3cea6f feat(backend): check-trace API, per-item ladder stepper, case stepper with export gate, judge summary (T-080, D-042)
0f58181 fix(backend): credibility sentence runs to . ? ! (semicolon/line break are clauses), full-sentence excerpt, D-043 allow-list trimmed (T-067 r5)
1193f8a docs(research): record and billing document formats for synthetic packets (T-078)
bb26bf0 docs(research): case library v2 real-world PI patterns (T-077)
8634bfe fix(backend): credibility flags fail toward flagging, whole-sentence allow-list only (T-067 r4, D-043)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:27:30.434Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md"
}
````

### User / tool · 2026-11-02T03:27:30.594Z

**tool result**
````
1	# Case library sources v2 (T-077)
2	
3	Seventeen real-world personal-injury record patterns from public sources, for the next round of fully synthetic packets in
4	`evals/library/` (after `case_lib01`–`case_lib07`, see `research/case-library-sources.md`). Researched 2026-11-01/02 by the
5	researcher agent. Feature names follow D-042 (`memory/ORCHESTRATOR_DECISIONS.md`) plus the base flag types (D-013) and the
6	credibility rule (D-043).
7	
8	**No duplication with v1.** v1 covered: ER visit then a long gap; slip-and-fall onto a previously operated knee; chiropractic
9	volume on a truck rear-end; facial dog bite and scar revision; pedestrian ORIF and hardware removal; LOP billed-vs-adjusted
10	(Haygood line); missing out-of-state records. None of the patterns below reuses those scenarios or v1's sources. Sources
11	already cited in `research/texas-pi-notes.md` and `research/adjuster-attacks.md` (Haygood, In re Allstate, K&L Auto Crushers,
12	Brinjikji, Nakashima) are not used as primary sources here.
13	
14	**Read depth (stated honestly).** "Full text" means the opinion or abstract itself was fetched and read. "Summary" means only
15	a secondary write-up or search excerpt was seen. Verify a summary-level source against the original before quoting it
16	outside this repo. Court opinions are authority for what the court said; firm write-ups and press are one side's account.
17	Medical studies describe record quality in general, not PI records specifically; the PI framing is ours.
18	
19	## Synthetic-safety rules (apply to every pattern)
20	
21	1. **Pattern, not facts.** We take the shape of the record (what kind of page, which wording, which billing columns, where
22	   the gap falls) and nothing else. No party, provider, clinic, county, road, date, amount or diagnosis code is copied.
23	2. **Invented people and places.** Every name, provider, clinic and town is invented (the v1 style: Marrowgate,
24	   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass, and the real case names in this file
25	   (e.g. Garza, Broussard, Rodriguez) must be added to that denylist before any v2 packet is built.
26	3. **Dates shifted.** Packet dates run in 2025–2027 and keep only the *interval* shape the pattern needs (e.g. "second event
27	   about 12 weeks after the first"). Real dates in this file are citation dates for the source, not record dates.
28	4. **Facts recombined.** Each packet mixes features from two or more patterns, so no packet maps back to one real matter.
29	5. **Every packet text file starts with the SYNTHETIC banner line** used by v1 and is labeled synthetic in its expected JSON.
30	6. **No real records.** Nothing here was taken from a medical record; opinions describe facts in prose, and we use that prose
31	   only for scenario shape. Spanish text in packets is written fresh, not translated from any source.
32	
33	## Patterns
34	
35	### P1. Intervening second accident between first care and the key imaging
36	- **Source:** JLG Trucking, LLC v. Garza, 466 S.W.3d 157 (Tex. 2015), opinion delivered 2015-04-24 —
37	  https://www.txcourts.gov/media/943999/130978.pdf (full text, background section read).
38	- **Summary:** The plaintiff was rear-ended, saw an orthopedist five days later, did about eleven weeks of PT, then had a
39	  second crash shortly after PT ended and was taken by ambulance in a hard collar. The MRI showing herniations came only after
40	  the second crash; surgery followed years later. The court held the second accident was relevant to causation and its
41	  exclusion (including on cross of the treating doctor) was harmful error, even without a defense causation expert.
42	- **Record features:** first-incident clinic visit with no records in the file; treating-physician notes that never mention
43	  the second event; an ER record from the second event with neck complaints; first MRI dated after event 2; a narrative
44	  "history" in the surgeon's note that attributes everything to event 1; multi-year span (nerve study, second MRI, fusion).
45	- **D-042 / flags:** conflict (two incident dates in the chart), causation (history-only attribution is self-reported/
46	  provider-recited, not an opinion), gap; multi-case library; vertical stepper must show "two incidents found: human
47	  decides relevance" as a HITL step. The tool never apportions.
48	- **Synthetic-safety:** invent both crashes, shift to 2025–2026, change the interval (e.g. 10–14 weeks), change body region
49	  if useful (lumbar instead of cervical); no county, highway or vehicle type from the opinion.
50	
51	### P2. Immediate care is common-knowledge; later complex care needs an expert
52	- **Source:** Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007), decided 2007-08-31 —
53	  https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html and commentary
54	  https://www.casemine.com/commentary/us/expert-medical-evidence-mandated-for-causation-in-high-cost-automobile-accident-claims:-guevara-v.-ferrer/view
55	  (summary only).
56	- **Summary:** An elderly passenger's family relied on lay testimony to tie over $1 million in medical expenses to a crash.
57	  The court held lay evidence can link a crash to conditions within common knowledge (immediate post-crash care), but
58	  conditions outside it need expert evidence; the claimant must show what conditions generated the expenses and that each
59	  was caused by the accident.
60	- **Record features:** EMS and ER pages close in time to the event with visible injuries; then a long, medically complex
61	  course (admissions, a procedure, rehab) whose notes contain no causation statement at all; a large itemized hospital bill
62	  spanning both phases; comorbidities in the problem list of an older patient.
63	- **D-042 / flags:** causation (absence of any provider causation statement on later care is shown as "no causation
64	  language found", not as a finding), pre_existing (comorbidity list), billing analysis (charges split by encounter, cited
65	  per line); calibrated confidence must not imply causation strength.
66	- **Synthetic-safety:** age band changed, no death in the packet, invented hospital, amounts invented and far smaller.
67	
68	### P3. Billing affidavits and records are not causation; conclusory physician letter
69	- **Source:** Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.]), memorandum op. 2020-01-14, withdrawn and
70	  substituted 2021-02-11 — firm write-up https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 (fetched; opinion
71	  itself not opened).
72	- **Summary:** A past-medical award was reversed because §18.001 affidavits and records do not prove an accident caused a
73	  soft-tissue condition (cervical radiculitis, lumbar disc displacement), and the physician's letters saying the accident
74	  caused all treated injuries were conclusory because they gave no basis.
75	- **Record features:** a short "To whom it may concern" letter from a treater stating the crash caused all treatment, with
76	  no reasoning; ICD-style diagnosis lines (radiculitis, disc displacement) repeated on every bill; billing-affidavit cover
77	  pages that look like records but contain no clinical content.
78	- **D-042 / flags:** causation (letter language is shown verbatim with source; the tool never upgrades it to an opinion);
79	  billing analysis (affidavit totals cited to the page, not re-derived by the LLM); LLM-as-judge visible: the judge must
80	  reject any summary that turns "the accident caused" into a fact; record_warning for non-clinical pages.
81	- **Synthetic-safety:** invented clinic and letter text; diagnosis wording paraphrased generically; no amounts reused.
82	
83	### P4. Spanish-speaking party, certified interpreter, uncertified translation; counteraffidavit fight
84	- **Source:** Chiv v. Figueroa, No. 01-23-00638-CV (Tex. App.—Houston [1st Dist.] 2025-08-21) —
85	  https://hallapproved.com/tx/cases/appeals/2025/10659616/ (page fetched; summarized by the fetch tool, not read line by line).
86	- **Summary:** A party sought to use a deposition taken in Spanish that lacked a certified translation, with a certified
87	  interpreter at trial; that point was not preserved. Separately, striking a §18.001 counteraffidavit was harmful because the
88	  only non-lay causation evidence came from admitted medical reports; past medical was reversed and remanded.
89	- **Record features:** records where the patient's history is given in Spanish and charted in English; a note line such as
90	  "history via interpreter" (or its absence); an itemized bill paired with a counteraffidavit-style rebuttal page.
91	- **D-042 / flags:** Spanish-language records (the excerpt stays in the original language; any LLM translation is labeled
92	  and judged); speaker attribution v2 (patient vs interpreter vs provider); billing analysis (contested line items shown, not
93	  resolved).
94	- **Synthetic-safety:** invented parties and providers; Spanish lines composed fresh; no deposition content used.
95	
96	### P5. Prior accidents, claimed brain injury, memory gaps, and a six-column billing request
97	- **Source:** In re Central Oregon Truck Co., No. 20-0945 (Tex. 2022, per curiam), opinion delivered 2022-05-06 —
98	  https://www.txcourts.gov/media/1454150/200945pc.pdf (full text read).
99	- **Summary:** After a rear-end crash the plaintiff claimed a TBI and lost earning capacity; she had treated after two
100	  earlier car accidents and for other conditions with overlapping symptoms, and said at deposition that memory problems
101	  limited her recall. The court held pre-accident medical records and provider billing data relevant (subject to
102	  proportionality). The billing discovery listed: total billed, adjustments/write-offs, amount paid and by whom, balance,
103	  insurer contracts, and any LOP, lien or guarantee.
104	- **Record features:** intake forms answering "prior accidents: none" vs older notes that mention them; a neuro or
105	  neuropsych note with memory complaints; a prior tailbone/other surgical history line; provider ledgers whose columns match
106	  the six categories exactly (billed, adjusted, paid, payer, balance, LOP/lien).
107	- **D-042 / flags:** billing analysis (all six columns, each cited; totals by code); pre_existing (prior accidents); conflict
108	  (intake denial vs older note); calibrated confidence (per-state precision, not a "TBI likely" score).
109	- **Synthetic-safety:** invented crash count and years (shift to e.g. 2019/2022 priors, 2026 index event); generic employment
110	  facts omitted; ledger numbers invented.
111	
112	### P6. Health-insurer-paid claims: EOBs with billed, allowed, paid, patient share
113	- **Source:** Gunn v. McCoy, 554 S.W.3d 645 (Tex. 2018), decided 2018-06-15 (one secondary source says 2018-02-08; trust the
114	  reporter citation) — https://dallas-appellate.blogspot.com/2018/06/kmh-scotx-insurance-agents-may-know.html and
115	  https://painterfirm.com/medmal/texas-supreme-court-allows-streamlined-approach-to-medical-billing-affidavits/ (summary only).
116	- **Summary:** The plaintiff replaced provider billing affidavits with affidavits from health insurers' subrogation agents
117	  stating amounts actually paid; the court held §18.001 does not limit affiants to providers or their custodians.
118	- **Record features:** insurer EOB pages (billed / allowed / plan paid / deductible / coinsurance / patient responsibility /
119	  "not covered" with a remark code); the same date of service appearing on a provider bill and an EOB with different numbers;
120	  a subrogation-agent affidavit page.
121	- **D-042 / flags:** billing analysis (paid vs incurred, never chosen by the LLM; code reconciles EOB to provider bill and
122	  flags mismatches); charge reclassification guard (an "allowed amount" is not a charge); dedupe of the same service across
123	  two documents.
124	- **Synthetic-safety:** invented insurer, plan and remark codes; amounts invented; no real payer names.
125	
126	### P7. Pain out of proportion, "somatization", "symptom magnification" in the exam note
127	- **Source:** Rodriguez v. Wal-Mart Stores, Inc., A-2/3-17 (N.J. 2019-03-04) —
128	  https://www.njcourts.gov/system/files/court-opinions/2019/a_2_3_17.pdf (syllabus read).
129	- **Summary:** A shopper hit by a falling display developed a CRPS diagnosis. A defense neurologist described a strong pain
130	  reaction to light touch while a companion rubbed the same arm without a reaction, found nothing objective, and used
131	  "somatization" and "symptom magnification". The court held such terms are admissible case by case, distinguished them from
132	  "malingering", and upheld admission of unrelated past medical history.
133	- **Record features:** an IME/defense exam with observed-behavior narration ("pain out of proportion", "inconsistent with
134	  exam"); treater notes using the same CRPS vocabulary in the opposite direction; psychiatric or unrelated history in the
135	  problem list.
136	- **D-042 / flags:** credibility flags (D-043: any credibility term flags; a second clause or contrast word always flags);
137	  speaker attribution v2 (examiner's observation vs patient's report vs companion's behavior); LLM-as-judge visible; the tool
138	  never concludes malingering.
139	- **Synthetic-safety:** different mechanism (e.g. falling shelf at a hardware store), different limb, invented examiner;
140	  no psychiatric details beyond a generic history line.
141	
142	### P8. Waddell signs charted as a score
143	- **Source:** Fishbain et al., "A Structured Evidence-Based Review on the Meaning of Nonorganic Physical Signs: Waddell
144	  Signs", Pain Medicine 4(2):141–181 (2003); companion review Clin J Pain 20(6):399–408 (2004) —
145	  https://www.statpearls.com/articlelibrary/viewarticle/31286/ (StatPearls overview; reviews seen via search summaries only).
146	- **Summary:** Reviews of the Waddell literature found the signs associated with poorer treatment outcomes but not reliably
147	  with secondary gain or malingering; adjusters and IMEs still cite a positive count as a credibility point.
148	- **Record features:** "Waddell 3/5 positive", "superficial tenderness", "overreaction", "distraction SLR negative";
149	  clean negations ("0/5 Waddell signs") on other dates; FCE "effort inconsistent" lines.
150	- **D-042 / flags:** credibility flags with the D-043 allow-list (clean negation does not flag; mixed sentence flags);
151	  dismissal-pattern learning must not learn to auto-dismiss credibility flags (eval-guarded).
152	- **Synthetic-safety:** all wording composed fresh; invented PT/FCE provider and dates.
153	
154	### P9. Interpreter errors and ad hoc (family) interpreters in a Spanish-language history
155	- **Source:** Flores G. et al., "Errors in medical interpretation and their potential clinical consequences in pediatric
156	  encounters", Pediatrics 111(1):6–14 (2003) — AHRQ research summary
157	  https://webarchive.library.unt.edu/web/20081105020658/http:/www.ahrq.gov/research/apr03/0403RA20.htm (summary only).
158	  Corroborating (search excerpt only, page returned 403): Texas DWC Appeals Panel decisions on interpreter word choice
159	  ("espalda" for the area between the shoulder blades; "cane" vs "crutches") — https://texasworker.com/?p=38127.
160	- **Summary:** Thirteen audiotaped visits averaged 31 interpretation errors each; most had potential clinical consequences,
161	  ad hoc interpreters' errors more often so (77% vs 53%); omission was the commonest error. One reported example turned a fall
162	  into a reported assault.
163	- **Record features:** "Hx obtained via patient's son (interpreter)"; mechanism worded differently on two records (fell vs
164	  struck); a body-region word that is ambiguous in Spanish ("espalda" = back, upper or lower); a Spanish intake form beside an
165	  English provider note; possibly DD/MM/YYYY dates on a form from a clinic across the border (our assumption; no source).
166	- **D-042 / flags:** Spanish-language records; speaker attribution v2 (who said it); conflict (mechanism mismatch, code
167	  surfaces both); date-convention suggestion (pre-select with reason, one confirm); body-region ambiguity goes to human.
168	- **Synthetic-safety:** no pediatric facts; adult patient, invented family member and clinic; Spanish text composed fresh.
169	
170	### P10. Copy-forward (cloned) notes that contradict the visit
171	- **Source:** Steinkamp J., Kantrowitz J.J., Airan-Javia S., "Prevalence and Sources of Duplicate Information in the
172	  Electronic Medical Record", JAMA Network Open 5(9) (2022-09-01) — https://pubmed.ncbi.nlm.nih.gov/36156143/ (abstract read).
173	- **Summary:** Across about 104.5 million notes at one health system (2015–2020), 50.1% of text was duplicated from earlier
174	  notes about the same patient, rising from 33% to 54.2%; 45.9% of duplicated text came from a different author.
175	- **Record features:** identical ROS/exam blocks across visits weeks apart ("denies neck pain" copied into a neck-pain
176	  follow-up); "pain 6/10" unchanged across six visits; a stale medication list; a plan that repeats a completed referral.
177	- **D-042 / flags:** conflict (same-visit contradiction between HPI and copied ROS); dedupe must *not* merge two visits just
178	  because text matches (code dedupes by date + provider + content, and shows near-duplicates for human review);
179	  LLM-as-judge must catch a summary that cites the copied line as current; vertical stepper shows "near-duplicate text
180	  across N visits".
181	- **Synthetic-safety:** template text invented; invented clinic.
182	
183	### P11. Left/right transposition across records
184	- **Source:** ElGhrably I., Fraser S.G., "An observational study of laterality errors in a sample of clinical records",
185	  Eye 22(3):340–343 (2008) — https://www.nature.com/articles/6702590 (abstract via search excerpts).
186	- **Summary:** In 100 randomly selected ophthalmic record sets the authors found 44 left/right transposition errors in 32
187	  sets; 19 were later corrected; three consent forms named the wrong eye.
188	- **Record features:** "right shoulder" in the ER note, "left shoulder" in the ortho note, MRI ordered on one side and read on
189	  the other; a radiculopathy side that flips; a correction addendum.
190	- **D-042 / flags:** conflict (mixed-side exam findings, code-detected by side tokens per body part; never resolved by the
191	  LLM); judge must reject a summary that silently picks a side; HITL step "confirm side".
192	- **Synthetic-safety:** orthopedic not ophthalmic; invented providers; side flip placed at an invented visit.
193	
194	### P12. Handwritten, scanned pages with illegible entries
195	- **Source:** Rodríguez-Vera F.J. et al., "Illegible handwriting in medical records", J R Soc Med 95(11):545–546 (2002) —
196	  https://pmc.ncbi.nlm.nih.gov/articles/PMC1279250 (abstract-level via search; full text not read).
197	- **Summary:** Of 117 hospital case notes, 15% were so illegible that meaning was unclear; surgical departments scored worse.
198	- **Record features:** faxed or scanned urgent-care and chiropractic daily notes; checkbox SOAP forms; handwritten pain
199	  scores and dates; signatures illegible; a typed later page that disagrees with a handwritten earlier page; skewed scans.
200	- **D-042 / flags:** local OCR (Tesseract) with page image beside OCR text, OCR-derived items always need review; date-
201	  convention suggestion for handwritten dates; PDF hidden-text detection (assumption, no public PI source found: a scanned
202	  page whose embedded text layer differs from the image, e.g. a copy-service OCR layer; we include it adversarially).
203	- **Synthetic-safety:** handwriting rendered synthetically (font or generated strokes), never scanned from a real chart.
204	
205	### P13. Concussion not diagnosed in the ER; LOC history changes later
206	- **Source:** Powell J.M. et al., "Accuracy of Mild Traumatic Brain Injury Diagnosis", Arch Phys Med Rehabil 89(8):1550–1555
207	  (2008) — https://natlawreview.com/article/new-study-finds-emergency-room-physicians-often-fail-to-diagnose-tbi (summary only).
208	- **Summary:** Among ED patients who met CDC mild-TBI criteria by study interview, 56% had no documented TBI diagnosis in the
209	  ED record; ED care focused on ruling out severe injury.
210	- **Record features:** ER "denies LOC", "CT head negative", discharge dx "neck strain"; a later neurology note "brief LOC per
211	  patient", headaches, word-finding complaints; a neuropsych page weeks later.
212	- **D-042 / flags:** conflict (LOC denied vs reported, both cited); causation (patient-stated onset); new body system after
213	  a gap; speaker attribution (per patient vs examiner). The tool does not diagnose concussion.
214	- **Synthetic-safety:** invented ED and neurologist; mechanism changed; dates shifted.
215	
216	### P14. Chargemaster charge vs what is owed (rate-vs-charge trap on hospital bills)
217	- **Source:** Bai G., Anderson G.F., "Extreme Markup: The Fifty US Hospitals With The Highest Charge-To-Cost Ratios",
218	  Health Affairs 34(6) (2015) — https://publichealth.jhu.edu/2015/some-hospitals-marking-up-prices-more-than-1000-percent
219	  (press release; paper not opened).
220	- **Summary:** In 2012 Medicare cost-report data the typical hospital charged about 3.4 times Medicare-allowable cost; the 50
221	  highest-markup hospitals charged roughly ten times, 49 of them for-profit.
222	- **Record features:** UB-04-style itemized bill with revenue codes, units and unit price; a "self-pay discount" line; a
223	  later statement with a contractual adjustment; a price list or rate sheet page that is not a charge.
224	- **D-042 / flags:** charge reclassification guard (a rate becomes a charge only with code-verified charge wording plus a
225	  judge re-check); billing analysis (units × unit price is recomputed in code and compared with the stated line total);
226	  totals in code only.
227	- **Synthetic-safety:** invented hospital, codes and prices; no real chargemaster data.
228	
229	### P15. Ambulance bill: base rate plus per-mile mileage
230	- **Source:** FAIR Health, "A Window into Utilization and Cost of Ground Ambulance Services" (brief, 2023) —
231	  https://mma.prnewswire.com/media/2207553/A_Window_into_Utilization_and_Cost_of_Ground_Ambulance_Services___A_FAIR_Health_Brief.pdf?p=pdf
232	  (search excerpt only).
233	- **Summary:** Ground ambulance claims are billed as a base transport line plus mileage per statute mile; most claim lines
234	  were out of network (63.7% in 2018, 59.4% in 2022).
235	- **Record features:** EMS run sheet (times, vitals, "ambulatory at scene" or "stretcher") plus an invoice with "ALS base",
236	  "mileage 14 mi @ $X/mi" and a line total; a balance-bill page.
237	- **D-042 / flags:** charge reclassification (the per-mile rate is a rate; only the extended line or stated total is a charge);
238	  billing analysis (lien/balance columns); code checks miles × rate = stated line.
239	- **Synthetic-safety:** invented EMS agency, mileage and rates.
240	
241	### P16. Same-week symptom contradiction across two providers
242	- **Source:** Lewis Brisbois write-up of a Harris County zero-damages defense verdict (trial 2023-12; published 2024-06-25)
243	  — https://www.legal500.com/intelligence/united-states/litigation-mediation-arbitration/houston-office-secures-zero-damages-verdict-in-rear-end-collision-case
244	  (fetched; defense-side account).
245	- **Summary:** After an ER visit the next day and care with several providers, the plaintiff reported significant neck and
246	  back pain to an orthopedic surgeon while denying those symptoms to her primary-care doctor; the defense also disputed a
247	  recommended discectomy and pointed to photos of a minor impact. The jury awarded nothing.
248	- **Record features:** ortho note "low back pain 8/10, radiating" and a PCP note days apart with ROS "denies back pain"
249	  (possibly copied forward, see P10); a surgical recommendation with a cost estimate; property-damage photos referenced but
250	  not in the file.
251	- **D-042 / flags:** conflict (cross-provider, code pairs nearby dates); billing analysis (estimate is not a charge, D-019);
252	  vertical stepper HITL "two providers disagree; paralegal decides which to cite".
253	- **Synthetic-safety:** drug-use facts from the write-up are **not** used; invented providers; shifted dates.
254	
255	### P17. Minimal property damage, low-speed impact (MIST) language in records
256	- **Source:** Hampton v. Miskell (Tex. App. 2017) — https://www.studicata.com/summaries/court-of-appeals-of-texas/hampton-v-miskell-2017-rbb5bb
257	  (search excerpt only; page returned 403).
258	- **Summary:** The court upheld admission of an accident reconstructionist's opinion that a vehicle was moving at five miles
259	  per hour or less, noting it was cumulative of other evidence of minor property damage.
260	- **Record features:** EMS "minor damage to rear bumper", "ambulatory at scene", "refused transport"; ER "low-speed MVC";
261	  later treater notes that describe the crash as "violent" or "high impact" (patient-reported).
262	- **D-042 / flags:** causation (scene facts per D-018 lexicon); conflict (mechanism description changes over time, both
263	  attributed); speaker attribution.
264	- **Synthetic-safety:** invented crash; no speeds or vehicles from the source.
265	
266	## Coverage map: pattern x D-042 feature
267	
268	| Feature (D-042 / base flags) | Patterns |
269	|---|---|
270	| Charge reclassification guard (rate vs charge) | P6, P14, P15 |
271	| Billing analysis (billed, adjusted, paid, LOP/lien, cited) | P2, P3, P4, P5, P6, P14, P15, P16 |
272	| Spanish-language records | P4, P9 |
273	| Local OCR, scanned/handwritten pages | P12 |
274	| PDF hidden-text detection | P12 (assumption-based, no public source) |
275	| Date-convention suggestion | P9 (assumption), P12 |
276	| Dismissal-pattern learning (eval guard) | P8 |
277	| Calibrated confidence | P2, P5 |
278	| Speaker attribution v2 | P4, P7, P9, P13, P17 |
279	| LLM-as-judge visible | P3, P7, P10, P11 |
280	| Vertical stepper / HITL hand-off | P1, P10, P11, P16 |
281	| Credibility flags (D-043) | P7, P8 |
282	| Conflict | P1, P5, P9, P10, P11, P13, P16, P17 |
283	| Pre-existing | P2, P5 |
284	| Causation language | P1, P2, P3, P13, P17 |
285	| Gap | P1, P13 |
286	
287	## Suggested v2 packets (each recombines two or more patterns)
288	
289	| Proposed id | Combines | One-line synthetic premise |
290	|---|---|---|
291	| lib08_second_crash_mri_after | P1 + P13 | Rear-end, PT, second minor crash 11 weeks later, MRI and neuro note after crash 2 |
292	| lib09_spanish_interpreter_espalda | P9 + P4 + P11 | History via son; "espalda" ambiguity; side flips between ER and ortho |
293	| lib10_eob_vs_provider_bill | P6 + P14 | Insured patient; hospital itemized bill plus EOBs with different numbers for same DOS |
294	| lib11_priors_and_ledger | P5 + P2 | Two prior crashes denied on intake; six-column ledgers; older patient comorbidities |
295	| lib12_ime_credibility | P7 + P8 | Defense IME with symptom-magnification wording; PT notes with clean and mixed Waddell lines |
296	| lib13_cloned_notes_cross_provider | P10 + P16 | Copied ROS denies the complaint the ortho charts the same week |
297	| lib14_handwritten_chiro_scans | P12 + P15 | Scanned handwritten daily notes; ambulance base + mileage invoice; hidden text layer |
298	| lib15_conclusory_letter_mist | P3 + P17 | "Accident caused all" letter; EMS minor-damage and refused-transport wording |
299	
300	## Assumptions and limits
301	
302	- Hidden-text PDFs and DD/MM/YYYY dates in Spanish-language records are our adversarial assumptions; no public PI source
303	  documented them. They are included because D-042 reinstated those features and they need test cases.
304	- Texas DWC Appeals Panel decisions (P9) and Hampton v. Miskell (P17) were seen only as search excerpts (pages returned 403).
305	- Medical studies (P9–P14) describe general record quality, not PI files; the record features are our inference.
306	- Defense-firm (P16) and plaintiff-side write-ups are advocacy; used for scenario shape only.
307	- Search also surfaced Texas Lawbook (2023-05-16) on a verdict where LOP provider entities were shown to the jury; it is
308	  paywalled and was not used.
309	
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:27:32.266Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/record-formats.md"
}
````

### User / tool · 2026-11-02T03:27:32.391Z

**tool result**
````
1	# Record and billing document formats for synthetic PI packets (T-078)
2	
3	**Purpose.** D-042 says the multi-case library grows from researched real-world document formats. This file describes the twelve document
4	types a Texas PI paralegal typically receives, so the packet generator can produce realistic, **fully synthetic** records that exercise the
5	tool's hard parts: dates, charges versus rates versus adjustments, totals lines, multiple authors, Spanish text and OCR noise.
6	
7	**Rules followed.** Every specimen below is invented and labeled SYNTHETIC. No person, provider, payer, address, phone, NPI, tax ID, claim
8	number or NDC is real; identifiers use a `SYN-` prefix, phones use the 555-01xx fiction range, places are invented. CPT, HCPCS, ICD-10 and
9	revenue codes are public code sets, used only as codes. Sources are listed per format with whether I opened the page or worked from a
10	search-result summary; where a source is thin I state the assumption.
11	
12	**How to use.** Section 1 holds the cross-cutting traps (dates, money, authorship). Sections 2 to 14 cover one format each (fields, wording,
13	traps, sources, specimen). Section 15 maps formats to product rules and proposes packet mixes. Section 16 lists assumptions and gaps.
14	
15	---
16	
17	## 1. Cross-cutting traps (apply to every format)
18	
19	### 1.1 Dates that are not service dates
20	| Date on the page | Where it appears | Why it is a trap |
21	|---|---|---|
22	| Date of injury / onset | CMS-1500 Item 14 (qualifier 431), UB-04 occurrence code date, LOP letter "Re:" line, intake form | It is the accident date, not a visit. Treating it as an encounter creates a phantom visit and hides the real first-treatment gap. |
23	| Signature / creation date | CMS-1500 Item 31, UB-04 FL 45 on the total line, radiology "Signed", op-note "D:/T:" dictation and transcription stamps | Usually a day or more after the service. Using it shifts the chronology and can invent a gap. |
24	| Statement / print / fax date | Ledger "Statement date", pharmacy "Printed on", fax header line at the top of every page | Same date on every page of a records production; a naive extractor dates every entry to the production date. |
25	| Received / Bates stamp | Rubber stamp "RECEIVED NOV 03 2026", Bates footer | Law-firm intake date; never a service date. |
26	| Fill date vs written date | Pharmacy log | A refill is not a visit and not a new prescription. |
27	| Exam date vs report date vs addendum date | Radiology | Three dates for one study. |
28	| Date ranges | CMS-1500 24A From/To with 24G units, UB-04 FL 6 statement period, PT "Visits 1 to 12" summary | One line can stand for many consecutive days (NUCC allows grouping only on consecutive days with identical code, charge and provider; days must equal units). |
29	
30	**Formats seen:** `05/14/2026`, `051426` (claim boxes, no separators), `05 | 14 | 2026` (boxed), `2026-05-14` (EHR exports), `14-MAY-26`
31	(pharmacy and lab systems), `14/05/2026` and `14 de mayo de 2026` (Spanish-language clinics, day first), `5/14` (handwritten, no year),
32	`ene/abr/ago/dic` (Spanish month abbreviations; `ago` = agosto, also an English word: "3 days ago").
33	
34	### 1.2 Money: charges, rates, adjustments, estimates
35	| Wording | Meaning | Counted as a billed charge? (D-019, D-042) |
36	|---|---|---|
37	| "Charges", "Total charges", "$Charges", "Amount billed", "Gross charges" | A stated charge for a dated service | Yes, when tied to a date of service and accepted |
38	| "Rate", "per visit", "per unit", "per day", "fee schedule", "Usual & customary", UB-04 FL 44 accommodation rate | A price, not something billed for a visit | No. D-042: a rate becomes a charge only with code-verified charge wording plus a judge re-check |
39	| "Adjustment", "Contractual adj", "Write-off", "W/O", "Network discount", "Courtesy discount", CARC "CO-45" | Reduction by the provider or under a contract | No (separate column; never subtracted silently from billed) |
40	| "Payment", "Ins pmt", "Pt pmt", "Plan paid", "Amount paid" (Item 29) | Money received | No |
41	| "Balance", "Balance due", "Amount due", "You owe", "Patient responsibility" | Remaining amount | No (it is a derived figure) |
42	| "Estimate", "Anticipated", "Quote", "Future care" | Not yet incurred | No |
43	| "LOP balance", "Lien amount", "Reduced to", "Accept in full satisfaction" | Negotiated or asserted amount | No (internal notes only) |
44	
45	**Number formats.** CMS-1500 boxes use no dollar sign, no comma and no decimal point, with cents in a separate box to the right of a vertical
46	line, so OCR reads `150 | 00` as `15000` or `150 00`. The shaded supplemental line *does* use a decimal point. Ledgers show credits as
47	`(45.00)`, `-45.00`, `45.00-` or `45.00 CR`. Spanish-language clinics in Mexico and much of Latin America use `$1.250,00`; Texas clinics
48	serving Spanish speakers usually print US format. A running-balance column is cumulative and must never be summed.
49	
50	### 1.3 Authorship and voice
51	A single ED visit carries the triage nurse, the physician (sometimes "scribed for"), the radiologist and the discharge nurse. Therapy notes
52	carry the PT, the PTA and a co-signature. Intake forms are in the patient's own hand. Per D-040 the tool does not label speakers; the generator
53	should still produce these mixed voices ("Pt states", "wife reports", "per EMS") so the excerpt carries them.
54	
55	### 1.4 One visit, several bills
56	An ED visit produces a facility bill (UB-04), an emergency-physician bill (CMS-1500), and a radiologist bill (CMS-1500 with modifier 26) for
57	the same date. Surgery adds surgeon, assistant, anesthesia, facility and implant lines. These are **not duplicates**; a dedupe that keys on
58	date plus amount, or date plus provider name, will wrongly merge or wrongly keep them. A true duplicate is the same bill reproduced twice
59	(e.g., once in the provider's production and again as an attachment to the §18.001 affidavit).
60	
61	---
62	
63	## 2. Emergency department note
64	
65	**Fields.** Arrival date/time; mode of arrival (EMS, private vehicle); triage block (ESI level, vitals, pain score, triage nurse narrative);
66	chief complaint (often in the patient's words, with duration); HPI (mechanism, onset, OPQRST / OLD CARTS elements); ROS; PMH/PSH, meds,
67	allergies, social history; physical exam; results (labs, imaging with preliminary reads); MDM (differential, ED course, reassessments);
68	clinical impression / diagnoses; disposition (discharged, admitted, transferred) with follow-up and return precautions; attestation and
69	electronic signature with timestamp.
70	
71	**Typical wording.** "Restrained driver in a rear-end MVC at approx 35 mph, + airbag deployment, ambulatory at scene." "Denies LOC, denies
72	head strike." "Pain 8/10." "ROS: all other systems reviewed and negative." "CT C-spine: no acute fracture (prelim)." "Dx: cervical strain,
73	initial encounter." "Dispo: home, f/u with PCP in 3 to 5 days, return for worsening." The ED note carries **no charges**; charges arrive on
74	the UB-04 and CMS-1500.
75	
76	**Extraction traps.**
77	- Midnight rollover: arrival 23:48, physician exam 00:31 the next calendar day; the visit date is the arrival date.
78	- Templated negatives ("all other systems negative") sit next to positives; a negation scope error drops a finding.
79	- Copy-forward PMH ("hx chronic low back pain") is a pre-existing-condition flag the adjuster will use.
80	- Triage pain score and post-medication pain score differ in the same note.
81	- Preliminary ED read versus the radiologist's final read can disagree; the final report is the authority.
82	- "Scribed for Dr. X by Y" and nurse addenda are different authors within one document.
83	
84	**Sources.**
85	- EMRA, *Medical Student Documentation* (ED note template: CC, HPI, PMH, exam, MDM, ED course, disposition): https://www.emra.org/be-involved/committees/education-committee/medical-student-documentation — search summary only (page 404 when fetched).
86	- IEM Student, *Documentation*: https://iem-student.org/documentation/ — search summary; takeaway: review triage notes and vitals before writing, CC ideally in the patient's words, mnemonics OLD CARS / OPQRST for HPI.
87	
88	**Specimen (SYNTHETIC).**
89	```
90	SYNTHETIC RECORD - NOT A REAL PATIENT
91	Quillfeather Regional Medical Center - Emergency Department        MRN: SYN-ED-40417
92	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   DOB: 03/09/1991
93	Arrival: 05/14/2026 23:48   Mode: EMS   ESI: 3
94	TRIAGE (RN Tamsin Brook, SYNTHETIC): BP 142/88 HR 96 RR 18 SpO2 98% Pain 8/10.
95	  Pt states "the truck hit me from behind and my neck snapped forward."
96	PHYSICIAN NOTE (Dr. Ilario Fenwick, SYNTHETIC)  Seen: 05/15/2026 00:31
97	CC: Neck pain x 1 hour.
98	HPI: Restrained driver, rear-end MVC, + airbag. Denies LOC. Reports tingling R hand.
99	PMH: Low back pain 2023, resolved per pt.
100	ROS: All other systems reviewed and negative.
101	EXAM: TTP C5-C7 paraspinals, no midline step-off. Grip 4/5 R.
102	RESULTS: CT cervical spine w/o contrast - no acute fracture (prelim, see final).
103	MDM: Strain vs radiculopathy. Toradol 30 mg IM. Reassessed 01:40, pain 5/10.
104	IMPRESSION: Cervical strain, initial encounter (S16.1XXA).
105	DISPO: Discharged 02:05 05/15/2026. F/U PCP 3-5 days. Return if weakness worsens.
106	Electronically signed 05/15/2026 03:12
107	```
108	
109	---
110	
111	## 3. Physical therapy daily note (SOAP)
112	
113	**Fields.** Date; visit number against plan ("Visit 7 of 24"); authorization/referral; time in and time out; S (patient report, NPRS pain
114	0-10, function, home exercise compliance); O (ROM in degrees, MMT grades, special tests, gait); interventions table with CPT, minutes and
115	units; total timed minutes and total treatment minutes; A (progress toward goals, tolerance); P (frequency and duration, next visit focus);
116	signature with credential (PT, PTA, DPT) and co-signature when a PTA treats.
117	
118	**Typical wording.** "Pt reports neck pain 5/10, improved from 7/10 at eval." "Cervical rotation R 55 deg, L 60 deg." "97110 TherEx 23 min
119	(2 units); 97140 Manual 12 min (1 unit); 97014 E-stim unattended 15 min." "Total timed: 35 min. Total tx: 50 min." "Tolerated well. Continue
120	POC 3x/wk x 4 wks." Cancellations appear as a note with no treatment: "Pt cancelled - no transportation." Charges usually do **not** appear
121	on the note; they appear on the CMS-1500 or ledger as units times a fee.
122	
123	**Extraction traps.**
124	- Timed codes bill in 15-minute units under the 8-minute rule; minutes are not dollars and units are not visits.
125	- "Visit 7 of 24" states the plan, not the count delivered; the adjuster compares planned versus actual.
126	- Cancelled or no-show entries are dated documents that are **not** encounters, but they may state the reason for a gap.
127	- Identical copy-forward text across visits (a known audit flag) reads as "cloned notes" to the defense.
128	- Re-evaluation and discharge summaries restate earlier values; extracting them as new measurements double counts.
129	
130	**Sources.**
131	- Colorado HCPF Bulletin B1900436 (timed-minute totals across codes, e.g. 40 minutes = 3 units): https://hcpf.colorado.gov/sites/hcpf/files/Bulletin_1019_B1900436.pdf — search summary.
132	- AAPC compliance article on therapist signatures and documented time after an OIG audit: https://aapc.com/codes/scc_articles/article_pdf/47/compliance-forget-your-john-hancock-and-you-could-be-out-thousands-41142 — search summary.
133	- WebPT, *SOAP note tips for PTs*: https://www.webpt.com/blog/soap-note-tips-for-pts-plus-examples — search result, not opened. Assumption: SOAP order and fields above match common PT EMR output.
134	
135	**Specimen (SYNTHETIC).**
136	```
137	SYNTHETIC RECORD
138	Larkspur Hollow Physical Therapy        Daily Note        Visit 7 of 24
139	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Date: 06/10/2026   In 09:02 Out 09:54
140	S: Pt reports neck pain 5/10 (7/10 at eval 05/27/2026). Still wakes at night.
141	O: Cerv rot R 55 deg / L 60 deg. Grip R 4/5.
142	Interventions:  97110 TherEx  23 min  2u
143	                97140 Manual  12 min  1u
144	                97014 E-stim  15 min  (untimed)
145	Total timed 35 min / Total tx 50 min
146	A: Tolerated well. Progressing toward goal of 70 deg rotation.
147	P: Continue POC 3x/wk x 4 wks.
148	Signed: Wren Abernathy, PTA (SYNTHETIC)   Co-signed: Odalys Kerr, DPT (SYNTHETIC) 06/11/2026
149	--
150	06/12/2026  Pt cancelled - no transportation. Rescheduled 06/15/2026.
151	```
152	
153	---
154	
155	## 4. Chiropractic daily note and travel card
156	
157	**Fields.** Date; subjective complaint with pain scale (VAS/NPRS) and functional change since last visit; objective exam documenting the
158	PART elements (Pain/tenderness, Asymmetry/misalignment, Range-of-motion abnormality, Tissue/tone change) at specific spinal levels;
159	segments adjusted (e.g., C5, C6, L4) and technique; modalities (97012 mechanical traction, 97014 e-stim, 97010 hot/cold); CPT for
160	manipulation (98940 one to two regions, 98941 three to four, 98942 five, 98943 extraspinal); assessment of progress; plan and visit
161	frequency; provider signature. Many PI chiropractic offices also keep a **travel card** (one row per visit with checkboxes for regions and
162	modalities), which arrives as a scanned grid.
163	
164	**Typical wording.** "Pt states neck 6/10, better than last visit." "TTP and hypertonicity bilat C4-C6, ROM flex 35 deg." "Adjusted C5, C6,
165	T4, L5 - diversified." "98941, 97014, 97010." "Pt responding favorably, continue 3x/wk." Fee slips say "Adjustment 3-4 regions $85.00" -
166	which may be a fee schedule **rate** or a charge for that visit depending on whether a date of service is attached.
167	
168	**Extraction traps.**
169	- Medicare guidance requires the exact segment, not just a region; PI notes often list both. Do not count segments as visits.
170	- "Same as last visit", "SALV", or identical text across weeks is the cloned-note pattern adjusters attack.
171	- Travel-card checkmarks are OCR-hostile (see section 13); a missed checkmark loses a modality, a stray mark invents one.
172	- Percent-improvement statements ("50% better") are patient report, not an objective measure.
173	- Post-visit narrative reports written for the attorney are supplemental reports, not daily notes; their date is the letter date.
174	
175	**Sources.**
176	- Noridian JF Part B, *Chiropractic Documentation Guidelines - Initial vs Subsequent Visits*: https://med.noridianmedicare.com/web/jfb/specialties/chiropractic/documentation-guidelines — **opened**. Takeaway: subsequent-visit notes need updated history, exam supporting the subluxation, assessment of progress, the exact segment treated, and date-specific (not cloned) findings.
177	- CMS MLN, *Chiropractic Services* compliance tip: https://www.cms.gov/training-education/medicare-learning-networkr-mln/compliance/medicare-provider-compliance-tips/chiropractic-services — search summary; PART acronym and AT modifier for 98940-98942.
178	
179	**Specimen (SYNTHETIC).**
180	```
181	SYNTHETIC RECORD
182	Brightwater Spine & Wellness (SYNTHETIC)         Daily Note
183	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   DOS: 06/03/2026   Visit #9
184	S: Neck 6/10, low back 4/10. Pt states "about 50% better since I started."
185	O: TTP + hypertonicity bilat C4-C6. Cerv flex 35 deg (norm 50). Asym: R high shoulder.
186	Adjusted: C5, C6, T4, L5 (diversified).  Modalities: 97014 e-stim 15 min, 97010 cold pack.
187	CPT: 98941, 97014, 97010
188	A: Improving. P: Continue 3x/wk x 4 wks, re-exam 06/24/2026.
189	Dr. Corvin Ashdown, DC (SYNTHETIC)
190	--- Travel card (scanned) ---
191	DATE    | C | T | L | ES | HP | TR
192	06/01   | x | x | x | x  | x  |
193	06/03   | x | x | x | x  | x  |
194	06/05   | x |   | x | x  |    |
195	```
196	
197	---
198	
199	## 5. Radiology report (x-ray, CT, MRI)
200	
201	**Fields.** Exam name and modality; exam date/time; accession number; ordering clinician; clinical indication/history; technique (contrast,
202	sequences); comparison (prior studies, or "None"); findings by structure; impression (most important first); recommendations; reading
203	radiologist and signature date/time; preliminary versus final status; addenda.
204	
205	**Typical wording.** "INDICATION: MVC 05/14/2026, neck pain, R arm paresthesia." "COMPARISON: None." / "COMPARISON: MRI 08/2023." "C5-6: disc
206	osteophyte complex with mild foraminal narrowing." "Straightening of the normal cervical lordosis, which may be positional or reflect muscle
207	spasm." "No acute fracture." "Chronic-appearing." "Clinical correlation recommended." Charges appear separately: a technical (facility) bill
208	and a professional (radiologist, modifier 26) bill.
209	
210	**Extraction traps.**
211	- Indication text is the ordering clinician's statement (often including the mechanism), not a finding by the radiologist.
212	- "Comparison: MRI 08/2023" reveals prior imaging - a pre-existing flag - even when the findings section is silent about it.
213	- Hedges ("may represent", "cannot be excluded", "likely chronic", "age-indeterminate", "degenerative") are the language adjusters quote.
214	- Exam date, signed date and addendum date differ; an addendum can change the impression.
215	- The ED's preliminary read and the final report may disagree; keep both, cite each.
216	
217	**Sources.**
218	- ACR *Practice Parameter for Communication of Diagnostic Imaging Findings* (rev. 2020): https://gravitas.acr.org/PPTS/GetDocumentView?docId=74 — **opened**, but only section headings rendered (II.B Components of the Report, II.C Final Report, II.D Preliminary Report). Takeaway from the search summary: a final report must be generated by the interpreting physician; follow-up studies suggested when appropriate.
219	- UF Radiology, *Components of a Report*: https://protocols.xray.ufl.edu/live_crr/prog/home/module-components_report.php — search summary; impression summarizes toward a diagnosis with the most important finding first.
220	- APS Medical Billing white paper (demographics, clinical information, body, impression): https://apsmedbill.com/whitepapers/documenting-complete-interpretation-report-diagnostic-radiology-services — search summary.
221	- Assumption: the INDICATION / TECHNIQUE / COMPARISON / FINDINGS / IMPRESSION order is near-universal; I did not read the ACR II.B body text.
222	
223	**Specimen (SYNTHETIC).**
224	```
225	SYNTHETIC RECORD
226	Ferncastle Imaging Associates (SYNTHETIC)          Accession: SYN-ACC-77120
227	EXAM: MRI CERVICAL SPINE WITHOUT CONTRAST     Exam date: 06/18/2026 14:05
228	Patient: Delphine Okonkwo-Vale (SYNTHETIC)    Ordering: Dr. Corvin Ashdown, DC (SYNTHETIC)
229	INDICATION: MVC 05/14/2026. Neck pain, R hand tingling.
230	TECHNIQUE: Sagittal T1, T2, STIR; axial T2.
231	COMPARISON: Cervical radiographs 05/15/2026.
232	FINDINGS: Straightening of the cervical lordosis, which may be positional or reflect spasm.
233	  C5-6: 3 mm posterior disc protrusion with mild R foraminal narrowing. Mild disc desiccation.
234	  No fracture. No marrow edema.
235	IMPRESSION:
236	  1. C5-6 disc protrusion with mild right foraminal narrowing. Age of finding cannot be determined.
237	  2. Mild C5-6 desiccation, likely degenerative.
238	Electronically signed: Dr. Peregrine Holt (SYNTHETIC) 06/19/2026 08:22
239	ADDENDUM 06/20/2026: Comparison radiographs reviewed; no change to impression.
240	```
241	
242	---
243	
244	## 6. Operative report
245	
246	**Fields.** Patient and record identifiers; date of surgery (start/stop times); preoperative diagnosis; postoperative diagnosis;
247	procedure(s) performed (often with CPT in the billing copy); surgeon, assistant(s); anesthesia type and anesthesiologist; estimated blood
248	loss (EBL) or quantitative blood loss; fluids; specimens; drains; implants (manufacturer, lot - often stickers); complications; indications
249	(history and consent); findings; description of procedure; condition and disposition; dictation and transcription stamps.
250	
251	**Typical wording.** "PREOPERATIVE DIAGNOSIS: Right C6 radiculopathy secondary to C5-6 disc protrusion." "PROCEDURE: C5-6 anterior cervical
252	discectomy and fusion." "EBL: 50 mL." "SPECIMENS: Disc material to pathology." "COMPLICATIONS: None." "INDICATIONS: The patient is a 35-year-old
253	who reports neck and arm pain since a motor vehicle collision..." "D: 08/04/2026 T: 08/05/2026."
254	
255	**Extraction traps.**
256	- The INDICATIONS paragraph repeats history, including the patient's account of the accident; it is not a causation opinion by the surgeon.
257	- Dictation (D:) and transcription (T:) dates follow the surgery date.
258	- Pre- and postoperative diagnoses can differ; the postoperative one reflects what was found.
259	- One surgery date generates several bills (surgeon, assistant with modifier 80/AS, anesthesia time units, facility/ASC, implants); not duplicates.
260	- "No EBL" or "no specimens" may simply be omitted (a Joint Commission FAQ says documentation is not required when there were none).
261	
262	**Sources.**
263	- Joint Commission FAQ, *Operative report - timing and content* (ambulatory RC): https://www.jointcommission.org/standards/standard-faqs/ambulatory/record-of-care-treatment-and-services-rc/000002043 — search summary; report written or dictated immediately after the procedure; no requirement to document absent EBL or specimens.
264	- ACDIS Q&A on the immediate post-op note elements (surgeons, procedures, findings, EBL, specimens, post-op diagnosis): https://www.acdis.org/articles/qa-anesthesia-records-and-querying-blood-transfusion — search summary.
265	- CAMC post-op documentation regulatory table (pre- and post-op diagnosis, dates and times, surgeon and assistants): https://camc.org/sites/default/files/MedicalAffairs/Post%20op%20Documentation%20Regulatory%20Requirements.pdf — search summary.
266	
267	**Specimen (SYNTHETIC).**
268	```
269	SYNTHETIC RECORD
270	Thistledown Surgical Center (SYNTHETIC)      OPERATIVE REPORT
271	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Date of surgery: 08/04/2026  07:42-09:15
272	PREOPERATIVE DIAGNOSIS: Right C6 radiculopathy, C5-6 disc protrusion.
273	POSTOPERATIVE DIAGNOSIS: Same.
274	PROCEDURE: C5-6 anterior cervical discectomy and fusion with interbody device.
275	SURGEON: Dr. Anselm Greaves (SYNTHETIC)   ASSISTANT: Juno Pell, PA-C (SYNTHETIC)
276	ANESTHESIA: General, Dr. Marisol Quint (SYNTHETIC)
277	EBL: 50 mL.  SPECIMENS: Disc material to pathology.  COMPLICATIONS: None.
278	IMPLANTS: Interbody cage, lot SYN-LOT-0042.
279	INDICATIONS: Pt reports neck and R arm pain since a motor vehicle collision on 05/14/2026,
280	  not improved with 12 weeks of therapy.
281	FINDINGS: Posterior disc protrusion compressing R C6 root.
282	D: 08/04/2026  T: 08/05/2026
283	```
284	
285	---
286	
287	## 7. Pharmacy dispensing log (patient Rx history printout)
288	
289	**Fields.** Pharmacy name, address and NABP/NCPDP number; patient; date range and "printed on" date; per fill: fill date, Rx number, refill
290	number (0 = new, 1..n = refill) or refills remaining, drug name and strength, NDC (11-digit, 5-4-2), quantity, days supply, prescriber,
291	price (usual and customary), plan paid, patient paid/copay, status (filled, reversed, returned to stock).
292	
293	**Typical wording.** "Fill 05/15/26 Rx 6604412 R0 CYCLOBENZAPRINE 10MG TAB Q 30 DS 10 Dr. Fenwick." "U&C $24.99 Plan $0.00 Pt pd $24.99."
294	"REVERSED 05/22/26." "Q/DS 90/30."
295	
296	**Extraction traps.**
297	- Days supply is not quantity (90 tabs over 30 days).
298	- Fill date is not the prescribing visit; refills (R1, R2) are not new prescriptions and not encounters.
299	- Reversed or returned-to-stock claims appear as a line with the same Rx number; counting them inflates both meds and money.
300	- U&C price, plan paid and patient paid are three different numbers on one line; which one is a "charge" for a demand is a legal choice
301	  the tool must not make (route to notes unless the record states a charge).
302	- NDC formats vary (10-digit hyphenated 4-4-2/5-3-2/5-4-1 vs 11-digit); generic substitution changes the drug name between fills.
303	
304	**Sources.**
305	- CVS Caremark receipt requirements via NYC PBA (minimum fields: NDC, fill date, metric quantity, total charge, days supply, pharmacy NABP; days supply is not quantity): https://www.nycpba.org/media/2706/caremark.pdf — search summary.
306	- OPM FEHB data attachment (refill number: 0 for new): https://piv.opm.gov/healthcare-insurance/carriers/fehb/2007/2007-09attachment2.pdf — search summary.
307	- RedSail NRx help, *Prescription Record* (Rx number, refills remaining, NDC, Q/DS): https://hub.redsailtechnologies.com/documents/RS/NRX/NRx%20Help%20Center/Set_Up_Store_Control_Options/Set_Up_Store_Control_Options/Prescription_Record,_Alphabetical_Order.htm — search summary.
308	
309	**Specimen (SYNTHETIC).**
310	```
311	SYNTHETIC RECORD
312	Mossgate Community Pharmacy (SYNTHETIC)  NCPDP SYN-0000123   Printed on: 11/02/2026
313	Patient Rx History  05/01/2026 - 10/31/2026   Patient: Delphine Okonkwo-Vale (SYNTHETIC)
314	FILL DT   RX#        RF DRUG                      NDC            QTY DS  PRESCRIBER        U&C    PLAN   PT PD  STATUS
315	05/15/26  SYN6604412 0  CYCLOBENZAPRINE 10MG TAB  00000-0000-01   30 10  FENWICK I (SYN)  24.99  0.00  24.99  FILLED
316	05/15/26  SYN6604413 0  NAPROXEN 500MG TAB        00000-0000-02   60 30  FENWICK I (SYN)  18.40  0.00  18.40  FILLED
317	05/25/26  SYN6604412 1  CYCLOBENZAPRINE 10MG TAB  00000-0000-01   30 10  FENWICK I (SYN)  24.99  0.00  24.99  REVERSED 05/26/26
318	06/02/26  SYN6604412 1  CYCLOBENZAPRINE 10MG TAB  00000-0000-03   30 10  FENWICK I (SYN)  21.50  0.00  21.50  FILLED
319	```
320	
321	---
322	
323	## 8. CMS-1500 (02/12) professional claim
324	
325	**Fields (NUCC numbering).** 1a insured ID; 2 patient name; 3 DOB (8-digit) and sex; 10a-c condition related to employment / **auto accident
326	(with state)** / other accident; 11 insured's policy; 14 date of current illness or injury with qualifier (431 onset); 17 referring provider;
327	21 ICD indicator (0 = ICD-10) and diagnoses A-L; 24A dates of service From/To; 24B place of service; 24D CPT/HCPCS with up to four modifiers;
328	24E diagnosis pointer (letters); 24F $charges; 24G days or units; 24J rendering provider NPI; 25 federal tax ID; 28 total charge; 29 amount
329	paid; 30 reserved for NUCC use (no balance-due box on 02/12); 31 signature and date; 32 service facility; 33 billing provider.
330	
331	**Typical wording and number format.** 24F "is the total billed amount for each service line": dollars right-justified left of a vertical
332	line, cents to the right, no dollar sign, comma or decimal point. Shaded supplemental lines above each service line hold NDC and other data
333	and *do* use a decimal point (e.g., `1000.00`). Item 28 is the total of all 24F lines. Item 29 is money paid by patient or other payers.
334	
335	**Extraction traps.**
336	- `150 | 00` OCRs as `15000` ($15,000) or `150 00`; the decimal is implied by the box, not printed.
337	- 24A From/To with 24G = 10 means ten consecutive days on one line; one line is not one visit (NUCC: days must equal units).
338	- 24F is the line total (units times fee), not a per-unit rate; a per-unit figure must not be read from it.
339	- Item 14 is the injury/onset date and Item 31 is the signature date: neither is a service date.
340	- Item 28 can disagree with the sum of lines (data entry), or a claim may run to a second page with its own lines; sum lines in code and
341	  compare to Item 28 rather than trusting either.
342	- 10b "Auto accident? YES  Place (State) TX" is a useful corroborating checkbox and an OCR checkbox trap.
343	
344	**Sources.**
345	- NUCC, *1500 Health Insurance Claim Form Reference Instruction Manual for Form Version 02/12*, Version 8.0 (7/20): https://www.nucc.org/images/stories/PDF/1500_claim_form_instruction_manual_2020_07-v8.pdf — **opened** (text extracted locally). Takeaways: Items 14, 24A, 24F, 24G, 28, 29, 30 as stated above. Newer manual versions may exist (NUCC updates each July); field layout of the 02/12 form is unchanged.
346	- CMS MLN web-based training on the 1500 (lesson 5): https://cms.gov/Outreach-and-Education/MLN/WBT/MLN4462429-MLN-WBT-1500/1500/lesson05/02/index.html — search result, not opened.
347	
348	**Specimen (SYNTHETIC)** (rendered as the OCR text a scanned form tends to produce):
349	```
350	SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS
351	2. PATIENT'S NAME  OKONKWO-VALE, DELPHINE (SYNTHETIC)     3. DOB 03 | 09 | 1991  F
352	10b. AUTO ACCIDENT?  [X] YES  [ ] NO   PLACE (State) TX
353	14. DATE OF CURRENT ILLNESS  05 | 14 | 26   QUAL 431
354	21. ICD Ind 0   A. S13.4XXA   B. M54.12
355	24. A DATE(S) OF SERVICE        B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI
356	    060326  060326               11    98941              AB     85 | 00       1      SYN-NPI-0001
357	    060326  060326               11    97014              A      30 | 00       1      SYN-NPI-0001
358	    060126  060526               11    97010              A      45 | 00       3      SYN-NPI-0001
359	25. FED TAX ID  SYN-TIN-0001     28. TOTAL CHARGE  160 | 00     29. AMOUNT PAID  0 | 00
360	31. SIGNATURE  Dr. Corvin Ashdown, DC (SYNTHETIC)  DATE 06/30/26
361	33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142
362	```
363	(Line 3 groups three dates on one line with 3 units; Item 31 date is not a visit.)
364	
365	---
366	
367	## 9. UB-04 (CMS-1450) institutional claim
368	
369	**Fields (form locators).** FL 1 provider; 3a patient control number, 3b medical record number; **FL 4 type of bill** (4-digit with leading zero,
370	e.g. 0131 hospital outpatient); **FL 6 statement covers period** From/Through; 8-11 patient name and demographics; 12-13 admission date/hour;
371	14 admission type; 15 source; 17 discharge status; 31-36 occurrence codes and dates (accident-related codes); 39-41 value codes; **FL 42
372	revenue code** (4-digit, e.g. 0450 emergency room, 0320 x-ray, 0350 CT, 0610 MRI, 0250 pharmacy, 0636 drugs requiring detailed coding);
373	43 description (and NDC); **FL 44 HCPCS / accommodation rate / HIPPS code**; 45 service date; 46 service units; **47 total charges** (per
374	line, plus the total after the last line); **48 non-covered charges**; 50 payer; 67 principal diagnosis and 67A-Q other diagnoses; 72
375	external cause of injury codes; 74 principal procedure; 76 attending provider; 80 remarks.
376	
377	**Typical wording.** Line 23 carries revenue code `0001` = total charges (paper claims), with the **creation date** in FL 45 of that line.
378	"PAGE 1 OF 2" on multi-page claims. FL 44 holds a per-day accommodation rate on inpatient room lines (e.g., `1850.00`) and a HCPCS code on
379	outpatient lines.
380	
381	**Extraction traps.**
382	- Summing every amount in FL 47 includes the 0001 total line and doubles the bill.
383	- FL 44 on room lines is a **rate**; FL 47 on the same line is the charge (rate times days). Classic rate-vs-charge confusion (D-042).
384	- FL 45 on the total line is the claim creation date, not a service date.
385	- On multi-page claims the total appears only on the last page.
386	- FL 48 non-covered is not an adjustment by the provider; it is still a charge the payer did not cover.
387	- Payer guides disagree on whether Medicare's FL 47 total excludes non-covered charges; compute from lines and keep both.
388	
389	**Sources.**
390	- Rhode Island EOHHS, *UB-04 Instructions*: https://eohhs.ri.gov/sites/g/files/xkgbur226/files/2021-03/ub04_instructions.pdf — **opened** (text extracted). Takeaways: FL 4 four-digit with leading zero; FL 6 MMDDYY; FL 42 enter "0001" after last revenue code for the total in column 47 (paper only); FL 47 per-line total plus grand total; FL 48 amount not covered by primary payer.
391	- NUBC, *Official UB-04 Data Specifications Manual 2024* (table of contents; FL 47 p.180, FL 48 p.181): https://www.nubc.org/system/files/media/file/2024/04/TOC%20FOR%20NUBC%20SITE%202024%20UB04%20Manual.pdf — search summary; the full manual is licensed.
392	- McGraw-Hill chapter summary on FL 47/48 Medicare treatment: https://highered.mheducation.com/sites/0073520896/student_view0/chapter12/chapter_summary.html — search summary.
393	- Assumption: FL 44 title "HCPCS/Rate/HIPPS code" and the creation-date-on-line-23 convention are from my prior knowledge of the form; verify against the NUBC manual before quoting.
394	
395	**Specimen (SYNTHETIC).**
396	```
397	SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
398	1 Quillfeather Regional Medical Center (SYNTHETIC)   3a SYN-PCN-5521  3b SYN-ED-40417  4 0131
399	6 STATEMENT COVERS PERIOD  FROM 051426  THROUGH 051526
400	8 OKONKWO-VALE, DELPHINE (SYNTHETIC)   12 ADMISSION 051426  13 HR 23
401	31 OCCURRENCE  CODE 01  DATE 051426
402	42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
403	0450    EMERGENCY ROOM LVL 4          99284          051426        1          2,410.00
404	0350    CT CERVICAL SPINE W/O         72125          051526        1          3,185.00
405	0636    KETOROLAC INJ 15MG            J1885          051526        2             96.00
406	0250    PHARMACY GENERAL                             051526        1             38.50           38.50
407	0001    TOTAL                                        051826                   5,729.50           38.50
408	67 S16.1XXA   72 ECI V43.52XA   76 ATTENDING Dr. Ilario Fenwick (SYNTHETIC)
409	PAGE 1 OF 1
410	```
411	(The 0001 line repeats the sum; 051826 on that line is the creation date.)
412	
413	---
414	
415	## 10. Itemized provider ledger / statement
416	
417	**Fields.** Provider name and address; patient and account number; statement date; prior balance / balance forward; per line: date of
418	service, posting date, CPT or internal code, description, charge, payment, adjustment, running balance; totals block (total charges, total
419	payments, total adjustments, balance due); notes ("Account on LOP hold", "Sent to attorney").
420	
421	**Typical wording.** CMS's consumer guide names the parts as total charges, allowed amount, adjustments, insurance payment, patient payment,
422	and balance due/patient responsibility. Real ledgers add: "Contractual adj", "W/O", "Courtesy disc", "Atty reduction", "Bal fwd", credits in
423	parentheses or with a trailing minus, "Pmt - Ck #SYN-1043". Hospital consumer statements often show only a total; the itemized version must be
424	requested.
425	
426	**Extraction traps.**
427	- Running balance is cumulative; summing it multiplies the bill.
428	- Balance forward from a prior statement re-counts earlier charges if two statements are both in the packet.
429	- Posting date versus date of service: a charge posted 06/30 for a 06/03 visit.
430	- Reversals ("Void", "Reverse chg") paired with a re-bill on a later line.
431	- Fee-schedule summaries ("Office visit est. $150.00 per visit") look like charge lines but carry no date of service (rate, not charge).
432	- An attorney reduction recorded as an adjustment after settlement talks is a negotiated number, not a billed charge.
433	
434	**Sources.**
435	- CMS, *How to read your medical bill*: https://www.cms.gov/initiatives/your-patient-rights/medical-bill-rights/get-help/medical-bill-guides-resources/how-read-your-medical-bill — **opened**. Takeaway: standard parts are total charges, allowed amount, adjustments, insurance payment, patient payment, balance due.
436	- Resolve Medical Bills, *Itemized Hospital Bills*: https://www.resolvemedicalbills.com/guides/itemized-hospital-bill — search summary; itemized bill is sent only on request and lists dates, codes and per-service prices.
437	- Texas CPRC §18.001 (affidavit must include an itemized statement of the service and charge): https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm — search summary; see also research/texas-pi-notes.md.
438	
439	**Specimen (SYNTHETIC).**
440	```
441	SYNTHETIC RECORD
442	Larkspur Hollow Physical Therapy (SYNTHETIC)     ITEMIZED STATEMENT     Statement date: 07/31/2026
443	Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Acct: SYN-PT-2207   Financial class: LOP
444	DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE
445	05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00
446	06/10/26  06/11/26  97110  Therapeutic exercise x2       130.00                         340.00
447	06/10/26  06/11/26  97140  Manual therapy x1              70.00                         410.00
448	06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00
449	06/10/26  06/30/26  97140  Manual therapy x1 VOID        (70.00)                        375.00
450	06/10/26  06/30/26  97140  Manual therapy x1              70.00                         445.00
451	07/15/26  07/15/26  ADJ    Courtesy discount                                 45.00-     400.00
452	                     TOTAL CHARGES 445.00  TOTAL PMTS 0.00  TOTAL ADJ (45.00)  BALANCE DUE 400.00
453	Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection.
454	```
455	
456	---
457	
458	## 11. Explanation of Benefits (EOB) / remittance
459	
460	**Fields.** "THIS IS NOT A BILL"; member name and ID; claim number; provider; processed date; per service: date of service, service
461	description or code, amount billed, network discount / not covered, allowed amount, deductible, copay, coinsurance, plan paid, patient
462	responsibility ("You may owe"); CARC/RARC codes with group code (CO contractual obligation, PR patient responsibility, OA other).
463	
464	**Typical wording.** "Amount billed $410.00 - Network discount $162.40 = Allowed $247.60." "Deductible applied $100.00; Coinsurance 20%
465	$29.52; Plan paid $118.08; You may owe $129.52." "CO-45: charge exceeds fee schedule/maximum allowable." "PR-1 deductible, PR-2 coinsurance,
466	PR-3 copay."
467	
468	**Extraction traps.**
469	- The EOB's "amount billed" restates the provider's charge; counting both the bill and the EOB double counts.
470	- The processed/paid date is not a service date.
471	- "You may owe" is not what the patient paid; for Texas paid-or-incurred analysis (out of scope for the tool) the numbers matter, so keep them in notes with citations.
472	- Group code decides who owes: CO amounts are written off by a contracted provider, PR amounts are the patient's.
473	- Health-plan EOBs in a PI file often signal a subrogation lien by the health plan.
474	
475	**Sources.**
476	- Noridian JF-A, *MSP Calculation Examples on EOBs*: https://med.noridianmedicare.com/web/jfa/topics/msp/calculation-examples-eob — **opened**. Takeaway: billed minus total CARC amount equals allowed; allowed minus paid equals patient responsibility; examples with CARC CO-16 and a network discount.
477	- D3RX glossary, *CO (Contractual Obligation)*: https://d3rx.com/glossary/co-contractual-obligation — search summary; billed minus allowed is a contractual write-off the participating provider cannot balance-bill.
478	
479	**Specimen (SYNTHETIC).**
480	```
481	SYNTHETIC RECORD - THIS IS NOT A BILL
482	Bluebonnet Mutual Health Plan (SYNTHETIC)   Explanation of Benefits   Processed 07/22/2026
483	Member: Delphine Okonkwo-Vale (SYNTHETIC)  ID SYN-MBR-88231  Claim SYN-CLM-0091
484	Provider: Larkspur Hollow Physical Therapy (SYNTHETIC)
485	DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES
486	06/10/26  97110    130.00    52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45
487	06/10/26  97140     70.00    28.00     42.00    22.00    4.00    16.00      26.00     PR-1, PR-2, CO-45
488	06/10/26  97014     35.00    35.00      0.00     0.00    0.00     0.00       0.00     CO-97
489	TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00
490	CO-97: payment included in allowance for another service.
491	```
492	
493	---
494	
495	## 12. Letter of protection (LOP) and lien letters
496	
497	**Fields.** Law-firm letterhead; letter date; addressee (provider billing office); "Re:" block with client name, DOB, date of injury, sometimes
498	claim number; statement of representation; request that the provider treat and defer collection; promise to protect the bill from any
499	settlement or judgment; statement that the client remains responsible if the recovery is insufficient; request for records, itemized bill
500	and §18.001 affidavit; attorney signature; client acknowledgement and signature. Related documents: provider-side lien notice or
501	"Assignment and Authorization" signed by the patient at intake; hospital lien notice; reduction letters ("accept $X in full satisfaction").
502	
503	**Typical wording.** "Please be advised this firm represents ___ for injuries sustained on ___." "We will protect your outstanding charges
504	from any recovery." "This letter does not relieve our client of responsibility for the balance." "Please forward complete records and an
505	itemized statement of charges." Provider intake LOPs add: the provider will not send the account to collections while the claim is pending,
506	a continuing lien on any recovery, a direction to pay, and duties to notify the provider before funds are disbursed.
507	
508	**Extraction traps.**
509	- The LOP is not a medical record: its accident narrative is the attorney's, and its dates (letter date, injury date) are not encounters.
510	- Amounts in an LOP or lien notice ("current balance $4,860.00") are asserted totals without dates of service; never charges (D-019).
511	- Reduction letters state negotiated numbers; they belong in internal notes only.
512	- Sources disagree on whether "LOP" and "lien" are interchangeable; the tool should keep the document's own words.
513	
514	**Sources.**
515	- Jotform HIPAA intake packet with an embedded LOP (chiropractic, auto/slip-and-fall): https://hipaa.jotform.com/221364153684052 — **opened**. Takeaway: patient signs; provider defers payment and collections; direction to pay from settlement after fees and costs; continuing lien; patient remains responsible for any shortfall; notice duties before disbursement.
516	- ChartRequest, *Letters of Protection and Medical Liens*: https://www.chartrequest.com/articles/letters-of-protection-medical-records — search summary; argues LOP and lien are distinct.
517	- D Law Group, *What is a Letter of Protection or Personal Injury Lien?*: https://dlawgroup.com/letter-of-protection-personal-injury-lien/ — search summary; LOP can operate as a contract; patient owes the balance if the case is lost.
518	- Miller & Zois forms library (sample assignment/LOP and hold-harmless letters): https://www.millerandzois.com/professional-attorney-information-center/forms-and-letters-for-personal-injury-lawyers/ — search result, not opened.
519	- Assumption: Texas hospital liens (Property Code ch. 55) produce a separate filed notice; I did not open the statute for this card.
520	
521	**Specimen (SYNTHETIC).**
522	```
523	SYNTHETIC RECORD
524	Harrowgate & Vey, PLLC (SYNTHETIC)     100 Example Row, Suite 5, Fernhollow, TX     555-0177
525	July 2, 2026
526	Billing Department, Larkspur Hollow Physical Therapy (SYNTHETIC)
527	Re: Our client Delphine Okonkwo-Vale (SYNTHETIC); Date of injury 05/14/2026
528	This firm represents the above client for injuries from a motor vehicle collision. We ask
529	that you continue treatment and defer collection while the claim is pending. We will
530	protect your reasonable charges from any settlement or judgment. This letter does not
531	relieve our client of responsibility for the balance. Please send complete records and an
532	itemized statement of charges with a business-records affidavit.
533	Current balance per your office: $445.00.
534	/s/ Ottoline Vey, Attorney (SYNTHETIC)
535	Acknowledged: Delphine Okonkwo-Vale (SYNTHETIC)  07/02/2026
536	```
537	
538	---
539	
540	## 13. Spanish-language clinic note
541	
542	**Fields.** Same structure as an English clinic note under Spanish headings: *Fecha*; *Ficha de identificación* (name, age, sex);
543	*Motivo de consulta* (reason for visit, with duration); *Enfermedad actual* / *Padecimiento actual* (onset, course, current state);
544	*Antecedentes* (personales patológicos, no patológicos, quirúrgicos, alergias); *Signos vitales*; *Exploración física*; *Impresión
545	diagnóstica* / *Diagnóstico* (IDx); *Plan* (diagnostic: *estudios solicitados*; therapeutic: drug, dose, *vía oral (VO)*, frequency *c/8h*,
546	duration); *Pronóstico*; signature with *cédula profesional* (Mexico) or license.
547	
548	**Typical wording.** "Paciente femenina de 35 años que acude por dolor cervical de 3 días de evolución posterior a choque vehicular por
549	alcance." "Refiere dolor 7/10, irradiado a brazo derecho." "Niega pérdida del estado de alerta." "A la exploración física: contractura
550	paravertebral cervical, dolor a la palpación C5-C7." "IDx: Esguince cervical grado I." "Plan: naproxeno 500 mg VO c/12h por 7 días,
551	reposo relativo, cita en 1 semana." "Consulta: $650.00" (charge) vs "Costo por sesión de terapia: $400.00" (rate).
552	
553	**Extraction traps.**
554	- Day-first dates: `03/06/2026` is 3 June, not March 6. Written months: `14 de mayo de 2026`, `14-may-26`, `12-ago-2026`.
555	- `ago` is a month abbreviation (agosto); `hace 3 días` is "3 days ago" and is relative to the visit date, not a date.
556	- `refiere` (patient reports) and `niega` (denies) mark voice and negation; a translation must keep them.
557	- Decimal comma and dot thousands in Latin American notes (`$1.250,00`); US-based clinics usually print `$1,250.00`. Currency may be MXN.
558	- Mixed English/Spanish ("dolor de low back", "MRI solicitada") in border-region clinics.
559	- Per D-042 the excerpt is always the original Spanish; any translation is LLM output, labeled, judged, and never the cited excerpt.
560	
561	**Sources.**
562	- Huli Practice, *Ejemplo Formato Historia Clínica* (Mexican clinical-history template: motivo de consulta, enfermedad actual, antecedentes, exploración, diagnóstico, plan): https://blog.hulipractice.com/content/files/2023/08/Ejemplo-Formato-Historia-Cli-nica.pdf — search summary.
563	- Universitat de Barcelona, *Estructura de una entrevista diagnóstica - Motivo de consulta y enfermedad actual*: https://diposit.ub.edu/items/77b3b1a7-0b60-48b7-850d-224ebebcb4e5/full — search summary; enfermedad actual covers onset, evolution and current state; impresión diagnóstica is the clinician's, not asked of the patient.
564	- AgendaPro, *Formato de Historia Clínica*: https://agendapro.com/blog/wp-content/uploads/sites/2/2026/03/Formato-de-Historia-Clinica.pdf — search summary; plan split into estudios solicitados and treatment with drug, dose, frequency, duration.
565	- Assumption: common phrasing above ("acude por", "de N días de evolución", "refiere", "niega", "c/8h", "VO") is from general clinical Spanish usage; sources are teaching templates, not a terminology standard.
566	
567	**Specimen (SYNTHETIC).**
568	```
569	REGISTRO SINTÉTICO / SYNTHETIC RECORD
570	Clínica Familiar Los Almendros (SINTÉTICO)          Nota de consulta
571	Fecha: 17/05/2026
572	Paciente: Rosalba Itzel Marqueño (SINTÉTICO)   Edad: 41 años   Sexo: F
573	Motivo de consulta: Dolor de cuello de 3 días de evolución posterior a choque vehicular por alcance.
574	Enfermedad actual: Refiere dolor 7/10, irradiado a brazo derecho, que aumenta al girar la cabeza.
575	  Niega pérdida del estado de alerta. Niega antecedentes de dolor cervical.
576	Signos vitales: TA 130/85, FC 88.
577	Exploración física: Contractura paravertebral cervical. Dolor a la palpación C5-C7.
578	IDx: Esguince cervical grado I.
579	Plan: Naproxeno 500 mg VO c/12h por 7 días. Reposo relativo. Rx de columna cervical.
580	  Cita de control en 1 semana (24/05/2026).
581	Consulta: $650.00     Costo por sesión de terapia física: $400.00
582	Dra. Inés Valcárcel (SINTÉTICO)
583	```
584	(`17/05/2026` is 17 May. The $400.00 is a per-session rate, not a charge.)
585	
586	---
587	
588	## 14. Scanned and handwritten intake forms (and OCR failure modes)
589	
590	**Fields.** Patient demographics; date of injury; "How did the injury occur?" (free text); body diagram with marked pain areas; pain scale
591	0-10 (circled); symptom checkboxes (headache, dizziness, numbness); "Prior injuries / accidents / chiropractic care? Yes / No" with
592	explanation lines; current medications; employer and work status; "Who referred you?" (often an attorney); attorney name; insurance (auto,
593	health, MedPay/PIP); signature and date; sometimes an embedded LOP or assignment of benefits (section 12).
594	
595	**Typical wording.** Handwriting, abbreviations and the patient's own words: "rear ended at light, neck + back hurt", "no prior", "Dr. told
596	me to come", "pain 7-8". Stamps: "RECEIVED", "SCANNED", Bates numbers; fax header on every page.
597	
598	**OCR failure modes to reproduce.**
599	| Failure | Example (truth → OCR) | Consequence |
600	|---|---|---|
601	| Checkbox read as character or dropped | `[X] No` → `IX] No` or `No`; `[ ] Yes [X] No` → `Yes No` | Prior-injury answer lost or flipped - high stakes for pre-existing flags |
602	| Glyph confusion | `0/O`, `1/l/I/7`, `5/S`, `8/B`, `2/Z` | `05/14/26` → `O5/l4/26`; `$150` → `$I50` |
603	| Dropped or added decimal | `$1,250.00` → `$125000` or `$1,25000` | Amount off by 100x |
604	| Implied decimal (CMS-1500 boxes) | `150 \| 00` → `15000` | Same |
605	| Circled number | Pain scale `0 1 2 3 4 5 6 7 8 9 10` with 7 circled → all digits | Pain score lost |
606	| Strike-through and correction | `6/12` struck, `6/15` written above | Both dates extracted |
607	| Two-column / form-grid reading order | Left and right columns interleaved | Answers attached to the wrong question |
608	| Fax header and stamps | `11/03/2026 09:14 FROM: 555-0199 P.3/14` | Fax date read as a record date |
609	| Skew, blur, shadow, bleed-through | Phone photo of a form | Character error rate rises; Tesseract was weakest on blur and shadow in one study |
610	| Hidden or layered text in PDFs | Searchable PDF with an invisible text layer that differs from the image | Extracted text not visible to the human reviewer (D-042 hidden-text detection) |
611	
612	**Sources.**
613	- *Compact Multimodal Language Models as Robust OCR Alternatives for Noisy Textual Clinical Reports* (arXiv 2511.13523): https://arxiv.org/html/2511.13523v1 — **opened**. Takeaway: on smartphone photos of printed clinical reports, Tesseract scored CER 0.189, WER 0.276 and numeric accuracy 0.756, worse than neural pipelines and small multimodal models; Tesseract struggled most with blur and shadows. (Cite by arXiv number; authors not recorded here.)
614	- Tesseract OCR mailing list, thread on reading "X" checkboxes: https://groups.google.com/g/tesseract-ocr/c/r9mVUg76iE0 — search summary; out-of-the-box quality is medium; form jargon needs training; one user got better results at 150 dpi than 600 dpi.
615	- ImageToTable blog, *Why AI reads handwriting but misses a ticked box*: https://imagetotable.ai/blog/how-ai-reads-handwritten-forms-checkboxes-to-excel — search summary (vendor); generic OCR has no character for a tick and skips or garbles it.
616	- Assumption: glyph confusions in the table are the standard OCR confusion set; I found no Tesseract-specific measurement of them.
617	
618	**Specimen (SYNTHETIC)** — what the page shows, then what OCR returns:
619	```
620	SYNTHETIC RECORD
621	[PAGE IMAGE, described] Brightwater Spine & Wellness New Patient Intake. Handwritten in blue ink.
622	  Date of injury: 5/14/26.  How did it happen: "rear ended at red light, neck and back hurt."
623	  Pain today: 7 circled on a 0-10 line.  Prior injuries? [ ] Yes [X] No.
624	  Who referred you? "my lawyer - Vey".  Signed 5/29/26.  Fax header: 11/03/2026 09:14 P.2/9.
625	  Stamp: RECEIVED NOV 03 2026.
626	[OCR TEXT as extracted]
627	  11/O3/2026 O9:14 FROM 555-0199 P.2/9
628	  Date of injury: 5/l4/26
629	  How did it happen: rear ended at red Iight, neck and back hurt
630	  Pain today: 0 1 2 3 4 5 6 7 8 9 10
631	  Prior injuries? Yes IX] No
632	  Who referred you? my Iawyer - Vey
633	  Signed 5/29/2G
634	  RECEIVED NOV O3 2026
635	```
636	(The chosen pain score and the prior-injury answer are not recoverable from the OCR text alone; the item needs the page image and review.)
637	
638	---
639	
640	## 15. Product mapping and proposed packet mixes
641	
642	| Format | Main rule it exercises | Expected tool behavior |
643	|---|---|---|
644	| ED note | Dates (rollover), voice, pre-existing, hedges | Date = arrival; excerpt verbatim; PMH flag |
645	| PT note | Gaps vs cancellations; plan vs actual | Cancellation is not an encounter; reason shown verbatim |
646	| Chiro note + travel card | Cloned notes; checkbox OCR | Travel card rows need review when OCR-derived |
647	| Radiology | Hedge and prior-imaging language; three dates | Exam date used; "Comparison: prior" flagged |
648	| Op note | Indications ≠ causation; D:/T: dates | No causation inferred; surgery date used |
649	| Pharmacy log | Refills, reversals, three price columns | Reversed lines excluded; prices to notes unless charge wording |
650	| CMS-1500 | Implied decimal; date ranges; Item 14/31 dates | Code parses amounts; line sum vs Item 28 compared |
651	| UB-04 | 0001 total; FL 44 rate; creation date | Total line not summed; rate not a charge (D-042 guard) |
652	| Ledger | Running balance; voids; balance forward; fee schedule | Only dated charge lines counted; voids netted in code |
653	| EOB | Double count of billed; CO/PR | EOB amounts to notes, never added to charges |
654	| LOP / lien | Non-record narrative; asserted totals | No entries created; amounts to notes only (D-019) |
655	| Spanish note | Day-first dates; voice; translation labeling | Original excerpt; date convention suggestion (D-042) needs confirm |
656	| Scanned intake | OCR glyphs, checkboxes, fax/stamp dates | OCR-derived items always need review; page image beside text |
657	
658	**Proposed synthetic packet mixes** (for the library generator; all names invented):
659	1. *ER-only then gap*: ED note + UB-04 (with 0001 line) + ED-physician CMS-1500 + radiology report + fax headers.
660	2. *Chiro under LOP*: intake form (scanned) + LOP + 12 chiro daily notes with a travel card + CMS-1500 with a grouped date range + ledger with a void and a courtesy adjustment.
661	3. *PT with health insurance*: PT eval + daily notes with two cancellations + ledger + EOB (CO-45, PR-1, CO-97).
662	4. *Surgery*: MRI with prior comparison + op note with indications paragraph + surgeon/assistant/anesthesia/facility bills on one date.
663	5. *Spanish-speaking client*: Spanish clinic note with day-first dates (choose days ≤ 12 so the ambiguity is real) + rate and charge on the same page + pharmacy log with a reversed fill.
664	
665	---
666	
667	## 16. Assumptions, limits and gaps
668	
669	- **Search-summary sources.** Sources marked "search summary" were not opened; their takeaways come from the search tool's summary. The
670	  NUCC manual, RI UB-04 instructions, Noridian chiro and EOB pages, CMS bill guide, arXiv OCR paper and Jotform LOP packet were opened.
671	- **ACR report components.** The ACR page rendered only headings; the component list rests on secondary sources plus common practice.
672	- **UB-04 specifics from memory.** FL 44 accommodation-rate use, the creation date on line 23, and occurrence code 01 for accident are from
673	  my prior knowledge of the form; verify against the licensed NUBC manual before quoting them in the submission.
674	- **Payer variation.** CMS-1500 and UB-04 rules here are NUCC/NUBC and one Medicaid guide; commercial and auto carriers vary.
675	- **Pharmacy "charge".** Whether U&C, plan paid or patient paid is the recoverable amount is a legal question the tool does not decide.
676	- **Spanish phrasing** is drawn from Mexican and Spanish teaching templates; Central American and Caribbean usage may differ.
677	- **OCR figures** come from one paper on smartphone photos of printed reports, not handwritten forms; handwriting is likely worse.
678	- **No real data.** Every specimen is invented. Any resemblance of a name (e.g., Quillfeather, Larkspur Hollow, Harrowgate & Vey) to a real
679	  person, provider or firm is unintended.
680	
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:28.075Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-077 | head -60; echo ----; python3 tools/board.py show T-078 | head -60; grep -rn \"record-formats.md §\\|record-formats.md#\\|§15\\b\" --include=*.md research memory board/cards 2>/dev/null | grep -v \"^research/record-formats.md\" | head; ls evals/library | head -40",
 "description": "Show card ACs and references"
}
````

### User / tool · 2026-11-02T03:29:28.279Z

**tool result**
````
---
id: "T-077"
title: "Research: real-world PI case patterns for the multi-case library (v2)"
milestone: "M3"
role: "researcher"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:04Z"
updated_at: "2026-11-02T03:27:07Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T03:27:07Z"
rounds: 1
commits: ["bb26bf0"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-077-paralegal.md", "at": "2026-11-02T03:27:07Z"}
ac:
  - {"n": 1, "text": "research/case-library-sources-v2.md lists >= 12 case patterns from public real-world sources (court opinions, verdict reports, bar/CLE materials, published studies) with URL, date and the record features each implies (gaps, priors, causation language, billing shape, language)", "done": true, "evidence": "research/case-library-sources-v2.md: 17 patterns (P1-P17), each with URL, source date, read depth, 2-3 line summary and record features; none reuses v1 scenarios or sources (commit bb26bf0)"}
  - {"n": 2, "text": "Each pattern names which product feature it exercises (D-042 list) and is marked synthetic-safe (no real names, dates shifted)", "done": true, "evidence": "Each pattern has a 'D-042 / flags' line and a 'Synthetic-safety' line; global rules section (no real names, dates shifted to 2025-2027, facts recombined) + coverage map + 8 recombined packet proposals (lib08-lib15)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T03:11:11Z researcher: claimed
- 2026-11-02T03:15:00Z researcher: Searched/opened ~18 public sources (TX Sup Ct JLG 2015 + Central Oregon 2022 full text; NJ Rodriguez v Wal-Mart 2019 syllabus; Hills v Donis, Chiv v Figueroa, Gunn v McCoy, Steinkamp 2022, Flores 2003, Powell 2008, ElGhrably 2008, Rodriguez-Vera 2002, Bai&Anderson 2015, Fishbain 2003, FAIR Health, defense verdict 2024). Writing research/case-library-sources-v2.md.
- 2026-11-02T03:16:57Z researcher: AC 1 checked: research/case-library-sources-v2.md: 17 patterns (P1-P17), each with URL, source date, read depth, 2-3 line summary and record features; none reuses v1 scenarios or sources (commit bb26bf0)
- 2026-11-02T03:16:57Z researcher: AC 2 checked: Each pattern has a 'D-042 / flags' line and a 'Synthetic-safety' line; global rules section (no real names, dates shifted to 2025-2027, facts recombined) + coverage map + 8 recombined packet proposals (lib08-lib15)
- 2026-11-02T03:16:57Z researcher: moved in_progress -> in_review
- 2026-11-02T03:17:12Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-02T03:17:12Z orchestrator: Review batched with T-078 once it lands.
- 2026-11-02T03:27:07Z orchestrator: review paralegal-reviewer (claude-sonnet-5-5): changes — reviews/T-077-paralegal.md; round 1; findings:
    - [major] Denylist for v2 real names is not in place, and the doc's list is incomplete and unsafe as written — fix: Researcher adds an explicit 'Denylist additions' block to the v2 doc and updates validate_library.py (case-insensitive) before T-079 starts. Include distinctive tokens: JLG, Pechero, Zapata, Guevara, Ferrer, Donis, Chiv, Figueroa, Broussard, 'Central Oregon', McCoy, Miskell, Wal-
    - [minor] 'Record features' mix source-derived and inferred content, and two sources do not support the record shape at all — fix: Tag each Record-features line 'from source' or 'our inference'. Give Hampton a full citation (court, district, docket or WL cite) or replace it with a retrievable source. Say plainly that P4 and P17 support only the scenario theme.
    - [minor] Hills v. Donis 'withdrawn and substituted 2021-02-11' is not supported by the cited page — fix: Either cite the substituted opinion with its own date and URL, or delete the sentence. Re-read the opinion itself, since the doc admits it was not opened.
    - [minor] P7/lib12 (defense IME) and P16 assume documents a demand-stage packet usually does not contain — fix: Label lib12 as litigation-stage, or recast it as a carrier records-review/peer-review letter or a treating-provider FCE note. Say in lib13 that the PCP note arrived from a records request.
    - [minor] P5 claim that provider ledgers 'match the six categories exactly' overstates the opinion — fix: Reword to 'ledger columns derived from items 1-4 and 6; item 5 (carrier contracts) is a separate document the packet may reference but not reproduce'.
    - [minor] Three D-042 features are credited to packets whose premises do not carry them — fix: Add a 'must contain' column to the packet table, e.g. lib09: one form dated 03/06/2026 day-first plus 14/05/2026; lib12: at least 4 credibility sentences (2 clean, 2 mixed) across 3 dates; lib13: a surgical estimate line.
- 2026-11-02T03:27:07Z researcher: claimed

## Handoff
What changed: research/case-library-sources-v2.md, 17 PI record patterns (TX Sup Ct JLG 2015, Central Oregon 2022, Guevara 2007, Gunn 2018; Tex App Hills v Donis, Chiv v Figueroa 2025, Hampton 2017; NJ Rodriguez v Wal-Mart 2019; studies on copy-forward notes, laterality errors, illegible handwriting, interpreter errors, missed mTBI, Waddell, chargemaster markup, ambulance mileage; a 2023 defense verdict), coverage map vs D-042, 8 recombined packet proposals. How verified: JLG and Central Oregon opinions and the Rodriguez syllabus read in full via pdftotext; the rest are summary-level and marked per pattern. What's left: build packets lib08-lib15 (qa/researcher card); add real case names (Garza, Broussard, Rodriguez, etc.) to the validate_library denylist first. Surprised me: no public source documents hidden-text PDFs or DD/MM dates in PI files, so those two are labeled assumptions.

----
---
id: "T-078"
title: "Research: medical-record and billing document formats for synthetic packets"
milestone: "M3"
role: "researcher"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T03:27:07Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T03:27:07Z"
rounds: 1
commits: ["1193f8a"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-078-paralegal.md", "at": "2026-11-02T03:27:07Z"}
ac:
  - {"n": 1, "text": "research/record-formats.md describes ER note, PT/chiro daily note, imaging report, op note, pharmacy log, CMS-1500, UB-04, itemized ledger, EOB, LOP/lien letter, Spanish-language clinic note, scanned/handwritten intake: fields, typical wording, source URL for each", "done": true, "evidence": "research/record-formats.md §2-14: 13 formats (ED, PT, chiro, radiology, op note, pharmacy, CMS-1500, UB-04, ledger, EOB, LOP/lien, Spanish note, scanned intake+OCR), each with Fields, Typical wording (charge/rate/adjustment), Extraction traps, Sources (URL, opened vs search summary); commit 1193f8a"}
  - {"n": 2, "text": "Each format has a short fully synthetic specimen labeled SYNTHETIC", "done": true, "evidence": "13 fenced specimens, each headed SYNTHETIC RECORD / REGISTRO SINTÉTICO; invented names, SYN- identifiers, 555-01xx phones; regex scan found no SSN/10-digit/phone patterns"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T03:11:11Z researcher: claimed
- 2026-11-02T03:11:29Z researcher: Started: web research on 12 record formats (CMS/NUCC, ACR, SOAP, EOB, LOP, OCR). Output research/record-formats.md.
- 2026-11-02T03:14:43Z researcher: Sources gathered: NUCC 1500 manual v8.0 (opened, text extracted), RI Medicaid UB-04 instructions (opened), Noridian chiro + EOB pages (opened), CMS how-to-read-bill (opened), arXiv 2511.13523 OCR (opened), Jotform LOP packet (opened); ACR/EMRA/op-note/Spanish/pharmacy from search snippets (marked). Writing record-formats.md.
- 2026-11-02T03:18:51Z researcher: AC 1 checked: research/record-formats.md §2-14: 13 formats (ED, PT, chiro, radiology, op note, pharmacy, CMS-1500, UB-04, ledger, EOB, LOP/lien, Spanish note, scanned intake+OCR), each with Fields, Typical wording (charge/rate/adjustment), Extraction traps, Sources (URL, opened vs search summary); commit 1193f8a
- 2026-11-02T03:18:51Z researcher: AC 2 checked: 13 fenced specimens, each headed SYNTHETIC RECORD / REGISTRO SINTÉTICO; invented names, SYN- identifiers, 555-01xx phones; regex scan found no SSN/10-digit/phone patterns
- 2026-11-02T03:18:51Z researcher: moved in_progress -> in_review
- 2026-11-02T03:19:13Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-02T03:27:07Z orchestrator: review paralegal-reviewer (claude-sonnet-5-5): changes — reviews/T-078-paralegal.md; round 1; findings:
    - [major] CMS-1500 line 3 violates the NUCC grouping rule the doc quotes, and the chiro travel card does not support it — fix: Make line 3 consistent, e.g. 060126 060526 with 5 units at $15 = $75 and a travel card with HP on all 5 days (total becomes 190), or split into three single-date lines. If the mismatch is deliberate, label it 'DELIBERATE: units != days' and state the expected tool outp
    - [major] The two headline traps are in the prose but not in the specimens — fix: Add an inpatient UB-04 specimen with e.g. '0120 ROOM & BOARD SEMI-PVT  [FL44] 1,850.00  [FL45] 051526  [FL46] 3  [FL47] 5,550.00' and the 0001 total recomputed. Add a second CMS-1500 specimen in degraded OCR form, e.g. '8500', '30 00', '16000', plus the clean boxed form.
    - [major] Formats that the T-077 packets need are missing: EMS run report, ambulance invoice, 1.18.001 affidavit/cover page, treater narrative letter — fix: Add four short sections in the same shape (fields, wording, traps, SYNTHETIC specimen): EMS patient-care report, ambulance invoice (base + mileage), CPRC 18.001 business-records/billing affidavit with its cover page, treating-provider narr
    - [minor] PT specimen bills 3 timed units for 35 timed minutes, contradicting the 8-minute rule the doc cites — fix: Either change minutes (e.g. 97110 25 min, 97140 13 min = 38 min = 3 units), or add a line 'units per AMA per-code method; CMS total-time method would give 2'.
    - [minor] The Delphine specimens do not agree with each other in several places — fix: Fix or annotate each as DELIBERATE with its expected flag. For (4) add a note that the packet tests ledger vs EOB mismatch and expects a billing-analysis flag.
    - [minor] UB-04 occurrence-code wording is too narrow, and two UB-04 conventions are stated as fact in the trap lists while still unverified — fix: Say 'accident codes 01 to 06; extraction treats any as an accident date'; vary the code across packets; add '(unverified)' next to the creation-date lines in sections 1.1 and 9.
    - [minor] The Spanish specimen does not exercise the day-first trap, and 'no provider or payer name is real' is asserted without a check — fix: Change one Spanish date to e.g. 03/06/2026 with a stated truth; soften the header claim or run a name-collision search on every provider, payer, firm and clinician name and record the result.
- 2026-11-02T03:27:07Z researcher: claimed

## Handoff
What changed: research/record-formats.md (679 lines): cross-cutting traps (non-service dates, money formats incl. CMS-1500 implied decimal, one-visit-many-bills), 13 format sections with fields, wording, traps, sources, SYNTHETIC specimen; §15 product mapping + 5 packet mixes; §16 assumptions. · How verified: NUCC 1500 manual v8.0 and RI UB-04 instructions text-extracted and read (Items 14/24A/24F/24G/28/29/30; FL 4/6/42-48); Noridian chiro + EOB, CMS bill guide, arXiv 2511.13523, Jotform LOP opened; others marked 'search summary'; specimen arithmetic hand-checked (1500 total 160.00, UB-04 5,729.50, ledger 400.00, EOB 104.00); identifier regex scan clean. · What's left: UB-04 FL44 rate/line-23 creation date/occurrence code 01 are from prior knowledge (flagged §16, verify vs NUBC); ACR II.B body not readable; library generator (qa/backend) should adopt §15 mixes. · Surprised me: CMS-1500 money boxes carry no decimal point (150|00 -> OCR 15000), and UB-04 FL44 holds a per-day rate on the same line as the charge, a ready-made D-042 rate-vs-charge trap.

board/cards/T-078.md:19:  - {"n": 1, "text": "research/record-formats.md describes ER note, PT/chiro daily note, imaging report, op note, pharmacy log, CMS-1500, UB-04, itemized ledger, EOB, LOP/lien letter, Spanish-language clinic note, scanned/handwritten intake: fields, typical wording, source URL for each", "done": true, "evidence": "research/record-formats.md §2-14: 13 formats (ED, PT, chiro, radiology, op note, pharmacy, CMS-1500, UB-04, ledger, EOB, LOP/lien, Spanish note, scanned intake+OCR), each with Fields, Typical wording (charge/rate/adjustment), Extraction traps, Sources (URL, opened vs search summary); commit 1193f8a"}
board/cards/T-078.md:29:- 2026-11-02T03:18:51Z researcher: AC 1 checked: research/record-formats.md §2-14: 13 formats (ED, PT, chiro, radiology, op note, pharmacy, CMS-1500, UB-04, ledger, EOB, LOP/lien, Spanish note, scanned intake+OCR), each with Fields, Typical wording (charge/rate/adjustment), Extraction traps, Sources (URL, opened vs search summary); commit 1193f8a
board/cards/T-078.md:44:What changed: research/record-formats.md (679 lines): cross-cutting traps (non-service dates, money formats incl. CMS-1500 implied decimal, one-visit-many-bills), 13 format sections with fields, wording, traps, sources, SYNTHETIC specimen; §15 product mapping + 5 packet mixes; §16 assumptions. · How verified: NUCC 1500 manual v8.0 and RI UB-04 instructions text-extracted and read (Items 14/24A/24F/24G/28/29/30; FL 4/6/42-48); Noridian chiro + EOB, CMS bill guide, arXiv 2511.13523, Jotform LOP opened; others marked 'search summary'; specimen arithmetic hand-checked (1500 total 160.00, UB-04 5,729.50, ledger 400.00, EOB 104.00); identifier regex scan clean. · What's left: UB-04 FL44 rate/line-23 creation date/occurrence code 01 are from prior knowledge (flagged §16, verify vs NUBC); ACR II.B body not readable; library generator (qa/backend) should adopt §15 mixes. · Surprised me: CMS-1500 money boxes carry no decimal point (150|00 -> OCR 15000), and UB-04 FL44 holds a per-day rate on the same line as the charge, a ready-made D-042 rate-vs-charge trap.
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
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:30.603Z

**tool call — ToolSearch**
````
{
 "query": "select:WebSearch,WebFetch",
 "max_results": 2
}
````

### User / tool · 2026-11-02T03:29:30.612Z

**tool result**
````
[tool_reference]
[tool_reference]
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:33.376Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B note T-077 --agent researcher --text \"Round 2 started: denylist (case-insensitive + self-test), record-feature tags, Hills/Hampton citations, stage + must-contain + formats columns, P5/P6 rewording.\" && $B note T-078 --agent researcher --text \"Round 2 started: CMS-1500 grouping fix + OCR rendering, inpatient UB-04 rate line, 4+ new formats (EMS PCR, ambulance invoice, 18.001 affidavit, narrative letter), occurrence codes 01-06, cross-specimen table, specimen check script.\" && python3 research/validate_library.py | tail -3",
 "description": "Note round 2 start and run current validator"
}
````

### User / tool · 2026-11-02T03:29:33.682Z

**tool result**
````
noted on T-077
noted on T-078
golden OK: 17 cases (16 synthetic), 85 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (7 packets, 26 denylist terms)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:36.880Z

**tool call — WebSearch**
````
{
 "query": "\"Hampton v. Miskell\" Tex. App. 2017 reconstructionist",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:37.481Z

**tool call — WebSearch**
````
{
 "query": "\"Hills v. Donis\" 14-18-00566-CV opinion",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:38.287Z

**tool call — WebSearch**
````
{
 "query": "UB-04 occurrence codes 01 accident medical coverage 02 no-fault 03 tort liability 04 employment 05 06 crime victim",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:39.281Z

**tool call — WebSearch**
````
{
 "query": "Medicare ambulance claims A0427 A0425 origin destination modifier SH fractional mileage tenth of a mile claims processing manual chapter 15",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:40.180Z

**tool call — WebSearch**
````
{
 "query": "NEMSIS data dictionary eTimes PSAP call unit arrived on scene patient care report refusal eDisposition",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:40.958Z

**tool call — WebSearch**
````
{
 "query": "personal injury treating physician narrative report \"reasonable medical probability\" causation prognosis future medical template",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:29:41.682Z

**tool result**
````
Web search results for query: ""Hampton v. Miskell" Tex. App. 2017 reconstructionist"

Links: [{"title":"txcourts.gov","url":"https://txcourts.gov/media/1458770/230861pc.pdf"},{"title":"Court of Civil Appeals of Texas, 2015","url":"https://hallapproved.com/tx/cases/appeals/2015/4296576/"},{"title":"Library Record","url":"https://texasranger.pastperfectonline.com/library/0815FE60-62DC-4CCD-9B0F-631143337450"},{"title":"muse.jhu.edu","url":"https://muse.jhu.edu/article/418809/pdf"},{"title":"[Clipping: Panel wants Hampton complaints heard: Texas Supreme Court asked to appoint master] Part: 4 of 4","url":"https://texashistory.unt.edu/ark:/67531/metadc1584447/m1/4/"},{"title":"[Clipping: Panel wants Hampton complaints heard: Texas Supreme Court asked to appoint master] Part: 4 of 4","url":"https://texashistory.unt.edu/ark:/67531/metadc1584447/m1/4/?rotate=270"},{"title":"hampton wade iii 1818 1902","url":"https://experts.illinois.edu/en/publications/hampton-wade-iii-1818-1902/"},{"title":"theclio.com","url":"https://theclio.com/entry/25503"},{"title":"The Younger Doctrine: Reconstructing Reconstruction","url":"https://scholarspace.manoa.hawaii.edu/handle/10125/35269?mode=full"},{"title":"Court of Civil Appeals of Texas, 2017","url":"https://hallapproved.com/tx/cases/appeals/2017/4373066/"},{"title":"Court of Civil Appeals of Texas, 2015","url":"https://hallapproved.com/tx/cases/appeals/2015/4293130/"},{"title":"Supreme Court of Texas Blog","url":"https://data.scotxblog.com/scotx/no/02-1020"},{"title":"Court of Civil Appeals of Texas, 2015","url":"https://hallapproved.com/tx/cases/appeals/2015/4296967/"},{"title":"Court of Civil Appeals of Texas, 2014","url":"https://hallapproved.com/tx/cases/appeals/2014/3070286/"},{"title":"Court of Civil Appeals of Texas, 2015","url":"https://hallapproved.com/tx/cases/appeals/2015/4293642/"},{"title":"Court of Civil Appeals of Texas, 2017","url":"https://hallapproved.com/tx/cases/appeals/2017/4416468/"},{"title":"Court of Civil Appeals of Texas, 2015","url":"https://hallapproved.com/tx/cases/appeals/2015/4281819/"},{"title":"Court of Civil Appeals of Texas, 2017","url":"https://hallapproved.com/tx/cases/appeals/2017/4387833/"}]

The search didn't turn up any case called "Hampton v. Miskell" from Texas in 2017, and nothing in the results mentions a reconstructionist.

The results did include a few unrelated Texas Hampton matters. One is a 2024 Texas Supreme Court decision, Hampton v. Thome, 687 S.W.3d 496 (Tex. 2024), which is cited in a court filing about a remanded case. Others are a Texas Supreme Court docket for Glenn T. Hampton v. Thomas M. Henderson and a 1989 newspaper clipping about Hampton complaints. None of these match the 2017 case you described.

The party name may be slightly different, or the case may not be indexed in this search tool. Searching a Texas appellate database such as CourtListener or the Texas courts' case search with the names and year, or with the term "reconstructionist" in a different context (such as an expert witness in an accident or forensic case), might locate it.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:29:43.579Z

**tool result**
````
Web search results for query: ""Hills v. Donis" 14-18-00566-CV opinion"

Links: [{"title":"Supreme Court of Texas Blog","url":"https://data.scotxblog.com/scotx/no/21-0287"},{"title":"Supreme Court of Texas Blog","url":"https://data.scotxblog.com/scotx/no/04-0409"},{"title":"Court of Civil Appeals of Texas, 2019","url":"https://hallapproved.com/tx/cases/appeals/2019/4678736/"},{"title":"Supreme Court of Texas Blog","url":"https://data.scotxblog.com/scotx/no/14-0643"},{"title":"Supreme Court of Texas Blog","url":"https://data.scotxblog.com/scotx/no/06-0610"},{"title":"hills vs ty","url":"https://www.digest.ph/decisions/hills-vs-ty"},{"title":"supreme court of texas orders 03 15 2019","url":"https://www.txcourts.gov/media/1443744/supreme-court-of-texas-orders-03-15-2019.pdf"},{"title":"march 15 2019","url":"https://txcourts.gov/supreme/orders-opinions/2019/march/march-15-2019/"},{"title":"september 28 2018","url":"https://txcourts.gov/supreme/orders-opinions/2018/september/september-28-2018/"},{"title":"december 20 2019","url":"https://www.txcourts.gov/supreme/orders-opinions/2019/december/december-20-2019"},{"title":"Learn About the Law","url":"https://caselaw.findlaw.com/court/us-5th-circuit/2038498.html"},{"title":"supreme court of texas orders 09 28 2018","url":"https://www.txcourts.gov/media/1442438/supreme-court-of-texas-orders-09-28-2018.pdf"},{"title":"Texas Court of Appeals, Fifth District Decisions 2014","url":"https://law.justia.com/cases/texas/fifth-court-of-appeals/2014/"},{"title":"SC RL 12092016","url":"https://judicial.alabama.gov/docs/SC/SC_RL_12092016.pdf"},{"title":"Texas Court of Appeals, Fifth District Decisions 2016","url":"https://law.justia.com/cases/texas/fifth-court-of-appeals/2016/?page=3"}]

The search didn't return the appellate opinion text, but it did find the case record. The matter is at the Fourteenth Court of Appeals as docket 14-18-00566-CV, and the Texas Supreme Court blog lists a related petition under No. 21-0287. That entry shows Carlos Donis, Calixto Donis, Victor Matamoros, Saira Castellanos, individually and as next friend of S.D., a minor as petitioners, with Eboni Ivory Hills as respondent. So the caption runs Donis v. Hills, with Hills as the appellee, not "Hills v. Donis" as you wrote it.

The blog credits Honorable Margaret "Meg" Poissant as the opinion author and identifies the trial court as the 11th District Court, County: Harris. A separate entry lists a Court of Appeals outcome field for a different, older case, so I can't confirm the disposition of this one from these results. The Supreme Court entry also shows a Motion for Extension of Time to File Petition for Review filed dated 2021-03-29.

To get the full opinion, check the Fourteenth Court of Appeals or Texas Judiciary websites, or the Texas Supreme Court docket for 21-0287.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:29:46.630Z

**tool result**
````
Web search results for query: "UB-04 occurrence codes 01 accident medical coverage 02 no-fault 03 tort liability 04 employment 05 06 crime victim"

Links: [{"title":"HL7 v2.4 Vocabulary","url":"https://build.fhir.org/ig/frankoemig/hl7.v2.terminology.v24/CodeSystem-nubc-OccurrenceCode-cs.json.html"},{"title":"Facility Billing","url":"https://d3rx.com/guides/ub-04-billing-explained"},{"title":"ub 04 condition code occurence code and","url":"https://cms1500claimform.blogspot.com/2016/07/ub-04-condition-code-occurence-code-and.html"},{"title":"2. IMPORTANT","url":"https://pt.slideshare.net/karna.indian/cms-1450-ub04-overview-presentation"},{"title":"ub04 occurrence codes","url":"https://medicalbillingrcm.com/ub04-occurrence-codes"},{"title":"support.drchrono.com","url":"https://support.drchrono.com/home/pdfexport/id/668c7d1b5487e4c1a708b306"},{"title":"UB04/CMS1450 Revenue Codes - Group 06","url":"https://www.findacode.com/ub04-revenue/ub04-revenue-cms-1450-codes-06-group.html"},{"title":"occurance codes medical billing","url":"https://www.brainbound.blog/occurance-codes-medical-billing"},{"title":"medicaid.gov","url":"https://medicaid.gov/tmsis/dataguide/data-elements/cip002145"},{"title":"UB04/CMS1450 Revenue Codes - Group 00","url":"https://www.findacode.com/ub04-revenue/ub04-revenue-cms-1450-codes-00-group.html"},{"title":"by Find-A-Codeā¢","url":"https://www.findacode.com/articles/ub-04-revenue-codes-obscure-still-part-game-37466.html"},{"title":"HL7 Terminology","url":"https://terminology.hl7.org/1.0.0/CodeSystem-v2-0350.ttl.html"},{"title":"omb.report","url":"https://omb.report/icr/202502-0920-016/doc/153487001.pdf"},{"title":"An official website of the United States government","url":"https://www.medicaid.gov/tmsis/dataguide/data-elements/cot002077/"},{"title":"HL7 Terminology (THO)","url":"https://terminology.hl7.org/en/NamingSystem-v2-0350.html"},{"title":"n.classweekly.com","url":"https://n.classweekly.com/icr/202505-0920-007/doc/157600601.pdf"},{"title":"UB04 Boxes 31-34 - What are occurrence codes and how do I add them to an institutional claim?","url":"https://owlknowledgeteststuff.drchrono.com/help/5485315415451"}]

The search confirmed some UB-04 occurrence code descriptions, but not all six you asked about. Codes 02 (no-fault) and 06 (crime victim) didn't appear in any result.

- **01 (auto accident):** The most commonly recognized Occurrence Codes by BCBSTX are listed below: Occurrence Code Definition 01 Auto Accident.
- **03 (accident/tort liability):** An HL7 vocabulary entry lists code 03 as "Accident/tort liability". The result gave only that name, not a fuller definition.
- **04 (employment-related):** Listed as "Accident – Employment Related" by one payer.
- **05 (other accident):** Also listed by that payer, as "Other Accident".
- **02 and 06:** No result gave their descriptions. Code 06 appears only in a Medicaid data guide, which requires it to be from a valid list without defining it, so I can't confirm the "crime victim" label from these results.

Where occurrence codes go: On the CMS-1450 form, also known as the UB-04, occurrence codes and their associated dates are located in Form Locators 31 through 34. One source also says that requires OC 01 or 02 with date of accident/injury, which suggests 02 is also accident-related, but that is a payer rule rather than a code definition.

One source is unreliable on this point. A patient-billing guide describes "01: Accident date. When an injury from an accident occurred." as a revenue code, but revenue codes are a separate 4-digit system, so that source is mixing the two.

For the official full list, the NUBC's UB-04 Data Specifications Manual is the authority, and the UB-04 Data Specifications Manual with the codes is available by subscription from NUBC. If you need the exact wording for 02, 03, and 06, check that manual or a payer's published code list.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:29:46.763Z

**tool result**
````
Web search results for query: "Medicare ambulance claims A0427 A0425 origin destination modifier SH fractional mileage tenth of a mile claims processing manual chapter 15"

Links: [{"title":"ambulance services","url":"https://assets.guidewell.com/m/328cacfcefaa039d/original/ambulance-services.pdf"},{"title":"truli providers payment policies ambulance services","url":"https://files.guidewell.com/m/776e376fc918b64d/original/truli-providers-payment-policies-ambulance-services.pdf"},{"title":"Commercial General Coding 069 Ambulance Services 10.24.23","url":"https://bluecrossmn.com/sites/default/files/DAM/2023-10/Commercial-General-Coding-069-Ambulance-Services-10.24.23.pdf"},{"title":"Pabau GO app","url":"https://pabau.com/procedure-codes/hcpcs-code-a0426/"},{"title":"www.priorityhealth.com","url":"https://www.priorityhealth.com/provider/manual/services/medical/ambulance"},{"title":"Medicare Carrier and Outpatient Files: Identifying Ambulance Services","url":"https://resdac.org/articles/medicare-carrier-and-outpatient-files-identifying-ambulance-services"},{"title":"Ambulance services","url":"https://sitecore-cd-prod.priorityhealth.com/provider/manual/services/medical/ambulance"},{"title":"webarchive.library.unt.edu","url":"https://webarchive.library.unt.edu/web/20080921135800/http://www.cms.hhs.gov/manuals/downloads/clm104c15.pdf"},{"title":"webarchive.library.unt.edu","url":"https://webarchive.library.unt.edu/web/20090109015334/http://www.cms.hhs.gov/manuals/downloads/clm104c15.pdf"},{"title":"Ambulance%20Services%20and%20required%20Modifiers LA","url":"https://ch.aetnabetterhealth.com/content/dam/aetna/medicaid/louisiana/providers/pdf/Ambulance%20Services%20and%20required%20Modifiers_LA.pdf"},{"title":"Origin/Destination Ambulance Modifiers","url":"https://www.csscoperations.com/palmetto/jmb.nsf/DIDC/8L9HK55061~Specialties~Ambulance"},{"title":"Ambulance billing guide","url":"https://medicare.fcso.com/billing/ambulance-billing-guide"},{"title":"Land Ambulance: No Transport and Non-Covered Transports","url":"https://dmepdac.com/palmetto/rr.nsf/DIDC/8EEMJP4858~Specialties~Ambulance"},{"title":"webharvest.gov","url":"https://webharvest.gov/peth04/20041024215805/http://www.cms.hhs.gov/manuals/104_claims/clm104c15.pdf"},{"title":"UHCCP Ambulance Policy (R0123)","url":"https://green-gateway.uhcprovider.com/content/dam/provider/docs/public/policies/medicaid-comm-plan-reimbursement/UHCCP-Ambulance-Policy-(R0123).pdf"},{"title":"Ambulance Mileage","url":"https://med.noridianmedicare.com/web/jeb/specialties/ambulance/mileage"},{"title":"10-144 Ch. 101","url":"https://www.maine.gov/sos/sites/maine.gov.sos/files/inline-files/c3s005 LUP 10.12.2020 (ACK).docx"},{"title":"One-Stop Solution For Revenue Cycle Management Services","url":"https://practolytics.com/blog/cpt-codes-and-modifiers-of-ambulance-transportation/"},{"title":"ambulance billing guidelines cpt codes","url":"https://www.codingahead.com/ambulance-billing-guidelines-cpt-codes"}]

I ran one search. It confirmed the general framework for these codes but did not turn up the specific rules you asked about: the SH modifier or fractional-mile rounding for ground mileage.

**What the results support:**
- Ground mileage is billed under A0425, described as ground mileage, per statute mile. Ambulance codes A0425-A0436 must be reported with modifiers that indicate pick-up origins and destinations for each ambulance trip provided.
- Origin/destination modifiers are two-character pairs. The first position of the modifier code is the point of origin and the second position is the destination. Missing modifiers lead to denial: ambulance codes missing origin and destination modifiers will be denied.
- Chapter 15 of the Medicare Claims Processing Manual is the governing reference. One copy, an archived 2008 version, is in the results, but the excerpt returned covers only the table of contents and general coverage notes, not the mileage or modifier sections.
- For an example of a pair, one payer's guide says that when transporting a Medicare patient from their residence (R) to hospital (H), report the appropriate ambulance transport HCPCS code and mileage code A0425 with modifiers RH.

**On mileage rounding:** One Medicare contractor (Noridian) says that for air ambulance codes, suppliers must report mileage rounded up to nearest whole number mile, and that if mileage not indicated, defaults "0.1". That rule is stated for the air codes (A0435/A0436), not clearly for ground A0425, so it doesn't answer your fractional-mileage question for ground transport.

**Gaps:** None of the results mention the SH modifier or a tenth-of-a-mile rule for ground A0425. For those, check the current Chapter 15 PDF on CMS.gov, especially its mileage section, and your MAC's ambulance billing article.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:29:47.852Z

**tool result**
````
Web search results for query: "personal injury treating physician narrative report "reasonable medical probability" causation prognosis future medical template"

Links: [{"title":"Templates Personal Injury Narrative Medical Report Request","url":"https://ezel.ai/templates/narrative-medical-report-request/"},{"title":"25 January 2012","url":"https://mondaq.com/unitedstates/healthcare/160998/tips-for-attorneys-direct-exam-of-a-treating-physician"},{"title":"dklaw.com","url":"https://dklaw.com/?p=109538"},{"title":"tn.gov","url":"https://TN.GOV/content/dam/tn/workforce/documents/Forms/c32.pdf"},{"title":"Accident Medical Documentation: Expert Analysis to Prove Causation","url":"https://www.daeryunlaw.com/es/practices/detail/accident-medical-documentation"},{"title":"Accident Medical Documentation: Expert Analysis to Prove Causation","url":"https://www.daeryunlaw.com/ar/practices/detail/accident-medical-documentation"},{"title":"Accident Medical Documentation: Expert Analysis to Prove Causation","url":"https://www.daeryunlaw.com/ja/practices/detail/accident-medical-documentation"},{"title":"Accident Medical Documentation: Expert Analysis to Prove Causation","url":"https://www.daeryunlaw.com/ru/practices/detail/accident-medical-documentation"},{"title":"Medical Documentation Best Practices for Personal Injury Cases: Provider Guide","url":"https://www.liensstudios.com/blog/medical-documentation-personal-injury-cases"},{"title":"Templates Medical Malpractice Chapter 74 Expert Report and Curriculum Vitae - Texas Health Care Liability Claim","url":"https://ezel.ai/templates/certificate-of-merit/tx"}]

The search turned up practical templates and guidance for treating-physician narrative reports in personal injury cases. I did not verify the legal rules against primary sources.

**Template structure.** An ezel.ai request-and-report template asks the physician to state whether the incident caused or substantially contributed to each diagnosed condition, whether the patient has reached maximum medical improvement, and what further treatment is recommended. Its checklist covers records reviewed, diagnoses with ICD-10 codes, treatment summary, causation, prognosis and future needs, permanency, work restrictions, and signature. It also says opinions should be framed as held to a reasonable degree of medical probability or certainty (Patient identifying information, summary of records reviewed, history, physical examination findings, diagnoses with ICD-10 codes, treatment summary; the sample narrative puts causation, prognosis (expected recovery and permanency), and future treatment (description and estimated costs) under separate headings).

**Direct-exam topics.** A Mondaq tips piece for attorneys lists the questions to put to a treating physician on future care, including the future medical care the plaintiff will require and the cost of that care, and closes with a causation question framed in reasonable medical probability.

**Causation language.** Sources warn against weak phrasing. One checklist flags "possibly related to accident" as creating doubt, and distinguishes reasonable medical certainty from reasonable medical probability (use appropriate level of certainty based on evidence). A law-firm piece says the causation statement should establish that the accident was the direct and proximate cause of the plaintiff's injuries.

**Jurisdiction.** A law-firm page says that in California, Evidence Code 801.1 now requires expert medical testimony to meet the "reasonable degree of medical probability" standard. This is a secondary, marketing-oriented source, so confirm the statute's current text before relying on it.

**Caveat.** The Texas result (ezel.ai Chapter 74 template) is a medical malpractice expert report, not a personal injury treating-physician narrative, so use it only as a loose structural reference. The Tennessee Form C-32 is a workers' compensation form, not a personal injury template.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:29:49.514Z

**tool result**
````
Web search results for query: "NEMSIS data dictionary eTimes PSAP call unit arrived on scene patient care report refusal eDisposition"

Links: [{"title":"Extended Data Definitions","url":"https://NEMSIS.ORG/media/nemsis_v3/release-3.5.0/DataDictionary/PDFHTML/EMSDEMSTATE/Extended Data Definitions.pdf"},{"title":"SIREN Elite Report Writer Fields","url":"https://www.healthvermont.gov/sites/default/files/DEPRIP.SIREN_.RW_Fields.February%202020.pdf"},{"title":"DDeTimesFieldsNew 4 9 2018","url":"https://portal.ct.gov/-/media/Departments-and-Agencies/DPH/dph/ems/pdf/CEMSTARS/DDeTimesFieldsNew-4-9-2018.pdf"},{"title":"pmc.ncbi.nlm.nih.gov","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC10491424/table/T3"},{"title":"Source | ihe.pcc.pcs#current:PCC - Paramedicine Care Summary (PCS) (v4.0.1) |","url":"https://www.fhir.org/guides/stats2/valueset-ihe.pcc.pcs-nemsis.statushistorysubtype.vs.html"},{"title":"Extended Data Definitions v3 Final","url":"https://NEMSIS.ORG/wp-content/uploads/2018/09/Extended-Data-Definitions_v3_Final.pdf"},{"title":"dphhs.mt.gov","url":"https://dphhs.mt.gov/assets/publichealth/EMSTS/EMS/Disposition.pdf"},{"title":"NASEMSO EMS Time Duration Definitions 6 18 24","url":"https://nemsis.org/wp-content/uploads/2024/06/NASEMSO_EMS_Time_Duration_Definitions-6-18-24.pdf"},{"title":"NEMSIS Fields Crosswalk","url":"https://support.angeltrack.com/hubfs/NemsisCrosswalk.htm"},{"title":"schema summary","url":"https://nemsis.org/media/nemsis_v3/3.4.0.160713CP2/DataDictionary/APIs/CADFrameDoc/schemas/eResponse_v3_xsd/schema-summary.html"},{"title":"NEMSIS v3.5 Requisite National Elements EMS DataSet","url":"https://nemsis.org/wp-content/uploads/2025/01/NEMSIS-v3.5-Requisite-National-Elements-EMS-DataSet.pdf"},{"title":"www.alabamapublichealth.gov","url":"https://www.alabamapublichealth.gov/ems/assets/2024reporting.guidelines.with.rules.pdf"},{"title":"Extended%20Data%20Definitions tcm1221 662868","url":"https://mn.gov/oems/assets/Extended%20Data%20Definitions_tcm1221-662868.pdf"},{"title":"NEMSIS Patient and Incident Disposition","url":"https://kbems.ky.gov:443/KSTARS/Documents/NEMSIS-Patient-and-Incident-Disposition.pdf"},{"title":"NEMSIS v3 National Elements","url":"https://test.nemsis.org/wp-content/uploads/2019/10/NEMSIS-v3-National-Elements.pdf"},{"title":"GA Cassie Longhart Medic Training v3.5 Incident Disposition Changes Sharable","url":"https://nemsis.org/wp-content/uploads/2022/10/GA-Cassie-Longhart-Medic-Training-v3.5-Incident-Disposition-Changes-Sharable.pdf"},{"title":"NEMSIS Flowchart Pronouncement DOA w Resucitation","url":"https://kbems.ky.gov:443/KSTARS/Documents/NEMSIS-Flowchart-Pronouncement-DOA-w-Resucitation.pdf"},{"title":"NEMSISV3.4.0RequisiteNationalElements EMSDataSet05 01 2015","url":"https://test.nemsis.org/wp-content/uploads/2023/11/NEMSISV3.4.0RequisiteNationalElements-EMSDataSet05-01-2015.pdf"}]

The search turned up the core NEMSIS v3 timestamp fields and the refusal-related disposition fields, but not a single page that ties them together for refusals.

**Timestamp fields:** The NEMSIS v3 times group is eTimes. eTimes.01 is the PSAP call time, eTimes.05 is en route, eTimes.06 is arrival on scene, eTimes.07 is arrival at the patient, eTimes.09 is departure from scene, and eTimes.11 is arrival at destination. The Unit Arrived on Scene field, eTimes.06, records the date and time the responding unit reached the scene. Connecticut's guidance says the en route, on-scene, arrived-at-patient, left-scene, and destination fields are expected if disposition includes treat/transport. That suggests they may not be expected for a pure refusal, but I didn't confirm this in the official dictionary, so check the element's usage pattern for your version.

**Refusal fields:** The refusal reason lives in eDisposition.31, and the crew disposition is eDisposition.29. A Montana document lists eDisposition.31 as the Reason for refusal/release, and a Kentucky flowchart pairs it with eDisposition.29 as the Crew Disposition. Georgia's training material also presents it as the reason for refusal during an incident. The NEMSIS v3.4 and v3.5 value sets differ, so match your state's version.

**Interval calculations:** NASEMSO's time-interval definitions compute Total Unit Response Time as eTimes.06 minus eTimes.03, and the unit's scene time as eTimes.09 minus eTimes.06, using eTimes.13 if eTimes.09 is null. Both are relevant when a refusal is recorded at the scene.

**Cancelled-on-scene edge case:** The NASEMSO extended definitions describe a unit that arrived on scene but was canceled by other on-scene unit(s)/agency(s) prior to initiating any patient contact. This is a separate situation from a patient refusal.

**Caveats:** I ran one search and did not open the full NEMSIS 3.5 data dictionary, so the exact required/expected rules for eTimes and eDisposition in refusal scenarios are unverified. The NEMSIS Extended Data Definitions PDF (v3.5.0, linked in the results) and the NEMSIS v3.5 Requisite National Elements list would be the next places to confirm them.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:55.043Z

**tool call — WebFetch**
````
{
 "url": "https://data.scotxblog.com/scotx/no/21-0287",
 "prompt": "Give all details: parties, court of appeals case number, CoA opinion date(s), CoA disposition, petition disposition and dates, any mention of rehearing, withdrawn or substituted opinion. Quote dates exactly."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:55.743Z

**tool call — WebSearch**
````
{
 "query": "\"Hills v. Donis\" 2021 substituted memorandum opinion rehearing Fourteenth Court of Appeals",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:29:57.452Z

**tool call — WebFetch**
````
{
 "url": "https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm",
 "prompt": "Quote verbatim Sec. 18.001 subsections (a)-(e) and (d-1) deadline language, and Sec. 18.002 (a) and (b-1) affidavit form wording in full (the form text). Also give the amendment history notes (Acts year) at the end of 18.001 and 18.002."
}
````

### User / tool · 2026-11-02T03:30:01.240Z

**tool result**
````
Web search results for query: ""Hills v. Donis" 2021 substituted memorandum opinion rehearing Fourteenth Court of Appeals"

Links: [{"title":"july 23 2021","url":"https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/"},{"title":"Supreme Court of Texas Blog","url":"https://data.scotxblog.com/scotx/no/21-0287"},{"title":"txcourts.gov","url":"https://txcourts.gov/All_Archived_Documents/14thCOA/Case/Opinions/091400/opinions.html"},{"title":"www.txcourts.gov","url":"https://www.txcourts.gov/media/1448530/180794jmnt.pdf"},{"title":"Court of Civil Appeals of Texas, 2021","url":"https://hallapproved.com/tx/cases/appeals/2021/4854547/"},{"title":"Court of Civil Appeals of Texas, 2021","url":"https://hallapproved.com/tx/cases/appeals/2021/5307772/"},{"title":"www2.ca3.uscourts.gov","url":"https://www2.ca3.uscourts.gov/opinarch/192532npo.pdf"},{"title":"www.supremecourt.gov","url":"https://www.supremecourt.gov/DocketPDF/17/17-9138/78706/20190108141615515_00000001.pdf"},{"title":"SUBSTITUTE MAJORITY OPINION ON REHEARING","url":"https://www.leagle.com/decision/intxco20201229519"},{"title":"Supreme Court of Texas Blog","url":"https://data.scotxblog.com/scotx/no/21-0765"},{"title":"Court of Civil Appeals of Texas, 2021","url":"https://hallapproved.com/tx/cases/appeals/2021/4870674/"},{"title":"Court of Civil Appeals of Texas, 2021","url":"https://hallapproved.com/tx/cases/appeals/2021/4904496/"},{"title":"www.txcourts.gov","url":"https://www.txcourts.gov/All_Archived_Documents/14thCOA/Case/Opinions/060800/opinions.html"},{"title":"Court of Civil Appeals of Texas, 2021","url":"https://hallapproved.com/tx/cases/appeals/2021/4856382/"},{"title":"Court of Civil Appeals of Texas, 2020","url":"https://hallapproved.com/tx/cases/appeals/2020/4735379/"},{"title":"Court of Civil Appeals of Texas, 2021","url":"https://hallapproved.com/tx/cases/appeals/2021/4900749/"},{"title":"Court of Civil Appeals of Texas, 2022","url":"https://hallapproved.com/tx/cases/appeals/2022/6352572/"},{"title":"Court of Civil Appeals of Texas, 2020","url":"https://hallapproved.com/tx/cases/appeals/2020/4744961/"},{"title":"ON REHEARING","url":"https://www.leagle.com/decision/intxco20191011779"}]

The search turned up the Texas Supreme Court docket for this case, but nothing that confirms the rehearing or substituted-opinion history you asked about.

- **Case:** CARLOS DONIS, CALIXTO DONIS, VICTOR MATAMOROS, SAIRA CASTELLANOS, INDIVIDUALLY AND AS NEXT FRIEND OF S.D., A MINOR v. EBONI IVORY HILLS; from Harris County; 14th Court of Appeals District (14-18-00566-CV, ___ SW3d ___, 02-11-21). The Fourteenth Court opinion is dated February 11, 2021, and the reporter citation is still blank.
- **Supreme Court history:** The petition for review was filed May 28, 2021, and Petition for Review disposed Denied on July 23, 2021. The docket lists it as No. 21-0287, while the July 23 orders list shows the same parties under No. 21-0290.
- **Gap:** None of the results say whether the February 11, 2021 opinion was a substituted opinion or whether it came from a rehearing motion. The 14th Court's rehearing and substitution orders in the results involve other cases. To confirm the history, check the Fourteenth Court's opinion page for No. 14-18-00566-CV or the case's docket entries on txcourts.gov.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:30:01.425Z

**tool result**
````
The web page you provided is a navigation index for the Texas Constitution and Statutes site. It lists the codes but doesn't include the text of any section, so I can't quote Sec. 18.001 or 18.002, the affidavit form wording, or the amendment history notes.

To get this language, you can open the Civil Practice and Remedies Code on the official Texas Constitution and Statutes site and navigate to Chapter 18. If you paste the text of those sections here, I can help you with them.
````

### User / tool · 2026-11-02T03:30:02.040Z

**tool result**
````
**Case:** No. 21-0287, *Carlos Donis, Calixto Donis, Victor Matamoros, Saira Castellanos, Individually and as Next Friend of S.D., a Minor v. Eboni Ivory Hills*

**Parties and counsel:**
- **Petitioners:** Calixto Donis, Saira Castellanos, Victor Matamoros, S.D., and Carlos Donis, all represented by Mr. Kevin Albert Murray.
- **Respondent:** Eboni Ivory Hills, represented by Mr. Robert T. Owen, Mr. Levon G. Hovnatanian, and Mr. William Osborn.
- **Other Interested Party:** Aaliyah Desiree Hills, represented by Mr. William Osborn.

**Court of Appeals:**
- **Court:** 14th Court of Appeals
- **Case number:** 14-18-00566-CV
- **Opinion author:** Honorable Margaret "Meg" Poissant
- **Disposition:** The page lists the outcome below as "Aff/Pt and Rev & Ren/Pt."
- **Opinion date(s):** Not listed on the page.
- **Rehearing, withdrawn, or substituted opinion:** None mentioned.

**Trial court:** 11th District Court, Harris County, Honorable Kristin Brauchle Hawkins, Trial Docket 2016-38471.

**Petition for review timeline:**
- 2021-03-29: Motion for Extension of Time to File Petition for Review filed.
- 2021-04-07: That motion was disposed of with the notation "Filed document is struck by the Court."
- 2021-04-09: Motion for Extension of Time to File Petition for Review filed.
- 2021-04-12: That motion was disposed of as "Filing granted."
- 2021-04-28: Second Motion for Extension of Time to File Petition for Review filed.
- 2021-04-29: That motion was disposed of as "Filing granted."
- 2021-05-28: Petition for Review filed by Petitioner.
- 2021-06-15: Response Waiver filed.
- 2021-06-22: Case forwarded to Court.
- 2021-07-23: Petition for Review disposed of as "Denied." The page states: "The Court denied review of the petition on July 23, 2021. File Closed."
- 2021-08-26: Notice sent to Court of Appeals.

**Opinions:** The page states, "The Court has not issued any opinions in this case."
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:30:08.595Z

**tool call — WebFetch**
````
{
 "url": "https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14",
 "prompt": "List all case events and opinions with dates: opinion issued, memorandum opinion, motion for rehearing, opinion withdrawn, substitute opinion, judgment. Give any document links (URLs) for opinions."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:30:09.408Z

**tool call — WebFetch**
````
{
 "url": "https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/",
 "prompt": "Find the entry for Donis v. Hills (21-0287 or 21-0290) and quote it exactly, including the court of appeals number, SW3d cite and date."
}
````

### User / tool · 2026-11-02T03:30:16.278Z

**tool result**
````
The matching entry is **21-0287**, not 21-0290. The 21-0290 entry is *In the Interest of M.A.G. and Z.A.G.*

Exact text, in segments under the 125-character limit:

- Case number and caption, first part: "CARLOS DONIS, CALIXTO DONIS, VICTOR MATAMOROS, SAIRA CASTELLANOS, INDIVIDUALLY AND AS NEXT FRIEND OF S.D., A MINOR v."
- Second part: "EBONI IVORY HILLS; from Harris County; 14th Court of Appeals District"
- Citation: "(14-18-00566-CV, ___ SW3d ___, 02-11-21)"

The entry appears under "The following petitions for review are denied." The SW3d cite is blank on the page ("___ SW3d ___"), so no reporter citation is listed. The date 02-11-21 is the court of appeals' decision date.
````

### User / tool · 2026-11-02T03:30:19.252Z

**tool result**
````
**Opinions, judgments, and rehearing events (Case 14-18-00566-CV)**

**01/14/2020: Judgment issued and memorandum opinion issued**
- Disposition: "REVERSED AND RENDERED"
- Memorandum opinion: https://search.txcourts.gov/SearchMedia.aspx?MediaVersionID=89e7de08-8bf9-4d91-bc7b-d11c8382be00&coa=coa14&DT=Opinion&MediaID=dafbcc12-ad41-41f8-99d5-cc0126ac8e95
- Notice (memorandum opinion issued): https://search.txcourts.gov/SearchMedia.aspx?MediaVersionID=2214ad29-8fb3-40be-b799-6d0167e6cb7b&coa=coa14&DT=MEM+OPINION+ISSD&MediaID=f2ac6a11-9150-4d30-bcbd-b5efb83cc112
- Judgment: https://search.txcourts.gov/SearchMedia.aspx?MediaVersionID=0af1b754-17fc-4bf6-8fad-1bd53693d24f&coa=coa14&DT=Judgment&MediaID=908c9575-d1ac-4aff-adca-3a9a80ca1267

**01/29/2020: Motion for rehearing filed**
- Motion: https://search.txcourts.gov/SearchMedia.aspx?MediaVersionID=2d7468ee-11fc-4f8f-a227-6f0c3a17b689&coa=coa14&DT=Motion&MediaID=8ceec994-42c9-4275-84d9-3cad9b0b606c

**02/11/2021: Motion for rehearing denied; judgment issued; new memorandum opinion issued; prior opinion withdrawn**
- Disposition: "AFFIRMED IN PART AND REVERSED AND RENDERED IN PART"
- Memorandum opinion: https://search.txcourts.gov/SearchMedia.aspx?MediaVersionID=9465fa85-40de-430f-8ab4-c1988996ca8f&coa=coa14&DT=Opinion&MediaID=9d2c62af-0658-4981-9b02-0314b4102f6f
- Notice (memorandum opinion issued): https://search.txcourts.gov/SearchMedia.aspx?MediaVersionID=1ba309f2-1dbc-4a0d-9ac4-3b6b2b9fd920&coa=coa14&DT=MEM+OPINION+ISSD&MediaID=292e70b4-c416-4ba8-820c-87616d3c1293
- Judgment: https://search.txcourts.gov/SearchMedia.aspx?MediaVersionID=49896dab-1b6f-473f-9f32-c899c8e07ef9&coa=coa14&DT=Judgment&MediaID=7c826a6e-c036-4f27-bad9-d786c7f98b99

**Substitute opinion:** None listed.

Notes:
- The page does not list a link for the withdrawn opinion.
- The page lists no separate motion for rehearing after the 02/11/2021 opinion. A "Motion for rehearing was not filed" entry appears on 02/26/2021.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:30:27.651Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dl && cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dl && curl -sL -A \"Mozilla/5.0\" -o hills2021.pdf \"https://search.txcourts.gov/SearchMedia.aspx?MediaVersionID=9465fa85-40de-430f-8ab4-c1988996ca8f&coa=coa14&DT=Opinion&MediaID=9d2c62af-0658-4981-9b02-0314b4102f6f\" && file hills2021.pdf && pdftotext -layout hills2021.pdf hills2021.txt && wc -l hills2021.txt && head -60 hills2021.txt && grep -n -i \"18.001\\|conclusory\\|withdraw\\|radicul\\|displacement\\|caused\" hills2021.txt | head -40",
 "description": "Download and extract Hills 2021 opinion"
}
````

### User / tool · 2026-11-02T03:30:28.884Z

**tool result**
````
hills2021.pdf: PDF document, version 1.7, 13 pages
     416 hills2021.txt
Motion Denied; Memorandum Opinion of January 14, 2020 Withdrawn;
Reversed and Rendered in Part, Affirmed in Part, and Substitute
Memorandum Opinion filed February 11, 2021.




                                      In The

                     Fourteenth Court of Appeals

                               NO. 14-18-00566-CV

                       EBONI IVORY HILLS, Appellant
                                         V.

  CARLOS DONIS, CALIXTO DONIS, VICTOR MATAMOROS, SAIRA
  CASTELLANOS, INDIVIDUALLY AND AS NEXT FRIEND OF S.D., A
                     MINOR, Appellees

                    On Appeal from the 11th District Court
                            Harris County, Texas
                      Trial Court Cause No. 2016-38471

                  SUBSTITUTE MEMORANDUM OPINION

      Appellees’ motion for rehearing is denied. We withdraw our memorandum
opinion of January 14, 2020 and issue this substitute memorandum opinion.

      This is a personal injury case arising from an automobile accident. On
appeal, Eboni Ivory Hills challenges the trial court’s judgment in favor of appellees
Carlos Donis, Calixto Donis, Victor Matamoros, and Saira Castellanos, both in her
individual capacity and as next friend of S.D., a minor (collectively the “Donis
Parties”). Hills asserts the Donis Parties failed to present legally and factually
sufficient evidence to support their negligence claims. For the reasons set forth
below, we reverse and render, in part, and affirm, in part.

                                I.    BACKGROUND

        On July 6, 2014, Carlos Donis was driving his car south on I-45 in Houston,
Texas, around 4:00 p.m. It was raining and the freeway was congested with traffic.
Calixto Donis, Victor Matamoros, Saira Castellanos, and S.D. were passengers in
Carlos’s car. Richard Morehouse was driving his vehicle behind Carlos’s vehicle.
There was standing water on the highway, which caused Carlos to slow down or
stop.

        Hills was entering I-45 behind a vehicle that blocked her view of Carlos’s
and Morehouse’s vehicles. According to her testimony, a vehicle in front of Hills
“jolt[ed] into traffic,” and Hills applied her brakes, but did not have enough time to
stop before hitting the back-right-side of Morehouse’s car, and then ricocheting
into the back of Carlos’s vehicle.

        Hills’s car was totaled. Morehouse’s vehicle sustained substantial damage,
but there was minimal damage to the rear of Carlos’s vehicle. No airbags deployed
in any of the vehicles.

        After the accident, none of the parties involved requested or left in an
ambulance. No one went to the emergency room. No one was bleeding, had
bruises, scrapes, cuts, or broken bones.      Carlos drove his car home with all
passengers.
1:Motion Denied; Memorandum Opinion of January 14, 2020 Withdrawn;
27:      Appellees’ motion for rehearing is denied. We withdraw our memorandum
44:There was standing water on the highway, which caused Carlos to slow down or
76:      The Donis Parties maintain that the accident caused substantial soft tissue
84:radiculitis, lumbar radiculitis, thoracalgia, cervical intervertebral disc (“IVD”)
85:displacement without myelopathy, lumbar IVD displacement without myelopathy,
93:included diagnoses of cervical radiculitis, lumbar radiculitis, thoracalgia, cervical
94:IVD displacement without myelopathy, lumbar IVD displacement without
95:myelopathy, thoracic IVD displacement without myelopathy, cervical discogenic
106:radiculitis, lumbar radiculitis, thoracalgia, cervical IVD displacement without
107:myelopathy, lumbar IVD displacement without myelopathy, cervical discogenic
114:evidence in the amount of $5,960.00 included diagnoses of cervical radiculitis,
115:lumbar radiculitis, ankle pain, ankle contusion, hip pain, muscle spasms, post-
155:       occurring on July 6, 2014 proximately caused the soft tissue injuries
160:       accident occurring on July 6, 2014 proximately caused the soft tissue
215:that the conduct of the defendant caused an event and that this event caused the
220:generated the expenses and ‘that all the conditions were caused by the accident.’”
252:compensation—i.e., cervical IVD displacement, lumbar IVD displacement,
253:thoracic IVD displacement, cervical discogenic pain, lumbar discogenic pain, disc
255:cervical radiculitis, lumbar radiculitis, thoracalgia, and lumbalgia—are neither
259:prove medical causation of disc herniations and radiculopathy); see also Sanchez v.
262:lumbar spine, back spasms, lumbar radiculopathy). As such, the claims of Carlos,
281:disc herniations and lumbar radiculopathy were “solely and directly” caused by an
288:S.W.3d 390, 397 (Tex. 2011) (Section 18.001 is “purely procedural, providing for
290:medical expenses.”). “Section 18.001 affidavits do not, however, establish the
296:nor that all the conditions were caused by the accident.” Guevara, 247 S.W.3d at
310:evidence of causation because his opinions are conclusory. See id. An expert’s
311:bare proclamation that this one event caused another is not enough to establish
313:why the breach caused the injury based on the facts presented.” Jelinek v. Casas,
323:burden to prove that their damages were proximately caused by the automobile
327:injuries (i.e., cervical IVD displacement, lumbar IVD displacement, thoracic IVD
331:displacement, cervical discogenic pain, lumbar discogenic pain, disc herniation,
333:radiculitis, lumbar radiculitis, thoracalgia, and lumbalgia). We conclude expert
352:diagnoses of cervical radiculitis, lumbar radiculitis, ankle pain, ankle contusion,
375:accident and Saira’s diagnoses for cervical radiculitis and lumbar radiculitis, her
394:diagnosed injuries of Carlos, Calixto, and Victor were caused by the automobile
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:30:33.058Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dl && sed -n 140,175p hills2021.txt; echo ....; sed -n 300,416p hills2021.txt",
 "description": "Read Hills opinion holdings"
}
````

### User / tool · 2026-11-02T03:30:33.161Z

**tool result**
````
       Saira Castellanos, individually — $5,960.00
       Saira Castellanos, as next friend of S.D. — $285.00
The total award for past medical expenses for all parties was $145,460.00.

       Also, on May 18, 2018, the trial court filed Findings of Fact and
Conclusions of Law.2 Hills filed a motion for new trial, which was denied. This
appeal timely followed.

                                       II.    ANALYSIS

       Hills presents two issues on appeal:

       1)    Whether the evidence is legally sufficient to support the district
       court’s judgment where the appellees failed to present any competent
       expert testimony demonstrating that the automobile accident
       occurring on July 6, 2014 proximately caused the soft tissue injuries
       about which [the Donis Parties] complain.
       2)     Whether the evidence is factually sufficient to support the
       district court’s judgment where the appellees failed to present any
       competent expert testimony demonstrating that the automobile
       accident occurring on July 6, 2014 proximately caused the soft tissue
       injuries about which [the Donis Parties] complain.

only asking for the medical bills in this case. They’re not looking for lost wages. They’re not
looking for pain and suffering and mental anguish. They just want to be compensated and made
whole for their medical bills paid.”
       2
          The record, however, contains only the second page of the trial court’s Findings of Fact
and Conclusions of Law. The Donis Parties filed a Motion to Correct Clerical Error by
Judgment Nunc Pro Tunc on April 22, 2019, which was denied by the trial court. Appellees
attached to their appellate brief, as an exhibit, the alleged missing page. This page, however, is
not part of the appellate record and, as such, is not properly before us for consideration.

                                                5
A.    STANDARD OF REVIEW

....
                                         9
      Additionally, to the extent Carlos, Calixto, and Victor point to Dr. Jeffrey
Reuben’s opinions (set forth in various letters or contained in statements within the
billing records) as evidence of causation, the opinions expressed in Dr. Rueben’s
letters constitute no evidence upon which the trial court’s judgment could be based.
To constitute competent evidence of causation, a medical expert’s opinion must be
reliable and rest in reasonable medical probability. Crye, 907 S.W.2d at 500.
“This rule applies whether the opinion is expressed in testimony or in a medical
record, as the need to avoid opinions based on speculation and conjecture is
identical in both situations.”     Id.     Dr. Reuben’s opinions are not competent
evidence of causation because his opinions are conclusory. See id. An expert’s
bare proclamation that this one event caused another is not enough to establish
causation; “the expert must go further and explain, to a reasonable degree, how and
why the breach caused the injury based on the facts presented.” Jelinek v. Casas,
328 S.W.3d 526, 539–40 (Tex. 2010). Dr. Reuben’s letters do not provide the
necessary link between the diagnosed injuries and the motor vehicle accident.
Absent this link, Dr. Reuben’s letters are unreliable speculation, which does not
constitute evidence in support of the trial court’s judgment. See id. at 532 (“When
the evidence offered to prove a vital fact is so weak as to do no more than create a
mere surmise or suspicion of its existence, the evidence is no more than a scintilla
and, in legal effect, is no evidence.”).

      Under these circumstances, as plaintiffs, Carlos, Calixto, and Victor bore the
burden to prove that their damages were proximately caused by the automobile
accident. See Doe v. Boys Clubs of Greater Dallas, Inc., 907 S.W.2d 472, 477
(Tex. 1995). It is undisputed that the Donis Parties presented no expert testimony
establishing that the automobile accident was a proximate cause of their diagnosed
injuries (i.e., cervical IVD displacement, lumbar IVD displacement, thoracic IVD


                                            10
displacement, cervical discogenic pain, lumbar discogenic pain, disc herniation,
cervical disc disorder, lumbar disc disorder, thoracic disc disorder, cervical
radiculitis, lumbar radiculitis, thoracalgia, and lumbalgia). We conclude expert
medical testimony was required to establish a nexus between the accident and
Carlos, Calixto, and Victor’s claimed injuries, and none was provided. As such,
the trial court erred in granting judgment in favor of Carlos, Calixto, and Victor.
Because Carlos, Calixto, and Victor did not meet their burden of proof to show
causation, we have no choice but to conclude the evidence is legally insufficient.4

       As such, we sustain Hills’s first issue as it relates to Carlos, Calixto, and
Victor.

       2.     SAIRA, INDIVIDUALLY AND AS NEXT FRIEND OF S.D., A MINOR

       We do find, however, the evidence legally and factually sufficient as to
Saira, individually and as next friend of S.D., a minor.

       Saira testified that she was in the front passenger seat, wearing a seat belt,
and had her “feet up” at the time of the accident. She testified that her ankle was
injured in the accident and that she received treatment to address her ankle injury.
Medical bills admitted into evidence in the amount of $5,960.00 included
diagnoses of cervical radiculitis, lumbar radiculitis, ankle pain, ankle contusion,
hip pain, muscle spasms, post-traumatic headache, numbness, and tingling. Saira’s
treatment (July through September 2014) included applying physical therapy,
massages, and ultrasound to her ankle, as well as therapy and massages to her
cervical spine.



       4
         Because we have sustained Hills’s legal sufficiency challenge as to Carlos, Calixto, and
Victor, we find it unnecessary to address Hills’s remaining, second issue regarding factual
sufficiency. See Tex. R. App. P. 47 .1.

                                               11
      With respect to S.D., Saira testified that S.D. was in the back seat in a car
seat at the time of the accident. She took S.D. with her to the chiropractor to be
evaluated because “she was at the accident at the time, and I thought it was the
right thing to do.” The medical bill admitted into evidence for S.D. demonstrates
she was evaluated on one occasion, July 9, 2014, treated with a cold/hot pack, and
diagnosed with lumbalgia and muscle spasms.         The bill is in the amount of
$285.00.

      While the evidence presented does not support a causal link between the
accident and Saira’s diagnoses for cervical radiculitis and lumbar radiculitis, her
testimony is sufficient to support a proximate cause finding as to all physical
conditions associated with her ankle injury. See Guevara, 247 S.W.3d at 666. Her
description of the accident as to herself and S.D., including the temporal proximity
between the accident and the injuries, is sufficient to “enable a layperson to
determine the causal relationship with reasonable probability.” See Kelley, 2017
WL 421980, at *2. Consequently, no expert testimony was needed to establish a
causal connection between the accident and Saira’s and S.D.’s claimed injuries.
Guevara, 247 S.W.3d at 669–70. Thus, the awards to Saira, individually and as
next friend of S.D., are supported by legally and factually sufficient evidence. We
also conclude the awards are not so against the great weight and preponderance of
the evidence as to be manifestly unjust.

      Hills’s first and second issues are overruled as they relate to Saira,
individually and as next friend of S.D., a minor.

                                III.   CONCLUSION

      Because we conclude expert medical testimony was required to establish the
diagnosed injuries of Carlos, Calixto, and Victor were caused by the automobile
accident, and because they presented no such evidence, we reverse this part of the
                                           12
trial court’s judgment and render that Carlos, Calixto, and Victor take nothing from
Hills.

         Additionally, we conclude no medical testimony was required to establish
the diagnosed injuries of Saira, individually and as next friend of S.D., a minor;
thus, we affirm this part of the trial court’s judgment.




                                        /s/    Margaret “Meg” Poissant
                                               Justice


Panel consists of Justices Wise, Jewell, and Poissant.




                                          13
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:30:37.573Z

**tool call — WebSearch**
````
{
 "query": "Hampton Miskell Texas court of appeals accident reconstruction \"five miles per hour\" memorandum opinion",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:30:38.690Z

**tool call — WebFetch**
````
{
 "url": "https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm#18.001",
 "prompt": "Quote verbatim the text of Sec. 18.001 (all subsections) and Sec. 18.002 including the affidavit form text. Include the Acts amendment notes."
}
````

### User / tool · 2026-11-02T03:30:42.494Z

**tool result**
````
The web page content you provided doesn't include Sec. 18.001 or 18.002, or any statute text, affidavit form, or amendment notes. It's only the site's navigation menu, listing the codes available, including the Civil Practice and Remedies Code.

To get the text, open the Civil Practice and Remedies Code on the site and search for Sec. 18.001 and 18.002. If you paste the section text here, I can help with it.
````

### User / tool · 2026-11-02T03:30:43.460Z

**tool result**
````
Web search results for query: "Hampton Miskell Texas court of appeals accident reconstruction "five miles per hour" memorandum opinion"

Links: [{"title":"HAMPTON v. MISKELL","url":"https://www.studicata.com/summaries/court-of-appeals-of-texas/hampton-v-miskell-2017-rbb5bb"},{"title":"Summaries of Civil Opinions and Published Criminal Opinions Issued – Week of May 21, 2007","url":"https://txcourts.gov/All_Archived_Documents/2ndCOA/summaries/2007/052107.htm"},{"title":"garza v robinson 5thca dallas 10082025","url":"https://www.girardslaw.com/library/garza-v-robinson-5thca-dallas-10082025.pdf"},{"title":"Learn About the Law","url":"https://caselaw.findlaw.com/tx-supreme-court/1510173.html"},{"title":"cabadvantage.com","url":"https://cabadvantage.com/articles/?p=9813"},{"title":"www.courtswv.gov","url":"https://www.courtswv.gov/sites/default/pubfilesmnt/2023-12/12-0667.pdf"},{"title":"Reversed and Remanded and Memorandum Opinion","url":"https://law.counselstack.com/opinion/juanita-walker-v-april-rangel-texapp-2009"},{"title":"Court of Civil Appeals of Texas, 2009","url":"https://hallapproved.com/tx/cases/appeals/2009/2934844/"},{"title":"txcourts.gov","url":"https://www.txcourts.gov/All_Archived_Documents/14thCOA/Case/Opinions/101900/990395f.pdf"},{"title":"Delarue v. State","url":"https://case-law.vlex.com/vid/delarue-v-state-no-886621092"},{"title":"Court of Civil Appeals of Texas, 2023","url":"https://hallapproved.com/tx/cases/appeals/2023/9420553/"},{"title":"Court of Civil Appeals of Texas, 2000","url":"https://hallapproved.com/tx/cases/appeals/2000/2862644/"},{"title":"2019 pd 0577 18","url":"https://cases.justia.com/texas/court-of-criminal-appeals/2019-pd-0577-18.pdf"},{"title":"Court of Civil Appeals of Texas, 2009","url":"https://hallapproved.com/tx/cases/appeals/2009/2842836/"},{"title":"Court of Civil Appeals of Texas, 2000","url":"https://hallapproved.com/tx/cases/appeals/2000/2912099/"},{"title":"Clark v. Cotten","url":"https://law.counselstack.com/opinion/clark-v-cotten-texapp-1978"},{"title":"www.vacourts.gov","url":"https://www.vacourts.gov/opinions/opncavwp/0699052.pdf"},{"title":"10 11 00071 cv","url":"https://cases.justia.com/texas/tenth-court-of-appeals/10-11-00071-cv.pdf"},{"title":"syfert.com","url":"https://syfert.com/caselaw/case.php?id=1487293"},{"title":"Court of Civil Appeals of Texas, 1978","url":"https://hallapproved.com/tx/cases/appeals/1978/1773852/"}]

The search turned up one relevant case, though not the opinion itself. A third-party case summary describes *Hampton v. Miskell* (Texas Court of Appeals, 2017). It involved a rear-end collision on an I-635 exit ramp in Dallas in April 2012. The defense's accident reconstructionist, Richard Baratta, testified that the defendant's vehicle was going five miles per hour or less at impact. The court held that the trial court did not abuse its discretion in admitting that speed testimony. The summary notes the plaintiff did not challenge the pretrial admissibility ruling on that opinion. ([studicata summary](https://www.studicata.com/summaries/court-of-appeals-of-texas/hampton-v-miskell-2017-rbb5bb))

I did not find the full opinion text, its docket number, or the exact appellate district, so those should be verified on a court site or a legal database before anyone relies on them. The other results covered unrelated Texas accident reconstruction cases, such as *Walker v. Rangel* (2009) and *TXI Transportation v. Hughes*.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:30:50.946Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dl && curl -s \"https://www.courtlistener.com/api/rest/v4/search/?q=%22Hampton%22+%22Miskell%22&type=o\" -A \"Mozilla/5.0\" | python3 -c \"import sys,json;d=json.load(sys.stdin);[print(r.get('caseName'),r.get('docketNumber'),r.get('dateFiled'),r.get('court'),r.get('citation'),'https://www.courtlistener.com'+r.get('absolute_url','')) for r in d.get('results',[])]\" ; curl -sL -A \"Mozilla/5.0\" -o cp18.htm \"https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm\"; ls -la cp18.htm; python3 -I -c \"\nimport re,html\nt=open('cp18.htm',encoding='utf-8',errors='replace').read()\nt=re.sub(r'<[^>]+>',' ',t);t=html.unescape(t);t=re.sub(r'[ \\t]+',' ',t)\ni=t.find('Sec. 18.001');print(t[i:i+9000])\"",
 "description": "Search CourtListener; fetch CPRC ch.18 text"
}
````

### User / tool · 2026-11-02T03:30:51.461Z

**tool result**
````
-rw-r--r--@ 1 arsis  wheel  250874 Nov  1 21:30 cp18.htm
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:30:56.524Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dl && head -c 1500 cp18.htm; echo; grep -o \"18\\.00[12][^<]\\{0,80\\}\" cp18.htm | head; curl -s \"https://www.courtlistener.com/api/rest/v4/search/?q=Hampton+Miskell&type=o\" -A \"Mozilla/5.0\" | head -c 600",
 "description": "Inspect downloaded statute page"
}
````

### User / tool · 2026-11-02T03:30:56.779Z

**tool result**
````
<!DOCTYPE html><html lang="en" data-beasties-container><head><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
  <meta charset="utf-8">
  <title>Texas Constitution and Statutes</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <style>@font-face{font-family:'Roboto';font-style:normal;font-weight:300;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/roboto/v51/KFO7CnqEu92Fr1ME7kSn66aGLdTylUAMa3GUBGEe.woff2) format('woff2');unicode-range:U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;}@font-face{font-family:'Roboto';font-style:normal;font-weight:300;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/roboto/v51/KFO7CnqEu92Fr1ME7kSn66aGLdTylUAMa3iUBGEe.woff2) format('woff2');unicode-range:U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;}@font-face{font-family:'Roboto';font-style:normal;font-weight:300;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/roboto/v51/KFO7CnqEu92Fr1ME7kSn66aGLdTylUAMa3CUBGEe.woff2) format('woff2');unicode-range:U+1F00-1FFF;}@font-face{font-family:'Roboto';font-style:normal;font-weight:300;font-stretch:100%;font-display:swap;src:url(https://fonts.gstatic.com/s/roboto/v51/KFO7CnqEu92Fr1ME7kSn66aGLdTylUAMa3-UBGEe.woff2) format('woff2');unicode-range:U+0370-0
{"detail":"Authentication credentials were not provided."}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:31:00.531Z

**tool call — WebFetch**
````
{
 "url": "https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_18.002",
 "prompt": "Quote verbatim the full text of section 18.002, including the complete affidavit form wording in subsection (a) and (b-1)/(b-2) if present, and the source/amendment note."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:31:01.644Z

**tool call — WebFetch**
````
{
 "url": "https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_18.001",
 "prompt": "Quote verbatim subsections (b), (c), (d), (d-1), (e), (e-1) of section 18.001 and the amendment source note (Acts years)."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:31:03.422Z

**tool call — Bash**
````
{
 "command": "curl -s \"https://www.courtlistener.com/api/rest/v3/search/?q=Hampton+Miskell&type=o\" -A \"Mozilla/5.0\" | python3 -c \"import sys,json;d=json.load(sys.stdin);print(d.get('count'));[print(r.get('caseName'),r.get('docketNumber'),r.get('dateFiled'),r.get('court'),r.get('citation'),'https://www.courtlistener.com'+r.get('absolute_url','')) for r in d.get('results',[])[:5]]\" 2>&1 | head",
 "description": "CourtListener v3 search for Hampton v. Miskell"
}
````

### User / tool · 2026-11-02T03:31:07.965Z

**tool result**
````
I can't reproduce the full text of Section 18.002 verbatim here because quotes from this source are limited to 125 characters each. Below is a summary of the section, with short quotes and the amendment note.

**Structure of Section 18.002**

- **(a) Affidavit by the service provider:** A sworn form in which the person who provided the service states their name, the date of service, and the name of the person who received it. It attaches an itemized statement of the service and charge, and states that the service was necessary and the charge reasonable at the time and place provided.
- **(b) Affidavit by the records custodian:** A sworn form for the person in charge of records showing the service and charge. It states that the records were kept in the regular course of business, were made at or near the time of service, and are the original or an exact duplicate.
- **(b-1) Medical expenses:** An affidavit for proof of medical expenses that need only substantially comply with the listed form. It also states the total amount paid and the amount still unpaid that the provider has a right to be paid after adjustments or credits.
- **(b-2) Non-recoverable charges:** If an attached bill or itemized statement under (b-1) includes a charge that is not recoverable, the reference to that charge is not admissible.
- **(c) Flexibility:** The forms are not exclusive. An affidavit that substantially complies with Section 18.001 is also sufficient. As the text puts it, "The form of an affidavit provided by this section is not exclusive."

**Amendment history**

- "Added by Acts 1993, 73rd Leg., ch. 248, Sec. 1, eff. Aug. 30, 1993."
- "Amended by: Acts 2013, 83rd Leg., R.S., Ch. 560 (S.B. 679), Sec. 2, eff. September 1, 2013."

**Source:** Section 18.002, Texas Civil Practice and Remedies Code, accessed May 26, 2025, at statutes.capitol.texas.gov. The official text, including the full blank forms, is available there.
````

### User / tool · 2026-11-02T03:31:14.213Z

**tool result**
````
The 125-character limit means I can't quote these subsections in full. Below are verbatim segments, each under 125 characters, with ellipses marking where the text continues.

**(b)**
- "Unless a controverting affidavit is served as provided by this section,"
- "is sufficient evidence to support a finding of fact by judge or jury that the amount charged was reasonable"
- "The affidavit is not evidence of and does not support a finding of the causation element of the cause of action"

**(c)**
- "The affidavit must:"
- "be taken before an officer with authority to administer oaths;"
- "be made by: (A) the person who provided the service; **or** (B) the person in charge of records showing the service provided and charge made; **and**"
- "include an itemized statement of the service and charge."

**(d)**
- "The party offering the affidavit in evidence or the party's attorney must serve a copy of the affidavit"
- "on each other party to the case by the earlier of:"
- "90 days after the date the defendant files an answer;"
- "the date the offering party must designate any expert witness under a court order; **or**"
- "the date the offering party must designate any expert witness as required by the Texas Rules of Civil Procedure."

**(d-1)**
- "Notwithstanding Subsection (d), if services are provided for the first time by a provider"
- "after the date the defendant files an answer,"
- "the party offering the affidavit in evidence or the party's attorney must serve a copy of the affidavit"
- "for services provided by that provider on each other party to the case by the earlier of:"
- "the date the offering party must designate any expert witness under a court order; **or**"
- "the date the offering party must designate any expert witness as required by the Texas Rules of Civil Procedure."

**(e)**
- "A party intending to controvert a claim reflected by the affidavit must serve a copy of the counteraffidavit"
- "on each other party or the party's attorney of record by the earlier of:"
- "120 days after the date the defendant files its answer;"
- "the date the party offering the counteraffidavit must designate expert witnesses under a court order; **or**"
- "the date the party offering the counteraffidavit must designate any expert witness as required by the"
- "Texas Rules of Civil Procedure."

**(e-1)**
- "Notwithstanding Subsection (e), if the party offering the affidavit in evidence serves a copy of the affidavit"
- "under Subsection (d-1), the party offering the counteraffidavit in evidence or the party's attorney must serve"
- "a copy of the counteraffidavit on each other party to the case by the later of:"
- "30 days after service of the affidavit on the party offering the counteraffidavit in evidence;"
- "the date the party offering the counteraffidavit must designate any expert witness under a court order; **or**"
- "the date the party offering the counteraffidavit in evidence must designate any expert witness"
- "as required by the Texas Rules of Civil Procedure."

**Amendment source note (Acts years):**
- "Acts 1985, 69th Leg., ch. 959, Sec. 1, eff. Sept. 1, 1985."
- "Amended by Acts 1987, 70th Leg., ch. 167, Sec. 3.04(a), eff. Sept. 1, 1987."
- Later amendments are listed under "Amended by" as Acts 2007 (80th Leg., S.B. 763), Acts 2013 (83rd Leg., S.B. 679), and Acts 2019 (86th Leg., H.B. 1693).
````

### User / tool · 2026-11-02T03:31:14.467Z

**tool result**
````
None
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:31:18.844Z

**tool call — WebSearch**
````
{
 "query": "\"Miskell\" \"Hampton\" 05-16 CV Dallas court of appeals 2017 Baratta",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:31:24.602Z

**tool result**
````
Web search results for query: ""Miskell" "Hampton" 05-16 CV Dallas court of appeals 2017 Baratta"

Links: [{"title":"No. 17-0547","url":"https://data.scotxblog.com/scotx/no/17-0547"},{"title":"hallapproved.com","url":"https://hallapproved.com/tx/cases/criminal/2018/4505934/"},{"title":"[Court of Appeals record regarding Hampton]","url":"https://texashistory.unt.edu/ark:/67531/metadc1404274/"},{"title":"Texas Court of Appeals, Fifth District Decisions 2016","url":"https://law.justia.com/cases/texas/fifth-court-of-appeals/2016/?page=3"},{"title":"Texas Court of Appeals, Fifth District Decisions 2016","url":"https://law.justia.com/cases/texas/fifth-court-of-appeals/2016/?page=2"},{"title":"Texas Court of Appeals, Fifth District Decisions 2020","url":"https://law.justia.com/cases/texas/fifth-court-of-appeals/2020/?page=2"},{"title":"No Opinions","url":"https://data.scotxblog.com/scotx/no/18-0895"},{"title":"Court of Civil Appeals of Texas, 2018","url":"https://hallapproved.com/tx/cases/appeals/2018/4463971/"},{"title":"Supreme Court of Texas Blog","url":"https://data.scotxblog.com/scotx/no/08-0455"},{"title":"march 31 2017","url":"https://txcourts.gov/supreme/orders-opinions/2017/march/march-31-2017/"},{"title":"Texas Court of Appeals, Fifth District Decisions 2020","url":"https://law.justia.com/cases/texas/fifth-court-of-appeals/2020/"},{"title":"No Opinions","url":"https://data.scotxblog.com/scotx/no/16-0705"},{"title":"No Opinions","url":"https://data.scotxblog.com/scotx/no/16-0792"},{"title":"Court of Civil Appeals of Texas, 2016","url":"https://hallapproved.com/tx/cases/appeals/2016/4327119/"},{"title":"Court of Civil Appeals of Texas, 2016","url":"https://hallapproved.com/tx/cases/appeals/2016/4302395/"},{"title":"Court of Civil Appeals of Texas, 2016","url":"https://hallapproved.com/tx/cases/appeals/2016/4326692/"},{"title":"Court of Civil Appeals of Texas, 2018","url":"https://hallapproved.com/tx/cases/appeals/2018/4464012/"}]

The search didn't turn up the case you're looking for. No result mentions both "Miskell" and "Hampton" under a 05-16 docket number in the Dallas Fifth District, and nothing mentions Baratta.

Some partial hits, none of which clearly match:

- **Docket 05-16-00784-CV** (Parks v. Affiliated Bank): TONY A PARKS & PARKS REALTY FIRM, LLC vs. AFFILIATED BANK, ET AL. The docket number fits the 05-16 pattern, but no Miskell or Hampton appears.
- **Hampton, 1992**: A Portal to Texas History record describes pages regarding the Dallas Court of Appeals hearing regarding the petition to remove Jack Hampton from the judge election ballot. It dates from 1992, not 2017.
- **Ex parte Gary Hampton**: A Texas Supreme Court blog entry lists a Fifth Court of Appeals case, 05-07-00523-CV, Opinion Author: Honorable Carolyn I. Wright. That is a 2007 docket, so it doesn't fit either.

The Fifth District's 2016 opinion listings on Justia are also indexed, but the snippets I got don't include a Miskell or Hampton matter. A search of the Fifth Court's own docket or Justia's 2017 listings, filtered by party name, would be the most direct next step.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:31:30.571Z

**tool call — WebFetch**
````
{
 "url": "https://pubmed.ncbi.nlm.nih.gov/?term=Castro+1997+whiplash+low-speed+rear+impacts+Eur+Spine+J",
 "prompt": "Give the PMID, full citation (authors, title, journal, year, volume, pages) and a 2-sentence summary of the abstract findings (delta-v range, symptoms in volunteers, placebo collisions) of the matching article."
}
````

### User / tool · 2026-11-02T03:31:35.874Z

**tool result**
````
**PMID:** 9455663

**Citation:** Castro WH, Schilgen M, Meyer S, Weber M, Peuker C, Wörtler K. Do "whiplash injuries" occur in low-speed rear impacts? *Eur Spine J*. 1997;6(6):366-75. doi:10.1007/BF01834062.

**Summary:**
1. Rear-end vehicle collisions produced velocity changes of 8.7–14.2 km/h (average 11.4 km/h), and the bumper car collisions, used as a comparison rather than a placebo, produced 8.3–10.6 km/h (average 9.9 km/h).
2. Of the 19 volunteers (14 men, 5 women), none showed injury signs on physical exams, motion analysis, or MRI, except one man who had a 10-degree reduction in left neck rotation lasting 10 weeks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:31:51.567Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dl && curl -sL -A \"Mozilla/5.0\" -o nemsis.pdf \"https://nemsis.org/wp-content/uploads/2025/01/NEMSIS-v3.5-Requisite-National-Elements-EMS-DataSet.pdf\" && file nemsis.pdf && pdftotext -layout nemsis.pdf nemsis.txt && grep -n -E \"eTimes\\.0[1-9]|eTimes\\.1[0-3]|eDisposition\\.(12|27|28|29|30|31)|eSituation\\.(01|02|04|09|11|12)|eNarrative|eVitals\\.(06|10|14|19|27)|eInjury\\.0[1-4]|ePatient\\.(13|15)|eResponse\\.(05|07)|eDisposition\\.(21|22|23|24)\" nemsis.txt | head -60",
 "description": "Download NEMSIS v3.5 national elements and grep fields"
}
````

### User / tool · 2026-11-02T03:31:52.513Z

**tool result (error)**
````
Exit code 1
nemsis.pdf: HTML document text, Unicode text, UTF-8 text, with very long lines (9291)
Syntax Warning: May not be a PDF file (continuing anyway)
Syntax Error (2): Illegal character <21> in hex string
Syntax Error (4): Illegal character <4f> in hex string
Syntax Error (6): Illegal character <54> in hex string
Syntax Error (7): Illegal character <59> in hex string
Syntax Error (8): Illegal character <50> in hex string
Syntax Error (11): Illegal character <68> in hex string
Syntax Error (12): Illegal character <74> in hex string
Syntax Error (13): Illegal character <6d> in hex string
Syntax Error (14): Illegal character <6c> in hex string
Syntax Error (18): Illegal character <68> in hex string
Syntax Error (19): Illegal character <74> in hex string
Syntax Error (20): Illegal character <6d> in hex string
Syntax Error (21): Illegal character <6c> in hex string
Syntax Error (23): Illegal character <6c> in hex string
Syntax Error (25): Illegal character <6e> in hex string
Syntax Error (26): Illegal character <67> in hex string
Syntax Error (27): Illegal character <3d> in hex string
Syntax Error (28): Illegal character <22> in hex string
Syntax Error (30): Illegal character <6e> in hex string
Syntax Error (31): Illegal character <2d> in hex string
Syntax Error (32): Illegal character <55> in hex string
Syntax Error (33): Illegal character <53> in hex string
Syntax Error (34): Illegal character <22> in hex string
Syntax Error (38): Illegal character <68> in hex string
Syntax Error (45): Illegal character <6d> in hex string
Syntax Error (47): Illegal character <74> in hex string
Syntax Error (50): Illegal character <6e> in hex string
Syntax Error (52): Illegal character <6d> in hex string
Syntax Error (54): Illegal character <3d> in hex string
Syntax Error (55): Illegal character <22> in hex string
Syntax Error (56): Illegal character <67> in hex string
Syntax Error (57): Illegal character <6f> in hex string
Syntax Error (58): Illegal character <6f> in hex string
Syntax Error (59): Illegal character <67> in hex string
Syntax Error (60): Illegal character <6c> in hex string
Syntax Error (62): Illegal character <2d> in hex string
Syntax Error (63): Illegal character <73> in hex string
Syntax Error (64): Illegal character <69> in hex string
Syntax Error (65): Illegal character <74> in hex string
Syntax Error (67): Illegal character <2d> in hex string
Syntax Error (68): Illegal character <76> in hex string
Syntax Error (70): Illegal character <72> in hex string
Syntax Error (71): Illegal character <69> in hex string
Syntax Error (73): Illegal character <69> in hex string
Syntax Error (76): Illegal character <74> in hex string
Syntax Error (77): Illegal character <69> in hex string
Syntax Error (78): Illegal character <6f> in hex string
Syntax Error (79): Illegal character <6e> in hex string
Syntax Error (80): Illegal character <22> in hex string
Syntax Error (83): Illegal character <6f> in hex string
Syntax Error (84): Illegal character <6e> in hex string
Syntax Error (85): Illegal character <74> in hex string
Syntax Error (87): Illegal character <6e> in hex string
Syntax Error (88): Illegal character <74> in hex string
Syntax Error (89): Illegal character <3d> in hex string
Syntax Error (90): Illegal character <22> in hex string
Syntax Error (92): Illegal character <58> in hex string
Syntax Error (95): Illegal character <52> in hex string
Syntax Error (96): Illegal character <7a> in hex string
Syntax Error (98): Illegal character <78> in hex string
Syntax Error (99): Illegal character <69> in hex string
Syntax Error (100): Illegal character <5f> in hex string
Syntax Error (103): Illegal character <70> in hex string
Syntax Error (104): Illegal character <53> in hex string
Syntax Error (105): Illegal character <54> in hex string
Syntax Error (106): Illegal character <72> in hex string
Syntax Error (108): Illegal character <6d> in hex string
Syntax Error (109): Illegal character <54> in hex string
Syntax Error (111): Illegal character <71> in hex string
Syntax Error (113): Illegal character <4e> in hex string
Syntax Error (114): Illegal character <2d> in hex string
Syntax Error (116): Illegal character <56> in hex string
Syntax Error (118): Illegal character <4f> in hex string
Syntax Error (119): Illegal character <71> in hex string
Syntax Error (121): Illegal character <6d> in hex string
Syntax Error (123): Illegal character <4c> in hex string
Syntax Error (124): Illegal character <50> in hex string
Syntax Error (125): Illegal character <54> in hex string
Syntax Error (126): Illegal character <4c> in hex string
Syntax Error (127): Illegal character <4f> in hex string
Syntax Error (128): Illegal character <59> in hex string
Syntax Error (129): Illegal character <6e> in hex string
Syntax Error (131): Illegal character <53> in hex string
Syntax Error (132): Illegal character <4f> in hex string
Syntax Error (133): Illegal character <67> in hex string
Syntax Error (134): Illegal character <22> in hex string
Syntax Error (136): Illegal character <2f> in hex string
Syntax Error (140): Illegal character <6d> in hex string
Syntax Error (142): Illegal character <74> in hex string
Syntax Error (146): Illegal character <68> in hex string
Syntax Error (148): Illegal character <72> in hex string
Syntax Error (149): Illegal character <73> in hex string
Syntax Error (151): Illegal character <74> in hex string
Syntax Error (152): Illegal character <3d> in hex string
Syntax Error (153): Illegal character <22> in hex string
Syntax Error (154): Illegal character <55> in hex string
Syntax Error (155): Illegal character <54> in hex string
Syntax Error (157): Illegal character <2d> in hex string
Syntax Error (159): Illegal character <22> in hex string
Syntax Error (163): Illegal character <6d> in hex string
Syntax Error (165): Illegal character <74> in hex string
Syntax Error (168): Illegal character <6e> in hex string
Syntax Error (170): Illegal character <6d> in hex string
Syntax Error (172): Illegal character <3d> in hex string
Syntax Error (173): Illegal character <22> in hex string
Syntax Error (174): Illegal character <76> in hex string
Syntax Error (175): Illegal character <69> in hex string
Syntax Error (177): Illegal character <77> in hex string
Syntax Error (178): Illegal character <70> in hex string
Syntax Error (179): Illegal character <6f> in hex string
Syntax Error (180): Illegal character <72> in hex string
Syntax Error (181): Illegal character <74> in hex string
Syntax Error (182): Illegal character <22> in hex string
Syntax Error (185): Illegal character <6f> in hex string
Syntax Error (186): Illegal character <6e> in hex string
Syntax Error (187): Illegal character <74> in hex string
Syntax Error (189): Illegal character <6e> in hex string
Syntax Error (190): Illegal character <74> in hex string
Syntax Error (191): Illegal character <3d> in hex string
Syntax Error (192): Illegal character <22> in hex string
Syntax Error (193): Illegal character <77> in hex string
Syntax Error (194): Illegal character <69> in hex string
Syntax Error (196): Illegal character <74> in hex string
Syntax Error (197): Illegal character <68> in hex string
Syntax Error (198): Illegal character <3d> in hex string
Syntax Error (201): Illegal character <76> in hex string
Syntax Error (202): Illegal character <69> in hex string
Syntax Error (205): Illegal character <2d> in hex string
Syntax Error (206): Illegal character <77> in hex string
Syntax Error (207): Illegal character <69> in hex string
Syntax Error (209): Illegal character <74> in hex string
Syntax Error (210): Illegal character <68> in hex string
Syntax Error (211): Illegal character <2c> in hex string
Syntax Error (213): Illegal character <69> in hex string
Syntax Error (214): Illegal character <6e> in hex string
Syntax Error (215): Illegal character <69> in hex string
Syntax Error (216): Illegal character <74> in hex string
Syntax Error (217): Illegal character <69> in hex string
Syntax Error (219): Illegal character <6c> in hex string
Syntax Error (220): Illegal character <2d> in hex string
Syntax Error (221): Illegal character <73> in hex string
Syntax Error (224): Illegal character <6c> in hex string
Syntax Error (226): Illegal character <3d> in hex string
Syntax Error (228): Illegal character <22> in hex string
Syntax Error: Couldn't find trailer dictionary
Syntax Error: Couldn't find trailer dictionary
Syntax Error: Couldn't read xref table
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:31:53.068Z

**tool call — WebFetch**
````
{
 "url": "https://med.noridianmedicare.com/web/jeb/specialties/ambulance/mileage",
 "prompt": "What does this page say about ground ambulance mileage billing: per statute mile, fractional mileage (tenths), rounding, loaded mileage only, HCPCS A0425, which modifiers? Quote short key sentences."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:31:54.420Z

**tool call — WebFetch**
````
{
 "url": "https://www.csscoperations.com/palmetto/jmb.nsf/DIDC/8L9HK55061~Specialties~Ambulance",
 "prompt": "List the origin/destination modifier letters and meanings (e.g., S = scene of accident, H = hospital, R = residence) and how the two-letter modifier is formed. Quote short key sentences."
}
````

### User / tool · 2026-11-02T03:31:54.844Z

**tool result**
````
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:31:55.813Z

**tool call — WebFetch**
````
{
 "url": "https://ezel.ai/templates/narrative-medical-report-request/",
 "prompt": "Summarize the structure of the narrative medical report: sections requested (records reviewed, history, exam, diagnoses, treatment summary, causation, prognosis/MMI, permanency, future care and costs, work restrictions), the causation wording standard requested, and any sample language. Short quotes only."
}
````

### User / tool · 2026-11-02T03:32:00.871Z

**tool result**
````
**Loaded miles only:** "Medicare only pays for miles traveled while the patient was on board or "loaded" miles." Miles driven to the pick-up point aren't paid.

**Per statute mile:** The page doesn't say "statute mile." It only refers to mileage to the nearest appropriate facility.

**HCPCS:** Covered ground mileage is billed under A0425. Mileage beyond the closest appropriate facility is billed under A0888.

**Fractional mileage and rounding:**
- **Under 1 mile:** Include a leading zero: "Mileage totaling less than 1 mile, providers/suppliers must include a "0" prior to decimal point"
- **100 miles or less:** Round up to the tenth: "Trips totaling 100 miles and less, suppliers must report mileage rounded up to nearest tenth of a mile"
- **100 miles or more:** Round up to the whole mile. Contractors truncate fractional units reported on these trips.
- **Missing mileage:** The contractor defaults to a 0.1 unit.

**Modifiers:**
- **Origin/Destination modifier:** Append to both A0425 and A0888.
- **GY modifier:** Append to A0888 only when the beneficiary is liable. Omit it when the supplier is liable.
````

### User / tool · 2026-11-02T03:32:04.223Z

**tool result**
````
**Structure of the narrative medical report request**

1. **Request basis register:** A table for recording the controlling authority, provision, and approved requirement for each issue: client instructions, patient authorization, secure transmission, provider role, opinion terminology, disclosure, fees, and deadlines.
2. **Cover letter:** Addressed to the treating physician, with the patient's name, date of birth, date of injury, and file number. It includes a background section on the mechanism of injury, initial complaints, and the treatment period.
3. **Records enclosed:** A checklist of records the firm is sending, such as office notes, ER and imaging reports, operative and therapy records, other providers' records, prior records, and billing.
4. **Information requested (sections A–J, 32 questions):**
   - **A. History and exam:** initial exam date, complaints, objective findings, prior history.
   - **B. Diagnosis:** incident-related diagnoses with ICD-10 codes.
   - **C. Causation:** causation opinion, aggravation of pre-existing conditions, and consistency with the mechanism of injury.
   - **D. Treatment:** care provided, tests ordered, medications, referrals, visit count.
   - **E. Treatment by others:** comments on other providers, if relevant.
   - **F. Current status:** condition, maximum medical improvement (MMI), further treatment needed.
   - **G. Prognosis:** recovery outlook, permanency, future care (type, frequency, duration, cost).
   - **H. Functional limits:** restrictions, whether temporary or permanent, effects on daily activities and work.
   - **I. Work status:** time off, light duty, current ability to work, permanent restrictions.
   - **J. Additional questions:** blank placeholders.
5. **Report format checklist:** Requires the provider's credentials, report date, patient identifiers, records summary, history, exam, diagnoses, treatment, causation, prognosis, permanency, work status, and signature.
6. **Matter-specific opinion terminology:** Lists counsel-approved wording, its controlling source, and the claim and provider role it applies to.
7. **Compensation:** Fee arrangement, written estimate, and a fee schedule for the report, records review, and deposition and trial testimony.
8. **Timeline, future testimony, contact, and authorization:** A requested deadline subject to the actual deadline, a non-binding planning note on depositions and trial testimony, contact details, and a request to confirm that the enclosed authorization is valid before disclosing anything.
9. **Enclosures and tracking:** Checklist of enclosures and a log for request, payment, follow-ups, receipt, and attorney review.
10. **Sample narrative report format:** Headings for history, past history, exam, studies, diagnoses, treatment, causation, prognosis, future treatment, and work status.

**Causation wording standard**

The template asks the physician to address causation only "within your expertise and independent professional judgment," using the counsel-approved matter-specific terminology from the Basis Register. That terminology is left as a blank placeholder, so no specific wording is provided. The template says the terminology should be used only if it "accurately expresses your independent opinion." The physician is asked to identify uncertainty, assumptions, records not reviewed, and limits on expertise rather than adopt wording they cannot support. If pre-existing conditions exist, the physician is asked to explain how the incident aggravated them.

**Sample language**

- Causation heading: "CAUSATION (IF REQUESTED AND WITHIN THE PROVIDER'S EXPERTISE)"
- Standard: "Please use the terminology only if it accurately expresses your independent opinion."
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:10.564Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dl && curl -sL -A \"Mozilla/5.0\" -o nasemso.pdf \"https://nemsis.org/wp-content/uploads/2024/06/NASEMSO_EMS_Time_Duration_Definitions-6-18-24.pdf\"; file nasemso.pdf; pdftotext -layout nasemso.pdf nasemso.txt 2>/dev/null && grep -n -E \"eTimes\\.[0-9]+\" nasemso.txt | head -30; curl -sL -A \"Mozilla/5.0\" -o mtdisp.pdf \"https://dphhs.mt.gov/assets/publichealth/EMSTS/EMS/Disposition.pdf\"; file mtdisp.pdf; pdftotext -layout mtdisp.pdf mtdisp.txt 2>/dev/null && grep -n -i -E \"eDisposition\\.(27|28|29|30|31)|refus|against medical\" mtdisp.txt | head -30",
 "description": "Fetch NASEMSO times and Montana disposition PDFs"
}
````

### User / tool · 2026-11-02T03:32:12.349Z

**tool result**
````
nasemso.pdf: PDF document, version 1.6 (zip deflate encoded)
9:      eTimes.01 - PSAP Call Date/Time
10:      eTimes.02 - Dispatch Notified Date/Time
11:      eTimes.03 - Unit Notified by Dispatch Date/Time
12:      eTimes.04 - Dispatch Acknowledged Date/Time
13:      eTimes.05 – Unit En Route Date/Time
14:      eTimes.06 – Unit Arrived on Scene Date/Time
15:      eTimes.07 – Arrived at Patient Date/Time
16:      eTimes.08 - Transfer of EMS Patient Date/Time
17:      eTimes.09 – Unit Left Scene Date/Time
18:      eTimes.10 – Arrival at Destination Landing Area Date/Time
19:      eTimes.11 - Patient Arrived at Destination Date/Time
20:      eTimes.12 – Destination Patient Transfer of Care Date/Time
21:      eTimes.13 – Unit Back in Service Date/Time
22:      eTimes.14 – Unit Cancelled Date/Time
23:      eTimes.15 – Unit Back at Home Location Date/Time
24:      eTimes.16 – EMS Call Completed Date/Time
25:      eTimes.17 – Unit Arrived at Staging Area Date/Time
43:    Unit Notified by Dispatch (eTimes.03) – PSAP Call (eTimes.01) =
48:      Unit Notified by Dispatch (eTimes.03) – Dispatch Notified (eTimes.02) =
53:      Unit En Route (eTimes.05) – PSAP Call (eTimes.01)* = Minutes/Seconds
55:      * If PSAP Call (eTimes.01) is null, use Dispatch Notified (eTimes.02)
59:      Unit En Route (eTimes.05) – Unit Notified by Dispatch (eTimes.03) =
64:      Unit Arrived on Scene (eTimes.06) – Unit Notified (eTimes.03) =
69:      Unit Arrived on Scene (eTimes.06) – Unit En Route (eTimes.05) =
74:      Unit Left Scene (eTimes.09)* – Unit Arrived on Scene (eTimes.06) =
77:      *If Unit Left Scene is null, use Unit Back in Service (eTimes.13)
80:      Unit Left Scene (eTimes.09)* – Arrived at Patient (eTimes.07) =
83:      *If Unit Left Scene is null, use Unit Back in Service (eTimes.13)
87:      Patient Arrived at Destination (eTimes.11) – Unit Left Scene (eTimes.09) =
92:      Destination Patient Transfer of Care (eTimes.12) – Patient Arrived at
mtdisp.pdf: PDF document, version 1.6 (zip deflate encoded)
2:           eDisposition.27 - Unit Disposition
5:           eDisposition.28 - Patient Evaluation/Care
8:           eDisposition.29 - Crew Disposition
11:           eDisposition.30 - Transport Disposition
13:           eDisposition.31 - Reason for Refusal/Release
17:eDisposition.12              eDisposition.27      eDisposition.28       eDisposition.29           eDispositiion.30              eDisposition.31            eDisposition.19
18:Incident/Patient             Unit Disposition     Patient               Crew Disposition          Transport Disposition         Reason for refusal/release Final patient
98:eDisposition.12             eDisposition.27    eDisposition.28       eDisposition.29            eDispositiion.30              eDisposition.31            eDisposition.19
99:Incident/Patient            Unit Disposition   Patient               Crew Disposition           Transport Disposition         Reason for refusal/release Final patient
137:Patient Refused
138:                            Patient contact    Patient Refused                                 crew                           -Against medical Advice         Any value Except
157:Patient Refused                                                      Back in Service,
158:                            Patient contact    Patient Refused                                                                -against medical advice         Any Value except
159:Evaluation/Care (Without                                             Care/Support Services      Patient Refused transport
161:Transport)                                                           Refused
177:                            Patient contact                                                     crew                          -Against medical Advice         Any Value except
178:Refused Care (With                             and Refused Care
198:                            Patient contact    Patient Evaluated     Care/Support Services                                    -against medical advice         Any Value except
199:Refused Care (Without                                                                           Patient Refused Transport
200:                            made               and Refused Care      Refused                                                  -pt/guardian states intent to   Black
208:1 For calls where the patient refuses care, with transport, Crew Disposition (eDisposition.29) still indicates that care was provided since you are
215:eDisposition.12           eDisposition.27    eDisposition.28       eDisposition.29           eDispositiion.30              eDisposition.31            eDisposition.19
216:Incident/Patient          Unit Disposition   Patient               Crew Disposition          Transport Disposition         Reason for refusal/release Final patient
223:                                                                                             Patient refused transport     Against Medical Advice
262:Transported by Law                                                                           Patient refused transport     Released to Law Enforcement Black
275:Transported by Private                                                                       Patient refused transport
295:contact or providing any services. An example scenario would be a first responder unit arrives, realizes they have a patient refusal as
312:standard situation where a patient was present and cared for or “treated”, without refusal, by EMS.
313:PATIENT EVALUATED AND REFUSED CARE: A patient was present and was evaluated by this crew, but the patient refused care.
315:PATIENT REFUSED EVALUATION/CARE: A patient was present and refused any evaluation or care by this crew. This value should
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:19.694Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dl && curl -sL -A \"Mozilla/5.0\" -o clm104c15.pdf \"https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/downloads/clm104c15.pdf\"; file clm104c15.pdf; pdftotext -layout clm104c15.pdf c15.txt 2>/dev/null; grep -n -E \"Scene of accident|^ *S *[-–] |A0427|A0425|nearest tenth|fractional|statute mile|loaded mile\" c15.txt | head -30",
 "description": "Fetch CMS claims manual ch.15 and grep ambulance rules"
}
````

### User / tool · 2026-11-02T03:32:20.105Z

**tool result**
````
clm104c15.pdf: PDF document, version 1.6 (zip deflate encoded)
318:       4. A nationally uniform loaded mileage rate;
333:       3. A nationally uniform loaded mileage rate for each type of air service; and
387:In the context of all payment instructions, the term “mileage” refers to loaded mileage. The
401:adjustment portion of the payment allowance. For loaded miles 1-17, the rural adjustment for
414:  All loaded miles       7/1/04 - 12/31/08             25%          FS Urban or Rural
879:       amount allowable for the mileage, multiply the number of loaded miles by the rural air
886:Charges for mileage must be based on loaded mileage only, e.g., from the pickup of a patient to
887:his/her arrival at destination. It is presumed that all unloaded mileage costs are taken into
889:loaded mileage. Suppliers should be notified that separate charges for unloaded mileage will be
919:reported in fractional numbers of loaded statute miles flown. Contractors must ensure that the
1025:BLS mileage is identified by HCPCS code A0425.
1072:        S = Scene of accident or acute event;
1093:A0425         BLS mileage (per mile)
1094:A0425         ALS mileage (per mile)
1097:A0427         Ambulance service, ALS, emergency transport, Level 1
1113:A0435         Air mileage; FW, (per statute mile)
1114:A0436         Air mileage; RW, (per statute mile)
1209:fractional units in the following situations:
1218:the fractional units. Item 24G of the Form CMS-1500 paper claim is used.
1223:fractional units in the following situations:
1232:the fractional units. Item 24G of the Form CMS-1500 paper claim is used.
1338:           •   Number of loaded miles (the number of miles traveled when the beneficiary was
1415:A0426; A0427; A0428; A0429; A0430; A0431; A0432; A0433; or A0434.
1418:(ALS1) or A0427 (ALS1 emergency), and are paid accordingly. In addition, all providers
1483:A0328, or A0330 (services before January 1, 2001) or code A0426, A0427, A0428, A0429,
1487:In addition, for line items reflecting HCPCS code A0380 or A0390, the number of loaded miles
1492:of loaded miles must be reported.
1496:For line items reflecting HCPCS codes A0426, A0427, A0428, A0429, A0430, A0431, A0432,
1580:                A0427, A0428, A0429, A0430, A0431, A0432, A0433, or A0434; and one of the
1582:                service on or after April 1, 2002, A0425;
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:24.312Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/dl && sed -n 1055,1100p c15.txt; sed -n 1200,1240p c15.txt",
 "description": "Read modifier and fractional mileage sections"
}
````

### User / tool · 2026-11-02T03:32:24.395Z

**tool result**
````
For ambulance service claims, institutional-based providers and suppliers must report an origin
and destination modifier for each ambulance trip provided in HCPCS/Rates. Origin and
destination modifiers used for ambulance services are created by combining two alpha
characters. Each alpha character, with the exception of “X”, represents an origin code or a
destination code. The pair of alpha codes creates one modifier. The first position alpha code
equals origin; the second position alpha code equals destination. Origin and destination codes
and their descriptions are listed below:

       D = Diagnostic or therapeutic site other than P or H when these are used as origin codes;
       E = Residential, domiciliary, custodial facility (other than 1819 facility);
       G = Hospital based ESRD facility;
       H = Hospital;
       I = Site of transfer (e.g. airport or helicopter pad) between modes of ambulance transport;
       J = Freestanding ESRD facility;
       N = Skilled nursing facility;
       P = Physician’s office;
       R = Residence;
        S = Scene of accident or acute event;
        X = Intermediate stop at physician’s office on way to hospital (destination code only)

In addition, institutional-based providers must report one of the following modifiers with every
HCPCS code to describe whether the service was provided under arrangement or directly:

        QM - Ambulance service provided under arrangement by a provider of services; or
        QN - Ambulance service furnished directly by a provider of services.

While combinations of these items may duplicate other HCPCS modifiers, when billed with an
ambulance transportation code, the reported modifiers can only indicate origin/destination.

B. HCPCS Codes

The following codes and definitions are effective for billing ambulance services on or after
January 1, 2001.

                    AMBULANCE HCPCS CODES AND DEFINITIONS

HCPCS                             Description of HCPCS Codes
Code
A0425         BLS mileage (per mile)
A0425         ALS mileage (per mile)
A0426         Ambulance service, Advanced Life Support (ALS), non-emergency
              transport, Level 1
A0427         Ambulance service, ALS, emergency transport, Level 1

A0428         Ambulance service, Basic Life Support (BLS), non-emergency
              transport
claim is rejected.


Mileage
Generally, each ambulance trip will require two lines of coding, e.g., one line for the service and
one line for the mileage. Suppliers who do not bill mileage would have one line of code for the
service.

Beginning with dates of service on or after January 1, 2011, mileage billed must be reported as
fractional units in the following situations:



   •   Where billing is by ASC X12 claims transaction (professional or institutional), and

   •   Where billing is by CMS-1500 paper form.

Electronic billers should see the appropriate Implementation Guide to determine where to report
the fractional units. Item 24G of the Form CMS-1500 paper claim is used.

Fractional units are not required on Form CMS-1450.

Beginning with dates of service on or after January 1, 2026, mileage billed must be reported as
fractional units in the following situations:



   •   Where billing is by ASC X12 claims transaction (professional or institutional), and

   •   Where billing is by CMS-1500 paper form.

Electronic billers should see the appropriate Implementation Guide to determine where to report
the fractional units. Item 24G of the Form CMS-1500 paper claim is used.

Fractional units are not required on Form CMS-1450.

For trips totaling up to100 covered miles suppliers must round the total miles up to the nearest
tenth of a mile and report the resulting number with the appropriate HCPCS code for ambulance
mileage. The decimal must be used in the appropriate place (e.g., 99.9).

For trips totaling 100 covered miles and greater, suppliers must report mileage rounded up to the
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:31.511Z

**tool call — WebSearch**
````
{
 "query": "Texas Rule of Civil Procedure 204 physical and mental examination motion order report of examining physician",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:32.112Z

**tool call — WebSearch**
````
{
 "query": "\"Brightwater Spine\" OR \"Brightwater Spine & Wellness\" chiropractic",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:32.715Z

**tool call — WebSearch**
````
{
 "query": "\"Bluebonnet Mutual\" health plan OR insurance",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:33.367Z

**tool call — WebSearch**
````
{
 "query": "\"Clínica Familiar Los Almendros\" OR \"Clinica Familiar Los Almendros\"",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:34.165Z

**tool call — WebSearch**
````
{
 "query": "\"Larkspur Hollow\" physical therapy OR \"Quillfeather Regional\" OR \"Ferncastle Imaging\" OR \"Thistledown Surgical\"",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:34.894Z

**tool call — WebSearch**
````
{
 "query": "\"Mossgate\" pharmacy OR \"Harrowgate & Vey\" OR \"Ines Valcarcel\" doctor",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:32:36.185Z

**tool result**
````
Web search results for query: ""Brightwater Spine" OR "Brightwater Spine & Wellness" chiropractic"

Links: [{"title":"Medimap Logo","url":"https://medimap.ca/clinics/chiropractors/on/whitewater-region"},{"title":"Lightwater Health & Chiropractic: Boosting Wellness Through Spinal Alignment","url":"https://coursereps.upsu.net/bold-post/lightwater-chiropractic-wellness-1770603465"},{"title":"truspinewellness.janeapp.com","url":"https://truspinewellness.janeapp.com/locations/truspine-wellness/book"},{"title":"Medimap Logo","url":"https://medimap.ca/clinics/chiropractors/on/bright"},{"title":"sites.google.com","url":"https://sites.google.com/view/spinalbloom/home"},{"title":"MoveWell Chiropractic & Wellness","url":"https://www.franklincoc.org/movewell-chiropractic-and-wellness"},{"title":"About Spine Integrative Wellness","url":"https://preview.vortala.com/pp5091/about-us/"},{"title":"11 Results forChiropractors near Whitewater, WI","url":"https://www.healthgrades.com/chiropractic-directory/wi-wisconsin/whitewater"},{"title":"Chiropractic Excellence in Bridgewater, NJ: Pioneers & Innovators","url":"https://beststartup.us/?p=26655"},{"title":"Medimap Logo","url":"https://medimap.ca/chiropractors/brighton-on"},{"title":"Bridgewater Chiropractic","url":"https://www.zoominfo.com/c/bridgewater-chiropractic/1140180223"},{"title":"• Moyer Total Wellness","url":"https://classpass.qa/search/mexico/chiropractic"},{"title":"Chiropractic Care","url":"https://baldwinst-chiro.vercel.app/treatments/chiropractic-care"},{"title":"• Moyer Total Wellness","url":"https://classpass.com.es/search/mexico/chiropractic"},{"title":"DiscoverNevadaHendersonChiropracticSpine Wellness Center","url":"https://lantern.llc/b/spine-wellness-center-las-vegas"},{"title":"new page 1","url":"https://nick-deliberato.squarespace.com/new-page-1"},{"title":"DR. CHAD POWELL, D.C. — BRIGHTON, CO","url":"https://practicefinder.newpatientsinc.com/chiro/dr-chad-powell-dc-brighton-co/"},{"title":"Chiropractic Care","url":"https://preview.vortala.com/pp2710/chiropractic-care/"},{"title":"DiscoverFloridaClearwaterChiropracticLivewell Chiropractic","url":"https://lantern.llc/b/livewell-chiropractic-clearwater"}]

The search didn't turn up any results for "Brightwater Spine" or "Brightwater Spine & Wellness" chiropractic, so I can't confirm that clinic exists or give details about it.

The results were for similarly named businesses, such as Spine Integrative Wellness, TruSpine & Wellness, Spine Wellness Center in Las Vegas, and Bridgewater Chiropractic in Pennsylvania. None of them is Brightwater. If you have a location, city, or website for the clinic, I can search again with that added. Otherwise, checking Google Maps or a directory like Healthgrades or Medimap by location would be the next step.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:32:37.864Z

**tool result**
````
Web search results for query: ""Bluebonnet Mutual" health plan OR insurance"

Links: [{"title":"Associated Companies","url":"https://www.bcbsms.com/about-us/associated-companies"},{"title":"www.tdi.texas.gov","url":"https://www.tdi.texas.gov/hmo/profiles/14503451.html"},{"title":"family healthcare (texas bluebonnet) home health in sw fort worth burleson tx","url":"https://www.brightstarcare.com/locations/sw-fort-worth-burleson/about-us/blog/family-healthcare-(texas-bluebonnet)-home-health-in-sw-fort-worth-burleson-tx/"},{"title":"Family Healthcare (Texas Bluebonnet) Home Health in North Dallas TX provided by BrightStar Care","url":"https://www.brightstarcare.com/locations/north-dallas-far-north-dallas/about-us/blog/family-healthcare-texas-bluebonnet-home-health-in-north-dallas-tx/"},{"title":"379282 230b1a79","url":"https://a-leads.co/company/379282_230b1a79"},{"title":"Bluebonnet Family Clinic Llc","url":"https://doctor.webmd.com/practice/baton-rouge-general-physicians-96cbf8c7-4703-e211-a42b-001f29e3eb44-physicians/alpha/www.brgphysicians.com"},{"title":"company profiles.blue cross  blue shield of mississippi a mutual insurance company.3b9cff03d15f32b1deab9dc7c448ce4c","url":"https://www.dnb.com/business-directory/company-profiles.blue_cross__blue_shield_of_mississippi_a_mutual_insurance_company.3b9cff03d15f32b1deab9dc7c448ce4c.html"},{"title":"Texas State SealTexas Department of Insurance","url":"https://webarchive.library.unt.edu/web/20070427064810/http://www.tdi.state.tx.us/consumer/cb005.html"},{"title":"alternatives competitors","url":"https://www.cbinsights.com/company/blue-cross-blue-shield-of-montana/alternatives-competitors"},{"title":"village.ai","url":"https://village.ai/company/bcbst"},{"title":"alternatives competitors","url":"https://www.cbinsights.com/company/blue-cross-blue-shield-of-mississippi/alternatives-competitors"},{"title":"company profiles.louisiana health service and indemnity company.2a144b224a60b619081d77ebc17619e0","url":"https://www.dnb.com/business-directory/company-profiles.louisiana_health_service_and_indemnity_company.2a144b224a60b619081d77ebc17619e0.html"},{"title":"bcbstx.com","url":"https://bcbstx.com/"},{"title":"company profiles.blue cross blue shield of north dakota.ef90ac67c3ef6ff64116944514c6b99f","url":"https://www.dnb.com/business-directory/company-profiles.blue_cross_blue_shield_of_north_dakota.ef90ac67c3ef6ff64116944514c6b99f.html"},{"title":"company profiles.blue cross and blue shield of florida inc.77f462ef8c44a84722a283a587b92d98","url":"https://www.dnb.com/business-directory/company-profiles.blue_cross_and_blue_shield_of_florida_inc.77f462ef8c44a84722a283a587b92d98.html"},{"title":"Newsroom | Media Resources","url":"https://ccpa.bcbstx.com/newsroom/media-resources"},{"title":"- Top Workplaces","url":"https://topworkplaces.com/company/blue-cross-blue-shield_1/albuquerque/"}]

The search didn't turn up any insurer called "Bluebonnet Mutual." The closest matches were several differently named Bluebonnet insurers:

- **Texas Bluebonnet Health Plan (Family Healthcare):** A home health provider's blog says Family Healthcare is a Texas-based managed care organization. It administers Texas Bluebonnet Health Plan products for Medicaid-eligible residents across several Texas service areas. Another blog says the plan offers both HMO and PPO plan options. These are marketing pages, so verify details with the plan.
- **Texas Bluebonnet Insurance Company:** The Texas Department of Insurance has a regulatory profile for this HMO, which includes financial, contact, and complaint information. The Company Profile page provides basic general information on the HMO.
- **Bluebonnet Life Insurance Company:** This is an affiliate of Blue Cross Blue Shield of Mississippi. It offers life and AD&D policies for covered groups. It is not a health plan.

If you meant a different company, or a "Bluebonnet Mutual" from a specific state or document, send me the details and I can search again.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:32:37.895Z

**tool result**
````
Web search results for query: "Texas Rule of Civil Procedure 204 physical and mental examination motion order report of examining physician"

Links: [{"title":"tex r civ p 204","url":"https://divorce.law/law/texas/tex-r-civ-p-204/"},{"title":"chapter 12 12 1 942637820","url":"https://law-journals-books.vlex.com/vid/chapter-12-12-1-942637820"},{"title":"RULE 204. PHYSICAL AND MENTAL EXAMINATION","url":"https://ruledex.com/texas/texas-rules-of-civil-procedure/part-ii-rules-of-practice-in-district-and-county-courts/section-9-evidence-and-discovery/b-discovery/rule-204-physical-and-mental-examination/"},{"title":"Back to Main Page / Back to List of Rules","url":"https://www.stcl.edu/lib/TexasRulesProject/TRCP166-175/rule167a1990.htm"},{"title":"Back to Main Page / Back to List of Rules","url":"https://www.stcl.edu/lib/TexasRulesProject/TRCP166-175/rule167a1973.htm"},{"title":"rule 204","url":"https://www.courtrules.net/texas/texas-civil-procedure/rule-204"},{"title":"State Rules","url":"https://state-rules.com/texas/civil/204/"},{"title":"RulesofCivilProcedure.com Civil Procedure · Every State","url":"https://rulesofcivilprocedure.com/tx/rule-204/"},{"title":"CHAPTER 12 - 12-2 Motion and Order Required","url":"https://law-journals-books.vlex.com/vid/chapter-12-12-2-942637816"},{"title":"2024 13 23 00437 cv","url":"https://cases.justia.com/texas/thirteenth-court-of-appeals/2024-13-23-00437-cv.pdf"},{"title":"Rule 204.2","url":"https://state-rules.com/texas/civil/204.2/"},{"title":"13 23 00437 cv","url":"https://law.justia.com/cases/texas/thirteenth-court-of-appeals/2024/13-23-00437-cv.html"},{"title":"Physical and Mental Examinations","url":"https://law-journals-books.vlex.com/vid/physical-and-mental-examinations-930396911"},{"title":"IN THE TENTH COURT OF APPEALS","url":"https://law.counselstack.com/opinion/in-re-christina-estabrook-texapp-2020"},{"title":"Court of Civil Appeals of Texas, 2025","url":"https://hallapproved.com/tx/cases/appeals/2025/10663878/"},{"title":"Court of Civil Appeals of Texas, 2024","url":"https://hallapproved.com/tx/cases/appeals/2024/9486878/"},{"title":"Court of Civil Appeals of Texas, 2021","url":"https://hallapproved.com/tx/cases/appeals/2021/4852679/"},{"title":"Court of Civil Appeals of Texas, 2018","url":"https://hallapproved.com/tx/cases/appeals/2018/4551329/"},{"title":"hallapproved.com","url":"https://hallapproved.com/tx/cases/appeals/2014/3073282/"}]

Rule 204 governs court-ordered physical and mental exams in Texas, and the search turned up several sources on its structure.

- **Motion and order:** A party may seek the order no later than 30 days before the discovery period ends. A party may – no later than 30 days before the end of any applicable discovery period – move for an order compelling another party to submit to an exam by a qualified physician or psychologist. The order must be in writing and must set out the exam's time, place, manner, conditions, scope, and examiner (The order must be in writing and must specify the time, place, manner, conditions, and scope of the examination and the person or persons by whom it is to be made.).
- **Report:** Rule 204.2 covers the examining physician's report. One source describes the requirement that, on request, the examining party gives the examined person a detailed written report of the findings (the party causing the examination to be made must deliver to the person a copy of a detailed written report of the examining physician or psychologist setting out the findings). Another source notes that if a physician fails or refuses to make a report, the court may exclude the testimony if offered at the trial.
- **Discovery of reports:** The rule does not block other discovery routes. A report can still be sought, or the physician deposed, under other rules (subdivision does not preclude discovery of a report of an examining physician or psychologist or the taking of a deposition of the physician or psychologist in accordance with the provisions of any other rule.).
- **Mandamus:** Orders under Rule 204 can be reviewed by mandamus. One Tenth Court of Appeals opinion cites In re Colonial Pipeline for that point (an order regarding a physical or mental examination under Texas Rule of Civil Procedure 204 may be subject to review by mandamus.).

Caveats: the sources are secondary sites and a treatise excerpt, not the official text. One site lists the rule as amended January 1, 2026, and another says it was current through March 1, 2026, so check the official txcourts.gov rule before relying on the exact wording. Also, the search didn't return the full text of Rule 204.2(b)–(c) or the good-cause standard in Rule 204.1(c), so those need a direct check.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:32:37.901Z

**tool result**
````
Web search results for query: ""Clínica Familiar Los Almendros" OR "Clinica Familiar Los Almendros""

Links: [{"title":"El Almendro, Spain","url":"https://en.wikipedia.org/wiki/El_Almendro,_Spain"},{"title":"Clínica Los Almendros","url":"https://bookingagency.io/cities/argentina/belen-de-escobar/hospitals/cl-nica-los-almendros-belen-de-escobar"},{"title":"Opiniones Residencia los almendros en Cartagena","url":"https://es.gowork.com/residencia-los-almendros-cartagena"},{"title":"Médicos de familia en Almensilla","url":"https://www.doctoralia.es/medico-de-familia/almensilla"},{"title":"Los Almendros Torcuato","url":"https://bookingagency.io/cities/argentina/beccar/hospitals/los-almendros-torcuato-beccar"},{"title":"www.doctoralia.es","url":"https://www.doctoralia.es/clinicas/clinisal"},{"title":"Clinica Medica Familiar — Santa Ana, CA","url":"https://local.yobi.com/medspa/clinica-medica-familiar-santa-ana-ca/"},{"title":"nuevo centro medico ubicado almendralejo incorpora grupo ho","url":"https://www.quironsalud.com/clideba/es/comunicacion/actualidad/nuevo-centro-medico-ubicado-almendralejo-incorpora-grupo-ho"},{"title":"nuevo centro medico ubicado almendralejo incorpora grupo ho","url":"https://www.quironsalud.com/almendralejo/es/comunicacion/actualidad/nuevo-centro-medico-ubicado-almendralejo-incorpora-grupo-ho"},{"title":"Datos del Prestador","url":"https://www.superdesalud.gob.cl/registro/centro-de-salud-familiar-los-alamos/"},{"title":"Canillas De Albaida Hotels Vrbo Property.h109087152.Hotel Information","url":"https://www.expedia.com/cn/Canillas-De-Albaida-Hotels-Vrbo-Property.h109087152.Hotel-Information"},{"title":"Médicos de familia en Almoradí","url":"https://www.doctoralia.es/medico-de-familia/almoradi"},{"title":"Centro Integral Los Almendros","url":"https://www.doctoralia.cl/clinicas/centro-integral-los-almendros"},{"title":"Primera visita Odontología en Almendralejo: clínicas y especialistas","url":"https://www.doctoralia.es/tratamientos-servicios/primera-visita-odontologia/almendralejo"},{"title":"consultorio almendricos","url":"https://www.murciasalud.es/web/centros-sanitarios/-/consultorio-almendricos"},{"title":"consultorio almendricos","url":"https://www.murciasalud.es/en/web/centros-sanitarios/-/consultorio-almendricos"},{"title":"Find Doctors and Dentists Near You","url":"https://doctor.webmd.com/practice/llamas-clinica-medica-familiar-dcde58c7-4703-e211-a42b-001f29e3eb44/physicians"}]

The search found no listing for "Clínica Familiar Los Almendros" under that exact name. Several similarly named places came up:

- **Clínica Los Almendros** in Belén de Escobar, Argentina. Its address is Bernardo de Irigoyen 629, B1625 Belén de Escobar, Provincia de Buenos Aires, and a listed phone number is +54 348 442-1212.
- **Los Almendros Torcuato** in the Beccar area of Argentina. It is at Calle Alvear 2100, Don Torcuato/Beccar area, with a listed phone of +54 11 4748-0382.
- **Centro Integral Los Almendros** in Antofagasta, Chile, listed on Doctoralia at Los almendros 8883 (trocadero), Antofagasta 1240000.

None of these sources says it is a family clinic, so I can't confirm any of them is the one you mean. If you can tell me the city or country, I can search again with that added.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:32:39.972Z

**tool result**
````
Web search results for query: ""Larkspur Hollow" physical therapy OR "Quillfeather Regional" OR "Ferncastle Imaging" OR "Thistledown Surgical""

Links: [{"title":"3 Best Humana in-clinic Physical Therapists near Larkspur, CO 80118","url":"https://beaminghealth.com/physical-therapy/larkspur-80118/humana/in-clinic"},{"title":"robert k gillespie pt","url":"https://centercare.com/listing/robert-k-gillespie-pt/"},{"title":"www.cantexcc.com","url":"https://www.cantexcc.com/snf/larkspur/"},{"title":"Disabled access: No","url":"https://npn.org.uk/physical-therapy-network/physios/practice-sandown-redstone-hollow-redhill-surrey-rh1-4bz"},{"title":"Highlands Ranch","url":"https://www.panoramaortho.com/?p=11404"},{"title":"www.panoramaortho.com","url":"https://www.panoramaortho.com/?p=8512"},{"title":"Go to main contentsGo to main menu","url":"https://www.fernleyreporter.com/article/5393,roc-express-walk-in-clinic-now-open-in-fernley"},{"title":"Rehab & Physical Therapy","url":"https://ardenthealth.com/locations?page=21"},{"title":"carefreecavecreek.org","url":"https://carefreecavecreek.org/directory-test_import/listing/98740/"},{"title":"skip to main menu","url":"https://slhn.org/providers/alex-flynn-1760159115"},{"title":"Our Care Sites","url":"https://www.trinityhealthmichigan.org/node/10046"},{"title":"oakbendmedcenter.org","url":"https://oakbendmedcenter.org/?p=3941"},{"title":"Articles by Angie Reid","url":"https://www.elon.edu/u/news/author/kreid6/page/6/"},{"title":"CONTACT INFORMATION REVIEWS & MORE DATA:","url":"https://nursinghomedatabase.com/doctors-group/7719140052/concierge-physical-therapists-llc"},{"title":"CONTACT INFORMATION REVIEWS & MORE DATA:","url":"https://nursinghomedatabase.com/doctors-group/9638087877/rock-valley-physical-therapy-center"},{"title":"CONTACT INFORMATION REVIEWS & MORE DATA:","url":"https://nursinghomedatabase.com/doctors-group/5799840211/summit-physical-therapy-llc"},{"title":"CONTACT INFORMATION REVIEWS & MORE DATA:","url":"https://nursinghomedatabase.com/doctors-group/4587562335/premier-imaging-and-intervention-pllc"},{"title":"CONTACT INFORMATION REVIEWS & MORE DATA:","url":"https://nursinghomedatabase.com/doctors-group/648583344/peak-physical-therapy-llc"}]

None of the four exact names appeared in the results. I found no page for "Larkspur Hollow," "Quillfeather Regional," "Ferncastle Imaging," or "Thistledown Surgical."

The closest matches were for other providers:

- **Larkspur:** A Beaming Health listing for physical therapists near Larkspur, CO 80118, and a 120-bed skilled nursing facility in Lufkin, Texas called Larkspur, which is not the same name.
- **Imaging and physical therapy:** Panorama Orthopedics in Highlands Ranch offers physical and occupational therapy, x-ray and MRI Imaging, but it is not named in your query.
- **Regional and surgical:** Frye Regional Medical Center in Hickory, NC appeared in a job listing, and Trinity Health Michigan's care-site page lists Northwest Surgical Specialists Inc. Neither is an exact match for your terms.

If these names are from a specific source, such as a referral, a bill, or a local directory, a spelling variant or a location would help narrow the search.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:32:40.929Z

**tool result**
````
Web search results for query: ""Mossgate" pharmacy OR "Harrowgate & Vey" OR "Ines Valcarcel" doctor"

Links: [{"title":"www.pharmacyregulation.org","url":"https://www.pharmacyregulation.org/registers/pharmacy/1101144"},{"title":"www.pharmacyregulation.org","url":"https://www.pharmacyregulation.org/registers/pharmacy/registrationnumber/1038931"},{"title":"www.pharmacyregulation.org","url":"https://www.pharmacyregulation.org/registers/pharmacy/registrationnumber/1038923"},{"title":"www.pharmacyregulation.org","url":"https://www.pharmacyregulation.org/registers/pharmacy/1038931"},{"title":"www.nhs.uk","url":"https://www.nhs.uk/services/pharmacy/kings-road-pharmcy-plus-health/FAX49/facilities"},{"title":"www.nhs.uk","url":"https://www.nhs.uk/Services/pharmacies/Overview/DefaultView.aspx?id=175415"},{"title":"www.nhs.uk","url":"https://www.nhs.uk/services/pharmacy/well/FD199"},{"title":"www.nhs.uk","url":"https://www.nhs.uk/services/pharmacy/well/FPC58"},{"title":"Doctify logo","url":"https://www.doctify.com/uk/find/all/morgate/pharmacies"},{"title":"www.pharmacyregulation.org","url":"https://www.pharmacyregulation.org/registers/pharmacy/registrationnumber/1079033"},{"title":"l hospitalet de llobregat","url":"https://www.doctoralia.es/marta-valcarcel-rodriguez-2/medico-general/l-hospitalet-de-llobregat"},{"title":"www.pharmacyregulation.org","url":"https://www.pharmacyregulation.org/registers/pharmacy/1079033"}]

The search didn't turn up anything for "Mossgate," "Harrowgate & Vey," or "Ines Valcarcel" as written. The results were mostly pharmacies in Harrogate, which may be a spelling variant of "Harrowgate."

- **Harrogate pharmacies:** The UK pharmacy register lists Cohens Chemist at a Harrogate medical centre, and another entry for Pharmacy Plus Health on Knaresborough Road. An NHS listing shows a Pharmcy Plus Health branch on King's Road.
- **"Mossgate":** The closest hit was a Doctify page for pharmacies in Moorgate, London, which lists 154 results. That doesn't match "Mossgate" directly.
- **"Ines Valcarcel":** No match. The only Valcarcel result was a Spanish doctor, Marta Valcarcel Rodriguez, a general practitioner in L'Hospitalet de Llobregat, which is a different name.

None of the results confirm a pharmacy called Mossgate, a practice called Harrowgate & Vey, or a doctor named Ines Valcarcel. If you can share where these names came from, such as a city, country, or the document they appeared in, I can run a narrower search.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:47.838Z

**tool call — WebSearch**
````
{
 "query": "CMS MLN Evaluation and Management Services Guide MLN006764 office visit medical decision making history exam documentation",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:32:48.642Z

**tool call — WebSearch**
````
{
 "query": "auto insurance bodily injury claim \"peer review\" OR \"records review\" report physician format causation \"medically necessary\" treatment after date personal injury",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:32:55.137Z

**tool result**
````
Web search results for query: "CMS MLN Evaluation and Management Services Guide MLN006764 office visit medical decision making history exam documentation"

Links: [{"title":"mln product revised evaluation and management services guide","url":"https://www.hhs.gov/guidance/document/mln-product-revised-evaluation-and-management-services-guide"},{"title":"mln006764 evaluation management services","url":"https://cms.gov/files/document/mln006764-evaluation-management-services.pdf"},{"title":"www.cms.gov","url":"https://www.cms.gov/Outreach-and-Education/Medicare-Learning-Network-MLN/MLNProducts/MLN-Publications-Items/CMS1243514"},{"title":"cms.gov","url":"https://cms.gov/outreach-and-education/medicare-learning-network-mln/mlnproducts/mln-publications-items/cms1243514"},{"title":"eval mgmt serv guide ICN006764","url":"https://uttyler.edu/academics/colleges-schools/health-science-center/files/eval-mgmt-serv-guide-ICN006764.pdf"},{"title":"health.maryland.gov","url":"https://health.maryland.gov/pophealth/Documents/Local%20Health%20Department%20Billing%20Manual/LHD%20Billing%20Manual%20V33/Section%20III%20RCM%20Updates/Coding%20and%20Documetation/CMS%20Evaluation%20and%20Management%20Services%20Guide.PDF"},{"title":"mln icn 006764 evaluation and management services final","url":"https://www.hhs.gov/guidance/sites/default/files/hhs-guidance-documents/mln_icn_006764_evaluation_and_management_services_final.pdf"},{"title":"Updated Evaluation and Management Services Guide","url":"https://med.noridianmedicare.com/web/jeb/article-detail/-/view/10525/updated-evaluation-and-management-services-guide"},{"title":"updated evaluation and management services guide","url":"https://med.noridianmedicare.com/web/jfb/search-result/-/view/10534/updated-evaluation-and-management-services-guide"},{"title":"www.chfs.ky.gov","url":"https://www.chfs.ky.gov/agencies/dbhdid/Documents/History%20and%20Physical%20Guide.pdf"},{"title":"sites.google.com","url":"https://sites.google.com/view/anesthesiology-category-i-and-/house-calls/16"},{"title":"sites.google.com","url":"https://sites.google.com/view/anesthesiology-category-i-and-/house-calls/17"},{"title":"sites.google.com","url":"https://sites.google.com/view/anesthesiology-category-i-and-/house-calls/15"},{"title":"Documentation Guidelines for Evaluation and Management (E/M) Services","url":"https://webarchive.library.unt.edu/web/20121007164324/https://www.cms.gov/Outreach-and-Education/Medicare-Learning-Network-MLN/MLNEdWebGuide/EMDOC.html"},{"title":"sites.google.com","url":"https://sites.google.com/view/anesthesiology-category-i-and-/house-calls/19"},{"title":"CMS- 2023 E & M Services Guide","url":"https://owlknowledgeteststuff.drchrono.com/home/18712945991707-cms-2023-e-m-services-guide"},{"title":"corpora.tika.apache.org","url":"https://corpora.tika.apache.org/base/docs/govdocs1/242/242223.pdf"},{"title":"MLN: Time-Based E/M Coding","url":"https://d3rx.com/regulations/mln-time-based-em"}]

The search turned up the current MLN006764 booklet and several older versions, but no excerpt covering the medical decision making (MDM) tables in detail.

- **Latest version:** The CMS PDF is dated March 2026, and its changes are marked in dark red. It covers HCPCS code G2211 and modifier 25 among its topics. (Substantive content changes are in dark red.; The PDF lists G2211 & Modifier 25 as a section heading.)
- **Purpose:** The booklet aims to help providers manage documentation and payment for E/M visits under the Medicare Physician Fee Schedule (Learn how to manage documentation and payment under the Medicare Physician Fee Schedule for evaluation and management (E/M) visits.).
- **Relationship to the 1995/1997 guidelines:** The guide is a reference tool and doesn't replace the 1995 or 1997 Documentation Guidelines for E/M Services (It is offered as a reference tool and sits alongside, rather than supplanting, the 1995 and 1997 documentation guidelines.).
- **History:** Older editions describe history elements. The Table 1 breakdown covers the history of present illness and review of systems. One source notes that a complete review of systems covers the systems tied to the presenting problems plus at least ten other organ systems (A complete ROS inquires about the system(s) directly related to the problem(s) identified in the HPI plus all additional (minimum of ten) organ systems.).
- **Exam:** The 1997 guidelines describe general multi-system and single-organ-system exams, with problem-focused exams among the types (The 1997 documentation guidelines describe two types of comprehensive examinations that can be performed during a patient's visit: general multi-system).
- **Documentation principle:** The guide says to record services during the encounter or as soon as practicable afterward (To maintain an accurate medical record, document services during the encounter or as soon as practicable after the encounter.).

Caveat: these results come from third-party copies of older editions (2021 and 2022), not the March 2026 CMS booklet itself. Check the official CMS PDF for current MDM and history/exam requirements before relying on any of this.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:32:58.656Z

**tool result**
````
Web search results for query: "auto insurance bodily injury claim "peer review" OR "records review" report physician format causation "medically necessary" treatment after date personal injury"

Links: [{"title":"aaa-nynf.modria.com","url":"https://aaa-nynf.modria.com/downloadAward/42428348"},{"title":"ROWLEY, President Judge:","url":"https://www.leagle.com/decision/19931036424pasuper6121978"},{"title":"What Medical Records Matter in Philadelphia Car Accident Cases?","url":"https://gproslaw.com/?p=32508"},{"title":"aaa-nynf.modria.com","url":"https://aaa-nynf.modria.com/downloadAward/36290616"},{"title":"aaa-nynf.modria.com","url":"https://aaa-nynf.modria.com/downloadAward/38565811"},{"title":"olsofsky v progressive insurance","url":"https://cetient.com/case/6388198/olsofsky-v-progressive-insurance"},{"title":"www.leagle.com","url":"https://www.leagle.com/decision/inflco20100210151"},{"title":"vallish v rapoport","url":"https://app.midpage.ai/opinion/6387498/vallish-v-rapoport"},{"title":"law.com","url":"https://law.com/ctlawtribune/almID/1202744080157"},{"title":"Auto / Liability","url":"https://site.danestreet.com/auto-liability"}]

The search turned up mostly state-specific case law and arbitration decisions, not a general template for these reports. Treat these as jurisdiction-dependent points, not universal rules.

- **Content requirements:** In New York no-fault arbitrations, one source notes that courts expect a peer review to go beyond a bare statement of the expert's conclusion. Denials are supported only when the peer review sets out a factual basis and a medical rationale. Another decision describes reviews as failing when the expert does not cite medical authority or accepted practice for the findings (the expert fails to cite to medical authority, standard, or generally accepted medical practice).
- **Causation vs. medical necessity (Pennsylvania):** Pennsylvania's peer review provision under the Motor Vehicle Financial Responsibility Law is aimed at reasonableness and necessity. One court explained that section 1797 encourages insurers to use peer review when they question whether treatment was needed or met accepted medical standards. Another court reasoned that allowing a peer review to decide causation would have no express statutory basis (a peer review determining causation would improperly let an insurer deny claims on an opinion lacking statutory authority).
- **Records review labeled as peer review:** In *Olsofsky v. Progressive*, the court treated a paper "medical record review" as the same thing as a statutory peer review, because a peer review is based upon a paper review of medical records and bills. The case is a useful reference when an insurer labels a causation opinion as a "records review" rather than a peer review.
- **Burden and presumptions (New York):** One decision notes that in first-party no-fault claims the claimant does not carry the initial causation burden, because causation is presumed. The insurer must then rebut it.
- **Practice criticism:** Commentary describes records-review vendors as having a financial incentive to favor insurers and says they are often labeled "independent" when they are not (insurers frequently contract with vendors to provide "records reviews," "peer reviews" or "paper reviews").

Nothing in these results addresses a specific "treatment after date" format or provides a standard report template. For that, you would need the governing state statute, the insurer's denial letter, and the relevant regulations. Consulting an attorney in the relevant state is advisable before relying on any of this.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:33:18.452Z

**tool call — Bash**
````
{
 "command": "grep -n -i -o -E \"\\b(pechero|zapata|broussard|morehouse)\\b\" research/*.md | sort | uniq -c | head; grep -rn \"validate_library\\|DENYLIST\" --include=*.py --include=*.md . 2>/dev/null | grep -v \"^./research/validate_library.py\" | grep -v reviews/ | head",
 "description": "Check name origins and validator references"
}
````

### User / tool · 2026-11-02T03:33:20.252Z

**tool result**
````
   1 research/case-library-sources-v2.md:25:Broussard
research/case-library-sources.md:4:Rebuild: `python3 research/library_build.py`. Validate: `python3 research/validate_library.py` (runs `evals/golden/check_golden.py` over golden + library,
research/validate_library.py:6:research/case-library-sources.md). Exit 0 = both pass.   Run: python3 research/validate_library.py
research/validate_library.py:13:DENYLIST = ["Nichols", "Duke Linden", "Haygood", "Escabedo", "K & L", "K&L", "Auto Crushers", "Alexandria", "Puerto Rico", "Rissman",
research/validate_library.py:33:        for w in DENYLIST:
research/validate_library.py:40:    print("identifier check:", "FAIL" if bad else f"ok ({len(cases)} packets, {len(DENYLIST)} denylist terms)")
research/case-library-sources-v2.md:24:   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass, and the real case names in this file
research/library_build.py:9:      python3 research/validate_library.py         (check_golden.py over golden + library; identifier denylist)
artifacts/review-evidence/T-055-security-r2/head_670ed09/research/case-library-sources.md:4:Rebuild: `python3 research/library_build.py`. Validate: `python3 research/validate_library.py` (runs `evals/golden/check_golden.py` over golden + library,
artifacts/review-evidence/T-055-security-r2/head_670ed09/research/library_build.py:9:      python3 research/validate_library.py         (check_golden.py over golden + library; identifier denylist)
artifacts/review-evidence/T-055-security-r2/head_670ed09/research/validate_library.py:6:research/case-library-sources.md). Exit 0 = both pass.   Run: python3 research/validate_library.py
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:33:53.037Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/validate_library.py",
 "content": "#!/usr/bin/env python3\n\"\"\"Validate evals/library/* with evals/golden/check_golden.py (T-052) and scan packets for real identifiers (T-077).\n\ncheck_golden.py reads cases from its own directory, so this copies evals/golden into a scratch dir, adds the library packets,\nruns the checker there, and then scans the library for real identifiers. The denylist holds every proper noun taken from the\ncited real sources in research/case-library-sources.md (v1) and research/case-library-sources-v2.md (v2): case parties, judges,\ndoctors named in opinions, firms, counties, cities, highways and study authors. Matching is case-insensitive and\naccent-insensitive ('GARZA', 'garza', 'Rodríguez' all hit). Exit 0 = both pass.\n\nRun:        python3 research/validate_library.py\nSelf-test:  python3 research/validate_library.py --self-test   (planted names must fail; v2 doc names must all be listed)\n\"\"\"\nimport pathlib, re, shutil, subprocess, sys, tempfile, unicodedata\n\nROOT = pathlib.Path(__file__).resolve().parents[1]\nLIB = ROOT / \"evals\" / \"library\"\nV2_DOC = ROOT / \"research\" / \"case-library-sources-v2.md\"\n\n# v1 sources (research/case-library-sources.md). States are listed because v1 sources named them; packets use the\n# two-letter abbreviation (e.g. \"TX\") where a state must appear.\nDENYLIST_V1 = [\"Nichols\", \"Duke Linden\", \"Haygood\", \"Escabedo\", \"K & L\", \"K&L\", \"Auto Crushers\", \"Alexandria\", \"Puerto Rico\",\n               \"Rissman\", \"Colossus\", \"Manitoba\", \"Verisk\", \"Medicare\", \"Tennessee\", \"Nebraska\", \"New Jersey\", \"Virginia\",\n               \"Oklahoma\", \"Texas\", \"Florida\", \"California\", \"Illinois\", \"Michigan\", \"Kelly\", \"Cutch\"]\n# v2 sources (research/case-library-sources-v2.md, \"Denylist additions\" block). Keep the two lists in sync; --self-test checks.\nDENYLIST_V2 = [\n    # P1 JLG Trucking v. Garza\n    \"JLG\", \"Garza\", \"Pechero\", \"Zapata\",\n    # P2 Guevara v. Ferrer\n    \"Guevara\", \"Ferrer\",\n    # P3 Hills v. Donis (parties, the doctor named in the opinion, the author justice, the highway)\n    \"Donis\", \"Matamoros\", \"Castellanos\", \"Morehouse\", \"Reuben\", \"Rueben\", \"Poissant\", \"I-45\",\n    # P4 Chiv v. Figueroa\n    \"Chiv\", \"Figueroa\",\n    # P5 In re Central Oregon Truck Co.\n    \"Central Oregon\", \"Oregon\", \"Broussard\",\n    # P6 Gunn v. McCoy\n    \"Gunn\", \"McCoy\",\n    # P7 Rodriguez v. Wal-Mart Stores\n    \"Rodriguez\", \"Wal-Mart\", \"Walmart\",\n    # P16 defense-firm write-up\n    \"Lewis Brisbois\", \"Brisbois\", \"Harris County\",\n    # P17 Hampton v. Miskell (dropped as a source, names still banned) and Castro et al.\n    \"Hampton\", \"Miskell\", \"Baratta\", \"I-635\", \"Castro\", \"Schilgen\",\n    # Study authors cited in v2\n    \"Steinkamp\", \"Kantrowitz\", \"Airan-Javia\", \"ElGhrably\", \"Fishbain\", \"Powell\", \"Anderson\",\n    # Cities and counties named in v2 citations\n    \"Houston\", \"Dallas\",\n]\n# Real names that are also ordinary lowercase words: banned only when capitalised (Title or UPPER), so \"rolling hills\" or\n# \"flores\" (Spanish for flowers) in a packet still passes while \"Hills\" / \"FLORES\" as a name fails.\nDENY_CAPITALISED = [\"Hills\", \"Flores\", \"Bai\"]\n# Eponymous clinical terms that share a name with a cited author and are allowed in packets on purpose.\nALLOWED_EPONYMS = [\"Waddell\"]\nDENYLIST = DENYLIST_V1 + DENYLIST_V2\nBANNER = \"SYNTHETIC — invented for evaluation; not real patient data\\n\"\n\n\ndef fold(s):\n    \"\"\"Strip accents so 'Rodríguez' matches 'Rodriguez'.\"\"\"\n    return \"\".join(c for c in unicodedata.normalize(\"NFKD\", s) if not unicodedata.combining(c))\n\n\n_ANY = [(w, re.compile(r\"(?<!\\w)\" + re.escape(fold(w)) + r\"(?!\\w)\", re.I)) for w in DENYLIST]\n_CAP = [(w, re.compile(r\"(?<!\\w)(?:\" + re.escape(w) + \"|\" + re.escape(w.upper()) + r\")(?!\\w)\")) for w in DENY_CAPITALISED]\n\n\ndef scan_text(text):\n    \"\"\"Return the denylist terms found in text (case- and accent-insensitive; capitalised-only terms need a capital).\"\"\"\n    t = fold(text)\n    return [w for w, rx in _ANY if rx.search(t)] + [w for w, rx in _CAP if rx.search(t)]\n\n\ndef doc_denylist_block(doc_text):\n    \"\"\"Terms listed in the v2 doc's fenced 'Denylist additions' block (one per line, '#' comments allowed).\"\"\"\n    m = re.search(r\"## Denylist additions.*?```text\\n(.*?)```\", doc_text, re.S)\n    if not m:\n        return None\n    return [ln.split(\"#\")[0].strip() for ln in m.group(1).splitlines() if ln.split(\"#\")[0].strip()]\n\n\n_GENERIC = {\"In\", \"re\", \"Inc\", \"Inc.\", \"LLC\", \"LLC,\", \"Co\", \"Co.\", \"Stores\", \"Stores,\", \"Truck\", \"Trucking\", \"Trucking,\", \"The\",\n            \"of\", \"and\", \"Tex\", \"Tex.\", \"App\", \"App.\"}\n\n\ndef doc_caption_names(doc_text):\n    \"\"\"Capitalised name tokens from every 'X v. Y' and 'In re X' caption in the v2 doc.\"\"\"\n    names = set()\n    for a, b in re.findall(r\"([A-Z][\\w.'&-]*(?:,? [A-Z][\\w.'&-]*)*) v\\. ([A-Z][\\w.'&-]*(?:,? [A-Z][\\w.'&-]*)*)\", doc_text):\n        for side in (a, b):\n            for tok in re.split(r\"[ ,]+\", side):\n                if tok and tok not in _GENERIC and tok[0].isupper():\n                    names.add(tok.rstrip(\".,\"))\n    for x in re.findall(r\"In re ([A-Z][\\w'-]*(?: [A-Z][\\w'-]*)*)\", doc_text):\n        toks = [t for t in x.split() if t not in _GENERIC]\n        if toks:\n            names.add(\" \".join(toks[:2]))\n    return names\n\n\ndef self_test():\n    fails = []\n    for w in DENYLIST:\n        for variant in {w, w.lower(), w.upper(), w.swapcase(), w.title()}:\n            if w not in scan_text(f\"Seen by Dr. {variant} at the clinic.\"):\n                fails.append(f\"planted {variant!r} not caught\")\n    for w in DENY_CAPITALISED:\n        for variant in (w, w.upper()):\n            if w not in scan_text(f\"Referred by {variant} Family Clinic.\"):\n                fails.append(f\"planted {variant!r} not caught\")\n        if scan_text(f\"walked up the {w.lower()} near home\"):\n            fails.append(f\"lowercase common word {w.lower()!r} wrongly flagged\")\n    if not scan_text(\"Patient: Ana Rodríguez (SYNTHETIC)\"):\n        fails.append(\"accented Rodríguez not caught\")\n    for w in ALLOWED_EPONYMS:\n        if scan_text(f\"{w} signs 0/5 today.\"):\n            fails.append(f\"eponym {w!r} wrongly flagged\")\n    doc = V2_DOC.read_text()\n    block = doc_denylist_block(doc)\n    listed = {fold(w).lower() for w in DENYLIST + DENY_CAPITALISED + ALLOWED_EPONYMS}\n    if block is None:\n        fails.append(\"v2 doc has no '## Denylist additions' ```text block\")\n    else:\n        for w in block:\n            if fold(w).lower() not in listed:\n                fails.append(f\"v2 doc denylist term {w!r} missing from validate_library.py\")\n        for w in DENYLIST_V2 + DENY_CAPITALISED:\n            if w not in block:\n                fails.append(f\"validate_library.py term {w!r} missing from the v2 doc block\")\n    for name in sorted(doc_caption_names(doc)):\n        if not any(fold(part).lower() in listed for part in [name] + name.split()):\n            fails.append(f\"v2 caption name {name!r} not on the denylist\")\n    # End-to-end: a planted packet must make the library scan fail.\n    with tempfile.TemporaryDirectory() as tmp:\n        p = pathlib.Path(tmp) / \"case_planted.txt\"\n        p.write_text(BANNER + \"Patient seen by DR. GARZA after the crash on i-45.\\n\")\n        if not scan_library([p]):\n            fails.append(\"planted packet passed the library scan\")\n    for f in fails:\n        print(\"SELF-TEST FAIL:\", f)\n    n = len(DENYLIST) * 5 + len(DENY_CAPITALISED) * 3\n    print(\"self-test:\", \"FAIL\" if fails else f\"ok ({n} planted variants caught, {len(doc_caption_names(doc))} caption names covered)\")\n    return 1 if fails else 0\n\n\ndef scan_library(files):\n    bad = []\n    for f in files:\n        t = f.read_text()\n        for w in scan_text(t):\n            bad.append(f\"{f.name}: contains real identifier {w!r}\")\n        if f.suffix == \".txt\" and not t.startswith(BANNER):\n            bad.append(f\"{f.name}: missing SYNTHETIC header\")\n    return bad\n\n\ndef main():\n    if \"--self-test\" in sys.argv:\n        return self_test()\n    cases = sorted(LIB.glob(\"case_*.expected.json\"))\n    if len(cases) < 6:\n        print(f\"FAIL: need >= 6 library cases, found {len(cases)}\")\n        return 1\n    with tempfile.TemporaryDirectory() as tmp:\n        d = pathlib.Path(tmp) / \"golden\"\n        shutil.copytree(ROOT / \"evals\" / \"golden\", d)\n        for f in LIB.glob(\"case_*\"):\n            shutil.copy(f, d / f.name)\n        r = subprocess.run([sys.executable, str(d / \"check_golden.py\")], capture_output=True, text=True, cwd=d)\n    print(r.stdout.strip()[-1500:] or r.stderr.strip()[-1500:])\n    bad = scan_library(sorted(LIB.glob(\"case_*\")))\n    for b in bad:\n        print(\"IDENTIFIER CHECK FAIL:\", b)\n    terms = len(DENYLIST) + len(DENY_CAPITALISED)\n    print(\"identifier check:\", \"FAIL\" if bad else f\"ok ({len(cases)} packets, {terms} denylist terms, case-insensitive)\")\n    return 1 if (r.returncode or bad) else 0\n\n\nif __name__ == \"__main__\":\n    sys.exit(main())\n"
}
````

### User / tool · 2026-11-02T03:33:53.105Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/research/validate_library.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:33:54.919Z

**tool call — Bash**
````
{
 "command": "python3 research/validate_library.py | tail -8",
 "description": "Run validator on existing library packets"
}
````

### User / tool · 2026-11-02T03:33:55.228Z

**tool result**
````
golden OK: 17 cases (16 synthetic), 85 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (7 packets, 71 denylist terms, case-insensitive)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:35:29.638Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re,pathlib\np=pathlib.Path(\"research/case-library-sources-v2.md\"); t=p.read_text()\ndef rep(old,new,count=1):\n    global t\n    assert t.count(old)==count, (old[:60], t.count(old))\n    t=t.replace(old,new)\n\nrep(\"\"\"   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass, and the real case names in this file\n   (e.g. Garza, Broussard, Rodriguez) must be added to that denylist before any v2 packet is built.\"\"\",\n\"\"\"   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass. Every real name in this file is on\n   that denylist (see \"Denylist additions\" below; matching is case- and accent-insensitive), and\n   `python3 research/validate_library.py --self-test` proves a planted name fails. Common surnames that appear here\n   (Garza, Rodriguez, Hills, Gunn, Hampton, Castro, Powell, Anderson, Flores) are banned as invented-name choices too,\n   including in the Spanish-language packets: pick distinctive invented surnames instead.\"\"\")\n\n# P1\nrep(\"\"\"- **Record features:** first-incident clinic visit with no records in the file; treating-physician notes that never mention\n  the second event; an ER record from the second event with neck complaints; first MRI dated after event 2; a narrative\n  \"history\" in the surgeon's note that attributes everything to event 1; multi-year span (nerve study, second MRI, fusion).\"\"\",\n\"\"\"- **Record features (from source):** an orthopedic visit days after event 1, then about eleven weeks of PT; an ambulance\n  transport in a hard collar after event 2; first MRI dated after event 2; a treating note whose history omits event 2;\n  multi-year span ending in fusion.\n- **Record features (our inference):** first-incident clinic records missing from the file; an ER record from event 2 with\n  neck complaints; a surgeon's narrative \"history\" that attributes everything to event 1.\"\"\")\n# P2\nrep(\"\"\"- **Record features:** EMS and ER pages close in time to the event with visible injuries; then a long, medically complex\n  course (admissions, a procedure, rehab) whose notes contain no causation statement at all; a large itemized hospital bill\n  spanning both phases; comorbidities in the problem list of an older patient.\"\"\",\n\"\"\"- **Record features (from source):** immediate post-crash care, then a long, medically complex course with large total\n  expenses in an elderly patient.\n- **Record features (our inference):** EMS and ER pages with visible injuries; later admission, procedure and rehab notes\n  with no causation statement; one itemized hospital bill spanning both phases; comorbidities in the problem list.\"\"\")\n# P3\nrep(\"\"\"- **Source:** Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.]), memorandum op. 2020-01-14, withdrawn and\n  substituted 2021-02-11 — firm write-up https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 (fetched; opinion\n  itself not opened).\n- **Summary:** A past-medical award was reversed because §18.001 affidavits and records do not prove an accident caused a\n  soft-tissue condition (cervical radiculitis, lumbar disc displacement), and the physician's letters saying the accident\n  caused all treated injuries were conclusory because they gave no basis.\n- **Record features:** a short \"To whom it may concern\" letter from a treater stating the crash caused all treatment, with\n  no reasoning; ICD-style diagnosis lines (radiculitis, disc displacement) repeated on every bill; billing-affidavit cover\n  pages that look like records but contain no clinical content.\"\"\",\n\"\"\"- **Source:** Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.] Feb. 11, 2021, pet. denied) (substitute\n  mem. op.) — opinion PDF via the court docket https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14 (full\n  text read, pdftotext). The docket shows the memorandum opinion of 2020-01-14, a rehearing motion, and on 2021-02-11\n  rehearing denied, the 2020 opinion withdrawn and a substitute memorandum opinion issued; petition for review No. 21-0287\n  denied 2021-07-23 (https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/). The firm newsbrief\n  https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the withdrawn 2020 opinion only.\n- **Summary (2021 substitute opinion):** Soft-tissue claims after a rear-end crash; no ambulance or ER. Past-medical awards\n  for three plaintiffs were reversed and rendered: §18.001 affidavits prove reasonableness of charges, not causation, and\n  a treating doctor's letters (and causation statements inside billing records) were conclusory because they gave no\n  explanation of how and why the crash caused the diagnoses. The award for a fourth plaintiff's ankle injury, and her\n  child's single visit, was affirmed on lay testimony and temporal proximity (Guevara).\n- **Record features (from source):** letters from a treater stating the crash caused the injuries, with no reasoning;\n  causation statements embedded in billing records; long diagnosis lists (radiculitis, disc displacement, discogenic pain)\n  on the bills; one plaintiff's single-visit bill (evaluation plus hot/cold pack).\n- **Record features (our inference):** billing-affidavit cover pages that look like records but carry no clinical content;\n  the same diagnosis lines repeated on every bill.\"\"\")\nrep(\"\"\"- **Synthetic-safety:** invented clinic and letter text; diagnosis wording paraphrased generically; no amounts reused.\n\n### P4\"\"\",\"\"\"- **Synthetic-safety:** invented clinic and letter text; diagnosis wording paraphrased generically; no amounts reused; no\n  highway, county or party name from the opinion.\n\n### P4\"\"\")\n# P4\nrep(\"\"\"- **Record features:** records where the patient's history is given in Spanish and charted in English; a note line such as\n  \"history via interpreter\" (or its absence); an itemized bill paired with a counteraffidavit-style rebuttal page.\"\"\",\n\"\"\"- **Scope of support:** this source supports only the scenario theme (Spanish-speaking party, translation and\n  counteraffidavit disputes). The opinion says nothing about how records are charted.\n- **Record features (our inference):** records where the history is given in Spanish and charted in English; a note line\n  such as \"history via interpreter\" (or its absence); an itemized bill paired with a counteraffidavit-style rebuttal page.\"\"\")\n# P5\nrep(\"\"\"  proportionality). The billing discovery listed: total billed, adjustments/write-offs, amount paid and by whom, balance,\n  insurer contracts, and any LOP, lien or guarantee.\n- **Record features:** intake forms answering \"prior accidents: none\" vs older notes that mention them; a neuro or\n  neuropsych note with memory complaints; a prior tailbone/other surgical history line; provider ledgers whose columns match\n  the six categories exactly (billed, adjusted, paid, payer, balance, LOP/lien).\n- **D-042 / flags:** billing analysis (all six columns, each cited; totals by code);\"\"\",\n\"\"\"  proportionality). The billing discovery listed six items: (1) total billed charges, (2) adjustments or write-offs,\n  (3) amount paid to the provider and by whom, (4) outstanding balances, (5) copies of contracts with the health-insurance\n  carrier, (6) any letters of protection, contracts, liens or other guarantees.\n- **Record features (from source):** two earlier car accidents with treatment; memory complaints; a prior tailbone surgery;\n  the six billing-discovery items above.\n- **Record features (our inference):** intake forms answering \"prior accidents: none\" vs older notes that mention them; a\n  neuro or neuropsych note with memory complaints; ledger columns derived from items 1-4 and 6 (billed, adjusted, paid,\n  payer, balance, LOP/lien). Item 5 (carrier contracts) is a separate document a packet may reference but never reproduce\n  as a ledger column.\n- **D-042 / flags:** billing analysis (ledger columns from items 1-4 and 6, each cited; totals by code);\"\"\")\n# P6\nrep(\"\"\"- **Summary:** The plaintiff replaced provider billing affidavits with affidavits from health insurers' subrogation agents\n  stating amounts actually paid; the court held §18.001 does not limit affiants to providers or their custodians.\n- **Record features:** insurer EOB pages\"\"\",\"\"\"- **Summary:** In a health care liability claim (medical malpractice, not a crash case), the plaintiff replaced provider\n  billing affidavits with affidavits from health insurers' subrogation agents stating amounts actually paid; the court held\n  §18.001 does not limit affiants to providers or their custodians.\n- **Record features (from source):** insurer subrogation-agent affidavits stating amounts paid.\n- **Record features (our inference):** insurer EOB pages\"\"\")\nrep(\"\"\"  a subrogation-agent affidavit page.\n- **D-042 / flags:** billing analysis (paid vs incurred\"\"\",\"\"\"  the affidavit page itself.\n- **D-042 / flags:** billing analysis (paid vs incurred\"\"\")\n# P7\nrep(\"\"\"- **Record features:** an IME/defense exam with observed-behavior narration (\"pain out of proportion\", \"inconsistent with\n  exam\"); treater notes using the same CRPS vocabulary in the opposite direction; psychiatric or unrelated history in the\n  problem list.\"\"\",\"\"\"- **Record features (from source):** a defense neurologist's exam narrating observed behavior (pain reaction to light touch vs\n  none when a companion touched the arm), no objective findings, \"somatization\" and \"symptom magnification\"; unrelated past\n  medical history.\n- **Record features (our inference):** treater notes using the same CRPS vocabulary in the opposite direction.\n- **Case stage:** a defense medical exam is a post-suit event (in Texas, TRCP 204 needs a motion and court order). For a\n  pre-suit demand packet use the same wording in a carrier records-review (peer-review) letter instead (see lib12).\"\"\")\n# P8\nrep(\"\"\"- **Record features:** \"Waddell 3/5 positive\", \"superficial tenderness\", \"overreaction\", \"distraction SLR negative\";\n  clean negations (\"0/5 Waddell signs\") on other dates; FCE \"effort inconsistent\" lines.\"\"\",\"\"\"- **Record features (from source):** the five Waddell sign categories (superficial/non-anatomic tenderness, simulation,\n  distraction, regional disturbance, overreaction) charted as a count.\n- **Record features (our inference):** \"Waddell 3/5 positive\", \"distraction SLR negative\"; clean negations (\"0/5 Waddell\n  signs\") on other dates; FCE \"effort inconsistent\" lines. \"Waddell\" is an eponymous clinical term and is allowed in\n  packets (it is on the validator's eponym allow-list, not the denylist).\"\"\")\n# P9\nrep(\"\"\"- **Record features:** \"Hx obtained via patient's son (interpreter)\"; mechanism worded differently on two records (fell vs\n  struck); a body-region word that is ambiguous in Spanish (\"espalda\" = back, upper or lower); a Spanish intake form beside an\n  English provider note; possibly DD/MM/YYYY dates on a form from a clinic across the border (our assumption; no source).\"\"\",\n\"\"\"- **Record features (from source):** an ad hoc family interpreter; omissions; a mechanism that changed in interpretation\n  (fall reported as assault); \"espalda\" word choice (DWC excerpt only).\n- **Record features (our inference):** \"Hx obtained via patient's son (interpreter)\"; mechanism worded differently on two\n  records; a Spanish intake form beside an English provider note; DD/MM/YYYY dates on a form from a clinic across the\n  border.\"\"\")\n# P10\nrep(\"\"\"- **Record features:** identical ROS/exam blocks across visits\"\"\",\"\"\"- **Record features (from source):** half of note text duplicated from earlier notes, often from another author.\n- **Record features (our inference):** identical ROS/exam blocks across visits\"\"\")\n# P11\nrep(\"\"\"- **Record features:** \"right shoulder\" in the ER note\"\"\",\"\"\"- **Record features (from source):** left/right transpositions across a record set, some later corrected; consent forms\n  naming the wrong side.\n- **Record features (our inference):** \"right shoulder\" in the ER note\"\"\")\n# P12\nrep(\"\"\"- **Record features:** faxed or scanned urgent-care\"\"\",\"\"\"- **Record features (from source):** illegible handwritten hospital notes whose meaning is unclear.\n- **Record features (our inference):** faxed or scanned urgent-care\"\"\")\n# P13\nrep(\"\"\"- **Record features:** ER \"denies LOC\", \"CT head negative\\\"\"\"\",\"\"\"- **Record features (from source):** an ED record with no TBI diagnosis for a patient who met mild-TBI criteria.\n- **Record features (our inference):** ER \"denies LOC\", \"CT head negative\\\"\"\"\")\n# P14\nrep(\"\"\"- **Record features:** UB-04-style itemized bill\"\"\",\"\"\"- **Record features (from source):** hospital charges several times cost.\n- **Record features (our inference):** UB-04-style itemized bill\"\"\")\n# P15\nrep(\"\"\"- **Record features:** EMS run sheet (times, vitals\"\"\",\"\"\"- **Record features (from source):** a base transport line plus per-mile mileage; out-of-network claim lines. Medicare billing\n  rules confirm two lines per trip and loaded miles rounded up to the tenth (see research/record-formats.md §16).\n- **Record features (our inference):** EMS run sheet (times, vitals\"\"\")\n# P16\nrep(\"\"\"- **Record features:** ortho note \"low back pain 8/10, radiating\" and a PCP note days apart\"\"\",\"\"\"- **Record features (from source):** neck and back pain reported to an orthopedic surgeon while denied to the primary-care\n  doctor; a recommended discectomy; photos of minor impact.\n- **Case stage and entry:** in the source the PCP records came in by defense subpoena (post-suit). In a pre-suit demand\n  packet the PCP note arrives from the paralegal's own records request after the client lists the PCP on intake (lib13).\n- **Record features (our inference):** ortho note \"low back pain 8/10, radiating\" and a PCP note days apart\"\"\")\n# P17 replace\ni=t.index(\"### P17.\"); j=t.index(\"## Coverage map\")\nt=t[:i]+\"\"\"### P17. Minimal property damage, low-speed impact (MIST) language in records\n- **Source:** Castro W.H. et al., \"Do 'whiplash injuries' occur in low-speed rear impacts?\", Eur Spine J 6(6):366–375\n  (1997), PMID 9455663 — https://pubmed.ncbi.nlm.nih.gov/9455663/ (abstract read via PubMed). This replaces the round-1\n  source (a Texas appellate summary on a reconstructionist's five-mph opinion) because no court, district, docket or\n  reporter cite could be found for it and its page returned 403; its names stay on the denylist.\n- **Summary:** Nineteen volunteers in staged rear impacts (velocity change about 9-14 km/h) showed no injury signs on exam,\n  motion analysis or MRI, with one minor exception. The study is the kind of biomechanical evidence the defense cites for\n  \"minor impact, soft tissue\" arguments.\n- **Scope of support:** this source supports only the scenario theme (low-speed impacts are argued to be non-injurious).\n  It says nothing about EMS or ER wording.\n- **Record features (our inference):** EMS \"minor damage to rear bumper\", \"ambulatory at scene\", \"refused transport\"; ER\n  \"low-speed MVC\"; later treater notes that describe the crash as \"violent\" or \"high impact\" (patient-reported).\n- **D-042 / flags:** causation (scene facts per D-018 lexicon); conflict (mechanism description changes over time, both\n  attributed); speaker attribution.\n- **Synthetic-safety:** invented crash; no speeds or vehicles from the source; no study data reproduced in a packet.\n\n\"\"\"+t[j:]\n# packet table\ni=t.index(\"## Suggested v2 packets\"); j=t.index(\"## Assumptions and limits\")\nt=t[:i]+\"\"\"## Suggested v2 packets (each recombines two or more patterns)\n\nStage: every packet simulates a **pre-suit demand file** unless marked otherwise. \"Entry\" says how each cross-provider record\nreached the paralegal. Format sections refer to `research/record-formats.md`.\n\n| Proposed id | Combines | One-line synthetic premise | Stage / entry |\n|---|---|---|---|\n| lib08_second_crash_mri_after | P1 + P13 | Rear-end, PT, second minor crash 11 weeks later, MRI and neuro note after crash 2 | Pre-suit; all records from the firm's requests to each provider |\n| lib09_spanish_interpreter_espalda | P9 + P4 + P11 | History via son; \"espalda\" ambiguity; side flips between ER and ortho | Pre-suit; Spanish clinic note supplied by the client |\n| lib10_eob_vs_provider_bill | P6 + P14 | Insured patient; hospital itemized bill plus EOBs with different numbers for same DOS | Pre-suit; EOBs from the client's health plan |\n| lib11_priors_and_ledger | P5 + P2 | Two prior crashes denied on intake; ledgers; older patient comorbidities | Pre-suit; older notes from a records request to the PCP |\n| lib12_records_review_credibility | P7 + P8 | Carrier records-review (peer-review) letter with symptom-magnification wording; PT/FCE notes with clean and mixed Waddell lines | Pre-suit; review letter came with the carrier's response to the demand. Litigation-stage variant: TRCP 204 exam report |\n| lib13_cloned_notes_cross_provider | P10 + P16 | Copied ROS denies the complaint the ortho charts the same week | Pre-suit; PCP note from the firm's records request after the client listed the PCP |\n| lib14_handwritten_chiro_scans | P12 + P15 | Scanned handwritten daily notes; ambulance base + mileage invoice; hidden text layer | Pre-suit; chiro records faxed by the provider |\n| lib15_conclusory_letter_mist | P3 + P17 | \"Accident caused all\" letter; EMS minor-damage and refused-transport wording | Pre-suit; affidavits obtained from providers for later service, not yet served |\n\n**Must contain** (the builder's checklist; each packet's expected JSON asserts these) and **formats used**:\n\n| Proposed id | Must contain (D-042 features and flags) | Formats (record-formats.md §) |\n|---|---|---|\n| lib08 | Two incident dates in the chart (conflict); ED \"denies LOC\" vs neuro \"brief LOC per patient\" (conflict, speaker); first MRI dated after event 2; gap between PT discharge and the neuro visit; stepper HITL step \"two incidents found\" | EMS PCR §15, ED §2, PT §3, radiology §5, office/specialist note §19, ambulance invoice §16 |\n| lib09 | One date `03/06/2026` day-first (truth 3 June 2026) and one `14/05/2026`; \"Hx via son (interpreter)\"; \"espalda\" with no level; right vs left shoulder across ER and ortho (conflict, HITL confirm side); translation labeled as LLM output | Spanish note §13, ED §2, office/specialist note §19, scanned intake §14 |\n| lib10 | Same DOS on a provider bill and an EOB with different numbers (dedupe + mismatch flag); one UB-04 room line where FL44 rate × FL46 days = FL47 charge (rate-vs-charge guard); a 0001 total line; one CMS-1500 amount OCR'd without a separator with its truth stated | UB-04 §9, ledger §10, EOB §11, CMS-1500 §8 |\n| lib11 | Intake \"prior accidents: none\" vs an older note naming two prior crashes (conflict, pre_existing); ledger with billed, adjustment, payment + payer, balance and LOP columns (items 1-4 and 6, no contract column); comorbidity problem list; calibrated confidence on pre-existing | scanned intake §14, office/specialist note §19, ledger §10, LOP §12 |\n| lib12 | At least 4 credibility sentences across 3 dates: 2 clean negations (\"0/5 Waddell signs\") that must not flag, 2 mixed sentences (\"Waddell 3/5; effort inconsistent\") that must flag (D-043); at least 3 dismissable non-credibility flags so the dismissal-pattern guard is exercised | records-review/IME report §20, PT §3 |\n| lib13 | PCP ROS \"denies back pain\" copied across 3 visits, and an ortho note \"low back pain 8/10\" in the same week (conflict, cloned text, no merge); a surgical cost estimate line (D-019: not a charge); HITL \"two providers disagree\" | office/specialist note §19 (PCP and ortho), ED §2 |\n| lib14 | Scanned travel card with checkmarks; one handwritten date with no year; a CMS-1500 grouped line where days = units; an ambulance invoice where miles × per-mile rate = line total; a page whose hidden text layer differs from the image | chiro §4, scanned intake §14, CMS-1500 §8, EMS PCR §15, ambulance invoice §16 |\n| lib15 | EMS \"refused transport\" and \"minor damage\" (causation lexicon, speaker); ER \"low-speed MVC\" vs later \"violent impact\" per patient (conflict); a narrative letter \"caused all treatment\" shown verbatim, never upgraded (judge rejects any summary that states it as fact); an 18.001 affidavit whose attached bill duplicates a bill already in the packet (dedupe) | EMS PCR §15, ED §2, chiro §4, narrative letter §18, 18.001 affidavit §17 |\n\n## Denylist additions\n\nEvery real proper noun in this file's sources. The same list is in `DENYLIST_V2` / `DENY_CAPITALISED` of\n`research/validate_library.py`; `python3 research/validate_library.py --self-test` fails if the two drift apart, if any\n\"X v. Y\" caption name here is not listed, or if a planted name in mixed case passes. Matching is case-insensitive and\naccent-insensitive; the three capitalised-only terms are also ordinary lowercase words. Allowed on purpose: \"Waddell\"\n(clinical eponym).\n\n```text\nJLG\nGarza\nPechero\nZapata\nGuevara\nFerrer\nDonis\nMatamoros\nCastellanos\nMorehouse\nReuben\nRueben\nPoissant\nI-45\nChiv\nFigueroa\nCentral Oregon\nOregon\nBroussard\nGunn\nMcCoy\nRodriguez\nWal-Mart\nWalmart\nLewis Brisbois\nBrisbois\nHarris County\nHampton\nMiskell\nBaratta\nI-635\nCastro\nSchilgen\nSteinkamp\nKantrowitz\nAiran-Javia\nElGhrably\nFishbain\nPowell\nAnderson\nHouston\nDallas\nHills        # capitalised only\nFlores       # capitalised only\nBai          # capitalised only\n```\n\n\"\"\"+t[j:]\n# assumptions\nrep(\"\"\"- Texas DWC Appeals Panel decisions (P9) and Hampton v. Miskell (P17) were seen only as search excerpts (pages returned 403).\"\"\",\n\"\"\"- Texas DWC Appeals Panel decisions (P9) were seen only as a search excerpt (page returned 403). Hampton v. Miskell was\n  dropped as P17's source in round 2: no court, district or docket could be found and its page returned 403.\n- P4 (Chiv v. Figueroa) and P17 (Castro et al.) support only the scenario theme, not any record wording.\n- Statute currency: CPRC §18.001/§18.002 text was checked 2026-11-02 through the texas.public.law mirror (amended through\n  Acts 2019, 86th Leg., H.B. 1693; §18.001(b) now says the affidavit is not evidence of causation). The official\n  statutes.capitol.texas.gov page is a JavaScript app that did not render for the fetch tool. Opinions are cited for\n  scenario shape, not as current law.\"\"\")\nrep(\"\"\"- Medical studies (P9–P14) describe general record quality, not PI files; the record features are our inference.\"\"\",\n\"\"\"- Medical studies (P8–P14, P17) describe general record quality or biomechanics, not PI files; every \"Record features\"\n  line is tagged \"(from source)\" or \"(our inference)\".\"\"\")\np.write_text(t)\nEOF\ngrep -c \"Record features (from source)\\|Record features (our inference)\" research/case-library-sources-v2.md; grep -n \"Record features:\" research/case-library-sources-v2.md; python3 research/validate_library.py --self-test",
 "description": "Apply v2 doc edits and run self-test"
}
````

### User / tool · 2026-11-02T03:35:29.812Z

**tool result (error)**
````
Exit code 1
32
SELF-TEST FAIL: v2 caption name 'A-2' not on the denylist
SELF-TEST FAIL: v2 caption name 'Allstate' not on the denylist
SELF-TEST FAIL: v2 caption name 'No' not on the denylist
SELF-TEST FAIL: v2 caption name 'X' not on the denylist
SELF-TEST FAIL: v2 caption name 'Y' not on the denylist
self-test: FAIL
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:35:37.837Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"research/validate_library.py\"); t=p.read_text()\nt=t.replace('''                if tok and tok not in _GENERIC and tok[0].isupper():''','''                if len(tok) > 1 and tok not in _GENERIC and tok[0].isupper() and not any(c.isdigit() for c in tok):''')\nt=t.replace('''\"of\", \"and\", \"Tex\", \"Tex.\", \"App\", \"App.\"}''','''\"of\", \"and\", \"Tex\", \"Tex.\", \"App\", \"App.\", \"No\", \"No.\"}''')\nt=t.replace('''    # Cities and counties named in v2 citations\n    \"Houston\", \"Dallas\",''','''    # Cities and counties named in v2 citations; insurer named in a v1 caption that v2 mentions\n    \"Houston\", \"Dallas\", \"Allstate\",''')\np.write_text(t)\nd=pathlib.Path(\"research/case-library-sources-v2.md\"); s=d.read_text()\ns=s.replace(\"Houston\\nDallas\\nHills\",\"Houston\\nDallas\\nAllstate\\nHills\"); d.write_text(s)\nEOF\npython3 research/validate_library.py --self-test; python3 research/validate_library.py | tail -1",
 "description": "Fix caption parsing and rerun self-test"
}
````

### User / tool · 2026-11-02T03:35:38.217Z

**tool result**
````
self-test: ok (354 planted variants caught, 16 caption names covered)
identifier check: ok (7 packets, 72 denylist terms, case-insensitive)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:35:44.467Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p $S/neg/research && sed 's/\"JLG\", \"Garza\", /\"JLG\", /' research/validate_library.py > $S/neg/research/validate_library.py && cp research/case-library-sources-v2.md $S/neg/research/ && python3 -I $S/neg/research/validate_library.py --self-test | tail -4",
 "description": "Negative test: removing Garza must fail self-test"
}
````

### User / tool · 2026-11-02T03:35:44.601Z

**tool result**
````
SELF-TEST FAIL: v2 doc denylist term 'Garza' missing from validate_library.py
SELF-TEST FAIL: v2 caption name 'Garza' not on the denylist
self-test: FAIL
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:37:19.555Z

**tool call — WebFetch**
````
{
 "url": "https://build.fhir.org/ig/frankoemig/hl7.v2.terminology.v24/CodeSystem-nubc-OccurrenceCode-cs.json.html",
 "prompt": "List the codes 01 through 06 and 11 with their display names exactly as given."
}
````

### User / tool · 2026-11-02T03:37:21.971Z

**tool result**
````
| Code | Display |
|---|---|
| 01 | "Auto accident" |
| 02 | "No fault insurance involved-including auto accident/other" |
| 03 | "Accident/tort liability" |
| 04 | "Accident/employment related" |
| 05 | "Other accident" |
| 06 | "Crime victim" |
| 11 | "Onset of symptoms/illness" |
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:37:26.059Z

**tool call — Bash**
````
{
 "command": "grep -n \"Bluebonnet\\|Los Almendros\\|Valc\\|twelve\\|Sections 2 to 14\\|Section 15\\|Section 16\\|section 15\\|section 16\\|(section 1[0-9])\\|see section\" research/record-formats.md",
 "description": "Find cross-references to renumber or rename"
}
````

### User / tool · 2026-11-02T03:37:26.137Z

**tool result**
````
3:**Purpose.** D-042 says the multi-case library grows from researched real-world document formats. This file describes the twelve document
12:**How to use.** Section 1 holds the cross-cutting traps (dates, money, authorship). Sections 2 to 14 cover one format each (fields, wording,
13:traps, sources, specimen). Section 15 maps formats to product rules and proposes packet mixes. Section 16 lists assumptions and gaps.
171:- Travel-card checkmarks are OCR-hostile (see section 13); a missed checkmark loses a modality, a stray mark invents one.
482:Bluebonnet Mutual Health Plan (SYNTHETIC)   Explanation of Benefits   Processed 07/22/2026
570:Clínica Familiar Los Almendros (SINTÉTICO)          Nota de consulta
582:Dra. Inés Valcárcel (SINTÉTICO)
593:health, MedPay/PIP); signature and date; sometimes an embedded LOP or assignment of benefits (section 12).
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:37:50.663Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"research/record-formats.md\"); t=p.read_text()\ndef rep(old,new):\n    global t\n    assert t.count(old)==1,(old[:70],t.count(old))\n    t=t.replace(old,new)\nrep(\"This file describes the twelve document\\ntypes\",\"This file describes the nineteen document\\ntypes\")\nrep(\"\"\"**Rules followed.** Every specimen below is invented and labeled SYNTHETIC. No person, provider, payer, address, phone, NPI, tax ID, claim\nnumber or NDC is real; identifiers use a `SYN-` prefix, phones use the 555-01xx fiction range, places are invented.\"\"\",\n\"\"\"**Rules followed.** Every specimen below is invented and labeled SYNTHETIC. Every person, provider, payer, address, phone, NPI, tax ID, claim\nnumber and NDC was made up for this file; identifiers use a `SYN-` prefix, phones use the 555-01xx fiction range, places are invented. A web\nsearch for each provider, payer, firm and clinician name (2026-11-02, results in section 23) found no exact match; two names close to real\norganizations were replaced.\"\"\")\nrep(\"\"\"**How to use.** Section 1 holds the cross-cutting traps (dates, money, authorship). Sections 2 to 14 cover one format each (fields, wording,\ntraps, sources, specimen). Section 15 maps formats to product rules and proposes packet mixes. Section 16 lists assumptions and gaps.\"\"\",\n\"\"\"**How to use.** Section 1 holds the cross-cutting traps (dates, money, authorship). Sections 2 to 20 cover one format each (fields, wording,\ntraps, sources, specimen): 2-14 from round 1, 15-20 added in round 2 for the v2 library packets (EMS report, ambulance invoice, §18.001\naffidavit, narrative letter, office/specialist note, records-review/IME report). Section 21 maps formats to product rules and packet mixes.\nSection 22 lists every cross-specimen mismatch as fixed or DELIBERATE. Section 23 lists assumptions, gaps and the name-collision search.\n`python3 research/record_formats_check.py` re-adds every specimen and checks the rules each one claims to follow.\"\"\")\n# 1.1 table\nrep(\"\"\"| Date of injury / onset | CMS-1500 Item 14 (qualifier 431), UB-04 occurrence code date, LOP letter \"Re:\" line, intake form |\"\"\",\n\"\"\"| Date of injury / onset | CMS-1500 Item 14 (qualifier 431), UB-04 occurrence code date (accident codes 01-06), LOP letter \"Re:\" line, intake form, narrative letter \"Re:\" line |\"\"\")\nrep(\"\"\"| Signature / creation date | CMS-1500 Item 31, UB-04 FL 45 on the total line, radiology \"Signed\", op-note \"D:/T:\" dictation and transcription stamps |\"\"\",\n\"\"\"| Signature / creation date | CMS-1500 Item 31, UB-04 FL 45 on the total line (unverified convention, see section 23), radiology \"Signed\", op-note \"D:/T:\" dictation and transcription stamps |\n| Sworn / letter / report date | §18.001 affidavit jurat and notary commission date, narrative letter date, records-review or IME report date | Paperwork about care, not care. The affidavit's own date-of-service range spans many visits. |\"\"\")\n# PT\nrep(\"\"\"\"97110 TherEx 23 min\n(2 units); 97140 Manual 12 min (1 unit); 97014 E-stim unattended 15 min.\" \"Total timed: 35 min. Total tx: 50 min.\" \"Tolerated well. Continue\nPOC 3x/wk x 4 wks.\\\"\"\"\",\"\"\"\"97110 TherEx 25 min\n(2 units); 97140 Manual 13 min (1 unit); 97014 E-stim unattended 15 min.\" \"Total timed: 38 min. Total tx: 53 min.\" \"Tolerated well. Continue\nPOC 2x/wk x 6 wks.\\\"\"\"\")\nrep(\"\"\"Larkspur Hollow Physical Therapy        Daily Note        Visit 7 of 24\nPatient: Delphine Okonkwo-Vale (SYNTHETIC)   Date: 06/10/2026   In 09:02 Out 09:54\"\"\",\"\"\"Larkspur Hollow Physical Therapy (SYNTHETIC)        Daily Note        Visit 2 of 12\nPatient: Delphine Okonkwo-Vale (SYNTHETIC)   Date: 06/10/2026   In 09:02 Out 09:55\"\"\")\nrep(\"\"\"Interventions:  97110 TherEx  23 min  2u\n                97140 Manual  12 min  1u\n                97014 E-stim  15 min  (untimed)\nTotal timed 35 min / Total tx 50 min\nA: Tolerated well. Progressing toward goal of 70 deg rotation.\nP: Continue POC 3x/wk x 4 wks.\"\"\",\"\"\"Interventions:  97110 TherEx  25 min  2u\n                97140 Manual  13 min  1u\n                97014 E-stim  15 min  (untimed)\nTotal timed 38 min / Total tx 53 min\nA: Tolerated well. Progressing toward goal of 70 deg rotation.\nP: Continue POC 2x/wk x 6 wks.\"\"\")\nrep(\"\"\"06/12/2026  Pt cancelled - no transportation. Rescheduled 06/15/2026.\n```\"\"\",\"\"\"06/12/2026  Pt cancelled - no transportation. Rescheduled 06/15/2026.\n```\n(Units follow the CMS total-time 8-minute rule: 38 timed minutes = 3 units, the extra unit going to the code with more minutes. The AMA\nper-code method gives the same 2 + 1 here. Visit 1 was the 05/27/2026 evaluation; 2x/wk x 6 wks = 12 planned visits.)\"\"\")\n# chiro\nrep(\"(see section 13); a missed checkmark\",\"(see section 14); a missed checkmark\")\nrep(\"\"\"Patient: Delphine Okonkwo-Vale (SYNTHETIC)   DOS: 06/03/2026   Visit #9\"\"\",\"\"\"Patient: Delphine Okonkwo-Vale (SYNTHETIC)   DOS: 06/03/2026   Visit #4\"\"\")\nrep(\"\"\"A: Improving. P: Continue 3x/wk x 4 wks, re-exam 06/24/2026.\nDr. Corvin Ashdown, DC (SYNTHETIC)\n--- Travel card (scanned) ---\nDATE    | C | T | L | ES | HP | TR\n06/01   | x | x | x | x  | x  |\n06/03   | x | x | x | x  | x  |\n06/05   | x |   | x | x  |    |\n```\"\"\",\"\"\"A: Improving. P: Daily through 06/05, then 3x/wk x 3 wks, re-exam 06/24/2026.\nDr. Corvin Ashdown, DC (SYNTHETIC)\n--- Travel card (scanned) ---\nDATE    | C | T | L | ES | H/C | TR\n06/01   | x | x | x | x  |  x  |\n06/02   | x | x | x | x  |  x  |\n06/03   | x | x | x | x  |  x  |\n```\n(Visit #1 was the new-patient exam on 05/29/2026, the date the intake in section 14 is signed; it was billed on an earlier claim not shown.\nVisits 2-4 are the three consecutive days on the travel card and on the CMS-1500 in section 8. C/T/L = regions adjusted, ES = 97014,\nH/C = 97010 hot/cold pack.)\"\"\")\n# radiology\nrep(\"\"\"COMPARISON: Cervical radiographs 05/15/2026.\"\"\",\"\"\"COMPARISON: CT cervical spine 05/15/2026 (Quillfeather Regional ED).\"\"\")\nrep(\"\"\"ADDENDUM 06/20/2026: Comparison radiographs reviewed; no change to impression.\"\"\",\"\"\"ADDENDUM 06/20/2026: Comparison CT images reviewed; no change to impression.\"\"\")\n# op note\nrep(\"\"\"FINDINGS: Posterior disc protrusion compressing R C6 root.\nD: 08/04/2026  T: 08/05/2026\n```\"\"\",\"\"\"FINDINGS: Posterior disc protrusion compressing R C6 root.\nD: 08/04/2026  T: 08/05/2026\n```\n(DELIBERATE: \"12 weeks of therapy\" is the surgeon's recital. The PT records run from 05/27/2026 to 08/04/2026 = 69 days, about 9.9 weeks.\nExpected: the excerpt is shown verbatim and attributed; no automatic flag (the product has no duration check); golden truth must never\nstate \"12 weeks\" as fact. An adjuster will count the weeks, so the paralegal should see both dates.)\"\"\")\np.write_text(t)\nEOF\necho ok",
 "description": "Edit record-formats sections 1-6"
}
````

### User / tool · 2026-11-02T03:37:50.775Z

**tool result**
````
ok
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:38:23.099Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"research/record-formats.md\"); t=p.read_text()\ndef rep(old,new):\n    global t\n    assert t.count(old)==1,(old[:70],t.count(old))\n    t=t.replace(old,new)\ni=t.index(\"**Specimen (SYNTHETIC)** (rendered as the OCR text a scanned form tends to produce):\")\nj=t.index(\"---\\n\\n## 9. UB-04\")\nt=t[:i]+\"\"\"**Specimen (SYNTHETIC), clean boxed form** (as printed; money boxes have no decimal point, cents sit right of the bar):\n```\nSYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS\n2. PATIENT'S NAME  OKONKWO-VALE, DELPHINE (SYNTHETIC)     3. DOB 03 | 09 | 1991  F\n10b. AUTO ACCIDENT?  [X] YES  [ ] NO   PLACE (State) TX\n14. DATE OF CURRENT ILLNESS  05 | 14 | 26   QUAL 431\n21. ICD Ind 0   A. S13.4XXA   B. M54.12\n24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI\n    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001\n    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001\n    060326   060326   11     98941              AB     85 | 00       1      SYN-NPI-0001\n    060126   060326   11     97014              A      90 | 00       3      SYN-NPI-0001\n    060126   060326   11     97010              A      45 | 00       3      SYN-NPI-0001\n25. FED TAX ID  SYN-TIN-0001     28. TOTAL CHARGE  390 | 00     29. AMOUNT PAID  0 | 00\n31. SIGNATURE  Dr. Corvin Ashdown, DC (SYNTHETIC)  DATE 06/30/26\n33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142\n```\n(Lines 4-5 group 06/01 to 06/03: three consecutive days, 3 units, each matching the travel card's ES and H/C marks on all three days in\nsection 4; $30.00 and $15.00 per day. Lines 1-3 bill the same code one line per day, which NUCC also allows. MOD is blank; AB and A are\ndiagnosis pointers in 24E. Line sum 85 + 85 + 85 + 90 + 45 = 390 = Item 28. Item 14 is the injury date and Item 31 the signature date;\nneither is a visit.)\n\n**Specimen (SYNTHETIC), the same claim as OCR text** (what a scanned copy returns; truth beside each money string):\n```\nSYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS\n24. 060126 060126 11 98941 AB 8500 1 SYN-NPI-0001         <- truth 85.00 (not 8,500.00)\n    060226 060226 11 98941 AB 85 00 1 SYN-NPI-0001        <- truth 85.00 (bar dropped, space kept)\n    O60326 060326 11 98941 AB 85|00 1 SYN-NPI-0001        <- truth 85.00; O for 0 in the date\n    060126 060326 11 97014 A 9000 3 SYN-NPI-0001          <- truth 90.00 (not 9,000.00)\n    060126 060326 11 97010 A 45 OO 3 SYN-NPI-0001         <- truth 45.00; O for 0 in the cents\n28. TOTAL CHARGE 39000   29. AMOUNT PAID 0 00             <- truth 390.00 and 0.00\n```\n(Expected tool behavior: money in 24F and Items 28-29 is parsed as implied-cents in code; the line sum is compared with Item 28 in code;\nevery OCR-derived amount and date goes to review with the page image. A parser that reads `8500` as dollars bills $8,500 per adjustment.)\n\n\"\"\"+t[j:]\n# UB-04 fields/wording/traps\nrep(\"\"\"31-36 occurrence codes and dates (accident-related codes);\"\"\",\"\"\"31-36 occurrence codes and dates (accident codes 01-06, see traps);\"\"\")\nrep(\"\"\"**Typical wording.** Line 23 carries revenue code `0001` = total charges (paper claims), with the **creation date** in FL 45 of that line.\n\"PAGE 1 OF 2\" on multi-page claims.\"\"\",\"\"\"**Typical wording.** Line 23 carries revenue code `0001` = total charges (paper claims), with the **creation date** in FL 45 of that line\n(unverified: common convention, not in the RI guide; NUBC manual not opened). \"PAGE 1 OF 2\" on multi-page claims.\"\"\")\nrep(\"\"\"- FL 45 on the total line is the claim creation date, not a service date.\"\"\",\"\"\"- FL 45 on the total line is the claim creation date (unverified convention), not a service date.\n- Occurrence codes 01-06 all carry an accident date: 01 auto accident (current NUBC wording reported as accident/medical coverage), 02\n  no-fault insurance involved, 03 accident/tort liability, 04 accident/employment related, 05 other accident, 06 crime victim. A PI claim may\n  carry any of them (01 or 03 most often). Extraction treats every one as the accident date, never a service date; packets vary the code.\n- On inpatient claims the room line has a rate in FL 44, days in FL 46 and often no FL 45 date; the stay dates come from FL 6 and FL 12.\"\"\")\nrep(\"\"\"- Assumption: FL 44 title \"HCPCS/Rate/HIPPS code\" and the creation-date-on-line-23 convention are from my prior knowledge of the form; verify against the NUBC manual before quoting.\"\"\",\n\"\"\"- HL7 v2.4 NUBC occurrence-code vocabulary: https://build.fhir.org/ig/frankoemig/hl7.v2.terminology.v24/CodeSystem-nubc-OccurrenceCode-cs.json.html — **opened**. Takeaway: 01 auto accident, 02 no-fault insurance involved, 03 accident/tort liability, 04 accident/employment related, 05 other accident, 06 crime victim, 11 onset of symptoms. This is an older HL7 rendering; the current NUBC label for 01 may differ.\n- Assumption: FL 44 title \"HCPCS/Rate/HIPPS code\" and the creation-date-on-line-23 convention are from prior knowledge, confirmed only by the T-078 reviewer's working knowledge; verify against the NUBC manual before quoting.\"\"\")\nrep(\"\"\"**Specimen (SYNTHETIC).**\n```\nSYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS\n1 Quillfeather\"\"\",\"\"\"**Specimen 1 (SYNTHETIC), outpatient ED claim.**\n```\nSYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS\n1 Quillfeather\"\"\")\nrep(\"\"\"(The 0001 line repeats the sum; 051826 on that line is the creation date.)\"\"\",\"\"\"(The 0001 line repeats the sum; 051826 on that line is the creation date, an unverified convention. Occurrence code 01.)\n\n**Specimen 2 (SYNTHETIC), inpatient claim with a room rate on the charge line** (a different synthetic patient):\n```\nSYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS\n1 Saltmarrow General Hospital (SYNTHETIC)   3a SYN-PCN-7730  3b SYN-IP-11902  4 0111\n6 STATEMENT COVERS PERIOD  FROM 091526  THROUGH 091826\n8 TELFAIR-NKEMELU, AMBROSE (SYNTHETIC)   12 ADMISSION 091526  13 HR 02  14 TYPE 1  17 STAT 01\n31 OCCURRENCE  CODE 03  DATE 091426\n42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED\n0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00\n0450    EMERGENCY ROOM                               091526        1          1,975.00\n0250    PHARMACY                                     091526       14            412.75\n0300    LABORATORY                                   091526        6            688.00\n0320    DX X-RAY                                     091526        2            540.00\n0001    TOTAL                                        092226                   9,165.75\n67 S42.201A   72 ECI V43.52XA   76 ATTENDING Dr. Rosamund Achterberg (SYNTHETIC)\nPAGE 1 OF 1\n```\n(Room line: FL 44 rate 1,850.00 x FL 46 3 days = FL 47 5,550.00. Only FL 47 is a charge; 1,850.00 is a rate. A naive sum of every money\nfigure adds the rate and the 0001 line and reports 20,181.50 instead of 9,165.75. Admitted 09/15, discharged 09/18 = 3 room days.\nOccurrence code 03, not 01: 09/14/2026 is the accident date, not a service date. 092226 on the 0001 line is the creation date.)\"\"\")\n# ledger\nrep(\"\"\"Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection.\n```\"\"\",\"\"\"Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection.\n```\n(DELIBERATE: no payment or contractual adjustment is posted, although the EOB in section 11 (processed 07/22/2026) shows plan paid 16.00 and\nCO-45/CO-97 reductions for DOS 06/10/26. Expected: billing analysis cites both documents' figures and flags the ledger-vs-EOB mismatch for\nreview; the tool never picks paid or incurred. The $65.00 fee-schedule line has no date of service: a rate, not a charge.)\"\"\")\n# EOB rename\nrep(\"\"\"Bluebonnet Mutual Health Plan (SYNTHETIC)\"\"\",\"\"\"Quoinmere Mutual Health Plan (SYNTHETIC)\"\"\")\n# Spanish\nrep(\"\"\"Clínica Familiar Los Almendros (SINTÉTICO)\"\"\",\"\"\"Consultorio Médico Peñaverde (SINTÉTICO)\"\"\")\nrep(\"\"\"  Cita de control en 1 semana (24/05/2026).\"\"\",\"\"\"  Cita de control en 3 semanas (07/06/2026).\"\"\")\nrep(\"\"\"Dra. Inés Valcárcel (SINTÉTICO)\n```\n(`17/05/2026` is 17 May. The $400.00 is a per-session rate, not a charge.)\"\"\",\"\"\"Dra. Itziar Orbezua Lanz (SINTÉTICO)\n```\n(`17/05/2026` is 17 May: unambiguous, day > 12. `07/06/2026` is **7 June 2026**, not July 6: both parts are 12 or less, so only the\nday-first convention decides; it is 21 days after the visit, matching \"en 3 semanas\". The $650.00 is the visit charge; the $400.00 is a\nper-session rate, not a charge.)\"\"\")\np.write_text(t)\nEOF\necho ok",
 "description": "Edit CMS-1500, UB-04, ledger, EOB, Spanish sections"
}
````

### User / tool · 2026-11-02T03:38:23.200Z

**tool result**
````
ok
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:38:25.575Z

**tool call — Bash**
````
{
 "command": "sed -n '/^## 15. Product mapping/,$p' research/record-formats.md | head -5 && grep -n \"^## \" research/record-formats.md",
 "description": "Locate tail sections"
}
````

### User / tool · 2026-11-02T03:38:25.682Z

**tool result**
````
## 15. Product mapping and proposed packet mixes

| Format | Main rule it exercises | Expected tool behavior |
|---|---|---|
| ED note | Dates (rollover), voice, pre-existing, hedges | Date = arrival; excerpt verbatim; PMH flag |
22:## 1. Cross-cutting traps (apply to every format)
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
703:## 15. Product mapping and proposed packet mixes
730:## 16. Assumptions, limits and gaps
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:38:26.884Z

Now the new sections 15 to 23.

### Assistant · claude-opus-5-5 · 2026-11-02T03:40:25.843Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/tail.md",
 "content": "## 15. EMS patient care report (ambulance run report)\n\n**Fields (NEMSIS v3 names in brackets).** Agency, unit and crew with certification levels; incident and run numbers; call times: PSAP call\n(eTimes.01), unit notified (eTimes.03), en route (eTimes.05), arrived on scene (eTimes.06), arrived at patient (eTimes.07), left scene\n(eTimes.09), arrived at destination (eTimes.11), transfer of care (eTimes.12); scene location type; patient demographics; chief complaint;\nmechanism of injury and vehicle/scene description; several timed vital-sign sets (BP, HR, RR, SpO2, GCS, pain); assessment by body region;\ntreatments with times (spinal motion restriction, cold pack, medications); narrative (often in CHART or SOAP order); disposition: unit\ndisposition, patient evaluation/care, crew disposition, transport disposition (eDisposition.27-30); reason for refusal or release\n(eDisposition.31); destination; patient or witness signature on a refusal; crew signatures.\n\n**Typical wording.** \"Dispatched for MVC with injuries.\" \"Arrived to find pt sitting in driver seat, self-extricated, ambulatory at scene.\"\n\"Moderate rear-end damage to pt's vehicle, airbags deployed.\" \"Pt c/o neck pain 7/10, denies LOC.\" \"GCS 15.\" \"Pt placed in position of\ncomfort, c-collar applied.\" Refusal: \"Pt refused transport against medical advice. Risks explained incl. worsening injury and death. Pt\nverbalized understanding, signed refusal.\" \"Minor damage to rear bumper.\" The run report carries **no charges**; the bill is section 16.\n\n**Extraction traps.**\n- The service date is the call date. A call at 23:12 that reaches the ED at 23:47 and is signed after midnight still belongs to the call date.\n- Eight timestamps for one encounter; the ED's own arrival time (section 2) can differ by a minute or two. That is not a conflict.\n- Scene descriptions (\"minor damage\", \"ambulatory at scene\", \"self-extricated\") are the crew's observations, not the patient's report and not\n  a medical finding. They are the defense's MIST language (D-018 causation lexicon; speaker is EMS).\n- A refusal is a dated encounter with no transport. The next care date after a refusal decides the first-treatment gap.\n- \"Pt states\" lines (history) sit beside crew observations in one narrative; the excerpt keeps both voices.\n- Repeated vital sets: pain 7/10 at 23:24 and 5/10 at 23:40 are both true at their times.\n\n**Sources.**\n- NASEMSO, *EMS Time Duration Definitions* (2024-06-18): https://nemsis.org/wp-content/uploads/2024/06/NASEMSO_EMS_Time_Duration_Definitions-6-18-24.pdf — **opened** (text extracted). Takeaway: the eTimes.01-17 list and interval formulas (scene time = left scene minus arrived on scene).\n- Montana DPHHS, *NEMSIS disposition guide*: https://dphhs.mt.gov/assets/publichealth/EMSTS/EMS/Disposition.pdf — **opened** (text extracted). Takeaway: eDisposition.27-31 (unit, patient evaluation/care, crew, transport disposition, reason for refusal/release); \"patient evaluated and refused care\" and \"patient refused transport\" values; \"against medical advice\" as a refusal reason.\n- NEMSIS v3.5 *Requisite National Elements*: https://nemsis.org/wp-content/uploads/2025/01/NEMSIS-v3.5-Requisite-National-Elements-EMS-DataSet.pdf — search summary (the URL returned an HTML page to curl).\n- Assumption: the narrative wording above is common EMS charting style; no Texas agency template was opened.\n\n**Specimen (SYNTHETIC).**\n```\nSYNTHETIC RECORD - PATIENT CARE REPORT - ALL IDENTIFIERS FICTITIOUS\nFernhollow County EMS (SYNTHETIC)   Unit: Medic 14   Incident SYN-INC-26-04471   Run SYN-RUN-0912\nDate: 05/14/2026   PSAP 23:12  Notified 23:13  En route 23:14  On scene 23:21  At pt 23:22\n                   Left scene 23:36  At dest 23:47  Transfer of care 23:52\nPatient: Delphine Okonkwo-Vale (SYNTHETIC)  DOB 03/09/1991  F\nCC: Neck pain.  MOI: MVC, rear-end, restrained driver, airbag deployed.\nScene: Moderate rear damage to pt vehicle. Pt self-extricated, ambulatory at scene.\nVITALS  23:24  BP 148/90  HR 102  RR 18  SpO2 98%  GCS 15  Pain 7/10\n        23:40  BP 142/88  HR 96   RR 18  SpO2 98%  GCS 15  Pain 6/10\nNARRATIVE: Pt states \"the truck hit me from behind.\" Denies LOC. C/o neck pain and\n  tingling R hand. C-collar applied, cold pack to neck. Transported to Quillfeather\n  Regional ED without incident.\nDISPOSITION: Patient treated, transported by this EMS unit.\nCrew: Hollis Brandvold, Paramedic (SYNTHETIC); Pia Strandquist, EMT (SYNTHETIC)\n--- Refusal variant (another synthetic run, for packets that need it) ---\nDate: 03/02/2026  On scene 16:05  Left scene 16:31\nScene: Minor damage to rear bumper. Pt ambulatory at scene, no visible injury.\nPt c/o mild neck stiffness. Pt refused transport against medical advice; risks explained.\nDISPOSITION: Patient evaluated and refused care / refused transport.  Pt signature on file.\n```\n(Arrival at destination 23:47 here vs ED arrival 23:48 in section 2: same event, not a conflict. \"Moderate rear damage\" is the crew's\nobservation; \"the truck hit me from behind\" is the patient's.)\n\n---\n\n## 16. Ambulance invoice (base rate plus mileage)\n\n**Fields.** Agency billing name and tax ID; invoice number, invoice date and run number; date of service; patient; pick-up and drop-off\n(origin/destination modifier letters); level of service line (HCPCS A0427 ALS1 emergency, A0429 BLS emergency, etc.); mileage line (A0425,\nunits = loaded miles, fractional to the tenth); per-unit rate and line charge; supplies lines if itemized; total charges; payments (auto\nPIP/MedPay, health plan); adjustments; balance due; \"out of network\" or balance-billing notice.\n\n**Typical wording.** \"A0427-SH ALS emergency transport, Level 1 ... 1,450.00.\" \"A0425-SH Ground mileage 8.7 mi @ 22.50/mi ... 195.75.\"\n\"Total charges 1,645.75.\" \"Balance due upon receipt.\" Origin/destination modifiers pair a pick-up letter with a drop-off letter (S = scene of\naccident or acute event, H = hospital, R = residence), so a crash scene to ED trip is SH.\n\n**Extraction traps.**\n- The per-mile figure (22.50/mi) is a **rate**; only the extended line (195.75) and the stated total are charges (D-042 rate-vs-charge guard;\n  miles x rate is recomputed in code).\n- Units are miles with a decimal (8.7), not visits and not integers. A parser that drops the decimal bills 87 miles.\n- Every trip is normally two lines (service + mileage) for one encounter; they are not two encounters.\n- Only loaded miles (patient on board) are billable for Medicare; commercial and auto carriers vary.\n- The invoice date and any statement date are not the service date; the run number ties the invoice to the run report (section 15).\n- A balance-billing notice states an asserted balance without a service line (notes only, D-019).\n\n**Sources.**\n- CMS, *Medicare Claims Processing Manual*, ch. 15 *Ambulance*: https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/downloads/clm104c15.pdf — **opened** (text extracted). Takeaways: origin/destination modifier letters (S = scene of accident or acute event, H = hospital, R = residence ...; first letter origin, second destination); A0425 ground mileage per mile, A0427 ALS1 emergency; generally two lines per trip; mileage reported in fractional units, rounded up to the nearest tenth for trips under 100 miles; mileage means loaded mileage.\n- Noridian JE, *Ambulance Mileage*: https://med.noridianmedicare.com/web/jeb/specialties/ambulance/mileage — **opened**. Takeaway: only loaded miles are paid; round up to the tenth for 100 miles or less; leading zero below 1 mile; missing mileage defaults to 0.1.\n- FAIR Health ground-ambulance brief (2023) via research/case-library-sources-v2.md P15 — search excerpt; most claim lines out of network.\n- Assumption: the rates in the specimen are invented and do not reflect any fee schedule.\n\n**Specimen (SYNTHETIC).**\n```\nSYNTHETIC RECORD - AMBULANCE INVOICE - ALL IDENTIFIERS FICTITIOUS\nFernhollow County EMS Billing (SYNTHETIC)   TIN SYN-TIN-0440   Invoice SYN-INV-77310   Invoice date 05/29/2026\nPatient: Delphine Okonkwo-Vale (SYNTHETIC)   Run SYN-RUN-0912   DOS 05/14/2026\nPick-up: Scene (S)   Drop-off: Quillfeather Regional Medical Center (H)\nCODE      DESCRIPTION                          UNITS   RATE       CHARGE\nA0427-SH  ALS emergency transport, Level 1      1      1,450.00   1,450.00\nA0425-SH  Ground mileage, loaded                8.7       22.50     195.75\n                                          TOTAL CHARGES          1,645.75\nPAYMENTS 0.00   ADJUSTMENTS 0.00   BALANCE DUE 1,645.75\nAccount noted: attorney representation, letter of protection requested.\n```\n(8.7 x 22.50 = 195.75; 1,450.00 + 195.75 = 1,645.75. 22.50 is a rate. 05/29/2026 is the invoice date, not a service date.)\n\n---\n\n## 17. Texas CPRC §18.001 billing affidavit and records cover page\n\n**Fields.** Optional caption (cause number, court, parties) when filed; affiant's name and role: the person who provided the service or the\nperson in charge of records (custodian); provider name; patient; date-of-service range; sworn statements that the records were kept in the\nregular course of business and made at or near the time, and that the services were necessary and the charges reasonable at the time and\nplace; for medical expenses, the amount charged, the amount paid and the amount still unpaid that the provider has a right to be paid\nafter adjustments or credits (§18.002(b-1)); jurat with notary signature, date and commission expiry; attached itemized statement; page\ncount. A records-retrieval **cover page** often sits on top: vendor name, request number, page count, a list of what is enclosed, or a\n\"no records found\" certification.\n\n**Typical wording (paraphrased, not the statutory form).** \"Before me, the undersigned authority, personally appeared ..., who being duly\nsworn deposed as follows.\" \"I am the custodian of records of ...\" \"Attached are 3 pages of records ... kept in the regular course of\nbusiness.\" \"The total amount charged for the services was $445.00. The amount paid was $0.00. The amount unpaid that the provider has a\nright to be paid is $400.00.\" \"Sworn to and subscribed before me on ...\" The exact form is in CPRC §18.002; quote it from the official text.\n\n**Extraction traps.**\n- The affidavit is **not a medical record**: no encounter, no clinical content. Its jurat date, notary commission date and cover-page date\n  are not service dates; its DOS range spans many visits.\n- §18.001(b) (as amended 2019): the affidavit supports reasonableness of the charge but is **not evidence of causation**. Diagnosis lines on\n  the attached bill are not a causation opinion (Hills v. Donis, 2021).\n- The attached itemized statement usually duplicates a bill already produced in the provider's records: a true duplicate (section 1.4).\n  Dedupe must keep one copy and cite both locations, never add both.\n- Charged / paid / unpaid totals are attested sums. Code recomputes totals from the attached lines and compares; paid vs unpaid is a\n  paid-or-incurred figure for notes only.\n- A counteraffidavit from the other side attacks the same lines; it is an opponent's opinion, not a provider record.\n- \"No records\" certifications are non-record pages (record_warning), but their date tells the paralegal a request was answered.\n\n**Sources.**\n- Texas Civil Practice and Remedies Code §18.001 and §18.002, via https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_18.001 and https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_18.002 — **opened** (fetch tool; short quotes only). Takeaways: affiant is the provider or the records custodian; affidavit must include an itemized statement and be sworn; 90-day / 120-day service deadlines for affidavits and counteraffidavits; §18.001(b) says it is not evidence of causation; §18.002(b-1) medical-expense form adds amount paid and amount unpaid; amended through Acts 2019 (H.B. 1693). Official page https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm is a JavaScript app that did not render for the fetch tool.\n- Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.] Feb. 11, 2021, pet. denied) (substitute mem. op.), via https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14 — **opened** (PDF, pdftotext). Takeaway: §18.001 affidavits do not establish causation.\n- Assumption: the cover-page layout is a common records-retrieval vendor style; no vendor template was opened.\n\n**Specimen (SYNTHETIC).**\n```\nSYNTHETIC RECORD - RECORDS CERTIFICATION COVER - ALL IDENTIFIERS FICTITIOUS\nGallowmere Records Retrieval (SYNTHETIC)   Request SYN-RR-3310   Completed 08/14/2026\nProvider: Larkspur Hollow Physical Therapy (SYNTHETIC)   Patient: Delphine Okonkwo-Vale (SYNTHETIC)\nEnclosed: Affidavit (2 pp) | Itemized statement (1 p) | Daily notes (6 pp)   Total pages: 9\n--- page 2 ---\nAFFIDAVIT CONCERNING COST AND NECESSITY OF SERVICES (CPRC 18.001)\nSTATE OF TX  /  COUNTY OF FERNHOLLOW (SYNTHETIC)\nBefore me appeared Marguerite Oyelaran-Pike (SYNTHETIC), who being sworn stated: I am the custodian of\nrecords of Larkspur Hollow Physical Therapy (SYNTHETIC). Attached are records of services provided to\nDelphine Okonkwo-Vale (SYNTHETIC) from 05/27/2026 through 07/15/2026, kept in the regular course of business\nand made at or near the time of service. The services were necessary and the charges reasonable.\nTotal amount charged: $445.00.  Amount paid: $0.00.  Amount unpaid that the provider has a right to be paid: $400.00.\nSworn to before me 08/12/2026.   /s/ Notary Public, State of TX (SYNTHETIC)   Commission expires 04/30/2029\n--- page 3: itemized statement (same document as section 10) ---\n```\n(The figures match the ledger in section 10: charges 445.00, adjustment 45.00, payments 0.00, balance 400.00. Page 3 is a duplicate of the\nsection 10 statement and must not be counted twice. Packets write the state as \"TX\" because the spelled-out state name is on the v1\nidentifier denylist in research/validate_library.py.)\n\n---\n\n## 18. Treating-provider narrative letter\n\n**Fields.** Letterhead; letter date; addressee (usually the patient's attorney); \"Re:\" line with patient, DOB, date of injury; records\nreviewed; history as told by the patient; initial complaints; examination findings; diagnoses (often with ICD-10); treatment summary\n(dates, visit count, modalities, referrals); current status and maximum medical improvement; prognosis and permanency; future care (type,\nfrequency, duration, estimated cost); work status and restrictions; causation statement; signature and credentials.\n\n**Typical wording.** Explained form: \"Based on the history, the timing of symptom onset, my examination and the MRI of 06/18/2026, it is my\nopinion within reasonable medical probability that the C5-6 disc protrusion was caused or aggravated by the collision of 05/14/2026,\nbecause ...\" Conclusory form: \"The accident caused all of the injuries and treatment listed above.\" Future care: \"Ms. X will need an\nestimated 12 additional visits at $150.00 per visit.\" \"She has not reached MMI.\"\n\n**Extraction traps.**\n- The letter date is not a service date. The letter is a summary written for the attorney, not a visit (section 4 traps).\n- The causation sentence is a provider statement: the D-018 causation lexicon flags it, the excerpt is shown verbatim, and no summary may\n  restate it as fact (the judge rejects one that does). The tool never grades whether it is conclusory; that is a legal judgment.\n- Restated history (\"Pt reports she was rear-ended ...\") is the patient's account repeated by the provider.\n- Visit counts and dates in the letter can disagree with the notes; code counts dated notes, the letter's number is cited as the letter's.\n- Future-care costs are estimates and per-visit prices are rates (D-019, D-042): never charges.\n- The letter may cite records not in the packet (an MRI from another facility); cite the letter, do not invent the record.\n\n**Sources.**\n- Ezel, *Personal Injury Narrative Medical Report Request* template: https://ezel.ai/templates/narrative-medical-report-request/ — **opened**. Takeaways: requested sections (history, exam, diagnoses with ICD-10, treatment, causation, MMI, prognosis, permanency, future care with cost, work status); causation addressed only within the provider's own judgment and in counsel-approved terms.\n- Hills v. Donis (2021), above — **opened**. Takeaway: a treater's letters that state the crash caused the injuries without explaining how and why are conclusory and no evidence of causation.\n- Mondaq, *Tips for attorneys: direct exam of a treating physician* (2012): https://mondaq.com/unitedstates/healthcare/160998/tips-for-attorneys-direct-exam-of-a-treating-physician — search summary; future care, cost and a causation question in reasonable medical probability.\n\n**Specimen (SYNTHETIC).**\n```\nSYNTHETIC RECORD\nBrightwater Spine & Wellness (SYNTHETIC)   555-0142\nJuly 20, 2026\nOttoline Vey, Attorney, Harrowgate & Vey, PLLC (SYNTHETIC)\nRe: Delphine Okonkwo-Vale (SYNTHETIC)   DOB 03/09/1991   Date of injury 05/14/2026\nMs. Okonkwo-Vale has treated in this office since 05/29/2026. She reports she was rear-ended\non 05/14/2026 and developed neck pain and right hand tingling the same night.\nDiagnoses: cervical sprain (S13.4XXA); cervical radiculopathy (M54.12).\nTreatment: spinal manipulation, e-stim and hot/cold packs; MRI 06/18/2026 ordered by this office.\nPrognosis: guarded. She has not reached maximum medical improvement.\nFuture care: an estimated 12 additional visits at $150.00 per visit ($1,800.00).\nThe motor vehicle collision of 05/14/2026 caused all of the injuries and treatment described in this letter.\nDr. Corvin Ashdown, DC (SYNTHETIC)\n```\n(Conclusory on purpose, as in v2 pattern P3: no explanation of how or why. $150.00 per visit is a rate and $1,800.00 an estimate; neither is\na charge. July 20, 2026 is the letter date. The diagnoses match the CMS-1500 in section 8.)\n\n---\n\n## 19. Physician office / specialist progress note (PCP, orthopedics, neurology, pain management)\n\n**Fields.** Date; visit type (new, follow-up); chief complaint; HPI or interval history; ROS; PMH/PSH, medications, allergies, social\nhistory (often carried forward); exam; data reviewed (imaging, outside records); assessment and plan (medical decision making); procedures\nrecommended or scheduled; referrals; work status; follow-up interval; E/M code on the billing copy (99202-99215); signature and date.\n\n**Typical wording.** \"Pt returns for f/u of neck pain.\" \"Interval hx: no improvement with 6 wks of PT.\" \"ROS: Negative except as noted in\nHPI.\" \"MRI C-spine 06/18/2026 reviewed: C5-6 protrusion with R foraminal narrowing.\" \"A/P: 1. Cervical radiculopathy, R C6. Discussed\noptions. Recommend C5-6 ACDF.\" \"Estimated surgeon fee $14,500.00.\" \"Work status: off work through 08/31/2026.\" \"RTC 4 wks.\"\n\n**Extraction traps.**\n- Carried-forward ROS and PMH (\"denies back pain\") can contradict the HPI of the same note or another provider's note the same week\n  (v2 patterns P10, P16); code pairs nearby dates, never merges two visits because text matches.\n- A recommended or scheduled procedure is not a performed one; its date is in the future.\n- \"Estimated\" surgeon or facility fees are estimates (D-019), not charges.\n- Work-status and follow-up dates are future dates, not encounters.\n- History \"per patient\" and outside imaging \"reviewed\" are cited as the note's statements, not as new findings.\n- A PCP note that predates the injury is a pre-existing-condition source even when it is about something else.\n\n**Sources.**\n- CMS MLN, *Evaluation and Management Services Guide* (MLN006764): https://www.cms.gov/files/document/mln006764-evaluation-management-services.pdf — search summary; history, exam and medical decision making as the documented elements; document during or soon after the encounter.\n- Steinkamp et al. (2022) via research/case-library-sources-v2.md P10 — abstract read; about half of note text is duplicated from earlier notes.\n- Assumption: the layout above is a common EHR office-note print; no specific vendor template was opened.\n\n**Specimen (SYNTHETIC).**\n```\nSYNTHETIC RECORD\nThistledown Orthopedic & Spine Clinic (SYNTHETIC)      Office Visit      DOS 07/08/2026\nPatient: Delphine Okonkwo-Vale (SYNTHETIC)   Referred by: Dr. Corvin Ashdown, DC (SYNTHETIC)\nCC: Neck pain with R arm tingling.\nHPI: Rear-end MVC 05/14/2026 per pt. PT since 05/27/2026 without lasting relief. Pain 7/10.\nROS: Negative except as noted in HPI.\nPMH: Low back pain 2023, resolved per pt.\nEXAM: Spurling + R. Grip 4/5 R. Diminished R biceps reflex.\nDATA: MRI C-spine 06/18/2026 reviewed: C5-6 protrusion, mild R foraminal narrowing.\nA/P: Cervical radiculopathy, R C6. Recommend C5-6 ACDF. Estimated surgeon fee $14,500.00.\nWork status: off work through 08/31/2026.   RTC after surgery.\nDr. Anselm Greaves, MD (SYNTHETIC)   99204\n```\n(The ACDF is recommended here and performed on 08/04/2026 (section 6). $14,500.00 is an estimate. 08/31/2026 is a future work-status\ndate, not a visit.)\n\n---\n\n## 20. Records-review (peer-review) letter and independent medical exam (IME) report\n\n**Fields.** Requesting party (liability carrier, PIP carrier or defense counsel); reviewer or examiner name, specialty and credentials;\nreport date; for an IME, the exam date and who attended; list of records reviewed with their dates; questions posed (Were the injuries\ncaused by the incident? Was treatment reasonable and necessary? Through what date? Has the person reached MMI?); the reviewer's history\nsummary; exam findings (IME only: inspection, ROM, neuro, non-organic signs such as Waddell signs, distraction tests); opinions; attestation.\n\n**Typical wording.** \"Based on my review of the records listed above ...\" \"Treatment after 07/15/2026 was not reasonable or medically\nnecessary.\" \"Findings consistent with a self-limited cervical strain.\" \"Degenerative changes that pre-date the incident.\" \"Symptom\nmagnification.\" \"Waddell signs 3/5.\" \"Effort was inconsistent.\" \"MMI as of 07/15/2026.\"\n\n**Extraction traps.**\n- Stage: a records review is often pre-suit (the carrier's response to the demand); a defense medical exam in Texas needs a motion and court\n  order under TRCP 204, so it is post-suit. The packet should say which.\n- The reviewer's history is a summary of other records, not an encounter. A records review has only a report date; only an IME has an exam\n  date, and the examiner is an adverse party's expert, not a treater.\n- Credibility words (\"symptom magnification\", \"inconsistent effort\", \"Waddell 3/5\") flag under D-043; a clean negation (\"0/5 Waddell signs\")\n  does not, and a sentence that mixes both does.\n- \"Not reasonable or necessary after date X\" and \"MMI as of X\" are opinions with dates; X is not a service date.\n- The reviewer may misquote dates or findings from the records; code can compare quoted dates with the packet's own entries.\n\n**Sources.**\n- Texas Rule of Civil Procedure 204 (physical and mental examination): https://ruledex.com/texas/texas-rules-of-civil-procedure/part-ii-rules-of-practice-in-district-and-county-courts/section-9-evidence-and-discovery/b-discovery/rule-204-physical-and-mental-examination/ — search summary; motion no later than 30 days before the discovery period ends; written order setting time, place, scope and examiner; report delivered on request.\n- Search summary of New York no-fault arbitration awards and Pennsylvania MVFRL decisions on peer reviews (e.g. https://aaa-nynf.modria.com/downloadAward/42428348): a peer review must state a factual basis and medical rationale; Pennsylvania peer review addresses reasonableness and necessity, not causation. Jurisdiction-specific; used for wording only.\n- Fishbain et al. (2003) on Waddell signs via research/case-library-sources-v2.md P8 — search summary.\n- Assumption: Texas third-party liability carriers commission records reviews informally; no Texas statute governs them. Not verified.\n\n**Specimen (SYNTHETIC).**\n```\nSYNTHETIC RECORD - RECORDS REVIEW - ALL IDENTIFIERS FICTITIOUS\nRequested by: Quillon Casualty Mutual (SYNTHETIC), claim SYN-BI-55120   Report date: 08/27/2026\nReviewer: Dr. Evander Pollitt-Rhys, MD, PM&R (SYNTHETIC)\nClaimant: Corentin Abelard-Moss (SYNTHETIC)   Date of loss: 05/02/2026\nRecords reviewed: ED 05/02/2026; PT notes 05/12/2026-07/31/2026; FCE 07/20/2026.\nSummary: The PT note of 06/12/2026 documents Waddell signs 0/5.\n  The PT note of 07/01/2026 documents no non-organic signs.\n  The FCE of 07/20/2026 documents Waddell 3/5 and inconsistent effort.\n  The PT note of 07/31/2026 documents full effort but symptom magnification with light touch.\nOpinions: Findings are consistent with a self-limited lumbar strain. Treatment after 07/20/2026 was\n  not reasonable or necessary. MMI as of 07/20/2026.\n/s/ Dr. Evander Pollitt-Rhys (SYNTHETIC)\n```\n(Credibility sentences across 4 dates: 06/12 and 07/01 are clean negations that must not flag; 07/20 and 07/31 must flag (07/31 mixes a\nclean and an adverse clause). 08/27/2026 is the report date; 07/20/2026 in the opinions is the reviewer's cut-off, not a visit.)\n\n---\n\n## 21. Product mapping and proposed packet mixes\n\n| Format | Main rule it exercises | Expected tool behavior |\n|---|---|---|\n| ED note | Dates (rollover), voice, pre-existing, hedges | Date = arrival; excerpt verbatim; PMH flag |\n| PT note | Gaps vs cancellations; plan vs actual; timed units | Cancellation is not an encounter; reason shown verbatim |\n| Chiro note + travel card | Cloned notes; checkbox OCR | Travel card rows need review when OCR-derived |\n| Radiology | Hedge and prior-imaging language; three dates | Exam date used; \"Comparison: prior\" flagged |\n| Op note | Indications ≠ causation; D:/T: dates | No causation inferred; surgery date used |\n| Pharmacy log | Refills, reversals, three price columns | Reversed lines excluded; prices to notes unless charge wording |\n| CMS-1500 | Implied decimal; date ranges; Item 14/31 dates | Code parses amounts as implied cents; line sum vs Item 28 compared; days = units checked |\n| UB-04 | 0001 total; FL 44 rate on the charge line; creation date; occurrence codes 01-06 | Total line not summed; rate not a charge (D-042 guard); any accident code = accident date |\n| Ledger | Running balance; voids; balance forward; fee schedule | Only dated charge lines counted; voids netted in code |\n| EOB | Double count of billed; CO/PR; mismatch with ledger | EOB amounts to notes, never added to charges; mismatch flagged |\n| LOP / lien | Non-record narrative; asserted totals | No entries created; amounts to notes only (D-019) |\n| Spanish note | Day-first dates; voice; translation labeling | Original excerpt; date convention suggestion (D-042) needs confirm |\n| Scanned intake | OCR glyphs, checkboxes, fax/stamp dates | OCR-derived items always need review; page image beside text |\n| EMS report | Call date and eight times; crew vs patient voice; refusal | One encounter on the call date; MIST wording attributed to EMS; refusal is an encounter without transport |\n| Ambulance invoice | Per-mile rate vs line; fractional units | Miles x rate recomputed in code; only line totals are charges |\n| §18.001 affidavit | Non-record page; duplicate attached bill; not causation | No encounter; duplicate deduped with both cites; totals recomputed |\n| Narrative letter | Causation statement; letter date; estimates | Causation shown verbatim and flagged, never upgraded; estimates to notes |\n| Office/specialist note | Copied ROS; recommended vs performed; estimates | Same-week contradiction surfaced; future dates not encounters |\n| Records review / IME | Adverse opinions; credibility words; report vs exam date | D-043 credibility flags; opinions attributed to the reviewer |\n\n**Proposed synthetic packet mixes** (round 1; the v2 library packets lib08-lib15 and the sections each needs are in\n`research/case-library-sources-v2.md`, \"Must contain\" table):\n1. *ER-only then gap*: EMS report + ED note + UB-04 (with 0001 line) + ED-physician CMS-1500 + radiology report + ambulance invoice + fax headers.\n2. *Chiro under LOP*: intake form (scanned) + LOP + chiro daily notes with a travel card + CMS-1500 with a grouped date range (clean and OCR\n   versions) + ledger with a void and a courtesy adjustment + narrative letter + §18.001 affidavit with a duplicate attached statement.\n3. *PT with health insurance*: PT eval + daily notes with two cancellations + ledger + EOB (CO-45, PR-1, CO-97) with the deliberate\n   ledger-vs-EOB mismatch.\n4. *Surgery*: MRI with prior comparison + ortho office note with a surgical estimate + op note with indications paragraph + surgeon/\n   assistant/anesthesia/facility bills on one date + inpatient UB-04 with a room-rate line.\n5. *Spanish-speaking client*: Spanish clinic note with a day-first date whose parts are both 12 or less + rate and charge on the same page +\n   pharmacy log with a reversed fill.\n\n---\n\n## 22. Cross-specimen consistency (Delphine Okonkwo-Vale timeline)\n\n| # | Mismatch found in round 1 review | Status | Expected tool behavior |\n|---|---|---|---|\n| 1 | Radiology compared with \"cervical radiographs\" though the ED did a CT | Fixed: comparison is the 05/15/2026 CT | None |\n| 2 | Chiro \"Visit #9\" on 06/03 with intake signed 05/29 | Fixed: Visit #4 (05/29 exam, 06/01-06/03 daily) | None |\n| 3 | PT \"Visit 7 of 24\" on 06/10 but the ledger shows only the eval and 06/10 | Fixed: Visit 2 of 12 | None |\n| 4 | Ledger shows no payments; EOB for the same DOS shows plan paid 16.00 and CO reductions | DELIBERATE | Billing analysis cites both and flags the mismatch; never picks paid vs incurred |\n| 5 | Op note \"12 weeks of therapy\"; PT 05/27-08/04 is 9.9 weeks | DELIBERATE | Excerpt verbatim and attributed; no automatic flag; golden truth never states 12 weeks |\n| 6 | PT plan \"3x/wk x 4 wks\" against 24 planned visits | Fixed: 2x/wk x 6 wks = 12 | None |\n| 7 | CMS-1500 line grouped 06/01-06/05 (5 days) with 3 units; travel card had non-consecutive dates | Fixed: grouped lines 06/01-06/03 = 3 days = 3 units; travel card marks match | Code checks days = units |\n| 8 | PT units: 35 timed minutes billed as 3 units | Fixed: 38 minutes = 3 units under the stated CMS method | None |\n| 9 | EMS arrival at destination 23:47 vs ED arrival 23:48 (new in round 2) | DELIBERATE (realistic) | Same encounter chain; no conflict flag |\n| 10 | §18.001 affidavit totals vs ledger (new in round 2) | Consistent: 445.00 / 0.00 / 400.00 | Attached statement deduped against section 10 |\n| 11 | Narrative letter \"since 05/29/2026\" and diagnoses vs chiro records and CMS-1500 (new in round 2) | Consistent | Letter cited as the letter; no new encounter |\n\n`python3 research/record_formats_check.py` re-checks rows 2, 3, 6, 7, 8 and 10 and every specimen total.\n\n---\n\n## 23. Assumptions, limits, gaps and the name-collision search\n\n- **Search-summary sources.** Sources marked \"search summary\" were not opened; their takeaways come from the search tool's summary. Opened:\n  NUCC 1500 manual, RI UB-04 instructions, HL7 NUBC occurrence-code list, Noridian chiro, EOB and ambulance-mileage pages, CMS bill guide,\n  CMS Claims Processing Manual ch. 15, NASEMSO time definitions, Montana NEMSIS disposition guide, CPRC §18.001/§18.002 (mirror), Hills v.\n  Donis 2021 opinion, Ezel narrative template, arXiv OCR paper, Jotform LOP packet.\n- **ACR report components.** The ACR page rendered only headings; the component list rests on secondary sources plus common practice.\n- **UB-04 specifics.** FL 44 accommodation-rate use and the creation date on line 23 are prior knowledge that the T-078 reviewer also\n  judged correct from working knowledge; both are marked \"unverified\" where they appear. Occurrence codes 01-06 come from an HL7 v2.4\n  rendering of the NUBC list; the current NUBC label for 01 may read \"accident/medical coverage\". Verify against the licensed NUBC manual\n  before quoting any of these in the submission.\n- **Payer variation.** CMS-1500, UB-04 and ambulance rules here are NUCC/NUBC, CMS and one Medicaid guide; commercial and auto carriers vary.\n- **Pharmacy \"charge\".** Whether U&C, plan paid or patient paid is the recoverable amount is a legal question the tool does not decide.\n- **Spanish phrasing** is drawn from Mexican and Spanish teaching templates; Central American and Caribbean usage may differ.\n- **OCR figures** come from one paper on smartphone photos of printed reports, not handwritten forms; handwriting is likely worse.\n- **Statute currency.** CPRC §18.001/§18.002 were read through a mirror (amended through 2019); the official site did not render. Not\n  checked for 2025-2026 amendments.\n- **Not covered.** Pain-management procedure notes (e.g. epidural steroid injection) and stand-alone work-status slips have no section;\n  the office-note section covers the visit that orders them.\n- **Name-collision search (2026-11-02).** Web searches for the invented provider, payer, firm and clinician names found no exact match for\n  Brightwater Spine & Wellness, Larkspur Hollow Physical Therapy, Quillfeather Regional Medical Center, Ferncastle Imaging Associates,\n  Thistledown Surgical Center, Mossgate Community Pharmacy or Harrowgate & Vey. Two names were replaced in round 2: \"Bluebonnet Mutual\n  Health Plan\" (Texas has real \"Bluebonnet\" health plans) became Quoinmere Mutual Health Plan, and \"Clínica Familiar Los Almendros\" /\n  \"Dra. Inés Valcárcel\" (a similarly named clinic and a real surname match) became Consultorio Médico Peñaverde / Dra. Itziar Orbezua Lanz.\n  Names added in round 2 (Fernhollow County EMS, Gallowmere Records Retrieval, Saltmarrow General Hospital, Quillon Casualty Mutual and the\n  clinicians) were built from uncommon word pairs and not searched individually. Any remaining resemblance is unintended; packets built\n  from these specimens still pass `research/validate_library.py`.\n"
}
````

### User / tool · 2026-11-02T03:40:25.895Z

**tool result**
````
File created successfully at: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/tail.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:40:39.703Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && python3 - \"$S/tail.md\" <<'EOF'\nimport pathlib,sys\np=pathlib.Path(\"research/record-formats.md\"); t=p.read_text()\ntail=pathlib.Path(sys.argv[1]).read_text()\ntail=tail.replace(\"Delphine Okonkwo-Vale (SYNTHETIC) from 05/27/2026 through 07/15/2026,\",\"Delphine Okonkwo-Vale (SYNTHETIC) from 05/27/2026 through 06/10/2026,\")\ntail=tail.replace(\"| 5 | Op note \\\"12 weeks of therapy\\\"; PT 05/27-08/04 is 9.9 weeks |\",\"| 5 | Op note \\\"12 weeks of therapy\\\"; PT eval 05/27 to surgery 08/04 is 9.9 weeks |\")\ni=t.index(\"## 15. Product mapping\")\nt=t[:i]+tail\nt=t.replace(\"The PT records run from 05/27/2026 to 08/04/2026 = 69 days, about 9.9 weeks.\",\"From the PT evaluation (05/27/2026) to surgery (08/04/2026) is 69 days, about 9.9 weeks.\")\np.write_text(t)\nEOF\ngrep -n \"^## \" research/record-formats.md; grep -c \"SYNTHETIC RECORD\\|REGISTRO SINTÉTICO\" research/record-formats.md; grep -n \"9.9 weeks\" research/record-formats.md",
 "description": "Splice new sections into record-formats.md"
}
````

### User / tool · 2026-11-02T03:40:39.839Z

**tool result**
````
22:## 1. Cross-cutting traps (apply to every format)
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
21
295:(DELIBERATE: "12 weeks of therapy" is the surgeon's recital. From the PT evaluation (05/27/2026) to surgery (08/04/2026) is 69 days, about 9.9 weeks.
1042:| 5 | Op note "12 weeks of therapy"; PT eval 05/27 to surgery 08/04 is 9.9 weeks | DELIBERATE | Excerpt verbatim and attributed; no automatic flag; golden truth never states 12 weeks |
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:41:35.812Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/record_formats_check.py",
 "content": "#!/usr/bin/env python3\n\"\"\"Re-check the SYNTHETIC specimens in research/record-formats.md (T-078 round 2).\n\nEach specimen claims to follow a rule (NUCC grouping, CMS 8-minute rule, UB-04 rate x days, totals). This script re-adds them in code so a\nlater edit cannot silently break one. Exit 0 = every check passes.   Run: python3 research/record_formats_check.py\n\"\"\"\nimport datetime as dt, pathlib, re, sys\nfrom decimal import Decimal as D\n\nDOC = pathlib.Path(__file__).resolve().parent / \"record-formats.md\"\nMONEY = r\"\\(?-?\\d{1,3}(?:,\\d{3})*\\.\\d\\d\\)?-?\"\nresults = []\n\n\ndef check(name, ok, detail=\"\"):\n    results.append((name, bool(ok), detail))\n\n\ndef money(s):\n    neg = s.startswith(\"(\") or s.endswith(\"-\") or s.startswith(\"-\")\n    v = D(s.strip(\"()-\").replace(\",\", \"\"))\n    return -v if neg else v\n\n\ndef sections(text):\n    parts = re.split(r\"^## (\\d+)\\. \", text, flags=re.M)\n    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}\n\n\ndef blocks(sec):\n    return re.findall(r\"```\\n(.*?)```\", sec, re.S)\n\n\ndef mmddyy(s):\n    s = s.replace(\"O\", \"0\")\n    return dt.date(2000 + int(s[4:6]), int(s[0:2]), int(s[2:4]))\n\n\ndef main():\n    text = DOC.read_text()\n    S = sections(text)\n    formats = [n for n in S if 2 <= n <= 20]\n    words = {19: \"nineteen\"}\n    check(\"intro format count matches sections 2-20\", f\"describes the {words.get(len(formats), '?')} document\" in text,\n          f\"{len(formats)} format sections\")\n    for n in formats:\n        bs = blocks(S[n])\n        check(f\"§{n} has a specimen\", bs)\n        for b in bs:\n            check(f\"§{n} specimen labeled synthetic\", re.search(r\"SYNTHETIC|SINTÉTICO\", b.splitlines()[0]), b.splitlines()[0][:60])\n\n    # §3 PT: CMS 8-minute rule on total timed minutes; plan count.\n    pt = blocks(S[3])[0]\n    timed = [(int(m), int(u)) for m, u in re.findall(r\"\\b97\\d{3} \\w+\\s+(\\d+) min\\s+(\\d+)u\", pt)]\n    total = sum(m for m, _ in timed)\n    cms_units = (total + 7) // 15 if total >= 8 else 0\n    check(\"PT timed minutes total stated\", f\"Total timed {total} min\" in pt, f\"{total} min\")\n    check(\"PT units = CMS 8-minute rule\", sum(u for _, u in timed) == cms_units, f\"{total} min -> {cms_units} units\")\n    check(\"PT per-code (AMA) units agree\", all(u == (m + 7) // 15 for m, u in timed))\n    v = re.search(r\"Visit (\\d+) of (\\d+)\", pt)\n    plan = re.search(r\"(\\d)x/wk x (\\d+) wks\", pt)\n    check(\"PT plan visits = frequency x weeks\", v and plan and int(v.group(2)) == int(plan.group(1)) * int(plan.group(2)))\n\n    # §4 travel card marks per column.\n    chiro = blocks(S[4])[0]\n    hdr = next(l for l in chiro.splitlines() if l.startswith(\"DATE\"))\n    cols = [c.strip() for c in hdr.split(\"|\")]\n    marks = {}\n    for l in chiro.splitlines():\n        if re.match(r\"\\d\\d/\\d\\d\\s+\\|\", l):\n            cells = [c.strip() for c in l.split(\"|\")]\n            for c, val in zip(cols, cells):\n                if val == \"x\":\n                    marks.setdefault(c, set()).add(dt.date(2026, int(cells[0][:2]), int(cells[0][3:5])))\n\n    # §8 CMS-1500 clean: days = units, grouped dates on the travel card, line sum = Item 28.\n    clean, ocr = blocks(S[8])[:2]\n    lines = re.findall(r\"^\\s+(\\d{6})\\s+(\\d{6})\\s+\\d+\\s+(\\w+)\\s+\\w+\\s+(\\d+) \\| (\\d\\d)\\s+(\\d+)\", clean, re.M)\n    check(\"CMS-1500 clean has service lines\", len(lines) >= 3, f\"{len(lines)} lines\")\n    col_for = {\"97014\": \"ES\", \"97010\": \"H/C\", \"98941\": \"C\"}\n    line_sum = D(0)\n    for f, t, code, dollars, cents, units in lines:\n        a, b = mmddyy(f), mmddyy(t)\n        days = (b - a).days + 1\n        check(f\"CMS-1500 {code} {f}-{t}: days = units\", days == int(units), f\"{days} days, {units} units\")\n        dates = {a + dt.timedelta(d) for d in range(days)}\n        check(f\"CMS-1500 {code} {f}-{t}: every date marked on travel card\", dates <= marks.get(col_for.get(code, \"\"), set()))\n        line_sum += D(f\"{dollars}.{cents}\")\n    item28 = re.search(r\"28\\. TOTAL CHARGE\\s+(\\d+) \\| (\\d\\d)\", clean)\n    check(\"CMS-1500 line sum = Item 28\", item28 and line_sum == D(f\"{item28.group(1)}.{item28.group(2)}\"), str(line_sum))\n\n    # §8 CMS-1500 OCR: at least one separator-less amount with its truth stated; truths add up to the Item 28 truth.\n    truths, bare = [], 0\n    for l in ocr.splitlines():\n        m = re.search(r\"<- truth (\\d+\\.\\d\\d)\", l)\n        if not m:\n            continue\n        if re.search(r\"\\s\\d{4,5}\\s\", l.split(\"<-\")[0]):\n            bare += 1\n        if l.lstrip().startswith((\"24.\", \"0\", \"O\")):\n            truths.append(D(m.group(1)))\n        elif \"28.\" in l:\n            t28 = D(m.group(1))\n    check(\"CMS-1500 OCR has separator-less amounts with truth\", bare >= 1, f\"{bare} lines\")\n    check(\"CMS-1500 OCR truths sum to Item 28 truth\", truths and sum(truths) == t28 == line_sum, str(sum(truths)))\n\n    # §9 UB-04: lines sum to 0001; a room line where rate x days = charge; occurrence codes differ and are 01-06.\n    occ = []\n    room_ok = False\n    for b in blocks(S[9]):\n        occ.append(re.search(r\"OCCURRENCE\\s+CODE (\\d\\d)\", b).group(1))\n        tot47 = D(0); tot48 = D(0); allm = D(0); total = None\n        for l in b.splitlines():\n            m = re.match(r\"(\\d{4})\\s{2,}\", l)\n            if not m:\n                continue\n            ms = [money(x) for x in re.findall(MONEY, l)]\n            allm += sum(ms)\n            rev = m.group(1)\n            if rev == \"0001\":\n                total = ms\n                continue\n            if rev.startswith(\"01\"):\n                rate, charge = ms[0], ms[1]\n                days = int(re.search(r\"\\d\\.\\d\\d\\s+(\\d+)\\s+\\d\", l.replace(\",\", \"\")).group(1))\n                room_ok = room_ok or rate * days == charge\n                check(f\"UB-04 room line {rev}: rate x days = charge\", rate * days == charge, f\"{rate} x {days} = {charge}\")\n                tot47 += charge\n            else:\n                tot47 += ms[0]\n                tot48 += ms[1] if len(ms) > 1 else 0\n        check(\"UB-04 lines sum to 0001 FL47\", total and total[0] == tot47, f\"{tot47} vs {total}\")\n        if total and len(total) > 1:\n            check(\"UB-04 FL48 lines sum to 0001 FL48\", total[1] == tot48)\n        if room_ok:\n            naive = f\"{allm:,.2f}\"\n            check(\"UB-04 naive-sum figure stated in the note\", naive in S[9], naive)\n    check(\"UB-04 has a rate-on-charge-line specimen\", room_ok)\n    check(\"UB-04 occurrence codes are accident codes 01-06 and vary\", all(c in {\"01\", \"02\", \"03\", \"04\", \"05\", \"06\"} for c in occ)\n          and len(set(occ)) >= 2, str(occ))\n\n    # §10 ledger: running balance and totals.\n    led = blocks(S[10])[0]\n    bal = D(0); ch = D(0); adj = D(0)\n    for l in led.splitlines():\n        if not re.match(r\"\\d\\d/\\d\\d/\\d\\d\", l):\n            continue\n        ms = [money(x) for x in re.findall(MONEY, l)]\n        if \" ADJ \" in l:\n            adj += ms[0]; bal -= ms[0]\n        else:\n            ch += ms[0]; bal += ms[0]\n        check(f\"ledger running balance {l[:8]}\", bal == ms[-1], f\"{bal} vs {ms[-1]}\")\n    tl = re.search(r\"TOTAL CHARGES ([\\d.,]+)\\s+TOTAL PMTS ([\\d.,]+)\\s+TOTAL ADJ \\(([\\d.,]+)\\)\\s+BALANCE DUE ([\\d.,]+)\", led)\n    check(\"ledger totals\", tl and (D(tl.group(1)), D(tl.group(3)), D(tl.group(4))) == (ch, adj, bal), f\"{ch} {adj} {bal}\")\n\n    # §11 EOB arithmetic per line and totals.\n    eob = blocks(S[11])[0]\n    sums = [D(0)] * 7\n    for l in eob.splitlines():\n        if re.match(r\"\\d\\d/\\d\\d/\\d\\d\", l):\n            b_, disc, allw, ded, coin, paid, owe = [D(x) for x in re.findall(r\"\\d+\\.\\d\\d\", l)]\n            check(f\"EOB line {l[10:15]}\", b_ - disc == allw and allw - ded - coin == paid and ded + coin == owe)\n            sums = [s + v for s, v in zip(sums, (b_, disc, allw, ded, coin, paid, owe))]\n        elif l.startswith(\"TOTAL\"):\n            check(\"EOB totals\", [D(x) for x in re.findall(r\"\\d+\\.\\d\\d\", l)] == sums)\n\n    # §13 Spanish: a day-first date with both parts <= 12 and its truth stated.\n    sp = S[13]\n    amb = [d for d in re.findall(r\"\\b(\\d\\d)/(\\d\\d)/(\\d{4})\\b\", blocks(sp)[0]) if int(d[0]) <= 12 and int(d[1]) <= 12]\n    months = [\"January\", \"February\", \"March\", \"April\", \"May\", \"June\", \"July\", \"August\", \"September\", \"October\", \"November\", \"December\"]\n    check(\"Spanish specimen has an ambiguous day-first date with stated truth\",\n          any(f\"{int(d)} {months[int(m) - 1]} {y}\" in sp for d, m, y in amb), str(amb))\n\n    # §15 EMS: call times in order.\n    ems = blocks(S[15])[0]\n    times = re.findall(r\"(?:PSAP|Notified|En route|On scene|At pt|Left scene|At dest|Transfer of care) (\\d\\d):(\\d\\d)\", ems.split(\"---\")[0])\n    mins = [int(h) * 60 + int(m) for h, m in times]\n    check(\"EMS times ascend\", len(mins) == 8 and mins == sorted(mins), str(times))\n\n    # §16 ambulance: units x rate = charge; lines sum to total; mileage units fractional.\n    amb_b = blocks(S[16])[0]\n    tot = D(0)\n    for code, units, rate, charge in re.findall(r\"(A04\\d\\d-\\w\\w).*?\\s([\\d.]+)\\s+([\\d,]+\\.\\d\\d)\\s+([\\d,]+\\.\\d\\d)\\s*$\", amb_b, re.M):\n        u, r, c = D(units), money(rate), money(charge)\n        check(f\"ambulance {code}: units x rate = charge\", u * r == c, f\"{u} x {r} = {c}\")\n        if code.startswith(\"A0425\"):\n            check(\"ambulance mileage units carry a tenth\", \".\" in units)\n        tot += c\n    tc = re.search(r\"TOTAL CHARGES\\s+([\\d,]+\\.\\d\\d)\", amb_b)\n    check(\"ambulance lines sum to total\", tc and money(tc.group(1)) == tot, str(tot))\n\n    # §17 affidavit amounts match the §10 ledger.\n    aff = blocks(S[17])[0]\n    a = re.search(r\"charged: \\$([\\d,.]+)\\.\\s+Amount paid: \\$([\\d,.]+)\\.\\s+Amount unpaid.*?\\$([\\d,.]+)\\.\", aff)\n    check(\"affidavit charged/paid/unpaid = ledger\", a and (D(a.group(1)), D(a.group(2)), D(a.group(3))) == (ch, D(0), bal),\n          a.groups() if a else \"no match\")\n\n    bad = [r for r in results if not r[1]]\n    for name, ok, detail in results:\n        if not ok or \"-v\" in sys.argv:\n            print((\"ok   \" if ok else \"FAIL \") + name + (f\"  [{detail}]\" if detail else \"\"))\n    print(f\"record_formats_check: {len(results) - len(bad)}/{len(results)} checks pass\")\n    return 1 if bad else 0\n\n\nif __name__ == \"__main__\":\n    sys.exit(main())\n"
}
````

### User / tool · 2026-11-02T03:41:35.871Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/research/record_formats_check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:41:37.849Z

**tool call — Bash**
````
{
 "command": "python3 research/record_formats_check.py -v",
 "description": "Run specimen checks"
}
````

### User / tool · 2026-11-02T03:41:37.958Z

**tool result (error)**
````
Exit code 1
ok   intro format count matches sections 2-20  [19 format sections]
ok   §2 has a specimen
ok   §2 specimen labeled synthetic  [SYNTHETIC RECORD - NOT A REAL PATIENT]
ok   §3 has a specimen
ok   §3 specimen labeled synthetic  [SYNTHETIC RECORD]
ok   §4 has a specimen
ok   §4 specimen labeled synthetic  [SYNTHETIC RECORD]
ok   §5 has a specimen
ok   §5 specimen labeled synthetic  [SYNTHETIC RECORD]
ok   §6 has a specimen
ok   §6 specimen labeled synthetic  [SYNTHETIC RECORD]
ok   §7 has a specimen
ok   §7 specimen labeled synthetic  [SYNTHETIC RECORD]
ok   §8 has a specimen
ok   §8 specimen labeled synthetic  [SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL ]
ok   §8 specimen labeled synthetic  [SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FIC]
ok   §9 has a specimen
ok   §9 specimen labeled synthetic  [SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS]
ok   §9 specimen labeled synthetic  [SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS]
ok   §10 has a specimen
ok   §10 specimen labeled synthetic  [SYNTHETIC RECORD]
ok   §11 has a specimen
ok   §11 specimen labeled synthetic  [SYNTHETIC RECORD - THIS IS NOT A BILL]
ok   §12 has a specimen
ok   §12 specimen labeled synthetic  [SYNTHETIC RECORD]
ok   §13 has a specimen
ok   §13 specimen labeled synthetic  [REGISTRO SINTÉTICO / SYNTHETIC RECORD]
ok   §14 has a specimen
ok   §14 specimen labeled synthetic  [SYNTHETIC RECORD]
ok   §15 has a specimen
ok   §15 specimen labeled synthetic  [SYNTHETIC RECORD - PATIENT CARE REPORT - ALL IDENTIFIERS FIC]
ok   §16 has a specimen
ok   §16 specimen labeled synthetic  [SYNTHETIC RECORD - AMBULANCE INVOICE - ALL IDENTIFIERS FICTI]
ok   §17 has a specimen
ok   §17 specimen labeled synthetic  [SYNTHETIC RECORD - RECORDS CERTIFICATION COVER - ALL IDENTIF]
ok   §18 has a specimen
ok   §18 specimen labeled synthetic  [SYNTHETIC RECORD]
ok   §19 has a specimen
ok   §19 specimen labeled synthetic  [SYNTHETIC RECORD]
ok   §20 has a specimen
ok   §20 specimen labeled synthetic  [SYNTHETIC RECORD - RECORDS REVIEW - ALL IDENTIFIERS FICTITIO]
ok   PT timed minutes total stated  [38 min]
ok   PT units = CMS 8-minute rule  [38 min -> 3 units]
ok   PT per-code (AMA) units agree
ok   PT plan visits = frequency x weeks
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
ok   ledger running balance 05/27/26  [210.00 vs 210.00]
ok   ledger running balance 06/10/26  [340.00 vs 340.00]
ok   ledger running balance 06/10/26  [410.00 vs 410.00]
ok   ledger running balance 06/10/26  [445.00 vs 445.00]
ok   ledger running balance 06/10/26  [375.00 vs 375.00]
ok   ledger running balance 06/10/26  [445.00 vs 445.00]
FAIL ledger running balance 07/15/26  [490.00 vs 400.00]
FAIL ledger totals  [445.00 -45.00 490.00]
ok   EOB line 97110
ok   EOB line 97140
ok   EOB line 97014
ok   EOB totals
ok   Spanish specimen has an ambiguous day-first date with stated truth  [[('07', '06', '2026')]]
ok   EMS times ascend  [[('23', '12'), ('23', '13'), ('23', '14'), ('23', '21'), ('23', '22'), ('23', '36'), ('23', '47'), ('23', '52')]]
ok   ambulance A0427-SH: units x rate = charge  [1 x 1450.00 = 1450.00]
ok   ambulance A0425-SH: units x rate = charge  [8.7 x 22.50 = 195.75]
ok   ambulance mileage units carry a tenth
ok   ambulance lines sum to total  [1645.75]
FAIL affidavit charged/paid/unpaid = ledger  [('445.00', '0.00', '400.00')]
record_formats_check: 82/85 checks pass
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:41:41.579Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"research/record_formats_check.py\"); t=p.read_text()\nt=t.replace(\"            adj += ms[0]; bal -= ms[0]\",\"            adj += abs(ms[0]); bal -= abs(ms[0])\")\np.write_text(t)\nEOF\npython3 research/record_formats_check.py; python3 research/validate_library.py --self-test",
 "description": "Fix adjustment sign and rerun checks"
}
````

### User / tool · 2026-11-02T03:41:41.779Z

**tool result**
````
record_formats_check: 85/85 checks pass
self-test: ok (354 planted variants caught, 16 caption names covered)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:41:48.956Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p $S/neg2 && sed 's/060126   060326   11     97010              A      45 | 00       3/060126   060526   11     97010              A      45 | 00       3/' research/record-formats.md > $S/neg2/record-formats.md && cp research/record_formats_check.py $S/neg2/ && python3 -I $S/neg2/record_formats_check.py | tail -4; grep -n \"Waddell\\|Texas\\|Medicare\" research/record-formats.md | head -5",
 "description": "Negative test: planted grouping error must fail"
}
````

### User / tool · 2026-11-02T03:41:49.083Z

**tool result**
````
FAIL CMS-1500 97010 060126-060526: days = units  [5 days, 3 units]
FAIL CMS-1500 97010 060126-060526: every date marked on travel card
record_formats_check: 83/85 checks pass
4:types a Texas PI paralegal typically receives, so the packet generator can produce realistic, **fully synthetic** records that exercise the
53:`(45.00)`, `-45.00`, `45.00-` or `45.00 CR`. Spanish-language clinics in Mexico and much of Latin America use `$1.250,00`; Texas clinics
177:- Medicare guidance requires the exact segment, not just a region; PI notes often list both. Do not count segments as visits.
423:- Payer guides disagree on whether Medicare's FL 47 total excludes non-covered charges; compute from lines and keep both.
428:- McGraw-Hill chapter summary on FL 47/48 Medicare treatment: https://highered.mheducation.com/sites/0073520896/student_view0/chapter12/chapter_summary.html — search summary.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:41:52.734Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport sys,re;sys.path.insert(0,'research')\nimport validate_library as v\nt=open('research/record-formats.md').read()\nfor i,b in enumerate(re.findall(r'\\`\\`\\`\\n(.*?)\\`\\`\\`',t,re.S)):\n    h=v.scan_text(b)\n    if h: print(i,b.splitlines()[0][:50],h)\nprint('done')\"",
 "description": "Scan specimens against denylist"
}
````

### User / tool · 2026-11-02T03:41:52.793Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:41:58.634Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat > $S/scan_specimens.py <<'EOF'\nimport sys, re\nsys.path.insert(0, \"research\")\nimport validate_library as v\nt = open(\"research/record-formats.md\").read()\nfence = chr(96) * 3\nfor i, b in enumerate(re.findall(fence + r\"\\n(.*?)\" + fence, t, re.S)):\n    h = v.scan_text(b)\n    if h:\n        print(i, b.splitlines()[0][:50], h)\nprint(\"done\")\nEOF\npython3 $S/scan_specimens.py",
 "description": "Scan specimens against denylist"
}
````

### User / tool · 2026-11-02T03:41:58.785Z

**tool result**
````
done
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:42:03.491Z

**tool call — Bash**
````
{
 "command": "grep -n \"ime_credibility\\|Hampton\\|withdrawn\\|six categories\\|\\*\\*Record features:\\*\\*\" research/case-library-sources-v2.md; grep -rn \"lib12_ime\" board/cards evals research 2>/dev/null | head; git diff --stat -- research/",
 "description": "Check leftovers and diff stat"
}
````

### User / tool · 2026-11-02T03:42:03.608Z

**tool result**
````
27:   (Garza, Rodriguez, Hills, Gunn, Hampton, Castro, Powell, Anderson, Flores) are banned as invented-name choices too,
78:  rehearing denied, the 2020 opinion withdrawn and a substitute memorandum opinion issued; petition for review No. 21-0287
80:  https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the withdrawn 2020 opinion only.
399:Hampton
424:- Texas DWC Appeals Panel decisions (P9) were seen only as a search excerpt (page returned 403). Hampton v. Miskell was
 research/case-library-sources-v2.md | 253 ++++++++++++-----
 research/record-formats.md          | 527 +++++++++++++++++++++++++++++++-----
 research/validate_library.py        | 168 ++++++++++--
 3 files changed, 805 insertions(+), 143 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:42:08.118Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/research-workflow-pitfalls.md"
}
````

### User / tool · 2026-11-02T03:42:08.124Z

**tool result**
````
1	---
2	name: research-workflow-pitfalls
3	description: Researcher tooling pitfalls in this repo: git-guard needs add/commit as separate commands; WebFetch cannot read PDFs but saves them for pdftotext; source-marking convention
4	metadata:
5	  type: feedback
6	---
7	
8	Stage and commit in **separate Bash calls** (`git add <path>` then `git commit -m ... -- <path>`); git-guard blocks a combined command so the secret scan sees the staged set.
9	**Why:** hook rejected `git add && git commit` on T-078.
10	**How to apply:** every commit of research/ or personas/.
11	
12	WebFetch returns "binary PDF" for PDF URLs but saves the file under the tool-results dir; copy it into a fresh scratchpad subdir and run `pdftotext -layout` (at /opt/homebrew/bin) to read official manuals (NUCC 1500, Medicaid UB-04 guides worked this way).
13	**Why:** primary-source manuals (NUCC, NUBC, CMS) are PDFs; the search summary alone is weaker evidence.
14	**How to apply:** prefer extracting the primary PDF over citing a search snippet.
15	
16	Source convention in research/*.md (since T-052, kept in T-078): each source line says **opened** vs "search summary" vs "not opened", and facts from prior knowledge are listed under Assumptions. Specimens use invented names, `SYN-` identifiers, 555-01xx phones, and a SYNTHETIC header. See [[record-formats-key-traps]].
17	
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:42:22.645Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"research-workflow-pitfalls.md\"); t=p.read_text()\nt=t.replace(\"description: Researcher tooling pitfalls in this repo: git-guard needs add/commit as separate commands; WebFetch cannot read PDFs but saves them for pdftotext; source-marking convention\",\n\"description: Researcher tooling pitfalls in this repo: git-guard needs add/commit as separate commands; PDFs via curl+pdftotext; Texas court/statute retrieval; denylist + self-check rule; source-marking convention\")\nt+=\"\"\"\nTexas sources: opinion PDFs come from the docket page `https://search.txcourts.gov/Case.aspx?cn=<No>&coa=coa<NN>` (WebFetch lists event links; `curl -L` the SearchMedia URL, then pdftotext). It shows withdrawn/substitute opinions a firm write-up hides (Hills v. Donis: 2020 op withdrawn, 2021-02-11 substitute). statutes.capitol.texas.gov is a JS app: use the texas.public.law mirror (fetch tool caps quotes at 125 chars). CourtListener API needs auth. git-guard also rejects Bash commands containing backslash-escaped backticks: write a script file instead.\n**Why:** T-077/T-078 round 2 lost time on 403s and a superseded opinion.\n**How to apply:** verify every case date/history on the docket before citing; give court, district and docket/reporter in every caption or drop the source.\n\nAny real name cited in research/case-library-sources*.md must be on the DENYLIST in research/validate_library.py in the same commit, and the doc carries a \"## Denylist additions\" text block that `--self-test` cross-checks (planted mixed-case names must fail; every \"X v. Y\" caption token must be listed). Specimens in record-formats.md must pass scan_text too (state written as \"TX\").\n**Why:** T-077 review major: doc said \"add names before packets are built\" but nothing enforced it.\n**How to apply:** run `python3 research/validate_library.py --self-test` and `python3 research/record_formats_check.py` before handing off research cards.\n\"\"\"\np.write_text(t)\nq=pathlib.Path(\"record-formats-key-traps.md\"); s=q.read_text()\ns=s.replace(\"**How to apply:** when building library cases, lexicon entries, or reviewing billing/OCR cards, start from §1 and §15 of that file. Unverified-from-memory items are listed in its §16.\",\n\"\"\"- Round 2 (2026-11-02) added §15-20 (EMS report, ambulance invoice with fractional mileage x rate, CPRC 18.001 affidavit + cover page, narrative letter, office note, records-review/IME), a decimal-less OCR 1500, an inpatient UB-04 room-rate line, §22 cross-specimen table (fixed vs DELIBERATE), and research/record_formats_check.py.\n- Occurrence codes 01-06 are all accident codes (not just 01); 1500 grouping only on consecutive days with days = units; PT units must follow a stated 8-minute method.\n**How to apply:** when building library cases, lexicon entries, or reviewing billing/OCR cards, start from §1, §21 and §22 of that file. Unverified items are in §23.\"\"\")\nq.write_text(s)\nm=pathlib.Path(\"MEMORY.md\"); u=m.read_text()\nu=u.replace(\"- [Research workflow pitfalls](research-workflow-pitfalls.md) — separate git add/commit; pdftotext for PDF sources; opened-vs-summary source marking\",\n\"- [Research workflow pitfalls](research-workflow-pitfalls.md) — separate git add/commit; pdftotext; TX docket/statute retrieval; denylist self-test rule\")\nu=u.replace(\"- [Record-format key traps](record-formats-key-traps.md) — CMS-1500 implied decimal, UB-04 0001/FL44 rate, non-service dates, Spanish dates (T-078)\",\n\"- [Record-format key traps](record-formats-key-traps.md) — CMS-1500 implied decimal, UB-04 0001/FL44 rate, occ codes 01-06, 1500 grouping, EMS/affidavit (T-078)\")\nm.write_text(u)\nEOF\ncat MEMORY.md",
 "description": "Update researcher agent memory"
}
````

### User / tool · 2026-11-02T03:42:22.768Z

**tool result**
````
- [Research workflow pitfalls](research-workflow-pitfalls.md) — separate git add/commit; pdftotext; TX docket/statute retrieval; denylist self-test rule
- [Record-format key traps](record-formats-key-traps.md) — CMS-1500 implied decimal, UB-04 0001/FL44 rate, occ codes 01-06, 1500 grouping, EMS/affidavit (T-078)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:42:27.095Z

**tool call — Bash**
````
{
 "command": "git add research/case-library-sources-v2.md research/validate_library.py",
 "description": "Stage T-077 files"
}
````

### User / tool · 2026-11-02T03:42:27.200Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:42:31.715Z

**tool call — Bash**
````
{
 "command": "git commit -m \"fix(research): v2 case-library denylist enforced with self-test, tagged record features, verified citations (T-077 r2)\n\n- validate_library.py: v2 real names added (case- and accent-insensitive), capitalised-only terms for\n  common words, Waddell eponym allowed, --self-test plants mixed-case names and cross-checks the doc's\n  Denylist additions block and every X v. Y caption\n- v2 doc: Record features tagged from source / our inference; Hills v. Donis re-cited to the 2021\n  substitute opinion (read in full); P17 source replaced (Hampton not retrievable); P5 six items\n  reworded; P6 case type; stage/entry, must-contain and formats columns for lib08-lib15\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- research/case-library-sources-v2.md research/validate_library.py && git log --oneline -1",
 "description": "Commit T-077 changes"
}
````

### User / tool · 2026-11-02T03:42:32.050Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
[main 5c2cb2f] fix(research): v2 case-library denylist enforced with self-test, tagged record features, verified citations (T-077 r2)
 2 files changed, 341 insertions(+), 80 deletions(-)
5c2cb2f fix(research): v2 case-library denylist enforced with self-test, tagged record features, verified citations (T-077 r2)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:42:33.743Z

**tool call — Bash**
````
{
 "command": "git add research/record-formats.md research/record_formats_check.py",
 "description": "Stage T-078 files"
}
````

### User / tool · 2026-11-02T03:42:33.849Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:42:38.884Z

**tool call — Bash**
````
{
 "command": "git commit -m \"fix(research): record formats r2 - NUCC-consistent 1500, OCR and room-rate specimens, six new formats (T-078 r2)\n\n- CMS-1500: grouped lines now consecutive days = units, matching the travel card; OCR rendering with\n  decimal-less amounts and stated truth\n- UB-04: inpatient specimen with FL44 rate x FL46 days = FL47 charge; occurrence codes 01-06 as the\n  accident family (code 03 used); creation-date convention marked unverified\n- New sections 15-20: EMS run report, ambulance invoice (fractional mileage), CPRC 18.001 affidavit\n  + cover page, treating narrative letter, office/specialist note, records-review/IME report\n- PT units follow the stated 8-minute rule; Spanish day-first date 07/06/2026; cross-specimen table\n  (fixed vs DELIBERATE); name-collision search, two names replaced\n- research/record_formats_check.py re-adds every specimen (85 checks)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- research/record-formats.md research/record_formats_check.py && git log --oneline -1",
 "description": "Commit T-078 changes"
}
````

### User / tool · 2026-11-02T03:42:39.209Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
[main 327ce46] fix(research): record formats r2 - NUCC-consistent 1500, OCR and room-rate specimens, six new formats (T-078 r2)
 2 files changed, 672 insertions(+), 63 deletions(-)
 create mode 100644 research/record_formats_check.py
327ce46 fix(research): record formats r2 - NUCC-consistent 1500, OCR and room-rate specimens, six new formats (T-078 r2)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:42:40.568Z

Now board updates: AC evidence, handoff, move, commit record.

### Assistant · claude-opus-5-5 · 2026-11-02T03:42:48.195Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && \\\n$B ac T-077 --check 1 --agent researcher --evidence \"r2 (5c2cb2f): 17 patterns; every Record-features line tagged (from source)/(our inference); Hills v. Donis re-cited to the 2021-02-11 substitute mem. op. (read in full via search.txcourts.gov docket), pet. denied 2021-07-23; P17 source replaced by Castro 1997 PMID 9455663 (Hampton not retrievable); P4/P17 marked theme-only; P5 items 1-4,6 vs 5; P6 case type; statute currency line\" && \\\n$B ac T-077 --check 2 --agent researcher --evidence \"r2 (5c2cb2f): Denylist additions block (46 terms) mirrored in research/validate_library.py DENYLIST_V2/DENY_CAPITALISED, case+accent-insensitive; 'python3 research/validate_library.py --self-test' -> ok (354 planted variants caught, 16 caption names covered); negative test (Garza removed) fails; library scan ok (7 packets, 72 terms); packet table has stage/entry, must-contain and record-formats § columns for lib08-lib15\" && \\\n$B ac T-078 --check 1 --agent researcher --evidence \"r2 (327ce46): research/record-formats.md now 19 formats; added §15 EMS PCR, §16 ambulance invoice, §17 CPRC 18.001 affidavit + cover, §18 narrative letter, §19 office/specialist note, §20 records-review/IME (fields, wording, traps, sources; CMS ch.15, NASEMSO, MT NEMSIS, CPRC mirror, Hills 2021, Ezel opened); occurrence codes 01-06; unverified markers; §22 cross-specimen table; §23 name-collision search\" && \\\n$B ac T-078 --check 2 --agent researcher --evidence \"r2 (327ce46): 21 SYNTHETIC specimens; 'python3 research/record_formats_check.py' -> 85/85 (1500 days=units vs travel card, OCR decimal-less truths sum to Item 28, UB-04 room 1850x3=5550 and 0001 totals, ledger, EOB, PT 8-minute rule, Spanish 07/06/2026 truth, EMS times, ambulance 8.7x22.50, affidavit = ledger); planted 060126-060526 grouping fails; all specimens pass validate_library scan_text\"",
 "description": "Record AC evidence on both cards"
}
````

### User / tool · 2026-11-02T03:42:48.491Z

**tool result**
````
AC 1 checked: r2 (5c2cb2f): 17 patterns; every Record-features line tagged (from source)/(our inference); Hills v. Donis re-cited to the 2021-02-11 substitute mem. op. (read in full via search.txcourts.gov docket), pet. denied 2021-07-23; P17 source replaced by Castro 1997 PMID 9455663 (Hampton not retrievable); P4/P17 marked theme-only; P5 items 1-4,6 vs 5; P6 case type; statute currency line
AC 2 checked: r2 (5c2cb2f): Denylist additions block (46 terms) mirrored in research/validate_library.py DENYLIST_V2/DENY_CAPITALISED, case+accent-insensitive; 'python3 research/validate_library.py --self-test' -> ok (354 planted variants caught, 16 caption names covered); negative test (Garza removed) fails; library scan ok (7 packets, 72 terms); packet table has stage/entry, must-contain and record-formats § columns for lib08-lib15
AC 1 checked: r2 (327ce46): research/record-formats.md now 19 formats; added §15 EMS PCR, §16 ambulance invoice, §17 CPRC 18.001 affidavit + cover, §18 narrative letter, §19 office/specialist note, §20 records-review/IME (fields, wording, traps, sources; CMS ch.15, NASEMSO, MT NEMSIS, CPRC mirror, Hills 2021, Ezel opened); occurrence codes 01-06; unverified markers; §22 cross-specimen table; §23 name-collision search
AC 2 checked: r2 (327ce46): 21 SYNTHETIC specimens; 'python3 research/record_formats_check.py' -> 85/85 (1500 days=units vs travel card, OCR decimal-less truths sum to Item 28, UB-04 room 1850x3=5550 and 0001 totals, ledger, EOB, PT 8-minute rule, Spanish 07/06/2026 truth, EMS times, ambulance 8.7x22.50, affidavit = ledger); planted 060126-060526 grouping fails; all specimens pass validate_library scan_text
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:43:00.127Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && \\\n$B handoff T-077 --agent researcher --text \"What changed (r2, 5c2cb2f): research/validate_library.py denylist now holds every real v2 name (case- and accent-insensitive; Hills/Flores/Bai capitalised-only; Waddell allowed as eponym) plus --self-test; v2 doc gains a Denylist additions block, tagged Record features, Hills v. Donis re-cited to the 2021 substitute opinion, P17 source swapped to Castro 1997 (Hampton had no retrievable cite), P5/P6 rewording, stage/entry + must-contain + formats columns; lib12 recast as a pre-suit carrier records review (renamed lib12_records_review_credibility; TRCP 204 exam as litigation variant). · How verified: python3 research/validate_library.py --self-test -> ok (354 planted variants, 16 caption names); negative test with Garza removed fails; python3 research/validate_library.py -> ok (7 packets, 72 terms). · What's left: T-079 should use the new lib12 id and the must-contain table; state names stay banned, so packets write TX. · What surprised me: the 2020 Hills opinion the firm write-up described was withdrawn; the 2021 substitute affirmed one plaintiff's ankle award on lay testimony.\" && \\\n$B handoff T-078 --agent researcher --text \"What changed (r2, 327ce46): CMS-1500 rebuilt (grouped 06/01-06/03 = 3 days = 3 units, matching the travel card; total 390) plus an OCR version with decimal-less amounts and stated truth; inpatient UB-04 with FL44 1,850.00 x 3 days = 5,550.00 and occurrence code 03; occurrence codes 01-06 documented; six new formats §15-20 (EMS PCR, ambulance invoice, CPRC 18.001 affidavit + cover, narrative letter, office/specialist note, records-review/IME); PT units fixed to 38 min = 3 units; Spanish 07/06/2026 = 7 June; §22 cross-specimen table (fixed vs DELIBERATE); §23 collision search, Bluebonnet and Los Almendros/Valcárcel replaced. · How verified: python3 research/record_formats_check.py -> 85/85; planted round-1 grouping fails; every specimen passes validate_library.scan_text. · What's left: NUBC manual still unopened (FL44 title, creation date, current 01 label marked unverified); pain-management procedure note and work-status slip not covered. · What surprised me: CMS ch.15 requires mileage in tenths in 24G, so 1500 units can carry a decimal.\" && \\\n$B commit T-077 --sha 5c2cb2f --agent researcher && $B commit T-078 --sha 327ce46 --agent researcher && \\\n$B move T-077 in_review --agent researcher && $B move T-078 in_review --agent researcher && \\\n$B lesson --agent researcher --text \"Research docs that cite real names must ship the denylist entry and a self-test in the same commit; specimens need a re-add script (record_formats_check.py) because hand-checked arithmetic missed a NUCC grouping error and an 8-minute-rule over-bill. Verify case history on the court docket, not a firm write-up.\"",
 "description": "Handoffs, commit records, move to review, lesson"
}
````

### User / tool · 2026-11-02T03:43:00.583Z

**tool result**
````
handoff written on T-077
handoff written on T-078
T-077: commit 5c2cb2f recorded
T-078: commit 327ce46 recorded
T-077: in_progress -> in_review
T-078: in_progress -> in_review
lesson recorded
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:43:06.457Z

T-077 and T-078 are back in `in_review`. T-077 (commit 5c2cb2f): `/Users/arsis/zlayt-pm-project/research/validate_library.py` now bans every v2 real name in any letter case (self-test: planted names fail, the doc list and code list match); P3 is re-cited to the 2021 substitute opinion and P17's source replaced because Hampton had no findable docket; the minors are fixed, and lib12 is now a pre-suit records review, so T-079 needs the new id.
T-078 (commit 327ce46): `/Users/arsis/zlayt-pm-project/research/record-formats.md` has the NUCC-consistent CMS-1500 plus an OCR copy with decimal-less amounts, an inpatient UB-04 with the rate on the charge line, occurrence codes 01–06, and six new formats (EMS report, ambulance invoice, §18.001 affidavit, narrative letter, plus office note and records review for the other lib rows); `/Users/arsis/zlayt-pm-project/research/record_formats_check.py` passes 85/85 and the NUBC-manual items are still marked unverified.
