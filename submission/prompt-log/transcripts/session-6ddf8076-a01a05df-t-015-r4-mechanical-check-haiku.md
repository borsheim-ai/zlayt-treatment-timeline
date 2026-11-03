# Subagent: T-015 r4 mechanical check (haiku) (T-015 r4 mechanical check (haiku))

Source: `agent-a01a05dfb41f3ccd8.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:06:04.450Z

Working directory: /Users/arsis/zlayt-pm-project. Mechanical re-check of T-015 after commit 0c03c4f against reviews/T-015-paralegal-r3.md and reviews/T-015-legal-nurse-r3.md. Run and quote: `python3 evals/golden/check_golden.py`; grep evals/golden/sample.export.expected.txt for the accident-date bullet and confirm it quotes both "Date of accident per intake form: 2026-01-19" and record 1's "rear-ended" text; `grep -rn "self_report_spans\|patient_self_report\|patient_report" evals/golden | head`; grep the export for "Pending items" (must be absent) and "Items not reviewed: 0."; confirm spec/REQUIREMENTS.md §6 notes line equals the golden AI line (`grep -n "Items not reviewed" spec/REQUIREMENTS.md evals/golden/sample.export.expected.txt`). Pass if the r3 blocker and majors are resolved per output. Write reviews/T-015-paralegal-r4.md (D.2 JSON; model = what you run as). Reply ≤ 3 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:06.157Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T01:06:06.165Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:06.504Z

**tool call — Bash**
````
{
 "command": "python3 evals/golden/check_golden.py; echo \"EXIT=$?\"",
 "description": "Run golden eval check script"
}
````

### User / tool · 2026-11-02T01:06:06.618Z

**tool result**
````
golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:06.993Z

**tool call — Bash**
````
{
 "command": "git -C /Users/arsis/zlayt-pm-project log --oneline -3 2>/dev/null; ls reviews/ | grep T-015; ls evals/golden/",
 "description": "Check recent commits and golden directory listing"
}
````

### User / tool · 2026-11-02T01:06:07.097Z

**tool result**
````
65537a4 fix(harness): debt entry no longer masks later fails; board-guard catches move-done in any arg order; M0 r3 closures
0c03c4f fix(evals): golden r3 fixes - both-sides accident conflict, self_report_spans key, R-EX-4 AI line, tighter flag matching
4cc0f81 docs(spec): golden is authority for exports; section 8 owners updated
T-015-legal-nurse-r2.md
T-015-legal-nurse-r3.md
T-015-legal-nurse.md
T-015-paralegal-r2.md
T-015-paralegal-r3.md
T-015-paralegal.md
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
sample.expected.json
sample.export.expected.txt
sample.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:07.197Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-015-paralegal-r3.md"
}
````

### User / tool · 2026-11-02T01:06:07.205Z

**tool result**
````
1	# T-015 round 3 (final): paralegal-reviewer (Maria Delgado lens)
2	
3	**Verdict: fail** (1 blocker, 2 majors, 3 minors).
4	
5	The r2 blocker is fixed. Flag matching now requires overlapping evidence plus one-to-one assignment, so a single record-7 "New onset pain" causation flag scores K4 only and causation recall is 4/5. That was my r2 acceptance test, and it passes in both the checker's fixtures and my own probe. The K5 intake-date line is in the causation bullet. Record 1 is listed under "flagged language quoted in the letter". The bills-to-request line matches the R-EX-4 example exactly. The letter total line is D-019 exact. All 9 letter quotes are verbatim from the record they are cited to, and every export summary meets its required_terms on the summary alone.
6	
7	Three problems remain.
8	- **Blocker.** The byte-exact export golden still does not quote the EMS side of the accident-date conflict. REQUIREMENTS §6 block 2 and R-FL-2 require both sides quoted. REQUIREMENTS §8 row 1 assigned this re-extraction to T-015 r3, and its own grep still fails. A product built to the spec fails ship bar 8. A product that drops the EMS quote passes.
9	- **Major.** The self-report spans live under the JSON key `spans`, but README and check_golden.py read `self_report_spans`. The D-022 span checks never run. Mutation proof: an objective, wrong-kind span passes `check_golden.py`.
10	- **Major.** The notes block has an AI-assistance line that differs from R-EX-4(1), a stale `Pending items: 0.` line, and a stray period. README says the golden is the authority, while REQUIREMENTS §8 says the golden must match §6. The two disagree byte for byte.
11	
12	Commands run (exact output):
13	- `python3 evals/golden/check_golden.py` → `golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered`, EXIT=0
14	- `git status --porcelain evals/golden/` → (empty); `git log -1 --format=%h -- evals/golden` → `f8c1948`
15	- `.venv/bin/python -I artifacts/review-evidence/T-015-r2-paralegal-probe.py` → `T-015-r3-paralegal-rerun-of-r2-probe.out.txt`. Sections 1-7 ran. Section 8 raised `KeyError: 'display'`, which is expected because totals were split into letter_line/ui_line/notes_lines. Section 4 still simulates the old type+cite rule, so it is superseded by probe A below.
16	- `.venv/bin/python -I artifacts/review-evidence/T-015-r2-nurse-probe.py` → `T-015-r3-rerun-of-r2-nurse-probe.out.txt`: `COUNTS [(('r1','OK'),36), (('r1','n/a(hit)'),2), (('r2','FALSEPOS'),2), (('r2','LEAK'),3), (('r2','OK'),45)]`
17	- `.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-probe.py` → `.out.txt`. This pulls the reference matcher out of check_golden.py with ast and covers: K4/K5 matching, span keys, summary-only checks on the export, the conflict bullet, an independent rebuild of the flagged-language and bills sections, and the nurse r2 items.
18	- `.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-s6diff.py` → `notes == s6 block2: False` (3 differing lines; `letter == s6 block1: True`)
19	- `.venv/bin/python -I artifacts/review-evidence/T-015-r3-paralegal-mutation.py <scratch copy>` → baseline exit=0; objective span under `spans` exit=0 (not caught); same span under `self_report_spans` exit=1 (caught)
20	- REQUIREMENTS §8 greps: `grep -n "Pending items: 0" evals/golden/sample.export.expected.txt` → `52:Pending items: 0.` (row 1 expects no match). `grep -n "patient_self_report\|summary+excerpt" ...README.md ...sample.expected.json` → `sample.expected.json:638: "subtype": "patient_self_report"` (row 4 expects no match). `grep -n "Known spec mismatches" README.md` → no match (row 3 OK).
21	
22	```json
23	{"card": "T-015", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
24	 "scope": "round 3 (final, s7.4), commit f8c1948 (git diff 3c5eb7c..f8c1948 -- evals/golden): README.md, sample.expected.json, sample.export.expected.txt, case_01..09 .expected.json, hallucinations*.jsonl, check_golden.py; refs spec/REQUIREMENTS.md s6, s8 rows 1/3/4, R-FL-2, R-FL-4, R-FL-7, R-EX-4, R-EX-6, R-EX-8; memory/ORCHESTRATOR_DECISIONS.md D-019, D-021, D-022 (binding). No app (pre-code eval data); sample case evals/golden/sample.txt",
25	 "exercised": [
26	  "python3 tools/board.py show T-015 (AC 1-4, r3 handoff)",
27	  "python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered' EXIT=0",
28	  "git status --porcelain evals/golden/ (empty); git log -1 --format=%h -- evals/golden -> f8c1948; git diff 3c5eb7c..f8c1948 -- README.md sample.export.expected.txt (read in full)",
29	  "re-ran r2 paralegal probe against f8c1948 -> T-015-r3-paralegal-rerun-of-r2-probe.out.txt (s1-s7 ran; s8 KeyError 'display' because totals were renamed; s4 old-rule simulation superseded)",
30	  "re-ran r2 nurse probe against f8c1948 -> T-015-r3-rerun-of-r2-nurse-probe.out.txt (r1 36 OK; r2 45 OK, 3 LEAK, 2 FALSEPOS)",
31	  "T-015-r3-paralegal-probe.py: reference matcher flag_matches/assign extracted from check_golden.py via ast, 11 K4/K5/C1 fixtures; span-key inventory across all 10 expected.json; export summaries vs required_terms and span attribution on the summary alone; conflict-bullet / AI-line checks; independent rebuild of R-EX-4(4) flagged-language and R-EX-4(8) bills from sample.expected.json; per-record quote verification of all 9 letter quotes; nurse r2 items",
32	  "T-015-r3-paralegal-s6diff.py: byte diff of golden notes block vs REQUIREMENTS s6 block 2",
33	  "T-015-r3-paralegal-mutation.py on a scratchpad copy of evals/golden: objective span under 'spans' vs 'self_report_spans'",
34	  "REQUIREMENTS s8 reconciliation greps for rows 1, 3, 4 (literal)",
35	  "compared sample.export.expected.txt line by line with the 9 records in sample.txt"
36	 ],
37	 "verdict": "fail",
38	 "scores": {"verify_quickly": 4, "arithmetic_and_dates": 5, "appendix_c_fidelity": 4, "flag_levels_realism": 5, "adjuster_attack_coverage": 4, "must_not_strength": 4, "export_golden_consistency": 2, "synthetic_labeling": 5},
39	 "findings": [
40	  {"severity": "blocker", "title": "Export golden's accident-date conflict bullet quotes only the intake-form side. Record 1's 'rear-ended' sentence is not quoted, the bullet does not say the tool does not choose between the dates, and the byte-exact golden makes this weaker form the required output.",
41	   "evidence": "sample.export.expected.txt:56 '- Conflict, accident date: record 1 (Austin EMS run report, January 9, 2026) and record 2 (Central ER discharge summary, January 9, 2026) show treatment on that date; record 7 (...): \"Date of accident per intake form: 2026-01-19.\"' REQUIREMENTS s6 block 2 has: 'record 7 (...): \"Date of accident per intake form: 2026-01-19.\" Record 1 (Austin EMS run report, January 9, 2026): \"41M restrained driver, rear-ended at approx. 35 mph.\" Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.' (T-015-r3-paralegal-s6diff.out.txt). R-FL-2: 'shown as a conflict and not merged, with both sides quoted (R-EX-4)'. REQUIREMENTS s8 row 1 assigns 'the accident-date conflict line still describes records 1 and 2 in tool wording instead of quoting both sides' to T-015 r3 (qa). check_golden.py:547 encodes the weaker form: '# accident-date conflict: the intake-form line is quoted; the EMS/ER records are cited by number'. Probe D: quotes record 1 'rear-ended' sentence: False; says tool does not choose: False. sample.expected.json C1 lists (1, excerpt, 'rear-ended at approx. 35 mph') as evidence.",
42	   "why_it_matters": "Checklist 7 says the conflict is flagged with both excerpts. When the adjuster raises the 01-19 intake date, my attorney needs the EMS sentence that fixes the collision on 01-09 next to it, in my notes, quoted. 'Show treatment on that date' is tool wording, not the record. R-EX-6 makes this file the byte-exact E2E reference, so a product that follows R-FL-2 fails ship bar 8, and one that drops the EMS quote passes. The eval rewards the weaker conflict note.",
43	   "fix": "Re-extract the INTERNAL_NOTES_TEXT block from REQUIREMENTS s6 block 2, as s8 row 1 directs. Change check_golden.py:547 so the C1 bullet must contain every C1 field-'excerpt' evidence item verbatim (record 7 intake line and record 1 'rear-ended at approx. 35 mph'), the phrase 'does not choose', and no computed delay.",
44	   "acceptance_test": "T-015-r3-paralegal-s6diff.py prints 'notes == s6 block2: True'. Deleting the record-1 quote from the C1 bullet in a scratch copy makes check_golden.py exit 1."},
45	  {"severity": "major", "title": "Self-report spans are stored under 'spans', but README and check_golden.py read 'self_report_spans'. The D-022 span checks and the export attribution check never run.",
46	   "evidence": "README.md:40 schema key 'self_report_spans'. check_golden.py:195 and :455 'e.get(\"self_report_spans\", [])'. The JSON uses '\"spans\"' at sample.expected.json:109, :272; case_01_date_formats.expected.json:175; case_06_subtle_pre_existing.expected.json:74, :120, :157. Probe B: 'entries with self_report_spans items = 0; with spans items = 6'. Mutation (T-015-r3-paralegal-mutation.out.txt): sample E1 span set to 'Alert and oriented' with source_kind 'WRONG' under 'spans' -> exit=0 'golden OK'. The same mutation under 'self_report_spans' -> exit=1 'span contains objective/assessment content: Alert and oriented'. Probe B: case_01 E8 ('Patient reports no new symptoms'), case_06 E3 ('History: occasional stiffness ...') and case_06 E5 ('Patient notes the old shoulder problem is acting up again') have attribution_also_in_required_terms=False, so their attribution is enforced nowhere. The handoff says 'self_report_spans per sentence with attribution_any ... Verified'.",
47	   "why_it_matters": "Checklist 23 says patient self-reports stay attributed, and D-022 (binding) moved that check onto spans. A runner built from the README schema reads an empty list and scores the self-report rule as vacuously passed. A tool that turns 'Patient notes the old shoulder problem is acting up again' into a provider finding would score full marks. The validator's claim to cover D-022 is false, though the span data itself is correct (all 6 spans are subjective sentences, probe B objective_hit=False).",
48	   "fix": "Rename 'spans' to 'self_report_spans' in all six entries (or rename README and checker, but make all three agree). Have check_golden.py fail on any unknown entry key, so a future rename can't silently disable a check.",
49	   "acceptance_test": "T-015-r3-paralegal-mutation.py's first mutation (objective span under the key the JSON uses) makes check_golden.py exit 1. A key inventory finds 6 'self_report_spans' items and 0 'spans'."},
50	  {"severity": "major", "title": "Notes block still differs from REQUIREMENTS s6 block 2: the AI-assistance line is not the R-EX-4(1) fixed text, a stale 'Pending items: 0.' line remains, and the K5 line has a stray period. README and REQUIREMENTS each name themselves the authority.",
51	   "evidence": "sample.export.expected.txt:51 'AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' and :52 'Pending items: 0.' R-EX-4(1) fixed text: 'This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.' :59 ends '2026-01-19.\".' while s6 ends '2026-01-19.\"'. s8 row 1 check: `grep -n \"Pending items: 0\" evals/golden/sample.export.expected.txt` -> '52:Pending items: 0.' (expects no match). README.md:99 'now maintained here'; README.md:152 'These golden files are the authority on expected outputs where REQUIREMENTS lags'. REQUIREMENTS s8: 'evals/golden/ (qa, T-015 round 3)' with row 1 'section 6 block 2 is the text to re-extract'.",
52	   "why_it_matters": "R-EX-6 makes this a byte-for-byte E2E target. A product that implements R-EX-4(1) word for word fails it. 'Every item was reviewed by the paralegal' also claims more than the product tracks: R-EX-4(1) scopes the claim to the treatment section and states the unreviewed count, which is the number I check before export (checklist 17). With two documents each claiming authority and disagreeing, the implementer has to guess.",
53	   "fix": "Re-extract block 2 from s6 together with the blocker fix. Remove the 'authority where REQUIREMENTS lags' sentence, or narrow it to items s8 actually lists as golden-owned. Have check_golden.py compare the notes block to s6 block 2 the way the r2 probe does.",
54	   "acceptance_test": "grep -n 'Pending items: 0' evals/golden/sample.export.expected.txt -> no match. check_golden.py fails when the golden notes block differs from REQUIREMENTS s6 block 2."},
55	  {"severity": "minor", "title": "Reference matcher's either-way substring overlap still lets broad evidence earn both K4 and K5, and lets a one-word fragment earn K4",
56	   "evidence": "Probe A (assign/flag_matches taken from check_golden.py): 'TWO flags both quoting whole record 7 (neither about intake date): got [K4, K5]'; 'K4 sentence + a second flag quoting whole record 7: got [K4, K5]'; '1-word fragment pain on record 7: got [K4]'. check_golden.py:94-96 overlap() = 'na in nb or nb in na'.",
57	   "why_it_matters": "The r2 failure mode is closed (one 'New onset' flag = K4 only). But a tool that emits two record-7 causation flags quoting the whole note, neither about the intake date, still gets 5/5 causation recall. The intake line is at least visible inside the quoted evidence, which is why this is minor.",
58	   "fix": "Before assignment, collapse candidates with identical (type, evidence) into one. Require the candidate excerpt to contain the golden excerpt, or to cover at least 50% of its normalized length, rather than allowing any substring either way.",
59	   "acceptance_test": "New check_golden fixtures: two identical whole-record-7 causation candidates -> {K4} or {K5}, not both. Candidate 'pain' -> {}."},
60	  {"severity": "minor", "title": "K3 flag still carries subtype 'patient_self_report' and no source_kind 'patient_report' (R-FL-7); REQUIREMENTS s8 row 4 grep still matches",
61	   "evidence": "sample.expected.json:638 '\"subtype\": \"patient_self_report\"'. Probe output for K3: 'source_kind=None'. R-FL-7: 'Sample record 9 flag has source_kind == \"patient_report\"'. s8 row 4 check: `grep -n \"patient_self_report\\|summary+excerpt\" README.md sample.expected.json` (expects no match) -> 1 match.",
62	   "why_it_matters": "The runner can't take R-FL-7's assertion from the golden, and the s8 check can't close.",
63	   "fix": "Add 'source_kind': 'patient_report' to K3, and rename the subtype (e.g. 'patient_reported_onset').",
64	   "acceptance_test": "The s8 row 4 grep returns nothing; K3.source_kind == 'patient_report'."},
65	  {"severity": "minor", "title": "M2 good_examples present tool commentary on causation ('no physician causation opinion is stated') as acceptable summary wording",
66	   "evidence": "sample.expected.json:812-813 good_examples 'Symptoms began after the January collision per patient report; no physician causation opinion is stated.' and 'Patient states symptoms began after the collision; no physician states they are due to the collision.' The regex applies to tool-authored text including letter summaries (README 'must_not' regex scope).",
67	   "why_it_matters": "In my treatment section, a tool sentence saying no doctor supports causation is a gift to the adjuster and flag-like content that R-EX-1 keeps out of the letter. It belongs in internal notes if anywhere. Golden good examples read as house style.",
68	   "fix": "Replace both with record-words examples (e.g. 'Per patient, symptoms began after the January collision.'). Add a letter-surface must_not for '\\bno (physician|doctor|provider)\\b.{0,40}\\b(states|opinion)'.",
69	   "acceptance_test": "No M2 good_example contains 'no physician'. The new must_not fires on both strings and not on the four record-words good examples."}
70	 ],
71	 "whats_right": [
72	  "K4/K5 are now separately enforceable: the reference matcher plus fixtures give 'New onset' alone K4 only (recall 4/5), and the K5 intake line sits in its own causation bullet.",
73	  "The letter block is clean demand text: 9 verbatim quotes each verified against its own record, US long dates, header labels as written, two charges, and 'Billed charges stated in these records: $8,390.00' with nothing after it (D-019).",
74	  "check_golden.py rebuilds the flagged-language and bills-to-request sections from the JSON and the R-EX-4 rules. My independent rebuild agrees, and the bills line equals the R-EX-4 example exactly."
75	 ],
76	 "questions_for_chris": [
77	  "When README (golden is the authority) and REQUIREMENTS s8 (golden must match s6) disagree on the export notes block, which file wins for the M1 byte-exact test?"
78	 ]}
79	```
80	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:07.402Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-015-legal-nurse-r3.md"
}
````

### User / tool · 2026-11-02T01:06:07.409Z

**tool result**
````
1	# T-015 Eval golden set, round 3 (final): legal-nurse checklist
2	
3	**Scope note:** the **paralegal-reviewer** agent (Opus 5.5) wrote this review at the orchestrator's request (D.6 brief, round 3). It is judged strictly against the legal-nurse r2 findings in `reviews/T-015-legal-nurse-r2.md`, not against the paralegal checklist. Clinical judgment beyond those findings is outside this agent's lens.
4	
5	**Verdict: changes** (0 blockers, 1 major, 3 minors).
6	
7	| r2 finding | r3 status | Evidence |
8	|---|---|---|
9	| M1 required_terms on summary+excerpt | **Fixed** | README.md:72 'a **summary** that by itself satisfies every `required_terms` item'. The nurse probe's 4 omission summaries (E1/E2/E8/E9) give `pass_on_summary_only=False`, so they now fail. E2/E8/E9 carry any-of qualifier alternatives. All 9 export summaries pass on the summary alone (probe C). check_golden.py:189-193 grounds every term in the record. |
10	| M2 patient-attributed causation allowed | **Fixed in substance** | 'Patient states her neck pain is due to the collision.' moved to bad_examples (sample.expected.json:806). M10 bad_examples include 'Patient states the collision caused his symptoms.' H35-H37 `temporal_to_causal` were added and REQ_CAT requires the category. Residual (minor): the literal r2 acceptance grep still finds a good_example with 'due to the collision' (:813). |
11	| M3 source_kind on whole mixed entries | **Data fixed, checks dead** | Entry-level source_kind is gone. 6 per-sentence spans use `patient_report`, and all are subjective (probe B objective_hit=False). But they are stored under `spans` while README and check_golden.py read `self_report_spans`, so the r2 acceptance test (the checker asserts span verbatim and no objective content) never runs. A mutation passes. K3 flag lacks R-FL-7 `source_kind`. |
12	| minor: regex leaks (30 of 50) | **27 of 30 closed** | Re-run: `('r2','LEAK'),3`. 'Diagnosed with cervical strain and concussion; CT head negative.' is now caught by summary-only required_terms (D-022). Still leaking: 'Findings may represent degenerative disc disease.' and 'Cervical disc disease at C5-C6.' |
13	| minor: controls S08/S10 | **Fixed** | S08 'The patient has seen a chiropractor ...' (no sex); S10 'pain radiating to the right arm'; check_golden.py:596 rejects invented pronouns |
14	| minor: missing judge items | **Fixed** | H38/H39 approximation_dropped, H40 abbreviation_misexpanded ('PT' -> 'prothrombin time'), SE5 kind judge_masked 'Visit 8: pain 8/10, improving.' -> needs_review |
15	| nit: case_01 'fracture' | **Fixed** | case_01 E1 required_terms ['ankle', 'negative for fracture'] |
16	
17	Commands run: `python3 evals/golden/check_golden.py` → `golden OK: ... 57 must_nots ..., 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase) ...` EXIT=0. `.venv/bin/python -I artifacts/review-evidence/T-015-r2-nurse-probe.py` → `T-015-r3-rerun-of-r2-nurse-probe.out.txt`. `T-015-r3-paralegal-probe.py` (sections B, C, F) and `T-015-r3-paralegal-mutation.py` on a scratch copy.
18	
19	```json
20	{"card": "T-015", "persona": "legal-nurse-reviewer", "model": "claude-opus-5-5",
21	 "scope": "round 3 (final), commit f8c1948 (git diff 3c5eb7c..f8c1948 -- evals/golden), judged strictly against reviews/T-015-legal-nurse-r2.md findings; written by the paralegal-reviewer agent against the legal-nurse checklist at orchestrator request. Files: README.md, sample.expected.json, case_01/06/08 expected.json, hallucinations.jsonl (40), hallucinations_controls.jsonl (10), sample.export.expected.txt summaries, check_golden.py; decisions D-021, D-022; spec R-FL-7, R-TL-10. No app (pre-code card).",
22	 "exercised": [
23	  "python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered' EXIT=0",
24	  ".venv/bin/python -I artifacts/review-evidence/T-015-r2-nurse-probe.py against f8c1948 -> T-015-r3-rerun-of-r2-nurse-probe.out.txt: COUNTS r1 OK 36, n/a 2; r2 OK 45, LEAK 3, FALSEPOS 2; omission probe pass_on_summary_only=False for E1/E2/E8/E9",
25	  "T-015-r3-paralegal-probe.py section B (span key inventory, objective-content regex on each span), C (export summaries vs required_terms and span attribution, summary alone), F (M2 examples, hallucination categories, S08/S10, M10, seeded edits, case_01 E1)",
26	  "T-015-r3-paralegal-mutation.py on a scratchpad copy: objective span under 'spans' -> exit 0; under 'self_report_spans' -> exit 1",
27	  "read sample.expected.json M2 bad/good examples (:795-815) and K3 (:638); README.md:40 and :72"
28	 ],
29	 "verdict": "changes",
30	 "scores": {"clinical_fidelity_of_reference_wording": 4, "appendix_c_must_not_check_reliability": 4, "hallucination_set_genuineness": 5, "hallucination_failure_mode_coverage": 5, "controls_faithfulness": 5, "objective_vs_subjective_coverage": 3, "summary_omission_measurement": 4},
31	 "findings": [
32	  {"severity": "major", "title": "r2 M3 acceptance test still fails: per-sentence self-report spans are correct but sit under key 'spans', so check_golden.py never validates them and a runner built from the README never scores them",
33	   "evidence": "README.md:40 and check_golden.py:195, :455 read 'self_report_spans'; the JSON uses '\"spans\"' (sample.expected.json:109, :272; case_01_date_formats.expected.json:175; case_06_subtle_pre_existing.expected.json:74, :120, :157). Probe B: 'self_report_spans items = 0; spans items = 6'. Mutation: sample E1 span 'Alert and oriented', source_kind 'WRONG', under 'spans' -> check_golden exit=0. Under 'self_report_spans' -> exit=1 'span contains objective/assessment content'. case_01 E8, case_06 E3 and case_06 E5 attribution appear in no required_terms (probe B attribution_also_in_required_terms=False).",
34	   "why_it_matters": "The r2 point was that the subjective/objective split must be encoded exactly and checked. The encoding is now right, but the check that would catch a future regression (an exam finding tagged as patient report) is dead. The eval also can't fail a summary that states 'History: occasional stiffness at baseline' or 'old shoulder problem is acting up again' as the provider's finding.",
35	   "fix": "Rename 'spans' to 'self_report_spans' in the six entries (or align README and checker the other way). Make check_golden.py reject unknown entry keys.",
36	   "acceptance_test": "The objective-span mutation under the JSON's key makes check_golden.py exit 1. A summary for case_06 E5 without 'patient notes/reports/states/per patient' is not found."},
37	  {"severity": "minor", "title": "K3 flag has no source_kind 'patient_report' (R-FL-7 value name) and keeps subtype 'patient_self_report'",
38	   "evidence": "sample.expected.json:638 '\"subtype\": \"patient_self_report\"'; probe: K3 source_kind=None. R-FL-7: 'Sample record 9 flag has source_kind == \"patient_report\"'. The r2 M3 fix asked to 'Use R-FL-7's value name'.",
39	   "why_it_matters": "The one flag that rests on the patient's own statement is the one R-FL-7 asserts on. Without the field, the runner can't check that the flag is never presented as a physician's opinion.",
40	   "fix": "Add 'source_kind': 'patient_report' to K3 and rename the subtype.",
41	   "acceptance_test": "K3.source_kind == 'patient_report'; grep 'patient_self_report' evals/golden/ returns nothing."},
42	  {"severity": "minor", "title": "r2 M2 literal acceptance grep still matches a good_example, and two M2 good_examples are tool commentary on causation rather than the record's words",
43	   "evidence": "`grep -n 'due to the collision' evals/golden/sample.expected.json` -> :806 (bad_example, correct) and :813 good_example 'Patient states symptoms began after the collision; no physician states they are due to the collision.' :812 good_example '... per patient report; no physician causation opinion is stated.'",
44	   "why_it_matters": "The substance of r2 M2 is fixed. But a good example that comments on what no physician said is a judgment about the record set, not a faithful summary. It also drops 'January' from the record's 'January collision'.",
45	   "fix": "Replace both with record-words examples, e.g. 'Per patient, symptoms began after the January collision.'",
46	   "acceptance_test": "No M2 good_example contains 'due to' or 'no physician'."},
47	  {"severity": "minor", "title": "Two regex-floor leaks from r2 remain: 'degenerative disc disease' under a hedge, and 'disc disease' without 'degenerative'",
48	   "evidence": "T-015-r3-rerun-of-r2-nurse-probe.out.txt: 'r2 V LEAK M3 M8 Findings may represent degenerative disc disease. -> {}' and 'r2 V LEAK M1 M8 M3 Cervical disc disease at C5-C6. -> {}'. (The third leak, the dropped LOC qualifier, is now caught by summary-only required_terms.)",
49	   "why_it_matters": "The record says 'degenerative change'. 'Degenerative disc disease' and 'disc disease' are diagnoses the radiologist did not make, and a hedge does not make a new diagnosis faithful. Judge #1 is the only backstop.",
50	   "fix": "Add a sample regex for '\\bdisc disease\\b|\\bDDD\\b' with no hedge exemption (the record never uses the term).",
51	   "acceptance_test": "Both probe strings become bad_examples that fire; 'Findings may represent degenerative change' stays a good example."}
52	 ],
53	 "whats_right": [
54	  "D-022 is implemented for entries: required_terms are summary-only with any-of qualifier alternatives, so dropping 'without loss of consciousness', the MRI hedge or 'patient states' now fails, and all 9 export summaries pass.",
55	  "The hallucination set (40) and controls (10) now cover temporal-to-causal, approximation dropped, abbreviation mis-expansion and the masked pain-score swap (SE5), and the controls no longer invent sex or drop 'radiating'.",
56	  "Every self-report span is a verbatim subjective sentence (C/O, patient states, denies, history, patient notes), and none carries an exam finding or assessment."
57	 ],
58	 "questions_for_chris": []}
59	```
60	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:12.127Z

**tool call — Bash**
````
{
 "command": "echo \"--- accident-date bullet (export) ---\" && grep -n \"Conflict, accident date\" evals/golden/sample.export.expected.txt; echo \"--- 'rear-ended' in export ---\"; grep -n \"rear-ended\" evals/golden/sample.export.expected.txt; echo \"rc=$?\"; echo \"--- 'does not choose' in export ---\"; grep -n \"does not choose\" evals/golden/sample.export.expected.txt; echo \"rc=$?\"; echo \"--- intake quote in export ---\"; grep -n \"Date of accident per intake form: 2026-01-19\" evals/golden/sample.export.expected.txt; echo \"--- record 1 source text in sample.txt ---\"; grep -n \"rear-ended\" evals/golden/sample.txt; grep -n \"Date of accident per intake form\" evals/golden/sample.txt",
 "description": "Grep export for accident-date bullet and record sources"
}
````

### User / tool · 2026-11-02T01:06:12.244Z

**tool result**
````
--- accident-date bullet (export) ---
55:- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
64:- Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Conflict, accident date.
--- 'rear-ended' in export ---
5:Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
6:Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
55:- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
64:- Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Conflict, accident date.
rc=0
--- 'does not choose' in export ---
55:- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
rc=0
--- intake quote in export ---
55:- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
58:- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
--- record 1 source text in sample.txt ---
6:Excerpt: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
36:Excerpt: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:12.985Z

**tool call — Bash**
````
{
 "command": "grep -rn \"self_report_spans\\|patient_self_report\\|patient_report\" evals/golden | head; echo \"--- spans key occurrences ---\"; grep -rn '\"spans\"' evals/golden | head; echo \"--- check_golden refs ---\"; grep -n \"self_report_spans\\|\\\"spans\\\"\" evals/golden/check_golden.py evals/golden/README.md",
 "description": "Grep golden dir for self-report span keys"
}
````

### User / tool · 2026-11-02T01:06:13.081Z

**tool result**
````
evals/golden/check_golden.py:87:    if sp.get("source_kind") != "patient_report":
evals/golden/check_golden.py:88:        out.append("source_kind must be 'patient_report' (D-022)")
evals/golden/check_golden.py:156:              "self_report_spans", "note", "needs_review", "date_candidates"}
evals/golden/check_golden.py:160:        not span_problems(dict(excerpt="Tenderness over the anterior shoulder", source_kind="patient_report", attribution_any=["x"])) or \
evals/golden/check_golden.py:161:        span_problems(dict(excerpt="C/O neck pain", source_kind="patient_report", attribution_any=["C/O"])):
evals/golden/check_golden.py:225:        for sp in e.get("self_report_spans", []):
evals/golden/check_golden.py:486:        for sp in e.get("self_report_spans", []):
evals/golden/case_06_subtle_pre_existing.expected.json:74:      "self_report_spans": [
evals/golden/case_06_subtle_pre_existing.expected.json:77:          "source_kind": "patient_report",
evals/golden/case_06_subtle_pre_existing.expected.json:120:      "self_report_spans": [
--- spans key occurrences ---
--- check_golden refs ---
evals/golden/README.md:40:      "self_report_spans": [{"excerpt": "verbatim subjective sentence", "source_kind": "patient_report",
evals/golden/README.md:72:* **Entries.** Found when the product emits an entry that covers `record_nos`, has the same `date` (or both ambiguous), `provider` equal to the record's header label after whitespace normalization (code copies it; merged duplicates take the lowest-numbered record's label), an excerpt containing every `must_contain_excerpt` item, and a **summary** that by itself satisfies every `required_terms` item (case-insensitive, whitespace-collapsed). A summary that drops a qualifier its excerpt carries (hedge, negation such as "without loss of consciousness", laterality, "approx.", self-report marker) is `needs_review` with reason `SUMMARY_DROPS_QUALIFIER` (D-022) and counts as not found. **Self-report:** for each `self_report_spans` item the summary must contain ≥ 1 `attribution_any` word, else the same reason. Spans are subjective sentences only (no findings, assessments or measurements). Recall pooled across cases ≥ 95%. More entries than `expected_entry_count` = dedupe failure.
evals/golden/check_golden.py:156:              "self_report_spans", "note", "needs_review", "date_candidates"}
evals/golden/check_golden.py:225:        for sp in e.get("self_report_spans", []):
evals/golden/check_golden.py:486:        for sp in e.get("self_report_spans", []):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:14.149Z

**tool call — Bash**
````
{
 "command": "echo \"--- Pending items (must be absent) ---\"; grep -n \"Pending items\" evals/golden/sample.export.expected.txt; echo \"rc=$?\"; echo \"--- Items not reviewed: 0. ---\"; grep -n \"Items not reviewed: 0\\.\" evals/golden/sample.export.expected.txt; echo \"rc=$?\"; echo \"--- Items not reviewed in export and REQUIREMENTS ---\"; grep -n \"Items not reviewed\" spec/REQUIREMENTS.md evals/golden/sample.export.expected.txt; echo \"--- AI line in export ---\"; grep -n \"AI assistance\" evals/golden/sample.export.expected.txt spec/REQUIREMENTS.md",
 "description": "Check export notes block and REQUIREMENTS notes line"
}
````

### User / tool · 2026-11-02T01:06:14.257Z

**tool result**
````
--- Pending items (must be absent) ---
rc=1
--- Items not reviewed: 0. ---
51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
rc=0
--- Items not reviewed in export and REQUIREMENTS ---
evals/golden/sample.export.expected.txt:51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
spec/REQUIREMENTS.md:273:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
--- AI line in export ---
spec/REQUIREMENTS.md:119:| R-EX-1 | **Treatment section (paste into letter)** contains accepted entries and accepted `charge` amounts only. It holds no tool-authored flag content: no flag note, type label, title, explanation, day count, count line or AI-assistance line. Record words appear only inside an accepted entry's excerpt or summary. | E2E: accept all 9 entries, both charges and all flags, add a reviewer note to the gap flag. Assert `letter_text` contains none of: the reviewer note text, "REVIEWER NOTE", any flag type label, any flag title or explanation string produced from `sample.expected.json`'s flags, "73 days", "AI assistance", or any count line. UT: every line of `letter_text` is a fixed heading, a date + provider heading, an entry summary, a `Source` line whose quote is a substring of the accepted excerpt, an amount line or the total line; the letter builder takes no flags argument. Set equality: with a chosen subset accepted, the item IDs in `letter_text` equal that subset. | E2E + UT |
spec/REQUIREMENTS.md:122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export." followed by "Pending items: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first appearance in the chronology, omitting any provider with an accepted charge, with " (itemized ledger)" appended when the provider has a non-dismissed rate. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 1, 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (entry 1 because the accident-date conflict cites its "rear-ended" sentence) (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); the accident-date conflict citing records 1 and 2 (header date, no choice between dates, D-017) and record 7's intake line; the K5 causation item for record 7's intake line; the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; the bills-to-request line is exactly "Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management." UT: every match of the case-insensitive pattern `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
spec/REQUIREMENTS.md:273:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
spec/REQUIREMENTS.md:370:| 3 | `memory/contracts/api.md` / `memory/DECISIONS.md` | `confirm_date` with a non-candidate date must be `422 date_invalid`; the AI line in DECISIONS must match R-EX-4(1); the gap example for a phone note must follow D-003 (excluded from gap math). | `grep -n "date_invalid" memory/contracts/api.md`; `grep -n "AI assistance" memory/DECISIONS.md`; `grep -n "phone" memory/contracts/api.md memory/DECISIONS.md` | T-028 (architect) |
evals/golden/sample.export.expected.txt:51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:14.750Z

**tool call — Bash**
````
{
 "command": "git log --oneline -8 && echo \"---\" && git log --oneline -1 0c03c4f && git show --stat 0c03c4f | head -30",
 "description": "Confirm commit history around 0c03c4f"
}
````

### User / tool · 2026-11-02T01:06:14.883Z

**tool result**
````
65537a4 fix(harness): debt entry no longer masks later fails; board-guard catches move-done in any arg order; M0 r3 closures
0c03c4f fix(evals): golden r3 fixes - both-sides accident conflict, self_report_spans key, R-EX-4 AI line, tighter flag matching
4cc0f81 docs(spec): golden is authority for exports; section 8 owners updated
de749c2 docs(architect): T-028 consistency pass (D-022, lexicon v2 categories, mg., confirm_date)
3426f3a chore(orchestrator): D-024 token budget; T-005/T-009/T-014 accepted with debt; T-027/T-028 split cards
158219b feat(frontend): board Office tab and /api/office (T-026)
654b31c docs(research): T-008 round 4 — quote record 7, A10 reason, referral scope, src 20 affiliation
cf009d2 docs(research): T-012 round 3 — 30-day retention default, §181.154 per-disclosure question to counsel, D-020 demo store-nothing
---
0c03c4f fix(evals): golden r3 fixes - both-sides accident conflict, self_report_spans key, R-EX-4 AI line, tighter flag matching
commit 0c03c4f1923c258933cb780c77997ccadaf6e6e0
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 19:04:54 2026 -0600

    fix(evals): golden r3 fixes - both-sides accident conflict, self_report_spans key, R-EX-4 AI line, tighter flag matching
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 evals/golden/README.md                             |  2 +-
 evals/golden/case_01_date_formats.expected.json    |  2 +-
 .../case_06_subtle_pre_existing.expected.json      |  6 +--
 evals/golden/check_golden.py                       | 62 +++++++++++++++++-----
 evals/golden/sample.expected.json                  | 17 +++---
 evals/golden/sample.export.expected.txt            |  7 ++-
 6 files changed, 68 insertions(+), 28 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:28.707Z

**tool call — Bash**
````
{
 "command": "echo \"--- full (no head) grep ---\"; grep -rn \"self_report_spans\\|patient_self_report\\|patient_report\" evals/golden; echo \"--- sample.expected.json span-ish keys ---\"; grep -n \"spans\\|self_report\\|patient_\" evals/golden/sample.expected.json | head -40; echo \"--- case_01 / case_06 spans keys ---\"; grep -n \"spans\" evals/golden/case_01_date_formats.expected.json evals/golden/case_06_subtle_pre_existing.expected.json; echo \"--- inventory of all span-ish keys across golden ---\"; grep -rhoE '\"[a-z_]*spans\"' evals/golden | sort | uniq -c",
 "description": "Full inventory of self-report span keys in golden"
}
````

### User / tool · 2026-11-02T01:06:28.829Z

**tool result**
````
--- full (no head) grep ---
evals/golden/case_06_subtle_pre_existing.expected.json:74:      "self_report_spans": [
evals/golden/case_06_subtle_pre_existing.expected.json:77:          "source_kind": "patient_report",
evals/golden/case_06_subtle_pre_existing.expected.json:120:      "self_report_spans": [
evals/golden/case_06_subtle_pre_existing.expected.json:123:          "source_kind": "patient_report",
evals/golden/case_06_subtle_pre_existing.expected.json:157:      "self_report_spans": [
evals/golden/case_06_subtle_pre_existing.expected.json:160:          "source_kind": "patient_report",
evals/golden/check_golden.py:87:    if sp.get("source_kind") != "patient_report":
evals/golden/check_golden.py:88:        out.append("source_kind must be 'patient_report' (D-022)")
evals/golden/check_golden.py:156:              "self_report_spans", "note", "needs_review", "date_candidates"}
evals/golden/check_golden.py:160:        not span_problems(dict(excerpt="Tenderness over the anterior shoulder", source_kind="patient_report", attribution_any=["x"])) or \
evals/golden/check_golden.py:161:        span_problems(dict(excerpt="C/O neck pain", source_kind="patient_report", attribution_any=["C/O"])):
evals/golden/check_golden.py:225:        for sp in e.get("self_report_spans", []):
evals/golden/check_golden.py:486:        for sp in e.get("self_report_spans", []):
evals/golden/README.md:40:      "self_report_spans": [{"excerpt": "verbatim subjective sentence", "source_kind": "patient_report",
evals/golden/README.md:72:* **Entries.** Found when the product emits an entry that covers `record_nos`, has the same `date` (or both ambiguous), `provider` equal to the record's header label after whitespace normalization (code copies it; merged duplicates take the lowest-numbered record's label), an excerpt containing every `must_contain_excerpt` item, and a **summary** that by itself satisfies every `required_terms` item (case-insensitive, whitespace-collapsed). A summary that drops a qualifier its excerpt carries (hedge, negation such as "without loss of consciousness", laterality, "approx.", self-report marker) is `needs_review` with reason `SUMMARY_DROPS_QUALIFIER` (D-022) and counts as not found. **Self-report:** for each `self_report_spans` item the summary must contain ≥ 1 `attribution_any` word, else the same reason. Spans are subjective sentences only (no findings, assessments or measurements). Recall pooled across cases ≥ 95%. More entries than `expected_entry_count` = dedupe failure.
evals/golden/case_01_date_formats.expected.json:175:      "self_report_spans": [
evals/golden/case_01_date_formats.expected.json:178:          "source_kind": "patient_report",
evals/golden/sample.expected.json:109:      "self_report_spans": [
evals/golden/sample.expected.json:112:          "source_kind": "patient_report",
evals/golden/sample.expected.json:272:      "self_report_spans": [
evals/golden/sample.expected.json:275:          "source_kind": "patient_report",
evals/golden/sample.expected.json:638:      "subtype": "patient_reported_onset",
evals/golden/sample.expected.json:639:      "source_kind": "patient_report"
--- sample.expected.json span-ish keys ---
109:      "self_report_spans": [
112:          "source_kind": "patient_report",
272:      "self_report_spans": [
275:          "source_kind": "patient_report",
638:      "subtype": "patient_reported_onset",
639:      "source_kind": "patient_report"
--- case_01 / case_06 spans keys ---
evals/golden/case_01_date_formats.expected.json:175:      "self_report_spans": [
evals/golden/case_06_subtle_pre_existing.expected.json:74:      "self_report_spans": [
evals/golden/case_06_subtle_pre_existing.expected.json:120:      "self_report_spans": [
evals/golden/case_06_subtle_pre_existing.expected.json:157:      "self_report_spans": [
--- inventory of all span-ish keys across golden ---
  10 "self_report_spans"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:30.199Z

**tool call — Bash**
````
{
 "command": "echo \"--- R-EX-4(1) text in REQUIREMENTS (line 122) ---\"; sed -n '122p' spec/REQUIREMENTS.md | grep -o \"(1) AI-assistance line.\\{0,260\\}\"; echo \"--- r3 quoted R-EX-4(1) string present in REQUIREMENTS? ---\"; grep -n \"every item in the treatment section was accepted by the paralegal. Items not reviewed: N\" spec/REQUIREMENTS.md; echo \"rc=$?\"; echo \"--- section 6 block 2 AI line context (REQUIREMENTS 265-285) ---\"; sed -n '265,285p' spec/REQUIREMENTS.md | cut -c1-400; echo \"--- README authority sentences ---\"; grep -n \"authority\\|now maintained here\" evals/golden/README.md | cut -c1-300",
 "description": "Check R-EX-4(1) spec text and README authority lines"
}
````

### User / tool · 2026-11-02T01:06:30.311Z

**tool result**
````
--- R-EX-4(1) text in REQUIREMENTS (line 122) ---
(1) AI-assistance line (D-009), fixed text: "AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export." followed by "Pending items: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, w
--- r3 quoted R-EX-4(1) string present in REQUIREMENTS? ---
rc=1
--- section 6 block 2 AI line context (REQUIREMENTS 265-285) ---
Billed charges stated in these records: $8,390.00
```

**Block 2 — Internal review notes — do not send**

```
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.

FLAGS ACCEPTED
- Gap: 73 days, March 6, 2026 to May 18, 2026: record 6 (Capital PT, visit 9, March 6, 2026) to record 7 (Hill Country Pain Management, new patient, May 18, 2026).
- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
- Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
- Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill C

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
--- README authority sentences ---
99:12. **Export golden (round 3).** `sample.export.expected.txt` is now maintained here (started from REQUIREMENTS §6). Changes: total line per D-019; the EMS summary says "complained of" (D-022 attribution); record 1 appears under "flagged language quoted in the letter" because its quote contains
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:38.784Z

**tool call — Bash**
````
{
 "command": "echo \"--- README authority / lags sentences ---\"; grep -n \"lags\\|golden files are\\|authority\" evals/golden/README.md | cut -c1-250; echo \"--- unknown-key guard in check_golden (line 150-160) ---\"; sed -n '150,158p' evals/golden/check_golden.py; echo \"--- notes-vs-s6 compare in check_golden? ---\"; grep -n \"REQUIREMENTS\\|s6\\|block 2\\|notes\" evals/golden/check_golden.py | head -20; echo \"--- accident-date check in check_golden ---\"; grep -n \"does not choose\\|rear-ended\\|accident-date\" evals/golden/check_golden.py | head; echo \"--- sample.expected.json C1 evidence ---\"; grep -n \"rear-ended\\|does not choose\" evals/golden/sample.expected.json | cut -c1-200",
 "description": "Check README authority text, checker guards, and C1 evidence"
}
````

### User / tool · 2026-11-02T01:06:38.896Z

**tool result**
````
--- README authority / lags sentences ---
55:  "flags": [{"id","type": "gap|conflict|pre_existing|causation","level": "must|should","subtype",
58:             "from_date","to_date","days"}],            // gap flags only for the last three
68:(`tolerated` replaces the earlier `tolerated_flags`.)
74:* **Flags — type match is explicit.** A golden flag is matched only by a candidate flag **of the same `type`** that cites every record in `cite.all` and ≥ 1 of `cite.any` (gap flags also need equal `from_date`/`to_date`/`days`). **Overlapping 
84:* **Future-dated records are intentional** (case_02 is in leap year 2028; case_06/08 run into late 2026). A future-date warning, if the product adds one, must not alter flags, gaps or entries.
88:1. **Strict `> 30`.** A gap flags only when strictly longer than 30 calendar days.
94:7. **Injected text is a code-detected warning** (row 14), not a fifth flag type; real flags stay open.
96:9. **`tolerated`** lists flags a careful tool may reasonably raise (e.g. possible duplicate x-ray billing in case_03, the denial-as-informational pre_existing in case_06, name-form variants in case_05).
--- unknown-key guard in check_golden (line 150-160) ---
    for gi in range(len(golden)):
        try_(gi, set())
    return {golden[gi]["id"] for gi in owner.values()}


ENTRY_KEYS = {"id", "record_nos", "date", "date_status", "encounter", "provider", "must_contain_excerpt", "required_terms",
              "self_report_spans", "note", "needs_review", "date_candidates"}

# a mislabelled span MUST be rejected (proves the span check is live)
--- notes-vs-s6 compare in check_golden? ---
13:    (billing statements, phone notes and ambiguous dates are excluded) and flag == (days > 30);
24:    evidence appears in the notes;
299:        err(cid, "totals.display removed: use letter_line / ui_line / notes_lines (one canonical string per surface)")
384:            for surf in [ex["totals"]["letter_line"], ex["totals"]["ui_line"]] + ex["totals"]["notes_lines"]:
442:    notes = etxt.split(m_n)[1].split("\n", 1)[1]
447:    for m in re.finditer(r'[Rr]ecord (\d+) \(([^)]*)\)', notes):
451:            errs.append(f"export notes: 'record {n} ({m.group(2)})' != '{want}'")
452:        tail = notes[m.end(): m.end() + 6]
455:            errs.append(f"export notes: quote cited to record {n} is not in record {n}: {q.group(1)[:50]}")
519:    # (4) derived notes sections: flagged language quoted in the letter, bills to request
531:    sec = re.search(r"FLAGGED LANGUAGE QUOTED IN THE LETTER[^\n]*\n(.*?)\n\n", notes, re.S)
537:            errs.append(f"export notes: malformed flagged-language line: {line[:60]}")
542:        errs.append(f"export notes: flagged-language section != derived from golden flags (D-012/R-EX-4). derived={derived} exported={exported}")
551:    sb = re.search(r"BILLS TO REQUEST[^\n]*\n- (.+)\.\n", notes)
554:        errs.append(f"export notes: bills to request {got_bills} != derived (label up to first comma, chronological) {want_bills}")
557:            errs.append(f"export notes: {h} should carry '(itemized ledger)'")
559:    bullets = {l.split(":")[0].lower(): l for l in notes.split("\n") if l.startswith("- ")}
570:            errs.append(f"export notes: no FLAGS ACCEPTED bullet for {f['id']}")
573:                errs.append(f"export notes: gap bullet lacks {f['id']} days/dates")
577:                    errs.append(f"export notes: must flag {f['id']} evidence missing from its bullet: {ev['excerpt'][:50]}")
--- accident-date check in check_golden ---
420:      cand("conflict", [(7, "Date of accident per intake form: 2026-01-19."), (1, "rear-ended at approx. 35 mph")])], {"G1", "C1"}),
578:        else:   # accident-date conflict (R-FL-2/R-EX-4): BOTH sides quoted, no choice made, no computed delay
582:            if "does not choose" not in b or not all(f"ecord {n}" in b for n in (1, 2, 7)):
583:                errs.append(f"export notes: {f['id']} bullet must cite records 1, 2, 7 and say the tool does not choose between the dates")
--- sample.expected.json C1 evidence ---
94:      "must_contain_excerpt": "rear-ended at approx. 35 mph",
96:        "rear-ended",
503:          "excerpt": "rear-ended at approx. 35 mph"
815:        "Restrained driver rear-ended at approx. 35 mph; neck pain 7/10 and headache."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:43.411Z

**tool call — Bash**
````
{
 "command": "sed -n '575,590p' evals/golden/check_golden.py; echo \"--- memory ---\"; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md; echo; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md; echo; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md | head -60",
 "description": "Read accident-date checker lines and reviewer memory notes"
}
````

### User / tool · 2026-11-02T01:06:43.508Z

**tool result**
````
            for ev in f["evidence"]:
                if ev.get("field", "excerpt") == "excerpt" and norm(ev["excerpt"]) not in norm(b):
                    errs.append(f"export notes: must flag {f['id']} evidence missing from its bullet: {ev['excerpt'][:50]}")
        else:   # accident-date conflict (R-FL-2/R-EX-4): BOTH sides quoted, no choice made, no computed delay
            for ev in f["evidence"]:
                if ev.get("field", "excerpt") == "excerpt" and norm(ev["excerpt"]) not in norm(b):
                    errs.append(f"export notes: {f['id']} bullet must quote both sides; missing: {ev['excerpt'][:50]}")
            if "does not choose" not in b or not all(f"ecord {n}" in b for n in (1, 2, 7)):
                errs.append(f"export notes: {f['id']} bullet must cite records 1, 2, 7 and say the tool does not choose between the dates")
            if re.search(r"\bdelay\w*|\d+ days|months? after", b, re.I):
                errs.append(f"export notes: {f['id']} bullet computes a delay (D-017)")
    first = notes.strip().split("\n")
    if first[2] != "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0." or "Pending items" in notes:
        errs.append("export notes: AI-assistance line must be the R-EX-4(1) text with 'Items not reviewed: N.' and no 'Pending items' line")
    if "FLAGS ACCEPTED" not in notes or "AMOUNTS NOT TOTALED" not in notes:
        errs.append("export notes: block incomplete")
--- memory ---
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

---
name: golden-set-recurring-findings
description: Patterns found reviewing evals/golden (T-015, 2026-11-01) to re-check on any later golden/eval change — must/should downgrades, leaky must_not regexes, missing tolerated flags
metadata:
  type: project
---

Recurring golden-set weaknesses found in the T-015 review (commit 47520a8, verdict fail):
- Appendix C "Expected flags (at minimum)" items got downgraded to `should` (K4 new onset after the 73-day gap, K5 wrong intake accident date). Under README scoring, `should` never counts as a miss, and cross-type credit isn't implemented. Re-check levels whenever golden files change.
- Explicit prior-condition mentions marked `should` (case_06 P2/P3), while the sample's different-region prior (P1) is `must`. Check that levels are consistent across cases.
- A credible adjuster attack with no golden or tolerated entry gets scored as a false positive (case_06 "denies prior neck problems" vs chiropractor history). Ask "what would the adjuster's letter quote?" and confirm each answer is must, should or tolerated.
- must_not regexes are only tested negatively (they must not match the input). Probe them with known-bad phrasings: the sample M9 regex missed "full recovery", and M2 missed "caused by the January collision" and "Degenerative findings".

Round 2 (commit 3c5eb7c) added these patterns:
- A level fix isn't enough. If two `must` flags share type and cite (K4/K5: causation, record 7) and matching is type+cite only, one candidate satisfies both. Simulate the README matching rule literally, and require evidence overlap plus one-to-one assignment.
- The byte-exact export golden (extracted from REQUIREMENTS §6) can drift from the golden JSON: a missing must-flag line, and evidence changes such as C1 "rear-ended" that should add a "flagged language" row. Rebuild each notes section from the JSON plus the R-EX-4 rules, and diff.
- Spec text (R-FL-4) can lag behind a golden change. Grep REQUIREMENTS for the old rule.

Round 3 (commit f8c1948, verdict fail) added these patterns:
- Schema key drift can silently disable a check. The JSON used `spans` while README and check_golden read `self_report_spans`, so the D-022 checks ran on empty lists and the validator stayed green. Count keys across all JSON files, and mutation-test every new assertion on a scratchpad copy (break the data, and the checker must exit 1).
- The writer fixes the line the reviewer named (the K5 line) and leaves the sibling lines that REQUIREMENTS §8 also listed (the C1 conflict bullet quoting both sides, the AI line). Byte-diff the golden against REQUIREMENTS §6 every round, and run the §8 reconciliation greps literally.
- Either-way substring overlap in the reference matcher lets a whole-record excerpt satisfy every golden flag on that record. Probe with whole-record and one-word candidates.

**Why:** these let a weaker product pass the ship bar while hiding exactly what costs the paralegal credibility.
**How to apply:** on any re-review of evals/golden or evals.run, re-run a probe like artifacts/review-evidence/T-015-paralegal-regex-probe.py and re-check the level of every Appendix C item. Related: [[reviewer-hook-constraints]]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:57.100Z

**tool call — Bash**
````
{
 "command": "grep -n \"__file__\\|Path(\\|open(\\|REQUIREMENTS\\|read_text\" evals/golden/check_golden.py | head -20; ls -la .venv/bin/python 2>&1 | head -2; echo \"--- export structure ---\"; grep -n \"INTERNAL REVIEW NOTES\\|^Billed\\|^TREATMENT\\|^[A-Z][A-Z ,—-]*$\" evals/golden/sample.export.expected.txt | head -20; echo \"--- s6 headings ---\"; grep -n \"^\\*\\*Block\\|^\\`\\`\\`$\" spec/REQUIREMENTS.md | sed -n '1,40p'",
 "description": "Check checker path handling and export/spec structure"
}
````

### User / tool · 2026-11-02T01:06:57.157Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No escaped character) | command: grep -n "__file__\|Path(\|open(\|REQUIREMENTS\|read_text" evals/golden/check_golden.py | head -20; ls -la .venv/bin/python 2>&1 | head -2; echo "--- export structure ---"; grep -n "INTERNAL REVIEW NOT
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:59.019Z

**tool call — Bash**
````
{
 "command": "grep -n \"__file__\\|Path(\\|open(\\|REQUIREMENTS\\|read_text\" evals/golden/check_golden.py | head -20; ls -la .venv/bin/python 2>&1 | head -2; echo \"--- export structure ---\"; grep -n \"INTERNAL REVIEW NOTES\\|^Billed\\|^[A-Z][A-Z ,-]*$\" evals/golden/sample.export.expected.txt | head -20; echo \"--- s6 block markers ---\"; grep -n \"Block 1\\|Block 2\\|Block 3\" spec/REQUIREMENTS.md",
 "description": "Check checker path handling and export structure"
}
````

### User / tool · 2026-11-02T01:06:59.128Z

**tool result**
````
35:D = pathlib.Path(__file__).parent
178:    ex = json.loads(jp.read_text())
179:    text = (D / ex["input_file"]).read_text()
436:etxt = ep.read_text()
597:items = [json.loads(l) for l in (D / "hallucinations.jsonl").read_text().splitlines() if l.strip()]
629:ctrls = [json.loads(l) for l in (D / "hallucinations_controls.jsonl").read_text().splitlines() if l.strip()]
649:n_must = sum(len(json.loads(p.read_text())["must_not"]) for p in cases)
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
--- export structure ---
2:TREATMENT CHRONOLOGY
40:BILLED CHARGES
47:Billed charges stated in these records: $8,390.00
49:INTERNAL REVIEW NOTES — DO NOT SEND
53:FLAGS ACCEPTED
60:FLAGS DISMISSED
71:AMOUNTS NOT TOTALED
83:RECORDS NOT IN THE TREATMENT SECTION
86:EDITED ITEMS
89:PENDING ITEMS NOT INCLUDED
--- s6 block markers ---
217:**Block 1 — Treatment section (paste into letter)**
268:**Block 2 — Internal review notes — do not send**
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:18.172Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-015-r4-paralegal-recheck.py",
 "content": "#!/usr/bin/env python3\n\"\"\"T-015 round 4 mechanical re-check (paralegal-reviewer).\n\nUsage: .venv/bin/python -I artifacts/review-evidence/T-015-r4-paralegal-recheck.py <scratch_dir>\n\nPart A: byte comparison of the golden export blocks against REQUIREMENTS s6 blocks 1 and 2,\n        and of the AI-assistance line against R-EX-4(1) in REQUIREMENTS.\nPart B: mutation tests on a scratch copy of evals/golden (the real files are never modified).\n        Each mutation must make check_golden.py exit 1; the unmutated copy must exit 0.\n\"\"\"\nimport difflib\nimport json\nimport pathlib\nimport shutil\nimport subprocess\nimport sys\n\nROOT = pathlib.Path(\"/Users/arsis/zlayt-pm-project\")\nGOLD = ROOT / \"evals\" / \"golden\"\nREQ = (ROOT / \"spec\" / \"REQUIREMENTS.md\").read_text()\nEXP = (GOLD / \"sample.export.expected.txt\").read_text()\nSCRATCH = pathlib.Path(sys.argv[1])\n\nNOTES_HEAD = \"INTERNAL REVIEW NOTES — DO NOT SEND\"\n\n\ndef s6_block(n):\n    head = {1: \"**Block 1 — Treatment section (paste into letter)**\",\n            2: \"**Block 2 — Internal review notes — do not send**\"}[n]\n    i = REQ.index(head)\n    f1 = REQ.index(\"```\\n\", i) + 4\n    f2 = REQ.index(\"\\n```\", f1)\n    return REQ[f1:f2].rstrip(\"\\n\")\n\n\ndef show_diff(a, b, label):\n    d = list(difflib.unified_diff(a.splitlines(), b.splitlines(), \"s6 \" + label, \"golden \" + label, lineterm=\"\", n=0))\n    print(f\"{label}: identical={a == b}  (s6 lines={len(a.splitlines())}, golden lines={len(b.splitlines())})\")\n    for line in d[:40]:\n        print(\"   \" + line)\n\n\nprint(\"=== PART A: byte comparisons ===\")\ns6_notes = s6_block(2)\ns6_letter = s6_block(1)\nex_notes = EXP[EXP.index(NOTES_HEAD):].rstrip(\"\\n\")\nex_letter = EXP[:EXP.index(NOTES_HEAD)].rstrip(\"\\n\")\nshow_diff(s6_letter, ex_letter, \"letter (block 1)\")\nshow_diff(s6_notes, ex_notes, \"notes (block 2)\")\n\nai_golden = [l for l in EXP.splitlines() if \"drafted with AI assistance\" in l]\nai_req = [l for l in REQ.splitlines() if \"drafted with AI assistance\" in l or \"AI-assistance line (D-009)\" in l]\nprint(\"golden AI lines:\", ai_golden)\nprint(\"REQUIREMENTS lines naming the AI line:\")\nfor l in ai_req:\n    print(\"   \", l[:200])\nrex41 = \"AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.\"\nprint(\"R-EX-4(1) fixed text present verbatim in REQUIREMENTS:\", rex41 in REQ)\nprint(\"golden AI line equals R-EX-4(1) fixed text:\", any(rex41 in l for l in ai_golden))\nprint(\"'Pending items' in golden export:\", \"Pending items\" in EXP)\nprint(\"'Items not reviewed: 0.' in golden export:\", \"Items not reviewed: 0.\" in EXP)\nprint(\"'Items not reviewed' occurrences REQUIREMENTS:\", REQ.count(\"Items not reviewed\"),\n      \" golden:\", EXP.count(\"Items not reviewed\"))\n\nprint()\nprint(\"=== PART B: mutation tests on scratch copy ===\")\n\n\ndef run_checker(d):\n    p = subprocess.run([sys.executable, \"-I\", str(d / \"check_golden.py\")], capture_output=True, text=True)\n    out = (p.stdout + p.stderr).strip().splitlines()\n    return p.returncode, (out[-1] if out else \"\")\n\n\ndef fresh(name):\n    d = SCRATCH / name\n    if d.exists():\n        shutil.rmtree(d)\n    shutil.copytree(GOLD, d)\n    return d\n\n\ndef first_key_dict(obj, key):\n    if isinstance(obj, dict):\n        if key in obj:\n            return obj\n        for v in obj.values():\n            r = first_key_dict(v, key)\n            if r is not None:\n                return r\n    elif isinstance(obj, list):\n        for v in obj:\n            r = first_key_dict(v, key)\n            if r is not None:\n                return r\n    return None\n\n\nresults = []\n\nd = fresh(\"m0_base\")\nresults.append((\"base (unmutated copy)\", *run_checker(d)))\n\n# M1: objective exam sentence tagged as patient report under the key the JSON uses\nd = fresh(\"m1_objective_span\")\np = d / \"sample.expected.json\"\nj = json.loads(p.read_text())\nent = first_key_dict(j, \"self_report_spans\")\nent[\"self_report_spans\"][0][\"excerpt\"] = \"Alert and oriented\"\np.write_text(json.dumps(j, indent=2, ensure_ascii=False) + \"\\n\")\nresults.append((\"M1 objective span 'Alert and oriented' under self_report_spans\", *run_checker(d)))\n\n# M2: drop the record-1 quote from the accident-date conflict bullet only\nd = fresh(\"m2_drop_ems_quote\")\np = d / \"sample.export.expected.txt\"\nlines = p.read_text().split(\"\\n\")\nhit = [i for i, l in enumerate(lines) if l.startswith(\"- Conflict, accident date:\")]\nassert len(hit) == 1, hit\nlines[hit[0]] = lines[hit[0]].replace('Record 1 (Austin EMS run report, January 9, 2026): \"41M restrained driver, rear-ended at approx. 35 mph.\" ', \"\")\np.write_text(\"\\n\".join(lines))\nresults.append((\"M2 drop record-1 'rear-ended' quote from accident-date bullet\", *run_checker(d)))\n\n# M3: rename self-report key to a non-schema key (guards against silent disable)\nd = fresh(\"m3_unknown_key\")\np = d / \"sample.expected.json\"\nj = json.loads(p.read_text())\nent = first_key_dict(j, \"self_report_spans\")\nent[\"spans\"] = ent.pop(\"self_report_spans\")\np.write_text(json.dumps(j, indent=2, ensure_ascii=False) + \"\\n\")\nresults.append((\"M3 self_report_spans renamed to 'spans' (unknown key)\", *run_checker(d)))\n\n# M4: reintroduce the stale Pending line in the export notes\nd = fresh(\"m4_pending_line\")\np = d / \"sample.export.expected.txt\"\np.write_text(p.read_text().replace(\"Items not reviewed: 0.\", \"Pending items: 0.\"))\nresults.append((\"M4 'Pending items: 0.' in notes block\", *run_checker(d)))\n\nfor name, rc, last in results:\n    print(f\"{name}: exit={rc}  last_line={last!r}\")\n"
}
````

### User / tool · 2026-11-02T01:07:18.278Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-015-r4-paralegal-recheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:20.415Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$SCR/t015r4\" && .venv/bin/python -I artifacts/review-evidence/T-015-r4-paralegal-recheck.py \"$SCR/t015r4\" 2>&1 | tee artifacts/review-evidence/T-015-r4-paralegal-recheck.out.txt; echo \"PARTB_RC=${PIPESTATUS[0]}\"",
 "description": "Run r4 recheck script with byte diffs and mutations"
}
````

### User / tool · 2026-11-02T01:07:20.796Z

**tool result**
````
=== PART A: byte comparisons ===
letter (block 1): identical=False  (s6 lines=46, golden lines=48)
   --- s6 letter (block 1)
   +++ golden letter (block 1)
   @@ -0,0 +1 @@
   +=== LETTER_TEXT (block 1: paste into letter) ===
   @@ -46,0 +48 @@
   +=== INTERNAL_NOTES_TEXT (block 2: do not send) ===
notes (block 2): identical=True  (s6 lines=42, golden lines=42)
golden AI lines: ['This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.']
REQUIREMENTS lines naming the AI line:
    | R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009
    This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
R-EX-4(1) fixed text present verbatim in REQUIREMENTS: True
golden AI line equals R-EX-4(1) fixed text: False
'Pending items' in golden export: False
'Items not reviewed: 0.' in golden export: True
'Items not reviewed' occurrences REQUIREMENTS: 1  golden: 1

=== PART B: mutation tests on scratch copy ===
base (unmutated copy): exit=0  last_line='golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered'
M1 objective span 'Alert and oriented' under self_report_spans: exit=1  last_line=' - sample: E1: self_report span: objective/assessment content: Alert and oriented'
M2 drop record-1 'rear-ended' quote from accident-date bullet: exit=1  last_line=' - export notes: C1 bullet must cite records 1, 2, 7 and say the tool does not choose between the dates'
M3 self_report_spans renamed to 'spans' (unknown key): exit=1  last_line=" - sample: E1: unknown entry keys ['spans'] (a renamed key would silently disable a check)"
M4 'Pending items: 0.' in notes block: exit=1  last_line=" - export notes: AI-assistance line must be the R-EX-4(1) text with 'Items not reviewed: N.' and no 'Pending items' line"
PARTB_RC=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:48.523Z

**tool call — Bash**
````
{
 "command": "echo \"--- s8 row 4 literal grep ---\"; grep -n \"patient_self_report\\|summary+excerpt\" evals/golden/README.md evals/golden/sample.expected.json; echo \"rc=$?\"; echo \"--- r3 minor: M2 good_examples ---\"; grep -n \"no physician\" evals/golden/sample.expected.json | cut -c1-220; echo \"--- K3 flag ---\"; sed -n '634,641p' evals/golden/sample.expected.json; echo \"--- export line 55 trailing period and line 51-52 ---\"; sed -n '51,52p' evals/golden/sample.export.expected.txt | cat -A | cut -c1-80; echo \"--- git status of golden and spec (read-only check) ---\"; git -C /Users/arsis/zlayt-pm-project status --porcelain evals/golden spec | head",
 "description": "Check remaining r3 minors and spec-key grep"
}
````

### User / tool · 2026-11-02T01:07:48.661Z

**tool result**
````
--- s8 row 4 literal grep ---
rc=1
--- r3 minor: M2 good_examples ---
1014:        "Per the patient, symptoms started after the January collision; the note records no physician opinion on cause.",
--- K3 flag ---
          "excerpt": "Patient states symptoms began after the January collision"
        }
      ],
      "summary": "Causation rests on patient self-report, not a physician's causation opinion.",
      "subtype": "patient_reported_onset",
      "source_kind": "patient_report"
    },
    {
--- export line 55 trailing period and line 51-52 ---
cat: illegal option -- A
usage: cat [-belnstuv] [file ...]
--- git status of golden and spec (read-only check) ---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:52.494Z

**tool call — Bash**
````
{
 "command": "sed -n '1000,1018p' evals/golden/sample.expected.json | cut -c1-200; echo \"--- M2 good_examples region ---\"; grep -n '\"good_examples\"\\|\"bad_examples\"' evals/golden/sample.expected.json | tail -8",
 "description": "View context around the remaining tool-commentary example"
}
````

### User / tool · 2026-11-02T01:07:52.590Z

**tool result**
````
    },
    {
      "id": "M10",
      "statement": "Presents the patient's self-report (records 1, 9) as a physician's opinion or examination finding.",
      "check": "judge",
      "bad_examples": [
        "The treating physician concluded the symptoms were caused by the January collision.",
        "Dr. at Hill Country attributes the symptoms to the collision.",
        "Examination revealed neck injury with 7/10 pain.",
        "Patient states the collision caused his symptoms.",
        "Patient reports her pain is from the crash."
      ],
      "good_examples": [
        "Patient states symptoms began after the January collision.",
        "Per the patient, symptoms started after the January collision; the note records no physician opinion on cause.",
        "41M restrained driver complaining of neck pain 7/10 and headache (C/O)."
      ]
    },
    {
--- M2 good_examples region ---
1074:      "bad_examples": [
1080:      "good_examples": [
1091:      "bad_examples": [
1097:      "good_examples": [
1108:      "bad_examples": [
1114:      "good_examples": [
1125:      "bad_examples": [
1139:      "good_examples": [
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:08:32.108Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-015-paralegal-r4.md",
 "content": "# T-015 round 4: paralegal-reviewer mechanical re-check (after commit 0c03c4f, HEAD 65537a4)\n\n**Verdict: changes** (0 blockers, 1 major, 1 minor).\n\nThe r3 blocker and the r3 span-key major are resolved on the output. The r3 AI-line major is only partly resolved. The golden AI line now matches REQUIREMENTS §6 byte for byte, but REQUIREMENTS R-EX-4(1), the normative text, still says something different. The r3 review also quoted an R-EX-4(1) string that is not in the spec file.\n\nResolved on the output:\n- **r3 blocker (accident-date bullet).** Export line 55 quotes record 7's intake line and record 1's \"rear-ended\" sentence, and says \"The tool does not choose between the dates.\" Deleting the record-1 quote makes check_golden.py exit 1 (mutation M2).\n- **r3 major (self-report key).** All 10 self-report entries use `self_report_spans`. None use `spans`. An objective span under that key exits 1 (M1), and a renamed key exits 1 (M3).\n- **r3 minor (K3 flag).** K3 now has `subtype: patient_reported_onset` and `source_kind: patient_report`. The `patient_self_report` string is gone from the golden.\n- **r3 major (notes block), partial.** The golden notes block is byte-identical to REQUIREMENTS §6 block 2. The stale \"Pending items: 0.\" line and the stray period are gone. The README \"authority where REQUIREMENTS lags\" sentence is gone. The AI-line mismatch with R-EX-4(1) remains (finding 1).\n\nProbe script: `artifacts/review-evidence/T-015-r4-paralegal-recheck.py`. Output: `artifacts/review-evidence/T-015-r4-paralegal-recheck.out.txt`.\n\nCommands and outputs (verbatim):\n- `python3 evals/golden/check_golden.py` → `golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered` EXIT=0\n- `grep -n \"Conflict, accident date\" evals/golden/sample.export.expected.txt` → line 55 contains `\"Date of accident per intake form: 2026-01-19.\"` and `\"41M restrained driver, rear-ended at approx. 35 mph.\"` and `The tool does not choose between the dates.` (record 1 source: sample.txt:6, record 7 source: sample.txt:36)\n- `grep -rn \"self_report_spans\\|patient_self_report\\|patient_report\" evals/golden | head` → 10 `self_report_spans` hits (case_01:175, case_06:74/120/157, sample:109/272, plus check_golden and README); `patient_self_report` no hit; `sample.expected.json:638-639` = `patient_reported_onset` / `patient_report`. `grep -rhoE '\"[a-z_]*spans\"' evals/golden` → `10 \"self_report_spans\"`, no other key.\n- `grep -n \"Pending items\" evals/golden/sample.export.expected.txt` → no match (rc=1)\n- `grep -n \"Items not reviewed: 0\\.\" evals/golden/sample.export.expected.txt` → `51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.`\n- `grep -n \"Items not reviewed\" spec/REQUIREMENTS.md evals/golden/sample.export.expected.txt` → `spec/REQUIREMENTS.md:273:` (identical sentence) and `evals/golden/sample.export.expected.txt:51:` (identical). The §6 line equals the golden AI line.\n- Probe Part A: `notes (block 2): identical=True`. `letter (block 1)`: body identical; the only differences are the golden's `=== LETTER_TEXT ===` and `=== INTERNAL_NOTES_TEXT ===` delimiter lines.\n- Probe Part A: `R-EX-4(1) fixed text present verbatim in REQUIREMENTS: True`; `golden AI line equals R-EX-4(1) fixed text: False`. `spec/REQUIREMENTS.md:122` R-EX-4(1) reads `AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.` followed by `Pending items: N.`. R-EX-4(11) reads `Pending items not included.`\n- Probe Part B (scratch copy, real files untouched): base exit=0; M1 objective span under self_report_spans exit=1 (`E1: self_report span: objective/assessment content: Alert and oriented`); M2 drop record-1 quote exit=1; M3 renamed key exit=1 (`unknown entry keys ['spans']`); M4 `Pending items: 0.` in notes exit=1.\n- `git status --porcelain evals/golden spec` → empty. `git log --oneline -3` → `65537a4`, `0c03c4f`, `4cc0f81`.\n- `grep -n \"patient_self_report\\|summary+excerpt\" evals/golden/README.md evals/golden/sample.expected.json` → no match (rc=1).\n- `grep -n \"no physician\" evals/golden/sample.expected.json` → line 1014 only.\n\nNot re-run this round: the r3 K4/K5 matcher probe and the r3 nurse probe. Their r3 minors are not re-tested here.\n\nModel note: this review was run as claude-haiku-5-5. The dossier's expected id (claude-opus-5-5) does not match the runtime model, so the id is recorded as observed.\n\n```json\n{\"card\": \"T-015\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"round 4 re-check after commit 0c03c4f (HEAD 65537a4). Files: evals/golden/check_golden.py, sample.export.expected.txt, sample.expected.json, case_01 and case_06 expected.json, README.md; spec/REQUIREMENTS.md R-EX-4(1), R-EX-4(11), section 6 blocks 1-2, section 8 row 4. No app (pre-code eval data). Sample case evals/golden/sample.txt. Prior rounds: reviews/T-015-paralegal-r3.md, reviews/T-015-legal-nurse-r3.md.\",\n \"exercised\": [\n  \"python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered' EXIT=0\",\n  \"grep accident-date bullet in sample.export.expected.txt (line 55 quotes intake line and record 1 'rear-ended at approx. 35 mph'; 'does not choose' present); record sources sample.txt:6 and :36\",\n  \"grep -rn self_report_spans|patient_self_report|patient_report evals/golden; grep -rhoE '\\\"[a-z_]*spans\\\"' evals/golden -> 10 self_report_spans, 0 spans, 0 patient_self_report\",\n  \"grep 'Pending items' export -> absent; grep 'Items not reviewed' spec/REQUIREMENTS.md and export -> identical line at REQUIREMENTS.md:273 and export:51\",\n  \"grep -n 'AI assistance' R-EX-4(1) at spec/REQUIREMENTS.md:122 and R-EX-4(11)\",\n  \"artifacts/review-evidence/T-015-r4-paralegal-recheck.py (.out.txt): byte diff of golden blocks 1-2 vs REQUIREMENTS section 6; R-EX-4(1) comparison; mutations M1-M4 on a scratch copy of evals/golden (base exit 0; M1, M2, M3, M4 each exit 1)\",\n  \"grep 'patient_self_report|summary+excerpt' README.md sample.expected.json -> no match; grep 'no physician' sample.expected.json -> line 1014\",\n  \"git status --porcelain evals/golden spec -> empty; git log --oneline -3 -> 65537a4, 0c03c4f, 4cc0f81\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"accident_conflict_both_sides\": 5, \"self_report_key_integrity\": 5, \"notes_block_matches_s6\": 4, \"ai_line_spec_consistency\": 2, \"tool_commentary_out_of_good_examples\": 3},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"AI-assistance line: golden and REQUIREMENTS section 6 agree, but normative R-EX-4(1) still has different text and a Pending items line that contradicts R-EX-4(11). The r3 finding's quoted R-EX-4(1) string is not in the spec.\",\n   \"evidence\": \"evals/golden/sample.export.expected.txt:51 'This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.' ; spec/REQUIREMENTS.md:273 same sentence (identical). spec/REQUIREMENTS.md:122 R-EX-4(1): 'AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' followed by 'Pending items: N.' R-EX-4(11) at :122: 'Pending items not included.' Probe Part A: 'R-EX-4(1) fixed text present verbatim in REQUIREMENTS: True; golden AI line equals R-EX-4(1) fixed text: False' (artifacts/review-evidence/T-015-r4-paralegal-recheck.out.txt). grep for the r3 quoted string 'every item in the treatment section was accepted by the paralegal. Items not reviewed: N' in spec/REQUIREMENTS.md -> rc=1.\",\n   \"why_it_matters\": \"R-EX-6 makes the export golden the byte-exact E2E target. An implementer who follows R-EX-4(1) fails the golden. An implementer who follows the golden contradicts R-EX-4(1). The spec also contradicts itself on pending items. The line says every item was reviewed, which overstates what the tool tracks. The count line is the one I check before export (checklist 17). Severity is held at major because the r3 finding was major and the residual is the same defect, not a new one.\",\n   \"fix\": \"Spec owner (architect or qa) picks one AI-line text and makes R-EX-4(1), REQUIREMENTS section 6 block 2 and the golden identical. Remove 'Pending items: N.' from R-EX-4(1) so it agrees with R-EX-4(11). Change the check_golden.py AI-line error text, which currently says 'the R-EX-4(1) text' while it checks the section 6 text, so it names the section that actually holds the text.\",\n   \"acceptance_test\": \"grep -n 'drafted with AI assistance' spec/REQUIREMENTS.md evals/golden/sample.export.expected.txt shows the same sentence in both files. grep -n 'Pending items: N' spec/REQUIREMENTS.md matches nothing. The r4 probe Part A prints 'golden AI line equals R-EX-4(1) fixed text: True'. check_golden.py exits 0.\"},\n  {\"severity\": \"minor\", \"title\": \"Carry-forward of the r3 minor: tool-authored commentary on what no physician said remains as a good example, now under M10\",\n   \"evidence\": \"evals/golden/sample.expected.json:1014 good_examples: 'Per the patient, symptoms started after the January collision; the note records no physician opinion on cause.' (grep 'no physician' returns only this line; the M2 examples the r3 finding named are gone.)\",\n   \"why_it_matters\": \"This sentence judges what the record set lacks. It is not the record's words, and R-EX-1 keeps that kind of tool commentary out of the letter. Golden good examples read as house style, so this example teaches the wrong style.\",\n   \"fix\": \"Replace with a record-words example, e.g. 'Per the patient, symptoms started after the January collision.'\",\n   \"acceptance_test\": \"grep -n 'no physician' evals/golden/sample.expected.json returns nothing. check_golden.py exits 0.\"}\n ],\n \"whats_right\": [\n  \"Export line 55 quotes both sides verbatim and says the tool does not choose between the dates. Deleting the record-1 quote from that bullet makes check_golden.py exit 1 (probe M2).\",\n  \"Self-report spans use one key everywhere (self_report_spans, 10 uses, 0 spans). An objective span under that key exits 1 (M1), and a renamed key exits 1 through the ENTRY_KEYS guard (M3).\",\n  \"The export notes block is byte-identical to REQUIREMENTS section 6 block 2. The stale Pending items line and the stray period are gone, and 'Items not reviewed: 0.' matches section 6 line 273.\"\n ],\n \"questions_for_chris\": [\n  \"Which AI-assistance text is authoritative: R-EX-4(1) ('AI assistance: ... before export.' followed by 'Pending items: N.') or REQUIREMENTS section 6 block 2 and the golden ('This chronology was drafted with AI assistance; ... Items not reviewed: 0.')? R-EX-4(1) also contradicts R-EX-4(11) ('Pending items not included.'). I am read-only on spec, so I have not edited it.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T01:08:32.270Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-015-paralegal-r4.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:08:35.678Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-015-r4-paralegal-jsoncheck.py",
 "content": "#!/usr/bin/env python3\n\"\"\"Check reviews/T-015-paralegal-r4.md: exactly one json fence, parses, verdict rule (CONTRACT 7.4), severity vocabulary.\"\"\"\nimport json\nimport pathlib\nimport re\nimport sys\n\npath = pathlib.Path(sys.argv[1])\ntext = path.read_text()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", text, re.S)\nassert len(blocks) == 1, f\"expected exactly one json fence, found {len(blocks)}\"\nrec = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in rec[\"findings\"]]\nassert all(s in {\"blocker\", \"major\", \"minor\", \"nit\"} for s in sev), sev\nwant = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"parsed OK; card\", rec[\"card\"], \"persona\", rec[\"persona\"], \"model\", rec[\"model\"])\nprint(\"severities\", sev, \"verdict\", rec[\"verdict\"], \"required by rule\", want)\nassert rec[\"verdict\"] == want, \"verdict rule violated\"\nassert len(rec[\"whats_right\"]) <= 3\nfor f in rec[\"findings\"]:\n    for k in (\"severity\", \"title\", \"evidence\", \"why_it_matters\", \"fix\", \"acceptance_test\"):\n        assert f.get(k), (k, f.get(\"title\"))\nprint(\"findings complete; whats_right\", len(rec[\"whats_right\"]), \"; verdict rule OK\")\n"
}
````

### User / tool · 2026-11-02T01:08:35.785Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-015-r4-paralegal-jsoncheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:08:37.142Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-015-r4-paralegal-jsoncheck.py reviews/T-015-paralegal-r4.md 2>&1 | tee artifacts/review-evidence/T-015-r4-paralegal-jsoncheck.out.txt",
 "description": "Validate r4 review JSON block and verdict rule"
}
````

### User / tool · 2026-11-02T01:08:37.249Z

**tool result**
````
parsed OK; card T-015 persona paralegal-reviewer model claude-haiku-5-5
severities ['major', 'minor'] verdict changes required by rule changes
findings complete; whats_right 3 ; verdict rule OK
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:08:41.323Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md",
 "old_string": "**Why:** these let a weaker product pass the ship bar while hiding exactly what costs the paralegal credibility.",
 "new_string": "Round 4 (commit 0c03c4f, HEAD 65537a4, verdict changes) added these patterns:\n- A fixed text can match one spec section and still break another. The golden AI line was made to match REQUIREMENTS section 6, but normative R-EX-4(1) keeps different text, and R-EX-4(1) contradicts R-EX-4(11). Diff the golden against every spec location that quotes the same text, not only the one the finding named.\n- A prior review's quoted \"spec text\" can be wrong. The r3 paralegal quoted an R-EX-4(1) string that grep does not find in REQUIREMENTS.md. Grep every quoted spec string before relying on it.\n- Key renames fix the data but can leave the checker's guard code stale. Mutation-test with the renamed key and with an objective span. The guard for unknown entry keys (ENTRY_KEYS in check_golden.py) is what makes the rename safe.\n\n**Why:** these let a weaker product pass the ship bar while hiding exactly what costs the paralegal credibility."
}
````

### User / tool · 2026-11-02T01:08:41.430Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:08:44.380Z

T-015 r4 verdict is **changes** (0 blockers, 1 major, 1 minor): the r3 blocker (accident-date bullet quotes both sides) and the self-report key major (`self_report_spans`, mutation-tested) are resolved; the AI-line major is only partly resolved because R-EX-4(1) still differs from the golden and §6.
Review: /Users/arsis/zlayt-pm-project/reviews/T-015-paralegal-r4.md (JSON validated by artifacts/review-evidence/T-015-r4-paralegal-jsoncheck.py; probe output in artifacts/review-evidence/T-015-r4-paralegal-recheck.out.txt).
Recorded model is claude-haiku-5-5, the runtime model; the dossier's expected claude-opus-5-5 does not match.
