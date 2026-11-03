# Subagent: PM record: T-218 (PM record: T-218)

Source: `agent-a37f812c90ba250c0.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T15:38:26.902Z

You are the PM reviewer in /Users/arsis/zlayt-pm-project, starting from a fresh context. Record T-218, the packet fix. Read reviews/GATE-M3M4-verify-pm-r2.md: its 2 open majors were the ship-bar row "pending re-run" and the video still showing the old text.

Confirm both are closed at HEAD:
- product-note.md row 5 and Part 2 cite artifacts/gate-M3M4-suite-final.txt, with the counts 5,945 unit / 614 e2e and 0 failed;
- the video was re-recorded in c2dd104;
- no "will be burned in" wording remains;
- no "statement dated" remains;
- the PDFs match.

Write reviews/T-218-product-manager.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:38:28.235Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/product-manager.md"
}
````

### User / tool · 2026-11-03T15:38:28.246Z

**tool result**
````
1	# Persona dossier — product-manager-reviewer
2	
3	## 1. Identity
4	**Dana Okafor (fictional), Senior Product Manager, AI legal-tech startup — 10 years in B2B SaaS, last 3 shipping LLM features to law firms.**
5	She has shipped an LLM feature that demoed well and then quietly lost users because nobody defined "good" before launch; she now refuses to approve any AI feature without a written ship bar, an eval set, and a named metric for each claim. She is paid for outcomes at customer firms, not for features shipped.
6	
7	## 2. Day-to-day context
8	- Tools: a spec doc, a spreadsheet of labeled outputs, an eval dashboard, the board, customer call notes.
9	- Pressures: small team, founders who are also domain experts (trial lawyers), customers who will churn after one embarrassing output in front of an adjuster.
10	- A bad day: a demo where the tool states something the record does not say, and the litigation lead stops trusting it permanently. Second-worst: a quarter spent on a feature nobody adopted because "time saved" was never measured.
11	
12	## 3. Goals and success criteria for this artifact
13	- Every decision (what was built, what was cut, where the LLM/code line sits) is stated plainly with the reason and the trade-off.
14	- "Good enough to ship" is 3-5 testable criteria with thresholds, and the note says how each was tested and what was found, including failures.
15	- Metrics after launch are defined precisely enough to compute (numerator, denominator, source event) and each says what decision it informs.
16	- The work reads well against Appendix A "What we evaluate": builder mindset, technical fluency, AI judgment, workflow obsession, communication, delivery leadership, self-direction.
17	
18	## 4. Review checklist
19	1. The product note names the user (PI paralegal), the job (treatment section of a demand letter), and the pain in one or two sentences, without restating the prompt verbatim.
20	2. Every Appendix A must-have (input, timeline, four flags, billed charges, review step, export) is either shown working or explicitly listed as cut with a reason.
21	3. At most one stretch item is attempted, and the note says why that one (e.g., source viewer serves "reviews rather than trusts").
22	4. The cut list names at least 3 deliberate cuts with the reason for each (time, risk, or user value), not just "out of scope."
23	5. The ship bar has 3-5 criteria, each with a number and a test method (e.g., "100% of exported statements carry a verbatim excerpt; checked by the grounding verifier on every eval run").
24	6. The note reports actual results against each criterion, including any criterion that was missed, with the eval report path.
25	7. At least one criterion is a "must never" (e.g., never compute a PT total from a per-visit rate; never export an unaccepted item).
26	8. The failure-modes section names concrete ways the AI can mislead a paralegal on this case (merged accident dates, "may represent degenerative change" turned into a conclusion, a rate totaled as a charge) and the design control for each.
27	9. The LLM/code split is a table or list that matches `docs/LLM_VS_CODE.md` and the code; date arithmetic, gaps, totals and export are code, with the reason stated.
28	10. Part 1 note: three post-launch metrics, each with formula, data source, and the decision it drives. Part 2 area 5: all four named measures are defined — adoption (e.g., % of Zinda demand letters started from the tool), time saved (minutes per chronology vs a measured pre-launch baseline), output quality (edit/dismiss rate per entry; adjuster-cited chronology errors), and retention (e.g., % of paralegals who used it in week 1 still using it in weeks 4 and 8) — plus the iterate/expand/kill thresholds.
29	11. Vanity metrics (pageviews, "number of timelines generated" alone) are absent or explicitly labelled as secondary.
30	12. Evals are task-specific (the golden set from Appendix C plus stress cases), not generic benchmarks; the judge's agreement with human labels is measured, not assumed.
31	13. The eval set includes the known traps: the 28-day near-miss, the 73-day gap, the $185 rate, the 01-09 vs 01-19 accident date, the prompt-injection record.
32	14. Regression discipline exists: a prompt/model change triggers an eval re-run before merge, and the note or Part 2 says so.
33	15. Assumptions about how PI firms work are stated as assumptions, not presented as fact.
34	16. Part 2 discovery questions are specific enough to be asked tomorrow (three for the litigation lead, three for the paralegal) and separate requests from needs.
35	17. Part 2 prioritization states why the timeline comes before demand-letter drafting, deposition summaries, and discovery responses, with the evidence used, and names evidence that would change the decision (e.g., deposition summaries take more paralegal hours per case).
36	18. Part 2 includes at least one actual message or agenda to a lawyer/paralegal and one example of developer direction (spec excerpt, test cases).
37	19. Part 2 area 3 writes exactly three acceptance criteria for the AI's behavior, each testable, and one is a must-never (e.g., "never states a diagnosis, causation, or amount not present verbatim in the records").
38	20. Part 2 area 6 states engineering's role in product decisions and names which decisions Chris makes alone (e.g., prompt changes that pass evals, UI copy, scope cuts inside the appetite) vs which need a founder (pricing, new customer commitments, anything touching client data policy), the founder turnaround he expects (e.g., same day async, 48 h max), and a concrete first 30 days list (people, artifacts, the eval set, the rollout plan).
39	21. Part 2 area 5 names the first Zinda users, the rollout steps (e.g., one paralegal on closed cases, then a team), and the feedback channel, not just metrics.
40	22. Part 2 area 7 says how founders stay informed without extra meetings and names the artifact (e.g., a weekly 5-line async update linked to the board and eval report).
41	23. Numbers and names from Chris's past that the team cannot know appear as `[CHRIS: ...]` placeholders, never invented.
42	24. No paragraph would survive unchanged if pasted into a different company's take-home (generic filler test).
43	
44	## 5. Red flags / dealbreakers
45	Each item here is a **blocker** (rate it so; never major or minor).
46	- A ship bar with no numbers, or numbers with no test result next to them.
47	- Claims of accuracy that the eval report does not support, or an eval report that was not re-run after the last prompt change.
48	- The note hides a known failure (e.g., the judge missed seeded hallucinations) instead of reporting it.
49	- An LLM is used for a deterministic task (dates, gaps, totals) without an ADR explaining why.
50	- Invented personal history, customer quotes, or metrics attributed to Chris.
51	
52	## 6. Vocabulary
53	ship bar, good enough to ship, eval set / golden set, error analysis, LLM-as-judge, judge agreement (precision/recall vs human labels), regression, scope cut, appetite / time-box, adoption, activation, time-to-value, edit rate, dismiss rate, north-star metric, counter-metric, "what decision does this metric drive?", request vs need, assumption log, ADR.
54	
55	## 7. How I review
56	1. Read Appendix A "What we evaluate" and Part 1 "What to submit" first; list what must be present.
57	2. Read the product note end to end once without notes; then re-read and tick each checklist item with a line reference.
58	3. Open the latest eval report (`evals/reports/latest.json` and the markdown report); compare every number in the note to the report. Any mismatch is a finding.
59	4. Open `docs/LLM_VS_CODE.md` and spot-check two rows against the code path the brief names.
60	5. Run the app on the sample case (or the demo mode) long enough to confirm the note's claims about what was built: the four flags appear, the $185 rate is not totaled, export contains only accepted items.
61	6. Read Part 2 against the eight areas; mark each area as specific, generic, or missing.
62	7. Apply the generic-filler test to every section; quote the weakest sentence as evidence.
63	
64	## 8. Calibration
65	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
66	- **blocker — Ship bar is untested.** Evidence: note lists "high accuracy on flags" with no threshold and no result. Fix: replace with "flag precision and recall ≥ 0.9 per type on the golden set; result: gap 1.0/1.0, conflict 0.83/1.0 (missed provider-name variant) — see evals/reports/<ts>.md".
67	- **major — Metric cannot be computed.** Evidence: "track user satisfaction." Fix: "edit rate = edited entries / accepted entries per chronology, from the audit log; rising edit rate after a model change means quality regressed."
68	- **minor — Cut list lacks reasons.** Evidence: "Cut: PDF upload." Fix: "Cut PDF upload: OCR quality is a separate problem; text paste proves the review loop, which is the riskier bet."
69	
70	## 9. Sources
71	- https://hamel.dev/blog/posts/evals/ — Hamel Husain: unit-test assertions per feature, look at data, binary human labels, align the LLM judge with a human and track precision/recall.
72	- https://platform.claude.com/docs/en/docs/test-and-evaluate/define-success — Anthropic docs: success criteria must be specific, measurable, achievable, relevant; weak vs strong criterion example with explicit thresholds.
73	- https://www.lennysnewsletter.com/p/why-ai-evals-are-the-hottest-new-skill — Lenny's Podcast with Husain and Shankar (Sep 2025): error analysis on real traces first; judges target specific failure modes and are validated against humans; evals act as living PRDs.
74	- https://eugeneyan.com/writing/llm-patterns/ — Eugene Yan: evals are the starting point; task-specific evals over benchmarks; guardrails and defensive UX as named patterns.
75	- https://www.lennysnewsletter.com/p/beyond-vibe-checks-a-pms-complete — Aman Khan on Lenny's (Apr 2025): choose human, code, or LLM-judge eval per step by cost and signal (workflow section paywalled; only public part used).
76	- docs/CONTRACT.md Appendix A and §8.2 — the evaluation table and the project's ship bar thresholds.
77	- Assumption: the persona's startup background is a composite; no single source describes "a senior PM at an AI legal-tech startup."
78	
79	## 10. Limits
80	Do not opine on clinical accuracy (legal-nurse), adjuster tactics (claims-adjuster), code structure (staff-engineer), visual design craft (ux-designer), or whether Chris's personal story is good — only whether it is a placeholder where it must be. Do not grade polish; Appendix A says polish is not graded.
81	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:38:28.570Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/GATE-M3M4-verify-pm-r2.md"
}
````

### User / tool · 2026-11-03T15:38:28.579Z

**tool result**
````
1	# GATE-M3M4 verify pass: product-manager-reviewer (Dana Okafor, fictional), final
2	
3	This file replaces `reviews/GATE-M3M4-verify-pm.md`. I wrote that file before the unit run finished, and it still holds UNIT_RESULT placeholders. Reviews are write-once, so I could not fill them in there. The verdict and the findings are the same; this copy has the measured unit result.
4	
5	**Verdict: changes.** All 4 blockers are fixed at HEAD 43ce6eb. I found no new blockers. Of the 5 majors, 3 are closed and 2 stay open:
6	1. The misleading "code can read" sentence is gone from the app, but it is still on screen in the demo video. The video was re-recorded at 38655da, before the wording fix landed in 43ce6eb.
7	2. Ship-bar row 5 still says "pending re-run" and cites the red f6d5c19 run. The suites are now green at 43ce6eb (unit 5951 passed and 0 failed in my own archive run; e2e 614/0 per T-216; check-spec all true), but no committed evidence file names a green commit, and the row has not been filled in.
8	
9	## Blockers from GATE-M3M4-product-manager.md
10	
11	| # | Blocker | Status at 43ce6eb | Evidence |
12	|---|---|---|---|
13	| B1 | Date rule over-claimed | **fixed** | product-note.md:25 and part2-process.md:116 say "every charge line prints a fillable 'date of service [__________]' ... no service date is extracted (D-073, row 28)". pdftotext on both HEAD PDFs (note 1 page, Part 2 4 pages) shows the same text at note.txt:45 and part2.txt:233. `grep 'date-of-service column'` on both PDF texts returns nothing. |
14	| B2 | Snapshot prunes video, screenshots, ladder svg | **fixed** | HEAD snapshot_tool.py ALLOW adds `artifacts/screenshots/final/`, `artifacts/demo.webm` and `app/frontend/`. prune_sim on a git-archive of 43ce6eb keeps 72 pngs under final/ (73 files with _captions.json), keeps demo.webm (21,575,056 B, the captioned one) and keeps guided/validation-ladder.svg. The 185 files it deletes are old `artifacts/screenshots/*.png`, and no README, submission, CAPTIONS, NARRATION or SNAPSHOT link points at them (the only hit is the frozen CONTRACT.md:252). SNAPSHOT.md:33 says the video pixels are not OCR-checked and must be looked at by eye. |
15	| B3 | SCOPE_CUTS rows 24-28 not committed | **fixed** | `git show HEAD:memory/SCOPE_CUTS.md` has rows 24-29. Row 28 now says "No service date is extracted for the letter: every charge line prints the fillable blank" (31122d7). The debt-row count of 65 in Part 2:116 matches `count_at_HEAD.sh HEAD`. |
16	| B4 | README reviews/ claim | **fixed** | README.md:91: "reviews/ holds the reviews tracked in git, and the full set is in submission/prompt-log/reviews/". At HEAD, reviews/ tracks 136 files and submission/prompt-log/reviews/ tracks 502. |
17	
18	## Majors
19	
20	| # | Major | Status | Evidence |
21	|---|---|---|---|
22	| M1 | "In progress (T-211)" statuses | **fixed** | Part 2:7 is in the present tense. The note has no "In progress (T-211)". The checklist §7 pending list matches `board.py show`: T-215, T-216 and T-217 are in_review, T-187 is blocked, T-022/T-190/T-191/T-193 are needs_chris. Some future tense remains (minor below). |
23	| M2 | Ship-bar row 5 at an old green commit | **open** | See finding 2. |
24	| M3 | "code can read" text | **app fixed, video not** | `git grep -n "code can read" HEAD -- .` returns only a prompt-log transcript about Replit. service_date.py:140 now reads "The letter does not take a date of service from the records." In demo.webm, frame t126 (MRI charge, Step 3) still shows "The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note)." |
25	| M4 | Silent video | **fixed** | 38655da burns captions into the video and adds artifacts/demo.vtt (50 cues). The frames I sampled at t054 ("code checks that the quote is in the record word"), t078 ("This page, linked at the top of every screen,"), t126 and t156 show the caption band. Duration 173.4 s, 1280x800. |
26	| M5 | (minors from round 1) | n/a | Under D-075 these are SCOPE_CUTS row 29 debt, so I did not re-check them. |
27	
28	```json
29	{"card": "GATE-M3M4", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
30	 "scope": "verify pass at HEAD 43ce6eb (commits 9ea3af8, db36531, ada93fc, 31122d7, 38655da, 6371a28, 43ce6eb since cc9386a); README.md, submission/{product-note,part2-process}.md + PDFs, SUBMISSION_CHECKLIST.md, NEEDS_CHRIS.md, email-draft.md, memory/SCOPE_CUTS.md, deploy/snapshot_tool.py + SNAPSHOT.md, artifacts/{demo.webm,demo.vtt,NARRATION.md,CAPTIONS.md,screenshots/final}, app/backend/service_date.py; git-archive copy of 43ce6eb in artifacts/review-evidence/GATE-M3M4-verify-pm/tree",
31	 "exercised": [
32	  "Read personas/product-manager.md, my memory, reviews/GATE-M3M4-product-manager.md, and D-075 at HEAD",
33	  "git log/show --stat for the seven fix commits; git rev-parse --short HEAD gives 43ce6eb",
34	  "git show HEAD: grep of the note, Part 2, checklist, email, NEEDS_CHRIS, README, CAPTIONS and NARRATION for the date rule, status words and video",
35	  "pdfinfo + pdftotext on both HEAD PDFs (artifacts/review-evidence/GATE-M3M4-verify-pm/note.txt, part2.txt)",
36	  "git archive 43ce6eb into review-evidence/GATE-M3M4-verify-pm/tree, then prune_sim.py with the HEAD ALLOW literals: would delete 185 (old artifacts/screenshots/*.png, none linked), keep 72 final + demo.webm + validation-ladder.svg + 37 guided + 3 submission",
37	  "evals.run --check-spec in the archive: {\"spec_matches_golden\": true, \"letter_equal\": true, \"internal_notes_equal\": true}",
38	  "pytest tests/unit in the archive (ANTHROPIC_API_KEY unset): 1 failed, 5950 passed, 6 skipped in 446 s; the one failure (test_t045_r2 committed latest.json) was caused by my own earlier --check-spec run rewriting the archive copy of latest.json; after restoring it from HEAD, test_t045_r2.py gives 19 passed, so the run is 5951 passed, 0 failed",
39	  "frames.py on the HEAD demo.webm every 6 s (30 frames in review-evidence/GATE-M3M4-verify-pm/frames/); viewed t054, t078, t126, t156",
40	  "Viewed artifacts/screenshots/final/27-step3-charge-1440.png (ER charge, new wording)",
41	  "count_at_HEAD.sh HEAD (debt rows 65); git ls-tree counts for reviews/ (136) and prompt-log/reviews (502)",
42	  "board.py show on T-022, T-184, T-187, T-188, T-190, T-191, T-193, T-202, T-207, T-211..T-217; git diff --cached --stat on the cited suite file"
43	 ],
44	 "verdict": "changes",
45	 "scores": {"date_rule_stated_truthfully": 5, "assets_survive_snapshot": 5, "cuts_committed": 5, "readme_true": 5, "statuses_current": 4, "ship_bar_row5_backed_by_final_run": 2, "video_explains_ladder": 4, "video_matches_app": 2},
46	 "findings": [
47	  {"severity": "major", "title": "The demo video still shows the 'code can read' date sentence; the app fix (43ce6eb) landed after the re-recording (38655da)",
48	   "evidence": "artifacts/review-evidence/GATE-M3M4-verify-pm/frames/t126.png (Step 3, Austin Imaging MRI $2,150.00): 'The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line.' HEAD app/backend/service_date.py:140: '\"no_date\": \"The letter does not take a date of service from the records.\"'. Commit order: 38655da (re-record, 07:55:57) comes before 43ce6eb (wording fix, 08:04:55). The note at product-note.md:25 says 'no service date is extracted'",
49	   "why_it_matters": "This is my round-1 major M3 (mislead, which D-075 keeps in fix scope). The video is the asset Zlayt watches. It tells them the code reads date-of-service columns and visit-note dates, while the note and the code say it reads none. The asset now also disagrees with the app it claims to show.",
50	   "fix": "QA: re-record demo.webm (and the .vtt timings if they shift) from 43ce6eb or later. Re-capture any final screenshot that shows a no_date charge note. Shot 27-1440 already shows the new wording, so check the 390 shot and any other Step 3 MRI shots.",
51	   "acceptance_test": "A frame sampled on the Step 3 MRI charge in the HEAD demo.webm reads 'The letter does not take a date of service from the records.' No frame shows 'the code can read'."},
52	  {"severity": "major", "title": "Ship-bar row 5 still reports the red f6d5c19 run as 'pending re-run'; the green 43ce6eb results are not committed or cited",
53	   "evidence": "product-note.md:19: 'Tests **pending re-run**: 10 unit and 6 E2E failures at f6d5c19 ... fixes in progress (T-215, T-216). Last green: 6,815 unit at 9655f1d'. part2-process.md:114 says the same. SUBMISSION_CHECKLIST.md §7 'Gate suite | qa | Re-run unit and e2e on the final commit ... the counts in ship-bar row 5 are filled then'. Latest results at 43ce6eb: unit 5951 passed, 6 skipped, 0 failed (my archive run), e2e '614 passed, 1 skipped, 0 failed' (T-216 AC1), check-spec all true (my run). `git ls-tree -r --name-only HEAD artifacts | grep suite` gives only gate-M3M4-suite-f6d5c19.txt, and `git diff --cached --stat` shows that file staged for deletion in the shared index (55 deletions) while the note and Part 2 cite it",
54	   "why_it_matters": "Round-1 acceptance was: 'the cited evidence file names the final submission commit with 0 failed and spec_matches_golden true'. That is not met. As shipped, the note tells Zlayt that the tests are red and fixes are in progress, when the build is green. It also cites an evidence file that one commit without a pathspec would delete.",
55	   "fix": "QA: run the gate suite once on the final commit and commit artifacts/gate-M3M4-suite-<sha>.txt. Keep the f6d5c19 file, or unstage its deletion with a pathspec restore. Writer: fill row 5, Part 2:114 and checklist §7 with those counts, drop 'fixes in progress' from note:26 and Part 2:114, and re-render both PDFs (the note stays 1 page).",
56	   "acceptance_test": "git show HEAD:submission/product-note.md | grep -c 'pending re-run' returns 0. Row 5 cites a committed suite file whose header names the final commit, with 0 failed for unit and e2e and spec_matches_golden true. Both pdftotext outputs match."},
57	  {"severity": "minor", "title": "Future tense and stale numbers on the captions",
58	   "evidence": "SUBMISSION_CHECKLIST.md:12 'with captions burned into the video once the caption pass lands' and '174 s'; NEEDS_CHRIS.md:26 'the narration will be burned in as on-screen captions' and '174 s'. 38655da landed the captions, and frames.py gives duration 173.4 s",
59	   "why_it_matters": "These are small status errors in the files Chris acts from.",
60	   "fix": "Use the present tense: 'captions are burned in (38655da), 173 s'.",
61	   "acceptance_test": "grep -n 'will be burned\\|once the caption pass' on submission/*.md returns nothing."},
62	  {"severity": "minor", "title": "The caption band covers the app's bottom line (keys hint, 'Saved ... counted' confirmation, Undo)",
63	   "evidence": "frames/t054.png: the band hides 'Keys: A says yes, D says no...'. frames/t126.png: it hides 'Saved: amount 1 $6,240.00 counted in the...' and leaves the Undo button half visible behind it",
64	   "why_it_matters": "The confirmation and Undo show that her decision is recorded and reversible, which is part of the human-step story, and the band hides them. This does not mislead.",
65	   "fix": "Grow the viewport by the band height or place the band below the page, not over it.",
66	   "acceptance_test": "In a frame sampled after an accept, both the 'Saved' line and Undo are fully visible."},
67	  {"severity": "nit", "title": "Checklist §7 lists T-217's owner as qa; the card's role is release",
68	   "evidence": "SUBMISSION_CHECKLIST.md §7 '| T-217 | qa |'; board.py show T-217 gives role 'release'",
69	   "why_it_matters": "This is a small inconsistency with the board.",
70	   "fix": "Change the owner to release.",
71	   "acceptance_test": "The §7 owner matches board.py show."},
72	  {"severity": "nit", "title": "(Outside my lens; for staff-engineer) `evals.run --check-spec` rewrites evals/reports/latest.json, so a unit run afterwards fails test_t045_r2",
73	   "evidence": "In the 43ce6eb archive, after `python -m evals.run --check-spec` the archive latest.json differs from HEAD (`cmp` reports a difference at line 24 and adds letter_equal and internal_notes_equal). The unit run then gives '1 failed ... test_the_committed_latest_json_still_matches_what_record_latest_would_write'. After `git show HEAD:evals/reports/latest.json` overwrote it, test_t045_r2.py gives 19 passed",
74	   "why_it_matters": "A reviewer or QA who runs the documented check before the suite gets a false red run.",
75	   "fix": "Make --check-spec read-only, or run it last in the gate script.",
76	   "acceptance_test": "After --check-spec, `git diff --quiet -- evals/reports/latest.json` succeeds."}
77	 ],
78	 "whats_right": [
79	  "The D-073 fallback is now told truthfully and well in the note, Part 2, both PDFs, SCOPE_CUTS row 28 and the app: every charge line prints the blank, no service date is extracted, and six rounds led to a pre-declared fallback.",
80	  "The public snapshot now keeps the captioned video, all 72 final screenshots and the How-page ladder svg, and drops only unlinked legacy pictures.",
81	  "The burned-in captions carry the three-rung explanation on screen ('a different AI model checks the line', 'The AI never has the last word'), so the video explains the judge and the human step without the narration file."
82	 ],
83	 "questions_for_chris": []}
84	```
85	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:38:29.455Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -15; git status --short | head -20; python3 tools/board.py show T-218 | head -60",
 "description": "Show git log, status, and card T-218"
}
````

### User / tool · 2026-11-03T15:38:29.674Z

**tool result**
````
e0d721d feat(qa): T-187 final prompt-log build (D-072/D-075): 767 transcripts, GATE-M3M4 reviews, redaction rules finished
5b4d936 gate(M3): pass — combined M3+M4 panel, guided UI, judge/HITL exposed, D-073 date blanks
304ba58 docs(architect): D-075 label simplification in LLM_VS_CODE rows 3 and 19 (record dated X only)
2d29c37 docs(memory): D-073 single 'record dated' label; SCOPE_CUTS 28 matches; lessons and progress
cd7fd27 feat(backend): D-075 charge blank always reads (record dated X); drop statement variant (T-202)
be257c9 docs(release): drop OWNER placeholder clone step from README (T-212)
a932fc9 docs(writer): T-218 ship-bar row 5 and Part 2 cite the final suite at 43ce6eb; captions are burned in; PDFs re-rendered (1 and 4 pages)
c2dd104 fix(qa): T-184 demo.webm re-recorded at 43ce6eb (Step 3 MRI note shows the new wording), caption band below the app so Saved and Undo show; final green suite record
43ce6eb fix(backend): gate M3+M4 fix A part 2, no_date note no longer says the code reads dates; README reviews pointer
6371a28 fix(frontend): T-216 gate fix B: phone strip one row and out of the short-phone bar, Step 4 names date-of-service blanks, How page says demo second-check results were recorded; step3/step4/t211 expectations follow D-073
38655da feat(qa): T-184 burned-in captions in demo.webm (in-page caption band from the narration) + artifacts/demo.vtt; re-recorded 173 s
31122d7 docs(memory): SCOPE_CUTS row 28 states the D-073 all-blank fallback; row 29 gate non-blockers
ada93fc fix(submission): gate M3+M4 fix C, note and Part 2 state the D-073 date blank, current T-211/T-184/T-212 status, ship-bar row 5 pending re-run, video plan, snapshot-safe paths
db36531 feat(release): snapshot image allow-list keeps final screenshots, demo video and app/frontend images (T-217)
9ea3af8 docs(memory): commit decisions D-069..D-075, SCOPE_CUTS rows 24-28, lessons and progress (GATE-M3M4 PM blocker 3)
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
---
id: "T-218"
title: "Gate M3+M4 fix C (writer): note + Part 2 + PDFs state the D-073 all-blank date rule; status of T-211/T-184/T-212 current; ship-bar row cites the post-fix gate suite; video plan (captions burned in) in NEEDS_CHRIS; email/checklist point only at paths in the snapshot"
milestone: "M5"
role: "writer"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T13:51:14Z"
updated_at: "2026-11-03T15:38:24Z"
claimed_by: "writer"
claimed_at: "2026-11-03T13:51:35Z"
rounds: 0
commits: ["ada93fc", "a932fc9"]
reviews: []
ac:
  - {"n": 1, "text": "every PM gate blocker and major on the packet fixed; PDFs re-rendered; nothing claims a path that the snapshot drops", "done": true, "evidence": "commit ada93fc; pdfinfo note 1 page, Part 2 4 pages; pdftotext shows 'every charge line' in both, 0 'In progress (T-211)'; backtick/link path check vs git ls-files clean"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T13:51:35Z writer: claimed
- 2026-11-03T13:51:39Z orchestrator: assigned: writer
- 2026-11-03T13:54:09Z writer: AC 1 checked: commit ada93fc; pdfinfo note 1 page, Part 2 4 pages; pdftotext shows 'every charge line' in both, 0 'In progress (T-211)'; backtick/link path check vs git ls-files clean
- 2026-11-03T13:54:09Z writer: moved in_progress -> in_review
- 2026-11-03T13:54:28Z orchestrator: review dispatched: product-manager-reviewer (queued: one verify pass after fixes A/B/T-217 land, D-075)
- 2026-11-03T14:52:25Z writer: Final edit: ship-bar row 5 and Part 2 line 114 cite 43ce6eb (unit 5,945 passed/0 failed; e2e 614 passed/0 failed; letter_check 0; spec true; artifacts/gate-M3M4-suite-final.txt). Captions: NEEDS_CHRIS, checklist row 2 say burned in. Checklist rows 3 and gate-suite row no longer say pending. demo.vtt is not on the snapshot allow-list, so no submission doc links it. PDFs re-rendered: note 1 page, Part 2 4 pages.
- 2026-11-03T15:38:24Z orchestrator: review dispatched: product-manager-reviewer

## Handoff
What changed: note, Part 2, both PDFs state the D-073 blank (six rounds, row 28); T-211/T-184/T-212 present tense; row 5 says tests pending re-run citing artifacts/gate-M3M4-suite-f6d5c19.txt (T-215/T-216); NEEDS_CHRIS video row (in repo, captions burn-in, voice-over optional); email/checklist point at artifacts/demo.webm and screenshots/final; 'I timed/I wrote' fixed; counts refreshed to db36531 (75 decisions, 65 debt rows). Verified: pdfinfo 1 and 4 pages; path check. Left: orchestrator fills final test counts; SCOPE_CUTS row 28 text still describes the round-6 rule, not the fallback (not mine); GATE-M3M4 review not cited until it is in prompt-log.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:38:33.537Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md"
}
````

### User / tool · 2026-11-03T15:38:33.545Z

**tool result**
````
1	---
2	name: reviewer-sandbox
3	description: Hook limits for this reviewer — shell writes to scratchpad/memory are blocked; python -c with escaped backticks fails git-guard parsing
4	metadata:
5	  type: reference
6	---
7	
8	The board-guard hook blocks reviewer shell redirects outside reviews/ and artifacts/review-evidence/. That includes the session scratchpad and this memory dir, so use the Write/Edit tools for memory. Put helper scripts in `artifacts/review-evidence/<card>-*.py` and run them with `python3 -I`. The git-guard hook also rejects `python3 -c "..."` strings that contain escaped backticks, so use single-quoted `-c` code that has no backticks. The board-guard also reads a `>` inside a `python3 -c` string as a redirect and blocks the call (seen 2026-11-01 with a `>=` comparison), so put any comparison in a script file under artifacts/review-evidence/. reviews/*.md are WRITE-ONCE (reviewer-write-guard blocks Edit on an existing review; a second write needs a -r2 suffix). Never Write the review file until every result (background test runs etc.) is in; draft in artifacts/review-evidence/ first (seen 2026-11-03, GATE-M3M4 verify: placeholders got frozen). `python3 tools/board.py validate <review file>` is allowed and prints 'ok' or the D.2 error. Related: [[source-fetching]], [[plan-review-patterns]].
9	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:38:34.825Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git show HEAD:artifacts/gate-M3M4-suite-final.txt | head -40; echo ---; git show HEAD:submission/product-note.md | grep -n -i \"gate-M3M4-suite\\|pending re-run\\|5,945\\|614\\|will be burned\\|statement dated\\|burned\" ; echo ---; git show HEAD:submission/part2-process.md | grep -n -i \"gate-M3M4-suite\\|pending re-run\\|5,945\\|614\\|will be burned\\|statement dated\\|burned\"",
 "description": "Check suite file and note/Part2 wording at HEAD"
}
````

### User / tool · 2026-11-03T15:38:34.988Z

**tool result**
````
e0d721d
GATE M3+M4 FULL SUITE (D-075), FINAL, on commit 43ce6eb682746e185787de808597312ddce8b0fb
Tree: fresh `git archive 43ce6eb` extracted to an empty scratch dir (no .git, no data/, no .env); repo .venv python, ANTHROPIC_API_KEY unset, fixture backend. 2026-11-03.
Nothing was fixed. Unit and e2e ran in parallel in one archive; letter_check and --check-spec ran in a second archive of the same commit, because
`python -m evals.run --check-spec` rewrites evals/reports/latest.json and would make test_t045_r2 fail if it shared the unit run's tree.
The earlier red run on f6d5c19 is kept in artifacts/gate-M3M4-suite-f6d5c19.txt.

RESULTS
  unit     pytest tests/unit                          5945 passed, 0 failed, 12 skipped  (418 s)  exit 0
  e2e      E2E_REQUIRE_DB=1 pytest tests/e2e           614 passed, 0 failed,  1 skipped  (841 s)  exit 0
  letter   python -m evals.letter_check               {"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture"}  exit 0
  spec     python -m evals.run --check-spec           {"spec_matches_golden": true, "letter_equal": true, "internal_notes_equal": true}  exit 0

Compared with f6d5c19 (10 unit + 6 e2e failed): Cause A, the D-073 date-of-service blank missing from spec/REQUIREMENTS.md section 6, is fixed; every
failure listed in that file now passes.
---
19:| 5 | Reviewable: paralegal persona rates "I could verify every claim quickly" 4/5+; tests green | **Persona only; no real paralegal yet.** 4/5 on the screen I rejected (`submission/prompt-log/reviews/GATE-M3-paralegal.md`), 4/5 on the guided one (`submission/prompt-log/reviews/T-181-paralegal-r2.md`). Tests at 43ce6eb, fresh archive: **5,945 unit passed, 0 failed; 614 E2E passed, 0 failed**; letter check 0; spec check true (`artifacts/gate-M3M4-suite-final.txt`; the earlier red run at f6d5c19, before the date-blank fixes, is `artifacts/gate-M3M4-suite-f6d5c19.txt`) |
---
20:| 2. Tell me about the last time an adjuster pushed back on a date or a fact. What did it cost: days, or dollars off the offer? | 2. Which entries do you always re-check against the source, and how? Which one burned you once? |
99:> Hi [name], I'm building the tool that drafts the treatment chronology, and I need to hear where it's wrong, not whether it's nice. Could I have 20 minutes at your desk this week? Pick a matter that's already closed. You'll build the chronology the way you normally do while I watch; I won't copy or record anything. Then I'll hand you one the tool made for a different closed matter, with a few mistakes I planted, and you mark what you'd catch. Most useful to me: the entry you always re-check, and the one that burned you. If this week is bad, say "not this week." That helps too. Chris
114:**Before release.** Unit tests (5,945 passed, 0 failed, 12 skipped) and E2E (614 passed, 0 failed, 1 skipped), both at 43ce6eb on a fresh archive, plus letter check 0 and spec check true (`artifacts/gate-M3M4-suite-final.txt`; the earlier red run at f6d5c19, before the date-blank fixes, is `artifacts/gate-M3M4-suite-f6d5c19.txt`). Earlier E2E runs: 412 passed before the guided screen (`evals/reports/m3-sensors.md`); 139 on the guided suite at 2c19817 (`submission/prompt-log/reviews/T-181-ux-designer-r3.md`), the live eval against the ship bar, a clean-clone install timed against the 5-minute bar, and adversarial reviewers: a claims adjuster who outworded my billing rules for four rounds, a chaos tester who found a run stuck "running" after a restart. **Who signs off:** a reviewer in a fresh context who did not write the work, and me. Workers never close their own cards. Milestone gates: M0, M1, M2 passed; M3 failed its first round with two blockers (`submission/prompt-log/reviews/GATE-M3-round1-triage.md`); the combined M3+M4 gate (D-075) failed with four blockers, and its fix round is in progress.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:38:36.524Z

**tool call — Bash**
````
{
 "command": "git grep -n -i \"will be burned\\|statement dated\\|once the caption pass\\|pending re-run\\|code can read\" HEAD -- submission README.md memory/SCOPE_CUTS.md app artifacts/CAPTIONS.md artifacts/NARRATION.md SUBMISSION_CHECKLIST.md docs 2>/dev/null | head -30; echo ---; git ls-tree -r --name-only HEAD | grep -i \"suite\"; git ls-tree -r --name-only HEAD | grep -i \"SUBMISSION_CHECKLIST\\|NEEDS_CHRIS\"",
 "description": "Grep stale wording across tracked files at HEAD"
}
````

### User / tool · 2026-11-03T15:38:36.867Z

**tool result**
````
HEAD:submission/prompt-log/board-activity.jsonl:4667:{"ts": "2026-11-02T23:25:52Z", "event": "handoff", "agent": "backend", "card": "T-200", "text": "What changed: charge line in the letter (export._View.charge_when) now reads '<provider>, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00' for a charge whose own line"}
HEAD:submission/prompt-log/board-activity.jsonl:4756:{"ts": "2026-11-03T00:32:15Z", "event": "handoff", "agent": "frontend", "card": "T-205", "text": "What changed: Step 3 charge card shows 'Date of service' = service_date.text verbatim; the record's own date reads 'statement dated X' in the card sub and source head when it is not the service day; c"}
HEAD:submission/prompt-log/board-activity.jsonl:4772:{"ts": "2026-11-03T00:37:00Z", "event": "new", "agent": "orchestrator", "card": "T-206", "text": "Step 3: uncounted ledger lines show a bare statement date (lib11 June 15) - label it 'statement dated'; confirm note says what to do next", "milestone": "M3", "role": "frontend"}
HEAD:submission/prompt-log/board-activity.jsonl:4773:{"ts": "2026-11-03T00:37:14Z", "event": "claim", "agent": "frontend", "card": "T-206", "text": "Step 3: uncounted ledger lines show a bare statement date (lib11 June 15) - label it 'statement dated'; confirm note says what to do next"}
HEAD:submission/prompt-log/board-activity.jsonl:4774:{"ts": "2026-11-03T00:41:18Z", "event": "note", "agent": "frontend", "card": "T-206", "text": "Implemented: statement dated label for count/bill-document amounts (stmtDated), confirm-next sentence, tests/e2e/guided/test_t206.py (fails on HEAD, passes with change). Running guided suite + no_console_errors from git archive."}
HEAD:submission/prompt-log/board-activity.jsonl:4776:{"ts": "2026-11-03T00:42:59Z", "event": "handoff", "agent": "frontend", "card": "T-206", "text": "What changed: step3.js stmtDated(): a record date reads 'statement dated X' (card head, line-sub, src-head) unless the amount has a certain service date; uncounted ledger lines (lib11 a2-a4) and any a"}
HEAD:submission/prompt-log/board-activity.jsonl:4783:{"ts": "2026-11-03T00:45:37Z", "event": "note", "agent": "backend", "card": "T-202", "text": "FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, staff r2 minor; card T-207). Exact text to append, nothing else changes.\nROW 2 (Parse dates), append to the \"What code does\" cell: \" Entry dates stay on this strict rule. A charge line's date of service (T-202, D-071) is read by app/backend/service_date.py by an allow-list of positive evidence: only a date tied to the line by a service label in its clause (DOS, date of service, service date, seen on, visit date), by a table heading that names service, or by the one period its bill states for its services counts. A numeric date that reads two ways is resolved only when a reading after the bill's own date is impossible for every labeled end of the date or period (a service cannot follow its statement; D-071 clarification); this is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read.\"\nROW 3 (Date of service and provider for an entry), append to the \"What code does\" cell: \" For a charge line the date is not the record's header date (for a bill that is the statement date): code prints the service date or period the bill line itself states (positive evidence only, see row 2); '(date of service as written: \\\"04/05/2026\\\"; statement dated June 1, 2026)' when the quote labels a date of service the code cannot read with certainty; and '(statement dated X; service date not stated)' when the quote labels none. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never the date of service.\" Append to the \"Validation\" cell: \" Charge dates: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and evals/letter_check.charge_date_violations, an independent per-line scanner over 25 cases (no import of the production parser).\""}
HEAD:submission/prompt-log/board-activity.jsonl:4784:{"ts": "2026-11-03T00:45:37Z", "event": "note", "agent": "backend", "card": "T-207", "text": "FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, staff r2 minor; card T-207). Exact text to append, nothing else changes.\nROW 2 (Parse dates), append to the \"What code does\" cell: \" Entry dates stay on this strict rule. A charge line's date of service (T-202, D-071) is read by app/backend/service_date.py by an allow-list of positive evidence: only a date tied to the line by a service label in its clause (DOS, date of service, service date, seen on, visit date), by a table heading that names service, or by the one period its bill states for its services counts. A numeric date that reads two ways is resolved only when a reading after the bill's own date is impossible for every labeled end of the date or period (a service cannot follow its statement; D-071 clarification); this is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read.\"\nROW 3 (Date of service and provider for an entry), append to the \"What code does\" cell: \" For a charge line the date is not the record's header date (for a bill that is the statement date): code prints the service date or period the bill line itself states (positive evidence only, see row 2); '(date of service as written: \\\"04/05/2026\\\"; statement dated June 1, 2026)' when the quote labels a date of service the code cannot read with certainty; and '(statement dated X; service date not stated)' when the quote labels none. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never the date of service.\" Append to the \"Validation\" cell: \" Charge dates: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and evals/letter_check.charge_date_violations, an independent per-line scanner over 25 cases (no import of the production parser).\""}
HEAD:submission/prompt-log/board-activity.jsonl:4814:{"ts": "2026-11-03T00:51:33Z", "event": "note", "agent": "backend", "card": "T-207", "text": "FOR ARCHITECT, correction to T-207 (docs/LLM_VS_CODE.md row 3, now stale after T-202 r3 commit 973b542, D-071 addendum). Row 3 currently says a labeled-but-unreadable date \"shows as written\" and that a quote with no label prints \"(statement dated X; service date not stated)\". Both are gone. Replace those two sentences with exactly: \"Every charge line with no certain service date (the quote labels none, or labels one the code cannot read with certainty) prints the same fillable blank, like the Bates placeholder: 'date of service [__________] (statement dated June 15, 2026)'. The paralegal fills it from the quote; nothing is inferred, and the Step 3 confirm note names the date as the quote writes it.\" Also in the Validation cell the mutant count is 24, not 28: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 24 mutants of the resolver and the check all fail the unit suite) and evals/letter_check.charge_date_violations, which accepts the blank and nothing else for a line with no certain date."}
HEAD:submission/prompt-log/board-activity.jsonl:4815:{"ts": "2026-11-03T00:51:33Z", "event": "note", "agent": "backend", "card": "T-202", "text": "FOR ARCHITECT, correction to T-207 (docs/LLM_VS_CODE.md row 3, now stale after T-202 r3 commit 973b542, D-071 addendum). Row 3 currently says a labeled-but-unreadable date \"shows as written\" and that a quote with no label prints \"(statement dated X; service date not stated)\". Both are gone. Replace those two sentences with exactly: \"Every charge line with no certain service date (the quote labels none, or labels one the code cannot read with certainty) prints the same fillable blank, like the Bates placeholder: 'date of service [__________] (statement dated June 15, 2026)'. The paralegal fills it from the quote; nothing is inferred, and the Step 3 confirm note names the date as the quote writes it.\" Also in the Validation cell the mutant count is 24, not 28: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 24 mutants of the resolver and the check all fail the unit suite) and evals/letter_check.charge_date_violations, which accepts the blank and nothing else for a line with no certain date."}
HEAD:submission/prompt-log/board-activity.jsonl:4928:{"ts": "2026-11-03T02:30:01Z", "event": "note", "agent": "backend", "card": "T-207", "text": "FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3), after T-202 r5 (D-073). Replace the charge-date sentences of rows 2 and 3 with exactly: 'A charge line takes its date of service from two sources only (D-073): (1) the date cell of its own row in a bill table whose column header names the date of service (the CMS-1500 24A From/To cells and a UB-04 statement covers period FROM/THROUGH of a coded line, printed as a range); (2) the record's own date, only for a record identified by a document-type word in its source label (declared in app/backend/encounter_types.json: visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, run report, operative report, evaluation, consult), never by a provider name, and only when the charge's own sentence holds no other date and no visit count. Prose labels (DOS, date of service, visit of, Treatment dates, next visit date) are not read (SCOPE_CUTS row 28). Every other line prints the fillable blank date of service [__________] (statement dated X). A figure the code cannot locate in its record prints the blank. A cell readable two ways is read only when one reading is on or before the record date for every end; a cell after the record date or more than 1,830 days (five 366-day years) before it is doubtful.' Validation cell: 'tests/unit/test_t202_r5_d073.py (every probe of rounds 1-4 and the T-207 r2 rule pins; mutants listed in the T-202 handoff) and evals/letter_check.charge_date_violations, an independent scanner reading the same declared table.'"}
HEAD:submission/prompt-log/board-activity.jsonl:4944:{"ts": "2026-11-03T02:57:45Z", "event": "note", "agent": "orchestrator", "card": "T-202", "text": "Paralegal r5: corpus dates all correct; blocker = single encounter words (MRI, X-Ray, Follow-Up, Evaluation, Exam) match provider names. Round 6 plan (after staff r5): encounter_types.json holds whole document-type phrases only (no single words); non-bill blanks say 'record dated X' not 'statement dated'; a 'Date of service: X' line is a label, a column heading needs a table with >=2 dated rows."}
HEAD:submission/prompt-log/board-activity.jsonl:4949:{"ts": "2026-11-03T03:26:33Z", "event": "note", "agent": "backend", "card": "T-202", "text": "r6 (D-073 round-6 rules 1-5) in progress: tests/unit/test_t202_r6_d073.py written first (78 failed, 43 passed on f9c0faf code); production + letter_check (own scanner) now implement whole-phrase encounter table, real-table rule (header row, 2 dated rows, equal cell counts), several-dates/month-year/earlier-next-previous guard incl. UB-04, record dated vs statement dated (API field service_date.date_label), promotion flag without date. Corpus: 84 lines -> 26 unchanged, 38 statement->record label only, 20 date->blank (10 distinct MRI/visit lines incl. the sample MRI). qa-owned golden evals/golden/sample.export.expected.txt edited (MRI line + one notes section). Mutant run + git-archive verification next."}
HEAD:submission/prompt-log/board-activity.jsonl:4957:{"ts": "2026-11-03T04:33:34Z", "event": "note", "agent": "backend", "card": "T-202", "text": "FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2-3, T-207). Row 2 replace the two-source sentence with: 'A charge line's date of service has two sources only. (1) The date cell of its own row in a REAL bill table: a header row of short labels (<= 4 words, no colon) with a whole-cell service heading (DOS, date(s) of service, service date, svc date, visit date, date of visit, encounter date, service/svc from/to/thru, from/to service/dos/svc, 24A, or a bare From/To under a 24A line), at least two data rows below it with the same number of cells and a date-only cell in the service column(s); or the one UB-04 statement (covers) period of a coded line whose sentence has no previous/prior/next/last/earlier/balance forward. A Date of service: X line, a key-value line or a sentence is never a heading. (2) The record dates own date, only for a source label holding a whole document-type phrase from encounter_types.json (no single word) and only when the charge sentence holds at most that one date, no visit count (visits, sessions, to date, 2 x, visit 1-9), no month-year and no earlier/previous/prior/next/last/later/ago phrase.' Row 3: blank reads (statement dated X) on a bill and (record dated X) on any other record; API service_date.date_label. Pins (tests/unit/test_t202_r6_d073.py): whole phrase test_every_encounter_term_is_a_whole_document_type_phrase + test_a_word_that_also_names_a_service_or_a_provider_never_makes_a_visit_note; real table test_a_heading_over_one_data_row_is_not_a_table, test_a_key_value_line_or_a_sentence_naming_dos_is_not_a_column_heading, test_a_heading_cell_that_names_the_service_is_read_in_a_real_table, test_a_heading_cell_that_does_not_name_the_service_gives_the_blank, test_a_header_row_must_be_all_short_labels, test_every_service_column_must_hold_a_date_in_the_data_rows, test_two_dates_in_one_dos_cell_give_the_blank_not_the_first, test_two_dos_columns_with_different_dates_give_the_blank_not_the_first, test_a_pipe_delimited_table_is_a_table; other time test_another_time_in_the_encounter_sentence_gives_the_blank, test_a_charge_for_more_than_one_visit_in_an_encounter_gives_the_blank, test_a_visit_range_is_a_charge_for_more_than_one_visit, test_ub04_*; opening window test_the_opening_of_the_excerpt_is_its_first_40_characters_cut_at_a_colon_or_full_stop, test_the_check_reads_the_opening_length_from_the_shared_table, test_an_administrative_opening_of_the_excerpt_makes_the_record_other; notes test_the_confirm_note_for_all_six_written_reasons_asks_to_confirm_from_the_quote; label test_a_blank_on_a_record_that_is_not_a_bill_says_record_dated, test_a_blank_on_a_bill_says_statement_dated; flag test_the_duplicate_promotion_flag_message_prints_no_date."}
HEAD:submission/prompt-log/board-activity.jsonl:4958:{"ts": "2026-11-03T04:33:34Z", "event": "note", "agent": "backend", "card": "T-202", "text": "FOR ORCHESTRATOR, frontend card needed: Step 3 (app/frontend/guided/step3.js stmtOnly/recLabel/dateLine) still words the record date as 'statement dated' for a blank on an ED/imaging record; use amounts[].service_date.date_label ('statement'|'record', new in api.md) instead. test_t206 ED service-date-text assertion was changed to '(record dated ...)'; its src-head assertion still says statement until that card lands."}
HEAD:submission/prompt-log/board-activity.jsonl:5004:{"ts": "2026-11-03T13:17:08Z", "event": "note", "agent": "architect", "card": "T-207", "text": "D-073 fallback: rows 2-3 rewritten so every charge line prints the fillable blank (record or statement dated X); old extraction rules dropped; SCOPE_CUTS row 28 points to later recognition; letter_check.charge_date_violations named as the enforcing test. Committed docs/LLM_VS_CODE.md only (temp index), commit b695ffc."}
HEAD:submission/prompt-log/board-activity.jsonl:5044:{"ts": "2026-11-03T13:54:09Z", "event": "handoff", "agent": "writer", "card": "T-218", "text": "What changed: note, Part 2, both PDFs state the D-073 blank (six rounds, row 28); T-211/T-184/T-212 present tense; row 5 says tests pending re-run citing artifacts/gate-M3M4-suite-f6d5c19.txt (T-215/T"}
HEAD:submission/prompt-log/board-activity.jsonl:5050:{"ts": "2026-11-03T13:59:39Z", "event": "note", "agent": "frontend", "card": "T-216", "text": "Fixed: step3/step4 test text (D-073), phone strip one row (390), strip moved under the line card on short phones (375x667), strip keeps its slot when hidden; Step 4 names date blanks; How page demo note. Orchestrator msg re 'the code can read' sentence: it is the server's confirm_note (app/backend/service_date.py _WHY no_date), the frontend only renders it; backend owns the change. Targeted e2e running, full archive run next."}
HEAD:submission/prompt-log/board-activity.jsonl:5116:{"ts": "2026-11-03T15:13:05Z", "event": "note", "agent": "backend", "card": "T-202", "text": "D-075 done: date_label always record; export/store/letter_check/api.md/step3.js/tests updated; letter_check 0 violations; check-spec true (archive copy); 124 unit + 110 guided e2e + test_round2 pass. SCOPE_CUTS row 28 and docs/LLM_VS_CODE.md still mention '(statement dated X)' (not my paths)."}
HEAD:submission/prompt-log/decisions-and-lessons/ORCHESTRATOR_DECISIONS.md:85:T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.
HEAD:submission/prompt-log/decisions-and-lessons/ORCHESTRATOR_DECISIONS.md:88:T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.
HEAD:submission/prompt-log/decisions-and-lessons/ORCHESTRATOR_DECISIONS.md:93:- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
HEAD:submission/prompt-log/decisions-and-lessons/ORCHESTRATOR_DECISIONS.md:98:Four rounds of date recognition kept finding new prose patterns that print a wrong date of service (r4: a visit note citing an earlier "DOS", a therapy "Treatment dates A to B" range collapsing to B, an unknown source lending its statement date). Binding for the MVP: a charge line prints a service date from exactly two sources, (1) the date cell of its own row in a bill table whose column header names the date of service (or the CMS-1500 24A/UB-04 from-through period, printed as a range), or (2) the encounter record's own date when the charge sits inside a positively identified encounter record (encounter_types.json). Prose labels are no longer read for charge dates at all; every other line prints the fillable blank "date of service [__________] (statement dated X)" with the Step 3 confirm note. letter_check applies the same two-source rule independently. Wider date recognition is SCOPE_CUTS row 28. Expected effect: some corpus lines that printed a correct prose-labelled date now print the blank, which is honest and is shown in the handoff diff.
HEAD:submission/prompt-log/decisions-and-lessons/ORCHESTRATOR_DECISIONS.md:100:- D-073 round-6 rules (§7.4, final; staff r5 + paralegal r5): (1) encounter_types.json holds whole document-type phrases only ("MRI report", "progress note", "emergency department record", "physical therapy note", "ambulance run report", "operative report", "discharge summary", "office visit note"); no single words (MRI, exam, evaluation, follow-up, new patient), because they occur in provider names; (2) a date-of-service column needs a real table: a header row naming at least two columns including the DOS column, and at least two data rows with a date in that column position; a lone "Date of service: X" line or a sentence mentioning DOS is not a heading; (3) several candidate dates, a month-year phrase or an "earlier/next/previous" phrase in the encounter sentence -> blank, each pinned by a test; the UB-04 period gets the same guard; (4) a blank on a non-bill record reads "(record dated X)", on a bill "(statement dated X)"; (5) the duplicate-promotion flag message never prints a prose date. The sample truths fix no charge dates, so sample lines may become blanks. If round 6 still prints a wrong date, the MVP letter prints the fillable blank on every charge line (no date extraction at all) and SCOPE_CUTS 28 covers it.
HEAD:submission/prompt-log/decisions-and-lessons/ORCHESTRATOR_DECISIONS.md:104:- D-073 fallback applied (T-202 r6 paralegal fail: a visit note lends its date to another visit's charge; a UB-04 period overrides a line's own date). Per the pre-declared rule the MVP letter prints the fillable blank "date of service [__________] (record|statement dated X)" on every charge line; no service date is extracted for the letter. Step 3 shows the same. SCOPE_CUTS 28 covers date extraction.
HEAD:submission/prompt-log/decisions-and-lessons/ORCHESTRATOR_DECISIONS.md:113:- D-073 label simplification (T-202 r7): the blank's parenthetical no longer classifies the source; every charge line reads "date of service [__________] (record dated X)". Classifying bill vs clinical record from excerpt words misfired ("ER charges:" on a clinical record printed "statement dated"); one neutral label cannot be wrong.
HEAD:submission/prompt-log/reviews/GATE-M3-product-manager.md:101:   "evidence": "lib11-counted-letter.out: 'Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00'. The line was held back because 'The line states no date of service'. board/cards/T-174.md:48 'letter statement dated wording ... not done'.",
HEAD:submission/prompt-log/reviews/GATE-M3-product-manager.md:103:   "fix": "Write 'itemized ledger (statement dated June 15, 2026; no service date stated)'. Open a card.",
HEAD:submission/prompt-log/reviews/GATE-M3-product-manager.md:104:   "acceptance_test": "lib11 export with a3 counted contains 'statement dated' and not 'June 15, 2026: $180.00'."},
HEAD:submission/prompt-log/reviews/GATE-M3-ux-designer.md:128:   "fix": "'itemized ledger (statement dated June 15, 2026; no service date stated): $250.00'.",
---
artifacts/gate-M3M4-suite-f6d5c19.txt
artifacts/gate-M3M4-suite-final.txt
submission/prompt-log/transcripts/session-6ddf8076-a8b2a0cf-backend-t-106-unit-suite-green.md
submission/prompt-log/transcripts/session-6ddf8076-aa96c14b-qa-green-suite-file-re-record-video.md
submission/prompt-log/transcripts/session-6ddf8076-aaeb9e98-qa-full-suite-on-gate-commit.md
.claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md
submission/NEEDS_CHRIS.md
submission/SUBMISSION_CHECKLIST.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:38:42.421Z

**tool call — Bash**
````
{
 "command": "git grep -n -i \"will be burned\\|statement dated\\|once the caption pass\\|pending re-run\\|code can read\\|pending\" HEAD -- submission/product-note.md submission/part2-process.md submission/NEEDS_CHRIS.md submission/SUBMISSION_CHECKLIST.md submission/email-draft.md README.md memory/SCOPE_CUTS.md docs/LLM_VS_CODE.md app artifacts/CAPTIONS.md artifacts/NARRATION.md ':!app/frontend/*.png' 2>/dev/null | cut -c1-260; echo \"--- working tree vs HEAD (submission, artifacts, app, memory)\"; git status --short -- submission artifacts app memory docs README.md | head -20",
 "description": "Grep stale wording in non-prompt-log tracked files, check dirty tree"
}
````

### User / tool · 2026-11-03T15:38:42.624Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:38:44.019Z

**tool call — Bash**
````
{
 "command": "git log --format='%h %ad %s' --date=iso -n 12 -- artifacts/demo.webm artifacts/demo.vtt submission/product-note.pdf submission/part2-process.pdf submission/product-note.md submission/part2-process.md app/backend/service_date.py app/backend/export.py | cut -c1-200; ls -la artifacts/demo.webm artifacts/demo.vtt submission/*.pdf 2>&1; git diff HEAD --stat -- artifacts/demo.webm submission/product-note.pdf submission/part2-process.pdf | tail -3",
 "description": "Check commit history for video, PDFs, md; file sizes"
}
````

### User / tool · 2026-11-03T15:38:44.179Z

**tool result**
````
cd7fd27 2026-11-03 09:12:32 -0600 feat(backend): D-075 charge blank always reads (record dated X); drop statement variant (T-202)
a932fc9 2026-11-03 08:52:22 -0600 docs(writer): T-218 ship-bar row 5 and Part 2 cite the final suite at 43ce6eb; captions are burned in; PDFs re-rendered (1 and 4 pages)
c2dd104 2026-11-03 08:50:49 -0600 fix(qa): T-184 demo.webm re-recorded at 43ce6eb (Step 3 MRI note shows the new wording), caption band below the app so Saved and Undo show; final green suite record
43ce6eb 2026-11-03 08:04:55 -0600 fix(backend): gate M3+M4 fix A part 2, no_date note no longer says the code reads dates; README reviews pointer
38655da 2026-11-03 07:55:57 -0600 feat(qa): T-184 burned-in captions in demo.webm (in-page caption band from the narration) + artifacts/demo.vtt; re-recorded 173 s
ada93fc 2026-11-03 07:54:08 -0600 fix(submission): gate M3+M4 fix C, note and Part 2 state the D-073 date blank, current T-211/T-184/T-212 status, ship-bar row 5 pending re-run, video plan, snapshot-s
aa21b24 2026-11-03 07:49:38 -0600 fix(backend): gate M3+M4 fix A, spec/api/LLM_VS_CODE/README match the D-073 blank; undated-charge notes section before BILLS TO REQUEST
5974034 2026-11-03 07:43:01 -0600 feat(qa): T-184 re-capture at f6d5c19: letter charge blank, one-statement panel, Found by code tag; 72 shots, 174 s video, captions and narration updated
b50952d 2026-11-03 07:24:37 -0600 feat(backend): T-202 r7 D-073 fallback applied: the letter and Step 3 print the fillable blank on every charge line, no service date extracted; letter_check requires 
cda2856 2026-11-02 23:15:23 -0600 feat(qa): T-184 demo assets: 72 final screenshots (1440x900, 390x844) with captions, 167 s Playwright walkthrough video, timed narration; scripts in tests/demo_assets
3784bfb 2026-11-02 22:44:50 -0600 docs(writer): T-188 submission checklist, email draft, NEEDS_CHRIS by priority, product note and Part 2 refreshed (T-181, T-179, D-071 to D-073), PDFs
756546b 2026-11-02 21:58:38 -0600 test(backend): T-202 r6 pin pipe cells, no-date bound, unlocated figure and visit ranges; heading cells gate the From/To pairing alone
-rw-r--r--@ 1 arsis  staff      3939 Nov  3 08:49 artifacts/demo.vtt
-rw-r--r--@ 1 arsis  staff  24236670 Nov  3 08:49 artifacts/demo.webm
-rw-r--r--@ 1 arsis  staff    259963 Nov  3 08:52 submission/part2-process.pdf
-rw-r--r--@ 1 arsis  staff    113390 Nov  3 08:52 submission/product-note.pdf
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:38:47.895Z

**tool call — Bash**
````
{
 "command": "for f in submission/product-note.md submission/part2-process.md submission/NEEDS_CHRIS.md submission/SUBMISSION_CHECKLIST.md submission/email-draft.md README.md memory/SCOPE_CUTS.md docs/LLM_VS_CODE.md artifacts/CAPTIONS.md artifacts/NARRATION.md; do echo \"== $f\"; git show HEAD:$f | grep -n -i \"will be burned\\|statement dated\\|once the caption pass\\|pending re-run\\|code can read\\|record dated\" | cut -c1-300; done; echo \"== app (py/js/html/md)\"; git grep -n -i \"statement dated\\|code can read\" HEAD -- app ':!*.png' ':!*.svg' | cut -c1-240",
 "description": "Targeted stale-wording grep per file at HEAD"
}
````

### User / tool · 2026-11-03T15:38:48.206Z

**tool result**
````
== submission/product-note.md
== submission/part2-process.md
== submission/NEEDS_CHRIS.md
== submission/SUBMISSION_CHECKLIST.md
== submission/email-draft.md
== README.md
== memory/SCOPE_CUTS.md
113:| 28 | Service-date extraction for letter charge lines (D-073 fallback) | No service date is extracted for the letter: every charge line prints the fillable blank "date of service [__________] (record dated X)" and Step 3 asks the user to fill it from the record. Six review rounds showed that re
== docs/LLM_VS_CODE.md
31:| 3 | Date of service and provider for an entry | **Code**: the record's own header date and its `Source:` label, exactly as written, give an entry's date and provider; the model is not asked for either. For a charge line the letter prints `date of service [__________] (record dated June 15, 2026
47:| 19 | Sorting, filter to accepted items, export assembly, citations, the total line | **Code**. Every letter line carries its verbatim excerpt, the provider as written, and an exhibit/Bates placeholder; each treatment line carries its date, and each charge line carries the fillable blank "date o
== artifacts/CAPTIONS.md
== artifacts/NARRATION.md
== app (py/js/html/md)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:38:50.263Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-218-pm && cd artifacts/review-evidence/T-218-pm && git show HEAD:submission/product-note.pdf > note.pdf && git show HEAD:submission/part2-process.pdf > part2.pdf && git show HEAD:submission/product-note.md > note.md && git show HEAD:submission/part2-process.md > part2.md && pdfinfo note.pdf | grep Pages; pdfinfo part2.pdf | grep Pages; pdftotext -layout note.pdf note.txt; pdftotext -layout part2.pdf part2.txt; cmp <(git show HEAD:submission/product-note.pdf) ../../../submission/product-note.pdf && echo \"note pdf worktree==HEAD\"; cmp <(git show HEAD:submission/part2-process.pdf) ../../../submission/part2-process.pdf && echo \"part2 pdf worktree==HEAD\"; grep -n -i \"5,945\\|614\\|gate-M3M4-suite\\|pending re-run\\|statement dated\\|burned\\|record dated\\|in progress\\|code can read\" note.txt part2.txt | cut -c1-260",
 "description": "Extract HEAD PDFs and grep their text"
}
````

### User / tool · 2026-11-03T15:38:50.652Z

**tool result**
````
Pages:           1
Pages:           4
note pdf worktree==HEAD
part2 pdf worktree==HEAD
note.txt:32:                                                   log/reviews/T-181-paralegal-r2.md). Tests at 43ce6eb, fresh archive: 5,945 unit passed, 0
note.txt:33:                                                   failed; 614 E2E passed, 0 failed; letter check 0; spec check true (artifacts/gate-M3M4-
note.txt:35:                                                   artifacts/gate-M3M4-suite-f6d5c19.txt)
note.txt:48:  (T-179 blocks it). The combined M3+M4 gate failed with four blockers; fixes in progress.
part2.txt:74:What did it cost: days, or dollars off the offer?                                            Which one burned you once?
part2.txt:194:       the entry you always re-check, and the one that burned you. If this week is bad, say “not this week.” That helps too.
part2.txt:218:Before release. Unit tests (5,945 passed, 0 failed, 12 skipped) and E2E (614 passed, 0 failed, 1 skipped), both at 43ce6eb on a fresh
part2.txt:219:archive, plus letter check 0 and spec check true (artifacts/gate-M3M4-suite-final.txt; the earlier red run at f6d5c19, before the
part2.txt:220:date-blank fixes, is artifacts/gate-M3M4-suite-f6d5c19.txt). Earlier E2E runs: 412 passed before the guided screen
part2.txt:226:M3+M4 gate (D-075) failed with four blockers, and its fix round is in progress.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:01.036Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/ | grep -i \"GATE-M3M4-verify-pm\\|frames\\|\\.py\" | head -20; ls artifacts/review-evidence/GATE-M3M4-verify-pm 2>/dev/null | head; which ffmpeg ffprobe; git show --stat c2dd104 | head -40; git show --stat cd7fd27 | head -40",
 "description": "Find prior frames tooling and commit stats"
}
````

### User / tool · 2026-11-03T15:39:01.294Z

**tool result**
````
GATE-M3-accessibility-audit.py
GATE-M3-accessibility-common.py
GATE-M3-accessibility-dbg1.py
GATE-M3-accessibility-dlgnames.py
GATE-M3-accessibility-explore.py
GATE-M3-accessibility-explore2.py
GATE-M3-accessibility-kb1.py
GATE-M3-accessibility-kb10.py
GATE-M3-accessibility-kb11.py
GATE-M3-accessibility-kb12.py
GATE-M3-accessibility-kb2.py
GATE-M3-accessibility-kb3.py
GATE-M3-accessibility-kb4.py
GATE-M3-accessibility-kb5.py
GATE-M3-accessibility-kb6.py
GATE-M3-accessibility-kb7.py
GATE-M3-accessibility-kb8.py
GATE-M3-accessibility-kb9.py
GATE-M3-accessibility-keys.py
GATE-M3-accessibility-keys2.py
frames
note.pdf
note.txt
part2.pdf
part2.txt
r2-draft.md
snapshot_tool_HEAD.py
tree
waitfile.py
commit c2dd104636b3ee3b0ab945a032df7fa67dc341c3
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Tue Nov 3 08:50:49 2026 -0600

    fix(qa): T-184 demo.webm re-recorded at 43ce6eb (Step 3 MRI note shows the new wording), caption band below the app so Saved and Undo show; final green suite record
    
    Unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0 violations, check-spec all true.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 artifacts/NARRATION.md              |  16 +++---
 artifacts/demo.vtt                  | 100 ++++++++++++++++++------------------
 artifacts/demo.webm                 | Bin 21575056 -> 24236670 bytes
 artifacts/gate-M3M4-suite-final.txt |  14 +++++
 tests/demo_assets/video.py          |  18 ++++---
 5 files changed, 84 insertions(+), 64 deletions(-)
commit cd7fd277416161eacabee3b7da7b8386937068fc
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Tue Nov 3 09:12:32 2026 -0600

    feat(backend): D-075 charge blank always reads (record dated X); drop statement variant (T-202)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/export.py                        |  4 ++--
 app/backend/service_date.py                  | 20 ++++++++--------
 app/backend/store.py                         |  7 +++---
 app/frontend/guided/step3.js                 | 10 ++++----
 evals/letter_check.py                        | 35 ++++------------------------
 memory/contracts/api.md                      |  4 ++--
 tests/e2e/guided/test_round2.py              |  2 +-
 tests/e2e/guided/test_t205.py                | 18 +++++++-------
 tests/e2e/guided/test_t206.py                | 10 ++++----
 tests/unit/test_t200_undated_charge_label.py |  8 +++----
 tests/unit/test_t202_r7_all_blank.py         | 17 +++++++-------
 11 files changed, 54 insertions(+), 81 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:02.013Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list --status in_review 2>&1 | head -20; ls reviews | grep -i \"GATE-M3M4\\|GATE-M3-summary\" ; git show HEAD:board/milestones.md | tail -25; git show --stat 5b4d936 | head -30",
 "description": "Check gate and milestone state"
}
````

### User / tool · 2026-11-03T15:39:02.277Z

**tool result**
````
T-187	M5	qa         	in_review        	P0	AC 1/1	M5 prompt log: submission/prompt-log/ with TOOLS.md, CONTRACT copy, board activity log, all reviews, DECISIONS, LESSONS, and tools/export_prompt_log.py export of the agent transcripts (unedited, one file per agent) plus a two-paragraph reading guide
T-217	M4	release    	in_review        	P0	AC 1/1	Snapshot image allow-list includes artifacts/screenshots/final/ and artifacts/demo.webm (the README and CAPTIONS link them; OCR-clean per GATE-M3M4 privacy)
T-218	M5	writer     	in_review        	P0	AC 1/1	Gate M3+M4 fix C (writer): note + Part 2 + PDFs state the D-073 all-blank date rule; status of T-211/T-184/T-212 current; ship-bar row cites the post-fix gate suite; video plan (captions burned in) in NEEDS_CHRIS; email/checklist point only at paths in the snapshot
GATE-M3-summary.md
GATE-M3M4-installer.md
GATE-M3M4-paralegal.md
GATE-M3M4-privacy-compliance.md
GATE-M3M4-product-manager.md
GATE-M3M4-staff-engineer.md
GATE-M3M4-ux-designer.md
GATE-M3M4-verify-pm-r2.md
GATE-M3M4-verify-pm.md
GATE-M3M4-verify-staff.md
T-184-gate-M3M4.md
T-188-gate-M3M4.md
T-202-gate-M3M4.md
T-207-gate-M3M4.md
T-211-gate-M3M4.md
T-212-gate-M3M4.md
T-213-gate-M3M4.md
T-214-gate-M3M4.md
T-215-gate-M3M4.md
T-216-gate-M3M4.md
---
milestones:
  - {"id": "M0", "title": "Operating system (harness, board, hooks, agents)", "status": "done", "budget_h": 1.5, "started_at": "2026-11-02T00:07:00Z", "gate_result": "pass", "gate_record": "reviews/GATE-M0-summary.md", "gate_at": "2026-11-02T01:11:14Z", "done_at": "2026-11-02T01:11:14Z"}
  - {"id": "M1", "title": "Research, personas, requirements, architecture", "status": "done", "budget_h": 2.5, "started_at": "2026-11-02T00:17:08Z", "gate_result": "pass", "gate_record": "reviews/GATE-M1-summary.md", "gate_at": "2026-11-02T01:38:56Z", "done_at": "2026-11-02T01:38:56Z"}
  - {"id": "M2", "title": "Core pipeline + evals green", "status": "done", "budget_h": 3.5, "started_at": "2026-11-02T01:38:56Z", "note": "re-gate round 2 at 7cfdb0b; live 3-run met ship bar at 312efe6 (7cfdb0b)", "gate_result": "pass", "gate_record": "reviews/GATE-M2-summary.md", "gate_at": "2026-11-02T19:30:29Z", "done_at": "2026-11-02T19:30:29Z"}
  - {"id": "M3", "title": "Review UI, export, E2E", "status": "active", "budget_h": 3.5, "started_at": "2026-11-02T19:30:37Z", "note": "round-1 findings triaged (reviews/GATE-M3-round1-triage.md); re-gate after T-177/T-178/T-179/T-045", "gate_result": "pass", "gate_record": "reviews/GATE-M3-summary.md", "gate_at": "2026-11-03T15:18:34Z"}
  - {"id": "M4", "title": "Hardening, deployment, demo assets", "status": "active", "budget_h": 2.0, "started_at": "2026-11-03T04:32:00Z"}
  - {"id": "M5", "title": "Submission package", "status": "active", "budget_h": 2.0, "started_at": "2026-11-03T04:32:00Z"}
---
# Milestones

Generated by `tools/board.py` — edit through `board.py milestone` / `board.py gate`.

| Milestone | Title | Status | Gate | Started | Finished | Budget (h) | Note |
|---|---|---|---|---|---|---|---|
| M0 | Operating system (harness, board, hooks, agents) | done | pass ([record](../reviews/GATE-M0-summary.md)) | 2026-11-02T00:07:00Z | 2026-11-02T01:11:14Z | 1.5 |  |
| M1 | Research, personas, requirements, architecture | done | pass ([record](../reviews/GATE-M1-summary.md)) | 2026-11-02T00:17:08Z | 2026-11-02T01:38:56Z | 2.5 |  |
| M2 | Core pipeline + evals green | done | pass ([record](../reviews/GATE-M2-summary.md)) | 2026-11-02T01:38:56Z | 2026-11-02T19:30:29Z | 3.5 | re-gate round 2 at 7cfdb0b; live 3-run met ship bar at 312efe6 (7cfdb0b) |
| M3 | Review UI, export, E2E | active | pass ([record](../reviews/GATE-M3-summary.md)) | 2026-11-02T19:30:37Z | - | 3.5 | round-1 findings triaged (reviews/GATE-M3-round1-triage.md); re-gate after T-177/T-178/T-179/T-045 |
| M4 | Hardening, deployment, demo assets | active | - | 2026-11-03T04:32:00Z | - | 2.0 |  |
| M5 | Submission package | active | - | 2026-11-03T04:32:00Z | - | 2.0 |  |

Definitions: see docs/CONTRACT.md §4 (M0) and §5 (M1–M5).
commit 5b4d936a4af07b7f3cc6f1d3ed3d02569dd08718
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Tue Nov 3 09:18:38 2026 -0600

    gate(M3): pass — combined M3+M4 panel, guided UI, judge/HITL exposed, D-073 date blanks
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 board/activity.jsonl                          | 3583 +++++++++++++++++++++++++
 board/cards/T-045.md                          |   74 +-
 board/cards/T-046.md                          |   55 +-
 board/cards/T-053.md                          |    3 +-
 board/cards/T-055.md                          |    8 +-
 board/cards/T-057.md                          |   21 +-
 board/cards/T-058.md                          |    8 +-
 board/cards/T-059.md                          |   14 +-
 board/cards/T-060.md                          |  127 +-
 board/cards/T-061.md                          |   18 +-
 board/cards/T-063.md                          |   30 +-
 board/cards/T-064.md                          |   49 +-
 board/cards/T-065.md                          |   38 +-
 board/cards/T-066.md                          |   39 +-
 board/cards/T-067.md                          |   85 +-
 board/cards/T-068.md                          |   67 +
 board/cards/T-069.md                          |   33 +
 board/cards/T-070.md                          |   44 +
 board/cards/T-071.md                          |   49 +
 board/cards/T-072.md                          |   76 +
 board/cards/T-073.md                          |   42 +
 board/cards/T-074.md                          |   43 +
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:05.105Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && ls | grep -i \"frames\\|waitfile\\|prune\\|count_at\" ; ls GATE-M3M4-verify-pm/frames | head -5; ls GATE-M3-*/ 2>/dev/null | head -0; find . -maxdepth 2 -name \"frames.py\" | head",
 "description": "Locate the frame extraction helper"
}
````

### User / tool · 2026-11-03T15:39:05.226Z

**tool result**
````
player.html
t000.png
t006.png
t012.png
t018.png
head: illegal line count -- 0
./T-184-gate-staff/frames.py
./GATE-M3M4-pm/frames.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:06.571Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && cat GATE-M3M4-pm/frames.py | head -60; cat GATE-M3M4-verify-pm/frames/player.html | head -30",
 "description": "Read frames helper"
}
````

### User / tool · 2026-11-03T15:39:06.656Z

**tool result**
````
"""Sample frames from a webm using headless Chromium (no ffmpeg available).
Usage: .venv/bin/python -I frames.py <video.webm> <outdir> <step_seconds>"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

video = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
step = float(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
html = out / "player.html"
html.write_text(f'<html><body style="margin:0;background:#000"><video id="v" src="{video.as_uri()}" muted preload="auto" style="width:1440px"></video></body></html>')
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(html.as_uri())
    pg.wait_for_function("document.getElementById('v').readyState >= 1", timeout=30000)
    dur = pg.evaluate("document.getElementById('v').duration")
    if dur == float("inf") or dur != dur:
        pg.evaluate("document.getElementById('v').currentTime = 1e9")
        pg.wait_for_timeout(1500)
        dur = pg.evaluate("document.getElementById('v').duration")
    vw = pg.evaluate("[document.getElementById('v').videoWidth, document.getElementById('v').videoHeight]")
    print("duration", dur, "size", vw)
    t = 0.5
    while t < dur:
        pg.evaluate(f"document.getElementById('v').currentTime = {t}")
        pg.wait_for_function("!document.getElementById('v').seeking", timeout=15000)
        pg.wait_for_timeout(150)
        pg.locator("#v").screenshot(path=str(out / f"t{int(t):03d}.png"))
        t += step
    b.close()
<html><body style="margin:0;background:#000"><video id="v" src="file:///Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3M4-verify-pm/tree/artifacts/demo.webm" muted preload="auto" style="width:1440px"></video></body></html>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:09.643Z

**tool call — Bash**
````
{
 "command": "git diff --quiet HEAD -- artifacts/demo.webm && echo \"demo.webm worktree==HEAD\"; git hash-object artifacts/demo.webm; git rev-parse HEAD:artifacts/demo.webm; mkdir -p artifacts/review-evidence/T-218-pm/frames && cp artifacts/review-evidence/GATE-M3M4-pm/frames.py artifacts/review-evidence/T-218-pm/frames.py && timeout 400 .venv/bin/python -I artifacts/review-evidence/T-218-pm/frames.py artifacts/demo.webm artifacts/review-evidence/T-218-pm/frames 6 2>&1 | tail -5; ls artifacts/review-evidence/T-218-pm/frames | wc -l",
 "description": "Sample frames from HEAD demo.webm every 6 s",
 "timeout": 420000
}
````

### User / tool · 2026-11-03T15:39:10.339Z

**tool result**
````
demo.webm worktree==HEAD
5de844ef1b94d521de2b220f8172d7940796c202
5de844ef1b94d521de2b220f8172d7940796c202
/bin/bash: timeout: command not found
       0
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:12.013Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-218-pm/frames.py artifacts/demo.webm artifacts/review-evidence/T-218-pm/frames 6 2>&1 | tail -5; ls artifacts/review-evidence/T-218-pm/frames | wc -l",
 "description": "Sample frames without timeout wrapper",
 "timeout": 420000
}
````

### User / tool · 2026-11-03T15:39:23.548Z

**tool result**
````
duration 173.16 size [1280, 886]
      30
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:25.905Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"dated\\|date of service\\|code can read\\|does not take\" artifacts/demo.vtt artifacts/NARRATION.md artifacts/CAPTIONS.md | cut -c1-260; ls artifacts/review-evidence/T-218-pm/frames",
 "description": "Search captions for date wording"
}
````

### User / tool · 2026-11-03T15:39:25.998Z

**tool result**
````
artifacts/NARRATION.md:24:| 2:34-2:42 | This is the file I downloaded, plain text, ready to paste. Each charge line has a blank for the date of service. |
artifacts/CAPTIONS.md:52:- `27-step3-charge-1440.png` (f6d5c19): Step 3, one bill amount at a time. The record shows the figure; the question is whether this charge counts toward the bill total. The charge line carries a fillable blank, date of service [______
artifacts/CAPTIONS.md:53:- `27-step3-charge-390.png` (f6d5c19): Step 3, one bill amount at a time. The record shows the figure; the question is whether this charge counts toward the bill total. The charge line carries a fillable blank, date of service [_______
artifacts/CAPTIONS.md:62:- `40-step4-letter-1440.png` (f6d5c19): Step 4, Get your letter. The letter is on the left, ready to paste into a demand letter; each charge line in it carries the fillable blank date of service [__________], and the bar says the [Ex. 
artifacts/CAPTIONS.md:63:- `40-step4-letter-390.png` (f6d5c19): Step 4, Get your letter. The letter is on the left, ready to paste into a demand letter; each charge line in it carries the fillable blank date of service [__________], and the bar says the [Ex. _
artifacts/demo.vtt:189:Each charge line has a blank for the date of service.
player.html
t000.png
t006.png
t012.png
t018.png
t024.png
t030.png
t036.png
t042.png
t048.png
t054.png
t060.png
t066.png
t072.png
t078.png
t084.png
t090.png
t096.png
t102.png
t108.png
t114.png
t120.png
t126.png
t132.png
t138.png
t144.png
t150.png
t156.png
t162.png
t168.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:26.201Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-218-pm/frames/t126.png"
}
````

### User / tool · 2026-11-03T15:39:26.226Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:30.577Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-218-pm/frames/t114.png"
}
````

### User / tool · 2026-11-03T15:39:30.601Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:30.973Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-218-pm/frames/t138.png"
}
````

### User / tool · 2026-11-03T15:39:30.986Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:31.405Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-218-pm/frames/t156.png"
}
````

### User / tool · 2026-11-03T15:39:31.415Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:31.724Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-218-pm/frames/t162.png"
}
````

### User / tool · 2026-11-03T15:39:31.734Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:35.485Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-218-pm/frames && which tesseract; .venv/bin/python -c 1 2>/dev/null; cd /Users/arsis/zlayt-pm-project && .venv/bin/python -I -c 'import pytesseract' 2>&1 | tail -1; ls artifacts/review-evidence | grep -i ocr | head",
 "description": "Check OCR availability"
}
````

### User / tool · 2026-11-03T15:39:35.620Z

**tool result**
````
/opt/homebrew/bin/tesseract
ModuleNotFoundError: No module named 'pytesseract'
GATE-M3M4-priv-ocr.py
T-194-ocr.py
T-194-r2-ocr.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:39:37.999Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-218-pm/frames && for f in t*.png; do tesseract $f stdout 2>/dev/null | tr '\\n' ' ' | grep -o -i \"statement dated[^.]\\{0,40\\}\\|code can read\\|will be burned\\|pending re-run\" | sed \"s/^/$f: /\"; done; echo \"OCR scan done\"; for f in t0[0-9][0-9].png t1[0-9][0-9].png; do tesseract $f stdout 2>/dev/null | tr '\\n' ' ' | grep -o -i \"record dated[^.]\\{0,25\\}\" | sed \"s/^/$f: /\"; done | head",
 "description": "OCR all 30 frames for stale wording",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T15:40:16.178Z

**tool result**
````
OCR scan done
t126.png: record dated May 29, 2026)  urce: Aus
t138.png: record dated January 9, 2026) ( Chang
t138.png: record dated May 29, 2026) ( change  
t156.png: record dated January 9, 2026): $6,240
t156.png: record dated May 29, 2026): $2,150
t162.png: record dated January 9, 2026): $6,240
t162.png: record dated May 29, 2026): $2,150
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:40:21.707Z

**tool call — Bash**
````
{
 "command": "head -30 reviews/GATE-M3-summary.md | cut -c1-400; echo ----; git show HEAD:submission/product-note.md | sed -n '17,30p;44,50p' | cut -c1-700; echo ----; git show HEAD:submission/part2-process.md | sed -n '224,228p;112,116p' | cut -c1-500",
 "description": "Read gate summary and note/Part 2 status lines"
}
````

### User / tool · 2026-11-03T15:40:21.841Z

**tool result**
````
# GATE-M3 summary — Review UI, export, E2E

Result: **pass** (round 2, combined M3+M4 panel under D-075). Pinned commit f6d5c19; fixes verified at 43ce6eb and later (cd7fd27, 304ba58, be257c9).

## Round 1 (d0b04bc) — fail
Triage: `reviews/GATE-M3-round1-triage.md` (2 blockers: curated answers labelled as AI output, T-177; run stuck after restart, T-178). Both closed: T-177 done after five rounds (D-065/D-069, prepared-wording templates + fault-injection property test), T-178 done.

## Chris's redesign (between rounds)
Chris: "this UI is VERY hard to use". D-068 guided 4-step UI designed (T-180) and built (T-181, T-203, T-206, T-209, T-211); UX r3 judged it meets the "grandma" bar on desktop and phone. Judge + human-in-the-loop shown on every item and explained on a "How each answer is checked" page (D-074).

## Round 2 — combined M3+M4 panel at f6d5c19 (D-075)
| Reviewer | Verdict | Outcome |
|---|---|---|
| staff-engineer | fail (2 doc blockers) | fixed in T-215; verify pass `reviews/GATE-M3M4-verify-staff.md` |
| ux-designer | pass | minors -> SCOPE_CUTS 29 |
| paralegal | pass | totals match truths on 4 cases; minors -> SCOPE_CUTS 29 |
| privacy-compliance | pass | working repo holds private values in 3 tracked files; publish only the snapshot (NEEDS_CHRIS) |
| installer | fail (1 blocker: README make-evals statement) | fixed in T-215; verify pass |
| product-manager | fail (4 blockers) | fixed in T-217/T-218/T-215 + memory commit; verify `reviews/GATE-M3M4-verify-pm-r2.md` changes on 2 majors, both closed by c2dd104 + a932fc9 |

Suite at 43ce6eb (`artifacts/gate-M3M4-suite-final.txt`): unit 5945 passed / 0 failed; e2e 614 passed / 0 failed; letter_check 0; spec check true.

## Date of service (D-071 -> D-073)
Six review rounds showed date extraction from bills, encounter records and prose kept printing wrong dates on new layouts. Shipped rule: every letter charge line prints "date of service [__________] (record dated X)" for the paralegal to fill (D-073 fallback + label simplification; paralegal r8 pass). SCOPE_CUTS 28.

## Accepted debt
SCOPE_CUTS 22-29; held M3 cards cancelled per D-063 (row 26).
----
| 3 | Flags: precision, recall 0.9 per type; 28-day gap not flagged, 73-day flagged | golden: 1.000/1.000, four types; 28 no, 73 yes [E]. **Library: 34 of 42 must-flags, 0.81 [L]** |
| 4 | No invented facts: 0 unsupported over 3 runs; judge catches 95% of seeded wrong summaries | 0; 40/40; 0 of 10 correct rejected; conflict and flag judges 20/20, 12/12 [E] |
| 5 | Reviewable: paralegal persona rates "I could verify every claim quickly" 4/5+; tests green | **Persona only; no real paralegal yet.** 4/5 on the screen I rejected (`submission/prompt-log/reviews/GATE-M3-paralegal.md`), 4/5 on the guided one (`submission/prompt-log/reviews/T-181-paralegal-r2.md`). Tests at 43ce6eb, fresh archive: **5,945 unit passed, 0 failed; 614 E2E passed, 0 failed**; letter check 0; spec check true (`artifacts/gate-M3M4-suite-final.txt`; the earlier red run at f6d5c19, before the date-blank fixes, is `artifacts/gate-M3M4-suite-f6d5c19.txt`) |

**What testing found.**

- **Reviewability passed on paper and failed in use.** A persona scored the M3 screen 4/5; when I used it, it was *very* hard to use. It is now four fixed steps (D-068). A UX reviewer passed it on desktop and a 390 px phone; the ship call still needs a real paralegal.
- **The 1.000 flag numbers do not generalize.** Golden cases were written next to the rules; on the 15 library packets must-flag recall is 0.81 (`submission/prompt-log/reviews/GATE-M3-product-manager.md`, `memory/SCOPE_CUTS.md` rows 13, 23). Misses are conflicts code never proposes ("Left" against "Right shoulder pain"). Judge numbers are partly in-sample.
- **Billing took four adversarial rounds.** A claims-adjuster reviewer outworded every word-list rule: a letter said $16,147 against a true $8,123.50 (`submission/prompt-log/reviews/T-140-claims-adjuster.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one by one, and the total reads "Billed charges accepted from these records". Date reading failed the same way. After six rounds the pre-declared fallback applies: every charge line prints a fillable "date of service [__________]" with the record or statement date in parentheses, and no service date is extracted (D-073, `memory/SCOPE_CUTS.md` row 28).
- **The M3 gate failed once:** prepared demo answers were labeled as AI output (T-177), and one click accepted a disputed summary 5 of 5 times (T-179 blocks it). The combined M3+M4 gate failed with four blockers; fixes in progress.

**How the AI can mislead her, and what the design does.**

| Failure | Design |
----
**Each week:** the board (cards by state, review rounds per card), the eval report against the last one (did a metric drop, did a prompt hash change), bugs that escaped, review findings by severity, decisions waiting on me. I check evidence, not claims. Two examples from this build: a worker's "12/12 pass" came from an uncommitted working tree and the committed code rendered no charges panel; two partial commits broke HEAD. The rule now is to verify from `git archive HEAD`, and pre-commit compil

**Before release.** Unit tests (5,945 passed, 0 failed, 12 skipped) and E2E (614 passed, 0 failed, 1 skipped), both at 43ce6eb on a fresh archive, plus letter check 0 and spec check true (`artifacts/gate-M3M4-suite-final.txt`; the earlier red run at f6d5c19, before the date-blank fixes, is `artifacts/gate-M3M4-suite-f6d5c19.txt`). Earlier E2E runs: 412 passed before the guided screen (`evals/reports/m3-sensors.md`); 139 on the guided suite at 2c19817 (`submission/prompt-log/reviews/T-181-ux-desi

**When work is late or a bug reaches users.** Late: I cut scope, not checks. D-063 held every non-P0 card to finish the MVP. After three review rounds I either accept with written debt (65 rows in `memory/SCOPE_CUTS.md`) or cut. A bug in front of users: stop, reproduce, write the failing test or eval case first, fix, then record the lesson. Example: demo answers prepared by our team were labeled as AI output; the decision is D-065; the fix is in code and passed review in the fifth round (T-177).
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:40:40.647Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-218-pm && rm -rf $D/tree && mkdir -p $D/tree && git archive HEAD | tar -x -C $D/tree && ls $D/tree | head -3 && (cd $D/tree && env -u ANTHROPIC_API_KEY /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider > ../unit-head.txt 2>&1; echo \"exit $?\" >> ../unit-head.txt) ",
 "description": "Run unit suite on HEAD archive in background",
 "run_in_background": true
}
````

### User / tool · 2026-11-03T15:40:40.715Z

**tool result**
````
Command running in background with ID: btl27xa22. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/btl27xa22.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:40:41.761Z

**tool call — Bash**
````
{
 "command": "for f in submission/product-note.md submission/part2-process.md submission/SUBMISSION_CHECKLIST.md submission/NEEDS_CHRIS.md submission/email-draft.md README.md; do echo \"== $f\"; git show HEAD:$f | grep -n -i \"statement date\\|record or statement\\|fix round\\|fixes in progress\\|in progress\\|burned\\|captions\" | cut -c1-330; done",
 "description": "Grep remaining statement-date and status phrases"
}
````

### User / tool · 2026-11-03T15:40:41.962Z

**tool result**
````
== submission/product-note.md
25:- **Billing took four adversarial rounds.** A claims-adjuster reviewer outworded every word-list rule: a letter said $16,147 against a true $8,123.50 (`submission/prompt-log/reviews/T-140-claims-adjuster.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one 
26:- **The M3 gate failed once:** prepared demo answers were labeled as AI output (T-177), and one click accepted a disputed summary 5 of 5 times (T-179 blocks it). The combined M3+M4 gate failed with four blockers; fixes in progress.
== submission/part2-process.md
20:| 2. Tell me about the last time an adjuster pushed back on a date or a fact. What did it cost: days, or dollars off the offer? | 2. Which entries do you always re-check against the source, and how? Which one burned you once? |
99:> Hi [name], I'm building the tool that drafts the treatment chronology, and I need to hear where it's wrong, not whether it's nice. Could I have 20 minutes at your desk this week? Pick a matter that's already closed. You'll build the chronology the way you normally do while I watch; I won't copy or record anything. Then I'll
114:**Before release.** Unit tests (5,945 passed, 0 failed, 12 skipped) and E2E (614 passed, 0 failed, 1 skipped), both at 43ce6eb on a fresh archive, plus letter check 0 and spec check true (`artifacts/gate-M3M4-suite-final.txt`; the earlier red run at f6d5c19, before the date-blank fixes, is `artifacts/gate-M3M4-suite-f6d5c19.
116:**When work is late or a bug reaches users.** Late: I cut scope, not checks. D-063 held every non-P0 card to finish the MVP. After three review rounds I either accept with written debt (65 rows in `memory/SCOPE_CUTS.md`) or cut. A bug in front of users: stop, reproduce, write the failing test or eval case first, fix, then re
== submission/SUBMISSION_CHECKLIST.md
12:| 2 | Part 1: demo video (3 min or less) or annotated screenshots | **final** (T-184): a 174 s recording on the sample case and 72 annotated screenshots, with captions burned into the video, and the snapshot allow-list keeps the video and the screenshots (T-217). Voice-over is optional for Chris | Video: [`artifacts/demo.webm
== submission/NEEDS_CHRIS.md
26:Optional, not blocking: the demo video ships in the repo as `artifacts/demo.webm` (174 s, sample case), the narration is burned in as on-screen captions, and the snapshot keeps the video and the screenshots (T-217). Nothing to host or paste for it. If you want your own voice, read `artifacts/NARRATION.md` over the video and r
== submission/email-draft.md
18:- **Demo recording and screenshots:** `artifacts/demo.webm` (under 3 minutes, sample case) and 72 annotated screenshots in `artifacts/screenshots/final/`, with `artifacts/CAPTIONS.md`
== README.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:40:44.896Z

**tool call — Bash**
````
{
 "command": "git show HEAD:submission/product-note.md | sed -n 25p | grep -o -i \".\\{80\\}statement date.\\{60\\}\"; git show HEAD:submission/part2-process.md | grep -n -o -i \".\\{60\\}statement date.\\{40\\}\"; git show HEAD:submission/part2-process.md | grep -n -o -i \".\\{60\\}record or statement.\\{40\\}\"; git show HEAD:submission/product-note.md | grep -n -i \"record or statement\" | cut -c1-80; git show HEAD:submission/product-note.md | grep -c \"ship bar\\|174\"; git show HEAD:artifacts/demo.vtt | tail -4",
 "description": "Quote the remaining statement-date phrase"
}
````

### User / tool · 2026-11-03T15:40:45.108Z

**tool result**
````
charge line prints a fillable "date of service [__________]" with the record or statement date in parentheses, and no service date is extracted (D-073, `m
116:ote" (D-066, T-179). A third: charge lines printed a bill's statement date as the service date. Six rounds of read
116: fillable "date of service [__________]" with the record or statement date in parentheses, and no service date is 
116:e prints a fillable "date of service [__________]" with the record or statement date in parentheses, and no service dat
25:- **Billing took four adversarial rounds.** A claims-adjuster reviewer outwor
0
50
00:02:48.752 --> 00:02:52.214
The AI's own results are in the evaluation report.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:40:51.752Z

**tool call — Bash**
````
{
 "command": "git show HEAD:submission/SUBMISSION_CHECKLIST.md | grep -n -i \"gate suite\\|T-215\\|T-216\\|T-217\\|T-218\\|suite\" | cut -c1-420",
 "description": "Check checklist section 7 rows"
}
````

### User / tool · 2026-11-03T15:40:51.854Z

**tool result**
````
12:| 2 | Part 1: demo video (3 min or less) or annotated screenshots | **final** (T-184): a 174 s recording on the sample case and 72 annotated screenshots, with captions burned into the video, and the snapshot allow-list keeps the video and the screenshots (T-217). Voice-over is optional for Chris | Video: [`artifacts/demo.webm`](../artifacts/demo.webm). Screenshots: [`artifacts/screenshots/final/`](../artifacts/scr
13:| 3 | Part 1: one-page product note | **final** wording; the ladder display (T-211) and the D-073 date-of-service blank are stated as built. Ship-bar row 5 test counts are filled at 43ce6eb (`artifacts/gate-M3M4-suite-final.txt`). Two `[CHRIS: ...]` placeholders (name, link) and one reason (T-191) are Chris's | [`submission/product-note.md`](product-note.md), PDF [`submission/product-note.pdf`](product-note.pdf) |
30:| Export: copy-ready treatment text, only what she accepted | final | [`app/backend/export.py`](../app/backend/export.py) | Byte-exact template [`evals/golden/sample.export.expected.txt`](../evals/golden/sample.export.expected.txt) (the spec copy of it is being aligned, T-215); [`evals/letter_check.py`](../evals/letter_check.py) |
32:| Guided four-step screen; the second AI check and the human decision shown on each item, and a "How each answer is checked" page | guided screen **final** (T-181); the ladder display is built (T-211, committed; its gate fixes are in T-216) | [`app/frontend/guided/`](../app/frontend/guided/) | T-181 reviews: [`submission/prompt-log/reviews/T-181-ux-designer-r3.md`](prompt-log/reviews/T-181-ux-designer-r3.md), [`su
85:| T-215 | backend | Gate fix A: spec section 6, api.md and LLM_VS_CODE match the date blank; 10 unit failures |
86:| T-216 | frontend | Gate fix B: 6 e2e failures, Step 4 names the date blanks |
87:| T-217 | qa | Snapshot allow-list keeps `artifacts/screenshots/final/` and `artifacts/demo.webm` |
88:| Gate suite | qa | Done: unit and e2e re-run at 43ce6eb; the counts in ship-bar row 5 are filled (`artifacts/gate-M3M4-suite-final.txt`; `artifacts/gate-M3M4-suite-f6d5c19.txt` is the earlier red run) |
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:40:54.992Z

**tool call — Bash**
````
{
 "command": "for t in T-215 T-216 T-217 T-211 T-212; do python3 tools/board.py list 2>/dev/null | grep \"^$t\" | cut -c1-90; done; git show HEAD:submission/SUBMISSION_CHECKLIST.md | sed -n 76,92p | cut -c1-200",
 "description": "Board status of cited cards and checklist section 7"
}
````

### User / tool · 2026-11-03T15:40:55.451Z

**tool result**
````
T-215	M4	backend    	done             	P0	AC 1/1	Gate M3+M4 fix A (docs/spec/backend): spe
T-216	M4	frontend   	done             	P0	AC 1/1	Gate M3+M4 fix B (frontend): 6 e2e failur
T-217	M4	release    	in_review        	P0	AC 1/1	Snapshot image allow-list includes artifa
T-211	M4	frontend   	done             	P0	AC 1/1	Guided UI exposes and explains the valida
T-212	M4	release    	done             	P0	AC 1/1	README front door for a repo-only reviewe
| One story: a miss | last section; **Chris writes it** (T-189) | Marked `[CHRIS: ...]` block with a suggested shape |
| Visual of the process | final | [`submission/validation-ladder.svg`](validation-ladder.svg) |

## 7. Pending, in one list

| Card | Owner | What is pending |
|---|---|---|
| T-187 | qa | Final prompt-log build and privacy sweep (after the last agent finishes, D-072) |
| T-194 | release | Public snapshot repo (single commit, redaction pass) |
| T-215 | backend | Gate fix A: spec section 6, api.md and LLM_VS_CODE match the date blank; 10 unit failures |
| T-216 | frontend | Gate fix B: 6 e2e failures, Step 4 names the date blanks |
| T-217 | qa | Snapshot allow-list keeps `artifacts/screenshots/final/` and `artifacts/demo.webm` |
| Gate suite | qa | Done: unit and e2e re-run at 43ce6eb; the counts in ship-bar row 5 are filled (`artifacts/gate-M3M4-suite-final.txt`; `artifacts/gate-M3M4-suite-f6d5c19.txt` is the earlier red run
| Chris | | `NEEDS_CHRIS.md`: T-189 (the story), T-190 (name, link), T-022 (demo link), T-193, T-191, T-192, T-019, T-023 |
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:41:01.400Z

**tool call — Bash**
````
{
 "command": "git status --short -- app evals tests | head -3; env -u ANTHROPIC_API_KEY .venv/bin/python -m evals.letter_check 2>&1 | tail -3; git status --short -- evals | head",
 "description": "Run letter_check at HEAD and verify it wrote nothing",
 "timeout": 180000
}
````

### User / tool · 2026-11-03T15:41:13.689Z

**tool result**
````
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
?? evals/reports/20261102T024355Z.md
?? evals/reports/20261102T024653Z.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:41:15.367Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-218-pm && tail -c 300 unit-head.txt 2>/dev/null; ls",
 "description": "Peek at unit run progress"
}
````

### User / tool · 2026-11-03T15:41:15.476Z

**tool result**
````
........................................................................ [ 10%]
........................................................................ [ 12%]
........................................................................ [ 13%]
...........................................................frames
frames.py
note.md
note.pdf
note.txt
part2.md
part2.pdf
part2.txt
tree
unit-head.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:41:19.482Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-218-pm && i=0; while ! grep -q '^exit' unit-head.txt && [ $i -lt 55 ]; do read -t 10 <> <(:) || true; i=$((i+1)); done; tail -c 400 unit-head.txt",
 "description": "Wait for the unit run to finish",
 "timeout": 590000
}
````

### User / tool · 2026-11-03T15:41:19.927Z

**tool result**
````
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
/bin/bash: /dev/fd/62: Permission denied
........................................................ [  9%]
........................................................................ [ 10%]
........................................................................ [ 12%]
........................................................................ [ 13%]
........................................................................ [ 14%]
................
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:41:21.541Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && cat GATE-M3M4-verify-pm/waitfile.py | head -20",
 "description": "Read waitfile helper"
}
````

### User / tool · 2026-11-03T15:41:21.631Z

**tool result**
````
import sys, time, pathlib
p = pathlib.Path(sys.argv[1]); end = time.time() + float(sys.argv[2])
while time.time() < end:
    t = p.read_text() if p.exists() else ""
    if "passed" in t or "failed" in t or "error" in t:
        print(t[-600:]); break
    time.sleep(10)
else:
    print("timeout")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:41:24.009Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/GATE-M3M4-verify-pm/waitfile.py artifacts/review-evidence/T-218-pm/unit-head.txt 560",
 "description": "Wait for the unit run result",
 "timeout": 590000
}
````

### User / tool · 2026-11-03T15:48:34.303Z

**tool result**
````
............................................................. [ 93%]
........................................................................ [ 94%]
........................................................................ [ 95%]
........................................................................ [ 96%]
........................................................................ [ 97%]
........................................................................ [ 99%]
.....................................................                    [100%]
5951 passed, 6 skipped in 466.17s (0:07:46)
exit 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:12.340Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-218-product-manager.md",
 "content": "# T-218 review: product-manager-reviewer (Dana Okafor, fictional)\n\n**Verdict: pass.** Both majors left open in `reviews/GATE-M3M4-verify-pm-r2.md` are closed at HEAD e0d721d. I found no blockers and no majors. Four minors and one nit remain.\n\n## The two open majors\n\n| Major (from verify-pm-r2) | Status at HEAD e0d721d | Evidence |\n|---|---|---|\n| Ship-bar row 5 said \"pending re-run\" and cited the red f6d5c19 run | **closed** | `git show HEAD:submission/product-note.md` row 5 (line 19): \"Tests at 43ce6eb, fresh archive: **5,945 unit passed, 0 failed; 614 E2E passed, 0 failed**; letter check 0; spec check true (`artifacts/gate-M3M4-suite-final.txt`; the earlier red run ... `artifacts/gate-M3M4-suite-f6d5c19.txt`)\". Part 2 line 114 says the same (\"5,945 passed, 0 failed, 12 skipped\", \"614 passed, 0 failed, 1 skipped\"). `git show HEAD:artifacts/gate-M3M4-suite-final.txt` is committed in c2dd104 and reads \"unit 5945 passed, 0 failed, 12 skipped exit 0\", \"e2e 614 passed, 0 failed, 1 skipped exit 0\", \"letter ... value 0\", \"spec ... spec_matches_golden true, letter_equal true, internal_notes_equal true\". `git ls-tree HEAD` keeps both suite files. \"pending re-run\" is absent from the note, Part 2, NEEDS_CHRIS, the checklist and the email. |\n| The video still showed the old date sentence | **closed** | c2dd104 (08:50:49) re-recorded `artifacts/demo.webm` (21,575,056 to 24,236,670 B), after the wording fix in 43ce6eb (08:04:55). The working tree file equals HEAD (`git hash-object` = `git rev-parse HEAD:artifacts/demo.webm` = 5de844ef). I sampled 30 frames every 6 s (`artifacts/review-evidence/T-218-pm/frames/`) and ran tesseract on all of them: 0 hits for \"code can read\", \"statement dated\", \"will be burned\" or \"pending re-run\". Frame t126 (Step 3, Austin Imaging MRI $2,150.00) reads \"The letter does not take a date of service from the records.\" The Saved line and the Undo button are fully visible above the caption band. Frames t156 and t162 show the exported letter: \"date of service [__________] (record dated May 29, 2026): $2,150.00\". |\n\n## The other checks you listed\n\n- **\"will be burned in\":** `git show HEAD:<file> | grep` on the note, Part 2, NEEDS_CHRIS, the checklist, the email draft, README, CAPTIONS and NARRATION returns nothing. NEEDS_CHRIS:26 and checklist row 2 say the captions are burned in.\n- **\"statement dated\":** zero hits in the note, Part 2, NEEDS_CHRIS, the checklist, the email, README, `docs/LLM_VS_CODE.md`, SCOPE_CUTS and `app/`. It remains only in `submission/prompt-log/` transcripts, reviews and decision logs, which are history. One related phrase survives (finding 1).\n- **PDFs match:** `pdfinfo` gives 1 page for the note and 4 for Part 2. `pdftotext` of both HEAD PDFs shows the 5,945/614 counts, both suite paths and no \"pending re-run\". Both PDFs and both .md files last changed in a932fc9, and `cmp` shows the working-tree PDFs are identical to HEAD.\n- **Check I ran beyond your list:** a fresh `git archive HEAD` unit run (ANTHROPIC_API_KEY unset) gave **5951 passed, 6 skipped, 0 failed** in 466 s. The skip count differs from the file's 12 and the total is the same, 5957, so it is an environment difference. `python -m evals.letter_check` at HEAD returns value 0 over 25 cases. I did not re-run e2e at HEAD (about 14 min), so I make no claim about it.\n\n## Why it is a pass, and what remains\n\nThe ship-bar row now has a number, a method and a result, and the failed run is disclosed next to it. The video matches the app at HEAD for the sample case. What is left is stale status wording and one gap in the evidence trail, listed as minors below.\n\n```json\n{\"card\": \"T-218\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"HEAD e0d721d (T-218 fixes in c2dd104 and a932fc9; D-075 code change cd7fd27 after them); submission/{product-note,part2-process}.md + PDFs, SUBMISSION_CHECKLIST.md, NEEDS_CHRIS.md, email-draft.md, artifacts/{demo.webm,demo.vtt,gate-M3M4-suite-final.txt}; no app URL used; sample case via the video\",\n \"exercised\": [\n  \"Read personas/product-manager.md and reviews/GATE-M3M4-verify-pm-r2.md\",\n  \"git rev-parse --short HEAD gives e0d721d; git log for the video, PDFs, notes and service_date.py; git show --stat c2dd104 and cd7fd27\",\n  \"git show HEAD:artifacts/gate-M3M4-suite-final.txt (header and RESULTS block)\",\n  \"git show HEAD: grep of product-note.md, part2-process.md, NEEDS_CHRIS.md, SUBMISSION_CHECKLIST.md, email-draft.md, README.md, SCOPE_CUTS.md, LLM_VS_CODE.md, CAPTIONS.md, NARRATION.md for 'pending re-run', 'will be burned', 'statement dated', 'code can read'; git grep over app/\",\n  \"pdfinfo + pdftotext on both HEAD PDFs; cmp of HEAD PDFs against the working tree; grep of the extracted text for 5,945, 614, the suite paths and stale phrases\",\n  \"git hash-object artifacts/demo.webm against git rev-parse HEAD:artifacts/demo.webm; frames.py every 6 s (30 frames in artifacts/review-evidence/T-218-pm/frames); viewed t114, t126, t138, t156, t162; tesseract OCR over all 30 frames\",\n  \"git archive HEAD into artifacts/review-evidence/T-218-pm/tree; pytest tests/unit there: 5951 passed, 6 skipped, 0 failed (artifacts/review-evidence/T-218-pm/unit-head.txt)\",\n  \"python -m evals.letter_check at HEAD: value 0, 25 cases\",\n  \"board.py show T-218; board.py list for T-211, T-212, T-215, T-216, T-217; reviews/GATE-M3-summary.md; board/milestones.md\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"ship_bar_row5_backed_by_committed_run\": 5, \"video_matches_app_at_head\": 5, \"pdfs_match_markdown\": 5, \"stale_wording_removed\": 4, \"status_statements_current\": 3, \"evidence_trail_reaches_head\": 3},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"The note and Part 2 still say the blank shows 'the record or statement date', but D-075 prints only 'record dated'\",\n   \"evidence\": \"product-note.md:25 and part2-process.md:116: 'a fillable \\\"date of service [__________]\\\" with the record or statement date in parentheses, and no service date is extracted'. HEAD docs/LLM_VS_CODE.md:31 and memory/SCOPE_CUTS.md:113 say '(record dated X)', and the video frames t156 and t162 show '(record dated ...)'. cd7fd27 (D-075) made the label always 'record'\",\n   \"why_it_matters\": \"This is the same date-rule wording that was my round-1 blocker B1. The product never prints a statement date any more, and the note says it sometimes does. It is mild because the blank is still unfilled either way.\",\n   \"fix\": \"Writer: change to 'with the record date in parentheses', then re-render both PDFs.\",\n   \"acceptance_test\": \"git show HEAD:submission/product-note.md | grep -c 'record or statement' returns 0, likewise for part2-process.md, and pdftotext on both PDFs finds no 'record or statement'.\"},\n  {\"severity\": \"minor\", \"title\": \"The cited green run is one code commit behind HEAD, and the note does not say so\",\n   \"evidence\": \"Row 5 says 'Tests at 43ce6eb'. git log shows cd7fd27 (D-075, 09:12) changed app/backend/export.py, service_date.py, store.py, app/frontend/guided/step3.js, evals/letter_check.py and 6 test files, after the 08:50 suite record. The only post-change check on the board is the backend note: '124 unit + 110 guided e2e + test_round2 pass; letter_check 0 violations; check-spec true (archive copy)'. My own HEAD unit run is green (5951/0), but no committed file covers e2e at HEAD\",\n   \"why_it_matters\": \"A reader takes 'tests green' as the shipped build. The label is true for 43ce6eb. The changed code is the exact text of the charge line in the letter, which is the one place a wrong word is expensive.\",\n   \"fix\": \"Either re-run unit and e2e on the final commit and cite the new file, or add one clause to row 5 and Part 2:114: 'cd7fd27 (record-dated label) came after this run; unit re-run at HEAD: 5,951 passed, 0 failed'.\",\n   \"acceptance_test\": \"Row 5 names a suite file whose header commit has no later change under app/ or tests/, or states the later commit and what was re-run on it.\"},\n  {\"severity\": \"minor\", \"title\": \"The gate-status sentence is stale: 'fixes in progress' and 'fix round is in progress'\",\n   \"evidence\": \"product-note.md:26 'The combined M3+M4 gate failed with four blockers; fixes in progress.' part2-process.md:114 'failed with four blockers, and its fix round is in progress.' Both PDFs repeat it (note.txt:48, part2.txt:226). reviews/GATE-M3-summary.md says 'Result: pass (round 2, combined M3+M4 panel under D-075)', and board/milestones.md shows the M3 gate_result pass at 2026-11-03T15:18:34Z. T-215 and T-216 are done on the board\",\n   \"why_it_matters\": \"This is the 'In progress' status defect from round 1 in a new place. The note undersells a passed gate and tells Zlayt the build is still being fixed.\",\n   \"fix\": \"Say what happened in the past tense: 'the combined M3+M4 gate failed with four blockers, all fixed and verified (fixes at 43ce6eb and later)'. Re-render both PDFs; the note must stay at 1 page.\",\n   \"acceptance_test\": \"grep -c 'fixes in progress\\\\|fix round is in progress' on both .md files returns 0; the note PDF is still 1 page.\"},\n  {\"severity\": \"minor\", \"title\": \"Checklist section 7 still lists T-215 and T-216 as pending with their failure counts\",\n   \"evidence\": \"SUBMISSION_CHECKLIST.md:85 '| T-215 | backend | ... 10 unit failures |', :86 '| T-216 | frontend | ... 6 e2e failures |', :30 '(the spec copy of it is being aligned, T-215)'. The same §7 row 88 says 'Gate suite ... Done'. board.py list: T-215 done, T-216 done\",\n   \"why_it_matters\": \"The page Chris acts from contradicts itself and the board: red counts are listed as pending next to a row that says the suite is green.\",\n   \"fix\": \"Move T-215 and T-216 out of 'pending' (or mark them done at 43ce6eb) and drop 'is being aligned' from line 30.\",\n   \"acceptance_test\": \"§7 lists only cards that are not done on the board; grep 'being aligned' returns nothing.\"},\n  {\"severity\": \"nit\", \"title\": \"Small leftovers from my round-2 notes: the T-217 owner and the video length\",\n   \"evidence\": \"SUBMISSION_CHECKLIST.md:87 '| T-217 | qa |' while board.py shows role release. Checklist row 2 and NEEDS_CHRIS:26 say '174 s'; frames.py measured 173.16 s for the HEAD video\",\n   \"why_it_matters\": \"These are small mismatches with the board and the file.\",\n   \"fix\": \"Owner release; '173 s'.\",\n   \"acceptance_test\": \"The §7 owner matches board.py show T-217; the stated length is within 1 s of the video.\"}\n ],\n \"whats_right\": [\n  \"Row 5 now carries a number, a method, a committed evidence file and the earlier red run side by side, so a reader can see that the failure was found and fixed.\",\n  \"The re-recorded video matches the app: the new date sentence on the MRI charge, '(record dated ...)' in the Step 3 list and the exported letter, and Saved and Undo no longer hidden by the caption band.\",\n  \"The PDFs were re-rendered in the same commit as the markdown (1 and 4 pages) and match it line for line on the counts and paths.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-03T15:49:12.493Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-218-product-manager.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:13.500Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-218-product-manager.md",
 "description": "Validate the review file format"
}
````

### User / tool · 2026-11-03T15:49:13.624Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:18.964Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/project_t218_review.md",
 "content": "---\nname: t218-review-history\ndescription: T-218 verify (2026-11-03, HEAD e0d721d) passed; recurring stale-status and one-commit-behind green-run patterns\nmetadata:\n  type: project\n---\n\nT-218 PM verdict: pass (0 blockers, 0 majors, 4 minors, 1 nit). Both verify-pm-r2 majors closed: row 5 cites artifacts/gate-M3M4-suite-final.txt (5,945 unit / 614 e2e, 0 failed, at 43ce6eb); demo.webm re-recorded in c2dd104 and OCR of 30 frames is clean.\n\n**Why:** the packet keeps drifting behind the code. Late D-075 commit cd7fd27 (record-dated label) landed after the \"final\" suite and after the PDFs, so row 5 is one code commit behind HEAD and the note still says \"record or statement date\". Gate prose (\"fixes in progress\") and checklist section 7 (T-215/T-216 pending) went stale once the gate passed.\n\n**How to apply:** on any later packet check, diff `git log <suite commit>..HEAD -- app tests evals` against the cited run; grep the note and Part 2 for words the last decision removed (here \"statement\"); compare \"in progress\" and pending-list wording with `board.py list` and board/milestones.md. HEAD unit at e0d721d from my archive run: 5951 passed, 6 skipped (the committed file says 12 skipped; the total is the same, so the skip count is environment-dependent). Related: [[submission-doc-patterns]].\n"
}
````

### User / tool · 2026-11-03T15:49:19.054Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/project_t218_review.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:19.644Z

**tool call — Bash**
````
{
 "command": "tail -3 .claude/agent-memory/product-manager-reviewer/MEMORY.md",
 "description": "Check memory index tail"
}
````

### User / tool · 2026-11-03T15:49:19.720Z

**tool result**
````
- [Submission doc patterns](feedback_submission_doc_patterns.md) — M5 note/Part 2: built-claims ahead of HEAD, proxy-vs-human, working-tree counts, shared-index hazards, placeholder judgment, fix-text vs board (r1 fail, r2 changes, r3 pass)
- [Asset delivery patterns](feedback_asset_delivery_patterns.md) — GATE-M3M4: snapshot prunes assets, uncommitted cited rows, fallback-vs-round-N claims, video frames w/o ffmpeg, asset-before-fix order, archive test runs
- [T-017/T-018 review history](project_t017_t018_review_history.md) — r1, r2, and r3 apply-check verdicts (all changes); open: owner rows, self-check claim, cut-order claim, T-018 AC2 evidence
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:21.448Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md",
 "old_string": "- [T-017/T-018 review history]",
 "new_string": "- [T-218 review history](project_t218_review.md) — pass at e0d721d; packet lags code (green run one commit behind, stale \"in progress\", \"record or statement\")\n- [T-017/T-018 review history]"
}
````

### User / tool · 2026-11-03T15:49:21.539Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:24.342Z

T-218: **pass** at HEAD e0d721d with 0 blockers, 0 majors and 4 minors plus 1 nit. Both r2 majors are closed: row 5 and Part 2 cite `artifacts/gate-M3M4-suite-final.txt` (5,945 unit and 614 e2e, 0 failed), and `demo.webm` was re-recorded in c2dd104. The video frames, "will be burned in", "statement dated" and the PDFs all check out. Review written to `/Users/arsis/zlayt-pm-project/reviews/T-218-product-manager.md` and passes `board.py validate`.

The minors: the note and Part 2 still say "record or statement date" after D-075, the cited green run is one code commit behind HEAD (cd7fd27), and the "fixes in progress" wording and checklist §7 are stale.

I did not re-run e2e at HEAD. A fresh-archive unit run at HEAD gave 5951 passed, 6 skipped, 0 failed.
