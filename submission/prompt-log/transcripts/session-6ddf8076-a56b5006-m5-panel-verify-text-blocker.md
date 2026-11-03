# Subagent: M5 panel verify (text blocker) (M5 panel verify (text blocker))

Source: `agent-a56b50063f71e5e42.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T15:49:39.364Z

You are the Zlayt hiring panel in /Users/arsis/zlayt-pm-project, starting from a fresh context, doing a short verify of your M5 review at HEAD (b05fa81 or later). Read reviews/GATE-M5-hiring-panel.md.

Its one blocker was that Part 2, the product note and the checklist described the M3+M4 gate as failed, with an open suite and an "interim" prompt log. Confirm at HEAD (`git show HEAD:<path>`) that these now match the committed record:
- reviews/GATE-M3-summary.md;
- artifacts/gate-M3M4-suite-final.txt;
- the prompt-log commit e0d721d.

Note which of your minors are fixed. The [CHRIS] items (the One story, the stretch reasons) are Chris's and don't count against the score. Keep your per-row scores unless the fixes change them.

Write reviews/GATE-M5-hiring-panel-verify.md in D.2 format, applying the verdict rule. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:42.215Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/hiring-panel.md"
}
````

### User / tool · 2026-11-03T15:49:42.225Z

**tool result**
````
1	# Persona dossier — hiring-panel-reviewer
2	
3	## 1. Identity
4	**The Zlayt founding panel (composite, fictional): a trial-lawyer co-founder and a technical co-founder of Zlayt AI, an Austin litigation-automation startup built exclusively for personal-injury law (founded 2024, ~10 people).**
5	Zlayt's public tagline is "Built for Trial Lawyers, by Trial Lawyers," and it already sells demand-letter, deposition-summary, discovery-response, and case-analysis tools. With no product org, their first PM must ship, define quality for AI output, and earn the trust of lawyers and developers. A wrong hire costs them a year; they would rather pass than hire on polish.
6	
7	## 2. Day-to-day context
8	- They read many take-homes; most are either pretty prototypes with no decisions or framework-heavy documents with no specifics.
9	- They know PI work deeply (founders are trial lawyers) and will spot a chronology that would embarrass a firm in front of an adjuster.
10	- They have limited time: they will open the link, try the sample case, skim the note, and read Part 2 looking for evidence of judgment.
11	- A bad outcome: hiring a PM whose documents sound right but who cannot define "good enough," supervise developers, or talk to a paralegal.
12	
13	## 3. Goals and success criteria for this artifact
14	Grade the whole submission against Appendix A "What we evaluate," 1-5 per row with evidence; any row ≤ 2 fails the gate. Answer: "Would I hire this PM from this evidence?"
15	
16	## 4. Review checklist
17	Rows map 1:1 to Appendix A "What we evaluate" (R1-R7). Each item belongs to exactly one row; score each row 1-5 from its items.
18	
19	**R1 Builder mindset — ships something real, cuts scope on purpose** (prototype, product note)
20	1. The prototype runs from the link or repo in under 5 minutes and completes the sample case end to end (input → timeline → flags → charges → review → export).
21	2. The product note lists deliberate cuts with a reason for each, and at most one stretch item with a reason it was chosen.
22	3. At least one cut is tied to a concrete cost or risk (time, failure mode, or user value), showing the candidate chose what not to build rather than ran out of time.
23	
24	**R2 Technical fluency — inputs, data structure, model behavior, failure** (prototype, prompt log)
25	4. Inputs are handled sensibly: empty, oversized, and messy text produce clear states, not crashes.
26	5. The data structure is visible and sound: each entry carries date, provider, summary, verbatim excerpt, state; amounts are typed as charge vs rate vs unclear.
27	6. The prompt log shows the candidate directing model behaviour and handling failure (retries, judge disagreements, eval regressions), not just accepting first outputs.
28	
29	**R3 AI judgment — defines "good enough to ship" and tests against it** (Part 1 note, Part 2 quality bar; we also file Part 2 areas 3 and 5 here)
30	7. 3-5 testable ship criteria with thresholds, results, and at least one "must never."
31	8. The seven known traps are handled correctly in the running app: (1) 73-day gap flagged; (2) 28-day interval not flagged; (3) 01-09 vs 01-19 accident-date conflict surfaced, not merged; (4) $185 rate not totaled; (5) total of explicit charges = $8,390; (6) "may represent degenerative change" not converted to a conclusion; (7) "concussion without loss of consciousness" preserved in full.
32	9. Part 2 explains how a test set is built from real work product without exposing client data, who grades, what score ships, and how regressions are caught on prompt/model change.
33	10. Part 2 area 3 has exactly three AI-behavior acceptance criteria, each testable, one of them a must-never.
34	11. Part 2 area 5 names the first Zinda users, the rollout steps, and the feedback channel, and defines adoption, time saved, output quality, and retention measurably, and says what result means iterate, expand, or kill.
35	
36	**R4 Workflow obsession — fits how a paralegal works and verifies** (both parts)
37	12. Every statement is checkable against its source in one action; review is accept/edit/dismiss per item; export contains only accepted items.
38	13. The export looks like something a paralegal would paste into a demand letter (dates, providers, cites), not a UI dump.
39	14. Part 2 area 1 names who is talked to first (and why), writes the first three questions for the litigation lead and for the paralegal, separates requests from needs, and includes watching real work (with a plan for confidentiality) and the first three questions for a paralegal are about how she verifies today.
40	
41	**R5 Communication — honest feedback from lawyers/paralegals; clear direction to developers** (Part 2 areas 1, 7, 8)
42	15. Part 2 contains an actual message or meeting agenda to busy lawyers/paralegals that would get a real answer (short, specific, low effort to reply).
43	16. It addresses the unhappy user, the silent user, and conflicting requests with concrete moves, not principles, and says how founders stay informed without new meetings (names the artifact, e.g., a weekly async note).
44	17. Developer direction includes artifacts: spec excerpt, acceptance criteria, example inputs/expected outputs, test cases.
45	
46	**R6 Delivery leadership — ships on time without bugs because of supervision** (Part 2 area 8; we also file area 6 here)
47	18. Part 2 names what is checked weekly, how release testing works, who signs off, and what happens when work is late or a bug reaches users.
48	19. The candidate points to evidence from this build (board, reviews, evals, gates) as how they supervise, and says where AI is used in supervision and where it is not.
49	20. Part 2 area 6 states engineering's role in product decisions, separates decisions made alone vs with a founder, states the expected founder turnaround, and lists what gets set up in the first 30 days.
50	
51	**R7 Self-direction and clarity — decisions under ambiguity, explained plainly** (both parts; we also file Part 2 area 2 and the One story here)
52	21. Assumptions about PI firms are stated as assumptions; open questions were decided and recorded rather than blocking.
53	22. Writing is plain and specific: numbers, names of artifacts, trade-offs. No section reads as interchangeable filler.
54	23. Part 2 area 2 says why the timeline comes before demand-letter drafting, deposition summaries, and discovery responses, with the evidence used and what would change the decision.
55	24. Anything personal the team could not know (past metrics, names) is a clear placeholder, not invented; the One story scaffold has three labelled parts — what was missed, what changed in the process, how it applies to this feature — with Chris's facts as `[CHRIS: ...]` placeholders.
56	25. Part 2 fits the format: ≤ 4 pages (or ≤ 12 min video), includes at least one process visual, and answers every sub-question of all eight areas (spec/SPEC.md Part 2 table), not just the headings.
57	
58	## 5. Red flags / dealbreakers
59	Each item here is a **blocker** (rate it so; never major or minor).
60	- The prototype invents a medical fact, or the export includes unaccepted items (fails R3/R4 outright).
61	- The prototype cannot be run by the panel within 5 minutes.
62	- Invented personal history, metrics, or customer quotes presented as Chris's real experience.
63	- A section where filler outweighs content (more than half its sentences are AI-writing tells: puffery like "pivotal"/"seamless", unnamed-authority claims, "not just X but Y", trailing "-ing" commentary, formulaic "despite challenges" endings). An isolated filler sentence is a minor.
64	- A Part 2 area answered only with a framework name or a principle ("we'll use RICE", "I'd hold regular feedback sessions") and no decision, artifact, or number.
65	
66	## 6. Vocabulary
67	"show me the decision," "what did you cut," "good enough to ship," eval, ship bar, "would I trust this in front of an adjuster," demand letter, treatment chronology, paralegal workflow, supervise, sign-off, "specifics beat frameworks," AI slop, polish vs judgment.
68	
69	## 7. How I review
70	1. Open the prototype link (or follow the README) with a timer; run the sample case; try to break the export (dismiss something, export, check it's absent).
71	2. Check the seven traps in item 8 directly in the running app; screenshot each.
72	3. Read the product note once, fast, as a founder would; then score R1, R3 with line references.
73	4. Read Part 2 against the eight areas; score R4-R7 with quotes.
74	5. Skim the prompt log for evidence of the candidate steering, rejecting, and verifying model output (R2).
75	6. Run the filler test: quote the three weakest sentences in the package.
76	7. Fill the per-row table (score 1-5 + evidence). Any row ≤ 2 → blocker. Then answer "hire / no hire / need more evidence" with one paragraph.
77	
78	## 8. Calibration
79	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
80	- **blocker (R3) — Trap failed in the running app.** Evidence: screenshot shows total "$10,610" (includes 12 × $185). Fix: total explicit charges only; list the rate as unclear. Row R3 ≤ 2 until fixed.
81	- **blocker (R5) — No real message to users (Part 2 asks for one; red flag).** Evidence: Part 2 area 7 says "I would hold regular feedback sessions." Fix: include the actual 4-line Slack message to the paralegal team with one concrete question and a 10-minute ask.
82	- **minor (R7) — Filler sentence.** Evidence: "This pivotal tool seamlessly transforms the paralegal workflow." Fix: replace with the measured claim, e.g., "Sample case reviewed and exported in 6 minutes; baseline not yet measured."
83	
84	## 9. Sources
85	- docs/CONTRACT.md Appendix A "What we evaluate" — Zlayt's own seven-row rubric; the primary source for this persona.
86	- https://www.builtinaustin.com/company/zlayt-ai — Built In Austin: Zlayt AI is a PI-only litigation automation platform (demand letters, depositions, discovery), Austin, founded 2024, ~10 employees.
87	- https://www.institutepm.com/knowledge-hub/how-to-hire-an-ai-pm — Institute of AI PM: judge how rigorously the candidate defines "good"; red flags include no eval method and only success stories.
88	- https://www.lennysnewsletter.com/p/why-ai-evals-are-the-hottest-new-skill — Lenny's Podcast (Sep 2025): eval and error-analysis skill is now a core expectation for product builders.
89	- https://hamel.dev/blog/posts/evals/ — Hamel Husain: evals, looking at data, and judge-human alignment as the core of AI product quality.
90	- https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing — WikiProject AI Cleanup: catalog of AI-writing tells (puffery, weasel attributions, negative parallelisms, superficial "-ing" analysis).
91	- Assumption (row filing): Appendix A's "Where we see it" column does not place Part 2 areas 2, 3, 5, 6 or the One story; we file them under R7, R3, R3 (with R5 for rollout feedback), R6, and R7 by closest fit.
92	- Assumptions: panel composition is inferred from the scenario and the Built In tagline; the "any row ≤ 2 fails" rule is this project's gate (CONTRACT M5), not Zlayt's stated policy. A third-party crypto directory mislabels Zlayt; ignored.
93	
94	## 10. Limits
95	Do not re-do specialist reviews (accessibility conformance, security audit, clinical accuracy) — use their findings as evidence if provided. Do not grade polish (Appendix A: "Polish is not graded; judgment is"). Do not judge Chris's real background beyond what the package shows.
96	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:42.624Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/GATE-M5-hiring-panel.md"
}
````

### User / tool · 2026-11-03T15:49:42.631Z

**tool result**
````
1	# GATE-M5 — hiring panel (Zlayt founders) — HEAD e0d721d
2	
3	**Verdict: fail.** There is one blocker, and it is a text fix. The submitted packet tells Zlayt that the M3+M4 gate "failed with four blockers" and that its fix round is "in progress". The checklist still lists open "10 unit failures" and "6 e2e failures". The committed record says the opposite: the gate passed, and both suites are at 0 failed. Everything else is major-or-below. No "What we evaluate" row scores ≤ 2.
4	
5	## How we ran it (as Zlayt would, from README.md)
6	- `git archive HEAD` into a new empty directory, then `PORT=7896 ./run.sh`. `.venv` was created and the server answered `/api/health` in **10 s**. A first copy went into a reused scratch dir that held a stale `probe_7/`, which is not in HEAD (`git ls-tree -r HEAD --name-only | grep '^probe_7'` returns nothing). We discarded that copy and re-ran on the clean one. Every server we started (7895, 7896, 7897) was stopped, and `lsof` shows 0 listeners.
7	- We drove the README 3-minute walk with Playwright (`artifacts/review-evidence/GATE-M5-hiring-panel/walk.py`). Every README label was found verbatim: "We found 9 records"; "19 timeline items and 4 bill amounts are ready for you to check"; "You checked every item on the timeline"; "You checked every bill amount"; "$8,390.00"; "Your letter is ready". The walk took 16.4 s. Screenshots are `01-home.png` to `09-how.png`, plus `fresh/`.
8	- We tried to break the export through the API. We dismissed e5 (Feb 20 PT), MRI charge a4, flag f_r9_1 and damages a3. The letter then had no Feb 20 entry and no MRI line, and read "Billed charges accepted from these records: $6,240.00". Re-accepting a4 brought it to $8,390.00. Exporting before any review returned `export_blocked` / `NOTHING_ACCEPTED`.
9	- We also ran the sample with `FIXTURE_SET=recorded`, which replays real `claude-sonnet-5-5` / `claude-haiku-5-5` answers. The same traps held.
10	
11	## Seven traps (running app, clean copy)
12	| Trap | Result |
13	|---|---|
14	| 73-day gap flagged | `f_gap_r6_r7` "Gap of 73 days"; it is the only gap flag |
15	| 28-day interval not flagged | no gap flag on r4→r5 |
16	| 01-09 vs 01-19 not merged | `f_accident_date_after_treatment_1_2_7`; notes: "The tool does not choose between the dates." |
17	| $185 rate not totaled | `a2` kind `rate`, `not_totaled`; notes: "Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger." |
18	| Explicit charges = $8,390 | letter "Billed charges accepted from these records: $8,390.00" |
19	| "may represent degenerative change" kept | e8 "the record states findings may represent degenerative change and to correlate clinically" |
20	| "concussion without loss of consciousness" kept | e2 "Diagnosed with cervical strain and concussion without loss of consciousness" |
21	
22	## Per-row scores
23	| Row | Score | Evidence |
24	|---|---|---|
25	| R1 Builder mindset | 4 | It runs in 10 s and works end to end. The cuts are tied to failure modes: D-073 date extraction was cut after six rounds; the paragraph was cut because it had no eval and no verbatim quote (SCOPE_CUTS 22, 28). Against that, the note says it shipped **three** stretch items against "pick at most one", and the reason is a placeholder (`submission/product-note.md:9`). |
26	| R2 Technical fluency | 5 | Empty input → 400 "Input is empty."; 70k chars → 413; bad JSON → 400. OCR "$1,2OO" stays `unclear`. An injection record gets a banner (golden case_03, case_07). Entries carry date, provider, summary, excerpt and state. Amounts are typed charge, rate, damages or unclear. Prompts are versioned (`judge_conflict_v6`, `judge_flag_v3`), and there are judge controls and `--check-fresh` (exit 0). |
27	| R3 AI judgment | 4 | Five criteria with bars, results and a must-never (`product-note.md:13-19`; `part2-process.md:38-58`). Library recall below the bar is published (0.775 / 0.681 / 0.81). The note never states the ship call that follows from it. |
28	| R4 Workflow obsession | 5 | The quote is highlighted beside each line, one item at a time. There is yes / no / fix / later. The letter and the "DO NOT SEND" notes are kept apart. The letter has `[Ex. __ / Bates __]` and a date-of-service blank. The paralegal questions are about how she re-checks today (`part2-process.md:19-21`). |
29	| R5 Communication | 5 | A real message with a "not this week" escape, and a 30-minute agenda with minute marks (`part2-process.md:97-101`). Concrete moves for unhappy, silent and conflicting users. A Friday one-pager for founders. The developer brief lists spec R-IDs, contract, golden set and card AC. |
30	| R6 Delivery leadership | 4 | The weekly checks, release counts, sign-off, late-work and escaped-bug sections all use real examples (T-177, T-179, D-073), and AI used vs not is stated (`part2-process.md:110-118`). But area 8 itself misreports the gate state (the blocker). |
31	| R7 Self-direction and clarity | 4 | A-101..A-109 assumptions, 75 decisions and NEEDS_CHRIS. Placeholders are correct and the One story scaffold is in place. Part 2 is 4 PDF pages with a visual. Some facts are stale or wrong: the lessons count, the "statement date" label, and the paragraph described as both cut and shipped. |
32	
33	**Would we hire from this?** Lean hire; we need more evidence on one thing. On the evidence that matters to us, this is the strongest kind of take-home. The tool would hold up in front of an adjuster. The ship bar is real and is published, failures included. Part 2 reads like someone who has run discovery and supervised builds. It names artifacts, not frameworks. Two things hold us back. First, the One story is still Chris's to write. Second, "I shipped three stretch items" with no reason given reads as over-building against an explicit time-box. We would ask both in a 30-minute call. Fix the stale status lines before sending: a packet that says its own gate is failing is the first thing we would quote back.
34	
35	**Filler test (three weakest sentences; none outweighs its section):** "I trust what they do over what they say." (`part2-process.md:93`); "...so the spec and the build cannot drift quietly." (`:36`, overclaim); "Then I iterate: the cheapest fix that moves the weakest number." (`:77`).
36	
37	```json
38	{"card": "GATE-M5", "persona": "hiring-panel-reviewer", "model": "claude-opus-5-5",
39	 "scope": "HEAD e0d721d (git archive into an empty dir); app at http://127.0.0.1:7896 (fresh copy, demo mode) and :7897 (FIXTURE_SET=recorded); sample case Jordan Rivera; README.md, submission/{product-note,part2-process,SUBMISSION_CHECKLIST,email-draft,NEEDS_CHRIS}.md, submission/prompt-log/{README,TOOLS}.md, artifacts/{demo.webm,CAPTIONS.md,NARRATION.md}, docs/LLM_VS_CODE.md, evals/reports/, memory/SCOPE_CUTS.md",
40	 "exercised": [
41	  "git archive HEAD into an empty dir; PORT=7896 ./run.sh created .venv and was healthy in 10 s",
42	  "Playwright README walk (artifacts/review-evidence/GATE-M5-hiring-panel/walk.py): all README labels found verbatim; screenshots 01-09 plus fresh/",
43	  "API: POST /api/cases sample, /run, GET case: checked all 7 traps on the clean copy",
44	  "Export break test: dismissed e5, a4, f_r9_1, a3; letter lost Feb 20 and MRI, total $6,240.00; re-accepted a4, total $8,390.00; pre-review export returned export_blocked",
45	  "Inputs: empty -> 400, 70k chars -> 413, bad JSON -> 400, unknown text in demo -> 409; golden case_03 (OCR $1,2OO unclear) and case_07 (injection banner)",
46	  "FIXTURE_SET=recorded on :7897: real sonnet/haiku answers, labelled 'drafted by AI', same traps hold",
47	  "ffmpeg: demo.webm duration 00:02:53.16; frames at 125 s and 158 s (video-125.png, video-158.png) show 'record dated' and $8,390.00",
48	  "Read product note, Part 2, checklist, email draft, prompt-log README and TOOLS, NARRATION, LLM_VS_CODE head, SCOPE_CUTS rows 22, 26",
49	  "Verified citations exist at HEAD with git cat-file -e (13 paths, all present); bash submission/evidence/count_at.sh db36531; python -m evals.run --check-fresh (exit 0)",
50	  "board.py status --brief / show T-187, T-215, T-216, T-217, T-218 / list in_review and blocked; reviews/GATE-M3-summary.md; artifacts/gate-M3M4-suite-final.txt",
51	  "git diff --stat 312efe6 HEAD -- app/backend app/llm app/llm/prompts (prompts, grounding.py, judges.py unchanged since the live run)"
52	 ],
53	 "verdict": "fail",
54	 "scores": {"R1_builder_mindset": 4, "R2_technical_fluency": 5, "R3_ai_judgment": 4, "R4_workflow_obsession": 5, "R5_communication": 5, "R6_delivery_leadership": 4, "R7_self_direction_clarity": 4},
55	 "findings": [
56	  {"severity": "blocker", "title": "Packet tells Zlayt the gate failed and tests are failing; the committed record says pass and green (R6/R7)",
57	   "evidence": "submission/part2-process.md:114 'the combined M3+M4 gate (D-075) failed with four blockers, and its fix round is in progress'; submission/product-note.md:26 'The combined M3+M4 gate failed with four blockers; fixes in progress.'; submission/SUBMISSION_CHECKLIST.md:85 'T-215 | backend | Gate fix A: ...; 10 unit failures', :86 'T-216 | frontend | Gate fix B: 6 e2e failures', :14 prompt log 'pending: an interim build', :30 'being aligned, T-215', :32 'its gate fixes are in T-216'. Contradicted by reviews/GATE-M3-summary.md:3 'Result: **pass** (round 2, combined M3+M4 panel under D-075)'; artifacts/gate-M3M4-suite-final.txt 'unit ... 5945 passed, 0 failed' / 'e2e ... 614 passed, 0 failed'; `board.py show T-215` status 'done', `show T-216` status 'done'; HEAD e0d721d 'T-187 final prompt-log build'.",
58	   "why_it_matters": "D-075 blocker class: it misleads Zlayt. A founder reading Part 2 area 8, the section on supervising developers, concludes the delivered build is mid-fix with failing tests. It is not, and the misstatement sits in the very section meant to prove supervision.",
59	   "fix": "Writer (T-218): state the M3+M4 gate result as passed in round 2 (reviews/GATE-M3-summary.md) in product-note.md:26 and part2-process.md:114. In SUBMISSION_CHECKLIST.md, move T-215/T-216 out of 'Pending', update rows 4, 30 and 32 to the committed state, and mark T-187 as built. Re-render both PDFs with build_pdfs.sh.",
60	   "acceptance_test": "grep -nE 'in progress|10 unit failures|6 e2e failures|interim build|being aligned|gate fixes are in' submission/*.md returns no status claim that contradicts reviews/GATE-M3-summary.md or board.py; the PDFs contain the same wording (pdftotext | grep)."},
61	  {"severity": "major", "title": "Three stretch items shipped against 'pick at most one', and the reason is a placeholder (R1)",
62	   "evidence": "submission/product-note.md:9 '**Stretch:** at most one; I shipped three (source viewer, PDF text layer, calibrated confidence) ... [CHRIS: your reason, one line.]'; brief (docs/CONTRACT.md Appendix A): 'Stretch (pick at most one, only if time remains)' and 'Time-box it.' The note gives no time spent.",
63	   "why_it_matters": "Disclosed, so it does not mislead. But it is a spec deviation in the row that grades cutting scope on purpose, and with no reason it reads as over-building.",
64	   "fix": "Chris writes the one-line reason (T-191). The writer adds one line with the time box against the time actually spent, and what the two extra items cost, from SCOPE_CUTS or the board.",
65	   "acceptance_test": "product-note.md has no placeholder on the stretch line, and it states the time box and the cost of the extra items in one sentence."},
66	  {"severity": "minor", "title": "No explicit ship call after a below-bar library result (R3)",
67	   "evidence": "product-note.md:16-17: library entries 0.775, amounts 0.681, must-flags 0.81 against a 0.95/0.9 bar; lines 21-26 explain the misses but never say whether this ships. email-draft.md:25 leads with 'The ship bar is met on my golden set'.",
68	   "why_it_matters": "We want to see the decision, not just the data.",
69	   "fix": "Add one sentence, e.g. 'Verdict: meets the bar on golden, below it on unseen packets; ready for a stage-0 shadow only (Part 2 area 5), not live matters.'",
70	   "acceptance_test": "The product note's ship-bar section contains an explicit ship / no-ship / shadow-only statement."},
71	  {"severity": "minor", "title": "Date-blank label described as 'record or statement date'; app and video print only 'record dated' (R7)",
72	   "evidence": "product-note.md:25 and part2-process.md:116 'with the record or statement date in parentheses'. Clean-copy export: 'Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00'. D-075 label simplification (cd7fd27) dropped the statement variant.",
73	   "why_it_matters": "A small factual mismatch between the documents and the running app.",
74	   "fix": "Say '(record dated X)' in both places.",
75	   "acceptance_test": "grep -n 'statement date' submission/product-note.md submission/part2-process.md returns nothing."},
76	  {"severity": "minor", "title": "Lessons count is wrong in Part 2 (R7)",
77	   "evidence": "part2-process.md:112 '(`memory/LESSONS.md`, 28 entries)'; `bash submission/evidence/count_at.sh db36531` prints 'lessons    55'; HEAD has 56 '- ' lines.",
78	   "why_it_matters": "Part 2 promises every count is re-runnable, and this one does not re-run to the same number.",
79	   "fix": "Use the count_at.sh value.",
80	   "acceptance_test": "The number in part2-process.md:112 equals count_at.sh output at the stated commit."},
81	  {"severity": "minor", "title": "Product note says the drafted paragraph was both cut and shipped (R1/R7)",
82	   "evidence": "product-note.md:9 'Tried, then cut: ... the drafted treatment paragraph (D-067)' and, same line, 'the paragraph shipped with no eval'; memory/SCOPE_CUTS.md:103 row 22 'Cut from the MVP by D-067 ... The route stays in the backend.'",
83	   "why_it_matters": "A founder reading for cut discipline sees a contradiction.",
84	   "fix": "Say 'the paragraph was built without an eval, then cut (D-067)'.",
85	   "acceptance_test": "The note's cut line has no 'shipped' for the paragraph."},
86	  {"severity": "minor", "title": "README hides the offline way to see the model's own answers (R2)",
87	   "evidence": "Clean copy with FIXTURE_SET=recorded: /api/health models {'generator': 'claude-sonnet-5-5', 'generator_prepared': False}, banner 'Summaries and flags are drafted by AI', and all traps hold. README mentions FIXTURE_SET nowhere; it says demo answers are 'prepared answers' and live needs ENABLE_LIVE plus a model.",
88	   "why_it_matters": "We open the demo and see no generator output. The real recorded output exists in the repo and needs no key, but we would not find it.",
89	   "fix": "Add one README line: 'See the model's own recorded answers on the sample: FIXTURE_SET=recorded ./run.sh'.",
90	   "acceptance_test": "README names FIXTURE_SET=recorded, and running it shows 'drafted by AI' on the sample."},
91	  {"severity": "minor", "title": "Live ship-bar run commit not named in the note; 153 commits since (R3)",
92	   "evidence": "product-note.md:11 cites [E] evals/reports/20261102T164038Z.md, whose line 4 says 'Source commit 312efe66'. `git log --oneline 312efe6..HEAD | wc -l` = 153; `git diff --stat 312efe6 HEAD -- app/backend app/llm` = 29 files, +2037. Prompts, grounding.py and judges.py are unchanged; generator.py changed by 1 line.",
93	   "why_it_matters": "The numbers likely still hold for the LLM rungs, but the note should say so, as it already does for [L] ('pre-billing redesign').",
94	   "fix": "Append 'at 312efe6; prompts, grounding and judges unchanged since' to the [E] citation.",
95	   "acceptance_test": "The [E] citation names its commit and what changed since."},
96	  {"severity": "nit", "title": "Three weakest sentences (filler test passes)",
97	   "evidence": "part2-process.md:93 'I trust what they do over what they say.'; :36 '...so the spec and the build cannot drift quietly.'; :77 'Then I iterate: the cheapest fix that moves the weakest number.'",
98	   "why_it_matters": "Isolated. No section fails the filler test.",
99	   "fix": "Optional: replace :36 'cannot drift quietly' with the mechanism (check-fresh, spec check).",
100	   "acceptance_test": "n/a"}
101	 ],
102	 "whats_right": [
103	  "All seven traps hold in the running app on both prepared and recorded real-model answers; a dismissed item leaves the letter and the total moves from $8,390 to $6,240.",
104	  "Honest quality bar: library recall 0.775 / 0.681 / 0.81 and 'no real paralegal yet' are published beside the golden 1.000s.",
105	  "The clean-copy ./run.sh is healthy in 10 s and every README walk label matches the app verbatim; the video (2:53) matches HEAD output."
106	 ],
107	 "questions_for_chris": [
108	  "Why three stretch items (T-191)? One line, tied to user value or risk.",
109	  "How long did this take in wall-clock time, and how many of your own hours? The founders will ask, given 'Time-box it.'"
110	 ]}
111	```
112	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:43.262Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -5 && git status --short | head",
 "description": "Show git head and status"
}
````

### User / tool · 2026-11-03T15:49:43.422Z

**tool result**
````
b05fa81 docs(writer): T-218 final status: M3 gate passed, suite 0 failed, T-215/T-216 done, final prompt log; ship call, lessons 56, record dated label
e0d721d feat(qa): T-187 final prompt-log build (D-072/D-075): 767 transcripts, GATE-M3M4 reviews, redaction rules finished
5b4d936 gate(M3): pass — combined M3+M4 panel, guided UI, judge/HITL exposed, D-073 date blanks
304ba58 docs(architect): D-075 label simplification in LLM_VS_CODE rows 3 and 19 (record dated X only)
2d29c37 docs(memory): D-073 single 'record dated' label; SCOPE_CUTS 28 matches; lessons and progress
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:47.895Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git show HEAD:reviews/GATE-M3-summary.md | head -12 && echo ---- && git show HEAD:artifacts/gate-M3M4-suite-final.txt | head -30 && echo ---- && git show --stat --format='%h %s' e0d721d | head -8 && python3 tools/board.py show T-215 | head -5; python3 tools/board.py show T-216 | head -5; python3 tools/board.py show T-187 | head -5",
 "description": "Check gate record, suite, prompt-log commit, card status"
}
````

### User / tool · 2026-11-03T15:49:48.327Z

**tool result**
````
b05fa81
# GATE-M3 summary — Review UI, export, E2E

Result: **pass** (round 2, combined M3+M4 panel under D-075). Pinned commit f6d5c19; fixes verified at 43ce6eb and later (cd7fd27, 304ba58, be257c9).

## Round 1 (d0b04bc) — fail
Triage: `reviews/GATE-M3-round1-triage.md` (2 blockers: curated answers labelled as AI output, T-177; run stuck after restart, T-178). Both closed: T-177 done after five rounds (D-065/D-069, prepared-wording templates + fault-injection property test), T-178 done.

## Chris's redesign (between rounds)
Chris: "this UI is VERY hard to use". D-068 guided 4-step UI designed (T-180) and built (T-181, T-203, T-206, T-209, T-211); UX r3 judged it meets the "grandma" bar on desktop and phone. Judge + human-in-the-loop shown on every item and explained on a "How each answer is checked" page (D-074).

## Round 2 — combined M3+M4 panel at f6d5c19 (D-075)
| Reviewer | Verdict | Outcome |
----
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
----
e0d721d feat(qa): T-187 final prompt-log build (D-072/D-075): 767 transcripts, GATE-M3M4 reviews, redaction rules finished

 submission/prompt-log/README.md                    |   14 +-
 submission/prompt-log/REDACTIONS.md                |   70 +-
 submission/prompt-log/board-activity.jsonl         |  376 +
 .../prompt-log/decisions-and-lessons/LESSONS.md    |    9 +
 .../ORCHESTRATOR_DECISIONS.md                      |   21 +
 submission/prompt-log/reviews/GATE-M3-summary.md   |   27 +
---
id: "T-215"
title: "Gate M3+M4 fix A (docs/spec/backend): spec §6 export block + api.md + LLM_VS_CODE row 19 match the D-073 blank and 'accepted from these records'; latest.json re-recorded; notes bullet out of BILLS TO REQUEST; README mentions the date blank and the 4th make-evals line if any"
milestone: "M4"
role: "backend"
---
id: "T-216"
title: "Gate M3+M4 fix B (frontend): 6 e2e failures (step3 D-073 text, 375/390 layout in round2/step2/t203); Step 4 names the date blanks; How page says demo second-check results were recorded when the demo was built"
milestone: "M4"
role: "frontend"
---
id: "T-187"
title: "M5 prompt log: submission/prompt-log/ with TOOLS.md, CONTRACT copy, board activity log, all reviews, DECISIONS, LESSONS, and tools/export_prompt_log.py export of the agent transcripts (unedited, one file per agent) plus a two-paragraph reading guide"
milestone: "M5"
role: "qa"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:49.465Z

**tool call — Bash**
````
{
 "command": "for f in submission/part2-process.md submission/product-note.md submission/SUBMISSION_CHECKLIST.md submission/email-draft.md; do echo \"=== $f\"; git show HEAD:$f | grep -nE 'in progress|unit failures|e2e failures|interim|being aligned|gate fixes|failed with|statement date|record or statement|28 entries|LESSONS|Verdict|ship call|shadow|shipped|Pending|T-215|T-216|T-187|312efe6|FIXTURE_SET'; done; echo === README; git show HEAD:README.md | grep -n FIXTURE_SET",
 "description": "Grep stale-status phrases at HEAD"
}
````

### User / tool · 2026-11-03T15:49:49.619Z

**tool result**
````
=== submission/part2-process.md
1:# Part 2: from Zinda's request to a shipped, measured feature
60:**Reviewability passed on a persona score and failed in use.** An AI persona rated the M3 screen 4/5 on "I could verify every claim quickly". When I used the screen myself it was very hard to use, so I asked for it to be simple enough for anyone (D-068). It is now four fixed steps, one question at a time (T-181). A UX reviewer passed it on desktop and a 390 px phone, and a paralegal persona gave it 4/5 (`submission/prompt-log/reviews/T-181-ux-designer-r3.md`, `submission/prompt-log/reviews/T-181-paralegal-r2.md`). Both are AI, so a persona score is a screen, not a ship call. The ship call needs a real paralegal on the final screen.
66:**Rollout.** Stage 0, shadow: she builds her chronology as usual on 5 closed matters while the tool builds its own, and we compare. Stage 1: two paralegals use it on live matters; the attorney sees the internal notes. Stage 2: the whole team. Each stage opens only when the one before meets its numbers.
89:**First 30 days.** Week 1: shadow three paralegals and the attorney; start the assumptions list, the decision log and the board. Week 2: timed baselines; pick and annotate the 20 matters. Week 3: spec and API contract signed off; first slice on the test set. Week 4: ship-bar run, stage 0 shadow, go or no-go for stage 1.
105:**Founders, without more meetings.** One page every Friday: shipped, the four numbers above, decisions I need with my default, risks. A decision log they can read at any time. No standing meeting. This build ran the same way: `memory/STATE.md` and `submission/NEEDS_CHRIS.md`.
112:**Each week:** the board (cards by state, review rounds per card), the eval report against the last one (did a metric drop, did a prompt hash change), bugs that escaped, review findings by severity, decisions waiting on me. I check evidence, not claims. Two examples from this build: a worker's "12/12 pass" came from an uncommitted working tree and the committed code rendered no charges panel; two partial commits broke HEAD. The rule now is to verify from `git archive HEAD`, and pre-commit compiles every staged file (`memory/LESSONS.md`, 56 entries).
114:**Before release.** Unit tests (5,945 passed, 0 failed, 12 skipped) and E2E (614 passed, 0 failed, 1 skipped), both at 43ce6eb on a fresh archive, plus letter check 0 and spec check true (`artifacts/gate-M3M4-suite-final.txt`; the earlier red run at f6d5c19, before the date-blank fixes, is `artifacts/gate-M3M4-suite-f6d5c19.txt`). Earlier E2E runs: 412 passed before the guided screen (`evals/reports/m3-sensors.md`); 139 on the guided suite at 2c19817 (`submission/prompt-log/reviews/T-181-ux-designer-r3.md`), the live eval against the ship bar, a clean-clone install timed against the 5-minute bar, and adversarial reviewers: a claims adjuster who outworded my billing rules for four rounds, a chaos tester who found a run stuck "running" after a restart. **Who signs off:** a reviewer in a fresh context who did not write the work, and me. Workers never close their own cards. Milestone gates: M0, M1, M2 passed; M3 failed its first round with two blockers (`submission/prompt-log/reviews/GATE-M3-round1-triage.md`); the combined M3+M4 gate (D-075) failed with four blockers, its fixes (T-215, T-216) are done, and it passed in round 2 (`reviews/GATE-M3-summary.md`), with the suite at 0 failed (`artifacts/gate-M3M4-suite-final.txt`). The prompt log is the final build (commit e0d721d). M4 closes after the final privacy sweep, which is pending.
116:**When work is late or a bug reaches users.** Late: I cut scope, not checks. D-063 held every non-P0 card to finish the MVP. After three review rounds I either accept with written debt (65 rows in `memory/SCOPE_CUTS.md`) or cut. A bug in front of users: stop, reproduce, write the failing test or eval case first, fix, then record the lesson. Example: demo answers prepared by our team were labeled as AI output; the decision is D-065; the fix is in code and passed review in the fifth round (T-177). A second: a disputed summary was one click from the letter; accepting it now needs a ticked "I compared it with the quote" (D-066, T-179). A third: charge lines printed a bill's statement date as the service date. Six rounds of reading dates kept finding new patterns that print a wrong one, so the fallback declared in advance applied (D-073): every charge line prints a fillable "date of service [__________]" followed by "(record dated X)", and no service date is extracted (`memory/SCOPE_CUTS.md` row 28).
125:> 1. What you shipped and what you expected it to do.
=== submission/product-note.md
9:**Cut** (`memory/SCOPE_CUTS.md`). For good: accounts, real patient data, EHR integrations, medical or legal judgment. Cut after trying: the "patient said it" label (D-040), per-provider billing totals (D-052) and the drafted treatment paragraph (built without an eval, then cut, D-067), extracting service dates (D-073). **Stretch:** at most one; I shipped three (source viewer, PDF text layer, calibrated confidence), (D-031, D-042: reinstated cuts needing no integration or login). [CHRIS: your reason, one line.] The cost: billing took four rounds.
11:**Good enough to ship.** Live, 3 runs; generator `claude-sonnet-5-5`, judge `claude-haiku-5-5`. [E] = `evals/reports/20261102T164038Z.md`; [L] = `evals/reports/library-latest.md` (15 packets, a74b727, pre-billing redesign). [E] ran at 312efe6; prompts, grounding, judges unchanged since.
21:**Ship call.** Meets the bar on golden, below it on the library (0.775, 0.681, 0.81). So: stage-0 shadow beside a paralegal's own chronology (Part 2, area 5), not live matters, until library recall meets the bar.
28:- **The M3 gate failed once:** prepared demo answers were labeled as AI output (T-177); one click accepted a disputed summary (T-179 blocks it). The combined M3+M4 gate failed with four blockers; after fixes T-215 and T-216 it passed in round 2 (`reviews/GATE-M3-summary.md`), suite 0 failed. Prompt log: final, e0d721d. M4 closes after the final privacy sweep (pending).
=== submission/SUBMISSION_CHECKLIST.md
14:| 4 | Part 1: prompt and conversation log | **final build** (T-187, commit e0d721d: 767 transcripts); the last step is the final privacy sweep, pending. What may be shown is Chris's call (T-193) | [`submission/prompt-log/`](prompt-log/): start with [`README.md`](prompt-log/README.md) (reading guide) and [`TOOLS.md`](prompt-log/TOOLS.md) (which AI tools). Transcripts: [`transcripts/`](prompt-log/transcripts/). Board log: [`board-activity.jsonl`](prompt-log/board-activity.jsonl). Reviews: [`reviews/`](prompt-log/reviews/). Decisions and lessons: [`decisions-and-lessons/`](prompt-log/decisions-and-lessons/). The brief: [`CONTRACT.md`](prompt-log/CONTRACT.md). What was redacted: [`REDACTIONS.md`](prompt-log/REDACTIONS.md) |
30:| Export: copy-ready treatment text, only what she accepted | final | [`app/backend/export.py`](../app/backend/export.py) | Byte-exact template [`evals/golden/sample.export.expected.txt`](../evals/golden/sample.export.expected.txt) (the spec copy matches it: T-215, done); [`evals/letter_check.py`](../evals/letter_check.py) |
31:| Stretch (at most one): side-by-side source viewer | final, but see the note in the product note: three stretch items shipped, not one | [`app/frontend/sidebyside.js`](../app/frontend/sidebyside.js), [`app/backend/pdf_text.py`](../app/backend/pdf_text.py), [`app/backend/confidence.py`](../app/backend/confidence.py) | Reason is Chris's to write (T-191) |
32:| Guided four-step screen; the second AI check and the human decision shown on each item, and a "How each answer is checked" page | guided screen **final** (T-181); the ladder display is built (T-211, committed; gate fixes T-216 done) | [`app/frontend/guided/`](../app/frontend/guided/) | T-181 reviews: [`submission/prompt-log/reviews/T-181-ux-designer-r3.md`](prompt-log/reviews/T-181-ux-designer-r3.md), [`submission/prompt-log/reviews/T-181-paralegal-r2.md`](prompt-log/reviews/T-181-paralegal-r2.md) |
48:| Keep the prompts | final build (T-187, e0d721d); privacy sweep pending | [`submission/prompt-log/`](prompt-log/) |
75:| 8. Supervising developers | 8 | [`board/`](../board/), [`submission/prompt-log/reviews/`](prompt-log/reviews/), [`memory/LESSONS.md`](../memory/LESSONS.md) |
79:## 7. Pending, in one list
83:| T-187 | qa | Final prompt-log build is done (e0d721d). Pending: the final privacy sweep, which closes M4 |
85:| T-215, T-216, T-217 | backend, frontend, qa | Done. The M3+M4 gate passed in round 2 (`reviews/GATE-M3-summary.md`); the suite is 0 failed (`artifacts/gate-M3M4-suite-final.txt`) |
=== submission/email-draft.md
29:I know the brief asked for one stretch item and I shipped three; the note explains why.
=== README
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:49:54.383Z

**tool call — Bash**
````
{
 "command": "for t in T-187 T-215 T-216 T-217 T-218; do echo $t; python3 tools/board.py show $t | grep -E '^status'; done; python3 tools/board.py status --brief | head -20; git show HEAD:memory/LESSONS.md | grep -c '^- '; bash submission/evidence/count_at.sh HEAD 2>&1 | grep -i lesson; git show HEAD:submission/prompt-log/README.md | grep -nE 'interim|pending|final' | head; git show HEAD:submission/product-note.md | grep -nE 'statement|record dated'; git show HEAD:submission/part2-process.md | grep -nE 'statement|record dated' | head -3; git show HEAD:submission/part2-process.md | grep -n 'cannot drift'; git show HEAD:README.md | grep -ni 'recorded'; git show HEAD:submission/SUBMISSION_CHECKLIST.md | grep -nE 'privacy sweep|T-217|T-193'; python3 tools/board.py show T-217 | head -8; ls submission/*.pdf 2>/dev/null; git show --stat --format=%h b05fa81 | head -12",
 "description": "Verify board status, counts, labels, remaining stale lines"
}
````

### User / tool · 2026-11-03T15:49:55.377Z

**tool result**
````
T-187
status: "in_review"
T-215
status: "done"
T-216
status: "done"
T-217
status: "in_review"
T-218
status: "done"
[board] 96.9% done | M0:done M1:done M2:done M3:active M4:active M5:active
[board] ready=0 in_progress=0 in_review=2 changes=0 blocked=4 needs_chris=8 done=185 | inbox_unread=0 stalled=0
56
lessons    56
5:The transcripts are exported by `tools/export_prompt_log.py` from the Claude Code JSONL files (driven by `evals/finalize_prompt_log.py`), and rendered as markdown with each model's thinking, tool calls and tool results in order. They are not summarized or tidied, but they are not byte-for-byte raw either: seven kinds of edit were made, listed here, and nothing else.
7:<!-- EDITS:START (written by evals/finalize_prompt_log.py from the files as built; do not edit by hand) -->
10:1. **Secret redaction**, marker `<redacted>` (801 occurrences in 130 files). Any string matching a `tools/check_secrets.py` pattern is replaced (for `ANTHROPIC_API_KEY=<redacted> only the value). The exporter masks `sk-ant-` keys and `ANTHROPIC_API_KEY=<redacted> values as it exports and `evals/finalize_prompt_log.py` replaces anything else the scanner matches. No key-shaped value remains in the folder, and values masked at export time were not inspected. `REDACTIONS.md` itemizes the finalize step's replacements by file and class, never by value.
11:2. **Private-network redaction**, marker `<redacted-private>` (1,381 occurrences in 155 files). Tailnet hostnames and labels, any mention of the tailnet suffix, Tailscale 100.64/10 addresses and the `100.x.` prefix, a work email address and its domain (one former-employer name in the bio in the `CONTRACT.md` copy is among them), and regex, backslash-escaped, quote-and-plus-split, one-character-wildcard and punctuation-gapped spellings of all of these (for example a pattern written with a backslash before each dot, a value cut into quoted pieces joined with `+` or into a tuple of quoted pieces, a regex with `*` or `?` between the name and the dot). A bare work-email domain counts as one of these. Names of Chris's computers and phone are replaced by `<device>` (235 occurrences in 37 files); the phone name is also replaced when it appears without its trailing number. The final check removes backslashes, quotes, `+` and whitespace from every file, folds case, allows up to 12 punctuation characters between the characters of each term, and confirms none of these terms remains.
16:7. **Outside project name redacted until Chris decides**, marker `<outside project>` (481 occurrences in 105 files). The name of one other project of Chris's (the one the omitted excerpts in edit 4 came from) is replaced wherever it appears, in any letter case and in these forms: a path segment, a file-name slug, prose, a backslash-escaped spelling, a value cut into quoted pieces joined with `+` or spread over whitespace, a tuple or regex whose pieces are separated by punctuation (up to 12 characters), or one character replaced by a wildcard. A path that runs through the name (a folder named after it, its sub-folders and the file) is replaced whole by the one marker. Unicode (`\u`), percent and HTML-entity escapes are not decoded. This is a default, not a verdict: it stays on until Chris says whether the name may be shown, and `REDACT_OUTSIDE_PROJECT_NAME` in `evals/finalize_prompt_log.py` is the single switch for it (no entry in the local patterns file can mask the name when the switch is off). Where a path or file-name rule from edit 3 already covers the whole path, that rule's marker is used instead.
21:The raw size is about 139 MB, so the full set lives in plain git rather than LFS; re-running `python3 evals/finalize_prompt_log.py` regenerates the whole folder, rewrites the list above from the files as built, and fails if a private pattern survives.
15:| 1 | Grounding: every exported statement and amount has a quote in the input (100%) | 1.000, 242 checked [E] |
27:- **Billing took four adversarial rounds.** An adjuster reviewer outworded every word-list rule: a letter said $16,147, true $8,123.50 (`submission/prompt-log/reviews/T-140-claims-adjuster.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one by one, and the total reads "Billed charges accepted from these records". Date reading failed the same way; after six rounds the pre-declared fallback applies: every charge line prints a fillable "date of service [__________]" followed by "(record dated X)", and no service date is extracted (D-073, `memory/SCOPE_CUTS.md` row 28).
54:| Grounding | 100% of exported statements and amounts have a quote in the input | 1.000 |
57:| No invented facts | 0 unsupported statements over 3 runs; judge catches at least 95% of seeded wrong summaries | 0; 40/40 |
116:**When work is late or a bug reaches users.** Late: I cut scope, not checks. D-063 held every non-P0 card to finish the MVP. After three review rounds I either accept with written debt (65 rows in `memory/SCOPE_CUTS.md`) or cut. A bug in front of users: stop, reproduce, write the failing test or eval case first, fix, then record the lesson. Example: demo answers prepared by our team were labeled as AI output; the decision is D-065; the fix is in code and passed review in the fifth round (T-177). A second: a disputed summary was one click from the letter; accepting it now needs a ticked "I compared it with the quote" (D-066, T-179). A third: charge lines printed a bill's statement date as the service date. Six rounds of reading dates kept finding new patterns that print a wrong one, so the fallback declared in advance applied (D-073): every charge line prints a fillable "date of service [__________]" followed by "(record dated X)", and no service date is extracted (`memory/SCOPE_CUTS.md` row 28).
36:The spec is `spec/REQUIREMENTS.md`: the user and assumptions (each with "if wrong"), 62 numbered requirements each with a pass condition and the checker that proves it (unit test, eval metric, E2E, or a persona review), non-goals, a byte-exact export template, the ship bar, and the LLM/code table (`docs/LLM_VS_CODE.md`). The API contract (`memory/contracts/api.md`) is written before code. Every decision made in review goes into the decision log, so the spec and the build cannot drift quietly. Three acceptance criteria for the AI's behavior:
25:**Docker (optional, not verified by us).** The `./run.sh` path above is the one we tested. The Dockerfile exists, but the team's machine had no running Docker daemon, so `docker build` and `docker run` have never been executed; we emulated the image's file list and environment instead. If you want to try it and it fails, use `./run.sh`. The open item is recorded in [`submission/NEEDS_CHRIS.md`](submission/NEEDS_CHRIS.md) ("Docker verification").
65:**Demo mode and live mode.** Demo mode is the default and needs nothing. In demo mode no model is called and none can be: the backend is `fixture` and replays stored answers from [`tests/fixtures/llm/`](tests/fixtures/llm/). The sample's summaries and flags are **prepared answers** written and hand-checked by the team and labelled "Prepared by our team", never "AI draft" (decision D-065). The second check's verdicts are different: they are real recorded outputs of the judge model, never scripted (D-056), and the code checks run for real on every item. Live mode is opt-in and runs the real generator and judge on any pasted text.
101:- `make evals` scores the golden set on the **fixture backend** and writes `data/evals/<timestamp>.md` (git-ignored; the committed `evals/reports/` are left alone). **It fails on a clean clone, and that is expected, not a defect** (the runner exits 1, so `make` prints `Error 1` and exits 2; the last lines name three `blocker:` items): the ship bar includes metrics that need live model runs (3-run determinism, the judge's seeded-error controls), and a fixture run cannot measure them, so the report says `ship_bar_met=False` and lists those as blockers by design. The Makefile prints a line saying so. Read the report's table for the numbers the fixture run can check (dates, gaps, totals, grounding); the ship-bar result comes from a live run, recorded in `evals/reports/latest.json`.
12:| 2 | Part 1: demo video (3 min or less) or annotated screenshots | **final** (T-184): a 174 s recording on the sample case and 72 annotated screenshots, with captions burned into the video, and the snapshot allow-list keeps the video and the screenshots (T-217). Voice-over is optional for Chris | Video: [`artifacts/demo.webm`](../artifacts/demo.webm). Screenshots: [`artifacts/screenshots/final/`](../artifacts/screenshots/final/). Captions: [`artifacts/CAPTIONS.md`](../artifacts/CAPTIONS.md). Narration script: [`artifacts/NARRATION.md`](../artifacts/NARRATION.md) |
14:| 4 | Part 1: prompt and conversation log | **final build** (T-187, commit e0d721d: 767 transcripts); the last step is the final privacy sweep, pending. What may be shown is Chris's call (T-193) | [`submission/prompt-log/`](prompt-log/): start with [`README.md`](prompt-log/README.md) (reading guide) and [`TOOLS.md`](prompt-log/TOOLS.md) (which AI tools). Transcripts: [`transcripts/`](prompt-log/transcripts/). Board log: [`board-activity.jsonl`](prompt-log/board-activity.jsonl). Reviews: [`reviews/`](prompt-log/reviews/). Decisions and lessons: [`decisions-and-lessons/`](prompt-log/decisions-and-lessons/). The brief: [`CONTRACT.md`](prompt-log/CONTRACT.md). What was redacted: [`REDACTIONS.md`](prompt-log/REDACTIONS.md) |
48:| Keep the prompts | final build (T-187, e0d721d); privacy sweep pending | [`submission/prompt-log/`](prompt-log/) |
83:| T-187 | qa | Final prompt-log build is done (e0d721d). Pending: the final privacy sweep, which closes M4 |
85:| T-215, T-216, T-217 | backend, frontend, qa | Done. The M3+M4 gate passed in round 2 (`reviews/GATE-M3-summary.md`); the suite is 0 failed (`artifacts/gate-M3M4-suite-final.txt`) |
87:| Chris | | `NEEDS_CHRIS.md`: T-189 (the story), T-190 (name, link), T-022 (demo link), T-193, T-191, T-192, T-019, T-023 |
---
id: "T-217"
title: "Snapshot image allow-list includes artifacts/screenshots/final/ and artifacts/demo.webm (the README and CAPTIONS link them; OCR-clean per GATE-M3M4 privacy)"
milestone: "M4"
role: "release"
status: "in_review"
priority: "P0"
depends_on: []
submission/part2-process.pdf
submission/product-note.pdf
b05fa81

 submission/SUBMISSION_CHECKLIST.md |  14 ++++++--------
 submission/part2-process.md        |  10 +++++-----
 submission/part2-process.pdf       | Bin 259963 -> 259338 bytes
 submission/product-note.md         |  28 +++++++++++++++-------------
 submission/product-note.pdf        | Bin 113390 -> 113810 bytes
 5 files changed, 26 insertions(+), 26 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:50:05.076Z

**tool call — Bash**
````
{
 "command": "for p in part2-process product-note; do git show HEAD:submission/$p.pdf > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/$p.pdf; echo == $p; pdftotext -layout /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/$p.pdf - | grep -nE 'in progress|statement date|28 entries|56 entries|passed in round 2|Ship call|e0d721d|privacy sweep'; pdfinfo /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/$p.pdf | grep Pages; done; git show HEAD:submission/NEEDS_CHRIS.md | grep -nE 'T-215|T-216|failed|in progress' | head; git show HEAD:docs/LLM_VS_CODE.md >/dev/null && echo ok; python3 tools/board.py show T-193 | grep -E '^status'",
 "description": "Check PDFs and NEEDS_CHRIS for stale text"
}
````

### User / tool · 2026-11-03T15:50:05.363Z

**tool result**
````
== part2-process
4:dated reports), memory/ORCHESTRATOR_DECISIONS.md (75 decisions). Paths are as committed. Every count is at commit e0d721d,
217:(memory/LESSONS.md, 56 entries).
226:M3+M4 gate (D-075) failed with four blockers, its fixes (T-215, T-216) are done, and it passed in round 2 (reviews/GATE-M3-
227:summary.md), with the suite at 0 failed (artifacts/gate-M3M4-suite-final.txt). The prompt log is the final build (commit e0d721d).
228:M4 closes after the final privacy sweep, which is pending.
234:lines printed a bill’s statement date as the service date. Six rounds of reading dates kept finding new patterns that print a wrong one,
252:Counts at commit e0d721d. Re-run: bash submission/evidence/count_at.sh e0d721d.
Pages:           4
== product-note
33:Ship call. Meets the bar on golden, below it on the library (0.775, 0.681, 0.81). So: stage-0 shadow beside a paralegal’s own chronology (Part 2,
47:   it). The combined M3+M4 gate failed with four blockers; after fixes T-215 and T-216 it passed in round 2 (reviews/GATE-M3-summary.md),
48:   suite 0 failed. Prompt log: final, e0d721d. M4 closes after the final privacy sweep (pending).
Pages:           1
ok
status: "needs_chris"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:50:08.250Z

**tool call — Bash**
````
{
 "command": "bash submission/evidence/count_at.sh e0d721d 2>&1 | head -12; mkdir -p artifacts/review-evidence/GATE-M5-hiring-panel",
 "description": "Re-run count script at stated commit"
}
````

### User / tool · 2026-11-03T15:50:08.463Z

**tool result**
````
reviews         555
reports    27
decisions        75
lessons    56
debt rows  65
personas   13
reqs             62
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:50:38.004Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/GATE-M5-hiring-panel-verify.md",
 "content": "# GATE-M5 hiring panel — verify at HEAD b05fa81\n\n**Verdict: pass.** The one blocker is closed. Part 2, the product note and the checklist now match the committed record: the M3+M4 gate passed in round 2, the suite is 0 failed, and the prompt log is the final build. No blocker and no major remains. Two small status mismatches remain in the checklist. The [CHRIS] items (One story, stretch reason) are Chris's and are not scored.\n\n## Blocker check (commands run, HEAD b05fa81)\n| Claim in the packet | Committed record | Match |\n|---|---|---|\n| `part2-process.md:114`: gate \"failed with four blockers, its fixes (T-215, T-216) are done, and it passed in round 2 ... suite at 0 failed\" | `git show HEAD:reviews/GATE-M3-summary.md` line 3: \"Result: **pass** (round 2, combined M3+M4 panel under D-075)\"; `board.py show T-215` and `T-216`: status \"done\" | yes |\n| 5,945 unit passed / 0 failed; 614 e2e passed / 0 failed | `git show HEAD:artifacts/gate-M3M4-suite-final.txt`: \"unit ... 5945 passed, 0 failed, 12 skipped\"; \"e2e ... 614 passed, 0 failed, 1 skipped\"; letter 0; spec true | yes |\n| \"The prompt log is the final build (commit e0d721d)\"; checklist row 4 \"final build (T-187, commit e0d721d: 767 transcripts)\" | `git show --stat e0d721d`: \"T-187 final prompt-log build ... 767 transcripts\" | yes |\n| `product-note.md:28`: gate passed after T-215/T-216, suite 0 failed | same sources | yes |\n| `grep -nE 'in progress\\|10 unit failures\\|6 e2e failures\\|interim\\|being aligned\\|gate fixes are in'` on the four submission .md files at HEAD | no status hit | yes |\n| PDFs | `pdftotext` of `HEAD:submission/part2-process.pdf` (4 pages) and `product-note.pdf` carry the same \"passed in round 2\", \"final build\", \"56 entries\" wording | yes |\n\n## Earlier minors\n| Minor | State |\n|---|---|\n| Ship call after below-bar library result | Fixed: `product-note.md:21` \"Ship call. ... stage-0 shadow ... not live matters\" |\n| \"record or statement date\" label | Fixed: `product-note.md:25` now \"record dated X\"; the remaining \"statement date\" in Part 2 line 116 describes the old bug, not the label |\n| Lessons count | Fixed: Part 2 says 56; `bash submission/evidence/count_at.sh e0d721d` prints `lessons 56` |\n| Paragraph \"cut and shipped\" | Fixed: \"built without an eval, then cut, D-067\" |\n| [E] citation without commit | Fixed: \"[E] ran at 312efe6; prompts, grounding, judges unchanged since\" |\n| README hides `FIXTURE_SET=recorded` | Not fixed: `git show HEAD:README.md | grep -n FIXTURE_SET` returns nothing |\n| Nit: \"cannot drift quietly\" (`part2-process.md:36`) | Not fixed (optional) |\n\n## Per-row scores\nUnchanged from the first review: R1 4, R2 5, R3 4, R4 5, R5 5, R6 4, R7 4. The fixes remove the misreport that held R6 and R7 down, but R6 and R7 stay at 4 because the stretch reason and the One story are not yet written. Neither is scored here. Note that the writer has not added the time-box line the first review asked for.\n\n**Hire call:** unchanged, lean hire. The packet no longer quotes its own gate as failing. What remains is Chris's to supply.\n\n```json\n{\"card\": \"GATE-M5\", \"persona\": \"hiring-panel-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"HEAD b05fa81 verify of reviews/GATE-M5-hiring-panel.md; submission/{part2-process,product-note,SUBMISSION_CHECKLIST,email-draft}.md and PDFs, README.md, reviews/GATE-M3-summary.md, artifacts/gate-M3M4-suite-final.txt, commit e0d721d\",\n \"exercised\": [\n  \"git rev-parse --short HEAD (b05fa81); git show --stat b05fa81 and e0d721d\",\n  \"git show HEAD:reviews/GATE-M3-summary.md and HEAD:artifacts/gate-M3M4-suite-final.txt\",\n  \"git show HEAD:<path> + grep for stale-status phrases in part2-process.md, product-note.md, SUBMISSION_CHECKLIST.md, email-draft.md, prompt-log/README.md, README.md\",\n  \"pdftotext on HEAD copies of part2-process.pdf and product-note.pdf; pdfinfo page count\",\n  \"board.py show T-187, T-215, T-216, T-217, T-218, T-193; board.py status --brief\",\n  \"bash submission/evidence/count_at.sh e0d721d (lessons 56)\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"R1_builder_mindset\": 4, \"R2_technical_fluency\": 5, \"R3_ai_judgment\": 4, \"R4_workflow_obsession\": 5, \"R5_communication\": 5, \"R6_delivery_leadership\": 4, \"R7_self_direction_clarity\": 4},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"Checklist marks T-217 done, and T-187 built, while the board still has both in_review\",\n   \"evidence\": \"submission/SUBMISSION_CHECKLIST.md:85 'T-215, T-216, T-217 | backend, frontend, qa | Done.'; `python3 tools/board.py show T-217` status \\\"in_review\\\"; `show T-187` status \\\"in_review\\\" (checklist :83 'Final prompt-log build is done (e0d721d)').\",\n   \"why_it_matters\": \"Same class as the first blocker, but small: a status line that the board does not back. T-217 is an allow-list card, not something that misleads on the product.\",\n   \"fix\": \"Say 'T-217 in review' (or wait for the review to close) and 'T-187 built, in review'.\",\n   \"acceptance_test\": \"Every T-### status in SUBMISSION_CHECKLIST.md equals `board.py show` at the commit it is rendered from.\"},\n  {\"severity\": \"minor\", \"title\": \"Stretch line still has no time box or cost of the two extra items (writer part)\",\n   \"evidence\": \"submission/product-note.md:9 'I shipped three ... [CHRIS: your reason, one line.] The cost: billing took four rounds.' Brief: 'pick at most one ... Time-box it.'\",\n   \"why_it_matters\": \"Disclosed, and Chris's reason is excluded from the score. The writer-side line (time spent against the box) is still missing. This was a major in the first review; it is minor now because the remaining gap is Chris's input.\",\n   \"fix\": \"Add one sentence with the hours spent on the three items from SCOPE_CUTS or the board; Chris adds the reason (T-191).\",\n   \"acceptance_test\": \"The stretch line states time spent and has no placeholder once T-191 is answered.\"},\n  {\"severity\": \"minor\", \"title\": \"README still hides the offline way to see the model's own recorded answers\",\n   \"evidence\": \"`git show HEAD:README.md | grep -n FIXTURE_SET` returns nothing (carried from the first review).\",\n   \"why_it_matters\": \"Zlayt opens the demo and sees only prepared answers; the real recorded output needs no key and they would not find it.\",\n   \"fix\": \"Add one README line: 'See the model's own recorded answers on the sample: FIXTURE_SET=recorded ./run.sh'.\",\n   \"acceptance_test\": \"README names FIXTURE_SET=recorded.\"}\n ],\n \"whats_right\": [\n  \"Gate state, suite counts, prompt-log commit and lessons count now re-run to the same numbers as the committed files, in Markdown and in both PDFs.\",\n  \"The product note now states a ship call (stage-0 shadow, not live matters) beside the below-bar library numbers.\",\n  \"The first-review traps, export test and scores were not touched by this fix round.\"\n ],\n \"questions_for_chris\": [\n  \"Why three stretch items (T-191), and how many hours did they take?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-03T15:50:38.155Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/GATE-M5-hiring-panel-verify.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:50:44.254Z

Verdict is pass at b05fa81. The blocker is closed: Part 2, the product note and both PDFs now match `reviews/GATE-M3-summary.md` (round 2 pass), `artifacts/gate-M3M4-suite-final.txt` (0 failed) and the final prompt-log build in e0d721d. Four of the six earlier minors are fixed (ship call, "record dated" label, lessons count of 56, cut/shipped paragraph). Open: the README never mentions `FIXTURE_SET=recorded`, the stretch line still has no time box, and the checklist marks T-217 done while the board has it in_review.
The file is `/Users/arsis/zlayt-pm-project/reviews/GATE-M5-hiring-panel-verify.md`. I kept the per-row scores unchanged, and it has no blockers or majors, only three minors.
