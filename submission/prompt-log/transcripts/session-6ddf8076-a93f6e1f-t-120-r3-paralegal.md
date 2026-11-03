# Subagent: T-120 r3 paralegal (T-120 r3 paralegal)

Source: `agent-a93f6e1f3ed3172e0.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:43:17.039Z

This is the round-3 paralegal re-check of board card T-120 in /Users/arsis/zlayt-pm-project. Read reviews/T-120-paralegal-r2.md and `python3 tools/board.py show T-120`.

Run the app from a `git archive HEAD` copy in your scratchpad on a spare port: fixture backend, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad. Re-test your r2 blocker sentences, including 'Hx obtained via patient's son, who reports neck pain.', and confirm that the interpreter-only sentence raises no flag. Add 5 new history sentences of your own.

Write reviews/T-120-paralegal-r3.md with a ```json block of real values: card, persona paralegal-reviewer, model claude-haiku-5-5, verdict, findings. Stop your server by PID. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:43:19.004Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T11:43:19.010Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T11:43:19.210Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-120-paralegal-r2.md"
}
````

### User / tool · 2026-11-02T11:43:19.222Z

**tool result**
````
1	# T-120 paralegal re-check (round 2)
2	
3	**Verdict: fail.** One blocker, the same class as round 1. The colon forms from the r1 blocker now raise the prior flag again. But the skip still hides a prior condition in a history-source sentence whenever the sentence has no colon, no digit and no "of", for example "Hx obtained via patient's son, who reports neck pain." The pre-T-120 build flags that sentence. HEAD does not.
4	
5	Scope: HEAD 433ac1c (contains 07dbd2b, the T-120 r2 commit) as a `git archive` copy in the session scratchpad, fixture backend, ZLAYT_MODE=local, port 7895, listener PID 17734 (stopped; port closed, curl returns 000). Baselines are also archive copies: 0c47356 (pre-T-120, the parent of 1cb8707) and 07dbd2b (r2). The paste route is refused on HEAD with 409 demo_mode_unsupported_input (demo_mode is true even with ZLAYT_MODE=local), so my own sentences went through the same engine the pipeline calls (flags.lexicon_flags, flags.py:80, which the pipeline calls at flags.py:249). Each sentence was put in lib09 record 1 with its excerpt replaced. The card's "record 2" is record 1.
6	
7	## Re-test of the r1 blocker and the interpreter-only sentence
8	
9	Full table: artifacts/review-evidence/T-120-r2-compare.txt. Labels S1 to S16 match the probe script.
10	
11	| # | Probe sentence | Pre-T-120 | HEAD 433ac1c | Expected | OK |
12	|---|---|---|---|---|---|
13	| S1 | PHx obtained via patient's son: lumbar strain 2019. (r1 blocker) | flag | flag | flag | yes |
14	| S2 | Hx obtained via patient's son, who interpreted. (interpreter-only) | flag | none | none | yes |
15	| S3 | Hx obtained via interpreter: lumbar strain 2019. | flag | flag | flag | yes |
16	| S4 | Hx obtained via patient's son, who reports neck pain. | flag | none | flag | NO |
17	| S5 | Hx obtained via patient's son, who reports chronic neck pain. | flag | flag | flag | yes |
18	| S6 | Hx obtained via patient's son; neck pain and headaches. | flag | none | flag | NO |
19	| S7 | Hx per patient's son, who interpreted. | flag | none | none | yes |
20	| S8 | Hx via interpreter, who interpreted; prior neck injury. | flag | flag | flag | yes |
21	| S9 | Hx of lumbar strain obtained via patient's son. | flag | flag | flag | yes |
22	| S10 | Hx obtained via patient's son, who interpreted, lumbar strain 2019. | flag | flag | flag | yes |
23	| S11 | Hx obtained via EMS crew, who relayed lumbar strain. | flag | none | flag | NO |
24	| S12 | Hx obtained via patient's son, who interpreted. Lumbar strain was noted. | flag | none | none | yes |
25	| S13 | Hx obtained via patient's son, who interpreted. Prior lumbar strain 2019. | flag | flag | flag | yes |
26	| S14 | Hx: lumbar strain 2019. (control, no source phrase) | flag | flag | flag | yes |
27	| S15 | Hx obtained via patient's son, who interpreted, and reports lumbar strain. | flag | none | flag | NO |
28	| S16 | Hx obtained via patient's son, who interpreted, denies neck pain. | flag | none | none | yes |
29	
30	Live app (HEAD, library route, the only route that takes this sentence): case_lib09_spanish_interpreter_espalda is ready with no pre_existing flags, so the interpreter-only sentence in record 1 stays unflagged. Sample record 3 ("Patient reports low back pain in 2023, resolved.") and record 8 ("Findings may represent degenerative change") still flag. lib02 and lib11 still flag their prior mentions. Evidence: artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json.
31	
32	## Findings
33	
34	### 1. blocker: the source-sentence skip still drops a prior condition that has no colon, digit or "of"
35	
36	- Four of the 16 probes (S4, S6, S11, S15) raise a pre_existing flag before T-120 and raise none on HEAD. The raw lexicon hit on the pre-T-120 build is `hx_abbrev`; on HEAD the lexicon finds nothing at all for the same sentences (`lexicon_hit_ids` is empty).
37	- Cause: `app/backend/lexicon_scan.py:107-115` (`_is_source_sentence`) returns False only when the rest of the sentence contains a colon, a digit or the word "of" (line 115: `return not re.search(r":|\d|\bof\b", rest, re.I)`). Line 152 then drops the `hx_abbrev` hit for every other source sentence.
38	- The unit tests do not cover this shape. Every REAL row that must still flag carries a colon, a digit or "of" (`tests/unit/test_t120_history_source_sentence.py:14-17`). `pytest tests/unit/test_t120_history_source_sentence.py` on the HEAD archive: 28 passed.
39	
40	Why it matters: checklist item 9 and card AC 1 require a real prior-condition mention to raise the flag. The r2 commit message says the skip applies only "when the sentence names no condition", but the check tests punctuation and one word, not the condition. A history line such as "who reports neck pain" gets no prior flag, and the adjuster reads that same line in the record. This is the r1 blocker for a different shape. The rule removes a guess (the source phrase is not a prior) and deletes the condition next to it. I am not downgrading it because the shape is less common than the colon form.
41	
42	Suggested direction (the fix owner decides the exact rule): skip only when the words after the source phrase are the attribution and nothing else, from a closed list such as "who interpreted", "who translated" or "who relayed", followed by the end of the clause. Any other word after the source phrase keeps the hit. The colon, digit and "of" cases already pass and should stay as they are.
43	
44	Acceptance test: add S4, S6, S11 and S15 (verbatim, as in the table) to REAL and assert `flags.lexicon_flags` returns a pre_existing flag for each. Keep S2 and S7 in SOURCE (no flag). Re-run `artifacts/review-evidence/T-120-r2-paralegal-probe.py engine` on the fixed archive and `T-120-r2-paralegal-compare.py`: every row must match its Expected column. Re-run `http` mode: lib09 record 1 pre_existing stays empty, and sample r3 and r8 still flag.
45	
46	### 2. minor: card AC 1 still cites "record 2" and a test name that no longer exists (carried from r1)
47	
48	- `python3 tools/board.py show T-120` prints AC 1 as "the interpreter-history sentence of record 2", and its evidence as "tests/unit/test_t120_history_source_sentence.py::test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes".
49	- HEAD has `def test_lib09_record_1_raises_no_prior_condition_flag_and_other_prior_mentions_still_do` at `tests/unit/test_t120_history_source_sentence.py:44`. The sentence is in lib09 record 1 (`lib09_record_numbers_with_source_sentence = [1]`).
50	- Why it matters: checklist item 3. A paralegal who opens record 2 will not find the sentence. The r2 handoff says the AC text "cannot be edited by hand", so the correction goes through the board, not a hand edit.
51	- Acceptance test: `board.py show T-120` shows "record 1" in AC 1, and its evidence names `test_lib09_record_1_...`.
52	
53	## Not re-tested this round
54	
55	- The r1 nit on positional flag ids (`f_r1_1` changed meaning). I did not check whether decisions carry over, so I make no claim either way.
56	- The live LLM merge path (flags.py:249). Fixture mode cannot run unseen text, and the paste route is refused at HEAD. The probe covers the lexicon path only.
57	
58	## What I exercised
59	
60	- Read `personas/paralegal.md` in full, `reviews/T-120-paralegal.md`, `python3 tools/board.py show T-120`, and my memory notes on T-120/T-123 and reviewer tooling.
61	- `git rev-parse HEAD` gave 433ac1c. Extracted `git archive --prefix=zlayt-head/ HEAD`, plus 07dbd2b and 0c47356, into the session scratchpad with `git archive ... | tar -x`.
62	- Started the app from the HEAD archive with ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, LLM_BACKEND=fixture, FIXTURE_SET=curated, PORT=7895. Listener PID 17734 (`python -m app.main`). Log: artifacts/review-evidence/T-120-r2-paralegal-server.log.
63	- HTTP (`T-120-r2-paralegal-probe.py http`): `/api/health`; paste POST with a history sentence (409 demo_mode_unsupported_input); library cases lib09, lib02, lib11 and the sample, each run to ready and read back through GET.
64	- Engine (`T-120-r2-paralegal-probe.py engine`, `-I`) on HEAD, 07dbd2b and 0c47356: 16 sentences through `flags.lexicon_flags` and `lexicon_scan.scan`. Compare output: artifacts/review-evidence/T-120-r2-compare.txt.
65	- `pytest tests/unit/test_t120_history_source_sentence.py` on the HEAD archive: 28 passed.
66	- Stopped the server: `kill 17734`, then `lsof` on 7895 returned nothing, `curl` returned 000, and `ps` showed no PID 17734.
67	
68	```json
69	{"card": "T-120", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
70	 "scope": "HEAD 433ac1c (includes 07dbd2b, T-120 r2) as a git archive copy in the session scratchpad; app on http://127.0.0.1:7895 (fixture backend, ZLAYT_MODE=local, listener PID 17734, stopped); paste route refused 409 (demo_mode true); engine probes via app.backend.flags.lexicon_flags and lexicon_scan.scan on lib09 record 1 with the excerpt replaced; baselines 0c47356 (pre-T-120) and 07dbd2b (r2) as git archive copies; library cases lib09, lib02, lib11 and sample evals/golden/sample.txt",
71	 "exercised": [
72	  "read personas/paralegal.md, reviews/T-120-paralegal.md, board show T-120, memory notes t120-123-patterns and reviewer tooling",
73	  "git archive --prefix=zlayt-head/ HEAD | tar -x (433ac1c), plus zlayt-r2 (07dbd2b) and zlayt-base (0c47356) in the session scratchpad",
74	  "started python -m app.main from the HEAD archive on PORT=7895 with ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, LLM_BACKEND=fixture; log artifacts/review-evidence/T-120-r2-paralegal-server.log",
75	  "HTTP probe artifacts/review-evidence/T-120-r2-paralegal-probe.py http: /api/health (demo_mode true), paste POST returned 409 demo_mode_unsupported_input, library lib09/lib02/lib11 and sample run to ready and read via GET; output artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json",
76	  "engine probe artifacts/review-evidence/T-120-r2-paralegal-probe.py engine (python -I) on HEAD, 07dbd2b and 0c47356: 16 sentences (S1 to S16) through flags.lexicon_flags and lexicon_scan.scan; outputs artifacts/review-evidence/T-120-r2-engine-*.json",
77	  "artifacts/review-evidence/T-120-r2-paralegal-compare.py > artifacts/review-evidence/T-120-r2-compare.txt: per-sentence table, all three builds",
78	  "pytest tests/unit/test_t120_history_source_sentence.py on the HEAD archive: 28 passed",
79	  "python3 tools/board.py show T-120 (AC 1 wording and evidence string)",
80	  "grep of lexicon_scan.py (lines 107, 115, 152) and test file (REAL rows 14-17, test_lib09_record_1 at line 44) on the HEAD archive",
81	  "kill 17734; lsof on 7895 empty; curl returned 000; ps showed no PID 17734"],
82	 "verdict": "fail",
83	 "scores": {"verify_quickly": 3, "prior_mentions_flagged": 3, "interpreter_sentence_not_flagged": 5},
84	 "findings": [
85	  {"severity": "blocker",
86	   "title": "Source-sentence skip still drops a prior condition named without a colon, digit or 'of' (S4, S6, S11, S15: flagged before T-120, not flagged on HEAD)",
87	   "evidence": "artifacts/review-evidence/T-120-r2-compare.txt rows S4, S6, S11, S15: pre-T-120 True, HEAD False, expected flag. Pre-T-120 raw hit on each is hx_abbrev (artifacts/review-evidence/T-120-r2-engine-base-0c47356.json). On HEAD lexicon_hit_ids is empty for the same four (artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json). Cause: app/backend/lexicon_scan.py:107-115 _is_source_sentence returns False only when the rest of the sentence contains a colon, a digit or the word of (line 115: return not re.search(r':|\\d|\\bof\\b', rest, re.I)); line 152 drops the hx_abbrev hit otherwise. Probe sentences, verbatim: 'Hx obtained via patient's son, who reports neck pain.' ; 'Hx obtained via patient's son; neck pain and headaches.' ; 'Hx obtained via EMS crew, who relayed lumbar strain.' ; 'Hx obtained via patient's son, who interpreted, and reports lumbar strain.' Unit tests miss this shape: REAL rows tests/unit/test_t120_history_source_sentence.py:14-17 all carry a colon, a digit or of; 28 passed on the HEAD archive.",
88	   "why_it_matters": "Checklist item 9 and card AC 1 require a real prior-condition mention to raise the flag. The r2 commit message says the skip applies only when the sentence names no condition, but the check tests punctuation and one word, not the condition. A history line such as 'who reports neck pain' gets no prior flag, and the adjuster reads the same line in the record. This is the r1 blocker for a different shape: the rule removes a guess (the source phrase is not a prior) and deletes the condition next to it. Not downgraded because the shape is less common than the colon form.",
89	   "fix": "Skip only when the words after the source phrase are the attribution and nothing else: a closed list such as 'who interpreted', 'who translated', 'who relayed', then the end of the clause. Any other word after the source phrase keeps the hit. Keep the colon, digit and of cases as they are. The fix owner decides the exact rule.",
90	   "acceptance_test": "Add the four sentences above verbatim to REAL in tests/unit/test_t120_history_source_sentence.py and assert flags.lexicon_flags returns a pre_existing flag for each. Keep 'Hx obtained via patient's son, who interpreted.' and 'Hx per patient's son, who interpreted.' in SOURCE (no flag). Re-run artifacts/review-evidence/T-120-r2-paralegal-probe.py engine on the fixed archive and T-120-r2-paralegal-compare.py: every row must match its expect column. Re-run http mode: lib09 record 1 pre_existing stays empty; sample records 3 and 8 still flag."},
91	  {"severity": "minor",
92	   "title": "Card AC 1 still cites lib09 record 2 and a test name that no longer exists (carried from r1; r2 renamed the test to record_1)",
93	   "evidence": "python3 tools/board.py show T-120 AC 1: 'the interpreter-history sentence of record 2'; evidence 'tests/unit/test_t120_history_source_sentence.py::test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes'. HEAD defines test_lib09_record_1_raises_no_prior_condition_flag_and_other_prior_mentions_still_do at tests/unit/test_t120_history_source_sentence.py:44. The sentence is in lib09 record 1 (artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json: lib09_record_numbers_with_source_sentence = [1]).",
94	   "why_it_matters": "Checklist item 3: a paralegal who opens record 2 will not find the sentence, and the card's evidence names a test that no longer exists. The r2 handoff says the AC text cannot be edited by hand, so the correction goes through the board.",
95	   "fix": "Correct AC 1 text and its evidence string to record 1 and test_lib09_record_1_... through the board (orchestrator to choose the route).",
96	   "acceptance_test": "python3 tools/board.py show T-120 shows 'record 1' in AC 1, and the evidence names test_lib09_record_1_...; the test exists at tests/unit/test_t120_history_source_sentence.py:44."}
97	 ],
98	 "whats_right": [
99	  "The r1 blocker shapes now flag on HEAD: 'PHx obtained via patient's son: lumbar strain 2019.' and 'Hx obtained via interpreter: lumbar strain 2019.' (compare rows S1, S3)",
100	  "The interpreter-only sentence stays unflagged, in the engine ('Hx obtained via patient's son, who interpreted.', S2) and on the live lib09 case (pre_existing list empty)",
101	  "Live sample and library priors still flag: sample record 3 'Patient reports low back pain in 2023, resolved.' and record 8 'Findings may represent degenerative change'; lib02 and lib11 keep their prior flags"],
102	 "questions_for_chris": [
103	  "Should the history-source skip be a closed list of attribution phrases (my suggested direction), or should the Hx hit be dropped only when the whole sentence is the attribution? Your call on the rule; I only need every condition-naming history line to keep its flag.",
104	  "The live LLM merge path (flags.py:249) is still untested: fixture mode cannot run unseen text and the paste route returns 409 at HEAD. Can the model raise a prior flag on the Hx sentence in the live backend?"]
105	}
106	```
107	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:43:19.493Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-120",
 "description": "Show board card T-120"
}
````

### User / tool · 2026-11-02T11:43:19.630Z

**tool result**
````
---
id: "T-120"
title: "No prior-condition flag on an interpreter sentence ('Hx obtained via patient's son, who interpreted')"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T10:41:17Z"
updated_at: "2026-11-02T11:43:08Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:27:48Z"
rounds: 2
commits: ["1cb8707", "07dbd2b", "f7829c1"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-120-staff-engineer.md", "at": "2026-11-02T11:21:45Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-120-paralegal.md", "at": "2026-11-02T11:25:55Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-120-paralegal-r2.md", "at": "2026-11-02T11:33:21Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-120-staff-engineer-r2.md", "at": "2026-11-02T11:35:59Z"}
ac:
  - {"n": 1, "text": "lib09 raises no 'Mention of a prior or pre-existing condition' flag on the interpreter-history sentence of record 2; a real prior-condition mention in another record still raises the flag (unit test for both)", "done": true, "evidence": "tests/unit/test_t120_history_source_sentence.py::test_lib09_record_1_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes (the sentence is lib09 record 1; AC text says record 2 in error); r3 rows: 32 staff probes, paralegal S4/S6/S11/S15, parent-regression forms"}
  - {"n": 2, "text": "tests/unit covers the rule so it cannot regress; evals report unchanged otherwise", "done": true, "evidence": "95 tests in test_t120_history_source_sentence.py; 12 guard mutants all killed; unit suite 3123 passed; evals fixture report evals/reports/20261102T114138Z.md flag precision/recall 1.000 all types"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T10:41:20Z frontend: Filed by frontend from T-060 pass-2 paralegal F13 (reviews/T-060-paralegal-pass2.md). Frontend cannot change it: the flag comes from the backend flag engine.
- 2026-11-02T11:02:21Z backend: claimed
- 2026-11-02T11:11:30Z backend: AC 1 checked: tests/unit/test_t120_history_source_sentence.py::test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes; real prior mentions still hit (REAL rows)
- 2026-11-02T11:11:31Z backend: AC 2 checked: 17 tests in test_t120_history_source_sentence.py; fixture evals.run flag precision/recall all 1.000, no change
- 2026-11-02T11:11:31Z backend: moved in_progress -> in_review
- 2026-11-02T11:14:34Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer
- 2026-11-02T11:21:45Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-120-staff-engineer.md; round 1; findings:
    - [major] The `Hx per ...` branch drops the flag on real prior-condition mentions — fix: Narrow the `per`/`via` branch so it skips only when the source phrase ends the clause or is followed by an interpreter/family-member noun and no condition text (or only skip the `Hx` token and let the remaining clause scan run). Do not skip when a colon, 'of', a year or a condition word follows the source.
- 2026-11-02T11:21:45Z orchestrator: assigned: backend
- 2026-11-02T11:25:55Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): fail — reviews/T-120-paralegal.md
- 2026-11-02T11:26:08Z orchestrator: assigned: backend
- 2026-11-02T11:27:48Z backend: claimed
- 2026-11-02T11:27:48Z backend: r2: per/via only before a person/channel noun; skip only when the rest of the sentence has no colon, digit or 'of' (PHx obtained via patient's son: lumbar strain 2019 and Hx per patient: ... hit). Mutants widening via or removing the rest check are killed. Citation corrected: the interpreter sentence is lib09 record 1 (r1); test renamed test_lib09_record_1_*; AC text says record 2 and cannot be edited by hand. Flag ids are positional (f_r1_1 changed meaning); the lib09 J4 fixture was re-recorded live (T-125).
- 2026-11-02T11:27:48Z backend: moved in_progress -> in_review
- 2026-11-02T11:28:05Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer
- 2026-11-02T11:33:21Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): fail — reviews/T-120-paralegal-r2.md; round 2; findings:
    - [blocker] Source-sentence skip still drops a prior condition named without a colon, digit or 'of' (S4, S6, S11, S15: flagged before T-120, not flagged on HEAD) — fix: Skip only when the words after the source phrase are the attribution and nothing else: a closed list such as 'who interpreted', 'who translated', 'who relayed', then the end of the clause. Any other word after the source phrase
    - [minor] Card AC 1 still cites lib09 record 2 and a test name that no longer exists (carried from r1; r2 renamed the test to record_1) — fix: Correct AC 1 text and its evidence string to record 1 and test_lib09_record_1_... through the board (orchestrator to choose the route).
- 2026-11-02T11:33:21Z orchestrator: Design direction for round 3 (orchestrator): stop guessing whether a sentence 'names a condition'. Instead, strip only the history-source attribution phrase itself (e.g. 'Hx obtained via patient's son', ', who interpreted', 'per patient') and run the normal prior-condition scan on whatever text remains, so 'who reports neck pain' and 'lumbar strain 2019' still flag, and a sentence that is only attribution yields nothing. Test with all forms from both paralegal reviews and the staff review.
- 2026-11-02T11:33:29Z orchestrator: moved changes_requested -> blocked: held until staff r2 (in flight) returns, so round 3 fixes both reviews at once
- 2026-11-02T11:35:59Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-120-staff-engineer-r2.md
- 2026-11-02T11:35:59Z orchestrator: moved blocked -> in_progress
- 2026-11-02T11:35:59Z orchestrator: assigned: backend
- 2026-11-02T11:42:15Z backend: AC 1 checked: tests/unit/test_t120_history_source_sentence.py::test_lib09_record_1_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes (the sentence is lib09 record 1; AC text says record 2 in error); r3 rows: 32 staff probes, paralegal S4/S6/S11/S15, parent-regression forms
- 2026-11-02T11:42:15Z backend: AC 2 checked: 95 tests in test_t120_history_source_sentence.py; 12 guard mutants all killed; unit suite 3123 passed; evals fixture report evals/reports/20261102T114138Z.md flag precision/recall 1.000 all types
- 2026-11-02T11:42:15Z backend: moved in_progress -> in_review
- 2026-11-02T11:43:08Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer

## Handoff
What changed: r3 drops the condition-guessing proxy (colon/digit/'of'). lexicon_scan._is_source_sentence now strips only the attribution phrase after Hx (verb+via/from/per + closed list of people/channels + ', who interpreted') and keeps the hit if any word is left in the sentence (newline does not end it; Dr. is part of the name). Only-attribution sentences yield nothing. How verified: 95 tests (all 32 staff probes minus 2 where bare 'History' has no lexicon entry and parent did not flag either; paralegal S4/S6/S11/S15 and r1 forms; 6 parent-regression forms asserting the Hx hit itself; M2/M8 mutants plus 12 more killed); unit suite 3123 passed; evals fixture report evals/reports/20261102T114138Z.md flags 1.000. Left: S16 ('who interpreted, denies neck pain') still flags (over-flag, safe direction; was flagged pre-T-120). Surprised: staff probes 'History provided by wife, notable for lumbar strain' have no lexicon hit at all (needs a researcher entry for bare 'History').
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:43:25.080Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git log --oneline -5 && ls artifacts/review-evidence/ | grep -i t-120 ; echo ---; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t120-r2-patterns.md; echo ---; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md; echo ---; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md",
 "description": "Check HEAD, T-120 evidence files, and memory notes"
}
````

### User / tool · 2026-11-02T11:43:25.217Z

**tool result**
````
f7829c1ccecb224875a1d79a6255ff4b109eed67
f7829c1 fix(backend): T-120 r3 history-source skip strips only the attribution phrase and scans what is left (no condition guessing)
93de5f2 feat(backend): T-127 keep gap_change on the gap flag, gap_changes_removed in GET case
3a74f75 fix(backend): T-129 a preamble no longer shifts record numbers
3d53ca5 feat(backend): T-128 summary trim never leaves a fragment, pin r3 mutants
433ac1c test(backend): T-123 pin which record is named as paperwork in either order (kills the provider-ordering mutant)
T-120-123-paralegal-common.py
T-120-123-paralegal-jsoncheck.py
T-120-123-paralegal-probe.out.json
T-120-123-paralegal-probe.py
T-120-paralegal-before-after-HEAD.txt
T-120-paralegal-before-after-parent.txt
T-120-paralegal-before-after.py
T-120-paralegal-dbg.py
T-120-paralegal-draft.md
T-120-paralegal-engine-HEAD.txt
T-120-paralegal-engine-parent.txt
T-120-paralegal-engine.py
T-120-paralegal-explore.py
T-120-paralegal-explore2.py
T-120-paralegal-flags-diff-HEAD.txt
T-120-paralegal-flags-diff-parent.txt
T-120-paralegal-flags-diff.py
T-120-paralegal-variants-HEAD.txt
T-120-paralegal-variants-parent.txt
T-120-paralegal-variants.py
T-120-r2-compare.txt
T-120-r2-engine-07dbd2b.json
T-120-r2-engine-HEAD-433ac1c.json
T-120-r2-engine-base-0c47356.json
T-120-r2-http-HEAD-433ac1c.json
T-120-r2-paralegal-compare.py
T-120-r2-paralegal-probe.py
T-120-r2-paralegal-server.log
---
---
name: t120-r2-patterns
description: T-120 r2 re-check (2026-11-02, HEAD 433ac1c): colon forms fixed, but condition-naming history lines without colon/digit/of still lose the prior flag; probe method and paste-route 409
metadata:
  type: project
---

T-120 r2 (07dbd2b, in HEAD 433ac1c): the colon fix works. "PHx obtained via patient's son: lumbar strain 2019." and "Hx obtained via interpreter: lumbar strain 2019." flag again. The interpreter-only sentence stays unflagged. Still failing: a source sentence whose rest has NO colon, digit or "of" drops the hx_abbrev hit even when it names a condition. Probes that lost the flag vs the pre-T-120 build (0c47356): "Hx obtained via patient's son, who reports neck pain.", "Hx obtained via patient's son; neck pain and headaches.", "Hx obtained via EMS crew, who relayed lumbar strain.", "...who interpreted, and reports lumbar strain." Verdict fail (blocker, same class as r1). Also still open: card AC 1 says "record 2" and cites a test name that r2 renamed to record_1 (board edits only).

**Why:** the rule is a punctuation/word proxy ("names a condition") and the lexicon has no entry for bare condition nouns like "neck pain". So the proxy is the only thing between the source phrase and the flag. Unit REAL rows all carry a colon, digit or "of", so 28 green tests missed the shape.

**How to apply:** for any source-phrase or history-skip change, probe sentences that name a condition in each of these shapes: colon, semicolon, comma-and, "who reports", digit, "of", a lexicon word ("chronic"), and a negated one ("denies"). Compare on the pre-change parent. The engine is enough when the paste route is refused: `ARCH=<archive> .venv/bin/python -I artifacts/review-evidence/T-120-r2-paralegal-probe.py engine`, which swaps the excerpt of lib09 record 1 and calls flags.lexicon_flags.

**Paste route:** at HEAD, /api/health says demo_mode true even with ZLAYT_MODE=local, so POST /api/cases with any non-library text returns 409 demo_mode_unsupported_input. Live checks are library cases only (lib09, lib02, lib11, sample). Only lib09 holds the interpreter sentence, so the live check cannot reach the failing shape.

**Flag JSON shape (for scripts):** case flags have no top-level excerpt or record_no. Use `evidence[0].record_id` and `evidence[0].excerpt`. The first version of my probe read the wrong keys and reported None.

Related: [[t120-123-patterns]] (r1), [[feedback_spec_review_patterns]] (check the claim against its own example shape).
---
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

## T-120 r2 additions (2026-11-02)
- The guard refused Edit on reviews/T-120-paralegal-r2.md right after the single Write (the name has no -rN suffix, so it is treated as existing and append-only). Two wording slips were found after the Write: "lib02 and lib11 keep their prior flags" (I had not compared them to the pre-T-120 build) and "r2 handoff" (the line is the r2 backend note). They could not be fixed in the file; they went into the one-line reply.
- Before the Write, check each "keeps / still / unchanged" claim against a run you have actually done, not against memory of the build.
---
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:43:48.327Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-120-r2-paralegal-probe.py; echo ---LOG; head -20 artifacts/review-evidence/T-120-r2-paralegal-server.log; echo ---COMPARE; cat artifacts/review-evidence/T-120-r2-compare.txt | head -5",
 "description": "Read r2 probe script, server log head, compare output"
}
````

### User / tool · 2026-11-02T11:43:48.414Z

**tool result**
````
"""T-120 r2 paralegal-reviewer probe (stdlib + the archive's own app code).

Two modes, both run with the project venv and -I:
  ARCH=<git archive copy> .venv/bin/python -I <this file> engine
      Same record dict through flags.lexicon_flags (the flag engine the pipeline calls) and lexicon_scan.scan.
      The record is lib09 record 1 with its excerpt replaced by each probe sentence (the card's 'record 2' is record 1).
  ZLAYT_BASE=http://127.0.0.1:7895 .venv/bin/python -I <this file> http
      Live app: paste route (expect 409 demo_mode_unsupported_input) and the library cases lib09, lib02, lib11 and the sample.

Output is JSON on stdout; the review cites the redirected files under artifacts/review-evidence/.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

MODE = sys.argv[1] if len(sys.argv) > 1 else "engine"

# (label, probe sentence, reviewer expectation for a pre_existing flag)
SENTENCES = [
    ("S1 blocker: PHx via son, colon, year", "PHx obtained via patient's son: lumbar strain 2019.", "flag"),
    ("S2 interpreter-only (lib09 r1 lead sentence)", "Hx obtained via patient's son, who interpreted.", "no flag"),
    ("S3 Hx via interpreter, colon, year", "Hx obtained via interpreter: lumbar strain 2019.", "flag"),
    ("S4 names condition, no colon/digit/of, no lexicon word", "Hx obtained via patient's son, who reports neck pain.", "flag"),
    ("S5 names condition with lexicon word 'chronic'", "Hx obtained via patient's son, who reports chronic neck pain.", "flag"),
    ("S6 semicolon, names condition, no digit", "Hx obtained via patient's son; neck pain and headaches.", "flag"),
    ("S7 per son, no condition", "Hx per patient's son, who interpreted.", "no flag"),
    ("S8 via interpreter, prior lexicon phrase after semicolon", "Hx via interpreter, who interpreted; prior neck injury.", "flag"),
    ("S9 'Hx of' then source phrase (not a source sentence)", "Hx of lumbar strain obtained via patient's son.", "flag"),
    ("S10 source sentence with year, no colon", "Hx obtained via patient's son, who interpreted, lumbar strain 2019.", "flag"),
    ("S11 EMS crew relayed, names condition, no digit", "Hx obtained via EMS crew, who relayed lumbar strain.", "flag"),
    ("S12 source sentence then a non-prior second sentence", "Hx obtained via patient's son, who interpreted. Lumbar strain was noted.", "no flag"),
    ("S13 source sentence then a dated prior second sentence", "Hx obtained via patient's son, who interpreted. Prior lumbar strain 2019.", "flag"),
    ("S14 plain Hx with colon, no source phrase (control)", "Hx: lumbar strain 2019.", "flag"),
    ("S15 names condition after 'and', no colon/digit/of", "Hx obtained via patient's son, who interpreted, and reports lumbar strain.", "flag"),
    ("S16 negated condition after source phrase", "Hx obtained via patient's son, who interpreted, denies neck pain.", "no flag"),
]


def engine():
    arch = os.environ["ARCH"]
    sys.path.insert(0, arch)
    sys.dont_write_bytecode = True
    from app.backend import flags as FL, ingest as I, lexicon_scan as LS  # noqa: E402
    lib = os.path.join(arch, "evals/library/case_lib09_spanish_interpreter_espalda.txt")
    recs = I.ingest(open(lib, encoding="utf-8").read())["records"]
    base = next(r for r in recs if "Hx obtained via" in r["excerpt"])
    out = {"arch": arch, "lib09_record_numbers_with_source_sentence": [r["n"] for r in recs if "Hx obtained via" in r["excerpt"]],
           "lib09_record1_unchanged_pre_existing": [f["excerpt"] for f in FL.lexicon_flags(base) if f["type"] == "pre_existing"],
           "probes": []}
    for label, exc, expect in SENTENCES:
        rec = dict(base, excerpt=exc)
        pre = [f["excerpt"] for f in FL.lexicon_flags(rec) if f["type"] == "pre_existing"]
        raw = sorted({h["id"] for h in LS.scan(exc) if h["flag_type"] == "pre_existing"})
        out["probes"].append({"label": label, "text": exc, "expect": expect,
                              "pre_existing_flags": pre, "raised": bool(pre), "lexicon_hit_ids": raw})
    return out


BASE = os.environ.get("ZLAYT_BASE", "http://127.0.0.1:7895")


def req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method, headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=180) as x:
            return x.status, json.loads(x.read() or b"null")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw or b"null")
        except ValueError:
            return e.code, raw.decode("utf-8", "replace")


def poll(tok):
    assert req("POST", f"/api/cases/{tok}/run", {})[0] == 202
    s = None
    for _ in range(960):
        s = req("GET", f"/api/cases/{tok}/status")[1]["status"]
        if s in ("ready", "failed", "done_with_errors"):
            break
        time.sleep(0.25)
    return s


def pre(case):
    # case flags carry evidence[] = [{record_id, excerpt, start, end}]; there is no top-level excerpt or record key
    return [{"title": f.get("title"), "record_ids": [e.get("record_id") for e in f.get("evidence") or []],
             "excerpts": [e.get("excerpt") for e in f.get("evidence") or []]}
            for f in case["flags"] if f["type"] == "pre_existing"]


def http():
    out = {"base": BASE}
    st, body = req("GET", "/api/health")
    out["health"] = [st, body]
    st, body = req("POST", "/api/cases", {"text": "Hx obtained via patient's son: lumbar strain 2019.", "name": "T-120 r2 probe"})
    out["paste_probe_status"] = st
    out["paste_probe_body"] = body
    libs = {}
    for lib in ("case_lib09_spanish_interpreter_espalda", "case_lib02_slip_fall_prior_knee", "case_lib11_priors_and_ledger"):
        st, body = req("POST", "/api/cases", {"library": lib})
        assert st == 201, (lib, st, body)
        tok = body["token"]
        status = poll(tok)
        c = req("GET", f"/api/cases/{tok}")[1]
        libs[lib] = {"status": status, "pre_existing": pre(c), "records": [r.get("id") for r in c["records"]]}
    out["library"] = libs
    st, body = req("POST", "/api/cases", {"sample": True})
    tok = body["token"]
    status = poll(tok)
    c = req("GET", f"/api/cases/{tok}")[1]
    out["sample"] = {"status": status, "pre_existing": pre(c)}
    return out


if __name__ == "__main__":
    result = engine() if MODE == "engine" else http()
    json.dump(result, sys.stdout, indent=1, ensure_ascii=False)
    print()
---LOG
---COMPARE
lib09 record numbers with the source sentence: [1]
lib09 record 1 pre_existing flags on HEAD (unchanged excerpt): []

probe                                                          expect   pre-T120  r2 07dbd2b  HEAD 433ac1c  HEAD ok?
S1 blocker: PHx via son, colon, year                           flag     True      True        True          yes
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:43:49.194Z

**tool call — Bash**
````
{
 "command": "git log --oneline --all | grep -i \"T-120\" ; echo ---; git status --short | head -20; echo ---; (lsof -iTCP:7896 -sTCP:LISTEN -nP; lsof -iTCP:7897 -sTCP:LISTEN -nP; echo \"lsof done\") 2>&1 | head; echo ---; grep -n \"PORT\\|ZLAYT_DB\\|ZLAYT_MODE\\|LLM_BACKEND\\|FIXTURE\" app/config.py | head -30",
 "description": "Check T-120 commits, working tree, free ports, config env vars"
}
````

### User / tool · 2026-11-02T11:43:49.668Z

**tool result**
````
f7829c1 fix(backend): T-120 r3 history-source skip strips only the attribution phrase and scans what is left (no condition guessing)
07dbd2b fix(backend): T-120 r2 history-source skip only when the sentence names no condition (colon, year, 'of' keep the flag); per/via only before a person or channel
4e294d7 test(backend): T-125 record the lib09 f_r1_1 J4 answer live (claude-cli); T-120 renumbered the flag so the old key missed
1cb8707 fix(backend): T-120 a history-source sentence (Hx obtained via ...) is not a prior-condition mention
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
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
---
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  27007 arsis    9u  IPv4 0x96c20b15f43d3912      0t0  TCP 127.0.0.1:7897 (LISTEN)
lsof done
---
ugrep: warning: app/config.py: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:43:55.492Z

**tool call — Bash**
````
{
 "command": "git archive --prefix=zlayt-r3/ f7829c1 | tar -x -C \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\" && ls \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/zlayt-r3\" | head -30; echo ---; grep -rn \"ZLAYT_MODE\\|environ.get(\\\"PORT\\|PORT\\b\" /Users/arsis/zlayt-pm-project/app/backend/*.py /Users/arsis/zlayt-pm-project/app/*.py 2>/dev/null | grep -v \"^.*#\" | head -20; echo ---; grep -rn \"ZLAYT_DB\\|LLM_BACKEND\\|FIXTURE_SET\" /Users/arsis/zlayt-pm-project/app --include=*.py | head -12",
 "description": "Extract HEAD archive to scratchpad and find config env vars"
}
````

### User / tool · 2026-11-02T11:43:56.203Z

**tool result**
````
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
---
/Users/arsis/zlayt-pm-project/app/backend/api.py:80:    return os.environ.get("ZLAYT_MODE") == "local"
/Users/arsis/zlayt-pm-project/app/backend/api.py:108:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
/Users/arsis/zlayt-pm-project/app/backend/api.py:550:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
/Users/arsis/zlayt-pm-project/app/backend/api.py:584:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
/Users/arsis/zlayt-pm-project/app/backend/calibration_route.py:26:REPORT = ROOT / "evals" / "reports" / "calibration.json"
/Users/arsis/zlayt-pm-project/app/backend/calibration_route.py:170:def load(path=REPORT, root=ROOT) -> dict:
/Users/arsis/zlayt-pm-project/app/backend/calibration_route.py:200:def add_routes(app, *, path=REPORT, root=ROOT):
/Users/arsis/zlayt-pm-project/app/backend/dismissal_patterns.py:5:ZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.
/Users/arsis/zlayt-pm-project/app/backend/present.py:341:    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
/Users/arsis/zlayt-pm-project/app/main.py:14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
/Users/arsis/zlayt-pm-project/app/backend/trace.py:7:Visibility is the /audit split (D-020/D-036): full=False (public/demo) returns metadata only; full=True (ZLAYT_MODE=local) adds the model's raw
---
/Users/arsis/zlayt-pm-project/app/llm/provider.py:3:LLM_BACKEND = fixture (default; no key, no network) | claude-cli (dev) | anthropic-api (live).
/Users/arsis/zlayt-pm-project/app/llm/provider.py:25:    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
/Users/arsis/zlayt-pm-project/app/llm/provider.py:27:    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
/Users/arsis/zlayt-pm-project/app/llm/record.py:1:"""Fixture recorder: LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record evals/golden/<case>.txt
/Users/arsis/zlayt-pm-project/app/llm/record.py:36:        raise ValueError("record mode needs a live LLM_BACKEND (claude-cli or anthropic-api)")
/Users/arsis/zlayt-pm-project/app/llm/record.py:102:            print("refused: needs a live LLM_BACKEND and RECORD_FIXTURES=1", file=sys.stderr)
/Users/arsis/zlayt-pm-project/app/llm/backends/fixture.py:13:    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
/Users/arsis/zlayt-pm-project/app/llm/backends/fixture.py:16:    name = os.environ.get("FIXTURE_SET", "").strip()
/Users/arsis/zlayt-pm-project/app/llm/backends/fixture.py:24:        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
/Users/arsis/zlayt-pm-project/app/backend/pipeline.py:421:        self.old = os.environ.get("LLM_BACKEND")
/Users/arsis/zlayt-pm-project/app/backend/pipeline.py:423:            os.environ["LLM_BACKEND"] = self.name
/Users/arsis/zlayt-pm-project/app/backend/pipeline.py:428:            os.environ.pop("LLM_BACKEND", None)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:44:00.299Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/zlayt-r3 && grep -rn \"ZLAYT_DB\" app | head -5; ls /Users/arsis/zlayt-pm-project/.venv/bin/python && ls evals/library | head -20",
 "description": "Confirm DB env var name and venv python in archive"
}
````

### User / tool · 2026-11-02T11:44:00.395Z

**tool result**
````
app/backend/api.py:94:    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
/Users/arsis/zlayt-pm-project/.venv/bin/python
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:44:04.565Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/zlayt-r3 && PYTHONDONTWRITEBYTECODE=1 ZLAYT_MODE=local ZLAYT_DB=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120-r3.sqlite LLM_BACKEND=fixture FIXTURE_SET=curated HOST=127.0.0.1 PORT=7896 /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main",
 "description": "Start the HEAD f7829c1 app on port 7896 in background",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T11:44:04.628Z

**tool result**
````
Command running in background with ID: balw64l08. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/balw64l08.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:44:06.210Z

**tool call — Bash**
````
{
 "command": "lsof -iTCP:7896 -sTCP:LISTEN -nP; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7896/api/health; curl -s http://127.0.0.1:7896/api/health; echo",
 "description": "Find listener PID on 7896 and check health"
}
````

### User / tool · 2026-11-02T11:44:06.393Z

**tool result**
````
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  53182 arsis    9u  IPv4 0x215c34cc79de1ff6      0t0  TCP 127.0.0.1:7896 (LISTEN)
200
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every item","sample_available":true}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:44:35.984Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r3-paralegal-probe.py",
 "content": "\"\"\"T-120 r3 paralegal-reviewer probe (stdlib + the archive's own app code).\n\nTwo modes, both run with the project venv and -I:\n  ARCH=<git archive copy> .venv/bin/python -I <this file> engine\n      Same record dict through flags.lexicon_flags (the flag engine the pipeline calls) and lexicon_scan.scan.\n      The record is lib09 record 1 with its excerpt replaced by each probe sentence (the card's 'record 2' is record 1).\n  ZLAYT_BASE=http://127.0.0.1:7896 .venv/bin/python -I <this file> http\n      Live app: paste route (expect 409 demo_mode_unsupported_input) and the library cases lib09, lib02, lib11 and the sample.\n\nExpectations are the reviewer's, fixed before the run. S1 to S16 are the r1/r2 set (same expectations as the r2 probe).\nN1 to N5 are new shapes written for r3. Output is JSON on stdout; the review cites the redirected file.\n\"\"\"\nimport json\nimport os\nimport sys\nimport time\nimport urllib.error\nimport urllib.request\n\nMODE = sys.argv[1] if len(sys.argv) > 1 else \"engine\"\n\n# (label, probe sentence, reviewer expectation for a pre_existing flag)\nSENTENCES = [\n    (\"S1 r1 blocker: PHx via son, colon, year\", \"PHx obtained via patient's son: lumbar strain 2019.\", \"flag\"),\n    (\"S2 interpreter-only (lib09 r1 lead sentence)\", \"Hx obtained via patient's son, who interpreted.\", \"no flag\"),\n    (\"S3 Hx via interpreter, colon, year\", \"Hx obtained via interpreter: lumbar strain 2019.\", \"flag\"),\n    (\"S4 r2 blocker: who reports neck pain (no colon/digit/of)\", \"Hx obtained via patient's son, who reports neck pain.\", \"flag\"),\n    (\"S5 names condition with lexicon word 'chronic'\", \"Hx obtained via patient's son, who reports chronic neck pain.\", \"flag\"),\n    (\"S6 r2 blocker: semicolon, neck pain and headaches\", \"Hx obtained via patient's son; neck pain and headaches.\", \"flag\"),\n    (\"S7 per son, no condition\", \"Hx per patient's son, who interpreted.\", \"no flag\"),\n    (\"S8 via interpreter, prior lexicon phrase after semicolon\", \"Hx via interpreter, who interpreted; prior neck injury.\", \"flag\"),\n    (\"S9 'Hx of' then source phrase\", \"Hx of lumbar strain obtained via patient's son.\", \"flag\"),\n    (\"S10 source sentence with year, no colon\", \"Hx obtained via patient's son, who interpreted, lumbar strain 2019.\", \"flag\"),\n    (\"S11 r2 blocker: EMS crew relayed lumbar strain\", \"Hx obtained via EMS crew, who relayed lumbar strain.\", \"flag\"),\n    (\"S12 source sentence then a second, non-prior sentence\", \"Hx obtained via patient's son, who interpreted. Lumbar strain was noted.\", \"no flag\"),\n    (\"S13 source sentence then a dated prior second sentence\", \"Hx obtained via patient's son, who interpreted. Prior lumbar strain 2019.\", \"flag\"),\n    (\"S14 plain Hx with colon, no source phrase (control)\", \"Hx: lumbar strain 2019.\", \"flag\"),\n    (\"S15 r2 blocker: names condition after 'and'\", \"Hx obtained via patient's son, who interpreted, and reports lumbar strain.\", \"flag\"),\n    (\"S16 negated condition after source phrase\", \"Hx obtained via patient's son, who interpreted, denies neck pain.\", \"no flag\"),\n    (\"N1 new: who reports chronic low back pain since 2019, daughter\", \"Hx obtained via patient's daughter, who reports chronic low back pain since 2019.\", \"flag\"),\n    (\"N2 new: from husband, semicolon, prior cervical strain\", \"Hx obtained from patient's husband; prior cervical strain.\", \"flag\"),\n    (\"N3 new: attribution only, 'who translated' (no condition)\", \"Hx obtained via EMS crew, who translated.\", \"no flag\"),\n    (\"N4 new: who reports headaches and dizziness (no lexicon word)\", \"Hx obtained via patient's son, who reports headaches and dizziness.\", \"flag\"),\n    (\"N5 new: per interpreter, lists prior shoulder surgery\", \"Hx per interpreter, who interpreted, and lists prior shoulder surgery.\", \"flag\"),\n]\n\n\ndef engine():\n    arch = os.environ[\"ARCH\"]\n    sys.path.insert(0, arch)\n    sys.dont_write_bytecode = True\n    from app.backend import flags as FL, ingest as I, lexicon_scan as LS  # noqa: E402\n    lib = os.path.join(arch, \"evals/library/case_lib09_spanish_interpreter_espalda.txt\")\n    recs = I.ingest(open(lib, encoding=\"utf-8\").read())[\"records\"]\n    base = next(r for r in recs if \"Hx obtained via\" in r[\"excerpt\"])\n    out = {\"arch\": arch,\n           \"lib09_record_numbers_with_source_sentence\": [r[\"n\"] for r in recs if \"Hx obtained via\" in r[\"excerpt\"]],\n           \"lib09_record1_unchanged_pre_existing\": [f[\"excerpt\"] for f in FL.lexicon_flags(base) if f[\"type\"] == \"pre_existing\"],\n           \"probes\": []}\n    for label, exc, expect in SENTENCES:\n        rec = dict(base, excerpt=exc)\n        pre = [f[\"excerpt\"] for f in FL.lexicon_flags(rec) if f[\"type\"] == \"pre_existing\"]\n        raw = sorted({h[\"id\"] for h in LS.scan(exc) if h[\"flag_type\"] == \"pre_existing\"})\n        raised = bool(pre)\n        out[\"probes\"].append({\"label\": label, \"text\": exc, \"expect\": expect, \"raised\": raised,\n                              \"match\": raised == (expect == \"flag\"),\n                              \"pre_existing_flags\": pre, \"lexicon_hit_ids\": raw})\n    out[\"mismatches\"] = [p[\"label\"] for p in out[\"probes\"] if not p[\"match\"]]\n    return out\n\n\nBASE = os.environ.get(\"ZLAYT_BASE\", \"http://127.0.0.1:7896\")\n\n\ndef req(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(BASE + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(r, timeout=180) as x:\n            return x.status, json.loads(x.read() or b\"null\")\n    except urllib.error.HTTPError as e:\n        raw = e.read()\n        try:\n            return e.code, json.loads(raw or b\"null\")\n        except ValueError:\n            return e.code, raw.decode(\"utf-8\", \"replace\")\n\n\ndef poll(tok):\n    assert req(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\n    s = None\n    for _ in range(960):\n        s = req(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"]\n        if s in (\"ready\", \"failed\", \"done_with_errors\"):\n            break\n        time.sleep(0.25)\n    return s\n\n\ndef pre(case):\n    # case flags carry evidence[] = [{record_id, excerpt, start, end}]; no top-level excerpt or record key\n    return [{\"title\": f.get(\"title\"), \"record_ids\": [e.get(\"record_id\") for e in f.get(\"evidence\") or []],\n             \"excerpts\": [e.get(\"excerpt\") for e in f.get(\"evidence\") or []]}\n            for f in case[\"flags\"] if f[\"type\"] == \"pre_existing\"]\n\n\ndef http():\n    out = {\"base\": BASE}\n    st, body = req(\"GET\", \"/api/health\")\n    out[\"health\"] = [st, body]\n    st, body = req(\"POST\", \"/api/cases\", {\"text\": \"Hx obtained via patient's son: lumbar strain 2019.\", \"name\": \"T-120 r3 probe\"})\n    out[\"paste_probe_status\"] = st\n    out[\"paste_probe_body\"] = body\n    libs = {}\n    for lib in (\"case_lib09_spanish_interpreter_espalda\", \"case_lib02_slip_fall_prior_knee\", \"case_lib11_priors_and_ledger\"):\n        st, body = req(\"POST\", \"/api/cases\", {\"library\": lib})\n        assert st == 201, (lib, st, body)\n        tok = body[\"token\"]\n        status = poll(tok)\n        c = req(\"GET\", f\"/api/cases/{tok}\")[1]\n        libs[lib] = {\"status\": status, \"pre_existing\": pre(c), \"records\": [r.get(\"id\") for r in c[\"records\"]]}\n    out[\"library\"] = libs\n    st, body = req(\"POST\", \"/api/cases\", {\"sample\": True})\n    tok = body[\"token\"]\n    status = poll(tok)\n    c = req(\"GET\", f\"/api/cases/{tok}\")[1]\n    out[\"sample\"] = {\"status\": status, \"pre_existing\": pre(c)}\n    return out\n\n\nif __name__ == \"__main__\":\n    result = engine() if MODE == \"engine\" else http()\n    json.dump(result, sys.stdout, indent=1, ensure_ascii=False)\n    print()\n"
}
````

### User / tool · 2026-11-02T11:44:36.098Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r3-paralegal-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:44:39.233Z

**tool call — Bash**
````
{
 "command": "ARCH=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/zlayt-r3 .venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-probe.py engine > artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json; echo \"exit $?\"; .venv/bin/python -I -c \"import json; d=json.load(open('artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json')); print(d['lib09_record_numbers_with_source_sentence'], d['lib09_record1_unchanged_pre_existing']); [print(p['label'][:3], p['expect'], 'raised=%s' % p['raised'], 'match=%s' % p['match'], p['lexicon_hit_ids'], p['pre_existing_flags']) for p in d['probes']]; print('mismatches', d['mismatches'])\"",
 "description": "Run the engine probe on the HEAD f7829c1 archive and summarize"
}
````

### User / tool · 2026-11-02T11:44:39.693Z

**tool result**
````
exit 0
[1] []
S1  flag raised=True match=True ['hx_abbrev'] ["PHx obtained via patient's son: lumbar strain 2019."]
S2  no flag raised=False match=True [] []
S3  flag raised=True match=True ['hx_abbrev'] ['Hx obtained via interpreter: lumbar strain 2019.']
S4  flag raised=True match=True ['hx_abbrev'] ["Hx obtained via patient's son, who reports neck pain."]
S5  flag raised=True match=True ['chronic', 'hx_abbrev'] ["Hx obtained via patient's son, who reports chronic neck pain."]
S6  flag raised=True match=True ['hx_abbrev'] ["Hx obtained via patient's son;"]
S7  no flag raised=False match=True [] []
S8  flag raised=True match=True ['hx_abbrev', 'prior_injury_or_condition'] ['Hx via interpreter, who interpreted;', 'prior neck injury.']
S9  flag raised=True match=True ['hx_abbrev'] ["Hx of lumbar strain obtained via patient's son."]
S10 flag raised=True match=True ['hx_abbrev'] ["Hx obtained via patient's son, who interpreted, lumbar strain 2019."]
S11 flag raised=True match=True ['hx_abbrev'] ['Hx obtained via EMS crew, who relayed lumbar strain.']
S12 no flag raised=False match=True [] []
S13 flag raised=True match=True ['prior_injury_or_condition'] ['Prior lumbar strain 2019.']
S14 flag raised=True match=True ['hx_abbrev'] ['Hx: lumbar strain 2019.']
S15 flag raised=True match=True ['hx_abbrev'] ["Hx obtained via patient's son, who interpreted, and reports lumbar strain."]
S16 no flag raised=True match=False ['hx_abbrev'] ["Hx obtained via patient's son, who interpreted, denies neck pain."]
N1  flag raised=True match=True ['chronic', 'condition_since_year', 'hx_abbrev'] ["Hx obtained via patient's daughter, who reports chronic low back pain since 2019."]
N2  flag raised=True match=True ['hx_abbrev', 'prior_injury_or_condition'] ["Hx obtained from patient's husband;", 'prior cervical strain.']
N3  no flag raised=False match=True [] []
N4  flag raised=True match=True ['hx_abbrev'] ["Hx obtained via patient's son, who reports headaches and dizziness."]
N5  flag raised=True match=True ['hx_abbrev', 'prior_surgery_terms'] ['Hx per interpreter, who interpreted, and lists prior shoulder surgery.']
mismatches ['S16 negated condition after source phrase']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:44:55.648Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\nfor f in ['artifacts/review-evidence/T-120-r2-engine-base-0c47356.json','artifacts/review-evidence/T-120-r2-engine-07dbd2b.json','artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json']:\n    d=json.load(open(f))\n    for p in d['probes']:\n        if p['label'][:2] in ('S6','S4','S8'):\n            print(f.split('/')[-1][:28], p['label'][:3], p['pre_existing_flags'], p['lexicon_hit_ids'])\n\"; echo ---; ZLAYT_BASE=http://127.0.0.1:7896 .venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-probe.py http > artifacts/review-evidence/T-120-r3-http-HEAD-f7829c1.json; echo \"exit $?\"; .venv/bin/python -I -c \"\nimport json\nd=json.load(open('artifacts/review-evidence/T-120-r3-http-HEAD-f7829c1.json'))\nprint('health', d['health'][0], d['health'][1].get('demo_mode'), d['health'].__len__())\nprint('paste', d['paste_probe_status'], d['paste_probe_body'])\nfor k,v in d['library'].items(): print(k, v['status'], v['records'], [ (x['title'], x['record_ids'], x['excerpts']) for x in v['pre_existing']])\nprint('sample', d['sample']['status'], [ (x['title'], x['record_ids'], x['excerpts']) for x in d['sample']['pre_existing']])\n\"",
 "description": "Compare S6/S4/S8 across builds and run the live HTTP probe"
}
````

### User / tool · 2026-11-02T11:44:57.195Z

**tool result**
````
T-120-r2-engine-base-0c47356 S4  ["Hx obtained via patient's son, who reports neck pain."] ['hx_abbrev']
T-120-r2-engine-base-0c47356 S6  ["Hx obtained via patient's son;"] ['hx_abbrev']
T-120-r2-engine-base-0c47356 S8  ['Hx via interpreter, who interpreted;', 'prior neck injury.'] ['hx_abbrev', 'prior_injury_or_condition']
T-120-r2-engine-07dbd2b.json S4  [] []
T-120-r2-engine-07dbd2b.json S6  [] []
T-120-r2-engine-07dbd2b.json S8  ['prior neck injury.'] ['prior_injury_or_condition']
T-120-r2-engine-HEAD-433ac1c S4  [] []
T-120-r2-engine-HEAD-433ac1c S6  [] []
T-120-r2-engine-HEAD-433ac1c S8  ['prior neck injury.'] ['prior_injury_or_condition']
---
exit 0
health 200 True 2
paste 409 {'error': {'code': 'demo_mode_unsupported_input', 'message': 'This demo only runs the recorded sample cases.', 'detail': {}}}
case_lib09_spanish_interpreter_espalda ready ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7'] []
case_lib02_slip_fall_prior_knee ready ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7'] [('Mention of prior surgery or repair', ['r2'], ['X-ray right knee: no acute fracture; prior arthroscopic changes noted.']), ('Mention of prior surgery or repair', ['r3'], ['Patient reports a right knee arthroscopy in 2021 with good recovery before the fall.']), ('Degenerative wording', ['r4'], ['Mild tricompartmental degenerative change.']), ('Mention of prior surgery or repair', ['r4'], ['Findings may reflect both acute injury and prior surgical change.']), ('Mention of a prior or pre-existing condition', ['r5'], ['Aggravation of the underlying knee condition is possible.'])]
case_lib11_priors_and_ledger ready ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9'] [('Mention of a prior or pre-existing condition', ['r1'], ['Problem list: hypertension, type 2 diabetes, chronic low back pain.']), ('Mention of a prior or pre-existing condition', ['r1'], ['History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.']), ('Mention of a prior or pre-existing condition', ['r6'], ['Prior accidents?']), ('Mention of a prior or pre-existing condition', ['r6'], ['Prior injuries?'])]
sample ready [('Mention of a prior or pre-existing condition', ['r3'], ['Patient reports low back pain in 2023, resolved.']), ('Degenerative wording', ['r8'], ['Findings may represent degenerative change'])]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:45:32.023Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\na=json.load(open('artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json'))\nb=json.load(open('artifacts/review-evidence/T-120-r3-http-HEAD-f7829c1.json'))\nfor k in a['library']:\n    print(k, 'pre_existing equal to r2 HEAD 433ac1c:', a['library'][k]['pre_existing']==b['library'][k]['pre_existing'], 'status', b['library'][k]['status'])\nprint('sample equal:', a['sample']['pre_existing']==b['sample']['pre_existing'], b['sample']['status'])\nprint('paste r2 vs r3:', a['paste_probe_status'], b['paste_probe_status'])\n\"; echo ---; python3 tools/board.py show T-120 | grep -n \"AC\\|text\\|evidence\" | head -8",
 "description": "Diff live pre-existing flags against the r2 run and recheck card AC 1"
}
````

### User / tool · 2026-11-02T11:45:32.194Z

**tool result**
````
case_lib09_spanish_interpreter_espalda pre_existing equal to r2 HEAD 433ac1c: True status ready
case_lib02_slip_fall_prior_knee pre_existing equal to r2 HEAD 433ac1c: True status ready
case_lib11_priors_and_ledger pre_existing equal to r2 HEAD 433ac1c: True status ready
sample equal: True ready
paste r2 vs r3: 409 409
---
22:  - {"n": 1, "text": "lib09 raises no 'Mention of a prior or pre-existing condition' flag on the interpreter-history sentence of record 2; a real prior-condition mention in another record still raises the flag (unit test for both)", "done": true, "evidence": "tests/unit/test_t120_history_source_sentence.py::test_lib09_record_1_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes (the sentence is lib09 record 1; AC text says record 2 in error); r3 rows: 32 staff probes, paralegal S4/S6/S11/S15, parent-regression forms"}
23:  - {"n": 2, "text": "tests/unit covers the rule so it cannot regress; evals report unchanged otherwise", "done": true, "evidence": "95 tests in test_t120_history_source_sentence.py; 12 guard mutants all killed; unit suite 3123 passed; evals fixture report evals/reports/20261102T114138Z.md flag precision/recall 1.000 all types"}
31:- 2026-11-02T11:11:30Z backend: AC 1 checked: tests/unit/test_t120_history_source_sentence.py::test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes; real prior mentions still hit (REAL rows)
32:- 2026-11-02T11:11:31Z backend: AC 2 checked: 17 tests in test_t120_history_source_sentence.py; fixture evals.run flag precision/recall all 1.000, no change
36:    - [major] The `Hx per ...` branch drops the flag on real prior-condition mentions — fix: Narrow the `per`/`via` branch so it skips only when the source phrase ends the clause or is followed by an interpreter/family-member noun and no condition text (or only skip the `Hx` token and let the remaining clause scan run). Do not skip when a colon, 'of', a year or a condition word follows the source.
41:- 2026-11-02T11:27:48Z backend: r2: per/via only before a person/channel noun; skip only when the rest of the sentence has no colon, digit or 'of' (PHx obtained via patient's son: lumbar strain 2019 and Hx per patient: ... hit). Mutants widening via or removing the rest check are killed. Citation corrected: the interpreter sentence is lib09 record 1 (r1); test renamed test_lib09_record_1_*; AC text says record 2 and cannot be edited by hand. Flag ids are positional (f_r1_1 changed meaning); the lib09 J4 fixture was re-recorded live (T-125).
46:    - [minor] Card AC 1 still cites lib09 record 2 and a test name that no longer exists (carried from r1; r2 renamed the test to record_1) — fix: Correct AC 1 text and its evidence string to record 1 and test_lib09_record_1_... through the board (orchestrator to choose the route).
47:- 2026-11-02T11:33:21Z orchestrator: Design direction for round 3 (orchestrator): stop guessing whether a sentence 'names a condition'. Instead, strip only the history-source attribution phrase itself (e.g. 'Hx obtained via patient's son', ', who interpreted', 'per patient') and run the normal prior-condition scan on whatever text remains, so 'who reports neck pain' and 'lumbar strain 2019' still flag, and a sentence that is only attribution yields nothing. Test with all forms from both paralegal reviews and the staff review.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:45:43.263Z

**tool call — Bash**
````
{
 "command": "ps -o pid=,ppid=,command= -p 53182; PP=$(ps -o ppid= -p 53182 | tr -d ' '); echo \"parent $PP\"; ps -o pid=,ppid=,command= -p $PP",
 "description": "Identify listener and launcher PIDs for port 7896"
}
````

### User / tool · 2026-11-02T11:45:43.367Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:45:46.087Z

**tool call — Bash**
````
{
 "command": "kill 53182 53181; sleep 2; lsof -iTCP:7896 -sTCP:LISTEN -nP; echo \"lsof exit $?\"; curl -s -o /dev/null -w \"%{http_code}\\n\" --max-time 3 http://127.0.0.1:7896/api/health; ps -o pid=,command= -p 53182 -p 53181; echo \"ps done\"",
 "description": "Stop the 7896 server by PID and confirm the port is closed"
}
````

### User / tool · 2026-11-02T11:45:48.284Z

**tool result**
````
lsof exit 1
000
ps done
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:45:54.177Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/zlayt-r3 && grep -n \"def _is_source_sentence\\|split(\\|hx_abbrev\\|def scan\\|re.split\\|\\\\\\;\\|;\" app/backend/lexicon_scan.py | head -30; echo ---; grep -n \"def test_lib09_record_1\\|def test_lib09_record_2\" tests/unit/test_t120_history_source_sentence.py; echo ---; grep -n \"S16\\|denies\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json | head -3; cd /Users/arsis/zlayt-pm-project && .venv/bin/python -I -c \"\nimport json\nd=json.load(open('artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json'))\nprint([ (p['label'][:3], p['pre_existing_flags']) for p in d['probes'] if p['label'][:3] in ('S16','S8 ','S2 ')])\n\"",
 "description": "Locate splitter and source-sentence code lines and r2 S16 value"
}
````

### User / tool · 2026-11-02T11:45:54.318Z

**tool result**
````
2:field answers, year_filter, suppress_if_followed_by. Pure; no model. Hits with strength high/medium raise flags; low is context only."""
8:TOKEN = re.compile(r"[\w'/-]+|[;,]")
12:# T-120 r3: "Hx obtained via patient's son, who interpreted" names who GAVE the history; it states no prior condition. We do not guess whether a
15:# attribution (no flag); anything left (", who reports neck pain", ": lumbar strain", a newline and more text) keeps the hit. An unknown source noun
40:    return " " + " ".join(t.lower() for t in tokens if t not in (",", ";")) + " "
57:        if low[i] in terms or any(" ".join(low[i:i + len(m.split())]) == m for m in multi):
68:    word_terms = [t for t in terms if t not in (",", ";")]
71:    if ";" in before:
72:        before = before[len(before) - before[::-1].index(";"):]
100:        if t in (",", ";") or t.lower() in word_terms:
115:def _is_source_sentence(text: str, end: int) -> bool:
139:    m = re.search(r"[,;.\n]", text[end:])
143:def scan(text: str, accident_year=None) -> list:
---
44:def test_lib09_record_1_raises_no_prior_condition_flag_and_other_prior_mentions_still_do():
---
161:   "label": "S16 negated condition after source phrase",
162:   "text": "Hx obtained via patient's son, who interpreted, denies neck pain.",
[('S2 ', []), ('S8 ', ['prior neck injury.']), ('S16', [])]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:45:57.294Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/zlayt-r3/app/backend/lexicon_scan.py",
 "offset": 110,
 "limit": 50
}
````

### User / tool · 2026-11-02T11:45:57.301Z

**tool result**
````
110	        sup = re.compile(e["suppress_if_followed_by"], re.I) if e.get("suppress_if_followed_by") else None
111	        out.append((e, re.compile(e["pattern"], re.I | re.M), sup))
112	    return tuple(out)
113	
114	
115	def _is_source_sentence(text: str, end: int) -> bool:
116	    """T-120 r3: the history word ends at text[end]. Strip the attribution phrase that follows it and test what is left of the sentence: only
117	    punctuation or nothing means the sentence was only attribution ("Hx obtained via patient's son, who interpreted."). Any other text keeps the
118	    hit, whatever it says ("who reports neck pain", ": lumbar strain 2019", "(lumbar strain)", a second line)."""
119	    m = _HISTORY_SOURCE.match(text, end) or _HISTORY_VIA.match(text, end)
120	    if not m:
121	        return False
122	    s = _SENT_END.search(text, m.end())
123	    rest = text[m.end():s.start() if s else len(text)]
124	    return not re.search(r"\w", rest)
125	
126	
127	def _hit_year(m):
128	    for g in ("year", "year2"):
129	        try:
130	            if m.group(g):
131	                return int(m.group(g))
132	        except IndexError:
133	            pass
134	    y = YEAR.search(m.group(0))
135	    return int(y.group(0)) if y else None
136	
137	
138	def _clause_after(text, end):
139	    m = re.search(r"[,;.\n]", text[end:])
140	    return text[end:end + m.start()] if m else text[end:]
141	
142	
143	def scan(text: str, accident_year=None) -> list:
144	    """Firing hits as [{id, flag_type, category, strength, start, end, text, unit_start, unit_end}], file order. Unknown accident_year keeps
145	    year-filtered hits (the item is reviewed anyway)."""
146	    neg = lexicon.load()["negation"]
147	    units = sentences.stripped_spans(text)
148	    out = []
149	    for e, rx, sup in _entries():
150	        if e["strength"] not in RAISES:
151	            continue
152	        for m in rx.finditer(text):
153	            if e.get("negatable") and negated(text, m.start(), m.end(), neg):
154	                continue
155	            if e.get("year_filter") and accident_year:
156	                y = _hit_year(m)
157	                if y and y >= accident_year:
158	                    continue
159	            if sup and sup.search(_clause_after(text, m.end())):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:46:03.662Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/zlayt-r3 && grep -n \"_SENT_END\\s*=\\|_HISTORY_SOURCE\\s*=\\|_HISTORY_VIA\\s*=\" app/backend/lexicon_scan.py; grep -rn \"def stripped_spans\" app/backend/ ; grep -n \"';'\\|\\\";\\\"\\|\\[;\" app/backend/sentences.py | head",
 "description": "Locate sentence-end and source-phrase regex definitions"
}
````

### User / tool · 2026-11-02T11:46:03.764Z

**tool result**
````
25:_HISTORY_SOURCE = re.compile(r"\s+(?:(?:was|is|were)\s+)?(?:obtained|taken|provided|given|gathered|collected|supplied|reported|relayed)\s+"
27:_HISTORY_VIA = re.compile(rf"\s+(?:per|via)\s+{_SOURCES}{_WHO_INTERPRETED}", re.I)
28:_SENT_END = re.compile(r"[.!?](?:\s|$)")   # a newline does NOT end the sentence here: "Hx per interpreter\nLumbar strain 2019" keeps the flag
app/backend/sentences.py:69:def stripped_spans(text: str) -> list:
5:letter, a digit or end of text; ';'; a line break. Deterministic code only.
36:        if ch == ";":
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:46:08.831Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/zlayt-r3/app/backend/sentences.py",
 "offset": 30,
 "limit": 45
}
````

### User / tool · 2026-11-02T11:46:08.840Z

**tool result**
````
30	def unit_spans(text: str) -> list:
31	    """[(start, end)] tiling `text` exactly (no gaps, no overlaps)."""
32	    spans, n, start, i = [], len(text), 0, 0
33	    while i < n:
34	        ch = text[i]
35	        end = None
36	        if ch == ";":
37	            end = i + 1
38	        elif ch == "\n":
39	            end = i + 1
40	        elif ch in ".?!":
41	            j = i + 1
42	            while j < n and text[j] in _CLOSERS:
43	                j += 1
44	            if j >= n:
45	                end = j
46	            elif text[j].isspace():
47	                k = j
48	                while k < n and text[k].isspace():
49	                    k += 1
50	                nxt_ok = k >= n or text[k].isupper() or text[k].isdigit() or "\n" in text[j:k]
51	                if nxt_ok and not (ch == "." and _abbrev_before(text, i)):
52	                    end = j
53	        if end is not None:
54	            while end < n and text[end].isspace():
55	                end += 1
56	            spans.append((start, end))
57	            start, i = end, end
58	        else:
59	            i += 1
60	    if start < n:
61	        spans.append((start, n))
62	    return spans
63	
64	
65	def units(text: str) -> list:
66	    return [text[a:b] for a, b in unit_spans(text)]
67	
68	
69	def stripped_spans(text: str) -> list:
70	    """Unit spans without surrounding whitespace (for API offsets and excerpt alignment)."""
71	    out = []
72	    for a, b in unit_spans(text):
73	        seg = text[a:b]
74	        lead = len(seg) - len(seg.lstrip())
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:47:07.455Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r3-paralegal-draft.json",
 "content": "{\"card\": \"T-120\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"HEAD f7829c1 (T-120 r3 commit, on top of 07dbd2b and 1cb8707) as a git archive copy in the session scratchpad, zlayt-r3/; app on http://127.0.0.1:7896 (fixture backend, ZLAYT_MODE=local, listener PID 53182, launcher PID 53181, both stopped); engine probes through app.backend.flags.lexicon_flags and lexicon_scan.scan on lib09 record 1 with the excerpt replaced (the card's 'record 2' is record 1); live library cases lib09, lib02, lib11 and the sample evals/golden/sample.txt\",\n \"exercised\": [\n  \"read personas/paralegal.md in full, reviews/T-120-paralegal-r2.md, python3 tools/board.py show T-120 (status in_review; AC 1 still reads 'of record 2')\",\n  \"git rev-parse HEAD gave f7829c1; git archive --prefix=zlayt-r3/ f7829c1 | tar -x -C <scratchpad> (the session scratchpad)\",\n  \"started .venv/bin/python -m app.main from the archive with PYTHONDONTWRITEBYTECODE=1, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, LLM_BACKEND=fixture, FIXTURE_SET=curated, HOST=127.0.0.1, PORT=7896; lsof gave listener PID 53182; /api/health returned 200 with demo_mode true\",\n  \"engine probe: ARCH=<archive> .venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-probe.py engine > artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json; 21 sentences: S1 to S16 (the r1 and r2 set, same expectations) and N1 to N5 (new)\",\n  \"live probe: ZLAYT_BASE=http://127.0.0.1:7896 .venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-probe.py http > artifacts/review-evidence/T-120-r3-http-HEAD-f7829c1.json; paste POST returned 409 demo_mode_unsupported_input; lib09, lib02, lib11 and sample all reached ready\",\n  \"diffed the live pre_existing lists against the r2 run artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json: equal for lib09, lib02, lib11 and the sample\",\n  \"read the archive code: app/backend/sentences.py:30-62 (unit_spans, ';' ends a unit at line 36-37), sentences.py:69 (stripped_spans), app/backend/lexicon_scan.py:28 (_SENT_END ends only at [.!?]) and lexicon_scan.py:115-124 (_is_source_sentence)\",\n  \"compared against the r2 engine runs artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json (S16 none) and artifacts/review-evidence/T-120-r2-engine-base-0c47356.json (S6 excerpt cut at the semicolon before T-120)\",\n  \"stopped the server: kill 53182 53181; lsof -iTCP:7896 -sTCP:LISTEN returned nothing (exit 1); curl returned 000; ps showed neither PID\",\n  \"not run: pytest (the unit suite is the backend's and staff reviewer's lane) and the live LLM merge path (flags.py:249), which fixture mode and the 409 paste route cannot reach\"],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 3, \"prior_mentions_flagged\": 3, \"interpreter_sentence_not_flagged\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"Semicolon history line: the prior condition after ';' is in no flag (S6 'Hx obtained via patient's son; neck pain and headaches.' flags only the attribution fragment)\",\n   \"evidence\": \"artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json probe S6: raised true, pre_existing_flags [\\\"Hx obtained via patient's son;\\\"], lexicon_hit_ids [hx_abbrev]. The words 'neck pain and headaches' are in no flag excerpt. Cause: app/backend/sentences.py:36-37 ends a unit at ';', and stripped_spans (sentences.py:69) takes each flag excerpt from that unit. app/backend/lexicon_scan.py:28 ends the source-sentence test only at [.!?], so the hit survives on the rest '; neck pain and headaches' (lexicon_scan.py:124). The same sentence without the semicolon (S4, 'who reports neck pain.') gets the whole sentence as its excerpt. Pre-T-120 build: the same truncated excerpt (artifacts/review-evidence/T-120-r2-engine-base-0c47356.json, S6). HEAD 433ac1c: no flag (artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json, S6).\",\n   \"why_it_matters\": \"Checklist item 9 and card AC 1: a prior-condition mention in a history line must raise a flag whose excerpt carries the mention. Here the flag sits on the source phrase, and 'neck pain and headaches' (history content) has no flag at all. This is the r2 blocker's defect (the condition is dropped from the flag) for the semicolon shape. A paralegal who dismisses 'Hx obtained via patient's son;' as only the source phrase never sees the condition. The lexicon has no bare 'neck pain' entry, so nothing else catches it. My probe's expect column checks only whether a flag was raised, so it marks S6 as a match; this finding is the excerpt check. Not downgraded to major: the condition is absent from every flag, which is the r2 blocker.\",\n   \"fix\": \"Keep the Hx source sentence whole through its semicolon, so that its flag excerpt contains the clause after ';' (as S4 does without the semicolon), or give that clause its own flag. The owner picks the rule; do not add condition words to the lexicon just for this case.\",\n   \"acceptance_test\": \"Engine probe S6 ('Hx obtained via patient's son; neck pain and headaches.'): a pre_existing flag is raised AND one of its evidence excerpts contains 'neck pain and headaches' (checked on the excerpt text, not only on raised). S2 and S7 still raise nothing. Re-run artifacts/review-evidence/T-120-r3-paralegal-probe.py engine on the fixed archive, with the excerpt check added.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Denial raises a prior flag: S16 'Hx obtained via patient's son, who interpreted, denies neck pain.' flags again (433ac1c did not)\",\n   \"evidence\": \"artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json S16: raised true, pre_existing_flags [\\\"Hx obtained via patient's son, who interpreted, denies neck pain.\\\"], lexicon_hit_ids [hx_abbrev]. artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json S16: pre_existing_flags []. Cause: lexicon_scan.py:124 keeps the hit for any word after the attribution, including 'denies neck pain'.\",\n   \"why_it_matters\": \"A denial is not a prior-condition mention. The flag adds a review item that the paralegal must dismiss, and the flag text itself says a prior condition is mentioned. The direction is safe (no fact is lost), so this is an over-flag, not a blocker. It is a regression from the r2 build, which handled this sentence correctly.\",\n   \"fix\": \"The owner decides: either suppress the hit when a negation word follows the source phrase, or record in the card that a denial keeps the flag by design (question_for_chris).\",\n   \"acceptance_test\": \"Engine probe S16 raises no pre_existing flag, or the card records the decision to keep it. S2, S7, S12 and N3 stay quiet, and the other rows keep their results.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Attribution fragments that end in ';' still raise a flag (S8 'Hx via interpreter, who interpreted;' and N2 'Hx obtained from patient's husband;')\",\n   \"evidence\": \"artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json S8: pre_existing_flags [\\\"Hx via interpreter, who interpreted;\\\", \\\"prior neck injury.\\\"]. N2: pre_existing_flags [\\\"Hx obtained from patient's husband;\\\", \\\"prior cervical strain.\\\"]. The same attribution with a period (S2, \\\"Hx obtained via patient's son, who interpreted.\\\") raises nothing. Cause: _SENT_END (lexicon_scan.py:28) ends only at [.!?], so the rest of the sentence after ';' keeps the hit, and the excerpt is cut at ';' (sentences.py:36-37).\",\n   \"why_it_matters\": \"The r3 design is that a sentence which is only attribution yields nothing. With a ';' the attribution is flagged on its own fragment, and the condition after the ';' gets a second flag. The paralegal sees two flags for one line, one of them empty of any condition. This is noise, not a lost fact.\",\n   \"fix\": \"Make the decision on the whole source unit, through the ';' (see the blocker fix). The attribution-only check then runs on the whole unit, so a unit with nothing but attribution yields nothing and a unit with a condition gets one flag whose excerpt contains the condition.\",\n   \"acceptance_test\": \"Engine probe: 'Hx obtained via patient's son, who interpreted;' raises no flag. 'Hx obtained from patient's husband; prior cervical strain.' raises one pre_existing flag whose excerpt contains 'prior cervical strain'. S2 is unchanged.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Card AC 1 still says the interpreter sentence is in lib09 record 2 (carried from r1 and r2; the evidence string now admits the error, the AC text does not)\",\n   \"evidence\": \"python3 tools/board.py show T-120, AC 1 text: \\\"...on the interpreter-history sentence of record 2; ...\\\"; AC 1 evidence: \\\"...the sentence is lib09 record 1; AC text says record 2 in error\\\". artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json: lib09_record_numbers_with_source_sentence [1].\",\n   \"why_it_matters\": \"Checklist item 3: a reviewer or paralegal who opens record 2 will not find the sentence. The evidence line says so, but the AC text stays wrong.\",\n   \"fix\": \"Correct AC 1 to 'record 1' through the board (orchestrator route; the AC text cannot be hand-edited).\",\n   \"acceptance_test\": \"python3 tools/board.py show T-120 shows 'record 1' in AC 1 and no 'record 2'.\"}\n ],\n \"whats_right\": [\n  \"The r2 blocker shapes now flag with the whole sentence as the excerpt: S4 'Hx obtained via patient's son, who reports neck pain.', S11 'Hx obtained via EMS crew, who relayed lumbar strain.' and S15 'Hx obtained via patient's son, who interpreted, and reports lumbar strain.'\",\n  \"The interpreter-only sentence raises no flag: engine S2 'Hx obtained via patient's son, who interpreted.' gives []; live lib09 pre_existing is empty; S7 and S12 are quiet too.\",\n  \"Live priors are unchanged from the r2 run on 433ac1c (lib02 5 flags, lib11 4, sample records 3 'Patient reports low back pain in 2023, resolved.' and 8 'Findings may represent degenerative change'), and the new sentences N1, N3, N4 and N5 behave as expected.\"],\n \"questions_for_chris\": [\n  \"Should a negated condition ('denies neck pain') raise a prior-condition flag? I count it as an over-flag (minor). Your answer decides whether S16 is a finding.\"]}\n"
}
````

### User / tool · 2026-11-02T11:47:07.571Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r3-paralegal-draft.json (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:47:15.713Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r3-paralegal-jsoncheck.py",
 "content": "\"\"\"Pre-check for the T-120 r3 paralegal review (run with .venv/bin/python -I).\n\nUsage: .venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-jsoncheck.py <file.json | review.md>\nA .md file must contain exactly one fenced json block. Checks the D.2 shape and the verdict rule (blocker -> fail,\nmajor -> changes, else pass). Prints the findings by severity and exits 1 on any problem.\n\"\"\"\nimport json\nimport re\nimport sys\n\nREQUIRED = [\"card\", \"persona\", \"model\", \"scope\", \"exercised\", \"verdict\", \"scores\", \"findings\", \"whats_right\", \"questions_for_chris\"]\nFINDING_KEYS = [\"severity\", \"title\", \"evidence\", \"why_it_matters\", \"fix\", \"acceptance_test\"]\nSEVERITIES = {\"blocker\", \"major\", \"minor\", \"nit\"}\n\n\ndef load(path):\n    text = open(path, encoding=\"utf-8\").read()\n    if path.endswith(\".md\"):\n        blocks = re.findall(r\"```json\\n(.*?)\\n```\", text, re.S)\n        if len(blocks) != 1:\n            raise SystemExit(f\"expected exactly one ```json block, found {len(blocks)}\")\n        text = blocks[0]\n    return json.loads(text)\n\n\ndef main(path):\n    problems = []\n    d = load(path)\n    for k in REQUIRED:\n        if k not in d:\n            problems.append(f\"missing key {k}\")\n    if d.get(\"card\") != \"T-120\":\n        problems.append(f\"card is {d.get('card')!r}\")\n    if d.get(\"persona\") != \"paralegal-reviewer\":\n        problems.append(f\"persona is {d.get('persona')!r}\")\n    if d.get(\"model\") != \"claude-haiku-5-5\":\n        problems.append(f\"model is {d.get('model')!r}\")\n    scores = d.get(\"scores\", {})\n    if \"verify_quickly\" not in scores:\n        problems.append(\"scores.verify_quickly missing (ship bar D-015)\")\n    for k, v in scores.items():\n        if not (isinstance(v, int) and 1 <= v <= 5):\n            problems.append(f\"score {k}={v!r} is not an int 1-5\")\n    sev = []\n    for i, f in enumerate(d.get(\"findings\", [])):\n        for k in FINDING_KEYS:\n            if not f.get(k):\n                problems.append(f\"finding {i} missing or empty {k}\")\n        if f.get(\"severity\") not in SEVERITIES:\n            problems.append(f\"finding {i} severity {f.get('severity')!r}\")\n        sev.append(f.get(\"severity\"))\n    if len(d.get(\"whats_right\", [])) > 3:\n        problems.append(\"whats_right has more than 3 lines\")\n    if \"blocker\" in sev:\n        want = \"fail\"\n    elif \"major\" in sev:\n        want = \"changes\"\n    else:\n        want = \"pass\"\n    if d.get(\"verdict\") != want:\n        problems.append(f\"verdict {d.get('verdict')!r} breaks the rule (should be {want!r})\")\n    print(\"severities:\", {s: sev.count(s) for s in sorted(SEVERITIES)})\n    print(\"verdict:\", d.get(\"verdict\"), \"| rule says:\", want)\n    print(\"exercised items:\", len(d.get(\"exercised\", [])), \"| findings:\", len(sev), \"| whats_right:\", len(d.get(\"whats_right\", [])))\n    if problems:\n        for p in problems:\n            print(\"PROBLEM:\", p)\n        return 1\n    print(\"ok\")\n    return 0\n\n\nif __name__ == \"__main__\":\n    sys.exit(main(sys.argv[1]))\n"
}
````

### User / tool · 2026-11-02T11:47:15.896Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r3-paralegal-jsoncheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:47:17.824Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-jsoncheck.py artifacts/review-evidence/T-120-r3-paralegal-draft.json; echo \"exit $?\"",
 "description": "Validate the draft review JSON with the pre-check script"
}
````

### User / tool · 2026-11-02T11:47:17.927Z

**tool result**
````
severities: {'blocker': 1, 'major': 0, 'minor': 3, 'nit': 0}
verdict: fail | rule says: fail
exercised items: 10 | findings: 4 | whats_right: 3
ok
exit 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:47:24.897Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r3-paralegal-draft.json",
 "old_string": "\"Live priors are unchanged from the r2 run on 433ac1c (lib02 5 flags, lib11 4, sample records 3 'Patient reports low back pain in 2023, resolved.' and 8 'Findings may represent degenerative change'), and the new sentences N1, N3, N4 and N5 behave as expected.\"],",
 "new_string": "\"Live priors are unchanged from the r2 run on 433ac1c (lib02 5 flags, lib11 4, sample records 3 'Patient reports low back pain in 2023, resolved.' and 8 'Findings may represent degenerative change'), and all five new sentences N1 to N5 match their expectations (N2 with the duplicate flag in finding 3).\"],"
}
````

### User / tool · 2026-11-02T11:47:24.994Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r3-paralegal-draft.json has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:47:27.556Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r3-paralegal-draft.json",
 "old_string": "\"scope\": \"HEAD f7829c1 (T-120 r3 commit, on top of 07dbd2b and 1cb8707) as a git archive copy",
 "new_string": "\"scope\": \"HEAD f7829c1 (the T-120 r3 commit; earlier T-120 commits 1cb8707 and 07dbd2b) as a git archive copy"
}
````

### User / tool · 2026-11-02T11:47:27.656Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-r3-paralegal-draft.json has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:47:37.527Z

**tool call — Bash**
````
{
 "command": "ls reviews/T-120-paralegal-r3.md 2>&1; .venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-jsoncheck.py artifacts/review-evidence/T-120-r3-paralegal-draft.json; echo \"exit $?\"; grep -n \"record 2\" artifacts/review-evidence/T-120-r3-paralegal-draft.json | cut -c1-120",
 "description": "Confirm the review file is new and re-run the JSON pre-check"
}
````

### User / tool · 2026-11-02T11:47:37.649Z

**tool result**
````
ls: reviews/T-120-paralegal-r3.md: No such file or directory
severities: {'blocker': 1, 'major': 0, 'minor': 3, 'nit': 0}
verdict: fail | rule says: fail
exercised items: 10 | findings: 4 | whats_right: 3
ok
exit 0
2: "scope": "HEAD f7829c1 (the T-120 r3 commit; earlier T-120 commits 1cb8707 and 07dbd2b) as a git archive copy in the 
4:  "read personas/paralegal.md in full, reviews/T-120-paralegal-r2.md, python3 tools/board.py show T-120 (status in_rev
36:   "title": "Card AC 1 still says the interpreter sentence is in lib09 record 2 (carried from r1 and r2; the evidence
37:   "evidence": "python3 tools/board.py show T-120, AC 1 text: \"...on the interpreter-history sentence of record 2; .
38:   "why_it_matters": "Checklist item 3: a reviewer or paralegal who opens record 2 will not find the sentence. The ev
40:   "acceptance_test": "python3 tools/board.py show T-120 shows 'record 1' in AC 1 and no 'record 2'."}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:48:01.834Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-120-paralegal-r3.md",
 "content": "# T-120 paralegal re-check (round 3)\n\n**Verdict: fail.** One blocker. The four r2 blocker shapes now raise the prior flag with the whole sentence as the excerpt, and the interpreter-only sentence stays quiet. But the semicolon form of the same content (\"Hx obtained via patient's son; neck pain and headaches.\") flags only the source phrase. The condition after the semicolon is in no flag, so the r2 defect (the condition is dropped) is still there for this shape.\n\nScope: HEAD f7829c1 (the T-120 r3 commit) as a `git archive` copy in the session scratchpad (zlayt-r3/), fixture backend, ZLAYT_MODE=local, port 7896. Listener PID 53182 and launcher PID 53181 were stopped; lsof on 7896 returned nothing and curl returned 000.\n\nEvidence: artifacts/review-evidence/T-120-r3-paralegal-probe.py (probe), artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json (21 sentences, engine), artifacts/review-evidence/T-120-r3-http-HEAD-f7829c1.json (live), artifacts/review-evidence/T-120-r3-paralegal-jsoncheck.py (this file's shape check).\n\n## Re-test of the r2 blocker sentences and the interpreter-only sentence\n\nEngine probe on lib09 record 1 with the excerpt replaced. The card's \"record 2\" is record 1. Column \"r2 433ac1c\" is the r2 run (artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json).\n\n| # | Probe sentence (abbreviated) | r2 433ac1c | r3 f7829c1 | Expected | OK |\n|---|---|---|---|---|---|\n| S1 | PHx obtained via patient's son: lumbar strain 2019. | flag | flag | flag | yes |\n| S2 | Hx obtained via patient's son, who interpreted. (interpreter-only) | none | none | none | yes |\n| S3 | Hx obtained via interpreter: lumbar strain 2019. | flag | flag | flag | yes |\n| S4 | Hx obtained via patient's son, who reports neck pain. (r2 blocker) | none | flag, whole sentence | flag | yes |\n| S5 | Hx obtained via patient's son, who reports chronic neck pain. | flag | flag | flag | yes |\n| S6 | Hx obtained via patient's son; neck pain and headaches. (r2 blocker) | none | flag, excerpt \"Hx obtained via patient's son;\" only | flag, condition in the flag | NO (blocker) |\n| S7 | Hx per patient's son, who interpreted. | none | none | none | yes |\n| S8 | Hx via interpreter, who interpreted; prior neck injury. | flag | flag (2 flags, one on \"Hx via interpreter, who interpreted;\") | flag | yes (duplicate fragment) |\n| S9 | Hx of lumbar strain obtained via patient's son. | flag | flag | flag | yes |\n| S10 | Hx obtained via patient's son, who interpreted, lumbar strain 2019. | flag | flag | flag | yes |\n| S11 | Hx obtained via EMS crew, who relayed lumbar strain. (r2 blocker) | none | flag, whole sentence | flag | yes |\n| S12 | Hx obtained via patient's son, who interpreted. Lumbar strain was noted. | none | none | none | yes |\n| S13 | ...who interpreted. Prior lumbar strain 2019. | flag | flag | flag | yes |\n| S14 | Hx: lumbar strain 2019. (control) | flag | flag | flag | yes |\n| S15 | Hx obtained via patient's son, who interpreted, and reports lumbar strain. (r2 blocker) | none | flag, whole sentence | flag | yes |\n| S16 | Hx obtained via patient's son, who interpreted, denies neck pain. | none | flag | none | NO (minor) |\n| N1 | Hx obtained via patient's daughter, who reports chronic low back pain since 2019. | not tested | flag, whole sentence | flag | yes |\n| N2 | Hx obtained from patient's husband; prior cervical strain. | not tested | flag (2 flags: \"Hx obtained from patient's husband;\" and \"prior cervical strain.\") | flag | yes (duplicate fragment) |\n| N3 | Hx obtained via EMS crew, who translated. | not tested | none | none | yes |\n| N4 | Hx obtained via patient's son, who reports headaches and dizziness. | not tested | flag, whole sentence | flag | yes |\n| N5 | Hx per interpreter, who interpreted, and lists prior shoulder surgery. | not tested | flag | flag | yes |\n\nEngine check, S2 and the live lib09 case: S2 gives no flag. In the live lib09 case (ready) the pre_existing list is empty.\n\nLive (HTTP): the paste route returns 409 demo_mode_unsupported_input, as in r2. lib09, lib02, lib11 and the sample all reach ready. Their pre_existing lists are identical to the r2 run on 433ac1c (diffed): lib02 has 5 flags, lib11 has 4, the sample keeps \"Patient reports low back pain in 2023, resolved.\" (r3) and \"Findings may represent degenerative change\" (r8).\n\n## Findings\n\n1. **blocker: the semicolon form of a condition-naming history line drops the condition from every flag (S6).** The flag's evidence is `[\"Hx obtained via patient's son;\"]`, so \"neck pain and headaches\" appears in no excerpt and has no flag of its own. Cause: `app/backend/sentences.py:36-37` ends a unit at \";\", and `stripped_spans` (sentences.py:69) takes the excerpt from that unit. `app/backend/lexicon_scan.py:28` ends the source-sentence test only at `[.!?]`, so the hit survives on the rest \"; neck pain and headaches\" (lexicon_scan.py:124). The same content without the semicolon (S4) shows the whole sentence. The pre-T-120 build gave the same cut excerpt (artifacts/review-evidence/T-120-r2-engine-base-0c47356.json, S6). My probe checks only whether a flag was raised, so it marked S6 as a match; the excerpt check is the finding. Fix: keep the source sentence whole through its semicolon, or give that clause its own flag. Acceptance: S6 raises a flag and an excerpt contains \"neck pain and headaches\"; S2 and S7 stay quiet.\n\n2. **minor: a denial raises the flag (S16).** \"denies neck pain\" now flags. The r2 build gave none (T-120-r2-engine-HEAD-433ac1c.json, S16). This is an over-flag in the safe direction. Question for Chris below.\n\n3. **minor: attribution fragments that end in \";\" still raise a flag (S8, N2).** \"Hx via interpreter, who interpreted;\" and \"Hx obtained from patient's husband;\" each get their own flag, while the period form (S2) gets none. The fix belongs with finding 1: decide on the whole source unit.\n\n4. **minor: card AC 1 still says \"record 2\"** (carried from r1 and r2). `python3 tools/board.py show T-120` prints \"...the interpreter-history sentence of record 2\". The evidence line now says record 1, but the AC text is still wrong.\n\n## What I exercised\n\n- Read personas/paralegal.md in full, reviews/T-120-paralegal-r2.md, and `python3 tools/board.py show T-120`.\n- `git rev-parse HEAD` gave f7829c1. `git archive --prefix=zlayt-r3/ f7829c1 | tar -x` into the session scratchpad.\n- Started `.venv/bin/python -m app.main` from the archive with ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, LLM_BACKEND=fixture, FIXTURE_SET=curated, HOST=127.0.0.1, PORT=7896. `/api/health` returned 200 with demo_mode true.\n- Engine probe (`.venv/bin/python -I`, ARCH=archive) for S1 to S16 and N1 to N5. HTTP probe (ZLAYT_BASE=http://127.0.0.1:7896) for the paste route and the four library cases. Diffed the HTTP output against artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json.\n- Read the archive code at sentences.py:30-62 and 69, and lexicon_scan.py:28 and 115-124.\n- Stopped the server: `kill 53182 53181`; `lsof -iTCP:7896 -sTCP:LISTEN -nP` returned nothing (exit 1); curl returned 000; ps showed neither PID.\n- Not run: pytest (backend and staff reviewer lane). The live LLM merge path (flags.py:249) is not reachable: fixture mode, and the paste route is refused.\n\n## What is right\n\n- The r2 blocker shapes S4, S11 and S15 now raise the flag with the whole sentence as the excerpt.\n- The interpreter-only sentence (S2) and its variants S7 and S12 raise nothing, and the live lib09 pre_existing list is empty.\n- The live priors (lib02, lib11, sample records 3 and 8) are unchanged from the r2 run, and the new sentences N1, N3, N4 and N5 match their expectations.\n\n## Questions for Chris\n\n- Should a negated condition (\"denies neck pain\") raise a prior-condition flag? I count it as an over-flag (minor). Your answer decides whether S16 stays a finding.\n\n```json\n{\"card\": \"T-120\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"HEAD f7829c1 (the T-120 r3 commit; earlier T-120 commits 1cb8707 and 07dbd2b) as a git archive copy in the session scratchpad, zlayt-r3/; app on http://127.0.0.1:7896 (fixture backend, ZLAYT_MODE=local, listener PID 53182, launcher PID 53181, both stopped); engine probes through app.backend.flags.lexicon_flags and lexicon_scan.scan on lib09 record 1 with the excerpt replaced (the card's 'record 2' is record 1); live library cases lib09, lib02, lib11 and the sample evals/golden/sample.txt\",\n \"exercised\": [\n  \"read personas/paralegal.md in full, reviews/T-120-paralegal-r2.md, python3 tools/board.py show T-120 (status in_review; AC 1 still reads 'of record 2')\",\n  \"git rev-parse HEAD gave f7829c1; git archive --prefix=zlayt-r3/ f7829c1 | tar -x -C <scratchpad> (the session scratchpad)\",\n  \"started .venv/bin/python -m app.main from the archive with PYTHONDONTWRITEBYTECODE=1, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, LLM_BACKEND=fixture, FIXTURE_SET=curated, HOST=127.0.0.1, PORT=7896; lsof gave listener PID 53182; /api/health returned 200 with demo_mode true\",\n  \"engine probe: ARCH=<archive> .venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-probe.py engine > artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json; 21 sentences: S1 to S16 (the r1 and r2 set, same expectations) and N1 to N5 (new)\",\n  \"live probe: ZLAYT_BASE=http://127.0.0.1:7896 .venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-probe.py http > artifacts/review-evidence/T-120-r3-http-HEAD-f7829c1.json; paste POST returned 409 demo_mode_unsupported_input; lib09, lib02, lib11 and sample all reached ready\",\n  \"diffed the live pre_existing lists against the r2 run artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json: equal for lib09, lib02, lib11 and the sample\",\n  \"read the archive code: app/backend/sentences.py:30-62 (unit_spans, ';' ends a unit at line 36-37), sentences.py:69 (stripped_spans), app/backend/lexicon_scan.py:28 (_SENT_END ends only at [.!?]) and lexicon_scan.py:115-124 (_is_source_sentence)\",\n  \"compared against the r2 engine runs artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json (S16 none) and artifacts/review-evidence/T-120-r2-engine-base-0c47356.json (S6 excerpt cut at the semicolon before T-120)\",\n  \"stopped the server: kill 53182 53181; lsof -iTCP:7896 -sTCP:LISTEN returned nothing (exit 1); curl returned 000; ps showed neither PID\",\n  \"not run: pytest (the unit suite is the backend's and staff reviewer's lane) and the live LLM merge path (flags.py:249), which fixture mode and the 409 paste route cannot reach\"],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 3, \"prior_mentions_flagged\": 3, \"interpreter_sentence_not_flagged\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"Semicolon history line: the prior condition after ';' is in no flag (S6 'Hx obtained via patient's son; neck pain and headaches.' flags only the attribution fragment)\",\n   \"evidence\": \"artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json probe S6: raised true, pre_existing_flags [\\\"Hx obtained via patient's son;\\\"], lexicon_hit_ids [hx_abbrev]. The words 'neck pain and headaches' are in no flag excerpt. Cause: app/backend/sentences.py:36-37 ends a unit at ';', and stripped_spans (sentences.py:69) takes each flag excerpt from that unit. app/backend/lexicon_scan.py:28 ends the source-sentence test only at [.!?], so the hit survives on the rest '; neck pain and headaches' (lexicon_scan.py:124). The same sentence without the semicolon (S4, 'who reports neck pain.') gets the whole sentence as its excerpt. Pre-T-120 build: the same truncated excerpt (artifacts/review-evidence/T-120-r2-engine-base-0c47356.json, S6). HEAD 433ac1c: no flag (artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json, S6).\",\n   \"why_it_matters\": \"Checklist item 9 and card AC 1: a prior-condition mention in a history line must raise a flag whose excerpt carries the mention. Here the flag sits on the source phrase, and 'neck pain and headaches' (history content) has no flag at all. This is the r2 blocker's defect (the condition is dropped from the flag) for the semicolon shape. A paralegal who dismisses 'Hx obtained via patient's son;' as only the source phrase never sees the condition. The lexicon has no bare 'neck pain' entry, so nothing else catches it. My probe's expect column checks only whether a flag was raised, so it marks S6 as a match; this finding is the excerpt check. Not downgraded to major: the condition is absent from every flag, which is the r2 blocker.\",\n   \"fix\": \"Keep the Hx source sentence whole through its semicolon, so that its flag excerpt contains the clause after ';' (as S4 does without the semicolon), or give that clause its own flag. The owner picks the rule; do not add condition words to the lexicon just for this case.\",\n   \"acceptance_test\": \"Engine probe S6 ('Hx obtained via patient's son; neck pain and headaches.'): a pre_existing flag is raised AND one of its evidence excerpts contains 'neck pain and headaches' (checked on the excerpt text, not only on raised). S2 and S7 still raise nothing. Re-run artifacts/review-evidence/T-120-r3-paralegal-probe.py engine on the fixed archive, with the excerpt check added.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Denial raises a prior flag: S16 'Hx obtained via patient's son, who interpreted, denies neck pain.' flags again (433ac1c did not)\",\n   \"evidence\": \"artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json S16: raised true, pre_existing_flags [\\\"Hx obtained via patient's son, who interpreted, denies neck pain.\\\"], lexicon_hit_ids [hx_abbrev]. artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json S16: pre_existing_flags []. Cause: lexicon_scan.py:124 keeps the hit for any word after the attribution, including 'denies neck pain'.\",\n   \"why_it_matters\": \"A denial is not a prior-condition mention. The flag adds a review item that the paralegal must dismiss, and the flag text itself says a prior condition is mentioned. The direction is safe (no fact is lost), so this is an over-flag, not a blocker. It is a regression from the r2 build, which handled this sentence correctly.\",\n   \"fix\": \"The owner decides: either suppress the hit when a negation word follows the source phrase, or record in the card that a denial keeps the flag by design (question_for_chris).\",\n   \"acceptance_test\": \"Engine probe S16 raises no pre_existing flag, or the card records the decision to keep it. S2, S7, S12 and N3 stay quiet, and the other rows keep their results.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Attribution fragments that end in ';' still raise a flag (S8 'Hx via interpreter, who interpreted;' and N2 'Hx obtained from patient's husband;')\",\n   \"evidence\": \"artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json S8: pre_existing_flags [\\\"Hx via interpreter, who interpreted;\\\", \\\"prior neck injury.\\\"]. N2: pre_existing_flags [\\\"Hx obtained from patient's husband;\\\", \\\"prior cervical strain.\\\"]. The same attribution with a period (S2, \\\"Hx obtained via patient's son, who interpreted.\\\") raises nothing. Cause: _SENT_END (lexicon_scan.py:28) ends only at [.!?], so the rest of the sentence after ';' keeps the hit, and the excerpt is cut at ';' (sentences.py:36-37).\",\n   \"why_it_matters\": \"The r3 design is that a sentence which is only attribution yields nothing. With a ';' the attribution is flagged on its own fragment, and the condition after the ';' gets a second flag. The paralegal sees two flags for one line, one of them empty of any condition. This is noise, not a lost fact.\",\n   \"fix\": \"Make the decision on the whole source unit, through the ';' (see the blocker fix). The attribution-only check then runs on the whole unit, so a unit with nothing but attribution yields nothing and a unit with a condition gets one flag whose excerpt contains the condition.\",\n   \"acceptance_test\": \"Engine probe: 'Hx obtained via patient's son, who interpreted;' raises no flag. 'Hx obtained from patient's husband; prior cervical strain.' raises one pre_existing flag whose excerpt contains 'prior cervical strain'. S2 is unchanged.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Card AC 1 still says the interpreter sentence is in lib09 record 2 (carried from r1 and r2; the evidence string now admits the error, the AC text does not)\",\n   \"evidence\": \"python3 tools/board.py show T-120, AC 1 text: \\\"...on the interpreter-history sentence of record 2; ...\\\"; AC 1 evidence: \\\"...the sentence is lib09 record 1; AC text says record 2 in error\\\". artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json: lib09_record_numbers_with_source_sentence [1].\",\n   \"why_it_matters\": \"Checklist item 3: a reviewer or paralegal who opens record 2 will not find the sentence. The evidence line says so, but the AC text stays wrong.\",\n   \"fix\": \"Correct AC 1 to 'record 1' through the board (orchestrator route; the AC text cannot be hand-edited).\",\n   \"acceptance_test\": \"python3 tools/board.py show T-120 shows 'record 1' in AC 1 and no 'record 2'.\"}\n ],\n \"whats_right\": [\n  \"The r2 blocker shapes now flag with the whole sentence as the excerpt: S4 'Hx obtained via patient's son, who reports neck pain.', S11 'Hx obtained via EMS crew, who relayed lumbar strain.' and S15 'Hx obtained via patient's son, who interpreted, and reports lumbar strain.'\",\n  \"The interpreter-only sentence raises no flag: engine S2 'Hx obtained via patient's son, who interpreted.' gives []; live lib09 pre_existing is empty; S7 and S12 are quiet too.\",\n  \"Live priors are unchanged from the r2 run on 433ac1c (lib02 5 flags, lib11 4, sample records 3 'Patient reports low back pain in 2023, resolved.' and 8 'Findings may represent degenerative change'), and all five new sentences N1 to N5 match their expectations (N2 with the duplicate flag in finding 3).\"],\n \"questions_for_chris\": [\n  \"Should a negated condition ('denies neck pain') raise a prior-condition flag? I count it as an over-flag (minor). Your answer decides whether S16 is a finding.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T11:48:01.988Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-120-paralegal-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:48:06.841Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-jsoncheck.py reviews/T-120-paralegal-r3.md; echo \"jsoncheck exit $?\"; python3 tools/board.py validate reviews/T-120-paralegal-r3.md; echo \"validate exit $?\"; .venv/bin/python -I - <<'EOF'\nimport json, re\nmd = open(\"reviews/T-120-paralegal-r3.md\", encoding=\"utf-8\").read()\nblock = re.findall(r\"```json\\n(.*?)\\n```\", md, re.S)[0]\ndraft = json.load(open(\"artifacts/review-evidence/T-120-r3-paralegal-draft.json\", encoding=\"utf-8\"))\nprint(\"review json equals draft:\", json.loads(block) == draft)\nprint(\"fence count:\", md.count(\"```\"))\nEOF",
 "description": "Validate the final review file and confirm its JSON matches the draft"
}
````

### User / tool · 2026-11-02T11:48:07.018Z

**tool result**
````
severities: {'blocker': 1, 'major': 0, 'minor': 3, 'nit': 0}
verdict: fail | rule says: fail
exercised items: 10 | findings: 4 | whats_right: 3
ok
jsoncheck exit 0
ok (1 file(s))
validate exit 0
review json equals draft: True
fence count: 2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:48:15.260Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t120-r3-patterns.md",
 "content": "---\nname: t120-r3-patterns\ndescription: T-120 r3 re-check (2026-11-02, HEAD f7829c1): r2 whole-sentence blockers now flag; semicolon splits the flag excerpt and drops the condition after ';' (blocker); denial and ';'-fragment over-flags\nmetadata:\n  type: project\n---\n\nT-120 r3 (f7829c1): the attribution-strip rule works for S4, S11, S15 (flag, whole sentence as excerpt) and the interpreter-only sentence stays quiet. Verdict fail on one blocker: \"Hx obtained via patient's son; neck pain and headaches.\" flags only \"Hx obtained via patient's son;\" and the condition appears in no flag. Minor: S16 \"denies neck pain\" now flags (r2 HEAD did not); \"Hx via interpreter, who interpreted;\" and \"Hx obtained from patient's husband;\" flag as fragments; AC 1 still says record 2.\n\n**Why:** two different unit boundaries are in play. The flag excerpt comes from `sentences.unit_spans`, which ends a unit at \";\" (sentences.py:36-37). The source-sentence test uses `_SENT_END`, which ends only at [.!?] (lexicon_scan.py:28). So the semicolon clause counts as part of the sentence for the decision but not for the excerpt. That one mismatch produces the S6 hole and the fragment flags.\n\n**How to apply:** when a skip or split rule changes, check the excerpt, not only \"raised\". My probe's expect column passed S6 because a flag was raised; the blocker only showed up when I read the excerpt list. Add an excerpt-contains check for every condition word in the probe. Also probe a semicolon form of every shape (S4, S11, S15 with \";\").\n\n**Method notes (this round):** `git archive --prefix=zlayt-r3/ f7829c1 | tar -x -C <scratchpad>` worked. The server was started from the archive with `.venv/bin/python -m app.main` (listener PID 53182, launcher bash PID 53181 with ppid 2007); both were killed by PID and lsof/curl confirmed the port closed. The paste route still returns 409 demo_mode_unsupported_input with ZLAYT_MODE=local. The later \"background task failed, exit 144\" notice was only the killed launcher, not a user message.\n\nRelated: [[t120-r2-patterns]], [[t120-123-patterns]], [[feedback_spec_review_patterns]] (check the claim against its own example shape).\n"
}
````

### User / tool · 2026-11-02T11:48:15.360Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t120-r3-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:48:16.825Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T11:48:16.833Z

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
13	- [T-114 rates and gap patterns](t114-rates-gap-patterns.md) — r2 (e1ce8dc): gap notice is page-memory only, not on the gap card; rate row keeps Needs review chip; lib09 still 42 to 40
14	- [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — r3 fail; r4 fail (warning gated by text regex); r5 (f8f358e) changes: same-day and header-list gaps in baseline wording
15	- [T-118 lib11 truth patterns](t118-lib11-truth-patterns.md) — validators pass on the wrong truth; record lists unguarded; intake form as phone_note stand-in; stale library-latest.md
16	- [T-060 UI polish patterns](t060-ui-polish-patterns.md) — pass 2 open items; reuse q0-q13 scripts; recount severities before the single Write
17	- [T-120/121/123 patterns](t120-123-patterns.md) — source-sentence skip hides colon-joined real prior (blocker); demo paste gate forces in-process probes; preamble phantom record
18	- [T-120 r2 patterns](t120-r2-patterns.md) — r2 colon fix holds; no-colon/digit/of condition lines still lose the prior flag (blocker); paste 409 in local mode
19	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:48:19.076Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-120 r2 patterns](t120-r2-patterns.md) — r2 colon fix holds; no-colon/digit/of condition lines still lose the prior flag (blocker); paste 409 in local mode\n",
 "new_string": "- [T-120 r2 patterns](t120-r2-patterns.md) — r2 colon fix holds; no-colon/digit/of condition lines still lose the prior flag (blocker); paste 409 in local mode\n- [T-120 r3 patterns](t120-r3-patterns.md) — r2 blockers flag now; \";\" cuts the flag excerpt so the condition after it is in no flag (blocker); probe must check excerpts, not only raised\n"
}
````

### User / tool · 2026-11-02T11:48:19.205Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:48:20.710Z

Wrote /Users/arsis/zlayt-pm-project/reviews/T-120-paralegal-r3.md (verdict fail: 1 blocker, the semicolon form "Hx obtained via patient's son; neck pain and headaches." puts the condition in no flag; server on 7896 stopped, listener PID 53182 and launcher PID 53181, port closed).
