# Subagent: Paralegal check: T-206 (Paralegal check: T-206)

Source: `agent-a8cb888aa538cf939.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T00:43:07.187Z

Check T-206 in /Users/arsis/zlayt-pm-project as the senior PI paralegal, starting from a fresh context. The card is commit 79714c6; read reviews/T-205-paralegal.md (your minors) and the T-206 handoff.

Extract a fresh `git archive 79714c6` into an empty directory and run demo mode on your own port; stop your PID afterward. In guided Step 3 on lib11:
- no bare date shows on uncounted ledger lines;
- the confirm note's next step is clear and correct for a demand-letter workflow.

The note says "If you count it, type the date into your letter yourself". Judge whether that's acceptable, or whether the letter should instead carry a visible placeholder. Report any private values only as <redacted>. Write reviews/T-206-paralegal.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:08.686Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-03T00:43:08.696Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:08.968Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-205-paralegal.md"
}
````

### User / tool · 2026-11-03T00:43:08.973Z

**tool result**
````
1	# T-205 review — paralegal-reviewer (Maria Delgado)
2	
3	Commit 203ac6a, fresh `git archive` in an empty scratch directory, demo mode (fixture backend, `ZLAYT_MODE=local`, health `demo_mode: true`) on port 7981. Listener PID 63090 stopped afterward (`lsof` exit 1, `curl` = 000). Private values seen: 0 (<redacted> count 0).
4	
5	**Verdict: pass (2 minors, 1 nit).** The service date on the Step 3 charge card equals what the letter prints on all three cases. The statement date is labeled "statement dated" wherever a charge card shows one, with one gap on uncounted ledger lines.
6	
7	- case_09: card "Date of service February 2, 2026 · statement dated March 1, 2026". Letter: "Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00". Match.
8	- lib10: all four charges show "Date of service June 9–12, 2026 · statement dated June 19, 2026". Letter prints "June 9–12, 2026" on each line. Match.
9	- lib11: ED line "Date of service March 18, 2026" (no statement label, correct for a dated visit note). Counted ledger lines show "(statement dated June 15, 2026; service date not stated)" in the Step 3 done list, on revisit, and in the letter. Match.
10	- Confirm note: the fixture set has no bill with a doubtful date, so no real note appeared on any of the three cases. I rendered all 7 backend reasons by rewriting only `service_date` in the GET case response (the worker's own method). The note shows in the card foot, in plain words, visible without scrolling at 1440x900, and says what the letter will do and what to do. Wording gaps are in the findings. Grade-only-the-display applies; T-202 r3 may change which lines are certain.
11	
12	```json
13	{"card": "T-205", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
14	 "scope": "commit 203ac6a (git archive extracted to session scratchpad a203/); app http://127.0.0.1:7981 demo mode (fixture backend, curated set, ZLAYT_MODE=local, health demo_mode true); case_09 (POST /api/cases with golden text, opened in UI), lib10 and lib11 (library tile). Display only; T-202 r3 parse changes not graded. Private values seen: 0.",
15	 "exercised": ["Read personas/paralegal.md, board show T-205 (handoff), D-071 and its amendment/clarification in memory/ORCHESTRATOR_DECISIONS.md:84-92, git show 203ac6a (step3.js/css diff)",
16	  "git archive 203ac6a into scratchpad a203; started server on 7981; health check demo_mode true; later killed PID 63090 and confirmed lsof exit 1 and curl 000",
17	  "artifacts/review-evidence/T-205-paralegal/p01.py via h.py: for case_09, lib10, lib11 did Step 2 by keyboard, walked every Step 3 card (DOM probe of service-date-text, statement-date, confirm-note, card text), counted charges, Step 4 download of letter and notes; output p01.out, letters ui-*-letter.txt, ui-*-notes.txt",
18	  "api.py / api.out: GET /api/cases/{token} amounts[].service_date for all three cases next to the record date",
19	  "p02_notes.py / p02.out: all 7 confirm_note reasons rendered on case_09 a1 and lib10 a2 with service_date stubbed in the GET response (fixtures have no real doubtful-date bill); measured note position vs viewport; screenshots note-lib10-ambiguous_numeric.png, note-lib10-no_date.png",
20	  "p03_revisit.py / p03.out: revisited counted lib11 a2 and a1; screenshots lib11-revisit-a2.png, lib11-s3-01-a2.png (pre-count card)",
21	  "Compared Step 3 date text with letter lines by grep (case_09 line 21, lib10 lines 37-44, lib11 lines 37-44); console/http errors: none (ERRORS count 0 in p01/p02/p03 outputs)"],
22	 "verdict": "pass",
23	 "scores": {"verify_quickly": 4, "step3_date_matches_letter": 5, "statement_date_labeled": 4, "confirm_note_plain_and_actionable": 3},
24	 "findings": [
25	  {"severity": "minor", "title": "Uncounted lib11 ledger lines show the statement date bare, with no Date of service line and no 'statement dated' label",
26	   "evidence": "p01.out:200 (PROBE lib11 a2): card 'Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 / $250.00 / The line states no date of service...', svc null; same for a3, a4. Screenshot artifacts/review-evidence/T-205-paralegal/lib11-s3-01-a2.png (card head and source head read 'June 15, 2026'). After counting, the same line reads 'statement dated June 15, 2026' (p03.out:2, lib11-revisit-a2.png) and the letter prints '(statement dated June 15, 2026; service date not stated)' (ui-lib11-letter.txt:39). sdOf in app/frontend/guided/step3.js requires kind === 'charge', and an uncounted ledger line is kind unclear, so service_date is null (api.out lib11 a5 shows the same for unclear rows).",
27	   "why_it_matters": "Those are the lines I am most careful with. Before I count them the card shows a bare June 15, 2026 in two places, which reads like a date of service, and it differs from what the letter will print. The body sentence says no date of service, so the risk is low, but the label I was asked to check is missing on this state. Never-counted UB-04 and ledger cards (lib10 a1/a6, lib11 a5-a8) show a bare record date too, though those carry no service-date claim.",
28	   "fix": "Apply the same 'statement dated X' wording to the card head, source head and sub for any amount whose record is a bill document (ledger, invoice, UB-04, billing statement), whatever its kind, and show the letter's not-stated text as the Date of service line on a countable ledger line before it is counted.",
29	   "acceptance_test": "E2E on lib11 a2 before counting: card head and src-head contain 'statement dated June 15, 2026', no bare 'June 15, 2026' without that prefix; the card shows '(statement dated June 15, 2026; service date not stated)' and it equals the text the letter prints after counting."},
30	  {"severity": "minor", "title": "The confirm note says to confirm the date but gives me nowhere to use it",
31	   "evidence": "p02.out:2 (and 16 variants): note text ends 'The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.' The card offers only 'Yes, count it' / 'No, don't count it' / 'Decide later'; screenshot note-lib10-ambiguous_numeric.png. The note does not say what to do once I have confirmed: add the date by hand in the Word letter, ask for the bill, or just count it.",
32	   "why_it_matters": "Plain wording and placement are good, but the instruction is half of one: I confirm the date from the highlighted words, and then the tool cannot take it and the letter still prints none. I need one sentence of next step so I do not guess.",
33	   "fix": "Append the next step to confirm_note, e.g. 'Counting the charge keeps it in the total; type the date into your letter yourself, or request the itemized bill.' Or tell me this tool cannot record a confirmed date.",
34	   "acceptance_test": "Unit test on service_date.confirm_note for all 7 reasons: each ends with a sentence naming the next action (not just 'confirm'); E2E asserts the foot note shows it beside the quote."},
35	  {"severity": "nit", "title": "Two notes say 'the code' to a paralegal",
36	   "evidence": "p02.out:3-4: 'The date 04/05/26 has a two-digit year, which the code does not guess.' and 'The date April 5 states no year, which the code does not borrow from the statement.' (app/backend/service_date.py _WHY).",
37	   "why_it_matters": "I do not know which code is meant; 'the tool' or no subject reads the same and is clearer.",
38	   "fix": "Reword: 'a two-digit year, which is not guessed' / 'no year, which is not taken from the statement date'.",
39	   "acceptance_test": "Unit test: no confirm_note contains the word 'code'."}
40	 ],
41	 "whats_right": ["Date of service on the Step 3 card is the letter's own text on case_09, lib10 and lib11 (period 'June 9–12, 2026' kept as a range), and the done-list column is now 'Date of service'.",
42	  "'statement dated March 1, 2026' / 'June 19, 2026' is named as a statement date in the card head, the Date of service line and the source head; the ED visit date is left unlabeled, correctly.",
43	  "The note sits in the card foot under the highlighted quote, is visible without scrolling, keeps Yes/No enabled, and states the letter will print no date."],
44	 "questions_for_chris": []}
45	```
46	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:09.697Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-206 2>&1 | tail -80; git log --oneline -3; git cat-file -t 79714c6"
}
````

### User / tool · 2026-11-03T00:43:09.857Z

**tool result**
````
---
id: "T-206"
title: "Step 3: uncounted ledger lines show a bare statement date (lib11 June 15) - label it 'statement dated'; confirm note says what to do next"
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T00:37:00Z"
updated_at: "2026-11-03T00:43:03Z"
claimed_by: "frontend"
claimed_at: "2026-11-03T00:37:14Z"
rounds: 0
commits: ["79714c6"]
reviews: []
ac:
  - {"n": 1, "text": "no bare date on any Step 3 charge card that is not a certain service date; the confirm note names the next action (check the quote, then Count or Fix the date); e2e on lib11", "done": true, "evidence": "tests/e2e/guided/test_t206.py (4 tests; 3 fail on HEAD step3.js, pass now); git archive of the commit tree: tests/e2e/guided + test_no_console_errors 147 passed, E2E_REQUIRE_DB=1"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T00:37:14Z frontend: claimed
- 2026-11-03T00:41:18Z frontend: Implemented: statement dated label for count/bill-document amounts (stmtDated), confirm-next sentence, tests/e2e/guided/test_t206.py (fails on HEAD, passes with change). Running guided suite + no_console_errors from git archive.
- 2026-11-03T00:42:59Z frontend: AC 1 checked: tests/e2e/guided/test_t206.py (4 tests; 3 fail on HEAD step3.js, pass now); git archive of the commit tree: tests/e2e/guided + test_no_console_errors 147 passed, E2E_REQUIRE_DB=1
- 2026-11-03T00:42:59Z frontend: moved in_progress -> in_review
- 2026-11-03T00:43:03Z orchestrator: review dispatched: paralegal-reviewer

## Handoff
What changed: step3.js stmtDated(): a record date reads 'statement dated X' (card head, line-sub, src-head) unless the amount has a certain service date; uncounted ledger lines (lib11 a2-a4) and any amount from a bill document source (ledger/invoice/UB-04/statement...) are labelled; sdOf reads service_date as api.md documents on any kind. New confirm-next sentence under the confirm note: 'check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself.' css: .svc-next. · Verified: tests/e2e/guided/test_t206.py; fresh git archive of the commit tree, E2E_REQUIRE_DB=1: guided suite + test_no_console_errors 147 passed. · Left: Step 3 has no control to fix or type a date, so 'Fix the date' is not promised; the note names the real buttons. If T-202 r3 adds one, change confirmNext. Never-counted amounts from non-bill records (visit-note rates) keep a plain date. · Surprised: other workers' dirty input.js/review.js/switcher.js are in the tree, so the commit used a temp index from HEAD (79714c6).

79714c6 feat(frontend): T-206 Step 3 names a bill document's date 'statement dated'; confirm note says what to do next
d23687e chore(guard): block git commit-tree and symbolic-ref (T-204 swapped a commit on HEAD by plumbing)
9b37b9c feat(frontend): no AI-worded fallback for a prepared item; refusal follows a late library (T-204)
commit
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:10.229Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t200-undated-charge-label.md"
}
````

### User / tool · 2026-11-03T00:43:10.234Z

**tool result**
````
1	---
2	name: t200-undated-charge-label
3	description: T-200 (bd72d5b) pass: counted undated lib11 ledger lines print "(statement dated June 15, 2026; service date not stated)"; D-071 binds that form; minors = notes silent, no count-walk eval
4	metadata:
5	  type: project
6	---
7	
8	T-200 review (reviews/T-200-paralegal.md, bd72d5b): pass, 2 minors + 1 nit. My T-181 r2 letter-date major is closed.
9	- D-071 (ORCHESTRATOR_DECISIONS.md:84) makes the T-200 wording binding for undated charges and moves dated charge lines (statement date vs service date: case_09, lib14, lib10) to another card. Grade that card on per-line service dates and period ranges.
10	- Open minors: the internal notes say nothing about counted charges that have no date of service (no "request dated itemized bill"). letter_check walks accept only, never D-064 count, so no eval produces the line.
11	- Mechanics: "demo mode" means a fixture backend; ZLAYT_MODE=local is still demo_mode true and gives /api/library. Reuse artifacts/review-evidence/T-200-paralegal/h.py + p01_lib11.py (port 7963, about 26 s end to end). The draft-then-cp flow with T-116-paralegal-r2-jsoncheck.py worked.
12	
13	**Why:** next round on the D-071 card, check the dated lines against the D-071 rules above.
14	**How to apply:** related [[t181-r2-patterns]], [[reviewer-run-pitfalls-pass4]].
15	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:12.653Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-205-paralegal/ | head -40; cat artifacts/review-evidence/T-205-paralegal/h.py; cat artifacts/review-evidence/T-205-paralegal/p01.py | head -120; cat docs/RUNBOOK.md | grep -n -i -E \"demo|port|ZLAYT\" | head -30"
}
````

### User / tool · 2026-11-03T00:43:12.793Z

**tool result**
````
api.out
api.py
case_09-s3-00-a1.png
case_09-step2-done.png
case_09-step3-done.png
case_09-step4.png
h.py
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
lib11-revisit-a1.png
lib11-revisit-a2.png
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
note-lib10-ambiguous_numeric.png
note-lib10-no_date.png
p01.out
p01.py
p02.out
p02_notes.py
"""T-200 paralegal review helper (copied from T-181 r2): persistent Chromium profile on the archive app (bd72d5b, demo/fixture, local mode, port 7963).

Usage: .venv/bin/python -I artifacts/review-evidence/T-200-paralegal/h.py <step-script.py>
The step script gets `pg` (page), `shot(name)`, `dump(label)`, `log(...)`, `BASE`, `OUT` in its globals.
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7981")  # T-202 r2: 986fc55 archive, port 7976
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
"""T-202 r2 paralegal (copied from r1): 986fc55 archive, demo/fixture backend, local mode, port 7976.
For each case (env CASES, default sample,case_09,lib14,lib10): open it as a user (sample tile / paste / library), draft, Step 2 accept with the
keyboard (compare box ticked where asked), Step 3 accept every bill item and tick 'count' boxes where offered, Step 4 download letter + notes.
Run: .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/h.py artifacts/review-evidence/T-202-paralegal/p01_cases.py
"""
import os
import re
import json

CASES = os.environ.get("CASES", "case_09,lib10,lib11").split(",")
PASTE = {"case_09": "/Users/arsis/zlayt-pm-project/evals/golden/case_09_nonvisit_hides_gap.txt"}
LIB = {"lib14": "case_lib14_handwritten_chiro_scans", "lib10": "case_lib10_eob_ub04_cms1500", "lib11": "case_lib11_priors_and_ledger"}


def iid():
    m = re.search(r"item=([^&]+)", pg.url)
    return m.group(1) if m else None


def card():
    return pg.evaluate("() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }")


for name in CASES:
    T0 = time.time()
    pg.goto(BASE + "/new")
    pg.wait_for_selector("[data-testid=view][data-ready]")
    if name == "sample":
        pg.click("[data-testid=tile-sample]")
    elif name in PASTE:
        # demo UI turns the paste tile off (step1.js:40 off: demo); the API accepts the golden text (201), so create it there and open it in the UI
        import json, urllib.request
        req = urllib.request.Request(BASE + "/api/cases", data=json.dumps({"text": open(PASTE[name]).read()}).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        tok = json.loads(urllib.request.urlopen(req, timeout=20).read())["token"]
        log(f"[{name}] created via POST /api/cases token={tok}")
        pg.goto(f"{BASE}/case/{tok}/records")
        pg.wait_for_selector("[data-testid=view][data-ready]")
        pg.wait_for_timeout(500)
    else:
        pg.click("[data-testid=tile-library]")
        pg.wait_for_timeout(300)
        pg.check(f"[data-testid=library-{LIB[name]}]")
    pg.wait_for_timeout(300)
    if name not in PASTE:
        pg.click("[data-testid=btn-read]")
    pg.wait_for_selector("[data-testid=btn-draft]", timeout=20000)
    pg.wait_for_timeout(300)
    pg.click("[data-testid=btn-draft]")
    for i in range(120):
        pg.wait_for_timeout(250)
        if pg.query_selector("text=Go to step 2") or "/timeline" in pg.url:
            break
    log(f"[{name}] draft took", round(time.time() - T0, 1), "s")
    if "/timeline" not in pg.url:
        pg.get_by_text("Go to step 2").first.click()
        pg.wait_for_selector("[data-testid=view][data-ready]")
    pg.wait_for_timeout(500)
    # Step 2
    for step in range(60):
        i = iid()
        if not i or "/timeline" not in pg.url:
            break
        yes = pg.query_selector("[data-testid=answer-yes]")
        yd = yes.is_disabled() if yes else None
        cmp_box = pg.query_selector("[data-testid=check-compare]")
        radios = pg.query_selector_all("input[type=radio]")
        log(f"[{name}] s2 item={i} yes_disabled={yd} compare={bool(cmp_box)} radios={len(radios)} :: {card().replace(chr(10), ' / ')[:300]}")
        if radios and pg.query_selector("button:has-text('Confirm date')"):
            radios[0].check(); pg.wait_for_timeout(200)
            pg.get_by_role("button", name="Confirm date").click(); pg.wait_for_timeout(600)
            log(f"[{name}]   confirmed first date reading")
            continue
        if cmp_box:
            pg.keyboard.press("a"); pg.wait_for_timeout(200)
            pg.keyboard.press("Space"); pg.wait_for_timeout(200)
            pg.keyboard.press("a")
        elif yd:
            pg.keyboard.press("d")
        else:
            pg.keyboard.press("a")
        pg.wait_for_timeout(450)
        if iid() == i:
            pg.keyboard.press("j"); pg.wait_for_timeout(300)
            if iid() == i:
                break
    shot(f"{name}-step2-done", full=True)
    if "/timeline" in pg.url:
        pg.click("[data-testid=btn-next-step]")
        pg.wait_for_selector("[data-testid=view][data-ready]")
        pg.wait_for_timeout(500)
    # Step 3
    seen = {}
    for step in range(40):
        i = iid()
        if not i or "/bills" not in pg.url:
            break
        seen[i] = seen.get(i, 0) + 1
        if seen[i] > 3:
            break
        boxes = [b.get_attribute("data-testid") for b in pg.query_selector_all("input[type=checkbox]") if b.is_visible()]
        log(f"[{name}] s3 item={i} boxes={boxes} :: {card().replace(chr(10), ' / ')}")
        probe = pg.evaluate("""() => { const q = (s) => { const e = document.querySelector(s); return e ? e.innerText : null; };
          const sub = document.querySelector('.work .card .card-h, .work .card .sub');
          return {svc: q('[data-testid=service-date-text]'), svcState: (document.querySelector('[data-testid=service-date]')||{getAttribute:()=>null}).getAttribute('data-state'), stmt: q('[data-testid=statement-date]'), note: q('[data-testid=confirm-note]'), figure: q('[data-testid=figure]'), noteRole: (document.querySelector('[data-testid=confirm-note]')||{getAttribute:()=>null}).getAttribute('role'), yesLabel: q('[data-testid=answer-yes]'), card: (document.querySelectorAll('.work .card')[document.querySelectorAll('.work .card').length-1]||{innerText:''}).innerText}; }""")
        log(f"[{name}] PROBE item={i} " + json.dumps(probe))
        pg.evaluate("() => { const c = document.querySelector('[data-testid=confirm-note]'); if (c) c.scrollIntoView(); }")
        shot(f"{name}-s3-{step:02d}-{i}")
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
    dump(f"[{name}] step 3 done")
    shot(f"{name}-step3-done", full=True)
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
11:Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
12:We restored those and gave the board and app their own ports so nothing of yours was clobbered.
21:- Or on the Mac: `touch ~/zlayt-pm-project/board/STOP`.
22:- **Resume after STOP:** from the phone, type into this Claude session (Remote Control): "Delete board/STOP and continue the loop." On the Mac: `rm ~/zlayt-pm-project/board/STOP`, then continue the session.
25:1. `cd ~/zlayt-pm-project`
26:2. Board server: `./tools/serve_board.sh` (also installs the native git pre-commit secret scan if missing) (tmux session `zlayt`, window `board`). Check: `curl -s localhost:7777/healthz`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:12.795Z

**tool call — Bash**
````
{
 "command": "git show 79714c6 --stat | head; git show 79714c6 -- app/frontend/guided/step3.js | head -150"
}
````

### User / tool · 2026-11-03T00:43:12.949Z

**tool result**
````
commit 79714c638066c01400784eba7cfbcbf5d35ba275
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 18:42:28 2026 -0600

    feat(frontend): T-206 Step 3 names a bill document's date 'statement dated'; confirm note says what to do next
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 .../frontend/project_t206_statement_label.md       | 12 +++
 app/frontend/guided/step3.css                      |  1 +
commit 79714c638066c01400784eba7cfbcbf5d35ba275
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 18:42:28 2026 -0600

    feat(frontend): T-206 Step 3 names a bill document's date 'statement dated'; confirm note says what to do next
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/guided/step3.js b/app/frontend/guided/step3.js
index fa0bf20..989e21f 100644
--- a/app/frontend/guided/step3.js
+++ b/app/frontend/guided/step3.js
@@ -16,10 +16,13 @@
   const cents = (a) => (a.value_cents == null ? null : a.value_cents);
   const hasDollar = (t) => /\$\s*\d|\d\s*(?:USD|dollars)/i.test(t || "");
   /* T-205 (D-071): a charge's date is the service date the letter prints (amounts[].service_date.text, byte for byte); the record's own date is called the statement date whenever it is not that day. Code only, no guessing. */
-  const sdOf = (a) => (a && a.kind === "charge" && a.service_date && typeof a.service_date === "object" ? a.service_date : null);
+  const sdOf = (a) => (a && a.service_date && typeof a.service_date === "object" ? a.service_date : null);
   const stmtOnly = (sd) => !!sd && !!sd.statement_date_iso && !(sd.state === "stated" && sd.date_iso === sd.statement_date_iso && !sd.end_iso);      // a bill's date, not the day of the service
-  const recDate = (r, sd) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || ""; return d ? (stmtOnly(sd) ? "statement dated " + d : d) : "no date"; };
-  const recLabel = (r, sd) => `Record ${r.seq} · ${r.source_label || "Record"} · ${recDate(r, sd)}`;
+  /* T-206: a record's date is shown bare only when it is a certain service date. An amount with no service_date of its own (a ledger line not counted yet, a UB-04 or invoice total) never has one: a bill document's date is its statement's. */
+  const BILL_DOC = /\b(ledger|invoice|statement|UB-?04|CMS-?1500|HCFA|EOB|explanation of benefits|itemi[sz]ed|billing|bill)\b/i;
+  const stmtDated = (item, sd, rec) => stmtOnly(sd) || (!sd && !!item && (kindOf(item) === "count" || BILL_DOC.test((rec && rec.source_label) || "")));
+  const recDate = (r, st) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || ""; return d ? (st ? "statement dated " + d : d) : "no date"; };
+  const recLabel = (r, st) => `Record ${r.seq} · ${r.source_label || "Record"} · ${recDate(r, st)}`;
   const figure = (a) => (cents(a) != null ? R.money(cents(a)) : a.text || "");
   const FLAG_BOX = { likely_duplicate: "I checked: this is a separate charge, not the same one counted twice.", likely_total: "I checked: this is a charge of its own, not a total of the others." };
   const flagBox = (f) => FLAG_BOX[f.flag] || `I checked: ${String(f.name || f.flag || "this is right").replace(/\.$/, "")}.`;
@@ -29,14 +32,16 @@
     h("span", { class: "label-cap" }, "Date of service"), " ", h("b", { "data-testid": "service-date-text" }, sd.text || ""),
     sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · statement dated ${R.longDate(sd.statement_date_iso)}`) : null);
   const confirmNote = (sd) => h("strong", { class: "svc-note", role: "note", "data-testid": "confirm-note" }, R.plain(sd.confirm_note));
+  /* T-206: the note says what to do next, with the buttons this card really has (it has no control to type a date, so the letter keeps "not stated" and she adds the date herself) */
+  const confirmNext = () => h("p", { class: "svc-next", "data-testid": "confirm-next" }, h("b", {}, "What to do: "), "check the date in the highlighted words, then press ", h("b", {}, "Yes, count it"), " or ", h("b", {}, "No, don't count it"), ". If you count it, type the date into your letter yourself.");
 
   function present(S, item) {
     const kind = kindOf(item), recs = (item.record_ids || []).map((id) => S.record(id)).filter(Boolean), rec = recs[0];
-    const sd = sdOf(item);
+    const sd = sdOf(item), st = stmtDated(item, sd, rec);
     const marks = item.excerpt_start != null ? [[item.excerpt_start, item.excerpt_end]] : [];
-    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, sd) : null }));
-    const src = { head: many ? "Records " + recs.slice(0, -1).map((r) => r.seq).join(", ") + " and " + recs[recs.length - 1].seq : rec ? recLabel(rec, sd) : "", nodes: srcNodes };
-    const sub = rec ? [rec.source_label, rec.date_iso ? (stmtOnly(sd) ? "statement dated " + R.longDate(rec.date_iso) : R.longDate(rec.date_iso)) : rec.date_raw].filter(Boolean).join(" · ") : "";
+    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, stmtDated(item, sd, r)) : null }));
+    const src = { head: many ? "Records " + recs.slice(0, -1).map((r) => r.seq).join(", ") + " and " + recs[recs.length - 1].seq : rec ? recLabel(rec, st) : "", nodes: srcNodes };
+    const sub = rec ? [rec.source_label, rec.date_iso ? (st ? "statement dated " + R.longDate(rec.date_iso) : R.longDate(rec.date_iso)) : rec.date_raw].filter(Boolean).join(" · ") : "";
     const disp = R.dispute(item) || (S.forceCompare.get(item.id) || null);
     const decided = item.review_status === "accepted" || item.review_status === "dismissed" || item.review_status === "edited";
     const flag = item.flag && item.confirm_required ? item.flag : null;
@@ -55,7 +60,7 @@
       }
       return { tag: { cls: "ok", text: "Charge" }, sub, src,
         body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), sd ? dateLine(sd) : null, h("p", { class: "explain muted gap-top" }, "Written in the record as ", h("b", {}, item.text || ""), "."), note],
-        foot: sd && sd.confirm_note ? { cls: "attn", nodes: [confirmNote(sd), ...(foot.length ? [h("div", { class: "gap-top" }, ...foot)] : [])] } : { cls, nodes: foot },          // T-205: the date is not certain: the note leads the foot, in plain words, under the highlighted quote
+        foot: sd && sd.confirm_note ? { cls: "attn", nodes: [confirmNote(sd), confirmNext(), ...(foot.length ? [h("div", { class: "gap-top" }, ...foot)] : [])] } : { cls, nodes: foot },          // T-205: the date is not certain: the note leads the foot, in plain words, under the highlighted quote
         question: "Should this charge count toward the bill total?",
         yes: { label: "Yes, count it", disabled: () => (!!flag && !ticked("flag")) || (!!disp && !ticked("compare")),
           run: () => S.decide(item, "accept", { ...(flag ? { confirm: flag.confirm_with } : {}), ...(disp && ticked("compare") ? { compared: true } : {}) }) },
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:17.328Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/a206 && git archive 79714c6 | tar -x -C $S/a206 && ls $S/a206 | head -30; cat tools/serve_app.sh 2>/dev/null | head -30; cat memory/reviewer-run-pitfalls-pass4.md 2>/dev/null | head -5; cat .claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md; ls artifacts/review-evidence/T-205-paralegal/*.sh 2>/dev/null; grep -rn \"demo\" docs/RUNBOOK.md | head"
}
````

### User / tool · 2026-11-03T00:43:18.516Z

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
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
---
name: reviewer-run-pitfalls-pass4
description: T-060/T-114 pass-4 run pitfalls: HEAD moves mid-review (pin by hash, run both if brief says HEAD and card names a commit); venv path relative from subdirs (exit 127); sed -i blocked again; Playwright selectors for case list, disclosure, confirm-date radios; reload restores the case
metadata:
  type: reference
---

- HEAD moved during the review: 433ac1c became f7829c1 while I worked (other agents commit). Record the hash you archived with `git rev-parse --short HEAD` at the start AND `git archive <hash>`. When the brief says HEAD and the card names a commit (e293daa), run both and say which commit each finding applies to. Check `git diff --stat <card-commit> HEAD -- app/frontend` (empty = same UI).
- Server launch: `env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch db> PORT=<p> HOST=127.0.0.1 .venv/bin/python -I artifacts/review-evidence/<card>-paralegal-pass4-serve.py <archive_root>` (runpy, puts the archive root first on sys.path). Background launch: the launcher task exits 0 while the listener lives; get the listener PID with `lsof -iTCP:<p> -sTCP:LISTEN -nP`, kill by number, confirm curl = 000. Port 7860 is the live dev app; never touch it.
- `.venv/bin/python` is relative: from artifacts/review-evidence/<card>/ it exits 127. Run from repo root.
- `sed -i` is refused by board-guard again (pass 4). Use the Edit tool on scripts and memory; check `grep -c` after.
- Playwright selectors (e293daa/HEAD): case list buttons are `[data-testid=case-<token>]`; library entries `[data-testid=library-case_lib09_spanish_interpreter_espalda]` sit inside a collapsed disclosure: click `summary:has-text('synthetic library')` first. The lib09 names repeat ("Spanish-language records, back pain") and differ only by token: never pick by name. Date step: `button:has-text('1 date to confirm')`; radios via `get_by_label("March 5, 2026")`; confirm `get_by_role("button", name="Confirm date")`; there is NO `form[data-testid=confirm-date]` in this build. Gap notice `[data-testid=gap-change-note]`; dismiss it `[data-testid=btn-dismiss-gap-note]`. Dismissed entries group `[data-testid=dismissed-summary]`. Export `[data-testid=btn-export]`, letter `[data-testid=export-letter]` (a PRE, read innerText not value), copy `[data-testid=btn-copy-letter]`, download `[data-testid=btn-download-letter]`.
- Keyboard: `a` on a flag or amount acts on it; `d` on a flag dismisses without a reason prompt; `e` opens the textarea only when focus is on the row, and Ctrl+Enter saves.
- Reload restores the last case view (no paste page), so a probe that expects the paste box after reload will time out. Use the case list or continue on the restored case.
- Output discipline: write every probe's output with `> file` in the same call; console-only numbers do not count as evidence when the review quotes them.
- Review files are write-once: proofread every line reference with grep before the single Write (api.md:341 D-045b checked; the erratum route is the final reply).

Why: all of these cost a probe rerun or an unfixable review line during the T-060/T-114 pass-4 run.
How to apply: start each Playwright run with `curl` on the port, confirm the archive hash, and keep one helper module per card. Related: [[reviewer-tooling-quirks]], [[reviewer-api-shape-gotchas]], [[t060-pass4-state-patterns]], [[t114-r3-gap-change-persistence]].
docs/RUNBOOK.md:8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:19.897Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/*serve*.py | head; mkdir -p artifacts/review-evidence/T-206-paralegal; cat artifacts/review-evidence/T-205-paralegal/p02_notes.py | head -80"
}
````

### User / tool · 2026-11-03T00:43:19.991Z

**tool result**
````
artifacts/review-evidence/T-060-paralegal-pass4-serve.py
"""T-205 paralegal: render every confirm_note reason in the Step 3 card (stub of GET /api/cases/{token} service_date only, as the worker's own test does;
the fixture set has no bill that parses to a doubtful date). Wording is the backend's own SD.confirm_note. Run via h.py."""
import json, re, sys
sys.path.insert(0, "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a203")
from app.backend import service_date as SD
TOK = {"case_09": ("Rb_-aRcu7JXIMZ90rAiyHA", "a1", "2026-03-01"), "lib10": ("_HdnjAt2eCEWDdnvroHTEw", "a2", "2026-06-19")}
RAW = {"ambiguous_numeric": "04/05/2026", "two_digit_year": "04/05/26", "no_year": "April 5", "invalid": "02/30/2026", "several_dates": "06/24/2026 and 07/08/2026",
       "non_service_date": "03/01/2026", "no_date": ""}
for case, (tok, aid, stmt) in TOK.items():
    for reason, raw in RAW.items():
        sd = {"state": "not_stated", "date_iso": None, "end_iso": None, "reason": reason, "text": SD.not_stated_text(stmt), "statement_date_iso": stmt, "confirm_note": SD.confirm_note(reason, raw)}
        def mk(sd, aid):
            def rewrite(route):
                r = route.fetch(); body = r.json()
                for x in body.get("amounts", []):
                    if x["id"] == aid:
                        x["service_date"] = sd
                route.fulfill(response=r, json=body)
            return rewrite
        rewrite = mk(sd, aid)
        pat = re.compile(rf"/api/cases/{tok}(\?.*)?$")
        pg.route(pat, rewrite)
        pg.goto(f"{BASE}/case/{tok}/bills?item={aid}")
        pg.wait_for_selector("[data-testid=view][data-ready]")
        pg.wait_for_selector("[data-testid=confirm-note]", timeout=8000)
        pg.wait_for_timeout(300)
        info = pg.evaluate("""() => { const n = document.querySelector('[data-testid=confirm-note]'); const r = n.getBoundingClientRect();
          const y = document.querySelector('[data-testid=answer-yes]').getBoundingClientRect();
          return {note: n.innerText, noteTop: Math.round(r.top), noteBottom: Math.round(r.bottom), vh: innerHeight, yesTop: Math.round(y.top), svc: document.querySelector('[data-testid=service-date]').innerText,
                  head: (document.querySelector('[data-testid=src-head]')||{innerText:''}).innerText, tag: (document.querySelector('.work .card')||{innerText:''}).innerText.split('\\n')[0]}; }""")
        log(f"[{case}/{reason}] " + json.dumps(info, ensure_ascii=False))
        if reason in ("ambiguous_numeric", "no_date") and case == "lib10":
            shot(f"note-{case}-{reason}", full=False)
        pg.unroute(pat)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:22.709Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-060-paralegal-pass4-serve.py; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls $S; lsof -iTCP:7990 -sTCP:LISTEN -nP; echo rc $?"
}
````

### User / tool · 2026-11-03T00:43:23.034Z

**tool result**
````
"""Start the app from a git-archive copy (commit e293daa) for the paralegal pass-4 / T-114 r3 review.

Usage (env vars set by the caller: LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch db> PORT=7897 HOST=127.0.0.1):
    .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py <archive_root>
Runs under -I (isolated), so the archive root is put first on sys.path explicitly.
"""
import os
import runpy
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
runpy.run_module("app.main", run_name="__main__")
641ed.bak
CLAUDE.md
GATEM3_se
M1
M1_nocombine
M2
M2_find0
MASTER_PROMPT.md
T-047-run1.json
T-060-pass2-head
T-093-r3-2ab7896
T-093-r3-run.py.orig
T-093-r3-scripts
T-093-r4-3223e50
T-093-r4-mutA
T-093-r4-mutB
T-109-probe
T-109-r1-card
T-109-r1-head
T-109-unit-head.txt
T-124-r1-head
T-124-r1-mut2
T-124-r1-parent
T-133-r1-archive
T-133-r1-source
T-133-r3-archive-4065ef2
T-133-r3-archive-f939ccb
T-133-r3-mutA
T-133-r3-mutB
T-133-r3-mutC
T-133-r3-mutD
T-133-r3-scripts
T-133-r4-archive-head
T-133-r5-13d.py
T-133-r5-15be212
T-133-r5-6fa8ecc
T-133-r5-head
T-133-r5-mut-backslash
T-133-r5-parent
T-133-r5-parse.py
T-133-r5-pmh.py
T-133-r5-probe.py
T-133-r5-r1
T-133-r5-unit-head.log
T-152-r1
T-157-r2-852b060
T-157-r2-full-unit.out
T-157-r2-mut
T-157-r2-mutants.out
T-157-r2-mutate.py
T-157-r2-parse.py
T-157-r2-probe.py
T-157-r2-probe2.py
T-157-r2-probe3-K.out
T-157-r2-probe3-base.out
T-157-r2-probe3.py
T-157-r2-probe4.py
T-157-r3-f31b146
T-157-r3-mut
T-157-r3-mutants.out
T-157-r3-mutate.py
T-160-r1
T-197-612dc2c
T-197-head
T-197-mutants
T-197-probe
T102_staff_r1
T102_staff_r2
T103_archive
T103_parent
T106_cli_out
T106_head_archive
T106_m_exportbranch
T106_m_hlreview
T106_m_hltrace
T106_m_pdfbypass
T106_m_pdfclaude
T106_m_rootcal
T106_r2_mut_a
T106_r2_mut_b
T106_r2_mut_c
T106_r2_mut_d
T106_r2_probe
T106_r2_suite.txt
T106_r2_suite_run2.txt
T106_r2_verify
T106_scripts
T106_unit_run1.log
T106_unit_run2_rs.log
T108_r2_clone
T108_r2_verify
T108_verify
T112_r1
T112_r1_scripts
T112_r2
T112_r3
T112_r3_mut
T112_r3_scripts
T113_r1_b66e748
T113_r1_b66e7481
T113_r1_e1ce8dc
T113_r1_evalout
T113_r1_fresh
T113_r1_head
T113_r2_arch
T113_r2_arch2
T113_r2_clone
T113_r2_probe
T113_r2_unit.log
T115_card_show.txt
T115_staff_r1
T115_staff_r2
T119_r2
T119_r3
T119_staff_r1
T120_r3_cli1.txt
T120_r3_cli2.txt
T120_r3_evals_head
T120_r3_evals_parent
T120_r3_fix
T120_r3_fixprobe.py
T120_r3_fprobe.py
T120_r3_head
T120_r3_mut
T120_r3_parent
T120_r3_probe_head.txt
T120_r3_probe_parent.txt
T120_r3_unit.txt
T128_9_127_r1
T128_9_r2
T128_9_r2b
T128r4_prev
T132r1
T132r1p
T132r3_arc
T132r3_cli1.err
T132r3_cli1.txt
T132r3_cli2.err
T132r3_cli2.txt
T132r3_cli_arc.txt
T132r3_cli_ctl.txt
T132r3_ctl
T132r3_mut
T133-r3-cli-1.txt
T133-r3-cli-2.txt
T133-r3-cli-r1.txt
T133-r3-negex.txt
T133-r3-pycontext-kb.yml
T133-r3-unit.log
T133-r4-arch-4065ef2
T133-r4-arch-e79c3aa
T133-r4-arch-parent
T133-r4-cli-reports.txt
T133-r4-clone
T133-r4-mutM1
T133-r4-mutM2
T133-r4-mutM3
T133-r4-pipeline-run1.txt
T133-r4-pipeline-run2.txt
T133-r4-record.json
T133-r4-scripts
T133-r4-suite-archive.txt
T133-r4-suite-clone.txt
T134r4_head
T134r4_head2db
T134r4_mut
T134r4_mut2
T134r4_src
T136_r1_e2e_full.txt
T136_r1_e2e_full2.txt
T136_r1_head
T136_r1_mutA
T136_r1_mutA.log
T136_r1_mutB1
T136_r1_mutB1.log
T136_r1_mutB2
T136_r1_mutB2.log
T136_r1_mutC
T136_r1_mutC.log
T136_r1_serve.sh
T136_r1_server.log
T136_r1_server2.log
T136_r1_unit.txt
T138r2_parent
T139_r1
T140_r1
T140_r2
T140_r3
T140_r4
T141_head
T141_mut
T141_pre
T141_preN2
T141_probe
T141_run
T141r2_head
T141r2_libreport.json
T141r2_mut2
T141r2_mutants.txt
T141r2_parent
T141r2_pk_T141_head.err
T141r2_pk_T141_head.json
T141r2_pk_T141_pre.err
T141r2_pk_T141_pre.json
T141r2_pk_T141r2_head.err
T141r2_pk_T141r2_head.json
T141r2_pl_orig.py
T141r3_head
T141r3_mut
T141r3_r2
T141r3_scripts
T141r4_head
T141r4_prev
T141r5_head
T141r5_mutA
T141r5_prev
T141r5_scripts
T141r6_824984f
T141r6_evidence
T141r6_head
T141r6_r5
T141r7_6379c0b
T141r7_824984f
T141r7_83f1afd
T141r7_acad4f6
T141r7_c2913a6
T141r7_head
T141r7_mut_guard2
T141r8_head_99438fb
T141r8_mutant_two_digit_off
T155_r1
T155r2_T164
T157r3
T159_161_r1
T162_r1
T162_r2
T162_r3
T167-mut
T167-r1-archive
T167-r1-out
T167-r1-out-local
T167-r1-out-local2
T168_r1
T169_staff_r1
T169_staff_r2
T179_r1
T179_r1_mut
T179_r2
T179_r2_mut
T196
T197_r2_9ab8cae
T197_r2_e425534
T197_r2_mut_both
T197_r2_mut_home
T197_r2_mut_none
T197_r2_mut_step1
T197_r2_scripts
T198-locate.py
T198-run1.txt
T198-run2.txt
T204_r1
__pycache__
_types.bak
a.sqlite3
a141
a178
a178.out
a201
a203
a206
a27e3a4.diff
a9ab
acc.py
across.py
addtags.py
adj_eval
adj_out
adr013.txt
after.py
all.txt
amounts_broken.py
ap3500.pdf
api
api.patch
api2
api_at_099732b.py
api_head.log
api_head.md
api_head.py
api_head.sqlite3
api_head_plus_mine.md
api_md_head.md
api_md_new.md
api_mine.md
api_new.py
api_parent.log
api_parent.sqlite3
apitmp
app
app-d0b04bc
app-head
app.log
app.pid
app.sqlite3
app2
app2.log
app2.pid
app2.sqlite3
app3
app3.sqlite3
app4
app4.log
app4.pid
app4.sqlite3
app5
app5.log
app5.pid
app5.sqlite3
app60
app60.log
app60.pid
app60.sqlite3
append_404.py
append_correction.py
ar2
ar_old
arc
arc.sh
arc2
arch
arch0c24
arch2
arch203r2
arch3
arch4
arch5
archB
arch_57a08ba
arch_head_r3b
arch_r2_54382
arch_r2_54382.idx
arch_r2b
arch_r2c
arch_r2d
arch_r3_final
arch_t140
archive
archpath.txt
artifacts
atk
aud.py
aud2.py
audit.py
audit_mine.js
audit_split.py
audited.bak
axe
b.sqlite3
base
base.err
base.json
base.txt
base1.log
baseline_journey.out
before.txt
big.json
billing.orig
bis1.txt
bis2.txt
bis3.txt
bis4.txt
blank.py
blob.tmp
board
body.py
bombs
boom_final.py
boom_server.py
boundary.py
boundary2.py
build_evidence.py
build_set.py
build_set.py.bak
build_t099_blobs.py
busy.out
c
c01.json
c1.json
c5.json
c8a9874
ca.sh
cal.bak
case.json
case.json.tok
case07.json
case3.json
case3.json.tok
case_01_date_formats.json
case_lib11_priors_and_ledger.json
case_list.orig.bak
cases.txt
ce70
ce70-report.md
census.py
charge_text.py.patch
charges.py
check.py
check_golden.out
check_json.py
check_r2.py
check_r3_json.py
check_r4.py
checks2.sh
checks3.sh
chk.js
chk.py
chk2.py
chk_mut.py
chk_syntax.py
clean2
clean3
clean4
clean5
clean5_unit.txt
clean_run1.txt
cleanup_check.py
cli1.out
cli2.out
cli_c1.err
cli_c1.txt
cli_final.err
cli_head_out.txt
cli_rep1.err
cli_rep2.err
cli_rep3.err
clone-run
clone194
cmscms.py
collapsed.png
collapsed.py
commit.sh
commit_paths.sh
commit_r3.sh
commit_tree
commitcases.txt
conf-1440.png
conf-390.png
conf_A.py
conf_B.py
conftest_mine.py
conftest_split.py
controls_run.log
copy
copyA
copyC
copy_untracked.py
corp_base.json
corp_r2.json
corpus.py
count.py
count1.py
count_base.py
counts.sh
cr.sh
cred_b05.py
cred_orig.py
cs.sh
ctl-out
ctl.log
d.py
d1
d2
d3
d4
d5
d6
d7
d8
data
data2
dates.orig
db
db3
db4
db5
dbg
dbg.png
dbg.py
dbg2.py
dbg3.png
dbg3.py
dbg4.py
dbg5.py
dbg97.py
de1.txt
decisions_head.md
demo
demo.log
demo.sqlite
dev
dev.db
diag.py
diff.py
dl
docker-venv
docker_emu.sh
docker_serve.log
docker_serve.pid
dockerctx
dockerdata
dockerhome
docs
dom.bak
dos
draft-pass2.md
drive.py
dump.py
e1-1440.png
e1-390.png
e1-390b.png
e1.py
e1400d4
e2.py
e2e-data
e2e-m1-server.log
e2e-m1.sqlite
e2e-run.sqlite
e2e-server.log
e2e.db
e2e.out
e2e1.log
e2e2.db
e2e2.out
e2e3.out
e2e_full.txt
e2e_full1.txt
e2e_full2.txt
edit133.py
edit133b.py
edit133r2.py
edit199.py
emptytree
endpoints.py
env97
err.out
err2.out
es1.txt
ev.json
ev.sh
eval_base.out
eval_r2.out
evalout
evalout2
evals
ex07.json
ex1.sh
ex2.sh
ex3.sh
exp-077
exp.py
exp2.py
exp_077.py
export.py.patch
export_curated.sqlite
export_recorded.sqlite
f3.out
f5f1be9-tree
fe-data
fe3.log
fe3.sqlite
fe4.log
fe4.sqlite
fetch
figs.py
files.txt
fill.py
final-data
final.py
final1
final1.log
final2.log
finalize_f5f1be9.py
find_miss.py
first.png
fix.log
fix.sqlite3
fixture_run.out
fixture_run_b.out
flags_commit.py
flip.out
flip.py
fpl.bak
fpl_new.py
fpl_old.py
fr_r2.txt
fragile
fresh
fresh.py
fresh_head.log
fresh_head.sqlite3
fresh_nosbs.log
fresh_nosbs.sqlite3
full.done
full.log
full.out
full.patch
full.txt
full2.out
full_head.txt
fx
fx.log
fx.sqlite3
fx_before.txt
fxbak
gate.db
gate_dir.txt
gate_m2
gen
gen.py
gen_controls.py
gm2
gm2r2
gm2r2_legal
gm2r2clone
gm3
gm3-7991.log
gm3-7992.log
gm3-a11y-arch
gm3-a11y-audit.log
gm3-a11y-pid.txt
gm3-a11y-server.log
gm3-a11y-wrap.py
gm3-a11y.sqlite3
gm3-emptyfx
gm3-ux-7991.sqlite3
gm3-ux-7992.sqlite3
gm3src
golden_scan.py
guardprobe.py
guardprobe.py.bak
h.txt
h178
h42.py
h60.txt
h_audit.js
h_charges.js
h_conftest.py
h_review.js
h_stepper.js
harness
head
head-a850be0
head-bc12d44
head-ec33bf0
head.db
head.log
head.py
head.sqlite3
head0
head2
head2.py
head3
head4
head5
head7
head8
head9
headA
head_950d4a5
head_9851a0d_r5
head_9c1af01
head_ae76835_r3
head_clean
head_clean.log
head_clean.sqlite3
head_copy
head_e63e564
head_faee448_r4
head_nosbs
head_nosbs.log
head_nosbs.sqlite3
head_run.sh
head_scan.txt
headcheck
headchk2
headfe
headx
heldout.py
helpers.py
helpers2.py
hf-config.html
hf-docker.html
hits.py
hookcopy
idx
idx162r3b
idx167
idx171
idx2
idx3
idx4
idx5
idx_commit
idx_r2b
idx_r2c
idx_r2d
idx_r3
idx_t139r4
idx_t139r4b
idxpath
image-emu
ing.bak
ingest.orig
ingest_novel.py
inj.py
jcheck.py
judge_live.py
judges.png
k1dump.py
kb2.py
kb3.py
kb_test.py
keys.py
last_commit
latest.before.sha
latest.committed.json
latest_head.json
latest_new.json
leak.py
letter_check.py.patch
lib-after.md
lib.md
lib.out
lib_app.sqlite
lib_report.md
lib_report3.md
lib_report5.md
libdump.py
library-after.md
library-base.md
library-report.md
link
live-demo
live-demo.log
live-local
live-local.log
live23.sh
live3.sh
llm_head.md
local
local.log
local.sqlite
m1.txt
m2.txt
m2regate-live.log
m3
m3.txt
m4
m4.txt
m5
m55_M_drop_whole_rule
m55_M_only_needs_review
m55_M_only_rejected
m58_M1_round1_regex
m58_M2_dates_iso_dollar
m58_M3_amounts_valid_dollar
m58_M4_fence_dollar
m59_N11_drop_stale_basis_clause
m59_N12_failed_redraft_overwrites
m59_N13_drop_SEVERITY_NOT_QUOTED
m59_N3_drop_D006_token_check
measure.py
memory
mine
mine.diff
mine.patch
mine.txt
miss.py
miss2.log
miss2.py
mk.py
mk_r3.sh
mkd.py
mkfix.py
mkindex171.sh
mkpatch.py
mkpdf.py
mkreview.py
mkreviews.py
mob.py
msg.txt
msg_r3.txt
mut-A
mut-B
mut-C
mut-D
mut-M6_drop_family_lookbehind
mut-base
mut-control
mut-gate
mut-qual
mut-t073-A-broad-catch
mut-t073-B-no-guard-in-review
mut-t073-C-expected-becomes-supported
mut-t073-D-drop-class
mut-t084-1-no-judge-gate
mut-t084-2-no-wording-gate
mut-t084-3-no-negation-gate
mut-t084-4-unsure-accepted
mut-t084-5-no-audit
mut-t084-6-no-value-gate
mut-t084-7-judge-fail-open
mut-tok
mut.py
mut.py.bak
mut080.py
mut1
mut105.py
mut105.py.bak
mut159.py
mut161.py
mut2
mut2.py
mut200.py
mut2_B0_pinned_baseline
mut2_G1_grounding_check_removed_in_extract
mut2_S1_judge_unavailable_fails_open_in_state
mut2_S2_judge1_error_becomes_supported
mut3
mut3_S2b_shared_judge_error_fails_open_to_supported
mut3_S3_j2_error_fails_open_to_agree_pipeline_only
mut4
mut98
mut99
mutB.txt
mutT132
mut_M0_baseline
mut_M1_noRollback
mut_M1_sdk_internal_retries_2
mut_M2
mut_M2_cli_drops_strict_mcp
mut_M3
mut_M3_cli_timeout_600
mut_M4
mut_M4_cli_leaks_stderr_into_error
mut_M5
mut_M5_fixture_miss_retried
mut_M6
mut_M6_j2_error_becomes_agree
mut_M7
mut_M7_stray_subprocess_import_outside_backends
mut_R4M1_stated_total_always_suppressed
mut_R4M2_no_other_figures_on_rate_holder
mut_R4M2_rate_unclear_move_to_other_figures_removed
mut_R4M3_rate_row_drops_own_other_figure_move
mut_R4M3_rate_row_stated_total_not_other_figure
mut_R4R_line790_raises
mut_branch
mut_branch.sqlite
mut_dedupe
mut_flagsdeadline
mut_guard_e2e.out
mut_guard_unit.out
mut_rmfixture
mut_rmjudgefixture
mut_run.py
mut_run2.py
mut_t055_M_drop_whole_rule
mut_t055_M_only_needs_review
mut_t055_M_only_rejected
mut_t058_M1_round1_regex
mut_t058_M2_dates_iso_dollar
mut_t058_M3_amounts_valid_dollar
mut_t058_M4_fence_dollar
mut_t059_N11_drop_stale_basis_clause
mut_t059_N12_failed_redraft_overwrites
mut_t059_N13_drop_SEVERITY_NOT_QUOTED
mut_t059_N3_drop_D006_token_check
mutant-M1-nocombine.txt
mutant-M2-find0.txt
mutant375_journey.out
mutant_timeline572.out
mutants
mutants-db08276.log
mutants-r3-db08276.log
mutants-work
mutants.py
mutate2.py
mutate3.py
mutate_api.py
mutate_run.py
mutate_run2.py
mutate_t055.py
mutate_t058.py
mutate_t059.py
mutrun.sh
mutv2_1
mutv2_2
mutv2_3
mutv2_4
mutv2_5
mutv2_6
mutv2_7
mvp95
mvp95.log
mvp95.pid
mvp95.sqlite3
mw
n.py
narr.py
neg
neg2
negex
negtest
new.err
new.json
new.txt
new2.json
new_record.py
novel.txt
nucc
nv.py
nv2.py
o1
o1.aIcW
o2
o2.vHBZ
o3_new.js
o3_v3.js
ocr_edit
ocr_edit_head
ocrinj
oe
oi
old-d0b04bc
old_unc.py
orch.idx
orig
out
out.txt
out_head.json
out_zlayt-pm-project.json
ov.py
overlay-head
own
p.py
p1.py
p1.txt
p2.db
p2.py
p2.txt
p3.log
p3.pid
p3.py
p3.sqlite3
p3.txt
p4-e293daa
p4-head
p5-b612176
p5-server.log
p5.db
p_be
p_fe
pa
page.txt
par
parent
parent-server.log
parent.sqlite3
part.py
part2-process.html
part2-process.pdf
paste.sqlite3
paste_attack_ledger.txt.sqlite
paste_synthetic_ledger.txt.sqlite
patch.py
patch2.py
patch3.py
patch_builder.py
path
path.txt
pathspec.txt
patterns.bak
patterns_copy
patterns_fresh
patterns_nomanual
pdb
pdf_time.py
pdfs
pdfs_head
peer.py
peer.sqlite3
personas
phi.py
pid
pid2
pidA
pidB
pin-690a0e3-r5
pin-6bca-r4
pin-8bc7f90
pin-HEAD-r4
pin-HEAD2-r4
pin-db08276
pin-f218263
pipeline.orig.py
pipeline.py
pipeline_commit.py
pl.orig
pm-gate.sqlite3
pn-head.md
pnh.html
pnh.pdf
portconflict.sh
pp
pp2
pr2_986fc55
pre
pre-t123-archive
pre_t095_schema.sql
present.patch
present.py
prev
probe
probe-db
probe-r2-output.txt
probe-top.png
probe.py
probe.sqlite3
probe133.py
probe133r2.py
probe133r3.py
probe2.py
probe2.py.bak
probe2_t067.py
probe3.py
probe3_t067.py
probe4.py
probe404.py
probe5.py
probe98
probe99
probeA
probeA.stderr
probeA.stdout
probeB
probeB.stderr
probeB.stdout
probe_404.py
probe_7df
probe_copy.sqlite3
probe_copy2.sqlite3
probe_copy3.sqlite3
probe_copy4.sqlite3
probe_copy5.sqlite3
probe_curated.sqlite
probe_err.log
probe_failed.py
probe_flags.sqlite
probe_flags_audit.sqlite
probe_head
probe_head_out.txt
probe_nojudge.py
probe_r4_ocr.py
probe_recorded.sqlite
probe_rej.py
probe_run.py
probe_server.log
probe_t067.py
probe_timeout.py
probe_tray.py
probe_work_head
probe_work_head2
probes
probes-t100
probes159
probes161
probes_r5_dir
proc.png
proc.py
proc2.png
product-note.html
product-note.pdf
prof.out
prof.py
pub.log
pub.py
pub.sqlite3
pub2.log
pure2
pw
r
r1
r2
r2-07c7558
r2-07c7558-server.log
r2-07c7558.sqlite3
r2-802d5fd
r2-cases.out
r2-deploy-head
r2-deploy-wt
r2-head
r2-ocr
r2-planted
r2-server.log
r2-sweep.out
r2.db
r2.log
r2.pid
r2.sqlite3
r2_app.sqlite3
r2_blank_judges.py
r2_check.py
r2_detect.py
r2_es2.py
r2_export.json
r2_for2.py
r2_ids.txt
r2_library.md
r2_mixed.py
r2_mut_base
r2_mut_base_m
r2_mutant_r2b.py
r2_mutants.py
r2_probe_out.txt
r2_rec.sqlite3
r2_run.log
r2_sentinel_data
r2_set_status.py
r2_t080_app.log
r2_t080_app.sqlite
r2_token.txt
r2_treeid.txt
r2_unit.txt
r2a
r2app
r2app-d865
r2arch
r2b
r2c_tree.txt
r2d.sqlite3
r2d_run.log
r2d_tree.txt
r2demo
r2demo.log
r2head
r2live.log
r2live.pid
r2live.sqlite3
r2local
r2local.log
r2mut
r2o
r2parent
r2server.log
r2src
r3
r3-25f585c
r3-a27
r3-demo.db
r3-demo.log
r3-local.db
r3-local.log
r3-parent
r3-server.log
r3.db
r3.log
r3.pid
r3.sqlite3
r3_acceptance_strings.py
r3_accepted.json
r3_api.py
r3_check_json.py
r3_full.log
r3_gate_check.py
r3_mut
r3_rootcause.py
r3_sentinel_data
r3_server.log
r3_t080.sqlite
r3_tok.txt
r3a
r3ap
r3api
r3api2
r3app.sqlite3
r3arch
r3b
r3bp
r3clone.81DVDF
r3clone.out
r3copy
r3da0c7fe
r3db.sqlite3
r3dev
r3e2e.log
r3h
r3head
r3health.json
r3img
r3m
r3mut
r3o
r3pop
r3probe.py
r3run
r3run.out
r3runpid
r3scripts
r3server.log
r3src
r3tb
r3timing.txt
r3tree
r3workdir
r4-8f78874
r4_probe_8634bfe.out.txt
r4_rootcause.py
r4arch
r4data
r4out
r4pin
r4probe
r4probe_on_0f58181.txt
r5
r5.log
r5.pid
r5.sqlite3
r5_e3.png
r5_flag.png
r5_top.png
r5b
r_head.json
r_new.json
rail.png
raw1.txt
raw2.txt
raw3.txt
raw4.txt
raw5.txt
raw6.txt
rec.py
rec.sh
rec_a.log
rec_all.log
rec_all.sh
rec_b.log
rec_judges.log
rec_narr.py
rec_sample.log
recon.py
render_curated.log
render_curated.sqlite
render_flags.log
render_flags.sqlite
render_race.log
render_race.sqlite
render_recorded.log
render_recorded.sqlite
replay.py
replit-config.html
replit-deploy.html
replit_env.py
repo
repro_stale
req_mut.md
requirements-dev.txt
requirements.txt
rerec.log
rerec.sh
rerun.out
rerun.sh
rerun2.sh
research
review.bak
review_commit.py
review_fixed.js
review_head.js
review_headplus.py
review_mine.py
reviews
rt_base.json
rt_r2.json
run.base.py
run.head.py
run.log
run.try.py
run1.err
run1.log
run1.out
run2
run2.err
run2.log
run2.out
run3.err
run3.log
run3.out
run4.err
run4.out
run4.time
run5.err
run5.out
run6.err
run6.out
run_c5.py
run_m2.pid
run_m2.sh
run_mutants_r3.py
run_p3_chain.sh
run_r3.sh
run_ro.py
run_t070_orig.py
runs.status
rv_T132_T128_r2r3
s-1440-0.png
s-1440-1700.png
s-1440-2300.png
s-1440-2600.png
s-1440-3300.png
s-1440-4400.png
s-1440-5400.png
s-1440-900.png
s-390-0.png
s-390-1500.png
s-390-3000.png
s-390-900.png
sample_case.json
sc.log
sc.sqlite3
scan.py
scan.py.bak
scan_specimens.py
scan_time_10x5000wide.pdf
schema_pre_T095.sql
score.py
scr.log
scr.sqlite3
scripted.log
scripts
scroll.py
selfcheck-r2.txt
serve_p3_wrapper.py
serve_snap.py
server-7871.log
server-7872.log
server.err
server.log
server.out
server.pid
server2.log
server2.pid
server7867.log
shard0.out
shard1.out
shard2.out
shard3.out
shard4.out
shoot.py
shot.py
shot2.py
shots
shots.log
shots.py
shots2.py
shots_old.py
shots_t046r2.py
show.py
show_T103.txt
snap
snap-077
snap-89a323a
snap-c61
snap-final
snap-h2
snap-head
snap-t187r3
snap.out
snap.path
snap2
snap3
snap7942
snap7942.db
snap7942.log
snap7942.pid
snap9
snap_run.sh
sp.txt
spec
splice.py
spy3.log
spy3.py
src
srv.KdvV
srv.log
srv.out
srv.pid
srv2.log
srv2.pid
srvdir
st_commit.py
stable.py
start.sh
states.py
steps-open.png
store.orig.bak
strip.py
strip_and_grep.py
submission
sync.py
sync.sh
sync_r5.sh
t015r4
t028.out
t030r2mut
t033mut
t033mut.py
t035
t038
t038r3
t040-077
t040-head
t040-live
t043-239
t043_r2_probe.py
t043_r2_probe2.py
t043_r2_probe3.py
t045r2-bypass
t045r2-clean
t045r3-clean
t046-server.log
t046.sqlite3
t046r2.log
t046r2.pid
t046r2.sqlite3
t053r3-data
t055_base_full.txt
t055_mut_full.txt
t056r2_01ipr4y9
t056r2_5_pc8ore
t056r2_gxnki_45
t056r2_jvse81hd
t056r2_pjbon2yp
t057
t060-a11y-axe
t060-a11y-data
t060-a11y-head
t060-a11y-serve.py
t060-p3-app
t060-p3-axe
t060-p3-chain.log
t060-p3-review.json
t060-p3-server.log
t060-p3-server.pid
t060-p3.sqlite3
t060p2
t060p2-wrap
t065
t065r2
t066r2
t066r3
t067
t067_59c7edb
t067_f6fa2dd
t067_head_archive
t067_m1
t067_m2
t067_m3
t067_probes
t067head
t067parent
t067r3
t067r4
t067r5
t067r5-probe-out.txt
t068-data
t068-data-commit
t068-data-commit2
t068-server-commit.log
t068-server-commit2.log
t068-server.log
t068r2-server.log
t068r2-snap
t068r3-case01-body.json
t068r3-case01-get.json
t068r3-data
t068r3-head
t068r3-probe-token.txt
t068r3-server.log
t070
t070r2b
t071_title_probe.py
t072
t072plant
t072r3
t072r3-p1_be_selfreport
t072r3-p2_be_patientstatement
t072r3-p3_be_patientstates
t072r3-p4_fe_selfreport
t072r3-p5_fe_patientstatement
t072r3-p6_fe_selfreported_ui
t072r4
t072r4_plants
t074
t075r2
t076r2
t076r2-data
t076r2-server.log
t077r3
t079.log
t079.sqlite3
t080m_M10_date_always_confirmed
t080m_M11_judge_partial_is_pass
t080m_M12_date_blocker_reason
t080m_M13_overrides_not_counted
t080m_M14_unavailable_counted_judged
t080m_M15_agreement_never_fails
t080m_M16_verbatim_fail_ignored_on_entry
t080m_M17_skip_after_reject_removed
t080m_M18_nothing_accepted_removed
t080m_M19_unsupported_excludes_disagrees
t080m_M1_rejected_blocks_gate
t080m_M20_step_order_swap
t080m_M21_progress_counts_skipped_as_pending
t080m_M22_total_inclusion_accepted_pending
t080m_M23_fixed_why_replaced_by_model_text
t080m_M2_dismissed_blocks_gate
t080m_M3_dismissed_human_pass
t080m_M4_qualifier_always_pass
t080m_M5_gate_ignores_running
t080m_M6_rate_pending_total
t080m_M7_raw_leak_in_metadata
t080m_M8_event_before_after_leak
t080m_M9_edited_text_leak
t080m_base
t080r4
t085r2
t085r3
t086head
t086wt
t090-out
t090.index
t090.patch
t090_code.patch
t090_patch2.py
t090_patch_run.py
t090_patch_tests.py
t090r2
t090r3
t092
t093.base.py
t094r2
t095.patch
t095r2_head
t096-evals
t096-export-check.py
t096-ux-36ceb38
t096-ux-server.log
t096-ux-walk-output.txt
t096-ux.sqlite3
t096_all.py
t096_ds.py
t096_probe.py
t096_probe2.py
t096_shot.py
t096_shot2.py
t096_start.sh
t096data
t097
t097.log
t097.pid
t097.sqlite3
t097b.sqlite3
t097r2
t097r2-server.log
t097r2.sqlite3
t097r2head
t097r3-archive-9f2811f
t097r3-server.log
t097r3-server.pid
t097r3.sqlite3
t098-e511778
t098-f5ddec8
t098-head
t099-3ecb8b1
t099-dirty-check
t099-f345bc8-r2
t099-gitclone-parent
t099-mut
t099.index
t099_msg.txt
t1.xXug
t100-card
t100-fresh
t101
t101r2
t103r2
t103r3_api.diff
t103r3_archive
t103r3_billing.diff
t103r3_control_archive
t103r3_mut
t103r4_archive
t104
t104-3462ad0-ux
t104-server.log
t104-server.pid
t104-state.json
t104-ux.sqlite3
t105
t105r2
t106_r2_archive
t108
t109_adr_edit.py
t109_doc_edit.py
t109r2_head
t109r2_mutA
t109r2_mutB
t109r2_pin
t109r3_head
t109r3_mut
t109r3_mutate.py
t109r3_pin
t109r3_probe_cc.py
t109r3_probe_flags.py
t109r3_probe_flags2.py
t109r3_probe_trim.py
t109r3_probe_trim2.py
t109r4
t110.sqlite3
t110b.sqlite3
t111-archive
t111-parent
t111r2
t111r2-base
t111r2-base.out.json
t111r2-head
t111r2-head.out.json
t111r2-parent
t111r2-parent.out.json
t112.index
t112_live.sh
t112_pipeline.py
t113_run1_evidence
t114
t114r2
t115.pid
t115.sqlite
t115srv.log
t116r2-base
t116r2-head
t116r3
t116r4
t116r5
t118-head
t118-mutA
t118-mutB
t118-pre
t119
t119.log
t119.pid
t119.sqlite3
t119m
t119m.log
t119m.pid
t119m.sqlite3
t120
t120-123-archive
t120-123-server.log
t120-123.sqlite3
t120-parent-archive
t120-parent-server.log
t120-parent.sqlite3
t120-r3.sqlite
t120r2
t120r2.sqlite3
t120r4
t121r2
t123-cmp-head.jsonl
t123-cmp-pre.jsonl
t126r1
t126r2
t133_r1_m3_full.out
t133_r1_m3_full.py
t133_r1_mutate.py
t133_r1_probe.py
t133_r2_probe_mine.py
t134_app.sqlite3
t134_server.log
t134m
t134parent
t134parent2
t134r1
t134r2
t134r3_c4bb
t134r3_cli1.err
t134r3_cli1.txt
t134r3_cli2.err
t134r3_cli2.txt
t134r3_dbg
t134r3_fix
t134r3_head
t134r3_mut
t134r3_mut.txt
t134r3_mut2
t134r3_mut_h.txt
t134r3_par
t134r3_unit.txt
t134r3_unit_c4bb.txt
t134r3_unit_fix.txt
t134scripts
t136-archive
t136-r2-staff
t136-server.log
t136.db
t139
t139_app.sqlite3
t139_overlay.err
t139_overlay.out
t139_overlay.sqlite3
t139_server.err
t139_server.out
t139_trace.sqlite3
t139_trace2.sqlite3
t139clean
t139overlay
t139r2
t139r2_app.sqlite3
t139r2_server.log
t139r3
t139r3_app.sqlite3
t139r4
t139r4_app.sqlite3
t139r4_server.log
t139r5
t139r5_mut1
t139r5_mut2
t139r5_mut3
t139r5_out
t139r5_prev
t139r5_scripts
t139tree
t143
t143p
t143r2
t143r2_case_lib01_er_only_then_gap.txt
t143r2_case_lib02_slip_fall_prior_knee.txt
t143r2_case_lib03_truck_rear_end_chiro.txt
t143r2_case_lib04_dog_bite_scar_revision.txt
t143r2_case_lib05_pedestrian_orif_hardware.txt
t143r2_case_lib06_lop_billed_vs_adjusted.txt
t143r2_case_lib07_parking_lot_fall_outside_records.txt
t143r2_case_lib08_second_crash_mri_after.txt
t143r2_case_lib09_spanish_interpreter_espalda.txt
t143r2_case_lib10_eob_ub04_cms1500.txt
t143r2_case_lib11_priors_and_ledger.txt
t143r2_case_lib12_records_review_credibility.txt
t143r2_case_lib13_cloned_notes_cross_provider.txt
t143r2_case_lib14_handwritten_chiro_scans.txt
t143r2_case_lib15_conclusory_letter_mist.txt
t143r2_mut.py
t143r2_sample.txt
t143r3
t144r1
t145r1
t146r2
t146r3
t146r4
t148r1
t149db
t149r2
t149r2-server.log
t149r2.pid
t149r2.sqlite3
t149server.log
t149src
t151-25f585c
t151-out
t151-scripts
t152_collect.py
t152_diff.py
t154
t154.sqlite3
t154b.sqlite3
t154r2
t154r2p
t155
t155r2
t157-check-json.py
t157-r1
t157r2b
t158-card
t158-f31
t158-f31-m2
t158-f31-m6
t158-f31-runs
t158-head
t158-m2
t158-m3
t158-m4
t158-m5
t158-m6
t158-mut
t158-probe
t158-r1
t158-review-head.js
t158-review-pre.js
t158-settle
t158r3
t159.patch
t160-review
t162.sqlite3
t162r2
t162r2.base
t162r2.idx
t162r3
t162r3.idx
t162v-final
t165-backend
t165-r2
t165-review
t165r2b
t166
t166-mvp-r2-ux-d865.sqlite3
t166-mvp-r2-ux.sqlite3
t166-r2-ux-d865.log
t166-r2-ux-server.log
t168r2
t169-clone-2
t169r2
t171
t171app.sqlite3
t171server.log
t173-final
t173-gen
t173-head
t173-verify
t173.idx
t174
t174r4-local.db
t174r4-local.log
t174r4-public.db
t174r4-public.log
t174r4-src
t175r1
t175r2
t177-arch
t177-arch-base
t177r4
t177r5-fresh
t177r5-prev
t177r5-probe
t178-interrupt.db
t178-interrupt2.db
t178-old.db
t178-pastes.db
t178-pid-7882
t178-pid-7883
t178-pid-7884
t178-server-7881.log
t178-server-7882.log
t178-server-7883.log
t178-server-7884.log
t178-stale.db
t179_commit.index
t179_final.index
t179_old
t179r2
t179r2_unit.txt
t179v2
t180.db
t181
t181-app.sqlite3
t181-local-server.log
t181-local.sqlite3
t181-server.log
t181r3-2c19817
t181ux
t182
t182-3sjF
t182-dir.txt
t182-index.html
t182-serve.log
t182-serve.pid
t182-t0.txt
t182-t1.txt
t182-z.txt
t187r2
t194.index
t194_commit.sh
t194_msg.txt
t199.index
t199_commit.sh
t199_msg.txt
t2.q4VB
t200
t200.idx
t200run
t201-r1
t202
t202.idx
t202.tree
t202parent
t202r2
t203
t203r2
t203r2.idx
t205.db
t2b.IKsK
t3.ORDQ
t4.0u5g
t84r4
tabflow.py
tail.md
test_billing_old.py
tests
tests_b05.py
tests_evals.sh
thr.py
thr2.out
thr2.py
timed_run.sh
tmp.index
tmp2.index
tmp3.index
tmpidx_t197
tmpindex
tog-open.png
tog.py
tok.json
tok_c1_local
tok_c3_local
tok_c5_local
tok_c7_local
tok_case_lib01_er_only_then_gap
tok_case_lib02_slip_fall_prior_knee
tok_case_lib03_truck_rear_end_chiro
tok_case_lib04_dog_bite_scar_revision
tok_case_lib05_pedestrian_orif_hardware
tok_g02_local
tok_g04_local
tok_g06_local
tok_g08_local
tok_g09_local
tok_sample2_local
tok_sample_local
tok_sample_pub
tokens.json
tools
tree
tree.sha
tree.txt
tree3
tree4
tree5
tree_r2
tree_r3
two.py
two.py.bak
u.orig
ub
ui-demo
ui-input.out
ui-local
unit-run-r2-clone-with-git.txt
unit-run-r2.txt
unit.out
unit.txt
unit1.txt
unit171.log
unit2.out
unit3.out
unit_full.txt
unit_full_head.out
unit_r2a.txt
unit_r2b.txt
ux-mvp-r3-da0c7fe.sqlite3
ux-mvp-r3-server.log
ux-mvp-r3.pid
ux-r2-2.sqlite3
ux-r2-3.sqlite3
ux-r2-debug-sample.png
ux-r2-server-2.log
ux-r2-server-3.log
ux-r2-server.log
ux-r2-server.pid
ux-r2.sqlite3
ux-t203-38ee0c3
ux-t203-demo.log
ux-t203-demo.pid
ux-t203-demo.sqlite3
ux-t203-e2e.out
ux-t203-local.log
ux-t203-local.pid
ux-t203-local.sqlite3
ux-t203r2-demo.log
ux-t203r2-demo.sqlite3
ux-t203r2-e2e.out
ux-t203r2-fa34fe9
ux-t203r2-local.log
ux-t203r2-local.sqlite3
ux3
v
validate_review.py
verify.py
view.json
walk.out
walk.py
walk2.py
why.orig.py
wide.py
wprobe.py
wt
wt-031a708
wt-7df65fb
wt-golden.txt
wt-head
wt2
wt7944.db
wt7944.log
wt7944.pid
wt7945.db
wt7945.log
wt7945.pid
wt7946.db
wt7946.log
wt7946.pid
wt_final
wt_final2
wt_head
wt_run.sh
wt_t155
x45.py
xc.py
xss.py
zlayt-base
zlayt-head
zlayt-public-snapshot.JTMbwv
zlayt-r2
zlayt-r3
rc 1
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:27.699Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; lsof -iTCP:7994 -sTCP:LISTEN -nP; env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$S/t206.db PORT=7994 HOST=127.0.0.1 nohup .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py $S/a206 > $S/t206-server.log 2>&1 &\nsleep 6; curl -s http://127.0.0.1:7994/api/health; lsof -iTCP:7994 -sTCP:LISTEN -nP"
}
````

### User / tool · 2026-11-03T00:43:33.955Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  81680 arsis    9u  IPv4 0x1d7071098997d4ee      0t0  TCP 127.0.0.1:7994 (LISTEN)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:36.931Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-206-paralegal && cp artifacts/review-evidence/T-205-paralegal/h.py $D/h.py && cp artifacts/review-evidence/T-205-paralegal/p01.py $D/p01.py && cp artifacts/review-evidence/T-205-paralegal/p02_notes.py $D/p02_notes.py && grep -n \"7981\\|a203\\|T-205\" $D/*.py"
}
````

### User / tool · 2026-11-03T00:43:37.053Z

**tool result**
````
artifacts/review-evidence/T-206-paralegal/h.py:11:BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7981")  # T-202 r2: 986fc55 archive, port 7976
artifacts/review-evidence/T-206-paralegal/p02_notes.py:1:"""T-205 paralegal: render every confirm_note reason in the Step 3 card (stub of GET /api/cases/{token} service_date only, as the worker's own test does;
artifacts/review-evidence/T-206-paralegal/p02_notes.py:4:sys.path.insert(0, "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a203")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:44.941Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-206-paralegal && python3 - <<'EOF'\np=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-206-paralegal/p01.py\"\ns=open(p).read()\ns=s.replace('T-202 r2 paralegal','T-206 paralegal',1)\nold='        pg.evaluate(\"() => { const c = document.querySelector(\\'[data-testid=confirm-note]\\'); if (c) c.scrollIntoView(); }\")'\nnew='''        full = pg.evaluate(\"() => { const w = document.querySelector('.work') || document.body; return w.innerText; }\")\n        heads = pg.evaluate(\"() => Array.from(document.querySelectorAll('[data-testid=src-head],.src-head,.sub,.card-h')).map(e=>e.innerText)\")\n        import re as _re\n        DATE = _re.compile(r\"(?:January|February|March|April|May|June|July|August|September|October|November|December) \\\\d{1,2}(?:[\\\\u2013-]\\\\d{1,2})?, \\\\d{4}\")\n        bare = []\n        for m in DATE.finditer(full):\n            pre = full[max(0, m.start()-16):m.start()]\n            if not pre.endswith(\"statement dated \"):\n                bare.append(full[max(0, m.start()-40):m.end()+10].replace(chr(10), \" | \"))\n        log(f\"[{name}] FULL item={i} bare_dates={json.dumps(bare)} heads={json.dumps(heads)}\")\n        log(f\"[{name}] FULLTEXT item={i} \" + full.replace(chr(10), \" | \"))\n        pg.evaluate(\"() => { const c = document.querySelector('[data-testid=confirm-note]'); if (c) c.scrollIntoView(); }\")'''\nassert old in s\ns=s.replace(old,new,1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"FULL item\" $D/p01.py | head -3\ntail -30 $D/p01.py"
}
````

### User / tool · 2026-11-03T00:43:45.071Z

**tool result**
````
116:        log(f"[{name}] FULL item={i} bare_dates={json.dumps(bare)} heads={json.dumps(heads)}")
            if not pre.endswith("statement dated "):
                bare.append(full[max(0, m.start()-40):m.end()+10].replace(chr(10), " | "))
        log(f"[{name}] FULL item={i} bare_dates={json.dumps(bare)} heads={json.dumps(heads)}")
        log(f"[{name}] FULLTEXT item={i} " + full.replace(chr(10), " | "))
        pg.evaluate("() => { const c = document.querySelector('[data-testid=confirm-note]'); if (c) c.scrollIntoView(); }")
        shot(f"{name}-s3-{step:02d}-{i}")
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
    dump(f"[{name}] step 3 done")
    shot(f"{name}-step3-done", full=True)
    pg.get_by_text("Go to step 4").first.click()
    pg.wait_for_selector("[data-testid=letter-text]", timeout=15000)
    pg.wait_for_timeout(600)
    with pg.expect_download() as d:
        pg.click("[data-testid=btn-download-letter]")
    d.value.save_as(f"{OUT}/ui-{name}-letter.txt")
    with pg.expect_download() as d2:
        pg.click("[data-testid=btn-download-notes]")
    d2.value.save_as(f"{OUT}/ui-{name}-notes.txt")
    open(f"{OUT}/ui-{name}-letter-onscreen.txt", "w").write(pg.inner_text("[data-testid=letter-text]"))
    shot(f"{name}-step4", full=True)
    log(f"[{name}] done in", round(time.time() - T0, 1), "s")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:46.934Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-206-paralegal && curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7994/ && T181_BASE=http://127.0.0.1:7994 T181_PROFILE=profile206 CASES=lib11 timeout 300 .venv/bin/python -I $D/h.py $D/p01.py > $D/p01.out 2>&1; echo rc $?; grep -n \"PROBE\\|FULL item\\|ERRORS\\|Traceback\\|Error\" $D/p01.out | cut -c1-900"
}
````

### User / tool · 2026-11-03T00:43:47.056Z

**tool result**
````
200
rc 127
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:48.202Z

**tool call — Bash**
````
{
 "command": "ls -la .venv/bin/python* 2>&1 | head; cat artifacts/review-evidence/T-206-paralegal/p01.out | head"
}
````

### User / tool · 2026-11-03T00:43:48.298Z

**tool result**
````
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python3 -> python3.12
lrwxr-xr-x@ 1 arsis  staff  44 Nov  1 18:02 .venv/bin/python3.12 -> /opt/homebrew/opt/python@3.12/bin/python3.12
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:43:50.060Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-206-paralegal && T181_BASE=http://127.0.0.1:7994 T181_PROFILE=profile206 CASES=lib11 .venv/bin/python -I $D/h.py $D/p01.py > $D/p01.out 2>&1; echo rc $?; grep -n \"PROBE\\|FULL item\\|ERRORS\\|Traceback\\|Error\\|done in\" $D/p01.out | cut -c1-1100",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T00:44:15.091Z

**tool result**
````
rc 0
26:[lib11] PROBE item=a1 {"svc": "March 18, 2026", "svcState": "stated", "stmt": null, "note": null, "figure": "$3,260.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nWexcombe Memorial ED \u00b7 March 18, 2026\n\n$3,260.00\n\nDate of service March 18, 2026\n\nWritten in the record as $3,260.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
27:[lib11] FULL item=a1 bare_dates=["ecord | Record 3 \u00b7 Wexcombe Memorial ED \u00b7 March 18, 2026 | === Recor", " $3,260.\" | Charge | Wexcombe Memorial ED \u00b7 March 18, 2026 |  | $3,260.0", "ch 18, 2026 |  | $3,260.00 |  | Date of service March 18, 2026 |  | Written "] heads=["From the record\nRecord 3 \u00b7 Wexcombe Memorial ED \u00b7 March 18, 2026", "Record 3 \u00b7 Wexcombe Memorial ED \u00b7 March 18, 2026", "Charge\nWexcombe Memorial ED \u00b7 March 18, 2026"]
31:[lib11] PROBE item=a2 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$250.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Not counted yet\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026\n\n$250.00\n\nThe line states no date of service, so it is not a single dated bill line and is not totaled.\n\nYou can still count it if you checked the ledger yourself.\nI checked this is a separate charge for a service.\nA second AI check thought this may be a billed charge, not what it was first sorted as.\nI read this amount against the highlighted words myself."}
32:[lib11] FULL item=a2 bare_dates=[] heads=["From the record\nRecord 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Record 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Not counted yet\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026"]
36:[lib11] PROBE item=a3 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$180.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Not counted yet\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026\n\n$180.00\n\nThe line states no date of service, so it is not a single dated bill line and is not totaled.\n\nYou can still count it if you checked the ledger yourself.\nI checked this is a separate charge for a service.\nA second AI check thought this may be a billed charge, not what it was first sorted as.\nI read this amount against the highlighted words myself."}
37:[lib11] FULL item=a3 bare_dates=[] heads=["From the record\nRecord 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Record 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Not counted yet\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026"]
41:[lib11] PROBE item=a4 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$2,310.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Not counted yet\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026\n\n$2,310.00\n\nThe line states no date of service, so it is not a single dated bill line and is not totaled.\n\nYou can still count it if you checked the ledger yourself.\nI checked this is a separate charge for a service.\nA second AI check thought this may be a billed charge, not what it was first sorted as.\nI read this amount against the highlighted words myself."}
42:[lib11] FULL item=a4 bare_dates=[] heads=["From the record\nRecord 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Record 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Not counted yet\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026"]
46:[lib11] PROBE item=a5 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$2,740.00", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026\n\n$2,740.00\n\nTotal or subtotal line: it repeats the charges listed with it, so it is not totaled.\n\nA second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide.\nI read this amount against the highlighted words myself."}
47:[lib11] FULL item=a5 bare_dates=[] heads=["From the record\nRecord 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Record 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026"]
51:[lib11] PROBE item=a6 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$300.00", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026\n\n$300.00\n\nPayment: money received, not a charge.\n\nA second AI check thought this may be a damages figure (for example lost wages), not what it was first sorted as. Read it against the highlighted words before you decide.\nI read this amount against the highlighted words myself."}
52:[lib11] FULL item=a6 bare_dates=[] heads=["From the record\nRecord 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Record 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026"]
56:[lib11] PROBE item=a7 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$274.00", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026\n\n$274.00\n\nAdjustment, write-off or credit: not a charge, and never subtracted from the billed charges.\n\nEither way, it is never added to the bill total."}
57:[lib11] FULL item=a7 bare_dates=[] heads=["From the record\nRecord 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Record 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026"]
61:[lib11] PROBE item=a8 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$2,166.00", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026\n\n$2,166.00\n\nBalance or amount due: worked out from charges, payments and adjustments, not a charge.\n\nA second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide.\nI read this amount against the highlighted words myself."}
62:[lib11] FULL item=a8 bare_dates=[] heads=["From the record\nRecord 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Record 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026"]
123:[lib11] done in 24.5 s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:44:17.636Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-206-paralegal && sed -n 62,123p $D/p01.out | cut -c1-400; echo ----; cat $D/ui-lib11-letter.txt | sed -n 30,60p; echo ---NOTES; grep -n -i \"march 18\\|june 15\\|date\" $D/ui-lib11-notes.txt | head -20"
}
````

### User / tool · 2026-11-03T00:44:17.740Z

**tool result**
````
[lib11] FULL item=a8 bare_dates=[] heads=["From the record\nRecord 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Record 9 \u00b7 Fennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026", "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 statement dated June 15, 2026"]
[lib11] FULLTEXT item=a8 From the record | Record 9 · Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026 | === Record 9 === | Date: 2026-06-15 | Source: Fennimoor Spine Clinic, itemized ledger | Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. 
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-206-paralegal/lib11-s3-07-a8.png
===== [lib11] step 3 done url=http://127.0.0.1:7994/case/2JJfegcNvODFQsikNXoyJw/bills
Skip to the main content
Synthetic data only — never paste real records
‹
Your cases
Priors and ledger
9 records
Demo: recorded AI answers
Dark mode
✓
1 Add records
Done
(step 1 of 4)
✓
2 Check the timeline
Done
(step 2 of 4)
✓
3 Check the bills
Done
(step 3 of 4)
4
4 Get your letter
Ready
(step 4 of 4)
Step 3 of 4
Check the bills
✓
You checked every bill amount.

This is the total line your letter will carry:

Billed charges accepted from these records: $6,000.00

Go to step 4: Get your letter
Counted (4)
Amount	From	Date of service	
$3,260.00	Wexcombe Memorial ED	March 18, 2026	Change
$250.00	Fennimoor Spine Clinic, itemized ledger	(statement dated June 15, 2026; service date not stated)	Change
$180.00	Fennimoor Spine Clinic, itemized ledger	(statement dated June 15, 2026; service date not stated)	Change
$2,310.00	Fennimoor Spine Clinic, itemized ledger	(statement dated June 15, 2026; service date not stated)	Change
Not counted by you (0)

You didn't leave out any charge.

Never counted (4)

These are never added to the total. The ones you listed go in the notes for the attorney.

Amount	From	Why it's never counted	
$2,740.00	Fennimoor Spine Clinic, itemized ledger	Total or subtotal line: it repeats the charges listed with it, so it is not totaled.	Change
$300.00	Fennimoor Spine Clinic, itemized ledger	Payment: money received, not a charge.	Change
$274.00	Fennimoor Spine Clinic, itemized ledger	Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.	Change
$2,166.00	Fennimoor Spine Clinic, itemized ledger	Balance or amount due: worked out from charges, payments and adjustments, not a charge.	Change
Demo: recorded AI answers. These are real AI answers recorded earlier; nothing new is sent to an AI.
=====
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-206-paralegal/lib11-step3-done.png
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-206-paralegal/lib11-step4.png
[lib11] done in 24.5 s
----

May 29, 2026 — Fennimoor Spine Clinic, visit 14
Neck pain 4/10, low back pain 5/10. Care continues.
Source [Ex. __ / Bates __]: "Neck pain 4/10, low back pain 5/10. Care continues."

BILLED CHARGES

Wexcombe Memorial ED, March 18, 2026: $3,260.00
Source [Ex. __ / Bates __]: "ED charge: $3,260."
Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00
Source [Ex. __ / Bates __]: "New patient exam charge $250.00"
Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $180.00
Source [Ex. __ / Bates __]: "x-ray charge $180.00"
Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $2,310.00
Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"

Billed charges accepted from these records: $6,000.00---NOTES
10:- Causation language: record 2 (Ashgrove Fire-Rescue run report, March 18, 2026) "Ambulatory at scene."; record 4 (Pellingham and Rook PLLC, correspondence (letter of protection), March 26, 2026) "Letter of protection to Fennimoor Spine Clinic."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Patient referred by attorney."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Treating under a letter of protection."; record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) "Account held under letter of protection."
17:- Record 2 (Ashgrove Fire-Rescue run report, March 18, 2026): "Ambulatory at scene." Causation language.
24:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "total charges $2,740.00." Not totaled ($2,740.00): Total or subtotal line: it repeats the charges listed with it, so it is not totaled.
25:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Payment received $300.00." Not totaled ($300.00): Payment: money received, not a charge.
26:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Adjustment (courtesy discount) -$274.00." Not totaled ($274.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.
27:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Balance due $2,166.00." Not totaled ($2,166.00): Balance or amount due: worked out from charges, payments and adjustments, not a charge.
39:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) — dismissed
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:44:24.439Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-206-paralegal && T181_BASE=http://127.0.0.1:7994 T181_PROFILE=profile206 CASES=case_09,lib10 .venv/bin/python -I $D/h.py $D/p01.py > $D/p01b.out 2>&1; echo rc $?; grep -n \"FULL item\\|ERRORS\\|Traceback\\|done in\\|created via\" $D/p01b.out | cut -c1-500; grep -n \"dismissed\" $D/ui-lib11-notes.txt | head -3; sed -n 36,42p $D/ui-lib11-notes.txt",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T00:44:51.297Z

**tool result**
````
rc 0
2:[case_09] created via POST /api/cases token=bptE_Hustu7hzLn58mg1qQ
13:[case_09] FULL item=a1 bare_dates=["March 1, 2026 |  | $275.00 |  | Date of service February 2, 2026 \u00b7 stateme"] heads=["From the record\nRecord 2 \u00b7 Hobbleton Family Clinic, billing statement \u00b7 statement dated March 1, 2026", "Record 2 \u00b7 Hobbleton Family Clinic, billing statement \u00b7 statement dated March 1, 2026", "Charge\nHobbleton Family Clinic, billing statement \u00b7 statement dated March 1, 2026"]
66:[case_09] done in 7.2 s
82:[lib10] FULL item=a2 bare_dates=["ne 19, 2026 |  | $4,920.00 |  | Date of service June 9\u201312, 2026 \u00b7 stateme"] heads=["From the record\nRecord 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Record 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026"]
87:[lib10] FULL item=a3 bare_dates=["ne 19, 2026 |  | $2,105.00 |  | Date of service June 9\u201312, 2026 \u00b7 stateme"] heads=["From the record\nRecord 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Record 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026"]
92:[lib10] FULL item=a4 bare_dates=["June 19, 2026 |  | $386.50 |  | Date of service June 9\u201312, 2026 \u00b7 stateme"] heads=["From the record\nRecord 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Record 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026"]
97:[lib10] FULL item=a5 bare_dates=["June 19, 2026 |  | $712.00 |  | Date of service June 9\u201312, 2026 \u00b7 stateme"] heads=["From the record\nRecord 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Record 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026"]
102:[lib10] FULL item=a1 bare_dates=[] heads=["From the record\nRecord 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Record 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Never counted\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026"]
107:[lib10] FULL item=a6 bare_dates=[] heads=["From the record\nRecord 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Record 4 \u00b7 Saltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026", "Never counted\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026"]
112:[lib10] FULL item=a7 bare_dates=[] heads=["From the record\nRecord 6 \u00b7 Quoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026", "Record 6 \u00b7 Quoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026", "Never counted\nQuoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026"]
117:[lib10] FULL item=a8 bare_dates=[] heads=["From the record\nRecord 6 \u00b7 Quoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026", "Record 6 \u00b7 Quoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026", "Never counted\nQuoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026"]
122:[lib10] FULL item=a9 bare_dates=[] heads=["From the record\nRecord 6 \u00b7 Quoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026", "Record 6 \u00b7 Quoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026", "Never counted\nQuoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026"]
127:[lib10] FULL item=a10 bare_dates=[] heads=["From the record\nRecord 6 \u00b7 Quoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026", "Record 6 \u00b7 Quoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026", "Never counted\nQuoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026"]
132:[lib10] FULL item=a11 bare_dates=[] heads=["From the record\nRecord 6 \u00b7 Quoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026", "Record 6 \u00b7 Quoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026", "Never counted\nQuoinmere Mutual Health Plan, EOB \u00b7 statement dated July 3, 2026"]
196:[lib10] done in 19.1 s
39:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) — dismissed
- Dr. Hesper Alderton; Ashgrove Fire-Rescue run report.

RECORDS NOT IN THE TREATMENT SECTION
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) — dismissed

EDITED ITEMS
- none
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:44:57.388Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-206-paralegal && grep -o \"case/[A-Za-z0-9_-]*/\" $D/p01b.out $D/p01.out | sort -u"
}
````

### User / tool · 2026-11-03T00:44:57.525Z

**tool result**
````
artifacts/review-evidence/T-206-paralegal/p01.out:case/2JJfegcNvODFQsikNXoyJw/
artifacts/review-evidence/T-206-paralegal/p01b.out:case/bptE_Hustu7hzLn58mg1qQ/
artifacts/review-evidence/T-206-paralegal/p01b.out:case/dUyn7AH3tDCFv4XfBcyhNw/
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:45:04.805Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-206-paralegal && python3 - <<'EOF'\nD=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-206-paralegal/\"\ns=open(D+\"p02_notes.py\").read()\ns=s.replace(\"scratchpad/a203\",\"scratchpad/a206\")\ns=s.replace(\"T-205 paralegal\",\"T-206 paralegal\")\ns=s.replace('TOK = {\"case_09\": (\"Rb_-aRcu7JXIMZ90rAiyHA\", \"a1\", \"2026-03-01\"), \"lib10\": (\"_HdnjAt2eCEWDdnvroHTEw\", \"a2\", \"2026-06-19\")}',\n 'TOK = {\"case_09\": (\"bptE_Hustu7hzLn58mg1qQ\", \"a1\", \"2026-03-01\"), \"lib10\": (\"dUyn7AH3tDCFv4XfBcyhNw\", \"a2\", \"2026-06-19\"), \"lib11\": (\"2JJfegcNvODFQsikNXoyJw\", \"a2\", \"2026-06-15\")}')\nold='''        info = pg.evaluate(\"\"\"'''\nnew='''        nxt = pg.evaluate(\"() => { const e = document.querySelector('[data-testid=confirm-next]'); return e ? e.innerText : null; }\")\n        foot = pg.evaluate(\"() => { const e = document.querySelector('[data-testid=confirm-note]'); const f = e && e.closest('.card-foot, .foot, [class*=foot]'); return f ? f.innerText : null; }\")\n        log(f\"[{case}/{reason}] NEXT={json.dumps(nxt)} FOOT={json.dumps(foot)}\")\n        info = pg.evaluate(\"\"\"'''\nassert old in s\ns=s.replace(old,new,1)\ns=s.replace('''if reason in (\"ambiguous_numeric\", \"no_date\") and case == \"lib10\":''','''if reason in (\"ambiguous_numeric\", \"no_date\") and case in (\"lib10\", \"lib11\"):''')\nopen(D+\"p02_notes.py\",\"w\").write(s)\nEOF\nT181_BASE=http://127.0.0.1:7994 T181_PROFILE=profile206 .venv/bin/python -I $D/h.py $D/p02_notes.py > $D/p02.out 2>&1; echo rc $?; grep -n \"NEXT=\" $D/p02.out | cut -c1-900 | head -30; grep -c \"ERRORS\" $D/p02.out; grep -n \"Traceback\\|Error\" $D/p02.out | head",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T00:45:14.489Z

**tool result**
````
rc 0
2:[case_09/ambiguous_numeric] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
4:[case_09/two_digit_year] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
6:[case_09/no_year] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
8:[case_09/invalid] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
10:[case_09/several_dates] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
12:[case_09/non_service_date] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
14:[case_09/no_date] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
16:[lib10/ambiguous_numeric] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
19:[lib10/two_digit_year] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
21:[lib10/no_year] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
23:[lib10/invalid] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
25:[lib10/several_dates] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
27:[lib10/non_service_date] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
29:[lib10/no_date] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
32:[lib11/ambiguous_numeric] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
35:[lib11/two_digit_year] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
37:[lib11/no_year] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
39:[lib11/invalid] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
41:[lib11/several_dates] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
43:[lib11/non_service_date] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
45:[lib11/no_date] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
0
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:45:24.863Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; grep -n \"not_stated\\|service date not stated\\|confirm_note\" $S/a206/app/backend/export.py $S/a206/app/backend/service_date.py | head -40; sed -n 1,60p $D/p02.out 2>/dev/null | head -0; grep -n \"no_date\\]\" artifacts/review-evidence/T-206-paralegal/p02.out | cut -c1-1500 | head -6"
}
````

### User / tool · 2026-11-03T00:45:24.977Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a206/app/backend/export.py:218:        NEVER given the record's date bare: 'Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated)'. Chosen over dropping the date
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a206/app/backend/export.py:227:        return f"{src} {service_date.not_stated_text(rd)}"
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a206/app/backend/service_date.py:5:services ('statement period 06/09/2026 to 06/12/2026', 'the run of 09/14/2026'). Everything else is `not_stated`, with a reason the Step 3 screen shows as a note asking the
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a206/app/backend/service_date.py:58:def not_stated_text(statement_iso) -> str:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a206/app/backend/service_date.py:61:        return f"(statement dated {display(statement_iso)}; service date not stated)"
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a206/app/backend/service_date.py:62:    return "(service date not stated)"
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a206/app/backend/service_date.py:76:def confirm_note(reason, raw) -> str:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a206/app/backend/service_date.py:264:    """{state: 'stated'|'not_stated', first, last (None for one day), reason (None when stated, else one of REASONS), raw (the date text the reason is about)} for the figure at
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a206/app/backend/service_date.py:266:    out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""}
head: illegal line count -- 0
14:[case_09/no_date] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
15:[case_09/no_date] {"note": "The line states no date of service. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 619, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated March 1, 2026; service date not stated)", "head": "Record 2 · Hobbleton Family Clinic, billing statement · statement dated March 1, 2026", "tag": "From the record"}
29:[lib10/no_date] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
30:[lib10/no_date] {"note": "The line states no date of service. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 619, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated June 19, 2026; service date not stated)", "head": "Record 4 · Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026", "tag": "From the record"}
45:[lib11/no_date] NEXT="What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself." FOOT=null
46:[lib11/no_date] {"note": "The line states no date of service. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 619, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated June 15, 2026; service date not stated)", "head": "Record 9 · Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026", "tag": "From the record"}
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:45:28.415Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-206-paralegal/note-lib11-ambiguous_numeric.png"
}
````

### User / tool · 2026-11-03T00:45:28.428Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:45:28.706Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-206-paralegal/lib11-s3-01-a2.png"
}
````

### User / tool · 2026-11-03T00:45:28.714Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:45:36.184Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-206-paralegal && grep -n -i \"not stated\\|type the\\|statement dated\\|Bills to request\\|\\$250\\|\\$180\\|2,310\" $D/ui-lib11-notes.txt; echo; sed -n 1,35p $D/ui-lib11-notes.txt | cut -c1-220; grep -c \"__\" $D/ui-lib11-letter.txt; grep -n \"service date not stated\" $D/ui-lib11-letter.txt"
}
````

### User / tool · 2026-11-03T00:45:36.338Z

**tool result**
````
35:BILLS TO REQUEST (entry in the letter, no accepted charge)

INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.

FLAGS ACCEPTED
- Gap: 35 days, April 24, 2026 to May 29, 2026: record 7 (Fennimoor Spine Clinic, visit 8, April 24, 2026) to record 8 (Fennimoor Spine Clinic, visit 14, May 29, 2026).
- Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior accidents? Yes [ ] No [X]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "Hist
- Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior injuries? Yes [ ] No IX]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "Histo
- Prior condition: record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "Problem list: hypertension, type 2 diabetes, chronic low back pain."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History p
- Causation language: record 2 (Ashgrove Fire-Rescue run report, March 18, 2026) "Ambulatory at scene."; record 4 (Pellingham and Rook PLLC, correspondence (letter of protection), March 26, 2026) "Letter of protection to

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- Record 1 (Dr. Hesper Alderton, primary care, March 4, 2026): "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy." Conflict, other fact mismatch; prior condit
- Record 2 (Ashgrove Fire-Rescue run report, March 18, 2026): "Ambulatory at scene." Causation language.
- Record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026): "Treating under a letter of protection." Causation language.
- Record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026): "Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]." Conflict, other fact mismatch; prior condition.
- Record 7 (Fennimoor Spine Clinic, visit 8, April 24, 2026): "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued." Gap.
- Record 8 (Fennimoor Spine Clinic, visit 14, May 29, 2026): "Neck pain 4/10, low back pain 5/10. Care continues." Gap.

AMOUNTS NOT TOTALED
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "total charges $2,740.00." Not totaled ($2,740.00): Total or subtotal line: it repeats the charges listed with it, so it is not totaled.
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Payment received $300.00." Not totaled ($300.00): Payment: money received, not a charge.
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Adjustment (courtesy discount) -$274.00." Not totaled ($274.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed c
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Balance due $2,166.00." Not totaled ($2,166.00): Balance or amount due: worked out from charges, payments and adjustments, not a charge.

DAMAGES MENTIONS (not charges)
- none

FUTURE TREATMENT RECOMMENDED (no cost stated)
- none

BILLS TO REQUEST (entry in the letter, no accepted charge)
12
39:Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00
41:Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $180.00
43:Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $2,310.00
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:45:46.798Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; sed -n 1,200p $S/a206/tests/e2e/guided/test_t206.py | cut -c1-260"
}
````

### User / tool · 2026-11-03T00:45:46.910Z

**tool result**
````
"""T-206 (D-071 follow-up to T-205, paralegal review minors): a Step 3 card shows a bare date only when it is a certain service date. An uncounted ledger line (lib11 a2-a4) and every other amount
taken from a bill document (the rest of the ledger) names its record's date "statement dated ...", on the card head, the line under it and the source head; the confirm note ends with what to do next in
the words of the buttons the card has. Real browser, fixture backend, real API; the doubtful-date note is the backend's own sentence put into the case response (the fixture set has no such bill)."""
import re
from playwright.sync_api import expect
from tests.e2e.guided.test_shell_smoke import watch, go
from tests.e2e.guided.test_step2 import make, phone, case, item, open_item   # noqa: F401  (make and phone are fixtures)
from tests.e2e.guided.test_t205 import LIB10, LIB11, SD
import tests.e2e.conftest as C

BARE = re.compile(r"(?<!statement dated )(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}")


def texts(page):
    return {k: page.get_by_test_id(k).inner_text() for k in ("card-line", "line-sub", "src-head")}


def test_lib11_uncounted_ledger_lines_never_show_a_bare_statement_date(page, make):
    seen = watch(page)
    tok = make(LIB11); amounts = {a["id"]: a for a in case(tok)["amounts"]}
    uncounted = [i for i, a in amounts.items() if a["kind"] != "charge"]
    assert {"a2", "a3", "a4"} <= set(uncounted) and amounts["a2"]["countable"] and amounts["a2"]["service_date"] is None
    for iid in uncounted:         # the three countable lines and the four never counted: all of them are the ledger
        open_item(page, tok, iid, step="bills")
        t = texts(page)
        assert "statement dated June 15, 2026" in t["src-head"] and "statement dated June 15, 2026" in t["line-sub"], (iid, t)
        for k, v in t.items():
            assert not BARE.search(v), (iid, k, v)
        assert page.get_by_test_id("confirm-note").count() == 0
    # the ED charge states its own visit date: that one is a certain service date and stays plain
    open_item(page, tok, "a1", step="bills")
    assert page.get_by_test_id("service-date-text").inner_text() == "March 18, 2026"
    assert "statement dated" not in page.get_by_test_id("src-head").inner_text()
    assert seen == [], seen


def test_lib11_a_counted_ledger_line_keeps_the_label_and_matches_the_letter(page, make):
    seen = watch(page)
    tok = make(LIB11); a = item(tok, "a2")
    st, r = C.api("POST", f"/api/cases/{tok}/items/a2/review", {"action": "count", "confirm": "separate_charge", "version": a["version"], "expected_status": "pending",
                                                              **({"confirm_flag": a["count_confirm"]["confirm_with"]} if a.get("count_confirm") else {})}); assert st == 200, r
    open_item(page, tok, "a2", step="bills")
    sd = item(tok, "a2")["service_date"]
    assert sd["state"] == "not_stated" and "statement dated June 15, 2026" in sd["text"]
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    for k, v in texts(page).items():
        assert not BARE.search(v), (k, v)
    assert seen == [], seen


def test_a_doubtful_date_note_ends_with_what_to_do_next(page, make):
    seen = watch(page)
    tok = make(LIB10); a = item(tok, "a2")
    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="ambiguous_numeric", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("ambiguous_numeric", "04/05/2026"))

    def rewrite(route):
        r = route.fetch(); body = r.json()
        for x in body.get("amounts", []):
            if x["id"] == "a2":
                x["service_date"] = sd
        route.fulfill(response=r, json=body)
    page.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
    open_item(page, tok, "a2", step="bills")
    nxt = page.get_by_test_id("confirm-next"); expect(nxt).to_be_visible()
    t = nxt.inner_text()
    assert "check the date in the highlighted words" in t.lower() and "Yes, count it" in t and "No, don't count it" in t and "type the date into your letter yourself" in t, t
    labels = [page.get_by_test_id("answer-yes").inner_text().strip(), page.get_by_test_id("answer-no").inner_text().strip()]
    assert labels == ["Yes, count it", "No, don't count it"], "the sentence names the buttons the card really has"
    assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-next]").count() == 1
    assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-note]").count() == 1
    for k, v in texts(page).items():
        assert not BARE.search(v), (k, v)
    assert seen == [], seen


def test_the_next_step_fits_a_phone(phone, make):
    tok = make(LIB10); a = item(tok, "a2")
    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="no_year", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("no_year", "April 5"))

    def rewrite(route):
        r = route.fetch(); body = r.json()
        for x in body.get("amounts", []):
            if x["id"] == "a2":
                x["service_date"] = sd
        route.fulfill(response=r, json=body)
    phone.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
    open_item(phone, tok, "a2", step="bills")
    expect(phone.get_by_test_id("confirm-next")).to_be_visible()
    assert phone.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
    assert phone.get_by_test_id("answer-yes").is_visible()
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:45:56.562Z

**tool call — Bash**
````
{
 "command": "kill 81680; sleep 1; lsof -iTCP:7994 -sTCP:LISTEN -nP; echo lsof_rc $?; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7994/api/health; cd /Users/arsis/zlayt-pm-project && git rev-parse --short 79714c6; grep -c \"ERRORS\" artifacts/review-evidence/T-206-paralegal/p01.out artifacts/review-evidence/T-206-paralegal/p01b.out artifacts/review-evidence/T-206-paralegal/p02.out; grep -n \"no_date\\|several\" app/backend/service_date.py 2>/dev/null | head -0; ls artifacts/review-evidence/T-206-paralegal | head -50 | wc -l"
}
````

### User / tool · 2026-11-03T00:45:57.805Z

**tool result**
````
lsof_rc 1
000
79714c6
artifacts/review-evidence/T-206-paralegal/p01b.out:0
artifacts/review-evidence/T-206-paralegal/p02.out:0
artifacts/review-evidence/T-206-paralegal/p01.out:0
head: illegal line count -- 0
/bin/bash: child setpgid (85168 to 85168): Operation not permitted
      50
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:46:25.071Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-206-paralegal.md",
 "content": "# T-206 review — paralegal-reviewer (Maria Delgado)\n\nCommit 79714c6, fresh `git archive` extracted to an empty scratchpad directory (a206), demo mode (fixture backend, `ZLAYT_MODE=local`, health `demo_mode: true`) on port 7994. Listener PID 81680 stopped afterward (`lsof` exit 1, `curl` = 000). Private values seen: 0 (<redacted> count 0).\n\n**Verdict: pass (3 minors).** Both things asked for hold. Neither is a blocker, and I am answering the placeholder question below.\n\n- **No bare date on uncounted ledger lines: confirmed.** lib11 a2, a3, a4 (not counted yet) and a5 to a8 (never counted) read \"Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026\" in the card head, the line under it and the source head (p01.out:31-62, `bare_dates=[]` on all seven). The only plain date on lib11 is the ED line \"March 18, 2026\", a certain visit date. case_09 and lib10 still read \"Date of service … · statement dated …\" and the UB-04 and EOB heads all say \"statement dated\" (p01b.out). After counting, the done list and the letter give \"(statement dated June 15, 2026; service date not stated)\" on all three lines (ui-lib11-letter.txt:39, 41, 43). My T-205 minor 1 is closed.\n- **Confirm note next step: present, plain, correct for the buttons, incomplete for the letter.** The fixture set has no bill with a doubtful date, so I rendered all 7 reasons on case_09 a1, lib10 a2 and lib11 a2 by rewriting only `service_date` in the GET case response (same method as T-205 and the worker's test). Each shows the note, then \"What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself.\" It sits in the card foot above the buttons and needs no scrolling (screenshot note-lib11-ambiguous_numeric.png).\n- **\"Type the date into your letter yourself\": acceptable as the note, not enough on its own.** I will do it, but only because the tool cannot record a confirmed date, and the note says so honestly. What I would not accept is leaving it at that. The letter line it points to is not a placeholder: it is prose \"(statement dated June 15, 2026; service date not stated)\" with no blank to fill. My `[Ex. __ / Bates __]` find does not catch it. If I type the date and forget to delete that parenthetical, the letter tells the adjuster the date is not stated beside a date. The internal notes do not list these lines either (ui-lib11-notes.txt:35, \"Bills to request\" is empty). That is a minor, not a blocker, because the text is visible in the letter and D-071 binds the parenthetical wording. The placeholder question goes to Chris below.\n\n```json\n{\"card\": \"T-206\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit 79714c6 (git archive extracted to session scratchpad a206/); app http://127.0.0.1:7994 demo mode (fixture backend, curated set, ZLAYT_MODE=local, health demo_mode true); lib11 (library tile, the case asked for), plus case_09 and lib10 for the dated-line regression check. Display only; no T-202 r3 parse changes graded. Private values seen: 0.\",\n \"exercised\": [\"Read personas/paralegal.md, reviews/T-205-paralegal.md (my minors), board show T-206 (AC and handoff), git show 79714c6 (step3.js diff: stmtDated, BILL_DOC, confirmNext), tests/e2e/guided/test_t206.py in the archive, app/backend/export.py:218-227 and service_date.py in the archive\",\n  \"git archive 79714c6 into scratchpad a206; started the server on 7994 with LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local via artifacts/review-evidence/T-060-paralegal-pass4-serve.py; health demo_mode true; killed PID 81680 afterward and confirmed lsof exit 1 and curl 000\",\n  \"artifacts/review-evidence/T-206-paralegal/p01.py via h.py (lib11): library tile, Step 1 to Step 4 by keyboard, a DOM probe on every Step 3 card with a regex for any month-name date not preceded by 'statement dated', and card head, source head and line-sub capture; output p01.out (lib11), p01b.out (case_09, lib10), letter ui-lib11-letter.txt, notes ui-lib11-notes.txt\",\n  \"p02_notes.py / p02.out: all 7 confirm_note reasons on case_09 a1, lib10 a2 and lib11 a2 with only service_date stubbed in the GET case response; read confirm-next text, note position vs viewport; screenshots note-lib11-ambiguous_numeric.png, note-lib11-no_date.png, note-lib10-ambiguous_numeric.png, note-lib10-no_date.png, lib11-s3-01-a2.png (a2 card before counting)\",\n  \"Compared the Step 3 done list with the downloaded letter and the internal notes for lib11 (letter lines 39, 41, 43; notes line 35 empty 'Bills to request'); console and HTTP errors: none (ERRORS count 0 in p01.out, p01b.out, p02.out)\"],\n \"verdict\": \"pass\",\n \"scores\": {\"verify_quickly\": 4, \"no_bare_date_on_uncounted_lines\": 5, \"confirm_next_step_clear\": 4, \"next_step_correct_for_demand_letter_workflow\": 3},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"The next step stops at 'type the date into your letter yourself': the letter line is not a findable placeholder, nothing says to remove the 'service date not stated' text, and the notes do not list these lines\",\n   \"evidence\": \"ui-lib11-letter.txt:39, 41, 43: 'Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00' (and $180.00, $2,310.00). The only blanks in that letter are the '[Ex. __ / Bates __]' ones (grep -c '__' = 12, all Source lines). p02.out:2 (and 20 more): 'What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it. If you count it, type the date into your letter yourself.' ui-lib11-notes.txt:35: 'BILLS TO REQUEST (entry in the letter, no accepted charge)' is empty, and no section lists the three counted ledger lines as needing a date. export.py:218-227 (archive) builds the line from service_date.not_stated_text.\",\n   \"why_it_matters\": \"I can type a date, but the tool gives me no marker to search for and no list of which lines need one. If I leave the parenthetical in, the letter says the date is not stated next to the date I typed, and the adjuster reads both. I want the date position to be a blank, like the exhibit cite, and the notes to name each counted line that still needs a date.\",\n   \"fix\": \"Either (a) put a blank in the letter for a counted line with no date, e.g. 'Fennimoor Spine Clinic, itemized ledger [Date of service __] (statement dated June 15, 2026): $250.00', so the same find-the-underscores pass catches it; or (b) keep the D-071 parenthetical and add to the note 'then delete the words service date not stated', and add a line to the internal notes for each counted charge with no date of service ('type the date or request a dated itemized bill'). If D-071 forbids (a), that is Chris's call.\",\n   \"acceptance_test\": \"Export test on lib11 with a2 to a4 counted: the letter contains no 'service date not stated' text without a blank to fill, or the note names removing it; the internal notes list the three counted lines as needing a service date. E2E: the confirm-next sentence mentions replacing the not-stated words.\"},\n  {\"severity\": \"minor\", \"title\": \"For the 'no date' reason the note tells me to check a date in the highlighted words, when the line has none\",\n   \"evidence\": \"p02.out:14-15 (case_09/no_date), 29-30 (lib10), 45-46 (lib11): note 'The line states no date of service. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.' followed by 'What to do: check the date in the highlighted words, then press Yes, count it or No, don't count it.' Screenshot note-lib11-no_date.png. The same four sentences are shown for every reason, including no_date.\",\n   \"why_it_matters\": \"On a ledger line like lib11 a2 the quote has no date at all, so 'check the date in the highlighted words' has nothing to check; the note and the next step both send me looking for a date that is not there. no_date is the reason these ledger lines would actually hit, so it is the case that matters.\",\n   \"fix\": \"Vary the next step by reason: for no_date, 'the line has no date of service; press Yes, count it only if you checked the ledger yourself, and add the date to your letter from the provider's bill'. Keep the shared wording for the date-reading reasons.\",\n   \"acceptance_test\": \"Unit or E2E per reason: for reason no_date the confirm-next text does not say 'check the date in the highlighted words'; for the other six it does.\"},\n  {\"severity\": \"nit\", \"title\": \"The E2E covers one reason and pins the wording, not the letter\",\n   \"evidence\": \"tests/e2e/guided/test_t206.py (archive): test_a_doubtful_date_note_ends_with_what_to_do_next uses reason ambiguous_numeric only; test_the_next_step_fits_a_phone uses no_year. It asserts the sentence 'type the date into your letter yourself' is present and never opens Step 4.\",\n   \"why_it_matters\": \"The finding above went through the test because nothing checks that the letter gives me somewhere to type the date.\",\n   \"fix\": \"Add the no_date reason and a Step 4 assertion for a counted undated line.\",\n   \"acceptance_test\": \"A parametrized test over all 7 reasons plus one Step 4 check for a counted undated line.\"}\n ],\n \"whats_right\": [\"The label 'statement dated June 15, 2026' is now on every ledger, UB-04 and EOB card (head, line under it, source head), certain visit dates stay plain, and the Step 3 done list equals the letter text.\",\n  \"The confirm note leads the card foot under the highlighted quote with a plain 'What to do' line that names the two buttons the card really has, and it does not promise a fix control the tool does not have.\",\n  \"Yes and No stay enabled and the note fits at 1440x900 with no scrolling and no console or HTTP errors.\"],\n \"questions_for_chris\": [\"Does D-071 allow a visible fill-in blank, such as [Date of service __], in the letter on a counted line with no date of service, in place of the 'service date not stated' parenthetical? As a paralegal I would take the blank; the parenthetical is acceptable only if the note also says to delete it and the internal notes list the line.\"]}\n```\n"
}
````

### User / tool · 2026-11-03T00:46:25.237Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-206-paralegal.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:46:27.912Z

T-206 passes with 3 minors and no blockers. lib11 uncounted ledger lines now read "statement dated June 15, 2026" with no bare date. The confirm note's next step names the two real buttons. The letter side is thin: the undated line is a parenthetical, not a fillable blank, so I'd want a `[Date of service __]` placeholder (question for Chris). The note also tells me to check a date for the "no date" reason, when the line has none. Review is at `/Users/arsis/zlayt-pm-project/reviews/T-206-paralegal.md`; my PID 81680 is stopped.
