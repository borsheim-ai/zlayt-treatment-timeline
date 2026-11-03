# Subagent: Paralegal: T-149 round 2 (Paralegal: T-149 round 2)

Source: `agent-a2ba80ff8eb5e1e47.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T15:36:50.942Z

As a senior Texas PI paralegal managing many cases, review round 2 of board card T-149 (commit 802d5fd) in /Users/arsis/zlayt-pm-project. Read reviews/T-149-paralegal.md and `python3 tools/board.py show T-149`.

Run the app from a `git archive HEAD` copy in your scratchpad on a spare port: fixture backend, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad. Create 5 or more cases: paste some, and name and rename them.

Check your round-1 majors:
- cases get real names, never "Untitled case";
- export is never shown as green while items are unreviewed;
- a single "Do this first" line names the item and links to it.

Then work two cases from the overview to export. Can you tell at a glance which case needs you and why?

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-149-paralegal-r2.md with a ```json block of real values: card, persona paralegal-reviewer, model claude-sonnet-5-5, verdict, findings, exercised. Stop your server by PID. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:00.208Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:00.209Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-149-paralegal.md"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:00.210Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-149; git log --oneline | head -5"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:00.214Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:00.215Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md"
}
````

### User / tool · 2026-11-02T15:37:00.237Z

**tool result**
````
1	# T-149 paralegal review (paralegal-reviewer, Maria Delgado persona): multi-case overview and detail
2	
3	Verdict: **changes** (0 blockers, 3 majors, 3 minors). Pinned commit 25f585c (HEAD at review start; the card lists 1394661, which is an ancestor). I ran `git archive 25f585c` into a fresh scratchpad directory (`r3-25f585c`) and served it on 127.0.0.1:7941 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratchpad DB. I seeded 6 cases through the API (library cases 01, 06, 02, 03, 09 plus the Rivera sample; 06 and 03 with entries accepted, 09 left unanalyzed), and my T-136 runs added five more pasted cases, so I also saw 11. The server (PID 21600) was stopped: `lsof -iTCP:7941 -sTCP:LISTEN` exit 1, curl 000. Port 7860 was not touched. Scripts and outputs: `artifacts/review-evidence/T-149-paralegal/`.
4	
5	## The two questions I was asked
6	
7	**1. With 5+ cases, can I see which need me, why, and what is ready to send? Partly. Which one is which, and what is ready, fail.**
8	- Each row shows a progress bar per kind, chips ("4 need review", "1 could not be verified", "Export blocked (1)") and the server's own blocker sentence. "Needs attention first" puts the blocked cases on top and both filters work (`o1.out.txt`, `o1-overview-1440.png`). The rows are readable and the counts match `GET /api/cases` (`setup.out.txt`).
9	- But "Ready to export" is green on a case with 1 of 7 entries accepted, 13 items not reviewed and 4 needing review (F-2), so I cannot tell what is ready to send. And the cases I pasted are all called "Untitled case, Nov 2" (F-1), so with 5 clients I cannot tell which row is which.
10	
11	**2. Does the overview block tell me what to do first? No.** It tells me the status. The action is in a different block, and the three places that could say "do this first" disagree (F-3).
12	
13	## Findings
14	
15	**F-1 (major). Pasted cases all read "Untitled case, Nov 2"; there is no way to name one, so five clients are five identical rows.** The home screen has only the paste box and "Upload .txt" (`o6.out.txt`, "inputs on home: input-text, file-input"; no name field and no rename). With five pasted cases, the order by "Needs attention first" reads: `Untitled case, Nov 2 / Created Nov 2, 2026, 8:30 AM`, then 8:29, 8:28, 8:27, 8:26 (`o6.out.txt`; `o6-eleven-cases.png`). The rows differ only by the creation minute. A paralegal with Rivera, Smith and Ochoa open cannot pick the right one, and an overview of cases she cannot tell apart does not tell her which need her. Fix: a case name field next to Analyze (client or matter), a rename on the row and in the detail header, and when no name is given default the title to something she can recognise from the records (provider of record 1 and the date range, never a guessed client name). Acceptance test: paste two different texts without a name, open the overview, assert the two row titles differ and each contains text taken from its own records; rename a case and assert the new name shows in the row and the detail header after a reload.
16	
17	**F-2 (major). "Ready to export" is green on cases that are far from ready to send; the "Needs attention" filter equals "All cases"; so "what is ready to send?" has no answer.** `GET /api/cases` marks `export_ready: true` when nothing blocks the gate, and the UI turns that into the same green chip a finished case would get. Rows as seen: "Truck rear-end, chiropractic plan: Entries 1 of 7, Flags 0 of 4, Amounts 0 of 3, 4 need review, Ready to export, 13 items are not reviewed" and "Letter of protection: Entries 5 of 7, 8 need review, 1 could not be verified, Ready to export, 14 items are not reviewed" (`o1.out.txt`). After I accepted ONE charge on the Rivera sample, that case went green with 21 items not reviewed (`o4.out.txt`: "sample after one charge accepted: export_ready True []"; the row then reads "Ready to export" with "21 items are not reviewed"). The filter chips read "All cases (6)", "Needs attention (6)", "Ready to export (2)" (`o1.out.txt`): all six cases need attention, including the two marked ready. The two counts on one row ("4 need review" and "13 items are not reviewed") are not explained, either. To a paralegal "ready to send" means everything is decided, or the rest was dismissed on purpose. A letter with one of seven entries in it is exactly the demand that gets sent half-finished. Fix: keep "Can export" (gate passes) apart from "Ready to send" (nothing left to decide). For a case with undecided items show an amber "Can export, 13 not reviewed" and keep the green chip for nothing pending; make the "Ready to export" filter use the stricter test and say so. Acceptance test: a case with undecided items has no element with `cases-chip-ready` and is not listed under the ready filter; a case with 0 pending and 0 edits to check shows the green chip and is listed.
18	
19	**F-3 (major). The case overview block does not say what to do first; the block, "Open decisions" and "What you need to do" give different answers, and the action names no item.**
20	- Rivera sample (`o3.out.txt`, `o2-detail-sample-1440.png`): the overview block says "Export blocked (1): Nothing is accepted or edited yet, so the letter would be empty." The "Open decisions" card says "Start review, 3 items need review" and its button moves focus to flag `f_r7_1` (the accident-date source), not to the first entry. The "What you need to do" bar says "Decide the 2 detected charges: accept the ones that are billed charges, dismiss the rest." Three different first steps in one screen. Accepting a charge does clear the blocker (I checked: `export_ready` turned true), but that is not what a paralegal does first with a nine-entry case.
21	- Slip and fall (lib02, `o3.out.txt`, `o2-detail-lib02-1440.png`): "What you need to do: This item cannot be used. Dismiss it, or write the entry by hand from the record." No item is named ("this item"), while the overview block above it shows 7 entries and 8 flags to decide. The item only appears after "Show this step" (`o4-lib01-show-step.png`, which also shows a raw `record ids ["r3"]` line).
22	- On a 900 px screen the case overview, "Open decisions" and "Case checks" blocks are stacked above the timeline, and the first screen holds two entry rows (`o2-detail-sample-1440.png`).
23	Fix: one line, "Do this first: ...", inside the overview block, built from the server's next action and naming the item (record number and provider), with one button that goes to it; show "Start review" and the case-checks bar only as the same action, never as a second one. Acceptance test: on the Rivera sample and lib02 the overview block contains exactly one "Do this first" line; its text names a record or provider; clicking its button focuses the item it names; the line, "Start review" and the case-checks bar never name different targets.
24	
25	**F-4 (minor). A case that was never analyzed shows "9 need review" and "Export blocked: Nothing is accepted or edited yet" and no hint to run the analysis.** Spanish-language records, back pain: status chip "Not analyzed yet", Entries "None", "9 need review", "Export blocked (1)" (`o1.out.txt`, `o1-overview-1440.png`). The honest next step, Analyze, shows only after opening the case ("Read by code only. No model has been called yet." `o2.out.txt`, lib09). Fix: for an ingested case show "Not analyzed. Open it and press Analyze" as the row's reason and drop the review and blocker chips.
26	
27	**F-5 (minor). The row says how many but never why.** "4 need review" does not say that one is a date conflict, one a gap, one a prior condition. Maria's rule 16 is "say why in one sentence". The server has the kinds (`kinds: gap 1, conflict 2, pre existing 2, causation 5` is in the case trace). Fix: a one-line "why" under the chips, for example "1 date conflict, 1 gap, 2 prior conditions".
28	
29	**F-6 (minor). The card's AC evidence "test_multicase.py 17 pass" did not reproduce.** In the archive, run with plain pytest (own private server, `env -u ZLAYT_DB`): `16 passed, 1 skipped, 1 failed`; the failure is `test_keyboard_only_open_move_between_rows_and_return_with_focus_on_the_case`, "ArrowDown moves to the next row's link" (`pytest-multicase.out.txt`; same failure in a second run). In the live app on my server ArrowDown, j and Tab all moved row to row and Enter opened the case, 3 of 3 times with a 600 ms wait after load (`o5.out.txt`), so I believe the key handler is bound after a delay or after a poll render, and the test presses before it. A paralegal who presses a key at once after the list paints loses the key. Fix: bind the handler before the rows paint, or have the test wait on a ready marker, and say which in the card.
30	
31	## What I ran
32	
33	1. `git rev-parse --short HEAD` = 25f585c; `git archive 25f585c | tar -x -C <scratchpad>/r3-25f585c`; server under `.venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py`; curl 200; stopped by PID 21600 (lsof exit 1, curl 000).
34	2. `setup_cases.py`: 6 cases seeded and GET /api/cases read (`setup.out.txt`).
35	3. `o1_overview.py`: overview text, default order, filters, all four sorts (`o1.out.txt`).
36	4. `o2_detail.py` and `o3_next.py`: opened five cases from the overview; read the overview block, next action, case summary and the trace's next_action per step (`o2.out.txt`, `o3.out.txt`).
37	5. `o4_actions.py`: "Show this step", one charge accepted via the API (gate), one entry accepted in the detail, back to the overview (counts, "Last activity", focus lands on the case link), reload (returns to the overview), 390 px overview and detail with no horizontal overflow (`o4.out.txt`).
38	6. `o5_keys.py`: ArrowDown, j, Tab, Enter on the overview, 3 runs (`o5.out.txt`). `o6_many.py`: 11 cases, name inputs, sort by attention (`o6.out.txt`).
39	7. `tests/e2e/test_multicase.py` from the archive with plain pytest, twice (`pytest-multicase.out.txt`).
40	8. Screenshots read: `o1-overview-1440.png`, `o2-detail-sample-1440.png`, `o2-detail-lib06-1440.png`, `o4-lib01-show-step.png`, `o4-detail-390.png`.
41	
42	Things outside my lens: whether the overview should show Stowers/limitation deadlines per case is a product call (see the question below); visual design beyond what slowed verification.
43	
44	```json
45	{"card": "T-149", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
46	 "scope": "git archive 25f585c (HEAD at review start; card commit 1394661 is an ancestor) served on http://127.0.0.1:7941 (PID 21600, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; 6 seeded cases (library 01, 06, 02, 03, 09 + Rivera sample) plus 5 pasted cases; live dev app 7860 not touched",
47	 "exercised": [
48	  "git archive 25f585c into a fresh scratchpad dir; server on 7941 under .venv/bin/python -I with the T-060 pass-4 launcher; curl 200; stopped by PID 21600 (lsof exit 1, curl 000)",
49	  "seeded 6 cases through the API and read GET /api/cases (setup_cases.py, setup.out.txt)",
50	  "overview in the browser: row text, default order, three filters, four sorts (o1_overview.py)",
51	  "opened five cases from the overview and read the case overview block, next action and case checks; read the trace next_action per step (o2_detail.py, o3_next.py)",
52	  "Show this step on lib01; one charge accepted via API to read the gate; one entry accepted in the detail then All cases (counts, last activity, focus); reload; 390 px overview and detail (o4_actions.py)",
53	  "keyboard on the overview: ArrowDown, j, Tab, Enter, 3 runs (o5_keys.py)",
54	  "11-case overview, name inputs on the home screen, attention sort (o6_many.py)",
55	  "tests/e2e/test_multicase.py from the archive with plain pytest, twice: 16 passed, 1 skipped, 1 failed (keyboard test)",
56	  "read the card, the handoff, overview.js header and sort/filter code, api.md case-list section; screenshots o1-overview-1440, o2-detail-sample-1440, o2-detail-lib06-1440, o4-lib01-show-step, o4-detail-390"
57	 ],
58	 "verdict": "changes",
59	 "scores": {"verify_quickly": 3, "overview_triage": 3, "ready_to_send_signal": 2, "detail_first_action": 2, "identify_case": 2},
60	 "findings": [
61	  {"severity": "major", "title": "Pasted cases all read 'Untitled case, Nov 2' and cannot be named, so five clients are five identical rows",
62	   "evidence": "artifacts/review-evidence/T-149-paralegal/o6.out.txt: inputs on home = input-text and file-input only; attention order lists five rows 'Untitled case, Nov 2 / Created Nov 2, 2026, 8:30 AM' ... 8:26 AM; o6-eleven-cases.png",
63	   "why_it_matters": "She manages 5+ cases. An overview of rows she cannot tell apart does not show which cases need her, and she may open or export the wrong client's file.",
64	   "fix": "Name field beside Analyze, rename on the row and in the detail header, and a recognisable default title taken from the records (provider of record 1 and date range), never a guessed client name.",
65	   "acceptance_test": "e2e: paste two different texts with no name; the two overview row titles differ and each contains text from its own records; rename a case and the new name shows in the row and the detail header after reload."},
66	  {"severity": "major", "title": "'Ready to export' is green on cases far from ready to send; the Needs attention filter equals All cases",
67	   "evidence": "o1.out.txt: 'Truck rear-end, chiropractic plan | Entries 1 of 7 ... 4 need review | Ready to export | 13 items are not reviewed'; 'Letter of protection ... 5 of 7 ... 8 need review ... Ready to export | 14 items are not reviewed'; filters 'All cases (6)', 'Needs attention (6)', 'Ready to export (2)'; o4.out.txt: one charge accepted -> 'export_ready True []' and the row reads Ready to export with 21 items not reviewed",
68	   "why_it_matters": "A green ready chip on a letter that carries 1 of 7 entries invites a half-finished demand to go out; the paralegal cannot answer 'what is ready to send' from the overview.",
69	   "fix": "Separate 'Can export' (gate passes, items undecided; amber, with the unreviewed count) from 'Ready to send' (nothing pending, no edit to check; green). The Ready filter uses the stricter test.",
70	   "acceptance_test": "e2e: a case with pending items has no cases-chip-ready and is not under the ready filter; a case with 0 pending and 0 edits to check shows the green chip and is listed."},
71	  {"severity": "major", "title": "The case overview block does not say what to do first; overview block, Open decisions and What you need to do disagree, and the action names no item",
72	   "evidence": "o3.out.txt sample: block 'Export blocked (1): Nothing is accepted or edited yet'; Open decisions 'Start review' focuses f_r7_1 (flag); case-next-action 'Decide the 2 detected charges'. lib02: case-next-action 'This item cannot be used. Dismiss it, or write the entry by hand from the record.' with no item named while the block shows 7 entries and 8 flags to decide; o2-detail-sample-1440.png; o4-lib01-show-step.png (raw 'record ids [\"r3\"]')",
73	   "why_it_matters": "She asked 'what do I do first?' on opening the case and got three answers or an unnamed 'this item'; the first screen at 900 px holds only two entry rows.",
74	   "fix": "One 'Do this first' line in the overview block from the server's next action, naming record and provider, with one button to it; 'Start review' and the case-checks bar repeat the same action only.",
75	   "acceptance_test": "e2e on the Rivera sample and lib02: the overview block has exactly one 'Do this first' line naming a record or provider; its button focuses that item; Start review and the case-checks bar never name a different target."},
76	  {"severity": "minor", "title": "A never-analyzed case shows '9 need review' and 'Export blocked: Nothing is accepted' with no hint to run the analysis",
77	   "evidence": "o1.out.txt row 'Spanish-language records, back pain | Not analyzed yet | Entries None | 9 need review | Export blocked (1) | Nothing is accepted or edited yet'; o2.out.txt lib09 detail 'Read by code only. No model has been called yet.'",
78	   "why_it_matters": "The reason shown is not the reason she must act; the real next step (Analyze) is only visible after opening the case.",
79	   "fix": "For an ingested case the row's reason reads 'Not analyzed. Open it and press Analyze' and the review and blocker chips are dropped.",
80	   "acceptance_test": "e2e: an ingested case row has no cases-chip-blocked and no cases-chip-needs-review and its reason text contains 'Analyze'."},
81	  {"severity": "minor", "title": "Row says how many items need review but never why",
82	   "evidence": "o1.out.txt chips '4 need review', '8 need review' with no kind; case trace 'kinds: gap 1, conflict 2, pre existing 2, causation 5' exists on the server (r2 stepper text in T-136-paralegal-r3/r2.stdout.txt)",
83	   "why_it_matters": "Checklist item 16: items needing review say why in one sentence; she cannot rank cases by what the adjuster will attack (a date conflict, a gap).",
84	   "fix": "One line under the chips: '1 date conflict, 1 gap, 2 prior conditions', from the server's counts.",
85	   "acceptance_test": "e2e: the Rivera sample row contains 'conflict' and 'gap' counts equal to the flags of those kinds in GET /api/cases/{token}."},
86	  {"severity": "minor", "title": "AC evidence 'test_multicase.py 17 pass' does not reproduce: the keyboard test fails on HEAD",
87	   "evidence": "artifacts/review-evidence/T-149-paralegal/pytest-multicase.out.txt: '1 failed, 16 passed, 1 skipped'; tests/e2e/test_multicase.py:253 'ArrowDown moves to the next row's link'; the same failure in a second run; live check o5.out.txt ArrowDown/j/Tab move focus 3 of 3 with a 600 ms wait",
88	   "why_it_matters": "The card's own AC (keyboard usable) is evidenced by a test that fails in a clean archive; a key pressed right after the list paints is lost.",
89	   "fix": "Bind the key handler before the rows paint, or wait on a ready marker in the test, and state which in the card.",
90	   "acceptance_test": "plain pytest tests/e2e/test_multicase.py in a clean archive: 17 passed, 3 runs in a row."}
91	 ],
92	 "whats_right": [
93	  "Overview rows carry the server's own plain blocker sentence, per-kind decided/total bars and counts that match GET /api/cases; Back and All cases return with focus on the case link and the counts refresh after an accept.",
94	  "Sorting by 'Needs attention first' puts blocked and unanalyzed cases on top, filters and sort hold across open and back, and the 390 px overview and detail have no horizontal overflow.",
95	  "The detail's export-gate steps open with 'Show this step' and land on the right step with its 'Go to the record' button."
96	 ],
97	 "questions_for_chris": ["Should the overview show a deadline per case (Stowers or limitation date)? A paralegal sorts her cases by it; the records carry no such date, so it would be a field she types. Outside my lens to decide, but it changes what 'needs me first' means."]}
98	```
99	
100	Erratum (appended, same review): where I wrote that ArrowDown, j and Tab moved focus (the F-6 paragraph and the F-6 evidence field), read "ArrowDown and Tab moved focus; j did nothing" (o5.out.txt, 3 of 3 runs). It does not change any finding.
101	
````

### User / tool · 2026-11-02T15:37:00.245Z

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

### User / tool · 2026-11-02T15:37:00.432Z

**tool result**
````
---
id: "T-149"
title: "Multi-case UI (Chris inbox 13:23Z): case Overview (list of cases with status, progress bar, HITL call-outs, export ready; sort/filter; open a case) and case Detail (case overview header: progress, call-outs, gate stepper summary, then the breakdown: timeline, flags, amounts, tray)"
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P1"
depends_on: ["T-148"]
created_by: "orchestrator"
created_at: "2026-11-02T13:25:02Z"
updated_at: "2026-11-02T15:36:38Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T13:37:24Z"
rounds: 1
commits: ["1394661", "802d5fd"]
reviews:
  - {"persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-149-ux-designer.md", "at": "2026-11-02T14:30:40Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-149-paralegal.md", "at": "2026-11-02T14:35:33Z"}
ac:
  - {"n": 1, "text": "overview lists all cases with status/progress/call-outs from GET /api/cases; clicking opens the detail; detail starts with a case overview block then the existing breakdown; keyboard and 390px usable; e2e; screenshots artifacts/screenshots/multicase-*.png", "done": true, "evidence": "tests/e2e/test_multicase.py 36 pass from git archive HEAD 802d5fd; clean-tree full e2e 315 pass, 4 fail outside this card (D-060 letter totals x3, charge_confirm focus race passes alone); unit suite pass; screenshots artifacts/screenshots/multicase-*.png"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:25:05Z orchestrator: assigned: frontend
- 2026-11-02T13:37:24Z frontend: claimed
- 2026-11-02T13:53:35Z frontend: AC 1 checked: tests/e2e/test_multicase.py 17 pass (+screenshots test); artifacts/screenshots/multicase-{overview,detail}-{1440,390}.png
- 2026-11-02T14:22:45Z frontend: moved in_progress -> in_review
- 2026-11-02T14:22:59Z orchestrator: review dispatched: ux-designer-reviewer, paralegal-reviewer
- 2026-11-02T14:30:40Z orchestrator: review ux-designer-reviewer (claude-sonnet-5-5): changes — reviews/T-149-ux-designer.md; round 1; findings:
    - [major] Overview 'need review' call-out stays after every item is decided, and the Needs attention filter keeps the finished case — fix: Show the chip from undecided needs_review items (needs_review among pending), or have the backend return that count; drive the Needs attention filter from the same number. Keep 'could not be verified' as a quiet note, not an amber call-out, since it needs n
    - [major] Overview load failure and open failure are invisible; no loading state — fix: Render the Cases section in a 'Loading cases...' state, an error state with the plain sentence and a Retry button in the same place when the list fails (distinguish 404 'multi-case not available' from 500), and keep the open-case error visible (do not clear loadErr in load(); show it on the clicked row or a
    - [major] The case overview block repeats three summaries already above the first entry and pushes the work down on a phone — fix: Merge, do not stack: let the case overview block own progress, call-outs and the gate steps, and drop the duplicate 'Case checks' summary row and the 'Open decisions' count text (keep the jump buttons). On the phone keep the block to progress plus chips and put the
    - [major] Green 'Ready to export' sits beside '8 need review' and '18 items are not reviewed'; the Ready filter lists such cases — fix: Change the chip and filter wording to something true to the gate, for example 'Export open: 1 accepted, 18 not reviewed' in amber, and keep green for 'Everything decided'. Add a fourth filter or make Needs attention and Ready mutually exclusive.
    - [minor] Not-analyzed row says '3 need review / Export blocked' and has no next action; the detail shows none of it — fix: For status ingested, replace the chips with one call-out 'Not analyzed: open the case and press Analyze' and show 'Not started' instead of 'None' in the bars.
    - [minor] Failed and running rows keep full review chips, and a failed row gives no reason or retry — fix: On a failed row show the run's reason in a sentence and 'Open the case to run it again'; hide the review chips for a failed or running case.
    - [minor] 'Needs attention' is not a useful partition: it equals All, and overlaps Ready to export — fix: Define the filters as non-overlapping states (Not analyzed, In review, Ready, Done) or show counts per state; once finding 1 is fixed re-check that Needs attention excludes finished cases.
    - [minor] Row is dense and has no search; status is split over three places — fix: One status pill per row at the top of the call-out column; one overall 'n of N decided' next to the three bars; show 'Last activity' only (created date on hover or in the detail); add a title search field beside the filters.
    - [minor] Failing and pending export steps look the same ('Needs your decision'); the word fail never appears — fix: Use a different glyph and word for fail ('Check failed') than for waiting ('Waiting for you').
    - [minor] Focus is lost when a case opens from the keyboard — fix: Move focus to the case heading (tabindex -1) when the detail opens and announce the case name.
- 2026-11-02T14:30:49Z orchestrator: assigned: frontend
- 2026-11-02T14:30:49Z orchestrator: moved changes_requested -> blocked: waits for the paralegal T-149 review (in flight) so round 2 fixes both at once
- 2026-11-02T14:35:33Z orchestrator: review paralegal-reviewer (claude-sonnet-5-5): changes — reviews/T-149-paralegal.md
- 2026-11-02T14:35:39Z orchestrator: Round 2 scope (UX + paralegal): (1) overview counts refresh after decisions (no stale '2 need review'); (2) loading state, and visible load/open errors; (3) detail overview block must not duplicate Case checks / Open decisions - merge into one, first entry above the fold at 390; (4) never green 'Ready to export' while items are unreviewed: amber 'Can export - N not reviewed (they stay out of the letter)'; (5) case names: name on create + rename, default from first record header (API T-157); (6) one 'Do this first' line naming the item from case_list.next_action (T-157) with a link; (7) j/k in the overview; (8) rerun offered only when item.rerun_available (T-157, T-136 debt); plus minors. Start on the UI-only items now; wire T-157 fields when they land.
- 2026-11-02T14:35:39Z orchestrator: moved blocked -> in_progress
- 2026-11-02T15:28:51Z frontend: r2 progress: UI items 1-7 done in the working tree (overview.js/css, timeline.js slot, stepper rerun gate, api/app/input): live counts + needs_review_open fallback, loading/error/retry/open-error states, ONE merged detail block (do-first from next_action, chips, todo strip + case checks inside it), amber 'Can export - N not reviewed', j/k + search + heading focus, rename + case name on create + T-157 titles, rerun only when rerun_available. Clean-tree e2e (HEAD archive + my overlay): 315 pass, 4 fail all outside this card (backend/letter specs). T-158 committed 0b2ce9c (in_review). Left: verify HEAD review.js (user warns an earlier commit broke it), commit T-149 via temp index, refresh screenshots, handoff, T-160.
- 2026-11-02T15:36:24Z frontend: AC 1 checked: tests/e2e/test_multicase.py 36 pass from git archive HEAD 802d5fd; clean-tree full e2e 315 pass, 4 fail outside this card (D-060 letter totals x3, charge_confirm focus race passes alone); unit suite pass; screenshots artifacts/screenshots/multicase-*.png
- 2026-11-02T15:36:25Z frontend: moved in_progress -> in_review
- 2026-11-02T15:36:38Z orchestrator: review dispatched: ux-designer-reviewer, paralegal-reviewer

## Handoff
What changed (r2, 802d5fd): 1 counts refresh (open-only needs-review, falls back when server lacks needs_review_open); 2 Loading/error/Try again/open-error states; 3 ONE detail block (progress, Do this first from next_action, chips, Open decisions and Case checks inside it); 4 amber 'Can export — N not reviewed (they stay out of the letter)', green only for 'Everything decided'; 5 case name field on create, Rename, T-157 titles; 6 Do this first line + Go to it; 7 j/k and arrows, title search, heading focus; 8 rerun only when item.rerun_available (else 'cannot be run again here'); minors: one status pill, n of N decided, Not started, failed/not analyzed call-outs, created date on hover, filters Needs attention vs Ready to send. · Verified: test_multicase 36 pass (written first) from git archive HEAD; clean-tree full e2e 315 pass / 4 fail outside card; unit pass; screenshots refreshed. · Left: backend should add hitl.needs_review_open (note on T-157); skipped: fail-vs-waiting glyph in stepper (many stepper tests pin the words), 'why' line under chips (needs kinds in the list). First entry at 390x844 is ~804 px (date line visible), not fully above the fold. · Surprised: list hitl.needs_review never falls after decisions; CSP blocks wait_for_function strings.

985dbd2 fix(backend): T-139 r4 one money detector (money.py) for the hold, the export gate and the letter eval; the gate scans the final letter text and blocks naming the line; labelled figures and number words after a money verb are money; held-out hints state the true cause
67be38d fix(frontend): T-162 r2 a collapsed Dismissed group says how many of its items carry a re-run note; e2e opens the group and asserts the entry and amount notes visible, unconditional; note helpers at module scope
a4eeb2b docs(orchestrator): scope cut 7e charge-source detection residuals (T-140)
94a31a4 fix(frontend): T-160 the Not in an entry (n) link sits in the entry head line right after the record chip, so it never takes a line of its own; rows are back inside the T-060 compact-row budget (<=2 px)
802d5fd feat(frontend): T-149 r2 one merged case overview block (do-this-first from next_action, amber Can export, open-count chips), loading/error/retry states, j/k and search, case names (create, rename, T-157 titles), rerun only when rerun_available
````

### User / tool · 2026-11-02T15:37:00.439Z

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

### User / tool · 2026-11-02T15:37:00.440Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:04.706Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git diff --stat 802d5fd HEAD -- app/frontend | tail -5; ls artifacts/review-evidence/T-149-paralegal/ | head -30; cat artifacts/review-evidence/T-060-paralegal-pass4-serve.py; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls $SP | head"
}
````

### User / tool · 2026-11-02T15:37:04.838Z

**tool result**
````
985dbd2
 app/frontend/review.js     | 17 +++++++++++------
 app/frontend/timeline.js   |  5 +++--
 app/frontend/uncovered.css |  3 +++
 app/frontend/uncovered.js  |  5 +++--
 4 files changed, 20 insertions(+), 10 deletions(-)
o1-filter-needs.png
o1-filter-ready.png
o1-overview-1440.png
o1.out.txt
o1_overview.py
o2-detail-lib02-1440.png
o2-detail-lib02-full.png
o2-detail-lib06-1440.png
o2-detail-lib06-full.png
o2-detail-lib09-1440.png
o2-detail-lib09-full.png
o2-detail-sample-1440.png
o2-detail-sample-full.png
o2.out.txt
o2_detail.py
o3.out.txt
o3_next.py
o4-detail-390.png
o4-lib01-show-step.png
o4-overview-390.png
o4-overview-after-accept.png
o4.out.txt
o4_actions.py
o5.out.txt
o5_keys.py
o6-eleven-cases.png
o6.out.txt
o6_many.py
pytest-multicase.out.txt
setup.out.txt
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
M1
M1_nocombine
M2
M2_find0
MASTER_PROMPT.md
T-047-run1.json
T-060-pass2-head
T-093-r3-2ab7896
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:10.633Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $SP/r2-802d5fd && git archive 802d5fd | tar -x -C $SP/r2-802d5fd && ls $SP/r2-802d5fd | head -20; ls artifacts/review-evidence/T-149-paralegal/*.py; sed -n 1,80p artifacts/review-evidence/T-149-paralegal/o6_many.py; ls tests/e2e/test_multicase.py; ls artifacts/review-evidence | grep -i setup"
}
````

### User / tool · 2026-11-02T15:37:11.209Z

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
artifacts/review-evidence/T-149-paralegal/o1_overview.py
artifacts/review-evidence/T-149-paralegal/o2_detail.py
artifacts/review-evidence/T-149-paralegal/o3_next.py
artifacts/review-evidence/T-149-paralegal/o4_actions.py
artifacts/review-evidence/T-149-paralegal/o5_keys.py
artifacts/review-evidence/T-149-paralegal/o6_many.py
artifacts/review-evidence/T-149-paralegal/setup_cases.py
from playwright.sync_api import sync_playwright
OUT = "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal/"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("http://127.0.0.1:7941/"); pg.get_by_test_id("cases-overview").wait_for(); pg.wait_for_timeout(800)
    print("inputs on home:", pg.evaluate("()=>Array.from(document.querySelectorAll('input,textarea')).map(e=>(e.getAttribute('data-testid')||e.name||e.type)+':'+(e.placeholder||'').slice(0,40))"))
    pg.get_by_test_id("cases-sort").select_option("attention"); pg.wait_for_timeout(300)
    print("ATTENTION order:", [r.get_by_test_id("cases-title").inner_text() + " / " + r.get_by_test_id("cases-dates").inner_text().split("·")[0].strip()[:34] for r in pg.locator('[data-testid=cases-row]').all()])
    pg.screenshot(path=OUT + "o6-eleven-cases.png", full_page=False)
    print("row height px:", pg.locator('[data-testid=cases-row]').first.bounding_box()["height"])
    b.close()
tests/e2e/test_multicase.py
T-081-ux-r3-setup.py
T-104-ux-designer-setup.py
T-149-ux-setup.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:17.010Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-149-paralegal/setup_cases.py; grep -n \"rename\\|case-name\\|do-first\\|data-testid\" /private/tmp/claude-501/*/*/*/scratchpad/r2-802d5fd/app/frontend/overview.js 2>/dev/null | head -80"
}
````

### User / tool · 2026-11-02T15:37:17.499Z

**tool result**
````
"""Seed 6 cases on the review server (127.0.0.1:7941) via the API. Prints tokens and a summary of GET /api/cases."""
import json, sys, time, urllib.request
B = "http://127.0.0.1:7941"
def api(m, p, body=None):
    d = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(B + p, data=d, method=m, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=120) as f:
            t = f.read(); return f.status, (json.loads(t) if t else None)
    except urllib.error.HTTPError as e:
        t = e.read(); return e.code, (json.loads(t) if t else None)
def run(tok):
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"): return s["status"]
        time.sleep(0.5)
toks = {}
for key, lib in [("lib01", "case_lib01_er_only_then_gap"), ("lib06", "case_lib06_lop_billed_vs_adjusted"), ("lib02", "case_lib02_slip_fall_prior_knee"),
                 ("lib03", "case_lib03_truck_rear_end_chiro"), ("lib09", "case_lib09_spanish_interpreter_espalda")]:
    st, c = api("POST", "/api/cases", {"library": lib}); assert st in (200, 201), (st, c)
    toks[key] = c["token"]
    if key != "lib09": print(key, run(c["token"]))
txt = open("/Users/arsis/zlayt-pm-project/evals/golden/sample.txt").read()
st, c = api("POST", "/api/cases", {"name": "Rivera sample", "text": txt}); assert st in (200, 201), (st, c)
toks["sample"] = c["token"]; print("sample", run(c["token"]))
json.dump(toks, open("/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal/tokens.json", "w"))
# lib06: accept every verified entry so it is mostly done; lib03: accept one entry
for key, n in (("lib06", 99), ("lib03", 1)):
    ents = [e for e in api("GET", f"/api/cases/{toks[key]}")[1]["entries"] if e["state"] == "verified"]
    for e in ents[:n]: api("POST", f"/api/cases/{toks[key]}/items/{e['id']}/review", {"action": "accept"})
for s in api("GET", "/api/cases")[1]["cases"]:
    print(json.dumps({k: s.get(k) for k in ("token", "title", "status", "progress", "hitl", "export_ready")})[:700])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:24.071Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/*/*/*/scratchpad/r2-802d5fd 2>/dev/null || cd $(ls -d /private/tmp/claude-501/*/*/*/scratchpad/r2-802d5fd | head -1); pwd; grep -on \"data-testid[=\\\"']*[a-z-]*\\|testid[:=\\\"' ]*[a-z-]*\" app/frontend/overview.js | sort -u -t: -k3 | head -80; grep -n \"Untitled\\|Rename\" app/frontend/*.js | head -20"
}
````

### User / tool · 2026-11-02T15:37:24.204Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:27.230Z

**tool call — Bash**
````
{
 "command": "R=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r2-802d5fd\"; cd $R && grep -ohE \"(data-testid|testid)[\\\"'=, ]+[a-z0-9-]+\" app/frontend/overview.js | sort -u | head -80; grep -n \"Untitled\\|Rename\" app/frontend/*.js | head -20; echo $R > /dev/null"
}
````

### User / tool · 2026-11-02T15:37:27.334Z

**tool result**
````
data-testid="case-heading
data-testid="case-overview
app/frontend/overview.js:57:  const titleOf = (s) => (/^case[ _]lib\d+/i.test(s.name || "") ? ZL.niceName(s.name) : s.title || ZL.niceName(s.name) || "Untitled case");
app/frontend/overview.js:258:  // ---- naming a case (T-157 PATCH /api/cases/{token} {title}): a Rename button beside the name in the header; Enter saves, Escape leaves the old name.
app/frontend/overview.js:263:    if (renameBox && !s.case) endRename(false);
app/frontend/overview.js:265:  function endRename(focusBtn) {
app/frontend/overview.js:271:  function startRename() {
app/frontend/overview.js:279:      if (title === cur) return endRename(true);
app/frontend/overview.js:288:        endRename(true); load();
app/frontend/overview.js:291:    input.addEventListener("keydown", (ev) => { if (ev.key === "Enter") { ev.preventDefault(); save(); } else if (ev.key === "Escape") { ev.preventDefault(); ev.stopPropagation(); endRename(true); } });
app/frontend/overview.js:293:      el("button", { type: "button", class: "btn btn--sm", onclick: () => endRename(true) }, "Cancel"), err);
app/frontend/overview.js:299:    renameBtn = el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-rename-case", "aria-label": "Rename this case", hidden: true, onclick: startRename }, "Rename");
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:30.892Z

**tool call — Bash**
````
{
 "command": "R=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r2-802d5fd\"; cd $R && grep -ohE \"[a-z]+-[a-z0-9-]+\" app/frontend/overview.js | grep -E \"^(cases|case|btn|do|todo)-\" | sort -u | tr '\\n' ' '; echo; grep -n \"case-name\\|name-input\\|cases-name\\|input-name\" app/frontend/*.js app/frontend/*.html | head; sed -n 255,300p app/frontend/overview.js"
}
````

### User / tool · 2026-11-02T15:37:30.990Z

**tool result**
````
btn--primary btn--sm btn-all-cases btn-do-first btn-rename-case btn-save-rename case-heading case-name case-overview case-rename-error case-rename-input cases-body cases-count cases-dates cases-decided cases-empty cases-filter- cases-list cases-load-error cases-loading cases-next cases-open cases-open-error cases-retry cases-row cases-search cases-sort cases-stage cases-title do-first 
app/frontend/app.js:28:    $("#case-name").hidden = !c; if (c) $("#case-name").textContent = nameOf(s) || "Case";
app/frontend/overview.js:274:    const input = el("input", { type: "text", class: "cv-rename-input", "data-testid": "case-rename-input", maxlength: "120", value: cur, "aria-label": "Case name", autocomplete: "off" });
app/frontend/overview.js:298:    caseNameEl = ZL.$("#case-name"); if (!caseNameEl) return;
app/frontend/index.html:23:    <span id="case-name" class="case-name" data-testid="case-name" hidden></span>
    load();
  });

  // ---- naming a case (T-157 PATCH /api/cases/{token} {title}): a Rename button beside the name in the header; Enter saves, Escape leaves the old name.
  let caseNameEl = null, renameBtn = null, renameBox = null;
  function renameSync(s) {
    if (!renameBtn) return;
    renameBtn.hidden = !(available === true && s.case) || !!renameBox;
    if (renameBox && !s.case) endRename(false);
  }
  function endRename(focusBtn) {
    if (renameBox) { renameBox.remove(); renameBox = null; }
    if (caseNameEl) caseNameEl.hidden = !ZL.state.get().case;
    renameSync(ZL.state.get());
    if (focusBtn && renameBtn && !renameBtn.hidden) renameBtn.focus();
  }
  function startRename() {
    const s = ZL.state.get(); if (!s.case || renameBox) return;
    const cur = (ZL.caseTitles || {})[s.token] || caseNameEl.textContent || "";
    const input = el("input", { type: "text", class: "cv-rename-input", "data-testid": "case-rename-input", maxlength: "120", value: cur, "aria-label": "Case name", autocomplete: "off" });
    const err = el("span", { class: "rv-error small", role: "alert", "data-testid": "case-rename-error" });
    const save = async () => {
      const title = input.value.trim();
      if (!title) { err.textContent = "Type a name for the case."; return; }
      if (title === cur) return endRename(true);
      save.busy = true; err.textContent = "";
      try {
        const r = await ZL.api.rename(s.token, title), shown = (r && r.title) || title;
        ZL.caseTitles[s.token] = shown; caseNameEl.textContent = shown;
        if (ZL.state.get().case) document.title = "Treatment timeline \u00b7 " + shown;
        const sm = summaryOf(s.token); if (sm) { sm.title = shown; sm.name = (r && r.name) || shown; }
        if (ZL.state.get().case) { ZL.state.get().case.title = shown; ZL.state.get().case.name = (r && r.name) || shown; }
        const h2 = document.querySelector('[data-testid="case-heading"]'); if (h2) h2.setAttribute("aria-label", "Case overview: " + shown);
        endRename(true); load();
      } catch (e) { err.textContent = (e && e.message) || "The name could not be saved."; input.focus(); }
    };
    input.addEventListener("keydown", (ev) => { if (ev.key === "Enter") { ev.preventDefault(); save(); } else if (ev.key === "Escape") { ev.preventDefault(); ev.stopPropagation(); endRename(true); } });
    renameBox = el("span", { class: "cv-rename" }, input, el("button", { type: "button", class: "btn btn--sm btn--primary", "data-testid": "btn-save-rename", onclick: save }, "Save"),
      el("button", { type: "button", class: "btn btn--sm", onclick: () => endRename(true) }, "Cancel"), err);
    caseNameEl.hidden = true; renameBtn.hidden = true; caseNameEl.after(renameBox);
    input.focus(); input.select();
  }
  document.addEventListener("DOMContentLoaded", () => {
    caseNameEl = ZL.$("#case-name"); if (!caseNameEl) return;
    renameBtn = el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-rename-case", "aria-label": "Rename this case", hidden: true, onclick: startRename }, "Rename");
    caseNameEl.after(renameBtn);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:33.794Z

**tool call — Bash**
````
{
 "command": "R=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r2-802d5fd\"; cd $R && grep -n \"name\" app/frontend/input.js | head -20; grep -n \"title\" app/backend/*.py | grep -i \"def \\|first\\|default\\|untitled\" | head -20"
}
````

### User / tool · 2026-11-02T15:37:33.896Z

**tool result**
````
33:    if (/\.pdf$/i.test(f.name) || f.type === "application/pdf") { ev.target.value = ""; return showError(PDF_MSG); }
34:    if (!/\.txt$/i.test(f.name) && f.type && f.type !== "text/plain") { ev.target.value = ""; return showError("Only .txt files are accepted. Paste the text instead, or save the file as plain text."); }
37:    rd.onload = () => { pending = { text: String(rd.result) }; ZL.$("#file-name").textContent = f.name; submitText(); };
50:        el("label", { for: "case-title", class: "lbl" }, "Case name (optional)"),
59:          el("span", { id: "file-name", class: "muted" })),
82:  // ---- processing state: a real progress element, the stage in plain words, elapsed seconds after a while, skeleton rows. No raw stage names.
105:    pending = null; history.replaceState(null, "", location.pathname + location.search);
app/backend/api.py:253:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
app/backend/api.py:340:        """T-157: body {title}. A blank or null title clears the name: the title goes back to the one derived from the first record header."""
app/backend/case_list.py:40:def validate_title(value) -> str:
app/backend/case_list.py:52:def plain_title(value) -> str:
app/backend/case_list.py:57:def clean_title(value) -> str:
app/backend/case_list.py:64:def derived_title(conn, case_id) -> str:
app/backend/case_list.py:65:    """T-157: the title of a case nobody named, from its first record header: the provider (Source line) and that record's date, "Marrowgate General ED, Feb 14, 2026".
app/backend/case_list.py:91:def readable_title(name, source, created_at) -> str:
app/backend/case_list.py:92:    """A name a paralegal would recognise; no name at all becomes "Records added Nov 1" (T-157: never "Untitled case"; `case_title` prefers the first record header over that fallback)."""
app/backend/case_list.py:100:def case_title(conn, case: dict) -> str:
app/backend/case_list.py:102:    Never "Untitled case", never markup."""
app/backend/conflicts.py:170:        title, expl = flag_templates.render("conflict", category, stated=a["iso"], quote=a["quote"], date=first,
app/backend/flag_templates.py:63:def _single(title, lead):
app/backend/flag_templates.py:68:def _pair(title):
app/backend/gaps.py:60:    (last comma segment) of the header label, or from the record's own first-line title; (2) no visit word appears in the label outside parentheses and
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:37.655Z

Start the server.

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:40.266Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p artifacts/review-evidence/T-149-paralegal-r2; rm -f $SP/r2.db; (env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$SP/r2.db PORT=7943 HOST=127.0.0.1 nohup .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py $SP/r2-802d5fd > $SP/r2-server.log 2>&1 &) ; sleep 6; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7943/; lsof -iTCP:7943 -sTCP:LISTEN -nP | tail -1"
}
````

### User / tool · 2026-11-02T15:37:46.455Z

**tool result**
````
200
Python  1826 arsis    9u  IPv4 0xc837ac7d28aec599      0t0  TCP 127.0.0.1:7943 (LISTEN)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:49.726Z

**tool call — Bash**
````
{
 "command": "ls evals/ evals/library 2>/dev/null | head -30; head -c 600 evals/golden/sample.txt"
}
````

### User / tool · 2026-11-02T15:37:49.807Z

**tool result**
````
evals/:
__init__.py
__pycache__
adversarial
golden
heldout_audit.py
j3_controls.py
letter_check.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
reports
run.py

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
SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data

=== Record 1 ===
Date: 2026-01-09
Source: Austin EMS run report
Excerpt: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."

=== Record 2 ===
Date: 2026-01-09
Source: Central ER discharge summary
Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."

=== Record 3 ===
Date: 2026-01-16
Source: D
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:37:56.665Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/setup_r2.py <<'EOF'\nimport json, sys, time, urllib.request\nB = \"http://127.0.0.1:7943\"\ndef api(m, p, body=None):\n    d = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(B + p, data=d, method=m, headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(r, timeout=120) as f:\n            t = f.read(); return f.status, (json.loads(t) if t else None)\n    except urllib.error.HTTPError as e:\n        t = e.read(); return e.code, (json.loads(t) if t else None)\ndef run(tok):\n    assert api(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\n    for _ in range(300):\n        s = api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n        if s[\"status\"] in (\"ready\", \"failed\"): return s[\"status\"]\n        time.sleep(0.5)\nL = \"/Users/arsis/zlayt-pm-project/evals/library/\"\nplan = [(\"sample\", \"/Users/arsis/zlayt-pm-project/evals/golden/sample.txt\", None, True),\n        (\"lib01\", L+\"case_lib01_er_only_then_gap.txt\", None, True),\n        (\"lib02\", L+\"case_lib02_slip_fall_prior_knee.txt\", None, True),\n        (\"lib03\", L+\"case_lib03_truck_rear_end_chiro.txt\", \"Delgado v. Hartwell (truck)\", True),\n        (\"lib06\", L+\"case_lib06_lop_billed_vs_adjusted.txt\", \"Okafor LOP\", True),\n        (\"lib09\", L+\"case_lib09_spanish_interpreter_espalda.txt\", None, False)]\ntoks = {}\nfor key, path, name, do_run in plan:\n    body = {\"text\": open(path).read()}\n    if name: body[\"name\"] = name\n    st, c = api(\"POST\", \"/api/cases\", body); print(key, st, (c or {}).get(\"token\"), (c or {}).get(\"title\"), (c or {}).get(\"name\"))\n    if st not in (200, 201): print(c); continue\n    toks[key] = c[\"token\"]\n    if do_run: print(\"  run\", run(c[\"token\"]))\njson.dump(toks, open(\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/tokens.json\", \"w\"))\nprint(\"--- GET /api/cases\")\nfor s in api(\"GET\", \"/api/cases\")[1][\"cases\"]:\n    print(json.dumps({k: s.get(k) for k in (\"token\",\"title\",\"name\",\"status\",\"next_action\",\"export_ready\",\"hitl\")})[:900])\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/setup_r2.py > artifacts/review-evidence/T-149-paralegal-r2/setup.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/setup.out.txt"
}
````

### User / tool · 2026-11-02T15:37:59.868Z

**tool result**
````
sample 201 Rz5jicMgA7vctUDY_rV9UQ Austin EMS run report, Jan 9, 2026 None
  run ready
lib01 201 d0Fj3f-itbTvXM9-0oPY2g Dunmarrow Fire-Rescue run report, Feb 14, 2026 None
  run ready
lib02 201 5m4ca8ArAHp8i_ox1Fz3OA Sablewood Market first-aid log, Mar 9, 2026 None
  run ready
lib03 201 FeoeeA0Ibkw5IuG9Y4F_Xw Delgado v. Hartwell (truck) Delgado v. Hartwell (truck)
  run ready
lib06 201 ERA-FKgVMyPHZP6KV3wKgg Okafor LOP Okafor LOP
  run ready
lib09 201 eTCVrQD2W45aQl4LvnX_2g Quillmere Regional ED, Mar 3, 2026 None
--- GET /api/cases
{"token": "eTCVrQD2W45aQl4LvnX_2g", "title": "Quillmere Regional ED, Mar 3, 2026", "name": null, "status": "ingested", "next_action": {"item_id": null, "kind": "run", "reason": "Run the case to draft the timeline. Nothing is waiting for you until then."}, "export_ready": false, "hitl": {"pending": 9, "needs_review": 9, "edits_to_check": 0, "could_not_verify": 0, "gate_blockers": [{"reason_code": "NOTHING_ACCEPTED", "kind": "case", "item_id": null, "why": "Nothing is accepted or edited yet, so the letter would be empty."}], "gate_warnings": [{"reason_code": "ITEMS_NOT_REVIEWED", "count": 9, "why": "9 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them."}]}}
{"token": "ERA-FKgVMyPHZP6KV3wKgg", "title": "Okafor LOP", "name": "Okafor LOP", "status": "ready", "next_action": {"item_id": "f_r3_2", "kind": "flag", "reason": "The phrase list found this flag but the AI did not; check that it applies."}, "export_ready": false, "hitl": {"pending": 19, "needs_review": 9, "edits_to_check": 0, "could_not_verify": 1, "gate_blockers": [{"reason_code": "NOTHING_ACCEPTED", "kind": "case", "item_id": null, "why": "Nothing is accepted or edited yet, so the letter would be empty."}], "gate_warnings": [{"reason_code": "ITEMS_NOT_REVIEWED", "count": 19, "why": "19 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them."}]}}
{"token": "FeoeeA0Ibkw5IuG9Y4F_Xw", "title": "Delgado v. Hartwell (truck)", "name": "Delgado v. Hartwell (truck)", "status": "ready", "next_action": {"item_id": "a2", "kind": "amount", "reason": "This figure is a rate, not a charge, so it is not added to the total."}, "export_ready": false, "hitl": {"pending": 14, "needs_review": 4, "edits_to_check": 0, "could_not_verify": 0, "gate_blockers": [{"reason_code": "NOTHING_ACCEPTED", "kind": "case", "item_id": null, "why": "Nothing is accepted or edited yet, so the letter would be empty."}], "gate_warnings": [{"reason_code": "ITEMS_NOT_REVIEWED", "count": 14, "why": "14 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them."}]}}
{"token": "5m4ca8ArAHp8i_ox1Fz3OA", "title": "Sablewood Market first-aid log, Mar 9, 2026", "name": null, "status": "ready", "next_action": {"item_id": "f_r2_1", "kind": "flag", "reason": "The AI found this flag but the phrase list did not; check that it applies."}, "export_ready": false, "hitl": {"pending": 18, "needs_review": 6, "edits_to_check": 0, "could_not_verify": 1, "gate_blockers": [{"reason_code": "NOTHING_ACCEPTED", "kind": "case", "item_id": null, "why": "Nothing is accepted or edited yet, so the letter would be empty."}], "gate_warnings": [{"reason_code": "ITEMS_NOT_REVIEWED", "count": 18, "why": "18 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them."}]}}
{"token": "d0Fj3f-itbTvXM9-0oPY2g", "title": "Dunmarrow Fire-Rescue run report, Feb 14, 2026", "name": null, "status": "ready", "next_action": {"item_id": "f_r3_1", "kind": "flag", "reason": "The AI found this flag but the phrase list did not; check that it applies."}, "export_ready": false, "hitl": {"pending": 9, "needs_review": 2, "edits_to_check": 0, "could_not_verify": 1, "gate_blockers": [{"reason_code": "NOTHING_ACCEPTED", "kind": "case", "item_id": null, "why": "Nothing is accepted or edited yet, so the letter would be empty."}], "gate_warnings": [{"reason_code": "ITEMS_NOT_REVIEWED", "count": 9, "why": "9 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them."}]}}
{"token": "Rz5jicMgA7vctUDY_rV9UQ", "title": "Austin EMS run report, Jan 9, 2026", "name": null, "status": "ready", "next_action": {"item_id": "a2", "kind": "amount", "reason": "This figure is a rate, not a charge, so it is not added to the total."}, "export_ready": false, "hitl": {"pending": 23, "needs_review": 3, "edits_to_check": 0, "could_not_verify": 0, "gate_blockers": [{"reason_code": "NOTHING_ACCEPTED", "kind": "case", "item_id": null, "why": "Nothing is accepted or edited yet, so the letter would be empty."}], "gate_warnings": [{"reason_code": "ITEMS_NOT_REVIEWED", "count": 23, "why": "23 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them."}]}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:38:09.680Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p1_overview.py <<'EOF'\nimport json\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(1200)\n    print(\"inputs on home:\", pg.evaluate(\"()=>Array.from(document.querySelectorAll('input,textarea')).map(e=>(e.getAttribute('data-testid')||e.id||e.type)+':'+(e.placeholder||e.getAttribute('aria-label')||'').slice(0,40))\"))\n    print(\"filter chips:\", [x.inner_text() for x in pg.locator('[data-testid^=cases-filter-]').all()])\n    pg.screenshot(path=OUT+\"p1-overview-default.png\")\n    for sort in [\"attention\", \"recent\"]:\n        try:\n            pg.get_by_test_id(\"cases-sort\").select_option(sort); pg.wait_for_timeout(300)\n        except Exception as e: print(\"sort\", sort, e); continue\n        print(\"=== sort\", sort)\n        for r in pg.locator('[data-testid=cases-row]').all():\n            print(\"ROW>>\", \" | \".join(t.strip() for t in r.inner_text().split(\"\\n\") if t.strip()))\n    pg.get_by_test_id(\"cases-sort\").select_option(\"attention\"); pg.wait_for_timeout(300)\n    pg.screenshot(path=OUT+\"p1-overview-attention.png\")\n    print(\"options:\", pg.get_by_test_id(\"cases-sort\").evaluate(\"e=>Array.from(e.options).map(o=>o.value+'='+o.text)\"))\n    for f in pg.locator('[data-testid^=cases-filter-]').all():\n        f.click(); pg.wait_for_timeout(250)\n        print(\"FILTER\", f.inner_text(), \"->\", [r.get_by_test_id(\"cases-title\").inner_text() for r in pg.locator('[data-testid=cases-row]').all()])\n    # any green chip?\n    print(\"green/ready class elems:\", pg.evaluate(\"()=>Array.from(document.querySelectorAll('[class*=ready],[class*=chip--ok],[class*=green]')).map(e=>e.className+':'+e.innerText.slice(0,40))\"))\n    print(\"Untitled in page:\", \"Untitled\" in pg.inner_text(\"body\"))\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p1_overview.py > artifacts/review-evidence/T-149-paralegal-r2/p1.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p1.out.txt"
}
````

### User / tool · 2026-11-02T15:38:13.400Z

**tool result**
````
inputs on home: ['cases-search:Title', 'input-title:Client or matter, for example Rivera kne', 'input-text:=== Record 1 ===\nDate: 2026-01-09\nSource', 'file-input:']
filter chips: ['All cases (6)', 'Needs attention (6)', 'Ready to send (0)']
=== sort attention
ROW>> Austin EMS run report, Jan 9, 2026 | Last activity Nov 2, 2026, 9:37 AM · 9 records | 0 of 23 decided | Entries | 0 of 9 | Flags | 0 of 10 | Amounts | 0 of 4 | Analysis done | 3 need review | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Okafor LOP | Last activity Nov 2, 2026, 9:37 AM · 7 records | 0 of 19 decided | Entries | 0 of 7 | Flags | 0 of 5 | Amounts | 0 of 7 | Analysis done | 9 need review | 1 could not be verified | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Sablewood Market first-aid log, Mar 9, 2026 | Last activity Nov 2, 2026, 9:37 AM · 7 records | 0 of 18 decided | Entries | 0 of 7 | Flags | 0 of 8 | Amounts | 0 of 3 | Analysis done | 6 need review | 1 could not be verified | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Delgado v. Hartwell (truck) | Last activity Nov 2, 2026, 9:37 AM · 7 records | 0 of 14 decided | Entries | 0 of 7 | Flags | 0 of 4 | Amounts | 0 of 3 | Analysis done | 4 need review | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Dunmarrow Fire-Rescue run report, Feb 14, 2026 | Last activity Nov 2, 2026, 9:37 AM · 6 records | 0 of 9 decided | Entries | 0 of 5 | Flags | 0 of 2 | Amounts | 0 of 2 | Analysis done | 2 need review | 1 could not be verified | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Quillmere Regional ED, Mar 3, 2026 | Last activity Nov 2, 2026, 9:37 AM · 7 records | Entries | Not started | Flags | Not started | Amounts | Not started | Not analyzed yet | Not analyzed: open the case and press Analyze.
=== sort recent
ROW>> Quillmere Regional ED, Mar 3, 2026 | Last activity Nov 2, 2026, 9:37 AM · 7 records | Entries | Not started | Flags | Not started | Amounts | Not started | Not analyzed yet | Not analyzed: open the case and press Analyze.
ROW>> Okafor LOP | Last activity Nov 2, 2026, 9:37 AM · 7 records | 0 of 19 decided | Entries | 0 of 7 | Flags | 0 of 5 | Amounts | 0 of 7 | Analysis done | 9 need review | 1 could not be verified | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Delgado v. Hartwell (truck) | Last activity Nov 2, 2026, 9:37 AM · 7 records | 0 of 14 decided | Entries | 0 of 7 | Flags | 0 of 4 | Amounts | 0 of 3 | Analysis done | 4 need review | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Sablewood Market first-aid log, Mar 9, 2026 | Last activity Nov 2, 2026, 9:37 AM · 7 records | 0 of 18 decided | Entries | 0 of 7 | Flags | 0 of 8 | Amounts | 0 of 3 | Analysis done | 6 need review | 1 could not be verified | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Dunmarrow Fire-Rescue run report, Feb 14, 2026 | Last activity Nov 2, 2026, 9:37 AM · 6 records | 0 of 9 decided | Entries | 0 of 5 | Flags | 0 of 2 | Amounts | 0 of 2 | Analysis done | 2 need review | 1 could not be verified | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Austin EMS run report, Jan 9, 2026 | Last activity Nov 2, 2026, 9:37 AM · 9 records | 0 of 23 decided | Entries | 0 of 9 | Flags | 0 of 10 | Amounts | 0 of 4 | Analysis done | 3 need review | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
options: ['recent=Latest activity', 'attention=Needs attention first', 'least_done=Least decided first', 'title=Title A to Z']
FILTER All cases (6) -> ['Austin EMS run report, Jan 9, 2026', 'Okafor LOP', 'Sablewood Market first-aid log, Mar 9, 2026', 'Delgado v. Hartwell (truck)', 'Dunmarrow Fire-Rescue run report, Feb 14, 2026', 'Quillmere Regional ED, Mar 3, 2026']
FILTER Needs attention (6) -> ['Austin EMS run report, Jan 9, 2026', 'Okafor LOP', 'Sablewood Market first-aid log, Mar 9, 2026', 'Delgado v. Hartwell (truck)', 'Dunmarrow Fire-Rescue run report, Feb 14, 2026', 'Quillmere Regional ED, Mar 3, 2026']
FILTER Ready to send (0) -> []
green/ready class elems: []
Untitled in page: False
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:38:23.963Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/p1-overview-attention.png"
}
````

### User / tool · 2026-11-02T15:38:23.982Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:38:31.601Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p2_detail.py <<'EOF'\nimport json\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\"))\ndef focus_info(pg):\n    return pg.evaluate(\"()=>{const a=document.activeElement;if(!a)return null;const r=a.closest('[data-item-id],[data-testid]');return {tag:a.tagName,testid:a.getAttribute('data-testid'),id:a.id,item:(a.closest('[data-item-id]')||{}).dataset?(a.closest('[data-item-id]').dataset.itemId):null,text:(a.innerText||'').slice(0,160)}}\")\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(1000)\n    for key in [\"sample\", \"lib02\", \"lib01\", \"lib09\"]:\n        pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n        pg.get_by_test_id(\"case-\"+T[key]).click(); pg.wait_for_timeout(1500)\n        print(\"=====\", key, \"header name:\", pg.get_by_test_id(\"case-name\").inner_text())\n        ov = pg.get_by_test_id(\"case-overview\")\n        print(\"OVERVIEW BLOCK:\\n\", ov.inner_text())\n        print(\"do-first count:\", pg.locator('[data-testid=do-first]').count(), \"| texts:\", [x.inner_text() for x in pg.locator('[data-testid=do-first]').all()])\n        print(\"Start review / Case checks / What you need to do present:\", pg.get_by_text(\"Start review\").count(), pg.get_by_text(\"Case checks\").count(), pg.get_by_text(\"What you need to do\").count(), pg.get_by_text(\"Open decisions\").count())\n        pg.screenshot(path=OUT+f\"p2-detail-{key}.png\")\n        btn = pg.locator('[data-testid=btn-do-first]')\n        if btn.count():\n            print(\"button label:\", btn.first.inner_text())\n            btn.first.click(); pg.wait_for_timeout(600)\n            print(\"FOCUS after Go to it:\", json.dumps(focus_info(pg)))\n            pg.screenshot(path=OUT+f\"p2-detail-{key}-after-go.png\")\n        pg.get_by_test_id(\"btn-all-cases\").click(); pg.wait_for_timeout(500)\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p2_detail.py > artifacts/review-evidence/T-149-paralegal-r2/p2.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p2.out.txt"
}
````

### User / tool · 2026-11-02T15:39:04.018Z

**tool result**
````
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/p2_detail.py", line 12, in <module>
    pg.get_by_test_id("case-"+T[key]).click(); pg.wait_for_timeout(1500)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 11021, in click
    self._sync(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py", line 174, in click
    return await self._frame._click(self._selector, strict=True, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py", line 598, in _click
    await self._channel.send("click", self._timeout, locals_to_params(locals()))
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 78, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 636, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for get_by_test_id("case-Rz5jicMgA7vctUDY_rV9UQ")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:39:07.188Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r2-802d5fd; grep -n \"cases-open\\|cases-title\\|cases-row\" $R/app/frontend/overview.js | head"
}
````

### User / tool · 2026-11-02T15:39:07.280Z

**tool result**
````
103:    const a = el("a", { class: "cv-open", href: "#/case/" + encodeURIComponent(s.token), "data-testid": "cases-open", onclick: (ev) => {
107:    return el("li", { class: "cv-row", "data-testid": "cases-row", "data-token": s.token, onclick: (ev) => { if (!ev.target.closest("a, button, select, input, summary")) openCase(s.token, true); } },
109:        el("h3", { class: "cv-title", "data-testid": "cases-title" }, a),
131:    openErrEl = el("p", { class: "cv-msg rv-error", role: "alert", "data-testid": "cases-open-error" });
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:39:09.032Z

**tool call — Bash**
````
{
 "command": "sed -i.bak 's/pg.get_by_test_id(\"case-\"+T\\[key\\]).click()/pg.locator(f\"[data-testid=cases-row][data-token=\\\\\"{T[key]}\\\\\"] [data-testid=cases-open]\").click()/' artifacts/review-evidence/T-149-paralegal-r2/p2_detail.py 2>&1 | head -2; grep -n \"cases-open\" artifacts/review-evidence/T-149-paralegal-r2/p2_detail.py"
}
````

### User / tool · 2026-11-02T15:39:09.138Z

**tool result**
````
12:        pg.locator(f"[data-testid=cases-row][data-token=\"{T[key]}\"] [data-testid=cases-open]").click(); pg.wait_for_timeout(1500)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:39:11.025Z

**tool call — Bash**
````
{
 "command": "rm -f artifacts/review-evidence/T-149-paralegal-r2/p2_detail.py.bak; .venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p2_detail.py > artifacts/review-evidence/T-149-paralegal-r2/p2.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p2.out.txt"
}
````

### User / tool · 2026-11-02T15:39:55.987Z

**tool result**
````
===== sample header name: Austin EMS run report, Jan 9, 2026
OVERVIEW BLOCK:
 Case overview
Entries
0 of 9
Flags
0 of 10
Amounts
0 of 4

Do this first: This figure is a rate, not a charge, so it is not added to the total.

Go to it
3 need review
Export blocked (1)
Nothing is accepted or edited yet, so the letter would be empty.
Open decisions
Start review
9 entries to decide
10 flags to review
2 charges to check
2 unclear amounts (not totaled)
Case checks
7/10 checks passed
3 need you
Export blocked by 1
Show
How the AI was checked
checked 19, all agreed with the draft
Show
do-first count: 1 | texts: ['Do this first: This figure is a rate, not a charge, so it is not added to the total.\n\nGo to it']
Start review / Case checks / What you need to do present: 1 1 4 1
button label: Go to it
FOCUS after Go to it: {"tag": "TR", "testid": "amount-$185", "id": "", "item": "a2", "text": "$185.00\nRate\n\t\nCervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.\nOpen record 4\nWhy this status\n\t\nNeeds review\nNot co"}
===== lib02 header name: Sablewood Market first-aid log, Mar 9, 2026
OVERVIEW BLOCK:
 Case overview
Entries
0 of 7
Flags
0 of 8
Amounts
0 of 3

Do this first: The AI found this flag but the phrase list did not; check that it applies.

Go to it
6 need review
1 could not be verified
Export blocked (1)
Nothing is accepted or edited yet, so the letter would be empty.
Open decisions
Start review
7 entries to decide
8 flags to review
2 charges to check
1 unclear amount (not totaled)
Case checks
5/10 checks passed
5 need you
Export blocked by 1
Show
How the AI was checked
16 checked, 16 agreed with the draft, 1 not checked
Show
do-first count: 1 | texts: ['Do this first: The AI found this flag but the phrase list did not; check that it applies.\n\nGo to it']
Start review / Case checks / What you need to do present: 1 1 8 1
button label: Go to it
FOCUS after Go to it: {"tag": "ARTICLE", "testid": "flag-f_r2_1", "id": "", "item": "f_r2_1", "text": "Mention of prior surgery or repair\nNeeds review\n\nTamsin Valley Urgent Care (March 9, 2026) mentions prior surgery or repair: \u201cX-ray right knee: no acute fractur"}
===== lib01 header name: Dunmarrow Fire-Rescue run report, Feb 14, 2026
OVERVIEW BLOCK:
 Case overview
Entries
0 of 5
Flags
0 of 2
Amounts
0 of 2

Do this first: The AI found this flag but the phrase list did not; check that it applies.

Go to it
2 need review
1 could not be verified
Export blocked (1)
Nothing is accepted or edited yet, so the letter would be empty.
Open decisions
Start review
5 entries to decide
2 flags to review
1 charge to check
1 unclear amount (not totaled)
Case checks
6/10 checks passed
4 need you
Export blocked by 1
Show
How the AI was checked
checked 8, all agreed with the draft
Show
do-first count: 1 | texts: ['Do this first: The AI found this flag but the phrase list did not; check that it applies.\n\nGo to it']
Start review / Case checks / What you need to do present: 1 1 5 1
button label: Go to it
FOCUS after Go to it: {"tag": "ARTICLE", "testid": "flag-f_r3_1", "id": "", "item": "f_r3_1", "text": "New-onset wording\nNeeds review\n\nNew-onset wording in Dr. Imelda Quarrington, primary care (March 30, 2026): \u201cNeck pain 5/10 with new left arm tingling.\u201d\n\nNeeds "}
===== lib09 header name: Quillmere Regional ED, Mar 3, 2026
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/p2_detail.py", line 15, in <module>
    print("OVERVIEW BLOCK:\n", ov.inner_text())
                               ^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 12419, in inner_text
    self._sync(self._impl_obj.inner_text(timeout=to_milliseconds(timeout)))
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py", line 514, in inner_text
    return await self._frame.inner_text(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py", line 748, in inner_text
    return await self._channel.send(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 78, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 636, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.TimeoutError: Locator.inner_text: Timeout 30000ms exceeded.
Call log:
  - waiting for get_by_test_id("case-overview")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:40:08.174Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p3_targets.py <<'EOF'\nimport json\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\"))\nFI = \"()=>{const a=document.activeElement;const it=a&&a.closest('[data-item-id]');return {tag:a&&a.tagName,testid:a&&a.getAttribute('data-testid'),item:it?it.dataset.itemId:null,text:((a&&a.innerText)||'').slice(0,120)}}\"\ndef open_case(pg, key):\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f\"[data-testid=cases-row][data-token=\\\"{T[key]}\\\"] [data-testid=cases-open]\").click(); pg.wait_for_timeout(1500)\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    for key in [\"sample\", \"lib02\"]:\n        open_case(pg, key)\n        print(\"=====\", key)\n        print(\"elements with 'What you need to do':\", pg.evaluate(\"()=>Array.from(document.querySelectorAll('*')).filter(e=>e.children.length<4&&/What you need to do/.test(e.textContent||'')&&(e.innerText||'').length<400).map(e=>(e.getAttribute('data-testid')||e.tagName)+': '+e.innerText.replace(/\\\\n/g,' / ').slice(0,260))\"))\n        print(\"case-next-action els:\", [x.inner_text().replace(\"\\n\",\" / \")[:300] for x in pg.locator('[data-testid=case-next-action]').all()])\n        sr = pg.get_by_role(\"button\", name=\"Start review\")\n        print(\"Start review count\", sr.count())\n        if sr.count():\n            sr.first.click(); pg.wait_for_timeout(500); print(\"Start review ->\", json.dumps(pg.evaluate(FI)))\n        pg.get_by_role(\"button\", name=\"Go to it\").first.click(); pg.wait_for_timeout(500); print(\"Go to it ->\", json.dumps(pg.evaluate(FI)))\n    open_case(pg, \"lib09\")\n    print(\"===== lib09 (never analyzed) body top:\", pg.inner_text(\"main\")[:700] if pg.locator(\"main\").count() else pg.inner_text(\"body\")[:700])\n    pg.screenshot(path=OUT+\"p3-lib09-detail.png\")\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p3_targets.py > artifacts/review-evidence/T-149-paralegal-r2/p3.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p3.out.txt"
}
````

### User / tool · 2026-11-02T15:40:17.994Z

**tool result**
````
===== sample
elements with 'What you need to do': ['DIV: Open decisions / Start review / 9 entries to decide / 10 flags to review / 2 charges to check / 2 unclear amounts (not totaled) / Case checks / 7/10 checks passed / 3 need you / Export blocked by 1 / Show / How the AI was checked / checked 19, all agreed with ', 'checks-card: Case checks / 7/10 checks passed / 3 need you / Export blocked by 1 / Show / How the AI was checked / checked 19, all agreed with the draft / Show', 'case-stepper: Case checks / 7/10 checks passed / 3 need you / Export blocked by 1 / Show', 'DETAILS: Case checks / 7/10 checks passed / 3 need you / Export blocked by 1 / Show', 'DIV: ', 'case-step: ', 'step-action: ', 'P: ', 'STRONG: ', 'case-step: ', 'step-action: ', 'P: ', 'STRONG: ', 'case-step: ', 'step-action: ', 'P: ', 'STRONG: ', 'case-next-action: What you need to do: Decide the 2 detected charges: accept the ones that are billed charges, dismiss the rest. The total counts accepted charges only.Show this step', 'P: What you need to do: Decide the 2 detected charges: accept the ones that are billed charges, dismiss the rest. The total counts accepted charges only.', 'STRONG: What you need to do: ']
case-next-action els: ['What you need to do: Decide the 2 detected charges: accept the ones that are billed charges, dismiss the rest. The total counts accepted charges only.Show this step']
Start review count 1
Start review -> {"tag": "ARTICLE", "testid": "flag-f_r7_1", "item": "f_r7_1", "text": "Accident date source\nNeeds review\n\nAccident date as stated in Hill Country Pain Management, new patient (May 18, 2026): "}
Go to it -> {"tag": "TR", "testid": "amount-$185", "item": "a2", "text": "$185.00\nRate\n\t\nCervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.\nOpen record"}
===== lib02
elements with 'What you need to do': ['DIV: Open decisions / Start review / 7 entries to decide / 8 flags to review / 2 charges to check / 1 unclear amount (not totaled) / Case checks / 5/10 checks passed / 5 need you / Export blocked by 1 / Show / How the AI was checked / 16 checked, 16 agreed with the', 'checks-card: Case checks / 5/10 checks passed / 5 need you / Export blocked by 1 / Show / How the AI was checked / 16 checked, 16 agreed with the draft, 1 not checked / Show', 'case-stepper: Case checks / 5/10 checks passed / 5 need you / Export blocked by 1 / Show', 'DETAILS: Case checks / 5/10 checks passed / 5 need you / Export blocked by 1 / Show', 'DIV: ', 'case-step: ', 'step-action: ', 'P: ', 'STRONG: ', 'case-step: ', 'P: ', 'STRONG: ', 'case-step: ', 'step-action: ', 'P: ', 'STRONG: ', 'case-step: ', 'step-action: ', 'P: ', 'STRONG: ', 'case-step: ', 'step-action: ', 'P: ', 'STRONG: ', 'case-next-action: What you need to do: This item cannot be used. Dismiss it, or write the entry by hand from the record.Show this step', 'P: What you need to do: This item cannot be used. Dismiss it, or write the entry by hand from the record.', 'STRONG: What you need to do: ', 'judge-panel: How the AI was checked / 16 checked, 16 agreed with the draft, 1 not checked / Show', 'judge-unresolved-list: ', 'judge-rerun-group: ', 'P: ', 'STRONG: ', 'UL: ', 'P: ', 'STRONG: ']
case-next-action els: ['What you need to do: This item cannot be used. Dismiss it, or write the entry by hand from the record.Show this step']
Start review count 1
Start review -> {"tag": "ARTICLE", "testid": "entry-4", "item": "e4", "text": "March 30, 2026\nTamsin Imaging, right knee MRI\nRec 4\n\nThe summary has a number, date, dollar figure or left/right/no/not/"}
Go to it -> {"tag": "ARTICLE", "testid": "flag-f_r2_1", "item": "f_r2_1", "text": "Mention of prior surgery or repair\nNeeds review\n\nTamsin Valley Urgent Care (March 9, 2026) mentions prior surgery or rep"}
===== lib09 (never analyzed) body top: Records

7 records found

Read by code only. No model has been called yet.

Record 1: Quillmere Regional ED — March 3, 2026
Record 2: Consultorio Médico Aguaclara, nota de consulta — April 14, 2026
Record 3: Dr. Lucan Ostrowe, orthopedics, new patient — April 21, 2026
Record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR) — date to confirm
Record 5: Cinder Valley Imaging, right shoulder MRI — May 5, 2026
Record 6: Dr. Lucan Ostrowe, orthopedics, follow-up — May 12, 2026
Record 7: Consultorio Médico Aguaclara, estado de cuenta (billing statement) — May 20, 2026
Analyze
Start over
Add a synthetic case
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:40:20.960Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/p2-detail-sample.png"
}
````

### User / tool · 2026-11-02T15:40:20.969Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:40:32.826Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p4_shortcuts.py <<'EOF'\nimport json\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\"))\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    # overview keys: j/k then Enter\n    pg.keyboard.press(\"j\"); pg.wait_for_timeout(200)\n    print(\"after j focus:\", pg.evaluate(\"()=>{const a=document.activeElement;return a.tagName+' '+a.textContent.slice(0,50)}\"))\n    pg.keyboard.press(\"j\"); pg.wait_for_timeout(200)\n    print(\"after j j focus:\", pg.evaluate(\"()=>{const a=document.activeElement;return a.tagName+' '+a.textContent.slice(0,50)}\"))\n    pg.keyboard.press(\"k\"); pg.wait_for_timeout(200)\n    print(\"after k focus:\", pg.evaluate(\"()=>{const a=document.activeElement;return a.tagName+' '+a.textContent.slice(0,50)}\"))\n    pg.keyboard.press(\"Enter\"); pg.wait_for_timeout(1500)\n    print(\"opened:\", pg.get_by_test_id(\"case-name\").inner_text(), \"| focus:\", pg.evaluate(\"()=>document.activeElement.getAttribute('data-testid')+' '+document.activeElement.tagName\"))\n    pg.get_by_role(\"button\", name=\"Shortcuts\").click(); pg.wait_for_timeout(400)\n    print(pg.inner_text(\"body\")[:1800] if False else [x.inner_text() for x in pg.locator(\"[role=dialog], dialog, [data-testid*=shortcut]\").all()])\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p4_shortcuts.py > artifacts/review-evidence/T-149-paralegal-r2/p4.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p4.out.txt"
}
````

### User / tool · 2026-11-02T15:41:06.323Z

**tool result**
````
after j focus: A Quillmere Regional ED, Mar 3, 2026
after j j focus: A Okafor LOP
after k focus: A Quillmere Regional ED, Mar 3, 2026
opened: Quillmere Regional ED, Mar 3, 2026 | focus: null BODY
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/p4_shortcuts.py", line 17, in <module>
    pg.get_by_role("button", name="Shortcuts").click(); pg.wait_for_timeout(400)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 11021, in click
    self._sync(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py", line 174, in click
    return await self._frame._click(self._selector, strict=True, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py", line 598, in _click
    await self._channel.send("click", self._timeout, locals_to_params(locals()))
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 78, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 636, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for get_by_role("button", name="Shortcuts")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:41:12.935Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r2-802d5fd; grep -n \"Next item\\|next item\\|Accept\\b.*key\\|<kbd\\|kbd\" $R/app/frontend/index.html $R/app/frontend/keys.js 2>/dev/null | head -30; ls $R/app/frontend"
}
````

### User / tool · 2026-11-02T15:41:13.036Z

**tool result**
````
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
index.html
input.js
judges.js
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
narrative.js
overview.css
overview.js
review.css
review.js
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:41:16.923Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r2-802d5fd; grep -n \"key ===\\|ev.key\\|e.key\" $R/app/frontend/review.js | head -30"
}
````

### User / tool · 2026-11-02T15:41:17.081Z

**tool result**
````
356:    // a dismissed item keeps only its state word, Undo and Audit: no Accept, Keep in notes or Edit (the paralegal's M1: one key must not reverse a dismissal)
410:        if (ev.key === "Escape") { ev.stopPropagation(); toggleEdit(false); }
411:        else if (ev.key === "Enter" && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); form.requestSubmit(); }
449:  // ---- keyboard flow (R-RV-4, WCAG 2.1.4 / T-060 blocker). Single-key shortcuts act ONLY while focus is on an item row or on something inside one.
457:      if (ev.key.length === 1 && "jkadero".includes(ev.key.toLowerCase()) && !ev.shiftKey && ZL.state.get().case) RV.say("A window is open. Press Escape to close it first, then use the key again.");
463:    const key = ev.key.length === 1 ? ev.key.toLowerCase() : ev.key, id = row.getAttribute("data-item-id");
464:    if (ev.key === "?") { ev.preventDefault(); if (RV.openShortcuts) RV.openShortcuts(); return; }
466:    if (key === "j" || key === "k") {
467:      const items = RV.domItems(), at = items.indexOf(row), n = items[at + (key === "j" ? 1 : -1)];
469:      if (n) focusNode(n); else RV.say(key === "j" ? "That is the last item." : "That is the first item.");
472:    if (ev.key.length !== 1 || !"aedro".includes(key)) return;
475:    if ((key === "a" || key === "d" || key === "e") && f.item.review_status === "dismissed") {   // T-060 r5 (paralegal M1): one key never undoes a dismissal; only Undo (or r) does
479:    if (key === "a" && /^(accepted|edited)$/.test(f.item.review_status) && !ZL.editToCheck(f.item)) {   // as the Accept button: a decided item is not decided twice (T-154: a confirmed flagged charge must not reopen "not counted" or write a second accept)
483:    if (key === "a" && ZL.editToCheck(f.item)) { askCompare(id); return; }   // T-136 (paralegal F1): one key press never records "I compared it with the quote"; the button (click, or Enter on it) does
484:    if (key === "a") RV.act(id, { action: "accept" }, { advance: true });
485:    else if (key === "d") RV.act(id, { action: "dismiss" }, { advance: true });
486:    else if (key === "r") { if (f.item.review_status !== "pending") RV.act(id, { action: "reset" }, { focus: "reset" }); }
487:    else if (key === "o") RV.openSource(f.item, f.kind);
488:    else if (key === "e") { if (ui[id] && ui[id].openEdit) ui[id].openEdit(); }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:41:29.975Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p5_work_A.py <<'EOF'\nimport json, urllib.request\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"lib03\"]\ndef get(p): return json.loads(urllib.request.urlopen(\"http://127.0.0.1:7943\"+p).read())\ndef row(pg):\n    pg.get_by_test_id(\"btn-all-cases\").click(); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(900)\n    r = pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"]')\n    print(\"   ROW>>\", \" | \".join(t.strip() for t in r.inner_text().split(\"\\n\") if t.strip()))\n    print(\"   filters:\", [x.inner_text() for x in pg.locator('[data-testid^=cases-filter-]').all()])\n    r.locator(\"[data-testid=cases-open]\").click(); pg.wait_for_timeout(1300)\ndef chips(pg):\n    ov = pg.get_by_test_id(\"case-overview\")\n    print(\"   BLOCK>>\", \" | \".join(t.strip() for t in ov.inner_text().split(\"\\n\") if t.strip()))\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1500)\n    print(\"STEP0 untouched\"); chips(pg)\n    # Rename in detail\n    pg.get_by_test_id(\"btn-rename-case\").click(); pg.get_by_test_id(\"case-rename-input\").fill(\"Delgado v. Hartwell - truck rear-end\"); pg.get_by_test_id(\"case-rename-input\").press(\"Enter\"); pg.wait_for_timeout(900)\n    print(\"RENAMED header:\", pg.get_by_test_id(\"case-name\").inner_text())\n    # Do this first -> keyboard: accept one thing\n    print(\"do-first:\", pg.locator(\"[data-testid=do-first]\").inner_text().replace(\"\\n\", \" \"))\n    pg.get_by_test_id(\"btn-do-first\").click(); pg.wait_for_timeout(500)\n    print(\"focus:\", pg.evaluate(\"()=>{const a=document.activeElement;const it=a.closest('[data-item-id]');return it?it.dataset.itemId+' '+it.innerText.slice(0,80).replace(/\\\\n/g,' '):a.tagName}\"))\n    pg.keyboard.press(\"a\"); pg.wait_for_timeout(700)\n    print(\"STEP1 pressed a on the do-first item\"); chips(pg)\n    print(\"   API gate:\", json.dumps({k: get(f\"/api/cases/{TOK}\").get(k) for k in (\"export_ready\",)}))\n    row(pg)\n    pg.screenshot(path=OUT+\"p5-A-after-one.png\")\n    print(\"STEP2 accept all verified entries\")\n    pg.get_by_role(\"button\", name=\"Accept all verified\").click(); pg.wait_for_timeout(1200)\n    chips(pg); row(pg)\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p5_work_A.py > artifacts/review-evidence/T-149-paralegal-r2/p5.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p5.out.txt | cut -c1-700"
}
````

### User / tool · 2026-11-02T15:41:41.167Z

**tool result**
````
STEP0 untouched
   BLOCK>> Case overview | Entries | 0 of 7 | Flags | 0 of 4 | Amounts | 0 of 3 | Do this first: This figure is a rate, not a charge, so it is not added to the total. | Go to it | 4 need review | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty. | Open decisions | Start review | 7 entries to decide | 4 flags to review | 2 charges to check | 1 unclear amount (not totaled) | Case checks | 6/10 checks passed | 4 need you | Export blocked by 1 | Show | How the AI was checked | 12 checked, 10 agreed with the draft, 2 questioned | Show
RENAMED header: Delgado v. Hartwell - truck rear-end
do-first: Do this first: This figure is a rate, not a charge, so it is not added to the total.  Go to it
focus: a2 $120.00 Rate 	 Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks. 
STEP1 pressed a on the do-first item
   BLOCK>> Case overview | Entries | 0 of 7 | Flags | 0 of 4 | Amounts | 1 of 3 | 3 need review | Can export — 13 not reviewed (they stay out of the letter) | Open decisions | Start review | 7 entries to decide | 4 flags to review | 2 charges to check | Case checks | 7/10 checks passed | 3 need you | Ready to export, 13 not reviewed | Show | What you need to do: Review the 2 items the AI objected to. Compare each one with its quote, then accept, edit or dismiss it. | Show this step | How the AI was checked | 12 checked, 10 agreed with the draft, 2 questioned | Show
   API gate: {"export_ready": null}
   ROW>> Delgado v. Hartwell - truck rear-end | Last activity Nov 2, 2026, 9:41 AM · 7 records | 1 of 14 decided | Entries | 0 of 7 | Flags | 0 of 4 | Amounts | 1 of 3 | Analysis done | 4 need review | Can export — 13 not reviewed (they stay out of the letter)
   filters: ['All cases (6)', 'Needs attention (6)', 'Ready to send (0)']
STEP2 accept all verified entries
   BLOCK>> Case overview | Entries | 7 of 7 | Flags | 0 of 4 | Amounts | 1 of 3 | Do this first: A second AI check disagreed with the first result for this item. | Go to it | 3 need review | Can export — 6 not reviewed (they stay out of the letter) | Open decisions | Start review | 4 flags to review | 2 charges to check | Case checks | 7/10 checks passed | 3 need you | Ready to export, 6 not reviewed | Show | How the AI was checked | 12 checked, 10 agreed with the draft, 2 questioned | Show
   ROW>> Delgado v. Hartwell - truck rear-end | Last activity Nov 2, 2026, 9:41 AM · 7 records | 8 of 14 decided | Entries | 7 of 7 | Flags | 0 of 4 | Amounts | 1 of 3 | Analysis done | 4 need review | Can export — 6 not reviewed (they stay out of the letter)
   filters: ['All cases (6)', 'Needs attention (6)', 'Ready to send (0)']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:41:47.836Z

**tool call — Bash**
````
{
 "command": "curl -s http://127.0.0.1:7943/api/cases | .venv/bin/python -I -c \"\nimport json,sys\nfor c in json.load(sys.stdin)['cases']:\n    print(c['title'][:40], '|', json.dumps(c.get('next_action'))[:260], '| ready', c.get('export_ready'), '| pend', c['hitl']['pending'])\n\""
}
````

### User / tool · 2026-11-02T15:41:47.976Z

**tool result**
````
Quillmere Regional ED, Mar 3, 2026 | {"item_id": null, "kind": "run", "reason": "Run the case to draft the timeline. Nothing is waiting for you until then."} | ready False | pend 9
Okafor LOP | {"item_id": "f_r3_2", "kind": "flag", "reason": "The phrase list found this flag but the AI did not; check that it applies."} | ready False | pend 19
Delgado v. Hartwell - truck rear-end | {"item_id": "f_r7_1", "kind": "flag", "reason": "A second AI check disagreed with the first result for this item."} | ready True | pend 6
Sablewood Market first-aid log, Mar 9, 2 | {"item_id": "f_r2_1", "kind": "flag", "reason": "The AI found this flag but the phrase list did not; check that it applies."} | ready False | pend 18
Dunmarrow Fire-Rescue run report, Feb 14 | {"item_id": "f_r3_1", "kind": "flag", "reason": "The AI found this flag but the phrase list did not; check that it applies."} | ready False | pend 9
Austin EMS run report, Jan 9, 2026 | {"item_id": "a2", "kind": "amount", "reason": "This figure is a rate, not a charge, so it is not added to the total."} | ready False | pend 23
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:41:48.380Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/p5-A-after-one.png"
}
````

### User / tool · 2026-11-02T15:41:48.391Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:42:03.852Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p6_work_A2.py <<'EOF'\nimport json, urllib.request\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"lib03\"]\ndef get(p): return json.loads(urllib.request.urlopen(\"http://127.0.0.1:7943\"+p).read())\ndef summ():\n    c = [x for x in get(\"/api/cases\")[\"cases\"] if x[\"token\"] == TOK][0]\n    return c[\"hitl\"][\"pending\"], c[\"export_ready\"], (c.get(\"next_action\") or {}).get(\"item_id\")\ndef block(pg):\n    print(\"   BLOCK>>\", \" | \".join(t.strip() for t in pg.get_by_test_id(\"case-overview\").inner_text().split(\"\\n\") if t.strip())[:520])\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1500)\n    print(\"start:\", summ()); block(pg)\n    # edit record 3 summary (entry 3) with keyboard: focus row, press e\n    row3 = pg.locator('[data-testid=entry-3]'); row3.scroll_into_view_if_needed(); row3.focus(); pg.keyboard.press(\"e\"); pg.wait_for_timeout(400)\n    ta = row3.locator(\"textarea\"); print(\"edit textarea count\", ta.count(), \"| current:\", ta.first.input_value() if ta.count() else None)\n    ta.first.fill(\"Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks.\"); pg.keyboard.press(\"Control+Enter\"); pg.wait_for_timeout(900)\n    print(\"after edit(record 3) row text:\", row3.inner_text().replace(\"\\n\",\" / \")[:420])\n    print(\"after edit:\", summ())\n    # walk everything with the keyboard from do-first: first dismiss one flag with d, else a\n    n = 0; dismissed = None\n    while n < 40:\n        pend, ready, nxt = summ()\n        if pend == 0: break\n        btn = pg.locator(\"[data-testid=btn-do-first]\")\n        if not btn.count(): print(\"   no do-first button while pending\", pend, nxt); block(pg); break\n        line = pg.locator(\"[data-testid=do-first]\").inner_text().replace(\"\\n\", \" \")\n        btn.click(); pg.wait_for_timeout(350)\n        info = pg.evaluate(\"()=>{const a=document.activeElement;const it=a.closest('[data-item-id]');return it?it.dataset.itemId:a.tagName}\")\n        key = \"d\" if (info.startswith(\"f_\") and dismissed is None) else \"a\"\n        if key == \"d\": dismissed = info\n        pg.keyboard.press(key); pg.wait_for_timeout(700)\n        n += 1\n        print(f\"  step {n}: pending {pend} | do-first said: {line[:110]} | focused {info} | pressed {key} | now {summ()}\")\n        # if an edited-to-check compare prompt appears, show\n        dlg = pg.locator(\"[role=dialog]\")\n        if dlg.count(): print(\"   DIALOG:\", dlg.first.inner_text().replace(\"\\n\",\" / \")[:300]); pg.keyboard.press(\"Escape\"); break\n    print(\"final:\", summ()); block(pg)\n    pg.screenshot(path=OUT+\"p6-A-final.png\")\n    print(\"dismissed flag:\", dismissed)\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p6_work_A2.py > artifacts/review-evidence/T-149-paralegal-r2/p6.out.txt 2>&1; cut -c1-650 artifacts/review-evidence/T-149-paralegal-r2/p6.out.txt"
}
````

### User / tool · 2026-11-02T15:42:54.062Z

**tool result**
````
start: (6, True, 'f_r7_1')
   BLOCK>> Case overview | Entries | 7 of 7 | Flags | 0 of 4 | Amounts | 1 of 3 | Do this first: A second AI check disagreed with the first result for this item. | Go to it | 3 need review | Can export — 6 not reviewed (they stay out of the letter) | Open decisions | Start review | 4 flags to review | 2 charges to check | Case checks | 7/10 checks passed | 3 need you | Ready to export, 6 not reviewed | Show | How the AI was checked | 12 checked, 10 agreed with the draft, 2 questioned | Show
edit textarea count 1 | current: Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks.
after edit(record 3) row text: April 9, 2026 / Thimbleby Chiropractic, initial exam / Rec 3 /  / The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked. /  / Needs review / Edited /  / Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks. /  / Edited by you; the code checked your wording against the quote when you saved. Original: Cervical and lumbar spasm. Plan: 3 visits per
after edit: (6, True, 'e3')
  step 1: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 2: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 3: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 4: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 5: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 6: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 7: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 8: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 9: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 10: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 11: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 12: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 13: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 14: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 15: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 16: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 17: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 18: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 19: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 20: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 21: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 22: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 23: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 24: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 25: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 26: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 27: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 28: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 29: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 30: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 31: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 32: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 33: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 34: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 35: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 36: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 37: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 38: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 39: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
  step 40: pending 6 | do-first said: Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has no | focused e3 | pressed a | now (6, True, 'e3')
final: (6, True, 'e3')
   BLOCK>> Case overview | Entries | 6 of 7 | Flags | 0 of 4 | Amounts | 1 of 3 | Do this first: The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked. | Go to it | 4 need review | 1 edit to check | Can export — 6 not reviewed (they stay out of the letter) | 1 edit is still marked Needs review (the second check did not confirm it), so it is not in the letter and is not counted as accepted until you compare it with the quote and accept. | Open decisions | Start rev
dismissed flag: None
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:43:01.125Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p7_compare.py <<'EOF'\nimport json\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"lib03\"]\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1500)\n    pg.get_by_test_id(\"btn-do-first\").click(); pg.wait_for_timeout(400)\n    pg.keyboard.press(\"a\"); pg.wait_for_timeout(600)\n    r = pg.locator(\"[data-testid=entry-3]\")\n    print(\"ROW3 after a:\", r.inner_text().replace(\"\\n\", \" / \")[:900])\n    print(\"buttons in row3:\", [x.inner_text() for x in r.locator(\"button\").all()])\n    pg.screenshot(path=OUT+\"p7-compare-prompt.png\")\n    print(\"focus:\", pg.evaluate(\"()=>{const a=document.activeElement;return a.tagName+' '+(a.getAttribute('data-testid')||'')+' '+a.innerText.slice(0,80)}\"))\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p7_compare.py > artifacts/review-evidence/T-149-paralegal-r2/p7.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p7.out.txt | cut -c1-1200"
}
````

### User / tool · 2026-11-02T15:43:05.039Z

**tool result**
````
ROW3 after a: April 9, 2026 / Thimbleby Chiropractic, initial exam / Rec 3 /  / The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked. /  / Needs review / Edited /  / Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks. /  / Edited by you; the code checked your wording against the quote when you saved. Original: Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks. /  / Excerpt · Record 3 · Thimbleby Chiropractic, initial exam / Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks. / I compared it with the quote / Edit / Dismiss / Undo /  / Still marked Needs review. Compare your wording with the quote, then press the button to say you did. Until then it is not in the letter and counts as open. /  / Not recorded yet. Read the quote against your edit. Then click “I compared it with the quote”, or press Ente
buttons in row3: ['I compared it with the quote', 'Edit', 'Dismiss', 'Undo', 'Save', 'Cancel', 'Use these sentences', 'Cancel', 'Why this status', 'Open record', 'Audit', 'Change quote', 'More']
focus: BUTTON btn-accept I compared it with the quote
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:43:14.705Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p8_finish_A.py <<'EOF'\nimport json, urllib.request\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"lib03\"]\ndef get(p): return json.loads(urllib.request.urlopen(\"http://127.0.0.1:7943\"+p).read())\ndef summ():\n    c = [x for x in get(\"/api/cases\")[\"cases\"] if x[\"token\"] == TOK][0]\n    return c[\"hitl\"][\"pending\"], c[\"hitl\"][\"edits_to_check\"], c[\"export_ready\"], (c.get(\"next_action\") or {})\ndef block(pg):\n    print(\"   BLOCK>>\", \" | \".join(t.strip() for t in pg.get_by_test_id(\"case-overview\").inner_text().split(\"\\n\") if t.strip())[:600])\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1500)\n    n = 0; dismissed = None\n    while n < 40:\n        pend, etc, ready, na = summ()\n        if pend == 0 and etc == 0: break\n        btn = pg.locator(\"[data-testid=btn-do-first]\")\n        if not btn.count(): print(\"  no do-first button; pend\", pend, etc, na); block(pg); break\n        line = pg.locator(\"[data-testid=do-first]\").inner_text().replace(\"\\n\", \" \")[12:]\n        btn.click(); pg.wait_for_timeout(350)\n        info = pg.evaluate(\"()=>{const a=document.activeElement;const it=a.closest('[data-item-id]');return (it?it.dataset.itemId:a.tagName)+'/'+(a.getAttribute('data-testid')||'')}\")\n        iid = info.split(\"/\")[0]\n        if iid.startswith(\"f_\") and dismissed is None: key = \"d\"; dismissed = iid\n        else: key = \"a\"\n        pg.keyboard.press(key); pg.wait_for_timeout(600)\n        if pg.evaluate(\"()=>document.activeElement.getAttribute('data-testid')\") == \"btn-accept\" and iid.startswith(\"e\"):\n            pg.keyboard.press(\"Enter\"); pg.wait_for_timeout(600); key += \"+Enter(compared)\"\n        n += 1\n        print(f\"  step {n}: pend {pend} etc {etc} | server next {na.get('item_id')} | line: {line[:100]} | focus {info} | key {key} | now {summ()[:3]}\")\n    print(\"final:\", summ()[:3]); block(pg)\n    pg.screenshot(path=OUT+\"p8-A-final.png\")\n    print(\"dismissed flag:\", dismissed)\n    pg.get_by_test_id(\"btn-all-cases\").click(); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(900)\n    r = pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"]')\n    print(\"ROW>>\", \" | \".join(t.strip() for t in r.inner_text().split(\"\\n\") if t.strip()))\n    print(\"filters:\", [x.inner_text() for x in pg.locator('[data-testid^=cases-filter-]').all()])\n    pg.screenshot(path=OUT+\"p8-overview-after-A.png\")\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p8_finish_A.py > artifacts/review-evidence/T-149-paralegal-r2/p8.out.txt 2>&1; cut -c1-900 artifacts/review-evidence/T-149-paralegal-r2/p8.out.txt"
}
````

### User / tool · 2026-11-02T15:43:20.303Z

**tool result**
````
  step 1: pend 6 etc 1 | server next e3 | line: t: The second check failed (the AI check was asked and gave no usable answer), so this item has not  | focus e3/entry-3 | key a+Enter(compared) | now (6, 0, True)
  no do-first button; pend 6 0 {'item_id': 'f_r7_1', 'kind': 'flag', 'reason': 'A second AI check disagreed with the first result for this item.'}
   BLOCK>> Case overview | Entries | 7 of 7 | Flags | 0 of 4 | Amounts | 1 of 3 | 3 need review | Can export — 6 not reviewed (they stay out of the letter) | Open decisions | Start review | 4 flags to review | 2 charges to check | Case checks | 7/10 checks passed | 3 need you | Ready to export, 6 not reviewed | Show | What you need to do: Review the 2 items the AI objected to. Compare each one with its quote, then accept, edit or dismiss it. | Show this step | How the AI was checked | 11 checked, 9 agreed with the draft, 2 questioned | Show
final: (6, 0, True)
   BLOCK>> Case overview | Entries | 7 of 7 | Flags | 0 of 4 | Amounts | 1 of 3 | 3 need review | Can export — 6 not reviewed (they stay out of the letter) | Open decisions | Start review | 4 flags to review | 2 charges to check | Case checks | 7/10 checks passed | 3 need you | Ready to export, 6 not reviewed | Show | What you need to do: Review the 2 items the AI objected to. Compare each one with its quote, then accept, edit or dismiss it. | Show this step | How the AI was checked | 11 checked, 9 agreed with the draft, 2 questioned | Show
dismissed flag: None
ROW>> Delgado v. Hartwell - truck rear-end | Last activity Nov 2, 2026, 9:43 AM · 7 records | 8 of 14 decided | Entries | 7 of 7 | Flags | 0 of 4 | Amounts | 1 of 3 | Analysis done | 5 need review | Can export — 6 not reviewed (they stay out of the letter)
filters: ['All cases (6)', 'Needs attention (6)', 'Ready to send (0)']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:43:28.168Z

**tool call — Bash**
````
{
 "command": "TOK=$(.venv/bin/python -I -c \"import json;print(json.load(open('artifacts/review-evidence/T-149-paralegal-r2/tokens.json'))['lib03'])\"); curl -s http://127.0.0.1:7943/api/cases | .venv/bin/python -I -c \"\nimport json,sys\nfor c in json.load(sys.stdin)['cases']:\n    if c['token']=='$TOK': print(json.dumps({k:c[k] for k in ('title','export_ready','next_action','hitl','progress')},indent=0)[:1800])\n\"; cat > artifacts/review-evidence/T-149-paralegal-r2/p9_reload.py <<'EOF'\nimport json\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"lib03\"]\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1800)\n    print(\"BLOCK>>\", \" | \".join(t.strip() for t in pg.get_by_test_id(\"case-overview\").inner_text().split(\"\\n\") if t.strip())[:700])\n    print(\"header:\", pg.locator(\"header, .topbar\").first.inner_text().replace(\"\\n\",\" | \")[:200])\n    pg.screenshot(path=OUT+\"p9-A-reopened.png\")\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p9_reload.py > artifacts/review-evidence/T-149-paralegal-r2/p9.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p9.out.txt"
}
````

### User / tool · 2026-11-02T15:43:31.457Z

**tool result**
````
{
"title": "Delgado v. Hartwell - truck rear-end",
"export_ready": true,
"next_action": {
"item_id": "f_r7_1",
"kind": "flag",
"reason": "A second AI check disagreed with the first result for this item."
},
"hitl": {
"pending": 6,
"needs_review": 5,
"edits_to_check": 0,
"could_not_verify": 0,
"gate_blockers": [],
"gate_warnings": [
{
"reason_code": "ITEMS_NOT_REVIEWED",
"count": 6,
"why": "6 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them."
}
]
},
"progress": {
"entries": {
"decided": 7,
"total": 7
},
"flags": {
"decided": 0,
"total": 4
},
"amounts": {
"decided": 1,
"total": 3
}
}
}
BLOCK>> Case overview | Entries | 7 of 7 | Flags | 0 of 4 | Amounts | 1 of 3 | Do this first: A second AI check disagreed with the first result for this item. | Go to it | 3 need review | Can export — 6 not reviewed (they stay out of the letter) | Open decisions | Start review | 4 flags to review | 2 charges to check | Case checks | 7/10 checks passed | 3 need you | Ready to export, 6 not reviewed | Show | How the AI was checked | 11 checked, 9 agreed with the draft, 2 questioned | Show
header: All cases | Delgado v. Hartwell - truck rear-end | Rename | 8 of 14 decided · 3 items need review | cached demo (curated responses) | Shortcuts | Theme: auto | Export
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:43:45.563Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p10_stale.py <<'EOF'\nimport json\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"lib03\"]\ndef df(pg):\n    l = pg.locator(\"[data-testid=do-first]\")\n    return l.inner_text().replace(\"\\n\",\" \")[:120] if l.count() else \"(no do-first line)\"\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1800)\n    print(\"open:\", df(pg))\n    pg.get_by_test_id(\"btn-do-first\").click(); pg.wait_for_timeout(400)\n    print(\"focus:\", pg.evaluate(\"()=>{const it=document.activeElement.closest('[data-item-id]');return it&&it.dataset.itemId}\"))\n    pg.keyboard.press(\"d\"); pg.wait_for_timeout(600)   # dismiss this flag\n    for t in (600, 1500, 3500):\n        pg.wait_for_timeout(t); print(f\"after d +{t}ms: {df(pg)}\")\n    print(\"BLOCK>>\", \" | \".join(t.strip() for t in pg.get_by_test_id(\"case-overview\").inner_text().split(\"\\n\") if t.strip())[:600])\n    print(\"header:\", pg.locator(\"header, .topbar\").first.inner_text().replace(\"\\n\",\" | \")[:140])\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p10_stale.py > artifacts/review-evidence/T-149-paralegal-r2/p10.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p10.out.txt"
}
````

### User / tool · 2026-11-02T15:43:55.418Z

**tool result**
````
open: Do this first: A second AI check disagreed with the first result for this item.  Go to it
focus: f_r7_1
after d +600ms: Do this first: A second AI check disagreed with the first result for this item.  Go to it
after d +1500ms: Do this first: A second AI check disagreed with the first result for this item.  Go to it
after d +3500ms: Do this first: A second AI check disagreed with the first result for this item.  Go to it
BLOCK>> Case overview | Entries | 7 of 7 | Flags | 1 of 4 | Amounts | 1 of 3 | Do this first: A second AI check disagreed with the first result for this item. | Go to it | 2 need review | Can export — 5 not reviewed (they stay out of the letter) | Open decisions | Start review | 3 flags to review | 2 charges to check | Case checks | 7/10 checks passed | 3 need you | Ready to export, 5 not reviewed | Show | How the AI was checked | 11 checked, 9 agreed with the draft, 2 questioned | Show
header: All cases | Delgado v. Hartwell - truck rear-end | Rename | 9 of 14 decided · 2 items need review | cached demo (curated responses) | Shortc
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:44:02.421Z

**tool call — Bash**
````
{
 "command": "TOK=$(.venv/bin/python -I -c \"import json;print(json.load(open('artifacts/review-evidence/T-149-paralegal-r2/tokens.json'))['lib03'])\"); curl -s http://127.0.0.1:7943/api/cases | .venv/bin/python -I -c \"\nimport json,sys\nfor c in json.load(sys.stdin)['cases']:\n    if c['token']=='$TOK': print(json.dumps(c['next_action']), c['hitl']['pending'], c['hitl']['needs_review'])\n\"; cat > artifacts/review-evidence/T-149-paralegal-r2/p11_stale2.py <<'EOF'\nimport json\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"lib03\"]\nFI = \"()=>{const a=document.activeElement;const it=a&&a.closest('[data-item-id]');return {item:it?it.dataset.itemId:null,tag:a&&a.tagName}}\"\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1800)\n    print(\"fresh open, do-first:\", pg.locator(\"[data-testid=do-first]\").inner_text().replace(\"\\n\",\" \") if pg.locator(\"[data-testid=do-first]\").count() else \"(none)\")\n    pg.get_by_test_id(\"btn-do-first\").click(); pg.wait_for_timeout(500); print(\"Go to it ->\", pg.evaluate(FI))\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p11_stale2.py > artifacts/review-evidence/T-149-paralegal-r2/p11.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p11.out.txt"
}
````

### User / tool · 2026-11-02T15:44:06.169Z

**tool result**
````
{"item_id": "f_r7_2", "kind": "flag", "reason": "A second AI check disagreed with the first result for this item."} 5 5
fresh open, do-first: Do this first: A second AI check disagreed with the first result for this item.  Go to it
Go to it -> {'item': 'f_r7_2', 'tag': 'ARTICLE'}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:44:19.239Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p12_finish_A.py <<'EOF'\nimport json, urllib.request\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"lib03\"]\ndef get(p): return json.loads(urllib.request.urlopen(\"http://127.0.0.1:7943\"+p).read())\ndef summ():\n    c = [x for x in get(\"/api/cases\")[\"cases\"] if x[\"token\"] == TOK][0]\n    return c[\"hitl\"][\"pending\"], c[\"hitl\"][\"edits_to_check\"], c[\"hitl\"][\"needs_review\"], c[\"export_ready\"], (c.get(\"next_action\") or {}).get(\"item_id\")\ndef rowtxt(pg):\n    pg.get_by_test_id(\"btn-all-cases\").click(); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(900)\n    r = pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"]')\n    t = \" | \".join(x.strip() for x in r.inner_text().split(\"\\n\") if x.strip()); print(\"   ROW>>\", t)\n    r.locator(\"[data-testid=cases-open]\").click(); pg.wait_for_timeout(1600)\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1600)\n    header = lambda: pg.locator(\"header, .topbar\").first.inner_text().replace(\"\\n\",\" | \")[:90]\n    print(\"start\", summ(), \"| detail header:\", header()); rowtxt(pg)\n    n = 0\n    while n < 30:\n        s = summ()\n        if s[0] == 0 and s[1] == 0: break\n        btn = pg.locator(\"[data-testid=btn-do-first]\")\n        if not btn.count():\n            pg.wait_for_timeout(1500)\n            if not btn.count(): print(\"  !! no do-first button with pending\", s, \"| block:\", pg.get_by_test_id(\"case-overview\").inner_text().replace(\"\\n\",\" | \")[:300]); break\n        btn.click(); pg.wait_for_timeout(350)\n        iid = pg.evaluate(\"()=>{const it=document.activeElement.closest('[data-item-id]');return it&&it.dataset.itemId}\")\n        pg.keyboard.press(\"a\"); pg.wait_for_timeout(700)\n        if pg.evaluate(\"()=>document.activeElement.getAttribute('data-testid')\") == \"btn-accept\" and (iid or \"\").startswith(\"e\"):\n            pg.keyboard.press(\"Enter\"); pg.wait_for_timeout(700)\n        n += 1; pg.wait_for_timeout(500); print(f\"  step {n}: item {iid} -> server {summ()} | detail header: {header()}\")\n    print(\"final server:\", summ()); print(\"final header:\", header())\n    print(\"BLOCK>>\", pg.get_by_test_id(\"case-overview\").inner_text().replace(\"\\n\",\" | \")[:600])\n    pg.screenshot(path=OUT+\"p12-A-all-decided.png\")\n    rowtxt(pg)\n    print(\"filters:\", [x.inner_text() for x in pg.locator('[data-testid^=cases-filter-]').all()])\n    pg.screenshot(path=OUT+\"p12-overview-A-all-decided.png\")\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p12_finish_A.py > artifacts/review-evidence/T-149-paralegal-r2/p12.out.txt 2>&1; cut -c1-700 artifacts/review-evidence/T-149-paralegal-r2/p12.out.txt"
}
````

### User / tool · 2026-11-02T15:44:32.449Z

**tool result**
````
start (5, 0, 5, True, 'f_r7_2') | detail header: All cases | Delgado v. Hartwell - truck rear-end | Rename | 9 of 14 decided · 2 items need
   ROW>> Delgado v. Hartwell - truck rear-end | Last activity Nov 2, 2026, 9:43 AM · 7 records | 9 of 14 decided | Entries | 7 of 7 | Flags | 1 of 4 | Amounts | 1 of 3 | Analysis done | 5 need review | Can export — 5 not reviewed (they stay out of the letter)
  step 1: item f_r7_2 -> server (4, 0, 5, True, 'f_r7_3') | detail header: All cases | Delgado v. Hartwell - truck rear-end | Rename | 10 of 14 decided · 1 item need
  step 2: item f_r7_3 -> server (3, 0, 5, True, None) | detail header: All cases | Delgado v. Hartwell - truck rear-end | Rename | 11 of 14 decided | cached demo
  !! no do-first button with pending (3, 0, 5, True, None) | block: Case overview | Entries | 7 of 7 | Flags | 3 of 4 | Amounts | 1 of 3 | Can export — 3 not reviewed (they stay out of the letter) | Open decisions | Start review | 1 flag to review | 2 charges to check | Case checks | 7/10 checks passed | 3 need you | Ready to export, 3 not reviewed | Show |  | What 
final server: (3, 0, 5, True, None)
final header: All cases | Delgado v. Hartwell - truck rear-end | Rename | 11 of 14 decided | cached demo
BLOCK>> Case overview | Entries | 7 of 7 | Flags | 3 of 4 | Amounts | 1 of 3 | Can export — 3 not reviewed (they stay out of the letter) | Open decisions | Start review | 1 flag to review | 2 charges to check | Case checks | 7/10 checks passed | 3 need you | Ready to export, 3 not reviewed | Show |  | What you need to do: Review the 2 items the AI objected to. Compare each one with its quote, then accept, edit or dismiss it. |  | Show this step | How the AI was checked | 11 checked, 9 agreed with the draft, 2 questioned | Show
   ROW>> Delgado v. Hartwell - truck rear-end | Last activity Nov 2, 2026, 9:44 AM · 7 records | 11 of 14 decided | Entries | 7 of 7 | Flags | 3 of 4 | Amounts | 1 of 3 | Analysis done | 3 need review | Can export — 3 not reviewed (they stay out of the letter)
filters: ['All cases (6)', 'Needs attention (6)', 'Ready to send (0)']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:44:45.441Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p13_finish_A2.py <<'EOF'\nimport json, urllib.request\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"lib03\"]\ndef get(p): return json.loads(urllib.request.urlopen(\"http://127.0.0.1:7943\"+p).read())\ndef summ():\n    c = [x for x in get(\"/api/cases\")[\"cases\"] if x[\"token\"] == TOK][0]\n    return c[\"hitl\"][\"pending\"], c[\"hitl\"][\"needs_review\"], c[\"export_ready\"], c.get(\"next_action\")\ndef rowtxt(pg):\n    pg.get_by_test_id(\"btn-all-cases\").click(); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(900)\n    r = pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"]')\n    print(\"   ROW>>\", \" | \".join(x.strip() for x in r.inner_text().split(\"\\n\") if x.strip()))\n    print(\"   filters:\", [x.inner_text() for x in pg.locator('[data-testid^=cases-filter-]').all()])\n    return r\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1600)\n    print(\"pending items:\", [ (i[\"id\"], i[\"kind\"] if \"kind\" in i else \"\", i.get(\"review_status\")) for i in get(f\"/api/cases/{TOK}\")[\"flags\"] if i.get(\"review_status\")==\"pending\"], [(a[\"id\"], a.get(\"kind\"), a.get(\"review_status\")) for a in get(f\"/api/cases/{TOK}\")[\"amounts\"] if a.get(\"review_status\")==\"pending\"])\n    pg.get_by_role(\"button\", name=\"Start review\").click(); pg.wait_for_timeout(500)\n    n = 0\n    while n < 12 and summ()[0] > 0:\n        iid = pg.evaluate(\"()=>{const it=document.activeElement.closest('[data-item-id]');return it&&it.dataset.itemId}\")\n        pg.keyboard.press(\"a\"); pg.wait_for_timeout(800); n += 1\n        print(f\"  a on {iid} -> {summ()[:3]}\")\n    print(\"final server:\", summ())\n    print(\"BLOCK>>\", pg.get_by_test_id(\"case-overview\").inner_text().replace(\"\\n\",\" | \")[:600])\n    print(\"header:\", pg.locator(\"header, .topbar\").first.inner_text().replace(\"\\n\",\" | \")[:100])\n    pg.screenshot(path=OUT+\"p13-A-all-decided.png\")\n    r = rowtxt(pg)\n    pg.screenshot(path=OUT+\"p13-overview-A-all-decided.png\")\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p13_finish_A2.py > artifacts/review-evidence/T-149-paralegal-r2/p13.out.txt 2>&1; cut -c1-800 artifacts/review-evidence/T-149-paralegal-r2/p13.out.txt"
}
````

### User / tool · 2026-11-02T15:45:00.598Z

**tool result**
````
pending items: [('f_gap_r6_r7', '', 'pending')] [('a1', 'charge', 'pending'), ('a3', 'charge', 'pending')]
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
  a on f_gap_r6_r7 -> (2, 5, True)
final server: (2, 5, True, None)
BLOCK>> Case overview | Entries | 7 of 7 | Flags | 4 of 4 | Amounts | 1 of 3 | Can export — 2 not reviewed (they stay out of the letter) | Open decisions | Start review | 2 charges to check | Case checks | 7/10 checks passed | 3 need you | Ready to export, 2 not reviewed | Show |  | What you need to do: Review the 2 items the AI objected to. Compare each one with its quote, then accept, edit or dismiss it. |  | Show this step | How the AI was checked | 11 checked, 9 agreed with the draft, 2 questioned | Show
header: All cases | Delgado v. Hartwell - truck rear-end | Rename | 12 of 14 decided | cached demo (curated 
   ROW>> Delgado v. Hartwell - truck rear-end | Last activity Nov 2, 2026, 9:44 AM · 7 records | 12 of 14 decided | Entries | 7 of 7 | Flags | 4 of 4 | Amounts | 1 of 3 | Analysis done | 2 need review | Can export — 2 not reviewed (they stay out of the letter)
   filters: ['All cases (6)', 'Needs attention (6)', 'Ready to send (0)']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:45:10.385Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p14_charges_export_A.py <<'EOF'\nimport json, urllib.request\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"lib03\"]\ndef get(p): return json.loads(urllib.request.urlopen(\"http://127.0.0.1:7943\"+p).read())\ndef summ():\n    c = [x for x in get(\"/api/cases\")[\"cases\"] if x[\"token\"] == TOK][0]\n    return c[\"hitl\"][\"pending\"], c[\"hitl\"][\"needs_review\"], c[\"export_ready\"], c.get(\"next_action\")\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1600)\n    for aid in (\"a1\", \"a3\"):\n        r = pg.locator(f'[data-item-id={aid}]').first; r.scroll_into_view_if_needed()\n        print(aid, \"row:\", r.inner_text().replace(\"\\n\",\" / \")[:240])\n        print(\"   buttons:\", [x.inner_text() for x in r.locator(\"button\").all()][:6])\n        r.focus(); pg.keyboard.press(\"a\"); pg.wait_for_timeout(900)\n        print(\"   after a:\", summ()[:3], \"| focus\", pg.evaluate(\"()=>document.activeElement.getAttribute('data-testid')\"))\n        dlg = pg.locator(\"[role=dialog]\")\n        if dlg.count(): print(\"   DIALOG:\", dlg.first.inner_text().replace(\"\\n\",\" / \")[:300])\n    pg.wait_for_timeout(1000)\n    print(\"final server:\", summ())\n    print(\"BLOCK>>\", pg.get_by_test_id(\"case-overview\").inner_text().replace(\"\\n\",\" | \")[:600])\n    print(\"header:\", pg.locator(\"header, .topbar\").first.inner_text().replace(\"\\n\",\" | \")[:100])\n    pg.screenshot(path=OUT+\"p14-A-after-charges.png\")\n    pg.get_by_test_id(\"btn-all-cases\").click(); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(900)\n    r = pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"]')\n    print(\"ROW>>\", \" | \".join(x.strip() for x in r.inner_text().split(\"\\n\") if x.strip()))\n    print(\"filters:\", [x.inner_text() for x in pg.locator('[data-testid^=cases-filter-]').all()])\n    pg.screenshot(path=OUT+\"p14-overview-A-done.png\")\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p14_charges_export_A.py > artifacts/review-evidence/T-149-paralegal-r2/p14.out.txt 2>&1; cut -c1-700 artifacts/review-evidence/T-149-paralegal-r2/p14.out.txt"
}
````

### User / tool · 2026-11-02T15:45:17.437Z

**tool result**
````
a1 row: $5,260.00 / Charge / 	 / Dx: lumbar and cervical sprain. CT cervical spine negative. Rx naproxen. Refer to chiropractic or primary care. ED charge: $5,260. / Open record 2 / Why this status / 	 / Quote matches / 	 / Accept / Dismiss / Audit
   buttons: ['Open record 2', 'Why this status', 'Accept', 'Dismiss', 'Audit']
   after a: (1, 5, True) | focus amount-$2,240
a3 row: $2,240.00 / Charge / 	 / L4-L5 disc bulge without nerve root compression. Mild disc desiccation. Radiology: findings likely chronic. MRI charge: $2,240. / Open record 7 / Why this status / 	 / Quote matches / 	 / Accept / Dismiss / Audit
   buttons: ['Open record 7', 'Why this status', 'Accept', 'Dismiss', 'Audit']
   after a: (0, 5, True) | focus btn-export
final server: (0, 5, True, None)
BLOCK>> Case overview | Entries | 7 of 7 | Flags | 4 of 4 | Amounts | 3 of 3 | Everything decided | Everything is decided |  | Nothing is waiting on you. Open Export to copy the treatment section; decisions you made are in the letter and the internal notes. |  | Go to Export | Case checks | 9/10 checks passed | 1 check was not run | Ready to export | Show |  | What you need to do: Review the 2 items the AI objected to. Compare each one with its quote, then accept, edit or dismiss it. |  | Show this step | How the AI was checked | 11 checked, 9 agreed with the draft, 2 questioned | Show
header: All cases | Delgado v. Hartwell - truck rear-end | Rename | 14 of 14 decided | cached demo (curated 
ROW>> Delgado v. Hartwell - truck rear-end | Last activity Nov 2, 2026, 9:45 AM · 7 records | 14 of 14 decided | Entries | 7 of 7 | Flags | 4 of 4 | Amounts | 3 of 3 | Analysis done | Everything decided
filters: ['All cases (6)', 'Needs attention (5)', 'Ready to send (1)']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:45:22.935Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p15_export.py <<'EOF'\nimport json, sys\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); key = sys.argv[1]; TOK = T[key]\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').click(); pg.wait_for_timeout(1600)\n    pg.get_by_test_id(\"btn-export\").click(); pg.wait_for_timeout(1500)\n    l = pg.get_by_test_id(\"export-letter\"); txt = l.inner_text()\n    open(OUT+f\"export-{key}.txt\", \"w\").write(txt)\n    print(txt)\n    pg.screenshot(path=OUT+f\"p15-export-{key}.png\")\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p15_export.py lib03 > artifacts/review-evidence/T-149-paralegal-r2/p15-A.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p15-A.out.txt | cut -c1-500"
}
````

### User / tool · 2026-11-02T15:45:27.445Z

**tool result**
````
TREATMENT CHRONOLOGY

April 6, 2026 — Okmarrow EMS run report
Restrained driver of a passenger car struck from behind by a tractor-trailer; complained of low back pain and neck pain; transported to Redhaven Regional ED.
Source [Ex. __ / Bates __]: "Passenger car struck from behind by a tractor-trailer. Restrained driver. C/O low back pain and neck pain. Transported to Redhaven Regional ED."

April 6, 2026 — Redhaven Regional ED
Diagnosed with lumbar and cervical sprain; CT cervical spine negative; naproxen prescribed; referred to chiropractic or primary care.
Source [Ex. __ / Bates __]: "Dx: lumbar and cervical sprain. CT cervical spine negative. Rx naproxen. Refer to chiropractic or primary care."

April 9, 2026 — Thimbleby Chiropractic, initial exam
Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks.
Source [Ex. __ / Bates __]: "Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks."

May 7, 2026 — Thimbleby Chiropractic, visit 14
Pain 5/10, unchanged from visit 1; plan to continue.
Source [Ex. __ / Bates __]: "Pain 5/10, unchanged from visit 1. Continue plan."

May 27, 2026 — Thimbleby Chiropractic, visit 22
Pain 4/10. Home exercises reviewed.
Source [Ex. __ / Bates __]: "Pain 4/10. Home exercises reviewed."

June 15, 2026 — Thimbleby Chiropractic, discharge
Discharged at maximum chiropractic benefit after 31 visits; pain 3/10.
Source [Ex. __ / Bates __]: "Discharged at maximum chiropractic benefit after 31 visits. Pain 3/10."

July 20, 2026 — Redhaven Imaging, lumbar MRI
L4-L5 disc bulge without nerve root compression; mild disc desiccation; radiology states findings likely chronic.
Source [Ex. __ / Bates __]: "L4-L5 disc bulge without nerve root compression. Mild disc desiccation. Radiology: findings likely chronic."

BILLED CHARGES

Redhaven Regional ED, April 6, 2026: $5,260.00
Source [Ex. __ / Bates __]: "ED charge: $5,260."
Redhaven Imaging, lumbar MRI, July 20, 2026: $2,240.00
Source [Ex. __ / Bates __]: "MRI charge: $2,240."

Billed charges accepted from these records: $7,500.00
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:45:31.423Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-060\" memory/ORCHESTRATOR_DECISIONS.md | head -3; grep -n \"accepted from these records\\|stated in these records\" memory/ORCHESTRATOR_DECISIONS.md | head -5; cat artifacts/review-evidence/T-149-paralegal-r2/p15-A.out.txt | wc -l; sed -n 1,3p /dev/null; grep -c \"Internal review notes\" artifacts/review-evidence/T-149-paralegal-r2/export-lib03.txt; ls artifacts/review-evidence/T-149-paralegal-r2/"
}
````

### User / tool · 2026-11-02T15:45:31.537Z

**tool result**
````
68:| D-060 | Amends D-059 (2026-11-02, T-140 adjuster r2): charge candidates are **default-deny**. An amount can be class `charge` only when it sits on an itemized service line: a date of service, a service description (CPT/HCPCS/revenue code or a service noun) and the amount on the same line or table row, in a provider bill or ledger. Every other amount (statement-level labels, account summaries, 'last statement', year-to-date, payment history, insurer documents, unlabeled figures) is `unclear` with its reason. Duplicates are matched on normalized date of service + service + amount (any date format). A charge cites its own line by offset, never by text search. | Deny-lists of total/balance wording lost every adversarial round; listing what a charge must look like cannot be outworded. | T-140 claims-adjuster r2 |
12:| D-004 | *(Partly superseded: guarded charge reclassification reinstated by D-042 (T-084); totals replaced by a cited line listing, D-052.)* Amounts: code extracts and classifies with explicit billing-phrase rules; judge #2 validates every classification; a rate can never become a charge; running total = accepted charges only; "detected" is shown separately and labelled not-a-total. Total line wording: "Billed charges stated in these records: $X". | Texas paid-or-incurred (§41.0105) — never "damages"; no PT total from a rate. | T-014 privacy B1; research T-008 |
27:| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
70:| D-062 | The letter total states what it is (2026-11-02, T-140 after 3 adversarial rounds). R-EX-8's line becomes `Billed charges accepted from these records: $X`, where X sums the charges the paralegal accepted one at a time, each listed above with its source line. The tool no longer claims the records themselves state the total. Charge sources are positively identified: only documents with a billing header (itemized statement, ledger, invoice, UB-04, CMS-1500) can yield a `charge`; clinical notes and discharge summaries yield a charge only from an encounter line, and never once the case holds an itemized bill from the same provider (amended at implementation: a literal ban zeroed the sample, whose charges are stated in visit notes); insurer and unknown documents never can. CPT/HCPCS codes are normalized ('CPT 99213' = '99213') before duplicate matching. Residual: a summary row dressed as a service line can still be accepted by a careless reviewer; it is cited and individually accepted, and listed as accepted debt. | An adversary can always word a ledger past a classifier; the honest claim is a sum of human-accepted, cited lines. | T-140 claims-adjuster r3 |
      38
0
export-lib03.txt
p1-overview-attention.png
p1-overview-default.png
p1.out.txt
p10.out.txt
p10_stale.py
p11.out.txt
p11_stale2.py
p12-A-all-decided.png
p12-overview-A-all-decided.png
p12.out.txt
p12_finish_A.py
p13-A-all-decided.png
p13-overview-A-all-decided.png
p13.out.txt
p13_finish_A2.py
p14-A-after-charges.png
p14-overview-A-done.png
p14.out.txt
p14_charges_export_A.py
p15-A.out.txt
p15-export-lib03.png
p15_export.py
p1_overview.py
p2-detail-lib01-after-go.png
p2-detail-lib01.png
p2-detail-lib02-after-go.png
p2-detail-lib02.png
p2-detail-sample-after-go.png
p2-detail-sample.png
p2.out.txt
p2_detail.py
p3-lib09-detail.png
p3.out.txt
p3_targets.py
p4.out.txt
p4_shortcuts.py
p5-A-after-one.png
p5.out.txt
p5_work_A.py
p6-A-final.png
p6.out.txt
p6_work_A2.py
p7-compare-prompt.png
p7.out.txt
p7_compare.py
p8-A-final.png
p8-overview-after-A.png
p8.out.txt
p8_finish_A.py
p9-A-reopened.png
p9.out.txt
p9_reload.py
setup.out.txt
setup_r2.py
tokens.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:45:41.231Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p16_paste_ui.py <<'EOF'\nimport json\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nL = \"/Users/arsis/zlayt-pm-project/evals/library/\"\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(800)\n    print(\"paste area visible:\", pg.get_by_test_id(\"input-text\").is_visible(), \"| title field:\", pg.get_by_test_id(\"input-title\").get_attribute(\"placeholder\"))\n    pg.screenshot(path=OUT+\"p16-home-full.png\", full_page=True)\n    for name, f in [(\"Nguyen - dog bite\", \"case_lib04_dog_bite_scar_revision.txt\"), (None, \"case_lib05_pedestrian_orif_hardware.txt\")]:\n        pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(600)\n        if name: pg.get_by_test_id(\"input-title\").fill(name)\n        pg.get_by_test_id(\"input-text\").fill(open(L+f).read())\n        pg.get_by_role(\"button\", name=\"Analyze\").click()\n        pg.get_by_test_id(\"case-name\").wait_for(state=\"visible\", timeout=60000); pg.wait_for_timeout(3000)\n        for _ in range(60):\n            if pg.get_by_test_id(\"case-overview\").count(): break\n            pg.wait_for_timeout(1000)\n        print(\"pasted\", f, \"-> header name:\", pg.get_by_test_id(\"case-name\").inner_text())\n    # rename the unnamed one\n    pg.get_by_test_id(\"btn-rename-case\").click(); pg.get_by_test_id(\"case-rename-input\").fill(\"Park - pedestrian ORIF\"); pg.keyboard.press(\"Enter\"); pg.wait_for_timeout(1000)\n    print(\"after rename header:\", pg.get_by_test_id(\"case-name\").inner_text())\n    pg.reload(); pg.wait_for_timeout(1800)\n    print(\"after reload, header:\", pg.get_by_test_id(\"case-name\").inner_text() if pg.get_by_test_id(\"case-name\").is_visible() else \"(not in a case)\")\n    pg.get_by_test_id(\"btn-all-cases\").click(); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(900)\n    print(\"titles:\", [r.get_by_test_id(\"cases-title\").inner_text() for r in pg.locator('[data-testid=cases-row]').all()])\n    print(\"Untitled anywhere:\", \"Untitled\" in pg.inner_text(\"body\"))\n    pg.screenshot(path=OUT+\"p16-overview-8cases.png\")\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p16_paste_ui.py > artifacts/review-evidence/T-149-paralegal-r2/p16.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p16.out.txt | cut -c1-500"
}
````

### User / tool · 2026-11-02T15:45:54.319Z

**tool result**
````
paste area visible: True | title field: Client or matter, for example Rivera knee
pasted case_lib04_dog_bite_scar_revision.txt -> header name: Nguyen - dog bite
pasted case_lib05_pedestrian_orif_hardware.txt -> header name: Brightwater EMS run report, Jan 22, 2026
after rename header: Park - pedestrian ORIF
after reload, header: Park - pedestrian ORIF
titles: ['Park - pedestrian ORIF', 'Nguyen - dog bite', 'Delgado v. Hartwell - truck rear-end', 'Quillmere Regional ED, Mar 3, 2026', 'Okafor LOP', 'Sablewood Market first-aid log, Mar 9, 2026', 'Dunmarrow Fire-Rescue run report, Feb 14, 2026', 'Austin EMS run report, Jan 9, 2026']
Untitled anywhere: False
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:46:00.030Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p17_titles.py <<'EOF'\nimport json, urllib.request\nB=\"http://127.0.0.1:7943\"\ndef post(body):\n    r = urllib.request.Request(B+\"/api/cases\", data=json.dumps(body).encode(), method=\"POST\", headers={\"Content-Type\":\"application/json\"})\n    try:\n        with urllib.request.urlopen(r) as f: return f.status, json.loads(f.read())\n    except urllib.error.HTTPError as e: return e.code, json.loads(e.read() or b\"{}\")\ntxt = open(\"/Users/arsis/zlayt-pm-project/evals/golden/sample.txt\").read()\nfor label, body in [(\"no headers\", {\"text\": \"Seen on 2026-01-02 for knee pain after a fall. Dr. Ames advised rest.\"}),\n                    (\"same sample pasted again, no name\", {\"text\": txt}),\n                    (\"blank name\", {\"text\": txt.replace(\"Rivera\", \"Soto\"), \"name\": \"   \"})]:\n    st, c = post(body); print(label, \"->\", st, repr(c.get(\"title\")), repr(c.get(\"name\")))\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p17_titles.py > artifacts/review-evidence/T-149-paralegal-r2/p17.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p17.out.txt | cut -c1-300"
}
````

### User / tool · 2026-11-02T15:46:00.185Z

**tool result**
````
no headers -> 409 None None
same sample pasted again, no name -> 201 'Austin EMS run report, Jan 9, 2026' None
blank name -> 409 None None
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:46:14.880Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p18_work_B.py <<'EOF'\nimport json, urllib.request\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nT = json.load(open(OUT+\"tokens.json\")); TOK = T[\"sample\"]\ndef get(p): return json.loads(urllib.request.urlopen(\"http://127.0.0.1:7943\"+p).read())\ndef summ():\n    c = [x for x in get(\"/api/cases\")[\"cases\"] if x[\"token\"] == TOK][0]\n    return c[\"hitl\"][\"pending\"], c[\"hitl\"][\"edits_to_check\"], c[\"export_ready\"], (c.get(\"next_action\") or {}).get(\"item_id\")\ndef line(pg):\n    l = pg.locator(\"[data-testid=do-first]\"); return l.inner_text().replace(\"\\n\",\" \")[12:110] if l.count() else \"(no do-first line)\"\nimport time\nt0 = time.time()\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(700)\n    # keyboard open: j until the sample row has focus, Enter\n    pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"] [data-testid=cases-open]').focus(); pg.keyboard.press(\"Enter\"); pg.wait_for_timeout(1600)\n    print(\"opened:\", pg.get_by_test_id(\"case-name\").inner_text(), summ())\n    pg.screenshot(path=OUT+\"p18-B-open.png\")\n    # edit record 3 summary\n    row3 = pg.locator('[data-testid=entry-3]'); row3.scroll_into_view_if_needed(); row3.focus(); pg.keyboard.press(\"e\"); pg.wait_for_timeout(400)\n    ta = row3.locator(\"textarea\"); print(\"rec3 original summary:\", ta.first.input_value())\n    ta.first.fill(\"Persistent neck pain 6/10 and daily headaches; referred to physical therapy.\"); pg.keyboard.press(\"Control+Enter\"); pg.wait_for_timeout(1000)\n    print(\"rec3 after edit:\", row3.inner_text().replace(\"\\n\",\" / \")[:380]); print(\"  server:\", summ())\n    n = 0; dflag = None\n    while n < 45:\n        s = summ()\n        if s[0] == 0 and s[1] == 0: break\n        btn = pg.locator(\"[data-testid=btn-do-first]\")\n        used = \"do-first\"\n        if not btn.count():\n            pg.wait_for_timeout(1200); used = \"Start review (no do-first line)\"\n            btn = pg.get_by_role(\"button\", name=\"Start review\")\n            if not btn.count(): print(\"  stuck\", s); break\n        ln = line(pg); btn.first.click(); pg.wait_for_timeout(350)\n        iid = pg.evaluate(\"()=>{const it=document.activeElement.closest('[data-item-id]');return it&&it.dataset.itemId}\")\n        key = \"a\"\n        if iid == \"a2\" or (iid and iid.startswith(\"f_\") and dflag is None): key = \"d\"; dflag = dflag or iid\n        pg.keyboard.press(key); pg.wait_for_timeout(700)\n        if pg.evaluate(\"()=>document.activeElement.getAttribute('data-testid')\") == \"btn-accept\" and (iid or \"\").startswith(\"e\"):\n            pg.keyboard.press(\"Enter\"); pg.wait_for_timeout(700); key += \"+Enter\"\n        n += 1; pg.wait_for_timeout(300); print(f\"  {n}: via {used} | line: {ln} | item {iid} key {key} -> {summ()}\")\n    print(\"done:\", summ(), \"| elapsed s:\", round(time.time()-t0))\n    print(\"BLOCK>>\", pg.get_by_test_id(\"case-overview\").inner_text().replace(\"\\n\",\" | \")[:500])\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p18_work_B.py > artifacts/review-evidence/T-149-paralegal-r2/p18.out.txt 2>&1; cut -c1-520 artifacts/review-evidence/T-149-paralegal-r2/p18.out.txt"
}
````

### User / tool · 2026-11-02T15:47:17.002Z

**tool result**
````
opened: Austin EMS run report, Jan 9, 2026 (23, 0, False, 'a2')
rec3 original summary: Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.
rec3 after edit: January 16, 2026 / Dr. Alvarez, primary care / Rec 3 /  / The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked. /  / Needs review / Edited / Not in an entry (1) /  / Persistent neck pain 6/10 and daily headaches; referred to physical therapy. /  / Edited by you; the code checked your wording against the quote when 
  server: (22, 1, False, 'e3')
  1: via do-first | line: t: The second check failed (the AI check was asked and gave no usable answer), so this item has no | item e3 key a+Enter -> (22, 0, True, 'a2')
  2: via do-first | line: t: This figure is a rate, not a charge, so it is not added to the total.  Go to it | item a2 key d -> (21, 0, True, 'a3')
  3: via do-first | line: t: This figure is not a bill (for example a damages or settlement figure), so it is not added to t | item a3 key a -> (20, 0, True, 'f_r7_1')
  4: via do-first | line: t: The phrase list found this flag but the AI did not; check that it applies.  Go to it | item f_r7_1 key a -> (19, 0, True, None)
  5: via Start review (no do-first line) | line: (no do-first line) | item e1 key a -> (18, 0, True, None)
  6: via Start review (no do-first line) | line: (no do-first line) | item e2 key a -> (17, 0, True, None)
  7: via Start review (no do-first line) | line: (no do-first line) | item e4 key a -> (16, 0, True, None)
  8: via Start review (no do-first line) | line: (no do-first line) | item e5 key a -> (15, 0, True, None)
  9: via Start review (no do-first line) | line: (no do-first line) | item e6 key a -> (14, 0, True, None)
  10: via Start review (no do-first line) | line: (no do-first line) | item e7 key a -> (13, 0, True, None)
  11: via Start review (no do-first line) | line: (no do-first line) | item e8 key a -> (12, 0, True, None)
  12: via Start review (no do-first line) | line: (no do-first line) | item e9 key a -> (11, 0, True, None)
  13: via Start review (no do-first line) | line: (no do-first line) | item f_gap_r6_r7 key a -> (10, 0, True, None)
  14: via Start review (no do-first line) | line: (no do-first line) | item f_accident_date_after_treatment_1_2_7 key a -> (9, 0, True, None)
  15: via Start review (no do-first line) | line: (no do-first line) | item f_cx1 key a -> (8, 0, True, None)
  16: via Start review (no do-first line) | line: (no do-first line) | item f_r3_1 key a -> (7, 0, True, None)
  17: via Start review (no do-first line) | line: (no do-first line) | item f_r8_1 key a -> (6, 0, True, None)
  18: via Start review (no do-first line) | line: (no do-first line) | item f_r6_1 key a -> (5, 0, True, None)
  19: via Start review (no do-first line) | line: (no do-first line) | item f_r7_2 key a -> (4, 0, True, None)
  20: via Start review (no do-first line) | line: (no do-first line) | item f_r8_2 key a -> (3, 0, True, None)
  21: via Start review (no do-first line) | line: (no do-first line) | item f_r9_1 key a -> (2, 0, True, None)
  22: via Start review (no do-first line) | line: (no do-first line) | item a1 key a -> (1, 0, True, None)
  23: via Start review (no do-first line) | line: (no do-first line) | item a4 key a -> (0, 0, True, None)
done: (0, 0, True, None) | elapsed s: 62
BLOCK>> Case overview | Entries | 9 of 9 | Flags | 10 of 10 | Amounts | 4 of 4 | Everything decided | Everything is decided |  | Nothing is waiting on you. Open Export to copy the treatment section; decisions you made are in the letter and the internal notes. |  | Go to Export | Case checks | 10/10 checks passed | Ready to export | Show | How the AI was checked | checked 18, all agreed with the draft | Show
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:47:26.211Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p15_export.py sample > artifacts/review-evidence/T-149-paralegal-r2/p15-B.out.txt 2>&1; cut -c1-330 artifacts/review-evidence/T-149-paralegal-r2/p15-B.out.txt; cat > artifacts/review-evidence/T-149-paralegal-r2/p19_overview_final.py <<'EOF'\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(\"http://127.0.0.1:7943/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(1200)\n    print(\"filters:\", [x.inner_text() for x in pg.locator('[data-testid^=cases-filter-]').all()])\n    pg.get_by_test_id(\"cases-sort\").select_option(\"attention\"); pg.wait_for_timeout(300)\n    for r in pg.locator('[data-testid=cases-row]').all():\n        print(\"ROW>>\", \" | \".join(t.strip() for t in r.inner_text().split(\"\\n\") if t.strip())[:330])\n    pg.screenshot(path=OUT+\"p19-overview-final.png\")\n    pg.get_by_test_id(\"cases-filter-ready\").click() if pg.get_by_test_id(\"cases-filter-ready\").count() else None\n    pg.wait_for_timeout(300); print(\"ready filter ->\", [r.get_by_test_id(\"cases-title\").inner_text() for r in pg.locator('[data-testid=cases-row]').all()])\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p19_overview_final.py > artifacts/review-evidence/T-149-paralegal-r2/p19.out.txt 2>&1; cat artifacts/review-evidence/T-149-paralegal-r2/p19.out.txt"
}
````

### User / tool · 2026-11-02T15:47:33.283Z

**tool result**
````
TREATMENT CHRONOLOGY

January 9, 2026 — Austin EMS run report
Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."

January 9, 2026 — Central ER discharge summary
Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."

January 16, 2026 — Dr. Alvarez, primary care
Persistent neck pain 6/10 and daily headaches; referred to physical therapy.
Source [Ex. __ / Bates __]: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."

January 23, 2026 — Capital PT, initial evaluation
Cervical range of motion reduced approx. 40%; plan of care 12 visits.
Source [Ex. __ / Bates __]: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."

February 20, 2026 — Capital PT, visit 8
Pain 4/10, improving.
Source [Ex. __ / Bates __]: "Pain 4/10, improving."

March 6, 2026 — Capital PT, visit 9
Discharged from physical therapy after two missed appointments; pain 3/10.
Source [Ex. __ / Bates __]: "Discharged from PT after two missed appointments. Pain 3/10."

May 18, 2026 — Hill Country Pain Management, new patient
New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
Source [Ex. __ / Bates __]: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered."

May 29, 2026 — Austin Imaging, cervical MRI
C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."

June 12, 2026 — Hill Country Pain Management, follow-up
Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
Source [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."

BILLED CHARGES

Central ER discharge summary, January 9, 2026: $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240."
Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
Source [Ex. __ / Bates __]: "Charge: $2,150."

Billed charges accepted from these records: $8,390.00
filters: ['All cases (9)', 'Needs attention (7)', 'Ready to send (2)']
ROW>> Okafor LOP | Last activity Nov 2, 2026, 9:37 AM · 7 records | 0 of 19 decided | Entries | 0 of 7 | Flags | 0 of 5 | Amounts | 0 of 7 | Analysis done | 9 need review | 1 could not be verified | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Sablewood Market first-aid log, Mar 9, 2026 | Last activity Nov 2, 2026, 9:37 AM · 7 records | 0 of 18 decided | Entries | 0 of 7 | Flags | 0 of 8 | Amounts | 0 of 3 | Analysis done | 6 need review | 1 could not be verified | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Park - pedestrian ORIF | Last activity Nov 2, 2026, 9:45 AM · 8 records | 0 of 16 decided | Entries | 0 of 8 | Flags | 0 of 5 | Amounts | 0 of 3 | Analysis done | 4 need review | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Nguyen - dog bite | Last activity Nov 2, 2026, 9:45 AM · 6 records | 0 of 11 decided | Entries | 0 of 6 | Flags | 0 of 2 | Amounts | 0 of 3 | Analysis done | 2 need review | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Dunmarrow Fire-Rescue run report, Feb 14, 2026 | Last activity Nov 2, 2026, 9:37 AM · 6 records | 0 of 9 decided | Entries | 0 of 5 | Flags | 0 of 2 | Amounts | 0 of 2 | Analysis done | 2 need review | 1 could not be verified | Export blocked (1) | Nothing is accepted or edited yet, so the letter would be empty.
ROW>> Quillmere Regional ED, Mar 3, 2026 | Last activity Nov 2, 2026, 9:37 AM · 7 records | Entries | Not started | Flags | Not started | Amounts | Not started | Not analyzed yet | Not analyzed: open the case and press Analyze.
ROW>> Austin EMS run report, Jan 9, 2026 | Last activity Nov 2, 2026, 9:46 AM · 9 records | Entries | Not started | Flags | Not started | Amounts | Not started | Not analyzed yet | Not analyzed: open the case and press Analyze.
ROW>> Austin EMS run report, Jan 9, 2026 | Last activity Nov 2, 2026, 9:47 AM · 9 records | 23 of 23 decided | Entries | 9 of 9 | Flags | 10 of 10 | Amounts | 4 of 4 | Analysis done | Everything decided
ROW>> Delgado v. Hartwell - truck rear-end | Last activity Nov 2, 2026, 9:45 AM · 7 records | 14 of 14 decided | Entries | 7 of 7 | Flags | 4 of 4 | Amounts | 3 of 3 | Analysis done | Everything decided
ready filter -> ['Austin EMS run report, Jan 9, 2026', 'Delgado v. Hartwell - truck rear-end']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:48:02.429Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-149-paralegal-r2/p20_partial.py <<'EOF'\nimport json, urllib.request\nfrom playwright.sync_api import sync_playwright\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/\"\nB = \"http://127.0.0.1:7943\"\ndef api(m, p, body=None):\n    d = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(B+p, data=d, method=m, headers={\"Content-Type\":\"application/json\"})\n    with urllib.request.urlopen(r) as f: t=f.read(); return json.loads(t) if t else None\ncs = [c for c in api(\"GET\", \"/api/cases\")[\"cases\"] if c[\"title\"] == \"Nguyen - dog bite\"]; TOK = cs[0][\"token\"]\nd = api(\"GET\", f\"/api/cases/{TOK}\"); ents = [e for e in d[\"entries\"] if e[\"state\"] == \"verified\"]\nprint(\"entries:\", [(e[\"id\"], e[\"state\"], e.get(\"date\")) for e in d[\"entries\"]])\nfor e in ents[:2]: api(\"POST\", f\"/api/cases/{TOK}/items/{e['id']}/review\", {\"action\": \"accept\"})\napi(\"POST\", f\"/api/cases/{TOK}/items/{ents[2]['id']}/review\", {\"action\": \"dismiss\"})\nprint(\"accepted\", [e[\"id\"] for e in ents[:2]], \"dismissed\", ents[2][\"id\"], \"left alone\", [e[\"id\"] for e in d[\"entries\"] if e[\"id\"] not in [x[\"id\"] for x in ents[:3]]])\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\": 1440, \"height\": 900})\n    pg.goto(B+\"/\"); pg.get_by_test_id(\"cases-list\").wait_for(); pg.wait_for_timeout(1000)\n    r = pg.locator(f'[data-testid=cases-row][data-token=\"{TOK}\"]')\n    print(\"ROW>>\", \" | \".join(x.strip() for x in r.inner_text().split(\"\\n\") if x.strip()))\n    print(\"any element with green ready chip:\", pg.locator(\"[data-testid=cases-chip-ready]\").count())\n    r.locator(\"[data-testid=cases-open]\").click(); pg.wait_for_timeout(1500)\n    pg.get_by_test_id(\"btn-export\").click(); pg.wait_for_timeout(1500)\n    print(\"EXPORT PANEL (top):\", pg.locator(\"[data-testid=export-panel], dialog, [role=dialog]\").first.inner_text().replace(\"\\n\",\" | \")[:900] if pg.locator(\"[data-testid=export-panel], dialog, [role=dialog]\").count() else pg.inner_text(\"body\")[:900])\n    txt = pg.get_by_test_id(\"export-letter\").inner_text(); open(OUT+\"export-nguyen-partial.txt\",\"w\").write(txt)\n    print(\"--- LETTER ---\\n\"+txt[:1800])\n    pg.screenshot(path=OUT+\"p20-export-partial.png\")\n    b.close()\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-149-paralegal-r2/p20_partial.py > artifacts/review-evidence/T-149-paralegal-r2/p20.out.txt 2>&1; cut -c1-1000 artifacts/review-evidence/T-149-paralegal-r2/p20.out.txt"
}
````

### User / tool · 2026-11-02T15:48:07.378Z

**tool result**
````
entries: [('e1', 'verified', '2025-09-13'), ('e2', 'verified', '2025-09-13'), ('e3', 'verified', '2025-09-20'), ('e4', 'verified', '2025-10-18'), ('e5', 'verified', '2025-12-13'), ('e6', 'verified', '2026-09-12')]
accepted ['e1', 'e2'] dismissed e3 left alone ['e4', 'e5', 'e6']
ROW>> Nguyen - dog bite | Last activity Nov 2, 2026, 9:48 AM · 6 records | 3 of 11 decided | Entries | 3 of 6 | Flags | 0 of 2 | Amounts | 0 of 3 | Analysis done | 2 need review | Can export — 8 not reviewed (they stay out of the letter)
any element with green ready chip: 2
EXPORT PANEL (top):  |   Source recordClose |    | 
--- LETTER ---
TREATMENT CHRONOLOGY

September 13, 2025 — Wrenfield EMS run report
Adult bitten on the left cheek and chin by a neighbor's dog; bleeding controlled; transported to Harlow Memorial ED.
Source [Ex. __ / Bates __]: "Adult bitten on the left cheek and chin by a neighbor's dog. Bleeding controlled. Transported to Harlow Memorial ED."

September 13, 2025 — Harlow Memorial ED
Dx dog bite with left cheek laceration 4 cm and chin laceration 2 cm; wounds irrigated and sutured; amoxicillin-clavulanate prescribed.
Source [Ex. __ / Bates __]: "Dx: dog bite, left cheek laceration 4 cm and chin laceration 2 cm. Wounds irrigated and sutured. Amoxicillin-clavulanate prescribed."
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:48:10.086Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/p20-export-partial.png"
}
````

### User / tool · 2026-11-02T15:48:10.096Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:48:12.473Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/p19-overview-final.png"
}
````

### User / tool · 2026-11-02T15:48:12.484Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:48:21.977Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r2-802d5fd && env -u ZLAYT_DB timeout 560 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_multicase.py -q -x -p no:cacheprovider > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/pytest-multicase.out.txt 2>&1; tail -8 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/pytest-multicase.out.txt",
 "timeout": 580000
}
````

### User / tool · 2026-11-02T15:48:22.240Z

**tool result**
````
env: timeout: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:48:26.050Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r2-802d5fd && env -u ZLAYT_DB /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_multicase.py -q -p no:cacheprovider > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/pytest-multicase.out.txt 2>&1; tail -8 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/pytest-multicase.out.txt",
 "timeout": 580000
}
````

### User / tool · 2026-11-02T15:48:48.216Z

**tool result**
````
...................................s                                     [100%]
35 passed, 1 skipped in 20.99s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:48:52.050Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r2-802d5fd && grep -n \"skip\" tests/e2e/test_multicase.py | head; grep -n \"do-first\\|do_first\" tests/e2e/test_multicase.py | head -20"
}
````

### User / tool · 2026-11-02T15:48:52.148Z

**tool result**
````
43:        pytest.skip("app server not running")
666:@pytest.mark.skipif(os.environ.get("ZLAYT_SCREENSHOTS") != "1", reason="set ZLAYT_SCREENSHOTS=1 to write artifacts/screenshots/multicase-*.png")
520:    line = page.get_by_test_id("case-overview").get_by_test_id("do-first")
524:    line.get_by_test_id("btn-do-first").click()
533:    expect(page.get_by_test_id("case-overview").get_by_test_id("do-first")).to_have_count(0)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:48:55.133Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r2-802d5fd && sed -n 505,540p tests/e2e/test_multicase.py"
}
````

### User / tool · 2026-11-02T15:48:55.301Z

**tool result**
````
# ---- "Do this first" (T-157 next_action), naming a case, and the second-check offer -----------------------------------------------------------
def _with_next_action(page, tok, na):
    def f(body):
        for c in body["cases"]:
            if c["token"] == tok:
                c["next_action"] = na
        return body
    _stub_list(page, f)


def test_do_this_first_is_one_line_built_from_next_action_and_its_button_goes_to_that_item(page, cs):
    c = api("GET", f"/api/cases/{cs['a']}")[1]
    item = next(e for e in c["entries"] if e.get("review_status") == "pending")
    _with_next_action(page, cs["a"], {"item_id": item["id"], "kind": "entry", "reason": "Decide this entry: its quote does not match the record word for word."})
    open_case(page, cs["a"])
    line = page.get_by_test_id("case-overview").get_by_test_id("do-first")
    expect(line).to_have_count(1)
    expect(line).to_contain_text("Do this first")
    expect(line).to_contain_text("its quote does not match the record word for word")
    line.get_by_test_id("btn-do-first").click()
    expect(page.locator(f'[data-item-id="{item["id"]}"]').first).to_be_focused()
    for n in page.get_by_test_id("case-next-action").all():
        expect(n).to_be_hidden()                                  # the case checks do not give a second, different first step


def test_without_next_action_there_is_no_do_this_first_line(page, cs):
    _with_next_action(page, cs["a"], None)
    open_case(page, cs["a"])
    expect(page.get_by_test_id("case-overview").get_by_test_id("do-first")).to_have_count(0)


def _accept_three(tok):
    c = api("GET", f"/api/cases/{tok}")[1]
    ids = [e["id"] for e in c["entries"] if e["state"] != "rejected" and e["date"]][:3]
    for i in ids:
        assert api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "accept"})[0] == 200
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:48:58.964Z

**tool call — Bash**
````
{
 "command": "PID=$(lsof -iTCP:7943 -sTCP:LISTEN -nP -t); echo \"PID=$PID\"; kill $PID; sleep 2; lsof -iTCP:7943 -sTCP:LISTEN -nP; echo \"lsof exit $?\"; curl -s -o /dev/null -w \"curl %{http_code}\\n\" http://127.0.0.1:7943/; ls artifacts/review-evidence/T-149-paralegal-r2/ | wc -l; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T15:49:01.305Z

**tool result**
````
PID=1826
lsof exit 1
curl 000
      76
95ffe36
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:50:03.628Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-149-paralegal-r2.md",
 "content": "# T-149 round 2 paralegal review (paralegal-reviewer, Maria Delgado persona)\n\nVerdict: **changes** (0 blockers, 1 major, 4 minors, 2 nits). Two of my three round-1 majors are fixed; the third (a \"Do this first\" line that names the item) is only half fixed.\n\nI ran `git archive 802d5fd` into the scratchpad (`r2-802d5fd`). HEAD was 95ffe36 by the end; `git diff --stat 802d5fd 985dbd2 -- app/frontend` touched only review.js, timeline.js, uncovered.css and uncovered.js, so the overview and detail code under review is the same. I served it on 127.0.0.1:7943 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratchpad DB. I created 9 cases: 6 seeded by API paste (3 unnamed, 2 named, 1 never analyzed), 2 pasted through the home screen (one named, one unnamed then renamed), and 1 accidental duplicate. The server (PID 1826) was stopped by PID: `lsof -iTCP:7943 -sTCP:LISTEN` exit 1, curl 000. Port 7860 was not touched. Scripts and outputs are in `artifacts/review-evidence/T-149-paralegal-r2/`.\n\n## Round-1 majors\n\n**F-1 case names: fixed.** The home screen has a \"Client or matter\" field (`p1.out.txt`: `input-title`). A named paste shows its name in the header (\"Nguyen - dog bite\"). An unnamed paste gets the provider and date of record 1 (\"Brightwater EMS run report, Jan 22, 2026\"), never \"Untitled case\" (`p16.out.txt`: \"Untitled anywhere: False\"). Rename in the detail header (\"Park - pedestrian ORIF\") survived a reload and showed in the overview. Rename is only in the detail header, not on the row; that is fine.\n\n**F-2 export green while items are unreviewed: fixed.** With 1 of 14 items decided the row and the block read the amber \"Can export — 13 not reviewed (they stay out of the letter)\" (`p5.out.txt`). The green \"Everything decided\" appeared only at 14 of 14 (`p14.out.txt`), and the filters then read \"Needs attention (5)\", \"Ready to send (1)\". A partly reviewed case (2 accepted, 1 dismissed, 8 not reviewed) showed amber, and its export summary says \"8 items pending (2 flags)\". The letter held exactly the two accepted entries; the dismissed one and the unreviewed ones were absent (`p20.out.txt`, `export-nguyen-partial.txt`). The two cases I worked to the end exported with only accepted items and cited quotes; the sample total reads $8,390.00 (`export-sample.txt`; line wording follows D-062).\n\n**F-3 one \"Do this first\" line that names the item and links to it: half fixed (F-A below).** There is one line per block and the button lands on the item the server named. It does not name the item, and two buttons still disagree.\n\n## Can I tell at a glance which case needs me, and why?\n\nPartly. The rows show \"n of N decided\", per-kind bars, \"n need review\" and, with 9 cases, the \"Needs attention first\" sort puts the untouched cases with the most items left on top (`p19.out.txt`). But six of the seven untouched rows carry the same sentence, \"Nothing is accepted or edited yet, so the letter would be empty.\" and none says what kind of item waits (date conflict, gap, prior condition), so I cannot rank by what the adjuster will attack. Never-analyzed cases now say \"Not analyzed: open the case and press Analyze.\" (fixed since round 1). Working two cases from the overview to export (Delgado, 14 items, and the Rivera sample, 23 items, the latter in 62 seconds of keyboard work including waits) went smoothly: j/k and Enter on the overview, \"Go to it\", then `a`, `d`, `e` and Enter on the compare button.\n\n## Findings\n\n**F-A (major). \"Do this first\" does not name the item, and the block still holds two blue buttons with different first steps.** On the Rivera sample the line reads \"Do this first: This figure is a rate, not a charge, so it is not added to the total.\" No record, provider or amount is named (`p2.out.txt`); \"Go to it\" lands on amount `$185` (a2). The primary \"Start review\" button directly under it lands on flag `f_r7_1`, the accident-date source (`p3.out.txt`: \"Start review -> flag-f_r7_1\", \"Go to it -> amount-$185\"). On lib02 \"Go to it\" lands on flag f_r2_1 and \"Start review\" on entry e4 (`p3.out.txt`). The same sentence is shown for different items: \"A second AI check disagreed with the first result for this item.\" was the line for f_r7_1, then for f_r7_2, then f_r7_3 as I decided them (`p10.out.txt`, `p11.out.txt`, `p12.out.txt` steps 1 and 2), so I could not tell the line had moved on. Expanding \"Case checks\" gives a third answer, \"What you need to do: This item cannot be used. Dismiss it, or write the entry by hand from the record.\" (`p3.out.txt`, lib02), again naming nothing. The card's own test stubs a `next_action` reason and never asserts that the line names a record or provider (`tests/e2e/test_multicase.py:514-529` in the archive). That is the round-1 acceptance test \"its text names a record or provider; Start review never names a different target\", still unmet. Fix: build the line as \"Do this first: Record 4, Capital PT: <reason>\" (or \"$185.00 rate, record 4\") from `next_action.item_id`; make \"Start review\" go to the same item as \"Go to it\", or show only one of them. Acceptance test: on the Rivera sample and lib02 the do-first text contains the record number or provider of the item at `next_action.item_id`, and the focus after \"Go to it\" and after \"Start review\" is the same `data-item-id`.\n\n**F-B (minor). The line disappears while items are still pending.** With 3 items left (1 gap flag, 2 charges) the server's `next_action` was null and the block showed no \"Do this first\" line, only \"Start review\" and the case-checks bar (`p12.out.txt`: \"!! no do-first button with pending (3, 0, 5, True, None)\"). On the Rivera sample, from step 5 to 23 (18 items down to 1 pending) every step went through \"Start review (no do-first line)\" (`p18.out.txt`). The block never says what comes next once the AI-flagged items are done. Fix: when `next_action` is null and items are pending, show \"Do this first: Review the remaining n items\" with the same target as \"Start review\". Test: a case with pending items always has one do-first line.\n\n**F-C (minor). The overview row overstates \"need review\" against the detail.** After I decided some flags, the Delgado row read \"5 need review\" while the opened case read \"3 items need review\" (`p8.out.txt` row, `p9.out.txt` block), and \"5 need review\" again against \"2 items need\" (`p12.out.txt` start). The server's `hitl.needs_review` stays at 5 (second value of the tuple in `p12.out.txt` is pending, third is `needs_review`: \"(5, 0, 5, True, 'f_r7_2')\"). The handoff says the backend field `needs_review_open` is still to come. It errs on the safe side, but the row and the detail disagree about the same case. Fix: the backend returns the open count; the row uses it. Test: row count equals the detail header count after decisions.\n\n**F-D (minor). The case checks contradict the new wording and go stale.** The block chip says \"Can export — 13 not reviewed\", while the Case checks line says \"Ready to export, 13 not reviewed\" (`p5.out.txt` step 1). When everything is decided the expanded checks still carry \"What you need to do: Review the 2 items the AI objected to\" (`p14.out.txt`). Fix: use one phrase (\"Can export, n not reviewed\") in both places, and clear the step text when nothing is pending.\n\n**F-E (minor, carried from round 1 F-5). The row says how many but not why.** Six rows repeat the same blocker sentence and the \"n need review\" chip has no kind (`p19.out.txt`). The handoff lists the \"why\" line as skipped. On the sample the first do-first items are the $185 rate, a $ figure that is not a bill, and a phrase-list flag; the accident-date conflict was only reached in step 14 (`p18.out.txt`). Fix: one line under the chips from the server's kinds (\"1 date conflict, 1 gap, 2 prior conditions\"), and rank date conflicts and gaps ahead of rate notes in `next_action`.\n\n**F-F (nit). Identical derived titles for identical records.** Pasting the same records twice gives two rows \"Austin EMS run report, Jan 9, 2026\" (`p19.out.txt`). Say so on the row (\"same title as another case\") or add the created minute.\n\n**F-G (nit). Test count does not match the card.** The card says \"36 pass\"; plain pytest from the archive gave \"35 passed, 1 skipped\" (`pytest-multicase.out.txt`). The skipped one is the screenshot test (needs `ZLAYT_SCREENSHOTS=1`). The round-1 keyboard failure did not recur.\n\n## What I exercised\n\n1. `git archive 802d5fd`, server on 7943 (PID 1826, stopped); `setup_r2.py` seeded 6 cases and read GET /api/cases (`setup.out.txt`).\n2. `p1_overview.py`: row text, sorts, filters, home inputs. `p2_detail.py`, `p3_targets.py`: do-first, Start review and case-next-action on four cases.\n3. `p4_shortcuts.py`: j/k/Enter on the overview. `p5` to `p14`: Delgado edited (Rec 3), compared, a flag dismissed, all 14 items decided with the keyboard; row and filters after each stage.\n4. `p15_export.py` on both worked cases; `p18_work_B.py` on the Rivera sample; `p16_paste_ui.py` (named paste, unnamed paste, rename, reload); `p17_titles.py`; `p20_partial.py` (partly reviewed case and its export panel).\n5. `tests/e2e/test_multicase.py` from the archive with plain pytest.\n\n```json\n{\"card\": \"T-149\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive 802d5fd (frontend identical to HEAD at review start 985dbd2 apart from review.js, timeline.js, uncovered.css/js) served on http://127.0.0.1:7943 (PID 1826, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; 9 cases (6 API-pasted, 2 pasted in the UI, 1 duplicate); two cases worked from the overview to export (Delgado v. Hartwell truck rear-end, Rivera sample); live dev app 7860 not touched\",\n \"exercised\": [\n  \"git archive 802d5fd into the scratchpad; server on 7943 under .venv/bin/python -I with the T-060 pass-4 launcher; curl 200; stopped by PID 1826 (lsof exit 1, curl 000)\",\n  \"seeded 6 cases through POST /api/cases (3 unnamed, 2 named, 1 left unanalyzed) and read GET /api/cases (setup_r2.py)\",\n  \"overview in the browser: row text, filters, sorts, home inputs, j/k/Enter (p1_overview.py, p4_shortcuts.py)\",\n  \"detail of four cases: do-first line, Go to it and Start review focus targets, case-next-action text (p2_detail.py, p3_targets.py)\",\n  \"pasted two cases through the home screen (one with a name, one without), renamed one in the detail header, reloaded, read the overview titles (p16_paste_ui.py)\",\n  \"worked Delgado v. Hartwell from the overview to export with the keyboard: renamed, edited Rec 3, compared, dismissed a flag, accepted the rest; read the row and filters at 1 of 14, 12 of 14 and 14 of 14 (p5 to p14)\",\n  \"worked the Rivera sample from the overview to export: edited Rec 3, dismissed the rate and a flag, accepted the rest, 62 seconds (p18_work_B.py)\",\n  \"exported both cases and a partly reviewed third case; read the letter text and the export summary and internal notes block (p15_export.py, p20_partial.py)\",\n  \"tests/e2e/test_multicase.py from the archive with plain pytest: 35 passed, 1 skipped\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"verify_quickly\": 4, \"overview_triage\": 3, \"ready_to_send_signal\": 4, \"detail_first_action\": 3, \"identify_case\": 4},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"'Do this first' does not name the item, and 'Start review' goes to a different item than 'Go to it'\",\n   \"evidence\": \"artifacts/review-evidence/T-149-paralegal-r2/p2.out.txt sample: 'Do this first: This figure is a rate, not a charge, so it is not added to the total.' (no record, provider or amount); p3.out.txt: sample 'Start review -> flag-f_r7_1' vs 'Go to it -> amount-$185', lib02 'Start review -> entry-4' vs 'Go to it -> flag-f_r2_1'; p10/p11/p12 out: the identical sentence 'A second AI check disagreed with the first result for this item.' shown for f_r7_1, f_r7_2, f_r7_3; p3.out.txt lib02 case-next-action 'This item cannot be used. Dismiss it, or write the entry by hand from the record.'; tests/e2e/test_multicase.py:514-529 stubs a reason and never asserts a named record\",\n   \"why_it_matters\": \"She asked 'what do I do first' and still gets two primary buttons with different targets and a sentence that names no record; with the same sentence for three flags she cannot tell the line moved. This was my round-1 major F-3.\",\n   \"fix\": \"Build the line from next_action.item_id with the record number and provider or the amount ('Do this first: Record 4, Capital PT: ...'); make Start review go to the same item as Go to it, or show only one of them.\",\n   \"acceptance_test\": \"e2e on the Rivera sample and lib02: the do-first text contains the record number or provider of the item at next_action.item_id; focus after 'Go to it' and after 'Start review' is the same data-item-id.\"},\n  {\"severity\": \"minor\", \"title\": \"The do-first line disappears while items are still pending\",\n   \"evidence\": \"p12.out.txt: '!! no do-first button with pending (3, 0, 5, True, None)'; p18.out.txt steps 5 to 23 all 'via Start review (no do-first line)' with 18 down to 1 pending\",\n   \"why_it_matters\": \"Once the AI-flagged items are done the block gives no sentence about what comes next, so the line she was told to rely on is absent for most of a review.\",\n   \"fix\": \"When next_action is null and items are pending show 'Do this first: Review the remaining n items' with the same target as Start review.\",\n   \"acceptance_test\": \"e2e: a case with at least one pending item has exactly one do-first line.\"},\n  {\"severity\": \"minor\", \"title\": \"Overview row 'need review' count is higher than the detail's for the same case\",\n   \"evidence\": \"p8.out.txt row 'Delgado v. Hartwell - truck rear-end ... 5 need review | Can export - 6 not reviewed' vs p9.out.txt opened block '3 need review' and header '3 items need review'; p12.out.txt start row '5 need review' vs detail header '2 items need'; server tuple (pending, edits, needs_review, ready, next) = (5, 0, 5, True, 'f_r7_2')\",\n   \"why_it_matters\": \"The same case reads 5 on the overview and 2 in the detail; the number she uses to choose a case is not the number she meets (the error is on the safe side).\",\n   \"fix\": \"Backend returns the open needs-review count (the handoff names hitl.needs_review_open) and the row uses it.\",\n   \"acceptance_test\": \"e2e: after deciding some flagged items, the overview row count equals the count in the opened case's header.\"},\n  {\"severity\": \"minor\", \"title\": \"Case checks say 'Ready to export, n not reviewed' beside the amber 'Can export'; stale step text after everything is decided\",\n   \"evidence\": \"p5.out.txt step 1: chip 'Can export - 13 not reviewed (they stay out of the letter)' and 'Case checks | 7/10 checks passed | 3 need you | Ready to export, 13 not reviewed'; p14.out.txt at 14 of 14: 'Everything decided ... Case checks ... Ready to export | Show | What you need to do: Review the 2 items the AI objected to.'\",\n   \"why_it_matters\": \"'Ready to export' beside unreviewed items is the wording round 1 asked to remove, and a leftover instruction after the case is done makes her doubt the green state.\",\n   \"fix\": \"One phrase in both places ('Can export, n not reviewed'); clear the step's next-action text when nothing is pending.\",\n   \"acceptance_test\": \"e2e: with pending items the page has no 'Ready to export' text; at 0 pending no 'What you need to do' text is visible.\"},\n  {\"severity\": \"minor\", \"title\": \"Row says how many need review but not why; the first do-first items on the sample are a rate and a non-bill, not the accident-date conflict\",\n   \"evidence\": \"p19.out.txt: six untouched rows repeat 'Nothing is accepted or edited yet, so the letter would be empty.' with no kind; p18.out.txt steps 2 to 4 (a2 rate, a3 not a bill, f_r7_1) and f_accident_date_after_treatment_1_2_7 only at step 14; handoff lists the why line as skipped\",\n   \"why_it_matters\": \"Checklist 16: items needing review say why in one sentence, and she cannot rank cases by what the adjuster will attack.\",\n   \"fix\": \"One line under the chips from the server's kinds ('1 date conflict, 1 gap, 2 prior conditions'); rank conflicts and gaps ahead of rate notes in next_action.\",\n   \"acceptance_test\": \"e2e: the Rivera sample row contains 'conflict' and 'gap' counts equal to the flags of those kinds from GET /api/cases/{token}; its first do-first item is a conflict or gap flag.\"},\n  {\"severity\": \"nit\", \"title\": \"Identical derived titles for the same records pasted twice\",\n   \"evidence\": \"p19.out.txt: two rows titled 'Austin EMS run report, Jan 9, 2026'\",\n   \"why_it_matters\": \"Two rows she cannot tell apart until she opens them.\",\n   \"fix\": \"Add the created minute to the title or a 'same title as another case' hint.\",\n   \"acceptance_test\": \"e2e: paste the same text twice; the two overview titles differ.\"},\n  {\"severity\": \"nit\", \"title\": \"Card evidence '36 pass' does not match plain pytest: 35 passed, 1 skipped\",\n   \"evidence\": \"artifacts/review-evidence/T-149-paralegal-r2/pytest-multicase.out.txt: '35 passed, 1 skipped in 20.99s' (skip = the screenshot test needing ZLAYT_SCREENSHOTS=1)\",\n   \"why_it_matters\": \"Evidence should reproduce as written.\",\n   \"fix\": \"State '35 pass, 1 skipped (screenshots)' in the card.\",\n   \"acceptance_test\": \"pytest tests/e2e/test_multicase.py in a clean archive prints no failures.\"}\n ],\n \"whats_right\": [\n  \"Cases get real names: a name field at create, a rename that survives reload, and a default from record 1's provider and date; 'Untitled case' never appeared.\",\n  \"Green appears only at 'Everything decided'; any unreviewed item gives amber 'Can export - n not reviewed (they stay out of the letter)', the Ready to send filter matches, and the letters held only accepted items with cited quotes.\",\n  \"Keyboard flow from the overview (j/k, Enter, Go to it, a, d, e, compare button) took a 23-item case from open to export in 62 seconds.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T15:50:03.839Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-149-paralegal-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:50:05.781Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -5; python3 - <<'EOF'\nimport re,json\nt=open('reviews/T-149-paralegal-r2.md').read()\nm=re.findall(r'```json\\n(.*?)```',t,re.S); print(len(m)); d=json.loads(m[0]); print(d['verdict'],[f['severity'] for f in d['findings']])\nEOF"
}
````

### User / tool · 2026-11-02T15:50:06.076Z

**tool result**
````
ok (166 file(s))
1
changes ['major', 'minor', 'minor', 'minor', 'minor', 'nit', 'nit']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:50:10.962Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t149-r2-overview-patterns.md",
 "content": "---\nname: t149-r2-overview-patterns\ndescription: T-149 r2 (802d5fd): names/amber-green fixed; do-first line names no item and Start review targets a different item; row needs-review count overstated vs detail; Playwright selectors for the overview\nmetadata:\n  type: project\n---\n\n- r2 verdict changes (1 major). Fixed: case names (input-title, rename, default = record-1 provider + date), amber \"Can export - n not reviewed\", green only \"Everything decided\". Open: `do-first` text is the server reason with no record/provider; \"Start review\" and \"Go to it\" land on different items; line absent when next_action is null with items pending; row `needs_review` (server, never falls) > detail count.\n- Selectors (802d5fd): rows `[data-testid=cases-row][data-token=...] [data-testid=cases-open]` (NOT `case-<token>`); `cases-sort`, `cases-filter-*`, `cases-search`, `input-title`, `input-text`, `btn-rename-case`, `case-rename-input`, `case-overview`, `do-first`, `btn-do-first`, `btn-all-cases`, `btn-export`, `export-letter`. j/k/Enter work on the overview. `a` on an edited row opens the compare prompt (focus on btn-accept; press Enter).\n- Letter total wording is now D-062 \"Billed charges accepted from these records: $X\", not D-019; do not flag it.\n- Local mode paste: text with no \"=== Record\" headers returns 409.\n\n**Why:** saves a re-derivation of selectors and the open items on round 3.\n**How to apply:** check do-first text names a record, Start review vs Go to it share a data-item-id, and row vs detail counts after decisions. Related: [[frontend-review-patterns]], [[reviewer-run-pitfalls-pass4]].\n"
}
````

### User / tool · 2026-11-02T15:50:11.063Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t149-r2-overview-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:50:12.715Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-136 r2 / T-142 patterns]",
 "new_string": "- [T-149 r2 overview patterns](t149-r2-overview-patterns.md) — names and amber/green fixed; do-first names no item, Start review differs; overview selectors\n- [T-136 r2 / T-142 patterns]"
}
````

### User / tool · 2026-11-02T15:50:12.832Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:50:15.080Z

Verdict: **changes** (0 blockers, 1 major, 4 minors, 2 nits). Case names and the amber "Can export — n not reviewed" (green only at "Everything decided") are fixed. The "Do this first" line is not: it names no item, and "Start review" goes to a different item than "Go to it". Review is in `/Users/arsis/zlayt-pm-project/reviews/T-149-paralegal-r2.md`, evidence in `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-149-paralegal-r2/`.

I ran 802d5fd on port 7943 (HEAD differs only in four frontend files unrelated to the overview), worked the Delgado and Rivera cases from the overview to export, and stopped the server by PID 1826 (lsof exit 1, curl 000).
