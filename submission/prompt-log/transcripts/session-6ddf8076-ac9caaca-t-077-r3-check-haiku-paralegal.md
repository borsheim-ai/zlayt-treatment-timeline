# Subagent: T-077 r3 check (haiku paralegal) (T-077 r3 check (haiku paralegal))

Source: `agent-ac9caaca56d17d0bc.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:54:18.178Z

Round-3 check of board card T-077 in /Users/arsis/zlayt-pm-project (commit 8d7548d). Using reviews/T-077-paralegal-r2.md, confirm that every real person or party name cited in research/case-library-sources-v2.md, study authors included, is on the research/validate_library.py denylist.

Check:
- the self-test extracts the cited names mechanically, and fails when a new name is cited without being denylisted;
- a planted name in a scratch packet fails validation;
- `python3 research/validate_library.py` passes on evals/library;
- whether the judgment call on firm names (limited to URL slugs and FAIR Health) is acceptable for synthetic-data safety.

Write reviews/T-077-paralegal-r3.md with a ```json block of real values: card, persona paralegal-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:20.270Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T03:54:20.277Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:20.545Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md"
}
````

### User / tool · 2026-11-02T03:54:20.552Z

**tool result**
````
1	---
2	name: golden-set-recurring-findings
3	description: Patterns found reviewing evals/golden (T-015, 2026-11-01) to re-check on any later golden/eval change — must/should downgrades, leaky must_not regexes, missing tolerated flags
4	metadata:
5	  type: project
6	---
7	
8	Recurring golden-set weaknesses found in the T-015 review (commit 47520a8, verdict fail):
9	- Appendix C "Expected flags (at minimum)" items got downgraded to `should` (K4 new onset after the 73-day gap, K5 wrong intake accident date). Under README scoring, `should` never counts as a miss, and cross-type credit isn't implemented. Re-check levels whenever golden files change.
10	- Explicit prior-condition mentions marked `should` (case_06 P2/P3), while the sample's different-region prior (P1) is `must`. Check that levels are consistent across cases.
11	- A credible adjuster attack with no golden or tolerated entry gets scored as a false positive (case_06 "denies prior neck problems" vs chiropractor history). Ask "what would the adjuster's letter quote?" and confirm each answer is must, should or tolerated.
12	- must_not regexes are only tested negatively (they must not match the input). Probe them with known-bad phrasings: the sample M9 regex missed "full recovery", and M2 missed "caused by the January collision" and "Degenerative findings".
13	
14	Round 2 (commit 3c5eb7c) added these patterns:
15	- A level fix isn't enough. If two `must` flags share type and cite (K4/K5: causation, record 7) and matching is type+cite only, one candidate satisfies both. Simulate the README matching rule literally, and require evidence overlap plus one-to-one assignment.
16	- The byte-exact export golden (extracted from REQUIREMENTS §6) can drift from the golden JSON: a missing must-flag line, and evidence changes such as C1 "rear-ended" that should add a "flagged language" row. Rebuild each notes section from the JSON plus the R-EX-4 rules, and diff.
17	- Spec text (R-FL-4) can lag behind a golden change. Grep REQUIREMENTS for the old rule.
18	
19	Round 3 (commit f8c1948, verdict fail) added these patterns:
20	- Schema key drift can silently disable a check. The JSON used `spans` while README and check_golden read `self_report_spans`, so the D-022 checks ran on empty lists and the validator stayed green. Count keys across all JSON files, and mutation-test every new assertion on a scratchpad copy (break the data, and the checker must exit 1).
21	- The writer fixes the line the reviewer named (the K5 line) and leaves the sibling lines that REQUIREMENTS §8 also listed (the C1 conflict bullet quoting both sides, the AI line). Byte-diff the golden against REQUIREMENTS §6 every round, and run the §8 reconciliation greps literally.
22	- Either-way substring overlap in the reference matcher lets a whole-record excerpt satisfy every golden flag on that record. Probe with whole-record and one-word candidates.
23	
24	Round 4 (commit 0c03c4f, HEAD 65537a4, verdict changes) added these patterns:
25	- A fixed text can match one spec section and still break another. The golden AI line was made to match REQUIREMENTS section 6, but normative R-EX-4(1) keeps different text, and R-EX-4(1) contradicts R-EX-4(11). Diff the golden against every spec location that quotes the same text, not only the one the finding named.
26	- A prior review's quoted "spec text" can be wrong. The r3 paralegal quoted an R-EX-4(1) string that grep does not find in REQUIREMENTS.md. Grep every quoted spec string before relying on it.
27	- Key renames fix the data but can leave the checker's guard code stale. Mutation-test with the renamed key and with an objective span. The guard for unknown entry keys (ENTRY_KEYS in check_golden.py) is what makes the rename safe.
28	
29	**Why:** these let a weaker product pass the ship bar while hiding exactly what costs the paralegal credibility.
30	**How to apply:** on any re-review of evals/golden or evals.run, re-run a probe like artifacts/review-evidence/T-015-paralegal-regex-probe.py and re-check the level of every Appendix C item. Related: [[reviewer-hook-constraints]]
31	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:20.772Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/library-review-patterns.md"
}
````

### User / tool · 2026-11-02T03:54:20.779Z

**tool result**
````
1	---
2	name: library-review-patterns
3	description: T-052 (2026-11-01) synthetic case library review - what held up, what to re-check on library/golden changes
4	metadata:
5	  type: project
6	---
7	
8	T-052 evals/library (7 packets) passed with minors only. Hand-recomputed gaps/totals were all right; identifier overlap vs fetchable sources was 0.
9	Re-check on any library change:
10	- Stated attendance count vs billed count (lib03 "31 visits", $120 rate left unclear): is the rule written in README/REQUIREMENTS?
11	- Flag type fit: lib06 attorney referral is typed `causation` (wrong heading).
12	- PT plan-of-care vs last visit with no discharge (lib05) is not surfaced.
13	- Library packets are one-sentence excerpts; no ledger-by-DOS, Bates, DOA conflict.
14	- valawyersweekly.com and rissman.com return 403 to curl even with a browser UA; studicata is unopened. Sources fetch fine for rmdlaw, oklahomalawyer, plasticsurgerypractice, thompsoncoe.
15	- curl `-o` to scratchpad and python heredocs containing `>=` trip board-guard; redirect stdout into artifacts/review-evidence and put code in a script file.
16	
17	**How to apply:** use artifacts/review-evidence/T-052-paralegal-scan.py as a starting probe. Related: [[golden-set-recurring-findings]], [[reviewer-hook-constraints]]
18	
19	## T-077 r2 (commit 5c2cb2f): denylist guard, self-test scope
20	- A denylist self-test that cross-checks only the doc's caption names ("X v. Y", "In re X") misses real names cited in prose (study authors, co-authors). Brinjikji, Nakashima, Fraser, Vera slipped through while the self-test printed "ok". Run the per-name check yourself: list every capitalised name in the doc and test each against the list.
21	- Firm domains in cited URLs (mdjwlaw, painterfirm) and organisation names (FAIR Health) are not on the list; decide with Chris whether they count as "real names".
22	- Rule text that says "every real name in this file is on the denylist" is a claim to test, not to trust.
23	- Fetched-page checks: a newsbrief sentence attributing a claim ("describes the withdrawn opinion") must be grepped on the page; the docket was the source that actually supported it.
24	- Date provenance: "checked 2026-11-02" in a doc written 2026-11-01 local is probably UTC. Ask, do not assume.
25	- Denylist and self-test changes in this area: keep a planted-name test per new term (mutation: delete a term and confirm self-test fails).
26	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:20.976Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r2.md"
}
````

### User / tool · 2026-11-02T03:54:20.982Z

**tool result**
````
1	# T-077 round 2: paralegal-reviewer (research/case-library-sources-v2.md + research/validate_library.py, commit 5c2cb2f)
2	
3	**Verdict: changes.** The round-1 major is only partly closed. The denylist mechanism works: the self-test passes, and every planted mixed-case and accented variant of a listed name fails. But four real names the v2 file cites are still not on the list (Brinjikji, Nakashima, Fraser, Vera), so the file's own rule "every real name in this file is on that denylist" is still false. The self-test only checks the "X v. Y" captions, not the prose author names. Nothing in the current packets contains these names (the 7-packet scan is clean), so this is a major and not a blocker. Three round-1 minors are closed. The Hills v. Donis fix is right on the docket but misattributes the withdrawal to the newsbrief.
4	
5	## Commands run and output
6	
7	```
8	$ python3 research/validate_library.py --self-test
9	self-test: ok (354 planted variants caught, 16 caption names covered)        exit 0
10	$ python3 research/validate_library.py
11	identifier check: ok (7 packets, 72 denylist terms, case-insensitive)       exit 0
12	```
13	
14	Per-name check (artifacts/review-evidence/T-077-paralegal-r2-denylist.py, output in T-077-paralegal-r2-denylist.out):
15	
16	```
17	'Brinjikji' cited at L12   on denylist=False planted-caught=False
18	'Nakashima' cited at L12   on denylist=False planted-caught=False
19	'Fraser'    cited at L215  on denylist=False planted-caught=False
20	'Vera'      cited at L228 (Rodriguez-Vera) on denylist=False planted-caught=False
21	cited real names NOT on denylist: ['Brinjikji', 'Nakashima', 'Fraser', 'Vera']
22	caption names checked by self-test: [16 names, all captions only]
23	```
24	
25	Round-1 minors:
26	
27	| Round-1 item | Status | Evidence |
28	|---|---|---|
29	| Record features not tagged | Closed | All 17 patterns (P1-P17) carry "(from source)" or "(our inference)"; P4 and P17 say the source supports only the scenario theme (lines 103-104, 305-306). |
30	| Hills v. Donis "withdrawn and substituted" | Partly closed | Docket supports it (artifacts/review-evidence/T-077-paralegal-r2-docket.out): "Opinion withdrawn 02/11/2021", "Motion for rehearing disposed DENIED 02/11/2021", "Memorandum opinion issued AFFIRMED IN PART AND REVERSED AND RENDERED IN PART [PDF/97 KB]". Supreme Court order list of July 23, 2021 denies 21-0287 (T-077-paralegal-r2-orders.out). But line 80 says the newsbrief "describes the withdrawn 2020 opinion": the fetched page has 0 matches for "withdr" and "substitut". See F2. |
31	| P7 / lib12 stage not stated | Closed | Case stage line (159-160); stage/entry column (345-348). |
32	| P5 "six ledger columns" overstated | Closed | Lines 124-126: ledger columns derived from items 1-4 and 6; item 5 is a separate document. |
33	| D-042 features not in packet rows | Closed | "Must contain" table (350-361) with lib09, lib12, lib13 fixtures. |
34	| P6 case type, statute currency | Closed | Line 136 "health care liability claim"; statute currency line 427-430. |
35	
36	## Findings
37	
38	1. **major, still open: four cited real names are not on the denylist.** Brinjikji and Nakashima (line 12), Fraser (line 215) and Rodriguez-Vera's "Vera" (line 228) are real names in the file and absent from DENYLIST_V2 and the doc block. The self-test checks only caption names (see the output above), though validate_library.py:11 says "v2 doc names must all be listed".
39	2. **minor: the Hills newsbrief is described as saying what it does not say.** Line 80. Cite the docket for withdrawal and substitution; add the substitute opinion's own PDF link or say it is not linked.
40	3. **minor: firm and organisation names are not on the list.** mdjwlaw (line 80), painterfirm (line 135), FAIR Health (line 266). The denylist section says it covers "every real proper noun in this file's sources".
41	4. **nit: provenance dates are after the review date.** Line 4 "Researched 2026-11-01/02", line 427 "checked 2026-11-02". The commit is "Sun Nov 1 21:42:31 2026 -0600", which is 2026-11-02 in UTC, so these are probably UTC. Same pattern in research/record-formats.md lines 9 and 1073. State the timezone.
42	
43	Outside my lens: whether a Texas statute or case holding is currently good law. I checked only what the doc says the sources say.
44	
45	```json
46	{"card": "T-077", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
47	 "scope": "research/case-library-sources-v2.md and research/validate_library.py at commit 5c2cb2f (round 2); prior review reviews/T-077-paralegal.md; no app run (research card); no sample case",
48	 "exercised": [
49	  "Read personas/paralegal.md, reviews/T-077-paralegal.md, git show --stat 5c2cb2f, research/validate_library.py (179 lines), research/case-library-sources-v2.md (435 lines, full)",
50	  "python3 research/validate_library.py --self-test -> 'self-test: ok (354 planted variants caught, 16 caption names covered)', exit 0",
51	  "python3 research/validate_library.py -> 'identifier check: ok (7 packets, 72 denylist terms, case-insensitive)', exit 0",
52	  "artifacts/review-evidence/T-077-paralegal-r2-denylist.py (+ .out): every real name found in the v2 file checked against DENYLIST and a planted sentence; Brinjikji, Nakashima, Fraser, Vera are not on the list and not caught; a planted packet with them passes the library scan",
53	  "artifacts/review-evidence/T-077-paralegal-r2-docket.out: search.txcourts.gov case 14-18-00566-CV (Opinion withdrawn 02/11/2021; rehearing denied and memorandum opinion issued 02/11/2021)",
54	  "artifacts/review-evidence/T-077-paralegal-r2-orders.py (+ .out): Texas Supreme Court July 23, 2021 order list denies 21-0287; date mentions in the doc (2026-11-02) checked against the commit date",
55	  "Fetched mdjwlaw newsbrief TIN-20200211-item1 (HTTP 200, 32,603 bytes): 0 matches for 'withdr' and 'substitut'; cites 2020 WL 206187 only",
56	  "Counted 'Record features' lines: 17 patterns, each tagged '(from source)' or '(our inference)'",
57	  "Not exercised: a fresh name-collision search; the round-1 web fetches were not repeated beyond the Hills pages; one fetch dump was written to the session scratchpad (outside the reviewer write paths, not a review artifact)"],
58	 "verdict": "changes",
59	 "scores": {"denylist_covers_cited_names": 2, "planted_name_self_test": 4, "round1_minors_closed": 3, "source_fidelity": 4, "synthetic_safety_enforcement": 3},
60	 "findings": [
61	  {"severity": "major", "title": "Denylist still omits four real names the v2 file cites; self-test checks only caption names",
62	   "evidence": "research/case-library-sources-v2.md:12 'Brinjikji, Nakashima'; :215 'ElGhrably I., Fraser S.G.'; :228 'Rodriguez-Vera F.J.'; rule at :24-25 says every real name in the file is on the denylist. research/validate_library.py:25-48 (DENYLIST_V2) has no Brinjikji, Nakashima, Fraser or Vera. artifacts/review-evidence/T-077-paralegal-r2-denylist.out: 'cited real names NOT on denylist: [Brinjikji, Nakashima, Fraser, Vera]'; self-test caption list has 16 names, all 'X v. Y' or 'In re' captions. validate_library.py:11 docstring says 'v2 doc names must all be listed'.",
63	   "why_it_matters": "The guard fails open for these four names: a packet containing 'Fraser' or 'Brinjikji' passes the identifier check, and the doc says it does not. No current packet contains them (the 7-packet scan is clean), so no real name has leaked; this is why it is a major and not a blocker. It stays open because the round-1 major was exactly this coverage gap.",
64	   "fix": "Add Brinjikji, Nakashima, Fraser and Vera (and Rodriguez-Vera as a unit) to DENYLIST_V2 and to the 'Denylist additions' block. Extend self_test so that author names in the doc's citations are checked against the list, not only X v. Y captions. Correct the validate_library.py docstring to say what is checked.",
65	   "acceptance_test": "python3 research/validate_library.py --self-test fails when 'Brinjikji' is removed from DENYLIST_V2 (it passes today); a packet containing 'Fraser S.G.' fails scan_library; the doc-versus-list check covers the prose author names."},
66	  {"severity": "minor", "title": "Hills v. Donis: the newsbrief is described as saying 'withdrawn', which it does not say",
67	   "evidence": "research/case-library-sources-v2.md:80 'The firm newsbrief https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the withdrawn 2020 opinion only.' Fetched page: 0 matches for 'withdr' and 'substitut'; it cites 'Hills v. Donis, No. 14-18-00566-CV, 2020 WL 206187 ... Jan. 14, 2020'. Docket supports the withdrawal (artifacts/review-evidence/T-077-paralegal-r2-docket.out: 'Opinion withdrawn 02/11/2021').",
68	   "why_it_matters": "This is the sentence round 1 flagged. The conclusion is now right, but a paralegal who opens the newsbrief to check the withdrawal will not find it. The 2021 substitute opinion also has no PDF link in the doc; the docket page is cited instead.",
69	   "fix": "Cite the docket page for the withdrawal and the substitution. Change the newsbrief sentence to 'describes the 2020 opinion (2020 WL 206187) and does not mention withdrawal'. Add the substitute opinion's own PDF link from the docket, or say it is not linked.",
70	   "acceptance_test": "In the P3 entry, 'withdrawn' is attributed only to the docket URL; the newsbrief sentence matches the fetched page (no 'withdr' or 'substitut' hits)."},
71	  {"severity": "minor", "title": "Firm and organisation names in cited URLs and text are not on the denylist",
72	   "evidence": "research/case-library-sources-v2.md:80 'mdjwlaw.com'; :135 'painterfirm.com/medmal/...'; :266 'FAIR Health, A Window into Utilization and Cost of Ground Ambulance Services'. None appears in DENYLIST_V2 or DENY_CAPITALISED (validate_library.py:21-53). The denylist section (:363-366) says it covers every real proper noun in the file's sources.",
73	   "why_it_matters": "These are firm and organisation names, not parties, so the risk is lower than for the names in F1. A packet could still carry 'Painter' or 'FAIR Health' with no flag, and the doc's own rule is broader than the list.",
74	   "fix": "Add mdjwlaw, Painter and FAIR Health to the denylist, or state in the doc that organisation and website names are exempt and why.",
75	   "acceptance_test": "The denylist block lists every firm or organisation token in the source citations, or the exemption is written in the doc."},
76	  {"severity": "nit", "title": "Provenance dates are after the review date and do not say which timezone",
77	   "evidence": "research/case-library-sources-v2.md:4 'Researched 2026-11-01/02'; :427 'CPRC 18.001/18.002 text was checked 2026-11-02'. Commit 5c2cb2f: 'Date: Sun Nov 1 21:42:31 2026 -0600'. The same date appears in research/record-formats.md:9 and :1073.",
78	   "why_it_matters": "The commit is 2026-11-02 in UTC, so the dates are probably UTC. A reader cannot tell which clock was used, and a statute-currency date should be unambiguous.",
79	   "fix": "State the timezone, or use the local date.",
80	   "acceptance_test": "Each date in the doc matches the commit date in the stated timezone."}
81	 ],
82	 "whats_right": [
83	  "All 17 'Record features' lines are tagged '(from source)' or '(our inference)', and P4 and P17 say their sources back only the scenario theme.",
84	  "The self-test plants 354 mixed-case and accented variants of the listed names and all are caught; lowercase 'hills' is not flagged, and 'Waddell' is allowed as an eponym.",
85	  "The P5 billing list now matches the opinion: four ledger columns from items 1-4 and 6, with item 5 (carrier contracts) marked as a separate document."],
86	 "questions_for_chris": [
87	  "Should cited firm websites and journal names count as 'real names' for the denylist, or only people and places? The doc says 'every real proper noun', and the answer decides F3."]}
88	```
89	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:23.249Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 && git show --stat 8d7548d | head -30 && cat research/validate_library.py",
 "description": "Show recent commits, T-077 commit stats, and validator source"
}
````

### User / tool · 2026-11-02T03:54:23.374Z

**tool result**
````
8d7548d fix(research): denylist covers every cited author surname; self-test extracts and checks them (T-077 r3)
f49c4c2 docs: D-045 scope of the judge export gate
8e3c26c fix(frontend): collapsed case rail and AI-check row, working case-step actions, narrative stepper entry, Why dialog opens on the active step, one row per item (T-081 r2, T-082 r2)
fe4ee80 feat(backend): D-044 export gate blocks accepted items whose second check never ran; POST /rejudge
b5b9b34 test(backend): T-075 r2 strengthen sort and judge-prompt tests, reword diagnosis as mitigations
commit 8d7548d5c5478d2120e3e7ed6c1ab4c6d6bb95a7
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 21:53:57 2026 -0600

    fix(research): denylist covers every cited author surname; self-test extracts and checks them (T-077 r3)
    
    - validate_library.py: DENYLIST_V2 adds Fraser, Brinjikji, Nakashima, Vera, Rodriguez-Vera (study authors and the bare
      citation list), plus mdjwlaw, painterfirm and FAIR Health (cited firm/organisation tokens)
    - self-test extracts every author surname (before initials or et al), every bare name in the 'already cited' list and
      every X v. Y caption; each must be listed, and each planted in a packet must fail the scan
    - v2 doc: denylist block and rule 2 updated; Hills v. Donis newsbrief sentence no longer says it mentions withdrawal
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 research/case-library-sources-v2.md | 29 +++++++++----
 research/validate_library.py        | 84 +++++++++++++++++++++++++++++++------
 2 files changed, 93 insertions(+), 20 deletions(-)
#!/usr/bin/env python3
"""Validate evals/library/* with evals/golden/check_golden.py (T-052) and scan packets for real identifiers (T-077).

check_golden.py reads cases from its own directory, so this copies evals/golden into a scratch dir, adds the library packets,
runs the checker there, and then scans the library for real identifiers. The denylist holds every proper noun taken from the
cited real sources in research/case-library-sources.md (v1) and research/case-library-sources-v2.md (v2): case parties, judges,
doctors named in opinions, study authors, firms, counties, cities and highways. Matching is case-insensitive and
accent-insensitive ('GARZA', 'garza', 'Rodríguez' all hit). Exit 0 = both pass.

Self-test checks the v2 doc mechanically: every surname written before author initials or 'et al' (e.g. 'Fraser S.G.'), every
bare surname in a parenthesised list inside a paragraph that cites earlier sources (e.g. 'Brinjikji, Nakashima'), and every
'X v. Y' / 'In re X' caption name must be on the denylist, and each one planted in a packet must fail the scan. A newly cited
name therefore fails the self-test until it is added to DENYLIST_V2 and the doc's 'Denylist additions' block.

Run:        python3 research/validate_library.py
Self-test:  python3 research/validate_library.py --self-test
"""
import pathlib, re, shutil, subprocess, sys, tempfile, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIB = ROOT / "evals" / "library"
V2_DOC = ROOT / "research" / "case-library-sources-v2.md"

# v1 sources (research/case-library-sources.md). States are listed because v1 sources named them; packets use the
# two-letter abbreviation (e.g. "TX") where a state must appear.
DENYLIST_V1 = ["Nichols", "Duke Linden", "Haygood", "Escabedo", "K & L", "K&L", "Auto Crushers", "Alexandria", "Puerto Rico",
               "Rissman", "Colossus", "Manitoba", "Verisk", "Medicare", "Tennessee", "Nebraska", "New Jersey", "Virginia",
               "Oklahoma", "Texas", "Florida", "California", "Illinois", "Michigan", "Kelly", "Cutch"]
# v2 sources (research/case-library-sources-v2.md, "Denylist additions" block). Keep the two lists in sync; --self-test checks.
DENYLIST_V2 = [
    # P1 JLG Trucking v. Garza
    "JLG", "Garza", "Pechero", "Zapata",
    # P2 Guevara v. Ferrer
    "Guevara", "Ferrer",
    # P3 Hills v. Donis (parties, the doctor named in the opinion, the author justice, the highway)
    "Donis", "Matamoros", "Castellanos", "Morehouse", "Reuben", "Rueben", "Poissant", "I-45",
    # P4 Chiv v. Figueroa
    "Chiv", "Figueroa",
    # P5 In re Central Oregon Truck Co.
    "Central Oregon", "Oregon", "Broussard",
    # P6 Gunn v. McCoy
    "Gunn", "McCoy",
    # P7 Rodriguez v. Wal-Mart Stores
    "Rodriguez", "Wal-Mart", "Walmart",
    # P16 defense-firm write-up
    "Lewis Brisbois", "Brisbois", "Harris County",
    # P17 Hampton v. Miskell (dropped as a source, names still banned) and Castro et al.
    "Hampton", "Miskell", "Baratta", "I-635", "Castro", "Schilgen",
    # Study authors cited in v2 (author initials or 'et al' in source lines; bare names in the opening citation list)
    "Steinkamp", "Kantrowitz", "Airan-Javia", "ElGhrably", "Fishbain", "Powell", "Anderson",
    "Fraser", "Brinjikji", "Nakashima", "Vera", "Rodríguez-Vera",
    # Firm website slugs in cited URLs (not people; a slug never occurs as ordinary packet text)
    "mdjwlaw", "painterfirm",
    # Cities and counties named in v2 citations; insurer named in a v1 caption that v2 mentions
    "Houston", "Dallas", "Allstate",
]
# Real names that are also ordinary lowercase words: banned only when capitalised (Title or UPPER), so "rolling hills" or
# "flores" (Spanish for flowers) in a packet still passes while "Hills" / "FLORES" as a name fails.
DENY_CAPITALISED = ["Hills", "Flores", "Bai", "FAIR Health"]
# Eponymous clinical terms that share a name with a cited author and are allowed in packets on purpose.
ALLOWED_EPONYMS = ["Waddell"]
DENYLIST = DENYLIST_V1 + DENYLIST_V2
BANNER = "SYNTHETIC — invented for evaluation; not real patient data\n"


def fold(s):
    """Strip accents so 'Rodríguez' matches 'Rodriguez'."""
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


_ANY = [(w, re.compile(r"(?<!\w)" + re.escape(fold(w)) + r"(?!\w)", re.I)) for w in DENYLIST]
_CAP = [(w, re.compile(r"(?<!\w)(?:" + re.escape(w) + "|" + re.escape(w.upper()) + r")(?!\w)")) for w in DENY_CAPITALISED]


def scan_text(text):
    """Return the denylist terms found in text (case- and accent-insensitive; capitalised-only terms need a capital)."""
    t = fold(text)
    return [w for w, rx in _ANY if rx.search(t)] + [w for w, rx in _CAP if rx.search(t)]


def doc_denylist_block(doc_text):
    """Terms listed in the v2 doc's fenced 'Denylist additions' block (one per line, '#' comments allowed)."""
    m = re.search(r"## Denylist additions.*?```text\n(.*?)```", doc_text, re.S)
    if not m:
        return None
    return [ln.split("#")[0].strip() for ln in m.group(1).splitlines() if ln.split("#")[0].strip()]


_GENERIC = {"In", "re", "Inc", "Inc.", "LLC", "LLC,", "Co", "Co.", "Stores", "Stores,", "Truck", "Trucking", "Trucking,", "The",
            "of", "and", "Tex", "Tex.", "App", "App.", "No", "No."}


def doc_caption_names(doc_text):
    """Capitalised name tokens from every 'X v. Y' and 'In re X' caption in the v2 doc."""
    names = set()
    for a, b in re.findall(r"([A-Z][\w.'&-]*(?:,? [A-Z][\w.'&-]*)*) v\. ([A-Z][\w.'&-]*(?:,? [A-Z][\w.'&-]*)*)", doc_text):
        for side in (a, b):
            for tok in re.split(r"[ ,]+", side):
                if len(tok) > 1 and tok not in _GENERIC and tok[0].isupper() and not any(c.isdigit() for c in tok):
                    names.add(tok.rstrip(".,"))
    for x in re.findall(r"In re ([A-Z][\w'-]*(?: [A-Z][\w'-]*)*)", doc_text):
        toks = [t for t in x.split() if t not in _GENERIC]
        if toks:
            names.add(" ".join(toks[:2]))
    return names


# A surname is a capitalised word directly before author initials ('Fraser S.G.', 'Steinkamp J.', 'Rodríguez-Vera F.J.')
# or before 'et al' ('Fishbain et al.'). Initials are capital letters only, so 'Co.', 'Inc.' and 'No.' never match.
_AUTHOR_RX = re.compile(r"(?<![\w'’-])([A-Z][\w'’-]*)(?=,? [A-Z]\.(?:[A-Z]\.)*(?!\w)|\s+et al\b)")


def doc_author_names(doc_text):
    """Surnames written before author initials or 'et al' anywhere in the v2 doc."""
    return {m.group(1) for m in _AUTHOR_RX.finditer(doc_text)}


def doc_listed_citation_names(doc_text):
    """Bare surnames in parenthesised lists inside paragraphs that cite earlier sources (the 'already cited' sentence).

    Only single capitalised words with lowercase letters count, so acronyms (MIST), IDs (D-043) and tool names are skipped
    by shape, and multi-word items such as 'In re Allstate' or 'K&L Auto Crushers' are left to the denylist entries.
    """
    names = set()
    for para in re.split(r"\n\s*\n", doc_text):
        if "cited" not in para:
            continue
        flat = " ".join(para.split())
        for group in re.findall(r"\(([^()]*)\)", flat):
            for item in re.split(r"[,;]", group):
                item = item.strip()
                if re.fullmatch(r"[A-Z][a-z][\w'’-]*", item):
                    names.add(item)
    return names


def doc_citation_names(doc_text):
    """Every name the v2 doc cites: author surnames, bare names in citation lists, and caption names."""
    return doc_author_names(doc_text) | doc_listed_citation_names(doc_text) | doc_caption_names(doc_text)


def _covered(name, listed):
    """A cited name is covered when the name, one of its words, or one of its hyphen parts is listed (case/accent-insensitive)."""
    return any(fold(p).lower() in listed for p in [name] + name.split() + re.split(r"-", name))


def self_test(doc_text=None):
    """Run the self-test. doc_text overrides the v2 doc (used to prove a newly cited name fails the test)."""
    fails = []
    for w in DENYLIST:
        for variant in {w, w.lower(), w.upper(), w.swapcase(), w.title()}:
            if w not in scan_text(f"Seen by Dr. {variant} at the clinic."):
                fails.append(f"planted {variant!r} not caught")
    for w in DENY_CAPITALISED:
        for variant in (w, w.upper()):
            if w not in scan_text(f"Referred by {variant} Family Clinic."):
                fails.append(f"planted {variant!r} not caught")
        if scan_text(f"walked up the {w.lower()} near home"):
            fails.append(f"lowercase common word {w.lower()!r} wrongly flagged")
    if not scan_text("Patient: Ana Rodríguez (SYNTHETIC)"):
        fails.append("accented Rodríguez not caught")
    for w in ALLOWED_EPONYMS:
        if scan_text(f"{w} signs 0/5 today."):
            fails.append(f"eponym {w!r} wrongly flagged")
    doc = V2_DOC.read_text() if doc_text is None else doc_text
    block = doc_denylist_block(doc)
    listed = {fold(w).lower() for w in DENYLIST + DENY_CAPITALISED + ALLOWED_EPONYMS}
    if block is None:
        fails.append("v2 doc has no '## Denylist additions' ```text block")
    else:
        for w in block:
            if fold(w).lower() not in listed:
                fails.append(f"v2 doc denylist term {w!r} missing from validate_library.py")
        for w in DENYLIST_V2 + DENY_CAPITALISED:
            if w not in block:
                fails.append(f"validate_library.py term {w!r} missing from the v2 doc block")
    authors = doc_author_names(doc)
    cite_lists = doc_listed_citation_names(doc)
    captions = doc_caption_names(doc)
    for name in sorted(authors | cite_lists | captions):
        if not _covered(name, listed):
            kind = "author" if name in authors else "citation-list" if name in cite_lists else "caption"
            fails.append(f"v2 doc cites {kind} name {name!r} but it is not on the denylist (add it to DENYLIST_V2 and the doc block)")
    with tempfile.TemporaryDirectory() as tmp:
        # Every cited author or citation-list surname, planted in a packet, must make the library scan fail.
        for i, name in enumerate(sorted(authors | cite_lists)):
            p = pathlib.Path(tmp) / f"case_planted_author_{i}.txt"
            p.write_text(BANNER + f"Seen by {name} S.G. at the clinic on 03/06/2026.\n")
            if not scan_library([p]):
                fails.append(f"planted author/citation surname {name!r} passed the library scan")
        # End-to-end: a planted packet must make the library scan fail.
        p = pathlib.Path(tmp) / "case_planted.txt"
        p.write_text(BANNER + "Patient seen by DR. GARZA after the crash on i-45.\n")
        if not scan_library([p]):
            fails.append("planted packet passed the library scan")
    for f in fails:
        print("SELF-TEST FAIL:", f)
    n = len(DENYLIST) * 5 + len(DENY_CAPITALISED) * 3 + len(authors | cite_lists)
    print("self-test:", "FAIL" if fails else
          f"ok ({n} planted variants caught; {len(authors | cite_lists | captions)} cited names covered: "
          f"{len(authors)} author, {len(cite_lists)} citation-list, {len(captions)} caption)")
    return 1 if fails else 0


def scan_library(files):
    bad = []
    for f in files:
        t = f.read_text()
        for w in scan_text(t):
            bad.append(f"{f.name}: contains real identifier {w!r}")
        if f.suffix == ".txt" and not t.startswith(BANNER):
            bad.append(f"{f.name}: missing SYNTHETIC header")
    return bad


def main():
    if "--self-test" in sys.argv:
        return self_test()
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
    bad = scan_library(sorted(LIB.glob("case_*")))
    for b in bad:
        print("IDENTIFIER CHECK FAIL:", b)
    terms = len(DENYLIST) + len(DENY_CAPITALISED)
    print("identifier check:", "FAIL" if bad else f"ok ({len(cases)} packets, {terms} denylist terms, case-insensitive)")
    return 1 if (r.returncode or bad) else 0


if __name__ == "__main__":
    sys.exit(main())
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:23.761Z

**tool call — Bash**
````
{
 "command": "cat -n research/case-library-sources-v2.md | sed -n '1,40p'",
 "description": "Read top of the v2 sources file with line numbers"
}
````

### User / tool · 2026-11-02T03:54:23.847Z

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
    24	   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass. Every real name in this file is on
    25	   that denylist (see "Denylist additions" below; matching is case- and accent-insensitive). `--self-test` extracts every
    26	   author surname, every bare name in the opening citation list and every caption name from this file, fails if any is not
    27	   listed, and fails if a planted packet containing one passes the scan. Common surnames that appear here
    28	   (Garza, Rodriguez, Hills, Gunn, Hampton, Castro, Powell, Anderson, Flores) are banned as invented-name choices too,
    29	   including in the Spanish-language packets: pick distinctive invented surnames instead.
    30	3. **Dates shifted.** Packet dates run in 2025–2027 and keep only the *interval* shape the pattern needs (e.g. "second event
    31	   about 12 weeks after the first"). Real dates in this file are citation dates for the source, not record dates.
    32	4. **Facts recombined.** Each packet mixes features from two or more patterns, so no packet maps back to one real matter.
    33	5. **Every packet text file starts with the SYNTHETIC banner line** used by v1 and is labeled synthetic in its expected JSON.
    34	6. **No real records.** Nothing here was taken from a medical record; opinions describe facts in prose, and we use that prose
    35	   only for scenario shape. Spanish text in packets is written fresh, not translated from any source.
    36	
    37	## Patterns
    38	
    39	### P1. Intervening second accident between first care and the key imaging
    40	- **Source:** JLG Trucking, LLC v. Garza, 466 S.W.3d 157 (Tex. 2015), opinion delivered 2015-04-24 —
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:28.144Z

**tool call — Bash**
````
{
 "command": "python3 research/validate_library.py --self-test; echo \"exit=$?\"; python3 research/validate_library.py; echo \"exit=$?\"",
 "description": "Run validator self-test and library check"
}
````

### User / tool · 2026-11-02T03:54:28.548Z

**tool result**
````
self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)
exit=0
golden OK: 17 cases (16 synthetic), 85 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (7 packets, 80 denylist terms, case-insensitive)
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:28.588Z

**tool call — Bash**
````
{
 "command": "cat -n research/case-library-sources-v2.md | sed -n '40,130p'",
 "description": "Read patterns P1-P3 of v2 doc with line numbers"
}
````

### User / tool · 2026-11-02T03:54:28.682Z

**tool result**
````
    40	- **Source:** JLG Trucking, LLC v. Garza, 466 S.W.3d 157 (Tex. 2015), opinion delivered 2015-04-24 —
    41	  https://www.txcourts.gov/media/943999/130978.pdf (full text, background section read).
    42	- **Summary:** The plaintiff was rear-ended, saw an orthopedist five days later, did about eleven weeks of PT, then had a
    43	  second crash shortly after PT ended and was taken by ambulance in a hard collar. The MRI showing herniations came only after
    44	  the second crash; surgery followed years later. The court held the second accident was relevant to causation and its
    45	  exclusion (including on cross of the treating doctor) was harmful error, even without a defense causation expert.
    46	- **Record features (from source):** an orthopedic visit days after event 1, then about eleven weeks of PT; an ambulance
    47	  transport in a hard collar after event 2; first MRI dated after event 2; a treating note whose history omits event 2;
    48	  multi-year span ending in fusion.
    49	- **Record features (our inference):** first-incident clinic records missing from the file; an ER record from event 2 with
    50	  neck complaints; a surgeon's narrative "history" that attributes everything to event 1.
    51	- **D-042 / flags:** conflict (two incident dates in the chart), causation (history-only attribution is self-reported/
    52	  provider-recited, not an opinion), gap; multi-case library; vertical stepper must show "two incidents found: human
    53	  decides relevance" as a HITL step. The tool never apportions.
    54	- **Synthetic-safety:** invent both crashes, shift to 2025–2026, change the interval (e.g. 10–14 weeks), change body region
    55	  if useful (lumbar instead of cervical); no county, highway or vehicle type from the opinion.
    56	
    57	### P2. Immediate care is common-knowledge; later complex care needs an expert
    58	- **Source:** Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007), decided 2007-08-31 —
    59	  https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html and commentary
    60	  https://www.casemine.com/commentary/us/expert-medical-evidence-mandated-for-causation-in-high-cost-automobile-accident-claims:-guevara-v.-ferrer/view
    61	  (summary only).
    62	- **Summary:** An elderly passenger's family relied on lay testimony to tie over $1 million in medical expenses to a crash.
    63	  The court held lay evidence can link a crash to conditions within common knowledge (immediate post-crash care), but
    64	  conditions outside it need expert evidence; the claimant must show what conditions generated the expenses and that each
    65	  was caused by the accident.
    66	- **Record features (from source):** immediate post-crash care, then a long, medically complex course with large total
    67	  expenses in an elderly patient.
    68	- **Record features (our inference):** EMS and ER pages with visible injuries; later admission, procedure and rehab notes
    69	  with no causation statement; one itemized hospital bill spanning both phases; comorbidities in the problem list.
    70	- **D-042 / flags:** causation (absence of any provider causation statement on later care is shown as "no causation
    71	  language found", not as a finding), pre_existing (comorbidity list), billing analysis (charges split by encounter, cited
    72	  per line); calibrated confidence must not imply causation strength.
    73	- **Synthetic-safety:** age band changed, no death in the packet, invented hospital, amounts invented and far smaller.
    74	
    75	### P3. Billing affidavits and records are not causation; conclusory physician letter
    76	- **Source:** Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.] Feb. 11, 2021, pet. denied) (substitute
    77	  mem. op.) — opinion PDF via the court docket https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14 (full
    78	  text read, pdftotext). The docket shows the memorandum opinion of 2020-01-14, a rehearing motion, and on 2021-02-11
    79	  rehearing denied, the 2020 opinion withdrawn and a substitute memorandum opinion issued; petition for review No. 21-0287
    80	  denied 2021-07-23 (https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/). The firm newsbrief
    81	  https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the 2020 opinion (2020 WL 206187) and does not mention
    82	  the withdrawal; the withdrawal and substitution are shown only on the docket page above (the substitute opinion is not linked).
    83	- **Summary (2021 substitute opinion):** Soft-tissue claims after a rear-end crash; no ambulance or ER. Past-medical awards
    84	  for three plaintiffs were reversed and rendered: §18.001 affidavits prove reasonableness of charges, not causation, and
    85	  a treating doctor's letters (and causation statements inside billing records) were conclusory because they gave no
    86	  explanation of how and why the crash caused the diagnoses. The award for a fourth plaintiff's ankle injury, and her
    87	  child's single visit, was affirmed on lay testimony and temporal proximity (Guevara).
    88	- **Record features (from source):** letters from a treater stating the crash caused the injuries, with no reasoning;
    89	  causation statements embedded in billing records; long diagnosis lists (radiculitis, disc displacement, discogenic pain)
    90	  on the bills; one plaintiff's single-visit bill (evaluation plus hot/cold pack).
    91	- **Record features (our inference):** billing-affidavit cover pages that look like records but carry no clinical content;
    92	  the same diagnosis lines repeated on every bill.
    93	- **D-042 / flags:** causation (letter language is shown verbatim with source; the tool never upgrades it to an opinion);
    94	  billing analysis (affidavit totals cited to the page, not re-derived by the LLM); LLM-as-judge visible: the judge must
    95	  reject any summary that turns "the accident caused" into a fact; record_warning for non-clinical pages.
    96	- **Synthetic-safety:** invented clinic and letter text; diagnosis wording paraphrased generically; no amounts reused; no
    97	  highway, county or party name from the opinion.
    98	
    99	### P4. Spanish-speaking party, certified interpreter, uncertified translation; counteraffidavit fight
   100	- **Source:** Chiv v. Figueroa, No. 01-23-00638-CV (Tex. App.—Houston [1st Dist.] 2025-08-21) —
   101	  https://hallapproved.com/tx/cases/appeals/2025/10659616/ (page fetched; summarized by the fetch tool, not read line by line).
   102	- **Summary:** A party sought to use a deposition taken in Spanish that lacked a certified translation, with a certified
   103	  interpreter at trial; that point was not preserved. Separately, striking a §18.001 counteraffidavit was harmful because the
   104	  only non-lay causation evidence came from admitted medical reports; past medical was reversed and remanded.
   105	- **Scope of support:** this source supports only the scenario theme (Spanish-speaking party, translation and
   106	  counteraffidavit disputes). The opinion says nothing about how records are charted.
   107	- **Record features (our inference):** records where the history is given in Spanish and charted in English; a note line
   108	  such as "history via interpreter" (or its absence); an itemized bill paired with a counteraffidavit-style rebuttal page.
   109	- **D-042 / flags:** Spanish-language records (the excerpt stays in the original language; any LLM translation is labeled
   110	  and judged); speaker attribution v2 (patient vs interpreter vs provider); billing analysis (contested line items shown, not
   111	  resolved).
   112	- **Synthetic-safety:** invented parties and providers; Spanish lines composed fresh; no deposition content used.
   113	
   114	### P5. Prior accidents, claimed brain injury, memory gaps, and a six-column billing request
   115	- **Source:** In re Central Oregon Truck Co., No. 20-0945 (Tex. 2022, per curiam), opinion delivered 2022-05-06 —
   116	  https://www.txcourts.gov/media/1454150/200945pc.pdf (full text read).
   117	- **Summary:** After a rear-end crash the plaintiff claimed a TBI and lost earning capacity; she had treated after two
   118	  earlier car accidents and for other conditions with overlapping symptoms, and said at deposition that memory problems
   119	  limited her recall. The court held pre-accident medical records and provider billing data relevant (subject to
   120	  proportionality). The billing discovery listed six items: (1) total billed charges, (2) adjustments or write-offs,
   121	  (3) amount paid to the provider and by whom, (4) outstanding balances, (5) copies of contracts with the health-insurance
   122	  carrier, (6) any letters of protection, contracts, liens or other guarantees.
   123	- **Record features (from source):** two earlier car accidents with treatment; memory complaints; a prior tailbone surgery;
   124	  the six billing-discovery items above.
   125	- **Record features (our inference):** intake forms answering "prior accidents: none" vs older notes that mention them; a
   126	  neuro or neuropsych note with memory complaints; ledger columns derived from items 1-4 and 6 (billed, adjusted, paid,
   127	  payer, balance, LOP/lien). Item 5 (carrier contracts) is a separate document a packet may reference but never reproduce
   128	  as a ledger column.
   129	- **D-042 / flags:** billing analysis (ledger columns from items 1-4 and 6, each cited; totals by code); pre_existing (prior accidents); conflict
   130	  (intake denial vs older note); calibrated confidence (per-state precision, not a "TBI likely" score).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:30.083Z

**tool call — Bash**
````
{
 "command": "cat -n research/case-library-sources-v2.md | sed -n '130,300p'",
 "description": "Read v2 doc lines 130-300"
}
````

### User / tool · 2026-11-02T03:54:30.166Z

**tool result**
````
   130	  (intake denial vs older note); calibrated confidence (per-state precision, not a "TBI likely" score).
   131	- **Synthetic-safety:** invented crash count and years (shift to e.g. 2019/2022 priors, 2026 index event); generic employment
   132	  facts omitted; ledger numbers invented.
   133	
   134	### P6. Health-insurer-paid claims: EOBs with billed, allowed, paid, patient share
   135	- **Source:** Gunn v. McCoy, 554 S.W.3d 645 (Tex. 2018), decided 2018-06-15 (one secondary source says 2018-02-08; trust the
   136	  reporter citation) — https://dallas-appellate.blogspot.com/2018/06/kmh-scotx-insurance-agents-may-know.html and
   137	  https://painterfirm.com/medmal/texas-supreme-court-allows-streamlined-approach-to-medical-billing-affidavits/ (summary only).
   138	- **Summary:** In a health care liability claim (medical malpractice, not a crash case), the plaintiff replaced provider
   139	  billing affidavits with affidavits from health insurers' subrogation agents stating amounts actually paid; the court held
   140	  §18.001 does not limit affiants to providers or their custodians.
   141	- **Record features (from source):** insurer subrogation-agent affidavits stating amounts paid.
   142	- **Record features (our inference):** insurer EOB pages (billed / allowed / plan paid / deductible / coinsurance / patient responsibility /
   143	  "not covered" with a remark code); the same date of service appearing on a provider bill and an EOB with different numbers;
   144	  the affidavit page itself.
   145	- **D-042 / flags:** billing analysis (paid vs incurred, never chosen by the LLM; code reconciles EOB to provider bill and
   146	  flags mismatches); charge reclassification guard (an "allowed amount" is not a charge); dedupe of the same service across
   147	  two documents.
   148	- **Synthetic-safety:** invented insurer, plan and remark codes; amounts invented; no real payer names.
   149	
   150	### P7. Pain out of proportion, "somatization", "symptom magnification" in the exam note
   151	- **Source:** Rodriguez v. Wal-Mart Stores, Inc., A-2/3-17 (N.J. 2019-03-04) —
   152	  https://www.njcourts.gov/system/files/court-opinions/2019/a_2_3_17.pdf (syllabus read).
   153	- **Summary:** A shopper hit by a falling display developed a CRPS diagnosis. A defense neurologist described a strong pain
   154	  reaction to light touch while a companion rubbed the same arm without a reaction, found nothing objective, and used
   155	  "somatization" and "symptom magnification". The court held such terms are admissible case by case, distinguished them from
   156	  "malingering", and upheld admission of unrelated past medical history.
   157	- **Record features (from source):** a defense neurologist's exam narrating observed behavior (pain reaction to light touch vs
   158	  none when a companion touched the arm), no objective findings, "somatization" and "symptom magnification"; unrelated past
   159	  medical history.
   160	- **Record features (our inference):** treater notes using the same CRPS vocabulary in the opposite direction.
   161	- **Case stage:** a defense medical exam is a post-suit event (in Texas, TRCP 204 needs a motion and court order). For a
   162	  pre-suit demand packet use the same wording in a carrier records-review (peer-review) letter instead (see lib12).
   163	- **D-042 / flags:** credibility flags (D-043: any credibility term flags; a second clause or contrast word always flags);
   164	  speaker attribution v2 (examiner's observation vs patient's report vs companion's behavior); LLM-as-judge visible; the tool
   165	  never concludes malingering.
   166	- **Synthetic-safety:** different mechanism (e.g. falling shelf at a hardware store), different limb, invented examiner;
   167	  no psychiatric details beyond a generic history line.
   168	
   169	### P8. Waddell signs charted as a score
   170	- **Source:** Fishbain et al., "A Structured Evidence-Based Review on the Meaning of Nonorganic Physical Signs: Waddell
   171	  Signs", Pain Medicine 4(2):141–181 (2003); companion review Clin J Pain 20(6):399–408 (2004) —
   172	  https://www.statpearls.com/articlelibrary/viewarticle/31286/ (StatPearls overview; reviews seen via search summaries only).
   173	- **Summary:** Reviews of the Waddell literature found the signs associated with poorer treatment outcomes but not reliably
   174	  with secondary gain or malingering; adjusters and IMEs still cite a positive count as a credibility point.
   175	- **Record features (from source):** the five Waddell sign categories (superficial/non-anatomic tenderness, simulation,
   176	  distraction, regional disturbance, overreaction) charted as a count.
   177	- **Record features (our inference):** "Waddell 3/5 positive", "distraction SLR negative"; clean negations ("0/5 Waddell
   178	  signs") on other dates; FCE "effort inconsistent" lines. "Waddell" is an eponymous clinical term and is allowed in
   179	  packets (it is on the validator's eponym allow-list, not the denylist).
   180	- **D-042 / flags:** credibility flags with the D-043 allow-list (clean negation does not flag; mixed sentence flags);
   181	  dismissal-pattern learning must not learn to auto-dismiss credibility flags (eval-guarded).
   182	- **Synthetic-safety:** all wording composed fresh; invented PT/FCE provider and dates.
   183	
   184	### P9. Interpreter errors and ad hoc (family) interpreters in a Spanish-language history
   185	- **Source:** Flores G. et al., "Errors in medical interpretation and their potential clinical consequences in pediatric
   186	  encounters", Pediatrics 111(1):6–14 (2003) — AHRQ research summary
   187	  https://webarchive.library.unt.edu/web/20081105020658/http:/www.ahrq.gov/research/apr03/0403RA20.htm (summary only).
   188	  Corroborating (search excerpt only, page returned 403): Texas DWC Appeals Panel decisions on interpreter word choice
   189	  ("espalda" for the area between the shoulder blades; "cane" vs "crutches") — https://texasworker.com/?p=38127.
   190	- **Summary:** Thirteen audiotaped visits averaged 31 interpretation errors each; most had potential clinical consequences,
   191	  ad hoc interpreters' errors more often so (77% vs 53%); omission was the commonest error. One reported example turned a fall
   192	  into a reported assault.
   193	- **Record features (from source):** an ad hoc family interpreter; omissions; a mechanism that changed in interpretation
   194	  (fall reported as assault); "espalda" word choice (DWC excerpt only).
   195	- **Record features (our inference):** "Hx obtained via patient's son (interpreter)"; mechanism worded differently on two
   196	  records; a Spanish intake form beside an English provider note; DD/MM/YYYY dates on a form from a clinic across the
   197	  border.
   198	- **D-042 / flags:** Spanish-language records; speaker attribution v2 (who said it); conflict (mechanism mismatch, code
   199	  surfaces both); date-convention suggestion (pre-select with reason, one confirm); body-region ambiguity goes to human.
   200	- **Synthetic-safety:** no pediatric facts; adult patient, invented family member and clinic; Spanish text composed fresh.
   201	
   202	### P10. Copy-forward (cloned) notes that contradict the visit
   203	- **Source:** Steinkamp J., Kantrowitz J.J., Airan-Javia S., "Prevalence and Sources of Duplicate Information in the
   204	  Electronic Medical Record", JAMA Network Open 5(9) (2022-09-01) — https://pubmed.ncbi.nlm.nih.gov/36156143/ (abstract read).
   205	- **Summary:** Across about 104.5 million notes at one health system (2015–2020), 50.1% of text was duplicated from earlier
   206	  notes about the same patient, rising from 33% to 54.2%; 45.9% of duplicated text came from a different author.
   207	- **Record features (from source):** half of note text duplicated from earlier notes, often from another author.
   208	- **Record features (our inference):** identical ROS/exam blocks across visits weeks apart ("denies neck pain" copied into a neck-pain
   209	  follow-up); "pain 6/10" unchanged across six visits; a stale medication list; a plan that repeats a completed referral.
   210	- **D-042 / flags:** conflict (same-visit contradiction between HPI and copied ROS); dedupe must *not* merge two visits just
   211	  because text matches (code dedupes by date + provider + content, and shows near-duplicates for human review);
   212	  LLM-as-judge must catch a summary that cites the copied line as current; vertical stepper shows "near-duplicate text
   213	  across N visits".
   214	- **Synthetic-safety:** template text invented; invented clinic.
   215	
   216	### P11. Left/right transposition across records
   217	- **Source:** ElGhrably I., Fraser S.G., "An observational study of laterality errors in a sample of clinical records",
   218	  Eye 22(3):340–343 (2008) — https://www.nature.com/articles/6702590 (abstract via search excerpts).
   219	- **Summary:** In 100 randomly selected ophthalmic record sets the authors found 44 left/right transposition errors in 32
   220	  sets; 19 were later corrected; three consent forms named the wrong eye.
   221	- **Record features (from source):** left/right transpositions across a record set, some later corrected; consent forms
   222	  naming the wrong side.
   223	- **Record features (our inference):** "right shoulder" in the ER note, "left shoulder" in the ortho note, MRI ordered on one side and read on
   224	  the other; a radiculopathy side that flips; a correction addendum.
   225	- **D-042 / flags:** conflict (mixed-side exam findings, code-detected by side tokens per body part; never resolved by the
   226	  LLM); judge must reject a summary that silently picks a side; HITL step "confirm side".
   227	- **Synthetic-safety:** orthopedic not ophthalmic; invented providers; side flip placed at an invented visit.
   228	
   229	### P12. Handwritten, scanned pages with illegible entries
   230	- **Source:** Rodríguez-Vera F.J. et al., "Illegible handwriting in medical records", J R Soc Med 95(11):545–546 (2002) —
   231	  https://pmc.ncbi.nlm.nih.gov/articles/PMC1279250 (abstract-level via search; full text not read).
   232	- **Summary:** Of 117 hospital case notes, 15% were so illegible that meaning was unclear; surgical departments scored worse.
   233	- **Record features (from source):** illegible handwritten hospital notes whose meaning is unclear.
   234	- **Record features (our inference):** faxed or scanned urgent-care and chiropractic daily notes; checkbox SOAP forms; handwritten pain
   235	  scores and dates; signatures illegible; a typed later page that disagrees with a handwritten earlier page; skewed scans.
   236	- **D-042 / flags:** local OCR (Tesseract) with page image beside OCR text, OCR-derived items always need review; date-
   237	  convention suggestion for handwritten dates; PDF hidden-text detection (assumption, no public PI source found: a scanned
   238	  page whose embedded text layer differs from the image, e.g. a copy-service OCR layer; we include it adversarially).
   239	- **Synthetic-safety:** handwriting rendered synthetically (font or generated strokes), never scanned from a real chart.
   240	
   241	### P13. Concussion not diagnosed in the ER; LOC history changes later
   242	- **Source:** Powell J.M. et al., "Accuracy of Mild Traumatic Brain Injury Diagnosis", Arch Phys Med Rehabil 89(8):1550–1555
   243	  (2008) — https://natlawreview.com/article/new-study-finds-emergency-room-physicians-often-fail-to-diagnose-tbi (summary only).
   244	- **Summary:** Among ED patients who met CDC mild-TBI criteria by study interview, 56% had no documented TBI diagnosis in the
   245	  ED record; ED care focused on ruling out severe injury.
   246	- **Record features (from source):** an ED record with no TBI diagnosis for a patient who met mild-TBI criteria.
   247	- **Record features (our inference):** ER "denies LOC", "CT head negative", discharge dx "neck strain"; a later neurology note "brief LOC per
   248	  patient", headaches, word-finding complaints; a neuropsych page weeks later.
   249	- **D-042 / flags:** conflict (LOC denied vs reported, both cited); causation (patient-stated onset); new body system after
   250	  a gap; speaker attribution (per patient vs examiner). The tool does not diagnose concussion.
   251	- **Synthetic-safety:** invented ED and neurologist; mechanism changed; dates shifted.
   252	
   253	### P14. Chargemaster charge vs what is owed (rate-vs-charge trap on hospital bills)
   254	- **Source:** Bai G., Anderson G.F., "Extreme Markup: The Fifty US Hospitals With The Highest Charge-To-Cost Ratios",
   255	  Health Affairs 34(6) (2015) — https://publichealth.jhu.edu/2015/some-hospitals-marking-up-prices-more-than-1000-percent
   256	  (press release; paper not opened).
   257	- **Summary:** In 2012 Medicare cost-report data the typical hospital charged about 3.4 times Medicare-allowable cost; the 50
   258	  highest-markup hospitals charged roughly ten times, 49 of them for-profit.
   259	- **Record features (from source):** hospital charges several times cost.
   260	- **Record features (our inference):** UB-04-style itemized bill with revenue codes, units and unit price; a "self-pay discount" line; a
   261	  later statement with a contractual adjustment; a price list or rate sheet page that is not a charge.
   262	- **D-042 / flags:** charge reclassification guard (a rate becomes a charge only with code-verified charge wording plus a
   263	  judge re-check); billing analysis (units × unit price is recomputed in code and compared with the stated line total);
   264	  totals in code only.
   265	- **Synthetic-safety:** invented hospital, codes and prices; no real chargemaster data.
   266	
   267	### P15. Ambulance bill: base rate plus per-mile mileage
   268	- **Source:** FAIR Health, "A Window into Utilization and Cost of Ground Ambulance Services" (brief, 2023) —
   269	  https://mma.prnewswire.com/media/2207553/A_Window_into_Utilization_and_Cost_of_Ground_Ambulance_Services___A_FAIR_Health_Brief.pdf?p=pdf
   270	  (search excerpt only).
   271	- **Summary:** Ground ambulance claims are billed as a base transport line plus mileage per statute mile; most claim lines
   272	  were out of network (63.7% in 2018, 59.4% in 2022).
   273	- **Record features (from source):** a base transport line plus per-mile mileage; out-of-network claim lines. Medicare billing
   274	  rules confirm two lines per trip and loaded miles rounded up to the tenth (see research/record-formats.md §16).
   275	- **Record features (our inference):** EMS run sheet (times, vitals, "ambulatory at scene" or "stretcher") plus an invoice with "ALS base",
   276	  "mileage 14 mi @ $X/mi" and a line total; a balance-bill page.
   277	- **D-042 / flags:** charge reclassification (the per-mile rate is a rate; only the extended line or stated total is a charge);
   278	  billing analysis (lien/balance columns); code checks miles × rate = stated line.
   279	- **Synthetic-safety:** invented EMS agency, mileage and rates.
   280	
   281	### P16. Same-week symptom contradiction across two providers
   282	- **Source:** Lewis Brisbois write-up of a Harris County zero-damages defense verdict (trial 2023-12; published 2024-06-25)
   283	  — https://www.legal500.com/intelligence/united-states/litigation-mediation-arbitration/houston-office-secures-zero-damages-verdict-in-rear-end-collision-case
   284	  (fetched; defense-side account).
   285	- **Summary:** After an ER visit the next day and care with several providers, the plaintiff reported significant neck and
   286	  back pain to an orthopedic surgeon while denying those symptoms to her primary-care doctor; the defense also disputed a
   287	  recommended discectomy and pointed to photos of a minor impact. The jury awarded nothing.
   288	- **Record features (from source):** neck and back pain reported to an orthopedic surgeon while denied to the primary-care
   289	  doctor; a recommended discectomy; photos of minor impact.
   290	- **Case stage and entry:** in the source the PCP records came in by defense subpoena (post-suit). In a pre-suit demand
   291	  packet the PCP note arrives from the paralegal's own records request after the client lists the PCP on intake (lib13).
   292	- **Record features (our inference):** ortho note "low back pain 8/10, radiating" and a PCP note days apart with ROS "denies back pain"
   293	  (possibly copied forward, see P10); a surgical recommendation with a cost estimate; property-damage photos referenced but
   294	  not in the file.
   295	- **D-042 / flags:** conflict (cross-provider, code pairs nearby dates); billing analysis (estimate is not a charge, D-019);
   296	  vertical stepper HITL "two providers disagree; paralegal decides which to cite".
   297	- **Synthetic-safety:** drug-use facts from the write-up are **not** used; invented providers; shifted dates.
   298	
   299	### P17. Minimal property damage, low-speed impact (MIST) language in records
   300	- **Source:** Castro W.H. et al., "Do 'whiplash injuries' occur in low-speed rear impacts?", Eur Spine J 6(6):366–375
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:31.727Z

**tool call — Bash**
````
{
 "command": "cat -n research/case-library-sources-v2.md | sed -n '300,440p'",
 "description": "Read v2 doc lines 300-440"
}
````

### User / tool · 2026-11-02T03:54:31.810Z

**tool result**
````
   300	- **Source:** Castro W.H. et al., "Do 'whiplash injuries' occur in low-speed rear impacts?", Eur Spine J 6(6):366–375
   301	  (1997), PMID 9455663 — https://pubmed.ncbi.nlm.nih.gov/9455663/ (abstract read via PubMed). This replaces the round-1
   302	  source (a Texas appellate summary on a reconstructionist's five-mph opinion) because no court, district, docket or
   303	  reporter cite could be found for it and its page returned 403; its names stay on the denylist.
   304	- **Summary:** Nineteen volunteers in staged rear impacts (velocity change about 9-14 km/h) showed no injury signs on exam,
   305	  motion analysis or MRI, with one minor exception. The study is the kind of biomechanical evidence the defense cites for
   306	  "minor impact, soft tissue" arguments.
   307	- **Scope of support:** this source supports only the scenario theme (low-speed impacts are argued to be non-injurious).
   308	  It says nothing about EMS or ER wording.
   309	- **Record features (our inference):** EMS "minor damage to rear bumper", "ambulatory at scene", "refused transport"; ER
   310	  "low-speed MVC"; later treater notes that describe the crash as "violent" or "high impact" (patient-reported).
   311	- **D-042 / flags:** causation (scene facts per D-018 lexicon); conflict (mechanism description changes over time, both
   312	  attributed); speaker attribution.
   313	- **Synthetic-safety:** invented crash; no speeds or vehicles from the source; no study data reproduced in a packet.
   314	
   315	## Coverage map: pattern x D-042 feature
   316	
   317	| Feature (D-042 / base flags) | Patterns |
   318	|---|---|
   319	| Charge reclassification guard (rate vs charge) | P6, P14, P15 |
   320	| Billing analysis (billed, adjusted, paid, LOP/lien, cited) | P2, P3, P4, P5, P6, P14, P15, P16 |
   321	| Spanish-language records | P4, P9 |
   322	| Local OCR, scanned/handwritten pages | P12 |
   323	| PDF hidden-text detection | P12 (assumption-based, no public source) |
   324	| Date-convention suggestion | P9 (assumption), P12 |
   325	| Dismissal-pattern learning (eval guard) | P8 |
   326	| Calibrated confidence | P2, P5 |
   327	| Speaker attribution v2 | P4, P7, P9, P13, P17 |
   328	| LLM-as-judge visible | P3, P7, P10, P11 |
   329	| Vertical stepper / HITL hand-off | P1, P10, P11, P16 |
   330	| Credibility flags (D-043) | P7, P8 |
   331	| Conflict | P1, P5, P9, P10, P11, P13, P16, P17 |
   332	| Pre-existing | P2, P5 |
   333	| Causation language | P1, P2, P3, P13, P17 |
   334	| Gap | P1, P13 |
   335	
   336	## Suggested v2 packets (each recombines two or more patterns)
   337	
   338	Stage: every packet simulates a **pre-suit demand file** unless marked otherwise. "Entry" says how each cross-provider record
   339	reached the paralegal. Format sections refer to `research/record-formats.md`.
   340	
   341	| Proposed id | Combines | One-line synthetic premise | Stage / entry |
   342	|---|---|---|---|
   343	| lib08_second_crash_mri_after | P1 + P13 | Rear-end, PT, second minor crash 11 weeks later, MRI and neuro note after crash 2 | Pre-suit; all records from the firm's requests to each provider |
   344	| lib09_spanish_interpreter_espalda | P9 + P4 + P11 | History via son; "espalda" ambiguity; side flips between ER and ortho | Pre-suit; Spanish clinic note supplied by the client |
   345	| lib10_eob_vs_provider_bill | P6 + P14 | Insured patient; hospital itemized bill plus EOBs with different numbers for same DOS | Pre-suit; EOBs from the client's health plan |
   346	| lib11_priors_and_ledger | P5 + P2 | Two prior crashes denied on intake; ledgers; older patient comorbidities | Pre-suit; older notes from a records request to the PCP |
   347	| lib12_records_review_credibility | P7 + P8 | Carrier records-review (peer-review) letter with symptom-magnification wording; PT/FCE notes with clean and mixed Waddell lines | Pre-suit; review letter came with the carrier's response to the demand. Litigation-stage variant: TRCP 204 exam report |
   348	| lib13_cloned_notes_cross_provider | P10 + P16 | Copied ROS denies the complaint the ortho charts the same week | Pre-suit; PCP note from the firm's records request after the client listed the PCP |
   349	| lib14_handwritten_chiro_scans | P12 + P15 | Scanned handwritten daily notes; ambulance base + mileage invoice; hidden text layer | Pre-suit; chiro records faxed by the provider |
   350	| lib15_conclusory_letter_mist | P3 + P17 | "Accident caused all" letter; EMS minor-damage and refused-transport wording | Pre-suit; affidavits obtained from providers for later service, not yet served |
   351	
   352	**Must contain** (the builder's checklist; each packet's expected JSON asserts these) and **formats used**:
   353	
   354	| Proposed id | Must contain (D-042 features and flags) | Formats (record-formats.md §) |
   355	|---|---|---|
   356	| lib08 | Two incident dates in the chart (conflict); ED "denies LOC" vs neuro "brief LOC per patient" (conflict, speaker); first MRI dated after event 2; gap between PT discharge and the neuro visit; stepper HITL step "two incidents found" | EMS PCR §15, ED §2, PT §3, radiology §5, office/specialist note §19, ambulance invoice §16 |
   357	| lib09 | One date `03/06/2026` day-first (truth 3 June 2026) and one `14/05/2026`; "Hx via son (interpreter)"; "espalda" with no level; right vs left shoulder across ER and ortho (conflict, HITL confirm side); translation labeled as LLM output | Spanish note §13, ED §2, office/specialist note §19, scanned intake §14 |
   358	| lib10 | Same DOS on a provider bill and an EOB with different numbers (dedupe + mismatch flag); one UB-04 room line where FL44 rate × FL46 days = FL47 charge (rate-vs-charge guard); a 0001 total line; one CMS-1500 amount OCR'd without a separator with its truth stated | UB-04 §9, ledger §10, EOB §11, CMS-1500 §8 |
   359	| lib11 | Intake "prior accidents: none" vs an older note naming two prior crashes (conflict, pre_existing); ledger with billed, adjustment, payment + payer, balance and LOP columns (items 1-4 and 6, no contract column); comorbidity problem list; calibrated confidence on pre-existing | scanned intake §14, office/specialist note §19, ledger §10, LOP §12 |
   360	| lib12 | At least 4 credibility sentences across 3 dates: 2 clean negations ("0/5 Waddell signs") that must not flag, 2 mixed sentences ("Waddell 3/5; effort inconsistent") that must flag (D-043); at least 3 dismissable non-credibility flags so the dismissal-pattern guard is exercised | records-review/IME report §20, PT §3 |
   361	| lib13 | PCP ROS "denies back pain" copied across 3 visits, and an ortho note "low back pain 8/10" in the same week (conflict, cloned text, no merge); a surgical cost estimate line (D-019: not a charge); HITL "two providers disagree" | office/specialist note §19 (PCP and ortho), ED §2 |
   362	| lib14 | Scanned travel card with checkmarks; one handwritten date with no year; a CMS-1500 grouped line where days = units; an ambulance invoice where miles × per-mile rate = line total; a page whose hidden text layer differs from the image | chiro §4, scanned intake §14, CMS-1500 §8, EMS PCR §15, ambulance invoice §16 |
   363	| lib15 | EMS "refused transport" and "minor damage" (causation lexicon, speaker); ER "low-speed MVC" vs later "violent impact" per patient (conflict); a narrative letter "caused all treatment" shown verbatim, never upgraded (judge rejects any summary that states it as fact); an 18.001 affidavit whose attached bill duplicates a bill already in the packet (dedupe) | EMS PCR §15, ED §2, chiro §4, narrative letter §18, 18.001 affidavit §17 |
   364	
   365	## Denylist additions
   366	
   367	Every real person's name and every firm-website slug or organisation name cited in this file's sources, including the
   368	study authors (Steinkamp, Kantrowitz, Airan-Javia, ElGhrably, Fishbain, Powell, Anderson, Fraser, Brinjikji, Nakashima,
   369	Rodríguez-Vera, Flores, Bai) and the bare-name citation list in the opening paragraph (Brinjikji, Nakashima). The same list is
   370	in `DENYLIST_V2` / `DENY_CAPITALISED` of `research/validate_library.py`. `python3 research/validate_library.py --self-test`
   371	fails if the two drift apart, if any surname it extracts from this file (author initials or 'et al', citation list, or
   372	"X v. Y" caption) is not listed, or if a planted name in mixed case passes. Matching is case-insensitive and
   373	accent-insensitive; the four capitalised-only terms are also ordinary lowercase words or phrases. Allowed on purpose:
   374	"Waddell" (clinical eponym).
   375	
   376	```text
   377	JLG
   378	Garza
   379	Pechero
   380	Zapata
   381	Guevara
   382	Ferrer
   383	Donis
   384	Matamoros
   385	Castellanos
   386	Morehouse
   387	Reuben
   388	Rueben
   389	Poissant
   390	I-45
   391	Chiv
   392	Figueroa
   393	Central Oregon
   394	Oregon
   395	Broussard
   396	Gunn
   397	McCoy
   398	Rodriguez
   399	Wal-Mart
   400	Walmart
   401	Lewis Brisbois
   402	Brisbois
   403	Harris County
   404	Hampton
   405	Miskell
   406	Baratta
   407	I-635
   408	Castro
   409	Schilgen
   410	Steinkamp
   411	Kantrowitz
   412	Airan-Javia
   413	ElGhrably
   414	Fishbain
   415	Powell
   416	Anderson
   417	Houston
   418	Dallas
   419	Allstate
   420	Fraser
   421	Brinjikji
   422	Nakashima
   423	Vera
   424	Rodríguez-Vera
   425	mdjwlaw
   426	painterfirm
   427	Hills        # capitalised only
   428	Flores       # capitalised only
   429	Bai          # capitalised only
   430	FAIR Health  # capitalised only (organisation)
   431	```
   432	
   433	## Assumptions and limits
   434	
   435	- Hidden-text PDFs and DD/MM/YYYY dates in Spanish-language records are our adversarial assumptions; no public PI source
   436	  documented them. They are included because D-042 reinstated those features and they need test cases.
   437	- Texas DWC Appeals Panel decisions (P9) were seen only as a search excerpt (page returned 403). Hampton v. Miskell was
   438	  dropped as P17's source in round 2: no court, district or docket could be found and its page returned 403.
   439	- P4 (Chiv v. Figueroa) and P17 (Castro et al.) support only the scenario theme, not any record wording.
   440	- Statute currency: CPRC §18.001/§18.002 text was checked 2026-11-02 through the texas.public.law mirror (amended through
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:55:35.716Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-paralegal-r3-names.py",
 "content": "#!/usr/bin/env python3\n\"\"\"T-077 round 3 (paralegal-reviewer): independent name extraction, self-test mutations, scratch-packet plants.\n\nReads research/validate_library.py and research/case-library-sources-v2.md at HEAD (commit 8d7548d). Mutations and planted\npackets are written only under the session scratchpad; nothing in the repo is changed.\nRun: python3 artifacts/review-evidence/T-077-paralegal-r3-names.py > artifacts/review-evidence/T-077-paralegal-r3-names.out\n\"\"\"\nimport contextlib, importlib.util, io, pathlib, re, shutil, subprocess, sys\n\nREPO = pathlib.Path(\"/Users/arsis/zlayt-pm-project\")\nSCR = pathlib.Path(\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\")\nVAL = REPO / \"research\" / \"validate_library.py\"\nDOC = REPO / \"research\" / \"case-library-sources-v2.md\"\n\n\ndef load(path, name):\n    spec = importlib.util.spec_from_file_location(name, path)\n    m = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(m)\n    return m\n\n\nv = load(VAL, \"vl_repo\")\ndoc = DOC.read_text()\nlisted = {v.fold(w).lower() for w in v.DENYLIST + v.DENY_CAPITALISED + v.ALLOWED_EPONYMS}\n\nprint(\"=== A. mechanical extraction by the validator (self-test inputs) ===\")\nauthors = v.doc_author_names(doc)\ncites = v.doc_listed_citation_names(doc)\ncaps = v.doc_caption_names(doc)\nfor label, s in ((\"author\", authors), (\"citation-list\", cites), (\"caption\", caps)):\n    for n in sorted(s):\n        print(f\"{label:14s} {n:22s} {'covered' if v._covered(n, listed) else 'NOT COVERED'}\")\nprint(\"counts: author\", len(authors), \"citation-list\", len(cites), \"caption\", len(caps))\n\nprint()\nprint(\"=== B. independent scan: every capitalised token in the doc prose (denylist section excluded) ===\")\nprose = doc.split(\"## Denylist additions\")[0]\ntok_rx = re.compile(r\"(?<![\\w'’-])([A-Z][\\w'’-]*(?:[- ][A-Z][\\w'’-]*)*)\")\nhits = {}\nfor ln, line in enumerate(prose.splitlines(), 1):\n    for m in tok_rx.finditer(line):\n        t = m.group(1)\n        hits.setdefault(t, []).append(ln)\nuncovered = []\nfor t, lines in sorted(hits.items()):\n    if v.scan_text(t):\n        continue\n    if any(v._covered(p, listed) for p in [t]):\n        continue\n    uncovered.append((t, lines))\nprint(\"distinct capitalised tokens:\", len(hits), \" not hit by denylist scan:\", len(uncovered))\nfor t, lines in uncovered:\n    print(f\"{t!r:45s} lines {lines[:6]}{' ...' if len(lines) > 6 else ''}\")\n\nprint()\nprint(\"=== C. self-test mutations (doc text altered in memory; validator unchanged) ===\")\n\n\ndef run_self_test(doc_text):\n    buf = io.StringIO()\n    with contextlib.redirect_stdout(buf):\n        rc = v.self_test(doc_text=doc_text)\n    return rc, buf.getvalue().strip()\n\n\nbase_rc, base_out = run_self_test(None)\nprint(\"baseline:\", base_rc, base_out)\n\nmutations = {\n    \"M1 new author with initials in source line (Smithers K.L.)\":\n        doc.replace(\"Steinkamp J., Kantrowitz J.J.\", \"Steinkamp J., Smithers K.L., Kantrowitz J.J.\", 1),\n    \"M2 new author-year 'Smithers (2019)' with no initials\":\n        doc.replace(\"## Patterns\", \"## Patterns\\n\\nA related review (Smithers 2019) is also cited.\", 1),\n    \"M3 new 'Smithers et al.' form\":\n        doc.replace(\"Fishbain et al.\", \"Smithers et al.\", 1),\n    \"M4 new prose mention 'as Smithers reported' (no initials)\":\n        doc.replace(\"the court held\", \"as Smithers reported, the court held\", 1),\n    \"M5 new caption 'Smithers v. Jones' in P1\":\n        doc.replace(\"JLG Trucking, LLC v. Garza\", \"JLG Trucking, LLC v. Garza; Smithers v. Jones\", 1),\n    \"M6 new bare name in parenthesised 'already cited' list\":\n        doc.replace(\"Brinjikji, Nakashima)\", \"Brinjikji, Nakashima, Smithers)\", 1),\n    \"M7 new surname in comma-year cite 'Smithers, 2019'\":\n        doc.replace(\"Powell J.M. et al.\", \"Smithers, 2019; Powell J.M. et al.\", 1),\n    \"M8 control: new name already on denylist ('Fraser S.G.' repeated)\":\n        doc.replace(\"Fraser S.G.\", \"Fraser S.G.; Fraser S.G.\", 1),\n}\nfor label, new in mutations.items():\n    if new == doc:\n        print(f\"{label}: MUTATION DID NOT APPLY\")\n        continue\n    rc, out = run_self_test(new)\n    flagged = [ln for ln in out.splitlines() if \"FAIL\" in ln or \"not on the denylist\" in ln or \"passed\" in ln]\n    print(f\"{label}\\n    exit={rc}  {('; '.join(flagged))[:400] if flagged else out[:200]}\")\n\nprint()\nprint(\"=== D. mutation of the validator copy: delete a cited author from the list ===\")\ncopy = SCR / \"r3copy\"\nif copy.exists():\n    shutil.rmtree(copy)\n(copy / \"research\").mkdir(parents=True)\nshutil.copytree(REPO / \"evals\" / \"golden\", copy / \"evals\" / \"golden\")\nshutil.copytree(REPO / \"evals\" / \"library\", copy / \"evals\" / \"library\")\nsrc_py = VAL.read_text()\nsrc_doc = DOC.read_text()\nfor mut_name, term_line in ((\"Fraser\", '\"Fraser\", \"Brinjikji\"'), (\"Brinjikji\", '\"Brinjikji\", \"Nakashima\"')):\n    shutil.copy(VAL, copy / \"research\" / \"validate_library.py\")\n    shutil.copy(DOC, copy / \"research\" / \"case-library-sources-v2.md\")\n    py = src_py\n    dc = src_doc\n    if term_line not in py:\n        print(\"term line not found:\", term_line)\n        continue\n    py = py.replace(term_line, term_line.replace(f'\"{mut_name}\", ', \"\"), 1)\n    dc = dc.replace(f\"\\n{mut_name}  # \", \"\\n#  \", 1) if f\"\\n{mut_name}  # \" in dc else dc\n    dc = re.sub(rf\"^{mut_name}\\n\", \"\", dc, count=0, flags=re.M) if mut_name == \"Fraser\" else dc\n    (copy / \"research\" / \"validate_library.py\").write_text(py)\n    (copy / \"research\" / \"case-library-sources-v2.md\").write_text(dc)\n    r = subprocess.run([sys.executable, \"-I\", str(copy / \"research\" / \"validate_library.py\"), \"--self-test\"],\n                       capture_output=True, text=True, cwd=str(copy))\n    print(f\"removed {mut_name!r} from DENYLIST_V2 and the doc block -> self-test exit={r.returncode}\")\n    for ln in (r.stdout + r.stderr).splitlines():\n        if \"FAIL\" in ln:\n            print(\"   \", ln[:220])\n            break\n    if r.returncode == 0:\n        print(\"    \" + (r.stdout.strip()[:200]))\n\nprint()\nprint(\"=== E. scan_text on single probe strings (validator's denylist, case/accent-insensitive) ===\")\nprobes = [\"Fraser S.G.\", \"Brinjikji\", \"Nakashima\", \"Rodriguez-Vera F.J.\", \"Fair Health\", \"FAIR Health\", \"fair health\",\n          \"Painter Law Firm\", \"painterfirm\", \"MDJW\", \"mdjwlaw\", \"Lewis Brisbois\", \"Hills v. Donis\", \"hills\", \"Smithers K.L.\",\n          \"Waddell 3/5\", \"Dr. Waddell\"]\nfor p in probes:\n    print(f\"{p!r:24s} -> {v.scan_text(p)}\")\n\nprint()\nprint(\"=== F. planted packets in a scratch copy, run through the real validator entry point ===\")\nplants = {\n    \"case_planted_fraser.txt\": \"Seen by Fraser S.G. at the clinic on 03/06/2026.\",\n    \"case_planted_brinjikji.txt\": \"Referred to Brinjikji at the clinic on 03/06/2026.\",\n    \"case_planted_fairhealth_titlecase.txt\": \"Ambulance billed to Fair Health plan, line 2, $0.\",\n    \"case_planted_painter.txt\": \"Records from Painter Medical Group, 03/06/2026.\",\n    \"case_planted_smithers_uncited.txt\": \"Seen by Smithers K.L. at the clinic on 03/06/2026.\",\n}\nbanner = \"SYNTHETIC — invented for evaluation; not real patient data\\n\"\nfor name, body in plants.items():\n    shutil.rmtree(copy / \"evals\" / \"library\", ignore_errors=True)\n    shutil.copytree(REPO / \"evals\" / \"library\", copy / \"evals\" / \"library\")\n    shutil.copy(VAL, copy / \"research\" / \"validate_library.py\")\n    shutil.copy(DOC, copy / \"research\" / \"case-library-sources-v2.md\")\n    (copy / \"evals\" / \"library\" / name).write_text(banner + body + \"\\n\")\n    r = subprocess.run([sys.executable, \"-I\", str(copy / \"research\" / \"validate_library.py\")],\n                       capture_output=True, text=True, cwd=str(copy))\n    fail_lines = [ln for ln in r.stdout.splitlines() if \"IDENTIFIER CHECK\" in ln or ln.startswith(\"identifier check\")]\n    print(f\"{name:40s} exit={r.returncode}  {fail_lines}\")\nprint(\"copy root:\", copy)\n"
}
````

### User / tool · 2026-11-02T03:55:35.815Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-paralegal-r3-names.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:55:46.947Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-paralegal-r3-names.py",
 "old_string": "    py = py.replace(term_line, term_line.replace(f'\"{mut_name}\", ', \"\"), 1)\n    dc = dc.replace(f\"\\n{mut_name}  # \", \"\\n#  \", 1) if f\"\\n{mut_name}  # \" in dc else dc\n    dc = re.sub(rf\"^{mut_name}\\n\", \"\", dc, count=0, flags=re.M) if mut_name == \"Fraser\" else dc",
 "new_string": "    py = py.replace(term_line, term_line.replace(f'\"{mut_name}\", ', \"\"), 1)\n    dc, n_block = re.subn(rf\"^{mut_name}\\n\", \"\", dc, flags=re.M)\n    print(f\"mutating {mut_name!r}: validator term removed, doc-block lines removed = {n_block}\")"
}
````

### User / tool · 2026-11-02T03:55:47.046Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-paralegal-r3-names.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:55:48.292Z

**tool call — Bash**
````
{
 "command": "python3 artifacts/review-evidence/T-077-paralegal-r3-names.py > artifacts/review-evidence/T-077-paralegal-r3-names.out 2>&1; echo \"exit=$?\"; cat artifacts/review-evidence/T-077-paralegal-r3-names.out",
 "description": "Run round-3 name probe script and save output"
}
````

### User / tool · 2026-11-02T03:55:50.043Z

**tool result**
````
exit=0
=== A. mechanical extraction by the validator (self-test inputs) ===
author         Airan-Javia            covered
author         Anderson               covered
author         Bai                    covered
author         Castro                 covered
author         ElGhrably              covered
author         Fishbain               covered
author         Flores                 covered
author         Fraser                 covered
author         Kantrowitz             covered
author         Powell                 covered
author         Rodríguez-Vera         covered
author         Steinkamp              covered
citation-list  Airan-Javia            covered
citation-list  Anderson               covered
citation-list  Bai                    covered
citation-list  Brinjikji              covered
citation-list  ElGhrably              covered
citation-list  Fishbain               covered
citation-list  Flores                 covered
citation-list  Fraser                 covered
citation-list  Guevara                covered
citation-list  Haygood                covered
citation-list  Kantrowitz             covered
citation-list  Nakashima              covered
citation-list  Powell                 covered
citation-list  Rodríguez-Vera         covered
citation-list  Steinkamp              covered
caption        Allstate               covered
caption        Central Oregon         covered
caption        Chiv                   covered
caption        Donis                  covered
caption        Ferrer                 covered
caption        Figueroa               covered
caption        Garza                  covered
caption        Guevara                covered
caption        Gunn                   covered
caption        Hampton                covered
caption        Hills                  covered
caption        JLG                    covered
caption        McCoy                  covered
caption        Miskell                covered
caption        Rodriguez              covered
caption        Wal-Mart               covered
counts: author 12 citation-list 15 caption 16

=== B. independent scan: every capitalised token in the doc prose (denylist section excluded) ===
distinct capitalised tokens: 281  not hit by denylist scan: 237
'A'                                           lines [102, 153, 153]
'A Structured Evidence-Based Review'          lines [170]
'A Window'                                    lines [268]
'A-2'                                         lines [151]
'AHRQ'                                        lines [186]
'ALS'                                         lines [275]
'A_Window_into_Utilization_and_Cost_of_Ground_Ambulance_Services___A_FAIR_Health_Brief' lines [269]
'Accident'                                    lines [350]
'Accuracy'                                    lines [242]
'Across'                                      lines [205]
'After'                                       lines [117, 285]
'Ambulance'                                   lines [267]
'Among ED'                                    lines [244]
'An'                                          lines [62, 217]
'App'                                         lines [76, 100]
'Arch Phys Med Rehabil'                       lines [242]
'At'                                          lines [360]
'Billing'                                     lines [75, 320]
'CDC'                                         lines [244]
'CMS-1500'                                    lines [358, 358, 362, 362]
'CRPS'                                        lines [153, 160]
'CT'                                          lines [247]
'Calibrated'                                  lines [326]
'Carrier'                                     lines [347]
'Case'                                        lines [1, 77, 161, 290]
'Causation'                                   lines [333]
'Charge'                                      lines [319]
'Chargemaster'                                lines [253]
'Clin J Pain'                                 lines [171]
'Combines'                                    lines [341]
'Common'                                      lines [27]
'Concussion'                                  lines [241]
'Conflict'                                    lines [331]
'Copied ROS'                                  lines [348]
'Copy-forward'                                lines [202]
'Corroborating'                               lines [188]
'Cost'                                        lines [268]
'Court'                                       lines [16]
'Coverage'                                    lines [315]
'Credibility'                                 lines [330]
'D-013'                                       lines [5]
'D-018'                                       lines [311]
'D-019'                                       lines [295, 361]
'D-042'                                       lines [5, 51, 70, 93, 109, 129] ...
'D-043'                                       lines [6, 163, 180, 330, 360]
'DD'                                          lines [196]
'DOS'                                         lines [345]
'DWC'                                         lines [194]
'Date-convention'                             lines [324]
'Dates'                                       lines [30]
'Denylist'                                    lines [25]
'Dismissal-pattern'                           lines [325]
'Dist'                                        lines [76, 100]
'Do'                                          lines [300]
'Dr'                                          lines [24]
'Duplicate Information'                       lines [203]
'ED'                                          lines [245, 245, 246, 251, 356, 356] ...
'EMS'                                         lines [68, 275, 279, 308, 309, 350] ...
'EMS PCR'                                     lines [356, 362, 363]
'EOB'                                         lines [142, 143, 145, 358, 358]
'EOBs'                                        lines [134, 345, 345]
'ER'                                          lines [8, 49, 68, 83, 223, 241] ...
'Each'                                        lines [32]
'Electronic Medical Record'                   lines [204]
'English'                                     lines [107, 196]
'Entry'                                       lines [338]
'Errors'                                      lines [185]
'Eur Spine J'                                 lines [300]
'Every'                                       lines [23, 24, 33]
'Extreme Markup'                              lines [254]
'Eye'                                         lines [218]
'F'                                           lines [254]
'FCE'                                         lines [178, 182, 347]
'FL44'                                        lines [358]
'FL46'                                        lines [358]
'FL47'                                        lines [358]
'Facts'                                       lines [32]
'Feature'                                     lines [5, 317]
'Feb'                                         lines [76]
'For'                                         lines [161]
'Format'                                      lines [339]
'Formats'                                     lines [354]
'Full'                                        lines [14]
'G'                                           lines [217]
'Gap'                                         lines [334]
'Ground'                                      lines [271]
'Ground Ambulance Services'                   lines [268]
'H'                                           lines [300]
'HITL'                                        lines [53, 226, 296, 329, 356, 357] ...
'HPI'                                         lines [210]
'Handwritten'                                 lines [229]
'Health Affairs'                              lines [255]
'Health-insurer-paid'                         lines [134]
'History'                                     lines [344]
'Hx'                                          lines [195, 357]
'IME'                                         lines [360]
'IMEs'                                        lines [174]
'Illegible'                                   lines [230]
'Immediate'                                   lines [57]
'In'                                          lines [11, 115, 138, 219, 257, 290]
'Inc'                                         lines [151]
'Insured'                                     lines [345]
'Intake'                                      lines [359]
'Interpreter'                                 lines [184]
'Intervening'                                 lines [39]
'Invented'                                    lines [23]
'It'                                          lines [308]
'Item'                                        lines [127]
'J'                                           lines [151, 203, 230]
'J R Soc Med'                                 lines [230]
'JAMA Network Open'                           lines [204]
'JSON'                                        lines [33, 352]
'June'                                        lines [357]
'K'                                           lines [11]
'LLC'                                         lines [40]
'LLM'                                         lines [94, 109, 145, 226, 357]
'LLM-as-judge'                                lines [94, 164, 212, 328]
'LOC'                                         lines [241, 247, 247, 249, 356, 356]
'LOP'                                         lines [9, 127, 320, 359, 359]
'Left'                                        lines [216]
'Litigation-stage'                            lines [347]
'Local OCR'                                   lines [322]
'M'                                           lines [242]
'MIST'                                        lines [299]
'MM'                                          lines [196]
'MRI'                                         lines [47, 223, 305, 343, 356]
'MVC'                                         lines [310, 363]
'Marrowgate'                                  lines [23]
'Meaning'                                     lines [170]
'Medical'                                     lines [17]
'Mild Traumatic Brain Injury Diagnosis'       lines [242]
'Minimal'                                     lines [299]
'Must'                                        lines [352, 354]
'N'                                           lines [151, 213]
'Nineteen'                                    lines [304]
'No'                                          lines [8, 22, 34, 76, 79, 100] ...
'None'                                        lines [10]
'Nonorganic Physical Signs'                   lines [170]
'Nothing'                                     lines [34]
'OCR'                                         lines [236, 236, 238]
"OCR'd"                                       lines [358]
'OCR-derived'                                 lines [236]
'ORCHESTRATOR_DECISIONS'                      lines [5]
'ORIF'                                        lines [9]
'Of'                                          lines [232]
'One'                                         lines [191, 357]
'One-line'                                    lines [341]
'P1'                                          lines [39, 329, 331, 333, 334, 343]
'P10'                                         lines [202, 293, 328, 329, 331, 348]
'P11'                                         lines [216, 328, 329, 331, 344]
'P12'                                         lines [229, 322, 323, 324, 349]
'P13'                                         lines [241, 327, 331, 333, 334, 343]
'P14'                                         lines [253, 319, 320, 345]
'P15'                                         lines [267, 319, 320, 349]
'P16'                                         lines [281, 320, 329, 331, 348]
'P17'                                         lines [299, 327, 331, 333, 350]
'P2'                                          lines [57, 320, 326, 332, 333, 346]
'P3'                                          lines [75, 320, 328, 333, 350]
'P4'                                          lines [99, 320, 321, 327, 344]
'P5'                                          lines [114, 320, 326, 331, 332, 346]
'P6'                                          lines [134, 319, 320, 345]
'P7'                                          lines [150, 327, 328, 330, 347]
'P8'                                          lines [169, 325, 330, 347]
'P9'                                          lines [184, 321, 324, 327, 331, 344]
'PCP'                                         lines [290, 291, 291, 292, 346, 348] ...
'PCP ROS'                                     lines [361]
'PDF'                                         lines [77, 237, 323]
'PI'                                          lines [17, 17, 237]
'PMC1279250'                                  lines [231]
'PMID'                                        lines [301]
'PT'                                          lines [42, 43, 46, 182, 343, 347] ...
'Packet'                                      lines [30]
'Pain'                                        lines [150]
'Pain Medicine'                               lines [171]
'Past-medical'                                lines [83]
'Pattern'                                     lines [21]
'Patterns'                                    lines [37, 317]
'Pediatrics'                                  lines [186]
'Pennywhistle'                                lines [24]
'Pre-existing'                                lines [332]
'Pre-suit'                                    lines [343, 344, 345, 346, 347, 348] ...
'Prevalence'                                  lines [203]
'Prior'                                       lines [114]
'Proposed'                                    lines [341, 354]
'PubMed'                                      lines [301]
'ROS'                                         lines [208, 210, 292]
'Read'                                        lines [14]
'Real'                                        lines [31]
'Rear-end'                                    lines [343]
'Record'                                      lines [46, 49, 66, 68, 88, 91] ...
'Researched'                                  lines [4]
'Reviews'                                     lines [173]
'S'                                           lines [40, 58, 135]
'SLR'                                         lines [177]
'SOAP'                                        lines [234]
'SYNTHETIC'                                   lines [33]
'Same DOS'                                    lines [358]
'Same-week'                                   lines [281]
'Scanned'                                     lines [349, 362]
'Scope'                                       lines [105, 307]
'Separately'                                  lines [103]
'Seventeen'                                   lines [3]
'Signs'                                       lines [171]
'Soft-tissue'                                 lines [83]
'Source'                                      lines [40, 58, 76, 100, 115, 135] ...
'Sources'                                     lines [10, 203]
'Spanish'                                     lines [35, 102, 107, 112, 196, 200] ...
'Spanish-language'                            lines [29, 109, 184, 198, 321]
'Spanish-speaking'                            lines [99, 105]
'Speaker'                                     lines [327]
'Stage'                                       lines [338, 341]
'StatPearls'                                  lines [172]
'Suggested'                                   lines [336]
'Summary'                                     lines [14, 42, 62, 83, 102, 117] ...
'Synthetic-safety'                            lines [19, 54, 73, 96, 112, 131] ...
'T-077'                                       lines [1]
'TBI'                                         lines [117, 130, 244, 246]
'TIN-20200211-item1'                          lines [81]
'TRCP'                                        lines [161, 347]
'Tesseract'                                   lines [236]
'Tex'                                         lines [40, 58, 76, 100, 115, 135]
'The'                                         lines [24, 42, 44, 53, 63, 78] ...
'The Fifty US Hospitals With The Highest Charge-To-Cost Ratios' lines [254]
'The MRI'                                     lines [43]
'Thirteen'                                    lines [190]
'This'                                        lines [301]
'Two'                                         lines [346, 356]
'UB-04'                                       lines [358, 358]
'UB-04-style'                                 lines [260]
'Utilization'                                 lines [268]
'Verify'                                      lines [15]
'Vertical'                                    lines [329]
'W'                                           lines [40, 58, 135]
'WL'                                          lines [81]
'We'                                          lines [21]
'X'                                           lines [276]
'YYYY'                                        lines [196]

=== C. self-test mutations (doc text altered in memory; validator unchanged) ===
baseline: 0 self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)
M1 new author with initials in source line (Smithers K.L.)
    exit=1  SELF-TEST FAIL: v2 doc cites author name 'Smithers' but it is not on the denylist (add it to DENYLIST_V2 and the doc block); SELF-TEST FAIL: planted author/citation surname 'Smithers' passed the library scan; self-test: FAIL
M2 new author-year 'Smithers (2019)' with no initials
    exit=0  self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)
M3 new 'Smithers et al.' form
    exit=1  SELF-TEST FAIL: v2 doc cites author name 'Smithers' but it is not on the denylist (add it to DENYLIST_V2 and the doc block); SELF-TEST FAIL: planted author/citation surname 'Smithers' passed the library scan; self-test: FAIL
M4 new prose mention 'as Smithers reported' (no initials)
    exit=0  self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)
M5 new caption 'Smithers v. Jones' in P1
    exit=1  SELF-TEST FAIL: v2 doc cites caption name 'Jones' but it is not on the denylist (add it to DENYLIST_V2 and the doc block); SELF-TEST FAIL: v2 doc cites caption name 'Smithers' but it is not on the denylist (add it to DENYLIST_V2 and the doc block); self-test: FAIL
M6 new bare name in parenthesised 'already cited' list
    exit=1  SELF-TEST FAIL: v2 doc cites citation-list name 'Smithers' but it is not on the denylist (add it to DENYLIST_V2 and the doc block); SELF-TEST FAIL: planted author/citation surname 'Smithers' passed the library scan; self-test: FAIL
M7 new surname in comma-year cite 'Smithers, 2019'
    exit=0  self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)
M8 control: new name already on denylist ('Fraser S.G.' repeated)
    exit=0  self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)

=== D. mutation of the validator copy: delete a cited author from the list ===
mutating 'Fraser': validator term removed, doc-block lines removed = 1
removed 'Fraser' from DENYLIST_V2 and the doc block -> self-test exit=1
    SELF-TEST FAIL: v2 doc cites author name 'Fraser' but it is not on the denylist (add it to DENYLIST_V2 and the doc block)
mutating 'Brinjikji': validator term removed, doc-block lines removed = 1
removed 'Brinjikji' from DENYLIST_V2 and the doc block -> self-test exit=1
    SELF-TEST FAIL: v2 doc cites citation-list name 'Brinjikji' but it is not on the denylist (add it to DENYLIST_V2 and the doc block)

=== E. scan_text on single probe strings (validator's denylist, case/accent-insensitive) ===
'Fraser S.G.'            -> ['Fraser']
'Brinjikji'              -> ['Brinjikji']
'Nakashima'              -> ['Nakashima']
'Rodriguez-Vera F.J.'    -> ['Rodriguez', 'Vera', 'Rodríguez-Vera']
'Fair Health'            -> []
'FAIR Health'            -> ['FAIR Health']
'fair health'            -> []
'Painter Law Firm'       -> []
'painterfirm'            -> ['painterfirm']
'MDJW'                   -> []
'mdjwlaw'                -> ['mdjwlaw']
'Lewis Brisbois'         -> ['Lewis Brisbois', 'Brisbois']
'Hills v. Donis'         -> ['Donis', 'Hills']
'hills'                  -> []
'Smithers K.L.'          -> []
'Waddell 3/5'            -> []
'Dr. Waddell'            -> []

=== F. planted packets in a scratch copy, run through the real validator entry point ===
case_planted_fraser.txt                  exit=1  ["IDENTIFIER CHECK FAIL: case_planted_fraser.txt: contains real identifier 'Fraser'", 'identifier check: FAIL']
case_planted_brinjikji.txt               exit=1  ["IDENTIFIER CHECK FAIL: case_planted_brinjikji.txt: contains real identifier 'Brinjikji'", 'identifier check: FAIL']
case_planted_fairhealth_titlecase.txt    exit=0  ['identifier check: ok (7 packets, 80 denylist terms, case-insensitive)']
case_planted_painter.txt                 exit=0  ['identifier check: ok (7 packets, 80 denylist terms, case-insensitive)']
case_planted_smithers_uncited.txt        exit=0  ['identifier check: ok (7 packets, 80 denylist terms, case-insensitive)']
copy root: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r3copy
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:56:50.823Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"painter\\|fair health\\|Health Affairs\\|Pediatrics\\|every real\\|capitalised only\\|case-insensitive\" research/case-library-sources-v2.md; echo \"---\"; grep -n \"DENY_CAPITALISED = \\|_CAP = \\|for variant in (w, w.upper())\" research/validate_library.py",
 "description": "Grep firm, organisation and matching-rule lines for evidence"
}
````

### User / tool · 2026-11-02T03:56:50.915Z

**tool result**
````
24:   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass. Every real name in this file is on
137:  https://painterfirm.com/medmal/texas-supreme-court-allows-streamlined-approach-to-medical-billing-affidavits/ (summary only).
186:  encounters", Pediatrics 111(1):6–14 (2003) — AHRQ research summary
255:  Health Affairs 34(6) (2015) — https://publichealth.jhu.edu/2015/some-hospitals-marking-up-prices-more-than-1000-percent
268:- **Source:** FAIR Health, "A Window into Utilization and Cost of Ground Ambulance Services" (brief, 2023) —
367:Every real person's name and every firm-website slug or organisation name cited in this file's sources, including the
372:"X v. Y" caption) is not listed, or if a planted name in mixed case passes. Matching is case-insensitive and
426:painterfirm
427:Hills        # capitalised only
428:Flores       # capitalised only
429:Bai          # capitalised only
430:FAIR Health  # capitalised only (organisation)
---
59:DENY_CAPITALISED = ["Hills", "Flores", "Bai", "FAIR Health"]
72:_CAP = [(w, re.compile(r"(?<!\w)(?:" + re.escape(w) + "|" + re.escape(w.upper()) + r")(?!\w)")) for w in DENY_CAPITALISED]
155:        for variant in (w, w.upper()):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:57:02.454Z

**tool call — Bash**
````
{
 "command": "grep -n \"_AUTHOR_RX = \\|def doc_listed_citation_names\\|if \\\"cited\\\" not in para\\|def doc_caption_names\\|for variant in (w, w.upper())\\|_CAP = \" research/validate_library.py; ls reviews/ | grep T-077; ls artifacts/review-evidence/ | grep T-077-paralegal-r3",
 "description": "Get validator line numbers for cited evidence"
}
````

### User / tool · 2026-11-02T03:57:02.557Z

**tool result**
````
72:_CAP = [(w, re.compile(r"(?<!\w)(?:" + re.escape(w) + "|" + re.escape(w.upper()) + r")(?!\w)")) for w in DENY_CAPITALISED]
93:def doc_caption_names(doc_text):
110:_AUTHOR_RX = re.compile(r"(?<![\w'’-])([A-Z][\w'’-]*)(?=,? [A-Z]\.(?:[A-Z]\.)*(?!\w)|\s+et al\b)")
118:def doc_listed_citation_names(doc_text):
126:        if "cited" not in para:
155:        for variant in (w, w.upper()):
T-077-paralegal-r2.md
T-077-paralegal.md
T-077-paralegal-r3-names.out
T-077-paralegal-r3-names.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:57:30.095Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r3.md",
 "content": "# T-077 round 3: paralegal-reviewer (research/validate_library.py + research/case-library-sources-v2.md, commit 8d7548d)\n\n**Verdict: changes.** The round-2 major is closed for the name shapes the validator parses. Every real person and party name in the v2 doc, study authors included, is on the denylist, and the library scan passes. Two gaps remain. The self-test only extracts names in three shapes (author initials or \"et al\", the bracketed \"already cited\" list, and \"X v. Y\" captions), so a new name cited in author-year form or in prose passes silently. And the capitalised-only matcher misses the title-case \"Fair Health\", although the doc claims case-insensitive matching. Neither gap is a blocker: no current packet and no current doc name is uncovered.\n\n## Answers to the four checks\n\n1. **Every cited real name is denylisted.** Yes. The self-test extracts 12 author surnames, 15 citation-list names and 16 caption names, and all 43 are covered. My own independent scan of every capitalised token in the doc prose (section B) found no person or party name outside the list. The only uncovered tokens are generic words, journal and publisher titles, agencies, URL fragments and invented names (Marrowgate, Pennywhistle, both v1 examples).\n2. **The self-test extracts mechanically and fails on a new name, for some shapes only.** Fails: a new author with initials (M1, `Smithers K.L.`), a new \"et al\" author (M3), a new caption (M5), and a new name in the bracketed \"already cited\" list (M6). Passes with exit 0: author-year with no initials (M2, `Smithers 2019`), prose mention (M4, `as Smithers reported`), and comma-year (M7, `Smithers, 2019`). Deleting Fraser or Brinjikji from the validator and the doc block makes the self-test exit 1 (section D), so the list itself is guarded.\n3. **Planted names in a scratch packet.** Fraser and Brinjikji planted in a packet in a scratch copy of the library make the real validator entry point exit 1 (`IDENTIFIER CHECK FAIL: ... contains real identifier 'Fraser'`). Title-case `Fair Health` passes (exit 0). An uncited, unlisted `Smithers` passes, as the list-based scan is designed to.\n4. **Judgment call on firm and organisation names.** Acceptable for synthetic-data safety with two conditions. A journal, publisher, agency or website domain is not a patient, provider or party identifier, and cannot be mistaken for one in a packet, so leaving those out is defensible. Firm words are different: `Painter` is a plausible invented surname, and the slug `painterfirm` implies a firm named Painter, so slug-only coverage leaves it open. Condition 1: fix the title-case FAIR Health gap (F2). Condition 2: add `Painter` as capitalised-only, as `Hills`, `Flores` and `Bai` are, and state the organisation exemption in the doc (F3).\n\n## Commands run and output\n\n```\n$ python3 research/validate_library.py --self-test\nself-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)     exit 0\n$ python3 research/validate_library.py\ngolden OK: 17 cases (16 synthetic), 85 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered\nidentifier check: ok (7 packets, 80 denylist terms, case-insensitive)      exit 0\n$ python3 artifacts/review-evidence/T-077-paralegal-r3-names.py > artifacts/review-evidence/T-077-paralegal-r3-names.out\n```\n\nFull output: `artifacts/review-evidence/T-077-paralegal-r3-names.out`. Sections:\n- A: validator extraction, all 43 names covered.\n- B: independent token scan, 281 capitalised tokens, 237 not hit by the denylist scan; reviewed by hand, no uncited person or party name.\n- C: self-test mutations M1 to M8 (M8 is a control).\n- D: deleting `Fraser` or `Brinjikji` from list and doc block, self-test exit 1 both times.\n- E: `scan_text` on probes: `'Fair Health' -> []`, `'FAIR Health' -> ['FAIR Health']`, `'Painter Law Firm' -> []`, `'painterfirm' -> ['painterfirm']`.\n- F: planted packets in `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r3copy/evals/library/`, run via the real entry point.\n\nRound-2 finding F1 (four real names missing from the list): closed. Brinjikji, Nakashima, Fraser and Vera are now in `DENYLIST_V2` (validate_library.py:53-56 region) and in the doc block (case-library-sources-v2.md:420-424).\n\n## Findings\n\n1. **major: the self-test extracts names only in three shapes, so a new name cited in author-year form or in prose passes.** Evidence: `artifacts/review-evidence/T-077-paralegal-r3-names.out`, section C: `M2 new author-year 'Smithers (2019)' with no initials ... exit=0  self-test: ok`; `M4 new prose mention 'as Smithers reported' ... exit=0`; `M7 new surname in comma-year cite 'Smithers, 2019' ... exit=0`. The extraction is shape-bound: `research/validate_library.py:110` (`_AUTHOR_RX`, initials or \"et al\" only), `:118-126` (citation list only in paragraphs containing \"cited\"), `:93` (captions only). The doc's rule text, case-library-sources-v2.md:24-25 (\"Every real name in this file is on that denylist\") and :26-27 (\"--self-test extracts every author surname ...\"), reads as a whole-file guarantee, which the self-test does not give. Current state is clean (section B), so this is a guard gap for future edits, not a leak. Why it matters: the next research edit that cites a study as \"Smithers (2019)\" or \"as Smithers reported\" would pass the self-test, and a packet built from it would pass the scan. Fix: either require every proper-name token in the doc (outside a fenced allow-list) to be listed or explicitly exempted, or add author-year and prose-name shapes to the extractor and fail on any unlisted capitalised token that is not in a small stop list. Acceptance test: M2, M4 and M7 in section C each exit 1 with the name reported; the baseline still exits 0.\n\n2. **minor: \"Fair Health\" in title case is not caught.** Evidence: section E `'Fair Health' -> []` and section F `case_planted_fairhealth_titlecase.txt exit=0`. `research/validate_library.py:72` builds the capitalised-only matcher from `w` and `w.upper()` only, and the self-test at :155 checks the same two variants, so the test does not see the gap. The doc says matching is case-insensitive (case-library-sources-v2.md:372) and labels FAIR Health \"capitalised only\" (:430). Title case is the natural casing for an organisation name, so the intent is to match it. Why it matters: a payer named \"Fair Health\" in a packet passes the scan. Risk is low (organisation, not a person or patient), but the guard does not do what the doc says. Fix: match title case as well, e.g. `re.compile(..., re.I)` for multi-word capitalised-only terms, or add `w.title()` to the variants at :72 and :155. Acceptance test: the title-case packet in section F exits 1 and the self-test planted-variant check includes `Fair Health`.\n\n3. **minor: firm and organisation exemptions are implicit, and \"Painter\" is not listed.** Evidence: case-library-sources-v2.md:137 (`painterfirm.com`), section E `'Painter Law Firm' -> []`, and section F `case_planted_painter.txt exit=0`. The doc's rule at :367-368 says the denylist covers \"every real person's name and every firm-website slug or organisation name cited in this file's sources\", but organisation names cited in the file are not listed: Health Affairs (:255), Pediatrics and AHRQ (:186), PubMed, Legal500, Casemine, FindLaw, texasworker, hallapproved, natlawreview, statpearls. Slugs are listed (`mdjwlaw`, `painterfirm`), so the firm's own words (\"Painter\") are not. Why it matters: \"Painter\" is an ordinary surname that the doc's own rule 2 says to avoid as an invented name (:27-28 bans common surnames). The doc overclaims the rule text, and a reader cannot tell which organisations are exempt or why. Fix: add `Painter` as capitalised-only with the other surname-words, and state in :367-368 that publishers, journals, agencies and website domains are exempt because they are not patient, provider or party identifiers. Acceptance test: a packet with `Painter Medical Group` fails the scan; the doc sentence names the exemption.\n\n## Scores\n\nNot an app run, so `verify_quickly` does not apply. Scores below are for this research card.\n\n## Outside my lens\n\nWhether the cited opinions and studies are good law or accurately summarised. I checked only the names against the list and the validator's behaviour.\n\n```json\n{\"card\": \"T-077\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"research/validate_library.py and research/case-library-sources-v2.md at commit 8d7548d (round 3); evals/library (7 packets) and evals/golden; no app run (research card, no sample case)\",\n \"exercised\": [\n  \"Read personas/paralegal.md, reviews/T-077-paralegal-r2.md, reviews/T-077-paralegal.md (round-1 context), my memory files for T-052 and T-077 r2\",\n  \"git log --oneline -5; git show --stat 8d7548d (2 files: research/case-library-sources-v2.md, research/validate_library.py)\",\n  \"Read research/validate_library.py in full (about 180 lines) and research/case-library-sources-v2.md lines 1-440 with line numbers\",\n  \"python3 research/validate_library.py --self-test -> 'self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)', exit 0\",\n  \"python3 research/validate_library.py -> 'identifier check: ok (7 packets, 80 denylist terms, case-insensitive)', exit 0\",\n  \"artifacts/review-evidence/T-077-paralegal-r3-names.py (+ .out): A) validator extraction, all 43 names covered; B) independent scan of 281 capitalised doc tokens, no uncited person or party name; C) eight self-test mutations (M1-M8): M1, M3, M5, M6 fail as designed; M2, M4, M7 pass (gap); M8 control passes; D) deleting Fraser or Brinjikji from list and doc block -> self-test exit 1; E) scan_text probes; F) planted packets in a scratch copy run through the real validator: Fraser and Brinjikji exit 1, title-case Fair Health exit 0, Painter exit 0, uncited Smithers exit 0\",\n  \"grep -n on case-library-sources-v2.md for painter, fair health, Health Affairs, Pediatrics, 'every real', 'capitalised only', 'case-insensitive'; grep -n on validate_library.py for DENY_CAPITALISED, _CAP, _AUTHOR_RX, the 'cited' paragraph test and the variant loop\",\n  \"Not exercised: a fetch of the cited sources to check whether 'Painter' is the plaintiff firm's name; the packet-level check_golden run in the scratch copy was run only through the validator's main() entry point\"],\n \"verdict\": \"changes\",\n \"scores\": {\"denylist_covers_cited_names\": 4, \"self_test_mechanical_extraction\": 3, \"planted_name_fails_scan\": 4, \"firm_org_judgment\": 3, \"synthetic_safety_enforcement\": 3},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Self-test extracts names in three shapes only; author-year and prose-cited names pass silently\",\n   \"evidence\": \"artifacts/review-evidence/T-077-paralegal-r3-names.out section C: 'M2 new author-year 'Smithers (2019)' with no initials ... exit=0  self-test: ok'; 'M4 new prose mention 'as Smithers reported' ... exit=0'; 'M7 new surname in comma-year cite 'Smithers, 2019' ... exit=0'. Extraction: research/validate_library.py:110 (_AUTHOR_RX, initials or et al), :118-126 (citation list, only paragraphs containing 'cited'), :93 (captions). Doc rule: research/case-library-sources-v2.md:24-25 'Every real name in this file is on that denylist'; :26-27 '--self-test extracts every author surname ...'.\",\n   \"why_it_matters\": \"The doc states a whole-file guarantee that the self-test does not enforce. Current state is clean: an independent scan of every capitalised token in the doc prose (section B) finds no cited person or party name outside the list, so no real identifier is in the packets. The exposure is the next research edit that cites a study as 'Smithers (2019)' or names an author in prose, which would pass the self-test and any packet built from it would pass the scan. Synthetic-data safety depends on this guard, so it is a major and not a minor. It is not a blocker because nothing leaks today.\",\n   \"fix\": \"Either (a) require every proper-name token in the doc prose to be listed or on an explicit exemption list, failing on any unlisted capitalised token not in a short stop list; or (b) add author-year ('Name (2019)', 'Name, 2019') and prose-name shapes to the extractor. State the scope of the self-test in the doc rule text at :24-27.\",\n   \"acceptance_test\": \"Re-run artifacts/review-evidence/T-077-paralegal-r3-names.py: M2, M4 and M7 each exit 1 and name the surname; baseline self-test still exits 0; the independent scan (section B) still shows no uncovered person or party name.\"},\n  {\"severity\": \"minor\", \"title\": \"Title-case 'Fair Health' passes the capitalised-only matcher\",\n   \"evidence\": \"artifacts/review-evidence/T-077-paralegal-r3-names.out section E: 'Fair Health' -> []; 'FAIR Health' -> ['FAIR Health']; section F: case_planted_fairhealth_titlecase.txt exit=0. research/validate_library.py:72 (_CAP built from w and w.upper() only) and :155 (self-test variants (w, w.upper())). Doc :372 'Matching is case-insensitive'; :430 'FAIR Health  # capitalised only (organisation)'.\",\n   \"why_it_matters\": \"The doc says matching is case-insensitive and the term is meant to match when capitalised. Title case is the natural casing for an organisation name, so the guard misses the most likely form. The self-test has the same blind spot, so it reports ok. Risk is low (organisation, not a person or patient), but the guard does not do what the doc says.\",\n   \"fix\": \"Match title case as well as UPPER for capitalised-only terms (add w.title() to the variants at :72 and :155, or match case-insensitively with a word-boundary and a capital first letter).\",\n   \"acceptance_test\": \"Planting 'Fair Health' in a packet makes the validator exit 1 (section F row fails); the self-test planted-variant check includes w.title().\"},\n  {\"severity\": \"minor\", \"title\": \"Firm and organisation exemptions are implicit; 'Painter' is not listed while its slug is\",\n   \"evidence\": \"research/case-library-sources-v2.md:137 'painterfirm.com/medmal/...'; :426 'painterfirm' listed; :367-368 'every real person's name and every firm-website slug or organisation name cited in this file's sources'. Organisation names cited but not listed: Health Affairs (:255), Pediatrics and AHRQ (:186), PubMed, Legal500, Casemine, FindLaw (:136 and :283), texasworker (:189), natlawreview (:243). Probes: section E 'Painter Law Firm' -> []; section F case_planted_painter.txt exit=0.\",\n   \"why_it_matters\": \"Slugs are listed but the firm's own words are not, and the doc's rule text says every organisation name is covered. The judgment call is acceptable for synthetic-data safety: publishers, journals, agencies and website domains are not patient, provider or party identifiers, and a packet is unlikely to carry them as a person. Firm words are a different case, because 'Painter' is an ordinary surname the doc's own rule 2 (:27-28) bans as an invented name. A reader cannot tell which organisations are exempt or why.\",\n   \"fix\": \"Add 'Painter' as capitalised-only (like Hills, Flores and Bai). Rewrite :367-368 to name the exemption: publishers, journals, agencies and website domains are exempt because they are not patient, provider or party identifiers; firm and payer names are listed.\",\n   \"acceptance_test\": \"A packet with 'Painter Medical Group' fails the validator; the doc's denylist section states the organisation exemption in one sentence.\"}\n ],\n \"whats_right\": [\n  \"Every author surname the validator extracts (Airan-Javia, Anderson, Bai, Castro, ElGhrably, Fishbain, Flores, Fraser, Kantrowitz, Powell, Rodríguez-Vera, Steinkamp) and the opening-list names (Haygood, Brinjikji, Nakashima) are on DENYLIST_V2 and the doc block; my independent token scan found no uncited person or party name.\",\n  \"Deleting Fraser or Brinjikji from the list and doc block makes the self-test exit 1, and planted Fraser or Brinjikji packets make the real validator exit 1 (artifacts/review-evidence/T-077-paralegal-r3-names.out sections D and F).\",\n  \"The validator's list and the doc's denylist block stay in sync (the self-test fails on drift in either direction), and the validator docstring at :1-11 states the self-test's shapes accurately.\"],\n \"questions_for_chris\": [\n  \"Is 'Waddell' (the eponym in the cited Fishbain title, used in packets as 'Waddell 3/5') an acceptable exception to 'every real person's name' in :367? The validator allows it on purpose (ALLOWED_EPONYMS); I did not object to the choice, I am asking you to confirm it.\",\n  \"Should publisher, journal, agency and website names (Health Affairs, Pediatrics, AHRQ, PubMed, Legal500) be listed or exempt in writing? My recommendation is written exemption (F3).\"]}\n```\n"
}
````

### User / tool · 2026-11-02T03:57:30.252Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:57:39.668Z

**tool call — Bash**
````
{
 "command": "grep -n '\"Fraser\"\\|\"Vera\"\\|DENYLIST_V2 = \\|DENYLIST_V1 = \\|^\"\"\"\\|self-test checks\\|v2 doc names' research/validate_library.py; grep -n \"Casemine\\|casemine\\|findlaw\\|Legal500\\|legal500\\|natlawreview\\|PubMed\\|pubmed\\|texasworker\\|Hallapproved\\|hallapproved\\|statpearls\" research/case-library-sources-v2.md | cut -c1-90",
 "description": "Verify validator and doc line numbers cited in review"
}
````

### User / tool · 2026-11-02T03:57:39.757Z

**tool result**
````
2:"""Validate evals/library/* with evals/golden/check_golden.py (T-052) and scan packets for real identifiers (T-077).
17:"""
26:DENYLIST_V1 = ["Nichols", "Duke Linden", "Haygood", "Escabedo", "K & L", "K&L", "Auto Crushers", "Alexandria", "Puerto Rico",
29:# v2 sources (research/case-library-sources-v2.md, "Denylist additions" block). Keep the two lists in sync; --self-test checks.
30:DENYLIST_V2 = [
51:    "Fraser", "Brinjikji", "Nakashima", "Vera", "Rodríguez-Vera",
59:  https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html a
60:  https://www.casemine.com/commentary/us/expert-medical-evidence-mandated-for-causation
101:  https://hallapproved.com/tx/cases/appeals/2025/10659616/ (page fetched; summarized b
172:  https://www.statpearls.com/articlelibrary/viewarticle/31286/ (StatPearls overview; r
189:  ("espalda" for the area between the shoulder blades; "cane" vs "crutches") — https
204:  Electronic Medical Record", JAMA Network Open 5(9) (2022-09-01) — https://pubmed.n
243:  (2008) — https://natlawreview.com/article/new-study-finds-emergency-room-physician
283:  — https://www.legal500.com/intelligence/united-states/litigation-mediation-arbitra
301:  (1997), PMID 9455663 — https://pubmed.ncbi.nlm.nih.gov/9455663/ (abstract read via
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:57:46.523Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r3.md",
 "old_string": "Brinjikji, Nakashima, Fraser and Vera are now in `DENYLIST_V2` (validate_library.py:53-56 region) and in the doc block (case-library-sources-v2.md:420-424).",
 "new_string": "Brinjikji, Nakashima, Fraser and Vera are now in `DENYLIST_V2` (validate_library.py:51) and in the doc block (case-library-sources-v2.md:420-424)."
}
````

### User / tool · 2026-11-02T03:57:46.568Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-077-paralegal-r3.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:57:47.405Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r3.md",
 "old_string": "The doc's rule text, case-library-sources-v2.md:24-25 (\"Every real name in this file is on that denylist\") and :26-27 (\"--self-test extracts every author surname ...\"), reads",
 "new_string": "The doc's rule text, case-library-sources-v2.md:24-25 (\"Every real name in this file is on that denylist\") and :25-26 (\"--self-test extracts every author surname ...\"), reads"
}
````

### User / tool · 2026-11-02T03:57:47.456Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-077-paralegal-r3.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:57:48.398Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r3.md",
 "old_string": "Organisation names cited but not listed: Health Affairs (:255), Pediatrics and AHRQ (:186), PubMed, Legal500, Casemine, FindLaw (:136 and :283), texasworker (:189), natlawreview (:243).",
 "new_string": "Organisation names cited but not listed: Health Affairs (:255), Pediatrics and AHRQ (:186), PubMed (:204, :301), Legal500 (:283), Casemine and FindLaw (:59-60), texasworker (:189), natlawreview (:243)."
}
````

### User / tool · 2026-11-02T03:57:48.443Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-077-paralegal-r3.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:57:49.236Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r3.md",
 "old_string": "Doc rule: research/case-library-sources-v2.md:24-25 'Every real name in this file is on that denylist'; :26-27 '--self-test extracts every author surname ...'.\",",
 "new_string": "Doc rule: research/case-library-sources-v2.md:24-25 'Every real name in this file is on that denylist'; :25-26 '--self-test extracts every author surname ...'.\","
}
````

### User / tool · 2026-11-02T03:57:49.289Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-077-paralegal-r3.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:57:50.200Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r3.md",
 "old_string": "Organisation names cited but not listed: Health Affairs (:255), Pediatrics and AHRQ (:186), PubMed, Legal500, Casemine, FindLaw (:136 and :283), texasworker (:189), natlawreview (:243).",
 "new_string": "Organisation names cited but not listed: Health Affairs (:255), Pediatrics and AHRQ (:186), PubMed (:204, :301), Legal500 (:283), Casemine and FindLaw (:59-60), texasworker (:189), natlawreview (:243)."
}
````

### User / tool · 2026-11-02T03:57:50.247Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-077-paralegal-r3.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:57:50.870Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r3.md",
 "old_string": "the validator docstring at :1-11 states the self-test's shapes accurately.",
 "new_string": "the validator docstring at lines 2-16 states the self-test's shapes accurately."
}
````

### User / tool · 2026-11-02T03:57:50.919Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-077-paralegal-r3.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:57:57.291Z

**tool call — Bash**
````
{
 "command": "grep -n -o \"validate_library.py:53-56 region\\|:26-27\\|:136 and :283\\|:1-11\" reviews/T-077-paralegal-r3.md; ls -la reviews/T-077-paralegal-r3.md",
 "description": "Locate the four stale line references in the review file"
}
````

### User / tool · 2026-11-02T03:57:57.381Z

**tool result**
````
31:validate_library.py:53-56 region
35::26-27
65::26-27
75::136 and :283
83::1-11
-rw-r--r--@ 1 arsis  staff  16912 Nov  1 21:57 reviews/T-077-paralegal-r3.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:58:00.563Z

**tool call — Bash**
````
{
 "command": "python3 -c \"import json,re; t=open('reviews/T-077-paralegal-r3.md').read(); b=re.search(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S).group(1); d=json.loads(b); print(d['card'], d['persona'], d['model'], d['verdict'], [(f['severity']) for f in d['findings']], list(d['scores'].keys()))\"",
 "description": "Check the review JSON block parses and carries the verdict"
}
````

### User / tool · 2026-11-02T03:58:00.620Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:58:02.932Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-paralegal-r3-jsoncheck.py",
 "content": "#!/usr/bin/env python3\n\"\"\"Parse the fenced json block in reviews/T-077-paralegal-r3.md and print the fields the board validator reads.\"\"\"\nimport json\nimport pathlib\nimport re\n\npath = pathlib.Path(\"/Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r3.md\")\ntext = path.read_text()\nm = re.search(r\"```json\\n(.*?)\\n```\", text, re.S)\ndata = json.loads(m.group(1))\nprint(\"card:\", data[\"card\"])\nprint(\"persona:\", data[\"persona\"])\nprint(\"model:\", data[\"model\"])\nprint(\"verdict:\", data[\"verdict\"])\nprint(\"findings:\", [(f[\"severity\"], f[\"title\"][:60]) for f in data[\"findings\"]])\nsev = [f[\"severity\"] for f in data[\"findings\"]]\nexpected = \"fail\" if \"blocker\" in sev else \"changes\" if \"major\" in sev else \"pass\"\nprint(\"verdict rule expects:\", expected, \"| matches:\", expected == data[\"verdict\"])\n"
}
````

### User / tool · 2026-11-02T03:58:03.028Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-077-paralegal-r3-jsoncheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:58:03.384Z

**tool call — Bash**
````
{
 "command": "python3 artifacts/review-evidence/T-077-paralegal-r3-jsoncheck.py",
 "description": "Run JSON block check on the review file"
}
````

### User / tool · 2026-11-02T03:58:03.483Z

**tool result**
````
card: T-077
persona: paralegal-reviewer
model: claude-haiku-5-5
verdict: changes
findings: [('major', 'Self-test extracts names in three shapes only; author-year a'), ('minor', "Title-case 'Fair Health' passes the capitalised-only matcher"), ('minor', "Firm and organisation exemptions are implicit; 'Painter' is ")]
verdict rule expects: changes | matches: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:58:07.088Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md"
}
````

### User / tool · 2026-11-02T03:58:07.100Z

**tool result**
````
1	---
2	name: reviewer-tooling-quirks
3	description: Hooks that block reviewer shell commands in Zlayt PM (board-guard on sed -i, git-guard on python -c with backticks) and the workaround
4	metadata:
5	  type: feedback
6	---
7	
8	Don't edit review files with `sed -i` (board-guard blocks it), and don't run `python3 -c` with backticks or regex escapes (git-guard can't parse it). Use the Edit tool for review files, and put checks in a script under artifacts/review-evidence/ run with `.venv/bin/python`.
9	
10	**Why:** Both were blocked during the T-013 r2 review (2026-11-01). A script also leaves reproducible evidence the review can cite.
11	
12	**How to apply:** For every review, put JSON/verdict validation in artifacts/review-evidence/<card>-*-jsoncheck.py. Related: [[spec-review-patterns]].
13	
14	## T-077/T-078 r2 additions (2026-11-01)
15	- `grep -E` with long `.{0,120}` patterns over fetched HTML fails in ugrep ("exceeds complexity limits"). Strip tags and search in a python script under artifacts/review-evidence/.
16	- `timeout` is not installed on this macOS host; drop it and rely on urllib's timeout argument.
17	- A `mktemp` + `rmdir` combo inside a Bash call tripped board-guard. Keep Bash calls to one purpose.
18	- Fetched pages redirected to the session scratchpad were not blocked by the hook, but the persona rule says reviewers write only under reviews/, artifacts/review-evidence/ and memory. Write fetch dumps to artifacts/review-evidence/ and say so in the review.
19	- The NUCC and CMS PDFs download fine with urllib; write the PDF into review-evidence, run `pdftotext -layout`, then delete the PDF and text.
20	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:58:09.749Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md",
 "old_string": "- The NUCC and CMS PDFs download fine with urllib; write the PDF into review-evidence, run `pdftotext -layout`, then delete the PDF and text.\n",
 "new_string": "- The NUCC and CMS PDFs download fine with urllib; write the PDF into review-evidence, run `pdftotext -layout`, then delete the PDF and text.\n\n## T-077 r3 additions (2026-11-01)\n- `reviewer-write-guard` makes review files append-only: once `reviews/<card>-<persona>-rN.md` exists, Edit is refused (\"reviews are append-only\"). Proof-read the review (grep every line ref and quote) BEFORE the single Write; a stale ref cannot be fixed afterwards without a new file.\n- A bash `python3 -c` with `\\`\\`\\`` and `\\d` escapes was denied by git-guard (\"could not parse command safely (No escaped character)\"). Move any JSON parse into a Write-created script under artifacts/review-evidence/ and run it.\n"
}
````

### User / tool · 2026-11-02T03:58:09.861Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:58:13.916Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/library-review-patterns.md",
 "old_string": "- Denylist and self-test changes in this area: keep a planted-name test per new term (mutation: delete a term and confirm self-test fails).\n",
 "new_string": "- Denylist and self-test changes in this area: keep a planted-name test per new term (mutation: delete a term and confirm self-test fails).\n\n## T-077 r3 (commit 8d7548d): what held, what to re-check\n- Denylist now covers all 12 extracted author surnames and the opening list (Brinjikji, Nakashima); the round-2 major is closed for those shapes. Verdict changes (F1 major).\n- Self-test extraction is shape-bound: initials/et al, the \"cited\" paragraph list, and X v. Y captions only. Author-year (\"Smithers (2019)\"), comma-year and prose mentions pass silently. Mutate the doc text in memory (self_test(doc_text=...)) to check each shape; do not trust the doc's \"every real name\" sentence.\n- Capitalised-only terms match only the exact case or UPPER. Title-case \"Fair Health\" passes; the self-test variants never include title case. Probe every capitalised-only term in Title case as well.\n- Firm exemptions: slugs are listed, the firm's words (Painter) are not; publisher and agency names are not listed but the rule says \"organisation names\". Ask for a written exemption rather than a list.\n- Review files are append-only (reviewer-write-guard): any stale line ref must be checked before the one Write. T-077 r3 went out with five stale refs (validate_library.py:53-56 vs real :51; doc :26-27 vs :25-26; :1-11 vs 2-16; :136 vs :59-60). Recheck with grep -n on every ref.\n- Re-check on any later library change: run artifacts/review-evidence/T-077-paralegal-r3-names.py (sections A to F) and compare to its .out.\n"
}
````

### User / tool · 2026-11-02T03:58:14.007Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/library-review-patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:58:16.019Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T03:58:16.028Z

**tool result**
````
1	- [Spec review patterns](feedback_spec_review_patterns.md) — check absolute claims vs the doc's own example; grep every named category/R-ID/fixture
2	- [Golden-set recurring findings](golden-set-recurring-findings.md) — T-015: must/should levels, shared type+cite flags, export/§6 drift, dead checks via key drift (mutation-test)
3	- [Reviewer hook constraints](reviewer-hook-constraints.md) — board.py allowed verbs, python heredoc form, write-allowed dirs
4	- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; use Edit + scripts in review-evidence
5	- [Frontend review patterns](frontend-review-patterns.md) — T-043: mock vs harness coverage, keyboard focus yank, recurring minor gaps
6	- [Library review patterns](library-review-patterns.md) — T-052 minors; T-077 r2: denylist self-test checks captions only, prose names escape
7	- [Record-format review patterns](record-format-review-patterns.md) — T-078 r2: mutation-test the check script; visit-count fix creates a PT gap; lib14 specimen gaps
8	- [Manual entry / split review patterns](manual-entry-split-review-patterns.md) — T-056: AC ticked for absent UI label, split amounts not moving, override trace missing
9	- [T-068 dates-to-confirm patterns](t068-dates-to-confirm-patterns.md) — orphan confirm dead-ends, record listed twice, text-only AC test, commit vs worktree divergence
10	- [D-041 date-gate patterns](d041-date-gate-patterns.md) — T-076 r2 (f4ef2ea): stale DATE_AMBIGUOUS fixed; Edit/Change quote still enabled on undated row (T-060)
11	- [Reviewer API shape gotchas](reviewer-api-shape-gotchas.md) — item GET nests under "item", status "ready", record warnings in case.flags, audit before/after local-only
12	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:58:17.583Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [Library review patterns](library-review-patterns.md) — T-052 minors; T-077 r2: denylist self-test checks captions only, prose names escape",
 "new_string": "- [Library review patterns](library-review-patterns.md) — T-052 minors; T-077 r2/r3: self-test shape-bound (author-year, prose escape), title-case FAIR Health passes"
}
````

### User / tool · 2026-11-02T03:58:17.679Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:58:18.421Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; use Edit + scripts in review-evidence",
 "new_string": "- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; review files are append-only (proofread before the one Write)"
}
````

### User / tool · 2026-11-02T03:58:18.524Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:58:21.375Z

Verdict: changes. 0 blockers, 1 major (self-test misses author-year and prose-cited names), 2 minors (title-case "Fair Health" passes; "Painter" and the firm/organisation exemptions are implicit). Review at /Users/arsis/zlayt-pm-project/reviews/T-077-paralegal-r3.md, but five line refs in it are stale (validator :53-56 should be :51, doc :26-27 should be :25-26, docstring :1-11 should be :2-16, FindLaw/Casemine :136 should be :59-60, and a fifth ref), and the append-only guard blocks editing, so I did not bypass it.
