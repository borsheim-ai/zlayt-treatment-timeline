# Subagent: PM review: product note + Part 2 (PM review: product note + Part 2)

Source: `agent-af190ce83607cdd17.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T21:10:58.367Z

Review board cards T-185 and T-186 in /Users/arsis/zlayt-pm-project: submission/product-note.md (one page), submission/part2-process.md (four pages or fewer) and submission/validation-ladder.svg. These go to Zlayt's hiring panel. Read docs/CONTRACT.md: the M5 section, Appendix A ("What we evaluate") and Appendix B (Chris's voice).

Check:
- **Accuracy:** every claim and number traces to the cited file. Spot-check at least 10.
- **No invented facts about Chris.** Placeholders must be marked [CHRIS: ...].
- **Required contents:** the product note covers all of its required elements; Part 2 answers all eight areas with this build's specifics, including three AI acceptance criteria with one "must never".
- **Honesty:** the misses (library recall, the billing rounds, the UI redesign after Chris's feedback) are told plainly.
- **Voice:** it sounds like Chris.
- **Length:** within limits.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-185-product-manager.md and reviews/T-186-product-manager.md. Each needs a ```json block of real values: card, persona product-manager-reviewer, model claude-opus-5-5, verdict, findings, exercised. Reply in 2 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:00.687Z

**tool call — Bash**
````
{
 "command": "cat personas/product-manager.md | head -c 200 && echo && ls .claude/agent-memory/product-manager-reviewer/ && wc -w submission/product-note.md submission/part2-process.md && ls -la submission/ && python3 tools/board.py show T-185 && python3 tools/board.py show T-186",
 "description": "Read dossier head, memory listing, word counts, cards"
}
````

### User / tool · 2026-11-02T21:11:00.929Z

**tool result**
````
# Persona dossier — product-manager-reviewer

## 1. Identity
**Dana Okafor (fictional), Senior Product Manager, AI legal-tech startup — 10 years in B2B SaaS, last 3 shipping LLM features to law fi
MEMORY.md
feedback_calibration_vs_redflags.md
feedback_gate_review_patterns.md
feedback_needs_chris_drift.md
feedback_plan_review_patterns.md
feedback_spec_review_patterns.md
project_t013_review_history.md
project_t017_t018_review_history.md
reference_reviewer_sandbox.md
reference_source_fetching.md
     996 submission/product-note.md
    2759 submission/part2-process.md
    3755 total
total 96
drwxr-xr-x@  8 arsis  staff    256 Nov  2 15:08 .
drwxr-xr-x  34 arsis  staff   1088 Nov  2 15:04 ..
-rw-r--r--@  1 arsis  staff   5436 Nov  2 15:09 NEEDS_CHRIS.md
-rw-r--r--@  1 arsis  staff  16111 Nov  2 15:09 part2-process.md
-rw-r--r--@  1 arsis  staff    433 Nov  2 15:06 print.css
-rw-r--r--@  1 arsis  staff   6162 Nov  2 15:06 product-note.md
drwxr-xr-x@ 10 arsis  staff    320 Nov  2 15:05 prompt-log
-rw-r--r--@  1 arsis  staff   8259 Nov  2 15:07 validation-ladder.svg
---
id: "T-185"
title: "M5 product note: submission/product-note.md, one page, in Chris's voice (Appendix B): problem and user, what was built, cuts and why, ship bar (3-5 testable criteria from the eval), testing and findings, how AI can mislead and the validation ladder, LLM/code split, three post-launch metrics"
milestone: "M5"
role: "writer"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T21:00:13Z"
updated_at: "2026-11-02T21:10:53Z"
claimed_by: "writer"
claimed_at: "2026-11-02T21:00:45Z"
rounds: 0
commits: ["59e33cacd152f21c18727aab4738c5dc096ac486"]
reviews: []
ac:
  - {"n": 1, "text": "one page; every number traces to evals/reports or reviews; no invented facts about Chris", "done": true, "evidence": "submission/product-note.md renders to 1 page (pandoc+Chrome, print.css); numbers traced to evals/reports/20261102T164038Z.md, m3-sensors.md, GATE-M3-product-manager.md, SCOPE_CUTS 13/23; Chris-past facts: none, placeholders only"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T21:00:16Z orchestrator: assigned: writer
- 2026-11-02T21:00:45Z writer: claimed
- 2026-11-02T21:10:23Z writer: Drafted one-page note (fits Letter at 8.7pt via submission/print.css; pandoc + headless Chrome page count = 1). All numbers cite evals/reports/20261102T164038Z.md, evals/reports/m3-sensors.md, reviews/GATE-M3-*.md, SCOPE_CUTS 13/23. Assumptions: guided UI (T-181) lands as described; fixes T-177/T-179 worded as in progress - update at final. Placeholders: full name, public link.
- 2026-11-02T21:10:23Z writer: AC 1 checked: submission/product-note.md renders to 1 page (pandoc+Chrome, print.css); numbers traced to evals/reports/20261102T164038Z.md, m3-sensors.md, GATE-M3-product-manager.md, SCOPE_CUTS 13/23; Chris-past facts: none, placeholders only
- 2026-11-02T21:10:38Z writer: moved in_progress -> in_review
- 2026-11-02T21:10:53Z orchestrator: review dispatched: product-manager-reviewer
- 2026-11-02T21:10:53Z orchestrator: Refresh at final (after T-181 ships): guided UI shipped wording, re-run verify_quickly on the guided UI, regenerate library-latest.md (qa) for the recall number.

## Handoff
What changed: submission/product-note.md, one page (pandoc + headless Chrome with submission/print.css, Letter 8.7pt, 1 page). Problem/user, built (guided 4 steps, ladder), cuts, ship bar table with live numbers, testing (library flag recall 0.81, billing rounds D-059..D-064, M3 gate fail), AI-misleads table, LLM/code, 3 metrics.
How verified: every number traced to evals/reports/20261102T164038Z.md, evals/reports/m3-sensors.md, reviews/GATE-M3-product-manager.md, reviews/GATE-M3-paralegal.md, reviews/T-140-claims-adjuster*.md, SCOPE_CUTS rows 13/23. No Chris-past facts; placeholders only.
Left: [CHRIS: full name, public link] (NEEDS_CHRIS #5). Update at final: T-177/T-179 are worded 'in progress'; guided UI (T-181) is described as built, and verify_quickly 4 is the old screen (stated in note); library 0.81 is from the d0b04bc PM review, library-latest.md in repo is stale (QA to regenerate).
Surprised me: one page needs ~1000 words at 8.7pt; trim before adding.

---
id: "T-186"
title: "M5 Part 2 process doc: submission/part2-process.md (<=4 pages) answering the eight Part 2 areas with this build's specifics; validation-ladder diagram + spec/eval-rubric excerpt as visuals; Chris's miss story as a marked [CHRIS: ...] block listed in NEEDS_CHRIS"
milestone: "M5"
role: "writer"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T21:00:13Z"
updated_at: "2026-11-02T21:10:53Z"
claimed_by: "writer"
claimed_at: "2026-11-02T21:00:45Z"
rounds: 0
commits: ["59e33cacd152f21c18727aab4738c5dc096ac486"]
reviews: []
ac:
  - {"n": 1, "text": "<=4 pages; 8 areas covered; at least one rendered visual; [CHRIS:] placeholders for anything about Chris's past", "done": true, "evidence": "submission/part2-process.md renders to 4 pages; 8 areas; validation-ladder.svg + 2 rubric tables; [CHRIS:] story + 4 optional markers; NEEDS_CHRIS rows 4-7 (T-189, T-190)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T21:00:16Z orchestrator: assigned: writer
- 2026-11-02T21:00:45Z writer: claimed
- 2026-11-02T21:10:23Z writer: Drafted Part 2 (4 pages at 9.4pt Letter, same pipeline). Visual: submission/validation-ladder.svg (mmdc not installed; hand-written SVG, rendered and checked in headless Chrome) + AI acceptance-criteria and ship-bar rubric tables. [CHRIS:] story block + 4 optional markers; NEEDS_CHRIS rows 4-7, cards T-189 (P0 story), T-190.
- 2026-11-02T21:10:23Z writer: AC 1 checked: submission/part2-process.md renders to 4 pages; 8 areas; validation-ladder.svg + 2 rubric tables; [CHRIS:] story + 4 optional markers; NEEDS_CHRIS rows 4-7 (T-189, T-190)
- 2026-11-02T21:10:38Z writer: moved in_progress -> in_review
- 2026-11-02T21:10:53Z orchestrator: review dispatched: product-manager-reviewer

## Handoff
What changed: submission/part2-process.md (4 pages, Letter 9.4pt via print.css), submission/validation-ladder.svg (hand-written; mmdc not installed), two rubric tables (3 AI acceptance criteria incl. must-never AI-3; ship bar), sample message + 30-min agenda, decision-rights table, rollout/metric thresholds (marked as my starting numbers).
How verified: pandoc + headless Chrome page count = 4; SVG rendered and inspected; numbers cite evals/reports/20261102T164038Z.md, m3-sensors.md, LESSONS (44), SCOPE_CUTS (61 debt rows), reviews/ (460 files), 68 decisions.
Left: Chris's miss story (marked block, NEEDS_CHRIS #4 / T-189), byline (#5), 4 optional [CHRIS: optional] one-liners (#6, T-190).
Surprised me: thresholds (30% time, 60% adoption) are my proposals, not facts; flagged as such in the doc. Counts (460 reviews, 74 reports) move; refresh at final.
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:01.865Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/product-manager.md"
}
````

### User / tool · 2026-11-02T21:11:01.876Z

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

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:02.315Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/submission/product-note.md"
}
````

### User / tool · 2026-11-02T21:11:02.321Z

**tool result**
````
1	# Treatment Timeline: product note
2	
3	Chris [CHRIS: full name] · Zlayt AI PM project, Part 1 · prototype: [CHRIS: public link, see `submission/NEEDS_CHRIS.md`] · synthetic data only · built with Claude Code agents I directed (`submission/prompt-log/TOOLS.md`); run steps in `README.md`
4	
5	**Problem and user.** A Zinda Law Group litigation lead says paralegals spend hours turning scattered records into a treatment chronology before each demand letter, and mistakes cost credibility. The user is the paralegal. She reviews, she does not trust, so every line must be checkable against its source. The attorney signs (assumption A-101).
6	
7	**What I built.** Paste or upload records (text or a PDF text layer). A guided four-step screen: **1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter** (D-068). Review is one item at a time: the record quote beside the AI's summary, two big answers. The export is two blocks that never mix (D-001): a **letter section** (accepted entries and charges only, each with its verbatim quote, provider, date and an `[Ex. __ / Bates __]` placeholder) and **internal notes, do not send** (30-day gaps, conflicts, prior conditions, causation language, amounts not totaled). Every AI step sits behind the validation ladder: the model drafts, code checks, a second model checks, she decides. Nothing reaches the letter without all three.
8	
9	**Cut** (`memory/SCOPE_CUTS.md`). For good: accounts and roles, real patient data, EHR integrations, any medical or legal judgment. After trying: the "patient said it" label (four adversarial rounds each found a mislabeled quote; D-040), per-provider billing totals (five rounds, each found a way to drop a figure, so billing is a cited line listing; D-052), the drafted treatment paragraph (no eval; D-067). Not cut: I reinstated cuts twice (D-031, D-042). The brief allows one stretch; I picked the source viewer and also shipped PDF text-layer upload.
10	
11	**Good enough to ship.** Live run, 3 runs, `claude-sonnet-5-5` generator, `claude-haiku-5-5` judge [E = `evals/reports/20261102T164038Z.md`].
12	
13	| # | Criterion (bar) | Result |
14	|-|------------|--------------|
15	| 1 | Grounding: every exported statement and amount has a quote found in the input (100%) | 1.000, 242 checked [E] |
16	| 2 | Recall of golden entries and amounts (95%) | entries 0.982, amounts 1.000 [E] |
17	| 3 | Flags: precision and recall 0.9 per type; 28-day interval not flagged, 73-day flagged | 1.000/1.000, all four types, 10 golden cases; 28 no, 73 yes [E]. **15 library packets: 34 of 42 must-flags, 0.81** |
18	| 4 | No invented facts: 0 unsupported over 3 runs; judge catches 95% of seeded wrong summaries | 0; 40/40; 0 of 10 correct summaries rejected; conflict and flag judges 20/20 and 12/12, 0 false agrees [E] |
19	| 5 | Reviewable: paralegal persona rates "I could verify every claim quickly" 4/5 or more; E2E green | 4/5 (`reviews/GATE-M3-paralegal.md`); 412 E2E, 5,698 unit tests pass (`evals/reports/m3-sensors.md`) |
20	
21	**What testing found.**
22	
23	- **The 1.000 flag numbers do not generalize.** The golden cases were written next to the rules. On 15 separate library packets, must-flag recall is 0.81 (`reviews/GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23). The misses are conflicts code never proposes, like "Left shoulder pain" against "Right shoulder pain". One entry was missed (`case_06`, a subtle prior condition). Only 5 of 17 "held-out" conflict controls are still clean, so judge numbers are partly in-sample. Score 5 is a persona reviewer on the previous screen, not a real paralegal; not re-scored on the guided screen.
24	- **Billing took four adversarial rounds.** A claims-adjuster reviewer outworded every word-list rule: one library letter said $10,906 against a true $6,000, another $16,147 against $8,123.50 (`reviews/T-140-claims-adjuster*.md`). The fix was a design change (D-059 to D-064): an amount counts only on a dated service line, she accepts charges one at a time, and the total says what it is: "Billed charges accepted from these records."
25	- **The M3 gate failed once.** Demo answers written by our team were labeled as AI output (D-065), and one click accepted a summary the second check had disputed, 5 of 5 times across 16 cases (D-066). Fixes are in progress (T-177, T-179): a disputed summary will need a named "I compared it with the quote."
26	
27	**How the AI can mislead her, and what the design does.**
28	
29	| Failure | Design |
30	|--------|-------------|
31	| Changes a number, side or negation; drops a hedge ("may represent") | Code needs each in the quote: hard refusal on her edits (D-034, D-047), needs-review on AI text (D-022) |
32	| Says more than the quote | Code removes unsupported clauses (D-054); judge 1 checks the rest; a disputed one needs a named confirm (D-066) |
33	| Invents an amount, or obeys an order hidden in a record | Only code finds money, default-deny, she accepts each charge; models have no tools and return a checked form |
34	| Rules on cause or diagnosis | Flag wording is a code template; the model returns a category and a quote only (D-007) |
35	| Silently drops what it could not verify | Nothing is dropped (D-053): a visible "could not verify" list |
36	| The judge is a model too | Judges are scored on seeded wrong items; "verified" never means accepted |
37	
38	**LLM and code.** Code does anything with one right answer: record splitting, dates (ambiguous ones wait for her), gap arithmetic, amounts and their class, totals, quote and number checks, flag wording, export. The model reads: the summary and quote, the flag category, one yes/no per code-proposed conflict pair, the second check. Table: `docs/LLM_VS_CODE.md`.
39	
40	**Three metrics after launch.**
41	
42	1. **Minutes from first paste to copied letter section, against her own last three by hand.** Is it faster? Read beside #2: speed from skipping review is no win.
43	2. **Escaped errors: letter lines an attorney corrects or an adjuster challenges, per 100.** Target 0. Does the ladder hold on real records? Each is a new eval case.
44	3. **Needs-review items accepted unchanged, and median seconds per item.** Verifying or clicking through? (D-066: 5 of 5 disputed items took one click.)
45	
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:02.812Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/submission/part2-process.md"
}
````

### User / tool · 2026-11-02T21:11:02.819Z

**tool result**
````
1	# Part 2: from Zinda's request to a shipped, measured feature
2	
3	Chris [CHRIS: full name] · Zlayt AI PM project. Part 1 was built by a team of AI agents on a board that I directed, so where I can, I answer with that process and point at its artifacts: `board/`, `reviews/` (460 review files), `evals/reports/` (74 dated reports), `memory/ORCHESTRATOR_DECISIONS.md` (68 decisions). Assumptions about how Zinda works are marked as assumptions.
4	
5	![Validation ladder: what stands between an AI draft and the letter](validation-ladder.svg){width=88%}
6	
7	## 1. Discovery
8	
9	**Who first.** The litigation lead who asked, then two or three paralegals who build chronologies, then the attorney who signs the demand. In that order, because the lead tells me what a mistake costs and the paralegals tell me where the time goes.
10	
11	**Request versus need.** The request is "faster." The need is "faster without a new way to be wrong." I ask for artifacts, not opinions: the last finished chronology, the letter it went into, and the adjuster's reply. Then I compare what they say with what they did, and note every point where she opens the source to check a line, because that is the step the tool must make cheap, not remove.
12	
13	**Watching real work without client data.** She works on her own machine on a closed matter; I watch, I copy nothing, I record nothing, and I write down steps, never content. If the firm prefers, she redoes a closed matter from a redacted copy, or we use synthetic records as in Part 1. In this build I had no access to Zinda's people, so my first interviews are the assumptions I wrote down (`memory/ASSUMPTIONS.md`, A-101 to A-108, each with "what changes if wrong" and "how to check") plus 13 researched persona dossiers (`personas/`). [CHRIS: optional, one real example of watching work without exposing client data.]
14	
15	| First three questions to the litigation lead | First three to a paralegal |
16	|--------------|--------------|
17	| 1. Take the last demand letter that went out. Where did the chronology wait on the way from records arriving to letter sent? | 1. Walk me through the last chronology you built, starting from the first record you opened. |
18	| 2. Tell me about the last time an adjuster pushed back on a date or a fact. What did it cost: days, or dollars off the offer? | 2. Which entries do you always re-check against the source, and how? Which one burned you once? |
19	| 3. What will you never let software write in a letter, and what would you check before you signed one it helped with? | 3. When two records disagree, or there is a long gap, where do you write that down, and who sees it? |
20	
21	## 2. Prioritization
22	
23	Chronology comes before demand drafting, deposition summaries and discovery responses for four reasons. **It sits upstream:** a letter drafted on an unchecked chronology repeats its errors. **It is checkable:** every output line traces to a source line, so I can measure quality before anyone uses it (this build has 40 seeded wrong summaries, a 73-day gap that must flag and a 28-day one that must not). Drafting prose from facts is harder to ground; depositions and discovery come later in a matter (assumption, to confirm). **The cost of error is concentrated here:** the lead said mistakes cost credibility with adjusters. **Every matter needs one,** so volume is high.
24	
25	What would change my mind:
26	
27	- A timed baseline shows the median hand chronology takes under an hour. Then "hours" is wrong and I look elsewhere.
28	- The lead says adjuster pushback comes from the bills, not the chronology. Billing goes first. (In Part 1 billing alone took four adversarial rounds.)
29	- Most records arrive as scans. Then the bottleneck is intake, and OCR comes first.
30	- In a pilot, checking the tool's chronology takes as long as writing one. Then I stop and tell the founders.
31	
32	## 3. Spec
33	
34	The spec is `spec/REQUIREMENTS.md`: the user and assumptions (each with "if wrong"), 62 numbered requirements each with a pass condition and the checker that proves it (unit test, eval metric, E2E, or a persona review), non-goals, a byte-exact export template, the ship bar, and the LLM/code table (`docs/LLM_VS_CODE.md`). The API contract (`memory/contracts/api.md`) is written before code. Every decision made in review goes into the decision log, so the spec and the build cannot drift quietly. Three acceptance criteria for the AI's behavior:
35	
36	| # | Acceptance criterion | Checked by |
37	|--|-------------------|-------------|
38	| AI-1 | Every timeline entry and every amount in the export carries a quote that appears word for word in the input. Anything that fails is rejected, shown in a "could not verify" list, and never exported. (R-TL-2) | `grounding_rate` = 1.000, 242 checked (`evals/reports/20261102T164038Z.md`) |
39	| AI-2 | A number, side, negation or hedge in a summary must be in its quote, or the item is marked needs review with the reason. For her own edits it is a hard refusal. (R-TL-10, D-034) | unit tests; 40 seeded wrong summaries, 40 caught |
40	| AI-3 **(must never)** | The tool must never state a diagnosis, severity or cause that the record's own words do not state. It never turns "may represent degenerative change" into "degenerative" or "traumatic," never merges two accident dates, and never totals PT from a "$185 per visit" rate. (R-CO-3) | golden `must_not` rules (regex with good and bad examples, `evals/golden/sample.expected.json`): 0 hits. Any hit is a blocker. |
41	
42	## 4. Quality bar
43	
44	**Building the test set from real work product.** Zinda picks about 20 closed matters (clean, messy, scanned, billing-heavy, two crashes), the attorney approves them, and they never leave Zinda's environment; access is logged (D-016). The senior paralegal's finished chronology is the answer key. A second paralegal marks entries, amounts, must-flags and must-nots independently; I list the disagreements and the attorney settles them. Answers are written before any run: in `evals/golden/` no expected output was ever produced by running the tool. I split the set, tune on one half, and look at the other half once per release. Part 1 shows why: the golden cases written beside the rules score 1.000 on flags, and 15 separate library packets score 0.81 (`reviews/GATE-M3-product-manager.md`).
45	
46	**Who grades.** The paralegal marks every output item right, wrong or missing; the attorney grades a sample on "would I sign this." The AI judges are graded too, on seeded wrong items (judge 1: 40/40; conflict judge 20/20; flag judge 12/12; 0 false agrees).
47	
48	**What score means ship** (`spec/REQUIREMENTS.md` section 7, rubric; live run `evals/reports/20261102T164038Z.md`). Shipping means a supervised pilot, not unsupervised use.
49	
50	| Ship-bar criterion | Bar | Part 1 result |
51	|-----|------------------|------------|
52	| Grounding | 100% of exported statements and amounts have a quote in the input | 1.000 |
53	| Recall | at least 95% of golden entries and amounts | 0.982 and 1.000 |
54	| Flags | precision and recall at least 0.9 per type; 28-day interval no flag, 73-day gap flag | 1.000 each on golden; 0.81 recall on library packets |
55	| No invented facts | 0 unsupported statements over 3 runs; judge catches at least 95% of seeded wrong summaries | 0; 40/40 |
56	| Reviewable | paralegal rates "I could verify every claim quickly" at least 4/5 | 4/5 (persona reviewer) |
57	
58	**Catching regressions.** Any change to a prompt, model, phrase list or schema reruns the eval before review. Prompts are versioned files; each report records the source commit and prompt hashes; `python -m evals.run --check-fresh` fails if the recorded report no longer matches the files. Every bug that escapes becomes a case. A fixture replay is quick; a live run takes about 40 minutes and model spend, so live runs happen before gates.
59	
60	## 5. Ship and learn
61	
62	**Rollout.** Stage 0, shadow: she builds her chronology as usual on 5 closed matters while the tool builds its own, and we compare. Stage 1: two paralegals use it on live matters; the attorney sees the internal notes. Stage 2: the whole team. Each stage opens only when the one before meets its numbers.
63	
64	**Feedback.** A 20-minute weekly check-in per paralegal (agenda in area 7), plus the audit log: every accept, edit and dismiss is stored with before and after, so I see where it was wrong without asking. [CHRIS: optional, one line on how you measured adoption on the OutSystems AI Agent Builder.]
65	
66	| Measure | Definition | Expand if | Kill if |
67	|----|----------|-------|-------|
68	| Adoption | Share of demand letters whose chronology started in the tool | at least 60% after 20 matters | under 25% after 6 weeks of fixes |
69	| Time saved | Median minutes, first paste to copied letter section, against her last three by hand | down at least 30% | down under 10% after 6 weeks |
70	| Output quality | Escaped errors per 100 letter lines (found by the attorney or an adjuster); share of needs-review items accepted unchanged | 0 escaped errors; accept-unchanged rate stable | two unsupported facts reach a carrier |
71	| Retention | Paralegals using it on two or more matters in week 8, among those active in week 4 | at least 80% | under 50% |
72	
73	These are my starting numbers; the lead and I agree them in week 1. In between, I iterate: the cheapest fix that moves the weakest number.
74	
75	## 6. Operating rhythm and fast decisions
76	
77	| I decide alone, same day | I decide with the litigation lead | A founder decides |
78	|-------|---------|---------|
79	| copy and wording, queue order, which eval cases to add, bug triage, a scope cut inside a feature | anything that changes what leaves the firm in a letter (flags stay out of the letter, D-001; the total line wording, D-062), what counts as an error | spend and vendors (model provider, data retention), any real client data in any environment, public exposure, expand or kill |
80	
81	**Speed.** Each question to a founder is one line with my default and what it unblocks. I ask for an answer within one business day (three for a vendor or spend call). No answer, and the default goes ahead and is logged, if it is reversible. This is how the build ran: `submission/NEEDS_CHRIS.md` holds only what needs a human, each row with its assumption, and nothing waits.
82	
83	**First 30 days.** Week 1: shadow three paralegals and the attorney; start the assumptions list, the decision log and the board. Week 2: timed baselines; pick and annotate the 20 matters. Week 3: spec and API contract signed off; first slice running on the test set. Week 4: ship-bar run, stage 0 shadow, go or no-go for stage 1.
84	
85	## 7. Communicating with the team
86	
87	**Honest feedback from busy people.** I do not ask whether they like it. I put output in front of them and ask them to find the error. In a "find the error" session I hand a paralegal a chronology with planted mistakes mixed in with the tool's own, and see what she catches. It is the same idea as the seeded wrong items that grade our judges. I sit with the paralegals without the lead present, since people say less in front of the person who assigns the work. I watch what they do, and trust it over what they say.
88	
89	**A message I would send a paralegal**
90	
91	> Subject: 20 minutes on one chronology?
92	>
93	> Hi [name], I'm building the tool that drafts the treatment chronology, and I need to hear where it's wrong, not whether it's nice. Could I have 20 minutes at your desk this week? Pick a matter that's already closed. You'll build the chronology the way you normally do while I watch; I won't copy or record anything. Then I'll hand you one the tool made for a different closed matter, with a few mistakes I planted, and you mark what you'd catch. Most useful to me: the entry you always re-check, and the one that burned you. If this week is bad, say "not this week." That helps too. Chris
94	
95	**Meeting agenda, 30 minutes, one paralegal:** 0-3 why I'm here and what I will not do (no client data leaves your machine). 3-13 you walk me through a closed matter. 13-23 you mark the tool's chronology: lines you'd trust, lines you wouldn't, why. 23-28 what would make you stop using it. 28-30 what I'll change and when you'll hear back.
96	
97	**Unhappy, silent, or conflicting users.** Unhappy: reproduce the problem on her own example in the room, tell her what changes and by when, then close the loop in writing within the week. Silent: I read the audit log first (items dismissed, time per item), then ask about one specific item, never "any feedback?" Conflicting: the person who signs the letter decides what goes in it; the person doing the work decides how the work flows. I tell both what I decided and why. The same call came up in the build: a paralegal reviewer blocked the first spec because accepted flags would have gone to the carrier. Accepting a flag now means "I've seen it," and flags live in internal notes (D-001).
98	
99	**Founders, without more meetings.** One page every Friday: shipped, the four numbers above, decisions I need with my default, risks. A decision log they can read at any time. No standing meeting. This build ran the same way: `memory/STATE.md` and `submission/NEEDS_CHRIS.md`.
100	[CHRIS: optional, one line on a time you got honest feedback from users who said little.]
101	
102	## 8. Supervising developers
103	
104	**Before they start:** the spec with R-IDs, the API contract, the golden set, the LLM/code table, non-goals, and a card per task whose acceptance criteria name the exact check. A developer who cannot say how a card will be tested does not start it.
105	
106	**Each week:** the board (cards by state, review rounds per card), the eval report against the last one (did a metric drop, did a prompt hash change), bugs that escaped, review findings by severity, decisions waiting on me. I check evidence, not claims. Two examples from this build: a worker's "12/12 pass" came from an uncommitted working tree and the committed code rendered no charges panel; two partial commits broke HEAD. The rule now is to verify from `git archive HEAD`, and pre-commit compiles every staged file (`memory/LESSONS.md`, 44 entries).
107	
108	**Before release.** Unit tests (5,698 passed), E2E (412 passed, `evals/reports/m3-sensors.md`), the live eval against the ship bar, a clean-clone install timed against the 5-minute bar, and adversarial reviewers: a claims adjuster who outworded my billing rules for four rounds, a chaos tester who found a run that stayed "running" forever after a restart. **Who signs off:** a reviewer in a fresh context who did not write the work, and me. Workers never close their own cards. Milestone gates: M0, M1, M2 passed; M3 failed its first round with two blockers (`reviews/GATE-M3-round1-triage.md`).
109	
110	**When work is late or a bug reaches users.** Late: I cut scope, not checks. D-063 held every non-P0 card to finish the MVP. After three review rounds I either accept with written debt (61 rows in `memory/SCOPE_CUTS.md`) or cut. A bug in front of users: stop, reproduce, write the failing test or eval case first, fix, then record the lesson. Example: demo answers prepared by our team were labeled as AI output; the decision is D-065.
111	
112	**AI used:** to build (orchestrator on Opus, workers on Sonnet, reviewers as adversarial personas), to draft documents, to red-team. **AI not used:** to approve its own work, to set the ship-bar numbers, to draw the LLM/code line, to talk to users, to send anything. [CHRIS: optional, one real example of supervising developers on a late feature.]
113	
114	## The one story: a miss
115	
116	> **[CHRIS: write this yourself. It has to be a feature or launch you owned that missed the mark, and the team will not write it for you.**
117	> Suggested shape, about 200 words:
118	>
119	> 1. What you shipped and what you expected it to do.
120	> 2. What you missed, and the number or signal that showed it.
121	> 3. One concrete thing you changed in your process afterward: an artifact or a rule, not "communicate more."
122	> 4. How that change shows up in this project.
123	>
124	> Hooks from this build you can tie it to: a "must never" acceptance criterion written before building; a held-out test set looked at once (golden 1.000 against library 0.81); checking evidence instead of a worker's claim; the demo that labeled prepared answers as AI output.**]**
125	
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:03.852Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer && cat feedback_gate_review_patterns.md feedback_calibration_vs_redflags.md reference_reviewer_sandbox.md feedback_needs_chris_drift.md",
 "description": "Read relevant memory files"
}
````

### User / tool · 2026-11-02T21:11:03.942Z

**tool result**
````
---
name: gate-review-patterns
description: Milestone-gate PM review checks that found real issues at GATE-M3 (2026-11-02) — demo provenance labels, one-click accept of judge-disputed items, stale cut lists, ungated stretch features, golden-vs-library gap
metadata:
  type: feedback
---

Run these checks first on any MVP or gate review. Each one found a real issue at GATE-M3 (d0b04bc).

1. **Demo provenance.** Read `tests/fixtures/llm/curated/*.json`, where the `CURATED` field says "Not a model output". Then check that the UI badge, the "AI draft" tags, the `/items/<id>/trace` generator step and `/audit` do not present those answers as AI output. D-029 requires an honest label. "Plain wording" cards (T-166 F7) removed that label as jargon, so check it again after any wording round.
2. **The human rung is the only gate.** Accept every JUDGE_PARTIAL or JUDGE_UNSUPPORTED entry and check the result. Script: artifacts/review-evidence/GATE-M3-pm/lib_sweep.py. Compare each letter summary with its own Source quote. Ship bar 4 measures the model before the human, so nothing measures what reaches the letter.
3. **Cut-list truth.** Compare SCOPE_CUTS rows and REQUIREMENTS §4/§5 with the running UI testids. Chris reinstated cuts twice (D-031, D-042), and both docs lagged.
4. **Held cards whose feature still ships.** Under D-063, a blocked card such as T-059 (the narrative) can still be live in the UI with its eval AC unmet. Grep `evals/run.py` for the feature name.
5. **Golden vs library.** Regenerate `python -m evals.library_report --out <evidence>` from the archive copy. At d0b04bc, must-flags were 34/42 on the library against 1.000 on golden. The committed library-latest.md and latest.json were stale.

**Why:** the panel grades over-claiming and "cut scope on purpose". These problems were invisible on the sample alone.

**How to apply:** reuse `journey.py`, `lib_sweep.py`, `ui_walk.py` and `lib_missed.py` in that folder. Run each with `python3 -I` against an archive-copy server. Related: [[plan-review-patterns]], [[calibration-vs-redflags]].
---
name: calibration-vs-redflags
description: Recurring dossier/review pattern — calibration examples graded softer than the persona's own dealbreakers or the spec's blocker definition; always cross-check
metadata:
  type: feedback
---

When reviewing persona dossiers (or any rubric that gets compiled into a reviewer prompt), cross-check every §8 calibration severity against the dossier's §5 red flags, Appendix A constraints, and CONTRACT.md:676 ("blocker = violates a spec constraint, invents or loses facts"). In the T-010/T-011 review (2026-11-02), 9 of 13 dossiers had dealbreakers anchored at major or minor. Examples: installer >5-min install rated major, a dropped LOC qualifier rated major, an invented "MRI performed" rated minor.

**Why:** calibration examples are the reviewer's severity anchors. Soft anchors build in the "identifies issue, then decides it's not a big deal" leniency failure.

**How to apply:** script a red-flag vs calibration grep (see artifacts/review-evidence/T-010-011-sections.txt) and treat each contradiction as a major against the dossier. Also check that PM/hiring-panel checklists cover every Part 2 sub-question by name (retention, first 30 days, the 3 AI ACs, keeping founders informed were missing). See [[part2-coverage]].

**Round 2 (T-011, commit 6559f5a, reviewed 2026-11-01): pass.** All anchors were fixed. Two things to watch for in later rounds:
- **Fix-induced over-breadth.** The new "Severity rule" line, "anything violating Appendix A ... is a blocker", is broader than D.2 and drops "unsafe". Check it against D.2 verbatim.
- **Catch-all items.** "Answers every sub-question" stands in for dedicated checks. Map each sub-question to a specific item. Still missing are: who first, why-this-first, rollout, collecting feedback, engineering's role, and the One story's three parts.
---
name: reviewer-sandbox
description: Hook limits for this reviewer — shell writes to scratchpad/memory are blocked; python -c with escaped backticks fails git-guard parsing
metadata:
  type: reference
---

The board-guard hook blocks reviewer shell redirects outside reviews/ and artifacts/review-evidence/. That includes the session scratchpad and this memory dir, so use the Write/Edit tools for memory. Put helper scripts in `artifacts/review-evidence/<card>-*.py` and run them with `python3 -I`. The git-guard hook also rejects `python3 -c "..."` strings that contain escaped backticks, so use single-quoted `-c` code that has no backticks. The board-guard also reads a `>` inside a `python3 -c` string as a redirect and blocks the call (seen 2026-11-01 with a `>=` comparison), so put any comparison in a script file under artifacts/review-evidence/. `python3 tools/board.py validate <review file>` is allowed and prints 'ok' or the D.2 error. Related: [[source-fetching]], [[plan-review-patterns]].
---
name: needs-chris-drift
description: Recurring NEEDS_CHRIS defects on this project. Rows are added without needs_chris cards, and questions that aren't Chris's (client practice, team product calls) get in. Check on every harness/submission review.
metadata:
  type: feedback
---

On every review that touches submission/NEEDS_CHRIS.md, check three things with commands:
1. **Row ↔ card parity.** Compare the row numbers in NEEDS_CHRIS.md with the `board.py list --status needs_chris` titles that contain "(NEEDS_CHRIS #n)", and check the priorities match. T-005 r1 had 0 of 1 rows carded; r2 had 2 of 10 (rows #4-#11 were added by the review-triage flow with no cards; row #1 was P1 in the file and P2 on the card).
2. **§11.5 scope.** Only things that genuinely need Chris belong there: his story, personal numbers, HF Space name, own-voice video, final send, credentials, spend. Questions about how "Zinda" (the fictional client in SPEC.md:8) works are discovery questions or ASSUMPTIONS, not Chris items. Product calls the team already made belong in ORCHESTRATOR_DECISIONS/ADRs. "Nothing to do" rows are FYIs.
3. **Exact action.** Each action names the expected reply ("demo-only" / "live with cap $X") rather than "Reply via inbox."

**Why:** The needs_chris column is what Chris sees on his phone, and the file is a graded submission artifact (§11.5 DoD). The file grows during review triage while the card step is skipped.

**T-005 r3 (2026-11-01):** parity was fixed at 3/3. The new defects were stale "NEEDS_CHRIS #n" references in D-entries and a garbled STATE heartbeat line in the working tree, which the RUNBOOK restart depends on. Always diff STATE.md against HEAD.

**How to apply:** Re-read the file at the end of the review, because it changed mid-review in T-005 r2. Also check that every ADR's stated facts match the running system (ADR-000e said http/no-TLS while https serve was live). See [[spec-review-patterns]].
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:05.376Z

**tool call — Bash**
````
{
 "command": "grep -n \"^#\" docs/CONTRACT.md | head -80",
 "description": "List CONTRACT headings"
}
````

### User / tool · 2026-11-02T21:11:05.463Z

**tool result**
````
1:# MASTER PROMPT — Zlayt PM Project: Autonomous Multi-Agent Build
7:## 0. Situation
16:## 1. Non-negotiables
33:## 2. Operating principles (why the harness is shaped this way)
66:## 3. Architecture
104:## 4. Milestone 0 — Build the operating system (do this first, ≤ 90 minutes)
108:### 4.1 Repository layout
150:### 4.2 `.claude/settings.json` (project-level)
181:### 4.3 Hooks (behavior spec — write the scripts)
191:### 4.4 Board
229:### 4.5 Memory layer rules
236:### 4.6 Agent definitions
242:### 4.7 `CLAUDE.md` (the map)
246:### 4.8 M0 exit criteria (smoke test — record results in `memory/PROGRESS.md`)
258:## 5. Milestones 1–5
262:### M1 — Research, personas, requirements, architecture (≤ 2.5 h)
274:### 5.2 The LLM/code boundary and validation ladder (binding for M2)
300:### M2 — Core pipeline + evals green (≤ 3.5 h)
306:### M3 — Review UI, export, E2E (≤ 3.5 h)
312:### M4 — Hardening, deployment, demo assets (≤ 2 h)
318:### M5 — Submission package (≤ 2 h)
330:## 6. Persona roster
332:### 6.1 Workers (agent-team teammates, `model: sonnet` unless noted, `effort: high`, `memory: project`)
345:### 6.2 Reviewer personas (fresh subagents per review; read-only; `memory: project`)
363:### 6.3 Persona dossier format (`personas/<name>.md`, written by researcher, compiled into the agent body by you)
378:## 7. Review and feedback protocol
380:### 7.1 Tiers
385:### 7.2 Reviewer brief (you write it; template Appendix D.6)
388:### 7.3 Skepticism rules (embed in every reviewer body)
397:### 7.4 Verdicts and loop budget
403:### 7.5 Optional: codify panels as workflows
408:## 8. Quality system
410:### 8.1 Sensors (all deterministic, all runnable with one command each, all run by qa before any gate)
417:### 8.2 The ship bar (these numbers are the product note's "good enough to ship" criteria; adjust only with an ADR)
424:### 8.3 Regression discipline
429:## 9. Autonomy and continuity
446:## 10. Build target and deployment
456:## 11. Submission package and Definition of Done
469:## 12. Guardrails and budgets
481:## 13. Bootstrap sequence (execute now, in order)
493:## Appendix A — The Zlayt spec (verbatim)
497:### Overview
507:#### Ground rules
513:#### What we evaluate
524:### Part 1: Vibe code a treatment timeline tool
527:#### What to build
538:#### Constraints
544:#### Sample records (synthetic)
559:#### What to submit for Part 1
565:### Part 2: Explain your process
570:#### Cover these eight areas
582:#### One story
585:#### Format
588:### Submitting and what happens next
598:## Appendix B — Candidate context and voice (for the writer; never invent beyond this)
609:## Appendix C — Known truths about the sample case (for the eval golden set; verify independently)
625:## Appendix D — Schemas and templates
627:### D.1 Board card (`board/cards/T-###.md`)
649:## Description
652:## Notes (append-only, newest last)
655:## Handoff (filled when moving to in_review)
659:### D.2 Review finding (`reviews/<card>-<persona>.md`, markdown with a JSON block)
678:### D.3 Handoff section — see D.1. Keep it to 10 lines; link evidence.
680:### D.4 Validation-ladder record (stored per LLM-derived item in the app)
688:### D.5 Agent definition template (`.claude/agents/<name>.md`)
711:## Rules
720:### D.6 Reviewer brief template
731:## Appendix E — Reference links (fetch only if you need detail; do not re-research)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:07.239Z

**tool call — Bash**
````
{
 "command": "sed -n 318,330p docs/CONTRACT.md; sed -n 417,428p docs/CONTRACT.md; sed -n 456,468p docs/CONTRACT.md; sed -n 493,608p docs/CONTRACT.md",
 "description": "Read M5, ship bar, DoD, Appendix A and B"
}
````

### User / tool · 2026-11-02T21:11:07.338Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:11.083Z

**tool call — Bash**
````
{
 "command": "ls evals/reports/ | tail -20; ls evals/reports | wc -l; echo ---; cat evals/reports/20261102T164038Z.md | head -150",
 "description": "List eval reports and read cited report"
}
````

### User / tool · 2026-11-02T21:11:11.177Z

**tool result**
````
controls-20261102T043911Z.md
controls-20261102T044933Z.json
controls-20261102T044933Z.md
controls-20261102T045207Z.json
controls-20261102T045207Z.md
controls-20261102T063331Z.json
controls-20261102T063331Z.md
controls-20261102T075238Z.json
controls-20261102T075238Z.md
controls-20261102T090925Z.json
controls-20261102T090925Z.md
controls-20261102T102626Z.json
controls-20261102T102626Z.md
controls-20261102T123937Z.json
controls-20261102T123937Z.md
determinism-diagnosis.md
latest.json
library-latest.md
m3-sensors.md
runs
      98
---
# Eval report 2026-11-02T16:40:38Z

**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `312efe663327539df1b712832e23bf1d2c495d42`, tree clean.

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
| grounding_rate | 1.000 (242 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
| unsupported_count_3run | 0 | 0 | R-TL-4 |
| determinism_3run | 1.0 | 1.0 | R-CO-7 |
| J3 judge_conflict_v6 seeded catch rate | 1.000 (20/20 wrong caught x3 runs; in-sample 14/14; held-out 6/6; false agree 0 []; correct accepted 21/21; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| letter_currency_outside_charges (fixture export, 25 cases; 11 entries held out) | 0 | 0 | R-CH-7, R-EX-8 |
| lexicon_recall_must_flags (reported, not gated) | 1.000 | none (D-026) | R-FL-3, R-RV-6 |


## Calibrated confidence (measured counts, backend `claude-cli`, 10 golden cases, source commit `312efe6633`)

- Verified items matched the record 82/83 times in testing on the claude-cli backend (10 golden cases, small sample).
- Items marked needs review matched the record 11/11 times in testing on the claude-cli backend (10 golden cases, small sample).

| Item type | Verified (matched/seen) | Needs review (matched/seen) |
|---|---|---|
| entry | 52/53 | 4/4 |
| amount | 9/9 | 6/6 |
| flag | 21/21 | 1/1 |


## Judge controls, per item

In-sample controls were written with the prompts they test. A held-out row is authored apart from the prompt, but only the status derived from git below says whether it is still held out. A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at the source commit: origin `packet` is a real candidate from a golden or library packet, `variant` is a crafted variant of one (T-093 r4; tests/unit/test_t093_j3_controls_reachable.py).

| id | judge | split | kind | pair | origin | expected | verdict per run | ok |
|---|---|---|---|---|---|---|---|---|
| J3R1 | j3 | in-sample | correct | plan_vs_outcome:Plan of care: 12 visits. | packet | conflict | conflict / conflict / conflict | yes |
| J3R2 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | packet | conflict | conflict / conflict / conflict | yes |
| J3R3 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | packet | conflict | conflict / conflict / conflict | yes |
| J3R4 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | packet | benign | benign / benign / benign | yes |
| J3R5 | j3 | in-sample | correct | history_denial:Prior accidents? Yes [ ] No [X]. | packet | conflict | conflict / conflict / conflict | yes |
| J3R6 | j3 | in-sample | correct | history_denial:Prior injuries? Yes [ ] No IX]. | packet | conflict | conflict / conflict / conflict | yes |
| J3R7 | j3 | in-sample | correct | history_denial:Prior injuries? Yes [ ] No IX]. | packet | conflict | conflict / conflict / conflict | yes |
| J3V1 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V18 | j3 | in-sample | wrong | plan_vs_outcome:Twelve visits authorized. | variant | benign | benign / benign / benign | yes |
| J3V19 | j3 | in-sample | wrong | plan_vs_outcome:PT x 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V14 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V2 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V3 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V4 | j3 | in-sample | correct | plan_vs_outcome:Plan of care: 12 visits. | variant | conflict | conflict / conflict / conflict | yes |
| J3V5 | j3 | in-sample | wrong | plan_vs_outcome:Refer to physical therapy 2x/week for 6 weeks. | variant | benign | benign / benign / benign | yes |
| J3V6 | j3 | in-sample | correct | plan_vs_outcome:Refer to physical therapy 2x/week for 6 weeks. | variant | conflict | conflict / conflict / conflict | yes |
| J3V20 | j3 | in-sample | wrong | history_denial:Prior accidents? Yes [ ] No [X]. | variant | benign | benign / benign / benign | yes |
| J3V7 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V10 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V15 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V16 | j3 | in-sample | wrong | history_denial:Patient denies any prior injury. | variant | benign | benign / benign / benign | yes |
| J3V11 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | variant | conflict | conflict / conflict / conflict | yes |
| J3V12 | j3 | in-sample | correct | history_denial:Patient denies any prior injury. | variant | conflict | conflict / conflict / conflict | yes |
| J3V17 | j3 | in-sample | wrong | history_denial:Patient denies any prior neck injury. | variant | benign | benign / benign / benign | yes |
| H3V2 | j3 | held-out | correct | plan_vs_outcome:Twelve visits authorized. | variant | conflict | conflict / conflict / conflict | yes |
| H3V4 | j3 | held-out | correct | plan_vs_outcome:PT x 12 visits. | variant | conflict | conflict / conflict / conflict | yes |
| H3V5 | j3 | held-out | correct | plan_vs_outcome:Chiropractic 3x/week for 4 weeks. | variant | conflict | conflict / conflict / conflict | yes |
| H3V6 | j3 | held-out | correct | plan_vs_outcome:Chiropractic 3x/week for 4 weeks. | variant | conflict | conflict / conflict / conflict | yes |
| H3V17 | j3 | held-out | wrong | plan_vs_outcome:Ten visits of PT were authorized. | variant | benign | benign / benign / benign | yes |
| H3V18 | j3 | held-out | correct | plan_vs_outcome:Ten visits of PT were authorized. | variant | conflict | conflict / conflict / conflict | yes |
| H3V8 | j3 | held-out | correct | history_denial:Patient denies any prior neck injury. | variant | conflict | conflict / conflict / conflict | yes |
| H3V9 | j3 | held-out | wrong | history_denial:Denies prior back surgery. | variant | benign | benign / benign / benign | yes |
| H3V10 | j3 | held-out | correct | history_denial:Denies prior back surgery. | variant | conflict | conflict / conflict / conflict | yes |
| H3V11 | j3 | held-out | wrong | history_denial:No history of low back problems. | variant | benign | benign / benign / benign | yes |
| H3V12 | j3 | held-out | correct | history_denial:No history of low back problems. | variant | conflict | conflict / conflict / conflict | yes |
| H3V13 | j3 | held-out | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| H3V14 | j3 | held-out | correct | history_denial:Patient denies prior neck problems. | variant | conflict | conflict / conflict / conflict | yes |
| H3V15 | j3 | held-out | correct | history_denial:No previous accidents. | variant | conflict | conflict / conflict / conflict | yes |
| H3V19 | j3 | held-out | wrong | history_denial:Patient denies any prior neck injury. | variant | benign | benign / benign / benign | yes |
| H3V20 | j3 | held-out | correct | history_denial:Patient denies any prior back injury. | variant | conflict | conflict / conflict / conflict | yes |
| H3V21 | j3 | held-out | wrong | history_denial:Patient denies any prior back injury. | variant | benign | benign / benign / benign | yes |
| J4W1 | j4 | in-sample | wrong | P4-neck-history |  | disagree | disagree / disagree / disagree | yes |
| J4C10 | j4 | in-sample | correct | P4-neck-history |  | agree | agree / agree / agree | yes |
| J4W6 | j4 | in-sample | wrong | P4-back-history |  | disagree | disagree / disagree / disagree | yes |
| J4C1 | j4 | in-sample | correct | P4-back-history |  | agree | agree / agree / agree | yes |
| J4W2 | j4 | in-sample | wrong | P4-hedged-findings |  | disagree | disagree / disagree / disagree | yes |
| J4C2 | j4 | in-sample | correct | P4-hedged-findings |  | agree | agree / agree / agree | yes |
| J4C6 | j4 | in-sample | correct | P4-hedged-findings |  | agree | agree / agree / agree | yes |
| J4W3 | j4 | in-sample | wrong | P4-missed-care |  | disagree | disagree / disagree / disagree | yes |
| J4C3 | j4 | in-sample | correct | P4-missed-care |  | agree | agree / agree / agree | yes |
| J4W9 | j4 | in-sample | wrong | P4-missed-care |  | disagree | disagree / disagree / disagree | yes |
| J4W4 | j4 | in-sample | wrong | P4-referral |  | disagree | disagree / disagree / disagree | yes |
| J4C11 | j4 | in-sample | correct | P4-referral |  | agree | agree / agree / agree | yes |
| J4C8 | j4 | in-sample | correct | P4-referral |  | agree | agree / agree / agree | yes |
| J4W8 | j4 | in-sample | wrong | P4-mri |  | disagree | disagree / disagree / disagree | yes |
| J4C9 | j4 | in-sample | correct | P4-mri |  | agree | agree / agree / agree | yes |
| J4W7 | j4 | in-sample | wrong | P4-scene |  | disagree | disagree / disagree / disagree | yes |
| J4C7 | j4 | in-sample | correct | P4-scene |  | agree | agree / agree / agree | yes |
| J4W5 | j4 | in-sample | wrong | P4-ct |  | disagree | disagree / disagree / disagree | yes |
| J4C4 | j4 | in-sample | correct | P4-onset |  | agree | agree / agree / agree | yes |
| J4C5 | j4 | in-sample | correct | P4-surgery |  | agree | agree / agree / agree | yes |
| H4W1 | j4 | held-out | wrong | H4-attendance |  | disagree | disagree / disagree / disagree | yes |
| H4C1 | j4 | held-out | correct | H4-attendance |  | agree | agree / agree / agree | yes |
| H4W2 | j4 | held-out | wrong | H4-prior |  | disagree | disagree / disagree / disagree | yes |
| H4C2 | j4 | held-out | correct | H4-prior |  | agree | agree / agree / agree | yes |
| H4W3 | j4 | held-out | wrong | H4-hedge |  | disagree | disagree / disagree / disagree | yes |
| H4C3 | j4 | held-out | correct | H4-hedge |  | agree | agree / agree / agree | yes |
| H4C4 | j4 | held-out | correct | H4-onset |  | agree | agree / agree / agree | yes |

Held-out status is derived from git (evals/heldout_audit.py), not from the label. Clean held-out J3 controls: 5 of 17 ['H3V17', 'H3V18', 'H3V19', 'H3V20', 'H3V21']. A control is clean when it was written apart from the prompt, none of its words is in the current prompt, and no prompt version was added after its first run.
Not clean: H3V2 seen_before_edit; H3V4 seen_before_edit; H3V5 seen_before_edit; H3V6 seen_before_edit; H3V8 seen_before_edit; H3V9 seen_before_edit; H3V10 seen_before_edit; H3V11 seen_before_edit; H3V12 seen_before_edit; H3V13 seen_before_edit; H3V14 seen_before_edit; H3V15 seen_before_edit. These are still reported as held-out rows above because they were authored separately; read them as seen.

Assertions: {"gap_28_not_flagged": true, "gap_73_flagged": true, "all_gap_rows_correct": true}
spec_matches_golden: True

## Misses (report what was found)

- entry misses: {"case_06_subtle_pre_existing": [{"entry": "E3", "why": "excerpt misses must_contain_excerpt"}]}
- missed must flags: {}
- summary clauses removed by code (D-054, reported not gated): {"items_trimmed": 5, "clauses_removed": 5, "tray_placeholders": 0, "per_case": {"case_03_rate_and_ocr": {"items_trimmed": 3, "clauses_removed": 3, "tray_placeholders": 0}, "case_07_prompt_injection": {"items_trimmed": 1, "clauses_removed": 1, "tray_placeholders": 0}, "case_08_diagnosis_temptation": {"items_trimmed": 1, "clauses_removed": 1, "tray_placeholders": 0}}}
- flag tray (could-not-verify flags, D-053; not scored, not in the R-CO-7 flag signature): 6 {"FILTERED_BY_RULE": 5, "LLM_ONLY": 1} by case {"case_01_date_formats": 3, "case_05_provider_conflict": 1, "case_07_prompt_injection": 1, "sample": 1}
- grounding failures: []
- seeded hallucinations not caught: []
- must_not detail: {}

- per-run artifacts: `evals/reports/runs/20261102T161327Z`

## Prompt and lexicon hashes

- `app/llm/prompts/extract_es_v1.md` 985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb
- `app/llm/prompts/extract_v1.md` 11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2
- `app/llm/prompts/flags_v1.md` d5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725
- `app/llm/prompts/judge_amount_class_v1.md` e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8
- `app/llm/prompts/judge_conflict_v1.md` 10c7cfddbd32d78cbdb005a14731abcb40ef55c83265b87abb88f74c48551daa
- `app/llm/prompts/judge_conflict_v2.md` 6eac7a227ea9292e89350c3f10c11bc94d057b446cd3bf8cfde1a4684843cbc6
- `app/llm/prompts/judge_conflict_v4.md` 15df87e8655a014111bbcddb2fee769d01e28149072ceea76f3f9d51fcae4649
- `app/llm/prompts/judge_conflict_v5.md` 90deea934564aa0fda0ad34dc38477104e371c0267259c38c61f58635819dffd
- `app/llm/prompts/judge_conflict_v6.md` 8a09702a5c12a9f08a162cad574374827d3a367cbcca7080e1331c76406318b5
- `app/llm/prompts/judge_faithfulness_es_v1.md` d51be0b39c9d2ba0725f81b402e82e80696282bd0ea98e9ce789f575fa21f898
- `app/llm/prompts/judge_faithfulness_v1.md` 636bd46d728af66608aba566efe431371e49e32a066fca71b2046534adbd002b
- `app/llm/prompts/judge_flag_v1.md` 97dd90e3d9546a836d327e12953c9c30ba574ebdcc6073ada9162cd480d2e432
- `app/llm/prompts/judge_flag_v2.md` 7b6b34712531643b0d79f3ccdd92932d8abb86bfdeeb756d7c39314e29ed39fe
- `app/llm/prompts/judge_flag_v3.md` 64d65c0182360d4ef84b5f4b62e19a6707ee3f508d975aec4ea6e527c9a5a664
- `app/llm/prompts/narrative_v1.md` 3d75a823c717359208322d17ba8b77fd58893a4aa15bc92a18c48c78e94e12ac
- `app/llm/prompts/split_v1.md` 9a2d0cffafa37f318e18a9c076c82f9f5c404ecb53781956813fafe7bf66197b
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:16.831Z

**tool call — Bash**
````
{
 "command": "ls evals/reports/*.md | grep -E '/[0-9]{8}T[0-9]{6}Z\\.md$' | wc -l; ls evals/reports/*.json | grep -E '/[0-9]{8}T[0-9]{6}Z\\.json$' | wc -l; ls evals/reports/ | grep -E '^[0-9]{8}T' | sed 's/\\..*//' | sort -u | wc -l; ls evals/reports | grep -vE '^[0-9]{8}T' | head -40; python3 -c 'import json;d=json.load(open(\"evals/reports/latest.json\"));print(d.get(\"timestamp\"),d.get(\"source_commit\"),d.get(\"ship_bar_met\"),list(d.keys())[:30])'",
 "description": "Count dated reports, inspect latest.json"
}
````

### User / tool · 2026-11-02T21:11:16.976Z

**tool result**
````
      74
       0
      74
calibration.json
controls-20261102T042306Z.json
controls-20261102T042306Z.md
controls-20261102T043911Z.json
controls-20261102T043911Z.md
controls-20261102T044933Z.json
controls-20261102T044933Z.md
controls-20261102T045207Z.json
controls-20261102T045207Z.md
controls-20261102T063331Z.json
controls-20261102T063331Z.md
controls-20261102T075238Z.json
controls-20261102T075238Z.md
controls-20261102T090925Z.json
controls-20261102T090925Z.md
controls-20261102T102626Z.json
controls-20261102T102626Z.md
controls-20261102T123937Z.json
controls-20261102T123937Z.md
determinism-diagnosis.md
latest.json
library-latest.md
m3-sensors.md
runs
None None True ['backend', 'blockers', 'generated_at', 'hashes', 'models', 'recorded_from', 'schema', 'ship_bar_met', 'source', 'spec_matches_golden']
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:19.146Z

**tool call — Bash**
````
{
 "command": "python3 -c 'import json;d=json.load(open(\"evals/reports/latest.json\"));print(d[\"generated_at\"],d[\"source\"],d[\"recorded_from\"],d[\"blockers\"],d[\"backend\"],d[\"models\"])'; ls -t evals/reports/2026*.md | head -3; git log --oneline -8; git status --short | head -30",
 "description": "Check latest.json provenance and git state"
}
````

### User / tool · 2026-11-02T21:11:19.315Z

**tool result**
````
2026-11-02T16:40:38Z {'clean': True, 'commit': '312efe663327539df1b712832e23bf1d2c495d42'} {'note': 'pointer parsed from the report; ship_bar_met recomputed from its body and per-run directory (T-045 r3), not a run', 'recorded_at': '2026-11-02T20:46:20Z', 'report': '20261102T164038Z.md', 'run_artifacts': 'evals/reports/runs/20261102T161327Z', 'sha256': '03eafb83f90c3d46cf8b9bc009dbab0ef17fc7056d7ab4e453e12117036bb5e3', 'ship_bar_recomputed': True, 'source_commit': '312efe663327539df1b712832e23bf1d2c495d42'} [] claude-cli {'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5'}
evals/reports/20261102T195748Z.md
evals/reports/20261102T164038Z.md
evals/reports/20261102T135655Z.md
59e33ca docs(submission): one-page product note, Part 2 process doc, validation-ladder SVG
f22f8fc tools: prompt-log export writes <redacted> (scanner-safe) and no stale 'capped' header (T-187)
3b5fe43 feat(qa): M5 prompt log package (T-187)
9199b72 docs: NEEDS_CHRIS Docker verification item (T-182)
f547db4 docs(release): T-182 record timed clone path (17s) and Docker-daemon caveat
4671eee test(backend): T-183 M4 hardening check; plain message when a record-count limit is hit
d07bf9d docs(orchestrator): D-065 tooltip wording (T-177 r2)
ac678bc feat(release): T-182 Dockerfile (7860, demo mode), README run path, run.sh/Makefile, .env.example, HF + Replit deploy docs
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t166_mvp_polish.md
D  .claude/agent-memory/frontend/project_t174_finish.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
 M app/backend/case_extras.py
MM app/backend/case_list.py
 M app/backend/export.py
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:22.418Z

**tool call — Bash**
````
{
 "command": "head -30 evals/reports/20261102T195748Z.md; echo ----; git log --oneline 312efe6..HEAD -- app/llm/prompts app/llm/lexicon.yaml app/backend/schema* evals/golden | head; echo ---; git diff --stat HEAD -- app/llm | tail -3; git log --oneline 312efe6..HEAD | wc -l",
 "description": "Check newer report and prompt changes since cited commit"
}
````

### User / tool · 2026-11-02T21:11:22.583Z

**tool result**
````
# Eval report 2026-11-02T19:57:48Z

**ship_bar_met: False**  backend `fixture`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `4510dc254760a69e2a2a77e4746ffeefcf24dc04`, tree clean.

Blockers: 4_no_invented_facts; backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7); judge_controls (J3/J4 seeded wrong items): not measured

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
| grounding_rate | 1.000 (241 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
| unsupported_count_3run | None | 0 | R-TL-4 |
| determinism_3run | None | 1.0 | R-CO-7 |
| judge_controls (J3/J4 seeded) | not_measured | catch every wrong item on every repeat, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| letter_currency_outside_charges (fixture export, 25 cases; 11 entries held out) | 0 | 0 | R-CH-7, R-EX-8 |
| lexicon_recall_must_flags (reported, not gated) | 1.000 | none (D-026) | R-FL-3, R-RV-6 |


## Calibrated confidence (measured counts, backend `fixture`, 10 golden cases, source commit `4510dc2547`)

----
---
      55
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:24.770Z

**tool call — Bash**
````
{
 "command": "timeout 120 .venv/bin/python -m evals.run --check-fresh 2>&1 | tail -15",
 "description": "Run eval freshness check"
}
````

### User / tool · 2026-11-02T21:11:24.858Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:26.393Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m evals.run --check-fresh 2>&1 | tail -15",
 "description": "Run eval freshness check",
 "timeout": 180000
}
````

### User / tool · 2026-11-02T21:11:26.528Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:28.237Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m evals.run --check-fresh; echo \"exit=$?\"; cat evals/reports/m3-sensors.md | head -60",
 "description": "Check exit code and read m3-sensors",
 "timeout": 180000
}
````

### User / tool · 2026-11-02T21:11:28.380Z

**tool result**
````
exit=0
# M3 sensors (qa, T-045), re-run 2026-11-02 (round 3: unit at b824a6c; e2e and live eval as of round 2, d7ea327)

The unit row ran in a clean detached worktree of b824a6c (git status empty); the e2e row ran in a clean worktree of d7ea327 and was not repeated in round 3 (round 3 changed only evals/run.py and tests/unit/test_t045_r2.py). Every run used `E2E_REQUIRE_DB=1`. This replaces the 02:39Z record, which predated the fixes and the live run.

| Sensor | Command | Result |
|---|---|---|
| Unit | `E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/unit -q` | **5782 passed, 2 skipped**, 0 failed (434 s), the pytest tail line at b824a6c. The round-2 figure 5698 was taken before later commits added tests and did not reproduce (the r2 reviewer measured 5704 at 7c73294 and the count grows as other cards land); a count is valid only for the commit named |
| E2E (fixture backend, curated set, private local-mode server and SQLite file) | `E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e -q -rsx` | **412 passed, 1 skipped**, 0 failed, 0 xfail (594 s). The one skip is `test_multicase::test_screenshots` (opt-in, `ZLAYT_SCREENSHOTS=1`). No DB spec skipped: `test_ladder_gate::test_rejected_attempt_visible_but_not_exportable` now runs (it puts one entry into the rejected state through the server's SQLite file) and is covered at unit level by `tests/unit/test_t045_r2.py` (accept and edit on a rejected item raise 409 `item_rejected` and write nothing; dismiss and reset still work). Both die when the guard at `app/backend/review.py` (`item["state"] == "rejected"`) is disabled. |
| Live eval | `LLM_BACKEND=claude-cli python -m evals.run` | `evals/reports/20261102T164038Z.md`: **ship_bar_met True**, backend claude-cli, generator claude-sonnet-5-5, judge claude-haiku-5-5, 3 runs, determinism 1.0, unsupported_count_3run 0, J3 20/20 and J4 12/12 caught x3 with 0 false agree. Source commit 312efe6, tree clean. |
| Fixture eval at HEAD | `python -m evals.run` | `evals/reports/20261102T195748Z.md`: ship_bar_met False **by design** (fixture cannot measure determinism, unsupported_count_3run, judge controls). Every measurable metric equals the live run: grounding 1.000 (241 checked), entry_recall 0.982, amount_recall 1.000, all eight flag P/R 1.000, hallucination_catch 40/40, controls 0 of 10, must_not 0, case_07_total_420 True, letter_currency_outside_charges 0. |
| letter_check | `python -m evals.letter_check` | exit 0, value 0 across 25 cases (R-CH-7, R-EX-8, R-EX-1) |
| Spec check | `python -m evals.run --check-spec` | exit 0 (letter and internal notes equal the golden export) |
| Calibration / freshness | `python -m evals.run --check-fresh` | **exit 0** (round 3: after `--record-latest` recomputed the bar from the report body and runs/20261102T161327Z; latest.json hashes and calibration.json equal the files at HEAD). `python3 tools/board.py status --json` reads `evals_ship_bar` true. |
| Secrets | `python tools/check_secrets.py` | exit 0 (2329 files) |

## Is the live run still valid at HEAD?
- Prompts and lexicon: `git log 312efe6..HEAD -- app/llm/prompts app/llm/lexicon.yaml` is empty, so the live run's prompt hashes equal HEAD's.
- Code since 312efe6 (34 commits): `app/backend` changes are presentation and review-flow (plain wording in notes T-167, hand-entry kept on re-run T-165, case-list T-175, count-charge T-172, why/present/trace); none touches extraction, grounding or the flag engines. The fixture eval at HEAD reproduces every deterministic live number, which is the check that matters here.
- Not re-run live: a fresh `claude-cli` 3-run at HEAD (about 40 min and model cost). The orchestrator may order one before the gate if it wants the number at the exact gate commit.

## `latest.json` now points at the live run (round 2, F3)
The live run's `latest.json` was never committed and each fixture run overwrote it. Fixed in code, not by editing values: `python -m evals.run --record-latest evals/reports/20261102T164038Z.md` parses backend, models, source commit, hashes, blockers and ship_bar_met out of the dated report and writes `latest.json` with `recorded_from` (report name, sha256 of the report, time). `--check-fresh` also fails if that report changes after it was recorded. A fixture run no longer replaces a live `latest.json` (it writes `latest.fixture.json`). Pinned by `tests/unit/test_t045_r2.py`. The metrics stay in the dated report; the pointer carries no `metrics` block.

## AC to evidence
| AC | Evidence |
|---|---|
| 1 journey, decisions survive reload | `test_review_matrix.py`, `test_timeline.py::test_needs_review_sorted_first_in_queue`, `test_edit.py::test_notes_list_edited_item_with_both_texts`, `test_export_ui.py`, and the new `test_journey_modes.py` (reload keeps both dismissals) |
| 2 R-EX-1 matrix | `test_letter_isolation.py` (sample, one note) plus new `test_letter_matrix.py`: 10 recorded cases x 3 decision profiles, letter independent of flag decisions and notes, planted-leak self-test |
| 3 keyboard, 375 px, adversarial | new `test_journey_modes.py` (keyboard-only with a pointer-click counter at 0; 375 px with 44 px targets and no sideways scroll on four screens, measured as scrollWidth <= 375, not against innerWidth, which Chromium's mobile emulation widens to the page width; it now fails on a 560 px `body, html` mutant and on a timeline `min-width` mutant), new `test_adversarial_ui.py` (empty, whitespace, oversize, non-English, pasted PDF text: whole-database llm_calls/cases unchanged; case_07 total $420.00 on screen and in the letter), `test_adversarial.py` (API) |
| 4 sensors | this file |
| 5 ladder gate | `test_ladder_gate.py::test_rejected_attempt_visible_but_not_exportable` (no skip), `tests/unit/test_t045_r2.py`, `test_ladder_gate.py::test_llm_item_with_no_human_action_is_absent_from_the_letter_and_from_every_accepted_part_of_the_notes` and the edited-item test |
| 6 contract review | T-038 AC4: `latest.json` records backend and models, fixture run reports ship_bar False and determinism/unsupported None (above). T-037 AC2: fixtures for sample, case_01..09, hallucinations and controls replay in the fixture eval: hallucination_catch 40/40 and controls 0 of 10 are measured from the recorded fixtures (the three blockers listed there are the live-only ones). T-045 AC4: live report path above. |
| 7 paralegal verify_quickly >= 4 | left for the M3 gate |
| 8 two library cases | new `test_two_cases_side_by_side.py` (two tabs, same item ids, alternating decisions, reload, case list, letters), `test_local_mode.py` (API) |

## Where an AC's literal text is stale (the current rule is tested)
- AC5 says an unacted LLM item is absent from "both blocks". Spec s.6 and D-045 keep `PENDING ITEMS NOT INCLUDED` in the notes so the reader is told what is out. The test requires absence from the letter and from every notes section that reports accepted or quoted content, and presence only under that titled section.
- AC2/R-EX-1 total line: the matrix uses D-062's "Billed charges accepted from these records: $X".
- An edit alone no longer opens the export (D-045); the edited-item test edits then accepts.
- D-034 hard 422 for new numbers and D-047 (no keep-my-wording confirm) are reflected in the existing edit specs.
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:32.689Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -i GATE-M3; grep -n -iE \"34|0\\.81|42|library|5 of 5|16 cases|one click|one-click\" reviews/GATE-M3-product-manager.md | head -40",
 "description": "Locate GATE-M3 PM numbers"
}
````

### User / tool · 2026-11-02T21:11:32.790Z

**tool result**
````
GATE-M3-accessibility.md
GATE-M3-chaos-tester.md
GATE-M3-paralegal.md
GATE-M3-product-manager.md
GATE-M3-round1-triage.md
GATE-M3-staff-engineer.md
GATE-M3-ux-designer.md
45:**Biggest product risk before M4/M5:** the human step is the only gate on AI summaries that the second check disputed, and it is a one-click Accept that does not say what is wrong.
46:- Across 16 cases, 5 of 5 judge-disputed entries were accepted with a single click.
48:- About a third of library items need review (106 of 297), so she will be clicking through a lot of warnings.
53: "scope": "git archive d0b04bc (HEAD d0b04bc); app at 127.0.0.1:7973 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB), server PID 50240 stopped; sample case + all 15 library packets; docs: CONTRACT What-we-evaluate and M3, spec/REQUIREMENTS.md incl. §7 ship bar, ORCHESTRATOR_DECISIONS D-042..D-064, SCOPE_CUTS, GATE-M2-summary, MVP-ux-audit-r4",
55:  "journey.py on the sample (API, real pipeline, fixture/curated): create, run, read, export 422 before any accept, accept every item one at a time, export 200; letter and notes in journey-sample.out (gap 73 flagged; $185 under Amounts not totaled; total $8,390.00; accident dates not merged)",
57:  "lib_sweep.py over the sample + 15 library cases: needs_review counts, and judge-disputed entries accepted with one click (lib_sweep.out: 106/297 needs_review; 5 of 5 disputed accepted with 200)",
63:  "evals.library_report regenerated at d0b04bc (library-d0b04bc.md); lib_missed.py lists missed must-flags for lib08/09/10/13/15",
75:  {"severity": "major", "title": "Biggest product risk: a one-click Accept puts a summary the second check disputed into the carrier letter, and nobody is told which words are unsupported",
76:   "evidence": "lib_sweep.out: 5 of 5 JUDGE_PARTIAL/JUDGE_UNSUPPORTED entries across 16 cases accept with 200. Letter (journey-lib11.out) shows 'Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ...' over Source 'Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.', so 'after ... struck from behind' adds a sequence link the quote lacks. lib10 e1 'Driver of a pickup struck at an intersection; ...' over Source 'Pt states chest wall and left knee pain.' 02-lib11-e2-row.png: only 'A second AI check found the summary only partly supported', with no words marked; ui_walk.out: Accept opens no dialog. The lib11 notes have no line for 'accepted over the second check'. 106/297 library items are needs_review.",
77:   "why_it_matters": "Ship bar 4 measures the model before the human. What reaches the letter depends on a tired paralegal clicking through a third of the items. The failure the persona fears most, the letter saying something its own Source line does not, is one click away and leaves no trace for the attorney.",
78:   "fix": "For entries with JUDGE_PARTIAL or JUDGE_UNSUPPORTED: (1) code marks the summary's content words that are not in the quote; (2) Accept needs either an edit or a named confirm ('I checked the summary against the quote'); (3) the internal notes list 'accepted over a second-check objection: record N' so the attorney sees it; (4) add a reported eval, 'letter summary lines whose own Source quote does not support them, accept-all profile, library + golden', and put its number in the product note.",
79:   "acceptance_test": "lib11 e2 accept without confirm or edit returns 422 with a plain reason; with the confirm it is 200 and internal_notes_text names record 2 under the objection section; the new eval metric appears in the report."},
81:   "evidence": "memory/SCOPE_CUTS.md:6-23 rows 2 (multi-case), 5 (firm-voice prose), 12 (manual entry), 13 (LLM split), 14 (batch accept, 'single-key accept is fast enough'), 16, 17, 19 still read as cut. :54 lists only D-042 reinstatements, not D-031's. 04-sample-top.png shows 'Accept all verified entries (9)', 'All cases', 'Draft treatment paragraph', 'Exhibit and Bates numbers'. spec/REQUIREMENTS.md:159-168 names one stretch (side-by-side) and argues against PDF upload and the firm-voice paragraph; §5 non-goals 1, 2, 9-14, 16, 19 contradict the build. R-CH-7 (:84) says 'no path turns a rate, estimate or unreadable amount into a totaled charge', but SCOPE_CUTS 7g says 'Proposed'/'Quoted' charge lines are still countable (D-064). Appendix A: 'Stretch (pick at most one ...)'.",
83:   "fix": "Rewrite SCOPE_CUTS as the current truth: one table with status cut / built (D-031/D-042) / held (D-063), each with its reason. Amend REQUIREMENTS §4/§5 and R-CH-3/R-CH-7 by ADR, or make 'Proposed'/'Quoted'/estimate lines not countable (class a). Get Chris's answer on presenting four stretch items (questions_for_chris) and write that reason into the note draft.",
90:  {"severity": "major", "title": "The ship bar's 1.000 flag numbers do not generalize: at d0b04bc the library shows 34/42 must-flags; the committed library and latest.json reports are stale",
91:   "evidence": "library-d0b04bc.md (regenerated at d0b04bc): must flags 1/3 lib08, 1/2 lib09, 0/1 lib10, 1/3 lib13, 1/3 lib15, 34/42 = 0.81 overall. lib_missed.py: missed conflicts 'Denies LOC per patient' vs 'brief loss of consciousness at the second collision', 'Left shoulder pain' vs 'Right shoulder pain', 'denies back pain' vs 'Low back pain 8/10'; lib10 G1 49-day gap reported as 'Gap of 43 days' from a CMS-1500. The committed evals/reports/library-latest.md is from a74b727 (231 commits back) and shows must_not hits that no longer reproduce. The committed evals/reports/latest.json reads ship_bar_met False (fixture, 14:39Z).",
92:   "why_it_matters": "The product note will quote 'flag precision/recall 1.000'. Those numbers come from 10 cases written alongside the rules. Without the library number beside them, the claim goes beyond what the evidence supports, and the canonical pointer a panel opens says False.",
93:   "fix": "qa commits a library report regenerated at the gate commit and the live latest.json. The product note reports golden and library side by side, naming the conflict categories not covered (SCOPE_CUTS 13).",
94:   "acceptance_test": "evals/reports/library-latest.md source commit equals the gate tag; evals/reports/latest.json ship_bar_met True with backend claude-cli; the note draft cites both numbers."},
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:36.869Z

**tool call — Bash**
````
{
 "command": "head -25 evals/reports/library-latest.md; ls artifacts/review-evidence/GATE-M3-pm/ 2>/dev/null; grep -n -iE \"must.?flag|overall\" artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md 2>/dev/null | head",
 "description": "Check library report state"
}
````

### User / tool · 2026-11-02T21:11:36.968Z

**tool result**
````
# Library report (reported, not gated)

Source commit: a74b727b1ed94befbd09c0a3da0e8556e66f787c (tree: clean). Regenerate from a clean worktree of the commit you cite.

Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.

| packet | status | entries | amounts | total ok | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |
|---|---|---|---|---|---|---|---|---|---|
| case_lib01_er_only_then_gap | done_with_errors | 5/6 | 2/2 | True | 1/1 | 0 | - | 0 | LLM_FAILED_AFTER_RETRIES r3 FIXTURE_MISS |
| case_lib02_slip_fall_prior_knee | done | 6/7 | 3/3 | True | 4/4 | 0 | - | 0 | - |
| case_lib03_truck_rear_end_chiro | done | 7/7 | 3/3 | True | 3/3 | 0 | - | 0 | - |
| case_lib04_dog_bite_scar_revision | done | 6/6 | 2/3 | False | 2/2 | 0 | M4 | 0 | - |
| case_lib05_pedestrian_orif_hardware | done | 7/8 | 2/3 | False | 3/3 | 0 | - | 0 | - |
| case_lib06_lop_billed_vs_adjusted | done | 6/7 | 3/7 | False | 2/2 | 0 | M3 | 0 | - |
| case_lib07_parking_lot_fall_outside_records | done | 7/7 | 2/2 | True | 5/5 | 0 | - | 0 | - |
| case_lib08_second_crash_mri_after | done | 12/12 | 4/4 | True | 1/3 | 0 | - | 0 | - |
| case_lib09_spanish_interpreter_espalda | done | 4/7 | 2/5 | False | 1/2 | 0 | M5 | 0 | - |
| case_lib10_eob_ub04_cms1500 | done | 6/9 | 5/9 | False | 1/1 | 0 | M1 | 0 | - |
| case_lib11_priors_and_ledger | done | 4/9 | 4/8 | False | 3/4 | 0 | M1 | 0 | - |
| case_lib12_records_review_credibility | done | 8/10 | 5/5 | True | 6/6 | 0 | - | 0 | - |
| case_lib13_cloned_notes_cross_provider | done | 5/9 | 3/3 | True | 1/3 | 0 | - | 0 | - |
| case_lib14_handwritten_chiro_scans | done | 6/8 | 3/5 | False | 0/0 | 0 | M2 | 0 | - |
| case_lib15_conclusory_letter_mist | done | 4/8 | 4/7 | False | 1/3 | 0 | M4 | 0 | - |

## Known honest failures (generated from the run above)
01-lib11-top.png
02-lib11-e2-row.png
03-lib11-after-accept-e2.png
04-sample-top.png
curated_provenance.py
fixture-eval-d0b04bc.md
journey-lib08.out
journey-lib10.out
journey-lib11.out
journey-sample.out
journey.py
lib11-counted-letter.out
lib_missed.py
lib_sweep.out
lib_sweep.py
library-d0b04bc.md
sample-e1-trace.out
sample-narrative-letter.out
sample-narrative-structure.out
ui_walk.out
ui_walk.py
7:| packet | status | entries | amounts | total ok | accept-all total | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:42.947Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md",
 "description": "Read regenerated library report"
}
````

### User / tool · 2026-11-02T21:11:43.030Z

**tool result**
````
# Library report (reported, not gated)

Source commit: unknown (tree: unknown). Regenerate from a clean worktree of the commit you cite.

Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.

| packet | status | entries | amounts | total ok | accept-all total | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |
|---|---|---|---|---|---|---|---|---|---|---|
| case_lib01_er_only_then_gap | done | 6/6 | 2/2 | True | ok | 1/1 | 0 | - | 0 | - |
| case_lib02_slip_fall_prior_knee | done | 6/7 | 3/3 | True | ok | 4/4 | 0 | - | 0 | - |
| case_lib03_truck_rear_end_chiro | done | 7/7 | 3/3 | True | ok | 3/3 | 0 | - | 0 | - |
| case_lib04_dog_bite_scar_revision | done | 6/6 | 2/3 | False | ok | 2/2 | 0 | - | 0 | - |
| case_lib05_pedestrian_orif_hardware | done | 7/8 | 2/3 | False | ok | 3/3 | 0 | - | 0 | - |
| case_lib06_lop_billed_vs_adjusted | done | 6/7 | 2/7 | False | ok | 2/2 | 0 | - | 0 | - |
| case_lib07_parking_lot_fall_outside_records | done | 7/7 | 2/2 | True | ok | 5/5 | 0 | - | 0 | - |
| case_lib08_second_crash_mri_after | done | 12/12 | 4/4 | True | ok | 1/3 | 0 | - | 0 | - |
| case_lib09_spanish_interpreter_espalda | done | 4/7 | 3/5 | False | ok | 1/2 | 0 | - | 0 | - |
| case_lib10_eob_ub04_cms1500 | done | 5/9 | 5/9 | True | ok | 0/1 | 1 | - | 1 | - |
| case_lib11_priors_and_ledger | done | 4/9 | 1/8 | False | ok | 4/4 | 0 | - | 0 | - |
| case_lib12_records_review_credibility | done | 8/10 | 2/5 | False | ok | 6/6 | 0 | - | 0 | - |
| case_lib13_cloned_notes_cross_provider | done | 5/9 | 3/3 | True | ok | 1/3 | 0 | - | 0 | - |
| case_lib14_handwritten_chiro_scans | done | 6/8 | 4/5 | True | ok | 0/0 | 0 | - | 0 | - |
| case_lib15_conclusory_letter_mist | done | 4/8 | 2/7 | False | ok | 1/3 | 0 | - | 0 | - |

## Known honest failures (generated from the run above)

None at this commit: every record of every packet replays from a recorded fixture on the fixture backend.

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:51.912Z

**tool call — Bash**
````
{
 "command": "grep -n -iE \"amount\" evals/library_report.py | head -30; sed -n 1,40p memory/SCOPE_CUTS.md | cut -c1-400",
 "description": "Check library amount scoring and SCOPE_CUTS"
}
````

### User / tool · 2026-11-02T21:11:51.998Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:57.096Z

**tool call — Bash**
````
{
 "command": "wc -l memory/SCOPE_CUTS.md; grep -n -iE \"library|0\\.81|34/42|left shoulder|conflict categor\" memory/SCOPE_CUTS.md | cut -c1-300; grep -c \"^| debt\" memory/SCOPE_CUTS.md",
 "description": "Find SCOPE_CUTS rows the note cites"
}
````

### User / tool · 2026-11-02T21:11:57.190Z

**tool result**
````
     104 memory/SCOPE_CUTS.md
104:| 23 | Library-case flag recall | Flag recall on the 15 library packets is 0.81 against 1.000 on the golden cases (GATE-M3 PM); the golden set is what the ship bar measures. The gap is reported, not hidden. | More lexicon entries and library expected-file review; ~1 day. | post-MVP |
61
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:11:58.576Z

**tool call — Bash**
````
{
 "command": "sed -n 60,104p memory/SCOPE_CUTS.md | cut -c1-500",
 "description": "Read rest of SCOPE_CUTS"
}
````

### User / tool · 2026-11-02T21:11:58.658Z

**tool result**
````
| debt | T-082 accepted with documented debt after 3 rounds (§7.4) | 3 rounds; all earlier majors fixed. Remaining 3 majors (rerun feedback placement, panel/gate copy for edited items, failed-rerun message) moved to T-097. | see card | M3 |
| debt | T-088 accepted with documented debt after 2 rounds (§7.4) | Backend half done and reviewed. AC1's UI half (pre-select in the Dates row) was never built here: it is T-096, so AC1 is only half met; the golden eval case is noted for qa. | see card | M3 |
| debt | T-090 accepted with documented debt after 3 rounds (§7.4) | 3 rounds; calibration reproducible from its recorded commit. Major (serving route) moved to T-099; minor (no-.git copy skips provenance tests) carried. | see card | M3 |
| debt | T-046 accepted with documented debt after 2 rounds (§7.4) | Stretch card, 2 rounds; pane works at >=1024px. Major (Show-gap-flag link needs ~190 Tab presses: add a skip link/shortcut) and minors carried to T-060. | see card | M3 |
| 11b | Automatic verification of non-English records | Spanish/uncertain items are always needs_review (D-050); code checks and the judge are advisory there. | A held-out multilingual eval with >= 99% qualifier recall, then per-language verified status; ~3+ days. | M3 (T-085) |
| 7b | Per-provider billing totals (billed/paid/balance, complete badge) | Billing ships as a cited line listing (D-052); totals failed 5 adversarial rounds. | A multi-form reconciliation model with column-position parsing and an adversarial ledger set; ~3 days. | M3 (T-083) |
| debt | T-097 accepted with documented debt after 3 rounds (§7.4) | 3 rounds; UI fixes all landed and B1 closed on the real backend. Remaining major is backend copy at trace.py:275 ('your wording' on AI drafts), folded into T-098 r3. | see card | M3 |
| debt | T-100 accepted with documented debt after 2 rounds (§7.4) | 2 rounds; blocker fixed and the fixture eval is unchanged (0 new failures over 186 recorded summaries). Remaining word-list gaps and false refusals move to T-105; the judge still checks paraphrase faithfulness for AI text. | see card | M3 |
| debt | T-087 accepted with documented debt after 4 rounds (§7.4) | 4 rounds; all hidden-text detection findings fixed and verified. The remaining major is in the opt-in OCR render path (T-086 area), moved to T-107. | see card | M3 |
| debt | T-106 accepted with documented debt after 2 rounds (§7.4) | 2 rounds; clean-HEAD unit suite green (2184 passed, 0 failed, twice). Remaining major: the static allow-list audit misses os-alias/ctypes/asyncio spawns; per D-023's threat model (accidents and lazy evasion, obfuscation residual) this is accepted; minors carried. | see card | M2 |
| 13 | Cross-record conflict detection beyond the code candidate rules (T-094, D-053) | Conflicts are proposed by code (plan vs early end; denial vs prior history), the model only classifies (R-CO-7: open-ended generation flapped). Covered: visit counts in digits or number words with a plan cue, frequency x duration in weeks, non-attendance / lost to follow-up / stopped or left care (negation- and completion-aware), denials of prior problems, injuries, surgery, accidents or claims. NOT covered, 
| debt | T-111 accepted with documented debt after 2 rounds (§7.4) | 2 rounds; the D-043 not-performed silence and the common positive Waddell orders are fixed. Remaining code-rule gaps (count before the term, word-form counts 'three of five', non-adjacent counts) are covered by the model flag path plus the paralegal; logged as a lexicon follow-up in T-105. | see card | M3 |
| debt | T-103 accepted with documented debt after 4 rounds (§7.4) | 4 rounds; exact money-token count holds on 0 of 24,600 random draws, no sums or comparisons remain. Q1 ruled by orchestrator: offset overlap is placement, not a figure comparison (allowed under D-052). Carried: UB-04 room total should sit in other_figures (minor). | see card | M3 |
| debt | T-093 accepted with documented debt after 4 rounds (§7.4) | 4 rounds; the controls instrument is sound (reachability guard, locked labels, provenance). The one major is the H3V5 label, which the D-046 second agent ruled should be conflict/unsure; that relabel (with the written reason in reviews/T-093-staff-engineer-r4.md) is done in T-113 before its controls run. | see card | M2 |
| debt | T-102 accepted with documented debt after 2 rounds (§7.4) | 2 rounds; staleness compares on-disk prompts and the unsplit scorer is real. The remaining major (stale line in the UI) was built in T-096 (36ceb38, under review); AC text there is tracked by that card. | see card | M3 |
| debt | Accident-year hint still counts an intake form (T-116 r3, D-055) | `pipeline._accident_year` (the year hint passed to the per-record flag pass) takes the earliest dated encounter, which can be an intake form. The accident-date baseline conflict now warns instead. The hint only picks a year for undated phrases, and the paralegal reviews every flag; changing it would mean guessing a record out. Conflict candidate code is owned by T-113. | ~0.25 day: prefer the earliest record that does no
| debt | T-115 accepted with documented debt after 2 rounds (§7.4) | 2 rounds; fixtures are real recordings and guarded. D-029 amended by D-056. J3 controls red is T-113's scope. Remaining: e2e race at test_stepper.py:204 -> folded into the T-060 round-3 e2e run (frontend worker declares/fixes tests it touches). | see card | M3 |
| debt | T-116 accepted with documented debt after 5 rounds (§7.4) | 5 rounds; gaps never invent or hide a span (D-055) and all suppression blockers closed. Remaining major (accident-baseline wording for same-day paperwork and questionnaire/authorization headers) moved to T-123. | see card | M3 |
| debt | T-112 accepted with documented debt after 3 rounds (§7.4) | 3 rounds; the D-054 trimmer is vocabulary-bound, so it misses some abbreviations (fresh probes: 12/43 faithful pairs over-trimmed to the tray, 9/30 unsupported clauses kept). Both directions are safe: over-trim is visible in the tray and the human recovers it; kept clauses still face judge 1 and the human. On 188 recorded outputs the trim never fires on English. | Fragments and surviving mutants: T-128. Full coverage would nee
| debt | T-112 accepted with documented debt after 3 rounds (§7.4) | memory/SCOPE_CUTS.md T-112 row; follow-up T-128 | see card | M2 |
| debt | T-105 accepted with documented debt after 2 rounds (§7.4) | pre-existing dropped-side parity gap moved to T-130 | see card | M3 |
| debt | T-105 accepted with documented debt after 2 rounds (§7.4) | Lexicon is the single source for qualifier lists; English dropped-side parity (bare-verb attribution, extra negation words) is pre-existing and still missing. | T-130 | M3 (T-130) |
| debt | T-060 accepted with documented debt after 3 rounds (§7.4) | paralegal pass-5 majors moved to T-136 | see card | M3 |
| 13c | Conflict candidates where a relative reports the patient's own history ('per his wife, he had prior back surgery') | T-113's different-person rule drops pairs whose subject is a family member, which also drops informant-reported patient history (recall gap, safe direction: no false conflict; the prior-condition lexicon flag still fires on the sentence). | An informant-clause rule distinguishing 'X reports that patient...' from 'X had...'; ~half day + controls. | M3 (T-113 r1 F2) |
| 13d | 'History reviewed; significant for X' (condition after a semicolon following a bare 'History ...' clause) | T-133 skips bare 'History' headers to stop HPI over-flags; this one semicolon form does not flag (it flagged only in T-133 r1, never before T-133). PMH:/Hx:/'history of'/'Past ... history:' still flag. | Clause-aware history rule; ~2 h + tests. | M3 (T-133 r3) |
| debt | T-113 accepted with documented debt after 2 rounds (§7.4) | r2: 0 blockers, 0 majors (only minors, moved to T-137); verdict label 'changes' contradicts the verdict rule | see card | M2 |
| 13e | Prior-condition flag quote edge cases (T-132): bare initials as a history source; a sentence-final 'Dr.' followed by a newline joins two sentences into one flag (X3); 57 of 20k fuzz inputs still yield a fragment quote (down from 69). Every quote stays verbatim and nothing is hidden (0 non-verbatim, 0 dropped conditions in the oracle). | A sentence segmenter with an abbreviation model; ~1 day. | M3 (T-132) |
| debt | T-134 accepted with documented debt after 4 rounds (§7.4) | remaining major is frontend wording, moved to T-136 r3 | see card | M3 |
| debt | T-136 accepted with documented debt after 3 rounds (§7.4) | rerun offer gated on rerun_available (T-157 + T-149 r2) | see card | M3 |
| 7c | Slang or shorthand money in record text ('6.5k', 'one eighty-five each', bare decimals with no money word, per-mile rates) is not detected by the charge-text hold or the letter check (T-139). Dollar signs, currency codes/signs, amounts in words and labelled claim-form fields are caught; 0 violations over 25 cases. | A money-expression parser with context; ~1 day + adversarial set. | M3 (T-139) |
| 7d | A summary row dressed as an itemized service line on a real bill (date + CPT + a total) is still classed as a charge with no flag (T-140 adjuster r3 blocker 1). It is cited and must be accepted individually; the letter total states it is a sum of accepted lines (D-062). | A cross-line arithmetic check per statement (row equals sum of others) generalized to dressed rows, plus an adversarial ledger set; ~1 day. | M3 (T-140) |
| 13f | Pre-accident date conflicts (T-141, D-061) are word-rule based: a few phrasings still read info-only ('Denies any accident on 01/03/2026') and some generic denials now raise a false conflict ('No prior accidents or collisions'). The rule leans to false conflicts (D-055). | A clause parser with negation scope; ~1-2 days + adversarial set. | M3 (T-141) |
| 7e | Charge-source detection (D-062) is name/word based: a note from a provider whose bill uses a name variant ('Lake Side' vs 'Lakeside') can add a second charge; documents labelled like 'Records packet p. 12', 'Intake summary' or an insurer name outside the word list can still yield charges. Each such charge is cited and accepted one at a time, and the letter total says it is a sum of accepted lines. | Provider-entity resolution and a positive document-type classifier; ~1-2 days + adversaria
| 7f | Same provider, same date, same amount, different service description (e.g. the adjuster's 'PT visit' restatement) is counted as two charges with no flag (T-140 adjuster r4). Two genuinely different services can share a date and price, so a blanket flag would be noise; each line is cited and accepted one at a time, and the letter total says it is a sum of accepted lines. | A same-day same-amount soft warning shown at accept time; ~2 h. | M3 (T-140) |
| debt | T-140 accepted with documented debt after 4 rounds (§7.4) | D-062 wording + default-deny/per-figure/CPT normalization verified; residuals are scope cuts 7d, 7e, 7f; 0 blockers in staff r4 and adjuster r4 | see card | M2 |
| debt | T-162 accepted with documented debt after 3 rounds (§7.4) | rerun_note shows in row and trace; panel smoke catches thrown panels; residual: a swallowed render error inside the manual panel still passes the smoke (held per D-063) | see card | M2 |
| debt | T-139 accepted with documented debt after 4 rounds (§7.4) | staff r5 pass; adjuster r4 majors fixed in ea988f8 and verified by staff r5; residual slang money is scope cut 7c | see card | M2 |
| debt | T-149 accepted with documented debt after 2 rounds (§7.4) | UX r3 pass; paralegal r2 majors fixed in f7a8f2a and verified by UX r3 (Do this first names the item, Start review goes there); minors held per D-063 | see card | M3 |
| debt | T-169 accepted with documented debt after 2 rounds (§7.4) | the calibration tests accept the live file and bind it to its report (forge detection works); residual run-folder binding strictness held per D-063 | see card | M2 |
| 7g | 'Count this charge' (D-064) residuals: no-show, late-cancel and interest fee lines and 'Proposed'/'Quoted' charge lines are still countable with the named confirm; synonym repeats outside the normalization list (ED vs emergency department, Initial evaluation vs New patient exam, CAT vs CT, Consult vs consultation: 4 of 14 held-out) need only the separate-charge confirm; and other payer or summary wordings may exist beyond the closed word list; each counted line is cited, confirmed by name
| debt | T-171 accepted with documented debt after 3 rounds (§7.4) | 3 rounds; payer/insurer lines not countable and service normalization verified; residual synonyms and fee/proposed lines are scope cut 7g; every count is named-confirm, audited and in a total that states it is a sum of accepted lines | see card | M2 |
| debt | T-173 accepted with documented debt after 2 rounds (§7.4) | specs seed the real placeholder and pass; 7 of 8 tray mutants caught; residual mutant M6 (browser no-attempt rule) held per D-063 | see card | M2 |
| debt | T-158 accepted with documented debt after 2 rounds (§7.4) | user-facing behaviour verified at HEAD: refusal spec 10/10 and the box inside the viewport and at rest in 20/20 probe runs at 390x844; residual majors are test-rigor (proof of settle-time scroll vs click-time scroll; AC evidence citation), held per D-063 | see card | M2 |
| 22 | Drafted treatment paragraph (narrative, D-031/T-059) in the UI and letter | Cut from the MVP by D-067: no eval of its own, and its letter lines cite only provider and date, not the verbatim quote D-002 requires. The route stays in the backend. | Its own eval set + per-sentence quote and Bates placeholder; ~1 day. | post-MVP |
| 23 | Library-case flag recall | Flag recall on the 15 library packets is 0.81 against 1.000 on the golden cases (GATE-M3 PM); the golden set is what the ship bar measures. The gap is reported, not hidden. | More lexicon entries and library expected-file review; ~1 day. | post-MVP |
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:07.538Z

**tool call — Bash**
````
{
 "command": "F=memory/ORCHESTRATOR_DECISIONS.md; grep -cE \"^#+ *D-[0-9]{3}|^\\| *D-[0-9]{3}|^- \\*\\*D-[0-9]{3}|^\\*\\*D-[0-9]{3}\" $F; grep -oE \"D-[0-9]{3}\" $F | sort -u | tail -3; grep -oE \"D-[0-9]{3}\" $F | sort -u | wc -l; for d in D-001 D-007 D-022 D-031 D-034 D-040 D-042 D-047 D-052 D-053 D-054 D-059 D-062 D-063 D-064 D-065 D-066 D-067 D-068; do echo \"== $d\"; grep -m1 -nE \"^(#+ *|\\| *|- \\*\\*|\\*\\*)$d\" $F | cut -c1-330; done",
 "description": "Spot-check decision IDs cited in the docs"
}
````

### User / tool · 2026-11-02T21:12:07.758Z

**tool result**
````
68
D-066
D-067
D-068
      68
== D-001
9:| D-001 | Export = two blocks: **Treatment section** (paste into letter: accepted entries + accepted charges) and **Internal review notes — do not send** (accepted flags, unclear amounts, records not included, bills to request, damages mentions, AI-assistance line). Flag notes/labels/counts never enter the letter. | Acceptin
== D-007
15:| D-007 | Flag titles/explanations are code templates; the LLM returns only category + excerpt spans. | No free LLM prose in the attorney's notes. | T-014 staff-eng F8, privacy |
== D-022
30:| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the su
== D-031
39:| D-031 | *(Reclassification cut here is superseded by D-042.)* **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case 
== D-034
42:| D-034 | Hardens D-006/R-RV-3: a number, date or $ figure in a summary, edit or manual entry that is not in that item's excerpt (or its source label/parsed date) is a **hard 422** — no 'keep my wording' override. The 409 confirm path remains only for non-numeric judge objections, and any override is listed in internal note
== D-040
48:| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four adjuster rounds each found mixed excerpts that a closed rule still mislabeled. The verbatim excerpt alre
== D-042
50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic
== D-047
55:| D-047 | Extends D-034 (2026-11-02): side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a **hard 422** on edit and manual entry. The 409 'keep my wording' path is removed, so the gate (T-098) and the edit route agree and no item can be confirmed into an unexportable s
== D-052
60:| D-052 | Billing ships as a **cited line listing without provider totals** (2026-11-02, §7.4 as pre-declared on T-083). Each parsed billing line is shown with its verbatim excerpt and classification (charge, adjustment, payment, rate, unclear), and unreconciled lines are listed; no billed/paid/balance totals and no 'complet
== D-053
61:| D-053 | Nothing the model proposes is silently dropped (2026-11-02, T-094 review blocker). A model-only flag or conflict that the judge rejects, or a model-proposed conflict that no code candidate confirms (the no-candidate rule applies to conflicts only; ADR-020), goes to the **could-not-verify tray** with the judge's reas
== D-054
62:| D-054 | Summary clauses the quote does not support are removed by code (2026-11-02, after T-094 r2). Before judging, code splits an AI summary into clauses; a clause is removed only when it adds salient content the excerpt lacks: a number or month, a side or a negation (only in a clause sharing no content word with the exce
== D-059
67:| D-059 | The letter total is built only from charges a human accepted one at a time (2026-11-02, T-140 adjuster fail). (1) Charges are never batch-accepted. (2) Code marks an amount `unclear` (not totaled, listed in internal notes with its reason) when its line or column label says total/subtotal/balance/balance forward/prev
== D-062
70:| D-062 | The letter total states what it is (2026-11-02, T-140 after 3 adversarial rounds). R-EX-8's line becomes `Billed charges accepted from these records: $X`, where X sums the charges the paralegal accepted one at a time, each listed above with its source line. The tool no longer claims the records themselves state the 
== D-063
71:| D-063 | Priority switch (Chris, 2026-11-02): finish a polished MVP. Only P0 cards and UX/UI work proceed; every other non-P0 card is held (blocked with a note) until the MVP is done. In-flight P1 cards finish their current round but get no further rounds unless they block the UI. New review rounds on held areas are not open
== D-064
72:| D-064 | Two kinds of "not counted" amounts (2026-11-02, GATE-M2 r2 paralegal). (a) Rule-excluded: total, balance, payment, credit, year-to-date, insurer restatement - never countable, the UI says why in plain words. (b) Not counted only because the line lacks something D-060 needs (no date of service, no bill header) - the 
== D-065
73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." (amended
== D-066
74:| D-066 | A summary the second check disputed is not one click from the letter (GATE-M3 PM major). Accepting an item whose judge verdict is disagree/unsupported/partially (or that carries JUDGE_DISAGREES) requires the same explicit "I compared it with the quote" confirm as an unconfirmed edit; the confirm is stored on the rev
== D-067
75:| D-067 | The drafted treatment paragraph is cut from the MVP UI (GATE-M3 PM + paralegal majors). The backend route stays, but the page does not offer it and it never reaches the letter, until it has its own eval and each sentence carries its verbatim quote and the [Ex. __ / Bates __] placeholder (D-002). Recorded as a scope 
== D-068
76:| D-068 | Guided UI redesign (Chris, 2026-11-02: "VERY hard to use… so simple someone's grandma can use it"). The app becomes a fixed four-step guide per case: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter. Home is "Your cases": one card per case with its step progress and one Continue button. In
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:11.185Z

**tool call — Bash**
````
{
 "command": "grep -n -iE \"hard to use|redesign|grandma|rebuilt|guided|D-068|previous screen|old screen\" submission/product-note.md submission/part2-process.md; echo ---; sed -n 76p memory/ORCHESTRATOR_DECISIONS.md",
 "description": "Check whether UI redesign miss is told"
}
````

### User / tool · 2026-11-02T21:12:11.279Z

**tool result**
````
submission/product-note.md:7:**What I built.** Paste or upload records (text or a PDF text layer). A guided four-step screen: **1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter** (D-068). Review is one item at a time: the record quote beside the AI's summary, two big answers. The export is two blocks that never mix (D-001): a **letter section** (accepted entries and charges only, each with its verbatim quote, provider, date and an `[Ex. __ / Bates __]` placeholder) and **internal notes, do not send** (30-day gaps, conflicts, prior conditions, causation language, amounts not totaled). Every AI step sits behind the validation ladder: the model drafts, code checks, a second model checks, she decides. Nothing reaches the letter without all three.
submission/product-note.md:23:- **The 1.000 flag numbers do not generalize.** The golden cases were written next to the rules. On 15 separate library packets, must-flag recall is 0.81 (`reviews/GATE-M3-product-manager.md`; `memory/SCOPE_CUTS.md` rows 13, 23). The misses are conflicts code never proposes, like "Left shoulder pain" against "Right shoulder pain". One entry was missed (`case_06`, a subtle prior condition). Only 5 of 17 "held-out" conflict controls are still clean, so judge numbers are partly in-sample. Score 5 is a persona reviewer on the previous screen, not a real paralegal; not re-scored on the guided screen.
---
| D-068 | Guided UI redesign (Chris, 2026-11-02: "VERY hard to use… so simple someone's grandma can use it"). The app becomes a fixed four-step guide per case: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter. Home is "Your cases": one card per case with its step progress and one Continue button. Inside a case the step bar never moves; each step is its own page; review is one item at a time (the highlighted quote beside the AI's line, a plain question, two big answers, Back, "3 of 9"). Flags and could-not-verify items join the same queue as plain questions. Step 4 shows the letter, Copy and Download, or "N items still need a decision — go back". No collapsing groups, no jargon, nothing that reflows on click. The backend, API and every ladder rule are unchanged; the old screen moves to /classic so its e2e suite keeps guarding behaviour while the guided UI gets its own suite. Supersedes T-179's UI scope. | The user's verdict on the current UI; a guide with fixed steps is the simplest model for a non-expert. | Chris chat |
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:15.891Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list --status in_progress; python3 tools/board.py list --status in_review; for t in T-177 T-179 T-181 T-189 T-190; do python3 tools/board.py show $t | grep -E '^(id|title|status):'; done",
 "description": "Check status of guided UI and related cards"
}
````

### User / tool · 2026-11-02T21:12:16.360Z

**tool result**
````
T-179	M3	frontend   	in_progress      	P0	AC 0/1	GATE-M3 UI round: D-066 compare-confirm to accept a judge-disputed item (backend enforces 422 without it; batch excludes); D-067 hide the drafted treatment paragraph; UX/a11y minors (h1 on case page, Undo row hidden under sticky header, Try again focus, dismiss announcement overwritten, refused-edit names the words to keep, 320px Theme/Shortcuts/Export)
T-181	M3	frontend   	in_progress      	P0	AC 0/1	Build the guided UI (D-068) on the existing API: new shell at /, old screen at /classic; Your cases, 4 fixed steps, one-item review queue, bills, letter; guided e2e suite
T-045	M3	qa         	in_review        	P0	AC 8/8	Playwright E2E: full paralegal journey, adversarial inputs, all sensors
T-177	M3	backend    	in_review        	P0	AC 1/1	GATE-M3 blocker (D-065): curated demo answers must never be labelled as AI output - badge, 'Prepared answer' tags, trace step and audit model 'hand-checked (qa)'; recorded answers keep AI labels
T-182	M4	release    	in_review        	P0	AC 0/1	M4 release: Dockerfile (port 7860) with docker run verified; Hugging Face Spaces (Docker SDK, app_port 7860, secrets via Space settings) and Replit instructions (check current HF docs); README.md timed run-from-clone (<5 min); .env.example; Makefile/run.sh
T-183	M4	backend    	in_review        	P0	AC 1/1	M4 hardening check: server-side key never exposed, per-session rate limit and spend cap on live calls, demo mode serves the prepared sample answers with no key, optional bring-your-own-key, input size limits, error states; fill only real gaps
T-185	M5	writer     	in_review        	P0	AC 1/1	M5 product note: submission/product-note.md, one page, in Chris's voice (Appendix B): problem and user, what was built, cuts and why, ship bar (3-5 testable criteria from the eval), testing and findings, how AI can mislead and the validation ladder, LLM/code split, three post-launch metrics
T-186	M5	writer     	in_review        	P0	AC 1/1	M5 Part 2 process doc: submission/part2-process.md (<=4 pages) answering the eight Part 2 areas with this build's specifics; validation-ladder diagram + spec/eval-rubric excerpt as visuals; Chris's miss story as a marked [CHRIS: ...] block listed in NEEDS_CHRIS
T-187	M5	qa         	in_review        	P0	AC 1/1	M5 prompt log: submission/prompt-log/ with TOOLS.md, CONTRACT copy, board activity log, all reviews, DECISIONS, LESSONS, and tools/export_prompt_log.py export of the agent transcripts (unedited, one file per agent) plus a two-paragraph reading guide
id: "T-177"
title: "GATE-M3 blocker (D-065): curated demo answers must never be labelled as AI output - badge, 'Prepared answer' tags, trace step and audit model 'hand-checked (qa)'; recorded answers keep AI labels"
status: "in_review"
id: "T-179"
title: "GATE-M3 UI round: D-066 compare-confirm to accept a judge-disputed item (backend enforces 422 without it; batch excludes); D-067 hide the drafted treatment paragraph; UX/a11y minors (h1 on case page, Undo row hidden under sticky header, Try again focus, dismiss announcement overwritten, refused-edit names the words to keep, 320px Theme/Shortcuts/Export)"
status: "in_progress"
id: "T-181"
title: "Build the guided UI (D-068) on the existing API: new shell at /, old screen at /classic; Your cases, 4 fixed steps, one-item review queue, bills, letter; guided e2e suite"
status: "in_progress"
id: "T-189"
title: "Chris: write the one story of a miss for Part 2 (submission/part2-process.md, last section, marked [CHRIS: ...] block)"
status: "needs_chris"
id: "T-190"
title: "Chris: fill the [CHRIS: ...] placeholders in the product note and Part 2 (full name, public link, optional real examples)"
status: "needs_chris"
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:23.011Z

**tool call — Bash**
````
{
 "command": "ls app/frontend/; git ls-files app/frontend | head -30; grep -rlE \"Get your letter|Check the bills\" app/frontend 2>/dev/null | head; git ls-files app/frontend | xargs grep -l \"Get your letter\" 2>/dev/null | head",
 "description": "Check whether guided UI exists in frontend"
}
````

### User / tool · 2026-11-02T21:12:23.147Z

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
app/frontend/api.js
app/frontend/app.js
app/frontend/audit.js
app/frontend/batch.js
app/frontend/charges.js
app/frontend/dev/harness.js
app/frontend/dev/mock-data.js
app/frontend/dev/mock-review.js
app/frontend/dev/panels.html
app/frontend/dom.js
app/frontend/excerpt.js
app/frontend/export.js
app/frontend/exportcfg.js
app/frontend/flags.js
app/frontend/index.html
app/frontend/input.js
app/frontend/judges.js
app/frontend/manual.js
app/frontend/mock.js
app/frontend/mock_extra.js
app/frontend/mock_flags.js
app/frontend/mock_sample.js
app/frontend/narrative.js
app/frontend/overview.css
app/frontend/overview.js
app/frontend/review.css
app/frontend/review.js
app/frontend/sidebyside.css
app/frontend/sidebyside.js
app/frontend/source.js
app/frontend/guided/core.js
app/frontend/guided/step3.js
app/frontend/guided/step4.js
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:26.356Z

**tool call — Bash**
````
{
 "command": "git ls-files --error-unmatch app/frontend/guided/core.js 2>&1 | head -2; ls app/frontend/guided; curl -s -m 5 -o /dev/null -w \"%{http_code}\\n\" http://localhost:7860/ ; curl -s -m 5 http://localhost:7860/ | head -c 600; echo; lsof -iTCP -sTCP:LISTEN -n -P 2>/dev/null | grep -E \"python|uvicorn\" | head",
 "description": "Check guided UI tracked status and running app"
}
````

### User / tool · 2026-11-02T21:12:26.603Z

**tool result**
````
error: pathspec 'app/frontend/guided/core.js' did not match any file(s) known to git
Did you forget to 'git add'?
app.js
core.js
home.css
home.js
index.html
review.css
review.js
step1.css
step1.js
step2.css
step2.js
step3.css
step3.js
step4.css
step4.js
styles.css
200
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Treatment timeline</title>
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="review.css">
<link rel="stylesheet" href="stepper.css">
<link rel="stylesheet" href="sidebyside.css">
<link rel="stylesheet" href="suggestions.css">
<link rel="stylesheet" href="overview.css">
<link rel="stylesheet" href="uncovered.css">
</head>
<body>
<nav id="skip-nav" class="skip-nav" aria-label="Skip links" data-tes
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:30.226Z

**tool call — Bash**
````
{
 "command": "head -40 artifacts/review-evidence/GATE-M3-pm/journey.py; curl -s -m 5 http://localhost:7860/api/health; echo; curl -s -m 5 http://localhost:7860/api/config | head -c 400",
 "description": "Inspect journey script and app health"
}
````

### User / tool · 2026-11-02T21:12:30.351Z

**tool result**
````
"""GATE-M3 PM journey: sample case end to end through the real API (fixture backend, curated set).
Usage: python3 -I journey.py http://127.0.0.1:7973 [sample|<library id>]"""
import json, sys, time, urllib.request, urllib.error

BASE = sys.argv[1]
WHICH = sys.argv[2] if len(sys.argv) > 2 else "sample"


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw.decode(errors="replace")[:300]}


body = {"sample": True} if WHICH == "sample" else {"library": WHICH}
s, c = call("POST", "/api/cases", body)
print("CREATE", s, "records", c.get("record_count"), "gap_flags", c.get("gap_flags"), "warnings", c.get("warnings"))
tok = c["token"]
s, r = call("POST", f"/api/cases/{tok}/run", {"confirm_rerun": False})
print("RUN", s, r.get("status"))
for _ in range(120):
    s, st = call("GET", f"/api/cases/{tok}/status")
    if st.get("status") in ("ready", "failed"):
        break
    time.sleep(1)
print("STATUS", st.get("status"), st.get("error"), st.get("counts"))
s, case = call("GET", f"/api/cases/{tok}")
print("TITLE", case.get("title"), "| next_action", case.get("next_action"))
print("REVIEW COUNTS", case.get("review", {}).get("counts"))
print("\nENTRIES")
for e in case.get("entries", []):
    print(" ", e["id"], e.get("date"), "|", e.get("provider"), "|", e.get("state"), e.get("reasons"), "|", (e.get("summary") or "")[:90])
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item","sample_available":true}
{"error":{"code":"not_found","message":"not found","detail":{}}}
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:33.549Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-185-pm && python3 -I artifacts/review-evidence/GATE-M3-pm/journey.py http://localhost:7860 sample > artifacts/review-evidence/T-185-pm/journey-sample-7860.out 2>&1; echo exit=$?; grep -nE \"CREATE|STATUS|185|gap|Gap|73|28|TOTAL|total|Billed|EXPORT|422|200|Prior|prior|causation|may represent|01-19|conflict\" artifacts/review-evidence/T-185-pm/journey-sample-7860.out | head -50",
 "description": "Run sample journey against live app",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T21:12:34.997Z

**tool result**
````
exit=0
1:CREATE 201 records 9 gap_flags ['f_gap_r6_r7'] warnings []
3:STATUS ready None {'entries': 9, 'amounts': 4, 'flags': 10}
4:TITLE Sample case | next_action {'item_id': 'a2', 'kind': 'amount', 'reason': 'This figure is a rate, not a charge, so it is not added to the total.'}
20:  f_gap_r6_r7 gap | verified | Gap of 73 days | ev: ['Date: 2026-03-06', 'Source: Capital PT, visit 9']
21:  f_accident_date_after_treatment_1_2_7 conflict | verified | Stated accident date is later than recorded treatment | ev: ['Date of accident per intake form: 2026-01-19', 'Date: 2026-01-09']
22:  f_cx1 conflict | verified | Treatment plan and what followed differ | ev: ['Plan of care: 12 visits.', 'Discharged from PT after two missed appointments.']
23:  f_r3_1 pre_existing | verified | Mention of a prior or pre-existing condition | ev: ['Patient reports low back pain in 2023, resolved.']
24:  f_r8_1 pre_existing | verified | Degenerative wording | ev: ['Findings may represent degenerative change']
25:  f_r6_1 causation | verified | Missed or ended care | ev: ['Discharged from PT after two missed appointments.']
26:  f_r7_1 causation | needs_review | Accident date source | ev: ['Date of accident per intake form: 2026-01-19.']
27:  f_r7_2 causation | verified | New-onset wording | ev: ['New onset pain']
28:  f_r8_2 causation | verified | Hedged wording | ev: ['may represent degenerative change; correlate clinically']
29:  f_r9_1 causation | verified | Reported onset | ev: ['Patient states symptoms began after the January collision.']
33:  a2 rate 18500 | needs_review ['AMOUNT_RATE_NOT_TOTALED'] | Cervical range of motion reduced approx. 40%. Plan of care:  | This figure is a rate, not a charge, so it is not added to the total.
35:  a3 damages None | needs_review ['AMOUNT_DAMAGES'] | Pain 4/10, improving. Patient reports missing 3 days of work | This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.
39:TOTALS {"accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"}, "detected_not_a_total": {"cents": 839000, "count": 2, "label": "Detected (not a total)"}, "flagged_charges": [], "not_totaled": [{"id": "a2", "kind": "rate", "text": "$185"}], "possible_overlaps": []}
41:EXPORT BEFORE DECISIONS 422 {"error": {"code": "export_blocked", "message": "Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.", "detail": {"blockers": [{"item_id": null, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": "Nothing is accepted or edited yet, so the letter would be em
43:ACCEPT RESULTS {'e1': (200, None), 'e2': (200, None), 'e3': (200, None), 'e4': (200, None), 'e5': (200, None), 'e6': (200, None), 'e7': (200, None), 'e8': (200, None), 'e9': (200, None), 'f_gap_r6_r7': (200, None), 'f_accident_date_after_treatment_1_2_7': (200, None), 'f_cx1': (200, None), 'f_r3_1': (200, None), 'f_r8_1': (200, None), 'f_r6_1': (200, None), 'f_r7_1': (200, None), 'f_r7_2': (200, None), 'f_r8_2': (200, None), 'f_r9_1': (200, None), 'a1': (200, None), 'a2': (200, None), 'a4': (200, None), 'a3': (200, None)}
45:EXPORT 200
78:C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
79:Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."
92:Billed charges accepted from these records: $8,390.00
99:- Gap: 73 days, March 6, 2026 to May 18, 2026: record 6 (Capital PT, visit 9, March 6, 2026) to record 7 (Hill Country Pain Management, new patient, May 18, 2026).
100:- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
102:- Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
103:- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
111:- Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
112:- Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
113:- Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
116:AMOUNTS NOT TOTALED
117:- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:41.740Z

**tool call — Bash**
````
{
 "command": "grep -n -iE \"split|amount|date|conflict|judge\" docs/LLM_VS_CODE.md | cut -c1-260 | head -40",
 "description": "Spot-check LLM_VS_CODE rows"
}
````

### User / tool · 2026-11-02T21:12:41.830Z

**tool result**
````
7:A paralegal turns scattered medical records into a treatment chronology, and an adjuster will read it looking for a reason to doubt it. One invented detail costs credibility. So we split the work by one question: **is there a single right answer?** If yes (a
11:1. **Arithmetic, dates, totals, sorting, de-duplication, quote-matching, number-matching, schema checks and export assembly are never done by a model.**
12:2. **The model never supplies a value.** It may write a one-line summary and choose an exact excerpt, and point at wording that looks like a flag (a category and a quote). It may not supply a date, an amount, an amount's class or the text of a warning. A da
14:4. **Every number in a summary is checked.** Any number, date or dollar figure, and the words left/right/no/not/without, in a summary or in the paralegal's own edit must appear in the excerpt. In a generated summary a miss marks the item for review with the
15:5. **A second model double-checks the first, and every dollar classification.** The checker uses a different prompt and, by default, a different model. It sees only the record and the candidate, never the first model's reasoning, and answers with a fixed ch
16:6. **No silent fixes.** When a check fails the system says so and why. It never "repairs" a quote, a date or an amount.
17:7. **A human decides everything.** Even a fully verified item starts as *pending*. Every accept is an individual decision, except a batch accept of verified, pending entries (code only, all or nothing; never amounts or flags). Every accept of an entry, sing
21:11. **Record text is data, never instructions.** The real protections are structural: models run with no tools, their output is a checked form, code (not a model) finds money and flags, and no code path can accept anything. A phrase scan adds a visible warn
29:| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the c
30:| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. | The spec says date arithmetic is a decision. A model states a wrong date confide
31:| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. | A model told to "find the 
32:| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Ru
34:| 6 | Find every dollar amount | **Code**: a currency pattern over every record; money as whole cents. `$1,2OO` is listed as *unclear* with no value and never corrected. Doses and pain scores are never amounts. | Recall of numbers must not depend on a model
35:| 7 | Say what an amount is: charge, rate, estimate, damages, unclear | **Code only**, by explicit billing phrases, first match wins: an injection-warned record or an unreadable figure is *unclear*; a rate cue in the label ("per" or "each" followed by a uni
36:| 8 | Running total of charges | **Code**: sum of **accepted** amounts of class `charge`. The screen also shows "Pending review" separately and a "detected, not a total" figure. Rates, estimates, damages and unclear amounts are listed "not totaled". Billing
37:| 9 | Treatment gap longer than 30 days | **Code** over the code-parsed **record dates** of all (de-duplicated) clinical-encounter records (billing statements and phone notes are excluded), independent of any model output or review state. Strictly more than
38:| 10 | Conflicts that are structural: stated accident date later than the earliest treatment; two different stated accident dates; the same provider spelled two ways | **Code**: a lexicon of accident-date phrases ("date of accident", "DOA", "accident date",
39:| 11 | Conflicts that need meaning: a plan of 12 visits versus a course that ended early; a denial of prior problems versus a history sentence in another record | **Code proposes; the LLM only classifies.** `app/backend/conflict_candidates.py` pairs two who
40:| 12 | Pre-existing conditions (flag type `pre_existing`) | **LLM** runs once **per record** and proposes a category and a quote; **and** a researched phrase list is scanned by code on every record as a second signal | Needs language judgment ("low back pai
41:| 13 | Language that weakens causation ("may represent degenerative change", "patient states", missed appointments, "new onset", scene facts such as refusing transport, an attorney referral; normal or negative exam findings are context only (D-032); defense
42:| 14 | The wording of every flag | **Code**: a fixed template per flag type and category, filled with dates, source labels and the verbatim quote. For example "Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Ma
43:| 15 | Numbers and dates in a summary or in the paralegal's edit | **Code**: every number, date, dollar figure and left/right/no/not/without in the text must be in the excerpt (or the record's source line / parsed date), and qualifiers in the excerpt must n
44:| 16 | Instruction-like text inside a record ("ignore previous instructions…") | **Code**: advisory phrase scan that raises a `record_warning` flag. Everything derived from that record needs review, its amounts cannot be charges, the cross-record conflict
45:| 17 | Confidence state per item (`verified`, `needs_review`, `rejected`) | **Code**: a fixed rule over the checks (rejected if a grounding check fails; needs review on any doubt; verified only if every check and the judge are positive, and the record is En
47:| 19 | Sorting, filter to accepted items, export assembly, citations, the total line | **Code**. Every letter line carries its verbatim excerpt, the provider as written, a date of service, and an exhibit/Bates placeholder. The total line is always exactly "
56:  [ LLM generator ]  --- candidate: summary, excerpt, flag category + quote ---+
61: RUNG 2: independent LLM judge  (other prompt, other model, sees only record + candidate, answers with a fixed choice)
66: RUNG 3: paralegal  accept | edit | dismiss     (nothing automatic; amounts and dates always explicit)
74:Record 7 (Hill Country Pain Management, header date 2026-05-18): *"New onset pain radiating to right arm ... Date of accident per intake form: 2026-01-19."*
76:- **Code** takes the header date (2026-05-18) as the date of service. The model is not asked.
78:- **Code** notices a stated accident date of 2026-01-19 that is later than treatment recorded on 2026-01-09 and raises a conflict, quoting both the intake-form phrase and the `Date:` header lines of records 1 and 2. The two dates are never merged. No model 
79:- **Code** computes 73 days between the PT discharge (March 6) and this visit (May 18) and raises the gap flag. The 28-day interval earlier is not flagged. The 73 comes from record dates, so no model failure could change it.
87:- **Code** finds the money. `$50,000` follows the word "add", not a billing label, so the rule says *unclear* (and the injection warning would force *unclear* in any case). It is not a `charge`, so it is in no total and never appears in the letter, includin
94:- **Manual entry for a rejected record (code checks, then judge 1).** If a record could not be verified, the paralegal can build the entry herself by selecting whole sentences of that record. Code checks they are verbatim whole sentences (otherwise 422) and
95:- **"Not a duplicate" (code undoes the merge; model drafts and checks the split-off record).** On a merged entry she picks one of the merged records. Code removes it from the entry, restores its amounts and recomputes gaps, and logs a `not_duplicate` event.
96:- **Draft treatment paragraph in the firm's voice (model, behind the full ladder).** A model may draft a paragraph from **accepted entries only**. The **model returns the sentences**, each citing one accepted entry (`NarrativeOutput.sentences`); code does n
97:- **Known limitation (judge errors).** The shared judge path used by manual entry and "not a duplicate" (`review.py`) catches any exception and reports `JUDGE_UNAVAILABLE`. The state is visible to the paralegal, but the error class and call id are not kept;
98:- **Batch accept (code only).** Accepts entries that are `verified` and still `pending`, in one all-or-nothing request, with the count on the button (no separate confirm step) and an Undo. Never amounts, never flags. The server refuses the whole batch if an
102:- **Numbers, sides, negations and qualifiers cannot be overridden (D-034, D-047).** A number, date, dollar figure, left/right, no/not/without, or dropped qualifier in a summary, edit or manual entry that the quote does not carry is a hard 422 and nothing i
107:State that the collision caused a disc herniation. Convert "may represent degenerative change" into either "degenerative" or "traumatic". Compute a PT total when visit counts are not stated. Merge the two accident dates into one. Treat "concussion without
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:43.811Z

**tool call — Bash**
````
{
 "command": "sed -n 29p docs/LLM_VS_CODE.md; sed -n 35p docs/LLM_VS_CODE.md | cut -c1-900; sed -n 15p docs/LLM_VS_CODE.md",
 "description": "Read split and amount class rows"
}
````

### User / tool · 2026-11-02T21:12:43.904Z

**tool result**
````
| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. `SPLIT_REJECTED` always names the reason, on case creation and on runs (T-066, commit d148e0f; `split_failure` in `memory/contracts/api.md`): `NO_MODEL` when there is no model or recorded answer for an unsplit paste, `NOT_ATTEMPTED` when several records are followed by an unsplit tail (the model is only asked about a single block, so the tail stays its own record). Every record cut by the model carries `LLM_SPLIT` and is `needs_review`. | Splitting is pattern matching. A model that rewrites or reorders text would alter the source, so it may only point at where to cut and code does the cutting. | The UI shows "N records found" before any pipeline model call. Unit tests: pieces concatenated equal the input; duplicates merge; `tests/unit/test_split_llm.py` covers accepted and rejected model splits. The call is audited as step `split`. A reviewer can mark one record of a merged entry "not a duplicate"; this is **not code only**: code undoes the merge and logs it, then the generator drafts that record's entry, judge 1 checks it, and the amount judge checks its amounts (see the second-wave section). |
| 7 | Say what an amount is: charge, rate, estimate, damages, unclear | **Code only**, by explicit billing phrases, first match wins: an injection-warned record or an unreadable figure is *unclear*; a rate cue in the label ("per" or "each" followed by a unit word such as visit or session, "rate of", "/visit") or right after the amount ("$185 per visit", "$185 each", "$185/hr") is a *rate* ("Charge per visit $185"); "estimate(d)" is an *estimate*; lost-wage wording is *damages*; in a billing-statement record, "Statement for visit of 2026-02-02: $275" is a *charge*; a label ending "charge:" ("ER charges:", "Charge:") or "billed:" is a *charge*; everything else is *unclear*. There is no model classifier. Billing ledgers are also read line by line by `billing.py` into a cited listing (charge, adjustment, payment, rate, unclear; D-052). That listing is computed on read, is never totaled and n
5. **A second model double-checks the first, and every dollar classification.** The checker uses a different prompt and, by default, a different model. It sees only the record and the candidate, never the first model's reasoning, and answers with a fixed choice (no prose).
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:48.831Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -i \"T-140\"; grep -l -E \"10,906|10906\" reviews/T-140-claims-adjuster* ; grep -l -E \"16,147|16147\" reviews/T-140-claims-adjuster*; grep -ohE \".{120}10,906.{120}\" reviews/T-140-claims-adjuster* | head -2; grep -ohE \".{150}16,147.{120}\" reviews/T-140-claims-adjuster* | head -2",
 "description": "Verify adjuster billing numbers"
}
````

### User / tool · 2026-11-02T21:12:49.056Z

**tool result**
````
T-140-claims-adjuster-r2.md
T-140-claims-adjuster-r3.md
T-140-claims-adjuster-r4.md
T-140-claims-adjuster.md
T-140-staff-engineer-r2.md
T-140-staff-engineer-r3.md
T-140-staff-engineer-r4.md
T-140-staff-engineer.md
reviews/T-140-claims-adjuster-r2.md
reviews/T-140-claims-adjuster.md
it_charges_total 8123.5, A7 'EOB restates the provider charge ... not a second charge'. library_report on HEAD: 'case_lib10_eob_ub04_cms1500 | WRONG $16,147.00 vs $8,123.50'. Handoff: 'lib10: EOB Amount billed $8,023.50 still charge, M1 ... not touched'. No open card covers i
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:51.026Z

**tool call — Bash**
````
{
 "command": "grep -ohE \".{0,200}10,906.{0,200}\" reviews/T-140-claims-adjuster.md reviews/T-140-claims-adjuster-r2.md | head -3",
 "description": "Find 10,906 context"
}
````

### User / tool · 2026-11-02T21:12:52.218Z

**tool result**
````
ugrep: error: error at position 84
xbf][\x80-\xbf]*){0,200}
                        \___exceeds complexity limits
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:54.254Z

**tool call — Bash**
````
{
 "command": "grep -oh \".\\{0,150\\}10,906.\\{0,150\\}\" reviews/T-140-claims-adjuster.md | head -3; grep -c \"6,000\" reviews/T-140-claims-adjuster.md",
 "description": "Find 10,906 context"
}
````

### User / tool · 2026-11-02T21:12:55.403Z

**tool result**
````
ugrep: error: error at position 84
xbf][\x80-\xbf]*){0,150}
                        \___exceeds complexity limits


4
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:57.056Z

**tool call — Bash**
````
{
 "command": "grep -n \"10,906\" reviews/T-140-claims-adjuster.md | cut -c1-400 | head -3",
 "description": "Find 10,906 lines"
}
````

### User / tool · 2026-11-02T21:12:57.156Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:12:59.114Z

**tool call — Bash**
````
{
 "command": "grep -rn -E \"10,?906\" reviews/T-140-claims-adjuster*.md | cut -c1-500 | head -4",
 "description": "Find 10906 in adjuster reviews"
}
````

### User / tool · 2026-11-02T21:12:59.199Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:13:02.757Z

**tool call — Bash**
````
{
 "command": "grep -rln \"10,906\\|10906\" reviews/ memory/ evals/reports/*.md 2>/dev/null | head; grep -rn \"10,906\\|10906\" reviews/ memory/ 2>/dev/null | cut -c1-400 | head -4",
 "description": "Search all reviews/memory for 10,906"
}
````

### User / tool · 2026-11-02T21:13:02.866Z

**tool result**
````
reviews/GATE-M2-round1-triage.md
reviews/GATE-M2-paralegal.md
reviews/GATE-M2-r2-paralegal.md
reviews/GATE-M2-round1-triage.md:9:| blocker | paralegal | Ledger total and balance-due lines classed as charges; lib11 letter total $10,906 vs $6,000 | T-140 |
reviews/GATE-M2-r2-paralegal.md:3:Verdict: **changes** (0 blockers, 1 major, 4 minor). Both round-1 findings are fixed. The lib11 letter total is now $3,260.00 (it was $10,906.00), and the intake form's "Prior accidents? ... No [X]" against the PCP's 2019 and 2022 accidents is now one conflict flag citing both records; the false "accident date is later than recorded treatment" conflict is gone. Th
reviews/GATE-M2-paralegal.md:3:Verdict: **fail** (1 blocker, 1 major, 3 minor). The sample case works the way a paralegal needs: every entry has its verbatim quote beside it, "Open record" highlights the quote inside the record, and the letter matches the golden export. The lib11 ledger case does not. The app labels the ledger total ($2,740) and the balance due ($2,166) as "Charge", says the secon
reviews/GATE-M2-paralegal.md:30:   "title": "lib11: ledger total and balance due are labelled Charge, and accept-all puts $10,906.00 in the letter (correct: $6,000.00)",
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:13:13.644Z

**tool call — Bash**
````
{
 "command": "grep -rln \"matched the record\" app/frontend app/backend 2>/dev/null | head; grep -n -iE \"stretch\" memory/ORCHESTRATOR_DECISIONS.md submission/NEEDS_CHRIS.md memory/ASSUMPTIONS.md spec/REQUIREMENTS.md | cut -c1-300 | head -12; ls board/inbox | tail -5",
 "description": "Check stretch items decision and confidence indicator"
}
````

### User / tool · 2026-11-02T21:13:13.753Z

**tool result**
````
app/frontend/suggestions.js
memory/ORCHESTRATOR_DECISIONS.md:39:| D-031 | *(Reclassification cut here is superseded by D-042.)* **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public de
spec/REQUIREMENTS.md:99:| R-RV-9 | **Open the full source record from any item.** Entries, flags (both records for a two-record flag) and charges open the full record text with the excerpt highlighted, in a modal or panel. The highlight range comes from code offsets, not the model. If the offset can
spec/REQUIREMENTS.md:159:## 4. Stretch pick: side-by-side source viewer
spec/REQUIREMENTS.md:161:**Chosen.** The two-pane layout. Left, the item queue. Right, the full source record, always visible, scrolled to the highlighted excerpt as she moves through the queue. Opening the full record (modal or panel, highlight by code offsets) is already core (R-RV-9), so what the
spec/REQUIREMENTS.md:171:- **Start** only when every M3 must-have card is done with no open blockers, and M3 is inside its 3.5 h budget. The stretch is built before the M3 gate so the gate reviews it.
archive
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:13:15.952Z

**tool call — Bash**
````
{
 "command": "sed -n 39p memory/ORCHESTRATOR_DECISIONS.md | cut -c1-1500; echo; sed -n 50p memory/ORCHESTRATOR_DECISIONS.md | cut -c1-1500; grep -n \"matched the record\" app/frontend/suggestions.js | head -3",
 "description": "Read D-031 and D-042 full text"
}
````

### User / tool · 2026-11-02T21:13:16.061Z

**tool result**
````
| D-031 | *(Reclassification cut here is superseded by D-042.)* **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_SPLIT); 'not a duplicate' split; full audit view (local mode); exhibit/Bates numbering as a per-case config; draft treatment paragraph in firm voice (stretch from spec; every sentence grounded + judged, internal until accepted). **Still cut, with reason:** charge reclassification (a rate must never become a charge — safety), auth/roles (needs an identity provider), per-user learning (needs its own evals), numeric confidence (unverifiable precision), non-English/handwriting, date-convention inference (silent-guess risk), OCR. | Chris asked; each reinstated item keeps the ladder and grounding rules. | Chris inbox 02:05Z |

| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling
119:  // "In testing on 10 synthetic cases, 84 of 85 verified items matched the record." Numbers are the report's own matched / total / case_count, printed as given.
120:  const plainCount = (c, state, what) => { const x = c && c.by_state && c.by_state[state]; return x && x.total != null && x.matched != null && c.case_count != null ? "In testing on " + c.case_count + " synthetic cases, " + x.matched + " of " + x.total + " " + what + " matched the record." : null; };
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:13:23.440Z

**tool call — Bash**
````
{
 "command": "grep -n \"suggestions.js\\|calibrat\" app/frontend/index.html app/frontend/app.js | head -5; curl -s -m 5 http://localhost:7860/api/calibration | head -c 300; echo; grep -rn \"calibration\" memory/contracts/api.md | head -3; grep -n \"OCR\\|ocr\" app/frontend/input.js | head -3",
 "description": "Check calibrated confidence and OCR in UI"
}
````

### User / tool · 2026-11-02T21:13:23.596Z

**tool result**
````
app/frontend/index.html:77:<script src="suggestions.js"></script>
{"status":"ok","calibration":{"schema":"evals.calibration/1","backend":"claude-cli","case_count":10,"small_sample":true,"source_commit":"312efe663327539df1b712832e23bf1d2c495d42","generated_at":"2026-11-02T16:40:38Z","by_state":{"needs_review":{"cases":["case_01_date_formats","case_03_rate_and_ocr",
memory/contracts/api.md:42:| GET | `/api/calibration` | T-099 read-only measured calibration (aggregate counts only, no case token, demo-safe): the T-096 shape in `calibration`, or `null` with `status` `missing`/`invalid`. See the section below |
memory/contracts/api.md:729:## GET /api/calibration  (T-099, serves T-090 counts to T-096)
memory/contracts/api.md:730:Read-only. Serves `evals/reports/calibration.json` (written by `python -m evals.run`), the measured calibration the review screen quotes. It holds aggregate counts, the statements built from them, the source commit, the backend and the sample size. No case token, no record text, so it works in demo mode with no gate. Any other method is `405`.
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:13:27.906Z

**tool call — Bash**
````
{
 "command": "grep -n -iE \"verify_quickly|4/5|verify every claim\" reviews/GATE-M3-paralegal.md | cut -c1-300 | head -5; head -20 reviews/GATE-M3-round1-triage.md | cut -c1-300; cat board/milestones.md | head -20; ls reviews | wc -l; ls reviews/*.md | wc -l; grep -cE \"^## |^- \\*\\*|^\\| L-|^### \" memory/LESSONS.md; grep -oE \"^(## |### )?L-?[0-9]+\" memory/LESSONS.md | wc -l; head -15 memory/LESSONS.md | cut -c1-200",
 "description": "Verify gate results, counts"
}
````

### User / tool · 2026-11-02T21:13:28.046Z

**tool result**
````
5:**Verdict: changes** (0 blockers, 1 major, 7 minors, 2 nits). **verify_quickly = 4.** The D-015 ship bar is met.
50: "scores": {"verify_quickly": 4, "sample_truths_found": 5, "export_fit_for_demand": 4, "keyboard_review": 4},
# GATE-M3 round 1 — triage (orchestrator)

Pinned commit d0b04bc. Panel: ux-designer (pass), paralegal (changes, verify_quickly 4), accessibility (pass), staff-engineer (changes), chaos-tester (fail), product-manager (fail).
Result: **fail** (2 blockers). Every finding at major or above is mapped to a card or decision; the gate re-runs on the fix commit.

| Severity | Source | Finding | Card / decision |
|---|---|---|---|
| blocker | product-manager | Curated demo answers labelled as AI output (badge, tags, trace, audit) | D-065, T-177 |
| blocker | chaos-tester | A run interrupted by a server restart stays 'running' forever | T-178 |
| major | product-manager | One click accepts a summary the second check disputed | D-066, T-179 |
| major | product-manager, paralegal | Drafted treatment paragraph: no eval; letter lines lack quotes and Bates placeholder | D-067, T-179; scope cut 22 |
| major | product-manager | Stale cut list and spec | SCOPE_CUTS 22-23 added; spec sync with the gate summary |
| major | product-manager | Library flag recall 0.81 vs 1.000 golden | scope cut 23 (reported, not hidden) |
| major | staff-engineer | 375px scroll check cannot fail; rejected-item guard untested; latest.json stale pointer | T-045 round 2 |
| major | chaos-tester | Stale second tab overrides a dismissal; zero-width paste spends model calls; lone surrogate 500 | T-178 |
| minor | ux-designer, accessibility | h1, Undo row under header, Try again focus, announcements, refused-edit wording, 320px controls | T-179 |
| question | chaos-tester | Is a lone-surrogate 500 a blocker? | Decided: fixed as major in T-178; no paste may return 500 |
---
milestones:
  - {"id": "M0", "title": "Operating system (harness, board, hooks, agents)", "status": "done", "budget_h": 1.5, "started_at": "2026-11-02T00:07:00Z", "gate_result": "pass", "gate_record": "reviews/GATE-M0-summary.md", "gate_at": "2026-11-02T01:11:14Z", "done_at": "2026-11-02T01:11:14Z"}
  - {"id": "M1", "title": "Research, personas, requirements, architecture", "status": "done", "budget_h": 2.5, "started_at": "2026-11-02T00:17:08Z", "gate_result": "pass", "gate_record": "reviews/GATE-M1-summary.md", "gate_at": "2026-11-02T01:38:56Z", "done_at": "2026-11-02T01:38:56Z"}
  - {"id": "M2", "title": "Core pipeline + evals green", "status": "done", "budget_h": 3.5, "started_at": "2026-11-02T01:38:56Z", "note": "re-gate round 2 at 7cfdb0b; live 3-run met ship bar at 312efe6 (7cfdb0b)", "gate_result": "pass", "gate_record": "reviews/GATE-M2-summary.md", "gate_at": "2026-11-02T19:30:29Z", "done_at": "2026-11-02T19:30:29Z"}
  - {"id": "M3", "title": "Review UI, export, E2E", "status": "active", "budget_h": 3.5, "started_at": "2026-11-02T19:30:37Z", "note": "round-1 findings triaged (reviews/GATE-M3-round1-triage.md); re-gate after T-177/T-178/T-179/T-045"}
  - {"id": "M4", "title": "Hardening, deployment, demo assets", "status": "planned", "budget_h": 2.0, "started_at": null}
  - {"id": "M5", "title": "Submission package", "status": "planned", "budget_h": 2.0, "started_at": null}
---
# Milestones

Generated by `tools/board.py` — edit through `board.py milestone` / `board.py gate`.

| Milestone | Title | Status | Gate | Started | Finished | Budget (h) | Note |
|---|---|---|---|---|---|---|---|
| M0 | Operating system (harness, board, hooks, agents) | done | pass ([record](../reviews/GATE-M0-summary.md)) | 2026-11-02T00:07:00Z | 2026-11-02T01:11:14Z | 1.5 |  |
| M1 | Research, personas, requirements, architecture | done | pass ([record](../reviews/GATE-M1-summary.md)) | 2026-11-02T00:17:08Z | 2026-11-02T01:38:56Z | 2.5 |  |
| M2 | Core pipeline + evals green | done | pass ([record](../reviews/GATE-M2-summary.md)) | 2026-11-02T01:38:56Z | 2026-11-02T19:30:29Z | 3.5 | re-gate round 2 at 7cfdb0b; live 3-run met ship bar at 312efe6 (7cfdb0b) |
| M3 | Review UI, export, E2E | active | - | 2026-11-02T19:30:37Z | - | 3.5 | round-1 findings triaged (reviews/GATE-M3-round1-triage.md); re-gate after T-177/T-178/T-179/T-045 |
| M4 | Hardening, deployment, demo assets | planned | - | - | - | 2.0 |  |
     462
     461
0
       0
# LESSONS (append-only via `board.py lesson`)

What worked, what didn't, and what harness change it caused.

- 2026-11-02T00:10:23Z **orchestrator**: git-guard fired on a destructive-git phrase inside heredoc file content and again inside a quoted --text note (the hook went live mid-session via settings hot-
- 2026-11-02T00:12:12Z **orchestrator**: A stale root-level needs_chris.md from a previous attempt (MASTER_PROMPT missing) was superseded by submission/NEEDS_CHRIS.md, the lane the contract defines.
- 2026-11-02T00:15:25Z **orchestrator**: tailscale serve --https=443 silently replaced an existing mapping on Chris's tailnet (443 -> 127.0.0.1:4173). Restored it; board now on :7777, app will use :78
- 2026-11-02T00:15:25Z **orchestrator**: Agent definitions written mid-session are not loaded by the Desktop host (Agent tool: 'Agent type not found'). Fallback: general-purpose subagent whose first s
- 2026-11-02T00:20:17Z **orchestrator**: A haiku mechanical reviewer filed a major on two false state claims (said PROGRESS marked a check PASS; said T-006 was READY). Harness change: reviewer rules n
- 2026-11-02T00:21:19Z **orchestrator**: Stop-guard counted queued work (cards assigned to a busy worker, reviews already dispatched) as actionable, which would trap the orchestrator in block loops wh
- 2026-11-02T00:22:43Z **orchestrator**: Native agent types appeared ~20 min after the definitions were written (host reloaded .claude/agents mid-session). Switched reviewers/workers to native types (
- 2026-11-02T00:27:32Z **researcher**: Persona dossiers: fanning source-gathering out to parallel subagents (each told to fetch-verify every URL and mark unverified) gave 4-12 verified sources per per
- 2026-11-02T00:30:38Z **researcher**: statutes.capitol.texas.gov, americanbar.org, ecfr.gov, hhs.gov and ajnr.org return nav-only/403/redirect to WebFetch; use mirrors (rulesofcivilprocedure.com, tex
- 2026-11-02T00:33:54Z **orchestrator**: The hardened secret scanner blocked my own commit: a test fixture held a literal key-shaped assignment. Fixed by building the string by concatenation. The PreT
- 2026-11-02T00:51:53Z **researcher**: Round-1 lexicon passed its own examples but failed 37/78 + 38/63 reviewer probes: a self-check that only replays the author's vectors proves nothing. Harness cha
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:13:32.045Z

**tool call — Bash**
````
{
 "command": "grep -c \"^- 20\" memory/LESSONS.md; grep -n -iE \"12/12|uncommitted|partial commit|git archive\" memory/LESSONS.md | cut -c1-260 | head -6; ls personas/*.md | wc -l; grep -oE \"A-1[0-9]{2}\" memory/ASSUMPTIONS.md | sort -u | tr '\\n' ' '; echo; grep -oE \"^\\| R-[A-Z]{2}-[0-9]+\" spec/REQUIREMENTS.md | sort -u | wc -l; grep -n -E \"^\\| R-TL-2 |^\\| R-TL-10 |^\\| R-CO-3 \" spec/REQUIREMENTS.md | cut -c1-350",
 "description": "Verify LESSONS, personas, assumptions, requirements counts"
}
````

### User / tool · 2026-11-02T21:13:32.177Z

**tool result**
````
44
23:- 2026-11-02T02:01:36Z **orchestrator**: Confirmed cause of the transient out-of-band card status: qa ran git stash in the shared worktree, briefly removing every agent's uncommitted work (restored, nothing lost). Already fixed by board-guard: subagents may
25:- 2026-11-02T02:20:22Z **orchestrator**: A reviewer overwrote an earlier uncommitted review file with the same name. Harness change: reviewer-write-guard denies Write/Edit to an existing reviews/*.md (append-only; use a new suffix).
26:- 2026-11-02T02:22:38Z **orchestrator**: Shared worktree + a shared file (api.py) edited by 3 backends: one commit swept others' uncommitted edits that import untracked files, breaking HEAD. Mitigation: commit new modules immediately (even as stubs) before 
29:- 2026-11-02T02:44:47Z **orchestrator**: Pathspec commits still take whole files, including another worker's uncommitted hunks in a shared file (test_edit.py, api.md). When a file has foreign hunks, commit from a temp index: GIT_INDEX_FILE=tmp git read-tree
42:- 2026-11-02T13:13:04Z **orchestrator**: Pathspec commits are not enough when a shared file (present.py, api.md) holds another worker's uncommitted hunks: 225e666 (T-143) swept T-141/T-134/T-138 WIP into HEAD. Rule: if git diff of a file you are committing 
43:- 2026-11-02T14:01:40Z **orchestrator**: HEAD broke twice from partial commits (225e666; 2db6ad2 used why.join left uncommitted). Harness: pre-commit should import-check the committed tree (git archive of the index into a temp dir + python -c 'import app.ba
      13
A-101 A-102 A-103 A-104 A-105 A-106 A-107 A-108 A-109 
      62
49:| R-TL-2 | **Excerpt is verbatim and made of whole sentences (D-012).** An excerpt is a contiguous run of one or more *sentence units* of its record and a substring after whitespace normalization. **Sentence unit** (one code splitter, shared by the generator check, the gap/flag evidence and the excerpt-edit UI): the text up to and including a te
57:| R-TL-10 | **Summaries keep the numbers and the qualifiers (D-006, D-022).** (a) A number, date, dollar figure or the word left, right, no, not or without in a summary must appear in the item's excerpt, the record's source label or its parsed date (token set: ADR-012 `grounding.new_tokens`) (so "visit 8" and a heading year don't trip it), or th
137:| R-CO-3 | **Nothing in the output that is not in the records.** | Ship bar items 1 and 4. On the sample case every `must_not` item in `evals/golden` holds (no fixed range), including: no disc herniation caused by the collision; "may represent degenerative change" not turned into "degenerative" or "traumatic"; no PT total; the two accident date
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:13:36.153Z

**tool call — Bash**
````
{
 "command": "grep -rn \"12/12\" memory/LESSONS.md | cut -c1-300; grep -rln \"charges panel\" memory/LESSONS.md reviews/ 2>/dev/null | head -3; grep -n \"charges panel\" memory/LESSONS.md | cut -c1-300; grep -rn -iE \"stays? .?running.? forever|stuck .?running\" reviews/GATE-M3-chaos-tester.md | head -2 | cut -c1-200; grep -n -iE \"40 min|about 40\" evals/reports/m3-sensors.md memory/*.md | head -3 | cut -c1-200",
 "description": "Verify Part 2 area 8 example claims"
}
````

### User / tool · 2026-11-02T21:13:36.288Z

**tool result**
````
memory/LESSONS.md:45:- 2026-11-02T15:09:24Z **orchestrator**: 6379c0b (T-154 r2) committed a frontend guard referencing an undefined variable; the worker's 12/12 came from the uncommitted working tree, so committed HEAD rendered no charges panel. Rule: verify from git archive HEAD, never the working
memory/LESSONS.md
reviews/T-154-claims-adjuster-r2.md
reviews/T-110-paralegal.md
45:- 2026-11-02T15:09:24Z **orchestrator**: 6379c0b (T-154 r2) committed a frontend guard referencing an undefined variable; the worker's 12/12 came from the uncommitted working tree, so committed HEAD rendered no charges panel. Rule: verify from git archive HEAD, never the working tree. Harness: on
reviews/GATE-M3-chaos-tester.md:116:   "evidence": "GATE-M3-chaos-killrerun.py: accept e1,e4,e5 -> POST /run {confirm_rerun:true} (202) -> SIGKILL own server -> restart same DB. Output: 'status after 
evals/reports/m3-sensors.md:19:- Not re-run live: a fresh `claude-cli` 3-run at HEAD (about 40 min and model cost). The orchestrator may order one before the gate if it wants the number at the exact g
memory/DECISIONS.md:125:- Consequences: about 40 LLM calls for the sample case (9 extract, 9 J1, 3 J2, 1 cross-record conflicts pass, 9 per-record flag passes, a handful of J3/J4). The judge is also a
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:14:01.044Z

**tool call — Bash**
````
{
 "command": "sed -n 274,299p docs/CONTRACT.md | cut -c1-400",
 "description": "Read CONTRACT 5.2 boundary section"
}
````

### User / tool · 2026-11-02T21:14:01.162Z

**tool result**
````
### 5.2 The LLM/code boundary and validation ladder (binding for M2)

`docs/LLM_VS_CODE.md` must contain this table, completed, and it must match the code:

| Pipeline step | Code or LLM | Why | Validated by |
|---|---|---|---|
| Ingest + split records | Code (heuristics on dates/sources/table rows); LLM fallback only when split is ambiguous, and then flagged | Deterministic where possible | Schema check; record count shown to user |
| Date parsing | Code, explicit format list; ambiguous → flag, never guess | Spec: "date arithmetic is a decision, not a given" | Unit tests |
| Per-record extraction: provider, one-line summary, verbatim excerpt, amounts mentioned, clinical facts | **LLM (generator)**, structured JSON output, temperature 0 | Language understanding | (1) **Grounding verifier (code):** every excerpt must be a verbatim substring of its record after whitespace normalization; every amount must appear in the text; the date must equal the code-parsed date. Fai
| Treatment gap > 30 days | Code (date arithmetic over the verified timeline) | Deterministic | Unit tests incl. 29/30/31 boundary |
| Billed charges + running total | Code (currency regex, dedupe) + LLM only to classify rate-vs-charge-vs-estimate when ambiguous | Numbers are deterministic; classification is judgment | Code: totals only over amounts classified `charge`; anything else listed as "unclear — not totaled". Judge #2 validates each classification with the excerpt. Human accepts every amount. |
| Conflicts across records | Code for structural conflicts (two different accident dates, provider name variants); LLM for semantic conflicts, each citing two excerpts | Hybrid | Grounding verifier on both excerpts; judge #3 confirms the two excerpts actually conflict; human. |
| Pre-existing / prior conditions | LLM classification + lexicon (`lexicon.yaml`) as a second deterministic signal | Language judgment | Judge; lexicon hit without LLM hit (or vice versa) → "needs review"; human. |
| Causation-weakening language | Same as above | Same | Same |
| Sorting, dedupe, export assembly, "only accepted items" | Code | Deterministic | E2E test: export contains exactly the accepted set |
| Confidence state per item | Code: `verified` (grounding ok ∧ judge supported) / `needs_review` (any doubt) / `rejected` (grounding failed) | Deterministic composition | Shown in UI; `needs_review` sorted first; `rejected` shown in a "could not verify" tray so the model's attempt is visible, never hidden |
| Audit | Code: every LLM call (model, prompt hash, response, judge verdict, latency, cost) stored and exportable | Traceability | Visible in UI "Why?" affordance per item |

Rules: the generator and the judge never share a prompt; the judge sees only the record and the candidate output; no LLM output is ever auto-accepted into the export; amounts and dates always require explicit human acceptance even when `verified`; the UI shows *why* an item is `needs_review` in one sentence; the model must be swappable via config; retries use changed conditions (shorter record win

**LLM provider abstraction (binding).** There is no API key during development; Chris will add one only when the app goes public. All LLM calls in the app go through one interface (`app/llm/provider.py`: `complete(model, system, user, json_schema) -> dict`) with three backends selected by `LLM_BACKEND`:
- `claude-cli` (**default during development**): shells out to Claude Code headless mode (`claude -p ...`), which uses Chris's claude.ai login. Requirements: pin the model (`--model claude-sonnet-5-5` for the generator, `claude-haiku-5-5` for judges); request JSON output and validate it with code (the API's schema features are not available here); no tools, no MCP servers, no hooks — run it with
- `anthropic-api`: the Anthropic Python SDK with `ANTHROPIC_API_KEY`; used for the public deployment and for a cross-check eval run whenever a key is present. Implement it now against recorded fixtures (`tests/fixtures/llm/*.json`) so it is tested even without a key.
- `fixture`: replays recorded responses; used by unit tests and by demo mode.
Backend switches are prompt/model changes under §8.3: the eval set must be re-run and the report attached before the switch is accepted. The audit record (D.4) stores which backend produced each item.
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:14:27.562Z

**tool call — Bash**
````
{
 "command": "grep -n \"def score_amounts\" -A 25 evals/run.py | head -40; grep -n \"def score_entries\" -A 20 evals/run.py | head -28",
 "description": "Inspect amount and entry scoring"
}
````

### User / tool · 2026-11-02T21:14:27.667Z

**tool result**
````
174:def score_amounts(exp, out):
175-    prod = out.get("amounts") or []
176-    req = [a for a in exp["amounts"] if a.get("required")]
177-    found, misses = 0, []
178-    for g in req:
179-        cents = None if g["value"] is None else round(g["value"] * 100)
180-        ok = any(f"r{g['record_no']}" in [str(r) for r in a.get("record_ids", [])] and a.get("text") == g["raw"]
181-                 and a.get("kind") == g["class"] and a.get("value_cents") == cents for a in prod)
182-        found += ok
183-        if not ok:
184-            misses.append(g["id"])
185-    gold_cents = round(exp["totals"]["explicit_charges_total"] * 100)
186-    charge_sum = sum(a.get("value_cents") or 0 for a in prod if a.get("kind") == "charge")
187-    t = out.get("totals") or {}
188-    shown = (t.get("detected_not_a_total") or {}).get("cents", charge_sum)
189-    return {"found": found, "total": len(req), "misses": misses, "charge_sum_cents": charge_sum, "golden_total_cents": gold_cents,
190-            "total_ok": charge_sum == gold_cents and shown == gold_cents}
191-
192-
193-def tray_flags(out):
194-    """Flags the judge or the code moved to the could-not-verify tray (state rejected; D-053). They are not assertions the product makes, so they
195-    are not scored for precision or recall and are reported apart."""
196-    return [f for f in out.get("flags") or [] if f.get("state") == "rejected" and f.get("type") != "record_warning"]
197-
198-
199-def to_candidates(out):
161:def score_entries(exp, out):
162-    prod = product_entries(out)
163-    found, misses = 0, []
164-    for g in exp["entries"]:
165-        ok, why = entry_found(g, prod)
166-        found += ok
167-        if not ok:
168-            misses.append({"entry": g["id"], "why": why})
169-    return {"found": found, "total": len(exp["entries"]), "misses": misses,
170-            "entry_count": len(prod), "expected_entry_count": exp["expected_entry_count"],
171-            "dedupe_ok": len(prod) <= exp["expected_entry_count"]}
172-
173-
174-def score_amounts(exp, out):
175-    prod = out.get("amounts") or []
176-    req = [a for a in exp["amounts"] if a.get("required")]
177-    found, misses = 0, []
178-    for g in req:
179-        cents = None if g["value"] is None else round(g["value"] * 100)
180-        ok = any(f"r{g['record_no']}" in [str(r) for r in a.get("record_ids", [])] and a.get("text") == g["raw"]
181-                 and a.get("kind") == g["class"] and a.get("value_cents") == cents for a in prod)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:14:35.908Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/lib_sums.py",
 "content": "\"\"\"Sum entries / amounts / must-flags columns of a library report table.\nUsage: python3 -I lib_sums.py <library-report.md>\"\"\"\nimport sys\n\nrows = [l for l in open(sys.argv[1]) if l.startswith(\"| case_lib\")]\nhdr = [l for l in open(sys.argv[1]) if l.startswith(\"| packet\")][0]\ncols = [c.strip() for c in hdr.strip().strip(\"|\").split(\"|\")]\ntot = {}\nfor r in rows:\n    cells = [c.strip() for c in r.strip().strip(\"|\").split(\"|\")]\n    for name in (\"entries\", \"amounts\", \"must flags\"):\n        n, d = cells[cols.index(name)].split(\"/\")\n        a, b = tot.get(name, (0, 0))\n        tot[name] = (a + int(n), b + int(d))\nprint(len(rows), \"packets\")\nfor k, (n, d) in tot.items():\n    print(f\"{k}: {n}/{d} = {n / d:.3f}\")\n"
}
````

### User / tool · 2026-11-02T21:14:36.065Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/lib_sums.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:14:37.869Z

**tool call — Bash**
````
{
 "command": "python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md; python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py evals/reports/library-latest.md",
 "description": "Compute library recall totals"
}
````

### User / tool · 2026-11-02T21:14:38.046Z

**tool result (error)**
````
Exit code 1
15 packets
entries: 93/120 = 0.775
amounts: 40/69 = 0.580
must flags: 34/42 = 0.810
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/lib_sums.py", line 12, in <module>
    n, d = cells[cols.index(name)].split("/")
    ^^^^
ValueError: not enough values to unpack (expected 2, got 1)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:14:40.335Z

**tool call — Bash**
````
{
 "command": "which pandoc; ls \"/Applications/Google Chrome.app/Contents/MacOS/\" 2>/dev/null; cat submission/print.css",
 "description": "Check render tools and print css"
}
````

### User / tool · 2026-11-02T21:14:40.458Z

**tool result**
````
/opt/homebrew/bin/pandoc
Google Chrome
@page{size:Letter;margin:0.4in}
body{font:8.7pt/1.25 -apple-system,Helvetica,Arial,sans-serif;max-width:none;margin:0;color:#111}
header{display:none}
h1{font-size:13pt;margin:0 0 2px}
p{margin:2px 0}li{margin:0.5px 0}
ul,ol{margin:2px 0;padding-left:16px}
table{border-collapse:collapse;width:100%;margin:3px 0;font-size:8.2pt}
td,th{border:1px solid #bbb;padding:1.5px 4px;vertical-align:top;text-align:left}
code{font-size:7.8pt}
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:14:46.005Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/submission && E=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm && pandoc product-note.md -s --css print.css --embed-resources --metadata title=\" \" -o $E/note.html 2>&1 | tail -2; pandoc part2-process.md -s --css print.css --embed-resources --metadata title=\" \" -o $E/part2.html 2>&1 | tail -2; C=\"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\"; \"$C\" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=$E/note.pdf file://$E/note.html 2>/dev/null; \"$C\" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=$E/part2.pdf file://$E/part2.html 2>/dev/null; for f in note part2; do python3 -I -c 'import sys,re;d=open(sys.argv[1],\"rb\").read();print(sys.argv[1].split(\"/\")[-1], len(re.findall(rb\"/Type\\s*/Page[^s]\",d)))' $E/$f.pdf; done",
 "description": "Render both docs to PDF and count pages",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T21:14:48.315Z

**tool result**
````
note.pdf 1
part2.pdf 4
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:14:51.849Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/part2.pdf",
 "pages": "1"
}
````

### User / tool · 2026-11-02T21:14:51.932Z

**tool result**
````
PDF pages extracted: 1 page(s) from /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-185-pm/part2.pdf (224.1KB)
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:14:58.092Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 --grep=\"D-066\" ; git grep -n -i \"compared it with the quote\" HEAD -- app/ | head -5",
 "description": "Check D-066 compare-confirm at HEAD"
}
````

### User / tool · 2026-11-02T21:14:58.299Z

**tool result**
````
b01382f feat(frontend): T-180 guided UI spec and clickable static mockup (D-068)
ee62967 docs(orchestrator): D-066 disputed accept needs a compare confirm; D-067 cut the drafted paragraph from the MVP UI; scope cuts 22-23
HEAD:app/backend/review.py:85:    reason such as OCR or a translation keeps it open). Her edit saved it, but she has not yet said she compared it with the quote, so it has not been decided: it is
HEAD:app/frontend/dom.js:46:  // letter, but she has not yet compared it with the quote). A dismissed item is decided and is never counted as needing review.
HEAD:app/frontend/review.js:266:  // T-136 (paralegal pass 5 F1): the confirmation "I compared it with the quote" is a statement by the paralegal. The a key (and Start review, which lands on this row) must not make it for her:
HEAD:app/frontend/review.js:269:  const COMPARE_PROMPT = "Not recorded yet. Read the quote against your edit. Then click \u201cI compared it with the quote\u201d, or press Enter on it, to say you did.";
HEAD:app/frontend/review.js:473:    const acceptText = toCheck ? "I compared it with the quote" : accepted ? (noted ? "Kept in notes" : st === "edited" ? "Edited" : "Accepted") : noted ? "Keep in notes" : "Accept";
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:15:14.248Z

**tool call — Bash**
````
{
 "command": "head -15 artifacts/review-evidence/GATE-M3-pm/lib_sweep.py",
 "description": "Inspect lib_sweep usage"
}
````

### User / tool · 2026-11-02T21:15:14.338Z

**tool result**
````
"""Sweep all library cases + sample: counts of needs_review, judge-disputed entries that a one-click accept would put in the letter.
Usage: python3 -I lib_sweep.py http://127.0.0.1:7973"""
import json, sys, time, urllib.request, urllib.error

BASE = sys.argv[1]


def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode() if body is not None else None, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:15:17.072Z

**tool call — Bash**
````
{
 "command": "python3 -I artifacts/review-evidence/GATE-M3-pm/lib_sweep.py http://localhost:7860 > artifacts/review-evidence/T-185-pm/lib_sweep-7860.out 2>&1; echo exit=$?; tail -15 artifacts/review-evidence/T-185-pm/lib_sweep-7860.out | cut -c1-300",
 "description": "Sweep disputed accepts on running app",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T21:15:17.259Z

**tool result**
````
exit=1
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/GATE-M3-pm/lib_sweep.py", line 19, in <module>
    ids = ["sample"] + [c["id"] for c in lib["cases"]]
                                         ~~~^^^^^^^^^
KeyError: 'cases'
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:15:20.214Z

**tool call — Bash**
````
{
 "command": "git grep -n -iE \"D-066|disputed\" HEAD -- app/backend | head -8; echo ---; git diff HEAD --stat -- app/backend | tail -2; grep -n -iE \"D-066\" app/backend/*.py | head -5",
 "description": "Check D-066 enforcement in HEAD vs working tree"
}
````

### User / tool · 2026-11-02T21:15:20.380Z

**tool result**
````
---
 app/backend/review.py      | 42 ++++++++++++++++++++++++++++++++++++++++++
 5 files changed, 72 insertions(+), 3 deletions(-)
app/backend/case_extras.py:46:        elif action == "accept" and review.judge_dispute(row):      # D-066: a disputed summary is accepted alone, with her explicit compare
app/backend/review.py:298:    """D-066: the second check's objection to this item, as its ladder verdict (partially | unsupported | disagrees), else None. The verdict on the item's ladder or any of the
app/backend/review.py:310:    """D-066: accepting an item the second check disputed needs the explicit statement that she compared it with the quote (`compared: true`). 422 COMPARE_REQUIRED without it."""
app/backend/review.py:320:    """D-066: her statement is kept in the accept event that carried it (after.compared = {at}), so the audit shows it."""
app/backend/review.py:349:        if action == "accept" and (err := compare_error(item_id, item, compared)):      # D-066; before any write
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:15:26.294Z

**tool call — Bash**
````
{
 "command": "grep -n \"A-101\" memory/ASSUMPTIONS.md | head -2 | cut -c1-300; grep -n -iE \"D-016\" memory/ORCHESTRATOR_DECISIONS.md | head -1 | cut -c1-250; grep -c \"\" submission/NEEDS_CHRIS.md; grep -n -E \"^\\| *[0-9]+ \" submission/NEEDS_CHRIS.md | cut -c1-200",
 "description": "Verify A-101, D-016, NEEDS_CHRIS rows"
}
````

### User / tool · 2026-11-02T21:15:26.424Z

**tool result**
````
15:| A-101 | The paralegal assembles the chronology; the attorney reviews and signs the demand. | Scenario wording ("a paralegal spends hours"). | Med-high | The user and the review UI's audience shift to attorneys. | Discovery Q to the litigation lead (Part 2, area 1). |
24:| D-016 | Post-launch, a test set **may** be built from real work product, but only inside the firm's environment, attorney-approved, with access logged; the prototype and this repo stay synthetic-only. Personas must not treat that as a dealbreake
39
8:| 1 | P1 | T-019 | Real Anthropic API key for the public deployment | Put a real key in `.env` as `ANTHROPIC_API_KEY=<redacted> (local) and as the Space secret `ANTHROPIC_API_KEY` (Hugging Face). Only nee
9:| 2 | P1 | T-022 | Public link: demo-only or live? | Inbox: `demo-only` or `live, cap $N/day`. | Demo-only (cached sample run through the real pipeline code). Live needs an env opt-in (D-008). |
10:| 3 | P2 | T-023 | Live-model eval budget on your claude.ai plan (~25–35 calls per sample run) | Inbox: `ok` or a cap, e.g. `max 300 calls`. | Live runs only for ship-bar measurements (3× sample
18:| 4 | P0 | T-189 | **The one story: a feature or launch you owned that missed the mark.** Yours alone; the team will not write it. | Replace the `[CHRIS: write this yourself ...]` block at the end 
19:| 5 | P1 | T-190 | Byline and public link for the product note and Part 2 | In `submission/product-note.md` line 3 and `submission/part2-process.md` line 3: replace `[CHRIS: full name]` with the na
20:| 6 | P2 | T-190 | Optional one-line real examples in Part 2 (each is marked `[CHRIS: optional ...]`) | Area 1: watching real work without exposing client data. Area 5: how you measured adoption on
21:| 7 | P2 | T-190 | Product note, "Score 5": the 4/5 "I could verify every claim quickly" is a persona reviewer on the previous screen, not a real paralegal | Optional: have a real paralegal (or som
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:15:37.371Z

**tool call — Bash**
````
{
 "command": "git ls-tree --name-only 59e33ca reviews/ | wc -l; git ls-tree --name-only 59e33ca evals/reports/ | grep -cE '/[0-9]{8}T[0-9]{6}Z\\.md$'; ls -d reviews/*/ 2>/dev/null",
 "description": "Count reviews and reports at writer commit"
}
````

### User / tool · 2026-11-02T21:15:37.525Z

**tool result (error)**
````
Exit code 1
     136
27
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:15:41.001Z

**tool call — Bash**
````
{
 "command": "git ls-files reviews | wc -l; git ls-files evals/reports | grep -cE '[0-9]{8}T[0-9]{6}Z\\.md$'; git status --short reviews | head -3; git status --short reviews | wc -l; git check-ignore -v reviews/GATE-M3-product-manager.md evals/reports/20261102T164038Z.md; git ls-files --error-unmatch reviews/GATE-M3-product-manager.md evals/reports/20261102T164038Z.md reviews/GATE-M3-paralegal.md 2>&1 | head",
 "description": "Check tracking of cited evidence files"
}
````

### User / tool · 2026-11-02T21:15:41.236Z

**tool result**
````
     136
33
?? reviews/GATE-M2-claims-adjuster.md
?? reviews/GATE-M2-legal-nurse.md
?? reviews/GATE-M2-paralegal.md
     328
error: pathspec 'reviews/GATE-M3-product-manager.md' did not match any file(s) known to git
error: pathspec 'reviews/GATE-M3-paralegal.md' did not match any file(s) known to git
Did you forget to 'git add'?
evals/reports/20261102T164038Z.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:15:47.183Z

**tool call — Bash**
````
{
 "command": "for f in reviews/T-140-claims-adjuster.md reviews/T-140-claims-adjuster-r2.md reviews/T-140-claims-adjuster-r3.md reviews/T-140-claims-adjuster-r4.md evals/reports/m3-sensors.md reviews/GATE-M3-round1-triage.md memory/SCOPE_CUTS.md memory/ORCHESTRATOR_DECISIONS.md memory/LESSONS.md memory/ASSUMPTIONS.md submission/validation-ladder.svg submission/print.css docs/LLM_VS_CODE.md spec/REQUIREMENTS.md evals/golden/sample.expected.json memory/STATE.md submission/NEEDS_CHRIS.md submission/prompt-log/TOOLS.md evals/reports/library-latest.md; do if git ls-files --error-unmatch $f >/dev/null 2>&1; then d=$(git diff --quiet HEAD -- $f && echo clean || echo modified); echo \"tracked $d $f\"; else echo \"UNTRACKED $f\"; fi; done; git ls-files personas | wc -l; ls submission/prompt-log/",
 "description": "Check tracking status of every cited file"
}
````

### User / tool · 2026-11-02T21:15:47.245Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: dynamic git subcommand is not allowed | command: for f in reviews/T-140-claims-adjuster.md reviews/T-140-claims-adjuster-r2.md reviews/T-140-claims-adjuster-r3.md reviews/T-140-claims-adjuster-r4.md evals/reports/m3-sensors.md reviews/GATE-M3-round1
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:15:51.142Z

**tool call — Bash**
````
{
 "command": "git ls-files --error-unmatch reviews/T-140-claims-adjuster.md reviews/T-140-claims-adjuster-r2.md reviews/T-140-claims-adjuster-r3.md reviews/T-140-claims-adjuster-r4.md evals/reports/m3-sensors.md reviews/GATE-M3-round1-triage.md memory/SCOPE_CUTS.md memory/ORCHESTRATOR_DECISIONS.md memory/LESSONS.md memory/ASSUMPTIONS.md submission/validation-ladder.svg submission/print.css docs/LLM_VS_CODE.md spec/REQUIREMENTS.md evals/golden/sample.expected.json memory/STATE.md submission/NEEDS_CHRIS.md evals/reports/library-latest.md 2>&1 | sed 's/^/  /'; echo; git status --short memory/SCOPE_CUTS.md memory/ORCHESTRATOR_DECISIONS.md memory/LESSONS.md memory/ASSUMPTIONS.md evals/reports/m3-sensors.md submission/ docs/LLM_VS_CODE.md",
 "description": "Check tracking of cited files"
}
````

### User / tool · 2026-11-02T21:15:51.280Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:15:54.606Z

**tool call — Bash**
````
{
 "command": "ls submission/prompt-log/; ls submission/prompt-log/reviews 2>/dev/null | wc -l; ls submission/prompt-log/reviews 2>/dev/null | grep -E \"GATE-M3-product|GATE-M3-paralegal|T-140-claims\" ; git ls-files submission/prompt-log/reviews | grep -cE \"GATE-M3-product|T-140-claims\"",
 "description": "Check whether reviews ship via prompt-log"
}
````

### User / tool · 2026-11-02T21:15:54.735Z

**tool result**
````
CONTRACT.md
README.md
REDACTIONS.md
TOOLS.md
board-activity.jsonl
decisions-and-lessons
reviews
transcripts
     464
GATE-M3-paralegal.md
GATE-M3-product-manager.md
T-140-claims-adjuster-r2.md
T-140-claims-adjuster-r3.md
T-140-claims-adjuster-r4.md
T-140-claims-adjuster.md
5
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:15:56.943Z

**tool call — Bash**
````
{
 "command": "git ls-files submission/prompt-log/reviews | grep -E \"GATE-M3-product|GATE-M3-paralegal|T-140-claims\"; git ls-files submission/prompt-log/reviews | wc -l; git ls-files reviews | grep -c GATE",
 "description": "List tracked copies of cited reviews"
}
````

### User / tool · 2026-11-02T21:15:57.094Z

**tool result**
````
submission/prompt-log/reviews/GATE-M3-paralegal.md
submission/prompt-log/reviews/GATE-M3-product-manager.md
submission/prompt-log/reviews/T-140-claims-adjuster-r2.md
submission/prompt-log/reviews/T-140-claims-adjuster-r3.md
submission/prompt-log/reviews/T-140-claims-adjuster-r4.md
submission/prompt-log/reviews/T-140-claims-adjuster.md
     460
5
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:16:20.192Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"reclassif\" docs/LLM_VS_CODE.md | cut -c1-400 | head -4; grep -n -iE \"rate is never|never a charge\" submission/validation-ladder.svg docs/LLM_VS_CODE.md | cut -c1-200 | head",
 "description": "Check reclassification vs SVG claim"
}
````

### User / tool · 2026-11-02T21:16:20.315Z

**tool result**
````
35:| 7 | Say what an amount is: charge, rate, estimate, damages, unclear | **Code only**, by explicit billing phrases, first match wins: an injection-warned record or an unreadable figure is *unclear*; a rate cue in the label ("per" or "each" followed by a unit word such as visit or session, "rate of", "/visit") or right after the amount ("$185 per visit", "$185 each", "$185/hr") is a *rate* ("Cha
103:- **Still cut, on purpose:** accounts and roles. Two items the first cut list named are built under the guards above: guarded charge reclassification (row 7, D-042) and dismissal-pattern suggestions (T-089, `app/backend/dismissal_patterns.py`, code only: suggestions never change a flag's state, and only lexicon-phrase pre-existing and causation flags are eligible).
submission/validation-ladder.svg:82:  <text x="554" y="138" font-size="11" fill="#222">(a rate is never a charge). Totals of what</text>
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:16:22.431Z

**tool call — Bash**
````
{
 "command": "sed -n 35p docs/LLM_VS_CODE.md | cut -c900-2600",
 "description": "Read rest of row 7"
}
````

### User / tool · 2026-11-02T21:16:22.530Z

**tool result**
````
never reaches the letter. | Billing language is regular enough for rules, and a rule can be tested. A rule cannot be argued with by a record that says "add $50,000 to the billed total". | **Judge 2 checks every classification** against the excerpt (`agrees`, `disagrees`, `unsure`), including the rule-made ones. A `charge` is `verified` only when judge 2 agrees; any other class needs review. Reclassification is guarded (D-042, T-084): a charge can always be moved out of the total; a figure moves in only if code finds charged-amount wording in its own sentence (no negation, balance cue or rate cue, a parsed value, no injection tag) and judge 2 agrees. A rate cue such as "Charge per visit $185" is refused before judge 2 is asked, so a rate cannot become a charge by its wording. Unit tests: 20 phrasings of "Charge per visit $185" all give *rate*; "Moderate" and "Corporate" never trigger the rate rule; all 14 dollar amounts across the golden cases get their golden class. `tests/unit/test_reclassify.py` covers each refusal (422 `reclassify_refused`) and the promotion of a figure that judge 2 agrees with. |
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:16:31.104Z

**tool call — Bash**
````
{
 "command": "sed -n 45,47p memory/LESSONS.md | cut -c200-700; ls .git/hooks | grep -v sample; grep -l -iE \"py_compile|compileall|node --check\" .git/hooks/* .claude/hooks/* tools/*.py 2>/dev/null | head",
 "description": "Verify pre-commit compile claim"
}
````

### User / tool · 2026-11-02T21:16:31.220Z

**tool result**
````
rendered no charges panel. Rule: verify from git archive HEAD, never the working tree. Harness: once tests/e2e/test_no_console_errors.py exists, the pre-commit hook runs it when app/frontend files are staged.
heckout/restore in the shared tree; mutants must run in a git archive copy.

pre-commit
/bin/bash: child setpgid (63482 to 63482): Operation not permitted
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:16:32.629Z

**tool call — Bash**
````
{
 "command": "grep -n -iE \"compile|node|import|check\" .git/hooks/pre-commit | head -15",
 "description": "Read pre-commit hook checks"
}
````

### User / tool · 2026-11-02T21:16:32.748Z

**tool result**
````
3:python3 "$top/tools/check_stale_index.py" || exit 1
4:python3 "$top/tools/check_index_imports.py" || exit 1
5:exec python3 "$top/tools/check_secrets.py" --staged
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:16:34.120Z

**tool call — Bash**
````
{
 "command": "head -20 tools/check_index_imports.py",
 "description": "Inspect index import check tool"
}
````

### User / tool · 2026-11-02T21:16:34.211Z

**tool result**
````
#!/usr/bin/env python3
"""Pre-commit guard: the tree being committed must import on its own (lessons: 225e666, 2db6ad2).

Several workers share one checkout, so a commit can depend on code that is still uncommitted in the working tree
(present.py called conflict_candidates.checks(); generator.py called why.join). This writes the index (honours
GIT_INDEX_FILE) to a temp dir and imports the app there. Exit 1 with the error; 0 otherwise. Skipped when no app/ file
is staged.
"""
from __future__ import annotations
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ("app.backend.api",)
# D-068 (T-181): the app has two front ends. /classic is loaded and exercised by test_no_console_errors.py; / (the guided app) and /classic's first paint by the guided shell smoke.
FRONTEND_SMOKE = ("tests/e2e/test_no_console_errors.py", "tests/e2e/guided/test_shell_smoke.py")
SMOKE = ("tests/unit/test_api_routes.py::test_create_sample_is_code_only_with_gap_flag",
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:16:58.098Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -E \"^T-18[56]\"; sed -n 19p submission/product-note.md | cut -c1-200; grep -n \"5,698\" submission/product-note.md submission/part2-process.md | cut -c1-80; grep -n \"Unit\" evals/reports/m3-sensors.md | head -2 | cut -c1-200",
 "description": "Confirm no existing review files and line refs"
}
````

### User / tool · 2026-11-02T21:16:58.224Z

**tool result**
````
| 5 | Reviewable: paralegal persona rates "I could verify every claim quickly" 4/5 or more; E2E green | 4/5 (`reviews/GATE-M3-paralegal.md`); 412 E2E, 5,698 unit tests pass (`evals/reports/m3-sensors.
submission/product-note.md:19:| 5 | Reviewable: paralegal persona rates "I could
submission/part2-process.md:108:**Before release.** Unit tests (5,698 passed), E
7:| Unit | `E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/unit -q` | **5782 passed, 2 skipped**, 0 failed (434 s), the pytest tail line at b824a6c. The round-2 figure 5698 was taken before later c
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:16:59.903Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"disputed needs|Split records|Code, no model|4 of 5\" submission/validation-ladder.svg | cut -c1-200",
 "description": "Locate SVG line numbers"
}
````

### User / tool · 2026-11-02T21:17:00.041Z

**tool result**
````
58:  <text x="34" y="504" font-size="11.5" fill="#222">A summary the judge disputed needs a named "I compared it with the quote."</text>
77:  <text x="554" y="60" font-size="12" font-weight="700" fill="#111">Code, no model</text>
78:  <text x="554" y="78" font-size="11" fill="#222">Split records. Parse dates (an ambiguous</text>
97:  <text x="554" y="488" font-size="11" fill="#222">every claim quickly" 4 of 5; but 5 of 5</text>
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:17:00.831Z

Now I'll write the T-185 review.

### Assistant · claude-opus-5-5 · 2026-11-02T21:18:02.201Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-185-product-manager.md",
 "content": "# T-185 product note: product-manager-reviewer (Dana Okafor lens)\n\n**Verdict: fail** (2 blockers, 4 majors, 3 minors, 1 nit).\n\nThe note mostly does what a hiring panel wants. It has a five-row ship bar with live numbers and a report path. It puts the golden-vs-library flag gap in bold. It tells the billing rounds and the M3 gate failure plainly. It invents nothing about Chris. Most numbers I checked trace to their source: 242 grounding checks, 0.982/1.000 recall, 40/40, 0 of 10, 20/20, 12/12, 5 of 17 clean held-out, 412 E2E, 34/42 = 0.81, $16,147 vs $8,123.50, and D-040/D-052/D-065..D-068.\n\nTwo things fail it.\n\n1. **It hides the biggest reviewability miss.** Chris used the M3 screen and called it \"VERY hard to use\", which forced a full redesign (D-068). The note still reports ship-bar row 5 as met at 4/5, a score from a persona reviewer on that same screen.\n2. **It describes things that are not built as built.** The guided four-step screen is T-181, still in_progress with AC 0/1. Its files are untracked, and the running app serves the old UI. The D-066 compare-confirm exists only in the uncommitted working tree.\n\nThe majors:\n- The unit-test count (5,698) is one the cited file says did not reproduce.\n- Three stretch items shipped against \"pick at most one\", and the note gives no reason.\n- The cited review paths are not in git.\n- Library entry and amount recall (0.775 and 0.580 on the same library run) go unmentioned while the note implies only flags fail to generalize.\n\nPage count: 1 page (pandoc + headless Chrome with submission/print.css, 8.7pt). Length is within the limit.\n\n```json\n{\"card\": \"T-185\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"submission/product-note.md at commit 59e33ca (working tree identical for this file); cited evidence: evals/reports/20261102T164038Z.md, evals/reports/m3-sensors.md, evals/reports/latest.json, reviews/GATE-M3-*.md, reviews/T-140-claims-adjuster*.md, memory/SCOPE_CUTS.md, memory/ORCHESTRATOR_DECISIONS.md, docs/LLM_VS_CODE.md; app at http://localhost:7860 (demo mode, fixture backend); sample case\",\n \"exercised\": [\n  \"Read personas/product-manager.md, docs/CONTRACT.md M5 (318-328), 8.2 ship bar, 11 DoD, Appendix A (493-596), Appendix B (598-607)\",\n  \"Read submission/product-note.md twice; rendered it with pandoc + headless Chrome using submission/print.css: 1 page (artifacts/review-evidence/T-185-pm/note.pdf)\",\n  \"Spot-checked 20+ numbers/claims against evals/reports/20261102T164038Z.md (grounding 1.000/242, entry 0.982, amount 1.000, flags 1.000 x4, 40/40, controls 0 of 10, J3 20/20, J4 12/12, 0 false agree, clean held-out 5 of 17, case_06 E3 miss, gap_28/73 assertions)\",\n  \".venv/bin/python -m evals.run --check-fresh -> exit=0; git log 312efe6..HEAD -- app/llm/prompts app/llm/lexicon.yaml -> empty (live run still valid for prompts)\",\n  \"Compared the unit/E2E counts with evals/reports/m3-sensors.md:7-8 (5782 unit, 412 E2E)\",\n  \"grep of D-001, D-007, D-022, D-031, D-034, D-040, D-042, D-047, D-052..D-054, D-059, D-062..D-068 in memory/ORCHESTRATOR_DECISIONS.md\",\n  \"grep -rn '10,906' reviews/ memory/ -> only GATE-M2-paralegal.md, GATE-M2-r2-paralegal.md, GATE-M2-round1-triage.md; not in T-140-claims-adjuster*\",\n  \"python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md -> entries 93/120 = 0.775, amounts 40/69 = 0.580, must flags 34/42 = 0.810\",\n  \"python3 tools/board.py show T-181/T-179/T-177 and board.py list --status in_progress: T-181 (guided UI) in_progress AC 0/1; T-179 (D-066) in_progress\",\n  \"git ls-files --error-unmatch app/frontend/guided/core.js -> not known to git; git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty; working tree app/backend/review.py:298-349 has D-066 (uncommitted)\",\n  \"curl http://localhost:7860/ -> old UI (index.html with stepper.css/sidebyside.css); /api/health -> demo_mode true, backend fixture\",\n  \"python3 -I artifacts/review-evidence/GATE-M3-pm/journey.py http://localhost:7860 sample -> artifacts/review-evidence/T-185-pm/journey-sample-7860.out: 4 flag types present, gap 73 flagged, $185 under AMOUNTS NOT TOTALED, total $8,390.00, export 422 before any accept, 200 after\",\n  \"curl /api/calibration -> calibrated confidence served; app/frontend/suggestions.js:119-120 renders it (confidence-indicator stretch item)\",\n  \"git ls-files --error-unmatch on every cited path: reviews/GATE-M3-product-manager.md, reviews/GATE-M3-paralegal.md, reviews/T-140-claims-adjuster*.md untracked; tracked copies under submission/prompt-log/reviews/\",\n  \"Spot-checked docs/LLM_VS_CODE.md rows 1 (split) and 7 (amount class) against the note's LLM/code paragraph\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"accuracy\": 2, \"no_invented_chris_facts\": 5, \"required_contents\": 4, \"honesty_of_misses\": 2, \"voice\": 4, \"length\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"The UI redesign after Chris's feedback is hidden, and ship-bar row 5 still reports reviewability as met\",\n   \"evidence\": \"memory/ORCHESTRATOR_DECISIONS.md:76 D-068: 'Guided UI redesign (Chris, 2026-11-02: \\\"VERY hard to use… so simple someone's grandma can use it\\\")' with the reason 'The user's verdict on the current UI'. product-note.md:19 row 5 Result: '4/5 (reviews/GATE-M3-paralegal.md)'. product-note.md:23 says only 'Score 5 is a persona reviewer on the previous screen, not a real paralegal; not re-scored on the guided screen.' grep -n -iE 'hard to use|redesign|grandma|rebuilt' submission/product-note.md -> no match; D-068 appears only at :7 as the label of the new screen.\",\n   \"why_it_matters\": \"This is the clearest AI-judgment lesson in the build. An AI persona passed the screen at 4/5, and the one human who used it said it was very hard to use. The note reports the proxy as a pass and never says the human verdict contradicted it. The panel grades 'define good enough and test against it'. Reporting a met bar on a screen the user rejected is hiding a known failure, a red flag in the dossier.\",\n   \"fix\": \"Add a 'What testing found' bullet in Chris's voice, for example: 'Reviewability passed on paper and failed in use. A persona reviewer scored the M3 screen 4/5 on \\\"I could verify every claim quickly\\\". When I used it myself it was very hard to use (D-068), so we rebuilt it as a four-step guide. An AI reviewer is not a substitute for a person at the desk.' Change row 5 Result to 'Not met on the shipped screen: persona 4/5 on the old screen, which I rejected in use; guided screen not yet scored', or give a re-score on the guided screen.\",\n   \"acceptance_test\": \"grep -n -iE 'hard to use|rebuilt|redesign' submission/product-note.md returns a line in 'What testing found'; row 5's Result no longer reads as met without that qualification.\"},\n  {\"severity\": \"blocker\", \"title\": \"The note describes the guided four-step screen and the D-066 disputed-accept confirm as built; neither is at HEAD\",\n   \"evidence\": \"product-note.md:7 'What I built. ... A guided four-step screen: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter (D-068). Review is one item at a time: ... two big answers.' board.py list --status in_progress: 'T-181 ... in_progress P0 AC 0/1 Build the guided UI (D-068)'. git ls-files --error-unmatch app/frontend/guided/core.js -> 'did not match any file(s) known to git'. curl http://localhost:7860/ serves the old index.html (stepper.css, sidebyside.css). product-note.md:32 'a disputed one needs a named confirm (D-066)'. git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty (D-066 code exists only uncommitted in app/backend/review.py:298-349; T-179 in_progress). The writer's own handoff says 'guided UI (T-181) is described as built'.\",\n   \"why_it_matters\": \"The panel will open the prototype link and see a different product from the one the note describes. A PM note that claims an unbuilt UI and an unbuilt safety control misstates what was built. That is an invented fact under D.2, and it undercuts every other number in the note.\",\n   \"fix\": \"Describe what HEAD ships today. Or hold the note until T-181 and T-179 are done and committed, then re-verify each sentence against the running app. Until then, mark both sentences [PENDING T-181] and [PENDING T-179] so nothing reads as shipped. Use present tense only for code at the commit the submission is tagged at.\",\n   \"acceptance_test\": \"At the submission commit: board.py show T-181 and T-179 show done; git ls-files app/frontend/guided lists the files; GET / serves the guided shell; accepting a judge-disputed item without compared:true returns 422 COMPARE_REQUIRED. Otherwise neither sentence appears in present tense.\"},\n  {\"severity\": \"major\", \"title\": \"The unit-test count 5,698 is the figure the cited file says did not reproduce\",\n   \"evidence\": \"product-note.md:19 '412 E2E, 5,698 unit tests pass (evals/reports/m3-sensors.md)'. evals/reports/m3-sensors.md:7: '5782 passed, 2 skipped ... The round-2 figure 5698 was taken before later commits added tests and did not reproduce ... a count is valid only for the commit named'.\",\n   \"why_it_matters\": \"A number that contradicts its own citation is the first thing a careful panelist checks. It costs trust in every other number in the table.\",\n   \"fix\": \"Use the count and commit the file states ('5,782 unit at b824a6c'), or re-run at the submission commit and cite that.\",\n   \"acceptance_test\": \"Every test count in product-note.md equals a count in the cited sensors file for the commit named next to it.\"},\n  {\"severity\": \"major\", \"title\": \"Stretch: three items shipped against 'pick at most one', the note names two, and gives no reason for going beyond the brief or for reinstating cuts\",\n   \"evidence\": \"Appendix A: 'Stretch (pick at most one, only if time remains): PDF upload, a confidence indicator, a side-by-side source viewer, or a draft paragraph'. product-note.md:9 'The brief allows one stretch; I picked the source viewer and also shipped PDF text-layer upload.' Calibrated confidence also ships (D-042 'calibrated confidence (shown as measured precision per state)'; GET /api/calibration returns it; app/frontend/suggestions.js:119-120 renders 'In testing on N synthetic cases, X of Y verified items matched the record'). :9 'Not cut: I reinstated cuts twice (D-031, D-042)' gives no why.\",\n   \"why_it_matters\": \"'Cut scope on purpose' is the first row of 'What we evaluate'. Going past an explicit limit is defensible only with a stated reason. Undercounting what shipped and giving no reason reads as drift, not as a decision.\",\n   \"fix\": \"Name all three (source viewer, PDF text layer, calibrated confidence). Add one sentence on why the brief's limit was exceeded and why cuts were reinstated, in Chris's words (see questions_for_chris), plus what that cost.\",\n   \"acceptance_test\": \"The Cut paragraph lists every shipped Appendix A stretch item and gives one reason sentence for exceeding 'at most one' and for D-031/D-042.\"},\n  {\"severity\": \"major\", \"title\": \"Cited evidence paths are not in the repo the panel will open\",\n   \"evidence\": \"git ls-files --error-unmatch reviews/GATE-M3-product-manager.md reviews/GATE-M3-paralegal.md reviews/T-140-claims-adjuster.md reviews/T-140-claims-adjuster-r2.md reviews/T-140-claims-adjuster-r3.md reviews/T-140-claims-adjuster-r4.md -> \\\"error: pathspec ... did not match any file(s) known to git\\\" for each. The tracked copies are submission/prompt-log/reviews/GATE-M3-product-manager.md etc. product-note.md:19, :23, :24 cite the reviews/ paths.\",\n   \"why_it_matters\": \"Appendix A: 'Make sure we can open every link'. The 0.81 library recall, the 4/5 score and the billing-round claims are the note's honesty evidence. As cited, none of them opens in the repo.\",\n   \"fix\": \"Either cite submission/prompt-log/reviews/... or have the orchestrator commit reviews/ before submission. Then click every path from a fresh clone.\",\n   \"acceptance_test\": \"From a fresh clone of the submission commit, every path in product-note.md exists (scripted: extract backticked paths, test -e each).\"},\n  {\"severity\": \"major\", \"title\": \"Generalization is reported only for flags; the same library run shows entry recall 0.775 and amount recall 0.580\",\n   \"evidence\": \"product-note.md:16 row 2 'entries 0.982, amounts 1.000 [E]' (golden only); :23 'The 1.000 flag numbers do not generalize'. python3 -I artifacts/review-evidence/T-185-pm/lib_sums.py artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md -> 'entries: 93/120 = 0.775', 'amounts: 40/69 = 0.580', 'must flags: 34/42 = 0.810'. The committed evals/reports/library-latest.md is from a74b727 (stale; the writer's handoff says so).\",\n   \"why_it_matters\": \"Saying the flag numbers do not generalize implies the recall numbers do. The same matchers on the same 15 packets say otherwise. Some of the gap may be expected-file drift after D-052/D-059 (exact class match in evals/run.py:180), but the note neither reports nor explains it.\",\n   \"fix\": \"qa regenerates library-latest.md at the submission commit. The note's row 2 then gives golden and library side by side, with one clause on what the misses are (real misses or expected files that predate the billing redesign).\",\n   \"acceptance_test\": \"evals/reports/library-latest.md source commit equals the submission commit; product-note.md row 2 cites its entry and amount numbers next to the golden ones.\"},\n  {\"severity\": \"minor\", \"title\": \"The $10,906 vs $6,000 billing example is attributed to the wrong reviews\",\n   \"evidence\": \"product-note.md:24 'A claims-adjuster reviewer outworded every word-list rule: one library letter said $10,906 against a true $6,000 ... (reviews/T-140-claims-adjuster*.md)'. grep -rn '10,906' reviews/T-140-claims-adjuster*.md -> nothing; the source is reviews/GATE-M2-paralegal.md:30 and reviews/GATE-M2-round1-triage.md:9 (paralegal persona). $16,147 vs $8,123.50 does trace to the T-140 adjuster reviews.\",\n   \"why_it_matters\": \"The brief requires each claim to trace to its cited file. This one does not.\",\n   \"fix\": \"Attribute the $10,906 case to the paralegal reviewer at GATE-M2 (cite its path), or drop it.\",\n   \"acceptance_test\": \"Each dollar figure on line 24 is found by grep in the file cited beside it.\"},\n  {\"severity\": \"minor\", \"title\": \"LLM/code paragraph says code does record splitting; the build has an LLM split fallback\",\n   \"evidence\": \"product-note.md:38 'Code does anything with one right answer: record splitting, ...' and the model list omits splitting. docs/LLM_VS_CODE.md:29 row 1: 'Only when the code split finds a single record that is unsplit ... may a model be asked ... it returns character offsets only'; D-031 'LLM split fallback (flagged LLM_SPLIT)'; app/llm/prompts/split_v1.md is in the live report's hash list.\",\n   \"why_it_matters\": \"The panel grades where the line was drawn. The note's summary should match LLM_VS_CODE.md, and here the honest version is the stronger one: the model only points at offsets, code cuts and validates.\",\n   \"fix\": \"Add to 'The model reads': 'where to cut an unsplittable paste (offsets only; code validates and flags it LLM_SPLIT)'.\",\n   \"acceptance_test\": \"The note's LLM list matches every LLM row in docs/LLM_VS_CODE.md.\"},\n  {\"severity\": \"minor\", \"title\": \"Post-launch metrics name no data source\",\n   \"evidence\": \"product-note.md:42-44: #1 'against her own last three by hand' (no timed baseline method); #2 'letter lines an attorney corrects or an adjuster challenges, per 100' (no capture mechanism); #3 no source named (it is the audit log).\",\n   \"why_it_matters\": \"A metric that cannot be computed cannot inform a decision. Each metric's decision is stated well; its source is not.\",\n   \"fix\": \"One clause each: #1 timestamps from case-created to letter-copied events vs a stopwatch baseline taken in week 2; #2 attorney edit log plus adjuster letters tagged by the paralegal; #3 audit log accept events with before/after and time on item.\",\n   \"acceptance_test\": \"Each of the three metrics names its event or log source.\"},\n  {\"severity\": \"nit\", \"title\": \"Internal decision IDs crowd a panel-facing page; 'Score 5' is unclear\",\n   \"evidence\": \"product-note.md:31-36 failure table cites D-034, D-047, D-022, D-054, D-066, D-053, D-007 in five rows; :23 'Score 5 is a persona reviewer'.\",\n   \"why_it_matters\": \"Appendix B voice: concise and plain. The panel cannot decode D-numbers without opening the log.\",\n   \"fix\": \"Keep one or two IDs where they prove a decision; write 'ship-bar row 5' for 'Score 5'.\",\n   \"acceptance_test\": \"At most three D-IDs in the failure table; no 'Score 5'.\"}\n ],\n \"whats_right\": [\n  \"The ship bar has five numeric criteria with live results and a report path, and the golden-vs-library flag gap is in bold rather than hidden.\",\n  \"The billing rounds and the M3 gate failure (prepared answers labeled as AI, one-click accept of disputed items) are told plainly, with numbers.\",\n  \"No invented facts about Chris: the byline and link are [CHRIS: ...] placeholders and tracked in NEEDS_CHRIS #5.\"\n ],\n \"questions_for_chris\": [\n  \"May the note quote your D-068 reaction ('VERY hard to use') in your own voice as the reviewability miss, or do you want it paraphrased?\",\n  \"In one line, why did you reinstate cuts (D-031, D-042) and ship three stretch items when the brief says 'at most one'? The note needs your reason, not ours.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T21:18:02.379Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-185-product-manager.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:18:46.706Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-186-product-manager.md",
 "content": "# T-186 Part 2 process doc: product-manager-reviewer (Dana Okafor lens)\n\n**Verdict: fail** (2 blockers, 3 majors, 2 minors).\n\nAll eight areas are present, and most are specific to this build:\n\n- **Area 1:** three plus three discovery questions, specific enough to ask tomorrow.\n- **Area 2:** reasons for doing this first, plus four concrete pieces of evidence that would change the decision.\n- **Area 3:** three AI acceptance criteria, one of them a \"must never\", each with its checker.\n- **Area 4:** a test set built from real work product, a held-out half, and regression discipline that works (`--check-fresh` exit 0).\n- **Area 5:** four measures with expand and kill thresholds, labeled as proposals.\n- **Area 7:** a real message and agenda.\n- **Area 8:** supervision examples taken from LESSONS.\n\nThe miss story is a correctly marked [CHRIS: ...] block, tracked in NEEDS_CHRIS #4 (T-189). The doc renders to 4 pages.\n\nTwo things fail it:\n\n1. **It hides the UI redesign.** Chris rejected the M3 screen as \"VERY hard to use\" (D-068). The quality-bar table and the SVG still present reviewability as 4/5 met, and the area 7 answer on honest feedback skips the build's best example of it.\n2. **The SVG claims an unbuilt control.** It presents the D-066 disputed-accept confirm as current behavior, but it is not at HEAD.\n\nThe majors:\n\n- The unit-test count (5,698) is one the cited file says did not reproduce.\n- Area 6 never says what engineering's role in product decisions is.\n- The cited paths and counts (`reviews/GATE-M3-product-manager.md`, \"460 review files\", \"74 dated reports\") do not match what is in git.\n\n```json\n{\"card\": \"T-186\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"submission/part2-process.md and submission/validation-ladder.svg at commit 59e33ca; cited evidence: evals/reports/20261102T164038Z.md, evals/reports/m3-sensors.md, reviews/GATE-M3-*.md, memory/{ORCHESTRATOR_DECISIONS,LESSONS,SCOPE_CUTS,ASSUMPTIONS}.md, spec/REQUIREMENTS.md, docs/LLM_VS_CODE.md; app at http://localhost:7860 (demo mode); sample case\",\n \"exercised\": [\n  \"Read personas/product-manager.md; docs/CONTRACT.md M5 (318-328), Appendix A Part 2 eight areas + One story + Format (565-586), Appendix B (598-607)\",\n  \"Read submission/part2-process.md twice and marked each of the eight areas specific/generic/missing; read submission/validation-ladder.svg source\",\n  \"Rendered with pandoc + headless Chrome (submission/print.css): artifacts/review-evidence/T-185-pm/part2.pdf = 4 pages; viewed page 1 (SVG renders with both columns and the measured box)\",\n  \"Spot-checked counts: memory/ORCHESTRATOR_DECISIONS.md 68 unique D-IDs (D-001..D-068); grep -c '^- 20' memory/LESSONS.md = 44; grep -c '^| debt' memory/SCOPE_CUTS.md = 61; ls personas/*.md = 13; spec/REQUIREMENTS.md 62 unique R-IDs; R-TL-2 (:49), R-TL-10 (:57), R-CO-3 (:137) exist; A-101..A-109 in ASSUMPTIONS\",\n  \"Checked the area 3/4 numbers against evals/reports/20261102T164038Z.md (grounding 1.000/242, 0.982/1.000, 40/40, J3 20/20, J4 12/12, 0 false agree, must_not 0)\",\n  \"Checked area 8 examples against memory/LESSONS.md:43,45 (12/12 from uncommitted tree; HEAD broke twice), .git/hooks/pre-commit -> tools/check_index_imports.py, reviews/GATE-M3-chaos-tester.md:116 (run stuck after restart), reviews/GATE-M3-round1-triage.md (M3 failed, 2 blockers), board/milestones.md (M0-M2 pass)\",\n  \".venv/bin/python -m evals.run --check-fresh -> exit=0 (the regression claim in area 4 holds)\",\n  \"git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty; T-179 in_progress (board.py show)\",\n  \"git ls-tree --name-only 59e33ca reviews/ | wc -l -> 136; git ls-files submission/prompt-log/reviews | wc -l -> 460; git ls-files evals/reports | grep -cE '[0-9]{8}T[0-9]{6}Z.md$' -> 33; git ls-files --error-unmatch reviews/GATE-M3-product-manager.md -> not known to git\",\n  \"python3 -I artifacts/review-evidence/GATE-M3-pm/journey.py http://localhost:7860 sample (four flag types, 73-day gap, $185 not totaled, export only after accepts)\",\n  \"Checked submission/NEEDS_CHRIS.md rows 4-7 against T-189/T-190 (both needs_chris)\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"accuracy\": 3, \"no_invented_chris_facts\": 5, \"eight_areas_covered\": 4, \"ai_acceptance_criteria\": 5, \"honesty_of_misses\": 2, \"voice\": 4, \"length\": 5, \"visual\": 4},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"The UI redesign after Chris's feedback is missing; the quality-bar table and the SVG present reviewability as met\",\n   \"evidence\": \"memory/ORCHESTRATOR_DECISIONS.md:76 D-068: 'Guided UI redesign (Chris, 2026-11-02: \\\"VERY hard to use… so simple someone's grandma can use it\\\")'. part2-process.md:56 'Reviewable | ... at least 4/5 | 4/5 (persona reviewer)'. validation-ladder.svg:97 'every claim quickly\\\" 4 of 5'. grep -n -iE 'hard to use|redesign|grandma|D-068|guided' submission/part2-process.md -> no match. Area 7 (:87) answers 'How do you get honest, usable feedback' with no build example. The miss-story hooks (:124) list library recall, evidence checks and demo labels, not this.\",\n   \"why_it_matters\": \"Part 2's quality bar is graded on 'what score means ship'. This build's own record says the persona score passed a screen the human rejected. Leaving that out overstates how well the bar worked, which is a dossier red flag (hides a known failure). It also wastes the most persuasive answer the doc could give to areas 4 and 7: AI reviewers are necessary but not enough, so a person at the desk comes before the ship call.\",\n   \"fix\": \"Area 4: add a line under the table: 'Reviewability passed on a persona score and failed in use. I found the M3 screen very hard to use and we rebuilt it (D-068). The ship call now needs a real paralegal session, not a persona score.' Change the table and SVG Result to 'persona 4/5 on the old screen; rejected in use; guided screen not yet scored'. Area 7: use it as the example of honest feedback. Optionally add it to the miss-story hooks.\",\n   \"acceptance_test\": \"grep -n -iE 'hard to use|rebuilt|D-068' submission/part2-process.md returns a line in area 4 or 7; the reviewability Result in the table and SVG no longer reads as met without qualification.\"},\n  {\"severity\": \"blocker\", \"title\": \"The SVG presents the D-066 compare-confirm as current product behavior; it is not at HEAD\",\n   \"evidence\": \"validation-ladder.svg:58 'A summary the judge disputed needs a named \\\"I compared it with the quote.\\\"' (inside 'Rung 3: the paralegal decides'). git grep -n -iE 'D-066|disputed' HEAD -- app/backend -> empty; the enforcement is only in uncommitted app/backend/review.py:298-349; board.py show T-179 -> status in_progress. GATE-M3-product-manager.md:46 measured 5 of 5 disputed entries accepted with one click.\",\n   \"why_it_matters\": \"The diagram is the visual the brief requires, and it claims a safety control on the path to the letter that the shipped code lacks. Overstating a guardrail in a hiring doc is an invented fact about the product (D.2).\",\n   \"fix\": \"Re-verify once T-179 is done and committed. Until then, word rung 3 as 'Decided (D-066), in progress: a disputed summary will need a named confirm'.\",\n   \"acceptance_test\": \"At the submission commit, accepting a judge-disputed item without compared:true returns 422 COMPARE_REQUIRED; otherwise the SVG line is in future tense.\"},\n  {\"severity\": \"major\", \"title\": \"The unit-test count 5,698 is the figure the cited file says did not reproduce\",\n   \"evidence\": \"part2-process.md:108 'Unit tests (5,698 passed), E2E (412 passed, evals/reports/m3-sensors.md)'. evals/reports/m3-sensors.md:7: '5782 passed, 2 skipped ... The round-2 figure 5698 was taken before later commits added tests and did not reproduce'.\",\n   \"why_it_matters\": \"Area 8 argues 'I check evidence, not claims'. Citing a number its own source disowns undercuts exactly that point.\",\n   \"fix\": \"Cite '5,782 at b824a6c', or re-run at the submission commit and cite that.\",\n   \"acceptance_test\": \"Each test count in part2-process.md equals the count in the cited file for the commit named.\"},\n  {\"severity\": \"major\", \"title\": \"Area 6 never states engineering's role in product decisions\",\n   \"evidence\": \"Appendix A area 6: 'How are product decisions made among the founders, engineering and you?' part2-process.md:77-79: the table has three columns, 'I decide alone', 'I decide with the litigation lead' and 'A founder decides'. Engineering does not appear in :75-83.\",\n   \"why_it_matters\": \"There is no product org at Zlayt, so who owns build-vs-buy, estimates, model and stack choices, and the LLM/code line is exactly what the founders asked. One of three named parties is missing.\",\n   \"fix\": \"Add an engineering column or two lines. For example: engineering decides how (stack, model routing inside the budget, test design) and has a veto on 'not safe to ship'; I decide what and when; the LLM/code line is drawn together and written down in an ADR.\",\n   \"acceptance_test\": \"Area 6 names at least two decisions engineering owns and how a disagreement with engineering is settled.\"},\n  {\"severity\": \"major\", \"title\": \"Cited evidence paths and artifact counts do not match what is in the repo\",\n   \"evidence\": \"part2-process.md:44 cites reviews/GATE-M3-product-manager.md -> git ls-files --error-unmatch: 'did not match any file(s) known to git' (the tracked copy is submission/prompt-log/reviews/GATE-M3-product-manager.md). :3 'reviews/ (460 review files)': git ls-tree 59e33ca reviews/ -> 136 files; the 460 are under submission/prompt-log/reviews/. :3 'evals/reports/ (74 dated reports)': 33 tracked.\",\n   \"why_it_matters\": \"The doc's argument is 'point at the artifacts as proof' (Appendix B). A panelist who opens reviews/ and finds 136 files, or a 404 on the gate review, reads it as over-claiming.\",\n   \"fix\": \"Point at the paths that exist in the submitted repo (submission/prompt-log/reviews/), or have the orchestrator commit reviews/ and evals/reports/ first, then recount at the submission commit.\",\n   \"acceptance_test\": \"From a fresh clone of the submission commit, every path in part2-process.md exists, and the counts on line 3 equal ls | wc -l of the named directory.\"},\n  {\"severity\": \"minor\", \"title\": \"The SVG says record splitting is code only; the build has an LLM split fallback\",\n   \"evidence\": \"validation-ladder.svg:77-78 'Code, no model' / 'Split records.' docs/LLM_VS_CODE.md:29 row 1: 'Only when the code split finds a single record that is unsplit ... may a model be asked ... character offsets only'; D-031 'LLM split fallback (flagged LLM_SPLIT)'.\",\n   \"why_it_matters\": \"The visual should match the graded LLM/code table, and the real design is the more impressive one.\",\n   \"fix\": \"Change to 'Split records (a model may only point at cut offsets for an unsplittable paste; code validates)'.\",\n   \"acceptance_test\": \"Every 'Code, no model' item in the SVG is code-only in docs/LLM_VS_CODE.md.\"},\n  {\"severity\": \"minor\", \"title\": \"A claim about how PI firms work is stated as fact; the assumption range is off by one\",\n   \"evidence\": \"part2-process.md:23 '**Every matter needs one,** so volume is high.' (no assumption marker, while the line above marks 'assumption, to confirm'). :13 'A-101 to A-108', but memory/ASSUMPTIONS.md also has A-109.\",\n   \"why_it_matters\": \"Appendix A ground rule: 'If you assume something about how personal injury firms work, state the assumption.'\",\n   \"fix\": \"'Every matter with treatment needs one (assumption: confirm the share of matters that reach a demand letter)'; 'A-101 to A-109'.\",\n   \"acceptance_test\": \"Each PI-practice claim in area 2 carries an assumption marker or an A-ID.\"}\n ],\n \"whats_right\": [\n  \"Discovery questions (3 + 3) and the paralegal message and agenda are specific enough to use tomorrow, and they ask for artifacts and errors, not opinions.\",\n  \"Three AI acceptance criteria, including the must-never AI-3 on hedges, merged dates and the $185 rate, each with a named checker and a live result.\",\n  \"Metrics table defines adoption, time saved, quality and retention with expand and kill thresholds, honestly labeled as starting proposals, and regression discipline is real (--check-fresh exit 0).\"\n ],\n \"questions_for_chris\": [\n  \"For area 6: what decision rights do you want to give engineering (for example a 'not safe to ship' veto, model choice inside a budget)? The doc should state your stance, not ours.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T21:18:46.885Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-186-product-manager.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:18:48.291Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-185-product-manager.md; python3 tools/board.py validate reviews/T-186-product-manager.md",
 "description": "Validate both review files"
}
````

### User / tool · 2026-11-02T21:18:48.510Z

**tool result**
````
ok (1 file(s))
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:18:49.438Z

Saving one memory note on recurring submission-doc patterns.

### Assistant · claude-opus-5-5 · 2026-11-02T21:18:58.382Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_submission_doc_patterns.md",
 "content": "---\nname: submission-doc-patterns\ndescription: M5 product-note / Part 2 review checks that found real defects (T-185/T-186, 2026-11-02) - built-claims ahead of HEAD, proxy-vs-human reviewability, disowned counts, untracked cited paths\nmetadata:\n  type: feedback\n---\n\nRun these checks on any submission doc (product note, Part 2, SVG, checklist). Each one found a real defect at T-185/T-186 r1 (commit 59e33ca). Both cards failed.\n\n1. **Built-claims vs HEAD.** For every present-tense \"I built\" sentence, check the card's status with `board.py show` and check HEAD with `git grep ... HEAD -- app/`. Writers describe in-progress cards as shipped. Examples: the guided UI (T-181) and the D-066 confirm (T-179) were only in the uncommitted working tree.\n2. **Proxy vs human.** A persona score (verify_quickly 4/5) passed the M3 screen, but Chris rejected that screen as \"VERY hard to use\" (D-068). The docs reported the persona score as met and left out the human verdict. Grep ORCHESTRATOR_DECISIONS for \"Chris\" reactions and check that each one is told.\n3. **Counts vs cited file.** Sensor files can disown older counts. m3-sensors.md said 5698 \"did not reproduce\", yet both docs cited 5,698.\n4. **Cited paths exist in git.** Most of reviews/ is untracked. The tracked copies are in submission/prompt-log/reviews/. Run `git ls-files --error-unmatch` on every backticked path.\n5. **Library vs golden on all metrics, not just flags.** At d0b04bc the library scored entries 0.775, amounts 0.580 and flags 0.81. Script: artifacts/review-evidence/T-185-pm/lib_sums.py.\n6. **Stretch count.** Count stretch items against the live UI. Calibrated confidence (GET /api/calibration, suggestions.js) is the Appendix A \"confidence indicator\", so the build ships 3 stretch items, not 2.\n\n**Why:** the hiring panel grades over-claiming and AI judgment. All six of these get past a reading of the doc alone.\n\n**How to apply:** render the docs with pandoc + headless Chrome using submission/print.css to get the page count. The demo app at :7860 serves the sample only; library cases need local mode. Related: [[gate-review-patterns]], [[needs-chris-drift]].\n"
}
````

### User / tool · 2026-11-02T21:18:58.509Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_submission_doc_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:18:59.792Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md",
 "old_string": "- [T-017/T-018 review history]",
 "new_string": "- [Submission doc patterns](feedback_submission_doc_patterns.md) — M5 note/Part 2: built-claims ahead of HEAD, persona-vs-human reviewability, disowned counts, untracked paths\n- [T-017/T-018 review history]"
}
````

### User / tool · 2026-11-02T21:18:59.901Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T21:19:03.907Z

T-185 (product note) fails with 2 blockers: it hides Chris's "VERY hard to use" verdict that forced the redesign (D-068) while still reporting the 4/5 persona score as meeting the reviewability bar, and it describes the guided screen (T-181) and the disputed-summary confirm (T-179) as built though neither is committed. The majors are a 5,698 test count its cited file says didn't reproduce, three stretch items with no reason given, cited reviews not in git, and unreported library recall (entries 0.775, amounts 0.580); details in /Users/arsis/zlayt-pm-project/reviews/T-185-product-manager.md.
T-186 (Part 2) fails with 2 blockers: the same redesign omission, and validation-ladder.svg presents the disputed-summary confirm as current behavior. The majors are the 5,698 count, no engineering role in area 6, and paths and counts that don't match git; details in /Users/arsis/zlayt-pm-project/reviews/T-186-product-manager.md (both files pass `board.py validate`).
