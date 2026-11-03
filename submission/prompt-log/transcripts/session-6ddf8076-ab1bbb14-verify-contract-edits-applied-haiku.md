# Subagent: Verify contract edits applied (haiku) (Verify contract edits applied (haiku))

Source: `agent-ab1bbb1454c60b995.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:23:04.147Z

Working directory: /Users/arsis/zlayt-pm-project. Mechanical check that the T-018 contract-review findings were applied. For each blocker/major finding in reviews/CONTRACT-M2M3-{product-manager,paralegal,staff-engineer}.md and reviews/T-017-product-manager.md, confirm via `python3 tools/board.py show T-0xx` (grep the AC lines) or docs/M2M3_COVERAGE.md / .claude/agents/paralegal-reviewer.md that the requested AC edit, dependency, new card (T-048) or doc section exists. Quote the evidence line for each. Write reviews/T-018-product-manager.md (card T-018) and reviews/T-017-product-manager-r2.md (card T-017), D.2 JSON each, verdict pass only if every finding is applied (list any not applied as majors). Model = what you run as. Reply ≤ 4 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:06.093Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/product-manager.md"
}
````

### User / tool · 2026-11-02T01:23:06.100Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:06.599Z

**tool call — Bash**
````
{
 "command": "ls -la /Users/arsis/zlayt-pm-project/reviews/ /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/ && cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md",
 "description": "List reviews and memory directories and read memory index"
}
````

### User / tool · 2026-11-02T01:23:06.687Z

**tool result**
````
/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/:
total 64
drwxr-xr-x@ 10 arsis  staff   320 Nov  1 19:22 .
drwxr-xr-x@ 12 arsis  staff   384 Nov  1 19:03 ..
-rw-r--r--@  1 arsis  staff  1076 Nov  1 19:22 MEMORY.md
-rw-r--r--@  1 arsis  staff  1844 Nov  1 18:42 feedback_calibration_vs_redflags.md
-rw-r--r--@  1 arsis  staff  1945 Nov  1 19:02 feedback_needs_chris_drift.md
-rw-r--r--@  1 arsis  staff  1961 Nov  1 19:22 feedback_plan_review_patterns.md
-rw-r--r--@  1 arsis  staff  2779 Nov  1 19:02 feedback_spec_review_patterns.md
-rw-r--r--@  1 arsis  staff  3046 Nov  1 19:05 project_t013_review_history.md
-rw-r--r--@  1 arsis  staff   680 Nov  1 18:42 reference_reviewer_sandbox.md
-rw-r--r--@  1 arsis  staff   575 Nov  1 18:33 reference_source_fetching.md

/Users/arsis/zlayt-pm-project/reviews/:
total 2056
drwxr-xr-x@ 70 arsis  staff   2240 Nov  1 19:23 .
drwxr-xr-x  24 arsis  staff    768 Nov  1 18:12 ..
-rw-r--r--@  1 arsis  staff   9315 Nov  1 19:20 CONTRACT-M2M3-paralegal.md
-rw-r--r--@  1 arsis  staff  13530 Nov  1 19:19 CONTRACT-M2M3-product-manager.md
-rw-r--r--@  1 arsis  staff  15623 Nov  1 19:21 CONTRACT-M2M3-staff-engineer.md
-rw-r--r--@  1 arsis  staff   2547 Nov  1 19:11 GATE-M0-summary.md
-rw-r--r--@  1 arsis  staff  11483 Nov  1 18:41 T-001-staff-engineer-r2.md
-rw-r--r--@  1 arsis  staff  10968 Nov  1 19:03 T-001-staff-engineer-r3.md
-rw-r--r--@  1 arsis  staff  14020 Nov  1 18:25 T-001-staff-engineer.md
-rw-r--r--@  1 arsis  staff   9099 Nov  1 18:42 T-002-staff-engineer-r2.md
-rw-r--r--@  1 arsis  staff   8136 Nov  1 19:04 T-002-staff-engineer-r3.md
-rw-r--r--@  1 arsis  staff  11161 Nov  1 18:25 T-002-staff-engineer.md
-rw-r--r--@  1 arsis  staff  26059 Nov  1 18:50 T-003-security-r2.md
-rw-r--r--@  1 arsis  staff  21904 Nov  1 19:08 T-003-security-r3.md
-rw-r--r--@  1 arsis  staff  15722 Nov  1 18:22 T-003-security.md
-rw-r--r--@  1 arsis  staff  12666 Nov  1 18:43 T-004-staff-engineer-r2.md
-rw-r--r--@  1 arsis  staff  10855 Nov  1 19:04 T-004-staff-engineer-r3.md
-rw-r--r--@  1 arsis  staff   9672 Nov  1 18:25 T-004-staff-engineer.md
-rw-r--r--@  1 arsis  staff  15006 Nov  1 18:38 T-005-product-manager-r2.md
-rw-r--r--@  1 arsis  staff   8109 Nov  1 19:02 T-005-product-manager-r3.md
-rw-r--r--@  1 arsis  staff  13377 Nov  1 18:18 T-005-product-manager.md
-rw-r--r--@  1 arsis  staff  13004 Nov  1 18:51 T-006-security-r2.md
-rw-r--r--@  1 arsis  staff  12203 Nov  1 19:08 T-006-security-r3.md
-rw-r--r--@  1 arsis  staff  11693 Nov  1 18:22 T-006-security.md
-rw-r--r--@  1 arsis  staff   6303 Nov  1 18:22 T-007-staff-engineer-r2.md
-rw-r--r--@  1 arsis  staff   6520 Nov  1 18:19 T-007-staff-engineer.md
-rw-r--r--@  1 arsis  staff   8740 Nov  1 18:53 T-008-claims-adjuster-r2.md
-rw-r--r--@  1 arsis  staff   8650 Nov  1 18:59 T-008-claims-adjuster-r3.md
-rw-r--r--@  1 arsis  staff   6630 Nov  1 19:02 T-008-claims-adjuster-r4.md
-rw-r--r--@  1 arsis  staff  12275 Nov  1 18:37 T-008-claims-adjuster.md
-rw-r--r--@  1 arsis  staff  18587 Nov  1 18:38 T-009-claims-adjuster.md
-rw-r--r--@  1 arsis  staff  20374 Nov  1 18:59 T-009-legal-nurse-r2.md
-rw-r--r--@  1 arsis  staff  18580 Nov  1 18:36 T-009-legal-nurse.md
-rw-r--r--@  1 arsis  staff  13751 Nov  1 18:47 T-010-litigation-lead-r2.md
-rw-r--r--@  1 arsis  staff   4951 Nov  1 18:53 T-010-litigation-lead-r3.md
-rw-r--r--@  1 arsis  staff  22468 Nov  1 18:38 T-010-litigation-lead.md
-rw-r--r--@  1 arsis  staff   6291 Nov  1 18:47 T-010-product-manager-r2.md
-rw-r--r--@  1 arsis  staff  10282 Nov  1 18:32 T-010-product-manager.md
-rw-r--r--@  1 arsis  staff  10424 Nov  1 18:41 T-011-product-manager-r2.md
-rw-r--r--@  1 arsis  staff  12882 Nov  1 18:33 T-011-product-manager.md
-rw-r--r--@  1 arsis  staff  15226 Nov  1 18:55 T-012-privacy-compliance-r2.md
-rw-r--r--@  1 arsis  staff   8564 Nov  1 19:00 T-012-privacy-compliance-r3.md
-rw-r--r--@  1 arsis  staff  18436 Nov  1 18:36 T-012-privacy-compliance.md
-rw-r--r--@  1 arsis  staff  16014 Nov  1 18:34 T-013-paralegal-r2.md
-rw-r--r--@  1 arsis  staff  15270 Nov  1 18:45 T-013-paralegal-r3.md
-rw-r--r--@  1 arsis  staff  20720 Nov  1 18:24 T-013-paralegal.md
-rw-r--r--@  1 arsis  staff  18762 Nov  1 18:34 T-013-product-manager-r2.md
-rw-r--r--@  1 arsis  staff  16148 Nov  1 18:47 T-013-product-manager-r3.md
-rw-r--r--@  1 arsis  staff  16995 Nov  1 18:23 T-013-product-manager.md
-rw-r--r--@  1 arsis  staff  18464 Nov  1 18:47 T-014-privacy-compliance-r2.md
-rw-r--r--@  1 arsis  staff  12119 Nov  1 19:01 T-014-privacy-compliance-r3.md
-rw-r--r--@  1 arsis  staff  26108 Nov  1 18:29 T-014-privacy-compliance.md
-rw-r--r--@  1 arsis  staff  24014 Nov  1 18:48 T-014-staff-engineer-r2.md
-rw-r--r--@  1 arsis  staff  24404 Nov  1 19:00 T-014-staff-engineer-r3.md
-rw-r--r--@  1 arsis  staff  25158 Nov  1 18:27 T-014-staff-engineer.md
-rw-r--r--@  1 arsis  staff  15033 Nov  1 18:50 T-015-legal-nurse-r2.md
-rw-r--r--@  1 arsis  staff   9902 Nov  1 19:03 T-015-legal-nurse-r3.md
-rw-r--r--@  1 arsis  staff  15248 Nov  1 18:30 T-015-legal-nurse.md
-rw-r--r--@  1 arsis  staff  14458 Nov  1 18:48 T-015-paralegal-r2.md
-rw-r--r--@  1 arsis  staff  16936 Nov  1 19:02 T-015-paralegal-r3.md
-rw-r--r--@  1 arsis  staff  10962 Nov  1 19:08 T-015-paralegal-r4.md
-rw-r--r--@  1 arsis  staff  17968 Nov  1 18:31 T-015-paralegal.md
-rw-r--r--@  1 arsis  staff   5054 Nov  1 18:58 T-016-staff-engineer.md
-rw-r--r--@  1 arsis  staff   6826 Nov  1 19:21 T-017-product-manager.md
-rw-r--r--@  1 arsis  staff  11578 Nov  1 19:05 T-025-product-manager-r2.md
-rw-r--r--@  1 arsis  staff  11996 Nov  1 19:02 T-025-product-manager.md
-rw-r--r--@  1 arsis  staff   3544 Nov  1 19:04 T-026-ux-designer.md
-rw-r--r--@  1 arsis  staff  23638 Nov  1 19:14 T-028-staff-engineer-r2.md
-rw-r--r--@  1 arsis  staff  17323 Nov  1 19:09 T-028-staff-engineer.md
-rw-r--r--@  1 arsis  staff   5855 Nov  1 19:23 T-047-ux-designer.md
- [Spec review patterns](feedback_spec_review_patterns.md) — recurring REQUIREMENTS defects: phantom IDs, fix-induced contradictions, vocab drift, stale golden counts, scope creep
- [Calibration vs red flags](feedback_calibration_vs_redflags.md) — dossier calibration severities softer than dealbreakers; cross-check
- [Source fetching](reference_source_fetching.md) — curl+UA fallback when WebFetch is missing; blocked hosts
- [NEEDS_CHRIS drift](feedback_needs_chris_drift.md) — rows added without cards, non-Chris questions, vague actions; ADR facts vs live system
- [Reviewer sandbox](reference_reviewer_sandbox.md) — hooks block shell writes to scratchpad/memory and backtick python -c; scripts go in artifacts/review-evidence
- [Plan/contract review patterns](feedback_plan_review_patterns.md) — mention-coverage, unowned tests, wrong critical path, fixture-replay ship bar; probe script
- [T-013/T-025 review history](project_t013_review_history.md) — r1-r3 + T-025 verdicts; open: false §8 'aligned' claims, circular authority, must_not M1–M14 vs M17
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:09.009Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/ && for f in reference_reviewer_sandbox.md feedback_plan_review_patterns.md feedback_spec_review_patterns.md feedback_needs_chris_drift.md feedback_calibration_vs_redflags.md; do echo \"=== $f\"; cat \"$f\"; echo; done",
 "description": "Read relevant reviewer memory files"
}
````

### User / tool · 2026-11-02T01:23:09.103Z

**tool result**
````
=== reference_reviewer_sandbox.md
---
name: reviewer-sandbox
description: Hook limits for this reviewer — shell writes to scratchpad/memory are blocked; python -c with escaped backticks fails git-guard parsing
metadata:
  type: reference
---

The board-guard hook blocks reviewer shell redirects outside reviews/ and artifacts/review-evidence/. That includes the session scratchpad and this memory dir, so use the Write/Edit tools for memory. Put helper scripts in `artifacts/review-evidence/<card>-*.py` and run them with `python3 -I`. The git-guard hook also rejects `python3 -c "..."` strings that contain escaped backticks, so use single-quoted `-c` code that has no backticks. Related: [[source-fetching]].

=== feedback_plan_review_patterns.md
---
name: plan-review-patterns
description: Recurring defects in card-plan / milestone-contract reviews (T-017/T-018, 2026-11-01) — mention-coverage, unowned tests, wrong critical path, fixture-replay ship bars
metadata:
  type: feedback
---

Things to check first on any card-plan or AC contract review. All of these were found on the T-017 plan (19 cards, 93 AC). Verdict was "changes" in all three lenses.

1. **Coverage counted by mention.** A matrix that says R-ID → card can still leave the R-ID's pass/fail test in no AC. Compare the REQUIREMENTS test input ("edit 1, reload") against the AC text. The usual gaps are edit persistence, the LLM-failed UI state and dealbreaker UI rendering.
2. **Test files nobody writes.** CONTRACT:240 gives tests/** to qa. Script the files each AC cites and list which qa card writes each one. On T-017, 20 of 35 had no author.
3. **Critical path drawn by hand.** Compute the longest depends_on chain. The stated path left out 2 cards, and the cut list held only an M3 card for an M2 overrun. Check whether a P1 card gates the P0 path.
4. **Ship bar met by replay.** The 3-run metrics (unsupported, determinism) on the fixture backend pass by construction. Fixtures for the hallucination set and seeded edits were never recorded. Ask what happens on a fixture miss.
5. **AC numbers vs golden.** Diff every number in the AC against the golden. Found: case_07 total, "7 of 9", and "only" amounts that contradicted golden A4.
6. **Values in golden strings that no AC derives** ("12 planned; discharged at visit 9"). These are hard-coding or LLM-value risks.

**Why:** A plan review passes the coverage matrix by eye while the dealbreakers stay untested. A script catches 2–5 in minutes.

**How to apply:** Reuse artifacts/review-evidence/T-018-contract-probe.py (it parses board/cards). Re-run it on any re-plan and check the 'qa:NONE' count and the chain. Related: [[spec-review-patterns]], [[t013-review-history]].

=== feedback_spec_review_patterns.md
---
name: spec-review-patterns
description: Recurring defects found reviewing spec/REQUIREMENTS.md (T-013 r1, r2) — check these first on any requirements/AC review
metadata:
  type: feedback
---

Recurring defects in requirements docs on this project. Check them before forming opinions.

1. **Cited identifiers that don't exist.** Round 1 had R-QA-2. Round 2 cited a lexicon `hedge` category that wasn't there. Script both checks: referenced R-IDs minus defined R-IDs, and grep every cited file, key or category in the cited file.
2. **Fixing one finding contradicts another rule.** In round 2, adding a "confirm date" flow conflicted with "date not editable → 422". Cross-check every new action against the per-type edit table and against api.md.
3. **Tests whose strings follow no rule.** The negative-string E2E banned record words that no excerpt rule excluded. The hand-written worked example passed only because the writer chose the excerpts.
4. **Vocabulary drift across REQ, api.md, golden and lexicon**, for example `prior_condition` vs `pre_existing`, and golden provider aliases that grounding would reject. Always diff the flag and class enums across the four.
5. **"Orchestrator decided X" with no recorded decision.** grep DECISIONS, STATE and ASSUMPTIONS. If the decision isn't there and no card owns the reconciliation, the hand-off is not clean.
7. **Hard-coded counts drift from the golden.** Example: "19 of the 20" seeded hallucinations, when the golden now has 34. Under the "literal wording" rule this quietly weakens the ship bar. Check every count in REQ against `wc -l`/len() of the current golden files, and compare git timestamps: golden/api commits often land minutes after the REQ commit.
8. **"Checked and aligned" lists and authority loops.** Re-run every alignment claim at the other file's latest commit, because codes can swap sides between commits. Also check whether the two cards point at each other as the authority: REQ:3 names the golden as the authority, and the golden's handoff names REQ. Make sure each §8 owner card actually carries the row as an AC.
6. **Scope creep while fixing review findings.** Round 2 went from 47 to 61 R-IDs. Name the add-ons that Appendix A does not require and that need new endpoints or ADR changes (batch accept, charge reclassification, the duplicate-split action).

**Why:** These recurred across rounds and drive M2/M3 card planning (T-017). Workers implement against api.md and the ADRs, so any divergence that goes unrecorded gets built two ways.

**How to apply:** On any REQUIREMENTS or AC review, run the inventory script, check the golden data with python, grep the cited artifacts, and append a resolution table to `artifacts/review-evidence/<card>-trace.md`. See [[t013-review-history]].

=== feedback_needs_chris_drift.md
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

=== feedback_calibration_vs_redflags.md
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:09.357Z

**tool call — Bash**
````
{
 "command": "cat reviews/CONTRACT-M2M3-product-manager.md",
 "description": "Read CONTRACT-M2M3 product-manager review"
}
````

### User / tool · 2026-11-02T01:23:09.440Z

**tool result**
````
# CONTRACT M2/M3: product-manager-reviewer (T-018, PM lens)

**Verdict: changes.** 0 blockers, 6 majors, 3 minors, 1 nit.

The R-ID to card trace is complete. 60 of 62 R-IDs are named in some AC; R-CO-8 and R-SU-1..5 are deferred to M4/M5 in the coverage file. The plan's numbers are not. The stated critical path leaves out three cards, and the only cut listed is in M3, so nothing can absorb an M2 overrun. Ship bar 4 can be "met" by replaying fixtures. Ship bar 5 has no owner. Regression discipline (§8.3) is not an AC on the cards that write the prompts.

Evidence: `artifacts/review-evidence/T-018-contract-probe.py` and `.out.txt`. The probe parses every card file and computes R-ID coverage, the authors of each test file, and the longest dependency chain.

```json
{"card": "T-018", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "Milestone contract review (CONTRACT §7.4). AC of M2/M3 cards T-027, T-029..T-046 (board/cards at commit e5733a1), docs/M2M3_COVERAGE.md, docs/LLM_VS_CODE.md, against spec/REQUIREMENTS.md, memory/ORCHESTRATOR_DECISIONS.md, evals/golden/README.md, docs/CONTRACT.md §5 M2/M3 and §8.3. No app exists yet (app/backend, app/db, app/frontend empty).",
 "exercised": [
  "python3 tools/board.py list --milestone M2 ; list --milestone M3 (19 cards, all ready, AC 0/5 each)",
  "python3 tools/board.py show T-027, T-029..T-046, T-017, T-016",
  "python3 -I artifacts/review-evidence/T-018-contract-probe.py -> 62 R-IDs defined; not named in any AC: R-CO-8, R-SU-1..5; 93 AC total; longest chain to T-038: T-029 -> T-032 -> T-033 -> T-035 -> T-036 -> T-037 -> T-038",
  "grep -c verify_quickly personas/paralegal.md .claude/agents/paralegal-reviewer.md -> 0 and 0",
  "sed -n 296,316p docs/CONTRACT.md (M2 <= 3.5 h, M3 <= 3.5 h); sed -n 424,427p (§8.3); CONTRACT:260 (cut at >150% of budget)",
  "wc -l evals/golden/hallucinations.jsonl hallucinations_controls.jsonl -> 40, 10",
  "grep -n 'variant E\\|forged' memory/SCOPE_CUTS.md evals/golden/* -> no hits (only docs/LLM_VS_CODE.md:21,44)",
  "read in full: spec/REQUIREMENTS.md, docs/LLM_VS_CODE.md, docs/M2M3_COVERAGE.md, evals/golden/README.md, memory/ORCHESTRATOR_DECISIONS.md"
 ],
 "verdict": "changes",
 "scores": {"scope_fits_budget": 2, "critical_path_correct": 2, "cut_order": 2, "ac_testable": 3, "ship_bar_traced": 3, "coverage_complete": 4},
 "findings": [
  {"severity": "major", "title": "Stated M2 critical path is wrong and the only cut cannot absorb an M2 overrun",
   "evidence": "docs/M2M3_COVERAGE.md:3 'Critical path (M2): T-029 -> T-030 -> T-035 -> T-037 -> T-038 (T-036 runs beside the generator)'; :4 'about 4 h, over the 3.5 h budget. If it slips, cut ... T-046' (an M3 card). Board deps: T-036 depends_on [T-035, T-033, T-027]; T-037 depends_on [T-036, ...]; T-033 depends_on [T-029, T-032]. Probe longest chain: T-029 -> T-032 -> T-033 -> T-035 -> T-036 -> T-037 -> T-038 (7 cards, not 5). Only T-029 (1 h), T-039 (1 h) and T-046 (45 min) carry any time estimate.",
   "why_it_matters": "The 4 h figure undercounts: T-036 runs after the generator, not beside it, and two backend cards are missing from the path. A milestone can't be time-boxed without an honest path, and with no M2 cut the team either drifts past 150% (CONTRACT:260) or cuts something on the ship bar under pressure.",
   "fix": "Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md.",
   "acceptance_test": "grep -n 'M2 cut order' docs/M2M3_COVERAGE.md returns a list of >= 3 items, none naming an R-ID from REQUIREMENTS §7 ship bar rows 1-4; the stated chain equals the longest depends_on chain printed by T-018-contract-probe.py."},
  {"severity": "major", "title": "A P1 researcher card gates the P0 critical path",
   "evidence": "T-036 depends_on: [\"T-035\", \"T-033\", \"T-027\"]; T-027 priority P1, role researcher, status ready, unclaimed; T-027 AC1 '>=40 sentences ... scores >=85%'. D-024(5) moves the researcher to sonnet and caps doc cards at 2 rounds.",
   "why_it_matters": "If T-027 stalls in review, T-036, T-037, T-038 and the whole M3 backend wait on it. The lexicon already exists and the LEXICON_ONLY/LLM_ONLY rule (R-FL-3) already turns lexicon weakness into visible doubt, so the hard dependency buys little.",
   "fix": "Either raise T-027 to P0 with a timebox in its Description, or remove T-027 from T-036 depends_on and add a T-036 AC: 'runs against app/llm/lexicon.yaml at HEAD; lexicon recall per must-flag is reported by evals.run (see T-038 finding)'.",
   "acceptance_test": "python3 tools/board.py show T-036 shows depends_on without T-027, or T-027 shows priority P0 with a timebox."},
  {"severity": "major", "title": "Ship bar 4 can be met on a fixture replay: unsupported_count_3run and the judge metrics are not tied to a live backend",
   "evidence": "T-038 AC4 makes only determinism_3run live-only ('on fixture the field is null/not_measured'). unsupported_count_3run (ship bar 4: '0 unsupported statements across 3 repeated runs') has no such clause. T-045 AC4: '`python -m evals.run` (ship_bar_met true)' does not name a backend. T-037 AC2 records fixtures for 'sample + 9 cases' only, not for the 40 + 10 items in hallucinations.jsonl / hallucinations_controls.jsonl.",
   "why_it_matters": "Three replays of one recording always give 0 differences and the same verdicts. A ship bar that passes by construction is the 'demo looked fine' failure. hallucination_catch_rate cannot be computed on fixture at all unless those 50 judge calls are recorded, so the runner will either error or quietly skip them.",
   "fix": "T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BACKEND != fixture; latest.json records backend and model ids; ship_bar_met is false when backend == fixture'. T-037 AC2: 'fixtures recorded for sample, case_01..09, every line of hallucinations.jsonl and hallucinations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_bar_met true; report path in handoff'.",
   "acceptance_test": "tests/unit/test_eval_runner.py::test_fixture_cannot_ship: a fixture-backend run writes ship_bar_met false and unsupported_count_3run 'not_measured'."},
  {"severity": "major", "title": "Regression discipline (§8.3, R-CO-6) is not an AC on the cards that write prompts, and there is no check after T-038",
   "evidence": "T-035 Description: 'The eval report required by CONTRACT 8.3 is attached once m2-qa-eval-runner exists'. T-038 depends_on T-037, which depends_on T-035 and T-036, so T-035/T-036 reach in_review before any runner exists. No AC on T-035, T-036, T-027 or T-038 checks that a later prompt, lexicon or schema change carries a fresh report. CONTRACT:426 'Any change to a prompt, model, lexicon, or schema requires re-running evals.run before in_review'.",
   "why_it_matters": "This is checklist item 14. Without it, the M2 gate report can predate the last prompt edit (red flag: 'an eval report that was not re-run after the last prompt change'), and nobody will notice.",
   "fix": "T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml; `python -m evals.run --check-fresh` exits 1 when any current hash differs'. T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'.",
   "acceptance_test": "Edit one byte of a prompt in a temp copy; `python -m evals.run --check-fresh` exits non-zero (tests/unit/test_eval_runner.py::test_check_fresh)."},
  {"severity": "major", "title": "Ship bar 5 (verify_quickly >= 4) has no owner in the M2/M3 plan; REQUIREMENTS §8 row 5 points at a done card that never delivered it",
   "evidence": "REQUIREMENTS §8 row 5: '`scores.verify_quickly` (D-015) must be requested in the brief ... Owner T-016'. `python3 tools/board.py show T-016` -> status done. `grep -c verify_quickly personas/paralegal.md .claude/agents/paralegal-reviewer.md` -> 0, 0. docs/M2M3_COVERAGE.md maps R-IDs and LLM rows, never ship-bar rows.",
   "why_it_matters": "Ship bar 5 is the one human criterion and the product note must report a number for it. If the M3 gate paralegal review comes back without the key, the gate can't be scored and the note's ship-bar table has a hole.",
   "fix": "Add a 'Ship bar row -> card' table to M2M3_COVERAGE.md (rows 1-4 -> T-038, row 5 -> T-045 + M3 gate). New orchestrator card (M3): 'paralegal-reviewer agent body and M3 gate brief request scores.verify_quickly 1-5 (D-015)'.",
   "acceptance_test": "grep -c verify_quickly .claude/agents/paralegal-reviewer.md >= 1; grep -n 'Ship bar' docs/M2M3_COVERAGE.md lists rows 1-5 each with a card id."},
  {"severity": "major", "title": "The phrase-list recall 'release gate' is not computed by any AC",
   "evidence": "docs/LLM_VS_CODE.md:40 row 12 'trusted only as far as its measured recall on the golden set'; :44 row 16 'phrase list, whose recall on the golden set is a release gate'; D-018 'The lexicon self-check must run over every golden case and report recall per must-flag'. T-038 AC1 metric list has no lexicon metric; T-027 AC1 measures a held-out probe set, not the golden set.",
   "why_it_matters": "The injection defence (R-RV-6) rests on the lexicon floor for cross-record flags, and the LLM/code page tells the panel this is gated. A claim the eval report doesn't support is a red flag for the product note.",
   "fix": "T-038 AC1: add `lexicon_recall_must_flags` (pre_existing + causation, per golden case, pooled) with R-IDs R-FL-3, R-RV-6, and state the threshold in REQUIREMENTS §7 by ADR, or edit LLM_VS_CODE rows 12/16 to 'reported, not gated'.",
   "acceptance_test": "jq '.metrics.lexicon_recall_must_flags' evals/reports/latest.json is a number, with its R-ID next to it."},
  {"severity": "minor", "title": "Several AC can't be checked as written",
   "evidence": "T-046 AC5 'cut order ... recorded if M3 passes 100% of budget' (no clock or start time recorded anywhere); T-037 AC1 'all flag groups' (which?); T-037 AC2 '`ls tests/fixtures/llm | wc -l` > 0' (one file passes); T-040 AC5 'no access log of tokens' (no test named).",
   "why_it_matters": "A worker can tick these with evidence that proves nothing, and the gate reviewer has nothing to re-run.",
   "fix": "T-046 AC5: 'M3 start/end timestamps from board activity.jsonl are quoted in the handoff; if end - start > 3.5 h, SCOPE_CUTS gains the next row of REQUIREMENTS §4'. T-037 AC1: 'prints flag groups gap, conflict, pre_existing, causation, record_warning with counts 1/2/2/5/0'. T-037 AC2: see the fixture-coverage fix. T-040 AC5: 'test_api::test_no_token_in_logs captures uvicorn access log and asserts the token string is absent'.",
   "acceptance_test": "Each named test or command exists and fails when the condition is broken."},
  {"severity": "minor", "title": "Golden variant E (forged billing line in an unwarned record) is promised but has no card and no SCOPE_CUTS row",
   "evidence": "docs/LLM_VS_CODE.md:44 'documented as golden variant E, a qa item, not yet in the golden set'; grep 'variant E|forged' memory/SCOPE_CUTS.md evals/golden/* -> no hits.",
   "why_it_matters": "The one injection path that only the human catches is the honest limit the note should cite. Right now it is an orphan promise.",
   "fix": "Either add AC to T-038: 'golden variant E exists; eval asserts the forged $50,000 charge is verified-but-pending and absent from the total until accepted', or add a SCOPE_CUTS row and edit LLM_VS_CODE row 16.",
   "acceptance_test": "grep -n 'variant E' evals/golden/README.md memory/SCOPE_CUTS.md returns one hit."},
  {"severity": "minor", "title": "T-033 AC1 'sample yields $6,240, $185, $2,150 only' contradicts the golden A4 damages item",
   "evidence": "sample.expected.json amounts: ('A4', 'missing 3 days of work', None, 'damages'); REQUIREMENTS R-CH-2 '\"missing 3 days of work\" -> damages (no value)'; golden notes require 'DAMAGES MENTIONS' for record 5.",
   "why_it_matters": "An implementer who follows 'only' drops the damages mention, and T-041 AC2's byte-equal golden then fails for a reason nobody planned for.",
   "fix": "T-033 AC1: 'sample yields currency amounts $6,240, $185, $2,150 and one damages mention (record 5, value null), nothing else'.",
   "acceptance_test": "test_amounts::test_sample_amounts asserts the four items by id and class."},
  {"severity": "nit", "title": "Endpoint path spelling",
   "evidence": "T-041 AC4 'GET /api/cases/{id}/export'; memory/contracts/api.md:266 'GET /api/cases/{token}/export'.",
   "why_it_matters": "This is cosmetic, but api.md is the contract.", "fix": "Use {token}.", "acceptance_test": "grep '{id}' in the T-041 card returns nothing."}
 ],
 "whats_right": [
  "R-ID trace is complete: 60/62 named in AC text, the 6 others explicitly deferred to M4/M5 in M2M3_COVERAGE.md",
  "Test-first golden for export: T-041 AC2 and T-044 AC5 require byte equality with sample.export.expected.txt on the fixture backend",
  "Stretch discipline is right: one item, 45-min timebox, start-only-when-done, cut-first, and the R-RV-9 modal stays core"
 ],
 "questions_for_chris": []}
```
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:11.040Z

**tool call — Bash**
````
{
 "command": "cat reviews/CONTRACT-M2M3-paralegal.md",
 "description": "Read CONTRACT-M2M3 paralegal review"
}
````

### User / tool · 2026-11-02T01:23:11.118Z

**tool result**
````
# CONTRACT M2/M3: paralegal-reviewer (T-018, paralegal lens, covered by the PM agent per D-024)

**Verdict: changes.** 0 blockers, 4 majors, 4 minors.

The review-and-export journey is mostly pinned down. The letter is accepted-only, flags are kept out of it, the $185 rate is never totaled, keyboard and 375 px are covered, and reload restores statuses. Four gaps would let a build pass every AC and still lose her trust. (1) Nothing proves her edits survive a reload or show up in the notes with the original. (2) The reconciliation count in one test-first AC is wrong. (3) No AC renders the accident-date conflict as two dates. (4) A record whose model call fails three times has no visible place in the UI.

Evidence: card AC text via `board.py show`, the golden export at `evals/golden/sample.export.expected.txt`, and `artifacts/review-evidence/T-018-contract-probe.out.txt`. There is no app yet, so this is a contract review. `scores.verify_quickly` is projected from the AC, not measured.

```json
{"card": "T-018", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "Contract review of M3 journey AC (T-039..T-046) plus M2 items she sees (T-032, T-033, T-036), against spec/REQUIREMENTS.md §1.5-1.6, §6, ORCHESTRATOR_DECISIONS D-001/D-002/D-010/D-017/D-019, evals/golden/sample.export.expected.txt; commit e5733a1. No running app (M1).",
 "exercised": [
  "python3 tools/board.py show T-039 T-040 T-041 T-042 T-043 T-044 T-045 T-046 (AC text read item by item against the paralegal checklist 1-23)",
  "grep -n '12 planned' evals/golden/sample.export.expected.txt -> line 72 rate note",
  "grep -n LLM_FAILED_AFTER_RETRIES memory/contracts/api.md -> :454 'the record has no entry from it'",
  "read personas/paralegal.md in full; REQUIREMENTS R-RV-2, R-RV-8, R-EX-4, R-EX-7, R-FL-2, R-FL-6, R-CH-3, R-CO-9"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "letter_isolation": 5, "charges_reconcilable": 4, "edits_safe": 2, "adverse_facts_surfaced": 3},
 "findings": [
  {"severity": "major", "title": "No AC proves her edit survives a reload, or that the notes show original and new text",
   "evidence": "R-RV-8 test: 'accept 3 items, edit 1, reload -> same statuses'. T-043 AC3 'reload restores statuses and total' (no edit in the matrix). T-044 AC1 checks the 'edited' label and the letter, not the reload or notes. R-RV-2: 'the notes list the original and the new text'. T-039 AC2 notes tests cover order, cites, bills line and dismissal, not EDITED ITEMS content. Golden notes show only 'EDITED ITEMS - none'.",
   "why_it_matters": "'Losing my edits on refresh or export' is a dealbreaker for her. As written, a build that drops edited summaries on reload, or prints 'EDITED ITEMS - none' after an edit, passes every AC.",
   "fix": "T-044 AC1 append: 'reload -> edited summary and \"edited\" label persist; export notes list record 3 under EDITED ITEMS with original and new text'. T-039 AC2 append: 'test_export::test_edited_items_section with entry 3 edited lists both texts and any keep-my-wording confirmation'.",
   "acceptance_test": "tests/e2e/test_edit.py::test_edit_survives_reload and tests/unit/test_export.py::test_edited_items_section, both red before T-044/T-041."},
  {"severity": "major", "title": "T-039 AC2 reconciliation count contradicts R-EX-7",
   "evidence": "T-039 AC2: 'dismissing entry 5 gives \"Record 5 ... dismissed\" and 7 of 9'. R-EX-7: 'dismiss entry 5 and leave entry 6 pending -> ... \"7 of 9\"'. With only entry 5 dismissed and the rest accepted, 8 of 9 records are in the letter. T-044 AC4 has it right.",
   "why_it_matters": "'N of 9 records in letter' is how she knows nothing dropped silently. A test-first suite that encodes the wrong count either fails a correct build or teaches the builder to miscount.",
   "fix": "T-039 AC2: 'dismissing entry 5 and leaving entry 6 pending gives \"Record 5 ... dismissed\", \"Record 6 ... not reviewed\" and 7 of 9'.",
   "acceptance_test": "test_export::test_reconciliation asserts both record lines and '7 of 9'."},
  {"severity": "major", "title": "No UI AC shows the accident-date conflict as two unmerged dates with both quotes",
   "evidence": "T-043 AC1: 'four flag groups ... sample has >=1 flag per group' (only a count). T-033 AC4 covers the backend rule. R-FL-2(a): '2026-01-09 (records 1, 2) vs \"Date of accident per intake form: 2026-01-19\" (record 7) ... not merged ... no choice made'.",
   "why_it_matters": "Merging or resolving the two accident dates is one of her dealbreakers, and it is the first thing an adjuster checks. The backend can be right while the card shows one date, or wording like 'corrected', and no test would fail.",
   "fix": "T-043 AC1 append: 'the accident-date conflict card shows \"Date of accident per intake form: 2026-01-19.\" and the 2026-01-09 header line(s) of records 1 and 2 side by side, and contains none of \"resolved\", \"correct date\", \"delay\"'.",
   "acceptance_test": "tests/e2e/test_flags_panel.py::test_accident_date_conflict_two_dates."},
  {"severity": "major", "title": "A record whose model call fails three times has no visible state in any M3 AC",
   "evidence": "R-CO-9: 'the item shows \"could not process\" with the reason, and the app stays usable'. api.md:454 'LLM_FAILED_AFTER_RETRIES | needs_review | ... the record has no entry from it'. T-034 AC2 tests the retry wrapper only; T-042 AC2 tray covers 'rejected' items; R-EX-7 reasons list 'rejected, dismissed or not reviewed', with nothing for failed. No M3 card names LLM_FAILED_AFTER_RETRIES.",
   "why_it_matters": "A record that silently has no entry is a lost fact, maybe the visit that closes a gap. She has to see 'record 4: could not process' and find it in the notes reconciliation.",
   "fix": "T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 \"could not process\" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECORDS NOT IN THE TREATMENT SECTION with reason \"could not process\"'.",
   "acceptance_test": "tests/e2e/test_timeline.py::test_llm_failed_record_visible and test_export::test_failed_record_reconciled."},
  {"severity": "minor", "title": "Needs-review reason sentence not asserted on the item itself",
   "evidence": "R-FL-6 'when needs_review, a one-sentence reason'. T-042 AC2 'rows show date, provider, summary, excerpt, state'; T-043 AC1 shows groups only. The reason is only tested via Why? (T-042 AC3).",
   "why_it_matters": "Checklist 16: items needing review say why in one sentence, on sight, without an extra click per item.",
   "fix": "T-042 AC2 append: 'every needs_review row shows its why-template sentence inline'.",
   "acceptance_test": "test_timeline.py::test_reason_inline on case_07 record 3 shows the INJECTION_SUSPECTED sentence."},
  {"severity": "minor", "title": "$185 UI string is truncated relative to R-CH-3",
   "evidence": "T-043 AC2 \"'rate $185/visit; visit count not stated'\"; R-CH-3 \"rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review\".",
   "why_it_matters": "The '12 planned; discharged at visit 9' context is what lets her write the ledger request without opening two records.",
   "fix": "Quote the full R-CH-3 string in T-043 AC2.", "acceptance_test": "test_charges.py asserts the full string."},
  {"severity": "minor", "title": "Charges and injection banner not covered by the source-record and banner tests",
   "evidence": "R-RV-9 'Entries, flags ... and charges open the full record'; T-042 AC4 entry 8, T-043 AC5 gap flag, no charge. LLM_VS_CODE row 16 'a banner names the record and says flags may be incomplete'; T-043 AC1 'case_07 shows an injection warning'.",
   "why_it_matters": "She reconciles the $6,240 against the ER record, and she needs to know which record may have suppressed flags.",
   "fix": "T-043 AC5 append 'and the $6,240 charge opens record 2 with \"ER charges: $6,240.\" highlighted'. T-043 AC1: 'case_07 banner names record 3 and says flags may be incomplete'.",
   "acceptance_test": "test_source_record.py::test_charge_highlight; test_flags_panel.py::test_injection_banner_names_record."},
  {"severity": "minor", "title": "Dismissed-flag reason not proven to reach the notes",
   "evidence": "R-RV-5 'A dismissed flag may carry an optional reason'; R-EX-4(3) 'Flags dismissed, with any reason'. T-043 AC3 dismiss -> reset -> dismiss has no reason; T-039 AC2 has no FLAGS DISMISSED content case.",
   "why_it_matters": "The attorney reads why she dismissed the 'new onset' flag. If the reason is lost, the dismissal looks like an oversight.",
   "fix": "T-043 AC3 append 'dismiss the gap flag with reason \"treating elsewhere, records requested\" -> notes FLAGS DISMISSED shows it verbatim'.",
   "acceptance_test": "test_review_matrix.py::test_dismiss_reason_in_notes."}
 ],
 "whats_right": [
  "Letter isolation is tested from both sides: builder has no flags argument (T-039 AC1) and E2E bans note text, labels, '73 days', counts (T-045 AC2)",
  "$185 can't reach the total by any path: T-033 AC2, T-039 AC3 accept-$185 keeps $8,390, T-043 AC2 no PT total",
  "Copy asks once when a flag is pending, '1 flag not reviewed' (T-044 AC4), and the count line is in neither block (T-044 AC3)"
 ],
 "questions_for_chris": []}
```
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:11.398Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-017-product-manager.md",
 "description": "Read T-017 product-manager review"
}
````

### User / tool · 2026-11-02T01:23:11.480Z

**tool result**
````
# T-017 M2/M3 plan: product-manager-reviewer

**Verdict: changes.** 0 blockers, 4 majors, 1 minor.

T-017's two AC are met as worded. Every R-ID appears in some AC or is explicitly deferred, and every LLM_VS_CODE row maps to a card. Mentioning an R-ID, though, is not the same as testing its pass condition. Four R-IDs are named but their REQUIREMENTS test is missing. Three AC contradict the golden or REQUIREMENTS. 20 of the 35 test files have no author. The critical path and the cut order are wrong. Details and the exact AC edits are in the three T-018 lens reviews (`reviews/CONTRACT-M2M3-{product-manager,paralegal,staff-engineer}.md`). This file judges the plan as a planning artifact.

```json
{"card": "T-017", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "T-017 deliverables: 19 cards T-027, T-029..T-046 on the board (commit e5733a1 'plan(M2/M3): 18 cards T-029..T-046 with coverage matrix'), docs/M2M3_COVERAGE.md, artifacts/tmp/m2m3_cards.json; T-017 AC1-2 and handoff.",
 "exercised": [
  "python3 tools/board.py show T-017 (AC1, AC2 checked with evidence; handoff 'Critical path M2 ~4 h ... cut order T-046 first')",
  "python3 -I artifacts/review-evidence/T-018-contract-probe.py -> R-IDs not named in any AC: R-CO-8, R-SU-1..5 (deferred in coverage); 20/35 cited test files with no qa author; longest chain T-029->T-032->T-033->T-035->T-036->T-037->T-038",
  "each R-ID's REQUIREMENTS pass/fail column compared with the AC of the cards M2M3_COVERAGE.md maps it to (R-RV-8, R-CO-9, R-EX-4, R-EX-7, R-FL-2, R-EX-8 spot-checked in full)",
  "grep -c verify_quickly .claude/agents/paralegal-reviewer.md -> 0",
  "golden cross-check: sample.expected.json amounts (A4 damages), sample.export.expected.txt:72, golden README:144 (case_07 total $420)"
 ],
 "verdict": "changes",
 "scores": {"coverage_complete": 4, "ac_testable": 3, "ac_consistent_with_golden": 2, "plan_realism": 2},
 "findings": [
  {"severity": "major", "title": "Coverage counts R-ID mentions rather than pass conditions; four R-IDs are named but their REQUIREMENTS test is in no AC",
   "evidence": "R-RV-8 test 'accept 3 items, edit 1, reload': T-043 AC3 reloads statuses only, with no edit. R-CO-9 'item shows \"could not process\"': only T-034 AC2 (wrapper); no M3 AC. R-EX-4(10) 'edited items, with original and new text': no AC exercises it with an edit. R-FL-2(a) 'shown as a conflict and not merged': UI AC T-043 AC1 checks group counts only.",
   "why_it_matters": "T-017 AC1 ('covered by >=1 M2/M3 card AC') was ticked by matrix lookup. Coverage looks complete in the matrix while dealbreaker behaviour (lost edits, merged accident dates, a silently missing record) goes untested.",
   "fix": "Add a 'pass condition -> AC n' column to M2M3_COVERAGE.md and fill it for every R-ID, using the AC edits in the T-018 paralegal review (T-044 AC1, T-043 AC1, T-042 AC2, T-041 AC3, T-039 AC2).",
   "acceptance_test": "For each R-ID row, the cited 'card ACn' text contains that R-ID's REQUIREMENTS test input (e.g. 'edit' + 'reload' for R-RV-8)."},
  {"severity": "major", "title": "Three AC contradict the golden or REQUIREMENTS, so they can't pass on a correct build",
   "evidence": "T-039 AC1 case_07 total '$8,390.00' (golden case_07 total $420); T-039 AC2 'dismissing entry 5 gives ... 7 of 9' (R-EX-7: 7 of 9 needs entry 6 pending too); T-033 AC1 '$6,240, $185, $2,150 only' (golden A4 damages item, required by the notes golden).",
   "why_it_matters": "Under test-first, a wrong red test either forces a wrong build or gets edited by the implementer, which defeats 'agree on done before code'.",
   "fix": "Apply the exact edits in reviews/CONTRACT-M2M3-staff-engineer.md (T-039 AC1, T-033 AC1) and reviews/CONTRACT-M2M3-paralegal.md (T-039 AC2). Add a plan self-check: every number in an AC is diffed against evals/golden expected values.",
   "acceptance_test": "grep -n '7 of 9' board/cards/T-039.md appears only next to 'entry 6 pending'; T-039 AC1 names $420.00 for case_07."},
  {"severity": "major", "title": "Validation is named but unowned: 20 of 35 cited test files have no qa author, and LLM_VS_CODE row 10 is mapped against the table",
   "evidence": "Probe 'qa:NONE' x20 (test_provider, test_judges, test_pipeline, test_api, 10 E2E files, ...). CONTRACT:240 'qa -> tests/**'. T-017 AC2 evidence: 'each card AC names its test/eval'. Row 10 says Code for provider-spelling conflicts; the coverage maps it to T-036 (LLM).",
   "why_it_matters": "AC2 asked for the validation to be named in AC. Naming a file no card writes is a promise with no owner, and a row-10 mismatch is a defect by LLM_VS_CODE's own rule.",
   "fix": "See staff-engineer review findings 1 and 7: a qa test-first card for LLM stages, T-039 AC4 naming the E2E files, and a row 10 engine decision (T-033 AC or an ADR).",
   "acceptance_test": "Re-run the probe: 0 'qa:NONE'; LLM_VS_CODE row 10 and the coverage row 10 name the same engine."},
  {"severity": "major", "title": "Critical path, budget and cut order in the handoff are wrong, and ship-bar rows are not traced",
   "evidence": "Handoff 'Critical path M2 ~4 h ...: T-029 -> T-030 -> T-035 -> T-037 -> T-038; cut order T-046 first' vs the 7-card depends_on chain; T-046 is M3. No 'ship bar row -> card' table; ship bar 5 key verify_quickly appears 0 times in the paralegal agent; LLM_VS_CODE row 16 lexicon 'release gate' is in no AC.",
   "why_it_matters": "A plan that can't say what gets cut in M2, or who measures ship bar 5, is not 'agreed done'.",
   "fix": "See PM review findings 1, 2, 5, 6: correct the chain with per-card estimates, an M2 cut order, a ship-bar trace table, and a lexicon recall metric (or a reworded row 16).",
   "acceptance_test": "M2M3_COVERAGE.md has 'M2 cut order' and 'Ship bar row -> card' sections; the chain matches the probe."},
  {"severity": "minor", "title": "T-017 AC2 evidence overstates: not every LLM_VS_CODE row maps to an M2 card",
   "evidence": "T-017 AC2 'every row ... maps to an M2 card'; M2M3_COVERAGE row 19 -> T-041, T-045 (both M3); row 15 edit half -> T-040 (M3).",
   "why_it_matters": "The plan is fine (export belongs in M3), but evidence that says more than the artifact shows is the habit the gate punishes.",
   "fix": "Reword the evidence: 'rows 1-18, 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design'.",
   "acceptance_test": "board.py show T-017 AC2 evidence names row 19 as M3."}
 ],
 "whats_right": [
  "One card per pipeline stage with the R-IDs and LLM_VS_CODE rows in each Description, which makes this review possible in one pass",
  "Grounding verifier sequenced first and all-code (T-030), as CONTRACT M2 'write it first' asks",
  "Non-goals and M4/M5 items are listed explicitly in the coverage file rather than silently dropped"
 ],
 "questions_for_chris": []}
```
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:13.092Z

**tool call — Bash**
````
{
 "command": "cat reviews/CONTRACT-M2M3-staff-engineer.md",
 "description": "Read CONTRACT-M2M3 staff-engineer review"
}
````

### User / tool · 2026-11-02T01:23:13.167Z

**tool result**
````
# CONTRACT M2/M3: staff-engineer-reviewer (T-018, staff-engineer lens, covered by the PM agent per D-024)

**Verdict: changes.** 0 blockers, 9 majors, 4 minors.

The plan never puts an LLM on arithmetic, dates, totals or export. The code-stages-without-LLM test (T-037 AC4) is the right kind of boundary proof. But test-first holds for only 15 of the 35 test files the AC cite; the other 20 have no qa author, although CONTRACT:240 gives `tests/**` to qa. Three fallback paths are left unspecified: the Anthropic SDK's built-in retries, a fixture-cache miss, and judge #2/#3/#4 errors. Two values the golden export requires byte for byte ("12 planned; discharged at visit 9" and the damages mention) have no AC that says code derives them. I found no red-flag violation in the plan itself, so there are no blockers.

Evidence: `artifacts/review-evidence/T-018-contract-probe.py` and `.out.txt`, which list test-file authorship and the dependency chains.

```json
{"card": "T-018", "persona": "staff-engineer-reviewer", "model": "claude-opus-5-5",
 "scope": "Contract review of AC + depends_on for T-027, T-029..T-046 at commit e5733a1 against docs/LLM_VS_CODE.md (rules 1-11, rows 1-20), CONTRACT §5.2/§8.3 and :240 ownership, memory/contracts/api.md, evals/golden. No product code exists (app/backend, app/db, app/frontend empty).",
 "exercised": [
  "python3 tools/board.py show T-029..T-046 (depends_on + AC)",
  "python3 -I artifacts/review-evidence/T-018-contract-probe.py -> 35 test files cited; 20 cited by no qa card (test_api, test_audited, test_charges, test_conflicts, test_edit, test_export_ui, test_flag_templates, test_flags_injection, test_flags_panel, test_flags_sample, test_input, test_judges, test_keyboard_mobile, test_pipeline, test_provider, test_review_matrix, test_schemas, test_side_by_side, test_source_record, test_timeline); grep -c 'qa:NONE' .out.txt -> 20",
  "grep -n ownership docs/CONTRACT.md:240 ('qa -> tests/**, evals/**'; 'db -> app/db/**, migrations, fixtures')",
  "python3 -I -c (sample.expected.json amounts) -> A4 'missing 3 days of work' None damages",
  "grep -n '12 planned' evals/golden/sample.export.expected.txt -> :72",
  "grep -c '^## (GET|POST|DELETE)' memory/contracts/api.md -> 11 endpoints",
  "ls app/llm -> lexicon.yaml, prompts/ (no code yet)"
 ],
 "verdict": "changes",
 "scores": {"dependencies_correct": 2, "test_first_real": 2, "boundary_enforced_by_tests": 3, "no_hidden_retries_fallbacks": 2, "determinism_and_audit": 4},
 "findings": [
  {"severity": "major", "title": "Test-first is real for 15 of 35 test files; 20 have no qa author although qa owns tests/**",
   "evidence": "Probe: test_provider, test_audited (T-034), test_schemas, test_judges (T-035/036), test_flags_sample, test_flags_injection (T-036), test_pipeline (T-037), test_conflicts, test_flag_templates (T-033), test_api (T-040, T-041), and E2E test_input, test_timeline, test_source_record, test_flags_panel, test_charges, test_review_matrix, test_keyboard_mobile, test_edit, test_export_ui, test_side_by_side are cited only by backend/frontend cards. T-039 AC4 lists E2E by R-ID but names no files. CONTRACT:240 'qa -> tests/**'.",
   "why_it_matters": "Either the implementer writes its own tests after the code (not test-first, and a cross-boundary write), or nobody does and the AC can't be ticked. The LLM-stage tests are the ones where test-after drifts toward the output.",
   "fix": "T-029 AC4 or a new qa card 'M2 LLM-stage tests first' (deps [], blocks T-034..T-037): write test_provider, test_audited, test_schemas, test_judges, test_flags_sample, test_flags_injection, test_pipeline, test_conflicts, test_flag_templates red. T-039 AC4: name test_api.py plus the 10 E2E files above, by file.",
   "acceptance_test": "Re-run T-018-contract-probe.py: every cited test file has a qa card in its 'qa:' column."},
  {"severity": "major", "title": "Missing depends_on edges let implementers start before their red tests or API exist",
   "evidence": "T-031 depends_on [] but test_db.py is written by T-029 AC4. T-042 depends_on [] and T-043 depends_on [T-042]: neither depends on T-039 (their E2E specs). T-043 AC3 'reload restores statuses and total' needs T-040 persistence, and T-043 AC2 totals need T-041/T-040, but T-043 has no backend dependency.",
   "why_it_matters": "The board's `next` will hand T-031/T-042 out first. Frontend gets built against a draft, and T-043 can't go green without a server, so it sits in_progress or is ticked against mocks.",
   "fix": "T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.",
   "acceptance_test": "board.py show T-031/T-042/T-043 shows the edges; probe chain to T-045 includes T-039."},
  {"severity": "major", "title": "Hidden retries: the Anthropic SDK retries twice by default and no AC turns that off",
   "evidence": "T-034 Description 'Backends never retry; audited.py owns the 1+2 retry loop'. T-034 AC4 tests the claude-cli argv (timeout, model pin) only; for anthropic-api it says 'tested against recorded fixtures/mocked SDK'. The anthropic Python client defaults to max_retries=2, so 3 audited attempts x 3 SDK attempts = up to 9 calls, with only 3 llm_calls rows.",
   "why_it_matters": "R-CO-9 caps retries at 2 with changed conditions and an audit row per attempt. SDK retries are unlogged and unchanged, the exact 'silent retry' this persona has been paged for.",
   "fix": "T-034 AC4 append: 'anthropic-api client is constructed with max_retries=0 and an explicit timeout (<= 120 s); test_provider::test_sdk_no_internal_retry asserts both on the constructed client'.",
   "acceptance_test": "test_provider::test_sdk_no_internal_retry fails if max_retries is left at the SDK default."},
  {"severity": "major", "title": "Fixture-backend miss behaviour is unspecified, and fixtures are recorded for too few inputs",
   "evidence": "T-034 AC1 'LLM_BACKEND=fixture pytest ... green with no API key' (no miss rule). T-037 AC2 'fixtures recorded ... for sample + 9 cases; `ls tests/fixtures/llm | wc -l` > 0'. Not recorded: 40 hallucinations.jsonl + 10 controls (judge #1), sample seeded_edits SE1-SE5 (T-039 AC3 'seeded herniation -> 409' runs on fixture).",
   "why_it_matters": "A fixture backend that returns a default or empty answer on a miss is a silent fallback inside every unit test and every demo-mode run. With today's recording list, hallucination_catch_rate and the herniation test can only pass through such a fallback.",
   "fix": "T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash); the audited wrapper turns it into LLM_FAILED_AFTER_RETRIES; never a default answer'. T-037 AC2 replace with: 'replaying sample, case_01..09, hallucinations(.jsonl, _controls) and SE1-SE5 on fixture reports 0 FixtureMissing (count printed)'.",
   "acceptance_test": "test_provider::test_fixture_miss_raises; `LLM_BACKEND=fixture python -m evals.run` prints 'fixture misses: 0'."},
  {"severity": "major", "title": "Judges #2, #3, #4 have no error, timeout or 'unsure' path in AC",
   "evidence": "T-035 AC3 gives judge #1 'error/timeout -> JUDGE_UNAVAILABLE'. T-035 AC4 (judge #2) covers 'disagrees -> JUDGE_DISAGREES' only; LLM_VS_CODE row 7 'agrees, disagrees, unsure' and 'A charge is verified only when judge 2 agrees'. T-036 AC5 '#3 and #4 must agree or flag is needs_review' (no error case).",
   "why_it_matters": "This is red-flag territory: an unspecified exception path is where 'on judge error, mark verified' gets written. A $6,240 charge verified because judge #2 timed out is the bad day.",
   "fix": "T-035 AC4 append: 'judge #2 unsure, error or timeout -> needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a charge is verified only on agrees'. T-036 AC5 append: 'judge #3/#4 error or timeout -> needs_review JUDGE_UNAVAILABLE'.",
   "acceptance_test": "test_judges::test_j2_timeout_never_verified and test_j34_unavailable using a fixture backend that raises TimeoutError."},
  {"severity": "major", "title": "LLM/code boundary test omits most code-only modules",
   "evidence": "T-029 AC4 test_boundaries scans 'gap, amounts, dates, dedupe, sentences, export'. LLM_VS_CODE rule 1 adds sorting, quote-matching, number-matching and schema checks; rows 10 (accident-date conflict), 14 (flag_templates), 16 (injection scan), 17 (confidence), 18 (why) are Code. T-030 AC5 claims 'test_boundaries green for these modules' (grounding, confidence, why), which T-029 never lists.",
   "why_it_matters": "Staff checklist 1-2: the table must match the code row by row. A boundary test that doesn't list grounding.py lets 'ask the model if the quote matches' through.",
   "fix": "T-029 AC4: module list = sentences, grounding, confidence, why, dates, ingest/dedupe, amounts (find + classify), totals, gaps, conflicts (accident date), flag_templates, injection scan, export; scan transitive imports, not just direct ones.",
   "acceptance_test": "test_boundaries.py parametrized over that list; adding `from app.llm import provider` to confidence.py makes it fail."},
  {"severity": "major", "title": "Row 10 split diverges: LLM_VS_CODE says code for provider-spelling conflicts, the plan gives it to the LLM card without saying which engine",
   "evidence": "LLM_VS_CODE.md:38 row 10 'Conflicts that are structural: ... the same provider spelled two ways | Code'. M2M3_COVERAGE row 10 -> 'T-036 (provider variants)'. T-036 AC3 'case_05 provider-name conflict raised and name variants tolerated' (engine not named). T-036 AC2 also lists 'conflict (a) accident date', which is T-033's code rule.",
   "why_it_matters": "A divergence from the table is a defect by the table's own rule (LLM_VS_CODE:107). Both engines raising the accident-date conflict costs conflict precision, and the panel will see two copies of the same flag.",
   "fix": "Either T-033 gains AC6 'case_05 provider conflict raised by code (normalized-name rule), no LLM call', or an ADR edits row 10 and T-036 AC3 says 'raised by the LLM conflict pass + judge #3'. T-036 AC2 append 'exactly one accident-date conflict flag in pipeline output (from T-033)'.",
   "acceptance_test": "test_conflicts::test_case05_code_only (LLM counter 0) or the ADR id in LLM_VS_CODE row 10; test_pipeline asserts one C1."},
  {"severity": "major", "title": "Two golden values have no producing AC: the rate note's '12 planned; discharged at visit 9' and the damages mention",
   "evidence": "sample.export.expected.txt:72 'Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.'; golden A4 ('missing 3 days of work', None, damages). T-041 AC2 requires both byte for byte. T-033 AC1 says 'sample yields $6,240, $185, $2,150 only' and no AC says where 12 and 9 come from. LLM_VS_CODE rule 2: 'The model never supplies a value'.",
   "why_it_matters": "The likely shortcuts are hard-coding the sample's string or letting the generator/conflict pass supply 12 and 9. The first passes the golden and breaks on the next case; the second breaks rule 2.",
   "fix": "T-033 new AC: 'rate note numbers are code-derived: N planned from the \"Plan of care: N visits\" match in a record with the same provider prefix, M from the highest \"visit M\" in a header label; omitted when not found; test on sample and a variant (plan 10, last visit 7)'. T-033 AC1: add 'one damages mention (record 5, value null) from the lexicon damages rule'.",
   "acceptance_test": "test_amounts::test_rate_note_derived_by_code (variant yields '10 planned; discharged at visit 7'); test_amounts::test_sample_amounts lists A4."},
  {"severity": "major", "title": "T-039 AC1 encodes a wrong total for case_07; money-as-cents is never asserted",
   "evidence": "T-039 AC1: \"total line exactly 'Billed charges stated in these records: $8,390.00' incl. case_07 with a rate present\". case_07's only charge is $420 (golden README:144). R-EX-8 asks only that the line keeps the template on case_07. No AC asserts integer cents (LLM_VS_CODE row 6 'money as whole cents'; checklist 6).",
   "why_it_matters": "A test-first test that is wrong forces a wrong build or gets 'fixed' by the implementer. Float money is a red flag that only a test catches early.",
   "fix": "T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is exactly \"Billed charges stated in these records: $420.00\"; with the $185 rate non-dismissed the sample line is unchanged'. T-033 AC1 append: '\"$6,240\" parses to int 624000; app/backend/amounts.py contains no float('.",
   "acceptance_test": "test_export::test_total_line_case07 and test_amounts::test_cents_int."},
  {"severity": "minor", "title": "'Red' is proven by --collect-only, which proves only that tests exist",
   "evidence": "T-029 AC3 'proved by `pytest tests/unit -q --collect-only`'; T-039 AC1 and AC4 same.",
   "why_it_matters": "Collected tests that pass vacuously, or error on import, count as red. Red tests on main also break every other worker's `pytest tests/unit` unless they are marked.",
   "fix": "'each new test is marked xfail(strict=True, reason=\"T-0xx\") and `pytest -rx` shows them xfailed with NotImplementedError, 0 errors'; the implementing card's AC removes the marks.",
   "acceptance_test": "pytest tests/unit -rx output lists the xfails by card id."},
  {"severity": "minor", "title": "Retry 'changed conditions' and the judge's input isolation are asserted only in prose",
   "evidence": "T-034 AC2 'each retry with changed conditions'; LLM_VS_CODE rule 5 'sees only the record and the candidate' and 'by default a different model'; T-035 AC5 checks only that prompts differ.",
   "why_it_matters": "Checklist 8 and 10. A retry that resends the same prompt, or a judge that sees the generator's prompt, passes as written.",
   "fix": "T-034 AC2: 'consecutive attempts have different prompt hashes in llm_calls'. T-035 AC5: 'rendered judge #1 prompt contains the record and candidate only (no generator prompt text); judge model id is config, default != generator model'.",
   "acceptance_test": "test_audited::test_retry_changes_prompt; test_judges::test_judge_input_isolation."},
  {"severity": "minor", "title": "No AC proves a test fails when the verifier is stubbed",
   "evidence": "Red flag: 'Tests that ... pass even when the verifier is stubbed out'. T-030 AC5 test_no_silent_fix checks repair, not removal.",
   "why_it_matters": "This is the cheapest guard against vacuous grounding tests.",
   "fix": "T-030 AC6: 'monkeypatching grounding.verify to always pass makes test_grounding and test_pipeline::test_rejected_never_in_timeline fail'.",
   "acceptance_test": "test_grounding::test_mutation_guard."},
  {"severity": "minor", "title": "No global no-network guard for tests",
   "evidence": "T-039 AC5 'use the fixture backend only (no key, no network)' is per-card prose; T-034 AC1 likewise.",
   "why_it_matters": "One test that reaches the network is flaky and spends money.",
   "fix": "T-029 AC5 append: 'tests/conftest.py blocks socket.connect except localhost; a test opening api.anthropic.com fails'.",
   "acceptance_test": "test_boundaries::test_network_blocked."}
 ],
 "whats_right": [
  "T-037 AC4 proves code stages (ingest, gaps) produce results when every LLM call raises: the right boundary test",
  "Single call path and no record text in logs are tested (T-034 AC5); audit row per attempt with prompt hash and backend (T-031 AC2)",
  "Gap boundaries 29/30/31 incl. leap year, D-003 exclusion via case_09, and dismissal-invariance are all in T-033 AC3"
 ],
 "questions_for_chris": []}
```
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:15.600Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list 2>&1 | head -120; echo \"---show T-048\"; python3 tools/board.py show T-048 2>&1 | head -80",
 "description": "List board cards and show T-048"
}
````

### User / tool · 2026-11-02T01:23:15.786Z

**tool result**
````
T-001	M0	orchestrator	done             	P0	AC 4/4	Board CLI (tools/board.py): cards, transitions, claims, reviews, gates, status
T-002	M0	orchestrator	done             	P0	AC 4/4	Board web UI (tools/board_server.py) + Tailscale serve
T-003	M0	orchestrator	done             	P0	AC 3/3	Hooks + .claude/settings.json (stop-guard, teammate-idle, board-validate, git-guard, reviewer-write-guard)
T-004	M0	orchestrator	done             	P0	AC 3/3	Agent definitions: 8 workers + 13 reviewer personas (provisional)
T-005	M0	orchestrator	done             	P1	AC 3/3	CLAUDE.md map, memory seeds, RUNBOOK, ENVIRONMENT
T-006	M0	orchestrator	done             	P0	AC 3/3	Secrets scanner + git hygiene (check_secrets.py, .gitignore, conventional commits, tag m0)
T-007	M0	orchestrator	done             	P0	AC 3/3	M0 smoke test (§4.8) + heartbeat + Playwright screenshot of board
T-008	M1	researcher 	done             	P0	AC 4/4	Domain research: PI treatment chronologies, demand packages, what adjusters attack
T-009	M1	researcher 	done             	P0	AC 3/3	Flag lexicon (app/llm/lexicon.yaml) with per-phrase rationale and source
T-010	M1	researcher 	done             	P0	AC 3/3	Persona dossiers: 5 domain personas (paralegal, litigation-lead, claims-adjuster, legal-nurse, privacy-compliance)
T-011	M1	researcher 	done             	P1	AC 2/2	Persona dossiers: 8 product/engineering personas (PM, UX, staff-eng, security, chaos, a11y, installer, hiring-panel)
T-012	M1	researcher 	done             	P1	AC 1/1	Research: PHI handling and supervision of AI output at law firms
T-013	M1	writer     	done             	P0	AC 4/4	spec/REQUIREMENTS.md: testable must-haves, stretch pick, non-goals
T-014	M1	architect  	done             	P0	AC 4/4	Architecture ADRs + docs/LLM_VS_CODE.md + API contract draft
T-015	M1	qa         	done             	P0	AC 4/4	Eval golden set: sample case + 6-10 synthetic stress cases with hand-written expected outputs
T-016	M1	orchestrator	done             	P0	AC 2/2	Compile persona dossiers into reviewer agent bodies (replace PROVISIONAL)
T-017	M1	orchestrator	in_review        	P0	AC 2/2	Plan M2 + M3 cards with testable acceptance criteria traced to REQUIREMENTS and LLM_VS_CODE
T-018	M1	orchestrator	in_review        	P0	AC 2/2	Milestone contract review (PM + paralegal + staff-engineer) of M2/M3 AC and the LLM/code table; apply edits
T-019	M5	orchestrator	needs_chris      	P1	AC 0/1	Provide a real Anthropic API key for the public deployment (NEEDS_CHRIS #1)
T-020	M5	orchestrator	cancelled        	P2	AC 0/1	Restart the session once so native agent definitions load (NEEDS_CHRIS #2)
T-021	M5	orchestrator	cancelled        	P2	AC 0/1	Confirm tailnet ports :7777/:7860 are fine (443/8443 kept for your services) (NEEDS_CHRIS #3)
T-022	M5	orchestrator	needs_chris      	P1	AC 0/1	Public link: demo-only or live? (NEEDS_CHRIS #2)
T-023	M5	orchestrator	needs_chris      	P2	AC 0/1	Live-model eval budget on claude.ai plan (NEEDS_CHRIS #3)
T-024	M5	orchestrator	done             	P2	AC 1/1	Git author email for this repo (NEEDS_CHRIS #4)
T-025	M1	writer     	done             	P0	AC 6/6	Spec reconciliation: REQUIREMENTS vs golden, D-016..D-021, ADRs (split from T-013 per §7.4)
T-026	M1	frontend   	done             	P2	AC 4/4	Board 'Office' view: agents as personas working in a visual office (Chris request)
T-027	M2	researcher 	ready            	P0	AC 0/3	Lexicon generalization: held-out recall for prior-history, hedges, patient attribution; ADR-013 category names
T-028	M1	architect  	done             	P0	AC 4/4	ADR consistency pass: D-022, lexicon v2 categories, confirm_date example, mg., per-record pass (split from T-014)
T-029	M2	qa         	ready            	P0	AC 0/7	Test-first unit suites for all deterministic modules (red before any backend code)
T-030	M2	backend    	ready            	P0	AC 0/5	Grounding verifier first: sentences.py, grounding.py, confidence.py, why.py
T-031	M2	db         	ready            	P0	AC 0/7	SQLite schema, helpers, ladder/audit/event tables, single purge function
T-032	M2	backend    	ready            	P0	AC 0/5	Ingest: record split, date parsing, dedupe, limits, injection scan
T-033	M2	backend    	ready            	P0	AC 0/8	Amounts, running total, gap rule, accident-date conflict, flag templates
T-034	M2	backend    	ready            	P0	AC 0/8	LLM provider (claude-cli / anthropic-api / fixture), audited retries, fixture recording
T-035	M2	backend    	ready            	P0	AC 0/7	Generator extraction + judge #1 (faithfulness) + judge #2 (amount class)
T-036	M2	backend    	ready            	P0	AC 0/10	LLM flag passes: per-record pre-existing/causation + lexicon floor, conflicts + judges #3/#4
T-037	M2	backend    	ready            	P0	AC 0/7	Pipeline stages, finalize, status, CLI and recorded fixtures for all golden inputs
T-038	M2	qa         	ready            	P0	AC 0/9	Eval runner: python -m evals.run -> evals/reports/latest.json with ship_bar_met
T-039	M3	qa         	ready            	P0	AC 0/9	Test-first export/review unit suites and E2E specs (red before build)
T-040	M3	backend    	ready            	P0	AC 0/5	FastAPI routes, demo gate, review/edit/confirm_date with re-check
T-041	M3	backend    	ready            	P0	AC 0/6	export.py: letter_text and internal_notes_text from accepted items only
T-042	M3	frontend   	ready            	P0	AC 0/7	Frontend: input, banners, timeline, Why?, rejected tray, source-record modal
T-043	M3	frontend   	ready            	P0	AC 0/7	Frontend: flags panel, charges and unclear tray, accept/dismiss controls, keyboard, 375 px
T-044	M3	frontend   	ready            	P0	AC 0/6	Frontend: entry edit with re-check warning, export view, two copy buttons, counts
T-045	M3	qa         	ready            	P0	AC 0/6	Playwright E2E: full paralegal journey, adversarial inputs, all sensors
T-046	M3	frontend   	ready            	P2	AC 0/5	Stretch (first to cut): side-by-side source viewer at >= 1024 px
T-047	M2	frontend   	in_review        	P2	AC 4/6	Office view v2: 3D office with agents moving room to room and pairing with counterparts (Chris request)
T-048	M2	qa         	ready            	P0	AC 0/2	M2 LLM-stage tests first (provider, audited, schemas, judges, flags, pipeline, conflicts, templates)
---show T-048
---
id: "T-048"
title: "M2 LLM-stage tests first (provider, audited, schemas, judges, flags, pipeline, conflicts, templates)"
milestone: "M2"
role: "qa"
status: "ready"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T01:22:47Z"
updated_at: "2026-11-02T01:22:47Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "tests/unit/test_provider.py, test_audited.py, test_schemas.py, test_judges.py, test_flags_sample.py, test_flags_injection.py, test_pipeline.py, test_conflicts.py, test_flag_templates.py exist and fail only on NotImplemented; `pytest tests/unit --collect-only` lists them", "done": false, "evidence": null}
  - {"n": 2, "text": "each test docstring cites its R-ID or LLM_VS_CODE row; fixture backend only, no key, no network", "done": false, "evidence": null}
---
## Description
From the T-018 contract review: 20 of 35 cited test files had no author. qa writes these failing tests before backend LLM-stage cards (T-034..T-037).

## Notes (append-only, newest last)

## Handoff (filled when moving to in_review)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:16.083Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-017 2>&1; echo \"---show T-018\"; python3 tools/board.py show T-018 2>&1",
 "description": "Show T-017 and T-018 cards"
}
````

### User / tool · 2026-11-02T01:23:16.252Z

**tool result**
````
---
id: "T-017"
title: "Plan M2 + M3 cards with testable acceptance criteria traced to REQUIREMENTS and LLM_VS_CODE"
milestone: "M1"
role: "orchestrator"
status: "in_review"
priority: "P0"
depends_on: ["T-013", "T-014", "T-015", "T-025", "T-028"]
created_by: "orchestrator"
created_at: "2026-11-02T00:17:08Z"
updated_at: "2026-11-02T01:23:10Z"
claimed_by: "orchestrator"
claimed_at: "2026-11-02T01:23:10Z"
rounds: 1
commits: []
reviews:
  - {"persona": "product-manager-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-017-product-manager.md", "at": "2026-11-02T01:23:10Z"}
ac:
  - {"n": 1, "text": "every R-ID in spec/REQUIREMENTS.md is covered by >=1 M2/M3 card AC", "done": true, "evidence": "docs/M2M3_COVERAGE.md: every R-ID mapped to T-029..T-046 (R-RV-7 withdrawn, R-SU-*/R-CO-4 INST/R-CO-8 assigned to M4/M5 explicitly)"}
  - {"n": 2, "text": "every row of the docs/LLM_VS_CODE.md table maps to an M2 card with its validation named in AC", "done": true, "evidence": "docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped, each card AC names its test/eval"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T00:50:27Z orchestrator: updated depends_on=['T-013', 'T-014', 'T-015', 'T-025']
- 2026-11-02T01:02:18Z orchestrator: updated depends_on=['T-013', 'T-014', 'T-015', 'T-025', 'T-028']
- 2026-11-02T01:09:12Z orchestrator: claimed
- 2026-11-02T01:09:12Z orchestrator: Drafting delegated to a sonnet Plan agent (token budget D-024): artifacts/tmp/m2m3_cards.json + m2m3_coverage.md; orchestrator reviews and loads onto the board.
- 2026-11-02T01:14:19Z orchestrator: AC 1 checked: docs/M2M3_COVERAGE.md: every R-ID mapped to T-029..T-046 (R-RV-7 withdrawn, R-SU-*/R-CO-4 INST/R-CO-8 assigned to M4/M5 explicitly)
- 2026-11-02T01:14:19Z orchestrator: AC 2 checked: docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped, each card AC names its test/eval
- 2026-11-02T01:14:19Z orchestrator: moved in_progress -> in_review
- 2026-11-02T01:14:19Z orchestrator: review dispatched: contract review (T-018)
- 2026-11-02T01:23:10Z orchestrator: review product-manager-reviewer (claude-opus-5-5): changes — reviews/T-017-product-manager.md; round 1; findings:
    - [major] Coverage counts R-ID mentions rather than pass conditions; four R-IDs are named but their REQUIREMENTS test is in no AC — fix: Add a 'pass condition -> AC n' column to M2M3_COVERAGE.md and fill it for every R-ID, using the AC edits in the T-018 paralegal review (T-044 AC1, T-043 AC1, T-042 AC2, T-041 AC3, T-039 AC2).
    - [major] Three AC contradict the golden or REQUIREMENTS, so they can't pass on a correct build — fix: Apply the exact edits in reviews/CONTRACT-M2M3-staff-engineer.md (T-039 AC1, T-033 AC1) and reviews/CONTRACT-M2M3-paralegal.md (T-039 AC2). Add a plan self-check: every number in an AC is diffed against evals/golden expected values.
    - [major] Validation is named but unowned: 20 of 35 cited test files have no qa author, and LLM_VS_CODE row 10 is mapped against the table — fix: See staff-engineer review findings 1 and 7: a qa test-first card for LLM stages, T-039 AC4 naming the E2E files, and a row 10 engine decision (T-033 AC or an ADR).
    - [major] Critical path, budget and cut order in the handoff are wrong, and ship-bar rows are not traced — fix: See PM review findings 1, 2, 5, 6: correct the chain with per-card estimates, an M2 cut order, a ship-bar trace table, and a lexicon recall metric (or a reworded row 16).
    - [minor] T-017 AC2 evidence overstates: not every LLM_VS_CODE row maps to an M2 card — fix: Reword the evidence: 'rows 1-18, 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design'.
- 2026-11-02T01:23:10Z orchestrator: claimed
- 2026-11-02T01:23:10Z orchestrator: moved in_progress -> in_review
- 2026-11-02T01:23:10Z orchestrator: review dispatched: haiku apply-check

## Handoff
Round 2: T-018 contract-review majors applied by script (artifacts/tmp/contract_fixes.json → AC additions on named cards), deps T-031/T-042/T-043 fixed, T-027 raised to P0, new qa card T-048 for unowned LLM-stage tests, coverage doc gains critical path, M2 cut order and ship-bar→card table.

---show T-018
---
id: "T-018"
title: "Milestone contract review (PM + paralegal + staff-engineer) of M2/M3 AC and the LLM/code table; apply edits"
milestone: "M1"
role: "orchestrator"
status: "in_review"
priority: "P0"
depends_on: ["T-016", "T-017"]
created_by: "orchestrator"
created_at: "2026-11-02T00:17:08Z"
updated_at: "2026-11-02T01:23:11Z"
claimed_by: "orchestrator"
claimed_at: "2026-11-02T01:14:19Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "reviews/CONTRACT-M2M3-{product-manager,paralegal,staff-engineer}.md exist", "done": true, "evidence": "reviews/CONTRACT-M2M3-{product-manager,paralegal,staff-engineer}.md"}
  - {"n": 2, "text": "every blocker/major finding is applied as an AC edit/new card or rejected with a recorded reason in reviews/GATE-M1-summary.md", "done": true, "evidence": "every blocker/major applied as AC edit/new card (artifacts/tmp/contract_fixes.json); verified by reviews/T-018-product-manager.md"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T01:14:19Z orchestrator: claimed
- 2026-11-02T01:23:11Z orchestrator: AC 1 checked: reviews/CONTRACT-M2M3-{product-manager,paralegal,staff-engineer}.md
- 2026-11-02T01:23:11Z orchestrator: AC 2 checked: every blocker/major applied as AC edit/new card (artifacts/tmp/contract_fixes.json); verified by reviews/T-018-product-manager.md
- 2026-11-02T01:23:11Z orchestrator: moved in_progress -> in_review
- 2026-11-02T01:23:11Z orchestrator: review dispatched: haiku apply-check

## Handoff
Contract review ran as one opus agent covering PM, paralegal and staff-engineer lenses (D-024). 0 blockers; ~23 majors applied as AC edits/deps/new card T-048 before any M2 claim.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:41.212Z

**tool call — Bash**
````
{
 "command": "cat -n docs/M2M3_COVERAGE.md; echo \"--- fixes json\"; ls -la artifacts/tmp/ 2>&1; cat artifacts/tmp/contract_fixes.json 2>&1 | head -c 6000; echo; echo \"--- probe dir\"; ls -la artifacts/review-evidence/ 2>&1",
 "description": "Read coverage doc, contract fixes file, and evidence dir"
}
````

### User / tool · 2026-11-02T01:23:41.317Z

**tool result**
````
     1	# M2 + M3 coverage (T-017, revised after T-018 contract review)
     2	
     3	## Critical path and cut order (orchestrator)
     4	- M2 critical path (7 cards): T-029/T-048 (tests first) → T-032 ingest → T-033 amounts/gaps → T-035 generator+judges → T-036 LLM flags → T-037 pipeline+fixtures → T-038 eval runner. Estimates ~30–45 min each with 4 workers in parallel (T-030 grounding, T-031 db, T-034 provider, T-027 lexicon run beside the chain).
     5	- M2 cut order (never touches ship-bar items): (1) anthropic-api backend stays mocked-SDK only; (2) judge #4 merged into judge #3 prompt; (3) lexicon held-out target lowered from 85% to "reported" (T-027) with debt.
     6	- M3 cut order: T-046 side-by-side → excerpt re-selection → notes sections 7–8 → R-RV-9 highlight (REQUIREMENTS §4).
     7	
     8	## Ship bar row → card
     9	| Ship bar | Card |
    10	|---|---|
    11	| 1 Grounding | T-038 (grounding_rate), T-041 (export grounding) |
    12	| 2 Recall | T-038 |
    13	| 3 Flags (incl. 28/73) | T-038, T-033 |
    14	| 4 No invented facts (live backend only) | T-038, T-037 |
    15	| 5 Reviewability (verify_quickly ≥ 4; E2E) | T-045 + M3 gate paralegal review |
    16	
    17	Card keys are in m2m3_cards.json. "Primary" is listed first. T-027 (existing lexicon card) is a dependency of T-036 (m2-be-llm-flags), not duplicated.
    18	Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 (m2-be-grounding) -> T-035 (m2-be-generator-judges) -> T-037 (m2-be-pipeline-cli) -> T-038 (m2-qa-eval-runner) (T-036 (m2-be-llm-flags) runs beside the generator).
    19	This runs about 4 h, over the 3.5 h budget. If it slips, cut in this order: T-046 (m3-fe-side-by-side), then the other items in the REQUIREMENTS section 4 cut order.
    20	
    21	## R-ID -> card
    22	| R-ID | Cards |
    23	|---|---|
    24	| R-IN-1 | T-032 (m2-be-ingest-dates), T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
    25	| R-IN-2 | T-042 (m3-fe-input-timeline), T-039 (m3-qa-tests-first) |
    26	| R-IN-3 | T-032 (m2-be-ingest-dates), T-038 (m2-qa-eval-runner) |
    27	| R-IN-4 | T-032 (m2-be-ingest-dates), T-040 (m3-be-api-review), T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
    28	| R-IN-5 | T-032 (m2-be-ingest-dates), T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review) |
    29	| R-TL-1 | T-035 (m2-be-generator-judges), T-038 (m2-qa-eval-runner), T-042 (m3-fe-input-timeline) |
    30	| R-TL-2 | T-030 (m2-be-grounding), T-029 (m2-qa-unit-first) |
    31	| R-TL-3 | T-032 (m2-be-ingest-dates), T-035 (m2-be-generator-judges) |
    32	| R-TL-4 | T-035 (m2-be-generator-judges), T-038 (m2-qa-eval-runner) |
    33	| R-TL-5 | T-030 (m2-be-grounding), T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
    34	| R-TL-6 | T-040 (m3-be-api-review), T-042 (m3-fe-input-timeline) |
    35	| R-TL-7 | T-032 (m2-be-ingest-dates), T-038 (m2-qa-eval-runner) |
    36	| R-TL-8 | T-030 (m2-be-grounding), T-044 (m3-fe-edit-export) |
    37	| R-TL-9 | T-032 (m2-be-ingest-dates), T-035 (m2-be-generator-judges) |
    38	| R-TL-10 | T-030 (m2-be-grounding), T-040 (m3-be-api-review) |
    39	| R-FL-1 | T-033 (m2-be-amounts-gaps), T-038 (m2-qa-eval-runner) |
    40	| R-FL-2 | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
    41	| R-FL-3 | T-036 (m2-be-llm-flags) |
    42	| R-FL-4 | T-036 (m2-be-llm-flags), T-038 (m2-qa-eval-runner) |
    43	| R-FL-5 | T-030 (m2-be-grounding), T-036 (m2-be-llm-flags) |
    44	| R-FL-6 | T-043 (m3-fe-flags-charges-review) |
    45	| R-FL-7 | T-036 (m2-be-llm-flags), T-043 (m3-fe-flags-charges-review) |
    46	| R-FL-8 | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
    47	| R-CH-1 | T-033 (m2-be-amounts-gaps), T-038 (m2-qa-eval-runner) |
    48	| R-CH-2 | T-033 (m2-be-amounts-gaps), T-035 (m2-be-generator-judges) |
    49	| R-CH-3 | T-033 (m2-be-amounts-gaps), T-043 (m3-fe-flags-charges-review), T-041 (m3-be-export) |
    50	| R-CH-4 | T-033 (m2-be-amounts-gaps), T-038 (m2-qa-eval-runner) |
    51	| R-CH-5 | T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review), T-039 (m3-qa-tests-first) |
    52	| R-CH-6 | T-033 (m2-be-amounts-gaps) |
    53	| R-CH-7 | T-040 (m3-be-api-review), T-039 (m3-qa-tests-first) |
    54	| R-RV-1 | T-043 (m3-fe-flags-charges-review), T-045 (m3-qa-e2e-journey) |
    55	| R-RV-2 | T-040 (m3-be-api-review), T-044 (m3-fe-edit-export), T-039 (m3-qa-tests-first) |
    56	| R-RV-3 | T-040 (m3-be-api-review), T-044 (m3-fe-edit-export) |
    57	| R-RV-4 | T-043 (m3-fe-flags-charges-review), T-045 (m3-qa-e2e-journey) |
    58	| R-RV-5 | T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review) |
    59	| R-RV-6 | T-032 (m2-be-ingest-dates), T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags), T-038 (m2-qa-eval-runner), T-045 (m3-qa-e2e-journey) |
    60	| R-RV-7 | withdrawn (D-011); no card |
    61	| R-RV-8 | T-031 (m2-db-schema), T-040 (m3-be-api-review), T-043 (m3-fe-flags-charges-review) |
    62	| R-RV-9 | T-030 (m2-be-grounding), T-042 (m3-fe-input-timeline), T-043 (m3-fe-flags-charges-review) |
    63	| R-EX-1 | T-041 (m3-be-export), T-045 (m3-qa-e2e-journey) |
    64	| R-EX-2 | T-041 (m3-be-export), T-038 (m2-qa-eval-runner) |
    65	| R-EX-3 | T-041 (m3-be-export) |
    66	| R-EX-4 | T-041 (m3-be-export) |
    67	| R-EX-5 | T-044 (m3-fe-edit-export) |
    68	| R-EX-6 | T-041 (m3-be-export), T-044 (m3-fe-edit-export), T-038 (m2-qa-eval-runner) (spec = golden check) |
    69	| R-EX-7 | T-041 (m3-be-export), T-044 (m3-fe-edit-export) |
    70	| R-EX-8 | T-041 (m3-be-export) |
    71	| R-EX-9 | T-044 (m3-fe-edit-export) |
    72	| R-CO-1 | T-029 (m2-qa-unit-first) (boundary test), T-041 (m3-be-export) |
    73	| R-CO-2 | T-031 (m2-db-schema), T-037 (m2-be-pipeline-cli), T-045 (m3-qa-e2e-journey) |
    74	| R-CO-3 | T-038 (m2-qa-eval-runner) |
    75	| R-CO-4 | T-040 (m3-be-api-review) (demo gate). INST half is M4 (non-goal for M2/M3) |
    76	| R-CO-5 | T-042 (m3-fe-input-timeline), T-045 (m3-qa-e2e-journey) |
    77	| R-CO-6 | T-034 (m2-be-provider-fixtures) |
    78	| R-CO-7 | T-038 (m2-qa-eval-runner) |
    79	| R-CO-8 | non-goal for M2/M3 cards: orchestrator logs SCOPE_CUTS; T-046 (m3-fe-side-by-side) AC logs R-ST-1 |
    80	| R-CO-9 | T-034 (m2-be-provider-fixtures) |
    81	| R-SU-1 .. R-SU-5 | non-goal for M2/M3: M4/M5 submission cards |
    82	| R-ST-1 | T-046 (m3-fe-side-by-side) |
    83	
    84	## LLM_VS_CODE row -> card
    85	| Row | Step | Cards |
    86	|---|---|---|
    87	| 1 | Split, merge duplicates | T-032 (m2-be-ingest-dates) |
    88	| 2 | Date parsing | T-032 (m2-be-ingest-dates) |
    89	| 3 | Date and provider by code | T-032 (m2-be-ingest-dates) |
    90	| 4 | Generator + rungs 1-2 | T-035 (m2-be-generator-judges), T-030 (m2-be-grounding) |
    91	| 5 | Clinical facts list: not built | T-035 (m2-be-generator-judges) (schema test enforces the omission) |
    92	| 6 | Find every amount | T-033 (m2-be-amounts-gaps) |
    93	| 7 | Amount class | T-033 (m2-be-amounts-gaps) (rules), T-035 (m2-be-generator-judges) (judge #2) |
    94	| 8 | Running total | T-033 (m2-be-amounts-gaps), T-041 (m3-be-export), T-043 (m3-fe-flags-charges-review) |
    95	| 9 | Gap > 30 days | T-033 (m2-be-amounts-gaps), T-037 (m2-be-pipeline-cli) |
    96	| 10 | Structural conflicts | T-033 (m2-be-amounts-gaps) (accident date), T-036 (m2-be-llm-flags) (provider variants) |
    97	| 11 | Semantic conflicts + judge #3 | T-036 (m2-be-llm-flags) |
    98	| 12 | Pre-existing | T-036 (m2-be-llm-flags) |
    99	| 13 | Causation language | T-036 (m2-be-llm-flags) |
   100	| 14 | Flag wording by code | T-033 (m2-be-amounts-gaps), T-036 (m2-be-llm-flags) |
   101	| 15 | Numbers in summary/edit | T-030 (m2-be-grounding), T-040 (m3-be-api-review) |
   102	| 16 | Injection scan | T-032 (m2-be-ingest-dates), T-036 (m2-be-llm-flags), T-038 (m2-qa-eval-runner) |
   103	| 17 | Confidence state | T-030 (m2-be-grounding) |
   104	| 18 | Why? sentence | T-030 (m2-be-grounding), T-042 (m3-fe-input-timeline) |
   105	| 19 | Sort, filter, export | T-041 (m3-be-export), T-045 (m3-qa-e2e-journey) |
   106	| 20 | Audit trail | T-031 (m2-db-schema), T-034 (m2-be-provider-fixtures), T-037 (m2-be-pipeline-cli) |
   107	
   108	Unmapped: none.--- fixes json
total 896
drwxr-xr-x@ 10 arsis  staff     320 Nov  1 19:22 .
drwxr-xr-x@  6 arsis  staff     192 Nov  1 18:20 ..
-rw-r--r--@  1 arsis  staff    6782 Nov  1 19:22 contract_fixes.json
drwxr-xr-x@ 10 arsis  staff     320 Nov  1 18:56 handoff
-rw-r--r--@  1 arsis  staff   28298 Nov  1 19:14 m2m3_cards.json
-rw-r--r--@  1 arsis  staff    5154 Nov  1 19:14 m2m3_coverage.md
-rw-r--r--@  1 arsis  staff     551 Nov  1 19:14 m2m3_ids.json
drwxr-xr-x@ 19 arsis  staff     608 Nov  1 18:19 plog
-rw-r--r--@  1 arsis  staff  405492 Nov  1 18:45 r3check.png
-rw-r--r--@  1 arsis  staff     659 Nov  1 18:32 xss_check.py
[
 {
  "src": "manag",
  "cards": [
   "T-027",
   "T-031",
   "T-034",
   "T-036"
  ],
  "fix": "Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md."
 },
 {
  "src": "manag",
  "cards": [
   "T-027",
   "T-036",
   "T-038"
  ],
  "fix": "Either raise T-027 to P0 with a timebox in its Description, or remove T-027 from T-036 depends_on and add a T-036 AC: 'runs against app/llm/lexicon.yaml at HEAD; lexicon recall per must-flag is reported by evals.run (see T-038 finding)'."
 },
 {
  "src": "manag",
  "cards": [
   "T-037",
   "T-038",
   "T-045"
  ],
  "fix": "T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BACKEND != fixture; latest.json records backend and model ids; ship_bar_met is false when backend == fixture'. T-037 AC2: 'fixtures recorded for sample, case_01..09, every line of hallucinations.jsonl and hallucinations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_bar_met true; report path in handoff'."
 },
 {
  "src": "manag",
  "cards": [
   "T-035",
   "T-036",
   "T-038"
  ],
  "fix": "T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml; `python -m evals.run --check-fresh` exits 1 when any current hash differs'. T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'."
 },
 {
  "src": "manag",
  "cards": [
   "T-038",
   "T-045"
  ],
  "fix": "Add a 'Ship bar row -> card' table to M2M3_COVERAGE.md (rows 1-4 -> T-038, row 5 -> T-045 + M3 gate). New orchestrator card (M3): 'paralegal-reviewer agent body and M3 gate brief request scores.verify_quickly 1-5 (D-015)'."
 },
 {
  "src": "manag",
  "cards": [
   "T-038"
  ],
  "fix": "T-038 AC1: add `lexicon_recall_must_flags` (pre_existing + causation, per golden case, pooled) with R-IDs R-FL-3, R-RV-6, and state the threshold in REQUIREMENTS \u00a77 by ADR, or edit LLM_VS_CODE rows 12/16 to 'reported, not gated'."
 },
 {
  "src": "paral",
  "cards": [
   "T-039",
   "T-044"
  ],
  "fix": "T-044 AC1 append: 'reload -> edited summary and \"edited\" label persist; export notes list record 3 under EDITED ITEMS with original and new text'. T-039 AC2 append: 'test_export::test_edited_items_section with entry 3 edited lists both texts and any keep-my-wording confirmation'."
 },
 {
  "src": "paral",
  "cards": [
   "T-039"
  ],
  "fix": "T-039 AC2: 'dismissing entry 5 and leaving entry 6 pending gives \"Record 5 ... dismissed\", \"Record 6 ... not reviewed\" and 7 of 9'."
 },
 {
  "src": "paral",
  "cards": [
   "T-043"
  ],
  "fix": "T-043 AC1 append: 'the accident-date conflict card shows \"Date of accident per intake form: 2026-01-19.\" and the 2026-01-09 header line(s) of records 1 and 2 side by side, and contains none of \"resolved\", \"correct date\", \"delay\"'."
 },
 {
  "src": "paral",
  "cards": [
   "T-041",
   "T-042"
  ],
  "fix": "T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 \"could not process\" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECORDS NOT IN THE TREATMENT SECTION with reason \"could not process\"'."
 },
 {
  "src": "engin",
  "cards": [
   "T-029",
   "T-034",
   "T-037",
   "T-039"
  ],
  "fix": "T-029 AC4 or a new qa card 'M2 LLM-stage tests first' (deps [], blocks T-034..T-037): write test_provider, test_audited, test_schemas, test_judges, test_flags_sample, test_flags_injection, test_pipeline, test_conflicts, test_flag_templates red. T-039 AC4: name test_api.py plus the 10 E2E files above, by file."
 },
 {
  "src": "engin",
  "cards": [
   "T-029",
   "T-031",
   "T-039",
   "T-040",
   "T-042",
   "T-043",
   "T-045"
  ],
  "fix": "T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045."
 },
 {
  "src": "engin",
  "cards": [
   "T-034"
  ],
  "fix": "T-034 AC4 append: 'anthropic-api client is constructed with max_retries=0 and an explicit timeout (<= 120 s); test_provider::test_sdk_no_internal_retry asserts both on the constructed client'."
 },
 {
  "src": "engin",
  "cards": [
   "T-034",
   "T-037"
  ],
  "fix": "T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash); the audited wrapper turns it into LLM_FAILED_AFTER_RETRIES; never a default answer'. T-037 AC2 replace with: 'replaying sample, case_01..09, hallucinations(.jsonl, _controls) and SE1-SE5 on fixture reports 0 FixtureMissing (count printed)'."
 },
 {
  "src": "engin",
  "cards": [
   "T-035",
   "T-036"
  ],
  "fix": "T-035 AC4 append: 'judge #2 unsure, error or timeout -> needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a charge is verified only on agrees'. T-036 AC5 append: 'judge #3/#4 error or timeout -> needs_review JUDGE_UNAVAILABLE'."
 },
 {
  "src": "engin",
  "cards": [
   "T-029"
  ],
  "fix": "T-029 AC4: module list = sentences, grounding, confidence, why, dates, ingest/dedupe, amounts (find + classify), totals, gaps, conflicts (accident date), flag_templates, injection scan, export; scan transitive imports, not just direct ones."
 },
 {
  "src": "engin",
  "cards": [
   "T-033",
   "T-036"
  ],
  "fix": "Either T-033 gains AC6 'case_05 provider conflict raised by code (normalized-name rule), no LLM call', or an ADR edits row 10 and T-036 AC3 says 'raised by the LLM conflict pass + judge #3'. T-036 AC2 append 'exactly one accident-date conflict flag in pipeline output (from T-033)'."
 },
 {
  "src": "engin",
  "cards":
--- probe dir
total 10360
drwxr-xr-x@ 191 arsis  staff    6112 Nov  1 19:22 .
drwxr-xr-x@   6 arsis  staff     192 Nov  1 18:20 ..
-rw-r--r--@   1 arsis  staff    5624 Nov  1 18:41 M0-r2-staff-resolution.md
-rw-r--r--@   1 arsis  staff    3998 Nov  1 18:17 T-001-exercise-1.txt
-rw-r--r--@   1 arsis  staff    4574 Nov  1 18:17 T-001-exercise-2.txt
-rw-r--r--@   1 arsis  staff    2738 Nov  1 18:23 T-001-exercise-3.txt
-rw-r--r--@   1 arsis  staff    3536 Nov  1 18:37 T-001-r2-readonly-repros.txt
-rw-r--r--@   1 arsis  staff    5099 Nov  1 18:59 T-001-r3-repro.out.txt
-rw-r--r--@   1 arsis  staff    4156 Nov  1 18:59 T-001-r3-repro.sh
-rw-r--r--@   1 arsis  staff   13729 Nov  1 18:22 T-002-curl.txt
-rw-r--r--@   1 arsis  staff  118831 Nov  1 18:42 T-002-r2-activity-390.png
-rw-r--r--@   1 arsis  staff   82140 Nov  1 18:42 T-002-r2-board-390.png
-rw-r--r--@   1 arsis  staff    1300 Nov  1 18:42 T-002-r2-csrf-curl.txt
-rw-r--r--@   1 arsis  staff   73730 Nov  1 18:42 T-002-r2-inbox-390.png
-rw-r--r--@   1 arsis  staff   80417 Nov  1 18:42 T-002-r2-milestones-390.png
-rw-r--r--@   1 arsis  staff   92057 Nov  1 18:42 T-002-r2-personas-390.png
-rw-r--r--@   1 arsis  staff   40406 Nov  1 18:42 T-002-r2-state-390.png
-rw-r--r--@   1 arsis  staff    1126 Nov  1 18:42 T-002-r2-xss.json
-rw-r--r--@   1 arsis  staff     488 Nov  1 19:00 T-002-r3-404.py
-rw-r--r--@   1 arsis  staff  116259 Nov  1 19:00 T-002-r3-activity-390.png
-rw-r--r--@   1 arsis  staff   80919 Nov  1 19:00 T-002-r3-board-390.png
-rw-r--r--@   1 arsis  staff   72782 Nov  1 19:00 T-002-r3-inbox-390.png
-rw-r--r--@   1 arsis  staff   80730 Nov  1 19:00 T-002-r3-milestones-390.png
-rw-r--r--@   1 arsis  staff   89842 Nov  1 19:00 T-002-r3-personas-390.png
-rw-r--r--@   1 arsis  staff    2910 Nov  1 19:00 T-002-r3-probe.out.txt
-rw-r--r--@   1 arsis  staff    3551 Nov  1 19:00 T-002-r3-probe.py
-rw-r--r--@   1 arsis  staff   97954 Nov  1 19:00 T-002-r3-state-390.png
-rw-r--r--@   1 arsis  staff    2132 Nov  1 19:00 T-002-r3-ui.out.txt
-rw-r--r--@   1 arsis  staff    1940 Nov  1 19:00 T-002-r3-ui.py
-rw-r--r--@   1 arsis  staff    1353 Nov  1 18:20 T-003-git-guard-commit-secret-probe.txt
-rw-r--r--@   1 arsis  staff   11736 Nov  1 18:17 T-003-git-guard-probe.txt
-rw-r--r--@   1 arsis  staff    5500 Nov  1 18:20 T-003-other-hooks-probe.txt
-rw-r--r--@   1 arsis  staff    1282 Nov  1 18:49 T-003-r2-commit-secret-probe.out.txt
-rw-r--r--@   1 arsis  staff    1792 Nov  1 18:49 T-003-r2-commit-secret-probe.py
-rw-r--r--@   1 arsis  staff   40696 Nov  1 18:39 T-003-r2-git-guard-results.txt
-rw-r--r--@   1 arsis  staff    8293 Nov  1 18:46 T-003-r2-probe-board2.out.txt
-rw-r--r--@   1 arsis  staff    6606 Nov  1 18:46 T-003-r2-probe-board2.py
-rw-r--r--@   1 arsis  staff   11627 Nov  1 18:39 T-003-r2-probe-corpus.txt
-rw-r--r--@   1 arsis  staff   24234 Nov  1 18:41 T-003-r2-probe-direct.out.txt
-rw-r--r--@   1 arsis  staff   24508 Nov  1 18:45 T-003-r2-probe-direct.out2.txt
-rw-r--r--@   1 arsis  staff   15783 Nov  1 18:41 T-003-r2-probe-direct.py
-rw-r--r--@   1 arsis  staff    8293 Nov  1 18:57 T-003-r3-probe-board2.out.txt
-rw-r--r--@   1 arsis  staff    9820 Nov  1 19:05 T-003-r3-probe-corpus.out.txt
-rw-r--r--@   1 arsis  staff    2129 Nov  1 18:56 T-003-r3-probe-corpus.py
-rw-r--r--@   1 arsis  staff   26955 Nov  1 19:06 T-003-r3-probe-direct.out.txt
-rw-r--r--@   1 arsis  staff     769 Nov  1 19:02 T-003-r3-probe-legit.out.txt
-rw-r--r--@   1 arsis  staff    3257 Nov  1 19:02 T-003-r3-probe-legit.py
-rw-r--r--@   1 arsis  staff     437 Nov  1 19:08 T-003-r3-probe-pwd.out.txt
-rw-r--r--@   1 arsis  staff     737 Nov  1 19:08 T-003-r3-probe-pwd.py
-rw-r--r--@   1 arsis  staff    5004 Nov  1 19:01 T-003-r3-probe-rwg.out.txt
-rw-r--r--@   1 arsis  staff    4720 Nov  1 19:01 T-003-r3-probe-rwg.py
-rw-r--r--@   1 arsis  staff   32357 Nov  1 19:06 T-003-r3-probe-targeted.out.txt
-rw-r--r--@   1 arsis  staff   17211 Nov  1 18:58 T-003-r3-probe-targeted.py
-rw-r--r--@   1 arsis  staff   22381 Nov  1 19:06 T-003-r3-probe-targeted2.out.txt
-rw-r--r--@   1 arsis  staff   13423 Nov  1 19:00 T-003-r3-probe-targeted2.py
-rw-r--r--@   1 arsis  staff     783 Nov  1 18:18 T-003-reviewer-write-guard-probe.txt
-rw-r--r--@   1 arsis  staff    3252 Nov  1 18:21 T-004-agent-check.txt
-rw-r--r--@   1 arsis  staff    1296 Nov  1 18:38 T-004-r2-agent-sync.txt
-rw-r--r--@   1 arsis  staff    2556 Nov  1 18:37 T-004-r2-board-guard-probe.py
-rw-r--r--@   1 arsis  staff    1985 Nov  1 18:37 T-004-r2-board-guard-probe.txt
-rw-r--r--@   1 arsis  staff     400 Nov  1 18:40 T-004-r2-shell-write-probe.txt
-rw-r--r--@   1 arsis  staff    4166 Nov  1 19:02 T-004-r3-board-guard-probe.out.txt
-rw-r--r--@   1 arsis  staff    4705 Nov  1 19:02 T-004-r3-board-guard-probe.py
-rw-r--r--@   1 arsis  staff    1269 Nov  1 18:36 T-005-r2-pathcheck.py
-rw-r--r--@   1 arsis  staff    3479 Nov  1 18:19 T-006-check-secrets-probe.txt
-rw-r--r--@   1 arsis  staff     457 Nov  1 18:46 T-006-r2-chain-probe.out.txt
-rw-r--r--@   1 arsis  staff    1299 Nov  1 18:46 T-006-r2-chain-probe.py
-rw-r--r--@   1 arsis  staff    1076 Nov  1 18:47 T-006-r2-fp-probe.out.txt
-rw-r--r--@   1 arsis  staff    1679 Nov  1 18:47 T-006-r2-fp-probe.py
-rw-r--r--@   1 arsis  staff   14186 Nov  1 18:44 T-006-r2-probe.out.txt
-rw-r--r--@   1 arsis  staff   12661 Nov  1 18:44 T-006-r2-probe.py
-rw-r--r--@   1 arsis  staff     652 Nov  1 19:02 T-006-r3-chain-probe.out.txt
-rw-r--r--@   1 arsis  staff     323 Nov  1 19:03 T-006-r3-commit-paths-probe.out.txt
-rw-r--r--@   1 arsis  staff    2170 Nov  1 19:03 T-006-r3-commit-paths-probe.py
-rw-r--r--@   1 arsis  staff    1076 Nov  1 19:02 T-006-r3-fp-probe.out.txt
-rw-r--r--@   1 arsis  staff   14411 Nov  1 19:02 T-006-r3-probe.out.txt
-rw-r--r--@   1 arsis  staff     266 Nov  1 18:21 T-006-rename-probe.txt
-rw-r--r--@   1 arsis  staff    3095 Nov  1 18:36 T-008-adjuster-source-checks.txt
-rw-r--r--@   1 arsis  staff    5000 Nov  1 18:53 T-008-r2-adjuster.md
drwxr-xr-x@   6 arsis  staff     192 Nov  1 18:52 T-008-r2-src
-rw-r--r--@   1 arsis  staff    4018 Nov  1 18:58 T-008-r3-adjuster-greps.txt
-rw-r--r--@   1 arsis  staff    4470 Nov  1 18:59 T-008-r3-adjuster-hits.md
-rw-r--r--@   1 arsis  staff  103085 Nov  1 18:58 T-008-r3-insurancejournal-854959.html
-rw-r--r--@   1 arsis  staff    5686 Nov  1 18:58 T-008-r3-insurancejournal-checks.txt
-rw-r--r--@   1 arsis  staff    7118 Nov  1 18:33 T-009-adjuster-probes.py
-rw-r--r--@   1 arsis  staff    7919 Nov  1 18:33 T-009-adjuster-probes.txt
-rw-r--r--@   1 arsis  staff    3506 Nov  1 18:34 T-009-nurse-golden-scan.txt
-rw-r--r--@   1 arsis  staff   10773 Nov  1 18:34 T-009-nurse-probe-output.txt
-rw-r--r--@   1 arsis  staff    1912 Nov  1 18:34 T-009-nurse-probe.py
-rw-r--r--@   1 arsis  staff    5508 Nov  1 18:34 T-009-nurse-probes.txt
-rw-r--r--@   1 arsis  staff   27892 Nov  1 18:55 T-009-r2-nurse-probe-output.txt
-rw-r--r--@   1 arsis  staff    9224 Nov  1 18:55 T-009-r2-nurse-probe.py
-rw-r--r--@   1 arsis  staff    2111 Nov  1 18:56 T-009-r2-nurse-variants-output.txt
-rw-r--r--@   1 arsis  staff    2729 Nov  1 18:56 T-009-r2-nurse-variants.py
-rw-r--r--@   1 arsis  staff    8083 Nov  1 18:58 T-009-r2-resolution.md
-rw-r--r--@   1 arsis  staff   17929 Nov  1 18:32 T-010-011-sections.txt
-rw-r--r--@   1 arsis  staff   11927 Nov  1 18:41 T-010-011-source-check.md
-rw-r--r--@   1 arsis  staff   10370 Nov  1 18:36 T-010-litlead-source-check.md
-rw-r--r--@   1 arsis  staff    1134 Nov  1 18:45 T-010-r2-count.py
-rw-r--r--@   1 arsis  staff    9595 Nov  1 18:46 T-010-r2-resolution.md
-rw-r--r--@   1 arsis  staff     601 Nov  1 18:43 T-010-r2-srch.py
-rw-r--r--@   1 arsis  staff    2065 Nov  1 18:52 T-010-r3-check.py
-rw-r--r--@   1 arsis  staff    4370 Nov  1 18:53 T-010-r3-resolution.md
-rw-r--r--@   1 arsis  staff    1898 Nov  1 18:38 T-011-r2-check.py
-rw-r--r--@   1 arsis  staff     958 Nov  1 18:32 T-012-h2t.py
-rw-r--r--@   1 arsis  staff    1886 Nov  1 18:52 T-012-r2-fetch.py
-rw-r--r--@   1 arsis  staff    4598 Nov  1 18:55 T-012-r2-resolution.md
-rw-r--r--@   1 arsis  staff    7818 Nov  1 18:35 T-012-source-check.md
-rw-r--r--@   1 arsis  staff   12757 Nov  1 18:23 T-013-paralegal-walkthrough.md
-rw-r--r--@   1 arsis  staff     710 Nov  1 18:34 T-013-r2-paralegal-jsoncheck.py
-rw-r--r--@   1 arsis  staff    4411 Nov  1 18:31 T-013-r2-paralegal-walk.out.txt
-rw-r--r--@   1 arsis  staff    4557 Nov  1 18:31 T-013-r2-paralegal-walk.py
-rw-r--r--@   1 arsis  staff    6010 Nov  1 18:33 T-013-r2-resolution.md
-rw-r--r--@   1 arsis  staff     667 Nov  1 18:44 T-013-r3-paralegal-golden-cmp.out.txt
-rw-r--r--@   1 arsis  staff    1583 Nov  1 18:44 T-013-r3-paralegal-golden-cmp.py
-rw-r--r--@   1 arsis  staff     824 Nov  1 18:46 T-013-r3-paralegal-jsoncheck.py
-rw-r--r--@   1 arsis  staff    4221 Nov  1 18:44 T-013-r3-paralegal-walk.out.txt
-rw-r--r--@   1 arsis  staff    8007 Nov  1 18:44 T-013-r3-paralegal-walk.py
-rw-r--r--@   1 arsis  staff    2857 Nov  1 18:45 T-013-r3-resolution.md
-rw-r--r--@   1 arsis  staff    2868 Nov  1 18:44 T-013-r3check.py
-rw-r--r--@   1 arsis  staff   23496 Nov  1 18:46 T-013-trace.md
-rw-r--r--@   1 arsis  staff    1235 Nov  1 18:27 T-014-amount-cue-demo.py
-rw-r--r--@   1 arsis  staff    6372 Nov  1 18:28 T-014-injection-trace.md
-rw-r--r--@   1 arsis  staff     376 Nov  1 18:23 T-014-json-check.out
-rw-r--r--@   1 arsis  staff     793 Nov  1 18:23 T-014-json-check.py
-rw-r--r--@   1 arsis  staff    7761 Nov  1 18:43 T-014-r2-amount-demo.py
-rw-r--r--@   1 arsis  staff    1371 Nov  1 18:46 T-014-r2-amount-sim.out
-rw-r--r--@   1 arsis  staff    1738 Nov  1 18:46 T-014-r2-amount-sim.py
-rw-r--r--@   1 arsis  staff     317 Nov  1 18:46 T-014-r2-json-check.out
-rw-r--r--@   1 arsis  staff    1522 Nov  1 18:46 T-014-r2-offset-check.out
-rw-r--r--@   1 arsis  staff    1351 Nov  1 18:46 T-014-r2-offset-check.py
-rw-r--r--@   1 arsis  staff   10089 Nov  1 18:45 T-014-r2-privacy-resolution.md
-rw-r--r--@   1 arsis  staff    6747 Nov  1 18:47 T-014-r2-staff-resolution.md
-rw-r--r--@   1 arsis  staff    3549 Nov  1 18:56 T-014-r3-amount-demo.out
-rw-r--r--@   1 arsis  staff    5551 Nov  1 18:56 T-014-r3-amount-demo.py
-rw-r--r--@   1 arsis  staff    1313 Nov  1 18:56 T-014-r3-amount-sim.out
-rw-r--r--@   1 arsis  staff    3719 Nov  1 18:56 T-014-r3-amount-sim.py
-rw-r--r--@   1 arsis  staff    9266 Nov  1 18:59 T-014-r3-resolution.md
-rw-r--r--@   1 arsis  staff    6710 Nov  1 18:26 T-014-walkthrough.md
-rw-r--r--@   1 arsis  staff   10226 Nov  1 18:29 T-015-legal-nurse-items.md
-rw-r--r--@   1 arsis  staff    7988 Nov  1 18:27 T-015-paralegal-blind.md
-rw-r--r--@   1 arsis  staff    1484 Nov  1 18:30 T-015-paralegal-regex-probe.out.txt
-rw-r--r--@   1 arsis  staff    2319 Nov  1 18:30 T-015-paralegal-regex-probe.py
-rw-r--r--@   1 arsis  staff    8869 Nov  1 18:47 T-015-r2-nurse-probe.out.txt
-rw-r--r--@   1 arsis  staff   10444 Nov  1 18:47 T-015-r2-nurse-probe.py
-rw-r--r--@   1 arsis  staff   10177 Nov  1 18:49 T-015-r2-nurse.md
-rw-r--r--@   1 arsis  staff     632 Nov  1 18:48 T-015-r2-paralegal-jsoncheck.py
-rw-r--r--@   1 arsis  staff   13119 Nov  1 18:45 T-015-r2-paralegal-probe.out.txt
-rw-r--r--@   1 arsis  staff    8982 Nov  1 18:45 T-015-r2-paralegal-probe.py
-rw-r--r--@   1 arsis  staff    3370 Nov  1 18:47 T-015-r2-paralegal.md
-rw-r--r--@   1 arsis  staff    3417 Nov  1 18:58 T-015-r3-paralegal-entries.out.txt
-rw-r--r--@   1 arsis  staff    1547 Nov  1 18:58 T-015-r3-paralegal-entries.py
-rw-r--r--@   1 arsis  staff     789 Nov  1 19:03 T-015-r3-paralegal-jsoncheck.py
-rw-r--r--@   1 arsis  staff     649 Nov  1 19:00 T-015-r3-paralegal-mutation.out.txt
-rw-r--r--@   1 arsis  staff    1145 Nov  1 19:00 T-015-r3-paralegal-mutation.py
-rw-r--r--@   1 arsis  staff    8956 Nov  1 19:00 T-015-r3-paralegal-probe.out.txt
-rw-r--r--@   1 arsis  staff    8196 Nov  1 19:00 T-015-r3-paralegal-probe.py
-rw-r--r--@   1 arsis  staff    9429 Nov  1 18:57 T-015-r3-paralegal-rerun-of-r2-probe.out.txt
-rw-r--r--@   1 arsis  staff    2288 Nov  1 18:58 T-015-r3-paralegal-s6diff.out.txt
-rw-r--r--@   1 arsis  staff     772 Nov  1 18:58 T-015-r3-paralegal-s6diff.py
-rw-r--r--@   1 arsis  staff    9710 Nov  1 18:59 T-015-r3-rerun-of-r2-nurse-probe.out.txt
-rw-r--r--@   1 arsis  staff     194 Nov  1 19:08 T-015-r4-paralegal-jsoncheck.out.txt
-rw-r--r--@   1 arsis  staff    1125 Nov  1 19:08 T-015-r4-paralegal-jsoncheck.py
-rw-r--r--@   1 arsis  staff    2130 Nov  1 19:07 T-015-r4-paralegal-recheck.out.txt
-rw-r--r--@   1 arsis  staff    5440 Nov  1 19:07 T-015-r4-paralegal-recheck.py
-rw-r--r--@   1 arsis  staff    3825 Nov  1 19:18 T-018-contract-probe.out.txt
-rw-r--r--@   1 arsis  staff    2589 Nov  1 19:17 T-018-contract-probe.py
-rw-r--r--@   1 arsis  staff    1217 Nov  1 18:58 T-025-pm-probe.out.txt
-rw-r--r--@   1 arsis  staff    1581 Nov  1 18:58 T-025-pm-probe.py
-rw-r--r--@   1 arsis  staff    1691 Nov  1 19:04 T-025-pm-r2-probe.out.txt
-rw-r--r--@   1 arsis  staff    1120 Nov  1 19:04 T-025-pm-r2-probe.py
-rw-r--r--@   1 arsis  staff  271072 Nov  1 19:03 T-026-desktop-dialog.png
-rw-r--r--@   1 arsis  staff  265680 Nov  1 19:03 T-026-desktop-office.png
-rw-r--r--@   1 arsis  staff  112324 Nov  1 19:03 T-026-mobile-dialog.png
-rw-r--r--@   1 arsis  staff  265502 Nov  1 19:03 T-026-mobile-office.png
-rw-r--r--@   1 arsis  staff    3151 Nov  1 19:03 T-026-ux-designer-office.py
-rw-r--r--@   1 arsis  staff    9797 Nov  1 19:13 T-028-r2-checks.py
-rw-r--r--@   1 arsis  staff    1018 Nov  1 19:14 T-028-r2-json-check.py
-rw-r--r--@   1 arsis  staff    8723 Nov  1 19:08 T-028-review-checks.py
-rw-r--r--@   1 arsis  staff    1076 Nov  1 19:09 T-028-review-json-check.py
-rw-r--r--@   1 arsis  staff  250341 Nov  1 19:21 T-047-desktop-1440-dialog.png
-rw-r--r--@   1 arsis  staff  195597 Nov  1 19:22 T-047-desktop-1440-forced-reviewing.png
-rw-r--r--@   1 arsis  staff  193861 Nov  1 19:21 T-047-desktop-1440.png
-rw-r--r--@   1 arsis  staff  275966 Nov  1 19:21 T-047-mobile-390-dialog.png
-rw-r--r--@   1 arsis  staff  504143 Nov  1 19:21 T-047-mobile-390-full.png
-rw-r--r--@   1 arsis  staff  198459 Nov  1 19:22 T-047-mobile-390-nav-onload.png
-rw-r--r--@   1 arsis  staff  273793 Nov  1 19:21 T-047-mobile-390.png
-rw-r--r--@   1 arsis  staff    2566 Nov  1 19:21 T-047-ux-designer-ac2-forced.py
-rw-r--r--@   1 arsis  staff    5750 Nov  1 19:21 T-047-ux-designer-check.py
-rw-r--r--@   1 arsis  staff    1574 Nov  1 19:22 T-047-ux-designer-nav-keyboard.py
drwxr-xr-x@   3 arsis  staff      96 Nov  1 18:56 __pycache__
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:47.463Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-018-contract-probe.py; echo ----; cat artifacts/review-evidence/T-018-contract-probe.out.txt 2>/dev/null | head -5; echo ----; sed -n 1,40p artifacts/tmp/contract_fixes.json | head -0; python3 -c 'import json;d=json.load(open(\"/Users/arsis/zlayt-pm-project/artifacts/tmp/contract_fixes.json\"));print(len(d));[print(i,x[\"src\"],x[\"cards\"]) for i,x in enumerate(d)]'",
 "description": "Inspect probe script and fixes file index"
}
````

### User / tool · 2026-11-02T01:23:47.577Z

**tool result**
````
"""T-018 contract probe (product-manager-reviewer). Read-only: parses card files + REQUIREMENTS.
Run: python3 -I artifacts/review-evidence/T-018-contract-probe.py <repo>"""
import re, sys, json, pathlib, glob, collections
root = pathlib.Path(sys.argv[1])
cards = {}
for p in sorted(glob.glob(str(root / "board/cards/T-0*.md"))):
    t = pathlib.Path(p).read_text()
    cid = re.search(r'^id: "(T-\d+)"', t, re.M).group(1)
    n = int(cid[2:])
    if n < 27 or n > 46 or n == 28:
        continue
    deps = json.loads(re.search(r'^depends_on: (.*)$', t, re.M).group(1))
    acs = [json.loads(l.strip()[2:])["text"] for l in t.splitlines() if l.strip().startswith('- {"n"')]
    cards[cid] = {"deps": deps, "ac": acs, "role": re.search(r'^role: "(\w+)"', t, re.M).group(1)}
req = (root / "spec/REQUIREMENTS.md").read_text()
rids = sorted(set(re.findall(r'^\| (R-[A-Z]{2}-\d+) \|', req, re.M)))
print("R-IDs defined:", len(rids))
actext = {c: " ".join(v["ac"]) for c, v in cards.items()}
missing = []
for r in rids:
    hit = [c for c, t in actext.items() if re.search(re.escape(r) + r'(?!\d)', t) or re.search(r'R-' + r[2:4] + r'-[\d/]*\b' , '')]
    if not hit:
        missing.append(r)
print("R-IDs named in NO card AC text:", missing)
# compact forms like R-IN-1/2/4
for r in missing:
    pre, num = r.rsplit("-", 1)
    alt = [c for c, t in actext.items() if re.search(re.escape(pre) + r'-[\d/]*\b' + '', t) and re.search(re.escape(pre) + r'-(?:\d+/)*' + num + r'(?:/\d+)*\b', t)]
    print("  ", r, "via slash form:", alt)
# test files cited per card
cited = collections.defaultdict(set)
for c, v in cards.items():
    for a in v["ac"]:
        for f in re.findall(r'(test_[a-z_0-9]+)(?:\.py|::)', a):
            cited[f].add(c)
qa_cards = [c for c, v in cards.items() if v["role"] == "qa"]
print("\nqa cards:", qa_cards)
print("test file -> cards citing it (qa-authored? = cited by a qa card)")
for f in sorted(cited):
    qa = sorted(cited[f] & set(qa_cards))
    print(f"  {f:28s} {sorted(cited[f])}  qa:{qa or 'NONE'}")
print("\ndeps:")
for c, v in cards.items():
    print(" ", c, v["role"], v["deps"])
# longest path (unweighted)
memo = {}
def lp(c):
    if c in memo: return memo[c]
    best = [c]
    for d in cards.get(c, {"deps": []})["deps"]:
        if d in cards:
            p = lp(d) + [c]
            if len(p) > len(best): best = p
    memo[c] = best; return best
print("longest dependency chain to T-038:", " -> ".join(lp("T-038")))
print("longest dependency chain to T-045:", " -> ".join(lp("T-045")))
print("AC count:", sum(len(v["ac"]) for v in cards.values()))
----
R-IDs defined: 62
R-IDs named in NO card AC text: ['R-CO-8', 'R-SU-1', 'R-SU-2', 'R-SU-3', 'R-SU-4', 'R-SU-5']
   R-CO-8 via slash form: []
   R-SU-1 via slash form: []
   R-SU-2 via slash form: []
----
head: illegal line count -- 0
19
0 manag ['T-027', 'T-031', 'T-034', 'T-036']
1 manag ['T-027', 'T-036', 'T-038']
2 manag ['T-037', 'T-038', 'T-045']
3 manag ['T-035', 'T-036', 'T-038']
4 manag ['T-038', 'T-045']
5 manag ['T-038']
6 paral ['T-039', 'T-044']
7 paral ['T-039']
8 paral ['T-043']
9 paral ['T-041', 'T-042']
10 engin ['T-029', 'T-034', 'T-037', 'T-039']
11 engin ['T-029', 'T-031', 'T-039', 'T-040', 'T-042', 'T-043', 'T-045']
12 engin ['T-034']
13 engin ['T-034', 'T-037']
14 engin ['T-035', 'T-036']
15 engin ['T-029']
16 engin ['T-033', 'T-036']
17 engin ['T-033']
18 engin ['T-033', 'T-039']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:52.264Z

**tool call — Bash**
````
{
 "command": "for c in T-027 T-029 T-030 T-031 T-032 T-033; do echo \"=== $c\"; python3 tools/board.py show $c | grep -E '^(priority|depends_on|status|  - \\{\"n\")'; done",
 "description": "Show AC lines and deps for M2 cards T-027..T-033"
}
````

### User / tool · 2026-11-02T01:23:52.678Z

**tool result**
````
=== T-027
status: "ready"
priority: "P0"
depends_on: []
  - {"n": 1, "text": "A held-out probe set (>=40 sentences, never copied into lexicon.yaml) lives in evals/ and the lexicon scores >=85% on it", "done": false, "evidence": null}
  - {"n": 2, "text": "Covers spinal levels and 'since <year>' in prior history, the hedges (may be degenerative/post-traumatic, favors, probable, uncertain chronicity), 'attributes/relates ... to'; no high pre_existing flag on post-accident wording", "done": false, "evidence": null}
  - {"n": 3, "text": "Category names match the ADR-013 closed list; self-check counts low-only hits as non-flags", "done": false, "evidence": null}
=== T-029
status: "ready"
priority: "P0"
depends_on: []
  - {"n": 1, "text": "tests/unit/test_sentences.py and test_grounding.py are committed first and fail only on NotImplemented: approx. 35 mph. is one unit, units concatenate to every golden record (R-TL-2), entry 8 with/without hedge (R-TL-8), summary-token and dropped-qualifier cases (R-TL-10), offset round trip (R-RV-9); proved by `pytest tests/unit/test_grounding.py -q`", "done": false, "evidence": null}
  - {"n": 2, "text": "tests/unit/test_confidence.py covers the full compose_state table (R-TL-5, row 17) and every reason code has a why template (row 18); proved by `pytest tests/unit/test_confidence.py -q`", "done": false, "evidence": null}
  - {"n": 3, "text": "test_dates.py, test_ingest.py, test_amounts.py, test_gaps.py encode: 7 formats + ambiguous 04/05/2026 (case_01), 29/30/31 incl. leap-year case_02, case_04 6->4 entries, 20 phrasings of 'Charge per visit $185' -> rate, $1,2OO unclear/null, record 7 header date; proved by `pytest tests/unit -q --collect-only` listing them", "done": false, "evidence": null}
  - {"n": 4, "text": "tests/unit/test_db.py (delete_case empties every table incl. prompts, 24h purge with injectable now, review_status round trip) and test_boundaries.py (AST scan: gap, amounts, dates, dedupe, sentences, export import no LLM client, R-CO-1); proved by `pytest tests/unit/test_boundaries.py`", "done": false, "evidence": null}
  - {"n": 5, "text": "every test docstring names an R-ID or table row; `grep -L 'R-[A-Z]*-[0-9]' tests/unit/test_*.py` prints nothing; `pytest tests/unit -x` shows no collection errors", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-029 AC4 or a new qa card 'M2 LLM-stage tests first' (deps [], blocks T-034..T-037): write test_provider, test_audited, test_schemas, test_judges, test_flags_sample, test_flags_injection, test_pipeline, test_conflicts, test_flag_templates red. T-039 AC4: name test_api.py plus the 10 E2E files above, by file.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-029 AC4: module list = sentences, grounding, confidence, why, dates, ingest/dedupe, amounts (find + classify), totals, gaps, conflicts (accident date), flag_templates, injection scan, export; scan transitive imports, not just direct ones.", "done": false, "evidence": null}
=== T-030
status: "ready"
priority: "P0"
depends_on: ["T-029"]
  - {"n": 1, "text": "`pytest tests/unit/test_sentences.py tests/unit/test_grounding.py` green: excerpt is a verbatim, whole-sentence, contiguous run; non-verbatim -> rejected, mid-unit -> needs_review (R-TL-2); hedge omitted -> EXCERPT_OMITS_QUALIFIER, hedge set read from lexicon.yaml `hedge: true` (R-TL-8)", "done": false, "evidence": null}
  - {"n": 2, "text": "new_tokens() and qualifier check: 'pain 4/10' over 'Pain 3/10.' and a summary dropping 'without loss of consciousness' -> needs_review; 'Visit 8' label passes (R-TL-10, row 15); proved by test_grounding::test_summary_tokens", "done": false, "evidence": null}
  - {"n": 3, "text": "offsets: for every golden excerpt raw_text[start:end] equals the quote; a mutated record makes lookup fail -> needs_review (R-RV-9, R-FL-5); proved by test_grounding::test_offsets_golden and test_offset_lookup_failure", "done": false, "evidence": null}
  - {"n": 4, "text": "`pytest tests/unit/test_confidence.py` green: full compose_state table, needs_review sorts first, every reason code has a why template (R-TL-5, rows 17, 18)", "done": false, "evidence": null}
  - {"n": 5, "text": "`pytest tests/unit/test_boundaries.py` green for these modules and a failing quote is never repaired (test_grounding::test_no_silent_fix, row 4 rung 1)", "done": false, "evidence": null}
=== T-031
status: "ready"
priority: "P0"
depends_on: ["T-029"]
  - {"n": 1, "text": "app/db/schema.sql applies on an empty DB and creates tables for records, entries, amounts, flags, llm_calls, events per ADR-002; `python -c \"from app.db import db; db.init(':memory:')\"` exits 0", "done": false, "evidence": null}
  - {"n": 2, "text": "llm_calls stores model, backend, prompt version+hash, prompt, response, verdict, latency, cost, one row per attempt; ladder record holds D.4 fields plus backend (R-CO-2, row 20); proved by tests/unit/test_db.py::test_ladder_roundtrip", "done": false, "evidence": null}
  - {"n": 3, "text": "delete_case(case_id) removes rows from every table including prompts, secure_delete is on, lazy 24h purge uses injectable now(); proved by test_db::test_delete_case_removes_all_tables and test_purge_24h", "done": false, "evidence": null}
  - {"n": 4, "text": "review_status and edits (originals kept) persist across a new connection (R-RV-8); proved by test_db::test_review_status_roundtrip", "done": false, "evidence": null}
  - {"n": 5, "text": "only the events helper writes review_status (grep test test_db::test_review_status_only_via_apply_review); every human action logs before/after (row 20)", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.", "done": false, "evidence": null}
=== T-032
status: "ready"
priority: "P0"
depends_on: ["T-029"]
  - {"n": 1, "text": "`pytest tests/unit/test_dates.py` green: case_01 seven formats parse, 04/05/2026 is date_ambiguous with candidates 2026-04-05 and 2026-05-04, no silent guess, confirm recompute hook (R-IN-3, R-IN-5, row 2)", "done": false, "evidence": null}
  - {"n": 2, "text": "`pytest tests/unit/test_ingest.py` green: sample splits to 9 records whose pieces concatenate to the input, 'N records found' count available with zero LLM calls (R-IN-1, row 1); case_04 6 records -> 4 entries citing all sources (R-TL-7)", "done": false, "evidence": null}
  - {"n": 3, "text": "date and provider set by code from the header: record 7 date 2026-05-18, record 4 provider 'Capital PT, initial evaluation' (R-TL-3, R-TL-9, row 3); proved by test_ingest::test_header_date_provider", "done": false, "evidence": null}
  - {"n": 4, "text": "empty and oversize input raise before any LLM call (counter == 0) (R-IN-4); proved by test_ingest::test_limits_no_llm", "done": false, "evidence": null}
  - {"n": 5, "text": "injection scan from lexicon `injection` category: case_07 record 3 tagged, record_warning flag created, its items forced needs_review, its amounts class unclear (R-RV-6, row 16); proved by test_ingest::test_injection_tag", "done": false, "evidence": null}
=== T-033
status: "ready"
priority: "P0"
depends_on: ["T-029", "T-032"]
  - {"n": 1, "text": "`pytest tests/unit/test_amounts.py` green: sample yields $6,240, $185, $2,150 only; 20 phrasings -> rate; $1,2OO and $9S.00 unclear/null; doses (10 mg etc.) never amounts; all golden amounts get golden class (R-CH-1, R-CH-2, R-CH-4, rows 6, 7)", "done": false, "evidence": null}
  - {"n": 2, "text": "totals: accepted $8,390, dismiss ER -> $2,150, detected shown separately and labelled not-a-total, no PT total (golden must_not M4), duplicate $6,240 counted once; injected $50,000 in case_07 never charge (R-CH-3, R-CH-6, R-RV-6, row 8); proved by test_amounts::test_totals", "done": false, "evidence": null}
  - {"n": 3, "text": "`pytest tests/unit/test_gaps.py` green: 29/30 no flag, 31 flags (case_02), sample 73 flagged and 28 not, case_09 56-day gap with billing/phone excluded, dismissing entry 6 leaves the gap unchanged (R-FL-1, D-003, row 9)", "done": false, "evidence": null}
  - {"n": 4, "text": "accident-date rule: sample conflict cites record 7 intake line vs records 1/2 header dates, never picks a date, no 'delay' text (R-FL-2a, D-017, row 10); proved by test_conflicts::test_accident_date", "done": false, "evidence": null}
  - {"n": 5, "text": "every flag title/explanation equals flag_templates output; no free-text field accepted (R-FL-8, row 14); proved by test_flag_templates::test_text_is_template", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): Either T-033 gains AC6 'case_05 provider conflict raised by code (normalized-name rule), no LLM call', or an ADR edits row 10 and T-036 AC3 says 'raised by the LLM conflict pass + judge #3'. T-036 AC2 append 'exactly one accident-date conflict flag in pipeline output (from T-033)'.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-033 new AC: 'rate note numbers are code-derived: N planned from the \"Plan of care: N visits\" match in a record with the same provider prefix, M from the highest \"visit M\" in a header label; omitted when not found; test on sample and a variant (plan 10, last visit 7)'. T-033 AC1: add 'one damages mention (record 5, value null) from the lexicon damages rule'.", "done": false, "evidence": null}
  - {"n": 8, "text": "Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is exactly \"Billed charges stated in these records: $420.00\"; with the $185 rate non-dismissed the sample line is unchanged'. T-033 AC1 append: '\"$6,240\" parses to int 624000; app/backend/amounts.py contains no float('.", "done": false, "evidence": null}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:23:52.797Z

**tool call — Bash**
````
{
 "command": "for c in T-034 T-035 T-036 T-037 T-038; do echo \"=== $c\"; python3 tools/board.py show $c | grep -E '^(priority|depends_on|status|  - \\{\"n\")'; done",
 "description": "Show AC lines and deps for M2 cards T-034..T-038"
}
````

### User / tool · 2026-11-02T01:23:53.145Z

**tool result**
````
=== T-034
status: "ready"
priority: "P0"
depends_on: ["T-031", "T-048"]
  - {"n": 1, "text": "`LLM_BACKEND=fixture pytest tests/unit/test_provider.py` green with no API key; backend chosen by LLM_BACKEND and recorded in each audit row (R-CO-6, ADR-004)", "done": false, "evidence": null}
  - {"n": 2, "text": "audited.py: fails 3 attempts -> LLM_FAILED_AFTER_RETRIES and app stays usable; fails twice then succeeds -> output returned; one llm_calls row per attempt, each retry with changed conditions (R-CO-9, row 20); proved by test_audited.py", "done": false, "evidence": null}
  - {"n": 3, "text": "record mode: `LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record evals/golden/sample.txt` writes tests/fixtures/llm/*.json; recorder refuses text not under evals/golden (test_provider::test_recorder_refuses_foreign_text)", "done": false, "evidence": null}
  - {"n": 4, "text": "claude-cli argv test: pinned --model, no tools/MCP, disableAllHooks settings, cwd outside project, 120 s timeout, concurrency <= 3 (flags confirmed with `claude --help`); anthropic-api tested against recorded fixtures/mocked SDK (CONTRACT 5.2)", "done": false, "evidence": null}
  - {"n": 5, "text": "no SDK/subprocess call outside app/llm/backends and no record text in logs: test_provider::test_single_call_path and test_no_text_in_logs", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-034 AC4 append: 'anthropic-api client is constructed with max_retries=0 and an explicit timeout (<= 120 s); test_provider::test_sdk_no_internal_retry asserts both on the constructed client'.", "done": false, "evidence": null}
  - {"n": 8, "text": "Contract review (T-018): T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash); the audited wrapper turns it into LLM_FAILED_AFTER_RETRIES; never a default answer'. T-037 AC2 replace with: 'replaying sample, case_01..09, hallucinations(.jsonl, _controls) and SE1-SE5 on fixture reports 0 FixtureMissing (count printed)'.", "done": false, "evidence": null}
=== T-035
status: "ready"
priority: "P0"
depends_on: ["T-030", "T-032", "T-033", "T-034", "T-048"]
  - {"n": 1, "text": "generator schema is {summary, excerpt} only: no provider, date, amount or clinical-facts field (R-TL-9, rows 3, 5 'not built'); proved by tests/unit/test_schemas.py::test_generator_schema_minimal", "done": false, "evidence": null}
  - {"n": 2, "text": "fixture run of the extract stage on evals/golden/sample.txt gives 9 entries, none of the four fields empty, same-date records 1 and 2 kept separate in source order (R-TL-1, A-108); a seeded non-verbatim excerpt is rejected and never reaches the timeline (R-TL-2)", "done": false, "evidence": null}
  - {"n": 3, "text": "judge #1 returns supported/partially/unsupported; partially or unsupported -> needs_review with reason; judge error/timeout -> JUDGE_UNAVAILABLE (R-TL-4, row 4 rung 2); proved by test_judges.py::test_j1_states", "done": false, "evidence": null}
  - {"n": 4, "text": "judge #2 re-reads every amount class incl. rule-made ones; disagrees -> JUDGE_DISAGREES; a rate never becomes a charge (R-CH-2, row 7); proved by test_judges.py::test_j2_every_amount", "done": false, "evidence": null}
  - {"n": 5, "text": "prompts are versioned files app/llm/prompts/*_v1.md with a changelog line (grep) and the generator and judge never share a prompt (CONTRACT 5.2)", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml; `python -m evals.run --check-fresh` exits 1 when any current hash differs'. T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-035 AC4 append: 'judge #2 unsure, error or timeout -> needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a charge is verified only on agrees'. T-036 AC5 append: 'judge #3/#4 error or timeout -> needs_review JUDGE_UNAVAILABLE'.", "done": false, "evidence": null}
=== T-036
status: "ready"
priority: "P0"
depends_on: ["T-027", "T-033", "T-035", "T-048"]
  - {"n": 1, "text": "flag output schema has category + excerpt spans only; extra or prose fields rejected (R-FL-8, row 14); proved by test_schemas::test_flag_schema_no_prose", "done": false, "evidence": null}
  - {"n": 2, "text": "fixture run on the sample raises: conflict (a) accident date and (b) 12-visit plan vs discharge at visit 9, pre_existing on records 3 and 8, causation K1-K5 as distinct flags with one-to-one matching via the check_golden matcher (R-FL-2b, R-FL-3, R-FL-4, rows 11-13); proved by tests/unit/test_flags_sample.py", "done": false, "evidence": null}
  - {"n": 3, "text": "only one of LLM/lexicon fires -> needs_review with LEXICON_ONLY or LLM_ONLY; case_06 28-day near-miss does not flag; case_05 provider-name conflict raised and name variants tolerated (R-FL-3, R-FL-2)", "done": false, "evidence": null}
  - {"n": 4, "text": "per-record pass: each prompt contains exactly one record nonce block; case_07 record 2 pre_existing flag still raised despite the injected record (R-RV-6, rows 12, 16); proved by test_flags_injection.py", "done": false, "evidence": null}
  - {"n": 5, "text": "judge #3 and #4 must agree or flag is needs_review; evidence that fails grounding -> rejected; source_kind patient_report set by code for record 9 (R-FL-5, R-FL-7, row 13)", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): Either raise T-027 to P0 with a timebox in its Description, or remove T-027 from T-036 depends_on and add a T-036 AC: 'runs against app/llm/lexicon.yaml at HEAD; lexicon recall per must-flag is reported by evals.run (see T-038 finding)'.", "done": false, "evidence": null}
  - {"n": 8, "text": "Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml; `python -m evals.run --check-fresh` exits 1 when any current hash differs'. T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'.", "done": false, "evidence": null}
  - {"n": 9, "text": "Contract review (T-018): T-035 AC4 append: 'judge #2 unsure, error or timeout -> needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a charge is verified only on agrees'. T-036 AC5 append: 'judge #3/#4 error or timeout -> needs_review JUDGE_UNAVAILABLE'.", "done": false, "evidence": null}
  - {"n": 10, "text": "Contract review (T-018): Either T-033 gains AC6 'case_05 provider conflict raised by code (normalized-name rule), no LLM call', or an ADR edits row 10 and T-036 AC3 says 'raised by the LLM conflict pass + judge #3'. T-036 AC2 append 'exactly one accident-date conflict flag in pipeline output (from T-033)'.", "done": false, "evidence": null}
=== T-037
status: "ready"
priority: "P0"
depends_on: ["T-032", "T-033", "T-035", "T-036", "T-048"]
  - {"n": 1, "text": "`python -m app.pipeline evals/golden/sample.txt` (fixture backend) prints 9 entries, the 73-day gap flag, charges $8,390 total, all flag groups, exit 0 in under 60 s (CONTRACT M2 CLI)", "done": false, "evidence": null}
  - {"n": 2, "text": "fixtures recorded with claude-cli for sample + 9 cases under tests/fixtures/llm/; `ls tests/fixtures/llm | wc -l` > 0 and a hash check shows nothing outside evals/golden", "done": false, "evidence": null}
  - {"n": 3, "text": "stage names match /status (ingest, extract, verify, judge_entries, amounts, conflicts, flags, finalize) and an 8-minute deadline fails visibly with injectable now(); proved by tests/unit/test_pipeline.py::test_stages_and_deadline", "done": false, "evidence": null}
  - {"n": 4, "text": "gap flags and ingest results exist when every LLM call raises (stub backend); dropping an entry leaves gaps unchanged (D-003, row 9); proved by test_pipeline::test_code_stages_without_llm", "done": false, "evidence": null}
  - {"n": 5, "text": "every LLM-derived item has a ladder record with backend, and no item has review_status other than pending after a run (R-CO-2, R-RV-6, row 20); proved by test_pipeline::test_ladder_and_pending", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BACKEND != fixture; latest.json records backend and model ids; ship_bar_met is false when backend == fixture'. T-037 AC2: 'fixtures recorded for sample, case_01..09, every line of hallucinations.jsonl and hallucinations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_bar_met true; report path in handoff'.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash); the audited wrapper turns it into LLM_FAILED_AFTER_RETRIES; never a default answer'. T-037 AC2 replace with: 'replaying sample, case_01..09, hallucinations(.jsonl, _controls) and SE1-SE5 on fixture reports 0 FixtureMissing (count printed)'.", "done": false, "evidence": null}
=== T-038
status: "ready"
priority: "P0"
depends_on: ["T-037"]
  - {"n": 1, "text": "`python -m evals.run` writes evals/reports/latest.json and a timestamped .md; `jq '.ship_bar_met, .metrics | keys' evals/reports/latest.json` shows ship_bar_met plus grounding_rate, entry_recall, amount_recall, flag_precision[type], flag_recall[type], hallucination_catch_rate, unsupported_count_3run, determinism_3run, each with its R-ID and gap_28_not_flagged / gap_73_flagged", "done": false, "evidence": null}
  - {"n": 2, "text": "spec-vs-golden check: `python -m evals.run --check-spec` compares REQUIREMENTS.md section 6 block 1/2 byte-for-byte with sample.export.expected.txt LETTER_TEXT/INTERNAL_NOTES_TEXT and writes spec_matches_golden to latest.json; changing one character in a temp copy makes it false (tests/unit/test_eval_spec_check.py)", "done": false, "evidence": null}
  - {"n": 3, "text": "hallucination_catch_rate >= 0.95 computed as a rate over every line of hallucinations.jsonl (today 40) and no control in hallucinations_controls.jsonl returns unsupported (R-TL-4, ship bar 4)", "done": false, "evidence": null}
  - {"n": 4, "text": "determinism_3run measured only on a live backend (claude-cli or anthropic-api): 3 runs on sample, code outputs identical, same states and same flag set = 1.0; on fixture the field is null/not_measured and cannot satisfy ship_bar_met (R-CO-7)", "done": false, "evidence": null}
  - {"n": 5, "text": "ship_bar_met is false when any bar is missed (test with a tampered report), golden must_not hits are counted (R-CO-3), and case_07 total stays $420 (R-RV-6); proved by tests/unit/test_eval_runner.py", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BACKEND != fixture; latest.json records backend and model ids; ship_bar_met is false when backend == fixture'. T-037 AC2: 'fixtures recorded for sample, case_01..09, every line of hallucinations.jsonl and hallucinations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_bar_met true; report path in handoff'.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml; `python -m evals.run --check-fresh` exits 1 when any current hash differs'. T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'.", "done": false, "evidence": null}
  - {"n": 8, "text": "Contract review (T-018): Add a 'Ship bar row -> card' table to M2M3_COVERAGE.md (rows 1-4 -> T-038, row 5 -> T-045 + M3 gate). New orchestrator card (M3): 'paralegal-reviewer agent body and M3 gate brief request scores.verify_quickly 1-5 (D-015)'.", "done": false, "evidence": null}
  - {"n": 9, "text": "Contract review (T-018): T-038 AC1: add `lexicon_recall_must_flags` (pre_existing + causation, per golden case, pooled) with R-IDs R-FL-3, R-RV-6, and state the threshold in REQUIREMENTS §7 by ADR, or edit LLM_VS_CODE rows 12/16 to 'reported, not gated'.", "done": false, "evidence": null}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:24:02.409Z

**tool call — Bash**
````
{
 "command": "for c in T-039 T-040 T-041 T-042 T-043 T-044 T-045 T-046; do echo \"=== $c\"; python3 tools/board.py show $c | grep -E '^(priority|depends_on|status|  - \\{\"n\")'; done",
 "description": "Show AC lines and deps for M3 cards T-039..T-046"
}
````

### User / tool · 2026-11-02T01:24:02.891Z

**tool result**
````
=== T-039
status: "ready"
priority: "P0"
depends_on: []
  - {"n": 1, "text": "tests/unit/test_export.py: every letter line is heading / date+provider / summary / Source quote / amount / total; builder signature has no flags argument; total line exactly 'Billed charges stated in these records: $8,390.00' incl. case_07 with a rate present; same accepted set -> byte-identical output; fixture sample equals sample.export.expected.txt (R-EX-1, R-EX-2, R-EX-3, R-EX-6, R-EX-8); proved by `pytest tests/unit/test_export.py --collect-only`", "done": false, "evidence": null}
  - {"n": 2, "text": "test_export notes: sections in R-EX-4 order, every 'record N' followed by (provider, date), bills-to-request line exact, dismissing entry 5 gives 'Record 5 ... dismissed' and 7 of 9 (R-EX-4, R-EX-7)", "done": false, "evidence": null}
  - {"n": 3, "text": "tests/unit/test_review_rules.py: 422 invalid_edit matrix (entry date/provider, flag evidence/type/title, charge amount/class, non-contiguous excerpt, hedge-dropping excerpt), 422 date_invalid, 409 needs_confirm for +$9,000 and seeded 'herniation', keep-my-wording resend saves, judge unavailable -> JUDGE_UNAVAILABLE; accept $1,2OO -> notes 'request clean copy of bill', not letter; accept $185 -> total still $8,390 (R-RV-2, R-RV-3, R-CH-5, R-CH-7)", "done": false, "evidence": null}
  - {"n": 4, "text": "tests/e2e specs with page helpers for R-IN-1/2/4, R-TL-5/6, R-FL-6/7, R-CH-3, R-RV-1/4/5/8/9, R-EX-5/7/9, R-CO-5, each red against the missing UI; `pytest tests/e2e --collect-only` lists them", "done": false, "evidence": null}
  - {"n": 5, "text": "all new tests cite R-IDs in docstrings and use the fixture backend only (no key, no network)", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-044 AC1 append: 'reload -> edited summary and \"edited\" label persist; export notes list record 3 under EDITED ITEMS with original and new text'. T-039 AC2 append: 'test_export::test_edited_items_section with entry 3 edited lists both texts and any keep-my-wording confirmation'.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-039 AC2: 'dismissing entry 5 and leaving entry 6 pending gives \"Record 5 ... dismissed\", \"Record 6 ... not reviewed\" and 7 of 9'.", "done": false, "evidence": null}
  - {"n": 8, "text": "Contract review (T-018): T-029 AC4 or a new qa card 'M2 LLM-stage tests first' (deps [], blocks T-034..T-037): write test_provider, test_audited, test_schemas, test_judges, test_flags_sample, test_flags_injection, test_pipeline, test_conflicts, test_flag_templates red. T-039 AC4: name test_api.py plus the 10 E2E files above, by file.", "done": false, "evidence": null}
  - {"n": 9, "text": "Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is exactly \"Billed charges stated in these records: $420.00\"; with the $185 rate non-dismissed the sample line is unchanged'. T-033 AC1 append: '\"$6,240\" parses to int 624000; app/backend/amounts.py contains no float('.", "done": false, "evidence": null}
=== T-040
status: "ready"
priority: "P0"
depends_on: ["T-037", "T-039", "T-031"]
  - {"n": 1, "text": "`pytest tests/unit/test_review_rules.py` green: 422 invalid_edit matrix, 409 needs_confirm then keep-my-wording, JUDGE_UNAVAILABLE, charges accept/dismiss/reset only (R-RV-2, R-RV-3, R-CH-7, R-RV-5, row 15 for edits)", "done": false, "evidence": null}
  - {"n": 2, "text": "`pytest tests/unit/test_api.py` green with fixture TestClient: all 11 endpoints match memory/contracts/api.md shapes, error format, unknown token 404, Why? returns ladder + backend (R-TL-6)", "done": false, "evidence": null}
  - {"n": 3, "text": "demo gate: unrecorded text -> 409 demo_mode_unsupported_input and nothing stored; oversize 413, empty 400 with LLM counter 0 (R-IN-4, R-CO-4 demo part, D-020)", "done": false, "evidence": null}
  - {"n": 4, "text": "confirm_date on case_01 record 8 with 2026-05-04 -> entry sorts after 03-25, gap table unchanged, event logged; no readings -> cannot confirm (R-IN-5, R-RV-2)", "done": false, "evidence": null}
  - {"n": 5, "text": "decisions survive a new TestClient/app restart (R-RV-8); only review and confirm_date set review_status (grep test); Referrer-Policy: no-referrer, no access log of tokens", "done": false, "evidence": null}
=== T-041
status: "ready"
priority: "P0"
depends_on: ["T-039", "T-033", "T-037"]
  - {"n": 1, "text": "`pytest tests/unit/test_export.py` green (line grammar, no flags argument, total line exact, determinism) (R-EX-1, R-EX-2, R-EX-3, R-EX-8)", "done": false, "evidence": null}
  - {"n": 2, "text": "golden: on the fixture backend with all entries/charges accepted, letter_text and internal_notes_text equal the sample.export.expected.txt sections byte for byte (R-EX-6); proved by test_export::test_golden_bytes", "done": false, "evidence": null}
  - {"n": 3, "text": "internal notes contain the 11 R-EX-4 sections in order, including flagged-language-in-letter, bills-to-request line and reconciliation (R-EX-4, R-EX-7); proved by test_export::test_notes_sections", "done": false, "evidence": null}
  - {"n": 4, "text": "GET /api/cases/{id}/export returns the two fields separately; pending/dismissed/rejected items never appear (row 19); proved by test_api::test_export_endpoint", "done": false, "evidence": null}
  - {"n": 5, "text": "export.py imports no LLM client (tests/unit/test_boundaries.py, R-CO-1) and the AI-assistance line only appears in notes", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 \"could not process\" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECORDS NOT IN THE TREATMENT SECTION with reason \"could not process\"'.", "done": false, "evidence": null}
=== T-042
status: "ready"
priority: "P0"
depends_on: ["T-039"]
  - {"n": 1, "text": "paste and .txt upload show '9 records found' before any model call; .pdf refused with a plain message; empty/oversize shows an error state (R-IN-1, R-IN-2, R-IN-4); proved by tests/e2e/test_input.py", "done": false, "evidence": null}
  - {"n": 2, "text": "timeline rows show date, provider, summary, excerpt, state; needs_review above verified; 'Dates to confirm' group after the timeline; rejected items in a 'could not verify' tray (R-TL-1, R-TL-5, R-IN-5); proved by test_timeline.py", "done": false, "evidence": null}
  - {"n": 3, "text": "Why? on entry 7 shows check results, judge verdict, state and backend (R-TL-6); proved by test_timeline.py::test_why_entry7", "done": false, "evidence": null}
  - {"n": 4, "text": "opening entry 8's record highlights a span equal to the excerpt using API offsets (R-RV-9); proved by test_source_record.py::test_entry_highlight", "done": false, "evidence": null}
  - {"n": 5, "text": "banner 'Synthetic data only — never paste real records' on every view and the AI banner on review (R-CO-5); `grep -c innerHTML app/frontend/*.js` is 0 (textContent only)", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 \"could not process\" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECORDS NOT IN THE TREATMENT SECTION with reason \"could not process\"'.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.", "done": false, "evidence": null}
=== T-043
status: "ready"
priority: "P0"
depends_on: ["T-039", "T-040", "T-042"]
  - {"n": 1, "text": "four flag groups plus 'Record warnings'; sample has >=1 flag per group; case_01 shows a dates-to-confirm item with a confirm_date control; case_07 shows an injection warning; 'Patient self-report' label on record 9 (R-FL-6, R-FL-7, R-IN-5); proved by tests/e2e/test_flags_panel.py", "done": false, "evidence": null}
  - {"n": 2, "text": "charges table: Accepted $8,390 then $2,150 after dismissing ER, 'Detected, not yet accepted' labelled not a total, $185 'rate $185/visit; visit count not stated', no PT total; accepting $1,2OO keeps it in the unclear tray (R-CH-3, R-CH-5); proved by test_charges.py", "done": false, "evidence": null}
  - {"n": 3, "text": "review matrix {accept, edit-note, dismiss} x flag, {accept, dismiss} x charge, entry accept/dismiss; fresh load all pending; dismiss -> reset -> dismiss; reload restores statuses and total (R-RV-1, R-RV-5, R-RV-8); proved by test_review_matrix.py", "done": false, "evidence": null}
  - {"n": 4, "text": "keyboard-only completion (accept/edit/dismiss/next) and 375 px with no horizontal scroll and every action reachable (R-RV-4); proved by test_keyboard_mobile.py", "done": false, "evidence": null}
  - {"n": 5, "text": "gap flag opens both records 6 and 7 in the source modal (R-RV-9); proved by test_source_record.py::test_gap_flag_two_records", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-043 AC1 append: 'the accident-date conflict card shows \"Date of accident per intake form: 2026-01-19.\" and the 2026-01-09 header line(s) of records 1 and 2 side by side, and contains none of \"resolved\", \"correct date\", \"delay\"'.", "done": false, "evidence": null}
  - {"n": 7, "text": "Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.", "done": false, "evidence": null}
=== T-044
status: "ready"
priority: "P0"
depends_on: ["T-043", "T-040", "T-041"]
  - {"n": 1, "text": "edit entry 3 summary -> 'edited' label in UI; letter shows new summary and citation with no 'edited' mark; adding '$9,000' shows the 409 reasons and 'keep my wording' (R-RV-2, R-RV-3); proved by tests/e2e/test_edit.py", "done": false, "evidence": null}
  - {"n": 2, "text": "excerpt re-selection lists sentence units of the same record only; dropping a hedge unit shows the invalid_edit message (R-RV-2, R-TL-8); proved by test_edit.py::test_excerpt_units", "done": false, "evidence": null}
  - {"n": 3, "text": "export view has two separate Copy buttons; clipboard after each equals the matching API field; count line is in neither block (R-EX-5, R-EX-9); proved by test_export_ui.py::test_copy_blocks", "done": false, "evidence": null}
  - {"n": 4, "text": "leaving the 73-day gap flag pending then Copy letter asks one confirmation reading '1 flag not reviewed' (R-EX-5); dismiss entry 5 and leave entry 6 pending shows '7 of 9 records in letter' (R-EX-7)", "done": false, "evidence": null}
  - {"n": 5, "text": "fixture-backend UI export with everything accepted equals sample.export.expected.txt (R-EX-6); proved by test_export_ui.py::test_golden_in_ui", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-044 AC1 append: 'reload -> edited summary and \"edited\" label persist; export notes list record 3 under EDITED ITEMS with original and new text'. T-039 AC2 append: 'test_export::test_edited_items_section with entry 3 edited lists both texts and any keep-my-wording confirmation'.", "done": false, "evidence": null}
=== T-045
status: "ready"
priority: "P0"
depends_on: ["T-044", "T-040", "T-041"]
  - {"n": 1, "text": "`pytest tests/e2e` green on the fixture backend: paste sample -> run -> review (accept, edit, dismiss) -> export; letter set equals accepted set, needs_review first, dismissed never exports, edits labeled, decisions survive reload (ship bar 5; R-RV-1, R-RV-5, R-RV-8, R-TL-5)", "done": false, "evidence": null}
  - {"n": 2, "text": "R-EX-1 matrix: accept all items, add a reviewer note to the gap flag; letter_text contains none of the note, any flag label/title, '73 days', 'AI assistance' or a count line; proved by tests/e2e/test_letter_isolation.py", "done": false, "evidence": null}
  - {"n": 3, "text": "journey by keyboard only and at 375 px; adversarial inputs (empty, oversize, non-English, case_07 injection with total staying $420, pasted PDF text with page headers) end in clear states with LLM counter 0 where required (R-IN-4, R-RV-4, R-RV-6, R-CO-5)", "done": false, "evidence": null}
  - {"n": 4, "text": "sensors recorded in evals/reports/m3-sensors.md: `pytest tests/unit`, `python -m evals.run` (ship_bar_met true), `python tools/check_secrets.py` exit 0, e2e green", "done": false, "evidence": null}
  - {"n": 5, "text": "M3 gate evidence: R-CO-2 check that an LLM item with no human action is absent from both blocks (tests/e2e/test_ladder_gate.py)", "done": false, "evidence": null}
  - {"n": 6, "text": "Contract review (T-018): T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BACKEND != fixture; latest.json records backend and model ids; ship_bar_met is false when backend == fixture'. T-037 AC2: 'fixtures recorded for sample, case_01..09, every line of hallucinations.jsonl and hallucinations_controls.jsonl, and sample seeded_edits SE1-SE5'. T-045 AC4: '`LLM_BACKEND=claude-cli python -m evals.run` -> ship_bar_met true; report path in handoff'.", "done": false, "evidence": null}
=== T-046
status: "ready"
priority: "P2"
depends_on: ["T-044"]
  - {"n": 1, "text": "at 1280 px the record pane sits beside the queue; stepping through three items by keyboard updates the pane and the highlighted span equals the excerpt (R-ST-1); proved by tests/e2e/test_side_by_side.py", "done": false, "evidence": null}
  - {"n": 2, "text": "at 375 px the R-RV-9 modal opens instead; proved by test_side_by_side.py::test_mobile_fallback", "done": false, "evidence": null}
  - {"n": 3, "text": "no new backend endpoint, offsets reused; the R-RV-9 modal tests stay green: `pytest tests/e2e/test_source_record.py`", "done": false, "evidence": null}
  - {"n": 4, "text": "timebox 45 min and start only when every other M3 card is done; if cut, memory/SCOPE_CUTS.md gains an R-ST-1 row (`grep R-ST-1 memory/SCOPE_CUTS.md`)", "done": false, "evidence": null}
  - {"n": 5, "text": "cut order per REQUIREMENTS section 4 recorded if M3 passes 100% of budget: R-ST-1, then excerpt re-selection, then R-EX-4 sections 7-8, then R-RV-9 highlight", "done": false, "evidence": null}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:24:03.052Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-027; echo; echo \"=== T-036 Description/Notes head\"; python3 tools/board.py show T-036 | sed -n '/^## Description/,/^## Notes/p' | head -30",
 "description": "Show M3 card AC lines and T-027 full card"
}
````

### User / tool · 2026-11-02T01:24:03.230Z

**tool result**
````
---
id: "T-027"
title: "Lexicon generalization: held-out recall for prior-history, hedges, patient attribution; ADR-013 category names"
milestone: "M2"
role: "researcher"
status: "ready"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T01:00:15Z"
updated_at: "2026-11-02T01:22:47Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "A held-out probe set (>=40 sentences, never copied into lexicon.yaml) lives in evals/ and the lexicon scores >=85% on it", "done": false, "evidence": null}
  - {"n": 2, "text": "Covers spinal levels and 'since <year>' in prior history, the hedges (may be degenerative/post-traumatic, favors, probable, uncertain chronicity), 'attributes/relates ... to'; no high pre_existing flag on post-accident wording", "done": false, "evidence": null}
  - {"n": 3, "text": "Category names match the ADR-013 closed list; self-check counts low-only hits as non-flags", "done": false, "evidence": null}
---
## Description
Debt from T-009 (reviews/T-009-legal-nurse-r2.md majors 1-5). The probe sets were copied into the lexicon examples, so the self-check measures memorization. Fix the patterns rather than the examples, and score on a held-out set.

## Notes (append-only, newest last)
- 2026-11-02T01:22:47Z orchestrator: updated priority=P0

## Handoff (filled when moving to in_review)


=== T-036 Description/Notes head
## Description
Hybrid flag engines with the lexicon as the floor, per R-FL-2b, R-FL-3 to R-FL-5, R-FL-7 and R-RV-6. Depends on existing researcher card T-027 (lexicon generalization) for held-out recall; LLM_VS_CODE rows 10 (provider variants), 11, 12, 13, 16.

Plan key: m2-be-llm-flags (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

## Notes (append-only, newest last)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:25:03.068Z

**tool call — Bash**
````
{
 "command": "echo \"--- verify_quickly in agent/persona\"; grep -n verify_quickly .claude/agents/paralegal-reviewer.md personas/paralegal.md; echo \"exit=$?\"; echo \"--- M3 cards mentioning verify_quickly\"; for c in $(python3 tools/board.py list | awk '{print $1}'); do python3 tools/board.py show $c 2>/dev/null | grep -l verify_quickly >/dev/null && echo \"$c\"; done; echo \"--- SCOPE_CUTS\"; cat memory/SCOPE_CUTS.md 2>/dev/null | head -60; echo \"--- LLM_VS_CODE rows 10,12,16\"; grep -n '^| 1[026] \\|^| 1[0-9] ' docs/LLM_VS_CODE.md | head -20",
 "description": "Check verify_quickly, SCOPE_CUTS and LLM_VS_CODE rows"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:25:04.357Z

**tool call — Bash**
````
{
 "command": "echo \"--- ORCH decisions re row10 / lexicon gate / engine\"; grep -n -i 'row 10\\|provider.*conflict\\|case_05\\|lexicon.*recall\\|release gate\\|reported, not gated\\|verify_quickly\\|D-015\\|D-024' memory/ORCHESTRATOR_DECISIONS.md | head -30; echo \"--- REQUIREMENTS ship bar section 7\"; grep -n -i 'ship bar\\|## 7\\|^## 8' spec/REQUIREMENTS.md | head; echo \"--- CONTRACT 8.3 and 5.2 default backend\"; grep -rn 'LLM_BACKEND' docs/CONTRACT.md memory/*.md 2>/dev/null | head -8",
 "description": "Check decisions, ship bar section and default backend"
}
````

### User / tool · 2026-11-02T01:25:05.666Z

**tool result**
````
--- verify_quickly in agent/persona
.claude/agents/paralegal-reviewer.md:111:**Ship-bar score (D-015):** whenever you review the running app, your review JSON must include `scores.verify_quickly` (1–5): "I could verify every claim quickly." ≥ 4 is the ship bar.
exit=0
--- M3 cards mentioning verify_quickly
T-025
T-038
--- SCOPE_CUTS
# SCOPE CUTS (what was cut · why · what it would take to add later)

| # | Cut | Why | Cost to add later | Milestone |
|---|---|---|---|---|
| 1 | PDF upload / OCR | OCR errors would sit upstream of the grounding check, so "verbatim excerpt" would stop meaning "in the record". | ~1 day: PDF text layer + page/Bates mapping; OCR needs its own verification step. | M1 (R non-goal 1) |
| 2 | Multi-case / matter management | One case proves the workflow; matter management is commodity. | ~2 days: case table, list view, per-case audit. | M1 (2) |
| 3 | Accounts, auth, roles, sharing | Prototype; nothing persists beyond a session. | ~1–2 days with an IdP; required before real data. | M1 (3) |
| 4 | Real data / PHI handling (retention, BAA, encryption at rest) | Spec forbids real data; we design for it in docs but don't implement. | Weeks: vendor BAA/zero-retention LLM, retention policy, access logs. | M1 (4) |
| 5 | Demand-letter prose in a firm's voice | Generated advocacy text is where invented facts creep in; export stays structured and cited. | ~1 day plus a new eval for faithfulness of prose. | M1 (5) |
| 6 | Medical or legal judgment (diagnosis, severity, causation opinions) | Flags point at the record's own words; judgment stays with the paralegal/attorney. | Not planned — out of the tool's role. | M1 (6) |
| 7 | Billing analysis (PT total from rate, reasonableness, liens, paid vs incurred) | Totals only stated charges; anything else is "unclear — not totaled". | ~1 day for itemized bills; needs the actual ledgers. | M1 (7) |
| 8 | Integrations (EHR, case management, email intake) | Paste/upload is enough to prove the workflow. | Per integration, days. | M1 (8) |
| 9 | Per-user learning from dismissals | Dismissals logged for metrics only; feeding them back would need its own evals. | ~2 days + eval guardrails. | M1 (9) |
| 10 | Numeric confidence scores | Three states (verified / needs_review / rejected) — a percentage would imply precision we can't verify. | Calibration study first. | M1 (10) |
| 11 | Non-English records, handwriting | Clear failure message; chaos-tested. | Translation + separate grounding rules. | M1 (11) |
| 12 | Manually adding a timeline entry for a record the pipeline rejected | Keeps every entry machine-grounded; a rejected record stays visible in the "could not verify" tray with its text. | ~half day: manual entry form that still requires selecting a verbatim excerpt. | M1 (architect, ADR) |
| 13 | LLM fallback for ambiguous record splitting | Code splits on dates/headers; an unsplittable paste is flagged for the paralegal instead of guessed. | ~half day + eval case; output must be flagged as LLM-split. | M1 (architect, ADR) |
| 14 | Batch accept | Not a must-have; needs an ADR change; single-key accept is fast enough for a 9-record case. | ~half day + guard so amounts are never batch-accepted. | M1 (D-011) |
| 15 | Charge reclassification by the paralegal | A rate must never become a totaled charge; accept/dismiss is enough. | ~half day + judge re-check. | M1 (D-011) |
| 16 | "Not a duplicate" split action | Dedupe merge stays visible with "duplicate of" note. | ~2 h. | M1 (D-011) |
| 17 | LLM date pointing, BYOK, audit ?full=1, flag text edits, case list | Time box; exposure on a public Space. | ~1 day total. | M1 (D-011) |
| 18 | Per-packet date-convention inference (infer MM/DD vs DD/MM from other dates) | An ambiguous numeric date always asks once; inference adds a silent-guess risk. | ~half day + its own eval. | M1 (REQUIREMENTS non-goal 18) |
| 19 | Exhibit/Bates numbering by the tool | Placeholder only; firm numbering lives in its own system. | Config + integration with the firm's exhibit list. | M1 (REQUIREMENTS non-goal 12) |
| debt | T-013 accepted with documented debt after 3 rounds (§7.4) | Remaining reconciliation (hallucination threshold as rate, K4/K5 must, D-019 total line, both-side accident-date quotes, D-016..D-021 refs, §8 clean) split to T-025, which T-017 depends on. | see card | M1 |
| debt | T-009 accepted with documented debt after 2 rounds (§7.4) | Lexicon passes golden (must 11/11) but overfits probes (11/40 held-out); generalization moved to new M2 card | see card | M1 |
| debt | T-014 accepted with documented debt after 3 rounds (§7.4) | 5 consistency majors, 0 blockers after 3 rounds; split to T-028 which T-017 depends on | see card | M1 |
| debt | T-005 accepted with documented debt after 3 rounds (§7.4) | r3 major (STATE heartbeat line) and minors fixed by orchestrator after review; residual: NEEDS_CHRIS row-to-card parity is a manual check | see card | M0 |
| debt | T-001 accepted with documented debt after 3 rounds (§7.4) | r3 major (debt entry masking later fails) fixed after review with test_debt_does_not_mask_later_fail; minors carried (review --file path scope, needs_chris close test, shallow review validation, stale claim lock) | see card | M0 |
| debt | T-004 accepted with documented debt after 3 rounds (§7.4) | r3 major (move T --agent x done spelling) fixed with tests; minors carried (read-only git verbs denied for reviewers, Write vs Bash scratchpad mismatch, compile --only typo rc) | see card | M0 |
| debt | T-025 accepted with documented debt after 2 rounds (§7.4) | r2 majors fixed by orchestrator after review (R-FL-4 range, A-106 row, row 5 owner, §6 notes block synced to golden by diff); residual: §8 has no automated equality check vs golden (add to M2 qa eval runner) | see card | M1 |
| debt | T-015 accepted with documented debt after 4 rounds (§7.4) | r3 blocker + self-report major resolved (haiku r4); remaining AI-line mismatch was in REQUIREMENTS R-EX-4(1), fixed by orchestrator to golden text; minor carried | see card | M1 |
| debt | T-003 accepted with documented debt after 3 rounds (§7.4) | r3 majors fixed after review (lazy add-all spellings via globs, command substitution and xargs; no-space and noclobber redirects) plus the wrapper-option regression, with tests; remaining minors are D-023 residuals (settings/hooks removal, checkout -B, reviewer read-only git false positives, log size cap) | see card | M0 |
| debt | T-028 accepted with documented debt after 2 rounds (§7.4) | remaining major (golden export byte test) is T-041 AC2 and T-038 spec-vs-golden check; minors (README-arch v1 names, confirm_date warning) carried to M2 backend cards | see card | M1 |
--- LLM_VS_CODE rows 10,12,16
38:| 10 | Conflicts that are structural: stated accident date later than the earliest treatment; two different stated accident dates; the same provider spelled two ways | **Code**: a lexicon of accident-date phrases ("date of accident", "DOA", "accident date", "collision on") plus date formats, compared with the earliest record date. Evidence is the stated-date quote and the `Date:` header line(s) of the earliest records. | Comparing two dates is not a language task, and the header line is part of the input text. | Unit test on the sample file with exact character offsets; both quotes ground; the two dates are shown side by side and never merged. No judge needed (arithmetic over quoted text). |
39:| 11 | Conflicts that need meaning: a plan of 12 visits versus discharge at visit 9 | **LLM** proposes a pair as a category and two quoted spans, nothing else | Needs reading comprehension. | **Rung 1:** both quotes ground. **Judge 3:** do these two quotes actually conflict? Human. |
40:| 12 | Pre-existing conditions (flag type `pre_existing`) | **LLM** runs once **per record** and proposes a category and a quote; **and** a researched phrase list is scanned by code on every record as a second signal | Needs language judgment ("low back pain in 2023, resolved"). Running per record means one record's text never reaches the call that decides another record's flags; the phrase list is a second floor, trusted only as far as its measured recall on the golden set. | Quote check; **judge 4** confirms the category. If only the list or only the model fires, the item needs review and says which. |
41:| 13 | Language that weakens causation ("may represent degenerative change", "patient states", missed appointments, "new onset", scene facts such as refusing transport, "no objective findings", a normal exam, an attorney referral) | Same as row 12 (per record). Whether wording is a **patient self-report** is set by code (a phrase match on "patient states/reports"), never by the model. | Same. The tool points at the record's own words; it never rules on causation. | Same, plus golden "must not" checks (no "degenerative" or "traumatic" in the tool's own voice). |
42:| 14 | The wording of every flag | **Code**: a fixed template per flag type and category, filled with dates, source labels and the verbatim quote. For example "Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient)". | A model explaining a flag is another unverified claim, and the place it would be tempted to rule on causation. | The model's output schema has no prose field; a test rejects extra fields. |
43:| 15 | Numbers and dates in a summary or in the paralegal's edit | **Code**: every number, date, dollar figure and left/right/no/not/without in the text must be in the excerpt (or the record's source line / parsed date), and qualifiers in the excerpt must not be dropped from the summary (`SUMMARY_DROPS_QUALIFIER`). | The most likely invented fact is a changed number. A small judge model can miss it; code cannot. | Unit tests: "Pain 9/10" over "Pain 4/10" is flagged; an edit adding "$9,000" shows a warning before acceptance and needs "keep my wording". |
44:| 16 | Instruction-like text inside a record ("ignore previous instructions…") | **Code**: advisory phrase scan that raises a `record_warning` flag. Everything derived from that record needs review, its amounts cannot be charges, the cross-record conflict pass carries the warning, and a banner names the record and says flags may be incomplete. | A phrase list is easy to bypass, so it is a warning, not the defence. The defences are structural (rule 11). | Golden case 07: ordinary entry with a warning; the injected "$50,000" is in no total; the pre-existing flag from another record survives (per-record pass plus phrase list, whose recall on the golden set is a release gate); nothing is accepted. A forged billing line in an untagged record is caught only by her accept (documented as golden variant E, a qa item, not yet in the golden set). |
45:| 17 | Confidence state per item (`verified`, `needs_review`, `rejected`) | **Code**: a fixed rule over the checks (rejected if a grounding check fails; needs review on any doubt; verified only if every check and the judge are positive). | The composition is logic, not opinion. Same input, same state. | Unit tests over the full rule table. `needs_review` sorts first; `rejected` sits in a tray. |
46:| 18 | The "Why?" sentence | **Code**: one template per reason code. | A model explaining its own doubt would be another unverified claim. | Test: every reason code has a template. |
47:| 19 | Sorting, filter to accepted items, export assembly, citations, the total line | **Code**. Every letter line carries its verbatim excerpt, the provider as written, a date of service, and an exhibit/Bates placeholder. The total line is always exactly "Billed charges stated in these records: $X" (accepted charges only), with no clause about anything else. Flags and unclear amounts go to a separate internal-notes block, never the letter. The format is `spec/REQUIREMENTS.md` section 6 and the golden file. | Deterministic, and the letter must never carry anything unquoted. | Unit and E2E: dismissed and pending items never export; every exported excerpt is in the input; same accepted set gives the same bytes. The internal notes list "flagged language quoted in the letter" so the attorney decides whether it stays. |
````

### User / tool · 2026-11-02T01:25:05.774Z

**tool result**
````
--- ORCH decisions re row10 / lexicon gate / engine
23:| D-015 | Paralegal ship-bar score key: `scores.verify_quickly` (1–5) in the paralegal review JSON; ≥ 4 to ship. | One name across REQUIREMENTS, briefs, reviews. | T-013 PM r2 |
26:| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS reports (ambulatory at scene, refused transport, minimal damage), "no objective findings", WNL/full ROM, and attorney referral are **causation** flags citing the excerpt (internal notes only, D-001). Delay to first treatment is not computed (D-017). The lexicon self-check must run over every golden case and report recall per must-flag. | Recall and precision both failed probes; vocab mismatch. | T-009 legal-nurse + claims-adjuster |
32:| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at milestone gates (Tier 2) and the final hiring panel. One agent may cover two persona checklists in one pass. (3) Docs/research cards: max 2 rounds; remaining majors without blockers become documented debt (§7.4) instead of round 3. (4) Briefs ≤ 12 lines, reviewer replies ≤ 10 lines. (5) Researcher moves to sonnet. (6) Heartbeat hourly, not every 20 min. (7) No more harness rounds after M0 r3: residual findings become debt under D-023. | Spend the budget on the product and the submission, not on review churn. | Chris inbox 2026-11-02T00:58Z |
--- REQUIREMENTS ship bar section 7
120:| R-EX-2 | Every entry and charge in the letter carries a source line with the verbatim excerpt. No short-cite mode (D-002). | UT: for every statement and amount line in `letter_text`, the quoted excerpt is a substring of the input after normalization (100%, ship bar 1). Headings and the total line are fixed text. | UT + EV `grounding_rate` |
137:| R-CO-3 | **Nothing in the output that is not in the records.** | Ship bar items 1 and 4. On the sample case every `must_not` item in `evals/golden` holds (no fixed range), including: no disc herniation caused by the collision; "may represent degenerative change" not turned into "degenerative" or "traumatic"; no PT total; the two accident dates not merged; "concussion without loss of consciousness" kept as written. Any hit is a blocker. | EV (negative assertions) + PR (claims-adjuster) |
153:| R-SU-3 | One-page product note. Checklist: the 7 required contents are present as headings (problem and user; what was built; what was cut and why; ship bar with 3–5 testable criteria, how tested, what was found; where AI can fail and how design handles it; model/code split; three metrics, each with a "tells you" line); exactly 3 post-launch metrics; renders to 1 page (≤ 650 words). Numbers in the note equal the latest eval report. | Checklist run by the writer self-check, then PR (hiring-panel, product-manager). | PR |
319:## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)
337:## 8. Assumptions and the hand-off list
373:| 6 | `docs/CONTRACT.md` §5 M2 | "qa injects 20"; closed as permanent. The ship bar here is a rate over the file and the product note quotes the rate. CONTRACT is never edited. | none | closed |
--- CONTRACT 8.3 and 5.2 default backend
memory/ASSUMPTIONS.md:9:| A-001 | No usable API key exists during the build; dev runs on `LLM_BACKEND=claude-cli`. | `.env` value is 10 chars (real keys are ~100). | High | We'd add an anthropic-api cross-check eval run (§5.2). | Chris drops a real key in `.env`; STATE notes it. |
docs/CONTRACT.md:294:**LLM provider abstraction (binding).** There is no API key during development; Chris will add one only when the app goes public. All LLM calls in the app go through one interface (`app/llm/provider.py`: `complete(model, system, user, json_schema) -> dict`) with three backends selected by `LLM_BACKEND`:
docs/CONTRACT.md:451:- Backends by environment: local development runs `LLM_BACKEND=claude-cli` (Chris's claude.ai login, no key); the Docker image and the public Space run `LLM_BACKEND=anthropic-api` and never include the CLI backend. Demo mode: when `ANTHROPIC_API_KEY` is absent in the container, the app serves cached pipeline output for the sample case (recorded from a green eval run) and labels it "cached demo"; when present, live calls run under a per-session rate limit and a daily spend cap. The installer-reviewer's 5-minute test runs the Docker/README path in demo mode, because Zlayt will not have Claude Code or a key.
memory/ENVIRONMENT.md:12:| claude CLI | 2.1.309 | logged in via claude.ai; dev LLM backend (`LLM_BACKEND=claude-cli`) |
memory/DECISIONS.md:133:  - `LLM_BACKEND` selects the backend; models come from config: `GENERATOR_MODEL` (default `claude-sonnet-5-5`), `JUDGE_MODEL` (default `claude-haiku-5-5`, a different model on purpose).
memory/DECISIONS.md:165:  - **Live mode** is for local use with a key (`LLM_BACKEND=anthropic-api` or `claude-cli`). There is **no in-app rate limiter and no in-app spend ledger** (cut, D-020, ADR-015). Spend control is a monthly spend limit set on the provider key in the provider's console (documented in the README; an action for Chris in NEEDS_CHRIS). With `anthropic-api` the app refuses to start unless `PROVIDER_CAP_CONFIRMED=1` is set, so the limit is a conscious step. Input limits stay: 60 000 characters, 40 records.
memory/DECISIONS.md:169:  - Local dev: `make run` on :7860 with `LLM_BACKEND=claude-cli`; tests and eval iteration use `fixture` by default; the live backend is used to record fixtures and for the 3-run determinism check.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:25:16.578Z

**tool call — Bash**
````
{
 "command": "sed -n 319,336p spec/REQUIREMENTS.md; echo \"--- per-card estimate check (Description text)\"; for c in T-027 T-029 T-030 T-031 T-032 T-033 T-034 T-035 T-036 T-037 T-038 T-039 T-040 T-041 T-042 T-043 T-044 T-045 T-046 T-048; do d=$(python3 tools/board.py show $c | sed -n '/^## Description/,/^## Notes/p' | grep -ciE '[0-9]+ ?(min|h)\\b|estimate|timebox'); echo \"$c estimate-mentions-in-Description=$d\"; done",
 "description": "Read ship bar section and check per-card estimates"
}
````

### User / tool · 2026-11-02T01:25:17.744Z

**tool result**
````
## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)

These five are the product note's "good enough to ship" criteria. Metric names are proposed; qa owns the final names in `evals/run`, and updates this table by card if they differ.

| # | Criterion (CONTRACT §8.2) | Number | Measured by | Run with | R-IDs |
|---|---|---|---|---|---|
| 1 | **Grounding** | 100% of exported statements and amounts carry a verbatim excerpt present in the input. Any miss is a blocker. | Eval metric `grounding_rate` (excerpts, providers, amounts, dates; exported items) + export unit test | `python -m evals.run`; `pytest tests/unit` | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| 2 | **Recall** | ≥ 95% of golden timeline entries and ≥ 95% of golden dollar amounts captured across the eval set | `entry_recall`, `amount_recall` | `python -m evals.run` | R-TL-1, R-TL-7, R-CH-1 |
| 3 | **Flags** | Per flag type (gap, conflict, pre_existing, causation): precision ≥ 0.9 and recall ≥ 0.9. 28-day near-miss must not flag; 73-day gap must. | `flag_precision[type]`, `flag_recall[type]`; assertions `gap_28_not_flagged`, `gap_73_flagged`; 29/30/31 unit test | `python -m evals.run`; `pytest tests/unit` | R-FL-1 to R-FL-4 |
| 4 | **No invented facts** | 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding). Judge recall on seeded hallucinations ≥ 95% of every item in `hallucinations.jsonl` (today 40, so at least 33). CONTRACT §5 M2 still says "qa injects 20"; the rate governs permanently and the product note quotes the rate. | `unsupported_count_3run`, `hallucination_catch_rate`, `determinism_3run`, golden `must_not` | `python -m evals.run` | R-TL-4, R-TL-10, R-CH-2, R-CH-7, R-CO-3, R-CO-7 |
| 5 | **Reviewability** | Paralegal persona completes the sample case end to end and scores "I could verify every claim quickly" ≥ 4/5. E2E export test green. | `reviews/<card>-paralegal.md`, key `scores.verify_quickly` (1–5, D-015) ≥ 4; `pytest tests/e2e` (letter block holds accepted entries and charges only, no flag content; `needs_review` first; dismissed never exports; edits labeled; decisions survive reload) | persona review + `pytest tests/e2e` | R-RV-1 to R-RV-6, R-RV-8, R-RV-9, R-EX-1 to R-EX-9 |

Other gates (not ship-bar numbers, still required): `python tools/check_secrets.py` clean; `tools/install_test.sh` under 5 minutes (R-CO-4).

Rule for the product note: report what the eval **found**, including misses, not just the targets.

---

--- per-card estimate check (Description text)
T-027 estimate-mentions-in-Description=0
T-029 estimate-mentions-in-Description=1
T-030 estimate-mentions-in-Description=0
T-031 estimate-mentions-in-Description=0
T-032 estimate-mentions-in-Description=0
T-033 estimate-mentions-in-Description=0
T-034 estimate-mentions-in-Description=0
T-035 estimate-mentions-in-Description=0
T-036 estimate-mentions-in-Description=0
T-037 estimate-mentions-in-Description=0
T-038 estimate-mentions-in-Description=0
T-039 estimate-mentions-in-Description=1
T-040 estimate-mentions-in-Description=0
T-041 estimate-mentions-in-Description=0
T-042 estimate-mentions-in-Description=0
T-043 estimate-mentions-in-Description=0
T-044 estimate-mentions-in-Description=0
T-045 estimate-mentions-in-Description=0
T-046 estimate-mentions-in-Description=0
T-048 estimate-mentions-in-Description=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:25:26.881Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-029 | sed -n '/^## Description/,/^## Notes/p'; python3 tools/board.py show T-039 | sed -n '/^## Description/,/^## Notes/p'; echo \"--- T-045 & T-038 Description\"; python3 tools/board.py show T-045 | sed -n '/^## Description/,/^## Notes/p'; python3 tools/board.py show T-038 | sed -n '/^## Description/,/^## Notes/p'; echo \"--- T-018 AC lines fix file entry 17-18 full\"; python3 -c 'import json;d=json.load(open(\"/Users/arsis/zlayt-pm-project/artifacts/tmp/contract_fixes.json\"));[print(i,x) for i,x in enumerate(d) if i>=17]'",
 "description": "Check Descriptions for estimates and remaining fix entries"
}
````

### User / tool · 2026-11-02T01:25:26.940Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to =17])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:25:29.355Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-029 | sed -n '/^## Description/,/^## Notes/p'; python3 tools/board.py show T-039 | sed -n '/^## Description/,/^## Notes/p'; echo \"--- T-045 Description\"; python3 tools/board.py show T-045 | sed -n '/^## Description/,/^## Notes/p'; echo \"--- T-038 Description\"; python3 tools/board.py show T-038 | sed -n '/^## Description/,/^## Notes/p'",
 "description": "Show Descriptions of T-029, T-039, T-045, T-038"
}
````

### User / tool · 2026-11-02T01:25:29.662Z

**tool result**
````
## Description
Writes the failing tests first so backend and db cards implement against them (backend owns app/**, qa owns tests/**). Grounding/sentences/confidence suites land first because the grounding verifier is the first M2 build (R-TL-2, R-TL-8, R-TL-10, R-FL-5, R-CO-1; LLM_VS_CODE rows 1, 2, 9, 15, 17, 18). Timebox 1 h, grounding suites within the first 30 min.

Plan key: m2-qa-unit-first (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

## Notes (append-only, newest last)
## Description
Writes M3's failing tests first so backend and frontend build against them (R-EX-1 to R-EX-9, R-RV-2, R-RV-3, R-CH-5, R-CH-7, LLM_VS_CODE rows 15 and 19). Timebox 1 h; unit suites first, E2E specs second.

Plan key: m3-qa-tests-first (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

## Notes (append-only, newest last)
--- T-045 Description
## Description
End-to-end proof of the review and export requirements (R-RV-1 to R-RV-6, R-RV-8, R-EX-1 to R-EX-9, R-CO-2, R-CO-5) and runs every sensor before the M3 gate. Covers the CONTRACT M3 chaos-tester inputs.

Plan key: m3-qa-e2e-journey (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

## Notes (append-only, newest last)
--- T-038 Description
## Description
Computes the CONTRACT 8.2 ship bar from the golden set (R-CO-3, R-CO-7, R-TL-4, R-TL-1, R-CH-1, R-FL-1 to R-FL-5, R-EX-2 grounding, R-IN-3, ship bar 1-4). The code-only metrics and the section-6 check can be pre-built while the pipeline card finishes. Attaches the report path required by CONTRACT 8.3.

Plan key: m2-qa-eval-runner (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

## Notes (append-only, newest last)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:09.669Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py",
 "content": "\"\"\"T-018 round-2 applied-check (product-manager-reviewer). Read-only: parses board/cards, docs, memory and the agent file.\nEach check prints APPLIED or NOT-APPLIED with the matching AC number / file line as evidence.\nOwner probe ignores AC text that is itself a review instruction (\"Contract review (T-018): ...\") because a\nworker cannot produce a test from an instruction to 'name' a file.\nRun: python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project\"\"\"\nimport re, sys, json, pathlib, glob, collections\n\nroot = pathlib.Path(sys.argv[1])\nINSTR = re.compile(r\"^Contract review \\(T-018\\):\")\ncards = {}\nfor p in sorted(glob.glob(str(root / \"board/cards/T-0*.md\"))):\n    t = pathlib.Path(p).read_text()\n    cid = re.search(r'^id: \"(T-\\d+)\"', t, re.M).group(1)\n    n = int(cid[2:])\n    if not (n == 48 or (27 <= n <= 46 and n != 28)):\n        continue\n    deps = json.loads(re.search(r'^depends_on: (.*)$', t, re.M).group(1))\n    acs = {}\n    for l in t.splitlines():\n        s = l.strip()\n        if s.startswith('- {\"n\"'):\n            d = json.loads(s[2:])\n            acs[d[\"n\"]] = d[\"text\"]\n    m = re.search(r'^## Description\\n(.*?)\\n## Notes', t, re.S | re.M)\n    cards[cid] = {\n        \"deps\": deps, \"acs\": acs,\n        \"role\": re.search(r'^role: \"(\\w+)\"', t, re.M).group(1),\n        \"priority\": re.search(r'^priority: \"(\\w+)\"', t, re.M).group(1),\n        \"milestone\": re.search(r'^milestone: \"(\\w+)\"', t, re.M).group(1),\n        \"desc\": m.group(1) if m else \"\",\n    }\n\nDOC = (root / \"docs/M2M3_COVERAGE.md\").read_text().splitlines()\nAGENT = (root / \".claude/agents/paralegal-reviewer.md\").read_text()\nT017 = (root / \"board/cards/T-017.md\").read_text()\nLLMVS = (root / \"docs/LLM_VS_CODE.md\").read_text().splitlines()\nSCOPE = (root / \"memory/SCOPE_CUTS.md\").read_text()\nDECIDE = (root / \"memory/ORCHESTRATOR_DECISIONS.md\").read_text()\n\nresults = []\n\ndef card_check(label, src, cids, pattern, want=True):\n    hits = []\n    for c in cids:\n        for k, txt in sorted(cards[c][\"acs\"].items()):\n            if re.search(pattern, txt):\n                hits.append(f\"{c} AC{k}: {txt[:110]}\")\n    ok = (len(hits) > 0) == want\n    results.append((label, src, ok))\n    tag = \"APPLIED\" if ok else \"NOT-APPLIED\"\n    print(f\"[{tag}] {label} ({src}) want={'present' if want else 'absent'} pattern={pattern!r}\")\n    for h in hits[:4]:\n        print(\"     evidence:\", h)\n    if not hits:\n        print(\"     evidence: no matching AC line\")\n\ndef lines_check(label, src, lines, pattern, want=True):\n    hits = [f\"{i+1}: {l[:150]}\" for i, l in enumerate(lines) if re.search(pattern, l)]\n    ok = (len(hits) > 0) == want\n    results.append((label, src, ok))\n    tag = \"APPLIED\" if ok else \"NOT-APPLIED\"\n    print(f\"[{tag}] {label} ({src}) want={'present' if want else 'absent'} pattern={pattern!r}\")\n    for h in hits[:4]:\n        print(\"     evidence:\", h)\n    if not hits:\n        print(\"     evidence: no matching line\")\n\ndef text_check(label, src, text, pattern, want=True):\n    hits = [f\"{i+1}: {l[:150]}\" for i, l in enumerate(text.splitlines()) if re.search(pattern, l)]\n    ok = (len(hits) > 0) == want\n    results.append((label, src, ok))\n    tag = \"APPLIED\" if ok else \"NOT-APPLIED\"\n    print(f\"[{tag}] {label} ({src}) want={'present' if want else 'absent'} pattern={pattern!r}\")\n    for h in hits[:4]:\n        print(\"     evidence:\", h)\n    if not hits:\n        print(\"     evidence: no matching line\")\n\nprint(\"=== PROBE: qa owner of every test file cited in non-instruction AC text (cards T-027..T-046, T-048)\")\nqa = [c for c, v in cards.items() if v[\"role\"] == \"qa\"]\ncited = collections.defaultdict(set)\nfor c, v in cards.items():\n    for k, a in v[\"acs\"].items():\n        if INSTR.search(a):\n            continue\n        for f in re.findall(r\"(test_[a-z_0-9]+)(?:\\.py|::)\", a):\n            cited[f].add(c)\nnone = []\nfor f in sorted(cited):\n    owners = sorted(cited[f] & set(qa))\n    print(f\"   {f:24s} cited_by={sorted(cited[f])} qa_owner={owners or 'NONE'}\")\n    if not owners:\n        none.append(f)\nprint(f\"   qa:NONE count = {len(none)} -> {none}\")\nqa_none_count = len(none)\n\nprint(\"\\n=== PROBE: deps and longest chains\")\nmemo = {}\ndef lp(c):\n    if c in memo:\n        return memo[c]\n    best = [c]\n    for d in cards.get(c, {\"deps\": []})[\"deps\"]:\n        if d in cards:\n            p = lp(d) + [c]\n            if len(p) > len(best):\n                best = p\n    memo[c] = best\n    return best\nprint(\"   longest chain to T-038:\", \" -> \".join(reversed(lp(\"T-038\"))))\nprint(\"   longest chain to T-045:\", \" -> \".join(reversed(lp(\"T-045\"))))\nfor c in [\"T-031\", \"T-042\", \"T-043\", \"T-034\", \"T-036\", \"T-027\"]:\n    print(f\"   deps {c}: {cards[c]['deps']}\")\n\nprint(\"\\n=== PM CONTRACT (6 majors)\")\n# PM-1 critical path / cut order / per-card estimates\nlines_check(\"PM-1a M2 cut order section present\", \"PM major 1 fix\",\n            DOC, r\"M2 cut order\")\nlines_check(\"PM-1b stale 5-card critical path removed from coverage doc\", \"PM major 1 fix\",\n            DOC, r\"T-029 \\(m2-qa-unit-first\\) -> T-030\", want=False)\nlines_check(\"PM-1c stale 'about 4 h' sentence removed\", \"PM major 1 fix\",\n            DOC, r\"This runs about 4 h\", want=False)\nest = [c for c, v in sorted(cards.items()) if not re.search(r\"\\b\\d+ ?(h|min)\\b|[Tt]imebox\", v[\"desc\"])]\nprint(f\"[{'APPLIED' if not est else 'NOT-APPLIED'}] PM-1d per-card estimate in each card Description (PM major 1 fix) cards missing estimate: {len(est)} of {len(cards)}\")\nprint(\"     evidence: cards without an estimate in Description:\", est)\nresults.append((\"PM-1d per-card estimates\", \"PM major 1 fix\", not est))\n\n# PM-2 T-027 raised to P0 with timebox in Description\ncard_check(\"PM-2a T-027 priority P0\", \"PM major 2 fix\", [\"T-027\"], r\"^$\", want=False) if False else None\nprint(f\"[{'APPLIED' if cards['T-027']['priority']=='P0' else 'NOT-APPLIED'}] PM-2a T-027 priority is P0 (PM major 2 fix) evidence: T-027 priority={cards['T-027']['priority']}\")\nresults.append((\"PM-2a T-027 P0\", \"PM major 2 fix\", cards['T-027']['priority'] == 'P0'))\ntext_check(\"PM-2b T-027 Description carries timebox\", \"PM major 2 fix\",\n           cards[\"T-027\"][\"desc\"], r\"[Tt]imebox|\\b\\d+ ?(h|min)\\b\")\n\n# PM-3 fixture cannot ship\ncard_check(\"PM-3a T-038 ship_bar_met false on fixture\", \"PM major 3 fix\", [\"T-038\"],\n           r\"ship_bar_met is false when backend == fixture\")\ncard_check(\"PM-3b T-037 fixtures for all 50 judge lines and SE1-SE5\", \"PM major 3 fix\", [\"T-037\"],\n           r\"hallucinations\\.jsonl.*SE1-SE5|SE1-SE5\")\ncard_check(\"PM-3c T-045 AC4 no longer requires ship_bar_met true on default (fixture) backend\", \"PM major 3 fix\", [\"T-045\"],\n           r\"`python -m evals\\.run` \\(ship_bar_met true\\)\", want=False)\ncard_check(\"PM-3d T-045 claude-cli run named\", \"PM major 3 fix\", [\"T-045\"],\n           r\"LLM_BACKEND=claude-cli python -m evals\\.run\")\n\n# PM-4 regression freshness\ncard_check(\"PM-4a T-038 check-fresh + prompt sha256\", \"PM major 4 fix\", [\"T-038\"],\n           r\"--check-fresh.*exits 1|sha256 of every app/llm/prompts\")\ncard_check(\"PM-4b T-035/T-036 handoff links report with prompt hashes = HEAD\", \"PM major 4 fix\", [\"T-035\", \"T-036\"],\n           r\"prompt hashes equal HEAD\")\n\n# PM-5 verify_quickly owner\nprint(f\"[{'APPLIED' if 'verify_quickly' in AGENT else 'NOT-APPLIED'}] PM-5a paralegal agent body carries scores.verify_quickly (PM major 5 fix) count={AGENT.count('verify_quickly')}\")\nfor ln in AGENT.splitlines():\n    if \"verify_quickly\" in ln:\n        print(\"     evidence:\", ln[:160]); break\nresults.append((\"PM-5a agent body\", \"PM major 5 fix\", 'verify_quickly' in AGENT))\nm3 = [c for c, v in sorted(cards.items()) if v[\"milestone\"] == \"M3\" and any(\"verify_quickly\" in a for a in v[\"acs\"].values())]\nprint(f\"[{'APPLIED' if m3 else 'NOT-APPLIED'}] PM-5b an M3 card (or the M3 gate) requests scores.verify_quickly (PM major 5 fix: 'New orchestrator card (M3)') M3 cards with the key: {m3}\")\nresults.append((\"PM-5b M3 card requests verify_quickly\", \"PM major 5 fix\", bool(m3)))\nlines_check(\"PM-5c ship-bar row -> card table covers rows 1-5\", \"PM major 5 fix\",\n            DOC, r\"^\\| [1-5] \", want=True)\n\n# PM-6 lexicon recall gate\ncard_check(\"PM-6a T-038 lexicon_recall_must_flags metric\", \"PM major 6 fix\", [\"T-038\"],\n           r\"lexicon_recall_must_flags\")\ntext_check(\"PM-6b LLM_VS_CODE rows 12/16 reworded to 'reported, not gated' (or metric ADR)\", \"PM major 6 fix\",\n           \"\\n\".join(LLMVS), r\"reported, not gated\", want=True)\ntext_check(\"PM-6c LLM_VS_CODE row 16 still says 'release gate'\", \"PM major 6 fix\",\n           \"\\n\".join(LLMVS), r\"recall on the golden set is a release gate\", want=False)\n\nprint(\"\\n=== PL CONTRACT (4 majors)\")\ncard_check(\"PL-1a T-044 AC edit survives reload + EDITED ITEMS\", \"PL major 1 fix\", [\"T-044\"],\n           r\"EDITED ITEMS with original and new text\")\ncard_check(\"PL-1b T-039 test_edited_items_section\", \"PL major 1 fix\", [\"T-039\"],\n           r\"test_edited_items_section\")\ncard_check(\"PL-2a T-039 reconciliation: entry 6 pending + 7 of 9 (appended)\", \"PL major 2 fix\", [\"T-039\"],\n           r\"entry 5 and leaving entry 6 pending gives\")\ncard_check(\"PL-2b T-039 AC2 original 'entry 5 gives ... 7 of 9' removed\", \"PL major 2 fix\", [\"T-039\"],\n           r\"dismissing entry 5 gives\", want=False)\ncard_check(\"PL-3 T-043 accident-date two dates, 2026-01-19 quote\", \"PL major 3 fix\", [\"T-043\"],\n           r\"Date of accident per intake form: 2026-01-19\")\ncard_check(\"PL-4a T-042 record 4 could not process in tray\", \"PL major 4 fix\", [\"T-042\"],\n           r\"\\\"could not process\\\" with the reason\")\ncard_check(\"PL-4b T-041 record 4 under RECORDS NOT IN THE TREATMENT SECTION\", \"PL major 4 fix\", [\"T-041\"],\n           r\"RECORDS NOT IN THE TREATMENT SECTION\")\n\nprint(\"\\n=== S CONTRACT (9 majors)\")\ncard_check(\"S-1a T-048 qa card exists with 9 named LLM-stage files\", \"staff major 1 fix\", [\"T-048\"],\n           r\"test_provider\\.py.*test_flag_templates\\.py\")\ncard_check(\"S-1b T-039 names test_api.py and E2E files by file (not instruction text)\", \"staff major 1 fix\", [\"T-039\"],\n           r\"test_api\\.py.*test_(input|timeline|edit|flags_panel)\\.py\", want=True)\nprint(f\"[{'APPLIED' if not qa_none_count else 'NOT-APPLIED'}] S-1c qa:NONE count is 0 after T-048 (staff major 1 acceptance) count={qa_none_count}\")\nresults.append((\"S-1c qa:NONE 0\", \"staff major 1\", qa_none_count == 0))\ncard_check(\"S-2a T-031 depends on T-029\", \"staff major 2 fix\", [\"T-031\"], r\"^$\", want=False) if False else None\nprint(f\"[{'APPLIED' if 'T-029' in cards['T-031']['deps'] else 'NOT-APPLIED'}] S-2a T-031 depends_on includes T-029 evidence: {cards['T-031']['deps']}\")\nprint(f\"[{'APPLIED' if 'T-039' in cards['T-042']['deps'] else 'NOT-APPLIED'}] S-2b T-042 depends_on includes T-039 evidence: {cards['T-042']['deps']}\")\nprint(f\"[{'APPLIED' if {'T-039','T-040'} <= set(cards['T-043']['deps']) else 'NOT-APPLIED'}] S-2c T-043 depends_on includes T-039, T-040 evidence: {cards['T-043']['deps']}\")\nresults.append((\"S-2a\", \"staff major 2\", 'T-029' in cards['T-031']['deps']))\nresults.append((\"S-2b\", \"staff major 2\", 'T-039' in cards['T-042']['deps']))\nresults.append((\"S-2c\", \"staff major 2\", {'T-039','T-040'} <= set(cards['T-043']['deps'])))\ncard_check(\"S-3 T-034 anthropic-api max_retries=0\", \"staff major 3 fix\", [\"T-034\"], r\"max_retries=0\")\ncard_check(\"S-4a T-034 fixture miss raises FixtureMissing\", \"staff major 4 fix\", [\"T-034\"], r\"FixtureMissing\")\ncard_check(\"S-4b T-037 replay reports 0 FixtureMissing\", \"staff major 4 fix\", [\"T-037\"], r\"0 FixtureMissing\")\ncard_check(\"S-5a T-035 judge #2 unsure/error/timeout -> needs_review\", \"staff major 5 fix\", [\"T-035\"], r\"JUDGE_UNSURE\")\ncard_check(\"S-5b T-036 judge #3/#4 error -> needs_review\", \"staff major 5 fix\", [\"T-036\"], r\"judge #3/#4 error or timeout\")\ncard_check(\"S-6 T-029 boundary module list incl. conflicts, flag_templates, injection scan\", \"staff major 6 fix\", [\"T-029\"],\n           r\"flag_templates.*injection scan\")\ncard_check(\"S-7a T-033 or T-036 decides provider-conflict engine (not an 'Either ... or' instruction)\", \"staff major 7 fix\",\n           [\"T-033\", \"T-036\"], r\"^Contract review \\(T-018\\): Either\", want=False)\nlines_check(\"S-7b coverage doc row 10 engine matches LLM_VS_CODE row 10 (Code)\", \"staff major 7 fix\",\n            DOC, r\"^\\| 10 \\| Structural conflicts .*provider variants\", want=False)\ntext_check(\"S-7c ADR/decision recording the row-10 engine\", \"staff major 7 fix\",\n           DECIDE, r\"row 10|provider.*(code|conflict)\", want=True)\ncard_check(\"S-8a T-033 rate note derived by code\", \"staff major 8 fix\", [\"T-033\"], r\"rate note numbers are code-derived\")\ncard_check(\"S-8b T-033 AC1 no longer says '$2,150 only' (damages mention added in place)\", \"staff major 8 fix\", [\"T-033\"],\n           r\"\\$2,150 only\", want=False)\ncard_check(\"S-9a T-039 AC1 case_07 total corrected in place ($8,390 removed)\", \"staff major 9 fix\", [\"T-039\"],\n           r\"incl\\. case_07 with a rate present\", want=False)\ncard_check(\"S-9b T-039 case_07 $420 AC present\", \"staff major 9 fix\", [\"T-039\"], r\"\\$420\\.00\")\ncard_check(\"S-9c T-033 money as int cents\", \"staff major 9 fix\", [\"T-033\"], r\"int 624000\")\n\nprint(\"\\n=== T-017 PLAN REVIEW (4 majors)\")\ntext_check(\"T17-1a coverage doc has pass-condition column\", \"T-017 major 1 fix\", \"\\n\".join(DOC),\n           r\"[Pp]ass condition\", want=True)\ntext_check(\"T17-2a self-check diffing AC numbers against golden\", \"T-017 major 2 fix\", \"\\n\".join(DOC) + DECIDE,\n           r\"self-check|diffed against|diff .* golden\", want=True)\ntext_check(\"T17-3 row-10 mapping in coverage doc (see S-7b)\", \"T-017 major 3 fix\", \"\\n\".join(DOC),\n           r\"T-036 \\(m2-be-llm-flags\\) \\(provider variants\\)\", want=False)\ntext_check(\"T17-4a M2 cut order section\", \"T-017 major 4 fix\", \"\\n\".join(DOC), r\"M2 cut order\", want=True)\ntext_check(\"T17-4b ship-bar row -> card table\", \"T-017 major 4 fix\", \"\\n\".join(DOC), r\"Ship bar row . card\", want=True)\ntext_check(\"T17-4c cut order does not cut lexicon recall target that LLM_VS_CODE calls a release gate\", \"T-017 major 4 fix\",\n           \"\\n\".join(DOC), r\"lexicon held-out target lowered\", want=False)\n\nprint(\"\\n=== MINORS (informational; severities kept as in source)\")\ncard_check(\"m-PM1a T-046 AC5 cut clock from activity log\", \"PM minor 1\", [\"T-046\"], r\"activity\\.jsonl|timestamp\", want=True)\ncard_check(\"m-PM1b T-037 AC1 names the five flag groups with counts\", \"PM minor 1\", [\"T-037\"], r\"gap, conflict, pre_existing\", want=True)\ncard_check(\"m-PM1c T-040 AC5 test_no_token_in_logs\", \"PM minor 1\", [\"T-040\"], r\"test_no_token_in_logs\", want=True)\ntext_check(\"m-PM2 golden variant E in SCOPE_CUTS or a card\", \"PM minor 2\", SCOPE + \"\\n\".join(v for c in cards.values() for v in c[\"acs\"].values()),\n           r\"variant E|forged\", want=True)\ncard_check(\"m-PM4 T-041 AC4 endpoint spelled {token}\", \"PM nit\", [\"T-041\"], r\"\\{token\\}/export\", want=True)\ncard_check(\"m-PL1 T-042 why-template sentence inline on needs_review rows\", \"PL minor 1\", [\"T-042\"], r\"why.template|sentence inline\", want=True)\ncard_check(\"m-PL2 T-043 AC2 full R-CH-3 rate string\", \"PL minor 2\", [\"T-043\"], r\"12 planned; discharged at visit 9\", want=True)\ncard_check(\"m-PL3a T-043 $6,240 charge highlight to record 2\", \"PL minor 3\", [\"T-043\"], r\"ER charges: \\$6,240\", want=True)\ncard_check(\"m-PL3b T-043 injection banner names record 3\", \"PL minor 3\", [\"T-043\"], r\"banner names record 3|names record 3\", want=True)\ncard_check(\"m-PL4 T-043 dismissed-flag reason reaches notes\", \"PL minor 4\", [\"T-043\"], r\"treating elsewhere|dismiss.*reason.*notes\", want=True)\ncard_check(\"m-S1 xfail(strict) red marks instead of --collect-only\", \"staff minor 1\", [\"T-029\", \"T-039\"], r\"xfail\", want=True)\ncard_check(\"m-S2a T-034 AC2 retry changes prompt hash\", \"staff minor 2\", [\"T-034\"], r\"prompt hash\", want=True)\ncard_check(\"m-S2b T-035 judge input isolation\", \"staff minor 2\", [\"T-035\"], r\"judge.*(candidate|isolation)\", want=True)\ncard_check(\"m-S3 T-030 mutation guard for verifier stub\", \"staff minor 3\", [\"T-030\"], r\"monkeypatch|mutation\", want=True)\ncard_check(\"m-S4 T-029 global no-network guard\", \"staff minor 4\", [\"T-029\"], r\"socket|no network|conftest\", want=True)\ntext_check(\"m-T17 T-017 AC2 evidence reworded (row 19 is M3)\", \"T-017 minor\", T017, r\"row 19\", want=True)\n\nprint(\"\\n=== SUMMARY\")\ngating = [r for r in results if r[1].split(\" \")[0] in (\"PM\", \"PL\", \"staff\", \"T-017\")]\nn_app = sum(1 for r in results if r[2])\nn_not = sum(1 for r in results if not r[2])\nprint(f\"checks: {len(results)} applied={n_app} not-applied={n_not}\")\nfor label, src, ok in results:\n    if not ok:\n        print(\"   NOT-APPLIED:\", label, \"|\", src)\n"
}
````

### User / tool · 2026-11-02T01:27:09.775Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:14.270Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py",
 "old_string": "# PM-2 T-027 raised to P0 with timebox in Description\ncard_check(\"PM-2a T-027 priority P0\", \"PM major 2 fix\", [\"T-027\"], r\"^$\", want=False) if False else None\nprint(",
 "new_string": "# PM-2 T-027 raised to P0 with timebox in Description\nprint("
}
````

### User / tool · 2026-11-02T01:27:14.365Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:14.837Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py",
 "old_string": "card_check(\"S-2a T-031 depends on T-029\", \"staff major 2 fix\", [\"T-031\"], r\"^$\", want=False) if False else None\nprint(",
 "new_string": "print("
}
````

### User / tool · 2026-11-02T01:27:14.934Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:16.426Z

**tool call — Bash**
````
{
 "command": "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project > artifacts/review-evidence/T-018-r2-applied-check.out.txt 2>&1; echo \"exit=$?\"; cat artifacts/review-evidence/T-018-r2-applied-check.out.txt",
 "description": "Run the applied-check script and save its output as evidence"
}
````

### User / tool · 2026-11-02T01:27:16.551Z

**tool result**
````
exit=0
=== PROBE: qa owner of every test file cited in non-instruction AC text (cards T-027..T-046, T-048)
   test_amounts             cited_by=['T-029', 'T-033'] qa_owner=['T-029']
   test_api                 cited_by=['T-040', 'T-041'] qa_owner=NONE
   test_audited             cited_by=['T-034', 'T-048'] qa_owner=['T-048']
   test_boundaries          cited_by=['T-029', 'T-030', 'T-041'] qa_owner=['T-029']
   test_charges             cited_by=['T-043'] qa_owner=NONE
   test_confidence          cited_by=['T-029', 'T-030'] qa_owner=['T-029']
   test_conflicts           cited_by=['T-033', 'T-048'] qa_owner=['T-048']
   test_dates               cited_by=['T-029', 'T-032'] qa_owner=['T-029']
   test_db                  cited_by=['T-029', 'T-031'] qa_owner=['T-029']
   test_edit                cited_by=['T-044'] qa_owner=NONE
   test_eval_runner         cited_by=['T-038'] qa_owner=['T-038']
   test_eval_spec_check     cited_by=['T-038'] qa_owner=['T-038']
   test_export              cited_by=['T-039', 'T-041'] qa_owner=['T-039']
   test_export_ui           cited_by=['T-044'] qa_owner=NONE
   test_flag_templates      cited_by=['T-033', 'T-048'] qa_owner=['T-048']
   test_flags_injection     cited_by=['T-036', 'T-048'] qa_owner=['T-048']
   test_flags_panel         cited_by=['T-043'] qa_owner=NONE
   test_flags_sample        cited_by=['T-036', 'T-048'] qa_owner=['T-048']
   test_gaps                cited_by=['T-029', 'T-033'] qa_owner=['T-029']
   test_grounding           cited_by=['T-029', 'T-030'] qa_owner=['T-029']
   test_ingest              cited_by=['T-029', 'T-032'] qa_owner=['T-029']
   test_input               cited_by=['T-042'] qa_owner=NONE
   test_judges              cited_by=['T-035', 'T-048'] qa_owner=['T-048']
   test_keyboard_mobile     cited_by=['T-043'] qa_owner=NONE
   test_ladder_gate         cited_by=['T-045'] qa_owner=['T-045']
   test_letter_isolation    cited_by=['T-045'] qa_owner=['T-045']
   test_pipeline            cited_by=['T-037', 'T-048'] qa_owner=['T-048']
   test_provider            cited_by=['T-034', 'T-048'] qa_owner=['T-048']
   test_review_matrix       cited_by=['T-043'] qa_owner=NONE
   test_review_rules        cited_by=['T-039', 'T-040'] qa_owner=['T-039']
   test_schemas             cited_by=['T-035', 'T-036', 'T-048'] qa_owner=['T-048']
   test_sentences           cited_by=['T-029', 'T-030'] qa_owner=['T-029']
   test_side_by_side        cited_by=['T-046'] qa_owner=NONE
   test_source_record       cited_by=['T-042', 'T-043', 'T-046'] qa_owner=NONE
   test_timeline            cited_by=['T-042'] qa_owner=NONE
   qa:NONE count = 11 -> ['test_api', 'test_charges', 'test_edit', 'test_export_ui', 'test_flags_panel', 'test_input', 'test_keyboard_mobile', 'test_review_matrix', 'test_side_by_side', 'test_source_record', 'test_timeline']

=== PROBE: deps and longest chains
   longest chain to T-038: T-038 -> T-037 -> T-036 -> T-035 -> T-033 -> T-032 -> T-029
   longest chain to T-045: T-045 -> T-044 -> T-043 -> T-040 -> T-037 -> T-036 -> T-035 -> T-033 -> T-032 -> T-029
   deps T-031: ['T-029']
   deps T-042: ['T-039']
   deps T-043: ['T-039', 'T-040', 'T-042']
   deps T-034: ['T-031', 'T-048']
   deps T-036: ['T-027', 'T-033', 'T-035', 'T-048']
   deps T-027: []

=== PM CONTRACT (6 majors)
[APPLIED] PM-1a M2 cut order section present (PM major 1 fix) want=present pattern='M2 cut order'
     evidence: 5: - M2 cut order (never touches ship-bar items): (1) anthropic-api backend stays mocked-SDK only; (2) judge #4 merged into judge #3 prompt; (3) lexicon 
[NOT-APPLIED] PM-1b stale 5-card critical path removed from coverage doc (PM major 1 fix) want=absent pattern='T-029 \\(m2-qa-unit-first\\) -> T-030'
     evidence: 18: Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 (m2-be-grounding) -> T-035 (m2-be-generator-judges) -> T-037 (m2-be-pipeline-cli) -> T-038 (m2-q
[NOT-APPLIED] PM-1c stale 'about 4 h' sentence removed (PM major 1 fix) want=absent pattern='This runs about 4 h'
     evidence: 19: This runs about 4 h, over the 3.5 h budget. If it slips, cut in this order: T-046 (m3-fe-side-by-side), then the other items in the REQUIREMENTS secti
[NOT-APPLIED] PM-1d per-card estimate in each card Description (PM major 1 fix) cards missing estimate: 18 of 20
     evidence: cards without an estimate in Description: ['T-027', 'T-030', 'T-031', 'T-032', 'T-033', 'T-034', 'T-035', 'T-036', 'T-037', 'T-038', 'T-040', 'T-041', 'T-042', 'T-043', 'T-044', 'T-045', 'T-046', 'T-048']
[APPLIED] PM-2a T-027 priority is P0 (PM major 2 fix) evidence: T-027 priority=P0
[NOT-APPLIED] PM-2b T-027 Description carries timebox (PM major 2 fix) want=present pattern='[Tt]imebox|\\b\\d+ ?(h|min)\\b'
     evidence: no matching line
[APPLIED] PM-3a T-038 ship_bar_met false on fixture (PM major 3 fix) want=present pattern='ship_bar_met is false when backend == fixture'
     evidence: T-038 AC6: Contract review (T-018): T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BA
[APPLIED] PM-3b T-037 fixtures for all 50 judge lines and SE1-SE5 (PM major 3 fix) want=present pattern='hallucinations\\.jsonl.*SE1-SE5|SE1-SE5'
     evidence: T-037 AC6: Contract review (T-018): T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BA
     evidence: T-037 AC7: Contract review (T-018): T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash)
[NOT-APPLIED] PM-3c T-045 AC4 no longer requires ship_bar_met true on default (fixture) backend (PM major 3 fix) want=absent pattern='`python -m evals\\.run` \\(ship_bar_met true\\)'
     evidence: T-045 AC4: sensors recorded in evals/reports/m3-sensors.md: `pytest tests/unit`, `python -m evals.run` (ship_bar_met true
[APPLIED] PM-3d T-045 claude-cli run named (PM major 3 fix) want=present pattern='LLM_BACKEND=claude-cli python -m evals\\.run'
     evidence: T-045 AC6: Contract review (T-018): T-038 AC4: 'determinism_3run and unsupported_count_3run are computed only when LLM_BA
[APPLIED] PM-4a T-038 check-fresh + prompt sha256 (PM major 4 fix) want=present pattern='--check-fresh.*exits 1|sha256 of every app/llm/prompts'
     evidence: T-038 AC7: Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/l
[APPLIED] PM-4b T-035/T-036 handoff links report with prompt hashes = HEAD (PM major 4 fix) want=present pattern='prompt hashes equal HEAD'
     evidence: T-035 AC6: Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/l
     evidence: T-036 AC8: Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/l
[APPLIED] PM-5a paralegal agent body carries scores.verify_quickly (PM major 5 fix) count=1
     evidence: **Ship-bar score (D-015):** whenever you review the running app, your review JSON must include `scores.verify_quickly` (1–5): "I could verify every claim quickl
[NOT-APPLIED] PM-5b an M3 card (or the M3 gate) requests scores.verify_quickly (PM major 5 fix: 'New orchestrator card (M3)') M3 cards with the key: []
[APPLIED] PM-5c ship-bar row -> card table covers rows 1-5 (PM major 5 fix) want=present pattern='^\\| [1-5] '
     evidence: 11: | 1 Grounding | T-038 (grounding_rate), T-041 (export grounding) |
     evidence: 12: | 2 Recall | T-038 |
     evidence: 13: | 3 Flags (incl. 28/73) | T-038, T-033 |
     evidence: 14: | 4 No invented facts (live backend only) | T-038, T-037 |
[APPLIED] PM-6a T-038 lexicon_recall_must_flags metric (PM major 6 fix) want=present pattern='lexicon_recall_must_flags'
     evidence: T-038 AC9: Contract review (T-018): T-038 AC1: add `lexicon_recall_must_flags` (pre_existing + causation, per golden case
[NOT-APPLIED] PM-6b LLM_VS_CODE rows 12/16 reworded to 'reported, not gated' (or metric ADR) (PM major 6 fix) want=present pattern='reported, not gated'
     evidence: no matching line
[NOT-APPLIED] PM-6c LLM_VS_CODE row 16 still says 'release gate' (PM major 6 fix) want=absent pattern='recall on the golden set is a release gate'
     evidence: 44: | 16 | Instruction-like text inside a record ("ignore previous instructions…") | **Code**: advisory phrase scan that raises a `record_warning` flag. E

=== PL CONTRACT (4 majors)
[APPLIED] PL-1a T-044 AC edit survives reload + EDITED ITEMS (PL major 1 fix) want=present pattern='EDITED ITEMS with original and new text'
     evidence: T-044 AC6: Contract review (T-018): T-044 AC1 append: 'reload -> edited summary and "edited" label persist; export notes 
[APPLIED] PL-1b T-039 test_edited_items_section (PL major 1 fix) want=present pattern='test_edited_items_section'
     evidence: T-039 AC6: Contract review (T-018): T-044 AC1 append: 'reload -> edited summary and "edited" label persist; export notes 
[APPLIED] PL-2a T-039 reconciliation: entry 6 pending + 7 of 9 (appended) (PL major 2 fix) want=present pattern='entry 5 and leaving entry 6 pending gives'
     evidence: T-039 AC7: Contract review (T-018): T-039 AC2: 'dismissing entry 5 and leaving entry 6 pending gives "Record 5 ... dismis
[NOT-APPLIED] PL-2b T-039 AC2 original 'entry 5 gives ... 7 of 9' removed (PL major 2 fix) want=absent pattern='dismissing entry 5 gives'
     evidence: T-039 AC2: test_export notes: sections in R-EX-4 order, every 'record N' followed by (provider, date), bills-to-request l
[APPLIED] PL-3 T-043 accident-date two dates, 2026-01-19 quote (PL major 3 fix) want=present pattern='Date of accident per intake form: 2026-01-19'
     evidence: T-043 AC6: Contract review (T-018): T-043 AC1 append: 'the accident-date conflict card shows "Date of accident per intake
[APPLIED] PL-4a T-042 record 4 could not process in tray (PL major 4 fix) want=present pattern='\\"could not process\\" with the reason'
     evidence: T-042 AC6: Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI show
[APPLIED] PL-4b T-041 record 4 under RECORDS NOT IN THE TREATMENT SECTION (PL major 4 fix) want=present pattern='RECORDS NOT IN THE TREATMENT SECTION'
     evidence: T-041 AC6: Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI show

=== S CONTRACT (9 majors)
[APPLIED] S-1a T-048 qa card exists with 9 named LLM-stage files (staff major 1 fix) want=present pattern='test_provider\\.py.*test_flag_templates\\.py'
     evidence: T-048 AC1: tests/unit/test_provider.py, test_audited.py, test_schemas.py, test_judges.py, test_flags_sample.py, test_flag
[NOT-APPLIED] S-1b T-039 names test_api.py and E2E files by file (not instruction text) (staff major 1 fix) want=present pattern='test_api\\.py.*test_(input|timeline|edit|flags_panel)\\.py'
     evidence: no matching AC line
[NOT-APPLIED] S-1c qa:NONE count is 0 after T-048 (staff major 1 acceptance) count=11
[APPLIED] S-2a T-031 depends_on includes T-029 evidence: ['T-029']
[APPLIED] S-2b T-042 depends_on includes T-039 evidence: ['T-039']
[APPLIED] S-2c T-043 depends_on includes T-039, T-040 evidence: ['T-039', 'T-040', 'T-042']
[APPLIED] S-3 T-034 anthropic-api max_retries=0 (staff major 3 fix) want=present pattern='max_retries=0'
     evidence: T-034 AC7: Contract review (T-018): T-034 AC4 append: 'anthropic-api client is constructed with max_retries=0 and an expl
[APPLIED] S-4a T-034 fixture miss raises FixtureMissing (staff major 4 fix) want=present pattern='FixtureMissing'
     evidence: T-034 AC8: Contract review (T-018): T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash)
[APPLIED] S-4b T-037 replay reports 0 FixtureMissing (staff major 4 fix) want=present pattern='0 FixtureMissing'
     evidence: T-037 AC7: Contract review (T-018): T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash)
[APPLIED] S-5a T-035 judge #2 unsure/error/timeout -> needs_review (staff major 5 fix) want=present pattern='JUDGE_UNSURE'
     evidence: T-035 AC7: Contract review (T-018): T-035 AC4 append: 'judge #2 unsure, error or timeout -> needs_review (JUDGE_UNSURE / 
[APPLIED] S-5b T-036 judge #3/#4 error -> needs_review (staff major 5 fix) want=present pattern='judge #3/#4 error or timeout'
     evidence: T-036 AC9: Contract review (T-018): T-035 AC4 append: 'judge #2 unsure, error or timeout -> needs_review (JUDGE_UNSURE / 
[APPLIED] S-6 T-029 boundary module list incl. conflicts, flag_templates, injection scan (staff major 6 fix) want=present pattern='flag_templates.*injection scan'
     evidence: T-029 AC7: Contract review (T-018): T-029 AC4: module list = sentences, grounding, confidence, why, dates, ingest/dedupe,
[NOT-APPLIED] S-7a T-033 or T-036 decides provider-conflict engine (not an 'Either ... or' instruction) (staff major 7 fix) want=absent pattern='^Contract review \\(T-018\\): Either'
     evidence: T-033 AC6: Contract review (T-018): Either T-033 gains AC6 'case_05 provider conflict raised by code (normalized-name rul
     evidence: T-036 AC7: Contract review (T-018): Either raise T-027 to P0 with a timebox in its Description, or remove T-027 from T-03
     evidence: T-036 AC10: Contract review (T-018): Either T-033 gains AC6 'case_05 provider conflict raised by code (normalized-name rul
[NOT-APPLIED] S-7b coverage doc row 10 engine matches LLM_VS_CODE row 10 (Code) (staff major 7 fix) want=absent pattern='^\\| 10 \\| Structural conflicts .*provider variants'
     evidence: 96: | 10 | Structural conflicts | T-033 (m2-be-amounts-gaps) (accident date), T-036 (m2-be-llm-flags) (provider variants) |
[APPLIED] S-7c ADR/decision recording the row-10 engine (staff major 7 fix) want=present pattern='row 10|provider.*(code|conflict)'
     evidence: 28: | D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a record
[APPLIED] S-8a T-033 rate note derived by code (staff major 8 fix) want=present pattern='rate note numbers are code-derived'
     evidence: T-033 AC7: Contract review (T-018): T-033 new AC: 'rate note numbers are code-derived: N planned from the "Plan of care: 
[NOT-APPLIED] S-8b T-033 AC1 no longer says '$2,150 only' (damages mention added in place) (staff major 8 fix) want=absent pattern='\\$2,150 only'
     evidence: T-033 AC1: `pytest tests/unit/test_amounts.py` green: sample yields $6,240, $185, $2,150 only; 20 phrasings -> rate; $1,2
[NOT-APPLIED] S-9a T-039 AC1 case_07 total corrected in place ($8,390 removed) (staff major 9 fix) want=absent pattern='incl\\. case_07 with a rate present'
     evidence: T-039 AC1: tests/unit/test_export.py: every letter line is heading / date+provider / summary / Source quote / amount / to
[APPLIED] S-9b T-039 case_07 $420 AC present (staff major 9 fix) want=present pattern='\\$420\\.00'
     evidence: T-039 AC9: Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is e
[APPLIED] S-9c T-033 money as int cents (staff major 9 fix) want=present pattern='int 624000'
     evidence: T-033 AC8: Contract review (T-018): T-039 AC1: 'on sample the line is ...$8,390.00; on case_07 with $420 accepted it is e

=== T-017 PLAN REVIEW (4 majors)
[NOT-APPLIED] T17-1a coverage doc has pass-condition column (T-017 major 1 fix) want=present pattern='[Pp]ass condition'
     evidence: no matching line
[APPLIED] T17-2a self-check diffing AC numbers against golden (T-017 major 2 fix) want=present pattern='self-check|diffed against|diff .* golden'
     evidence: 133: | D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_rep
[NOT-APPLIED] T17-3 row-10 mapping in coverage doc (see S-7b) (T-017 major 3 fix) want=absent pattern='T-036 \\(m2-be-llm-flags\\) \\(provider variants\\)'
     evidence: 96: | 10 | Structural conflicts | T-033 (m2-be-amounts-gaps) (accident date), T-036 (m2-be-llm-flags) (provider variants) |
[APPLIED] T17-4a M2 cut order section (T-017 major 4 fix) want=present pattern='M2 cut order'
     evidence: 5: - M2 cut order (never touches ship-bar items): (1) anthropic-api backend stays mocked-SDK only; (2) judge #4 merged into judge #3 prompt; (3) lexicon 
[APPLIED] T17-4b ship-bar row -> card table (T-017 major 4 fix) want=present pattern='Ship bar row . card'
     evidence: 8: ## Ship bar row → card
[NOT-APPLIED] T17-4c cut order does not cut lexicon recall target that LLM_VS_CODE calls a release gate (T-017 major 4 fix) want=absent pattern='lexicon held-out target lowered'
     evidence: 5: - M2 cut order (never touches ship-bar items): (1) anthropic-api backend stays mocked-SDK only; (2) judge #4 merged into judge #3 prompt; (3) lexicon 

=== MINORS (informational; severities kept as in source)
[NOT-APPLIED] m-PM1a T-046 AC5 cut clock from activity log (PM minor 1) want=present pattern='activity\\.jsonl|timestamp'
     evidence: no matching AC line
[NOT-APPLIED] m-PM1b T-037 AC1 names the five flag groups with counts (PM minor 1) want=present pattern='gap, conflict, pre_existing'
     evidence: no matching AC line
[NOT-APPLIED] m-PM1c T-040 AC5 test_no_token_in_logs (PM minor 1) want=present pattern='test_no_token_in_logs'
     evidence: no matching AC line
[NOT-APPLIED] m-PM2 golden variant E in SCOPE_CUTS or a card (PM minor 2) want=present pattern='variant E|forged'
     evidence: no matching line
[NOT-APPLIED] m-PM4 T-041 AC4 endpoint spelled {token} (PM nit) want=present pattern='\\{token\\}/export'
     evidence: no matching AC line
[NOT-APPLIED] m-PL1 T-042 why-template sentence inline on needs_review rows (PL minor 1) want=present pattern='why.template|sentence inline'
     evidence: no matching AC line
[NOT-APPLIED] m-PL2 T-043 AC2 full R-CH-3 rate string (PL minor 2) want=present pattern='12 planned; discharged at visit 9'
     evidence: no matching AC line
[NOT-APPLIED] m-PL3a T-043 $6,240 charge highlight to record 2 (PL minor 3) want=present pattern='ER charges: \\$6,240'
     evidence: no matching AC line
[NOT-APPLIED] m-PL3b T-043 injection banner names record 3 (PL minor 3) want=present pattern='banner names record 3|names record 3'
     evidence: no matching AC line
[NOT-APPLIED] m-PL4 T-043 dismissed-flag reason reaches notes (PL minor 4) want=present pattern='treating elsewhere|dismiss.*reason.*notes'
     evidence: no matching AC line
[NOT-APPLIED] m-S1 xfail(strict) red marks instead of --collect-only (staff minor 1) want=present pattern='xfail'
     evidence: no matching AC line
[APPLIED] m-S2a T-034 AC2 retry changes prompt hash (staff minor 2) want=present pattern='prompt hash'
     evidence: T-034 AC8: Contract review (T-018): T-034 AC1 append: 'a fixture miss raises FixtureMissing (logged with the prompt hash)
[NOT-APPLIED] m-S2b T-035 judge input isolation (staff minor 2) want=present pattern='judge.*(candidate|isolation)'
     evidence: no matching AC line
[NOT-APPLIED] m-S3 T-030 mutation guard for verifier stub (staff minor 3) want=present pattern='monkeypatch|mutation'
     evidence: no matching AC line
[NOT-APPLIED] m-S4 T-029 global no-network guard (staff minor 4) want=present pattern='socket|no network|conftest'
     evidence: no matching AC line
[APPLIED] m-T17 T-017 AC2 evidence reworded (row 19 is M3) (T-017 minor) want=present pattern='row 19'
     evidence: 39:     - [minor] T-017 AC2 evidence overstates: not every LLM_VS_CODE row maps to an M2 card — fix: Reword the evidence: 'rows 1-18, 20 have an M2 card; 

=== SUMMARY
checks: 67 applied=35 not-applied=32
   NOT-APPLIED: PM-1b stale 5-card critical path removed from coverage doc | PM major 1 fix
   NOT-APPLIED: PM-1c stale 'about 4 h' sentence removed | PM major 1 fix
   NOT-APPLIED: PM-1d per-card estimates | PM major 1 fix
   NOT-APPLIED: PM-2b T-027 Description carries timebox | PM major 2 fix
   NOT-APPLIED: PM-3c T-045 AC4 no longer requires ship_bar_met true on default (fixture) backend | PM major 3 fix
   NOT-APPLIED: PM-5b M3 card requests verify_quickly | PM major 5 fix
   NOT-APPLIED: PM-6b LLM_VS_CODE rows 12/16 reworded to 'reported, not gated' (or metric ADR) | PM major 6 fix
   NOT-APPLIED: PM-6c LLM_VS_CODE row 16 still says 'release gate' | PM major 6 fix
   NOT-APPLIED: PL-2b T-039 AC2 original 'entry 5 gives ... 7 of 9' removed | PL major 2 fix
   NOT-APPLIED: S-1b T-039 names test_api.py and E2E files by file (not instruction text) | staff major 1 fix
   NOT-APPLIED: S-1c qa:NONE 0 | staff major 1
   NOT-APPLIED: S-7a T-033 or T-036 decides provider-conflict engine (not an 'Either ... or' instruction) | staff major 7 fix
   NOT-APPLIED: S-7b coverage doc row 10 engine matches LLM_VS_CODE row 10 (Code) | staff major 7 fix
   NOT-APPLIED: S-8b T-033 AC1 no longer says '$2,150 only' (damages mention added in place) | staff major 8 fix
   NOT-APPLIED: S-9a T-039 AC1 case_07 total corrected in place ($8,390 removed) | staff major 9 fix
   NOT-APPLIED: T17-1a coverage doc has pass-condition column | T-017 major 1 fix
   NOT-APPLIED: T17-3 row-10 mapping in coverage doc (see S-7b) | T-017 major 3 fix
   NOT-APPLIED: T17-4c cut order does not cut lexicon recall target that LLM_VS_CODE calls a release gate | T-017 major 4 fix
   NOT-APPLIED: m-PM1a T-046 AC5 cut clock from activity log | PM minor 1
   NOT-APPLIED: m-PM1b T-037 AC1 names the five flag groups with counts | PM minor 1
   NOT-APPLIED: m-PM1c T-040 AC5 test_no_token_in_logs | PM minor 1
   NOT-APPLIED: m-PM2 golden variant E in SCOPE_CUTS or a card | PM minor 2
   NOT-APPLIED: m-PM4 T-041 AC4 endpoint spelled {token} | PM nit
   NOT-APPLIED: m-PL1 T-042 why-template sentence inline on needs_review rows | PL minor 1
   NOT-APPLIED: m-PL2 T-043 AC2 full R-CH-3 rate string | PL minor 2
   NOT-APPLIED: m-PL3a T-043 $6,240 charge highlight to record 2 | PL minor 3
   NOT-APPLIED: m-PL3b T-043 injection banner names record 3 | PL minor 3
   NOT-APPLIED: m-PL4 T-043 dismissed-flag reason reaches notes | PL minor 4
   NOT-APPLIED: m-S1 xfail(strict) red marks instead of --collect-only | staff minor 1
   NOT-APPLIED: m-S2b T-035 judge input isolation | staff minor 2
   NOT-APPLIED: m-S3 T-030 mutation guard for verifier stub | staff minor 3
   NOT-APPLIED: m-S4 T-029 global no-network guard | staff minor 4
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:37.618Z

**tool call — Bash**
````
{
 "command": "grep -rln 'case_05' docs memory spec 2>/dev/null; echo ---; grep -rn 'case_05' memory/ORCHESTRATOR_DECISIONS.md memory/DECISIONS.md docs/adr 2>/dev/null | head -5; echo ---; grep -n 'row 10\\|row 16\\|release gate' memory/*.md docs/*.md 2>/dev/null | head -10; echo ---; python3 tools/board.py show T-017 | grep -n '\"n\": 2'",
 "description": "Search for row-10 engine decision and T-017 AC2 evidence"
}
````

### User / tool · 2026-11-02T01:27:37.778Z

**tool result**
````
spec/REQUIREMENTS.md
---
---
docs/LLM_VS_CODE.md:44:| 16 | Instruction-like text inside a record ("ignore previous instructions…") | **Code**: advisory phrase scan that raises a `record_warning` flag. Everything derived from that record needs review, its amounts cannot be charges, the cross-record conflict pass carries the warning, and a banner names the record and says flags may be incomplete. | A phrase list is easy to bypass, so it is a warning, not the defence. The defences are structural (rule 11). | Golden case 07: ordinary entry with a warning; the injected "$50,000" is in no total; the pre-existing flag from another record survives (per-record pass plus phrase list, whose recall on the golden set is a release gate); nothing is accepted. A forged billing line in an untagged record is caught only by her accept (documented as golden variant E, a qa item, not yet in the golden set). |
---
20:  - {"n": 2, "text": "every row of the docs/LLM_VS_CODE.md table maps to an M2 card with its validation named in AC", "done": true, "evidence": "docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped, each card AC names its test/eval"}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:41.007Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py",
 "old_string": "def card_check(label, src, cids, pattern, want=True):\n    hits = []\n    for c in cids:\n        for k, txt in sorted(cards[c][\"acs\"].items()):\n            if re.search(pattern, txt):\n                hits.append(f\"{c} AC{k}: {txt[:110]}\")",
 "new_string": "def window(txt, pattern, pad=70):\n    m = re.search(pattern, txt)\n    return txt[max(0, m.start() - pad): m.end() + pad]\n\ndef card_check(label, src, cids, pattern, want=True):\n    hits = []\n    for c in cids:\n        for k, txt in sorted(cards[c][\"acs\"].items()):\n            if re.search(pattern, txt):\n                hits.append(f\"{c} AC{k}: ...{window(txt, pattern)}...\")"
}
````

### User / tool · 2026-11-02T01:27:41.104Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:42.067Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py",
 "old_string": "text_check(\"T17-2a self-check diffing AC numbers against golden\", \"T-017 major 2 fix\", \"\\n\".join(DOC) + DECIDE,\n           r\"self-check|diffed against|diff .* golden\", want=True)",
 "new_string": "text_check(\"T17-2a plan self-check: AC numbers diffed against golden (in coverage doc)\", \"T-017 major 2 fix\", \"\\n\".join(DOC),\n           r\"self-check|every number in an AC|diffed against\", want=True)"
}
````

### User / tool · 2026-11-02T01:27:42.163Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:42.986Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py",
 "old_string": "text_check(\"S-7c ADR/decision recording the row-10 engine\", \"staff major 7 fix\",\n           DECIDE, r\"row 10|provider.*(code|conflict)\", want=True)",
 "new_string": "text_check(\"S-7c ADR/decision recording the row-10 engine (ORCHESTRATOR_DECISIONS)\", \"staff major 7 fix\",\n           DECIDE, r\"row 10|case_05\", want=True)"
}
````

### User / tool · 2026-11-02T01:27:43.086Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:44.149Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py",
 "old_string": "card_check(\"m-S2a T-034 AC2 retry changes prompt hash\", \"staff minor 2\", [\"T-034\"], r\"prompt hash\", want=True)",
 "new_string": "print(f\"[{'APPLIED' if 'prompt hash' in cards['T-034']['acs'][2] else 'NOT-APPLIED'}] m-S2a T-034 AC2 retry changes prompt hash (staff minor 2) AC2 text: {cards['T-034']['acs'][2][:140]}\")\nresults.append((\"m-S2a\", \"staff minor 2\", 'prompt hash' in cards['T-034']['acs'][2]))"
}
````

### User / tool · 2026-11-02T01:27:44.244Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:45.787Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py",
 "old_string": "text_check(\"m-T17 T-017 AC2 evidence reworded (row 19 is M3)\", \"T-017 minor\", T017, r\"row 19\", want=True)",
 "new_string": "text_check(\"m-T17 T-017 AC2 evidence reworded: 'rows 1-20 all mapped' removed\", \"T-017 minor\", T017,\n           r\"rows 1-20 all mapped\", want=False)\ndup = collections.defaultdict(set)\nfor c, v in cards.items():\n    for a in v[\"acs\"].values():\n        if INSTR.search(a):\n            dup[a[:90]].add(c)\nmulti = {k: sorted(v) for k, v in dup.items() if len(v) > 1}\nprint(f\"[INFO] instruction-style 'Contract review (T-018):' ACs copied onto more than one card: {len(multi)} distinct texts\")\nfor k, v in sorted(multi.items(), key=lambda kv: kv[0]):\n    print(f\"     {v}: {k}...\")"
}
````

### User / tool · 2026-11-02T01:27:45.884Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:50.327Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py",
 "old_string": "text_check(\"m-T17 T-017 AC2 evidence reworded: 'rows 1-20 all mapped' removed\", \"T-017 minor\", T017,\n           r\"rows 1-20 all mapped\", want=False)",
 "new_string": "FRONT17 = T017.split(\"---\")[1]  # frontmatter only (AC evidence); Notes history is append-only\ntext_check(\"m-T17 T-017 AC2 frontmatter evidence reworded: 'rows 1-20 all mapped' removed\", \"T-017 minor\", FRONT17,\n           r\"rows 1-20 all mapped\", want=False)"
}
````

### User / tool · 2026-11-02T01:27:50.421Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:51.393Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py",
 "old_string": "text_check(\"PM-6b LLM_VS_CODE rows 12/16 reworded to 'reported, not gated' (or metric ADR)\", \"PM major 6 fix\",",
 "new_string": "card_check(\"PM-6d T-038 lexicon gate decided (no open 'or edit LLM_VS_CODE rows 12/16' alternative)\", \"PM major 6 fix\", [\"T-038\"],\n           r\"or edit LLM_VS_CODE rows 12/16\", want=False)\ntext_check(\"PM-6b LLM_VS_CODE rows 12/16 reworded to 'reported, not gated' (or metric ADR)\", \"PM major 6 fix\","
}
````

### User / tool · 2026-11-02T01:27:51.488Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:27:54.407Z

**tool call — Bash**
````
{
 "command": "python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project > artifacts/review-evidence/T-018-r2-applied-check.out.txt 2>&1; echo \"exit=$?\"; grep -n -A3 'PM-1b\\|PM-6a\\|PM-6d\\|PL-2b\\|S-1b\\|S-7c\\|S-8b\\|S-9a\\|T17-2a\\|m-S2a\\|m-T17\\|INFO' artifacts/review-evidence/T-018-r2-applied-check.out.txt | head -120; echo; tail -45 artifacts/review-evidence/T-018-r2-applied-check.out.txt | grep -A200 '=== SUMMARY' | head -3; grep -c 'APPLIED\\]' artifacts/review-evidence/T-018-r2-applied-check.out.txt; grep -c 'NOT-APPLIED\\]' artifacts/review-evidence/T-018-r2-applied-check.out.txt",
 "description": "Re-run the applied-check and show key evidence lines"
}
````

### User / tool · 2026-11-02T01:27:54.564Z

**tool result**
````
exit=0
52:[NOT-APPLIED] PM-1b stale 5-card critical path removed from coverage doc (PM major 1 fix) want=absent pattern='T-029 \\(m2-qa-unit-first\\) -> T-030'
53-     evidence: 18: Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 (m2-be-grounding) -> T-035 (m2-be-generator-judges) -> T-037 (m2-be-pipeline-cli) -> T-038 (m2-q
54-[NOT-APPLIED] PM-1c stale 'about 4 h' sentence removed (PM major 1 fix) want=absent pattern='This runs about 4 h'
55-     evidence: 19: This runs about 4 h, over the 3.5 h budget. If it slips, cut in this order: T-046 (m3-fe-side-by-side), then the other items in the REQUIREMENTS secti
--
83:[APPLIED] PM-6a T-038 lexicon_recall_must_flags metric (PM major 6 fix) want=present pattern='lexicon_recall_must_flags'
84-     evidence: T-038 AC9: ...Contract review (T-018): T-038 AC1: add `lexicon_recall_must_flags` (pre_existing + causation, per golden case, pooled) with R-IDs R-FL-...
85:[NOT-APPLIED] PM-6d T-038 lexicon gate decided (no open 'or edit LLM_VS_CODE rows 12/16' alternative) (PM major 6 fix) want=absent pattern='or edit LLM_VS_CODE rows 12/16'
86-     evidence: T-038 AC9: ...Ds R-FL-3, R-RV-6, and state the threshold in REQUIREMENTS §7 by ADR, or edit LLM_VS_CODE rows 12/16 to 'reported, not gated'....
87-[NOT-APPLIED] PM-6b LLM_VS_CODE rows 12/16 reworded to 'reported, not gated' (or metric ADR) (PM major 6 fix) want=present pattern='reported, not gated'
88-     evidence: no matching line
--
99:[NOT-APPLIED] PL-2b T-039 AC2 original 'entry 5 gives ... 7 of 9' removed (PL major 2 fix) want=absent pattern='dismissing entry 5 gives'
100-     evidence: T-039 AC2: ...'record N' followed by (provider, date), bills-to-request line exact, dismissing entry 5 gives 'Record 5 ... dismissed' and 7 of 9 (R-EX-4, R-EX-7)...
101-[APPLIED] PL-3 T-043 accident-date two dates, 2026-01-19 quote (PL major 3 fix) want=present pattern='Date of accident per intake form: 2026-01-19'
102-     evidence: T-043 AC6: ...ew (T-018): T-043 AC1 append: 'the accident-date conflict card shows "Date of accident per intake form: 2026-01-19." and the 2026-01-09 header line(s) of records 1 and 2 side by side, ...
--
111:[NOT-APPLIED] S-1b T-039 names test_api.py and E2E files by file (not instruction text) (staff major 1 fix) want=present pattern='test_api\\.py.*test_(input|timeline|edit|flags_panel)\\.py'
112-     evidence: no matching AC line
113-[NOT-APPLIED] S-1c qa:NONE count is 0 after T-048 (staff major 1 acceptance) count=11
114-[APPLIED] S-2a T-031 depends_on includes T-029 evidence: ['T-029']
--
135:[NOT-APPLIED] S-7c ADR/decision recording the row-10 engine (ORCHESTRATOR_DECISIONS) (staff major 7 fix) want=present pattern='row 10|case_05'
136-     evidence: no matching line
137-[APPLIED] S-8a T-033 rate note derived by code (staff major 8 fix) want=present pattern='rate note numbers are code-derived'
138-     evidence: T-033 AC7: ...Contract review (T-018): T-033 new AC: 'rate note numbers are code-derived: N planned from the "Plan of care: N visits" match in a record with t...
139:[NOT-APPLIED] S-8b T-033 AC1 no longer says '$2,150 only' (damages mention added in place) (staff major 8 fix) want=absent pattern='\\$2,150 only'
140-     evidence: T-033 AC1: ...pytest tests/unit/test_amounts.py` green: sample yields $6,240, $185, $2,150 only; 20 phrasings -> rate; $1,2OO and $9S.00 unclear/null; doses (10 mg e...
141:[NOT-APPLIED] S-9a T-039 AC1 case_07 total corrected in place ($8,390 removed) (staff major 9 fix) want=absent pattern='incl\\. case_07 with a rate present'
142-     evidence: T-039 AC1: ...otal line exactly 'Billed charges stated in these records: $8,390.00' incl. case_07 with a rate present; same accepted set -> byte-identical output; fixture sample equals sa...
143-[APPLIED] S-9b T-039 case_07 $420 AC present (staff major 9 fix) want=present pattern='\\$420\\.00'
144-     evidence: T-039 AC9: ... $420 accepted it is exactly "Billed charges stated in these records: $420.00"; with the $185 rate non-dismissed the sample line is unchanged'. T-0...
--
151:[NOT-APPLIED] T17-2a plan self-check: AC numbers diffed against golden (in coverage doc) (T-017 major 2 fix) want=present pattern='self-check|every number in an AC|diffed against'
152-     evidence: no matching line
153-[NOT-APPLIED] T17-3 row-10 mapping in coverage doc (see S-7b) (T-017 major 3 fix) want=absent pattern='T-036 \\(m2-be-llm-flags\\) \\(provider variants\\)'
154-     evidence: 96: | 10 | Structural conflicts | T-033 (m2-be-amounts-gaps) (accident date), T-036 (m2-be-llm-flags) (provider variants) |
--
185:[NOT-APPLIED] m-S2a T-034 AC2 retry changes prompt hash (staff minor 2) AC2 text: audited.py: fails 3 attempts -> LLM_FAILED_AFTER_RETRIES and app stays usable; fails twice then succeeds -> output returned; one llm_calls r
186-[NOT-APPLIED] m-S2b T-035 judge input isolation (staff minor 2) want=present pattern='judge.*(candidate|isolation)'
187-     evidence: no matching AC line
188-[NOT-APPLIED] m-S3 T-030 mutation guard for verifier stub (staff minor 3) want=present pattern='monkeypatch|mutation'
--
192:[NOT-APPLIED] m-T17 T-017 AC2 frontmatter evidence reworded: 'rows 1-20 all mapped' removed (T-017 minor) want=absent pattern='rows 1-20 all mapped'
193-     evidence: 20:   - {"n": 2, "text": "every row of the docs/LLM_VS_CODE.md table maps to an M2 card with its validation named in AC", "done": true, "evidence": "docs/
194:[INFO] instruction-style 'Contract review (T-018):' ACs copied onto more than one card: 11 distinct texts
195-     ['T-033', 'T-036']: Contract review (T-018): Either T-033 gains AC6 'case_05 provider conflict raised by code ...
196-     ['T-031', 'T-034', 'T-036']: Contract review (T-018): Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card...
197-     ['T-029', 'T-039']: Contract review (T-018): T-029 AC4 or a new qa card 'M2 LLM-stage tests first' (deps [], b...
--
209:   NOT-APPLIED: PM-1b stale 5-card critical path removed from coverage doc | PM major 1 fix
210-   NOT-APPLIED: PM-1c stale 'about 4 h' sentence removed | PM major 1 fix
211-   NOT-APPLIED: PM-1d per-card estimates | PM major 1 fix
212-   NOT-APPLIED: PM-2b T-027 Description carries timebox | PM major 2 fix
--
215:   NOT-APPLIED: PM-6d T-038 lexicon gate decided (no open 'or edit LLM_VS_CODE rows 12/16' alternative) | PM major 6 fix
216-   NOT-APPLIED: PM-6b LLM_VS_CODE rows 12/16 reworded to 'reported, not gated' (or metric ADR) | PM major 6 fix
217-   NOT-APPLIED: PM-6c LLM_VS_CODE row 16 still says 'release gate' | PM major 6 fix
218:   NOT-APPLIED: PL-2b T-039 AC2 original 'entry 5 gives ... 7 of 9' removed | PL major 2 fix
219:   NOT-APPLIED: S-1b T-039 names test_api.py and E2E files by file (not instruction text) | staff major 1 fix
220-   NOT-APPLIED: S-1c qa:NONE 0 | staff major 1
221-   NOT-APPLIED: S-7a T-033 or T-036 decides provider-conflict engine (not an 'Either ... or' instruction) | staff major 7 fix
222-   NOT-APPLIED: S-7b coverage doc row 10 engine matches LLM_VS_CODE row 10 (Code) | staff major 7 fix
223:   NOT-APPLIED: S-7c ADR/decision recording the row-10 engine (ORCHESTRATOR_DECISIONS) | staff major 7 fix
224:   NOT-APPLIED: S-8b T-033 AC1 no longer says '$2,150 only' (damages mention added in place) | staff major 8 fix
225:   NOT-APPLIED: S-9a T-039 AC1 case_07 total corrected in place ($8,390 removed) | staff major 9 fix
226-   NOT-APPLIED: T17-1a coverage doc has pass-condition column | T-017 major 1 fix
227:   NOT-APPLIED: T17-2a plan self-check: AC numbers diffed against golden (in coverage doc) | T-017 major 2 fix
228-   NOT-APPLIED: T17-3 row-10 mapping in coverage doc (see S-7b) | T-017 major 3 fix
229-   NOT-APPLIED: T17-4c cut order does not cut lexicon recall target that LLM_VS_CODE calls a release gate | T-017 major 4 fix
230-   NOT-APPLIED: m-PM1a T-046 AC5 cut clock from activity log | PM minor 1
--
241:   NOT-APPLIED: m-S2a | staff minor 2
242-   NOT-APPLIED: m-S2b T-035 judge input isolation | staff minor 2
243-   NOT-APPLIED: m-S3 T-030 mutation guard for verifier stub | staff minor 3
244-   NOT-APPLIED: m-S4 T-029 global no-network guard | staff minor 4
245:   NOT-APPLIED: m-T17 T-017 AC2 frontmatter evidence reworded: 'rows 1-20 all mapped' removed | T-017 minor

=== SUMMARY
checks: 68 applied=31 not-applied=37
   NOT-APPLIED: PM-1b stale 5-card critical path removed from coverage doc | PM major 1 fix
68
37
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:28:39.200Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -15; echo \"exit=$?\"; grep -n 'def cmd_validate\\|def validate\\|reviews/' tools/board.py | head -20",
 "description": "Run read-only board validate and check its review rules"
}
````

### User / tool · 2026-11-02T01:28:39.351Z

**tool result**
````
ok (48 file(s))
exit=0
896:def validate_review_file(p: Path) -> list[str]:
927:def cmd_validate(a):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:28:40.781Z

**tool call — Bash**
````
{
 "command": "sed -n 896,935p tools/board.py",
 "description": "Read the review-file validator rules in board.py"
}
````

### User / tool · 2026-11-02T01:28:40.863Z

**tool result**
````
def validate_review_file(p: Path) -> list[str]:
    errs = []
    if p.name.startswith("GATE-") or p.name.startswith("CONTRACT-"):
        if len(p.read_text(encoding="utf-8").strip()) < 50:
            errs.append("gate summary is empty")
        return errs
    d = review_json(p)
    if d is None:
        return ["review must contain a ```json block (Appendix D.2) with a verdict"]
    for k in ("card", "persona", "verdict", "findings", "exercised"):
        if k not in d:
            errs.append(f"review JSON missing '{k}'")
    if d.get("verdict") not in VERDICTS:
        errs.append(f"verdict must be one of {VERDICTS}")
    if not isinstance(d.get("findings"), list):
        return ["review JSON 'findings' must be a list (use [] for none)"]
    sev = [f.get("severity") for f in d.get("findings", []) if isinstance(f, dict)]
    for f in d.get("findings", []):
        if not isinstance(f, dict) or f.get("severity") not in ("blocker", "major", "minor", "nit"):
            errs.append(f"finding has bad severity: {str(f)[:80]}")
        elif not f.get("evidence"):
            errs.append(f"finding without evidence: {f.get('title')}")
    if "blocker" in sev and d.get("verdict") != "fail":
        errs.append("a blocker finding requires verdict 'fail' (§7.4)")
    elif "major" in sev and "blocker" not in sev and d.get("verdict") != "changes":
        errs.append("a major finding (no blockers) requires verdict 'changes' (§7.4)")
    if not d.get("exercised"):
        errs.append("'exercised' is empty — a review that didn't exercise the artifact is invalid")
    return errs


def cmd_validate(a):
    targets = [Path(a.path)] if a.path else sorted(CARDS.glob("T-*.md"))
    errors = []
    shadow = _read_shadow()
    for t in targets:
        p = t if t.is_absolute() else (Path.cwd() / t)
        if not p.exists() and not t.is_absolute() and (ROOT / t).exists():
            p = ROOT / t
        p = Path(os.path.realpath(p))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:29:19.462Z

**tool call — Bash**
````
{
 "command": "grep -n '\\*\\*Flags\\*\\*\\|\\*\\*Reviewability\\*\\*\\|\\*\\*No invented' spec/REQUIREMENTS.md; grep -n '420' evals/golden/README.md | head -3; grep -n 'by default' memory/DECISIONS.md | head -2; grep -n 'T-039\\|rows 1-18' board/cards/T-017.md | head -2; python3 tools/board.py show T-041 | grep -n 'GET /api/cases'; python3 tools/board.py show T-029 | grep -n 'collect-only'; python3 tools/board.py show T-034 | grep -n 'changed conditions'",
 "description": "Confirm line citations for spec, golden and card text"
}
````

### User / tool · 2026-11-02T01:29:19.728Z

**tool result**
````
327:| 3 | **Flags** | Per flag type (gap, conflict, pre_existing, causation): precision ≥ 0.9 and recall ≥ 0.9. 28-day near-miss must not flag; 73-day gap must. | `flag_precision[type]`, `flag_recall[type]`; assertions `gap_28_not_flagged`, `gap_73_flagged`; 29/30/31 unit test | `python -m evals.run`; `pytest tests/unit` | R-FL-1 to R-FL-4 |
328:| 4 | **No invented facts** | 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding). Judge recall on seeded hallucinations ≥ 95% of every item in `hallucinations.jsonl` (today 40, so at least 33). CONTRACT §5 M2 still says "qa injects 20"; the rate governs permanently and the product note quotes the rate. | `unsupported_count_3run`, `hallucination_catch_rate`, `determinism_3run`, golden `must_not` | `python -m evals.run` | R-TL-4, R-TL-10, R-CH-2, R-CH-7, R-CO-3, R-CO-7 |
329:| 5 | **Reviewability** | Paralegal persona completes the sample case end to end and scores "I could verify every claim quickly" ≥ 4/5. E2E export test green. | `reviews/<card>-paralegal.md`, key `scores.verify_quickly` (1–5, D-015) ≥ 4; `pytest tests/e2e` (letter block holds accepted entries and charges only, no flag content; `needs_review` first; dismissed never exports; edits labeled; decisions survive reload) | persona review + `pytest tests/e2e` | R-RV-1 to R-RV-6, R-RV-8, R-RV-9, R-EX-1 to R-EX-9 |
144:**case_07**: 03-02→03-09: 7; 03-09→03-16: 7; 03-16→05-04: 15 (to Mar 31) + 30 (Apr) + 4 = **49** flag. Total $420; $50,000 never totaled (no 50,420).
169:  - Local dev: `make run` on :7860 with `LLM_BACKEND=claude-cli`; tests and eval iteration use `fixture` by default; the live backend is used to record fixtures and for the 3-run determinism check.
35:    - [major] Coverage counts R-ID mentions rather than pass conditions; four R-IDs are named but their REQUIREMENTS test is in no AC — fix: Add a 'pass condition -> AC n' column to M2M3_COVERAGE.md and fill it for every R-ID, using the AC edits in the T-018 paralegal review (T-044 AC1, T-043 AC1, T-042 AC2, T-041 AC3, T-039 AC2).
36:    - [major] Three AC contradict the golden or REQUIREMENTS, so they can't pass on a correct build — fix: Apply the exact edits in reviews/CONTRACT-M2M3-staff-engineer.md (T-039 AC1, T-033 AC1) and reviews/CONTRACT-M2M3-paralegal.md (T-039 AC2). Add a plan self-check: every number in an AC is diffed against evals/golden expected values.
21:  - {"n": 4, "text": "GET /api/cases/{id}/export returns the two fields separately; pending/dismissed/rejected items never appear (row 19); proved by test_api::test_export_endpoint", "done": false, "evidence": null}
20:  - {"n": 3, "text": "test_dates.py, test_ingest.py, test_amounts.py, test_gaps.py encode: 7 formats + ambiguous 04/05/2026 (case_01), 29/30/31 incl. leap-year case_02, case_04 6->4 entries, 20 phrasings of 'Charge per visit $185' -> rate, $1,2OO unclear/null, record 7 header date; proved by `pytest tests/unit -q --collect-only` listing them", "done": false, "evidence": null}
19:  - {"n": 2, "text": "audited.py: fails 3 attempts -> LLM_FAILED_AFTER_RETRIES and app stays usable; fails twice then succeeds -> output returned; one llm_calls row per attempt, each retry with changed conditions (R-CO-9, row 20); proved by test_audited.py", "done": false, "evidence": null}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:30:01.560Z

**tool call — Bash**
````
{
 "command": "grep -n 'export' memory/contracts/api.md | head -5; python3 tools/board.py show T-046 | grep -n '\"n\": 5'; python3 tools/board.py show T-040 | grep -n '\"n\": 5' ; python3 tools/board.py show T-030 | grep -c '\"n\"'",
 "description": "Confirm api.md export path and a few AC lines for citations"
}
````

### User / tool · 2026-11-02T01:30:01.810Z

**tool result**
````
11:- `warnings[]` appears on case, ingest, review and export responses. Shape: `{"code": "...", "message": "...", "item_id": null}`.
26:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items |
192:    "ready_to_export": false },
197:(The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative`, `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
261:              "queue": ["a3", "e4", "e2", "a1"], "ready_to_export": false },
22:  - {"n": 5, "text": "cut order per REQUIREMENTS section 4 recorded if M3 passes 100% of budget: R-ST-1, then excerpt re-selection, then R-EX-4 sections 7-8, then R-RV-9 highlight", "done": false, "evidence": null}
22:  - {"n": 5, "text": "decisions survive a new TestClient/app restart (R-RV-8); only review and confirm_date set review_status (grep test); Referrer-Policy: no-referrer, no access log of tokens", "done": false, "evidence": null}
5
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:30:39.746Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-018-product-manager.md",
 "content": "# T-018 apply-check: contract-review findings (product-manager-reviewer, round 2)\n\n**Verdict: changes.** 0 blockers. 10 majors: 9 of the 19 contract majors are not applied (or applied in a form that still contradicts the card), plus one new major (T-018 AC2 is ticked on evidence this check refutes). 4 minor groups remain unapplied and are not gating (scope is blocker/major per the brief; severities kept as in source).\n\nMechanical check: `artifacts/review-evidence/T-018-r2-applied-check.py`, run as `python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project`, output in `artifacts/review-evidence/T-018-r2-applied-check.out.txt`. 68 checks: 31 pass, 37 fail. The failures include the minors and the T-017 items.\n\nRule used: an appended `Contract review (T-018): ...` AC counts as the requested edit only if a worker can test it and no in-place text on the same card contradicts it. An AC that still says \"Either ... or\" or \"add ... or edit\" leaves the decision open, so it counts as not applied.\n\n| Finding (source) | Status | Evidence (verbatim, from `board.py show` or the file) |\n|---|---|---|\n| PM1 critical path, estimates, cut order | NOT APPLIED | `docs/M2M3_COVERAGE.md:18` \"Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 ...\" and `:19` \"This runs about 4 h, over the 3.5 h budget.\" remain beside the new text at `:4`. Estimate on 2 of 20 cards (check PM-1d). |\n| PM2 T-027 P0 plus timebox | NOT APPLIED | `priority: \"P0\"` applied; Description has no timebox (PM-2b). |\n| PM3 fixture cannot ship | NOT APPLIED | T-038 AC6 \"ship_bar_met is false when backend == fixture\" applied; T-045 AC4 still \"`python -m evals.run` (ship_bar_met true)\" (PM-3c). |\n| PM4 regression freshness | APPLIED | T-038 AC7 \"latest.json records sha256 of every app/llm/prompts/*.md ... `--check-fresh` exits 1\"; T-035 AC6 and T-036 AC8 handoff text. |\n| PM5 verify_quickly owner | NOT APPLIED | `.claude/agents/paralegal-reviewer.md:111` \"`scores.verify_quickly` (1–5)\" applied; no M3 card names the key (PM-5b, M3 list empty). |\n| PM6 lexicon recall gate | NOT APPLIED | T-038 AC9 \"...or edit LLM_VS_CODE rows 12/16 to 'reported, not gated'\" (open \"or\"); `docs/LLM_VS_CODE.md:44` \"...whose recall on the golden set is a release gate\" (PM-6c). |\n| PL1 edits survive reload | APPLIED | T-044 AC6 \"...export notes list record 3 under EDITED ITEMS with original and new text\"; T-039 AC6 test_edited_items_section. |\n| PL2 reconciliation \"7 of 9\" | NOT APPLIED | T-039 AC2 still \"dismissing entry 5 gives 'Record 5 ... dismissed' and 7 of 9\" (PL-2b); corrected wording only in AC7. |\n| PL3 accident date as two dates | APPLIED | T-043 AC6 \"Date of accident per intake form: 2026-01-19.\" |\n| PL4 record 4 visible as failed | APPLIED | T-042 AC6 \"'could not process' with the reason in the could-not-verify tray\"; T-041 AC6 \"RECORDS NOT IN THE TREATMENT SECTION with reason\". |\n| S1 qa author for 20 test files | NOT APPLIED | T-048 exists (applied, AC1 names 9 files). 11 files still have no qa owner (probe: \"qa:NONE count = 11\"). T-039 names none of them (S-1b). |\n| S2 missing depends_on | APPLIED | T-031 `['T-029']`; T-042 `['T-039']`; T-043 `['T-039', 'T-040', 'T-042']`. |\n| S3 SDK hidden retries | APPLIED | T-034 AC7 \"max_retries=0 and an explicit timeout (<= 120 s)\". |\n| S4 fixture-miss behaviour | APPLIED | T-034 AC8 \"a fixture miss raises FixtureMissing\"; T-037 AC7 \"reports 0 FixtureMissing\". The weaker original T-037 AC2 remains and does not contradict. |\n| S5 judges #2-4 error path | APPLIED | T-035 AC7 \"JUDGE_UNSURE / JUDGE_UNAVAILABLE\"; T-036 AC9 \"judge #3/#4 error or timeout -> needs_review\". |\n| S6 boundary-test module list | APPLIED | T-029 AC7 \"conflicts (accident date), flag_templates, injection scan\". |\n| S7 row-10 engine | NOT APPLIED | T-033 AC6 \"Either T-033 gains AC6 ... or an ADR edits row 10\"; `docs/M2M3_COVERAGE.md:96` \"T-036 (m2-be-llm-flags) (provider variants)\"; no decision in memory/ORCHESTRATOR_DECISIONS.md (S-7a, S-7b, S-7c). |\n| S8 rate note derived by code, damages mention | APPLIED | T-033 AC7 \"rate note numbers are code-derived ... one damages mention (record 5, value null)\". The \"only\" left in T-033 AC1 is in the minors below. |\n| S9 case_07 total | NOT APPLIED | T-039 AC1 still \"'Billed charges stated in these records: $8,390.00' incl. case_07 with a rate present\" (S-9a); $420 is only in AC9. |\n\n## New finding\n- **N1 (major).** T-018 AC2 is ticked as \"every blocker/major applied ... verified by reviews/T-018-product-manager.md\". This review refutes it (see F1-F9 below). The T-018 handoff's \"~23 majors applied\" is also wrong: 10 of 19 contract majors are applied.\n\n## Things that landed and should not break\n- T-048 exists and gates T-034..T-037; the test-first wiring for LLM stages is real.\n- Fixture-cannot-ship is written into T-038 AC6 and T-037 AC7 (every hallucinations line and SE1-SE5 are named).\n- The paralegal edit-reload, two-date accident conflict and record-4 visibility ACs are on the board (PL1, PL3, PL4).\n\n```json\n{\"card\": \"T-018\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"Apply-check of the T-018 contract-review findings: reviews/CONTRACT-M2M3-product-manager.md (6 majors, 3 minors, 1 nit), CONTRACT-M2M3-paralegal.md (4 majors, 4 minors), CONTRACT-M2M3-staff-engineer.md (9 majors, 4 minors), against the board working tree (board/cards T-017, T-018, T-027, T-029..T-046, T-048), docs/M2M3_COVERAGE.md, docs/LLM_VS_CODE.md, .claude/agents/paralegal-reviewer.md, memory/ORCHESTRATOR_DECISIONS.md, memory/SCOPE_CUTS.md, memory/DECISIONS.md, evals/golden/README.md, memory/contracts/api.md. No app code exists; no sample-case run (contract review).\",\n \"exercised\": [\n  \"read personas/product-manager.md in full; memory index and memory files plan_review_patterns, spec_review_patterns, reviewer_sandbox, needs_chris_drift, calibration_vs_redflags\",\n  \"read reviews/CONTRACT-M2M3-product-manager.md, CONTRACT-M2M3-paralegal.md, CONTRACT-M2M3-staff-engineer.md and reviews/T-017-product-manager.md in full\",\n  \"python3 tools/board.py validate -> 'ok (48 file(s))' (before writing this review)\",\n  \"python3 tools/board.py list; show T-017, T-018, T-048; show T-027 and T-029..T-046 with grep for priority, depends_on, status and AC lines; show Descriptions of T-027, T-029, T-036, T-038, T-039, T-045\",\n  \"cat -n docs/M2M3_COVERAGE.md (lines 3-19 critical path and cut order, 8-15 ship-bar table, 22 R-ID header, 96 row 10)\",\n  \"python3 -c read of artifacts/tmp/contract_fixes.json: 19 entries (6 manag, 4 paral, 9 engin) mapped to the cards they name\",\n  \"grep -n verify_quickly .claude/agents/paralegal-reviewer.md personas/paralegal.md -> agent body line 111\",\n  \"sed/grep docs/LLM_VS_CODE.md rows 10, 12, 16 (lines 38, 40, 44); spec/REQUIREMENTS.md section 7 rows 3-5 (lines 327-329); memory/ORCHESTRATOR_DECISIONS.md and grep case_05 across docs, memory, spec (no row-10 decision); memory/SCOPE_CUTS.md (no variant E row); evals/golden/README.md:144 (case_07 total $420); memory/DECISIONS.md:169 (fixture by default); memory/contracts/api.md:26 ({token} export path)\",\n  \"python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project > artifacts/review-evidence/T-018-r2-applied-check.out.txt -> 68 checks, 31 pass, 37 fail; probe qa:NONE count = 11; longest chain to T-038: T-038 -> T-037 -> T-036 -> T-035 -> T-033 -> T-032 -> T-029\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"majors_applied_in_full\": 2, \"ship_bar_traced\": 3, \"fixture_cannot_ship\": 2, \"regression_discipline\": 4, \"test_first_owners\": 2, \"golden_numbers_consistent\": 2, \"paralegal_journey_acs\": 4},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"PM1: stale 5-card critical path and 4 h sentence still in the coverage doc; per-card estimates missing; cut order touches the lexicon gate\",\n   \"evidence\": \"docs/M2M3_COVERAGE.md:18 'Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 (m2-be-grounding) -> T-035 ... -> T-038' and :19 'This runs about 4 h, over the 3.5 h budget.' (check PM-1b, PM-1c). Estimates: 2 of 20 M2/M3 cards carry one (T-029 and T-039 'Timebox 1 h'); 18 do not (check PM-1d). docs/M2M3_COVERAGE.md:5 'M2 cut order (never touches ship-bar items) ... (3) lexicon held-out target lowered from 85% to reported'; docs/LLM_VS_CODE.md:44 '...whose recall on the golden set is a release gate'; spec/REQUIREMENTS.md:327 ship-bar row 3 'R-FL-1 to R-FL-4'.\",\n   \"why_it_matters\": \"The doc now states two critical paths. At its own 30-45 min per card, seven cards is 3.5-5.25 h against a 3.5 h M2 budget, with no total and no cut trigger. Cut 3 lowers the floor under flag recall, which ship-bar row 3 measures per type, so 'never touches ship-bar items' is false as written.\",\n   \"fix\": \"Delete coverage lines 18-19. Add an 'Estimate: N min' line to the Description of each of the 18 cards. State the total and the cut trigger in one sentence. Remove cut 3, or record in memory/SCOPE_CUTS.md that it touches R-FL-3/R-FL-4 (ship-bar row 3) before the cut is allowed.\",\n   \"acceptance_test\": \"grep -c 'This runs about 4 h' docs/M2M3_COVERAGE.md = 0; board.py show prints an estimate in the Description of all 20 M2/M3 cards; the M2 cut order names no lever that touches REQUIREMENTS section 7 row 3 unless that impact is written next to it.\"},\n  {\"severity\": \"major\", \"title\": \"PM2: T-027 raised to P0 without the timebox the fix requires\",\n   \"evidence\": \"python3 tools/board.py show T-027: priority \\\"P0\\\" (applied). Description: 'Debt from T-009 ... Fix the patterns rather than the examples, and score on a held-out set.' No timebox (check PM-2b). T-036 depends_on still includes T-027.\",\n   \"why_it_matters\": \"A P0 card with no stop rule gates the M2 chain through T-036 with no limit on how long it can run.\",\n   \"fix\": \"Add a timebox line to T-027 Description, e.g. 'Timebox N h; at timebox, held-out recall is reported, not gated, and the gap is logged in memory/SCOPE_CUTS.md' (N set by the orchestrator).\",\n   \"acceptance_test\": \"board.py show T-027 Description contains 'Timebox'.\"},\n  {\"severity\": \"major\", \"title\": \"PM3: T-045 AC4 still requires ship_bar_met true on the default run, which T-038 AC6 makes false on fixture\",\n   \"evidence\": \"python3 tools/board.py show T-045 AC4: 'sensors recorded in evals/reports/m3-sensors.md: `pytest tests/unit`, `python -m evals.run` (ship_bar_met true), ...' (check PM-3c). T-038 AC6: 'ship_bar_met is false when backend == fixture'. memory/DECISIONS.md:169: 'tests and eval iteration use `fixture` by default'.\",\n   \"why_it_matters\": \"A worker who follows AC4 literally runs the default fixture backend and gets ship_bar_met false, so the card either cannot close or someone sets the flag by hand. The claude-cli form is only in appended AC6, so the replay path the PM review targeted is still the default one.\",\n   \"fix\": \"Replace AC4's bare '`python -m evals.run` (ship_bar_met true)' with '`LLM_BACKEND=claude-cli python -m evals.run` (ship_bar_met true)' in place; keep the fixture run as its own sensor line.\",\n   \"acceptance_test\": \"board.py show T-045 AC4 contains 'LLM_BACKEND=claude-cli' and no bare '`python -m evals.run` (ship_bar_met true)'.\"},\n  {\"severity\": \"major\", \"title\": \"PM5: verify_quickly is in the paralegal agent body, but no M3 card or gate AC asks for it\",\n   \"evidence\": \".claude/agents/paralegal-reviewer.md:111 '**Ship-bar score (D-015):** ... your review JSON must include `scores.verify_quickly` (1–5) ... ≥ 4 is the ship bar.' (applied). M3 cards whose ACs name the key: none (check PM-5b). The only other hits are T-025 and T-038 AC8, whose 'New orchestrator card (M3)' does not exist on the board.\",\n   \"why_it_matters\": \"Ship-bar row 5 (spec/REQUIREMENTS.md:329) is the one human number. Without an M3 AC that requests it, the M3 gate can close on a paralegal review with no score.\",\n   \"fix\": \"Create the M3 card the fix named, or add an AC to T-045: 'M3 gate paralegal review writes reviews/<card>-paralegal.md with scores.verify_quickly (D-015); ship bar 5 met when >= 4'.\",\n   \"acceptance_test\": \"board.py show of an M3 card includes an AC naming scores.verify_quickly; grep -l verify_quickly board/cards/T-04*.md lists it.\"},\n  {\"severity\": \"major\", \"title\": \"PM6: the lexicon-recall release gate is undecided; T-038 AC9 is an 'or' and LLM_VS_CODE still calls it a gate\",\n   \"evidence\": \"python3 tools/board.py show T-038 AC9: '...add `lexicon_recall_must_flags` ... and state the threshold in REQUIREMENTS section 7 by ADR, or edit LLM_VS_CODE rows 12/16 to \\\"reported, not gated\\\".' (open 'or', check PM-6d). docs/LLM_VS_CODE.md:44 '...whose recall on the golden set is a release gate' (check PM-6c). T-038 AC1 metric list has no lexicon metric.\",\n   \"why_it_matters\": \"The injection defence (R-RV-6) is either gated or not, and the product note will say one or the other. The coverage cut order already treats it as ungated; the LLM/code table still says gated.\",\n   \"fix\": \"Choose one and record it in memory/ORCHESTRATOR_DECISIONS.md. Either add lexicon_recall_must_flags to T-038 AC1 with a threshold, or edit LLM_VS_CODE rows 12 and 16 to 'reported, not gated' and delete 'release gate'. Remove the 'or' from T-038 AC9.\",\n   \"acceptance_test\": \"grep -c 'release gate' docs/LLM_VS_CODE.md = 0 and T-038 has no 'or edit' text; or jq '.metrics.lexicon_recall_must_flags' evals/reports/latest.json returns a number after T-038 runs.\"},\n  {\"severity\": \"major\", \"title\": \"PL2: T-039 AC2 still says dismissing entry 5 alone gives '7 of 9'; the corrected AC is appended as AC7\",\n   \"evidence\": \"python3 tools/board.py show T-039 AC2: '...dismissing entry 5 gives \\\"Record 5 ... dismissed\\\" and 7 of 9 (R-EX-4, R-EX-7)' (check PL-2b, not removed). Corrected text is AC7 only: 'dismissing entry 5 and leaving entry 6 pending gives ... and 7 of 9'.\",\n   \"why_it_matters\": \"One card gives two counts for the same dismissal. With only entry 5 dismissed the letter holds 8 of 9 records, so the uncorrected AC2 encodes the wrong count and a correct build can fail it.\",\n   \"fix\": \"Replace T-039 AC2's 'dismissing entry 5 gives ... 7 of 9' in place with the AC7 wording, and delete AC7.\",\n   \"acceptance_test\": \"grep -c 'dismissing entry 5 gives' board/cards/T-039.md = 0.\"},\n  {\"severity\": \"major\", \"title\": \"S1: 11 test files still have no qa author; T-039 does not name them\",\n   \"evidence\": \"python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ... -> 'qa:NONE count = 11 -> [test_api, test_charges, test_edit, test_export_ui, test_flags_panel, test_input, test_keyboard_mobile, test_review_matrix, test_side_by_side, test_source_record, test_timeline]'. T-039 AC8 is the instruction 'name test_api.py plus the 10 E2E files above, by file'; no T-039 AC names any of the 11 (check S-1b).\",\n   \"why_it_matters\": \"CONTRACT:240 gives tests/** to qa. These files are cited by backend and frontend ACs, so those cards cannot be test-first, and T-039's 'test-first' covers them only by R-ID.\",\n   \"fix\": \"Rewrite T-039 AC4 to list the 11 files by name with the R-IDs each covers. test_api.py may move to T-048. Re-run the applied-check.\",\n   \"acceptance_test\": \"python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ... prints 'qa:NONE count = 0'.\"},\n  {\"severity\": \"major\", \"title\": \"S7: the row-10 engine is still an 'Either ... or' instruction; no decision is recorded\",\n   \"evidence\": \"python3 tools/board.py show T-033 AC6: 'Either T-033 gains AC6 ... or an ADR edits row 10 and T-036 AC3 says ...' (check S-7a); same text on T-036 AC10. docs/M2M3_COVERAGE.md:96 '| 10 | Structural conflicts | T-033 (m2-be-amounts-gaps) (accident date), T-036 (m2-be-llm-flags) (provider variants) |'. docs/LLM_VS_CODE.md:38 row 10 '... the same provider spelled two ways | **Code**'. grep case_05 across docs, memory and spec: no decision (only spec/REQUIREMENTS.md).\",\n   \"why_it_matters\": \"The table says code, the plan gives it to the LLM card, and the T-036 implementer will pick one. A provider-name conflict raised by both engines shows the panel the same flag twice.\",\n   \"fix\": \"Decide and record it. Either provider-variant conflict is Code (a T-033 AC with no LLM call, row 10 unchanged), or row 10 changes by ADR. Replace the 'Either' text on T-033 AC6 and T-036 AC10 with the decision, and update docs/M2M3_COVERAGE.md row 10 to match.\",\n   \"acceptance_test\": \"grep -c 'Either' board/cards/T-033.md board/cards/T-036.md = 0; coverage row 10 and LLM_VS_CODE row 10 name the same engine.\"},\n  {\"severity\": \"major\", \"title\": \"S9: T-039 AC1 still asserts $8,390.00 for case_07; the $420 line is appended as AC9\",\n   \"evidence\": \"python3 tools/board.py show T-039 AC1: 'total line exactly \\\"Billed charges stated in these records: $8,390.00\\\" incl. case_07 with a rate present' (check S-9a). Golden: evals/golden/README.md:144 'Total $420; $50,000 never totaled'. Corrected text is AC9 only.\",\n   \"why_it_matters\": \"A test-first card that asserts $8,390 for case_07 contradicts the golden $420 total and leaves the implementer to pick. A wrong money assertion is the bad-day case for this product.\",\n   \"fix\": \"Replace AC1's case_07 clause in place with the AC9 wording ('on case_07 with $420 accepted it is exactly ... $420.00'), and delete AC9.\",\n   \"acceptance_test\": \"board.py show T-039 AC1 contains '$420.00' on case_07 and does not contain '$8,390.00 incl. case_07'.\"},\n  {\"severity\": \"major\", \"title\": \"N1: T-018 AC2 is ticked on evidence this check refutes\",\n   \"evidence\": \"python3 tools/board.py show T-018 AC2 evidence: 'every blocker/major applied as AC edit/new card (artifacts/tmp/contract_fixes.json); verified by reviews/T-018-product-manager.md'. T-018 Handoff: '~23 majors applied as AC edits/deps/new card T-048 before any M2 claim.' This check: 9 of 19 contract majors not applied (PM1, PM2, PM3, PM5, PM6, PL2, S1, S7, S9), see the table above.\",\n   \"why_it_matters\": \"The gate that closes the contract review records a claim this check refutes. Later cards would treat the M2 contract as settled.\",\n   \"fix\": \"Reopen T-018 AC2 (done false) or change its evidence to this review's verdict. Correct the handoff count to the applied number once PM1-S9 land.\",\n   \"acceptance_test\": \"board.py show T-018 shows AC2 done false, or AC2 evidence cites reviews/T-018-product-manager.md with verdict pass.\"},\n  {\"severity\": \"minor\", \"title\": \"Unapplied PM minors (not gating): cut clock, flag-group count, token-log test, golden variant E, 'only' in T-033 AC1, {id} path\",\n   \"evidence\": \"python3 tools/board.py show T-046 AC5: 'cut order per REQUIREMENTS section 4 recorded if M3 passes 100% of budget' (no clock, check m-PM1a). T-037 AC1: 'prints ... all flag groups' (m-PM1b). T-040 AC5: 'no access log of tokens' (m-PM1c). docs/LLM_VS_CODE.md:44 'documented as golden variant E, a qa item, not yet in the golden set'; no variant E in memory/SCOPE_CUTS.md or any card AC (m-PM2). T-033 AC1: 'sample yields $6,240, $185, $2,150 only' (S-8b). T-041 AC4: 'GET /api/cases/{id}/export' (nit; memory/contracts/api.md:26 spells {token}).\",\n   \"why_it_matters\": \"Each is a check a worker can tick without proving anything. The variant E item is the one injection path only the human catches, and the note should cite it.\",\n   \"fix\": \"T-046 AC5: quote M3 start and end timestamps from board activity and state the trigger. T-037 AC1: name the five groups with counts 1/2/2/5/0. T-040 AC5: add test_api::test_no_token_in_logs. Add variant E to T-038 or a SCOPE_CUTS row. T-033 AC1: replace 'only' with the damages mention. T-041 AC4: {token}.\",\n   \"acceptance_test\": \"Each named test or command exists and fails when its condition is broken.\"},\n  {\"severity\": \"minor\", \"title\": \"Unapplied PL minors (not gating): reason sentence inline, full $185 string, charge highlight and banner record, dismissal reason to notes\",\n   \"evidence\": \"python3 tools/board.py show T-042 AC2: 'timeline rows show date, provider, summary, excerpt, state' (no inline reason, m-PL1). T-043 AC2: \\\"$185 'rate $185/visit; visit count not stated'\\\" (truncated, m-PL2). T-043 AC1 'case_07 shows an injection warning' (no record 3, m-PL3b); T-043 AC5 'gap flag opens both records 6 and 7' (no $6,240 charge highlight, m-PL3a). T-043 AC3 'dismiss -> reset -> dismiss' (no reason, m-PL4).\",\n   \"why_it_matters\": \"She reads why an item needs review on sight, and she reconciles $6,240 against the ER record. Each of these is a fact she checks in the first minute.\",\n   \"fix\": \"T-042 AC2: 'every needs_review row shows its why-template sentence inline'. T-043 AC2: quote the full R-CH-3 string. T-043 AC1: 'case_07 banner names record 3 and says flags may be incomplete'. T-043 AC5: '$6,240 charge opens record 2 with \\\"ER charges: $6,240.\\\" highlighted'. T-043 AC3: dismiss the gap flag with a reason and check it in the notes FLAGS DISMISSED.\",\n   \"acceptance_test\": \"tests/e2e/test_timeline.py::test_reason_inline; test_flags_panel.py::test_injection_banner_names_record; test_source_record.py::test_charge_highlight; test_review_matrix.py::test_dismiss_reason_in_notes.\"},\n  {\"severity\": \"minor\", \"title\": \"Unapplied staff minors (not gating): xfail instead of --collect-only, retry prompt hash, judge input isolation, verifier mutation guard, network guard\",\n   \"evidence\": \"python3 tools/board.py show T-029 AC3: 'proved by `pytest tests/unit -q --collect-only` listing them' (m-S1). T-034 AC2: 'each retry with changed conditions' (no prompt-hash check, m-S2a). T-035 AC5: 'prompts are versioned files ... the generator and judge never share a prompt' (no input-isolation check, m-S2b). T-030 has 5 ACs, none naming monkeypatch or mutation (m-S3). T-029 AC5 names no socket or network guard (m-S4).\",\n   \"why_it_matters\": \"Collected-but-broken red tests pass for 'red'; a retry that resends the same prompt passes; a verifier stubbed to pass goes unnoticed; one stray network call makes the suite flaky and costs money.\",\n   \"fix\": \"T-029 AC3: each new test is xfail(strict=True, reason='T-0xx') and pytest -rx shows them. T-034 AC2: consecutive attempts have different prompt hashes in llm_calls. T-035 AC5: the rendered judge #1 prompt holds the record and candidate only. T-030 AC6: monkeypatching grounding.verify to pass fails test_grounding and test_pipeline. T-029 AC5: tests/conftest.py blocks socket.connect except localhost.\",\n   \"acceptance_test\": \"test_provider::test_fixture_miss_raises style tests exist; each named test fails when its condition is broken.\"},\n  {\"severity\": \"minor\", \"title\": \"N2: instruction-style ACs copied onto 2-3 cards; one asks a db card to rewrite a planning doc at stale line numbers\",\n   \"evidence\": \"python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ... INFO line: \\\"instruction-style 'Contract review (T-018):' ACs copied onto more than one card: 11 distinct texts\\\"; ['T-031', 'T-034', 'T-036']: 'Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain ...' (T-031 AC6 is a db card); ['T-029', 'T-039']: 'T-029 AC4 or a new qa card ...'.\",\n   \"why_it_matters\": \"Three workers tick copies of the same doc rewrite, and nobody owns the outcome. The line references are already stale (the doc moved).\",\n   \"fix\": \"One owner per instruction. The coverage-doc change belongs to the orchestrator card, not to T-031, T-034 or T-036. Replace each copied instruction with a testable AC on the card that owns the outcome.\",\n   \"acceptance_test\": \"the applied-check INFO line shows no 'Contract review (T-018):' text on more than one card.\"}\n ],\n \"whats_right\": [\n  \"T-048 exists with deps [] and T-034, T-035, T-036 and T-037 depend on it; T-031, T-042 and T-043 got their depends_on edges (S1 test-first wiring, S2 edges).\",\n  \"The fixture-cannot-ship rule is on the board (T-038 AC6) with the 50 seeded judge lines and SE1-SE5 named (T-037 AC6-AC7), and the regression freshness check is on T-038 AC7.\",\n  \"The paralegal journey gaps are now ACs: edited items survive reload (T-044 AC6), two accident dates shown side by side (T-043 AC6), record 4 visible as failed (T-042 AC6, T-041 AC6).\"\n ],\n \"questions_for_chris\": [\"Is the lexicon held-out recall (LLM_VS_CODE row 16, 'a release gate') a gate you will hold to? Your answer decides whether M2 cut 3 is allowed and whether T-038 gets a metric or the table changes (finding PM6).\"]}\n```\n"
}
````

### User / tool · 2026-11-02T01:30:39.896Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-018-product-manager.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:30:43.185Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-018-product-manager.md 2>&1; echo \"exit=$?\"; python3 -c 'import re,json,sys; t=open(\"reviews/T-018-product-manager.md\").read(); blocks=re.findall(r\"```json\\n(.*?)\\n```\", t, re.S); print(\"json blocks:\", len(blocks)); d=json.loads(blocks[0]); print(\"verdict:\", d[\"verdict\"], \"findings:\", len(d[\"findings\"]), collections_count if False else \"\", sorted(set(f[\"severity\"] for f in d[\"findings\"])))' 2>&1",
 "description": "Validate T-018 review file and parse its JSON block"
}
````

### User / tool · 2026-11-02T01:30:43.341Z

**tool result**
````
ok (1 file(s))
exit=0
json blocks: 1
verdict: changes findings: 14  ['major', 'minor']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:23.006Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-017-product-manager-r2.md",
 "content": "# T-017 round 2: product-manager-reviewer apply-check of the round-1 plan findings\n\n**Verdict: changes.** 0 blockers. 4 majors from `reviews/T-017-product-manager.md` are not applied (one of them is only partly applied). Plus 1 minor and 1 nit. Evidence comes from the same run as the T-018 review: `artifacts/review-evidence/T-018-r2-applied-check.py`, output in `artifacts/review-evidence/T-018-r2-applied-check.out.txt`.\n\nWhat landed: the M2 cut order (`docs/M2M3_COVERAGE.md:5`), the ship-bar to card table (`:8-15`), the seven-card critical path in `:4`, T-048 as the qa card for LLM-stage tests, and T-027 at P0. What did not: the pass-condition column, the in-place AC fixes, the qa owner gap (11 files left), the row-10 decision, and the stale chain text that still sits in the same doc.\n\n| Round-1 finding | Status | Evidence (verbatim) |\n|---|---|---|\n| Major 1: coverage counts mentions, not pass conditions | NOT APPLIED | `docs/M2M3_COVERAGE.md:22` \"`| R-ID | Cards |`\", no pass-condition column (T17-1a). |\n| Major 2: three AC contradict golden or REQUIREMENTS; plan self-check | NOT APPLIED | T-039 AC1 still \"'Billed charges stated in these records: $8,390.00' incl. case_07\" (S-9a); T-039 AC2 still \"dismissing entry 5 gives ... and 7 of 9\" (PL-2b); T-033 AC1 still \"$2,150 only\" (S-8b). No plan self-check line in the coverage doc (T17-2a). |\n| Major 3: unowned validation; row 10 engine | NOT APPLIED | Probe \"qa:NONE count = 11\". `docs/M2M3_COVERAGE.md:96` \"T-036 (m2-be-llm-flags) (provider variants)\"; `docs/LLM_VS_CODE.md:38` row 10 \"...the same provider spelled two ways | **Code**\"; no decision recorded (S-7c). |\n| Major 4: critical path, budget, cut order, ship-bar trace | PARTLY APPLIED, NOT APPLIED AS A WHOLE | Applied: `:4` seven-card chain, `:5` M2 cut order, `:8-15` ship-bar table. Not applied: `:18` \"Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 ...\" and `:19` \"This runs about 4 h, over the 3.5 h budget.\" still there (T17-4a/b; PM1). Cut `:5` item (3) \"lexicon held-out target lowered from 85% to reported\" conflicts with `docs/LLM_VS_CODE.md:44` \"...whose recall on the golden set is a release gate\" (T17-4c; PM6). |\n| Minor: T-017 AC2 evidence overstates | NOT APPLIED | `python3 tools/board.py show T-017` AC2 evidence still \"rows 1-20 all mapped\" (m-T17); row 19 is M3 at `docs/M2M3_COVERAGE.md:105` and row 15 edit half at `:101`. |\n\n## Findings\n\n```json\n{\"card\": \"T-017\", \"persona\": \"product-manager-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"Round-2 apply-check of reviews/T-017-product-manager.md (4 majors, 1 minor) against the current plan: docs/M2M3_COVERAGE.md, board/cards T-027, T-029..T-039, T-041..T-048 (AC text and depends_on), docs/LLM_VS_CODE.md rows 10, 12, 16, evals/golden/README.md, spec/REQUIREMENTS.md section 7. No app code exists; plan review only.\",\n \"exercised\": [\n  \"read reviews/T-017-product-manager.md in full (round-1 findings and the exact fix text)\",\n  \"python3 tools/board.py show T-017 (AC1, AC2 evidence and round-1 notes); show T-018 Handoff\",\n  \"cat -n docs/M2M3_COVERAGE.md (lines 3-19, 22, 84-108)\",\n  \"python3 tools/board.py show on T-027, T-029..T-039, T-041..T-048 (AC lines, depends_on, Descriptions) to test each fix\",\n  \"python3 -I artifacts/review-evidence/T-018-r2-applied-check.py /Users/arsis/zlayt-pm-project > artifacts/review-evidence/T-018-r2-applied-check.out.txt: T17-1a, T17-2a, T17-3, T17-4a/b/c, m-T17 (plus the card checks it depends on, S-7b, S-9a, PL-2b, S-8b); probe qa:NONE = 11; longest chain T-038 -> T-037 -> T-036 -> T-035 -> T-033 -> T-032 -> T-029\",\n  \"probe depends_on: T-034 ['T-031', 'T-048'] and T-031 ['T-029'] (second seven-card path)\",\n  \"grep -n 'row 10|row 16|release gate' docs/LLM_VS_CODE.md (rows 16 line 44 'release gate'); grep case_05 across docs, memory, spec (no decision)\",\n  \"python3 tools/board.py validate -> ok (48 file(s)) before writing this review\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"coverage_pass_conditions\": 2, \"ac_consistent_with_golden\": 2, \"qa_owned_tests\": 2, \"critical_path_and_cut_order\": 2, \"ship_bar_traced\": 3},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Round-1 major 1 not applied: coverage still counts R-ID mentions; no pass-condition column\",\n   \"evidence\": \"docs/M2M3_COVERAGE.md:22 '| R-ID | Cards |' (header unchanged, no pass-condition column; applied-check T17-1a: no match). The R-RV-8 test input 'accept 3 items, edit 1, reload' now has an AC (T-044 AC6, 'reload -> edited summary and \\\"edited\\\" label persist'), but the matrix does not point to it.\",\n   \"why_it_matters\": \"T-017 AC1 was ticked by looking up mentions. Without a pass-condition column, the next R-ID can be marked covered by a card that never tests its REQUIREMENTS input, which is how the lost-edit and merged-date cases got through round 1.\",\n   \"fix\": \"Add a 'Pass condition -> AC' column to docs/M2M3_COVERAGE.md for every R-ID row: quote the REQUIREMENTS test input and cite the AC id. Start with R-RV-8 -> T-044 AC6, R-CO-9 -> T-042 AC6 and T-041 AC6, R-EX-4(10) -> T-044 AC6 and T-039 AC6, R-FL-2(a) -> T-043 AC6.\",\n   \"acceptance_test\": \"Every R-ID row in docs/M2M3_COVERAGE.md has a non-empty pass-condition cell; each cell quotes the REQUIREMENTS test input and names an AC that contains it (grep the AC text).\"},\n  {\"severity\": \"major\", \"title\": \"Round-1 major 2 not applied: three ACs still contradict golden or REQUIREMENTS in place; no plan self-check\",\n   \"evidence\": \"python3 tools/board.py show T-039 AC1: 'total line exactly \\\"Billed charges stated in these records: $8,390.00\\\" incl. case_07 with a rate present' (S-9a). T-039 AC2: 'dismissing entry 5 gives \\\"Record 5 ... dismissed\\\" and 7 of 9' (PL-2b). T-033 AC1: 'sample yields $6,240, $185, $2,150 only' (S-8b). The corrected wording exists only in appended ACs (T-039 AC9, T-039 AC7, T-033 AC7). docs/M2M3_COVERAGE.md has no plan self-check line (T17-2a).\",\n   \"why_it_matters\": \"Under test-first, a card that contradicts itself is one the implementer will 'fix' by editing the test, which is the thing the plan says must not happen. The golden says case_07 total is $420 (evals/golden/README.md:144).\",\n   \"fix\": \"Edit T-039 AC1, T-039 AC2 and T-033 AC1 in place to the corrected text and delete the appended duplicates (T-039 AC7, AC9). Add to docs/M2M3_COVERAGE.md: 'Plan self-check: every number in an AC is diffed against evals/golden expected values before in_review.'\",\n   \"acceptance_test\": \"board.py show T-039 contains no 'incl. case_07' next to '$8,390.00', no 'dismissing entry 5 gives'; T-033 AC1 has no 'only' next to the three amounts; docs/M2M3_COVERAGE.md contains the self-check sentence.\"},\n  {\"severity\": \"major\", \"title\": \"Round-1 major 3 not applied: 11 test files still have no qa author; LLM_VS_CODE row 10 and the coverage row disagree\",\n   \"evidence\": \"python3 -I artifacts/review-evidence/T-018-r2-applied-check.py ...: 'qa:NONE count = 11 -> [test_api, test_charges, test_edit, test_export_ui, test_flags_panel, test_input, test_keyboard_mobile, test_review_matrix, test_side_by_side, test_source_record, test_timeline]' (T-048 covers 9 of 20). docs/M2M3_COVERAGE.md:96 '| 10 | Structural conflicts | T-033 (m2-be-amounts-gaps) (accident date), T-036 (m2-be-llm-flags) (provider variants) |' against docs/LLM_VS_CODE.md:38 '...the same provider spelled two ways | **Code**'. No ADR or decision (S-7c).\",\n   \"why_it_matters\": \"T-017 AC2 says each card AC names its test. Eleven named test files have no author, and the engine for provider conflicts is still unresolved, so an implementer can produce the same conflict twice.\",\n   \"fix\": \"Name the 11 files by path on T-039 (or T-048) with the R-IDs each covers. Decide row 10 by ADR or by a code AC on T-033, and make docs/M2M3_COVERAGE.md row 10 match the decision.\",\n   \"acceptance_test\": \"The applied-check prints 'qa:NONE count = 0'; coverage row 10 and LLM_VS_CODE row 10 name the same engine.\"},\n  {\"severity\": \"major\", \"title\": \"Round-1 major 4 not applied as a whole: the doc still has two critical paths, no per-card estimates, and a cut that touches the lexicon gate\",\n   \"evidence\": \"docs/M2M3_COVERAGE.md:4 'M2 critical path (7 cards): T-029/T-048 (tests first) -> T-032 ... -> T-038 eval runner.' (applied; matches the probe chain). But :18 'Critical path (M2): T-029 (m2-qa-unit-first) -> T-030 (m2-be-grounding) -> T-035 ... -> T-038' and :19 'This runs about 4 h, over the 3.5 h budget.' remain (T17-4a/b). Per-card estimates absent on 18 of 20 cards (PM1). Cut :5 item (3) 'lexicon held-out target lowered from 85% to reported' vs docs/LLM_VS_CODE.md:44 '...recall on the golden set is a release gate' (T17-4c).\",\n   \"why_it_matters\": \"A reader who reaches line 18 gets a different critical path and a '4 h, over budget' verdict. The table at :8-15 and the cut order at :5 are right in shape, but the cut order claims it 'never touches ship-bar items' while cut (3) lowers the floor under flag recall that ship-bar row 3 measures.\",\n   \"fix\": \"Delete docs/M2M3_COVERAGE.md lines 18-19. Add 'Estimate: N min' to each card Description (PM1). Resolve the lexicon gate (PM6) before keeping cut (3), and state which ship-bar row each cut touches.\",\n   \"acceptance_test\": \"grep -c 'T-030 (m2-be-grounding) -> T-035' docs/M2M3_COVERAGE.md = 0; estimates present on all 20 M2/M3 cards; the lexicon gate decision is recorded in ORCHESTRATOR_DECISIONS.md.\"},\n  {\"severity\": \"minor\", \"title\": \"T-017 AC2 evidence still says 'rows 1-20 all mapped' (round-1 minor, not reworded)\",\n   \"evidence\": \"python3 tools/board.py show T-017, AC2 evidence: \\\"docs/M2M3_COVERAGE.md 'LLM_VS_CODE row -> card': rows 1-20 all mapped, each card AC names its test/eval\\\" (m-T17). docs/M2M3_COVERAGE.md:105 row 19 maps to T-041 and T-045, both M3 cards; :101 row 15 edit half maps to T-040 (M3).\",\n   \"why_it_matters\": \"The evidence claims more than the artifact shows about M2, which is the habit the gate looks for.\",\n   \"fix\": \"Reword the AC2 evidence: 'rows 1-18 and 20 have an M2 card; row 19 and the edit half of row 15 are M3 by design'.\",\n   \"acceptance_test\": \"board.py show T-017 AC2 evidence does not contain 'rows 1-20 all mapped'.\"},\n  {\"severity\": \"nit\", \"title\": \"The seven-card critical path has a tie that the doc does not mention\",\n   \"evidence\": \"Probe depends_on: T-034 ['T-031', 'T-048']; T-031 ['T-029']. So T-029 -> T-031 -> T-034 -> T-035 -> T-036 -> T-037 -> T-038 is also seven cards. docs/M2M3_COVERAGE.md:4 names only the T-032/T-033 route.\",\n   \"why_it_matters\": \"Which path is longest decides which card the cut order protects. A reader can't tell from line 4 which path to watch.\",\n   \"fix\": \"Add one clause to :4: 'ties with T-029 -> T-031 -> T-034 -> ... -> T-038'.\",\n   \"acceptance_test\": \"docs/M2M3_COVERAGE.md:4 names both seven-card paths, or the probe shows one longest path.\"}\n ],\n \"whats_right\": [\n  \"The M2 cut order and the ship-bar to card table are on the page (docs/M2M3_COVERAGE.md:5 and :8-15), so the gate can point at them.\",\n  \"T-048 is the qa card for the LLM-stage tests with deps []; T-034, T-035, T-036 and T-037 depend on it.\",\n  \"T-027 is P0 and T-036 keeps its dependency, so the lexicon work sits on the path it gates.\"\n ],\n \"questions_for_chris\": [\"Is the lexicon held-out recall (LLM_VS_CODE row 16, 'a release gate') a gate you will hold to? It decides whether M2 cut (3) is allowed and whether T-038 gets a metric or the table changes.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T01:31:23.156Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-017-product-manager-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:25.805Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-017-product-manager-r2.md 2>&1; echo \"exit=$?\"; python3 tools/board.py validate reviews/T-018-product-manager.md 2>&1; echo \"exit=$?\"; python3 -c 'import re,json; t=open(\"reviews/T-017-product-manager-r2.md\").read(); b=re.findall(r\"```json\\n(.*?)\\n```\", t, re.S); d=json.loads(b[0]); print(\"blocks\", len(b), \"verdict\", d[\"verdict\"], \"sev\", [f[\"severity\"] for f in d[\"findings\"]])'; python3 tools/board.py validate 2>&1 | tail -2",
 "description": "Validate both new review files and the whole board"
}
````

### User / tool · 2026-11-02T01:31:26.074Z

**tool result**
````
ok (1 file(s))
exit=0
ok (1 file(s))
exit=0
blocks 1 verdict changes sev ['major', 'major', 'major', 'major', 'minor', 'nit']
ok (48 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:37.955Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_plan_review_patterns.md"
}
````

### User / tool · 2026-11-02T01:31:37.970Z

**tool result**
````
1	---
2	name: plan-review-patterns
3	description: Recurring defects in card-plan / milestone-contract reviews (T-017/T-018, 2026-11-01) — mention-coverage, unowned tests, wrong critical path, fixture-replay ship bars
4	metadata:
5	  type: feedback
6	---
7	
8	Things to check first on any card-plan or AC contract review. All of these were found on the T-017 plan (19 cards, 93 AC). Verdict was "changes" in all three lenses.
9	
10	1. **Coverage counted by mention.** A matrix that says R-ID → card can still leave the R-ID's pass/fail test in no AC. Compare the REQUIREMENTS test input ("edit 1, reload") against the AC text. The usual gaps are edit persistence, the LLM-failed UI state and dealbreaker UI rendering.
11	2. **Test files nobody writes.** CONTRACT:240 gives tests/** to qa. Script the files each AC cites and list which qa card writes each one. On T-017, 20 of 35 had no author.
12	3. **Critical path drawn by hand.** Compute the longest depends_on chain. The stated path left out 2 cards, and the cut list held only an M3 card for an M2 overrun. Check whether a P1 card gates the P0 path.
13	4. **Ship bar met by replay.** The 3-run metrics (unsupported, determinism) on the fixture backend pass by construction. Fixtures for the hallucination set and seeded edits were never recorded. Ask what happens on a fixture miss.
14	5. **AC numbers vs golden.** Diff every number in the AC against the golden. Found: case_07 total, "7 of 9", and "only" amounts that contradicted golden A4.
15	6. **Values in golden strings that no AC derives** ("12 planned; discharged at visit 9"). These are hard-coding or LLM-value risks.
16	
17	**Why:** A plan review passes the coverage matrix by eye while the dealbreakers stay untested. A script catches 2–5 in minutes.
18	
19	**How to apply:** Reuse artifacts/review-evidence/T-018-contract-probe.py (it parses board/cards). Re-run it on any re-plan and check the 'qa:NONE' count and the chain. Related: [[spec-review-patterns]], [[t013-review-history]].
20	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:38.219Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md"
}
````

### User / tool · 2026-11-02T01:31:38.231Z

**tool result**
````
1	---
2	name: reviewer-sandbox
3	description: Hook limits for this reviewer — shell writes to scratchpad/memory are blocked; python -c with escaped backticks fails git-guard parsing
4	metadata:
5	  type: reference
6	---
7	
8	The board-guard hook blocks reviewer shell redirects outside reviews/ and artifacts/review-evidence/. That includes the session scratchpad and this memory dir, so use the Write/Edit tools for memory. Put helper scripts in `artifacts/review-evidence/<card>-*.py` and run them with `python3 -I`. The git-guard hook also rejects `python3 -c "..."` strings that contain escaped backticks, so use single-quoted `-c` code that has no backticks. Related: [[source-fetching]].
9	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:38.447Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T01:31:38.459Z

**tool result**
````
1	- [Spec review patterns](feedback_spec_review_patterns.md) — recurring REQUIREMENTS defects: phantom IDs, fix-induced contradictions, vocab drift, stale golden counts, scope creep
2	- [Calibration vs red flags](feedback_calibration_vs_redflags.md) — dossier calibration severities softer than dealbreakers; cross-check
3	- [Source fetching](reference_source_fetching.md) — curl+UA fallback when WebFetch is missing; blocked hosts
4	- [NEEDS_CHRIS drift](feedback_needs_chris_drift.md) — rows added without cards, non-Chris questions, vague actions; ADR facts vs live system
5	- [Reviewer sandbox](reference_reviewer_sandbox.md) — hooks block shell writes to scratchpad/memory and backtick python -c; scripts go in artifacts/review-evidence
6	- [Plan/contract review patterns](feedback_plan_review_patterns.md) — mention-coverage, unowned tests, wrong critical path, fixture-replay ship bar; probe script
7	- [T-013/T-025 review history](project_t013_review_history.md) — r1-r3 + T-025 verdicts; open: false §8 'aligned' claims, circular authority, must_not M1–M14 vs M17
8	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:43.991Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_plan_review_patterns.md",
 "old_string": "**How to apply:** Reuse artifacts/review-evidence/T-018-contract-probe.py (it parses board/cards). Re-run it on any re-plan and check the 'qa:NONE' count and the chain. Related: [[spec-review-patterns]], [[t013-review-history]].",
 "new_string": "**How to apply:** Reuse artifacts/review-evidence/T-018-contract-probe.py (it parses board/cards). Re-run it on any re-plan and check the 'qa:NONE' count and the chain. Related: [[spec-review-patterns]], [[t013-review-history]].\n\n## Apply-check defects (T-018 round 2, 2026-11-01)\nWhen the orchestrator \"applies\" review findings, check the result, not the claim. Round 2 showed the same failure modes:\n7. **Appended, not edited.** The fix was added as a new AC (e.g. T-039 AC9) and the wrong AC (T-039 AC1, AC2) was left in place, so the card contradicts itself. Rule used: an appended AC counts only if no in-place text on the same card contradicts it.\n8. **'Either ... or' left in the AC.** \"Either T-033 gains AC6 ... or an ADR edits row 10\" is a decision the card never made. Count it as not applied until one branch is chosen and recorded in ORCHESTRATOR_DECISIONS.\n9. **Estimates and timeboxes skipped.** \"Per-card estimate in each Description\" landed on 2 of 20 cards. Count the cards, not the doc sentence.\n10. **Old text kept beside the new.** The coverage doc got a new critical-path section, but the old 5-card chain and '4 h, over budget' lines stayed 15 lines lower. grep for the stale phrase.\n11. **Instruction copied to several cards.** 11 distinct 'Contract review (T-018):' ACs sit on 2-3 cards each, so nobody owns the outcome.\n12. **Claim on the board that the check refutes.** T-018 AC2 said \"every blocker/major applied\"; 9 of 19 were not.\n13. **Owner probe must skip instruction text.** An AC that says \"name test_api.py ... by file\" is not an owner. Exclude 'Contract review (T-018):' lines from the qa-owner probe, or the count reads 0 when it is 11.\n14. **Patterns match in the wrong file.** A 'self-check|diff .* golden' pattern matched an unrelated lexicon decision (D-018). Anchor patterns to the file and section that must hold the text, then read each matched line.\n\n**Script:** artifacts/review-evidence/T-018-r2-applied-check.py (68 checks, prints the matched line for each; output in T-018-r2-applied-check.out.txt). Re-run on every apply round before any 'applied' verdict. Related: [[needs-chris-drift]]."
}
````

### User / tool · 2026-11-02T01:31:44.086Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/feedback_plan_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:45.482Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md",
 "old_string": "The git-guard hook also rejects `python3 -c \"...\"` strings that contain escaped backticks, so use single-quoted `-c` code that has no backticks. Related: [[source-fetching]].",
 "new_string": "The git-guard hook also rejects `python3 -c \"...\"` strings that contain escaped backticks, so use single-quoted `-c` code that has no backticks. The board-guard also reads a `>` inside a `python3 -c` string as a redirect and blocks the call (seen 2026-11-01 with a `>=` comparison), so put any comparison in a script file under artifacts/review-evidence/. `python3 tools/board.py validate <review file>` is allowed and prints 'ok' or the D.2 error. Related: [[source-fetching]], [[plan-review-patterns]]."
}
````

### User / tool · 2026-11-02T01:31:45.577Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:46.388Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md",
 "old_string": "- [Plan/contract review patterns](feedback_plan_review_patterns.md) — mention-coverage, unowned tests, wrong critical path, fixture-replay ship bar; probe script",
 "new_string": "- [Plan/contract review patterns](feedback_plan_review_patterns.md) — mention-coverage, unowned tests, wrong critical path, fixture-replay ship bar; apply-check defects (appended-not-edited, either/or, stale text); probe scripts"
}
````

### User / tool · 2026-11-02T01:31:46.484Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:51.710Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/project_t017_t018_review_history.md",
 "content": "---\nname: t017-t018-review-history\ndescription: T-017 plan / T-018 contract review rounds (2026-11-01 to 11-02) — round-1 verdicts all 'changes', round-2 apply-check verdicts 'changes' with 9 contract majors and 4 T-017 majors still open\nmetadata:\n  type: project\n---\n\nState as of the round-2 apply-check (this review), not a live status. Re-check the board before acting on it.\n\n- Round 1: CONTRACT-M2M3-{product-manager,paralegal,staff-engineer}.md, all 'changes' (6 + 4 + 9 majors). reviews/T-017-product-manager.md 'changes' (4 majors). Source of the fix texts.\n- Round 2 (this review): reviews/T-018-product-manager.md 'changes': 10 majors (9 of 19 contract majors not applied, plus N1, T-018 AC2 ticked on a refuted claim). reviews/T-017-product-manager-r2.md 'changes': 4 majors not applied.\n- Still open: pass-condition column in docs/M2M3_COVERAGE.md; the lexicon-recall release gate (LLM_VS_CODE rows 12/16 vs T-038 AC9 'or'); row-10 engine decision; 11 unowned test files (applied-check qa:NONE=11); T-039 AC1/AC2 and T-033 AC1 contradictions left in place; stale 5-card chain at coverage lines 18-19.\n- Applied and verified: T-048 qa card; deps T-031/T-042/T-043; T-034 max_retries=0 and FixtureMissing; judge error paths; boundary module list; paralegal edit-reload, two-date conflict and record-4 ACs; verify_quickly in the paralegal agent body.\n\n**Why:** The orchestrator's round-2 claim ('every blocker/major applied') closed T-018 AC2. Without this record, a future reviewer would assume the M2 contract is settled.\n\n**How to apply:** On any future apply round, re-run artifacts/review-evidence/T-018-r2-applied-check.py and compare against the open list above. Check the lexicon gate decision first: cut (3) of the M2 cut order depends on it. See [[plan-review-patterns]] for the apply-check defects.\n"
}
````

### User / tool · 2026-11-02T01:31:51.804Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/project_t017_t018_review_history.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:52.781Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md",
 "old_string": "- [T-013/T-025 review history](project_t013_review_history.md) — r1-r3 + T-025 verdicts; open: false §8 'aligned' claims, circular authority, must_not M1–M14 vs M17",
 "new_string": "- [T-013/T-025 review history](project_t013_review_history.md) — r1-r3 + T-025 verdicts; open: false §8 'aligned' claims, circular authority, must_not M1–M14 vs M17\n- [T-017/T-018 review history](project_t017_t018_review_history.md) — round-1 and round-2 apply-check verdicts (changes); open: gate decision, pass-condition column, 11 unowned tests"
}
````

### User / tool · 2026-11-02T01:31:52.886Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/product-manager-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:31:57.777Z

Both reviews are written and pass `board.py validate`. Verdict is **changes** for both: T-018 has 9 of 19 contract majors not applied, plus a new major that T-018 AC2 is ticked on a refuted claim. T-017 r2 has all 4 majors not applied (no pass-condition column, 3 contradictory ACs with no self-check, 11 unowned test files and the row-10 engine open, critical path still stale at coverage lines 18-19).
Files: `/Users/arsis/zlayt-pm-project/reviews/T-018-product-manager.md` and `/Users/arsis/zlayt-pm-project/reviews/T-017-product-manager-r2.md`. Evidence: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-018-r2-applied-check.out.txt` (68 checks, 31 pass, 37 fail).
Model is `claude-haiku-5-5` as the runtime reports it; the dossier expects `claude-opus-5-5`, so please confirm which id you want on the record. Unapplied minors (12 items) are reported but not gating; one question for Chris is in both files (is the lexicon recall a release gate).
